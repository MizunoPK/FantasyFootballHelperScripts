# Fantasy Football Helper Scripts

A comprehensive suite of modular tools for managing a "Start 7 Fantasy League" through data-driven draft assistance and trade analysis.

## 🏈 What This Does

This project provides automated fantasy football analysis for a **10-team "Start 7 Fantasy League"** using real-time ESPN data. Built with a modern modular architecture featuring async operations, week-by-week projections, and configurable data export pipelines. Key features:

- **Draft Planning**: Interactive draft assistant with position-based recommendations and configurable strategy
- **Trade Analysis**: Weekly roster optimization using pure greedy algorithm with trade suggestions
- **Advanced Data Collection**: Week-by-week player projections with automatic fallbacks and data preservation
- **Multi-Format Export**: CSV, Excel, JSON outputs with timestamped historical data

## 🎯 League Format ("Start 7 Fantasy League")

**Roster Structure:**
- **Total Players**: 15 (14 players + 1 defense)
- **Starting Lineup**: 7 players + 1 kicker + 1 defense each week
  - 1 Quarterback
  - 2 Running Backs  
  - 2 Wide Receivers
  - 1 Tight End
  - 1 FLEX (Wide Receiver OR Running Back)
  - 1 Kicker
  - 1 Defense/Special Teams
- **Bench**: 6 slots for backups
- **Reserve**: 3 slots for injured players
- **League Size**: 10 teams

## 🚀 Quick Start

### Prerequisites
- Python 3.13.6 or later
- Windows environment (paths configured for Windows)
- Internet connection for ESPN API access

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd FantasyFootballHelperScripts

# Set up virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
.venv\Scripts\pip.exe install -r requirements.txt
```

### Initial Setup (Start of Season)
```bash
# 1. Update bye weeks (manual, once per season)
# Edit shared_files/bye_weeks.csv with current season bye weeks

# 2. Fetch initial player data from ESPN
.venv\Scripts\python.exe run_player_data_fetcher.py

# 3. Configure for draft mode
# Edit draft_helper/config.py: set TRADE_HELPER_MODE = False

# 4. Run draft assistant
.venv\Scripts\python.exe run_draft_helper.py
```

## 📊 Core Scripts

### 1. Player Data Fetcher
**File**: `run_player_data_fetcher.py`
**Purpose**: Fetches player projections using advanced week-by-week calculation system from ESPN API
**When to Run**: 1-2 times per week before games start (8-15 minutes processing time)

```bash
.venv\Scripts\python.exe run_player_data_fetcher.py
```

**Features**:
- **Week-by-Week Projections**: Optimized system with 646 API calls vs. legacy 10,336 calls
- **Automatic Fallbacks**: Uses remaining season projections when week-by-week data unavailable
- **Data Preservation**: Maintains drafted/locked player status between updates
- **Multi-Format Export**: CSV, Excel, JSON with timestamped historical data

**Output**:
- `shared_files/players.csv` (master database)
- `player-data-fetcher/data/` (timestamped exports in multiple formats)

### 2. Draft Helper
**File**: `run_draft_helper.py`  
**Purpose**: Dual-mode tool for draft assistance and trade analysis  
**Modes**: Draft mode (initial draft) or Trade mode (weekly analysis)

#### Draft Mode (Initial Season)
```bash
# Set TRADE_HELPER_MODE = False in draft_helper/config.py
.venv\Scripts\python.exe run_draft_helper.py
```

#### Trade Mode (Weekly Analysis)  
```bash
# Set TRADE_HELPER_MODE = True in draft_helper/config.py
.venv\Scripts\python.exe run_draft_helper.py
```

**Features**:
- **Pure Greedy Optimization**: Simple, efficient trade algorithm without complex lookahead
- **Position-based Recommendations**: Configurable draft strategy by round with FLEX eligibility
- **Injury Risk Assessment**: Configurable penalties for different injury statuses
- **Trade Impact Analysis**: Direct trade suggestions with runner-up alternatives
- **Roster Validation**: Automatic enforcement of "Start 7 Fantasy League" rules

### 3. NFL Scores Fetcher  
**File**: `run_nfl_scores_fetcher.py`  
**Purpose**: Compiles NFL game scores for external spreadsheet analysis  
**When to Run**: As needed for data compilation

```bash
.venv\Scripts\python.exe run_nfl_scores_fetcher.py
```

**Output**: 
- `nfl-scores-fetcher/data/` (CSV, JSON, Excel formats)

## 🔧 Configuration System

**Modular Configuration Architecture**: Each module has its own config.py file with centralized management and validation.

### Player Data Fetcher (`player-data-fetcher/config.py`)
**Week-by-Week System Settings**:
- `CURRENT_NFL_WEEK`: Update weekly (most important setting)
- `USE_WEEK_BY_WEEK_PROJECTIONS`: Enable advanced projection system
- `USE_REMAINING_SEASON_PROJECTIONS`: Use remaining games vs. full season
- `RECENT_WEEKS_FOR_AVERAGE`: Number of weeks for projection averaging

**Data Management**:
- `PRESERVE_DRAFTED_VALUES`: Keep draft status between updates
- **Dual Performance Optimizations**:
  - `SKIP_DRAFTED_PLAYER_UPDATES`: Skip API calls for drafted=1 players
  - `USE_SCORE_THRESHOLD`: Skip API calls for low-scoring players, preserve existing data
  - `PLAYER_SCORE_THRESHOLD`: Minimum fantasy points to trigger API update (default: 15.0)
- **ESPN API settings**: Season, scoring format (PPR/Standard/Half)
- **Output formats**: CSV, Excel, JSON with condensed Excel option

### Draft Helper (`draft_helper/config.py`)
**Trade Optimization**:
- `TRADE_HELPER_MODE`: Switch between draft/trade modes
- `MIN_TRADE_IMPROVEMENT`: Point threshold for trade suggestions
- `NUM_TRADE_RUNNERS_UP`: Number of alternative trades to show

**Draft Strategy**:
- `DRAFT_ORDER`: Position priorities by round (frequently modified)
- `MAX_POSITIONS`: Roster limits for each position
- `INJURY_PENALTIES`: Risk tolerance for LOW/MEDIUM/HIGH injury statuses

### NFL Scores Fetcher (`nfl-scores-fetcher/config.py`)
- **Season settings**: Current week, season type, completed games filter
- **API configuration**: Timeout, rate limiting
- **Output preferences**: Multiple data formats and directories

## 📅 Typical Workflow

### Season Start (August)
1. **Update bye weeks** in `shared_files/bye_weeks.csv`
2. **Set draft mode**: `TRADE_HELPER_MODE = False`  
3. **Fetch player data**: Run player data fetcher
4. **Draft your team**: Use draft helper interactively

### Weekly During Season (September-December)
1. **Update roster**: Manually sync `shared_files/players.csv` with NFL Fantasy changes
2. **Set trade mode**: `TRADE_HELPER_MODE = True`
3. **Fetch updated data**: Run player data fetcher (1-2x per week)  
4. **Analyze trades**: Run draft helper to see recommendations
5. **Compile scores**: Run NFL scores fetcher as needed

## 🛠️ Advanced Features

### Strategy Customization
Fine-tune your approach by editing `draft_helper/config.py`:

```python
# Week-by-Week System (player-data-fetcher/config.py)
CURRENT_NFL_WEEK = 3  # Update this weekly!
USE_WEEK_BY_WEEK_PROJECTIONS = True  # Advanced projection system

# Dual Performance Optimizations (player-data-fetcher/config.py)
SKIP_DRAFTED_PLAYER_UPDATES = True  # Skip API calls for drafted=1 players
USE_SCORE_THRESHOLD = True  # Skip API calls for low-scoring players
PLAYER_SCORE_THRESHOLD = 30.0  # Only update players with 30+ fantasy points

# Draft Strategy (draft_helper/config.py)
DRAFT_ORDER[0] = {RB: 1.2, FLEX: 0.8}  # Aggressive early RB strategy
INJURY_PENALTIES = {"MEDIUM": 40, "HIGH": 80}  # Conservative injury approach
MIN_TRADE_IMPROVEMENT = 15  # High trade threshold (only strong trades)
```

### Modern Architecture Features
- **Async Operations**: High-performance data fetching with httpx and aiofiles
- **Pydantic Models**: Type-safe data validation and serialization
- **Modular Design**: Independent modules with clean interfaces
- **Data Preservation**: Draft/locked status maintained between updates
- **Historical Tracking**: Timestamped exports with projection history
- **Configuration Validation**: Built-in validation for each module

### Performance Optimizations
- **Week-by-Week System**: 646 API calls vs. legacy 10,336 calls (16x improvement)
- **Dual Optimization System**:
  - **Drafted Player Skipping**: Skip API calls for drafted=1 players
  - **Score Threshold Filtering**: Preserve existing data for players below threshold (default: 15 points)
  - **Combined Effect**: Can reduce API calls from 646 to 100-200 depending on configuration
- **Smart Data Preservation**: Always updates roster players (drafted=2) regardless of score threshold
- **Async Processing**: Concurrent data fetching and export operations
- **Fallback Systems**: Graceful degradation when API data unavailable

## 📁 Project Structure

```
FantasyFootballHelperScripts/
├── run_*.py                    # Wrapper scripts (run these)
├── config.py                   # Shared configuration (file paths only)
├── requirements.txt           # Python dependencies
├── shared_files/               # Shared data and models
│   ├── players.csv            # Master player database
│   ├── bye_weeks.csv          # NFL bye week schedule (manual updates)
│   └── FantasyPlayer.py       # Shared player data model
├── draft_helper/              # Draft and trade analysis
│   ├── config.py              # Strategy, roster, trade settings
│   ├── draft_helper.py        # Core draft/trade logic
│   ├── FantasyTeam.py         # Roster management and validation
│   └── draft_helper_constants.py # Configuration imports
├── player-data-fetcher/       # ESPN player data collection (modular)
│   ├── config.py              # Week-by-week, API, export settings
│   ├── data_fetcher-players.py # Main async fetcher script
│   ├── espn_client.py         # ESPN API client with retry logic
│   ├── models.py              # Pydantic data models
│   ├── data_exporter.py       # Multi-format async export
│   └── data/                  # Timestamped projection exports
└── nfl-scores-fetcher/        # NFL game scores collection (modular)
    ├── config.py              # Scores API and export settings
    ├── data_fetcher-scores.py # Main async scores script
    ├── nfl_api_client.py      # NFL API client
    ├── models.py              # Game score data models
    ├── data_exporter.py       # Scores export functionality
    └── data/                  # Game scores exports
```

## 🔍 Troubleshooting

### Week-by-Week Projection System
**Expected Performance**: 8-15 minutes to process ~646 players
**API Optimization**: Single call per player (not per week)
**Normal Behavior**: Some players may lack complete week-by-week data

**🔥 Weekly Maintenance Checklist**:
- ✅ Update `CURRENT_NFL_WEEK` every Tuesday in `player-data-fetcher/config.py`
- ✅ Verify `USE_REMAINING_SEASON_PROJECTIONS = True` during season
- ✅ Run player data fetcher 1-2x per week before games

### Common Issues

**Outdated Week Number**: Most common issue - update `CURRENT_NFL_WEEK` weekly
**Week-by-Week Timeouts**: If fetcher takes >20 minutes, set `USE_WEEK_BY_WEEK_PROJECTIONS = False` temporarily
**Import Errors**: Ensure all config files exist with required settings
**Path Issues**: Verify `shared_files/players.csv` exists and is accessible
**ESPN API Issues**: Check internet connection; ESPN API is free but unofficial
**Roster Math Errors**: Ensure position limits in config add up correctly

**Week-by-Week System Notes**:
- Some players may show "Using remaining_season fallback" - this is normal
- System automatically falls back to legacy methods if week-by-week data unavailable
- Performance: 646 optimized API calls (1 per player) vs 10,336 in original implementation  

### Testing After Changes
```bash
# Test all core functionality
.venv\Scripts\python.exe run_player_data_fetcher.py
# Verify: DST teams have realistic points (>50)

.venv\Scripts\python.exe run_draft_helper.py  
# Verify: Shows correct mode, no import errors

.venv\Scripts\python.exe run_nfl_scores_fetcher.py
# Verify: Fetches recent games successfully
```

## 📈 Data Sources & Architecture

### ESPN APIs (Free, No Authentication Required)
- **Fantasy API**: Player projections, injury status, team assignments (real-time)
- **Scores API**: NFL game results and schedules (automated)
- **Week-by-Week Data**: Individual week projections with automatic fallbacks

### Manual Data Management
- **Bye Weeks**: Season schedule in `shared_files/bye_weeks.csv` (update pre-season)
- **Roster Changes**: Manual sync of `shared_files/players.csv` with NFL Fantasy updates

### Technical Architecture
- **Async/Await**: httpx client with tenacity retry logic for resilient API calls
- **Type Safety**: Pydantic models for data validation and serialization
- **Export Pipelines**: aiofiles for concurrent multi-format data export
- **Configuration Management**: Modular config system with validation

## 🚀 Recent Improvements

### Version 2.0+ Features
- **Massive Performance Improvements**:
  - Week-by-week system (646 vs 10,336 API calls = 16x improvement)
  - Score threshold optimization (can reduce to 100-200 calls = additional 3-6x improvement)
- **Pure Greedy Trade Algorithm**: Simplified, efficient trade optimization
- **Smart Data Management**:
  - Preserve existing data for low-scoring players
  - Always update roster players regardless of score threshold
  - Advanced drafted/locked player handling
- **Multi-Format Export**: Concurrent CSV, Excel, JSON export with timestamps
- **Configurable Fallbacks**: Graceful handling of missing API data

## 🤝 Contributing

This is a personal fantasy football tool optimized for a specific league format:
1. **Test thoroughly**: All configuration changes should be validated across modules
2. **Update documentation**: Maintain README.md and CLAUDE.md for any changes
3. **Preserve data**: Maintain backward compatibility with existing CSV/data files
4. **Follow patterns**: Use existing modular architecture and async patterns

---

**Built for the 2025 NFL season**
**Python 3.13.6 • Modular Architecture • Async Operations**
**Optimized for 10-team "Start 7 Fantasy League" format**