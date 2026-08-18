# Ten-Mock-Draft A/B — LINEAR vs BUCKETED Multiplier Scaling (D10)

**The mock-draft A/B is a LOCAL-ONLY acceptance signal.** It is reproducible **only** on a checkout
that already has `_internal/mock_drafts/` present. It is **not** reproducible from a fresh clone,
**not** reproducible by another machine or another person, and **not** durable against the loss or
regeneration of that folder. Its recorded *result* is the durable artifact; its *input* is not.

That caveat is binding on every artifact that cites this run, and no text anywhere may describe this
A/B as durable, reproducible, or re-runnable elsewhere. Under D10.4's `U5` it gains one further hop:
the inputs are absent not only from a fresh clone but from the assignee lane itself, and were
hand-provisioned into it from the shared workspace root for this run.

**Ticket:** D10 (`continuous-multiplier-scaling`), unit D10.4 (`player-rating-linear-cutover`), which
is the last unit in the ticket by construction because this comparison needs BOTH factors switched.
The unit records live under `.shamt-core/tickets/D10-continuous-multiplier-scaling/`, which is
git-ignored and not resolvable from this repository; it is named here for provenance only, per the
same convention `docs/simulation/SIM_DATA_COVERAGE_DIAGNOSIS_D8.md` uses.

---

## What was compared

- **Arm A (baseline, "BUCKETED"):** `data/configs/league_config.json` as it stood before D10's
  cutovers — `ADP_SCORING` and `PLAYER_RATING_SCORING` both with no `SCALING` key, so both resolve
  to `BUCKETED` (D10's TD4: absent implies BUCKETED).
- **Both arms carry the SAME, UNCHANGED `WEIGHT` values.** Neither factor's `WEIGHT` was re-derived
  for this ticket: the accuracy engine's `PARAMETER_ORDER` does not include either
  `*_SCORING_WEIGHT`, so it cannot tune them, and the win-rate `DRAFT_SWEEP_PARAMS` owns them
  instead. The re-derivation is deferred to a follow-up unit. **Consequence for reading this A/B:**
  it isolates the scaling-model and window change cleanly (a good thing), but both arms run against
  weights fitted for the pre-cutover bucketed model — so it does not measure the fully re-tuned
  configuration, and no conclusion here may be stated as if it did.
- **Arm B (shipped, "LINEAR"):** both factors carrying `SCALING: "LINEAR"`, with
  `PLAYER_RATING_SCORING.THRESHOLDS.STEPS` at 25 (D10.4) and `ADP_SCORING`'s own re-derived window
  (D10.3).
- **Population:** the ten mock drafts in `_internal/mock_drafts/` (`mock_draft_slot01..10.json`),
  one per draft slot, replayed under each arm.
- **Convention:** rosters are compared pick-for-pick; a difference is counted at the pick where the
  two arms first select different players, and per-slot roster deltas are reported by player rather
  than by team name.

## Method — and one thing this run must NOT do

The A/B runs against the **real `_get_multiplier`** with `score_player()` driving the draft. It must
**never** run against the scoring-scale spike's prototype, whose equivalence to the real scorer holds
only at week 1 with an empty roster; from round 2 the roster is non-empty and the bye penalty becomes
live.

Nothing is committed and nothing is snapshotted (D10's TD7, option T3). The ten drafts stay in
git-ignored `_internal/`, and no league team name appears in this document.

## Result

PENDING /du4-test

## Per-slot roster deltas

PENDING /du4-test

## Reading it — what this does and does not establish

PENDING /du4-test

## Standing caveats that survive whatever the numbers say

- **Within-position only.** `player_rating` is normalized within position (`espn_client.py:1773-1791`,
  untouched by D10), so the added resolution separates players *inside* a position and overstates any
  cross-position benefit. The frequently-quoted `5 -> 555` headline is a **within-position** figure
  **measured at the PRE-CUTOVER window 20-80**; at the `STEPS = 25` this ticket ships the count is
  **730**. A figure quoted for the shipped config must use 730, and the within-position caveat applies
  to either number.
- **A six-player residue is a different failure class and was not chased.** **Six** players carry
  `player_rating` exactly 100.0. **Population, stated precisely because D9 changed it:** the six are
  six of the **737 numeric** `player_rating` values in `data/player_data/*_data.json` — that file set
  holds **773** `player_rating` entries in total, of which **36 are now `None`** (introduced by D9)
  and therefore are not numeric inputs to the ladder at all; the 737 numeric values span 1.0-100.0 and
  are **715 distinct**. *(An earlier draft of this document said "six of 799", which was the pre-D9
  entry count and no longer describes anything on disk.)* The six share one multiplier because they
  share an *input*, not because they are clamped. No window and no display precision removes it, and
  it must not be reported as residual clamping.
- **`STEPS = 25` is CONFIRMED and is NO LONGER PROVISIONAL.** Ticket D9
  (`player-rating-position-floor`) moves the `player_rating` input distribution this window was
  derived against, and it was unbuilt when D10.4 was *planned* — so the value was recorded as
  provisional and D10.4 carried a **binding re-run** of the derivation for after D9 landed.
  **D9 has since landed** (`D9.1` = `cefc2f15`, `D9.2` = `327f5f19`, both verified ancestors of this
  unit's branch point), and **the binding re-run was executed at D10.4's build against the post-D9
  pool. The value did not move: `STEPS = 25` is confirmed.** The pool did move — D9 both shrank the
  numeric set and shifted its low tail — so the absolute counts differ from the pre-D9 derivation
  while the decision is unchanged: at `STEPS = 25` better-end clamping is still the only row to reach
  **0**, and total distinct multipliers is still maximized, at **607** post-D9 (against 572 at
  `STEPS = 24` and 605 at `STEPS = 26`). **The distinct-multiplier figure quoted in the
  within-position bullet above is the PRE-D9 measurement** and is retained as the figure the ticket's
  headline correction was written against; **607** is the post-D9 count for the shipped configuration. An independent hard ceiling bounds the answer in any
  case: `MULTIPLIER_INPUT_DOMAINS[PLAYER_RATING_SCORING]` is `(0, 100)` and the anchors are
  `[S, 2S, 3S, 4S]`, so `4S <= 100` means `S <= 25` — `S = 26` raises `ValueError` at config load.
