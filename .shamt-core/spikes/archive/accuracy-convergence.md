# Spike: Converting the Accuracy Simulation from an Endless Loop to a Convergence Stop

> **Delivery-track spike doc** (`/d-spike accuracy-convergence`). Transient, unnumbered, no status machine.
> Lives at `.shamt-core/spikes/accuracy-convergence.md`; archives to `.shamt-core/spikes/archive/accuracy-convergence.md`
> once it has emitted its tickets — that archive is git-tracked and is the durable record of
> **why** the work was split the way it was. Converted from `_internal/` on 2026-08-05.

> Status: **Realigned post-merge and at decomposition (2026-08-05).** The conversion this spike set
> out to evaluate **began landing while the spike was running** (T69 Stages A and B, `3373db4d` +
> `afbc809e`, plus an in-flight pass-loop rewrite) and has since **merged to `main` as `32a00a54`**
> ("T69: convergent, self-terminating accuracy-sim optimization", PR #81). This document is
> therefore no longer a proposal for unstarted work: it is (a) the measured **before** state, which
> nothing else records, (b) a review input for the change that landed, and (c) the record of which
> of its own recommendations survived that change. **§Re-verified at HEAD is the authoritative
> post-merge reading** — it supersedes any pre-merge claim in the body, including in
> §What landed mid-spike, which was written against the branch tip `598c5c6a` and is now one
> recommendation out of date. No project code changed **by this spike**.
>
> Started 2026-08-04. Measurements were taken against the accuracy path as it stood at `6aecf7c0`,
> which was byte-identical to `da40b29a` (`git diff --name-only da40b29a..6aecf7c0` → four
> `win_rate` paths only), so no measurement straddles a change to the code it measures. **Citation
> convention:** every line citation is qualified by the commit it is against — `6aecf7c0` for the
> pre-T69 engine the measurements describe, `598c5c6a` (branch
> `feature/T69-accuracy-sim-convergence-coordinate-ascent-like-win-rate/MizunoPK`, the T69 tip at
> time of writing) for the landed conversion; unqualified citations are to files T69 did not touch.
> Data: `simulation/sim_data/`, `data/configs/` and
> `simulation/simulation_configs/accuracy_optimal_2026-07-24_07-01-27/` as committed.
>
> Trigger (state at `6aecf7c0`): `run_accuracy_simulation.py` ended in `while True: main()` — the
> tournament restarted forever, and the documented operating procedure was "Stop (Ctrl+C) when
> pairwise accuracy plateaus" (`docs/simulation/ACCURACY_SIMULATION_FLOW_VERIFIED.md:1539`, **still
> uncorrected**). The win-rate sweep already had the shape we wanted: loop parameter passes until a
> full pass changes nothing, then stop (`SweepTournament.run`,
> `simulation/win_rate/SweepTournament.py:365-403`).
>
> Purpose: work out what a convergence stop would actually mean for the accuracy engine, whether
> the current engine even supports one, and what has to change alongside it. This document decides
> nothing.
>
> Measurements: one offline probe of candidate generation (`probe_candidates.py`, scratch,
> uncommitted) plus two real runs of the **unmodified** sim against the committed `sim_data/`
> (`--max-workers 14`, scratch `--output`): one from the shipped config (§3a) and one from a
> constructed neutral baseline, run to convergence (§3b). **No project code was modified for any
> measurement.**

---

## TL;DR

**Yes — and it is a smaller change than it looks, because the engine is already a monotone ascent.
But a stopping rule alone would be a waste-elimination change, not an accuracy change, and the
reason why is the more important finding.**

*(Points 1–5 below are stated against the pre-T69 engine, which is what every measurement here
describes. Points 1, 3 and 4 are unaffected by what has since landed; point 2's "never detected" is
now fixed in code. §What landed mid-spike maps each one onto the current tree.)*

1. **The endless loop is not searching.** Candidate values are `[baseline] + 10 uniform-random
   draws` per parameter, drawn from a **seeded private RNG whose draw sequence does not depend on
   the baseline at all** (`ConfigGenerator._rng`, `ConfigGenerator.py:305, 520-532`). Measured: two
   generators with deliberately different baselines produce **byte-identical non-anchor candidate
   sets**. Every pass therefore re-tests the *same* 10 values per (parameter, horizon) — the last
   pass of an overnight run explores exactly what pass 1 explored.
2. **So convergence is already guaranteed, it is just never detected.** The evaluator is
   deterministic (nothing on the evaluation path draws randomness — §Evidence 2), adoption is
   strictly-better-only (`AccuracyConfigPerformance.is_better_than`,
   `AccuracyResultsManager.py:179-236`), and the incumbent is always candidate `test_0`. That is a
   monotone ascent over a **finite, fixed reachable set** (≤ 44 values per parameter per horizon).
   It must reach a fixed point in finitely many passes and then repeat identical work forever.
   **Measured twice.** (i) The config currently in `data/configs/` is already that fixed point — a
   full 19m35s / 2,816-evaluation pass over it changed **0 of 61 parameter values in every horizon**
   and returned bit-identical pairwise accuracy. (ii) From a deliberately neutral start the search
   **converged after 2 passes**, and pass 3 moved **0 of 63** values in every horizon. At ~20
   min/pass a weekend run is ~144 passes; ~142 of them do nothing.
3. **Detecting it is cheap.** The state is four JSON files; a pass-over-pass fixed-point test is a
   dict comparison. The win-rate engine's in-invocation form (`while moved:` over the parameter
   list) ports over almost directly, and the accuracy engine already writes a per-parameter
   checkpoint (`accuracy_intermediate_*` folders + `_detect_resume_state`) to build on — though not
   a pass-aware one, which is the fiddly part (§Blast radius).
4. **The catch: stopping at today's fixed point is honest, not better — and the fixed point is not
   unique.** Starting the same search from a neutral baseline converges on a *different* config that
   **beats the shipped one on 2 of 4 horizons** (§3b), so "converged" ≠ "optimal" even inside this
   search's own reachable set. The optimum is also capped by 10 arbitrary points per parameter.
   Adding a stop makes the tool tell the truth about when it quit learning; it does not raise the
   accuracy it reaches. If the goal is "loop until we stabilize
   at maximum accuracy", the stopping rule has to be paired with a **candidate-generation change**
   (a deterministic grid, or an anchor-local neighbourhood that shrinks each pass) — otherwise
   "stabilized" means "exhausted 10 arbitrary points", which is exactly where the shipped config
   already sits. Today the only levers that make a re-run explore anything new are `--seed` and
   `--test-values`; the loop itself is not one.
5. **There is a finished precedent for the whole job.** The archived epic
   `T1-win-rate-sim-overhaul-sweep-endless-modes` did exactly this conversion for the win-rate sweep
   (engine → resume → endless → report; 5 features / 7 stories, PRs #15–#19). Its Out-of-Scope list
   says "The accuracy simulation engine (`run_accuracy_simulation.py`) — untouched", and its
   In-Scope bullet on `--endless` carry-over already names the trap this spike measured: *"a
   deterministic restart-from-baseline endless loop would simply repeat identically"*
   (`epic.md:48`). That is a description of `run_accuracy_simulation.py` today.

Recommended path: **package P3 (§Options) — no-move convergence + an ε adoption gate + an
anchor-local shrinking candidate set**, with `--endless` kept as an opt-in (re-seeded per pass if
the reproducibility question allows — Q2/Q3). P1 (stop-only) is a legitimate cheap first step and is
strictly better than today, but it should be landed knowing it buys CPU, not accuracy.

---

## What landed mid-spike (T69)

Between this spike's first measurement and its validation pass, three commits on
`feature/T69-accuracy-sim-convergence-coordinate-ascent-like-win-rate/MizunoPK` implemented most of
§Options' P1+P2. This work was still moving while the spike was being validated — Stage C was
uncommitted when first read and committed minutes later — so the state below is the T69 tip
`598c5c6a` at time of writing, and later stages may add to it.

| Commit | What it does |
|---|---|
| `3373db4d` — T69 Stage A | Adds a **per-season consistency gate** to `is_better_than` (`AccuracyResultsManager.py:179-236`): a candidate must also beat the incumbent on ⌈0.8 × shared seasons⌉ individual seasons. Details + consequences in §3c. |
| `afbc809e` — T69 Stage B | **Deletes `while True: main()`.** `main()` now exits 0 on success / 1 on failure, and the comment states "There is deliberately no `--endless` opt-back-in." |
| `598c5c6a` — T69 Stage C | Moves the pass loop **inside** `AccuracySimulationManager`: `_run_ascent_pass` (`598c5c6a:508`) is an explicit port of `SweepTournament`'s `while moved:`; a horizon that adopts nothing in a full pass is **frozen** — skipped for candidate generation (`:556`) *and* for result recording (`:592`, "frozen -- its best is final for this run"); the run stops when every horizon has frozen, or at `MAX_ASCENT_PASSES = 10` (`:61`), reported as a distinct **BOUND-HIT ≠ CONVERGED** disposition. |

So of this spike's four packages, as of `598c5c6a`: **P1 and P2 are substantially done** (stopping
rule, in-manager pass loop, real exit code, pass bound, terminal dispositions), **P4 is decided
against** (no `--endless`), and **P3 is untouched** — candidate generation is still the frozen 10
uniform draws of §Evidence 1.

**What this spike still contributes, given that:**

1. **The only measured before/after baseline.** §Evidence 3 is the one record of what the endless
   loop actually did — converged in 2 passes and then repeated null passes forever. It is the
   evidence that the change was worth making and the yardstick for whether the new engine reproduces
   the same optimum.
2. **Three things the landed work does not do**, each still open:
   - **No magnitude gate.** Grepping `simulation/accuracy/` at `598c5c6a` finds no ε /
     minimum-improvement constant. Stage A gates on *consistency* (is the win broad-based across seasons), not
     *magnitude* (is it big enough to be worth changing a shipped value). A broad-based 2e-6
     improvement is still adopted, so the churn described in §What "no real change" should mean
     survives. §3b bounds the ε that would close it at ≈1e-4.
   - **Per-horizon freezing has a cost the joint rule does not.** Stage C freezes each horizon
     independently. That is *sound* — freezing blocks recording as well as
     generation, so a frozen horizon's best cannot be displaced by a stale donation, which is the
     failure mode §The horizon tournament complicates the "state" warned about. But it is not
     free: because any horizon can adopt a config donated from another horizon's baseline, a
     horizon frozen at pass *k* forgoes donations that later passes would have offered it. Joint
     stopping ("stop when no horizon moved") and per-horizon freezing can therefore end at
     different configs. Which is better is an empirical question this spike did not run, and §3b's
     harness answers it cheaply: re-run the neutral experiment under both rules and `--compare`.
   - **The documentation is now wrong.** `docs/simulation/ACCURACY_SIMULATION_FLOW_VERIFIED.md`
     still presents the infinite loop as a headline feature in at least six places (re-counted at
     HEAD as **8** — §Re-verified at HEAD governs)
     (`:202, 274, 286, 294, 1160, 1539-1556`), including a "Typical Use Cases" workflow whose step
     4 is "Stop (Ctrl+C) when pairwise accuracy plateaus". Its last commit is `8370b2e2`, which
     predates all three T69 stages.
3. **A re-measurement worth having.** Every number in §Evidence 3 was produced by the pre-T69
   engine. Re-running §3b under the new engine answers, in one command, whether the consistency
   gate + per-horizon freezing reach the same fixed point the old joint search did.

---

## Re-verified at HEAD (2026-08-05) — the realignment

§What landed mid-spike was written against the **branch tip `598c5c6a`**. T69 has since merged as
`32a00a54`, and it **kept moving between that tip and the merge**. Every residual below was
re-checked against the merged tree; this section, not the pre-merge prose above, is what the
decomposition rests on.

| Residual (as the spike left it) | State at `32a00a54` | Evidence |
|---|---|---|
| **1. Re-measure §3b under the new engine** | **Still open** | No recorded re-run exists. Every figure in §Evidence 3 is still pre-T69. |
| **2. Add the ε magnitude gate** | **Still open — gate absent** | A grep of `simulation/accuracy/` for `EPSILON` / `MIN_IMPROVEMENT` / `min_effect` / `MIN_DELTA` returns nothing. Stage A's gate is *consistency* (`_min_season_wins`), not magnitude. |
| **3. Joint-stop vs per-horizon freeze** | **Still open — empirical, unrun** | Per-horizon freezing is implemented (`frozen_horizons`, `AccuracySimulationManager.py:445-484`). Which rule reaches the better fixed point was never measured. |
| **4. Fix the documentation** | **Still open — now provably wrong** | `docs/simulation/ACCURACY_SIMULATION_FLOW_VERIFIED.md` still teaches the loop in **8** places (`:202` `while True: # CRITICAL: Never stops automatically`, `:274`, `:286`, `:294`, `:368`, `:1160`, `:1539`, `:1552`). Its last commit is `8370b2e2` (T75), which predates all three T69 stages. |
| **5. Make resume pass-aware** | ❌ **RETIRED — this landed** | See below. |
| **6. P3 candidate generation** | **Still open — untouched** | `ConfigGenerator._generate_test_values_array` (`:520-532`) is still `[baseline] + N` draws from the private `self._rng`. §Evidence 1 stands unchanged. |

### Residual 5 is retired — pass-aware resume shipped

The spike recommended making resume pass-aware and recorded the gap as "parameter-index-only,
applies to pass 0 alone (`598c5c6a:531`)". **That is no longer true**, and the correction matters
because the spike called the resume state machine "the single most delicate piece of the conversion"
(§Blast radius) and flagged its failure mode as *silent* — a valid-looking optimal folder from a
truncated search. At `32a00a54`:

- `AccuracyResultsManager` writes **`_ascent_state.json`** into each intermediate folder (`:802`).
- `AccuracySimulationManager._read_ascent_state` (`:241-264`) reads back **`pass_idx`** and
  **`frozen_horizons`**, degrading to `(0, set())` on an absent or malformed file rather than
  raising — an explicitly-commented choice ("losing the pass/frozen detail is far better than
  discarding the run's work").
- `_detect_resume_state` returns the pass index and frozen set (`:362-383`), and `run_both` resumes
  from them, including the already-fully-frozen case (`:451-471`).
- Both paths are tested — valid state at `tests/simulation/test_AccuracySimulationManager.py:1071`,
  malformed at `:1099`; the artifact's existence at `tests/simulation/test_AccuracyResultsManager.py:657-661`.

So the residual list is **five items, not six**, and the one the spike rated most dangerous is gone.

### Two adjacent findings the spike recorded but never ticketed

Both sit on paths this work touches, and both were re-confirmed at HEAD:

- **`_sync_schedule_params` is dead code** (`AccuracyResultsManager.py:431-466`). It tests
  `'MATCHUP_SCORING' in synced` at the **top level** of the config dict, but a real config nests
  everything under `parameters` — verified: the committed optimal folder's `week1-5.json` has
  top-level keys `config_name`, `description`, `parameters`, `performance_metrics`, and
  `'MATCHUP_SCORING' in c` is `False`. The **caller two lines later proves it knows this**, reading
  through `synced_config.get('parameters', synced_config)` (`:546`, `:685`). So the mirror never
  fires. It is convenient for the convergence argument (saved == evaluated, exactly) and inert for
  Starter Helper, but **not** inert everywhere: the trade simulator scores with
  `schedule=True, matchup=False` (`trade_analyzer.py:343-352`), consuming `SCHEDULE_SCORING` values
  that nothing tunes and that the intended mirror never applies. A live no-op on the save path.
- **`find_baseline_config` scans a hardcoded path.** `run_accuracy_simulation.py:187` resolves the
  baseline by scanning `Path("simulation/simulation_configs")` (`:200`) rather than `--output`,
  even though that string is only the *default* (`DEFAULT_OUTPUT`, `:64`). Compounding it, this is
  the **deliberate-baseline trap** that `spikes/archive/draft-risk-scoring.md` left deliberately
  **unowned** when its gate dropped ticket 7: the default baseline is the most recent
  `accuracy_optimal_*` folder, i.e. values fitted to whatever chain produced them.

---

## The two engines, side by side

| | `run_accuracy_simulation.py` (**at `6aecf7c0`, pre-T69**) | `run_win_rate_simulation.py --sweep` (post-T1) |
|---|---|---|
| Objective | pairwise ranking accuracy (MAE diagnostic) | win rate in simulated leagues |
| Evaluator | **deterministic** — same config, same data, same number | **stochastic** — Monte-Carlo leagues |
| Candidate values | `[anchor] + 10 uniform randoms over the full range, seed-frozen` | fixed discrete grid over `[min,max]` at the param's precision + anchor (`param_value_generation.py`) |
| Inner loop | one pass over 16 params, each param optimized once | `while moved:` over 6 params, repeated to convergence (`SweepTournament.py:365-403`) |
| Adoption rule | strict `>` on pairwise accuracy — any improvement, however tiny, is adopted | one-sided z-test vs the 0.50 null **AND** a min-effect-size floor (`_adopt_by_significance`) |
| Stopping rule | **none** — `while True: main()` (`6aecf7c0:493-494`), Ctrl+C | **convergence** — a full pass that moves no parameter; `--endless` is opt-in on top |
| Resume | `accuracy_intermediate_{idx}_{param}/` folders + `_detect_resume_state` (`6aecf7c0:228-322`) | per-config convergence map in the sweep store + input fingerprint (`--fresh`) |
| Terminal states | n/a | `converged` / `in_progress` / `starved` |
| Exit code | never exits 0 | 0 on convergence |

(Rows 4–8 of the accuracy column are what T69 changed — see §What landed mid-spike. The candidate-
values row is not: that is still true today.)

The important asymmetry: **win-rate needed a statistical gate because its evaluator is noisy;
accuracy does not.** Everything the significance gate is defending against (adopting a candidate
that is not really better) reduces, in a deterministic engine, to a single scalar question — *how
much pairwise improvement is worth changing a config value for?* That is the ε in §What "no real
change" should mean.

---

## Evidence 1 — the candidate set is frozen, and independent of the baseline

`ConfigGenerator._generate_test_values_array` (`ConfigGenerator.py:520-532`) returns
`[baseline] + N` draws from `self._rng` over the parameter's full `[min, max]`. `self._rng` is
`random.Random(seed)` with `seed` defaulting to `DEFAULT_ACCURACY_SEED = 42` (`:305`, `:61`), and
the draw sequence depends only on the order of `generate_horizon_test_values` calls — i.e. on
`PARAMETER_ORDER` and `--test-values`, never on the config being refined.

Probe (`probe_candidates.py`): build a `ConfigGenerator` from the committed optimal folder; build a
second one from the same folder with every horizon baseline deliberately perturbed; build a third
from `data/configs`. Generate all 16 parameters' candidate arrays from each.

| Comparison | Non-anchor draws identical? |
|---|---|
| optimal folder vs. same folder with mutated baselines | **yes** |
| optimal folder vs. `data/configs` (a different config entirely) | **yes** |

Only element `[0]` — the anchor — ever differs. So the reachable value set for one parameter in one
horizon is **11 fixed values** (10 frozen draws + whatever the incumbent happens to be), and across
the four horizons at most **44**, since a config generated from horizon A's baseline is evaluated
against all four horizons and can win any of them.

(All 16 parameters in `PARAMETER_ORDER` map to sections listed in `WEEK_SPECIFIC_PARAMS`
(`config_constants.py:19-28`), so `generate_horizon_test_values` always takes its four-horizon
branch and the `{'shared': …}` branch is unreachable from the CLI. A replacement generator still has
to decide what it does with that branch rather than inherit it by accident.)

Two consequences worth stating plainly:

- **The search cannot refine.** There is no mechanism by which a later pass looks *near* a good
  value. If the optimum for `MATCHUP_SCORING_WEIGHT` in weeks 1–5 is 2.20, the engine can only ever
  offer `{0.23, 0.32, 0.63, 2.01, 2.17, 2.32, 2.34, 2.99, 3.41, 3.84}` plus the incumbent — forever,
  on every pass, for the life of the seed.
- **The endless loop's later passes are not exploration.** They are a re-run of a search whose
  input set has not changed. The only thing that can differ between pass *k* and pass *k+1* is the
  anchor, and once the anchors stop moving the passes are literally identical work.

---

## Evidence 2 — why a convergence test is mathematically sound here

Four conditions hold, and together they make "a pass that changes nothing" a *terminal* state
rather than a coincidence:

1. **Determinism.** Nothing on the evaluation path draws randomness: no `random`/`shuffle`/clock
   call appears in `simulation/accuracy/*.py` (bar an orphan-temp-dir age check) or in
   `player_scoring.py` / `PlayerManager.py`, so the scoring call is a fixed function of (config,
   historical data). Confirmed end-to-end in §Evidence 3a: the committed config re-evaluated 11 days
   later, in a fresh process pool, returned **bit-identical** pairwise floats on all four horizons.
2. **The incumbent is always in the pool.** `test_0` of each horizon's array is that horizon's
   current baseline value, so the running best can never be worse than the config it started from.
3. **Strict improvement.** `is_better_than` ends in `self.pairwise > other.pairwise`
   (`AccuracyResultsManager.py:236`) — ties keep the incumbent, a stabilising policy: the engine
   will not thrash between two equal-scoring configs. As of `3373db4d` a per-season consistency
   gate sits in front of that comparison (§3c); it only ever *rejects*, so the ascent stays
   monotone in the mean and this condition holds a fortiori.
4. **Finite reachable set.** §Evidence 1.

Monotone ascent + finite set ⇒ a fixed point in finitely many passes. The guarantee also holds
*across* passes, not just within one, because the chain is closed: `run_both` reloads its four
horizon baselines from the newest-by-mtime `accuracy_optimal_*` folder in `--output`
(`6aecf7c0:368-381`; observed in the §Evidence 3b run log — pass 2 opens with
`Using latest optimal config as baseline: accuracy_optimal_2026-08-04_14-36-57`, pass 1's own
output), that winner re-enters as `test_0`, and the saved config
*is* the evaluated config — `save_optimal_configs` writes the winner's week-specific params straight
through (`AccuracyResultsManager.py:540-552`). (`find_baseline_config`,
`run_accuracy_simulation.py:187-233`, picks the same folder for the *base* half of the config when
`--baseline` is omitted — with the quirk that it scans a hardcoded `simulation/simulation_configs`
rather than `--output`. The base half holds none of the 16 tuned parameters, so it does not affect
the ascent, but any pass-loop rework inherits the quirk.)

**One caveat found while checking that "saved == evaluated" step:**
`_sync_schedule_params` (`AccuracyResultsManager.py:432-467`), which is supposed to mirror
`MATCHUP_SCORING` into `SCHEDULE_SCORING` before saving, tests `if 'MATCHUP_SCORING' in synced`
against the *whole* config dict — but the real config nests everything under `parameters`, so the
key is never present. Verified: the function returns its input unchanged on a realistic config
shape. It is **dead code today**. Convenient for the convergence argument (saved == evaluated, exactly),
and inert for Starter Helper — which passes `schedule=False`, exactly matching the accuracy sim's
own scoring flags (`StarterHelperModeManager.py:343-357` vs `ParallelAccuracyRunner.py:126-139`), so
the sim is a faithful mirror of the mode it tunes. It is **not** inert everywhere: the trade
simulator scores with `schedule=True, matchup=False` (`trade_analyzer.py:343-352`), so it consumes
`SCHEDULE_SCORING` values that the accuracy sim never tunes (`SCHEDULE_SCORING` is absent from
`PARAMETER_ORDER`) and that the intended mirror-from-`MATCHUP` never applies. Out of scope here, but
it is a live no-op sitting on the save path this work would touch, and it should be fixed or deleted
rather than left as a trap.

---

## Evidence 3 — what successive passes actually do (measured)

### 3a. The shipped config is already at the fixed point

Ran the **unmodified** sim against the committed baseline
(`accuracy_optimal_2026-07-24_07-01-27`, which is also byte-identical in `parameters` to the live
`data/configs/`), committed `sim_data/`, `--max-workers 14`. One pass = 16 parameters × 44 configs ×
4 horizons = **2,816 evaluations, 19m35s wall**.

| Horizon | Pairwise before | Pairwise after pass 1 | Leaf param values changed |
|---|--:|--:|--:|
| week1-5 | 0.6101003805527109 | 0.6101003805527109 | **0 / 61** |
| week6-9 | 0.6326991702158308 | 0.6326991702158308 | **0 / 61** |
| week10-13 | 0.6248874139560197 | 0.6248874139560197 | **0 / 61** |
| week14-17 | 0.6382644203594079 | 0.6382644203594079 | **0 / 60** |

Not "changed a little" — **nothing moved at all**, in any horizon, and the pairwise floats came back
*bit-identical* after a fresh 19-minute search in a new process. This is the strongest form of the
§Evidence 2 argument: the config currently in production is a fixed point of this search, so every
further pass of the endless loop is 2,816 evaluations that reproduce their own input. On this
hardware (16 cores, `--max-workers 14`) an overnight run is ~24 such passes and a weekend run ~145;
the figures in `ACCURACY_SIMULATION_FLOW_VERIFIED.md:1355-1360` (~15 min/pass, 32 and 192) are the
same statement on different hardware.

It also settles §Evidence 2 condition 1 empirically: the same config, re-evaluated 11 days later in
a different process, produced the identical `float` on all four horizons. **The accuracy sim has no
run-to-run noise** — which is the half of `draft_risk_scoring_spike.md`'s open noise-floor question
that can be answered without instrumentation.

### 3b. Convergence dynamics from a neutral baseline

Because 3a starts converged, it shows the fixed point but not the path to it. Second experiment:
build a **neutral baseline** — the committed config with all 16 tunable parameters set to their
`PARAM_DEFINITIONS` range midpoints in every horizon, everything else untouched — and run the
unmodified sim from there. (This doubles as a test of the mitigation `draft_risk_scoring_spike.md`
§"Consequence 2" recommends for post-change re-runs: start from a neutral config rather than
inheriting the stale optimum.)

**Pass 1** (same 2,816 evaluations, 18m52s wall):

| Horizon | Neutral start | After pass 1 | Shipped optimum | Gap to shipped | Leaf values changed |
|---|--:|--:|--:|--:|--:|
| week1-5 | 0.5990 | 0.609329 | 0.610100 | **−0.000771** | 10 / 63 |
| week6-9 | 0.6120 | 0.630964 | 0.632699 | **−0.001735** | 12 / 63 |
| week10-13 | 0.6080 | 0.624517 | 0.624887 | **−0.000370** | 11 / 63 |
| week14-17 | 0.6220 | 0.636730 | 0.638264 | **−0.001535** | 12 / 63 |

("Neutral start" is the first `New best` line of the run — the midpoint config's own score, logged
as a percentage to one decimal (59.9% → 0.5990). The leaf denominator is 63 rather than 3a's 61/60
because the neutral baseline carries all three `LOCATION_MODIFIERS` keys in every horizon, which the
shipped folder does not — see the partial-block observation in §The horizon tournament complicates
the "state".)

Four things fall out of this, and they matter more to the design than the pass count does:

- **One pass does essentially all the work.** From a deliberately naive start, a single pass closes
  to within **0.0004–0.0017** pairwise of the config that is the endpoint of the shipped search.
  The whole distance the optimizer travels is ~0.01–0.02 pairwise (1–2 points); the distance the
  *second and subsequent* passes can still travel is bounded by the sub-0.002 residual above.
- **That residual sets the scale for ε.** The improvements the search is fighting over at the end
  are O(1e-3) (pass 2 below: +0.0005 to +0.0021). An adoption gate at ε ≈ 1e-4 would keep every move
  that matters at this scale and reject the 1e-6 churn described in §What "no real change" should
  mean; ε ≈ 1e-3 would freeze the last pass entirely. This is the data Q1 asked for, and it argues
  for the low end.
- **The horizon rankings are stable across wildly different starting points** — weeks 14-17 scores
  highest and weeks 1-5 lowest, from both the shipped config and the midpoint config. The corpus,
  not the tuning, dominates the level; the tuning moves it by ~2%.
- **The tournament re-specialises the horizons on its own.** Setting all 16 parameters to midpoints
  makes the four horizon configs *identical* (verified); one pass makes all four pairwise-distinct
  again (verified). So the donation channel of §The horizon tournament complicates the "state" is a
  homogenisation pressure, not a homogenisation outcome — the per-horizon signal in the corpus is
  strong enough to pull them back apart.

**Passes 2 and 3** — the run was left going; here is the whole trajectory:

| Pass | Horizon | Pairwise | Δ vs prior pass | Leaf values moved | Wall |
|---|---|--:|--:|--:|---|
| 1 | week1-5 / 6-9 / 10-13 / 14-17 | .609329 / .630964 / .624517 / .636730 | +.0103 / +.0190 / +.0165 / +.0147 | 10 / 12 / 11 / 12 | 18m52s |
| 2 | week1-5 / 6-9 / 10-13 / 14-17 | .609848 / .633015 / .625836 / .637985 | **+.000519 / +.002051 / +.001319 / +.001255** | 3 / 4 / 6 / 6 | 18m56s |
| 3 | week1-5 / 6-9 / 10-13 / 14-17 | *identical* | **+0 / +0 / +0 / +0** | **0 / 0 / 0 / 0** | 22m32s |

**It converged after two productive passes.** Pass 3 is the no-change pass a convergence rule would
stop on — today's engine instead began pass 4, which is where the run was killed (the log shows a
fourth `Optimizing parameter 1/16`). Total useful work: **~38 minutes** out of an unbounded run. At
~20 min/pass a weekend run performs ~144 passes, **~142 of them null**.

The trajectory is the shape the design should assume: pass 1 does ~90% of the climb, pass 2 does the
remaining ~10% at O(1e-3), pass 3 does nothing. A stopping rule catches this at pass 3; an ε gate at
1e-4 would not have changed the outcome here (every pass-2 move exceeded it), while an ε at 1e-3
would have discarded most of pass 2.

**And the converged point is not the shipped one:**

| Horizon | Neutral run, converged | Shipped optimum | Δ |
|---|--:|--:|--:|
| week1-5 | 0.609848 | 0.610100 | −0.000252 |
| week6-9 | **0.633015** | 0.632699 | **+0.000316** |
| week10-13 | **0.625836** | 0.624887 | **+0.000949** |
| week14-17 | 0.637985 | 0.638264 | −0.000280 |

Two different fixed points, same frozen candidate set, same data, same seed — differing only in
where the ascent started. **"Converged" therefore does not mean "optimal"**, even within this
search's own tiny reachable set: coordinate ascent over a non-separable objective is path-dependent,
and the shipped config is one arbitrary local optimum among several. That is an argument *for* a
stopping rule (you cannot compare fixed points you never reach) and *against* reading one as an
answer.

### 3c. Caveat — the adoption rule changed under this spike

Commit `3373db4d` ("T69 Stage A: per-season consistency adoption gate") landed while §3b was
running. It adds a second condition to `is_better_than`
(`AccuracyResultsManager.py:179-236`, with `_min_season_wins` at `:41-58`): a candidate must now
also beat the incumbent on **⌈0.8 × shared seasons⌉** of the individual seasons, degrading to the
old mean-only comparison when fewer than 2 shared seasons carry a per-season vector.

Every measurement above was produced by the **pre-T69** engine (the process loaded its modules at
14:18, before the commit), so passes 1–3 are internally consistent and describe the engine as it
stood at `6aecf7c0`. Consequences for this spike, none of them fatal:

- **The convergence argument survives unchanged, a fortiori.** The gate only ever *rejects*
  adoptions, so the ascent is still monotone in the mean over the same finite set, and it can only
  converge in the same number of passes or fewer.
- **T69 and the ε question are orthogonal, and the spike's ε recommendation still stands.** T69's
  own comment is explicit that it "Guards against a difference driven by one or two idiosyncratic
  seasons -- NOT against sampling noise", and that the deterministic evaluator makes the win-rate
  z-test the wrong import — the same conclusion §The two engines, side by side reaches
  independently. A consistency gate answers *"is this improvement broad-based?"*; ε answers *"is it
  big enough to be worth changing a shipped value for?"* Neither substitutes for the other, and
  §3b's O(1e-3) endgame is the data for the second.
- **The §3b numbers should be re-measured under T69 before they are used to set ε** — some pass-2
  moves may have been single-season-driven and would now be rejected, which would shorten the
  trajectory further (strengthening the case for a stop, not weakening it).

---

## What "no real change" should mean

The user's phrasing — *loop until we are not seeing any real changes to the configuration values* —
has two defensible readings, and they behave differently:

**(a) State fixed point.** Stop when pass *k+1* produces the same four horizon configs as pass *k*.
No threshold to choose; trivially implementable (compare the four `week*.json` payloads); exactly
what the win-rate epic's success criterion says ("looping full parameter passes until an entire pass
leaves that config's selected ideal values unchanged").

**(b) Metric plateau.** Stop when the best pairwise accuracy stops improving by more than ε for K
consecutive passes. Needs two knobs, but tolerates a search that keeps offering new candidates.

They coincide only if adoption itself is ε-gated. Without a gate, a candidate that improves pairwise
accuracy by 2e-6 — far below any meaningful resolution, given the metric is a mean over seasons of
per-week means across thousands of player pairs — is adopted, the config changes, and (a) never
fires even though nothing real happened. **So the ε belongs on the adoption decision, not only on
the stopping test**: adopt a candidate only when it beats the incumbent by more than ε, then "no
parameter moved" and "no real change" are the same statement, and (a) is sufficient.

This is the deterministic analogue of the win-rate engine's `DEFAULT_MIN_EFFECT_SIZE = 0.01` floor —
which exists for exactly this reason, AND-ed with its z-test because that engine also has noise.
§3b bounds accuracy's ε at ≈1e-4 (Q1).

Note the accuracy engine acquired *an* adoption gate during this spike (T69, §3c), but a
**consistency** one — the candidate must win a supermajority of seasons — not a **magnitude** one.
It rejects a 2e-6 improvement only when that improvement is also season-lopsided; a broad-based 2e-6
still passes and still changes the config. So it narrows the churn problem without closing it, and
the ε argument above is unaffected.

---

## The horizon tournament complicates the "state"

The accuracy engine is not four independent optimizations. Each candidate config is built from one
horizon's baseline and then **evaluated against all four horizons** (`run_both`,
`6aecf7c0:384-459`; the same fan-out survives Stage C's rewrite at `598c5c6a:582-600`), and any
horizon can adopt it. When it does,
`update_baseline_for_horizon` (`ConfigGenerator.py:404-448`) copies **every** differing
week-specific section from the winner into that horizon's baseline — not just the parameter under
test.

Consequences for a convergence design:

- **A "move" is not one value.** One parameter's step can rewrite several sections of a horizon's
  config at once (whatever the donor horizon happened to carry). A no-move test must compare the
  whole horizon config, not the parameter currently being optimized.
- **Convergence is joint, not per-horizon.** A horizon that looks settled can still be displaced by
  a config donated from a horizon that is still moving. So the win-rate trick of marking individual
  configs `converged` and skipping them does **not** port safely; the stopping rule should be
  "no horizon changed this pass". (Per-horizon skipping is still available as a *cost* optimization
  if the donation channel is closed first — see Q4.)
- **It is also a homogenisation pressure**, and worth watching during any change here: the four
  horizon files exist to specialise by season phase, and the donation channel pushes them toward
  each other. They have not collapsed — in the committed optimal folder all four files are still
  distinct, differing somewhere among `MATCHUP_SCORING`, `TEMPERATURE_SCORING`, `WIND_SCORING`,
  `LOCATION_MODIFIERS`, `PERFORMANCE_SCORING`, `TEAM_QUALITY_SCORING` and
  `NORMALIZATION_MAX_SCALE` (only `SCHEDULE_SCORING`, which nothing tunes, is identical across all
  four) — but nothing in the engine prevents it.

Adjacent observation, not chased: in that same committed folder the `LOCATION_MODIFIERS` sections
are **partial** — `week1-5` has `AWAY`/`HOME` but no `INTERNATIONAL`, `week14-17` has only `HOME`.
`_extract_param_value` defaults a missing key to `0.0` (`ConfigGenerator.py:452-484`), so the sim
happily optimizes a key the config does not contain. Whether the live app tolerates a partial
`LOCATION_MODIFIERS` block is a separate question from this spike.

---

## Options

Four coherent packages. P1 ⊂ P2 ⊂ P3 are cumulative — each keeps the previous one's mechanism and
adds to it. P4 is a different axis: it changes what candidate *sampling* does rather than how the
loop stops, so it can pair with P1/P2 as an alternative to P3's generator, or sit on top of P3 as
the meaning of `--endless` (see the note after P4).

> **Status as of `afbc809e` + the in-flight change: P1 ✅ and P2 ✅ largely landed, P4 ❌ decided
> against (no `--endless`), P3 ⬜ untouched.** The descriptions are kept as written — they are what
> the options were assessed as, and P2's description still names the two pieces the landed work
> does *not* include (the ε adoption gate, and pass-aware resume). See §What landed mid-spike.

### P1 — Stop-only (cheapest, honest, no accuracy change)

Wrap the existing loop: after `save_optimal_configs()`, compare the new folder's four `week*.json`
parameter payloads with the previous pass's. Identical ⇒ log "converged after N passes" and exit 0.
Add `--endless` to restore today's behaviour for anyone who wants it.

- **Cost:** small — a comparison helper, a loop in `main()` (or better, move the loop *into* the
  manager so the `while True` at `6aecf7c0:493-494` disappears), a flag, docs, tests.
- **Buys:** the CPU currently burned re-deriving the same answer, a real exit code, and an end to
  "watch the console and Ctrl+C when it plateaus" as an operating procedure.
- **Does not buy:** any accuracy *by itself*. It stops at the first fixed point of a
  10-random-point search — though §3b shows which fixed point you land on depends on where you
  start, so a deliberate re-run from a neutral baseline can buy accuracy independently of the
  stopping rule.
- **Risk:** it will look like a regression ("it used to keep improving overnight") unless the
  release note says plainly that it did not.

### P2 — Convergent coordinate ascent (win-rate parity)

P1 plus: move the pass loop inside `AccuracySimulationManager.run_both` as `while moved:` over
`PARAMETER_ORDER`, tracking `moved` per horizon config, mirroring `SweepTournament.run`. Add the
ε adoption gate (§What "no real change" should mean). Extend the intermediate-folder checkpoint to
carry the pass number and a terminal disposition, so resume works across passes and not just within
one.

- **Cost:** medium — this is the T2/T4 shape from the archived win-rate epic. `_detect_resume_state`
  becomes pass-aware (today it only reasons about parameter index).
- **Buys:** a single invocation that runs to a defensible terminal state; a resumable long run;
  parity of vocabulary between the two sims.
- **Does not buy:** a better optimum than P1 from the same starting point, for the same reason.

### P3 — P2 + a candidate set that can actually refine (recommended)

Replace `[anchor] + N uniform randoms over the full range` with an **anchor-local neighbourhood that
shrinks on a no-move pass**: pass 1 tests anchor ± a coarse step across the range, and each pass
that moves nothing halves the step instead of stopping; convergence is declared when the step
reaches the parameter's own precision (`PARAM_DEFINITIONS`, already carries `(min, max, precision)`).

- **Cost:** medium-high — a new generator alongside the existing one (keep the random generator
  behind a flag for comparison runs), plus its own determinism tests. `test_config_generator.py` and
  `test_accuracy_determinism.py` both assert the current shape and will need work.
- **Buys:** the thing the endless loop was *supposed* to be doing. "Stabilized" becomes "no better
  value exists within one precision step", which is a claim worth making.
- **Note:** a plain deterministic grid (reusing the win-rate `generate_candidate_values` shape) is
  a legitimate cheaper variant — finite, complete, provably terminating, and it makes the two sims
  share one candidate-generation concept. Its cost is that resolution is fixed by the grid step: a
  *full* grid at the parameter's own precision is 401 values for `MATCHUP_SCORING_WEIGHT`
  (`[0.0, 4.0]` at 2dp) and 651 for `ADP_SCORING_WEIGHT`, far too many to evaluate at ~5s per
  config-horizon, so a coarse grid is what you would actually ship. The shrinking neighbourhood
  reaches precision-level resolution without paying for the whole grid, which is why it is the
  better fit here.

### P4 — Keep the random search, add patience

Keep uniform random draws but **re-seed per pass** (`seed = base_seed + pass_index`), so each pass
genuinely explores new points, and stop after K consecutive passes with no adoption above ε.

- **Cost:** small-medium.
- **Buys:** the endless loop's *intent* — an overnight run that keeps finding things — with a
  defensible stop. Closest to today's behaviour in spirit.
- **Costs you:** run-to-run reproducibility, which T51 deliberately introduced
  (`DEFAULT_ACCURACY_SEED`, `test_accuracy_determinism.py`). Any version of P4 has to say what it
  does to that guarantee — reproducible-given-(base_seed, pass_count) is probably the answer.
- **Weakest guarantee:** "K passes found nothing" is evidence, not proof, of a local optimum.

P3 and P4 are not exclusive: a shrinking-neighbourhood ascent with a random restart when the step
bottoms out is the standard combination, and it is what an `--endless` mode should probably do after
P3 lands.

---

## Blast radius

*(Written before T69; the first three bullets have since been largely actioned — see §What landed
mid-spike. Kept because it is still the map of what a P3 follow-up touches.)*

- **`run_accuracy_simulation.py`** — the `while True` (removed by `afbc809e`), plus new flags
  (`--endless`, an ε knob, possibly a candidate-mode knob) and their validation/mutual-exclusion
  rules (note `--promote`/`--compare` already have interaction rules at `:366-390`; win-rate
  forbids `--promote` with `--endless` for a reason that applies here too).
- **`AccuracySimulationManager.run_both`** — the pass loop, the `moved` bookkeeping, the terminal
  log line, and the return value (a converged-vs-stopped disposition, not just a path).
- **`_detect_resume_state` (`6aecf7c0:228-322`)** — it infers "where did we stop" purely from
  `accuracy_intermediate_{idx}_{param}` folder names, and treats *all params complete* as "start
  fresh". Under a multi-pass engine, "all params complete" means "start pass k+1", so this function's
  contract changes. It is the single most delicate piece of the conversion.
- **`ConfigGenerator`** — only under P3/P4.
- **`--promote`** — unchanged mechanically, but "promote the converged config" becomes a
  meaningful, defensible operation for the first time.
- **Tests** — `tests/simulation/test_AccuracySimulationManager.py` (956 lines),
  `tests/root_scripts/test_run_accuracy_simulation.py` (933),
  `tests/integration/test_accuracy_simulation_integration.py` (594),
  `tests/simulation/test_config_generator.py` (575), `test_accuracy_determinism.py`. The
  root-scripts suite asserts CLI surface; the integration suite drives the manager.
- **Docs** — `docs/simulation/ACCURACY_SIMULATION_FLOW_VERIFIED.md` describes the infinite loop as a
  headline feature in at least six places (`:202, 274, 286, 294, 1160, 1539-1556`) — re-counted at
  HEAD as **8** sites, §Re-verified at HEAD governing — including a
  "Typical Use Cases" section whose entire workflow is "stop when it plateaus". **Not yet updated —
  its last commit predates T69, so it is now wrong rather than merely stale.**
- **Operating habits** — because the runner never exited 0, any smoke of it had to run under
  `timeout` and accept exit 124. No such smoke exists in-repo (nothing under `tests/` invoked the
  runner that way), so this was always about ad-hoc and agent-driven checks rather than a suite that
  would break — but wherever the 124 convention is encoded by habit it now has to be unlearned,
  because `afbc809e` makes the runner exit 0 on success.

---

## Risks

1. **Stopping early looks like stopping worse.** P1/P2 terminate at exactly the optimum an
   overnight run would also have reached — measured: pass 3 of §3b is already null — but the
   perception is the opposite. Mitigation: report the pass count and the per-horizon pairwise at
   exit, and keep `--endless`.
2. **ε set too high silently freezes the search**; set too low, it never converges. §Evidence 3's
   deltas bound it from below; the metric's own resolution bounds it from above.
3. **The resume state machine is easy to get subtly wrong** (§Blast radius). A resume bug here is
   silent — it produces a valid-looking optimal folder from a truncated search.
4. **P3 changes the search, so it changes the answer** — but so does merely changing the starting
   point, which §3b already demonstrated (two fixed points, one better on 2 of 4 horizons, from
   identical inputs). So "the values moved" is not evidence either way, and only the pairwise
   numbers adjudicate. `--compare FOLDER_A FOLDER_B`
   (`run_accuracy_simulation.py:140-186`) already prints exactly the before/after table needed, and
   the pairwise numbers it reports are the right adjudicator.
5. **This spike's premise depends on the sim being able to discriminate configs at all** — the open
   question `spikes/draft-risk-scoring.md` §"The re-tuning workflow" raises (the win-rate
   sweep's noise floor exceeded its entire config spread). The determinism condition in §Evidence 2
   answers half of it — the accuracy sim has **no** run-to-run noise, so any measured difference is
   real — but "real" is not "meaningful": a 0.0001 pairwise difference is a reproducible artifact of
   the historical corpus, not evidence that one config predicts better. That is the same ε question
   from a different direction, and it is the reason ε should be chosen from data rather than picked.

---

## Open questions

1. **What is ε?** What pairwise-accuracy improvement is worth adopting a different parameter value
   for? §3b bounds it: the endgame moves are +0.0005 to +0.0021, so **ε ≈ 1e-4** keeps every move
   that mattered there and still rejects the 1e-6 churn; ε ≈ 1e-3 would discard most of pass 2.
   Confirm against a re-measured trajectory under T69 (§3c) before fixing the constant.
2. ~~**Does `--endless` survive, and what does it mean?**~~ **Answered by `afbc809e`: it does not
   exist** ("There is deliberately no `--endless` opt-back-in"). Re-opens only if P3 lands and a
   random restart at the step-floor is wanted.
3. **Is run-to-run reproducibility (T51) still a requirement** once a convergence stop exists? The
   two goals pull in opposite directions under P4.
4. **Should the cross-horizon donation channel stay?** It is what makes convergence joint rather
   than per-horizon, it is a homogenisation pressure on four files whose purpose is specialisation,
   and closing it would make per-horizon convergence marks (the win-rate pattern) safe. Closing it
   is a change to what the sim optimizes, so it is a separate decision — but a convergence design
   has to state which side of it the design assumes.
5. **What is the terminal disposition vocabulary?** Partly answered — the in-flight change has
   CONVERGED / BOUND-HIT, and per-horizon frozen. Still open: whether a resumed run needs a
   persisted disposition (today resume is parameter-index-only and applies to pass 0 alone,
   `598c5c6a:531`, so an interrupted multi-pass run restarts its ascent rather than resuming at
   pass *k*), and what P3's "stopped at the step floor" would be called.
6. ~~**Does a pass cap belong at all?**~~ **Answered by the in-flight change: yes** —
   `MAX_ASCENT_PASSES = 10`, reported as a BOUND-HIT disposition distinct from CONVERGED, which is
   the right shape (it cannot be mistaken for convergence). §3b's 3-pass trajectory says 10 is
   comfortable for a same-corpus run; a P3 shrinking generator would need it revisited, since
   step-halving deliberately spends passes.

---

## Artifacts

- Scratch, uncommitted, project code untouched: `probe_candidates.py` (offline candidate-generation
  comparison), `analyze_passes.py` (the pass-over-pass diff behind the §3 tables), and the neutral
  baseline builder (all 16 params → `PARAM_DEFINITIONS` midpoints, everything else copied from the
  shipped optimal folder).
- Run logs + optimal folders: scratch `--output` trees, `--max-workers 14`, data `simulation/sim_data/`
  as committed. §3a baseline `simulation/simulation_configs/accuracy_optimal_2026-07-24_07-01-27`
  (1 pass, 13:56–14:16); §3b baseline the neutral folder (3 passes, 14:18–15:18, converged at pass 3).
- Key code sites:
  - `run_accuracy_simulation.py:66` (`DEFAULT_TEST_VALUES = 10`), `:187-233`
    (`find_baseline_config`); `6aecf7c0:493-494` (`while True: main()`, deleted by `afbc809e`)
  - `simulation/shared/ConfigGenerator.py:61` (`DEFAULT_ACCURACY_SEED`), `:305` (private RNG),
    `:312-364` (`generate_horizon_test_values`), `:404-448` (`update_baseline_for_horizon`),
    `:520-532` (`_generate_test_values_array`)
  - `simulation/accuracy/AccuracySimulationManager.py` — pre-T69: `6aecf7c0:228-322`
    (`_detect_resume_state`), `6aecf7c0:326-491` (`run_both`); post-T69: `598c5c6a:61`
    (`MAX_ASCENT_PASSES`), `:508` (`_run_ascent_pass`), `:531` (the pass-0-only resume skip)
  - `simulation/accuracy/AccuracyResultsManager.py:179-236` (`is_better_than`, incl. the
    T69 season gate), `:432-467` (`_sync_schedule_params`, dead), `:469-617`
    (`save_optimal_configs`)
  - `simulation/accuracy/ParallelAccuracyRunner.py:95-175` (the scoring call under evaluation)
  - `simulation/win_rate/SweepTournament.py:48-88` (`_adopt_by_significance`), `:365-403` (the
    convergence loop), `simulation/win_rate/param_value_generation.py` (the deterministic grid)
  - `run_win_rate_simulation.py:285-500` (`--sweep` driver: fingerprint, resume, endless passes)
- Prior art: `.shamt-core/epics/archive/T1-win-rate-sim-overhaul-sweep-endless-modes/` — the same
  conversion, already delivered, on the other sim.
- Related spikes: `spikes/draft-risk-scoring.md` (§"The re-tuning workflow" — the accuracy
  sim's unmeasured noise floor), `_internal/win_rate_similarity_investigation.md` (the win-rate
  sweep's measured one).

---

## Recommendation

**The cheap half is already landing — so the useful recommendation is now about what it left
behind, and what this spike's evidence says about each piece.**

1. **Verify the landed engine reproduces the measured before-state.** Re-run §3b's neutral
   experiment under the new engine and `--compare` it to the pre-T69 result recorded here. This is
   ~40 minutes of wall time and it answers three questions at once: does the consistency gate change
   the fixed point, does per-horizon freezing change it, and does the new loop stop where the old
   one did (it should — pass 3 of §3b was already null).
2. **Add the magnitude gate (ε ≈ 1e-4).** Still absent. Stage A gates consistency, not size; without
   ε a broad-based 1e-6 improvement still rewrites a shipped config value. §3b's endgame (+0.0005 to
   +0.0021) is the data; confirm against the re-measured trajectory from step 1 before fixing the
   constant.
3. **Settle joint-stop vs per-horizon freeze on evidence, not preference** (Q4). Freezing is sound
   as implemented, but it forgoes cross-horizon donations that later passes would offer. The same
   harness as step 1 measures the difference.
4. **Fix the documentation.** `ACCURACY_SIMULATION_FLOW_VERIFIED.md` still teaches the infinite loop
   and "Ctrl+C when it plateaus" in **8** places (re-counted at HEAD — see §Re-verified at HEAD,
   which supersedes the "at least six" figure this section carried before the realignment; the
   earlier count was not wrong, it collapsed `:1539-1556` into one entry and missed `:368`). It is
   now actively wrong, and it is the
   first thing a future reader of this simulation will find.
5. ~~**Make resume pass-aware, or say it is not.**~~ **RETIRED (2026-08-05) — this landed between
   `598c5c6a` and the merge at `32a00a54`.** Resume now persists and restores `pass_idx` +
   `frozen_horizons` via `_ascent_state.json`, with both the valid and malformed paths tested. See
   §Re-verified at HEAD. The recommendation is struck rather than deleted so a reader who
   remembers it does not re-file it.
6. **P3 (candidate generation) remains the only item that can raise accuracy.** Everything above is
   correctness, honesty, and CPU. The search still offers 10 frozen random points per parameter and
   cannot refine near a good value; §Evidence 1 and §3b's two-different-fixed-points result are the
   argument, and §Options P3 is the shape.

### Candidate directions (declared touch-sets — the input the independence probe is bounded by)

| # | Direction | Rationale | Declared touch-set |
|---|---|---|---|
| A | **`accuracy-engine-convergence-remeasure`** | Every figure in §Evidence 3 is pre-T69. One ~40-minute neutral re-run under the merged engine answers three questions at once: does the consistency gate move the fixed point, does per-horizon freezing move it, and are the endgame deltas still O(1e-3) — which is the data that sets ε. | No production files. Scratch invocation + `--compare`; results recorded on the ticket. |
| B | **`accuracy-adoption-magnitude-gate`** | Stage A gates *consistency*, not *size*, so a broad-based 2e-6 improvement still rewrites a shipped config value. §3b bounds ε at ≈1e-4. Without it, "no parameter moved" and "no real change" are not the same statement. | `simulation/accuracy/AccuracyResultsManager.py`, `simulation/accuracy/AccuracySimulationManager.py`, `tests/simulation/test_AccuracyResultsManager.py`, `tests/simulation/test_AccuracySimulationManager.py` |
| C | **`accuracy-sim-flow-doc-currency`** | The doc teaches the infinite loop and "Ctrl+C when it plateaus" in 8 places against an engine that exits 0 on convergence. It is the first thing a future reader of this simulation finds, and it is now wrong rather than stale. | `docs/simulation/ACCURACY_SIMULATION_FLOW_VERIFIED.md` |
| D | **`accuracy-candidate-generation-refinement`** | P3 — the only residual that can raise accuracy. The search still offers 10 frozen random points per parameter and cannot look *near* a good value; §Evidence 1's two-different-fixed-points result is the argument. | `simulation/shared/ConfigGenerator.py`, `run_accuracy_simulation.py`, `tests/simulation/test_config_generator.py`, `tests/simulation/test_accuracy_determinism.py` |
| E | **`sync-schedule-params-dead-code`** | A live no-op on the save path this work touches, whose intended effect (mirror `MATCHUP` into `SCHEDULE`) never fires — while the trade simulator really does consume the un-mirrored `SCHEDULE_SCORING`. Fix or delete; do not leave as a trap. | `simulation/accuracy/AccuracyResultsManager.py`, `tests/simulation/test_AccuracyResultsManager.py` |
| F | **`accuracy-baseline-resolution`** | `find_baseline_config` scans a hardcoded `simulation/simulation_configs` rather than `--output`, and the default-to-most-recent-`accuracy_optimal_*` behaviour is the deliberate-baseline trap left **unowned** when spike 1's gate dropped its ticket 7. | `run_accuracy_simulation.py`, `tests/root_scripts/test_run_accuracy_simulation.py` |

**Boundary against `D2` (`accuracy-sim-noise-floor-unmeasured`) — decided (user, 2026-08-05).**
Direction A is filed separately, and `D2` is **flagged for re-scoping by its own flow**, not edited
from here. The reason is a finding of this spike: `D2`'s first success criterion — re-evaluate a
fixed config N times and report run-to-run variance — will measure **exactly zero**, because the
accuracy evaluator is deterministic (§Evidence 2 condition 1; confirmed end-to-end in §3a, where the
committed config re-evaluated 11 days later in a fresh process pool returned bit-identical pairwise
floats on all four horizons). That framing was imported from the *win-rate* sweep, which genuinely is
stochastic. `D2`'s **surviving substance** is its fourth criterion — the *minimum resolvable effect
size* — which is the ε question direction B applies and direction A measures. Recorded here so
`D2`'s `/dt3-design` inherits the finding instead of rediscovering it.

**The measurement that would settle whether P3 is worth its cost** is unchanged by any of this:
re-run the §3b neutral experiment under a shrinking-neighbourhood generator and `--compare`. If it
reaches pairwise accuracy the frozen-10 search cannot, P3 pays for itself. If it lands within ε of
the same answer, the current optimum is genuinely near-optimal for this parameterisation — a good
outcome, and one nobody can currently claim.

---
Validated 2026-08-04 — 8 rounds, 1 adversarial sub-agent confirmed (sha256:38149a782f6be22b) (spike; 4 adversarial dispatches, 3 with findings)

---

## Decomposition

**Proposed: 6 delivery tickets**, from §Candidate directions A–F. The set is larger than the sibling
`scoring-scale` spike's because these residuals are genuinely *separate* work rather than stages of
one rollout — which is the distinction the rubric turns on, not a preference for more tickets.

(The ticket numbers are **landing order**, so they deliberately do not follow the A–F letters of
§Candidate directions. The `Dir` column carries the mapping: 1=A, 2=E, 3=F, 4=B, 5=C, 6=D.)

| # | Dir | Ticket slug | Scope (one line) | Size |
|---|---|---|---|---|
| 1 | A | `accuracy-engine-convergence-remeasure` | Re-run §3b's neutral experiment under the merged T69 engine and `--compare` it to the pre-T69 record; answer joint-stop vs per-horizon freeze and produce the endgame deltas that set ε. | Medium |
| 2 | E | `sync-schedule-params-dead-code` | `_sync_schedule_params` never fires (tests a top-level key against a `parameters`-nested config). Fix or delete; the trade simulator really does consume the un-mirrored values. | Small |
| 3 | F | `accuracy-baseline-resolution` | `find_baseline_config` scans a hardcoded `simulation/simulation_configs` rather than `--output`; also gives the unowned deliberate-baseline trap an owner. | Small |
| 4 | B | `accuracy-adoption-magnitude-gate` | Add the ε magnitude gate (≈1e-4, confirmed by ticket 1) so a broad-based 2e-6 improvement stops rewriting shipped config values. | Medium |
| 5 | C | `accuracy-sim-flow-doc-currency` | Correct the 8 sites in `ACCURACY_SIMULATION_FLOW_VERIFIED.md` that still teach the infinite loop and "Ctrl+C when it plateaus". | Small-medium |
| 6 | D | `accuracy-candidate-generation-refinement` | P3 — replace the frozen 10 uniform draws with an anchor-local neighbourhood that shrinks on a no-move pass. The only residual that can raise accuracy. | Large |

**Landing order: 1 → 2 → 3 → 4 → 5, with 6 schedulable any time after BOTH 1 and 3.** Acyclic.

> The "after 3" half is not a preference — it is the 3 × 6 hop-1 collision below. Both edit
> `run_accuracy_simulation.py`, so 6 cannot start while 3 is in flight. An earlier draft of this
> line read "6 unordered (schedulable any time after 1)", which contradicted the resolution
> recorded two paragraphs down; corrected at validation.
Ticket 1 leads because it sets ticket 4's constant and settles the freeze question; 2 and 3 are
independent small fixes placed early because they are cheap and sit on paths 4 and 6 touch; 5 lands
after 4 so the doc describes the adoption rule as it will ship.

### Why 6 tickets does not violate the rollout rubric

Only **ticket 6** contains a staged rollout — a new generator landing alongside the existing random
one behind a comparison flag, then a cutover, then retirement of the old path. That rollout stays
**inside ticket 6** as its unit set, drawn at `/dt4-decompose`. Nothing else here is a stage of
anything: tickets 2 and 3 are unrelated defects on adjacent paths, 5 is a documentation correction,
1 is a measurement, and 4 is a single behavioural gate. Splitting *those* apart is what the rubric
asks for — it forbids splitting a rollout, not splitting independent work.

**One follow-on deliberately not filed:** if ticket 1 finds that per-horizon freezing reaches a
*worse* fixed point than joint stopping, changing the stopping rule is its own ticket. Its
precondition is ticket 1's result, which does not exist yet, so filing it now would emit a ticket
nothing in this set makes landable.

### Independence probe — all 15 pairs

Probed per `reference/project_separability_test.md`, bounded by the declared touch-sets in
§Candidate directions. **Ticket 1 declares no production files** (it is a measurement), so every
pair involving it is empty at both hops by construction — recorded explicitly rather than skipped,
since "no files" is a probe *result*, not an excuse to omit the pair.

| Pair | Outcome |
|---|---|
| 1 × 2 | `probed: independent` — ticket 1 declares no files; no symbol relationship |
| 1 × 3 | `probed: independent` — as above (see the invocation note below) |
| 1 × 4 | **`probed: coupled — data dependency, hop 2 n/a`** — ticket 1's measured endgame deltas *are* the value ticket 4 encodes |
| 1 × 5 | `probed: independent` |
| 1 × 6 | `probed: independent` — ticket 1's `--compare` harness is also how 6 is judged, but that is reuse, not coupling |
| 2 × 3 | `probed: independent` — `AccuracyResultsManager.py` vs `run_accuracy_simulation.py` |
| 2 × 4 | **`probed: coupled — shared file, hop 1`** — both touch `simulation/accuracy/AccuracyResultsManager.py` and `tests/simulation/test_AccuracyResultsManager.py` |
| 2 × 5 | `probed: independent` |
| 2 × 6 | `probed: independent` |
| 3 × 4 | `probed: independent` |
| 3 × 5 | `probed: independent` (content note below) |
| 3 × 6 | **`probed: coupled — shared file, hop 1`** — both touch `run_accuracy_simulation.py` |
| 4 × 5 | `probed: independent` (content note below) |
| 4 × 6 | `probed: independent` — adoption lives in `AccuracyResultsManager`, candidate generation in `ConfigGenerator`; neither references the other |
| 5 × 6 | `probed: independent` (content note below) |

**Three falsified premises, each resolved before the gate:**

1. **1 × 4 — dropped the independence claim, kept as an ordering dependency.** Ticket 4 cannot fix
   its constant without ticket 1's measurement; landing 4 first would encode an ε chosen from
   pre-T69 data. Encoded in the landing order. Not merged: the measurement and the gate are
   separately valuable, and 4 is re-runnable if the number later moves.
2. **2 × 4 and 3 × 6 — file-level collisions.** Each pair edits a different *function* in a shared
   file (`_sync_schedule_params` vs `is_better_than`; `find_baseline_config` vs the generator flag),
   so they are not the same work — but they cannot be built concurrently without conflict. Resolved
   by **sequencing**, which the landing order already encodes (2 before 4; 3 before 6). The
   independence claim is dropped for both pairs.
3. **Ticket 5's content dependency on 3, 4 and 6 — resolved by scoping, not by ordering.** The doc
   describes the engine, so *any* of those tickets changes what it should say. Rather than pin 5
   behind all of them (which would leave a provably-wrong document standing for as long as ticket 6
   takes), **ticket 5 is scoped to the engine as merged at `32a00a54`**, and tickets 3, 4 and 6 each
   carry their **own** documentation delta in their own scope. This is recorded so a later reader
   does not mistake the residual doc churn for ticket 5 having been done badly.

### Emitted (2026-08-05)

Gate outcome: all 6 approved **as proposed** — no member added, removed or re-scoped.

| Ticket | Dir | Slug |
|---|---|---|
| `D11` | A | `accuracy-engine-convergence-remeasure` |
| `D12` | E | `sync-schedule-params-dead-code` |
| `D13` | F | `accuracy-baseline-resolution` |
| `D14` | B | `accuracy-adoption-magnitude-gate` |
| `D15` | C | `accuracy-sim-flow-doc-currency` |
| `D16` | D | `accuracy-candidate-generation-refinement` |

Landing order: `D11` → `D12` → `D13` → `D14` → `D15`, with `D16` schedulable after **both** `D11`
and `D13`. All six back-link to `spikes/archive/accuracy-convergence.md`.

**Dependencies encoded in the emitted records:** `D11` → `D14` (data dependency — the ε value);
`D12` → `D14` (hop-1 file collision in `AccuracyResultsManager.py`); `D13` → `D16` (hop-1 file
collision in `run_accuracy_simulation.py`); `D11` → `D16` (the before-state to compare against).
`D15` is scoped to the engine **as merged at `32a00a54`**, with `D13`/`D14`/`D16` each carrying
their own doc delta.

**Recorded for `D2`'s design stage, not acted on here:** the accuracy evaluator is deterministic, so
`D2`'s run-to-run-variance criterion measures zero and its surviving substance is the minimum
resolvable effect size — the same ε question `D11` measures and `D14` encodes.

---
Validated 2026-08-05 — 3 rounds, 1 adversarial sub-agent confirmed (sha256:bd6bfb78af3608d4) (spike; post-T69 realignment + decomposition)
