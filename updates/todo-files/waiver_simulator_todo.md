# Waiver Simulator TODO

**Objective**: Add "Waiver" option to Manual Trade Visualizer for analyzing trades with waiver wire players

**Status**: 🔨 DRAFT - Awaiting first verification round (3 iterations)

**Keep this file updated**: As you complete tasks, mark them as DONE and add notes about any issues encountered or decisions made. This ensures continuity if work spans multiple sessions.

---

## Original Requirements

From `updates/waiver_simulator.txt`:
1. Add an option to the Trade Visualizer that allows you to visualize a specific trade between one or more of the user's players and one or more of the waiver players
2. This option should appear in the list of other teams that the user can choose to trade from
3. Any trades that are simulated should not bother considering any position limits or team constraints on the waivers "team". It should only assess how the user's team will change

---

## Phase 1: Add Waiver Option to Manual Trade Visualizer UI

### Task 1.1: Modify opponent selection to include "Waiver" option
**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
**Location**: `start_manual_trade()` method (lines 540-557)

- [ ] Create waiver player list using existing pattern from `start_waiver_optimizer()` (line 240)
- [ ] Create TradeSimTeam for waivers: `TradeSimTeam("Waiver Wire", waiver_players, self.player_manager, isOpponent=True)`
- [ ] Add "Waiver" as an option to the opponent selection menu (before or after opponent teams list)
- [ ] Handle case where "Waiver" option is selected
- [ ] Store selected opponent type (regular team vs waiver) for later use

**Pattern**: Similar to `start_waiver_optimizer()` lines 234-249

**Questions**:
- Should "Waiver" appear at the top of the list, bottom, or alphabetically sorted with team names?
- What should happen if no waiver players are available? (empty waiver list)
- Should waiver players be filtered by minimum score threshold like in waiver optimizer? (uses `Constants.MIN_WAIVER_IMPROVEMENT`)

**Iteration 2 Addition - Error Handling**:
- [ ] Add logging when waiver option selected: `self.logger.info("Selected Waiver Wire for manual trade")`
- [ ] Add logging for waiver player count: `self.logger.info(f"Found {len(waiver_players)} waiver players")`
- [ ] Add warning if waiver list empty: `self.logger.warning("No waiver players available")`

**Iteration 2 Addition - Constants**:
- [ ] Use `Constants.MIN_WAIVER_IMPROVEMENT` for filtering waiver players (line 239 pattern)
- [ ] Consider if waiver filtering should be optional for manual trades (ask user)

### Task 1.2: Pass waiver flag to trade processing
**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
**Location**: `start_manual_trade()` method (around line 632)

- [ ] Track whether selected opponent is waivers or regular team
- [ ] Pass `is_waivers` flag to `analyzer.process_manual_trade()` call
- [ ] Update method call to include new parameter

**Pattern**: Similar to `get_trade_combinations()` call with `is_waivers=True` (line 259)

---

## Phase 2: Update Trade Processing to Skip Waiver Validation

### Task 2.1: Add is_waivers parameter to process_manual_trade()
**File**: `league_helper/trade_simulator_mode/trade_analyzer.py`
**Location**: `process_manual_trade()` method definition (line 434)

- [ ] Add `is_waivers: bool = False` parameter to method signature
- [ ] Update docstring to explain is_waivers parameter behavior
- [ ] Document that waiver validation is skipped when is_waivers=True

**Pattern**: Similar to `get_trade_combinations()` which has `is_waivers` parameter

### Task 2.2: Conditionally skip waiver team validation
**File**: `league_helper/trade_simulator_mode/trade_analyzer.py`
**Location**: `process_manual_trade()` method (lines 533-547)

- [ ] Wrap "their team" validation logic in `if not is_waivers:` conditional
- [ ] When is_waivers=True, skip validation of their_roster (line 547)
- [ ] When is_waivers=True, skip drop candidate generation for their team (lines 565-574)
- [ ] Ensure my team validation still runs normally
- [ ] Update roster validity check (line 550) to account for skipped waiver validation

**Logic**:
```python
# Validate their team's roster ONLY if not waivers
if is_waivers:
    their_roster_valid = True  # Skip validation for waiver "team"
else:
    their_roster_valid = self.validate_roster_lenient(their_original_full_roster, their_full_roster)
```

**Questions**:
- Should we still generate waiver recommendations for user's team when trading with waivers?
- Should drop candidates be offered for user if their roster becomes invalid?

---

## Phase 3: Update Tests

### Task 3.1: Update existing manual trade tests
**File**: `tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py`

- [ ] Review existing tests to ensure they still pass
- [ ] Add `is_waivers=False` to existing `process_manual_trade()` test calls if needed
- [ ] Verify no regression in normal team-to-team trading

**Pattern**: Follow existing test structure in file

### Task 3.2: Add new waiver trade tests
**File**: `tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py`

- [ ] Test `process_manual_trade()` with `is_waivers=True`
- [ ] Test that waiver team validation is skipped
- [ ] Test that user team validation still runs
- [ ] Test waiver trade with invalid user roster (drops required)
- [ ] Test waiver trade with valid user roster
- [ ] Test edge case: empty waiver player list

**Tests to create** (following existing `is_waivers` test pattern from test_trade_analyzer.py:332):
- `test_manual_trade_waiver_skips_their_validation()` - Verify `is_waivers=True` skips waiver validation
- `test_manual_trade_waiver_validates_my_team()` - Verify user team still validated
- `test_manual_trade_waiver_with_drops_required()` - Test drops when user roster invalid
- `test_manual_trade_waiver_valid_roster()` - Test successful waiver trade
- `test_start_manual_trade_waiver_selection()` - Test UI flow when selecting "Waiver" option
- `test_start_manual_trade_empty_waivers()` - Test edge case with no waiver players

**Mock Pattern** (from test_trade_analyzer.py:336):
```python
analyzer.validate_roster_lenient = Mock(return_value=True)
mock_my_new = Mock()
mock_my_new.team_score = 106.0
```

---

## Phase 4: Documentation

### Task 4.1: Update method docstrings
- [ ] Update `start_manual_trade()` docstring to mention waiver option
- [ ] Update `process_manual_trade()` docstring to explain is_waivers parameter

### Task 4.2: Update README.md if needed
**File**: `README.md`
- [ ] Check if Manual Trade Visualizer is documented
- [ ] Add mention of waiver trading option if documented
- [ ] Explain that waiver trades skip opponent validation

### Task 4.3: Update CLAUDE.md if needed
**File**: `CLAUDE.md`
- [ ] Check if trade simulator mode details are present
- [ ] Update if manual trade visualizer workflow is documented

---

## Phase 5: Pre-Commit Validation

### Task 5.1: Run all unit tests
- [ ] Execute: `python tests/run_all_tests.py`
- [ ] Ensure 100% pass rate (all 1855+ tests)
- [ ] Fix any failing tests before proceeding

### Task 5.2: Manual testing
- [ ] Run: `python run_league_helper.py`
- [ ] Select Trade Simulator mode
- [ ] Select Manual Trade Visualizer
- [ ] Verify "Waiver" appears in opponent selection list
- [ ] Test trade with waiver players
- [ ] Test that waiver trades skip validation for waiver side
- [ ] Test that user roster validation still works

### Task 5.3: Edge case testing
- [ ] Test with empty waiver wire
- [ ] Test with large waiver wire (many players)
- [ ] Test unequal trades (1-for-2, 2-for-1) with waivers
- [ ] Test equal trades (1-for-1, 2-for-2) with waivers

---

## Implementation Notes

**Key Files**:
- `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` - Add waiver option to UI
- `league_helper/trade_simulator_mode/trade_analyzer.py` - Skip waiver validation
- `tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py` - Add tests

**Existing Patterns to Follow**:
- Waiver player retrieval: `start_waiver_optimizer()` lines 234-249
- TradeSimTeam creation: `TradeSimTeam("Waiver Wire", waiver_players, self.player_manager, isOpponent=True)`
- `is_waivers` flag usage: `get_trade_combinations()` line 259

**Dependencies**:
- Phase 1 must complete before Phase 2 (need flag to pass)
- Phase 2 must complete before Phase 3 (tests depend on implementation)
- Phase 3 must complete before Phase 4 (validate tests pass before documenting)
- All phases must complete before Phase 5 (final validation)

---

## Verification Summary

**Iteration 1 Complete**: ✅
- Re-read original requirements file
- Verified all 4 explicit requirements covered in TODO
- No missing requirements found
- Researched `show_list_selection()` - takes list of options, displays numbered menu
- Researched waiver player retrieval - `player_manager.get_player_list(drafted_vals=[0], ...)`
- Researched `display_combined_roster()` - accepts team name parameter, no changes needed
- Found edge case handling pattern (lines 243-245 in waiver optimizer)

**Findings**:
- `show_list_selection()` is simple - just add "Waiver" to options list
- Waiver team name will display automatically in combined roster
- Empty waiver list should be handled with early return (similar to line 243-245)
- `is_waivers=True` pattern already used in `get_trade_combinations()`

**Questions Identified for User**:
1. Where should "Waiver" appear in team selection list? (top, bottom, or alphabetically)
2. Should waiver players be filtered by minimum score threshold?
3. What message to show if waiver wire is empty?

**Iteration 2 Complete**: ✅
- Researched logging patterns: `.info()` for steps, `.warning()` for edge cases, `.debug()` for details
- Researched constants: `Constants.MIN_WAIVER_IMPROVEMENT` used in waiver optimizer (line 239)
- No circular dependency risk identified (TradeAnalyzer imported by Manager, not vice versa)
- Added error handling tasks: logging for waiver selection, waiver count, empty list warning
- Added constants usage: MIN_WAIVER_IMPROVEMENT filter pattern

**Additional Questions for User**:
4. Should waiver filtering (MIN_WAIVER_IMPROVEMENT) be optional for manual trades?
5. Should we reuse existing waiver team name "Waiver Wire" or allow customization?

**Iteration 3 Complete**: ✅
- Researched test mock patterns: `unittest.mock`, `Mock()`, `patch()` (test_trade_analyzer.py)
- Found existing `is_waivers=True` test at line 332 in test_trade_analyzer.py
- Verified test pattern: mocking validate_roster_lenient, TradeSimTeam, and TradeSnapshot
- Added 6 test cases to TODO (UI flow, validation skip, edge cases)
- Added mock pattern example to Phase 3 Task 3.2
- No additional integration points identified - changes isolated to TradeSimulatorModeManager and TradeAnalyzer
- File paths verified: all absolute, proper Path construction

**Risk Areas Identified**:
1. Empty waiver list handling (mitigated with early return pattern)
2. User confusion if "Waiver" appears in wrong position in list (addressed in questions)
3. Performance with large waiver lists (likely fine - same as waiver optimizer)

**Final Questions for User** (Total: 5):
1. Where should "Waiver" appear in team selection list? (top, bottom, or alphabetically)
2. What message to show if waiver wire is empty?
3. Should waiver players be filtered by minimum score threshold? (Constants.MIN_WAIVER_IMPROVEMENT)
4. Should waiver filtering be optional for manual trades?
5. Should we reuse "Waiver Wire" name or allow customization?

**Status**: ✅ FIRST VERIFICATION ROUND COMPLETE (3 iterations) - Ready to create questions file
