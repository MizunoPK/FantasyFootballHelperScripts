# Sub-Feature 5: ProjectedPointsManager Consolidation - Implementation Checklist

**Instructions**: Check off EACH requirement as you implement it. Do NOT batch-check.

**Created:** 2025-12-28
**Source:** sub_feature_05_projected_points_manager_consolidation_spec.md + todo.md

---

## Phase 1: Add Methods to PlayerManager

### Task 1: Add get_projected_points() method
- [ ] Method signature: `def get_projected_points(self, player: FantasyPlayer, week: int) -> Optional[float]`
      Spec: NEW-100, spec lines 61-71
      TODO: Task 1, lines 22-37
      File: league_helper/util/PlayerManager.py
- [ ] Week validation (1-17, raise ValueError if out of range)
      Spec: spec lines 63-64, checklist lines 43-44
- [ ] Use player.projected_points array
      Spec: spec lines 65-66
- [ ] Treat 0.0 as None (bye weeks)
      Spec: spec lines 68-69
- [ ] Acceptance criteria: Returns correct values for weeks 1-17, None for bye weeks, ValueError for invalid weeks

### Task 2: Add get_projected_points_array() method
- [ ] Method signature: `def get_projected_points_array(self, player: FantasyPlayer, start_week: int, end_week: int) -> List[Optional[float]]`
      Spec: NEW-101, spec lines 49-53
      TODO: Task 2, lines 39-49
- [ ] Delegates to get_projected_points() for each week in range
      Spec: spec line 52
- [ ] Handles empty ranges (start > end)
- [ ] Acceptance criteria: Returns correct list for any valid week range

### Task 3: Add get_historical_projected_points() method
- [ ] Method signature: `def get_historical_projected_points(self, player: FantasyPlayer) -> List[Optional[float]]`
      Spec: NEW-102, spec lines 54-60
      TODO: Task 3, lines 51-62
- [ ] Uses self.config.current_nfl_week to determine range
      Spec: spec line 58
- [ ] Delegates to get_projected_points_array(player, 1, current_week-1)
      Spec: spec line 59
- [ ] Handles current_week = 1 (returns empty list)
- [ ] Acceptance criteria: Returns correct historical range based on current_nfl_week

---

## Phase 2: Update Callers

### Task 4: Remove ProjectedPointsManager from PlayerManager.__init__()
- [ ] Remove import at line 44: `from util.ProjectedPointsManager import ProjectedPointsManager`
      Spec: NEW-103, lines 67-73
      TODO: Task 4, lines 67-72
- [ ] Remove instantiation at line 114: `self.projected_points_manager = ProjectedPointsManager(config, data_folder)`
- [ ] Update PlayerScoringCalculator instantiation at line 122: Change `self.projected_points_manager,` to `self,`
      Critical: Iteration 8 finding
- [ ] Acceptance criteria: PlayerManager no longer instantiates or imports ProjectedPointsManager, passes self to PlayerScoringCalculator

### Task 5: Update player_scoring.py to use PlayerManager methods
- [ ] Add TYPE_CHECKING import at line 24
      TODO: Task 5, line 59
- [ ] Add conditional import block (after line 29)
      ```python
      if TYPE_CHECKING:
          from util.PlayerManager import PlayerManager
      ```
- [ ] Remove ProjectedPointsManager import at line 32
      Spec: NEW-104, lines 74-81
      TODO: Task 5, line 65
- [ ] Update __init__ parameter at line 65: `projected_points_manager: ProjectedPointsManager` → `player_manager: PlayerManager`
      TODO: Task 5, line 66
- [ ] Update __init__ docstring at line 77
      TODO: Task 5, line 67
- [ ] Update attribute assignment at line 86: `self.projected_points_manager = projected_points_manager` → `self.player_manager = player_manager`
      TODO: Task 5, line 68
- [ ] Update method call at line 234: `self.projected_points_manager.get_projected_points(player, week)` → `self.player_manager.get_projected_points(player, week)`
      TODO: Task 5, line 69
- [ ] Acceptance criteria: All references to ProjectedPointsManager removed, player_manager used instead, TYPE_CHECKING pattern prevents circular imports

---

## Phase 3: Deprecate Old Code

### Task 6: Mark ProjectedPointsManager as deprecated
- [ ] Add DEPRECATED notice to module docstring
      Spec: NEW-105, lines 87-106
      TODO: Task 6, lines 75-80
- [ ] Direct users to PlayerManager methods
- [ ] Keep file for potential out-of-scope dependencies
- [ ] Acceptance criteria: Clear deprecation notice with migration instructions

---

## Phase 4: Testing

### Task 7: Add tests for new PlayerManager projection methods
- [ ] Test get_projected_points() with valid weeks (1-17)
      Spec: NEW-106, lines 113-121
      TODO: Task 7, lines 85-93
- [ ] Test get_projected_points() with invalid weeks (0, 18) - should raise ValueError
- [ ] Test 0.0 handling (bye weeks - should return None)
- [ ] Test get_projected_points_array() with various week ranges
- [ ] Test get_historical_projected_points() with different current_week values
- [ ] Test with all positions (QB, RB, WR, TE, K, DST)
- [ ] Acceptance criteria: All edge cases covered, 100% test pass rate

### Task 8: Update player_scoring tests
- [ ] Verify performance multiplier calculations still work
      Spec: NEW-107, lines 122-127
      TODO: Task 8, lines 95-101
- [ ] Verify calls to player_manager.get_projected_points()
- [ ] Test performance deviation calculations (actual vs original projection)
- [ ] Verify no regressions in scoring logic
- [ ] Acceptance criteria: All existing tests pass, new method calls verified

### Task 9: Integration test - scoring calculations
- [ ] Load players from JSON (with projected_points arrays)
      Spec: NEW-108, lines 128-133
      TODO: Task 9, lines 103-110
- [ ] Calculate player scores using player_scoring module
- [ ] Verify performance deviation calculations work
- [ ] Compare results with old ProjectedPointsManager approach (if needed)
- [ ] Verify no regressions in player rankings
- [ ] Acceptance criteria: Integration tests pass, results match expected behavior

---

## Phase 5: Cleanup

### Task 10: Mark players_projected.csv as deprecated
- [ ] Rename to players_projected.csv.OLD or add deprecation notice
      Spec: NEW-109, lines 139-145
      TODO: Task 10, lines 115-119
- [ ] Keep temporarily for validation during migration
- [ ] Acceptance criteria: File marked deprecated but available for validation

---

## Verification Log

| Requirement | Spec Location | Implementation | Verified? | Matches Spec? | Notes |
|-------------|---------------|----------------|-----------|---------------|-------|
| get_projected_points() | NEW-100, lines 61-71 | PlayerManager.py:TBD | ⏸️ | ⏸️ | Not yet implemented |
| get_projected_points_array() | NEW-101, lines 49-53 | PlayerManager.py:TBD | ⏸️ | ⏸️ | Not yet implemented |
| get_historical_projected_points() | NEW-102, lines 54-60 | PlayerManager.py:TBD | ⏸️ | ⏸️ | Not yet implemented |
| Remove ProjectedPointsManager import | NEW-103 | PlayerManager.py:44 | ⏸️ | ⏸️ | Not yet implemented |
| Remove ProjectedPointsManager instantiation | NEW-103 | PlayerManager.py:114 | ⏸️ | ⏸️ | Not yet implemented |
| Update PlayerScoringCalculator call | Iteration 8 | PlayerManager.py:122 | ⏸️ | ⏸️ | Not yet implemented |
| Update player_scoring.py | NEW-104 | player_scoring.py | ⏸️ | ⏸️ | Not yet implemented |
| Deprecation notice | NEW-105 | ProjectedPointsManager.py | ⏸️ | ⏸️ | Not yet implemented |
| Test new methods | NEW-106 | test_PlayerManager.py | ⏸️ | ⏸️ | Not yet implemented |
| Update scoring tests | NEW-107 | test_player_scoring.py | ⏸️ | ⏸️ | Not yet implemented |
| Integration test | NEW-108 | test_league_helper_integration.py | ⏸️ | ⏸️ | Not yet implemented |
| Deprecate CSV | NEW-109 | players_projected.csv | ⏸️ | ⏸️ | Not yet implemented |

---

## Mini-QC Checkpoints

### After Phase 1 (Add Methods)
- [ ] All 3 new methods added to PlayerManager
- [ ] Method signatures match spec exactly
- [ ] Error handling matches spec (ValueError for invalid weeks)
- [ ] Docstrings complete
- [ ] Unit tests passing (100% pass rate)

### After Phase 2 (Update Callers)
- [ ] ProjectedPointsManager removed from PlayerManager
- [ ] player_scoring.py updated with TYPE_CHECKING pattern
- [ ] PlayerScoringCalculator receives PlayerManager instance
- [ ] No import errors or circular dependencies
- [ ] Unit tests passing (100% pass rate)

### After Phase 3 (Deprecate)
- [ ] ProjectedPointsManager has deprecation notice
- [ ] Migration instructions clear
- [ ] Unit tests passing (100% pass rate)

### After Phase 4 (Testing)
- [ ] All new tests written and passing
- [ ] All existing tests still passing
- [ ] Edge cases covered
- [ ] Integration tests verify no regressions
- [ ] Unit tests passing (100% pass rate)

### After Phase 5 (Cleanup)
- [ ] CSV file marked deprecated
- [ ] All tasks complete
- [ ] All acceptance criteria satisfied
- [ ] Unit tests passing (100% pass rate)
- [ ] Ready for Post-Implementation QC

---

## Implementation Status

**Last Updated:** 2025-12-28
**Phase:** Setup Complete
**Next Action:** Begin Phase 1 - Add get_projected_points() method (Task 1)
**Tests Status:** Not yet run (baseline: 2406/2406 passing)
**Blockers:** None
