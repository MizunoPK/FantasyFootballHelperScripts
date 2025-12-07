# Modify Player Data Modes - TODO

**Objective**: Implement 4 player data modification modes with fuzzy search functionality

**Status**: Not Started

**Progress Tracking**: Update this file as each task is completed to maintain session continuity

---

## Investigation Summary

### Critical Issues Found and Resolved:

**ISSUE 1: interactive_search() Method Signature (Found during re-investigation)**
- **Problem**: Initial TODO suggested passing pre-filtered list to interactive_search()
- **Root Cause**: Misunderstood the old code pattern - it searches from self.players with drafted_filter
- **Solution**: Changed interactive_search() to take drafted_filter parameter instead of pre-filtered list
- **Reference**: Old code line 109 uses `search_players_by_name(search_term, drafted_filter=0)`
- **Impact**: All Phase 3 mode implementations updated to use correct pattern

**ISSUE 2: Drop Player Mode Filtering (Found during re-investigation)**
- **Problem**: search_players_by_name() can't handle "drafted != 0" (only supports 0, 1, 2, or None)
- **Root Cause**: Old code line 179 manually filters `[p for p in self.players if p.drafted != 0]`
- **Solution**: Added search_players_by_name_not_available() helper method and not_available parameter
- **Reference**: Old drop player code manually filters before searching
- **Impact**: Phase 2 needs additional helper method, Drop Player mode uses not_available=True

### Key Findings:
1. **FantasyPlayer.__str__() location**: `utils/FantasyPlayer.py` line 351-360
   - Current format: `{name} ({team} {position}) - {score:.1f} pts {injury_status} [Bye={bye_week}] [{drafted_status}]`
   - Need to append " [LOCKED]" at end when player.locked == 1
   - locked attribute already exists (line 91) and is properly handled by from_dict() (line 157)

2. **PlayerSearch reference**: `old_structure/draft_helper/core/player_search.py`
   - search_players_by_name() method implements fuzzy matching (lines 35-87)
   - search_and_mark_player_interactive() shows continuous search pattern (lines 89-157)
   - search_and_drop_player_interactive() shows drop workflow (lines 159-243)
   - Key pattern: while True loop, display matches with numbers, handle exit via empty input or 'exit'

3. **PlayerManager.update_players_file()**: `league_helper/util/PlayerManager.py` line 269-312
   - Saves all players to CSV with proper field ordering
   - Sorts by drafted status before saving
   - No parameters needed, just call directly

4. **user_input.show_list_selection()**: `league_helper/util/user_input.py` line 4-20
   - Used for menu display throughout league_helper
   - Pattern: show_list_selection(title, options_list, quit_string)
   - Returns integer choice (1-based)

5. **Existing mode manager pattern**: `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
   - __init__ takes (config, player_manager, team_data_manager)
   - start_interactive_mode() is entry point, receives updated managers
   - set_managers() helper to update manager references
   - Calls player_manager.update_players_file() after modifications

6. **Test structure**:
   - Only 15 test files total in entire tests/ directory
   - Tests in `tests/league_helper/util/` (e.g., test_PlayerManager_scoring.py)
   - No tests/utils/ directory exists
   - Need to create tests/league_helper/modify_player_data_mode/ directory

7. **Requirements from original file**:
   - Line 2: 4 options upon entering section ✓
   - Line 3: Fuzzy search from old_structure ✓
   - Line 4: Mark as Drafted (drafted=0 → drafted=1) ✓
   - Line 5: Mark as Rostered (drafted=0 → drafted=2) ✓ (typo confirmed in questions)
   - Line 6: Drop Player (drafted≠0 → drafted=0) ✓
   - Line 7: Lock Player (toggle locked, show [LOCKED]) ✓
   - Line 8: Update via PlayerManager, return to menu ✓

---

## Phase 1: Update FantasyPlayer __str__ Method
**Goal**: Add [LOCKED] indicator to player display string

**File**: `utils/FantasyPlayer.py` line 351-360

### Phase 1.1: Modify FantasyPlayer.__str__()
- [ ] Read current __str__ implementation (line 351-360)
- [ ] Update __str__ method to append " [LOCKED]" at end if player.locked == 1
  - Current ending: `[{drafted_status}]`
  - New ending: `[{drafted_status}]` or `[{drafted_status}] [LOCKED]`
- [ ] Verify the locked attribute is accessed correctly (self.locked)

### Phase 1.2: Test FantasyPlayer Changes
- [ ] Note: No tests/utils/ directory exists, tests for FantasyPlayer need to be created
- [ ] Create `tests/utils/` directory
- [ ] Create `tests/utils/__init__.py`
- [ ] Create `tests/utils/test_FantasyPlayer.py`
- [ ] Write test: `test_str_shows_locked_indicator_when_locked_is_one()`
  - Create FantasyPlayer with locked=1
  - Assert " [LOCKED]" appears at end of str(player)
- [ ] Write test: `test_str_no_locked_indicator_when_locked_is_zero()`
  - Create FantasyPlayer with locked=0
  - Assert " [LOCKED]" does NOT appear in str(player)
- [ ] Run unit tests: `python tests/run_all_tests.py`
- [ ] Fix any failing tests
- [ ] **MANDATORY**: Achieve 100% test pass rate before proceeding

### Phase 1.3: Validate and Commit
- [ ] Run `python tests/run_all_tests.py` (100% pass required)
- [ ] Manual testing: Create a test player with locked=1, print str(player)
- [ ] Git status and diff review
- [ ] Commit changes with message: "Add LOCKED indicator to FantasyPlayer display"
- [ ] Update code changes documentation

---

## Phase 2: Create PlayerSearch Utility
**Goal**: Extract and adapt fuzzy search functionality from old_structure

**Reference**: `old_structure/draft_helper/core/player_search.py`

### Phase 2.1: Create PlayerSearch Class Structure
- [ ] Create `league_helper/util/player_search.py`
- [ ] Import requirements:
  - `from typing import List, Optional, Callable`
  - `from pathlib import Path`
  - `import sys`
  - Add parent path for imports
  - `from utils.FantasyPlayer import FantasyPlayer`
  - `from utils.LoggingManager import get_logger`
- [ ] Create PlayerSearch class with __init__(players: List[FantasyPlayer], logger=None)
- [ ] Store players list and logger as instance variables

### Phase 2.2: Implement Core Search Method
- [ ] Copy search_players_by_name() from old player_search.py (lines 35-87)
- [ ] Adapt for league_helper imports (change shared_files.FantasyPlayer to utils.FantasyPlayer)
- [ ] Method signature: `search_players_by_name(search_term: str, drafted_filter: Optional[int] = None, exact_match: bool = False) -> List[FantasyPlayer]`
- [ ] Implement fuzzy matching logic:
  - Filter by drafted_filter if provided (0, 1, 2, or None for all)
  - Case-insensitive search
  - Match if search_term in name OR search_term in any word OR any word starts with search_term
- [ ] Return list of matching players

### Phase 2.3: Implement Interactive Search Method
- [ ] **CRITICAL FIX**: Method should take drafted_filter parameter, NOT pre-filtered list
- [ ] Create method: `interactive_search(drafted_filter: Optional[int] = None, prompt: str = "Enter player name", not_available: bool = False) -> Optional[FantasyPlayer]`
- [ ] Method searches from self.players using drafted_filter parameter OR not_available flag
- [ ] Implement continuous search loop pattern (reference line 99-157 in old code):
  ```python
  def interactive_search(self, drafted_filter: Optional[int] = None,
                        prompt: str = "Enter player name",
                        not_available: bool = False) -> Optional[FantasyPlayer]:
      """
      Interactive player search with continuous search loop.

      Args:
          drafted_filter: Filter by drafted status (0, 1, 2, or None for all)
          prompt: Prompt message for user input
          not_available: If True, search only drafted players (drafted != 0)

      Returns:
          Selected player or None if user exits
      """
      while True:
          search_term = input(f"\n{prompt} (or press Enter to return): ").strip()

          # Check if user wants to exit
          if not search_term or search_term.lower() == 'exit':
              print("Returning to Main Menu...")
              return None

          try:
              # Use appropriate search method
              if not_available:
                  matches = self.search_players_by_name_not_available(search_term)
              else:
                  matches = self.search_players_by_name(search_term, drafted_filter=drafted_filter)

              if not matches:
                  print(f"No players found matching '{search_term}'. Try again or type 'exit' to return.")
                  continue

              # Display matches with numbers
              print(f"\nFound {len(matches)} matching player(s):")
              for i, player in enumerate(matches, start=1):
                  print(f"{i}. {player}")  # Uses FantasyPlayer.__str__() which now shows [LOCKED]

              print(f"{len(matches) + 1}. Search again")

              # Get user choice
              try:
                  choice = int(input(f"Enter your choice (1-{len(matches) + 1}): ").strip())

                  if 1 <= choice <= len(matches):
                      selected_player = matches[choice - 1]
                      if self.logger:
                          self.logger.info(f"Selected player: {selected_player.name}")
                      return selected_player
                  elif choice == len(matches) + 1:
                      # Search again
                      continue
                  else:
                      print("Invalid choice. Please try again.")
                      continue

              except ValueError:
                  print("Invalid input. Please enter a number.")
                  continue
          except Exception as e:
              print(f"Error during search: {e}")
              if self.logger:
                  self.logger.error(f"Error during player search: {e}")
              return None
  ```
- [ ] Ensure method handles both drafted_filter and not_available parameters correctly
- [ ] Add logging for search attempts and selections
- [ ] Return selected player or None if user exits

### Phase 2.4: Add Helper Method for "Not Equal" Filtering
- [ ] **ISSUE**: search_players_by_name() can't handle drafted != 0 (only supports 0, 1, 2, or None)
- [ ] **SOLUTION**: Add helper method for Drop Player mode:
  ```python
  def search_players_by_name_not_available(self, search_term: str) -> List[FantasyPlayer]:
      """Search for players that are drafted (drafted != 0)."""
      # Filter to only drafted players (1 or 2)
      candidate_players = [p for p in self.players if p.drafted != 0]

      if not search_term:
          return []

      matches = []
      search_lower = search_term.lower()

      for player in candidate_players:
          name_lower = player.name.lower()
          name_words = name_lower.split()

          # Fuzzy matching
          if (search_lower in name_lower or
              any(search_lower in word or word.startswith(search_lower)
                  for word in name_words)):
              matches.append(player)

      return matches
  ```
- [ ] Update interactive_search() signature to: `interactive_search(drafted_filter: Optional[int], prompt: str, not_available: bool = False)`
- [ ] When not_available=True, use search_players_by_name_not_available() instead

### Phase 2.5: Simplify for League Helper Use
- [ ] DO NOT copy search_and_mark_player_interactive() or search_and_drop_player_interactive()
- [ ] The interactive_search() method is generic enough for all 4 modes
- [ ] Each mode passes appropriate parameters to interactive_search():
  - Mark as Drafted: drafted_filter=0 (available players)
  - Mark as Rostered: drafted_filter=0 (available players)
  - Drop Player: not_available=True (drafted != 0)
  - Lock Player: drafted_filter=None (all players)

### Phase 2.6: Test PlayerSearch Utility
- [ ] Create `tests/league_helper/util/test_player_search.py`
- [ ] Test fuzzy matching with search_players_by_name():
  - Test exact match: "Patrick Mahomes" finds Patrick Mahomes
  - Test partial match: "Mahomes" finds Patrick Mahomes
  - Test first name: "Patrick" finds all Patricks
  - Test case insensitive: "mahomes" finds Patrick Mahomes
  - Test word start: "Mah" finds Patrick Mahomes
- [ ] Test drafted status filtering:
  - drafted_filter=0: only returns players with drafted=0
  - drafted_filter=1: only returns players with drafted=1
  - drafted_filter=2: only returns players with drafted=2
  - drafted_filter=None: returns all players matching name
- [ ] Test search_players_by_name_not_available():
  - Only returns players with drafted != 0
  - Excludes players with drafted == 0
  - Fuzzy matching works correctly
- [ ] Test empty search results:
  - Search for "ZZZ999" returns empty list
- [ ] Test interactive_search():
  - Mock input/output to simulate user interaction
  - Test successful selection returns player
  - Test empty input returns None
  - Test 'exit' returns None
  - Test "Search again" option continues loop
  - Test with drafted_filter=0, 1, 2, None
  - Test with not_available=True
- [ ] Run unit tests: `python tests/run_all_tests.py`
- [ ] Fix any failing tests
- [ ] **MANDATORY**: Achieve 100% test pass rate before proceeding

### Phase 2.7: Validate and Commit
- [ ] Run `python tests/run_all_tests.py` (100% pass required)
- [ ] Git status and diff review
- [ ] Commit changes with message: "Add PlayerSearch utility for fuzzy player search"
- [ ] Update code changes documentation

---

## Phase 3: Create ModifyPlayerDataModeManager
**Goal**: Implement main mode manager with 4 sub-modes

**Pattern Reference**: `league_helper/add_to_roster_mode/AddToRosterModeManager.py`

### Phase 3.1: Create Manager Structure
- [ ] Create directory: `league_helper/modify_player_data_mode/`
- [ ] Create `league_helper/modify_player_data_mode/__init__.py` (empty file)
- [ ] Create `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py`
- [ ] Import requirements:
  ```python
  from pathlib import Path
  from typing import Optional
  import sys
  sys.path.append(str(Path(__file__).parent.parent))
  from util.PlayerManager import PlayerManager
  from util.player_search import PlayerSearch
  sys.path.append(str(Path(__file__).parent.parent.parent))
  from utils.LoggingManager import get_logger
  from utils.FantasyPlayer import FantasyPlayer
  ```
- [ ] Create class: `ModifyPlayerDataModeManager`
- [ ] Implement `__init__(self, player_manager: PlayerManager)`
  - Store player_manager reference
  - Initialize logger with get_logger()
  - Log: "Initializing Modify Player Data Mode Manager"
- [ ] Implement `set_managers(self, player_manager: PlayerManager)` helper
  - Update player_manager reference (pattern from AddToRosterModeManager)

### Phase 3.2: Implement Main Menu and Interactive Loop
- [ ] Implement `start_interactive_mode(self, player_manager: PlayerManager)`
- [ ] Call set_managers() to update player_manager reference
- [ ] Log: "Entering Modify Player Data interactive mode"
- [ ] Create menu loop:
  ```python
  while True:
      from util.user_input import show_list_selection
      choice = show_list_selection(
          "MODIFY PLAYER DATA",
          ["Mark Player as Drafted", "Mark Player as Rostered", "Drop Player", "Lock Player"],
          "Return to Main Menu"
      )
      if choice == 1:
          self._mark_player_as_drafted()
      elif choice == 2:
          self._mark_player_as_rostered()
      elif choice == 3:
          self._drop_player()
      elif choice == 4:
          self._lock_player()
      elif choice == 5:
          print("Returning to Main Menu...")
          break
  ```
- [ ] Add error handling with try/except around menu operations
- [ ] Log menu selections

### Phase 3.3: Implement Mark Player as Drafted Mode
- [ ] Create `_mark_player_as_drafted(self)` method
- [ ] Log: "Starting Mark Player as Drafted mode"
- [ ] Create PlayerSearch instance: `searcher = PlayerSearch(self.player_manager.players, self.logger)`
- [ ] Call: `selected_player = searcher.interactive_search(drafted_filter=0, prompt="Enter player name to mark as drafted")`
  - **NOTE**: drafted_filter=0 searches only available players (drafted==0)
- [ ] If selected_player is None (user exited): return to menu
- [ ] Set player status: `selected_player.drafted = 1`
- [ ] Save changes: `self.player_manager.update_players_file()`
- [ ] Print: `f"✓ Marked {selected_player.name} as drafted by another team!"`
- [ ] Log: `f"Player {selected_player.name} marked as drafted=1"`
- [ ] Return to menu (continuous mode)

### Phase 3.4: Implement Mark Player as Rostered Mode
- [ ] Create `_mark_player_as_rostered(self)` method
- [ ] Log: "Starting Mark Player as Rostered mode"
- [ ] Create PlayerSearch instance: `searcher = PlayerSearch(self.player_manager.players, self.logger)`
- [ ] Call: `selected_player = searcher.interactive_search(drafted_filter=0, prompt="Enter player name to add to your roster")`
  - **NOTE**: drafted_filter=0 searches only available players (drafted==0)
- [ ] If selected_player is None: return
- [ ] Set player status: `selected_player.drafted = 2`
- [ ] Save changes: `self.player_manager.update_players_file()`
- [ ] Print: `f"✓ Added {selected_player.name} to your roster!"`
- [ ] Log: `f"Player {selected_player.name} marked as drafted=2 (rostered)"`
- [ ] Return to menu

### Phase 3.5: Implement Drop Player Mode
- [ ] Create `_drop_player(self)` method
- [ ] Log: "Starting Drop Player mode"
- [ ] Create PlayerSearch instance: `searcher = PlayerSearch(self.player_manager.players, self.logger)`
- [ ] Call: `selected_player = searcher.interactive_search(drafted_filter=None, prompt="Enter player name to drop", not_available=True)`
  - **NOTE**: not_available=True uses search_players_by_name_not_available() which filters drafted != 0
- [ ] If selected_player is None: return
- [ ] Store old status for message: `old_status = "your roster" if selected_player.drafted == 2 else "drafted players"`
- [ ] Set player status: `selected_player.drafted = 0`
- [ ] Save changes: `self.player_manager.update_players_file()`
- [ ] Print: `f"✓ Dropped {selected_player.name} from {old_status}!"`
- [ ] Log: `f"Player {selected_player.name} dropped (set drafted=0)"`
- [ ] Return to menu

### Phase 3.6: Implement Lock Player Mode
- [ ] Create `_lock_player(self)` method
- [ ] Log: "Starting Lock Player mode"
- [ ] Create PlayerSearch instance: `searcher = PlayerSearch(self.player_manager.players, self.logger)`
- [ ] Call: `selected_player = searcher.interactive_search(drafted_filter=None, prompt="Enter player name to lock/unlock")`
  - **NOTE**: drafted_filter=None searches ALL players regardless of drafted status
  - **NOTE**: [LOCKED] indicator automatically shows via FantasyPlayer.__str__()
- [ ] If selected_player is None: return
- [ ] Store old state: `was_locked = selected_player.locked == 1`
- [ ] Toggle locked state: `selected_player.locked = 0 if was_locked else 1`
- [ ] Save changes: `self.player_manager.update_players_file()`
- [ ] Print appropriate message:
  - If now locked: `f"🔒 Locked {selected_player.name}!"`
  - If now unlocked: `f"🔓 Unlocked {selected_player.name}!"`
- [ ] Log: `f"Player {selected_player.name} lock toggled (locked={selected_player.locked})"`
- [ ] Return to menu

### Phase 3.7: Test ModifyPlayerDataModeManager
- [ ] Create `tests/league_helper/modify_player_data_mode/` directory
- [ ] Create `tests/league_helper/modify_player_data_mode/__init__.py` (empty file)
- [ ] Create `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py`
- [ ] Import requirements:
  ```python
  import pytest
  from unittest.mock import Mock, patch, MagicMock
  from league_helper.modify_player_data_mode.ModifyPlayerDataModeManager import ModifyPlayerDataModeManager
  from utils.FantasyPlayer import FantasyPlayer
  ```
- [ ] Create test fixtures:
  - `@pytest.fixture` for mock_player_manager with mock players list
  - `@pytest.fixture` for sample FantasyPlayer objects (available, drafted, rostered, locked)
- [ ] Test Mark as Drafted mode:
  - `test_mark_player_as_drafted_sets_drafted_to_one()`
  - Mock PlayerSearch.interactive_search() to return available player
  - Call _mark_player_as_drafted()
  - Assert player.drafted == 1
  - Assert update_players_file() was called
- [ ] Test Mark as Rostered mode:
  - `test_mark_player_as_rostered_sets_drafted_to_two()`
  - Similar pattern, assert player.drafted == 2
- [ ] Test Drop Player mode:
  - `test_drop_player_sets_drafted_to_zero()`
  - Mock with drafted player (drafted=1 or 2)
  - Assert player.drafted == 0 after drop
- [ ] Test Lock Player mode:
  - `test_lock_player_toggles_locked_from_zero_to_one()`
  - `test_lock_player_toggles_locked_from_one_to_zero()`
  - Test both directions of toggle
- [ ] Test user exit scenarios:
  - `test_mark_as_drafted_handles_user_exit_gracefully()`
  - Mock interactive_search() to return None
  - Assert no exception raised, no file update called
- [ ] Test menu navigation:
  - `test_start_interactive_mode_calls_correct_method_for_each_choice()`
  - Mock show_list_selection() to return each choice (1-5)
  - Assert appropriate method called for each
- [ ] Run unit tests: `python tests/run_all_tests.py`
- [ ] Fix any failing tests
- [ ] **MANDATORY**: Achieve 100% test pass rate before proceeding

### Phase 3.8: Validate and Commit
- [ ] Run `python tests/run_all_tests.py` (100% pass required)
- [ ] Git status and diff review
- [ ] Commit changes with message: "Implement ModifyPlayerDataModeManager with 4 modes"
- [ ] Update code changes documentation

---

## Phase 4: Integrate with LeagueHelperManager
**Goal**: Connect Modify Player Data mode to main menu

**File**: `league_helper/LeagueHelperManager.py`
**Note**: Line 135 already calls run_modify_player_data_mode() but method doesn't exist yet

### Phase 4.1: Add Manager Initialization
- [ ] Read `league_helper/LeagueHelperManager.py` lines 89-94 (where managers are initialized)
- [ ] Add import at top of file (around line 27):
  ```python
  from modify_player_data_mode.ModifyPlayerDataModeManager import ModifyPlayerDataModeManager
  ```
- [ ] Add initialization in __init__ method (around line 93, after trade_simulator_mode_manager):
  ```python
  self.modify_player_data_mode_manager = ModifyPlayerDataModeManager(self.player_manager)
  self.logger.info("Modify Player Data mode manager initialized successfully")
  ```
- [ ] Update docstring (line 50-55) to include modify_player_data_mode_manager attribute

### Phase 4.2: Implement run_modify_player_data_mode()
- [ ] Note: Method is already called at line 135 but doesn't exist yet
- [ ] Add method after _run_trade_simulator_mode() (around line 172):
  ```python
  def run_modify_player_data_mode(self):
      """
      Delegate to Modify Player Data mode manager.

      Passes current player_manager instance to the mode manager
      to ensure it has the latest data.
      """
      self.modify_player_data_mode_manager.start_interactive_mode(self.player_manager)
  ```
- [ ] Add logging before calling manager:
  ```python
  self.logger.info("Starting Modify Player Data mode")
  ```

### Phase 4.3: Test LeagueHelperManager Integration
- [ ] Find or create test file for LeagueHelperManager
- [ ] Test that modify_player_data_mode_manager is properly initialized
- [ ] Test that run_modify_player_data_mode() calls the manager correctly
- [ ] Test menu option 4 routes to modify player data mode
- [ ] Run unit tests: `python tests/run_all_tests.py`
- [ ] Fix any failing tests
- [ ] **MANDATORY**: Achieve 100% test pass rate before proceeding

### Phase 4.4: Validate and Commit
- [ ] Run `python tests/run_all_tests.py` (100% pass required)
- [ ] Git status and diff review
- [ ] Commit changes with message: "Integrate Modify Player Data mode with LeagueHelperManager"
- [ ] Update code changes documentation

---

## Phase 5: Manual Integration Testing
**Goal**: Test complete workflow end-to-end

### Phase 5.1: Test Each Mode Manually
- [ ] Run `python run_league_helper.py`
- [ ] Test Mark Player as Drafted:
  - Select option 4 (Modify Player Data)
  - Select option 1 (Mark as Drafted)
  - Search for available player
  - Verify drafted status changes to 1
  - Verify CSV file updated
- [ ] Test Mark Player as Rostered:
  - Search for available player
  - Verify drafted status changes to 2
  - Verify CSV file updated
- [ ] Test Drop Player:
  - Search for drafted/rostered player
  - Verify drafted status changes to 0
  - Verify CSV file updated
- [ ] Test Lock Player:
  - Search for any player
  - Verify [LOCKED] indicator appears in search results
  - Verify locked status toggles
  - Verify CSV file updated
- [ ] Test continuous search workflow in each mode
- [ ] Test user exit (empty input, 'exit' command)
- [ ] Test invalid searches (no matches)
- [ ] Test menu navigation (all options)

### Phase 5.2: Test Edge Cases
- [ ] Test searching for locked players shows [LOCKED] indicator
- [ ] Test marking already drafted player as drafted (should not appear in search)
- [ ] Test dropping already dropped player (should not appear in search)
- [ ] Test fuzzy search with partial names
- [ ] Test fuzzy search with special characters
- [ ] Test CSV persistence after each operation

### Phase 5.3: Document Manual Testing
- [ ] Create testing notes in code changes documentation
- [ ] Document any issues found and fixed
- [ ] Verify all functionality works as expected

---

## Phase 6: Final Validation
**Goal**: Ensure all requirements met and system fully functional

### Phase 6.1: Run Complete Test Suite
- [ ] Run `python tests/run_all_tests.py` (100% pass required)
- [ ] Verify all 236+ tests pass
- [ ] Fix any failing tests
- [ ] Re-run until 100% pass rate achieved
- [ ] **MANDATORY**: Cannot proceed without 100% pass rate

### Phase 6.2: Requirement Verification Protocol
- [ ] Re-read original `updates/modify_data_modes.txt`
- [ ] Create checklist of ALL requirements:
  - [ ] 4-option menu upon entering section
  - [ ] Mark Player as Drafted mode (drafted=0 → drafted=1)
  - [ ] Mark Player as Rostered mode (drafted=0 → drafted=2)
  - [ ] Drop Player mode (drafted≠0 → drafted=0)
  - [ ] Lock Player mode (toggle locked 0↔1)
  - [ ] Fuzzy search functionality
  - [ ] [LOCKED] indicator in player display
  - [ ] PlayerManager.update_players_file() called after changes
  - [ ] Return to Modify Player Data menu after each operation
- [ ] Verify each requirement with code evidence (file paths, line numbers)
- [ ] Mark each as ✅ DONE or ❌ MISSING
- [ ] If ANY requirement is ❌ MISSING: STOP, implement it, re-verify

### Phase 6.3: Update Documentation
- [ ] Review and finalize `updates/modify_data_modes_code_changes.md`
- [ ] Ensure all changes documented with:
  - File paths and line numbers
  - Before/after code snippets
  - Rationale for changes
  - Impact analysis
- [ ] Add "Requirements Verification" section to code changes file
- [ ] List all requirements with implementation evidence

### Phase 6.4: Update Project Documentation
- [ ] Update README.md if needed (add Modify Player Data mode documentation)
- [ ] Update CLAUDE.md if workflow changed
- [ ] Update any module-specific documentation

### Phase 6.5: Final Commit
- [ ] Run `python tests/run_all_tests.py` one final time (100% pass required)
- [ ] Git status and diff review
- [ ] Commit any documentation updates
- [ ] Commit message: "Complete Modify Player Data modes implementation"

---

## Phase 7: Objective Completion
**Goal**: Finalize and archive objective

### Phase 7.1: Finalize Documentation
- [ ] Review `updates/modify_data_modes_code_changes.md` for completeness
- [ ] Ensure all code changes documented
- [ ] Ensure requirements verification section complete
- [ ] Ensure manual testing notes included

### Phase 7.2: Move Files to Done
- [ ] Move `updates/modify_data_modes.txt` to `updates/done/`
- [ ] Move `updates/modify_data_modes_code_changes.md` to `updates/done/`
- [ ] Delete `updates/modify_data_modes_questions.md`
- [ ] Delete this TODO file: `updates/todo-files/modify_data_modes_todo.md`

### Phase 7.3: Notify User
- [ ] Inform user that objective is complete
- [ ] Provide summary of what was implemented
- [ ] Mention test pass rate (should be 100%)
- [ ] Mention files moved to done folder

---

## Notes
- Each phase must achieve 100% test pass rate before proceeding to next phase
- Update this TODO file after completing each task
- Document all changes incrementally in code changes file
- Follow pre-commit validation protocol at end of each phase
- No exceptions to testing requirements
- Manual testing is required in Phase 5 before claiming completion

## Development Rules Reminders
1. Questions answered → TODO created → Code changes doc created → Implementation begins
2. Update code changes doc incrementally as work progresses
3. Run ALL unit tests before each commit (100% pass required)
4. Add new unit tests to cover new functionality
5. Follow requirement verification protocol before marking complete
6. No partial completion - 100% of requirements must be met

---

## Investigation Completeness Check

This TODO file has been updated with comprehensive investigation findings:

✅ **FantasyPlayer.__str__()**: Exact location (line 351-360), current format understood, locked attribute confirmed
✅ **PlayerSearch implementation**: Reference file identified, key methods documented with line numbers
✅ **PlayerManager.update_players_file()**: Location confirmed (line 269-312), usage pattern understood
✅ **user_input.show_list_selection()**: Usage pattern documented for menu display
✅ **Mode manager pattern**: AddToRosterModeManager analyzed as reference, patterns extracted
✅ **Test structure**: Directory layout understood, test count confirmed (15 files)
✅ **All requirements mapped**: Every line from original update file accounted for in TODO
✅ **Integration point identified**: Line 135 in LeagueHelperManager already calls method
✅ **Code patterns**: Interactive search loop, continuous mode, filter patterns all documented
✅ **Dependencies**: All imports and class relationships identified

**Code snippets provided for**:
- Complete interactive_search() method implementation
- Menu loop structure with show_list_selection()
- Each of the 4 mode method implementations
- Test fixture patterns and test method structure
- Integration code for LeagueHelperManager

**Files to create**:
1. `utils/FantasyPlayer.py` - MODIFY __str__() line 351-360
2. `tests/utils/` - CREATE directory
3. `tests/utils/__init__.py` - CREATE empty file
4. `tests/utils/test_FantasyPlayer.py` - CREATE with 2 tests
5. `league_helper/util/player_search.py` - CREATE new file
6. `tests/league_helper/util/test_player_search.py` - CREATE new file
7. `league_helper/modify_player_data_mode/` - CREATE directory
8. `league_helper/modify_player_data_mode/__init__.py` - CREATE empty file
9. `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py` - CREATE new file
10. `tests/league_helper/modify_player_data_mode/` - CREATE directory
11. `tests/league_helper/modify_player_data_mode/__init__.py` - CREATE empty file
12. `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py` - CREATE new file
13. `league_helper/LeagueHelperManager.py` - MODIFY (add import, init manager, implement method)

**Total**: 10 new files, 3 modified files

---

## Re-Investigation Findings (2025-10-16)

**Prompted by**: User request to re-read all files and ensure ALL requirements met

**Additional investigation performed**:
1. ✅ Re-read original update file line-by-line
2. ✅ Re-read questions file to verify all answers addressed
3. ✅ Re-read existing TODO to find gaps
4. ✅ Examined old PlayerSearch code (line 99-243) for exact implementation patterns
5. ✅ Verified method signatures and parameter passing patterns

**Critical design flaws found and fixed**:
1. **interactive_search() signature** - Was going to pass pre-filtered list, but should use drafted_filter parameter
   - **Evidence**: Line 109 in old code: `matches = self.search_players_by_name(search_term, drafted_filter=0)`
   - **Fix**: Changed signature from `interactive_search(players, prompt)` to `interactive_search(drafted_filter, prompt, not_available)`
   - **Files updated**: Phase 2.3, Phase 3.3-3.6

2. **Drop Player filtering** - search_players_by_name() can't handle "!=" comparisons
   - **Evidence**: Line 179 in old code manually filters: `drafted_players = [p for p in self.players if p.drafted != 0]`
   - **Fix**: Added search_players_by_name_not_available() helper method with not_available parameter
   - **Files updated**: Phase 2.4, Phase 2.6 tests, Phase 3.5

**Verification that all requirements are met**:
- ✅ Line 2: 4 options menu - Phase 3.2 implements with show_list_selection()
- ✅ Line 3: Fuzzy search from old_structure - Phase 2 extracts and adapts player_search.py
- ✅ Line 4: Mark as Drafted (0→1) - Phase 3.3 implements with drafted_filter=0
- ✅ Line 5: Mark as Rostered (0→2) - Phase 3.4 implements with drafted_filter=0 (typo corrected in questions)
- ✅ Line 6: Drop Player (≠0→0) - Phase 3.5 implements with not_available=True
- ✅ Line 7: Lock Player (toggle, show [LOCKED]) - Phase 3.6 implements with drafted_filter=None, Phase 1 adds [LOCKED] to __str__()
- ✅ Line 8: Update via PlayerManager, return to menu - All Phase 3 modes call update_players_file() and return to menu

**No additional gaps found**. All requirements accounted for with detailed implementation instructions.

This TODO is now ready for systematic implementation with all necessary details provided and all design flaws corrected.
