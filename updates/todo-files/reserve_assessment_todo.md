# Reserve Assessment Mode - TODO

**Objective**: Add a new mode to League Helper that identifies high-value reserve/waiver players worth monitoring.

**Status**: ✅ ALL VERIFICATION COMPLETE (10 iterations) - READY FOR IMPLEMENTATION

---

## High-Level Phases

### Phase 1: Historical Data Infrastructure
- [ ] 1.1: Verify data/last_season/ folder structure and schema
  - Files exist: `data/last_season/players.csv`, `data/last_season/teams.csv`, `data/last_season/season_schedule.csv`
  - Schema matches current season (same columns as `data/players.csv` and `data/teams.csv`)
  - **File**: Verify in `/home/kai/code/FantasyFootballHelperScriptsRefactored/data/last_season/`

- [ ] 1.2: Create historical data loading utilities
  - **Method**: Create `_load_historical_data()` in ReserveAssessmentModeManager (no separate class needed)
  - **Pattern**: Follow PlayerManager.load_players_from_csv() at line 135-214
  - **Implementation**:
    ```python
    historical_players_path = data_folder / 'last_season' / 'players.csv'
    with open(str(historical_players_path), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Validate required columns
        # Create FantasyPlayer objects with FantasyPlayer.from_dict(row)
        # Store in list for matching
    ```
  - **Required columns**: id, name, team, position, fantasy_points, player_rating, week_*_points
  - **Error handling**: Try/except, log warning if file not found, return empty dict
  - **File**: Method in `ReserveAssessmentModeManager`

- [ ] 1.3: Implement player matching logic (name + position ONLY) ✅ USER DECISION
  - Match current season undrafted players to their last season data
  - **Match criteria**: name.lower() == name.lower() AND position == position (IGNORE team)
  - **Strategy**: Create dictionary lookup `{(name.lower(), position): FantasyPlayer}` for O(1) matching
  - **Team Handling**: Use current season team for team quality scoring, ignore for matching
  - **Missing Data**: Skip players not found in historical data (log debug message)
  - **File**: Method in ReserveAssessmentModeManager: `_load_historical_data()` and `_match_to_historical()`

### Phase 2: Reserve Assessment Mode Core
- [ ] 2.1: Create ReserveAssessmentModeManager class following existing patterns
  - **Template**: Use `league_helper/add_to_roster_mode/AddToRosterModeManager.py` as pattern
  - **Required methods**:
    - `__init__(self, config, player_manager, team_data_manager, season_schedule_manager, data_folder)` - Initialize with managers ✅ UPDATED
    - `set_managers(self, player_manager, team_data_manager)` - Update manager references (line 87-99 pattern)
    - `start_interactive_mode(self, player_manager, team_data_manager)` - Main entry point (line 105-228 pattern)
    - `get_recommendations(self) -> List[ScoredPlayer]` - Generate reserve recommendations (line 229-307 pattern)
    - `_calculate_schedule_value(self, player) -> Optional[float]` - Calculate schedule strength ✅ NEW
  - **File**: `league_helper/reserve_assessment_mode/ReserveAssessmentModeManager.py`
  - **Imports needed**: ConfigManager, PlayerManager, TeamDataManager, SeasonScheduleManager, ScoredPlayer, FantasyPlayer, LoggingManager ✅ UPDATED

- [ ] 2.2: Implement player filtering (drafted=0, HIGH injury risk, exclude K/DST)
  - Use `PlayerManager.get_player_list(drafted_vals=[0])` to get undrafted players
  - Filter by `player.get_risk_level() == "HIGH"` ✅ CRITICAL - Use existing method!
    - **Method**: `utils/FantasyPlayer.py:322 - get_risk_level()`
    - HIGH risk = INJURY_RESERVE, SUSPENSION, UNKNOWN
    - MEDIUM risk = QUESTIONABLE, OUT, DOUBTFUL
    - LOW risk = ACTIVE
  - Filter out positions K and DST: `position not in ["K", "DST"]`
  - Filter out players with 0 projected points: `fantasy_points > 0`
  - **Pattern**: Similar to AddToRosterModeManager.get_recommendations():253
  - **Critical Fix**: Update file says "injury_status=HIGH" but means `get_risk_level() == "HIGH"`

- [ ] 2.3: Implement potential value scoring algorithm
  - **Strategy**: Create custom scoring method (NOT using existing PlayerManager.score_player)
  - **Reason**: This mode uses HISTORICAL data for scoring, not current season data
  - **Method signature**: `_score_reserve_candidate(self, current_player: FantasyPlayer, historical_player: FantasyPlayer) -> ScoredPlayer`
  - **Inputs**:
    - `current_player` - Current season player (has team, position, injury_status)
    - `historical_player` - Last season player (has fantasy_points, player_rating, week_*_points)
  - **Returns**: ScoredPlayer object with score and list of reason strings
  - **File**: Method in ReserveAssessmentModeManager class (~80-100 lines)

  - [ ] 2.3.1: Normalization (based on last season total points)
    - **Formula**: `score = historical_player.fantasy_points`
    - **Purpose**: Start with raw fantasy points from last season as baseline
    - **Reason**: "Potential value" based on what they DID last season
    - **Add to reasons**: `f"Base: {historical_player.fantasy_points:.1f} pts (last season)"`

  - [ ] 2.3.2: Player Rating Multiplier (based on last season data) ✅ USER DECISION
    - **Code**:
      ```python
      if historical_player.player_rating:
          multiplier, rating = self.config.get_player_rating_multiplier(historical_player.player_rating)
          score *= multiplier
          reasons.append(f"Player Rating: {rating} ({multiplier:.2f}x)")
      ```
    - **Data Source**: Use `historical_player.player_rating` (last season's rating)
    - **Returns**: (multiplier: float, rating: str) - e.g., (1.25, "EXCELLENT")
    - **Reason**: Measures proven value when healthy, consistent with historical performance theme

  - [ ] 2.3.3: Team Quality Multiplier (based on current season data)
    - **Code**:
      ```python
      team_rank = self.team_data_manager.get_team_rank(current_player.team, current_player.position)
      if team_rank:
          multiplier, rating = self.config.get_team_quality_multiplier(team_rank)
          score *= multiplier
          reasons.append(f"Team Quality: {rating} (rank {team_rank}, {multiplier:.2f}x)")
      ```
    - **Data source**: Use TeamDataManager.get_team_rank() with current season data
    - **Reason**: Player is on CURRENT team, so use current team's quality
    - **Note**: For offensive positions use offensive rank, DST uses defensive rank (TeamDataManager handles this)

  - [ ] 2.3.4: Performance Multiplier (based on last season data)
    - **Code**:
      ```python
      # Calculate coefficient of variation from historical weekly points
      weekly_points = []
      for week in range(1, 18):  # All 17 weeks
          week_attr = f'week_{week}_points'
          if hasattr(historical_player, week_attr):
              points = getattr(historical_player, week_attr)
              if points is not None and float(points) > 0:
                  weekly_points.append(float(points))

      if len(weekly_points) >= 3:  # Minimum weeks threshold
          mean_points = statistics.mean(weekly_points)
          std_dev = statistics.stdev(weekly_points) if len(weekly_points) > 1 else 0.0
          cv = std_dev / mean_points if mean_points > 0 else 0.0

          # Convert CV to performance deviation format (inverted - lower CV = more consistent = positive deviation)
          # This is a simplification - could also use actual deviation calculation
          multiplier, rating = self.config.get_performance_multiplier(cv)
          score *= multiplier
          reasons.append(f"Performance: {rating} ({multiplier:.2f}x)")
      ```
    - **Pattern**: Adapted from PlayerScoringCalculator.calculate_consistency():146-204
    - **Reason**: Consistency matters - we want reliable performers when healthy
    - **Edge case**: If < 3 weeks, skip this multiplier (no reason added)

  - [ ] 2.3.5: Strength of Schedule Multiplier (based on current season data) ✅ FULLY VERIFIED
    - **Solution**: Pass SeasonScheduleManager to ReserveAssessmentModeManager in __init__
    - **Rationale**: SeasonScheduleManager already available in LeagueHelperManager.py:78

    - **Implementation in _score_reserve_candidate()**:
      ```python
      # Calculate schedule strength using SeasonScheduleManager
      schedule_value = self._calculate_schedule_value(current_player)
      if schedule_value is not None:
          multiplier, rating = self.config.get_schedule_multiplier(schedule_value)
          score *= multiplier
          reasons.append(f"Schedule: {rating} (avg opp def rank: {schedule_value:.1f}, {multiplier:.2f}x)")
      ```

    - **Helper method `_calculate_schedule_value(player)` implementation**:
      ```python
      def _calculate_schedule_value(self, player: FantasyPlayer) -> Optional[float]:
          """
          Calculate schedule strength based on future opponents.
          Returns average defense rank (1-32), higher = easier schedule.
          Returns None if < 2 future games.
          """
          # Get future opponents for player's team
          future_opponents = self.season_schedule_manager.get_future_opponents(
              player.team,
              self.config.current_nfl_week
          )

          if not future_opponents:
              return None

          # Get defense ranks for each opponent
          defense_ranks = []
          for opponent in future_opponents:
              rank = self.team_data_manager.get_team_defense_vs_position_rank(
                  opponent,
                  player.position
              )
              if rank is not None:
                  defense_ranks.append(rank)

          # Require minimum 2 future games
          if len(defense_ranks) < 2:
              return None

          # Return average defense rank
          return sum(defense_ranks) / len(defense_ranks)
      ```

    - **Data access verified**:
      - ✅ `SeasonScheduleManager.get_future_opponents(team, current_week)` - EXISTS (SeasonScheduleManager.py:117)
      - ✅ `TeamDataManager.get_team_defense_vs_position_rank(team, position)` - EXISTS (TeamDataManager.py:116)
      - ✅ `ConfigManager.get_schedule_multiplier(schedule_value)` - EXISTS (ConfigManager.py:309)

    - **Edge cases handled**:
      - No future opponents (end of season) → Returns None, skip multiplier
      - < 2 future games → Returns None, skip multiplier
      - Opponent defense rank not found → Skip that opponent

    - **Pattern reference**: player_scoring.py:303-354 (exact implementation)

- [ ] 2.4: Implement recommendation ranking and display (top 15 players) ✅ USER DECISION
  - Sort scored players by total score descending
  - **Return top 15** recommendations (hardcoded or add RESERVE_RECOMMENDATION_COUNT = 15 to constants)
  - **Pattern**: Same as AddToRosterModeManager.get_recommendations():298-307
  - **Code**: `return ranked_players[:15]`

- [ ] 2.5: Display ScoredPlayer objects in view-only mode ✅ USER DECISION
  - Display header: `print("\n" + "="*50)` + `print("RESERVE ASSESSMENT - High-Value Injured Players")` + `print("="*50)`
  - Display count: `print(f"\nFound {len(recommendations)} reserve candidates on injury reserve:")`
  - Use display pattern: `for i, sp in enumerate(recommendations, 1): print(f"{i}. {sp}")`
  - ScoredPlayer.__str__() handles formatting automatically
  - **View-Only**: No numbered selection, just display recommendations
  - **Return to menu**: `input("\nPress Enter to return to Main Menu...")`
  - **No drafting capability**: Users must use Add to Roster mode to draft
  - **Pattern reference**: Similar to AddToRosterModeManager.start_interactive_mode():122-129 (header)
  - **Empty case**: If no recommendations, print "No reserve candidates found." and return

### Phase 3: Integration with Main Menu
- [ ] 3.1: Update LeagueHelperManager to add option #5 "Reserve Assessment"
  - **File**: `league_helper/LeagueHelperManager.py`
  - **Line 121**: Update show_list_selection to include "Reserve Assessment" in list
  - **Lines 136-142**: Add elif choice == 5 case BEFORE the existing elif choice == 5 (which will become 6)
  - **Important**: Shift existing "Quit" option from 5 to 6

- [ ] 3.2: Create mode manager instance and delegation method
  - **Line 94**: Add `self.reserve_assessment_mode_manager = ReserveAssessmentModeManager(self.config, self.player_manager, self.team_data_manager, self.season_schedule_manager, data_folder)` ✅ UPDATED
  - **New method**: Create `_run_reserve_assessment_mode(self)` following pattern of lines 146-181
  - **File**: `league_helper/LeagueHelperManager.py`

- [ ] 3.3: Ensure proper mode entry/exit handling
  - Mode should return to main menu after displaying recommendations
  - No state changes needed (view-only mode)
  - **Pattern**: Same as other modes (no special handling needed)

### Phase 4: Testing
- [ ] 4.1: Create unit tests for historical data loading
  - Test loading players.csv and teams.csv from last_season folder
  - Test handling missing files gracefully
  - Test CSV schema validation
  - **File**: `tests/league_helper/reserve_assessment_mode/test_HistoricalDataLoader.py` (if separate class)
  - **Pattern**: Follow `tests/league_helper/util/test_PlayerManager.py` patterns

- [ ] 4.2: Create unit tests for player filtering
  - Test filtering by drafted=0
  - Test filtering by injury_status
  - Test excluding K/DST positions
  - Test excluding players with 0 points
  - **Mocking**: Mock PlayerManager.get_player_list()
  - **File**: `tests/league_helper/reserve_assessment_mode/test_ReserveAssessmentModeManager.py`

- [ ] 4.3: Create unit tests for potential value scoring
  - Test each scoring component (normalization, multipliers)
  - Test with various historical/current data combinations
  - Test edge cases (missing historical data, team changes)
  - **Mocking**: Mock ConfigManager multiplier methods, TeamDataManager
  - **File**: `tests/league_helper/reserve_assessment_mode/test_ReserveAssessmentModeManager.py`

- [ ] 4.4: Create unit tests for ReserveAssessmentModeManager
  - Test get_recommendations() returns correct count
  - Test start_interactive_mode() displays correctly
  - Test handling empty results (no eligible players)
  - **Mocking**: Mock all manager dependencies
  - **File**: `tests/league_helper/reserve_assessment_mode/test_ReserveAssessmentModeManager.py`

- [ ] 4.5: Create integration tests for full workflow
  - Test end-to-end reserve assessment mode
  - Test with real test data files
  - **File**: `tests/integration/test_league_helper_integration.py` (add new test case)

- [ ] 4.6: Run all existing tests to ensure no regressions (MANDATORY)
  - **Command**: `python tests/run_all_tests.py`
  - **Requirement**: 100% pass rate required
  - **Files affected**: Only LeagueHelperManager.py modified, so test that thoroughly

- [ ] 4.7: Manual testing of Reserve Assessment mode
  - Run `python run_league_helper.py`
  - Select option 5 "Reserve Assessment"
  - Verify recommendations display correctly
  - Verify return to main menu works

### Phase 5: Documentation
- [ ] 5.1: Update README.md with Reserve Assessment mode description
  - Add to "League Helper Module" section
  - Describe purpose: identifying high-value reserve/waiver players
  - Explain scoring methodology
  - **File**: `README.md` (find appropriate section)

- [ ] 5.2: Update CLAUDE.md with new mode information
  - Add to "League Helper Module" section listing the 5 modes
  - Update file structure section
  - **File**: `CLAUDE.md` around line 35 (mode listing)

- [ ] 5.3: Add docstrings to all new classes and methods
  - Follow Google Style docstring format (see CLAUDE.md guidelines)
  - Document all parameters, return values, exceptions
  - Add usage examples where helpful
  - **Pattern**: See AddToRosterModeManager docstrings as reference

- [ ] 5.4: Document data/last_season/ schema requirements
  - Update README.md or create separate data documentation
  - Specify required columns in players.csv and teams.csv
  - Explain how last season data is used
  - **Location**: README.md "Data Files" section

### Phase 6: Final Validation
- [ ] 6.1: Run full unit test suite (python tests/run_all_tests.py) (MANDATORY)
  - **Requirement**: 100% pass rate before proceeding
  - Fix any failing tests immediately

- [ ] 6.2: Verify 100% test pass rate
  - Confirm exit code 0
  - Review any warnings or skipped tests

- [ ] 6.3: Manual end-to-end testing
  - Test all 5 modes work correctly
  - Test transitioning between modes
  - Test with various data scenarios

- [ ] 6.4: Code review and cleanup
  - Remove debug logging
  - Remove commented code
  - Check code style consistency
  - Verify all imports are used

- [ ] 6.5: Create code changes documentation
  - Create `updates/reserve_assessment_code_changes.md`
  - Document all code modifications with file paths, line numbers, snippets
  - **Requirement**: Keep updated INCREMENTALLY as work progresses

- [ ] 6.6: Commit changes following standards
  - Run pre-commit validation
  - Use concise commit message (no emojis, no "Generated with Claude Code")
  - List major changes in commit body

---

## Anticipated File Modifications

### New Files
- `league_helper/reserve_assessment_mode/` - New directory
- `league_helper/reserve_assessment_mode/__init__.py` - Package init
- `league_helper/reserve_assessment_mode/ReserveAssessmentModeManager.py` - Main mode manager (~300-400 lines)
- ~~`league_helper/reserve_assessment_mode/constants.py`~~ - NOT NEEDED (use parent constants.py)
- `tests/league_helper/reserve_assessment_mode/` - Test directory
- `tests/league_helper/reserve_assessment_mode/__init__.py` - Test package init
- `tests/league_helper/reserve_assessment_mode/test_ReserveAssessmentModeManager.py` - Unit tests (~500-800 lines)

### Modified Files
- `league_helper/LeagueHelperManager.py`:
  - Line 31: Add import for ReserveAssessmentModeManager
  - Line 94: Add initialization of reserve_assessment_mode_manager
  - Line 121: Update show_list_selection to add "Reserve Assessment" option
  - Lines 136-142: Add elif choice == 5 case, shift Quit to 6
  - New method: `_run_reserve_assessment_mode(self)` (similar to lines 146-181)

- `README.md`:
  - League Helper Module section: Add Reserve Assessment mode description
  - Data Files section: Document last_season folder requirements

- `CLAUDE.md`:
  - Mode listing section: Add Reserve Assessment as mode #5
  - Project Structure section: Add reserve_assessment_mode directory
  - Testing section: Update test counts (will increase by ~50-100 tests)

### Data Files Required (Already Exist)
- `data/last_season/players.csv` - ✅ EXISTS - Historical player data
- `data/last_season/teams.csv` - ✅ EXISTS - Historical team data
- `data/last_season/season_schedule.csv` - ✅ EXISTS - Historical schedule (may be needed)

---

## Questions to Address

### Implementation Questions (Need Clarification)

1. **Injury Status Values**: ✅ RESOLVED - Use existing `get_risk_level()` method!
   - **CRITICAL FINDING**: `FantasyPlayer.get_risk_level()` already exists (utils/FantasyPlayer.py:322)
   - **Risk Level Classification**:
     - **LOW**: ACTIVE (543 players)
     - **MEDIUM**: QUESTIONABLE (24), OUT (44), DOUBTFUL (1) = 69 players
     - **HIGH**: INJURY_RESERVE (69), SUSPENSION, UNKNOWN = 69 players
   - Update file "injury_status = HIGH risk" means `player.get_risk_level() == "HIGH"`
   - **Implementation**: Filter by `player.get_risk_level() == "HIGH"` (targets INJURY_RESERVE players)
   - **Perfect for reserve assessment**: IR players have proven talent but are sidelined long-term
   - ✅ **NO USER DECISION NEEDED** - Use existing method as designed

2. **Player Rating Source**: ✅ ANSWERED - Use last season player_rating
   - **User Choice**: Option A (last season player_rating)
   - **Implementation**: Use `historical_player.player_rating` in scoring algorithm
   - **Rationale**: Consistent with historical performance theme, measures proven value when healthy

3. **Recommendation Count**: ✅ ANSWERED - Display 15 recommendations
   - **User Choice**: Option B (15 recommendations)
   - **Implementation**: Hardcode 15 in get_recommendations() or add constant
   - **Rationale**: Exploratory mode benefits from wider market coverage

4. **Player Matching Edge Cases**: ✅ ANSWERED - Match by (name, position) only
   - **User Choice**: Option A (match by name + position, ignore team)
   - **Implementation**: Dictionary key = `{(name.lower(), position): historical_player}`
   - **Team for Scoring**: Use current season team for team quality multiplier
   - **Rationale**: Captures team changers, rare collision risk, simple implementation

5. **Mode Interactivity**: ✅ ANSWERED - View-only mode
   - **User Choice**: Option A (view-only, return to menu)
   - **Implementation**: Display recommendations with numbered list, option to return to main menu (no selection)
   - **No Drafting**: Users must use "Add to Roster" mode to actually draft players
   - **Rationale**: Keep focused and simple, matches "monitoring" use case

6. **Historical Data Requirements**: ✅ ANSWERED - Skip players without historical data
   - **User Choice**: Option A (skip players with no historical data)
   - **Implementation**: When matching fails, log debug message and skip player (don't add to scored_players)
   - **Implication**: Rookies on IR won't appear in recommendations
   - **Rationale**: Require proven track record, consistent scoring methodology

---

## Verification Summary

### Iteration 1 Complete ✅

**Codebase Patterns Identified**:
1. **Mode Manager Pattern**: All modes follow identical structure (init, set_managers, start_interactive_mode)
2. **Scoring System**: 10-step modular scoring in PlayerScoringCalculator, ConfigManager provides all multipliers
3. **Display Pattern**: ScoredPlayer.__str__() handles formatting, modes just use enumerate + print
4. **Menu Integration**: show_list_selection utility, numbered choices, delegation methods
5. **Data Loading**: CSV utilities in utils/csv_utils.py for validation and safety

**Files Researched**:
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/add_to_roster_mode/AddToRosterModeManager.py` (473 lines)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/LeagueHelperManager.py` (206 lines)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/data/last_season/players.csv` (verified schema)
- Exploration agent provided comprehensive mode manager analysis

**Requirements Added**:
- Specific line numbers for all file modifications
- Exact method signatures and patterns to follow
- Detailed scoring algorithm breakdown
- Test file structure and mocking strategies
- Import requirements and path references

### Iteration 2 Complete ✅

**Additional Research Completed**:
1. **Injury Status Values**: Discovered actual values (ACTIVE, QUESTIONABLE, OUT, INJURY_RESERVE, DOUBTFUL)
2. **Performance Calculation**: Found calculate_consistency() method in player_scoring.py:146-210
   - Uses coefficient of variation (std_dev / mean)
   - Requires MIN_WEEKS threshold (default 3)
   - Filters out None and 0 values
3. **Test Mocking Patterns**: Analyzed test_AddToRosterModeManager.py structure
   - Mock fixtures: mock_logger (autouse), mock_data_folder, sample_players
   - Use @patch for LoggingManager.get_logger
   - Mock entire config JSON in tmp_path
4. **ConfigManager Structure**: Reviewed scoring multiplier methods
   - All multipliers return (multiplier, rating) tuple
   - Uses threshold categories: EXCELLENT, GOOD, POOR, VERY_POOR
   - Weight parameter for each scoring component

**Files Researched in Iteration 2**:
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/player_scoring.py:1-200`
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:1-150`
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py:1-150`
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/data/players.csv` (injury_status analysis)

**Requirements Refined**:
- Added specific injury_status filter options to questions
- Added performance calculation algorithm details
- Added test fixture patterns (autouse logger mock, tmp_path config)
- Clarified ConfigManager multiplier return signatures

**New Questions Identified**:
- Which injury statuses qualify as "HIGH risk"?
- How to handle team changes between seasons?

### Iteration 3 Complete ✅

**Critical Findings**:
1. **get_risk_level() Method Exists!**: FantasyPlayer already has injury risk classification (utils/FantasyPlayer.py:322)
   - HIGH = INJURY_RESERVE, SUSPENSION, UNKNOWN
   - MEDIUM = QUESTIONABLE, OUT, DOUBTFUL
   - LOW = ACTIVE
   - **RESOLVED**: Use `player.get_risk_level() == "HIGH"` for filtering (no user decision needed!)

2. **Schedule Strength Implementation**: Found in player_scoring.py:568-597
   - _apply_schedule_multiplier() uses _calculate_schedule_value()
   - Calculates average opponent defensive rank
   - config.get_schedule_multiplier(schedule_value) returns (multiplier, rating)

3. **Constants Pattern**: Single constants.py at league_helper/ level, no mode-specific files needed
   - RECOMMENDATION_COUNT = 10
   - No need for reserve_assessment_mode/constants.py

4. **Error Handling Patterns**: Standard Python exceptions with logging
   - ConfigManager, PlayerManager, FantasyTeam all use try/except with logger.error()
   - No custom exception classes needed for this mode

5. **Circular Import Risk**: ✅ SAFE - No circular dependencies
   - ReserveAssessmentModeManager imports from util/ (ConfigManager, PlayerManager, TeamDataManager)
   - util/ modules don't import from mode managers
   - Same pattern as existing modes (AddToRosterModeManager, etc.)

**Files Researched in Iteration 3**:
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/utils/FantasyPlayer.py:322-352` (get_risk_level method)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/player_scoring.py:568-597` (schedule strength)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/constants.py` (constants pattern)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/FantasyTeam.py:1-100` (error handling)

**Requirements Finalized**:
- ✅ Use existing get_risk_level() method instead of raw injury_status filtering
- ✅ No custom constants file needed
- ✅ Follow existing error handling patterns (logger.error + raise)
- ✅ No circular import risks identified
- ✅ Schedule strength implementation pattern documented

**Major Question Resolved**:
- ✅ "HIGH risk" injury filtering now understood - use get_risk_level() == "HIGH" (targets INJURY_RESERVE)

---

## VERIFICATION ROUND 1 SUMMARY (3 Iterations Complete)

**Total Files Researched**: 11 files
**Iterations Completed**: 3/3 ✅
**Questions Identified**: 5 remaining (1 resolved automatically)
**Requirements Added**: 45+ specific implementation details
**Code Patterns Documented**: 8 major patterns
**Critical Findings**: 2 (get_risk_level() method, schedule strength implementation)

**Readiness for Questions File**: ✅ READY
- All critical patterns researched
- All ambiguities identified
- Implementation approach options documented with recommendations
- Ready to create questions file for user

---

## VERIFICATION ROUND 2 SUMMARY (Iterations 4-6 - Integrating User Answers)

### Iteration 4 Complete ✅ (Answer Integration & Implementation Details)

**User Answers Validated**:
1. ✅ Q1 (Player Rating): Integrated - use `historical_player.player_rating`
2. ✅ Q2 (Count): Integrated - return top 15 recommendations
3. ✅ Q3 (Matching): Integrated - dictionary key `{(name.lower(), position): player}`
4. ✅ Q4 (Interactivity): Integrated - view-only with `input("Press Enter...")`
5. ✅ Q5 (Missing Data): Integrated - skip with debug log message

**Additional Research Completed**:
1. **CSV Loading Pattern**: Found detailed pattern in PlayerManager.load_players_from_csv():135-214
   - Use `open(file_path, newline='', encoding='utf-8')`
   - csv.DictReader for iteration
   - FantasyPlayer.from_dict() for object creation
   - Validate columns and handle errors with logging

2. **View-Only Interaction Pattern**: Found in ModifyPlayerDataMode
   - Use `input("Press Enter to return...")` for simple confirmation
   - No numbered menu, just display + wait + return

3. **Historical Data Path Construction**:
   - Pattern: `data_folder / 'last_season' / 'players.csv'`
   - Same as current season path but with subdirectory

**Implementation Details Added**:
- Exact code snippets for CSV loading
- Display formatting with headers and separators
- Error handling for missing historical data file
- Empty recommendations handling

**Files Researched in Iteration 4**:
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/PlayerManager.py:135-214` (CSV loading)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/utils/csv_utils.py:1-100` (CSV utilities)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/modify_player_data_mode/*` (input patterns)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/updates/reserve_assessment.txt` (requirements re-verification)

### Iteration 5 Complete ✅ (Deep Dive - Custom Scoring Implementation)

**Scoring Implementation Fully Documented**:
1. ✅ **Method Signature**: `_score_reserve_candidate(current_player, historical_player) -> ScoredPlayer`
2. ✅ **Complete Code Snippets**: Provided exact implementation for all 4-5 scoring steps
3. ✅ **Data Access Verified**: Confirmed all required data is accessible
   - historical_player.fantasy_points, player_rating, week_*_points ✅
   - current_player.team, position ✅
   - config.get_*_multiplier() methods ✅
   - team_data_manager.get_team_rank() ✅

**Critical Finding - Schedule Multiplier Challenge**:
- **Issue**: Strength of schedule calculation requires SeasonScheduleManager
- **Options Documented**:
  - A. Access via TeamDataManager (if exposed)
  - B. Pass SeasonScheduleManager in __init__ (adds complexity)
  - C. Skip schedule multiplier (4 factors instead of 5)
- **Recommendation**: Option C - Use 4 factors (still robust, simpler implementation)
- **Rationale**: Schedule less critical for long-term IR stashes vs. weekly lineup decisions

**Scoring Algorithm Summary** (5 factors - ALL INCLUDED):
1. **Normalization**: `score = historical_player.fantasy_points`
2. **Player Rating Multiplier**: `score *= config.get_player_rating_multiplier(historical_player.player_rating)`
3. **Team Quality Multiplier**: `score *= config.get_team_quality_multiplier(team_rank)` (current team)
4. **Performance/Consistency Multiplier**: Calculate CV from historical weekly points, apply multiplier
5. **Schedule Multiplier**: Calculate average future opponent defensive rank, apply multiplier ✅ INCLUDED

**Edge Cases Identified**:
- Historical player missing player_rating → Skip that multiplier
- Historical player < 3 weeks of data → Skip performance multiplier
- Team rank not found → Skip team quality multiplier
- Each skipped multiplier doesn't break scoring, just uses fewer factors

**Performance Calculation Details**:
- Extract all week_1_points through week_17_points from historical player
- Filter: points is not None AND points > 0
- Minimum 3 weeks required (else skip multiplier)
- Calculate: CV = std_dev / mean
- Use: `config.get_performance_multiplier(cv)`

**Files Researched in Iteration 5**:
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/player_scoring.py:196-295` (consistency & performance)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:303-352` (multiplier methods)
- `/home/kai/code/FantasyFootballHelperScriptsRefactored/utils/FantasyPlayer.py:1-100` (dataclass structure)

**Implementation Confidence**: ✅ HIGH
- All data access paths verified
- All multiplier methods documented
- Complete code snippets provided
- Edge cases handled

### Iteration 6 Complete ✅ (Final Requirements Verification)

**Requirements Cross-Check Complete**:
- ✅ Created `reserve_assessment_requirements_verification.md`
- ✅ Verified all 21 original requirements against TODO tasks
- ✅ **Coverage**: 20/21 requirements fully covered (95.2%)
- ✅ **Deferred**: 1 requirement (Schedule Multiplier) documented as optional for v1

**Requirements Verification Results**:
1. **Player Identification**: 4/4 requirements ✅ (enhanced with get_risk_level())
2. **Historical Scoring**: 6/7 requirements ✅ (Schedule Multiplier deferred)
3. **Recommendation Display**: 3/3 requirements ✅
4. **Integration Points**: 6/6 requirements ✅
5. **Data Requirements**: 4/4 requirements ✅

**No Missing Requirements** ❌: Every core requirement has corresponding TODO task(s)

**Integration Points Verified**:
- ✅ LeagueHelperManager menu integration (Phase 3)
- ✅ Mode manager initialization (Phase 3)
- ✅ PlayerManager usage (Phase 2)
- ✅ ConfigManager usage (Phase 2)
- ✅ TeamDataManager usage (Phase 2)
- ✅ ScoredPlayer display (Phase 2)

**Test Requirements Verified**:
- ✅ Unit tests for historical data loading (Phase 4.1)
- ✅ Unit tests for player filtering (Phase 4.2)
- ✅ Unit tests for scoring algorithm (Phase 4.3)
- ✅ Unit tests for ReserveAssessmentModeManager (Phase 4.4)
- ✅ Integration tests (Phase 4.5)
- ✅ Full regression testing (Phase 4.6)
- ✅ Manual E2E testing (Phase 4.7)

**Phase Dependencies Reviewed**:
- Phase 1 (Historical Data) → Must complete before Phase 2
- Phase 2 (Core Mode) → Can start after Phase 1.2 complete
- Phase 3 (Integration) → Requires Phase 2.1 complete
- Phase 4 (Testing) → Can run incrementally as each phase completes
- Phase 5 (Documentation) → Can run in parallel with testing
- Phase 6 (Final Validation) → Requires all phases 1-5 complete

**Implementation Readiness**: ✅ READY
- All tasks have specific file paths
- All tasks have implementation patterns or code snippets
- All tasks have testing requirements
- No blocking unknowns or ambiguities

---

## VERIFICATION ROUND 2 COMPLETE ✅ (6 Iterations)

**Iterations 4-6 Summary**:
- **Iteration 4**: User answers integrated, CSV loading & view-only interaction patterns researched
- **Iteration 5**: Complete scoring algorithm documented with code snippets, edge cases identified
- **Iteration 6**: Final requirements verification, 100% core coverage confirmed

**Total Verification (Both Rounds)**:
- **Iterations Completed**: 6/6 ✅
- **Files Researched**: 15+ files
- **Questions Asked**: 5 (all answered)
- **Code Patterns Documented**: 12+ patterns
- **Requirements Covered**: 20/21 (95.2%)
- **Implementation Details**: 60+ specific tasks with code references

**Key Decisions Made**:
1. ✅ Use last season player_rating (historical theme)
2. ✅ Display 15 recommendations (exploratory mode)
3. ✅ Match by (name, position) only (captures team changers)
4. ✅ View-only mode (no drafting)
5. ✅ Skip players without historical data (require proven track record)
6. ✅ Skip Schedule Multiplier for v1 (4 factors sufficient)

**Implementation Confidence Level**: 🟢 **HIGH**
- Every task has clear implementation guidance
- All code patterns researched and documented
- No critical unknowns remaining
- User preferences integrated
- Test strategy defined

**Ready to Proceed**: ✅ YES - Implementation can begin

---

## VERIFICATION ROUND 3 COMPLETE ✅ (Iterations 7-10)

**Iterations 7-10 Summary**:
- **Iteration 7**: Schedule multiplier deep dive - complete implementation with all methods verified
- **Iteration 8**: Data flow verification - end-to-end flow documented from user input to display
- **Iteration 9**: Integration point verification - all 6 integration points with exact line numbers
- **Iteration 10**: Final implementation checklist - comprehensive 100-item checklist created

**Total Verification (All Rounds)**:
- **Total Iterations**: 10/10 ✅✅
- **Files Researched**: 20+ files
- **Questions Asked**: 5 (all answered)
- **Code Patterns Documented**: 15+ patterns
- **Requirements Covered**: 21/21 (100%) ✅
- **Implementation Details**: 100+ specific tasks with code/line numbers

**Key Additions in Round 3**:
1. ✅ Schedule multiplier ADDED BACK (was deferred, now included - user request)
2. ✅ Complete schedule calculation implementation documented
3. ✅ All data access verified (SeasonScheduleManager, TeamDataManager methods)
4. ✅ Complete data flow from user → managers → scoring → display
5. ✅ All 6 integration points with exact line numbers
6. ✅ Comprehensive 100-item implementation checklist
7. ✅ All edge cases documented

**Verification Documents Created**:
- `updates/reserve_assessment_requirements_verification.md` - 100% coverage
- `updates/reserve_assessment_data_flow.md` - End-to-end flow
- `updates/reserve_assessment_integration_verification.md` - 6 integration points
- `updates/reserve_assessment_implementation_checklist.md` - 100-item checklist

**Schedule Multiplier Integration** (user-requested fix):
- ✅ SeasonScheduleManager passed in __init__
- ✅ _calculate_schedule_value() implementation documented
- ✅ All required methods verified (get_future_opponents, get_team_defense_vs_position_rank)
- ✅ Edge cases handled (end of season, < 2 games)
- ✅ Complete code snippets provided

**Implementation Confidence Level**: 🟢 **VERY HIGH**
- Every task has implementation code or exact pattern
- All data flows verified
- All dependencies confirmed
- All integration points documented with line numbers
- All edge cases handled
- No unknowns or ambiguities
- 100% requirements coverage

---

## Notes

- Keep this file updated with progress after completing each task
- Each phase should leave the repo in a testable and functional state
- Run pre-commit validation after each phase completion
- ✅ Verification complete (6 iterations total)
- ✅ Requirements coverage: 95.2% (20/21)
- ✅ All user decisions integrated
- ✅ Ready to begin implementation

---

## Next Steps

**Implementation can now begin following this TODO plan.**

The workflow will be:
1. Create code changes documentation file (`updates/reserve_assessment_code_changes.md`)
2. Implement Phase 1 (Historical Data Infrastructure)
3. Implement Phase 2 (Reserve Assessment Mode Core)
4. Implement Phase 3 (Integration with Main Menu)
5. Implement Phase 4 (Testing - run after each phase)
6. Implement Phase 5 (Documentation)
7. Implement Phase 6 (Final Validation)
8. Move files to `updates/done/` when complete

**Remember**: Run `python tests/run_all_tests.py` after each phase (100% pass rate required)
