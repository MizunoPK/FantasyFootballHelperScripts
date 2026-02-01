# Epic Smoke Test Plan: improve_configurability_of_scripts

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** 2026-01-28 (S1)
**Last Updated:** 2026-01-31 (S4 Round 3 - Feature 09 Documentation)

**✅ STATUS: S4 UPDATED (ALL 9 FEATURES) - Ready for Implementation**

This test plan has been comprehensively updated in S4 based on ALL 9 feature specifications completed in S2-S3. Test scenarios are now specific, measurable, and directly traceable to feature requirements. Includes documentation validation criteria for Feature 09.

---

## Epic Success Criteria (MEASURABLE - Updated S4)

**The epic is successful when ALL of the following measurable criteria are met:**

### 1. Argument Support (All 7 Features)
- ✅ --help displays usage with all arguments listed
- ✅ --debug flag exists and enables DEBUG logging
- ✅ --e2e-test flag exists and runs automated test mode
- ✅ --log-level accepts [DEBUG, INFO, WARNING, ERROR, CRITICAL]
- **Measurement**: Run `--help` for all 7 scripts, verify argument presence

### 2. E2E Performance (All 7 Features)
- ✅ Each E2E mode completes in ≤180 seconds (3 minutes)
- ✅ Exit code 0 (success)
- ✅ No errors in output
- **Measurement**: `time python <script> --e2e-test`, verify duration ≤180s

### 3. E2E Behavior Validation (Feature-Specific)
- Feature 01: Fetches player data for 1 league (automated selection)
- Feature 02: Fetches schedule for current season (automated)
- Feature 03: Fetches game data for 1 week (week 1, automated)
- Feature 04: Compiles data for 1 season (current season, skips backups)
- Feature 05: Runs test mode with 2 test values (automated)
- Feature 06: Runs test mode with 2 test values, runs once and exits
- Feature 07: Runs all 5 modes with automated selections (≤3 min total)
- **Measurement**: Verify actual output matches documented E2E behavior from specs

### 4. Data Flow Integration
- ✅ Features 01-03 outputs compatible with Feature 04 input (fetchers → compiler)
- ✅ Feature 04 output compatible with Features 05-06 input (compiler → simulations)
- ✅ All data available to Feature 07 (league helper modes)
- **Measurement**: Run full chain (fetchers → compiler → simulations → league helper), verify no errors

### 5. Logging Consistency (All 7 Features)
- ✅ --debug flag sets DEBUG level (verbose output visible)
- ✅ E2E mode defaults to INFO level (unless --debug or --log-level override)
- ✅ Default mode uses INFO level
- **Measurement**: Compare log output with/without --debug, verify level changes

### 6. Argument Validation (All 7 Features)
- ✅ Invalid arguments show user-friendly error message
- ✅ No crashes from invalid input
- ✅ Error messages suggest correct usage
- **Measurement**: Test invalid inputs, verify graceful error handling

### 7. Integration Test Framework (Feature 08)
- ✅ 5 new CLI test files exist (test_player_fetcher_cli.py, test_schedule_fetcher_cli.py, test_game_data_fetcher_cli.py, test_historical_compiler_cli.py, test_league_helper_cli.py)
- ✅ 2 enhanced files exist with CLI test classes (test_simulation_integration.py → TestWinRateSimulationCLI, test_accuracy_simulation_integration.py → TestAccuracySimulationCLI)
- ✅ 1 master runner exists (tests/integration/run_all_integration_tests.py)
- ✅ Master runner executes all 7 test runners (5 new + 2 enhanced)
- ✅ All CLI tests use --e2e-test flag and validate exit codes + specific outcomes
- ✅ Exit code 0 when all tests pass
- **Measurement**: `python tests/integration/run_all_integration_tests.py`, verify exit code 0 and 7/7 test runners passed

### 8. Unit Test Stability
- ✅ All existing unit tests still pass (100% pass rate)
- ✅ No regressions introduced
- **Measurement**: `python tests/run_all_tests.py`, verify exit code 0

### 9. Backward Compatibility
- ✅ Feature 03: --output flag preserved (existing argparse compatibility)
- ✅ Feature 04: --verbose flag preserved (existing argparse compatibility)
- ✅ All existing workflows continue to work without modification
- **Measurement**: Run legacy commands, verify no breaking changes

### 10. Documentation Completeness and Accuracy (Feature 09)
- ✅ README.md updated: Quick Start section documents all 60+ CLI arguments across 7 scripts
- ✅ README.md updated: Testing section includes integration testing subsection
- ✅ ARCHITECTURE.md updated: Testing Architecture includes integration test framework documentation
- ✅ docs/testing/INTEGRATION_TESTING_GUIDE.md created with 5 sections (~300 lines)
- ✅ Workflow guides updated: S7/S9 reference integration test runners
- ✅ Documentation accuracy: All CLI arguments match Features 01-07 specs (zero missing/incorrect)
- ✅ Documentation accuracy: Integration test framework matches Feature 08 spec
- ✅ Cross-references valid: All spec references, file paths, guide references accurate
- **Measurement**: Manual review of documentation files, validate argument lists against feature specs, verify all cross-references resolve correctly

**Epic is considered SUCCESSFUL when ALL 10 criteria above are met with 100% pass rate.**

---

## Integration Points (Identified in S4)

**Data Flow Chain:**
```
Features 01-03 (Fetchers) → Feature 04 (Compiler) → Features 05-06 (Simulations) → Feature 07 (League Helper)
```

### Integration Point 1: Fetcher → Compiler Dependencies
- Feature 01 (player_fetcher) output → Feature 04 input
- Feature 02 (schedule_fetcher) output → Feature 04 input
- Feature 03 (game_data_fetcher) output → Feature 04 input
- **Critical Tests**: Data format compatibility, path resolution, data completeness

### Integration Point 2: Compiler → Simulation Dependencies
- Feature 04 (historical_compiler) output → Feature 05 (win_rate_simulation) input
- Feature 04 (historical_compiler) output → Feature 06 (accuracy_simulation) input
- **Critical Tests**: Compiled data structure, value validation, simulation execution success

### Integration Point 3: All Features → League Helper
- Features 01-06 data availability → Feature 07 (league_helper) modes
- **Critical Tests**: Data loading for all 5 modes, mode functionality with real data

### Integration Point 4: Common Argument Patterns (Cross-Feature)
- All 7 features: --debug, --e2e-test, --log-level
- **Critical Tests**: Consistent behavior across all scripts, uniform error handling

### Integration Point 5: Feature 08 → Features 01-07 (Test Framework Dependency)
- Feature 08 (integration_test_framework) tests Features 01-07 CLI implementations
- Feature 08 cannot be implemented until Features 01-07 are implemented (S5-S7)
- Feature 08 validates:
  - CLI argument parsing (subprocess.run() execution)
  - Exit codes + specific outcomes (logs, files, formats)
  - --e2e-test mode behavior (≤180 seconds)
  - Precedence rules (--debug forces DEBUG level)
- **Critical Tests**: Integration tests pass for all 7 scripts, master runner aggregates results correctly

### Integration Point 6: Feature 09 → Features 01-08 (Documentation Dependency)
- Feature 09 (documentation) documents Features 01-08 implementations
- Feature 09 cannot be implemented until Features 01-08 specs are finalized (S2-S3-S4)
- Feature 09 content sources:
  - Features 01-07 specs: CLI argument lists, E2E behaviors, debug modes
  - Feature 08 spec: Integration test framework structure, validation logic
- Feature 09 validates:
  - Documentation completeness (all 60+ arguments documented)
  - Documentation accuracy (arguments match specs exactly)
  - Cross-references valid (all spec/file/guide references resolve)
- **Critical Tests**: Manual review of documentation against feature specs, cross-reference validation, argument list comparison

---

## Update History

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| 2026-01-28 | S1 | (initial) | Initial plan created | Epic planning based on epic request assumptions |
| 2026-01-30 | S4 Round 1 | Group 1 (F01-07) | MAJOR UPDATE: Added measurable criteria, integration points, 17+ specific test scenarios, data quality checks | S2-S3 complete for all 7 Group 1 features - specs provide concrete implementation details |
| 2026-01-30 | S4 Round 2 | Group 2 (F08) | Updated criterion #7 (integration test framework), fixed test file names (5 new CLI files + 2 enhanced), added Integration Point 5, enhanced Scenario 5.2 expected results | S2-S3 complete for Feature 08 - integration test framework spec finalized |
| 2026-01-31 | S4 Round 3 | Group 3 (F09) | Added criterion #10 (documentation completeness and accuracy), added Integration Point 6 (Feature 09 → Features 01-08 documentation dependency), validation approach documented | S2-S3 complete for Feature 09 - documentation spec finalized |

**Current version is informed by:**
- S1: Initial assumptions from epic request
- **Round 1 (Group 1 - Features 01-07):**
  - S2: Deep dive specifications for 7 features (player_fetcher, schedule_fetcher, game_data_fetcher, historical_compiler, win_rate_simulation, accuracy_simulation, league_helper)
  - S3: Cross-feature consistency validation (18 issues resolved, all specs aligned)
  - S4: Integration points 1-4, measurable criteria 1-9, test scenarios 1-7
- **Round 2 (Group 2 - Feature 08):**
  - S2: Deep dive specification for integration_test_framework
  - S3: Cross-feature alignment (Feature 08 vs Features 01-07, 1 precedence rule override)
  - S4: Integration Point 5, updated criterion #7, enhanced test scenarios 5.1-5.2
- **Round 3 (Group 3 - Feature 09):**
  - S2: Deep dive specification for documentation
  - S3: Cross-feature alignment (Feature 09 vs Features 01-08, zero conflicts)
  - S4: Integration Point 6, added criterion #10, documentation validation approach ← **CURRENT**
- S8.P2 updates: (Not yet - will update after each feature implementation)

---

## Test Scenarios (S4 - SPECIFIC & EXECUTABLE)

**Instructions for Agent:**
- Execute EACH scenario listed below during S9 (Epic-Level Final QC)
- Verify ACTUAL behavior (not just "command runs")
- Verify ACTUAL data values (not just "file exists")
- Document results in S9 with pass/fail status for each scenario
- If ANY scenario fails, enter debugging protocol and fix before proceeding

**Test Execution Order:**
1. Part 1: Feature-Level Tests (validate individual scripts)
2. Part 2: Integration Tests (validate data flow between features)
3. Part 3: Epic-Level Tests (validate common patterns across all features)
4. Part 4: Data Quality Tests (validate actual output values)

---

### Part 1: Feature-Level Tests (Individual Scripts)

**Scenario 1.1: Feature 01 (player_fetcher) - E2E Validation**
```bash
# Test E2E mode completes in ≤180s with automated selection
time python run_player_fetcher.py --e2e-test

# Verify output file exists and has content
ls -lh data/player_stats_*.csv
```

**Expected Result:**
- Completes in ≤180 seconds
- Exit code 0
- Fetches player data for 1 league (first available, automated selection)
- Output: data/player_stats_<league>.csv created with player data

---

**Scenario 1.2: Feature 02 (schedule_fetcher) - E2E Validation**
```bash
# Test E2E mode completes in ≤180s
time python run_schedule_fetcher.py --e2e-test

# Verify output file exists and has content
ls -lh data/schedule_*.csv
```

**Expected Result:**
- Completes in ≤180 seconds
- Exit code 0
- Fetches schedule for current season (automated selection)
- Output: data/schedule_<season>.csv created with schedule data

---

**Scenario 1.3: Feature 03 (game_data_fetcher) - E2E Validation**
```bash
# Test E2E mode completes in ≤180s
time python run_game_data_fetcher.py --e2e-test

# Verify output file exists and has content
ls -lh data/game_data_*.json
```

**Expected Result:**
- Completes in ≤180 seconds
- Exit code 0
- Fetches game data for 1 week (week 1, automated selection)
- Output: data/game_data_week_1.json created with game data

---

**Scenario 1.4: Feature 04 (historical_compiler) - E2E Validation**
```bash
# Test E2E mode completes in ≤180s
time python compile_historical_data.py --e2e-test

# Verify output file exists and has content
ls -lh data/compiled_historical_*.csv
```

**Expected Result:**
- Completes in ≤180 seconds
- Exit code 0
- Compiles data for 1 season (current season, automated selection)
- Skips backup creation (E2E optimization)
- Output: data/compiled_historical_<season>.csv created with compiled data

---

**Scenario 1.5: Feature 05 (win_rate_simulation) - E2E Validation**
```bash
# Test E2E mode completes in ≤180s
time python run_win_rate_simulation.py --e2e-test

# Verify exit code
echo "Exit code: $?"
```

**Expected Result:**
- Completes in ≤180 seconds
- Exit code 0
- Runs test mode with 2 test values (automated selection)
- Output: Simulation results displayed to console

---

**Scenario 1.6: Feature 06 (accuracy_simulation) - E2E Validation**
```bash
# Test E2E mode completes in ≤180s
time python run_accuracy_simulation.py --e2e-test

# Verify exit code
echo "Exit code: $?"
```

**Expected Result:**
- Completes in ≤180 seconds
- Exit code 0
- Runs test mode with 2 test values (automated selection)
- Runs once and exits (NOT continuous loop)
- Output: Accuracy results displayed to console

---

**Scenario 1.7: Feature 07 (league_helper) - E2E Validation**
```bash
# Test E2E mode completes in ≤180s (ALL 5 MODES)
time python run_league_helper.py --e2e-test

# Verify exit code
echo "Exit code: $?"
```

**Expected Result:**
- Completes in ≤180 seconds (all 5 modes combined)
- Exit code 0
- Runs all 5 modes sequentially with automated selections:
  - Mode 1 (Draft): Show 2 recommendations (debug count)
  - Mode 2 (Optimizer): Show 2 recommendations (debug count)
  - Mode 3 (Trade): Show 1 trade (debug count)
  - Mode 4 (Search): Search top 50 players (debug count)
  - Mode 5 (Data Editor): Load data only, no edits
- No user prompts (fully automated)
- --mode argument ignored when --e2e-test is set (warning displayed)

---

### Part 2: Integration Tests (Data Flow Validation)

**Scenario 2.1: Fetcher → Compiler Integration**
```bash
# Run fetchers in sequence (create input data for compiler)
python run_player_fetcher.py --e2e-test
python run_schedule_fetcher.py --e2e-test
python run_game_data_fetcher.py --e2e-test

# Run compiler (should consume fetcher outputs)
python compile_historical_data.py --e2e-test

# Verify compiled output
ls -lh data/compiled_historical_*.csv
```

**Expected Result:**
- Compiler reads fetcher outputs without errors
- Compiled data file created successfully
- No "file not found" or "format error" messages
- Data from all 3 fetchers integrated into compiled output

---

**Scenario 2.2: Compiler → Simulation Integration**
```bash
# Run compiler first (create input data for simulations)
python compile_historical_data.py --e2e-test

# Run simulations (should consume compiler output)
python run_win_rate_simulation.py --e2e-test
python run_accuracy_simulation.py --e2e-test

# Verify exit codes
echo "Win rate simulation exit code: $?"
echo "Accuracy simulation exit code: $?"
```

**Expected Result:**
- Simulations read compiled data without errors
- Simulation results displayed successfully
- No "file not found" or "data incomplete" errors
- Both simulations exit code 0

---

**Scenario 2.3: Full Data Flow Chain (End-to-End Pipeline)**
```bash
# Run complete data flow: Fetchers → Compiler → Simulations
python run_player_fetcher.py --e2e-test && \
python run_schedule_fetcher.py --e2e-test && \
python run_game_data_fetcher.py --e2e-test && \
python compile_historical_data.py --e2e-test && \
python run_win_rate_simulation.py --e2e-test && \
python run_accuracy_simulation.py --e2e-test

# Verify final exit code
echo "Full chain exit code: $?"
```

**Expected Result:**
- All commands complete successfully (exit code 0)
- Data flows through entire pipeline without errors
- Each stage consumes previous stage output correctly
- No broken integration points

---

### Part 3: Epic-Level Tests (Common Patterns Across All Features)

**Scenario 3.1: Debug Flag Consistency (All 7 Features)**
```bash
# Test --debug flag enables DEBUG logging for all scripts
python run_player_fetcher.py --debug --e2e-test 2>&1 | grep -c "DEBUG"
python run_schedule_fetcher.py --debug --e2e-test 2>&1 | grep -c "DEBUG"
python run_game_data_fetcher.py --debug --e2e-test 2>&1 | grep -c "DEBUG"
python compile_historical_data.py --debug --e2e-test 2>&1 | grep -c "DEBUG"
python run_win_rate_simulation.py --debug --e2e-test 2>&1 | grep -c "DEBUG"
python run_accuracy_simulation.py --debug --e2e-test 2>&1 | grep -c "DEBUG"
python run_league_helper.py --debug --e2e-test 2>&1 | grep -c "DEBUG"
```

**Expected Result:**
- All 7 scripts show DEBUG messages (count > 0)
- Consistent debug output format across all scripts
- More verbose output than without --debug flag

---

**Scenario 3.2: Log Level Argument (All 7 Features)**
```bash
# Test --log-level WARNING suppresses INFO messages
python run_player_fetcher.py --log-level WARNING --e2e-test 2>&1 | grep -c "INFO"
# Expected: 0 INFO messages (WARNING level should suppress INFO)

# Test --log-level INFO shows INFO messages
python run_player_fetcher.py --log-level INFO --e2e-test 2>&1 | grep -c "INFO"
# Expected: >0 INFO messages

# Repeat pattern for all 7 scripts to verify consistency
```

**Expected Result:**
- --log-level argument works consistently across all 7 scripts
- WARNING level suppresses INFO messages
- INFO level shows INFO messages
- DEBUG level shows all messages
- Consistent behavior across all features

---

**Scenario 3.3: Help Text Validation (All 7 Features)**
```bash
# Verify --help displays all required arguments for each script
python run_player_fetcher.py --help | grep -E "(--debug|--e2e-test|--log-level)"
python run_schedule_fetcher.py --help | grep -E "(--debug|--e2e-test|--log-level)"
python run_game_data_fetcher.py --help | grep -E "(--debug|--e2e-test|--log-level)"
python compile_historical_data.py --help | grep -E "(--debug|--e2e-test|--log-level|--verbose)"
python run_win_rate_simulation.py --help | grep -E "(--debug|--e2e-test|--log-level)"
python run_accuracy_simulation.py --help | grep -E "(--debug|--e2e-test|--log-level)"
python run_league_helper.py --help | grep -E "(--debug|--e2e-test|--log-level|--mode)"
```

**Expected Result:**
- All 7 scripts show required arguments in help text
- Common arguments (--debug, --e2e-test, --log-level) present in all scripts
- Feature 04: Also shows --verbose (backward compatibility)
- Feature 07: Also shows --mode (unique to league_helper)
- Help text is clear and user-friendly

---

**Scenario 3.4: Argument Validation (Error Handling)**
```bash
# Test invalid --log-level value
python run_player_fetcher.py --log-level INVALID 2>&1

# Test invalid argument
python run_player_fetcher.py --invalid-arg 2>&1

# Test conflicting arguments (Feature 04 specific)
python compile_historical_data.py --verbose --log-level DEBUG 2>&1
```

**Expected Result:**
- Invalid --log-level shows user-friendly error message with valid choices
- Invalid arguments show error message suggesting --help
- No crashes or stack traces from invalid input
- Feature 04: --verbose takes precedence over --log-level (with warning message)

---

### Part 4: Data Quality Tests (Value Verification)

**Scenario 4.1: Player Data Quality (Feature 01 Output)**
```bash
# Run fetcher and verify actual data VALUES
python run_player_fetcher.py --e2e-test

# Verify CSV has expected columns and non-empty values
python -c "
import pandas as pd
import glob
csv_file = glob.glob('data/player_stats_*.csv')[0]
df = pd.read_csv(csv_file)
print(f'Rows: {len(df)}')
print(f'Columns: {list(df.columns)}')
print(f'Null values: {df.isnull().sum().sum()}')
print(f'Sample data:')
print(df.head(3))
"
```

**Expected Result:**
- Rows > 0 (data fetched successfully)
- Columns include player names, stats, positions (verify actual column names)
- Null values = 0 or minimal (complete data)
- Sample data shows actual player information (not empty/placeholder values)

---

**Scenario 4.2: Compiled Data Quality (Feature 04 Output)**
```bash
# Run compiler and verify actual compiled VALUES
python compile_historical_data.py --e2e-test

# Verify compiled CSV has integrated data from all fetchers
python -c "
import pandas as pd
import glob
csv_file = glob.glob('data/compiled_historical_*.csv')[0]
df = pd.read_csv(csv_file)
print(f'Rows: {len(df)}')
print(f'Columns: {list(df.columns)}')
if 'date' in df.columns:
    print(f'Date range: {df[\"date\"].min()} to {df[\"date\"].max()}')
print(f'Sample compiled data:')
print(df.head(3))
"
```

**Expected Result:**
- Rows > 0 (data compiled successfully)
- Columns include data from all 3 fetchers (player stats + schedule + game data)
- Date range covers fetched season (if date column exists)
- Sample data shows integrated information from multiple sources

---

**Scenario 4.3: Simulation Output Quality (Features 05-06 Results)**
```bash
# Run simulations and verify actual result VALUES
python run_win_rate_simulation.py --e2e-test > win_rate_output.txt
python run_accuracy_simulation.py --e2e-test > accuracy_output.txt

# Verify output contains expected result format
echo "=== Win Rate Simulation Output ==="
cat win_rate_output.txt

echo "=== Accuracy Simulation Output ==="
cat accuracy_output.txt

# Check for expected keywords in output
grep -E "win rate|accuracy|parameter|result|test" win_rate_output.txt
grep -E "win rate|accuracy|parameter|result|test" accuracy_output.txt
```

**Expected Result:**
- Win rate simulation shows parameter values and results (numeric)
- Accuracy simulation shows accuracy percentages (0-100% range)
- Results are actual values, not placeholders or errors
- Output format is clear and interpretable
- 2 test values executed for each simulation (as documented in E2E specs)

---

**Scenario 4.4: League Helper Mode Execution (Feature 07 All Modes)**
```bash
# Run league helper E2E and capture mode execution
python run_league_helper.py --e2e-test > league_helper_output.txt

# Verify all 5 modes executed
echo "=== League Helper E2E Output ==="
cat league_helper_output.txt

# Check for all 5 modes in output
grep -i "draft" league_helper_output.txt
grep -i "optimizer" league_helper_output.txt
grep -i "trade" league_helper_output.txt
grep -i "search" league_helper_output.txt
grep -i "data editor" league_helper_output.txt
```

**Expected Result:**
- All 5 modes execute in sequence (draft, optimizer, trade, search, data editor)
- Draft mode shows 2 recommendations (debug count)
- Optimizer mode shows 2 recommendations (debug count)
- Trade mode shows 1 trade (debug count)
- Search mode searches top 50 players (debug count)
- Data Editor mode loads data only, no edits
- Total execution time ≤180 seconds
- No user prompts (fully automated)

---

### Part 5: Integration Test Framework Validation

**Scenario 5.1: Master Test Runner Execution**
```bash
# Run master integration test runner
python tests/integration/run_all_integration_tests.py

# Verify exit code
echo "Master runner exit code: $?"
```

**Expected Result:**
- Master runner executes all 7 individual test runners sequentially
- All tests pass (exit code 0)
- No errors reported
- Test summary shows 7/7 features passed

---

**Scenario 5.2: Individual CLI Integration Test Runners**
```bash
# Run each individual CLI test runner to verify isolation
# 5 new CLI test files
pytest tests/integration/test_player_fetcher_cli.py
pytest tests/integration/test_schedule_fetcher_cli.py
pytest tests/integration/test_game_data_fetcher_cli.py
pytest tests/integration/test_historical_compiler_cli.py
pytest tests/integration/test_league_helper_cli.py

# 2 enhanced files with CLI test classes
pytest tests/integration/test_simulation_integration.py::TestWinRateSimulationCLI
pytest tests/integration/test_accuracy_simulation_integration.py::TestAccuracySimulationCLI

# Verify all exit codes
echo "All individual tests exit code: $?"
```

**Expected Result:**
- Each individual test runner can execute independently
- All individual tests pass (exit code 0 for each)
- Each test validates:
  - Exit codes (assert returncode == 0)
  - Specific outcomes (log messages, output files, file formats)
  - Universal CLI arguments (--debug, --e2e-test, --log-level)
  - Precedence rule (--debug forces DEBUG level)
  - 3-5 representative argument combinations per script
- Tests complete in ≤180 seconds per script
- No cross-test dependencies or failures

---

### Part 6: Backward Compatibility Validation

**Scenario 6.1: Feature 03 - Existing --output Flag**
```bash
# Test that existing --output argument still works (backward compatibility)
python run_game_data_fetcher.py --output data/custom_game_data.json --e2e-test

# Verify output at custom location
ls -lh data/custom_game_data.json
```

**Expected Result:**
- --output flag works as before (no breaking changes)
- Output file created at specified custom location
- Backward compatible with existing run_game_data_fetcher.py usage

---

**Scenario 6.2: Feature 04 - Existing --verbose Flag**
```bash
# Test that existing --verbose argument still works (backward compatibility)
python compile_historical_data.py --verbose --e2e-test 2>&1 | grep -c "verbose"

# Test precedence: --verbose takes precedence over --log-level
python compile_historical_data.py --verbose --log-level WARNING --e2e-test 2>&1
# Expected: Verbose output shown (--verbose wins), warning displayed about precedence
```

**Expected Result:**
- --verbose flag works as before (no breaking changes)
- --verbose takes precedence over --log-level when both specified
- Warning message displayed about precedence rule
- Backward compatible with existing compile_historical_data.py usage

---

### Part 7: Unit Test Stability Validation

**Scenario 7.1: All Unit Tests Pass**
```bash
# Run complete unit test suite
python tests/run_all_tests.py

# Verify exit code
echo "Unit tests exit code: $?"
```

**Expected Result:**
- All existing unit tests pass (100% pass rate)
- Exit code 0
- No regressions introduced by new argument additions
- Test count >= 2,200 (existing baseline)

---

**Scenario 7.2: Feature 09 (documentation) - Documentation Validation**
```bash
# Validate README.md updates
grep "player_fetcher" README.md
grep "integration testing" README.md

# Validate ARCHITECTURE.md updates
grep "Integration Test Framework" ARCHITECTURE.md

# Validate INTEGRATION_TESTING_GUIDE.md exists
ls -lh docs/testing/INTEGRATION_TESTING_GUIDE.md

# Validate workflow guide updates
grep "integration test" feature-updates/guides_v2/stages/s7/s7_p1_smoke_testing.md
grep "integration test" feature-updates/guides_v2/stages/s9/s9_p1_epic_smoke_testing.md
```

**Expected Result:**
- README.md Quick Start: Documents all 7 scripts with CLI arguments (60+ arguments total)
- README.md Testing: Includes integration testing subsection with master runner execution
- ARCHITECTURE.md Testing Architecture: Includes integration test framework documentation with directory tree
- docs/testing/INTEGRATION_TESTING_GUIDE.md: Created with 5 sections (~300 lines)
- S7/S9 workflow guides: Reference integration test runners with example commands
- **Manual validation required**:
  - Cross-reference CLI argument lists in README against Features 01-07 specs (verify accuracy)
  - Cross-reference integration test details against Feature 08 spec (verify accuracy)
  - Verify all cross-references resolve correctly (no broken links or incorrect line numbers)

**Validation Checklist (Manual Review):**
- [ ] All 60+ CLI arguments documented (no missing arguments from specs)
- [ ] Argument descriptions match spec requirements
- [ ] Integration test framework structure matches Feature 08 spec
- [ ] All cross-references (features, files, guides) are accurate
- [ ] No typos or formatting issues
- [ ] Examples are realistic and match expected usage patterns

---

## Test Execution Summary Template (For S9)

**Agent Instructions for S9:** Copy this template to S9 documentation and fill in results for each scenario.

```markdown
## Epic Smoke Test Execution Results

**Date Executed:** [YYYY-MM-DD]
**Executed By:** Agent ID
**Stage:** S9.P1 (Epic Smoke Testing)

### Results Summary

| Part | Scenario | Status | Notes |
|------|----------|--------|-------|
| 1.1 | Feature 01 E2E | ☐ PASS ☐ FAIL | |
| 1.2 | Feature 02 E2E | ☐ PASS ☐ FAIL | |
| 1.3 | Feature 03 E2E | ☐ PASS ☐ FAIL | |
| 1.4 | Feature 04 E2E | ☐ PASS ☐ FAIL | |
| 1.5 | Feature 05 E2E | ☐ PASS ☐ FAIL | |
| 1.6 | Feature 06 E2E | ☐ PASS ☐ FAIL | |
| 1.7 | Feature 07 E2E | ☐ PASS ☐ FAIL | |
| 2.1 | Fetcher→Compiler Integration | ☐ PASS ☐ FAIL | |
| 2.2 | Compiler→Simulation Integration | ☐ PASS ☐ FAIL | |
| 2.3 | Full Data Flow Chain | ☐ PASS ☐ FAIL | |
| 3.1 | Debug Flag Consistency | ☐ PASS ☐ FAIL | |
| 3.2 | Log Level Argument | ☐ PASS ☐ FAIL | |
| 3.3 | Help Text Validation | ☐ PASS ☐ FAIL | |
| 3.4 | Argument Validation | ☐ PASS ☐ FAIL | |
| 4.1 | Player Data Quality | ☐ PASS ☐ FAIL | |
| 4.2 | Compiled Data Quality | ☐ PASS ☐ FAIL | |
| 4.3 | Simulation Output Quality | ☐ PASS ☐ FAIL | |
| 4.4 | League Helper Mode Execution | ☐ PASS ☐ FAIL | |
| 5.1 | Master Test Runner | ☐ PASS ☐ FAIL | |
| 5.2 | Individual Test Runners | ☐ PASS ☐ FAIL | |
| 6.1 | Feature 03 Backward Compat | ☐ PASS ☐ FAIL | |
| 6.2 | Feature 04 Backward Compat | ☐ PASS ☐ FAIL | |
| 7.1 | Unit Test Stability | ☐ PASS ☐ FAIL | |

**Overall Pass Rate:** [X/23 scenarios passed]

**Issues Found:** [List any failures with issue numbers]

**Next Steps:** [If all pass: proceed to S9.P2. If any fail: enter debugging protocol]
```

---

**Note:** This test plan will be updated again in S8.P2 after each feature implementation to reflect any new integration points or edge cases discovered during development.
