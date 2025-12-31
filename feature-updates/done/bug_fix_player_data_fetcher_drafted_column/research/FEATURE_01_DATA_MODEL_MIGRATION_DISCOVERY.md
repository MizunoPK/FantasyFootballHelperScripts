# Feature 01: Update Data Models and Field Migration - Discovery Findings

**Research Date:** 2025-12-30
**Researcher:** Agent
**Feature:** feature_01_update_data_models_and_field_migration

---

## Problem Statement

**Root Cause:**
- ESPNPlayerData model uses OLD field: `drafted: int` (0/1/2)
- FantasyPlayer class uses NEW field: `drafted_by: str` (team name or empty)
- Conversion logic in `_espn_player_to_fantasy_player()` tries to pass `drafted=` to FantasyPlayer constructor
- **Error:** FantasyPlayer constructor doesn't accept `drafted` parameter (removed in previous migration)

---

## Components Identified

### 1. ESPNPlayerData Model
**File:** `player-data-fetcher/player_data_models.py`
**Line:** 41
**Current State:**
```python
drafted: int = 0  # 0 = not drafted, 1 = drafted, 2 = roster player
```

**Required Change:**
- Remove `drafted: int` field
- Add `drafted_by: str = ""` field (team name or empty string)

---

### 2. ESPNClient Player Creation
**File:** `player-data-fetcher/espn_client.py`
**Line:** 1833
**Current State:**
```python
drafted=0,  # Initialize all players as not drafted
```

**Required Change:**
- Change to `drafted_by="",  # Initialize all players as free agents`

---

### 3. DataExporter Conversion Logic
**File:** `player-data-fetcher/player_data_exporter.py`
**Line:** 274-320 (method `_espn_player_to_fantasy_player()`)

**Current State:**
```python
def _espn_player_to_fantasy_player(self, player_data: ESPNPlayerData) -> FantasyPlayer:
    # Lines 278-282: Get drafted_value from preservation logic
    drafted_value = player_data.drafted  # ← Uses old field

    if PRESERVE_DRAFTED_VALUES and player_data.id in self.existing_drafted_values:
        drafted_value = self.existing_drafted_values[player_data.id]

    # Line 310: Pass to FantasyPlayer constructor
    return FantasyPlayer(
        ...
        drafted=drafted_value,  # ← ERROR: FantasyPlayer has no 'drafted' parameter
        ...
    )
```

**Required Changes:**
- Line 278: Change `player_data.drafted` → `player_data.drafted_by`
- Lines 280-282: Update preservation logic to work with `drafted_by: str` instead of `drafted: int`
- Line 310: Change `drafted=drafted_value` → `drafted_by=drafted_by_value`

---

###4. Helper Method: `_get_drafted_by()`
**File:** `player-data-fetcher/player_data_exporter.py`
**Line:** 544-548

**Current State:**
```python
def _get_drafted_by(self, player: FantasyPlayer) -> str:
    if player.drafted == 0:
        return ""  # Free agent
    elif player.drafted == 2:
        return MY_TEAM_NAME  # Our roster
    else:
        return "OPPONENT"  # Opponent team
```

**Status:** This method appears to be converting FROM the old `drafted: int` field TO the new `drafted_by: str` field.

**Required Change:**
- This method may no longer be needed (players already have `drafted_by` field)
- OR needs to be updated to work directly with `drafted_by` field
- Need to check all callers of this method

---

### 5. EXPORT_COLUMNS Configuration
**File:** `player-data-fetcher/config.py`
**Line:** 82-92

**Current State:**
```python
EXPORT_COLUMNS = [
    'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
    'injury_status', 'drafted', 'locked', 'average_draft_position',  # ← 'drafted' here
    'player_rating',
    ...
]
```

**Required Change:**
- Replace `'drafted'` with `'drafted_by'` in EXPORT_COLUMNS list

---

### 6. Preservation Logic: `_load_existing_drafted_values()`
**File:** `player-data-fetcher/player_data_exporter.py`
**Line:** 236-240

**Current State:**
```python
def _load_existing_drafted_values(self):
    # Reads old CSV and extracts drafted column (int values)
    drafted_value = int(row.get('drafted', 0))
    self.existing_drafted_values[player_id] = drafted_value
```

**Required Changes:**
- Update to read `drafted_by` column (string values) instead of `drafted` column (int values)
- Store as strings in `self.existing_drafted_values` dictionary
- OR rename dictionary to `self.existing_drafted_by_values` for clarity

---

### 7. DraftedRosterManager Integration
**File:** `player-data-fetcher/player_data_exporter.py`
**Line:** 326-327

**Current State:**
```python
# Apply drafted data from CSV file to players using DraftedRosterManager
fantasy_players = self.drafted_roster_manager.apply_drafted_state_to_players(fantasy_players)
```

**Status:** DraftedRosterManager already uses `drafted_by` field (confirmed from grep results showing `matched_player.drafted_by = fantasy_team`)

**Required Change:** None - DraftedRosterManager already works with new field

---

## Data Flow Analysis

**Current (BROKEN) Flow:**
```
1. ESPNClient creates ESPNPlayerData with drafted: int = 0
2. DataExporter._espn_player_to_fantasy_player() reads player_data.drafted (int)
3. Tries to create FantasyPlayer(drafted=int_value)  ← ERROR: Parameter doesn't exist
4. FantasyPlayer expects drafted_by: str, not drafted: int
```

**Target (FIXED) Flow:**
```
1. ESPNClient creates ESPNPlayerData with drafted_by: str = ""
2. DataExporter._espn_player_to_fantasy_player() reads player_data.drafted_by (str)
3. Creates FantasyPlayer(drafted_by=str_value)  ← WORKS: Parameter matches
4. FantasyPlayer receives drafted_by: str correctly
```

---

## Preservation Logic Migration

**OLD Preservation (drafted: int):**
```python
# Store: {player_id: int}  (e.g., {12345: 2})
self.existing_drafted_values = {"12345": 2, "67890": 0}

# Apply:
drafted_value = self.existing_drafted_values.get(player_id, 0)  # int
return FantasyPlayer(drafted=drafted_value)
```

**NEW Preservation (drafted_by: str):**
```python
# Store: {player_id: str}  (e.g., {12345: "Sea Sharp"})
self.existing_drafted_by_values = {"12345": "Sea Sharp", "67890": ""}

# Apply:
drafted_by_value = self.existing_drafted_by_values.get(player_id, "")  # str
return FantasyPlayer(drafted_by=drafted_by_value)
```

---

## Edge Cases Identified

### Edge Case 1: PRESERVE_DRAFTED_VALUES Enabled
**Scenario:** User has `PRESERVE_DRAFTED_VALUES = True` in config
**Current Behavior:** Reads old CSV with `drafted` column (int values)
**Required Behavior:** Read old CSV with `drafted_by` column (string values)
**Migration Path:**
- Update `_load_existing_drafted_values()` to read `drafted_by` column
- Handle missing column gracefully (if old CSV still has `drafted` column, convert int→str)

### Edge Case 2: LOAD_DRAFTED_DATA_FROM_FILE Enabled
**Scenario:** User has `LOAD_DRAFTED_DATA_FROM_FILE = True` in config
**Current Behavior:** DraftedRosterManager loads CSV and applies `drafted_by` field
**Required Behavior:** No change (already uses `drafted_by`)
**Status:** ✅ Already compatible (DraftedRosterManager updated in previous migration)

### Edge Case 3: Both Preservation Options Disabled
**Scenario:** Both `PRESERVE_DRAFTED_VALUES = False` and `LOAD_DRAFTED_DATA_FROM_FILE = False`
**Current Behavior:** All players get `drafted=0` (free agents)
**Required Behavior:** All players get `drafted_by=""` (free agents)
**Migration:** Simple - just use empty string instead of 0

### Edge Case 4: Existing CSV Files with `drafted` Column
**Scenario:** User has old CSV files with `drafted: int` column
**Required Behavior:** Gracefully handle during preservation (convert int→str if needed)
**Conversion Logic:**
```python
# If old CSV has drafted: int
if 'drafted' in row and 'drafted_by' not in row:
    drafted_int = int(row['drafted'])
    if drafted_int == 0:
        drafted_by = ""
    elif drafted_int == 2:
        drafted_by = MY_TEAM_NAME
    else:
        drafted_by = "OPPONENT"  # Or skip unknown values
```

---

## Dependencies and Integration Points

### Dependencies (What This Feature Needs):
- FantasyPlayer class structure (already has `drafted_by` field) ✅
- DraftedRosterManager (already uses `drafted_by` field) ✅
- Configuration constants (PRESERVE_DRAFTED_VALUES, LOAD_DRAFTED_DATA_FROM_FILE, MY_TEAM_NAME) ✅

### Integration Points (What Uses This Feature):
- Position JSON exports (read from FantasyPlayer objects, will automatically use `drafted_by`)
- CSV exports (players.csv, players_projected.csv) - handled by Feature 2
- DraftedRosterManager (already compatible)

---

## Similar Existing Patterns

### Pattern: Field Migration in FantasyPlayer
**Source:** `utils/FantasyPlayer.py`
**Pattern Found:** Previous migration from `drafted: int` to `drafted_by: str`
- Added `drafted_by: str` field
- Removed `drafted: int` field
- Added helper methods: `is_rostered()`, `is_free_agent()`, `is_drafted_by_opponent()`

**Reusable Approach:**
- Same pattern applies to ESPNPlayerData
- Can follow same helper method pattern if needed

---

## Files Affected Summary

**Confirmed Files to Modify:**
1. ✅ `player-data-fetcher/player_data_models.py` (ESPNPlayerData model - Line 41)
2. ✅ `player-data-fetcher/espn_client.py` (Player creation - Line 1833)
3. ✅ `player-data-fetcher/player_data_exporter.py` (Conversion logic - Lines 278, 282, 310)
4. ✅ `player-data-fetcher/player_data_exporter.py` (Preservation logic - Lines 236-240)
5. ✅ `player-data-fetcher/player_data_exporter.py` (`_get_drafted_by()` method - Lines 544-548)
6. ✅ `player-data-fetcher/config.py` (EXPORT_COLUMNS - Line 84)

**Files Already Compatible (No Changes Needed):**
- ✅ `utils/FantasyPlayer.py` (already has `drafted_by` field)
- ✅ `utils/DraftedRosterManager.py` (already uses `drafted_by` field)

---

## Existing Test Patterns

**Test files to update/create:**
- `tests/player-data-fetcher/test_player_data_models.py` (test ESPNPlayerData model)
- `tests/player-data-fetcher/test_player_data_exporter.py` (test conversion logic)
- `tests/player-data-fetcher/test_espn_client.py` (test player creation)

**Pattern to follow:**
- Use pytest fixtures for sample ESPNPlayerData
- Mock DraftedRosterManager
- Test conversion with different `drafted_by` values ("", "Sea Sharp", "Opponent")

---

## Algorithm: ESPNPlayerData → FantasyPlayer Conversion

**Pseudocode:**
```
1. Create ESPNPlayerData with drafted_by: str = ""
2. For each player in ESPN data:
   a. Get drafted_by value from player_data.drafted_by

   b. If PRESERVE_DRAFTED_VALUES enabled:
      - Load existing drafted_by values from old CSV
      - Use preserved value if found: drafted_by = existing_drafted_by_values[player_id]

   c. Create FantasyPlayer with:
      - drafted_by = drafted_by_value (string)

   d. If LOAD_DRAFTED_DATA_FROM_FILE enabled:
      - DraftedRosterManager.apply_drafted_state_to_players() updates drafted_by field

3. Return list of FantasyPlayer objects with correct drafted_by values
```

---

## Next Steps for Phase 2 (Update Spec)

1. Update `spec.md` with:
   - Detailed component changes (all 6 files above)
   - Algorithm pseudocode (conversion logic)
   - Edge case handling (4 edge cases documented)
   - Data structure changes (int → str migration)

2. Create `checklist.md` with open questions:
   - How to handle backward compatibility with old CSV files?
   - Should `_get_drafted_by()` be removed or updated?
   - Should `existing_drafted_values` be renamed to `existing_drafted_by_values`?

3. Document findings in feature README.md

---

**Research Complete:** All components identified, data flow understood, edge cases documented.
