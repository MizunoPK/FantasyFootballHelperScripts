# Story promote-cli Ticket

<!-- Parent back-refs (optional). Present when this story was created by /p4-decompose-feature; absent for standalone stories. -->
**Parent Feature:** config-auto-promotion
**Parent Epic:** win-rate-multi-param-sweep

**Tracker profile:** local
**Source:** PO flow — /p4-decompose-feature
**Date received:** 2026-06-11

---

Add a `--promote` flag to `run_win_rate_simulation.py` that invokes the committed promotion writer (`simulation/win_rate/config_promoter.promote_best_combination`) to land the winning sweep combination into the live `league_config.json` and reports what was promoted, leaving the existing strategy-only and `--sweep` modes unchanged.

## Acceptance Criteria

- `run_win_rate_simulation.py --promote` constructs `SweepResultsManager(data_folder / "win_rate_sweep_results.json")` and calls `promote_best_combination(store, data_folder)` (writer's default `config_path` = `data/configs/league_config.json`), then prints a readable report of what was promoted (strategy id, cumulative win rate, games, and the 7 promoted param values).
- The writer's raised errors are handled at the CLI boundary: `ConfigurationError` (empty store, strategy unresolved, missing/corrupt config) and `FileOperationError` (write failure) are logged and the process exits non-zero — no traceback dump.
- The existing strategy-only mode (no flag) and `--sweep` mode are unchanged: `--promote` is its own dispatch branch and does not run a sweep or strategy pass.
- A unit test exercises the `--promote` dispatch (promoter invoked + result reported) and the error-exit path, with `promote_best_combination` patched.

## Context / References

- Built component (on `main`): `simulation/win_rate/config_promoter.promote_best_combination(store, data_folder, config_path="data/configs/league_config.json") -> {strategy_id, param_values, win_rate, games}`; raises `ConfigurationError` / `FileOperationError`.
- CLI structure: `run_win_rate_simulation.py` — `_build_parser()` declares flags; `main()` dispatches `if args.sweep: _run_sweep_mode(...); return` before the strategy path. `--promote` mirrors that pattern with a `_run_promote_mode(...)` helper.
- The sweep store path is `data_folder / "win_rate_sweep_results.json"` (same as `_run_sweep_mode`); `--data` defaults to `simulation/sim_data`.
- Parent feature `features/config-auto-promotion-winner-promotion/feature.md`: `--promote` writes only `league_config.json`; week-range files untouched (guaranteed by the writer).

**Deferred to Spec (Gate 2a):** interaction when `--promote` is combined with `--sweep` (run sweep then promote, vs. promote-only / mutually exclusive); exact report formatting.

---

## Open Questions

*(None at the ticket level — scope is well-defined by the validated parent feature and the committed writer. The `--sweep` + `--promote` interaction is a design choice deferred to Spec/Gate 2a.)*
