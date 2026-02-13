## Epic Smoke Test Plan: KAI-9 - remove_player_fetcher_legacy_features

**Created:** 2026-02-13
**Updated:** 2026-02-13 (S8.P2 - updated with actual implementation details after Feature 01 complete)
**Status:** S8.P2 VERSION (refined with implementation-verified details)

---

## Purpose

This file defines epic-level smoke testing executed in S9.P1 before final QC rounds.

**Epic Goal:** Verify all legacy export features are removed, imports fixed, and position JSON + team exports work perfectly with zero regressions.

**Evolution:**
- **S1:** Initial placeholder
- **S3:** Concrete test scenarios defined
- **S8.P2:** Updated with actual implementation details (this version)
- **S9.P1:** Executed as final validation

---

## Epic Success Criteria

**The epic is successful when ALL criteria below are met:**

### Criterion 1: Zero Import Errors (Import Health)
✅ **MEASURABLE:** `python player-data-fetcher/player_data_fetcher_main.py --help` exits with code 0, no ImportError

**Verification Command:**
```bash
python player-data-fetcher/player_data_fetcher_main.py --help
echo "Exit code: $?"  # Should be 0
```

---

### Criterion 2: Config File Cleanup Complete
✅ **MEASURABLE:** All 9 legacy config values + dataclass import removed (22 lines total)

**Verification Commands:**
```bash
# Should return 0 matches for each deleted value
grep -n "PRESERVE_LOCKED_VALUES\|OUTPUT_DIRECTORY\|CREATE_CSV\|CREATE_JSON\|CREATE_EXCEL\|CREATE_CONDENSED_EXCEL\|CREATE_POSITION_JSON\|DEFAULT_FILE_CAPS\|EXCEL_POSITION_SHEETS\|EXPORT_COLUMNS" player-data-fetcher/config.py | wc -l

# Should return 0 for dataclass import
grep -n "from dataclasses import dataclass" player-data-fetcher/config.py | wc -l
```

---

### Criterion 3: Export Methods Removed
✅ **MEASURABLE:** 6 export methods + 2 helpers deleted (grep returns 0 matches)

**Verification Commands:**
```bash
# Should return 0 for each deleted method
grep -n "def export_json\|def export_csv\|def export_excel\|def export_all_formats\|def export_teams_csv\|def export_all_formats_with_teams\|def _prepare_export_dataframe\|def _write_excel_sheets" player-data-fetcher/player_data_exporter.py | wc -l
```

---

### Criterion 4: Locked Preservation Removed
✅ **MEASURABLE:** All preservation logic deleted (grep returns 0 matches)

**Verification Commands:**
```bash
# Should return 0
grep -n "PRESERVE_LOCKED\|existing_locked_values\|_load_existing_locked_values" player-data-fetcher/player_data_exporter.py | wc -l
```

---

### Criterion 5: Settings Class Cleanup
✅ **MEASURABLE:** 4 legacy fields removed from Settings class

**Verification Commands:**
```bash
# Should return 0 for each deleted field
grep -n "output_directory:\|create_csv:\|create_json:\|create_excel:" player-data-fetcher/player_data_fetcher_main.py | wc -l
```

---

### Criterion 6: Position JSON Files Generate Successfully
✅ **MEASURABLE:** 6 position JSON files created (QB, RB, WR, TE, K, DST) with valid JSON

**Verification:** Run player fetcher, check for 6 files in data/player_data/

---

### Criterion 7: Position JSON Data Integrity (Zero Regressions)
✅ **MEASURABLE:** Position JSON files contain correct player data (validated against baseline)

**Verification:** Compare generated files to pre-removal baseline (same players, same data structure)

---

### Criterion 8: Team Data Export Preserved
✅ **MEASURABLE:** Team data folder created with CSV files

**Verification:** Check for data/team_data/ folder with 32 team CSV files

---

### Criterion 9: Unit Test Pass Rate 100%
✅ **MEASURABLE:** All remaining unit tests pass with zero failures

**Verification Command:**
```bash
# Exporter-specific tests: 5 classes, 10 tests
pytest tests/player-data-fetcher/test_player_data_exporter.py -v

# Full player-data-fetcher suite: 310 tests
pytest tests/player-data-fetcher/ -v
```

**[UPDATED S8.P2]** Actual implementation confirmed: 5 test classes (not 6), 10 tests total in exporter file. Full player-data-fetcher suite: 310 tests passing.

---

## Epic-Level Integration Points

**For single-feature epic:** No cross-feature integration (only 1 feature)

**Internal Integration Points (within Feature 01):**

### Integration Point 1: NFLProjectionsCollector → DataExporter
**Type:** Method call integration
**Flow:**
1. NFLProjectionsCollector.export_data() calls DataExporter methods
2. Must call export_position_json_files() for position data
3. Must call export_teams_to_data() for team data
4. Must NOT call export_all_formats_with_teams() (deleted)

**Test Need:** Verify integration point updated correctly (removed legacy calls, added team call)

---

### Integration Point 2: DataExporter → DataFileManager
**Type:** Utility dependency
**Flow:**
1. DataExporter creates DataFileManager instances (2 locations)
2. Must pass None for file_caps parameter (not DEFAULT_FILE_CAPS)
3. DataFileManager falls back to shared_config when None

**[UPDATED S8.P2]** Actual locations verified:
- player_data_exporter.py:48 (DataExporter.__init__)
- player_data_exporter.py:173 (export_position_json_files, dedicated position file manager)

**Test Need:** Verify DataFileManager initialization works with None parameter

---

## Specific Test Scenarios

### Test Scenario 1: Import Validation

**Purpose:** Verify all import fixes applied correctly, no ImportError crashes

**Steps:**
1. Run `python player-data-fetcher/player_data_fetcher_main.py --help`
2. Observe output

**Expected Results:**
✅ Command exits cleanly with help message
✅ No ImportError or ModuleNotFoundError
✅ Exit code 0

**Failure Indicators:**
❌ ImportError: cannot import name 'DEFAULT_FILE_CAPS' → Import fix incomplete
❌ ImportError: cannot import name 'CREATE_CSV' → Import fix incomplete
❌ Any other ImportError → Configuration error

**Command:**
```bash
python player-data-fetcher/player_data_fetcher_main.py --help
```

---

### Test Scenario 2: Config File Cleanup Verification

**Purpose:** Verify all legacy config values deleted, no orphaned references

**Steps:**
1. Grep for each deleted config value in config.py
2. Count matches
3. Grep for dataclass import

**Expected Results:**
✅ PRESERVE_LOCKED_VALUES: 0 matches
✅ OUTPUT_DIRECTORY: 0 matches
✅ CREATE_CSV/JSON/EXCEL/CONDENSED_EXCEL: 0 matches
✅ CREATE_POSITION_JSON: 0 matches
✅ DEFAULT_FILE_CAPS: 0 matches
✅ EXCEL_POSITION_SHEETS: 0 matches
✅ EXPORT_COLUMNS: 0 matches
✅ dataclass import: 0 matches

**Failure Indicators:**
❌ Any value still present in config.py → Deletion incomplete

**Commands:**
```bash
grep -n "PRESERVE_LOCKED_VALUES" player-data-fetcher/config.py
grep -n "OUTPUT_DIRECTORY" player-data-fetcher/config.py
grep -n "CREATE_CSV\|CREATE_JSON\|CREATE_EXCEL" player-data-fetcher/config.py
grep -n "DEFAULT_FILE_CAPS" player-data-fetcher/config.py
grep -n "EXCEL_POSITION_SHEETS\|EXPORT_COLUMNS" player-data-fetcher/config.py
grep -n "from dataclasses import dataclass" player-data-fetcher/config.py
```

---

### Test Scenario 3: Export Method Removal Verification

**Purpose:** Verify all 6 export methods + 2 helpers deleted

**Steps:**
1. Grep for each method definition in player_data_exporter.py
2. Count matches

**Expected Results:**
✅ export_json(): 0 matches
✅ export_csv(): 0 matches
✅ export_excel(): 0 matches
✅ export_all_formats(): 0 matches
✅ export_teams_csv(): 0 matches
✅ export_all_formats_with_teams(): 0 matches
✅ _prepare_export_dataframe(): 0 matches
✅ _write_excel_sheets(): 0 matches

**Failure Indicators:**
❌ Any method still present → Deletion incomplete

**Commands:**
```bash
grep -n "def export_json" player-data-fetcher/player_data_exporter.py
grep -n "def export_csv" player-data-fetcher/player_data_exporter.py
grep -n "def export_excel" player-data-fetcher/player_data_exporter.py
grep -n "def export_all_formats" player-data-fetcher/player_data_exporter.py
grep -n "def export_teams_csv" player-data-fetcher/player_data_exporter.py
grep -n "def export_all_formats_with_teams" player-data-fetcher/player_data_exporter.py
grep -n "def _prepare_export_dataframe" player-data-fetcher/player_data_exporter.py
grep -n "def _write_excel_sheets" player-data-fetcher/player_data_exporter.py
```

---

### Test Scenario 4: Position JSON Generation (End-to-End)

**Purpose:** Verify position JSON export works perfectly with zero regressions

**[UPDATED S8.P2]** Note: Full E2E requires ESPN API credentials and network access. For S9, validate using existing data/player_data/ files from last successful run and unit test coverage.

**Steps:**
1. Verify existing data/player_data/ folder contains 6 position files (from last run)
2. Verify each file contains valid JSON with correct structure
3. Count players in each file
4. Spot-check player data fields match expected schema
5. Run unit test: TestPositionJSONExport::test_position_json_files_created

**Expected Results:**
✅ 6 files present: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
✅ All files contain valid JSON (no parse errors)
✅ Each file has root key matching `{position}_data` (e.g., `qb_data`)
✅ Player objects include: id, name, team, position, bye_week, injury_status, drafted_by, locked, average_draft_position, player_rating, projected_points (17-element array), actual_points (17-element array)
✅ Position-specific stat arrays present (passing/rushing/receiving for QB, etc.)
✅ Unit test passes confirming export_position_json_files() works correctly

**Failure Indicators:**
❌ Fewer than 6 files → Export method broken
❌ JSON parse error → Data format broken
❌ Missing root key or wrong key name → Structure broken
❌ Missing fields in player objects → Data preparation broken

**Commands:**
```bash
dir data\player_data\*.json  # Should list 6 files
python -m json.tool data/player_data/qb_data.json > NUL  # Validate JSON (Windows)
pytest tests/player-data-fetcher/test_player_data_exporter.py::TestPositionJSONExport -v
```

---

### Test Scenario 5: Team Data Export Verification

**Purpose:** Verify team export functionality preserved

**Steps:**
1. Run player fetcher (same as Test Scenario 4)
2. Check data/team_data/ folder for CSV files
3. Verify 32 team files created (one per NFL team)
4. Spot-check file contents

**Expected Results:**
✅ data/team_data/ folder exists
✅ 32 CSV files created (one per team)
✅ Files contain historical team data
✅ CSV format valid (no parse errors)

**Failure Indicators:**
❌ team_data/ folder not created → export_teams_to_data() not called
❌ Fewer than 32 files → Team export broken
❌ CSV parse error → Data format broken

**Commands:**
```bash
ls data/team_data/*.csv | wc -l  # Should be 32
head -n 5 data/team_data/ARI.csv  # Spot-check format
```

---

### Test Scenario 6: Unit Test Cleanup and Pass Rate

**Purpose:** Verify 5 test classes deleted, remaining classes pass at 100%

**[UPDATED S8.P2]** Actual implementation verified: 5 remaining test classes (not 6), 10 tests total.

**Steps:**
1. Run pytest on test_player_data_exporter.py with -v flag
2. Count test classes and tests executed
3. Verify 100% pass rate
4. Verify deleted test classes not present
5. Run full player-data-fetcher test suite for broader regression check

**Expected Results:**
✅ 5 test classes execute:
   - TestDataExporterInit (3 tests)
   - TestSetTeamData (2 tests)
   - TestCreateDataFrame (2 tests)
   - TestGetFantasyPlayers (2 tests)
   - TestPositionJSONExport (1 test)
✅ 10/10 tests pass (100% pass rate)
✅ 0 failures, 0 errors
✅ Deleted classes not found: TestPrepareExportDataFrame, TestExportJSON, TestExportCSV, TestExportExcel, TestExportAllFormats
✅ Full suite: 310/310 tests pass

**Failure Indicators:**
❌ Deleted test classes still execute → Test deletion incomplete
❌ Any test failures → Remaining functionality broken
❌ ImportError in tests → Test dependencies broken
❌ Full suite failures in player-data-fetcher/ → Regression detected

**Commands:**
```bash
pytest tests/player-data-fetcher/test_player_data_exporter.py -v
# Verify: 5 classes, 10 tests, 100% pass

pytest tests/player-data-fetcher/ -q
# Verify: 310 passed
```

---

### Test Scenario 7: Integration Point Validation

**Purpose:** Verify NFLProjectionsCollector.export_data() updated correctly

**Steps:**
1. Read player_data_fetcher_main.py lines 308-370
2. Verify export_all_formats_with_teams() call removed
3. Verify export_position_json_files() call present
4. Verify export_teams_to_data() call added
5. Verify Settings flags (create_csv, create_json, create_excel) not used

**Expected Results:**
✅ export_all_formats_with_teams(): 0 calls (method deleted)
✅ export_position_json_files(): 1 call (existing, preserved)
✅ export_teams_to_data(): 1 call (newly added)
✅ Settings.create_csv/json/excel: 0 references (fields deleted)

**Failure Indicators:**
❌ export_all_formats_with_teams() still called → Integration update incomplete
❌ export_teams_to_data() not called → Team export broken
❌ Settings flags still referenced → Settings cleanup incomplete

**Commands:**
```bash
grep -n "export_all_formats_with_teams" player-data-fetcher/player_data_fetcher_main.py
grep -n "export_position_json_files" player-data-fetcher/player_data_fetcher_main.py
grep -n "export_teams_to_data" player-data-fetcher/player_data_fetcher_main.py
grep -n "create_csv\|create_json\|create_excel" player-data-fetcher/player_data_fetcher_main.py
```

---

### Test Scenario 8: DataFileManager None Parameter Verification

**Purpose:** Verify DataFileManager calls updated to pass None

**[UPDATED S8.P2]** Actual line numbers from implementation:
- Line 48: DataExporter.__init__ (class-level file manager)
- Line 173: export_position_json_files (position-specific file manager)

**Steps:**
1. Read player_data_exporter.py lines 48 and 173
2. Verify both DataFileManager initializations pass None (not DEFAULT_FILE_CAPS)
3. Verify no remaining references to DEFAULT_FILE_CAPS anywhere in codebase

**Expected Results:**
✅ Line 48: DataFileManager(str(self.output_dir), None)
✅ Line 173: DataFileManager(str(output_path), None)
✅ No DEFAULT_FILE_CAPS references in player-data-fetcher/ directory
✅ Unit tests pass (DataFileManager accepts None without error)

**Failure Indicators:**
❌ DEFAULT_FILE_CAPS still passed → Update incomplete
❌ Tests crash with TypeError → None parameter not handled

**Commands:**
```bash
grep -rn "DEFAULT_FILE_CAPS" player-data-fetcher/  # Should be 0 matches
grep -n "DataFileManager.*None" player-data-fetcher/player_data_exporter.py  # Should be 2 matches
```

---

## Exit Criteria

**Epic smoke testing PASSES when ALL test scenarios pass:**

- [ ] Test Scenario 1: Import Validation (no ImportError)
- [ ] Test Scenario 2: Config Cleanup (all values deleted)
- [ ] Test Scenario 3: Method Removal (all methods deleted)
- [ ] Test Scenario 4: Position JSON Generation (6 files, correct data)
- [ ] Test Scenario 5: Team Export (32 files, correct data)
- [ ] Test Scenario 6: Unit Tests (5 classes, 10 tests pass, 100% rate; full suite 310 pass)
- [ ] Test Scenario 7: Integration Point (updated correctly)
- [ ] Test Scenario 8: DataFileManager (None parameter works)

**If ANY scenario fails:** Epic smoke testing FAILS, return to debugging protocol

---

## S8.P2 Update Checkpoint

**After Feature 01 implementation complete (S8.P2): ALL DONE**
- [x] Update test scenarios with actual line numbers post-implementation
- [x] Correct test class/count based on actual implementation (5 classes, 10 tests)
- [x] Document edge cases discovered during S7.P2 validation
- [x] Refine verification commands for Windows environment
- [x] Add E2E note about API dependency for Scenario 4
- [x] Update DataFileManager line numbers (48 and 173, not 49 and 373)

---

## Edge Cases Discovered During Implementation (S7.P2)

**[ADDED S8.P2]** 5 issues found during S7.P2 validation rounds:

1. **NFLProjectionsCollector.__init__ referenced deleted settings.output_directory** - Fixed by updating initialization to not reference deleted Settings fields
2. **test_player_data_fetcher_main.py had 19 test failures** - Tests referenced deleted Settings fields; updated fixtures and mocks
3. **test_run_player_fetcher.py had 10 test failures** - Tests referenced deleted config values; updated imports and assertions
4. **test_config.py had 3 test failures** - Tests validated deleted config values; removed obsolete test cases
5. **test_export_data_basic mocked deleted methods** - Test mock setup referenced export_all_formats_with_teams; updated to mock preserved methods

**Root cause pattern:** Comprehensive grep was not performed across tests/ directory after config/method deletions. All issues caught by S7.P2 validation loop.

---

## Notes

**Version History:**
- **S1:** Initial placeholder (TBD test categories)
- **S3:** Concrete test scenarios defined (8 specific scenarios with commands)
- **S8.P2:** Updated with actual implementation details, corrected line numbers, test counts, Windows commands, edge cases from S7.P2

**Update History:**

| Date | Stage | Changes Made | Reason |
|------|-------|--------------|--------|
| 2026-02-13 | S1 | Initial creation | Epic planning |
| 2026-02-13 | S3 | 8 concrete test scenarios with commands | Cross-feature sanity check |
| 2026-02-13 | S8.P2 | Corrected test counts (5 classes/10 tests), updated line numbers (48/173), added edge cases from S7.P2, refined Scenario 4 for API dependency, updated commands for Windows | Feature 01 implementation complete, actual code reviewed |

**Single-Feature Epic:**
This epic has only 1 feature, so cross-feature integration testing is N/A. All test scenarios validate Feature 01 end-to-end functionality and verify zero regressions.
