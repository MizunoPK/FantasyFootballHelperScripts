# Reserve Assessment Mode - Final Implementation Checklist

**Purpose**: Comprehensive pre-implementation checklist to ensure nothing is missed

**Date**: Iteration 10 - Verification Round 3

**Status**: All verifications complete, ready to implement

---

## Pre-Implementation Verification ✅

### Requirements Coverage
- [x] All 21 requirements identified
- [x] 21/21 requirements covered (100%)
- [x] All 5 scoring factors included
- [x] Schedule multiplier verified and included
- [x] User decisions integrated (5/5 answered)

### Code Pattern Research
- [x] Mode manager pattern researched (4 existing modes)
- [x] Scoring algorithm documented (5 factors with code snippets)
- [x] Historical data loading pattern found
- [x] CSV loading utilities identified
- [x] Test patterns researched

### Data Access Verification
- [x] Historical data files exist (players.csv, teams.csv, schedule.csv)
- [x] All scoring data sources verified
- [x] All multiplier methods verified (ConfigManager)
- [x] All team/schedule methods verified (TeamDataManager, SeasonScheduleManager)
- [x] Complete data flow documented

### Integration Verification
- [x] LeagueHelperManager integration points identified (exact line numbers)
- [x] No conflicts with existing modes
- [x] No import cycle risks
- [x] No shared state issues

---

## Implementation Checklist

### Phase 1: Historical Data Infrastructure

#### Task 1.1: Verify data/last_season/ folder structure
- [x] ALREADY VERIFIED - files exist with correct schema

#### Task 1.2: Create _load_historical_data() method
- [ ] Implement in ReserveAssessmentModeManager.__init__()
- [ ] Load from `data_folder / 'last_season' / 'players.csv'`
- [ ] Use csv.DictReader pattern (PlayerManager.py:158)
- [ ] Create FantasyPlayer objects with FantasyPlayer.from_dict()
- [ ] Build dictionary: `{(name.lower(), position): FantasyPlayer}`
- [ ] Handle missing file gracefully (try/except, return empty dict)
- [ ] Add debug logging for load success/failure

**Expected Result**: `self.historical_players_dict` populated on initialization

#### Task 1.3: Implement player matching logic
- [ ] Implemented in get_recommendations() method
- [ ] Match key: `(current_player.name.lower(), current_player.position)`
- [ ] Lookup: `historical_players_dict.get(key)`
- [ ] Skip if None (log debug message)
- [ ] Use current player's team for scoring (not historical team)

**Expected Result**: Current players matched to historical data

---

### Phase 2: Reserve Assessment Mode Core

#### Task 2.1: Create ReserveAssessmentModeManager class
- [ ] Create file: `league_helper/reserve_assessment_mode/ReserveAssessmentModeManager.py`
- [ ] Create file: `league_helper/reserve_assessment_mode/__init__.py`
- [ ] Add class docstring (Google style)
- [ ] Implement __init__(config, player_manager, team_data_manager, season_schedule_manager, data_folder)
- [ ] Implement set_managers(player_manager, team_data_manager)
- [ ] Implement start_interactive_mode(player_manager, team_data_manager)
- [ ] Implement get_recommendations() -> List[ScoredPlayer]
- [ ] Implement _load_historical_data() -> Dict
- [ ] Implement _score_reserve_candidate(current, historical) -> ScoredPlayer
- [ ] Implement _calculate_schedule_value(player) -> Optional[float]
- [ ] Add all required imports

**Lines of Code Estimate**: ~400-500 lines

#### Task 2.2: Implement player filtering
- [ ] In get_recommendations(): Get undrafted players
- [ ] Filter: `player.get_risk_level() == "HIGH"`
- [ ] Filter: `player.position not in ["K", "DST"]`
- [ ] Filter: `player.fantasy_points > 0`

**Expected Result**: List of IR-eligible candidates

#### Task 2.3: Implement _score_reserve_candidate() method
- [ ] 2.3.1: Normalization - `score = historical_player.fantasy_points`
- [ ] 2.3.2: Player rating multiplier (historical)
- [ ] 2.3.3: Team quality multiplier (current)
- [ ] 2.3.4: Performance/consistency multiplier (historical weekly data)
- [ ] 2.3.5: Schedule multiplier (current, via _calculate_schedule_value)
- [ ] Build reasons list for each step
- [ ] Return ScoredPlayer(player=current_player, score=score, reason=reasons)

**Expected Result**: ScoredPlayer with final score and reasoning

#### Task 2.4: Implement recommendation ranking
- [ ] Sort scored_players by score descending
- [ ] Return top 15: `scored_players[:15]`

**Expected Result**: Top 15 reserve candidates

#### Task 2.5: Implement display logic
- [ ] Print header: "RESERVE ASSESSMENT - High-Value Injured Players"
- [ ] Print count: "Found {count} reserve candidates..."
- [ ] Loop and print: `for i, sp in enumerate(recommendations, 1): print(f"{i}. {sp}")`
- [ ] Handle empty case: "No reserve candidates found."
- [ ] Wait for user: `input("\nPress Enter to return to Main Menu...")`

**Expected Result**: User sees formatted recommendations

---

### Phase 3: Integration with Main Menu

#### Task 3.1: Update LeagueHelperManager.py - Imports
- [ ] Add import: `from reserve_assessment_mode.ReserveAssessmentModeManager import ReserveAssessmentModeManager`
- [ ] Location: After other mode manager imports

#### Task 3.2: Update LeagueHelperManager.py - Initialization
- [ ] Add initialization in __init__ (line ~94):
  ```python
  self.reserve_assessment_mode_manager = ReserveAssessmentModeManager(
      self.config,
      self.player_manager,
      self.team_data_manager,
      self.season_schedule_manager,
      data_folder
  )
  ```

#### Task 3.3: Update LeagueHelperManager.py - Menu Display
- [ ] Update line 121: Add "Reserve Assessment" to options list
- [ ] New list: `["Add to Roster", "Starter Helper", "Trade Simulator", "Modify Player Data", "Reserve Assessment"]`

#### Task 3.4: Update LeagueHelperManager.py - Menu Handling
- [ ] Add after choice == 4 block:
  ```python
  elif choice == 5:
      self.logger.info("Starting Reserve Assessment mode")
      self._run_reserve_assessment_mode()
  ```
- [ ] Update existing choice == 5 to choice == 6 (Quit)

#### Task 3.5: Update LeagueHelperManager.py - Delegation Method
- [ ] Add new method after _run_trade_simulator_mode():
  ```python
  def _run_reserve_assessment_mode(self):
      """Delegate to Reserve Assessment mode manager."""
      self.reserve_assessment_mode_manager.start_interactive_mode(
          self.player_manager,
          self.team_data_manager
      )
  ```

---

### Phase 4: Testing

#### Task 4.1: Create unit tests for historical data loading
- [ ] Create file: `tests/league_helper/reserve_assessment_mode/test_ReserveAssessmentModeManager.py`
- [ ] Create file: `tests/league_helper/reserve_assessment_mode/__init__.py`
- [ ] Test _load_historical_data() with valid CSV
- [ ] Test _load_historical_data() with missing file
- [ ] Test dictionary structure is correct
- [ ] Use tmp_path fixture for test data

#### Task 4.2: Create unit tests for player filtering
- [ ] Test filtering by get_risk_level() == "HIGH"
- [ ] Test excluding K/DST positions
- [ ] Test excluding players with 0 points
- [ ] Mock PlayerManager.get_player_list()

#### Task 4.3: Create unit tests for scoring algorithm
- [ ] Test _score_reserve_candidate() with all multipliers
- [ ] Test with missing player_rating (skip multiplier)
- [ ] Test with < 3 weeks data (skip performance multiplier)
- [ ] Test with no future opponents (skip schedule multiplier)
- [ ] Mock ConfigManager multiplier methods
- [ ] Mock TeamDataManager
- [ ] Mock SeasonScheduleManager

#### Task 4.4: Create unit tests for ReserveAssessmentModeManager
- [ ] Test __init__() receives all parameters
- [ ] Test set_managers() updates references
- [ ] Test get_recommendations() returns List[ScoredPlayer]
- [ ] Test get_recommendations() returns max 15 items
- [ ] Test start_interactive_mode() is callable
- [ ] Mock all dependencies

#### Task 4.5: Create integration test
- [ ] Add test case to `tests/integration/test_league_helper_integration.py`
- [ ] Test full workflow: menu → mode → display → return
- [ ] Use real test data files

#### Task 4.6: Run all existing tests (MANDATORY)
- [ ] Command: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Fix any failures immediately

#### Task 4.7: Manual E2E testing
- [ ] Run: `python run_league_helper.py`
- [ ] Select option 5 "Reserve Assessment"
- [ ] Verify recommendations display correctly
- [ ] Verify return to menu works
- [ ] Test all other modes still work (no regression)

---

### Phase 5: Documentation

#### Task 5.1: Update README.md
- [ ] Add Reserve Assessment to "League Helper Module" section
- [ ] Describe purpose and functionality
- [ ] Explain scoring methodology (5 factors)
- [ ] Add usage example

#### Task 5.2: Update CLAUDE.md
- [ ] Add reserve_assessment_mode to mode listing (line ~35)
- [ ] Update "Main Scripts" section if needed
- [ ] Update project structure section
- [ ] Update test counts (add ~50-100 tests)

#### Task 5.3: Add docstrings to all new code
- [ ] ReserveAssessmentModeManager class docstring
- [ ] All method docstrings (Google style)
- [ ] Parameter descriptions
- [ ] Return value descriptions
- [ ] Usage examples where helpful

#### Task 5.4: Update code changes documentation
- [ ] Document all file modifications in `reserve_assessment_code_changes.md`
- [ ] Include file paths, line numbers, code snippets
- [ ] Document incrementally as changes are made

---

### Phase 6: Final Validation

#### Task 6.1: Run full test suite (MANDATORY)
- [ ] Command: `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Review any warnings

#### Task 6.2: Code review and cleanup
- [ ] Remove any debug logging
- [ ] Remove commented code
- [ ] Check import ordering
- [ ] Verify all imports are used
- [ ] Check code style consistency

#### Task 6.3: Update TODO file status
- [ ] Mark all completed tasks in `reserve_assessment_todo.md`
- [ ] Move to "COMPLETE" status

#### Task 6.4: Move files to updates/done/
- [ ] Move `updates/reserve_assessment.txt` to `updates/done/`
- [ ] Move `updates/reserve_assessment_questions.md` to `updates/done/`
- [ ] Keep TODO and code_changes files for reference

#### Task 6.5: Create git commit (MANDATORY PRE-COMMIT VALIDATION)
- [ ] Run: `python tests/run_all_tests.py` (must pass 100%)
- [ ] Run: `git status` and `git diff` to review changes
- [ ] Stage files: `git add .`
- [ ] Create commit with message:
  ```
  Add Reserve Assessment mode for high-value reserve players

  - Add new Reserve Assessment mode (5th League Helper mode)
  - Identify undrafted players on IR with high historical value
  - Implement 5-factor scoring: normalization, player rating, team quality, performance, schedule
  - Load historical data from last_season/ folder
  - Display top 15 reserve candidates with scoring breakdown
  - Add comprehensive unit tests (50+ new tests)
  - Update documentation (README.md, CLAUDE.md)
  - Integrate with main League Helper menu as option 5
  ```

---

## Files to Create (9 new files)

1. [ ] `league_helper/reserve_assessment_mode/__init__.py`
2. [ ] `league_helper/reserve_assessment_mode/ReserveAssessmentModeManager.py`
3. [ ] `tests/league_helper/reserve_assessment_mode/__init__.py`
4. [ ] `tests/league_helper/reserve_assessment_mode/test_ReserveAssessmentModeManager.py`

## Files to Modify (3 files)

5. [ ] `league_helper/LeagueHelperManager.py` (~20 lines added/modified)
6. [ ] `README.md` (~10-20 lines added)
7. [ ] `CLAUDE.md` (~5-10 lines modified)

## Documentation Files (already created)

8. [x] `updates/reserve_assessment_todo.md` (tracking)
9. [x] `updates/reserve_assessment_questions.md` (answered)
10. [x] `updates/reserve_assessment_code_changes.md` (incremental)
11. [x] `updates/reserve_assessment_requirements_verification.md`
12. [x] `updates/reserve_assessment_data_flow.md`
13. [x] `updates/reserve_assessment_integration_verification.md`
14. [x] `updates/reserve_assessment_implementation_checklist.md` (this file)

---

## Estimated Effort

- **Phase 1**: 30-45 minutes (historical data loading)
- **Phase 2**: 2-3 hours (core mode manager implementation)
- **Phase 3**: 15-30 minutes (integration)
- **Phase 4**: 1-2 hours (comprehensive testing)
- **Phase 5**: 30-45 minutes (documentation)
- **Phase 6**: 15-30 minutes (validation and commit)

**Total Estimated Time**: 5-7 hours

---

## Success Criteria

- [x] All verification complete (10 iterations done)
- [ ] All 6 phases complete
- [ ] 100% test pass rate
- [ ] No regressions in existing modes
- [ ] All documentation updated
- [ ] Code committed with proper message
- [ ] Reserve Assessment mode functional and usable

---

## Ready to Implement

✅ **ALL VERIFICATIONS COMPLETE**
✅ **ALL QUESTIONS ANSWERED**
✅ **ALL PATTERNS RESEARCHED**
✅ **ALL INTEGRATIONS VERIFIED**
✅ **COMPLETE IMPLEMENTATION PLAN READY**

**Status**: 🟢 **READY TO BEGIN IMPLEMENTATION**
