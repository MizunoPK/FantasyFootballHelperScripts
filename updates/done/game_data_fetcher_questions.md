# Game Data Fetcher - Questions for User Clarification

**Source Specification**: `updates/game_data_fetcher.txt`
**TODO File**: `updates/todo-files/game_data_fetcher_todo.md`

---

## Questions Identified During Verification

Based on 5 verification iterations of the specification and codebase research, the following questions need clarification before implementation:

### Question 1: Async vs Sync HTTP Implementation

**Context**: The existing `espn_client.py` uses async/await with httpx for HTTP requests. However, the game data fetcher makes relatively few API calls (18 weeks × ~16 games = ~288 ESPN calls + weather calls).

**Options**:
1. **Async (like ESPNClient)**: More complex but consistent with existing patterns
2. **Sync (simple httpx)**: Simpler implementation, easier to test, sufficient for this use case

**Recommendation**: Sync httpx for simplicity, since game fetching is infrequent and doesn't need the performance of async.

**Question**: Should game_data_fetcher use async or sync HTTP?

Answer: Use sync http

---

### Question 2: Standalone Runner Script

**Context**: The specification mentions `run_game_data_fetcher.py --season 2024 --output simulation/sim_data/game_data.csv`. This suggests a standalone script similar to `run_player_fetcher.py`.

**Options**:
1. **Standalone script**: `run_game_data_fetcher.py` in project root with argparse for --season and --output
2. **Integrated only**: Only run as part of the main player data fetcher workflow

**Recommendation**: Create standalone script (matches spec and allows flexible usage).

**Question**: Do you want a standalone `run_game_data_fetcher.py` script in the project root?

Answer: Yes it should have both a standalone script and be integrated into the player_data_fetcher. We can use the standalone script to help with generating season 2024 data for the simulation

---

### Question 3: Indoor Flag Source Priority

**Context**: Both `coordinates.json` and the ESPN API provide an `indoor` flag. There's potential for conflict.

**Options**:
1. **coordinates.json priority**: Use pre-defined indoor flag from coordinates.json for NFL stadiums, ESPN for international venues
2. **ESPN API priority**: Always trust ESPN's venue.indoor flag
3. **Merge with validation**: Use both and log warning if they differ

**Recommendation**: Use coordinates.json for NFL stadiums (more reliable, we control it), ESPN for international venues only.

**Question**: Which source should be authoritative for the indoor flag?

Answer: Use the ESPN API. I believe we can actually remove the indoor flag from coordinates.json entirely

---

### Question 4: Open-Meteo API Selection (Historical vs Forecast)

**Context**: Open-Meteo has TWO separate APIs with different time coverage:

| API | Endpoint | Time Coverage |
|-----|----------|---------------|
| **Historical API** | `archive-api.open-meteo.com/v1/archive` | 1940 to **5 days ago** |
| **Forecast API** | `api.open-meteo.com/v1/forecast` | Past 92 days to **16 days in the future** |

This means:
- **Past games (>5 days ago)**: Use Historical API (more accurate reanalysis data)
- **Recent games (last 5 days)**: Use Forecast API with `past_days` parameter
- **Upcoming games (next 16 days)**: Use Forecast API with `forecast_days` parameter

**Options**:
1. **Dual-API approach**: Check game date and route to appropriate API endpoint
2. **Historical only**: Only use Historical API, leave recent/future games with None weather
3. **Forecast only**: Use Forecast API for everything (simpler but less accurate for old games)

**Recommendation**: Use dual-API approach - Historical for games >5 days old, Forecast for recent/upcoming games.

**Question**: Should we implement the dual-API approach to get weather for all games (past and upcoming)?

Answer: Yes

---

### Question 5: Week Range for 2024 Simulation Data

**Context**: The spec says "all 18 weeks of 2024 regular season". The 2024 NFL regular season had 18 weeks.

**Confirmation needed**: Should we fetch weeks 1-18 for the 2024 simulation data?

Answer: Yes, get data for all weeks of the 2024 season for the simulation.

---

## Summary of Answers

| Question | Recommendation | User Answer |
|----------|----------------|-------------|
| 1. Async vs Sync | Sync httpx (simpler) | **Sync HTTP** |
| 2. Standalone script | Yes, create run_game_data_fetcher.py | **Yes** - both standalone and integrated |
| 3. Indoor flag source | coordinates.json for NFL, ESPN for international | **ESPN API only** - remove indoor from coordinates.json |
| 4. Open-Meteo API | Dual-API (Historical + Forecast) | **Yes** - use dual-API approach |
| 5. 2024 week range | Weeks 1-18 | **Yes** - all weeks |

---

**All questions answered.** Proceeding with second verification round (iterations 6-12) and implementation.
