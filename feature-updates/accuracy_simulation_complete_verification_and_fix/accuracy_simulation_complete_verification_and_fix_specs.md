# Accuracy Simulation - Complete Verification and Fix

## Problem Statement

The accuracy simulation system is fundamentally broken across multiple layers. After implementing the original accuracy simulation feature, the ConfigGenerator horizon fix, and investigating the 'both' mode behavior, it's become clear that the system requires comprehensive verification and repair.

**Critical Discovery:** All 16 parameters optimized by accuracy simulation are WEEK_SPECIFIC_PARAMS, meaning each horizon (ros, 1-5, 6-9, 10-13, 14-17) should optimize independently with its own parameter values. This fundamentally changes how the simulation must work.

---

## Background: What Has Been Implemented

### Phase 1: Original Accuracy Simulation (COMPLETED)
- Created AccuracySimulationManager, AccuracyCalculator, AccuracyResultsManager
- Implemented ROS mode (season-long accuracy evaluation)
- Implemented weekly mode (per-week accuracy evaluation)
- Implemented 'both' mode (sequential: ROS then weekly)
- Created 6-file config structure: league_config.json, draft_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json
- MAE (Mean Absolute Error) as accuracy metric

### Phase 2: ConfigGenerator Horizon Fix (COMPLETED)
- Refactored ConfigGenerator to support 5 separate horizon baselines
- Added generate_horizon_test_values() method
- Added get_config_for_horizon() method
- Added update_baseline_for_horizon() method
- Supports both shared params (BASE_CONFIG_PARAMS) and horizon-specific params (WEEK_SPECIFIC_PARAMS)
- Win-rate simulation updated to use new interface (optimizes shared params only)

### Phase 3: Fix 'both' Mode Behavior (PLANNED BUT PAUSED)
- Discovered fundamental misunderstanding about parameter types
- Realized 'both' mode sequential approach is wrong
- Identified that accuracy params are ALL week-specific (not shared)
- Need to verify entire system before proceeding with 'both' mode fix

---

## The Fundamental Issue

**Accuracy simulation optimizes WEEK_SPECIFIC_PARAMS, not BASE_CONFIG_PARAMS.**

From run_accuracy_simulation.py lines 71-88, all 16 parameters are week-specific:
- NORMALIZATION_MAX_SCALE
- TEAM_QUALITY_SCORING (WEIGHT + MIN_WEEKS)
- PERFORMANCE_SCORING (WEIGHT + STEPS + MIN_WEEKS)
- MATCHUP_SCORING (IMPACT_SCALE + WEIGHT + MIN_WEEKS)
- TEMPERATURE_SCORING (IMPACT_SCALE + WEIGHT)
- WIND_SCORING (IMPACT_SCALE + WEIGHT)
- LOCATION_MODIFIERS (HOME + AWAY + INTERNATIONAL)

**This means:**
- ConfigGenerator.generate_horizon_test_values() should return: `{'ros': [...], '1-5': [...], '6-9': [...], '10-13': [...], '14-17': [...]}`
- NOT `{'shared': [...]}`
- Each horizon has its own baseline value and test values
- Tournament model optimization: each horizon competes independently
- For parameter N+1: Generate test configs from 5 different base configs (one per horizon's previous best)

**Current behavior MAY be wrong:**
- Unclear if ROS/weekly modes are correctly using horizon-specific approach
- 'both' mode definitely wrong (sequential optimization)
- May be treating week-specific params as shared params
- May not be properly maintaining 5 independent optimization paths

---

## Scope of This Feature

**This feature will VERIFY and FIX the ENTIRE accuracy simulation system.**

### IN SCOPE:

**1. Verification Phase (Comprehensive Audit)**
- Verify ROS mode correctly uses horizon-specific parameters
- Verify weekly mode correctly uses horizon-specific parameters
- Verify ConfigGenerator integration is correct for week-specific params
- Verify results tracking for 5 independent horizons
- Verify intermediate/optimal folder saving (6 files with potentially different param values)
- Verify AccuracyCalculator MAE calculations are correct
- Verify PlayerManager integration for accuracy evaluation
- Verify that configs are generated from correct baselines
- Verify that each horizon maintains independent optimization path
- Document ALL issues found during verification

**2. Fix Phase (Implement Corrections)**
- Fix any issues found in ROS mode
- Fix any issues found in weekly mode
- Completely rewrite 'both' mode with correct per-config evaluation approach
- Fix config generation to properly handle 5 horizon baselines
- Fix results tracking if needed
- Add parallel processing (ProcessPoolExecutor, default 8 workers)
- Add --max-workers and --use-processes CLI flags
- Fix intermediate saving to occur once per parameter (not per new best)
- Ensure tournament model: each horizon optimizes from its own best config

**3. Testing Phase (Validation)**
- Run test simulations with small parameter sets
- Verify each mode produces valid output
- Verify 6-file output structure has correct values
- Verify different horizons can have different optimal parameter values
- Verify parallel processing works correctly
- Verify no config is evaluated twice unnecessarily
- Compare results to expected behavior

### OUT OF SCOPE:
- Changes to MAE calculation algorithm (already correct)
- Changes to PlayerManager scoring architecture
- Changes to win-rate simulation (already correct)
- New accuracy metrics beyond MAE
- UI/visualization improvements

---

## Expected Correct Behavior

### ROS Mode (run_ros_optimization)
**For each parameter in parameter_order:**
1. ConfigGenerator.generate_horizon_test_values(param_name) returns: `{'ros': [baseline, test1, test2, ...]}`
2. For each test_idx in test values:
   - Get config: config_generator.get_config_for_horizon('ros', param_name, test_idx)
   - Evaluate config for ROS accuracy (MAE calculation)
   - Track result with results_manager.add_result('ros', config, result, ...)
3. After all test values evaluated:
   - Identify best config for ROS horizon
   - Save intermediate folder with best draft_config.json
   - Update ConfigGenerator baseline: config_generator.update_baseline_for_horizon('ros', best_config)
4. Continue to next parameter

**Expected configs per parameter:** 1 baseline + N test values (e.g., 1 + 20 = 21 configs)

### Weekly Mode (run_weekly_optimization)
**For each parameter in parameter_order:**
1. ConfigGenerator.generate_horizon_test_values(param_name) returns:
   ```python
   {
       '1-5': [baseline, test1, test2, ...],
       '6-9': [baseline, test1, test2, ...],
       '10-13': [baseline, test1, test2, ...],
       '14-17': [baseline, test1, test2, ...]
   }
   ```
2. For each horizon in ['1-5', '6-9', '10-13', '14-17']:
   - For each test_idx in test values for this horizon:
     - Get config: config_generator.get_config_for_horizon(horizon, param_name, test_idx)
     - Evaluate config for this horizon's weekly accuracy
     - Track result with results_manager.add_result(horizon, config, result, ...)
   - After all test values evaluated for this horizon:
     - Identify best config for this horizon
     - Update ConfigGenerator baseline: config_generator.update_baseline_for_horizon(horizon, best_config)
3. After all 4 horizons tested:
   - Save intermediate folder with all 4 best week configs
4. Continue to next parameter

**Expected configs per parameter:** 4 horizons × (1 baseline + N test values) = 4 × 21 = 84 configs

### Both Mode (run_both) - TARGET CORRECT BEHAVIOR
**For each parameter in parameter_order:**
1. ConfigGenerator.generate_horizon_test_values(param_name) returns:
   ```python
   {
       'ros': [baseline_ros, test1_ros, test2_ros, ...],
       '1-5': [baseline_1_5, test1_1_5, test2_1_5, ...],
       '6-9': [baseline_6_9, test1_6_9, test2_6_9, ...],
       '10-13': [baseline_10_13, test1_10_13, test2_10_13, ...],
       '14-17': [baseline_14_17, test1_14_17, test2_14_17, ...]
   }
   ```
2. For each horizon in ALL_HORIZONS:
   - For each test_idx in test values for this horizon:
     - Get config: config_generator.get_config_for_horizon(horizon, param_name, test_idx)
     - Evaluate config across ALL 5 horizons (5 MAE calculations):
       ```python
       all_results = _evaluate_config_both(config)  # Returns dict with 5 AccuracyResults
       # all_results = {'ros': result_ros, '1-5': result_1_5, ...}
       ```
     - Record ALL 5 results:
       ```python
       for result_horizon, result in all_results.items():
           config_id = f"{param_name}_{test_idx}_horizon_{result_horizon}"
           results_manager.add_result(
               result_horizon,
               config,
               result,
               config_id=config_id,
               base_horizon=horizon,  # Which baseline was used
               param_name=param_name,
               test_idx=test_idx
           )
       ```
3. After all test values evaluated for ALL horizons:
   - Identify best config for EACH of 5 horizons independently
   - Save intermediate folder with all 6 files (league_config.json + 5 horizon files)
   - Update ConfigGenerator baselines for ALL 5 horizons with their respective best configs
4. Continue to next parameter

**Expected configs per parameter:** 5 horizons × (1 baseline + N test values) = 5 × 21 = 105 configs
**Expected MAE calculations per parameter:** 105 configs × 5 horizons each = 525 evaluations
**Key insight:** Each config is evaluated once but calculates MAE for all 5 horizons

### Tournament Model Explanation
**Parameter 1 (NORMALIZATION_MAX_SCALE):**
- All 5 horizons start from same baseline (first parameter)
- Test all configs, find best for each horizon
- Output: 5 configs with potentially different NORMALIZATION_MAX_SCALE values

**Parameter 2 (TEAM_QUALITY_SCORING_WEIGHT):**
- ROS tests: Start from draft_config.json (NORMALIZATION_MAX_SCALE=150, best for ROS from param 1)
- 1-5 tests: Start from week1-5.json (NORMALIZATION_MAX_SCALE=120, best for 1-5 from param 1)
- 6-9 tests: Start from week6-9.json (NORMALIZATION_MAX_SCALE=180, best for 6-9 from param 1)
- 10-13 tests: Start from week10-13.json (NORMALIZATION_MAX_SCALE=140, best for 10-13 from param 1)
- 14-17 tests: Start from week14-17.json (NORMALIZATION_MAX_SCALE=160, best for 14-17 from param 1)
- Generate 5 different sets of test configs (one per horizon's baseline)
- Each config evaluated across all 5 horizons
- Each horizon's "champion" competes to stay champion with new parameter value

---

## Technical Details

### Files to Verify/Modify

**Primary Files:**
1. `simulation/accuracy/AccuracySimulationManager.py`
   - run_ros_optimization() - verify correct horizon-specific behavior
   - run_weekly_optimization() - verify correct horizon-specific behavior
   - run_both() - COMPLETE REWRITE required
   - _evaluate_config_ros() - verify correct
   - _evaluate_config_weekly() - verify correct
   - _evaluate_config_both() - CREATE NEW (calls ros + 4 weekly)
   - Add parallel processing support
   - Add max_workers, use_processes parameters to __init__

2. `simulation/accuracy/AccuracyResultsManager.py`
   - verify add_result() handles 5 independent horizons
   - verify save_intermediate_results() creates 6-file structure correctly
   - verify save_optimal_configs() creates 6-file structure correctly
   - verify best config tracking per horizon
   - AccuracyConfigPerformance.is_better_than() - verify handles player_count=0
   - Add tournament metadata fields: base_horizon, param_name, test_idx

3. `simulation/accuracy/AccuracyCalculator.py`
   - verify calculate_ros_mae() is correct
   - verify calculate_weekly_mae() is correct
   - verify handles missing data gracefully

4. `run_accuracy_simulation.py`
   - Add --max-workers CLI flag (default: 8)
   - Add --use-processes / --no-use-processes flags (default: enabled)
   - Pass parameters to AccuracySimulationManager

**Supporting Files:**
5. `simulation/shared/ConfigGenerator.py`
   - verify generate_horizon_test_values() works correctly for week-specific params
   - verify get_config_for_horizon() returns correct merged configs
   - verify update_baseline_for_horizon() updates correctly for week-specific params
   - verify baseline_configs dict maintains 5 separate configs

6. `simulation/shared/ResultsManager.py` (base class)
   - verify WEEK_SPECIFIC_PARAMS list is complete and correct
   - verify BASE_CONFIG_PARAMS list is complete and correct

### Key Implementation Requirements

**1. Parallel Processing (from fix_both_mode_behavior notes)**
- Use ProcessPoolExecutor for true parallelism (bypasses GIL)
- Module-level function `_evaluate_config_both_process()` for pickling
- Default: 8 workers, ProcessPoolExecutor enabled
- ThreadPoolExecutor fallback option (--no-use-processes)

**2. Intermediate Saving (from fix_both_mode_behavior notes)**
- Save ONCE per parameter after all configs tested (not after each new best)
- Match win-rate simulation pattern
- All 5 horizons must have valid best configs before saving

**3. Config ID Format (from fix_both_mode_behavior notes)**
- Use win-rate format: `{param_name}_{test_idx}_horizon_{result_horizon}`
- Parseable with regex: `r'_(\d+)_horizon_'`
- Examples: `NORMALIZATION_MAX_SCALE_0_horizon_ros`, `TEAM_QUALITY_SCORING_WEIGHT_4_horizon_1-5`

**4. Tournament Metadata (from fix_both_mode_behavior notes)**
- Add to AccuracyConfigPerformance: base_horizon, param_name, test_idx
- Useful for debugging which baseline config was used
- Track optimization history

**5. Error Handling**
- AccuracyConfigPerformance.is_better_than() must reject player_count=0
- Handle horizons with no valid players gracefully
- Don't mark invalid configs as optimal

---

## Verification Protocol

### Phase 1: Code Review (Manual Verification)
1. Read run_ros_optimization() line by line
   - Does it use generate_horizon_test_values() correctly?
   - Does it call get_config_for_horizon('ros', ...) for each test?
   - Does it update baseline for 'ros' horizon only?
   - Does it save only draft_config.json?

2. Read run_weekly_optimization() line by line
   - Does it iterate all 4 weekly horizons?
   - Does it use generate_horizon_test_values() correctly?
   - Does it call get_config_for_horizon() with correct horizon?
   - Does it update baselines for each horizon independently?
   - Does it save all 4 week configs?

3. Read run_both() line by line
   - Does it currently do sequential optimization? (WRONG)
   - Document exact current behavior
   - Design correct replacement

4. Read ConfigGenerator integration
   - How does AccuracySimulationManager call ConfigGenerator?
   - Are week-specific params handled correctly?
   - Are 5 baselines maintained separately?

5. Read results tracking
   - Does AccuracyResultsManager track 5 independent best configs?
   - Is intermediate saving correct?
   - Are all 6 files saved with correct values?

### Phase 2: Test Run (Small Parameter Set)
1. Create test baseline config folder
2. Run ROS mode with 1 parameter, 2 test values
   - Verify generates correct number of configs (3 total)
   - Verify output draft_config.json has optimal value
   - Verify intermediate folder created correctly

3. Run weekly mode with 1 parameter, 2 test values
   - Verify generates correct number of configs (12 total: 4 horizons × 3 values)
   - Verify output week files have optimal values (may differ per horizon)
   - Verify intermediate folder created correctly

4. Run both mode with 1 parameter, 2 test values (AFTER rewrite)
   - Verify generates correct number of configs (15 total: 5 horizons × 3 values)
   - Verify each config evaluated across all 5 horizons
   - Verify no config evaluated twice
   - Verify output folder has all 6 files with correct values
   - Verify different horizons CAN have different optimal values

### Phase 3: Integration Test (Full Parameter Order)
1. Run full accuracy simulation with 3 test values per parameter
2. Monitor for errors
3. Verify convergence to reasonable parameter values
4. Compare ROS vs weekly vs both mode outputs
5. Verify both mode finds parameters that work well across all horizons

---

## Success Criteria

**Code-Level:**
- [ ] All verification steps completed and documented
- [ ] All identified issues fixed
- [ ] run_both() completely rewritten with per-config evaluation
- [ ] Parallel processing implemented (ProcessPoolExecutor, 8 workers default)
- [ ] CLI flags added (--max-workers, --use-processes)
- [ ] Intermediate saving happens once per parameter
- [ ] Tournament metadata tracked in results
- [ ] Config ID format matches win-rate pattern
- [ ] Error handling for player_count=0 implemented

**Behavioral:**
- [ ] ROS mode generates correct number of configs per parameter
- [ ] Weekly mode generates correct number of configs per parameter
- [ ] Both mode generates correct number of configs per parameter
- [ ] Each config in both mode evaluated exactly once (5 MAE calculations per config)
- [ ] No duplicate config evaluations
- [ ] Output folders contain all 6 files
- [ ] Different horizons can have different optimal parameter values
- [ ] Optimization follows tournament model (each horizon from own best)

**Performance:**
- [ ] Parallel processing utilizes all CPU cores
- [ ] ProcessPoolExecutor bypasses GIL for MAE calculations
- [ ] Reasonable runtime for full parameter order (estimate and document)

**Testing:**
- [ ] All unit tests pass
- [ ] Small test run (1 param, 2 values) succeeds for all modes
- [ ] Full simulation run completes without errors
- [ ] Output configs are reasonable and usable

---

## Notes from Previous Features

### From accuracy_simulation feature:
- MAE is the correct accuracy metric (lower is better)
- Calculated projected points found via PlayerManager.score_player()
- Point normalization must be reversed to get "calculated projected points"
- Separate ROS accuracy (season-long) from weekly accuracy (per-week)
- draft_config.json is NEW file for Add to Roster Mode
- week*.json files used by Starter Helper and Trade Simulator

### From fix_config_generator_horizon_behavior feature:
- ConfigGenerator now supports 5 separate baseline_configs (one per horizon)
- generate_horizon_test_values() returns dict with 'shared' key OR horizon keys
- get_config_for_horizon() merges league_config + horizon-specific config
- update_baseline_for_horizon() updates all horizons for shared params, one horizon for week-specific
- Win-rate sim optimizes BASE_CONFIG_PARAMS (shared)
- Accuracy sim optimizes WEEK_SPECIFIC_PARAMS (horizon-specific)

### From fix_both_mode_behavior investigation:
- Current both mode is WRONG (sequential optimization)
- Should evaluate each config across all 5 horizons
- Should save once per parameter, not per new best
- Should use parallel processing
- Should track tournament metadata
- All 16 accuracy params are WEEK_SPECIFIC (critical insight!)

---

## ⚠️ MAJOR SCOPE CHANGE (2025-12-17)

**User Decision: ROS and Weekly modes will be DEPRECATED.**

The accuracy simulation will ONLY support the tournament optimization model (previously called 'both' mode). This simplifies everything significantly.

---

## Resolved Implementation Decisions

All open questions have been resolved during the planning phase. See `accuracy_simulation_complete_verification_and_fix_checklist.md` for detailed resolutions. Key decisions:

### Architecture Decisions

1. **Mode Deprecation**: ROS and weekly modes are deprecated. Only tournament mode remains.
2. **6-File Structure**: Required - no backward compatibility with old structures (Q39)
3. **Resume Capability**: YES - implement auto-resume using existing _detect_resume_state() pattern (Q8)
4. **Error Handling**: Fail-fast - raise exceptions immediately on errors (Q10, Q12)
5. **Config Validation**: Use existing ConfigGenerator validation - no separate script needed (Q41)

### Performance Decisions

6. **Runtime Target**: No specific target - optimize for speed (continuous optimization loop) (Q21)
7. **Parallel Processing**: YES - ProcessPoolExecutor with 8 workers default (Q13)
8. **Progress Tracking**: Use MultiLevelProgressTracker (outer: configs, inner: horizons, overall: ETA) (Q22)
9. **Intermediate Saving**: Once per parameter after all horizons tested (Q26)
10. **Default Test Values**: Keep 20 test values (525 evaluations per parameter = 105 configs × 5 horizons)

### Implementation Details

11. **Module-Level Function**: Create separate ParallelAccuracyRunner.py file (Q15)
12. **Worker Parameters**: Pass explicit parameters (no shared ConfigGenerator) (Q16)
13. **Progress Integration**: Use existing ProgressTracker with callbacks (Q17)
14. **CLI Updates**: Add constants for defaults, remove mode argument, add --log-level flag (Q18, Q19, Q44)
15. **Folder Naming**: Simple naming (accuracy_intermediate_XX_PARAM_NAME) with metadata.json (Q24)

### Logging & Metadata

16. **Logging Strategy**: Log new bests during optimization + parameter summary after completion (Q25, Q44)
17. **Log Levels**: Add --log-level flag with systematic review (debug: all evals, info: new bests) (Q44)
18. **Metadata Tracking**: Add metadata.json in intermediate folders with param info and best MAEs (Q28, Q29, Q30)
19. **Config IDs**: Internal-only tracking, no regex constraints (Q27)

### Testing Strategy

20. **Test Fixtures**: Create tests/fixtures/accuracy_test_baseline/ with mock configs (Q31)
21. **Test Coverage**: Minimum 2 parameters to validate progression and baseline updates (Q32)
22. **Test Data**: Synthetic for unit tests, real (simulation/sim_data/) for integration tests (Q33)
23. **Divergence Testing**: Unit test with mocked MAE + manual QA verification (Q34)
24. **Old Configs**: Ignore old ROS/weekly configs - clean break, no migration (Q40)

### Bug Fixes

25. **is_better_than()**: Fix to reject player_count=0 configs (Q11)
26. **Intermediate Saving**: Fix ROS mode to save once per parameter (not per new best)
27. **Tournament Mode**: Complete rewrite of run_both() for per-parameter optimization (Q7, Q9)

---

## Implementation Priority

Based on planning phase audit, implement in this order:

1. **Phase 1: Core Fixes** (Critical path)
   - Fix is_better_than() to check player_count=0 (Q11)
   - Fix intermediate saving timing in ROS mode (Q26)
   - Create test fixtures (Q31-Q33)

2. **Phase 2: Tournament Rewrite** (Core feature)
   - Complete rewrite of run_both() for tournament model (Q7)
   - Implement per-parameter optimization across all 5 horizons (Q9)
   - Add metadata tracking (Q28-Q30)

3. **Phase 3: Parallel Processing** (Performance enhancement)
   - Create ParallelAccuracyRunner.py (Q15)
   - Implement module-level evaluation function (Q13)
   - Add MultiLevelProgressTracker integration (Q17, Q22)

4. **Phase 4: CLI & Logging** (Observability)
   - Add --log-level flag and systematic logging review (Q44)
   - Update CLI constants and remove mode argument (Q18, Q19)
   - Add --max-workers flag (Q13)

5. **Phase 5: Testing & Validation** (Quality assurance)
   - Unit tests with mocked MAE for divergence (Q34)
   - Integration tests with 2 parameters (Q32)
   - Manual QA verification (Q34)

---

## Expected Outcomes

After this feature is complete:

1. **Tournament optimization will be fully functional:**
   - Tournament mode (only mode) correctly evaluates each config across all 5 horizons simultaneously
   - Each parameter optimizes across ALL 5 horizons before moving to next parameter
   - Each horizon maintains independent optimization path
   - Parameter N+1 uses parameter N's best config as baseline (per horizon)
   - Different horizons can discover different optimal parameter values

2. **Performance will be optimized:**
   - Parallel processing utilizes all CPU cores (ProcessPoolExecutor with 8 workers)
   - ProcessPoolExecutor bypasses GIL for true parallelism
   - MultiLevelProgressTracker shows real-time progress and ETA
   - Runs continuously in optimization loop for parameter convergence

3. **Output will be correct:**
   - All 6 files saved with appropriate parameter values (league_config + 5 horizon configs)
   - Different horizons may have different values (tournament winners)
   - Intermediate folders track optimization progress with metadata.json
   - Metadata includes param info, best MAEs per horizon, timestamps

4. **Observability will be comprehensive:**
   - --log-level flag controls verbosity (debug: all evals, info: new bests + summaries)
   - New bests logged during optimization
   - Parameter summaries logged after completion showing all 5 horizon results
   - Progress tracking with ETA for both config-level and overall optimization

5. **Code will be maintainable:**
   - Clean separation: ParallelAccuracyRunner.py for parallel processing
   - Comprehensive error handling (fail-fast on errors, reject player_count=0)
   - Tournament metadata tracking for debugging
   - Good logging at appropriate levels
   - Documented behavior and expectations
   - ROS/weekly modes kept for reference but deprecated

6. **Testing will be robust:**
   - Test fixtures in tests/fixtures/accuracy_test_baseline/
   - Unit tests with mocked MAE for divergence scenarios
   - Integration tests with 2 parameters validating progression
   - Both synthetic (unit) and real (integration) test data
