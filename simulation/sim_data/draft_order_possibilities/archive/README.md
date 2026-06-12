# Archived Draft Strategies

Files in this directory are not loaded by `DraftStrategyOrchestrator` (the orchestrator
uses non-recursive `glob("*.json")` on the parent directory, so this subfolder is
naturally excluded).

## Why files are here

These strategies were identified as functional duplicates of strategies still in
active use. Keeping them out of the sim avoids:

- Diluting the meta_data signal across functionally identical strategies
- Wasting sim cycles producing the same result under a different name
- Inflating the search-space size for the parameter-sweep epic (FF-7)

## Archived files

### `41_stream_premium.json` — duplicate of `20_depth_first.json`
**Byte-identical** DRAFT_ORDER array. Same primaries AND same secondaries in all 15
rounds. Only `name` and `description` differ. There is no parameter-config under
which these would produce different sim outcomes.

### `31_double_qb_spread.json` — functional duplicate of `7_elite_qb_early.json`
Same primary position in all 12 meaningful rounds (`QB,RB,WR,RB,WR,TE,RB,WR,TE,RB,
WR,QB`). Differs only in 2 secondary preferences (R6, R9 — TE backed by FLEX vs WR).
The description claims "maximum gap" QB drafting but the structure puts QBs at R1
and R12, which is exactly what Elite QB Early does. Sim outcomes are
indistinguishable for practical purposes.

## Restoring an archived strategy

Move the file back to the parent directory:

```
mv archive/<filename>.json ../
```

It will be picked up on the next orchestrator run.

## Stale meta_data entries

`simulation/sim_data/win_rate_meta_data.json` may still have entries for archived
strategies. The orchestrator ignores them (it only writes/reads entries for files
it iterates). The entries are kept for historical reference; they can be manually
deleted if desired.

---

*Archived: 2026-05-28 during FF-7 (win_rate_param_sweep) planning.*
