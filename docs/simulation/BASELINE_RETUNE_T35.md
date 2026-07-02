# Baseline Re-Tune — Before/After Evidence (T35)

**Status: PROVISIONAL.** These numbers come from a **bounded, seeded** in-flow win-rate sweep
(a deliberately small `--sims`/`--num-values` run over a 3-strategy subset), NOT the definitive
full baseline. They exercise the reworked discriminating machinery end-to-end and give a
directional before/after signal — they are **not** an authoritative re-tune. See FOLLOW-UP.

**Story:** T35 (epic T17 / feature T23) — run the discriminating sweep, capture the recommended
baseline draft params and the before/after win-rate delta vs the current live config, and
record it for the epic evidence trail. This document is **document-only**: it writes nothing to
`data/configs/league_config.json`. Applying the recommendation is a separate, explicit,
human-gated `--promote --confirm` step (T34) — out of scope here.

---

## Regime

- **Candidate SELECTION:** the bounded DEFAULT self-play `--sweep` (10 self-play
  DraftHelperTeams share each swept config — symmetric; the self-play win rate may barely move,
  so selection here is a weak/provisional signal).
- **Delta MEASUREMENT:** the ASYMMETRIC measured-vs-reference CRN-paired A/B
  (`simulation/win_rate/paired_comparison.py::run_paired_ab_comparison`) — the empirically
  discriminating setup (investigation Exp 6: weak−strong gap ≈ 0.095, z ≈ 5.0). The measured
  DraftHelperTeam scores with the config under test; every opponent holds the current baseline;
  both arms share per-(season, sim_id) seeds (common random numbers), so the variance of the
  before/after difference collapses.

---

## Recommended Params (current → recommended)

Winning strategy (DRAFT_ORDER): `1_zero_rb.json`

| Param | Current (live) | Recommended (bounded sweep) |
|-------|----------------|-----------------------------|
| SAME_POS_BYE_WEIGHT | `0.07` | `0.07` |
| DIFF_POS_BYE_WEIGHT | `0.01` | `0.01` |
| PRIMARY_BONUS | `67` | `67` |
| SECONDARY_BONUS | `69` | `69` |
| ADP_SCORING_WEIGHT | `4.76` | `0.5` |
| PLAYER_RATING_SCORING_WEIGHT | `3.52` | `3.52` |

---

## Before/After Delta (asymmetric measured-vs-reference CRN-paired A/B)

| Metric | Value |
|--------|-------|
| Current win rate (before) | `0.5735` |
| Recommended win rate (after) | `0.6029` |
| Δ (recommended − current) | `0.0294` |
| z (pooled two-proportion) | `0.348` |
| Games (per arm) | `68` |
| Seed | `20260701` |
| Regime | asymmetric measured-vs-reference, CRN-paired |

Reproduce the delta: call `run_paired_ab_comparison(current_config, recommended_config,
Path("simulation/sim_data"), seed=20260701, num_simulations=1)` with the two configs above.

---

## Sweep Provenance

Exact bounded command (self-play default; fixed seed; write-isolated scratch `--data`):

```bash
# $SCRATCH = a mktemp -d dir holding symlinks to the 2021, 2022, 2024, and 2025 season folders
# (season 2023 was skipped at runtime as invalid — only 85 valid players, below the 150-player
# threshold — so 4 seasons × 17 games/arm = 68 games/arm) and a 3-strategy subset
# (1_zero_rb.json, 12_safe_floor.json, 14_robust_rb.json) under draft_order_possibilities/ —
# so all sweep writes land in $SCRATCH, never in simulation/sim_data/.
.venv/bin/python run_win_rate_simulation.py --sweep --sims 1 --num-values 3 --seed 20260701 --workers 8 --data "$SCRATCH"
```

- **Bounded params:** `--sims 1`, `--num-values 3`, 3-strategy subset, fixed `--seed 20260701`.
- **No live-config write:** no `--promote --confirm` was run. The candidate params were read via
  the dry-run `compute_promotion` path; the live config was read READ-ONLY.
- **Live config unchanged (D4):** `sha256(data/configs/league_config.json)` =
  `c824b8b41af7aaec602323fe528a4cf43b72258fdcabd03579668c60ea83ac6b` (equal before and after the whole run;
  baseline `c824b8b41af7aaec602323fe528a4cf43b72258fdcabd03579668c60ea83ac6b`).

---

## PROVISIONAL Caveat

This is a **weak, bounded** signal, not the definitive re-tune. The default self-play sweep
applies each swept config symmetrically to all 10 teams, so the selection signal is muted; the
bounded `--sims`/`--num-values`/strategy-subset limits statistical power. Treat the recommended
params as a **directional candidate**, and the delta as **provisional evidence** that the
asymmetric CRN A/B discriminates — not as grounds to promote.

## FOLLOW-UP (out of scope for T35)

Run the **full, overnight, human-launched `--sweep`** (all ~49 strategies, larger `--sims`,
denser `--num-values`, to convergence) per `TESTING_STANDARDS.md` (multi-hour sweeps are a
human-launched activity) to produce the authoritative recommendation, then re-measure the delta
with the same asymmetric CRN A/B and, if warranted, apply via the human-gated
`--promote --confirm` (T34). This bounded run is the interim provisional evidence until then.
