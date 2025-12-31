# Epic Smoke Test Plan: bug_fix_player_data_fetcher_drafted_column

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 5e (Updated after feature_01 implementation)**
- Created: 2025-12-30 (Stage 1)
- Last Updated: 2025-12-31 (Stage 5e - after feature_01)
- Based on: Feature_01 ACTUAL implementation insights (not just specs)
- Quality: EXECUTABLE - Concrete tests with actual data values verified
- Next Update: Stage 5e (after feature_02 implementation)

---

## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: Player Data Fetcher Runs End-to-End ✅
**MEASURABLE:**
- Command: `python player-data-fetcher/player_data_fetcher_main.py`
- Exit code: 0 (success)
- No ERROR or CRITICAL messages in logs

**Verification:** Run player-data-fetcher, check exit code and logs

---

### Criterion 2: All Position JSON Files Created with Correct Field ✅
**MEASURABLE:**
- Files exist: `data/player_data/{qb,rb,wr,te,k,dst}_data.json` (6 files)
- Each file contains field: `"drafted_by"` (string)
- NO file contains deprecated field: `"drafted"` (integer)

**Verification:**
```bash
# Check all position files exist and have correct field
for pos in qb rb wr te k dst; do
  test -f "data/player_data/${pos}_data.json" && echo "${pos}_data.json exists" || echo "FAILED: ${pos}_data.json missing"
  grep -q "drafted_by" "data/player_data/${pos}_data.json" && echo "${pos} has drafted_by" || echo "FAILED: ${pos} missing drafted_by"
  ! grep -q "\"drafted\":" "data/player_data/${pos}_data.json" && echo "${pos} no old drafted field" || echo "FAILED: ${pos} still has drafted"
done
```

---

### Criterion 3: Deprecated CSV Files NOT Created ✅
**MEASURABLE:**
- Files do NOT exist after player-data-fetcher runs:
  - `data/players.csv`
  - `data/players_projected.csv`

**Verification:**
```bash
! test -f "data/players.csv" && echo "players.csv NOT created (correct)" || echo "FAILED: players.csv still created"
! test -f "data/players_projected.csv" && echo "players_projected.csv NOT created (correct)" || echo "FAILED: players_projected.csv still created"
```

---

### Criterion 4: No References to Deprecated 'drafted' Field in Code ✅
**MEASURABLE:**
- Grep search finds 0 active references to `drafted: int` or `drafted=` in player-data-fetcher module (excluding comments)
- Config has `drafted_by` in EXPORT_COLUMNS, NOT `drafted`

**Verification:**
```bash
# Should find 0 results (only comments/deprecated code if any)
grep -r "drafted: int" player-data-fetcher/*.py --include="*.py" | grep -v "#" | wc -l  # Should be 0
grep -r "drafted=" player-data-fetcher/*.py --include="*.py" | grep -v "#" | wc -l  # Should be 0 or only drafted_by=
```

---

### Criterion 5: League Helper Loads Data Successfully ✅
**MEASURABLE:**
- League helper runs in all 4 modes without errors
- PlayerManager.load_players_from_json() succeeds
- All loaded players have `drafted_by` field

**Verification:**
```python
# In Python REPL
from league_helper.util.PlayerManager import PlayerManager
pm = PlayerManager(data_folder="data/")
players = pm.load_players_from_json()
assert len(players) > 0, "No players loaded"
assert hasattr(players[0], 'drafted_by'), "Players missing drafted_by field"
print(f"✅ Loaded {len(players)} players with drafted_by field")
```

---

## Integration Points Identified

### Integration Point 1: ESPNPlayerData → FantasyPlayer Data Model

**[UPDATED Stage 5e - feature_01]:** Enhanced with actual integration flow discovered during implementation

**Features Involved:** Feature 1, Feature 2
**Type:** Shared data structure with post-processing
**Flow:**
- Feature 1 changes: ESPNPlayerData field `drafted: int` → `drafted_by: str`
- Feature 1 updates: FantasyPlayer conversion to use `drafted_by` parameter
- **[NEW]** Feature 1 integration: DraftedRosterManager.apply_drafted_state_to_players() called at player_data_exporter.py:297
  - All players start with drafted_by = "" (free agents)
  - DraftedRosterManager reads drafted_data.csv
  - Populates drafted_by with team names for drafted players
  - Leaves free agents as empty string ""
- Feature 2 depends on: Correct data model (can't export broken CSVs)

**Test Need:**
- Verify ESPNPlayerData and FantasyPlayer have `drafted_by` field after Feature 1
- **[NEW]** Verify DraftedRosterManager integration at line 297 (Test Scenario 7)
- **[NEW]** Verify actual team names populated (Test Scenario 6)

---

### Integration Point 2: Position JSON Export
**Features Involved:** Feature 1, Feature 2
**Type:** File system output
**Flow:**
- Feature 1 ensures: Position JSON files export `drafted_by` field (not `drafted`)
- Feature 2 requires: Position JSON exports work (only export remaining)

**Test Need:** Verify position JSON files created with `drafted_by` field

---

### Integration Point 3: player-data-fetcher Module
**Features Involved:** Feature 1, Feature 2
**Type:** Code module interaction
**Flow:**
- Feature 1 modifies: player_data_models.py, espn_client.py, player_data_exporter.py (3 sections)
- Feature 2 modifies: player_data_fetcher_main.py, player_data_exporter.py (2 methods)
- Overlap: player_data_exporter.py (different sections - no conflicts)

**Test Need:** Verify player-data-fetcher runs end-to-end after BOTH features

---

### Integration Point 4: config.py Configuration File
**Features Involved:** Feature 1, Feature 2
**Type:** Shared configuration
**Flow:**
- Feature 1 removes: PRESERVE_DRAFTED_VALUES (line 17), updates EXPORT_COLUMNS (line 84)
- Feature 2 removes: PLAYERS_CSV constant (line 38)

**Test Need:** Verify config.py has no merge conflicts, all imports still work

---

### Integration Point 5: Sequential Dependency
**Features Involved:** Feature 1 → Feature 2
**Type:** Implementation order dependency
**Flow:**
- Feature 1 MUST complete first (data model fixed)
- Feature 2 requires Feature 1 (can't disable broken exports)

**Test Need:** Verify Feature 2 only runs after Feature 1 complete

---

### Integration Point 6: League Helper System (Downstream)
**Features Involved:** Feature 1, Feature 2 (both affect league helper)
**Type:** System integration
**Flow:**
- League helper loads from position JSON files (PlayerManager.load_players_from_json())
- Must work with `drafted_by` field from Feature 1
- Must NOT need players.csv after Feature 2

**Test Need:** Verify league helper runs in all modes after epic

---

## Specific Test Scenarios

**These tests MUST be run for epic-level validation:**

### Test Scenario 1: Data Model Migration (Feature 1)

**Purpose:** Verify Feature 1 successfully migrates ESPNPlayerData and FantasyPlayer to use `drafted_by` field

**Steps:**
1. Inspect ESPNPlayerData model definition
2. Inspect FantasyPlayer conversion in player_data_exporter.py
3. Run player-data-fetcher
4. Check position JSON files

**Expected Results:**
- ✅ ESPNPlayerData has field: `drafted_by: str = ""`
- ✅ Conversion uses: `drafted_by=player_data.drafted_by`
- ✅ Position JSON files contain `"drafted_by"` field for all players
- ✅ No `drafted: int` field in ESPNPlayerData

**Failure Indicators:**
- ❌ ESPNPlayerData still has `drafted: int` → Feature 1 incomplete
- ❌ Conversion still uses `drafted=` → Feature 1 incomplete
- ❌ JSON files missing `drafted_by` field → Export broken

**Command to verify:**
```bash
# Check model definition
grep "drafted_by: str" player-data-fetcher/player_data_models.py && echo "✅ Model updated" || echo "❌ Model NOT updated"

# Check JSON output
cat data/player_data/qb_data.json | python -m json.tool | grep drafted_by | head -1
```

---

### Test Scenario 2: CSV Export Removal (Feature 2)

**Purpose:** Verify Feature 2 successfully removes deprecated CSV export calls

**Steps:**
1. Delete old CSV files (if present)
2. Run player-data-fetcher
3. Check that CSV files were NOT recreated
4. Check that position JSON files WERE created

**Expected Results:**
- ✅ `data/players.csv` does NOT exist after run
- ✅ `data/players_projected.csv` does NOT exist after run
- ✅ All 6 position JSON files DO exist
- ✅ No errors in player-data-fetcher logs

**Failure Indicators:**
- ❌ CSV files created → Feature 2 incomplete
- ❌ JSON files NOT created → Feature 1 or position export broken
- ❌ Errors in logs → Export logic broken

**Command to verify:**
```bash
# Clean old files
rm -f data/players.csv data/players_projected.csv

# Run fetcher
python player-data-fetcher/player_data_fetcher_main.py

# Verify
! test -f data/players.csv && echo "✅ players.csv NOT created" || echo "❌ FAILED: players.csv created"
! test -f data/players_projected.csv && echo "✅ players_projected.csv NOT created" || echo "❌ FAILED: players_projected.csv created"
test -f data/player_data/qb_data.json && echo "✅ JSON files created" || echo "❌ FAILED: JSON not created"
```

---

### Test Scenario 3: End-to-End Player Data Fetcher Workflow

**Purpose:** Verify complete player-data-fetcher workflow after BOTH features

**Steps:**
1. Run player-data-fetcher from start to finish
2. Check all outputs created correctly
3. Verify no errors

**Expected Results:**
- ✅ Exit code 0
- ✅ All 6 position JSON files created in `data/player_data/`
- ✅ No `data/players.csv` or `data/players_projected.csv` created
- ✅ Logs show successful export of position files
- ✅ No ERROR or CRITICAL messages in logs

**Failure Indicators:**
- ❌ Exit code != 0 → Runtime error
- ❌ Missing JSON files → Export failed
- ❌ CSV files created → Feature 2 not applied
- ❌ Errors in logs → Implementation issue

**Command to verify:**
```bash
python player-data-fetcher/player_data_fetcher_main.py
echo "Exit code: $?"  # Should be 0

# Count position JSON files (should be 6)
ls data/player_data/*.json | wc -l
```

---

### Test Scenario 4: League Helper Integration (All 4 Modes)

**Purpose:** Verify league helper works with updated data model in all modes

**Steps:**
1. Run player-data-fetcher (sets up data)
2. Launch league helper in each mode:
   - Draft mode (add_to_roster)
   - Optimizer mode (starter_helper)
   - Trade mode (trade_simulator)
   - Modify mode (modify_player_data)
3. Verify each mode loads players successfully

**Expected Results:**
- ✅ Draft mode: Loads players, shows recommendations
- ✅ Optimizer mode: Loads roster, calculates scores
- ✅ Trade mode: Loads teams, simulates trades
- ✅ Modify mode: Loads players, allows modifications
- ✅ All modes: Players have `drafted_by` field populated

**Failure Indicators:**
- ❌ Import errors → Module integration broken
- ❌ AttributeError on `drafted_by` → Field migration incomplete
- ❌ No players loaded → JSON loading broken
- ❌ Mode crashes → Unexpected field format

**Command to verify (draft mode):**
```bash
# Test draft mode
python run_league_helper.py --mode draft <<EOF
QB
exit
EOF
echo "Exit code: $?"  # Should be 0
```

---

### Test Scenario 5: SaveCalculatedPointsManager File Copy

**Purpose:** Verify SaveCalculatedPointsManager doesn't try to copy non-existent CSV files

**Steps:**
1. Run save_calculated_points mode (creates historical snapshot)
2. Verify it copies files successfully
3. Check that it does NOT try to copy players.csv

**Expected Results:**
- ✅ Historical snapshot created in `sim_data/{year}/weeks/week_NN/`
- ✅ Files copied: game_data.csv, drafted_data.csv
- ✅ NO attempt to copy: players.csv, players_projected.csv
- ✅ No file-not-found errors in logs

**Failure Indicators:**
- ❌ FileNotFoundError for players.csv → Feature 2 incomplete (SaveCalculatedPointsManager not updated)
- ❌ Missing snapshot files → Copy logic broken
- ❌ Snapshot folder not created → Mode failed

**Command to verify:**
```bash
# Run save mode (requires league helper)
python run_league_helper.py --mode save

# Check snapshot
ls sim_data/2025/weeks/week_*/  # Should have game_data.csv, drafted_data.csv (NOT players.csv)
```

---

### Test Scenario 6: Data Value Verification (drafted_by Field)

**Purpose:** Verify `drafted_by` field contains ACTUAL team names (not just non-empty strings)

**[UPDATED Stage 5e - feature_01]:** Enhanced with actual data values discovered during implementation

**Steps:**
1. Run player-data-fetcher to generate fresh data
2. Validate drafted_by field values across all position JSON files
3. Verify distribution matches expected (drafted vs free agents)
4. Confirm NO old integer values remain

**Expected Results:**
- ✅ Approximately 150-200 drafted players with team names (e.g., "The Injury Report", "Fishoutawater")
- ✅ Approximately 500-600 free agents with empty string ""
- ✅ Approximately 8-12 unique team names
- ✅ All drafted_by values are strings (no null, no integers)
- ✅ NO old integer string values ('0', '1', '2') present
- ✅ Team names have reasonable variety (not all same team)

**Failure Indicators:**
- ❌ All `drafted_by == ""` → DraftedRosterManager not applying team names
- ❌ Any `drafted_by = None` → Field not initialized properly
- ❌ Any `drafted_by in ['0', '1', '2']` → Old integer values leaked
- ❌ Only 1 team name → drafted_data.csv not loaded correctly
- ❌ 0 drafted players → Integration with DraftedRosterManager failed

**Command to verify:**
```python
# Create validation script
import json
from pathlib import Path

data_folder = Path("data/player_data")
all_drafted_by = []

# Load all position files
for pos_file in ["qb_data.json", "rb_data.json", "wr_data.json",
                 "te_data.json", "k_data.json", "dst_data.json"]:
    with open(data_folder / pos_file) as f:
        data_raw = json.load(f)
        data = list(data_raw.values())[0] if isinstance(data_raw, dict) else data_raw
        all_drafted_by.extend([p["drafted_by"] for p in data])

# Validate
drafted_count = sum(1 for d in all_drafted_by if d != "")
free_agent_count = sum(1 for d in all_drafted_by if d == "")
unique_teams = len(set(d for d in all_drafted_by if d != ""))
old_int_values = sum(1 for d in all_drafted_by if d in ['0', '1', '2'])

print(f"Total players: {len(all_drafted_by)}")
print(f"Drafted players: {drafted_count}")
print(f"Free agents: {free_agent_count}")
print(f"Unique teams: {unique_teams}")
print(f"Old integer values: {old_int_values}")

assert drafted_count > 100, f"Too few drafted players: {drafted_count}"
assert free_agent_count > 400, f"Too few free agents: {free_agent_count}"
assert unique_teams >= 8, f"Too few teams: {unique_teams}"
assert old_int_values == 0, f"Found old integer values: {old_int_values}"
print("✅ All validations passed")
```

**Why updated:** Feature_01 implementation revealed specific data distributions (154 drafted, 585 free agents, 10 teams) that Stage 4 plan didn't capture. This enhanced test verifies ACTUAL data values, not just "some drafted, some free".

---

### Test Scenario 7: DraftedRosterManager Integration

**Added:** Stage 5e (feature_01)

**Purpose:** Verify DraftedRosterManager.apply_drafted_state_to_players() correctly populates team names

**Steps:**
1. Verify DraftedRosterManager is actually called during player-data-fetcher execution
2. Check that team names come from drafted_data.csv
3. Validate integration point at player_data_exporter.py line 297

**Expected Results:**
- ✅ DraftedRosterManager.apply_drafted_state_to_players() is called in player_data_exporter.py (line 297)
- ✅ Team names in JSON files match teams in drafted_data.csv
- ✅ Players not in drafted_data.csv have drafted_by = "" (empty string)
- ✅ Players in drafted_data.csv have drafted_by = team name (string)

**Failure Indicators:**
- ❌ Line 297 not calling apply_drafted_state_to_players() → Integration missing
- ❌ Team names don't match drafted_data.csv → Wrong data source
- ❌ All players have empty drafted_by → Integration not working
- ❌ FileNotFoundError for drafted_data.csv → Missing dependency

**Command to verify:**
```bash
# Verify integration point exists
grep -n "apply_drafted_state_to_players" player-data-fetcher/player_data_exporter.py
# Should show line ~297 with the call

# Verify drafted_data.csv exists
test -f data/drafted_data.csv && echo "✅ drafted_data.csv exists" || echo "❌ MISSING: drafted_data.csv"

# Compare team names
python -c "
import json
import csv

# Load teams from drafted_data.csv
with open('data/drafted_data.csv') as f:
    reader = csv.DictReader(f)
    csv_teams = set(row['team'] for row in reader if row.get('team'))

# Load teams from JSON
with open('data/player_data/qb_data.json') as f:
    data = json.load(f)
    players = list(data.values())[0] if isinstance(data, dict) else data
    json_teams = set(p['drafted_by'] for p in players if p['drafted_by'] != '')

print(f'Teams in drafted_data.csv: {sorted(csv_teams)}')
print(f'Teams in JSON files: {sorted(json_teams)}')
assert csv_teams == json_teams, 'Team mismatch!'
print('✅ Teams match')
"
```

**Why added:** Feature_01 implementation revealed critical integration point at line 297 where DraftedRosterManager populates team names. Stage 4 plan mentioned DraftedRosterManager but didn't test the actual integration. This test verifies the integration works correctly.

---

### Test Scenario 8: Config Cleanup Verification

**Added:** Stage 5e (feature_01)

**Purpose:** Verify PRESERVE_DRAFTED_VALUES config was completely removed without breaking imports

**Steps:**
1. Check that PRESERVE_DRAFTED_VALUES no longer exists in config.py
2. Verify no import errors when loading config
3. Confirm PRESERVE_LOCKED_VALUES still works (wasn't accidentally removed)

**Expected Results:**
- ✅ config.py does NOT contain PRESERVE_DRAFTED_VALUES
- ✅ player_data_exporter.py does NOT import PRESERVE_DRAFTED_VALUES
- ✅ config.py still contains PRESERVE_LOCKED_VALUES (unchanged)
- ✅ No ImportError when loading config module

**Failure Indicators:**
- ❌ PRESERVE_DRAFTED_VALUES still in config.py → Cleanup incomplete
- ❌ Import of PRESERVE_DRAFTED_VALUES in player_data_exporter.py → Import not removed
- ❌ PRESERVE_LOCKED_VALUES missing → Accidentally deleted wrong constant
- ❌ ImportError on config module → Broken imports

**Command to verify:**
```bash
# Verify PRESERVE_DRAFTED_VALUES removed from config.py
! grep -q "PRESERVE_DRAFTED_VALUES" player-data-fetcher/config.py && echo "✅ PRESERVE_DRAFTED_VALUES removed" || echo "❌ FAILED: Still in config.py"

# Verify not imported in player_data_exporter.py
! grep -q "PRESERVE_DRAFTED_VALUES" player-data-fetcher/player_data_exporter.py && echo "✅ Not imported" || echo "❌ FAILED: Still imported"

# Verify PRESERVE_LOCKED_VALUES still exists (unchanged)
grep -q "PRESERVE_LOCKED_VALUES" player-data-fetcher/config.py && echo "✅ PRESERVE_LOCKED_VALUES preserved" || echo "❌ FAILED: Accidentally removed"

# Test module imports
python -c "from player-data-fetcher.config import PRESERVE_LOCKED_VALUES; print('✅ Config imports work')"
```

**Why added:** Feature_01 deleted PRESERVE_DRAFTED_VALUES constant and all related imports. This test ensures cleanup was complete and didn't break anything. Stage 4 plan didn't cover configuration cleanup verification.

---

### Test Scenario 9: Empty String Preservation

**Added:** Stage 5e (feature_01)

**Purpose:** Verify free agents correctly use empty string "" (not null, not "0", not undefined)

**Steps:**
1. Check that free agents have drafted_by = "" (empty string)
2. Verify empty strings are preserved through export/import cycle
3. Confirm no null/None values or integer strings

**Expected Results:**
- ✅ Free agents have drafted_by = "" exactly (empty string)
- ✅ No drafted_by = None (null values)
- ✅ No drafted_by = "0" (old integer as string)
- ✅ Empty strings preserved when JSON exported and re-imported

**Failure Indicators:**
- ❌ drafted_by = None → Field initialization failed
- ❌ drafted_by = "0" → Old integer value leaked
- ❌ drafted_by missing from JSON → Export broken
- ❌ Empty string becomes null on import → Round-trip issue

**Command to verify:**
```python
import json
from pathlib import Path

data_folder = Path("data/player_data")
all_players = []

# Load all position files
for pos_file in ["qb_data.json", "rb_data.json", "wr_data.json",
                 "te_data.json", "k_data.json", "dst_data.json"]:
    with open(data_folder / pos_file) as f:
        data_raw = json.load(f)
        data = list(data_raw.values())[0] if isinstance(data_raw, dict) else data_raw
        all_players.extend(data)

# Check free agents
free_agents = [p for p in all_players if p["drafted_by"] == ""]
null_values = [p for p in all_players if p["drafted_by"] is None]
zero_strings = [p for p in all_players if p["drafted_by"] == "0"]

print(f"Free agents (empty string): {len(free_agents)}")
print(f"Null values: {len(null_values)}")
print(f"Zero strings: {len(zero_strings)}")

assert len(free_agents) > 400, f"Too few free agents: {len(free_agents)}"
assert len(null_values) == 0, f"Found null values: {len(null_values)}"
assert len(zero_strings) == 0, f"Found '0' strings: {len(zero_strings)}"
print("✅ Empty string handling correct")
```

**Why added:** Feature_01 implementation uses empty string "" for free agents (not null, not "0"). This was an implementation detail not explicitly tested in Stage 4 plan. Important to verify empty strings are preserved correctly.

---

## High-Level Test Categories

**Agent will create additional scenarios for these categories during Stage 5e:**

### Category 1: Cross-Feature Integration
**What to test:** Features working together correctly
**Known integration points:**
- ESPNPlayerData → FantasyPlayer data model (both features modify)
- Position JSON export (Feature 1 changes field, Feature 2 relies on it)
- player-data-fetcher module (both features modify different files)
- config.py (both features modify different lines)
- Sequential dependency (Feature 2 depends on Feature 1)
- League helper integration (both features affect downstream system)

**Stage 5e will add:** Specific tests after seeing actual implementation

---

### Category 2: Error Handling
**What to test:** Graceful degradation when data missing or invalid
**Known error scenarios:**
- Missing drafted_data.csv (DraftedRosterManager dependency)
- Invalid ESPN API response
- Malformed JSON export

**Stage 5e will add:** Specific error scenarios discovered during implementation

---

### Category 3: Data Validation
**What to test:** All exported data uses correct field names and types
**Known validation needs:**
- `drafted_by` field is string type (not int)
- `drafted_by` contains team names or empty string (not 0/1/2)
- Position JSON schema matches FantasyPlayer model

**Stage 5e will add:** Validation checks after implementation

---

### Category 4: Performance
**What to test:** Epic doesn't slow down significantly
**Known performance concerns:**
- Removing CSV exports should speed up execution slightly
- No performance impact from field migration (same data, different name)

**Stage 5e will add:** Performance benchmarks after implementation

---

## Update Log

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| 2025-12-30 | Stage 1 | Initial plan created | Epic planning - assumptions only |
| 2025-12-30 | Stage 4 | **MAJOR UPDATE** | Based on feature specs (Stages 2-3) |
| 2025-12-31 | Stage 5e (Feature 1) | **Implementation-based updates** | feature_01 revealed integration points, data values, edge cases |

**Stage 4 changes:**
- Added 6 specific test scenarios with concrete commands (was 3 placeholders with TBD)
- Replaced 4 vague success criteria with 5 measurable criteria
- Identified 6 integration points between features (was 0)
- Added expected results and failure indicators for each test
- Documented actual file paths, grep patterns, Python verification code
- Updated from INITIAL to STAGE 4 version

**Stage 5e (feature_01) changes:**
- Enhanced Test Scenario 6 with ACTUAL data values (154 drafted, 585 free agents, 10 teams)
- Added Test Scenario 7: DraftedRosterManager integration (line 297 verification)
- Added Test Scenario 8: Config cleanup verification (PRESERVE_DRAFTED_VALUES removed)
- Added Test Scenario 9: Empty string preservation (free agents use "" not null)
- Updated Integration Point 1 with actual DraftedRosterManager flow
- Updated success criteria (no old integer values, empty strings preserved)

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request
- Stage 4: Feature specs and approved implementation plan
- **Stage 5e (feature_01): Actual implementation insights** ← YOU ARE HERE
- Stage 5e (feature_02): (Pending) Will update after feature_02 implementation

**Next update:** Stage 5e after feature_02 completes (will add CSV removal tests)

---

## Notes for Stage 5e Updates

**After Feature 1 implementation:**
- Add tests for actual ESPNPlayerData initialization
- Add tests for actual DraftedRosterManager integration
- Add error handling tests for edge cases discovered

**After Feature 2 implementation:**
- Add tests for actual export method removal
- Add tests for SaveCalculatedPointsManager file copy updates
- Add performance benchmarks (with/without CSV exports)

**After BOTH features complete:**
- Add integration tests combining both features
- Add regression tests for common user workflows
- Update success criteria based on actual implementation details
