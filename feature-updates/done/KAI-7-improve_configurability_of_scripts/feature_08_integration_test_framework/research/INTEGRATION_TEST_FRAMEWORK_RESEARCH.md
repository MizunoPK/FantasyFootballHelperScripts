# Integration Test Framework Research

**Feature:** Feature 08 - Integration Test Framework
**Date:** 2026-01-29
**Researcher:** Secondary-G
**Research Phase:** S2.P1 Phase 1 (Feature-Specific Research)

---

## Research Questions & Answers

### Q1: What existing integration test patterns exist in the codebase?

**Answer:** 5 integration test files found in `tests/integration/`:

1. `test_simulation_integration.py` (win rate simulation)
2. `test_accuracy_simulation_integration.py` (accuracy simulation)
3. `test_data_fetcher_integration.py`
4. `test_game_conditions_integration.py`
5. `test_league_helper_integration.py`

**Pattern Observations:**
- **Test framework:** pytest (NOT unittest)
- **Test structure:** Class-based organization (`class TestX`)
- **Test fixtures:** Use `@pytest.fixture` for test data setup
- **Mock data:** Helper functions create realistic test data structures
- **Test levels:** Test initialization, API calls, workflows (not just end-to-end)

---

### Q2: Where are the 2 existing simulation integration tests located?

**Answer:**
- **Win Rate Simulation:** `tests/integration/test_simulation_integration.py` (535 lines)
- **Accuracy Simulation:** `tests/integration/test_accuracy_simulation_integration.py` (711 lines)

**Current State:**
- Both files exist and use pytest framework
- Both follow same structural patterns (fixtures, class-based tests, mock data)
- Both test initialization + API calls + workflows (not full E2E due to complexity)
- Both use `@pytest.mark.skip` for complex tests requiring full data environment

**Enhancement Needed (from Discovery):**
- Add E2E test mode validation (--e2e-test flag behavior)
- Add debug mode validation (--debug flag = logging + behavioral changes)
- Add multiple argument combination tests
- Add outcome validation beyond exit codes

---

### Q3: What test framework is used?

**Answer:** **pytest** (NOT unittest)

**Evidence:**
- All existing integration tests import pytest: `import pytest`
- Use pytest fixtures: `@pytest.fixture`
- Use pytest markers: `@pytest.mark.skip`
- Test discovery relies on pytest conventions (test_*.py, test_*)
- Test runner (`run_all_tests.py`) invokes pytest subprocess

**Implications for Feature 08:**
- All 7 new test runners MUST use pytest
- Enhancement of existing tests MUST maintain pytest patterns
- Master runner can leverage existing pytest infrastructure

---

### Q4: How do existing tests validate outcomes beyond exit codes?

**Answer:** Comprehensive validation using **assertions** (not just exit code checks):

**Validation Patterns Found:**

1. **Object Initialization:**
   ```python
   assert manager is not None
   assert hasattr(manager, 'baseline_configs')
   ```

2. **Attribute Validation:**
   ```python
   assert manager.output_dir == output_dir
   assert runner.max_workers == 2
   ```

3. **Count Validation:**
   ```python
   assert len(generator.baseline_configs) == 4
   assert result.player_count > 0
   ```

4. **Result Validation:**
   ```python
   assert result.mae > 0
   assert abs(win_rate - expected_rate) < 0.001
   ```

5. **File Existence Checks:**
   ```python
   assert optimal_path.exists()
   assert (optimal_path / 'league_config.json').exists()
   ```

6. **Data Correctness:**
   ```python
   assert result.config_id == "test_config_1"
   assert best.num_simulations == 2
   ```

**Exit Code Validation:**
- Implicitly validated by pytest (test passes = exit code 0, test fails = exit code 1)
- NO explicit `subprocess.run(...).returncode == 0` checks in existing tests

**Key Insight:** Tests use **direct Python imports** and method calls (NOT subprocess invocation), so exit codes are handled by pytest framework automatically.

---

### Q5: What is the current test directory structure?

**Answer:**

```
tests/
├── README.md                          # Test documentation
├── conftest.py                        # Pytest configuration (path setup)
├── run_all_tests.py                   # Master test runner (100% pass requirement)
├── integration/                       # Integration tests folder
│   ├── test_simulation_integration.py       # Win rate sim (535 lines)
│   ├── test_accuracy_simulation_integration.py  # Accuracy sim (711 lines)
│   ├── test_data_fetcher_integration.py
│   ├── test_game_conditions_integration.py
│   └── test_league_helper_integration.py
├── league_helper/                     # League helper unit tests
│   ├── util/
│   ├── add_to_roster_mode/
│   └── trade_simulator_mode/
├── player-data-fetcher/               # Player fetcher unit tests
├── simulation/                        # Simulation unit tests
├── utils/                             # Utils unit tests
└── root_scripts/                      # Root scripts unit tests
```

**Observations:**
- Integration tests live in dedicated `tests/integration/` folder
- Test structure mirrors source code structure
- Test naming convention: `test_<module>_integration.py`

---

### Q6: How are tests currently run?

**Answer:** Two methods:

**Method 1: Master Test Runner (Recommended)**
```bash
python tests/run_all_tests.py
python tests/run_all_tests.py --verbose
python tests/run_all_tests.py --detailed
python tests/run_all_tests.py --single  # All tests in one pytest command
```

**Exit Codes:**
- `0` = All tests passed (100%)
- `1` = One or more tests failed (< 100%)

**Method 2: Direct Pytest**
```bash
.venv/bin/python -m pytest tests/ -v
.venv/bin/python -m pytest tests/integration/test_simulation_integration.py -v
```

**Master Runner Features (`run_all_tests.py`):**
- Discovers all `test_*.py` files recursively
- Runs pytest on each file
- Parses output for pass/fail counts
- Validates 100% pass requirement
- Detailed reporting per file

**Implications for Feature 08:**
- New integration tests will be automatically discovered by existing runner
- Can reuse `run_all_tests.py` pattern OR create integration-specific runner
- Must maintain 100% pass requirement

---

### Q7: What assertion utilities are available for validation?

**Answer:**

**Pytest Built-in Assertions:**
- `assert` statements (Python native)
- `pytest.raises(Exception)` for exception testing
- `pytest.warns(Warning)` for warning testing
- `pytest.approx()` for floating-point comparison

**Mock Utilities:**
- `unittest.mock.Mock` - Create mock objects
- `unittest.mock.MagicMock` - Mock with magic methods
- `unittest.mock.patch` - Patch imports and methods
- `@pytest.fixture` - Create reusable test data

**Custom Assertions (Available):**
- None found - tests use standard pytest assertions
- Could create custom assertion helpers if needed

**File System Utilities:**
- `pathlib.Path` for path operations
- `.exists()`, `.is_file()`, `.read_text()` for file checks
- `tmp_path` fixture for temporary directories

---

### Q8: How do tests invoke runner scripts?

**Answer:** **Direct Python imports** (NOT subprocess calls)

**Pattern Found in Existing Tests:**
```python
# Direct imports from modules
from ConfigGenerator import ConfigGenerator
from SimulationManager import SimulationManager

# Direct method calls (no subprocess)
manager = SimulationManager(...)
manager.run_single_config_test()
results = manager.results_manager.get_best_config()
```

**NO subprocess patterns found like:**
```python
# This pattern is NOT used
subprocess.run(["python", "run_simulation.py", "--args"])
```

**Why Direct Imports?**
- Faster execution (no process spawning overhead)
- Better error messages (direct Python stack traces)
- Easier debugging (can use debugger directly)
- More granular testing (can test individual methods, not just end-to-end)

**Implications for Feature 08:**
- New tests should use **direct imports** of runner script logic
- Tests will import modules/classes from runner scripts, not subprocess them
- Need to refactor runner scripts to separate:
  - **CLI parsing** (argparse logic)
  - **Core functionality** (importable modules)
  - **Main execution** (if __name__ == "__main__")

---

## 7 Runner Scripts to Test

Based on Discovery document Feature 01-07:

| # | Script | Feature | Current State | Test Needed |
|---|--------|---------|---------------|-------------|
| 1 | `run_player_fetcher.py` | Feature 01 | No argparse | Add argparse + E2E + debug modes |
| 2 | `run_schedule_fetcher.py` | Feature 02 | No argparse | Add argparse + E2E + debug modes |
| 3 | `run_game_data_fetcher.py` | Feature 03 | Has argparse | Enhance with E2E + debug modes |
| 4 | `compile_historical_data.py` | Feature 04 | Has argparse | Enhance with E2E + debug modes |
| 5 | `run_win_rate_simulation.py` | Feature 05 | Has argparse | Add E2E mode (has log-level) |
| 6 | `run_accuracy_simulation.py` | Feature 06 | Has argparse | Add E2E mode (has log-level) |
| 7 | `run_league_helper.py` | Feature 07 | No argparse | Add argparse + mode selection + E2E + debug |

**Note:** `compile_historical_data.py` is NOT prefixed with `run_` but is still a runner script.

---

## Test Framework Implementation Patterns

### Pattern 1: Fixtures for Test Data Setup

```python
@pytest.fixture
def temp_simulation_data(tmp_path):
    """Create temporary simulation data folder"""
    data_folder = tmp_path / "sim_data"
    data_folder.mkdir()
    # Create mock data structure
    return data_folder

@pytest.fixture
def baseline_config(tmp_path):
    """Create baseline configuration folder"""
    config_folder = tmp_path / "test_configs"
    # Create config files
    return config_folder
```

**Usage in Tests:**
```python
def test_manager_initializes(baseline_config, temp_simulation_data, tmp_path):
    manager = SimulationManager(
        baseline_config_path=baseline_config,
        data_folder=temp_simulation_data,
        ...
    )
    assert manager is not None
```

---

### Pattern 2: Class-Based Test Organization

```python
class TestConfigGeneratorIntegration:
    """Integration tests for config generator"""

    def test_config_generator_loads_baseline(self, baseline_config):
        generator = ConfigGenerator(baseline_config)
        assert generator is not None
        assert len(generator.baseline_configs) == 4

    def test_config_generator_creates_combinations(self, baseline_config):
        generator = ConfigGenerator(baseline_config, num_test_values=1)
        test_values = generator.generate_horizon_test_values('WEIGHT')
        assert len(test_values) >= 1
```

---

### Pattern 3: Mock Data Creation Helpers

```python
def create_mock_historical_season(data_folder: Path, year: str = "2024") -> None:
    """Create a mock historical season folder structure"""
    season_folder = data_folder / year
    season_folder.mkdir(parents=True, exist_ok=True)

    # Create required files
    (season_folder / "season_schedule.csv").write_text("week,home,away\n1,KC,DET\n")
    (season_folder / "game_data.csv").write_text("week,home,away\n1,KC,DET\n")

    # Create week folders with JSON files
    weeks_folder = season_folder / "weeks"
    weeks_folder.mkdir(exist_ok=True)
    for week_num in range(1, 18):
        week_folder = weeks_folder / f"week_{week_num:02d}"
        week_folder.mkdir(exist_ok=True)
        # Create position JSON files
        ...
```

---

### Pattern 4: Test Skip Markers for Complex Tests

```python
@pytest.mark.skip(reason="Complex integration test requires full data environment")
def test_complete_workflow(self, baseline_config, temp_data):
    """Test complete workflow: init → run → get results"""
    # Test implementation
    ...
```

**Why Skip:**
- Complex tests require complete environment setup
- Simplified test data may not satisfy all dependencies
- Basic functionality verified by simpler tests + smoke tests

---

## Test Validation Requirements (from Discovery)

From User Answer Q5 (Discovery line 28):
> "Check exit code AND verify expected outcomes (specific logs, result counts)"

**Required Validation for Each Test:**

1. **Exit Code Validation**
   - Implicitly via pytest (test pass = exit code 0)
   - NO explicit subprocess.returncode checks needed (using direct imports)

2. **Specific Outcome Validation** (Examples):
   - **Log Counts:** Check DEBUG logs are enabled in debug mode
   - **File Existence:** Verify output files created
   - **Result Counts:** Validate number of players/results
   - **Output Content:** Check specific data in output files
   - **Behavioral Changes:** Verify debug mode reduces iterations/data
   - **Performance:** Verify E2E mode completes in ≤3 minutes

---

## Master Test Runner Analysis

**Existing Master Runner:** `tests/run_all_tests.py` (324 lines)

**Features:**
- Discovers all `test_*.py` files recursively
- Runs pytest on each file individually
- Parses output for pass/fail counts
- Validates 100% pass requirement
- Detailed reporting per file
- Exit codes: 0 = all pass, 1 = any fail
- Two modes: per-file (default) or single command (--single)

**For Feature 08:**

**Option 1:** Reuse existing `run_all_tests.py`
- **Pros:** Already discovers integration tests automatically, no new code needed
- **Cons:** Runs ALL tests (unit + integration), can't run integration tests alone

**Option 2:** Create `tests/integration/run_integration_tests.py`
- **Pros:** Run integration tests independently, faster for integration-only testing
- **Cons:** Need to create new runner, maintain two runners

**Option 3:** Create `run_all_integration_tests.py` at project root
- **Pros:** Easier to find (project root), matches Discovery requirement ("master integration test runner")
- **Cons:** Duplicate logic from run_all_tests.py, confusion with existing runner

**Recommendation:** **Option 1** (reuse existing runner) with **Option 2** (integration-specific runner) as enhancement
- Existing runner works immediately for all tests
- Integration-specific runner added for convenience/speed
- Both runners can coexist without conflict

---

## Key Implementation Insights

### Insight 1: Direct Imports vs Subprocess

**Finding:** All existing integration tests use **direct Python imports**, NOT subprocess calls.

**Implications:**
- Runner scripts need refactoring to expose importable logic
- CLI parsing (argparse) should be separate from core functionality
- Tests import modules/classes directly and call methods
- Exit codes validated implicitly by pytest (test pass = exit 0)

**Example Refactoring Pattern:**
```python
# BEFORE (monolithic runner)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # ... argparse setup ...
    args = parser.parse_args()
    # ... business logic inline ...

# AFTER (importable + testable)
class PlayerFetcherRunner:
    def __init__(self, week, output_dir, debug=False):
        self.week = week
        self.output_dir = output_dir
        self.debug = debug

    def run(self):
        # Business logic here (importable)
        ...

def main():
    parser = argparse.ArgumentParser()
    # ... argparse setup ...
    args = parser.parse_args()

    runner = PlayerFetcherRunner(args.week, args.output_dir, args.debug)
    runner.run()

if __name__ == "__main__":
    main()
```

**Tests can then import:**
```python
from run_player_fetcher import PlayerFetcherRunner

def test_player_fetcher_debug_mode():
    runner = PlayerFetcherRunner(week=1, output_dir=tmp_path, debug=True)
    runner.run()
    # Validate debug behavior
    assert runner.debug_mode_active
```

---

### Insight 2: E2E Mode Needs Specific Validation

**From Discovery User Answer Q3:**
> "Simulations: single run with 0-1 random configs. Fetchers: real APIs with data limiting args"

**Validation Requirements for E2E Mode:**
- **Performance:** Verify completion time ≤3 minutes
- **Behavior:** Verify single run (simulations) or limited data (fetchers)
- **Arguments:** Verify --e2e-test flag triggers correct behavior
- **Output:** Verify expected minimal output (not full production output)

**Example Test Pattern:**
```python
import time

def test_e2e_mode_completes_quickly(tmp_path):
    runner = SimulationRunner(
        config_path=tmp_path,
        e2e_test=True  # E2E mode enabled
    )

    start = time.time()
    runner.run()
    duration = time.time() - start

    # Verify completes in ≤3 minutes
    assert duration <= 180, f"E2E mode took {duration}s (expected ≤180s)"

    # Verify single run (not multiple configs)
    assert runner.num_configs_tested == 1
```

---

### Insight 3: Debug Mode = Logging + Behavioral Changes

**From Discovery User Answer Q4:**
> "Option C: Both logging AND behavioral changes"

**Validation Requirements for Debug Mode:**
- **Logging:** Verify DEBUG log level enabled
- **Behavioral Changes:** Verify reduced iterations, smaller datasets, verbose output

**Example Test Pattern:**
```python
import logging

def test_debug_mode_enables_logging_and_behavior(tmp_path, caplog):
    caplog.set_level(logging.DEBUG)

    runner = FetcherRunner(
        output_dir=tmp_path,
        debug=True  # Debug mode enabled
    )
    runner.run()

    # Verify DEBUG logging enabled
    assert any(record.levelno == logging.DEBUG for record in caplog.records)

    # Verify behavioral changes
    assert runner.dataset_size < runner.NORMAL_DATASET_SIZE
    assert runner.iterations < runner.NORMAL_ITERATIONS
```

---

### Insight 4: Multiple Argument Combinations Testing

**From Discovery In Scope (line 212):**
> "Tests cover multiple argument combinations per script"

**Pattern:** Test various combinations of arguments to ensure compatibility

**Example Test Pattern:**
```python
@pytest.mark.parametrize("week,debug,e2e", [
    (1, False, False),  # Normal mode
    (5, True, False),   # Debug mode
    (10, False, True),  # E2E mode
    (14, True, True),   # Debug + E2E mode (edge case)
])
def test_argument_combinations(tmp_path, week, debug, e2e):
    runner = FetcherRunner(
        week=week,
        output_dir=tmp_path,
        debug=debug,
        e2e_test=e2e
    )
    runner.run()

    # Verify successful execution
    assert runner.exit_code == 0

    # Verify output files exist
    assert (tmp_path / f"week_{week}_data.json").exists()
```

---

## Research Summary

**Completed Research Questions:** 8/8 ✅

**Key Findings:**
1. **Test Framework:** pytest (NOT unittest)
2. **Existing Tests:** 5 integration tests (2 simulation tests to enhance)
3. **Test Pattern:** Direct imports (NOT subprocess), fixtures, class-based organization
4. **Validation:** Exit code (implicit) + specific outcomes (assertions)
5. **Master Runner:** Exists (`run_all_tests.py`), can be reused or augmented
6. **7 Scripts:** All identified (1-7 from Features 01-07)
7. **Runner Refactoring Needed:** Separate CLI parsing from core logic for testability
8. **Test Requirements:** E2E performance, debug behavior, multiple arg combinations

**Next Steps:**
- Phase 1.5: Research Completeness Audit (verify all questions answered)
- S2.P2: Specification Phase (create detailed spec.md based on research)

---

**Research Status:** COMPLETE
**Date Completed:** 2026-01-29
**Time Spent:** ~60 minutes
