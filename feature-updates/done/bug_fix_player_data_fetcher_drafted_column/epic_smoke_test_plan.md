# Epic Smoke Test Plan: bug_fix_player_data_fetcher_drafted_column

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 5e (Updated after ALL features implementation)**
- Created: 2025-12-30 (Stage 1)
- Last Updated: 2025-12-31 (Stage 5e - after feature_02)
- Based on: Feature_01 AND Feature_02 ACTUAL implementation insights (not just specs)
- Quality: EXECUTABLE - Concrete tests with actual data values verified
- Next Update: Stage 6 (Epic Final QC)

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

**[UPDATED Stage 5e - feature_02]:** Enhanced with actual method removal details

**Purpose:** Verify Feature 2 successfully removes deprecated CSV export calls and methods

**Steps:**
1. Verify export methods no longer exist in codebase
2. Verify PLAYERS_CSV constant removed from config
3. Delete old CSV files (if present)
4. Run player-data-fetcher
5. Check that CSV files were NOT recreated
6. Check that position JSON files WERE created

**Expected Results:**
- ✅ `export_to_data()` method NOT in player_data_exporter.py
- ✅ `export_projected_points_data()` method NOT in player_data_exporter.py
- ✅ `PLAYERS_CSV` constant NOT in config.py
- ✅ No import of PLAYERS_CSV in player_data_exporter.py
- ✅ `data/players.csv` does NOT exist after run
- ✅ `data/players_projected.csv` does NOT exist after run
- ✅ All 6 position JSON files DO exist
- ✅ No errors in player-data-fetcher logs

**Failure Indicators:**
- ❌ CSV files created → Export methods not removed
- ❌ Methods still in code → Feature 2 incomplete
- ❌ PLAYERS_CSV constant exists → Config not updated
- ❌ JSON files NOT created → Feature 1 or position export broken
- ❌ Errors in logs → Export logic broken

**Command to verify:**
```bash
# Verify methods removed
! grep -q "def export_to_data" player-data-fetcher/player_data_exporter.py && echo "✅ export_to_data removed" || echo "❌ FAILED: export_to_data exists"
! grep -q "def export_projected_points_data" player-data-fetcher/player_data_exporter.py && echo "✅ export_projected_points_data removed" || echo "❌ FAILED: export_projected_points_data exists"

# Verify config cleaned up
! grep -q "PLAYERS_CSV" player-data-fetcher/config.py && echo "✅ PLAYERS_CSV removed" || echo "❌ FAILED: PLAYERS_CSV exists"

# Clean old files
rm -f data/players.csv data/players_projected.csv

# Run fetcher
python player-data-fetcher/player_data_fetcher_main.py

# Verify
! test -f data/players.csv && echo "✅ players.csv NOT created" || echo "❌ FAILED: players.csv created"
! test -f data/players_projected.csv && echo "✅ players_projected.csv NOT created" || echo "❌ FAILED: players_projected.csv created"
test -f data/player_data/qb_data.json && echo "✅ JSON files created" || echo "❌ FAILED: JSON not created"
```

**Why updated:** Feature_02 implementation involved removing 2 complete methods (export_to_data, export_projected_points_data) and PLAYERS_CSV constant. Stage 4 plan just checked "CSV files not created" - now verifies the actual code removal.

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

**[UPDATED Stage 5e - feature_02]:** Enhanced with actual files_to_copy list changes (6 → 4 file types)

**Purpose:** Verify SaveCalculatedPointsManager copies only 4 file types (not 6) after CSV deprecation

**Steps:**
1. Verify files_to_copy list in SaveCalculatedPointsManager.py
2. Run save_calculated_points mode (creates historical snapshot)
3. Verify it copies files successfully
4. Check that it does NOT try to copy players.csv or players_projected.csv

**Expected Results:**
- ✅ files_to_copy list contains 4 file types (NOT 6):
  - Position JSON files (qb_data.json, rb_data.json, etc.) - 6 files
  - Team CSV files (team_data/*.csv)
  - Game data CSV (game_data.csv)
  - Drafted data CSV (drafted_data.csv)
- ✅ files_to_copy list does NOT contain:
  - players.csv (REMOVED)
  - players_projected.csv (REMOVED)
- ✅ Historical snapshot created in `sim_data/{year}/weeks/week_NN/`
- ✅ Position JSON files copied to snapshot
- ✅ game_data.csv and drafted_data.csv copied
- ✅ NO attempt to copy: players.csv, players_projected.csv
- ✅ No file-not-found errors in logs

**Failure Indicators:**
- ❌ FileNotFoundError for players.csv → files_to_copy not updated
- ❌ files_to_copy still has 6 types → Feature 2 incomplete
- ❌ Missing snapshot files → Copy logic broken
- ❌ Snapshot folder not created → Mode failed

**Command to verify:**
```bash
# Verify files_to_copy list updated
grep -A 10 "files_to_copy = \[" league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py
# Should NOT see "players.csv" or "players_projected.csv" in the list

# Run save mode (requires league helper)
python run_league_helper.py --mode save

# Check snapshot
ls sim_data/2025/weeks/week_*/
# Should have: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json, game_data.csv, drafted_data.csv
# Should NOT have: players.csv, players_projected.csv
```

**Why updated:** Feature_02 removed 2 entries from files_to_copy list (players.csv, players_projected.csv), reducing file types from 6 to 4. Stage 4 plan just checked "CSV files not copied" - now verifies the actual list changes and counts 4 file types.

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

### Test Scenario 10: _load_existing_locked_values() Migration to JSON

**Added:** Stage 5e (feature_02)

**Purpose:** Verify _load_existing_locked_values() loads from position JSON files (not deprecated CSV) when PRESERVE_LOCKED_VALUES enabled

**Steps:**
1. Verify _load_existing_locked_values() method in player_data_exporter.py
2. Check that it reads from position JSON files (not PLAYERS_CSV)
3. Enable PRESERVE_LOCKED_VALUES in config.py temporarily
4. Add locked values to position JSON files
5. Run player-data-fetcher and verify locked values preserved

**Expected Results:**
- ✅ _load_existing_locked_values() reads from qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
- ✅ NO reference to PLAYERS_CSV in method body
- ✅ Method handles both dict format `{position_data: [...]}` and list format `[...]`
- ✅ Boolean locked values converted to int (True → 1, False → 0)
- ✅ If PRESERVE_LOCKED_VALUES = True, locked values from JSON are preserved
- ✅ No NameError or undefined variable errors

**Failure Indicators:**
- ❌ NameError: PLAYERS_CSV undefined → Bug fix not applied
- ❌ Method still references players.csv → Not migrated to JSON
- ❌ Locked values not preserved → Method not working
- ❌ FileNotFoundError for position JSON → Wrong file path

**Command to verify:**
```bash
# Verify method loads from JSON files
grep -A 30 "def _load_existing_locked_values" player-data-fetcher/player_data_exporter.py | grep "json"
# Should see references to position JSON files (qb_data.json, rb_data.json, etc.)

# Verify NO reference to PLAYERS_CSV
! grep -A 30 "def _load_existing_locked_values" player-data-fetcher/player_data_exporter.py | grep "PLAYERS_CSV" && echo "✅ No PLAYERS_CSV reference" || echo "❌ FAILED: Still uses PLAYERS_CSV"

# Test with PRESERVE_LOCKED_VALUES = True (optional integration test)
python -c "
import sys
sys.path.append('player-data-fetcher')
from player_data_exporter import PlayerDataExporter

exporter = PlayerDataExporter('data/')
# If PRESERVE_LOCKED_VALUES = True in config, this should work without NameError
try:
    exporter._load_existing_locked_values()
    print('✅ Method works (no NameError)')
except NameError as e:
    print(f'❌ FAILED: {e}')
"
```

**Why added:** Feature_02 QC Round 3 discovered critical bug - _load_existing_locked_values() referenced deleted PLAYERS_CSV constant. Bug fix rewrote method to load from position JSON files. This test ensures the bug fix works correctly and method doesn't crash if PRESERVE_LOCKED_VALUES enabled.

---

### Test Scenario 11: CSV Cleanup Documentation

**Added:** Stage 5e (feature_02)

**Purpose:** Verify CSV_CLEANUP_GUIDE.md exists and provides clear instructions for users

**Steps:**
1. Check that CSV_CLEANUP_GUIDE.md exists
2. Verify it contains cleanup options (delete, backup, keep)
3. Verify it explains impact of each option
4. Confirm it has verification steps

**Expected Results:**
- ✅ CSV_CLEANUP_GUIDE.md exists in feature_02 folder
- ✅ Guide contains at least 3 cleanup options
- ✅ Guide explains migration impact
- ✅ Guide has verification steps
- ✅ Guide has troubleshooting section

**Failure Indicators:**
- ❌ CSV_CLEANUP_GUIDE.md missing → Documentation not created
- ❌ Guide lacks cleanup options → Incomplete guidance
- ❌ No verification steps → Users can't validate cleanup

**Command to verify:**
```bash
# Verify guide exists
test -f "feature-updates/bug_fix_player_data_fetcher_drafted_column/feature_02_disable_deprecated_csv_exports/CSV_CLEANUP_GUIDE.md" && echo "✅ CSV_CLEANUP_GUIDE.md exists" || echo "❌ FAILED: Guide missing"

# Verify content (basic check)
grep -q "Cleanup Options" "feature-updates/bug_fix_player_data_fetcher_drafted_column/feature_02_disable_deprecated_csv_exports/CSV_CLEANUP_GUIDE.md" && echo "✅ Has cleanup options" || echo "❌ FAILED: Missing cleanup options"
grep -q "Verification" "feature-updates/bug_fix_player_data_fetcher_drafted_column/feature_02_disable_deprecated_csv_exports/CSV_CLEANUP_GUIDE.md" && echo "✅ Has verification steps" || echo "❌ FAILED: Missing verification"
```

**Why added:** Feature_02 implementation created CSV_CLEANUP_GUIDE.md to help users manage deprecated CSV files after migration. This test ensures the documentation exists and is useful. Stage 4 plan didn't account for user-facing documentation.

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
| 2025-12-31 | Stage 5e (Feature 2) | **CSV deprecation updates** | feature_02 revealed method removals, bug fixes, file list changes |

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

**Stage 5e (feature_02) changes:**
- Enhanced Test Scenario 2 with method removal verification (export_to_data, export_projected_points_data, PLAYERS_CSV)
- Enhanced Test Scenario 5 with actual file list changes (6 → 4 file types in files_to_copy)
- Added Test Scenario 10: _load_existing_locked_values() migration to JSON (QC Round 3 bug fix)
- Added Test Scenario 11: CSV_CLEANUP_GUIDE.md documentation verification
- Verified PLAYERS_CSV constant completely removed from codebase
- Confirmed SaveCalculatedPointsManager updated to skip deprecated CSV files

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request
- Stage 4: Feature specs and approved implementation plan
- Stage 5e (feature_01): Actual implementation insights (DraftedRosterManager integration, data values)
- **Stage 5e (feature_02): Actual implementation insights (method removals, bug fixes, file list changes)** ← YOU ARE HERE

**Next update:** Stage 6 (Epic Final QC) - will execute all scenarios against complete epic

---

## Stage 5e Update Summary

**✅ Feature 1 implementation updates (COMPLETE):**
- ✅ Added tests for actual ESPNPlayerData initialization
- ✅ Added tests for actual DraftedRosterManager integration (Test Scenario 7)
- ✅ Added error handling tests for edge cases discovered (Test Scenarios 8, 9)

**✅ Feature 2 implementation updates (COMPLETE):**
- ✅ Added tests for actual export method removal (Test Scenario 2 enhanced)
- ✅ Added tests for SaveCalculatedPointsManager file copy updates (Test Scenario 5 enhanced)
- ✅ Added tests for _load_existing_locked_values() bug fix (Test Scenario 10)
- ✅ Added CSV_CLEANUP_GUIDE.md verification (Test Scenario 11)

**Both features complete - Ready for Stage 6:**
- ✅ All 11 test scenarios defined with executable commands
- ✅ All integration points documented
- ✅ Success criteria measurable and verifiable
- ✅ Epic test plan ready for execution in Stage 6 (Epic Final QC)
