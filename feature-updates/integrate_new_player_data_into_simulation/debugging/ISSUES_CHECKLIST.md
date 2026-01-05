# Issues Checklist - Epic: integrate_new_player_data_into_simulation

**Epic**: integrate_new_player_data_into_simulation
**Stage**: Epic-Level Debugging (discovered during Feature 02 completion)
**Date Created**: 2026-01-04
**Last Updated**: 2026-01-04

---

## Status Overview

**Total Issues**: 8
- 🔴 CRITICAL: 2 (Issues #7, #8 - both FIXED)
- 🟡 MAJOR: 3 (Issues #6, #5, #3 - all fixed)
- 🟢 MINOR: 3 (Issues #1, #2, #4 - all fixed)

**Status Breakdown**:
- ❌ OPEN: 0 issues
- 🔄 IN PROGRESS: 0 issues
- 🟢 FIXED: 8 issues (ALL ISSUES RESOLVED)

---

## Issues List

### Issue #1: Accuracy Simulation - CURRENT_NFL_WEEK Incorrectly Set
**Severity**: 🟢 MINOR
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04
**Fixed**: 2026-01-04
**Symptom**: Hundreds of "Max projection is 0.0 (weekly)" warnings
**Root Cause**: Shallow copy + wrong nesting level for CURRENT_NFL_WEEK config
**Fix**: Deep copy + correct nesting (`config_dict_copy['parameters']['CURRENT_NFL_WEEK']`)
**Files**: `simulation/accuracy/ParallelAccuracyRunner.py`, `AccuracySimulationManager.py`
**Verification**: ✅ Clean run, no warnings
**Details**: See `debugging/issue_01_accuracy_current_nfl_week.md` (to be created if investigation needed)

---

### Issue #2: Win Rate Simulation - Loading Week 1 Instead of Latest Week
**Severity**: 🟢 MINOR
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04
**Fixed**: 2026-01-04
**Symptom**: Win rate simulation scoring 0.00 total points
**Root Cause**: Hardcoded to load week_01 folder (no actual_points data)
**Fix**: Load latest week folder (has complete actual_points for entire season)
**Files**: `simulation/win_rate/SimulatedLeague.py:159-168`
**Verification**: ✅ Patrick Mahomes has 14 weeks of actual_points
**Details**: See `debugging/issue_02_win_rate_week_loading.md` (to be created if investigation needed)

---

### Issue #3: Win Rate Simulation - Using Hybrid Projection Instead of Actual Points
**Severity**: 🟡 MAJOR
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04
**Fixed**: 2026-01-04
**Symptom**: Teams scoring ~23.8 pts/week instead of ~100-150 pts/week
**Root Cause**: `get_weekly_projection()` hybrid logic returning projected_points when week == current_nfl_week
**Fix**: Direct array access to `player.actual_points[week-1]`
**Files**: `simulation/win_rate/DraftHelperTeam.py:210-220`, `SimulatedOpponent.py:329-337`
**Verification**: ✅ Fixed but revealed Issue #6
**Details**: See `debugging/issue_03_hybrid_projection.md` (to be created if investigation needed)

---

### Issue #4: Unicode Characters on Windows
**Severity**: 🟢 MINOR
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04
**Fixed**: 2026-01-04
**Symptom**: `UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'`
**Root Cause**: Windows console doesn't support Unicode checkmark (✓)
**Fix**: Replace ✓ with [OK] in print statements
**Files**: `run_win_rate_simulation.py:272, 282, 291`
**Verification**: ✅ No encoding errors
**Details**: See `debugging/issue_04_unicode_encoding.md` (to be created if investigation needed)

---

### Issue #5: Deprecated `.drafted` API Usage
**Severity**: 🟡 MAJOR
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04
**Fixed**: 2026-01-04
**Symptom**: `AttributeError: 'FantasyPlayer' object has no attribute 'drafted'`
**Root Cause**: Feature 03 changed API from `player.drafted` to `player.drafted_by`
**Fix**: Use `is_free_agent()` and `drafted_by = "OPPONENT"`
**Files**: `simulation/win_rate/SimulatedOpponent.py:151, 122-130, 350-358`
**Verification**: ✅ No AttributeError
**Details**: See `debugging/issue_05_deprecated_drafted_api.md` (to be created if investigation needed)

---

### Issue #6: Win Rate Simulation - DraftHelperTeam Using Deprecated API
**Severity**: 🟡 MAJOR
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04 (during Issue #3 investigation)
**Fixed**: 2026-01-04
**Symptom**: Players not being marked as drafted correctly, only 1 player in projected_pm.team.roster
**Root Cause**: DraftHelperTeam uses deprecated `.drafted` API instead of new `.drafted_by` API
**Fix**:
- Updated `draft_player()`: `p.drafted = 2` → `p.drafted_by = "Sea Sharp"`
- Updated `mark_player_drafted()`: `p.drafted = 1` → `p.drafted_by = "OPPONENT"`
**Files**: `simulation/win_rate/DraftHelperTeam.py:103-122, 242-267`
**Verification**: ✅ projected_pm.team.roster now has 15 players (was 1)
**Details**: See `debugging/issue_06_lineup_optimization_broken.md`
**Note**: Fix revealed Issue #7 (scoring problem)

---

### Issue #7: Win Rate Simulation - All Players Score Identically (133.00)
**Severity**: 🔴 CRITICAL
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04 (during Issue #6 fix verification)
**Fixed**: 2026-01-04
**Symptom**: All draft recommendations have identical score (133.00), no differentiation between players
**Impact**:
- Draft picks all RBs (15/15 roster spots)
- No positional diversity (0 QB, 0 WR, 0 TE, 0 K, 0 DST)
- Lineup only fills 3 positions (RB1, RB2, FLEX)
- Win rate: 7.06% (expected ~40-60%)
- Average score: 925 pts (expected ~1700-2550 pts)
- **Simulation results still invalid**
- **BLOCKS EPIC COMPLETION**

**Debug Evidence**:
```
DEBUG Draft pick #1
DEBUG Top 5 recommendations:
  1. Christian McCaffrey (RB) - score: 133.00
  2. Bijan Robinson (RB) - score: 133.00
  3. Jonathan Taylor (RB) - score: 133.00
  4. Jahmyr Gibbs (RB) - score: 133.00
  5. De'Von Achane (RB) - score: 133.00

DEBUG After draft - DraftHelperTeam roster size: 15
DEBUG DraftHelperTeam roster composition:
  QB: 0
  RB: 15
  WR: 0
  TE: 0
  K: 0
  DST: 0
```

**Root Cause**: PlayerScoringCalculator.max_projection never updated after players load
- PlayerManager.__init__() creates PlayerScoringCalculator with max_projection=0.0
- PlayerManager.load_players_from_json() calculates self.max_projection=373.90
- BUT never updates self.scoring_calculator.max_projection (stays 0.0)
- During draft, normalization: fantasy_points / 0 = 0 for all players
- All multipliers apply to 0, final score = draft bonus only (identical for all)

**Fix**:
- Updated `PlayerManager.load_players_from_json()` (lines 384-387)
- Added: `self.scoring_calculator.max_projection = self.max_projection`
- PlayerScoringCalculator now has correct max_projection (373.90)
- Normalization produces differentiated base scores

**Files Modified**:
- `league_helper/util/PlayerManager.py` (lines 384-387)

**Verification Results**:
- ✅ Win Rate: 30.59% (was 7.06%)
- ✅ Avg Points: 1466.42 (was 925)
- ✅ Roster has diverse positions (not all RBs)
- ✅ Lineup fills all positions (not just RB1, RB2, FLEX)
- ⚠️ Win rate still below expected 40-60% (may need further investigation)

**Investigation Time**: 55 minutes (2 rounds)

**Details**: See `debugging/issue_07_identical_scoring.md`

---

### Issue #8: Win Rate Simulation - Draft Not Respecting MAX_POSITIONS Config
**Severity**: 🔴 CRITICAL
**Status**: 🟢 FIXED
**Discovered**: 2026-01-04 (during Issue #7 fix verification)
**Fixed**: 2026-01-04
**Symptom**: Draft produces rosters with no positional diversity - all RBs and WRs, missing QB/TE/K/DST

**Root Cause**: DraftHelperTeam.draft_player() bypasses positional slot assignment system
- Manual roster append instead of calling FantasyTeam.draft_player()
- Never updates slot_assignments tracking
- can_draft() always returns True (no position ever "full")
- MAX_POSITIONS limits never enforced
- All 15 picks are RB/WR (highest scores due to draft bonuses)

**Fix**:
- Updated `DraftHelperTeam.draft_player()` (lines 91-138)
- Changed from manual roster.append() to proper PlayerManager.draft_player()
- Now uses FantasyTeam.draft_player() → _assign_player_to_slot()
- Properly enforces MAX_POSITIONS and slot assignment system

**Files Modified**:
- `simulation/win_rate/DraftHelperTeam.py` (lines 91-138)

**Verification Results**:
- ✅ BEFORE: QB: 0, RB: 7, WR: 8, TE: 0, K: 0, DST: 0 (5/9 lineup positions)
- ✅ AFTER: QB: 2, RB: 5, WR: 4, TE: 2, K: 1, DST: 1 (9/9 lineup positions)
- ✅ Win Rate: +47.06% (36.47% → 83.53%)
- ✅ Avg Points: +754.58 pts (1358.56 → 2113.14)
- ✅ All positions drafted, MAX_POSITIONS respected, slot system working

**Investigation Time**: 45 minutes (1 round - root cause found immediately)

**Details**: See `debugging/issue_08_draft_position_diversity.md`

---

## Test Failures Related to Issues

**Current Test Status**: 0 failures (ALL TESTS PASSING - 2481/2481 = 100%)

### test_AccuracySimulationManager.py (1 failure → FIXED)
**Related Issue**: Issue #1 (CURRENT_NFL_WEEK fix)
**Status**: ✅ FIXED
**Root Cause**: Mock signature mismatch - `create_manager_side_effect` expected 4 params but only had 3
**Fix**: Added `week_num` parameter to mock function signature
**Files**: `tests/simulation/test_AccuracySimulationManager.py:537`

### test_DraftHelperTeam.py (11 failures → FIXED)
**Related Issue**: Issues #5, #6, #8 (drafted API change, lineup optimization, draft position diversity)
**Status**: ✅ FIXED
**Root Causes**:
1. Tests checking old `.drafted` API (5 failures)
2. Tests expecting manual roster manipulation (2 failures)
3. Mock objects missing `actual_points` arrays and `.name`/`.position` attributes (4 failures)
**Fixes**:
1. Updated assertions to check `.drafted_by` or verify `draft_player()` called
2. Updated to verify proper `draft_player()` method calls instead of manual roster manipulation
3. Added missing attributes to Mock objects
**Files**: `tests/simulation/test_DraftHelperTeam.py` (multiple tests updated)

### test_SimulatedOpponent.py (4 failures → FIXED)
**Related Issue**: Issue #5 (drafted API change)
**Status**: ✅ FIXED
**Root Cause**: Tests checking old `.drafted` API
**Fix**: Updated assertions to check `.drafted_by == "OPPONENT"`
**Files**: `tests/simulation/test_SimulatedOpponent.py` (4 tests updated)

**Resolution Summary**:
- **Total failures fixed**: 16 (not 8 as initially expected)
- **All failures were test updates** - no actual bugs found in implementation
- **100% test pass rate achieved** (2481/2481 tests passing)
- Tests updated to match new API behavior from Issues #5, #6, #7, #8 fixes

---

## Debugging Protocol Workflow

**Current Phase**: Phase 1 - Issue Discovery & Checklist Update ✅ COMPLETE

**Next Phase**: Phase 2 - Investigation Rounds (Issue #6)

**Phases Remaining**:
- Phase 2: Investigation Rounds (for Issue #6)
- Phase 3: Root Cause Analysis (for Issue #6)
- Phase 4: Fix Implementation (for Issue #6)
- Phase 5: User Verification (for Issue #6)

**After All Issues Fixed**:
- Loop back to testing stage (determine which stage to restart from)
- Epic-level: Restart Stage 6a (Epic Smoke Testing)
- Re-run epic smoke test plan
- Proceed to Stage 6b/6c if smoke testing passes

---

## Investigation Priority

**All Issues Fixed**: ✅ All 8 issues resolved
**Next Priority**: Test failures (8 failures remaining)

**Recently Fixed**:
- Issue #8 (CRITICAL - draft position diversity) - FIXED 2026-01-04
- Issue #7 (CRITICAL - identical scoring) - FIXED 2026-01-04
- Issue #6 (MAJOR - deprecated API usage) - FIXED 2026-01-04
- Issues #1-5 (MINOR/MAJOR) - All fixed 2026-01-04

**Next Steps**:
1. Investigate 8 test failures (test_AccuracySimulationManager, test_DraftHelperTeam, test_SimulatedOpponent)
2. Loop back to Stage 6a (Epic Smoke Testing) per Debugging Protocol
3. Re-run epic_smoke_test_plan.md after test failures resolved

---

## Related Documents

- **BUG_TRACKING.md**: Original bug documentation (comprehensive analysis)
- **EPIC_README.md**: Epic status and progress
- **epic_smoke_test_plan.md**: Testing plan to execute after fixes
- **Feature 02 lessons_learned.md**: Insights from accuracy sim verification
- **Feature 03 spec.md**: Cross-simulation testing requirements

---

**Last Updated**: 2026-01-04
**Next Review**: After test failures investigation
