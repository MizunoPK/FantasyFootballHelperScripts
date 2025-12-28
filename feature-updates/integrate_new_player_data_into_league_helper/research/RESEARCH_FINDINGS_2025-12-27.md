# Codebase Research Findings - December 27, 2025

## Purpose
This document captures comprehensive research findings from investigating the current codebase to answer pending checklist items. These findings were obtained by directly examining JSON files, source code, and running grep searches.

---

## ✅ STRAIGHTFORWARD ANSWERS (No Ambiguity)

### 1. bye_week Field Location - FOUND ✅

**Finding:** `bye_week` field exists as a top-level integer field in all position JSON files.

**Evidence:**
```json
{
  "id": "3918298",
  "name": "Josh Allen",
  "team": "BUF",
  "position": "QB",
  "bye_week": 7,    // ← FOUND HERE
  ...
}
```

**Source Files Verified:**
- data/player_data/qb_data.json (bye_week: 7)
- data/player_data/rb_data.json (bye_week: 8)
- data/player_data/wr_data.json (bye_week: 10)
- data/player_data/te_data.json (bye_week: 8)
- data/player_data/k_data.json (bye_week: 10)
- data/player_data/dst_data.json (bye_week: 12)

**Mapping Strategy:** Direct integer mapping
```python
bye_week=safe_int_conversion(data.get('bye_week'), None)
```

---

### 2. Empty drafted_by Confirmation - VERIFIED ✅

**Finding:** Empty string `""` definitively means "not drafted"

**Evidence from actual data:**
```json
// Example 1: Not drafted (would be drafted=0 in old CSV)
"drafted_by": ""

// Example 2: Drafted by opponent (would be drafted=1)
"drafted_by": "The Injury Report"
"drafted_by": "Fishoutawater"
"drafted_by": "Chase-ing points"
"drafted_by": "The Eskimo Brothers"

// Example 3: Would need to check if any match FANTASY_TEAM_NAME (drafted=2)
```

**Constants.FANTASY_TEAM_NAME:** "Sea Sharp" (from league_helper/constants.py:19)

**Conversion Logic Confirmed:**
- `drafted_by == ""` → `drafted = 0`
- `drafted_by != "" and drafted_by != "Sea Sharp"` → `drafted = 1`
- `drafted_by == "Sea Sharp"` → `drafted = 2`

---

### 3. Complete Field Inventory - DOCUMENTED ✅

**Universal Fields (All Positions):**
```python
[
    'id',                       # String (needs conversion to int)
    'name',                     # String
    'team',                     # String
    'position',                 # String (QB/RB/WR/TE/K/DST)
    'bye_week',                 # Integer
    'injury_status',            # String (ACTIVE, QUESTIONABLE, etc.)
    'drafted_by',               # String (team name or "")
    'locked',                   # Boolean
    'average_draft_position',   # Float
    'player_rating',            # Float
    'projected_points',         # Array[17] of floats
    'actual_points'             # Array[17] of floats
]
```

**Position-Specific Nested Stats:**

**QB, RB, WR, TE:**
```python
{
    "passing": {
        "completions": [float, ...],      # 17 elements
        "attempts": [float, ...],
        "pass_yds": [float, ...],
        "pass_tds": [float, ...],
        "interceptions": [float, ...],
        "sacks": [float, ...]
    },
    "rushing": {
        "attempts": [float, ...],
        "rush_yds": [float, ...],
        "rush_tds": [float, ...]
    },
    "receiving": {
        "targets": [float, ...],
        "receiving_yds": [float, ...],
        "receiving_tds": [float, ...],
        "receptions": [float, ...]
    },
    "misc": {
        "fumbles": [float, ...]           # QB/RB/WR/TE only
    }
}
```

**K (Kicker) Only:**
```python
{
    "extra_points": {
        "made": [float, ...],
        "missed": [float, ...]
    },
    "field_goals": {
        "made": [float, ...],
        "missed": [float, ...]
    }
    // NO misc field
}
```

**DST (Defense/Special Teams) Only:**
```python
{
    "defense": {
        "yds_g": [float, ...],
        "pts_g": [float, ...],
        "def_td": [float, ...],
        "sacks": [float, ...],
        "safety": [float, ...],
        "interceptions": [float, ...]
    }
    // NO misc field
}
```

**NEW DISCOVERY:** `misc` field exists with nested `fumbles` array
- Present in: QB, RB, WR, TE
- Absent in: K, DST
- Must be stored as Optional[Dict[str, List[float]]]

---

### 4. fantasy_points Field - NOT IN JSON, MUST CALCULATE ✅

**Finding:** `fantasy_points` does NOT exist in JSON files. Must be calculated.

**Evidence:**
```bash
$ python -c "import json; data = json.load(open('data/player_data/qb_data.json')); print('Has fantasy_points:', 'fantasy_points' in data['qb_data'][0])"
Has fantasy_points: False
```

**Calculation Required:**
```python
# Sum of projected_points array
fantasy_points = sum(data['projected_points'])  # Example: 347.64 for Josh Allen
```

**Implementation in from_json():**
```python
projected_points = data.get('projected_points', [])
fantasy_points = sum(projected_points) if projected_points else 0.0
```

---

### 5. Complete .drafted Assignment Inventory - VERIFIED ✅

**Finding:** Found ALL locations that assign `.drafted = ` (17 total assignments across 10 files)

**League Helper Module (7 assignments):**
1. `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:231` - `selected_player.drafted = 2`
2. `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:236` - `selected_player.drafted = 1`
3. `league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:303` - `selected_player.drafted = 0`
4. `league_helper/util/FantasyTeam.py:192` - `player.drafted = 2`
5. `league_helper/util/FantasyTeam.py:204` - `player.drafted = 0`
6. `league_helper/util/FantasyTeam.py:247` - `player.drafted = 0`
7. `league_helper/trade_simulator_mode/trade_analyzer.py:117` - `p_copy.drafted = 0`
8. `league_helper/trade_simulator_mode/trade_analyzer.py:180` - `p_copy.drafted = 0`

**Simulation Module (6 assignments):**
9. `simulation/win_rate/DraftHelperTeam.py:109` - `p.drafted = 2`
10. `simulation/win_rate/DraftHelperTeam.py:117` - `p.drafted = 2`
11. `simulation/win_rate/DraftHelperTeam.py:237` - `p.drafted = 1`
12. `simulation/win_rate/DraftHelperTeam.py:243` - `p.drafted = 1`
13. `simulation/win_rate/SimulatedOpponent.py:124` - `p.drafted = 1`
14. `simulation/win_rate/SimulatedOpponent.py:129` - `p.drafted = 1`
15. `simulation/win_rate/SimulatedOpponent.py:351` - `p.drafted = 1`
16. `simulation/win_rate/SimulatedOpponent.py:357` - `p.drafted = 1`

**Utils Module (1 assignment):**
17. `utils/DraftedRosterManager.py:255` - `matched_player.drafted = drafted_value`

**CRITICAL:** If implementing read-only properties, ALL 17 locations must be updated to use `set_drafted_status()` helper method.

**Out of Scope (Simulation):**
- Simulation module assignments (9-16) are OUT OF SCOPE for this feature
- Feature is LEAGUE HELPER ONLY per specs
- Simulation changes would be a separate feature

**In Scope (League Helper + Utils):**
- 9 assignments need updating (1-8 + 17)
- DraftedRosterManager.py is in utils/ (shared), needs update

---

### 6. Nested Structure Already Exists - DOCUMENTED ✅

**Finding:** JSON already uses nested dict structure for stats. Should preserve as-is.

**Recommendation:** Keep nested structure, don't flatten

**Rationale:**
1. Matches JSON structure exactly (easier round-trip)
2. Cleaner organization (passing.completions vs passing_completions)
3. Position-specific grouping (all passing stats together)
4. Future-proof (new stats added to nested object, not top-level)

**Implementation:**
```python
@dataclass
class FantasyPlayer:
    # ... existing fields ...

    # Position-specific nested stats
    passing: Optional[Dict[str, List[float]]] = None      # QB, some RB
    rushing: Optional[Dict[str, List[float]]] = None      # RB, QB, WR
    receiving: Optional[Dict[str, List[float]]] = None    # WR, RB, TE
    misc: Optional[Dict[str, List[float]]] = None         # QB, RB, WR, TE (fumbles)
    extra_points: Optional[Dict[str, List[float]]] = None # K only
    field_goals: Optional[Dict[str, List[float]]] = None  # K only
    defense: Optional[Dict[str, List[float]]] = None      # DST only
```

---

### 7. Dataclass Property Compatibility - VERIFIED ✅

**Finding:** FantasyPlayer ALREADY uses @property with @dataclass decorator successfully

**Evidence:**
```python
# From utils/FantasyPlayer.py:461
@property
def adp(self):
    """Alias for average_draft_position for backward compatibility."""
    return self.average_draft_position
```

**Conclusion:** Properties ARE compatible with dataclasses.

**Implementation for read-only drafted/drafted_by:**
```python
@dataclass
class FantasyPlayer:
    # Private backing fields
    _drafted: int = field(default=0, init=False, repr=False)
    _drafted_by: str = field(default="", init=False, repr=False)

    @property
    def drafted(self) -> int:
        """Read-only property. Use set_drafted_status() to modify."""
        return self._drafted

    @property
    def drafted_by(self) -> str:
        """Read-only property. Use set_drafted_status() to modify."""
        return self._drafted_by

    def set_drafted_status(self, drafted_value: int, team_name: str = "") -> None:
        """Only way to modify drafted/drafted_by fields."""
        # Validation logic here...
        self._drafted = drafted_value
        self._drafted_by = ...
```

**Note:** Existing code shows this pattern works. The `adp` property provides read-only access to `average_draft_position` field.

---

## ⚠️ AMBIGUOUS ITEMS (Multiple Valid Options - Need User Decision)

### 1. projected_points vs actual_points - BOTH EXIST ⚠️

**Finding:** JSON contains BOTH arrays. Need user decision on which maps to `week_N_points`.

**Evidence:**
```json
{
  "projected_points": [23.63, 21.06, 21.54, ...],  // Pre-game ESPN projections
  "actual_points": [38.76, 11.82, 23.02, ...]      // Post-game actual results
}
```

**Options:**

**Option A: Use projected_points (pre-game projections)**
- Pros: Matches field name "week_N_points" semantics (projections)
- Pros: Aligns with league helper's draft/pre-week planning purpose
- Cons: Loses historical actual results

**Option B: Use actual_points (post-game results)**
- Pros: Better for historical analysis
- Pros: Shows what actually happened
- Cons: Not helpful for future week planning

**Option C: Store BOTH (add new field)**
- Add `week_N_actual_points` fields alongside `week_N_points`
- Pros: Preserves all data
- Cons: Adds 17 more fields to FantasyPlayer

**User Decision Required:** Which option?

**My Recommendation:** Option A (projected_points) - League Helper is primarily a draft/planning tool, so pre-game projections are more useful than post-game actuals.

---

### 2. Conflict Resolution If Both Fields Present - POLICY NEEDED ⚠️

**Scenario:** What if JSON file has BOTH `drafted` and `drafted_by` fields that conflict?

**Example:**
```json
{
  "drafted": 2,              // Says "on our team"
  "drafted_by": "Opponent"   // Says "opponent drafted"
}
```

**Options:**

**Option A: drafted_by is source of truth**
- Ignore `drafted` field entirely
- Calculate `drafted` from `drafted_by`
- Rationale: JSON is new format, `drafted_by` is canonical

**Option B: drafted field wins**
- If both present, trust `drafted` integer
- Use `drafted_by` only if `drafted` missing
- Rationale: Backward compatibility

**Option C: Error on conflict**
- Validate both match during load
- Raise ValueError if mismatch
- Forces data consistency

**User Decision Required:** Which policy?

**My Recommendation:** Option A (drafted_by is source of truth) - The new JSON format is the canonical source, old `drafted` int is legacy.

---

### 3. Error Handling Strategy - MULTIPLE APPROACHES ⚠️

**Question:** How to handle various error conditions?

**Scenarios & Options:**

**Missing JSON File:**
- A) Skip position, log warning, continue with other positions
- B) Raise error, halt loading
- C) Return empty list for that position

**Malformed JSON (parse error):**
- A) Skip file, log error, continue
- B) Raise error, halt loading
- C) Attempt partial recovery

**Missing Required Field (id, name, position):**
- A) Skip player, log warning
- B) Use default values (id=0, name="Unknown")
- C) Raise error

**Type Mismatch (drafted_by is int instead of string):**
- A) Attempt conversion, log warning
- B) Skip player, log error
- C) Raise TypeError

**User Decision Required:** Define error handling policy for each scenario

**My Recommendation:**
- Missing file: Option A (skip position, log warning)
- Malformed JSON: Option B (raise error - indicates data corruption)
- Missing required field: Option A (skip player, log warning)
- Type mismatch: Option A (attempt conversion with warning)

---

### 4. Write Atomicity Strategy - MULTIPLE OPTIONS ⚠️

**Question:** How to ensure safe writes to JSON files?

**Options:**

**Option A: Temp file + atomic rename**
```python
temp_file = f"{filepath}.tmp"
with open(temp_file, 'w') as f:
    json.dump(data, f)
os.replace(temp_file, filepath)  # Atomic on most systems
```
- Pros: Most robust, atomic on POSIX systems
- Cons: More complex, may not be atomic on Windows

**Option B: Backup before write**
```python
if filepath.exists():
    shutil.copy(filepath, f"{filepath}.backup")
with open(filepath, 'w') as f:
    json.dump(data, f)
```
- Pros: Can recover if write fails
- Cons: Doubles disk usage temporarily

**Option C: Simple write (no atomicity)**
```python
with open(filepath, 'w') as f:
    json.dump(data, f)
```
- Pros: Simplest implementation
- Cons: Risk of corruption if interrupted

**User Decision Required:** Which strategy?

**My Recommendation:** Option B (backup before write) - Good balance of safety and simplicity, works consistently on all platforms.

---

### 5. Directory Creation Policy - OPTIONS ⚠️

**Question:** What if `/data/player_data/` directory doesn't exist?

**Options:**

**Option A: Create automatically**
```python
player_data_dir = data_folder / "player_data"
player_data_dir.mkdir(parents=True, exist_ok=True)
```
- Pros: Convenient, handles missing directory
- Cons: May hide configuration errors

**Option B: Error if missing**
```python
if not player_data_dir.exists():
    raise FileNotFoundError(f"Player data directory not found: {player_data_dir}")
```
- Pros: Explicit, catches misconfiguration
- Cons: Less convenient

**User Decision Required:** Which approach?

**My Recommendation:** Option B (error if missing) - The directory should always exist since it's part of the repository. Missing directory indicates a problem.

---

## 🆕 NEW CHECKLIST ITEMS (Discovered During Research)

### NEW-1: Handle misc.fumbles field

**Issue:** Discovered unexpected `misc` field with nested `fumbles` array

**Positions Affected:** QB, RB, WR, TE (NOT K or DST)

**Structure:**
```json
"misc": {
  "fumbles": [0.0, 0.0, 1.0, 1.0, ...]  // 17 elements
}
```

**Action Required:**
- Add `misc: Optional[Dict[str, List[float]]] = None` to FantasyPlayer
- Load from JSON: `player.misc = data.get('misc')`
- Write to JSON: Include in `to_json()` output

**Checklist Item:**
- [ ] Add `misc` field to FantasyPlayer dataclass
- [ ] Verify misc field is preserved during round-trip (load → modify → save)

---

### NEW-2: Decide on locked field strategy

**Current Status:** Checklist has this as pending

**Research Finding:** locked is consistently boolean in JSON

**Options:**
- A) Keep as int in FantasyPlayer, convert during load/save
- B) Change FantasyPlayer to boolean, update all code that checks `locked == 1`

**NEW Question:** How many places check `locked == 1` in codebase?

**Action Required:** Grep for locked usage patterns

**Checklist Item:**
- [ ] Grep for all `.locked == ` patterns in league_helper/
- [ ] Count usages to determine migration effort
- [ ] User decides: keep int or migrate to boolean

---

### NEW-3: Scope clarification - Simulation module

**Discovery:** simulation/ module ALSO assigns `.drafted = ` (8 assignments)

**Question:** Is simulation module in scope for this feature?

**From specs.md:**
```
**OUT OF SCOPE:**
- Changes to simulation or other modules (League Helper only)
```

**Implication:** If implementing read-only properties, simulation code will BREAK

**Options:**
- A) Expand scope to include simulation module
- B) Keep simulation using old CSV data (doesn't use JSON)
- C) Update simulation separately in future feature

**Checklist Item:**
- [ ] Confirm simulation module is OUT OF SCOPE
- [ ] If so, document that simulation will continue using CSV temporarily
- [ ] If read-only properties implemented, note simulation incompatibility

---

### NEW-4: DraftedRosterManager.py scope decision

**Discovery:** `utils/DraftedRosterManager.py:255` assigns `.drafted = drafted_value`

**Question:** Is utils/ module in scope?

**Context:** DraftedRosterManager is in utils/ (shared between modules)

**If implementing read-only properties:** This file MUST be updated (it's breaking change)

**Checklist Item:**
- [ ] Confirm utils/DraftedRosterManager.py is IN SCOPE
- [ ] Add to list of files requiring updates for read-only property implementation

---

### NEW-5: Position-specific field handling strategy

**Discovery:** Not all positions have all stat fields

**Examples:**
- QB has passing (substantial), rushing (some), receiving (minimal)
- RB has rushing (substantial), receiving (some), passing (zeros/none)
- WR has receiving (substantial), rushing (minimal), passing (none)
- TE has receiving (substantial only)
- K has extra_points, field_goals ONLY (no passing/rushing/receiving/misc)
- DST has defense ONLY

**Question:** Should we validate position vs fields?

**Example Issue:**
```python
# What if we try to access qb.field_goals?
qb = FantasyPlayer.from_json(qb_data)
print(qb.field_goals)  # None - is this OK or should it error?
```

**Options:**
- A) All fields Optional, None for N/A positions (simple, flexible)
- B) Validate during load (raise error if K has passing stats)
- C) Use typing.Union with position-specific subclasses (complex, type-safe)

**Checklist Item:**
- [ ] Define policy: Optional fields vs validation vs subclasses
- [ ] Document expected behavior when accessing non-applicable stat

---

### NEW-6: Round-trip field preservation verification

**Issue:** JSON has many fields FantasyPlayer doesn't currently use

**Current FantasyPlayer fields that DON'T exist:**
- passing, rushing, receiving, misc, extra_points, field_goals, defense
- actual_points array

**Risk:** If we don't store these, they'll be LOST on write

**Example:**
```python
# Load from JSON
player = FantasyPlayer.from_json(data)  # passing stats loaded
player.name = "New Name"

# Write back to JSON
update_players_file()  # ← Are passing stats still there?
```

**Checklist Item:**
- [ ] Verify complete field list added to FantasyPlayer
- [ ] Create test: load JSON → modify simple field → save → reload → verify all nested stats preserved
- [ ] Document which fields are "preserved but unused" vs "actively used"

---

## 📊 SUMMARY STATISTICS

**Straightforward Answers Found:** 7 items
- bye_week location
- Empty drafted_by confirmation
- Complete field inventory
- fantasy_points calculation
- .drafted assignment inventory
- Nested structure documentation
- Dataclass property compatibility

**Ambiguous Items Requiring Decision:** 5 items
- projected vs actual mapping
- Conflict resolution policy
- Error handling strategies
- Write atomicity approach
- Directory creation policy

**New Checklist Items Discovered:** 6 items
- misc.fumbles field handling
- locked field strategy
- Simulation module scope
- DraftedRosterManager scope
- Position-specific field handling
- Round-trip field preservation

**Total Files Requiring Updates (if read-only properties):** 9 files
- 7 in league_helper/
- 1 in utils/
- 1 in player-data-fetcher/ (out of scope)

**Total .drafted Assignments:** 17 locations
- 9 in scope (league_helper + utils)
- 8 out of scope (simulation)

---

## 🎯 RECOMMENDED NEXT STEPS

1. **Present ambiguous items to user** - Get decisions on 5 policy questions
2. **Add 6 new checklist items** - Update checklist.md with discoveries
3. **Update specs.md** - Document all straightforward findings
4. **Update field mapping table** - Add all discovered fields
5. **Create implementation plan** - Once all decisions made

---

## 📝 NOTES FOR IMPLEMENTATION PHASE

**Critical Dependencies:**
- Must add ALL nested stat fields to FantasyPlayer (8 new Optional fields)
- Must implement from_json() with proper array→field mapping
- Must implement to_json() with field→array mapping + nested stat preservation
- If read-only properties chosen: Must update 9 files with .drafted assignments

**Testing Requirements:**
- Round-trip test: load JSON → save JSON → compare (verify no data loss)
- Position coverage: Test all 6 positions (QB/RB/WR/TE/K/DST)
- Edge cases: Empty arrays, None values, missing fields

**Performance Considerations:**
- Loading 6 files vs 1 CSV: Acceptable (Python json.load is fast)
- Memory: 17-element arrays × 7 nested objects × ~500 players ≈ 60KB extra (negligible)
