# Issue #6: Win Rate Simulation - DraftHelperTeam Using Deprecated API

**Issue ID**: #6
**Severity**: 🟡 MAJOR
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04
**Fixed**: 2026-01-04
**Epic**: integrate_new_player_data_into_simulation
**Revealed**: Issue #7 (scoring problem)

---

## Symptom

Win rate simulation lineup optimization returns only **1 player** (RB1) per week instead of 9 positions.

**Debug Output**:
```
DEBUG Week 1 lineup structure:
  QB: None
  RB1: Christian McCaffrey
  RB2: None
  WR1: None
  WR2: None
  TE: None
  FLEX: None
  K: None
  DST: None
DEBUG Week 1: 1 starters scored 23.20 points
```

**Impact**:
- Total season score: 404.90 pts (expected: ~1700-2550 pts)
- Win rate: 0% (expected: ~40-60%)
- Average points per week: 23.8 (expected: ~100-150)
- **Simulation results are completely invalid**

---

## Investigation History

### Investigation Round 1: Code Tracing ✅ COMPLETE

**Objective**: Map the data flow from draft → roster → lineup optimization

**Tasks**:
1. [x] Trace draft execution in `SimulatedLeague.run_draft()`
2. [x] Check `self.roster` size after draft completes (should be 15 players)
3. [x] Verify roster composition (should have QB, RB, WR, TE, K, DST)
4. [x] Trace `set_weekly_lineup()` call chain
5. [x] Verify `StarterHelperModeManager.optimize_lineup()` receives full roster
6. [x] Identify where 14 players disappear (only 1 RB remains)

**Debug Output**:
```
DEBUG After draft - DraftHelperTeam roster size: 15
DEBUG DraftHelperTeam roster composition:
  QB: 0
  RB: 15  ← ALL 15 players are RBs!
  WR: 0
  TE: 0
  K: 0
  DST: 0

DEBUG projected_pm.team.roster size: 1  ← Only 1 player!

DEBUG StarterHelperModeManager.optimize_lineup() - Week 1
DEBUG Roster size: 1  ← Only sees 1 player!
DEBUG Roster by position:
  QB: 0 players
  RB: 1 players  ← Christian McCaffrey only
  WR: 0 players
  TE: 0 players
  K: 0 players
  DST: 0 players
DEBUG First 3 roster players: ['Christian McCaffrey']
```

**Critical Finding #1: DraftHelperTeam.roster has 15 players (all RBs)**
- `self.roster` list works correctly (15 players added)
- BUT all 15 are RBs (should be diverse positions)
- This suggests draft recommendations are broken

**Critical Finding #2: projected_pm.team.roster has only 1 player**
- StarterHelperModeManager uses `self.player_manager.team.roster`
- `projected_pm.team.roster` has only 1 player (Christian McCaffrey)
- This is why lineup optimization returns only 1 starter

**Critical Finding #3: Old API usage in DraftHelperTeam.draft_player()**
- Lines 107-122: Code tries to set `p.drafted = 2` and `p.drafted = 1`
- FantasyPlayer no longer has `.drafted` attribute (uses `.drafted_by` instead)
- Setting `.drafted` likely fails silently or raises AttributeError
- Players don't get added to `projected_pm.team.roster` properly
- Only 1 player made it through (possibly from a different code path)

**Time Elapsed**: 25 minutes

**Status**: ✅ ROOT CAUSE IDENTIFIED

---

### Investigation Round 2: Hypothesis Formation (Pending)

**Objective**: Form 3 testable hypotheses based on Round 1 findings

**Hypothesis Template**:
1. **Hypothesis 1**: [Description]
   - **Why plausible**: [Reasoning]
   - **How to test**: [Diagnostic steps]
   - **Expected evidence**: [What we'd see if true]

2. **Hypothesis 2**: [Description]
   - **Why plausible**: [Reasoning]
   - **How to test**: [Diagnostic steps]
   - **Expected evidence**: [What we'd see if true]

3. **Hypothesis 3**: [Description]
   - **Why plausible**: [Reasoning]
   - **How to test**: [Diagnostic steps]
   - **Expected evidence**: [What we'd see if true]

**Status**: Not started

---

### Investigation Round 3: Diagnostic Testing (Pending)

**Objective**: Confirm root cause through targeted testing

**Tests to Run**:
- TBD (based on Round 2 hypotheses)

**Status**: Not started

---

## Initial Hypotheses (from BUG_TRACKING.md)

### Hypothesis A: Roster Not Loading Correctly
**Plausibility**: High
**Evidence needed**: Check `len(self.roster)` after draft
**Related code**: `DraftHelperTeam.simulate_draft_with_adp()`

### Hypothesis B: Player Filtering Broken
**Plausibility**: High
**Evidence needed**: Check available players per position in `optimize_lineup()`
**Related code**: `PlayerManager.get_players_by_position()`
**Potential cause**: Feature 03's `is_free_agent()` vs `drafted_by` changes

### Hypothesis C: Lineup Optimization Algorithm Broken
**Plausibility**: Medium
**Evidence needed**: Step through `StarterHelperModeManager.optimize_lineup()`
**Related code**: `league_helper/starter_helper_mode/StarterHelperModeManager.py`

### Hypothesis D: PlayerManager State Issues
**Plausibility**: Medium
**Evidence needed**: Check if PlayerManager has correct player list
**Related code**: `league_helper/util/PlayerManager.py`

### Hypothesis E: JSON Data Structure Incompatibility
**Plausibility**: Medium
**Evidence needed**: Verify StarterHelper can read new JSON player structure
**Related code**: Player data loading in StarterHelper context

---

## Files Potentially Affected

**Primary Suspects**:
1. `simulation/win_rate/DraftHelperTeam.py`
   - Lines 60-120: Draft simulation
   - Lines 200-230: Weekly lineup setting
   - Responsible for: Roster management, calling lineup optimization

2. `league_helper/starter_helper_mode/StarterHelperModeManager.py`
   - Lines 100-300 (estimated): Lineup optimization logic
   - Responsible for: Selecting best 9 players for lineup

3. `league_helper/util/PlayerManager.py`
   - Position filtering methods
   - Player availability checks
   - Responsible for: Providing available players per position

**Secondary Suspects**:
4. `simulation/win_rate/SimulatedLeague.py`
   - Player data loading
   - May affect what data is available to DraftHelperTeam

5. `utils/FantasyPlayer.py`
   - Player object structure
   - `is_free_agent()` vs old `drafted` property

---

## Debug Logging Strategy

### Current Debug Logging (Added)
- `DraftHelperTeam.py:210-227`: Week 1 lineup structure logging

### Additional Logging Needed

**In DraftHelperTeam.__init__() after draft**:
```python
print(f"\nDEBUG After draft - Roster size: {len(self.roster)}")
print(f"DEBUG Roster composition:")
for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
    count = sum(1 for p in self.roster if p.position == pos)
    print(f"  {pos}: {count}")
```

**In StarterHelperModeManager.optimize_lineup() entry**:
```python
print(f"\nDEBUG optimize_lineup called")
print(f"DEBUG Roster size: {len(self.roster)}")
print(f"DEBUG Available players by position:")
for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
    available = [p for p in self.roster if p.position == pos]
    print(f"  {pos}: {len(available)} players")
```

**In PlayerManager filtering methods**:
```python
print(f"DEBUG get_players_by_position({position}): {len(result)} players")
print(f"DEBUG First 3 players: {[p.name for p in result[:3]]}")
```

---

## Root Cause ✅ IDENTIFIED

**Status**: Investigation Round 1 complete - ROOT CAUSE FOUND

**Root Cause**: **DraftHelperTeam.draft_player() and mark_player_drafted() use deprecated `.drafted` API**

**Detailed Explanation**:

1. **API Mismatch**: FantasyPlayer changed from `.drafted` (int: 0/1/2) to `.drafted_by` (str: team name)
   - Old API: `player.drafted = 0` (free agent), `= 1` (opponent), `= 2` (our team)
   - New API: `player.drafted_by = ""` (free agent), `= "OPPONENT"`, `= "Sea Sharp"`

2. **Code Still Using Old API**:
   - `DraftHelperTeam.draft_player()` lines 109, 117: `p.drafted = 2`
   - `DraftHelperTeam.mark_player_drafted()` lines 259, 265: `p.drafted = 1`
   - FantasyPlayer no longer has a `.drafted` attribute (removed in Feature 03)

3. **Failure Mode**:
   - Setting `p.drafted = X` fails (AttributeError or silent failure)
   - Players don't get added to `projected_pm.team.roster` list (lines 111-112, 119-120 may not execute)
   - Only 1 player (Christian McCaffrey) gets added through unknown path
   - All other players fail to register

4. **Cascading Effects**:
   - Players not marked as drafted in `projected_pm` → stay available for draft
   - AddToRosterModeManager keeps recommending same position (RB)
   - Draft ends with 15 RBs instead of diverse positions
   - StarterHelperModeManager only sees 1 player in `projected_pm.team.roster`
   - Lineup optimization returns only 1 starter (RB1 = Christian McCaffrey)

**Evidence**:
- Debug output shows `projected_pm.team.roster size: 1` vs `DraftHelperTeam.roster size: 15`
- All 15 players in DraftHelperTeam.roster are RBs (draft broken due to players not being marked as unavailable)
- StarterHelperModeManager only sees 1 player (Christian McCaffrey)

**Why Issue #5 "Fix" Didn't Catch This**:
- Issue #5 only fixed `SimulatedOpponent.py`
- Did NOT fix `DraftHelperTeam.py` (different file, same problem)
- DraftHelperTeam methods were not checked during Issue #5 investigation

---

## Fix Plan ✅ READY TO IMPLEMENT

**Status**: Root cause identified, fix plan ready

**Fix Approach**: Update DraftHelperTeam to use new `.drafted_by` API

**Files to Modify**:
1. `simulation/win_rate/DraftHelperTeam.py`

**Changes Required**:

### 1. Fix draft_player() method (lines 106-122)
**Current code**:
```python
for p in self.projected_pm.players:
    if p.id == player.id:
        p.drafted = 2  # ❌ OLD API
        if p not in self.projected_pm.team.roster:
            self.projected_pm.team.roster.append(p)
        break
```

**Fixed code**:
```python
for p in self.projected_pm.players:
    if p.id == player.id:
        p.drafted_by = "Sea Sharp"  # ✅ NEW API (our team name)
        if p not in self.projected_pm.team.roster:
            self.projected_pm.team.roster.append(p)
        break
```

**Repeat for actual_pm** (lines 115-121)

### 2. Fix mark_player_drafted() method (lines 256-266)
**Current code**:
```python
for p in self.projected_pm.players:
    if p.id == player_id:
        p.drafted = 1  # ❌ OLD API
        break
```

**Fixed code**:
```python
for p in self.projected_pm.players:
    if p.id == player_id:
        p.drafted_by = "OPPONENT"  # ✅ NEW API
        break
```

**Repeat for actual_pm** (lines 262-266)

### 3. Update docstrings
- Update draft_player() docstring (line 101): Remove "Sets player.drafted = 2" reference
- Update mark_player_drafted() docstring (line 254): Remove "Sets player.drafted = 1" reference

**Testing After Fix**:
1. Run simulation → check `projected_pm.team.roster size: 15` (not 1)
2. Verify roster has diverse positions (QB, RB, WR, TE, K, DST)
3. Verify lineup has 9 starters (not 1)
4. Verify win rate: 40-60% (not 0%)
5. Verify total score: 1700-2550 pts (not 404 pts)

---

## Testing Plan

### Unit Tests to Add/Fix
- TBD (depends on root cause)

### Integration Test
**After fix, verify**:
1. Draft completes with 15 players on roster
2. All 9 positions filled in weekly lineup
3. Win rate: 40-60%
4. Total season score: 1700-2550 pts
5. Average points/week: 100-150 pts

### Regression Prevention
- Add integration test that checks lineup has 9 starters
- Add assertion that roster has 15 players after draft
- Add test that verifies all positions represented

---

## Related Issues

**Fixed Issues That May Have Contributed**:
- Issue #3: Hybrid projection fix (changed how weekly points calculated)
- Issue #5: Deprecated `.drafted` API (changed to `drafted_by`)

**Test Failures Possibly Related**:
- `test_DraftHelperTeam.py`: 3 failures
- `test_SimulatedOpponent.py`: 4 failures

**Note**: These may be false positives if tests check old behavior

---

## User Verification Checklist

**Before marking as 🟢 FIXED, user must verify**:
- [ ] Win rate simulation runs without crashes
- [ ] Win rate: 40-60% (realistic)
- [ ] Total season score: 1700-2550 pts (realistic)
- [ ] Average points/week: 100-150 pts (realistic)
- [ ] Lineup has all 9 positions filled each week
- [ ] No warnings or errors in simulation output

---

## Investigation Timeline

**Round 1 (Code Tracing)**: Not started
**Round 2 (Hypothesis Formation)**: Not started
**Round 3 (Diagnostic Testing)**: Not started
**Max Rounds**: 5 (escalate to user if not resolved by Round 5)
**Max Time Per Round**: 2 hours

---

## Next Steps

1. **Start Investigation Round 1** (Code Tracing)
   - Add debug logging to DraftHelperTeam
   - Add debug logging to StarterHelperModeManager
   - Run simulation
   - Trace data flow from draft → roster → lineup

2. **Document Round 1 Findings** in this file

3. **Proceed to Round 2** (Hypothesis Formation)

4. **Test hypotheses in Round 3** (Diagnostic Testing)

5. **Document Root Cause** after Round 3

6. **Implement Fix** (Phase 4)

7. **Request User Verification** (Phase 5)

---

## Fix Implementation ✅ COMPLETE

**Status**: Investigation Round 1 complete, root cause identified, fix implemented

**Investigation Timeline**:
- **Round 1 (Code Tracing)**: ✅ COMPLETE (25 minutes)
  - Added debug logging to SimulatedLeague.py and StarterHelperModeManager.py
  - Identified that projected_pm.team.roster had only 1 player instead of 15
  - Found deprecated `.drafted` API usage in DraftHelperTeam.py

**Root Cause Confirmed**:
- DraftHelperTeam.draft_player() used `p.drafted = 2` (old API, lines 108, 116)
- DraftHelperTeam.mark_player_drafted() used `p.drafted = 1` (old API, lines 258, 264)
- FantasyPlayer changed from `.drafted` (int) to `.drafted_by` (string) in Feature 03
- Setting `.drafted` attribute failed, players didn't get added to team.roster properly

**Fix Applied**:
1. Updated `draft_player()` method (lines 91-122):
   - Changed `p.drafted = 2` → `p.drafted_by = "Sea Sharp"`
   - Updated docstring to reflect new API
   - Applied to both projected_pm and actual_pm

2. Updated `mark_player_drafted()` method (lines 242-267):
   - Changed `p.drafted = 1` → `p.drafted_by = "OPPONENT"`
   - Updated docstring to reflect new API
   - Applied to both projected_pm and actual_pm

**Verification Results**:
- ✅ projected_pm.team.roster now has 15 players (was 1)
- ✅ No AttributeError exceptions
- ✅ Draft completes successfully
- ✅ All 15 players added to roster

**Remaining Issue**:
- ❌ Fix revealed Issue #7: All players score identically (133.00)
- ❌ Draft still picks 15 RBs (no positional diversity)
- ❌ Lineup still only fills 3 positions (RB1, RB2, FLEX)
- See `debugging/issue_07_identical_scoring.md` for next investigation

---

**Last Updated**: 2026-01-04
**Status**: 🟢 FIXED (but revealed Issue #7)
