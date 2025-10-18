# Trade Simulator Addition - TODO File

## Objective
Add three new combination options to Trade Suggestor:
1. Two-for-one (2:1 both directions)
2. Three-for-one (3:1 both directions)
3. Three-for-two (3:2 both directions)

Fill any lost roster spots using Add to Roster mode logic to get top recommendations.

---

## User Requirements Summary

From `updates/trade_simulator_addition.txt`:
- Add 2-for-1, 3-for-1, and 3-for-2 trade options
- Include both directions (give 2 get 1, AND give 1 get 2, etc.)
- Do usual trade assessment
- Fill any roster spots lost in trade by using Add to Roster mode logic

From answered questions:
- **R1**: Use constants at top of file for toggling (no UI changes)
- **R2**: No limits on combinations (exhaustive search)
- **R3**: Include waiver recommendations in trade output file, print ScoredPlayer objects
- **R4**: Show top N waiver adds needed to fill empty spots

---

## Implementation Plan (DRAFT - ITERATION 1)

### Phase 1: Add Configuration Constants
**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` (top of file)

**Tasks**:
1.1. Add constants for toggling unequal trade types:
```python
# Trade combination toggles (add near line 10)
ENABLE_TWO_FOR_ONE = True
ENABLE_ONE_FOR_TWO = True
ENABLE_THREE_FOR_ONE = True
ENABLE_ONE_FOR_THREE = True
ENABLE_THREE_FOR_TWO = True
ENABLE_TWO_FOR_THREE = True
```

### Phase 2: Add Waiver Recommendation Helper Method
**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`

**Tasks**:
2.1. Create new method `_get_waiver_recommendations(self, num_spots: int) -> List[ScoredPlayer]`
   - Similar to AddToRosterModeManager.get_recommendations()
   - Get available players with `drafted=0`, `can_draft=True`
   - Score each player using `player_manager.score_player()`
   - Return top `num_spots` players sorted by score descending
   - Add to file around line 840 (after start_manual_trade method)

### Phase 3: Modify get_trade_combinations Method
**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` (line 979)

**Current signature**:
```python
def get_trade_combinations(self, my_team, their_team, is_waivers=False,
                          one_for_one=True, two_for_two=True, three_for_three=False,
                          ignore_max_positions=False) -> List[TradeSnapshot]
```

**Tasks**:
3.1. Add new parameters to method signature:
```python
def get_trade_combinations(self, my_team, their_team, is_waivers=False,
                          one_for_one=True, two_for_two=True, three_for_three=False,
                          two_for_one=False, one_for_two=False,
                          three_for_one=False, one_for_three=False,
                          three_for_two=False, two_for_three=False,
                          ignore_max_positions=False) -> List[TradeSnapshot]
```

3.2. Add 2-for-1 trade generation logic (after 3-for-3 block, around line 1221)
3.3. Add 1-for-2 trade generation logic
3.4. Add 3-for-1 trade generation logic
3.5. Add 1-for-3 trade generation logic
3.6. Add 3-for-2 trade generation logic
3.7. Add 2-for-3 trade generation logic

**Pattern to follow**: Copy existing 2-for-2 or 3-for-3 logic, adjust combination sizes

### Phase 4: Modify TradeSnapshot to Include Waiver Recommendations
**File**: `league_helper/trade_simulator_mode/TradeSnapshot.py`

**Tasks**:
4.1. Read TradeSnapshot.py to understand current structure
4.2. Add optional `waiver_recommendations: List[ScoredPlayer]` field
4.3. Update `__init__` method to accept waiver_recommendations parameter (optional, default None)

### Phase 5: Update start_trade_suggestor to Use New Trade Types
**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` (line 209)

**Tasks**:
5.1. Update get_trade_combinations call (around line 276) to include new parameters:
```python
trade_combos = self.get_trade_combinations(
    my_team=self.my_team,
    their_team=opponent_team,
    is_waivers=False,
    one_for_one=True,
    two_for_two=True,
    three_for_three=False,
    two_for_one=ENABLE_TWO_FOR_ONE,
    one_for_two=ENABLE_ONE_FOR_TWO,
    three_for_one=ENABLE_THREE_FOR_ONE,
    one_for_three=ENABLE_ONE_FOR_THREE,
    three_for_two=ENABLE_THREE_FOR_TWO,
    two_for_three=ENABLE_TWO_FOR_THREE,
    ignore_max_positions=True
)
```

5.2. Update expected combinations calculation (line 266-271) to include new types

### Phase 6: Calculate and Add Waiver Recommendations
**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`

**Tasks**:
6.1. In get_trade_combinations(), for each valid unequal trade:
   - Calculate net roster spots: `net_spots = len(my_new_roster) - len(my_roster)`
   - If net_spots < 0 (losing roster spots):
     - Call `_get_waiver_recommendations(abs(net_spots))`
     - Attach to TradeSnapshot

### Phase 7: Update Trade Output to Display Waiver Recommendations
**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`

**Tasks**:
7.1. Update save_trades_to_file() method (line 1235):
   - After displaying "I receive:" section
   - Add "Recommended waiver adds:" section if trade has waiver_recommendations
   - Print each ScoredPlayer in waiver_recommendations list

7.2. Update console display in start_trade_suggestor() (line 304):
   - Add waiver recommendations display after trade details

### Phase 8: Update Tests
**File**: `tests/league_helper/trade_simulator_mode/test_trade_simulator.py`

**Tasks**:
8.1. Add test for 2-for-1 trade generation
8.2. Add test for 1-for-2 trade generation
8.3. Add test for 3-for-1 trade generation
8.4. Add test for 1-for-3 trade generation
8.5. Add test for 3-for-2 trade generation
8.6. Add test for 2-for-3 trade generation
8.7. Add test for waiver recommendations attachment
8.8. Run all tests to ensure 100% pass rate

### Phase 9: Documentation
**File**: Various

**Tasks**:
9.1. Update CLAUDE.md if workflow changed
9.2. Update README.md if user-facing behavior changed
9.3. Add docstrings to new methods

### Phase 10: Validation & Commit
**Tasks**:
10.1. Run all unit tests: `python tests/run_all_tests.py`
10.2. Verify 100% test pass rate
10.3. Manual testing: Run trade suggestor with new options enabled
10.4. Commit changes with appropriate message

---

## Progress Tracking

- [ ] Phase 1: Configuration Constants
- [ ] Phase 2: Waiver Helper Method
- [ ] Phase 3: Modify get_trade_combinations
- [ ] Phase 4: Update TradeSnapshot
- [ ] Phase 5: Update start_trade_suggestor
- [ ] Phase 6: Calculate Waiver Recommendations
- [ ] Phase 7: Update Output Display
- [ ] Phase 8: Update Tests
- [ ] Phase 9: Documentation
- [ ] Phase 10: Validation & Commit

---

## Notes for Future Sessions

This TODO file should be updated after each phase completion. If a new agent needs to continue this work, they should:
1. Review completed phases above
2. Continue from the next unchecked phase
3. Update this file with progress
4. Run tests after each phase

---

# VERIFICATION ITERATION 1 - COMPLETE

## Cross-Reference Requirements Checklist
- [x] Add 2:1, 1:2, 3:1, 1:3, 3:2, 2:3 trade combinations
- [x] Constants at top of file for toggling
- [x] Exhaustive search (no limits)
- [x] Waiver recommendations in output file
- [x] Print ScoredPlayer objects for waiver adds
- [x] Top N waiver adds to fill spots
- [x] Keep existing 1:1 and 2:2 trades working

## Questions to Self - Answered

**Q**: What specific files need modification?
**A**:
- TradeSimulatorModeManager.py (main logic)
- TradeSnapshot.py (add waiver_recommendations field)
- test_trade_simulator.py (add tests)

**Q**: What existing patterns can be leveraged?
**A**:
- 2-for-2 trade block (lines 1082-1150) is perfect template
- Use combinations() from itertools
- Follow same validation/scoring pattern

**Q**: What edge cases need handling?
**A**:
- Net roster change calculation (must account for locked players)
- Trades that GAIN roster spots (1:2, 1:3, 2:3) don't need waiver adds
- Empty waiver wire case (no players available)
- All available players locked or already drafted

**Q**: What error handling is needed?
**A**:
- Handle case where _get_waiver_recommendations returns fewer than requested
- Validate waiver players aren't locked
- Log rejection stats for new trade types

**Q**: What logging should be added?
**A**:
- Log when generating each new trade type
- Log number of combinations for each type
- Log waiver recommendation calls
- Update expected combination calculations

## Codebase Research Findings

### TradeSnapshot Structure (TradeSnapshot.py:10-29)
```python
class TradeSnapshot:
    def __init__(self, my_new_team, my_new_players,
                 their_new_team, their_new_players,
                 my_original_players=None):
```
**NEED TO ADD**: `waiver_recommendations` parameter (optional, default None)

### Trade Generation Pattern (TradeSimulatorModeManager.py:1082-1150)
Key steps for each trade type:
1. Get combinations using `combinations(roster, n)`
2. Create new rosters: `[p for p in roster if p not in traded_players] + list(received_players)`
3. Validate rosters (include locked players)
4. Create new TradeSimTeam objects
5. Check improvements vs thresholds
6. Create TradeSnapshot with original scored players
7. Append to trade_combos list

### Add to Roster Pattern (AddToRosterModeManager.py:217-241)
```python
available_players = player_manager.get_player_list(drafted_vals=[0], can_draft=True)
for p in available_players:
    scored_player = player_manager.score_player(p, draft_round=current_round,
                                                 adp=True, player_rating=True,
                                                 team_quality=True, performance=True,
                                                 matchup=True)
    scored_players.append(scored_player)
ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)
return ranked_players[:Constants.RECOMMENDATION_COUNT]
```

## Updated Implementation Details

### Phase 1: Add Configuration Constants (UPDATED)
**Location**: Line 10 in TradeSimulatorModeManager.py (after imports, before class)

Add after line 23 (after LoggingManager import):
```python
# =============================================================================
# UNEQUAL TRADE CONFIGURATION
# =============================================================================
# Toggle unequal trade types (user can modify these)
ENABLE_TWO_FOR_ONE = True    # Give 2 players, get 1 player
ENABLE_ONE_FOR_TWO = True    # Give 1 player, get 2 players
ENABLE_THREE_FOR_ONE = True  # Give 3 players, get 1 player
ENABLE_ONE_FOR_THREE = True  # Give 1 player, get 3 players
ENABLE_THREE_FOR_TWO = True  # Give 3 players, get 2 players
ENABLE_TWO_FOR_THREE = True  # Give 2 players, get 3 players
```

### Phase 2: Add Waiver Recommendation Helper Method (UPDATED)
**Location**: After `start_manual_trade()` method, around line 840

```python
def _get_waiver_recommendations(self, num_spots: int) -> List[ScoredPlayer]:
    """
    Get top N waiver wire recommendations to fill roster spots.

    Uses same logic as Add to Roster mode to score and rank available players.

    Args:
        num_spots (int): Number of waiver players needed

    Returns:
        List[ScoredPlayer]: Top num_spots players sorted by score descending.
                           May return fewer if insufficient players available.

    Example:
        >>> waiver_adds = self._get_waiver_recommendations(2)
        >>> print([p.player.name for p in waiver_adds])
        ['Available Player 1', 'Available Player 2']
    """
    # Get available players (drafted=0, can_draft=True, unlocked)
    available_players = self.player_manager.get_player_list(
        drafted_vals=[0],
        can_draft=True,
        unlocked_only=True
    )

    if not available_players:
        self.logger.warning("No waiver wire players available for recommendations")
        return []

    # Score each player
    scored_players: List[ScoredPlayer] = []
    for p in available_players:
        # Use current week for matchup scoring
        scored_player = self.player_manager.score_player(
            p,
            draft_round=None,  # Not draft context
            adp=True,
            player_rating=True,
            team_quality=True,
            performance=True,
            matchup=True
        )
        scored_players.append(scored_player)

    # Sort by score descending
    ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

    # Return top num_spots (or fewer if not enough available)
    result_count = min(num_spots, len(ranked_players))
    self.logger.info(f"Generated {result_count} waiver recommendations (requested: {num_spots})")

    return ranked_players[:result_count]
```

### Phase 3: Modify get_trade_combinations (UPDATED)
**Location**: Line 979, update method signature

**Step 3.1**: Update signature
```python
def get_trade_combinations(self, my_team: TradeSimTeam, their_team: TradeSimTeam,
                          is_waivers: bool = False,
                          one_for_one: bool = True,
                          two_for_two: bool = True,
                          three_for_three: bool = False,
                          two_for_one: bool = False,
                          one_for_two: bool = False,
                          three_for_one: bool = False,
                          one_for_three: bool = False,
                          three_for_two: bool = False,
                          two_for_three: bool = False,
                          ignore_max_positions: bool = False) -> List[TradeSnapshot]:
```

**Steps 3.2-3.7**: Add trade generation blocks AFTER 3-for-3 block (after line 1220)

Each block should follow this pattern (example for 2-for-1):
```python
# Generate 2-for-1 trades (give 2, get 1)
if two_for_one:
    my_combos = list(combinations(my_roster, 2))
    their_combos = list(combinations(their_roster, 1))

    for my_players in my_combos:
        for their_players in their_combos:
            # Create new rosters
            my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
            their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

            # Validation (same as 2-for-2)
            # ... [copy validation from 2-for-2 block]

            # Create teams, check improvements
            # ... [copy from 2-for-2 block]

            # Calculate waiver recommendations for net roster loss
            waiver_recs = None
            net_roster_change = len(my_new_roster) - len(my_roster)
            if net_roster_change < 0 and not is_waivers:
                waiver_recs = self._get_waiver_recommendations(abs(net_roster_change))

            # Create TradeSnapshot with waiver_recommendations
            snapshot = TradeSnapshot(
                my_new_team=my_new_team,
                my_new_players=my_new_team.get_scored_players(list(their_players)),
                their_new_team=their_new_team,
                their_new_players=their_new_team.get_scored_players(list(my_players)),
                my_original_players=my_original_scored,
                waiver_recommendations=waiver_recs
            )
            trade_combos.append(snapshot)
```

### Phase 4: Update TradeSnapshot (UPDATED)
**Location**: TradeSnapshot.py:12-29

**Step 4.1**: Add import for List[ScoredPlayer] type (already imported at line 8)

**Step 4.2**: Update __init__ method:
```python
def __init__(self, my_new_team: TradeSimTeam, my_new_players: List[ScoredPlayer],
             their_new_team: TradeSimTeam, their_new_players: List[ScoredPlayer],
             my_original_players: List[ScoredPlayer] = None,
             waiver_recommendations: List[ScoredPlayer] = None):
    """
    Trade snapshot storing both new team state and original player scores.

    Args:
        my_new_team: My team after the trade
        my_new_players: Players I receive (scored in new team context)
        their_new_team: Their team after the trade
        their_new_players: Players they receive (scored in new team context)
        my_original_players: Players I give up (scored in original team context)
        waiver_recommendations: Recommended waiver adds to fill roster spots (optional)
    """
    self.my_new_team = my_new_team
    self.my_new_players = my_new_players
    self.their_new_team = their_new_team
    self.their_new_players = their_new_players
    self.my_original_players = my_original_players if my_original_players is not None else []
    self.waiver_recommendations = waiver_recommendations if waiver_recommendations is not None else []
```

### Phase 5: Update start_trade_suggestor (UPDATED)
**Location**: Line 276 in TradeSimulatorModeManager.py

**Step 5.1**: Update get_trade_combinations call:
```python
trade_combos = self.get_trade_combinations(
    my_team=self.my_team,
    their_team=opponent_team,
    is_waivers=False,
    one_for_one=True,
    two_for_two=True,
    three_for_three=False,
    two_for_one=ENABLE_TWO_FOR_ONE,
    one_for_two=ENABLE_ONE_FOR_TWO,
    three_for_one=ENABLE_THREE_FOR_ONE,
    one_for_three=ENABLE_ONE_FOR_THREE,
    three_for_two=ENABLE_THREE_FOR_TWO,
    two_for_three=ENABLE_TWO_FOR_THREE,
    ignore_max_positions=True
)
```

**Step 5.2**: Update expected combinations calculation (lines 263-271):
```python
my_unlocked = len([p for p in self.my_team.team if p.locked != 1])
their_unlocked = len([p for p in opponent_team.team if p.locked != 1])

one_for_one_combos = my_unlocked * their_unlocked
two_for_two_combos = (my_unlocked * (my_unlocked - 1) // 2) * (their_unlocked * (their_unlocked - 1) // 2)
two_for_one_combos = (my_unlocked * (my_unlocked - 1) // 2) * their_unlocked if ENABLE_TWO_FOR_ONE else 0
one_for_two_combos = my_unlocked * (their_unlocked * (their_unlocked - 1) // 2) if ENABLE_ONE_FOR_TWO else 0
three_for_one_combos = (my_unlocked * (my_unlocked - 1) * (my_unlocked - 2) // 6) * their_unlocked if ENABLE_THREE_FOR_ONE else 0
one_for_three_combos = my_unlocked * (their_unlocked * (their_unlocked - 1) * (their_unlocked - 2) // 6) if ENABLE_ONE_FOR_THREE else 0
three_for_two_combos = (my_unlocked * (my_unlocked - 1) * (my_unlocked - 2) // 6) * (their_unlocked * (their_unlocked - 1) // 2) if ENABLE_THREE_FOR_TWO else 0
two_for_three_combos = (my_unlocked * (my_unlocked - 1) // 2) * (their_unlocked * (their_unlocked - 1) * (their_unlocked - 2) // 6) if ENABLE_TWO_FOR_THREE else 0

total_expected = one_for_one_combos + two_for_two_combos + two_for_one_combos + one_for_two_combos + three_for_one_combos + one_for_three_combos + three_for_two_combos + two_for_three_combos
```

### Phase 7: Update Trade Output (UPDATED)
**Location**: Line 1262 in save_trades_to_file() and line 329 in start_trade_suggestor()

**Step 7.1**: Update save_trades_to_file():
```python
# After line 1273 (after "I receive:" section)
# Add waiver recommendations section
if trade.waiver_recommendations:
    file.write(f"  Recommended waiver adds to fill roster:\n")
    for waiver_player in trade.waiver_recommendations:
        file.write(f"    - {waiver_player}\n")
```

**Step 7.2**: Update console display in start_trade_suggestor():
```python
# After line 336 (after displaying "I receive:")
if trade.waiver_recommendations:
    print(f"  Recommended waiver adds to fill roster:")
    for waiver_player in trade.waiver_recommendations:
        print(f"    - {waiver_player}")
```

---

# VERIFICATION ITERATION 1 COMPLETE

## Changes Made in Iteration 1:
- Added specific line numbers for all changes
- Added complete code examples following existing patterns
- Identified exact locations for modifications
- Added edge case handling (empty waiver wire, fewer players than requested)
- Added logging requirements
- Added type hints to method signatures
- Clarified net roster calculation must account for locked players

## Risks Identified:
- Performance: 3:2 trades generate ~48K combinations per opponent (acceptable per user)
- Edge case: Waiver wire might be empty (handled with warning log)
- Edge case: Trade that gains roster spots (1:2, 1:3, 2:3) should NOT get waiver recs (handled with net_roster_change < 0 check)

---

# VERIFICATION ITERATION 2 - COMPLETE

## Additional Clarifying Questions - Answered

**Q**: What data structures will be passed between functions?
**A**:
- `List[ScoredPlayer]` for waiver recommendations
- `ScoredPlayer` has `__str__` method (line 25-41) that formats nicely
- Includes player position, team, name, score, bye week, and reasons
- Format: `[POS] [TEAM] Name - XX.XX pts (Bye=N)`

**Q**: What error handling strategies?
**A**:
- Existing code uses minimal try/except (only 1 instance found)
- Use warning logs for non-critical issues (empty waiver wire)
- Return empty list `[]` when no waiver players available
- No exceptions needed - graceful degradation

**Q**: Are there performance considerations?
**A**:
- User confirmed: no limits, exhaustive search acceptable
- 3:2 trades: ~48K combinations per opponent
- Waiver recommendation scoring happens once per valid trade
- Performance should be acceptable based on existing 2:2 and 3:3 behavior

**Q**: What logging for debugging?
**A**:
- `self.logger.info()` for waiver recommendation generation (count)
- `self.logger.warning()` if waiver wire is empty
- Update expected combinations log (already exists)
- Use existing logging pattern (no need for debug level)

**Q**: Should constants go in configuration files?
**A**:
- NO - user wants them at top of TradeSimulatorModeManager.py
- Easy for user to modify directly
- Consistent with existing RECOMMENDATION_COUNT pattern in constants.py
- Keep simple toggle switches in module file

**Q**: What documentation needs updating?
**A**:
- TradeSimulatorModeManager: Add docstring to _get_waiver_recommendations()
- TradeSnapshot: Update __init__ docstring with waiver_recommendations
- get_trade_combinations: Update docstring with new parameters
- README.md: May need update if user-facing (check after implementation)
- CLAUDE.md: May need update if workflow changed (check after implementation)

**Q**: Backward compatibility concerns?
**A**:
- ✅ TradeSnapshot.waiver_recommendations is optional (default None)
- ✅ Existing 4 TradeSnapshot() calls won't break (lines 817, 1067, 1137, 1207)
- ✅ get_trade_combinations new parameters have defaults (False)
- ✅ No breaking changes to existing functionality
- ✅ Existing 1:1 and 2:2 trades continue working unchanged

## Additional Code Pattern Research

### Existing TradeSnapshot Calls (Need to Remain Compatible)
1. Line 817 - Manual trade visualizer
2. Line 1067 - 1-for-1 trades
3. Line 1137 - 2-for-2 trades
4. Line 1207 - 3-for-3 trades

All use 5 parameters (my_original_players=... format), new 6th parameter is optional.

### ScoredPlayer String Format (ScoredPlayer.py:25-41)
```python
def __str__(self) -> str:
    header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.score:.2f} pts (Bye={self.player.bye_week})"
    lines = [header]
    for reason in self.reason:
        lines.append(f"            - {reason}")
    return "\n".join(lines)
```
This will print correctly when writing to file with `file.write(f"    - {waiver_player}\n")`

### PlayerManager.get_player_list Signature (PlayerManager.py:355)
```python
def get_player_list(self, drafted_vals: List[int] = [],
                   can_draft: bool = False,
                   min_scores: Dict[str,float] = {},
                   unlocked_only=False) -> List[FantasyPlayer]:
```
Parameters needed:
- `drafted_vals=[0]` - only waiver wire players
- `can_draft=True` - only draftable players
- `unlocked_only=True` - exclude locked players

## Updated Implementation Details - ITERATION 2

### Phase 2: Waiver Helper Method (REFINED)
**Additional considerations**:
- Must handle empty list gracefully
- Log count of recommendations vs requested
- No draft_round parameter (not in draft context)
- Use `unlocked_only=True` to avoid locked waiver players

**Error cases**:
```python
if not available_players:
    self.logger.warning("No waiver wire players available for recommendations")
    return []

if num_spots <= 0:
    self.logger.debug(f"No waiver recommendations needed (num_spots={num_spots})")
    return []
```

### Phase 3: Trade Generation Blocks (REFINED)
**Important**: Each of 6 new trade types needs identical structure:
1. Check if enabled with `if <trade_type>:`
2. Generate combinations with `combinations(roster, n)`
3. Loop through combination pairs
4. Create new rosters
5. Validate (copy exact validation from 2-for-2)
6. Create TradeSimTeam objects
7. Check improvements
8. **NEW**: Calculate waiver recommendations
9. Create TradeSnapshot with waiver_recommendations
10. Update rejection_stats

**Waiver calculation pattern** (add to each unequal trade block):
```python
# Calculate waiver recommendations for net roster loss
waiver_recs = None
if not is_waivers:  # Skip for waiver optimizer mode
    net_roster_change = len(my_new_roster) - len(my_roster)
    if net_roster_change < 0:
        waiver_recs = self._get_waiver_recommendations(abs(net_roster_change))
```

### Phase 4: TradeSnapshot Update (REFINED)
**Backward compatibility ensured**:
- New parameter is last parameter
- Has default value `None`
- Existing calls use keyword arguments, so they won't break
- New field initialized as empty list if None

### Phase 8: Testing (REFINED)
**Test scenarios needed**:
1. Test 2-for-1 generation (my perspective)
2. Test 1-for-2 generation (opponent perspective)
3. Test 3-for-1 generation (my perspective)
4. Test 1-for-3 generation (opponent perspective)
5. Test 3-for-2 generation (my perspective)
6. Test 2-for-3 generation (opponent perspective)
7. Test waiver recommendation attachment (verify List[ScoredPlayer])
8. Test waiver recs only on roster-losing trades (not 1:2, 1:3, 2:3)
9. Test empty waiver wire case (returns empty list)
10. Test backward compatibility (existing tests still pass)

**Mock requirements**:
- Mock player_manager.get_player_list to return test waiver players
- Mock player_manager.score_player to return mock ScoredPlayer objects
- Verify waiver_recommendations field in TradeSnapshot

### Phase 9: Documentation Updates (REFINED)
**Files to check**:
- README.md: Check if Trade Suggestor is documented (update if mentioned)
- CLAUDE.md: Check if Trade Simulator workflow is documented (update if mentioned)
- No changes needed to PROJECT_DOCUMENTATION.md (implementation detail)

---

# VERIFICATION ITERATION 2 COMPLETE

## Changes Made in Iteration 2:
- Clarified data structures (List[ScoredPlayer], ScoredPlayer.__str__)
- Defined error handling strategy (warning logs, graceful degradation)
- Confirmed performance approach (exhaustive search, no sampling)
- Specified logging requirements (info/warning, no debug needed)
- Confirmed constants placement (module file, not config)
- Identified documentation files to update
- Verified backward compatibility (optional parameter, existing calls safe)
- Refined waiver calculation logic (check is_waivers, check net_roster_change)
- Added test scenarios (10 specific tests needed)
- Clarified mock requirements for testing

## Additional Risks Identified:
- Edge case: num_spots <= 0 (handled with early return)
- Edge case: get_player_list returns locked players (use unlocked_only=True)
- Testing: Need to mock player_manager methods
- Backward compat: Must verify existing tests still pass (Phase 8)

---

# VERIFICATION ITERATION 3 - COMPLETE

## Final Technical Questions - Answered

**Q**: Are there any integration points with other modules not addressed?
**A**:
- TradeSnapshot imported by: TradeSimulatorModeManager, test_trade_simulator, test_manual_trade_visualizer
- TradeSimulatorModeManager imported by: LeagueHelperManager (line 27, 91, 131, 163, 170)
- LeagueHelperManager only calls `run_interactive_mode()` - NO CHANGES NEEDED
- Test files need updates (already in Phase 8)
- No other integration points found

**Q**: What mock objects will be needed for testing?
**A**:
```python
# Mock player_manager for waiver tests
mock_player_manager.get_player_list = Mock(return_value=[waiver_player1, waiver_player2])
mock_player_manager.score_player = Mock(return_value=mock_scored_player)

# Mock ScoredPlayer for verification
mock_scored_player = Mock(spec=ScoredPlayer)
mock_scored_player.score = 100.0
mock_scored_player.player = mock_fantasy_player
```

**Q**: Are there any circular dependency risks?
**A**:
- NO - TradeSimulatorModeManager already imports ScoredPlayer (via TradeSnapshot)
- NO - PlayerManager is passed in __init__, not imported
- NO - All imports follow existing patterns
- Import order: utils -> util -> trade_simulator_mode (safe)

**Q**: What happens if operations fail midway through?
**A**:
- Waiver recommendation failure: Returns empty list, trade still created
- get_player_list returns empty: Warning logged, returns []
- score_player fails: Would raise exception from PlayerManager (existing behavior)
- Validation failure: Trade rejected, not added to trade_combos (existing behavior)
- No cleanup needed - all operations are atomic per trade

**Q**: Are all file paths absolute or properly constructed?
**A**:
- ✅ All file paths use Path objects (existing pattern)
- ✅ Output files use relative path: `./league_helper/trade_simulator_mode/trade_outputs/`
- ✅ No new file operations added (only modifying existing output)

**Q**: What cleanup operations are needed if errors occur?
**A**:
- NONE - Each trade is evaluated independently
- Failed trades are simply not added to trade_combos list
- No state changes that need rollback
- Logging captures all failures for debugging

## Integration Points Research

### Files Importing TradeSnapshot:
1. `TradeSimulatorModeManager.py` - Will be updated (Phase 4)
2. `test_trade_simulator.py` - Will be updated (Phase 8)
3. `test_manual_trade_visualizer.py` - NO CHANGES NEEDED (optional param)

### Files Importing TradeSimulatorModeManager:
1. `LeagueHelperManager.py` - NO CHANGES NEEDED (only calls run_interactive_mode)
2. `test_trade_simulator.py` - Will be updated (Phase 8)
3. `test_manual_trade_visualizer.py` - NO CHANGES NEEDED (tests manual trade only)

### Potential Circular Imports:
- ✅ NONE FOUND - Import hierarchy is safe
- TradeSimulatorModeManager → TradeSnapshot → ScoredPlayer
- TradeSimulatorModeManager ← LeagueHelperManager (dependency injection)
- No circular references

## Final TODO Update

### Phase 8: Testing (FINALIZED)

**Test file**: `tests/league_helper/trade_simulator_mode/test_trade_simulator.py`

**New test methods to add**:

```python
def test_two_for_one_trade_generation(mock_config, mock_player_manager):
    """Test 2-for-1 trade generation (give 2, get 1)"""
    # Setup: Create manager, my_team, their_team
    # Execute: get_trade_combinations with two_for_one=True
    # Assert: Trades generated, waiver_recommendations attached
    # Assert: len(my_original_players) == 2, len(my_new_players) == 1
    # Assert: waiver_recommendations has 1 player (net loss of 1 spot)

def test_one_for_two_trade_generation(mock_config, mock_player_manager):
    """Test 1-for-2 trade generation (give 1, get 2)"""
    # Assert: waiver_recommendations is empty (net gain of 1 spot)

def test_three_for_one_trade_generation(mock_config, mock_player_manager):
    """Test 3-for-1 trade generation (give 3, get 1)"""
    # Assert: waiver_recommendations has 2 players (net loss of 2 spots)

def test_one_for_three_trade_generation(mock_config, mock_player_manager):
    """Test 1-for-3 trade generation (give 1, get 3)"""
    # Assert: waiver_recommendations is empty (net gain of 2 spots)

def test_three_for_two_trade_generation(mock_config, mock_player_manager):
    """Test 3-for-2 trade generation (give 3, get 2)"""
    # Assert: waiver_recommendations has 1 player (net loss of 1 spot)

def test_two_for_three_trade_generation(mock_config, mock_player_manager):
    """Test 2-for-3 trade generation (give 2, get 3)"""
    # Assert: waiver_recommendations is empty (net gain of 1 spot)

def test_waiver_recommendations_empty_waiver_wire(mock_config, mock_player_manager):
    """Test waiver recommendations when waiver wire is empty"""
    # Mock: get_player_list returns []
    # Assert: waiver_recommendations is []
    # Assert: Trade still created successfully

def test_waiver_recommendations_content(mock_config, mock_player_manager):
    """Test waiver recommendations contain correct ScoredPlayer objects"""
    # Mock: get_player_list returns 3 players
    # Mock: score_player returns ScoredPlayer with known scores
    # Execute: 2-for-1 trade
    # Assert: waiver_recommendations[0] is ScoredPlayer
    # Assert: waiver_recommendations[0].score is highest score

def test_backward_compatibility_existing_trade_snapshots(mock_config, mock_player_manager):
    """Test that existing TradeSnapshot calls still work"""
    # Create TradeSnapshot with 5 parameters (no waiver_recommendations)
    # Assert: snapshot.waiver_recommendations == []
    # Assert: All fields populated correctly

def test_constants_toggle_unequal_trades(mock_config, mock_player_manager):
    """Test that constants correctly enable/disable unequal trades"""
    # Set ENABLE_TWO_FOR_ONE = False
    # Execute: get_trade_combinations with two_for_one=True
    # Assert: No 2-for-1 trades generated
```

**Existing tests to verify**:
- Run all existing tests to ensure no regression
- Verify 1-for-1 and 2-for-2 trades still work
- Verify manual trade visualizer still works

### Phase 10: Validation & Commit (FINALIZED)

**Pre-commit checklist**:
```bash
# 1. Run all unit tests
python tests/run_all_tests.py

# Expected output: 100% pass rate
# If ANY test fails: STOP and fix before commit

# 2. Manual verification
python run_league_helper.py
# Select: Trade Simulator > Trade Suggestor
# Verify: New trade types appear in output
# Verify: Waiver recommendations display correctly
# Verify: Output file contains waiver recommendations

# 3. Performance check
# Monitor time for trade generation with all types enabled
# Should complete in reasonable time (<60s per opponent)

# 4. Git operations
git status
git diff
git add league_helper/trade_simulator_mode/TradeSimulatorModeManager.py
git add league_helper/trade_simulator_mode/TradeSnapshot.py
git add tests/league_helper/trade_simulator_mode/test_trade_simulator.py
# Add any documentation changes
git commit -m "Add unequal trade options to Trade Suggestor

- Add 2:1, 1:2, 3:1, 1:3, 3:2, 2:3 trade combinations
- Add waiver recommendations for roster-losing trades
- Add configuration constants for toggling trade types
- Update TradeSnapshot to include waiver_recommendations
- Add comprehensive tests for new functionality"
```

---

# VERIFICATION ITERATION 3 COMPLETE

## Changes Made in Iteration 3:
- Verified integration points (no circular dependencies)
- Defined mock object requirements for testing
- Confirmed no circular dependency risks
- Clarified error handling (atomic operations, no cleanup needed)
- Verified file path handling (existing patterns)
- Finalized test specifications (10 test methods with details)
- Created pre-commit validation checklist
- Defined commit message

## Final Risks Assessment:
- ✅ NO circular dependencies found
- ✅ NO integration issues identified
- ✅ Backward compatibility verified (optional parameters)
- ✅ Error handling graceful (empty list returns, warning logs)
- ⚠️ Performance: 3:2 trades ~48K combos per opponent (acceptable per user)
- ✅ Testing: 10 comprehensive tests planned
- ✅ Documentation: Paths identified for updates

---

# VERIFICATION SUMMARY

## Verification Complete: 3 Iterations Performed

### Iteration 1 - Initial Verification:
- ✅ Re-read all source documents
- ✅ Cross-referenced all requirements (7 requirements)
- ✅ Researched codebase patterns (TradeSnapshot, get_trade_combinations, AddToRosterMode)
- ✅ Added specific file paths and line numbers
- ✅ Identified edge cases (empty waiver, net roster calculations)
- ✅ Added complete code examples
- **Result**: 11 requirements added after initial draft

### Iteration 2 - Deep Dive Verification:
- ✅ Clarified data structures (List[ScoredPlayer], __str__ format)
- ✅ Defined error handling strategy (warning logs, graceful degradation)
- ✅ Researched additional code patterns (ScoredPlayer, get_player_list)
- ✅ Confirmed performance approach (exhaustive search)
- ✅ Verified backward compatibility (optional parameters)
- ✅ Refined waiver calculation logic
- **Result**: 8 additional requirements and edge cases identified

### Iteration 3 - Final Verification:
- ✅ Re-read all documents one more time
- ✅ Researched integration points (5 files checked)
- ✅ Confirmed no circular dependencies
- ✅ Finalized test specifications (10 tests with mock requirements)
- ✅ Created pre-commit validation checklist
- ✅ Verified all file paths and imports
- **Result**: Complete integration verification, no issues found

## Key Codebase Patterns/Utilities Identified for Reuse:
1. **Trade Generation Pattern** (lines 1082-1150): Copy structure for all 6 new trade types
2. **combinations()** from itertools: For generating player combinations
3. **TradeSnapshot** structure: Add optional waiver_recommendations parameter
4. **_validate_roster()** method: Reuse for validation
5. **player_manager.get_player_list()**: Get waiver players
6. **player_manager.score_player()**: Score waiver players
7. **ScoredPlayer.__str__()**: Automatic formatting for output
8. **Logging patterns**: Use self.logger.info/warning

## Critical Dependencies or Ordering Requirements:
1. Phase 4 (TradeSnapshot update) MUST complete before Phase 3 (trade generation)
2. Phase 2 (waiver helper) MUST complete before Phase 3 (trade generation)
3. Phase 1 (constants) MUST complete before Phase 5 (start_trade_suggestor)
4. Phases 1-7 MUST complete before Phase 8 (testing)
5. ALL tests MUST pass before Phase 10 (commit)

## Risk Areas Identified During Research:
1. **Performance**: 3:2 trades generate ~48K combinations per opponent
   - Mitigation: User accepted, exhaustive search confirmed
   - Monitor: Check generation time in manual testing

2. **Empty Waiver Wire**: No players available for recommendations
   - Mitigation: Return empty list, log warning, trade still valid

3. **Backward Compatibility**: Existing TradeSnapshot calls
   - Mitigation: Optional parameter with default None, existing tests verify

4. **Testing Complexity**: 10 new tests needed with mocking
   - Mitigation: Clear test specifications provided, mock patterns defined

---

# IMPLEMENTATION PROGRESS - SESSION 2

## Phase 1 (Waiver System) - ✅ COMPLETED

### Completed Items:
- ✅ TradeSnapshot updated with `their_waiver_recommendations` field
- ✅ All 6 trade types calculate opponent waiver needs
- ✅ Waivers added to rosters BEFORE TradeSimTeam creation
- ✅ Team scores naturally include waiver players
- ✅ Console and file output show both user and opponent waivers
- ✅ Tests updated for waiver functionality
- ✅ All 362 tests passing

### Implementation Details:
- **File Modified**: `TradeSnapshot.py` (added `their_waiver_recommendations` parameter)
- **File Modified**: `TradeSimulatorModeManager.py` (all 6 trade types updated)
- **File Modified**: `test_trade_simulator.py` (7 new waiver tests added)
- **Lines Modified**: 1330-1807 (trade generation blocks)
- **Lines Modified**: 372-382 (console output)
- **Lines Modified**: 1861-1871 (file output)

---

## Phase 2 (Drop System) - ✅ COMPLETE

### Completed Items:
- ✅ TradeSnapshot updated with `my_dropped_players` and `their_dropped_players` fields (lines 17-18, 40-41)
- ✅ Helper method `_get_lowest_scored_players_per_position()` created (lines 946-997)
- ✅ 1:2 trades: User drop system implemented (lines 1487-1553)
- ✅ 1:3 trades: User drop system with 2-player combinations (lines 1705-1771)
- ✅ 2:3 trades: User drop system implemented (lines 1927-1993)
- ✅ 2:1 trades: Opponent drop system implemented (lines 1427-1478)
- ✅ 3:1 trades: Opponent drop system with 2-player combinations (lines 1695-1746)
- ✅ 3:2 trades: Opponent drop system implemented (lines 1965-2016)
- ✅ Console display output for dropped players (lines 384-394)
- ✅ File output for dropped players (lines 2274-2284)
- ✅ Tests for drop functionality (6 new tests added to test_trade_simulator.py)
- ✅ Full test suite validation (367/367 tests passing - 100%)

### Implementation Summary:

**Drop System Logic Flow**:
1. Unequal trade attempted (e.g., 1:2, 3:1, etc.)
2. Roster validation fails (would exceed MAX_PLAYERS = 15)
3. System identifies team receiving MORE players
4. Calls `_get_lowest_scored_players_per_position()`:
   - Excludes players being traded away
   - Excludes locked players
   - Returns lowest 2 scorers per position (QB, RB, WR, TE, K, DST)
5. Tries all drop combinations:
   - 1 drop for net +1 roster change (1:2, 2:1, 2:3, 3:2)
   - 2 drops for net +2 roster change (1:3, 3:1)
6. For each drop variation:
   - Validates roster is legal
   - Creates TradeSimTeam with drops applied
   - Compares against ORIGINAL team score
   - Suggests only if improvement ≥ MIN_TRADE_IMPROVEMENT (30 pts)
7. Creates TradeSnapshot with dropped players included
8. Displays in console and saves to file

**Key Features**:
- **Smart Selection**: Only lowest scorers per position considered
- **Fair Evaluation**: Final score vs original (not vs hypothetical legal trade)
- **Bilateral**: Works for both user and opponent teams
- **Transparent**: Shows exactly who must be dropped
- **Efficient**: Limits search space to 2 per position

**Test Coverage**:
- `test_tradesnapshot_with_my_dropped_players()` - User drops storage
- `test_tradesnapshot_with_their_dropped_players()` - Opponent drops storage
- `test_tradesnapshot_without_dropped_players()` - Default empty lists
- `test_tradesnapshot_dropped_players_none_becomes_empty_list()` - None handling
- `test_tradesnapshot_with_all_fields()` - All optional fields together
- Plus integration with existing trade generation tests

---

# IMPLEMENTATION COMPLETE ✅

## Final Status Summary

### ✅ Phase 1 (Waiver System) - COMPLETE
**Implementation Date**: Session 2
**Files Modified**:
- `TradeSnapshot.py` - Added `their_waiver_recommendations`
- `TradeSimulatorModeManager.py` - All 6 trade types calculate opponent waivers
- `test_trade_simulator.py` - 7 new waiver tests

**Key Changes**:
- Waivers calculated for BOTH teams (user and opponent)
- Waivers added to rosters BEFORE TradeSimTeam creation
- Team scores naturally include waiver players
- Console output lines 372-382
- File output lines 1861-1871 (before drop system was added)
- Tests passing: 362/362 (100%)

### ✅ Phase 2 (Drop System) - COMPLETE
**Implementation Date**: Session 2 (continued)
**Files Modified**:
- `TradeSnapshot.py` - Added `my_dropped_players` and `their_dropped_players`
- `TradeSimulatorModeManager.py` - Drop logic for all 6 trade types
- `test_trade_simulator.py` - 6 new drop tests

**Key Changes**:
- Helper method `_get_lowest_scored_players_per_position()` (lines 946-997)
- User drop systems: 1:2, 1:3, 2:3 trades
- Opponent drop systems: 2:1, 3:1, 3:2 trades
- Console output lines 384-394
- File output lines 2274-2284
- Tests passing: 367/367 (100%)

---

## Project Statistics

**Total Lines Added**: ~600 lines
- Drop logic implementations: ~450 lines
- Test code: ~150 lines

**Test Coverage**:
- New tests added: 13 (7 waiver + 6 drop)
- Total tests: 367
- Pass rate: 100%
- Test file: `tests/league_helper/trade_simulator_mode/test_trade_simulator.py`

**Backward Compatibility**: ✅ YES
- All new parameters are optional with default values
- Existing TradeSnapshot calls work without modification
- No breaking changes to public API

---

## Next Steps (If Needed)

### Potential Future Enhancements:
1. **Performance Optimization**:
   - Cache drop candidate calculations
   - Parallelize drop combination testing
   - Add progress indicators for large combination spaces

2. **Enhanced Drop Intelligence**:
   - Consider position scarcity (don't drop last RB)
   - Factor in bye weeks for drop decisions
   - Weight recent performance more heavily

3. **User Configuration**:
   - Allow user to set `num_per_position` for drop candidates
   - Configure MIN_TRADE_IMPROVEMENT per trade type
   - Enable/disable drop system via constants

4. **Additional Output**:
   - Show drop reasoning in output (why this player was selected)
   - Display alternative drop options
   - Export drop analysis to separate file

5. **Testing Enhancements**:
   - Add integration tests with real roster data
   - Performance benchmarks for drop combinations
   - Edge case testing (all positions full, etc.)

---

## Documentation Updates Needed

If this feature is considered stable and complete:

1. **Update README.md**: Add section on drop system functionality
2. **Update CLAUDE.md**: Document drop system patterns if applicable
3. **Update PROJECT_DOCUMENTATION.md**: Add drop system architecture details
4. **Create User Guide**: Explain how drops work in trade suggestions

---

## Completion Checklist

- [x] Requirements gathered and clarified
- [x] Phase 1 (Waiver System) implemented
- [x] Phase 2 (Drop System) implemented
- [x] All tests passing (100%)
- [x] Console output updated
- [x] File output updated
- [x] Backward compatibility verified
- [x] Code reviewed for quality
- [x] Documentation updated (this file)
- [x] Ready for commit

**STATUS**: ✅ READY TO COMMIT

**Suggested Commit Message**:
```
Add drop system for unequal trades with roster violations

Phase 1 (Waiver System):
- Add opponent waiver recommendations
- Include waivers in team score calculations
- Update display output for both teams' waivers

Phase 2 (Drop System):
- Implement drop logic for all 6 unequal trade types
- Add smart drop candidate selection (lowest scorers per position)
- Handle both user and opponent roster violations
- Compare final scores against original team scores
- Display dropped players in console and file output

Files Modified:
- TradeSnapshot.py: Add waiver and drop player fields
- TradeSimulatorModeManager.py: Core drop and waiver logic
- test_trade_simulator.py: 13 new tests for waivers and drops

Tests: 367/367 passing (100%)
Backward Compatible: Yes (all new fields optional)
```
