# Accuracy Simulation Seed-Sensitivity — One-Seed Smoke Verdict (D2)

**Status: PARTIAL — ONE-SEED SMOKE RUN ONLY.** This document does not establish seed-to-seed
sensitivity (Success Criteria 2/3 of `D2`'s ticket record remain unmeasured) and issues no
trustworthiness verdict on using accuracy-sim output as a validation gate (Success Criterion 7,
partial). It proves the seed-sweep harness end-to-end on one seed and reports every figure that
IS computable from a single run. The full five-seed sweep is deferred to a follow-up delivery
ticket — see "Follow-up" below.

**Ticket:** D2 (`accuracy-sim-noise-floor-unmeasured`), unit D2.3
(`seed-sweep-harness-and-verdict`). This unit's design gate amended the ticket's `TD6` and Success
Criteria 2/3/7 to a one-seed smoke run by explicit user decision (2026-08-06); see the unit's own
`spec.md` §Ticket Summary for the full resolution record — that record lives under
`.shamt-core/tickets/D2-accuracy-sim-noise-floor-unmeasured/`, which is git-ignored and not
resolvable from this repository; it is named here for provenance only, per the same convention
`docs/simulation/SIM_DATA_COVERAGE_DIAGNOSIS_D8.md` uses.

---

## TL;DR

- The seed-sweep harness (`run_accuracy_seed_sweep.py`) works end-to-end: it ran seed 42 against
  the pinned `data/configs/` baseline, produced a completed `accuracy_optimal_*` folder, and
  emitted the raw-sample JSON.
- **Seed-to-seed sensitivity is NOT measured.** One sample cannot produce a spread. That question
  is open until the follow-up ticket runs the remaining four seeds.
- The **within-run, between-candidate** spread of `pairwise_accuracy` — a different population,
  never to be read as a seed-to-seed figure — IS measured, per horizon: see "Between-candidate
  spread" below.
- The **exact-tie rate** and **per-season-gate rejection rate** ARE measured from this one run's
  `candidate_results.json`: see "Tie-break and gate characterisation" below.
- **No trustworthiness verdict follows.** A judgment on whether accuracy-sim output is safe to use
  as a validation gate requires the seed-to-seed comparison this run cannot provide.

---

## Reproducibility

| Field | Value |
|---|---|
| Commit | `2d87b789c17757315914293c46c7a274708cef39` |
| Baseline | `data/configs/` (pinned, `TD3`/`TD4` of `spec.md`) |
| `sim_data` coverage arm | default (every season-week evaluated) — `--exclude-low-coverage-weeks` is available (D8.4 merged as `7f836965`, an ancestor of this base) but was deliberately not passed: the flag is opt-in (`action='store_true', default=False`), and running both arms would double a ~67 min measurement on a unit the user narrowed to one seed. The excluded-weeks arm was available and deliberately not run; the follow-up ticket inherits the arm choice as an open degree of freedom. |
| Seeds run | `42` (1 of the eventual 5; `--seeds 42`) |
| Invocation | `python run_accuracy_seed_sweep.py --seeds 42` |
| Worker / process flags | default (`--max-workers 8`, `--use-processes`) — not overridden |
| Output folder | `_internal/data/accuracy_seed_sweep_D2/seed_42/accuracy_optimal_2026-08-06_12-48-23` |

`N = 1` yields no dispersion at all — this table exists so the run can be repeated (after any
engine or `sim_data` change) rather than because five points would ever have been in reach here.
The run reached CONVERGED after 3 passes over 7,744 evaluated configs, in ~67 minutes wall clock
(the plan's ~40 min estimate, sourced from D11's per-ascent figure, proved low for this run — this
is the observed figure, not the estimate).

---

## Between-candidate spread (within the single seed-42 run)

**Population: every candidate `run_accuracy_seed_sweep.py --seeds 42` evaluated for that horizon,
in this one run** (from `candidate_results.json`, D2.2's artifact). **Convention:** min/max/spread
of `pairwise_accuracy` (`CODING_STANDARDS.md` §"Measurement and Comparison Conventions"). **This is
NOT a seed-to-seed population** — it says nothing about what a different seed's search would find.

| Horizon | n candidates | min | max | spread |
|---|---|---|---|---|
| `week_1_5` | 2112 | 0.5913 | 0.6102 | 0.0189 |
| `week_6_9` | 1408 | 0.6058 | 0.6327 | 0.0269 |
| `week_10_13` | 2112 | 0.5975 | 0.6250 | 0.0274 |
| `week_14_17` | 2112 | 0.6112 | 0.6383 | 0.0271 |

**The promoted config's value per horizon — a single data point, never a spread:**

| Horizon | Promoted `pairwise_accuracy` |
|---|---|
| `week_1_5` | 0.610131089536813 |
| `week_6_9` | 0.6326991702158308 |
| `week_10_13` | 0.6249918381927317 |
| `week_14_17` | 0.6383062679824812 |

Note the promoted value is **not** always the maximum candidate value: promotion applies a
per-season consistency gate (`is_better_than`) before adopting a higher-mean challenger, so it is
not a pure argmax — e.g. `week_1_5` promoted `0.610131089536813` vs the max candidate
`0.6102` shown above (the two differ at higher precision than the table's 4-decimal rounding
shows).

---

## Tie-break and gate characterisation (SC4, SC6)

**Population: every "comparable" candidate — a candidate with a non-null `incumbent_pairwise`
(i.e. not the first-ever candidate for its horizon) — from the seed-42 run's
`candidate_results.json`.** Total candidates: 7744. Comparable candidates: 7740.

- **Exact-tie rate** (`pairwise_accuracy == incumbent_pairwise`): 515 of
  comparable candidates (6.7%). Each exact tie is decided by worker arrival
  order (`ParallelAccuracyRunner`'s `as_completed`, non-deterministic), not by the objective —
  `context.md` §Notes source 2.
- **Per-season-gate rejection rate** (`pairwise_accuracy > incumbent_pairwise ∧ ¬adopted`):
  16 of comparable candidates (0.2%). Each such rejection is
  a case where the per-season consistency gate (`is_better_than`, `AccuracyResultsManager.py`)
  rejected a higher-mean challenger — the selection rule is not a pure argmax of the mean.

---

## Decision rule (stated, not applied)

The rule inherited from the win-rate precedent
(`_internal/win_rate_similarity_investigation.md`, local-provenance citation only — git-ignored,
not repo-resolvable): *the harness cannot distinguish its own candidates on a horizon whose
seed-to-seed spread is ≥ the between-candidate spread on that horizon* — the same condition that
disqualified the win-rate sweep (0.031 ≥ 0.023).

**This rule is stated here but NOT applied.** There is no seed-to-seed spread from one sample to
compare against the between-candidate spread above. The follow-up ticket applies this rule
unchanged, per horizon, once the remaining four seeds are run.

---

## What this verdict does NOT establish

- **Seed-to-seed sensitivity (SC2/SC3): unmeasured.** One seed cannot produce a spread across
  seeds. Whether the promoted config's objective is stable or highly seed-dependent is unknown.
- **No trustworthiness verdict (SC7, partial).** Whether accuracy-sim output may be used as a
  validation gate for scoring changes — and under what conditions — cannot be judged from a single
  sample. This document makes no such claim.
- **No ε / minimum-resolvable-effect-size figure.** That is `D11`'s, per `TD10`. The
  between-candidate spread reported above is a comparator, never an effect-size bound.
- **Corpus-conditional.** This run's `sim_data` corpus carries D3's phantom-bye-week error
  (unresolved as of this run — see `context.md` §Notes). Re-measurement after D3 lands may be
  owed; recorded as a recommendation to the follow-up ticket, not performed here.

---

## Follow-up

The remaining four seeds, the seed-to-seed spread per horizon, the applied decision rule, and the
full trustworthiness verdict are deferred to a **follow-up delivery ticket**
(pending — to be filed). That ticket runs
`python run_accuracy_seed_sweep.py --seeds 42,<4 more>` against this same harness, unchanged
(`--seeds` accepts any count, `TD3`/`context.md` Key Design Decision D3) — no code change is
required to run the full sweep, only the invocation.

**Recommendation to that ticket (not performed here):** re-run after `D3` lands if the corpus has
changed by then; record which `sim_data` coverage arm (default vs `--exclude-low-coverage-weeks`,
if `D8.4` has merged) each of its five runs used.
