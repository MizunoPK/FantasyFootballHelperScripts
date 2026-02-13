## Epic Smoke Test Plan: KAI-9 - remove_player_fetcher_legacy_features

**Created:** 2026-02-13
**Updated:** 2026-02-13 (S3 version - will update in S8.P2)
**Status:** S3 VERSION (concrete test scenarios defined)

---

## Purpose

This file defines epic-level smoke testing executed in S9.P1 before final QC rounds.

**Epic Goal:** Verify all legacy export features are removed, imports fixed, and position JSON + team exports work perfectly with zero regressions.

**Evolution:**
- **S1:** Initial placeholder
- **S3:** Concrete test scenarios defined (this version)
- **S8.P2:** Updated with implementation details after Feature 01 complete
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
pytest tests/player-data-fetcher/test_player_data_exporter.py -v
# Should show: 6 test classes pass, 0 failures, 0 errors
```

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

**Steps:**
1. Run player fetcher: `python player-data-fetcher/run_player_fetcher.py`
2. Check data/player_data/ folder for 6 position files
3. Verify each file contains valid JSON
4. Count players in each file
5. Spot-check player data accuracy

**Expected Results:**
✅ 6 files created: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
✅ All files contain valid JSON (no parse errors)
✅ QB file has ~100+ players
✅ RB file has ~150+ players
✅ WR file has ~200+ players
✅ TE file has ~80+ players
✅ K file has ~50+ players
✅ DST file has ~32 teams
✅ Player data includes: id, name, team, position, fantasy_points, injury_status, drafted_by

**Failure Indicators:**
❌ Fewer than 6 files generated → Export method broken
❌ JSON parse error → Data format broken
❌ Missing players compared to baseline → Filter logic broken
❌ Missing data fields → Data preparation broken

**Commands:**
```bash
python player-data-fetcher/run_player_fetcher.py
ls -lh data/player_data/*.json | wc -l  # Should be 6
python -m json.tool data/player_data/qb_data.json > /dev/null  # Validate JSON
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

**Purpose:** Verify 5 test classes deleted, remaining 6 pass at 100%

**Steps:**
1. Run pytest on test_player_data_exporter.py
2. Count test classes executed
3. Verify 100% pass rate
4. Verify deleted test classes not present

**Expected Results:**
✅ 6 test classes execute (TestDataExporterInit, TestSetTeamData, TestCreateDataFrame, TestGetFantasyPlayers, TestDeprecatedCSVFilesNotCreated, position JSON test)
✅ All tests pass (100% pass rate)
✅ 0 failures, 0 errors
✅ Deleted classes not found: TestPrepareExportDataFrame, TestExportJSON, TestExportCSV, TestExportExcel, TestExportAllFormats

**Failure Indicators:**
❌ Deleted test classes still execute → Test deletion incomplete
❌ Any test failures → Remaining functionality broken
❌ ImportError in tests → Test dependencies broken

**Commands:**
```bash
pytest tests/player-data-fetcher/test_player_data_exporter.py -v
# Verify output shows 6 test classes, 100% pass
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

**Steps:**
1. Read player_data_exporter.py lines 49 and 373
2. Verify both DataFileManager initializations pass None (not DEFAULT_FILE_CAPS)
3. Run player fetcher to verify functionality

**Expected Results:**
✅ Line 49: DataFileManager(str(self.output_dir), None)
✅ Line 373: DataFileManager(str(output_path), None)
✅ No DEFAULT_FILE_CAPS references
✅ Player fetcher runs successfully (DataFileManager accepts None)

**Failure Indicators:**
❌ DEFAULT_FILE_CAPS still passed → Update incomplete
❌ Player fetcher crashes with TypeError → None parameter not handled

**Commands:**
```bash
grep -n "DataFileManager.*DEFAULT_FILE_CAPS" player-data-fetcher/player_data_exporter.py  # Should be 0
grep -n "DataFileManager.*None" player-data-fetcher/player_data_exporter.py  # Should be 2
```

---

## Exit Criteria

**Epic smoke testing PASSES when ALL test scenarios pass:**

- [ ] Test Scenario 1: Import Validation (no ImportError)
- [ ] Test Scenario 2: Config Cleanup (all values deleted)
- [ ] Test Scenario 3: Method Removal (all methods deleted)
- [ ] Test Scenario 4: Position JSON Generation (6 files, correct data)
- [ ] Test Scenario 5: Team Export (32 files, correct data)
- [ ] Test Scenario 6: Unit Tests (6 classes pass, 100% rate)
- [ ] Test Scenario 7: Integration Point (updated correctly)
- [ ] Test Scenario 8: DataFileManager (None parameter works)

**If ANY scenario fails:** Epic smoke testing FAILS, return to debugging protocol

---

## S8.P2 Update Checkpoint

**After Feature 01 implementation complete (S8.P2):**
- [ ] Update test scenarios with actual line numbers post-implementation
- [ ] Add baseline player counts for position JSON validation
- [ ] Document any edge cases discovered during implementation
- [ ] Refine verification commands based on actual file structure

**This version (S3) provides concrete test scenarios. S8.P2 will refine with implementation details.**

---

## Notes

**Version History:**
- **S1:** Initial placeholder (TBD test categories)
- **S3:** Concrete test scenarios defined (8 specific scenarios with commands)
- **S8.P2:** Will update with implementation-specific details
- **S9.P1:** Execution version

**Single-Feature Epic:**
This epic has only 1 feature, so cross-feature integration testing is N/A. All test scenarios validate Feature 01 end-to-end functionality and verify zero regressions.
