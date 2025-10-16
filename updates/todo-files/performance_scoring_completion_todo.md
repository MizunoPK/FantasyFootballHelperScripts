# Performance Scoring Implementation Completion - TODO

**CRITICAL**: This TODO addresses missing requirements from the original update_consistency.txt specification that were not fully implemented.

**IMPORTANT**: Keep this file updated with progress after each task completion. Mark tasks as DONE when completed.

---

## Summary of Missing Requirements

Based on re-review of original specification (updates/update_consistency.txt and updates/update_consistency_questions.md):

### Missing Requirements Identified:
1. **Requirement #6**: Player-data-fetcher does NOT update players_projected.csv when run
2. **Requirement #15**: Simulation system does NOT have PERFORMANCE_SCORING implemented
3. **Requirement #13**: Score_player calls were missing performance=True (FIXED during review)

### Already Fixed (During Review):
- ✅ StarterHelperModeManager.py now has `performance=True` in score_player call
- ✅ TradeSimTeam.py now has `performance=True` instead of `consistency=False` (which would have caused TypeError)

---

## PHASE 1: Update Player Data Fetcher to Maintain players_projected.csv

### Task 1.1: Add players_projected.csv update logic to player_data_exporter.py ⬜ TODO

**Requirement Reference**: Line 6 of update_consistency.txt:
> "Update the player_data_fetcher such that every time the player_data_fetcher is run, the info for the current week and everything upcoming is updated in that players_projected.csv file."

**Question Answer Reference**: Q10 - "Update only the current week. Leave historical weeks alone"

**Implementation Details**:
- Location: `player-data-fetcher/player_data_exporter.py`
- Add new method: `export_projected_points_data(self, data: ProjectionData) -> str`
- Logic:
  1. Load existing `data/players_projected.csv`
  2. For each player in the new data:
     - Match player by ID
     - Update ONLY `week_N_points` where N >= CURRENT_NFL_WEEK
     - Preserve all historical weeks (weeks 1 to CURRENT_NFL_WEEK-1)
  3. Save back to `data/players_projected.csv`
- **Validation**: Only current and future weeks updated, historical data preserved

**Files to Modify**:
- `player-data-fetcher/player_data_exporter.py` - Add new method
- `player-data-fetcher/player_data_fetcher_main.py` - Call new method in export_data()

### Task 1.2: Integrate players_projected.csv update into main export flow ⬜ TODO

**Implementation Details**:
- Location: `player-data-fetcher/player_data_fetcher_main.py`
- In `NFLProjectionsCollector.export_data()` method:
  - After `export_to_data()` call
  - Add call to `export_projected_points_data()`
- **Validation**: Run player_data_fetcher and verify players_projected.csv updates

**Files to Modify**:
- `player-data-fetcher/player_data_fetcher_main.py` - Update export_data() method

### Task 1.3: Add unit tests for players_projected.csv updates ⬜ TODO

**Implementation Details**:
- Location: `tests/player_data_fetcher/test_player_data_exporter.py` (create if doesn't exist)
- Test cases:
  - Test that current week projections are updated
  - Test that future week projections are updated
  - Test that historical weeks are NOT modified
  - Test that new players are added to players_projected.csv
  - Test that missing players in new data don't lose historical data
- **Validation**: All tests pass

**Files to Create/Modify**:
- `tests/player_data_fetcher/test_player_data_exporter.py` - Add new tests

### Task 1.4: Run pre-commit validation for Phase 1 ⬜ TODO

```bash
python tests/run_all_tests.py
git status
git diff
```

- **Expected**: All tests pass (100%)
- **Manual Test**: Run `python run_player_fetcher.py` and verify players_projected.csv updated
- **Commit**: "Add players_projected.csv update logic to player data fetcher"

---

## PHASE 2: Add PERFORMANCE_SCORING to Simulation System

### Task 2.1: Add PERFORMANCE_SCORING parameter definitions to ConfigGenerator ⬜ TODO

**Requirement Reference**: Line 15 of update_consistency.txt:
> "Add performance to the Simulation in the same way that multipliers like adp and player rating are implemented."

**Implementation Details**:
- Location: `simulation/ConfigGenerator.py`
- Update `PARAM_DEFINITIONS` dict:
  ```python
  'PERFORMANCE_SCORING_WEIGHT': (0.3, 0.0, 5.0),
  ```
- Update `SCORING_SECTIONS` list:
  ```python
  SCORING_SECTIONS = [
      'ADP_SCORING',
      'PLAYER_RATING_SCORING',
      'TEAM_QUALITY_SCORING',
      'PERFORMANCE_SCORING',  # ADD THIS
      'MATCHUP_SCORING'
  ]
  ```
- Update `PARAMETER_ORDER` list:
  ```python
  PARAMETER_ORDER = [
      'NORMALIZATION_MAX_SCALE',
      'BASE_BYE_PENALTY',
      'PRIMARY_BONUS',
      'SECONDARY_BONUS',
      # Multiplier Weights
      'ADP_SCORING_WEIGHT',
      'PLAYER_RATING_SCORING_WEIGHT',
      'TEAM_QUALITY_SCORING_WEIGHT',
      'PERFORMANCE_SCORING_WEIGHT',  # ADD THIS
      'MATCHUP_SCORING_WEIGHT',
  ]
  ```
- **Validation**: ConfigGenerator can parse PERFORMANCE_SCORING

**Files to Modify**:
- `simulation/ConfigGenerator.py` - Lines 48, 56, 70

### Task 2.2: Add PERFORMANCE_SCORING value generation to ConfigGenerator ⬜ TODO

**Implementation Details**:
- Location: `simulation/ConfigGenerator.py`
- In `generate_all_parameter_value_sets()` method (around line 234):
  - Remove line 231 comment: `# value_sets = self.generate_multiplier_parameter_values(value_sets, "CONSISTENCY_SCORING")`
  - Add AFTER line 228 (Team Quality):
    ```python
    # PERFORMANCE
    value_sets = self.generate_multiplier_parameter_values(value_sets, "PERFORMANCE_SCORING")
    ```
- **Validation**: Parameter value sets include PERFORMANCE_SCORING_WEIGHT

**Files to Modify**:
- `simulation/ConfigGenerator.py` - Line 231-234

### Task 2.3: Update config extraction and creation methods ⬜ TODO

**Implementation Details**:
- Location: `simulation/ConfigGenerator.py`
- In `_extract_combination_from_config()` method (around line 366):
  - Update loop to include PERFORMANCE:
    ```python
    for section in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
        param_name = f'{section}_SCORING_WEIGHT'
        combination[param_name] = params[f'{section}_SCORING']['WEIGHT']
    ```
- In `create_config_dict()` method (around line 396):
  - Update loop to include PERFORMANCE:
    ```python
    for parameter in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
        params[f'{parameter}_SCORING']['WEIGHT'] = combination[f'{parameter}_SCORING_WEIGHT']
    ```
- **Validation**: Configs created with PERFORMANCE_SCORING weights

**Files to Modify**:
- `simulation/ConfigGenerator.py` - Lines 366, 396

### Task 2.4: Update baseline config file with PERFORMANCE_SCORING ⬜ TODO

**Implementation Details**:
- Location: Find current baseline config being used for simulations
- Add PERFORMANCE_SCORING section after TEAM_QUALITY_SCORING:
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
- Remove CONSISTENCY_SCORING section if present
- **Validation**: Baseline config loads successfully

**Files to Modify**:
- Baseline simulation config file (determine which one is active)

### Task 2.5: Update simulation tests for PERFORMANCE_SCORING ⬜ TODO

**Implementation Details**:
- Search for all test files that reference CONSISTENCY_SCORING
- Update to use PERFORMANCE_SCORING instead
- Update test expectations for new parameter counts (6→6 if consistency was counted, or 5→6)
- **Validation**: All simulation tests pass

**Files to Modify**:
- `tests/simulation/test_config_generator.py` (if exists)
- Any other simulation test files

### Task 2.6: Run pre-commit validation for Phase 2 ⬜ TODO

```bash
python tests/run_all_tests.py
git status
git diff
```

- **Expected**: All tests pass (100%)
- **Manual Test**: Run config generator and verify PERFORMANCE_SCORING in output
- **Commit**: "Add PERFORMANCE_SCORING to simulation system"

---

## PHASE 3: Final Verification and Documentation

### Task 3.1: Re-review original requirements file ⬜ TODO

**Critical Step**: Re-read ENTIRE update_consistency.txt and update_consistency_questions.md

**Verification Checklist**:
- [ ] Requirement #1-3: Performance calculation logic - ✅ DONE (previous implementation)
- [ ] Requirement #4: players_projected.csv created - ✅ DONE (previous implementation)
- [ ] Requirement #5: Historical week data populated - ✅ DONE (previous implementation)
- [ ] Requirement #6: Player-data-fetcher updates players_projected.csv - ⬜ THIS TODO
- [ ] Requirement #7: ProjectedPointsManager created - ✅ DONE (previous implementation)
- [ ] Requirement #8-10: Performance calculation in PlayerManager - ✅ DONE (previous implementation)
- [ ] Requirement #11: PERFORMANCE_SCORING in league_config.json - ✅ DONE (previous implementation)
- [ ] Requirement #12: No backwards compatibility - ✅ DONE (consistency fully removed)
- [ ] Requirement #13: performance=True in modes - ✅ DONE (fixed during this review)
- [ ] Requirement #14: MIN_WEEKS constant - ✅ DONE (previous implementation)
- [ ] Requirement #15: Performance in simulation - ⬜ THIS TODO

**Action**: Go through each line of update_consistency.txt and verify implementation

### Task 3.2: Verify all question answers implemented ⬜ TODO

**Critical Step**: Re-read ENTIRE update_consistency_questions.md

**Verification Checklist**:
- [ ] Q1: players_projected.csv location (data/) - ✅ DONE
- [ ] Q2: Populate weeks 1-6 - ✅ DONE
- [ ] Q3: Unmatched players handling - ✅ DONE
- [ ] Q4: Performance calculation method (% deviation) - ✅ DONE
- [ ] Q5: Threshold values - ✅ DONE
- [ ] Q6: Multiplier values - ✅ DONE
- [ ] Q7: Minimum 3 weeks - ✅ DONE
- [ ] Q8: PERFORMANCE_SCORING structure - ✅ DONE
- [ ] Q9: performance=True in modes - ✅ DONE (fixed during review)
- [ ] Q10: Update only current week in fetcher - ⬜ THIS TODO (Phase 1)
- [ ] Q11: ProjectedPointsManager location - ✅ DONE
- [ ] Q12: Remove all consistency code - ✅ DONE
- [ ] Q13: Update all tests - ✅ DONE
- [ ] Q14: Leave historical sim configs as-is - ✅ DONE
- [ ] Q15: Week 6 handling - ✅ DONE
- [ ] Q16: Skip DST for performance - ✅ DONE

**Action**: Go through each question answer and verify implementation

### Task 3.3: Run comprehensive test suite ⬜ TODO

```bash
# Run all unit tests
python tests/run_all_tests.py --verbose

# Manual integration tests
python run_league_helper.py  # Test starter helper and trade simulator modes
python run_player_fetcher.py # Verify players_projected.csv updates
python run_simulation.py     # Test simulation with PERFORMANCE_SCORING
```

- **Expected**: 100% test pass rate
- **Expected**: All modes functional with performance scoring
- **Validation**: Complete system works end-to-end

### Task 3.4: Update code changes documentation ⬜ TODO

**Implementation Details**:
- Location: `updates/done/performance_scoring_code_changes.md`
- Add new sections documenting:
  1. Player-data-fetcher updates (Phase 1)
     - File: player_data_exporter.py
     - New method: export_projected_points_data()
     - Logic: Update current week only, preserve historical
  2. Simulation system updates (Phase 2)
     - File: ConfigGenerator.py
     - Added: PERFORMANCE_SCORING_WEIGHT parameter
     - Updated: All config generation methods
  3. Bug fixes discovered during review
     - TradeSimTeam.py: consistency=False → performance=True
     - StarterHelperModeManager.py: Added performance=True
- **Validation**: Documentation complete and accurate

**Files to Modify**:
- `updates/done/performance_scoring_code_changes.md`

### Task 3.5: Final commit and cleanup ⬜ TODO

```bash
git status
git diff
```

- **Commit**: "Complete performance scoring implementation - all requirements met"
- Move `updates/update_consistency.txt` to `updates/done/` (if not already)
- Delete `updates/update_consistency_questions.md`
- Delete `updates/todo-files/update_consistency_todo.md`
- Delete `updates/todo-files/performance_scoring_completion_todo.md` (this file)
- **Validation**: All objective files properly organized

---

## Pre-Commit Validation Checklist

**EXECUTE AT END OF EVERY PHASE**:

1. ✅ Analyze changes: `git status` and `git diff`
2. ✅ Run all unit tests: `python tests/run_all_tests.py`
3. ✅ Verify 100% test pass rate
4. ✅ Manual testing of affected functionality
5. ✅ Update documentation if needed
6. ✅ Commit with proper message format

**STOP if any tests fail. Fix issues before proceeding to next phase.**

---

## Summary

**Total Phases**: 3
- Phase 1: Player-data-fetcher updates (Requirement #6)
- Phase 2: Simulation system updates (Requirement #15)
- Phase 3: Final verification and documentation

**Critical Success Factors**:
- ALL requirements from update_consistency.txt must be implemented
- ALL question answers from update_consistency_questions.md must be addressed
- 100% unit test pass rate required
- Manual integration testing required
- Complete documentation required

**NO HALF MEASURES. NO PARTIAL IMPLEMENTATIONS.**

---

## Notes

- This TODO was created after discovering missing requirements during final review
- Original implementation was ~90% complete but missing critical integration points
- Requirements #6 and #15 were completely missing
- Requirement #13 was partially missing (fixed during review)
- Bug in TradeSimTeam.py would have caused TypeError (fixed during review)

**Keep this file updated as you complete each task!**
