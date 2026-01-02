# Epic Smoke Test Plan: fix_2025_adp

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 4 (Updated after deep dives)**
- Created: 2025-12-31 (Stage 1)
- Last Updated: 2025-12-31 (Stage 4)
- Based on: Feature specs from Stages 2-3, approved plan, Stage 3 sanity check
- Quality: CONCRETE - Specific tests based on actual feature designs
- Next Update: Stage 5e (after each feature implementation - will add more tests based on actual code)

**Update History:**
- Stage 1: Initial placeholder (assumptions only)
- Stage 4: **MAJOR UPDATE** - Added specific tests, integration points, measurable criteria
- Stage 5e: (Pending) Will update after each feature implementation

---

## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: CSV Data Successfully Loaded
✅ **MEASURABLE:** Feature 1 (CSV Data Loading) successfully loads CSV file

**Verification:**
```python
from utils.adp_csv_loader import load_adp_from_csv
from pathlib import Path

csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')
adp_df = load_adp_from_csv(csv_path)

# Expected results:
assert len(adp_df) == 988  # All CSV rows loaded
assert list(adp_df.columns) == ['player_name', 'adp', 'position']
assert (adp_df['adp'] > 0).all()  # All ADP values positive
assert set(adp_df['position']) == {'QB', 'RB', 'WR', 'TE', 'K', 'DST'}  # Clean positions
```

**Success Indicators:**
- DataFrame has 988 rows (all CSV players)
- All required columns present: player_name, adp, position
- All ADP values >0 (validated)
- All positions clean (no suffixes: WR1→WR, QB12→QB)

---

### Criterion 2: Player Matching Successful
✅ **MEASURABLE:** Feature 2 (Player Matching) matches >85% of JSON players to CSV players

**Verification:**
```python
from utils.adp_updater import update_player_adp_values
from pathlib import Path

adp_df = load_adp_from_csv(csv_path)
data_folder = Path('data')
report = update_player_adp_values(adp_df, data_folder)

# Expected results:
total_json_players = 739  # 100 QB + 168 RB + 254 WR + 147 TE + 38 K + 32 DST
assert report['summary']['total_json_players'] == total_json_players
assert report['summary']['matched'] > (total_json_players * 0.85)  # >85% match rate
assert len(report['unmatched_json_players']) < (total_json_players * 0.15)  # <15% unmatched
```

**Success Indicators:**
- Total JSON players: 739
- Matched players: >627 (85% of 739)
- Unmatched JSON players: <112 (15% of 739)
- Match report contains all required sections

---

### Criterion 3: ADP Values Updated in JSON Files
✅ **MEASURABLE:** All matched players have updated ADP values (not 170.0 placeholder)

**Verification:**
```python
import json
from pathlib import Path

# Check one JSON file (e.g., QB data)
qb_json_path = Path('data/player_data/qb_data.json')
with open(qb_json_path, 'r') as f:
    qb_data = json.load(f)

players_with_real_adp = [
    p for p in qb_data['qb_data']
    if p.get('average_draft_position', 170.0) != 170.0
]

# Expected: Most QBs should have updated ADP (not 170.0)
total_qbs = len(qb_data['qb_data'])
assert len(players_with_real_adp) > (total_qbs * 0.85)  # >85% updated
```

**Success Indicators:**
- Matched players have ADP != 170.0
- Unmatched players retain ADP = 170.0 (expected behavior)
- JSON structure preserved (only `average_draft_position` field changed)
- All 6 JSON files updated: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json

---

### Criterion 4: Data Integrity Maintained
✅ **MEASURABLE:** All other player fields remain unchanged (only ADP updated)

**Verification:**
1. Create backup of original JSON files before running epic
2. Run epic (Features 1 + 2)
3. Compare before/after JSON files

```python
# Verify only 'average_draft_position' changed
for player_before, player_after in zip(original_data, updated_data):
    # All fields same except ADP
    for key in player_before.keys():
        if key == 'average_draft_position':
            # ADP should change (unless unmatched)
            continue
        else:
            # All other fields unchanged
            assert player_before[key] == player_after[key]
```

**Success Indicators:**
- Only `average_draft_position` field modified
- All other fields unchanged: name, position, projected_points, etc.
- JSON array structure preserved
- No players added or removed

---

### Criterion 5: Match Report Generated
✅ **MEASURABLE:** Comprehensive match report returned with all required sections

**Verification:**
```python
report = update_player_adp_values(adp_df, data_folder)

# Verify report structure
assert 'summary' in report
assert 'unmatched_json_players' in report
assert 'unmatched_csv_players' in report
assert 'confidence_distribution' in report
assert 'individual_matches' in report

# Verify summary contents
assert 'total_json_players' in report['summary']
assert 'matched' in report['summary']
assert 'unmatched_json' in report['summary']
assert 'unmatched_csv' in report['summary']
```

**Success Indicators:**
- Report has all 5 required sections
- Summary shows accurate counts
- Unmatched lists contain player details
- Confidence distribution shows score ranges (1.0, 0.9-0.99, 0.75-0.89)
- Individual matches show all match details (for comprehensive report)

---

### Criterion 6: No Errors in E2E Workflow
✅ **MEASURABLE:** Complete workflow runs without exceptions

**Verification:**
```bash
# Run complete epic workflow
python -c "
from utils.adp_csv_loader import load_adp_from_csv
from utils.adp_updater import update_player_adp_values
from pathlib import Path

csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')
data_folder = Path('data')

# Feature 1: Load CSV
adp_df = load_adp_from_csv(csv_path)
print(f'CSV loaded: {len(adp_df)} players')

# Feature 2: Update JSON files
report = update_player_adp_values(adp_df, data_folder)
print(f'Matched: {report[\"summary\"][\"matched\"]} players')
print('Epic workflow complete!')
"
echo "Exit code: $?"  # Should be 0
```

**Success Indicators:**
- Exit code: 0 (success)
- No FileNotFoundError (CSV exists, JSON files exist)
- No ValueError (CSV valid, DataFrame valid)
- No PermissionError (JSON files writable)
- No exceptions during execution

---

## Integration Points Identified

### Integration Point 1: Feature 1 → Feature 2 (CSV DataFrame)

**Features Involved:** Feature 1 (CSV Data Loading) → Feature 2 (Player Matching & Data Update)

**Type:** Data interface

**Flow:**
1. Feature 1 loads CSV file
2. Feature 1 returns pandas DataFrame (player_name, adp, position)
3. Feature 2 receives DataFrame as input parameter
4. Feature 2 uses DataFrame to match and update players

**Interface Contract:**
```python
# Feature 1 output:
adp_df = load_adp_from_csv(csv_path)
# DataFrame columns: ['player_name', 'adp', 'position']
# Data types: str, float, str
# Position values: QB, RB, WR, TE, K, DST (clean, no suffixes)
# ADP values: positive floats (>0)

# Feature 2 input:
report = update_player_adp_values(adp_dataframe=adp_df, data_folder=data_folder)
# Expects same DataFrame structure as Feature 1 output
```

**Test Need:** Verify DataFrame structure matches exactly between Feature 1 output and Feature 2 input

**Verified in Stage 3:** ✅ Zero conflicts found, perfect alignment

---

### Integration Point 2: Feature 2 ↔ JSON Files (Data Persistence)

**Features Involved:** Feature 2 (Player Matching & Data Update)

**Type:** File system interaction (read/write)

**Flow:**
1. Feature 2 reads 6 JSON files from `data/player_data/`
2. Feature 2 updates `average_draft_position` field for matched players
3. Feature 2 writes updated JSON files (atomic write pattern)

**Files Affected:**
- `data/player_data/qb_data.json` (100 players)
- `data/player_data/rb_data.json` (168 players)
- `data/player_data/wr_data.json` (254 players)
- `data/player_data/te_data.json` (147 players)
- `data/player_data/k_data.json` (38 players)
- `data/player_data/dst_data.json` (32 players)

**Test Need:**
- Verify all 6 files readable
- Verify all 6 files writable (permissions)
- Verify atomic write pattern prevents corruption
- Verify JSON structure preserved after updates

---

### Integration Point 3: Fuzzy Matching Logic (Code Reuse)

**Features Involved:** Feature 2 (Player Matching & Data Update)

**Type:** Algorithm adaptation

**Flow:**
1. Feature 2 adapts fuzzy matching from `utils/DraftedRosterManager.py`
2. Uses same 0.75 confidence threshold (proven pattern)
3. Uses same name normalization logic (remove punctuation, suffixes)
4. Uses difflib.SequenceMatcher for similarity scoring

**Source Code:**
- `utils/DraftedRosterManager.py` - Existing fuzzy matching (read-only reference)

**Test Need:**
- Verify 0.75 threshold applied correctly
- Verify normalization handles name variations (St. Brown, Kenneth Walker III, Jr., Sr.)
- Verify best match selection (highest confidence score wins)

---

## Specific Test Scenarios

**These tests MUST be run for epic-level validation:**

---

### Test Scenario 1: CSV Data Loading (Feature 1)

**Purpose:** Verify Feature 1 loads CSV correctly and returns expected DataFrame structure

**Setup:**
- Ensure `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv` exists
- CSV should have 989 rows (1 header + 988 data)

**Steps:**
```python
from utils.adp_csv_loader import load_adp_from_csv
from pathlib import Path

csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')
adp_df = load_adp_from_csv(csv_path)

print(f"Rows loaded: {len(adp_df)}")
print(f"Columns: {list(adp_df.columns)}")
print(f"Positions: {sorted(adp_df['position'].unique())}")
print(f"ADP range: {adp_df['adp'].min():.1f} - {adp_df['adp'].max():.1f}")
```

**Expected Results:**
✅ Rows loaded: 988
✅ Columns: ['player_name', 'adp', 'position']
✅ Positions: ['DST', 'K', 'QB', 'RB', 'TE', 'WR'] (clean, no suffixes)
✅ ADP range: 1.0 - 988.0 (all positive)
✅ No exceptions raised

**Failure Indicators:**
❌ FileNotFoundError → CSV file missing or wrong path
❌ ValueError (missing columns) → CSV structure changed
❌ ValueError (ADP <=0) → CSV has invalid ADP values
❌ Wrong row count → CSV not fully loaded
❌ Position suffixes present (WR1, QB12) → Suffix stripping failed

---

### Test Scenario 2: Position Suffix Stripping (Feature 1)

**Purpose:** Verify Feature 1 correctly strips position tier suffixes

**Setup:**
- Use real CSV data with suffixes (WR1, RB2, QB12, TE1, K1, DST1)

**Steps:**
```python
from utils.adp_csv_loader import load_adp_from_csv

adp_df = load_adp_from_csv(csv_path)

# Check specific players with known suffixes
wr_positions = adp_df[adp_df['position'] == 'WR']['position'].unique()
qb_positions = adp_df[adp_df['position'] == 'QB']['position'].unique()

print(f"WR positions: {wr_positions}")  # Should be ['WR'] only
print(f"QB positions: {qb_positions}")  # Should be ['QB'] only
```

**Expected Results:**
✅ All WR entries show position = 'WR' (not 'WR1', 'WR2', etc.)
✅ All QB entries show position = 'QB' (not 'QB1', 'QB12', etc.)
✅ All position values in: {QB, RB, WR, TE, K, DST}
✅ No numeric suffixes in any position value

**Failure Indicators:**
❌ Position values like 'WR1' → Suffix stripping failed
❌ Position values with digits → Regex not applied
❌ Unexpected position values → Data parsing issue

---

### Test Scenario 3: DataFrame Interface Compatibility (Integration Point 1)

**Purpose:** Verify Feature 1 output matches Feature 2 input expectations

**Setup:**
- Run Feature 1 to get DataFrame
- Verify structure before passing to Feature 2

**Steps:**
```python
from utils.adp_csv_loader import load_adp_from_csv
from utils.adp_updater import update_player_adp_values

# Feature 1: Load CSV
adp_df = load_adp_from_csv(csv_path)

# Verify interface contract
assert 'player_name' in adp_df.columns, "Missing player_name column"
assert 'adp' in adp_df.columns, "Missing adp column"
assert 'position' in adp_df.columns, "Missing position column"
assert adp_df['adp'].dtype == 'float64', "ADP not float type"
assert (adp_df['adp'] > 0).all(), "ADP values not all positive"

print("✅ DataFrame interface verified - ready for Feature 2")

# Feature 2: Use DataFrame (should accept without modification)
report = update_player_adp_values(adp_df, data_folder)
print(f"✅ Feature 2 accepted DataFrame - matched {report['summary']['matched']} players")
```

**Expected Results:**
✅ All interface assertions pass
✅ Feature 2 accepts DataFrame without errors
✅ No ValueError from Feature 2 (DataFrame valid)

**Failure Indicators:**
❌ Missing column → Feature 1 output incomplete
❌ Wrong data type → Feature 1 parsing issue
❌ Feature 2 ValueError → Interface mismatch

---

### Test Scenario 4: Fuzzy Matching with Name Variations (Feature 2)

**Purpose:** Verify Feature 2 handles name variations correctly using fuzzy matching

**Setup:**
- Create test cases with known name variations:
  - "Amon-Ra St. Brown" (CSV) vs "Amon-Ra St Brown" (JSON) - punctuation
  - "Kenneth Walker III" (CSV) vs "Kenneth Walker" (JSON) - suffix
  - "Patrick Mahomes II" (CSV) vs "Patrick Mahomes" (JSON) - suffix

**Steps:**
```python
# Run matching
report = update_player_adp_values(adp_df, data_folder)

# Check individual matches for known variations
matches = report['individual_matches']
st_brown_match = [m for m in matches if 'St' in m['csv_name'] or 'St' in m['json_name']]
walker_match = [m for m in matches if 'Walker' in m['csv_name']]

print(f"St. Brown match confidence: {st_brown_match[0]['confidence']}")
print(f"Walker match confidence: {walker_match[0]['confidence']}")
```

**Expected Results:**
✅ St. Brown matches despite punctuation difference (confidence >0.75)
✅ Walker III matches despite suffix difference (confidence >0.75)
✅ Mahomes II matches despite suffix difference (confidence >0.75)
✅ All confidence scores >= 0.75 threshold

**Failure Indicators:**
❌ Confidence <0.75 for obvious matches → Normalization failed
❌ No match found → Fuzzy matching not working
❌ Wrong player matched → Best match selection failed

---

### Test Scenario 5: Player Matching and ADP Updates (Feature 2)

**Purpose:** Verify Feature 2 matches players and updates ADP values correctly

**Setup:**
- Run complete workflow (Feature 1 + Feature 2)
- Backup JSON files before test
- Restore JSON files after test

**Steps:**
```bash
# Backup original JSON files
cp data/player_data/qb_data.json data/player_data/qb_data.json.bak

# Run epic workflow
python -c "
from utils.adp_csv_loader import load_adp_from_csv
from utils.adp_updater import update_player_adp_values
from pathlib import Path
import json

csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')
data_folder = Path('data')

# Load and match
adp_df = load_adp_from_csv(csv_path)
report = update_player_adp_values(adp_df, data_folder)

print(f'Total JSON players: {report[\"summary\"][\"total_json_players\"]}')
print(f'Matched: {report[\"summary\"][\"matched\"]}')
print(f'Unmatched JSON: {report[\"summary\"][\"unmatched_json\"]}')
print(f'Match rate: {report[\"summary\"][\"matched\"] / report[\"summary\"][\"total_json_players\"] * 100:.1f}%')

# Verify ADP updated
with open('data/player_data/qb_data.json', 'r') as f:
    qb_data = json.load(f)
    updated_count = sum(1 for p in qb_data['qb_data'] if p.get('average_draft_position', 170.0) != 170.0)
    print(f'QBs with updated ADP: {updated_count}/{len(qb_data[\"qb_data\"])}')
"

# Restore backup
mv data/player_data/qb_data.json.bak data/player_data/qb_data.json
```

**Expected Results:**
✅ Total JSON players: 739
✅ Matched: >627 (85% match rate)
✅ Unmatched JSON: <112 (15% unmatch rate)
✅ QBs with updated ADP: >85 (85% of 100 QBs)
✅ Match report shows all required sections

**Failure Indicators:**
❌ Match rate <85% → Fuzzy matching not effective
❌ No ADP updates → JSON write failed
❌ All players still 170.0 → Matching or update logic broken
❌ Missing report sections → Report generation incomplete

---

### Test Scenario 6: JSON Data Integrity (Feature 2)

**Purpose:** Verify only ADP field updated, all other fields preserved

**Setup:**
- Create snapshot of original JSON data
- Run epic workflow
- Compare before/after

**Steps:**
```python
import json
from pathlib import Path

# Load original data
original_qb_path = Path('data/player_data/qb_data.json.bak')
updated_qb_path = Path('data/player_data/qb_data.json')

with open(original_qb_path, 'r') as f:
    original_data = json.load(f)['qb_data']

# Run epic (Feature 1 + Feature 2)
adp_df = load_adp_from_csv(csv_path)
report = update_player_adp_values(adp_df, data_folder)

# Load updated data
with open(updated_qb_path, 'r') as f:
    updated_data = json.load(f)['qb_data']

# Verify integrity
for orig, upd in zip(original_data, updated_data):
    # All fields same except ADP
    for key in orig.keys():
        if key == 'average_draft_position':
            # ADP can change (for matched players)
            continue
        else:
            # All other fields must be identical
            assert orig[key] == upd[key], f"Field {key} changed for player {orig.get('name')}"

print("✅ Data integrity verified - only ADP field modified")
```

**Expected Results:**
✅ Only `average_draft_position` field modified
✅ All other fields unchanged: name, position, projected_points, etc.
✅ Same number of players (no additions/deletions)
✅ JSON structure preserved

**Failure Indicators:**
❌ Other fields modified → Data corruption
❌ Players added/removed → Array manipulation error
❌ JSON structure broken → Write logic issue

---

### Test Scenario 7: Atomic Write Pattern (Feature 2)

**Purpose:** Verify Feature 2 uses atomic writes to prevent file corruption

**Setup:**
- Monitor file system during write operations
- Check for .tmp files during write

**Steps:**
```python
from pathlib import Path
import time

# Start monitoring
json_path = Path('data/player_data/qb_data.json')
tmp_path = json_path.with_suffix('.tmp')

# Run update
report = update_player_adp_values(adp_df, data_folder)

# Verify .tmp file used (may be cleaned up by now)
# Verify final file exists and is valid JSON
assert json_path.exists(), "JSON file missing after update"

with open(json_path, 'r') as f:
    data = json.load(f)  # Should not raise JSONDecodeError

print("✅ Atomic write successful - no corruption")
```

**Expected Results:**
✅ Temporary .tmp file created during write (or write too fast to observe)
✅ Final JSON file valid (no corruption)
✅ No JSONDecodeError when reading updated file

**Failure Indicators:**
❌ JSONDecodeError → File corrupted during write
❌ Partial write → File truncated
❌ Permission error → .tmp file couldn't be created

---

### Test Scenario 8: Match Report Comprehensive (Feature 2 - Decision 3)

**Purpose:** Verify match report includes all required sections per user Decision 3 (Option D)

**Setup:**
- Run Feature 2 with real data
- Capture full match report

**Steps:**
```python
report = update_player_adp_values(adp_df, data_folder)

# Verify all 5 required sections exist
assert 'summary' in report, "Missing summary section"
assert 'unmatched_json_players' in report, "Missing unmatched JSON list"
assert 'unmatched_csv_players' in report, "Missing unmatched CSV list"
assert 'confidence_distribution' in report, "Missing confidence distribution"
assert 'individual_matches' in report, "Missing individual matches"

# Verify summary contents
summary = report['summary']
assert 'total_json_players' in summary
assert 'matched' in summary
assert 'unmatched_json' in summary
assert 'unmatched_csv' in summary

# Verify confidence distribution
conf_dist = report['confidence_distribution']
assert '1.0' in conf_dist or 'perfect' in conf_dist
assert '0.9-0.99' in conf_dist or 'high' in conf_dist
assert '0.75-0.89' in conf_dist or 'medium' in conf_dist

# Verify individual matches (comprehensive report)
assert len(report['individual_matches']) == summary['matched']

print("✅ Comprehensive match report verified - all sections present")
```

**Expected Results:**
✅ All 5 sections present in report
✅ Summary has accurate counts
✅ Unmatched lists contain player details (name, position)
✅ Confidence distribution shows score ranges
✅ Individual matches show all matched players with details

**Failure Indicators:**
❌ Missing section → Report generation incomplete
❌ Empty lists when should have data → Logic error
❌ Individual matches incomplete → Not comprehensive (Decision 3 violation)

---

### Test Scenario 9: Logging Verification (Feature 2 - Decision 4)

**Purpose:** Verify hybrid logging approach (unmatched players as WARNING + summary as INFO)

**Setup:**
- Capture log output during Feature 2 execution
- Verify WARNING and INFO messages

**Steps:**
```python
import logging
from io import StringIO

# Capture logs
log_stream = StringIO()
handler = logging.StreamHandler(log_stream)
handler.setLevel(logging.DEBUG)
logger = logging.getLogger('utils.adp_updater')
logger.addHandler(handler)

# Run Feature 2
report = update_player_adp_values(adp_df, data_folder)

# Get log output
log_output = log_stream.getvalue()

# Verify logging
assert 'WARNING' in log_output, "Missing WARNING logs for unmatched players"
assert 'INFO' in log_output, "Missing INFO logs for summary"
assert 'matched' in log_output.lower(), "Summary not logged"

# Verify unmatched players logged as WARNING
unmatched_count = report['summary']['unmatched_json']
warning_lines = [line for line in log_output.split('\n') if 'WARNING' in line]
# Should have one WARNING per unmatched player (or grouped)

print(f"✅ Logging verified - {len(warning_lines)} WARNING logs, summary logged at INFO")
```

**Expected Results:**
✅ Unmatched players logged as WARNING
✅ Summary logged as INFO
✅ No DEBUG logs in default output (only if DEBUG level set)
✅ Hybrid approach confirmed (Decision 4)

**Failure Indicators:**
❌ No WARNING logs → Unmatched players not logged
❌ No INFO logs → Summary not logged
❌ Wrong log levels → Logging configuration incorrect

---

### Test Scenario 10: End-to-End Integration Test

**Purpose:** Verify complete epic workflow (Feature 1 + Feature 2) runs successfully

**Setup:**
- Clean environment
- Real CSV file present
- Real JSON files present (backup first)

**Steps:**
```bash
# Complete E2E test
python -c "
import sys
from pathlib import Path
from utils.adp_csv_loader import load_adp_from_csv
from utils.adp_updater import update_player_adp_values
import json

try:
    # Feature 1: Load CSV
    csv_path = Path('feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv')
    print('Loading CSV...')
    adp_df = load_adp_from_csv(csv_path)
    print(f'✅ CSV loaded: {len(adp_df)} players')

    # Feature 2: Update JSON files
    data_folder = Path('data')
    print('Matching and updating players...')
    report = update_player_adp_values(adp_df, data_folder)
    print(f'✅ Matched: {report[\"summary\"][\"matched\"]} players')
    print(f'✅ Unmatched JSON: {report[\"summary\"][\"unmatched_json\"]} players')
    print(f'✅ Match rate: {report[\"summary\"][\"matched\"] / report[\"summary\"][\"total_json_players\"] * 100:.1f}%')

    # Verify JSON files updated
    with open('data/player_data/qb_data.json', 'r') as f:
        qb_data = json.load(f)
        updated_qbs = sum(1 for p in qb_data['qb_data'] if p.get('average_draft_position', 170.0) != 170.0)
        print(f'✅ QBs with updated ADP: {updated_qbs}/{len(qb_data[\"qb_data\"])}')

    print('')
    print('🎉 Epic workflow complete - all tests passed!')
    sys.exit(0)

except Exception as e:
    print(f'❌ Error: {e}', file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

echo "Exit code: $?"  # Should be 0
```

**Expected Results:**
✅ CSV loads successfully (988 players)
✅ Matching completes successfully
✅ Match rate >85% (>627 of 739 players)
✅ JSON files updated with real ADP values
✅ No exceptions raised
✅ Exit code 0

**Failure Indicators:**
❌ Exit code != 0 → Workflow failed
❌ Exception raised → Error in Feature 1 or Feature 2
❌ Match rate <85% → Fuzzy matching ineffective
❌ No ADP updates → Update logic failed

---

## High-Level Test Categories

**Agent will create additional scenarios for these categories during Stage 5e (after implementation):**

### Category 1: Data Loading & Validation
**What to test:** CSV parsing handles all edge cases (extra spaces, special characters, name variations)

**Known specific tests (from above):**
- Test Scenario 1: CSV Data Loading
- Test Scenario 2: Position Suffix Stripping

**Stage 5e will add:**
- Additional edge cases discovered during implementation
- Performance benchmarks for CSV loading
- Error handling scenarios (missing file, corrupt CSV, etc.)

---

### Category 2: Fuzzy Matching Accuracy
**What to test:** Name variations match correctly, confidence thresholds work, best match selection

**Known specific tests (from above):**
- Test Scenario 4: Fuzzy Matching with Name Variations
- Test Scenario 5: Player Matching and ADP Updates

**Stage 5e will add:**
- Additional name variation test cases
- Confidence threshold boundary tests (0.74 vs 0.75 vs 0.76)
- Position filtering verification
- Best match selection verification (multiple high-confidence matches)

---

### Category 3: Data Update Integrity
**What to test:** Only ADP field updated, all other fields preserved, JSON structure valid

**Known specific tests (from above):**
- Test Scenario 6: JSON Data Integrity
- Test Scenario 7: Atomic Write Pattern

**Stage 5e will add:**
- All 6 position files verified (not just QB)
- Concurrent write safety (if applicable)
- Rollback scenarios (if write fails mid-process)

---

### Category 4: Error Handling
**What to test:** Missing files, invalid CSV data, unmatched players, permission errors

**Known error scenarios:**
- Missing CSV file → FileNotFoundError
- Missing columns in CSV → ValueError
- Invalid ADP values (<=0) → ValueError
- Missing data/player_data/ folder → FileNotFoundError
- Permission denied on JSON files → PermissionError

**Stage 5e will add:**
- Specific error handling tests
- Graceful degradation scenarios
- Error message verification

---

### Category 5: Integration Points
**What to test:** Features work together correctly, data flows properly, no interface mismatches

**Known integration points (from above):**
- Integration Point 1: Feature 1 → Feature 2 (DataFrame)
- Integration Point 2: Feature 2 ↔ JSON Files
- Integration Point 3: Fuzzy Matching Logic (code reuse)

**Known specific tests (from above):**
- Test Scenario 3: DataFrame Interface Compatibility
- Test Scenario 10: End-to-End Integration Test

**Stage 5e will add:**
- Cross-feature error propagation
- Integration failure scenarios
- Performance impact of integration

---

### Category 6: Logging & Reporting
**What to test:** Correct log levels, comprehensive reports, user-facing output quality

**Known specific tests (from above):**
- Test Scenario 8: Match Report Comprehensive
- Test Scenario 9: Logging Verification

**Stage 5e will add:**
- Log output format verification
- Report export scenarios (if applicable)
- User-facing message clarity

---

## Update Log

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| 2025-12-31 | Stage 1 | Initial plan created | Epic planning - assumptions only |
| 2025-12-31 | Stage 4 | **MAJOR UPDATE** | Based on feature specs (Stages 2-3) |

**Stage 4 changes:**
- Added 10 specific test scenarios with concrete commands (was 3 TBD placeholders)
- Replaced 5 vague success criteria with 6 MEASURABLE criteria
- Identified 3 integration points between features
- Added concrete Python code and bash commands for verification
- Documented failure indicators for each test
- Added comprehensive match report verification (Decision 3)
- Added hybrid logging verification (Decision 4)
- Included data integrity and atomic write verification

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request
- Stage 2: Feature deep dives (csv_data_loading, player_matching_update)
- Stage 3: Cross-feature sanity check (zero conflicts found)
- **Stage 4: Feature specs and approved implementation plan** ← YOU ARE HERE

**Integration points discovered:**
1. Feature 1 → Feature 2 via pandas DataFrame (player_name, adp, position)
2. Feature 2 ↔ JSON files (atomic read/write pattern)
3. Fuzzy matching logic adapted from DraftedRosterManager.py (0.75 threshold)

**Next update:** Stage 5e after each feature completes (will add implementation-specific tests based on actual code, not just specs)

---

**Testing Strategy Complete - Ready for Implementation (Stage 5)**
