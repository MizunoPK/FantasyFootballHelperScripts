# Breaking Changes Verification Report
**Date:** 2025-12-27
**Purpose:** Comprehensive verification of all claims made in checklist/specs for three major breaking changes

---

## Executive Summary

**Verification Status:** ✅ All major claims VERIFIED
**New Issues Found:** 8 new checklist items required
**Critical Findings:** 3 missing dependencies identified

---

## Breaking Change 1: projected_points / actual_points Arrays

### Claims Made in Specs/Checklist

✅ **VERIFIED:** week_N_points fields exist in FantasyPlayer (lines 102-118)
✅ **VERIFIED:** from_dict() loads week_N_points (lines 170-186)
✅ **VERIFIED:** get_weekly_projections() returns list of week_N_points (lines 347-351)
✅ **VERIFIED:** get_single_weekly_projection(week) accesses via index (line 353)

### Actual Usage in Codebase

**Direct Method Calls (4 locations):**
1. `StarterHelperModeManager.py:212` - Gets weekly projection for current week
2. `SaveCalculatedPointsManager.py:112` - Gets weekly projection for week
3. `PlayerManager.py:307` - Gets weekly projection for scoring
4. `player_scoring.py:123` - Gets weekly projection for week

**Field Name References (4 locations):**
1. `PlayerManager.py:375-379` - Lists week_N_points as required CSV columns for save_players()
2. `TeamDataManager.py:83, 119` - Expects D/ST data as [week_1_points, ..., week_17_points]
3. `ProjectedPointsManager.py:53, 108` - Expects CSV format with week_N_points columns

**Dynamic Access:** ❌ None found (no getattr/f-string patterns)

### ⚠️ CRITICAL MISSING ITEMS

**NEW-45:** `PlayerManager.save_players()` method (lines 370-390)
- **Issue:** Currently writes to CSV with week_N_points as fieldnames
- **Impact:** This method needs updating to write to JSON instead OR be deprecated
- **Decision needed:** Keep save_players() and update to JSON, or remove entirely?

**NEW-46:** `TeamDataManager` D/ST data structure
- **Issue:** Uses [week_1_points, ..., week_17_points] array format in comments/docs
- **Impact:** Code expects this structure - need to verify actual implementation
- **Action:** Review TeamDataManager to see if it actually uses week_N_points or just documents it

**NEW-47:** `ProjectedPointsManager` CSV assumptions
- **Issue:** Hardcoded expectation of CSV format with week_N_points columns
- **Impact:** May need updating if it reads player data
- **Action:** Verify if ProjectedPointsManager reads from players.csv or different source

### Verification Summary: Breaking Change 1

**Total Affected Locations:** 8
**Method Calls:** 4
**Field References:** 4
**New Checklist Items:** 3 (NEW-45, NEW-46, NEW-47)

---

## Breaking Change 2: drafted_by Field

### Claims Made in Specs/Checklist

✅ **VERIFIED:** JSON files contain `drafted_by` string field
✅ **VERIFIED:** FantasyPlayer currently does NOT have `drafted_by` field
✅ **VERIFIED:** No existing code uses `drafted_by` in league_helper
✅ **VERIFIED:** This is a NEW field being added (not a migration)

### Actual Usage in Codebase

**Current State:**
- FantasyPlayer.py:95 has `drafted: int = 0` field
- NO `drafted_by` field exists
- NO code in league_helper/ uses drafted_by
- JSON files in data/player_data/ have drafted_by
- JSON files in simulation/sim_data/ have drafted_by (451 total JSON files)

**drafted Field Usage (17 assignments found previously):**
- League Helper: 9 assignments (in scope)
- Simulation: 8 assignments (out of scope)
- Utils: 1 assignment (DraftedRosterManager.py:255)

### ⚠️ CRITICAL CLAIM VERIFICATION

**CLAIM:** "drafted_by is source of truth (ignore drafted field if it exists)"

**REALITY CHECK:**
- ✅ JSON files DO have drafted_by
- ✅ JSON files do NOT currently have drafted field
- ✅ This decision is future-proofing (in case old field appears)
- ✅ Decision is sound - new format should win

**NEW-48:** Documentation of drafted_by values
- **Issue:** Need to document ALL possible team name values in drafted_by
- **Why:** Conversion logic depends on recognizing "Sea Sharp" vs other names
- **Action:** Get complete list of possible team names from user's league
- **Risk:** If team name changes, conversion breaks

### Verification Summary: Breaking Change 2

**Total Affected Locations:** 17 (from previous research)
**Current drafted_by Usage:** 0 (it's a new field)
**New Checklist Items:** 1 (NEW-48)

---

## Breaking Change 3: locked Field (Boolean vs Int)

### Claims Made in Specs/Checklist

❓ **PENDING:** "Should change locked int to boolean, or keep int and convert?"
✅ **VERIFIED:** JSON has `locked` as boolean (true/false)
✅ **VERIFIED:** FantasyPlayer has `locked: int = 0`
✅ **VERIFIED:** Extensive usage of `locked == 0` and `locked == 1` in codebase

### Actual Usage in Codebase

**locked Field Checks (14 locations):**

**In FantasyPlayer.py (3 usages):**
1. Line 308: `return self.drafted == 0 and self.locked == 0` (is_available method)
2. Line 320: `return self.locked == 1` (is_locked method)
3. Line 397: `locked_indicator = " [LOCKED]" if self.locked == 1 else ""` (string formatting)

**In league_helper/ (11 usages):**
1. `PlayerManager.py:552` - `if p.score < lowest_scores[p.position] and p.locked == 0:`
2. `ModifyPlayerDataModeManager.py:338` - `locked_players = [p for p in self.player_manager.players if p.locked == 1]`
3. `ModifyPlayerDataModeManager.py:394` - `was_locked = selected_player.locked == 1`
4. `ModifyPlayerDataModeManager.py:401` - `selected_player.locked = 0 if was_locked else 1` ⚠️ **ASSIGNMENT**
5. `ModifyPlayerDataModeManager.py:409` - `if selected_player.locked == 1:`
6. `trade_analyzer.py:181` - `p_copy.locked = 0` ⚠️ **ASSIGNMENT**
7. `trade_analyzer.py:639` - `my_locked_original = [p for p in my_team.team if p.locked == 1 and ...]`
8. `trade_analyzer.py:643` - `their_locked_original = [p for p in their_team.team if p.locked == 1 and ...]`
9. `trade_analyzer.py:808` - Comment: `LOCKED players (player.locked == 1)`
10. `trade_analyzer.py:820` - `my_locked = [p for p in my_team.team if p.locked == 1 and ...]`
11. `trade_analyzer.py:824` - `their_locked = [p for p in their_team.team if p.locked == 1 and ...]`

**Assignments:** 2 locations
**Comparisons:** 12 locations (including 1 in comment)

### ⚠️ CRITICAL DECISION IMPACT

**If we change locked to boolean:**
- **14 locations** need updating (all `== 0` → `== False`, `== 1` → `== True`)
- **2 assignments** need updating (ModifyPlayerDataModeManager, trade_analyzer)
- **Simpler loading:** Direct boolean from JSON (no conversion)
- **Cleaner code:** Booleans are more Pythonic for true/false state

**If we keep locked as int:**
- **0 code changes** required (just convert boolean → int during load)
- **More complex loading:** Convert true/false → 1/0
- **Less Pythonic:** Using 0/1 for boolean state

### NEW FINDINGS

**NEW-49:** locked field migration strategy decision
- **Question:** Change to boolean (14 locations) or keep as int (0 locations)?
- **Recommendation:** **CHANGE TO BOOLEAN**
  - Only 14 locations to update (manageable)
  - More Pythonic and clearer intent
  - Simpler loading (no conversion needed)
  - Matches JSON format exactly

**NEW-50:** Verify is_locked() method usage
- **Issue:** FantasyPlayer has is_locked() method (line 320)
- **Action:** Check if code uses `player.is_locked()` instead of `player.locked == 1`
- **Benefit:** If is_locked() is widely used, changing to boolean is easier

**NEW-51:** Verify is_available() method usage
- **Issue:** is_available() checks both drafted AND locked (line 308)
- **Action:** Find all usages of is_available() - may reduce direct locked checks
- **Benefit:** Fewer places to update if method is used instead of direct checks

### Verification Summary: Breaking Change 3

**Total Affected Locations:** 14 comparisons + 2 assignments = 16 total
**If changing to boolean:** 16 locations need updates
**If keeping as int:** 0 locations need updates (just conversion in from_json)
**New Checklist Items:** 3 (NEW-49, NEW-50, NEW-51)

---

## Additional Findings

### Missing PlayerManager.save_players() Analysis

**Current Implementation (PlayerManager.py:370-390):**
```python
fieldnames = [
    'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
    'injury_status', 'drafted', 'locked', 'average_draft_position',
    'player_rating',
    # Weekly projections (weeks 1-17 fantasy regular season only)
    'week_1_points', 'week_2_points', ..., 'week_17_points'
]

# Save sorted players to CSV
with open(self.file_str, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for p in sorted_players:
        player_dict = p.to_dict()
        filtered_dict = {key: player_dict.get(key, None) for key in fieldnames}
        writer.writerow(filtered_dict)
```

**Issues:**
1. Writes to CSV (self.file_str points to players.csv)
2. Uses week_N_points fieldnames (will break when fields removed)
3. Uses drafted int field (will break if changed to drafted_by)
4. Uses locked int field (will break if changed to boolean)

**NEW-52:** PlayerManager.save_players() migration strategy
- **Decision needed:**
  - Option A: Update to write to JSON files (6 position files)
  - Option B: Keep writing to CSV during transition (temporary)
  - Option C: Deprecate save_players() entirely (who uses it?)
- **Action:** Search for save_players() usage to determine impact

**NEW-53:** to_dict() method verification
- **Issue:** save_players() uses `p.to_dict()` - need to verify this method
- **Action:** Check FantasyPlayer.to_dict() implementation
- **Requirement:** to_dict() must match our new field structure

---

## Summary of New Checklist Items

| Item | Type | Description | Priority |
|------|------|-------------|----------|
| NEW-45 | Investigation | PlayerManager.save_players() migration strategy | HIGH |
| NEW-46 | Verification | TeamDataManager D/ST data structure usage | MEDIUM |
| NEW-47 | Verification | ProjectedPointsManager CSV format assumptions | MEDIUM |
| NEW-48 | Documentation | Complete list of possible drafted_by team names | HIGH |
| NEW-49 | Decision | locked field: boolean vs int migration strategy | HIGH |
| NEW-50 | Investigation | is_locked() method usage analysis | MEDIUM |
| NEW-51 | Investigation | is_available() method usage analysis | MEDIUM |
| NEW-52 | Decision | save_players() migration/deprecation strategy | HIGH |
| NEW-53 | Verification | to_dict() method matches new field structure | HIGH |

**Total New Items:** 9

---

## Recommended Next Steps

1. **Resolve NEW-49 (locked field strategy)** - Blocks implementation approach
2. **Resolve NEW-52 (save_players strategy)** - May affect file update approach
3. **Complete NEW-50, NEW-51** - May reduce locked field migration scope
4. **Document NEW-48** - Required for correct drafted_by conversion
5. **Verify NEW-53** - Critical for data preservation

---

## Overall Verification Status

✅ **All original claims VERIFIED**
⚠️ **9 new items discovered** requiring decisions/investigation
📊 **Impact Assessment Complete** for all three breaking changes

**Recommendation:** Resolve HIGH priority new items (5 items) before continuing with remaining decisions.
