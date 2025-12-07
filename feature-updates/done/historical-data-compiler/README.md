# Historical Data Compiler - Work in Progress

## What This Is

We are building a **standalone script** (`compile_historical_data.py`) that compiles historical NFL season data for use in the fantasy football simulation system. The script fetches data from ESPN APIs and creates "point-in-time" snapshots for each week of a season.

## Why We Need This

The simulation system needs historical data to:
1. Test and validate scoring algorithms against known outcomes
2. Run simulations with real past season data
3. Backtest draft strategies and configuration parameters
4. Support multiple seasons for comprehensive analysis

## Scope

**IN SCOPE:**
- Creating a standalone script to compile seasonal datasets
- Generating data files for historical seasons (starting with 2024)
- Defining a new folder/file structure optimized for historical data

**OUT OF SCOPE:**
- Updating the simulation system to consume these new datasets
- Matching the current `simulation/sim_data/` folder structure

The new dataset structure will be **different** from the current simulation data structure. The current `sim_data/` has a flat structure with single files. The new structure will be organized by year and week to support point-in-time analysis.

A **future effort** will update the simulation system to work with these new datasets, but that work is separate and not part of this initiative.

## Current Status: READY FOR IMPLEMENTATION ✓

All data sources and algorithms have been identified. **Planning is complete - ready to create TODO file and begin coding.**

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context for future agents |
| `historical_data_compiler.txt` | High-level requirements and open questions |
| `historical_data_compiler_checklist.md` | Detailed field-by-field checklist of what we need |

## Key Context for Future Agents

### Data Sources (ESPN API Only)
- **Player Data:** ESPN Fantasy API (`lm-api-reads.fantasy.espn.com`)
- **Game Data:** ESPN Scoreboard API (`site.api.espn.com`)
- **Weather Data:** Open-Meteo Archive/Forecast API
- **Years Supported:** 2021+ (weekly data available)

### Target Output Structure
```
simulation/sim_data/{YEAR}/
├── season_schedule.csv
├── game_data.csv
├── team_data/
│   └── {32 team CSVs}
└── weeks/
    └── week_01...week_17/
        ├── players.csv
        └── players_projected.csv
```

### What's Resolved ✓
- **Player stats** - ESPN Fantasy API (actuals + projections for all 6 positions)
- **Game data** - ESPN Scoreboard API (scores, venue, dates) + Open-Meteo (weather)
- **Schedule/bye weeks** - ESPN Scoreboard API

### What's Still Pending
**Nothing!** All data sources and algorithms are resolved.

### Resolved Data Sources

**Player Data (ESPN Fantasy API):**

| Field | Source | Notes |
|-------|--------|-------|
| Weekly actuals | ESPN API `statSourceId=0` | All 6 positions verified |
| Weekly projections | ESPN API `statSourceId=1` | All 6 positions verified |
| player_rating | ESPN API (calculated) | Week 1: draft rank; Week 2+: fantasy_points ranking |
| ADP | ESPN API `ownership.averageDraftPosition` | Verified for historical seasons |
| Schedule/bye weeks | ESPN Scoreboard API | Reuse ScheduleFetcher logic |
| Injury status | Default to "ACTIVE" | Historical injury data not available |

**Game Data (ESPN Scoreboard + Open-Meteo):**

| Field | Source | Notes |
|-------|--------|-------|
| Scores | ESPN Scoreboard API | `competitors[].score` |
| Venue info | ESPN Scoreboard API | `venue.indoor`, `venue.address.*` |
| Neutral site | ESPN Scoreboard API | `competition.neutralSite` |
| Game date | ESPN Scoreboard API | `event.date` (ISO 8601) |
| Weather | Open-Meteo Archive API | Temperature, gust, precipitation |

**Team Data (Calculated):**

| Field | Source | Notes |
|-------|--------|-------|
| pts_allowed_to_* | Calculated | Aggregate player fantasy points by opponent |
| points_scored | Calculated | Sum team's player fantasy points |
| points_allowed | Calculated | Sum opponent player fantasy points |

**Reusable Code:**
- `player-data-fetcher/game_data_fetcher.py` for game data
- `player-data-fetcher/espn_client.py:_collect_team_weekly_data()` for team data

**player_rating Calculation:**
- **Week 1:** Normalize ESPN draft rank to position-specific 1-100
- **Week 2+:** Rank by cumulative fantasy_points, normalize to 1-100

### Key Decisions Made
- **Years:** 2021+ only (weekly data required)
- **Weeks:** 1-17 (full regular season)
- **Positions:** QB, RB, WR, TE, K, DST (6 fantasy-relevant)
- **DST source:** ESPN API (NFL-Data only has individual defensive players)

### Key Decisions Made (Additional)
- **Player filtering:** Include players with at least 1 game or projected points
- **Missing projections:** Skip player entirely
- **Error handling:** Fail loudly (stop and report errors)

## Next Steps

1. Create TODO file in `updates/todo-files/` for implementation
2. Build script incrementally with tests
3. Validate with 2024 season data first
4. Test with additional seasons (2021-2023)

## How to Continue This Work

1. Read `historical_data_compiler.txt` for complete implementation specifications
2. Read `historical_data_compiler_checklist.md` to verify all items are resolved
3. Create implementation TODO file in `updates/todo-files/`
4. Follow standard project workflow (see `rules.md` and `CLAUDE.md`)

## Important: Keeping Documentation in Sync

**As checklist items are marked resolved, the `historical_data_compiler.txt` file MUST be updated with implementation details.**

- The **checklist** tracks what's resolved vs pending
- The **txt file** contains the actual implementation guidance (sources, logic, formulas, etc.)

When resolving an item:
1. Mark it complete in the checklist with a brief note
2. Add full implementation details to the txt file (data source, field mapping, calculation logic, etc.)

This ensures the txt file becomes a complete implementation specification that future agents can use without needing to re-research decisions.
