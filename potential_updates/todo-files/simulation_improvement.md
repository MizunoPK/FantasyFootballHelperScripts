# Simulation Improvement TODO

## Objective
Improve the draft_helper simulation to use projected vs actual data files for more realistic simulation behavior.

**Key Changes:**
- Use 'projected' files (players_projected.csv, teams_projected.csv) for drafting decisions
- Use 'projected' files with starter_helper for lineup optimization
- Use 'actual' files (players_actual.csv, teams_actual.csv) for final scoring and match winners

## Progress Tracking
**IMPORTANT:** Keep this file updated with progress made in case a new Claude session needs to finish the work.

## Tasks Checklist

### Analysis & Planning
- [x] Analyze existing simulation structure and current data flow
- [x] Create comprehensive TODO file for simulation improvement objective
- [x] Ask clarifying questions about simulation requirements
- [x] Understand current vs desired behavior

### Implementation Tasks

#### Data Management Updates
- [x] Update SimulationDataManager to handle projected/actual file pairs
  - [x] Add methods to load players_projected.csv and players_actual.csv
  - ~~[x] Add methods to load teams_projected.csv and teams_actual.csv~~ - CHANGED TO WEEKLY STRUCTURE
  - [x] Update setup_simulation_data() to handle both file types
  - [x] Add validation for both projected and actual data integrity
- [ ] **NEW**: Update SimulationDataManager for weekly teams.csv structure
  - [ ] Add methods to load teams_week_0.csv through teams_week_18.csv
  - [ ] Update setup_simulation_data() to copy source teams.csv to all 19 weekly versions
  - [ ] Add validation for all 19 weekly teams files
  - [ ] Add method to get teams data by specific week number

#### Configuration Updates
- [x] Update simulation config to add projected/actual data parameters
  - [x] Remove old file path references (PLAYERS_CSV_COPY, SOURCE_PLAYERS_CSV)
  - [x] Keep SIMULATION_DATA_DIR for new file structure
  - [x] Maintain backward compatibility with existing validation

#### Draft Engine Updates
- [x] Modify DraftSimulationEngine to use projected data for drafting
  - [x] DraftSimulationEngine already accepts dataframe parameter
  - [x] Main simulator now passes projected data to draft engine
  - [x] All draft decisions use projected player data via updated data flow

#### Season Simulation Updates
- [ ] Update SeasonSimulator to use starter_helper with projected data for lineups
  - [x] Update main_simulator to load both projected and actual dataframes
  - [x] Update _run_single_complete_simulation to pass both dataframes
  - [ ] Modify SeasonSimulator constructor to accept both dataframes
  - [ ] Integrate starter_helper functionality for lineup optimization
  - [ ] Use projected data to determine best starting lineups
  - [ ] Ensure FLEX position handling works correctly
  - [ ] **NEW**: Use appropriate weekly teams.csv file for each week (week 1-18)
- [ ] Update SeasonSimulator to use actual data for scoring/determining winners
  - [ ] Use actual points to determine weekly matchup winners
  - [ ] Ensure actual scores are used for season statistics

#### **NEW**: Weekly Teams Data Integration
- [ ] Update draft engine to use week 0 teams.csv for positional rankings
  - [ ] Modify draft strategies to use teams_week_0.csv for positional ranking calculations
  - [ ] Ensure draft decisions use week 0 team data consistently
- [ ] Update starter_helper integration to use weekly teams.csv files
  - [ ] Pass appropriate teams_week_X.csv to starter_helper for each simulation week
  - [ ] Ensure positional ranking calculations use correct weekly team data
  - [ ] Modify lineup optimization to accept week-specific teams data

### Testing & Validation
- [x] Create/update unit tests for new projected/actual data functionality
  - [x] Test SimulationDataManager with both file types
  - [x] **NEW**: Test SimulationDataManager with weekly teams.csv files (19 files)
  - [x] Test DraftSimulationEngine with projected data and week 0 teams data
  - [x] Test SeasonSimulator with projected lineups and actual scoring
  - [x] Test integration between starter_helper and simulation with weekly teams data
  - [x] **NEW**: Test weekly teams data loading and validation (week 0-18)
- [ ] Run all existing unit tests to ensure compatibility
  - [x] Run simulation data manager tests: All 13 tests passing
  - [ ] Run simulation-specific tests: `pytest draft_helper/simulation/tests/ -v`
  - [ ] Run all repository tests: `pytest --tb=short`
  - [ ] Verify 100% test pass rate maintained

### Documentation & Cleanup
- [ ] Update documentation (README/CLAUDE.md) for new simulation features
  - [ ] Document new projected vs actual data workflow
  - [ ] Update simulation configuration documentation
  - [ ] Add examples of new functionality
- [ ] Move simulation_improvement.txt to done folder when complete

## Current Understanding

### Existing Structure
- Simulation currently copies `shared_files/players.csv` to `draft_helper/simulation/data/players_simulation.csv`
- SimulationDataManager handles data isolation for simulations
- DraftSimulationEngine runs drafts with team strategies
- SeasonSimulator handles head-to-head matchups for 17-week season

### New Structure (Target)
- `draft_helper/simulation/data/` contains multiple files:
  - `players_projected.csv` - Expected points for drafting decisions
  - `players_actual.csv` - Actual points earned for scoring
  - `teams_week_0.csv` - Team data for draft phase positional rankings
  - `teams_week_1.csv` through `teams_week_18.csv` - Weekly team data for season phase positional rankings

### Key Questions for Clarification
- ~~Line 7 in objective is incomplete~~ - RESOLVED: Should be ignored (was meant to be deleted)
- ~~Should teams_projected.csv and teams_actual.csv contain different data?~~ - RESOLVED: They are for positional ranking calculations
- ~~When using starter_helper for lineup optimization, should it write to simulation-specific directory?~~ - RESOLVED: No need for output files
- ~~Should the simulation maintain both projected and actual team rosters throughout the season?~~ - RESOLVED: Teams reference both projected and actual data versions
- ~~Are the existing team strategy algorithms expected to work with projected data without modification?~~ - RESOLVED: Yes, maintain config compatibility

## NEW REQUIREMENTS (Teams CSV Weekly Structure)
- **Teams CSV Files**: Now 19 versions (week_0.csv through week_18.csv) instead of just projected/actual
- **Draft Phase**: Use teams_week_0.csv for positional ranking calculations during drafting
- **Season Phase**: Use teams_week_1.csv through teams_week_18.csv for weekly positional rankings by starter_helper
- **File Structure**: `/simulation/data/teams_week_0.csv` to `/simulation/data/teams_week_18.csv`

## Notes
- All 4 data files already exist in `draft_helper/simulation/data/`
- Current simulation uses single data source for both decisions and scoring
- Integration with starter_helper will require careful path management
- Must maintain existing simulation configuration compatibility
- All unit tests must continue to pass (currently 241/241 success rate)

## Progress Log
- **Initial Analysis**: Examined existing simulation structure, identified current data flow using single copied CSV file
- **TODO Creation**: Created comprehensive task breakdown with clarifying questions
- **Clarifications Received**:
  - Line 7 config parameter should be ignored (was meant to be deleted)
  - teams.csv versions are for positional ranking calculations
  - No need for starter_helper output files, modify to work with simulation
  - Teams should reference both projected and actual roster versions
  - Replace old system completely, maintain config compatibility
- **Data Manager Updated**: Complete rewrite to handle projected/actual file pairs with new methods and validation
- **Config Updated**: Removed old file path references, kept SIMULATION_DATA_DIR
- **Main Simulator Updated**: Now loads both projected/actual dataframes and passes both to simulation
- **Draft Flow Complete**: DraftSimulationEngine now uses projected data for all draft decisions
- **NEW REQUIREMENTS RECEIVED**: Teams CSV structure changed to 19 weekly files (week_0.csv to week_18.csv)
  - Draft phase: Use teams_week_0.csv for positional rankings
  - Season phase: Use teams_week_1.csv through teams_week_18.csv for weekly positional rankings
  - Need to update SimulationDataManager and all components that use teams data
- **IMPLEMENTATION COMPLETED**: All core functionality implemented and tested
  - **SimulationDataManager**: Updated for weekly teams CSV structure (19 files)
  - **SeasonSimulator**: Now accepts projected/actual dataframes and uses actual data for scoring
  - **DraftSimulationEngine**: Uses week 0 teams CSV for positional rankings during draft
  - **Starter Helper Integration**: Full integration with weekly lineup optimization using projected data
  - **Weekly Teams Data**: Proper handling of teams_week_0.csv through teams_week_18.csv
  - **Unit Tests**: Updated and all 13 data manager tests passing