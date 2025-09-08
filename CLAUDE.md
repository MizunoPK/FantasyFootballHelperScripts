# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment

This is a Python 3.13.6 project using a virtual environment located at `.venv/`. 

### Setup Commands
```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
.venv\Scripts\pip.exe install -r requirements.txt
```

### Running the Application

**IMPORTANT**: All scripts are run from the root directory using wrapper scripts:

```bash
# Run the main draft helper
.venv\Scripts\python.exe draft_helper.py

# Generate fresh player data (run before draft_helper.py)
.venv\Scripts\python.exe player_data_generator.py

# Run draft simulation
.venv\Scripts\python.exe draft_helper_simulator.py

# Run player projections fetcher (ESPN API)
.venv\Scripts\python.exe run_player_data_fetcher.py

# Run NFL scores fetcher
.venv\Scripts\python.exe run_nfl_scores_fetcher.py
```

**Script Organization:**
- Main scripts are in root directory
- Sub-modules are in subdirectories (`player-data-fetcher/`, `nfl-scores-fetcher/`)
- Wrapper scripts (`run_*.py`) change to subdirectory and execute the actual script
- All paths in sub-modules must account for being run from their subdirectory via wrapper

## Code Architecture

### Core Components

**Data Flow Pipeline:**
1. `player_data_generator.py` - Fetches player data from Sleeper API and combines with ADP/bye week data
2. `draft_helper.py` - Main application providing draft recommendations
3. Data stored in CSV files under `data/` directory

**Key Classes:**
- `Player` (`Player.py`) - Represents individual players with stats, ADP, bye weeks, injury status
- `FantasyTeam` (`FantasyTeam.py`) - Manages drafted roster, tracks starters vs bench, enforces limits
- `DraftHelper` (`draft_helper.py`) - Core logic for scoring and recommending players

**Configuration:**
- `Constants.py` - Centralized configuration including roster limits, scoring weights, and ideal draft strategy
- Draft strategy defined by `DRAFT_ORDER` array specifying position priorities by round

### Data Sources

**CSV Files (in `data/`):**
- `players.csv` - Master player list with ADP, bye weeks, injury status
- `team.csv` - Currently drafted players (cleared between drafts)  
- `adp.csv` - Average Draft Position data from external source
- `bye_weeks.csv` - NFL bye week schedule

### Scoring Algorithm

Players are scored using multiple weighted factors:
- **Positional Need** - Matches team roster needs vs ideal draft strategy
- **ADP Value** - Lower ADP = higher draft value
- **Bye Week Conflicts** - Penalizes players with same bye as current roster
- **Injury Status** - Penalizes injured players

Scoring weights configurable in `Constants.py` under "SCORE WEIGHTS" section.

## Typical Workflow

1. Download ADP data to `data/adp.csv` 
2. Update bye week data in `data/bye_weeks.csv`
3. Run `player_data_generator.py` to refresh `data/players.csv`
4. Clear/delete `data/team.csv` for new draft
5. Run `draft_helper.py` for live draft recommendations

## Dependencies

- `requests` - HTTP API calls to Sleeper
- `pandas` - CSV data manipulation