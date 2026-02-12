# Epic Tracker

**Purpose:** Centralized log of all epics with KAI numbers, descriptions, and commit history.

**Branch Naming Convention:** `{work_type}/KAI-{number}`
- `epic` - Work with multiple features
- `feat` - Work with single feature
- `fix` - Bug fix work

**Commit Message Convention:** `{commit_type}/KAI-{number}: {message}`
- `feat` - Feature commit
- `fix` - Bug fix commit

---

## Active Epics

| KAI # | Epic Name | Type | Branch | Status | Date Started |
|-------|-----------|------|--------|--------|--------------|
| (none) | - | - | - | - | - |

---

## Completed Epics

### Next Available Number: KAI-9

| KAI # | Epic Name | Type | Branch | Date Completed | Location |
|-------|-----------|------|--------|----------------|----------|
| 8 | logging_refactoring | epic | epic/KAI-8 | 2026-02-12 | feature-updates/done/KAI-8-logging_refactoring/ |
| 7 | improve_configurability_of_scripts | epic | epic/KAI-7 | 2026-02-01 | feature-updates/done/KAI-7-improve_configurability_of_scripts/ |
| 6 | nfl_team_penalty | epic | epic/KAI-6 | 2026-01-15 | feature-updates/done/KAI-6-nfl_team_penalty/ |
| 5 | add_k_dst_ranking_metrics_support | epic | epic/KAI-5 | 2026-01-09 | feature-updates/done/KAI-5-add_k_dst_ranking_metrics_support/ |
| 3 | integrate_new_player_data_into_simulation | epic | epic/KAI-3 | 2026-01-04 | feature-updates/done/integrate_new_player_data_into_simulation/ |
| 2 | fix_2025_adp | epic | epic/KAI-2 | 2026-01-01 | feature-updates/done/fix_2025_adp/ |
| 1 | bug_fix-draft_mode | fix | fix/KAI-1 | 2025-12-31 | feature-updates/done/bug_fix-draft_mode/ |

---

## Epic Details

<!-- Each epic gets a detailed section below once completed -->

---

### KAI-8: logging_refactoring

**Type:** epic
**Branch:** epic/KAI-8
**Date Started:** 2026-02-06
**Date Completed:** 2026-02-12
**Location:** feature-updates/done/KAI-8-logging_refactoring/

**Description:**
Improved logging infrastructure across all major scripts with centralized log management, automated rotation, quality improvements to Debug/Info logs, and CLI toggle for file logging. The epic introduced a centralized LoggingHelper utility that manages log files across all 4 root scripts (run_league_helper.py, run_simulation.py, run_player_fetcher.py, run_scores_fetcher.py) with automatic rotation by both date and size (50MB max, 30-day retention). Each script gained a --no-log-file CLI flag to disable file logging while preserving console output, addressing a critical simulation performance bottleneck where sequential league runs generated 50MB+ log files in <1 minute. The epic systematically audited and improved 939 logger calls across 60 files, upgrading console clarity (more Info-level contextual messages) and file diagnostic detail (more Debug-level technical data). Group-based S2 parallelization enabled completion of 7 features in 6 days with zero bugs during epic testing.

**Features Implemented:**
1. feature_01_core_logging_infrastructure - Created LoggingHelper utility with file rotation (date + size), log directory management, and automated cleanup
2. feature_02_league_helper_logging - Integrated LoggingHelper into run_league_helper.py, audited 4 module logger calls, added --no-log-file flag
3. feature_03_player_data_fetcher_logging - Integrated LoggingHelper into run_player_fetcher.py, preserved existing error.log file, added --no-log-file flag
4. feature_04_accuracy_sim_logging - Integrated LoggingHelper into accuracy simulation with --no-log-file flag, audited 214 logger calls across 4 files
5. feature_05_win_rate_sim_logging - Integrated LoggingHelper into win rate simulation with --no-log-file flag, audited 277 logger calls across 5 files
6. feature_06_historical_data_compiler_logging - Integrated LoggingHelper into compile_historical_data.py, audited 120 logger calls across 2 files
7. feature_07_schedule_fetcher_logging - Integrated LoggingHelper into schedule fetcher, audited 73 logger calls across 2 files

**Key Changes:**
- utils/logging_helper.py: Created 180-line LoggingHelper utility with RotatingFileHandler (50MB max, 30-day retention), automated log directory setup, graceful failure handling
- run_league_helper.py: Integrated LoggingHelper, added --no-log-file CLI flag, updated 10 logger calls (3 Info, 7 Debug)
- run_simulation.py: Integrated LoggingHelper into both accuracy and win rate simulations with --no-log-file flag
- run_player_fetcher.py: Integrated LoggingHelper while preserving existing error.log behavior
- compile_historical_data.py: Integrated LoggingHelper with performance-critical --no-log-file support
- historical_data_compiler/game_data_fetcher.py: Audited 81 logger calls (19 Info, 62 Debug)
- historical_data_compiler/schedule_fetcher.py: Audited 73 logger calls (22 Info, 51 Debug)
- simulation/accuracy/: Audited 214 logger calls across AccuracySimulationManager, AccuracyCalculator, AccuracyResultsManager
- simulation/win_rate/: Audited 277 logger calls across SimulationManager, ParallelLeagueRunner, SimulatedLeague, DraftHelperTeam
- tests/: Updated 3 test files for new run_league_helper behavior, all tests passing (2661/2661)
- feature-updates/guides_v2/: Applied 3 S10.P1 guide improvements + comprehensive S5 v1→v2 terminology migration (17 files)

**Commit History:**
- `08f3c11` - `docs/KAI-8: Update EPIC_README with completion summary`
- `35cb011` - `chore/KAI-8: Add S5 terminology migration proposal to epic folder`
- `3767d21` - `chore/KAI-8: Move completed epic to done/ folder`
- `265e2fa` - `docs/guides: Migrate S5 v1→v2 terminology across reference files`
- `4198be8` - `feat/KAI-8: Complete logging_refactoring epic`
- `014cdd6` - `docs/KAI-8: Apply S10.P1 guide improvements from lessons learned`
- `21401cf` - `feat/KAI-8: Complete S9.P2 Epic QC Validation Loop`
- `1b29b0c` - `feat/KAI-8: Complete S8.P2 - All 7 features reviewed`
- Plus 12 additional feature implementation commits (20 total)

**Testing Results:**
- Unit tests: 2,661/2,661 passing (100%)
- Epic smoke testing: Passed (4 parts, zero issues)
- Epic QC Validation Loop: Passed (3 consecutive clean rounds, zero issues)
- User testing: Approved (zero bugs found in S9.P3)
- S10.P1 Guide updates: 3 proposals applied (P0, P2, P3)
- Guide audits: 2 comprehensive audits (initial + fresh validation post-migration)

**Lessons Learned:**
See feature-updates/done/KAI-8-logging_refactoring/epic_lessons_learned.md - Key success factors: Group-based S2 parallelization enabled 71% time reduction (14h sequential → 4h group-based), systematic logger call auditing (939 calls across 60 files) found zero implementation bugs, CLI flag approach (--no-log-file) solved performance without architectural changes, S5 v2 Validation Loop (11 dimensions, 3 consecutive clean rounds) prevented all bugs before implementation. Critical process lessons: S2 parallelization requires dependency analysis (Group 1: foundation, Group 2: dependents), reactive coordination model (not proactive monitoring), handoff packages should reference file paths (not paste 300+ lines). Generated comprehensive guide improvements including group-based parallelization workflow, S5 v1→v2 terminology migration across 17 reference files, and 2 new reference guides (s2_parallelization_decision_tree.md, s2_primary_agent_group_wave_guide.md planned).

**Related Documentation:**
- Epic README: feature-updates/done/KAI-8-logging_refactoring/EPIC_README.md
- Epic Test Plan: feature-updates/done/KAI-8-logging_refactoring/epic_smoke_test_plan.md
- Epic Lessons Learned: feature-updates/done/KAI-8-logging_refactoring/epic_lessons_learned.md
- Guide Update Proposals:
  - feature-updates/done/KAI-8-logging_refactoring/GUIDE_UPDATE_PROPOSAL.md (3 proposals)
  - feature-updates/done/KAI-8-logging_refactoring/GUIDE_UPDATE_PROPOSAL_S5_TERMINOLOGY.md (17-file migration)
- Research Analysis:
  - feature-updates/done/KAI-8-logging_refactoring/research/GROUP_BASED_S2_PARALLELIZATION_INTENDED_FLOW.md
  - feature-updates/done/KAI-8-logging_refactoring/research/PARALLEL_S2_STRUCTURE_INCONSISTENCY_ANALYSIS.md

---

### KAI-6: nfl_team_penalty

**Type:** epic
**Branch:** epic/KAI-6
**Date Started:** 2026-01-12
**Date Completed:** 2026-01-15
**Location:** feature-updates/done/KAI-6-nfl_team_penalty/

**Description:**
Added NFL team penalty system to Add to Roster mode scoring, allowing users to specify NFL teams they want to avoid drafting. Users configure a team penalty list (e.g., ["LV", "NYJ"]) and penalty weight (0.0-1.0 multiplier) in league_config.json, and the system reduces player scores from those teams by multiplying their final score by the weight. This feature enables user-specific draft preferences (e.g., avoiding rivals) without affecting simulation objectivity, since simulations use default values (empty list, 1.0 weight). The penalty applies as Step 14 in the existing 14-step scoring algorithm, only in Add to Roster mode (parameter-based mode isolation). The implementation maintains full backward compatibility - all existing code continues working unchanged with parameter defaults ensuring no behavior changes.

**Features Implemented:**
1. feature_01_config_infrastructure - Added NFL_TEAM_PENALTY (list) and NFL_TEAM_PENALTY_WEIGHT (float) config settings to ConfigManager with validation logic, updated 10 config files (league_config.json + 9 simulation configs)
2. feature_02_score_penalty_application - Implemented Step 14 in 14-step scoring algorithm, added _apply_nfl_team_penalty() helper method, enabled penalty only in Add to Roster mode via nfl_team_penalty parameter

**Key Changes:**
- league_helper/util/ConfigManager.py: Added NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT properties with validation (team abbreviations, weight range 0.0-1.0)
- league_helper/util/player_scoring.py: Added Step 14 NFL team penalty logic, _apply_nfl_team_penalty() helper method, nfl_team_penalty parameter (default=False)
- league_helper/util/PlayerManager.py: Parameter pass-through from score_player() to PlayerScoringCalculator
- league_helper/add_to_roster_mode/AddToRosterModeManager.py: Enabled penalty (nfl_team_penalty=True) only in this mode
- data/league_config.json: User-specific penalty teams configured
- data/*.json: 9 simulation configs updated with defaults (empty list, 1.0 weight)
- tests/league_helper/util/test_ConfigManager_nfl_team_penalty.py: Created 12 comprehensive tests for config validation
- tests/league_helper/util/test_player_scoring_nfl_team_penalty.py: Created 10 comprehensive tests for penalty logic
- feature-updates/guides_v2/: Applied 5 guide improvements based on lessons learned (autonomous resolution warnings, investigation checklists, status progression examples, anti-patterns)

**Commit History:**
- `6f38d11` - `feat/KAI-6: Add NFL team penalty to Add to Roster mode scoring` (squashed)

**Testing Results:**
- Unit tests: 2,506/2,506 passing (100%)
- New tests added: 22 (all passing)
- Epic smoke testing: Passed (4 parts, zero issues)
- Epic QC rounds: Passed (3 rounds, zero issues)
- User testing: Approved (user skipped manual testing, approved automated results)
- S10.P1 Guide updates: 5 proposals applied

**Lessons Learned:**
See feature-updates/done/KAI-6-nfl_team_penalty/epic_lessons_learned.md - Key success factors: Zero autonomous resolution pattern (agents create questions, users provide answers), systematic investigation using 5-category checklist prevents narrow scope, explicit user approval required for marking questions RESOLVED, status progression must be OPEN → PENDING → RESOLVED (never skip), proper investigation ≠ resolution. Generated 5 concrete guide updates: autonomous resolution warning in S2.P3, checklist template role definitions, investigation scope checklist in S2 guides, status progression examples in S2.P2, anti-pattern examples in CLAUDE.md. This epic validated the importance of maintaining strict boundaries between agent research capabilities and user decision authority.

**Related Documentation:**
- Epic README: feature-updates/done/KAI-6-nfl_team_penalty/EPIC_README.md
- Epic Test Plan: feature-updates/done/KAI-6-nfl_team_penalty/epic_smoke_test_plan.md
- Epic Lessons Learned: feature-updates/done/KAI-6-nfl_team_penalty/epic_lessons_learned.md
- Feature 01 Spec: feature-updates/done/KAI-6-nfl_team_penalty/feature_01_config_infrastructure/spec.md
- Feature 02 Spec: feature-updates/done/KAI-6-nfl_team_penalty/feature_02_score_penalty_application/spec.md
- Guide Update Proposal: feature-updates/done/KAI-6-nfl_team_penalty/GUIDE_UPDATE_PROPOSAL.md

---

### KAI-1: bug_fix-draft_mode

**Type:** fix
**Branch:** fix/KAI-1
**Date Started:** 2025-12-31
**Date Completed:** 2025-12-31
**Location:** feature-updates/done/bug_fix-draft_mode/

**Description:**
Fixed critical bug in Add to Roster mode where RB/WR players could only match FLEX-ideal draft rounds, not their native position rounds (RB-ideal, WR-ideal). This caused 8 out of 15 roster slots to incorrectly display as [EMPTY SLOT] even with a full roster. The fix allows FLEX-eligible positions (RB/WR) to match both their native position rounds AND FLEX rounds, while maintaining exact-match-only behavior for non-FLEX positions (QB/TE/K/DST).

**Features Implemented:**
1. feature_01_fix_player_round_assignment - Created `_position_matches_ideal()` helper method to correctly handle FLEX position matching logic

**Key Changes:**
- league_helper/add_to_roster_mode/AddToRosterModeManager.py: Added `_position_matches_ideal()` helper method (30 lines) to replace buggy inline logic
- league_helper/add_to_roster_mode/AddToRosterModeManager.py: Updated `_match_players_to_rounds()` to use new helper method instead of `get_position_with_flex()`
- tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py: Added 7 comprehensive tests validating bug fix and preventing regressions

**Commit History:**
- `cf20b90` - `feat/KAI-1: Initialize epic tracking for bug_fix-draft_mode`
- `13b4fe4` - `fix/KAI-1: Fix Add to Roster mode player-to-round assignment logic`

**Testing Results:**
- Unit tests: 2,423/2,423 passing (100%)
- Epic smoke testing: Passed (3/3 applicable parts)
- Epic QC rounds: Passed (3/3 rounds, 0 issues)
- User testing: Passed (zero bugs found)

**Lessons Learned:**
See feature-updates/done/bug_fix-draft_mode/epic_lessons_learned.md - Key success factors: rigorous Stage 5a planning (24 iterations with Algorithm Traceability Matrix), comprehensive testing (7 unit tests + integration test with actual user data), data values verification (real player names, not placeholders), progressive quality validation (6 QC rounds total), and zero tech debt tolerance.

**Related Documentation:**
- Epic README: feature-updates/done/bug_fix-draft_mode/EPIC_README.md
- Epic Test Plan: feature-updates/done/bug_fix-draft_mode/epic_smoke_test_plan.md
- Epic Lessons Learned: feature-updates/done/bug_fix-draft_mode/epic_lessons_learned.md

---

### KAI-2: fix_2025_adp

**Type:** epic
**Branch:** epic/KAI-2
**Date Started:** 2025-12-31
**Date Completed:** 2026-01-01
**Location:** feature-updates/done/fix_2025_adp/

**Description:**
Integrated 2025 ADP (Average Draft Position) data across all simulation weeks to replace placeholder values with real market data. ESPN API returns placeholder ADP value of 170.0 for all players in 2025 data, which degrades simulation accuracy since ADP multiplier is a key scoring component. This epic implemented a complete ADP data integration system that loads FantasyPros consensus ADP rankings, matches players using fuzzy matching logic, and updates 108 simulation files (18 weeks × 6 positions) with real ADP data. A critical bug was discovered during Stage 7 testing where the epic targeted the wrong data folder entirely (data/player_data/ instead of simulation/sim_data/2025/weeks/), requiring a comprehensive bug fix that updated the multi-week iteration logic, implemented direct JSON array handling, and added DST-specific matching logic to handle name format differences between CSV ("Baltimore Ravens") and JSON ("Ravens D/ST").

**Features Implemented:**
1. feature_01_csv_data_loading - Load and validate ADP data from FantasyPros CSV file with position suffix stripping and data integrity validation
2. feature_02_player_matching_update - Match CSV players to existing player data using fuzzy matching and update ADP values in JSON files with comprehensive reporting

**Bug Fix:**
- bugfix_high_wrong_data_folder - Fixed epic to target simulation/sim_data/2025/weeks/ (108 files across 18 weeks) instead of data/player_data/ (6 files), implemented multi-week iteration with direct JSON array handling, and added DST team name extraction for accurate matching

**Key Changes:**
- utils/adp_csv_loader.py: Created ADP CSV loader (112 lines) with validation, position suffix stripping, and data integrity checks
- utils/adp_updater.py: Created ADP updater (428 lines) with fuzzy matching (confidence threshold 0.75), DST-specific team name extraction, atomic write pattern, and comprehensive match reporting
- utils/adp_updater.py: Added DST special handling with extract_dst_team_name() to handle format differences ("Baltimore Ravens" → "ravens", "Ravens D/ST" → "ravens")
- simulation/sim_data/2025/weeks/week_*/: Updated 108 JSON files (18 weeks × 6 positions) with real 2025 ADP data using atomic writes
- tests/utils/test_adp_csv_loader.py: Added 13 unit tests for CSV loading validation
- tests/utils/test_adp_updater.py: Added 27 unit tests including 7 DST-specific tests
- update_adp_values.py: Created standalone script for easy ADP updates across all weeks
- feature-updates/guides_v2/: Updated 5 workflow guides with 6 enhancements for data validation, category-specific testing, and per-category verification

**Commit History:**
- `9be4461` - `feat/KAI-2: Initialize epic tracking for fix_2025_adp`
- `e66fb58` - `feat/KAI-2: Integrate 2025 ADP data across simulation weeks`

**Testing Results:**
- Unit tests: 2,463/2,463 passing (100%)
- Epic smoke testing: 12/12 passed
- Epic QC rounds: Passed (3/3 rounds, 0 issues)
- User testing: Passed (zero bugs found)

**Lessons Learned:**
See feature-updates/done/fix_2025_adp/epic_lessons_learned.md and bugfix_high_wrong_data_folder/lessons_learned.md - Key success factors: QC Round 3 proved critical by catching DST matching bug that Rounds 1-2 missed (only 90/108 files updated instead of 108), emphasizing importance of per-category data verification instead of just checking totals. Six guide enhancements added to prevent similar issues: data format validation (Iteration 6), category-specific test coverage (Iteration 15), position-specific test verification (Iteration 23a Part 2), per-category data validation (Smoke Testing Part 3), per-category file verification (QC Round 1 Section 3), and list item verification (QC Round 3 Section 1).

**Related Documentation:**
- Epic README: feature-updates/done/fix_2025_adp/EPIC_README.md
- Epic Test Plan: feature-updates/done/fix_2025_adp/epic_smoke_test_plan.md
- Epic Lessons Learned: feature-updates/done/fix_2025_adp/epic_lessons_learned.md
- Bug Fix Lessons: feature-updates/done/fix_2025_adp/bugfix_high_wrong_data_folder/lessons_learned.md

---

### KAI-3: integrate_new_player_data_into_simulation

**Type:** epic
**Branch:** epic/KAI-3
**Date Started:** 2026-01-02
**Date Completed:** 2026-01-04
**Location:** feature-updates/done/integrate_new_player_data_into_simulation/

**Description:**
Verified and cleaned up simulation modules after JSON data migration, ensuring both Win Rate Sim and Accuracy Sim work correctly with new JSON player data format. The epic was triggered by the recent JSON migration (2025-12-30) which broke both simulations. Through comprehensive verification testing, discovered and fixed 8 critical bugs including PlayerScoringCalculator max_projection sync issues, draft position diversity enforcement bugs, and deprecated API usage. Deleted 2.2M+ lines of deprecated CSV data and old config folders, improved simulation logging (70% reduction in spam), and validated both simulations work correctly with JSON through parameter optimization runs. Feature 03 (cross-simulation testing) was absorbed into epic-level testing (Stage 6a) since its verification scope was completed through Features 01, 02, and epic smoke testing.

**Features Implemented:**
1. feature_01_win_rate_sim_verification - Removed CSV loading, verified Win Rate Sim JSON data flow, validated simulation completeness
2. feature_02_accuracy_sim_verification - Verified Accuracy Sim JSON loading via PlayerManager, aligned edge cases with Win Rate Sim
3. feature_03_cross_simulation_testing - Epic-level validation absorbed into Stage 6a (end-to-end testing, documentation updates, final verification)

**Bug Fixes During Epic:**
- Issue #1: Accuracy Sim CURRENT_NFL_WEEK config shallow copy issue
- Issue #2: Win Rate Sim hardcoded week_01 loading
- Issue #3: Using hybrid projection instead of actual points
- Issue #4: Unicode encoding on Windows (replaced checkmark with [OK])
- Issue #5: Deprecated .drafted API usage (changed to .drafted_by)
- Issue #6: DraftHelperTeam using deprecated API
- Issue #7: PlayerScoringCalculator.max_projection sync (CRITICAL) - max_projection initialized to 0.0 before players loaded, causing identical scoring for all players
- Issue #8: Draft not respecting MAX_POSITIONS config (CRITICAL) - draft_order_primary/secondary selection ignored max_positions enforcement

**Key Changes:**
- league_helper/util/PlayerManager.py: Added defensive check for scoring_calculator (Issue #7 fix), defensive hasattr check for test compatibility
- simulation/win_rate/SimulatedLeague.py: Removed CSV loading, verified JSON works
- simulation/win_rate/DraftHelperTeam.py: Fixed draft position diversity (Issue #8 - respects MAX_POSITIONS during selection)
- simulation/accuracy/AccuracySimulationManager.py: Verified JSON loading via PlayerManager
- simulation/win_rate/SimulationManager.py: Improved logging (70% reduction, better progress tracking)
- simulation/win_rate/ParallelLeagueRunner.py: Changed verbose logs to debug level
- tests/: Updated 16 tests to match new API behavior (100% pass rate)
- Deleted 2.2M+ lines: 2023/2025 CSV files, old config folders (accuracy_optimal, old strategies)

**Commit History:**
- `3d4fba5` - `feat/KAI-3: Add guide improvements from epic workflow`
- `7858f24` - `feat/KAI-3: Complete integrate_new_player_data_into_simulation epic`
- `4c6b2df` - `feat/KAI-3: Update epic smoke test plan after feature_02_accuracy_sim_verification`
- `6ad8d0a` - `feat/KAI-3: Update Feature 03 spec based on Feature 02 implementation`
- `9d48805` - `fix/KAI-3: Fix JSON array handling in PlayerManager and TeamDataManager`
- `ee3a978` - `feat/KAI-3: Update epic smoke test plan after feature_01_win_rate_sim_verification`

**Testing Results:**
- Unit tests: 2,481/2,481 passing (100%)
- Epic smoke testing: Passed (5 test scenarios)
- User testing: Passed (zero bugs found)
- Both simulations validated with JSON data:
  - Win Rate Sim: Generated intermediate_01, optimized DRAFT_NORMALIZATION_MAX_SCALE to 140
  - Accuracy Sim: Generated 6 intermediate folders, MAE calculated for all horizons (4.51-4.61)

**Lessons Learned:**
See feature-updates/done/integrate_new_player_data_into_simulation/epic_lessons_learned.md - Key success factors: All features concluded guides worked correctly when followed (zero guide updates needed), verification features require minimal code changes with comprehensive test plans, QC rounds effectively caught spec deviations and bugs, and debugging protocol successfully resolved all 8 issues systematically. The epic validated the v2 workflow operates correctly without requiring modifications.

**Related Documentation:**
- Epic README: feature-updates/done/integrate_new_player_data_into_simulation/EPIC_README.md
- Epic Test Plan: feature-updates/done/integrate_new_player_data_into_simulation/epic_smoke_test_plan.md
- Epic Lessons Learned: feature-updates/done/integrate_new_player_data_into_simulation/epic_lessons_learned.md

---

### KAI-5: add_k_dst_ranking_metrics_support

**Type:** epic
**Branch:** epic/KAI-5
**Date Started:** 2026-01-08
**Date Completed:** 2026-01-09
**Location:** feature-updates/done/KAI-5-add_k_dst_ranking_metrics_support/

**Description:**
Added Kicker (K) and Defense/Special Teams (DST) positions to ranking-based accuracy metrics (pairwise accuracy, top-N accuracy, Spearman correlation) in the accuracy simulation. Previously, K and DST were only evaluated using MAE (fallback metric), while QB/RB/WR/TE used pairwise accuracy (primary metric). This epic extended ranking metrics to all 6 positions, enabling consistent evaluation across all position groups. During user testing, discovered and resolved 3 critical bugs related to backward compatibility with old intermediate files, which led to significant guide improvements based on systematic root cause analysis.

**Features Implemented:**
1. feature_01_add_k_dst_ranking_metrics_support - Added K and DST to position lists in AccuracyCalculator (lines 258, 544), enabling all ranking metrics for these positions

**Bug Fixes During Epic:**
- Issue #001: Incomplete Simulation Results - Resume logic loaded old intermediate files without ranking_metrics, polluting best_configs; comparison logic fell back to MAE allowing invalid comparisons; invalid 'ros' key caused warnings
- Issue #002: config_value Showing null - param_name not passed to add_result() causing parameter value extraction to fail
- Issue #003: Missing Position-Specific Metrics - by_position dict not serialized to JSON output files

**Key Changes:**
- simulation/accuracy/AccuracyCalculator.py: Added K and DST to position_data dict (line 258) and positions list (line 544)
- simulation/accuracy/AccuracyResultsManager.py: Fixed resume logic (don't populate best_configs with old data), removed MAE fallback from is_better_than() (reject invalid configs), added by_position serialization to ranking_metrics output
- simulation/accuracy/AccuracySimulationManager.py: Pass param_name and test_idx to add_result() for config_value extraction, removed invalid 'ros' key from horizon_map
- feature-updates/guides_v2/stages/stage_5/round1_todo_creation.md: Added Iteration 7a (Backward Compatibility Analysis)
- feature-updates/guides_v2/stages/stage_5/round2_todo_creation.md: Added resume/persistence testing requirements
- feature-updates/guides_v2/stages/stage_5/round3_part2a_gates_1_2.md: Added Part 5 (Design Decision Scrutiny) to Iteration 23a
- tests/: Updated 13 test files with ranking_metrics fixtures, added 7 new K/DST test cases (100% pass rate)

**Commit History:**
- `09c69ea` - `feat/KAI-5: Complete add_k_dst_ranking_metrics_support epic`

**Testing Results:**
- Unit tests: 2,486/2,486 passing (100%)
- Epic smoke testing: Passed (7 scenarios, 5 success criteria, zero issues)
- Epic QC rounds: Passed (3/3 rounds, zero issues)
- User testing: Passed (3 issues found and resolved)

**Lessons Learned:**
See feature-updates/done/KAI-5-add_k_dst_ranking_metrics_support/epic_lessons_learned.md - Key success factors: Position-agnostic architecture enabled minimal code changes (2 lines), thorough Stage 5a research (24 iterations) prevented implementation surprises, QC process caught zero bugs (production-ready on first attempt), pure data modifications are lowest risk changes. Critical process lesson: NEVER skip guide steps for "efficiency" - batching iterations leads to skipped verification and bugs. Debugging lessons: Backward compatibility must be explicit in research (new Iteration 7a), test real-world scenarios not just happy path, validate data before use and fail fast on invalid, version all serialized structures, question all "for backward compatibility" design decisions. Generated 5 concrete guide updates to prevent similar bugs in future epics.

**Related Documentation:**
- Epic README: feature-updates/done/KAI-5-add_k_dst_ranking_metrics_support/EPIC_README.md
- Epic Test Plan: feature-updates/done/KAI-5-add_k_dst_ranking_metrics_support/epic_smoke_test_plan.md
- Epic Lessons Learned: feature-updates/done/KAI-5-add_k_dst_ranking_metrics_support/epic_lessons_learned.md
- Debugging Analysis: feature-updates/done/KAI-5-add_k_dst_ranking_metrics_support/debugging/process_failure_analysis.md
- Guide Updates: feature-updates/done/KAI-5-add_k_dst_ranking_metrics_support/debugging/guide_update_recommendations.md

---

## Usage Instructions

### Starting a New Epic

1. **Assign KAI Number:**
   - Check "Next Available Number" above
   - Use that number for your epic
   - Increment "Next Available Number" immediately

2. **Determine Work Type:**
   - `epic` - Multiple features (most common)
   - `feat` - Single feature only
   - `fix` - Already classified as bug fix

3. **Create Branch:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b {work_type}/KAI-{number}
   ```
   Example: `git checkout -b epic/KAI-1`

4. **Update Active Epics Table:**
   - Add row with KAI number, epic name, type, branch, status "In Progress", date

5. **During Development:**
   - All commits use format: `{commit_type}/KAI-{number}: {message}`
   - commit_type is either `feat` or `fix` (not `epic`)
   - Example: `feat/KAI-1: Add week 18 data folder creation`
   - Example: `fix/KAI-1: Correct week range validation logic`

### Completing an Epic

1. **Move from Active to Completed:**
   - Remove row from Active Epics table
   - Add row to Completed Epics table with completion date and done/ location

2. **Create Epic Detail Section:**
   - Add section below with full details (see template below)

3. **Update Next Available Number:**
   - Increment to next number

4. **Merge to Main:**
   ```bash
   git checkout main
   git pull origin main
   git merge {work_type}/KAI-{number}
   git push origin main
   ```

5. **Delete Branch (Optional):**
   ```bash
   git branch -d {work_type}/KAI-{number}
   ```

---

## Epic Detail Template

```markdown
---

### KAI-{number}: {Epic Name}

**Type:** epic / feat / fix
**Branch:** {work_type}/KAI-{number}
**Date Started:** YYYY-MM-DD
**Date Completed:** YYYY-MM-DD
**Location:** feature-updates/done/{epic_folder_name}/

**Description:**
{1-2 paragraph description of what this epic accomplished}

**Features Implemented:**
1. {feature_01_name} - {brief description}
2. {feature_02_name} - {brief description}
3. {feature_03_name} - {brief description}

**Key Changes:**
- {file_path}: {what changed and why}
- {file_path}: {what changed and why}
- {file_path}: {what changed and why}

**Commit History:**
- `{commit_hash}` - `{commit_type}/KAI-{number}: {commit message}`
- `{commit_hash}` - `{commit_type}/KAI-{number}: {commit message}`
- `{commit_hash}` - `{commit_type}/KAI-{number}: {commit message}`

**Testing Results:**
- Unit tests: {X}/{Y} passing
- Integration tests: {status}
- Epic smoke testing: {status}

**Lessons Learned:**
{Link to epic_lessons_learned.md or key insights}

**Related Documentation:**
- Epic README: feature-updates/done/{epic_name}/EPIC_README.md
- Epic Test Plan: feature-updates/done/{epic_name}/epic_smoke_test_plan.md
```

---

## Historical Notes

**Initialization:** 2025-12-31
- Tracker created to support git branching workflow
- Starting fresh with KAI-1 for next epic
- All future epics will be tracked here

---

## Quick Reference

**Current Next Number:** KAI-1

**Active Epic Count:** 0

**Completed Epic Count:** 0

**Branch Naming Examples:**
- `epic/KAI-1` - Multi-feature epic
- `feat/KAI-2` - Single feature work
- `fix/KAI-3` - Bug fix work

**Commit Message Examples:**
- `feat/KAI-1: Add ADP integration to PlayerManager`
- `feat/KAI-1: Create matchup difficulty calculation`
- `fix/KAI-1: Correct bye week penalty calculation`
- `fix/KAI-2: Fix draft mode crash when no players available`

---

**Last Updated:** 2025-12-31
