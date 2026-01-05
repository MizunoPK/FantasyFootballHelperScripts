# Bug Tracking - Integrate New Player Data Into Simulation

**Epic**: integrate_new_player_data_into_simulation
**Date Created**: 2026-01-04
**Last Updated**: 2026-01-04

This document tracks all bugs discovered during Stage 7 (Epic Cleanup) user testing, along with their fixes and open questions.

---

## Table of Contents

1. [Bugs Fixed](#bugs-fixed)
2. [Critical Open Issues](#critical-open-issues)
3. [Warnings/Errors Summary](#warningserrors-summary)
4. [Open Questions](#open-questions)
5. [Test Results](#test-results)

---

## Bugs Fixed

### Bug #1: Accuracy Simulation - CURRENT_NFL_WEEK Incorrectly Set ✅ FIXED

**Severity**: High
**Symptom**: Hundreds of "Max projection is 0.0 (weekly)" warnings during accuracy simulation
**Impact**: Accuracy simulation was comparing projected_points vs projected_points instead of calculated_projection vs actual_points

**Root Cause**:
1. When simulating week 1, config had `CURRENT_NFL_WEEK=16` (from baseline config)
2. `FantasyPlayer.get_weekly_projections()` uses hybrid logic:
   - If `week < current_nfl_week`: returns `actual_points` (all zeros in week 1 folder)
   - If `week >= current_nfl_week`: returns `projected_points`
3. This caused `calculate_max_weekly_projection()` to return 0.0

**Files Affected**:
- `simulation/accuracy/ParallelAccuracyRunner.py:292-297`
- `simulation/accuracy/AccuracySimulationManager.py:393-397`

**Fix Applied**:
```python
# BEFORE (shallow copy + wrong nesting level):
config_dict_copy = config_dict.copy()
config_dict_copy['CURRENT_NFL_WEEK'] = week_num

# AFTER (deep copy + correct nesting):
import copy
config_dict_copy = copy.deepcopy(config_dict)
config_dict_copy['parameters']['CURRENT_NFL_WEEK'] = week_num
```

**Why This Works**:
- Config structure is `{"config_name": "...", "parameters": {"CURRENT_NFL_WEEK": 16, ...}}`
- Deep copy prevents shared references between configs
- Setting at correct nesting level ensures ConfigManager reads the updated value

**Verification**:
```
Before: week_num=1, config.current_nfl_week=16 → Max projection = 0.0
After:  week_num=1, config.current_nfl_week=1  → Max projection = 24.3
```

**Status**: ✅ Fixed, verified working

---

### Bug #2: Win Rate Simulation - Loading Week 1 Instead of Latest Week ✅ FIXED

**Severity**: Critical
**Symptom**: Win rate simulation scoring 0.00 total points
**Impact**: All actual_points were 0.0 because week 1 folder doesn't have actual results

**Root Cause**:
- `SimulatedLeague._initialize_teams()` was hardcoded to load from `week_01` folder
- Week 1 folder has `actual_points = [0.0, 0.0, ...]` (no games played yet)
- Need latest week folder which has complete `actual_points` for entire season

**File Affected**:
- `simulation/win_rate/SimulatedLeague.py:159-168`

**Fix Applied**:
```python
# BEFORE:
week_folder = self.data_folder / "weeks" / "week_01"

# AFTER:
weeks_folder = self.data_folder / "weeks"
available_weeks = sorted([f for f in weeks_folder.iterdir()
                          if f.is_dir() and f.name.startswith("week_")])
week_folder = available_weeks[-1]  # Use last week (has all actual results)
```

**Verification**:
```
Patrick Mahomes week_17 folder:
  actual_points: [26.0, 22.1, 13.2, 27.3, 26.7, ...]
  Total non-zero: 14 weeks
```

**Status**: ✅ Fixed, verified working

---

### Bug #3: Win Rate Simulation - Using Hybrid Projection Instead of Actual Points ✅ FIXED

**Severity**: High
**Symptom**: After Bug #2 fix, total points increased from 0.00 to 404.90, but still extremely low
**Impact**: Teams were scoring ~23.8 pts/week instead of ~100-150 pts/week

**Root Cause**:
- `DraftHelperTeam.set_weekly_lineup()` sets `self.config.current_nfl_week = week`
- Then calls `actual_pm.get_weekly_projection(player, week)`
- Since `week == current_nfl_week`, the hybrid logic returns **projected_points** not actual_points
- This is the same hybrid logic issue as Bug #1

**Files Affected**:
- `simulation/win_rate/DraftHelperTeam.py:210-220`
- `simulation/win_rate/SimulatedOpponent.py:329-337`

**Fix Applied**:
```python
# BEFORE:
actual_weekly_points, _ = self.actual_pm.get_weekly_projection(starter.player, week)
total_actual_points += actual_weekly_points

# AFTER (direct array access):
if 1 <= week <= 17 and len(starter.player.actual_points) >= week:
    actual_points = starter.player.actual_points[week - 1]
    if actual_points is not None:
        total_actual_points += actual_points
```

**Why This Works**:
- Bypasses the hybrid `get_weekly_projections()` logic entirely
- Directly accesses `actual_points` array from JSON data
- Array indexing: week 1 = index 0, week N = index N-1

**Status**: ✅ Fixed, but revealed Bug #4

---

### Bug #4: Unicode Characters on Windows (Minor) ✅ FIXED

**Severity**: Low
**Symptom**: `UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'`
**Impact**: Simulation crashed on Windows when printing Unicode checkmark (✓)

**Files Affected**:
- `run_win_rate_simulation.py:272, 282, 291`

**Fix Applied**:
```python
# BEFORE: print(f"✓ Found intermediate folders...")
# AFTER:  print(f"[OK] Found intermediate folders...")
```

**Status**: ✅ Fixed

---

### Bug #5: Deprecated `.drafted` API Usage ✅ FIXED

**Severity**: Medium
**Symptom**: `AttributeError: 'FantasyPlayer' object has no attribute 'drafted'`
**Impact**: Win rate simulation crashed when checking player availability

**Root Cause**:
- Feature 03 changed from `player.drafted` (int) to `player.drafted_by` (str) + helper methods
- `SimulatedOpponent.py` still used old API

**File Affected**:
- `simulation/win_rate/SimulatedOpponent.py:151, 122-130, 350-358`

**Fix Applied**:
```python
# BEFORE:
if p.drafted == 0 and p.fantasy_points > 0:
    p.drafted = 1

# AFTER:
if p.is_free_agent() and p.fantasy_points > 0:
    p.drafted_by = "OPPONENT"
```

**Status**: ✅ Fixed

---

## Critical Open Issues

### Issue #1: Win Rate Simulation - Lineup Optimization Broken 🔴 CRITICAL

**Severity**: Critical
**Status**: ⚠️ OPEN - BLOCKS EPIC COMPLETION
**Discovered**: 2026-01-04 during Bug #3 investigation

**Symptom**:
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
- Lineup optimization only returns **1 player** (RB1) instead of 9 positions
- Total season score: 404.90 pts (should be ~1700-2550 pts)
- Win rate: 0% (should be ~40-60%)
- **Simulation results are completely invalid**

**Root Cause**: Unknown
- `StarterHelperModeManager.optimize_lineup()` is broken
- Likely related to Feature 03 changes (new player data structure)
- Could be:
  1. Roster data not loading correctly
  2. Player filtering broken (all positions filtered out except RB)
  3. Lineup optimization algorithm broken
  4. Player manager state issues

**Investigation Needed**:
1. Check if `DraftHelperTeam.roster` has all 15 drafted players
2. Verify `StarterHelperModeManager` receives correct roster
3. Debug `optimize_lineup()` to see where 8 positions are lost
4. Check if Feature 03's JSON data structure is compatible with StarterHelper

**Files Potentially Affected**:
- `simulation/win_rate/DraftHelperTeam.py` (roster management)
- `league_helper/modes/StarterHelperModeManager.py` (lineup optimization)
- `league_helper/util/PlayerManager.py` (player filtering)

**Next Steps**:
1. Add debug logging to track roster size after draft
2. Add debug logging in `optimize_lineup()` to see available players per position
3. Check if `is_free_agent()` vs `drafted_by` changes broke position filtering
4. Verify JSON data has all positions (QB, RB, WR, TE, K, DST)

**Priority**: 🔴 **HIGHEST** - Must fix before epic can be completed

---

## Warnings/Errors Summary

### Accuracy Simulation
| Warning/Error | Status | Notes |
|--------------|--------|-------|
| Max projection is 0.0 (weekly) | ✅ FIXED | Bug #1 - CURRENT_NFL_WEEK issue |
| Zero variance warnings | ⚠️ NOT INVESTIGATED | Deprioritized after Bug #1 fix |
| UnicodeEncodeError | ✅ FIXED | Bug #4 - checkmark character |

**Final Status**: Clean run, no warnings/errors

### Win Rate Simulation
| Warning/Error | Status | Notes |
|--------------|--------|-------|
| UnicodeEncodeError | ✅ FIXED | Bug #4 - checkmark character |
| AttributeError: 'drafted' | ✅ FIXED | Bug #5 - API change |
| 0% win rate | 🔴 OPEN | Issue #1 - Lineup optimization broken |
| ~23.8 pts/week | 🔴 OPEN | Issue #1 - Only 1 starter per week |

**Final Status**: Runs without crashes, but **produces invalid results**

---

## Open Questions

### Q1: Should accuracy simulation use calculated projection or raw projection?
**Status**: ✅ ANSWERED

**Question**: Is accuracy simulation correctly comparing calculated_projection (after scoring algorithm) vs actual_points, or should it compare raw projected_points vs actual_points?

**Answer**: **Calculated projection is CORRECT**

**Evidence**:
```
Josh Allen Week 1:
  Raw JSON projection: 21.60 pts
  Calculated projection (after scoring algorithm): 22.24 pts
  Difference: +0.64 pts (3% increase from scoring adjustments)
```

**Explanation**:
- The scoring algorithm applies 6 adjustment factors:
  - Team quality multiplier
  - Performance multiplier (actual vs projected deviation)
  - Matchup multiplier (opponent strength)
  - Temperature bonus/penalty
  - Wind bonus/penalty
  - Location bonus/penalty
- The `scored.projected_points` value is de-normalized back to fantasy points scale: `(final_score / normalization_scale) * max_projection`
- This is **exactly what we want** - testing how well the scoring algorithm predicts actual performance

**File Reference**: `league_helper/util/player_scoring.py:469-481`

---

### Q2: Does accuracy simulation use correct data sources?
**Status**: ✅ ANSWERED

**Question**: Does accuracy simulation correctly use week_N folder for projections and week_N+1 folder for actuals?

**Answer**: **YES, confirmed correct**

**Data Flow**:
1. **Week N folder** (e.g., `week_01`):
   - Contains `projected_points` for week N
   - Used to calculate scoring algorithm adjustments
   - Returns calculated projection

2. **Week N+1 folder** (e.g., `week_02`):
   - Contains `actual_points[N-1]` for week N (results now available)
   - Used for comparison vs calculated projection

**Verification**:
```
Week 1 folder (week_01):
  projected_points[0] = 19.5
  actual_points[0] = 0.0 (week 1 hasn't happened)

Week 2 folder (week_02):
  projected_points[0] = 19.5 (same)
  actual_points[0] = 15.1 (week 1 results!)
```

**File Reference**: `simulation/accuracy/ParallelAccuracyRunner.py:113-176`

---

### Q3: Why was single mode using CURRENT_NFL_WEEK=16?
**Status**: ⚠️ PARTIALLY ANSWERED

**Context**: During Bug #1 investigation, we found the baseline config had `CURRENT_NFL_WEEK=16` but was simulating week 1 data.

**Observations**:
- Baseline config: `simulation_configs/accuracy_optimal_2025-12-23_12-02-15/league_config.json`
- Has `"CURRENT_NFL_WEEK": 17` (current real-world week)
- This is correct for real-world usage but wrong for historical simulation

**Partial Answer**:
- The config represents "current state" of the NFL season
- Historical simulation should override this for each week being simulated
- Bug #1 fix ensures this happens correctly

**Remaining Question**: Should we create separate "simulation baseline configs" with CURRENT_NFL_WEEK=1 to avoid confusion?

---

### Q4: Should win rate simulation use same week folder for all teams?
**Status**: ✅ ANSWERED

**Question**: Win rate sim loads ONE week folder for initial team setup. Is this correct?

**Answer**: **YES, using latest week is correct**

**Reasoning**:
- All teams draft from the same player pool
- Need complete `actual_points` data for scoring weekly lineups
- Latest week folder (week_17 or week_18) has all historical results
- Using week 1 would mean `actual_points = [0, 0, 0, ...]` (no data)

**Note**: This is different from accuracy simulation which loads different weeks for different purposes (projected vs actual data).

**File Reference**: `simulation/win_rate/SimulatedLeague.py:159-168`

---

## Test Results

### Accuracy Simulation
```bash
Command: python run_accuracy_simulation.py --test-values 1 --max-workers 2 --log-level warning
Duration: ~30 seconds
Result: ✅ PASS

Output:
- No WARNING messages
- No ERROR messages
- Clean execution
```

**Verification Sample**:
```
Week 1 [Josh Allen]: Raw JSON=21.60, Calculated=22.24, Diff=0.64
Week 2 [Kyler Murray]: Raw JSON=21.50, Calculated=22.17, Diff=0.67
Week 3 [Kyler Murray]: Raw JSON=24.90, Calculated=25.55, Diff=0.65
```

**Status**: ✅ **READY FOR PRODUCTION**

---

### Win Rate Simulation
```bash
Command: python run_win_rate_simulation.py single --sims 1
Duration: ~13 seconds
Result: ❌ FAIL (Invalid Results)

Output:
Config: test
Simulations: 1
Record: 0W-17L (17 games)
Win Rate: 0.00%
Avg Points/League: 404.90

Expected:
Record: ~7W-10L
Win Rate: ~40-60%
Avg Points/League: ~1700-2550
```

**Root Cause**: Issue #1 - Lineup optimization broken (only 1 starter per week)

**Status**: 🔴 **BLOCKED** - Cannot proceed until Issue #1 is fixed

---

## Next Steps

### Immediate (Required for Epic Completion)

1. **🔴 CRITICAL**: Fix Issue #1 (Lineup Optimization Broken)
   - Add debug logging to `DraftHelperTeam` to check roster size after draft
   - Debug `StarterHelperModeManager.optimize_lineup()` to trace where players are lost
   - Verify compatibility with Feature 03's new player data structure
   - **Priority**: HIGHEST - Blocks epic completion

2. **After Issue #1 Fix**: Re-run win rate simulation
   - Verify realistic win rates (40-60%)
   - Verify realistic scoring (~100-150 pts/week)
   - Check for any new warnings/errors

3. **Final Verification**: Run full epic smoke test plan
   - All 3 features complete
   - Both simulations producing valid results
   - No warnings or errors

### Future Improvements (Post-Epic)

1. Investigate "Zero variance" warnings (deprioritized)
2. Consider creating separate "simulation baseline configs" with CURRENT_NFL_WEEK=1
3. Add integration tests to catch lineup optimization regressions
4. Document expected win rate ranges for different configurations

---

## File Change Summary

### Files Modified (All Changes Committed)

**Accuracy Simulation**:
- ✅ `simulation/accuracy/ParallelAccuracyRunner.py` (Bug #1 fix)
- ✅ `simulation/accuracy/AccuracySimulationManager.py` (Bug #1 fix)

**Win Rate Simulation**:
- ✅ `simulation/win_rate/SimulatedLeague.py` (Bug #2 fix)
- ✅ `simulation/win_rate/DraftHelperTeam.py` (Bug #3 fix + debug logging)
- ✅ `simulation/win_rate/SimulatedOpponent.py` (Bug #3 fix + Bug #5 fix)
- ✅ `run_win_rate_simulation.py` (Bug #4 fix)
- ✅ `simulation/win_rate/SimulationManager.py` (single mode restoration)

**Shared**:
- ✅ `league_helper/util/PlayerManager.py` (removed debug logging)
- ✅ `utils/FantasyPlayer.py` (removed debug logging)

### Files With Debug Logging (To Be Cleaned Up)

- ⚠️ `simulation/win_rate/DraftHelperTeam.py:210-227` (Week 1 lineup debug logging)

**Note**: Debug logging should be removed after Issue #1 is fixed

---

## Related Documents

- **Epic README**: `EPIC_README.md`
- **Epic Ticket**: `EPIC_TICKET.md`
- **Smoke Test Plan**: `epic_smoke_test_plan.md`
- **Lessons Learned**: `epic_lessons_learned.md`
- **Feature 03 Spec**: `feature_03_cross_simulation_testing/spec.md`

---

**Last Updated**: 2026-01-04 07:30 UTC
**Next Review**: After Issue #1 is fixed
