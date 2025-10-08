# Starter Helper

This directory contains all components for weekly starting lineup optimization based on CSV weekly projection data (no API calls required).

## Structure

```
starter_helper/
├── __init__.py                  # Package initialization
├── starter_helper_config.py    # Configuration settings
├── starter_helper.py           # Main script - entry point
├── lineup_optimizer.py         # Core lineup optimization logic
├── positional_ranking_calculator.py # Team ranking-based adjustments
├── espn_current_week_client.py # Legacy ESPN client (unused in current implementation)
├── tests/                      # Unit tests
└── README.md                   # This file
```

## Usage

### From Parent Directory
```bash
# Run from the main project directory
python run_starter_helper.py
```

### From This Directory
```bash
# Run directly from starter_helper directory
cd starter_helper
python starter_helper.py
```

## Features

- **CSV-Based Projections**: Reads weekly projections directly from `week_N_points` columns in players.csv (no API calls)
- **Roster Filtering**: Automatically filters for your roster players (drafted=2)
- **Optimal Lineup Generation**: Creates best starting lineup with position constraints:
  - 1 Quarterback (QB)
  - 2 Running Backs (RB1, RB2)
  - 2 Wide Receivers (WR1, WR2)
  - 1 Tight End (TE)
  - 1 FLEX (best available RB or WR)
  - 1 Kicker (K)
  - 1 Defense/Special Teams (DST)
- **FLEX Optimization**: Automatically selects best available RB or WR for FLEX position
- **Penalty System**: Applies injury and bye week penalties to player scores
- **Positional Ranking System**: Automatic adjustments based on team offensive/defensive rankings:
  - Uses team rankings from teams.csv to calculate score adjustments
  - Conservative multipliers (1.1x for excellent, 0.9x for poor matchups)
  - 15% weight factor for balanced impact on recommendations
  - Transparent adjustment explanations in output
- **Bench Recommendations**: Shows top bench alternatives with positional ranking adjustments
- **Output Management**: Saves results to timestamped files with latest version
- **Performance Optimized**: Handles large rosters (100+ players) efficiently

## Configuration

Primary settings in `starter_helper_config.py`:

```python
# Week Settings
CURRENT_NFL_WEEK = 3                    # Current NFL week (1-18)
NFL_SEASON = 2025                       # NFL season year
NFL_SCORING_FORMAT = "ppr"              # Scoring format

# Roster Requirements
STARTING_LINEUP_REQUIREMENTS = {
    "QB": 1, "RB": 2, "WR": 2, "TE": 1,
    "FLEX": 1, "K": 1, "DST": 1
}

# Display Settings
SHOW_PROJECTION_DETAILS = True         # Show detailed info
SHOW_INJURY_STATUS = True              # Show injury status
RECOMMENDATION_COUNT = 15               # Number of players to show

# Positional Ranking Settings
# Team rankings are automatically loaded from teams.csv
# Adjustments are applied based on offensive/defensive rankings
# Configuration is handled in positional_ranking_calculator.py

# Output Settings
SAVE_OUTPUT_TO_FILE = True             # Save results to files
OUTPUT_FILE_PREFIX = 'starter_results' # Output file prefix
```

## How It Works

1. **Load Roster**: Filters players.csv for your roster (drafted=2)
2. **Get Projections**: Reads current week projections from `week_N_points` columns
3. **Apply Penalties**: Subtracts injury and bye week penalties from projections
4. **Apply Positional Rankings**: Adds/subtracts points based on team rankings (15% weight)
5. **Optimize Positions**: Selects best players for each required position
6. **Handle FLEX**: Chooses best remaining RB or WR for FLEX spot
7. **Generate Output**: Creates formatted lineup with bench alternatives and ranking adjustments

## Sample Output

```
================================================================================
OPTIMAL STARTING LINEUP - WEEK 3 (PPR SCORING)
================================================================================
 1. QB  : Patrick Mahomes (KC)     - 22.4 pts
 2. RB  : Christian McCaffrey (SF)  - 18.9 pts [+1.2 rank adj (Elite offensive (rank 2): +7.5%)]
 3. RB  : Josh Jacobs (LV)         - 16.3 pts
 4. WR  : Tyreek Hill (MIA)        - 17.8 pts
 5. WR  : Stefon Diggs (BUF)       - 16.1 pts [+0.8 rank adj (Good offensive (rank 8): +5.0%)]
 6. TE  : Travis Kelce (KC)        - 13.2 pts
 7. FLEX: Keenan Allen (LAC) - WR  - 14.7 pts
 8. K   : Harrison Butker (KC)     - 9.1 pts
 9. DEF : San Francisco (SF)       - 8.8 pts [+0.5 rank adj (Elite defensive (rank 3): +5.0%)]
--------------------------------------------------------------------------------
TOTAL PROJECTED POINTS: 155.7 (includes positional adjustments)
--------------------------------------------------------------------------------

TOP BENCH ALTERNATIVES:
------------------------------------------------------------
 1. DeAndre Hopkins (TEN) - WR        - 12.3 pts
 2. David Montgomery (DET) - RB       - 11.8 pts [QUESTIONABLE]
 3. Tyler Bass (BUF) - K              - 8.9 pts
```

## Quick Start

1. **Update Week Settings**:
   ```python
   # In starter_helper_config.py
   CURRENT_NFL_WEEK = [current_week]
   ```

2. **Ensure Current Roster**: Make sure your players have drafted=2 in players.csv

3. **Team rankings loaded automatically from teams.csv**

4. **Run the Script**:
   ```bash
   python run_starter_helper.py
   ```

## Technical Details

- **Data Source**: CSV-based projections from players.csv weekly columns
- **Offline Operation**: Works completely offline using CSV data and team rankings
- **Position Constraints**: Enforces league requirements automatically
- **FLEX Handling**: Intelligent selection between RB and WR for FLEX spot
- **Injury Awareness**: Configurable penalties for different injury statuses
- **Processing Time**: < 1 second for typical roster sizes (15-20 players) with positional rankings

## Performance

- **Fast**: < 1 second execution time for typical rosters
- **Memory Efficient**: Processes only roster players (not entire player database)
- **Scalable**: Handles large rosters (100+ players) without performance degradation

## Troubleshooting

Common issues and solutions:

- **No Roster Players Found**: Ensure players have drafted=2 in players.csv
- **Missing Weekly Projections**: Check that `week_N_points` columns exist in players.csv
- **Missing Team Rankings**: Ensure teams.csv contains offensive_rank and defensive_rank columns
- **Configuration Errors**: All settings are validated on startup with clear error messages

## Dependencies

Core requirements:
- `pandas` - Data manipulation and CSV processing

## Testing

Run the test suite to verify functionality:

```bash
# From starter_helper directory
python -m pytest tests/ -v

# Specific test files
python -m pytest tests/test_starter_helper.py -v
python -m pytest tests/test_lineup_optimizer.py -v
```

The test suite covers:
- Configuration validation
- CSV data loading and processing
- Lineup optimization algorithms
- Penalty calculations
- Output formatting
- Error handling scenarios