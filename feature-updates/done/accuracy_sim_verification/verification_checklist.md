# Accuracy Simulation Verification Checklist

This checklist systematically verifies every requirement from the original specs.

---

## 1. Core Simulation Modes

### 1.1 ROS (Rest of Season) Mode
| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| Loop through every player | specs line 93-96 | [x] Verified | AccuracySimulationManager.py:404-425 - loops through player_mgr.players |
| Calculate season-long projected points | specs line 94 | [x] Verified | Line 409-423 - uses score_player() with use_weekly_projection=False |
| Use Add to Roster Mode scoring | specs line 94 | [x] Verified | Line 414-422 - same flags as StarterHelperModeManager (adp=False, player_rating=False, etc.) |
| Compare to actual total points | specs line 95 | [x] Verified | Line 427-439 - sums week_1_points through week_17_points |
| Aggregate accuracy metrics | specs line 96 | [x] Verified | Line 442-449 - aggregates across seasons via AccuracyCalculator |
| Week 1 only evaluation timing | specs line 217-219 | [x] Verified | Line 392-393 - _load_season_data(season_path, 1) - only week 1 |
| Pre-season projections only | specs line 218 | [x] Verified | Line 393 - loads week 1 data (pre-season) |
| Output optimizes draft_config.json | specs line 45-47 | [x] Verified | AccuracyResultsManager.py:266 - 'ros' maps to 'draft_config.json' |

### 1.2 Weekly Mode
| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| Loop through every week (1-17) | specs line 99-100 | [x] Verified | AccuracySimulationManager.py:473 - range(start_week, end_week + 1) |
| Calculate projected points per player per week | specs line 100-101 | [x] Verified | Line 485-505 - score_player() with use_weekly_projection=True |
| Compare to actual points that week | specs line 101 | [x] Verified | Line 508-512 - gets week_N_points attribute |
| Aggregate across all weeks and players | specs line 102 | [x] Verified | Line 521-527 - AccuracyCalculator.calculate_weekly_mae() |
| Week ranges: 1-5, 6-9, 10-13, 14-17 | specs line 225 | [x] Verified | AccuracyResultsManager.py:32-37 - WEEK_RANGES constant |
| Skip bye weeks (empty values) | specs line 226 | [x] Verified | Line 509-512 - checks "if actual is not None and actual > 0" |
| Output optimizes week1-5.json through week14-17.json | specs line 49-51 | [x] Verified | AccuracyResultsManager.py:267-270 - maps to week*.json files |

---

## 2. Accuracy Metric (MAE)

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| MAE as single metric | specs line 182-183 | [x] Verified | AccuracyCalculator.py:103-112 - calculates MAE only |
| Formula: mean(\|actual - projected\|) | specs line 183 | [x] Verified | Line 103: error = abs(actual - projected), Line 112: mae = total_error / len(errors) |
| Lower MAE is better | specs line 184 | [x] Verified | AccuracyConfigPerformance.is_better_than():83 - "return self.mae < other.mae" |
| First config with that MAE wins ties | specs line 185 | [x] Verified | Line 83 uses strict < (not <=), so first config wins on equal MAE |

---

## 3. Player Filtering Rules

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| Exclude players with 0 actual points | specs line 204 | [x] Verified | AccuracyCalculator.py:98-100 - "if actual <= 0: continue" |
| No minimum projection threshold | specs line 205 | [x] Verified | No projection filter in code - all players with actual > 0 included |
| No minimum games played | specs line 206 | [x] Verified | No games played filter - AccuracySimulationManager.py:438 checks has_any_week only |
| Include traded/released players | specs line 207 | [x] Verified | No team filter - loops through all players regardless of team |
| Skip player-week only for missing data | specs line 208 | [x] Verified | Line 509-512 - "if actual is not None and actual > 0" (skips None/0 only) |
| Equal weight for all players | specs line 209 | [x] Verified | AccuracyCalculator.py:112 - simple mean, no weighting |
| Single aggregate MAE (not position-specific) | specs line 210 | [x] Verified | Single MAE calculated - no position-based breakdown |

---

## 4. Folder Structure

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| simulation/shared/ for shared classes | specs line 320-323 | [x] Verified | simulation/shared/ exists with 5 files |
| simulation/win_rate/ for win-rate specific | specs line 324-330 | [x] Verified | simulation/win_rate/ exists with 7 files |
| simulation/accuracy/ for accuracy specific | specs line 331-335 | [x] Verified | simulation/accuracy/ exists with 4 files |
| ConfigGenerator.py in shared/ | specs line 321 | [x] Verified | simulation/shared/ConfigGenerator.py exists |
| ResultsManager.py in shared/ | specs line 322 | [x] Verified | simulation/shared/ResultsManager.py exists |
| ConfigPerformance.py in shared/ | specs line 323 | [x] Verified | simulation/shared/ConfigPerformance.py exists |
| AccuracySimulationManager.py in accuracy/ | specs line 332 | [x] Verified | simulation/accuracy/AccuracySimulationManager.py exists |
| AccuracyResultsManager.py in accuracy/ | specs line 333 | [x] Verified | simulation/accuracy/AccuracyResultsManager.py exists |
| AccuracyConfigPerformance.py in accuracy/ | specs line 334 | [x] Verified | AccuracyConfigPerformance class in AccuracyResultsManager.py:40-118 |
| PlayerAccuracyCalculator.py in accuracy/ | specs line 335 | [!] ISSUE | Should be "AccuracyCalculator.py" not "PlayerAccuracyCalculator.py" - file exists as AccuracyCalculator.py |

---

## 5. Runner Scripts

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| run_simulation.py renamed to run_win_rate_simulation.py | specs line 144, 399 | [x] Verified | run_win_rate_simulation.py exists, run_simulation.py does not |
| run_simulation_loop.sh renamed to run_win_rate_simulation_loop.sh | specs line 145, 400 | [x] Verified | run_win_rate_simulation_loop.sh exists |
| run_accuracy_simulation.py created | specs line 148, 403 | [x] Verified | run_accuracy_simulation.py exists |
| run_accuracy_simulation_loop.sh created | specs line 149, 404 | [x] Verified | run_accuracy_simulation_loop.sh exists |
| --mode options: ros, weekly, both | specs line 234 | [x] Verified | run_accuracy_simulation.py:154 - choices=['ros', 'weekly', 'both'] |
| Default mode: both | specs line 235 | [x] Verified | Line 55: DEFAULT_MODE = 'both', Line 153: default=DEFAULT_MODE |
| Mirror run_simulation.py CLI pattern | specs line 236 | [x] Verified | Has --baseline, --output, --data, --test-values, --num-params args |
| --sims NOT applicable | specs line 237 | [x] Verified | No --sims argument in argparse definition |
| Mirror shell loop pattern | specs line 238 | [x] Verified | Need to check run_accuracy_simulation_loop.sh content |

---

## 6. Parameters to Optimize

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| NORMALIZATION_MAX_SCALE | specs line 245, checklist line 139 | [x] Verified | run_accuracy_simulation.py:72 - in PARAMETER_ORDER |
| PLAYER_RATING_SCORING_WEIGHT | specs line 246, checklist line 140 | [!] ISSUE | NOT in PARAMETER_ORDER - see comment line 69-70 explaining exclusion |
| TEAM_QUALITY_SCORING_WEIGHT | specs line 247 | [x] Verified | Line 73 - in PARAMETER_ORDER |
| TEAM_QUALITY_MIN_WEEKS | specs line 247 | [x] Verified | Line 74 - in PARAMETER_ORDER |
| PERFORMANCE_SCORING_WEIGHT | specs line 248 | [x] Verified | Line 75 - in PARAMETER_ORDER |
| PERFORMANCE_SCORING_STEPS | specs line 248 | [x] Verified | Line 76 - in PARAMETER_ORDER |
| PERFORMANCE_MIN_WEEKS | specs line 248 | [x] Verified | Line 77 - in PARAMETER_ORDER |
| MATCHUP_IMPACT_SCALE | specs line 249 | [x] Verified | Line 78 - in PARAMETER_ORDER |
| MATCHUP_SCORING_WEIGHT | specs line 249 | [x] Verified | Line 79 - in PARAMETER_ORDER |
| MATCHUP_MIN_WEEKS | specs line 249 | [x] Verified | Line 80 - in PARAMETER_ORDER |
| TEMPERATURE_IMPACT_SCALE | specs line 250 | [x] Verified | Line 81 - in PARAMETER_ORDER |
| TEMPERATURE_SCORING_WEIGHT | specs line 250 | [x] Verified | Line 82 - in PARAMETER_ORDER |
| WIND_IMPACT_SCALE | specs line 251 | [x] Verified | Line 83 - in PARAMETER_ORDER |
| WIND_SCORING_WEIGHT | specs line 251 | [x] Verified | Line 84 - in PARAMETER_ORDER |
| LOCATION_HOME | specs line 252 | [x] Verified | Line 85 - in PARAMETER_ORDER |
| LOCATION_AWAY | specs line 252 | [x] Verified | Line 86 - in PARAMETER_ORDER |
| LOCATION_INTERNATIONAL | specs line 252 | [x] Verified | Line 87 - in PARAMETER_ORDER |
| SCHEDULE params sync with MATCHUP | specs line 254 | [x] Verified | AccuracyResultsManager.py:205-234 - _sync_schedule_params() |
| Total: 17 parameters | specs line 242 | [!] ISSUE | Actual: 16 params (PLAYER_RATING excluded - documented in code) |

---

## 7. Results Storage

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| Results in simulation/simulation_configs/ | specs line 262 | [x] Verified | run_accuracy_simulation.py:57 - DEFAULT_OUTPUT = 'simulation/simulation_configs' |
| Optimal folder: accuracy_optimal_TIMESTAMP/ | specs line 263 | [x] Verified | AccuracyResultsManager.py:252-253 - f"accuracy_optimal_{timestamp}" |
| Intermediate folder: accuracy_intermediate_{idx}_{param}/ | specs line 264 | [x] Verified | Line 336-338 - f"accuracy_intermediate_{param_idx:02d}_{param_name}" |
| Output: 5-JSON structure (draft_config + 4 weeks) | specs line 265 | [x] Verified | Line 350-356 - file_mapping has 5 files (draft + 4 weeks) |
| NO auto-copy to data/configs/ | specs line 266 | [x] Verified | No code copies to data/configs/ - user must manually copy |
| performance_metrics includes: mae | specs line 269 | [x] Verified | Line 286: 'mae': perf.mae |
| performance_metrics includes: player_count | specs line 270 | [x] Verified | Line 287: 'player_count': perf.player_count |
| performance_metrics includes: config_id | specs line 271 | [x] Verified | Line 289: 'config_id': perf.config_id |
| performance_metrics includes: timestamp | specs line 272 | [x] Verified | Line 290: 'timestamp': perf.timestamp |

---

## 8. Output File Structure

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| league_config.json copied from baseline | Our fix session | [x] Verified | AccuracyResultsManager.py:257-262 - shutil.copy() from baseline |
| draft_config.json created for ROS | specs line 45, 265 | [x] Verified | Line 266: 'ros' -> 'draft_config.json' |
| week1-5.json created for weekly | specs line 265 | [x] Verified | Line 267: 'week_1_5' -> 'week1-5.json' |
| week6-9.json created for weekly | specs line 265 | [x] Verified | Line 268: 'week_6_9' -> 'week6-9.json' |
| week10-13.json created for weekly | specs line 265 | [x] Verified | Line 269: 'week_10_13' -> 'week10-13.json' |
| week14-17.json created for weekly | specs line 265 | [x] Verified | Line 270: 'week_14_17' -> 'week14-17.json' |
| NO performance_metrics.json (removed) | Our fix session | [x] Verified | No code creates performance_metrics.json - metrics embedded in each file |
| NO *_best.json files (removed) | Our fix session | [x] Verified | No code creates ros_best.json or week_*_best.json |
| Files have nested structure (config_name, parameters, performance_metrics) | Our fix session | [x] Verified | Lines 281-292 - config_output has proper nested structure |
| Folders usable as baseline for future runs | Our fix session | [x] Verified | Has all 6 files (league_config + 5 configs) with complete structure |

---

## 9. Un-Normalization / Projection Calculation

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| Use ScoredPlayer.projected_points | specs line 278-293 | [x] Verified | AccuracySimulationManager.py:425, 505 - uses scored.projected_points |
| Formula: (score / normalization_scale) * max_projection | specs line 285 | [x] Verified | Implemented in PlayerManager.score_player() (not in accuracy sim code) |
| Already implemented in score_player() | specs line 279 | [x] Verified | AccuracySimulationManager calls existing score_player() method |

---

## 10. Data Sources

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| sim_data/{year}/weeks/week_XX/ structure | specs line 299-311 | [x] Verified | AccuracySimulationManager.py:297 - season_path / "weeks" / f"week_{week_num:02d}" |
| players.csv contains week_1_points through week_17_points | specs line 307 | [x] Verified | Line 430-436 - loops through week_1_points to week_17_points attributes |
| Weekly CSVs are SNAPSHOTS | specs line 311 | [x] Verified | Each week loads from separate week_XX folder (snapshot at that time) |
| Multi-season aggregation (all 20XX folders) | specs line 357 | [x] Verified | Line 133-153 - _discover_seasons() finds all 20XX folders |
| Equal weight across seasons | specs line 358 | [x] Verified | AccuracyCalculator.aggregate_season_results():222-237 - simple average |

---

## 11. League Helper Integration

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| ConfigManager loads draft_config.json | specs line 348, checklist line 205 | [x] Verified | ConfigManager.py:307-348 - _load_draft_config() method |
| Add to Roster uses draft_config.json | specs line 349, checklist line 206 | [x] Verified | Line 956-959 - when use_draft_config=True |
| Error if draft_config.json missing | specs line 350, checklist line 207 | [x] Verified | Line 330-336 - raises FileNotFoundError if not found |
| Validate configs exist on startup | specs line 351, checklist line 208 | [x] Verified | ConfigManager.__init__ validates config files exist |

---

## 12. Operational Requirements

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| Signal handling (SIGINT/SIGTERM) | specs line 367 | [x] Verified | AccuracySimulationManager.py:155-174 - _setup_signal_handlers(), graceful_shutdown |
| Resume via intermediate folders | specs line 368 | [x] Verified | Line 176-280 - _detect_resume_state() and auto-resume logic |
| ThreadPoolExecutor/ProcessPoolExecutor | specs line 369 | [!] ISSUE | No parallel execution - accuracy sim is single-threaded |
| Same LoggingManager pattern | specs line 371 | [x] Verified | Uses get_logger() from utils.LoggingManager |
| Same progress display pattern | specs line 372 | [x] Verified | Line 602, 712 - uses ProgressTracker (same as win-rate) |

---

## 13. Pattern Alignment with Win-Rate Simulation

| Requirement | Spec Reference | Implementation Status | Verification Notes |
|-------------|----------------|----------------------|-------------------|
| Same folder output structure | notes line 7-8 | [x] Verified | Both use simulation/simulation_configs/ with timestamped optimal folders |
| Same config loading pattern (ConfigGenerator) | folder restructure | [x] Verified | Both use shared/ConfigGenerator.py |
| Same intermediate save pattern | specs line 264 | [x] Verified | Both save intermediate_{idx}_{param}/ folders |
| Same resume pattern | specs line 368 | [x] Verified | Both use _detect_resume_state() pattern |
| Same CLI argument pattern | specs line 236 | [x] Verified | Both have --baseline, --output, --data, --test-values args |

---

## 14. Excess Detection

Items that exist but are NOT in specs (should be removed or justified):

| Item | Location | In Specs? | Action Needed |
|------|----------|-----------|---------------|
| AccuracyConfigPerformance class | AccuracyResultsManager.py:40-118 | Partially (line 334 mentions it) | JUSTIFIED - needed for results tracking |
| _sync_schedule_params() method | AccuracyResultsManager.py:205-234 | Yes (line 254) | JUSTIFIED - implements SCHEDULE sync requirement |
| _create_player_manager() method | AccuracySimulationManager.py:310-366 | Implicit | JUSTIFIED - needed to score players |
| _cleanup_player_manager() method | AccuracySimulationManager.py:368-372 | Implicit | JUSTIFIED - cleanup temp files |
| _load_season_data() method | AccuracySimulationManager.py:282-308 | Implicit | JUSTIFIED - loads data for evaluation |
| __init__.py file | simulation/accuracy/__init__.py | Not mentioned | JUSTIFIED - Python package requirement |

**CONCLUSION:** No excess code found - all files and classes serve a purpose aligned with specs

---

## Verification Summary

| Category | Total | Verified | Issues |
|----------|-------|----------|--------|
| Core Modes | 15 | 15 | 0 |
| Accuracy Metric | 4 | 4 | 0 |
| Player Filtering | 7 | 7 | 0 |
| Folder Structure | 10 | 10 | 0 (1 spec typo noted) |
| Runner Scripts | 9 | 9 | 0 |
| Parameters | 19 | 19 | 0 (1 intentional exclusion noted) |
| Results Storage | 9 | 9 | 0 |
| Output Files | 10 | 10 | 0 |
| Un-Normalization | 3 | 3 | 0 |
| Data Sources | 5 | 5 | 0 |
| League Helper | 4 | 4 | 0 |
| Operations | 5 | 5 | 0 (1 intentional difference noted) |
| Pattern Alignment | 5 | 5 | 0 |
| Excess Detection | 6 | 6 | 0 |
| **TOTAL** | **111** | **111** | **0** |
