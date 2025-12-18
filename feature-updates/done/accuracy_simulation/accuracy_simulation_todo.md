# Accuracy Simulation - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 |

**Current Iteration:** 24 (COMPLETE)

**Note (Step 3):** No questions file needed - spec is complete. Issues found during verification are implementation details that don't require user decisions. Proceeding to Step 5 (Second Verification Round).

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [x]1 [x]2 [x]3 [x]8 [x]9 [x]10 [x]15 [x]16 |
| Algorithm Traceability | 4, 11, 19 | [x]4 [x]11 [x]19 |
| End-to-End Data Flow | 5, 12 | [x]5 [x]12 |
| Skeptical Re-verification | 6, 13, 22 | [x]6 [x]13 [x]22 |
| Integration Gap Check | 7, 14, 23 | [x]7 [x]14 [x]23 |
| Fresh Eyes Review | 17, 18 | [x]17 [x]18 |
| Edge Case Verification | 20 | [x]20 |
| Test Coverage Planning | 21 | [x]21 |
| Implementation Readiness | 24 | [x]24 |

---

## Verification Summary

- Iterations completed: 24/24 ✓ ALL COMPLETE
- Requirements from spec: 45+
- Requirements in TODO: 10 phases, 28 tasks
- Questions for user: 0 (spec complete)
- Integration points identified: 8 (see Integration Matrix)
- Dependencies documented: PlayerManager → ConfigManager, TeamDataManager, SeasonScheduleManager
- Implementation Ready: YES

---

## Phase 1: Folder Restructuring

### Task 1.1: Create shared/ folder and move shared classes
- **Files to move:**
  - `simulation/ConfigGenerator.py` → `simulation/shared/ConfigGenerator.py`
  - `simulation/ResultsManager.py` → `simulation/shared/ResultsManager.py`
  - `simulation/ConfigPerformance.py` → `simulation/shared/ConfigPerformance.py`
  - `simulation/ProgressTracker.py` → `simulation/shared/ProgressTracker.py` **(DISCOVERED: used by both sims)**
  - `simulation/config_cleanup.py` → `simulation/shared/config_cleanup.py` **(DISCOVERED: needs update for accuracy_optimal_* pattern)**
- **Create:** `simulation/shared/__init__.py` (optional per sys.path pattern)
- **Tests:** Update test imports in `tests/simulation/`
- **Status:** [x] COMPLETE

### Task 1.2: Create win_rate/ folder and move win-rate specific classes
- **Files to move:**
  - `simulation/SimulationManager.py` → `simulation/win_rate/SimulationManager.py`
  - `simulation/ParallelLeagueRunner.py` → `simulation/win_rate/ParallelLeagueRunner.py`
  - `simulation/SimulatedLeague.py` → `simulation/win_rate/SimulatedLeague.py`
  - `simulation/DraftHelperTeam.py` → `simulation/win_rate/DraftHelperTeam.py`
  - `simulation/SimulatedOpponent.py` → `simulation/win_rate/SimulatedOpponent.py`
  - `simulation/Week.py` → `simulation/win_rate/Week.py`
  - `simulation/manual_simulation.py` → `simulation/win_rate/manual_simulation.py` **(DISCOVERED: runs drafts)**
- **Tests:** Update test imports
- **Status:** [x] COMPLETE

### Task 1.3: Create accuracy/ folder structure
- **Create:**
  - `simulation/accuracy/` folder
  - `simulation/accuracy/AccuracySimulationManager.py`
  - `simulation/accuracy/AccuracyResultsManager.py`
  - `simulation/accuracy/AccuracyConfigPerformance.py` (merged into AccuracyResultsManager.py)
  - `simulation/accuracy/AccuracyCalculator.py` (replaces PlayerAccuracyCalculator.py)
- **Status:** [x] COMPLETE

### Task 1.4: Update all imports after folder restructure
- **Files to update:**
  - All files in `simulation/win_rate/` - update imports for shared classes
  - `run_simulation.py` (before rename) - update imports
  - Test files - update imports
- **Pattern:** Keep sys.path.append, adjust paths
- **Specific import changes needed:**
  - `SimulationManager.py`: ConfigGenerator, ResultsManager, ConfigPerformance, ProgressTracker, config_cleanup → from shared/
  - `SimulationManager.py`: ParallelLeagueRunner → stays local (win_rate/)
  - `ParallelLeagueRunner.py`: SimulatedLeague → stays local (win_rate/)
  - `SimulatedLeague.py`: DraftHelperTeam, SimulatedOpponent, Week → stay local (win_rate/)
  - `Week.py`: DraftHelperTeam, SimulatedOpponent → stay local (win_rate/)
  - `ConfigGenerator.py`: ResultsManager → from shared/ (self-reference after move)
  - `ResultsManager.py`: ConfigPerformance, config_cleanup → from shared/ (self-reference)
  - `manual_simulation.py`: SimulatedLeague → stays local (win_rate/)
- **Status:** [x] COMPLETE

---

## Phase 2: Runner Script Changes

### Task 2.1: Rename existing simulation scripts
- **Rename:**
  - `run_simulation.py` → `run_win_rate_simulation.py`
  - `run_simulation_loop.sh` → `run_win_rate_simulation_loop.sh`
- **Update imports:** Adjust for new folder structure
- **Status:** [x] COMPLETE

### Task 2.2: Create run_accuracy_simulation.py
- **Similar to:** `run_simulation.py` (current)
- **CLI args:** --mode (ros/weekly/both), --baseline, --output, --workers, --data, --test-values, --use-processes
- **Note:** NO --sims flag (MAE is deterministic)
- **Default mode:** `both` (runs ROS first, then Weekly)
- **Status:** [x] COMPLETE

### Task 2.3: Create run_accuracy_simulation_loop.sh
- **Similar to:** `run_simulation_loop.sh`
- **Pattern:** trap signals, restart on kill/error, exit on success
- **Status:** [x] COMPLETE

---

## Phase 3: Accuracy Simulation Core Classes

### Task 3.1: Create AccuracySimulationManager.py
- **Location:** `simulation/accuracy/AccuracySimulationManager.py`
- **Responsibilities:**
  - Handle --mode options (ros, weekly, both)
  - Iterate through config parameters (17 prediction params)
  - Coordinate ROS and Weekly accuracy calculations
  - Signal handling (SIGINT/SIGTERM graceful shutdown)
  - Resume capability via intermediate folders
- **Similar to:** `SimulationManager.py` for structure
- **Status:** [x] COMPLETE

### Task 3.2: Create AccuracyConfigPerformance.py
- **Location:** `simulation/accuracy/AccuracyResultsManager.py` (merged into same file)
- **Metrics to track:**
  - `mae` - Mean Absolute Error (primary, lower is better)
  - `player_count` - Number of players evaluated
  - `config_id` - Parameter combo hash
  - `timestamp` - When config was tested
- **Similar to:** `ConfigPerformance.py` but with MAE instead of win_rate
- **Status:** [x] COMPLETE

### Task 3.3: Create AccuracyResultsManager.py
- **Location:** `simulation/accuracy/AccuracyResultsManager.py`
- **Output folders:**
  - `accuracy_optimal_TIMESTAMP/`
  - `accuracy_intermediate_{idx}_{param}/`
- **Output files:** draft_config.json + 4 week-range files
- **Best config selection:** Lowest MAE wins (opposite of win-rate)
- **Similar to:** `ResultsManager.py` but inverted comparison
- **Status:** [x] COMPLETE

### Task 3.4: Create AccuracyCalculator.py (was PlayerAccuracyCalculator.py)
- **Location:** `simulation/accuracy/AccuracyCalculator.py`
- **Core algorithm:**
  ```python
  # For each player:
  error = abs(actual_points - projected_points)
  # Aggregate across all players:
  mae = sum(errors) / len(errors)
  ```
- **Player filtering:**
  - Exclude: 0 actual points
  - Include: All others regardless of projection or games played
  - Skip: Missing data (incomplete weeks) for that player-week only
- **Data sources:**
  - `scored_player.projected_points` (un-normalized) - from PlayerManager.score_player()
  - `player.actual_points` from CSV
- **Dependencies (DISCOVERED in verification):**
  - PlayerManager requires: ConfigManager, TeamDataManager, SeasonScheduleManager
  - Must create these managers for each config test
  - Config can be loaded from JSON generated by ConfigGenerator
- **Status:** [x] COMPLETE

---

## Phase 4: ROS (Rest of Season) Mode

### Task 4.1: Implement ROS accuracy calculation
- **Evaluation timing:** Week 1 only (pre-season predictions)
- **Data source:** `sim_data/{year}/weeks/week_01/` for projections
- **Actual source:** Season totals from `sim_data/players_actual.csv`
- **Output:** Optimizes `draft_config.json`
- **Status:** [x] COMPLETE (in AccuracySimulationManager.py)

### Task 4.2: Handle multi-season ROS aggregation
- **Aggregate across:** All 20XX folders in sim_data (2021, 2022, 2024)
- **Weighting:** Equal weight - all seasons count the same
- **Status:** [x] COMPLETE (in AccuracySimulationManager.py)

---

## Phase 5: Weekly Mode

### Task 5.1: Implement Weekly accuracy calculation
- **Week ranges:** 1-5, 6-9, 10-13, 14-17 (same as win-rate)
- **Data source:** Weekly CSVs are SNAPSHOTS at that week
- **Bye week handling:** Skip empty week_N_points values
- **Output:** Optimizes week1-5.json, week6-9.json, week10-13.json, week14-17.json
- **Status:** [x] COMPLETE (in AccuracySimulationManager.py)

### Task 5.2: Handle multi-season Weekly aggregation
- **Same pattern as ROS:** Aggregate across all years equally
- **Status:** [x] COMPLETE (in AccuracySimulationManager.py)

---

## Phase 6: ConfigManager Updates

### Task 6.1: Add draft_config.json support to ConfigManager
- **Location:** `league_helper/util/ConfigManager.py`
- **Change:** Add ability to load draft_config.json for Add to Roster Mode
- **Mode-specific selection:** Add `use_draft_config` parameter to __init__ (default False)
- **Missing file handling:** Error with helpful message (no silent fallback)
- **Implementation approach:**
  - Add `use_draft_config: bool = False` parameter to __init__
  - If True: load draft_config.json instead of week-specific config
  - If draft_config.json missing: raise FileNotFoundError with helpful message
- **Status:** [x] COMPLETE

### Task 6.1a: Update LeagueHelperManager to pass use_draft_config
- **Location:** `league_helper/LeagueHelperManager.py`
- **Change:** Create separate ConfigManager and PlayerManager for Add to Roster Mode
- **Implementation:**
  - Added `self.draft_config = ConfigManager(data_folder, use_draft_config=True)`
  - Added `self.draft_player_manager = PlayerManager(data_folder, self.draft_config, ...)`
  - Updated `AddToRosterModeManager` initialization to use `draft_config` and `draft_player_manager`
  - Updated `_run_add_to_roster_mode()` to pass `draft_player_manager`
- **Status:** [x] COMPLETE

### Task 6.2: Create initial draft_config.json
- **Location:** `data/configs/draft_config.json`
- **Initial content:** Copy of week1-5.json
- **Status:** [x] COMPLETE - Created 2025-12-15

---

## Phase 7: Win Rate Simulation Updates

### Task 7.1: Create separate PARAMETER_ORDER for Win Rate
- **Purpose:** Only test league_config.json params (strategy)
- **Strategy params (5 total):**
  - SAME_POS_BYE_WEIGHT
  - DIFF_POS_BYE_WEIGHT
  - PRIMARY_BONUS
  - SECONDARY_BONUS
  - ADP_SCORING_WEIGHT
- **Implementation:** Update PARAMETER_ORDER in run_win_rate_simulation.py to only include these 5
- **Note:** NORMALIZATION_MAX_SCALE is in week configs, not league_config - remove from win-rate
- **Status:** [x] COMPLETE

### Task 7.2: Disable auto-copy in Win Rate simulation
- **Current behavior:** Auto-copies to data/configs/
- **New behavior:** Manual copy only
- **Status:** [ ] N/A - Auto-copy was already not implemented

---

## Phase 8: Accuracy Simulation Parameter Handling

### Task 8.1: Define PARAMETER_ORDER for Accuracy simulation
- **17 prediction params:**
  1. NORMALIZATION_MAX_SCALE
  2. PLAYER_RATING_SCORING_WEIGHT
  3. TEAM_QUALITY_SCORING_WEIGHT
  4. TEAM_QUALITY_MIN_WEEKS
  5. PERFORMANCE_SCORING_WEIGHT
  6. PERFORMANCE_SCORING_STEPS
  7. PERFORMANCE_MIN_WEEKS
  8. MATCHUP_IMPACT_SCALE
  9. MATCHUP_SCORING_WEIGHT
  10. MATCHUP_MIN_WEEKS
  11. TEMPERATURE_IMPACT_SCALE
  12. TEMPERATURE_SCORING_WEIGHT
  13. WIND_IMPACT_SCALE
  14. WIND_SCORING_WEIGHT
  15. LOCATION_HOME
  16. LOCATION_AWAY
  17. LOCATION_INTERNATIONAL
- **Status:** [x] COMPLETE (defined in AccuracySimulationManager.py as ACCURACY_PARAMETER_ORDER)

### Task 8.2: Implement SCHEDULE sync with MATCHUP
- **Requirement:** When updating JSON files, SCHEDULE params must mirror MATCHUP
- **Params to sync:**
  - SCHEDULE_IMPACT_SCALE = MATCHUP_IMPACT_SCALE
  - SCHEDULE_SCORING_WEIGHT = MATCHUP_SCORING_WEIGHT
  - SCHEDULE_MIN_WEEKS = MATCHUP_MIN_WEEKS
- **Status:** [x] COMPLETE (implemented in AccuracyResultsManager._sync_schedule_params())

---

## Phase 9: Testing

### Task 9.1: Create accuracy simulation unit tests
- **Location:** `tests/simulation/` (kept in main tests/simulation for now)
- **Test files created:**
  - `test_AccuracyCalculator.py` (21 tests):
    - Test MAE calculation with various scenarios
    - Test player filtering (exclude 0 actual, include all others)
    - Test ROS and weekly MAE calculation
    - Test season result aggregation
  - `test_AccuracyResultsManager.py` (28 tests):
    - Test AccuracyConfigPerformance creation and comparison
    - Test is_better_than() (lower MAE = better)
    - Test save_optimal_configs()
    - Test intermediate folder creation
    - Test _sync_schedule_params()
    - Test accuracy_optimal_* folder naming
  - `test_AccuracySimulationManager.py` (10 tests):
    - Test initialization
    - Test parameter order
    - Test mode handling
- **Status:** [x] COMPLETE

### Task 9.2: Update existing simulation tests
- **Update imports:** For new folder structure
- **Test win_rate/ classes:** Ensure existing tests still pass
- **Note:** Tests kept in tests/simulation/ to avoid breaking pytest discovery. Imports updated to use sys.path.append pattern.
- **Status:** [x] COMPLETE (all 2281 tests pass)

### Task 9.3: Create MAE formula validation tests
- **Known inputs/outputs:** Create test fixtures with expected MAE values
- **Edge cases to test (verified in iteration 20):**
  - 0 players → Returns MAE=0, player_count=0
  - Single player → MAE = abs(actual - projected) for that player
  - Tie-breaking → First config found wins (per spec)
  - Empty week_N_points (None) → Skip this week for this player
  - 0 actual points → Exclude player from calculation
  - 0 projected points → Include player (no threshold per spec)
  - All players excluded → Returns MAE=0, player_count=0
  - Very large errors → Should still calculate (no overflow protection needed for realistic data)
- **Status:** [x] COMPLETE (included in test_AccuracyCalculator.py)

### Task 9.4: Create integration tests
- **End-to-end:** Test run_accuracy_simulation.py execution
- **Real objects:** Minimize mocking for integration tests
- **Output validation:** Verify JSON contents, not just existence
- **Status:** [x] COMPLETE - 15 tests in tests/integration/test_accuracy_simulation_integration.py

---

## Phase 10: Documentation

### Task 10.1: Add workflow documentation
- **Explain:** When to run which simulation (Win-rate = strategy, Accuracy = prediction)
- **Location:** simulation/README.md
- **Status:** [x] COMPLETE - Updated simulation/README.md with two-mode overview, architecture diagram, quick start examples

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| AccuracySimulationManager | accuracy/AccuracySimulationManager.py | run_accuracy_simulation.py | run_accuracy_simulation.py:main() | Task 2.2 |
| AccuracyResultsManager | accuracy/AccuracyResultsManager.py | AccuracySimulationManager | AccuracySimulationManager.py:__init__ | Task 3.1 |
| AccuracyConfigPerformance | accuracy/AccuracyConfigPerformance.py | AccuracyResultsManager | AccuracyResultsManager.py | Task 3.3 |
| PlayerAccuracyCalculator | accuracy/PlayerAccuracyCalculator.py | AccuracySimulationManager | AccuracySimulationManager.py:run_ros/weekly | Task 3.1 |
| _load_draft_config() | ConfigManager.py | ConfigManager._load_config() | ConfigManager.py:_load_config | Task 6.1 |
| use_draft_config param | ConfigManager.__init__ | LeagueHelperManager.__init__() | LeagueHelperManager.py:74 | Task 6.1a |
| _sync_schedule_params() | AccuracyResultsManager.py | AccuracyResultsManager.save_config() | AccuracyResultsManager.py | Task 3.3 |
| cleanup_old_accuracy_folders() | config_cleanup.py | AccuracyResultsManager.save_optimal() | AccuracyResultsManager.py | Task 1.1 (update) |

**Integration Gap Check Results (Iteration 7):**
- All new methods have identified callers ✓
- Task 6.1a added to address ConfigManager caller in LeagueHelperManager ✓
- config_cleanup.py needs update to handle accuracy_optimal_* pattern ✓

**Integration Gap Check Results (Iteration 14):**
- PlayerAccuracyCalculator needs PlayerManager → requires ConfigManager, TeamDataManager, SeasonScheduleManager
- AccuracySimulationManager must create these dependency managers for each config test
- Pattern: Similar to how SimulatedLeague creates these managers

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Accuracy Metric (lines 180-196) | MAE = mean(abs(actual - projected)) | PlayerAccuracyCalculator.calculate_mae() | None - simple aggregation |
| Player Filtering (lines 200-211) | Exclude 0 actual, skip missing data | PlayerAccuracyCalculator._should_include_player() | if actual == 0: exclude; if week_data is None: skip |
| Un-Normalization (lines 275-292) | Use ScoredPlayer.projected_points | EXISTING: player_scoring.py:455-466 | N/A - already implemented |
| Best Config Selection (lines 182-185) | Lowest MAE wins | AccuracyResultsManager.is_better_config() | if new_mae < current_best_mae: True |
| SCHEDULE Sync (lines 253) | SCHEDULE params = MATCHUP params | AccuracyResultsManager._sync_schedule_params() | Copy MATCHUP values to SCHEDULE |
| ROS Mode (lines 215-219) | Week 1 evaluation only | AccuracySimulationManager.run_ros_mode() | Load week_01/ data only |
| Weekly Mode (lines 223-228) | Per week-range evaluation | AccuracySimulationManager.run_weekly_mode() | Loop WEEK_RANGES [1-5, 6-9, 10-13, 14-17] |
| --mode CLI (lines 232-238) | ros/weekly/both options | AccuracySimulationManager.run() | if mode=="both": ROS first, then Weekly |

---

## Data Flow Traces

### Requirement: ROS Accuracy Calculation
```
Entry: run_accuracy_simulation.py --mode ros
  → AccuracySimulationManager.__init__()
  → AccuracySimulationManager.run_ros_mode()
  → For each config combination:
    → PlayerAccuracyCalculator.calculate_ros_accuracy()
    → AccuracyConfigPerformance.record_mae()
  → AccuracyResultsManager.save_best_config()
  → Output: simulation/simulation_configs/accuracy_optimal_TIMESTAMP/draft_config.json
```

### Requirement: Weekly Accuracy Calculation
```
Entry: run_accuracy_simulation.py --mode weekly
  → AccuracySimulationManager.__init__()
  → AccuracySimulationManager.run_weekly_mode()
  → For each week_range in [1-5, 6-9, 10-13, 14-17]:
    → For each config combination:
      → PlayerAccuracyCalculator.calculate_weekly_accuracy(week_range)
      → AccuracyConfigPerformance.record_mae()
    → AccuracyResultsManager.save_best_config(week_range)
  → Output: simulation/simulation_configs/accuracy_optimal_TIMESTAMP/week{range}.json
```

### Requirement: ConfigManager draft_config.json loading
```
Entry: run_league_helper.py → Add to Roster Mode
  → LeagueHelperManager.__init__() [LeagueHelperManager.py:54]
  → ConfigManager.__init__(data_folder) [ConfigManager.py:159]
  → ConfigManager._load_config() [ConfigManager.py:848]
    → NEW: If mode is Add to Roster:
      → ConfigManager._load_draft_config() ← NEW METHOD
      → Merge draft_config.json params over base
  → AddToRosterModeManager uses merged config for prediction params
```

### Requirement: Folder Restructure Import Updates
```
BEFORE (current):
  run_simulation.py imports from simulation/SimulationManager.py
  SimulationManager.py imports ConfigGenerator, ParallelLeagueRunner, ResultsManager from simulation/

AFTER (restructured):
  run_win_rate_simulation.py imports from simulation/win_rate/SimulationManager.py
  SimulationManager.py imports from simulation/shared/ for shared classes
  SimulationManager.py imports from simulation/win_rate/ for win_rate specific classes
```

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:**
  - ScoredPlayer.projected_points field exists (ScoredPlayer.py:59)
  - Un-normalization formula in player_scoring.py:455-466
  - Weekly CSVs are snapshots (verified different values between weeks)
  - SCHEDULE and MATCHUP have same structure for sync
- **Issues identified:**
  1. **config_cleanup.py only handles "optimal_*" pattern** - needs update for "accuracy_optimal_*"
  2. **ConfigManager mode awareness** - needs way to know when to load draft_config.json vs week config
- **Corrections made:**
  - Added Task 1.1 note about config_cleanup.py needing update
  - Need to add ConfigManager task for mode-aware config loading
- **Confidence level:** Medium-High (2 issues need resolution)

### Round 2 (Iteration 13)
- **Verified correct:**
  - Data file structure at sim_data/ level
  - players_actual.csv contains season-end actual points
  - Weekly CSVs have week_N_points columns
  - SimulatedLeague already imports from league_helper.util.PlayerManager
- **Issues identified:**
  1. **PlayerManager dependencies** - Need ConfigManager, TeamDataManager, SeasonScheduleManager to score players
  2. Must create these managers for each config being tested
- **Corrections made:**
  - Added dependency note to Task 3.4 (PlayerAccuracyCalculator)
- **Confidence level:** High (dependencies well-understood now)

### Round 3 (Iteration 22)
- **Verified correct:**
  - Implementation order is correct (folder restructure first)
  - PlayerManager can be instantiated multiple times (no singleton)
  - ConfigGenerator creates config dicts in memory
  - FantasyPlayer already has week_N_points fields
- **Issues identified:**
  - ConfigManager expects file paths, but ConfigGenerator creates in-memory dicts
  - Solution: Either write temp configs to disk OR create temp ConfigManager from dict
  - Existing pattern: SimulatedLeague uses temp files for config (verify)
- **Corrections made:** None needed - this is an implementation detail
- **Confidence level:** High - all core algorithms and data flows verified

### Iteration 23: Integration Gap Check #3
- **Verified all integration points:**
  - AccuracySimulationManager → PlayerAccuracyCalculator: calls calculate_ros_accuracy(), calculate_weekly_accuracy()
  - PlayerAccuracyCalculator → PlayerManager: needs to create instances with proper dependencies
  - ConfigManager temp file pattern: SimulatedLeague.py:108-110 shows write to temp_dir/league_config.json
  - AccuracyResultsManager → config_cleanup.py: needs cleanup_old_accuracy_folders() function
- **Pattern confirmed:**
  - SimulatedLeague creates temp directory (tempfile.mkdtemp)
  - Writes config_dict to temp_dir/league_config.json using json.dump
  - ConfigManager loads from that path
  - Same pattern will work for accuracy simulation
- **No new gaps identified:** All integration points have clear implementation paths

### Iteration 24: Implementation Readiness Final Check
- **Checklist:**
  - [x] All 24 verification iterations complete
  - [x] All algorithms have traceability to code locations
  - [x] All data flows documented
  - [x] All integration points mapped
  - [x] Test coverage planned
  - [x] Edge cases documented
  - [x] No blocking questions remain
  - [x] Existing patterns identified for reuse (temp file config pattern)
- **Ready to implement:** YES
- **Implementation order confirmed:**
  1. Phase 1: Folder restructure (enables clean separation)
  2. Phase 2: Runner script changes
  3. Phase 3-5: Accuracy simulation core (3=classes, 4=ROS, 5=Weekly)
  4. Phase 6: ConfigManager updates
  5. Phase 7: Win Rate simulation updates
  6. Phase 8: Parameter handling
  7. Phase 9: Testing
  8. Phase 10: Documentation

---

## Progress Notes

**Last Updated:** 2025-12-14
**Current Status:** IMPLEMENTATION COMPLETE

### Completed Phases:
- [x] Phase 1: Folder restructuring (simulation/shared/, win_rate/, accuracy/)
- [x] Phase 2: Runner scripts (run_win_rate_simulation.py, run_accuracy_simulation.py, loop scripts)
- [x] Phase 3: Accuracy simulation core classes (AccuracyCalculator, AccuracyResultsManager, AccuracySimulationManager)
- [x] Phase 4: ROS mode implementation (in AccuracySimulationManager)
- [x] Phase 5: Weekly mode implementation (in AccuracySimulationManager)
- [x] Phase 6: ConfigManager draft_config.json support (use_draft_config parameter)
- [x] Phase 6.1a: LeagueHelperManager integration (separate ConfigManager/PlayerManager for Add to Roster Mode)
- [x] Phase 7: Win Rate PARAMETER_ORDER split (5 strategy params only)
- [x] Phase 8: SCHEDULE sync with MATCHUP (_sync_schedule_params())
- [x] Phase 9: Unit tests (59 new tests, all 2281 tests pass)

### Deferred Tasks:
- Task 6.2: Create initial draft_config.json - [x] COMPLETE (2025-12-15)
- Task 9.4: Integration tests - [x] COMPLETE (15 tests in tests/integration/test_accuracy_simulation_integration.py)
- Task 10.1: Documentation - [x] COMPLETE (simulation/README.md updated)

### Files Created:
- `simulation/shared/` - ConfigGenerator, ResultsManager, ConfigPerformance, ProgressTracker, config_cleanup
- `simulation/win_rate/` - SimulationManager, ParallelLeagueRunner, SimulatedLeague, etc.
- `simulation/accuracy/` - AccuracyCalculator, AccuracyResultsManager, AccuracySimulationManager
- `run_win_rate_simulation.py` (renamed from run_simulation.py)
- `run_accuracy_simulation.py` (new)
- `run_win_rate_simulation_loop.sh` (renamed)
- `run_accuracy_simulation_loop.sh` (new)
- `tests/simulation/test_AccuracyCalculator.py` (21 tests)
- `tests/simulation/test_AccuracyResultsManager.py` (28 tests)
- `tests/simulation/test_AccuracySimulationManager.py` (10 tests)

**Blockers:** None
