# Research Notes: accuracy_simulation_e2e (Feature 06)

**Research Date:** 2026-02-18
**Researcher:** Secondary-E (S2.P1.I1)

---

## Files Researched

### Primary File: run_accuracy_simulation.py

**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/run_accuracy_simulation.py`
**Lines:** 330 total

**Current argparse setup (10 add_argument calls, lines 159-234):**
| Line | Argument | Type | Default | Note |
|------|----------|------|---------|------|
| 159 | `--baseline` | str | `''` | Path to baseline config folder |
| 167 | `--output` | str | `'simulation/simulation_configs'` | Output directory |
| 173 | `--data` | str | `'simulation/sim_data'` | Path to sim_data folder |
| 180 | `--test-values` | int | `3` | Test values per parameter |
| 187 | `--num-params` | int | `1` | Params to test at once |
| 195 | `--max-workers` | int | `8` | Parallel workers |
| 202 | `--use-processes` | flag | `True` | Use ProcessPoolExecutor |
| 209 | `--no-use-processes` | flag | - | Complement of --use-processes |
| 216 | `--log-level` | str | `'info'` | choices: `['debug', 'info', 'warning', 'error']` — **lowercase, missing 'critical'** |
| 227 | `--enable-log-file` | flag | `False` | File logging |

**Module-level constants (lines 52-97):**
- `DEFAULT_LOG_LEVEL = 'info'` (line 53) — used as --log-level default
- `LOGGING_TO_FILE = False` (line 54) — not CLI-configurable (fixed)
- `LOG_NAME = "accuracy_simulation"` (line 55) — not CLI-configurable
- `LOGGING_FORMAT = "detailed"` (line 58) — not CLI-configurable
- `DEFAULT_BASELINE = ''` (line 61) — used as --baseline default
- `DEFAULT_OUTPUT = 'simulation/simulation_configs'` (line 62) — used as --output default
- `DEFAULT_DATA = 'simulation/sim_data'` (line 63) — used as --data default
- `DEFAULT_TEST_VALUES = 3` (line 64) — used as --test-values default
- `NUM_PARAMETERS_TO_TEST = 1` (line 65) — used as --num-params default
- `DEFAULT_MAX_WORKERS = 8` (line 67) — used as --max-workers default
- `DEFAULT_USE_PROCESSES = True` (line 69) — used as --use-processes default
- `PARAMETER_ORDER` (lines 80-97) — list of 16 prediction parameter names

**Key finding:** NO config module imports. `run_accuracy_simulation.py` imports only:
- `argparse, signal, sys` (stdlib)
- `pathlib.Path` (stdlib)
- `AccuracySimulationManager` from simulation/accuracy/
- `setup_logger, get_logger` from utils/LoggingManager

**--log-level critical finding (line 240):**
```python
setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)
```
The `.upper()` call converts lowercase 'info' → 'INFO' before passing to setup_logger. This means functionally the existing lowercase choices work identically to uppercase choices at runtime.

**AccuracySimulationManager construction (lines 292-305):**
```python
manager = AccuracySimulationManager(
    baseline_config_path=baseline_path,
    output_dir=output_path,
    data_folder=data_path,
    parameter_order=PARAMETER_ORDER,  # <- Uses module-level PARAMETER_ORDER
    num_test_values=args.test_values,
    num_parameters_to_test=args.num_params,
    max_workers=args.max_workers,
    use_processes=args.use_processes
)
```

**E2E mode scope insight:** For E2E mode, we need to pass a SUBSET of PARAMETER_ORDER (e.g., just `['NORMALIZATION_MAX_SCALE']`) to limit the simulation to 1 parameter. The AccuracySimulationManager constructor accepts `parameter_order` as a list, so we can pass a subset directly. No changes to AccuracySimulationManager needed.

---

### AccuracySimulationManager

**Location:** `simulation/accuracy/AccuracySimulationManager.py`
**Key finding:** Already uses constructor parameter pattern — all configuration passed through constructor.

**Constructor signature (lines 71-81):**
```python
def __init__(
    self,
    baseline_config_path: Path,
    output_dir: Path,
    data_folder: Path,
    parameter_order: List[str],
    num_test_values: int = 5,
    num_parameters_to_test: int = 1,
    max_workers: int = 8,
    use_processes: bool = True
) -> None:
```

**`run_both()` parameter loop (lines 774-779):**
```python
for param_idx, param_name in enumerate(self.parameter_order):
    # Loops ALL parameters in self.parameter_order — not limited by num_parameters_to_test
```
**Critical finding:** `num_parameters_to_test` stored in `self.num_parameters_to_test` but NOT used to limit the loop in `run_both()`. The `parameter_order` list length determines how many parameters are actually tested.
→ **E2E mode must pass a SHORT `parameter_order` list, not set `--num-params`**

---

### Existing Test Files

**File 1:** `tests/root_scripts/test_run_accuracy_simulation.py` (58 tests)
- Tests CLI flags, logging setup, log quality
- `create_test_parser()` helper (line 581) mirrors actual parser with lowercase --log-level choices
- `test_existing_log_level_flag_unchanged` (line 86): passes `'debug'` lowercase — will fail if choices change to uppercase-only
- No tests yet for --debug or --e2e-test flags

**File 2:** `tests/integration/test_accuracy_simulation_integration.py`
- Tests AccuracyCalculator, AccuracyResultsManager, AccuracySimulationManager internals
- NOTE: Feature 08 will add a CLI test class to this file (not Feature 06's job)

---

### Simulation Module Structure

**Files in simulation/accuracy/:**
- `AccuracySimulationManager.py` — orchestrator
- `AccuracyCalculator.py` — MAE calculation
- `AccuracyResultsManager.py` — results tracking
- `ParallelAccuracyRunner.py` — parallel execution
- `__init__.py`

**No config.py or constants.py in simulation/** — confirmed.

---

## Integration Points

| Integration Point | Finding |
|-------------------|---------|
| AccuracySimulationManager constructor | Already accepts all params — no changes needed to internal modules |
| parameter_order handling | Pass subset list from runner to limit E2E/debug scope |
| Logging setup | `setup_logger(LOG_NAME, args.log_level.upper(), ...)` at line 240 — add debug override before this call |
| Test file `create_test_parser()` | Needs updating if --log-level choices change |

---

## Compatibility Findings

**No external library dependencies** for new features — only stdlib argparse changes.

**AccuracySimulationManager compatibility:**
- Adding --debug/--e2e-test does NOT require changes to AccuracySimulationManager
- E2E mode: pass `parameter_order=['NORMALIZATION_MAX_SCALE']` + `num_test_values=1`
- Debug mode: force DEBUG logging + optionally same scope reduction as E2E

---

## Design Correction Applied (2026-02-18)

**No --debug flag in this epic.** Handoff package correction (top of file) clarifies:
- Universal args: `--e2e-test` + `--log-level` only (2 args, not 3)
- `--e2e-test` serves both fast-mode AND debugging purposes
- Developers use `--e2e-test --log-level DEBUG` for verbose debug sessions

Feature 01 spec confirmed this — universal args table shows `--e2e-test` and `--log-level` only.

## Open Questions Identified During Research

1. **Q1 (--log-level normalization):** ANSWERED by Feature 01 precedent — use `type=str.upper` + uppercase choices + add CRITICAL
2. **Q2 (--debug scope reduction):** ELIMINATED — no --debug flag in this epic
3. **Q3 (--e2e-test max_workers):** Keep default 8 vs force 1 for test environments — see checklist.md

---

## Gate 1 Evidence (Research Completeness Audit)

| Category | Evidence |
|----------|----------|
| **Cat 1: Exact files/classes to modify (with line numbers)** | `run_accuracy_simulation.py:159-234` (argparse), `:240` (logging call), `:292-305` (manager construction); `tests/root_scripts/test_run_accuracy_simulation.py:86-92,581-615` (tests to update) |
| **Cat 2: Read source code (actual method signatures)** | Read full `run_accuracy_simulation.py` (330 lines); Read `AccuracySimulationManager.__init__` (lines 71-81); Read `run_both()` (lines 725-902) |
| **Cat 3: Verified data structures from source** | Verified `parameter_order` is a `List[str]` accepted by constructor; Verified `num_parameters_to_test` does NOT limit `run_both()` loop |
| **Cat 4: Reviewed DISCOVERY.md for context** | Read full DISCOVERY.md — Finding 8 confirms accuracy sim has --log-level, missing --debug/--e2e-test |
