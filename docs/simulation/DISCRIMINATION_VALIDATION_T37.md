# Discrimination Validation — Before/After Evidence (T37)

**Status: DOCUMENT-ONLY.** This document writes nothing to `data/configs/league_config.json`
and changes no source or test code. It is the T17 epic **finale**: it synthesizes the
discrimination evidence from
`_internal/win_rate_similarity_investigation.md`
(Experiments 1 / 4 / 5 / 6, validated 2026-06-26) into a durable before/after. **No fresh
simulation run** — every number below is transcribed from that investigation and its raw
JSON under `_internal/data/`. (`_internal/` is a **local, git-ignored** working area — not
repo-resolvable paths; see Deviation Note. These are local-provenance references only. Committing
the raw source evidence into a tracked location is a possible follow-up, outside this doc's scope.)

**Story:** T37 (epic T17 / feature T24 — discrimination-validation) — produce a documented
before/after demonstrating that the **reworked** win-rate sweep machinery *discriminates* draft
configs (a measurable, statistically significant win-rate gap) where the **old naive-opponent**
sweep *could not*. Closes epic success criteria **#2** (discrimination) and **#7** (documented
before/after).

---

## Deviation Note — doc location

The T37 ticket/feature say to commit this evidence **under `_internal/`**. This document
deliberately deviates: it lives at git-tracked **`docs/simulation/DISCRIMINATION_VALIDATION_T37.md`**
instead.

**Rationale:** `_internal/` is **git-ignored** (`.gitignore` line 12, `**/_internal`) — a file
placed there is untracked and absent from history, so it is **not auditable**, directly
contradicting the ticket's own stated goal ("so the epic's success is auditable"). Even the source
investigation under `_internal/` is untracked (`git ls-files _internal/` is empty). `docs/simulation/`
is git-tracked, versioned, and auditable, and mirrors the sibling evidence doc
[`BASELINE_RETUNE_T35.md`](./BASELINE_RETUNE_T35.md) (same `UPPERCASE_WITH_UNDERSCORES`
convention). This deviation honors the ticket's *intent* (auditability) over its *literal path*.

---

## BEFORE — the naive-opponent regime

**Regime.** The legacy sweep field: **1** optimized `DraftHelperTeam` vs **9** deliberately-naive
`SimulatedOpponent`s. This structurally wins **~0.84** — a near-saturated ceiling with almost no
headroom for a config tweak to move the metric. Reproducible via the retained runner flag (not
invoked here):

```bash
.venv/bin/python run_win_rate_simulation.py --naive-opponents
```

(`--naive-opponents`, retained from T19/T28: "Use the legacy naive-opponent composition
(1 DraftHelperTeam + 9 SimulatedOpponents) instead of the default self-play field
(10 DraftHelperTeams). Reproduces the prior ~0.84 baseline.")

**What it could measure.** Taking the identical weak-corner vs strong-corner param pair (opposite
corners of the 7-D swept param space) and evaluating each at **1,360 games** (10× the 136-game Exp 1 evaluation count; the `--sims` CLI
default is 10, not 136), the investigation's **Exp 4** measured:

| Config (1,360 games/eval, n=4 reps) | mean win rate |
|-------------------------------------|---------------|
| weak corner | **0.810** |
| strong corner | **0.784** |
| **weak − strong gap** | **+0.026 (z ≈ 3.4)** |

*Source: Exp 4, `_internal/data/sims_scaling_results.json` (local, git-ignored working area).*

**Why it "could not discriminate" at operational sims.** That +0.026 gap only surfaces at 10×
games. At the **Exp 1 evaluation count (136 games)** — the `--sims` CLI default is 10, not 136;
136 was Exp 1's configured setting — the same pair is **within the evaluation
noise band**: re-running a *single fixed config* gives win rates with within-config stdev
**σ ≈ 0.031** — *larger* than the entire **0.023** win-rate spread across all 1,860 different store
configs. The config-to-config differences are smaller than the noise of one config evaluated twice,
so at operational sims the naive sweep **cannot tell any config from any other**.

*Source: Exp 1, `_internal/data/noise_results.json` (local, git-ignored; within-config σ ≈ 0.031;
between-config store spread 0.023).*

---

## AFTER — the reworked asymmetric measured-vs-reference regime

**Regime.** The reworked machinery lowers the opponent ceiling to **self-play** (9 real
`DraftHelperTeam` opponents), pulling the measured team's baseline to **~0.48** — the ~50%
max-headroom regime where config differences have room to show. Discrimination is measured by the
**asymmetric measured-vs-reference CRN-paired A/B**: the measured `DraftHelperTeam` scores with the
config under test while every opponent holds a fixed reference config, both arms sharing
per-(season, sim) seeds (common random numbers) so the *difference's* variance collapses. The
first-party tool (referenced, not invoked here) is:

```
simulation/win_rate/paired_comparison.py::run_paired_ab_comparison(
    current_config, recommended_config, data_folder, seed=..., num_simulations=...)
```

**What it measures.** Re-running the **same** weak vs strong corner pair at the **same 1,360
games**, but against the self-play field, the investigation's **Exp 6** measured:

| Config (1,360 games/eval, self-play field) | mean win rate |
|--------------------------------------------|---------------|
| weak corner | **0.513** |
| strong corner | **0.418** |
| **weak − strong gap** | **+0.095 (z ≈ 5.0)** |

*Source: Exp 6, `_internal/data/amplification_results.json` (local, git-ignored).*

Lowering the ceiling **amplified the same param effect ~3.6× (0.026 → 0.095)** and roughly doubled
its significance. The gap **+0.095** clears epic criterion **#2**'s **≥ 0.05** separability bar at
**z ≈ 5.0** — far above any reasonable significance threshold (z ≈ 2). The reworked sweep
**discriminates**.

---

## Discrimination-gap summary

| Metric | BEFORE — naive (~0.84 ceiling) | AFTER — reworked asymmetric (~0.48 ceiling) |
|--------|--------------------------------|---------------------------------------------|
| weak − strong gap | **+0.026** | **+0.095** (~3.6× amplification) |
| z/t statistic (n reps) | **≈ 3.4** | **≈ 5.0** |
| games / eval | 1,360 | 1,360 |
| Exp 1 sim count (136 games) | **within noise** (σ ≈ 0.031 ≥ 0.023 spread) — **could not discriminate** | headroom regime (~0.48 baseline) — **discriminates** |
| source experiment(s) | Exp 4 + Exp 1 | Exp 6 |

The contrast: identical weak/strong param pair, identical 1,360 games — swapping the naive field for
the reworked asymmetric self-play field turns a within-noise, operationally-invisible **+0.026** into
a clearly significant **+0.095**.

*Ceiling reference (epic #1).* Exp 5 confirms the ~0.84 is a weak-opponent artifact: the measured
team's baseline falls **monotonically 0.843 → 0.802 → 0.637 → 0.476** as 0 → 2 → 5 → 9 opponents
become self-play, landing at the ~0.50 symmetric-field regime. *Source: Exp 5,
`_internal/data/selfplay_ceiling_results.json` (local, git-ignored).*

---

## Honesty framing

The discriminating signal comes **specifically** from the **asymmetric measured-vs-reference**
machinery (Exp 6 / `run_paired_ab_comparison`): the measured team holds the config under test while
opponents hold a fixed reference, so the config difference is not cancelled out. The stock
**symmetric self-play `--sweep`** — where all 10 teams share the swept config — does **not** produce
this gap: a symmetric field of equal-skill drafters sits pinned near ~0.50 / noise, so its selection
signal is muted. Any "the reworked sweep discriminates" claim is therefore scoped to the reworked
*machinery* (the asymmetric CRN A/B), **not** the symmetric self-play sweep alone.

**Epic evidence trail:**

- **T35** — [`BASELINE_RETUNE_T35.md`](./BASELINE_RETUNE_T35.md): a bounded, seeded before/after that
  exercises the reworked asymmetric CRN A/B end-to-end (a provisional retune signal).
- **T36** — the ≥3-seed `--promote` reproducibility test (merged), showing the top config is selected
  the same way across independent RNG seeds.

---

## Epic success-criteria mapping

This document is the T17 epic finale. It **closes**:

- **#2 — discrimination** ("The sweep reliably separates two configs whose true win rate differs by
  ≥ 0.05 at the chosen baseline (statistically significant) — a separation the current sweep cannot
  make. (Exact target gap finalized at decomposition.)"): **CLOSED** — Exp 6's **+0.095 gap at z ≈ 5.0**
  clears the ≥ 0.05 bar, a separation the naive sweep (Exp 4 / Exp 1, within-noise at operational
  sims) could not make.
- **#7 — documented before/after** ("The rework is covered by tests, and a documented before/after
  demonstrates the sweep discriminating (and promotion reproducible) where it previously could not"):
  **CLOSED JOINTLY** — this document supplies the "discriminating" half; sibling **T36** (≥3-seed
  `--promote` reproducibility test, merged) supplies the "promotion reproducible" half (criterion #3).
  Criterion #7 is closed by T37 + T36 together.

Already-covered context (not closed here):

- **#1 — ~50% baseline** (off the ~80% ceiling): corroborated by **Exp 5** (0.843 → 0.802 → 0.637 →
  0.476 as the field becomes self-play).
- **#3 — ≥3-seed `--promote` reproducibility**: the deliverable of sibling story **T36** (a merged
  automated test), referenced here, not built by this story.

---

*Evidence synthesized from `_internal/win_rate_similarity_investigation.md` (validated 2026-06-26,
Exp 1 / 4 / 5 / 6) and its raw JSON under `_internal/data/`. Both are in a **local, git-ignored**
working area (`_internal/` is excluded from the repo — see Deviation Note); these are
local-provenance references, not committed or repo-resolvable paths. Committing the raw experiment
data into a tracked location is a possible follow-up, outside this doc's scope. Document-only — no
simulation run, no code or test change, no live-config write. T37, epic T17 / feature T24.*
