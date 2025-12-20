# Accuracy Simulation Complete Verification and Fix - Requirements Checklist

> **Note:** Items marked [x] are resolved. Items marked [ ] need investigation or user decision.

---

## ⚠️ MAJOR SCOPE CHANGE (2025-12-17): ROS/Weekly Modes DEPRECATED

**User Decision:** Only tournament optimization mode (formerly 'both') will be supported going forward.

**Impact on Questions:**
- Q1-Q6: ROS/weekly specific questions → **MOOT** (modes deprecated)
- Q42-Q43: Scope boundary questions for ROS/weekly → **MOOT**
- All other questions remain relevant to tournament optimization implementation

---

## THREE-ITERATION Question Generation

### Iteration 1: Core Implementation & Edge Cases

**ROS Mode Verification:** [DEPRECATED - QUESTIONS MOOT]
1. **Q1**: ~~ROS mode intermediate saving - does it save after EACH new best or ONCE per parameter?~~ **MOOT**
2. **Q2**: ~~ROS mode with 0 players for a season - does AccuracyCalculator handle gracefully?~~ **STILL RELEVANT** (applies to tournament mode)
3. **Q3**: ~~ROS mode auto-resume - if interrupted mid-parameter, does it correctly resume from last complete parameter?~~ **MOOT** (but auto-resume concept applies to tournament mode)

**Weekly Mode Verification:** [DEPRECATED - QUESTIONS MOOT]
4. **Q4**: ~~Weekly mode intermediate folder naming uses `week_key` prefix - does this break resume detection?~~ **MOOT**
5. **Q5**: ~~Weekly mode optimizes ALL parameters for EACH week range - is this the intended behavior or should it be inverted (each parameter across all weeks)?~~ **MOOT** (tournament mode uses parameter-first)
6. **Q6**: ~~Weekly mode saves intermediate after each parameter per week range - should it save once per parameter after all 4 week ranges tested?~~ **MOOT** (but answer applies to tournament mode)

**Both Mode Implementation:**
7. **Q7**: Should 'both' mode rewrite completely replace run_both() or add a new method (e.g., run_both_tournament())?
8. **Q8**: Should 'both' mode support the same auto-resume capability as ROS/weekly modes?
9. **Q9**: For 'both' mode per-config evaluation, should _evaluate_config_both() be instance method or module-level function?

**Error Handling:**
10. **Q10**: If one horizon fails during 'both' mode evaluation (exception), should we skip that horizon's result or fail entire config?
11. **Q11**: AccuracyConfigPerformance.is_better_than() with player_count=0 - is this already fixed or needs fixing?
12. **Q12**: What happens if ConfigGenerator.generate_horizon_test_values() returns empty array for a horizon?

### Iteration 2: Parallel Processing & Performance

**Parallel Processing Design:**
13. **Q13**: Should parallel processing be added to ALL modes (ROS, weekly, both) or just 'both' mode?
14. **Q14**: ProcessPoolExecutor requires pickle - does AccuracyCalculator pickle correctly (stateless except logger)?
15. **Q15**: Module-level function for ProcessPoolExecutor - should it be in AccuracySimulationManager.py or separate file?
16. **Q16**: How should parallel workers handle the data_folder and available_seasons parameters?
17. **Q17**: Should progress tracking use tqdm or similar for visibility with parallel execution?

**CLI & Configuration:**
18. **Q18**: --max-workers and --use-processes flags - should they have defaults in run_accuracy_simulation.py constants or only as CLI args?
19. **Q19**: Should there be a --mode flag to select ros/weekly/both, or keep current positional argument?
20. **Q20**: Is there a --resume flag or is auto-resume always enabled?

**Performance Considerations:**
21. **Q21**: With 105 configs × 5 horizons = 525 MAE calculations per parameter in 'both' mode, what's acceptable runtime?
22. **Q22**: Should we add progress estimation/ETA logging for long-running optimizations?
23. **Q23**: ConfigGenerator caching - is it safe in parallel execution or does it need thread-safety?

### Iteration 3: Integration & Testing

**Results & Output:**
24. **Q24**: Should intermediate folders for 'both' mode use a different naming scheme than ROS/weekly?
25. **Q25**: How should performance metrics be logged in 'both' mode (5 MAE values per config)?
26. **Q26**: Should save_intermediate_results() be called per parameter or per horizon per parameter in 'both' mode?
27. **Q27**: Config ID format `{param}_{idx}_horizon_{horizon}` - does this work with existing regex patterns for resume detection?

**Tournament Metadata:**
28. **Q28**: Tournament metadata (base_horizon, param_name, test_idx) - add to AccuracyConfigPerformance now or during 'both' mode rewrite?
29. **Q29**: Should metadata be saved to JSON output files or just kept in memory?
30. **Q30**: Is metadata needed for ROS/weekly modes or only 'both' mode?

**Testing Strategy:**
31. **Q31**: Should we create a test baseline config with small parameter ranges for faster verification?
32. **Q32**: What's the minimum test: 1 parameter with how many test values?
33. **Q33**: Should test runs use real historical season data or synthetic/minimal data?
34. **Q34**: How to verify that different horizons CAN find different optimal values (test with known divergent case)?

**Integration Verification:**
35. **Q35**: Does AccuracyCalculator.calculate_ros_mae() correctly reverse point normalization?
36. **Q36**: Does AccuracyCalculator.calculate_weekly_mae() correctly handle weekly data?
37. **Q37**: PlayerManager temp directory cleanup - verified to work correctly in parallel?
38. **Q38**: Are there any shared state issues in AccuracyCalculator or PlayerManager that would break parallelism?

**Backward Compatibility:**
39. **Q39**: Should we maintain backward compatibility with old 5-file structure or require 6-file structure?
40. **Q40**: If old optimal configs exist, how to migrate or warn user?
41. **Q41**: Should there be a validation script to check config folder structure before running?

**Scope Boundaries:**
42. **Q42**: ~~Is fixing the weekly mode folder naming (`week_key` prefix) in scope or defer to separate fix?~~ **MOOT** (weekly mode deprecated)
43. **Q43**: ~~Should we optimize the weekly mode execution order (parameter-first vs week-first) or leave as-is?~~ **MOOT** (weekly mode deprecated)
44. **Q44**: Is adding logging improvements (debug vs info levels) in scope or separate enhancement?

---

## Checklist Items (Categorized)

### A. Verification Questions (What exists now) - UPDATED FOR SCOPE CHANGE
- [MOOT] **Q1**: ~~ROS mode saves intermediate~~ - ROS mode deprecated
- [x] **Q2**: AccuracyCalculator returns safe default with player_count=0 (line 107-109 - CORRECT) [VERIFIED]
- [MOOT] **Q3**: ~~ROS mode has auto-resume~~ - ROS mode deprecated (but tournament mode WILL need auto-resume)
- [MOOT] **Q4**: ~~Weekly folder naming~~ - Weekly mode deprecated
- [x] **Q11**: is_better_than() needs fix for player_count=0 (lines 75-83 - NEEDS FIX) [VERIFIED]
- [x] **Q14**: AccuracyCalculator only has logger state (lines 65-68 - STATELESS) [DEEP VERIFIED]
- [x] **Q20**: Auto-resume always enabled, no flag needed (confirmed in code) [DEEP VERIFIED]
- [x] **Q23**: ConfigGenerator caching is per-instance, safe for parallel [DEEP VERIFIED]
- [x] **Q35**: calculate_ros_mae() verified correct (lines 70-162) [DEEP VERIFIED]
- [x] **Q36**: calculate_weekly_mae() verified correct (lines 164-258) [DEEP VERIFIED]
- [x] **Q37**: PlayerManager cleanup in try/finally blocks (lines 396-446 - CORRECT) [DEEP VERIFIED]
- [x] **Q38**: No shared state issues found in AccuracyCalculator [DEEP VERIFIED]
- [x] **Q39**: 6-file structure required (ConfigGenerator expects it) [DEEP VERIFIED]

### B. Implementation Decisions Needed - UPDATED FOR SCOPE CHANGE
- [MOOT] **Q5**: ~~Weekly mode optimization order~~ - Weekly mode deprecated (tournament uses parameter-first)
- [MOOT] **Q6**: ~~Weekly mode intermediate saving~~ - Weekly mode deprecated (tournament saves once per parameter)
- [x] **Q7**: 'both' mode rewrite approach - replace or add new method? [VERIFIED - replace run_both()]
- [x] **Q8**: Tournament mode auto-resume - implement or not? [VERIFIED - YES, use existing pattern]
- [x] **Q9**: _evaluate_config_tournament() - instance or module-level? [VERIFIED - instance method]
- [x] **Q10**: Error handling in tournament mode - skip horizon or fail config? [VERIFIED - fail entire parameter]
- [x] **Q12**: Empty test values array - how to handle? [VERIFIED - raise exception immediately]
- [x] **Q13**: Parallel processing scope - implement for tournament mode? [VERIFIED - YES, implement parallel processing]
- [x] **Q15**: Module-level function location - same file or separate? [VERIFIED - separate file]
- [x] **Q16**: Parallel worker parameters - how to pass data_folder/seasons? [VERIFIED - explicit parameters]
- [x] **Q17**: Progress tracking - tqdm or custom logging? [VERIFIED - use existing ProgressTracker]
- [x] **Q18**: CLI flag defaults - in constants or CLI only? [VERIFIED - constants]
- [x] **Q19**: --mode flag - add or keep positional arg? [VERIFIED - remove mode argument entirely]
- [x] **Q24**: Tournament folder naming - simple format? [VERIFIED - yes, simple naming]
- [x] **Q25**: Tournament logging - how to show 5 MAE values? [VERIFIED - log new bests only]
- [x] **Q26**: Tournament saving - per parameter or per horizon? [VERIFIED - once per parameter]
- [x] **Q28**: Metadata timing - add now or during rewrite? [VERIFIED - add now]
- [x] **Q29**: Metadata persistence - save to JSON or memory only? [VERIFIED - save to JSON]
- [x] **Q30**: Metadata scope - all modes or tournament only? [VERIFIED - tournament only]
- [MOOT] **Q42**: ~~Weekly folder naming fix~~ - Weekly mode deprecated
- [MOOT] **Q43**: ~~Weekly optimization order~~ - Weekly mode deprecated
- [x] **Q44**: Logging improvements - IN SCOPE (add --log-level flag) ✓

### C. Testing & Validation Questions
- [x] **Q21**: Acceptable runtime for 525 evaluations per parameter? ✓
- [x] **Q22**: Progress estimation/ETA - add MultiLevelProgressTracker ✓
- [x] **Q27**: Config ID regex compatibility - VERIFIED internal only ✓
- [x] **Q31**: Test baseline config - create mock test configs ✓
- [x] **Q32**: Minimum test parameters - 2 parameters ✓
- [x] **Q33**: Test data - both synthetic (unit) and real (integration) ✓
- [x] **Q34**: Divergent optimal test - unit test + manual QA ✓
- [x] **Q40**: Old config migration - ignore (clean break) ✓
- [x] **Q41**: Config validation - ConfigGenerator already handles it ✓

---

## Progress

**After Scope Change + Fresh Analysis:**
- **MOOT**: 7 questions (Q1, Q3, Q4, Q5, Q6, Q42, Q43)
- **Resolved by User**: 2 questions (Q2, Q7)
- **Answered by Research** (need user confirmation): 6 questions (Q8, Q9, Q13, Q15, Q24, Q26)
- **Remaining for User Decision**: 29 questions

**Breakdown:**
- Verification questions: Q11, Q14, Q20, Q23, Q35-Q39 (already researched, need review)
- Implementation decisions: Q10, Q12, Q16-Q19, Q25, Q28-Q30, Q44
- Testing & validation: Q21-Q22, Q27, Q31-Q34, Q40-Q41

**Original counts (before scope change):**
- Resolved from Codebase: 13/44 questions (30%)
- Need User Decision: 28/44 questions (64%)
- Unknown: 3/44 questions (7%)

---

## Resolution Log

### ⚠️ MAJOR SCOPE CHANGE (2025-12-17)

**User Decision: Deprecate ROS and Weekly modes, focus solely on tournament optimization (formerly 'both' mode)**

**Impact:**
- 7 questions marked MOOT (Q1, Q3, Q4, Q5, Q6, Q42, Q43)
- run_ros_optimization() and run_weekly_optimization() → Deprecated (keep for reference)
- run_both() → The only mode (tournament optimization)
- CLI simplified - no mode selection needed
- Implementation focuses on: tournament model rewrite, parallel processing, auto-resume for tournament mode

---

### Resolved from Codebase Verification

**Q1: ROS mode intermediate saving timing** ✓ [USER VERIFIED]
- **Finding**: Saves after EACH new best (AccuracySimulationManager.py:619-623)
- **Current behavior**: `if is_new_best: self.results_manager.save_intermediate_results(...)`
- **Specs requirement**: Save ONCE per parameter after all configs tested
- **User decision**: Confirmed - files should save ONLY after entire parameter optimization finishes
- **Action needed**: Move save_intermediate_results() call outside test value loop (after all configs evaluated)

**Q2: AccuracyCalculator handles 0 players** ✓ [USER VERIFIED]
- **Finding**: Returns safe default `AccuracyResult(mae=0.0, player_count=0, total_error=0.0)` (line 107-109)
- **User decision**: Confirmed - this is correct behavior (graceful handling of edge case)
- **Status**: NO ACTION NEEDED (but see Q11 for related is_better_than() fix)

**Q3: ROS mode auto-resume** ✓ [USER VERIFIED - TESTING REQUIRED]
- **Finding**: Complete implementation exists (lines 551-570)
- **Components verified**:
  - Detection: _detect_resume_state() validates intermediate folders and finds highest completed parameter
  - Loading: load_intermediate_results() reads config files and restores best_configs state
  - Execution: Parameter skip logic continues from next parameter after interruption
  - Error handling: Falls back to fresh start if load fails
- **User decision**: Implementation appears correct, but MUST be verified in integration tests and QA rounds
- **Testing requirement**:
  - Integration test: Start ROS optimization, interrupt mid-parameter, verify resume continues correctly
  - QA test: Manually interrupt optimization, verify intermediate folder detection and state restoration
- **Status**: Code verified correct, requires runtime testing before final sign-off

**Q4: Weekly folder naming** ✓
- **Finding**: Uses `f"{week_key}_{param_name}"` format (line 745)
- **Example**: `accuracy_intermediate_00_week_1_5_NORMALIZATION_MAX_SCALE`
- **Concern**: Very long folder names, may affect resume detection

**Q11: is_better_than() player_count=0 handling** ✓
- **Finding**: Current implementation (lines 75-83) does NOT check player_count
- **Issue**: `mae=0.0` with `player_count=0` would beat real MAE values
- **Action needed**: Add player_count check as specified in notes

**Q14: AccuracyCalculator picklability** ✓
- **Finding**: Only state is `self.logger` (lines 65-68)
- **Status**: STATELESS (except logger), should pickle correctly

**Q20: Auto-resume flag** ✓
- **Finding**: Auto-resume is always enabled, no flag exists
- **Status**: Works via folder detection, no CLI flag needed

**Q23: ConfigGenerator caching thread-safety** ✓
- **Finding**: Cache is instance variable `self._cached_test_values` (lines 1269-1275)
- **Status**: NOT THREAD-SAFE (but each worker would have own ConfigGenerator instance)

**Q35: calculate_ros_mae() correctness** ✓
- **Finding**: Verified implementation (lines 70-162)
- **Status**: CORRECT

**Q36: calculate_weekly_mae() correctness** ✓
- **Finding**: Verified implementation (lines 164-258)
- **Status**: CORRECT

**Q37: PlayerManager cleanup in parallel** ✓
- **Finding**: try/finally blocks handle cleanup (lines 396-446)
- **Status**: CORRECT pattern (matches win-rate simulation)

**Q38: Shared state issues** ✓
- **Finding**: No shared state in AccuracyCalculator
- **Status**: SAFE for parallelism

**Q39: Backward compatibility** ✓
- **Finding**: ConfigGenerator expects 6-file structure
- **Status**: Must require 6-file structure (no backward compat)

---

### Resolved from User Decisions

**Q7: Tournament mode rewrite approach** ✓
- **Decision**: Completely replace existing run_both() method
- **Rationale**: Current implementation is wrong (sequential execution), no value in preserving it
- **Action needed**: Rewrite run_both() → run_tournament_optimization() for per-parameter tournament model

---

### Resolved from Fresh Codebase Analysis (Post Scope Change)

**Tournament Model Implementation Findings:**

**Current run_both() (lines 774-792):**
- Just calls run_ros_optimization() then run_weekly_optimization() sequentially
- Only 19 lines - trivial to replace entirely
- No code worth preserving from this method

**Reusable Infrastructure (GOOD NEWS):**
- ✅ ConfigGenerator already supports 5-horizon configs perfectly (lines 278-365, 1239-1397)
- ✅ AccuracyResultsManager already tracks 5 best_configs independently (lines 120-204)
- ✅ _evaluate_config_ros() and _evaluate_config_weekly() can be wrapped for tournament (lines 374-527)
- ✅ Auto-resume pattern (_detect_resume_state lines 176-280) works for tournament with same regex
- ✅ Signal handlers (lines 155-174) work unchanged
- ✅ Intermediate folder cleanup (lines 573-582, 681-690) works unchanged
- ✅ save_intermediate_results() saves all 5 configs - perfect for tournament (lines 353-456)

**New Code Needed:**
- ⚠️ run_tournament_optimization() - complete rewrite of run_both()
- ⚠️ _evaluate_config_tournament() - lightweight wrapper around existing evaluation methods
- ⚠️ Metadata tracking (optional) - metadata.json in intermediate folders

**Parallel Processing Status:**
- ❌ Accuracy simulation has ZERO parallel processing currently
- ✅ Win-rate simulation has ParallelLeagueRunner (ThreadPoolExecutor/ProcessPoolExecutor pattern)
- ⚠️ For tournament: Can parallelize horizon evaluation per config OR keep sequential (deterministic MAE)

**Questions Answered by Fresh Analysis:**

**Q8: Tournament auto-resume** ✓ [USER VERIFIED]
- Existing _detect_resume_state() (lines 176-280) works perfectly for tournament
- Regex pattern already supports `accuracy_intermediate_{idx}_{paramname}` format
- Resume logic already handles: detect highest param, load last config, resume from next param
- **User decision**: YES - implement auto-resume using existing pattern
- **Action needed**: Reuse _detect_resume_state() in tournament mode, test resume capability in QA rounds

**Q9: _evaluate_config_tournament() placement** ✓ [USER VERIFIED]
- Existing _evaluate_config_ros() and _evaluate_config_weekly() are instance methods
- Tournament method will just wrap/delegate to these based on horizon
- **User decision**: Instance method for consistency
- **Action needed**: Create instance method that delegates to existing evaluation methods based on horizon parameter

**Q13: Parallel processing scope** - RESEARCH SUGGESTS DEFER/OPTIONAL
- Current accuracy simulation: no parallelization
- Each config evaluation: deterministic single MAE calculation (limited benefit from parallelization)
- 525 evaluations per parameter might be slow, but start simple
- **Recommendation**: Implement WITHOUT parallel processing initially, add later if needed

**Q15: Module-level function location** - BECOMES MOOT
- If no parallel processing initially, no module-level function needed
- If added later, follow win-rate pattern (separate file)

**Q24: Tournament folder naming** - RESEARCH SUGGESTS SIMPLE FORMAT
- Format: `accuracy_intermediate_{idx:02d}_{param_name}`
- Example: `accuracy_intermediate_05_MATCHUP_SCORING_WEIGHT`
- Existing regex already supports this
- **Recommendation**: Use simple naming, add metadata.json inside folder for details

**Q24: Tournament folder naming** ✓ [USER VERIFIED]
- **Decision**: Use simple format without horizon suffix
- **Format**: `accuracy_intermediate_{idx:02d}_{param_name}`
- **Example**: `accuracy_intermediate_05_MATCHUP_SCORING_WEIGHT`
- **Regex support**: Existing pattern already handles this
- **Metadata**: Add metadata.json inside folder for detailed information
- **Action needed**: Use simple naming pattern, create metadata.json with horizon details

**Q25: Tournament logging for 5 MAE values** ✓
- **Decision**: Combination - log new bests during optimization (C) + parameter summary at end (D)
- **During optimization (Option C)**:
  - Log only when new best found: `New best for {horizon}: MAE={mae:.4f} (config test_{idx})`
  - Example: `New best for ros: MAE=2.34 (config test_05)`
- **After parameter complete (Option D)**:
  - Summary of all 5 horizons' best results:
  ```
  Parameter NORMALIZATION_MAX_SCALE complete:
    ros: MAE=2.34 (test_05)
    1-5: MAE=2.41 (test_03)
    6-9: MAE=2.38 (test_05)
    10-13: MAE=2.45 (test_01)
    14-17: MAE=2.52 (test_02)
  ```
- **Rationale**: Shows progress during optimization, clear summary at end
- **Action needed**:
  - Log when results_manager.add_result() returns True
  - Print summary after each parameter completes

**Q26: Tournament saving frequency** ✓ [USER VERIFIED]
- **Decision**: Save once per parameter after ALL test values and ALL 5 horizons evaluated
- **Flow**:
  - Test all values for parameter N across all 5 horizons
  - Save intermediate results (all 5 best configs updated)
  - Move to parameter N+1 with updated baselines
- **Rationale**: Matches parameter-first pattern, consistent with ROS/weekly decisions
- **Action needed**: Call save_intermediate_results() once per parameter, after inner loops complete

**Q28-Q30: Tournament metadata** ✓
- **Q28 Decision**: Add metadata support now during implementation
- **Q29 Decision**: Save to metadata.json in intermediate folders
- **Q30 Decision**: Tournament mode only (ROS/weekly deprecated)
- **Metadata structure**:
  ```json
  {
    "param_idx": 5,
    "param_name": "MATCHUP_SCORING_WEIGHT",
    "horizons_evaluated": ["ros", "1-5", "6-9", "10-13", "14-17"],
    "best_mae_per_horizon": {
      "ros": {"mae": 2.34, "test_idx": 5},
      "1-5": {"mae": 2.41, "test_idx": 3},
      ...
    },
    "timestamp": "2025-12-17_20:30:15"
  }
  ```
- **Rationale**: Useful for debugging and resume verification
- **Action needed**: Create metadata.json when saving intermediate results

**Q21: Acceptable runtime for 525 evaluations per parameter** ✓
- **Context**: Tournament mode runs continuously in a loop to converge on optimal parameters
- **User decision**: No specific target - optimize for speed
- **Rationale**: Faster iterations = faster convergence to optimal parameters
- **Key insight**: This is a continuous optimization loop, not a one-time run
- **Action needed**:
  - Implement parallel processing with 8 workers (already decided in Q13)
  - Focus on minimizing per-evaluation overhead
  - Ensure efficient PlayerManager usage

**Q22: Progress estimation/ETA logging** ✓
- **Decision**: Use MultiLevelProgressTracker (Option A - match win-rate sim pattern)
- **Structure**:
  - Outer level: Config being tested (1-105)
  - Inner level: Horizon evaluations for that config (1-5)
  - Overall: True progress across all parameter work
  - Single ETA: Remaining time for entire parameter
- **Research findings**:
  - MultiLevelProgressTracker already exists and works excellently in win-rate sim
  - Current accuracy sim only uses single-level ProgressTracker (poor visibility)
  - Win-rate shows: "Configs: 125/46656 (0.3%) | Sims: 87/100 (87.0%) | Overall: 0.3% | Elapsed: 5m 23s | ETA: 23h 45m"
- **Rationale**: Since optimization runs continuously, clear progress visibility and accurate ETAs are valuable for monitoring
- **Action needed**:
  - Use MultiLevelProgressTracker(outer_total=105, inner_total=5, outer_desc="Configs", inner_desc="Horizons")
  - Integrate progress callbacks from parallel evaluation
  - Update outer with next_outer() after each config completes
  - Update inner with update_inner() after each horizon evaluation
  - Display overall progress and ETA continuously

**Q27: Config ID regex compatibility** ✓ [VERIFIED]
- **Verification findings**:
  - Config IDs are used ONLY for internal tracking in ResultsManager
  - Config IDs appear in: logs, performance_metrics JSON field, metadata tracking
  - Config IDs are NEVER used in: folder names, file names, Path construction
  - Folder names use: `accuracy_intermediate_{idx:02d}_{param_name}` (no config_id)
  - File names are standard: `draft_config.json`, `week1-5.json`, etc. (no config_id)
- **Code verification** (grep results):
  - All config_id uses are in: logging (f-strings), dict keys, JSON fields
  - Zero uses in: Path concatenation, folder creation, file naming
  - Resume detection uses folder name regex, NOT config_id
- **Conclusion**: Config ID format is internal-only, no regex compatibility needed
- **Action needed**: None - config IDs can use any format, no constraints

**Q31: Test baseline config** ✓
- **Decision**: Create mock test configs specific to tests (Option A)
- **Structure**: `tests/fixtures/accuracy_test_baseline/`
  - `league_config.json` (strategy params)
  - `draft_config.json` (ROS prediction params with minimal test ranges)
  - `week1-5.json`, `week6-9.json`, `week10-13.json`, `week14-17.json` (weekly prediction params)
- **Test ranges**: Use 2-3 test values per parameter (instead of 20)
- **Rationale**:
  - Ensures test isolation (not dependent on real optimal configs existing)
  - Fast test execution (minutes instead of hours)
  - Consistent test data across CI/CD and developer machines
  - Tests verify behavior, not real optimization quality
- **Action needed**:
  - Create `tests/fixtures/accuracy_test_baseline/` folder
  - Create all 6 config files with minimal parameter ranges
  - Update integration tests to use test baseline instead of real configs
  - Document test config structure in `tests/README.md`

**Q32: Minimum test parameters for integration tests** ✓
- **Decision**: Test 2 parameters (Option B)
- **Test coverage**: 2 × (21 configs × 5 horizons) = 210 evaluations
- **Estimated runtime**: ~5-10 minutes with 8 workers
- **What this validates**:
  - ✅ Parameter N completes successfully
  - ✅ Intermediate folder saved after parameter N
  - ✅ Parameter N+1 loads from 5 different baseline configs (one per horizon)
  - ✅ Baseline updates work correctly (each horizon uses its own best from N)
  - ✅ Tournament progression works (param N → param N+1)
  - ✅ Independent horizon optimization (5 different bests per parameter)
- **Rationale**: 1 parameter can't test progression/baseline updates (critical behaviors). 3+ parameters add test time without significantly more coverage.
- **Action needed**:
  - Configure integration test with `--num-params 2`
  - Use first 2 parameters from PARAMETER_ORDER
  - Verify intermediate folder created after parameter 1
  - Verify parameter 2 uses parameter 1's best configs as baselines

**Q33: Test data - real or synthetic?** ✓
- **Decision**: Both synthetic (unit tests) and real (integration tests) - Option C
- **Unit tests**:
  - Use synthetic/mocked data: `tests/fixtures/accuracy_test_data/`
  - Create minimal player CSVs with predetermined projected/actual values
  - 5-10 fake players with known MAE values
  - **Pro**: Fast, deterministic, full control over edge cases
- **Integration tests**:
  - Use real historical data: `simulation/sim_data/YEAR/` (NOT `data/`)
  - Tests validate against actual NFL seasons
  - **Pro**: Catches real-world edge cases, validates production behavior
- **Rationale**: This matches existing codebase pattern (unit tests fast/isolated, integration tests realistic)
- **Important clarification**: Real historical data for simulations lives in `simulation/sim_data/`, not the main `data/` folder
- **Action needed**:
  - Create `tests/fixtures/accuracy_test_data/` with synthetic player data
  - Unit tests use synthetic data for fast execution
  - Integration tests use `simulation/sim_data/` for real historical seasons
  - Document test data locations in `tests/README.md`

**Q34: Verify different horizons can find different optimal values** ✓
- **Decision**: Combination approach - Unit test (E) + Manual QA (A)
- **Unit test approach**:
  - Mock AccuracyCalculator to return deliberately different MAE values per horizon
  - Example: For NORMALIZATION_MAX_SCALE=100 → ros: 2.5, 1-5: 2.8, 14-17: 2.2
  - Example: For NORMALIZATION_MAX_SCALE=200 → ros: 2.7, 1-5: 2.4, 14-17: 2.6
  - Verify ResultsManager tracks 5 independent best configs (one per horizon)
  - Verify each horizon selects different optimal value
  - **Pro**: Fast, deterministic, tests the mechanism works
- **Manual QA approach**:
  - During QC rounds, run real tournament optimization with 2 parameters
  - Inspect output configs: `draft_config.json`, `week1-5.json`, `week14-17.json`
  - Check if horizons naturally diverge (different parameter values)
  - Document findings in QC report
  - **Pro**: Validates real-world behavior with actual data
- **Rationale**: Unit test proves system CAN handle divergence, manual QA shows it DOES in practice
- **Action needed**:
  - Write unit test: `test_tournament_horizon_divergence()` with mocked MAE
  - QC Round 1: Run real optimization, inspect horizon divergence
  - Document whether horizons diverged naturally in QC report

**Q40: Old config migration** ✓
- **Decision**: Ignore old configs (Option C) - clean break
- **Context**: Users may have old optimal configs from deprecated ROS/weekly modes
- **Approach**:
  - No migration script - tournament is a new optimization model
  - Old optimal configs remain in place but aren't used
  - No detection or warning messages needed
  - Documentation addition: Add note to accuracy simulation README
- **Documentation text** (for README):
  ```
  **Note on Previous Optimal Configs:**
  Tournament mode is a new optimization approach. Previous ROS/weekly optimal
  configs (from deprecated modes) are not compatible. Run tournament optimization
  to generate new optimal configs for all 5 horizons.
  ```
- **Rationale**: This is a major feature change with deprecated modes. Clean break makes sense.
- **Action needed**:
  - Add note to `simulation/accuracy/README.md` about incompatibility
  - No migration code needed
  - Old configs can remain in `simulation/simulation_configs/` without causing issues

**Q41: Config validation script** ✓
- **Decision**: No separate script needed (Option C) - ConfigGenerator already validates
- **Verification from Q39**: ConfigGenerator.__init__() strictly requires 6 files:
  - `league_config.json` + `draft_config.json` + 4 week configs
  - Raises ValueError with clear message if any file missing
  - Lines 314-324 in simulation/shared/ConfigGenerator.py
- **Rationale**: Existing validation is sufficient, fails fast with clear errors
- **Action needed**: None - rely on ConfigGenerator's existing validation

**Q44: Logging improvements** ✓
- **Decision**: IN SCOPE - Add --log-level flag and systematic review (Option A)
- **What to implement**:
  - Add `--log-level` CLI argument (choices: debug, info, warning, error)
  - Default: info (current behavior)
  - Debug level: Log every config evaluation result, parameter updates, detailed progress
  - Info level: Log new bests, parameter completion, major milestones (current)
  - Systematic review: Audit all log statements in accuracy simulation code
- **Rationale**: Since we're rewriting run_both() and adding new logging (Q25), it makes sense to add proper log level control
- **Action needed**:
  - Add `--log-level` argument to run_accuracy_simulation.py CLI
  - Pass log level to AccuracySimulationManager
  - Review all logger.info/debug statements in accuracy simulation
  - Add debug-level logging for:
    - Each config evaluation: "Config test_05: ros=2.45 MAE, 1-5=2.67 MAE, ..."
    - Parameter updates: "Updated baseline for ros: NORMALIZATION_MAX_SCALE 100→150"
    - Parallel worker activity: "Worker 3 completed config test_12"
  - Ensure info-level shows only: new bests, parameter completion, summaries

---

### Resolved from User Decisions (Post Fresh Analysis)

**Q10: Tournament mode error handling** ✓
- **Decision**: Fail entire parameter optimization if any horizon evaluation fails
- **Rationale**: Forces user to fix data issues, ensures data integrity
- **Behavior**: If exception occurs during any horizon evaluation, log error and raise exception (stop optimization)
- **Action needed**: No try/catch around individual horizon evaluations - let exceptions propagate and halt optimization

**Q11: is_better_than() player_count=0 fix** ✓ [USER VERIFIED]
- **Finding**: Current implementation (lines 75-83) does NOT check player_count
- **Issue**: Config with mae=0.0, player_count=0 would beat real results
- **User decision**: YES - fix needed to reject invalid configs
- **Action needed**: Add player_count checks:
  ```python
  if self.player_count == 0:
      return False  # Invalid config can't be "better"
  if other.player_count == 0:
      return True   # Valid config beats invalid
  ```

**Q12: Empty test values array handling** ✓
- **Decision**: Raise exception immediately (fail fast)
- **Rationale**: Consistent with Q10 error handling approach, forces user to fix configuration
- **Scenarios**: Config error, invalid parameter name, ConfigGenerator bug
- **Action needed**: Check if test_values array is empty after generate_horizon_test_values(), raise ValueError with descriptive message

**Q13: Parallel processing for tournament mode** ✓ [USER OVERRODE RESEARCH RECOMMENDATION]
- **Research recommendation**: Start without parallel processing (keep simple)
- **User decision**: YES - implement parallel processing for tournament mode
- **Rationale**: 525 evaluations per parameter (105 configs × 5 horizons) warrants parallelization for performance
- **Pattern to follow**: Win-rate simulation's ProcessPoolExecutor pattern (ParallelLeagueRunner)
- **Action needed**:
  - Add module-level evaluation function for pickling
  - Implement parallel config evaluation (evaluate multiple configs in parallel)
  - Add CLI flags: --max-workers, --use-processes / --no-use-processes
  - Default: 8 workers, ProcessPoolExecutor (true parallelism, bypasses GIL)

**Q15: Module-level function location** ✓
- **Decision**: Separate file (follow win-rate pattern)
- **Create new file**: `simulation/accuracy/ParallelAccuracyRunner.py`
- **Contents**:
  - Module-level function: `_evaluate_config_tournament_process()`
  - Class: `ParallelAccuracyRunner` (manages ProcessPoolExecutor)
- **Action needed**: Create new file following ParallelLeagueRunner pattern from win-rate simulation

**Q16: Parallel worker parameters** ✓
- **Decision**: Explicit parameters (match win-rate pattern)
- **Function signature**:
  ```python
  def _evaluate_config_tournament_process(
      config_dict: dict,
      data_folder: Path,
      available_seasons: List[str],
      horizon: str
  ) -> AccuracyResult:
  ```
- **Rationale**: Type-safe, clear, matches win-rate ProcessPoolExecutor pattern
- **Action needed**: Implement with explicit parameters, not bundled dict

**Q17: Progress tracking** ✓
- **Decision**: Use existing ProgressTracker
- **Location**: `simulation/shared/ProgressTracker.py` already exists
- **Usage**: Create ProgressTracker for config evaluations per parameter
- **Rationale**: Consistent with current ROS/weekly modes, no new dependencies
- **Action needed**: Use ProgressTracker in tournament optimization loop, may need minor enhancements for parallel execution

**Q18: CLI flag defaults** ✓
- **Decision**: Define defaults in constants section
- **Constants to add**:
  - `DEFAULT_MAX_WORKERS = 8`
  - `DEFAULT_USE_PROCESSES = True`
- **Rationale**: Easier to change, documents defaults clearly
- **Action needed**: Add constants at top of run_accuracy_simulation.py, reference in argparse

**Q19: Mode selection** ✓
- **Decision**: Remove mode argument entirely (tournament is implicit)
- **Current**: `python run_accuracy_simulation.py ros` (positional arg)
- **New**: `python run_accuracy_simulation.py` (no mode arg needed)
- **Rationale**: Only one mode exists (tournament), no need to specify
- **Action needed**: Remove mode positional argument from argparse, update --help text

---

*(Remaining user decision items to be resolved during Phase 4)*

