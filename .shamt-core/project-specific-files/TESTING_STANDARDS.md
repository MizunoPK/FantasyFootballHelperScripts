---
Last Updated: 2026-08-10
Update History:
  - 2026-08-10: D3.2 repair-live-pool-203-records-in-place — refreshed the whole-suite figure in §"Automated test infrastructure" from the stale **3,412 tests across 151 files** (measured 2026-08-06) to **3,495 across 153**, measured 2026-08-10 by a full green run of the declared run-source (`SUCCESS: ALL 3495 TESTS PASSED (100%)`, exit `0`), with the file count independently re-derived by `find tests -name "test_*.py" | wc -l`. This unit contributes **+19 tests / +1 file** of the drift: the new `tests/root_scripts/test_repair_bye_week_points.py` (18 tests — 16 at build, plus 2 added at `/du6-polish` closing the review's non-integer-`bye_week` and orphaned-`.tmp` CONCERN/SUGGESTION) plus `+1` in `tests/player_data_fetcher/test_player_data_exporter.py` (33 → 34, the module-level delegation regression). The merge base `origin/main` carries 152 files, so the remaining drift predates this branch (D3.1 and D3.4 merged after the 2026-08-06 measurement). Raised at `/du5-review` as a **Documentation Currency CONCERN** — the stated count is a tool-checkable claim this unit's own diff partly falsifies — and applied at `/du6-polish` under a user-approved amendment to the unit's diff manifest, since this path sits outside it (the identical class and handling as the D8.2/D8.3/D8.4 entries below). The figure supersedes the D8.4 entry's figure; no other section changed, and no template drift (slug: D3.2-repair-live-pool-203-records-in-place)
  - 2026-08-08: Mode C refresh after framework import — reconciled the document to the current six-stage delivery-ticket flow, which retired ticket-scope test-plan and test-execution stages. `/du4-test` is now the sole delivery test stage: it always runs the full declared suite to green and writes unit `testing_results.md`; it conditionally authors and executes a thin unit `user_test_plan.md` when the non-author determination says the unit changes user-observable behavior, recording (but never gating on) its disposition. `/dt5-review` and archive-only `/dt6-finalize` consume the units' test evidence and write no ticket-scope `testing_results.md`. Replaced the retired `/dt7-review` / `/dt8-polish` documentation ownership references with `/dt5-review` / `/du6-polish`, and generalized the non-author test-plan determination to every unit-creation site
  - 2026-06-16: Initial creation (project initialization)
  - 2026-06-16: Populated all sections from repository research (slug: populate-shamt-project-docs)
  - 2026-06-29: Note win-rate `--seed N` determinism flag + table-block comparison in the driver entry (slug: deterministic-seeding)
  - 2026-06-29: T30 paired-comparison-in-ascent — sweep auto-seed policy + resume fingerprint-includes-seed behavior (slug: paired-comparison-in-ascent-shared-seeds)
  - 2026-07-01: T34 human-approved-promote-gate-no-auto-write — update win-rate `--promote` caution: bare `--promote` previews (no write); `--promote --confirm` writes
  - 2026-07-15: Align to master template after framework import — corrected stale Shamt phase numbers (Test→Phase 6, Review→7, Polish→8, test-plan drafting→Phase 4); added Execution mode + User test plan fields (User test plan = optional); replaced stale `manual_test_plan.md` reference with the out-of-band human routing (slug: project-doc-master-alignment)
  - 2026-07-18: Align to master template after `#187 user_test_plan_mode` import — renamed "Agent-as-user testing" → "User-driving conventions"; retired the bespoke "Execution mode" doc field (usage mode is now the `user_test_plan_mode` config key, set to `agent-run` for this project); refreshed the Purpose to the config-key framing
  - 2026-07-19: Conform the "User test plan" convention to the agent-run rule — `user_test_plan.md` is now **required on every story** (per-story opt-out is honored only under `human-reference`, unused here); retired the earlier "optional (ask per story)" stance; guidance reframed from whether-to-author to plan depth-by-surface (slug: stale-tests-readme follow-up)
  - 2026-07-30: T81 team-selection-index-unvalidated — added the piped-drive line-accounting note to the League Helper driver entry (an out-of-range choice now re-prompts, consuming one extra stdin line). The review's *stronger* contingent ask (a hang warning + a mandatory `timeout` wrapper on every piped drive) is deliberately **not** applied: it was contingent on the BLOCKING infinite loop shipping, and that was fixed in the same story (slug: T81-team-selection-index-unvalidated-silent-misassign)
  - 2026-07-27: Mode C refresh after framework import — retired the dangling `testing_plan.md` references (the artifact and its template are gone framework-wide; this doc's "Automated test infrastructure" section is now the Phase-6 run-source), added the template's `Working directory` + `Whole-suite run + pass/fail interpretation` fields, and added the missing falsified-clause Update Trigger
  - 2026-08-01: T82 — documented the `LEAGUE_DATA_DIR` scratch-data-tree redirect in the League Helper driver entry (mechanism `league_helper/LeagueHelperManager.py:235`, precedent `tests/integration/test_league_helper_e2e.py:40`), which answers that entry's pre-existing "Modify Player Data writes `data/player_data/*`" caution and was T82's whole Phase-6 driving mechanism; added the matching clarification to the "Files written" observation bullet (slug: T82-player-search-shows-zero-points-transient-score)
  - 2026-08-02: T83 — EOF is now terminal for the whole session, so "letting the pipe run out" no longer leaves a mode: added the EOF-is-terminal rule to the League Helper driver entry (every piped drive must supply a complete, exactly-counted script terminated by `6` and state its expected exit code — `0`/`1`/`130`), mirrored the three statuses into the "What to observe" League Helper bullet, and **corrected the line-short example drive** at "Representative inputs" (`printf '2\n6\n'` → `printf '2\n\n6\n'`; the blank line satisfies Starter Helper's `Press Enter to Continue...`, `StarterHelperModeManager.py:311` — both drives re-executed under a `LEAGUE_DATA_DIR` scratch tree, exit `1` vs exit `0`) (slug: T83-menu-eof-unhandled-traceback-ctrl-d)
  - 2026-08-02: T88 test-subprocess-calls-lack-timeout-hang-guard — re-quoted the whole-suite **red** signal line to match the runner's new percentage-free output (`FAILURE: {failed} of {total} TESTS DID NOT PASS ({passed} passed)` — "DID NOT PASS" because the count includes collection/import errors as well as assertion failures, per Copilot review feedback on PR #72; plus the second `FAILURE: {N} TEST FILE(S) FAILED TO RUN` form for the timeout/exception path), and made the **mode distinction** explicit: the default flagless invocation (the Phase-6 run-source) and the `--single` mode print *different* red lines. The green line is unchanged. The §"User-driving conventions" win-rate entry ("a ranked strategy/win-rate table is printed and the process exits `0`") was re-verified against `run_win_rate_simulation.py:610-611` and is **correct as written — left unchanged** (slug: T88-test-subprocess-calls-lack-timeout-hang-guard)
  - 2026-08-03: T91 exporter-test-writes-real-player-data — corrected the false "2-dummy-player, all-zero-projection placeholder" description of the committed `data/player_data/` (it holds 799 players / 167,211 lines; the placeholder description was a fossil of T91's own wipe), re-motivated the retained `tests/fixtures/player_data/` overlay from "the tracked tree is worthless" to "pin a refresh-independent pool", documented the new `PLAYER_DATA_DIR` data-root redirect (`player_data_fetcher/config.py::data_root()`, the player-data parallel of `LEAGUE_DATA_DIR`), and documented `tests/run_all_tests.py`'s new baseline-diff `data/` cleanliness backstop and its pre-commit consequence (slug: T91-exporter-test-writes-real-player-data)
  - 2026-08-03: T75 — refreshed the whole-suite figure after deleting ConfigGenerator's 15 production-unreachable members and their 29 dead tests (3,351 -> 3,322 across 150 files) (slug: T75-configgenerator-dead-and-broken-methods)
  - 2026-08-04: Mode C refresh after framework import — retired the accuracy simulation's stale **"endless runner"** guidance at all four sites (the driver entry, Representative inputs, What to observe, Standard scenario 4). T69 (commit `32a00a54`) made the run convergent and self-terminating: the entry calls `main()` once (`run_accuracy_simulation.py:492-501`) and exits `0` on success, so the smoke now asserts **exit `0`** and a `timeout` wrapper is a hang bound (`timeout 600`, sized against a measured ~56s / 96-config run on 2026-08-04) rather than the pass signal — exit `124` now means a hang. Also corrected the driver entry's objective description from "by MAE" to pairwise ranking accuracy with MAE as a diagnostic, matching `ARCHITECTURE.md` → Component 3 (T45) and the runner's own `(diag)` output. No template drift: the section set still matches the current imported `testing_standards.template.md`. Also repaired two line citations that had drifted since T82 (`LeagueHelperManager.py:229` → `:235`, `test_league_helper_e2e.py:46` → `:40`; both re-derived by grep on 2026-08-04). The §"Out of scope" `--endless` mention was adversarially challenged and is **correct as written** — that flag belongs to the *win-rate* runner (`run_win_rate_simulation.py:57`) and still exists; only the *accuracy* runner's endless behavior was removed by T69. Finally, refreshed the whole-suite figure from the stale `3,322` to **3,352 tests across 150 files**, measured by a full green run of the declared run-source on 2026-08-04, and retired the running T75/3,351-baseline lineage in favour of a plain measured figure
  - 2026-08-05: Mode C refresh after the project's conversion to `flow_track: delivery`. Re-pointed every flow-facing reference off the retired Phase-4/Phase-6 Engineer vocabulary onto the two delivery test stages — `/du4-test` (per unit, suite green, blocks the unit's own merge) and `/dt6-execute-tests` (ticket scope, suite + ticket-scope user test plan) — including the frontmatter `How to Update` block, the Purpose, and five sites in the §"Whole-suite run + pass/fail interpretation" bullet. Added the Purpose's new post-hoc caveat: `/dt6` runs AFTER every unit has merged, so the real ship gates are `/du4-test` and `/du5-review`. **Substantively rewrote the user-test-plan rule** from the single "required on every story" into the delivery track's genuine two-level contract — ticket-scope (`/dt5-write-test-plan`, always authored, and under this project's `agent-run` setting it IS the verification with a recorded verdict) versus unit-scope (`/du4-test`, optional and thin, required only when the unit changes user-observable behavior, the determination made by a NON-AUTHOR at `/dt4-decompose` and escalatable-but-never-downgradable, with an absent plan skipped rather than pending and `testing_results.md` as the stage's completion signal). No template drift; no change to the automated-suite declaration or the driving conventions. Round 1 of validation caught three surviving Engineer-flow references the initial sweep's `Phase [0-9]` pattern missed because they were hyphenated or noun-form (`Phase-6` in the `LEAGUE_DATA_DIR` note, "the ones a story touches" in Standard scenarios, and "the story's `user_test_plan.md` ... required Phase-6 pass" in Out of scope)
  - 2026-08-05: D8.2 coverage-measurement-reporting-only — refreshed the whole-suite figure in §"Automated test infrastructure" from the stale **3,352 tests across 150 files** to **3,375 across 151**, measured 2026-08-05 by a full green run of the declared run-source (`SUCCESS: ALL 3375 TESTS PASSED (100%)`), with the file count independently re-derived by `find tests -name "test_*.py" | wc -l`. The unit adds `tests/simulation/shared/test_sim_data_coverage.py` (the +1 file) plus call-site cases in `tests/root_scripts/test_validate_sim_data.py`. Raised at `/du5-review` as a **Documentation Impact: Required** finding — the stated count is a tool-checkable claim this unit's own diff falsifies — and applied at `/du6-polish` under a user-approved amendment to the unit's diff manifest, since this path sits outside it. The figure supersedes the 2026-08-04 lineage entry above; no other section changed, and no template drift (slug: D8.2-coverage-measurement-reporting-only)
  - 2026-08-05: D8.3 coverage-enforcement-exit-1 — refreshed the whole-suite figure in §"Automated test infrastructure" from **3,375 across 151 files** to **3,390 across 151**, measured 2026-08-05 by a full green run of the declared run-source (`SUCCESS: ALL 3390 TESTS PASSED (100%)`, exit `0`), with the file count independently re-derived by `find tests -name "test_*.py" | wc -l`. **The file count is unchanged** — this unit adds no test file (`**Test Build Plan:** none` on `unit.md` holds); the whole `+15` lands in the existing `tests/simulation/shared/test_sim_data_coverage.py` (19 → 34 methods), while `tests/root_scripts/test_validate_sim_data.py` stays at 17 because its idle-property guard was **inverted in place** rather than added. Raised at `/du5-review` as a **Documentation Impact: Required / Documentation Currency CONCERN** — the stated count is a tool-checkable claim this unit's own diff falsifies — and applied at `/du6-polish` under a user-approved amendment to the unit's diff manifest, since this path sits outside it (the identical class and handling as the D8.2 entry above). The figure supersedes the D8.2 entry's figure; no other section changed, and no template drift (slug: D8.3-coverage-enforcement-exit-1)
  - 2026-08-05: D8.4 harness-exclusion-accuracy-opt-in-flag — refreshed the whole-suite figure in §"Automated test infrastructure" from **3,390 across 151 files** to **3,411 across 151**, measured 2026-08-05 by a full green run of the declared run-source (`SUCCESS: ALL 3411 TESTS PASSED (100%)`, exit `0`), with the file count independently re-derived by `find tests -name "test_*.py" | wc -l`. **The file count is unchanged** — this unit adds no test file (`**Test Build Plan:** none` on `unit.md` holds). The `+21` is the unit's own `+17` (recorded at `/du5-review` as 3,407 at commit `54b83bd8`) plus the `+4` `/du6-polish` added when closing the review's two test-coverage CONCERNs: one manager→runner wiring assertion in `tests/simulation/test_AccuracySimulationManager.py`, and three in `tests/simulation/shared/test_sim_data_coverage.py` (the `OSError` and `KeyError` fail-open arms of `excluded_weeks_by_season`, plus the unmeasurable-season summary line). Raised at `/du5-review` as a **Documentation Impact: Required / Documentation Currency CONCERN** — the stated count is a tool-checkable claim this unit's own diff falsifies — and applied at `/du6-polish` under the same user-approved diff-manifest amendment the D8.2 and D8.3 entries record, since this path sits outside the unit's manifest (the identical class and handling as the two entries above). The figure supersedes the D8.3 entry's figure; no other section changed, and no template drift (slug: D8.4-harness-exclusion-accuracy-opt-in-flag)
Update Triggers: |
  Update this document when:
  - The way the project is run/driven as a user changes (new entry point, new CLI, new flow)
  - Automated test infrastructure is added, removed, or its runner/command changes
  - A new class of behavior needs a documented user-driving procedure
  - A recurring test-surfaced bug reveals a missing standard scenario worth codifying
  - When adding an entry, re-read this document's own overview/status/summary prose and flag any clause the new entry falsifies; re-run until a clean pass.
How to Update: |
  Open a delivery ticket (or a framework-update proposal if this is a shamt-core change), follow the
  delivery track, and amend the relevant sections of this file. `/du5-review` (per unit) and
  `/dt5-review` (cross-unit) flag whether a change implies an update; `/du6-polish` applies
  per-unit documentation fixes and re-validates. `/update-project-doc` is the direct route for a doc-only edit.
  Run `/validate-artifact .shamt-core/project-specific-files/TESTING_STANDARDS.md` after substantive edits.
  Keep `Last Updated` current and add an `Update History` entry with the triggering ticket/unit or
  proposal slug.
---

# Project Testing Standards

**Purpose:** The source of truth for how this project is verified. This project runs the **delivery
track** (`flow_track: delivery`), whose sole test stage is **`/du4-test`** at unit altitude. That stage
reads the automated-suite declaration, blocks until the whole suite is green, always writes the unit's
`testing_results.md`, and conditionally authors and executes a thin unit `user_test_plan.md` from these
user-driving conventions. This project sets **`user_test_plan_mode: agent-run`** in
`.shamt-core/shamt-config.json`, so an authored unit plan is executed by `user-simulator` and its
disposition is recorded; the disposition never gates later stages. Under `human-reference`, the plan
would instead be a document a human tester follows. The standards are also threaded into
`/dt3-design`'s test strategy. The user-test-plan **usage mode** is the `user_test_plan_mode` config
key, not a field here.

**Ticket altitude has no test-plan or test-execution stage.** `/dt5-review` and archive-only
`/dt6-finalize` read every non-withdrawn unit's `testing_results.md`; neither writes a ticket-scope
`testing_results.md`. The ship gates therefore remain at unit altitude: `/du4-test` supplies the
green-suite evidence and `/du5-review` gates the unit's merge.

---

## Automated test infrastructure

- **Status:** **Present.**
- **Runner / command:** `python tests/run_all_tests.py` — the canonical full-suite gate; it discovers every `test_*.py` under `tests/`, runs each through `pytest` with `-m "not live_api"`, and **requires a 100% pass rate** (exit `0` = all passed, `1` = any failure **or** a run that dirtied `data/` — see the data-cleanliness backstop below). The offline suite is **3,495 tests across 153 files** (measured 2026-08-10 by a full green run of this runner — `SUCCESS: ALL 3495 TESTS PASSED (100%)`, exit `0`; file count re-derived by `find tests -name "test_*.py" | wc -l`). The pre-commit wrapper `python run_pre_commit_validation.py` calls the same runner.
  - Direct pytest equivalent: `.venv/bin/python -m pytest tests/ -m "not live_api"`.
- **Working directory:** the **project root** (`/home/kai/code/FantasyFootballHelperScripts`) — this is a `single-repo` layout, so both the runner and any direct `pytest` invocation are run from there, using the project virtualenv (`.venv/bin/python`). `tests/conftest.py` puts the repo root on `sys.path`, so a run from any other directory will fail to import the source packages.
- **Test file layout / naming:** `tests/` mirrors the source tree; files are `test_<module>.py` (a module may be split into `test_<module>_<aspect>.py`). Buckets include `tests/league_helper/`, `tests/simulation/`, `tests/player_data_fetcher/`, `tests/integration/`, `tests/unit/`, `tests/root_scripts/`, plus committed offline `tests/fixtures/`.
- **How to run a single test / suite:**
  - One file: `.venv/bin/python -m pytest tests/league_helper/util/test_PlayerManager_scoring.py -v`
  - One class: `... test_PlayerManager_scoring.py::TestConsistencyMultiplier -v`
  - One method: `... ::TestConsistencyMultiplier::test_consistency_excellent_low_cv -v`
  - Note: `-m "not live_api"` is implied by the project runner; add it yourself when invoking pytest directly so no test reaches the network.
  - **`-k` caution:** pytest `-k` substring tokens must be contiguous substrings of method names; exit code `5` means "matched nothing," not a failure.
- **Markers (`pytest.ini`):** `live_api` (requires live ESPN access — excluded from the default run) and `offline`. The default suite is **fully offline**.
- **Whole-suite run + pass/fail interpretation:** the exact invocation `/du4-test` blocks-until-green on for every unit is `python tests/run_all_tests.py`, run from the project root — the **whole** declared offline suite, never a unit-scoped subset. Read pass/fail from the **exit code** (`sys.exit(0 if success else 1)`): `0` = every test passed (the runner enforces a strict 100% pass rate); `1` = at least one test failed **or no tests were discovered** (`FAILURE: NO TESTS DISCOVERED (0/0)` also exits `1`, so an empty run can never read as green). Confirming output lines **of the default, flagless invocation — the run-source `/du4-test` uses**: `SUCCESS: ALL {N} TESTS PASSED (100%)` on green; `FAILURE: {failed} of {total} TESTS DID NOT PASS ({passed} passed)` plus a `Failed test files:` list and per-file `[FAIL]` lines on red. The wording is **"DID NOT PASS", not "FAILED"**, because the runner's `total_count` is `passed + failed + error` (`_parse_test_results`), so the count legitimately includes collection/import **errors** as well as assertion failures. A second red form, `FAILURE: {N} TEST FILE(S) FAILED TO RUN ({passed} tests passed)`, is printed when a file produced **no** test-level counts at all — the timeout/exception path — where a test-level count would misreport `0` failures. **The red line carries no percentage** (since T88) — a near-perfect run can no longer round to `100.0%` on a failing line. **Mode distinction:** the `--single` / `-s` mode is a *different* code path and prints a *different* red line — `FAILURE: {passed}/{total} TESTS PASSED`, with no failure count — so that form must not be expected from the flagless invocation `/du4-test` uses; both modes print the same green line. The exit code is the signal the test stage interprets as green.
- **CI:** None checked in. The suite is run locally as the pre-commit gate (`run_pre_commit_validation.py`).

## User-driving conventions (how a human runs the project; plan authored per the User test plan mode)

How this project is driven **as a user** when a user test plan is executed. The interactive League
Helper and both simulation engines run **fully offline from committed data** (no network), so the
`user-simulator` persona can drive them directly. Always use `.venv/bin/python` from the project root.

- **Usage mode:** this project sets **`user_test_plan_mode: agent-run`** in
  `.shamt-core/shamt-config.json` (the config key, not a field here), so `/du4-test` dispatches the
  `user-simulator` persona to **execute** an authored unit `user_test_plan.md` and records the
  `agent_test_session_{datetime}.md` verdict in `testing_results.md`. That disposition is evidence,
  never a downstream gate. The narrow set of scenarios the agent genuinely cannot simulate is
  enumerated under "Out of scope for the agent" below and handled out of band by a human.
- **User test plan — unit-only, optional and deliberately thin.** The delivery track has no
  ticket-scope test plan. A unit plan is a *slice-validation* artifact scoped to that unit's own
  change. It is **required when the unit changes user-observable behavior** and optional when it does
  not. Three rules matter: (1) the determination is made by a **non-author** at whichever unit-creation
  site created the unit — `/dt4-decompose`, the ticket review, a `/du1-spec` or `/du2-plan` split, or a
  `/du5-review` + `/du6-polish` spawn — and `/du1-spec` or `/du4-test` may **escalate it, never
  downgrade it**, because the unit's own author is the party most likely to underestimate it; (2) an
  absent unit plan is **skipped, never pending** — no stage halts on it and nothing downstream gates on
  its presence or verdict; (3) `/du4-test` always writes `testing_results.md`, whose presence is the
  stage's completion signal.
  - **Depth guidance:** scale to the surface. Work touching an interactive or
    user-facing surface (a League Helper mode, a simulation driver's CLI/observable behavior, a
    fetcher's offline flow) gets a full user-driven scenario set; work with little or no user-facing
    surface (a pure internal refactor, a docs-only change) asserts that observable behavior is
    **unchanged**, with the declared automated suite (see "Automated test infrastructure" above) as
    the backstop.
- **How to run / drive the project:**

  1. **League Helper (interactive — the primary user surface).**
     ```bash
     printf '<menu-choices>\n' | .venv/bin/python run_league_helper.py
     ```
     It prints a banner (config name, week, scoring format, roster size) then a numbered MAIN MENU:
     `1. Add to Roster`, `2. Starter Helper`, `3. Trade Simulator`, `4. Modify Player Data`,
     `5. Save Calculated Projected Points`, `6. Quit`. Drive it by piping the numbered choices it
     prompts for on stdin (each prompt is a number; sub-menus prompt further). To exit cleanly, send
     `6` (Quit). Optional flags: `--week N` (override the NFL week in-memory), `--enable-log-file` (write
     rotating logs under `logs/<script>/` instead of console-only).
     **Caution:** Modify Player Data mode (`4`) *writes* `data/player_data/*` — only exercise it in a
     scratch checkout or when the spec intends a data edit.
     **`LEAGUE_DATA_DIR` — the supported scratch-data-tree redirect (since T82, 2026-08-01).** This is
     the answer to the Caution above, and the preferred one: rather than a scratch *checkout*, point the
     helper at a scratch *data tree*. `LEAGUE_DATA_DIR` is an already-existing environment variable read
     at `league_helper/LeagueHelperManager.py:235`
     (`data_path = Path(os.environ["LEAGUE_DATA_DIR"]) if os.environ.get("LEAGUE_DATA_DIR") else base_path / "data"`),
     with an in-repo precedent at `tests/integration/test_league_helper_e2e.py:40`
     (`env["LEAGUE_DATA_DIR"] = str(data_dir)`). Recipe:
     ```bash
     S=$(mktemp -d)
     cp -a data "$S/data"                                  # copy the WHOLE root, not just player_data/.
                                                           # Required: the league config — this repo uses
                                                           # data/configs/league_config.json (ConfigManager
                                                           # also accepts a legacy data/league_config.json).
                                                           # Optional but wanted for a realistic drive:
                                                           # data/team_data/ and data/season_schedule.csv —
                                                           # absent, they only warn-and-continue, so a
                                                           # partial copy degrades silently rather than
                                                           # failing loudly.
     cp tests/fixtures/player_data/*_data.json "$S/data/player_data/"   # overlay a realistic player pool
     export LEAGUE_DATA_DIR="$S/data"                      # export, not a prefix on `printf`
     printf '<menu-choices>\n' | .venv/bin/python run_league_helper.py
     ```
     Every write the interactive modes perform (including Modify Player Data's
     `data/player_data/*` writes) then lands in the disposable scratch tree; assert the tracked tree was
     never touched with a closing `git status --porcelain -- data/` that prints nothing. **The committed
     `data/player_data/` holds the real live dataset** — verified on `main` @ `b4cc1a88` (2026-08-02) as
     **799 players across the six position files, 167,211 lines total** (qb 105, rb 172, wr 294, te 159,
     dst 32, k 37). This doc previously described that tree as "a 2-dummy-player, all-zero-projection
     placeholder"; that description was a **symptom of T91**, in which a suite run overwrote the tracked
     tree with two synthetic test players, and it is corrected here. The
     `cp tests/fixtures/player_data/*_data.json` overlay above is **retained**, with its motivation
     restated: it pins a **stable, refresh-independent player pool** (6 committed fixture files, dated
     2026-03-30) so a drive's expected figures do not move whenever the tracked tree is refreshed — not
     because the tracked tree is worthless. A drive against the tracked tree is a legitimate drive.
     This was T82's entire test-phase driving mechanism. No `--data` CLI flag exists or is needed.
     **`PLAYER_DATA_DIR` — the player-data-fetcher's equivalent redirect (since T91, 2026-08-03).**
     The `player_data_fetcher` package reads `PLAYER_DATA_DIR` through the single shared resolver
     `player_data_fetcher/config.py::data_root()`, which every path default in `DataExporter.__init__`,
     the `Settings` dataclass, and `run_player_fetcher.py`'s argparse defaults routes through. Like
     `LEAGUE_DATA_DIR`, it names the **data ROOT** — the directory that *contains* `player_data/`,
     `team_data/` and `drafted_data.csv` — **not** the `player_data/` subdirectory. Unset, every path
     resolves to exactly its historical repo-anchored value. Resolution happens at **construction time**,
     so setting the variable after import still takes effect. Caution: exporting it persistently in a
     shell makes a real `run_player_fetcher.py` fetch write into the scratch tree instead of `data/` —
     the failure is loud (the tracked tree simply does not change), not destructive.
     **Runner-level `data/` backstop (since T91, 2026-08-03).** `tests/run_all_tests.py` now snapshots
     `git status --porcelain -- data/` before and after the run and fails the run — exit non-zero, even
     when every test passed — if a path is **newly** dirtied, naming each one. It is a baseline **diff**,
     not a clean-tree assertion, so a developer with in-flight `data/` edits gets no false red; an
     already-dirty path that is further modified during the run is a documented, accepted blind spot.
     When `git` is unavailable or the runner is outside a git work tree, it prints a notice and skips.
     Because `run_pre_commit_validation.py` calls the same runner, this is also a pre-commit gate.
     **Line accounting (since T81, 2026-07-30):** a numbered menu now *re-prompts* on an out-of-range
     choice instead of returning it, so every deliberate out-of-range line in a piped drive consumes
     **one extra** stdin line — follow each with a valid choice or the pipe runs short.
     **EOF is terminal (since T83, 2026-08-02):** an exhausted or closed stdin ends the whole
     *session*, not just the active mode — the app prints `No input available on stdin — exiting.`
     and exits **`1`**. "Letting the pipe run out" is therefore no longer a way to leave a mode, and a
     drive whose script is one line short ends early with its remaining assertions unreached rather
     than falling through to a menu. Combined with the line-accounting rule above, **every piped
     drive must supply a complete, exactly-counted input script terminated by `6`, and must state its
     expected exit code** (`0` for a clean Quit, `1` for a deliberate EOF scenario) so a short pipe
     can never be mistaken for a pass. Ctrl+C exits **`130`**. Note that not every consumed line is a
     menu number: a mode may prompt `Press Enter to Continue...` (e.g.
     `StarterHelperModeManager.py:311`), which consumes one **blank** line — count it.

  2. **Win-rate simulation (offline replay).**
     ```bash
     .venv/bin/python run_win_rate_simulation.py --sims 1 --workers 2 --strategy 1_zero_rb.json
     ```
     Replays committed seasons under `simulation/sim_data/` and prints a ranked strategy table.
     `--strategy <basename>` limits it to one of the ~50 files in
     `simulation/sim_data/draft_order_possibilities/` (fast smoke). Omit `--strategy` for a full run.
     `--seed N` makes the run deterministic (same seed → identical ranked table); omit it for the
     default stochastic behavior. For a reproducibility/determinism check, run twice with the same
     `--seed K` and compare the `Strategy Win Rate Summary` table block — note that log lines are
     written to **stdout** with timestamps, so compare the extracted table (e.g.
     `sed -n '/Strategy Win Rate Summary/,$p'`), not the raw capture.
     **Caution:** Bare `--promote` *previews* (dry-run, no write); `--promote --confirm` *writes*
     `data/configs/league_config.json` — only use `--promote --confirm` when promotion is the
     intended behavior under test.
     **Sweep auto-seed policy (T30):** `--sweep` without `--seed` auto-assigns a base seed from OS
     entropy, logs it at INFO as `Auto-assigned sweep base seed: N (re-run with --seed N to reproduce)`,
     and embeds it in the resume fingerprint. This means an unseeded `--sweep` re-run starts fresh
     (fingerprint mismatch, no silent seed-mixing) while an explicit `--seed N` re-run resumes cleanly
     (same fingerprint). The logged seed is re-passable via `--seed N` to reproduce the exact paired
     coordinate-ascent draws.

  3. **Accuracy simulation (offline replay).**
     ```bash
     .venv/bin/python run_accuracy_simulation.py --test-values 2 --params NORMALIZATION_MAX_SCALE
     ```
     Tournament-optimizes scoring parameters against the committed sim data (objective = pairwise
     ranking accuracy; MAE is reported as a diagnostic) and writes result folders under
     `simulation/simulation_configs/`. `--compare FOLDER_A FOLDER_B` inspects results without
     running. **Caution:** `--promote [FOLDER]` *writes* into `data/configs/`.
     **Convergent and self-terminating (since T69, 2026-08-04):** the optimization run **ends on its
     own and exits `0`** — the entry point calls `main()` exactly once
     (`run_accuracy_simulation.py:492-501`), and the multi-pass loop lives inside the ascent driver,
     which stops when every horizon has converged or hits its bound. `main()` exits `0` on success
     and `1` on failure, so the smoke asserts **exit `0`**, not a timeout. This **supersedes** the
     former "endless runner" guidance (`while True: main()`, never exiting `0`, exit `124` accepted
     as the pass signal) — that behavior was removed by T69, and there is deliberately no
     `--endless` opt-back-in. A `timeout` wrapper is still worth using as a **hang bound** (per
     `CODING_STANDARDS.md` → Subprocess timeouts), sized well above the real runtime rather than as
     a performance budget: the two-value single-parameter smoke above completed in **~56s / 96
     configs tested** (measured 2026-08-04), so `timeout 600` is a comfortable bound. Exit `124`
     now means the run **hung**, not that it passed.

  4. **Data fetchers (offline, via recorded fixtures).** The reliable, verified offline driver for the
     fetchers/compiler is the **committed integration suite**, run with `ESPN_FIXTURE_DIR` so every
     ESPN request reads a JSON fixture instead of the network:
     ```bash
     ESPN_FIXTURE_DIR=tests/fixtures .venv/bin/python -m pytest tests/integration/ -m "not live_api" -q
     ```
     This exercises the schedule/player/game fetchers and the historical compiler offline end-to-end
     (e.g. `test_offline_mode_runners_integration.py`, `test_player_data_fetcher_e2e.py`,
     `test_schedule_fetcher_e2e.py`) — expect `... passed` and exit `0`. The `schedule` runner also
     drives cleanly offline as a one-off (`ESPN_FIXTURE_DIR=tests/fixtures .venv/bin/python
     run_schedule_fetcher.py --season 2024 --force-refresh`). In offline mode a missing fixture raises
     `FileNotFoundError` with recording instructions (it does **not** silently hit the network).
     **Do not** drive `run_player_fetcher.py` directly as an offline smoke — the committed fixtures do
     not cover its full player-pool fetch, so the raw runner can hang waiting on data; use the
     integration suite above for offline fetcher coverage. Recording new fixtures
     (`ESPN_RECORD_FIXTURES_DIR=...`) **does** make live calls and is human/network-gated — see
     "Out of scope" below.

  5. **Sim-data validation utility.**
     ```bash
     .venv/bin/python validate_sim_data.py --year 2025
     ```
     Sanity-checks a compiled `simulation/sim_data/{YEAR}/` tree (exit `0` pass / `1` fail).

- **Representative inputs:**
  - *League Helper, valid:* `printf '6\n'` (launch → Quit) is the minimal smoke, exit `0`;
    `printf '2\n\n6\n'` drives Starter Helper then quits, exit `0` — the **blank second line**
    satisfies Starter Helper's terminal `Press Enter to Continue...`
    (`StarterHelperModeManager.py:311`), without which the `6` is consumed there and the drive dies
    at EOF with exit `1` instead of quitting (both drives executed against a `LEAGUE_DATA_DIR`
    scratch tree on 2026-08-02; the previously documented `printf '2\n6\n'` was line-short). For
    draft flow, follow the prompts to pick a mode and enter drafted players when asked.
  - *League Helper, deliberate EOF:* `printf '2\n'` (or `printf ''`) ends the session at the first
    exhausted read — expect `No input available on stdin — exiting.` and exit `1`, never a traceback.
  - *League Helper, edge/invalid:* an out-of-range menu number (e.g. `9`) should be rejected with
    "Invalid choice. Please try again." and re-prompt — it must not crash.
  - *Win-rate, valid:* `--sims 1 --workers 2 --strategy 1_zero_rb.json`. *Edge:* `--strategy
    does_not_exist.json` should log "matched no strategy files" and exit non-zero (clean error, no
    traceback dump).
  - *Fetcher offline, valid:* `ESPN_FIXTURE_DIR=tests/fixtures ... -m pytest tests/integration/ -m
    "not live_api"` (the verified offline driver). *Edge:* a season/week with no committed fixture
    should raise a clear `FileNotFoundError` with recording instructions, not a silent network call.
  - *Accuracy sim, valid:* `timeout 600 .venv/bin/python run_accuracy_simulation.py --test-values 2
    --params NORMALIZATION_MAX_SCALE` — expect **exit `0`** with a result folder written under
    `simulation/simulation_configs/` (~56s on the 2026-08-04 measurement; the `timeout` is a hang
    bound, so exit `124` is a failure). *Compare (one-shot):* `--compare FOLDER_A FOLDER_B` inspects
    results and exits `0` without running.

- **What to observe (expected behavior):**
  - **Exit code `0`** on success for the non-interactive scripts; a clean, single-line error message
    (not an unhandled traceback) plus non-zero exit on bad input.
  - **League Helper:** banner + menu render, prompts accept piped input, `6` exits with "Goodbye!"
    and exit `0`; invalid choices re-prompt rather than crash. **Every drive states its expected exit
    code** (since T83, 2026-08-02): `0` = clean Quit via `6`; `1` = stdin exhausted or closed, which
    ends the whole session with the single line `No input available on stdin — exiting.` (a
    line-short pipe therefore reads as this, *not* as a fall-through to the menu); `130` = Ctrl+C,
    with the single line `Interrupted — exiting.`. None of the three prints a Python traceback.
  - **Win-rate sim:** a ranked strategy/win-rate table is printed and the process exits `0`.
  - **Accuracy sim:** result/optimal config folders appear under `simulation/simulation_configs/`
    and the run **terminates on its own with exit `0`** (since T69) once every horizon has converged
    or hit its bound; `--compare` / `--promote` also exit `0`. A `timeout`-wrapped smoke returning
    exit `124` now indicates a **hang**, not a pass.
  - **Files written** match the documented writer for the action (and *only* those files): Modify
    Player Data → `data/player_data/*`; `--promote` → `data/configs/league_config.json`; fetchers →
    their `data/` or `sim_data/` targets. Confirm no unexpected file is mutated. Under a
    `LEAGUE_DATA_DIR` drive (see the League Helper entry above) the League Helper's `data/…` writes are
    rooted at the scratch tree instead, so the tracked `data/` must show **zero** changes.
  - **Logs** go to console by default; with `--enable-log-file`, rotating files appear under
    `logs/<script>/`. No secrets or sensitive data in output.

- **Standard scenarios** (exercise the ones the unit or ticket touches):
  1. **Launch-and-quit smoke** of the League Helper (`printf '6\n' | ... run_league_helper.py`,
     expect exit `0` + "Goodbye!").
  2. **Each affected League Helper mode** driven through its prompts to a recommendation/result and
     back to Quit, verifying the on-screen output is sensible and the process exits cleanly.
  3. **Win-rate single-strategy smoke** (`--sims 1 --strategy <file>`) when scoring/simulation code
     changed — confirm a ranked table prints and exit `0`.
  4. **Accuracy single-parameter smoke** (`timeout 600 ... --test-values 2 --params <NAME>`) when
     accuracy/scoring code changed — confirm result folders are produced and the run exits `0` on its
     own (the `timeout` is a hang bound; exit `124` is a failure).
  5. **Offline fetcher coverage** via the integration suite (`ESPN_FIXTURE_DIR=tests/fixtures ...
     pytest tests/integration/ -m "not live_api"`) when fetcher/parsing/compiler code changed —
     confirm fixtures are read end-to-end and the suite exits `0`.
  6. **Config-edit round-trip** when config handling changed: read with `ConfigManager`/League Helper,
     confirm the expected parameter is applied (e.g. correct week override loaded).
  7. Re-run the **automated suite** (`python tests/run_all_tests.py`) as the backstop after any change.

- **Out of scope for the agent (human-only)** — scenarios the agent cannot simulate, handled out of
  band by a human and never scoped into a unit `user_test_plan.md`; the required `/du4-test` automated-suite pass remains fully offline:
  - **Live network fetches / fixture recording:** any run *without* `ESPN_FIXTURE_DIR` (real ESPN /
    Open-Meteo calls) and any `ESPN_RECORD_FIXTURES_DIR` recording run — network- and time-dependent,
    and dependent on the external APIs being up.
  - **The Chrome extension** (`nfl-fantasy-exporter-extension/`): requires Chrome, "Load unpacked",
    and a logged-in fantasy.nfl.com session; it cannot be driven headlessly here. Its output
    (`data/drafted_data.csv`) can be simulated with a hand-built CSV for downstream tests.
  - **Full-scale simulation sweeps** (multi-hour `--sweep` / full grid / `--endless`): correctness is
    smoke-tested at small `--sims`; the long optimization runs are a human-launched activity.
  - **Excel export visual inspection:** the Manual Trade Visualizer writes `.xlsx`; verifying its
    rendered formatting (vs. that the file is produced) is a human check.

---
Validated 2026-08-08 — 1 rounds, 1 adversarial sub-agent confirmed (sha256:7614e5c878052841) (Mode C refresh: unit-only delivery testing model)
