# Manual Trade Visualizer - Implementation TODO

**Objective**: Implement manual trade visualizer feature that allows users to manually select players for trades and see the impact analysis.

**Status**: Questions answered - Ready for implementation

**Important**: Keep this file updated with progress after completing each task. Mark tasks as [DONE] when completed.

---

## Quick Reference Summary

**Implementation Location**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
**Test Location**: `tests/league_helper/trade_simulator_mode/test_TradeSimulatorModeManager_manual_trade.py`
**Documentation**: `updates/manual_trade_visualizer_code_changes.md`

**Methods to Implement:**
1. `_display_numbered_roster(roster, title)` - Display roster with numbers
2. `_parse_player_selection(input_str, max_index)` - Parse comma-separated input
3. `_get_players_by_indices(roster, indices)` - Extract players by indices
4. `_display_trade_result(trade, original_my_score, original_their_score)` - Show trade impact
5. `_save_manual_trade_to_file(trade, opponent_name, original_my_score, original_their_score)` - Save to file
6. `start_manual_trade()` - Main workflow (replace stub at line 282)

**Key Design Decisions:**
- File naming: `trade_info_{opponent_name}_{timestamp}.txt`
- Input handling: Accept spaces, 'exit' to cancel, re-prompt on invalid
- Display: Use FantasyPlayer.__str__ in numbered list format
- Validation: Reuse _validate_roster() method
- Trade filtering: Show ANY trade (not just mutually beneficial)
- Return type: `Tuple[bool, List[TradeSnapshot]]` (matches other modes)

**Test Coverage Target**: >80%
**Test Pass Requirement**: 100% (MANDATORY before commit)

---

## Phase 0: Planning & Clarification
- [x] Create questions file for requirement clarification
- [x] Wait for user to answer questions
- [x] Update this TODO based on answers
- [x] Create code changes documentation file: `updates/manual_trade_visualizer_code_changes.md`

---

## Phase 1: Core Implementation

**Key Design Decisions from Question Answers:**
- Input format: Accept spaces in comma-separated numbers, no ranges, 'exit' to cancel
- Display: Use FantasyPlayer.__str__ with numbered list format (similar to show_list_selection)
- Validation: Reuse _validate_roster() method from TradeSimulatorModeManager
- Display format: Same format as start_trade_suggestor() for consistency
- File naming: `trade_info_{opponent_name}_{timestamp}.txt`
- Workflow: One trade, save/skip, return to menu
- Error handling: Alert user and return to Trade Simulator menu
- Trade filtering: Show ANY trade (not just mutually beneficial), bypass get_trade_combinations
- Locked players: Allowed in manual trades

### Step 1.1: Create Helper Method - Display Numbered Roster
**Location**: TradeSimulatorModeManager class (line ~283)
**Method signature**: `_display_numbered_roster(self, roster: List[FantasyPlayer], title: str) -> None`

**Implementation details:**
- [ ] Print header with title (format: "="*25, title, "="*25)
- [ ] Iterate through roster with enumerate(roster, 1)
- [ ] Print each player as: `f"{i}. {player}"` (uses FantasyPlayer.__str__)
- [ ] Print footer separator ("="*25)
- [ ] Include docstring explaining purpose and parameters

**Testing considerations:**
- Unit test with empty roster
- Unit test with 1 player
- Unit test with multiple players
- Verify output format matches show_list_selection style

### Step 1.2: Create Helper Method - Parse Player Selection
**Location**: TradeSimulatorModeManager class (line ~295)
**Method signature**: `_parse_player_selection(self, input_str: str, max_index: int) -> Optional[List[int]]`

**Implementation details:**
- [ ] Strip whitespace from input_str
- [ ] Check if input is 'exit' (case-insensitive), return None if True
- [ ] Split by comma and strip whitespace from each element
- [ ] Try to convert each element to int, catch ValueError
- [ ] Validate each index is in range [1, max_index]
- [ ] Check for duplicate indices (set vs list length comparison)
- [ ] Return list of valid indices (1-based) or None on any error
- [ ] Include comprehensive docstring

**Edge cases to handle:**
- Empty string: Return None
- Invalid characters: Return None
- Out of range numbers: Return None
- Negative numbers: Return None
- Duplicate numbers: Return None
- Mixed valid/invalid: Return None

### Step 1.3: Create Helper Method - Get Players by Indices
**Location**: TradeSimulatorModeManager class (line ~315)
**Method signature**: `_get_players_by_indices(self, roster: List[FantasyPlayer], indices: List[int]) -> List[FantasyPlayer]`

**Implementation details:**
- [ ] Convert 1-based indices to 0-based (subtract 1)
- [ ] Extract players at each index from roster
- [ ] Return list of FantasyPlayer objects
- [ ] Simple helper to avoid index math duplication

### Step 1.4: Create Helper Method - Display Trade Results
**Location**: TradeSimulatorModeManager class (line ~325)
**Method signature**: `_display_trade_result(self, trade: TradeSnapshot, original_my_score: float, original_their_score: float) -> None`

**Implementation details:**
- [ ] Calculate my_improvement = trade.my_new_team.team_score - original_my_score
- [ ] Calculate their_improvement = trade.their_new_team.team_score - original_their_score
- [ ] Print header ("="*80)
- [ ] Print "MANUAL TRADE VISUALIZER - Trade Impact Analysis"
- [ ] Print "="*80
- [ ] Print f"Trade with {trade.their_new_team.name}"
- [ ] Print my improvement and new score (format: +X.2f pts)
- [ ] Print their improvement and new score (format: +X.2f pts)
- [ ] Print "I give:" followed by list of trade.their_new_players
- [ ] Print "I receive:" followed by list of trade.my_new_players
- [ ] Print footer ("="*80)
- [ ] **REFACTOR OPPORTUNITY**: Extract display logic from start_trade_suggestor() (lines 269-278)

**Refactoring note:**
- Lines 269-278 in start_trade_suggestor() contain similar display logic
- Consider extracting shared formatting into this method
- Update start_trade_suggestor() to call this method instead of duplicating code

### Step 1.5: Create Helper Method - Save Manual Trade to File
**Location**: TradeSimulatorModeManager class (line ~345)
**Method signature**: `_save_manual_trade_to_file(self, trade: TradeSnapshot, opponent_name: str, original_my_score: float, original_their_score: float) -> None`

**Implementation details:**
- [ ] Import datetime at top of file: `from datetime import datetime`
- [ ] Generate timestamp: `timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")`
- [ ] Create filename: `f"trade_info_{opponent_name}_{timestamp}.txt"`
- [ ] Sanitize opponent_name (replace spaces with underscores)
- [ ] Calculate improvements (same as _display_trade_result)
- [ ] Open file in write mode
- [ ] Write same content as displayed by _display_trade_result (reuse formatting)
- [ ] Add success message after writing

**File format** (matches TradeSnapshot display):
```
Trade with {opponent_name}
  My improvement: +X.XX pts (New score: Y.YY)
  Their improvement: +X.XX pts (New score: Y.YY)
  I give:
    - Player Name (POS) - TEAM
  I receive:
    - Player Name (POS) - TEAM
```

### Step 1.6: Implement start_manual_trade() Method
**Location**: TradeSimulatorModeManager.start_manual_trade() (line 282-283)
**Method signature**: Already exists, replace `return False` with full implementation
**Return type**: `Tuple[bool, List[TradeSnapshot]]` (matches other mode methods)

**Implementation flow:**

**Part A: Validate opponent teams exist**
- [ ] Check if len(self.opponent_simulated_teams) == 0
- [ ] If no opponents: print error message, return (True, [])
- [ ] Error message: "No opponent teams available for manual trade analysis."

**Part B: Display user's roster and get player selection**
- [ ] Call _display_numbered_roster(self.my_team.team, "YOUR ROSTER - Select Players to Trade")
- [ ] Prompt user: "Enter player numbers to trade (comma-separated, or 'exit' to cancel): "
- [ ] Call _parse_player_selection(input_str, len(self.my_team.team))
- [ ] If None returned: print "Trade cancelled." and return (True, [])
- [ ] If invalid: print "Invalid selection. Please try again." and return (True, [])
- [ ] Call _get_players_by_indices to get my_selected_players
- [ ] Validate roster won't be empty: if len(my_selected_players) == len(self.my_team.team), print error and return (True, [])

**Part C: Select opponent team**
- [ ] Create list of opponent names from self.opponent_simulated_teams
- [ ] Call show_list_selection("SELECT OPPONENT TEAM", opponent_names, "Cancel")
- [ ] If choice > len(opponent_names): return (True, [])
- [ ] Get selected opponent: opponent = self.opponent_simulated_teams[choice - 1]

**Part D: Display opponent roster and get player selection**
- [ ] Call _display_numbered_roster(opponent.team, f"{opponent.name}'S ROSTER - Select Players to Receive")
- [ ] Prompt user: "Enter player numbers to receive (comma-separated, or 'exit' to cancel): "
- [ ] Call _parse_player_selection(input_str, len(opponent.team))
- [ ] If None returned: print "Trade cancelled." and return (True, [])
- [ ] If invalid: print "Invalid selection." and return (True, [])
- [ ] Call _get_players_by_indices to get their_selected_players
- [ ] Validate opponent roster won't be empty: if len(their_selected_players) == len(opponent.team), print error and return (True, [])

**Part E: Create new rosters and validate**
- [ ] Create my_new_roster: Remove my_selected_players, add their_selected_players
  - `my_new_roster = [p for p in self.my_team.team if p not in my_selected_players] + their_selected_players`
- [ ] Create their_new_roster: Remove their_selected_players, add my_selected_players
  - `their_new_roster = [p for p in opponent.team if p not in their_selected_players] + my_selected_players`
- [ ] Validate my_new_roster with _validate_roster(my_new_roster)
- [ ] Validate their_new_roster with _validate_roster(their_new_roster)
- [ ] If either invalid: print "Trade violates roster constraints." and return (True, [])

**Part F: Create TradeSnapshot and calculate impact**
- [ ] Create my_new_team = TradeSimTeam(self.my_team.name, my_new_roster, self.player_manager, isOpponent=False)
- [ ] Create their_new_team = TradeSimTeam(opponent.name, their_new_roster, self.player_manager, isOpponent=True)
- [ ] Create trade = TradeSnapshot(my_new_team, their_selected_players, their_new_team, my_selected_players)
- [ ] Store original scores: original_my_score = self.my_team.team_score, original_their_score = opponent.team_score
- [ ] Call _display_trade_result(trade, original_my_score, original_their_score)

**Part G: Save to file option**
- [ ] Print blank line
- [ ] Prompt: "Save this trade to a file? (y/n): "
- [ ] Get input, strip, and convert to lowercase
- [ ] If input == 'y': call _save_manual_trade_to_file(trade, opponent.name, original_my_score, original_their_score)
- [ ] If 'y': print f"Trade saved to trade_info_{opponent.name}_{timestamp}.txt"
- [ ] Return (True, [trade]) to pass trade to save_trades_to_file (which will be skipped in run_interactive_mode)

**Error handling throughout:**
- Wrap input() calls in try-except KeyboardInterrupt to handle Ctrl+C gracefully
- Return (True, []) to return to Trade Simulator menu on any error

---

## Phase 2: Testing & Validation

**Test Coverage Target**: >80% (per Q11 answer)
**Test File Location**: `tests/league_helper/trade_simulator_mode/test_TradeSimulatorModeManager_manual_trade.py`

### Step 2.1: Unit Tests for Helper Methods

**Test _display_numbered_roster():**
- [ ] Test with empty roster (should print header/footer only)
- [ ] Test with single player roster
- [ ] Test with multiple players (verify numbering starts at 1)
- [ ] Use capsys fixture to capture stdout
- [ ] Verify output format matches: `"{i}. {player}"`

**Test _parse_player_selection():**
- [ ] Test valid single number: "1" → [1]
- [ ] Test valid multiple numbers: "1,2,3" → [1,2,3]
- [ ] Test with spaces: "1, 2, 3" → [1,2,3]
- [ ] Test 'exit' (lowercase) → None
- [ ] Test 'EXIT' (uppercase) → None
- [ ] Test 'Exit' (mixed case) → None
- [ ] Test empty string → None
- [ ] Test invalid characters: "1,a,3" → None
- [ ] Test out of range: "1,99" with max_index=5 → None
- [ ] Test negative numbers: "1,-2" → None
- [ ] Test zero: "0,1" → None
- [ ] Test duplicates: "1,2,1" → None
- [ ] Test leading/trailing spaces: "  1, 2  " → [1,2]

**Test _get_players_by_indices():**
- [ ] Test extracting single player by index
- [ ] Test extracting multiple players by indices
- [ ] Test indices in non-sequential order
- [ ] Verify correct players returned (check player IDs or names)
- [ ] Test with mock FantasyPlayer objects

**Test _display_trade_result():**
- [ ] Create mock TradeSnapshot with test data
- [ ] Verify header/footer formatting ("="*80)
- [ ] Verify improvement calculations displayed correctly
- [ ] Verify "I give:" and "I receive:" sections
- [ ] Use capsys to capture and verify output

**Test _save_manual_trade_to_file():**
- [ ] Mock datetime.now() to control timestamp
- [ ] Verify file created with correct name format
- [ ] Verify file content matches expected format
- [ ] Test with opponent name containing spaces (verify underscore replacement)
- [ ] Use tmp_path fixture for file operations
- [ ] Verify file content matches _display_trade_result output format

### Step 2.2: Integration Tests for start_manual_trade()

**Test full workflow with mocked input:**
- [ ] Mock input() calls using unittest.mock.patch
- [ ] Test complete successful trade flow:
  - Select own players: "1,2"
  - Select opponent team: 1
  - Select opponent players: "3,4"
  - Save to file: "y"
- [ ] Verify TradeSnapshot returned in tuple
- [ ] Verify file created with correct content

**Test 'exit' at each input stage:**
- [ ] Mock input to return 'exit' at own player selection
- [ ] Verify returns (True, [])
- [ ] Verify "Trade cancelled." printed
- [ ] Mock input to return 'exit' at opponent player selection
- [ ] Verify returns (True, [])

**Test invalid inputs:**
- [ ] Mock invalid player selection (out of range)
- [ ] Verify error message printed
- [ ] Verify returns (True, [])
- [ ] Mock invalid opponent team selection (> max)
- [ ] Verify returns (True, [])

**Test edge case: no opponent teams:**
- [ ] Set self.opponent_simulated_teams = []
- [ ] Verify error message printed
- [ ] Verify returns (True, [])

**Test edge case: empty roster validation:**
- [ ] Mock selecting ALL players from own roster
- [ ] Verify error message printed
- [ ] Verify returns (True, [])
- [ ] Same test for opponent roster

**Test roster constraint violations:**
- [ ] Mock trade that violates position limits
- [ ] Mock _validate_roster to return False
- [ ] Verify error message printed
- [ ] Verify returns (True, [])

**Test save to file declined:**
- [ ] Complete full trade flow
- [ ] Mock save prompt response: "n"
- [ ] Verify no file created
- [ ] Verify still returns (True, [trade])

### Step 2.3: Run All Tests
- [ ] Run `python tests/run_all_tests.py`
- [ ] Ensure 100% pass rate
- [ ] Verify >80% code coverage for new methods
- [ ] Check coverage report: `pytest --cov=league_helper.trade_simulator_mode.TradeSimulatorModeManager --cov-report=term-missing`

### Step 2.4: Manual Integration Testing
**Manual test scenarios to verify:**
- [ ] Launch application, navigate to Trade Simulator → Manual Trade Visualizer
- [ ] Test with real data: select 1 player to trade
- [ ] Test with real data: select 2 players to trade
- [ ] Test typing 'exit' at own player selection (returns to menu)
- [ ] Test typing 'exit' at opponent player selection (returns to menu)
- [ ] Test invalid input: "1,99" (should re-prompt or return to menu)
- [ ] Test invalid input: "1,a,3" (should re-prompt or return to menu)
- [ ] Test save to file: verify file created with timestamp
- [ ] Test decline save: verify no file created
- [ ] Open generated file, verify format matches expectations
- [ ] Test with locked players (verify they CAN be selected)

### Step 2.5: Mock Examples for Reference

**Example: Mocking input() for trade flow:**
```python
from unittest.mock import patch

@patch('builtins.input', side_effect=['1,2', '1', '3,4', 'y'])
def test_complete_trade_flow(mock_input, manager):
    # Setup test data
    # Call start_manual_trade()
    # Verify results
```

**Example: Mocking datetime for filename:**
```python
from unittest.mock import patch
from datetime import datetime

@patch('league_helper.trade_simulator_mode.TradeSimulatorModeManager.datetime')
def test_save_file_timestamp(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 10, 16, 12, 30, 45)
    # Expected filename: trade_info_OpponentName_20251016_123045.txt
```

---

## Phase 3: Documentation & Cleanup

### Step 3.1: Code Documentation
**Ensure all methods have comprehensive docstrings:**
- [ ] _display_numbered_roster: Document purpose, parameters (roster, title), return type
- [ ] _parse_player_selection: Document purpose, parameters (input_str, max_index), return type (Optional[List[int]]), edge cases
- [ ] _get_players_by_indices: Document purpose, parameters (roster, indices), return type
- [ ] _display_trade_result: Document purpose, parameters (trade, original_my_score, original_their_score), return type
- [ ] _save_manual_trade_to_file: Document purpose, parameters, file format, return type
- [ ] start_manual_trade: Update docstring with complete workflow description, return type

**Docstring format example:**
```python
def _parse_player_selection(self, input_str: str, max_index: int) -> Optional[List[int]]:
    """
    Parse comma-separated player numbers from user input.

    Args:
        input_str (str): User input string with comma-separated numbers
        max_index (int): Maximum valid index (1-based)

    Returns:
        Optional[List[int]]: List of valid 1-based indices, or None if:
            - Input is 'exit' (case-insensitive)
            - Input contains invalid characters
            - Any number is out of range [1, max_index]
            - Duplicate numbers detected

    Examples:
        >>> _parse_player_selection("1,2,3", 5)
        [1, 2, 3]
        >>> _parse_player_selection("exit", 5)
        None
        >>> _parse_player_selection("1,99", 5)
        None
    """
```

### Step 3.2: Update Code Changes Documentation
**File**: `updates/manual_trade_visualizer_code_changes.md`

**Document all changes made:**
- [ ] List all new methods added to TradeSimulatorModeManager
- [ ] Document new import: `from datetime import datetime`
- [ ] Document changes to start_manual_trade() (replaced stub with full implementation)
- [ ] Document any refactoring done (if display logic extracted from start_trade_suggestor)
- [ ] List all test files created
- [ ] Document file naming convention: `trade_info_{opponent_name}_{timestamp}.txt`
- [ ] Include code snippets for key methods
- [ ] Note any design decisions or trade-offs made during implementation

### Step 3.3: Update Project Documentation (if needed)
**Check if updates required:**
- [ ] Review README.md - does it list Trade Simulator features?
- [ ] If yes, add "Manual Trade Visualizer" to feature list
- [ ] Review CLAUDE.md - does it need updates? (unlikely unless workflow changed)
- [ ] Review any relevant module documentation in `league_helper/` directory

---

## Phase 4: Final Verification (MANDATORY)

### Step 4.1: Requirement Verification Protocol
**Reference**: rules.txt lines 11-71

**Process:**
- [ ] Re-read original `updates/manual_trade_visualizer.txt` file
- [ ] Extract EVERY requirement from the file (line by line if needed)
- [ ] Create comprehensive checklist in code changes file
- [ ] For each requirement, verify implementation:
  - ✅ Implemented correctly
  - ❌ Not implemented or incorrect
- [ ] Search codebase for implementation evidence using Grep tool
- [ ] Document verification results in code changes file

**Requirements Checklist (preliminary - expand during verification):**
1. [ ] Display numbered list of user's roster
2. [ ] User can enter comma-separated player numbers
3. [ ] Display numbered list of opponent teams
4. [ ] User can select opponent team
5. [ ] Display numbered list of opponent's roster
6. [ ] User can enter comma-separated opponent player numbers
7. [ ] Calculate trade impact (score changes)
8. [ ] Display trade results (my improvement, their improvement)
9. [ ] Prompt y/n to save results
10. [ ] Save to file if yes
11. [ ] Return to Trade Simulator menu

**Question Answer Verification (all must be implemented):**
- [ ] Q1: Accept spaces, no ranges, 'exit' to cancel, re-ask on invalid
- [ ] Q2: Use FantasyPlayer.__str__, numbered list format
- [ ] Q3: Same validation as waiver/trade suggestor
- [ ] Q4: Same display format as waiver/trade
- [ ] Q5: File naming: `trade_info_{opponent_name}_{timestamp}.txt`
- [ ] Q6: One trade per session, save/skip, return to menu
- [ ] Q7: No pre-confirmations, error handling returns to menu
- [ ] Q8: All edge cases alert user and return to menu
- [ ] Q9: Show any trade, bypass get_trade_combinations
- [ ] Q10: Locked players allowed
- [ ] Q11: >80% test coverage, unit + integration tests
- [ ] Q12: No additional features

### Step 4.2: Pre-Commit Validation Protocol
**Reference**: rules.txt lines 73-166

**MANDATORY STEPS (100% pass required):**

**4.2.1: Run All Tests**
- [ ] Execute: `python tests/run_all_tests.py`
- [ ] Verify: 100% pass rate (NOT 99%, NOT "mostly passing" - 100%)
- [ ] If ANY test fails: STOP, fix the failure, re-run all tests
- [ ] Document test results in code changes file

**4.2.2: Check Test Coverage**
- [ ] Execute: `pytest --cov=league_helper.trade_simulator_mode.TradeSimulatorModeManager --cov-report=term-missing tests/league_helper/trade_simulator_mode/`
- [ ] Verify: >80% coverage for new methods
- [ ] If below 80%: Add more tests, re-run
- [ ] Document coverage percentage in code changes file

**4.2.3: Review Changes**
- [ ] Execute: `git status`
- [ ] Execute: `git diff`
- [ ] Review EVERY changed file
- [ ] Verify no unintended changes
- [ ] Verify no debug code left behind (print statements, commented code)
- [ ] Verify no placeholder TODOs in code
- [ ] Verify all imports are used

**4.2.4: Manual Feature Testing**
- [ ] Run application: `python run_simulation.py` (or correct entry point)
- [ ] Navigate: Main Menu → Trade Simulator → Manual Trade Visualizer
- [ ] Test scenario 1: Complete successful trade, save to file
- [ ] Test scenario 2: Type 'exit' at player selection
- [ ] Test scenario 3: Enter invalid input (out of range)
- [ ] Test scenario 4: Enter invalid input (letters)
- [ ] Test scenario 5: Decline save to file
- [ ] Verify all scenarios work as expected
- [ ] Document manual test results in code changes file

**4.2.5: Code Quality Checks**
- [ ] Verify all methods have docstrings
- [ ] Verify all docstrings are accurate and complete
- [ ] Verify type hints on all method signatures
- [ ] Verify consistent code style (indentation, spacing)
- [ ] Verify no dead code or unused imports
- [ ] Run linter if available: `pylint league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`

### Step 4.3: Completion Tasks

**4.3.1: Finalize Documentation**
- [ ] Review code changes documentation for completeness
- [ ] Add "Implementation Complete" section with summary
- [ ] Add verification results (all requirements ✅)
- [ ] Add test results (100% pass, X% coverage)
- [ ] Add manual test results summary

**4.3.2: File Organization**
- [ ] Create `updates/done/` directory if it doesn't exist
- [ ] Move `updates/manual_trade_visualizer.txt` to `updates/done/`
- [ ] Move `updates/manual_trade_visualizer_code_changes.md` to `updates/done/`
- [ ] Delete `updates/manual_trade_visualizer_questions.md`
- [ ] Delete `updates/todo-files/manual_trade_visualizer_todo.md` (this file)

**4.3.3: Git Commit**
- [ ] Stage all changes: `git add` (relevant files only)
- [ ] Verify staged changes: `git diff --staged`
- [ ] Commit with descriptive message (following project standards):
  ```
  Implement manual trade visualizer feature

  - Add manual trade mode to Trade Simulator
  - Allow users to manually select players for trade analysis
  - Display trade impact with score improvements
  - Save results to timestamped file
  - Include comprehensive unit and integration tests
  ```
- [ ] NO "Generated with Claude Code" footer (per CLAUDE.md)
- [ ] NO emojis in commit message

---

## Notes
- All phases must leave repo in testable, functional state
- Run `python tests/run_all_tests.py` after each phase completion
- Update this file incrementally as work progresses
- 100% test pass rate required before moving between phases
- REQUIREMENT VERIFICATION PROTOCOL is mandatory before marking complete
