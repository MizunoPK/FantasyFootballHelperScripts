# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment

This is a Python 3.13.6 project using a virtual environment located at `.venv/` with a modern modular architecture featuring async operations, week-by-week projections, and type-safe data validation.

### Setup Commands
```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies (includes httpx, pydantic, tenacity, aiofiles)
.venv\Scripts\pip.exe install -r requirements.txt
```

### Running the Application

**IMPORTANT**: All scripts are run from the root directory using wrapper scripts:

```bash
# Run player projections fetcher (ESPN API) - Advanced week-by-week system (8-15 min)
# CRITICAL: Update CURRENT_NFL_WEEK weekly in player-data-fetcher/config.py
.venv\Scripts\python.exe run_player_data_fetcher.py

# Run draft helper in draft mode (initial draft)
# Set TRADE_HELPER_MODE = False in draft_helper/config.py
.venv\Scripts\python.exe run_draft_helper.py

# Run draft helper in trade mode (weekly trade analysis using pure greedy algorithm)
# Set TRADE_HELPER_MODE = True in draft_helper/config.py
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
- **Week-by-Week Projection System**: Advanced optimization reducing API calls from 10,336 to 646 (16x improvement)
- **Async Architecture**: httpx client with tenacity retry logic and concurrent aiofiles export
- **Smart Data Preservation**: Maintains drafted/locked status with `SKIP_DRAFTED_PLAYER_UPDATES` optimization
- **Multi-Format Export**: Concurrent CSV, Excel, JSON output with timestamps
- **Automatic Fallbacks**: Graceful degradation when week-by-week data unavailable
- **Pydantic Models**: Type-safe data validation and serialization throughout pipeline
- **Configuration-Driven**: Modular config system with weekly `CURRENT_NFL_WEEK` updates

**2. Draft Helper (`draft_helper/`)**
- **Pure Greedy Trade Algorithm**: Simplified, efficient trade optimization without complex lookahead
- **Draft Mode**: Interactive draft assistant with configurable position-based strategy
- **Trade Mode**: Weekly roster optimization with runner-up trade suggestions
- **FLEX Position Handling**: Advanced logic for RB/WR eligibility in FLEX slots
- **Injury Risk Assessment**: Configurable penalties for LOW/MEDIUM/HIGH injury statuses
- **Roster Validation**: Automatic enforcement of "Start 7 Fantasy League" construction rules

**3. NFL Scores Fetcher (`nfl-scores-fetcher/`)**
- **Async Score Collection**: Recent NFL game data with configurable time windows
- **Multi-Format Export**: CSV, JSON, Excel outputs for external spreadsheet integration
- **Modular Architecture**: Standalone client and export components
- **Configurable Filtering**: Completed games only, specific weeks, season type selection

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

**Modular Configuration Architecture:**
- `player-data-fetcher/config.py` - **Week-by-week projection system**, data preservation, async export settings
- `nfl-scores-fetcher/config.py` - Scores API configuration, filtering options, export preferences
- `draft_helper/config.py` - **Pure greedy trade optimization**, draft strategy, roster construction rules
- `config.py` (root) - Shared file paths only (minimal centralized configuration)

Each module includes comprehensive validation and clear documentation of frequently modified settings.

**Most Frequently Modified Settings:**
- **🔥 CRITICAL WEEKLY UPDATE**: `CURRENT_NFL_WEEK` in `player-data-fetcher/config.py` (update every Tuesday)
- **Major Performance Optimizations**:
  - `SKIP_DRAFTED_PLAYER_UPDATES` (skip API calls for drafted=1 players)
  - `USE_SCORE_THRESHOLD` (skip API calls for low-scoring players, preserve existing data)
  - `PLAYER_SCORE_THRESHOLD` (minimum fantasy points to trigger API update, default: 15.0)
- **Week-by-Week System**: `USE_WEEK_BY_WEEK_PROJECTIONS` (True=advanced 646-call system, False=legacy)
- **Trade Mode**: `TRADE_HELPER_MODE` (True=trade analysis, False=draft mode)
- **Draft Strategy**: `DRAFT_ORDER` array (position priorities by round with FLEX handling)
- **Trade Algorithm**: `MIN_TRADE_IMPROVEMENT` (point threshold for pure greedy recommendations)
- **Injury Tolerance**: `INJURY_PENALTIES` (LOW/MEDIUM/HIGH risk assessment)

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

**Modern Async Architecture Stack:**
```bash
# Async HTTP and data processing
httpx>=0.24.0           # High-performance async HTTP client
aiofiles>=23.0.0        # Async file operations for concurrent export
pandas>=2.0.0           # Data manipulation and analysis

# Type Safety and Validation
pydantic>=2.0.0         # Runtime type checking and data validation
pydantic-settings>=2.0.0 # Configuration management with validation

# Resilience and Configuration
tenacity>=8.2.0         # Retry logic with exponential backoff
python-dotenv>=1.0.0    # Environment variable management

# Export Formats and Legacy Support
openpyxl>=3.1.0         # Excel export support
requests>=2.31.0        # Legacy HTTP support (minimal usage)
```

**Key Architecture Benefits:**
- **16x Performance**: Week-by-week system reduces API calls from 10,336 to 646
- **Type Safety**: Pydantic models prevent runtime errors and validate data
- **Async Operations**: Concurrent data fetching and export for faster processing
- **Resilient APIs**: Automatic retry logic handles network issues gracefully

## Common Workflows

### 1. Initial Season Setup (Draft Mode)
```bash
# 1. Update bye weeks in shared_files/bye_weeks.csv (manual, once per season)

# 2. Configure week-by-week projections for draft
# Edit player-data-fetcher/config.py:
CURRENT_NFL_WEEK = 1                           # Start of season
USE_WEEK_BY_WEEK_PROJECTIONS = True            # Enable advanced projections
USE_REMAINING_SEASON_PROJECTIONS = False       # Full season for draft
INCLUDE_PLAYOFF_WEEKS = False                  # Regular season only

# 3. Set draft mode
# Edit draft_helper/config.py: TRADE_HELPER_MODE = False

# 4. Fetch fresh player data (takes 8-15 minutes with week-by-week)
.venv\Scripts\python.exe run_player_data_fetcher.py

# 5. Run draft helper for live draft
.venv\Scripts\python.exe run_draft_helper.py
```

### 2. Weekly Trade Analysis (During Season)
```bash
# 🔥 STEP 1: Update current week (CRITICAL - Do this every Tuesday)
# Edit player-data-fetcher/config.py:
CURRENT_NFL_WEEK = [current_week]              # Update weekly: 1, 2, 3... 18
USE_WEEK_BY_WEEK_PROJECTIONS = True            # Keep advanced projections
USE_REMAINING_SEASON_PROJECTIONS = True        # Only remaining weeks matter
INCLUDE_PLAYOFF_WEEKS = False                  # Regular season focus

# 2. Set trade mode
# Edit draft_helper/config.py: TRADE_HELPER_MODE = True

# 3. Fetch updated player data (1-2x per week before games)
.venv\Scripts\python.exe run_player_data_fetcher.py

# 4. Update players.csv with any manual roster changes from NFL Fantasy

# 5. Run trade analysis
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

# 1. Test player data fetcher with week-by-week projections
.venv\Scripts\python.exe run_player_data_fetcher.py
# Verify:
#   ✅ DST teams have realistic points (>50)
#   ✅ Log shows "Week-by-week total for [Top Players]: [250-350] points (15 weeks)"
#   ✅ Completes in 8-15 minutes (not hours)
#   ✅ No "Failed to get all weeks data" warnings for majority of players
#   ✅ Some players may show "Using remaining_season fallback" (normal)

# 2. Test draft helper in draft mode
# Edit draft_helper/config.py: TRADE_HELPER_MODE = False
timeout 10 .venv\Scripts\python.exe run_draft_helper.py
# Verify: Shows "Draft Helper!", displays draft order, prompts for input

# 3. Test pure greedy trade helper
# Edit draft_helper/config.py: TRADE_HELPER_MODE = True
.venv\Scripts\python.exe run_draft_helper.py
# Verify: Shows "Trade Helper!", pure greedy optimization, runner-up alternatives

# 4. Test async NFL scores fetcher
.venv\Scripts\python.exe run_nfl_scores_fetcher.py
# Verify: Fetches recent games, concurrent multi-format export
```

### Week-by-Week Projection System Validation
```bash
# Advanced validation for the new projection system:

# Expected log output during player data fetcher run:
# ✅ "Week-by-week total for Lamar Jackson: 341.1 points (15 weeks)"
# ✅ "Week-by-week total for Christian McCaffrey: 318.3 points (15 weeks)"
# ✅ "Week-by-week total for [DST]: 95.5 points (16 weeks)" (defenses get 16)
# ✅ "Using remaining_season fallback for [Some Player]" (normal for incomplete data)

# Performance indicators:
# ✅ Processing ~646 players in 8-15 minutes
# ✅ One API call per player (not per week)
# ✅ No timeout errors or extended delays
```

### Configuration Validation
- Each config file has built-in validation on import
- Draft helper validates roster math: `sum(MAX_POSITIONS) >= MAX_PLAYERS`
- Draft order validation: `len(DRAFT_ORDER) == MAX_PLAYERS`

### Common Issues and Solutions
1. **Week-by-Week Timeouts**: If player data fetcher takes >20 minutes, set `USE_WEEK_BY_WEEK_PROJECTIONS = False`
2. **Inconsistent Player Points**: Ensure `CURRENT_NFL_WEEK` is updated weekly during season (most common issue)
3. **Missing Week-by-Week Data**: Some players may show "Using remaining_season fallback" - this is normal
4. **Import Errors**: Check that script-specific config files exist and have required constants
5. **Path Issues**: Verify `shared_files/players.csv` exists and is accessible from module directories
6. **ESPN API Issues**: Check network connectivity; ESPN API is free but unofficial
7. **Roster Math**: Ensure position limits add up correctly in `draft_helper/config.py`

### Week-by-Week System Troubleshooting
**Problem**: "Failed to get all weeks data for player [X]" warnings
- **Solution**: Normal for some players; system falls back to existing methods
- **Action**: No action needed unless >50% of players show this warning

**Problem**: Player data fetcher takes >30 minutes
- **Solution**: Temporary ESPN API slowdown; try again later or disable week-by-week
- **Action**: Set `USE_WEEK_BY_WEEK_PROJECTIONS = False` temporarily

**Problem**: Player projections seem too low/high after week update
- **Solution**: Verify `CURRENT_NFL_WEEK` matches actual NFL week
- **Action**: Check `CURRENT_NFL_WEEK = [1-18]` and `USE_REMAINING_SEASON_PROJECTIONS = True`

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

## 🚀 Recent Architecture Improvements

### Version 2.0+ Enhancements
- **Modular Async Architecture**: Completely refactored with httpx, aiofiles, and pydantic models
- **Week-by-Week Projection System**: 16x performance improvement (646 vs 10,336 API calls)
- **Pure Greedy Trade Algorithm**: Simplified from complex lookahead systems for better reliability
- **Smart Data Preservation**: Skip API calls for drafted players, maintain status between updates
- **Multi-Format Export Pipeline**: Concurrent CSV, Excel, JSON export with timestamp tracking
- **Configuration Validation**: Built-in validation for all modules with clear error messages

### Performance Optimizations
- **API Call Reduction**: Optimized from 10,336 to 646 calls using week-by-week player approach
- **Dual Optimization System**:
  - **Drafted Player Skipping**: `SKIP_DRAFTED_PLAYER_UPDATES` skips API calls for drafted=1 players
  - **Score Threshold Filtering**: `USE_SCORE_THRESHOLD` preserves existing data for players below `PLAYER_SCORE_THRESHOLD`
  - **Combined Effect**: Can reduce API calls from 646 to potentially 100-200 depending on threshold
- **Smart Data Preservation**: Always updates roster players (drafted=2) regardless of score
- **Concurrent Operations**: Async data fetching and export operations for faster processing
- **Graceful Fallbacks**: Automatic fallback to legacy methods when week-by-week data unavailable

### Code Quality Improvements
- **Type Safety**: Pydantic models provide runtime type checking and validation
- **Error Handling**: Comprehensive error handling with tenacity retry logic
- **Modular Design**: Clean separation of concerns with standalone modules
- **Configuration Management**: Centralized config system with per-module validation

This system provides sophisticated draft assistance and trade analysis with modern async architecture while maintaining flexibility for strategy adjustments throughout the fantasy football season.