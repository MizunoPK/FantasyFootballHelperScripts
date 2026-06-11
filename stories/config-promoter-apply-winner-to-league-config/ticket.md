# Story config-promoter Ticket

<!-- Parent back-refs (optional). Present when this story was created by /p4-decompose-feature; absent for standalone stories. -->
**Parent Feature:** config-auto-promotion
**Parent Epic:** win-rate-multi-param-sweep

**Tracker profile:** local
**Source:** PO flow — /p4-decompose-feature
**Date received:** 2026-06-11

---

## Ask

Provide the promotion writer that lands the sweep's winning combination into the live `league_config.json`: rank the sweep store's combinations by cumulative win rate, take the best `(strategy_id, param_values)`, resolve that strategy's `DRAFT_ORDER`, apply it + the 7 draft-side params onto `league_config.json` via the committed `apply_draft_overrides` (every other key preserved), and write the file atomically (tmp→rename). Because recovery relies on git, warn before overwriting if `league_config.json` has uncommitted changes. This is the one component that mutates the operator's live config.

## Acceptance Criteria

- Resolves the best combination from the sweep store (`SweepResultsManager.get_all_combinations()` → `sweep_summary.rank_combinations` top entry, ranked by cumulative win rate) — its `strategy_id` + `param_values` (the 7 flat param names, as stored).
- Loads the winning strategy's `DRAFT_ORDER` (the store keys by strategy filename; resolve it via the shared strategy loader).
- Applies `DRAFT_ORDER` + the 7 params onto the current `league_config.json` via `apply_draft_overrides` (preserving all other keys — `CURRENT_NFL_WEEK`, `MAX_POSITIONS`, scoring sub-blocks, etc.) and writes atomically (tmp-file → rename).
- A pre-write git dirty-state check on `league_config.json` surfaces uncommitted changes before overwriting (the recovery path is git); exact warn-vs-block behavior is a Gate 2a decision.
- An empty store (no combinations) is handled gracefully (clear error, no write).
- Unit tests: promotes the top combination's `DRAFT_ORDER` + 7 params, preserves all other keys, atomic write produces valid JSON, empty-store path, and the git dirty-state path.

## Context / References

- Parent feature: `features/config-auto-promotion-winner-promotion/feature.md` (validated; recovery = git; the win-rate sim becomes a new writer of `league_config.json`).
- Committed building blocks (all on `main`): `simulation/win_rate/SweepResultsManager.get_all_combinations()` (records `{strategy_id, param_values, best_win_rate, total_wins, total_games, total_runs, last_run}`); `simulation/win_rate/sweep_summary.rank_combinations(combinations, n)` (ranked by cumulative win rate); `simulation/win_rate/config_overrides.apply_draft_overrides(base_config, draft_order, param_values)` (the stored `param_values` are already keyed by the 7 flat names, directly usable); `simulation/win_rate/strategy_loader.load_valid_strategies(data_folder)` (resolve the winner's `DRAFT_ORDER` by filename).
- Existing promotion precedent: `simulation/accuracy/AccuracyResultsManager.propagate_to_configs` — copies optimal configs to `data/configs/`, preserves user-maintained keys, but writes **non-atomically with no backup**; this story improves on that with atomic write + git-based recoverability (per the feature decision).
- Target: `data/configs/league_config.json` (the live base config).
- **Deferred to Spec (Gate 2a):** (a) **warn-vs-block** on a dirty `league_config.json` (warn-and-proceed since git recovers, vs. block-unless-`--force`); (b) **min-sample guard** — should promotion refuse a winner below a minimum cumulative games (avoid promoting a tiny-sample fluke)? (c) interface/module placement (`simulation/win_rate/config_promoter.py`?) and empty-store handling; (d) **path** — this mutates the live config (a destructive edit, git-recoverable), so it likely warrants risk-triggered adversarial validation even on the Quick path.

---

## Open Questions

*(None at the ticket level — scope is well-defined by the validated parent feature. Substantive design choices are recorded above as deferred to Spec.)*
