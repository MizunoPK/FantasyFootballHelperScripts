# Team Data Architecture Refactor - TODO

## Objective
Replace centralized teams.csv with per-team historical data files and on-the-fly ranking calculations.

---

## Progress Tracking
- [x] Phase 1: Create new data structure
- [x] Phase 2: Update league_helper
- [x] Phase 3: Update simulation
- [x] Phase 4: Cleanup and testing

**Status**: COMPLETED (2025-11-20)

**Final Notes**:
- Simulation updated to use **16 weeks** instead of 17 due to incomplete week 17 source data
- Column names updated to `pts_allowed_to_{POS}` format for clarity
- All 1987 tests pass (100%)
- Documentation updated with notes about new team_data folder format
- data/teams.csv removed

---

## Phase 1: Create New Data Structure

### 1.1 Define new team CSV format
- [ ] Create data/team_data/ folder
- [ ] Define CSV format: week,QB,RB,WR,TE,K,points_scored,points_allowed
- [ ] Weeks 1-17 as rows, values for completed weeks only

### 1.2 Update player-data-fetcher/config.py
- [ ] Remove TEAMS_CSV constant (line 40)
- [ ] Remove MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS constant (line 43)
- [ ] Add TEAM_DATA_FOLDER constant pointing to data/team_data/

### 1.3 Update player-data-fetcher/espn_client.py
- [ ] Modify _calculate_rolling_window_rankings() to output per-team weekly data
- [ ] Modify _calculate_position_defense_rankings() to output per-team weekly data
- [ ] Return data structure suitable for new format (dict of teams -> list of week data)

### 1.4 Update player-data-fetcher/player_data_exporter.py
- [ ] Remove export_teams_csv() (lines 452-492)
- [ ] Remove export_teams_to_data() (lines 494-525)
- [ ] Add new export_team_data() method for team_data folder
- [ ] Create 32 individual team CSV files

### 1.5 Update player-data-fetcher/player_data_fetcher_main.py
- [ ] Update save_to_historical_data() (lines 362-419)
- [ ] Remove teams.csv from files_to_copy
- [ ] Add logic to copy team_data folder to historical data

### 1.6 Update utils/TeamData.py
- [ ] Keep TeamData dataclass
- [ ] Remove load_teams_from_csv()
- [ ] Remove extract_teams_from_rankings()
- [ ] Remove save_teams_to_csv()
- [ ] Add new functions for reading/writing team_data format

### 1.7 Run pre-commit validation
- [ ] Run `python tests/run_all_tests.py`
- [ ] Fix any failing tests
- [ ] Commit Phase 1 changes

---

## Phase 2: Update League Helper

### 2.1 Update data/league_config.json
- [ ] Add "MIN_WEEKS": 5 to TEAM_QUALITY_SCORING
- [ ] Add "MIN_WEEKS": 5 to MATCHUP_SCORING
- [ ] Add "MIN_WEEKS": 5 to SCHEDULE_SCORING

### 2.2 Update league_helper/util/ConfigManager.py
- [ ] Add get_team_quality_min_weeks() method returning self.team_quality_scoring.get('MIN_WEEKS', 5)
- [ ] Add get_matchup_min_weeks() method returning self.matchup_scoring.get('MIN_WEEKS', 5)
- [ ] Add get_schedule_min_weeks() method returning self.schedule_scoring.get('MIN_WEEKS', 5)
- [ ] Pattern: Similar to existing get_X_multiplier() methods

### 2.3 Refactor league_helper/util/TeamDataManager.py (major refactor)
- [ ] Update __init__ signature: add `config_manager: ConfigManager` parameter (BREAKING CHANGE)
  - [ ] New: `def __init__(self, data_folder, config_manager, season_schedule_manager, current_nfl_week)`
- [ ] Load all team CSV files from data/team_data/*.csv
- [ ] Store complete historical data: `team_weekly_data: Dict[str, List[Dict]]` (team -> weeks -> data)
- [ ] Implement ranking calculation methods:
  - [ ] `_calculate_rankings()` - called during init
  - [ ] Get MIN_WEEKS from config_manager.get_team_quality_min_weeks() for offensive/defensive ranks
  - [ ] Get MIN_WEEKS from config_manager.get_matchup_min_weeks() for position-specific ranks
  - [ ] Handle early season: return 16 (neutral) when weeks < MIN_WEEKS
- [ ] Calculate offensive rank: sum points_scored / games over past MIN_WEEKS weeks, rank 1-32
- [ ] Calculate defensive rank: sum points_allowed / games over past MIN_WEEKS weeks, rank 1-32
- [ ] Calculate position ranks: sum position points / games over past MIN_WEEKS weeks, rank 1-32
- [ ] Cache rankings: `offensive_ranks: Dict[str, int]`, `defensive_ranks: Dict[str, int]`, `position_ranks: Dict[str, Dict[str, int]]`
- [ ] Update get_team_offensive_rank() to return from cache
- [ ] Update get_team_defensive_rank() to return from cache
- [ ] Update get_team_defense_vs_position_rank() to return from cache
- [ ] Update reload_team_data() to reload CSVs and recalculate rankings
- [ ] Add set_current_week(week_num) method for simulation to update rankings per week
  - [ ] Updates self.current_nfl_week
  - [ ] Calls _calculate_rankings() to recalculate based on new week

### 2.4 Update league_helper/util/PlayerManager.py
- [ ] Update lines 218-219 to use new TeamDataManager methods
- [ ] Ensure proper initialization order with ConfigManager

### 2.5 Update league_helper/LeagueHelperManager.py
- [ ] Update line 83 to pass config to TeamDataManager:
  - [ ] Old: `TeamDataManager(data_folder, self.season_schedule_manager, self.config.current_nfl_week)`
  - [ ] New: `TeamDataManager(data_folder, self.config, self.season_schedule_manager, self.config.current_nfl_week)`

### 2.6 Run pre-commit validation
- [ ] Run `python tests/run_all_tests.py`
- [ ] Fix any failing tests
- [ ] Commit Phase 2 changes

---

## Phase 3: Update Simulation

### 3.1 Create standalone team_data generation script
- [ ] Create `simulation/generate_team_data.py` as standalone script
- [ ] Load players_actual.csv (columns: team, position, week_1_points...week_17_points)
- [ ] Load season_schedule.csv (columns: week, team, opponent)
- [ ] For each NFL team (32 teams):
  - [ ] Create team CSV file (e.g., sim_data/team_data/KC.csv)
  - [ ] For each week (1-17):
    - [ ] Look up opponent from season_schedule.csv
    - [ ] Find all players on opponent's team in players_actual
    - [ ] Sum fantasy points by position (QB, RB, WR, TE, K) - this is points allowed
    - [ ] Sum team's own points_scored from their players
    - [ ] Track points_allowed from opponent's players vs this defense
  - [ ] Write CSV: week,QB,RB,WR,TE,K,points_scored,points_allowed
- [ ] Generate all 32 team CSV files in sim_data/team_data/
- [ ] Handle bye weeks (0 values for that week)
- [ ] Add main() for command-line execution

### 3.2 Update simulation/ConfigGenerator.py
- [ ] Add PARAM_DEFINITIONS entries:
  - [ ] 'TEAM_QUALITY_MIN_WEEKS': (3, 6)
  - [ ] 'MATCHUP_MIN_WEEKS': (3, 6)
  - [ ] (SCHEDULE_MIN_WEEKS stays disabled per user decision)
- [ ] Add to PARAMETER_ORDER list (after respective WEIGHT entries)
- [ ] Update generate_multiplier_parameter_values() to handle MIN_WEEKS
- [ ] Update build_config_from_combination() to set MIN_WEEKS in scoring sections

### 3.3 Update simulation/SimulatedLeague.py
- [ ] Update line 186 to pass config to TeamDataManager:
  - [ ] Old: `TeamDataManager(team_dir, season_schedule_mgr, config.current_nfl_week)`
  - [ ] New: `TeamDataManager(team_dir, config, season_schedule_mgr, config.current_nfl_week)`
- [ ] Remove line 185 that copies teams_week_1.csv
- [ ] Update _initialize_teams() to copy team_data folder to each team_dir
- [ ] Simplify _update_team_rankings() (lines 306-327):
  - [ ] Instead of copying files, call team_data_mgr.set_current_week(week_num) for each team
  - [ ] This recalculates rankings based on new week using MIN_WEEKS rolling window

### 3.4 Remove old simulation team data
- [ ] Delete simulation/sim_data/teams_week_1.csv through teams_week_18.csv
- [ ] Verify sim_data/team_data/ folder is properly created

### 3.5 Run pre-commit validation
- [ ] Run `python tests/run_all_tests.py`
- [ ] Fix any failing tests
- [ ] Commit Phase 3 changes

---

## Phase 4: Cleanup and Testing

### 4.1 Remove all teams.csv references
- [ ] Remove data/teams.csv file
- [ ] Remove player-data-fetcher/data/teams_*.csv files
- [ ] Search codebase for any remaining teams.csv references
- [ ] Clean up any orphaned imports or constants

### 4.2 Update all unit tests
- [ ] tests/utils/test_TeamData.py - Update for new format
- [ ] tests/league_helper/util/test_TeamDataManager.py - **MAJOR UPDATES (18+ call sites)**
  - [ ] Update all TeamDataManager() calls to include ConfigManager parameter
  - [ ] Create mock ConfigManager fixture with MIN_WEEKS methods
  - [ ] Update test data to use new team_data folder format
- [ ] tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py - 5 call sites
- [ ] tests/league_helper/util/test_PlayerManager_scoring.py - 1 call site
- [ ] tests/player-data-fetcher/test_config.py - Remove old constant tests
- [ ] All tests referencing teams.csv (search found 47 files total)

### 4.3 Update integration tests
- [ ] tests/integration/test_league_helper_integration.py
- [ ] tests/integration/test_data_fetcher_integration.py
- [ ] tests/integration/test_simulation_integration.py

### 4.4 Update documentation
- [ ] docs/scoring/04_team_quality_multiplier.md
- [ ] docs/scoring/06_matchup_multiplier.md
- [ ] docs/scoring/07_schedule_multiplier.md
- [ ] README.md
- [ ] ARCHITECTURE.md
- [ ] CLAUDE.md
- [ ] simulation/README.md (if exists)

### 4.5 Final validation
- [ ] Run complete test suite: `python tests/run_all_tests.py`
- [ ] Ensure 100% test pass rate
- [ ] Manual testing of league_helper modes
- [ ] Manual testing of simulation system
- [ ] Commit Phase 4 changes

---

## Files to Modify Summary

### Player Data Fetcher
- player-data-fetcher/config.py
- player-data-fetcher/espn_client.py
- player-data-fetcher/player_data_exporter.py
- player-data-fetcher/player_data_fetcher_main.py

### League Helper
- data/league_config.json
- league_helper/util/TeamDataManager.py
- league_helper/util/PlayerManager.py
- league_helper/util/ConfigManager.py
- league_helper/LeagueHelperManager.py

### Simulation
- simulation/SimulationManager.py (or new script)
- simulation/ConfigGenerator.py
- simulation/SimulatedLeague.py
- simulation/sim_data/

### Utils
- utils/TeamData.py

### Data Files
- Create: data/team_data/
- Remove: data/teams.csv
- Remove: player-data-fetcher/data/teams_*.csv
- Remove: simulation/sim_data/teams_week_*.csv

---

## Verification Summary (First Round - 5 Iterations Complete)

### Iterations Completed: 5 (including skeptical re-verification)

### Requirements Added After Initial Draft:
- **47 files reference teams.csv** (significantly more than initially estimated)
- ConfigManager already has ConfigKeys.MIN_WEEKS defined (line 79)
- TeamDataManager currently doesn't receive ConfigManager - signature change needed
- LeagueHelperManager.py line 83 creates TeamDataManager without ConfigManager
- SCHEDULE_SCORING is currently disabled in ConfigGenerator.py

### Key Codebase Patterns Identified:
- ConfigManager multiplier pattern: `get_X_multiplier()` returns `Tuple[float, str]`
- TeamDataManager uses `team_data_cache: Dict[str, TeamData]` structure
- SimulatedLeague copies files to temp team directories per team
- season_schedule.csv format: `week,team,opponent`

### Critical Dependencies/Ordering:
1. TeamDataManager needs ConfigManager passed in (signature change)
2. LeagueHelperManager creates ConfigManager before TeamDataManager (can pass it)
3. SimulatedLeague creates ConfigManager line 174, TeamDataManager line 186 (can pass it)

### Risk Areas Identified:
- **47 files need teams.csv cleanup** - higher effort than estimated
- TeamDataManager signature change affects all call sites
- Simulation data generation is complex (needs opponent lookup + fantasy point aggregation)
- Early-season handling when MIN_WEEKS data isn't available yet

### Questions Identified for User Clarification:
1. Same or separate MIN_WEEKS values across scoring sections?
2. Simulation data generation - standalone script or integrated?
3. TeamDataManager backwards compatibility for tests?
4. Early-season handling when insufficient historical data exists?

### Skeptical Re-Verification Results (Iteration 5):
**Verified as Correct:**
- config.py lines 40, 43 for TEAMS_CSV and MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS
- TeamDataManager line numbers and method signatures
- SimulatedLeague lines 185, 306-327 for teams_week handling
- player_data_exporter.py lines 452, 494 for export methods
- player_data_fetcher_main.py line 400 for files_to_copy

**Corrected:**
- Expanded teams.csv file count from ~12 files to 47 files
- Added LeagueHelperManager initialization details (line 83)
- Noted SCHEDULE_SCORING is disabled in ConfigGenerator

**Confidence Level: HIGH** - All major claims verified with code evidence

---

## Second Verification Round Summary (7 More Iterations Complete)

### Iterations Completed: 12 total (5 + 7)

### Key Updates Based on User Answers:
- Separate MIN_WEEKS for each scoring section (independent optimization)
- Standalone script simulation/generate_team_data.py for data generation
- Breaking change to TeamDataManager signature (no backwards compatibility)
- 17 weeks for team data (fantasy regular season)

### Critical Findings from Skeptical Re-Verification (Iteration 10):
- **24+ TeamDataManager call sites** found (more than initially estimated):
  - Production: 2 (LeagueHelperManager, SimulatedLeague)
  - Tests: 22+ (test_TeamDataManager, test_manual_trade_visualizer, test_PlayerManager_scoring)
- Added set_current_week() method requirement for simulation weekly updates

### Implementation Details Refined:
- ConfigGenerator needs 'TEAM_QUALITY_MIN_WEEKS' and 'MATCHUP_MIN_WEEKS' parameters
- generate_team_data.py uses season_schedule.csv for opponent lookups
- Team CSV format: week,QB,RB,WR,TE,K,points_scored,points_allowed

### Risk Assessment:
- **High effort**: 24+ call sites to update for TeamDataManager signature change
- **Medium effort**: generate_team_data.py script (complex opponent/position aggregation)
- **Low risk**: ConfigManager changes (follow existing patterns)

### Confidence Level: HIGH
All user decisions integrated, call sites verified, implementation approach validated.

---

## User Decision Summary (From Questions)

1. **MIN_WEEKS**: Separate values for each scoring section (TEAM_QUALITY, MATCHUP, SCHEDULE)
2. **Simulation data script**: Standalone script `simulation/generate_team_data.py`
3. **TeamDataManager signature**: Breaking change - update all call sites
4. **Early season handling**: Return neutral ranks (16) when insufficient data
5. **SCHEDULE_SCORING**: Keep disabled in ConfigGenerator
6. **Week range**: 17 weeks (1-17)

---

## Notes
- NO backwards compatibility with teams.csv
- Default MIN_WEEKS value: 5 (matches current behavior)
- Simulation MIN_WEEKS range: (3, 6)
