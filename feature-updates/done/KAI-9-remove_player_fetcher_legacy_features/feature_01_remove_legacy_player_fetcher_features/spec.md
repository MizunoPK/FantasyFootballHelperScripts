## Feature 01: Remove Legacy Player Fetcher Features - Specification

**Epic:** KAI-9 - remove_player_fetcher_legacy_features
**Created:** 2026-02-13
**Status:** APPROVED (Gate 3 passed - user approved 2026-02-13)

---

## Discovery Context

**This section grounds the feature in epic-level research from DISCOVERY.md.**

### Epic Discovery Summary

The epic Discovery Phase (completed 2026-02-13, user approved) conducted 3 research iterations and 5 Validation Loop rounds, identifying all legacy features for removal and their dependencies.

**Key Findings:**

1. **Config State Clarification (Q0):**
   - User confirmed: Config values NOT yet deleted
   - Deletion IS part of this epic scope
   - Source: `../DISCOVERY.md` Q0 answer

2. **Scope Identified:**
   - 9 config values + 1 dataclass import to delete
   - 9 export methods + 2 helper methods to remove (~700-950 lines)
   - Locked player preservation logic to remove (~100-150 lines)
   - 9 broken imports to fix (5 in exporter, 4 in main)
   - 4 Settings class fields to remove + docstring update
   - 5 test classes to delete
   - Source: `../DISCOVERY.md` Synthesis section

3. **Integration Points Identified:**
   - DataFileManager accepts `None` parameter (no refactoring needed)
   - NFLProjectionsCollector.export_data() needs update (lines 349-354)
   - 2 DataFileManager initialization points (lines 49, 373 in exporter)
   - Source: `../DISCOVERY.md` Research Iteration 2

4. **Zero Regression Requirement:**
   - Position JSON export must work perfectly (6 files: QB, RB, WR, TE, K, DST)
   - Team data export must remain functional (export_teams_to_data)
   - Source: Epic goal and user expectations

**Referenced Files from Discovery:**
- `player-data-fetcher/config.py` - Config values to delete
- `player-data-fetcher/player_data_exporter.py` - Export methods, locked preservation, imports
- `player-data-fetcher/player_data_fetcher_main.py` - Settings class, main integration
- `tests/player-data-fetcher/test_player_data_exporter.py` - Test classes for removal
- `utils/data_file_manager.py` - DataFileManager signature verification

**Epic Validation Loop Results:**
- 5 rounds executed (3 consecutive clean rounds: Rounds 3, 4, 5)
- 5 questions resolved (Q0-Q4)
- User approved findings on 2026-02-13

---

## Feature Requirements

**Requirement Traceability:** All requirements cite source from epic Discovery or user answers

### R1: Config Value Deletion

**Requirement:** Delete 9 legacy config values + 1 dataclass import from config.py

**Source:** Epic Request (DISCOVERY.md lines 397-404, Scope Definition) + User Answer to Q0 (config deletion IS part of epic)

**Details:**
- Line 11: `from dataclasses import dataclass` (import)
- Line 17: `PRESERVE_LOCKED_VALUES`
- Line 25: `OUTPUT_DIRECTORY`
- Lines 26-29: `CREATE_CSV`, `CREATE_JSON`, `CREATE_EXCEL`, `CREATE_CONDENSED_EXCEL`
- Line 30: `CREATE_POSITION_JSON` (config value deleted, functionality preserved)
- Line 31: `DEFAULT_FILE_CAPS`
- Line 78: `EXCEL_POSITION_SHEETS`
- Lines 79-89: `EXPORT_COLUMNS` (11-line list definition)

**Acceptance:** All 22 lines deleted, config.py contains no legacy values

---

### R2: Import Dependency Fixes (Exporter)

**Requirement:** Fix broken imports in player_data_exporter.py by removing references to deleted config values

**Source:** Epic Discovery (DISCOVERY.md lines 68-71, Import Dependencies)

**Details:**
- Delete 5 imports from lines 31-32: `DEFAULT_FILE_CAPS`, `CREATE_POSITION_JSON`, `EXCEL_POSITION_SHEETS`, `EXPORT_COLUMNS`, `PRESERVE_LOCKED_VALUES`
- Keep 7 imports: `POSITION_JSON_OUTPUT`, `CURRENT_NFL_WEEK`, `TEAM_DATA_FOLDER`, `LOAD_DRAFTED_DATA_FROM_FILE`, `DRAFTED_DATA`, `MY_TEAM_NAME`

**Acceptance:** File imports successfully, no ImportError on startup

---

### R3: Import Dependency Fixes (Main)

**Requirement:** Fix broken imports in player_data_fetcher_main.py by removing references to deleted config values

**Source:** Epic Discovery (DISCOVERY.md lines 68-71, Import Dependencies)

**Details:**
- Delete 4 imports from lines 38-44: `OUTPUT_DIRECTORY`, `CREATE_CSV`, `CREATE_JSON`, `CREATE_EXCEL`
- Keep other imports: `NFL_SEASON`, `CURRENT_NFL_WEEK`, `REQUEST_TIMEOUT`, `RATE_LIMIT_DELAY`, `LOGGING_LEVEL`, `LOG_NAME`, `LOGGING_FORMAT`, `ENABLE_HISTORICAL_DATA_SAVE`, `ENABLE_GAME_DATA_FETCH`

**Acceptance:** File imports successfully, no ImportError on startup

---

### R4: Export Method Deletion

**Requirement:** Remove 6 legacy export methods from player_data_exporter.py

**Source:** Epic Discovery (DISCOVERY.md lines 73-75, Export Methods Confirmed) + Research Notes

**Details:**
1. `export_json()` (lines 91-122) - 32 lines
2. `export_csv()` (lines 124-149) - 26 lines
3. `export_excel()` (lines 151-177) - 27 lines
4. `export_all_formats()` (lines 316-345) - 30 lines
5. `export_teams_csv()` (lines 786-816) - 31 lines
6. `export_all_formats_with_teams()` (lines 849-870+) - ~50+ lines

**Acceptance:** All 6 methods deleted, ~196+ lines removed

---

### R5: Helper Method Deletion

**Requirement:** Remove 2 helper methods that are only used by deleted export methods

**Source:** Epic Discovery (DISCOVERY.md lines 161-164, Iteration 3 Finding #1)

**Details:**
1. `_prepare_export_dataframe()` (lines 187-205) - 19 lines, used only by export_csv and export_excel
2. `_write_excel_sheets()` (lines 207-219) - 13 lines, used only by export_excel

**Acceptance:** Both helpers deleted, ~32 lines removed

---

### R6: Locked Player Preservation Removal

**Requirement:** Remove all locked player preservation logic from player_data_exporter.py

**Source:** Epic Discovery (DISCOVERY.md lines 78-83, Locked Player Preservation)

**Details:**
1. Instance variable `existing_locked_values` dict (line 58)
2. Initialization logic (lines 59-60: `if PRESERVE_LOCKED_VALUES:`)
3. `_load_existing_locked_values()` method (lines 225-255) - 31 lines
4. Usage in player conversion (lines 268-269: `if PRESERVE_LOCKED_VALUES and...`)

**Acceptance:** All preservation logic deleted, ~100-120 lines removed

---

### R7: Settings Class Cleanup

**Requirement:** Remove 4 legacy output configuration fields from Settings class in player_data_fetcher_main.py

**Source:** Epic Discovery (DISCOVERY.md lines 127-134, Settings Class Fields Confirmed)

**Details:**
- Delete field definitions (lines 95-98): `output_directory`, `create_csv`, `create_json`, `create_excel`
- Delete docstring references (lines 59-62): Same 4 attributes

**Acceptance:** Settings class contains no legacy fields, docstring updated

---

### R8: DataFileManager Call Updates

**Requirement:** Update 2 DataFileManager initialization calls to pass None instead of DEFAULT_FILE_CAPS

**Source:** Epic Discovery (DISCOVERY.md lines 123-125, DataFileManager Accepts None) + Research Notes

**Details:**
- Location 1 (line 49): Main output_dir manager - Change `DEFAULT_FILE_CAPS` to `None`
- Location 2 (line 373): Position JSON manager - Change `DEFAULT_FILE_CAPS` to `None`

**Acceptance:** Both calls pass None, DataFileManager falls back to shared_config

---

### R9: Integration Point Update

**Requirement:** Update NFLProjectionsCollector.export_data() to call position JSON and team exports directly (remove legacy format calls)

**Source:** Epic Discovery (DISCOVERY.md lines 167-170, Integration Point Identified)

**Details:**
- Remove export_all_formats_with_teams() call (lines 349-354)
- Remove Settings flags usage (create_csv, create_json, create_excel)
- Keep export_position_json_files() call (already present, lines 363-366)
- Add export_teams_to_data() call (currently missing, team export must be preserved)

**Acceptance:** Integration calls only position JSON + team export, no legacy format calls

---

### R10: Test Class Deletion

**Requirement:** Delete 5 test classes for removed export features from test_player_data_exporter.py

**Source:** Epic Discovery (DISCOVERY.md lines 172-185, Iteration 3 Finding #3) + User Answer to Q4 (delete tests for removed features)

**Details:**
1. `TestPrepareExportDataFrame` (line 115) - Tests deleted helper
2. `TestExportJSON` (line 175) - Tests deleted method
3. `TestExportCSV` (line 214) - Tests deleted method
4. `TestExportExcel` (line 260) - Tests deleted method
5. `TestExportAllFormats` (line 283) - Tests deleted method

**Acceptance:** 5 test classes deleted, 6 remaining test classes pass

---

### R11: Preserve Position JSON Export

**Requirement:** Maintain zero regressions in position JSON export functionality (6 files: QB, RB, WR, TE, K, DST)

**Source:** Epic Goal (DISCOVERY.md line 12, Zero Regression Requirement)

**Details:**
- Keep `export_position_json_files()` method unchanged
- Keep `_export_single_position_json()` helper unchanged
- Keep `_prepare_position_json_data()` helper unchanged
- Keep `POSITION_JSON_OUTPUT` and `CURRENT_NFL_WEEK` imports
- Verify 6 position files generate correctly after changes

**Acceptance:** All 6 position JSON files generate with correct data, identical to pre-removal baseline

---

### R12: Preserve Team Data Export

**Requirement:** Maintain team data export functionality (export_teams_to_data method)

**Source:** Derived from Epic Scope (DISCOVERY.md line 435, Out of Scope - team export stays)

**Details:**
- Keep `export_teams_to_data()` method (line 818) unchanged
- Keep team data setters unchanged (set_team_rankings, set_current_week_schedule, etc.)
- Keep `TEAM_DATA_FOLDER` import
- Add explicit call to export_teams_to_data() in integration point (R9)

**Acceptance:** Team data export generates successfully, folder contains correct CSV files

---

### R13: Unit Test Pass Rate

**Requirement:** Maintain 100% unit test pass rate after all removals

**Source:** Epic Success Indicator (EPIC_TICKET.md line 41, 100% test pass rate)

**Details:**
- Delete 5 test classes for removed features (R10)
- Keep 6 test classes for remaining functionality
- Ensure remaining tests pass without modification
- Verify position JSON tests pass (validates R11)

**Acceptance:** All remaining unit tests pass (100% pass rate), zero failures

---

## Acceptance Criteria

**This feature is considered DONE when ALL criteria below are met:**

### AC1: Config File Cleanup

**Criteria:**
- [ ] All 9 config values deleted from config.py (PRESERVE_LOCKED_VALUES, OUTPUT_DIRECTORY, CREATE_CSV, CREATE_JSON, CREATE_EXCEL, CREATE_CONDENSED_EXCEL, CREATE_POSITION_JSON, DEFAULT_FILE_CAPS, EXCEL_POSITION_SHEETS, EXPORT_COLUMNS)
- [ ] Dataclass import deleted (line 11)
- [ ] Total 22 lines removed from config.py
- [ ] No legacy config values remain in file

**Verification:** Grep for deleted value names returns zero matches in config.py

---

### AC2: Import Health (Zero Crashes)

**Criteria:**
- [ ] player_data_exporter.py imports successfully (no ImportError)
- [ ] player_data_fetcher_main.py imports successfully (no ImportError)
- [ ] Both files import only existing config values
- [ ] 9 total imports fixed (5 in exporter, 4 in main)

**Verification:** Run `python player-data-fetcher/player_data_fetcher_main.py --help` (exits cleanly without ImportError)

---

### AC3: Export Method Removal

**Criteria:**
- [ ] 6 export methods deleted: export_json, export_csv, export_excel, export_all_formats, export_teams_csv, export_all_formats_with_teams
- [ ] 2 helper methods deleted: _prepare_export_dataframe, _write_excel_sheets
- [ ] Estimated 228+ lines removed from player_data_exporter.py
- [ ] No references to deleted methods remain in codebase

**Verification:** Grep for method names returns zero matches in implementation files

---

### AC4: Locked Preservation Removal

**Criteria:**
- [ ] existing_locked_values dict removed (line 58)
- [ ] Initialization logic removed (lines 59-60)
- [ ] _load_existing_locked_values method removed (lines 225-255)
- [ ] PRESERVE_LOCKED_VALUES checks removed (lines 268-269)
- [ ] Estimated 100-120 lines removed

**Verification:** Grep for "PRESERVE_LOCKED" and "existing_locked_values" returns zero matches

---

### AC5: Settings Class Cleanup

**Criteria:**
- [ ] 4 field definitions removed (output_directory, create_csv, create_json, create_excel)
- [ ] Docstring updated (4 attribute references removed)
- [ ] Settings class contains no legacy fields
- [ ] No references to deleted fields in NFLProjectionsCollector

**Verification:** Settings class definition clean, no references to deleted fields in player_data_fetcher_main.py

---

### AC6: DataFileManager Updates

**Criteria:**
- [ ] Line 49: DataFileManager initialization passes None (not DEFAULT_FILE_CAPS)
- [ ] Line 373: Position JSON manager initialization passes None
- [ ] Both locations compile and run correctly
- [ ] DataFileManager falls back to shared_config as designed

**Verification:** Both DataFileManager calls use None parameter

---

### AC7: Integration Point Update

**Criteria:**
- [ ] export_all_formats_with_teams() call removed from NFLProjectionsCollector.export_data()
- [ ] Settings flags removed (create_csv, create_json, create_excel)
- [ ] export_position_json_files() call remains (already present)
- [ ] export_teams_to_data() call added (team export preserved)

**Verification:** Integration point calls only position JSON + team export methods

---

### AC8: Test Class Cleanup

**Criteria:**
- [ ] 5 test classes deleted: TestPrepareExportDataFrame, TestExportJSON, TestExportCSV, TestExportExcel, TestExportAllFormats
- [ ] 6 test classes remain: TestDataExporterInit, TestSetTeamData, TestCreateDataFrame, TestGetFantasyPlayers, TestDeprecatedCSVFilesNotCreated, position JSON test
- [ ] Test file structure valid (no syntax errors)

**Verification:** Test file imports successfully, 6 test classes remain

---

### AC9: Position JSON Integrity (Zero Regressions)

**Criteria:**
- [ ] All 6 position JSON files generate successfully (QB, RB, WR, TE, K, DST)
- [ ] Each file contains correct player data (validated against sample run)
- [ ] File format identical to pre-removal baseline
- [ ] No missing players, no incorrect data
- [ ] export_position_json_files() method unchanged

**Verification:** Run player fetcher, verify 6 files generated with expected player counts and data structure

---

### AC10: Team Data Export Preserved

**Criteria:**
- [ ] export_teams_to_data() method unchanged
- [ ] Team data folder generates successfully
- [ ] Team CSV files contain correct historical data
- [ ] Integration point calls team export explicitly (AC7)

**Verification:** Run player fetcher, verify team_data/ folder created with CSV files

---

### AC11: Unit Test Pass Rate (100%)

**Criteria:**
- [ ] All remaining unit tests pass (100% pass rate)
- [ ] Zero test failures
- [ ] Zero test errors
- [ ] Test suite runs to completion
- [ ] Position JSON tests pass (validates AC9)

**Verification:** Run `pytest tests/player-data-fetcher/test_player_data_exporter.py -v` → All tests pass

---

### AC12: Code Quality

**Criteria:**
- [ ] No commented-out code left behind
- [ ] No unused imports
- [ ] No orphaned variables or methods
- [ ] Python syntax valid (no compile errors)

**Verification:** Manual code review + Python import test

---

### AC13: Scope Boundaries Respected

**Criteria:**
- [ ] LOAD_DRAFTED_DATA_FROM_FILE functionality unchanged (out of scope)
- [ ] ESPN API calls unchanged (out of scope)
- [ ] DataFileManager class implementation unchanged (out of scope)
- [ ] Position JSON format unchanged (out of scope)
- [ ] Only deletions performed, no new features added

**Verification:** Grep for LOAD_DRAFTED_DATA_FROM_FILE, verify ESPN API unchanged, verify DataFileManager class file unchanged

---

## Summary Acceptance

**Feature is DONE when:**
- ✅ All 13 acceptance criteria marked complete
- ✅ Manual testing confirms position JSON + team export work
- ✅ Unit tests pass (100% rate)
- ✅ Code review confirms no orphaned code
- ✅ Zero regressions in remaining functionality

---

## User Approval

- [x] User has reviewed acceptance criteria
- [x] User explicitly approved
- **Approved by:** User
- **Approved date:** 2026-02-13
- **Approval status:** APPROVED - Ready for S3/S4/S5

---

## Implementation Notes

{Will be populated during S2.P1-S2.P3 as research and questions are resolved}

**Technical Constraints:**
- Must maintain 100% backward compatibility for position JSON export
- Must pass all remaining unit tests (100% pass rate)
- Zero regressions in position JSON file generation
- Team export functionality must remain unchanged

---

## Open Questions

**See:** `checklist.md` for all open questions requiring user resolution.

Questions will be asked ONE at a time during S2.P3 (Question Resolution phase).

---

## Related Research

{Will reference research documents in epic/research/ folder}

**Epic-Level Research:**
- `../DISCOVERY.md` - Epic discovery findings (user approved)
- `../EPIC_TICKET.md` - Epic acceptance criteria (user validated)

**Feature-Level Research:**
- {To be created during S2.P1 in epic/research/ folder}

---

## Notes

**This spec is DRAFT until Gate 3 (User Approval) is passed.**

The spec will evolve through S2 phases:
- **S2.P1.I1:** Discovery Context Review + Feature-Level Research
- **S2.P1.I2:** Checklist Resolution (answer user questions)
- **S2.P1.I3:** Refinement & Alignment (validate against epic)
- **S2.P2:** Cross-Feature Alignment (N/A for single-feature epic)
- **Gate 3:** User approval of acceptance criteria

After Gate 3, spec becomes authoritative source for S4 (Testing Strategy) and S5 (Implementation Planning).
