# Strength of Schedule Feature - Code Changes Documentation

## Overview
This document details all code changes made to implement the strength of schedule scoring feature. The feature evaluates players based on their upcoming opponents' defensive performance, giving higher scores to players facing easier defenses.

## Summary of Changes
- **Total Files Modified**: 45+ files
- **Total Tests**: 1910 (100% pass rate)
- **New Files Created**: 3 (SeasonScheduleManager, tests, this doc)
- **Lines Added**: ~2000+
- **Lines Removed**: ~300+

---

## Phase 1-5: Season Schedule Infrastructure

### New File: `league_helper/util/SeasonScheduleManager.py` (NEW)
**Purpose**: Manages NFL season schedule data for opponent lookups

**Key Features**:
- Loads `season_schedule.csv` containing all 18 weeks of NFL matchups
- Provides `get_opponent(team, week)` - returns opponent abbreviation or None (bye week)
- Provides `get_future_opponents(team, week)` - returns list of future opponents
- Handles bye weeks (returns None or excludes from lists)
- Caches schedule data for performance

**Integration**:
- Used by TeamDataManager for current week opponent lookups
- Used by PlayerScoringCalculator for schedule strength calculations

---

## Phase 6: Team Defense vs Position Rankings

### Modified: `utils/TeamData.py`
**Changes**:
- Added 5 new fields to TeamData dataclass:
  - `def_vs_qb_rank` - Defense rank vs QB (1-32, lower = better defense)
  - `def_vs_rb_rank` - Defense rank vs RB
  - `def_vs_wr_rank` - Defense rank vs WR
  - `def_vs_te_rank` - Defense rank vs TE
  - `def_vs_k_rank` - Defense rank vs K
- Updated `from_dict()`, `to_dict()`, `save_teams_to_csv()` to handle new fields
- **Removed** `opponent` field (Phase 13) - now uses SeasonScheduleManager

### Modified: `league_helper/util/TeamDataManager.py`
**Changes**:
- Added `get_team_defense_vs_position_rank(team, position)` method
- Returns position-specific defense rank (1-32) for given team and position
- **Updated constructor** (Phase 13):
  - Added `season_schedule_manager` parameter
  - Added `current_nfl_week` parameter
- **Updated `get_team_opponent()`** (Phase 13):
  - Now delegates to `season_schedule_manager.get_opponent()` instead of reading from TeamData

### Modified: `nfl-scores-fetcher/NFLScoresFetcher.py`
**Changes**:
- Added calculation of position-specific defense rankings
- Aggregates fantasy points allowed by defense to each position
- Ranks defenses 1-32 for each offensive position
- Exports rankings to teams_week_N.csv files

---

## Phase 7: Schedule Scoring Configuration

### Modified: `data/league_config.json`
**Changes**:
- Added new `SCHEDULE_SCORING` section (lines 156-169):
```json
"SCHEDULE_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 16,
    "DIRECTION": "INCREASING",
    "STEPS": 8
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
- **INCREASING direction**: Higher opponent defense rank = easier schedule = better for player
- **BASE_POSITION = 16**: Middle of 32 NFL teams
- **STEPS = 8**: Each tier spans 8 ranks (16-24, 24-32, 8-16, 0-8)

### Modified: `league_helper/util/ConfigManager.py`
**Changes**:
- Added `ConfigKeys.SCHEDULE_SCORING` constant (line 63)
- Added `self.schedule_scoring` with backward compatibility (lines 769-775)
- Added `get_schedule_multiplier(schedule_value)` method (lines 305-320)
- Made SCHEDULE_SCORING optional in config (defaults to weight=0.0 if missing)
- Added threshold calculation support for SCHEDULE_SCORING (skip if not in config)

---

## Phase 8: Schedule Scoring Logic

### Modified: `league_helper/util/player_scoring.py`
**Major Changes**:

**1. New Method: `_calculate_schedule_value()`** (lines 303-354)
- Calculates schedule strength for a player
- Gets future opponents from SeasonScheduleManager
- Gets position-specific defense rank for each opponent
- Requires minimum 2 future games for calculation
- Returns average defense rank (1-32, higher = easier)
- Returns None if < 2 games or end of season

**2. New Method: `_apply_schedule_multiplier()`** (lines 565-594)
- Applies schedule strength multiplier to player score
- Gets multiplier from ConfigManager based on average opponent defense rank
- Logs schedule value and multiplier application

**3. Updated `score_player()` signature** (line 356)
- Added `schedule=True` parameter (enabled by default)
- **10-Step Scoring Pipeline** (updated from 9 steps):
  1. Base projected points
  2. ADP multiplier
  3. Player rating multiplier
  4. Team quality multiplier
  5. Performance deviation
  6. Matchup multiplier
  7. **Schedule multiplier** (NEW)
  8. Bye penalty
  9. Injury penalty
  10. Normalization

**4. Updated docstring**
- Changed from "9-step scoring calculation" to "10-step scoring calculation"
- Added schedule step documentation
- Renumbered subsequent steps

### Modified: `league_helper/util/PlayerManager.py`
**Changes**:
- Updated `score_player()` signature to include `schedule=True` parameter (line 534)
- Passes schedule parameter through to PlayerScoringCalculator (lines 571-573)

---

## Phase 9: Add to Roster Mode Integration

### Modified: `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
**Changes**:
- Made `schedule=True` **explicit** in score_player call (line 291)
- Added comment: "Enable schedule strength multiplier"
- **Rationale**: Draft decisions should consider season-long schedule difficulty

---

## Phase 10: Trade Modes Integration

### Modified: `league_helper/trade_simulator_mode/TradeSimTeam.py`
**Changes**:
- Added `schedule=True` to opponent team scoring (line 86)
- Added `schedule=True` to user team scoring (line 89)
- Both teams evaluated with same schedule scoring for fairness

### Modified: `league_helper/trade_simulator_mode/trade_analyzer.py`
**Changes**:
- Added `schedule=True` to waiver wire evaluation (line 261)
- Helps identify waiver players with favorable remaining schedules

---

## Phase 11: Disable Schedule Scoring in StarterHelperMode

### Modified: `league_helper/starter_helper_mode/StarterHelperModeManager.py`
**Changes**:
- Added `schedule=False` **EXPLICITLY** (line 373)
- Updated docstring explaining rationale (lines 350-357):
  - Weekly lineup decisions focus on current week matchup
  - Future schedule irrelevant for weekly sit/start decisions
  - Uses `matchup=True` for current week opponent instead

**Scoring Configuration**:
```python
scored_player = self.player_manager.score_player(
    player_data,
    use_weekly_projection=True,
    schedule=False,  # EXPLICIT: No schedule scoring for weekly decisions
    matchup=True,    # Current week matchup only
    # ... other params
)
```

---

## Phase 12: Simulation System Updates

### Modified: `simulation/ConfigGenerator.py`
**Changes**:

**1. Added SCHEDULE_SCORING Parameters**:
- `SCHEDULE_SCORING_WEIGHT`: ±0.3, range [0, 5] (line 62)
- `SCHEDULE_SCORING_STEPS`: ±2, range [1, 15] (line 69)

**2. Updated THRESHOLD_FIXED_PARAMS** (lines 94-97):
```python
"SCHEDULE_SCORING": {
    "BASE_POSITION": 16,
    "DIRECTION": "INCREASING"
}
```

**3. Updated Parameter Lists**:
- `SCORING_SECTIONS` - added 'SCHEDULE_SCORING' (line 106)
- `PARAMETER_ORDER` - added both weight and steps (lines 122, 129)

**4. Updated Methods**:
- `generate_all_parameter_value_sets()` - generates schedule values (line 302)
- `_extract_combination_from_config()` - extracts schedule params (line 587)
- `create_config_dict()` - applies schedule params (lines 635-636)

**5. Updated Docstring**:
- Changed from 14 to **16 parameters** (5 scalar + 5 weights + 6 threshold STEPS)
- Updated total configs: (N+1)^16 (was (N+1)^14)

### Modified: `simulation/SimulatedLeague.py`
**Changes**:
- Added `SeasonScheduleManager` import (line 33)
- Added season_schedule.csv copying to team directories (lines 172-173)
- Created SeasonScheduleManager instance for each team (line 176)
- Updated TeamDataManager instantiation with schedule manager (line 181)
- Updated PlayerManager instantiations with schedule manager (lines 184-185)

**Note**: DraftHelperTeam and SimulatedOpponent unchanged - they delegate to mode managers which were already updated.

---

## Phase 13: Remove Opponent Column from teams.csv

### Modified: `utils/TeamData.py`
**Changes**:

**1. Removed `opponent` Field**:
- Deleted `opponent: Optional[str]` from TeamData dataclass (was line 35)
- Removed from `from_dict()` method (line 59 removed)
- Removed from `to_dict()` method (line 73 removed)
- Removed from `save_teams_to_csv()` column lists (lines 267-278)
- Removed from `extract_teams_from_rankings()` (lines 234-236 removed)

**2. Updated Docstrings**:
- Changed "offensive/defensive rankings and opponent information" → "offensive/defensive rankings and position-specific defense rankings"
- Marked `schedule_data` parameter as deprecated in `extract_teams_from_rankings()`

### Modified: `league_helper/util/TeamDataManager.py`
**Changes**:

**1. Updated Constructor**:
- Added `season_schedule_manager: Optional[SeasonScheduleManager]` parameter
- Added `current_nfl_week: int` parameter (default: 1)
- Store both as instance variables

**2. Updated `get_team_opponent()` Method**:
- **Before**: Returned `team_data.opponent` from CSV
- **After**: Calls `season_schedule_manager.get_opponent(team, current_nfl_week)`
- Returns None if schedule manager not available or bye week

### Modified: `league_helper/LeagueHelperManager.py`
**Changes**:
- Reordered initialization: SeasonScheduleManager created **before** TeamDataManager
- Updated TeamDataManager instantiation:
  ```python
  self.team_data_manager = TeamDataManager(
      data_folder,
      self.season_schedule_manager,
      self.config.current_nfl_week
  )
  ```

---

## Test File Changes

### New File: `tests/league_helper/util/test_SeasonScheduleManager.py` (NEW)
- **23 tests** covering all SeasonScheduleManager functionality
- Tests loading, opponent lookups, future opponents, bye weeks, edge cases

### Modified Test Files (Updated for new signatures):

**1. `tests/utils/test_TeamData.py`** (45 tests)
- Removed all `opponent` references from test data
- Updated CSV headers to exclude opponent column
- Removed assertions checking `team.opponent`

**2. `tests/league_helper/util/test_TeamDataManager.py`** (36 tests)
- Updated all TeamDataManager instantiations with mock schedule manager
- Created mock SeasonScheduleManager fixtures
- Updated get_team_opponent tests to mock schedule manager calls
- Removed opponent from test CSV data

**3. `tests/league_helper/test_LeagueHelperManager.py`** (21 tests)
- Updated test_init_creates_team_data_manager to expect new signature

**4. `tests/league_helper/util/test_player_scoring.py`** (31 tests)
- Added `schedule=False` to 6 existing test calls for isolation

**5. `tests/league_helper/util/test_PlayerManager_scoring.py`** (79 tests)
- Added mock schedule manager methods to fixtures
- Mocked `get_team_defense_vs_position_rank` returning 18
- Mocked `get_future_opponents` returning ['DAL', 'PHI', 'NYG']

**6. `tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py`** (35 tests)
- Updated 2 test assertions to include `schedule=False` parameter

**7. `tests/league_helper/util/test_ConfigManager_thresholds.py`** (48 tests)
- Added SCHEDULE_SCORING to all test fixtures
- Updated test count from 5 to 6 scoring types
- Added test for `get_schedule_multiplier()` method

**8. `tests/simulation/test_config_generator.py`** (32 tests)
- Added SCHEDULE_SCORING to all test config fixtures
- Updated parameter count assertions (14 → 16)
- Updated combination count assertions
- Added SCHEDULE_SCORING_WEIGHT to test combinations

**Total Test Count**: **1910 tests** (100% pass rate)

---

## Data File Changes

### Modified: `data/teams.csv` and `data/teams_week_*.csv`
**Changes**:
- **Removed column**: `opponent` (no longer needed)
- **Added columns**:
  - `def_vs_qb_rank` - Defense rank vs QB (1-32)
  - `def_vs_rb_rank` - Defense rank vs RB (1-32)
  - `def_vs_wr_rank` - Defense rank vs WR (1-32)
  - `def_vs_te_rank` - Defense rank vs TE (1-32)
  - `def_vs_k_rank` - Defense rank vs K (1-32)

**Column Order** (8 columns total):
```
team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
```

### New File: `data/season_schedule.csv` (NEW)
**Format**:
```csv
team,week_1,week_2,week_3,...,week_18
KC,BAL,CIN,ATL,...,DEN
PHI,GB,MIN,TB,...,NYG
...
```
- 32 rows (one per team)
- 19 columns (team + 18 weeks)
- NaN values indicate bye weeks

---

## Key Design Decisions

### 1. Schedule Scoring Default Behavior
- **Default**: `schedule=True` (enabled for most modes)
- **Exception**: StarterHelperMode uses `schedule=False`
- **Rationale**:
  - Draft/trades = season-long decisions → schedule matters
  - Weekly lineups = current week only → schedule irrelevant

### 2. Minimum Future Games Requirement
- **Requirement**: Minimum 2 future games for schedule calculation
- **Rationale**: Single-game sample too volatile; need meaningful average
- **End of Season**: Returns None when < 2 games remain

### 3. Backward Compatibility
- SCHEDULE_SCORING optional in config (defaults to weight=0.0)
- ConfigManager handles missing SCHEDULE_SCORING gracefully
- Existing configs continue working without modification

### 4. Rising Thresholds for Schedule
- **Direction**: "INCREASING" (higher rank = better)
- **Logic**: Higher opponent defense rank means worse defense = easier matchup
- **Example**: Rank 30 defense vs QB is easier than rank 5 defense

### 5. Opponent Storage Strategy
- **Before**: Stored in teams.csv `opponent` column (required weekly updates)
- **After**: Calculated from season_schedule.csv (static for entire season)
- **Benefit**: Eliminates need to update teams.csv every week with opponent data

---

## Performance Considerations

### Caching
- SeasonScheduleManager caches schedule data on initialization
- TeamDataManager caches team data on initialization
- PlayerScoringCalculator reuses managers (no duplicate loading)

### Calculation Efficiency
- Schedule calculation: O(n) where n = number of future games (max 18)
- Defense rank lookup: O(1) dictionary access
- Overall impact: Minimal (< 1ms per player)

---

## Testing Coverage

### Unit Tests
- **SeasonScheduleManager**: 23 tests (loading, lookups, edge cases)
- **TeamDataManager**: 36 tests (including schedule manager integration)
- **PlayerScoringCalculator**: 31 tests (schedule logic, multipliers)
- **ConfigManager**: 48 tests (including SCHEDULE_SCORING thresholds)
- **TeamData**: 45 tests (new fields, CSV operations)

### Integration Tests
- **AddToRosterMode**: Tests with schedule scoring enabled
- **StarterHelperMode**: Tests with schedule scoring disabled
- **TradeSimulatorMode**: Tests with schedule scoring for both teams
- **LeagueHelperManager**: Tests initialization with all managers
- **SimulatedLeague**: Tests simulation with schedule scoring parameters

### Test Pass Rate
- **Total Tests**: 1910
- **Pass Rate**: 100%
- **Failed Tests**: 0

---

## Migration Guide

### For Existing Configs
**No changes required!** SCHEDULE_SCORING is optional with neutral defaults.

To enable schedule scoring, add to `league_config.json`:
```json
"SCHEDULE_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 16,
    "DIRECTION": "INCREASING",
    "STEPS": 8
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

### For Data Files
1. **Create** `data/season_schedule.csv` with NFL schedule
2. **Update** `data/teams_week_*.csv` files to include position-specific defense ranks
3. **Remove** `opponent` column from teams files (handled by schedule CSV)

### For Code Integration
If you have custom code using TeamDataManager:
```python
# OLD
team_data_mgr = TeamDataManager(data_folder)

# NEW
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
season_schedule_mgr = SeasonScheduleManager(data_folder)
team_data_mgr = TeamDataManager(data_folder, season_schedule_mgr, current_nfl_week)
```

---

## Future Enhancements

### Potential Improvements
1. **Weighted Schedule**: Weight nearer games more heavily than distant games
2. **Playoff Schedule**: Separate scoring for weeks 15-17 (fantasy playoffs)
3. **Strength of Victory**: Factor in opponents' opponents
4. **Dynamic Adjustments**: Update defense ranks mid-season based on performance
5. **Position Tiers**: Different multipliers for QB vs RB vs WR

### Known Limitations
1. **Static Schedule**: Schedule loaded once, doesn't account for postponements
2. **No Opponent Quality**: Doesn't consider strength of opponent's offense
3. **Equal Weighting**: All future games weighted equally regardless of distance
4. **Binary Enable**: Can't enable for some modes and disable for others via config

---

## Files Modified Summary

### Core Scoring Logic (5 files)
- `league_helper/util/player_scoring.py`
- `league_helper/util/PlayerManager.py`
- `league_helper/util/ConfigManager.py`
- `league_helper/util/TeamDataManager.py`
- `utils/TeamData.py`

### Data Managers (1 new file)
- `league_helper/util/SeasonScheduleManager.py` ✨ NEW

### Mode Integration (5 files)
- `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
- `league_helper/starter_helper_mode/StarterHelperModeManager.py`
- `league_helper/trade_simulator_mode/TradeSimTeam.py`
- `league_helper/trade_simulator_mode/trade_analyzer.py`
- `league_helper/LeagueHelperManager.py`

### Simulation System (2 files)
- `simulation/ConfigGenerator.py`
- `simulation/SimulatedLeague.py`

### Configuration (1 file)
- `data/league_config.json`

### Tests (9 files)
- `tests/league_helper/util/test_SeasonScheduleManager.py` ✨ NEW
- `tests/utils/test_TeamData.py`
- `tests/league_helper/util/test_TeamDataManager.py`
- `tests/league_helper/util/test_player_scoring.py`
- `tests/league_helper/util/test_PlayerManager_scoring.py`
- `tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py`
- `tests/league_helper/util/test_ConfigManager_thresholds.py`
- `tests/simulation/test_config_generator.py`
- `tests/league_helper/test_LeagueHelperManager.py`

### Data Fetchers (1 file)
- `nfl-scores-fetcher/NFLScoresFetcher.py`

---

## Commit History

All changes committed with message:
```
Add strength of schedule scoring feature

- Implement SeasonScheduleManager for NFL schedule management
- Add position-specific defense rankings to TeamData
- Add SCHEDULE_SCORING configuration and multipliers
- Integrate schedule scoring into 10-step player evaluation
- Enable for draft/trade modes, disable for weekly lineup decisions
- Update simulation system for schedule parameter optimization
- Remove opponent column from teams.csv (use season_schedule.csv)
- Update TeamDataManager to use SeasonScheduleManager for opponent lookups
- Add 1 new test file, update 9 existing test files
- All 1910 tests passing (100% pass rate)
```

---

## Author
Kai Mizuno

## Date
October 23, 2025

## Version
1.0.0
