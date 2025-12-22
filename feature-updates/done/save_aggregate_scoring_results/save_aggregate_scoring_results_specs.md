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

## Execution Path Coverage Analysis

**MANDATORY ANALYSIS per planning guide - prevents parallel path bugs like ranking_accuracy_metrics**

### Core Operations

This feature performs TWO core operations:
1. **Score all players** using PlayerManager.score_player()
2. **Copy files** to historical_data folder

### All Execution Paths Identified

**Path 1: Menu Selection (ONLY PATH)**
- **Entry:** User selects "Save Calculated Projected Points" from main menu
- **Route:** `LeagueHelperManager.start_interactive_mode()` → menu choice 5 → `_run_save_calculated_points_mode()` → `SaveCalculatedPointsManager.execute()`
- **Characteristics:** Synchronous, single-threaded, blocking operation
- **Needs update:** YES - this is the feature implementation

**No additional paths exist:**
- ❌ No parallel/worker process path
- ❌ No async/background task path
- ❌ No batch mode vs interactive mode distinction
- ❌ No API endpoint or external trigger
- ❌ No scheduled/automated execution
- ❌ Not callable from other modes programmatically (by design)

### Verification Checklist

- [x] Listed all files that perform scoring operations → Only new SaveCalculatedPointsManager
- [x] Listed all files that perform file copying → Only new SaveCalculatedPointsManager
- [x] Checked for parallel/worker implementations → None
- [x] Checked for async/event-driven paths → None
- [x] Checked for batch vs interactive modes → Only interactive (menu-driven)
- [x] Verified no missed execution paths

### Conclusion

This is a **simple, single-path feature** with no execution path complexity. The only entry point is the main menu selection, and it executes synchronously in the main thread.

---

## Resolved Implementation Details

### Architecture Decisions

**1. Mode Manager Structure** ✅ RESOLVED (2025-12-22)
- **Decision:** Full mode manager with standard structure (Option A)
- **Implementation:**
  ```python
  class SaveCalculatedPointsManager:
      def __init__(self, config: ConfigManager, player_manager: PlayerManager, data_folder: Path):
          self.logger = get_logger()
          self.config = config
          self.player_manager = player_manager
          self.data_folder = data_folder

      def execute(self) -> None:
          """Main entry point - score players and save to historical data."""
          # Implementation here
  ```
- **Rationale:** Consistency with other modes, easier for future developers, allows for future enhancements
- **File Location:** `league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py`

**2. ConfigManager Error Handling** ✅ RESOLVED (2025-12-22)
- **Decision:** Trust ConfigManager initialization (Option A)
- **Implementation:** Direct use of `self.config.current_nfl_week` and `self.config.nfl_season` without defensive checks
- **Rationale:** Matches all existing code patterns, ConfigManager is well-tested and typed, if config is broken the entire app fails during initialization anyway

### Files & Data Decisions

**3. Config Files to Copy** ✅ RESOLVED (2025-12-22)
- **Decision:** Copy entire `data/configs/` folder
- **Implementation:**
  ```python
  # Copy configs folder
  configs_source = data_folder / "configs"
  configs_dest = historical_folder / "configs"
  if configs_source.exists():
      shutil.copytree(str(configs_source), str(configs_dest), dirs_exist_ok=True)
  ```
- **Rationale:** Full reproducibility - preserves ALL configuration state (league_config.json + week-range configs) at time of scoring
- **Files included:** league_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json

**4. drafted_data.csv Copy** ✅ RESOLVED (2025-12-22)
- **Decision:** Copy drafted_data.csv (Option A)
- **Implementation:** Add to files_to_copy list
- **Rationale:** Captures roster state at time of scoring, enables historical analysis ("Who was available week 5?"), consistent with comprehensive snapshot approach

**Complete files to copy list:**
1. players.csv
2. players_projected.csv
3. game_data.csv
4. drafted_data.csv ← NEW
5. team_data/ (folder)
6. configs/ (folder) ← NEW

### User Experience Decisions

**5. Progress Display** ✅ RESOLVED (2025-12-22)
- **Decision:** Summary message only (Option C)
- **Implementation:**
  ```python
  # Entry message
  self.logger.info(f"Entering Save Calculated Points mode (Week {self.config.current_nfl_week})")

  # Score players (no progress messages)

  # Completion message
  print(f"Saved {len(scored_players)} player scores to {json_path}")
  print(f"Files copied: players.csv, game_data.csv, drafted_data.csv, team_data/ ({team_file_count} files), configs/ ({config_file_count} files)")
  ```
- **Rationale:** 1-4 seconds is fast enough that progress bar is unnecessary, summary provides confirmation and useful info, matches StarterHelper pattern

**6. JSON Format** ✅ RESOLVED (2025-12-22)
- **Decision:** Simple format without metadata wrapper (Option A)
- **Format:**
  ```json
  {
      "12345": 342.57,
      "67890": 298.13,
      "78901": 275.44
  }
  ```
- **Implementation:**
  ```python
  scored_dict = {str(player.id): round(scored.score, 2) for player, scored in scored_players}
  with open(json_path, 'w') as f:
      json.dump(scored_dict, f, indent=2)
  ```
- **Rationale:** Week/season info in folder path, config info in copied configs folder, simpler to parse, YAGNI principle (don't add complexity until needed)

### Scoring Details Decisions

**7. Parallelization** ✅ RESOLVED (2025-12-22)
- **Decision:** Sequential loop (Option A)
- **Implementation:**
  ```python
  scored_players = []
  for player in self.player_manager.players:
      scored = self.player_manager.score_player(
          player,
          use_weekly_projection=(week > 0),  # False for week 0 (season-long)
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
      scored_players.append((player, scored))
  ```
- **Rationale:** 1-4 seconds is acceptable, simplicity preferred over marginal performance gain, matches existing patterns, easier to maintain and debug

**8. Player Filtering** ✅ RESOLVED (2025-12-22)
- **Decision:** Score all available players (Option A)
- **Implementation:** Score all players in `self.player_manager.players` (no filtering)
  ```python
  # Score ALL players (available + drafted + on our team)
  for player in self.player_manager.players:
      scored = self.player_manager.score_player(player, ...)
  ```
- **Rationale:** Comprehensive historical record (~1500 players), enables future analysis ("Should I have picked up player X in week 5?"), negligible time difference vs filtering, matches comprehensive snapshot approach

**9. Season-Long Scoring (Week 0)** ✅ RESOLVED (2025-12-22)
- **Decision:** Use `use_weekly_projection=False` for week 0 (Option A)
- **Implementation:**
  ```python
  week = self.config.current_nfl_week

  # Only calculate max_weekly_projection if using weekly scoring
  if week > 0:
      max_weekly = self.player_manager.calculate_max_weekly_projection(week)
      self.player_manager.scoring_calculator.max_weekly_projection = max_weekly

  # Score players with conditional flag
  for player in self.player_manager.players:
      scored = self.player_manager.score_player(
          player,
          use_weekly_projection=(week > 0),  # False for week 0, True for 1-17
          # ... other parameters
      )
  ```
- **Rationale:** When week=0, `use_weekly_projection=False` uses `fantasy_points` (season-long projection) instead of weekly projections. Simplest implementation, uses existing parameter designed for this.

**Output paths:**
- Week 0: `data/historical_data/{SEASON}/calculated_season_long_projected_points.json` (no week subfolder)
- Week 1-17: `data/historical_data/{SEASON}/{WEEK}/calculated_projected_points.json`

**10. JSON Score Precision** ✅ RESOLVED (2025-12-22)
- **Decision:** Round to 2 decimal places (Option B)
- **Implementation:**
  ```python
  scored_dict = {str(player.id): round(scored.score, 2) for player, scored in scored_players}
  with open(json_path, 'w') as f:
      json.dump(scored_dict, f, indent=2)
  ```
- **Example output:**
  ```json
  {
    "12345": 342.57,
    "67890": 298.13,
    "78901": 275.44
  }
  ```
- **Rationale:** Standard for scoring/monetary values, good balance between precision and readability, sufficient for meaningful comparisons, smaller file size than full float precision

---

## Open Questions (To Be Resolved)

### Architecture Questions

**3. Error Handling Strategy:** How should we handle missing files or folders?
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

## Performance Analysis

**MANDATORY per planning guide - analyze efficiency implications**

### Time Complexity Analysis

| Operation | Count | Time per Op (est.) | Total Time (est.) |
|-----------|-------|-------------------|-------------------|
| Score players | ~1500 players | ~0.5-2ms/player | ~0.75-3 seconds |
| Copy files | 3 files + folder | ~10-50ms/file | ~40-200ms |
| Write JSON | 1 file (~500KB) | ~10-50ms | ~10-50ms |
| **TOTAL** | - | - | **~1-4 seconds** |

**Assumptions:**
- `score_player()` is fast (no network calls, pure computation)
- File I/O is to local disk (not network drive)
- ~1500 players typical dataset size
- JSON file ~500KB (1500 players × ~350 bytes/player)

### Space Complexity

| Resource | Size | Notes |
|----------|------|-------|
| In-memory player list | ~15MB | Already loaded by PlayerManager |
| Scored results dict | ~500KB | {player_id: score} for ~1500 players |
| JSON output | ~500KB | Written to disk |
| Copied files | ~5-10MB | players.csv (5MB), game_data.csv (50KB), team_data (500KB) |
| **Peak memory** | ~15MB | No significant increase (players already loaded) |

### I/O Analysis

| Operation | Disk Reads | Disk Writes | Network Calls |
|-----------|------------|-------------|---------------|
| Score players | 0 (data in memory) | 0 | 0 |
| Copy files | 3 + ~32 team files | 3 + ~32 team files | 0 |
| Write JSON | 0 | 1 | 0 |
| **TOTAL** | ~35 reads | ~36 writes | 0 |

**Bottleneck:** File copying (35 reads + 36 writes) is likely slower than scoring

### Performance Recommendations

**Sequential vs Parallel:**
- **Recommendation:** Sequential loop for scoring (simplest)
- **Rationale:**
  - ~1-4 seconds is acceptable for menu operation
  - No user is waiting impatiently (they can walk away)
  - Parallelization adds complexity with minimal benefit
  - Matches existing mode patterns (all are sequential)

**Optimization Opportunities:**
1. **Skip scoring if folder exists** (like player-data-fetcher) - saves 1-3 seconds
2. **Progress display for >1000 players** - improves UX perception
3. **Batch write to JSON** (current plan) - most efficient

**User Experience Impact:**
- Expected delay: 1-4 seconds (acceptable for "Save" operation)
- Should display completion message: "Saved 1523 player scores to {path}"
- No progress bar needed if <5 seconds

---

## Vagueness Audit

**MANDATORY per planning guide - flag ambiguous phrases requiring clarification**

### Vague Phrases Found in Notes

| Phrase | Problem | Checklist Item Added |
|---------|---------|---------------------|
| "Same scoring logic as StarterHelper" | Which parameters? Which setup steps? | ✓ Added to checklist (Q4-Q5) |
| "Relevant files" | Which files exactly? | ✓ RESOLVED - match player-data-fetcher list |
| "Current week or entire season" | How to detect/handle week 0? | ✓ Added to checklist (Q5) |
| "Calculate calculated projected points" | Redundant terminology - means what? | ✓ Clarified: output of score_player() |

### Feature Pair Completeness Check

| Feature Phrase | Required Pair | Status |
|----------------|---------------|--------|
| "Save X" | Load X (and use it!) | ✓ OUT OF SCOPE - saving only for now |
| "Copy files" | Verify files exist | ✓ RESOLVED - check exists(), skip missing |
| "Historical data" | Multiple seasons support | ✓ RESOLVED - path includes season |
| "Menu mode" | Return to menu | ✓ IMPLICIT - all modes return to menu |

### "Same As X" Verification

| Phrase | Reference | Verification Status |
|---------|-----------|---------------------|
| "Same scoring logic as StarterHelper" | StarterHelperModeManager.py:405-419 | ✓ VERIFIED - exact parameters documented in specs |
| "Same files as player-data-fetcher" | player_data_fetcher_main.py:410 | ✓ VERIFIED - exact list documented in specs |
| "Historical data folder structure" | player_data_fetcher_main.py:397 | ✓ VERIFIED - path pattern documented in specs |

**All vague phrases resolved or added to checklist for user decision.**

---

## Testing Requirements Analysis

**MANDATORY per planning guide - define validation and smoke testing**

### Integration Points

| Component A | Component B | Integration Mechanism | How to Verify |
|-------------|-------------|----------------------|---------------|
| SaveCalculatedPointsManager | PlayerManager | Calls score_player() for each player | Verify score values match expected range |
| SaveCalculatedPointsManager | ConfigManager | Reads current_nfl_week, nfl_season | Verify folder path uses correct week/season |
| SaveCalculatedPointsManager | File system | Creates folders, copies files, writes JSON | Verify all files exist after execution |
| LeagueHelperManager | SaveCalculatedPointsManager | Menu selection calls execute() | Integration test: select menu → verify JSON created |

### Smoke Test Success Criteria

**Output Validation:**
- [ ] JSON file created at expected path
- [ ] JSON contains expected number of players (~1500)
- [ ] Score values are reasonable (e.g., 0-500 range for draft, 0-50 for weekly)
- [ ] All player IDs are valid integers (converted to string keys)
- [ ] Files copied successfully (players.csv, game_data.csv, team_data/)

**Log Quality:**
- [ ] Info log: "Entering Save Calculated Points mode (Week X)"
- [ ] Info log: "Saved X player scores to {path}"
- [ ] No ERROR messages in output
- [ ] Warning messages only for expected cases (missing optional files)

**User Experience:**
- [ ] Operation completes in <5 seconds
- [ ] Returns to main menu after completion
- [ ] Folder structure matches player-data-fetcher pattern (zero-padded week)

### Expected vs Actual Validation

| Metric | Expected Value/Pattern | How to Check |
|--------|------------------------|--------------|
| Player count | 1400-1600 players | `len(json_data)` in JSON file |
| Score range (draft) | 0-500 | Sample player scores |
| Score range (weekly) | 0-50 | Sample player scores |
| JSON file size | ~500KB | File size check |
| Execution time | 1-4 seconds | Time operation |
| Files copied | 3 files + team_data/ | Count files in historical_data/{SEASON}/{WEEK}/ |

### User-Facing Outputs

**Console Output:**
```
Entering Save Calculated Points mode (Week 15)
Scoring 1523 players...
Saved 1523 player scores to data/historical_data/2025/15/calculated_projected_points.json
Files copied: players.csv, players_projected.csv, game_data.csv, team_data/ (32 files)
```

**Files Created:**
```
data/historical_data/2025/15/
├── calculated_projected_points.json  (NEW)
├── players.csv (copied)
├── players_projected.csv (copied)
├── game_data.csv (copied)
└── team_data/ (copied, 32 CSV files)
```

### Acceptance Testing Plan

**Manual Verification Steps:**
1. User runs League Helper, selects "Save Calculated Projected Points"
2. User observes:
   - [ ] Completion message displays with player count and path
   - [ ] Operation returns to menu within 5 seconds
   - [ ] No error messages appear
3. User checks output folder:
   - [ ] Folder exists at data/historical_data/2025/15/ (or current season/week)
   - [ ] JSON file exists and is ~500KB
   - [ ] Copied files all exist
4. User opens JSON file:
   - [ ] Valid JSON format
   - [ ] Contains ~1500 player entries
   - [ ] Scores are reasonable numbers

**Comparison to Working Reference:**
- Compare folder structure to existing historical_data folders (from player-data-fetcher)
- Verify same files are present
- Verify same folder naming convention (zero-padded weeks)

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
