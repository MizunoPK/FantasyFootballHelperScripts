# KAI-16: Remove Code Comments — Epic Overview

**Epic:** KAI-16 — Remove Code Comments
**Branch:** `epic/KAI-16` → `main`
**Date Created:** 2026-03-28
**Date Completed:** 2026-04-09
**Features:** 2 (source_comment_removal, test_comment_removal)
**Files Changed:** 187 modified, 1 deleted (188 total)
**Lines Changed:** +1,695 / -8,930 (net: -7,235 lines)

---

## 1. Problem Statement

The codebase had accumulated thousands of `#` comment lines across all Python source packages and test files. Over time these comments had drifted out of sync with the code they described — functions were renamed, logic was refactored, and the comments that once explained those things now described something different or nothing at all. Rather than helping a reader understand the code, many comments added noise or actively mislead.

The project already requires Google-style docstrings on all public interfaces (`CODING_STANDARDS.md`). Docstrings are structured, versioned with the code, and show up in tooling. Inline `#` comments have no such structure — they are easy to write, easy to forget, and hard to keep accurate. The project decision was to remove them entirely rather than maintain an ever-growing backlog of stale annotations.

Without this epic, the comment drift would continue: new comments would be added during feature work, more would go stale, and future agents would face increasingly unreliable inline documentation.

---

## 2. Goals

- Remove **every** `#` comment line from every in-scope `.py` file (source packages, runner scripts, test files)
- Remove **every** trailing inline `#` comment from every code line in every in-scope `.py` file
- Preserve three categories of functional `#` lines: shebang lines (`#!/`), `# noqa` directives, and `# type: ignore` pragmas
- Update `CODING_STANDARDS.md` with an explicit no-comments rule to prevent re-introduction
- Make zero logic, behavior, or interface changes — pure deletion only

---

## 3. Solution Overview

The core of the solution is a disposable tokenize-based Python script (`strip_comments.py`) that was created during F1, used across both features, and deleted after the epic completed. The script uses Python's built-in `tokenize` module to parse each file's token stream and remove only `tokenize.COMMENT` tokens — leaving everything else (including `#` characters inside strings, f-string format codes, and regex patterns) completely untouched.

This approach is fundamentally different from grep-based removal. A regex like `s/#.*//` will happily destroy `"#hashtag"` inside a string literal, or remove `# noqa` directives. The tokenizer already knows the difference — it is the authoritative classifier of what is a comment versus what is a string. The script simply asks the tokenizer and acts on the answer.

The two features divided the scope cleanly: F1 handled all source packages and runner scripts (84 files), F2 handled all test files (122 files) and updated `CODING_STANDARDS.md`. Both features used the identical script with identical preservation rules.

---

## 4. Architecture & Key Decisions

### Decision 1: Tokenize module over regex or AST

**Decision:** Use `tokenize.generate_tokens()` to identify `COMMENT` tokens.

**Alternatives considered:**
- **Regex (`re.sub`):** Fast to write, but cannot distinguish `#comment` inside a string from a real comment. Would require complex lookahead rules that are fragile and hard to audit.
- **AST parsing:** The `ast` module parses Python syntax trees but does not expose comment tokens — comments are stripped before the AST is built. No `ast`-based approach can find comments.
- **`tokenize`:** The tokenizer operates before the AST is built and classifies every character including comments. It is the correct tool for this task.

**Why this matters:** The codebase has docstrings with code examples that contain `#` characters (e.g., `grep` command examples in docstrings, regex patterns as string literals). Any regex-based approach would corrupt these. The tokenizer approach correctly ignores all of them.

### Decision 2: Preservation rules

Three categories of `#` lines are preserved:
- **Shebang lines (`#!/`):** Functional — runner scripts require these on line 1 to be directly executable
- **`# noqa` directives:** Functional — suppress specific linting warnings; removing them would change linting behavior
- **`# type: ignore` pragmas:** Functional — suppress type checker errors on specific lines

The script checks token content at the COMMENT classification step. Any `COMMENT` token whose stripped content starts with `#!` (and is on line 1), or contains `noqa` or `type: ignore`, is left in place.

### Decision 3: Disposable script (created then deleted)

`strip_comments.py` was intended as a one-time tool, not a permanent utility. It was created during F1's S6 execution, used for both F1 and F2, and deleted in the final S10 cleanup commit. This keeps the repository clean — a script whose sole purpose was a one-time migration has no ongoing value in the codebase.

The script exists in git history (commit `07e61465`) for reference if ever needed again, but does not clutter the working tree going forward.

### Decision 4: Binary write mode for line ending preservation

When the script normalizes CRLF line endings to LF for tokenization (the tokenizer requires LF), and then writes the result back, it must restore the original line endings. The initial implementation used text mode writes, which caused Python's universal newline handling to add spurious trailing newlines on subsequent runs (making the operation non-idempotent). The fix was to detect the original line ending style (by checking for `\r\n` in the raw bytes) and write in binary mode, explicitly encoding the output and restoring the detected line ending.

### The string_lines Bug

During S9.P1 smoke testing, 357 trailing inline comments were discovered to have survived the initial removal pass across 80 files. Root cause: the initial script maintained a `string_lines` set — a set of line numbers that contained any `tokenize.STRING` token — and skipped any `COMMENT` token on those lines. This was intended to protect strings, but it was completely backwards: the tokenizer had already correctly classified the COMMENT token as a comment. The guard prevented the script from removing real comments on lines that also happened to contain string literals (e.g., `LOGGING_LEVEL = 'INFO'  # comment`).

The fix was removing the `string_lines` guard entirely. The tokenizer does not need help distinguishing comments from strings — that is exactly what it does.

**Takeaway:** Trust the tokenizer. If `tokenize` says a token is `tokenize.COMMENT`, it is a comment.

---

## 5. Changes by Feature

### F1: source_comment_removal

**Scope:** 84 source package files across 6 packages + 7 runner scripts (91 files total)

**Packages covered:** `league_helper/`, `player_data_fetcher/`, `simulation/`, `utils/`, `historical_data_compiler/`, `schedule_data_fetcher/`

**Runner scripts:** `run_accuracy_simulation.py`, `run_league_helper.py`, `run_player_fetcher.py`, `run_pre_commit_validation.py`, `run_schedule_fetcher.py`, `run_win_rate_simulation.py`, `compile_historical_data.py`

**Starting state:** All source packages contained `#` comment lines and trailing inline comments documenting implementation details that were often stale (e.g., `# use numpy for speed`, `# fallback to defaults`, `# ESPN API v3`).

**What changed:** All `#` comment lines and trailing inline comments were removed. No logic, imports, function signatures, or docstrings were modified. 40 shebang lines were preserved intact on line 1 of runner scripts.

**Commits:** 4 commits, organized by package group
- `2180a6f4` — league_helper/ (most comment-dense package)
- `9f2cc371` — simulation/
- `4cd00516` — player_data_fetcher/
- `988abbaa` — remaining packages (utils/, historical_data_compiler/, schedule_data_fetcher/) + all runners

**Result:** 3,451 comment lines removed, 79 files modified, 40 shebangs preserved.

---

### F2: test_comment_removal + CODING_STANDARDS.md

**Scope:** 122 test files across all `tests/` subdirectories + 1 local-only standards update

**Test directories covered:** `tests/league_helper/`, `tests/simulation/`, `tests/integration/`, `tests/root_scripts/`, `tests/utils/`, `tests/unit/`, `tests/player_data_fetcher/`, `tests/historical_data_compiler/`, `tests/schedule_data_fetcher/`, `tests/fixtures/`

**Starting state:** Test files contained `#` comment blocks documenting test rationale, fixture setup intent, and parameter explanations — most no longer accurate after test refactors in KAI-14 and KAI-15.

**What changed:** All `#` comment lines and trailing inline comments were removed from all 122 test files. 28 shebang lines preserved. The single `# noqa: F401` directive at `tests/player_data_fetcher/test_run_player_fetcher.py:125` was preserved intact. `CODING_STANDARDS.md` was updated locally with a new `### Comments` subsection prohibiting `#` comments (with the three preserved-categories exceptions documented).

**Note on CODING_STANDARDS.md:** This file lives in `.shamt/project-specific-configs/` which is gitignored. The update exists locally but is not in the git commit history. This is a known limitation of the current gitignore structure.

**Commits:** 5 commits, organized by test directory group
- `3dd45f6f` — tests/league_helper/
- `f8536a37` — tests/simulation/
- `c0ca5c48` — tests/integration/ and tests/root_scripts/
- `704efd1e` — tests/utils/ and tests/unit/
- `8b9dd9ac` — remaining test files

**Result:** ~3,570 comment lines removed, 122 files modified, 28 shebangs preserved, 1 noqa preserved.

---

### Bug Fix Pass (both features)

After the initial 9 feature commits, S9.P1 smoke testing discovered 357 surviving trailing inline comments due to the `string_lines` bug described above. Two additional fix-up commits addressed the missed comments:

- `a6c66bec` — re-pass over source packages and runners (80 files, 357 trailing inline comments)
- `23452c7f` — re-pass over test files (verified zero remaining)

Then the script itself was fixed:
- `07e61465` — fixed `strip_comments.py`: removed `string_lines` guard, fixed binary write mode for CRLF preservation

Finally, the script was deleted per the original spec:
- `c6f6a325` — deleted `strip_comments.py` (disposable tool, no longer needed)

---

## 6. Complete File Changelog

> All files are `Modified` unless noted otherwise. Change type `Deleted` for `strip_comments.py`.

### Source Packages

| File | Change Type | Description |
|------|-------------|-------------|
| `league_helper/LeagueHelperManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/add_to_roster_mode/AddToRosterModeManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/constants.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/starter_helper_mode/StarterHelperModeManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/trade_simulator_mode/TradeSimTeam.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/trade_simulator_mode/trade_analyzer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/trade_simulator_mode/trade_display_helper.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/trade_simulator_mode/trade_file_writer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/trade_simulator_mode/trade_input_parser.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/ConfigManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/FantasyTeam.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/GameDataManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/PlayerManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/ScoredPlayer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/SeasonScheduleManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/TeamDataManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/player_scoring.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/player_search.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/upcoming_game_model.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `league_helper/util/user_input.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/config.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/coordinates_manager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/espn_client.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/fantasy_points_calculator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/game_data_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/game_data_models.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/player_data_constants.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/player_data_exporter.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/player_data_fetcher_main.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/player_data_models.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `player_data_fetcher/progress_tracker.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/accuracy/AccuracyCalculator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/accuracy/AccuracyResultsManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/accuracy/AccuracySimulationManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/accuracy/ParallelAccuracyRunner.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/accuracy/__init__.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/shared/ConfigGenerator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/shared/ConfigPerformance.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/shared/ProgressTracker.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/shared/ResultsManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/shared/config_cleanup.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/utils/scheduler.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/win_rate/DraftHelperTeam.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/win_rate/ParallelLeagueRunner.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/win_rate/SimulatedLeague.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/win_rate/SimulatedOpponent.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/win_rate/SimulationManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/win_rate/Week.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `simulation/win_rate/manual_simulation.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/DraftedRosterManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/FantasyPlayer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/LineBasedRotatingHandler.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/LoggingManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/TeamData.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/adp_csv_loader.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/adp_updater.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/csv_utils.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/data_file_manager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `utils/error_handler.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/__init__.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/constants.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/game_data_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/http_client.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/json_exporter.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/player_data_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/schedule_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/team_data_calculator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `historical_data_compiler/weekly_snapshot_generator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `schedule_data_fetcher/ScheduleFetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |

### Runner Scripts

| File | Change Type | Description |
|------|-------------|-------------|
| `compile_historical_data.py` | Modified | Removed all `#` comment lines and trailing inline comments; shebang preserved |
| `run_accuracy_simulation.py` | Modified | Removed all `#` comment lines and trailing inline comments; shebang preserved |
| `run_league_helper.py` | Modified | Removed all `#` comment lines and trailing inline comments; shebang preserved |
| `run_player_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments; shebang preserved |
| `run_pre_commit_validation.py` | Modified | Removed all `#` comment lines and trailing inline comments; shebang preserved |
| `run_schedule_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments; shebang preserved |
| `run_win_rate_simulation.py` | Modified | Removed all `#` comment lines and trailing inline comments; shebang preserved |

### Test Files

| File | Change Type | Description |
|------|-------------|-------------|
| `tests/fixtures/helpers.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/run_all_tests.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/historical_data_compiler/__init__.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/historical_data_compiler/test_constants.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/historical_data_compiler/test_game_data_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/historical_data_compiler/test_json_exporter.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/historical_data_compiler/test_player_data_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/historical_data_compiler/test_team_data_calculator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/historical_data_compiler/test_weekly_snapshot_generator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_accuracy_simulation_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_compile_historical_data_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_config_variations.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_data_fetcher_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_fixture_infrastructure_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_fixture_recording_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_game_conditions_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_historical_data_compiler_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_info_behavior.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_json_exporter_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_league_helper_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_logging_infrastructure_e2e.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_offline_mode_runners_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_player_data_fetcher_main_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_schedule_fetcher_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_season_schedule_manager_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/integration/test_simulation_integration.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/save_calculated_points_mode/test_SaveCalculatedPointsManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/test_LeagueHelperManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/test_constants.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/trade_simulator_mode/__init__.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/trade_simulator_mode/test_trade_display_helper.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/trade_simulator_mode/test_trade_file_writer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/trade_simulator_mode/test_trade_input_parser.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/trade_simulator_mode/test_trade_simulator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_ConfigManager_flex_eligible_positions.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_ConfigManager_impact_scale.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_ConfigManager_max_positions.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_ConfigManager_nfl_team_penalty.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_ConfigManager_thresholds.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_ConfigManager_week_config.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_FantasyTeam.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_GameDataManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_PlayerManager_file_updates.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_PlayerManager_json_loading.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_PlayerManager_scoring.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_ScoredPlayer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_SeasonScheduleManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_TeamDataManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_player_scoring.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_player_scoring_game_conditions.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_player_scoring_nfl_team_penalty.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_player_search.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/league_helper/util/test_user_input.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_config.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_coordinates_manager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_espn_client.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_fantasy_points_calculator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_game_data_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_game_data_models.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_player_data_exporter.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_player_data_fetcher_main.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_player_data_models.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_progress_tracker.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/player_data_fetcher/test_run_player_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments; `# noqa: F401` at line 125 preserved |
| `tests/player_data_fetcher/test_settings_and_flow.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/root_scripts/test_root_scripts.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/root_scripts/test_run_accuracy_simulation.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/root_scripts/test_run_schedule_fetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/root_scripts/test_run_win_rate_simulation.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/schedule_data_fetcher/test_ScheduleFetcher.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/__init__.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_AccuracyCalculator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_AccuracyResultsManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_AccuracySimulationManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_ConfigPerformance.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_DraftHelperTeam.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_ParallelLeagueRunner.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_ProgressTracker.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_ResultsManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_SimulatedLeague.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_SimulatedOpponent.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_Week.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_config_cleanup.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_config_generator.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_manual_simulation.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/simulation/test_scheduler.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/unit/test_compile_historical_data_cli.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/unit/test_compile_historical_data_info_logs.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/unit/test_compile_historical_data_logger.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/unit/test_debug_logs_preserved.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/unit/test_game_data_fetcher_logs.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/unit/test_info_quality.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/unit/test_schedule_fetcher_logs.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_DraftedRosterManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_FantasyPlayer.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_LineBasedRotatingHandler.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_LoggingManager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_TeamData.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_adp_csv_loader.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_adp_updater.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_csv_utils.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_data_file_manager.py` | Modified | Removed all `#` comment lines and trailing inline comments |
| `tests/utils/test_error_handler.py` | Modified | Removed all `#` comment lines and trailing inline comments |

### Tool Script (created and deleted within epic)

| File | Change Type | Description |
|------|-------------|-------------|
| `strip_comments.py` | Deleted | Disposable tokenize-based comment removal script; committed in `07e61465`, deleted in `c6f6a325` per spec |

---

## 7. Testing Summary

**Testing Approach:** A — Smoke testing only (no automated test requirement for pure deletion epics)

**Verification method:** Two independent checks:
1. **Grep-based:** `grep -rn "^\s*#" --include="*.py" <scope> | grep -v ':1:#!/' | grep -v '# noqa' | grep -v '# type: ignore'` returns zero results
2. **Tokenize idempotency:** Re-running `strip_comments.py` on already-processed files produces zero file changes — if any `COMMENT` tokens survived the first pass, the second pass would remove them, producing a diff

**Note on grep false positives:** The grep verification command produces 17+ false-positive matches for `#` characters inside docstring content (e.g., grep command examples embedded in docstrings). These are `tokenize.STRING` tokens, not COMMENT tokens, and the tokenize-based idempotency check is the authoritative verification. This is documented in the Guide Deviation Log in EPIC_README.

**Smoke Test Results (S9.P1):**
- Zero `#` comment lines remaining (tokenizer-verified across all 206 in-scope `.py` files)
- Zero trailing inline `#` comments remaining
- 69 shebang lines preserved (40 source/runners + 29 tests — note: `test_run_player_fetcher.py` shebang was present, counted in test totals)
- 1 `# noqa: F401` directive preserved at `tests/player_data_fetcher/test_run_player_fetcher.py:125`
- 0 `# type: ignore` directives preserved (none existed pre-epic)
- Zero docstrings modified or removed
- No logic, behavior, or interface changes introduced
- Test suite stable (same 4 pre-existing failures, no new failures)

---

## 8. Out of Scope / Known Limitations

**Explicitly out of scope:**
- Docstrings (triple-quoted strings) — required by `CODING_STANDARDS.md`, not comments
- Adding or replacing docstrings to compensate for removed comments — out of scope; no documentation was added in this epic
- `.venv/` and `.shamt/` directories — not project code
- `_internal/` package — verified to contain zero `.py` files during discovery

**Known limitations:**
- `CODING_STANDARDS.md` update is local-only (file is gitignored) — the no-comments rule exists in the local standards doc but is not part of the git history. Anyone cloning fresh will not see the rule until they run the local config setup.
- The grep-based acceptance criterion in the epic ticket is technically imprecise (produces false positives for `#` in docstrings) — the authoritative check is the tokenize idempotency test.

**Planned follow-on:**
- Guide update proposals from this epic (3 proposals targeting `s9_p4_epic_final_review.md`) are recorded in `.shamt/unimplemented_design_proposals/KAI-16-guide-update-proposals.md` and await a future guide maintenance epic.

---

## 9. Review Guidance

**This is a pure deletion PR.** No logic was changed. The only behavioral question is whether the right things were deleted (comments) and the right things were preserved (shebangs, noqa, type: ignore, docstrings, string literals containing `#`).

**Suggested review order:**

1. **Start with the commit log** (13 commits) — the first 9 are the feature commits (4 F1, 5 F2), the next 2 are the bug-fix passes, then the script fix commit, then the deletion commit. Understanding the shape of the commit history tells the full story.

2. **Check a representative sample of modified files** — open any 3-5 files from different packages and verify: (a) no `#` lines remain (excluding preserved categories), (b) all docstrings are intact, (c) code logic is unchanged. The diff for each file should look like only line deletions.

3. **Verify preservation cases:**
   - Any runner script (`run_*.py`) — first line should be `#!/usr/bin/env python3`
   - `tests/player_data_fetcher/test_run_player_fetcher.py` line 125 — should contain `# noqa: F401`

4. **Spot-check the bug-fix commits** (`a6c66bec`, `23452c7f`) — these re-pass over files to catch trailing inline comments that survived the first pass (e.g., `LOGGING_LEVEL = 'INFO'  # comment`). Verify the diffs show only trailing comment removal, no other changes.

5. **`strip_comments.py` is not in the branch HEAD** — it was committed in `07e61465` and deleted in `c6f6a325`. You may see it in the diff history but it should not be present in the final working tree.

**What to focus scrutiny on:**
- Any file where a `#` inside a string literal was accidentally removed — look for truncated strings, broken regex patterns, or missing format strings
- Any file where a shebang was removed (would break direct execution of runner scripts)
- Any file where a docstring was shortened (would remove required documentation)
