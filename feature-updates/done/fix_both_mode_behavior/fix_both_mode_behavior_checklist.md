# Fix 'both' Mode Behavior - Requirements Checklist

> **Note:** Items marked [x] are resolved. Items marked [ ] need investigation or user decision.

---

## THREE-ITERATION Question Generation

### Iteration 1: Surface-Level Questions (from notes analysis)

1. **Q1**: Should `_evaluate_config_both()` reuse existing `_evaluate_config_ros()` and `_evaluate_config_weekly()` methods, or should we inline the evaluation logic?
2. **Q2**: How should parallel processing handle temporary directory cleanup for PlayerManager instances?
3. **Q3**: Should the results_manager track which configs were tested from which base (for tournament tracking)?
4. **Q4**: What should happen if a horizon fails to find any valid players during evaluation?
5. **Q5**: Should intermediate results save all 5 horizon configs, or only those that have been actively tested?
6. **Q6**: How should config_id be formatted for 'both' mode? (e.g., `param_test_idx_horizon_all` vs separate IDs per horizon)
7. **Q7**: Should parallel workers share a single AccuracyCalculator instance or create their own?
8. **Q8**: What logging level should be used for per-config evaluation (5 horizons = verbose output)?

### Iteration 2: Implementation Details (from codebase research)

9. **Q9**: ConfigGenerator's `generate_horizon_test_values()` returns dict with keys 'shared' or horizon names - how do we iterate to test all horizons with one config in 'both' mode?
10. **Q10**: AccuracySimulationManager currently uses `self.config_generator.baseline_configs[horizon]` - should `run_both()` maintain 5 separate base configs like `run_weekly_optimization()` does?
11. **Q11**: The current `run_both()` calls `run_ros_optimization()` then `run_weekly_optimization()` sequentially - should we keep the sequential mode as a fallback option or completely replace it?
12. **Q12**: ProcessPoolExecutor requires picklable functions - should `_evaluate_config_both()` be a module-level function or can it stay as an instance method?
13. **Q13**: AccuracyResultsManager.add_result() expects a week_range_key ('ros', 'week_1_5', etc.) - should 'both' mode call add_result() 5 times per config with different keys?
14. **Q14**: The existing resume detection (`_detect_resume_state`) expects mode parameter ('ros' or 'weekly') - what mode string should 'both' mode use?
15. **Q15**: Should --max-workers and --use-processes be added to run_accuracy_simulation.py's DEFAULT constants or only as CLI arguments?
16. **Q16**: ConfigGenerator caches test values in `_cached_test_values` - does this work correctly when we need all 5 horizons' test values simultaneously?

### Iteration 3: Edge Cases and Integration (deeper analysis)

17. **Q17**: What happens if ROS evaluation succeeds but one of the weekly evaluations fails for the same config? Should we skip that horizon or fail the entire config?
18. **Q18**: The notes mention "5 different base configs per parameter" for tournament behavior - does this mean parameter 2+ should generate 5x more test configs than parameter 1?
19. **Q19**: AccuracyCalculator methods are deterministic (no randomness) - does this mean parallel evaluation can safely run without seed management?
20. **Q20**: The current code uses `copy.deepcopy(self.config_generator.baseline_configs[horizon])` - will this work correctly in multiprocessing (pickle serialization)?
21. **Q21**: Should save_intermediate_results() be called after EACH config (new best), or only after ALL configs for a parameter are tested?
22. **Q22**: If parallel evaluation fails partway through, should we save partial results or discard everything from that parameter?
23. **Q23**: The notes say "each config evaluated across all 5 horizons" - should test_values arrays be aligned across horizons (index 0 of ROS tests with index 0 of week1-5)?
24. **Q24**: Should the tournament model allow a horizon to "skip" a parameter if its optimal config from the previous parameter is already at the boundary of the parameter range?
25. **Q25**: How should logging distinguish between the 5 horizon evaluations within a single config test (to avoid log clutter)?
26. **Q26**: If `--use-processes=False` (ThreadPoolExecutor), will GIL contention make parallelization pointless for deterministic MAE calculations?
27. **Q27**: Should `run_both()` support the same auto-resume capability as `run_ros_optimization()` and `run_weekly_optimization()`?
28. **Q28**: The spec mentions "config_id format works with regex fix" - should we verify the config_id format before creating it to ensure compatibility?

---

## Checklist Items (Categorized)

### A. Core Architecture Questions

- [ ] **Q11**: Replace sequential `run_both()` completely or keep as fallback?
- [ ] **Q13**: Call add_result() 5 times per config (once per horizon)?
- [ ] **Q10**: Maintain 5 separate base configs in `run_both()` like `run_weekly_optimization()`?
- [ ] **Q18**: Parameter 2+ generates 5x test configs (one per base)?
- [ ] **Q23**: Align test_values arrays across horizons by index?

### B. Parallel Processing Questions

- [x] **Q2**: How to handle PlayerManager temp directory cleanup in parallel?
- [x] **Q7**: Shared vs per-worker AccuracyCalculator instance?
- [x] **Q12**: `_evaluate_config_both()` as module-level function for pickling? (Same as Q7)
- [ ] **Q20**: Deep copy of baseline_configs works with pickle serialization?
- [ ] **Q26**: Is ThreadPoolExecutor (GIL-limited) pointless for deterministic MAE?

### C. Implementation Details

- [x] **Q1**: Reuse `_evaluate_config_ros()` / `_evaluate_config_weekly()` or inline?
- [ ] **Q9**: How to iterate ConfigGenerator's horizon-based test values for 'both' mode? (RESET - see week-specific params context)
- [ ] **Q16**: ConfigGenerator cache handles simultaneous access to all 5 horizons' values?
- [ ] **Q15**: --max-workers/--use-processes as DEFAULT constants or CLI-only?
- [ ] **Q19**: No seed management needed (deterministic evaluation)?

### D. Error Handling & Edge Cases

- [x] **Q4**: What if no valid players found for a horizon?
- [ ] **Q17**: If one horizon fails, skip horizon or fail entire config?
- [ ] **Q22**: Save partial results or discard on failure?
- [ ] **Q24**: Allow horizon to "skip" parameter if already at range boundary?

### E. State Management & Resume

- [x] **Q5**: Intermediate results save all 5 configs or only tested ones?
- [ ] **Q14**: What mode string for `_detect_resume_state()` in 'both' mode?
- [x] **Q21**: Save intermediate after each new best or after all configs tested? (Same as Q5)
- [ ] **Q27**: Support auto-resume in `run_both()`?

### F. Output & Logging

- [x] **Q3**: Track which configs tested from which base (tournament tracking)?
- [x] **Q6**: config_id format for 'both' mode?
- [x] **Q8**: Logging level for per-config evaluation (verbose)?
- [ ] **Q25**: Distinguish 5 horizon evaluations in logs?
- [ ] **Q28**: Verify config_id format compatibility with regex fix?

---

## CRITICAL CONTEXT: Week-Specific Parameters

**IMPORTANT:** Accuracy simulation optimizes WEEK_SPECIFIC_PARAMS (not BASE_CONFIG_PARAMS).

**From run_accuracy_simulation.py lines 71-88:**
All 16 parameters in PARAMETER_ORDER are WEEK_SPECIFIC:
- NORMALIZATION_MAX_SCALE
- TEAM_QUALITY_SCORING (WEIGHT + MIN_WEEKS)
- PERFORMANCE_SCORING (WEIGHT + STEPS + MIN_WEEKS)
- MATCHUP_SCORING (IMPACT_SCALE + WEIGHT + MIN_WEEKS)
- TEMPERATURE_SCORING (IMPACT_SCALE + WEIGHT)
- WIND_SCORING (IMPACT_SCALE + WEIGHT)
- LOCATION_MODIFIERS (HOME + AWAY + INTERNATIONAL)

**From simulation/shared/ResultsManager.py:**
- BASE_CONFIG_PARAMS: SAME_POS_BYE_WEIGHT, ADP_SCORING, DRAFT_ORDER_BONUSES, etc. (shared across all horizons)
- WEEK_SPECIFIC_PARAMS: See above (can vary per horizon for optimal predictions)

**This means:**
- ConfigGenerator.generate_horizon_test_values() returns: `{'ros': [...], '1-5': [...], '6-9': [...], '10-13': [...], '14-17': [...]}`
- NOT `{'shared': [...]}`
- Each horizon has its own baseline value and test values
- Tournament model is CORRECT: each horizon optimizes independently
- For parameter 2+: Generate test configs from 5 different base configs (one per horizon's previous best)

**Implementation impact:**
- Must iterate test_idx for EACH horizon (not just once for "shared")
- Each parameter tests 5x as many configs (one set per horizon)
- Each config is still evaluated across ALL 5 horizons
- Results tracked separately per horizon (5 independent "best" configs)

---

## Resolution Log

**Progress:** 9/28 questions resolved (32%) - Q9 reset due to week-specific params clarification

---

### Q1: Reuse existing methods ✓
**Date:** 2025-12-17
**Decision:** Option A - Reuse `_evaluate_config_ros()` and `_evaluate_config_weekly()`
**Rationale:**
- Methods already in production use (run_ros_optimization, run_weekly_optimization)
- Handle cleanup properly via try/finally blocks
- Temp directory creation is unavoidable (PlayerManager architecture requirement)
- File copying overhead negligible compared to MAE calculations
- Simpler code (5 lines vs ~80-100) reduces bug risk
- Parallel workers handle performance, no need for micro-optimization

**Implementation:**
```python
def _evaluate_config_both(self, config_dict: Dict[str, Any]) -> Dict[str, AccuracyResult]:
    results = {}
    results['ros'] = self._evaluate_config_ros(config_dict)
    for week_key, week_range in WEEK_RANGES.items():
        results[week_key] = self._evaluate_config_weekly(config_dict, week_range)
    return results
```

---

### Q2: Temp directory cleanup in parallel ✓
**Date:** 2025-12-17
**Decision:** Option A - No changes needed (existing try/finally cleanup works)
**Rationale:**
- Accuracy simulation already uses same pattern as win-rate simulation
- Win-rate uses explicit cleanup in finally blocks (ParallelLeagueRunner lines 189-221)
- Pattern: `try: create resource → finally: cleanup() + del object`
- Works in both ThreadPoolExecutor and ProcessPoolExecutor contexts
- `_evaluate_config_ros()` and `_evaluate_config_weekly()` already have try/finally
- `_cleanup_player_manager()` deletes temp directories properly
- Cleanup happens at right granularity (per season evaluation)
- Pattern is production-tested and handles exceptions correctly

**Verification:**
- Win-rate: `league.cleanup()` + `del league` in finally block
- Accuracy: `self._cleanup_player_manager(player_mgr)` in finally block
- Both patterns ensure cleanup even on worker process failure

**No implementation changes required.**

---

### Q3: Tournament metadata tracking ✓
**Date:** 2025-12-17
**Decision:** Option B - Add full tournament metadata to AccuracyConfigPerformance
**Rationale:**
- Useful for debugging (why did this config win?)
- Can trace optimization history across parameters
- Helps understand parameter interactions
- User specifically wants this for debugging purposes
- Small overhead (just 3 extra fields per result)

**Implementation:**
1. Add fields to `AccuracyConfigPerformance.__init__()`:
   - `base_horizon: Optional[str]` - Which horizon's base was used ('ros', '1-5', '6-9', '10-13', '14-17')
   - `param_name: Optional[str]` - Which parameter was being tested
   - `test_idx: Optional[int]` - Which test value index (0 = baseline)

2. Update `AccuracyResultsManager.add_result()` signature:
   ```python
   def add_result(
       self,
       week_range_key: str,
       config_dict: dict,
       accuracy_result: AccuracyResult,
       base_horizon: Optional[str] = None,  # NEW
       param_name: Optional[str] = None,    # NEW
       test_idx: Optional[int] = None       # NEW
   ) -> bool:
   ```

3. Update `to_dict()` and `from_dict()` to serialize new fields

4. Call site in `run_both()` passes metadata:
   ```python
   is_new_best = self.results_manager.add_result(
       horizon_key,
       config_dict,
       result,
       base_horizon=horizon,     # Which base was used
       param_name=param_name,    # Current parameter
       test_idx=test_idx         # Test value index
   )
   ```

**Benefits:**
- Full tournament history in saved JSON files
- Can reconstruct optimization path
- Debug why certain configs won
- Analyze parameter interaction patterns

---

### Q4: Handle horizon with no valid players ✓
**Date:** 2025-12-17
**Decision:** Option B - Fix `is_better_than()` logic to reject results with player_count=0
**Rationale:**
- AccuracyCalculator already returns safe default: `AccuracyResult(mae=0.0, player_count=0, total_error=0.0)`
- Problem: `is_better_than()` would consider mae=0.0 as "better" than real MAE values
- Fix at comparison layer (not calculation or result tracking layer)
- Allows tracking that a horizon had no valid players (useful for debugging)
- Won't accidentally mark invalid config as optimal
- Clear semantics: "0 players is never better than having actual data"

**Implementation:**
Update `AccuracyConfigPerformance.is_better_than()` in AccuracyResultsManager.py:
```python
def is_better_than(self, other: 'AccuracyConfigPerformance') -> bool:
    """
    Check if this configuration is better than another.
    Lower MAE is better. Results with 0 players are never considered better.
    """
    if other is None:
        return True

    # Never consider results with 0 players as "better"
    if self.player_count == 0:
        return False

    # If other has 0 players but we have data, we're better
    if other.player_count == 0:
        return True

    # Both have valid data - compare MAE (lower is better)
    return self.mae < other.mae
```

**Edge Cases Handled:**
- Config with 0 players: Never wins, but still tracked (for debugging)
- All configs have 0 players: First one becomes "best" (all equally invalid)
- Mixed valid/invalid: Valid configs always beat invalid ones

---

### Q5: When to save intermediate results ✓
**Date:** 2025-12-17
**Decision:** Option B - Save ONCE per parameter after all 5 horizons tested (not after each new best)
**Rationale:**
- **Win-rate pattern**: Saves intermediate ONCE per parameter, after all test values tested (SimulationManager.py:826-834)
- **Win-rate collects ALL ranges**: Lines 816-823 collect week_range_performance for all 4 ranges before saving
- **Efficiency**: 1 save per parameter vs dozens of saves (current accuracy ROS/weekly modes save on every new best)
- **Consistency**: All 5 horizons have valid results before save
- **Clean structure**: Intermediate folders always have all 6 files with real data
- **User requirement**: "All 5 horizons must finish being tested before saving"

**Current accuracy behavior (WRONG for 'both' mode):**
```python
# ROS mode (lines 619-623) and Weekly mode (lines 743-746)
for test_idx in test_values:
    result = self._evaluate_config_ros(config_dict)
    is_new_best = self.results_manager.add_result('ros', config_dict, result)
    if is_new_best:  # ← Saves EVERY new best
        self.results_manager.save_intermediate_results(param_idx, param_name)
```

**Correct 'both' mode behavior (matches win-rate):**
```python
for param_idx, param_name in enumerate(self.parameter_order):
    # Test ALL configs for this parameter
    for config in configs_to_test:
        results = self._evaluate_config_both(config)  # All 5 horizons
        for horizon_key, result in results.items():
            self.results_manager.add_result(horizon_key, config, result, ...)

    # AFTER all configs tested, save ONCE (all 5 horizons populated)
    self._current_optimal_config_path = self.results_manager.save_intermediate_results(
        param_idx, param_name
    )
```

**Implementation changes:**
- Move save_intermediate_results() call outside config loop
- Remove `if is_new_best:` condition
- Save once per parameter with all 5 horizons having valid best configs

---

### Q6: config_id format for 'both' mode ✓
**Date:** 2025-12-17
**Decision:** Option B - Use win-rate format: `{param_name}_{test_idx}_horizon_{result_horizon}`
**Rationale:**
- **Win-rate pattern (SimulationManager.py:745)**: Uses exact same format
  ```python
  config_id = f"{param_name}_{test_idx}_horizon_{horizon}"
  # Examples: SAME_POS_BYE_WEIGHT_4_horizon_ros
  #           ADP_SCORING_WEIGHT_2_horizon_1-5
  ```
- **Parseable**: Regex `r'_(\d+)_horizon_'` extracts test_idx (used in line 789)
- **Debuggable**: Can see parameter, test index, and horizon from ID
- **Handles underscores**: Works with param names like SAME_POS_BYE_WEIGHT
- **Simpler than encoding everything**: Base horizon tracked separately in metadata (Q3)
- **Compatible with regex fix**: Works with fix from commit b0cf69f

**Current accuracy behavior (hash-based):**
```python
# AccuracyConfigPerformance._generate_id()
config_str = json.dumps(config, sort_keys=True)
return hashlib.md5(config_str.encode()).hexdigest()[:8]  # → "a3f8c2d1"
```

**Problems with hash:**
- Not parseable (can't extract test_idx or horizon)
- Not debuggable (no semantic meaning)
- Same config from different contexts = same hash (collision)

**New behavior for 'both' mode:**
```python
# In run_both() when calling add_result()
for result_horizon, result in all_results.items():
    config_id = f"{param_name}_{test_idx}_horizon_{result_horizon}"

    self.results_manager.add_result(
        result_horizon,
        config_dict,
        result,
        config_id=config_id,  # Pass explicit ID
        base_horizon=base_horizon,  # From Q3
        param_name=param_name,      # From Q3
        test_idx=test_idx           # From Q3
    )
```

**Implementation changes:**
1. Update `AccuracyConfigPerformance.__init__()` to accept optional config_id parameter (already has this)
2. Update `AccuracyResultsManager.add_result()` to accept config_id parameter
3. Generate config_id in run_both() loop before calling add_result()
4. Format: `f"{param_name}_{test_idx}_horizon_{result_horizon}"`

**Examples:**
- `NORMALIZATION_MAX_SCALE_0_horizon_ros`
- `NORMALIZATION_MAX_SCALE_2_horizon_week_1_5`
- `TEAM_QUALITY_SCORING_WEIGHT_4_horizon_week_6_9`

---

### Q7: Shared vs per-worker AccuracyCalculator ✓
**Date:** 2025-12-17
**Decision:** Option A - Module-level function with per-worker AccuracyCalculator instances
**Rationale:**
- **Win-rate pattern (ParallelLeagueRunner.py:44-69)**: Uses module-level functions that create their own objects
  ```python
  def _run_simulation_process(args):
      league = SimulatedLeague(config_dict, data_folder)  # Creates own objects
      # ... run simulation ...
      return results
  ```
- **AccuracyCalculator is stateless**: Only has logger, all methods are pure functions
  ```python
  class AccuracyCalculator:
      def __init__(self):
          self.logger = get_logger()  # Only state (read-only)
  ```
- **ProcessPoolExecutor requirement**: Module-level functions are picklable, instance methods require pickling entire manager
- **True parallelism**: ProcessPoolExecutor bypasses GIL (important for CPU-bound MAE calculations)
- **Clean separation**: Each worker is independent, no shared state concerns
- **Lightweight**: Creating AccuracyCalculator per worker is cheap (just instantiates logger)

**Current accuracy pattern:**
```python
# AccuracySimulationManager.__init__ (line 118)
self.accuracy_calculator = AccuracyCalculator()  # Single instance

# _evaluate_config_ros() uses instance method
def _evaluate_config_ros(self, config_dict):
    result = self.accuracy_calculator.calculate_ros_mae(...)  # Uses self
```

**New pattern for 'both' mode (matches win-rate):**
```python
# Module-level function (outside class, at top of file)
def _evaluate_config_both_process(args: Tuple) -> Dict[str, AccuracyResult]:
    """
    Evaluate config across all 5 horizons in worker process.
    Module-level function required for ProcessPoolExecutor pickling.
    """
    config_dict, data_folder, available_seasons, baseline_path = args

    # Create calculator in worker process
    calculator = AccuracyCalculator()  # Per-worker instance

    # Reuse _evaluate_config_ros and _evaluate_config_weekly logic
    # ... evaluation code ...

    return {
        'ros': ros_result,
        'week_1_5': week_1_5_result,
        # ... all 5 results
    }

# In run_both()
with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
    futures = {
        executor.submit(
            _evaluate_config_both_process,
            (config_dict, self.data_folder, self.available_seasons, self.baseline_config_path)
        ): (horizon, test_idx)
        for horizon, test_idx, config_dict in configs_to_test
    }
```

**Implementation notes:**
- Keep instance method `_evaluate_config_both()` for ThreadPoolExecutor fallback
- Module-level function for ProcessPoolExecutor (default)
- Choose function based on `use_processes` flag (like ParallelLeagueRunner lines 317-332)

---

### Q8: Logging levels for per-config evaluation ✓
**Date:** 2025-12-17
**Decision:** Option A - Match win-rate pattern (info for configs, debug for horizons/seasons)
**Rationale:**
- **Win-rate pattern (SimulationManager.py:712, 760, 772)**:
  - `logger.info()` for major milestones (parameter start, config completion, best results)
  - `logger.debug()` for within-config details (season-level processing)
  - `logger.warning()` for skipped items

**Win-rate example:**
```python
# Parameter level
logger.info("OPTIMIZING PARAMETER X/Y: {param_name}")  # Line 712

# Config level
logger.info(f"Completed test value {test_idx + 1}/{len(test_values)}")  # Line 760

# Season level (within config)
logger.debug(f"Season {season_idx + 1}/{total_seasons}: {season_name}")  # Line 345
logger.debug(f"  Season {season_name}: {count} players")  # Line 258
```

**For 'both' mode logging:**
```python
# Parameter level (info)
logger.info("=" * 80)
logger.info(f"OPTIMIZING PARAMETER {param_idx}/{num_params}: {param_name}")
logger.info("=" * 80)

# Config level (info) - main progress indicator
logger.info(f"Testing config {cfg_idx + 1}/{total_configs}")

# Horizon level (debug) - detailed breakdown
logger.debug(f"  Horizon {horizon}: MAE={result.mae:.4f}, players={result.player_count}")

# Season level (debug) - very detailed
logger.debug(f"    Season {season_name}: {player_count} players evaluated")

# New best found (info)
logger.info(f"New best for {horizon}: MAE={mae:.4f} (previous: {prev_mae:.4f})")
```

**Benefits:**
- Clean default output (shows config-level progress)
- Debug mode reveals all details (horizon, season breakdown)
- Consistent with win-rate simulation
- Users can control verbosity with logging level

**Log volume estimate (default INFO level):**
- Per parameter: ~30 config progress lines + ~5 "new best" lines = 35 info lines
- With DEBUG: adds ~450 debug lines (30 configs × 5 horizons × 3 seasons)

---
