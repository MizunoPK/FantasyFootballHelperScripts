# Feature 1: Update Data Models and Field Migration - Detailed Specification (REVISED)

**Created:** 2025-12-30 (Stage 1)
**Detailed:** 2025-12-30 (Stage 2 - Phase 2)
**Revised:** 2025-12-30 (Corrected after user clarification)

---

## Objective

Migrate player-data-fetcher from old `drafted: int` field to new `drafted_by: str` field to match FantasyPlayer schema. This is a simple field migration with NO CSV preservation needed (players.csv is deprecated).

---

## Root Cause Analysis

**Error:** `_espn_player_to_fantasy_player()` and `_get_drafted_by()` try to access `player.drafted` (int field), but FantasyPlayer only has `player.drafted_by` (str field).

**Why this happened:**
- FantasyPlayer was migrated from `drafted: int` → `drafted_by: str` in previous epic
- ESPNPlayerData model was NOT migrated (still uses `drafted: int`)
- Conversion and helper methods still reference old field

**Impact:**
- Player data fetcher crashes when creating FantasyPlayer objects
- Position JSON exports fail (qb_data.json, rb_data.json, etc.)
- End-to-end execution broken

---

## KEY CLARIFICATION: No CSV Preservation

**Important Understanding:**
- `drafted_by` is a FIELD in JSON files (position JSON exports)
- There is NO `drafted_by` column in CSV files
- `players.csv` and `players_projected.csv` are DEPRECATED (Feature 2 removes them)
- Therefore: **NO backward compatibility or CSV preservation logic needed!**

**Data Flow:**
```
ESPNPlayerData (drafted: int)
  → FantasyPlayer (drafted_by: str)
  → DraftedRosterManager applies team names from drafted_data.csv
  → Position JSON export (drafted_by field in JSON)
```

---

## Components Affected (REVISED - Simpler!)

### 1. ESPNPlayerData Model
**File:** `player-data-fetcher/player_data_models.py`
**Line:** 41

**Current:**
```python
drafted: int = 0  # 0 = not drafted, 1 = drafted, 2 = roster player
```

**Required Change:**
```python
drafted_by: str = ""  # Team name (empty = free agent)
```

---

### 2. ESPNClient Player Creation
**File:** `player-data-fetcher/espn_client.py`
**Line:** 1833

**Current:**
```python
drafted=0,  # Initialize all players as not drafted
```

**Required Change:**
```python
drafted_by="",  # Initialize all players as free agents
```

---

### 3. DataExporter Conversion Logic
**File:** `player-data-fetcher/player_data_exporter.py`
**Lines:** 274-320

**Current (BROKEN):**
```python
def _espn_player_to_fantasy_player(self, player_data: ESPNPlayerData) -> FantasyPlayer:
    drafted_value = player_data.drafted  # ← OLD FIELD (int)

    if PRESERVE_DRAFTED_VALUES and player_data.id in self.existing_drafted_values:
        drafted_value = self.existing_drafted_values[player_data.id]  # ← DEPRECATED LOGIC

    return FantasyPlayer(
        ...
        drafted=drafted_value,  # ← ERROR: FantasyPlayer has no 'drafted' parameter
        ...
    )
```

**Required Changes:**
```python
def _espn_player_to_fantasy_player(self, player_data: ESPNPlayerData) -> FantasyPlayer:
    drafted_by_value = player_data.drafted_by  # ← NEW FIELD (str)

    # REMOVE preservation logic (players.csv is deprecated)

    return FantasyPlayer(
        ...
        drafted_by=drafted_by_value,  # ← CORRECT parameter
        ...
    )
```

**Impact:** Fixes TypeError, removes deprecated preservation logic

---

### 4. Helper Method: `_get_drafted_by()` ✅ DECISION: Simplify to Return Field
**File:** `player-data-fetcher/player_data_exporter.py`
**Lines:** 544-552

**Current (BROKEN):**
```python
def _get_drafted_by(self, player: FantasyPlayer) -> str:
    if player.drafted == 0:  # ← ERROR: player has no 'drafted' field!
        return ""
    elif player.drafted == 2:
        return MY_TEAM_NAME
    else:
        return self.drafted_roster_manager.get_team_name_for_player(player)
```

**Required Change (APPROVED - Option A):**
```python
def _get_drafted_by(self, player: FantasyPlayer) -> str:
    """Get drafted_by value from player (team name or empty string)"""
    return player.drafted_by  # Player already has correct value!
```

**Why this works:**
- FantasyPlayer already has `drafted_by` field with correct value
- DraftedRosterManager already applied team names
- No conversion needed - just return the field!
- Maintains abstraction layer for future flexibility

**Used by:** Position JSON export (line 500: `"drafted_by": self._get_drafted_by(player)`)

---

### 5. Preservation Logic: `_load_existing_drafted_values()` - REMOVE ENTIRELY
**File:** `player-data-fetcher/player_data_exporter.py`
**Lines:** 236-240

**Current:**
```python
def _load_existing_drafted_values(self):
    # Reads from players.csv (DEPRECATED file)
    ...
```

**Required Action:** **DELETE this method entirely**

**Reason:** Reads from deprecated `players.csv` file which is being removed in Feature 2

---

### 6. Preservation Logic in `__init__()` - REMOVE
**File:** `player-data-fetcher/player_data_exporter.py`
**Lines:** 60-61

**Current:**
```python
if PRESERVE_DRAFTED_VALUES:
    self._load_existing_drafted_values()
```

**Required Action:** **DELETE these lines**

**Also remove:** `self.existing_drafted_values = {}` initialization (line 58)

---

### 7. EXPORT_COLUMNS Configuration
**File:** `player-data-fetcher/config.py`
**Line:** 84

**Current:**
```python
EXPORT_COLUMNS = [
    'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
    'injury_status', 'drafted', 'locked', ...  # ← 'drafted' here
]
```

**Required Change:**
```python
EXPORT_COLUMNS = [
    'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
    'injury_status', 'drafted_by', 'locked', ...  # ← 'drafted_by'
]
```

---

### 8. PRESERVE_DRAFTED_VALUES Config Option - REMOVE ENTIRELY ✅
**File:** `player-data-fetcher/config.py`
**Line:** 17

**Current:**
```python
PRESERVE_DRAFTED_VALUES = False   # Keep draft status between data updates
```

**Decision:** ✅ **REMOVE ENTIRELY** (User approved Option A)

**User's Rationale:** "It has never been used since the introduction of drafted_data.csv anyway"

**Required Actions:**
- Delete line 17 from config.py
- Remove from imports in player_data_exporter.py
- Remove all usage in code (if-statements, initialization)

---

## Data Structures

### Field Mapping

| Old Field (ESPNPlayerData) | New Field (ESPNPlayerData) | FantasyPlayer Field | JSON Export |
|----------------------------|----------------------------|---------------------|-------------|
| `drafted: int = 0` | `drafted_by: str = ""` | `drafted_by: str = ""` | `"drafted_by": ""` |

**No conversion needed** - just use string field throughout!

---

## Algorithms

### Algorithm: ESPNPlayerData → FantasyPlayer Conversion (SIMPLIFIED)

**Pseudocode:**
```
FUNCTION _espn_player_to_fantasy_player(player_data: ESPNPlayerData) -> FantasyPlayer:
    # Step 1: Get drafted_by value from ESPN data
    drafted_by_value = player_data.drafted_by  # Simple field access

    # Step 2: Create FantasyPlayer
    player = FantasyPlayer(
        id=player_data.id,
        name=player_data.name,
        team=player_data.team,
        position=player_data.position,
        drafted_by=drafted_by_value,  # Pass string value
        ...
    )

    RETURN player

# Note: DraftedRosterManager applies team names in post-processing
# No preservation logic needed here!
```

**Complexity:** LOW (simple field mapping, no conversion)

---

## Dependencies

**This feature depends on:**
- ✅ FantasyPlayer class (already has `drafted_by` field)
- ✅ DraftedRosterManager (already uses `drafted_by` field, reads from `drafted_data.csv`)

**This feature blocks:**
- Feature 2: Disable Deprecated CSV File Exports

**This feature is independent of:**
- (No parallel features)

---

## Testing Strategy

### Unit Tests:

1. **test_player_data_models.py**
   - Test ESPNPlayerData with `drafted_by: str` field
   - Verify default value is "" (empty string)

2. **test_player_data_exporter.py**
   - Test `_espn_player_to_fantasy_player()` conversion
   - Test `_get_drafted_by()` returns player.drafted_by directly
   - Verify preservation logic removed

3. **test_espn_client.py**
   - Test player creation with `drafted_by=""` default

### Integration Tests:

1. **End-to-End Flow:**
   - Fetch players → Convert to FantasyPlayer → Export to position JSON
   - Verify `drafted_by` field present in JSON output (qb_data.json, etc.)
   - Verify no `drafted` field in output

2. **DraftedRosterManager Integration:**
   - Load `drafted_data.csv` → Apply to players → Verify `drafted_by` field set correctly

---

## Files Modified Summary (REVISED)

| File | Lines Changed | Complexity | Risk |
|------|---------------|------------|------|
| player_data_models.py | 1 | LOW | LOW |
| espn_client.py | 1 | LOW | LOW |
| player_data_exporter.py (conversion) | 3 | LOW | LOW |
| player_data_exporter.py (_get_drafted_by) | 8 | LOW | LOW |
| player_data_exporter.py (remove preservation) | -15 | LOW | LOW |
| config.py (EXPORT_COLUMNS) | 1 | LOW | LOW |
| config.py (PRESERVE_DRAFTED_VALUES - optional) | -3 | LOW | LOW |

**Total Estimated Changes:** ~20 lines modified, ~18 lines removed = ~38 lines total
**Overall Complexity:** LOW (down from MEDIUM!)
**Overall Risk:** LOW (down from MEDIUM!)

---

## Implementation Checklist (SIMPLIFIED)

**High-Level Tasks:**
1. Update ESPNPlayerData model: `drafted: int = 0` → `drafted_by: str = ""`
2. Update ESPNClient player creation: `drafted=0` → `drafted_by=""`
3. Update conversion in `_espn_player_to_fantasy_player()`:
   - Change `player_data.drafted` → `player_data.drafted_by`
   - Remove preservation logic (lines 280-282)
   - Change `drafted=` → `drafted_by=` parameter
4. Simplify `_get_drafted_by()`: return `player.drafted_by` directly
5. Remove `_load_existing_drafted_values()` method
6. Remove preservation logic from `__init__()` (lines 58, 60-61)
7. Update EXPORT_COLUMNS: `'drafted'` → `'drafted_by'`
8. (OPTIONAL) Remove or deprecate PRESERVE_DRAFTED_VALUES config
9. Update unit tests
10. Run end-to-end test

**Estimated Total Tasks:** ~15 items (down from 20!)

---

## Open Questions (See checklist.md)

**All questions resolved:**
1. ~~Should we remove PRESERVE_DRAFTED_VALUES config option entirely?~~ ✅ RESOLVED - Remove entirely
2. ~~Should `_get_drafted_by()` just return `player.drafted_by` directly?~~ ✅ RESOLVED - Simplify to return field (Option A)

---

**Status:** Spec complete with all decisions finalized (Stage 2 - Phase 3 complete)
**Next:** Phase 4 - Dynamic Scope Adjustment, Phase 5 - Cross-Feature Alignment
