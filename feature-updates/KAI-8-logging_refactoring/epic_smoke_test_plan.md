# Epic Smoke Test Plan: logging_refactoring

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** 2026-02-06 (S1)
**Last Updated:** 2026-02-08 (S8.P2 - Feature 01 complete)
**Status:** UPDATED WITH FEATURE 01 ACTUAL IMPLEMENTATION

---

## Epic Success Criteria

**The epic is successful if:**

1. All 6 scripts (league_helper, player-data-fetcher, accuracy_sim, win_rate_sim, historical_data_compiler, schedule_fetcher) support --enable-log-file CLI flag with file logging OFF by default
   - Example: `python run_league_helper.py --enable-log-file` creates log file, without flag does not

2. Log files are created in centralized logs/{script_name}/ subfolders
   - Example: logs/league_helper/, logs/accuracy_sim/, logs/player-data-fetcher/, etc.

3. Log files use timestamped naming format with microsecond precision for rotated files
   - Initial file: {script_name}-{YYYYMMDD_HHMMSS}.log (e.g., league_helper-20260206_143522.log)
   - Rotated files: {script_name}-{YYYYMMDD_HHMMSS_microseconds}.log (e.g., league_helper-20260206_143525_123456.log)
   - **[UPDATED S8.P2 - Feature 01]:** Microsecond precision prevents timestamp collisions during rapid rotation

4. Log rotation occurs automatically at 500 lines per file
   - Example: When line 500 written, new timestamped file created

5. Each script subfolder maintains maximum 50 log files, automatically deleting oldest when limit exceeded
   - Example: logs/league_helper/ never exceeds 50 files

6. logs/ folder is added to .gitignore (log files not committed to repository)
   - Example: `git status` shows logs/ as ignored

7. DEBUG level logs across all modules enable tracing of data flow and function execution without overwhelming the logs
   - Example: Function entry/exit with parameters, data transformations visible

8. INFO level logs across all modules provide runtime awareness of script progress and outcomes without implementation details
   - Example: "Starting draft helper mode", "Processing 150 players", "Draft recommendations complete"

9. All unit tests pass (100% pass rate, including updated test assertions for log changes)
   - Example: pytest runs show 2200+ tests passing

10. Epic smoke testing passes for all 6 scripts with --enable-log-file flag enabled
    - Example: All scenarios below execute successfully

**Epic is considered SUCCESSFUL when ALL criteria above are met.**

**Note on Success Criteria #7 and #8 (Log Quality):**
- DEBUG/INFO log quality (criteria #7-8) requires subjective manual review
- Smoke tests verify logs are CREATED and FORMATTED correctly
- Log CONTENT quality will be manually reviewed during S9.P3 (User Testing)
- User will verify: DEBUG logs show data flow, INFO logs show progress, both are appropriately verbose

---

## Update History

**Track when and why this plan was updated:**

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| 2026-02-06 | S1 | (initial) | Initial plan created | Epic planning based on Discovery findings |
| 2026-02-06 | S4 | ALL | Major update: Added specific test scenarios, integration points, concrete commands, measurable criteria | Based on completed feature specs from S2, zero conflicts from S3 |
| 2026-02-08 | S8.P2 | Feature 01 | Updated filename format (microseconds for rotated files), added rapid rotation test scenario, updated Scenario 4.1 | Feature 01 implementation revealed timestamp collision fix (microsecond precision added to prevent duplicate filenames during rapid rotation within same second) |

**Current version is informed by:**
- S1: Discovery Phase findings (7 features, group-based parallelization)
- S2: Feature specs (all 7 features, user-approved, zero conflicts)
- S3: Cross-feature alignment (21 pairwise comparisons, perfect consistency)
- S4: Integration points identified, specific test scenarios created
- S8.P2 updates:
  - Feature 01 (core_logging_infrastructure): Filename format, rapid rotation edge case

---

## Test Scenarios

**Instructions for Agent (S9):**
- Execute EACH scenario listed below
- Verify ACTUAL DATA VALUES (not just "file exists")
- Document results in S9

**Note:** Detailed scenarios will be added during S4 (Epic Testing Strategy) and refined during S8.P2 (after each feature implementation).

---

### Part 1: Epic-Level Import Tests

**Purpose:** Verify all epic modules can be imported together (Feature 01 provides core infrastructure)

**Test 1.1: Import LineBasedRotatingHandler**
```python
from utils.LineBasedRotatingHandler import LineBasedRotatingHandler
```
**Expected:** No ImportError, class available

**Test 1.2: Import Modified LoggingManager**
```python
from utils.LoggingManager import setup_logger
```
**Expected:** No ImportError, setup_logger function available with updated signature

**Test 1.3: Instantiate LineBasedRotatingHandler**
```python
handler = LineBasedRotatingHandler(
    filename='logs/test/test.log',
    max_lines=500,
    max_files=50,
    encoding='utf-8'
)
```
**Expected:** Handler created successfully, no errors

---

### Part 2: Epic-Level Entry Point Tests

**Purpose:** Verify all 6 scripts accept --enable-log-file flag (Features 02-07)

**Test 2.1: league_helper accepts --enable-log-file**
```bash
python run_league_helper.py --help
```
**Expected:** Help text shows `--enable-log-file` option

**Test 2.2: player-data-fetcher accepts --enable-log-file**
```bash
python run_player_fetcher.py --help
```
**Expected:** Help text shows `--enable-log-file` option

**Test 2.3: accuracy_sim accepts --enable-log-file**
```bash
python run_accuracy_simulation.py --help
```
**Expected:** Help text shows `--enable-log-file` option (in addition to existing `--log-level`)

**Test 2.4: win_rate_sim accepts --enable-log-file**
```bash
python run_win_rate_simulation.py --help
```
**Expected:** Help text shows `--enable-log-file` option

**Test 2.5: historical_data_compiler accepts --enable-log-file**
```bash
python compile_historical_data.py --help
```
**Expected:** Help text shows `--enable-log-file` option

**Test 2.6: schedule_fetcher accepts --enable-log-file**
```bash
python run_schedule_fetcher.py --help
```
**Expected:** Help text shows `--enable-log-file` option

**Test 2.7: Verify default behavior (file logging OFF)**
```bash
# Run any script WITHOUT --enable-log-file flag
python run_league_helper.py
```
**Expected:** No log file created, console logging only

---

### Part 3: Epic End-to-End Execution Tests

**Purpose:** Execute complete epic workflows with REAL data

**Scenario 3.1: league_helper with file logging enabled**
```bash
python run_league_helper.py --enable-log-file
```
**Expected Result:**
- Script executes successfully
- Log file created: `logs/league_helper/league_helper-{YYYYMMDD_HHMMSS}.log`
- Log file contains INFO messages (script start, mode selection, completion)
- Log file readable and properly formatted

**Scenario 3.2: player-data-fetcher with file logging enabled**
```bash
python run_player_fetcher.py --enable-log-file
```
**Expected Result:**
- Script executes successfully
- Log file created: `logs/player_data_fetcher/player_data_fetcher-{YYYYMMDD_HHMMSS}.log`
- Log file contains fetch progress INFO messages

**Scenario 3.3: accuracy_sim with file logging enabled**
```bash
python run_accuracy_simulation.py --enable-log-file
```
**Expected Result:**
- Script executes successfully
- Log file created: `logs/accuracy_simulation/accuracy_simulation-{YYYYMMDD_HHMMSS}.log`
- Log file contains simulation INFO messages

**Scenario 3.4: win_rate_sim with file logging enabled**
```bash
python run_win_rate_simulation.py --enable-log-file
```
**Expected Result:**
- Script executes successfully
- Log file created: `logs/win_rate_simulation/win_rate_simulation-{YYYYMMDD_HHMMSS}.log`
- Log file contains simulation INFO messages

**Scenario 3.5: historical_data_compiler with file logging enabled**
```bash
python compile_historical_data.py --enable-log-file
```
**Expected Result:**
- Script executes successfully
- Log file created: `logs/historical_data_compiler/historical_data_compiler-{YYYYMMDD_HHMMSS}.log`
- Log file contains compilation INFO messages

**Scenario 3.6: schedule_fetcher with file logging enabled**
```bash
python run_schedule_fetcher.py --enable-log-file
```
**Expected Result:**
- Script executes successfully
- Log file created: `logs/schedule_fetcher/schedule_fetcher-{YYYYMMDD_HHMMSS}.log`
- Log file contains fetch INFO messages

---

### Part 4: Cross-Feature Integration Tests

**Purpose:** Test feature interactions and integration points - verify LineBasedRotatingHandler works across all scripts

**Scenario 4.1: Log rotation at 500 lines**
```bash
# Use any script that generates sufficient log output
python run_league_helper.py --enable-log-file
# Generate enough operations to exceed 500 lines
```
**Expected Result:**
- Initial file created: `logs/league_helper/league_helper-{YYYYMMDD_HHMMSS}.log` (e.g., league_helper-20260208_120000.log)
- When line 501 written, rotation triggers new file: `logs/league_helper/league_helper-{YYYYMMDD_HHMMSS_microseconds}.log` (e.g., league_helper-20260208_120005_123456.log)
- **[UPDATED S8.P2 - Feature 01]:** Rotated file includes microsecond precision (6 additional digits after seconds)
- Both files exist in logs/league_helper/ folder
- Initial file contains exactly 500 lines
- No data loss between rotations
- Timestamps are unique even during rapid rotation

**Why updated:** Feature 01 implementation (utils/LineBasedRotatingHandler.py:169-176) adds microsecond precision to prevent timestamp collisions discovered during S7 smoke testing.

**Scenario 4.2: Max 50 files cleanup**
```bash
# Generate 51 log files in one script's folder
# (Simulate by creating dummy files or running script repeatedly)
ls -1 logs/league_helper/ | wc -l
```
**Expected Result:**
- Folder contains maximum 50 log files
- Oldest timestamped file automatically deleted when 51st file created
- Newest 50 files retained

**Scenario 4.3: Centralized logs/ folder structure**
```bash
# Run multiple scripts with --enable-log-file
python run_league_helper.py --enable-log-file
python run_player_fetcher.py --enable-log-file
python run_accuracy_simulation.py --enable-log-file
ls -la logs/
```
**Expected Result:**
- logs/ folder exists in project root
- Subfolders created: logs/league_helper/, logs/player_data_fetcher/, logs/accuracy_simulation/
- Each subfolder contains script-specific log files
- Folder structure: logs/{script_name}/{script_name}-{TIMESTAMP}.log

**Scenario 4.4: .gitignore integration**
```bash
git status
```
**Expected Result:**
- logs/ folder not shown in untracked files
- .gitignore contains entry: `logs/` (line 71)
- Log files never appear in git status (even after creation)

**Scenario 4.5: File logging OFF by default**
```bash
# Run all 6 scripts WITHOUT --enable-log-file flag
python run_league_helper.py
python run_player_fetcher.py
python run_accuracy_simulation.py
python run_win_rate_simulation.py
python compile_historical_data.py
python run_schedule_fetcher.py
ls logs/
```
**Expected Result:**
- No log files created (logs/ folder may not exist or be empty)
- Console logging still works
- Scripts execute normally

**Scenario 4.6: Concurrent script execution**
```bash
# Run multiple scripts simultaneously with file logging
python run_league_helper.py --enable-log-file &
python run_player_fetcher.py --enable-log-file &
wait
```
**Expected Result:**
- Each script creates its own log file in its own subfolder
- No file conflicts or locking issues
- All log files properly formatted and complete

---

## High-Level Test Categories

**Instructions for Agent:**
- These categories are FLEXIBLE - create specific scenarios during S4 and S8.P2
- Base scenarios on ACTUAL implementation (not assumptions)

---

### Category 1: Error Handling Validation

**What to test:** Epic handles errors gracefully across all features

**Scenario E1: Missing logs/ directory**
```bash
# Delete logs/ folder if exists, run script with --enable-log-file
rm -rf logs/
python run_league_helper.py --enable-log-file
```
**Expected Result:**
- logs/ folder auto-created
- logs/league_helper/ subfolder auto-created
- Log file created successfully
- Script continues normally

**Scenario E2: Permission errors (read-only logs/ folder)**
```bash
# Make logs/ folder read-only
mkdir -p logs/
chmod 444 logs/
python run_league_helper.py --enable-log-file
chmod 755 logs/  # Restore permissions after test
```
**Expected Result:**
- Script handles permission error gracefully (logged to console)
- Script continues with console-only logging
- No crash or unhandled exception

**Scenario E3: Disk space simulation (rotation failure)**
```bash
# Simulate by filling disk or using quota limits (manual test)
# Verify behavior when rotation cannot create new file
```
**Expected Result:**
- Script logs error to console
- Continues with console-only logging
- No data corruption in existing log files

---

### Category 2: Performance Validation

**What to test:** Epic performance acceptable with realistic data

**Scenario P1: Log rotation performance**
```bash
# Generate 500 lines rapidly, measure rotation time
time python run_league_helper.py --enable-log-file
# Check that rotation happens quickly (< 1 second)
```
**Expected Result:**
- Rotation at line 500 completes in < 1 second
- No noticeable performance degradation
- Script continues immediately after rotation

**Scenario P2: Cleanup performance (50 files)**
```bash
# Create 50 existing log files, then trigger cleanup
# Measure time to delete oldest file and create new one
```
**Expected Result:**
- Cleanup completes in < 1 second
- Only oldest file deleted
- No impact on script execution

**Scenario P3: No performance degradation with file logging**
```bash
# Run script with and without --enable-log-file, compare execution time
time python run_accuracy_simulation.py
time python run_accuracy_simulation.py --enable-log-file
```
**Expected Result:**
- Execution time difference < 5%
- File logging adds minimal overhead
- Script remains responsive

---

### Category 3: Edge Cases

**What to test:** Epic handles edge cases correctly

**Scenario EC1: Exactly 500 lines**
```python
# Generate exactly 500 log lines, verify rotation
import logging
logger = logging.getLogger('test')
for i in range(500):
    logger.info(f"Line {i+1}")
```
**Expected Result:**
- First log file contains exactly 500 lines
- Line 501 triggers rotation to new file
- No data loss at boundary

**Scenario EC2: Exactly 50 files**
```bash
# Create exactly 50 log files, then create 51st
# Verify oldest is deleted
```
**Expected Result:**
- Folder maintains exactly 50 files
- 51st file creation triggers deletion of oldest
- Newest 50 files retained

**Scenario EC3: Rapid log generation**
```python
# Generate logs rapidly in tight loop
for i in range(10000):
    logger.debug(f"Rapid log {i}")
```
**Expected Result:**
- All logs written successfully
- Multiple rotations occur correctly (every 500 lines)
- **[UPDATED S8.P2 - Feature 01]:** No timestamp collisions (microsecond precision ensures unique filenames even when rotations occur within same second)
- No race conditions or data corruption
- Each rotated file has unique timestamp with microseconds

**Why updated:** Feature 01 implementation discovered timestamp collision bug during S7.P1 smoke testing. Fix added microsecond precision (strftime('%Y%m%d_%H%M%S_%f')) to doRollover() to prevent duplicate filenames during rapid rotation. This scenario explicitly tests that fix.

**How to verify:**
```bash
ls -1 logs/test_logger/ | grep -E '\d{8}_\d{6}_\d{6}\.log' | sort | uniq -d
```
Expected: Empty output (no duplicate filenames)

**Scenario EC4: Empty logger name**
```python
# Test with empty string logger name
setup_logger(name="", log_to_file=True)
```
**Expected Result:**
- Handles gracefully (Feature 01 trusts callers)
- Creates folder with empty name or uses default
- No crash

**Scenario EC5: Very long logger name**
```python
# Test with extremely long logger name (>255 chars)
setup_logger(name="a" * 300, log_to_file=True)
```
**Expected Result:**
- Handles gracefully (Feature 01 trusts callers)
- May truncate folder name or handle OS limits
- No crash

**Scenario EC6: Rapid rotation within same second (timestamp collision prevention)**

**Added:** S8.P2 (Feature 01 implementation)

**What to test:** Verify that multiple rotations within the same second create unique filenames

**How to test:**
```python
import logging
from utils.LoggingManager import setup_logger

# Create logger that rotates frequently
logger = setup_logger('rapid_test', log_to_file=True)

# Generate 1500 lines rapidly (3 rotations within ~1 second)
for i in range(1500):
    logger.info(f"Rapid message {i}")

# Check for unique filenames
import os
from pathlib import Path
log_dir = Path('logs/rapid_test')
log_files = sorted(log_dir.glob('*.log'))
print(f"Files created: {len(log_files)}")
for f in log_files:
    print(f"  {f.name}")
```

**Expected result:**
- 3 log files created (0-500, 501-1000, 1001-1500)
- Initial file: `rapid_test-{YYYYMMDD_HHMMSS}.log`
- Rotated files: `rapid_test-{YYYYMMDD_HHMMSS_microseconds}.log`
- All filenames are unique (no collisions)
- Microsecond component differs between rotated files
- No overwritten files
- All 1500 lines preserved across 3 files

**Why added:** Feature 01 implementation discovered timestamp collision bug in S7.P1 smoke testing. When rotation happened rapidly (within same second), duplicate filenames caused file overwriting. Fix added microsecond precision (utils/LineBasedRotatingHandler.py:174) to ensure uniqueness. This scenario explicitly validates the fix works.

**Rationale:** This is an epic-level test (not feature unit test) because it validates the core infrastructure contract: "every script can rely on log rotation working correctly even under rapid logging."

---

## Execution Checklist (For S9)

**Agent will check off each scenario as executed during S9 epic smoke testing**

**Part 1: Epic-Level Import Tests**
- [ ] Test 1.1: Import LineBasedRotatingHandler
- [ ] Test 1.2: Import Modified LoggingManager
- [ ] Test 1.3: Instantiate LineBasedRotatingHandler

**Part 2: Epic-Level Entry Point Tests**
- [ ] Test 2.1: league_helper accepts --enable-log-file
- [ ] Test 2.2: player-data-fetcher accepts --enable-log-file
- [ ] Test 2.3: accuracy_sim accepts --enable-log-file
- [ ] Test 2.4: win_rate_sim accepts --enable-log-file
- [ ] Test 2.5: historical_data_compiler accepts --enable-log-file
- [ ] Test 2.6: schedule_fetcher accepts --enable-log-file
- [ ] Test 2.7: Verify default behavior (file logging OFF)

**Part 3: Epic End-to-End Execution Tests**
- [ ] Scenario 3.1: league_helper with file logging enabled
- [ ] Scenario 3.2: player-data-fetcher with file logging enabled
- [ ] Scenario 3.3: accuracy_sim with file logging enabled
- [ ] Scenario 3.4: win_rate_sim with file logging enabled
- [ ] Scenario 3.5: historical_data_compiler with file logging enabled
- [ ] Scenario 3.6: schedule_fetcher with file logging enabled

**Part 4: Cross-Feature Integration Tests**
- [ ] Scenario 4.1: Log rotation at 500 lines
- [ ] Scenario 4.2: Max 50 files cleanup
- [ ] Scenario 4.3: Centralized logs/ folder structure
- [ ] Scenario 4.4: .gitignore integration
- [ ] Scenario 4.5: File logging OFF by default
- [ ] Scenario 4.6: Concurrent script execution

**Category 1: Error Handling Validation**
- [ ] Scenario E1: Missing logs/ directory
- [ ] Scenario E2: Permission errors (read-only logs/ folder)
- [ ] Scenario E3: Disk space simulation (rotation failure)

**Category 2: Performance Validation**
- [ ] Scenario P1: Log rotation performance
- [ ] Scenario P2: Cleanup performance (50 files)
- [ ] Scenario P3: No performance degradation with file logging

**Category 3: Edge Cases**
- [ ] Scenario EC1: Exactly 500 lines
- [ ] Scenario EC2: Exactly 50 files
- [ ] Scenario EC3: Rapid log generation
- [ ] Scenario EC4: Empty logger name
- [ ] Scenario EC5: Very long logger name
- [ ] **[ADDED S8.P2 - Feature 01]** Scenario EC6: Rapid rotation within same second (timestamp collision prevention)

**Overall Status:** {TO BE DETERMINED IN S9}

---

## Notes

**Testing Environment:**

**Prerequisites:**
- Python 3.x installed
- Project dependencies installed: `pip install -r requirements.txt`
- Working directory: Project root (`/home/kai/code/FantasyFootballHelperScriptsRefactored/`)
- Git repository initialized (for .gitignore tests)
- Sufficient disk space for log file generation (minimum 10MB)
- Write permissions in project root (for logs/ folder creation)

**Required Data Files:**
- `data/league_config.csv` (for run_league_helper.py)
- `data/player_stats.csv` (for run_player_fetcher.py, simulations)
- `data/team_rankings.csv` (for run_schedule_fetcher.py)
- `data/league_scoring_rules.csv` (for simulations)

**Environment Configuration:**
- No special environment variables required
- Default logging level: INFO (can test with DEBUG via existing --log-level flags where available)
- File logging: OFF by default, enabled via --enable-log-file flag

**Test Execution Order:**
1. Part 1 (Import Tests) - Verify infrastructure imports work
2. Part 2 (Entry Point Tests) - Verify CLI flags exist
3. Part 3 (E2E Tests) - Verify basic execution with file logging
4. Part 4 (Integration Tests) - Verify rotation, cleanup, folder structure
5. Category 1-3 (Edge Cases) - Verify error handling, performance, edge cases

**Known Issues:**
- None currently (will be updated during S9 if issues discovered)
