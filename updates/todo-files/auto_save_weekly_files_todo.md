# Auto-Save Weekly Files - TODO

## Objective

Add automatic saving of weekly player and team data files to the historical data folder after the player data fetcher completes its update process.

**Based on**: `updates/auto_save_weekly_files.txt`

## Requirements Summary

After player data fetcher finishes updating:
1. `data/players.csv`
2. `data/players_projected.csv`
3. `data/teams.csv`

The system should automatically check if these files should be saved to `data/historical_data/{Season}/week{Week}/`. If the folder doesn't exist, create it and copy the 3 files. If it already exists, do nothing (files already saved for that week).

---

## High-Level Implementation Plan

### Phase 0: Add Configuration Option
**File**: `player-data-fetcher/config.py`

Add new configuration constant:
- `ENABLE_HISTORICAL_DATA_SAVE = True` - Boolean flag to enable/disable auto-save

**Expected Location**: After line 47 (after MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS)

### Phase 1: Add Historical Data Save Method
**File**: `player-data-fetcher/player_data_fetcher_main.py`

Add a new method to `NFLProjectionsCollector` class that:
- Checks config flag `ENABLE_HISTORICAL_DATA_SAVE`
- Checks if historical data folder exists for current season/week
- Creates folder if it doesn't exist (using zero-padded week number: `01`, `02`, `11`)
- Copies the 3 data files to the historical folder
- Logs the operation

**Folder naming**: `data/historical_data/{Season}/{WeekNumber}/` where WeekNumber is zero-padded (e.g., `01`, `11`)

**Expected Location**: After `export_data()` method (around line 358)

### Phase 2: Rename Existing Historical Folders
**Files**: `data/historical_data/2024/` and `data/historical_data/2025/`

Rename existing folders to match new convention:
- `week9` → `09`
- `week10` → `10`
- `week11` → `11`
- `WEEK8` → `08`

This ensures all historical data follows the consistent naming pattern: zero-padded numbers only.

**Note**: This is a one-time migration task. Create a simple Python script or use bash commands.

### Phase 3: Integrate with Export Workflow
**File**: `player-data-fetcher/player_data_fetcher_main.py`

Modify `main()` function to call the auto-save method after successful data export.

**Expected Location**: After line 442 (`output_files = await collector.export_data(projection_data)`)

### Phase 4: Add Unit Tests
**File**: `tests/player-data-fetcher/test_player_data_fetcher_main.py` (create if doesn't exist)

Create comprehensive tests for:
- Config flag check (ENABLE_HISTORICAL_DATA_SAVE)
- Historical folder creation when it doesn't exist
- File copying behavior with zero-padded week numbers
- Skip copying when folder already exists
- Error handling (permissions, disk space, etc.)
- Season and week folder path construction

### Phase 5: Integration Testing
**File**: Manual testing

Test the complete workflow:
- Run `python run_player_fetcher.py`
- Verify files are saved to correct location with zero-padded week number
- Run again and verify no duplicate saves
- Test with different week numbers
- Test with config flag disabled

### Phase 6: Documentation Updates
**Files**:
- `README.md`
- `player-data-fetcher/README.md` (if exists)
- `player-data-fetcher/config.py` (add comment for ENABLE_HISTORICAL_DATA_SAVE)

Document:
- New auto-save feature
- Historical data folder structure (zero-padded week numbers)
- How to disable/enable via config option
- Folder naming convention change

### Phase 7: Pre-Commit Validation
**Required**: 100% test pass rate before completion

Run full test suite:
```bash
python tests/run_all_tests.py
```

---

## Detailed Task Breakdown

### Phase 0: Add Configuration Option

#### Task 0.1: Add ENABLE_HISTORICAL_DATA_SAVE to config.py
**File**: `player-data-fetcher/config.py`
**Location**: After line 47 (after MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS)

Add new configuration constant:
```python
# Historical Data Auto-Save Configuration (FREQUENTLY MODIFIED)
ENABLE_HISTORICAL_DATA_SAVE = True  # Automatically save weekly data snapshots to historical folder
```

**Implementation Details**:
- Default to `True` (enabled by default)
- Place in "FREQUENTLY MODIFIED" section for easy access
- Add clear comment explaining purpose

### Phase 1: Add Historical Data Save Method

#### Task 1.1: Create `save_to_historical_data()` method
**File**: `player-data-fetcher/player_data_fetcher_main.py`
**Location**: After `export_data()` method (around line 358)

```python
def save_to_historical_data(self) -> bool:
    """
    Save current data files to historical data folder for the current week.

    Checks config flag ENABLE_HISTORICAL_DATA_SAVE before proceeding.
    Checks if data/historical_data/{Season}/{WeekNumber}/ exists.
    If not, creates it and copies players.csv, players_projected.csv, teams.csv.
    If it exists, skips (files already saved for this week).

    Week numbers are zero-padded (01, 02, ..., 11, 12).

    Returns:
        bool: True if files were saved, False if already saved, disabled, or error occurred
    """
```

**Implementation Details**:
1. Check if `ENABLE_HISTORICAL_DATA_SAVE` is True (if False, log and return False)
2. Construct week number with zero-padding: `f"{CURRENT_NFL_WEEK:02d}"` → `"01"`, `"11"`
3. Construct path: `data/historical_data/{NFL_SEASON}/{week_number}/`
4. Check if path exists using `Path.exists()`
5. If not exists:
   - Create directory with `Path.mkdir(parents=True, exist_ok=True)`
   - Copy 3 files using `shutil.copy2()` to preserve metadata
   - Log success with INFO level
   - Return True
6. If exists:
   - Log "already saved" message with INFO level
   - Return False
7. Add error handling with try/except, log warnings on error

**Required Imports**:
```python
import shutil
from pathlib import Path
from config import ENABLE_HISTORICAL_DATA_SAVE  # Add to existing imports
```

**Similar Pattern**: See `DataExporter._create_output_directory()` in `player_data_exporter.py` for directory creation pattern

#### Task 1.2: Add logging for historical data operations
**File**: `player-data-fetcher/player_data_fetcher_main.py`

Add appropriate logging:
- INFO: When creating new week folder
- INFO: When copying files
- INFO: When folder already exists (skip operation)
- WARNING: When copy operation fails
- ERROR: When path creation fails

**Pattern**: Follow existing logging patterns in the file (e.g., lines 249-260)

### Phase 2: Rename Existing Historical Folders

#### Task 2.1: Rename 2024 historical folders
**Directory**: `data/historical_data/2024/`

**Folders to rename**:
- No folders currently exist in 2024 (verified by file listing)
- Skip this task if folder is empty

#### Task 2.2: Rename 2025 historical folders
**Directory**: `data/historical_data/2025/`

**Folders to rename**:
- `WEEK8` → `08`
- `week9` → `09`
- `week10` → `10`
- `week11` → `11`

**Implementation**:
Use bash commands or create simple Python script:
```bash
cd data/historical_data/2025/
mv WEEK8 08
mv week9 09
mv week10 10
mv week11 11
```

Or Python script:
```python
from pathlib import Path

historical_2025 = Path("data/historical_data/2025")
renames = {
    "WEEK8": "08",
    "week9": "09",
    "week10": "10",
    "week11": "11"
}

for old_name, new_name in renames.items():
    old_path = historical_2025 / old_name
    new_path = historical_2025 / new_name
    if old_path.exists():
        old_path.rename(new_path)
        print(f"Renamed {old_name} → {new_name}")
```

**Verification**:
- Check that all folders are renamed correctly
- Verify files inside folders are intact
- Verify season_schedule.csv is still in 2025/ directory

### Phase 3: Integrate with Export Workflow

#### Task 3.1: Call auto-save after successful export
**File**: `player-data-fetcher/player_data_fetcher_main.py`
**Location**: In `main()` function after line 442

Add call to new method:
```python
# Export data
output_files = await collector.export_data(projection_data)

# Auto-save to historical data folder (if enabled via config)
try:
    saved = collector.save_to_historical_data()
    if saved:
        print(f"\n[INFO] Saved weekly data to historical folder")
    elif not ENABLE_HISTORICAL_DATA_SAVE:
        logger.debug("Historical data auto-save disabled via config")
    else:
        print(f"\n[INFO] Weekly data already saved for Week {settings.current_nfl_week}")
except Exception as e:
    logger.warning(f"Failed to save historical data: {e}")
    print(f"\n[WARNING] Could not save to historical folder: {e}")
```

**Note**: Use try/except to ensure save failure doesn't crash the entire program

#### Task 3.2: Pass necessary context to method
**File**: `player-data-fetcher/player_data_fetcher_main.py`

Ensure method has access to:
- `NFL_SEASON` (from config, already imported)
- `CURRENT_NFL_WEEK` (from config, already imported via settings)
- Path to data files (use script_dir to construct paths)

### Phase 3: Add Unit Tests

#### Task 3.1: Create test file structure
**File**: `tests/player-data-fetcher/test_player_data_fetcher_main.py`

Check if file exists. If not, create new test file with basic structure:
```python
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys

sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))
from player_data_fetcher_main import NFLProjectionsCollector, Settings

class TestHistoricalDataSave:
    """Test automatic saving of weekly data to historical folder"""
```

**Pattern**: Follow test structure from `tests/player-data-fetcher/test_espn_client.py`

#### Task 3.2: Add test for folder creation
Test that folder is created when it doesn't exist:
```python
@patch('player_data_fetcher_main.shutil.copy2')
def test_save_creates_folder_when_missing(self, mock_copy, tmp_path, test_collector):
    """Test that historical data folder is created if it doesn't exist"""
```

#### Task 3.3: Add test for file copying
Test that 3 files are copied correctly:
```python
@patch('player_data_fetcher_main.shutil.copy2')
@patch('pathlib.Path.exists')
def test_save_copies_three_files(self, mock_exists, mock_copy, test_collector):
    """Test that players.csv, players_projected.csv, and teams.csv are copied"""
```

#### Task 3.4: Add test for skip when folder exists
Test that nothing happens if folder already exists:
```python
@patch('pathlib.Path.exists')
def test_save_skips_when_folder_exists(self, mock_exists, test_collector):
    """Test that save operation is skipped when weekly folder already exists"""
```

#### Task 3.5: Add test for error handling
Test graceful error handling:
```python
@patch('player_data_fetcher_main.shutil.copy2')
@patch('pathlib.Path.mkdir')
def test_save_handles_permission_error(self, mock_mkdir, mock_copy, test_collector):
    """Test that permission errors are handled gracefully"""
```

#### Task 3.6: Add test for path construction
Test correct path formatting:
```python
def test_save_constructs_correct_path(self, test_collector):
    """Test that historical data path is correctly formatted"""
```

### Phase 4: Integration Testing

#### Task 4.1: Manual test - First run (folder creation)
**Steps**:
1. Delete `data/historical_data/2025/week11/` folder if it exists
2. Run `python run_player_fetcher.py`
3. Verify folder created at `data/historical_data/2025/week11/`
4. Verify 3 files exist in folder:
   - `players.csv`
   - `players_projected.csv`
   - `teams.csv`
5. Verify file contents match source files

#### Task 4.2: Manual test - Second run (skip save)
**Steps**:
1. Note modification timestamps of files in historical folder
2. Run `python run_player_fetcher.py` again
3. Verify log shows "already saved" message
4. Verify file timestamps unchanged (no overwrite)

#### Task 4.3: Manual test - Different week
**Steps**:
1. Change `CURRENT_NFL_WEEK` in `config.py` to 12
2. Run `python run_player_fetcher.py`
3. Verify new folder created at `data/historical_data/2025/week12/`
4. Verify week11 folder unchanged

### Phase 5: Documentation Updates

#### Task 5.1: Update README.md
**File**: `README.md`
**Section**: Under "Player Data Fetcher" section

Add description of auto-save feature:
```markdown
### Automatic Historical Data Saving

The player data fetcher automatically saves weekly snapshots to `data/historical_data/{Season}/week{Week}/`:
- `players.csv` - Current player data
- `players_projected.csv` - Week-by-week projections
- `teams.csv` - Team quality rankings

Files are only saved once per week. Subsequent runs in the same week skip the save operation to prevent overwrites.
```

#### Task 5.2: Update player-data-fetcher documentation
**File**: `player-data-fetcher/README.md` (if exists)

Add similar documentation about auto-save feature.
If file doesn't exist, skip this task.

### Phase 6: Pre-Commit Validation

#### Task 6.1: Run full unit test suite
**Command**: `python tests/run_all_tests.py`

**Required**: 100% pass rate across all 1,811+ tests

**Verification**:
- All existing tests still pass
- New tests for auto-save feature pass
- No regressions introduced

#### Task 6.2: Run player data fetcher tests specifically
**Command**: `python -m pytest tests/player-data-fetcher/ -v`

Verify all player-data-fetcher tests pass.

---

## Progress Tracking

**Keep this section updated as work progresses**:

- [ ] Phase 0: Add Configuration Option
  - [ ] Task 0.1: Add ENABLE_HISTORICAL_DATA_SAVE to config.py
- [ ] Phase 1: Add Historical Data Save Method
  - [ ] Task 1.1: Create `save_to_historical_data()` method
  - [ ] Task 1.2: Add logging
- [ ] Phase 2: Rename Existing Historical Folders
  - [ ] Task 2.1: Rename 2024 historical folders (skip if empty)
  - [ ] Task 2.2: Rename 2025 historical folders (WEEK8→08, week9→09, week10→10, week11→11)
- [ ] Phase 3: Integrate with Export Workflow
  - [ ] Task 3.1: Call auto-save after export
  - [ ] Task 3.2: Pass necessary context
- [ ] Phase 4: Add Unit Tests
  - [ ] Task 4.1: Create test file structure
  - [ ] Task 4.2: Test config flag check
  - [ ] Task 4.3: Test folder creation with zero-padded week
  - [ ] Task 4.4: Test file copying
  - [ ] Task 4.5: Test skip when exists
  - [ ] Task 4.6: Test error handling
  - [ ] Task 4.7: Test path construction
- [ ] Phase 5: Integration Testing
  - [ ] Task 5.1: First run test (folder creation)
  - [ ] Task 5.2: Second run test (skip save)
  - [ ] Task 5.3: Different week test
  - [ ] Task 5.4: Config flag disabled test
- [ ] Phase 6: Documentation Updates
  - [ ] Task 6.1: Update README.md
  - [ ] Task 6.2: Update player-data-fetcher docs
  - [ ] Task 6.3: Add config comment
- [ ] Phase 7: Pre-Commit Validation
  - [ ] Task 7.1: Run full test suite (100% pass)
  - [ ] Task 7.2: Run player-data-fetcher tests

---

## Notes for Continuation

**If a new Claude agent needs to continue this work**:
1. Read this TODO file completely
2. Check progress tracking section for completed tasks
3. Review `updates/auto_save_weekly_files_code_changes.md` for code already written
4. Continue from first unchecked task in progress tracking
5. Update this TODO file as each task is completed
6. Run tests after each phase completion

**Critical Dependencies**:
- `shutil` module for file copying
- `Path` from pathlib for path manipulation
- `NFL_SEASON` and `CURRENT_NFL_WEEK` from `config.py`
- Existing `data/` folder structure

**Risk Areas**:
- Permission errors when creating folders
- Disk space issues when copying files
- Race conditions if multiple processes run simultaneously
- Path construction errors on different OS platforms (Windows vs Linux)

---

## Verification Summary

### First Verification Round (Iterations 1-3)
- [x] Iteration 1 complete - Initial verification and codebase research
- [x] Iteration 2 complete - Deep dive into error handling and test patterns
- [x] Iteration 3 complete - Integration points and final verification

### Second Verification Round (Iterations 4-6)
- [x] Iteration 4 complete - Validated user answers integrated
- [x] Iteration 5 complete - Implementation refinement and edge cases
- [x] Iteration 6 complete - Final comprehensive verification

**Total Iterations**: 6/6 complete ✅

**Iteration 6 Findings - Final Verification**:
- ✅ All original requirements covered: check folder, create if missing, copy 3 files, skip if exists
- ✅ All 8 user decisions fully integrated into implementation plan
- ✅ Task dependencies verified: Phase 0 → Phase 1 → Phase 2 (can run parallel with Phase 1) → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7
- ✅ Test coverage plan comprehensive: config flag, folder creation, file copying, skip logic, error handling
- ✅ Documentation updates specified for README, config comments, and feature description
- ✅ Pre-commit validation checkpoints at phase completions
- ✅ No circular dependencies or integration conflicts
- ✅ Path construction uses relative paths from script_dir for portability
- ✅ Error handling preserves main workflow (non-fatal errors)
- ✅ Implementation ready to begin

**Iteration 5 Findings - Implementation Refinement**:
- **Edge Case**: Week 0 - NFL season doesn't have week 0, starts at week 1. Zero-padding works correctly: `f"{1:02d}"` = `"01"`
- **Edge Case**: Week 18+ - Playoffs. Current implementation handles up to week 18 correctly. If CURRENT_NFL_WEEK > 18, format still works but folder would be `19`, `20`, etc.
- **Import Order**: ENABLE_HISTORICAL_DATA_SAVE must be imported at top of player_data_fetcher_main.py with other config imports (line 32-38)
- **Folder Rename Safety**: Use `Path.rename()` method - atomic operation on same filesystem, safe
- **Folder Rename Verification**: After rename, verify files exist in renamed folders before marking complete
- **Config Import in Settings**: Settings class doesn't need ENABLE_HISTORICAL_DATA_SAVE - only NFLProjectionsCollector needs it
- **Test Config Mocking**: Tests should mock ENABLE_HISTORICAL_DATA_SAVE to test both enabled and disabled states
- **Path Construction**: Use `self.script_dir.parent / "data" / "historical_data"` for relative path from player-data-fetcher/ directory

**Iteration 4 Findings - User Answer Integration**:
- ✅ Config option ENABLE_HISTORICAL_DATA_SAVE added to Phase 0
- ✅ Zero-padded folder naming `{:02d}` integrated throughout (e.g., `01`, `11`)
- ✅ Phase 2 added for renaming existing folders to match new convention
- ✅ All 8 user decisions documented in verification summary
- ✅ Task numbering updated to reflect new Phase 0 and Phase 2
- ✅ Progress tracking updated with all new tasks
- ✅ Import requirement updated: `from config import ENABLE_HISTORICAL_DATA_SAVE`
- ✅ Console output updated to handle disabled config case

**Iteration 3 Findings - Integration & Finalization**:
- **Integration Point**: Player data fetcher called via subprocess from run_player_fetcher.py
- **No Cross-Module Dependencies**: Auto-save feature contained within player_data_fetcher_main.py only
- **Integration Tests**: Test structure uses tmp_path fixtures and mocks (tests/integration/test_data_fetcher_integration.py)
- **Test Mocking Strategy**: Mock _get_api_client method, use AsyncMock for session context manager
- **Path Construction**: Use Path objects exclusively - compatible with Windows and Linux
- **No Circular Dependencies**: Feature is self-contained, no imports from other league helper modules
- **File Integrity**: No checksum validation needed - simple file copy operation
- **Cleanup Operations**: Not required - feature is append-only (never deletes historical data)

**Iteration 2 Findings - Error Handling & Testing**:
- **Error Handling Strategy**: Use specific exceptions (FileNotFoundError) first, then broad Exception as fallback
- **Logging in Exception Handlers**: Always log errors with appropriate level (ERROR for critical, WARNING for non-critical)
- **Non-Fatal Errors**: Supplementary features should not crash main workflow (see player_data_fetcher_main.py:348-356)
- **Error Logging with Traceback**: Use `exc_info=True` for detailed error information (see line 470)
- **Test Structure**: Tests already exist in tests/player-data-fetcher/test_player_data_fetcher_main.py
- **Test Patterns**: Use @patch decorators, Mock/AsyncMock objects, pytest fixtures
- **Test Organization**: Group related tests in classes (TestSettings, TestNFLProjectionsCollectorInit, etc.)
- **Test File Structure**: Mirror source file structure (test_player_data_fetcher_main.py tests player_data_fetcher_main.py)

**Requirements Added After Draft**:
- **NEW**: Add configuration option ENABLE_HISTORICAL_DATA_SAVE to config.py (User Decision: Question 1 - Option B)
- **CHANGED**: Folder naming convention: `{N}` (zero-padded numbers only, e.g., `01`, `11`) - NOT `week{N}` (User Decision: Question 4 & 7)
- **NEW**: Rename existing folders to match new convention (User Decision: Question 4)
- Verified folder path: `data/historical_data/{Season}/{WeekNumber}/`
- Confirmed 3 files to copy: players.csv, players_projected.csv, teams.csv
- All requirements from original specification covered in TODO

**User Decisions from Questions File**:
1. Configuration: Add config option (ENABLE_HISTORICAL_DATA_SAVE) - Option B
2. Notification Level: INFO logging + console message - Option A
3. Error Handling: Log warning, continue execution - Option A
4. Folder Naming: Just the number (e.g., `11`) - CUSTOM (no "week" prefix)
5. Metadata Preservation: Preserve metadata (shutil.copy2) - Option A
6. Season Folder Creation: Create if needed (parents=True) - Option A
7. Week Padding: Zero-padded (e.g., `01`, `11`) - CUSTOM (zero-padded)
8. Historical Cleanup: No automatic cleanup - Option A

**Key Codebase Patterns Identified**:
1. **Directory Creation Pattern**: `Path.mkdir(parents=True, exist_ok=True)` (used in utils/data_file_manager.py:59 and player_data_exporter.py:43)
2. **Path Handling**: Use `Path` objects, convert to string only when needed
3. **Error Handling**: Wrap operations in try/except with logging
4. **Logging Pattern**: DEBUG for details, INFO for operations, WARNING for skips, ERROR for failures
5. **Historical Data Access**: Already exists in league_helper/reserve_assessment_mode/ReserveAssessmentModeManager.py:238
6. **File Copying**: `shutil` module already used in utils/data_file_manager.py

**Critical Dependencies**:
- `shutil.copy2()` for file copying (preserves metadata)
- `Path.exists()` for folder existence check
- `Path.mkdir(parents=True, exist_ok=True)` for folder creation
- `NFL_SEASON` from config.py (currently 2025)
- `CURRENT_NFL_WEEK` from settings.current_nfl_week (from config.py, currently 11)
- `self.script_dir` for path construction (already available in NFLProjectionsCollector)

**Risk Areas**:
- Permission errors when creating folders (mitigated with try/except)
- Disk space issues when copying large files (each file ~124KB + 2.7MB + 839B = ~2.8MB total)
- Race conditions if multiple processes run simultaneously (unlikely, but handle with folder existence check)
- Path construction errors (mitigated by using Path objects and testing on different OS)
