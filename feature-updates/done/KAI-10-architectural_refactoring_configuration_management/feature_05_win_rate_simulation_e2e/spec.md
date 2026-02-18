## Feature Spec: win_rate_simulation_e2e

**Status:** APPROVED (S2.P1 complete — Gate 3 passed 2026-02-18)
**Last Updated:** 2026-02-18

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Add --e2e-test and --log-level to existing argparse. References Feature 01 spec for design patterns.

**Key scope items:**
- Add to run_win_rate_simulation.py: --e2e-test, --log-level (currently has 9 unique args, missing both)
- Implement --e2e-test mode: single run, sims=1, ≤180 seconds; also used for debugging development
- Remove LOGGING_LEVEL module constant (replace with --log-level arg)

**Design Correction (from HANDOFF_PACKAGE.md update):**
- There is NO separate `--debug` flag in this epic
- Universal args are `--e2e-test` + `--log-level` only (2 universal args, not 3)
- `--e2e-test` serves both purposes: fast E2E testing AND debugging (use `--e2e-test --log-level DEBUG` for debug-style runs)
- Feature 01 spec confirmed this pattern (REQ-01: only 2 universal args)

**Research Finding:** Discovery said "17 args" but actual file has 9 unique args. Discrepancy is due to Discovery agent counting args across all subparsers (single/full/iterative each repeat the same args). Scope is unchanged: add 2 universal args.

### Relevant Discovery Decisions

- **Solution Approach:** Enhance existing comprehensive argparse; argparse defaults are single source of truth
- **Key Constraints:** win_rate_simulation already has 9 unique args — only adding 2; preserve all existing arg behavior
- **Dependencies:** None (Wave 2 — references Feature 01 spec for design patterns after it completes S2)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

---

## Requirements

### REQ-01: CLI Arguments — run_win_rate_simulation.py

**Source:** Epic Request (universal args spec) + Feature 01 design precedent + S2 research (current args verified)

Add the following CLI arguments to `run_win_rate_simulation.py` via argparse (main parser only):

**Universal arguments (2 new args):**
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--e2e-test` | flag | False | E2E test mode: single run, sims=1, completes in ≤180 seconds; also used for debugging |
| `--log-level` | str | 'INFO' | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

**Existing arguments (preserved as-is):**
| Argument | Type | Default | Notes |
|----------|------|---------|-------|
| mode (positional) | str | 'iterative' | Subcommand: single/full/iterative |
| `--enable-log-file` | flag | False | Pre-existing — preserved |
| `--sims` | int | 5 | Pre-existing — preserved |
| `--baseline` | str | '' | Pre-existing — preserved |
| `--output` | str | 'simulation/simulation_configs' | Pre-existing — preserved |
| `--workers` | int | 8 | Pre-existing — preserved |
| `--data` | str | 'simulation/sim_data' | Pre-existing — preserved |
| `--test-values` | int | 5 | Pre-existing — preserved |
| `--use-processes` | flag | False | Pre-existing — preserved |

**Total: 11 unique CLI arguments** (9 existing + 2 new universal args)

---

### REQ-02: Remove LOGGING_LEVEL Module Constant

**Source:** Epic Request ("zero CLI constants in runner scripts") + S2 research (line 33 verified)

Remove `LOGGING_LEVEL = 'INFO'` from module level of `run_win_rate_simulation.py` (currently line 33).

**Non-CLI constants to KEEP (unchanged):**
- `LOG_NAME = "win_rate_simulation"` — non-CLI internal constant (required by existing tests)
- `LOGGING_FORMAT = 'standard'` — non-CLI internal constant
- `DEFAULT_MODE`, `DEFAULT_SIMS`, `DEFAULT_BASELINE`, `DEFAULT_OUTPUT`, `DEFAULT_WORKERS`, `DEFAULT_DATA`, `DEFAULT_TEST_VALUES`, `NUM_PARAMETERS_TO_TEST`, `PARAMETER_ORDER` — these are argparse defaults, NOT CLI-configurable constants; they stay

**Update `setup_logger()` call** (currently line 223):
```python
# BEFORE
setup_logger(LOG_NAME, LOGGING_LEVEL, args.enable_log_file, None, LOGGING_FORMAT)

# AFTER
setup_logger(LOG_NAME, args.log_level, args.enable_log_file, None, LOGGING_FORMAT)
```

---

### REQ-03: E2E Test Mode (--e2e-test)

**Source:** Epic Request (Section 3: E2E Test Modes) + Feature 01 design precedent (REQ-11)

When `--e2e-test` flag is set:
- Force mode to `'single'` (one config test — not full sweep, not iterative loop)
- Force `sims=1` (single simulation — minimal computation)
- Force `workers=1` (single-threaded — predictable timing)
- Script must complete in ≤180 seconds
- Exit code 0 on success

**Implementation (in runner, before SimulationManager creation):**
```python
# Apply E2E test overrides — force minimal single-config run
if args.e2e_test:
    args.mode = 'single'
    args.sims = 1
    args.workers = 1
```

**Graceful skip behavior (RESOLVED Q2 — Option A):**
- If baseline config folder not found → exit 0 with info message (graceful skip, consistent with Feature 01 E2E pattern)
- If sim_data folder not found → exit 0 with info message (graceful skip)

**Season selection (RESOLVED Q1 — Option A):**
- Keep hardcoded `season='2025'` — matches current single mode behavior exactly
- `run_single_config_test(season='2025')` unchanged

**Precedence rule:** `--e2e-test` overrides individual --sims, --workers, mode for data limits.

---

### REQ-04: --log-level behavior

**Source:** Epic Request (universal argument spec) + Feature 01 design precedent (REQ-13)

- `--log-level` accepts: DEBUG, INFO, WARNING, ERROR, CRITICAL (uppercase — consistent with Feature 01 universal standard)
- Default: 'INFO'
- Replaces hardcoded `LOGGING_LEVEL = 'INFO'` module constant (REQ-02)
- For debugging: use `--e2e-test --log-level DEBUG` (no separate --debug flag)

**Note:** `run_accuracy_simulation.py` uses lowercase choices — Feature 06 will normalize that. Feature 05 uses uppercase choices from the start (consistent with Feature 01).

---

### REQ-05: Backward Compatibility

**Source:** Derived requirement (zero regression from EPIC_TICKET.md)

- Running `python run_win_rate_simulation.py` (no args) must behave identically to current
- Running `python run_win_rate_simulation.py single --sims 5` must preserve existing behavior
- Running `python run_win_rate_simulation.py --enable-log-file` must preserve existing behavior
- All 2,744+ existing unit tests must pass

---

### REQ-06: Update test_run_win_rate_simulation.py — Add new CLI arg tests

**Source:** S2 research (28 existing tests verified — all must pass)

`tests/root_scripts/test_run_win_rate_simulation.py` currently has 28 tests across 4 categories covering `--enable-log-file` and DEBUG log quality. After adding 2 new CLI args, new tests should cover:

- `--log-level` flag: exists in help, accepts valid choices (DEBUG/INFO/.../CRITICAL), defaults to INFO
- `--e2e-test` flag: exists in help, defaults False, sets True, forces mode='single'/sims=1/workers=1

**All 28 existing tests must continue to pass** (no deletions).

---

## Open Scope Questions

All checklist questions resolved. No open scope questions remain.

**Decisions made (see `checklist.md`):**
1. **Q1 → A**: Season for E2E mode: keep hardcoded `'2025'` (matches existing single mode)
2. **Q2 → A**: Graceful skip (exit 0 + info) when baseline config or sim_data missing

---

## Acceptance Criteria

- [ ] `python run_win_rate_simulation.py --help` displays `--e2e-test` and `--log-level` arguments
- [ ] `python run_win_rate_simulation.py --log-level DEBUG` sets logging to DEBUG level
- [ ] `python run_win_rate_simulation.py --log-level WARNING` sets logging to WARNING level
- [ ] `python run_win_rate_simulation.py --log-level INVALID` exits with argparse error (invalid choice)
- [ ] `python run_win_rate_simulation.py --e2e-test` completes in ≤180 seconds with exit code 0 (when sim data present)
- [ ] `python run_win_rate_simulation.py --e2e-test` exits 0 with info message when no baseline config found (graceful skip)
- [ ] `python run_win_rate_simulation.py --e2e-test` exits 0 with info message when sim_data folder missing (graceful skip)
- [ ] `python run_win_rate_simulation.py` (no args) behavior identical to current (default: iterative mode, INFO logging)
- [ ] `python run_win_rate_simulation.py --enable-log-file` preserves existing behavior
- [ ] `python run_win_rate_simulation.py single --sims 5` preserves existing behavior
- [ ] `grep "LOGGING_LEVEL" run_win_rate_simulation.py` returns empty (constant removed)
- [ ] `grep "LOG_NAME" run_win_rate_simulation.py` returns `LOG_NAME = "win_rate_simulation"` (non-CLI constant kept)
- [ ] `pytest tests/` reports all 2,744+ passed, 0 failed

---

## Files to Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_win_rate_simulation.py` | Add 2 universal args, remove LOGGING_LEVEL, apply E2E override logic | Low |
| `tests/root_scripts/test_run_win_rate_simulation.py` | Add tests for new args (preserve all 28 existing) | Low |

**Total: 2 files to modify** (no internal simulation module changes needed — no config.py exists)
