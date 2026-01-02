# Stage 3: Cross-Feature Sanity Check

**Date:** 2025-12-31
**Epic:** fix_2025_adp
**Features Compared:** 2 (feature_01_csv_data_loading, feature_02_player_matching_update)

---

## Comparison Matrix

### Category 1: Data Structures

#### Feature 1 (CSV Data Loading)

**Input:**
- CSV file: `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv`
- 988 rows (players)
- Columns used: Player, POS, AVG

**Output:**
- pandas DataFrame
- Columns: `player_name` (str), `adp` (float), `position` (str)
- Clean positions: QB, RB, WR, TE, K, DST (suffixes stripped)
- ADP values: positive floats (validated >0)
- Example:
  ```
     player_name       adp  position
  0  Ja'Marr Chase     1.0  WR
  1  Bijan Robinson    2.2  RB
  ```

**Internal Data Structures:**
- None (simple transformation pipeline)

#### Feature 2 (Player Matching & Data Update)

**Input:**
- pandas DataFrame from Feature 1 (player_name, adp, position)
- JSON files from `data/player_data/`:
  - qb_data.json (100 players)
  - rb_data.json (168 players)
  - wr_data.json (254 players)
  - te_data.json (147 players)
  - k_data.json (38 players)
  - dst_data.json (32 players)
  - Total: 739 players

**Output:**
- Updated JSON files (same structure, ADP values changed)
- Match report dictionary:
  ```python
  {
      'summary': {
          'total_json_players': 739,
          'matched': 650,
          'unmatched_json': 89,
          'unmatched_csv': 338
      },
      'unmatched_json_players': [...],
      'unmatched_csv_players': [...],
      'confidence_distribution': {...},
      'individual_matches': [...]
  }
  ```

**Internal Data Structures:**
- Match tracking dictionaries
- Confidence score mappings
- Position-filtered player lists

#### ✅ ALIGNMENT CHECK: Data Structures

**Feature 1 Output → Feature 2 Input:**
- ✅ DataFrame structure matches exactly
- ✅ Column names match: player_name, adp, position
- ✅ Data types match: str, float, str
- ✅ Position values match: QB, RB, WR, TE, K, DST (Feature 1 strips suffixes)
- ✅ ADP validation matches: Feature 1 validates >0, Feature 2 expects positive floats

**Conflicts:** NONE

---

### Category 2: Interfaces & Dependencies

#### Feature 1 (CSV Data Loading)

**Public Interface:**
```python
# utils/adp_csv_loader.py
def load_adp_from_csv(csv_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load ADP data from FantasyPros CSV file.

    Returns:
        DataFrame with columns: player_name, adp, position

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If required columns missing or data invalid
    """
```

**Dependencies:**
- pandas (existing)
- pathlib.Path (existing)
- utils.csv_utils (existing)
- utils.error_handler (existing)
- utils.LoggingManager (existing)

**Blocks:** Feature 2 (provides CSV DataFrame)

**Blocked By:** None (foundation feature)

#### Feature 2 (Player Matching & Data Update)

**Public Interface:**
```python
# utils/adp_updater.py
def update_player_adp_values(
    adp_dataframe: pd.DataFrame,
    data_folder: Union[str, Path]
) -> Dict[str, Any]:
    """
    Match CSV players to JSON players and update ADP values.

    Args:
        adp_dataframe: DataFrame from Feature 1 (player_name, adp, position)
        data_folder: Path to data/ folder containing player_data/

    Returns:
        Match report dictionary with summary, unmatched lists, confidence distribution

    Raises:
        ValueError: If DataFrame is empty or has wrong columns
        FileNotFoundError: If data_folder/player_data/ doesn't exist
        PermissionError: If JSON files can't be written
    """
```

**Dependencies:**
- pandas (existing)
- pathlib.Path (existing)
- json (standard library)
- difflib.SequenceMatcher (standard library)
- utils.error_handler (existing)
- utils.LoggingManager (existing)
- **Depends on Feature 1 output** (adp_dataframe parameter)

**Blocks:** None (final feature)

**Blocked By:** Feature 1 (needs CSV DataFrame)

#### ✅ ALIGNMENT CHECK: Interfaces & Dependencies

**Integration Point (Feature 1 → Feature 2):**
```python
# Expected usage pattern:
from utils.adp_csv_loader import load_adp_from_csv
from utils.adp_updater import update_player_adp_values

# Feature 1: Load CSV
csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')
adp_df = load_adp_from_csv(csv_path)

# Feature 2: Update JSON files
data_folder = Path('data')
report = update_player_adp_values(adp_df, data_folder)
```

**Interface Compatibility:**
- ✅ Feature 1 returns `pd.DataFrame` → Feature 2 expects `pd.DataFrame`
- ✅ Column names match exactly (player_name, adp, position)
- ✅ Data types compatible (str, float, str)
- ✅ Error handling compatible (both use utils.error_handler)
- ✅ Logging compatible (both use utils.LoggingManager)

**Dependency Chain:**
- ✅ Feature 1 has no dependencies (foundation)
- ✅ Feature 2 depends only on Feature 1 output (clear chain)
- ✅ No circular dependencies
- ✅ No shared mutable state

**Conflicts:** NONE

---

### Category 3: File Locations & Naming

#### Feature 1 (CSV Data Loading)

**New Files to Create:**
- `utils/adp_csv_loader.py` - Main module
- `tests/utils/test_adp_csv_loader.py` - Unit tests

**Files to Read:**
- `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv` - Input CSV
- `utils/csv_utils.py` - Existing utilities (read only)

**Files Modified:** NONE

#### Feature 2 (Player Matching & Data Update)

**New Files to Create:**
- `utils/adp_updater.py` - Main module
- `tests/utils/test_adp_updater.py` - Unit tests

**Files to Read:**
- `data/player_data/qb_data.json` - Player data
- `data/player_data/rb_data.json` - Player data
- `data/player_data/wr_data.json` - Player data
- `data/player_data/te_data.json` - Player data
- `data/player_data/k_data.json` - Player data
- `data/player_data/dst_data.json` - Player data
- `utils/DraftedRosterManager.py` - Fuzzy matching reference (read only)
- `league_helper/util/PlayerManager.py` - JSON I/O reference (read only)

**Files Modified:**
- `data/player_data/qb_data.json` - ADP updates
- `data/player_data/rb_data.json` - ADP updates
- `data/player_data/wr_data.json` - ADP updates
- `data/player_data/te_data.json` - ADP updates
- `data/player_data/k_data.json` - ADP updates
- `data/player_data/dst_data.json` - ADP updates

#### ✅ ALIGNMENT CHECK: File Locations & Naming

**Module Naming:**
- ✅ Feature 1: `adp_csv_loader.py` (describes purpose: CSV loading)
- ✅ Feature 2: `adp_updater.py` (describes purpose: ADP updates)
- ✅ Both in `utils/` folder (appropriate for shared utilities)
- ✅ No naming conflicts

**Test Naming:**
- ✅ Feature 1: `tests/utils/test_adp_csv_loader.py` (mirrors source)
- ✅ Feature 2: `tests/utils/test_adp_updater.py` (mirrors source)
- ✅ Both follow project convention (test_ prefix)
- ✅ No naming conflicts

**File Access Patterns:**
- ✅ Feature 1 reads CSV (read-only) → No conflicts
- ✅ Feature 2 reads/writes JSON (atomic writes) → No conflicts
- ✅ No overlapping file modifications
- ✅ No race conditions (sequential execution expected)

**Conflicts:** NONE

---

### Category 4: Configuration Keys

#### Feature 1 (CSV Data Loading)

**Configuration Used:** NONE

- No league_config.json keys
- No environment variables
- No command-line arguments
- CSV path passed as function parameter

#### Feature 2 (Player Matching & Data Update)

**Configuration Used:** NONE

- No league_config.json keys
- No environment variables
- No command-line arguments
- Confidence threshold hardcoded (0.75 from proven pattern)
- Data folder path passed as function parameter

#### ✅ ALIGNMENT CHECK: Configuration Keys

**Configuration Overlap:**
- ✅ No shared configuration keys
- ✅ No configuration conflicts
- ✅ Both features use parameters instead of config files (good for testability)

**Conflicts:** NONE

---

### Category 5: Algorithms & Logic

#### Feature 1 (CSV Data Loading)

**Algorithm:**
1. Validate file exists
2. Validate required columns: Player, POS, AVG
3. Read CSV using `read_csv_with_validation()`
4. Extract columns: Player, POS, AVG
5. Clean position: Strip numeric suffixes (regex: `r'\d+$'`)
   - WR1 → WR
   - QB12 → QB
   - RB2 → RB
6. Parse AVG as float
7. Rename columns: Player → player_name, AVG → adp, POS → position
8. Validate player_name non-empty
9. Validate adp > 0 (raise ValueError if <=0)
10. Return DataFrame

**Position Cleaning Logic:**
```python
# Remove trailing digits from position
df['position'] = df['POS'].str.replace(r'\d+$', '', regex=True)
```

**Validation Logic:**
```python
# Validate ADP values are positive
if (df['adp'] <= 0).any():
    raise ValueError("ADP values must be positive")
```

#### Feature 2 (Player Matching & Data Update)

**Algorithm:**
1. Load all JSON files (6 position files)
2. For each JSON player:
   a. Filter CSV DataFrame by position (exact match: QB, RB, WR, TE, K, DST)
   b. Normalize JSON player name (lowercase, strip suffixes, remove punctuation)
   c. For each CSV player in same position:
      - Normalize CSV player name
      - Calculate similarity score (difflib.SequenceMatcher.ratio())
   d. Select best match if score >= 0.75
   e. If matched: Update JSON player's `average_draft_position` field
   f. If not matched: Keep existing 170.0 value
3. Write updated JSON files (atomic write pattern)
4. Generate match report (summary, unmatched lists, confidence distribution, individual matches)
5. Log unmatched players (WARNING) and summary (INFO)
6. Return match report dictionary

**Name Normalization Logic:**
```python
def normalize_name(name: str) -> str:
    # Lowercase and collapse spaces
    normalized = re.sub(r'\s+', ' ', name.strip().lower())
    # Remove suffixes (Jr., Sr., III, IV)
    normalized = re.sub(r'\b(jr\.?|sr\.?|iii?|iv)\b', '', normalized)
    # Remove punctuation
    normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')
    return normalized.strip()
```

**Fuzzy Matching Logic:**
```python
def find_best_match(json_name: str, csv_players: List[str]) -> Optional[Tuple[str, float]]:
    normalized_json = normalize_name(json_name)
    best_match = None
    best_score = 0.0

    for csv_name in csv_players:
        normalized_csv = normalize_name(csv_name)
        score = SequenceMatcher(None, normalized_json, normalized_csv).ratio()
        if score > best_score:
            best_score = score
            best_match = csv_name

    if best_score >= 0.75:
        return (best_match, best_score)
    return None
```

**Atomic Write Pattern:**
```python
tmp_path = json_path.with_suffix('.tmp')
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2)
tmp_path.replace(json_path)  # Atomic replace
```

#### ✅ ALIGNMENT CHECK: Algorithms & Logic

**Position Handling:**
- ✅ Feature 1 strips suffixes: WR1 → WR, QB12 → QB
- ✅ Feature 2 expects clean positions: QB, RB, WR, TE, K, DST
- ✅ Position values match exactly after Feature 1 processing
- ✅ Feature 2 filters CSV by exact position match (no suffix handling needed)

**Data Validation:**
- ✅ Feature 1 validates ADP > 0 (raises ValueError if <=0)
- ✅ Feature 2 expects positive float ADP values
- ✅ No invalid ADP values can reach Feature 2

**Name Handling:**
- ✅ Feature 1 passes names through as-is (no normalization)
- ✅ Feature 2 handles normalization (punctuation, suffixes)
- ✅ Separation of concerns is correct (Feature 1 = load, Feature 2 = match)

**Error Handling:**
- ✅ Both use utils.error_handler
- ✅ Both use fail-fast approach
- ✅ Compatible exception types (FileNotFoundError, ValueError, PermissionError)

**Conflicts:** NONE

---

### Category 6: Testing Assumptions

#### Feature 1 (CSV Data Loading)

**Test Location:** `tests/utils/test_adp_csv_loader.py`

**Test Fixtures:**
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
```

**Test Cases (10 total):**
1. test_loads_csv_successfully
2. test_validates_required_columns
3. test_raises_error_when_file_missing
4. test_raises_error_when_columns_missing
5. test_strips_position_suffixes
6. test_parses_adp_as_float
7. test_handles_empty_team_field
8. test_output_has_correct_columns
9. test_validates_positive_adp_values
10. test_handles_player_name_variations

**Mocking Strategy:**
- Use tmp_path for test CSVs
- No mocking needed (pure data transformation)

#### Feature 2 (Player Matching & Data Update)

**Test Location:** `tests/utils/test_adp_updater.py`

**Test Fixtures:**
```python
@pytest.fixture
def test_adp_dataframe():
    """Create test DataFrame matching Feature 1 output"""
    return pd.DataFrame({
        'player_name': ['Patrick Mahomes', 'Christian McCaffrey'],
        'adp': [15.5, 2.0],
        'position': ['QB', 'RB']
    })

@pytest.fixture
def test_player_data_folder(tmp_path):
    """Create test JSON files with sample players"""
    data_folder = tmp_path / 'data'
    player_data_folder = data_folder / 'player_data'
    player_data_folder.mkdir(parents=True)

    # Create QB JSON
    qb_data = {
        'qb_data': [{
            'name': 'Patrick Mahomes II',
            'position': 'QB',
            'average_draft_position': 170.0
        }]
    }
    (player_data_folder / 'qb_data.json').write_text(json.dumps(qb_data, indent=2))

    return data_folder
```

**Test Cases (15 total):**
1. test_matches_players_successfully
2. test_updates_json_files
3. test_returns_match_report
4. test_handles_no_match_keeps_170
5. test_fuzzy_matching_with_name_variations
6. test_position_filtering
7. test_confidence_threshold_075
8. test_atomic_write_pattern
9. test_raises_error_empty_dataframe
10. test_raises_error_missing_data_folder
11. test_logs_unmatched_players
12. test_logs_summary
13. test_comprehensive_match_report
14. test_multiple_positions
15. test_best_match_selection

**Mocking Strategy:**
- Use tmp_path for test JSON files
- Use test DataFrame matching Feature 1 output structure
- Mock logging (verify WARNING for unmatched, INFO for summary)

#### ✅ ALIGNMENT CHECK: Testing Assumptions

**Integration Testing:**
- ✅ Feature 2 tests use DataFrame fixture matching Feature 1 output structure
- ✅ DataFrame columns match: player_name, adp, position
- ✅ Data types match: str, float, str
- ✅ Position values match: QB, RB, WR, TE, K, DST (clean, no suffixes)
- ✅ ADP values positive (Feature 1 validation ensures this)

**Test Data Consistency:**
- ✅ Both features use tmp_path for test files
- ✅ Both features use pytest fixtures
- ✅ No shared test data files (isolated tests)

**Mock Compatibility:**
- ✅ No conflicting mocks
- ✅ Both features mock logging independently
- ✅ Feature 2 doesn't need to mock Feature 1 (uses real DataFrame fixture)

**Integration Test Plan:**
```python
# tests/integration/test_fix_2025_adp_integration.py
def test_complete_adp_update_workflow(tmp_path):
    """Test Feature 1 → Feature 2 integration"""
    # Arrange: Create test CSV
    csv_path = tmp_path / 'test_adp.csv'
    # ... create CSV ...

    # Create test JSON files
    data_folder = tmp_path / 'data'
    # ... create JSON files ...

    # Act: Feature 1
    adp_df = load_adp_from_csv(csv_path)

    # Act: Feature 2
    report = update_player_adp_values(adp_df, data_folder)

    # Assert: Verify integration
    assert len(adp_df) > 0
    assert report['summary']['matched'] > 0
    # ... verify JSON files updated ...
```

**Conflicts:** NONE

---

## Summary of Findings

### Total Features Compared: 2

**Feature 1 (CSV Data Loading):**
- Scope: 14 items
- Complexity: LOW
- Dependencies: None (foundation)

**Feature 2 (Player Matching & Data Update):**
- Scope: 17 items
- Complexity: LOW-MODERATE
- Dependencies: Feature 1 output (DataFrame)

### Categories Analyzed: 6

1. ✅ Data Structures - ALIGNED
2. ✅ Interfaces & Dependencies - ALIGNED
3. ✅ File Locations & Naming - ALIGNED
4. ✅ Configuration Keys - ALIGNED
5. ✅ Algorithms & Logic - ALIGNED
6. ✅ Testing Assumptions - ALIGNED

### Total Conflicts Found: 0

### Integration Points Verified: 1

**Feature 1 → Feature 2 (CSV DataFrame):**
- ✅ DataFrame structure matches exactly
- ✅ Column names match: player_name, adp, position
- ✅ Data types match: str, float, str
- ✅ Position values match: QB, RB, WR, TE, K, DST
- ✅ ADP validation compatible: >0
- ✅ Error handling compatible
- ✅ Logging compatible

---

## Conflict Resolution

**Status:** N/A (No conflicts found)

All features are fully aligned. No resolution steps required.

---

## Validation Checklist

**Pre-Comparison:**
- [x] Both features completed Stage 2
- [x] All feature specs complete
- [x] All feature checklists resolved
- [x] Research documents available

**During Comparison:**
- [x] Compared Data Structures (Category 1)
- [x] Compared Interfaces & Dependencies (Category 2)
- [x] Compared File Locations & Naming (Category 3)
- [x] Compared Configuration Keys (Category 4)
- [x] Compared Algorithms & Logic (Category 5)
- [x] Compared Testing Assumptions (Category 6)

**Post-Comparison:**
- [x] All conflicts documented (0 found)
- [x] Integration points identified (1 found)
- [x] Integration compatibility verified
- [ ] User sign-off obtained (PENDING)

---

## Recommendations

### Epic Implementation Order

**Recommended:** Sequential (Feature 1 → Feature 2)

**Rationale:**
- Feature 2 depends on Feature 1 output
- Clear dependency chain
- No parallel work possible

**Implementation Plan:**
1. Implement Feature 1 (CSV Data Loading) - Stages 5a→5b→5c→5d→5e
2. Implement Feature 2 (Player Matching & Data Update) - Stages 5a→5b→5c→5d→5e
3. Epic Final QC (Stage 6)
4. Epic Cleanup (Stage 7)

### Integration Testing Strategy

**Create integration test:** `tests/integration/test_fix_2025_adp_integration.py`

**Test Coverage:**
- Feature 1 → Feature 2 data flow
- Complete CSV → JSON update workflow
- End-to-end validation (verify actual JSON updates)

**Test Scenarios:**
- Normal case: CSV loads, players match, JSON updates
- Edge case: No matches found, 170.0 values retained
- Edge case: Partial matches, some updated, some not
- Error case: Missing CSV, missing JSON files, permission errors

### Risk Assessment

**Overall Risk Level:** LOW

**Risks Identified:**
1. **File Permissions** - JSON files might not be writable
   - Mitigation: PermissionError propagates, atomic writes prevent corruption
2. **CSV Format Changes** - FantasyPros might change CSV structure
   - Mitigation: Column validation catches this immediately
3. **Name Variations** - Some players might not match
   - Mitigation: 0.75 threshold proven, unmatched players keep 170.0 (safe fallback)

**No blocking risks identified**

---

## Next Steps

**Stage 3 Status:** ✅ Comparison complete, no conflicts found

**Ready for User Sign-Off:** YES

**After User Approval:**
1. Mark Stage 3 complete in EPIC_README.md
2. Proceed to Stage 4 (Epic Testing Strategy)
3. Update epic_smoke_test_plan.md based on findings
4. Begin Stage 5 implementation (Feature 1 first)

---

**Comparison completed by:** Claude Sonnet 4.5
**Date:** 2025-12-31
**Time spent:** Systematic analysis across 6 categories
**Confidence level:** HIGH (all specs reviewed, no ambiguities found)
