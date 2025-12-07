# Game Data Fetcher - TODO File

**Objective**: Create game_data.csv file with NFL game information (including weather from Open-Meteo) and 2024 simulation data.

**Status**: DRAFT - Starting verification iterations

**Source File**: `updates/game_data_fetcher.txt`

---

## Progress Tracking

> **IMPORTANT**: Keep this file updated with progress. If a new Claude agent continues this work, they should be able to pick up exactly where the previous agent left off.

- [x] Draft TODO created
- [x] First verification round (5 iterations) completed
- [x] Questions file created (`updates/game_data_fetcher_questions.md`)
- [x] User answers received (all 5 questions answered)
- [x] Second verification round (7 iterations) completed
- [ ] Implementation started
- [ ] All phases complete
- [ ] All tests pass (100%)
- [ ] Documentation updated
- [ ] Objective complete

---

## Part 1: Core Infrastructure

### Phase 1: Create Data Models and Coordinates Manager

**1.1 Create game_data_models.py**
- [ ] Create `player-data-fetcher/game_data_models.py`
- [ ] Define `GameData` Pydantic model with 13 columns:
  - week (int), home_team (str), away_team (str)
  - temperature (Optional[int]), gust (Optional[int]), precipitation (Optional[float])
  - home_team_score (Optional[int]), away_team_score (Optional[int])
  - indoor (bool), neutral_site (bool)
  - country (str), city (str), state (Optional[str])
  - date (str - ISO 8601)
- [ ] Add `model_config` for JSON serialization
- [ ] Add `to_csv_row()` method
- [ ] Add `from_espn_data()` class method
- [ ] Follow patterns from `player_data_models.py`

**1.2 Create coordinates_manager.py**
- [ ] Create `player-data-fetcher/coordinates_manager.py`
- [ ] Implement `CoordinatesManager` class with methods:
  - `__init__(coordinates_file: Path)` - Load or create JSON
  - `_load_coordinates() -> dict` - Load from file
  - `_save_coordinates()` - Save with indent=2
  - `get_nfl_stadium(team_abbrev: str) -> Optional[dict]`
  - `get_international_venue(city: str, country: str) -> Optional[dict]`
  - `get_or_fetch_coordinates(...)` - Main lookup with API fallback
  - `_fetch_coordinates_from_api(city, country) -> Optional[dict]`
- [ ] Use httpx for geocoding API calls
- [ ] Add proper logging with `get_logger()`
- [ ] Handle API errors gracefully (return None, log warning)

**1.3 Create coordinates.json**
- [ ] Create `player-data-fetcher/coordinates.json`
- [ ] Pre-populate all 32 NFL stadiums with:
  - lat, lon, tz, name (NO indoor flag - use ESPN API instead)
- [ ] Structure: `{"nfl_stadiums": {...}, "international_venues": {}}`
- [ ] International venues added dynamically via geocoding API

**1.4 Update config.py**
- [ ] Add `GAME_DATA_CSV = "game_data.csv"`
- [ ] Add `COORDINATES_JSON = "coordinates.json"`
- [ ] Add `ENABLE_GAME_DATA_FETCH = True` flag

### Phase 2: API Clients and Weather Fetching

**2.1 Create game_data_fetcher.py - Weather Functions (Dual-API)**
- [ ] Create `player-data-fetcher/game_data_fetcher.py`
- [ ] Implement `fetch_weather_for_game()` function:
  - Parameters: coords_manager, home_team, game_date, is_international, city, country
  - Returns: dict with temperature, gust, precipitation (or None for indoor)
- [ ] Parse ISO 8601 date for Open-Meteo query
- [ ] **Implement dual-API date routing:**
  - Games >5 days old → Historical API (`archive-api.open-meteo.com/v1/archive`)
  - Recent/upcoming games → Forecast API (`api.open-meteo.com/v1/forecast`)
- [ ] Build Open-Meteo request with correct units (F, mph, inches)
- [ ] Handle indoor games (return None values) - use ESPN venue.indoor flag
- [ ] Use **sync httpx** (not async)

**2.2 Create ESPN Scoreboard Parser**
- [ ] Implement `fetch_games_for_week(week: int, season: int)` function
- [ ] Build ESPN Scoreboard API URL with params
- [ ] Parse response to extract:
  - Home/away teams (abbreviations)
  - Venue info (city, state, country, indoor)
  - Neutral site flag
  - Game date (ISO 8601)
  - Scores (if completed)
- [ ] Handle team abbreviation mapping
- [ ] Use rate limiting (0.2s delay)

**2.3 Create Game Data Builder**
- [ ] Implement `build_game_data()` function
- [ ] Combine ESPN data with weather data
- [ ] Determine international game status
- [ ] Construct `GameData` model instance

### Phase 3: Main Fetcher Logic

**3.1 Create GameDataFetcher Class**
- [ ] Implement `GameDataFetcher` class in `game_data_fetcher.py`
- [ ] `__init__(data_folder: Path, season: int)` - Initialize paths
- [ ] `_load_existing_data() -> List[GameData]` - Load from CSV
- [ ] `_get_existing_weeks() -> Set[int]` - Get weeks already fetched
- [ ] `_determine_weeks_to_fetch() -> List[int]` - Missing weeks
- [ ] `fetch_all() -> List[GameData]` - Main orchestration
- [ ] `save_to_csv(games: List[GameData]) -> Path` - Write CSV
- [ ] `save_to_historical(games: List[GameData])` - Copy to historical

**3.2 Implement Week Detection Logic**
- [ ] Read existing game_data.csv if exists
- [ ] Parse to get set of weeks with data
- [ ] Compare with CURRENT_NFL_WEEK from config
- [ ] Return list of weeks needing fetch

**3.3 Implement Score Backfill Logic**
- [ ] Create `backfill_previous_week_scores()` method
- [ ] Check week (CURRENT_NFL_WEEK - 1)
- [ ] Find games with None scores
- [ ] Re-fetch from ESPN to get completed scores
- [ ] Update data and mark for save

**3.4 Implement CSV I/O**
- [ ] Use pandas for reading/writing
- [ ] Handle None values (empty string in CSV)
- [ ] Column order: week, home_team, away_team, temperature, gust, precipitation, home_team_score, away_team_score, indoor, neutral_site, country, city, state, date
- [ ] Follow utils/csv_utils.py patterns

**3.5 Implement Historical Data Saving**
- [ ] Check if `data/historical_data/{Season}/{WeekNumber}/` exists
- [ ] If not, create folder and copy game_data.csv
- [ ] If exists, skip
- [ ] Follow pattern from player_data_exporter.py

### Phase 4: Integration

**4.1 Update player_data_fetcher_main.py**
- [ ] Import GameDataFetcher
- [ ] Add game data fetch to NFLProjectionsCollector workflow
- [ ] Make conditional on ENABLE_GAME_DATA_FETCH config
- [ ] Handle errors gracefully (don't fail player fetch)

**4.2 Create Root-Level Runner (Optional)**
- [ ] Create `run_game_data_fetcher.py` in project root
- [ ] Support `--season` argument for 2024 data
- [ ] Support `--output` for custom output path
- [ ] Follow pattern from `run_player_fetcher.py`

---

## Part 2: 2024 Simulation Data

### Phase 5: Generate 2024 Season Data

**5.1 Fetch 2024 Game Data**
- [ ] Run fetcher with `--season 2024`
- [ ] Fetch all 18 weeks of 2024 regular season
- [ ] Verify all games have scores (complete season)
- [ ] Verify weather populated for outdoor games
- [ ] Save to `simulation/sim_data/game_data.csv`

**5.2 Validate 2024 Data**
- [ ] Check ~272 games present
- [ ] No None scores
- [ ] Indoor games have None weather
- [ ] Outdoor games have weather data

---

## Part 3: Testing

### Phase 6: Unit Tests

**6.1 Test game_data_models.py**
- [ ] Create `tests/player-data-fetcher/test_game_data_models.py`
- [ ] Test GameData model creation
- [ ] Test optional fields as None
- [ ] Test to_csv_row() method
- [ ] Test from_espn_data() class method
- [ ] Test JSON serialization

**6.2 Test coordinates_manager.py**
- [ ] Create `tests/player-data-fetcher/test_coordinates_manager.py`
- [ ] Test loading from existing JSON
- [ ] Test creating new JSON when none exists
- [ ] Test get_nfl_stadium() cache hit
- [ ] Test get_international_venue() cache hit
- [ ] Test API fallback for unknown venues (mock API)
- [ ] Test saving after API lookup
- [ ] Test handling geocoding API errors
- [ ] Test handling malformed JSON file

**6.3 Test game_data_fetcher.py**
- [ ] Create `tests/player-data-fetcher/test_game_data_fetcher.py`
- [ ] Test _load_existing_data() with CSV
- [ ] Test _load_existing_data() with no CSV
- [ ] Test _get_existing_weeks() extraction
- [ ] Test _determine_weeks_to_fetch() logic
- [ ] Test backfill_previous_week_scores() (mock ESPN)
- [ ] Test fetch_all() orchestration
- [ ] Test save_to_csv() output format
- [ ] Test save_to_historical()
- [ ] Test weather fetch for outdoor games (mock Open-Meteo)
- [ ] Test weather skip for indoor games
- [ ] Test international venue handling
- [ ] Test API error handling

**6.4 Run All Tests**
- [ ] Run `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Fix any failing tests
- [ ] Ensure no regressions

---

## Part 4: Documentation

### Phase 7: Documentation Updates

**7.1 Update README.md**
- [ ] Add section on game data fetcher
- [ ] Document game_data.csv format
- [ ] Add usage examples

**7.2 Update CLAUDE.md**
- [ ] Add new files to project structure
- [ ] Update data fetchers section

**7.3 Create Code Changes Documentation**
- [ ] Create `updates/game_data_fetcher_code_changes.md`
- [ ] Document all new files
- [ ] Document modified files
- [ ] Include before/after snippets

**7.4 Final Cleanup**
- [ ] Run full test suite
- [ ] Move `updates/game_data_fetcher.txt` to `updates/done/`
- [ ] Delete questions file
- [ ] Commit with descriptive message

---

## Verification Summary

### First Verification Round (5 iterations)
- Iterations completed: 5/5
- Skeptical re-verification (iteration 5): COMPLETE

**Iteration 1 Findings:**
- ✅ Verified config.py location and structure (lines 1-88)
- ✅ Verified player_data_models.py Pydantic patterns (lines 1-149)
- ✅ Verified ESPN scoreboard API usage in espn_client.py (lines 1081, 1154, 1232)
- ✅ Verified team abbreviation mapping in player_data_constants.py (lines 16-23)
- ✅ Verified save_to_historical_data() pattern in player_data_fetcher_main.py (lines 363-429)
- ✅ Verified run_player_fetcher.py runner script pattern (lines 1-52)
- ✅ Verified test file structure in tests/player-data-fetcher/

**Codebase Patterns Identified:**
1. Pydantic models use `Field(default_factory=...)` for default values
2. ESPN API parsing uses `event.get('competitions', [])[0]` pattern
3. Team abbreviation mapping: WAS → WSH handled in ESPN parsing
4. Historical data path: `data/historical_data/{Season}/{WeekNumber:02d}/`
5. Tests use `sys.path.append()` for imports
6. Config imports are from relative path

**Questions Identified for User:**
1. Should game_data_fetcher use async (like ESPN client) or sync (for simpler implementation)?
2. Should we add a standalone `run_game_data_fetcher.py` script?
3. Should indoor flag come from coordinates.json or ESPN API?

**Iteration 2 Findings (Deep Dive):**
- ✅ Verified BaseAPIClient pattern for HTTP requests (espn_client.py:52-176)
- ✅ Verified httpx + tenacity retry pattern (lines 117-176)
- ✅ Verified custom exceptions pattern (ESPNAPIError, ESPNRateLimitError, ESPNServerError)
- ✅ Verified csv_utils.py patterns: read_csv_with_validation, write_csv_with_backup, write_dict_csv
- ✅ Verified async write pattern: write_csv_async uses run_in_executor
- ✅ Verified safe_csv_read with @handle_errors decorator

**Error Handling Patterns:**
1. Custom exceptions for specific error types (API errors, file errors)
2. Use error_context() context manager for structured logging
3. Log errors before raising with logger.error()
4. Graceful degradation with default values where appropriate

**CSV I/O Patterns:**
1. Use Path objects for file paths
2. Validate columns before reading with validate_csv_columns()
3. Create parent directories with mkdir(parents=True, exist_ok=True)
4. Backup existing files before overwriting (write_csv_with_backup)

**Additional Questions:**
4. Should we use sync httpx for simplicity since game fetching is infrequent?
5. Which Open-Meteo API should we use (Historical, Forecast, or both)?

**User Answers Received (ALL):**
- Q1: **Sync HTTP** - use sync httpx for simplicity
- Q2: **Yes** - both standalone script AND integrated into player_data_fetcher
- Q3: **ESPN API only** for indoor flag - remove indoor from coordinates.json
- Q4: **Yes** - use dual-API approach (Historical + Forecast)
- Q5: **Yes** - fetch all 18 weeks for 2024 simulation data

**Iteration 3 Findings (Integration Points):**
- ✅ Verified historical data structure: `data/historical_data/2025/{WeekNumber:02d}/`
- ✅ Confirmed week folders contain: players.csv, players_projected.csv, team_data/
- ✅ Verified simulation data location: `simulation/sim_data/` (season_schedule.csv, players_*.csv, team_data/)
- ✅ Confirmed game_data.csv should go in both: `data/game_data.csv` and `simulation/sim_data/game_data.csv`
- ✅ Verified save_to_historical_data() pattern uses shutil.copy2 and shutil.copytree

**Integration Points:**
1. **Historical saving**: Add game_data.csv to files_to_copy list in save_to_historical_data()
2. **Main workflow**: Add game data fetch after player data collection in collect_all_projections()
3. **Config**: Add GAME_DATA_CSV and COORDINATES_JSON constants
4. **Simulation data**: 2024 game data goes to simulation/sim_data/game_data.csv

**Data Flow:**
```
ESPN Scoreboard API → Parse games → Open-Meteo API → Weather data
                                  → CoordinatesManager → Geocoding API (if needed)
                                  → GameData model → game_data.csv
```

**Iteration 4 Findings (Technical Details):**

**ESPN Scoreboard API Response Structure:**
```json
{
  "events": [{
    "date": "2024-09-05T00:20Z",  // ISO 8601
    "competitions": [{
      "neutralSite": true/false,
      "venue": {
        "fullName": "Arrowhead Stadium",
        "address": {
          "city": "Kansas City",
          "state": "MO",
          "country": "USA"
        },
        "indoor": true/false
      },
      "competitors": [{
        "homeAway": "home",
        "score": "27",  // STRING not int!
        "team": {"abbreviation": "KC"}
      }],
      "status": {"type": {"completed": true/false}}
    }]
  }]
}
```

**Open-Meteo Weather APIs (TWO endpoints):**

| API | Endpoint | Time Coverage |
|-----|----------|---------------|
| **Historical** | `archive-api.open-meteo.com/v1/archive` | 1940 to 5 days ago |
| **Forecast** | `api.open-meteo.com/v1/forecast` | Past 92 days to 16 days ahead |

- Parameters: `latitude`, `longitude`, `start_date`, `end_date` (or `past_days`, `forecast_days`)
- Hourly vars: `temperature_2m,wind_gusts_10m,precipitation`
- Units: `temperature_unit=fahrenheit`, `wind_speed_unit=mph`, `precipitation_unit=inch`
- Response: `hourly.time[]`, `hourly.temperature_2m[]`, `hourly.wind_gusts_10m[]`, `hourly.precipitation[]`

**Implementation**: Check game date and route to appropriate API:
- Games >5 days old → Historical API (more accurate reanalysis data)
- Recent games (last 5 days) → Forecast API with `past_days`
- Upcoming games (next 16 days) → Forecast API with `forecast_days`

**Key Implementation Notes:**
1. ESPN score is STRING - must convert to int()
2. ESPN date is already ISO 8601 format
3. neutralSite=true does NOT mean international (could be Super Bowl)
4. International = neutralSite AND country != "USA"
5. Open-Meteo hourly array indexed by hour (0-23)

**Iteration 5 - SKEPTICAL RE-VERIFICATION:**

**Re-verified Requirements (CONFIRMED):**
- ✅ 13 columns (not 15 - no grass column): week, home_team, away_team, temperature, gust, precipitation, home_team_score, away_team_score, indoor, neutral_site, country, city, state, date
- ✅ coordinates.json in player-data-fetcher/ with dynamic geocoding fallback
- ✅ run_game_data_fetcher.py with --season and --output arguments (per spec line 469)
- ✅ Need BOTH test_game_data_fetcher.py AND test_game_data_models.py (per spec lines 423, 499)
- ✅ Historical data path uses zero-padded week: `{WeekNumber:02d}` (verified in main.py:384)

**Potential Issues Found:**
1. ⚠️ Current espn_client.py does NOT parse venue info - verified with grep
2. ⚠️ indoor flag from ESPN API needs verification (specified but not currently parsed)
3. ⚠️ Spec says "Indoor" but ESPN returns "indoor" (lowercase) - need to verify
4. ⚠️ coordinates.json "indoor" field may conflict with ESPN's indoor flag

**Critical Corrections to TODO:**
1. Need to add test_game_data_models.py (was missing from Phase 6)
2. Need to explicitly verify run_game_data_fetcher.py is in project root (line 147)
3. Indoor flag source: use coordinates.json for NFL teams (more reliable), ESPN for international

**Confidence Level:** HIGH - All file paths verified, API structures confirmed via web fetch

### Second Verification Round (7 iterations)
- Iterations completed: 7/7
- Skeptical re-verification (iteration 10): COMPLETE
- Final refinement (iterations 11-12): COMPLETE

**Iteration 6 Findings (Post-Questions - Incorporate User Answers):**

Updates based on user answers:
1. ✅ Use **sync httpx** (not async) - simpler implementation
2. ✅ Create **both** standalone script AND integrate into player_data_fetcher
3. ✅ Remove indoor flag from coordinates.json - use **ESPN API only**
4. ✅ Implement **dual Open-Meteo API** approach (Historical + Forecast)
5. ✅ Fetch **weeks 1-18** for 2024 simulation data

**TODO Updates Required:**
- Phase 2.1: Update weather fetching to use dual-API with date-based routing ✅
- Phase 1.3: Remove indoor field from coordinates.json structure ✅
- Phase 4.2: Confirm standalone script is created (run_game_data_fetcher.py) ✅

**Iteration 7 Findings (Deep Dive with Answers):**

**Spec vs User Answer Discrepancies (to note during implementation):**
1. Spec line 343 uses `coords.get("indoor")` but user said use ESPN API
2. Spec coordinates.json example (lines 211-242) still has indoor field
3. Implementation should pass indoor flag from ESPN to weather function, not coordinates

**Weather Function Signature Update:**
```python
def fetch_weather_for_game(
    coords_manager: CoordinatesManager,
    home_team: str,
    game_date: str,
    is_indoor: bool,  # From ESPN API, not coordinates.json
    is_international: bool,
    city: str,
    country: str
) -> dict:
```

**Iteration 8 Findings (Integration with Answers):**

**Sync HTTP Implementation Pattern:**
```python
import httpx

def fetch_espn_scoreboard(week: int, season: int) -> dict:
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    params = {"seasontype": 2, "week": week, "dates": season}
    response = httpx.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
```

**Dual Open-Meteo API Pattern:**
```python
from datetime import datetime, timedelta

def get_weather_api_endpoint(game_date: str) -> str:
    game_dt = datetime.fromisoformat(game_date.replace('Z', '+00:00'))
    five_days_ago = datetime.now(timezone.utc) - timedelta(days=5)

    if game_dt < five_days_ago:
        return "https://archive-api.open-meteo.com/v1/archive"
    else:
        return "https://api.open-meteo.com/v1/forecast"
```

**Iteration 9 Findings (Implementation-Specific Details):**

**File Creation Order:**
1. coordinates.json (with stadium data, NO indoor flag)
2. game_data_models.py (Pydantic GameData model)
3. coordinates_manager.py (coordinate lookups)
4. game_data_fetcher.py (main fetcher logic)
5. Update config.py (add constants)
6. Update player_data_fetcher_main.py (integration)
7. Create run_game_data_fetcher.py (standalone script)

**Standalone Script Arguments:**
```python
# run_game_data_fetcher.py
parser = argparse.ArgumentParser()
parser.add_argument('--season', type=int, default=2025)
parser.add_argument('--output', type=str, default='data/game_data.csv')
parser.add_argument('--weeks', type=str, help='e.g., "1-18" or "1,5,10"')
```

**Iteration 10 - SKEPTICAL RE-VERIFICATION (Second Round):**

**Final Checklist - All User Answers Incorporated:**
- ✅ Sync HTTP: Using httpx.get() not async
- ✅ Standalone + Integrated: Both run_game_data_fetcher.py AND integration in main
- ✅ ESPN API for indoor: Removed from coordinates.json, pass from ESPN venue.indoor
- ✅ Dual Open-Meteo: Historical for >5 days, Forecast for recent/upcoming
- ✅ 2024 weeks 1-18: Full season for simulation data

**Potential Edge Cases to Handle:**
1. Game in progress (not completed but has partial scores)
2. Postponed/cancelled games
3. Games >16 days in future (outside Forecast API range)
4. Geocoding API returns no results for international venue
5. ESPN API returns different team abbreviation format

**Test Coverage Requirements:**
- Unit tests for each new file (3 test files)
- Mock all external APIs (ESPN, Open-Meteo Historical, Open-Meteo Forecast, Geocoding)
- Test date routing logic for dual-API
- Test CSV I/O with None values
- Test score backfill logic

**Confidence Level:** HIGH - Ready for implementation

**Iteration 11-12 - FINAL REFINEMENT:**

**Implementation Ready Checklist:**
- ✅ All 5 user questions answered and incorporated
- ✅ 12 verification iterations complete (5 first round + 7 second round)
- ✅ All TODO tasks defined with clear acceptance criteria
- ✅ API endpoints and response formats verified
- ✅ File paths and patterns verified against codebase
- ✅ Edge cases identified for testing
- ✅ Test file structure defined

**Final Implementation Summary:**

| Component | File | Status |
|-----------|------|--------|
| Pydantic Model | game_data_models.py | Ready |
| Coordinates Manager | coordinates_manager.py | Ready |
| Coordinates Data | coordinates.json | Ready (no indoor flag) |
| Main Fetcher | game_data_fetcher.py | Ready (sync, dual-API) |
| Config Updates | config.py | Ready |
| Integration | player_data_fetcher_main.py | Ready |
| Standalone Script | run_game_data_fetcher.py | Ready |
| Tests | 3 test files | Ready |

**VERIFICATION COMPLETE - READY FOR IMPLEMENTATION**

---

## Notes

### Key Technical Details (from specification)

**Data Sources:**
- ESPN Scoreboard API: teams, scores, venue, indoor, neutral_site, date
- Open-Meteo Historical API: temperature, wind gusts, precipitation
- Open-Meteo Geocoding API: coordinates for unknown venues

**13 CSV Columns:**
1. week (int)
2. home_team (str)
3. away_team (str)
4. temperature (int or None) - Fahrenheit
5. gust (int or None) - mph
6. precipitation (float or None) - inches
7. home_team_score (int or None)
8. away_team_score (int or None)
9. indoor (bool)
10. neutral_site (bool)
11. country (str)
12. city (str)
13. state (str or None)
14. date (str - ISO 8601)

**Open-Meteo Weather APIs:**
- **Historical API**: `https://archive-api.open-meteo.com/v1/archive` (1940 to 5 days ago)
- **Forecast API**: `https://api.open-meteo.com/v1/forecast` (past 92 days to 16 days ahead)
- No API key required
- 10,000 calls/day free tier
- Use dual-API approach: Historical for old games, Forecast for recent/upcoming

**Open-Meteo Geocoding API:**
- Endpoint: `https://geocoding-api.open-meteo.com/v1/search`
- No API key required
- Used for unknown international venues

**Coordinates Storage:**
- File: `player-data-fetcher/coordinates.json`
- Pre-populated: 32 NFL stadiums (lat, lon, tz, name - NO indoor flag)
- Dynamically added: International venues via geocoding API
- Indoor flag: Use ESPN API venue.indoor instead of coordinates.json

**New Files:**
- `player-data-fetcher/game_data_fetcher.py`
- `player-data-fetcher/game_data_models.py`
- `player-data-fetcher/coordinates_manager.py`
- `player-data-fetcher/coordinates.json`
- `data/game_data.csv`
- `simulation/sim_data/game_data.csv`

**Modified Files:**
- `player-data-fetcher/config.py`
- `player-data-fetcher/player_data_fetcher_main.py`
