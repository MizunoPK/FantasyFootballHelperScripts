# Player Data Fetcher

This directory contains all components for NFL player data collection from ESPN's fantasy API.

## Structure

```
player-data-fetcher/
├── __init__.py                  # Package initialization
├── data_fetcher-players.py      # Main script - entry point
├── models.py                    # Data models (Pydantic)
├── espn_client.py              # ESPN API client
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

- **Modular Architecture**: Clean separation of concerns across multiple files
- **Async Operations**: Concurrent data fetching and file exports
- **Multiple Formats**: Exports to CSV, JSON, and Excel with position sheets
- **Error Handling**: Comprehensive error handling with specific exception types
- **Type Safety**: Full type hints and Pydantic validation
- **Performance**: Async file I/O and concurrent operations

## Configuration

Settings are controlled via environment variables or `.env` file in the parent directory:

```bash
NFL_PROJ_SCORING_FORMAT=ppr     # ppr, std, or half
NFL_PROJ_SEASON=2025            # NFL season year
NFL_PROJ_OUTPUT_DIRECTORY=./data
NFL_PROJ_CREATE_CSV=true
NFL_PROJ_CREATE_JSON=true
NFL_PROJ_CREATE_EXCEL=true
```

## Output Files

Generated in the configured output directory:
- `nfl_projections_season_TIMESTAMP_FORMAT.csv`
- `nfl_projections_season_TIMESTAMP_FORMAT.json`
- `nfl_projections_season_TIMESTAMP_FORMAT.xlsx`
- `nfl_projections_latest_season.*` (latest versions)

## Dependencies

See parent directory's `requirements.txt` for full dependency list.

## Data Source

Uses ESPN's unofficial fantasy football API - free but subject to change.