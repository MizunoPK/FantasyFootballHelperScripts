# Discovery Phase: improve_configurability_of_scripts

**Epic:** KAI-7-improve_configurability_of_scripts
**Created:** 2026-01-28
**Last Updated:** 2026-01-29
**Status:** COMPLETE

---

## Epic Request Summary

User wants to make runner scripts configurable via command-line arguments, add debug mode support across all scripts, and create fast end-to-end test modes (≤3 minutes each) for integration testing. This includes making 7 runner scripts accept arguments, supporting debug logging, creating E2E test modes, building an integration test framework with per-script test runners, and creating a master test runner that validates all argument combinations.

**Original Request:** `improve_configurability_of_scripts_notes.txt`

---

## Discovery Questions

### Resolved Questions

| # | Question | Answer | Impact | Resolved |
|---|----------|--------|--------|----------|
| 1 | What specific arguments should each runner script accept beyond --debug and --e2e-test? | Script-specific args focusing on constants.py settings for configurability | Need to research each script's constants | 2026-01-28 |
| 2 | For league helper E2E mode, should it run ALL modes/submodes or allow selecting specific ones? | Support both: all 4 modes OR specific mode via --mode arg | Need mode selection argument design | 2026-01-28 |
| 3 | What makes an E2E run "reasonable" (3 min max)? What can be reduced/mocked? | Simulations: single run with 0-1 random configs. Fetchers: real APIs with data limiting args | Design data-limiting arguments | 2026-01-28 |
| 4 | Should debug mode be a separate log level or different behavior entirely? | Option C: Both logging AND behavioral changes | Debug mode changes behavior + enables DEBUG logs | 2026-01-28 |
| 5 | How should integration tests determine pass/fail? Exit code only or also check output? | Check exit code AND verify expected outcomes (specific logs, result counts) | Each test validates specific expected results | 2026-01-28 |

### Pending Questions

| # | Question | Context | Asked |
|---|----------|---------|-------|
| - | (None pending - proceeding to Iteration 2 research) | - | - |

---

## Research Findings

### Iteration 1 (2026-01-28 - Initial Research)

**Researched:** Current state of all 7 runner scripts, existing argument patterns, logging infrastructure

**Files Examined:**
- `run_league_helper.py` (lines 1-68): Currently no argparse, subprocess call with hardcoded DATA_FOLDER
- `run_player_fetcher.py` (lines 1-51): No argparse, just runs player_data_fetcher_main.py
- `run_schedule_fetcher.py` (lines 1-59): No argparse, async runner for ScheduleFetcher
- `run_win_rate_simulation.py` (lines 1-110): HAS argparse with mode, sims, baseline, workers, etc.
- `run_accuracy_simulation.py` (lines 1-80): HAS argparse with baseline, test-values, log-level, etc.
- `run_game_data_fetcher.py` (lines 1-80): HAS argparse with season, output, weeks
- `compile_historical_data.py` (lines 1-60): HAS argparse with year, weeks, validate, clean
- `utils/LoggingManager.py`: Exists with setup_logger supporting DEBUG/INFO/WARNING/ERROR/CRITICAL levels

**Key Findings:**
- **4 scripts have NO argparse:** league_helper, player_fetcher, schedule_fetcher (need to add)
- **3 scripts HAVE argparse:** simulations, game_data_fetcher, historical_compiler (need to enhance)
- **Logging infrastructure EXISTS:** LoggingManager supports all levels including DEBUG
- **Simulation scripts already have extensive args:** mode, sims, baseline, workers, output, data, test-values
- **Pattern inconsistency:** Some scripts use argparse, some don't
- **No E2E test mode exists anywhere:** Would need to be designed from scratch
- **League helper is subprocess-based:** Calls LeagueHelperManager.py with DATA_FOLDER arg

**Questions Identified:**
- Questions 1-5 above (pending user answers)

---

### Iteration 2 (2026-01-28 22:30 - Constants Research)

**Researched:** Configuration constants in each module that should become CLI arguments

**Files Examined:**
- `player-data-fetcher/config.py` (lines 1-90): CURRENT_NFL_WEEK, PRESERVE_LOCKED_VALUES, OUTPUT_DIRECTORY, CREATE_CSV/JSON/EXCEL/POSITION_JSON, ENABLE_HISTORICAL_DATA_SAVE, ENABLE_GAME_DATA_FETCH, LOGGING_LEVEL, PROGRESS_UPDATE_FREQUENCY
- `league_helper/constants.py` (lines 1-87): LOGGING_LEVEL, LOGGING_TO_FILE, RECOMMENDATION_COUNT, MIN_WAIVER_IMPROVEMENT, MIN_TRADE_IMPROVEMENT
- `league_helper/LeagueHelperManager.py` (lines 127): 5 modes identified: Add to Roster, Starter Helper, Trade Simulator, Modify Player Data, Save Calculated Points
- `historical_data_compiler/constants.py` (lines 1-157): REQUEST_TIMEOUT, RATE_LIMIT_DELAY, MIN_SUPPORTED_YEAR, REGULAR_SEASON_WEEKS
- `run_win_rate_simulation.py` (lines 33-46): LOGGING_LEVEL, DEFAULT_SIMS, DEFAULT_WORKERS, DEFAULT_TEST_VALUES (already has extensive argparse)
- `run_accuracy_simulation.py` (lines 53-68): DEFAULT_LOG_LEVEL, DEFAULT_TEST_VALUES, DEFAULT_MAX_WORKERS (already has extensive argparse)

**Key Findings:**
- **Player fetcher constants** (11 configurable): week, preserve-locked, output-dir, create-csv, create-json, create-excel, create-position-json, enable-historical-save, enable-game-data, log-level, progress-frequency
- **League helper constants** (4 configurable + modes): log-level, log-to-file, recommendation-count, min-waiver-improvement + mode selection (5 modes)
- **League helper has 5 modes** (epic said 4): Add to Roster, Starter Helper, Trade Simulator, Modify Player Data, Save Calculated Points
- **Historical compiler constants** (4 configurable): timeout, rate-limit-delay, min-year, regular-season-weeks
- **Simulations already well-configured**: Both have extensive args (sims, baseline, output, workers, data, test-values, log-level)
- **Schedule fetcher has no config file**: Would need to add arguments for season, output-path

**Questions Identified:**
- None (synthesis ready - user answers provided direction)

---

## Discovery Log

| Timestamp | Activity | Outcome |
|-----------|----------|---------|
| 2026-01-28 22:00 | Initialized Discovery | Epic size LARGE, time-box 3-4 hours |
| 2026-01-28 22:15 | Iteration 1 Research | Examined all 7 runners, found 4 without argparse, 3 with |
| 2026-01-28 22:25 | User answered Q1-Q5 | Script-specific args, mode selection, E2E specs, debug behavior, test validation |
| 2026-01-28 22:30 | Iteration 2 Research | Found 11 player-fetcher constants, 5 league helper modes, 4 historical compiler constants |
| 2026-01-28 22:45 | Discovery Loop Exit | No new questions, proceeding to synthesis |

---

## Solution Options

### Option 1: Minimal Argparse (--debug, --e2e-test only)

**Description:** Add only --debug and --e2e-test flags to each script, keep all other settings in config files.

**Pros:**
- Simple, fast implementation
- Minimal changes to existing code
- Easy to test and maintain

**Cons:**
- Doesn't address "any config or flag" requirement from epic
- Limited configurability for testing
- Doesn't leverage existing constants research

**Effort Estimate:** LOW

**Fit Assessment:** POOR (doesn't meet epic requirement for comprehensive configurability)

---

### Option 2: Comprehensive Argparse (Script-Specific Constants)

**Description:** For each script, expose frequently-modified constants as CLI arguments (e.g., --week, --output-dir, --create-json for player fetcher). Keep --debug and --e2e-test universal.

**Pros:**
- Meets epic requirement ("any config or flag")
- Leverages existing constants research
- Script-specific args match actual usage patterns
- Maintains backward compatibility (args override constants)

**Cons:**
- More implementation work per script
- Different args for each script (not uniform)
- More extensive testing needed

**Effort Estimate:** MEDIUM-HIGH

**Fit Assessment:** EXCELLENT (matches user Answer Q1: script-specific args from constants)

---

### Option 3: Hybrid (Universal + Script-Specific)

**Description:** Universal args for all scripts (--debug, --e2e-test, --log-level, --output) plus script-specific args for unique constants.

**Pros:**
- Consistent baseline across all scripts
- Script-specific customization where needed
- Good balance of uniformity and flexibility

**Cons:**
- Some arguments might not apply to all scripts (e.g., --output not meaningful for some)
- Complexity in determining what's universal vs script-specific

**Effort Estimate:** MEDIUM

**Fit Assessment:** GOOD (provides consistency + flexibility)

---

### Option Comparison Summary

| Option | Effort | Fit | Recommended |
|--------|--------|-----|-------------|
| Minimal Argparse | LOW | POOR | NO |
| Comprehensive Argparse | MEDIUM-HIGH | EXCELLENT | YES |
| Hybrid | MEDIUM | GOOD | NO (adds complexity without enough benefit) |

---

## Recommended Approach

**Recommendation:** Option 2 - Comprehensive Script-Specific Argparse

**Rationale:**
- User Answer Q1: "Script specific... research to determine what arguments should be added... focus on constants.py settings"
- User Answer Q2: League helper needs mode selection (--mode arg)
- User Answer Q3: E2E modes need specific configurations (simulations: single run, fetchers: data limiting)
- User Answer Q4: Debug mode = behavioral changes + logging (needs --debug flag)
- User Answer Q5: Integration tests validate specific outcomes (need configurable test scenarios)
- Research shows clear set of constants per script to expose (player-fetcher: 11, league-helper: 5, etc.)

**Key Design Decisions:**
- **Script-Specific Args:** Each runner gets args matching its config.py/constants.py settings
- **Universal Flags:** --debug and --e2e-test on all 7 runners
- **League Helper Mode Selection:** --mode arg to select 1 of 5 modes OR run all
- **E2E Behavior:** --e2e-test triggers: simulations (single run, 0-1 configs), fetchers (limited data), league helper (pre-defined flows)
- **Debug Behavior:** --debug triggers: DEBUG log level + behavioral changes (fewer iterations, smaller datasets)
- **Integration Test Validation:** Each test checks exit code AND specific expected outcomes (log counts, file existence, etc.)

---

## Scope Definition

### In Scope

- Add argparse to 4 scripts without it (player_fetcher, schedule_fetcher, league_helper + enhance 3 with it)
- Script-specific arguments from constants.py/config.py files (11 for player-fetcher, 4 for league-helper, 4 for historical, etc.)
- Universal --debug flag on all 7 runners (enables DEBUG logging + behavioral changes)
- Universal --e2e-test flag on all 7 runners (triggers fast E2E mode ≤3 min)
- League helper --mode argument (select 1 of 5 modes OR run all)
- E2E test modes with specific behaviors (simulations: 1 run/0-1 configs, fetchers: limited data, league helper: automated flows)
- Debug mode behavioral changes (fewer iterations, smaller datasets, verbose output)
- 7 individual integration test runners (one per script, test multiple argument combinations)
- 1 master integration test runner (runs all 7 individual runners)
- Integration tests validate exit codes AND specific expected outcomes
- Documentation updates (README.md, ARCHITECTURE.md, testing guide)
- Epic workflow guide updates (reference integration test runners in S7/S9)

### Out of Scope

- Configuration file support (only CLI arguments, not config files)
- Interactive debug modes (debug is non-interactive with pre-defined behavior)
- GUI or web interface for configuration
- Automated CI/CD integration (manual test runner execution only)
- Performance optimizations beyond E2E requirements
- New features or functionality (only making existing features configurable)
- Mocking or stubbing APIs (use real APIs with data limiting)

### Deferred (Future Work)

- Mock data support for fetchers (mentioned in epic notes as "nice-to-have")
- Configuration file format (YAML/TOML) if CLI args become too numerous
- Automated smoke testing in CI/CD pipeline

---

## Proposed Feature Breakdown

**Total Features:** 9
**Implementation Order:** Sequential (simple → complex scripts)

### Feature 01: player_fetcher

**Purpose:** Add comprehensive argparse and debug/E2E modes to player data fetcher

**Scope:**
- Add argparse with 13+ arguments (--week, --output-dir, --create-csv, --create-json, --create-excel, --create-position-json, --enable-historical-save, --enable-game-data, --preserve-locked, --log-level, --progress-frequency, --debug, --e2e-test)
- Add debug mode (DEBUG logging + minimal data fetch)
- Add E2E test mode (fetch limited player set, ≤3 min)
- Unit tests for argument handling

**Dependencies:** None (establishes patterns)

**Discovery Basis:**
- Based on Finding: player-data-fetcher/config.py has 11 frequently-modified constants (Iteration 2)
- Based on User Answer Q1: Script-specific args from constants
- Based on User Answer Q3: Fetchers use real APIs with data limiting
- Based on User Answer Q4: Debug = behavioral changes + DEBUG logs

**Estimated Size:** SMALL-MEDIUM

---

### Feature 02: schedule_fetcher

**Purpose:** Add argparse and debug/E2E modes to schedule fetcher

**Scope:**
- Add argparse with arguments (--season, --output-path, --debug, --e2e-test, --log-level)
- Add debug mode (DEBUG logging)
- Add E2E test mode (fetch single week schedule, ≤3 min)
- Unit tests

**Dependencies:** None (benefits from Feature 01 patterns)

**Discovery Basis:**
- Based on Finding: schedule-data-fetcher has no config file (Iteration 2)
- Based on User Answer Q1: Script-specific args
- Based on User Answer Q4: Debug mode with behavioral changes

**Estimated Size:** SMALL

---

### Feature 03: game_data_fetcher

**Purpose:** Enhance existing argparse with debug/E2E modes

**Scope:**
- Enhance existing argparse (add --debug, --e2e-test, --log-level)
- Add debug mode (DEBUG logging + limited weeks)
- Add E2E test mode (fetch single week, ≤3 min)
- Unit tests

**Dependencies:** None

**Discovery Basis:**
- Based on Finding: Already has argparse with --season, --output, --weeks (Iteration 1)
- Based on User Answer Q3: Real APIs with data limiting
- Based on User Answer Q4: Debug = behavioral + logging

**Estimated Size:** SMALL

---

### Feature 04: historical_compiler

**Purpose:** Enhance historical compiler with debug/E2E modes and additional args

**Scope:**
- Enhance argparse (add --debug, --e2e-test, --timeout, --rate-limit-delay, --log-level)
- Add debug mode (DEBUG logging + single week compilation)
- Add E2E test mode (compile minimal dataset, ≤3 min)
- Unit tests

**Dependencies:** None

**Discovery Basis:**
- Based on Finding: historical_data_compiler/constants.py has configurable timeouts, rate limits (Iteration 2)
- Based on User Answer Q1: Script-specific args from constants
- Based on User Answer Q3: Fetchers limit data for speed

**Estimated Size:** SMALL-MEDIUM

---

### Feature 05: win_rate_simulation

**Purpose:** Add E2E mode and debug enhancements to win rate simulation

**Scope:**
- Enhance argparse (add --e2e-test flag)
- Add E2E test mode (single run, 0-1 random configs, ≤3 min)
- Enhance debug mode (already has --log-level, add behavioral changes for debug)
- Unit tests for E2E mode

**Dependencies:** None

**Discovery Basis:**
- Based on Finding: Already has extensive argparse (Iteration 2)
- Based on User Answer Q3: Simulations single run with 0-1 random configs
- Based on User Answer Q4: Debug = behavioral + logging

**Estimated Size:** SMALL

---

### Feature 06: accuracy_simulation

**Purpose:** Add E2E mode and debug enhancements to accuracy simulation

**Scope:**
- Enhance argparse (add --e2e-test flag)
- Add E2E test mode (single horizon, single run, 0-1 test values, ≤3 min)
- Enhance debug mode (already has --log-level arg, add behavioral changes)
- Unit tests

**Dependencies:** None (benefits from Feature 05 patterns)

**Discovery Basis:**
- Based on Finding: Already has extensive argparse including --log-level (Iteration 2)
- Based on User Answer Q3: Single run, 0-1 configs for E2E
- Based on User Answer Q4: Debug behavioral changes

**Estimated Size:** SMALL-MEDIUM

---

### Feature 07: league_helper

**Purpose:** Add comprehensive argparse with mode selection and E2E test flows

**Scope:**
- Add argparse (--mode [1-5 or all], --submode, --config-path, --debug, --e2e-test, --data-folder, --log-level, --recommendation-count, --min-waiver-improvement)
- Create E2E test flows (automated flows for all 5 modes, skip user prompts, ≤3 min total)
- Add debug mode (DEBUG logging + smaller datasets)
- Unit tests for args and E2E flows

**Dependencies:** None (but benefits from all previous patterns)

**Discovery Basis:**
- Based on Finding: 5 modes identified (Add to Roster, Starter Helper, Trade Simulator, Modify Player Data, Save Calculated Points) (Iteration 2)
- Based on Finding: league_helper/constants.py has 4 configurable settings (Iteration 2)
- Based on User Answer Q2: Support all 4 modes OR specific mode selection
- Based on User Answer Q3: E2E should be fast (≤3 min)
- Based on User Answer Q4: Debug = behavioral + logging

**Estimated Size:** MEDIUM-LARGE (most complex)

---

### Feature 08: integration_test_framework

**Purpose:** Create integration test runners for all scripts

**Scope:**
- Create 7 individual test runners (test_player_fetcher_integration.py through test_league_helper_integration.py)
- Enhance 2 existing simulation integration tests
- Create master runner (run_all_integration_tests.py)
- Each test validates exit code AND specific expected outcomes (log counts, file existence, output validation)
- Tests cover multiple argument combinations per script

**Dependencies:** Features 01-07 (need all scripts enhanced)

**Discovery Basis:**
- Based on Epic Request: "integration test runner for each script... greater integration test runner that goes through all"
- Based on User Answer Q5: Tests check exit code AND expected outcomes (specific logs, result counts)
- Based on Finding: Existing integration tests for simulations to enhance (Iteration 1)

**Estimated Size:** MEDIUM

---

### Feature 09: documentation

**Purpose:** Update documentation for new arguments and testing workflows

**Scope:**
- Update README.md (Quick Start, Testing sections)
- Update ARCHITECTURE.md (Testing Architecture)
- Create docs/testing/INTEGRATION_TESTING_GUIDE.md
- Update epic workflow guides (reference integration tests in S7/S9)
- Document all new arguments with examples
- Add troubleshooting guide

**Dependencies:** Feature 08 (need tests complete to document)

**Discovery Basis:**
- Based on Epic Request: "update all relevant documentation... ensure integration test runners are used"
- Based on User Answer Q5: Integration tests have specific validation (needs documentation)
- Based on Finding: README.md and ARCHITECTURE.md exist (Iteration 1)

**Estimated Size:** SMALL

---

### Feature Dependency Diagram

```
Feature 01 (player_fetcher)      Feature 02 (schedule_fetcher)
Feature 03 (game_data_fetcher)   Feature 04 (historical_compiler)
Feature 05 (win_rate_simulation) Feature 06 (accuracy_simulation)
Feature 07 (league_helper)
         ↓ (all complete)
Feature 08 (integration_test_framework)
         ↓
Feature 09 (documentation)
```

**Implementation Order:** Features 01-07 (sequential, simple → complex), then 08, then 09

---

## User Approval

**Discovery Approved:** YES
**Approved Date:** 2026-01-29
**Approved By:** User

**Approval Notes:**
User approved Discovery findings and instructed to proceed with epic work. Comprehensive Script-Specific Argparse approach validated with 9-feature breakdown. All 5 discovery questions resolved successfully.

---

## Post-Discovery Updates

No post-Discovery updates.
