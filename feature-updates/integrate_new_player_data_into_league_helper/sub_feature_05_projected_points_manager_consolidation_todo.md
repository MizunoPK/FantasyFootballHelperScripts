# Sub-Feature 5: ProjectedPointsManager Consolidation - TODO

**Objective:** Consolidate ProjectedPointsManager functionality into PlayerManager (eliminates ~200 lines of code)

**Dependencies:** Sub-feature 2 (Weekly Data Migration) ✅ COMPLETE

---

## Iteration Tracker

**Round 1:** Iterations 1-7 (+ 4a) - ⏸️ In Progress
**Round 2:** Iterations 8-16 - ⏸️ Pending
**Round 3:** Iterations 17-24 (+ 23a) - ⏸️ Pending

---

## Implementation Phases

### Phase 1: Add Methods to PlayerManager

**Tasks:**
1. Add `get_projected_points(player, week)` method
   - Get original projected points for specific player/week
   - Signature: `def get_projected_points(self, player: FantasyPlayer, week: int) -> Optional[float]`
   - Returns: Original projected points for week, or None for bye weeks (0.0 → None)
   - **Validates:** Week number (1-17, raise ValueError if out of range)
     - **Note:** Original ProjectedPointsManager returned None for invalid weeks
     - **Improvement:** Raising ValueError provides better error detection and debugging
     - **Current caller:** player_scoring.py always passes valid weeks (no impact)
   - Uses: player.projected_points array already loaded from JSON
   - **Error handling:**
     - Invalid week (< 1 or > 17): Raise ValueError with message
     - Missing projected_points array: Return None (graceful degradation)
     - Bye week (0.0 value): Return None
     - Valid projection: Return float value
   - File: league_helper/util/PlayerManager.py (~15 lines)
   - Acceptance Criteria: Returns correct values for all weeks 1-17, None for bye weeks, ValueError for invalid weeks

2. Add `get_projected_points_array(player, start_week, end_week)` method
   - Get projected points for a range of weeks
   - Signature: `def get_projected_points_array(self, player: FantasyPlayer, start_week: int, end_week: int) -> List[Optional[float]]`
   - Returns: List of projected points (None for bye weeks)
   - Delegates: Calls get_projected_points() for each week in range
   - **Error handling:**
     - Invalid weeks: Caught by get_projected_points() ValueError (delegates)
     - start_week > end_week: Return empty list [] (graceful handling)
     - Empty range: Return empty list []
   - File: league_helper/util/PlayerManager.py (~5 lines)
   - Acceptance Criteria: Returns correct list for any valid week range, empty list for invalid ranges

3. Add `get_historical_projected_points(player)` method
   - Get historical projections (weeks 1 to current-1)
   - Signature: `def get_historical_projected_points(self, player: FantasyPlayer) -> List[Optional[float]]`
   - Returns: List of projected points for weeks 1 to current_week-1
   - Uses: self.config.current_nfl_week to determine range
   - Delegates: Calls get_projected_points_array(player, 1, current_week-1)
   - **Error handling:**
     - current_nfl_week = 1: Returns empty list [] (no historical weeks, 1 to 0 range)
     - current_nfl_week < 1: Returns empty list [] (invalid range handled by array method)
     - Invalid weeks in range: Caught by get_projected_points() ValueError (delegates)
   - File: league_helper/util/PlayerManager.py (~5 lines)
   - Acceptance Criteria: Returns correct historical range based on current_nfl_week, empty list for week 1

### Phase 2: Update Callers

**Tasks:**
4. Remove ProjectedPointsManager from PlayerManager.__init__()
   - Remove import: Line 44 `from util.ProjectedPointsManager import ProjectedPointsManager`
   - Remove instantiation: Line 114 `self.projected_points_manager = ProjectedPointsManager(config, data_folder)`
   - **Update PlayerScoringCalculator instantiation:** Line 122 - Change `self.projected_points_manager,` to `self,` (pass PlayerManager instance)
   - File: league_helper/util/PlayerManager.py
   - Acceptance Criteria: PlayerManager no longer instantiates or imports ProjectedPointsManager, passes self to PlayerScoringCalculator

5. Update player_scoring.py to use PlayerManager methods
   - **Add TYPE_CHECKING import:** Line 24 - Add `TYPE_CHECKING` to imports: `from typing import Tuple, Optional, List, Dict, TYPE_CHECKING`
   - **Add conditional import:** After line 29 (after sys.path.append), add:
     ```python
     if TYPE_CHECKING:
         from util.PlayerManager import PlayerManager
     ```
   - Remove ProjectedPointsManager import: Line 32 `from ProjectedPointsManager import ProjectedPointsManager`
   - Update __init__ parameter: Line 65 - Change `projected_points_manager: ProjectedPointsManager` to `player_manager: PlayerManager`
   - Update __init__ docstring: Line 77 - Change "projected_points_manager (ProjectedPointsManager): Manager for projected points" to "player_manager (PlayerManager): Manager for player data and projected points"
   - Update attribute assignment: Line 86 - Change `self.projected_points_manager = projected_points_manager` to `self.player_manager = player_manager`
   - Update method call: Line 234 - Change `self.projected_points_manager.get_projected_points(player, week)` to `self.player_manager.get_projected_points(player, week)`
   - File: league_helper/util/player_scoring.py
   - Acceptance Criteria: All references to ProjectedPointsManager removed, player_manager used instead, TYPE_CHECKING pattern prevents circular imports

### Phase 3: Deprecate Old Code

**Tasks:**
6. Mark ProjectedPointsManager as deprecated
   - Add DEPRECATED notice to module docstring
   - Direct users to PlayerManager methods
   - Keep file for potential out-of-scope dependencies
   - File: league_helper/util/ProjectedPointsManager.py
   - Acceptance Criteria: Clear deprecation notice with migration instructions

### Phase 4: Testing

**Tasks:**
7. Add tests for new PlayerManager projection methods
   - Test get_projected_points() with valid weeks (1-17)
   - Test get_projected_points() with invalid weeks (0, 18) - should raise ValueError
   - Test 0.0 handling (bye weeks - should return None)
   - Test get_projected_points_array() with various week ranges
   - Test get_historical_projected_points() with different current_week values
   - Test with all positions (QB, RB, WR, TE, K, DST)
   - File: tests/league_helper/util/test_PlayerManager.py
   - Acceptance Criteria: All edge cases covered, 100% test pass rate

8. Update player_scoring tests
   - Verify performance multiplier calculations still work
   - Verify calls to player_manager.get_projected_points()
   - Test performance deviation calculations (actual vs original projection)
   - Verify no regressions in scoring logic
   - File: tests/league_helper/util/test_player_scoring.py
   - Acceptance Criteria: All existing tests pass, new method calls verified

9. Integration test - scoring calculations
   - Load players from JSON (with projected_points arrays)
   - Calculate player scores using player_scoring module
   - Verify performance deviation calculations work
   - Compare results with old ProjectedPointsManager approach
   - Verify no regressions in player rankings
   - File: tests/integration/test_league_helper_integration.py
   - Acceptance Criteria: Integration tests pass, results match expected behavior

### Phase 5: Cleanup

**Tasks:**
10. Mark players_projected.csv as deprecated
    - Rename to players_projected.csv.OLD or add deprecation notice
    - Keep temporarily for validation during migration
    - File: data/players_projected.csv
    - Acceptance Criteria: File marked deprecated but available for validation

---

## Success Criteria

- ✅ 3 projection accessor methods added to PlayerManager
- ✅ player_scoring.py uses PlayerManager methods (not ProjectedPointsManager)
- ✅ ProjectedPointsManager marked as deprecated
- ✅ All unit tests passing (100%)
- ✅ Integration tests verify scoring calculations unchanged
- ✅ Performance deviation calculations working correctly
- ✅ ~200 lines of code eliminated (ProjectedPointsManager obsolete)

---

## Integration Matrix

**Callers of new methods:**
- player_scoring.py (PlayerScorer class, line 235)
  - Calls: get_projected_points(player, week)
  - Purpose: Get original projections for performance deviation calculations

**Dependencies:**
- Sub-feature 1: projected_points arrays loaded into FantasyPlayer objects ✅
- Sub-feature 2: Weekly data migration complete ✅

**Files Modified:**
- league_helper/util/PlayerManager.py (add 3 methods, remove ProjectedPointsManager)
- league_helper/util/player_scoring.py (update method calls, type hints)
- league_helper/util/ProjectedPointsManager.py (add deprecation notice)
- data/players_projected.csv (rename to .OLD)

---

## Risk Assessment

**Risk Level:** VERY LOW

**Reasons:**
- Simple delegation to existing projected_points arrays
- No new data loading logic
- Only 1 caller to update (player_scoring.py)
- Reduces complexity significantly

**Mitigation:**
- Comprehensive tests for new methods
- Integration tests verify no regressions
- Keep old CSV file temporarily for validation

---

## Algorithm Traceability Matrix

**Purpose:** Map spec requirements to TODO tasks for 100% coverage verification

| Spec Requirement | Spec Location | TODO Task | Implementation |
|------------------|---------------|-----------|----------------|
| Add get_projected_points() method | NEW-100, lines 61-71 | Task 1 | PlayerManager.py ~line 570 |
| - Week validation (1-17) | Spec lines 63-64 | Task 1 | `if week < 1 or week > 17: raise ValueError` |
| - Use projected_points array | Spec lines 65-66 | Task 1 | `player.projected_points[week-1]` |
| - Treat 0.0 as None | Spec lines 68-69 | Task 1 | `return None if projected == 0.0 else projected` |
| Add get_projected_points_array() | NEW-101, spec lines 49-53 | Task 2 | PlayerManager.py ~line 585 |
| - Delegate to get_projected_points() | Spec line 52 | Task 2 | Loop calling get_projected_points() |
| Add get_historical_projected_points() | NEW-102, spec lines 54-60 | Task 3 | PlayerManager.py ~line 595 |
| - Use current_nfl_week | Spec line 58 | Task 3 | `self.config.current_nfl_week` |
| - Delegate to get_projected_points_array() | Spec line 59 | Task 3 | Call get_projected_points_array(player, 1, current-1) |
| Remove ProjectedPointsManager import | NEW-103, lines 67-73 | Task 4 | Remove line 44 import |
| Remove ProjectedPointsManager instantiation | NEW-103, lines 67-73 | Task 4 | Remove line 114 self.projected_points_manager |
| **Update PlayerScoringCalculator call** | **Iteration 8 finding** | **Task 4** | **Change line 122 to pass self** |
| Update player_scoring.py method call | NEW-104, lines 74-81 | Task 5 | Change line 234 to use player_manager |
| Update player_scoring.py type hints | NEW-104, lines 74-81 | Task 5 | Remove ProjectedPointsManager from lines 53,65,77,86 |
| Add deprecation notice | NEW-105, lines 87-106 | Task 6 | ProjectedPointsManager.py module docstring |
| Test new methods | NEW-106, lines 113-121 | Task 7 | test_PlayerManager.py |
| Update scoring tests | NEW-107, lines 122-127 | Task 8 | test_player_scoring.py |
| Integration test | NEW-108, lines 128-133 | Task 9 | test_league_helper_integration.py |
| Deprecate CSV file | NEW-109, lines 139-145 | Task 10 | Rename players_projected.csv |

**Coverage:** 11/11 total requirements (100%)
**Mapping:** All NEW-100 through NEW-109 mapped to tasks 1-10 + 1 critical finding from Iteration 8

---

## Notes

- Original plan had 23 items (update ProjectedPointsManager to read JSON)
- Discovery: PlayerManager already has all the data!
- Revised plan: 10 items (consolidate into PlayerManager)
- Savings: ~200 lines of code eliminated
- See: research/PROJECTED_POINTS_MANAGER_ANALYSIS.md
