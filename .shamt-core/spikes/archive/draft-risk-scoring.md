# Spike: Risk / Availability in Draft Recommendation Scoring

> **Delivery-track spike doc** (`/d-spike draft-risk-scoring`). Transient, unnumbered, no status machine.
> Lives at `.shamt-core/spikes/draft-risk-scoring.md`; archives to `.shamt-core/spikes/archive/draft-risk-scoring.md`
> once it has emitted its tickets — that archive is git-tracked and is the durable record of
> **why** the work was split the way it was. Converted from `_internal/` on 2026-08-05.

> Status: **Spike open** — research complete for the five identified work items; no tickets filed yet.
> Started 2026-08-03. Baseline: `main` @ `97ee42e7`; `data/` byte-identical to that commit
> (2026 week-1 PPR, 799 players). **Every figure below is reproducible from that committed
> state** — see §Artifacts for the provenance note, including why an earlier live re-fetch was
> discarded as a basis.
> Trigger: a 10-sim mock draft run (`_internal/mock_drafts/`) had the app take Christian McCaffrey
> as the round-1 recommendation from every draft slot 1–6. Investigating *why* revealed that
> the recommender has no availability/durability dimension at all, and that two separate defects — a
> fetcher data bug and a config threshold inversion — make the situation worse than "risk is simply
> unmodelled". Two further items (a UI presentation defect and a second dead scoring dimension)
> surfaced while validating this document.
>
> Scope constraint (user-set): any new data must be obtainable from the **ESPN API**. No paid
> feeds, no scraping, no manual CSV maintenance.
>
> Purpose: capture the evidence and the design options so tickets can be written later. This
> document decides nothing.

---

## TL;DR

The round-1 recommendation is a **pure rest-of-season projected-points sort**. Every other factor
in the 14-step chain is either constant across the candidate set or switched off:

| Factor | State at round 1, week 1 | Why |
|---|---|---|
| ADP multiplier | identical (`1.10897x`) for all 69 players with ADP ≤ 80 | threshold direction bug — §Item B |
| Player rating | identical (`1.21551x`) for all 209 players rated ≥ 80 | 5-tier bucketing, top tier is wide |
| Team quality | `NEUTRAL 1.00x` for **all 799 players** | **dead dimension** — `team_offensive_rank` never populated in the JSON load path, at any week — §Item E |
| Draft-order bonus | `+50` for both PRIMARY and SECONDARY | `{PRIMARY: 50, SECONDARY: 50}` — no P/S signal |
| Bye penalty | 0 | empty roster at round 1 (correct) |
| Injury penalty | 0 | `INJURY_PENALTIES = {LOW: 0, MEDIUM: 0, HIGH: 0}` — disabled |

So the ordering is decided at **step 1** and nothing downstream can change it. Five separable
work items came out of this — A–C from the investigation, D and E from validating this document:

- **Item A — bye-week phantom projections.** 203 of 799 players carry a non-zero projection in
  their own bye week. The ROS sum therefore credits points that cannot be scored. It lands
  asymmetrically on the exact players under comparison (McCaffrey **+21.6**, Gibbs **+18.7**,
  Bijan **0.0**). *Data-correctness bug, no design decisions, no new ESPN data.*
- **Item B — ADP threshold direction inversion.** `ADP_SCORING.THRESHOLDS.DIRECTION` is
  `INCREASING` but `get_adp_multiplier` consumes it with `rising_thresholds=False`. The result is
  a **binary cliff at ADP 80** — `GOOD`, `NEUTRAL`, and `POOR` are structurally unreachable.
  Every player from ADP 1.76 to ADP 78.56 gets the identical multiplier, which is precisely why
  the market's risk discount on McCaffrey (ADP 6.31 vs Gibbs 1.76) is invisible to the model.
  *Config/logic bug, no new ESPN data.*
- **Item C — no availability dimension.** Nothing in the chain models expected games played.
  This is the actual missing feature, and the only item requiring substantial design work. The project
  **already has** five seasons of per-week actuals on disk, so the v1 needs **zero** new API calls.
- **Item D — the displayed `pts` headline is not a projection.** The recommendation list shows
  `588.80 pts` for a player whose real rest-of-season projection is `355.83`: the headline is the
  *score* back-converted through the normalization, so the additive `+50` bonus re-inflates into
  ~109 phantom "points". Ranking is unaffected (monotone transform), but it changes how option C3
  should be judged. *Presentation bug, no new ESPN data.*
- **Item E — team quality is a dead dimension.** `team_offensive_rank` is never attached to players
  in the JSON load path (0/799): the field is not exported to `player_data/*.json`, and
  `refresh_matchup_scores()` populates only `matchup_score`. The ranks exist in `TeamDataManager`
  (32 entries) but never reach scoring, so the factor returns `NEUTRAL` for everyone **in every
  week**, not just week 1. *Bug, no new ESPN data.*

Fixing A and C inverts the round-1 ranking completely (§Impact model).

---

## Evidence log

### The round-1 trace (instrumented against the live clean board)

`AddToRosterModeManager.get_recommendations()` (`league_helper/add_to_roster_mode/AddToRosterModeManager.py:243`)
scores every free agent with `adp/player_rating/team_quality/bye/injury/nfl_team_penalty` enabled and
`performance/matchup/schedule` disabled. Normalization is `(ROS / pool_max) * 163` where
`pool_max = 355.83` — which *is* McCaffrey, so he enters at a full 163.000.

| | McCaffrey | Gibbs | Bijan |
|---|--:|--:|--:|
| ROS projection | 355.83 | 322.22 | 312.62 |
| normalized (×163 / 355.83) | **163.000** | **147.604** | **143.206** |
| × ADP | 1.10897 | 1.10897 | 1.10897 |
| × player rating | 1.21551 | 1.21551 | 1.21551 |
| × team quality | 1.00 | 1.00 | 1.00 |
| + draft-order bonus | +50 | +50 | +50 |
| injury penalty | 0 | 0 (`QUESTIONABLE`) | 0 |
| **final score** | **269.718** | **248.966** | **243.036** |

The 15.4-point normalization gap is scaled by a common ×1.348 and offset by a common +50. Ordering
is fixed at step 1.

Corroborating detail: Ja'Marr Chase (WR, `SECONDARY` in round 1) scores **249.734**, edging Gibbs
(RB, `PRIMARY`, 248.966). A `SECONDARY` beats a `PRIMARY` because both bonuses are 50 — the
`DRAFT_ORDER` P/S distinction contributes nothing to ordering among positions that both appear in
the round. (It *is* load-bearing against positions absent from the round, which get +0.)

### Cross-link: these are swept parameters

`INJURY_PENALTIES`, `DRAFT_ORDER_BONUSES`, and `ADP_SCORING` are all in the win-rate sweep's
override space (`simulation/win_rate/config_overrides.py:34-36`,
`simulation/shared/config_constants.py:8-14`). Their current values are plausibly optimizer
outputs, not hand-authored intent — `{PRIMARY: 50, SECONDARY: 50}` and all-zero injury penalties
are exactly what an optimizer lands on when it cannot distinguish anything.

Per `_internal/win_rate_similarity_investigation.md`, the sweep is **noise-dominated**: single-config
re-runs have stdev 0.031, larger than the 0.023 spread across all 1,860 configs. So "the optimizer
chose 0" is **not** evidence that injury penalties don't help — it is evidence the harness could not
measure them. Any ticket that re-tunes these should not treat the current values as a validated
baseline, and should be aware the sweep in its current state cannot validate the new values either.

> **Consequence for Item C:** the sweep cannot be used as the acceptance gate for a durability
> factor until the ceiling problem in that investigation is addressed. Backtesting (§Item C
> validation) is the realistic alternative.

---

## Item A — Bye-week phantom projections

### Root cause

`ESPNClient._populate_weekly_projections()` (`player_data_fetcher/espn_client.py:484-527`) loops
weeks 1–17 and writes whatever ESPN returns for `statSourceId=1`, with no bye-week check:

```python
projected_points = self._extract_raw_espn_week_points(player_info, week, position, 'projection')
if projected_points is not None and (projected_points > 0 or position == 'DST'):
    player_data.set_week_projected(week, projected_points)
```

The fetcher **does** know each team's bye — `_derive_bye_weeks_from_schedule()`
(`player_data_fetcher/player_data_fetcher_main.py:181`) derives it from `season_schedule.csv`
(empty `opponent` = bye) and it is handed to the client as `client.bye_weeks`
(`espn_client.py:276`, consumed at `1600`). It is written to the player record as `bye_week` but
**never used to zero the projection array**.

ESPN's `kona_player_info` payload simply carries a projection for the bye `scoringPeriodId` for
some players and not others. Where the array *is* zero on a bye (Bijan, week 11), that is ESPN
happening to omit the entry — not the fetcher doing anything.

Consumption side: `FantasyPlayer.get_rest_of_season_projection()` (`utils/FantasyPlayer.py:478-487`)
sums `range(current_week, 18)` unconditionally. The 17-slot array vs 18-week season is *not* an
off-by-one — fantasy regular seasons end at week 17 and both sides agree — but it does mean week 18
is silently excluded, which is worth confirming is intended.

### Blast radius

- **203 of 799 players (25.4%)** carry a non-zero projection in their own bye week.
- Top offenders: Jayden Daniels +23.6, Justin Fields +21.7, **McCaffrey +21.6**, De'Von Achane +20.4,
  Amon-Ra St. Brown +18.9, **Gibbs +18.7**, Justin Herbert +17.8, Mahomes +17.7.
- Error magnitude, measured across the 203 affected players as phantom ÷ season total:
  **median 7.0%, p10 3.9%, p90 17.8%, range 0.3%–100%** (the 100% case is Travis Homer, whose only
  non-zero projected week *is* his bye). For the round-1 names it is ~6%, but the tail is far worse,
  so "a few percent" understates it badly for low-projection players — exactly the deep-bench pool
  where late-round and waiver decisions are made.
- It is **not** uniform — it is effectively a coin flip per player (203/799), so it perturbs relative
  ordering, not just absolute magnitudes.
- Every downstream consumer of `fantasy_points` inherits it: Add-to-Roster, Starter Helper, Trade
  Simulator, the win-rate sim, and the "Projected: N pts" headline the user reads.

### Secondary anomaly (separate, needs its own investigation)

Bijan Robinson's week 5 is 0.0 even though ATL plays BAL that week. That is a projection **gap**,
not a bye. Unknown whether it is an ESPN omission, a parse miss, or a real ESPN zero. Worth a
sweep of "zero-valued non-bye weeks" across the pool before deciding whether it belongs in this
ticket or a separate one.

### Options

| Option | Where | Pros | Cons |
|---|---|---|---|
| **A1. Zero the bye at fetch** | `_populate_weekly_projections`, using the `bye_weeks` map already present | Fixes the data at source; every consumer inherits it; one place; `bye_weeks` already wired in | Requires a re-fetch to take effect; historical `sim_data/` stays wrong unless recompiled |
| **A2. Zero the bye at load** | `FantasyPlayer.from_json` / `get_weekly_projections` | Fixes existing on-disk data with no re-fetch | Repairs a symptom in the read path while leaving the file wrong; two sources of truth for "what is week N"; **does NOT reach `sim_data`** — the win-rate sim loads via `SimDataLoader._parse_players_json` → `PlayerManager.set_player_data`, never `FantasyPlayer.from_json` |
| **A3. Skip the bye in the ROS sum only** | `get_rest_of_season_projection` | Smallest diff | Leaves per-week projections wrong for Starter Helper and the sim; treats the bug as ROS-specific when it isn't |
| **A4. A1 + A2** | both | Correct at source *and* self-healing for already-fetched data | Slightly redundant; needs a clear statement of which layer owns the invariant |

Leaning **A1 + A2** (A4): A1 is the real fix, A2 makes it idempotent for `data/player_data/` already
on disk. Worth deciding explicitly whether the invariant "a bye week is always 0.0" is owned by the
fetcher or by the model.

**Neither option reaches `simulation/sim_data/`.** That tree is loaded by `SimDataLoader`
(`simulation/win_rate/SimDataLoader.py`) into `PlayerManager.set_player_data()`
(`league_helper/util/PlayerManager.py:959`), which replaces the per-week arrays wholesale and
bypasses `FantasyPlayer.from_json` entirely. So the five compiled seasons Item C wants to read need
either a **recompile** after A1 lands, a **third fix site** in the sim load path, or a bye-aware
denominator computed inside Item C itself. This is a real dependency, not a footnote — see
§Design questions #4.

**New ESPN data required: none.**

---

## Item B — ADP threshold direction inversion

### Root cause

`data/configs/league_config.json`:

```json
"ADP_SCORING": {
  "THRESHOLDS": { "BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20 },
  "MULTIPLIERS": { "VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05 },
  "WEIGHT": 2.12
}
```

`DIRECTION: INCREASING` resolves (`ConfigManager.calculate_thresholds`, `ConfigManager.py:734`,
INCREASING branch at `772-778`) to
`VERY_POOR=20, POOR=40, GOOD=60, EXCELLENT=80`. But ADP is lower-is-better, so
`get_adp_multiplier` calls `_get_multiplier(..., rising_thresholds=False)`
(`ConfigManager.py:369-370`), whose branch order is:

```python
if   val <= THRESHOLDS[EXCELLENT]: -> EXCELLENT      # 80  <- catches everything ≤ 80
elif val <= THRESHOLDS[GOOD]:      -> GOOD           # 60  <- unreachable
elif val >= THRESHOLDS[VERY_POOR]: -> VERY_POOR      # 20  <- always true once val > 80
elif val >= THRESHOLDS[POOR]:      -> POOR           # 40  <- unreachable
else:                              -> NEUTRAL        #     <- unreachable
```

With an ascending ladder fed to a descending comparator, **`GOOD`, `POOR`, and `NEUTRAL` can never
fire**. The factor is binary with a cliff at ADP 80.

Measured across all 799 players:

```
EXCELLENT   n=69    ADP  1.76 –  78.56   -> 1.10897x
VERY_POOR   n=730   ADP 85.58 – 171.28   -> 0.89696x
(GOOD / NEUTRAL / POOR: 0 players, structurally unreachable)
```

Among the 60 earliest-ADP players — the entire first six rounds of a 10-team draft — **all 60 get
the identical multiplier**, spanning ADP 1.76 to 70.33.

Contrast with `TEAM_QUALITY_SCORING`, which correctly uses `DIRECTION: DECREASING` and produces a
proper 5-tier ladder (rank 1→EXCELLENT, 12→GOOD, 18→POOR, 24→VERY_POOR). Same machinery, right
direction, works fine. This is a one-word config error, not an architectural limitation.

Also note `ADP_SCORING_STEPS` is a swept parameter with range `[5, 50]`
(`simulation/shared/ConfigGenerator.py:94`). Under the inversion, `STEPS` only slides the single
cliff (`4 × STEPS`); it can never create tiers. So the optimizer has been tuning a dial that does
far less than intended.

### Options

| Option | Change | Pros | Cons |
|---|---|---|---|
| **B1. Flip to `DECREASING`** | one config word | Minimal; restores the intended 5-tier ladder (E≤20, G≤40, P≥60, VP≥80); consistent with `TEAM_QUALITY`; no code change. **Not cosmetic** — measured, it re-tiers today's single 69-player EXCELLENT block into E 17 / G 16 / N 19 / P 17, so real ordering changes across rounds 2–8 | Still coarse *at the very top* — ADP 1.76 and 19.9 both stay EXCELLENT, and that is exactly the round-1 case that motivated this spike |
| **B2. Continuous curve for ADP** | new multiplier mode, e.g. `mult = clamp(1 + k·(log(ref/adp)))` | Monotone signal all the way down; separates 1.76 from 6.31 — exactly the risk discount we want | New scoring mode in `_get_multiplier`; a second shape to tune, document, and sweep; departs from the uniform 5-tier convention every other factor uses |
| **B3. Positional/rank-relative ADP** | compare ADP to positional ADP rank | Handles positional scarcity properly | Bigger change; overlaps conceptually with the draft-order bonus |
| **B4. Guard against unreachable tiers** | validate at config load that all 5 tiers are reachable, warn/raise otherwise | Prevents the whole class of bug recurring across all **eight** `_get_multiplier` consumers (`ConfigManager.py:370-448`); cheap; catches optimizer-generated configs that are silently degenerate | Doesn't itself fix ADP; needs a decision on warn vs raise (raise could break existing sweep configs) |

Leaning **B1 + B4 first** (correctness + a guard), with **B2 evaluated separately** because it is
where the actual risk signal lives.

Two things to hold together when scoping this: B1 is a **one-word change with a non-trivial
behavioural blast radius** (it re-tiers 69 players and will move mid-round recommendations), yet it
**still does not solve the motivating case** — McCaffrey (ADP 6.31) and Gibbs (ADP 1.76) both remain
EXCELLENT under a 20 threshold. So B1 should be scoped and tested as a real behaviour change
in its own right, and **B2 is the option that addresses the original complaint.**

**New ESPN data required: none.** ADP is already fetched. Additional market signals already present
in the same response and currently discarded (see §Data source options under Item C) could enrich this at zero extra
API cost: `draftRanksByRankType.PPR.rank`, `percentOwned`, `auctionValueAverage`,
`averageDraftPositionPercentChange`.

---

## Item C — Availability / durability dimension

The real gap. ADP is a *proxy* for risk (the market prices durability in); this would model it
directly.

### What the data says about the motivating case

Games with points ÷ 16 possible (17 slots − bye), from `simulation/sim_data/`:

| | 2021 | 2022 | 2023 | 2024 | 2025 | 5-yr | 3-yr |
|---|--:|--:|--:|--:|--:|--:|--:|
| McCaffrey | 7 | 16 | 16 | **4** | 16 | **73.8%** | 75.0% |
| Gibbs | — | — | 14 | 16 | 16 | 95.8% | 95.8% |
| Bijan | — | — | 16 | 16 | 16 | 100% | 100% |

Stable across window choice. External consensus agrees: McCaffrey is age 30 off a league-high 450
touches, [SI](https://www.si.com/onsi/fantasy/injuries/nfl-running-back-injury-risk-regression-candidates-2026-fantasy-football)
counts 10 career injuries and notes that 2025 was the fourth time he carried 240+ times, and that in
**two of the previous three** such instances he failed to play more than six games the following
year; [Yahoo](https://sports.yahoo.com/articles/christian-mccaffrey-fantasy-football-2026-175427479.html)
calls him "risky near the top of round 1." Bijan is described by
[SI](https://www.si.com/onsi/fantasy/nfl/jahmyr-gibbs-or-bijan-robinson-who-should-be-fantasy-footballs-first-running-back-off-the-board)
as "the safest pick in the draft — zero missed games." He is currently practicing fully
([ESPN camp tracker](https://www.espn.com/nfl/story/_/id/49427696/san-francisco-49ers-training-camp-2026-intel-updates)) —
the concern is durability, not present health, which is exactly what a *status* field cannot capture
and an *availability* factor can.

### Where it could live — four architectural options

**C1. New multiplicative step in the existing chain (step 15: Availability).**
- *Pros:* Uses the established `_apply_*` + `_get_multiplier` + config-thresholds pattern; ships as
  a new `AVAILABILITY_SCORING` block with its own `WEIGHT`, so it slots straight into the sweep
  space; independently toggleable per mode (draft on, weekly lineup off) like every other flag;
  appears in the `reason` list, which the recommendation UI does print (verified — `ScoredPlayer.py:52-83`),
  so the UI explains itself for free.
- *Cons:* Adds a 15th dimension to a chain whose factors already interact multiplicatively and
  saturate (§Cross-cutting). Semantically it is a *season-long* property being multiplied into a
  score that in weekly modes represents a *single game*, where "expected games played" is the wrong
  question — so it needs care to stay draft-only.

**C2. Repurpose the existing (dead) injury step.**
- *Pros:* No new dimension; `INJURY_PENALTIES` is currently all zeros so nothing is lost; the step,
  the config block, and the reason line already exist. Arguably what the injury step was *meant* to
  be — it currently keys on a point-in-time `injuryStatus` string, which is near-useless in August
  and can only ever say "this player is hurt right now," never "this player gets hurt."
- *Cons:* Conflates two genuinely different things — current health (Gibbs is `QUESTIONABLE` today)
  and chronic durability (McCaffrey misses seasons). Overloading one step means one weight has to
  serve both. Migration ambiguity: does `INJURY_PENALTIES` keep its meaning?

**C3. Adjust the projection input rather than the score.**
Multiply weekly projections by expected availability so ROS becomes a genuine expectation.
- *Pros:* Most theoretically honest — a 74%-available player's expected points really are ~74% of
  their healthy projection, and the "Projected: 355.8 pts" headline the user sees becomes truthful.
  Fixes every consumer at once (Starter Helper, Trade Simulator, sim) with no per-mode flags.
  Composes correctly with everything downstream instead of being one more multiplier fighting
  the others.
- *Cons:* **Changes the displayed projection.** Weaker than it first appears — per §Item D the
  headline figure is *already* not ESPN's number (it reads 588.80 for McCaffrey against a real 355.83),
  so C3 would be replacing a meaningless number rather than corrupting a trusted one. Double-counting risk if ESPN's projections already haircut for
  injury risk (unknown — needs checking). Muddies validation against ESPN. Harder to A/B against
  the current behaviour because the baseline number itself moves.

**C4. Move from point-estimate to distribution / risk-adjusted EV.**
Carry a variance or floor/ceiling alongside the mean and let the recommender optimize a
risk-adjusted objective (e.g. mean − λ·σ, or p25 for a floor-seeking strategy).
- *Pros:* The theoretically right frame — "risk" is variance, and this is what a real draft model
  wants. Would also let the draft-round context matter (early picks want floor, late picks want
  ceiling), which is genuinely how drafting works. Subsumes C1–C3 as special cases.
- *Cons:* Large rewrite of the scoring engine, `ScoredPlayer`, the display layer, and the sim.
  Needs a variance estimate per player that ESPN does not provide directly. Almost certainly not
  the next ticket — but worth recording as the direction C1/C2 should not actively foreclose.

**Leaning:** C1 for v1 (fits the architecture, cheap, reversible, sweepable), explicitly draft-mode-only
via the existing flag pattern, with C3 recorded as the more honest long-term shape and C4 as the
eventual direction. C2 is tempting for tidiness but the health/durability conflation looks like a
trap.

### Data source options (ESPN-only, per the scope constraint)

| Source | Extra API calls | Gives | Assessment |
|---|--:|---|---|
| **`simulation/sim_data/2021–2025` per-week actuals** (already on disk) | **0** | Games played per season, 5 seasons | **v1 choice.** No API work at all; already validated by `validate_sim_data.py`; the numbers in the table above came from it |
| `player.injuryStatus` + `injured` (already fetched, currently only feeding the dead penalty) | 0 | Current status only | Complementary, not a durability signal. Useful as a *separate* current-health term |
| League-wide injuries endpoint `site.api.espn.com/apis/site/v2/sports/football/nfl/injuries` | **1** | 800 entries across 32 teams: `status`, `type`, `date`, `shortComment`/`longComment` | Cheap and much richer than the status string. Good for current-health; verified live returning 200 |
| Per-team injury history `sports.core.api.espn.com/v2/.../teams/{id}/injuries` | 32 (paged: ~128) | Per-season injury records; SF returned `count: 85` | Possible injury-*history* signal. Needs a spike of its own — unclear how far back it reaches |
| Per-athlete bio `sports.core.api.espn.com/v3/sports/football/nfl/athletes/{id}` | **~799** | `age`, `dateOfBirth`, `experience.years`, height/weight | Age is a strong durability covariate (the age-30 RB cliff is the whole McCaffrey thesis). **But the bulk athletes list does NOT carry age** — verified: `/v3/.../athletes?limit=1000` returns only name/id/jersey/active across 21 pages. So age costs ~799 calls, i.e. roughly a second full fetch pass |
| Per-athlete gamelog `site.web.api.espn.com/apis/common/v3/.../athletes/{id}/gamelog?season=YYYY` | ~799/season | Authoritative games played | Same games-played answer `sim_data` already gives for free. Only worth it to extend history beyond 2021 |

**Verified live 2026-08-03**: the `kona_player_info` payload already carries, per player and at zero
extra cost, `ownership{averageDraftPosition, averageDraftPositionPercentChange, percentOwned,
percentStarted, auctionValueAverage, auctionValueAverageChange}`, `draftRanksByRankType{STANDARD,
PPR, ELIMINATION, SUPERFLEX}`, `injuryStatus`, `injured`, `seasonOutlook` (free text),
`ratings{positionalRanking, totalRanking, totalRating}`, `eligibleSlots`, `lastNewsDate`. Of these
only `averageDraftPosition` and the weekly `stats` are currently exported to
`data/player_data/*.json`.

**Recommendation for v1:** `sim_data` only (zero new API surface). Treat age as a **phase 2**
decision precisely because it costs a second ~799-call pass — that cost, not the modelling value,
is the blocker, and it should be an explicit call rather than a silent one.

### Design questions the ticket must answer

1. **Window and weighting.** 3 seasons or 5? Recency-weighted? Both windows agree for these three
   players, but that will not generalise.
2. **Rookies and short histories.** Gibbs has 3 seasons, Bijan 3, a 2026 rookie has 0. Need a prior
   — positional average? Neutral 1.0? A shrinkage estimator toward the positional mean is the
   principled answer and avoids punishing players for being young.
3. **Distinguishing "injured" from "benched/inactive/rookie-year-timeshare".** Games with 0 points is
   a crude proxy; a healthy backup also scores 0. This is the main threat to validity of the
   `sim_data` approach and needs a sanity pass before committing.
4. **Bye contamination, and Item A does not reach the data Item C reads.** Availability is computed
   from `simulation/sim_data/`, which neither Item-A fix option touches (§Item A → Options). So Item C
   must either wait on a `sim_data` recompile, add a third fix site in `SimDataLoader`, or compute a
   bye-aware denominator itself. Decide which before scoping — this is Item C's only hard dependency
   and it is easy to assume away.
5. **Position sensitivity.** RB durability ≠ QB durability ≠ K durability. Probably needs to be
   positional, or at minimum validated per position.
6. **Draft-mode only?** Availability is a season-long property; in weekly Starter Helper the question
   is "is he playing this week," which is a different (and better-answered) question.
7. **Interaction with ADP.** If Item B ships a continuous ADP curve, the market discount and the
   durability factor both encode injury risk — **double-counting risk**. Needs an explicit decision
   about which owns it, or a joint tune.

### Validation approach

The win-rate sweep is **not** a usable gate (§Cross-link — noise floor exceeds the effect size).

**The backtest already exists — it is `run_accuracy_simulation.py`.** An earlier draft of this
section proposed building one; that was wrong, and the correction matters because it removes the
main cost objection to Item C. The accuracy simulation optimizes **pairwise ranking accuracy against
historical actuals** (MAE is computed as a diagnostic only — the League Helper's decisions are
ordinal, and `is_better_than` deliberately compares ranking accuracy, not MAE), using tournament
optimization across four weekly horizons (weeks 1–5, 6–9, 10–13, 14–17) over `simulation/sim_data/`.
That is precisely the evaluation this spike wants, already built.

So the gate for Item C is: does the availability factor improve pairwise ranking accuracy in the
accuracy sim? Hold out by season to avoid fitting on the same data the factor is derived from.

**But it is contaminated by Item A.** The accuracy sim reads `simulation/sim_data/`, whose
`projected_points` arrays carry the phantom-bye error — and neither Item-A fix option reaches that
tree (§Item A → Options). So Item A must land *and* `sim_data` must be corrected before the accuracy
sim can produce trustworthy numbers for anything in this spike. This is the same dependency as
§Design questions #4, and it now blocks the validation path as well as the factor itself.

---

## Item D — the displayed "pts" headline is not a projection

*(Found while validating this document.)*

The recommendation list does print the full `reason` breakdown (`ScoredPlayer.__str__`,
`ScoredPlayer.py:52-83`), so a new scoring dimension would explain itself in the UI for free — good
news for C1. But driving the real CLI to inspect that output surfaced a separate problem:

```
1. [RB] [SF] Christian McCaffrey - 588.80 pts (Score: 269.72) (Bye=8)
            - Projected: 355.83 pts, Weighted: 163.00 pts
```

The **headline** figure is `588.80 pts`; the player's actual rest-of-season projection is `355.83`.
`ScoredPlayer.projected_points` is back-computed in `player_scoring.py:429-436` as
`(player_score / normalization_scale) * chosen_max` — i.e. the *score* converted back through the
normalization, at `355.83 / 163 = 2.183x`. Because the score includes multipliers **and the additive
`+50` draft-order bonus**, that bonus alone re-inflates to **109.15 phantom "points"**:

| | score | displayed "pts" | real ROS | inflation |
|---|--:|--:|--:|--:|
| McCaffrey | 269.72 | 588.80 | 355.83 | +232.97 (1.65×) |
| Chase | 249.73 | 545.17 | 323.47 | +221.70 (1.69×) |
| Gibbs | 248.97 | 543.50 | 322.22 | +221.28 (1.69×) |

So the number presented as points is roughly **1.65–1.69× any achievable point total**, and the two
figures on the same line disagree by design. The ordering it implies is still correct (it is a
monotone transform of the score), so this is a **presentation** defect, not a ranking one — but it
directly undercuts the framing of option **C3**, whose stated con was "changes the displayed
projection, which users read as ESPN's number." The displayed headline is *already* not ESPN's
number. If anything that strengthens C3: it would replace a meaningless figure with a meaningful one.

Worth confirming with the user whether the headline is intended to be a projection or an
arbitrary-scale ranking score — the label `pts` and the co-displayed `Projected: 355.83 pts` cannot
both be right.

---

## Item E — team quality is inert in the JSON load path, at every week

*(Found while validating this document.)*

The TL;DR originally attributed the flat `Team Quality: NEUTRAL (1.00x)` to week 1 having no ranking
data. That explanation is wrong, and the real cause is worse.

`PlayerManager.load_players_from_json()` (`PlayerManager.py:262-357`) builds each player via
`FantasyPlayer.from_json()`, which reads `team_offensive_rank` out of the JSON
(`utils/FantasyPlayer.py:150`). **That field is not exported to `data/player_data/*.json` at all** —
the player records carry only `actual_points, average_draft_position, bye_week, defense, drafted_by, extra_points, field_goals, id, injury_status, locked, misc, name, passing, player_rating, position, projected_points, receiving, rushing, team` (19 keys, re-enumerated across **all six** position files on 2026-08-05; an earlier revision of this doc listed 15, having sampled only the RB/WR files and so missing `passing`, `field_goals`, `extra_points` and `defense` — the omission does not affect the finding, since `team_offensive_rank` is absent either way). So it resolves to `None` for every player.

The deprecated CSV path *does* populate it (`PlayerManager.py:195`, from
`TeamDataManager.get_team_offensive_rank`). The JSON path calls only `refresh_matchup_scores()`
(called at `PlayerManager.py:342`, defined at `359-375`), which assigns `matchup_score` and nothing
else — its own docstring says it "mirrors the population the deprecated CSV path performs", but it
mirrors **one** of the fields that path assigns; `team_offensive_rank` and `team_defensive_rank`
were left behind.

Measured on the live objects:

```
TeamDataManager.offensive_ranks populated?      32 entries   (SF -> 16)
players with team_offensive_rank set (JSON):     0 / 799
players with non-zero matchup_score:           799 / 799
```

The ranks **are** available at runtime — `TeamDataManager` has all 32 — they are simply never
attached to the players. `_apply_team_quality_multiplier` (`player_scoring.py:467-476`) then reads
`p.team_offensive_rank` (or `team_defensive_rank` for DST), gets `None`, and `_get_multiplier`
returns `NEUTRAL 1.0` (`ConfigManager.py:1224-1226`).

**Consequences:**

- Team quality contributes **nothing, for every player, in every week** via the JSON path — not just
  week 1. At week 1 the symptom is **masked**: `TeamDataManager` returns a flat neutral 16 for all 32
  teams that early, which would map to `NEUTRAL` anyway. The bug only becomes *visible* once real
  ranks exist — measured:

  ```
  TeamDataManager(week=1).offensive_ranks   -> 32 teams, distinct values = [16]        (neutral)
  TeamDataManager(week=11).offensive_ranks  -> 32 teams, distinct values = [1..32]     (real)
  ```

  Discrimination begins around **week 11**, gated by `TEAM_QUALITY_SCORING.MIN_WEEKS = 10` in
  `TeamDataManager` (`TeamDataManager.py:144-147`). From then on the factor is *still* dead, because
  the rank never reaches the player object.
- Note there are **two different `MIN_WEEKS` constants** and they are easy to conflate:
  `TEAM_QUALITY_SCORING.MIN_WEEKS = 10` (runtime, `TeamDataManager`, the one that governs the ranks
  above) and `MIN_WEEKS_FOR_RANKINGS = 5` (fetch-side, `player_data_fetcher/player_data_constants.py:33`,
  governing whether the *fetcher* computes its own rankings). Only the former is relevant here.
- `TEAM_QUALITY_SCORING.WEIGHT` (currently 2.77) is another swept parameter tuning a dead dial —
  same class of problem as `ADP_SCORING_STEPS` in §Item B, and more evidence for the §Cross-link
  reading that the sweep cannot see what it is tuning.

**Fix shape:** populate `team_offensive_rank` / `team_defensive_rank` in `refresh_matchup_scores()`
(or a renamed `refresh_team_context()`) alongside `matchup_score`, so the JSON path matches the CSV
path it claims to mirror. Cheap and self-contained. **New ESPN data required: none** — the values are
already computed and in memory.

**Open question this raises:** DST scoring uses `get_team_dst_fantasy_rank` in the CSV path but plain
`get_team_defensive_rank` for non-DST; both are unset here. Whether restoring them changes DST
rankings materially needs a before/after check, not an assumption.

---

## The re-tuning workflow (the stated goal of both spikes)

The purpose of these spikes is not the code changes in isolation: it is to change the scoring logic
and then **re-derive the optimal config values** by re-running both simulations. That framing has
consequences worth recording before any ticket is written.


> **Citation currency note (2026-08-05).** Every `file:line` citation in this section was
> **re-derived against `main` @ `32a00a54`** during the `/d-spike` validation pass. T69 restructured
> `AccuracySimulationManager` into a convergent multi-pass ascent, which shifted or invalidated the
> original citations written against `97ee42e7`. The *claims* all still hold — the stale-baseline
> incumbency, the hold-others-fixed coordinate sweep, and the order dependence are unchanged — but
> the line numbers were not, and a ticket inheriting them would have cited dead lines.

### What each simulation owns

| | `run_accuracy_simulation.py` | `run_win_rate_simulation.py` |
|---|---|---|
| Objective | pairwise ranking accuracy vs. historical actuals (MAE diagnostic only) | win rate in simulated leagues |
| Method | coordinate-wise, one parameter at a time, structured as a tournament across 4 weekly horizons | coordinate ascent / sweep |
| Data | `simulation/sim_data/` | `simulation/sim_data/` |
| Output | `simulation/simulation_configs/accuracy_optimal_*/` | `simulation/simulation_configs/optimal_*/` |
| Noise floor measured? | **no — never studied** (see below) | yes — **noise-dominated** (§Cross-link) |

**The accuracy sim's reliability is assumed, not established.** `win_rate_similarity_investigation.md`
measured the win-rate sweep's noise floor and found it exceeds the entire spread across 1,860
configs. **No equivalent study exists for the accuracy simulation.** Its objective is better suited
to the question (ordinal, ground-truth-anchored, four horizons) and it does not obviously suffer the
ceiling effect that sinks the win-rate sweep — but "better suited in principle" is not a measured
noise floor. Since the entire re-tuning plan rests on this harness being able to distinguish
configs, the cheap precaution is to run the same experiment the win-rate investigation ran:
re-evaluate one fixed config N times and compare that variance against the spread between
candidate configs. Until that is done, treat promoted `accuracy_optimal_*` values as provisional.

The swept surface (`simulation/shared/config_constants.py:1-28`) includes — among others — every
parameter these spikes touch: `ADP_SCORING`, `PLAYER_RATING_SCORING`, `INJURY_PENALTIES`,
`DRAFT_ORDER_BONUSES`, `DRAFT_NORMALIZATION_MAX_SCALE` in the base config, and
`TEAM_QUALITY_SCORING`, `MATCHUP_SCORING`, `SCHEDULE_SCORING`, `NORMALIZATION_MAX_SCALE` in the
week-specific configs. So there is no item in this spike whose tuning survives the change untouched.

### Consequence 1 — the current optimal values are fitted to a broken chain

This is the strongest argument *for* re-tuning, and it is stronger than "the values may want
re-tuning":

- `ADP_SCORING.WEIGHT = 2.12` was fitted against a factor that is a **binary cliff** (Item B) —
  three of its five tiers unreachable.
- `TEAM_QUALITY_SCORING.WEIGHT = 2.77` was fitted against a factor that returns `NEUTRAL` for
  **every player in every week** (Item E). Whatever the optimizer did with that dial, it was not
  measuring team quality.
- `INJURY_PENALTIES = {0, 0, 0}` and `DRAFT_ORDER_BONUSES = {P: 50, S: 50}` are what an optimizer
  lands on when it cannot distinguish anything.

So re-running is **required, not optional** — the existing values are not a validated baseline being
refined, they are artifacts of a degenerate search space.

### Consequence 2 — a concrete trap in the re-run

`run_accuracy_simulation.py` **defaults its baseline to the most recent
`accuracy_optimal_*` folder**, falling back to a win-rate `optimal_*` folder
(`find_baseline_config`, `run_accuracy_simulation.py:187-236`). A naive post-change re-run therefore **starts tournament
optimization from values fitted to the broken chain.**

How much that matters depends on the search, which is worth stating precisely rather than assuming.
Per parameter, the candidate set is `[baseline] + N uniform-random draws across the parameter's full
legal range` (`ConfigGenerator._generate_test_values_array`, `ConfigGenerator.py:520`), with
**`N = 10` by default** — `DEFAULT_TEST_VALUES` in `run_accuracy_simulation.py:66`, passed through at
`:460`, giving 11 candidates per parameter (`:440`). (Note `ConfigGenerator.__init__` carries its own
default of `5` (`ConfigGenerator.py:262`), which applies only to direct construction, not to the CLI path.) So the sweep is
**not** a local perturbation around the baseline — each parameter does explore its whole range. The
stale baseline still biases the result through three channels:

1. **Incumbency.** The baseline is a candidate and survives unless a random draw beats it. Ten
   uniform draws over a range like `ADP_SCORING_WEIGHT`'s `[0.5, 7.0]` is thin coverage, so a value
   that is decent by luck can persist.
2. **Coordinate ascent holds the others fixed.** While one parameter is swept, every other parameter
   sits at its baseline value (`AccuracySimulationManager`; the pass driver is `_run_ascent_pass`, `AccuracySimulationManager.py:529`, and the order is `self.parameter_order`, `:119`/`:308`). Sweeping `ADP_SCORING_WEIGHT`
   against a dead `TEAM_QUALITY_SCORING` measures something different from sweeping it against a live
   one.
3. **Order dependence.** Parameters are optimized sequentially in `parameter_order`, so early
   choices condition later ones.

Channel 2 is the significant one here, because Items B and E are precisely the parameters that were
dead or degenerate while everything else was tuned around them.

Mitigation: pass `--baseline` explicitly to a neutral or hand-set starting config for the first
post-change run, and treat the pre-change `optimal_*` folders as historical rather than as a
starting point. Worth deciding deliberately rather than inheriting the default.

### Consequence 3 — ordering

The re-tune has to come **after** the scoring fixes, and the fixes have to come after `sim_data` is
clean, or the tuning optimizes against corrupted inputs:

```
[0]  measure the accuracy sim's noise floor        (gates trusting anything below)
 |
Item A (bye fix)  ->  sim_data corrected / recompiled
 |
Items B1, B4, E   (dead / degenerate factors fixed)
 |
re-run accuracy sim from a DELIBERATE baseline  ->  promote new configs
 |
only then evaluate Items B2 / C against the new baseline
```

Step 0 comes first because it is cheap and it gates the credibility of everything below it. If the
accuracy sim cannot resolve the effect sizes involved, promoting its output is not tuning — it is
noise-adoption, which is exactly the failure `win_rate_similarity_investigation.md` documented for
the other harness.

Item D (display) is independent of all of this.

---

## Cross-cutting: should this be a new dimension at all?

Observations about the scoring architecture that bear on all five items.

**The chain is `normalized_projection × Π(base_i^WEIGHT_i) + bonus`.** Consequences:

- **Multiplicative factors compound and saturate.** ADP (1.109) × rating (1.216) is already
  ×1.348. Each added dimension makes every individual weight less interpretable and expands the
  sweep space multiplicatively — in a sweep that is already noise-dominated. *Argues for modifying
  existing dimensions (B1/B2, C2) over adding new ones (C1).*
- **Two of the eight factors are dials connected to nothing.** ADP is binary (§Item B) and team
  quality is `NEUTRAL` for everyone (§Item E), yet both carry swept `WEIGHT` parameters (2.12, 2.77).
  Before adding a dimension it is worth asking how many existing dimensions actually fire.
  *Argues strongly for fixing B and E before evaluating C's marginal value — C's benefit would
  otherwise be measured against a baseline that is itself broken.*
- **Bucketed multipliers destroy within-tier signal.** This is the direct cause of Item B and it also
  limits player rating (top tier holds 209 players). Any new bucketed dimension inherits the same
  flaw. *Argues that if C1 is chosen, it should be continuous, not 5-tier — even though that breaks
  convention.* Tension with the house pattern; worth an explicit decision.
- **The `+50` bonus is additive into a ~163-max normalized space** — measured, it is **18.5–20.3% of
  a top-5 score, 25% by pick 20, 30% by pick 50 and 40% by pick 100** — applied as a step function on
  position. It outweighs any single multiplier (the ADP factor moves a 163-base by ~17.8 points; the
  bonus moves it by 50), and it is currently the same value for PRIMARY and SECONDARY. Two
  consequences: a multiplicative risk factor is structurally the weaker signal, and because the
  bonus is a *fixed* 50 against a *shrinking* score, positional steering silently strengthens as the
  draft goes on. *Argues for revisiting the additive/multiplicative mix, which is really C4
  territory.*
- **Normalization is relative to the pool max, which is fixed for the session.** The best player in
  the *whole pool* scores exactly 163 pre-multiplier. `max_projection` is computed over
  `self.players` — **every** player, not the free-agent pool (`PlayerManager.py:350`) — so it does
  **not** move as players are drafted, and scores stay comparable across rounds within a session.
  (An earlier draft of this document claimed the opposite; it was wrong.) What it does mean is that
  scores are **not** comparable across datasets or seasons, since the denominator is whatever that
  file's best projection happens to be — relevant to choosing a risk factor's magnitude, and to any
  backtest that compares scores across the 2022–2025 seasons (§Validation approach).

**Where the five items sit on the effort/benefit map:**

| | Effort | Confidence it's wrong today | Behaviour change | New ESPN data |
|---|---|---|---|---|
| A — bye zeroing | Low | **Certain** (203 players measured) | Moderate, broad | None |
| B1 — ADP direction | Trivial | **Certain** (3 tiers unreachable) | **Larger than it looks** — splits today's single all-EXCELLENT block of 69 into E 17 / G 16 / N 19 / P 17 | None |
| B4 — reachability guard | Low | n/a (preventative) | None | None |
| B2 — continuous ADP | Medium | Design choice | **Large** — this is the risk signal | None |
| C — availability factor | Medium-High | Design choice | **Large** | None for v1 |
| *(re-tune)* accuracy + win-rate sims | Medium | n/a — the stated goal | Re-derives every swept value | None |
| D — displayed "pts" headline | Low | **Certain** (588.80 vs 355.83 measured) | None to ranking; **large to what the user reads** | None |
| E — team quality never populated | Low | **Certain** (0/799 measured) | **Large from ~week 11 on** (when ranks start discriminating); none at week 1 | None |

---

## Impact model (illustrative, not a proposal)

Applying an Item-A bye correction and a naive availability multiplier (games-with-points ÷ 16 over
5 seasons) to the round-1 three. **The availability model here is a strawman for magnitude only —
it makes none of the §Design questions decisions.**

| | raw ROS | bye-fixed | availability | risk-adj ROS | score now | score adj |
|---|--:|--:|--:|--:|--:|--:|
| McCaffrey | 355.8 | 334.2 | 73.8% | 246.5 | 269.72 | **202.20** |
| Gibbs | 322.2 | 303.5 | 95.8% | 290.9 | 248.96 | 229.61 |
| Bijan | 312.6 | 312.6 | 100% | 312.6 | 243.04 | **243.04** |

- **Today:** McCaffrey → Gibbs → Bijan
- **Item A alone:** McCaffrey → Bijan → Gibbs *(A alone already reorders the 2/3 slots)*
- **A + C:** **Bijan → Gibbs → McCaffrey** — full inversion

That the ordering is this sensitive is itself a finding: it means the current ranking's top is not
robust, and it raises the stakes on getting the availability model right rather than merely
present. A crude factor could be as wrong in the other direction.

---

## Open questions for the ticket-writing pass

1. Is week 18's exclusion from `get_rest_of_season_projection` (`range(current_week, 18)`) intended?
2. Do ESPN's own weekly projections already haircut for injury risk? If so, an availability
   multiplier double-counts. (Checkable: compare ESPN projection ÷ healthy-rate across known
   injury-prone vs iron-man players.)
3. How does the Item-A bye fix reach `simulation/sim_data/`? Neither A1 (fetch-time) nor A2
   (load-time) does — the sim loads via `SimDataLoader` → `PlayerManager.set_player_data()`. Options:
   recompile the five seasons, add a third fix site in the sim load path, or make Item C compute a
   bye-aware denominator itself. (§Item A → Options, §Design questions #4.)
4. Is the Bijan week-5 zero (non-bye) part of Item A or its own investigation? Needs the
   pool-wide sweep first.
5. If both B2 and C ship, which owns the injury-risk signal — and how is double-counting prevented?
6. Should the `_get_multiplier` machinery grow a continuous mode, or is the 5-tier convention worth
   preserving at the cost of resolution?
7. Is the recommendation headline (`588.80 pts`) meant to be a projection or an arbitrary-scale
   ranking score? (§Item D — the label and the co-displayed `Projected:` line contradict each other.)
8. Does restoring team quality (§Item E) change DST rankings materially, given the CSV path uses
   `get_team_dst_fantasy_rank` for DST while `get_team_defensive_rank` is what a naive JSON-path fix
   would attach?
9. What baseline should the first post-change accuracy-sim run start from, given the default is a
   config folder fitted to the broken chain (§Re-tuning workflow, consequence 2)?
10. **What is the accuracy simulation's noise floor?** Never measured. The whole re-tuning plan
    depends on it being able to distinguish configs, and the sibling harness demonstrably cannot.
    Run the fixed-config-repeat experiment before trusting promoted values.
11. Is the win-rate sim worth re-running at all before its noise-floor problem is addressed, or
    should the accuracy sim own config derivation for now?

---

## Artifacts

- `_internal/mock_drafts/mock_draft_slot01..10.{md,json}` — the 10-sim run that triggered this.
- `_internal/win_rate_similarity_investigation.md` — why the sweep cannot validate any of this yet.
- Key code sites:
  - `league_helper/add_to_roster_mode/AddToRosterModeManager.py:243`
  - `league_helper/util/PlayerManager.py:195, 262-357, 342, 350, 359-375, 959`
  - `league_helper/util/player_scoring.py:304-439, 429-436, 467-476`
  - `league_helper/util/ConfigManager.py:369, 734, 772-778, 1196-1256`
  - `league_helper/util/TeamDataManager.py:144-147, 343`
  - `league_helper/util/ScoredPlayer.py:52-83`
  - `player_data_fetcher/espn_client.py:484-527, 637-666, 678-722`
  - `player_data_fetcher/player_data_fetcher_main.py:181`, `player_data_fetcher/player_data_constants.py:31`
  - `utils/FantasyPlayer.py:150, 465-487`
- All measurements taken against `main` @ `97ee42e7` with `data/` byte-identical to that commit
  (2026 week-1 PPR, 799 players, `max_projection = 355.83`). Reproducible by checking out that
  commit and re-running; no live fetch required.
- **Provenance note.** The investigation began after a live re-fetch, and a first draft of this
  document mixed figures from that fetch (`max_projection` 355.81; McCaffrey ADP 6.36, Gibbs 1.79)
  with figures from the committed tree (McCaffrey 6.31, Gibbs 1.76) — ordinary intra-day ADP drift.
  The working tree subsequently returned to the committed state, and **every figure in this document
  has been re-derived on that single committed basis.** No conclusion depended on the difference:
  the ADP deltas are ~0.05 and both snapshots sit in the same (broken) ADP tier, and the phantom-bye
  values are identical to 2 d.p. Recorded because a reader reproducing these numbers against a
  *fresh* fetch will see small ADP drift and should not treat it as a discrepancy.

---

## Proposed ticket shape (for a later pass — not filed)

1. **Spike — measure the accuracy simulation's noise floor.** Cheap, independent of every code
   change, and it gates whether the re-tuning plan is meaningful at all. Same experiment
   `win_rate_similarity_investigation.md` ran on the other harness: re-evaluate one fixed config N
   times and compare that variance to the spread between candidate configs.
2. **Bug — bye-week projections not zeroed** (Item A). Self-contained, certain, blocks C.
3. **Bug — ADP threshold direction inversion + reachability guard** (Items B1 + B4). One-word config
   change, certain, but with a measured behavioural blast radius (69 players re-tiered) that needs
   its own test pass. The guard prevents recurrence across all **eight** threshold-based factors
   (ADP, player rating, team quality, matchup, schedule, performance, temperature, wind —
   `ConfigManager.py:370-448`).
4. **Spike/Story — continuous ADP curve** (Item B2). Design work; the first change that actually
   surfaces market risk.
5. **Bug — team quality never populated in the JSON load path** (Item E). Self-contained; restores a
   whole scoring dimension that is inert year-round. Needs a before/after check on DST, which uses a
   different rank accessor. **Sequenced before Item C deliberately** — see the note below.
6. **Story — availability/durability factor, v1 from `sim_data`** (Item C). Depends on #2 (bye data)
   and is best measured after #3 and #5. Needs the seven §Design questions answered and a backtest
   harness.
7. **Bug — displayed "pts" headline is a back-converted score, not a projection** (Item D).
   Presentation-only (ordering is unaffected), independent of the others, and needs a user decision
   on what the headline is meant to mean.
8. *(Deferred)* age as a durability covariate — gated on accepting a ~799-call second fetch pass.
9. *(Deferred)* risk-adjusted EV / distributional scoring (C4).

**Sequencing note.** Items B and E are each a dead or degenerate scoring dimension (§Cross-cutting).
Until they are fixed, the recommender's baseline is not the system as designed, and any measurement
of Item C's marginal value is taken against a broken reference. The cheap certain fixes (A, B1+B4, E)
should therefore land before the design work (B2, C) is evaluated — not because they are
prerequisites in a code sense, but because they change what "better" is measured against.

---
Validated 2026-08-03 — 6 rounds, 1 adversarial sub-agent confirmed (sha256:bd9c8b0609da5e33) (spike, re-validated)

---

## Downstream dependents (reverse edge — read before decomposing)

`spikes/scoring-scale.md` (continuous vs. bucketed scaling) declares **hard and soft dependencies on
this spike's items**, recorded here so the decomposition of *this* spike does not have to discover
them by reading the other one. Its own §"Interaction with spike 1" table is the authoritative
statement; this is the pointer:

| This spike's item | What scoring-scale needs from it |
|---|---|
| **B1** (ADP direction) | **Hard prerequisite.** Interpolation without the direction fix inverts ADP pool-wide, because bucketing's `val <= EXCELLENT` short-circuit is currently masking the bug by accident. |
| **B4** (reachability guard) | Should ship **before or alongside** — continuous scaling raises the cost of a bad config, so the guard becomes more valuable, not less. |
| **E** (team quality inert) | **Should land first.** No value in adding resolution to a factor returning `NEUTRAL` for everyone. |
| **B2** (continuous ADP curve) | **Largely subsumed** by interpolation; narrows to a cut point plus a flat tail. |
| **A** (bye zeroing) | Prerequisite for the **re-tune**, not for the code change — the accuracy sim reads `sim_data`, which carries the phantom-bye error. |
| **D** (display) | Independent. |

**Consequence for decomposition.** These are cross-*ticket* ordering constraints, which are legal and
normal — each emitted ticket records its own dependencies. What they must **not** become is a single
rollout spanning two tickets: per `reference/rollout_staging.md`, a rollout lives inside **one** ticket
so its partial order stays in one live record rather than spanning records that finalize independently.

---

## Decomposition

**Proposed: 8 delivery tickets; 6 emitted after the gate (see §Gate outcome).** Landing order below is the spike's own §"Consequence 3 — ordering",
which is a genuine constraint chain, not a preference: the noise-floor measurement gates whether any
re-tune output can be trusted; the bye fix must precede anything the accuracy sim validates; and the
two dead/degenerate factors must be live before the re-tune, or the optimizer tunes against a broken
chain (§Consequence 1).

| # | Ticket slug | Item | Scope (one line) | Declared touch-set |
|---|---|---|---|---|
| 1 | `accuracy-sim-noise-floor` | Step 0 | Re-evaluate one fixed config N times; compare that variance to the spread between candidates. Decides whether the accuracy sim can gate anything. | `run_accuracy_simulation.py`, `simulation/accuracy/AccuracySimulationManager.py`, `tests/simulation/` |
| 2 | `bye-week-phantom-projections` | A | Zero the bye-week projection at fetch (+ load), and settle whether `sim_data` is recompiled or fixed in its own load path. | `player_data_fetcher/espn_client.py`, `utils/FantasyPlayer.py`, `simulation/win_rate/SimDataLoader.py`, `league_helper/util/PlayerManager.py` |
| 3 | `adp-threshold-direction` | B1 | Flip `ADP_SCORING.THRESHOLDS.DIRECTION` to `DECREASING`, restoring the 5-tier ladder. Behaviour change, not cosmetic — re-tiers 69 players. | `data/configs/league_config.json` |
| 4 | `unreachable-tier-guard` | B4 | Validate at config load that all five tiers are reachable, across all eight `_get_multiplier` consumers. Decide warn vs raise. | `league_helper/util/ConfigManager.py` |
| 5 | `team-quality-inert-json-path` | E | Populate `team_offensive_rank` / `team_defensive_rank` in the JSON load path so the factor stops returning `NEUTRAL` for all 799. | `league_helper/util/PlayerManager.py`, `utils/FantasyPlayer.py`, `league_helper/util/player_scoring.py` |
| 6 | `projected-points-headline` | D | Stop presenting the back-converted score as `pts`; the headline is 1.65-1.69x any achievable total. | `league_helper/util/player_scoring.py`, `league_helper/util/ScoredPlayer.py` |
| 7 | `rescoring-retune-baseline` | re-tune | Re-run the accuracy sim from a **deliberate** baseline (not the default most-recent `accuracy_optimal_*`) and promote. | `data/configs/*`, `run_accuracy_simulation.py` (invocation only) |
| 8 | `availability-durability-factor` | C | The actual missing feature: an availability/durability dimension, v1 from `sim_data` at zero new API cost. | `league_helper/util/player_scoring.py`, `data/configs/league_config.json`, `simulation/shared/config_constants.py`, `league_helper/util/ScoredPlayer.py` |

**Landing order:** 1 -> 2 -> 3 -> 4 -> 5, with **6 unordered**. Acyclic.

### Gate outcome (2026-08-05) — 6 tickets emitted, not 8

The proposed 8 went to the user gate and came back **amended**. Two members were removed, and both
removals are recorded here because each drops something the spike had identified:

- **Ticket 7 (`rescoring-retune-baseline`) — DROPPED, not deferred.** Re-tuning becomes an
  operational step the user runs rather than tracked work. **Accepted consequence, stated so it is a
  decision and not a surprise:** §Consequence 2's trap is now **unowned**.
  `run_accuracy_simulation.py` defaults its baseline to the most recent `accuracy_optimal_*` folder
  (`find_baseline_config`, `:187-236`), and those folders are fitted to the broken chain this spike
  documents. A post-fix re-run that inherits that default starts coordinate ascent from values tuned
  against a dead team-quality factor and a binary ADP cliff. The mitigation — pass `--baseline`
  explicitly to a neutral or hand-set config — has to be remembered at the point of running, because
  no ticket now carries it.
- **Ticket 8 (`availability-durability-factor`) — PROMOTED to its own spike**, not dropped:
  `spikes/availability-durability.md`. Item C carries **four** competing architectural options
  (C1-C4, spanning a new chain step through to a full risk-adjusted-EV rewrite) and **seven** open
  design questions, several of which — the window, the rookie prior, and separating "injured" from
  "benched" — are genuine research rather than scoping. That is spike-shaped, not ticket-shaped, and
  filing it as one ticket would have pushed the research into `/dt3-design` where the alternatives
  are no longer visible as alternatives. Its content moves to the child spike; this spike keeps the
  evidence that motivated it.

**Consequence for the probe table below:** the five coupled pairs were computed over the proposed 8.
Three of them involved ticket 8 (`adp-threshold-direction`, `team-quality-inert-json-path` and
`projected-points-headline` each x `availability-durability-factor`) and are now **out of scope for
this decomposition** — they become the child spike's to re-probe against whatever ticket set it
emits, since its touch-set is no longer fixed. The two surviving coupled pairs are 2 x 5 and 5 x 6.
**Among the 6 emitted tickets, 13 of 15 pairs are `probed: independent`.**


### Emitted (2026-08-05)

| Ticket | Slug |
|---|---|
| `D2` | `accuracy-sim-noise-floor-unmeasured` |
| `D3` | `bye-week-phantom-projections` |
| `D4` | `adp-threshold-direction-inversion` |
| `D5` | `unreachable-multiplier-tier-guard` |
| `D6` | `team-quality-inert-in-json-load-path` |
| `D7` | `projected-points-headline-not-a-projection` |

Plus one **child spike**: `spikes/availability-durability.md` (Item C).
Landing order: `D2` -> `D3` -> `D4` -> `D5` -> `D6`, with `D7` unordered.

### Boundary rationale

- **B splits into two tickets (3 and 4), not one.** They have disjoint touch-sets (a config value vs
  a validation mechanism) and independent value: 3 fixes ADP, 4 prevents the whole class across all
  eight `_get_multiplier` consumers. The ordering is real though — a guard that *raises* would reject
  today's config, so 3 lands first (or 4 ships warn-only).
- **B2 (continuous ADP curve) is deliberately NOT a ticket here.** `spikes/scoring-scale.md` records
  it as **largely subsumed** by interpolation, narrowing to "how should the ADP tail be handled on
  top of interpolation?". Filing it now would emit a ticket whose scope is decided by a different
  spike. It is deferred to that spike's decomposition.
- **Item A's secondary anomaly** (Bijan's week-5 zero on a non-bye week) is **not** a ticket. The
  spike says it needs a pool-wide sweep of zero-valued non-bye weeks before anyone can say whether it
  is an ESPN omission, a parse miss, or real. That sweep is in ticket 2's scope; a ticket is filed
  only if it finds something.
- **The re-tune is its own ticket (7), not a step inside each fix.** It has a decision of its own —
  §Consequence 2's deliberate-baseline trap — and it is gated on 1-5 collectively. Folding it into
  any single fix would hide that decision.

### Downstream

`spikes/scoring-scale.md` has a **hard prerequisite on ticket 3** and ordering preferences on 4 and
5 (see §"Downstream dependents" above). Those are cross-*ticket* dependencies, which are legal; they
must not become a rollout spanning tickets.
