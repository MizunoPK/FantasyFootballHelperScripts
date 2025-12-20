# Accuracy Simulation - Testing & Validation - Implementation TODO

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: □□□□□□□ (0/7)   R2: □□□□□□□□□ (0/9)   R3: □□□□□□□□ (0/8)
```
Legend: ■ = complete, □ = pending, ▣ = in progress

**Current:** Iteration ___ ({type} - Round {N})
**Confidence:** HIGH / MEDIUM / LOW
**Blockers:** None / {description}

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [ ]1 [ ]2 [ ]3 [ ]4 [ ]5 [ ]6 [ ]7 | 0/7 |
| Second (9) | [ ]8 [ ]9 [ ]10 [ ]11 [ ]12 [ ]13 [ ]14 [ ]15 [ ]16 | 0/9 |
| Third (8) | [ ]17 [ ]18 [ ]19 [ ]20 [ ]21 [ ]22 [ ]23 [ ]24 | 0/8 |

**Current Iteration:** ___

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [ ]1 [ ]2 [ ]3 [ ]8 [ ]9 [ ]10 [ ]15 [ ]16 |
| Algorithm Traceability | 4, 11, 19 | [ ]4 [ ]11 [ ]19 |
| End-to-End Data Flow | 5, 12 | [ ]5 [ ]12 |
| Skeptical Re-verification | 6, 13, 22 | [ ]6 [ ]13 [ ]22 |
| Integration Gap Check | 7, 14, 23 | [ ]7 [ ]14 [ ]23 |
| Fresh Eyes Review | 17, 18 | [ ]17 [ ]18 |
| Edge Case Verification | 20 | [ ]20 |
| Test Coverage Planning + Mock Audit | 21 | [ ]21 |
| Implementation Readiness | 24 | [ ]24 |
| Interface Verification | Pre-impl | [ ] |

---

## Verification Summary

- Iterations completed: 0/24
- Requirements from spec: 6 (unit tests, integration tests, manual QA, test fixtures, divergence tests)
- Requirements in TODO: 6
- Questions for user: 0
- Integration points identified: 3

---

## Sub-Feature Overview

**Name:** Testing & Validation (Phase 5 of 5)
**Priority:** Quality assurance - final phase before completion
**Dependencies:** Phases 1-4 (Core Fixes, Tournament Rewrite, Parallel Processing, CLI & Logging) must be complete
**Next Phase:** None - this is the final phase

**What this sub-feature implements:**
1. Unit tests with mocked MAE for divergence scenarios (Q34)
2. Integration tests with 2 parameters validating progression (Q32)
3. Manual QA verification during 3 QC rounds (Q34)
4. Verify test fixtures work correctly (Q31, Q33)
5. Test both synthetic (unit) and real (integration) data (Q33)
6. Verify different horizons can find different optimal values (Q34)

**Why these are grouped:**
- All testing and quality assurance tasks
- Final validation before marking feature complete
- Ensures tournament optimization works correctly
- Catches edge cases and integration issues
- 3 QC rounds provide comprehensive coverage

---

## Phase 1: Unit Tests for Core Fixes

### Task 1.1: Write unit test for is_better_than() player_count=0 handling

- **File:** `tests/simulation/test_AccuracyResultsManager.py`
- **Test:** `test_is_better_than_rejects_zero_players()`
- **Purpose:** Verify is_better_than() rejects configs with player_count=0
- **Status:** [ ] Not started

**Implementation details:**
1. Create two AccuracyConfigPerformance objects
2. Config A: mae=2.5, player_count=100 (valid)
3. Config B: mae=2.0, player_count=0 (invalid - better MAE but no players)
4. Verify: A.is_better_than(B) = False (valid never beats invalid)
5. Verify: B.is_better_than(A) = False (invalid never beats valid)

**Test code:**
```python
def test_is_better_than_rejects_zero_players(self):
    """Test that is_better_than() rejects configs with player_count=0."""
    # Valid config
    config_a = AccuracyConfigPerformance(
        config_id="test_a",
        config={},
        mae=2.5,
        player_count=100,
        total_error=250.0
    )

    # Invalid config (better MAE but no players)
    config_b = AccuracyConfigPerformance(
        config_id="test_b",
        config={},
        mae=2.0,
        player_count=0,
        total_error=0.0
    )

    # Valid config should not beat invalid config
    assert config_a.is_better_than(config_b) == False

    # Invalid config should not beat valid config
    assert config_b.is_better_than(config_a) == False
```

**Verification:**
- [ ] Test created
- [ ] Test covers valid vs invalid
- [ ] Test covers invalid vs valid
- [ ] Test passes

---

### Task 1.2: Write unit test for both configs with player_count=0

- **File:** `tests/simulation/test_AccuracyResultsManager.py`
- **Test:** `test_is_better_than_both_zero_players()`
- **Purpose:** Verify neither config is better when both have player_count=0
- **Status:** [ ] Not started

**Test code:**
```python
def test_is_better_than_both_zero_players(self):
    """Test that neither config is better when both have player_count=0."""
    config_a = AccuracyConfigPerformance(
        config_id="test_a",
        config={},
        mae=2.5,
        player_count=0,
        total_error=0.0
    )

    config_b = AccuracyConfigPerformance(
        config_id="test_b",
        config={},
        mae=2.0,
        player_count=0,
        total_error=0.0
    )

    # Neither invalid config beats the other
    assert config_a.is_better_than(config_b) == False
    assert config_b.is_better_than(config_a) == False
```

**Verification:**
- [ ] Test created
- [ ] Test covers both invalid
- [ ] Test passes

---

## Phase 2: Unit Tests for Tournament Optimization

### Task 2.1: Write unit test for tournament horizon divergence (mocked MAE)

- **File:** `tests/simulation/test_AccuracySimulationManager.py` or create new file
- **Test:** `test_tournament_horizon_divergence()`
- **Purpose:** Verify different horizons can find different optimal values (Q34)
- **Status:** [ ] Not started

**Implementation details:**
1. Mock AccuracyCalculator to return deliberately different MAE values per horizon
2. Run tournament optimization with 1 parameter, 2 test values
3. Verify each horizon tracks independent best config
4. Verify horizons select different optimal values

**Test code structure:**
```python
@patch('simulation.accuracy.AccuracyCalculator.AccuracyCalculator')
def test_tournament_horizon_divergence(self, mock_calculator_class):
    """Test that different horizons can find different optimal parameter values."""
    # Setup mock calculator
    mock_calculator = Mock()

    # Mock MAE values: different horizons prefer different test values
    # For NORMALIZATION_MAX_SCALE test values: 100, 150, 200
    # Value 100: ros prefers, 1-5 prefers 150, 14-17 prefers 200
    def mock_calculate_ros_mae(data_folder, config):
        scale = config.get('NORMALIZATION_MAX_SCALE', 150)
        if scale == 100:
            return AccuracyResult(mae=2.0, player_count=50, total_error=100.0)  # Best for ROS
        elif scale == 150:
            return AccuracyResult(mae=2.5, player_count=50, total_error=125.0)
        else:  # 200
            return AccuracyResult(mae=3.0, player_count=50, total_error=150.0)

    def mock_calculate_weekly_mae(data_folder, config, week_range):
        scale = config.get('NORMALIZATION_MAX_SCALE', 150)
        if week_range == '1-5':
            # 1-5 prefers 150
            if scale == 150:
                return AccuracyResult(mae=2.0, player_count=50, total_error=100.0)
            else:
                return AccuracyResult(mae=2.5, player_count=50, total_error=125.0)
        elif week_range == '14-17':
            # 14-17 prefers 200
            if scale == 200:
                return AccuracyResult(mae=2.0, player_count=50, total_error=100.0)
            else:
                return AccuracyResult(mae=2.5, player_count=50, total_error=125.0)
        else:
            # 6-9, 10-13 neutral
            return AccuracyResult(mae=2.3, player_count=50, total_error=115.0)

    mock_calculator.calculate_ros_mae.side_effect = mock_calculate_ros_mae
    mock_calculator.calculate_weekly_mae.side_effect = mock_calculate_weekly_mae
    mock_calculator_class.return_value = mock_calculator

    # Run tournament optimization
    # ... create manager with test baseline ...
    # ... run with 1 parameter, test values [100, 150, 200] ...

    # Verify different horizons found different optimal values
    assert manager.results_manager.best_configs['ros'].config['NORMALIZATION_MAX_SCALE'] == 100
    assert manager.results_manager.best_configs['1-5'].config['NORMALIZATION_MAX_SCALE'] == 150
    assert manager.results_manager.best_configs['14-17'].config['NORMALIZATION_MAX_SCALE'] == 200

    # Verify all horizons have valid results
    for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
        assert manager.results_manager.best_configs[horizon].player_count > 0
        assert manager.results_manager.best_configs[horizon].mae > 0
```

**Verification:**
- [ ] Test created
- [ ] MAE values mocked to create deliberate divergence
- [ ] Tournament optimization runs
- [ ] Different horizons select different values
- [ ] All horizons have valid results
- [ ] Test passes

---

## Phase 3: Integration Tests with Real Data

### Task 3.1: Write integration test for 2-parameter tournament optimization

- **File:** `tests/integration/test_accuracy_simulation_integration.py`
- **Test:** `test_tournament_optimization_two_parameters()`
- **Purpose:** Validate tournament progression and baseline updates (Q32)
- **Status:** [ ] Not started

**Implementation details:**
1. Use test baseline from `tests/fixtures/accuracy_test_baseline/`
2. Use real data from `simulation/sim_data/` for one season
3. Run tournament with 2 parameters, 2 test values each
4. Verify intermediate folder created after parameter 1
5. Verify parameter 2 uses parameter 1's best configs as baselines
6. Verify all 6 config files saved
7. Verify metadata.json present

**Test code structure:**
```python
def test_tournament_optimization_two_parameters(tmp_path):
    """Integration test: Run tournament with 2 parameters, verify progression."""
    # Setup
    baseline_path = Path("tests/fixtures/accuracy_test_baseline")
    data_folder = Path("simulation/sim_data")
    available_seasons = ["2023"]  # Use one real season

    # Create manager
    manager = AccuracySimulationManager(
        baseline_config_path=baseline_path,
        data_folder=data_folder,
        available_seasons=available_seasons,
        parameter_order=['NORMALIZATION_MAX_SCALE', 'TEAM_QUALITY_SCORING_WEIGHT'],
        num_test_values=2,
        intermediate_folder=tmp_path / "intermediate",
        optimal_folder=tmp_path / "optimal"
    )

    # Run tournament optimization
    manager.run_both()

    # Verify intermediate folder for parameter 1
    param1_folder = tmp_path / "intermediate" / "accuracy_intermediate_00_NORMALIZATION_MAX_SCALE"
    assert param1_folder.exists()
    assert (param1_folder / "metadata.json").exists()
    assert (param1_folder / "league_config.json").exists()
    assert (param1_folder / "draft_config.json").exists()
    assert (param1_folder / "week1-5.json").exists()
    assert (param1_folder / "week6-9.json").exists()
    assert (param1_folder / "week10-13.json").exists()
    assert (param1_folder / "week14-17.json").exists()

    # Load metadata for parameter 1
    with open(param1_folder / "metadata.json") as f:
        metadata1 = json.load(f)
    assert metadata1['param_name'] == 'NORMALIZATION_MAX_SCALE'
    assert len(metadata1['best_mae_per_horizon']) == 5

    # Verify intermediate folder for parameter 2
    param2_folder = tmp_path / "intermediate" / "accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT"
    assert param2_folder.exists()
    assert (param2_folder / "metadata.json").exists()

    # Load metadata for parameter 2
    with open(param2_folder / "metadata.json") as f:
        metadata2 = json.load(f)
    assert metadata2['param_name'] == 'TEAM_QUALITY_SCORING_WEIGHT'

    # Verify optimal configs saved
    optimal_folder = tmp_path / "optimal"
    assert optimal_folder.exists()
    assert (optimal_folder / "league_config.json").exists()
    assert (optimal_folder / "draft_config.json").exists()

    # Verify different horizons can have different parameter values
    with open(optimal_folder / "draft_config.json") as f:
        draft_config = json.load(f)
    with open(optimal_folder / "week1-5.json") as f:
        week1_5_config = json.load(f)

    # Horizons may have different values (not required, but check they're independent)
    # Just verify configs are valid
    assert 'NORMALIZATION_MAX_SCALE' in draft_config
    assert 'TEAM_QUALITY_SCORING_WEIGHT' in draft_config
    assert 'NORMALIZATION_MAX_SCALE' in week1_5_config
    assert 'TEAM_QUALITY_SCORING_WEIGHT' in week1_5_config
```

**Verification:**
- [ ] Test created
- [ ] Uses test baseline fixture
- [ ] Uses real data from sim_data/
- [ ] Runs 2 parameters
- [ ] Verifies intermediate folders
- [ ] Verifies metadata.json
- [ ] Verifies all 6 config files
- [ ] Verifies optimal configs
- [ ] Test passes (may take 5-10 minutes)

---

### Task 3.2: Write integration test for auto-resume

- **File:** `tests/integration/test_accuracy_simulation_integration.py`
- **Test:** `test_tournament_auto_resume()`
- **Purpose:** Verify auto-resume works correctly (Q8)
- **Status:** [ ] Not started

**Implementation details:**
1. Run tournament with 2 parameters
2. Interrupt after parameter 1 completes (don't call run_both() second time)
3. Create new manager with same folders
4. Verify resume detected
5. Verify parameter 2 runs from correct baseline
6. Verify final results match non-interrupted run

**Test code structure:**
```python
def test_tournament_auto_resume(tmp_path):
    """Integration test: Verify auto-resume works after interruption."""
    # Setup
    baseline_path = Path("tests/fixtures/accuracy_test_baseline")
    data_folder = Path("simulation/sim_data")
    available_seasons = ["2023"]
    intermediate_folder = tmp_path / "intermediate"
    optimal_folder = tmp_path / "optimal"

    # First run: Complete parameter 1 only
    manager1 = AccuracySimulationManager(
        baseline_config_path=baseline_path,
        data_folder=data_folder,
        available_seasons=available_seasons,
        parameter_order=['NORMALIZATION_MAX_SCALE', 'TEAM_QUALITY_SCORING_WEIGHT'],
        num_test_values=2,
        intermediate_folder=intermediate_folder,
        optimal_folder=optimal_folder
    )

    # Manually run parameter 1 only (simulate interruption)
    # ... run first parameter ...
    # ... save intermediate results ...

    # Verify intermediate folder exists
    param1_folder = intermediate_folder / "accuracy_intermediate_00_NORMALIZATION_MAX_SCALE"
    assert param1_folder.exists()

    # Second run: Resume from interruption
    manager2 = AccuracySimulationManager(
        baseline_config_path=baseline_path,
        data_folder=data_folder,
        available_seasons=available_seasons,
        parameter_order=['NORMALIZATION_MAX_SCALE', 'TEAM_QUALITY_SCORING_WEIGHT'],
        num_test_values=2,
        intermediate_folder=intermediate_folder,
        optimal_folder=optimal_folder
    )

    # Verify resume detected
    resume_idx = manager2._detect_resume_state()
    assert resume_idx == 0  # Resumed from parameter 0 (first parameter)

    # Run tournament (should skip parameter 1, run parameter 2)
    manager2.run_both()

    # Verify parameter 2 folder created
    param2_folder = intermediate_folder / "accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT"
    assert param2_folder.exists()

    # Verify optimal configs saved
    assert optimal_folder.exists()
```

**Verification:**
- [ ] Test created
- [ ] Simulates interruption after parameter 1
- [ ] Resume detection works
- [ ] Parameter 2 runs correctly
- [ ] Final results valid
- [ ] Test passes

---

## Phase 4: Manual QA Verification (3 QC Rounds)

### Task 4.1: QC Round 1 - Functionality Verification

- **Purpose:** Verify tournament optimization works end-to-end
- **Status:** [ ] Not started

**QC Round 1 Checklist:**

**Setup:**
- [ ] All phases 1-4 complete and passing unit/integration tests
- [ ] Run: `python run_accuracy_simulation.py --test-values 3 --num-params 2 --log-level info`

**Functional Requirements:**
- [ ] Tournament optimization starts without errors
- [ ] No mode selection required (mode argument removed)
- [ ] Progress tracker shows configs, horizons, overall progress, ETA
- [ ] Parallel processing uses 8 workers by default
- [ ] New bests logged during optimization (info level)
- [ ] Parameter summaries logged after each parameter (info level)
- [ ] Intermediate folder created after parameter 1
- [ ] metadata.json present in intermediate folder with correct structure
- [ ] All 6 config files saved in intermediate folder
- [ ] Intermediate folder created after parameter 2
- [ ] Optimal configs saved to optimal folder
- [ ] All 6 config files in optimal folder

**Metadata Verification:**
- [ ] Open `intermediate/accuracy_intermediate_00_*/metadata.json`
- [ ] Verify: param_idx=0, param_name correct
- [ ] Verify: horizons_evaluated has 5 entries
- [ ] Verify: best_mae_per_horizon has 5 horizons
- [ ] Verify: timestamp present

**Config Verification:**
- [ ] Open `optimal/draft_config.json` and `optimal/week1-5.json`
- [ ] Verify: Both parameters present (NORMALIZATION_MAX_SCALE, TEAM_QUALITY_SCORING_WEIGHT)
- [ ] Verify: Values may differ between horizons (independent optimization)
- [ ] Verify: All other parameters present (default values)

**Performance:**
- [ ] Note total runtime
- [ ] Verify parallel processing is faster than sequential would be
- [ ] Verify no long pauses or hangs

**Error Handling:**
- [ ] No errors in output
- [ ] No warnings (unless expected)
- [ ] Clean termination

**If any item fails:** Document issue, fix, re-run QC Round 1

---

### Task 4.2: QC Round 2 - Edge Cases and Robustness

- **Purpose:** Test edge cases and error handling
- **Status:** [ ] Not started

**QC Round 2 Checklist:**

**Test: Debug logging**
- [ ] Run: `python run_accuracy_simulation.py --test-values 2 --num-params 1 --log-level debug`
- [ ] Verify: Each config evaluation logged with all 5 MAE values
- [ ] Verify: Baseline updates logged with old→new values
- [ ] Verify: Much more verbose than info level

**Test: Different worker counts**
- [ ] Run: `python run_accuracy_simulation.py --test-values 2 --num-params 1 --max-workers 4`
- [ ] Verify: Uses 4 workers
- [ ] Verify: Results correct
- [ ] Run: `python run_accuracy_simulation.py --test-values 2 --num-params 1 --max-workers 1`
- [ ] Verify: Sequential execution (1 worker)
- [ ] Verify: Results match parallel execution

**Test: ThreadPoolExecutor fallback**
- [ ] Run: `python run_accuracy_simulation.py --test-values 2 --num-params 1 --no-use-processes`
- [ ] Verify: Uses ThreadPoolExecutor instead of ProcessPoolExecutor
- [ ] Verify: Results correct (slower than processes)

**Test: Auto-resume (manual interruption)**
- [ ] Start: `python run_accuracy_simulation.py --test-values 3 --num-params 3`
- [ ] Wait for parameter 1 to complete
- [ ] Interrupt (Ctrl+C)
- [ ] Verify: Intermediate folder exists for parameter 1
- [ ] Resume: `python run_accuracy_simulation.py --test-values 3 --num-params 3`
- [ ] Verify: Resumes from parameter 2
- [ ] Verify: Skips parameter 1
- [ ] Verify: Parameters 2-3 complete successfully
- [ ] Verify: Final results valid

**Test: Horizon divergence (real data)**
- [ ] Run: `python run_accuracy_simulation.py --test-values 5 --num-params 2`
- [ ] After completion, open optimal configs
- [ ] Compare `draft_config.json` vs `week1-5.json` vs `week14-17.json`
- [ ] Document: Do horizons have different parameter values? (Expected: possibly yes)
- [ ] Document: MAE values per horizon from final log summary

**If any item fails:** Document issue, fix, re-run QC Round 2

---

### Task 4.3: QC Round 3 - Performance and Scalability

- **Purpose:** Verify performance at scale
- **Status:** [ ] Not started

**QC Round 3 Checklist:**

**Test: Full parameter order (3 parameters)**
- [ ] Run: `python run_accuracy_simulation.py --test-values 5 --num-params 3 --max-workers 8`
- [ ] Note: Total configs = 105 (5 horizons × 21 values)
- [ ] Note: Total evaluations = 525 per parameter (105 configs × 5 horizons)
- [ ] Verify: Completes without errors
- [ ] Document: Total runtime for 3 parameters
- [ ] Document: Average time per parameter
- [ ] Document: Average time per config evaluation
- [ ] Verify: ETA estimates reasonable
- [ ] Verify: Progress tracking accurate

**Test: Memory usage**
- [ ] Monitor memory during optimization
- [ ] Verify: No memory leaks
- [ ] Verify: Memory usage stable across parameters
- [ ] Document: Peak memory usage

**Test: CPU utilization**
- [ ] Monitor CPU usage during optimization
- [ ] Verify: All 8 cores utilized (with 8 workers)
- [ ] Document: Average CPU utilization

**Test: Results quality**
- [ ] After full run, inspect final MAE values
- [ ] Verify: MAE decreases or stays stable across parameters (optimization working)
- [ ] Verify: MAE values reasonable (not 0.0, not extremely high)
- [ ] Document: Final MAE per horizon

**Comparison to old ROS/weekly modes (if available):**
- [ ] Compare runtime: Tournament vs old modes
- [ ] Compare results: MAE values similar quality?
- [ ] Document: Any significant differences

**If any item fails:** Document issue, fix, re-run QC Round 3

---

## Phase 5: Final Validation

### Task 5.1: Verify all test fixtures work correctly

- **Purpose:** Ensure test baseline configs loadable
- **Status:** [ ] Not started

**Validation steps:**
1. Read all 6 files from `tests/fixtures/accuracy_test_baseline/`
2. Verify ConfigGenerator can load them without errors
3. Verify generate_horizon_test_values() returns expected ranges
4. Verify test runs complete successfully

**Verification script:**
```python
from pathlib import Path
from simulation.shared.ConfigGenerator import ConfigGenerator

# Load test baseline
baseline_path = Path("tests/fixtures/accuracy_test_baseline")
gen = ConfigGenerator(baseline_path)

# Verify 5 horizons loaded
print(f"Loaded horizons: {list(gen.baseline_configs.keys())}")
# Expected: ['ros', '1-5', '6-9', '10-13', '14-17']

# Verify test values generation
test_values = gen.generate_horizon_test_values('NORMALIZATION_MAX_SCALE')
print(f"Test values: {test_values}")
# Expected: dict with 5 keys, each with 2-3 values

# Run quick test
# python run_accuracy_simulation.py --baseline tests/fixtures/accuracy_test_baseline --test-values 2 --num-params 1
```

**Checklist:**
- [ ] All 6 config files exist in `tests/fixtures/accuracy_test_baseline/`
- [ ] Files are valid JSON
- [ ] ConfigGenerator loads them without errors
- [ ] Test values generated correctly (2-3 per parameter)
- [ ] Test run completes in reasonable time (~5 minutes)

---

### Task 5.2: Run all unit tests and verify 100% pass rate

- **Command:** `python tests/run_all_tests.py`
- **Status:** [ ] Not started

**Verification:**
- [ ] All unit tests pass
- [ ] No test failures
- [ ] No test errors
- [ ] New tests added:
  - [ ] test_is_better_than_rejects_zero_players
  - [ ] test_is_better_than_both_zero_players
  - [ ] test_tournament_horizon_divergence
- [ ] Integration tests pass:
  - [ ] test_tournament_optimization_two_parameters
  - [ ] test_tournament_auto_resume

---

### Task 5.3: Final smoke test with full optimization

- **Purpose:** End-to-end validation with realistic parameters
- **Status:** [ ] Not started

**Smoke test:**
```bash
# Run tournament optimization with realistic settings
python run_accuracy_simulation.py \
  --test-values 10 \
  --num-params 5 \
  --max-workers 8 \
  --log-level info
```

**Verification:**
- [ ] Optimization completes without errors
- [ ] All 5 parameters optimize successfully
- [ ] Intermediate folders created for all 5 parameters
- [ ] All metadata.json files present and valid
- [ ] Optimal configs saved with all 6 files
- [ ] Results quality reasonable (MAE values make sense)
- [ ] Runtime acceptable (document actual time)
- [ ] No memory issues
- [ ] No CPU issues
- [ ] Progress tracking accurate throughout

**Final results documentation:**
- [ ] Document final MAE per horizon
- [ ] Document total runtime
- [ ] Document average time per parameter
- [ ] Document any unexpected behavior
- [ ] Document lessons learned for future optimizations

---

### QA CHECKPOINT 5: Final Validation

- **Status:** [ ] Not started
- **Expected outcome:** All tests pass, QC rounds complete, feature ready for production
- **Verify:**
  - [ ] All unit tests pass (100%)
  - [ ] All integration tests pass
  - [ ] QC Round 1 complete (all items checked)
  - [ ] QC Round 2 complete (all items checked)
  - [ ] QC Round 3 complete (all items checked)
  - [ ] Test fixtures verified
  - [ ] Final smoke test passed
  - [ ] No known issues or bugs
  - [ ] Documentation updated
  - [ ] Lessons learned documented
  - [ ] Feature ready to move to done/

**If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### Test Fixtures
- **Location:** `tests/fixtures/accuracy_test_baseline/`
- **Files:** 6 config files (league + 5 horizons)
- **Purpose:** Fast unit/integration tests
- **Verified:** [ ]

### Unit Tests
- **Location:** `tests/simulation/test_AccuracyResultsManager.py`, `test_AccuracySimulationManager.py`
- **New tests:** 3 (is_better_than × 2, horizon_divergence × 1)
- **Verified:** [ ]

### Integration Tests
- **Location:** `tests/integration/test_accuracy_simulation_integration.py`
- **New tests:** 2 (two_parameters, auto_resume)
- **Verified:** [ ]

### Quick E2E Validation Plan
- **Minimal test command:**
  ```bash
  python tests/run_all_tests.py
  ```
- **Expected result:**
  - All tests pass
  - New tests included
  - Integration tests complete in reasonable time
- **Run before:** Marking feature complete
- **Status:** [ ] Not run | [ ] Passed | [ ] Failed (fix before proceeding)

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| Test fixtures | tests/fixtures/ | ConfigGenerator | (test code) | Task 5.1 (verify loads) |
| Unit tests | tests/simulation/ | run_all_tests.py | tests/run_all_tests.py:~50 | Task 1.1, 1.2, 2.1 (create tests) |
| Integration tests | tests/integration/ | run_all_tests.py | tests/run_all_tests.py:~80 | Task 3.1, 3.2 (create tests) |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Q31 Resolution | Test baseline configs | tests/fixtures/accuracy_test_baseline/ | 6 files with minimal ranges |
| Q32 Resolution | 2-parameter test coverage | test_tournament_optimization_two_parameters() | Validates progression |
| Q33 Resolution | Synthetic + real data | Unit tests (synthetic), Integration tests (real) | Both types |
| Q34 Resolution | Divergence verification | test_tournament_horizon_divergence() + QC Round 2 | Unit test + manual QA |

---

## Data Flow Traces

### Requirement: Unit test with mocked MAE for divergence
```
Entry: test_tournament_horizon_divergence()
  → Mock AccuracyCalculator
  → Return different MAE values per horizon:
      - ros prefers value 100
      - 1-5 prefers value 150
      - 14-17 prefers value 200
  → Run tournament optimization
  → Verify each horizon selected its preferred value
  → Result: Proves system CAN handle divergence
```

### Requirement: Integration test with 2 parameters
```
Entry: test_tournament_optimization_two_parameters()
  → Load test baseline from fixtures
  → Use real data from sim_data/2023
  → Run tournament with 2 parameters
  → Verify intermediate folder after parameter 1:
      - All 6 config files present
      - metadata.json present with correct structure
  → Verify intermediate folder after parameter 2:
      - All 6 config files present
      - metadata.json present
  → Verify optimal folder:
      - All 6 config files present
      - Both parameters optimized
  → Result: Validates tournament progression and baseline updates
```

### Requirement: Manual QA for real divergence
```
Entry: QC Round 2 - Horizon divergence test
  → Run real optimization: --test-values 5 --num-params 2
  → Inspect optimal configs:
      - draft_config.json (ROS horizon)
      - week1-5.json
      - week14-17.json
  → Compare parameter values across horizons
  → Document: Did horizons naturally diverge?
  → Result: Validates real-world behavior
```

---

## Verification Gaps

Document any gaps found during iterations here:

### Iteration {X} Gaps
(To be filled during verification iterations)

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:** (To be filled)
- **Corrections made:** (To be filled)
- **Confidence level:** (To be filled)

### Round 2 (Iteration 13)
- **Verified correct:** (To be filled)
- **Corrections made:** (To be filled)
- **Confidence level:** (To be filled)

### Round 3 (Iteration 22)
- **Verified correct:** (To be filled)
- **Corrections made:** (To be filled)
- **Confidence level:** (To be filled)

---

## Integration Gap Check Results

### Check 1 (Iteration 7)
**Every new method has a caller:**
- [ ] Test fixtures: Loaded by ConfigGenerator in tests
- [ ] Unit tests: Called by run_all_tests.py
- [ ] Integration tests: Called by run_all_tests.py

**Every caller modified:**
- [ ] Task 5.1: ConfigGenerator loads test fixtures
- [ ] Task 5.2: run_all_tests.py includes new tests

**Status:** (To be filled)

### Check 2 (Iteration 14)
(To be filled)

### Check 3 (Iteration 23)
(To be filled)

---

## Notes

- This is Phase 5 of 5 sub-features (FINAL PHASE)
- Quality assurance and validation
- 3 QC rounds provide comprehensive coverage
- Unit tests prove mechanism works
- Integration tests validate real-world behavior
- Manual QA catches edge cases
- Must complete all 24 verification iterations before implementing
- Dependencies: Phases 1-4 (Core Fixes, Tournament Rewrite, Parallel Processing, CLI & Logging) must be complete
- Next phase: None - after this phase, feature is complete and ready to move to done/
