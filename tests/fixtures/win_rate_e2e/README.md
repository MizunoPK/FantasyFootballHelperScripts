# `win_rate_e2e` config fixture

A frozen snapshot of a `<root>/configs/` league-config tree, used so the win-rate tests below
score against a **committed** config instead of the live `data/configs/league_config.json`.

## Provenance

Snapshotted from `data/configs/` at the commit that pinned `best_win_rate` in
`tests/root_scripts/test_run_win_rate_simulation_e2e.py` (delivery unit D4.3), then **frozen**.
Its `parameters.ADP_SCORING.THRESHOLDS.DIRECTION` is pinned to `DECREASING` — the post-D4.2
value — as an intentional pin, not as a copy that tracks the live store.

The tree is five files because that is the shape `ConfigManager` requires: it is reached as
`config_path.parent.parent`, selects the `configs/` subdirectory, and merges the `week{N}-{M}.json`
matching `CURRENT_NFL_WEEK`. All four week files are committed, not just the one matching the
fixture's own `CURRENT_NFL_WEEK`, because a missing week file does **not** fail — it logs a
WARNING and merges an empty dict, so a later edit to `CURRENT_NFL_WEEK` would silently score
against an unmerged config.

## Consumers (complete list)

- `tests/root_scripts/test_run_win_rate_simulation_e2e.py` — passes `--config` at this tree and
  asserts an exact `best_win_rate` measured against it. This is the only consumer that asserts a
  win-rate value.
- `tests/integration/test_simulation_integration.py` — the two in-process
  `DraftStrategyOrchestrator` constructions (`test_orchestrator_initializes` and the
  `_make_orchestrator` helper) pass `config_path=` at this tree. Neither asserts a win-rate value.

## Rules

1. **Never re-sync this tree to `data/configs/`.** Re-syncing restores exactly the live-config
   coupling this fixture exists to cut.
2. **Read it; never edit it to suit a new test.** A test needing different config values adds its
   own fixture. Editing this one to suit a new consumer re-creates, by accretion, the shared-fixture
   coupling a single-purpose tree was chosen to avoid.
3. **If you add a consumer, add it to the list above.** The list is load-bearing: it is what makes
   "single-purpose" checkable rather than assumed.

Note that the tripwire is only partly mechanical. An edit touching any scoring parameter the draft
path reads moves `best_win_rate` and fails the e2e pin loudly; an edit to a key that path ignores
passes silently. That is why rule 2 is written down rather than left to the pin.
