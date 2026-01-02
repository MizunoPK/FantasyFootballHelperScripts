# Feature 01: CSV Data Loading

## Objective

Parse and validate FantasyPros ADP CSV data, preparing it for player matching in Feature 2.

## Scope

**What's included in THIS feature:**
- Load CSV file: feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv
- Validate CSV file exists and has required columns
- Parse CSV data using existing utils/csv_utils.py utilities
- Extract critical columns: Player (name), POS (position), AVG (consensus ADP)
- Clean position strings (strip tier suffixes: "WR1" → "WR", "QB12" → "QB")
- Parse AVG column as float values
- Create efficient data structure for Feature 2 consumption
- Handle edge cases: empty Team fields, trailing spaces, position suffixes
- Return structured data with player_name, adp, position fields

**What's NOT included:**
- Player matching (Feature 2)
- Data updates to JSON files (Feature 2)
- Fuzzy matching logic (Feature 2)
- Team field validation (unreliable due to empty values)
- Individual platform rankings (ESPN, Sleeper, CBS, etc.) - not needed

## CSV File Details

**File:** `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv`

**Structure:**
- Total rows: 989 (1 header + 988 data rows)
- Total columns: 13
- Encoding: UTF-8
- Format: CSV with quoted fields

**Columns:**
1. Rank - Player ranking (1-988) - **NOT USED**
2. Player - Player name (e.g., "Ja'Marr Chase") - **CRITICAL**
3. Team - NFL team abbreviation (e.g., "CIN", "ATL") - **UNRELIABLE (has empty values)**
4. Bye - Bye week number (1-17) - **NOT USED (already in player data)**
5. POS - Position with tier (e.g., "WR1", "RB2", "TE1") - **USED (strip suffix)**
6. ESPN - ESPN ADP - **NOT USED**
7. Sleeper - Sleeper ADP - **NOT USED**
8. CBS - CBS ADP - **NOT USED**
9. NFL - NFL.com ADP - **NOT USED**
10. RTSports - RTSports ADP - **NOT USED**
11. Fantrax - Fantrax ADP - **NOT USED**
12. AVG - **CRITICAL: Consensus ADP (float)**
13. Real-Time - Real-time ranking - **NOT USED**

**Sample Data:**
```csv
"1","Ja'Marr Chase","CIN","10","WR1","1","1","1","1","1","1","1.0","1"
"2","Bijan Robinson","ATL","5","RB1","2","3","2","2","2","2","2.2","2"
"19","Brock Bowers","LV","8 ","TE1","20","20","24","17","21","18","20.0","22  -3"
```

## Edge Cases to Handle

1. **Empty Team Fields** - Some rows have empty Team values → Don't rely on Team field
2. **Trailing Spaces** - Bye column has trailing spaces (e.g., "8 ") → Ignore Bye column
3. **Position Tier Suffixes** - POS has suffixes (WR1, RB2, QB12) → Strip numeric suffix ✅ Confirmed
4. **Decimal ADP Values** - AVG is float (1.0, 2.2, 20.0) → Parse as float, not int
5. **Player Name Variations** - May have punctuation (St. Brown, Kenneth Walker III) → Pass through as-is (Feature 2 handles fuzzy matching)
6. **CSV Encoding** - Special characters possible → Use UTF-8 encoding

## Technical Approach

### Existing Utilities to Leverage

**File:** `utils/csv_utils.py`

**Functions:**
- `validate_csv_columns(filepath, required_columns)` - Validates required columns present
- `read_csv_with_validation(filepath, required_columns, encoding='utf-8')` - Reads CSV with validation

**Usage:**
```python
from utils.csv_utils import read_csv_with_validation

df = read_csv_with_validation(
    csv_path,
    required_columns=['Player', 'POS', 'AVG'],
    encoding='utf-8'
)
```

### Implementation Module

**New file to create:** `utils/adp_csv_loader.py`

**Primary function:**
```python
def load_adp_from_csv(csv_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load ADP data from FantasyPros CSV file.

    Args:
        csv_path: Path to CSV file

    Returns:
        DataFrame with columns: player_name, adp, position

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If required columns missing or data invalid
    """
```

### Processing Steps

1. Validate file exists (`Path.exists()`)
2. Validate required columns present: Player, POS, AVG
3. Read CSV using `read_csv_with_validation()`
4. Extract only needed columns: Player, POS, AVG
5. Clean position field: Strip numeric suffixes (WR1 → WR)
6. Parse AVG as float
7. Rename columns: Player → player_name, AVG → adp, POS → position
8. Validate all player_name values are non-empty
9. Validate all adp values are positive floats
10. Return DataFrame

### Output Data Structure

**Confirmed:** pandas DataFrame

**Columns:**
- `player_name` (str) - Player name from CSV
- `adp` (float) - Consensus ADP value
- `position` (str) - Clean position (QB, RB, WR, TE, K, DST)

**Example:**
```
   player_name       adp  position
0  Ja'Marr Chase     1.0  WR
1  Bijan Robinson    2.2  RB
2  Brock Bowers     20.0  TE
```

**Rationale:**
- Already using pandas for CSV reading
- Easy to filter/search for Feature 2
- Standard data science format
- Good performance for 988 rows

### Validation Requirements

**Pre-conditions:**
- CSV file must exist at specified path
- CSV must have columns: Player, POS, AVG
- CSV encoding must be UTF-8

**Post-conditions:**
- All rows have non-empty player_name
- All adp values are valid positive floats (>0) ✅ Validated
- All position values are 2-3 character strings (QB, RB, WR, TE, K, DST)
- Duplicate player names allowed (Feature 2 handles disambiguation) ✅ Confirmed

**Error Handling:**
- Fail fast on missing file (raise FileNotFoundError)
- Fail fast on missing columns (raise ValueError)
- Fail fast on invalid ADP values (raise ValueError if ADP <= 0) ✅ Confirmed

## Dependencies

**Prerequisites:** None (foundation feature)

**Blocks:** Feature 2 (Player Matching & Data Update needs clean CSV data structure)

**Python Modules:**
- `pandas` - CSV parsing (already in project)
- `pathlib.Path` - File operations (already in project)
- `utils.csv_utils` - CSV utilities (already in project)
- `utils.error_handler` - Error context managers (already in project)
- `utils.LoggingManager` - Logging (already in project)

**No new external dependencies required**

## Testing Strategy

### Test File Location

`tests/utils/test_adp_csv_loader.py` (mirrors source structure)

### Test Cases Required

1. **test_loads_csv_successfully** - Verify CSV loads and returns DataFrame
2. **test_validates_required_columns** - Verify required columns checked
3. **test_raises_error_when_file_missing** - FileNotFoundError when CSV doesn't exist
4. **test_raises_error_when_columns_missing** - ValueError when required columns missing
5. **test_strips_position_suffixes** - Verify WR1 → WR, QB12 → QB
6. **test_parses_adp_as_float** - Verify AVG column parsed as float
7. **test_handles_empty_team_field** - Verify empty Team doesn't cause errors
8. **test_output_has_correct_columns** - Verify player_name, adp, position columns
9. **test_validates_positive_adp_values** - Verify all ADP values are positive
10. **test_handles_player_name_variations** - Verify names with punctuation pass through

### Test Pattern

```python
@pytest.fixture
def test_csv_file(tmp_path):
    """Create test CSV with sample data"""
    csv_path = tmp_path / "test_adp.csv"
    csv_path.write_text(
        'Player,POS,AVG\n'
        '"Ja\'Marr Chase","WR1","1.0"\n'
        '"Bijan Robinson","RB2","2.2"\n'
    )
    return csv_path

def test_loads_csv_successfully(test_csv_file):
    # Arrange
    expected_count = 2

    # Act
    df = load_adp_from_csv(test_csv_file)

    # Assert
    assert len(df) == expected_count
    assert list(df.columns) == ['player_name', 'adp', 'position']
    assert df.iloc[0]['player_name'] == "Ja'Marr Chase"
    assert df.iloc[0]['adp'] == 1.0
    assert df.iloc[0]['position'] == 'WR'
```

## Technical Decisions ✅ All Confirmed

1. ✅ CSV file path passed as parameter (better testability)
2. ✅ Position suffixes stripped in Feature 1 (WR1→WR, QB12→QB)
3. ✅ Output structure: pandas DataFrame (player_name, adp, position)
4. ✅ Team field excluded from output (unreliable, not needed)
5. ✅ ADP values validated as positive floats (raise ValueError if <=0)
6. ✅ Duplicate player names allowed (Feature 2 handles disambiguation)

## Files Affected

**New files to create:**
- `utils/adp_csv_loader.py` - CSV loading module
- `tests/utils/test_adp_csv_loader.py` - Unit tests

**Existing files to read:**
- `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv` - Input data
- `utils/csv_utils.py` - Existing CSV utilities (leverage functions)

**No existing files modified** (this feature only loads and structures data)

## Complexity Assessment

- **Risk level:** LOW (standard CSV parsing, no external APIs)
- **Complexity:** LOW (straightforward data loading and cleaning)
- **Estimated scope items:** 15-20 (within Small feature threshold)
- **Dependencies:** None (foundation feature)

---

**Status:** Stage 2 Phase 3 complete (Interactive Questions - All decisions confirmed)
**Next:** Phase 4 - Dynamic Scope Adjustment, then Phase 5 - Cross-Feature Alignment
