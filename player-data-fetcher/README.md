# Player Data Fetcher

This directory contains all components for NFL player data collection from ESPN's fantasy API.

## Structure

```
player-data-fetcher/
├── __init__.py                  # Package initialization
├── config.py                   # 🔥 Configuration (update CURRENT_NFL_WEEK weekly)
├── data_fetcher-players.py      # Main script - entry point
├── models.py                    # Data models (Pydantic)
├── espn_client.py              # 🆕 ESPN API client with week-by-week system
├── data_exporter.py            # Export operations (CSV, JSON, Excel)
├── player_data_constants.py    # Constants and mappings
└── README.md                   # This file
```

## Usage

### From Parent Directory
```bash
# Run from the main project directory
python run_player_data_fetcher.py
```

### From This Directory
```bash
# Run directly from player-data-fetcher directory
cd player-data-fetcher
python data_fetcher-players.py
```

## Features

- **🆕 Week-by-Week Projections**: Advanced primary scoring system combining actual + projected performance
- **Optimized API Calls**: Single request per player (646 calls vs 10,336 in naive implementation)
- **Intelligent Fallbacks**: Automatic fallback to legacy methods when week-by-week data unavailable
- **Configurable Projection Scope**: Full season vs remaining weeks, with/without playoffs
- **Modular Architecture**: Clean separation of concerns across multiple files
- **Async Operations**: Concurrent data fetching and file exports
- **Multiple Formats**: Exports to CSV, JSON, and Excel with position sheets
- **Error Handling**: Comprehensive error handling with specific exception types
- **Type Safety**: Full type hints and Pydantic validation
- **Performance**: Async file I/O and concurrent operations

## Configuration

Primary settings in `config.py` (most frequently modified):

```python
# Week-by-Week Projection Settings (🔥 UPDATE WEEKLY)
CURRENT_NFL_WEEK = 2                      # Current NFL week (1-18)
USE_WEEK_BY_WEEK_PROJECTIONS = True       # Enable advanced projection system
USE_REMAINING_SEASON_PROJECTIONS = True   # True=remaining weeks, False=full season
INCLUDE_PLAYOFF_WEEKS = False             # Include playoff weeks (19-22)

# Season Configuration
NFL_SEASON = 2025
NFL_SCORING_FORMAT = "ppr"                 # "ppr", "std", or "half"

# Output Settings
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = True
```

Alternatively, can be controlled via environment variables or `.env` file.

## Output Files

Generated in the configured output directory:
- `nfl_projections_season_TIMESTAMP_FORMAT.csv`
- `nfl_projections_season_TIMESTAMP_FORMAT.json`
- `nfl_projections_season_TIMESTAMP_FORMAT.xlsx`
- `nfl_projections_latest_season.*` (latest versions)

## Dependencies

See parent directory's `requirements.txt` for full dependency list.

## Week-by-Week Projection System

### How It Works
1. **Single API Call Per Player**: Fetches all weekly data in one optimized request
2. **Smart Data Selection**:
   - Past weeks (≤ CURRENT_NFL_WEEK): Uses actual performance when available
   - Future weeks (> CURRENT_NFL_WEEK): Uses projected performance
   - Bye weeks: Automatically handled as 0 points
3. **Multi-Source Averaging**: Averages multiple data sources when available
4. **Intelligent Fallbacks**: Falls back to season projections or ADP-based estimates

### Performance
- **Processing Time**: 8-15 minutes for ~646 players
- **API Efficiency**: 646 calls (1 per player) vs 10,336 calls (naive per-week approach)
- **Success Rate**: ~90%+ players get week-by-week data, rest use fallbacks

### Expected Log Output
```
Week-by-week total for Lamar Jackson: 341.1 points (15 weeks)
Week-by-week total for Christian McCaffrey: 318.3 points (15 weeks)
Using remaining_season fallback for Joe Burrow (QB): 230.4 points
```

### Troubleshooting
- **Long Processing Times**: If >20 minutes, set `USE_WEEK_BY_WEEK_PROJECTIONS = False`
- **Fallback Messages**: Normal for some players - indicates incomplete ESPN data
- **Inconsistent Results**: Ensure `CURRENT_NFL_WEEK` is updated weekly

## Data Source

Uses ESPN's unofficial fantasy football API - free but subject to change.