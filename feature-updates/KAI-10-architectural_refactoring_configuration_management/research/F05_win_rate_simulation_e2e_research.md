# Research Notes: Feature 05 — win_rate_simulation_e2e

**Researcher:** Secondary-D
**Date:** 2026-02-18
**Stage:** S2.P1.I1

---

## ⚠️ Design Correction Applied

**Source:** HANDOFF_PACKAGE.md update (2026-02-18)

The initial research and draft spec included a `--debug` flag. This was **incorrect**. The corrected design is:
- Universal args: `--e2e-test` + `--log-level` ONLY (2 args, not 3)
- No separate `--debug` flag in this epic
- For debug-style runs: use `--e2e-test --log-level DEBUG`
- Feature 01 spec confirmed and updated to reflect this

All references to `--debug` in this research document are **historical only** and do NOT reflect the final spec.

---

## Files Researched

| File | Status | Key Findings |
|------|--------|--------------|
| `run_win_rate_simulation.py` | Read in full | CLI args, LOGGING_LEVEL constant, setup_logger call |
| `simulation/win_rate/SimulationManager.py` | Read (lines 1-250, 1088-1150) | Constructor signature, run_single_config_test() |
| `tests/root_scripts/test_run_win_rate_simulation.py` | Read in full | 28 existing tests, categories |
| `tests/integration/test_simulation_integration.py` | Read in full | Integration test structure |
| `run_accuracy_simulation.py` | Read in full | --log-level reference implementation |
| `feature_01_refactor_player_data_fetcher/spec.md` | Read in full | Design precedents |
| `feature_02_schedule_fetcher_cli/spec.md` | Read in full | Wave 2 E2E approach reference (draft) |
| `DISCOVERY.md` | Read in full | Epic scope, Feature 05 definition |

---

## Finding 1: Current CLI Args in run_win_rate_simulation.py

**Expected (from Discovery):** 17 args
**Actual (from code):** 9 unique args

The Discovery agent said "17" but the actual file has 9 unique CLI args:

| Arg | Type | Default | Notes |
|-----|------|---------|-------|
| mode (positional) | str | 'iterative' | subcommand: single/full/iterative |
| --enable-log-file | flag | False | Preserved from previous feature |
| --sims | int | 5 | Appears in main parser AND each subparser |
| --baseline | str | '' | Appears in main parser AND each subparser |
| --output | str | 'simulation/simulation_configs' | Appears in main parser AND each subparser |
| --workers | int | 8 | Appears in main parser AND each subparser |
| --data | str | 'simulation/sim_data' | Appears in main parser AND each subparser |
| --test-values | int | 5 | Appears in main parser AND each subparser |
| --use-processes | flag | False | Appears in main parser AND each subparser |

**Explanation of discrepancy:** The Discovery agent may have counted all arg definitions across the main parser AND all three subparsers (single/full/iterative), counting --sims, --baseline, --output, --workers, --data, --test-values, --use-processes 4 times each. The actual unique CLI args a user can pass is 9.

**Impact on scope:** None. We're still adding 3 universal args (--debug, --e2e-test, --log-level). Total after feature: 12 unique args.

---

## Finding 2: LOGGING_LEVEL Constant

The runner has these module-level constants at lines 33-38:

```python
LOGGING_LEVEL = 'INFO'          # Line 33 — CLI-configurable → becomes --log-level
LOG_NAME = "win_rate_simulation" # Line 34 — non-CLI, keep
LOGGING_FORMAT = 'standard'     # Line 35 — non-CLI, keep
```

`setup_logger()` is called at line 223:
```python
setup_logger(LOG_NAME, LOGGING_LEVEL, args.enable_log_file, None, LOGGING_FORMAT)
```

After Feature 05: `LOGGING_LEVEL` constant is removed, replaced by `args.log_level`.

**Existing test** checks: `assert not hasattr(run_win_rate_simulation, 'LOGGING_TO_FILE')` — won't conflict.
**Existing test** checks: `assert run_win_rate_simulation.LOG_NAME == "win_rate_simulation"` — must preserve `LOG_NAME`.

---

## Finding 3: No Config File in simulation/win_rate/

`simulation/win_rate/` contains only Python modules — no config.py or constants.py:
- SimulationManager.py, ParallelLeagueRunner.py, SimulatedLeague.py, DraftHelperTeam.py
- SimulatedOpponent.py, Week.py, manual_simulation.py, config_cleanup.py, ConfigGenerator.py (actually in shared/)
- ConfigPerformance.py, ProgressTracker.py, ResultsManager.py (in shared/)

**Impact:** Feature 05 scope is ONLY the runner script (`run_win_rate_simulation.py`). No internal module config stripping needed.

---

## Finding 4: SimulationManager Constructor Signature

```python
SimulationManager(
    baseline_config_path: Path,
    output_dir: Path,
    num_simulations_per_config: int,
    max_workers: int,
    data_folder: Path,
    parameter_order: List[str],
    num_test_values: int = 5,
    num_parameters_to_test: int = 1,
    auto_update_league_config: bool = True,
    use_processes: bool = False
) -> None
```

**For E2E mode:** Can pass `num_simulations_per_config=1` and `max_workers=1` to limit computation.

---

## Finding 5: run_single_config_test() Is Deprecated

```python
def run_single_config_test(self, config_id: str = "test", season: str = "2025") -> None:
    warnings.warn(
        "run_single_config_test() uses single-season data only. "
        "Use run_iterative_optimization() for multi-season validation.",
        DeprecationWarning, stacklevel=2
    )
```

The `single` mode in the runner currently calls `manager.run_single_config_test(season='2025')`. This is deprecated but functional. E2E mode should use this same single-mode path with `sims=1`.

**Season hardcoded as '2025'** — may fail if only 2026 data exists. Open question for user.

---

## Finding 6: E2E Mode Timing Analysis

Current simulation modes:
- **single**: Runs N sims with just the baseline config (no parameter sweep). With sims=1 → 1 simulation run.
- **full**: Grid search all parameter combinations → VERY slow (never use for E2E)
- **iterative**: Coordinate descent, infinite loop → NEVER use for E2E

**E2E strategy:** Force mode='single', sims=1, workers=1. This runs exactly 1 fantasy league simulation with the baseline config, which should complete well under 180 seconds.

**Risk:** If no baseline config exists, `sys.exit(1)` is called. Need to decide: graceful skip (exit 0) or preserve exit 1?

---

## Finding 7: Existing Test Suite

`tests/root_scripts/test_run_win_rate_simulation.py` — 28 tests in 4 categories:

1. **Category 1: CLI Flag Unit Tests (6 tests)** — tests `--enable-log-file` exists, defaults False, sets True
2. **Category 2: CLI Flag Integration Tests (8 tests)** — tests flag with each mode, logger name
3. **Category 3: DEBUG Log Quality Unit Tests (12 tests)** — inspects SimulationManager source for debug quality
4. **Category 4: DEBUG Log Quality Integration Tests (2 tests)** — skipped integration tests

**Note:** These tests were labeled "Feature 05: win_rate_sim_logging" from a PREVIOUS epic (likely KAI-9). They test the `--enable-log-file` flag which was already added. They test DEBUG log quality in simulation modules (already audited).

**Impact:** All 28 tests must continue to pass. New tests for --debug, --e2e-test, --log-level will be added.

---

## Finding 8: --log-level Pattern from run_accuracy_simulation.py

```python
parser.add_argument(
    '--log-level',
    choices=['debug', 'info', 'warning', 'error'],  # lowercase in accuracy
    default=DEFAULT_LOG_LEVEL,  # 'info' (lowercase)
    ...
)
setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)
```

**Feature 01 universal standard:** uppercase choices (DEBUG, INFO, WARNING, ERROR, CRITICAL)
**Accuracy_simulation current:** lowercase choices, `.upper()` conversion at setup_logger call

**Decision for Feature 05:** Use uppercase choices (DEBUG/INFO/WARNING/ERROR/CRITICAL) matching the Feature 01 universal standard. Feature 06 will normalize accuracy_simulation to uppercase as well.

---

## Integration Points

| Integration Point | Current Code | After Feature 05 |
|------------------|--------------|-----------------|
| setup_logger call (line 223) | `setup_logger(LOG_NAME, LOGGING_LEVEL, ...)` | `setup_logger(LOG_NAME, log_level, ...)` where `log_level = 'DEBUG' if args.debug else args.log_level` |
| LOGGING_LEVEL constant (line 33) | `LOGGING_LEVEL = 'INFO'` | Removed |
| SimulationManager init (modes) | 3 modes: single/full/iterative | E2E mode forces single + sims=1 + workers=1 |

---

## Open Questions

**Q1:** What data reduction does `--debug` apply?
- Context: Feature 01 reduces espn_player_limit. Simulation doesn't have a player limit.
- Option A: Force sims=1, mode='single' (fastest possible run)
- Option B: Just enable DEBUG logging, no data reduction
- Option C: Force sims=2 (small reduction)

**Q2:** What does `--e2e-test` specifically execute?
- Option A: Force mode='single' + sims=1 + workers=1 (simplest, guaranteed fast)
- Option B: Force mode='single' + sims=1 (let --workers remain user-controlled)

**Q3:** When `--e2e-test` is set but baseline config or sim_data doesn't exist:
- Option A: Exit 0 with info message (graceful skip — consistent with Feature 01 E2E pattern for missing files)
- Option B: Exit 1 with error (data required)

**Q4:** Season for E2E/single mode: current code hardcodes `season='2025'`:
- Option A: Use hardcoded '2025' (matches current single mode behavior)
- Option B: Auto-detect most recent available season from sim_data folder
- Context: In 2026, if only 2026 data exists, '2025' would fail

---

## Files to Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_win_rate_simulation.py` | Add 3 args, remove LOGGING_LEVEL, apply precedence rules | Low-Medium |
| `tests/root_scripts/test_run_win_rate_simulation.py` | Add new tests (preserve all 28 existing) | Low |

**Total: 2 files to modify** (no internal simulation module changes needed)
