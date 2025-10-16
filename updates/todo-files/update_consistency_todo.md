# Update Consistency to Performance Scoring - Implementation TODO

**IMPORTANT**: Keep this file updated with progress after each task completion. Mark tasks as DONE when completed.

## Summary of Requirements

Based on answered questions:
- Create `data/players_projected.csv` with historical projection data from weeks 1-6
- Replace all CONSISTENCY scoring with PERFORMANCE scoring throughout the codebase
- Performance = deviation from projected points: (actual - projected) / projected
- Thresholds: VERY_POOR < -20%, POOR -20% to -10%, AVERAGE -10% to +10%, GOOD +10% to +20%, EXCELLENT > +20%
- Multipliers: Same as consistency (0.95, 0.975, 1.0, 1.025, 1.05)
- Minimum 3 weeks of data required
- Skip DST teams for performance scoring
- Player data fetcher updates only current week (week 7) projections
- Remove all consistency code (no backwards compatibility)
- Update simulation configs to use PERFORMANCE (leave historical configs as-is)

---

## PHASE 1: Create players_projected.csv with Historical Data

### Task 1.1: Create players_projected.csv structure ⬜ TODO
- Read current `data/players.csv`
- Extract columns: `id`, `name`, `week_1_points` through `week_17_points`
- Write to `data/players_projected.csv`
- **Validation**: File exists with correct columns

### Task 1.2: Populate weeks 1-6 from historical data ⬜ TODO
- For each week 1-6 in `2025_compiled_data/historical_weeks/`:
  - Read the historical week file
  - Match players by name (case-insensitive)
  - Update corresponding week_N_points column in players_projected.csv
  - For unmatched players: keep value from original players.csv
- **Validation**: Verify data populated correctly by spot-checking known players

### Task 1.3: Run pre-commit validation ⬜ TODO
```bash
python tests/run_all_tests.py
git status
git diff data/players_projected.csv
```
- **Expected**: All tests pass (100%), new file created
- **Commit**: "Create players_projected.csv with historical week 1-6 projections"

---

## PHASE 2: Create ProjectedPointsManager Utility

### Task 2.1: Create ProjectedPointsManager.py ⬜ TODO
- Location: `league_helper/util/ProjectedPointsManager.py`
- Class structure:
  - `__init__(self, config)` - Load players_projected.csv
  - `get_projected_points(self, player, weeks)` - Get projected points for specific weeks
  - `get_projected_points_array(self, player, start_week, end_week)` - Get array of projections
- Use ConfigManager for CURRENT_NFL_WEEK access
- **Validation**: Class loads data correctly

### Task 2.2: Add unit tests for ProjectedPointsManager ⬜ TODO
- Location: `tests/league_helper/util/test_ProjectedPointsManager.py`
- Test cases:
  - Test loading players_projected.csv
  - Test get_projected_points with valid player
  - Test get_projected_points with invalid player
  - Test get_projected_points_array
  - Test handling of missing weeks
- **Validation**: All tests pass

### Task 2.3: Run pre-commit validation ⬜ TODO
```bash
python tests/run_all_tests.py
```
- **Expected**: All tests pass (100%)
- **Commit**: "Add ProjectedPointsManager utility for projected points data access"

---

## PHASE 3: Update PlayerManager for Performance Scoring

### Task 3.1: Add performance calculation method to PlayerManager ⬜ TODO
- Location: `league_helper/util/PlayerManager.py`
- Add method: `_calculate_performance_deviation(self, player)`
  - Get projected points for weeks 1 to (CURRENT_NFL_WEEK - 1) using ProjectedPointsManager
  - Get actual points for same weeks from player object
  - Skip weeks where actual = 0 (player didn't play)
  - **IMPORTANT**: Skip weeks where projected = 0.0 AND actual ≠ 0.0 (prevents division by zero and skewed metrics for unprojected performances)
  - Skip DST teams (position == 'DST')
  - Require minimum 3 weeks of data
  - Calculate average % deviation: (actual - projected) / projected
  - Return deviation percentage
- **Validation**: Method calculates correctly

### Task 3.2: Add performance multiplier method ⬜ TODO
- Add method: `_get_performance_multiplier(self, player)`
  - Call `_calculate_performance_deviation(player)`
  - If < 3 weeks data or DST: return 1.0
  - Apply thresholds from PERFORMANCE_SCORING config:
    - deviation < -0.20: VERY_POOR multiplier (0.95)
    - -0.20 <= deviation < -0.10: POOR multiplier (0.975)
    - -0.10 <= deviation < 0.10: AVERAGE multiplier (1.0)
    - 0.10 <= deviation < 0.20: GOOD multiplier (1.025)
    - deviation >= 0.20: EXCELLENT multiplier (1.05)
  - Apply WEIGHT from config
- **Validation**: Method returns correct multipliers

### Task 3.3: Update score_player method ⬜ TODO
- Add parameter: `performance=False` (default False)
- Remove all consistency-related code
- Add performance scoring logic:
  ```python
  if performance:
      performance_multiplier = self._get_performance_multiplier(player)
      score *= performance_multiplier
  ```
- **Validation**: Method signature updated, logic implemented

### Task 3.4: Remove consistency methods ⬜ TODO
- Remove method: `_calculate_consistency()`
- Remove method: `_get_consistency_multiplier()`
- Remove any other consistency-related helper methods
- **Validation**: No consistency code remains in PlayerManager

### Task 3.5: Add unit tests for performance scoring ⬜ TODO
- Location: `tests/league_helper/util/test_PlayerManager_performance.py`
- Test cases:
  - Test performance calculation with outperforming player
  - Test performance calculation with underperforming player
  - Test performance calculation with < 3 weeks data
  - Test performance skips DST teams
  - Test performance multiplier thresholds (all 5 levels)
  - Test performance integration in score_player
- **Validation**: All new tests pass

### Task 3.6: Update existing PlayerManager tests ⬜ TODO
- Location: `tests/league_helper/util/test_PlayerManager_scoring.py`
- Replace all CONSISTENCY_SCORING with PERFORMANCE_SCORING
- Update test fixtures to use performance thresholds
- Remove consistency-specific tests
- Update assertions to match new performance logic
- **Validation**: All tests pass

### Task 3.7: Run pre-commit validation ⬜ TODO
```bash
python tests/run_all_tests.py
```
- **Expected**: All tests pass (100%)
- **Commit**: "Replace consistency scoring with performance scoring in PlayerManager"

---

## PHASE 4: Update Configuration Files

### Task 4.1: Update league_config.json ⬜ TODO
- Location: `data/league_config.json`
- Remove: `CONSISTENCY_SCORING` section
- Add: `PERFORMANCE_SCORING` section:
```json
"PERFORMANCE_SCORING": {
    "MIN_WEEKS": 3,
    "THRESHOLDS": {
        "VERY_POOR": -0.2,
        "POOR": -0.1,
        "GOOD": 0.1,
        "EXCELLENT": 0.2
    },
    "MULTIPLIERS": {
        "VERY_POOR": 0.95,
        "POOR": 0.975,
        "GOOD": 1.025,
        "EXCELLENT": 1.05
    },
    "WEIGHT": 1.0
}
```
- **Validation**: JSON is valid, structure correct

### Task 4.2: Update ConfigManager.py ⬜ TODO
- Location: `league_helper/util/ConfigManager.py`
- Remove all consistency-related property accessors
- Add performance-related property accessors:
  - `performance_scoring` property
  - `performance_min_weeks` property
  - `performance_thresholds` property
  - `performance_multipliers` property
  - `performance_weight` property
- **Validation**: Properties accessible

### Task 4.3: Update ConfigManager tests ⬜ TODO
- Location: `tests/league_helper/util/test_ConfigManager.py`
- Remove consistency test cases
- Add performance test cases
- **Validation**: All tests pass

### Task 4.4: Run pre-commit validation ⬜ TODO
```bash
python tests/run_all_tests.py
```
- **Expected**: All tests pass (100%)
- **Commit**: "Update configuration files to use performance scoring"

---

## PHASE 5: Update League Helper Modes

### Task 5.1: Update StarterHelperModeManager ⬜ TODO
- Location: `league_helper/starter_helper_mode/StarterHelperModeManager.py`
- Find all calls to `player_manager.score_player()`
- Update to include `performance=True` parameter
- Remove any consistency-related code
- **Validation**: All score_player calls updated

### Task 5.2: Update TradeSimulatorModeManager ⬜ TODO
- Location: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
- Find all calls to `player_manager.score_player()`
- Update to include `performance=True` parameter
- Remove any consistency-related code
- **Validation**: All score_player calls updated

### Task 5.3: Update AddToRosterModeManager ⬜ TODO
- Location: `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
- Verify score_player calls (should remain `performance=False` by default)
- Remove any consistency-related code
- **Validation**: Code updated

### Task 5.4: Update mode tests ⬜ TODO
- Update tests in:
  - `tests/league_helper/starter_helper_mode/`
  - `tests/league_helper/trade_simulator_mode/`
  - `tests/league_helper/add_to_roster_mode/`
- Replace CONSISTENCY with PERFORMANCE in fixtures
- Update assertions
- **Validation**: All tests pass

### Task 5.5: Run pre-commit validation ⬜ TODO
```bash
python tests/run_all_tests.py
```
- **Expected**: All tests pass (100%)
- **Commit**: "Update league helper modes to use performance scoring"

---

## PHASE 6: Update Player Data Fetcher

### Task 6.1: Update player data fetcher to maintain players_projected.csv ⬜ TODO
- Location: `player-data-fetcher/main.py` or equivalent
- After fetching new projections:
  - Load `data/players_projected.csv`
  - Update only `week_7_points` column (current week) with new projections
  - Keep all historical weeks (1-6) unchanged
  - Save back to `data/players_projected.csv`
- **Validation**: Only current week updated, historical preserved

### Task 6.2: Add tests for player data fetcher updates ⬜ TODO
- Location: `tests/player_data_fetcher/`
- Test that players_projected.csv is updated correctly
- Test that historical weeks remain unchanged
- **Validation**: Tests pass

### Task 6.3: Run pre-commit validation ⬜ TODO
```bash
python tests/run_all_tests.py
```
- **Expected**: All tests pass (100%)
- **Commit**: "Update player data fetcher to maintain players_projected.csv"

---

## PHASE 7: Update Simulation System

### Task 7.1: Update ConfigGenerator.py ⬜ TODO
- Location: `simulation/ConfigGenerator.py`
- Remove CONSISTENCY_SCORING parameter definitions
- Add PERFORMANCE_SCORING parameter definitions
- Update PARAMETER_ORDER
- **Validation**: Config generation uses performance

### Task 7.2: Update simulation config files ⬜ TODO
- **Leave historical configs unchanged** (per Q14 answer)
- For any new/current configs being used:
  - Replace CONSISTENCY_SCORING with PERFORMANCE_SCORING
  - Update thresholds and structure
- **Validation**: Active configs use performance

### Task 7.3: Update simulation tests ⬜ TODO
- Location: `tests/simulation/test_config_generator.py`
- Replace CONSISTENCY with PERFORMANCE
- Update test expectations
- **Validation**: All tests pass

### Task 7.4: Run pre-commit validation ⬜ TODO
```bash
python tests/run_all_tests.py
```
- **Expected**: All tests pass (100%)
- **Commit**: "Update simulation system to use performance scoring"

---

## PHASE 8: Final Cleanup and Documentation

### Task 8.1: Search for remaining consistency references ⬜ TODO
```bash
grep -r "consistency" --include="*.py" league_helper/
grep -r "CONSISTENCY" --include="*.py" league_helper/
grep -r "consistency" --include="*.py" simulation/
grep -r "CONSISTENCY" --include="*.json" data/
```
- Remove any remaining consistency code
- **Validation**: No consistency references in active code

### Task 8.2: Update constants.py ⬜ TODO
- Location: `league_helper/constants.py`
- Remove consistency-related constants
- Add performance-related constants if needed
- **Validation**: Constants updated

### Task 8.3: Update README.md ⬜ TODO
- Document performance scoring system
- Explain how it works (actual vs projected deviation)
- Update any references to consistency
- **Validation**: Documentation accurate

### Task 8.4: Update PROJECT_DOCUMENTATION.md ⬜ TODO
- Replace consistency references with performance
- Document performance calculation methodology
- Update scoring system overview
- **Validation**: Documentation complete

### Task 8.5: Run final comprehensive validation ⬜ TODO
```bash
# Run all unit tests
python tests/run_all_tests.py

# Manual testing
python run_league_helper.py  # Test all modes
python run_player_fetcher.py # Verify players_projected.csv updates
python run_simulation.py     # Test simulation with performance scoring
```
- **Expected**: All tests pass, system functional
- **Commit**: "Complete performance scoring implementation and update documentation"

### Task 8.6: Move files and cleanup ⬜ TODO
- Move `updates/update_consistency.txt` to `updates/done/`
- Delete `updates/update_consistency_questions.md`
- Delete `updates/todo-files/update_consistency_todo.md` (this file)
- **Validation**: Files organized

---

## Pre-Commit Validation Checklist

**EXECUTE AT END OF EVERY PHASE** (see rules.txt lines 9-102):

1. ✅ Analyze changes: `git status` and `git diff`
2. ✅ Run all unit tests: `python tests/run_all_tests.py`
3. ✅ Verify 100% test pass rate
4. ✅ Manual testing of affected functionality
5. ✅ Update documentation if needed
6. ✅ Commit with proper message format

**STOP if any tests fail. Fix issues before proceeding to next phase.**

---

## Notes

- Total phases: 8
- Each phase must achieve 100% test pass rate before proceeding
- Performance scoring completely replaces consistency scoring
- No backwards compatibility maintained
- DST teams are skipped for performance calculations
- Player data fetcher only updates current week (week 7) projections
- Historical simulation configs remain unchanged

**Keep this file updated as you complete each task!**
