## Epic Ticket: remove_player_fetcher_legacy_features

**Created:** 2026-02-13
**Status:** VALIDATED

---

## Description

This epic removes all legacy export formats (CSV, JSON, Excel), locked player preservation, and file caps management from the player data fetcher, streamlining the codebase to support only position-based JSON output. After this epic, the player fetcher will have ~700-950 fewer lines of dead code, zero broken imports, a simplified Settings class, and maintain perfect functionality for the only remaining export format (position JSON: QB, RB, WR, TE, K, DST files).

---

## Acceptance Criteria (Epic-Level)

**The epic is successful when ALL of these are true:**

- [ ] Config file contains NO legacy values (PRESERVE_LOCKED_VALUES, OUTPUT_DIRECTORY, CREATE_CSV/JSON/EXCEL, CREATE_CONDENSED_EXCEL, CREATE_POSITION_JSON config, DEFAULT_FILE_CAPS, EXCEL_POSITION_SHEETS, EXPORT_COLUMNS, dataclass import)
- [ ] player_data_exporter.py contains NO legacy export methods (export_json, export_csv, export_excel, export_all_formats, export_teams_csv, export_all_formats_with_teams, _prepare_export_dataframe, _write_excel_sheets)
- [ ] player_data_exporter.py contains NO locked player preservation logic (_load_existing_locked_values method, existing_locked_values dict, PRESERVE_LOCKED_VALUES checks)
- [ ] All imports are valid (zero ImportError crashes - both files import only existing config values)
- [ ] Settings class contains NO legacy fields (output_directory, create_csv, create_json, create_excel removed from lines 95-98 and docstring)
- [ ] NFLProjectionsCollector.export_data() calls position JSON export directly (no export_all_formats_with_teams call)
- [ ] Position JSON export works perfectly (6 files generated: QB, RB, WR, TE, K, DST with correct data)
- [ ] Team data export still works (export_teams_to_data() untouched and functional)
- [ ] All unit tests pass (100% pass rate, with 5 test classes for removed features deleted)
- [ ] Epic smoke testing passes (position JSON generation, zero regressions)

---

## Success Indicators

**Measurable metrics that show epic succeeded:**

- Lines removed: 700-950 lines of dead code deleted from codebase
- Config cleanup: 9 config values + 1 import removed from config.py
- Import health: 0 broken imports (9 imports fixed across 2 files)
- Test cleanup: 5 test classes deleted (TestPrepareExportDataFrame, TestExportJSON, TestExportCSV, TestExportExcel, TestExportAllFormats)
- Position JSON integrity: 6/6 position files generate correctly with accurate player data
- Zero regressions: Position JSON output identical to pre-epic baseline (same players, same data, same format)
- Test coverage: 100% test pass rate maintained (remaining tests all pass)

---

## Failure Patterns (How We'd Know Epic Failed)

**These symptoms indicate the epic FAILED its goals:**

❌ Import crashes on startup (config values deleted but imports not fixed)
❌ Position JSON files fail to generate (accidentally removed required export methods)
❌ Position JSON files contain wrong data (data preparation logic accidentally modified)
❌ Position JSON files missing players (filtered by removed logic accidentally)
❌ Team data export broken (export_teams_to_data accidentally removed or modified)
❌ Remaining test classes fail (dependencies on removed code not properly cleaned)
❌ DataFileManager crashes (DEFAULT_FILE_CAPS not replaced with None)
❌ NFLProjectionsCollector.export_data() crashes (integration point not updated correctly)

---

## Scope Boundaries

✅ **In Scope (What IS included):**
- Deleting 9 config values + dataclass import from config.py
- Removing 9 export methods + 2 helper methods from player_data_exporter.py
- Removing locked player preservation (method, dict, logic checks)
- Fixing 9 broken imports (5 in exporter, 4 in main)
- Removing 4 Settings class fields + updating docstring
- Updating 2 DataFileManager calls to pass None
- Updating NFLProjectionsCollector.export_data() integration point
- Deleting 5 test classes for removed features
- Keeping position JSON export methods untouched and functional
- Keeping team data export untouched and functional

❌ **Out of Scope (What is NOT included):**
- Changing position JSON file format or structure
- Modifying DataFileManager class implementation (only updating callers)
- Removing team data export functionality (export_teams_to_data stays)
- Changing drafted data loading behavior (LOAD_DRAFTED_DATA_FROM_FILE untouched)
- Modifying ESPN API calls or data fetching logic
- Performance optimization (focus is removal only)
- Adding new export formats or features
- Documentation updates beyond removing references to deleted features

---

## User Validation

**This section filled out by USER - agent presents ticket and asks user to verify/approve**

**User comments:**
No changes requested - epic ticket accurately reflects desired outcomes.

**User approval:** YES
**Approved by:** User
**Approved date:** 2026-02-13

---

## Notes

**Why this ticket matters:**
This ticket serves as the source of truth for epic-level outcomes. It's created BEFORE folder structure to ensure agent understands WHAT the epic achieves (removal of legacy features while maintaining position JSON functionality). During implementation, this ticket will be the reference for validating that all removals are complete and zero regressions occurred.

**Removal Epic Context:**
Unlike feature addition epics, this removal epic has clear success criteria: deleted code should be gone, remaining code should work perfectly, and tests should pass. The epic ticket ensures we don't accidentally remove required functionality (position JSON, team data) while cleaning up legacy features.
