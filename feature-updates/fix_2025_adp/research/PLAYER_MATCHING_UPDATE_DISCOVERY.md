# Player Matching & Data Update - Discovery Report

**Feature:** feature_02_player_matching_update
**Date:** 2025-12-31
**Phase:** Stage 2 Phase 1 (Targeted Research)

---

## Components Identified

### Feature 1 Interface (Input)

**From Feature 1 (CSV Data Loading):**
- pandas DataFrame with columns: `player_name`, `adp`, `position`
- 988 rows from CSV
- Positions cleaned (WR, RB, TE, QB, K, DST - no suffixes)
- ADP values validated (positive floats)

**Example:**
```
   player_name       adp  position
0  Ja'Marr Chase     1.0  WR
1  Bijan Robinson    2.2  RB
2  Brock Bowers     20.0  TE
```

### Player Data JSON Files (Target to Update)

**Location:** `data/player_data/*.json`

**Files (6 total):**
1. `qb_data.json` - 100 players
2. `rb_data.json` - 168 players
3. `wr_data.json` - 254 players
4. `te_data.json` - 147 players
5. `k_data.json` - 38 players
6. `dst_data.json` - 32 players

**Total:** 739 players in JSON files

**Structure:**
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
      "average_draft_position": 170.0,  // <-- FIELD TO UPDATE
      "player_rating": 93.46700507614213,
      "projected_points": [...],
      "actual_points": [...]
    }
  ]
}
```

**Field to Update:** `average_draft_position` (currently 170.0 placeholder)

**Fields to Preserve:** All other fields must remain unchanged

### Existing Fuzzy Matching Logic

**File:** `utils/DraftedRosterManager.py`

**Key Components Available:**

1. **Similarity Scoring (lines 440-442):**
```python
def _similarity_score(self, s1: str, s2: str) -> float:
    """Calculate similarity score between two strings (0.0 to 1.0)."""
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
```
- Uses `difflib.SequenceMatcher`
- Returns float 0.0 to 1.0
- **Threshold used: 0.75** (good balance of accuracy and recall)

2. **Normalization Logic (lines 341-373):**
```python
def _normalize_player_info(self, player_info: str) -> str:
    """Normalize player info string for consistent matching."""
    # Lowercase, collapse spaces
    normalized = re.sub(r'\s+', ' ', player_info.strip().lower())

    # Remove suffixes (Jr., Sr., III, IV)
    normalized = re.sub(r'\b(jr\.?|sr\.?|iii?|iv)\b', '', normalized)

    # Remove injury tags
    normalized = re.sub(r'\b(q view news|view news|sus|ir|nfi-r)\b', '', normalized)

    # Normalize punctuation (St. -> St, O'Dell -> ODell, Amon-Ra -> Amon Ra)
    normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')

    # Clean up spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized
```

3. **Progressive Matching Strategy (lines 569-630):**
- Exact full name match (fastest, O(1))
- Defense-specific matching (handles name format variations)
- Last name + position/team validation
- First name + validation (for unique names)
- Fuzzy matching fallback (0.75 threshold)

4. **Position Equivalency (lines 444-457):**
```python
def _positions_equivalent(self, pos1: str, pos2: str) -> bool:
    """Check if two position strings are equivalent (handles DST/DEF variations)."""
    if pos1.upper() == pos2.upper():
        return True

    # Defense equivalency
    defense_positions = {"DST", "DEF", "D/ST"}
    if pos1.upper() in defense_positions and pos2.upper() in defense_positions:
        return True

    return False
```

**Adaptation for This Feature:**
- Can reuse normalization logic
- Can reuse similarity_score function
- Can reuse positions_equivalent function
- Simpler matching needed (no team validation, just name + position)

---

## Interface Dependencies

### Input Dependency

**From Feature 1:** pandas DataFrame
- Confirmed structure: player_name, adp, position
- 988 rows (CSV data)
- All ADP values validated as positive floats

### Output Dependency

**None** - This is the final feature in the epic

### Match Rate Expectations

**CSV Players:** 988 (from FantasyPros)
**JSON Players:** 739 (from player data files)

**Expected outcomes:**
- **Matched:** ~500-700 players (most JSON players should match CSV)
- **Unmatched CSV:** ~300-400 players (CSV has players not in our JSON)
- **Unmatched JSON:** ~50-100 players (some JSON players may not be in CSV top 988)

**Note:** Unmatched CSV players are expected and OK (they're not in our JSON files)
**Note:** Unmatched JSON players will keep their 170.0 placeholder value

---

## Technical Approach

### JSON I/O Pattern (from PlayerManager)

**Reading JSON:**
```python
with open(filepath, 'r') as f:
    json_data = json.load(f)

position_key = position_file.replace('.json', '')  # "qb_data"
players_array = json_data.get(position_key, [])
```

**Writing JSON (Atomic Pattern):**
```python
# Wrap array back in object with position key
json_data_to_write = {position_key: players_array}

# Write to temp file first
tmp_path = json_path.with_suffix('.tmp')
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(json_data_to_write, f, indent=2)

# Atomic replace
tmp_path.replace(json_path)
```

**Why atomic writes?**
- Prevents data corruption if program crashes during write
- Either old file exists or new file exists (never half-written)
- Standard pattern in PlayerManager

### Matching Algorithm

**Proposed approach:**

1. **Load Feature 1 DataFrame** (from csv_data_loading module)
2. **For each JSON file** (6 position files):
   - Load JSON file
   - Extract players array
   - **For each JSON player:**
     - Filter CSV DataFrame by position
     - Find best match using fuzzy matching
     - If match confidence >= 0.75:
       - Update `average_draft_position` with CSV adp value
       - Track match (player_name, confidence_score, old_adp, new_adp)
     - If no match found:
       - Track as unmatched (player_name, position)
       - Keep 170.0 placeholder value
   - Write updated JSON file (atomic pattern)
3. **Generate match report:**
   - Total matched count
   - Total unmatched count
   - Match confidence distribution
   - List of unmatched JSON players
   - Optional: List of unmatched CSV players

**Fuzzy Matching Implementation:**
```python
def find_best_match(json_player_name: str, csv_df: pd.DataFrame) -> Tuple[Optional[float], float]:
    """
    Find best matching CSV player for JSON player.

    Args:
        json_player_name: Name from JSON player
        csv_df: DataFrame filtered by position

    Returns:
        Tuple of (adp_value, confidence_score) or (None, 0.0) if no match
    """
    best_score = 0.0
    best_adp = None

    json_normalized = normalize_name(json_player_name)

    for idx, row in csv_df.iterrows():
        csv_normalized = normalize_name(row['player_name'])
        score = similarity_score(json_normalized, csv_normalized)

        if score >= 0.75 and score > best_score:
            best_score = score
            best_adp = row['adp']

    return (best_adp, best_score)
```

### Module Structure

**New file to create:** `utils/adp_updater.py` (or similar)

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
            'unmatched_json_players': List[str],
            'match_confidence_stats': Dict,
            'files_updated': List[str]
        }

    Raises:
        FileNotFoundError: If player_data directory doesn't exist
        ValueError: If CSV DataFrame invalid
        PermissionError: If cannot write to JSON files
    """
```

**Helper functions:**
```python
def normalize_name(name: str) -> str:
    """Normalize player name for matching (adapted from DraftedRosterManager)."""

def similarity_score(s1: str, s2: str) -> float:
    """Calculate string similarity 0.0-1.0 (from DraftedRosterManager)."""

def find_best_match(...) -> Tuple[Optional[float], float]:
    """Find best matching CSV player for JSON player."""

def update_position_file(...) -> Dict:
    """Update single position JSON file with ADP values."""
```

---

## Edge Cases Identified

### 1. Name Variations

**Issue:** Players may have different name formats
**Examples:**
- "Amon-Ra St. Brown" vs "Amon Ra St Brown" (punctuation)
- "Kenneth Walker III" vs "Kenneth Walker" (suffix)
- "AJ Brown" vs "A.J. Brown" (initials)

**Solution:** Use normalization from DraftedRosterManager (strips punctuation, suffixes)

### 2. Multiple Matches Above Threshold

**Issue:** Multiple CSV players might match JSON player with score >= 0.75
**Example:** Two "Mike Williams" in CSV

**Solution:** Use highest confidence score (best_score pattern)

### 3. Position Mismatch

**Issue:** CSV position might differ from JSON position
**Example:** CSV has "WR" but JSON has "D/ST" (shouldn't happen but possible)

**Solution:** Filter CSV by position before matching (only match within same position)

### 4. Defense Name Formats

**Issue:** Defenses have inconsistent naming
**Examples:**
- CSV: "Seattle Seahawks"
- JSON: "Seahawks D/ST"

**Solution:**
- CSV positions already normalized (Feature 1 stripped suffixes)
- Both should be "DST" position
- Fuzzy matching should handle name variations

### 5. JSON File Corruption During Write

**Issue:** Program crashes mid-write, corrupting JSON file

**Solution:** Atomic write pattern (write to .tmp, then replace)

### 6. No Matches Found for JSON Player

**Issue:** JSON player not in CSV top 988 (e.g., backup RB not ranked)

**Solution:** Keep existing 170.0 value, track in unmatched list

### 7. CSV Player Not in JSON

**Issue:** CSV player not in our JSON files (expected - CSV has all ranked players)

**Solution:** Ignore (this is expected and OK)

### 8. Empty CSV DataFrame

**Issue:** Feature 1 returns empty DataFrame (CSV load failed)

**Solution:** Validate DataFrame has rows before processing (fail fast)

### 9. Missing player_data Directory

**Issue:** data/player_data/ doesn't exist

**Solution:** Raise FileNotFoundError with helpful message

### 10. Read-only File Permissions

**Issue:** Cannot write to JSON files (permission error)

**Solution:** Let PermissionError propagate with clear error message

---

## Existing Test Patterns

### Test File Location

Will create: `tests/utils/test_adp_updater.py`

### Test Patterns to Follow

**From existing tests (PlayerManager, DraftedRosterManager):**

1. **Use tmp_path fixture for test data:**
```python
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
                "average_draft_position": 170.0,
                # ...other fields
            }
        ]
    }
    (player_data_dir / "qb_data.json").write_text(json.dumps(qb_data, indent=2))

    return tmp_path
```

2. **Mock Feature 1 DataFrame:**
```python
@pytest.fixture
def csv_dataframe():
    """Create test CSV DataFrame from Feature 1"""
    return pd.DataFrame({
        'player_name': ['Josh Allen', 'Patrick Mahomes'],
        'adp': [5.0, 8.0],
        'position': ['QB', 'QB']
    })
```

3. **Test fuzzy matching:**
```python
def test_finds_match_with_punctuation_difference():
    """Test that 'Amon-Ra St. Brown' matches 'Amon Ra St Brown'"""
    json_name = "Amon-Ra St. Brown"
    csv_df = pd.DataFrame({
        'player_name': ['Amon Ra St Brown'],
        'adp': [20.0],
        'position': ['WR']
    })

    adp, confidence = find_best_match(json_name, csv_df)

    assert adp == 20.0
    assert confidence >= 0.75
```

4. **Test atomic writes:**
```python
def test_atomic_write_creates_tmp_file_first(test_player_data):
    """Test that .tmp file is created before replacing original"""
    # Monitor file system to ensure .tmp created before .json replaced
```

5. **Test edge cases:**
```python
def test_handles_no_match_found():
    """Test that unmatched players keep 170.0 value"""

def test_handles_multiple_matches_chooses_best():
    """Test that highest confidence match is chosen"""

def test_handles_empty_dataframe():
    """Test that empty CSV DataFrame is handled gracefully"""

def test_handles_missing_player_data_directory():
    """Test FileNotFoundError when player_data/ missing"""
```

### Required Test Coverage

**Must test:**
- ✅ CSV DataFrame loaded successfully
- ✅ JSON files loaded successfully
- ✅ Fuzzy matching finds exact matches (confidence = 1.0)
- ✅ Fuzzy matching finds similar matches (confidence >= 0.75)
- ✅ Fuzzy matching handles punctuation differences
- ✅ Fuzzy matching handles name suffix differences
- ✅ Position filtering works (only matches within same position)
- ✅ Multiple matches choose highest confidence
- ✅ No match found keeps 170.0 value
- ✅ Atomic write pattern used
- ✅ All other JSON fields preserved
- ✅ Match report generated correctly
- ✅ FileNotFoundError when player_data/ missing
- ✅ ValueError when CSV DataFrame empty/invalid
- ✅ PermissionError handled gracefully

---

## Technical Decisions Needed (For Checklist)

### Decision 1: Matching Confidence Threshold

**Question:** What confidence threshold should we use for accepting matches?

**Options:**
A. 0.75 (same as DraftedRosterManager)
B. 0.80 (more conservative)
C. 0.70 (more permissive)
D. Configurable parameter

**Recommendation:** Option A (0.75) - proven threshold from existing code

### Decision 2: Handling No Matches

**Question:** What should happen if a JSON player has no CSV match?

**Options:**
A. Keep existing 170.0 value
B. Set to None or null
C. Set to a different default (e.g., 999.0)
D. Remove player from JSON

**Recommendation:** Option A (keep 170.0) - least disruptive

### Decision 3: Match Report Details

**Question:** What level of detail should the match report include?

**Options:**
A. Summary only (matched/unmatched counts)
B. Summary + unmatched player lists
C. Summary + unmatched lists + confidence distribution
D. Summary + unmatched lists + all individual match details

**Recommendation:** Option C - good balance of detail vs verbosity

### Decision 4: Logging Level

**Question:** What should be logged during matching?

**Options:**
A. Log every match (INFO level)
B. Log only unmatched players (WARNING level)
C. Log summary only (INFO level)
D. Log everything in DEBUG, summary in INFO

**Recommendation:** Option D - detailed logs available for debugging

### Decision 5: Dry Run Mode

**Question:** Should there be a dry-run mode that doesn't write files?

**Options:**
A. Yes - add dry_run parameter
B. No - always write files

**Recommendation:** Option B - simpler, can test with tmp files

### Decision 6: Backup Files

**Question:** Should original JSON files be backed up before update?

**Options:**
A. Yes - create .bak files before updating
B. No - atomic writes are sufficient
C. Optional - add backup parameter

**Recommendation:** Option B - atomic writes prevent corruption, git provides history

### Decision 7: Match Report Format

**Question:** What format should the match report be?

**Options:**
A. Dictionary (returned by function)
B. Text file written to disk
C. Both
D. JSON file written to disk

**Recommendation:** Option A - returned dict (caller can write if desired)

---

## Implementation Scope Estimate

**Complexity:** MODERATE
- More complex than Feature 1 (fuzzy matching + file updates)
- But has existing patterns to follow (DraftedRosterManager, PlayerManager)

**Risk:** MODERATE
- File corruption risk (mitigated by atomic writes)
- Matching accuracy risk (mitigated by proven 0.75 threshold)

**Estimated items:** 25-30

**Dependencies:**
- Feature 1 (CSV Data Loading) - must be complete
- Existing fuzzy matching logic - available in DraftedRosterManager
- Existing JSON I/O patterns - available in PlayerManager

---

## Questions for User (Preliminary)

These will be asked ONE AT A TIME in Phase 3:

1. Should we use 0.75 as the confidence threshold (same as existing code)?
2. What should happen if a JSON player has no CSV match? (keep 170.0 or other)
3. What level of detail should the match report include?
4. Should we log every match or just summaries?
5. Should there be a dry-run mode?
6. Should we create backup files before updating?
7. What format should the match report be (dict, file, etc.)?

---

## Summary

**Feature 2 Scope:**
- Load DataFrame from Feature 1 (988 CSV players)
- Load 6 JSON files (739 total players)
- Fuzzy match JSON players to CSV players (by position)
- Update `average_draft_position` field for matched players
- Write updated JSON files (atomic pattern)
- Generate match report

**Reusable Components:**
- Fuzzy matching logic from DraftedRosterManager
- JSON I/O patterns from PlayerManager
- Normalization logic from DraftedRosterManager

**Expected Results:**
- ~500-700 JSON players matched and updated
- ~50-100 JSON players unmatched (keep 170.0)
- ~300-400 CSV players unmatched (expected - not in JSON)

**Ready for Phase 2:** YES - sufficient research completed
