---
name: draft-sim-test
description: >
  Project-specific end-to-end draft-simulation harness for the interactive
  League Helper — an INDEPENDENT, ad-hoc, human-invoked tool for the user's
  own manual testing, EXPLICITLY OUTSIDE the scope of Shamt testing (at
  least for now). Fetches the current 2026 season's data via this project's
  fetch runners (schedule + player + optional game-data), snapshots the
  freshly-fetched `data/` tree, verifies that every config/constant/data
  value is set to a correct, mutually-consistent 2026-live baseline, then
  drives a full 10-team, 15-round (150-pick) snake draft through the real
  run_league_helper.py CLI as a user would — our picks via Add to Roster
  (option 1), all nine opponents' picks via Modify Player Data → Mark
  Player as Drafted (option 4/1) — and unconditionally rolls back the
  draft's own mutations to the post-fetch snapshot on exit (the freshly
  fetched player/schedule data PERSISTS as a real `data/` diff for the
  user to commit or discard). Emits a WARNING when the sole remaining
  known-open draft-flow defect (T87 missing `game_data.csv`) is observed,
  so the run doubles as a regression signal for that ticket — the WARN
  flips to PASS on its own the moment T87 lands. Invoke when the user
  asks to run a draft simulation,
  test the draft flow, simulate a 10-team draft, smoke the draft, exercise
  the endgame / K/DST rounds, or verify the interactive draft path
  end-to-end.
triggers:
  - "run a draft simulation"
  - "test the draft flow"
  - "simulate a 10-team draft"
  - "draft sim"
  - "draft-sim-test"
  - "smoke the draft"
  - "end-to-end draft test"
  - "exercise the draft endgame"
---

# /draft-sim-test

**Purpose:** A standalone, human-invoked utility that (1) FETCHES current live 2026 data via the project's own fetch runners, (2) VERIFIES every config / constant / data value is set to a correct, mutually-consistent 2026-live baseline, then (3) drives a **full 10-team, 15-round snake draft** (150 roster slots filled) through the interactive League Helper end-to-end from that freshly-fetched `data/` tree, exercising the whole draft surface — early-round RB/WR runs, mid-round QB/TE, late-round K/DST, position limits, the T42 zero-value fallback, and roster-full — then rolls back the draft's own mutations to the post-fetch snapshot and emits a structured run report.

**Identity — scope.** This skill is an **independent, ad-hoc tool for the user's own manual testing**, deliberately **outside the scope of Shamt testing** (at least for now — see §Lifecycle interaction below). It is NOT a Phase-6 verdict source: no `user_test_plan.md` should cite it as a green gate, and the `user-simulator` persona does not invoke it. It complements — does not replace — Shamt's Phase-6 automated + user-test-plan machinery, and it can be run any time (post-config edit, post-fetcher change, post-scoring tweak, or just before a real draft night) without any Shamt phase running.

**Relation to `TESTING_STANDARDS.md`.** Because this skill is **outside Shamt testing scope**, TESTING_STANDARDS' "Out of scope for the agent (human-only)" boundary — which forbids live network fetches in the agent-driven testing path — **does not bind this skill**. The fetch step below is legitimate here precisely because the skill is a human-invoked utility, not agent-driven Shamt testing. Where TESTING_STANDARDS' §"User-driving conventions" prescribes purely **mechanical driving conventions** — project-root cwd, `.venv/bin/python`, log-line filtering, the `Modify Player Data` writes-to-disk caution, exit-code interpretation — those rules still apply and this skill inherits them.

## Preconditions

- Run everything from the project root (`/home/kai/code/FantasyFootballHelperScripts`) with `.venv/bin/python`. `tests/conftest.py` puts the repo root on `sys.path`; a run from any other directory will fail.
- The **automated suite** is not driven by this skill.
- **Working tree state.** Preflight requires `git status --porcelain -- data/` to report **no tracked modifications** (`M`/`A`/`D`/`R`) at start; otherwise HALT and report. The clean baseline is what the fetch's diff will show against, and what the draft's rollback restores to (via the post-fetch snapshot).
  - **Untracked entries (`??`) under `data/` do NOT block preflight.** This skill's own step-2 fetch produces untracked by-products — `data/game_data.csv` is untracked, as is `data/season_schedule.backup.csv` — so a strict "porcelain output is empty" gate would pass exactly once and then halt every subsequent run forever. Record the untracked set in the run report (it is part of what the step-3 snapshot captures and step 9 compares against), but do not halt on it.
- **Live network** — the fetch step calls the ESPN/API endpoints the project's fetchers use. If the user is offline or an endpoint is down, the skill HALTS at the fetch step rather than falling back to stale data.

## Steps

### 1. Preflight
   - Verify cwd is the project root; confirm `.venv/bin/python` resolves.
   - Confirm `git status --porcelain -- data/` reports no **tracked** modifications; halt otherwise. Untracked (`??`) entries are expected fetch by-products and never halt — see §Preconditions.
   - Note the current HEAD and record it in the run report.
   - Read `league_helper/constants.py` and record the module-level `RECOMMENDATION_COUNT` (must be **5** — the "one Add-to-Roster entry = one pick" chaining assumption keys on this) and module-level `FANTASY_TEAM_NAME` (`Sea Sharp` at this writing). **These are module-level names, NOT class attributes** — the file defines no `Constants` class, so `from league_helper.constants import Constants` raises `ImportError`. Import as `from league_helper.constants import RECOMMENDATION_COUNT, FANTASY_TEAM_NAME` (or read the file textually). If either constant changed, halt and ask — the chaining/team-index conventions below are keyed to them.
   - Read `data/configs/league_config.json` and record the fetch-argument-driving values: `NFL_SEASON`, `CURRENT_NFL_WEEK`, `NFL_SCORING_FORMAT`, `MAX_POSITIONS`. These are the values every fetch invocation below MUST be parameterized against — NEVER accept a fetcher default.
   - **Every config value this skill names lives under the file's top-level `parameters` object**, not at the document root — read them as `json.load(open("data/configs/league_config.json"))["parameters"]["NFL_SEASON"]` (and likewise for `CURRENT_NFL_WEEK`, `NFL_SCORING_FORMAT`, `MAX_POSITIONS`, `FLEX_ELIGIBLE_POSITIONS`, `DRAFT_ORDER`, `OPPONENT_TEAMS`). A bare root-level read raises `KeyError`. The `ConfigManager` accessors below already unwrap this for you.
   - Also record `OPPONENT_TEAMS` from the same file (the nine opponents; read at runtime as `ConfigManager.opponent_teams`). This is the **sole** source of the opponent roster since [[T80]] landed — there is no longer any team list in `constants.py`. If it does not hold exactly nine names, halt and ask.

### 2. Fetch live data (ALWAYS, every run)
   The League Helper's fetchers each carry defaults that DISAGREE with the current live config (as of this writing `run_player_fetcher.py` defaults to `--season 2025 --week 17` while the live `league_config.json` is `NFL_SEASON 2026 / CURRENT_NFL_WEEK 1`). A bare invocation silently fetches the WRONG SEASON. **This step derives every argument from the config values recorded in step 1 and passes them explicitly; never rely on a fetcher default.**

   Invocations (all from project root, in this order):

   1. **Schedule** — `.venv/bin/python run_schedule_fetcher.py --season <NFL_SEASON> --force-refresh` (plus `--enable-log-file` if the run report will parse logs). Writes `data/season_schedule.csv`.
   2. **Player data (with game-data)** — `.venv/bin/python run_player_fetcher.py --season <NFL_SEASON> --week <CURRENT_NFL_WEEK> --scoring-format <NFL_SCORING_FORMAT> --my-team-name "<FANTASY_TEAM_NAME>" --no-load-drafted-data --enable-game-data` (add `--game-data-csv <path>` if the target path differs from the fetcher's default; `--enable-historical-save` optional). `--no-load-drafted-data` is deliberate: the fetch must produce a **clean all-free-agent board** so no player is pre-assigned to a team; combined with the reset in step 3 it is belt-and-suspenders.
   3. **Historical compile (optional, only if a compiled sim tree is expected)** — `.venv/bin/python compile_historical_data.py --year <NFL_SEASON>` (or `--all-years` if a full rebuild is wanted). Writes under `simulation/sim_data/{YEAR}/`.

   Use generous per-fetch timeouts (300s+ each; the player fetch is the slow one — ESPN pagination + rate-limit-delay).

   **On any fetch failure (non-zero exit, timeout, missing output file) — HALT.** Do not proceed to verify or draft against stale/partial data. Record the failure in the run report and stop.

   **`data/` is git-TRACKED.** The fetch will therefore surface as a real `git diff` in `data/` — the schedule CSV + the per-position player JSONs. (`data/game_data.csv` is the exception: it is **untracked**, so it lands as a `??` entry rather than inside the diff.) This is EXPECTED, not a failure. The user chooses to commit or discard the diff after the skill exits. The **draft's own** mutations (drafted_by / locked marks from Add-to-Roster and Mark-as-Drafted) will be rolled back by step 9, so the surviving diff is the fetch-only diff.

### 3. Clean the board, then snapshot `data/` (both AFTER the fetch)
   **Order is load-bearing: reset FIRST, then snapshot, then arm the trap.** The snapshot must capture the board the draft actually starts from, so it has to be taken *after* the reset. Snapshotting first would make the rollback baseline an *unreset* board, so a mid-run restore would drop the draft onto a board that already carries `drafted_by` marks — the integrity counts in step 8 would then never reconcile.

   1. **Clean-board reset.** Even with `--no-load-drafted-data` passed to the fetcher, defensively normalize every player: for every player in every position file under `data/player_data/`, set `drafted_by = ""` and `locked = false` as you write. This is REQUIRED regardless of the fetch options — the draft simulation depends on starting from a genuinely empty board.
   2. **Snapshot.** Copy `data/` to a scratch backup (e.g. under the scratchpad directory). This is the rollback baseline, and it now genuinely is *freshly-fetched data + a clean board* — the exact state step 9 restores to.
   3. **Install the unconditional restore trap.** The trap MUST fire on normal exit, on error, on `KeyboardInterrupt`, on timeout, and on any halt below — the invariant is "if this skill mutated `data/` after the snapshot, this skill restores `data/` to the snapshot." Verify the restore succeeded by asserting `git diff --stat data/` matches the fetch-only diff (i.e. no draft-mutation delta on top).

   *(The reset happens before the trap is armed, so it is deliberately **not** rolled back — it is part of the intended baseline, not a mutation to undo. The window between the reset and the trap touches only `data/player_data/` ownership fields, which the fetch in step 2 has just rewritten anyway; a failure inside that window is recoverable by re-running the skill.)*
   *(Historical note: the previous version of this skill seeded `data/player_data/` from `tests/fixtures/player_data/`. That is now retired — the live fetch supersedes fixture seeding as the data source. Only the `drafted_by`/`locked` reset survived because it is required regardless of source.)*

### 4. Verify — every value is set to a correct, mutually-consistent baseline
   Emit each check below as a `PASS`, `WARN`, `FAIL`, or `n/a` line in the run report. Two tiers, and the distinction is load-bearing:

   - **FAIL → HALT before drafting.** Reserved for conditions that make the draft *meaningless or impossible* — wrong season fetched, scoring-format mismatch, roster shape that breaks the loop.
   - **WARN → record and continue.** Used for **known-open, ticketed defects** whose behaviour is understood and tolerable (worked around where a workaround is needed; T87 below needs none — the draft simply runs without game-conditions scoring), exactly as the T87 `game_data.csv` check below is handled. A ticketed defect must not brick this skill; a WARN keeps the run useful while making the defect impossible to miss, and flips to PASS on its own the moment the ticket lands (provided the WARN's state is explicitly re-read at runtime here — see the retirement lessons in §Retiring below).

   Ticket bodies live at `.shamt-core/epics/T38-tech-stories/T39-bugs/`.

   1. **Season/week coherence.** `NFL_SEASON` and `CURRENT_NFL_WEEK` (from step 1) must match what was actually fetched. Two concrete assertions, both against sources that actually carry the values (the schedule CSV's header is exactly `week,team,opponent` — **it has no season column**, so a `NFL_SEASON`-vs-schedule assertion is not performable; the player JSONs likewise carry no `season` field. Only the following two sources do):
      - **Season** — `data/game_data.csv` **does** carry the season, via its `date` column (ISO like `2026-09-10T00:20Z`). Assert that every non-empty `date`'s calendar year matches `NFL_SEASON` (or, for a season spanning the calendar boundary, matches `NFL_SEASON` or `NFL_SEASON + 1`). If `data/game_data.csv` is absent (the T87 WARN in check 4.5), fall back to asserting only that the fetch was **invoked** with `--season <NFL_SEASON>` (record the arg string in the run report as evidence).
      - **Week / coverage** — assert `data/season_schedule.csv` covers weeks **1–18** (the regular-season shape; at this writing every week 1–18 is present).

      A mismatch is the load-bearing trap this whole verify step exists to catch (e.g. a bare `run_player_fetcher.py` silently pulling the prior season).
   2. **Scoring format coherence.** `NFL_SCORING_FORMAT` must equal the `--scoring-format` this run passed to the fetcher.
   3. **Roster shape coherence.** `sum(MAX_POSITIONS.values())` MUST equal `len(DRAFT_ORDER)`. At this writing that is `15 == 15` (MAX_POSITIONS `{QB:2, RB:4, WR:4, FLEX:1, TE:2, K:1, DST:1}` → 15; DRAFT_ORDER has 15 rounds). A mismatch breaks the draft loop; FAIL.
   4. **Team identity — FAIL tier.** `FANTASY_TEAM_NAME` + `OPPONENT_TEAMS` (from `league_config.json`) must total **10** distinct teams. Report the count. FAIL if the total is not 10, which would break the ten-team draft structure. Since [[T80]] landed, `OPPONENT_TEAMS` is the single source of truth for the opponent roster — the `TEAM SELECTION` menu is seeded from it, so a config edit flows straight through to the UI and no constant-vs-fixture divergence is possible.
   5. **`game_data.csv` presence (T87) — WARN tier.** After the fetch, assert `data/game_data.csv` (or the configured path) exists and is non-empty. Its absence makes the League Helper print `game conditions scoring disabled` every launch — a scoring dimension silently off, tracked by [[T87]]. Step 2's `--enable-game-data` should produce it; `WARN` if it did not land, and continue (the draft still runs, just without game-conditions scoring).
   6. **Sim data validity — usually `n/a`.** Only meaningful if a compiled `simulation/sim_data/{NFL_SEASON}/` tree exists. **At this writing `simulation/sim_data/` holds 2021–2025 only — there is NO 2026 tree**, so with `NFL_SEASON 2026` this check records `n/a` unless step 2's third invocation (the historical compile) was explicitly run to build one. When a tree does exist, run `.venv/bin/python validate_sim_data.py --year <NFL_SEASON>`: exit 0 → PASS, exit 1 → FAIL. Do not invoke it against a season with no tree — that is a spurious failure, not a finding.
   7. **Summary.** Report every check as one `PASS` / `WARN` / `FAIL` / `n/a` line, and a roll-up count of each. **HALT before drafting (i.e. before the next step) on any FAIL; a WARN never halts.** A run whose only findings are WARNs on tracked tickets is a legitimate, useful run — say so in the report rather than implying it is degraded.

### 5. Build the snake-draft order (15 rounds × 10 teams = 150 roster slots)
   - Snake order over the ten teams — `Sea Sharp` at a chosen slot (record it in the report).
   - For each round, compute the ordered list of picks: (team, roster-slot-hint).
   - **Intra-round ordering caveat — step 7's two-phase design puts OUR pick first in every round.** Phase 1 (our Add-to-Roster pick) necessarily runs before Phase 2 (the nine opponent marks), because Phase 2 must re-probe against a pool that already excludes the app's own choice. So the harness does **not** reproduce a positional snake for `Sea Sharp` — we effectively pick 1.01 every round. This is deliberate and does not affect anything the run asserts: the integrity checks in step 8 are about roster **shape and counts**, not about draft-position realism, and the whole 150-slot surface is still exercised. Use the snake order for the **opponents'** slot hints (which position each opponent plausibly takes next); record `Sea Sharp`'s nominal slot in the report but do not expect the recommendations to reflect it.
   - **Roster limits come from `data/configs/league_config.json`, NOT from `constants.py`** — `constants.py` states outright that `MAX_POSITIONS` / `MAX_PLAYERS` moved to the config. Read them at runtime via `ConfigManager.max_positions`; `ConfigManager.max_players` is the derived `sum(MAX_POSITIONS.values())`, not a stored key. At this writing that is `{QB: 2, RB: 4, WR: 4, FLEX: 1, TE: 2, K: 1, DST: 1}` = **15**, matching the 15 draft rounds. Do **not** hardcode these — a config change must flow through.
   - Note the distinction: `MAX_POSITIONS` is the **roster capacity** the draft fills; the 9-slot *starting lineup* Starter Helper reports (QB/RB/RB/WR/WR/TE/FLEX/K/DEF) is a different shape. The integrity check in step 8 asserts against **`MAX_POSITIONS`**.

### 6. Round loop — our pick + nine opponent picks per round
   For each round `R` in 1..15: run §6a (our pick) every round.

   Run §6b (the nine opponent picks) in **all 15 rounds** — 9 × 15 = **135** opponent picks plus our 15 = **150** picks made in-run, with nothing seeded.

   #### 6a. Our pick (Add to Roster)
   - Each own pick costs exactly **`1\n1\n`** — the first `1` enters Add to Roster from the main menu, the second selects the top recommendation. `RECOMMENDATION_COUNT = 5` caps the list, so in a normal round options are `1`–`5` with `6` = "Back to Main Menu" — but the Back option is printed as `len(recommendations) + 1`, and late rounds (K/DST, the T42 zero-value fallback pool) can return **fewer** than 5, so never key on `6`. Always send `1`, which is valid whenever any recommendation exists.
   - After a **successful** pick the mode **breaks back to the main menu**. You therefore **cannot take two picks inside one mode entry** — to take N consecutive own picks, simply repeat the pair N times (`1\n1\n1\n1\n` = two picks: enter/select, enter/select). This is why our picks are chained as pairs while opponent picks (§6b) chain inside a single mode entry — the two modes have opposite loop behavior, and conflating them desynchronizes the whole input stream.
   - **Roster-full path (late rounds):** if `Add to Roster` prints `"No recommendations available (roster may be full or no available players)."` and returns to the main menu, that is **correct behavior**, not a failure — record it and move on to the opponent picks.

   #### 6b. Nine opponent picks (Modify Player Data → Mark as Drafted)
   Unlike Add to Roster, `Mark as Drafted` **loops back to the sub-menu** after each mark, so chain **all nine** opponents in **one** `4` entry, then `4\n` to return.

   For each opponent pick `p` in this round:
   - **Choose the target.** Query the current free-agent pool out-of-process — construct `ConfigManager` / `SeasonScheduleManager` / `TeamDataManager` / `PlayerManager` over `data/`, then filter `pm.players` on `is_free_agent()` — for the top-K by projected points that plausibly fit the opponent's next roster slot (position-aware, snake-order-plausible). "Plausible" = position not yet at its roster limit for that opponent AND consistent with typical fantasy draft order.
   - **Pick a distinctive search term for that player, then verify — against the CURRENT pool — that it matches EXACTLY ONE player** (the pool shrinks every pick, so re-probe every time). This is **the biggest hazard**, and it has **two distinct failure modes**, because `PlayerSearch.interactive_search` always prints the match list and then always prompts exactly once for a choice — a unique match is *not* auto-selected, which is why every pick spends a `<match-index>` line:
     - **2+ matches → silent misassignment, same line count.** The stream stays in sync and `1` is accepted, but it selects the *first* match, which may be the wrong player — no error, no visible symptom until the step-8 integrity check.
     - **0 matches → silent per-collision pick loss (measured 2026-08-02).** The search prints `No players found matching '<term>'. Try again or press Enter to exit.` and **re-prompts for a search term** — it does not fall through. So the quadruple's remaining lines (the `<match-index>` and `<team-index>`) are each consumed as *further search terms*. **When each of those stray lines also zero-matches**, each just re-prompts and the stream **naturally resynchronizes at the following quadruple** — no crash, no traceback, no misassignment. Net measured effect in that case: **exactly one opponent pick silently lost per collision** (the run that surfaced this landed 136/150 instead of 150/150 across nine of ten rounds where a collision fired).
       - **The benign resync is NOT guaranteed — a stray digit line that *matches* breaks it (verified 2026-08-02).** Search is a plain substring/word-prefix match on the player name, so a stray numeric line matches any name containing that digit. In the live 2026 pool exactly one name does: **`49ers D/ST`**, matched by a stray `4` or `9` — i.e. by team-indices 4 and 9, both of which the nine-opponent index set uses. Driven end-to-end, a zero-matching `<term>` followed by `<match-index>=1` and `<team-index>=4` had the `4` match `49ers D/ST`, the *next* quadruple's leading `1` select it, its `<term>` rejected as a non-numeric team choice, and its `<match-index>` accepted as the team — **assigning `49ers D/ST` to the wrong team and then dropping the following `<team-index>` into the sub-menu as a `2` = `Drop Player` entry**. So a collision can cost more than one pick and *can* misassign. Treat the benign single-pick-loss case as the best case, never the guaranteed one.

     Both modes have the same fix: never emit a term that matches anything other than exactly one player. The primary trigger of the zero-match mode is the design pitfall in step 7 below (a precomputed opponent target colliding with the app's own just-chosen pick); the round-by-round two-phase design in step 7 removes it structurally, and the step-8 count check is the backstop.

     Known-ambiguous fragments actually hit in the wild: `McCaffrey` → 2 (Christian + Luke), `Amon` → 2 (Rhamondre Stevenson + Amon-Ra St. Brown), `Jefferson` → 2 (Justin + Van), `Conner` → 2 (James + Tanner). Prefer a distinctive fragment; **verify, don't assume** — and never emit a term that matches zero players. If the pool changes mid-round, re-verify.
   - **Determine the team index.** The `TEAM SELECTION` menu is the sorted union of `ConfigManager.opponent_teams`, `FANTASY_TEAM_NAME`, and every non-empty `drafted_by` present in the player data; it is sorted **alphabetically** each time it is shown, the index is the position in that sorted list, and `Cancel` is `len(teams) + 1`. Because the configured roster is present from pick 1, the order is **stable for the whole run** unless an out-of-band `drafted_by` name appears that is not in `OPPONENT_TEAMS`. **Recompute the sorted order every time anyway** — never hardcode indices across picks or rounds (a mid-run team-set change silently shifts every remaining index).

   Emit the chained opponent block for this round's Phase 2 (per step 7): the leading `4\n` enters Modify Player Data, nine `1\n<term>\n<match-index>\n<team-index>\n` quadruples chain inside that mode entry, a trailing `4\n` returns to the main menu, and (because Phase 2 is its own process) a final `6\n` quits.

   `4\n` + `1\n<search-term-1>\n<match-index-1>\n<team-index-1>\n` … `1\n<search-term-9>\n<match-index-9>\n<team-index-9>\n` + `4\n` + `6\n`

   That is 1 + (9 × 4) + 1 + 1 = **39 input lines** for one round's Phase 2, on top of Phase 1's three lines (`1\n1\n6\n`) for our own pick.

### 7. Terminate cleanly — round-by-round, two invocations per round

   **A single precomputed input string for the whole draft is structurally wrong** and MUST NOT be used, even though it looks tempting for its simplicity. Step 6b requires re-probing every search term against the CURRENT free-agent pool "because the pool shrinks every pick" — but our own pick is chosen BY THE APP (the top recommendation), so its identity is unknowable in advance. Precomputing the nine opponent targets before invoking the app therefore risks the app's own pick colliding with the first precomputed opponent target; the opponent search then zero-matches and consumes the quadruple's remaining lines as re-prompts (per step 6b's zero-match arm), silently losing **at least** one opponent pick that round — and, in the bad sub-case step 6b records, misassigning a player as well. This was measured in the wild on 2026-08-02: nine of ten rounds lost exactly one pick, ending 136/150 instead of 150/150.

   **The prescribed design — round-by-round, in separate processes, each round split into two phases.** The app persists `drafted_by` to `data/player_data/*.json` on every pick, so state carries across invocations and each phase reloads the current pool from disk. For each round `R` in 1..15:

   - **Phase 1 — our pick alone.** One invocation, one process, driving only `1\n1\n6\n` (Add to Roster → top recommendation → Quit). The app's chosen player is now recorded on disk.
   - **Phase 2 — nine opponent picks.** A second invocation, in a fresh process. **Before** building this phase's input string, **reload the player pool from disk** (construct `PlayerManager` etc. over `data/`) so the pool reflects the app's Phase-1 pick. Then compute the nine opponent targets against that reloaded pool (per step 6b, verifying each search term uniquely matches exactly one CURRENT free agent — including against the just-drafted player, who is no longer a free agent). Drive `4\n` + nine quadruples + `4\n` + `6\n`.

   This is what makes the "re-probe every pick" rule actually satisfiable. Executed end-to-end on 2026-08-02 it produced a clean **150/150 picks, ten picks per round, zero findings**.

   **Terminate every phase with `6\n` (Quit).** Expect `Goodbye!` and exit `0` from each invocation.
   - **NEVER** rely on input exhaustion to end any phase — a short input script means that phase did not complete, and the run tells you nothing about the real exit path. (Since T83 landed 2026-08-02 EOF now surfaces as a clean `No input available on stdin — exiting.` message with exit `1` rather than a traceback, but a short script remains a legitimate FAIL — see §Failure / halt policy.)
   - Use generous timeouts: **60s** is ample for each Phase-1 own-pick invocation and comfortable for each Phase-2 opponent-block invocation (nine marks + one search each is fast; the slow work is recommendation scoring, which happens only in Phase 1). Budget a whole-run timeout well above `15 * (Phase1 + Phase2)`.

   Launch invocation shape (repeated for each phase of each round):

   ```bash
   printf '<phase-input>' | timeout 120 .venv/bin/python run_league_helper.py
   ```

   Optional flags per TESTING_STANDARDS' mechanical conventions: `--week N` (in-memory week override), `--enable-log-file` (rotating log files under `logs/<script>/` — otherwise timestamped log lines interleave on stdout).

   **Log-noise filter when reading output:** timestamped log lines go to stdout interleaved with UI. Filter with `grep -v "^20[0-9][0-9]-"` when parsing.

   **Worked example — one round's two phases.** The `TEAM SELECTION` menu is the sorted union of the nine `OPPONENT_TEAMS` + `Sea Sharp` — **ten rows from pick 1**, with `Cancel` as the eleventh — so with the `league_config.json` roster as committed at this writing the alphabetical `TEAM SELECTION` order is:

   ```
    1. Annihilators          6. Saquon Deez
    2. Bo Him-ian Rhapsody   7. Sea Sharp        <- our team, never a target here
    3. Chase-ing points      8. Striking Shibas
    4. Fishoutawater         9. The Eskimo Brothers
    5. Pidgin               10. The Injury Report
   ```

   So the nine opponent team-indices are `1,2,3,4,5,6,8,9,10` — **7 is skipped**, because that is us. (`Cancel` would be `11`.)

   **Phase 1** input (one own pick + quit):

   ```
   1\n1\n6\n
   ```

   Then reload the pool from disk, compute the nine opponent targets, and drive **Phase 2** input (nine opponent picks + quit):

   ```
   4\n1\nBijan\n1\n2\n1\nJa'Marr\n1\n4\n1\nSaquon\n1\n6\n1\nJahmyr\n1\n9\n1\nCeeDee\n1\n1\n1\nPuka\n1\n5\n1\nAmon-Ra\n1\n3\n1\nNabers\n1\n10\n1\nBowers\n1\n8\n4\n6\n
   ```

   Reading Phase 2: `4\n` enters Modify Player Data. Then nine `1\n<name>\n<match-index=1>\n<team-index>\n` quadruples for the nine opponents (match-index is `1` for every one **because each search term was pre-verified unique against the CURRENT pool** — never assume this; and the pool here is the one that already excludes the app's Phase-1 pick). Then `4\n` to return to the main menu, then `6\n` to quit.

   **The nine terms above are round-1 examples, verified unique against the 2026 pool on 2026-08-02 — they are NOT reusable across rounds or seasons.** They are all first-name/distinctive fragments precisely because surname fragments are the trap: in this very pool `Henry` → 2 (Derrick + Hunter), `Evans` → 2 (Mike + Mitchell), `Higgins` → 3, and `Mixon` → **0**. Re-derive and re-verify every term against the live pool each round (step 6b); never copy this line forward.

   This is **one full round, in two invocations**. The whole run is 15 such round-pairs — **30 invocations total**, no cross-round input carry, no single monolithic stream.

   **This table is illustrative, not authoritative** — recompute the sorted order at runtime (step 6b) from the live `OPPONENT_TEAMS`. If the configured roster changes, every index shifts.

### 8. Post-draft integrity checks (general truthfulness)
   Before restore, out-of-process on the mutated `data/`:
   Assert against `MAX_POSITIONS` read from config (step 5), never hardcoded numbers:

   - **Every team holds exactly `sum(MAX_POSITIONS.values())` players** (15 at this writing) — or hit a legitimate roster-full / T42 zero-value-fallback branch the run report explains.
   - No team exceeds any individual `MAX_POSITIONS` limit **once FLEX is accounted for** (e.g. no 3rd QB). **Do NOT do a naive per-position comparison against `MAX_POSITIONS`** — the FLEX slot (`MAX_POSITIONS.FLEX = 1` at this writing) is filled by an extra RB or WR (per `FLEX_ELIGIBLE_POSITIONS` in `league_config.json`), so a 5th RB or 5th WR **is legal** when it fills the single FLEX slot. Correct check: per team, allow `MAX_POSITIONS[pos] + MAX_POSITIONS.FLEX` for each FLEX-eligible position, and ensure the total across FLEX-eligible positions does not exceed `sum(MAX_POSITIONS[pos] for pos in FLEX_ELIGIBLE_POSITIONS) + MAX_POSITIONS.FLEX`. **This bit hard on 2026-08-02:** 9 of 10 teams looked like violations under a naive check (they all had one extra RB or WR filling FLEX) until FLEX was accounted for; the earlier text's "no 5th RB" example was wrong on exactly this point.
   - Our own team (`Sea Sharp`) has a full 15-slot roster, or an explained shortfall.
   - **No player is owned by two teams**, and no player appears twice in one roster.
   - **Counts reconcile exactly:** 9 opponents × 15 picks = 135, plus our 15 = **150 picks made in-run** = **150 distinct drafted players**, nothing seeded.

   **Any count mismatch is a FAIL, not a warning** — it is the primary evidence that a search term went wrong in one of step 6b's two ways (a zero-match term desynchronized the input stream, or an ambiguous term silently drafted the wrong player), or that some other defect misassigned a pick. (This check was originally written as the T81 mitigation; T81 landed 2026-07-30 — `show_list_selection` now range-checks every menu index — but the check is retained because it is generally useful and catches the input-desync class T81 never covered.)

### 9. Restore to the post-fetch snapshot and verify
   - Run the restore trap unconditionally (idempotent — safe even if the run already restored on a mid-run halt). Restore target is the **step-3 snapshot** (freshly-fetched data + clean board), NOT the step-1 HEAD.
   - After restore, assert `git diff --stat data/` matches the **fetch-only** diff (i.e. the schedule + player changes from step 2 remain, and NO draft-mutation delta remains on top). If a draft-mutation delta survives, FAIL loudly and include the diff in the report — restore-fail is never soft.
   - **`git diff` alone is not a sufficient restore check** — it reports only *tracked* files, and `data/game_data.csv` is **untracked** (as is any other fetch by-product the repo does not track). Pair the diff with a direct **file-tree comparison against the step-3 snapshot** (e.g. `diff -rq <snapshot> data/`) so an untracked file the draft touched cannot slip through invisibly. Use `git status --porcelain -- data/` to enumerate the untracked set rather than assuming it.
   - Do **NOT** revert the fetch-only diff. The freshly-fetched data is intended to persist as a real, user-inspectable `git diff` in `data/`; the user commits or discards it after the skill exits.

### 10. Run report (structured)
   Emit:
   ```
   DRAFT-SIM-TEST RESULT: {PASS | FAIL | KNOWN-BUG-WARNED}
   Fetch:
     schedule: {ok | FAILED (reason)}
     player_data: {ok | FAILED (reason)}   [season=..., week=..., scoring=...]
     game_data.csv: {landed | MISSING}
     historical_compile: {ok | skipped | FAILED (reason)}
   Verify:   [WARN tier = known-open ticket, never halts | FAIL tier = halts before drafting]
     season/week coherence: {PASS | FAIL}                          <- FAIL tier
     scoring-format coherence: {PASS | FAIL}                       <- FAIL tier
     roster-shape coherence: {PASS (sum(MAX_POSITIONS)=len(DRAFT_ORDER)=15) | FAIL}   <- FAIL tier
     team-identity total: {PASS (10) | FAIL — total != 10}         <- FAIL tier
     T87 game_data.csv: {PASS | WARN — T87 live, absent (game-conditions scoring disabled)}
     sim_data validate: {PASS | FAIL | n/a — no compiled tree for season N}
     roll-up: {P pass, W warn, F fail}
   Rounds completed: {R}/15
   Picks made in-run: {N}/150
   Total distinct drafted: {N}/150
   Per-team roster counts: {team: count, ... — all should equal sum(MAX_POSITIONS))}
   Own roster: {slot-by-slot summary}
   Endgame observed: K rounds {yes/no}, DST rounds {yes/no}, T42 zero-value fallback fired {yes/no}, roster-full observed {yes/no}
   Clean `Goodbye!` exit: {yes | no — input exhausted before `6\n` (FAIL) | no — other (FAIL)}
   Integrity checks: {all pass | list failures}
   Restore verified (post-fetch snapshot; fetch-only diff surviving + untracked tree matches): {yes | NO — extra draft-mutation DIFF: ...}
   Exit code: {0 | ...}
   ```

## Failure / halt policy

- A **FAIL** is: any fetch step failed, any verify check FAILed (halt before drafting), process crashed, non-zero exit, `Goodbye!` never printed, **input exhaustion (a short input script — the run never reached a clean `Goodbye!`; the draft did not complete)**, any integrity check failure, or restore did not verify clean against the post-fetch snapshot. (Input exhaustion was previously T83's signature; T83 landed 2026-08-02 and EOF now surfaces as a clean `No input available on stdin — exiting.` message with exit `1`, no traceback. Per the user's 2026-08-02 override of this skill's own §Retiring instruction — which said to delete the clause — the clause was **re-worded, not deleted**: a short input script remains a legitimate FAIL because the draft did not complete, even though it is no longer specifically a T83 signal. Deleting it outright would downgrade a still-valid failure mode to a pass. See §Retiring below for the recorded override reason.)
- A **KNOWN-BUG-WARNED** run — the sole remaining tracked defect (T87 missing `game_data.csv`, the step-4 WARN-tier verify check) still observed and recorded as a WARN (it needs no workaround: the draft runs unchanged, just without game-conditions scoring) — is **still a pass IF** the whole draft completed, terminated cleanly, and every integrity check passed. The warning must name its ticket in the report so a future fix flips it to `PASS`; T87 is a WARN-tier check whose state is explicitly re-read at runtime, so this flip happens with no edit to this skill (the general "flips with no edit" claim is only honest for a WARN whose state is re-read every run — see the un-probed-entry lesson in §Retiring below). **A run whose only finding is a WARN on T87 is a legitimate, useful run** — report it as such, not as degraded.
- **Never fabricate a pass.** If any pick placement was uncertain (e.g. an ambiguous-search-term-slipped-through was detected after the fact by the integrity check), the run is FAIL — not "probably fine."
- **Restore runs on every path**, including on halt, on timeout, on user interrupt, on any exception. If restore itself fails, the FAIL includes the on-disk diff.

## Retiring the known-defect entries

Delete the corresponding part of this skill the moment each ticket lands and its check stops matching:

- **T87 fixed** → drop the T87 verify check (step 4.5) and this bullet.

**Retirement lessons — read before adding a new probe or WARN entry.** T82 (fixed `e835bd06`, 2026-08-01), T83 (fixed `5322e6c8`, 2026-08-02), and T86 (fixed `7ec70270`) were all retired from this skill on 2026-08-02. Two lessons the retirements exposed:

- **Un-probed WARN entries do NOT self-retire.** The retired T82 entry declared "no workaround at the harness — mitigation is a coding rule" and carried no executable probe; its run-report template line was hard-coded to `T82: assumed-live (no probe)`, so every run kept reporting T82 as live after the fix landed — a stale claim the skill had no mechanism to correct, and one that also falsified the skill's own general claim that a future fix "flips it to PASS with no edit." That claim is honest only for WARN-tier checks whose state is explicitly re-read at runtime (T86's raw-count sweep, T87's file-presence check, T83's now-retired probe); an un-probed entry must be **manually retired** the moment its ticket lands. If a new entry cannot carry an executable probe, spell that out in its bullet — call out the manual retirement obligation up front, and add a note to §"Failure / halt policy" narrowing the "flips with no edit" claim to probed entries only.
- **A FAIL signature that outlives its ticket must be re-worded, not deleted.** The retired T83 bullet originally read *"delete the 'if input exhaustion, FAIL' clause in §Failure / halt policy that treats it as a T83 signal, and this bullet."* Per the user's 2026-08-02 override, that clause was **re-worded, not deleted**: input exhaustion is still a legitimate FAIL because it means the draft did not complete — it is just no longer specifically a T83 signal. Deleting the clause outright, as this skill's own instruction said to, would have downgraded a still-valid failure mode to a pass. This override is recorded here so a future maintainer who reads it as a mistake and "corrects" it back to deletion knows why the pre-written instruction is wrong.

With only T87 remaining, the skill is one WARN-tier check away from the intended steady state — fetch + coherence-verify + pure draft-driving harness. Once T87 lands and its check is dropped, the skill will consist entirely of the coherence-verify FAIL-tier checks (season/week, scoring-format, roster-shape, team-identity), the mechanical draft-driving loop, the integrity checks, and the restore trap — no bug-driven entries left.

## Notes — lifecycle interaction

**Mode:** ALONGSIDE the Shamt command set (there is no master command named `draft-sim-test`, so nothing is shadowed and no `OVERRIDE:` warning fires at regen). Every Shamt command generated into this project continues to load unchanged — the Engineer set (`/e1`–`/e9`, `/e-all`, `/e-next`, `/e-diagram`), the PO set (`/pe*`, `/pf*`, `/ps*`, `/po-status`), and the shared utilities (`/validate-artifact`, `/u-*`, `/update-project-doc`, `/update-project-skill`, the `/sync-*` commands). This project is `work_item_tracker: local`, so the remote-flow `/ef*` / `/es*` sets are not generated here at all and are irrelevant.

**Phases it touches:** **none.** This skill is a **standalone, human-invoked utility, deliberately outside the scope of Shamt testing** (per the user's 2026-07-27 decision — recorded here so a future reader understands this is a deliberate scoping call, not an oversight). Specifically:

- **NOT a Phase-4 test-plan citation.** A `user_test_plan.md` should not point at this skill for a Phase-6 verdict. Phase-4 authoring under `user_test_plan_mode: agent-run` (this project's setting) still writes plans in the normal way; those plans do not delegate to this skill.
- **NOT a Phase-6 verdict source.** The `user-simulator` persona does not invoke this skill and this skill's structured PASS/FAIL is not consumable as an `agent_test_session` verdict. Phase-6 continues to run the automated suite from `TESTING_STANDARDS.md` and (under `agent-run`) the user-simulator-executed `user_test_plan.md`; this skill is orthogonal to both.
- **NO Engineer or PO phase depends on this skill.** It can be added, edited, or deleted without affecting any `/e*`, `/p*`, or `/f*` command.
- **This boundary is "at least for now."** The user explicitly reserved the right to bring this skill inside Shamt testing scope later (e.g. by making it a Phase-6 verdict source for draft-touching stories). If that happens, the change is a deliberate re-scoping — a re-edit of this section with the coupling detail — not a discovery that the current framing was wrong.

**Any phase, standalone.** The skill is trigger-invokable outside a story (post-config edit, post-fetcher change, post-scoring tweak, or just before a real draft night). It writes to `data/` — the fetch step produces a real, intended diff the user commits or discards; the draft's own mutations are rolled back to the post-fetch snapshot on every exit path.

**Alongside-vs-override consequences.** Because this skill is ALONGSIDE (a new name), the risk surface is bounded: nothing that a Shamt phase or driver *depends on* is shadowed, so a regression here can never break `/e6`, `/user-simulator`, or any other Shamt command — only this skill's own human-invoked run breaks, and the user reruns it after fixing. If a future edit were to convert this skill to an override of a same-named master command, the override warning at regen would surface but is NOT a safety net — the override risk to call out would be whichever master flow the shadowed command was load-bearing for.

**Relation to `TESTING_STANDARDS.md` (mechanical conventions only).** This skill is outside Shamt testing scope, so `TESTING_STANDARDS.md`'s "Out of scope for the agent (human-only)" boundary — which forbids live network fetches in the agent-driven testing path — does not bind it (the always-fetch step above is legitimate here for that reason). What it DOES still inherit from TESTING_STANDARDS are the mechanical driving conventions where they remain useful: the launch pattern (`printf … | timeout … .venv/bin/python run_league_helper.py`), the project-root-cwd + `.venv/bin/python` invariant, log filtering, the `Modify Player Data` writes-to-disk caution, and exit-code interpretation. If TESTING_STANDARDS is later updated in a way that contradicts a *mechanical* rule here, TESTING_STANDARDS wins and this skill is updated to conform; a contradiction that touches the *scope* boundary above requires the deliberate re-scoping decision described in "This boundary is 'at least for now.'"

**Risks.**

- **HIGH — fetching the wrong season silently.** The fetcher default (`--season 2025 --week 17`) does not match the live config; a bare invocation drafts against last year's data with no error. Fully mitigated by step 2's derive-every-arg-from-config-and-pass-explicitly rule and step 4's season/week coherence verify check. Any future edit that lets a fetch invocation fall back to a fetcher default is a regression against this skill's core promise.
- **HIGH — a bad search term silently corrupts the run.** Two modes (step 6b): an ambiguous term (2+ matches) drafts the wrong player at the same line count, and a zero-match term desynchronizes the input stream — best case losing exactly one pick before resyncing at the next quadruple, worst case (a stray digit line matching a player, e.g. `4`/`9` → `49ers D/ST`) misassigning a player and dropping the stream into the wrong sub-menu. Fully mitigated by the verify-exactly-one-match-every-pick rule in step 6b; the integrity check in step 8 is the backstop. If either is skipped, the whole run can be silently wrong.
- **HIGH — restore-on-exit skipped on an error path.** Fully mitigated by the trap-style unconditional restore in step 3 and the assert-against-post-fetch-snapshot verification in step 9. Any future edit that turns the restore into a conditional, or restores to step-1 HEAD instead of the step-3 snapshot (thereby wiping the intentional fetch diff too), is a regression.
- **HIGH — drafting against wrong data because a FAIL-tier verify check was skipped or downgraded.** Mitigated by step 4's "any FAIL halts before drafting" rule. The FAIL tier is exactly the four baseline checks — season/week, scoring-format, roster-shape, and team-identity — and downgrading any of them to a warning would let a run land a green report against last year's data or a config whose roster shape cannot complete the draft. **This is NOT an argument against the WARN tier:** WARN is reserved for *known-open, ticketed* defects (currently only T87 remains) whose behaviour is understood and tolerable. Deliberately distinguishing the two tiers is what keeps a tracked ticket from bricking the skill while still halting on a genuinely invalid baseline. Collapsing them in either direction is the regression.
- **MEDIUM — a WARN-tier check drifts (its state is misread or its condition mutates without the fix landing).** Only relevant while WARN entries exist; today only T87's `game_data.csv` presence check qualifies, and its state is a plain file-existence read that is hard to misread. Mitigation: the run report always names ticket IDs so a mismatch is obvious.
- **LOW — a hand-edited `OPPONENT_TEAMS` typo shifts every team index.** Since [[T80]] landed the menu is config-driven, so a mistyped or dropped name changes the alphabetical order the piped indices are computed against. Mitigated by step 1's nine-name check, step 4.4's ten-team total check, and step 6b's recompute-the-order-every-time rule.

---

**Last verified end-to-end.** Executed in full on 2026-08-02 against live 2026 data at `main` @ `5322e6c8`. Result: **150/150 picks, all ten rosters 15/15, no duplicate ownership, no position-limit violation, clean `Goodbye!` / exit `0` every round, restore verified.** This is a provenance record, not a probe — do not turn it into a check.

---
Validated 2026-08-02 — 5 rounds, 1 adversarial sub-agent confirmed (sha256:4ec4fd352a18ff46)

<!-- Managed by Shamt (project skill) -->
