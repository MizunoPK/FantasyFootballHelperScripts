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
# Run player projections fetcher (ESPN API) - Run 1-2x per week before games
.venv\Scripts\python.exe run_player_data_fetcher.py

# Run draft helper in draft mode (initial draft)
.venv\Scripts\python.exe run_draft_helper.py

# Run draft helper in trade mode (weekly trade analysis)
# First set TRADE_HELPER_MODE = True in draft_helper/config.py
.venv\Scripts\python.exe run_draft_helper.py

# Run NFL scores fetcher (for data compilation)
.venv\Scripts\python.exe run_nfl_scores_fetcher.py
```

**Script Organization:**
- Main wrapper scripts (`run_*.py`) are in root directory
- Core modules are in subdirectories (`player-data-fetcher/`, `nfl-scores-fetcher/`, `draft_helper/`)
- Wrapper scripts change to subdirectory and execute the actual script
- Shared components are in `shared_files/` directory

## Project Architecture

### Core Modules

**1. Player Data Fetcher (`player-data-fetcher/`)**
- Fetches player projections from ESPN API (free, no signup required)
- Processes fantasy points, injury status, team assignments
- Preserves drafted/locked player status between updates
- Outputs to `shared_files/players.csv` and module `data/` directory

**2. Draft Helper (`draft_helper/`)**
- **Draft Mode**: Interactive draft assistant with recommendations
- **Trade Mode**: Analyzes current roster and suggests beneficial trades
- Configurable draft strategy and scoring weights
- Mode controlled by `TRADE_HELPER_MODE` in `draft_helper/config.py`

**3. NFL Scores Fetcher (`nfl-scores-fetcher/`)**
- Fetches NFL game scores from ESPN API
- Used for data compilation into external spreadsheets
- Outputs in CSV, JSON, and Excel formats

### Key Classes

**FantasyPlayer** (`shared_files/FantasyPlayer.py`)
- Represents individual players with projections, injury status, team info
- Handles drafted/locked status and availability calculations

**FantasyTeam** (`draft_helper/FantasyTeam.py`)
- Manages 15-player roster with position limits and FLEX eligibility
- Enforces "Start 7 Fantasy League" roster construction rules
- Handles draft validation and trade optimization

**DraftHelper** (`draft_helper/draft_helper.py`)
- Core logic for player scoring and recommendations
- Supports both draft and trade modes
- Configurable penalties for bye weeks, injuries, positional needs

### League Configuration ("Start 7 Fantasy League")

**Roster Rules:**
- **Total Players**: 15 (14 players + 1 defense)
- **Starting Lineup**: 7 players + 1 kicker + 1 defense
  - 1 Quarterback
  - 2 Running Backs  
  - 2 Wide Receivers
  - 1 Tight End
  - 1 FLEX (Wide Receiver OR Running Back)
  - 1 Kicker
  - 1 Defense/Special Teams
- **Bench**: 6 slots
- **Reserve**: 3 slots (injured players)
- **League Size**: 10 teams

**Current Roster Limits** (in `draft_helper/config.py`):
```python
MAX_POSITIONS = {
    QB: 2,      # 1 starter + 1 backup
    RB: 4,      # 2 starters + FLEX + backup
    WR: 4,      # 2 starters + FLEX + backup  
    FLEX: 1,    # Can be RB or WR
    TE: 2,      # 1 starter + 1 backup
    K: 1,       # 1 starter only
    DST: 1,     # 1 starter only
}
```

### Configuration System

**Script-Specific Config Files:**
- `player-data-fetcher/config.py` - ESPN API settings, output formats, fallback scoring
- `nfl-scores-fetcher/config.py` - NFL API settings, current week, season settings  
- `draft_helper/config.py` - Draft strategy, roster limits, scoring weights, trade thresholds
- `config.py` (root) - Shared constants (mainly file paths)

**Most Frequently Modified Settings:**
- **Draft Strategy**: `DRAFT_ORDER` array (position priorities by round)
- **Injury Tolerance**: `INJURY_PENALTIES` (LOW/MEDIUM/HIGH risk penalties)
- **Trade Sensitivity**: `MIN_TRADE_IMPROVEMENT` (minimum points for trade recommendations)
- **Mode Switching**: `TRADE_HELPER_MODE` (True=trade analysis, False=draft mode)

### Data Flow and Files

**Data Sources:**
- **ESPN API**: Player projections, injury status, team assignments (automated)
- **ESPN API**: NFL game scores (automated)  
- **Manual**: Bye weeks (`shared_files/bye_weeks.csv` - updated before season)
- **Manual**: Draft status updates (`shared_files/players.csv` - based on NFL Fantasy changes)

**Key Data Files:**
- `shared_files/players.csv` - Master player database (preserved between updates)
- `shared_files/bye_weeks.csv` - NFL bye week schedule (manual, pre-season)
- `shared_files/FantasyPlayer.py` - Shared player data model
- Module-specific `data/` directories for exported data

**Data Preservation:**
- Drafted player status is preserved between player data updates
- Locked player status can be preserved (configurable)
- Historical projections are maintained in timestamped files

### Dependencies

```bash
# Core HTTP and data processing
requests>=2.31.0
httpx>=0.24.0           # Async HTTP client
pandas>=2.0.0           # Data manipulation

# Data validation and settings  
pydantic>=2.0.0         # Data validation
pydantic-settings>=2.0.0
python-dotenv>=1.0.0    # Environment variables

# Resilience and file I/O
tenacity>=8.2.0         # Retry logic
aiofiles>=23.0.0        # Async file operations

# Export formats
openpyxl>=3.1.0         # Excel support
```

## Common Workflows

### 1. Initial Season Setup (Draft Mode)
```bash
# 1. Update bye weeks in shared_files/bye_weeks.csv (manual, once per season)
# 2. Set draft mode
# Edit draft_helper/config.py: TRADE_HELPER_MODE = False
# 3. Fetch fresh player data
.venv\Scripts\python.exe run_player_data_fetcher.py
# 4. Run draft helper for live draft
.venv\Scripts\python.exe run_draft_helper.py
```

### 2. Weekly Trade Analysis
```bash
# 1. Set trade mode  
# Edit draft_helper/config.py: TRADE_HELPER_MODE = True
# 2. Fetch updated player data (1-2x per week before games)
.venv\Scripts\python.exe run_player_data_fetcher.py
# 3. Update players.csv with any manual roster changes from NFL Fantasy
# 4. Run trade analysis
.venv\Scripts\python.exe run_draft_helper.py
```

### 3. Data Compilation for External Analysis
```bash
# Fetch NFL scores for spreadsheet compilation
.venv\Scripts\python.exe run_nfl_scores_fetcher.py
# Output files will be in nfl-scores-fetcher/data/
```

## Testing and Validation

### Pre-Change Testing Protocol
```bash
# Test all three core functions after configuration changes:

# 1. Test player data fetcher
.venv\Scripts\python.exe run_player_data_fetcher.py
# Verify: DST teams have realistic points (>50), no import errors

# 2. Test draft helper in draft mode
# Edit draft_helper/config.py: TRADE_HELPER_MODE = False  
timeout 10 .venv\Scripts\python.exe run_draft_helper.py
# Verify: Shows "Draft Helper!", displays draft order, prompts for input

# 3. Test draft helper in trade mode
# Edit draft_helper/config.py: TRADE_HELPER_MODE = True
.venv\Scripts\python.exe run_draft_helper.py
# Verify: Shows "Trade Helper!", analyzes roster, suggests trades

# 4. Test NFL scores fetcher
.venv\Scripts\python.exe run_nfl_scores_fetcher.py
# Verify: Fetches recent games, creates CSV/Excel output
```

### Configuration Validation
- Each config file has built-in validation on import
- Draft helper validates roster math: `sum(MAX_POSITIONS) >= MAX_PLAYERS`
- Draft order validation: `len(DRAFT_ORDER) == MAX_PLAYERS`

### Common Issues and Solutions
1. **Import Errors**: Check that script-specific config files exist and have required constants
2. **Path Issues**: Verify `shared_files/players.csv` exists and is accessible from module directories  
3. **ESPN API Issues**: Check network connectivity; ESPN API is free but unofficial
4. **Roster Math**: Ensure position limits add up correctly in `draft_helper/config.py`

## Strategy Tuning

### Frequently Adjusted Settings

**Draft Strategy** (`draft_helper/config.py`):
```python
# Position priorities by round (higher = more priority)
DRAFT_ORDER = [
    {FLEX: 1.0, QB: 0.7},    # Round 1: Prefer FLEX players, consider QB
    {QB: 1.0, FLEX: 0.7},    # Round 5: Prioritize QB, backup FLEX
    # ... adjust based on league trends
]
```

**Risk Tolerance** (`draft_helper/config.py`):
```python
INJURY_PENALTIES = {
    "LOW": 0,        # Healthy players
    "MEDIUM": 25,    # Questionable, Day-to-Day (tune this)
    "HIGH": 50       # Out, IR, Suspended (tune this)
}
```

**Trade Sensitivity** (`draft_helper/config.py`):
```python
MIN_TRADE_IMPROVEMENT = 1  # Minimum points to suggest trade (lower = more trades)
```

### Strategy Examples
```python
# Conservative injury approach (avoid risk)
INJURY_PENALTIES = {"MEDIUM": 40, "HIGH": 80}

# Aggressive RB strategy (prioritize early)  
DRAFT_ORDER[0] = {RB: 1.2, FLEX: 0.8}

# High trade threshold (only suggest strong trades)
MIN_TRADE_IMPROVEMENT = 15
```

This system provides sophisticated draft assistance and trade analysis while maintaining flexibility for strategy adjustments throughout the fantasy football season.