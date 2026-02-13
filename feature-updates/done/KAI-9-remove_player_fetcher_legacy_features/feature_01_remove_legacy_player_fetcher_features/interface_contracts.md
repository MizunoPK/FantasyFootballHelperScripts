## Feature 01: Interface Contracts

**Purpose:** Document EXACT signatures of all external interfaces used in this feature

**Created:** 2026-02-13 (S6 Step 2 - Interface Verification Protocol)

**Source:** All signatures verified from actual source code (NOT from memory or assumptions)

---

## External Dependencies

### 1. DataFileManager Class

**File:** `utils/data_file_manager.py`

**Constructor Signature (lines 41-56):**
```python
def __init__(self, data_folder_path: str, file_caps: Optional[Dict[str, int]] = None):
    """
    Initialize DataFileManager for a specific data folder.

    Args:
        data_folder_path: Path to the data folder to manage
        file_caps: Dictionary of file type caps (e.g., {'csv': 5, 'json': 5})
                  If None, will try to import from shared_config
    """
    self.data_folder = Path(data_folder_path)

    # Set default caps if not provided
    if file_caps is None:
        file_caps = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}

    self.file_caps = file_caps
```

**Verification:**
- ✅ Accepts `None` as `file_caps` parameter (lines 52-54)
- ✅ Has fallback logic when None provided (default caps dict)
- ✅ Task 8 assumption VERIFIED: Can pass None without refactoring

---

### 2. DataExporter.export_position_json_files Method

**File:** `player-data-fetcher/player_data_exporter.py`

**Method Signature (lines 347-361):**
```python
async def export_position_json_files(self, data: ProjectionData) -> List[str]:
    """
    Export position-based JSON files concurrently.

    Creates 6 JSON files (one per position: QB, RB, WR, TE, K, DST)
    in POSITION_JSON_OUTPUT folder.

    Spec: specs.md lines 14-19, USER_DECISIONS_SUMMARY.md Decision 1

    Args:
        data: ProjectionData containing player data

    Returns:
        List of file paths created (empty if CREATE_POSITION_JSON=False)
    """
```

**Verification:**
- ✅ Takes single parameter: `ProjectionData`
- ✅ Returns `List[str]` (file paths)
- ✅ Creates 6 JSON files (QB, RB, WR, TE, K, DST)
- ✅ Task 11 assumption VERIFIED: Method signature matches spec

---

### 3. DataExporter.export_teams_to_data Method

**File:** `player-data-fetcher/player_data_exporter.py`

**Method Signature (lines 818-829):**
```python
async def export_teams_to_data(self, data: ProjectionData) -> str:
    """
    Export team data to shared data directory for consumption by other modules.

    Creates team_data folder with individual CSV files for each NFL team.

    Args:
        data: ProjectionData containing player information

    Returns:
        str: Path to the team_data folder
    """
```

**Verification:**
- ✅ Takes single parameter: `ProjectionData`
- ✅ Returns `str` (folder path)
- ✅ Creates team_data folder with individual CSV files per team
- ✅ Task 9 assumption VERIFIED: Method to be called after deletion of export_all_formats_with_teams

---

### 4. NFLProjectionsCollector.export_data Method

**File:** `player-data-fetcher/player_data_fetcher_main.py`

**Current Integration Point (lines 345-372):**
```python
for data_type, data in projection_data.items():
    # Export to all configured formats (CSV/JSON/Excel)
    # Also creates timestamped and latest versions
    # Also creates team_data folder with per-team historical data
    files = await self.exporter.export_all_formats_with_teams(
        data,
        create_csv=self.settings.create_csv,
        create_json=self.settings.create_json,
        create_excel=self.settings.create_excel
    )  # Lines 349-354 - TO BE DELETED in Task 9
    output_files.extend(files)
    self.logger.info(f"Exported {data_type} projections to configured formats")

    # Export position-based JSON files (if enabled via config)
    # Creates 6 files: new_qb_data.json, new_rb_data.json, new_wr_data.json,
    # new_te_data.json, new_k_data.json, new_dst_data.json
    try:
        position_json_files = await self.exporter.export_position_json_files(data)  # Line 363 - PRESERVED
        if position_json_files:
            output_files.extend(position_json_files)
            self.logger.info(f"Exported {len(position_json_files)} position-based JSON files")
    except Exception as e:
        self.logger.error(f"Error exporting position JSON files: {e}")
```

**Task 9 Changes:**
- ❌ DELETE lines 349-354 (export_all_formats_with_teams call)
- ❌ DELETE lines 355-357 (output_files.extend and logging)
- ✅ PRESERVE line 363 (export_position_json_files call)
- ➕ ADD export_teams_to_data() call after line 370

**Verification:**
- ✅ Current integration point identified
- ✅ Lines to delete: 349-354
- ✅ Method to preserve: export_position_json_files (line 363)
- ✅ Method to add: export_teams_to_data (new call after line 370)
- ✅ Task 9 assumptions VERIFIED

---

## Assumption Validation

**Checking implementation_plan.md assumptions against verified interfaces:**

### Task 8 Assumptions (DataFileManager):
- **Assumption:** DataFileManager accepts None for file_caps parameter
- **Reality:** ✅ VERIFIED - Lines 52-54 show fallback logic: `if file_caps is None: file_caps = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}`
- **Status:** ✅ NO REFACTORING NEEDED

### Task 9 Assumptions (Integration Point):
- **Assumption:** Remove export_all_formats_with_teams call, add export_teams_to_data call, preserve export_position_json_files
- **Reality:** ✅ VERIFIED - Lines 349-354 contain export_all_formats_with_teams, line 363 contains export_position_json_files
- **Status:** ✅ ASSUMPTIONS MATCH REALITY

### Task 11 Assumptions (Position JSON):
- **Assumption:** export_position_json_files creates 6 JSON files (QB, RB, WR, TE, K, DST)
- **Reality:** ✅ VERIFIED - Method docstring confirms "Creates 6 JSON files (one per position: QB, RB, WR, TE, K, DST)"
- **Status:** ✅ ASSUMPTIONS MATCH REALITY

### Task 12 Assumptions (Team Export):
- **Assumption:** export_teams_to_data creates 32 CSV files (one per NFL team)
- **Reality:** ✅ VERIFIED - Method docstring confirms "Creates team_data folder with individual CSV files for each NFL team"
- **Status:** ✅ ASSUMPTIONS MATCH REALITY

---

## Completion Status

**Interface Verification Protocol:** COMPLETE ✅

**All 4 external interfaces verified from source code:**
1. ✅ DataFileManager.__init__() - Accepts None, has fallback
2. ✅ DataExporter.export_position_json_files() - Creates 6 position JSON files
3. ✅ DataExporter.export_teams_to_data() - Creates team CSV files
4. ✅ NFLProjectionsCollector.export_data() - Integration point identified

**All assumptions validated:** 4/4 match reality (100%)

**Ready to proceed:** S6 Step 3 - Phase-by-Phase Implementation

---

**END OF INTERFACE CONTRACTS**
