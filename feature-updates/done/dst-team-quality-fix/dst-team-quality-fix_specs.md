# D/ST Team Quality Fix - Specification

## Objective

Fix the team quality multiplier (Step 4 of scoring algorithm) for D/ST positions to use the correct ranking metric based on D/ST fantasy points scored instead of fantasy points allowed to opponents.

---

## Problem Statement

### Current (Incorrect) Behavior

For D/ST positions, the scoring system:
1. Uses `team_defensive_rank` from TeamDataManager
2. This rank is calculated from `points_allowed` in `team_data/*.csv`
3. `points_allowed` = total fantasy points allowed to ALL opposing players (QB+RB+WR+TE+K)
4. Higher points allowed → worse defensive rank → lower team quality multiplier

**Real-world example: Houston Texans D/ST**
- Week 15: Allowed 116.6 fantasy points to opponents
- Defensive rank: 24th out of 32 teams
- Team quality rating: VERY_POOR (0.95x multiplier)
- **BUT**: Houston D/ST scored 6.0 fantasy points in week 15, ranked 9th
- **Season-long**: Houston D/ST averages 9.34 ppg, ranked #2 in the entire league!

### Root Cause

The `points_allowed` metric measures how well the opposing offense performs against the team, NOT how well the D/ST unit performs in fantasy football.

- High `points_allowed` = Good opposing offenses (irrelevant to D/ST fantasy value)
- Low `points_allowed` = Bad opposing offenses (also irrelevant)

**D/ST fantasy scoring is actually based on:**
- Sacks, interceptions, fumbles recovered
- Defensive/Special teams touchdowns
- Points allowed (real NFL points, not fantasy points)
- Safeties, blocked kicks, etc.

---

## Desired Behavior (Correct)

For D/ST positions, the team quality multiplier should be based on:
- **D/ST fantasy points SCORED** (from `players.csv` weekly_points data)
- Ranking D/ST units by their actual fantasy performance
- Higher fantasy points scored → better rank → higher team quality multiplier

**Example with fix: Houston Texans D/ST**
- Season average: 9.34 ppg
- Rank: #2 out of 32 teams
- Team quality rating: EXCELLENT (1.05x multiplier)

---

## Solution Options

### Option 1: Add D/ST-Specific Ranking Calculation

**Approach:**
1. Add new ranking method to TeamDataManager: `get_dst_fantasy_rank(team)`
2. Calculate D/ST fantasy rankings from `players.csv` weekly D/ST scores
3. Use rolling window (MIN_WEEKS) like other rankings
4. Modify `player_scoring.py` to use D/ST-specific rank for D/ST positions

**Code Changes:**

**TeamDataManager.py:**
```python
def get_dst_fantasy_rank(self, team: str) -> int:
    """
    Get D/ST fantasy performance rank (1=best, 32=worst).
    Based on D/ST fantasy points scored, not points allowed.
    """
    # Calculate from players.csv D/ST weekly scores
    # Use rolling window like offensive/defensive ranks
    pass

def _rank_dst_fantasy(self, totals: Dict[str, tuple]) -> None:
    """Rank teams by D/ST fantasy points scored (more points = better = rank 1)."""
    # Calculate per-game averages
    # Sort by average descending (most points = rank 1)
    pass
```

**player_scoring.py:**
```python
def _apply_team_quality_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply team quality multiplier (Step 4)."""
    quality_val = p.team_offensive_rank
    if p.position in Constants.DEFENSE_POSITIONS:
        quality_val = p.team_dst_fantasy_rank  # NEW: D/ST-specific rank

    multiplier, rating = self.config.get_team_quality_multiplier(quality_val)
    reason = f"Team Quality: {rating} ({multiplier:.2f}x)"
    return player_score * multiplier, reason
```

**PlayerManager.py:**
```python
# Load team quality rankings for scoring calculations
player.team_offensive_rank = self.team_data_manager.get_team_offensive_rank(player.team)
player.team_defensive_rank = self.team_data_manager.get_team_defensive_rank(player.team)
if player.position in Constants.DEFENSE_POSITIONS:
    player.team_dst_fantasy_rank = self.team_data_manager.get_dst_fantasy_rank(player.team)
```

**Pros:**
- Most accurate - reflects actual D/ST fantasy performance
- Consistent with team quality philosophy for other positions
- Enables proper differentiation between elite and poor D/ST units

**Cons:**
- More complex implementation
- Requires new data processing logic
- Additional attribute on FantasyPlayer model

---

### Option 2: Disable Team Quality for D/ST

**Approach:**
Return neutral multiplier (1.0x) for D/ST positions, effectively disabling team quality adjustment.

**Code Changes:**

**player_scoring.py:**
```python
def _apply_team_quality_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply team quality multiplier (Step 4)."""
    # Skip team quality for D/ST - their value is captured in projected points
    if p.position in Constants.DEFENSE_POSITIONS:
        return player_score, "Team Quality: N/A (D/ST)"

    quality_val = p.team_offensive_rank
    multiplier, rating = self.config.get_team_quality_multiplier(quality_val)
    reason = f"Team Quality: {rating} ({multiplier:.2f}x)"
    return player_score * multiplier, reason
```

**Pros:**
- Simplest implementation (minimal code changes)
- Avoids incorrect metric entirely
- D/ST value already captured in projected points

**Cons:**
- Less sophisticated than Option 1
- Misses opportunity to differentiate elite vs poor D/ST units
- Inconsistent with how team quality works for other positions

---

## High-Level Requirements

### Functional Requirements

1. **Correct Ranking Metric**
   - D/ST team quality must be based on D/ST fantasy points scored
   - Elite D/ST units (top 6) should receive EXCELLENT/GOOD ratings (1.05x-1.02x)
   - Poor D/ST units (bottom 6) should receive POOR/VERY_POOR ratings (0.98x-0.95x)

2. **Data Source**
   - Use `players.csv` weekly D/ST fantasy points
   - Apply rolling window (MIN_WEEKS) for recent performance weighting
   - Handle bye weeks and missing data appropriately

3. **Integration**
   - Maintain consistency with existing team quality system
   - Preserve behavior for non-D/ST positions
   - Update only D/ST-specific logic

### Non-Functional Requirements

1. **Testing**
   - Unit tests for D/ST ranking calculation
   - Verification tests for Houston D/ST (should be EXCELLENT)
   - Regression tests for non-D/ST positions (unchanged)
   - Integration test for full scoring calculation

2. **Documentation**
   - Update `docs/scoring/04_team_quality_multiplier.md`
   - Document D/ST-specific logic and rationale
   - Add example calculations

3. **Backward Compatibility**
   - Changes D/ST scoring when TEAM_QUALITY_WEIGHT > 0
   - No impact when WEIGHT = 0.0 (current state)
   - Simulation results may change when team quality enabled

---

## Data Verification

### Current D/ST Fantasy Rankings (Season-long)

Based on `players.csv` data:

| Rank | Team | Avg PPG | Current Quality Rating | Expected Quality Rating |
|------|------|---------|------------------------|-------------------------|
| 1 | SEA | 9.89 | ? | EXCELLENT (1.05x) |
| 2 | HOU | 9.34 | VERY_POOR ❌ | EXCELLENT (1.05x) |
| 3 | DEN | 7.52 | ? | EXCELLENT (1.05x) |
| 4 | JAX | 7.39 | ? | EXCELLENT (1.05x) |
| 5 | NE | 7.21 | ? | EXCELLENT (1.05x) |
| 6 | CLE | 7.20 | ? | EXCELLENT (1.05x) |

### Current Defensive Ranks (by points_allowed)

| Rank | Team | Pts Allowed | Quality Rating |
|------|------|-------------|----------------|
| 1 | PHI | 52.0 | EXCELLENT |
| ... | ... | ... | ... |
| 24 | HOU | 116.6 | VERY_POOR |

This clearly shows the mismatch between actual D/ST fantasy performance (#2) and incorrect team quality rating (VERY_POOR).

---

## Open Questions

*(To be populated during Phase 2 investigation)*

### Data Source Questions
- [ ] Where exactly in `players.csv` are D/ST weekly scores stored?
- [ ] What is the format of D/ST player names/IDs?
- [ ] How are bye weeks handled in the data?

### Algorithm Questions
- [ ] Should D/ST ranking use the same MIN_WEEKS threshold as offensive/defensive ranks?
- [ ] How to handle missing data for D/ST units with incomplete game history?

### Architecture Questions
- [ ] Which solution option should we implement (Option 1 vs Option 2)?
- [ ] If Option 1: Where should D/ST ranking calculation live?
- [ ] If Option 1: Should `team_dst_fantasy_rank` be a new attribute on FantasyPlayer?

### Testing Questions
- [ ] What should the acceptance criteria be for "correct" D/ST rankings?
- [ ] How to test edge cases (new teams, missing data, bye weeks)?

### Integration Questions
- [ ] Does `TeamDataManager` already have patterns we should follow?
- [ ] How are other rankings (offensive/defensive) currently calculated?
- [ ] Are there existing tests for team quality multiplier that need updating?

---

## Resolved Implementation Details

### Solution Choice (Q1.1) - RESOLVED 2025-12-21

**Decision**: Implement Option 1 - Add D/ST-Specific Ranking

**Implementation Approach:**
- Add `_rank_dst_fantasy()` method to TeamDataManager (follows pattern of `_rank_offensive()`)
- Add `get_team_dst_fantasy_rank(team: str) -> Optional[int]` getter to TeamDataManager
- Modify PlayerManager.load_players() to populate `team_defensive_rank` differently for D/ST:
  - For D/ST positions: `player.team_defensive_rank = get_team_dst_fantasy_rank()`
  - For other positions: `player.team_defensive_rank = get_team_defensive_rank()` (unchanged)
- ScoringCalculator._apply_team_quality_multiplier() requires NO changes (already uses team_defensive_rank for D/ST)

**Rationale:**
- Most accurate approach - reflects actual D/ST fantasy performance
- Consistent with team quality philosophy for other positions
- Differentiates elite (Houston #2, Seattle #1) from poor D/ST units
- When TEAM_QUALITY_WEIGHT is enabled, provides appropriate boost/penalty
- Codebase already has ranking infrastructure to support this pattern

**Files Affected:**
1. `league_helper/util/TeamDataManager.py` - Add D/ST ranking calculation
2. `league_helper/util/PlayerManager.py` - Set team_defensive_rank differently for D/ST positions
3. `tests/league_helper/util/test_PlayerManager_scoring.py` - Update/add tests
4. `docs/scoring/04_team_quality_multiplier.md` - Document D/ST logic

**Files NOT Affected:**
- `utils/FantasyPlayer.py` - No changes (reusing existing team_defensive_rank attribute)
- `league_helper/util/player_scoring.py` - No changes (already uses team_defensive_rank for D/ST)

### MIN_WEEKS Threshold (Q1.2) - RESOLVED 2025-12-21

**Decision**: D/ST fantasy rankings use same MIN_WEEKS threshold as offensive/defensive rankings

**Implementation:**
- D/ST ranking calculation uses `team_quality_min_weeks` from ConfigManager
- Same rolling window approach as `_rank_offensive()` and `_rank_defensive()`
- No new configuration parameter needed

**Rationale:**
- Consistency - all team quality rankings share same recency preference
- Simplicity - leverages existing config parameter
- User controls recency in one place
- No evidence D/ST performance trends differ from team offense/defense trends

**Code Reference:**
```python
# In TeamDataManager._calculate_rankings()
team_quality_min_weeks = self.config_manager.get_team_quality_min_weeks()

# Calculate D/ST rankings using same window as offensive/defensive
dst_start_week = max(1, end_week - team_quality_min_weeks + 1)
# Use weeks dst_start_week through end_week for D/ST ranking
```

### Incomplete Game History Handling (Q1.3) - RESOLVED 2025-12-21

**Decision**: Assign neutral rank 16 until MIN_WEEKS threshold is met

**Implementation:**
- Follow existing pattern in TeamDataManager._calculate_rankings() (lines 120-125)
- When `current_nfl_week <= team_quality_min_weeks`, call `_set_neutral_rankings()`
- Update `_set_neutral_rankings()` to include: `self.dst_fantasy_ranks[team] = 16`
- Rank 16 = neutral (middle of 32 teams) → results in neutral team quality multiplier

**Rationale:**
- Consistent with existing offensive/defensive ranking behavior
- Ensures minimum data quality before making ranking decisions
- Prevents early-season volatility from affecting D/ST team quality scores
- Rank 16 produces neutral multiplier via ConfigManager.get_team_quality_multiplier()

**Code Reference:**
```python
# In TeamDataManager._set_neutral_rankings()
def _set_neutral_rankings(self) -> None:
    """Set all rankings to neutral (16) for early season."""
    for team in NFL_TEAMS:
        self.offensive_ranks[team] = 16
        self.defensive_ranks[team] = 16
        self.dst_fantasy_ranks[team] = 16  # NEW: Add D/ST neutral ranking
        self.position_ranks[team] = {
            'QB': 16, 'RB': 16, 'WR': 16, 'TE': 16, 'K': 16
        }
```

### Bye Week Handling (Q1.5) - RESOLVED 2025-12-21

**Decision**: Skip weeks where week_N_points is None or 0

**Implementation:**
- When iterating through weeks in rolling window, skip weeks where D/ST week_N_points is None or 0
- Only count games actually played in the average calculation
- Consistent with existing bye week handling pattern

**Rationale:**
- Consistent with offensive/defensive ranking bye week logic (skip zeros)
- Fair comparison - D/ST didn't play poorly, they didn't play at all
- Accurate ppg - points per game played, not points per calendar week
- Handles both None (field unpopulated) and 0.0 (explicit zero) representations

**Code Reference:**
```python
# In TeamDataManager._rank_dst_fantasy()
for week_num in range(dst_start_week, end_week + 1):
    week_points = getattr(dst_player, f'week_{week_num}_points', None)

    # Skip bye weeks (None or 0)
    if week_points is None or week_points == 0:
        continue

    total_points += week_points
    games_played += 1

avg_ppg = total_points / games_played if games_played > 0 else 0.0
```

### TEAM_QUALITY_WEIGHT Application (Q1.8) - RESOLVED 2025-12-21

**Decision**: TEAM_QUALITY_WEIGHT applies to D/ST team quality multiplier same as other positions

**Implementation:**
- No special case logic needed in ScoringCalculator
- D/ST uses team_dst_fantasy_rank to get multiplier from ConfigManager
- WEIGHT parameter affects D/ST multiplier same as QB, RB, WR, TE, K

**Rationale:**
- Consistency - all positions affected by TEAM_QUALITY_WEIGHT uniformly
- User control - single parameter controls team quality impact for all positions
- Simplicity - no special case logic needed
- Logical behavior when weight changes:
  - WEIGHT = 0.0 → All positions (including D/ST) get neutral 1.0x
  - WEIGHT = 0.5 → All positions (including D/ST) get partial multiplier effect
  - WEIGHT = 1.0 → All positions (including D/ST) get full multiplier effect

**Code Impact:**
- No changes needed to existing WEIGHT application logic
- ScoringCalculator._apply_team_quality_multiplier() will use dst_fantasy_rank for D/ST
- ConfigManager.get_team_quality_multiplier() returns multiplier based on rank
- Existing WEIGHT application logic applies multiplier uniformly

### Logging (Q2.1) - RESOLVED 2025-12-21

**Decision**: Match existing debug-level logging pattern for offensive/defensive rankings

**Implementation:**
- Add debug logging when D/ST ranking calculation starts (which weeks used)
- Add debug logging when D/ST ranking calculation completes (how many teams)
- Follow same format as existing TeamDataManager logging

**Rationale:**
- Consistency with existing offensive/defensive ranking logs
- Debug level appropriate (not spammy in production)
- Provides sufficient detail for verification and troubleshooting
- User guidance: "Match the existing pattern whenever possible"

**Code Reference:**
```python
# In TeamDataManager._calculate_rankings()
dst_start_week = max(1, end_week - team_quality_min_weeks + 1)
self.logger.debug(f"D/ST fantasy rankings from weeks {dst_start_week}-{end_week}")

# ... calculation logic ...

self.logger.debug(f"Calculated D/ST fantasy rankings for {len(self.dst_fantasy_ranks)} teams")
```

### Before/After Logging (Q2.2) - RESOLVED 2025-12-21

**Decision**: No special before/after comparison logging

**Implementation:**
- No additional logging beyond standard debug logs (Q2.1)
- No temporary logging to show old vs new ranks
- Tests will verify correctness instead of production logs

**Rationale:**
- Matches existing pattern (no before/after logs elsewhere in codebase)
- Tests provide same verification capability
- Simpler implementation (no temporary code to remove)
- Regular debug logging is sufficient for troubleshooting
- User guidance: "Match the existing pattern whenever possible"

### Eager Calculation (Q2.4) - RESOLVED 2025-12-21

**Decision**: Calculate D/ST rankings eagerly in _calculate_rankings()

**Implementation:**
- D/ST rankings calculated in TeamDataManager._calculate_rankings() at initialization
- Called alongside offensive, defensive, and position-specific rankings
- No lazy loading or on-demand calculation

**Rationale:**
- Matches existing pattern (all rankings calculated eagerly at init)
- Consistent with how offensive_ranks and defensive_ranks are populated
- Simpler - no need for lazy loading infrastructure
- User guidance: Match existing pattern

**Code Reference:**
```python
# In TeamDataManager.__init__() - lines 87-88
self._load_team_data()
self._calculate_rankings()  # Calculates ALL rankings including D/ST

# In TeamDataManager._calculate_rankings()
self._rank_offensive(offensive_totals)
self._rank_defensive(defensive_totals)
self._rank_dst_fantasy(dst_totals)  # NEW: Calculate D/ST rankings
self._rank_positions(position_totals, positions)
```

### D/ST Ranking Pattern (Q3.1) - RESOLVED 2025-12-21

**Decision**: Follow offensive ranking pattern (descending sort, more points = rank 1)

**Implementation:**
- Sort D/ST teams by fantasy points descending
- Most fantasy points = rank 1 (best)
- Least fantasy points = rank 32 (worst)
- Same sorting direction as _rank_offensive()

**Rationale:**
- D/ST fantasy points are like offensive points (higher is better)
- NOT like defensive points_allowed (where lower is better)
- Matches existing offensive pattern for "scoring" metrics
- User guidance: Match existing pattern

**Code Reference:**
```python
# In TeamDataManager._rank_dst_fantasy()
def _rank_dst_fantasy(self, totals: Dict[str, tuple]) -> None:
    """Rank teams by D/ST fantasy production (more points = better = rank 1)."""
    # Calculate per-game averages
    averages = []
    for team, (total, games) in totals.items():
        avg = total / games if games > 0 else 0
        averages.append((team, avg))

    # Sort by average descending (most points = rank 1) - MATCHES OFFENSIVE PATTERN
    averages.sort(key=lambda x: x[1], reverse=True)

    for rank, (team, _) in enumerate(averages, 1):
        self.dst_fantasy_ranks[team] = rank
```

### TeamDataManager Method Pattern (Q3.3) - RESOLVED 2025-12-21

**Decision**: Add get_team_dst_fantasy_rank(team) following existing getter pattern

**Implementation:**
- Add public getter method with same signature as get_team_offensive_rank()
- Returns Optional[int] (None if team not found)
- Follows same naming convention and pattern

**Rationale:**
- Consistency with existing TeamDataManager API
- Same signature and return type as other getters
- Predictable interface for callers
- User guidance: Match existing pattern

**Code Reference:**
```python
# In TeamDataManager - add alongside existing getters
def get_team_offensive_rank(self, team: str) -> Optional[int]:
    """Get team's offensive rank (1=best, 32=worst)."""
    return self.offensive_ranks.get(team)

def get_team_defensive_rank(self, team: str) -> Optional[int]:
    """Get team's defensive rank (1=best, 32=worst)."""
    return self.defensive_ranks.get(team)

def get_team_dst_fantasy_rank(self, team: str) -> Optional[int]:  # NEW
    """Get team's D/ST fantasy rank (1=best, 32=worst)."""
    return self.dst_fantasy_ranks.get(team)
```

### Test Coverage (Q2.5) - RESOLVED 2025-12-21

**Decision**: Implement full test suite (10 tests)

**Test Plan:**

**Unit Tests - TeamDataManager (6 tests):**
1. **test_rank_dst_fantasy_calculates_correctly**
   - Setup: Mock D/ST players with known weekly scores
   - Verify: Teams ranked correctly (most points = rank 1)
   - Assert: Houston (9.34 ppg) > Denver (7.52 ppg)

2. **test_rank_dst_fantasy_handles_bye_weeks**
   - Setup: D/ST with None and 0 values for bye weeks
   - Verify: Bye weeks skipped in average calculation
   - Assert: avg = sum(non-bye weeks) / games_played

3. **test_rank_dst_fantasy_handles_negative_scores**
   - Setup: D/ST with negative weekly scores (e.g., -5.0)
   - Verify: Negative scores included in total
   - Assert: avg includes negatives (can be < 0)

4. **test_rank_dst_fantasy_missing_team_returns_none**
   - Setup: Request rank for non-existent team
   - Verify: get_team_dst_fantasy_rank() returns None
   - Assert: None leads to neutral 1.0x multiplier

5. **test_rank_dst_fantasy_uses_rolling_window**
   - Setup: current_week=10, MIN_WEEKS=4
   - Verify: Only weeks 6-9 included in calculation
   - Assert: Weeks 1-5 and 10+ not counted

6. **test_rank_dst_fantasy_neutral_early_season**
   - Setup: current_week=3, MIN_WEEKS=4
   - Verify: _set_neutral_rankings() called
   - Assert: All teams get rank 16

**Integration Tests - PlayerManager (2 tests):**
7. **test_dst_uses_dst_fantasy_rank_not_defensive_rank**
   - Setup: D/ST player with dst_fantasy_rank=2, defensive_rank=24
   - Score player with team_quality=True
   - Verify: Uses rank 2 (EXCELLENT), not rank 24 (VERY_POOR)
   - Assert: Multiplier matches rank 2

8. **test_offensive_players_unchanged**
   - Setup: QB, RB, WR, TE, K players
   - Score with team_quality=True
   - Verify: Still use team_offensive_rank
   - Assert: No behavioral changes for non-D/ST

**Regression Tests (2 tests):**
9. **Update test_team_quality_defense_uses_defensive_rank** (line 737)
   - Change assertion to check dst_fantasy_rank instead
   - Verify: DST uses new ranking system
   - Keep test structure, change what's being tested

10. **test_houston_dst_gets_excellent_rating**
    - Setup: Load real Houston D/ST data (9.34 ppg season avg)
    - Calculate dst_fantasy_rank
    - Verify: Rank in range 1-6 (EXCELLENT tier)
    - Assert: Rating is "EXCELLENT" or "GOOD", NOT "VERY_POOR"

**Rationale:**
- Comprehensive coverage matching existing test patterns
- Protects against regressions (edge cases, early season, integration)
- Meets project quality standards (2200+ tests, 100% pass rate requirement)
- Each edge case identified in planning gets explicit test coverage

### Update Existing Test (Q2.6) - RESOLVED 2025-12-21

**Decision**: Update existing test `test_team_quality_defense_uses_defensive_rank` (line 737)

**Implementation:**
- Keep test structure and name (or rename to `test_team_quality_defense_uses_dst_fantasy_rank`)
- Change assertions to verify dst_fantasy_rank instead of defensive_rank
- Preserve test intent: "D/ST uses correct team ranking for quality multiplier"

**Rationale:**
- Preserves test history (git blame shows test evolution)
- Minimal changes (update assertions, not delete + add)
- Clear diff shows exactly what changed
- Test intent unchanged (D/ST uses appropriate rank)

**Code Changes:**
```python
# BEFORE (line 737-746)
def test_team_quality_defense_uses_defensive_rank(self, player_manager, test_player):
    """DST position should use team_defensive_rank"""
    test_player.team_offensive_rank = 25  # Bad offense
    test_player.team_defensive_rank = 3   # Good defense
    test_player.position = "DST"
    base_score = 100.0
    result, reason = player_manager.scoring_calculator._apply_team_quality_multiplier(test_player, base_score)
    # Should use defensive rank (3) which is EXCELLENT
    assert result == 100.0 * 1.30
    assert reason == "Team Quality: EXCELLENT (1.30x)"

# AFTER (modified)
def test_team_quality_defense_uses_dst_fantasy_rank(self, player_manager, test_player):
    """DST position should use team_dst_fantasy_rank"""
    test_player.team_offensive_rank = 25  # Bad offense
    test_player.team_dst_fantasy_rank = 3   # Good D/ST fantasy performance (NEW)
    test_player.position = "DST"
    base_score = 100.0
    result, reason = player_manager.scoring_calculator._apply_team_quality_multiplier(test_player, base_score)
    # Should use dst_fantasy_rank (3) which is EXCELLENT (CHANGED)
    assert result == 100.0 * 1.30
    assert reason == "Team Quality: EXCELLENT (1.30x)"
```

### Test Fixtures (Q2.7) - RESOLVED 2025-12-21

**Decision**: Use pytest fixtures matching existing test pattern

**Implementation:**
- Use `@pytest.fixture` decorator for reusable test data
- Create mock FantasyPlayer objects with known D/ST weekly scores
- Use `unittest.mock.Mock` for external dependencies (PlayerManager, ConfigManager)
- Follow existing fixture patterns in test_PlayerManager_scoring.py

**Rationale:**
- Matches existing test infrastructure (pytest + unittest.mock)
- Consistent with how other tests create fixtures
- Reusable across multiple test functions
- User guidance: Match existing pattern

**Example Fixture:**
```python
@pytest.fixture
def mock_dst_players():
    """Create mock D/ST players with known weekly scores for testing."""
    houston = FantasyPlayer(
        id=-16034, name="Texans D/ST", team="HOU", position="DST",
        week_1_points=8.0, week_2_points=5.0, week_3_points=12.0, week_4_points=9.0,
        week_5_points=10.0, week_6_points=7.0
    )
    seattle = FantasyPlayer(
        id=-16026, name="Seahawks D/ST", team="SEA", position="DST",
        week_1_points=10.0, week_2_points=12.0, week_3_points=11.0, week_4_points=9.0,
        week_5_points=11.0, week_6_points=10.0
    )
    denver = FantasyPlayer(
        id=-16007, name="Broncos D/ST", team="DEN", position="DST",
        week_1_points=5.0, week_2_points=-5.0, week_3_points=6.0, week_4_points=7.0,
        week_5_points=6.0, week_6_points=8.0
    )
    return {"HOU": houston, "SEA": seattle, "DEN": denver}

@pytest.fixture
def mock_team_data_manager(mock_dst_players):
    """Create mock TeamDataManager with D/ST ranking capability."""
    manager = Mock()
    manager.get_team_dst_fantasy_rank = Mock(side_effect=lambda team: {
        "HOU": 2,   # Good D/ST
        "SEA": 1,   # Best D/ST
        "DEN": 10   # Mid-tier D/ST
    }.get(team))
    return manager
```

### FantasyPlayer Attribute (Q3.7 & Q3.8) - RESOLVED 2025-12-21

**Decision**: Reuse existing `team_defensive_rank` attribute (NO new attribute needed)

**Implementation:**
- FantasyPlayer dataclass unchanged (no new attribute)
- For D/ST positions: `team_defensive_rank` contains D/ST fantasy rank
- For other positions: `team_defensive_rank` contains defensive rank (unchanged behavior)
- ScoringCalculator unchanged (already uses `team_defensive_rank` for D/ST positions)

**Rationale:**
- Simpler - no data model changes required
- Cleaner - attribute meaning adapts based on position
- Less code changes - player_scoring.py requires no modification
- Existing pattern - team_defensive_rank already used for D/ST in scoring logic

**Code Changes:**
```python
# In PlayerManager.load_players() - BEFORE
player.team_offensive_rank = self.team_data_manager.get_team_offensive_rank(player.team)
player.team_defensive_rank = self.team_data_manager.get_team_defensive_rank(player.team)

# In PlayerManager.load_players() - AFTER
player.team_offensive_rank = self.team_data_manager.get_team_offensive_rank(player.team)

# Set team_defensive_rank based on position
if player.position in Constants.DEFENSE_POSITIONS:
    # For D/ST: use D/ST fantasy ranking
    player.team_defensive_rank = self.team_data_manager.get_team_dst_fantasy_rank(player.team)
else:
    # For others: use traditional defensive ranking (points allowed)
    player.team_defensive_rank = self.team_data_manager.get_team_defensive_rank(player.team)
```

**Semantic Shift:**
- `team_defensive_rank` meaning for D/ST: "How good is this team's D/ST unit at fantasy football?"
- `team_defensive_rank` meaning for others: "How good is this team's defense at limiting opponent points?"

### Documentation Updates (Q3.9) - RESOLVED 2025-12-21

**Decision**: Update all documentation (scoring docs, ARCHITECTURE.md, inline docstrings)

**Required Updates:**

**1. docs/scoring/04_team_quality_multiplier.md**
- Add D/ST-specific section after main algorithm description
- Explain why D/ST uses different metric than team_defensive_rank for other positions
- Document that D/ST uses fantasy points scored, not points_allowed
- Add example: "Houston D/ST ranks #2 by fantasy points (9.34 ppg) → EXCELLENT rating"
- Clarify semantic difference in team_defensive_rank for D/ST vs other positions

**2. ARCHITECTURE.md - TeamDataManager section**
- Document new `_rank_dst_fantasy()` method
- Document new `get_team_dst_fantasy_rank()` getter
- Explain D/ST ranking uses players.csv weekly scores instead of team_data/*.csv
- Note semantic shift: team_defensive_rank contains different metrics based on position

**3. Inline Docstrings**

Add docstrings for new methods:
```python
def _rank_dst_fantasy(self, totals: Dict[str, tuple]) -> None:
    """
    Rank teams by D/ST fantasy production (more points = better = rank 1).

    Unlike defensive_rank which measures points allowed to opponents,
    dst_fantasy_rank measures how many fantasy points the D/ST unit scores.
    This provides accurate team quality assessment for D/ST positions.

    Args:
        totals: Dict mapping team -> (total_points, games_played)

    Side Effects:
        Populates self.dst_fantasy_ranks with team rankings
    """

def get_team_dst_fantasy_rank(self, team: str) -> Optional[int]:
    """
    Get team's D/ST fantasy performance rank (1=best, 32=worst).

    Based on D/ST fantasy points scored, not defensive points allowed.
    Used for D/ST team quality multiplier calculation.

    Args:
        team: Team abbreviation (e.g., 'HOU', 'SEA')

    Returns:
        Rank 1-32, or None if team not found
    """
```

Update PlayerManager.load_players() comment:
```python
# Set team_defensive_rank based on position
# For D/ST: use D/ST fantasy ranking (how good at scoring fantasy points)
# For others: use traditional defensive ranking (how good at limiting opponent points)
if player.position in Constants.DEFENSE_POSITIONS:
    player.team_defensive_rank = self.team_data_manager.get_team_dst_fantasy_rank(player.team)
else:
    player.team_defensive_rank = self.team_data_manager.get_team_defensive_rank(player.team)
```

**Rationale:**
- Comprehensive documentation helps future agents understand D/ST-specific behavior
- ARCHITECTURE.md update maintains system documentation accuracy
- Inline docstrings follow existing code documentation standards
- Prevents confusion about team_defensive_rank semantic shift

---



## Dependency Map

### Module Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│ league_helper/util/player_scoring.py                           │
│   └─► _apply_team_quality_multiplier()                         │
│         │ (Line 519-533: MODIFIED)                             │
│         │ Checks p.position in Constants.DEFENSE_POSITIONS     │
│         │ OLD: Uses p.team_defensive_rank                      │
│         │ NEW: Uses p.team_dst_fantasy_rank                    │
│         └─► ConfigManager.get_team_quality_multiplier()        │
│                                                                 │
│ league_helper/util/PlayerManager.py                            │
│   └─► load_players()                                           │
│         │ (Lines 199-202: MODIFIED)                            │
│         │ Sets team rankings on each player                    │
│         │ NEW: For DST positions, also set dst_fantasy_rank   │
│         ├─► TeamDataManager.get_team_offensive_rank()          │
│         ├─► TeamDataManager.get_team_defensive_rank()          │
│         └─► TeamDataManager.get_team_dst_fantasy_rank() (NEW)  │
│                                                                 │
│ league_helper/util/TeamDataManager.py                          │
│   ├─► __init__()                                               │
│   │     └─► _calculate_rankings()                              │
│   │           │ (Line 104: MODIFIED)                           │
│   │           ├─► _rank_offensive()                            │
│   │           ├─► _rank_defensive()                            │
│   │           └─► _rank_dst_fantasy() (NEW)                    │
│   │                                                             │
│   ├─► _rank_dst_fantasy() (NEW METHOD)                         │
│   │     │ Similar to _rank_offensive()                         │
│   │     │ Loads D/ST weekly scores from players.csv           │
│   │     │ Calculates rolling window average                    │
│   │     │ Sorts descending (more points = rank 1)             │
│   │     └─► Populates self.dst_fantasy_ranks dict             │
│   │                                                             │
│   └─► get_team_dst_fantasy_rank(team) (NEW METHOD)             │
│         │ Returns rank for team's D/ST unit                    │
│         └─► Returns None if team not found                     │
│                                                                 │
│ utils/FantasyPlayer.py                                         │
│   └─► FantasyPlayer dataclass                                  │
│         │ (Line 132: NEW ATTRIBUTE)                            │
│         └─► team_dst_fantasy_rank: Optional[int] = None (NEW)  │
│                                                                 │
│ league_helper/constants.py                                     │
│   └─► DEFENSE_POSITIONS = ["DEF", "DST", "D/ST"]               │
│         │ (Line 68: READ ONLY - no changes)                    │
│         └─► Used to identify D/ST players                      │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

**Option 1 Implementation (D/ST-Specific Ranking):**

```
INPUT: data/players.csv
│ Contains D/ST entries with weekly scores:
│ - Position: "DST"
│ - Name: "{Team} D/ST"
│ - week_1_points, week_2_points, ..., week_17_points
│
▼
TeamDataManager.__init__()
│ Called during PlayerManager initialization
│
▼
TeamDataManager._calculate_rankings()
│ Determines rolling window (current_week - MIN_WEEKS)
│
├─► _rank_offensive() → offensive_ranks dict
├─► _rank_defensive() → defensive_ranks dict
└─► _rank_dst_fantasy() (NEW)
      │ Loads players.csv
      │ Filters to position="DST"
      │ For each team:
      │   - Sum week_N_points for weeks in rolling window
      │   - Calculate average (skip None/0 for bye weeks)
      │   - Sort descending (most points = rank 1)
      │ Populates dst_fantasy_ranks dict: {team: rank}
      │
      ▼
    get_team_dst_fantasy_rank(team) (NEW)
      │ Returns dst_fantasy_ranks[team]
      │ Returns None if team not found
      │
      ▼
PlayerManager.load_players()
│ For each player in players.csv:
│   - Set player.team_offensive_rank
│   - Set player.team_defensive_rank
│   - If player.position in DEFENSE_POSITIONS:
│       Set player.team_dst_fantasy_rank (NEW)
│
▼
PlayerManager.score_player(player, team_quality=True)
│
▼
ScoringCalculator._apply_team_quality_multiplier(player)
│ If player.position in DEFENSE_POSITIONS:
│   quality_val = player.team_dst_fantasy_rank (NEW)
│ Else:
│   quality_val = player.team_offensive_rank
│
▼
ConfigManager.get_team_quality_multiplier(quality_val)
│ Returns (multiplier, rating) based on rank
│ Examples:
│   - Rank 1-6: EXCELLENT (1.05x)
│   - Rank 25-32: VERY_POOR (0.95x)
│
▼
OUTPUT: Scored D/ST player with correct team quality multiplier
```

**Option 2 Implementation (Disable Team Quality for D/ST):**

```
PlayerManager.score_player(player, team_quality=True)
│
▼
ScoringCalculator._apply_team_quality_multiplier(player)
│ If player.position in DEFENSE_POSITIONS:
│   return (player_score * 1.0, "Team Quality: N/A (D/ST)")
│ Else:
│   ... (existing logic for offensive players)
│
▼
OUTPUT: D/ST gets neutral 1.0x multiplier (no boost or penalty)
```

---

## Assumptions

| Assumption | Basis | Risk if Wrong | Mitigation |
|------------|-------|---------------|------------|
| **D/ST weekly scores are in players.csv** | Verified with grep - found entries like "Texans D/ST" with week_N_points | Feature fails if D/ST data missing | Add validation to check D/ST entries exist |
| **DEFENSE_POSITIONS constant covers all variations** | Constants.py line 68: ["DEF", "DST", "D/ST"] | Miss some D/ST players if new format added | Test with actual data to verify all D/ST captured |
| **MIN_WEEKS threshold is appropriate for D/ST** | Current offensive/defensive rankings use same threshold | D/ST rankings might need different window | Make configurable if needed |
| **Negative D/ST scores are valid** | Confirmed in data: Broncos -5.0, Seahawks -5.0 | If negatives are errors, ranking will be wrong | No mitigation - negatives are legitimate D/ST scores |
| **Bye week scores are None or 0** | FantasyPlayer has bye_week field; confirmed pattern in TeamDataManager | If bye weeks have non-zero scores, will affect average | Skip weeks where week_N_points is None or 0 |
| **PlayerManager loads from players.csv at init** | Verified in PlayerManager.load_players() | If data source changes, our ranking won't find data | Read from same source as other player data |
| **TEAM_QUALITY_WEIGHT=0.0 currently** | Notes state "masked by WEIGHT=0.0" | If enabled before fix, will use wrong metric | Feature is backward compatible - works whether enabled or not |
| **Team abbreviations match between files** | players.csv uses "HOU", team_data uses "HOU.csv" | If mismatch, won't link D/ST to team | Use NFL_TEAMS constant for validation |
| **All 32 NFL teams have D/ST entries** | Standard fantasy football setup | If missing teams, those D/ST won't rank | Return None for missing teams (neutral multiplier) |
| **D/ST fantasy scoring doesn't vary by PPR** | D/ST scores based on sacks/TDs/points allowed, not receptions | If D/ST scoring varies by league type, ranking may be wrong | Verified - D/ST is not PPR-sensitive |

---

## Testing Requirements

### Integration Points

| Component A | Component B | Integration Mechanism | How to Verify |
|-------------|-------------|----------------------|---------------|
| TeamDataManager | players.csv | Loads D/ST weekly scores via CSV reading | Check dst_fantasy_ranks dict populated with 32 teams |
| TeamDataManager | PlayerManager | Returns dst_fantasy_rank via get_team_dst_fantasy_rank() | Mock TeamDataManager, verify PlayerManager calls method |
| PlayerManager | FantasyPlayer | Sets team_dst_fantasy_rank attribute | Verify attribute is set for D/ST positions |
| ScoringCalculator | FantasyPlayer | Reads team_dst_fantasy_rank for D/ST positions | Mock player with dst_fantasy_rank, verify used in calculation |
| ScoringCalculator | ConfigManager | Calls get_team_quality_multiplier() with dst rank | Verify rank passed correctly results in correct multiplier |

### Smoke Test Success Criteria

#### 1. Output Validation
- [ ] Houston D/ST team_dst_fantasy_rank is in range 1-6 (top tier)
- [ ] Houston D/ST gets EXCELLENT or GOOD rating (not VERY_POOR)
- [ ] Seattle D/ST (highest season avg) gets rank 1
- [ ] All 32 NFL teams have dst_fantasy_rank calculated (or None if missing data)
- [ ] D/ST with negative scores still ranked correctly (negatives included in average)

#### 2. Log Analysis
- [ ] Debug log shows "D/ST fantasy rankings from weeks X-Y" message
- [ ] No WARNING or ERROR messages related to D/ST ranking
- [ ] Log shows which teams got which ranks (top 6 and bottom 6 at minimum)

#### 3. Regression Testing
- [ ] Non-D/ST positions still use team_offensive_rank (QB, RB, WR, TE, K unchanged)
- [ ] Offensive rankings unchanged (same ranks as before)
- [ ] Defensive rankings unchanged (same ranks as before)
- [ ] All existing unit tests pass (100% pass rate)

#### 4. Comparison to Expected Values

Based on current data (season averages from players.csv):

| Team | Season Avg PPG | Expected Rank | Expected Rating | Current Rating (Wrong) |
|------|----------------|---------------|-----------------|------------------------|
| SEA | 9.89 | 1 | EXCELLENT | ? |
| HOU | 9.34 | 2 | EXCELLENT | VERY_POOR ❌ |
| DEN | 7.52 | 3 | EXCELLENT | ? |
| JAX | 7.39 | 4 | EXCELLENT | ? |
| NE | 7.21 | 5 | EXCELLENT | ? |
| CLE | 7.20 | 6 | EXCELLENT | ? |

**Acceptance Criteria**: After fix, all top-6 D/ST units should receive EXCELLENT or GOOD ratings (not POOR/VERY_POOR).

### Expected vs Actual Comparisons

| Test Case | Expected Result | How to Verify |
|-----------|-----------------|---------------|
| **Houston D/ST Scoring** | team_dst_fantasy_rank = 2, rating = "EXCELLENT" (1.05x) | Load real data, check HOU D/ST rank and multiplier |
| **Bye Week Handling** | Week with 0 or None points skipped in average | Create D/ST with bye week, verify average excludes that week |
| **Negative Score Handling** | Negative scores included in total | Create D/ST with negative week, verify included in average |
| **Missing Team Data** | dst_fantasy_rank = None, neutral 1.0x multiplier | Create D/ST for non-existent team, verify returns None |
| **Offensive Player Unchanged** | RB still uses team_offensive_rank | Score RB before/after fix, verify same rank used |
| **Rolling Window** | Only last MIN_WEEKS included | Mock current_week = 10, MIN_WEEKS = 4, verify only weeks 6-9 used |

### User-Facing Outputs

#### Console Output (if logging enabled)
- [ ] "Calculating D/ST fantasy rankings..." (debug level)
- [ ] "D/ST fantasy rankings: HOU=#2 (avg 9.34 ppg)" (debug level)

#### Files Created/Modified
- None (this is a scoring logic fix, not a data output feature)

#### Player Scoring Output
- [ ] When scoring D/ST with team_quality=True, reason includes "Team Quality: {rating} ({multiplier}x)"
- [ ] Rating matches D/ST fantasy performance (not defensive performance)

### Acceptance Testing Plan

#### Manual Verification Steps
1. Run unit tests: `python tests/run_all_tests.py`
   - [ ] All tests pass (100% rate)
2. Check Houston D/ST specifically:
   - [ ] Load players.csv in test
   - [ ] Calculate dst_fantasy_ranks
   - [ ] Verify HOU rank is 1-6 (EXCELLENT tier)
3. Score a D/ST player end-to-end:
   - [ ] Load D/ST from players.csv
   - [ ] Score with team_quality=True
   - [ ] Verify uses dst_fantasy_rank not defensive_rank
   - [ ] Verify multiplier matches expected tier

#### Comparison to Existing Feature
Compare to offensive/defensive ranking patterns:
- [ ] D/ST ranking uses same rolling window approach
- [ ] D/ST ranking follows offensive pattern (higher points = better rank)
- [ ] D/ST ranking integrates seamlessly with TeamDataManager
- [ ] No breaking changes to existing ranking infrastructure
