# Feature 02: score_penalty_application - Code Changes

**Purpose:** Document all code changes made during S6 implementation

**Last Updated:** 2026-01-15 (S6 start)

---

## Changes

### Change 1: Add nfl_team_penalty Parameter to PlayerScoringCalculator.score_player()

**Date:** 2026-01-15
**File:** league_helper/util/player_scoring.py
**Lines:** 333 (signature), 335 (docstring step count), 351 (docstring new step), 372-373 (docstring new param)

**What Changed:**
- Added `nfl_team_penalty=False` parameter to score_player() method signature
- Updated docstring from "13-step calculation" to "14-step calculation"
- Added Step 14 description: "Apply NFL Team Penalty (multiply score by penalty weight for specified teams)"
- Added parameter documentation for nfl_team_penalty

**Why:**
- Implements Requirement 1 from spec.md
- User specified "during Add to Roster mode" (epic line 1)
- Enables mode-specific behavior via parameter flag

**Impact:**
- Add to Roster mode can now enable penalty by passing nfl_team_penalty=True
- Other modes unaffected (default False)
- Backward compatible (all existing code continues to work)

---

### Change 2: Implement Step 14 NFL Team Penalty Logic in score_player()

**Date:** 2026-01-15
**File:** league_helper/util/player_scoring.py
**Lines:** 465-469 (new code after Step 13)

**What Changed:**
- Added Step 14 conditional logic after Step 13 (location scoring)
- Conditional: Only executes if `nfl_team_penalty` parameter is True
- Calls `self._apply_nfl_team_penalty(p, player_score)`
- Adds reason string to reasons list
- Logs at debug level: "Step 14 - After NFL team penalty for {name}: {score}"
- Updated Step 13 log from "Final score" to "After location scoring"

**Why:**
- Implements Requirements 2, 3, 4, 6 from spec.md
- User explicitly requested "their final score would be multiplied by 0.75" (epic line 8)
- Follows established pattern from existing steps (if flag: apply, add reason, log)

**Impact:**
- When nfl_team_penalty=True, penalty is applied after all 13 existing steps
- Penalty timing: After normalization, multipliers, bonuses, and penalties
- Transparent: Reason string shows penalty was applied

---

### Change 3: Create _apply_nfl_team_penalty() Helper Method

**Date:** 2026-01-15
**File:** league_helper/util/player_scoring.py
**Lines:** 727-737 (new method)

**What Changed:**
- Created new private method `_apply_nfl_team_penalty()`
- Signature: `def _apply_nfl_team_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]`
- Logic:
  1. Check if `p.team in self.config.nfl_team_penalty`
  2. If yes: multiply score by weight, return reason string
  3. If no: return unchanged score and empty reason
- Reason format: "NFL Team Penalty: {team} ({weight:.2f}x)"
- Follows exact pattern of _apply_injury_penalty() method

**Why:**
- Implements Requirements 2, 3, 4, 7 from spec.md
- User explicitly requested checking player team: "for any player on the Raiders, Jets, Giants, or Chiefs" (epic line 8)
- Established pattern: All scoring steps have private helper methods

**Impact:**
- Encapsulates penalty logic in reusable method
- Returns tuple following established pattern (score, reason)
- Handles edge cases: empty list, team not in list (returns unchanged score)

---

### Change 4: Add nfl_team_penalty Parameter to PlayerManager.score_player()

**Date:** 2026-01-15
**File:** league_helper/util/PlayerManager.py
**Lines:** 925 (signature), 927 (docstring step count), 945 (docstring new step), 965-966 (docstring new param), 976 (delegation call)

**What Changed:**
- Added `nfl_team_penalty=False` parameter to score_player() method signature
- Updated docstring from "13-step calculation" to "14-step calculation"
- Added Step 14 description in docstring
- Added parameter documentation for nfl_team_penalty
- Pass parameter through to PlayerScoringCalculator: `..., is_draft_mode, nfl_team_penalty`

**Why:**
- Implements Requirement 5 from spec.md (derived requirement)
- PlayerManager delegates to PlayerScoringCalculator (line 925)
- Must pass parameter through to enable penalty in underlying calculator
- Standard pattern for all scoring flags

**Impact:**
- PlayerManager now supports nfl_team_penalty flag
- Pure delegation - no additional logic
- Backward compatible (default False)

---

### Change 5: Enable nfl_team_penalty in AddToRosterModeManager.get_recommendations()

**Date:** 2026-01-15
**File:** league_helper/add_to_roster_mode/AddToRosterModeManager.py
**Lines:** 293 (new argument)

**What Changed:**
- Added `nfl_team_penalty=True` to score_player() call at line 281
- Added comment: "# Enable NFL team penalty (Add to Roster mode only)"
- No changes to other modes (draft, optimizer, trade analyzer)

**Why:**
- Implements Requirement 5 from spec.md
- User explicitly specified "during Add to Roster mode" (epic line 1)
- This is the ONLY mode that should enable the penalty
- Other modes use default False (no penalty)

**Impact:**
- Add to Roster mode now applies NFL team penalty to player scores
- Players on penalized teams (e.g., LV, NYJ, NYG, KC) have scores multiplied by weight (e.g., 0.75)
- Penalty visible in scoring reasons: "NFL Team Penalty: LV (0.75x)"
- Mode isolation verified: Draft, Optimizer, Trade modes NOT affected

---

### Change 6: Create Test File test_player_scoring_nfl_team_penalty.py

**Date:** 2026-01-15
**File:** tests/league_helper/util/test_player_scoring_nfl_team_penalty.py (NEW)
**Lines:** 1-180 (complete test file)

**What Changed:**
- Created comprehensive test file with 10 test scenarios
- Tests cover all edge cases: penalty applied, not applied, empty list, various weights
- Tests verify reason string format, multiple teams, weight boundaries
- All tests pass (10/10)

**Test Scenarios:**
1. Penalty applied when team in list (score * weight)
2. No penalty when team not in list (score unchanged)
3. No penalty when penalty list empty (score unchanged)
4. Weight 0.75 calculation (120.5 * 0.75 = 90.375)
5. Weight 1.0 edge case (no effect)
6. Weight 0.0 edge case (score becomes 0.0)
7. Reason string format verification
8. Empty reason when no penalty
9. Multiple teams penalty (all 4 teams tested)
10. Different weight values (0.0, 0.25, 0.5, 0.75, 0.9, 1.0)

**Why:**
- Implements Requirement 8 from spec.md
- Comprehensive coverage of all penalty logic
- Ensures robustness and prevents regressions

**Impact:**
- 100% test coverage of new _apply_nfl_team_penalty() method
- All edge cases covered (empty list, boundaries, multiple teams)
- Test suite now has 2506 tests (up from 2496)

---

## Summary

**Files Created:** 1 (test_player_scoring_nfl_team_penalty.py)
**Files Modified:** 3 (player_scoring.py, PlayerManager.py, AddToRosterModeManager.py)
**Lines Added:** ~195
**Lines Modified:** ~10
**Lines Deleted:** 0
**Tests Added:** 10
**Total Test Count:** 2506 (all passing - 100%)
