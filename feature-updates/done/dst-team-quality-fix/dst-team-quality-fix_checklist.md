# D/ST Team Quality Fix - Checklist

## Purpose

This checklist tracks all decisions and open questions that need resolution before implementation. Items marked `[x]` are resolved; items marked `[ ]` are pending.

---

## Resolution Log

**Progress:** 17/30 questions resolved (+ 11 resolved from codebase = 28/30 total)

**Codebase Investigation Complete:** Yes (2 verification rounds complete)

**Latest Resolution:** Q3.10 - Rationale documentation: Covered by Q3.9 - 2025-12-21

**PLANNING PHASE COMPLETE:** All user decision items resolved!

**User Guidance:** "Match the existing pattern whenever possible" - USER CONFIRMED: "For all checklist items where the options are 'matches existing pattern' or 'do something else', choose to match the existing pattern"

---

## Checklist Categories

### ITERATION 1: Edge Cases, Error Conditions, Configuration

#### Solution Choice
- [x] **Q1.1**: Which solution should we implement - Option 1 (D/ST-specific ranking) or Option 2 (disable team quality for D/ST)?
  - **Codebase Evidence**: Both are technically feasible based on current architecture
  - **Recommendation**: Option 1 (more accurate, aligns with team quality philosophy)
  - **✅ RESOLVED**: Option 1 - Add D/ST-specific ranking calculation
  - **Decision Date**: 2025-12-21
  - **Rationale**: More accurate, consistent with team quality philosophy, differentiates elite from poor D/ST units

#### Data Source
- [x] **Q1.2**: Should D/ST fantasy rankings use the same MIN_WEEKS threshold as team_offensive_rank and team_defensive_rank?
  - **Codebase Evidence**: `TeamDataManager._calculate_rankings()` uses `team_quality_min_weeks` from config (line 117)
  - **Current Value**: Needs verification from league_config.json
  - **Recommendation**: Yes, for consistency
  - **✅ RESOLVED**: Yes, use same `team_quality_min_weeks` threshold
  - **Decision Date**: 2025-12-21
  - **Rationale**: Consistency with existing rankings, simplicity, no evidence D/ST needs different window

- [x] **Q1.3**: How to handle D/ST units with incomplete game history (fewer than MIN_WEEKS games)?
  - **Codebase Evidence**: TeamDataManager checks `if current_nfl_week <= min_required` and calls `_set_neutral_rankings()` which assigns rank 16 (lines 120-125, 195-203)
  - **Options**: (A) Use available data with warning, (B) Assign neutral rank until MIN_WEEKS met
  - **Recommendation**: Option B - matches existing behavior
  - **✅ RESOLVED**: Assign neutral rank 16 until MIN_WEEKS threshold met
  - **Decision Date**: 2025-12-21
  - **Rationale**: Consistent with existing offensive/defensive ranking behavior, ensures minimum data quality, prevents early-season volatility

- [ ] **Q1.4**: How to extract D/ST weekly scores from players.csv?
  - **Codebase Evidence**: D/ST entries exist as position="DST", weekly scores in week_1_points through week_17_points
  - **Format**: "{Team} D/ST" (e.g., "Texans D/ST" for team "HOU")
  - **Status**: RESOLVED from codebase - use FantasyPlayer.week_N_points attributes

#### Edge Cases
- [x] **Q1.5**: How to handle bye weeks in D/ST ranking calculation?
  - **Codebase Evidence**: Current code skips weeks where `points_scored == 0 and points_allowed == 0` (TeamDataManager.py:149-150)
  - **D/ST Context**: bye_week field exists on FantasyPlayer, week_N_points will be 0 or None for bye
  - **Recommendation**: Skip weeks where week_N_points is None or 0 (consistent with current pattern)
  - **✅ RESOLVED**: Skip weeks where week_N_points is None or 0
  - **Decision Date**: 2025-12-21
  - **Rationale**: Consistent with existing bye week handling, fair comparison (didn't play vs played poorly), accurate ppg calculation

- [ ] **Q1.6**: How to handle negative D/ST scores in ranking?
  - **Codebase Evidence**: D/ST can score negative (e.g., Seahawks week 15: -5.0, Broncos week 2: -5.0)
  - **Impact**: Negative scores are valid fantasy points, should be included in average calculation
  - **Status**: No special handling needed - include in total like positive scores

- [ ] **Q1.7**: What if a team's D/ST has no data at all (new team, data missing)?
  - **Codebase Evidence**: Current code handles missing teams by returning None for ranks (leads to neutral multiplier)
  - **Recommendation**: Return None for team_dst_fantasy_rank → neutral 1.0x multiplier

#### Configuration
- [x] **Q1.8**: Should TEAM_QUALITY_WEIGHT apply to D/ST team quality multiplier?
  - **Codebase Evidence**: Currently WEIGHT = 0.0 (disabled), but when enabled should apply consistently
  - **Recommendation**: Yes, use same WEIGHT for D/ST as other positions
  - **✅ RESOLVED**: Yes, TEAM_QUALITY_WEIGHT applies to D/ST same as other positions
  - **Decision Date**: 2025-12-21
  - **Rationale**: Consistency across all positions, user controls impact via single parameter, simplicity (no special cases)

### ITERATION 2: Logging, Performance, Testing, Integration Workflows

#### Logging & Debugging
- [x] **Q2.1**: What logging should be added for D/ST ranking calculation?
  - **Recommendation**: Log D/ST ranking calculation similar to offensive/defensive ranks (debug level)
  - **Example**: "D/ST fantasy rankings from weeks {start}-{end}: HOU=#2 (avg 9.34 ppg)"
  - **✅ RESOLVED**: Match existing debug-level logging pattern
  - **Decision Date**: 2025-12-21
  - **Rationale**: Consistency with offensive/defensive logging, appropriate detail level, won't spam production logs

- [x] **Q2.2**: Should we log when D/ST uses dst_fantasy_rank vs when it would have used defensive_rank?
  - **Recommendation**: Debug log showing before/after for validation during rollout
  - **✅ RESOLVED**: No special before/after logging
  - **Decision Date**: 2025-12-21
  - **Rationale**: Matches existing pattern (no before/after logs in codebase), tests provide verification, simpler implementation

#### Performance
- [ ] **Q2.3**: Does calculating D/ST rankings add significant performance overhead?
  - **Analysis**: One additional ranking calculation (32 teams), similar complexity to offensive/defensive
  - **Status**: RESOLVED from codebase - negligible impact (same O(n log n) sort as existing)

- [x] **Q2.4**: Should D/ST rankings be calculated lazily or eagerly with other rankings?
  - **Codebase Evidence**: Current pattern calculates all rankings in `_calculate_rankings()` at init (lines 87-88)
  - **Recommendation**: Calculate eagerly with other rankings for consistency
  - **✅ RESOLVED**: Calculate eagerly in _calculate_rankings() (matches existing pattern)
  - **Decision Date**: 2025-12-21
  - **Rationale**: Existing code calculates offensive/defensive/position rankings eagerly at init, D/ST should follow same pattern

#### Testing
- [x] **Q2.5**: What test cases are needed for D/ST ranking calculation?
  - **Unit Tests** (TeamDataManager):
    1. test_rank_dst_fantasy_calculates_correctly - Verify ranking calculation with known data
    2. test_rank_dst_fantasy_handles_bye_weeks - Verify bye weeks (None/0) are skipped
    3. test_rank_dst_fantasy_handles_negative_scores - Verify negative scores included in average
    4. test_rank_dst_fantasy_missing_team_returns_none - Verify None for non-existent teams
    5. test_rank_dst_fantasy_uses_rolling_window - Verify only MIN_WEEKS data used
    6. test_rank_dst_fantasy_neutral_early_season - Verify rank 16 until MIN_WEEKS met
  - **Integration Tests** (PlayerManager):
    7. test_dst_uses_dst_fantasy_rank_not_defensive_rank - Verify D/ST uses new rank
    8. test_offensive_players_unchanged - Verify QB/RB/WR/TE/K still use offensive_rank
  - **Regression Tests**:
    9. Update existing test_team_quality_defense_uses_defensive_rank (line 737) to use dst_fantasy_rank
    10. test_houston_dst_gets_excellent_rating - Specific test for the Houston example
  - **✅ RESOLVED**: Full test suite (10 tests)
  - **Decision Date**: 2025-12-21
  - **Rationale**: Comprehensive coverage matching existing test patterns, protects against regressions, meets project quality standards (2200+ tests, 100% pass rate)

- [x] **Q2.6**: Should existing test `test_team_quality_defense_uses_defensive_rank` be updated or replaced?
  - **Location**: `tests/league_helper/util/test_PlayerManager_scoring.py:737-746`
  - **Current**: Tests that DST uses team_defensive_rank
  - **Recommendation**: Update to test that DST uses team_dst_fantasy_rank instead
  - **✅ RESOLVED**: Update existing test (keep structure, change assertions)
  - **Decision Date**: 2025-12-21
  - **Rationale**: Preserves test history, minimal churn, clear git diff showing behavior change

- [x] **Q2.7**: How to create test fixtures for D/ST ranking calculation?
  - **Recommendation**: Create mock players.csv data with known D/ST weekly scores, verify rankings match expected
  - **✅ RESOLVED**: Use pytest fixtures with @pytest.fixture decorator, mock FantasyPlayer objects
  - **Decision Date**: 2025-12-21
  - **Rationale**: Matches existing test fixture patterns in test_PlayerManager_scoring.py, uses pytest and unittest.mock infrastructure

#### Integration Workflows
- [ ] **Q2.8**: Does StarterHelperMode need any changes for D/ST team quality?
  - **Codebase Evidence**: StarterHelperMode uses PlayerManager.score_player() with team_quality flag
  - **Status**: RESOLVED from codebase - no changes needed (uses PlayerManager scoring)

- [ ] **Q2.9**: Does TradeSimulatorMode need any changes?
  - **Status**: RESOLVED from codebase - no changes needed (uses PlayerManager scoring)

- [ ] **Q2.10**: Does simulation system need any changes?
  - **Status**: RESOLVED from codebase - no changes needed (uses PlayerManager scoring)

### ITERATION 3: Relationships, Cross-Cutting Concerns, Similar Features

#### Comparison to Similar Features
- [x] **Q3.1**: How does D/ST ranking compare to offensive/defensive ranking patterns?
  - **Codebase Evidence**:
    - Offensive: `_rank_offensive()` sorts by points_scored descending (more points = rank 1)
    - Defensive: `_rank_defensive()` sorts by points_allowed ascending (fewer points = rank 1)
    - D/ST: Should sort by fantasy_points descending (more points = rank 1)
  - **Pattern**: D/ST should follow offensive pattern (higher is better)
  - **✅ RESOLVED**: Follow offensive ranking pattern (descending sort, more points = rank 1)
  - **Decision Date**: 2025-12-21
  - **Rationale**: D/ST fantasy points work like offensive points (higher is better), not like defensive points_allowed (lower is better)

- [ ] **Q3.2**: Should D/ST ranking use the same rolling window approach as other rankings?
  - **Codebase Evidence**: Both offensive and defensive use configurable MIN_WEEKS window
  - **Status**: RESOLVED - Yes, for consistency

- [x] **Q3.3**: Should TeamDataManager have a method pattern similar to get_team_offensive_rank()?
  - **Codebase Evidence**: Existing getters: `get_team_offensive_rank()`, `get_team_defensive_rank()`
  - **Recommendation**: Add `get_team_dst_fantasy_rank()` following same pattern
  - **✅ RESOLVED**: Add get_team_dst_fantasy_rank(team) following existing getter pattern
  - **Decision Date**: 2025-12-21
  - **Rationale**: Consistency with existing TeamDataManager API, same signature and return type as other getters

#### Cross-Cutting Concerns
- [ ] **Q3.4**: Does this affect multi-season simulation?
  - **Status**: RESOLVED from codebase - no special handling needed (each season loads own data)

- [ ] **Q3.5**: Does this affect different scoring modes (PPR vs standard)?
  - **Status**: RESOLVED from codebase - D/ST scoring doesn't vary by PPR mode

- [ ] **Q3.6**: What if user has multiple D/ST units on their roster?
  - **Status**: RESOLVED - each D/ST gets ranked independently, no special handling needed

#### Data Model Changes
- [x] **Q3.7**: If Option 1: Should FantasyPlayer have a new attribute `team_dst_fantasy_rank`?
  - **Codebase Evidence**: Current attributes are `team_offensive_rank` and `team_defensive_rank` (FantasyPlayer.py:130-131)
  - **Recommendation**: Yes, add `team_dst_fantasy_rank: Optional[int] = None`
  - **Alternative**: Reuse team_defensive_rank but change its meaning for D/ST (confusing)
  - **✅ RESOLVED**: Reuse existing team_defensive_rank attribute (NO new attribute needed)
  - **Decision Date**: 2025-12-21
  - **Rationale**: Simpler, no data model changes, team_defensive_rank populated differently based on position (D/ST gets fantasy rank, others get defensive rank)

- [x] **Q3.8**: Should team_defensive_rank still be set for D/ST players?
  - **Recommendation**: Yes, set both (defensive_rank for compatibility, dst_fantasy_rank for scoring)
  - **Reason**: Other code might read defensive_rank, don't break it
  - **✅ RESOLVED**: Yes, but with D/ST fantasy rank value (not defensive rank value)
  - **Decision Date**: 2025-12-21
  - **Rationale**: Reusing team_defensive_rank attribute means for D/ST it contains fantasy rank, for others it contains defensive rank

#### Documentation Updates
- [x] **Q3.9**: What documentation needs updating?
  - **Files**:
    - `docs/scoring/04_team_quality_multiplier.md` - Add D/ST-specific section
    - `ARCHITECTURE.md` - Document new TeamDataManager method
    - Inline docstrings for new methods
  - **✅ RESOLVED**: All documentation updates (scoring docs, ARCHITECTURE.md, inline docstrings)
  - **Decision Date**: 2025-12-21
  - **Rationale**: Comprehensive documentation for completeness, helps future agents understand D/ST-specific behavior

- [x] **Q3.10**: Should we document why D/ST uses different metric than team_defensive_rank?
  - **Recommendation**: Yes, in both code comments and docs/scoring/04_team_quality_multiplier.md
  - **Content**: Explain that defensive_rank measures opponent offense strength, dst_fantasy_rank measures D/ST unit performance
  - **✅ RESOLVED**: Yes, already covered by Q3.9 comprehensive documentation
  - **Decision Date**: 2025-12-21
  - **Rationale**: Q3.9 includes explaining rationale in both scoring docs and inline docstrings

---

## Codebase Verification Results

### Round 1: Initial Research

**Files Examined:**
- `league_helper/util/player_scoring.py` (lines 519-533)
- `league_helper/util/PlayerManager.py` (lines 199-202)
- `league_helper/util/TeamDataManager.py` (lines 1-260)
- `league_helper/constants.py` (DEFENSE_POSITIONS constant)
- `utils/FantasyPlayer.py` (dataclass definition)
- `data/players.csv` (D/ST data format)
- `data/team_data/HOU.csv` (team weekly data structure)
- `tests/league_helper/util/test_PlayerManager_scoring.py` (team quality tests)

**Key Findings:**
1. DEFENSE_POSITIONS = ["DEF", "DST", "D/ST"] (covers all variations)
2. D/ST entries in players.csv: position="DST", name="{Team} D/ST", team abbreviation (e.g., "HOU")
3. Weekly D/ST scores stored in week_1_points through week_17_points attributes
4. Current defensive rank uses points_allowed from team_data/*.csv (sum of fantasy points to QB+RB+WR+TE+K)
5. TeamDataManager uses rolling window (MIN_WEEKS) for rankings
6. FantasyPlayer has team_offensive_rank and team_defensive_rank attributes
7. Test at line 737-746 explicitly tests DST uses defensive_rank (will need updating)

### Round 2: Skeptical Re-verification

**Verified Claims:**
- ✅ D/ST weekly scores are in players.csv (confirmed with grep)
- ✅ DEFENSE_POSITIONS includes multiple variations (confirmed in constants.py:68)
- ✅ Negative D/ST scores are possible (confirmed: Broncos -5.0, Seahawks -5.0 in data)
- ✅ TeamDataManager skips bye weeks with 0 points (confirmed: lines 149-150)
- ✅ Rolling window uses configurable MIN_WEEKS (confirmed: line 117)

**Additional Findings:**
- PlayerManager sets both offensive_rank and defensive_rank for ALL players including D/ST (lines 201-202)
- Current pattern: PlayerManager loads data, TeamDataManager calculates rankings
- No existing DST-specific ranking infrastructure (will need to be added)

---

## Notes

**Three-Iteration Question Generation Complete**: 30 questions identified across 3 iterations
- **Iteration 1**: 8 questions (Edge Cases, Error Conditions, Configuration)
- **Iteration 2**: 10 questions (Logging, Performance, Testing, Integration)
- **Iteration 3**: 12 questions (Relationships, Similar Features, Cross-Cutting Concerns)

**Codebase Verification Rounds Complete**: 2 rounds performed
- **Round 1**: Initial research to identify patterns and existing code
- **Round 2**: Skeptical re-verification of Round 1 findings

**Items Resolved from Codebase**: 11 items (marked with "RESOLVED from codebase" or "Status: RESOLVED")

**Items Needing User Decision**: 19 items (primarily architectural choices and test strategies)
