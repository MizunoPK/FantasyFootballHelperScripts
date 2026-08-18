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

Measured 2026-08-17 at unit branch `unit/D10.4` @ `90147b3b`, by the `/du4-test` agent-run pass
recorded in that unit's `agent_test_session_2026-08-17T2310.md`.

**The result is not null. Every one of the ten drafts diverged.**

| Metric | A vs B (both cutovers) | A2 vs B (D10.4 alone) |
|---|---|---|
| Draft slots whose roster diverged | **10 of 10** | **10 of 10** |
| Our picks that differ | **59 of 150** (39.3%) | **59 of 150** (39.3%) |
| Earliest round of divergence | **Round 6**, in all ten slots | **Round 6**, in all ten slots |
| Position mix of players B took that the comparison arm did not | TE 10, K 10, RB 4, DST 3, QB 1 | TE 10, K 10, RB 4, DST 3, QB 1 |

**A third arm was added to isolate this factor, and it changed the attribution.** The two-arm
comparison the section above defines (A = both factors BUCKETED, B = both LINEAR) measures D10.3 and
D10.4 *together*. A third arm **A2** was therefore also replayed — `ADP_SCORING` LINEAR,
`PLAYER_RATING_SCORING` BUCKETED, i.e. the tree exactly as it stood at this unit's branch point
`ebb7a6e8`. **Arms A and A2 produced pick-for-pick identical rosters in all ten slots.** So
`ADP_SCORING`'s LINEAR cutover (D10.3) has **zero** observable effect on draft selection in this
scenario set, and **every** difference reported above is attributable to `PLAYER_RATING_SCORING`
alone. That is consistent with, and independently reproduces, D10.3's own recorded finding that the
committed ADP pool is a wall of identical placeholder values with none inside the interpolating
window — its cutover is a no-op on committed data.

**Arm construction, stated precisely because the arms are what the comparison rests on.** All three
arms are scratch copies of the lane's `data/` tree that differ **only** in
`configs/league_config.json` (asserted by `diff -rq` of each baseline arm against arm B before the
replays -- A-vs-B and A2-vs-B were run, and A-vs-A2 follows transitively; no `player_data/`,
`team_data/` or schedule file differs). Arm A's config is `git show cd16eef7:...`, the last commit
on that file before D10's cutovers. Arm A2's is `git show ebb7a6e8:...`. Arm B's is the shipped
branch state. `PLAYER_RATING_SCORING.WEIGHT` is **4.0 in all three arms** — asserted explicitly,
because an unequal weight would have made this measure two changes at once. Nothing was committed,
nothing was snapshotted, and the working tree was verified clean before and after.

**Replay method.** Each of the ten recorded drafts is replayed pick-by-pick in `overall` order.
Opponent picks are taken from the record and marked drafted. At each of our fifteen picks the
recorded player is **ignored** and the real `AddToRosterModeManager.get_recommendations()` is called
— the same call the interactive Add to Roster mode makes, which drives the real scorer and multiplier
accessor — and its top recommendation is drafted through the real manager. No scoring logic was
reimplemented, approximated or copied. Each slot ran in a fresh manager construction so no state leaks
between slots or arms. (`get_recommendations()` is the one call name the unit's session log attests
directly; the deeper call path is described here from the harness, not from the log.)

**One population caveat, measured rather than assumed.** Seven distinct player names appearing in the
recorded drafts (59 pick occurrences in total) are absent from the current 773-player pool, because
the drafts were recorded on 2026-08-03 and the pool has moved since. Those picks are simply not
marked taken — **identically in all three arms**, so they do not bias the comparison — but they mean
each replayed draft runs against a pool 5-7 opponent-removals shallower than the original did (59
across all ten slots, distributed 7+6+6+6+5+5+5+5+7+7).

## Per-slot roster deltas

Per-slot rosters for all three arms are in the unit's session log; the deltas are reproduced here
because this is the tracked artifact. Rounds 1-5 are identical across all three arms in every slot —
divergence begins at Round 6 (the TE slot) every time. "B-unique" = on arm B's roster and not on the
comparison arm's; the reverse column is the comparison arm's. **A2 vs B is identical to A vs B in
every row, because A and A2 are identical.**

| Slot | First divergent round | Differing picks | B-unique | A / A2-unique |
|---|---|---|---|---|
| 01 | R6 | 6/15 | Travis Kelce (TE), Jake Bates (K), Tyrone Tracy Jr. (RB) | Jake Ferguson (TE), Jaylen Warren (RB), Brandon Aubrey (K) |
| 02 | R6 | 6/15 | Travis Kelce (TE), Jake Bates (K), Kenneth Gainwell (RB) | Jake Ferguson (TE), Jaylen Warren (RB), Brandon Aubrey (K) |
| 03 | R6 | 7/15 | Travis Kelce (TE), Jake Bates (K), Kenneth Gainwell (RB) | Jake Ferguson (TE), Jaylen Warren (RB), Brandon Aubrey (K) |
| 04 | R6 | 5/15 | Travis Kelce (TE), Jake Bates (K) | Hunter Henry (TE), Brandon Aubrey (K) |
| 05 | R6 | 5/15 | Travis Kelce (TE), Jake Bates (K) | Hunter Henry (TE), Brandon Aubrey (K) |
| 06 | R6 | 6/15 | Travis Kelce (TE), Jake Bates (K), Steelers D/ST (DST) | Hunter Henry (TE), Brandon Aubrey (K), Seahawks D/ST (DST) |
| 07 | R6 | 9/15 | Travis Kelce (TE), Jake Bates (K), Steelers D/ST (DST), Kenneth Gainwell (RB) | Jaylen Warren (RB), Hunter Henry (TE), Brandon Aubrey (K), Lions D/ST (DST) |
| 08 | R6 | 3/15 | Travis Kelce (TE), Jake Bates (K) | Hunter Henry (TE), Brandon Aubrey (K) |
| 09 | R6 | 5/15 | Travis Kelce (TE), Jake Bates (K) | Hunter Henry (TE), Brandon Aubrey (K) |
| 10 | R6 | 7/15 | Travis Kelce (TE), Baker Mayfield (QB), Jake Bates (K), Colts D/ST (DST) | Matthew Stafford (QB), Hunter Henry (TE), Brandon Aubrey (K), Bills D/ST (DST) |

The two most consistent single-player swaps are the TE slot (Travis Kelce under LINEAR, in place of
Jake Ferguson or Hunter Henry) and the K slot (Jake Bates in place of Brandon Aubrey), each in all
ten slots. Only NFL player and NFL-defense names appear here; no fantasy league team name is recorded
in this document or in the session log.

## Reading it — what this does and does not establish

**What it establishes.** Switching `PLAYER_RATING_SCORING` to LINEAR at `STEPS = 25` changes the
drafted roster on committed data, in every one of the ten drafts, from Round 6 onward, in 39% of our
picks. It is therefore **not** a no-op, and the ticket's premise — that the step function was
discarding decision-relevant resolution — is borne out on the live scoring path rather than only in a
distribution table. The mechanism is visible directly: under BUCKETED, 212 of the 737 numeric
`player_rating` values (28.8%) all receive the identical maximum multiplier `1.2155x` and are
indistinguishable to the recommender;
at `STEPS = 25` that better-end collapse falls to **0**, and a probe of the real accessor on the
shipped config returns six distinct interior values across 30/37.5/50/62.5/75/87.5 where the previous
model returned repeated constants. A recommendation list driven through the real interactive Add to
Roster surface shows the same thing — the top backs carry distinct `EXCELLENT`-tier multipliers
(1.2102x, 1.2067x, 1.2155x, 1.2050x, 1.2120x) instead of all collapsing to `1.2155x`.

**What it does NOT establish — and this is the load-bearing limit.** It does **not** show that arm B
drafts *better* rosters. It measures **difference**, not **quality**. Nothing here is a win-rate,
points, or accuracy measurement; no arm was scored against an outcome. A 39% pick-change rate is
equally consistent with a real improvement and with a real regression, and this document must not be
cited as evidence of improvement. Establishing direction needs the win-rate sweep of
`PLAYER_RATING_SCORING_STEPS` that ticket `D27-sweepable-scoring-steps` carries as an open question,
and a re-derived `WEIGHT` that no unit in this ticket performed.

**Both arms carry weights fitted for the BUCKETED model.** As stated above, no `WEIGHT` was
re-derived for this ticket; `PLAYER_RATING_SCORING.WEIGHT` is 4.0 in every arm. That is what makes
the comparison single-variable and clean, and it is simultaneously why the shipped configuration is
**not** the fully re-tuned one. The re-derivation is deferred and carried on the ticket's gap ledger.

**The accompanying accuracy-simulation signal is unqualified.** `docs/simulation/ACCURACY_SIM_NOISE_FLOOR_D2.md`
records D2 as `Status: PARTIAL - ONE-SEED SMOKE RUN ONLY`. Nothing in this ticket may present the
accuracy sim as a qualified acceptance signal, and this A/B does not stand in for one.

**Reproducibility.** Re-read the LOCAL-ONLY caveat at the head of this document. It is binding on
this section too: the numbers above are durable, their inputs are not, and no reader can re-run this
comparison without a checkout that already carries `_internal/mock_drafts/`.

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
  headline correction was written against; **607** is the post-D9 count for the shipped configuration. A reachability ceiling bounds the answer in any
  case, and it is **mode-dependent**: `MULTIPLIER_INPUT_DOMAINS[PLAYER_RATING_SCORING]` is `(0, 100)`
  with anchors `[S, 2S, 3S, 4S]`. Under **BUCKETED**, `EXCELLENT` requires an in-domain input at or
  beyond `4S`, so `4S <= 100` — `S <= 25`, and `S = 26` raises `ValueError` at load. Under the
  **LINEAR** mode this document describes as shipped, a valued input resolves to its better-side
  *bracketing* anchor (TD3 option C), so `EXCELLENT` stays reachable for every in-domain input above
  `GOOD = 3S` and the binding constraint is `3S <= 100` — **`S <= 33`**, with `S = 34` raising
  `ValueError` (verbatim: `GOOD=102` leaves the domain, not `EXCELLENT`). Measured by driving
  `ConfigManager` over scratch copies of the shipped `data/` tree, 2026-08-18: under LINEAR, `25`,
  `26` and `33` all load and `34` raises; under BUCKETED, `25` loads and `26` already raises.
