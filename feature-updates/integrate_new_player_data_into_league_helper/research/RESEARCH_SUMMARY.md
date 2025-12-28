# Research Phase Summary - December 27, 2025

## Quick Overview

**Research Completed:** ✅ Comprehensive codebase investigation
**Straightforward Answers Found:** 7 items can be documented with certainty
**Decisions Still Needed:** 5 items require user input
**New Issues Discovered:** 6 new checklist items identified

**Detailed Findings:** See `RESEARCH_FINDINGS_2025-12-27.md` for complete documentation

---

## ✅ What We Now Know For Certain

### 1. **bye_week field** - FOUND!
- Location: Top-level integer field in all JSON files
- Example: `"bye_week": 7`
- No ambiguity - direct mapping

### 2. **Empty drafted_by** - CONFIRMED!
- Empty string `""` definitely means "not drafted"
- Real team names found: "The Injury Report", "Fishoutawater", "Chase-ing points", "The Eskimo Brothers"
- Conversion logic is straightforward

### 3. **Complete field inventory** - DOCUMENTED!
- Universal fields: 12 fields present in all positions
- Position-specific nested stats fully mapped:
  - QB/RB/WR/TE: passing, rushing, receiving, misc (fumbles)
  - K: extra_points, field_goals
  - DST: defense
- **NEW DISCOVERY:** `misc` field with nested `fumbles` array (was not in previous docs)

### 4. **fantasy_points** - MUST BE CALCULATED!
- Does NOT exist in JSON
- Must calculate: `sum(projected_points)`
- Example: Josh Allen = 347.64 total projected points

### 5. **All .drafted assignments** - INVENTORIED!
- Found 17 total assignments across codebase
- **9 are IN SCOPE** (league_helper + utils)
- **8 are OUT OF SCOPE** (simulation module)
- Critical if implementing read-only properties

### 6. **Nested structure** - ALREADY EXISTS!
- JSON uses nested dicts (e.g., `passing.completions`)
- Should preserve this structure (don't flatten)
- Cleaner organization and easier round-trip

### 7. **Dataclass + properties** - COMPATIBLE!
- FantasyPlayer already uses `@property` successfully (`adp` property)
- Can implement read-only properties with private backing fields
- Pattern is proven in existing code

---

## ⚠️ What Still Needs User Decision

### 1. **projected_points vs actual_points** - BOTH EXIST!

JSON has BOTH arrays. Which maps to `week_N_points`?

**Option A:** Use `projected_points` (pre-game ESPN projections)
- Better for draft/planning tool
- **Recommended**

**Option B:** Use `actual_points` (post-game results)
- Better for historical analysis

**Option C:** Store BOTH (add 17 new fields `week_N_actual_points`)
- Preserves all data
- Significant field expansion

**Your decision:** _____

---

### 2. **Conflict resolution** - IF both drafted and drafted_by exist

**Option A:** `drafted_by` is source of truth (ignore `drafted` field)
- **Recommended** - new format is canonical

**Option B:** `drafted` field wins (backward compat)

**Option C:** Error on conflict (strict validation)

**Your decision:** _____

---

### 3. **Error handling** - Multiple scenarios

**Missing JSON file:**
- A) Skip position, log warning, continue
- B) Raise error, halt loading
- **Recommended:** A

**Malformed JSON:**
- A) Skip file, log error, continue
- B) Raise error, halt loading
- **Recommended:** B (indicates corruption)

**Missing required field (id, name):**
- A) Skip player, log warning
- B) Use defaults (id=0, name="Unknown")
- **Recommended:** A

**Your decisions:** _____

---

### 4. **Write atomicity** - How to safely write JSON files

**Option A:** Temp file + atomic rename (most robust)

**Option B:** Backup before write (good balance)
- **Recommended**

**Option C:** Simple write (no protection)

**Your decision:** _____

---

### 5. **Directory creation** - If `/data/player_data/` missing

**Option A:** Create automatically

**Option B:** Error if missing
- **Recommended** - should exist in repo

**Your decision:** _____

---

## 🆕 New Issues Discovered

### NEW-1: `misc` field with fumbles array
- Exists in QB/RB/WR/TE (NOT K or DST)
- Must add to FantasyPlayer as `Optional[Dict[str, List[float]]]`

### NEW-2: locked field strategy decision
- JSON uses boolean consistently
- Should we:
  - A) Keep int in FantasyPlayer, convert on load/save?
  - B) Migrate FantasyPlayer to boolean?
- Need to grep for `.locked == ` usage patterns first

### NEW-3: Simulation module scope
- Simulation code assigns `.drafted = ` in 8 locations
- Specs say simulation is OUT OF SCOPE
- If read-only properties implemented, simulation code will BREAK
- Need confirmation: is simulation truly out of scope?

### NEW-4: DraftedRosterManager.py scope
- `utils/DraftedRosterManager.py` assigns `.drafted = `
- Is utils/ in scope? (Shared between modules)
- If implementing read-only properties, this MUST be updated

### NEW-5: Position-specific field handling
- Not all positions have all fields (K has no passing stats, QB has no kicking stats)
- Should we validate? Or just make all Optional?
- **Recommended:** All Optional, no validation (flexible)

### NEW-6: Round-trip field preservation
- Must verify ALL nested stats preserved during save/load cycle
- Need test: load → modify name → save → reload → verify stats unchanged

---

## 📊 Impact Analysis

**Files Requiring Updates (if read-only properties):**
```
IN SCOPE (9 files):
  league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py (3 assignments)
  league_helper/util/FantasyTeam.py (3 assignments)
  league_helper/trade_simulator_mode/trade_analyzer.py (2 assignments)
  league_helper/util/PlayerManager.py (1 read)
  league_helper/util/player_search.py (4 reads)
  league_helper/reserve_assessment_mode/ReserveAssessmentModeManager.py (1 read)
  utils/DraftedRosterManager.py (1 assignment)

OUT OF SCOPE (simulation module - 8 assignments):
  simulation/win_rate/DraftHelperTeam.py (4 assignments)
  simulation/win_rate/SimulatedOpponent.py (4 assignments)
```

**New Fields to Add to FantasyPlayer:**
```python
# Nested stat structures (all Optional)
passing: Optional[Dict[str, List[float]]] = None        # QB, some RB
rushing: Optional[Dict[str, List[float]]] = None        # RB, QB, WR
receiving: Optional[Dict[str, List[float]]] = None      # WR, RB, TE
misc: Optional[Dict[str, List[float]]] = None           # QB, RB, WR, TE (fumbles)
extra_points: Optional[Dict[str, List[float]]] = None   # K only
field_goals: Optional[Dict[str, List[float]]] = None    # K only
defense: Optional[Dict[str, List[float]]] = None        # DST only
drafted_by: str = ""                                     # New field (already decided)
```

---

## 🎯 Next Steps

1. **User reviews this summary** and makes 5 policy decisions
2. **User confirms** 6 new checklist items should be added
3. **Agent updates** checklist.md and specs.md with findings
4. **Continue Phase 3** - resolve remaining items one by one
5. **Move to Phase 4** when all checklist items resolved

---

## 📄 Reference Documents

- **Full Findings:** `RESEARCH_FINDINGS_2025-12-27.md` (comprehensive details)
- **This Summary:** `RESEARCH_SUMMARY.md` (you are here)
- **Checklist:** `integrate_new_player_data_into_league_helper_checklist.md` (to be updated)
- **Specs:** `integrate_new_player_data_into_league_helper_specs.md` (to be updated)
