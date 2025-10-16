# Modify Player Data Modes - Questions

## Requirements Clarifications

Based on `updates/modify_data_modes.txt`, I have the following questions:

### 1. Fuzzy Search Implementation
- **Q:** Should the fuzzy search utility be extracted as a standalone util file that can be imported by all 4 modes?
- **Assumption:** Yes - create `league_helper/util/player_search.py` with a `PlayerSearch` class that can be reused
Answer: Yes

### 2. Mode Structure
- **Q:** Should each mode (Mark as Drafted, Mark as Rostered, Drop Player, Lock Player) be its own manager class in separate files/folders like the existing modes (add_to_roster_mode, starter_helper_mode)?
- **Assumption:** No - These are simpler operations, so create a single `ModifyPlayerDataModeManager` class in `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py`
Answer: Have a single class for now

### 3. Mark Player as Drafted vs Mark Player as Rostered
- **Q:** Line 5 says "Mark Player as Drafted mode will allow the user to search from a list of drafted=0 players, and anyone selected will have their drafted status set to 2" - is this a typo? Should "Mark Player as Rostered" set drafted=2 instead?
- **Assumption:** Yes - Line 4 (Mark as Drafted) sets drafted=1, Line 5 (Mark as Rostered) sets drafted=2
Yes you are correct here

### 4. Search Functionality
- **Q:** Should the search allow continuous searching and modification (like the old player_search.py does), or should it exit after one modification?
- **Assumption:** Continuous - Allow user to search and modify multiple players, then return to the Modify Player Data menu when they press Enter or type 'exit'
Answer: Continuous

### 5. Display Format
- **Q:** What information should be displayed for each matching player in search results?
- **Assumption:** Follow format from old player_search.py: "Name (Position, Team) - Status" where status shows drafted/rostered state and locked indicator
Answer: print the FantasyPlayer object

### 6. Lock Player Display
- **Q:** Should "[LOCKED]" appear at the end of the player string (after position/team) or in a different location?
- **Assumption:** Append to the end of the player display string, similar to how injury status might be shown
Update the FantasyPlayer's __str__ function to append the locked label to the end if they are locked

### 7. Menu Flow
- **Q:** After selecting a mode from the 4-option menu, should the user be able to go back to the Modify Player Data menu without making a change?
- **Assumption:** Yes - Allow user to press Enter or type 'exit' at the search prompt to return to menu
Answer: Yes do exactly this

### 8. Validation
- **Q:** Should there be any confirmation prompts before modifying player data?
- **Assumption:** No - The old player_search.py doesn't use confirmations, so modify immediately and show success message
Answer: No confirmation prompts

### 9. Integration with LeagueHelperManager
- **Q:** I see line 135 in LeagueHelperManager.py already calls `run_modify_player_data_mode()` but this method doesn't exist yet - should I implement this?
- **Assumption:** Yes - Implement `run_modify_player_data_mode()` in LeagueHelperManager that creates/calls the ModifyPlayerDataModeManager
Answer: Yes implement that

### 10. Testing
- **Q:** Should unit tests be created for all 4 modes?
- **Assumption:** Yes - Create `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py` with comprehensive test coverage
Answer: Yes comprehensive tests are required

## Current Understanding

Based on the requirements and existing code:

1. Create `league_helper/util/player_search.py` - Fuzzy search utility extracted from old_structure
2. Create `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py` - Main mode manager
3. Implement 4 sub-modes within the manager:
   - Mark Player as Drafted (drafted=0 → drafted=1)
   - Mark Player as Rostered (drafted=0 → drafted=2)
   - Drop Player (drafted≠0 → drafted=0)
   - Lock Player (locked=0 ↔ locked=1, show [LOCKED] indicator)
4. Add menu display method that shows 4 options
5. Each mode uses fuzzy search to find players, shows matches, allows selection, modifies data, saves via PlayerManager.update_players_file()
6. Return to Modify Player Data menu after each operation
7. Implement `run_modify_player_data_mode()` method in LeagueHelperManager
8. Create comprehensive unit tests

## Ready to Proceed?

If these assumptions are correct, I can proceed with creating the TODO file and implementing the feature.
