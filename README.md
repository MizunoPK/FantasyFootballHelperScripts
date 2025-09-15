# Fantasy Football Helper Scripts

A comprehensive suite of tools for managing a "Start 7 Fantasy League" through data-driven draft assistance and trade analysis.

## 🏈 What This Does

This project provides automated fantasy football analysis for a **10-team "Start 7 Fantasy League"** using real-time ESPN data. It helps with:

- **Draft Planning**: Interactive draft assistant with position-based recommendations
- **Trade Analysis**: Weekly roster optimization and trade suggestions  
- **Data Collection**: Automated player projections and NFL scores compilation

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
**Purpose**: Fetches player projections, injury status, and team data from ESPN API  
**When to Run**: 1-2 times per week before games start

```bash
.venv\Scripts\python.exe run_player_data_fetcher.py
```

**Output**: 
- `shared_files/players.csv` (master database)
- `player-data-fetcher/data/` (timestamped exports)

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
- Position-based draft recommendations
- Configurable draft strategy by round
- Injury risk assessment and penalties
- Trade impact analysis and suggestions
- Roster validation and optimization

### 3. NFL Scores Fetcher  
**File**: `run_nfl_scores_fetcher.py`  
**Purpose**: Compiles NFL game scores for external spreadsheet analysis  
**When to Run**: As needed for data compilation

```bash
.venv\Scripts\python.exe run_nfl_scores_fetcher.py
```

**Output**: 
- `nfl-scores-fetcher/data/` (CSV, JSON, Excel formats)

## 🔧 Configuration

Each module has its own configuration file for easy customization:

### Player Data Fetcher (`player-data-fetcher/config.py`)
- **ESPN API settings**: Season, scoring format (PPR/Standard)
- **Output formats**: CSV, Excel, JSON options
- **Fallback scoring**: Custom point calculations when API data missing

### Draft Helper (`draft_helper/config.py`)  
- **Mode switching**: `TRADE_HELPER_MODE` (True/False)
- **Draft strategy**: `DRAFT_ORDER` position priorities by round
- **Risk tolerance**: `INJURY_PENALTIES` for different injury statuses
- **Trade sensitivity**: `MIN_TRADE_IMPROVEMENT` threshold

### NFL Scores Fetcher (`nfl-scores-fetcher/config.py`)
- **Season settings**: Current week, season type
- **Output preferences**: Data formats and directories

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
# Aggressive early RB strategy
DRAFT_ORDER[0] = {RB: 1.2, FLEX: 0.8}

# Conservative injury approach  
INJURY_PENALTIES = {"MEDIUM": 40, "HIGH": 80}

# High trade threshold (only strong trades)
MIN_TRADE_IMPROVEMENT = 15
```

### Data Persistence
- **Draft status**: Preserved between data updates
- **Player locks**: Optional preservation of manual player locks
- **Historical data**: Timestamped exports maintain projection history

### Validation & Testing
Built-in configuration validation ensures:
- Roster math adds up correctly
- Draft order matches total players
- Required data files exist
- API connectivity works

## 📁 Project Structure

```
FantasyFootballHelperScripts/
├── run_*.py                    # Wrapper scripts (run these)
├── config.py                   # Shared configuration
├── shared_files/               # Shared data and models
│   ├── players.csv            # Master player database
│   ├── bye_weeks.csv          # NFL bye week schedule
│   └── FantasyPlayer.py       # Player data model
├── draft_helper/              # Draft and trade analysis
│   ├── config.py              # Strategy and roster settings
│   ├── draft_helper.py        # Core logic
│   └── FantasyTeam.py         # Roster management
├── player-data-fetcher/       # ESPN player data collection
│   ├── config.py              # API and output settings
│   └── data_fetcher-players.py # Main fetcher script
├── nfl-scores-fetcher/        # NFL game scores collection
│   ├── config.py              # Scores API settings
│   └── data_fetcher-scores.py # Main scores script
└── requirements.txt           # Python dependencies
```

## 🔍 Troubleshooting

### Common Issues

**Import Errors**: Ensure all config files exist with required settings  
**Path Issues**: Verify `shared_files/players.csv` exists and is accessible  
**ESPN API Issues**: Check internet connection; ESPN API is free but unofficial  
**Roster Math Errors**: Ensure position limits in config add up correctly  

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

## 📈 Data Sources

- **ESPN Fantasy API**: Player projections, injury status, team assignments (automated)
- **ESPN Scores API**: NFL game results and schedules (automated)  
- **Manual Input**: Bye week schedule and roster changes from NFL Fantasy

## 🤝 Contributing

This is a personal fantasy football tool, but contributions are welcome:
1. Test configuration changes thoroughly
2. Update documentation for new features  
3. Maintain backward compatibility with existing data files

---

**Built for the 2025 NFL season with Python 3.13.6**  
**Optimized for 10-team "Start 7 Fantasy League" format**