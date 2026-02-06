# Epic Smoke Test Plan: logging_refactoring

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** 2026-02-06 (S1)
**Last Updated:** 2026-02-06 (S1)
**Status:** INITIAL - WILL BE UPDATED IN S4 AND S8.P2

---

## Epic Success Criteria

**The epic is successful if:**

1. All 6 scripts (league_helper, player-data-fetcher, accuracy_sim, win_rate_sim, historical_data_compiler, schedule_fetcher) support --enable-log-file CLI flag with file logging OFF by default
   - Example: `python run_league_helper.py --enable-log-file` creates log file, without flag does not

2. Log files are created in centralized logs/{script_name}/ subfolders
   - Example: logs/league_helper/, logs/accuracy_sim/, logs/player-data-fetcher/, etc.

3. Log files use timestamped naming format: {script_name}-{YYYYMMDD_HHMMSS}.log
   - Example: league_helper-20260206_143522.log

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

---

## Update History

**Track when and why this plan was updated:**

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| 2026-02-06 | S1 | (initial) | Initial plan created | Epic planning based on Discovery findings |

**Current version is informed by:**
- S1: Discovery Phase findings
- S4: {Will be updated with deep dive findings}
- S8.P2 updates: {Will be updated as features complete}

---

## Test Scenarios

**Instructions for Agent (S9):**
- Execute EACH scenario listed below
- Verify ACTUAL DATA VALUES (not just "file exists")
- Document results in S9

**Note:** Detailed scenarios will be added during S4 (Epic Testing Strategy) and refined during S8.P2 (after each feature implementation).

---

### Part 1: Epic-Level Import Tests

**Purpose:** Verify all epic modules can be imported together

{To be expanded in S4 - verify LineBasedRotatingHandler and modified LoggingManager can be imported}

---

### Part 2: Epic-Level Entry Point Tests

**Purpose:** Verify epic-level entry points start correctly

{To be expanded in S4 - verify all 6 scripts accept --enable-log-file flag}

---

### Part 3: Epic End-to-End Execution Tests

**Purpose:** Execute complete epic workflows with REAL data

**Scenario: Complete Epic Workflow (All 6 Scripts with File Logging)**

{To be detailed in S4 and refined in S8.P2}

**Expected Result:**
- All 6 scripts run successfully with --enable-log-file flag
- Log files created in correct folders (logs/{script_name}/)
- Timestamped filenames present
- **DATA VERIFICATION (CRITICAL):**
  - {To be defined in S4 based on deep dive}

---

### Part 4: Cross-Feature Integration Tests

**Purpose:** Test feature interactions and integration points

{To be expanded in S8.P2 as features complete - verify LineBasedRotatingHandler integration works for all scripts}

---

## High-Level Test Categories

**Instructions for Agent:**
- These categories are FLEXIBLE - create specific scenarios during S4 and S8.P2
- Base scenarios on ACTUAL implementation (not assumptions)

---

### Category 1: Error Handling Validation

**What to test:** Epic handles errors gracefully across all features

{Agent will create scenarios in S4/S8.P2 for missing log directories, permission errors, disk space issues}

---

### Category 2: Performance Validation

**What to test:** Epic performance acceptable with realistic data

{Agent will create scenarios in S4/S8.P2 for rotation performance, cleanup performance, no degradation}

---

### Category 3: Edge Cases

**What to test:** Epic handles edge cases correctly

{Agent will create scenarios in S4/S8.P2 for rapid log generation, exactly 50 files, exactly 500 lines, etc.}

---

## Execution Checklist (For S9)

{To be populated during S9 - agent will check off each scenario as executed}

**Part 1: Import Tests**
- [ ] {Scenarios to be defined in S4}

**Part 2: Entry Point Tests**
- [ ] {Scenarios to be defined in S4}

**Part 3: E2E Execution Tests**
- [ ] {Scenarios to be defined in S4}

**Part 4: Cross-Feature Integration Tests**
- [ ] {Scenarios to be defined in S8.P2}

**Overall Status:** {TO BE DETERMINED IN S9}

---

## Notes

**Testing Environment:**
- {To be defined in S4 - required data files, configuration, prerequisites}

**Known Issues:**
- None currently
