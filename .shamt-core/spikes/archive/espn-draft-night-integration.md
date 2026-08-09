# Spike: espn-draft-night-integration

**Created:** 2026-08-05   **Status:** Spike (investigation — unnumbered, transient)

> Transient investigation doc — NOT a ticket, NOT a design doc with a lifecycle.
> Archives to spikes/archive/espn-draft-night-integration.md once it has emitted its tickets.

## Ask

Our fantasy league has migrated from **NFL Fantasy** to **ESPN**. Improve the draft-night
experience of using the League Helper to aid our draft picks. Specifically: is there a way to
integrate with an API, or use a browser extension, to make it easier to keep track of the state
of the draft as it progresses?

Two distinguishable sub-asks are bundled here and the investigation must keep them separate:

1. **Platform migration** — the existing ownership-import path is NFL-Fantasy-shaped and is now
   dead for this league.
2. **Draft-night experience** — reduce the manual bookkeeping burden during a live draft and
   surface better in-the-moment decision support, regardless of platform.

## Findings

### F1 — The project already speaks ESPN; it is the *ownership/draft* path that is NFL-shaped

`player_data_fetcher/espn_client.py` already fetches projections from ESPN's hidden fantasy API
over `httpx`, including the **league-read host** used by league-scoped endpoints:

```
https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/{pprId}
```

(`espn_client.py:653`). Team/scoreboard data comes from `site.api.espn.com`. `ARCHITECTURE.md`
§Integration Points records these as **unauthenticated public endpoints**, with `ESPN_FIXTURE_DIR`
/ `ESPN_RECORD_FIXTURES_DIR` giving an offline fixture mode and committed fixtures under
`tests/fixtures/espn_api/`.

So the ESPN HTTP client, retry policy, fixture harness, and User-Agent handling **already exist**.
A league-scoped draft read is a new endpoint on an existing client, not a new integration.

### F2 — Player records already carry the ESPN player ID, which is the natural draft join key

`data/player_data/{qb,rb,wr,te,k,dst}_data.json` records carry `"id": "4429795"` — the ESPN player
ID — alongside `name`, `team`, `position`, and the **`drafted_by`** string that *is* the League
Helper's draft state. Example (`rb_data.json`, Jahmyr Gibbs):

```json
{ "id": "4429795", "name": "Jahmyr Gibbs", "team": "DET", "position": "RB",
  "drafted_by": "", "locked": false, "average_draft_position": 1.76, ... }
```

ESPN's draft-pick payloads identify picks by `playerId` + `teamId`. Because our records already
carry the same ID space, an API-sourced draft feed can join on **exact integer IDs** and skip
name matching entirely.

### F3 — The current ownership-import path is fuzzy-matched, NFL-Fantasy-shaped, and currently inert

- `nfl-fantasy-exporter-extension/` — a Manifest V3 Chrome extension whose `host_permissions` are
  `https://fantasy.nfl.com/*` only. It DOM-scrapes the "All Taken Players" table, clicking through
  the O / K / DEF position tabs and pagination, and downloads `drafted_data.csv` in the shape
  `"A.J. Brown WR - PHI View News","Pidgin"`.
- `utils/DraftedRosterManager.py` (641 lines) parses that CSV and matches each row back to a
  `FantasyPlayer` via a five-stage progressive strategy ending in `SequenceMatcher` fuzzy matching
  at a 0.75 threshold, plus a hand-maintained 32-entry NFL-team-name→abbreviation map duplicated
  across two methods, plus DST name-shape special cases.
- **Code consumers: `player_data_fetcher` only.** The module's own header records that
  `league_helper` has migrated to `PlayerManager.get_players_by_team()`; a `grep` for
  `DraftedRoster` across `league_helper/` returns no import. The fetcher constructs and loads the
  manager at `player_data_exporter.py:73-75` and applies the state at
  `player_data_exporter.py:135` (`apply_drafted_state_to_players`), preserving `drafted_by` across
  refetches.
- **Non-code consumers exist and are easy to miss** — the CSV *contract* outlives its last import:
  - `league_helper/trade_simulator_mode/TRADE_ANALYSIS_GUIDE.md` instructs the reader to
    `Read()`/`grep` `drafted_data.csv` directly for roster extraction at **seven** sites
    (lines 122, 131, 260, 270, 271, 635, 1118). Deleting the CSV path without updating this guide
    leaves live operator instructions pointing at a file that will never again exist.
  - `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:184-185` carries a
    comment justifying its team-name union on the grounds that a team may be "seeded out-of-band
    (DraftedRosterManager, from drafted_data.csv)" — a rationale that becomes false once ESPN is
    the seeding source.

  Both are in C-A's *contract* stage scope and are declared in its touch-set below. This is the
  finding that most changes the ingest ticket's shape: the migration is not "swap one importer",
  it is "retire a data contract that documentation and code comments still assume."
- `data/drafted_data.csv` **does not currently exist** on disk — the path is dormant.

Every piece of that machinery — the scraper's host permission, the CSV shape, the fuzzy matcher,
the team-name map — exists to bridge a name-only export. An ID-keyed feed removes the *reason*
for it, not merely its current implementation.

### F4 — Draft state in the League Helper is a per-player string, mutated one pick at a time by hand

`drafted_by` on each `FantasyPlayer` is the whole draft model:
`""` = free agent, our team name = ours, any other string = an opponent's.
`league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:153` (`_mark_player_as_drafted`)
is the opponent-pick entry point: search for a player, pick the drafting team from a list built
from `OPPONENT_TEAMS` in `data/configs/league_config.json` union'd with names already present in
the data, then set the field. Our own picks go through
`league_helper/add_to_roster_mode/AddToRosterModeManager.py`.

The project's own `draft-sim-test` skill documents the resulting draft-night workload: a 10-team,
15-round draft is **150 picks**, of which **135 are opponents'** and each one is a manual
search-and-select through the CLI. That is the burden the ask is about.

### F5 — The recommendation engine is roster-derived and has no concept of draft *position*

`AddToRosterModeManager._get_current_round()` derives the current round from **how many players we
have rostered**, and `get_recommendations()` applies `DRAFT_ORDER` bonuses for that round
(`league_config.json` carries a 15-entry `DRAFT_ORDER` of PRIMARY/SECONDARY position targets and
`DRAFT_ORDER_BONUSES` of 50/50).

Nothing in the system knows: the overall pick number, our draft slot, whether the draft is a snake,
how many picks until our next turn, or who is on the clock. Those are exactly the quantities that
make a live draft feed worth more than a state mirror — they enable "will this player survive until
our next pick?" reasoning that the current engine structurally cannot express.

### F6 — Config already carries the league's shape, but not its identity

`data/configs/league_config.json` has `OPPONENT_TEAMS` (nine hand-typed opponent names),
`NFL_SEASON: 2026`, `MAX_POSITIONS`, `DRAFT_ORDER`, and scoring parameters.
`league_helper/constants.py:19` hard-codes `FANTASY_TEAM_NAME = "Sea Sharp"`.

There is **no ESPN league ID, no team ID, and no credential handling anywhere in the project**.
`ARCHITECTURE.md` §Security Posture records that the project holds no credentials of its own and
that the Chrome extension "runs in the user's authenticated browser session… It holds no
credentials of its own." Any private-league API read changes that posture and must be treated as a
deliberate decision, not an implementation detail.

### F7 — The league is PRIVATE and drafts in ESPN's online draft room (user-confirmed)

Two answers settled during the dialog, and together they set the whole design frame:

- **Venue: ESPN's online draft room.** Every pick lands in ESPN's system in real time as it is
  made, so a live feed genuinely exists to consume. (Had the league drafted offline and loaded
  ESPN afterward, the entire API direction would have been dead on arrival — this was the first
  question asked for that reason.)
- **Visibility: private.** A league-scoped read therefore requires the `espn_s2` and `SWID`
  cookies from a logged-in ESPN session.

The privacy answer **directly contradicts the posture `ARCHITECTURE.md` §Integration Points
records** ("No authentication (public endpoints)") and §Security Posture ("holds no credentials of
its own"). Every ESPN call the project makes today is unauthenticated; a private-league read is
the first authenticated one. That is a documented-architecture change, not an implementation
detail, and it is the reason the transport question below is a genuine fork rather than a
preference:

- A **Python-side poll** must acquire, store, and scope two long-lived session cookies — a new
  credential-at-rest surface the project has never had.
- A **browser extension** runs *inside* the already-authenticated session and needs no credentials
  at rest at all — exactly the posture §Security Posture already ascribes to the existing NFL
  extension. Its cost is the delivery channel: getting data from the browser into the Python CLI.

### F8 — The candidate ESPN endpoint (to be probed, not assumed)

The league-scoped read is believed to be:

```
GET https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{leagueId}
    ?view=mDraftDetail&view=mTeam&view=mRoster
```

returning a `draftDetail` object with `drafted` / `inProgress` flags and a `picks[]` array of
`{playerId, teamId, roundId, roundPickNumber, overallPickNumber, keeper, autoDraftTypeId}`, plus
`teams[]` giving the fantasy team ID→name mapping needed to populate `drafted_by`.

**FULLY SETTLED — this section is retained as the original hypothesis, not as an open question.**
F9 confirmed the **route pattern** without credentials; **F11 confirmed the authorized response
body** with a live HTTP 200 against a real private league, including one structural detail this
hypothesis got wrong by omission (F11a's placeholder rows). Read F8 → F9 → F11 in order. It was
originally stated
here as a claim to be falsified against the live league before any ticket depends on it. See
Open Questions.

## Surface surveyed

| Area | Read | What it settled |
|---|---|---|
| `player_data_fetcher/espn_client.py` | endpoint/header/fixture structure | F1 — league-read host + fixture harness already present |
| `player_data_fetcher/{config,player_data_exporter,player_data_fetcher_main}.py` | drafted-data wiring | F3 — fetcher is the only `drafted_data.csv` consumer |
| `data/player_data/*.json` | record schema | F2 — ESPN `id` + `drafted_by` present |
| `utils/DraftedRosterManager.py` (641 L) | full read | F3 — fuzzy match + team map + DST special cases |
| `nfl-fantasy-exporter-extension/{manifest.json,README.md}` | full read | F3 — NFL-only host permission, DOM scrape, CSV shape |
| `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py` | mark-drafted flow | F4 — per-pick manual entry |
| `league_helper/add_to_roster_mode/AddToRosterModeManager.py` | recommendation flow | F5 — round derived from roster count |
| `league_helper/util/PlayerManager.py` | load/save paths | F4 — JSON is the durable draft state, atomic `.tmp` writes |
| `league_helper/constants.py`, `data/configs/league_config.json` | config surface | F6 — no league identity, no credentials |
| `.shamt-core/project-specific-files/ARCHITECTURE.md` | §Integration Points, §Security Posture, §Data Stores | F1/F6 — recorded posture: public endpoints, no credentials |
| `.claude/skills/draft-sim-test/SKILL.md` | draft-night workload | F4 — 150 picks, 135 manual |
| **Live ESPN `leagues/{id}?view=mDraftDetail`** | unauth 401/404 probe; authed 200 pre-draft; authed 200 mid-offline-draft | F9, F11, F13 — route, schema, placeholder grid, unstable `pickOrder`, in-progress state |
| **Live ESPN `leaguedefaults/3?view=kona_player_info`** | 300-player pull, ID cross-check | F14 — three-way `playerId` match + the `defaultPositionId`/`lineupSlotId` enum split |
| `player_data_fetcher/espn_client.py:1567-1568`, `player_data_exporter.py:116,244` | `id` provenance trace | F14 — ESPN player ID copied verbatim to disk |

### F9 — Route confirmed with no credentials (the authorized body was subsequently confirmed by F11)

Two probe requests (2026-08-05, no credentials) split F8's single premise into a confirmed half
and an open half:

```
GET .../seasons/2025/segments/0/leagues/1?view=mDraftDetail&view=mTeam
  → HTTP 401 {"type":"AUTH_LEAGUE_NOT_VISIBLE","message":"You are not authorized to view this League."}
GET .../seasons/2025/segments/0/leagues/999999999?view=...
  → HTTP 404 {"type":"GENERAL_NOT_FOUND","message":"Not Found"}
```

The endpoint **discriminates "exists but not visible" from "no such league"**, which a wrong path
could not do — so the route pattern `/seasons/{season}/segments/0/leagues/{leagueId}` is
**confirmed correct**, and ESPN returns structured JSON errors with a machine-readable `type` on
the failure paths (an error-handling affordance the ingest should consume rather than treating any
non-200 as opaque).

**Left open at the time, and since settled by F11:** the authorized 200 body — `draftDetail.picks[]`
carrying `playerId` / `overallPickNumber`, and `teams[]` carrying the id→name mapping. Both are now
**confirmed** against a live private league.

**The incremental-population premise — since NARROWED by F13, not fully closed.** F11 observed only
the *pre-draft* state (all placeholders). **F13 then observed incremental population directly**: an
in-progress draft with 3 of 160 picks filled and `inProgress: True`, on the same fields and the same
array. So "does `picks[]` fill in incrementally, and is the in-progress state observable?" is
**answered yes**.

What remains strictly unobserved is narrower: whether ESPN's **live online draft room** (the venue
SD1 records, `type: SNAKE`) populates identically to the **offline** commissioner path
(`type: OFFLINE`) F13 exercised. Same endpoint, same array, same fields — so the risk is low and
this is stated as residual rather than open. It is discharged either by C-D's rehearsal or by the
real draft itself; **no ticket boundary depends on it.**

### F10 — Testability is a first-class design constraint here, and it was initially missed

A draft is a **single, unrepeatable, time-boxed live event**. Unlike every other capability in this
project — where a wrong answer is re-runnable — draft-night ingest gets exactly one production
execution per season, under time pressure, with no rollback. Software that cannot be rehearsed
beforehand is software whose first real test *is* draft night.

**The project's existing harness covers less of this than it first appears.**

- `player_data_fetcher/espn_client.py` already has `ESPN_FIXTURE_DIR` / `ESPN_RECORD_FIXTURES_DIR`
  and a `_get_fixture_filename()` URL→filename mapping. That mapping **raises `ValueError` on an
  unmapped URL** (`espn_client.py:168-171`, *"No fixture filename defined for URL"*), so a new
  league-scoped endpoint is **not optional to add** — fixture support is a hard prerequisite of the
  client existing at all, not a follow-up.
- The project's own `draft-sim-test` skill already drives a **full 10-team / 15-round / 150-pick
  draft** end-to-end through the real CLI, with snapshot-and-rollback of `data/`. This is a
  substantial existing rehearsal rig — but it drives picks *manually* through the menus, which is
  precisely the path the ingest replaces. It tests the flow being retired.

**The gap a completed-draft fixture does not close.** A recorded finished draft tests *"parse a
completed draft."* It does not test what actually matters on the night: **incremental delta
application** — pick 47 arrives, state updates, recommendations re-rank, nothing double-applies,
nothing is lost across a dropped or duplicated poll, and a pick that arrives out of order is not
mis-attributed. Exercising that requires a feed that **changes between polls**.

The cheap way to get one, requiring no additional ESPN dependency: record **one** real completed
draft, then derive N successive fixture snapshots from it mechanically (`picks[0:1]`, `picks[0:2]`,
… `picks[0:150]`) and replay them as a time series. One recording yields a fully deterministic,
offline, replayable draft night — including adversarial variants (a stalled poll, a duplicated
pick, a gap) that a live rehearsal cannot reliably produce on demand.

**What a dummy league is and is not needed for.** A throwaway ESPN league the user owns is needed
**twice**: once to prove the private-league authenticated read works with real `espn_s2`/`SWID`
against a league they control, and once to produce the real recording everything else derives from.
It should **not** be a standing dependency — day-to-day development, CI, and regression runs must
execute against fixtures with zero network and zero credentials, matching the posture
`ARCHITECTURE.md` §Integration Points already records for every other ESPN call.

**~~No additional ESPN accounts should be required.~~ FALSIFIED 2026-08-05 — see F12.** This
section originally asserted that ESPN autodrafts teams with no owner, so a 10-team league with one
claimed team would draft itself. **That is wrong.** ESPN refuses to start a draft until the league
is full. The expectation was recorded as an expectation rather than a fact precisely so that being
wrong would cost one observation instead of a redesign — which is what happened. F12 records the
corrected path; the staged plan below survives with stage 2's *mechanism* replaced.

**Uncertain, flagged rather than assumed** (each resolvable by observation, none load-bearing for
the split):

| Unknown | Why it does not block | How it gets answered |
|---|---|---|
| ~~Can a draft start with 9 unclaimed teams?~~ | — | **ANSWERED: NO** (F12). Fallback ladder in F12b |
| Does commissioner *offline draft* entry populate `draftDetail.picks[]` or only rosters? | Ladder rungs 2 and 3 remain (F12b) | **Now the decisive open test** — Q-offline-draft |
| ~~Is ESPN's *mock draft lobby* API-visible under a real `leagueId`?~~ | — | **MOOT** — superseded by F12b's ladder, which needs no mock lobby |
| ~~Can a commissioner reset a completed draft to rehearse repeatedly?~~ | — | **ANSWERED: YES**, ESPN documents draft reset (F12), pending UI confirmation |

**Staged dummy-league plan — each stage is independently valuable, so a failure at stage 2 does
not waste stage 1. Stage 2's mechanism was replanned by F12; the staging itself survives.**

1. **Create the league; do not draft it; probe immediately.** Requires no additional accounts and
   settles the highest-value unknowns: that the `espn_s2`/`SWID` pair authenticates, that `teams[]`
   carries the id→name mapping, and what `draftSettings` holds. It also captures the
   **pre-draft/undrafted league state** — which is *not* a throwaway: it is exactly the state the
   helper is in when opened before the draft begins, and the ingest must handle it gracefully.
   **This stage alone unblocks most of C-A's provision unit.**
2. **Populate a draft and re-probe — mechanism per F12b's ladder** (Offline Draft entry if
   Q-offline-draft confirms it reaches `draftDetail`; otherwise a 4-team live draft; otherwise
   synthesis over the F11 envelope). Yields the pick recording that C-A's fixture time-series and
   C-D's rehearsal scenarios derive from.

Ladder rung 3 is always available as a floor: a `picks[]` array authored over the **real**
`teams[]` / `draftSettings` / placeholder-grid envelope captured at stage 1 remains a sound
fixture — the surrounding structure is genuine ESPN output, and only the `playerId` sequence is
synthesized. **This is why the dummy league was never a hard blocker for C-A, C-B, or C-C.**

### F11 — F8 CONFIRMED against a live private league, with one trap that would have bitten on draft night

Probed 2026-08-05 against a user-created 10-team private league (`seasonId=2026`), authenticated
with `espn_s2` + `SWID`. **HTTP 200.** Every structural premise F8 asserted is confirmed:

- `draftDetail` present, keys `{drafted, inProgress, picks}` — `drafted: False`, `inProgress: False`
- `picks[]` rows carry `playerId`, `teamId`, `roundId`, `roundPickNumber`, `overallPickNumber`,
  `lineupSlotId`, `keeper`, `reservedForKeeper`, `autoDraftTypeId`, `bidAmount`,
  `nominatingTeamId`, `tradeLocked`, `id`
- `teams[]` carries `id` → `name` (plus `abbrev`, `owners`, `primaryOwner`) — the `drafted_by`
  mapping F2 depends on is real
- `settings.draftSettings`: `type: SNAKE`, `timePerSelection: 90`, `pickOrder: [1…10]`
- `settings.rosterSettings.lineupSlotCounts` gives the roster shape;
  `status` carries `isFull`, `teamsJoined`, `activatedDate`

**SD2 is confirmed empirically:** the authenticated read works, so the credential-handling design
is load-bearing rather than hypothetical.

#### F11a — `picks[]` is PRE-ALLOCATED with placeholder rows before the draft starts

**All 160 picks are present before a single selection has been made, every one with
`playerId: -1`.** The array is a fully-formed 16-round × 10-team grid of empty slots.

This is the single most valuable thing the probe found, because the obvious implementation is
wrong in a way that fails silently and catastrophically:

| Naive signal | What it reports pre-draft | Consequence |
|---|---|---|
| `len(picks)` | 160 — "the draft is complete" | Marks 160 phantom players drafted; `drafted_by` garbage across the whole player pool |
| `if picks:` | truthy | Same |
| **`sum(1 for p in picks if p['playerId'] != -1)`** | **0 — correct** | Correct progress count |
| `draftDetail.drafted` / `.inProgress` | `False` / `False` — correct | Correct state gate |

The ingest **must** filter on `playerId != -1` (and gate on `drafted`/`inProgress`), never on array
length or truthiness. This is a required correctness behaviour of C-A's cutover unit and a named
scenario for C-D, not an optimization.

#### F11b — Snake geometry is served by the API, not something C-B must derive

Round 1's `teamId` sequence is `[1,2,3,4,5,6,7,8,9,10]`; round 2's is `[10,9,8,7,6,5,4,3,2,1]`.
ESPN **pre-computes the reversal** — every pick's owning team, round, and overall number is stated
in the placeholder grid before the draft begins.

C-B therefore *reads* the draft geometry rather than reconstructing it from `pickOrder` plus a
snake rule. **Picks-until-our-next-turn is a filter over the served grid**, not a
derivation, which materially shrinks C-B. C-B should still validate the served order rather than
trust it blindly, but the reconstruction logic is not needed as the primary path.

> **Qualified by F13b — read them together.** The grid is served, but it is **not stable**: the
> pick order was observed changing when the draft was configured. "Served, not derived" holds;
> "captured once" does not. Every consumer re-reads.

#### F11c — Round count is league configuration and must not be hardcoded

The probed league has **16 rounds / 160 picks** (`lineupSlotCounts` = QB1, RB2, WR2, TE1, FLEX1,
D/ST1, K1, + 7 bench + 1 IR = 16 roster slots). The **real** league's config
(`data/configs/league_config.json`) has a 15-entry `DRAFT_ORDER` and `MAX_POSITIONS` summing to
**15**. The two do not match.

Two consequences: (1) nothing in the ingest may assume 15 rounds or 150 picks — round count is
derived from the payload; (2) **the dummy league's roster settings must be edited to mirror the
real league (drop one bench slot → 15 rounds)** before the stage-2 recording, or the fixture corpus
will encode a 160-pick draft that the real season never produces.

#### F11d — `timePerSelection: 90` bounds the poll budget

Ninety seconds per pick sets the latency target: a poll interval materially above ~10s risks the
helper's recommendations lagging the board by a full pick. This is a concrete, sourced number for
C-C's poll design rather than a guess.

### F12 — ESPN blocks a draft until the league is full; the unblock is Offline Draft, not dummy accounts

**Observed by the user, 2026-08-05:** ESPN will not run a draft in a league that is not full. This
**falsifies F10's autodraft-the-empty-teams expectation** outright. The nine unclaimed "Team N"
entries that were enough to *create and probe* the league (F11) are not enough to *draft* it.

Two constraints found while re-checking rather than re-guessing:

- **ESPN's minimum league size is 4 teams**, not 10 ([League Types – ESPN Fan
  Support](https://support.espn.com/hc/en-us/articles/115003927611-League-Types)). A live-draft
  fallback therefore needs **3** additional accounts, not 9.
- **ESPN supports an Offline Draft mode** (LM Tools → Edit Draft Settings), where the commissioner
  enters every pick by filling roster slots directly — no live draft, and the full-league
  requirement does not apply ([Offline Draft – ESPN Fan
  Support](https://support.espn.com/hc/en-us/articles/360000140891-Offline-Draft)).
- **ESPN documents resetting a draft** ([Edit Draft Type, Date, Order and/or Reset the Draft – ESPN
  Fan Support](https://support.espn.com/hc/en-us/articles/360000085851-Edit-Draft-Type-Date-Order-and-or-Reset-the-Draft)),
  which resolves F10's "can a completed draft be rehearsed again?" uncertainty in the affirmative,
  pending UI confirmation.

#### F12a — The one thing that must be tested next, and why it is decisive either way

**Does commissioner Offline Draft entry populate `draftDetail.picks[]` with real `playerId`s, or
does it only write rosters (`mRoster`) and leave the placeholder grid at `-1`?**

This was already flagged uncertain in F10 and is now on the critical path. It is a ~5-minute test:
switch the dummy league to Offline Draft, enter **two or three** picks, re-probe, and read the
`playerId != -1` count from F11a's check.

Both outcomes are valuable, which is what makes this the right next action:

| Outcome | Consequence |
|---|---|
| **`picks[]` populates** | Best case, and *better than a live draft*: the commissioner enters picks **one at a time, pausably**, probing between each. That is a hand-cranked incremental feed — exactly the delta-application rig F10 says a completed-draft fixture cannot provide — with **zero** extra accounts and full control over out-of-order and stalled-poll scenarios |
| **`picks[]` stays `-1`** | Also important: it means an offline draft is **invisible to `mDraftDetail`**, so the ingest must not assume the endpoint sees every draft type. Falls back to the ladder below |

#### F12b — The fallback ladder, in preference order

1. **Offline Draft in the existing 10-team league** — 0 extra accounts, pausable.
   ~~Contingent on F12a.~~ **CONFIRMED AVAILABLE by F13 — this is the selected rung; rungs 2 and 3
   below are retained as documented fallbacks, not as planned work.**
2. **A 4-team live draft** — 3 additional ESPN accounts (email `+` aliases). Exercises the genuine
   live in-progress path. Team and round counts differ from production, which **F11c already
   requires the ingest to tolerate**, so a 4-team observation is a sound live-behaviour probe even
   though it is not a production-shaped fixture.
3. **Synthesize `picks[]` over the real captured envelope** — assign real ESPN player IDs (already
   present in `data/player_data/*.json`, orderable by `average_draft_position`) into the **genuine**
   160-row placeholder grid captured in F11. Only the `playerId` values are synthetic; teams,
   rounds, overall numbers, lineup slots, and the snake reversal are all real ESPN output.

**The two purposes decouple, and should.** Observing *live incremental population* needs **a** real
draft of any size (ladder 1 or 2). A production-shaped **fixture corpus** does not need a real draft
at all (ladder 3, over the F11 envelope). Conflating them is what made the dummy league look like a
hard blocker; separated, ladder 3 alone unblocks C-A, C-B, and C-C, and only C-D's live-behaviour
rehearsal depends on 1 or 2.

### F13 — Offline Draft DOES reach `draftDetail`; ladder rung 1 confirmed; and the pick grid is NOT stable

**Q-offline-draft answered YES**, probed 2026-08-05 after the user set the dummy league to
`draftSettings.type: OFFLINE` and entered three round-1 picks:

```
drafted / inProgress : False / True          <- the in-progress state IS observable
total picks          : 160
picks with playerId  : 3                     <- 157 still at -1
  overall 1  teamId 1  playerId 4429795  lineupSlotId 2
  overall 5  teamId 2  playerId 4430807  lineupSlotId 2
  overall 6  teamId 3  playerId 4426515  lineupSlotId 4
```

**F12b ladder rung 1 is available**, and it is better than a live draft for our purposes: the
commissioner advances the draft **one pick at a time, pausably**, and the endpoint reflects each
entry. That is a hand-cranked incremental feed — the exact delta-application rig F10 said a
completed-draft recording cannot provide — with **zero additional ESPN accounts**. It also makes
`inProgress: True` reproducible on demand, which no completed-draft fixture can offer.

#### F13a — The `playerId` join is confirmed end-to-end, not merely structurally

All three drafted `playerId`s resolve against this project's own `data/player_data/*.json`:

| overall | teamId | playerId | resolved locally | ADP |
|---|---|---|---|---|
| 1 | 1 | 4429795 | Jahmyr Gibbs, RB, DET | 1.76 |
| 5 | 2 | 4430807 | Bijan Robinson, RB, ATL | 2.68 |
| 6 | 3 | 4426515 | Puka Nacua, WR, LAR | 3.69 |

F2 asserted the ID spaces match; this **proves** it against live draft output. The fuzzy
name-matching machinery F3 describes is now demonstrably unnecessary for this path, which
strengthens C-A's *contract* stage rather than merely justifying it.

`lineupSlotId` also agrees with position (2 = RB, 4 = WR), giving a free cross-check the ingest can
assert on.

#### F13b — `pickOrder` CHANGED between probes: the placeholder grid is NOT stable

This is the second trap the probes have caught, and it partially qualifies F11b.

| | `pickOrder` | round-1 `teamId` sequence |
|---|---|---|
| F11 (pre-draft-setup) | `[1,2,3,4,5,6,7,8,9,10]` | `[1,2,3,4,5,6,7,8,9,10]` |
| F13 (after draft setup) | **`[1,4,9,6,2,3,10,8,5,7]`** | **`[1,4,9,6,2,3,10,8,5,7]`** |

The order was **randomized when the draft was configured**. The initial sequential order F11
captured was a pre-configuration default, not the real order — which is why F11's three picks land
at overall **1, 5, 6** rather than 1, 2, 3.

Consequences, all load-bearing:

- **The grid must be re-read, never cached across the draft-setup boundary.** Any `pickOrder` or
  team→slot mapping captured before the commissioner finalizes the draft is **stale and wrong**. A
  helper that snapshots the order at startup and reuses it will mis-attribute every pick.
- **C-B's "validate the served order rather than trust it" recommendation is vindicated** — but the
  validation must be *freshness*, not just internal consistency. Both grids above are internally
  consistent snake orders; only one is current.
- **F11b still holds in substance** (geometry is served, not derived — round 2 remains the exact
  reverse of round 1: `[7,5,8,10,3,2,6,9,4,1]`), but its "already in hand" phrasing must not be read
  as "capturable once."
- **Our own draft slot is not a config constant.** `FANTASY_TEAM_NAME` / `teamId` identifies *which
  team* we are; *where we pick* is league state that can change until the draft locks. C-B must
  resolve slot from the live payload, and C-A's config surface should carry `teamId`, **not** a
  draft position.

### F14 — The `playerId` join is proven across all three surfaces, and the provenance is code-verified

F13a showed draft `playerId`s resolving against our on-disk JSON. That alone leaves open whether
our `id` field is *genuinely* ESPN's player ID or something that happened to match. It is genuinely
ESPN's, established two ways:

**Code provenance.** `espn_client.py:1567-1568` reads `player_info = player.get('player', {})` then
`id = str(player_info.get('id', ''))` — ESPN's player-object ID copied verbatim, no derivation and
no synthetic key. `player_data_exporter.py:116` (`id=player_data.id`) and `:244` (`"id": player.id`)
carry it unchanged to disk.

**Live three-way match**, probed 2026-08-05 against the **same projections endpoint the fetcher
calls** (`leaguedefaults/3?view=kona_player_info`, `espn_client.py:653-663`):

| playerId | draft endpoint (`mDraftDetail`) | projections endpoint (`kona_player_info`) | our `data/player_data/*.json` |
|---|---|---|---|
| 4429795 | pick overall 1 | Jahmyr Gibbs | Jahmyr Gibbs, RB, DET |
| 4430807 | pick overall 5 | Bijan Robinson | Bijan Robinson, RB, ATL |
| 4426515 | pick overall 6 | Puka Nacua | Puka Nacua, WR, LAR |

**The join is sound and durable** — same provider, same ID space, same season, ID copied verbatim
through the pipeline. C-A's *contract* stage is therefore removing machinery that is **provably
redundant on this path**, not merely currently unused.

#### F14a — `defaultPositionId` and `lineupSlotId` are DIFFERENT enums; do not conflate them

Observed in the same comparison:

| player | `defaultPositionId` (projections) | `lineupSlotId` (draft pick) | actual position |
|---|---|---|---|
| Jahmyr Gibbs | 2 | 2 | RB |
| Puka Nacua | **3** | **4** | WR |

RB coincides at 2; **WR does not** (position 3 vs slot 4). Any ingest code that treats a draft
pick's `lineupSlotId` as a position ID — or reuses one lookup table for both — will mis-position
every WR and, by extension, corrupt FLEX and positional-scarcity reasoning. The two enums need
separate mappings, and the cross-check F13a suggested (assert pick slot agrees with known position)
must translate between them rather than compare raw integers.

Note also that `proTeamId` is a **numeric** team ID (Gibbs = 8, Robinson = 1, Nacua = 14), not the
`"DET"` / `"ATL"` / `"LAR"` abbreviations our JSON stores — a third mapping the ingest needs if it
ever reads team from the API rather than joining on `playerId` alone. Joining on `playerId` avoids
all three mappings, which is a further argument for the ID join over any attribute-based match.

## Resolved design decisions

| # | Decision | Consequence |
|---|---|---|
| SD1 | League drafts in **ESPN's online draft room** | A live pick feed genuinely exists to consume; the API direction is viable |
| SD2 | League is **private** | Reads need `espn_s2` + `SWID`; contradicts the recorded "no authentication / no credentials" posture |
| SD3 | **The CLI stays the cockpit** | No overlay, no second-screen dashboard. The existing scoring engine, `DRAFT_ORDER` bonuses, and `run_league_helper.py` entry point are preserved; what changes is that opponent picks stop being hand-entered |
| SD4 | **Python polls ESPN directly** | Extends `espn_client.py` rather than building a browser bridge. Reuses the existing httpx client, retry policy, and `ESPN_FIXTURE_DIR` harness. Accepts two secrets at rest on the user's machine as the explicit cost |
| SD5 | **Fixture time-series replay lands inside the ingest ticket; a separate ticket owns end-to-end rehearsal** | Fixture mapping is a hard prerequisite of the client (`espn_client.py:168-171` raises on an unmapped URL), and tickets C-B/C-C are untestable without a replayable feed — so replay cannot be deferred to a later ticket. Full draft-night rehearsal (re-pointing `draft-sim-test`) is genuinely separable and lands last, as C-D |

| SD6 | **`espn_s2` / `SWID` live in the existing `.env`**, read via `os.environ` | Conforms to an established house convention rather than inventing a fifth config mechanism — see the evidence below. C-A owns wiring the loader, expiry detection, and a loud mid-draft 401 |

**SD6 evidence — the convention already exists and C-A conforms to it** (Global Story Invariant:
*codebase pattern discovery* — emulate the nearest established shape, do not invent):

- `python-dotenv>=1.0.0` is **already declared** in `requirements.txt`, under the comment
  "Environment and configuration".
- **`.env` already exists**, is **gitignored** (`.gitignore:153`), and is **not present anywhere in
  git history** (`git ls-files` + `git log --all -- .env` both empty).
- It **already carries a secret** — `ACCU_WEATHER_API_KEY` — so secrets-in-`.env` is an existing
  precedent in this project, not a new posture.
- `os.environ` is the established read idiom, used at **10 production sites across 5 modules**
  (`schedule_data_fetcher/ScheduleFetcher.py` ×3, `player_data_fetcher/espn_client.py` ×3,
  `historical_data_compiler/http_client.py` ×2, `player_data_fetcher/config.py`,
  `league_helper/LeagueHelperManager.py`) — reading `ESPN_FIXTURE_DIR`,
  `ESPN_RECORD_FIXTURES_DIR`, `LEAGUE_DATA_DIR`, `PLAYER_DATA_DIR`. Tests excluded from the count.

**Two consequences C-A must own, recorded so they are not mistaken for free:**

1. **Nothing currently loads `.env`.** There is **no `load_dotenv()` call anywhere** in the
   codebase, and `ACCU_WEATHER_API_KEY` is read by nothing — `python-dotenv` is a **declared but
   unused** dependency. C-A is the *first real consumer* and must wire the loader, decide its
   invocation point, and keep `os.environ` precedence over the file so CI and fixture runs override
   cleanly.
2. **`.env` sits inside the repo tree**, so it remains recoverable from backups and one
   `git add -f` from a commit. Accepted deliberately: the convention already exists, the file is
   already ignored and never-committed, and `chmod 600` is a cheap mitigation. An
   outside-the-repo location was considered and **rejected as convention divergence**, not on
   security grounds.

**A dummy ESPN league is a two-time input, not a standing dependency.** It is needed once to prove
the authenticated read against a league the user controls, and once to produce the single real
recording every fixture derives from. Development, CI, and regression runs execute offline against
committed fixtures with no credentials — the posture `ARCHITECTURE.md` §Integration Points already
records for every other ESPN call.

SD3 + SD4 together **eliminate the browser-extension direction** for this work. The existing
`nfl-fantasy-exporter-extension/` is therefore not ported — it is decommissioned (see C-A below).

## Candidate directions

### C-A — ESPN draft-state ingest: migrate the ownership source from NFL scrape to ESPN API

**One rollout, therefore one ticket** (per the hard decomposition rubric): stand up the ESPN
league read alongside the existing CSV path, cut the consumers over to it, then remove the NFL
path. Splitting these across tickets would strand the codebase in a half-migrated state with two
ownership sources live.

- *provision* — league-scoped authenticated read (`?view=mDraftDetail&view=mTeam`), credential
  config (gitignored), league/team identity in config, recorded fixtures.
- *cutover* — `picks[]` → `drafted_by` by **exact `playerId` join** (F2, proven end-to-end in F14),
  ESPN `teamId` → fantasy team name reconciled against `OPPONENT_TEAMS` + `FANTASY_TEAM_NAME`;
  `player_data_fetcher` reads ESPN instead of `drafted_data.csv`. **Carries four probe-found
  correctness requirements, each of which fails silently if missed:**
  - **F11a** — filter `playerId != -1`; never gate on `len(picks)` or truthiness, because the grid
    is fully pre-allocated before the draft.
  - **F13b** — re-read the pick grid; never cache it across the draft-setup boundary.
  - **F14a** — `defaultPositionId` and `lineupSlotId` are **different enums** (WR is 3 vs 4); keep
    separate mappings and translate before comparing.
  - **F14a** — `proTeamId` is numeric, not the `"DET"`-style abbreviation stored on disk; joining
    on `playerId` alone avoids needing that mapping at all.
- *contract* — retire `nfl-fantasy-exporter-extension/`, `utils/DraftedRosterManager.py`, the
  `--drafted-data-path` CLI surface, and the dead fuzzy-match/team-name-map machinery; update
  `ARCHITECTURE.md` §Integration Points + §Security Posture for the now-authenticated call.

**Declared touch-set:** `player_data_fetcher/espn_client.py`, new
`player_data_fetcher/espn_league_client.py`, `player_data_fetcher/player_data_exporter.py`,
`player_data_fetcher/player_data_fetcher_main.py`, `player_data_fetcher/config.py`,
`run_player_fetcher.py`, `utils/DraftedRosterManager.py` (deleted),
`nfl-fantasy-exporter-extension/` (deleted), `data/configs/league_config.json`, `.gitignore`,
new `.env.example` (key names only, no values — the committed record of what `.env` must supply,
since `.env` itself is correctly never committed),
`tests/fixtures/espn_api/`, `tests/utils/test_DraftedRosterManager.py` (deleted),
`tests/player_data_fetcher/*`, `tests/integration/*`,
`tests/fixtures/league/drafted_data.csv` (deleted — the last surviving copy of the retired CSV),
`league_helper/trade_simulator_mode/TRADE_ANALYSIS_GUIDE.md`,
`league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py` (comment only),
`.shamt-core/project-specific-files/ARCHITECTURE.md`.

**Also inside this ticket, per SD5:** the `_get_fixture_filename()` mapping entry for the new
league endpoint (mandatory — the client raises without it), a recorded real-draft fixture, and the
**time-series replay** capability that derives successive `picks[0:N]` snapshots from that one
recording. C-B and C-C are untestable until this exists, which is why it cannot be deferred.

### C-B — Draft-position model + position-aware recommendations

Closes the F5 gap: the engine currently derives "round" from *our roster count* and knows nothing
about the draft's actual geometry.

**Re-sized by F11b — this ticket is smaller than it first appeared.** ESPN *serves* the geometry:
the placeholder grid already states every pick's owning team, round, and overall number, with the
snake reversal pre-computed. So C-B does **not** reconstruct snake ordering from `pickOrder` plus a
rule — it **reads** it, and *picks-until-our-next-turn is a filter over the served grid*.

**But re-qualified by F13b: the grid is not stable, so "reads it" means reads it *afresh*.** The
order was observed changing between probes when the commissioner configured the draft. What remains
genuinely new:

- **Reading the served geometry from the current payload on every evaluation** — never from a
  startup snapshot, a cached config value, or a value captured before the draft was configured.
- **Freshness validation, not merely internal-consistency validation.** F13b is explicit that this
  distinction is the whole point: *both* observed grids were internally consistent snake orders
  (round 2 correctly reversing round 1), and a `pickOrder` + `roundId` parity check passes on the
  stale one. Consistency cannot detect staleness; only re-reading can. A parity check is still
  worth keeping as a corruption guard — it is simply **not** the defence against F13b's failure.
- **Identifying which team is ours** (`teamId`), which no current config records — see F6. Per
  F13b, config carries `teamId` (**who** we are, stable) and never a draft slot (**where** we pick,
  league state that moves until the draft locks).
- **The survival estimate** — "will this player still be there at our next pick?", derived from
  `average_draft_position` against the picks-until-next-turn count. This is the actual analytical
  content of the ticket and the thing that turns a state mirror into decision support.
- **Feeding both into the existing `DRAFT_ORDER` bonus path** so recommendations become
  position-aware in the real draft's terms rather than our roster count's.

**Declared touch-set:** `league_helper/add_to_roster_mode/AddToRosterModeManager.py`,
new `league_helper/util/draft_position.py`, `league_helper/util/ConfigManager.py`,
`data/configs/league_config.json`, `league_helper/constants.py`,
`tests/league_helper/add_to_roster_mode/*`,
`tests/league_helper/util/test_ConfigManager_draft_order_bonus.py`,
new `tests/league_helper/util/test_draft_position.py`.

### C-C — Live draft cockpit: auto-refreshing CLI mode

The UX payoff of SD3. A League Helper mode that polls the ingest on an interval, applies pick
deltas to in-memory state, re-renders recommendations without re-navigating menus, and shows the
live board (who is on the clock, recent picks, our turn countdown). Removes the ~135 manual
opponent-pick entries the `draft-sim-test` skill documents (F4).

**Declared touch-set:** `league_helper/LeagueHelperManager.py`,
new `league_helper/live_draft_mode/`, `league_helper/add_to_roster_mode/AddToRosterModeManager.py`,
`league_helper/util/PlayerManager.py`, `league_helper/constants.py`,
new `tests/league_helper/live_draft_mode/*`.

### C-D — Draft-night rehearsal: re-point the existing end-to-end harness at the ESPN path

The project's `draft-sim-test` project skill already drives a full 10-team / 15-round / 150-pick
draft through the real CLI with snapshot-and-rollback of `data/` — but it drives every pick
**manually through the menus**, i.e. it exercises the exact path C-A retires and C-C replaces. This
ticket re-points it at the ESPN-sourced path and adds the adversarial scenarios a live rehearsal
cannot produce on demand: a dropped poll, a duplicated pick, an out-of-order arrival, a mid-draft
restart, and an expired-credential mid-draft failure.

Lands **last**, because it verifies the assembled behaviour of C-A + C-B + C-C. It is separable
from all three: its touch-set is the skill body and integration tests, not production modules.

**Declared touch-set:** `.shamt-core/project-specific-files/skills/draft-sim-test/SKILL.md`,
new `tests/integration/test_draft_night_e2e.py`, `tests/fixtures/espn_api/` (replay scenarios),
`tests/integration/` helpers.

## Open Questions

- ~~**Q-probe**~~ — **CLOSED 2026-08-05 by F11.** Probed live, HTTP 200, every structural premise
  confirmed, plus the F11a placeholder trap the doc would otherwise have shipped into every ticket.
- **Q-dummy-league — stage 1 CLOSED; stage 2 REPLANNED after F12.** Stage 1 is done: the league
  exists and probes successfully (F11). Stage 2's original mechanism (autodraft the empty teams) is
  **falsified** — ESPN blocks a draft until the league is full (F12). Replanned per F12b's ladder,
  with **Q-offline-draft below as the deciding test**. Carries one prerequisite from F11c
  regardless of ladder rung: *edit the dummy league's roster settings to 15 slots to mirror the
  real league before recording*, or the fixture corpus encodes a draft shape the real season never
  produces. **RECLASSIFIED — this is no longer an open question but a recorded input C-A's
  provision unit consumes:** its answer cannot change the artifact (the ladder rung is chosen, the
  mechanism confirmed by F13), only supply data to the ticket. Carried forward as C-A work.
- ~~**Q-offline-draft**~~ — **CLOSED 2026-08-05 by F13: YES.** Offline Draft entry populates
  `draftDetail.picks[]` and exposes `inProgress: True`. Ladder rung 1 is available (0 extra
  accounts, pausable one-pick-at-a-time feed). The probe additionally caught F13b's unstable
  `pickOrder` — a second would-have-bitten defect.
- ~~**Q-credential-lifecycle**~~ — **CLOSED 2026-08-05 → `.env`, per SD6 below.** The residual
  operational items (rotate the conversation-exposed pair; detect expiry; surface a mid-draft 401
  loudly rather than stalling the poll, inside F11d's 90-second pick clock) are **C-A design
  content**, not open questions.

## Decomposition

### Confirmed split — 3 delivery tickets (user-gated 2026-08-05)

| # | Slug | One-liner |
|---|---|---|
| 1 | `espn-draft-ingest` | Migrate the ownership/draft source from the NFL scrape to the authenticated ESPN league API (provision → cutover → contract), incl. fixture mapping + time-series replay |
| 2 | `live-draft-cockpit` | **C-B + C-C merged.** Read the served draft geometry afresh (`teamId`, picks-until-next-turn, ADP survival estimate) **and** the polling CLI mode that applies pick deltas and re-renders recommendations without menu navigation |
| 3 | `draft-night-rehearsal` | Re-point `draft-sim-test` at the ESPN path; add dropped-poll / duplicate-pick / out-of-order / mid-draft-restart / expired-credential scenarios |

**Landing order: 1 → 2 → 3.** Stated, strictly linear, acyclic.

**The C-B + C-C merge is a user decision at the gate, and the probe evidence supports it.** The
pair probed `coupled` at **hop 1** on two shared modules (`AddToRosterModeManager.py`,
`league_helper/constants.py`) — the tightest coupling of any pair in the original set. The split
had been argued on *standalone value* (the survival estimate helps even with no live feed) and
*differing risk profiles* (pure analytics vs a long-running poll loop); the user judged the shared
module surface to outweigh both. Recorded here as the durable reason rather than silently
re-drawn. Consequence: the merged ticket's **unit set** carries the analytics/presentation
separation that would otherwise have been a ticket boundary — the distinction survives one
altitude down rather than being lost.

**Candidate directions C-B and C-C above are left as written.** They are the investigation record
of what was *discovered*; this section records what was *emitted*. Candidates are not tickets, and
rewriting history to match the outcome would destroy the reasoning the doc exists to preserve.

### Independence probes — recorded outcomes (`reference/project_separability_test.md`)

**Every pair probed. The honest result: NO pair is independent. The independence claim is
DROPPED and replaced by an explicit total ordering**, per the protocol's instruction to state the
ordering dependency rather than assert an independence that fails.

**Probed on the emitted 3-ticket set** (the original 4-way probe table is preserved below it,
since the merge was decided *after* those probes and their evidence is what justified it):

| Pair | Hop 1 — touch-set intersection | Hop 2 — cross-referenced symbol | Outcome |
|---|---|---|---|
| 1 ↔ 2 | `data/configs/league_config.json` (distinct keys), `league_helper/constants.py` | 2 consumes 1's ingest payload and its `drafted_by` writes | `probed: coupled — shared config + payload dependency, hop 1` |
| 1 ↔ 3 | `tests/fixtures/espn_api/`, `tests/integration/*` | 3 replays 1's recorded fixtures | `probed: coupled — shared fixture corpus, hop 1` |
| 2 ↔ 3 | none | 3 drives 2's poll loop and asserts its geometry behaviour under replay | `probed: coupled — 3 exercises 2, hop 2` |

*Pre-merge 4-way probe (retained as the evidence behind the merge decision):*

| Pair | Hop 1 | Hop 2 | Outcome |
|---|---|---|---|
| C-A ↔ C-B | `league_config.json` | C-B consumes C-A's payload | `probed: coupled, hop 1` |
| C-A ↔ C-C | none | C-C polls C-A's client + applies its writes | `probed: coupled, hop 2` |
| C-A ↔ C-D | `tests/fixtures/espn_api/`, `tests/integration/*` | C-D replays C-A's fixtures | `probed: coupled, hop 1` |
| **C-B ↔ C-C** | **`AddToRosterModeManager.py`, `constants.py`** | C-C renders C-B's estimate | **`probed: coupled, hop 1` — the tightest pair; merged at the gate** |
| C-B ↔ C-D | none | C-D asserts C-B's behaviour | `probed: coupled, hop 2` |
| C-C ↔ C-D | none | C-D drives C-C's loop | `probed: coupled, hop 2` |

### Why 3 ordered tickets rather than 1 — the rubric applied, not asserted

Total coupling raises the fair challenge: *if nothing is independent, should this be one ticket?*
No — and the distinction is **deliverability, not independence**:

- **The hard rubric bars splitting ONE rollout across tickets**, because that strands the codebase
  in a broken half-migrated state. Ticket 1 is itself a complete provision → cutover → contract
  rollout and is **kept whole** — its three stages become its unit set, never separate tickets.
- **Tickets 2 and 3 are not stages of ticket 1's rollout.** They are subsequent capabilities built
  on its finished state. After each of 1, 2, and 3, the system is coherent, shippable, and more
  useful than before — there is no intermediate broken state to strand.
- **Ordering is not a rubric violation.** The delivery track records dependency notes and a
  Sequencing & Parallelization ordering precisely because ordered tickets are expected; the thing
  the rubric forbids is a *rollout* spanning tickets, which this split does not do.

### Rationale for the boundaries

- **1 is bounded by the rollout rule** — the ESPN read, the `drafted_by` cutover, and the NFL-path
  retirement cannot separate without two live ownership sources (F3, F14).
- **2 merges analytics and presentation** (user-gated). The analytics/presentation distinction is
  real and survives as 2's **unit boundary** rather than a ticket boundary: the geometry + survival
  model is independently valuable even with no live feed, and the poll loop carries failure modes
  the model has none of. Merged because the pair shares two modules at hop 1 — the tightest
  coupling in the set.
- **3 is last by necessity** — it verifies the assembled behaviour of 1 + 2, and its touch-set is
  the skill body and integration tests, not production modules.
- **SD5 keeps fixture replay inside 1**, not in 4: `espn_client.py:168-171` raises on an unmapped
  fixture URL, so fixture support is a prerequisite of the client existing, and 2 and 3 are
  untestable without a replayable feed.

### Risk note carried into ticket 1

The four probe-found silent-failure defects (F11a placeholder rows, F13b unstable grid, F14a enum
split, F14a numeric `proTeamId`) all land in ticket 1's cutover unit. Each fails **without an
error**, which is the class that would surface only on draft night.

---
Validated 2026-08-05 — 10 rounds, 1 adversarial sub-agent confirmed (sha256:d7e11cce2e99cb5f) (spike Step 2.5 — pre-decomposition)
