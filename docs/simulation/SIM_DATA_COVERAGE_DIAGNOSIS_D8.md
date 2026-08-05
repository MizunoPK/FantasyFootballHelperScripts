# sim_data Projection Coverage — Diagnosis Record (D8)

**Status: DOCUMENT-ONLY.** This document changes no source or test code, writes nothing to
`simulation/sim_data/`, `simulation/simulation_configs/` or `data/configs/`, and performs no fetch
and no simulation run. It records a diagnosis; it repairs nothing.

**Ticket:** D8 (`sim-data-projection-coverage-gaps`), authored by unit **D8.1**. Every figure below is
**transcribed** from that ticket's validated intake record and design digest — there was no fresh
measurement, no re-derivation, and above all **no re-fetch** performed for this document. That is
deliberate: §"The ESPN archive degrades" explains why a casual re-fetch is the one action this record
exists to prevent.

---

## TL;DR — four facts, in causal order

1. **2023 week 1 projections are zeroed at the source.** ESPN returns the rows, but for that
   season-week almost all of them carry `appliedTotal == 0.0`. The compiler is behaving correctly;
   the loss is upstream of this repository.
2. **It is irrecoverable, and this is proven rather than assumed.** A compile taken eight months
   earlier already showed the same gap, and no cached raw payload exists anywhere in the tree or in
   git history.
3. **The accuracy engine *scored* those zeros rather than skipping them.** Its pairwise comparison
   skips only *actual* ties, so a pair of zero projections is evaluated as a confident prediction —
   right about half the time by luck — not as an abstention.
4. **Every accuracy config promoted to date was fitted with them.** 224 poisoned observations sat
   inside the `week_1_5` objective while every `accuracy_optimal_*` folder and every promoted
   `data/configs/week1-5.json` was being selected.

---

## Defect A — mechanism and evidence

**Coverage, measured scale-free.** Population: the **top 200 players by season actual production**,
the identical rule for every season (never a top-N-by-ADP cut, which would couple this detector to
Defect B below). Counted: players carrying a **week 1** projection, against a bye-included
denominator of 200.

| season | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|--:|--:|--:|--:|--:|
| week 1 coverage | 196/200 | 183/200 | **32/200** | 190/200 | 190/200 |

2023 sits at **16.0%** where its four siblings sit between 91.5% and 98%.

**It is not a compiler bug and not a fetch-parameter bug.** ESPN *does* return `statSourceId=1` rows
for 2023 `scoringPeriodId=1` — **1,128** of them — but **1,037 carry `appliedTotal == 0.0`**; only
**91** are greater than zero, and the maximum is **15.4**. Probing `scoringPeriodId=1` against
`scoringPeriodId=0` returns **byte-identical** results, so the parameter is not the cause either.

**The compiler is correct, and that is what locates the loss upstream.**
`historical_data_compiler/player_data_fetcher.py:440-442` drops zero-valued projections by design:

```python
if projected_points is not None:
    if position == 'DST' or projected_points > 0:
        projected_weeks[week] = projected_points
```

A zeroed projection is not a projection, so dropping it is right. The data never existed on ESPN's
side in usable form — which is why nothing in this repository can be changed to recover it.

---

## Irrecoverability — the proof, not an assertion

**A recompile cannot fix 2023 week 1.** The December-2025 compile at
`adc0f749:simulation/sim_data/2023/weeks/week_17/players_projected.csv` already carried exactly
**85** week-1 projections against **430** for week 2. Those two are **whole-file counts over all 798
players in that compile** — not the top-200 population used above — and are directly comparable to
each other. The gap is therefore **stable across two fetches eight months apart**, not an artifact of
one bad request.

**And there is no local fallback.** No cached raw ESPN payload exists in the working tree or anywhere
in git history, so there is nothing to re-parse.

**Option D — "just recompile 2023" — is recorded as REJECTED, with its evidence, so that a later
reader does not mistake the rejection for an untried idea.** It was rejected on two independent
grounds:

1. **Futile for 2023.** The `adc0f749` counts above show the gap predates the current fetch; a
   re-fetch reproduces it.
2. **Net-negative risk for the other four seasons.** ESPN's archive demonstrably degrades — see
   §"The ESPN archive degrades" — so a blind recompile can replace a currently-good season with a
   worse snapshot recoverable only from git.

This is the reasoning behind D8's defining constraint: **D8 changes no byte of
`simulation/sim_data/`.**

---

## Contamination arithmetic — why the zeros were scored, not skipped

The `week_1_5` horizon **includes week 1** (`simulation/accuracy/horizon_labels.py:27`,
`'week_1_5': (1, 5)`). Counting qualifying observations (`actual >= 3`) against the projection the
harness actually reads:

| season-week | qualifying | zero-projection |
|---|--:|--:|
| 2021 wk1 | 269 | 1 (0%) |
| 2022 wk1 | 267 | 4 (1%) |
| **2023 wk1** | **271** | **224 (83%)** |
| 2023 wk2 | 281 | 6 (2%) |
| 2024 wk1 | 251 | 3 (1%) |
| **whole horizon** | **6,508** | **327 (5.0%)** |

**224 of the 327 come from 2023 week 1 alone.**

The mechanism is in `simulation/accuracy/AccuracyCalculator.py`:

```
409:  if actual_i == actual_j:      # skips only ACTUAL ties
410:      continue
412:  predicted_order = proj_i > proj_j
```

Line `:409` skips a pair only when the two **actuals** tie. Line `:412` then evaluates
`proj_i > proj_j`, which is uniformly `False` when **both projections are `0.0`** — a definite
"j outranks i" prediction, not an abstention. **There is no projection-tie guard anywhere in the
loop.** So each zeroed pair is scored as a confident prediction that is right about half the time by
luck, and the pairwise metric — which is the accuracy engine's *selection objective*, not a reported
side statistic — is diluted toward 50% on `week_1_5` in proportion to the zeroed share.

---

## Consequence for already-promoted artifacts

Every `accuracy_optimal_*` folder under `simulation/simulation_configs/` and every promoted
`data/configs/week1-5.json` produced **to date** was fitted with those 224 poisoned observations
inside its objective.

D8 **re-runs and re-promotes nothing** — that is operational work, outside the ticket's scope. The
point of recording it here is narrower and more useful: a later operator re-tuning `week1-5.json`
would otherwise have no way to know that the prior baseline it compares against was itself diluted.
This record makes that re-tune a **decision** rather than a **discovery**.

---

## The ESPN archive degrades — capture and diff before overwriting

2023 week 1 was **partially fetchable in December 2025** (85 projections in the `adc0f749` compile)
and today returns **1,037 of 1,128 rows zeroed**. The archive is not a stable source that can be
re-read at will; it gets worse.

**Therefore: any future recompile or re-fetch must capture-and-diff before overwriting.** Fetch to a
side location, diff against the committed `simulation/sim_data/` tree, and only then decide whether
to overwrite. Skipping that step can silently replace a currently-good season with a worse snapshot,
recoverable only from git — and only if someone notices in time to look.

This is the single finding in this document with a real, immediate operational cost if it is lost.

---

## Note to the availability-durability spike

The delivery-track spike `availability-durability` computed its own coverage measurements over an
**ADP-based**
population — the same selection rule that produced this ticket's own **retracted** third claim
("2025 is uniformly sparse"), which was an artifact of the Defect B placeholder tie rather than a
real sparsity. Under the scale-free production-ranked rule, 2025 is in fact the **best** of the five
seasons.

**Those measurements must be re-derived scale-free before that spike's design question 1 is
answered.** This record states the note; **D8.1 does not edit the spike** — re-deriving belongs to
the spike itself.

(That spike lives at `.shamt-core/spikes/availability-durability.md`, inside the **local,
git-ignored** Shamt work tree, so it is not resolvable from a fresh clone. The note is recorded here
precisely because the tracked record outlives it.)

---

## Defect B — mechanism and evidence, with its repair deferred

Recorded here for completeness because it shares the same root surface. **Its repair is deferred; its
diagnosis is not.**

**Mechanism.** `historical_data_compiler/player_data_fetcher.py:339-342` copies
`ownership.averageDraftPosition` **verbatim** — nothing normalises it. Seasons 2021–2024 sit on
ESPN's compressed ≤170 rank-like scale, where `170.0` is the undrafted cap. 2025 does not:

| season | ADP <170 | ==170 | >170 | max ADP |
|---|--:|--:|--:|--:|
| 2021 | 693 | 105 | 66 | 170.6 |
| 2022 | 718 | 60 | 12 | 170.2 |
| 2023 | 582 | 68 | 147 | 170.6 |
| 2024 | 715 | 51 | 8 | 170.1 |
| **2025** | **165** | **120** | **485** | **880.0** |

In 2025 the `170.0` value is a **missing-value placeholder sitting ahead of 485 genuinely drafted
players** in the 171–880 range. Provenance is in git — commit `4f274f97`: *"2025 ADP restored from
commit `e66fb589` … ESPN's kona view returns 170.0 placeholder for the 2025 season (known issue)"* —
so 2025 mixes restored real ADPs with un-restored placeholders.

**Consumer.** The **win-rate** simulator's opponents draft by ADP ascending with a `999.0` null
fallback (`simulation/win_rate/SimulatedOpponent.py:189`, `:202`), so over 2025 data the 120
placeholder players draft **ahead of** 485 real ones.

**It contaminates a different engine from Defect A, and that is why the two decompose cleanly.** The
accuracy simulation passes `adp=False` (`simulation/accuracy/ParallelAccuracyRunner.py:129`) and
never reads ADP at all. Defect A poisons the accuracy engine's objective; Defect B distorts the
win-rate engine's draft order. Neither touches the other's input.

**Repairable in place, and deferred anyway.** The real 2025 values exist at `e66fb589`, so the repair
needs **no re-fetch**. It is nonetheless **out of scope for D8** and belongs to a named follow-up —
*"Normalize the 2025 ADP scale in `sim_data`, sequenced with D3"* — because it is a `sim_data`
**content** change, as is D3's resolution, and keeping every mutation of the shared corpus behind one
carrier is both cheaper and safer than scattering them. **D8 changes no ADP value.**

---

## What D8 ships instead

D8 repairs neither defect. It ships **detection and containment**, so that the next corrupt
season-week is loud instead of silent:

- **D8.2 — measurement, reporting only.** A per-week and per-season coverage computation over the
  scale-free production-ranked population, bye-excluded, added to `validate_sim_data.py`. Present and
  idle: its result is not folded into the pass/fail outcome, so behaviour is unchanged.
- **D8.3 — enforcement.** Flips that check to failing, with thresholds calibrated against D8.2's
  recorded five-season output. Reversible by flipping back.
- **D8.4 — containment.** An opt-in flag on the accuracy harness that skips any season-week below the
  per-week floor, every exclusion logged, the floor read from the same single owner D8.2 creates.

Detection and containment are separable from repair, which is why D8 ships them and leaves repair to
its named carriers. This record is the reason a later reader can tell the difference between "not yet
fixed" and "cannot be fixed".

---

*Transcribed from delivery ticket D8's validated `ticket.md` and `context.md` (both `Validated`-footed
2026-08-05). Document-only — no fetch, no simulation run, no code or test change, no `sim_data`,
config or promotion write. Authored by unit D8.1.*
