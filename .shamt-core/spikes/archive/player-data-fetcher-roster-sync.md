# Spike: player-data-fetcher-roster-sync

**Created:** 2026-08-05   **Status:** Spike (investigation — unnumbered, transient)

> Transient investigation doc — NOT a ticket, NOT a design doc with a lifecycle.
> Archives to spikes/archive/player-data-fetcher-roster-sync.md once it has emitted its tickets.

## Ask

Update the **player data fetcher** to use the same ESPN league integration being built for draft
night (`spikes/archive/espn-draft-night-integration.md` → tickets **D17** / **D18** / **D19**), so
that a fetch run can read the **current state of the fantasy teams** from ESPN and set the local
player data accordingly — which players are assigned to which fantasy teams.

The reuse is deliberate and explicit: the authenticated league client, the `.env` credential
handling, the league/team identity config, and the `ESPN_FIXTURE_DIR` recorded-fixture harness are
all provisioned by **D17**; this work adds a *different read* and a *different reconciliation
semantic* on top of that same foundation rather than standing up a second integration.

## Findings

### F1 — Draft picks are a frozen append-log; roster membership is mutable state. D17 delivers the first and cannot express the second

**D17's read is `?view=mDraftDetail&view=mTeam&view=mSettings`** (`tickets/D17-espn-draft-ingest/ticket.md`
§Scope). `draftDetail.picks[]` is an **immutable record of one night**: it is written once, never
amended, and — as the parent spike's F11a records — pre-allocated as a fixed grid whose rows only
ever transition from `playerId: -1` to a real ID.

Nothing in that array can express any of the three ownership changes that dominate the *rest* of
the season:

| Event | Effect on real ownership | Effect on `picks[]` |
|---|---|---|
| Waiver / FA add | player gains an owner | **none** — never appears |
| Drop | player returns to the free-agent pool | **none** — his draft pick row still names the drafting team |
| Trade | player changes owner | **none** — the pick row still names the *original* drafter |

So `drafted_by` seeded from draft picks is correct for exactly one evening and monotonically
decays thereafter. The **current team state** the ask names lives behind a different view
(`mRoster`), and reading it is a distinct capability rather than one more `&view=` on D17's call.

**The lifetime framing is inverted from how the initiative reads.** The draft is a single night;
the fetcher runs **every week of the season**. Roster sync is therefore the *dominant* lifetime
path of the ESPN league integration, and the draft ingest is the one-night special case that
happens to be built first because D19's rehearsal and D18's cockpit depend on it.

### F2 — The application seam already exists, is single, and is the same one D17 targets

`DataExporter.get_fantasy_players()` (`player_data_fetcher/player_data_exporter.py:131-137`) is the
**one** place external ownership state is applied to freshly-fetched players:

```python
fantasy_players = [self._espn_player_to_fantasy_player(player) for player in data.players]
fantasy_players = self.drafted_roster_manager.apply_drafted_state_to_players(fantasy_players)
return fantasy_players
```

Every position export funnels through it (`_export_single_position_json` calls it per position).
D17 replaces what sits on the right-hand side of that second line; this work changes *which ESPN
read* feeds it and *how the result is reconciled*. **The seam itself needs no new architecture** —
which is what makes the ask a fetcher change rather than a new subsystem.

### F3 — Everything the roster read needs is provisioned by D17; the delta is one view and one semantic

D17's declared scope already stands up: the authenticated league-scoped client on the existing
`espn_client` infrastructure, `espn_s2` + `SWID` in `.env` via `os.environ` with a wired
`python-dotenv` loader, league ID + our `teamId` in config, the `_get_fixture_filename()` mapping
for the league endpoint, and the recorded-fixture harness.

This work reuses **all** of it. Its delta is:

1. a `view=mRoster` read (same host, same league ID, same credentials, same retry policy), and
2. a **reconciliation semantic that D17 does not have** (F4).

That is a hard dependency, not a preference — **this work cannot precede D17** and is not
independent of it.

### F4 — The design crux: a roster read is an AUTHORITATIVE SNAPSHOT, and snapshots must DELETE

This is the finding that makes the work a separate design problem rather than a parameter change.

- A **pick feed** is additive. Applying it can only ever *set* `drafted_by`. A bug leaves state
  stale, never wrong-in-the-destructive-direction.
- A **roster snapshot** is authoritative. Applying it correctly requires the converse operation:
  a player present on no roster **must be reset to `drafted_by: ""`**. Without that, a drop is
  invisible and the helper keeps treating a now-available player as owned — which is precisely
  the free-agent recommendation the user most wants.

So the roster sync is the **first ownership write in this project that deletes state**, and every
failure mode inverts accordingly: a partial or mis-parsed roster payload does not under-apply, it
**mass-clears the league**. That asymmetry (a naive `len()`/truthiness read wipes ownership rather
than fabricating it) is the direct analog of the parent spike's F11a trap, and it needs the same
class of explicit guard — a sanity floor on the snapshot before any clear is applied.

### F5 — A full fetch ALREADY destroys local state today, and `locked` is destroyed unconditionally

Traced through the fetch write path:

- `espn_client.py:1722` constructs every `ESPNPlayerData` with `drafted_by=""`.
- `player_data_exporter.py:103` sets `locked_value = 0` **unconditionally**, and `:251` writes
  `"locked": bool(player.locked)` into the JSON.
- The fetcher reads **nothing** back from the existing `data/player_data/*.json` — a grep for
  merge/preserve logic across `player_data_fetcher/` finds it only in `game_data_fetcher.py`
  (week-level CSV resumption), never in the player export path.

Consequences, both load-bearing:

1. **`drafted_by` survives a fetch only because an external source re-supplies it.** The fetcher
   has no preservation property of its own — `DraftedRosterManager` is not a merge step, it is a
   re-seed. So switching that seed from CSV to ESPN (D17) or to ESPN rosters (this work) does not
   *remove* a preservation guarantee, because there never was one. This materially de-risks the
   authority decision below.
2. **`locked` is wiped on every single fetch run, and nothing re-supplies it.** No source — not
   the CSV, not `mDraftDetail`, not `mRoster` — carries it, because it is a purely local concept
   (`PlayerManager.update_player_data_files` writes it; `get_players_by_criteria(unlocked_only=…)`
   and the drop-candidate logic at `PlayerManager.py:765` read it). This is a **pre-existing
   data-loss defect in the fetch path, independent of ESPN**, sitting squarely inside this work's
   blast radius. It is not caused by the roster sync — but the roster sync is the change that
   makes "what does a fetch preserve?" an answered question rather than an unexamined one.

### F6 — The join key is already proven; no new matching machinery is needed

The parent spike's F14 established the `playerId` join across three surfaces and code-verified the
provenance (`espn_client.py:1567-1568` copies ESPN's player-object `id` verbatim; the exporter
carries it unchanged to disk at `player_data_exporter.py:116` / `:244`). ESPN's roster entries
identify players by the
same `playerId`, so the roster reconciliation joins on **exact integer IDs** — no name matching, no
team-abbreviation mapping, and none of the fuzzy machinery D17 retires.

The parent spike's **F14a caveat carries across in form**: a roster entry's `lineupSlotId` is a
*slot* enum, not the `defaultPositionId` *position* enum (WR is 3 vs 4), so any use of roster slot
data must translate rather than compare raw integers. **RD2 then makes it inapplicable in
practice** — no slot data is read or stored, so the enum is never touched on this path. It is
recorded here because it becomes live again the moment RD2 is revisited, not because C-A must
handle it.

### F7 — `teamId` → fantasy-team-name reconciliation is shared with D17, not re-derived

Both reads need the same `mTeam`-sourced `teamId` → `name` mapping reconciled against
`OPPONENT_TEAMS` in `data/configs/league_config.json` and `FANTASY_TEAM_NAME` in
`league_helper/constants.py`. D17 owns building that reconciliation for the pick feed; this work
**reuses** it (Global Story Invariant: *codebase pattern discovery* — reuse the shared helper
rather than fork it). A second, parallel mapping would be the defect, not the deliverable.

### F8 — The CLI/config surface this work inherits is D17's, not today's

`run_player_fetcher.py:78-87` exposes `--load-drafted-data` / `--drafted-data-path`, threaded
through `PlayerDataFetcherSettings` (`player_data_fetcher_main.py:74-78, 124-126, 174-176`) and a
pre-flight existence check at `:556-567`. **D17 retires all of it.** This work therefore designs
its trigger surface against D17's post-state, and any design that reads as "add a flag beside
`--drafted-data-path`" is reasoning against a surface that will not exist.

**Discharged by RD4 — recorded so this finding has a stated home rather than sitting as unhomed
context.** RD4 makes the roster sync unconditional, so this work adds **no** CLI option of its own.
Its only business in these two files is *removal*: whatever ownership-source plumbing survives
D17's retirement (the `load_drafted_data` / `drafted_data_path` fields threaded through
`PlayerDataFetcherSettings` and the pre-flight check, to the extent D17's own contract stage leaves
any residue) goes with C-A's contract stage. If D17 lands cleanly and leaves none, this reduces to
a no-op verification rather than an edit — which is the outcome to expect, not a scope gap.

### F9 — The `mRoster` payload shape is a HYPOTHESIS here, not a confirmed observation

The parent spike confirmed `mDraftDetail` and `mTeam` empirically (F11, F13) by probing a real
private league. **This spike has probed nothing**: the roster read is *believed* to be

```
GET .../seasons/{season}/segments/0/leagues/{leagueId}?view=mRoster&view=mTeam
  → teams[].roster.entries[] of {playerId, lineupSlotId, acquisitionType, playerPoolEntry.player{…}}
```

but that is stated as a claim to be falsified, exactly as F8 of the parent spike was before F11
confirmed it. `.env` currently carries only `ACCU_WEATHER_API_KEY` (key names checked; no ESPN
credentials present), so no live probe was available in this session.

**This does not block the split, and it is recorded as residual rather than open**, for the same
reason the parent spike's ladder-3 argument gave: the probe is a ~5-minute read against the dummy
league D17 already provisions, both outcomes are cheap, and **no ticket boundary depends on the
answer** — a differently-shaped roster payload changes the parsing inside the ticket, not which
tickets exist. It is discharged by the ticket's own design stage, which has the credentials D17
puts in place.

### F10 — The "abort to protect existing files" guard RD1 needs already exists as a house pattern

`player_data_fetcher_main.py:579-584` already refuses to write when a fetch comes back implausibly
thin:

```python
if total_players < MIN_EXPECTED_PLAYER_COUNT:          # = 100, :39
    logger.error(f"Insufficient player data: only {total_players} players collected "
                 f"(minimum {MIN_EXPECTED_PLAYER_COUNT}). Aborting to protect existing files.")
    sys.exit(1)
```

So the sanity floor RD1 requires is **not a new idea in this codebase** — the *posture* (refuse the
whole run and exit non-zero rather than write a degraded snapshot over good data), the log shape,
and the module-level named-constant threshold are all established. Per the Global Story Invariant
on **codebase pattern discovery**, C-A emulates this shape rather than inventing a parallel one.

**But it emulates the posture, not the mechanism — and the distinction is the whole point of F10.**
The existing guard is a **count threshold**, which is sound for projections because a healthy fetch
always returns hundreds of players. It is exactly the wrong shape for rosters, because RD5's
ordinary pre-draft run legitimately returns **zero** rostered players and must proceed. A roster
floor copied from this one would refuse every pre-draft run; a roster floor that simply drops the
threshold would wave through the mass-clear it exists to stop. What transfers is *abort-to-protect
+ exit non-zero + named constant*; what does not is *compare a count to a number*.

## Surface surveyed

| Area | Read | What it settled |
|---|---|---|
| `spikes/archive/espn-draft-night-integration.md` | full read | F1/F3/F6/F7 — what D17 provisions, the proven `playerId` join, the F11a/F13b/F14a traps |
| `tickets/D17-espn-draft-ingest/ticket.md` | full read | F1/F3/F8 — D17's exact view set (`mDraftDetail`/`mTeam`/`mSettings`, **no** `mRoster`) and its retirement list |
| `player_data_fetcher/player_data_exporter.py` | constructor, `get_fantasy_players`, `_espn_player_to_fantasy_player`, `_export_single_position_json`, JSON assembly | F2/F5 — the single application seam; `locked_value = 0`; full-rewrite export |
| `player_data_fetcher/espn_client.py` | `_get_fixture_filename`, fetch methods, `:1722` | F3/F5/F6 — fixture harness, `drafted_by=""` on construction, verbatim `id` |
| `player_data_fetcher/player_data_fetcher_main.py`, `run_player_fetcher.py` | drafted-data settings + pre-flight check; `MIN_EXPECTED_PLAYER_COUNT` guard at `:39` / `:579-584` | F8 — the CLI surface D17 retires; **F10** — the established abort-to-protect-existing-files guard |
| `utils/DraftedRosterManager.py` | `apply_drafted_state_to_players` | F5 — a re-seed, not a merge; no preservation property |
| `league_helper/util/PlayerManager.py` | `update_player_data_files`, `get_players_by_criteria`, `get_players_by_team`, drop-candidate logic | F5 — `locked` is local-only with real consumers |
| `league_helper/util/FantasyTeam.py` | `drafted_by` writes | F5 — league_helper mutates ownership locally between fetches |
| `player_data_fetcher/` (grep: merge/preserve/existing) | sweep | F5 — no read-back of existing player JSON anywhere in the player export path |
| `.env` (key names only) | key-name listing | F9 — no ESPN credentials present; no live probe possible this session |

## Resolved design decisions

| # | Decision | Consequence |
|---|---|---|
| RD1 | **ESPN is authoritative — full replace.** Every fetch rewrites `drafted_by` from the roster snapshot; a player on no roster is reset to `""` | Drops, adds and trades all propagate automatically (the ask's actual value). Requires the F4 delete path and a **sanity floor** guarding it. A hand-edited local ownership value is overwritten — acceptable because F5 proves the fetcher never preserved one anyway |
| RD2 | **Ownership only.** `drafted_by` is the sole synced field; no `roster_slot` / IR / acquisition-type data lands | No player-JSON schema change, no `lineupSlotId` enum mapping needed on the write path (F14a's caveat becomes inapplicable rather than merely handled), and nothing ships without a consumer. Slot detail stays a future ticket if a consumer ever appears |
| RD3 | **`locked` preservation is folded into this work** (user decision at the gate) | The fetch write path gains a defined preservation contract: ESPN owns `drafted_by`, the existing on-disk JSON owns `locked`. Cost, accepted: the F5 wipe stays live until this ticket lands behind D17, rather than being fixed sooner as a standalone bug |
| RD4 | **Rosters are the fetcher's only ownership source** — always, no flag, no mid-draft branch | One rule, no special cases, and the pick→`drafted_by` application D17 installs in the fetcher is **retired** by this work (the *contract* stage of its rollout). The pick feed survives where it is genuinely needed — D18's live cockpit, which needs pick geometry rosters structurally cannot provide (overall pick number, who is on the clock, picks until our turn) |

### RD5 — Operating assumption: the fetcher runs BEFORE and AFTER a draft, never during

**User-stated 2026-08-05**, and it retires what was recorded a moment earlier as RD4's residual
risk. That risk was the unprobed premise that ESPN populates `teams[].roster` *during* a draft
rather than only at its completion — a premise RD4 depended on because "always the rosters" would
otherwise be wrong for any run that landed mid-draft.

Under RD5 **no such run exists**, so the premise is not merely low-risk, it is **inapplicable**.
Three consequences:

1. **The mid-draft probe is dropped** from C-A's required design-stage checks. Only F9's
   `mRoster` payload-shape probe remains.
2. **The `inProgress` guard drops from a correctness requirement to an optional assertion.** It is
   no longer defending against a real operating mode. It is still cheap and still worth a design-
   stage call — as an *assumption-enforcing* check (refuse and say why, rather than silently apply
   a snapshot taken mid-draft) — which keeps RD5 visible in code rather than living only here.
3. **The `drafted`/`inProgress` flags stop being a source-selection switch** in the fetcher
   entirely, which is what makes RD4's "one rule, no special cases" literally true rather than
   true-modulo-a-branch.

**One interaction RD5 makes load-bearing, and it cuts against RD1's sanity floor.** "Before the
draft" is a legitimate, expected run in which **every roster is empty and the correct result is
that every player is a free agent**. That is indistinguishable, by count alone, from the
mass-clear failure the sanity floor exists to reject. So the floor **cannot** be a bare
"too few rostered players ⇒ refuse": it must separate *a league that has legitimately drafted
nobody* from *a payload that failed to parse*, using the league's own state (the `drafted` flag, a
successfully-parsed `teams[]` with rosters genuinely present-but-empty) rather than a threshold on
the rostered-player count. Getting this wrong in either direction is a real defect: too strict and
the ordinary pre-draft run refuses; too loose and RD1's delete path erases a drafted league. This
is named as a C-A cutover requirement below.

## Candidate directions

### C-A — ESPN roster-state sync in the player data fetcher

**One rollout, therefore one ticket** (per the hard decomposition rubric): stand up the roster
read, cut the fetcher's ownership source over to it, then retire the pick-based application path
D17 leaves in the fetcher. Splitting these across tickets would strand the fetcher with two live
ownership writers — the precise state F1 and RD4 exist to prevent.

- *provision* — a `view=mRoster&view=mTeam` league read on D17's authenticated client; the
  `_get_fixture_filename()` mapping entry for it (**mandatory, not deferrable** — the client raises
  `ValueError` on an unmapped URL at `espn_client.py:168-171`, so fixture support is a prerequisite
  of the read existing at all); recorded fixtures covering a populated in-season league, plus the
  derived offline scenarios the reconciliation must survive (a drop, a trade, a waiver add, an
  empty/partial payload).
- *cutover* — roster entries → `drafted_by` by exact `playerId` join (F6), `teamId` → fantasy team
  name via **D17's existing reconciliation helper, reused not forked** (F7), applied at the single
  `DataExporter.get_fantasy_players()` seam (F2). Carries **three correctness requirements — each
  of which fails destructively rather than loudly — plus one optional assertion**:
  - **RD1's delete path** — a player on no roster is reset to `""`. This is the first ownership
    write in the project that deletes state (F4).
  - **A sanity floor gating that delete** — a partial, empty or mis-parsed roster payload must
    refuse to apply rather than mass-clear the league. The failure direction is inverted from
    D17's: where a naive pick read *fabricates* ownership (F11a), a naive roster read *erases* it.
    **The floor must be state-based, not count-based** — per RD5, an ordinary pre-draft run
    legitimately yields zero rostered players and must apply cleanly, so the floor discriminates on
    the league's own `drafted` flag and on rosters being *parsed-and-empty* rather than on a
    threshold over the rostered count. **Emulates F10's established abort-to-protect-existing-files
    posture** (refuse the run, log, exit non-zero, threshold in a module-level named constant) —
    the posture, explicitly not its count-comparison mechanism.
  - **`locked` preservation** (RD3) — read the existing `data/player_data/*.json` back and carry
    `locked` forward, since nothing external supplies it (F5). Note this makes the exporter a
    *merge* writer for the first time; it is a pure full-rewrite today. Two traps the design stage
    owns: the read-back must resolve through the **same** `position_json_output` path the write
    uses (constructor-resolved at `player_data_exporter.py:45-53`, deliberately not a def-time
    default — see the T91 comment there), and it must tolerate **absent** files, since a first-ever
    fetch has nothing to read back.

  Plus one optional assertion:

  - **An `inProgress` assertion** (design-stage call) — refuse-and-explain rather than apply a
    snapshot taken mid-draft, keeping RD5's operating assumption visible in code. Demoted from a
    correctness requirement by RD5, which makes the mid-draft run non-existent.
- *contract* — retire the pick→`drafted_by` application D17 installs in the fetcher, leaving the
  pick feed to D18's cockpit; update `ARCHITECTURE.md` §Data Flow (the fetcher now reads its
  existing output back before writing) and §Integration Points (the fetcher's ownership source is
  the roster view, not the draft view).

**Declared touch-set:** `player_data_fetcher/espn_client.py` (roster read + fixture mapping),
`player_data_fetcher/espn_league_client.py` (**forward reference** — the new league-client module
D17's rollout is expected to create; named by the parent spike's C-A touch-set but not yet on disk
and not named in D17's own ticket, so treat it as "D17's league client, wherever it lands" and
**extend** it rather than fork a second client),
`player_data_fetcher/player_data_exporter.py` (the seam, the reconciliation, the `locked` read-back),
`player_data_fetcher/player_data_fetcher_main.py`, `run_player_fetcher.py`,
`player_data_fetcher/config.py`, `data/configs/league_config.json`,
`tests/fixtures/espn_api/`, `tests/player_data_fetcher/*`, `tests/integration/*`,
`.shamt-core/project-specific-files/ARCHITECTURE.md`.

**Required design-stage check** (carried into `/dt3-design`, cheap, with credentials D17 provides):
probe the live `mRoster` payload to discharge **F9**'s hypothesis. The mid-draft roster-population
probe that sat here is **dropped** — RD5 makes a mid-draft fetch run non-existent, so the question
is inapplicable rather than unanswered.

### Candidates considered and NOT emitted

Recorded so a later reader sees they were weighed rather than missed:

- **`locked`-preservation as a standalone ticket.** Genuinely separable on value (it is a live bug
  with no ESPN dependency) and was offered as its own ticket at the gate; the user chose to fold it
  in (RD3). Its touch-set intersects C-A's at `player_data_exporter.py` — hop 1 — so the merge is
  consistent with the independence evidence as well as with the decision.
- **Roster-slot / IR / acquisition-type ingest.** Ruled out by RD2 — no consumer exists in
  `league_helper`, so it would ship unused. Revisit only when a consumer does.
- **A roster-change diff report.** Subsumed by RD1's full-replace choice, which declined the
  reviewed-diff option. Cheap to add later inside the ticket if the silent rewrite proves
  uncomfortable in practice.
- **An in-season sync rehearsal harness**, mirroring D19's argument for draft night. Not emitted:
  D19 is separable because it verifies the *assembled* behaviour of three tickets and its touch-set
  is a skill body plus integration tests. There is only one ticket here, and its own
  `/dt4-decompose` unit set and `/dt5` ticket-scope test plan already own its verification — a
  separate rehearsal ticket would duplicate them rather than add coverage.

## Open Questions

- ~~**Q-authority**~~ — **CLOSED at the gate → RD1**, ESPN authoritative, full replace including the
  free-agent reset.
- ~~**Q-state-scope**~~ — **CLOSED at the gate → RD2**, ownership only.
- ~~**Q-locked**~~ — **CLOSED at the gate → RD3**, folded into this work rather than emitted as its
  own ticket or deferred.
- ~~**Q-source**~~ — **CLOSED at the gate → RD4**, rosters are the fetcher's only ownership source.
- ~~**Q-mid-draft-rosters**~~ — **CLOSED 2026-08-05 by RD5**, and closed by *elimination* rather
  than by answer: the user stated the fetcher only ever runs before and after a draft, so whether
  ESPN populates rosters mid-draft no longer bears on anything. The probe is dropped, the
  `inProgress` guard is demoted to an optional assertion, and the question's one surviving
  consequence — that a legitimate pre-draft run has zero rostered players and must not trip the
  sanity floor — is carried into C-A's cutover requirements.
- **Q-roster-payload — RECLASSIFIED, not open.** F9's `mRoster` shape is a hypothesis, not an
  observation, and this session had no credentials to probe with. It cannot change the artifact —
  only the parsing inside the one emitted ticket — so it is carried as a **required design-stage
  check** on C-A rather than a question blocking decomposition, exactly as the parent spike carried
  its stage-2 dummy-league input into D17.

## Decomposition

### Proposed split — 1 delivery ticket

| # | Slug | One-liner |
|---|---|---|
| 1 | `espn-roster-state-sync` | Make the ESPN team rosters the player data fetcher's authoritative ownership source — read `mRoster` on D17's league client, reconcile `drafted_by` by `playerId` join including the free-agent reset, preserve the local `locked` flag across the write, and retire the pick-based ownership write D17 leaves in the fetcher |

**A one-ticket outcome is the honest result here, not a degenerate one.** The spike was still worth
running: it produced ten findings, four user-gated design decisions plus one operating assumption,
and — most consequentially — it moved the work's shape from *"add `&view=mRoster` to D17's call"*
(how the ask reads) to *"the fetcher's first state-deleting write, guarded"* (F4/F10/RD5). None of
that was visible before the codebase was surveyed, which is exactly what a spike is for.

### Why one ticket and not several — the rubric applied, not asserted

The obvious 2- or 3-way splits were each considered and each fails the **hard rollout rubric**:

- *"Read first, cut over second"* — provisioning the roster read without cutting the fetcher over
  to it ships a live read nothing consumes; cutting over without retiring D17's pick-based write
  leaves **two live ownership writers** racing on the same field, which is precisely the
  half-migrated state the rubric exists to prevent. Provision → cutover → contract is **one
  rollout**, so it is one ticket's **unit set**.
- *"`locked` preservation as its own ticket"* — genuinely separable on value, offered at the gate,
  and **merged by user decision** (RD3). The evidence agrees with the decision: the pair intersects
  at `player_data_exporter.py` at hop 1.
- *"Slot detail"* and *"a change-diff report"* — ruled out by RD2 and RD1 respectively; see
  §"Candidates considered and NOT emitted".

### Landing order

```
D17 (espn-draft-ingest)  ->  D18 (live-draft-cockpit)  ->  D19 (draft-night-rehearsal)  ->  [this ticket]
```

Stated, strictly linear, acyclic. Two distinct reasons, neither of which is mere preference:

1. **D17 is a hard technical dependency** (F3): the authenticated client, the credentials, the
   league identity config and the fixture harness are all its deliverables, and this ticket extends
   rather than duplicates them. It **cannot** precede D17.
2. **D18 and D19 are a deadline dependency, not a technical one.** This ticket's value is
   *in-season*; theirs is a single unrepeatable evening. Landing this one last costs nothing it
   needs and keeps the draft-night path from being disturbed while it is being rehearsed.

**One consequence of that ordering, recorded rather than discovered later.** D19 re-points the
`draft-sim-test` harness at the ESPN path, and that harness performs a **pre-draft fetch**. This
ticket changes what a pre-draft fetch does to ownership (RD5's zero-rosters case: every player
correctly reads as a free agent). So landing after D19 means D19's harness may need a small
follow-up touch. That is accepted as the cheaper side of the trade — the alternative is disturbing
the draft-night path during its rehearsal window — and it is a known follow-up rather than a
surprise.

### Independence probes — recorded outcomes (`reference/project_separability_test.md`)

**No intra-set pairs exist** (N = 1), so the pairwise obligation is discharged against the
**already-emitted** tickets this one shares a codebase with. **The honest result: it is independent
of none of them.** The independence claim is therefore **dropped** and replaced by the explicit
total ordering above, per the protocol's instruction to state the ordering dependency rather than
assert an independence that fails.

| Pair | Hop 1 — touch-set intersection | Hop 2 — cross-referenced symbol | Outcome |
|---|---|---|---|
| this ↔ **D17** | `espn_client.py`, `player_data_exporter.py`, `player_data_fetcher_main.py`, `run_player_fetcher.py`, `config.py`, `league_config.json`, `tests/fixtures/espn_api/`, `tests/player_data_fetcher/*`, `tests/integration/*`, `ARCHITECTURE.md` | this ticket **extends** D17's league client and **retires** the pick→`drafted_by` write D17 installs | `probed: coupled — 10-path touch-set intersection + supersedes D17's fetcher-side ownership write, hop 1` |
| this ↔ **D18** | `data/configs/league_config.json` (distinct keys — D18 adds `teamId`/geometry, this adds none) | D18's recommendations read the `drafted_by` state this ticket writes | `probed: coupled — shared config file + consumes this ticket's output, hop 1` |
| this ↔ **D19** | `tests/fixtures/espn_api/`, `tests/integration/*` | D19's harness performs the pre-draft fetch this ticket changes the behaviour of | `probed: coupled — shared fixture corpus + exercises this ticket's path, hop 1` |

**Total coupling raises the fair challenge — should this be folded into D17 instead?** No, and the
distinction is **deliverability, not independence**. D17 is a complete, coherent rollout on its own
and ships a working draft-night ingest; this ticket is a *subsequent capability built on its
finished state*, with a different authority model (F4), a different failure direction (F10), and a
different operating window (RD5). After each of them the system is coherent and shippable. What the
rubric forbids is a **rollout** spanning tickets — which this split does not do, because each is a
whole rollout.

### Ticket emitted

| ID | Folder | Back-link |
|---|---|---|
| **D20** | `tickets/D20-espn-roster-state-sync-fetcher/` | `Spike: spikes/archive/player-data-fetcher-roster-sync.md` |

---
Validated 2026-08-05 — 4 rounds, 1 adversarial sub-agent confirmed (sha256:1b6128d4c0ab4254) (spike Step 2.5 — pre-decomposition)
