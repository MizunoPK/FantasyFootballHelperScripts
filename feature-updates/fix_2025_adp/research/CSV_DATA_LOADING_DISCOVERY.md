# CSV Data Loading - Discovery Report

**Feature:** feature_01_csv_data_loading
**Date:** 2025-12-31
**Phase:** Stage 2 Phase 1 (Targeted Research)

---

## Components Identified

### CSV File Structure

**File:** `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv`

**Row Count:** 989 total rows (1 header + 988 data rows)

**Columns (13 total):**
1. Rank - Player ranking (1-988)
2. Player - Player name (e.g., "Ja'Marr Chase")
3. Team - NFL team abbreviation (e.g., "CIN", "ATL")
4. Bye - Bye week number (1-17, some with trailing spaces)
5. POS - Position with tier suffix (e.g., "WR1", "RB2", "TE1", "QB12")
6. ESPN - ESPN-specific ADP ranking
7. Sleeper - Sleeper-specific ADP ranking
8. CBS - CBS-specific ADP ranking
9. NFL - NFL.com-specific ADP ranking
10. RTSports - RTSports-specific ADP ranking
11. Fantrax - Fantrax-specific ADP ranking
12. AVG - **CRITICAL: Average ADP across all platforms (the value we need)**
13. Real-Time - Real-time ranking with trend indicators (e.g., "22  -3")

**Sample Data:**
```csv
"1","Ja'Marr Chase","CIN","10","WR1","1","1","1","1","1","1","1.0","1"
"2","Bijan Robinson","ATL","5","RB1","2","3","2","2","2","2","2.2","2"
"19","Brock Bowers","LV","8 ","TE1","20","20","24","17","21","18","20.0","22  -3"
```

### Existing Utilities Available

**File:** `utils/csv_utils.py`

**Functions to Leverage:**

1. `validate_csv_columns(filepath, required_columns) -> bool`
   - Validates CSV contains required columns
   - Uses error_context for structured logging
   - Fail-fast pattern if file doesn't exist
   - Returns True if all required columns present

2. `read_csv_with_validation(filepath, required_columns, encoding='utf-8') -> pd.DataFrame`
   - Reads CSV with optional column validation
   - Standardized error handling
   - Returns pandas DataFrame

**Usage Pattern:**
```python
from utils.csv_utils import read_csv_with_validation

df = read_csv_with_validation(
    csv_path,
    required_columns=['Player', 'POS', 'AVG'],
    encoding='utf-8'
)
```

### Data Processing Requirements

**Primary Field:** `AVG` column contains the consensus ADP value to extract

**Secondary Fields Needed:**
- `Player` - For matching to JSON player names
- `POS` - For validation (ensure position matches JSON data)
- `Team` - For additional validation (optional, has edge cases)

**Fields NOT Needed:**
- Individual platform rankings (ESPN, Sleeper, CBS, NFL, RTSports, Fantrax)
- Real-Time ranking
- Rank column (not needed for lookup)
- Bye week (already in player data)

---

## Interface Dependencies

### Input Dependency

**CSV File Location:** `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv`
- Fixed path (not configurable)
- 989 rows
- Must exist before running Feature 2

### Output Interface (for Feature 2)

Feature 2 (Player Matching & Data Update) will need:

1. **Data Structure:** Dictionary or DataFrame with:
   - Key: Player name (cleaned)
   - Value: AVG (ADP value)
   - Optional: POS (for validation)

2. **Example Structure:**
```python
# Option A: Dictionary
{
    "Ja'Marr Chase": {"adp": 1.0, "position": "WR"},
    "Bijan Robinson": {"adp": 2.2, "position": "RB"},
    "Brock Bowers": {"adp": 20.0, "position": "TE"}
}

# Option B: pandas DataFrame
#    player_name    adp  position
# 0  Ja'Marr Chase  1.0  WR
# 1  Bijan Robinson 2.2  RB
# 2  Brock Bowers   20.0 TE
```

### External Dependencies

**Python Modules:**
- `pandas` - For CSV parsing (already in project)
- `pathlib.Path` - For file operations
- `utils.csv_utils` - Existing CSV utilities
- `utils.error_handler` - Error handling context managers
- `utils.LoggingManager` - Logging

**No new dependencies required** - all modules already in project.

---

## Edge Cases Identified

### 1. Empty Team Fields

**Issue:** Some rows have empty Team field
**Example:** Row with Player but no Team value
**Impact:** Team validation cannot be used reliably
**Solution:** Don't require Team field for validation, treat as optional

### 2. Trailing Spaces in Bye Column

**Issue:** Bye column has trailing spaces (e.g., "8 " instead of "8")
**Example:** Row 19: "Brock Bowers","LV","8 ","TE1"
**Impact:** String parsing issues if bye week is used
**Solution:** Not using Bye column (already in player data), no action needed

### 3. Position Tier Suffixes

**Issue:** POS column includes tier numbers (e.g., "WR1", "RB2", "TE1", "QB12")
**Example:** "WR1" instead of "WR"
**Impact:** Need to strip numeric suffix for position matching
**Solution:**
```python
position = row['POS']
clean_position = ''.join([c for c in position if not c.isdigit()])
# "WR1" -> "WR"
# "QB12" -> "QB"
# "TE1" -> "TE"
```

### 4. Player Name Variations

**Issue:** Player names may have punctuation, spacing differences
**Examples:**
- "St. Brown" vs "St Brown"
- "Kenneth Walker III" vs "Kenneth Walker"
- Punctuation variations

**Impact:** Direct string matching will fail
**Solution:** Feature 2 handles this with fuzzy matching (not this feature's concern)

### 5. Decimal vs Integer ADP Values

**Issue:** AVG column contains decimal values (e.g., "1.0", "2.2", "20.0")
**Example:** "1.0" vs "20.0"
**Impact:** Must parse as float, not int
**Solution:**
```python
adp_value = float(row['AVG'])
```

### 6. CSV Encoding

**Issue:** CSV may have encoding issues with special characters
**Example:** Player names with accents, apostrophes
**Impact:** UnicodeDecodeError if wrong encoding
**Solution:** Use utf-8 encoding (already default in csv_utils.py)

### 7. Duplicate Player Names

**Issue:** Multiple players might have same name (unlikely but possible)
**Example:** Two "Mike Williams" (different teams)
**Impact:** Ambiguous matching in Feature 2
**Solution:** Feature 2 can use Team field as tiebreaker (not this feature's concern)

---

## Existing Test Patterns

### Test File Location
Will create: `tests/PLACEHOLDER_feature_01_csv_data_loading/test_csv_data_loading.py`

**Note:** Test folder name is PLACEHOLDER until implementation creates actual module.

### Test Patterns to Follow

**From existing test files (utils/test_csv_utils.py pattern):**

1. **Use tmp_path fixture for test data:**
```python
@pytest.fixture
def test_csv_file(tmp_path):
    csv_path = tmp_path / "test_adp.csv"
    csv_path.write_text(
        "Player,POS,AVG\n"
        "Ja'Marr Chase,WR1,1.0\n"
        "Bijan Robinson,RB1,2.2\n"
    )
    return csv_path
```

2. **Mock file operations where needed:**
```python
@patch('pathlib.Path.exists')
def test_file_not_found(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(FileNotFoundError):
        load_csv_data(Path("nonexistent.csv"))
```

3. **Test edge cases explicitly:**
```python
def test_handles_position_suffixes():
    """Test that position suffixes (WR1, RB2) are stripped correctly"""

def test_handles_empty_team_field():
    """Test that empty Team field doesn't cause errors"""

def test_parses_decimal_adp_values():
    """Test that AVG column is parsed as float"""
```

4. **Use AAA pattern (Arrange, Act, Assert):**
```python
def test_loads_csv_successfully(test_csv_file):
    # Arrange
    expected_count = 2

    # Act
    data = load_csv_data(test_csv_file)

    # Assert
    assert len(data) == expected_count
    assert "Ja'Marr Chase" in data
```

### Required Test Coverage

**Must test:**
- ✅ CSV file loads successfully
- ✅ Required columns validated (Player, POS, AVG)
- ✅ Player names extracted correctly
- ✅ AVG values parsed as float
- ✅ Position suffixes stripped (WR1 -> WR)
- ✅ Empty Team field handled gracefully
- ✅ FileNotFoundError when CSV missing
- ✅ ValueError when required columns missing
- ✅ Data structure returned matches expected format

---

## Technical Decisions Needed (For Checklist)

### Decision 1: Return Data Structure

**Question:** What data structure should be returned for Feature 2?

**Options:**
A. Dictionary: `{player_name: {"adp": float, "position": str}}`
B. pandas DataFrame with columns: player_name, adp, position
C. List of tuples: `[(player_name, adp, position), ...]`
D. Custom dataclass/NamedTuple

**Recommendation:** Option B (DataFrame) - already using pandas, easy to filter/search

### Decision 2: Position Suffix Handling

**Question:** Should position suffixes be stripped in this feature or Feature 2?

**Options:**
A. Strip here (return clean "WR", "RB" positions)
B. Keep raw values, let Feature 2 handle it
C. Return both (raw and clean)

**Recommendation:** Option A - cleaner interface for Feature 2

### Decision 3: Empty Team Field Handling

**Question:** How should empty Team fields be handled?

**Options:**
A. Skip rows with empty Team
B. Use None or "" for Team
C. Don't include Team in output at all

**Recommendation:** Option C - Team field unreliable, don't expose it

### Decision 4: File Path

**Question:** Should CSV file path be hardcoded or configurable?

**Options:**
A. Hardcoded: `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv`
B. Configurable parameter
C. Read from config file

**Recommendation:** Option B - more testable and flexible

### Decision 5: Error Handling

**Question:** What should happen if CSV is malformed?

**Options:**
A. Raise exception immediately (fail fast)
B. Log warning and skip bad rows
C. Return partial data with error list

**Recommendation:** Option A - fail fast, data integrity critical

---

## Implementation Approach (Preliminary)

### Module Structure

**File to create:** `utils/adp_csv_loader.py` (or similar)

**Class/Function:**
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
        ValueError: If required columns missing
    """
```

### Processing Steps

1. **Validate file exists** (Path.exists())
2. **Validate required columns** (csv_utils.validate_csv_columns)
3. **Read CSV** (csv_utils.read_csv_with_validation or pd.read_csv)
4. **Extract columns:** Player, POS, AVG
5. **Clean position field:** Strip numeric suffixes
6. **Parse ADP as float**
7. **Create output DataFrame**
8. **Return to caller**

### Validation Strategy

**Pre-conditions:**
- CSV file must exist
- Required columns must be present: Player, POS, AVG

**Post-conditions:**
- All rows have non-empty player_name
- All adp values are valid floats
- All position values are 2-3 character strings (QB, RB, WR, TE, K, DST)

---

## Questions for User (Preliminary)

These will be asked ONE AT A TIME in Phase 3:

1. Should the CSV file path be hardcoded or passed as a parameter?
2. Should position suffixes (WR1, RB2) be stripped in this feature or in Feature 2?
3. What should be the output data structure (Dictionary, DataFrame, or other)?
4. Should empty Team fields cause the row to be skipped or should we continue without Team validation?
5. Should we validate that all ADP values are positive floats?

---

## Summary

**Complexity Assessment:** LOW
- Straightforward CSV parsing
- Existing utilities available
- No complex algorithms needed
- Well-defined input/output

**Risk Assessment:** LOW
- No external API calls
- No database operations
- Existing patterns to follow
- Good test coverage possible

**Estimated Scope Items:** 15-20 (within Small feature threshold)

**Ready for Phase 2:** YES - sufficient research completed
