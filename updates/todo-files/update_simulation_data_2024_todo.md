# TODO: Update Simulation Data to 2024 Season

**Objective**: Update simulation/sim_data/ folder with 2024 season information and new schedule scoring format

**Created**: 2025-10-23

**Status**: Ready for Implementation

---

## Requirements Analysis

### Core Requirements

1. **Add season_schedule.csv to sim_data/**
   - Must contain 2024 NFL regular season schedule (weeks 1-17)
   - Format: week, team, opponent
   - Should match data/season_schedule.csv format

2. **Update teams_week files to new format**
   - Current format: team, offensive_rank, defensive_rank, opponent
   - New format: team, offensive_rank, defensive_rank, def_vs_qb_rank, def_vs_rb_rank, def_vs_wr_rank, def_vs_te_rank, def_vs_k_rank
   - Remove opponent column (now in season_schedule.csv)
   - 19 files total: teams_week_0.csv through teams_week_18.csv

3. **Ensure 2024 season data**
   - Team rankings should reflect 2024 NFL season
   - Verify player data is compatible with 2024 season
   - Verify bye weeks are accurate for 2024

### Discovered from Codebase Analysis

**Files that use sim_data/**:
- `simulation/SimulatedLeague.py` - Main simulation orchestrator
- `simulation/ParallelLeagueRunner.py` - Parallel execution
- `simulation/manual_simulation.py` - Manual testing
- `simulation/SimulationManager.py` - Simulation management

**Key Usage Patterns**:
```python
# SimulatedLeague.py checks for season_schedule.csv
if (self.data_folder / "season_schedule.csv").exists():
    shutil.copy(self.data_folder / "season_schedule.csv", team_dir / "season_schedule.csv")

# Creates SeasonScheduleManager with sim_data
season_schedule_mgr = SeasonScheduleManager(team_dir)
team_data_mgr = TeamDataManager(team_dir, season_schedule_mgr, config.current_nfl_week)
```

**Current sim_data/ Contents**:
- ✅ players_projected.csv (needs verification for 2024 compatibility)
- ✅ players_actual.csv (needs verification for 2024 compatibility)
- ✅ teams_week_0.csv through teams_week_18.csv (need format update + 2024 data)
- ❌ season_schedule.csv (MISSING - needs to be added)

---

## Implementation Tasks

### Phase 1: Data Preparation

#### Task 1.1: Create season_schedule.csv for sim_data/
**Priority**: HIGH
**Effort**: Low
**Dependencies**: None

**Description**: Fetch 2024 NFL schedule from ESPN API and create season_schedule.csv

**Steps**:
1. Use existing ESPN API client method `_fetch_full_season_schedule()` (espn_client.py:957-1031)
2. Fetch 2024 season schedule (weeks 1-17)
3. Format as CSV: week, team, opponent
4. Write to simulation/sim_data/season_schedule.csv
5. Verify format and completeness

**Alternative**: Extract from existing sim_data/teams_week_*.csv opponent columns (already has 2024 schedule embedded)

**Validation**:
- File exists at simulation/sim_data/season_schedule.csv
- Contains header: week,team,opponent
- Contains 32 teams × 17 weeks = 544 rows (+ 1 header = 545 total)
- All team abbreviations match standard 3-letter codes

**Files Modified**:
- NEW: `simulation/sim_data/season_schedule.csv`

---

#### Task 1.2: Fetch 2024 Team Rankings and Defense Stats
**Priority**: HIGH
**Effort**: Medium
**Dependencies**: None

**Description**: Fetch 2024 team rankings and position-specific defense stats from ESPN API

**Approach** (DECIDED):
Use ESPN API to fetch actual 2024 historical data

**Implementation**:
1. Use `_calculate_position_defense_rankings()` (espn_client.py:1033-1138)
   - Fetches player stats for entire 2024 season
   - Calculates points allowed by each defense to each position (QB/RB/WR/TE/K)
   - Ranks teams 1-32 (fewer points = better defense)
2. Generate team rankings for weeks 0-18
   - Week 0: Pre-season projections (can use consistent baseline)
   - Weeks 1-18: Cumulative season stats through each week

**Why ESPN API**:
- Code already exists in player-data-fetcher/espn_client.py
- Provides actual 2024 historical data for accuracy
- Matches simulation validation against 2024 season
- Industry-standard approach (calculate from player stats)
- Prior investigation documented in updates/espn_api_investigation_results.md

**Notes**:
- ESPN API does NOT provide position-specific defense ranks directly
- Must calculate from aggregated player fantasy points allowed
- This is the standard industry approach for defense rankings

---

### Phase 2: Update Team Files Format

#### Task 2.1: Update teams_week_0.csv format and data
**Priority**: HIGH
**Effort**: Medium
**Dependencies**: Task 1.2 (rankings source decision)

**Description**: Update teams_week_0.csv to new format with 2024 data

**Current Format**:
```csv
team,offensive_rank,defensive_rank,opponent
ARI,21,18,NO
...
```

**New Format**:
```csv
team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
ARI,19,20,11,23,10,26,27
...
```

**Steps**:
1. Create new CSV header
2. For each team, populate:
   - team (unchanged)
   - offensive_rank (from 2024 data source)
   - defensive_rank (from 2024 data source)
   - def_vs_qb_rank (from 2024 data source)
   - def_vs_rb_rank (from 2024 data source)
   - def_vs_wr_rank (from 2024 data source)
   - def_vs_te_rank (from 2024 data source)
   - def_vs_k_rank (from 2024 data source)
3. Remove opponent column (now in season_schedule.csv)
4. Ensure all 32 teams present
5. Verify ranking values are 1-32

**Data Source**:
- Reference: data/teams.csv for current rankings
- Adjust based on Task 1.2 decision

**Files Modified**:
- `simulation/sim_data/teams_week_0.csv`

---

#### Task 2.2: Update teams_week_1.csv through teams_week_18.csv
**Priority**: HIGH
**Effort**: High (18 files)
**Dependencies**: Task 2.1 (first file as template)

**Description**: Apply same format update to remaining 18 weekly team files

**Approach**:
1. Use teams_week_0.csv as template for format
2. For each week file (1-18):
   - Apply new CSV header
   - Populate team rankings (may vary slightly week-to-week or use consistent values)
   - Remove opponent column
   - Verify all 32 teams present

**Efficiency Strategy**:
- Create Python script to batch process all files
- Use consistent rankings across weeks (or apply minor variation)
- Validate output programmatically

**Script Pseudocode**:
```python
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from player_data_fetcher.espn_client import ESPNClient

async def update_teams_week_files():
    # Initialize ESPN client
    client = ESPNClient()

    # Fetch 2024 schedule
    schedule = await client._fetch_full_season_schedule()

    # Fetch all 2024 player stats
    players = await client.fetch_all_player_data()

    # Calculate position-specific defense rankings for each week
    for week in range(0, 19):
        # Calculate rankings through this week (cumulative)
        rankings = client._calculate_position_defense_rankings(
            players, schedule, current_week=week
        )

        # Format as CSV
        output_data = []
        for team in sorted(rankings.keys()):
            output_data.append({
                'team': team,
                'offensive_rank': rankings[team]['offensive_rank'],
                'defensive_rank': rankings[team]['defensive_rank'],
                'def_vs_qb_rank': rankings[team]['def_vs_qb_rank'],
                'def_vs_rb_rank': rankings[team]['def_vs_rb_rank'],
                'def_vs_wr_rank': rankings[team]['def_vs_wr_rank'],
                'def_vs_te_rank': rankings[team]['def_vs_te_rank'],
                'def_vs_k_rank': rankings[team]['def_vs_k_rank']
            })

        # Write to file
        df = pd.DataFrame(output_data)
        output_file = f'simulation/sim_data/teams_week_{week}.csv'
        df.to_csv(output_file, index=False)
        print(f"✅ Updated {output_file}")

# Run async
import asyncio
asyncio.run(update_teams_week_files())
```

**Files Modified**:
- `simulation/sim_data/teams_week_1.csv`
- `simulation/sim_data/teams_week_2.csv`
- ... (continuing through)
- `simulation/sim_data/teams_week_18.csv`

---

### Phase 3: Data Validation

#### Task 3.1: Validate season_schedule.csv
**Priority**: HIGH
**Effort**: Low
**Dependencies**: Task 1.1

**Description**: Verify season_schedule.csv is correctly formatted and complete

**Validation Checks**:
```python
import pandas as pd

schedule = pd.read_csv('simulation/sim_data/season_schedule.csv')

# Check 1: Correct columns
assert list(schedule.columns) == ['week', 'team', 'opponent']

# Check 2: Week range
assert schedule['week'].min() == 1
assert schedule['week'].max() == 17

# Check 3: Total matchups (32 teams × 17 weeks = 544 rows)
assert len(schedule) == 544

# Check 4: Each team appears exactly 17 times
team_counts = schedule['team'].value_counts()
assert all(team_counts == 17)
assert len(team_counts) == 32

# Check 5: Valid team abbreviations
valid_teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
               'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
               'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
               'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH']
assert all(schedule['team'].isin(valid_teams))
assert all(schedule['opponent'].isin(valid_teams))

# Check 6: Matchups are reciprocal (if ARI plays NO, NO plays ARI)
for _, row in schedule.iterrows():
    reciprocal = schedule[
        (schedule['week'] == row['week']) &
        (schedule['team'] == row['opponent']) &
        (schedule['opponent'] == row['team'])
    ]
    assert len(reciprocal) == 1

print("✅ season_schedule.csv validation passed")
```

**Success Criteria**:
- All validation checks pass
- No duplicate matchups
- No missing teams

---

#### Task 3.2: Validate teams_week files format
**Priority**: HIGH
**Effort**: Low
**Dependencies**: Task 2.2

**Description**: Verify all teams_week files have correct format and data

**Validation Checks**:
```python
import pandas as pd
from pathlib import Path

# Expected columns
expected_columns = [
    'team', 'offensive_rank', 'defensive_rank',
    'def_vs_qb_rank', 'def_vs_rb_rank', 'def_vs_wr_rank',
    'def_vs_te_rank', 'def_vs_k_rank'
]

# Validate each week file
for week in range(0, 19):
    file_path = f'simulation/sim_data/teams_week_{week}.csv'
    df = pd.read_csv(file_path)

    # Check 1: Correct columns
    assert list(df.columns) == expected_columns, f"Week {week}: Column mismatch"

    # Check 2: 32 teams present
    assert len(df) == 32, f"Week {week}: Expected 32 teams, got {len(df)}"

    # Check 3: No duplicate teams
    assert df['team'].nunique() == 32, f"Week {week}: Duplicate teams found"

    # Check 4: Rankings are 1-32
    for col in expected_columns[1:]:  # Skip 'team' column
        assert df[col].min() >= 1, f"Week {week}: {col} has value < 1"
        assert df[col].max() <= 32, f"Week {week}: {col} has value > 32"
        assert df[col].nunique() == 32, f"Week {week}: {col} has duplicate ranks"

    # Check 5: No NaN values
    assert not df.isnull().any().any(), f"Week {week}: Contains NaN values"

    print(f"✅ teams_week_{week}.csv validation passed")

print("\n✅ All teams_week files validated successfully")
```

**Success Criteria**:
- All 19 files pass validation
- Consistent format across all files
- Valid ranking values (1-32)

---

#### Task 3.3: Integration test with SimulatedLeague
**Priority**: HIGH
**Effort**: Medium
**Dependencies**: Task 3.1, Task 3.2

**Description**: Verify simulation can load and use updated data files

**Test Script**:
```python
from pathlib import Path
from simulation.SimulatedLeague import SimulatedLeague

# Load test config
test_config = {
    'config_name': 'validation_test',
    'parameters': {
        'CURRENT_NFL_WEEK': 8,
        # ... other required parameters
    }
}

# Initialize simulated league
data_folder = Path('simulation/sim_data')
league = SimulatedLeague(test_config, data_folder)

# Verify season_schedule loaded
assert league.season_schedule is not None
assert len(league.season_schedule) == 17  # 17 weeks

# Verify teams loaded for each week
for week in range(1, 18):
    teams_file = data_folder / f'teams_week_{week}.csv'
    assert teams_file.exists()

# Run first week simulation
league.run_draft()
league.run_single_week(week_num=1)

print("✅ Integration test passed - simulation can use updated data")
```

**Success Criteria**:
- SimulatedLeague initializes without errors
- season_schedule.csv loads successfully
- SeasonScheduleManager initializes correctly
- TeamDataManager can read new teams_week format
- First week simulates without errors

---

### Phase 4: Documentation

#### Task 4.1: Update simulation data README
**Priority**: MEDIUM
**Effort**: Low
**Dependencies**: Phase 3 complete

**Description**: Document the updated sim_data structure and 2024 data

**Create/Update**: `simulation/sim_data/README.md`

**Content**:
```markdown
# Simulation Data - 2024 Season

This folder contains data files used by the simulation system to run league simulations.

## Files

### Player Data
- `players_projected.csv` - Projected player statistics for 2024 season
- `players_actual.csv` - Actual player statistics for 2024 season

### Team Data
- `teams_week_0.csv` through `teams_week_18.csv` - Team rankings by week
  - Week 0: Pre-season rankings
  - Weeks 1-17: Regular season rankings
  - Week 18: Final regular season rankings

**Format**: team, offensive_rank, defensive_rank, def_vs_qb_rank, def_vs_rb_rank, def_vs_wr_rank, def_vs_te_rank, def_vs_k_rank

### Schedule Data
- `season_schedule.csv` - 2024 NFL regular season schedule (weeks 1-17)

**Format**: week, team, opponent

## Data Updates

**Last Updated**: 2025-10-23
**Season**: 2024 NFL Regular Season
**Weeks Covered**: 1-17 (regular season)

## Usage

These files are used by:
- `simulation/SimulatedLeague.py` - Main simulation orchestrator
- `simulation/ParallelLeagueRunner.py` - Parallel execution
- `league_helper/util/SeasonScheduleManager.py` - Schedule lookups
- `league_helper/util/TeamDataManager.py` - Team ranking lookups

## Data Sources

Team rankings: [Document source used for 2024 data]
Schedule: NFL 2024 regular season schedule
Player data: [Document source/generation method]

## Validation

To validate data files, run:
```bash
python tests/simulation/test_sim_data_validation.py
```
```

**Files Created/Modified**:
- NEW: `simulation/sim_data/README.md`

---

#### Task 4.2: Update ARCHITECTURE.md
**Priority**: LOW
**Effort**: Low
**Dependencies**: Task 4.1

**Description**: Update ARCHITECTURE.md to reflect sim_data structure changes

**Changes Needed**:
- Document new teams_week file format
- Document season_schedule.csv addition
- Update simulation data flow diagrams if present

**Search for**: References to "sim_data", "teams_week", "simulation data"

**Files Modified**:
- `ARCHITECTURE.md` (if updates needed)

---

### Phase 5: Testing

#### Task 5.1: Create validation test suite
**Priority**: MEDIUM
**Effort**: Medium
**Dependencies**: Phase 3 complete

**Description**: Create automated tests for sim_data validation

**Create**: `tests/simulation/test_sim_data_validation.py`

**Test Cases**:
1. `test_season_schedule_exists` - File exists
2. `test_season_schedule_format` - Correct columns and format
3. `test_season_schedule_completeness` - All weeks and teams
4. `test_season_schedule_reciprocal` - Matchups are reciprocal
5. `test_teams_week_files_exist` - All 19 files present
6. `test_teams_week_format` - Correct columns in all files
7. `test_teams_week_data_integrity` - Valid rankings, no duplicates
8. `test_teams_week_no_opponent_column` - Old format removed
9. `test_simulation_loads_data` - SimulatedLeague can load data
10. `test_season_schedule_manager_integration` - SeasonScheduleManager works

**Files Created**:
- NEW: `tests/simulation/test_sim_data_validation.py`

---

## Risk Analysis

### Risk 1: Historical Data Accuracy
**Impact**: MEDIUM
**Likelihood**: HIGH

**Issue**: May not have accurate historical 2024 week-by-week rankings

**Mitigation**:
- Use current 2024 rankings as baseline for all weeks
- Apply minor random variation to simulate week-to-week changes
- Document that sim_data uses approximated rankings for validation purposes
- Simulation validity depends on relative rankings, not absolute accuracy

---

### Risk 2: Breaking Existing Simulations
**Impact**: HIGH
**Likelihood**: MEDIUM

**Issue**: Format changes might break existing simulation code

**Mitigation**:
- Run full simulation test suite after changes (Task 3.3)
- Check all files that read teams_week files
- Verify SeasonScheduleManager handles schedule lookups correctly
- Test both manual_simulation.py and automated simulation runs

**Files to Check**:
- `simulation/SimulatedLeague.py`
- `league_helper/util/TeamDataManager.py`
- `league_helper/util/SeasonScheduleManager.py`
- Any code that reads teams_week files

---

### Risk 3: Player Data Compatibility
**Impact**: MEDIUM
**Likelihood**: LOW

**Issue**: Player data might have 2023 data or incorrect bye weeks for 2024

**Mitigation**:
- Verify bye_week column in players files matches 2024 season
- Check if any players need updates for 2024 team changes
- Validate player IDs are current

**Validation**:
```python
# Check bye weeks are reasonable (1-17)
players = pd.read_csv('simulation/sim_data/players_projected.csv')
assert players['bye_week'].min() >= 1
assert players['bye_week'].max() <= 17
```

---

## Success Criteria

**Phase 1 Complete**:
- ✅ season_schedule.csv added to sim_data/
- ✅ 2024 data source identified and documented

**Phase 2 Complete**:
- ✅ All 19 teams_week files updated to new format
- ✅ Opponent column removed from all teams_week files
- ✅ Position-specific defensive rankings added to all files

**Phase 3 Complete**:
- ✅ All validation checks pass
- ✅ Integration test successful
- ✅ No errors when running SimulatedLeague

**Phase 4 Complete**:
- ✅ sim_data/README.md created
- ✅ ARCHITECTURE.md updated (if needed)

**Phase 5 Complete**:
- ✅ Validation test suite created
- ✅ All tests passing

**Final Validation**:
- ✅ Run full simulation test suite: `python tests/run_all_tests.py`
- ✅ All 1910+ tests still passing
- ✅ Manual simulation run completes successfully
- ✅ No regression in simulation functionality

---

## Estimated Effort

**UPDATED** - Using existing ESPN API infrastructure:

- **Phase 1**: 30 minutes (ESPN API integration script)
- **Phase 2**: 15 minutes (automated bulk update via ESPN data)
- **Phase 3**: 1 hour (validation and integration testing)
- **Phase 4**: 30 minutes (documentation)
- **Phase 5**: 1 hour (test creation)

**Total**: ~3 hours (significantly reduced from original 7-11 hours)

**Rationale for reduction**:
- ESPN API code already exists (no development needed)
- Data fetching is automated (no manual research/compilation)
- Bulk processing via script (no per-file manual work)
- Main effort is script orchestration and validation

---

## Verification Iterations - COMPLETE ✅

**Date**: 2025-10-23
**Iterations**: 6 (2 rounds of 3 each)
**Status**: All questions answered, ready for implementation

### Round 1: Understanding Current State (Iterations 1-3)

**Iteration 1: Code Analysis**
- ✅ SimulatedLeague already checks for and copies season_schedule.csv (line 172-173)
- ✅ TeamData class defines expected format (utils/TeamData.py lines 18-74)
- ✅ SeasonScheduleManager loads schedule with format: week,team,opponent
- ✅ No code changes needed - data format update only

**Iteration 2: Format Comparison**
- ✅ Current sim_data format: team, offensive_rank, defensive_rank, opponent
- ✅ Expected format: team, offensive_rank, defensive_rank, def_vs_qb_rank, def_vs_rb_rank, def_vs_wr_rank, def_vs_te_rank, def_vs_k_rank
- ✅ data/teams.csv already has correct format (reference for update)
- ✅ Schedule data confirmed 2024 (matches season_schedule.csv)
- ✅ Bye weeks confirmed 2024 (weeks 5-12, 14 - no week 13)

**Iteration 3: Testing Coverage**
- ✅ Current tests use mock data folders (tmp_path / "sim_data")
- ✅ No tests validate actual sim_data folder format
- ✅ Integration tests mock the data
- ✅ Need to create validation tests for updated format

### Round 2: Answering Questions & Planning (Iterations 4-6)

**Iteration 4: Question Answers** ✅

**Q1: Data Source Decision**
- **ANSWER**: Use ESPN API to fetch **2024 historical data**
- **Rationale**:
  - Code already exists in `player-data-fetcher/espn_client.py`:
    - `_fetch_full_season_schedule()` (lines 957-1031): Fetches 2024 schedule
    - `_calculate_position_defense_rankings()` (lines 1033-1138): Calculates position-specific defense ranks
  - ESPN investigation already completed (see `updates/espn_api_investigation_results.md`)
  - Can fetch actual 2024 season data for accuracy
  - Simulation data should match the historical season being validated

**Q2: Player Data**
- **ANSWER**: Keep player files unchanged
- **Rationale**:
  - Already have correct 2024 bye weeks
  - Simulation needs separate projected vs actual (draft vs scoring)
  - data/players.csv is 2025 data (not compatible)
  - Oct 17 files are 2024 data (correct for simulation)
  - Player files have:
    - players_projected.csv: Even point distribution for draft decisions
    - players_actual.csv: Realistic variance for weekly scoring

**Q3: Validation Rigor**
- **ANSWER**: Use actual 2024 historical data from ESPN API
- **Rationale**:
  - Simulation validates against 2024 season performance
  - ESPN API provides accurate historical data
  - Existing code infrastructure supports it
  - More accurate than static rankings
  - Key requirements (all met):
    - ✅ Valid team rankings (1-32) from ESPN
    - ✅ Valid 2024 schedule (17 weeks) from ESPN
    - ✅ Correct 2024 bye weeks (already in sim_data)
    - ✅ Position-specific defense ranks (calculated from ESPN stats)

**Iteration 5: File Mapping** ✅

**Files to ADD: 1**
1. `simulation/sim_data/season_schedule.csv`
   - Source: `data/season_schedule.csv` (copy)
   - Size: 545 lines (544 matchups + header)
   - Format: week,team,opponent

**Files to UPDATE: 19**
1-19. `simulation/sim_data/teams_week_0.csv` through `teams_week_18.csv`
   - Source template: `data/teams.csv`
   - Size: 33 lines each (32 teams + header)
   - Remove: opponent column
   - Add: def_vs_qb_rank, def_vs_rb_rank, def_vs_wr_rank, def_vs_te_rank, def_vs_k_rank
   - Update: Use 2024 rankings

**Files UNCHANGED: 2**
- `simulation/sim_data/players_projected.csv` (draft decisions)
- `simulation/sim_data/players_actual.csv` (weekly scoring)

**Iteration 6: Completeness Validation** ✅

**Implementation Scripts Ready:**
- ✅ update_sim_data_2024.py - Transform all files
- ✅ validate_sim_data.py - Verify format and data integrity
- ✅ Integration test approach defined
- ✅ No code changes needed

**All Requirements Covered:**
- ✅ season_schedule.csv addition
- ✅ teams_week format update (19 files)
- ✅ 2024 data verification
- ✅ Position-specific defense ranks
- ✅ Remove opponent column
- ✅ Validation strategy
- ✅ Testing approach
- ✅ Documentation plan

**Implementation Scripts Pseudocode:**
```python
# update_sim_data_2024.py - Using ESPN API
import asyncio
from player_data_fetcher.espn_client import ESPNClient

async def main():
    client = ESPNClient()

    # 1. Fetch 2024 season schedule from ESPN API
    schedule = await client._fetch_full_season_schedule()
    # Write to sim_data/season_schedule.csv
    write_schedule_csv(schedule, 'simulation/sim_data/season_schedule.csv')

    # 2. Fetch all 2024 player stats
    players = await client.fetch_all_player_data()

    # 3. Calculate position-specific defense rankings for each week (0-18)
    for week in range(0, 19):
        rankings = client._calculate_position_defense_rankings(
            players, schedule, current_week=week
        )
        # Write to sim_data/teams_week_N.csv
        write_teams_csv(rankings, f'simulation/sim_data/teams_week_{week}.csv')

    # 4. Validate all outputs
    validate_all_files()

asyncio.run(main())

# validate_sim_data.py
1. Validate season_schedule.csv:
   - Columns: week, team, opponent
   - 544 matchups (32 teams × 17 weeks)
   - Reciprocal matchups (if A plays B, B plays A)
2. Validate teams_week files (19 files):
   - Correct columns (8 total, no opponent)
   - 32 teams each
   - Rankings 1-32
   - No duplicates
```

---

## ESPN API Implementation Considerations

### Season Configuration
- ESPN client uses `NFL_SEASON` constant to specify year
- Must ensure `NFL_SEASON = 2024` when fetching data
- Check `player-data-fetcher/espn_client.py` configuration before running

### API Rate Limiting
- ESPN API has rate limits for requests
- Fetching full season data requires:
  - 18 requests for schedule (weeks 1-18)
  - Multiple requests for player stats
- Consider adding delays between requests if rate limited
- Existing client has `_make_request()` with retry logic

### Data Availability
- 2024 season must be complete for historical data
- Verify ESPN API still provides 2024 data (not archived)
- If 2024 data unavailable, fallback to extraction from existing sim_data/teams_week_*.csv files

### Alternative Approach (Fallback)
If ESPN API is unavailable or 2024 data is not accessible:
1. Extract schedule from existing sim_data/teams_week_*.csv opponent columns
2. Use consistent team rankings across all weeks (simplified approach)
3. Manually populate position-specific defense rankings from available sources

### Key ESPN Client Methods Reference
- `_fetch_full_season_schedule()`: Lines 957-1031 in espn_client.py
- `_calculate_position_defense_rankings()`: Lines 1033-1138 in espn_client.py
- `_make_request()`: HTTP client with retry logic
- `fetch_all_player_data()`: Fetch all player stats for season

---

## Implementation Ready Status - FINAL ✅

**Pre-implementation checklist**:
- ✅ All files identified (20 files to modify/add)
- ✅ Current format documented
- ✅ Target format documented
- ✅ Dependencies mapped
- ✅ Risks identified with mitigations
- ✅ All questions answered through verification
- ✅ Implementation scripts ready
- ✅ Validation scripts ready
- ✅ No code changes needed (data-only update)
- ✅ Test strategy defined

**Ready to proceed**: YES - All information gathered, implementation can begin immediately.

**Estimated Time**: 30-60 minutes (mostly script execution and validation)

---

## Final Implementation Summary

### Decision: ESPN API Approach ✅

After research and verification, the implementation will use **ESPN API to fetch actual 2024 historical data**.

### Why ESPN API?
1. **Code already exists**: Full implementation in `player-data-fetcher/espn_client.py`
2. **Accurate data**: Actual 2024 season statistics, not approximations
3. **Prior validation**: Approach documented in `updates/espn_api_investigation_results.md`
4. **Standard approach**: Industry-standard method for defense rankings

### Key Implementation Points:
1. **Schedule Data**: Use `_fetch_full_season_schedule()` to get 2024 NFL schedule
2. **Defense Rankings**: Use `_calculate_position_defense_rankings()` to compute position-specific stats
3. **Week-by-week**: Generate rankings for weeks 0-18 (cumulative through each week)
4. **Format Update**: Remove opponent column, add 5 position-specific defense rank columns

### Files to Generate:
- **1 new file**: `simulation/sim_data/season_schedule.csv` (2024 schedule)
- **19 updated files**: `simulation/sim_data/teams_week_0.csv` through `teams_week_18.csv` (new format)
- **2 unchanged files**: Player CSV files (already 2024 data)

### Critical Note:
The main `data/` folder contains **2025 season data** and should NOT be used as source. The simulation requires **2024 historical data** to validate against the completed season.

### Alternative (If ESPN API Unavailable):
Extract 2024 schedule from existing sim_data opponent columns; use simplified/consistent rankings

---

**Next Step**: Create `update_sim_data_2024.py` script to orchestrate ESPN API calls and generate files

---

## Verification Iteration 7: ESPN API Implementation Details ✅

**Date**: 2025-10-23 (continued)
**Focus**: Verify actual ESPN client implementation and identify critical issues

### Critical Finding #1: Config Season Mismatch 🚨

**Issue**: `player-data-fetcher/config.py` line 14 has `NFL_SEASON = 2025`
- ESPN API methods use `NFL_SEASON` from config to fetch data
- We need 2024 historical data, not 2025 data
- All ESPN methods (`_fetch_full_season_schedule`, `_calculate_team_rankings_from_stats`) reference this config

**Solutions**:
1. **Option A (Recommended)**: Temporarily override config in script
   ```python
   import sys
   sys.path.insert(0, 'player-data-fetcher')
   import config
   config.NFL_SEASON = 2024  # Override for this script only
   from espn_client import ESPNClient
   ```

2. **Option B**: Modify ESPN client methods to accept season parameter (requires code changes)

3. **Option C**: Use fallback approach (extract schedule from existing sim_data opponent columns)

### Verified: ESPN Client Methods ✅

**Confirmed method signatures and functionality**:

1. **`_fetch_full_season_schedule()`** (lines 957-1031)
   - Returns: `Dict[int, Dict[str, str]]` - `{week: {team: opponent}}`
   - Uses `NFL_SEASON` from config (line 981)
   - Makes 18 API calls (one per week)
   - Has rate limiting (0.2s delay between requests)

2. **`_calculate_position_defense_rankings()`** (lines 1033-1138)
   - Returns: `Dict[str, Dict[str, int]]` - `{team: {'def_vs_qb_rank': int, ...}}`
   - **ONLY** returns 5 position-specific defense ranks
   - **Does NOT** return offensive_rank or defensive_rank
   - Uses actual player stats to calculate points allowed

3. **`_fetch_team_rankings()`** (line 350)
   - Returns: `Dict[str, Dict[str, int]]` - `{team: {'offensive_rank': int, 'defensive_rank': int}}`
   - Calls `_calculate_team_rankings_from_stats()`
   - Uses `NFL_SEASON` from config

4. **`_calculate_team_rankings_from_stats()`** (lines 727-799)
   - Calculates offensive_rank (by points per game)
   - Calculates defensive_rank (by takeaways)
   - Uses `NFL_SEASON` from config (line 741)
   - Falls back to previous season if insufficient data

### Critical Finding #2: Must Combine Two Method Results 🚨

**Issue**: teams_week files need 8 columns, but methods return different subsets:
- `_calculate_position_defense_rankings()` returns: def_vs_qb_rank, def_vs_rb_rank, def_vs_wr_rank, def_vs_te_rank, def_vs_k_rank (5 columns)
- `_fetch_team_rankings()` returns: offensive_rank, defensive_rank (2 columns)
- Total needed: 7 ranking columns + 1 team column = 8 columns

**Solution**: Call BOTH methods and merge results:
```python
# Get offensive/defensive rankings
team_rankings = await client._fetch_team_rankings()

# Get position-specific defense rankings
pos_def_rankings = client._calculate_position_defense_rankings(
    players, schedule, current_week=week
)

# Merge results
for team in all_teams:
    combined_data[team] = {
        'team': team,
        'offensive_rank': team_rankings[team]['offensive_rank'],
        'defensive_rank': team_rankings[team]['defensive_rank'],
        **pos_def_rankings[team]  # Adds def_vs_qb_rank, etc.
    }
```

### Verified: ESPNPlayerData Model ✅

**Confirmed**: `ESPNPlayerData` class (player_data_models.py:25) has:
- `get_week_points(week: int)` method (line 78) ✅
- Returns `Optional[float]` for weeks 1-17
- Used by `_calculate_position_defense_rankings()` to get player stats

### Verified: Sim Data Format ✅

**Confirmed**: `simulation/sim_data/teams_week_1.csv` contains:
- OLD format: team, offensive_rank, defensive_rank, opponent
- 2024 schedule embedded in opponent column
- Can extract schedule from existing files if ESPN API unavailable

### Updated Implementation Requirements

**Phase 1 Changes**:
1. Override `config.NFL_SEASON = 2024` before importing ESPN client
2. Call `_fetch_team_rankings()` for offensive/defensive ranks
3. Call `_calculate_position_defense_rankings()` for position-specific ranks
4. Merge both results into 8-column format
5. Handle season config override carefully to avoid affecting other scripts

**Estimated Effort Update**:
- Config override adds minimal complexity (~5 minutes)
- Merging two data sources adds ~10 minutes
- Total remains ~3 hours (mostly waiting for API calls)

### Risk Analysis Update

**New Risk: Config Override Side Effects**
- **Impact**: LOW
- **Likelihood**: LOW
- **Mitigation**: Use sys.path manipulation to isolate imports; restore config after execution

**New Risk: API Data Availability for 2024**
- **Impact**: MEDIUM
- **Likelihood**: MEDIUM
- **Issue**: ESPN may not provide complete 2024 historical data
- **Mitigation**: Fallback to extracting schedule from existing sim_data files; use neutral rankings if needed

---

## Verification Summary - All Iterations Complete ✅

**7 Iterations Total**:
1. ✅ Code analysis (SimulatedLeague, TeamData)
2. ✅ Format comparison (old vs new)
3. ✅ Testing coverage review
4. ✅ Question answers (ESPN API approach)
5. ✅ File mapping (20 files)
6. ✅ Completeness validation
7. ✅ **ESPN API implementation details (THIS ITERATION)**

**All questions answered. Ready for implementation with documented caveats.**

---

## Verification Iteration 8: Initialization and Fallback Validation ✅

**Date**: 2025-10-23 (continued)
**Focus**: Verify ESPNClient initialization requirements and validate fallback approach

### Verified: ESPNClient Initialization ✅

**Requirements for creating ESPNClient**:
```python
from pydantic_settings import BaseSettings
from player_data_models import ScoringFormat

class Settings(BaseSettings):
    scoring_format: ScoringFormat = ScoringFormat.PPR
    season: int = 2024  # MUST set to 2024 for our use case
    current_nfl_week: int = 8
    # ... other optional settings

# Initialize client
settings = Settings()
client = ESPNClient(settings)
```

**Key Finding**: ESPNClient initialization is straightforward - just needs a Settings object with:
- `season` (int) - **CRITICAL**: Must be 2024 for historical data
- `scoring_format` (ScoringFormat enum) - PPR/Half-PPR/Standard
- `current_nfl_week` (int) - Used for ranking calculations
- Other settings have defaults

**Reference**: player_data_fetcher_main.py lines 41-69, 430

### Verified: Public API Method ✅

**Main data fetching method**: `get_season_projections()` (espn_client.py:696)
```python
players = await client.get_season_projections()
# Returns: List[ESPNPlayerData]
# Each player has:
#   - team, position, name
#   - get_week_points(week) method for weeks 1-17
```

**Usage pattern**:
```python
import asyncio
from espn_client import ESPNClient

# Override config for 2024
import sys
sys.path.insert(0, 'player-data-fetcher')
import config
config.NFL_SEASON = 2024
config.CURRENT_NFL_WEEK = 18  # Use final week to get all data

# Create settings and client
settings = Settings()
client = ESPNClient(settings)

# Fetch all data
schedule = await client._fetch_full_season_schedule()
team_rankings = await client._fetch_team_rankings()
players = await client.get_season_projections()

# Calculate position-specific defense rankings
pos_def_rankings = client._calculate_position_defense_rankings(
    players, schedule, current_week=18
)
```

### Verified: Fallback Schedule Extraction ✅

**Confirmed**: All 19 teams_week files (0-18) exist in sim_data with 2024 schedule embedded

**Sample data** (teams_week_1.csv):
```csv
team,offensive_rank,defensive_rank,opponent
ARI,21,18,NO
ATL,24,8,TB
BAL,5,28,BUF
```

**Extraction logic**:
```python
import pandas as pd
from pathlib import Path

def extract_2024_schedule_from_sim_data():
    """Extract 2024 schedule from existing sim_data files"""
    schedule_data = []

    for week in range(1, 18):  # Weeks 1-17
        file_path = Path(f'simulation/sim_data/teams_week_{week}.csv')
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            if row['opponent'] != 'BYE':
                schedule_data.append({
                    'week': week,
                    'team': row['team'],
                    'opponent': row['opponent']
                })

    # Create season_schedule.csv
    schedule_df = pd.DataFrame(schedule_data)
    schedule_df.to_csv('simulation/sim_data/season_schedule.csv', index=False)
    return schedule_df
```

**Advantages of fallback approach**:
- ✅ No API calls required
- ✅ Data already verified as 2024 season
- ✅ Handles BYE weeks correctly (week 5 shows ATL,BYE)
- ✅ Fast execution (< 1 second)

**Disadvantages**:
- ❌ Still need ESPN API for position-specific defense rankings
- ❌ Still need ESPN API for offensive/defensive rankings (unless we use placeholders)

### Implementation Decision Matrix

| Approach | Schedule | Offensive/Defensive Ranks | Position-Specific Defense Ranks | Effort | Data Quality |
|----------|----------|---------------------------|----------------------------------|--------|--------------|
| **Full ESPN API** | ESPN API | ESPN API | ESPN API (calculated) | Medium | High (actual 2024 data) |
| **Hybrid (Recommended)** | Extract from sim_data | ESPN API | ESPN API (calculated) | Low-Medium | High |
| **Minimal (Emergency)** | Extract from sim_data | Use neutral (16) | Use neutral (16) | Very Low | Low (simulation will be inaccurate) |

**Recommended**: **Hybrid Approach**
1. Extract schedule from existing sim_data files (fast, reliable)
2. Use ESPN API for offensive/defensive/position-specific rankings (accurate data)
3. Benefit: Reduces API calls by 18 requests (full schedule fetch)

### Updated Implementation Script Outline

```python
#!/usr/bin/env python3
"""
Update simulation data to 2024 format with schedule scoring support.

Hybrid approach:
1. Extract schedule from existing sim_data files (no API needed)
2. Fetch team rankings from ESPN API (2024 data)
3. Calculate position-specific defense rankings from ESPN player stats
"""

import asyncio
import sys
from pathlib import Path
import pandas as pd

# Override config for 2024 data
sys.path.insert(0, 'player-data-fetcher')
import config
config.NFL_SEASON = 2024
config.CURRENT_NFL_WEEK = 18  # Use final week for complete data

from espn_client import ESPNClient
from player_data_fetcher_main import Settings

async def main():
    # Step 1: Extract schedule from existing sim_data (FAST)
    print("Extracting 2024 schedule from sim_data files...")
    schedule_data = extract_schedule_from_sim_data()
    schedule_data.to_csv('simulation/sim_data/season_schedule.csv', index=False)

    # Step 2: Initialize ESPN client with 2024 config
    print("Initializing ESPN client for 2024 data...")
    settings = Settings(season=2024, current_nfl_week=18)
    client = ESPNClient(settings)

    # Step 3: Fetch team rankings
    print("Fetching 2024 team rankings from ESPN...")
    team_rankings = await client._fetch_team_rankings()

    # Step 4: Fetch player data for position-specific calculations
    print("Fetching 2024 player stats from ESPN...")
    players = await client.get_season_projections()

    # Step 5: Build schedule dict for defense rankings
    schedule_dict = build_schedule_dict(schedule_data)

    # Step 6: Generate teams_week files for weeks 0-18
    print("Generating teams_week files...")
    for week in range(0, 19):
        print(f"  Week {week}/18...", end='')

        # Calculate position-specific defense rankings for this week
        pos_def_rankings = client._calculate_position_defense_rankings(
            players, schedule_dict, current_week=week if week > 0 else 1
        )

        # Merge team rankings + position defense rankings
        combined_data = merge_rankings(team_rankings, pos_def_rankings)

        # Write to CSV
        write_teams_week_csv(combined_data, week)
        print(" Done")

    print("\n✅ All files generated successfully!")
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Risk Assessment Update

**Reduced Risk with Hybrid Approach**:
- **Schedule extraction**: LOW risk (data already exists, no API dependency)
- **ESPN API availability**: MEDIUM risk (only for rankings, not schedule)
- **Config override**: LOW risk (isolated to script execution)
- **Data quality**: HIGH (uses actual 2024 data where available)

### Estimated Effort Update (Hybrid Approach)

- **Schedule extraction**: 10 minutes (simple pandas script)
- **ESPN API integration**: 30 minutes (settings override + client setup)
- **Rankings merge logic**: 15 minutes (combine two datasets)
- **File generation loop**: 10 minutes (write 19 CSVs)
- **Validation**: 30 minutes (verify format and data)
- **Testing**: 45 minutes (integration test with SimulatedLeague)

**Total**: ~2.5 hours (reduced from 3 hours with full ESPN approach)

---

## Verification Summary - 8 Iterations Complete ✅

**8 Iterations Total**:
1. ✅ Code analysis (SimulatedLeague, TeamData)
2. ✅ Format comparison (old vs new)
3. ✅ Testing coverage review
4. ✅ Question answers (ESPN API approach)
5. ✅ File mapping (20 files)
6. ✅ Completeness validation
7. ✅ ESPN API implementation details
8. ✅ **Initialization & fallback validation (THIS ITERATION)**

**Recommendation**: Use **Hybrid Approach** (extract schedule from sim_data + ESPN API for rankings)
**Ready for implementation**: YES - All questions answered with complete implementation plan
