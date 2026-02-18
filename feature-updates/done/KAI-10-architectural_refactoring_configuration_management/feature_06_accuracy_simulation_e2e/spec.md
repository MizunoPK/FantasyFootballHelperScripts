## Feature Spec: accuracy_simulation_e2e

**Status:** USER APPROVED (S2.P1 complete — Gate 3 passed 2026-02-18)
**Last Updated:** 2026-02-18

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Add --e2e-test and normalize --log-level to existing argparse. References Feature 01 spec for design patterns.

**Key scope items:**
- Add to `run_accuracy_simulation.py`: `--e2e-test` (1 new flag)
- Normalize `--log-level` choices to uppercase (DEBUG, INFO, WARNING, ERROR, CRITICAL) — matches universal standard from Feature 01
- `--e2e-test` serves both purposes: fast E2E test mode AND development debugging (use `--e2e-test --log-level DEBUG` for debug sessions)
- Implement --e2e-test mode: single parameter, minimal config, ≤180 seconds
- NO separate --debug flag — eliminated from epic design (see handoff correction 2026-02-18)
- NO internal module refactoring needed (AccuracySimulationManager already uses constructor parameter pattern)
- NO config imports to remove (run_accuracy_simulation.py has no config module imports)

### Relevant Discovery Decisions

- **Solution Approach:** Enhance existing argparse only; AccuracySimulationManager already uses constructor pattern
- **Key Constraints:** ≤180s E2E target requires passing a subset PARAMETER_ORDER to AccuracySimulationManager
- **Dependencies:** Feature 01 spec provides design precedents (universal args are --e2e-test + --log-level only)

### Design Precedent (from Feature 01 spec — authoritative)

| Pattern | Feature 01 Decision | Feature 06 Application |
|---------|-------------------|----------------------|
| Universal args | `--e2e-test` + `--log-level` (NO --debug) | Same: add --e2e-test, normalize --log-level |
| `--e2e-test` purpose | Fast mode AND debugging (use `--log-level DEBUG` for verbose output) | Same |
| `--log-level` choices | Uppercase: `['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']`, default `'INFO'` | Normalize from current lowercase |
| `--e2e-test` data scope | Limits data/API calls, ≤180s | Limits parameters evaluated (1 param, 1 test value) |

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Requirements

### REQ-01: Add --e2e-test flag to run_accuracy_simulation.py

**Source:** Epic Request (Section 3: E2E Test Modes) + EPIC_TICKET.md AC-03 + Feature 01 universal arg standard

Add `--e2e-test` to argparse in `run_accuracy_simulation.py`:

```python
parser.add_argument(
    '--e2e-test',
    action='store_true',
    default=False,
    help='E2E test mode: limit to 1 parameter + 1 test value, completes in ≤180 seconds. '
         'Also useful for development debugging with --log-level DEBUG.'
)
```

**Behavior when --e2e-test is set:**
- Pass reduced PARAMETER_ORDER = `['NORMALIZATION_MAX_SCALE']` (1 parameter only) to AccuracySimulationManager
- Pass `num_test_values=1` (1 test value only)
- Script must complete in ≤180 seconds
- Exit code 0 on success

**Implementation in main() (after baseline validation, before manager construction):**

```python
# Apply --e2e-test limits
parameter_order = PARAMETER_ORDER
test_values = args.test_values
if args.e2e_test:
    parameter_order = ['NORMALIZATION_MAX_SCALE']  # Single parameter
    test_values = 1  # Minimal test values

manager = AccuracySimulationManager(
    baseline_config_path=baseline_path,
    output_dir=output_path,
    data_folder=data_path,
    parameter_order=parameter_order,
    num_test_values=test_values,
    num_parameters_to_test=args.num_params,
    max_workers=args.max_workers,
    use_processes=args.use_processes
)
```

**Precedence rule:**
- `--e2e-test` takes precedence for scope limits over individual `--test-values` value

**Graceful skip behavior when data missing (ALIGNED with Feature 05 REQ-03):**
- If `sim_data/` folder not found → log info message, exit 0 (graceful skip, not hard failure)
- If no baseline config found (and --baseline not provided) → log info message, exit 0 (graceful skip)
- Graceful skip ONLY applies in `--e2e-test` mode; normal mode retains existing hard-failure behavior (logger.error + sys.exit(1))
- This makes E2E mode portable in CI environments without historical data

**Implementation (E2E graceful checks, before standard validation):**
```python
if args.e2e_test:
    if not data_path.exists():
        logger.info(f"[E2E] sim_data folder not found: {data_path}. Skipping (exit 0).")
        sys.exit(0)
    if not args.baseline:
        try:
            baseline_path = find_baseline_config()
        except FileNotFoundError:
            logger.info("[E2E] No baseline config found. Skipping (exit 0).")
            sys.exit(0)
```

---

### REQ-02: Normalize --log-level to uppercase choices

**Source:** Feature 01 spec (authoritative universal arg standard) + Epic Request (universal arg specification)

**Current state (lines 216-225 in run_accuracy_simulation.py):**
```python
parser.add_argument(
    '--log-level',
    choices=['debug', 'info', 'warning', 'error'],   # lowercase, missing 'critical'
    default=DEFAULT_LOG_LEVEL,                         # 'info' (lowercase string)
    ...
)
# Used as: setup_logger(LOG_NAME, args.log_level.upper(), ...)  # .upper() call at line 240
```

**Required state (matching Feature 01 universal standard):**
```python
parser.add_argument(
    '--log-level',
    type=str.upper,                                          # Accept lowercase input, normalize to upper
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],  # Uppercase + add CRITICAL
    default='INFO',                                          # Uppercase default
    help='Logging level (default: INFO). Use with --e2e-test --log-level DEBUG for verbose debug output.'
)
```

**Changes required:**
- Add `type=str.upper` — converts input to uppercase before choice validation (backward compat: `--log-level debug` still works)
- Change `choices` to uppercase + add `'CRITICAL'`
- Change `default` from `'info'` to `'INFO'`
- Update `DEFAULT_LOG_LEVEL = 'info'` constant at line 53 to `DEFAULT_LOG_LEVEL = 'INFO'`
- Remove `.upper()` call from `setup_logger()` invocation at line 240 (no longer needed with `type=str.upper`)

**Backward compatibility:** `type=str.upper` means `--log-level debug` (lowercase) still works — gets converted to `'DEBUG'` before choice validation. Zero breaking changes.

**Impact on existing tests:**
- `test_existing_log_level_flag_unchanged` (line 86-92): passes `'debug'` → will be accepted (type=str.upper normalizes it) → test still passes with minimal update to expected value check
- `create_test_parser()` helper (lines 581-615): update choices to uppercase + add str.upper type

---

### REQ-03: Backward Compatibility

**Source:** Derived requirement (zero regression from EPIC_TICKET.md)

- Running `python run_accuracy_simulation.py` (no args) must behave identically to current behavior
- All 10 existing CLI arguments preserved and working
- `--log-level debug` (lowercase) must continue to work (handled by `type=str.upper`)
- All 2,744+ existing unit tests must pass after changes

---

### REQ-04: Update tests/root_scripts/test_run_accuracy_simulation.py

**Source:** S2 research (tests exist for this file)

**Tests to ADD for --e2e-test:**
- `test_e2e_test_flag_exists_in_argparse` — verify `--e2e-test` arg in parser
- `test_e2e_test_flag_default_false` — verify default is False
- `test_e2e_test_flag_store_true` — verify action='store_true'
- `test_e2e_test_limits_parameter_order` — verify parameter_order is subset when --e2e-test set (mock AccuracySimulationManager, check parameter_order arg)
- `test_e2e_test_limits_test_values` — verify num_test_values=1 when --e2e-test set
- `test_e2e_test_graceful_skip_no_data_folder` — verify exit 0 + info message when sim_data/ missing in E2E mode
- `test_e2e_test_graceful_skip_no_baseline` — verify exit 0 + info message when no baseline config in E2E mode

**Tests to UPDATE for --log-level normalization:**
- `test_existing_log_level_flag_unchanged` (line 86-92): currently asserts `args.log_level == 'debug'` → will now get `'DEBUG'` (after str.upper) — update assertion to `'DEBUG'`
- `create_test_parser()` helper (line 581-615): update choices to uppercase + add `type=str.upper`

**Tests to ADD for --log-level normalization:**
- `test_log_level_accepts_uppercase` — verify `--log-level DEBUG` accepted
- `test_log_level_accepts_lowercase` — verify `--log-level debug` accepted (backward compat via str.upper)
- `test_log_level_includes_critical` — verify `--log-level CRITICAL` now accepted
- `test_log_level_default_is_uppercase_INFO` — verify default is `'INFO'` not `'info'`

---

## Acceptance Criteria

- [ ] `python run_accuracy_simulation.py --help` displays `--e2e-test` flag
- [ ] `python run_accuracy_simulation.py --e2e-test` (with sim_data/ + baseline present) completes in ≤180 seconds with exit code 0
- [ ] `python run_accuracy_simulation.py --e2e-test` (without sim_data/) exits 0 with info message (graceful skip)
- [ ] `python run_accuracy_simulation.py --e2e-test` (without baseline config) exits 0 with info message (graceful skip)
- [ ] `python run_accuracy_simulation.py --e2e-test --log-level DEBUG` completes in ≤180 seconds with DEBUG-level logging
- [ ] `python run_accuracy_simulation.py --log-level debug` accepted (lowercase) and treated as DEBUG
- [ ] `python run_accuracy_simulation.py --log-level CRITICAL` accepted (new choice added)
- [ ] `python run_accuracy_simulation.py` (no args) behavior identical to current (default INFO logging, full parameter set)
- [ ] `python run_accuracy_simulation.py --log-level warning` (previously worked) still works
- [ ] `pytest tests/root_scripts/test_run_accuracy_simulation.py` all pass
- [ ] `pytest tests/` reports all 2,744+ passed, 0 failed

---

## Files to Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_accuracy_simulation.py` | Add --e2e-test flag + normalize --log-level | Low |
| `tests/root_scripts/test_run_accuracy_simulation.py` | Add ~5 --e2e-test tests + update ~2 --log-level tests | Low |

**Total: 2 files to modify**

---

## Open Scope Questions

See `checklist.md`. Only 1 question remains (Q3 — max_workers for --e2e-test).
