# Feature 02: score_penalty_application - Implementation Checklist

**Purpose:** Track implementation task completion during S6 (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**Update this file IN REAL-TIME (not batched at end)**

---

## Implementation Tasks (7 Total)

### Task 1: Add nfl_team_penalty Parameter to PlayerScoringCalculator.score_player()
- [x] Parameter added to score_player() signature at line 333
- [x] Parameter name: `nfl_team_penalty`
- [x] Default value: False
- [x] Docstring updated
- [x] Tests passing

### Task 2: Implement Step 14 NFL Team Penalty Logic in score_player()
- [x] Code added after Step 13 (after line 460)
- [x] Conditional: Only executes if `nfl_team_penalty` is True
- [x] Calls `_apply_nfl_team_penalty()` method
- [x] Adds reason to reasons list
- [x] Debug logging added
- [x] Tests passing

### Task 3: Create _apply_nfl_team_penalty() Helper Method
- [x] Method created after line 716
- [x] Signature: `def _apply_nfl_team_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:`
- [x] Check: `if p.team in self.config.nfl_team_penalty:`
- [x] Apply: `player_score * self.config.nfl_team_penalty_weight`
- [x] Reason format: `f"NFL Team Penalty: {p.team} ({weight:.2f}x)"`
- [x] Docstring added
- [x] Tests passing

### Task 4: Add nfl_team_penalty Parameter to PlayerManager.score_player()
- [x] Parameter added to score_player() signature at line 925
- [x] Parameter name: `nfl_team_penalty`
- [x] Default value: False
- [x] Pass-through to PlayerScoringCalculator
- [x] Docstring updated
- [x] Tests passing

### Task 5: Enable nfl_team_penalty in AddToRosterModeManager.get_recommendations()
- [x] Modify call at line 281
- [x] Add argument: `nfl_team_penalty=True`
- [x] Comment added
- [x] Tests passing

### Task 6: Create Test File test_player_scoring_nfl_team_penalty.py
- [x] File created: `tests/league_helper/util/test_player_scoring_nfl_team_penalty.py`
- [x] 10 test scenarios implemented (comprehensive coverage)
- [x] All tests passing (10/10)

### Task 7: Verify Simulation Compatibility
- [x] Run existing simulation tests
- [x] All simulation tests passing (2506/2506 tests - 100%)
- [x] Backward compatibility confirmed

---

## Summary

**Total Tasks:** 7
**Implemented:** 7
**Remaining:** 0

**Last Updated:** 2026-01-15 (S6 complete)
**Status:** ✅ ALL TASKS COMPLETE
