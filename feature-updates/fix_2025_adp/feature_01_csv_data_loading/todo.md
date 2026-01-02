# Feature 01: CSV Data Loading - Implementation TODO

**Created:** 2025-12-31
**Feature:** CSV Data Loading (Feature 1 of 2)
**Epic:** fix_2025_adp

**Status:** Round 1 (Iterations 1-7 + 4a) in progress

---

## Round 1 Progress Tracker

**Iterations Complete:**
- [x] Iteration 1: Requirements Coverage Check
- [ ] Iteration 2: Component Dependency Mapping
- [ ] Iteration 3: Data Structure Verification
- [ ] Iteration 4: Algorithm Traceability Matrix
- [ ] Iteration 4a: TODO Specification Audit (MANDATORY GATE)
- [ ] Iteration 5: End-to-End Data Flow
- [ ] Iteration 6: Error Handling Scenarios
- [ ] Iteration 7: Integration Gap Check

**Round 1 Checkpoint:** Not reached yet

---

## Task List (Based on spec.md Requirements)

### Task 1: Create adp_csv_loader.py Module

**Requirement:** Create new module for CSV loading (spec.md Implementation Module section)

**Acceptance Criteria:**
- [ ] File created: `utils/adp_csv_loader.py`
- [ ] Module docstring added (describes purpose: Load ADP data from FantasyPros CSV)
- [ ] Imports added:
  - `from pathlib import Path`
  - `from typing import Union`
  - `import pandas as pd`
  - `from utils.csv_utils import read_csv_with_validation`
  - `from utils.error_handler import error_context`
  - `from utils.LoggingManager import get_logger`
- [ ] Logger initialized: `logger = get_logger()`
- [ ] File structure follows project conventions

**Implementation Location:**
- File: `utils/adp_csv_loader.py` (NEW FILE)
- Lines: 1-20 (module header)

**Dependencies:**
- Requires: Existing utils modules (csv_utils, error_handler, LoggingManager)
- Called by: Task 2 (load_adp_from_csv function)

**Tests:**
- Module import test: `test_adp_csv_loader_module_imports()`

---

### Task 2: Implement load_adp_from_csv() Function

**Requirement:** Load ADP data from FantasyPros CSV file (spec.md Primary Function section)

**Acceptance Criteria:**
- [ ] Function created: `def load_adp_from_csv(csv_path: Union[str, Path]) -> pd.DataFrame:`
- [ ] Docstring added with:
  - Purpose: Load ADP data from FantasyPros CSV file
  - Args: csv_path (Union[str, Path]) - Path to CSV file
  - Returns: DataFrame with columns: player_name, adp, position
  - Raises: FileNotFoundError, ValueError
- [ ] Function signature matches spec exactly
- [ ] Type hints complete and correct
- [ ] Implementation follows all processing steps (Task 3-10)

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~25-80

**Dependencies:**
- Requires: Task 1 complete (module created)
- Requires: Tasks 3-10 (processing steps)
- Called by: Feature 2 (player matching update)

**Tests:**
- Unit test: `test_load_adp_from_csv_success()`
- Unit test: `test_load_adp_from_csv_returns_dataframe()`

---

### Task 3: Validate File Exists

**Requirement:** Validate CSV file exists before processing (spec.md Processing Steps, step 1)

**Acceptance Criteria:**
- [ ] Convert csv_path to Path object
- [ ] Check: `Path(csv_path).exists()`
- [ ] If file doesn't exist: raise FileNotFoundError with message
- [ ] Error message includes: file path attempted
- [ ] Logged before raising: `logger.error(f"CSV file not found: {csv_path}")`

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~30-35 (early validation)

**Dependencies:**
- Requires: Task 2 (function created)
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_file_not_found()`

---

### Task 4: Validate Required Columns Present

**Requirement:** Validate CSV has required columns (spec.md Processing Steps, step 2; spec.md Validation Requirements)

**Acceptance Criteria:**
- [ ] Required columns list: `['Player', 'POS', 'AVG']`
- [ ] Use: `read_csv_with_validation(csv_path, required_columns=['Player', 'POS', 'AVG'], encoding='utf-8')`
- [ ] If columns missing: ValueError raised by csv_utils (let propagate)
- [ ] Logged after validation: `logger.info(f"CSV validation passed: {csv_path}")`

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~38-42 (CSV reading)

**Dependencies:**
- Requires: Task 3 (file exists validated)
- Requires: `utils.csv_utils.read_csv_with_validation()`
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_missing_columns()`

---

### Task 5: Extract Required Columns

**Requirement:** Extract only needed columns from CSV (spec.md Processing Steps, step 4)

**Acceptance Criteria:**
- [ ] Extract columns: `df = df[['Player', 'POS', 'AVG']]`
- [ ] Other columns (Team, Bye, ESPN, etc.) dropped
- [ ] DataFrame has exactly 3 columns after extraction
- [ ] Verified: No data loss for required columns

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~45-47 (column extraction)

**Dependencies:**
- Requires: Task 4 (CSV loaded)
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_correct_columns()`

---

### Task 6: Clean Position Field (Strip Suffixes)

**Requirement:** Strip numeric suffixes from position field (spec.md Processing Steps, step 5; spec.md Technical Decisions #2)

**Algorithm from spec:**
> "Clean position strings (strip tier suffixes: 'WR1' → 'WR', 'QB12' → 'QB')"

**Acceptance Criteria:**
- [ ] Apply regex: `df['position'] = df['POS'].str.replace(r'\d+$', '', regex=True)`
- [ ] Verified: 'WR1' becomes 'WR'
- [ ] Verified: 'QB12' becomes 'QB'
- [ ] Verified: 'RB2' becomes 'RB'
- [ ] Verified: 'TE1' becomes 'TE'
- [ ] Verified: 'K1' becomes 'K'
- [ ] Verified: 'DST1' becomes 'DST'
- [ ] Result: Only clean positions (QB, RB, WR, TE, K, DST)

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~50-52 (position cleaning)

**Dependencies:**
- Requires: Task 5 (columns extracted)
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_strips_position_suffixes()`
- Unit test: `test_position_cleaning_all_positions()`

---

### Task 7: Parse AVG as Float

**Requirement:** Parse AVG column as float values (spec.md Processing Steps, step 6)

**Acceptance Criteria:**
- [ ] Convert: `df['adp'] = df['AVG'].astype(float)`
- [ ] Verified: Column dtype is float64
- [ ] Handles decimal values: 1.0, 2.2, 20.0
- [ ] No type errors during conversion

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~55-57 (ADP parsing)

**Dependencies:**
- Requires: Task 5 (columns extracted)
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_adp_is_float()`
- Unit test: `test_load_adp_from_csv_handles_decimal_adp()`

---

### Task 8: Rename Columns

**Requirement:** Rename columns to standard names (spec.md Processing Steps, step 7; spec.md Output Data Structure)

**Acceptance Criteria:**
- [ ] Rename: `df = df.rename(columns={'Player': 'player_name'})`
- [ ] Column 'POS' dropped (already created 'position' in Task 6)
- [ ] Column 'AVG' dropped (already created 'adp' in Task 7)
- [ ] Final columns: `['player_name', 'adp', 'position']`
- [ ] Column order: player_name, adp, position

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~60-62 (column renaming)

**Dependencies:**
- Requires: Task 6 (position cleaned)
- Requires: Task 7 (adp parsed)
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_column_names()`

---

### Task 9: Validate Player Names Non-Empty

**Requirement:** Validate all player_name values are non-empty (spec.md Processing Steps, step 8; spec.md Validation Requirements)

**Acceptance Criteria:**
- [ ] Check: `df['player_name'].notna().all()`
- [ ] Check: `(df['player_name'].str.len() > 0).all()`
- [ ] If empty player names found: raise ValueError("Empty player names found in CSV")
- [ ] Logged: `logger.info(f"Validated {len(df)} player names")`

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~65-70 (validation)

**Dependencies:**
- Requires: Task 8 (columns renamed)
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_validates_player_names()`
- Unit test: `test_load_adp_from_csv_rejects_empty_names()`

---

### Task 10: Validate ADP Values Positive

**Requirement:** Validate all adp values are positive floats (spec.md Processing Steps, step 9; spec.md Technical Decisions #5)

**Acceptance Criteria:**
- [ ] Check: `(df['adp'] > 0).all()`
- [ ] If ADP <= 0 found: raise ValueError(f"Invalid ADP values found: ADP must be > 0")
- [ ] Logged: `logger.info(f"Validated {len(df)} ADP values (all > 0)")`

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~72-77 (validation)

**Dependencies:**
- Requires: Task 7 (adp parsed as float)
- Requires: Task 9 (player names validated)
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_validates_adp_positive()`
- Unit test: `test_load_adp_from_csv_rejects_zero_adp()`
- Unit test: `test_load_adp_from_csv_rejects_negative_adp()`

---

### Task 11: Return DataFrame

**Requirement:** Return DataFrame with correct structure (spec.md Processing Steps, step 10; spec.md Output Data Structure)

**Acceptance Criteria:**
- [ ] Return statement: `return df`
- [ ] Returned DataFrame has columns: `['player_name', 'adp', 'position']`
- [ ] Returned DataFrame has correct types:
  - player_name: str (object dtype)
  - adp: float (float64 dtype)
  - position: str (object dtype)
- [ ] Row count matches CSV (988 rows expected)
- [ ] Logged: `logger.info(f"Successfully loaded {len(df)} ADP rankings from CSV")`

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~80-82 (return)

**Dependencies:**
- Requires: All previous tasks (1-10)
- Part of: Task 2 implementation

**Tests:**
- Unit test: `test_load_adp_from_csv_returns_correct_structure()`
- Unit test: `test_load_adp_from_csv_row_count()`

---

### Task 12: Error Handling - FileNotFoundError

**Requirement:** Handle missing CSV file gracefully (spec.md Error Handling section)

**Acceptance Criteria:**
- [ ] File existence check in Task 3
- [ ] Raises: `FileNotFoundError` with descriptive message
- [ ] Error message: f"CSV file not found: {csv_path}"
- [ ] Logged before raising: `logger.error(f"CSV file not found: {csv_path}")`
- [ ] No silent failures (error must propagate)

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~30-35 (part of Task 3)

**Dependencies:**
- Part of: Task 3 (file validation)

**Tests:**
- Unit test: `test_load_adp_from_csv_file_not_found()`

---

### Task 13: Error Handling - ValueError (Missing Columns)

**Requirement:** Handle CSV with missing required columns (spec.md Error Handling section)

**Acceptance Criteria:**
- [ ] Validation in Task 4 using csv_utils
- [ ] Raises: `ValueError` if required columns missing
- [ ] Error propagates from `read_csv_with_validation()`
- [ ] Error message includes which columns missing
- [ ] Logged: csv_utils handles logging

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~38-42 (part of Task 4)

**Dependencies:**
- Part of: Task 4 (column validation)
- Requires: utils.csv_utils.read_csv_with_validation()

**Tests:**
- Unit test: `test_load_adp_from_csv_missing_columns()`

---

### Task 14: Error Handling - ValueError (Invalid ADP)

**Requirement:** Handle invalid ADP values (spec.md Error Handling section; spec.md Validation Requirements)

**Acceptance Criteria:**
- [ ] Validation in Task 10
- [ ] Raises: `ValueError` if ADP <= 0
- [ ] Error message: f"Invalid ADP values found: ADP must be > 0"
- [ ] Logged before raising: details of invalid values
- [ ] No silent failures

**Implementation Location:**
- File: `utils/adp_csv_loader.py`
- Function: `load_adp_from_csv()`
- Lines: ~72-77 (part of Task 10)

**Dependencies:**
- Part of: Task 10 (ADP validation)

**Tests:**
- Unit test: `test_load_adp_from_csv_rejects_zero_adp()`
- Unit test: `test_load_adp_from_csv_rejects_negative_adp()`

---

## Test Tasks

### Task 15: Create Test Module

**Requirement:** Create test file following project structure (spec.md Testing Strategy)

**Acceptance Criteria:**
- [ ] File created: `tests/utils/test_adp_csv_loader.py`
- [ ] Imports added:
  - `import pytest`
  - `from pathlib import Path`
  - `import pandas as pd`
  - `from utils.adp_csv_loader import load_adp_from_csv`
- [ ] Test class: `class TestLoadAdpFromCsv:`
- [ ] Fixtures created (Task 16)

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py` (NEW FILE)
- Lines: 1-20 (module header)

**Dependencies:**
- Requires: Task 1 (module created)

**Tests:**
- N/A (this IS the test file)

---

### Task 16: Create Test Fixtures

**Requirement:** Create reusable test data fixtures (spec.md Test Pattern)

**Acceptance Criteria:**
- [ ] Fixture: `test_csv_file(tmp_path)` - creates valid test CSV
- [ ] Test CSV contains:
  - Header row: Player,POS,AVG
  - Data rows: At least 2 players with known values
  - Example: "Ja'Marr Chase","WR1","1.0"
  - Example: "Bijan Robinson","RB2","2.2"
- [ ] Fixture returns: Path to test CSV file
- [ ] CSV written with proper encoding (UTF-8)

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Fixtures: `test_csv_file()`
- Lines: ~25-40

**Dependencies:**
- Requires: Task 15 (test module created)
- Used by: All test tasks (17-26)

**Tests:**
- N/A (this creates test fixtures)

---

### Task 17: Test - Successful CSV Load

**Requirement:** Test normal CSV loading (spec.md Test Cases #1)

**Acceptance Criteria:**
- [ ] Test: `test_loads_csv_successfully(test_csv_file)`
- [ ] Loads DataFrame using test CSV
- [ ] Asserts: `len(df) == 2` (test CSV has 2 rows)
- [ ] Asserts: `list(df.columns) == ['player_name', 'adp', 'position']`
- [ ] Asserts: First row matches expected values
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_loads_csv_successfully()`
- Lines: ~45-55

**Dependencies:**
- Requires: Task 2 (function implemented)
- Requires: Task 16 (fixture created)

**Tests:**
- This IS a test

---

### Task 18: Test - Validates Required Columns

**Requirement:** Test column validation (spec.md Test Cases #2)

**Acceptance Criteria:**
- [ ] Test: `test_validates_required_columns(tmp_path)`
- [ ] Creates CSV missing 'AVG' column
- [ ] Calls: `load_adp_from_csv(csv_path)`
- [ ] Asserts: `ValueError` raised
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_validates_required_columns()`
- Lines: ~60-70

**Dependencies:**
- Requires: Task 4 (column validation implemented)

**Tests:**
- This IS a test

---

### Task 19: Test - FileNotFoundError When Missing

**Requirement:** Test missing file handling (spec.md Test Cases #3)

**Acceptance Criteria:**
- [ ] Test: `test_raises_error_when_file_missing(tmp_path)`
- [ ] Creates path to non-existent file
- [ ] Calls: `load_adp_from_csv(nonexistent_path)`
- [ ] Asserts: `FileNotFoundError` raised
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_raises_error_when_file_missing()`
- Lines: ~75-85

**Dependencies:**
- Requires: Task 3 (file validation implemented)

**Tests:**
- This IS a test

---

### Task 20: Test - Position Suffix Stripping

**Requirement:** Test position cleaning (spec.md Test Cases #5)

**Acceptance Criteria:**
- [ ] Test: `test_strips_position_suffixes(test_csv_file)`
- [ ] Test CSV has positions: WR1, RB2, QB12
- [ ] Loads DataFrame
- [ ] Asserts: `df['position'].tolist() == ['WR', 'RB', 'QB']` (no suffixes)
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_strips_position_suffixes()`
- Lines: ~90-100

**Dependencies:**
- Requires: Task 6 (position cleaning implemented)

**Tests:**
- This IS a test

---

### Task 21: Test - ADP Parsed as Float

**Requirement:** Test ADP type conversion (spec.md Test Cases #6)

**Acceptance Criteria:**
- [ ] Test: `test_parses_adp_as_float(test_csv_file)`
- [ ] Loads DataFrame
- [ ] Asserts: `df['adp'].dtype == 'float64'`
- [ ] Asserts: `df['adp'].iloc[0] == 1.0` (exact value)
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_parses_adp_as_float()`
- Lines: ~105-115

**Dependencies:**
- Requires: Task 7 (ADP parsing implemented)

**Tests:**
- This IS a test

---

### Task 22: Test - Output Has Correct Columns

**Requirement:** Test DataFrame structure (spec.md Test Cases #8)

**Acceptance Criteria:**
- [ ] Test: `test_output_has_correct_columns(test_csv_file)`
- [ ] Loads DataFrame
- [ ] Asserts: `list(df.columns) == ['player_name', 'adp', 'position']`
- [ ] Asserts: Column order correct
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_output_has_correct_columns()`
- Lines: ~120-130

**Dependencies:**
- Requires: Task 8 (column renaming implemented)

**Tests:**
- This IS a test

---

### Task 23: Test - Validates Positive ADP Values

**Requirement:** Test ADP validation (spec.md Test Cases #9)

**Acceptance Criteria:**
- [ ] Test: `test_validates_positive_adp_values(tmp_path)`
- [ ] Creates CSV with ADP value = 0
- [ ] Calls: `load_adp_from_csv(csv_path)`
- [ ] Asserts: `ValueError` raised
- [ ] Error message contains "ADP must be > 0"
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_validates_positive_adp_values()`
- Lines: ~135-145

**Dependencies:**
- Requires: Task 10 (ADP validation implemented)

**Tests:**
- This IS a test

---

### Task 24: Test - Player Name Variations

**Requirement:** Test names with special characters (spec.md Test Cases #10)

**Acceptance Criteria:**
- [ ] Test: `test_handles_player_name_variations(tmp_path)`
- [ ] Creates CSV with names: "Ja'Marr Chase", "Kenneth Walker III"
- [ ] Loads DataFrame
- [ ] Asserts: Names preserved exactly (with apostrophe, with suffix)
- [ ] No parsing errors
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_handles_player_name_variations()`
- Lines: ~150-160

**Dependencies:**
- Requires: Task 9 (player name validation implemented)

**Tests:**
- This IS a test

---

### Task 25: Test - Real CSV File (Integration Test)

**Requirement:** Test with actual FantasyPros CSV (optional integration test)

**Acceptance Criteria:**
- [ ] Test: `test_loads_real_fantasypros_csv()` (skip if file not present)
- [ ] Path: `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv`
- [ ] Uses pytest.mark.skipif if file missing
- [ ] Loads DataFrame
- [ ] Asserts: `len(df) == 988` (expected row count)
- [ ] Asserts: All positions in {QB, RB, WR, TE, K, DST}
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_loads_real_fantasypros_csv()`
- Lines: ~165-180

**Dependencies:**
- Requires: All implementation tasks complete (1-14)

**Tests:**
- This IS a test (integration test)

---

### Task 26: Test - Empty Team Field Handling

**Requirement:** Test handling of empty Team fields (spec.md Edge Cases #1)

**Acceptance Criteria:**
- [ ] Test: `test_handles_empty_team_field(tmp_path)`
- [ ] Creates CSV with empty Team column (like real CSV)
- [ ] Columns used: Player, POS, AVG (Team excluded)
- [ ] Loads DataFrame successfully
- [ ] Asserts: No errors from empty Team field
- [ ] Test passes

**Implementation Location:**
- File: `tests/utils/test_adp_csv_loader.py`
- Test: `test_handles_empty_team_field()`
- Lines: ~185-195

**Dependencies:**
- Requires: Task 5 (column extraction - Team excluded)

**Tests:**
- This IS a test

---

## Iteration 4a: TODO Specification Audit

**Status:** PENDING (will execute after all tasks created)

**Audit Criteria:**
- Every task has: Requirement reference ✅
- Every task has: Acceptance criteria ✅
- Every task has: Implementation location ✅
- Every task has: Dependencies ✅
- Every task has: Tests ✅

---

## Summary

**Total Tasks:** 26
- Implementation tasks: 14 (Tasks 1-14)
- Test tasks: 12 (Tasks 15-26)

**Task Categories:**
- Module setup: 1 task
- Core function: 1 task
- Processing steps: 8 tasks (Tasks 3-10)
- Error handling: 3 tasks (Tasks 12-14)
- Testing: 12 tasks (Tasks 15-26)

**Estimated Complexity:** LOW-MODERATE
- All tasks well-defined from spec
- No ambiguous requirements
- Clear acceptance criteria for each task

**Dependencies:**
- External: utils.csv_utils, utils.error_handler, utils.LoggingManager
- Internal: Sequential (Tasks 3-11 build on Task 2)
- Tests: Depend on implementation tasks

**Next:** Iteration 2 - Component Dependency Mapping
