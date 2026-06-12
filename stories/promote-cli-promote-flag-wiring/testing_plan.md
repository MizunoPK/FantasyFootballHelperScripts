# Testing Plan: promote-cli

**Note:** Produced during Phase 3b because `.shamt-core/shamt-config.json` sets `testing: "enabled"` and this Quick-path story introduces a new test file (escalates from the inline checklist). Executed during Phase 5 (Test) by the `test-executor` persona (Haiku tier).

**Created:** 2026-06-11
**Story:** stories/promote-cli-promote-flag-wiring/
**Spec:** stories/promote-cli-promote-flag-wiring/spec.md
**Implementation Plan:** N/A (Quick path — built from spec Build Checklist)
**Path:** Quick path (risk-triggered validation — the wired `--promote` triggers a live-config write via the committed writer)
**Baseline:** v1
**Baseline status:** Active

---

## Test Strategy

The story adds CLI dispatch + a thin `_run_promote_mode` around the committed writer. Coverage is **unit-only**, using the established `run_win_rate_simulation` patch harness (`patch` on the `run_win_rate_simulation` module namespace; `patch("sys.argv", …)` with the real parser for `main()` dispatch; `Namespace` for direct helper calls). The destructive write itself is owned and tested by `config-promoter`; here we verify dispatch correctness, error-exit behavior, the report, and that strategy-only/sweep paths are untouched.

- **End-to-end:** N/A — exercising the real promote against the live `league_config.json` is out of scope (the writer is unit-tested in `config-promoter`); CLI tests patch `promote_best_combination`.
- **Integration:** the `main()` dispatch branches (promote-only, sweep-then-promote, endless-reject) are the integration surface, tested with dispatch helpers patched.
- **Unit:** `run_win_rate_simulation._run_promote_mode`, `_print_promotion`, the `--promote` parser flag, and the `main()` dispatch guard.
- **Test runner:** `pytest` — `python -m pytest tests/root_scripts/test_run_win_rate_simulation_promote.py -vv`; regression across the three CLI test files; full gate `python tests/run_all_tests.py`.
- **Test file conventions:** new file `tests/root_scripts/test_run_win_rate_simulation_promote.py`; `MODULE = "run_win_rate_simulation"`; `unittest.mock.patch` on the module namespace; `capsys` for report assertions; `pytest.raises(SystemExit)` (+ `.value.code`) for exit paths; mirror `test_run_win_rate_simulation_sweep.py`'s `_sweep_args` Namespace style.
- **Project assumptions checked:** `promote_best_combination`, `ConfigurationError`, `FileOperationError` importable on the module; `_run_sweep_mode` returns cleanly on the non-endless path (so sweep-then-promote reaches promote); the existing `_sweep_args` helper now carries `promote=False`.

**`-k` token discipline:** tokens (`invokes_writer`, `config_error`, `file_error`, `promote_only`, `sweep_then`, `endless_promote`, `default_false`, `present_true`) are each a **contiguous substring of their target method name** and a non-substring of the path components `run_win_rate_simulation` / `test_run_win_rate_simulation_promote` (note: a bare `promote` token is deliberately avoided — it is a substring of the filename and would select the whole file; `endless_promote` — not `endless_rejected` — is used because the method is `test_dispatch_endless_promote_rejected`, so `endless_rejected` is **not** contiguous). Each step asserts ≥1 selected (pytest exits 5 on no-match).

---

## Test Plan Steps

### Step 1: `_run_promote_mode` — invokes the writer, reports, and error-exits
**Type:** unit
**File:** `tests/root_scripts/test_run_win_rate_simulation_promote.py`
**Invocation:** `python -m pytest tests/root_scripts/test_run_win_rate_simulation_promote.py -k "invokes_writer or config_error or file_error" -vv`
**Pass criterion:** All selected pass (≥1). Patch approach: `patch(f"{MODULE}.SweepResultsManager")` (constructor returns a mock store) and `patch(f"{MODULE}.promote_best_combination")` (returns a sample result dict with all four keys + the 7 param values). Covers: (a) `_run_promote_mode(data_folder, logger)` calls `promote_best_combination` once with the constructed store object + `data_folder`, and the printed report (`capsys`) contains the **full** D3 content — the target config path, the strategy id, the cumulative win rate and games, and **each of the 7 param names** from `result["param_values"]`; (b) when the patched writer raises `ConfigurationError`, `_run_promote_mode` logs (`mock_logger.error` called) and raises `SystemExit` with code 1 and prints **no** report (`capsys` out is empty); (c) same for `FileOperationError` → `SystemExit` code 1, no report.
**Expected test methods:** `test_promote_mode_invokes_writer_and_reports`, `test_promote_mode_config_error_exits`, `test_promote_mode_file_error_exits`.
**Covers:** spec Requirements — functional bullets 2, 5; D2, D3, D4.

---

### Step 2: `main()` dispatch — promote-only, sweep-then-promote, endless-reject
**Type:** unit
**File:** `tests/root_scripts/test_run_win_rate_simulation_promote.py`
**Invocation:** `python -m pytest tests/root_scripts/test_run_win_rate_simulation_promote.py -k "promote_only or sweep_then or endless_promote" -vv`
**Pass criterion:** All selected pass (≥1). Covers, with `_run_sweep_mode`, `_run_promote_mode`, `DraftStrategyOrchestrator`, `WinRateMetaDataManager` patched and `sys.argv` (or a `Namespace`) set: (a) `--promote` alone → `_run_promote_mode` called once, `_run_sweep_mode` and `DraftStrategyOrchestrator` **not** called; (b) `--sweep --promote` → `_run_sweep_mode` then `_run_promote_mode` both called once, **in that order** — verified by attaching both mocks to a shared parent (`parent = Mock(); parent.attach_mock(mock_sweep, "sweep"); parent.attach_mock(mock_promote, "promote")`) and asserting `parent.mock_calls` lists the sweep call before the promote call (or equivalently a `side_effect` that appends each helper name to a shared list, asserted `== ["sweep", "promote"]`); (c) `--endless --promote` → `SystemExit` code 2 and **neither** `_run_sweep_mode` nor `_run_promote_mode` called.
**Expected test methods:** `test_dispatch_promote_only`, `test_dispatch_sweep_then_promote`, `test_dispatch_endless_promote_rejected`.
**Covers:** spec Requirements — functional bullets 2, 3, 4, 6; D1.

---

### Step 3: `--promote` flag parsing
**Type:** unit
**File:** `tests/root_scripts/test_run_win_rate_simulation_promote.py`
**Invocation:** `python -m pytest tests/root_scripts/test_run_win_rate_simulation_promote.py -k "default_false or present_true" -vv`
**Pass criterion:** All selected pass (≥1). Covers: `_build_parser().parse_args([])` yields `promote is False`; `parse_args(["--promote"])` yields `promote is True`.
**Expected test methods:** `test_promote_flag_default_false`, `test_promote_flag_present_true`.
**Covers:** spec Requirements — functional bullet 1.

---

### Step 4: Full new file + CLI regression + gate
**Type:** unit
**File:** `tests/root_scripts/test_run_win_rate_simulation_promote.py` (+ existing CLI files)
**Invocation:** `python -m pytest tests/root_scripts/test_run_win_rate_simulation_promote.py tests/root_scripts/test_run_win_rate_simulation_sweep.py tests/root_scripts/test_run_win_rate_simulation.py -vv` then `python tests/run_all_tests.py`
**Pass criterion:** The new file passes in full (no method outside Steps 1–3 left unrun); the existing CLI test files pass (proving the `_sweep_args` `promote=False` update keeps `main()` dispatch working and strategy-only/sweep behavior unchanged); the full project suite reports 100% (this 100%-pass requirement is the CODING_STANDARDS *commit gate*, not a style check). Pre-existing working-tree deletions of `data/historical_data/2025/*` are unrelated and must not cause failures.
**Covers:** spec Requirements — functional bullet 6 (strategy-only unchanged); spec Verification bullets 1–2; the CODING_STANDARDS 100%-pass commit gate. (The spec's non-functional "Matches CODING_STANDARDS" *style* compliance — thin runner helpers, `get_logger`, error hierarchy — is a static property verified in Phase 6 Code Review, not by the test runner.)

---

## Shared Setup / Teardown

N/A — each step is self-contained. Tests patch the `run_win_rate_simulation` module namespace and build `Namespace` / `sys.argv` inline; no services, DB, network, files, or env vars; the live `league_config.json` is never touched (`promote_best_combination` is patched).

---

## Results Log

| Step | Status | Run at | Evidence | Notes |
|------|--------|--------|----------|-------|
| 1 | PASS | 2026-06-11 | `3 passed, 5 deselected` | invokes_writer / config_error / file_error |
| 2 | PASS | 2026-06-11 | `3 passed, 5 deselected` | promote_only / sweep_then / endless_promote |
| 3 | PASS | 2026-06-11 | `2 passed, 6 deselected` | default_false / present_true |
| 4 | PASS | 2026-06-11 | new file `8 passed`; CLI files `38 passed`; full suite `2849/2849 (100%)` | `_sweep_args` promote=False update verified; pre-existing deletions caused no failures |

**Status values:** `PENDING`, `PASS`, `FAIL`, `BLOCKED`. Phase 5 blocks until every step is `PASS`.

---

## Failure Diagnosis

[Populated only on failure.]

---

## Open Questions

*(None — test design follows the spec Test Strategy directly; every case maps to a spec Requirement / Design Decision.)*

---

## Validation

Validated via Pattern 1. Dimensions:

- **Step clarity** — each step has an exact `pytest -k` invocation, named expected methods, and a binary pass criterion.
- **Executability** — commands resolve in the project's pytest environment; the only state is patched module seams + inline `Namespace`/`sys.argv` (Shared Setup = N/A).
- **Verification completeness** — every spec Requirement maps to a step: functional 1 → Step 3; functional 2 → Steps 1–2; functional 3, 4 → Step 2; functional 5 → Step 1; functional 6 → Steps 2 & 4; spec Verification → Step 4. Design Decisions D1–D4 are exercised by Steps 1–2; **D5 (branch from local `main`) is a one-time build action, not unit-testable — excluded from automated coverage and verified by the Build/Review** (the branch-prep step). The spec's non-functional CODING_STANDARDS *style* compliance is verified in Phase 6 Code Review, not here.

Exit: risk-triggered (part of the live-config promotion feature) → primary clean round + 1 adversarial sub-agent confirmation.

---
Validated 2026-06-11 — 3 rounds, 1 adversarial sub-agent confirmed
