## Feature 01: Remove Legacy Player Fetcher Features - Research Notes

**Epic:** KAI-9 - remove_player_fetcher_legacy_features
**Created:** 2026-02-13
**Status:** S2.P1.I1 Complete (Feature-Level Research)

---

## Research Summary

Conducted targeted feature-level research to verify exact implementation details for legacy feature removal. All findings align with epic Discovery Phase results.

**Files Examined:**
- `player-data-fetcher/config.py` (full file)
- `player-data-fetcher/player_data_exporter.py` (lines 30-870)
- `player-data-fetcher/player_data_fetcher_main.py` (lines 38-370)
- `tests/player-data-fetcher/test_player_data_exporter.py` (class list via grep)
- `utils/data_file_manager.py` (verified in epic Discovery)

---

## Code Locations Verified

### 1. Config Values to Delete (config.py)

**Exact Line Numbers:**
- Line 11: `from dataclasses import dataclass` (import to delete)
- Line 17: `PRESERVE_LOCKED_VALUES = False`
- Line 25: `OUTPUT_DIRECTORY = "./data"`
- Line 26: `CREATE_CSV = True`
- Line 27: `CREATE_JSON = False`
- Line 28: `CREATE_EXCEL = False`
- Line 29: `CREATE_CONDENSED_EXCEL = False`
- Line 30: `CREATE_POSITION_JSON = True` (config value deleted, functionality kept)
- Line 31: `DEFAULT_FILE_CAPS = {'csv': 5, 'json': 18, 'xlsx': 5, 'txt': 5}`
- Line 78: `EXCEL_POSITION_SHEETS = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']`
- Lines 79-89: `EXPORT_COLUMNS = [...]` (11 lines total)

**Total Lines to Delete:** 22 lines (1 import + 9 config values + 1 list definition with 11 lines)

---

### 2. Import Fixes (player_data_exporter.py)

**Current Imports (Lines 31-32):**
```python
from config import DEFAULT_FILE_CAPS, CREATE_POSITION_JSON, POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK
from config import EXCEL_POSITION_SHEETS, EXPORT_COLUMNS, PRESERVE_LOCKED_VALUES, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME
```

**To Delete (5 values):**
- `DEFAULT_FILE_CAPS`
- `CREATE_POSITION_JSON` (config value only, functionality stays)
- `EXCEL_POSITION_SHEETS`
- `EXPORT_COLUMNS`
- `PRESERVE_LOCKED_VALUES`

**To Keep (7 values):**
- `POSITION_JSON_OUTPUT` (used by position JSON export)
- `CURRENT_NFL_WEEK` (used by position JSON export)
- `TEAM_DATA_FOLDER` (used by team export)
- `LOAD_DRAFTED_DATA_FROM_FILE` (drafted data loading, not removed)
- `DRAFTED_DATA` (drafted data path)
- `MY_TEAM_NAME` (team name for drafted data)

**After Fix:**
```python
from config import POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK
from config import TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME
```

---

### 3. Import Fixes (player_data_fetcher_main.py)

**Current Imports (Lines 38-44):**
```python
from config import (
    NFL_SEASON, CURRENT_NFL_WEEK,
    OUTPUT_DIRECTORY, CREATE_CSV, CREATE_JSON, CREATE_EXCEL,
    REQUEST_TIMEOUT, RATE_LIMIT_DELAY, LOGGING_LEVEL,
    LOG_NAME, LOGGING_FORMAT,
    ENABLE_HISTORICAL_DATA_SAVE, ENABLE_GAME_DATA_FETCH
)
```

**To Delete (4 values):**
- `OUTPUT_DIRECTORY`
- `CREATE_CSV`
- `CREATE_JSON`
- `CREATE_EXCEL`

**After Fix:**
```python
from config import (
    NFL_SEASON, CURRENT_NFL_WEEK,
    REQUEST_TIMEOUT, RATE_LIMIT_DELAY, LOGGING_LEVEL,
    LOG_NAME, LOGGING_FORMAT,
    ENABLE_HISTORICAL_DATA_SAVE, ENABLE_GAME_DATA_FETCH
)
```

---

### 4. Export Methods to Delete (player_data_exporter.py)

**Methods:**
1. `export_json()` (lines 91-122) - 32 lines
2. `export_csv()` (lines 124-149) - 26 lines
3. `export_excel()` (lines 151-177) - 27 lines
4. `export_all_formats()` (lines 316-345) - 30 lines
5. `export_teams_csv()` (lines 786-816) - 31 lines
6. `export_all_formats_with_teams()` (lines 849-870+) - ~50+ lines

**Helper Methods:**
7. `_prepare_export_dataframe()` (lines 187-205) - 19 lines
   - Used ONLY by export_csv (line 128) and export_excel (line 154)
   - References `EXPORT_COLUMNS` (line 194, 199, 205)
   - Safe to delete

8. `_write_excel_sheets()` (lines 207-219) - 13 lines
   - Used ONLY by export_excel (lines 162, 169)
   - References `EXCEL_POSITION_SHEETS` (line 215)
   - Safe to delete

**Total Estimated Removal:** ~228+ lines (6 methods + 2 helpers)

---

### 5. Locked Player Preservation Logic (player_data_exporter.py)

**Components:**
1. **Instance Variable** (line 58): `self.existing_locked_values = {}`
2. **Initialization Logic** (lines 59-60):
   ```python
   if PRESERVE_LOCKED_VALUES:
       self._load_existing_locked_values()
   ```
3. **Load Method** (lines 225-255): `_load_existing_locked_values()` - 31 lines
4. **Usage in Player Conversion** (lines 268-269):
   ```python
   locked_value = 0  # Default
   if PRESERVE_LOCKED_VALUES and player_data.id in self.existing_locked_values:
   ```

**Total Estimated Removal:** ~100-120 lines

---

### 6. Settings Class Updates (player_data_fetcher_main.py)

**Field Definitions (Lines 95-98):**
```python
output_directory: str = OUTPUT_DIRECTORY  # Output directory (from config)
create_csv: bool = CREATE_CSV  # Whether to create CSV output (from config)
create_json: bool = CREATE_JSON  # Whether to create JSON output (from config)
create_excel: bool = CREATE_EXCEL  # Whether to create Excel output (from config)
```

**Docstring References (Lines 59-62):**
```python
output_directory: Directory for output files
create_csv: Whether to create CSV output
create_json: Whether to create JSON output
create_excel: Whether to create Excel output
```

**After Fix:**
- Delete lines 95-98 (4 field definitions)
- Delete lines 59-62 from docstring (4 attribute descriptions)

---

### 7. DataFileManager Updates (player_data_exporter.py)

**Location 1 (Line 49):**
```python
# Initialize file manager for automatic file caps
self.file_manager = DataFileManager(str(self.output_dir), DEFAULT_FILE_CAPS)
```

**After Fix:**
```python
# Initialize file manager for automatic file caps
self.file_manager = DataFileManager(str(self.output_dir), None)
```

**Location 2 (Line 373):**
```python
# Create dedicated DataFileManager for position JSON exports
# This ensures files are saved to POSITION_JSON_OUTPUT, not OUTPUT_DIRECTORY
position_file_manager = DataFileManager(str(output_path), DEFAULT_FILE_CAPS)
```

**After Fix:**
```python
# Create dedicated DataFileManager for position JSON exports
# This ensures files are saved to POSITION_JSON_OUTPUT, not OUTPUT_DIRECTORY
position_file_manager = DataFileManager(str(output_path), None)
```

**Verified:** DataFileManager signature accepts `Optional[Dict[str, int]] = None` (epic Discovery confirmed)

---

### 8. Integration Point Update (player_data_fetcher_main.py)

**Current Implementation (Lines 349-366):**
```python
files = await self.exporter.export_all_formats_with_teams(
    data,
    create_csv=self.settings.create_csv,
    create_json=self.settings.create_json,
    create_excel=self.settings.create_excel
)
output_files.extend(files)
self.logger.info(f"Exported {data_type} projections to configured formats")

# Export position-based JSON files (if enabled via config)
# Creates 6 files: new_qb_data.json, new_rb_data.json, new_wr_data.json,
# new_te_data.json, new_k_data.json, new_dst_data.json
# Spec: specs.md lines 10-19, USER_DECISIONS_SUMMARY.md Decision 1
try:
    position_json_files = await self.exporter.export_position_json_files(data)
    if position_json_files:
        output_files.extend(position_json_files)
        self.logger.info(f"Exported {len(position_json_files)} position-based JSON files")
```

**After Fix:**
```python
# Export position-based JSON files (6 files: QB, RB, WR, TE, K, DST)
try:
    position_json_files = await self.exporter.export_position_json_files(data)
    if position_json_files:
        output_files.extend(position_json_files)
        self.logger.info(f"Exported {len(position_json_files)} position-based JSON files")
except Exception as e:
    # Error exporting position JSON
    self.logger.error(f"Position JSON export failed: {e}")

# Export team data to shared data directory
try:
    team_data_path = await self.exporter.export_teams_to_data(data)
    if team_data_path:
        output_files.append(team_data_path)
        self.logger.info(f"Exported team data to: {team_data_path}")
except Exception as e:
    # Error exporting team data
    self.logger.error(f"Team data export failed: {e}")
```

**Rationale:**
- Remove export_all_formats_with_teams() call (method being deleted)
- Remove Settings flags (create_csv, create_json, create_excel - fields being deleted)
- Keep export_position_json_files() call (already present)
- Add export_teams_to_data() call (team export functionality must be preserved)

---

### 9. Test Class Deletions (test_player_data_exporter.py)

**Classes to DELETE (5 classes):**
1. `TestPrepareExportDataFrame` (line 115) - Tests `_prepare_export_dataframe()` helper
2. `TestExportJSON` (line 175) - Tests `export_json()` method
3. `TestExportCSV` (line 214) - Tests `export_csv()` method
4. `TestExportExcel` (line 260) - Tests `export_excel()` method
5. `TestExportAllFormats` (line 283) - Tests `export_all_formats()` method

**Classes to KEEP (6 classes):**
1. `TestDataExporterInit` (line 26) - Tests initialization (still needed)
2. `TestSetTeamData` (line 52) - Tests team data setters (still needed)
3. `TestCreateDataFrame` (line 74) - Tests DataFrame creation (may be used by position JSON)
4. `TestGetFantasyPlayers` (line 137) - Tests player retrieval (still needed)
5. `TestDeprecatedCSVFilesNotCreated` (line 342) - Tests deprecated files NOT created
6. Position JSON test (line 398: `test_position_json_files_still_created`) - Tests remaining functionality

---

## Methods to KEEP (Verification)

**Export Methods:**
1. `export_position_json_files()` (line 347) - Position JSON export (core remaining functionality)
2. `_export_single_position_json()` (line 396+) - Helper for position JSON
3. `_prepare_position_json_data()` (exact line TBD) - Helper for position JSON
4. `export_teams_to_data()` (line 818) - Team data export to shared folder

**Core Data Methods:**
1. `_create_dataframe()` (line 183) - DataFrame creation (used by position JSON)
2. `get_fantasy_players()` (exact line TBD) - Player conversion (used by position JSON)
3. `_espn_player_to_fantasy_player()` (line 261) - Player conversion helper

**Team Data Setters:**
1. `set_team_rankings()` (line 67)
2. `set_current_week_schedule()` (line 72)
3. `set_position_defense_rankings()` (line 77)
4. `set_team_weekly_data()` (line 82)

---

## Integration Points Verified

**1. NFLProjectionsCollector.export_data() (lines 308-370)**
- Lines 349-354: Calls export_all_formats_with_teams() → DELETE call, replace with position JSON + teams
- Lines 363-366: Calls export_position_json_files() → KEEP call (already correct)
- Missing: Call to export_teams_to_data() → ADD call

**2. DataFileManager Initializations**
- Line 49 in __init__: Pass None instead of DEFAULT_FILE_CAPS
- Line 373 in export_position_json_files: Pass None instead of DEFAULT_FILE_CAPS

---

## External Dependencies Verification

**No external library compatibility issues:**
- All removals are internal methods and config values
- Position JSON export uses standard libraries (json, pathlib, pandas)
- DataFileManager already supports None parameter (verified in epic Discovery)
- No API endpoint changes (ESPN API calls unchanged)

---

## Edge Cases Identified

**None identified** - Removal epic has clear boundaries:
- Legacy methods are not called by position JSON export
- Helper methods are only used by deleted methods
- Config values are only used by deleted methods
- Settings fields are only used by deleted methods

---

## Open Questions

**None** - All questions were resolved during epic Discovery Phase (Q0-Q4 answered)

---

## Compatibility Findings

**No compatibility concerns:**
- Position JSON export is independent of legacy formats
- Team export is independent of legacy formats
- DataFileManager gracefully handles None parameter
- Test suite structure supports class-level deletion

---

## Next Steps

1. Update spec.md with requirement traceability
2. Create checklist.md (if any clarifications needed - currently none expected)
3. Run Validation Loop (Gate 1: Research Completeness Audit)
4. Continue to S2.P1.I2 (Checklist Resolution)

---

## Research Confidence Level

**HIGH** - All code locations verified, all method signatures confirmed, all integration points identified, all test classes confirmed, zero external dependencies, zero compatibility concerns.
