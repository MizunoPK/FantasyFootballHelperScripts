# Historical Data Compiler - Implementation TODO

> **IMPORTANT**: Keep this file updated as you progress. Mark tasks complete, add notes, and document any blockers for future sessions.

---

## Overview

**Objective**: Create `compile_historical_data.py` - a standalone script that fetches historical NFL season data from ESPN APIs and creates point-in-time snapshots for simulation system testing.

**Output Location**: `simulation/sim_data/{YEAR}/`

**Data Sources**:
- ESPN Fantasy API (player data, projections, ADP)
- ESPN Scoreboard API (schedule, game data, scores)
- Open-Meteo API (weather data)

---

## Phase 1: Project Setup and Core Infrastructure

### 1.1 Create script file and folder structure
- [ ] Create `compile_historical_data.py` at project root
- [ ] Add argument parsing (--year parameter, required)
- [ ] Add year validation (2021+ only)
- [ ] Create output folder structure generator

**Files to create/modify**:
- `compile_historical_data.py` (new)

### 1.2 Set up HTTP client and constants
- [ ] Create `historical_data_compiler/` module folder (per Q1: multi-module)
- [ ] Create `__init__.py`
- [ ] Create `constants.py` - COPY from `player-data-fetcher/player_data_constants.py` (per Q2: copy and adapt)
- [ ] Create `http_client.py` - COPY HTTP patterns from `player-data-fetcher/espn_client.py`
- [ ] Add adaptive throttling with tenacity retry (per Q3: adaptive throttling)

**Files to create**:
- `historical_data_compiler/__init__.py`
- `historical_data_compiler/constants.py`
- `historical_data_compiler/http_client.py`

**Copy from existing code** (per Q2):
- `player-data-fetcher/player_data_constants.py` → copy ESPN_TEAM_MAPPINGS, ESPN_POSITION_MAPPINGS
- `player-data-fetcher/espn_client.py:117-166` → copy retry pattern:
  ```python
  @retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=10))
  async def _make_request(self, method: str, url: str, **kwargs):
      await asyncio.sleep(self.settings.rate_limit_delay)  # 0.1-0.5s
      # Handle 429 → ESPNRateLimitError (triggers retry)
      # Handle 500+ → ESPNServerError (triggers retry)
      # Handle 400-499 → ESPNAPIError (no retry)
  ```

### 1.3 Set up logging and error handling
- [ ] Configure logging using project's LoggingManager
- [ ] Implement error handling following project patterns
- [ ] Add fail-loud behavior - ANY error stops entire compilation (per Q4: fail completely)
- [ ] No partial output on failure - clean exit with error message

**Files to reference**:
- `utils/LoggingManager.py`
- `utils/error_handler.py`

**Error Handling Strategy** (per Q4):
- Wrap main compilation in try/except
- Any exception → log error, clean up partial files, exit(1)
- No "continue with warnings" - simulation needs complete data

---

## Phase 2: Season Schedule Fetcher

### 2.1 Create schedule fetcher module
- [ ] Create `schedule_fetcher.py` module
- [ ] Implement ESPN Scoreboard API calls for schedule
- [ ] Extract team matchups for weeks 1-17
- [ ] Handle bye week detection (team missing from week = bye)
- [ ] Normalize team abbreviations (use ESPN_TEAM_MAPPINGS)

**API Endpoint**:
```
https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
Parameters: seasontype=2, week={1-17}, dates={YEAR}
```

**Output**: `season_schedule.csv`
```csv
week,team,opponent
1,ARI,BUF
...
6,KC,  # bye week - empty opponent
```

**Reusable code**:
- `schedule-data-fetcher/ScheduleFetcher.py` - schedule fetching logic

### 2.2 Write season_schedule.csv
- [ ] Implement CSV writer for schedule
- [ ] Include all 32 teams for all 17 weeks
- [ ] Bye weeks have empty opponent field
- [ ] Validate output (all teams present, correct week count)

---

## Phase 3: Game Data Fetcher

### 3.1 Create game data fetcher module
- [ ] Create `game_data_fetcher.py` module
- [ ] Implement ESPN Scoreboard API calls for game results
- [ ] Extract scores, venue info, game dates
- [ ] Handle neutral site games
- [ ] Handle indoor vs outdoor venues

**API Endpoint**: Same as schedule (ESPN Scoreboard)

**Field mappings from ESPN API**:
| Field | ESPN API Path |
|-------|--------------|
| home_team | `competitions[0].competitors[].team.abbreviation` where `homeAway=home` |
| away_team | `competitions[0].competitors[].team.abbreviation` where `homeAway=away` |
| home_team_score | `competitions[0].competitors[].score` where `homeAway=home` |
| away_team_score | `competitions[0].competitors[].score` where `homeAway=away` |
| indoor | `competitions[0].venue.indoor` |
| neutral_site | `competitions[0].neutralSite` |
| country | `competitions[0].venue.address.country` |
| city | `competitions[0].venue.address.city` |
| state | `competitions[0].venue.address.state` |
| date | `event.date` |

### 3.2 Integrate weather data
- [ ] Create `weather_fetcher.py` module
- [ ] Implement Open-Meteo Archive API calls (historical)
- [ ] Implement Open-Meteo Forecast API calls (recent)
- [ ] Load stadium coordinates from coordinates.json
- [ ] Skip weather for indoor games (return None)
- [ ] Find hourly data closest to game start time

**API Endpoints**:
```
Historical: https://archive-api.open-meteo.com/v1/archive
Forecast: https://api.open-meteo.com/v1/forecast
Parameters: latitude, longitude, hourly=temperature_2m,wind_gusts_10m,precipitation
Units: fahrenheit, mph, inch
```

**Reusable code**:
- `player-data-fetcher/game_data_fetcher.py` - weather fetching logic
- `player-data-fetcher/coordinates_manager.py` - stadium coordinates

### 3.3 Write game_data.csv
- [ ] Implement CSV writer for game data
- [ ] Combine ESPN data with weather data
- [ ] Handle all 17 weeks
- [ ] Validate output (all games present, weather for outdoor games)

**Output**: `game_data.csv`
```csv
week,home_team,away_team,temperature,gust,precipitation,home_team_score,away_team_score,indoor,neutral_site,country,city,state,date
```

---

## Phase 4: Player Data Fetcher

### 4.1 Create ESPN Fantasy API client
- [ ] Create `espn_fantasy_client.py` module
- [ ] Implement player data fetching for all 6 positions (QB, RB, WR, TE, K, DST)
- [ ] Handle weekly actual points (`statSourceId=0, appliedTotal`)
- [ ] Handle weekly projected points (`statSourceId=1, appliedTotal`)
- [ ] Extract ADP (`ownership.averageDraftPosition`)
- [ ] Extract draft rank (`draftRanksByRankType.PPR.rank`)

**API Endpoint**:
```
https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{YEAR}/segments/0/leaguedefaults/3
Parameters: view=kona_player_info, scoringPeriodId=0 (all weeks)
```

**Position Filtering** (X-Fantasy-Filter header):
| Position | Slot ID | Position ID |
|----------|---------|-------------|
| QB | 0 | 1 |
| RB | 2 | 2 |
| WR | 4 | 3 |
| TE | 6 | 4 |
| K | 17 | 5 |
| DST | 16 | 16 |

**Reusable code**:
- `player-data-fetcher/espn_client.py` - API calls, X-Fantasy-Filter patterns

### 4.2 Implement player filtering
- [ ] Filter by activity (at least 1 game played OR has projected points)
- [ ] Skip players with no projections entirely
- [ ] Filter by fantasy-relevant positions only (QB, RB, WR, TE, K, DST)

### 4.3 Calculate player_rating field
- [ ] Week 1: Use ESPN draft rank, normalize to position-specific 1-100 scale
- [ ] Week 2+: Calculate from cumulative fantasy_points, rank within position
- [ ] Normalization formula:
  ```
  player_rating = max(1, 100 - ((position_rank - 1) / total_in_position) * 99)
  ```

### 4.4 Build weekly player data structures
- [ ] For each week 1-17, build player data with:
  - Past weeks: actual points
  - Current/future weeks: projected points
  - Bye weeks: 0 points
- [ ] Calculate fantasy_points total (sum of all week columns)
- [ ] Look up bye_week from schedule

---

## Phase 5: Team Data Calculator

### 5.1 Create team data calculator module
- [ ] Create `team_data_calculator.py` module
- [ ] Implement algorithm from `espn_client.py:_collect_team_weekly_data()`

**Algorithm**:
```
For each team and each week:
  1. Initialize: pts_allowed_to_{QB,RB,WR,TE,K} = 0, points_scored = 0, points_allowed = 0
  2. For each player in league:
     - Get player's fantasy points for this week
     - Add to player's team's points_scored
     - Find opponent from schedule
     - Add to opponent's pts_allowed_to_{player.position}
     - Add to opponent's points_allowed
  3. Round all values to 1 decimal place
```

### 5.2 Write team data files
- [ ] Create `team_data/` subfolder
- [ ] Write 32 CSV files (one per team: ARI.csv, ATL.csv, etc.)
- [ ] Include bye weeks with 0 values for all fields
- [ ] Validate output (32 files, 17 rows each)

**Output**: `team_data/{TEAM}.csv`
```csv
week,pts_allowed_to_QB,pts_allowed_to_RB,pts_allowed_to_WR,pts_allowed_to_TE,pts_allowed_to_K,points_scored,points_allowed
```

---

## Phase 6: Weekly Snapshot Generator

### 6.1 Create players.csv generator
- [ ] Create `weekly_snapshot_generator.py` module
- [ ] For week X, generate players.csv with:
  - Weeks < X: Actual points from ESPN API
  - Weeks >= X: Projected points from ESPN API
  - Bye weeks: 0
- [ ] Include all fields: id, name, team, position, bye_week, fantasy_points, injury_status, drafted, locked, average_draft_position, player_rating, week_1_points...week_17_points
- [ ] Default injury_status to "ACTIVE"
- [ ] Default drafted and locked to 0

### 6.2 Create players_projected.csv generator
- [ ] For week X, generate players_projected.csv with:
  - Weeks < X: Historical projection from ESPN API for that week
  - Weeks >= X: Current projection from ESPN API for week X
  - Bye weeks: 0
- [ ] Same fields as players.csv

### 6.3 Write weekly folders
- [ ] Create `weeks/` subfolder
- [ ] Create `week_01/` through `week_17/` subfolders
- [ ] Write `players.csv` and `players_projected.csv` to each
- [ ] Validate output (17 folders, 2 files each)

---

## Phase 7: Main Script Integration

### 7.1 Orchestrate data compilation
- [ ] Create main compilation workflow in `compile_historical_data.py`
- [ ] Execute fetchers in order:
  1. Fetch schedule data
  2. Fetch game data + weather
  3. Fetch player data (all positions, all weeks)
  4. Calculate team data
  5. Generate weekly snapshots
- [ ] Add progress logging
- [ ] Implement fail-loud error handling

### 7.2 Add validation and reporting
- [ ] Validate all output files exist
- [ ] Report row counts and file sizes
- [ ] Validate data integrity (e.g., all teams present, correct week counts)
- [ ] Print summary when complete

---

## Phase 8: Testing (per Q7: Unit + Fixture Tests)

### 8.1 Create unit tests with fixtures
- [ ] Create `tests/historical_data_compiler/` directory
- [ ] Create `tests/historical_data_compiler/fixtures/` for API response fixtures
- [ ] Save sample ESPN API responses as JSON fixtures
- [ ] Save sample Open-Meteo responses as JSON fixtures
- [ ] Write tests for each module:
  - `test_schedule_fetcher.py` - with schedule fixture
  - `test_game_data_fetcher.py` - with game/venue fixture
  - `test_weather_fetcher.py` - with weather fixture
  - `test_espn_fantasy_client.py` - with player data fixture
  - `test_team_data_calculator.py` - with player points fixture
  - `test_weekly_snapshot_generator.py` - with full data fixture
- [ ] Mock external API calls using fixtures
- [ ] Test edge cases (bye weeks, DST negative scores, indoor games)

### 8.2 Create fixture-based integration tests
- [ ] Test full compilation workflow with fixture data
- [ ] Validate output structure matches specification
- [ ] Test 2024 season data structure (not live API)

### 8.3 Run full test suite
- [ ] Run `python tests/run_all_tests.py`
- [ ] Ensure 100% pass rate
- [ ] Fix any failing tests

**Testing Strategy** (per Q7):
- Unit tests mock all API calls
- Fixtures provide realistic API response patterns
- No network dependency in CI
- Fixtures stored in `tests/historical_data_compiler/fixtures/`

---

## Phase 9: Documentation and Finalization

### 9.1 Update documentation
- [ ] Add usage instructions to README.md
- [ ] Document command-line arguments
- [ ] Document output file formats
- [ ] Update CLAUDE.md if needed

### 9.2 Final validation
- [ ] Run script for 2024 season: `python compile_historical_data.py --year 2024`
- [ ] Verify output structure matches specification
- [ ] Spot-check specific players/weeks for accuracy
- [ ] Run full test suite one final time

### 9.3 Cleanup
- [ ] Move `updates/historical-data-compiler/` files to `updates/done/`
- [ ] Delete questions file (after user answers integrated)
- [ ] Verify all TODO items complete

---

## Verification Summary

**Status**: READY FOR IMPLEMENTATION ✓

**Iterations Completed**: 16/16 (ALL COMPLETE)

### User Answers Integrated:

| Question | Choice | Decision |
|----------|--------|----------|
| Q1: Module Structure | Option 1 | Multi-module `historical_data_compiler/` folder |
| Q2: Code Reuse | Option 2 | Copy and adapt from existing code |
| Q3: Rate Limiting | Option 3 | Adaptive throttling with tenacity |
| Q4: Error Handling | Option 1 | Fail completely on any error |
| Q5: Multi-Year | Option 1 | Single year only (`--year 2024`) |
| Q6: Output Location | Option 1 | `simulation/sim_data/{YEAR}/` |
| Q7: Testing | Option 3 | Unit tests + fixture tests |

### Iteration 1-4 Findings:

**Existing Patterns Identified:**
- `player-data-fetcher/player_data_constants.py` - ESPN_TEAM_MAPPINGS (32 teams), ESPN_POSITION_MAPPINGS (6 positions)
- `player-data-fetcher/espn_client.py:1407-1493` - Team weekly data collection algorithm
- `player-data-fetcher/game_data_fetcher.py` - ESPN Scoreboard + Open-Meteo weather API patterns
- `schedule-data-fetcher/ScheduleFetcher.py` - Schedule fetching from ESPN API
- `player-data-fetcher/coordinates.json` - Stadium lat/lon for weather lookups

**File Format Verification:**
- `season_schedule.csv` - 3 columns (week, team, opponent)
- `game_data.csv` - 14 columns (matches spec)
- `team_data/{TEAM}.csv` - 8 columns (week + 7 stats), bye weeks show 0s
- `players_actual.csv` - All required fields present

**Key Decisions Confirmed:**
- This is a STANDALONE script - no modification to existing simulation code needed
- Simulation system update is OUT OF SCOPE (future effort per README)
- Indoor games have empty weather fields (not "None" string)
- International games have empty state field
- Position filtering happens after API fetch (via defaultPositionId)

---

## Progress Notes

> Add notes here as you progress through implementation. Document any blockers, decisions, or changes from the original plan.

### Research Notes:
- ESPN uses `defaultPositionId` for position mapping: QB=1, RB=2, WR=3, TE=4, K=5, DST=16
- ESPN uses `slotId` for ranking slots: QB=0, RB=2, WR=4, TE=6, K=17, DST=16 (different!)
- X-Fantasy-Filter uses JSON syntax like `{"players":{"limit":1000,"sortPercOwned":{...}}}`
- Team data algorithm skips DST position (only QB/RB/WR/TE/K tracked)

---

## Integration Checklist

This is a **standalone script** - no caller modifications needed.

| New Component | File | Called By | Notes |
|---------------|------|-----------|-------|
| `compile_historical_data.py` | Root level | User CLI | Entry point, no callers to modify |
| `historical_data_compiler/schedule_fetcher.py` | New module | compile_historical_data.py | Internal to new script |
| `historical_data_compiler/game_data_fetcher.py` | New module | compile_historical_data.py | Internal to new script |
| `historical_data_compiler/espn_fantasy_client.py` | New module | compile_historical_data.py | Internal to new script |
| `historical_data_compiler/team_data_calculator.py` | New module | compile_historical_data.py | Internal to new script |
| `historical_data_compiler/weekly_snapshot_generator.py` | New module | compile_historical_data.py | Internal to new script |

**No integration with existing code required** - this creates data files that a future project will consume.

---

## Integration Gap Check (Iteration 14 - Second Round)

### New Component → Caller Matrix (Standalone Script):

| New Component | File | Called By | Integration Status |
|---------------|------|-----------|-------------------|
| `compile_historical_data.py` | Root | User CLI | ✅ Entry point - no caller needed |
| `schedule_fetcher.py` | `historical_data_compiler/` | `compile_historical_data.py` | ✅ Will be imported |
| `game_data_fetcher.py` | `historical_data_compiler/` | `compile_historical_data.py` | ✅ Will be imported |
| `espn_fantasy_client.py` | `historical_data_compiler/` | `compile_historical_data.py` | ✅ Will be imported |
| `team_data_calculator.py` | `historical_data_compiler/` | `compile_historical_data.py` | ✅ Will be imported |
| `weekly_snapshot_generator.py` | `historical_data_compiler/` | `compile_historical_data.py` | ✅ Will be imported |
| `constants.py` | `historical_data_compiler/` | All modules | ✅ Shared constants |
| `http_client.py` | `historical_data_compiler/` | All fetchers | ✅ Shared HTTP client |

### Orphan Code Check:
- ✅ No orphan code - all modules called from main script
- ✅ Standalone script - no existing code modifications needed
- ✅ Output files consumed by future simulation update (out of scope)

### Entry Script File Discovery:
- ✅ Not applicable - this is a NEW entry script
- ✅ No existing scripts need to find historical data compiler output (simulation update is future work)

---

## Skeptical Re-Verification Results (Iteration 6)

### Verified Correct:
- ✅ ESPN Scoreboard API endpoint in codebase: `site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- ✅ ESPN Fantasy API endpoint in codebase: `lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{YEAR}/segments/0/leaguedefaults/3`
- ✅ `players_actual.csv` has 28 columns (11 base + 17 weeks)
- ✅ `game_data.csv` has 14 columns
- ✅ `season_schedule.csv` has 545 rows (544 data + 1 header = 32 teams × 17 weeks)
- ✅ Team data algorithm exists at `espn_client.py:1407-1493`
- ✅ ESPN_TEAM_MAPPINGS has 32 teams
- ✅ ESPN_POSITION_MAPPINGS has 6 positions
- ✅ coordinates.json exists in `player-data-fetcher/`

### Corrected During Verification:
- None - all documented patterns verified correctly

### Confidence Level: HIGH
All claims verified against actual codebase. Patterns match documented sources.

---

## Skeptical Re-Verification Results (Iteration 13 - Second Round)

### Re-Verified with User Answers:
- ✅ Multi-module structure matches project patterns (Q1)
- ✅ Copy-and-adapt approach is appropriate - historical needs differ from live (Q2)
- ✅ Tenacity retry pattern exists at `espn_client.py:117` - confirmed (Q3)
- ✅ Fail-completely matches original spec requirement (Q4)
- ✅ Output location `simulation/sim_data/{YEAR}/` matches spec (Q6)
- ✅ 32 team data files confirmed in current sim_data
- ✅ Team data files have 18 rows (1 header + 17 weeks)
- ✅ Team data header: `week,pts_allowed_to_QB,pts_allowed_to_RB,pts_allowed_to_WR,pts_allowed_to_TE,pts_allowed_to_K,points_scored,points_allowed`

### No Corrections Needed
User answers align with codebase patterns and original specification.

---

## Data Flow Traces

### Entry Point → Output (Updated with User Decisions)
```
User runs: python compile_historical_data.py --year 2024

compile_historical_data.py (entry point, per Q5: single year only)
  │
  ├─→ Validate year >= 2021
  ├─→ Create output folder: simulation/sim_data/2024/ (per Q6)
  │
  ├─→ [1] historical_data_compiler.schedule_fetcher.fetch_schedule(year=2024)
  │     └─→ ESPN Scoreboard API (weeks 1-17)
  │     └─→ Adaptive throttling with tenacity (per Q3)
  │     └─→ Output: simulation/sim_data/2024/season_schedule.csv
  │
  ├─→ [2] historical_data_compiler.game_data_fetcher.fetch_game_data(year=2024)
  │     ├─→ ESPN Scoreboard API (scores, venues)
  │     └─→ Open-Meteo API (weather for outdoor games)
  │     └─→ Output: simulation/sim_data/2024/game_data.csv
  │
  ├─→ [3] historical_data_compiler.espn_fantasy_client.fetch_all_player_data(year=2024)
  │     └─→ ESPN Fantasy API (all positions, all weeks)
  │     └─→ Returns: player_data dict with actuals + projections
  │
  ├─→ [4] historical_data_compiler.team_data_calculator.calculate_team_data(players, schedule)
  │     └─→ Copied algorithm from espn_client.py:1407-1493
  │     └─→ Output: simulation/sim_data/2024/team_data/{32 files}
  │
  ├─→ [5] historical_data_compiler.weekly_snapshot_generator.generate_all_weeks(...)
  │     └─→ For each week 1-17:
  │          └─→ Output: simulation/sim_data/2024/weeks/week_NN/players.csv
  │          └─→ Output: simulation/sim_data/2024/weeks/week_NN/players_projected.csv
  │
  └─→ ERROR HANDLING (per Q4: fail completely):
        └─→ Any exception → cleanup partial files, log error, exit(1)
```

### Output Structure Verification:
```
simulation/sim_data/2024/
├── season_schedule.csv       # 544 rows (32 teams × 17 weeks)
├── game_data.csv             # ~272 rows (16-17 games × 17 weeks)
├── team_data/                # 32 files
│   ├── ARI.csv               # 17 rows (one per week)
│   ├── ATL.csv
│   └── ... (30 more)
└── weeks/                    # 17 folders
    ├── week_01/
    │   ├── players.csv       # ~500+ players
    │   └── players_projected.csv
    ├── week_02/
    └── ... (15 more)
```

---

## Integration Verification Checklist (For Implementation Phase)

Use this checklist during implementation to verify each component is properly integrated:

### Phase 1: Core Infrastructure
- [ ] `compile_historical_data.py` created at root
- [ ] `historical_data_compiler/` module folder created
- [ ] `historical_data_compiler/__init__.py` created
- [ ] `historical_data_compiler/constants.py` - copied from player_data_constants.py
- [ ] `historical_data_compiler/http_client.py` - copied from espn_client.py
- [ ] Entry point tested: `python compile_historical_data.py --help`

### Phase 2: Schedule Fetcher
- [ ] `schedule_fetcher.py` created
- [ ] Imported and called from main script
- [ ] Unit tests with fixtures pass
- [ ] Output verified: `season_schedule.csv` has 544 rows

### Phase 3: Game Data Fetcher
- [ ] `game_data_fetcher.py` created
- [ ] Weather integration working (Open-Meteo)
- [ ] Indoor games have empty weather fields
- [ ] Output verified: `game_data.csv` has 14 columns

### Phase 4: Player Data Fetcher
- [ ] `espn_fantasy_client.py` created
- [ ] All 6 positions fetched (QB, RB, WR, TE, K, DST)
- [ ] Actuals (statSourceId=0) and projections (statSourceId=1) both working
- [ ] Player filtering by activity working

### Phase 5: Team Data Calculator
- [ ] `team_data_calculator.py` created
- [ ] Algorithm copied from espn_client.py:1407-1493
- [ ] Output verified: 32 files in `team_data/`, each with 17 rows

### Phase 6: Weekly Snapshot Generator
- [ ] `weekly_snapshot_generator.py` created
- [ ] players.csv logic: past=actuals, future=projections
- [ ] players_projected.csv logic: all projections
- [ ] Output verified: 17 folders with 2 files each

### Phase 7: Final Integration
- [ ] Full compilation tested: `python compile_historical_data.py --year 2024`
- [ ] All output files exist and have correct row counts
- [ ] Error handling tested: script fails completely on API error

### Phase 8: Testing
- [ ] `tests/historical_data_compiler/` directory created
- [ ] `tests/historical_data_compiler/fixtures/` with API response fixtures
- [ ] All unit tests pass: `python tests/run_all_tests.py`
- [ ] 100% pass rate achieved

### Phase 9: Documentation
- [ ] README.md updated with usage instructions
- [ ] CLAUDE.md updated if needed
- [ ] Code changes documented

---

## Risk Assessment (Iterations 15-16)

### Low Risk:
- Module structure is well-defined
- Existing code patterns are clear
- API endpoints are verified
- No integration with existing code needed

### Medium Risk:
- ESPN API rate limiting (mitigated by adaptive throttling)
- Historical data availability (verified for 2021+)
- Weather API for old games (Open-Meteo Archive verified)

### Mitigations:
- Tenacity retry with exponential backoff
- Fail-completely approach ensures data integrity
- Fixture tests don't depend on network

---
