# Save Aggregate Scoring Results

## Objective

Add a new top-level menu mode to the League Helper application that saves calculated projected points for all players to JSON files in the historical_data folder structure, using the same scoring logic as the Starter Helper mode. Additionally, copy relevant data files from the main data folder into historical_data for archival purposes.

---

## High-Level Requirements

### 1. Menu Integration
- **Location:** Top-level menu (same level as "Draft Mode", "Roster Helper", etc.)
- **Label:** "Save Calculated Projected Points"
- **Behavior:** When selected, execute scoring and file operations, then return to main menu

### 2. Scoring Logic
- **Source:** Reuse exact scoring logic from StarterHelper mode
- **Weekly Scoring (week 1-17):**
  - Use weekly projected points for the current NFL week
  - Score all available players using the same method call and parameters as StarterHelper
- **Season-Long Scoring (week 0):**
  - Use compiled season-long projected points instead of weekly
  - Same scoring method but with season-long data

### 3. Output Files

**Weekly Output (weeks 1-17):**
```
data/historical_data/{SEASON}/{WEEK}/calculated_projected_points.json
```

**Season-Long Output (week 0):**
```
data/historical_data/{SEASON}/calculated_season_long_projected_points.json
```

**JSON Format:**
```json
{
    "player_id_1": calculated_score,
    "player_id_2": calculated_score,
    ...
}
```

### 4. File Copying to Historical Data
- **Purpose:** Archive the current state of all relevant data files
- **Source:** `data/` folder
- **Destination:** `data/historical_data/{SEASON}/{WEEK}/`
- **Files to Copy:** players.csv, players_projected.csv, game_data.csv, team_data/ folder
- **Behavior:** Copy files from data/ to historical_data/ with same filenames using shutil.copy2

---

## Dependency Map

### Module Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│ league_helper/LeagueHelperManager.py (entry point)             │
│     │                                                           │
│     ▼                                                           │
│ SaveCalculatedPointsManager (NEW)                              │
│     │                                                           │
│     ├──► PlayerManager (existing)                              │
│     │         └──► score_player() with weekly params           │
│     │         └──► players list (all available players)        │
│     │                                                           │
│     ├──► ConfigManager (existing)                              │
│     │         └──► current_nfl_week, nfl_season                │
│     │                                                           │
│     └──► File operations (NEW)                                 │
│               ├──► shutil.copy2() for files                    │
│               ├──► shutil.copytree() for team_data/ folder     │
│               └──► JSON output: calculated_projected_points.json│
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Entry: LeagueHelperManager menu selection
  ↓
SaveCalculatedPointsManager.execute()
  ↓
1. Get season/week from ConfigManager
  ↓
2. Calculate max_weekly_projection (if weekly mode)
  ↓
3. For each player in PlayerManager.players:
     score_player(use_weekly_projection=True/False, <params>)
  ↓
4. Build dict {player.id: score}
  ↓
5. Write JSON to historical_data/{SEASON}/{WEEK}/calculated_projected_points.json
  ↓
6. Copy files from data/ to historical_data/{SEASON}/{WEEK}/
     - players.csv
     - players_projected.csv
     - game_data.csv
     - team_data/ (folder)
  ↓
Output: JSON file + copied data files in historical_data
```

### Key Integration Points

| Component | Depends On | Used By | Notes |
|-----------|------------|---------|-------|
| SaveCalculatedPointsManager | PlayerManager | LeagueHelperManager | NEW - scores all players |
| SaveCalculatedPointsManager | ConfigManager | LeagueHelperManager | Uses current_nfl_week, nfl_season |
| Menu dispatch | show_list_selection | LeagueHelperManager | Add new option to menu list |

---

## Codebase Research Findings

### Menu System Pattern (from LeagueHelperManager.py)

**How to add a new menu mode:**

1. **Import the new mode manager** (top of file):
   ```python
   from save_calculated_points_mode.SaveCalculatedPointsManager import SaveCalculatedPointsManager
   ```

2. **Initialize in `__init__()`** (around line 109):
   ```python
   self.save_calculated_points_manager = SaveCalculatedPointsManager(
       self.config,
       self.player_manager,
       data_folder
   )
   ```

3. **Add to menu list** (line 136):
   ```python
   choice = show_list_selection(
       "MAIN MENU",
       [
           "Add to Roster",
           "Starter Helper",
           "Trade Simulator",
           "Modify Player Data",
           "Save Calculated Projected Points"  # NEW
       ],
       "Quit"
   )
   ```

4. **Add elif dispatch** (around line 148):
   ```python
   elif choice == 5:
       self.logger.info("Starting Save Calculated Points mode")
       self._run_save_calculated_points_mode()
   elif choice == 6:  # Shift Quit to 6
       print("Goodbye!")
       break
   ```

5. **Add dispatch method** (around line 196):
   ```python
   def _run_save_calculated_points_mode(self):
       """Delegate to Save Calculated Points mode manager."""
       self.save_calculated_points_manager.execute()
   ```

### StarterHelper Scoring Pattern (from StarterHelperModeManager.py)

**Critical initialization steps (lines 452-453):**
```python
# MUST calculate max_weekly_projection before scoring
max_weekly = self.player_manager.calculate_max_weekly_projection(self.config.current_nfl_week)
self.player_manager.scoring_calculator.max_weekly_projection = max_weekly
```

**Scoring method call (lines 405-420):**
```python
scored_player = self.player_manager.score_player(
    player_data,
    use_weekly_projection=True,      # For weekly; False for season-long
    adp=False,
    player_rating=False,
    team_quality=True,
    performance=True,
    matchup=True,
    schedule=False,
    bye=False,
    injury=False,
    temperature=True,
    wind=True,
    location=True
)
```

**Player source:**
- All players: `self.player_manager.players` (loaded from players.csv)
- Team roster only: `self.player_manager.team.roster`
- For this feature: Use ALL players (`self.player_manager.players`)

### Historical Data Copying Pattern (from player-data-fetcher)

**Files to copy (from player_data_fetcher_main.py lines 372-438):**
```python
files_to_copy = ["players.csv", "players_projected.csv", "game_data.csv"]
```

**Folder structure:**
```python
historical_folder = data_folder / "historical_data" / str(NFL_SEASON) / f"{CURRENT_NFL_WEEK:02d}"
```

**Copying logic:**
```python
# Create folder if needed
historical_folder.mkdir(parents=True, exist_ok=True)

# Copy each file
for filename in files_to_copy:
    source = data_folder / filename
    destination = historical_folder / filename
    if source.exists():
        shutil.copy2(str(source), str(destination))

# Copy team_data folder
team_data_source = data_folder / "team_data"
team_data_dest = historical_folder / "team_data"
if team_data_source.exists() and team_data_source.is_dir():
    shutil.copytree(str(team_data_source), str(team_data_dest), dirs_exist_ok=True)
```

### Config Values (from ConfigManager.py)

**Season and week from ConfigManager:**
```python
config.current_nfl_week  # int (0-17, where 0 = season-long)
config.nfl_season        # int (e.g., 2025)
```

---

## Open Questions (To Be Resolved)

### Architecture Questions

1. **Mode Manager Structure:** Should this be a full mode manager class (like AddToRosterModeManager) or a simpler utility class with just an execute() method?
   - **Context:** This mode has no user interaction beyond initial selection
   - **Options:**
     - A) Full mode manager with start_interactive_mode() (consistent pattern)
     - B) Simple manager with execute() method (lighter weight)

2. **Error Handling Strategy:** How should we handle missing files or folders?
   - **Context:** Files might not exist if player-data-fetcher hasn't run
   - **Options:**
     - A) Create folders automatically, skip missing files with warnings
     - B) Fail fast if any expected file is missing
     - C) Create folders automatically, error if critical files missing (players.csv)

3. **File Overwrite Behavior:** What if historical_data/{SEASON}/{WEEK}/ already exists with files?
   - **Context:** User might run this mode multiple times for same week
   - **Options:**
     - A) Skip if folder exists (idempotent like player-data-fetcher)
     - B) Overwrite all files
     - C) Prompt user for confirmation

### Scoring Logic Questions

4. **Player Filtering:** Should we score ALL players or only certain ones?
   - **Context:** `self.player_manager.players` includes all available players
   - **Options:**
     - A) Score all players (most useful for historical data)
     - B) Only score players on user's roster
     - C) Only score non-drafted players (free agents)

5. **Season-Long Scoring:** How to handle week 0 (season-long) scoring?
   - **Context:** StarterHelper uses weekly projections; need ROS equivalent
   - **Options:**
     - A) use_weekly_projection=False (uses rest-of-season from current week)
     - B) Special handling for week 0
     - C) Skip max_weekly_projection setup for season-long

6. **JSON Value Format:** What precision for calculated scores?
   - **Options:**
     - A) Full float precision (e.g., 342.5678901234)
     - B) Rounded to 2 decimals (e.g., 342.57)
     - C) Rounded to 1 decimal (e.g., 342.6)

### Implementation Details

7. **Player ID Key Format:** What format should player IDs be in JSON?
   - **Context:** player.id could be int or string
   - **Options:**
     - A) String keys (e.g., "12345")
     - B) Integer keys (e.g., 12345) - note: JSON will convert to string anyway

8. **Folder Location:** Where should the new mode manager class live?
   - **Options:**
     - A) `league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py`
     - B) `league_helper/SaveCalculatedPointsManager.py` (top level, since it's simple)

9. **Empty Results:** What if no players are available to score?
   - **Options:**
     - A) Save empty JSON {}
     - B) Error and don't create file
     - C) Warning and skip file creation

10. **Progress Display:** Should we show progress while scoring players?
    - **Context:** Scoring 1000+ players could take time
    - **Options:**
      - A) Silent execution (fast return to menu)
      - B) Show progress: "Scoring players: 500/1500..."
      - C) Show completion message: "Saved 1500 player scores to {path}"

### Edge Cases

11. **Week Validation:** What if current_nfl_week is invalid (< 0 or > 17)?
    - **Options:**
      - A) Clamp to valid range (0-17)
      - B) Error and abort
      - C) Use week value as-is and let folder creation handle it

12. **Missing game_data.csv:** What if game data file doesn't exist?
    - **Context:** Needed for temperature/wind/location scoring
    - **Options:**
      - A) Skip copying game_data.csv, score without those factors
      - B) Error and abort entire operation
      - C) Warning, continue with whatever files exist

---

## Resolved Implementation Details

(To be populated during Phase 4 as questions are resolved)

---

## Implementation Notes

### Files to Modify
- `league_helper/LeagueHelperManager.py` - Add new menu option and dispatch to new mode

### Files to Create
- `league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py` (or top-level location TBD)

### Dependencies
- `PlayerManager` - For loading players and scoring
- `ConfigManager` - For current week/season values
- `shutil` - For file copying operations
- `json` - For JSON output
- `pathlib.Path` - For path manipulation

### Reusable Code Patterns
- StarterHelper scoring initialization (max_weekly_projection setup) - lines 452-453
- StarterHelper score_player() call - lines 405-420
- player-data-fetcher file copying logic - lines 372-438

### Testing Strategy
- Unit tests for SaveCalculatedPointsManager class
- Integration test: Run mode, verify JSON output format and content
- Integration test: Verify file copying works correctly
- Test both weekly and season-long modes
- Test error handling for missing files

---

## Assumptions

| Assumption | Basis | Risk if Wrong | Mitigation |
|------------|-------|---------------|------------|
| PlayerManager.players has all available players | Code inspection of PlayerManager.load_players_from_csv() | Might only load team roster | Verify during implementation |
| ConfigManager.current_nfl_week is always valid | Used throughout codebase | Could be invalid value | Add validation check |
| shutil.copy2 preserves file integrity | Standard library behavior | File corruption | Use try-except for IOError |
| JSON can handle all player IDs | Standard JSON spec | ID format incompatibility | Convert IDs to strings explicitly |
| Historical data folder structure is consistent | player-data-fetcher uses same pattern | Folder mismatch | Follow exact pattern from fetcher |

---

## Status: PLANNING - Phase 2 Investigation in Progress
