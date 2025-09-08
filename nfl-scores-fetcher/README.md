# NFL Scores Fetcher

This directory contains all components for NFL game scores collection from ESPN's API.

## Structure

```
nfl-scores-fetcher/
├── __init__.py                  # Package initialization
├── data_fetcher-scores.py       # Main script - entry point
├── models.py                    # Data models (Pydantic)
├── nfl_api_client.py           # NFL API client (ESPN)
├── data_exporter.py            # Export operations (CSV, JSON, Excel)
├── scores_constants.py         # Constants and mappings
└── README.md                   # This file
```

## Usage

### From Parent Directory
```bash
# Run from the main project directory
python run_nfl_scores_fetcher.py
```

### From This Directory
```bash
# Run directly from nfl-scores-fetcher directory
cd nfl-scores-fetcher
python data_fetcher-scores.py
```

## Features

- **Modular Architecture**: Clean separation of concerns across multiple files
- **Async Operations**: Concurrent data fetching and file exports
- **Multiple Formats**: Exports to CSV, JSON, and Excel with analysis sheets
- **Flexible Collection**: Current week, specific week, or recent games
- **Rich Data Model**: Comprehensive game information including venue, weather, odds
- **Error Handling**: Robust error handling with specific exception types
- **Performance**: Async file I/O and concurrent operations

## Configuration

Settings are controlled via environment variables or `.env` file in the parent directory:

```bash
NFL_SCORES_SEASON=2025                          # NFL season year
NFL_SCORES_SEASON_TYPE=2                        # 1=Preseason, 2=Regular, 3=Postseason  
NFL_SCORES_CURRENT_WEEK=15                      # Specific week (optional)
NFL_SCORES_ONLY_COMPLETED_GAMES=true            # Filter to completed games only
NFL_SCORES_OUTPUT_DIRECTORY=./data   # Output directory
NFL_SCORES_CREATE_CSV=false                     # Create CSV files
NFL_SCORES_CREATE_JSON=false                    # Create JSON files  
NFL_SCORES_CREATE_EXCEL=true                    # Create Excel files
NFL_SCORES_CREATE_CONDENSED_EXCEL=true          # Create condensed Excel files
```

## Data Collection Modes

1. **Current Week Mode**: Gets ESPN's current week scores
2. **Specific Week Mode**: Set `NFL_SCORES_CURRENT_WEEK=X` for week X
3. **Recent Games Mode**: Gets completed games from last 10 days (default)

## Output Files

Generated in the configured output directory:
- `nfl_scores_weekX_TIMESTAMP.json` (if JSON enabled)
- `nfl_scores_weekX_TIMESTAMP.csv` (if CSV enabled)
- `nfl_scores_weekX_TIMESTAMP.xlsx` (full game data with multiple sheets)
- `nfl_scores_condensed_weekX_TIMESTAMP.xlsx` (condensed data with team analysis)
- `nfl_scores_latest.*` (latest versions)

## Excel Sheet Details

**Full Excel Export:**
- All Games: Complete game data
- Completed Games: Only finished games
- Summary: Statistical analysis
- High Scoring Games: Games with 50+ points

**Condensed Excel Export:**
- Game Results: Essential game information
- Team Analysis: Win/loss records, scoring stats
- Summary: Quick overview statistics

## Dependencies

See parent directory's `requirements.txt` for full dependency list.

## Data Source

Uses ESPN's unofficial NFL scoreboard API - free but subject to change.