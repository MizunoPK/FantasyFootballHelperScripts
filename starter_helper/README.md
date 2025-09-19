# Starter Helper

This directory contains all components for weekly starting lineup optimization based on CSV weekly projection data (no API calls required).

## Structure

```
starter_helper/
├── __init__.py                  # Package initialization
├── config.py                   # Configuration settings
├── starter_helper.py           # Main script - entry point
├── lineup_optimizer.py         # Core lineup optimization logic
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
- **Bench Recommendations**: Shows top bench alternatives
- **Output Management**: Saves results to timestamped files with latest version
- **Performance Optimized**: Handles large rosters (100+ players) efficiently

## Configuration

Primary settings in `config.py`:

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

# Penalty System
INJURY_PENALTIES = {
    "LOW": 0,      # ACTIVE players
    "MEDIUM": 5,   # QUESTIONABLE, DOUBTFUL
    "HIGH": 15     # OUT, IR, SUSPENDED
}
BYE_WEEK_PENALTY = 50                   # Penalty for bye week players

# Output Settings
SAVE_OUTPUT_TO_FILE = True              # Save results to files
SHOW_PROJECTION_DETAILS = True          # Show full roster breakdown
SHOW_INJURY_STATUS = True               # Display injury status in output
```

## How It Works

### 1. Data Source
- **Input**: `shared_files/players.csv` with weekly projection columns
- **Player Filter**: Only processes players with `drafted=2` (your roster)
- **Weekly Data**: Reads from `week_N_points` column where N = CURRENT_NFL_WEEK

### 2. Lineup Optimization Process
1. **Load Roster**: Filters CSV for drafted=2 players
2. **Extract Projections**: Reads current week points from weekly columns
3. **Apply Penalties**: Subtracts injury and bye week penalties
4. **Position Assignment**: Fills required positions with best available players
5. **FLEX Optimization**: Assigns best remaining RB or WR to FLEX
6. **Generate Output**: Creates formatted lineup with bench alternatives

### 3. Position Priority Logic
```python
# Lineup positions filled in this order:
1. QB (1 required) - Best available quarterback
2. RB (2 required) - Two best running backs
3. WR (2 required) - Two best wide receivers
4. TE (1 required) - Best available tight end
5. K (1 required) - Best available kicker
6. DST (1 required) - Best available defense
7. FLEX (1 required) - Best remaining RB or WR
```

## Expected Output

```
================================================================================
OPTIMAL STARTING LINEUP - WEEK 3 (PPR SCORING)
================================================================================
 1. QB  : Josh Allen (BUF)      - 28.5 pts
 2. RB  : Christian McCaffrey (SF) - 22.3 pts
 3. RB  : Breece Hall (NYJ)     - 18.7 pts [QUESTIONABLE]
 4. WR  : Tyreek Hill (MIA)     - 19.2 pts
 5. WR  : Davante Adams (LV)    - 16.8 pts
 6. TE  : Travis Kelce (KC)     - 14.1 pts
 7. FLEX: Jaylen Waddle (MIA)   - 15.4 pts [OUT] (-15 injury penalty)
 8. K   : Justin Tucker (BAL)   - 9.2 pts
 9. DEF : Buffalo Bills (BUF)   - 11.5 pts
--------------------------------------------------------------------------------
TOTAL PROJECTED POINTS: 155.7
--------------------------------------------------------------------------------

TOP BENCH ALTERNATIVES:
------------------------------------------------------------
 1. Backup RB (BENCH) - RB     - 8.3 pts
 2. Bench WR (BENCH) - WR      - 6.5 pts
```

## Output Files

Generated in `starter_helper/data/` directory:
- `starter_recommendations_YYYYMMDD_HHMMSS.txt` (timestamped)
- `starter_recommendations_latest.txt` (most recent)

## Prerequisites

### Data Requirements
1. **Updated players.csv**: Must contain weekly projection columns (`week_1_points`, `week_2_points`, etc.)
2. **Roster Status**: Players marked with `drafted=2` for your current roster
3. **Current Week**: `CURRENT_NFL_WEEK` must be updated weekly in config.py

### Weekly Workflow
```bash
# 1. Update current week (every Tuesday)
# Edit starter_helper/config.py: CURRENT_NFL_WEEK = X

# 2. Ensure roster is current
# Verify players.csv has drafted=2 for your roster players

# 3. Run starter helper
python run_starter_helper.py

# 4. Review recommendations
# Check starter_helper/data/starter_recommendations_latest.txt
```

## Integration with Other Modules

- **Data Source**: Uses output from `player-data-fetcher` (players.csv with weekly columns)
- **No API Calls**: Completely independent, works offline with existing CSV data
- **Roster Management**: Designed to work with draft/trade decisions from `draft_helper`

## Performance

- **Processing Time**: < 1 second for typical roster sizes (15-20 players)
- **Large Roster Support**: Tested with 100+ players
- **Memory Efficient**: Minimal memory usage, no API rate limiting

## Troubleshooting

### Common Issues
- **No Roster Players Found**: Ensure players.csv has `drafted=2` for your roster
- **Missing Weekly Column**: Check that `week_N_points` column exists in players.csv
- **Zero Projections**: Verify weekly data was populated by player-data-fetcher
- **Incorrect Week**: Update `CURRENT_NFL_WEEK` in config.py

### Validation Commands
```bash
# Check roster players
python -c "import pandas as pd; df=pd.read_csv('../shared_files/players.csv'); print(f'Roster players: {len(df[df.drafted==2])}')"

# Check weekly column
python -c "import pandas as pd; df=pd.read_csv('../shared_files/players.csv'); print([c for c in df.columns if 'week_' in c])"
```

## Dependencies

See parent directory's `requirements.txt` for full dependency list. Key dependencies:
- `pandas` - CSV data manipulation
- `pathlib` - Cross-platform file paths

## Data Flow

```
player-data-fetcher → players.csv → starter_helper → lineup recommendations
                     (weekly columns)              (optimal lineup)
```

This module provides the final step in the weekly fantasy football workflow: converting weekly projections into actionable starting lineup decisions.