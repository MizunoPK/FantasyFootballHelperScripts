# Feature 02: Player Matching & Data Update

## Objective

Match CSV players to existing player data using fuzzy matching and update ADP values in JSON files.

## Scope

**What's included in THIS feature:**
- Load DataFrame from Feature 1 (player_name, adp, position)
- Load 6 player data JSON files (739 total players)
- Fuzzy match JSON players to CSV players (within same position)
- Adapt fuzzy matching logic from utils/DraftedRosterManager.py
- Update `average_draft_position` field for matched players (>= 0.75 confidence)
- Preserve all other JSON fields unchanged
- Write updated JSON files using atomic write pattern
- Generate comprehensive match report
- Handle edge cases: name variations, multiple matches, no matches

**What's NOT included:**
- CSV parsing and data loading (Feature 1)
- Creating new player entries (only update existing)
- Changing any fields besides `average_draft_position`
- Team field validation (unreliable in CSV)

## Feature 1 Interface (Input)

**From Feature 1 (CSV Data Loading):**

pandas DataFrame with structure:
```
   player_name       adp  position
0  Ja'Marr Chase     1.0  WR
1  Bijan Robinson    2.2  RB
2  Brock Bowers     20.0  TE
```

**Columns:**
- `player_name` (str) - Player name from CSV
- `adp` (float) - Consensus ADP value (validated >0)
- `position` (str) - Clean position (QB, RB, WR, TE, K, DST)

**Row count:** 988 (from CSV)

**Source:** Feature 1's `load_adp_from_csv()` function

## Player Data JSON Files (Target)

**Location:** `data/player_data/*.json`

**Files (6 total):**
- `qb_data.json` - 100 players
- `rb_data.json` - 168 players
- `wr_data.json` - 254 players
- `te_data.json` - 147 players
- `k_data.json` - 38 players
- `dst_data.json` - 32 players

**Total:** 739 players

**JSON Structure:**
```json
{
  "qb_data": [
    {
      "id": "3918298",
      "name": "Josh Allen",
      "team": "BUF",
      "position": "QB",
      "bye_week": 7,
      "injury_status": "QUESTIONABLE",
      "drafted_by": "The Injury Report",
      "locked": false,
      "average_draft_position": 170.0,  // <-- UPDATE THIS FIELD
      "player_rating": 93.46700507614213,
      "projected_points": [...],
      "actual_points": [...]
    }
  ]
}
```

**Field to Update:** `average_draft_position`
**Fields to Preserve:** ALL other fields unchanged

## Fuzzy Matching Approach

### Existing Logic to Adapt

**Source:** `utils/DraftedRosterManager.py`

**Key components to reuse:**

1. **Similarity Scoring (lines 440-442):**
```python
from difflib import SequenceMatcher

def _similarity_score(self, s1: str, s2: str) -> float:
    """Calculate similarity score between two strings (0.0 to 1.0)."""
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
```

2. **Name Normalization (lines 341-373):**
```python
def _normalize_player_info(self, player_info: str) -> str:
    """Normalize player info string for consistent matching."""
    # Lowercase, collapse spaces
    normalized = re.sub(r'\s+', ' ', player_info.strip().lower())

    # Remove suffixes (Jr., Sr., III, IV)
    normalized = re.sub(r'\b(jr\.?|sr\.?|iii?|iv)\b', '', normalized)

    # Normalize punctuation (St. -> St, O'Dell -> ODell, Amon-Ra -> Amon Ra)
    normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')

    # Clean up spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized
```

3. **Confidence Threshold:** 0.75 (proven from existing code)

### Matching Algorithm

**For each JSON player:**

1. **Filter CSV by position** (only compare within same position)
2. **Normalize names** (JSON player name and CSV player names)
3. **Calculate similarity scores** for all CSV players in same position
4. **Select best match** if score >= 0.75
5. **Update JSON player** with matched ADP value
6. **Track match** for reporting

**Pseudocode:**
```python
def find_best_match(json_player_name: str, csv_df: pd.DataFrame, position: str) -> Tuple[Optional[float], float]:
    """
    Find best matching CSV player for JSON player.

    Args:
        json_player_name: Name from JSON player
        csv_df: DataFrame from Feature 1
        position: Player position to filter by

    Returns:
        Tuple of (adp_value, confidence_score) or (None, 0.0) if no match
    """
    best_score = 0.0
    best_adp = None

    # Filter CSV by position
    position_df = csv_df[csv_df['position'] == position]

    # Normalize JSON player name
    json_normalized = normalize_name(json_player_name)

    # Check each CSV player in same position
    for idx, row in position_df.iterrows():
        csv_normalized = normalize_name(row['player_name'])
        score = similarity_score(json_normalized, csv_normalized)

        if score >= 0.75 and score > best_score:
            best_score = score
            best_adp = row['adp']

    return (best_adp, best_score)
```

## JSON I/O Pattern

### Reading JSON Files

**Pattern from PlayerManager (lines 350-356):**
```python
with open(filepath, 'r') as f:
    json_data = json.load(f)

position_key = position_file.replace('.json', '')  # "qb_data"
players_array = json_data.get(position_key, [])
```

### Writing JSON Files (Atomic Pattern)

**Pattern from PlayerManager (lines 554-562):**
```python
# Wrap array back in object with position key
json_data_to_write = {position_key: players_array}

# Write to temp file first
tmp_path = json_path.with_suffix('.tmp')
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(json_data_to_write, f, indent=2)

# Atomic replace (overwrites existing .json file)
tmp_path.replace(json_path)
```

**Why atomic writes?**
- Prevents corruption if program crashes during write
- Either old file exists or new file exists (never half-written file)
- Standard pattern in existing codebase

## Processing Flow

**Main workflow:**

1. **Load CSV DataFrame** from Feature 1
2. **Validate inputs:**
   - DataFrame not empty
   - player_data/ directory exists
3. **For each position file** (6 files):
   - Load JSON file
   - Extract players array
   - **For each JSON player:**
     - Find best CSV match (within same position)
     - If match confidence >= 0.75:
       - Update `average_draft_position` with CSV adp
       - Track match (name, confidence, old_adp, new_adp)
     - Else (no match):
       - Keep existing 170.0 value
       - Track as unmatched (name, position)
   - Write updated JSON (atomic pattern)
4. **Generate match report**
5. **Return report to caller**

## Implementation Module

**New file to create:** `utils/adp_updater.py`

**Primary function:**
```python
def update_adp_from_csv(
    csv_dataframe: pd.DataFrame,
    data_folder: Union[str, Path]
) -> Dict[str, Any]:
    """
    Update player data JSON files with ADP values from CSV DataFrame.

    Args:
        csv_dataframe: DataFrame from Feature 1 (player_name, adp, position)
        data_folder: Path to data folder containing player_data/ directory

    Returns:
        Dict with match report:
        {
            'total_json_players': int,
            'matched_count': int,
            'unmatched_json_count': int,
            'unmatched_json_players': List[Dict[str, str]],
            'match_confidence_distribution': Dict[str, int],
            'files_updated': List[str],
            'matches': List[Dict]  # Individual match details
        }

    Raises:
        FileNotFoundError: If player_data directory doesn't exist
        ValueError: If CSV DataFrame is empty or invalid
        PermissionError: If cannot write to JSON files
    """
```

**Helper functions:**
```python
def normalize_name(name: str) -> str:
    """
    Normalize player name for matching.
    Adapted from DraftedRosterManager._normalize_player_info().
    """

def similarity_score(s1: str, s2: str) -> float:
    """
    Calculate string similarity 0.0-1.0.
    From DraftedRosterManager._similarity_score().
    """

def find_best_match(
    json_player_name: str,
    csv_df: pd.DataFrame,
    position: str
) -> Tuple[Optional[float], float]:
    """
    Find best matching CSV player for JSON player within same position.
    Returns (adp_value, confidence_score) or (None, 0.0).
    """

def update_position_file(
    position_file: str,
    csv_df: pd.DataFrame,
    player_data_dir: Path
) -> Dict:
    """
    Update single position JSON file with ADP values.
    Returns match statistics for this position.
    """
```

## Edge Cases to Handle

1. **Name Variations:**
   - "Amon-Ra St. Brown" vs "Amon Ra St Brown" (punctuation)
   - "Kenneth Walker III" vs "Kenneth Walker" (suffix)
   - "AJ Brown" vs "A.J. Brown" (initials)
   - **Solution:** normalize_name() handles all these

2. **Multiple Matches Above Threshold:**
   - Two CSV players match JSON player with score >= 0.75
   - **Solution:** Use highest confidence score (best_score pattern)

3. **Position Equivalency:**
   - CSV and JSON might use different defense position names
   - **Solution:** Both use "DST" (Feature 1 normalized positions)

4. **Defense Name Formats:**
   - CSV: "Seattle Seahawks", JSON: "Seahawks D/ST"
   - **Solution:** Fuzzy matching handles variations

5. **No Match Found:**
   - JSON player not in CSV top 988 (e.g., backup RB)
   - **Solution:** Keep existing 170.0 value, track in unmatched list

6. **CSV Player Not in JSON:**
   - CSV player not in our JSON files (expected)
   - **Solution:** Ignore (this is OK and expected)

7. **Empty CSV DataFrame:**
   - Feature 1 returns empty DataFrame (load failed)
   - **Solution:** Raise ValueError with clear message

8. **Missing player_data Directory:**
   - data/player_data/ doesn't exist
   - **Solution:** Raise FileNotFoundError with helpful message

9. **File Permission Errors:**
   - Cannot write to JSON files
   - **Solution:** Let PermissionError propagate with error message

10. **JSON File Corruption:**
    - Program crashes during write
    - **Solution:** Atomic write pattern prevents corruption

## Match Report Structure

**Confirmed:** Comprehensive report with all details
```python
{
    'total_json_players': 739,
    'matched_count': 650,
    'unmatched_json_count': 89,
    'unmatched_json_players': [
        {'name': 'Backup RB', 'position': 'RB'},
        {'name': 'Third String QB', 'position': 'QB'}
    ],
    'match_confidence_distribution': {
        '1.00': 400,           # Exact matches
        '0.90-0.99': 180,      # Very close
        '0.75-0.89': 70        # Good match
    },
    'files_updated': [
        'qb_data.json',
        'rb_data.json',
        'wr_data.json',
        'te_data.json',
        'k_data.json',
        'dst_data.json'
    ],
    'matches': [  # Individual match details (for debugging)
        {
            'json_name': 'Josh Allen',
            'csv_name': 'Josh Allen',
            'position': 'QB',
            'confidence': 1.0,
            'old_adp': 170.0,
            'new_adp': 5.0
        }
    ]
}
```

**Rationale:**
- Summary stats for quick overview
- Unmatched list for verification
- Confidence distribution shows match quality
- Individual matches for detailed analysis/debugging

## Expected Results

**Match Rate Predictions:**
- CSV players: 988
- JSON players: 739
- Expected matched: ~500-700 (most JSON players should match)
- Expected unmatched JSON: ~50-100 (some JSON players not in CSV top 988)
- Expected unmatched CSV: ~300-400 (CSV has players not in our JSON)

**Unmatched JSON players are expected:**
- Backup players not ranked in top 988
- Players added to JSON but not in FantasyPros rankings
- These keep their 170.0 placeholder value

**Unmatched CSV players are expected and OK:**
- CSV has all 988 ranked players
- Our JSON only has 739 players we care about
- We don't need to update players we don't have

## Dependencies

**Prerequisites:**
- Feature 1 (CSV Data Loading) - MUST be complete
- Existing player data JSON files - must exist

**Python Modules:**
- `pandas` - DataFrame from Feature 1 (already in project)
- `json` - JSON I/O (standard library)
- `difflib.SequenceMatcher` - Fuzzy matching (standard library)
- `re` - Name normalization (standard library)
- `pathlib.Path` - File operations (standard library)
- `typing` - Type hints (standard library)
- `utils.LoggingManager` - Logging (already in project)

**No new external dependencies required**

## Testing Strategy

### Test File Location

`tests/utils/test_adp_updater.py` (mirrors source structure)

### Test Cases Required

1. **test_loads_csv_dataframe_successfully** - Verify DataFrame loaded
2. **test_loads_json_files_successfully** - Verify all 6 JSON files loaded
3. **test_finds_exact_match** - Confidence = 1.0 for identical names
4. **test_finds_similar_match** - Confidence >= 0.75 for similar names
5. **test_handles_punctuation_differences** - "St. Brown" vs "St Brown"
6. **test_handles_name_suffix_differences** - "Kenneth Walker III" vs "Kenneth Walker"
7. **test_position_filtering** - Only matches within same position
8. **test_multiple_matches_chooses_best** - Highest confidence wins
9. **test_no_match_keeps_170** - Unmatched players keep placeholder
10. **test_atomic_write_pattern** - .tmp file created then replaced
11. **test_preserves_other_fields** - Only average_draft_position changes
12. **test_match_report_generated** - Report structure correct
13. **test_raises_error_when_directory_missing** - FileNotFoundError
14. **test_raises_error_when_dataframe_empty** - ValueError
15. **test_handles_permission_error** - PermissionError gracefully

### Test Pattern

```python
import pytest
import pandas as pd
import json
from pathlib import Path

@pytest.fixture
def test_player_data(tmp_path):
    """Create test player data JSON files"""
    player_data_dir = tmp_path / "player_data"
    player_data_dir.mkdir()

    # Create qb_data.json
    qb_data = {
        "qb_data": [
            {
                "id": "1",
                "name": "Josh Allen",
                "team": "BUF",
                "position": "QB",
                "bye_week": 7,
                "average_draft_position": 170.0,
                "player_rating": 95.0,
                "projected_points": [20.0] * 17,
                "actual_points": [18.0] * 17
            }
        ]
    }
    (player_data_dir / "qb_data.json").write_text(json.dumps(qb_data, indent=2))

    return tmp_path

@pytest.fixture
def csv_dataframe():
    """Create test CSV DataFrame from Feature 1"""
    return pd.DataFrame({
        'player_name': ['Josh Allen', 'Patrick Mahomes'],
        'adp': [5.0, 8.0],
        'position': ['QB', 'QB']
    })

def test_finds_exact_match(test_player_data, csv_dataframe):
    # Arrange
    expected_new_adp = 5.0

    # Act
    report = update_adp_from_csv(csv_dataframe, test_player_data)

    # Assert
    assert report['matched_count'] == 1
    assert report['matches'][0]['new_adp'] == expected_new_adp
    assert report['matches'][0]['confidence'] == 1.0

    # Verify JSON was updated
    qb_json = json.loads((test_player_data / "player_data" / "qb_data.json").read_text())
    assert qb_json['qb_data'][0]['average_draft_position'] == 5.0
    assert qb_json['qb_data'][0]['name'] == 'Josh Allen'  # Other fields preserved
```

## Open Questions (See checklist.md)

1. Should we use 0.75 as the confidence threshold?
2. What should happen if JSON player has no CSV match? (keep 170.0 or other)
3. What level of detail should match report include?
4. Should we log every match or just summaries?
5. Should there be a dry-run mode?
6. Should we create backup files before updating?
7. What format should the match report be (dict, file, JSON, etc.)?

## Files Affected

**New files to create:**
- `utils/adp_updater.py` - Main matching and updating module
- `tests/utils/test_adp_updater.py` - Unit tests

**Existing files to read:**
- `utils/DraftedRosterManager.py` - Adapt fuzzy matching logic
- `league_helper/util/PlayerManager.py` - Reference JSON I/O patterns
- `data/player_data/qb_data.json` - Read and update
- `data/player_data/rb_data.json` - Read and update
- `data/player_data/wr_data.json` - Read and update
- `data/player_data/te_data.json` - Read and update
- `data/player_data/k_data.json` - Read and update
- `data/player_data/dst_data.json` - Read and update

**No existing files modified** (only read for patterns, update player data files)

## Complexity Assessment

- **Risk level:** MODERATE (fuzzy matching, file updates)
- **Complexity:** MODERATE (more complex than Feature 1)
- **Estimated scope items:** 25-30 (within Medium feature threshold)
- **Dependencies:** Feature 1 (must be complete)

---

**Status:** Stage 2 COMPLETE - All 5 phases done (2025-12-31)
**Next:** Stage 3 (Cross-Feature Sanity Check) - after both features complete Stage 2
