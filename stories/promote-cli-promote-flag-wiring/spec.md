# Spec: promote-cli

**Created:** 2026-06-11
**Story:** stories/promote-cli-promote-flag-wiring/
**Path:** Quick path — risk-triggered validation (the wired `--promote` triggers a live `league_config.json` write via the committed writer)
**Status:** Validated — awaiting Gate 2b approval
**Baseline:** v1
**Baseline status:** Active

Parent Feature: config-auto-promotion · Parent Epic: win-rate-multi-param-sweep

---

## Ticket Summary

- Add `--promote` to `run_win_rate_simulation.py`: build the sweep store and call the committed `promote_best_combination`, report what was promoted, leave strategy-only and `--sweep` modes unchanged.
- Acceptance: dispatch branch + readable report; CLI-boundary error handling (`ConfigurationError`/`FileOperationError` → log + non-zero exit); `--sweep --promote` runs sweep then promotes; unit tests.
- Final story of the epic.

---

## Problem Summary

The promotion writer (`simulation/win_rate/config_promoter.promote_best_combination`, committed) has no user entry point yet. This story wires it to a `--promote` CLI flag and a `_run_promote_mode` dispatch branch, so the operator can land the best-found combination with one command — and chain it after a sweep.

---

## Proposed Architecture

Edit `run_win_rate_simulation.py` only (+ tests):

1. **Parser** — add `--promote` (`action="store_true"`, sweep-adjacent help text).
2. **Dispatch in `main()`** (D1 — sweep-then-promote):
   ```python
   if args.promote and args.endless:
       logger.error("--promote cannot be combined with --endless ...")
       sys.exit(2)
   if args.sweep:
       _run_sweep_mode(args, data_folder, logger)
       if args.promote:
           _run_promote_mode(data_folder, logger)
       return
   if args.promote:
       _run_promote_mode(data_folder, logger)
       return
   # ... unchanged strategy-only path ...
   ```
3. **`_run_promote_mode(data_folder, logger)`** — build the store, call the writer, handle errors, report:
   ```python
   def _run_promote_mode(data_folder, logger):
       store = SweepResultsManager(data_folder / "win_rate_sweep_results.json")
       try:
           result = promote_best_combination(store, data_folder)
       except (ConfigurationError, FileOperationError) as e:
           logger.error(f"Promotion failed: {e}")
           sys.exit(1)
       _print_promotion(result)
   ```
4. **`_print_promotion(result)`** — print target path, strategy id, cumulative win rate + games, and the 7 promoted param values (D3).

`SweepResultsManager` is already imported. Add imports for `promote_best_combination` and `ConfigurationError`/`FileOperationError`.

**Pros:** mirrors the existing `_run_sweep_mode` dispatch pattern exactly; the destructive logic stays in the already-validated writer; one production file changed.
**Cons:** `--sweep --promote` runs the sweep synchronously first (non-endless) before promoting — acceptable and what the operator asked for; `--endless` is rejected with `--promote` to avoid an unreachable promote.

---

## Key Design Decisions

| ID | Decision | Summary |
|----|----------|---------|
| D1 | Sweep-then-promote dispatch (Gate 2a) | `--sweep --promote` → run the sweep, then promote its winner. `--promote` alone → promote from the existing store. `--endless` combined with `--promote` is rejected (`sys.exit(2)`, clear message) — an endless sweep never returns to promote, and `--endless` is meaningless for a one-shot promote. |
| D2 | CLI-boundary error handling | `_run_promote_mode` catches `ConfigurationError` and `FileOperationError` from the writer, logs `Promotion failed: …`, and `sys.exit(1)` — no traceback dump. All other exceptions propagate (genuine bugs). |
| D3 | Human-readable report | On success print the target path, strategy id, cumulative win rate over games, and each of the 7 promoted params (from `result["param_values"]`). |
| D4 | Reuse the committed writer | `promote_best_combination(store, data_folder)` with its default `config_path=data/configs/league_config.json`; no `--config` flag, no re-implementation. |
| D5 | Branch from local `main` (documented exception) | Local `main` now contains the committed `config_promoter` (this story's dependency) plus the rest of the epic; `origin/main` does not. Cut `feature/promote-cli/kai` from local `main`. Nothing pushed unless the user asks. Same epic-scoped exception as the prior stories. |

---

## Requirements

**Functional:**
- [ ] `--promote` flag exists (`store_true`, default `False`); `run_win_rate_simulation.py --help` succeeds.
- [ ] `--promote` alone → `_run_promote_mode` builds `SweepResultsManager(data_folder / "win_rate_sweep_results.json")`, calls `promote_best_combination(store, data_folder)`, and prints the report; the strategy-only and sweep paths do **not** run.
- [ ] `--sweep --promote` → `_run_sweep_mode` runs, then `_run_promote_mode` runs (in that order); `--sweep` alone is unchanged.
- [ ] `--endless` with `--promote` → logged error + `sys.exit(2)`; neither sweep nor promote runs.
- [ ] Writer errors (`ConfigurationError`, `FileOperationError`) → logged + `sys.exit(1)`; the report is not printed.
- [ ] Strategy-only mode (no flag) is byte-for-byte unchanged in behavior.

**Non-functional:**
- [ ] Matches CODING_STANDARDS (thin `main()`/helper runners, `get_logger`, errors from the hierarchy). The new `_run_promote_mode`/`_print_promotion` helpers mirror `_run_sweep_mode`/`_print_summary` shape.
- [ ] Existing CLI tests that build a manual `argparse.Namespace` and call `main()` are updated to include `promote=False` so `args.promote` resolves (see Build Checklist).

---

## Test Strategy

- **Test kinds in scope:** unit, via the established `run_win_rate_simulation` patch harness (`patch("sys.argv", …)` with the real parser, or `Namespace` + patched dispatch helpers — per `tests/root_scripts/test_run_win_rate_simulation_sweep.py`).
- **New test file:** `tests/root_scripts/test_run_win_rate_simulation_promote.py` — `_run_promote_mode` invokes the writer + reports; config-error and file-error both `sys.exit(1)` without reporting; `--promote` alone dispatches to promote only (sweep/orchestrator not called); `--sweep --promote` calls sweep then promote; `--endless --promote` → `sys.exit(2)` with neither run; `--promote` flag parses (default `False`, present `True`).
- **Existing test update:** `tests/root_scripts/test_run_win_rate_simulation_sweep.py` `_sweep_args` gains `promote=False` (its `Namespace` feeds `rws.main()`, which now reads `args.promote`). The base file (`test_run_win_rate_simulation.py`) uses the real parser via `sys.argv`, so it auto-defaults — no change needed there.
- **Project conventions:** pytest, `MODULE = "run_win_rate_simulation"`, `unittest.mock.patch` on the module namespace, `capsys` for report assertions, `pytest.raises(SystemExit)` for exit paths.

**Escalation:** introduces a new test file → testing escalates to a full `testing_plan.md` via `/e3b-write-testing-plan`.

---

## Review Prevention Gates

| Surface | Applies? | Requirement / Prevention | Evidence |
|---------|----------|--------------------------|----------|
| Regulated / sensitive data | No | Public NFL config scalars. | — |
| Tenant / auth / route | No | Local CLI tool. | ARCHITECTURE.md |
| Database read/write | No | No DB; the destructive config write is in the committed writer (already tested). | — |
| Infrastructure / deployment | Yes (indirect) | This flag is the user entry point that triggers the live `league_config.json` write. Prevention lives in the writer (atomic write, git dirty-state warning, key preservation — covered by `config-promoter`); this story adds CLI-boundary error handling so writer failures exit cleanly. No new writer mechanics here. | D2; `config-promoter` review_v1 |
| Frontend | No | CLI only. | — |
| Testing / test data | Yes | New unit tests + one existing arg-builder update (manifested). | Test Strategy |
| Removed/weakened checks | No | Additive; strategy-only and sweep paths unchanged. | Requirements |

---

## Out of Scope

- The promotion writer itself (`config-promoter`, committed — reused).
- The sweep/tournament/store (reused/read).
- A `--config` flag or promoting per-week-range files (writer targets `league_config.json` only).

---

## Open Questions

*(None — D1 (sweep-then-promote + endless rejection) resolved at Gate 2a; D2–D5 resolved by the architect against the committed writer + CLI structure.)*

---

## Evidence

### Research Findings
- `run_win_rate_simulation.py` — `_build_parser()` declares flags; `main()` (line 126) dispatches `if args.sweep: _run_sweep_mode(args, data_folder, logger); return` before constructing the strategy orchestrator. `_run_sweep_mode` (line 160) builds `SweepResultsManager(data_folder / "win_rate_sweep_results.json")`. `SweepResultsManager` is already imported (line 18). `data_folder = Path(args.data)`; `--data` default `simulation/sim_data`.
- `simulation/win_rate/config_promoter.promote_best_combination(store, data_folder, config_path="data/configs/league_config.json") -> {strategy_id, param_values, win_rate, games}`; raises `ConfigurationError` (empty store / unresolved strategy / missing-corrupt config) and `FileOperationError` (write failure).
- `tests/root_scripts/test_run_win_rate_simulation_sweep.py` — `_sweep_args(tmp_path)` builds a manual `Namespace(...)` **without** `promote` and calls `rws.main()` in `test_sweep_flag_dispatches_to_sweep_mode` / `test_no_sweep_runs_strategy_only`; these need `promote=False` once `main()` reads `args.promote`.
- `tests/root_scripts/test_run_win_rate_simulation.py` `TestMainFlow` — uses `patch("sys.argv", …)` + the real parser, so `args.promote` auto-defaults to `False`; `test_help_shows_all_new_flags` asserts a non-exhaustive flag list (adding `--promote` won't break it).

### Architecture And Standards Notes
- CODING_STANDARDS: thin runner helpers, `get_logger`, error hierarchy. New helpers mirror the existing `_run_sweep_mode`/`_print_summary` idiom.
- ARCHITECTURE.md: the `league_config.json` writers column already gained "Win-rate sim `--promote`" in the `config-promoter` story; this story realizes that `--promote` entry point. No further doc change required (verify in Review).

### Review Prevention Evidence
- The destructive surface is the writer (covered by `config-promoter` tests incl. write-failure). This story's added risk is only CLI dispatch correctness + clean error exit — covered by the new tests.

---

## Code Shapes

- `run_win_rate_simulation.py` (EDIT) — add `--promote` arg; add `_run_promote_mode(data_folder, logger)` + `_print_promotion(result)`; insert the dispatch branch in `main()`; add imports `promote_best_combination`, `ConfigurationError`, `FileOperationError`.
- `tests/root_scripts/test_run_win_rate_simulation_promote.py` (CREATE).
- `tests/root_scripts/test_run_win_rate_simulation_sweep.py` (EDIT) — `_sweep_args` gains `promote=False`.

---

## Build Checklist

0. BRANCH - per **D5**: `git checkout main && git checkout -b feature/promote-cli/kai` (local `main`, holds `config_promoter`). If the branch exists, stop and report.
1. EDIT `run_win_rate_simulation.py` imports - add `from simulation.win_rate.config_promoter import promote_best_combination` and `from utils.error_handler import ConfigurationError, FileOperationError`.
2. EDIT `_build_parser` - add the `--promote` `store_true` argument with help text (after `--calib-sims`).
3. EDIT `main()` - add the `--endless` + `--promote` guard (`sys.exit(2)`), the `if args.promote` branch inside the `args.sweep` block (sweep-then-promote), and the standalone `if args.promote` branch before the strategy path (D1).
4. CREATE `_run_promote_mode(data_folder, logger)` + `_print_promotion(result)` per D2/D3.
5. EDIT `tests/root_scripts/test_run_win_rate_simulation_sweep.py` - `_sweep_args` Namespace gains `promote=False`.
6. CREATE `tests/root_scripts/test_run_win_rate_simulation_promote.py` - the Test Strategy cases (mirrors `testing_plan.md`; Phase 5 executes).
7. VERIFY - `python -m pytest tests/root_scripts/test_run_win_rate_simulation_promote.py tests/root_scripts/test_run_win_rate_simulation_sweep.py tests/root_scripts/test_run_win_rate_simulation.py -vv` → all pass.

---

## Review Prevention Checklist

- [ ] Testing: new CLI dispatch tests + the manifested `_sweep_args` update (Build steps 5–6 / Phase 5).
- [ ] Infrastructure (indirect): CLI-boundary error handling for the writer's `ConfigurationError`/`FileOperationError` (Build step 4); destructive write mechanics owned/tested by `config-promoter`.
- [ ] No regulated/tenant/auth/DB/frontend/removed-check obligation — N/A reasons recorded.

---

## Verification

- [ ] `python -m pytest tests/root_scripts/test_run_win_rate_simulation_promote.py tests/root_scripts/test_run_win_rate_simulation_sweep.py tests/root_scripts/test_run_win_rate_simulation.py -vv` passes.
- [ ] Full gate `python tests/run_all_tests.py` passes (no regression).
- [ ] Manual smoke: `python run_win_rate_simulation.py --help` lists `--promote`; `--promote` with an empty store logs `Promotion failed: …` and exits 1 (no traceback).

---

## Post-Build Review

**Plan Alignment:** N/A - Quick path used spec Build Checklist instead of implementation_plan.md.

**Findings:** [Pending Build.]

---
Validated 2026-06-11 — 1 round, 1 adversarial sub-agent confirmed
