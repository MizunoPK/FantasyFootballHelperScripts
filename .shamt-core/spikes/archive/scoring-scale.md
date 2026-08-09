# Spike: Continuous vs. Bucketed Scaling in the Scoring Chain

> **Delivery-track spike doc** (`/d-spike scoring-scale`). Transient, unnumbered, no status machine.
> Lives at `.shamt-core/spikes/scoring-scale.md`; archives to `.shamt-core/spikes/archive/scoring-scale.md`
> once it has emitted its tickets — that archive is git-tracked and is the durable record of
> **why** the work was split the way it was. Converted from `_internal/` on 2026-08-05.

> Status: **Investigation complete, all 9 open questions closed (2026-08-05) — at decomposition.**
> Prototype built and measured; no project code changed by this spike.
> Started 2026-08-03. Baseline: `main` @ `97ee42e7`; `data/` byte-identical to that commit
> (2026 week-1 PPR, 799 players). Measurements taken at week 1 and, where team ranks must
> discriminate, at week 11.
>
> **Shorthand used throughout this doc:** "spike 1" = `spikes/draft-risk-scoring.md`
> (items A-E), "spike 3" = this doc. The numbering predates the delivery-track conversion and is
> retained because the item labels (B1, B4, E, ...) are cited by number in both directions.
>
> Trigger: `spikes/draft-risk-scoring.md` (spike 1) found that the ADP factor collapses
> 293 distinct inputs into 2 distinct outputs, and that player rating collapses 773 into 5. That
> raised a broader question than the ADP bug itself: **should the five-tier bucket mechanism be
> replaced with continuous scaling across all eight scoring factors?**
>
> Purpose: answer "is it worth exploring", size the work, and surface the constraints. **The
> investigation body decided nothing** — that was true through 2026-08-04 and the analysis below is
> written in that voice. At the 2026-08-05 decomposition the nine open questions *were* decided;
> those decisions live in §Open questions (each marked DECIDED or RESOLVED with its reasoning) and
> are applied in §Recommendation and §Decomposition. Where the analysis prose and a decision differ
> in emphasis, **the decision governs**.
>
> Prototype: `interp_proto.py` (scratch, not committed) — an offline model of interpolated
> multipliers. **No project code was modified for any measurement in this document.**

---

## TL;DR

**Yes, worth doing — and the cheapest version of it is much cheaper than a rewrite.** But four
findings change the shape of the work:

1. **The information loss is severe and measurable.** On the two richest factors the bucket layer
   keeps under 1% of the resolution the inputs carry (773 distinct player ratings → 5 multipliers;
   293 distinct ADPs → 2). The rank-based factors lose less, because their inputs are already coarse
   (team quality 32 → 5, matchup 26 → 5).
2. **The bucket layer is currently *masking* the Item-B ADP bug, and going continuous unmasks it
   catastrophically.** Interpolating without first fixing the threshold direction inverts the ADP
   factor for the entire pool — the prototype's round-5 board leads with Mahomes, Herbert and Bo Nix
   ahead of every elite RB. **Spike 1's Item B1 is a hard prerequisite**, not a nice-to-have.
3. **"Linear" is the wrong prescription for ADP specifically.** 640 of 799 players (80%) are packed
   into ADP 160.25–171.28 — a real but near-degenerate measurement, not a sentinel. A linear curve
   would spend most of its range separating players who are effectively tied; a rank or percentile
   transform would be *worse*, manufacturing confident separations out of 0.01-point noise.
4. **`player_rating` is computed here, not fetched — and it is normalized *within position*.** So
   the best player at every position scores exactly 100.0, and adding resolution to it adds
   within-position resolution only. It is also ~81% correlated with ADP in the draftable region, so
   the two together partially double-count the draft market. See §What `player_rating` actually is.

Recommended path: **fix B1, then interpolate between the existing anchors** (keeps every config key,
every sweep parameter, and the tier labels), and treat per-factor input transforms — chiefly ADP —
as a separate, later decision. Resolve the `player_rating` questions before, or alongside, adding
resolution to that factor.

> **Amended at decomposition (2026-08-05).** Two clauses above are superseded by decisions: the
> per-factor input transform for ADP is **closed as subsumed**, not deferred (Q2 — clamping already
> delivers the prescribed hybrid), and the `player_rating` questions are **decided**, not
> outstanding (Q7 keep both factors, Q8 keep within-position normalization). Finding 3 below stands
> as *analysis* — a linear-in-raw-ADP curve would indeed be wrong — but it is no longer an open
> problem, because the anchors clamp the tail flat without any transform.

**Correction to an earlier claim.** During the conversation that prompted this spike I asserted that
interpolation "cannot widen the score range" because it shares endpoints with the bucketed version.
**That is true per factor and false for the product.** Measured across four live factors, the
realized spread widens from **2.640× to 2.812×** and 295 of 799 players move more than 5%. The
*theoretical* envelope is unchanged (each factor is still clamped to its anchor range); the
*realized* one widens because more players land near the extremes. See §Risks.

---

## Evidence: how much resolution the buckets destroy

Distinct input values vs. distinct multiplier values actually produced, across all 799 players,
measured at week 11 so team ranks discriminate:

| Factor | Distinct inputs | Distinct multipliers | Resolution kept |
|---|--:|--:|--:|
| Player rating | 773 | 5 | 0.6% |
| ADP | 293 | 2 | 0.7% |
| Team quality | 32 | 5 | 16% |
| Matchup | 26 | 5 | 19% |

The two factors with the richest inputs are the two that lose the most. Player rating is a 0–100
score **derived by this project** (not fetched — see §What `player_rating` actually is) and
normalized within position, then flattened to one of five values; 209 of 799 players share the top
value, and the full tier census is `EXCELLENT 209 / GOOD 205 / NEUTRAL 203 / POOR 160 /
VERY_POOR 22`.

Under the prototype, with spike 1's B1 direction fix applied:

| Factor | Bucketed | Interpolated | Multiplier range |
|---|--:|--:|---|
| ADP | 2 distinct | **51 distinct** | 0.8970 – 1.1090 (unchanged) |
| Player rating | 5 distinct | **555 distinct** | 0.8145 – 1.2155 (unchanged) |

Per factor, the achievable range is identical — interpolation fills the interior, it does not extend
the ends.

---

## Feasibility: are the eight factors even shaped for this?

All eight are **monotone in their (possibly transformed) input**, which is the property that makes a
single continuous mechanism viable:

| Factor | `DIRECTION` | `STEPS` | `WEIGHT` | Input |
|---|---|--:|--:|---|
| ADP | `INCREASING` *(bug — spike 1 Item B)* | 20 | 2.12 | ADP, lower better |
| Player rating | `INCREASING` | 20 | 4.00 | 0–100, **derived here; normalized within position** |
| Team quality | `DECREASING` | 6 | 2.77 | team rank 1–32 |
| Matchup | `INCREASING` | 6 | 1.62 | rank difference |
| Schedule | `BI_EXCELLENT_HI` | 2 | 0.90 | avg future opponent rank |
| Performance | `BI_EXCELLENT_HI` | 0.18 | 0.03 | actual-vs-projected deviation |
| Temperature | `DECREASING` | 10 | 0.75 | **distance from ideal** |
| Wind | `DECREASING` | 8 | 3.76 | gust speed |

Two things worth noting, because both look like blockers and neither is:

- **`BI_EXCELLENT_HI` is not a non-monotone response.** It places the four thresholds symmetrically
  around `BASE_POSITION` (`VP = base − 2·steps … E = base + 2·steps`,
  `ConfigManager.py:789-795`) and is still monotone increasing. The "BI" describes threshold
  *placement*, not curve shape.
- **Temperature's genuine non-monotonicity is handled upstream.** `get_temperature_distance()`
  (`ConfigManager.py:401`) converts temperature to an absolute distance from ideal *before* the
  curve is applied, so the curve itself stays monotone decreasing. That is the pattern any future
  non-monotone factor should follow, and it means the multiplier layer never needs to represent a
  peak.

So no factor requires a fundamentally different shape. One continuous mechanism can serve all eight.

---

## The distribution problem — why "linear" ≠ "continuous"

Continuous scaling is the right *goal*; a linear map from raw input to multiplier is the right
*implementation* for only some of these factors.

**ADP is the problem case.** Its distribution is near-degenerate, not continuous:

```
ADP  < 80        69 players
ADP  80–160      90 players
ADP  160–168     25 players
ADP  >= 168     615 players
```

640 players (80% of the pool) sit in a ~11-point band (160.25–171.28) at the top of the range.

**It is not a literal sentinel.** Those 615 players at ≥168 carry **113 distinct exact values**,
tightly clustered — 170.0 (93 players), 169.99 (86), 170.01 (64), 169.98 (41), 169.97 (38). So this
is a real measurement asymptoting for players drafted in a vanishing fraction of leagues, not a
hardcoded default. That distinction matters, because it rules out the obvious remedy:

- A linear-in-ADP curve spends most of its dynamic range separating players who are effectively
  tied, and compresses the top ~70 where the signal is.
- **A rank or percentile transform is worse, not better, for this tail.** Ranking 615 players whose
  ADPs differ by 0.01 manufactures large, confident rank separations out of what is plainly noise.
  Percentile-transforming the whole pool would spread that noise across most of the output range.
- So the transform must be **hybrid**: meaningful resolution over the ~159 players with ADP < 160,
  and a deliberate flat/`NEUTRAL` treatment of the tail — with the cut point chosen from the data
  rather than assumed. Where exactly that cut falls is an open question, not a solved one.
- This affects **spike 1's Item B2** (continuous ADP curve) whether or not the broader change here
  happens. It should be recorded there regardless.

**The rank-based factors are the easy case.** Team quality (1–32) and matchup (rank difference) are
uniform by construction — linear interpolation is not just acceptable but close to ideal, since the
input is already a rank.

**Player rating** is 0–100 and reasonably well spread (773 distinct values across 799 players);
linear with clamping at the anchors is a defensible default — but see §What `player_rating` actually
is before adding resolution to it: the extra resolution is within-position only.

---

## What `player_rating` actually is — and two consequences

Found while validating this document. The original draft of this section asserted that
`player_rating` is derived from ESPN's draft rank. **That is only the fallback path**, and the
correction changes what follows.

### Provenance

`player_rating` is **computed by this project, not fetched**. Two paths:

1. **Primary** (`espn_client.py:1497-1533`) — ESPN's `rankings` object, taking `averageRank` for
   `rankType == 'PPR'` at the player's slot. This is ESPN's expert/consensus **positional** ranking,
   a different signal from the draft market.
2. **Fallback** (`espn_client.py:1697-1709`) — when the rankings object is missing, a piecewise
   formula over `draftRanksByRankType.PPR.rank`, logged as a warning.

Either way the result is then **min-max normalized within position** to a 1–100 scale
(`espn_client.py:1773-1791`):

```python
normalized = 1 + ((positional_rank - max_rank) / (min_rank - max_rank)) * 99
```

Verified on the live data — every position tops out at exactly 100.00, which is the signature of
per-position min-max normalization:

```
DST  n= 32   min  1.00 (Dolphins D/ST)    max 100.00 (Broncos D/ST)
K    n= 37   min  1.00 (Ben Sauls)        max 100.00 (Brandon Aubrey)
QB   n=105   min  1.00 (Philip Rivers)    max 100.00 (Josh Allen)
RB   n=172   min 28.87 (C.J. Ham)         max 100.00 (Jahmyr Gibbs)
TE   n=159   min  5.97 (Zack Kuntz)       max 100.00 (Trey McBride)
WR   n=294   min  1.54 (Kaden Prather)    max 100.00 (Puka Nacua)
```

(RB's floor of 28.87 rather than 1.00 is unexplained. The obvious hypothesis — that some RBs took the
fallback path, whose formula floors at 15 — is **not** supported: no RB carries a rating of exactly
15.0, and the low end is a smooth arithmetic ramp (28.87, 29.29, 29.70, 30.12 … step ≈ 0.42), which
is the signature of min-max normalization over a rank range whose bottom no surviving RB occupies.
That would mean `position_rank_ranges['RB']` spans players who were later filtered out of the export.)

**Update (2026-08-05, decomposition step): re-confirmed at HEAD and promoted from observation to
ticket 1.** The figures reproduce on the current `data/` tree — RB `n=172 min=28.87`, TE
`n=159 min=5.97`, against WR `min=1.54`, QB/K/DST `min=1.00`, every position `max=100.00` — and the
low-end ramp holds at a constant step ≈ 0.415 (28.87, 29.29, 29.70, 30.12, 30.53, 30.95). The
mechanism is now **supported, not merely hypothesized**: `position_rank_ranges` is accumulated over
every player carrying a `PPR` `averageRank` (`espn_client.py:1535-1551`) and then used as the
normalization span at `:1778-1791`, so any player who is ranked but filtered out of the export leaves
the survivors unable to reach the scale's floor.

**Why it stopped being out of scope.** As an isolated curiosity it was cosmetic. Read against
§Consequence 1 it is not: `player_rating` carries `WEIGHT 4.00` — the largest in the chain — and the
chain uses it to build a **cross-position** ranking, so a floor that differs by position (28.87 for
RB, 1.00 for QB) is a systematic cross-position bias in the heaviest factor, not a rounding artifact.
It is independent of everything else in this document and shippable on its own merits. **This is
ticket 1** (§Decomposition), and the diagnosis proper — is the filtered-out set free agents, an
inactive-roster cut, or something else — belongs to that ticket's design stage, not here.

### Consequence 1 — `player_rating` carries no cross-positional information at the top

Because normalization is per position, **the best player at every position scores exactly 100.0** and
therefore receives the identical `1.2155×` multiplier. Brandon Aubrey (K) and the Broncos D/ST get
the same rating multiplier as Jahmyr Gibbs (RB) and Josh Allen (QB).

The chain nevertheless uses this factor to produce a **cross-position** ranking. Nothing in the
rating layer distinguishes "best RB in the league" from "best kicker" — that separation comes
entirely from the normalized projection and the draft-order bonus.

This matters directly for the question this spike asks: **adding resolution to `player_rating` adds
within-position resolution only.** It sharpens "is this the RB3 or the RB7" and does nothing for the
cross-position comparison the recommender actually has to make. That is a real limit on the benefit
of option 3 for this particular factor, and it is invisible if you only look at the
5 → 555 distinct-value headline.

### Consequence 2 — measurable overlap with ADP

The two factors are correlated, though — after the correction above — they are related rather than
identical: one is an expert positional ranking normalized within position, the other a global
market draft position.

```
Pearson r(ADP, player_rating), all 799 players          -0.6082
Spearman rho, all 799 players                           -0.4958
Pearson r, restricted to ADP < 160 (n=159)              -0.8086   <- the draftable region
```

81% correlated in the region where drafting decisions happen. The chain multiplies them as though
independent, at `WEIGHT` 2.12 and 4.00 — a combined exponent of ~6.12, the largest influence in the
chain. Adding resolution to both sharpens a partially double-counted signal rather than adding
proportionate information.

This is not an argument against continuous scaling. It is an argument that **resolution and
independence are separate problems, and this spike only addresses the first.**

**Options, none of them free:**

- **Accept it.** Expert rank and market ADP genuinely differ, and double-weighting the draft-market
  consensus may be empirically fine. But it should be a recorded decision rather than an accident of
  two factors having grown up separately.
- **Collapse to one.** Cleanest model; loses either the positional normalization (rating) or the
  global comparability (ADP). Given consequence 1, these are complementary rather than redundant —
  so collapsing is less attractive than the raw correlation suggests.
- **Keep both, re-tune jointly.** Treat them as one composite and tune the combined exponent. Least
  disruptive, but leaves two dials that must move together — which the sweep, treating them as
  independent coordinates, will not do.

**This also lands on spike 1.** Its Item C open question 7 asks who owns the injury-risk signal if
both a continuous ADP curve and a durability factor ship. It is now three-way — ADP, `player_rating`,
and any new availability factor all encode overlapping draft-market information. Re-scope it there.

---

## Options

| Option | What changes | Pros | Cons |
|---|---|---|---|
| **1. Status quo** | nothing | Zero risk; tier labels are readable; robust to outliers and bad data | Discards >99% of input resolution on the two richest factors; hides config errors (§The sequencing finding) |
| **2. More tiers** | 5 → e.g. 10–20 buckets | Trivial; no mechanism change; keeps labels | Palliative, not a fix; more thresholds to configure and sweep; still arbitrary edges |
| **3. Interpolate between existing anchors** | `_get_multiplier` only | **Recommended.** Keeps every config key, every sweep parameter, and the tier labels; identical output *at* the anchors; one function; no migration | Loses the exact-`1.0` NEUTRAL band; realized spread widens modestly (§Risks); does not fix input distributions |
| **4. Per-factor input transforms + interpolation** | Option 3 + a transform hook per factor | The only option that can address the ADP tail at all; right in principle | A second design decision per factor; more to document and tune; needs its own validation. **No clean transform exists for the ADP tail** (§Distribution) — the likely answer is a chosen cut point plus a flat tail, which is a judgement call, not a derivation |
| **5. Learned / fitted weights** | replace hand-tuned curves with a fit against historical outcomes | Removes guesswork entirely | Needs a labelled objective and a trustworthy backtest; the win-rate sweep cannot currently provide one (spike 1 §Cross-link); far beyond this spike |

**Option 3 is the recommendation for a first pass**, with option 4 as the natural follow-up scoped
per factor rather than all at once.

### What option 3 actually does

Keep `BASE_POSITION`, `STEPS`, `MULTIPLIERS` and `WEIGHT` exactly as they are. Treat the four
thresholds as anchor points and interpolate linearly between them in input space, clamping outside
the outermost anchors. At each anchor the output is bit-identical to today's, so the change is
backward compatible at those points and the existing swept values remain meaningful.

Prototype (`interp_proto.py`, 57 lines including docstrings and the direction-fix helper)
implements exactly this, and needs no changes to `ConfigManager` beyond `_get_multiplier` itself.

---

## Prototype results

Four models compared on the live board. `B1only` = spike 1's direction fix, bucketed.
`interpNoB1` = interpolation on today's (broken) anchors. `B1+interp` = both.

**Prototype fidelity — verified, not assumed.** The prototype models a draft score as
`normalized_projection × adp × player_rating + draft_order_bonus`, which looks like a simplification
of the 14-step chain but is **exactly equivalent** in Add-to-Roster at week 1 with an empty roster,
because every other step is inert there:

| Step | State | Why |
|---|---|---|
| team quality | `1.0` | never populated in the JSON load path (spike 1 Item E) |
| matchup | off | `matchup=False` in the draft-mode call (`AddToRosterModeManager.py:243-257`) |
| performance, schedule | off | both `False` in the same call |
| bye penalty | `0` | empty roster, no overlap to penalize |
| injury penalty | `0` | `INJURY_PENALTIES = {LOW: 0, MEDIUM: 0, HIGH: 0}` |
| NFL team penalty | no-op | `nfl_team_penalty` is `[]`, weight `1.0` |

Checked empirically: prototype `today` vs. the real `PlayerManager.score_player()` across all **650
draftable players** gives a **maximum absolute difference of 0.0000000000**. The comparison is
therefore against the real scorer, not a stand-in.

**Scope limit worth stating:** that equivalence holds *at week 1 with an empty roster*. Later rounds
(non-empty roster → live bye penalty) and later weeks (team quality would matter if Item E were
fixed) would need the real scorer, not this prototype.

**Round 1** (`RB` primary, `WR` secondary) — top 6 identical under all four models; the elite RBs are
far enough clear that multiplier changes cannot reorder them. Churn appears further down:

| Model | Top-20 membership swaps | Positions reordered in top 20 |
|---|--:|--:|
| B1 only | 1 | 10 |
| interp only (no B1) | 5 | 13 |
| **B1 + interp** | 2 | 5 |

**Round 5** (`QB` primary, `FLEX` secondary) — where it gets decisive:

| # | today | B1 only | **interp only (no B1)** | B1 + interp |
|--:|---|---|---|---|
| 1 | McCaffrey | McCaffrey | **Mahomes** | McCaffrey |
| 2 | Josh Allen | Josh Allen | **Herbert** | Josh Allen |
| 3 | Ja'Marr Chase | Ja'Marr Chase | McCaffrey | Ja'Marr Chase |
| 4 | Gibbs | Gibbs | Josh Allen | Gibbs |
| 5 | Jonathan Taylor | Jonathan Taylor | **Bo Nix** | Jonathan Taylor |
| 6 | De'Von Achane | De'Von Achane | **Dak Prescott** | De'Von Achane |

`interp only` churns 9 of the top 20 and reorders all 20. `B1 + interp` changes no top-20 membership
and reorders 11 within it — a resolution refinement, which is exactly the intended effect.

---

## The sequencing finding (the important one)

**Bucketing is accidentally masking the ADP direction bug, and interpolation removes the accident.**

Today, `ADP_SCORING` has ascending anchors (`VP=20, P=40, G=60, E=80`) consumed by a
lower-is-better comparator. The branch order (`ConfigManager.py:1244-1252`) tests
`val <= EXCELLENT` **first**, so every player with ADP ≤ 80 falls into `EXCELLENT` before any other
branch can fire. That happens to be the *right* answer for elite players — by accident, and only
because the step function short-circuits.

Interpolation has no short-circuit. It reads the anchors as an ordered curve, so ascending anchors
under a lower-is-better reading produce a genuinely **inverted** ADP factor: ADP 1.76 clamps to the
`VERY_POOR` end (0.897×) and ADP ≥ 80 clamps to `EXCELLENT` (1.109×). The whole pool is scored
backwards. That is precisely what the `interpNoB1` column shows.

**Consequence:** any move toward continuous scaling must fix the direction first. More generally, it
argues for shipping spike 1's **B4 reachability guard before or alongside** this work — under
bucketing a misconfigured direction degrades quietly to a step function that may still be roughly
right; under interpolation the same misconfiguration is silently catastrophic. Continuous scaling
raises the cost of a bad config, which makes the guard more valuable, not less.

---

## Risks

- **Realized spread widens (corrected claim).** Per factor the range is unchanged, but across four
  live factors the realized product spread goes from **2.640× to 2.812×**, stdev 0.181 → 0.206, and
  **295 of 799 players** move more than 5%. The theoretical envelope is identical — every factor is
  still clamped to its anchor range — but more players sit near the extremes once the interior is
  filled. Not disqualifying; it does mean the swept `WEIGHT` values may want re-tuning after the
  change, and that this cannot be shipped as a silent no-op.
- **The exact-`1.0` NEUTRAL band disappears.** Today a mid-range input returns exactly 1.0
  (203 players for player rating). Under interpolation the neutral zone becomes a ramp through 1.0,
  so almost no player is exactly neutral. Whether that matters is a judgment call — it is arguably
  more honest, but it removes a meaningful "this factor has no opinion" state. If that state is
  worth keeping, the interpolation needs an explicit flat segment between the `POOR` and `GOOD`
  anchors rather than a straight ramp.
- **Interpretability.** Tier labels survive, but the numbers beside them stop being one of five
  values. Measured, post-B1, at a few ADPs:

  | ADP | bucketed | interpolated |
  |--:|---|---|
  | 6.31 | `EXCELLENT 1.1090` | `EXCELLENT 1.1090` |
  | 22 | `GOOD 1.0537` | `EXCELLENT 1.1034` |
  | 30 | `GOOD 1.0537` | `GOOD 1.0812` |
  | 70 | `POOR 0.9477` | `POOR 0.9222` |

  Note ADP 22 changes *tier*, not just value — so the label is not merely cosmetic drift. The reason
  lines are printed in the recommendation UI (`ScoredPlayer.py:52-83`), so this is user-visible and
  worth a look before shipping.
- **Config errors get more expensive.** See §The sequencing finding. Mitigation is the B4 guard.
- **Every swept value must be re-derived — that is the stated goal, not a side effect.** See
  §Re-tuning below. The `WEIGHT` values for both `ADP_SCORING` (2.12) and `PLAYER_RATING_SCORING`
  (4.00) were fitted against a *bucketed* response surface; interpolation changes that surface for
  both. Re-running is required, and the win-rate sweep cannot credibly do it (spike 1 §Cross-link) —
  the accuracy simulation can.

**One hypothesis worth testing, not a finding:** a continuous response surface should be *easier* for
the sweep's coordinate ascent than a step function, because a step function creates plateaus where
the gradient is exactly zero and the optimizer adopts noise. If that holds, this change would
partially help the problem documented in `win_rate_similarity_investigation.md`. Unverified.

---

## Re-tuning: this change invalidates the fitted config values

The goal of both spikes is to change the scoring logic and then **re-derive optimal config values**
by re-running the accuracy and win-rate simulations. Spike 1 §"The re-tuning workflow" carries the
full contract; what is specific to *this* change:

- **Both factors this spike touches are swept.** `ADP_SCORING` and `PLAYER_RATING_SCORING` are in
  `BASE_CONFIG_PARAMS` (`simulation/shared/config_constants.py:1-17`), including their `THRESHOLDS`
  (`BASE_POSITION`, `STEPS`) and `WEIGHT`. Interpolation changes the meaning of `STEPS` — under
  bucketing it positions four cliffs; under interpolation it sets the slope of the ramp between
  anchors. **The swept `STEPS` values do not carry over with the same semantics**, which is a
  stronger statement than "may need re-tuning".
- **`ADP_SCORING_STEPS` was tuned against a dial that could not work.** Its sweep range is `[5, 50]`
  (`simulation/shared/ConfigGenerator.py:94`), but under the direction inversion `STEPS` only slid a
  single cliff at `4 × STEPS`; it could never create tiers. Post-B1 + interpolation it becomes a
  genuine slope control for the first time, so its current value carries no information.
- **The accuracy sim is the right harness in principle — but its noise floor is unmeasured.** It
  optimizes pairwise ranking accuracy against historical actuals across four weekly horizons, an
  ordinal objective, which is exactly what a resolution change should be judged on: a change that
  adds discrimination without improving ranking accuracy has not earned its complexity. **However**,
  no noise-floor study exists for it (spike 1 §Re-tuning workflow), and its sibling harness turned
  out to be noise-dominated. Measure it before trusting a promoted config — this matters more for
  interpolation than for most changes, because the expected effect is a *refinement* (round-1 top-6
  unchanged, 11 reorderings inside the top 20), and a refinement is exactly the size of signal a
  noisy harness cannot see.
- **Sequencing.** The re-tune must run *after* B1, E and this change land, and after `sim_data`
  is corrected for spike 1's Item A (the accuracy sim reads that tree). Starting it earlier tunes
  against a chain that is still degenerate.
- **Mind the default baseline.** `run_accuracy_simulation.py` defaults to the most recent
  `accuracy_optimal_*` folder (`run_accuracy_simulation.py:184-230`), i.e. values fitted to the
  bucketed chain. Pass `--baseline` deliberately for the first post-change run — see spike 1
  §Re-tuning workflow, consequence 2.

This also settles open question 3 in part: the swept `WEIGHT` values **do** need re-deriving, and the
objective is the accuracy sim's ranking accuracy rather than the win-rate sweep.

---

## Interaction with spike 1

| Spike-1 item | Effect of this work |
|---|---|
| **B1** (ADP direction) | **Hard prerequisite.** Interpolation without it inverts ADP pool-wide |
| **B4** (reachability guard) | **More valuable**, not less — continuous scaling raises the cost of a bad config |
| **B2** (continuous ADP curve) | **Largely subsumed.** Becomes "how should the ADP tail be handled on top of interpolation?" — option 4, scoped to one factor. Note a rank/percentile transform is *ruled out* by §Distribution, so B2's likely shape narrows to a cut point plus a flat tail |
| **E** (team quality dead) | **Should land first.** No value in adding resolution to a factor that returns `NEUTRAL` for everyone |
| **C** (availability factor) | If a new dimension is added, it should be built continuous from the start rather than as a 5-tier block — this spike decides what "the house pattern" is. Also: build it **cross-positionally comparable**, unlike `player_rating` (§What `player_rating` actually is, consequence 1) |
| **A** (bye zeroing) | **Prerequisite for the re-tune**, not for the code change — the accuracy sim reads `sim_data`, which carries the phantom-bye error |
| **D** (display) | Independent |

---

## Open questions

1. ~~Should the flat `NEUTRAL` band be preserved as an explicit segment?~~ **DECIDED (user,
   2026-08-05): no flat segment — a straight ramp through 1.0.** Plain linear interpolation between
   the `POOR` and `GOOD` anchors, which is exactly what `interp_proto.py` modelled, so **every
   measurement in this document describes what will ship** — no re-measurement is owed, and the
   §Prototype results tables stay the ticket's acceptance reference. Accepted cost: "this factor has
   no opinion" stops being expressible as an exact value (203 players are exactly neutral on
   `player_rating` today; under the ramp essentially none are), and the reason line's displayed
   multiplier stops landing on a round 1.0. No `NEUTRAL`-band width key is added, so the config
   surface grows by exactly the one `SCALING` key of Q4.
2. ~~What is the correct treatment of the ADP tail?~~ **DECIDED (user, 2026-08-05): closed —
   clamping already *is* the hybrid this section asked for, and the cut point is a swept value the
   re-tune owns. No ADP-tail ticket is emitted.**

   **The evidence that narrowed it** (checked at `97ee42e7`, and it reconciles with the prototype
   rather than merely sounding plausible). `data/configs/league_config.json` carries
   `ADP_SCORING.THRESHOLDS = {BASE_POSITION: 0, DIRECTION: INCREASING, STEPS: 20}`. Under the B1
   fix (`DIRECTION: DECREASING`) the `DECREASING` arm of `calculate_thresholds`
   (`ConfigManager.py:781-787`) derives `E = base + steps = 20`, `G = 40`, `P = 60`,
   `VP = base + 4×steps = 80`. So the interpolated curve spans **ADP 20 → 80** and clamps outside:

   | ADP band | Treatment | Players | Distinct ADPs |
   |---|---|--:|--:|
   | 1.76 – 20 | clamp `EXCELLENT` 1.1090× | 17 | — (all one value) |
   | 20 – 80 | **interpolated** | 52 | **49** |
   | 80 – 171.28 | clamp `VERY_POOR` 0.8970× | 730 (incl. the whole 640-player tail) | — (all one value) |

   (Measured on the committed `data/` tree, 799 players with an ADP, 293 distinct overall.) That is
   **49 interpolated values + 2 clamp values = 51 distinct**, exactly the figure §Evidence measured
   independently from `interp_proto.py` — so the anchor reading is corroborated by the prototype
   rather than asserted. Note the reconciliation is on **distinct ADP values (49)**, not on the
   player count in the band (52); three of those 52 players share an ADP with another.

   **Therefore:** the §Distribution prescription ("meaningful resolution over the draftable players,
   a deliberate flat tail, cut chosen from the data") is **already satisfied structurally** by
   clamping — it needs no transform, no sentinel rule and no cut-point heuristic. The cut point
   *is* `BASE_POSITION + 4 × STEPS`, both of which are swept (`BASE_CONFIG_PARAMS`), so **where it
   falls is the optimizer's decision, not a ticket's**. Two consequences recorded rather than
   ticketed: the tail maps to flat **`VERY_POOR`**, not flat `NEUTRAL` (an undrafted player takes a
   0.897× penalty — accepted as a real negative signal), and the ~20 elite players below ADP 20 are
   *also* clamped flat, so interpolation adds no resolution at the very top either. **Spike 1's
   Item B2 closes here as subsumed** — it does not become a ticket in this set.
3. ~~The swept `WEIGHT` **and `STEPS`** values need re-deriving — against what objective, and from
   what baseline?~~ **DECIDED (user, 2026-08-05): no re-tune ticket; the re-tune stays operational,
   but it is BOUND to the enablement ticket as an explicit acceptance step.** This deliberately
   **honours** spike 1's gate decision (its ticket 7 `rescoring-retune-baseline` was *dropped*, not
   deferred) rather than quietly reversing it one day later.

   The objective and baseline are already settled by §Re-tuning and are not re-opened: the
   **objective** is the accuracy simulation's pairwise ranking accuracy (an ordinal objective, the
   right one for a resolution change; the win-rate sweep cannot credibly serve — spike 1
   §Cross-link), and the **baseline** must be passed **deliberately** via `--baseline`, never the
   default most-recent `accuracy_optimal_*` folder, which is fitted to the bucketed chain
   (`run_accuracy_simulation.py:184-230`).

   **What the binding buys:** switching a factor to `LINEAR` without re-deriving its `STEPS` ships a
   value that no longer *means* anything — `STEPS` positions four cliffs under bucketing and sets
   the ramp slope under interpolation. So the enablement ticket carries the re-tune in its own
   acceptance scope, and spike 1's **now-unowned deliberate-baseline trap gains an owner for the
   first time since it was dropped**. The plumbing ticket is unaffected (default `BUCKETED` ⇒ no
   shipped score changes ⇒ nothing to re-derive).
4. ~~Should interpolation be opt-in per factor, or applied to all eight at once?~~ **DECIDED (user,
   2026-08-05): per-factor opt-in via a `SCALING: LINEAR|BUCKETED` key, defaulting to `BUCKETED`.**
   The mechanism lands **dark and inert** — with every factor defaulted to `BUCKETED` the change is
   a genuine behavioural no-op on import, which is what makes the §Recommendation A/B (the ten
   `_internal/mock_drafts/` runs under both models) possible at all. Factors switch on one at a
   time as each is validated.

   **Three consequences for the split, all load-bearing:**
   - The **mechanism** ticket (add the key + the interpolation branch, default off) and each
     **enablement** are separable, so the risky part is not welded to the plumbing.
   - Two mechanisms coexist in `_get_multiplier` for as long as any factor stays `BUCKETED`. That
     is **accepted, and deliberately not ticketed here**: a cleanup that deletes the bucketed branch
     is only writable once every factor has been switched and validated, which has not happened.
     Filing it now would emit a ticket whose precondition no ticket in this set establishes.
   - Because the default is off, the mechanism ticket **does not depend on the re-tune** — it
     changes no shipped score. The dependency attaches to the first *enablement*, not to the
     plumbing.
5. ~~Does the tier *label* stay useful once values are continuous?~~ **DECIDED (user, 2026-08-05):
   keep the label AND show the raw multiplier beside it** — `ADP: EXCELLENT (1.1034x)`. The label
   remains the at-a-glance summary; the number makes the now-continuous value legible and explains
   why two players both labelled `EXCELLENT` score differently (the measured ADP-22
   `GOOD → EXCELLENT` tier flip is exactly that confusion). Contained in `ScoredPlayer.py:52-83`.
   **Folded into the enablement ticket, not filed separately** — a display change describing a
   continuous value is meaningless while every factor is still `BUCKETED`.

   **Recorded coupling:** this touches `ScoredPlayer.py`, which is also in **`D7`
   (`projected-points-headline-not-a-projection`)**'s declared touch-set. See §Decomposition's
   probe table — it is a real cross-ticket dependency, not an independence claim.
6. ~~Is there any consumer that depends on the multiplier taking one of exactly five values?~~
   **RESOLVED (2026-08-05, from code — agent-resolved per Principle 2 point 5, no user judgment
   involved). No production consumer does.** `_get_multiplier` has exactly 8 call sites, all inside
   `ConfigManager.py:370-448`, and the label it returns reaches only the `ScoredPlayer` reason lines
   (display, `ScoredPlayer.py:52-83`). The flagged unknown is cleared: `trade_file_writer.py` parses
   reason strings with regexes targeting **`Bye Overlaps:`** (`:676-692`) and **`Injury:`**
   (`:694-708`) only — neither line originates from `_get_multiplier`, so no tier label is ever
   parsed back. Outside `ConfigManager.py` the five label constants appear only in docstrings
   (`ScoredPlayer.py:37,67,72`, `player_scoring.py:485,489`).

   **The real coupling is the test surface, and it is bounded:** 5 files / 40 call sites exercise
   the eight multiplier getters — `tests/integration/test_game_conditions_integration.py` (16),
   `tests/league_helper/util/test_player_scoring_game_conditions.py` (12),
   `tests/league_helper/util/test_ConfigManager_thresholds.py` (8),
   `tests/utils/test_FantasyPlayer.py` (3),
   `tests/league_helper/util/test_PlayerManager_matchup.py` (1). Any assertion pinning a bucketed
   value at a **non-anchor** input changes under interpolation; assertions at an anchor do not
   (option 3 is bit-identical there). That test delta belongs to the interpolation ticket, not to a
   ticket of its own.
7. ~~**Should ADP and `player_rating` remain two factors at all** (r = −0.81 in the draftable
   region)?~~ **DECIDED (user, 2026-08-05): keep both — "accept", recorded as a decision.** The
   reasoning is §Consequence 1's, not the raw correlation's: the two are **complementary rather
   than redundant** — `player_rating` carries within-position resolution and no cross-positional
   signal at the top, ADP carries the global market position — so collapsing would lose real signal
   that r = −0.81 conceals. The partial double-count of draft-market consensus is an **accepted,
   recorded overlap**, not an accident. **Consequence for the split: this does NOT block adding
   resolution to either factor**, so the interpolation work is ticketable now; sizing the combined
   ~6.12 exponent is the later re-tune's job, not a prerequisite.
8. ~~Should `player_rating` be normalized within position at all?~~ **DECIDED (user, 2026-08-05):
   keep within-position normalization; file the limit as a known bound.** Nothing about
   `espn_client.py:1773-1791` changes. The interpolation ticket **must record** that added
   resolution on this factor is **within-position only** — so the headline `5 → 555 distinct`
   figure overstates the cross-position benefit — and cross-position separation continues to come
   from the normalized projection plus the draft-order bonus, exactly as today. The
   K-scores-100-like-the-RB1 artifact is therefore an **accepted** property, not a defect this
   spike's ticket set repairs; a future change to it is a separate investigation, not a scope
   extension of interpolation.
9. ~~Can the accuracy simulation actually resolve an effect this small?~~ **RESOLVED (2026-08-05,
   agent-resolved per Principle 2 point 5 — the question has an owner, so it is not this spike's to
   answer.)** It is **`D2` (`accuracy-sim-noise-floor-unmeasured`)**'s whole purpose: re-evaluate one
   fixed config N times and compare that variance to the spread between candidates. This spike
   neither duplicates that work nor blocks on it — but the answer **gates the enablement ticket, not
   the mechanism ticket**: if the harness cannot resolve a refinement of this size, no factor should
   be switched to `LINEAR` on the strength of a promoted config, and the mock-draft A/B
   (§Recommendation) becomes the only usable acceptance signal. Recorded as a cross-ticket
   dependency in §Decomposition, not as an open question.

**No open questions remain.** Seven were user-decided (Q1, Q2, Q3, Q4, Q5, Q7, Q8); two were
agent-resolved from evidence with the resolution recorded inline (Q6 from code, Q9 by owner).

---

## Artifacts

- Prototype: `interp_proto.py` (scratch, uncommitted) — offline interpolation model; project code
  untouched.
- `spikes/draft-risk-scoring.md` — spike 1, the source of items A–E referenced throughout.
- `_internal/win_rate_similarity_investigation.md` — why the sweep cannot validate any of this.
- Key code sites:
  - `league_helper/util/ConfigManager.py:369-448` (the eight `_get_multiplier` consumers),
    `734, 772-795` (threshold derivation), `401` (temperature distance transform),
    `1196-1256` (`_get_multiplier`, branch order at `1244-1252`)
  - `league_helper/util/player_scoring.py:304-439` (the 14-step chain)
  - `league_helper/util/ScoredPlayer.py:52-83` (reason display)
  - `league_helper/add_to_roster_mode/AddToRosterModeManager.py:243-257` (the draft-mode scoring call
    whose flags make the prototype exact)
  - `player_data_fetcher/espn_client.py:1497-1533` (positional rank from ESPN `rankings`),
    `1697-1709` (draft-rank fallback formula), `1773-1791` (within-position min-max normalization)
- All measurements against `main` @ `97ee42e7`, `data/` byte-identical to that commit; week 1 except
  where week 11 is stated (needed for team ranks to discriminate).

---

## Recommendation

**Worth exploring — proceed, but sequenced behind spike 1's cheap fixes.**

Suggested order — **as amended at the 2026-08-05 decomposition**, which resolved every open question
and changed three steps. The original seven-step list is preserved in git; this is the live one:

0. **Measure the accuracy simulation's noise floor** — `D2`. Independent of everything below, and it
   decides whether any of the re-tuning that follows is meaningful (Q9).
1. Spike 1 **A** (bye fix) + correct `simulation/sim_data/` — `D3`. Prerequisite of the **re-tune**,
   not of the code change.
2. Spike 1 **B1** (ADP direction) — `D4`. **Hard prerequisite** for the ADP cutover.
3. ~~Spike 1 **E** (team quality population)~~ — `D6`. **No longer a prerequisite:** Q4's per-factor
   rollout does not enable team quality, so the "no point adding resolution to a dead factor"
   argument no longer applies to this work. `D6` remains worth landing on its own merits.
4. Spike 1 **B4** (reachability guard) — `D5`. More valuable once continuous; before or alongside.
5. **`player-rating-position-floor`** (ticket 1) — the RB/TE normalization floor. **New**, promoted
   from §Provenance's observation, and ordered here because it changes the input distribution the
   next step re-tunes against.
6. **`continuous-multiplier-scaling`** (ticket 2) — option 3 behind the per-factor `SCALING` key
   (Q4), defaulted `BUCKETED`; then the ADP + `player_rating` cutover, the bound re-tune from a
   **deliberate** `--baseline` (Q3), and the reason-line multiplier (Q5). One rollout, one ticket.
7. ~~**Option 4** (per-factor input transforms), starting with ADP~~ — **closed as subsumed** (Q2):
   clamping already delivers the prescribed hybrid and the cut point is a swept value. Spike 1's B2
   closes with it.

**Open questions 7 and 8 are decided** (keep both factors, recorded as an accepted overlap; keep
within-position normalization, its within-position-only benefit recorded as a known bound) — so the
caution that shaped this list is now a recorded constraint on ticket 2 rather than an open risk.
The underlying warning stands: the headline `5 → 555` figure overstates the cross-position benefit.

**The measurement that would settle it.** Re-run the ten mock drafts in `_internal/mock_drafts/`
under both models and compare the resulting rosters — a concrete A/B against a baseline that already
exists on disk.

One caveat on method: **this cannot use the prototype as-is.** Its exact equivalence to the real
scorer holds only at week 1 with an empty roster (§Prototype results); from round 2 on, the roster is
non-empty and the bye penalty becomes live. The A/B needs the interpolation applied inside
`_get_multiplier` itself and the real `score_player()` driving the draft — which is the same one-
function change option 3 proposes anyway, so the work is not wasted. Behind the per-factor opt-in of
open question 4, it can be landed dark and measured before being switched on.

---
Validated 2026-08-03 — 5 rounds, 1 adversarial sub-agent confirmed (sha256:52bbc9b9279e47e3) (spike, re-validated)

---

## Decomposition

**Proposed: 2 delivery tickets.** The count is low *because of the hard rubric*, not despite it — see
§"Why this is two tickets and not four" below, which is the part of this record worth reading.

| # | Ticket slug | Scope (one line) | Declared touch-set |
|---|---|---|---|
| 1 | `player-rating-position-floor` | `player_rating`'s within-position min-max spans ranks no surviving player occupies, so RB compresses into 28.87–100 while WR/QB span ~1–100 — a cross-position bias in the chain's largest-weight factor (4.00). | `player_data_fetcher/espn_client.py`, `tests/player_data_fetcher/` |
| 2 | `continuous-multiplier-scaling` | The whole interpolation rollout: add `SCALING: LINEAR\|BUCKETED` + the interpolation branch defaulted off, then switch ADP and `player_rating` on, re-tune, and surface the raw multiplier in the reason line. | `league_helper/util/ConfigManager.py`, `data/configs/league_config.json`, `league_helper/util/ScoredPlayer.py`, `tests/league_helper/util/test_ConfigManager_thresholds.py`, `tests/league_helper/util/test_player_scoring_game_conditions.py`, `tests/integration/test_game_conditions_integration.py`, `tests/utils/test_FantasyPlayer.py`, `tests/league_helper/util/test_PlayerManager_matchup.py` |

**Landing order: 1 → 2. Acyclic.**

### Why this is two tickets and not four

The obvious split — *(a)* add the mechanism dark, *(b)* enable ADP, *(c)* enable `player_rating`,
*(d)* delete the bucketed branch — is **wrong at the rubric**, and naming why is the point of this
record. That sequence is precisely **provision → cutover → contract**: a staged rollout, which
`reference/rollout_staging.md` puts inside **one** ticket's unit set, never across N tickets. Splitting
it would scatter one deployment-risk surface across four tickets and leave the partial-order table
("the cutover needs the flag first") with no single live record to live in. So (a)–(c) are **units of
ticket 2**, drawn at `/dt4-decompose` once its `/dt3-design` has assessed the risk across the whole
change.

Three further candidates were **considered and deliberately not filed**, each for a stated reason
rather than by omission:

- **The bucketing teardown (the `contract` stage).** Deleting the bucketed branch is only writable
  once *every* factor is `LINEAR` and validated — and this ticket set switches on **two of eight**.
  Its precondition is therefore not established by anything here, and filing it now would emit a
  ticket no member of this set makes landable. It stays unowned **by design**; the two mechanisms
  coexist in `_get_multiplier` meanwhile (Q4's accepted cost).
- **The ADP tail transform** (spike 1's B2). Closed as subsumed — Q2 showed clamping already
  delivers the prescribed shape and the cut point is a swept value. No ticket.
- **The re-tune.** Not re-filed; spike 1's gate dropped it deliberately (Q3), and it is bound into
  ticket 2's acceptance instead.

### Independence probe — every pair

One pair (`O(2×1)`), probed per `reference/project_separability_test.md`, bounded by the declared
touch-sets above.

| Pair | Outcome |
|---|---|
| 1 × 2 | **`probed: coupled — data-flow through the `player_rating` field, hop 2`** |

**Hop 1 — touch-set intersection: empty.** Ticket 1 is confined to `player_data_fetcher/espn_client.py`;
ticket 2 to `ConfigManager.py` / `league_config.json` / `ScoredPlayer.py` and the five multiplier
test files. No shared file. Hop 1 alone would have passed the pair as independent.

**Hop 2 — cross-referenced symbol: HIT, and it falsifies the premise.** `player_rating` is *written*
by ticket 1's touch-set (`espn_client.py:1773-1791`, normalizing over the `position_rank_ranges`
collected at `:1535-1551`) and *read* by ticket 2's (`ConfigManager.get_player_rating_multiplier`,
`:373`). Ticket 1 changes the **distribution of the inputs** ticket 2 adds resolution to and re-tunes
against. Landing them in the wrong order means `player_rating`'s re-derived `STEPS` and `WEIGHT` are
fitted to a compressed 28.87–100 RB scale that ticket 1 then widens — silently invalidating the
re-tune ticket 2 just performed. This is exactly the failure hop 1 could not see.

**Resolution (required before the gate):** the independence claim is **dropped**, not repaired. The
pair is recorded as an **ordering dependency — ticket 1 lands before ticket 2's cutover** — which the
landing order above encodes. They are not merged into one ticket: the touch-sets are genuinely
disjoint, the defect in ticket 1 is real and shippable on its own merits regardless of whether
interpolation ever happens, and a re-tune is re-runnable if the order is ever violated.

### Cross-ticket dependencies on the already-emitted set

These are cross-*ticket* dependencies (legal), not a rollout spanning tickets:

| Dependency | Kind | Note |
|---|---|---|
| `D4` (`adp-threshold-direction-inversion`) → ticket 2 | **Hard prerequisite** | Interpolating on today's ascending anchors inverts ADP pool-wide (§The sequencing finding). Ticket 2's ADP cutover **cannot** land first. |
| `D2` (`accuracy-sim-noise-floor-unmeasured`) → ticket 2 | Gates the re-tune's trustworthiness | Q9. If the harness cannot resolve a refinement this small, the mock-draft A/B is the only usable acceptance signal. |
| `D3` (`bye-week-phantom-projections`) → ticket 2 | Prerequisite of the re-tune only | The accuracy sim reads `simulation/sim_data/`, which carries the phantom-bye error. Not a prerequisite of the code change. |
| `D5` (`unreachable-multiplier-tier-guard`) → ticket 2 | Preference, before or alongside | Continuous scaling raises the cost of a bad config, making the guard more valuable (§The sequencing finding). |
| `D7` (`projected-points-headline-not-a-projection`) × ticket 2 | **File-level coupling** | Both touch `ScoredPlayer.py` (`D7` the `pts` headline, ticket 2 the reason line at `:52-83`). Sequence them; do not run concurrently. |
| `D6` (`team-quality-inert-in-json-load-path`) | **No longer a prerequisite** | §Interaction with spike 1 said E "should land first — no point adding resolution to a dead factor." That reasoning applied to enabling *team quality*, which Q4's per-factor rollout **does not** do. Recorded as a narrowing, so a later reader does not re-impose a dependency this set dropped on purpose. |

### Acceptance caveat carried into ticket 2

§Recommendation's settling measurement — re-running the ten `_internal/mock_drafts/` under both
models — rests on a baseline that is **present on disk but not version-controlled**: `git check-ignore`
resolves `_internal` to `.gitignore:13` (`**/_internal`). The ten `mock_draft_slot*.{json,md}` exist
on this machine only. Ticket 2 must either snapshot them into its own `test_data/` or record that the
A/B is reproducible only where those files exist — it must not cite them as a durable baseline.

### Emitted (2026-08-05)

Gate outcome: the proposed 2 were approved **as proposed** — no member added, removed or re-scoped.

| Ticket | Slug |
|---|---|
| `D9` | `player-rating-position-floor` |
| `D10` | `continuous-multiplier-scaling` |

Landing order: `D9` → `D10`, per the recorded hop-2 coupling. Both back-link to
`spikes/archive/scoring-scale.md`.

Cross-ticket prerequisites carried into `D10` from the already-emitted set: `D4` (hard, ADP
cutover), `D9` (hard, this spike's own), `D3` (re-tune only), `D2` (gates re-tune trust), `D5`
(preference), `D7` (file-level coupling on `ScoredPlayer.py`). `D6` is explicitly **not** a
prerequisite.

---
Validated 2026-08-05 — 2 rounds, 1 adversarial sub-agent confirmed (sha256:571bf62ffd2dbace) (spike; decomposition round)
