# CLAUDE.md

Fantasy Football Helper Scripts - Technical reference for Claude Code

---

## Quick Start

**Environment**: Python 3.13.6, `.venv/` virtual environment
**Run from**: Repository root directory

```bash
# Setup
.venv\Scripts\activate
.venv\Scripts\pip.exe install -r requirements.txt

# Weekly routine: Update CURRENT_NFL_WEEK in shared_files/configs/shared_config.py

# Core scripts (all via run_*.py wrappers)
.venv\Scripts\python.exe run_player_data_fetcher.py  # Fetch projections (8-15 min)
.venv\Scripts\python.exe run_draft_helper.py         # Draft/trade mode
.venv\Scripts\python.exe run_starter_helper.py       # Optimal lineup (<1 sec)
.venv\Scripts\python.exe run_nfl_scores_fetcher.py   # NFL scores
```

---

## Architecture Overview

### Core Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **player-data-fetcher/** | ESPN projections | Week-by-week API (646 calls vs 10,336), async, weeks 1-17 only |
| **draft_helper/** | Draft/trade analysis | 7-step scoring, menu system, simulation engine |
| **starter_helper/** | Weekly lineups | 3-step scoring (projections + matchups + injuries) |
| **nfl-scores-fetcher/** | Game data | Async score collection for analysis |
| **shared_files/** | Shared code | FantasyPlayer, calculators, utilities |

### Key Data Files

- `shared_files/players.csv` - Master player database (preserved between updates)
- `shared_files/bye_weeks.csv` - NFL bye schedule (manual, pre-season)
- `shared_files/teams.csv` - Team rankings and matchups (manual, weekly)

---

## Critical Configurations

### Weekly Update Required
```python
# shared_files/configs/shared_config.py - Update every Tuesday
CURRENT_NFL_WEEK = 5  # Current week (1-18)
```

### Draft Helper Modes
```python
# shared_files/configs/draft_helper_config.py
TRADE_HELPER_MODE = False  # Draft mode (initial roster)
TRADE_HELPER_MODE = True   # Trade mode (weekly optimization)
```

### Frequently Modified Settings

**Player Data Fetcher** (`shared_files/configs/player_data_fetcher_config.py`):
- `SKIP_DRAFTED_PLAYER_UPDATES = True` - Skip API for drafted=1 players
- `USE_SCORE_THRESHOLD = True` - Only update high-scoring players
- `PLAYER_SCORE_THRESHOLD = 15.0` - Minimum points for update

**Draft Helper** (`shared_files/configs/draft_helper_config.py`):
- `NORMALIZATION_MAX_SCALE = 100.0` - Point normalization scale
- `DRAFT_ORDER_PRIMARY_BONUS = 50` - Primary position bonus
- `DRAFT_ORDER_SECONDARY_BONUS = 25` - Secondary position bonus
- `INJURY_PENALTIES = {"LOW": 0, "MEDIUM": 25, "HIGH": 50}`
- `APPLY_INJURY_PENALTY_TO_ROSTER = False` - Roster injury toggle
- `ENABLE_CONSISTENCY_SCORING = True` - CV-based volatility scoring
- `CONSISTENCY_MULTIPLIERS = {"LOW": 1.08, "MEDIUM": 1.00, "HIGH": 0.92}`

**Starter Helper** (`shared_files/configs/starter_helper_config.py`):
- `MATCHUP_MULTIPLIERS` - Matchup impact (0.8x to 1.2x)
- `STARTER_HELPER_ACTIVE_STATUSES = ['ACTIVE', 'QUESTIONABLE']`

**File Management** (`shared_files/configs/shared_config.py`):
- `DEFAULT_FILE_CAPS = 5` - Files per type (CSV, JSON, XLSX)
- `ENABLE_FILE_CAPS = True` - Automatic cleanup
- `DRY_RUN_MODE = False` - Test without deletion

---

## Scoring Systems

### Draft Helper: Add to Roster (8 steps)
1. **Normalize** fantasy points (0-100 scale)
2. **ADP multiplier** (1.15x excellent, 1.08x good, 0.92x poor)
3. **Player rating multiplier** (1.20x excellent, 1.10x good, 0.90x poor)
4. **Team quality multiplier** (1.12x excellent, 1.06x good, 0.94x poor)
5. **Consistency multiplier** (1.08x LOW volatility, 1.00x MEDIUM, 0.92x HIGH)
6. **Draft order bonus** (position-specific by round)
7. **Bye week penalty** (10-20 points, draft only)
8. **Injury penalty** (0/25/50 points by risk level)

### Draft Helper: Trade/Waiver (7 steps)
Same as above **without** Draft Order bonus (step 6)

### Starter Helper (4 steps)
1. **Base projections** from weekly CSV data
2. **Matchup multiplier** (offense rank vs defense rank)
3. **Consistency multiplier** (1.08x LOW volatility, 1.00x MEDIUM, 0.92x HIGH)
4. **Binary injury filter** (zero out non-ACTIVE/QUESTIONABLE)

---

## League Rules ("Start 7 Fantasy League")

**Roster**: 15 total (14 players + 1 DST)
**Starters**: 1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX (RB/WR only), 1 K, 1 DST
**Bench**: 6 slots
**Reserve**: 3 slots (injured)

**Position Limits** (`shared_files/configs/draft_helper_config.py`):
```python
MAX_POSITIONS = {
    QB: 2, RB: 4, WR: 4, FLEX: 1, TE: 2, K: 1, DST: 1
}
```

---

## Common Workflows

### 1. Season Setup (Draft)
```bash
# 1. Update bye_weeks.csv (once per season)
# 2. Configure for draft
#    - shared_files/configs/shared_config.py: CURRENT_NFL_WEEK = 1
#    - shared_files/configs/draft_helper_config.py: TRADE_HELPER_MODE = False
# 3. Fetch player data (8-15 min)
.venv\Scripts\python.exe run_player_data_fetcher.py
# 4. Run draft helper
.venv\Scripts\python.exe run_draft_helper.py
```

### 2. Weekly Trade Analysis
```bash
# 1. Update CURRENT_NFL_WEEK in shared_files/configs/shared_config.py (every Tuesday!)
# 2. Configure for trade mode
#    - shared_files/configs/draft_helper_config.py: TRADE_HELPER_MODE = True
# 3. Fetch updated data (1-2x per week)
.venv\Scripts\python.exe run_player_data_fetcher.py
# 4. Update players.csv with roster changes
# 5. Run trade analysis
.venv\Scripts\python.exe run_draft_helper.py
```

### 3. Weekly Lineup Optimization
```bash
# 1. Update CURRENT_NFL_WEEK in shared_files/configs/shared_config.py
# 2. Update teams.csv with this week's matchups/rankings
# 3. Run starter helper
.venv\Scripts\python.exe run_starter_helper.py
```

### 4. Running Parameter Optimization Simulations
```bash
# 1. Create or select parameter configuration JSON file
# 2. Run simulation with configuration
python run_simulation.py draft_helper/simulation/parameters/baseline_parameters.json

# Available configurations:
# - baseline_parameters.json: Conservative default values (single values)
# - parameter_template.json: Template with 2-value ranges for testing

# 3. After simulation completes, tell Claude "new simulation result file is ready"
# 4. Claude analyzes results, updates execution tracker, generates next iteration
```

**Parameter Configuration Format**:
- JSON files stored in `draft_helper/simulation/parameters/`
- Each parameter has a list of values to test in combinations
- All 20 parameters required (see `parameters/README.md`)
- Results saved to `draft_helper/simulation/results/` with timestamps

**Workflow**:
1. User runs: `python run_simulation.py parameters/iteration_1.json`
2. Simulation generates timestamped results file
3. User notifies Claude: "new simulation result file is ready"
4. Claude reads strategy (`simulation_optimization_strategy.md`) and tracker
5. Claude analyzes results, updates tracker with findings
6. Claude generates next parameter JSON based on optimization strategy

---

## Testing

### Run All Tests (577 tests, 100% passing)
```bash
# Complete test suite (577 tests)
.venv\Scripts\python.exe -m pytest --tb=short

# By module
.venv\Scripts\python.exe -m pytest draft_helper/tests/ -v
.venv\Scripts\python.exe -m pytest shared_files/tests/ -v
.venv\Scripts\python.exe -m pytest starter_helper/tests/ -v
```

### Startup Validation
```bash
# Verify scripts start without errors (10 sec timeout)
timeout 10 .venv\Scripts\python.exe run_player_data_fetcher.py
timeout 10 .venv\Scripts\python.exe run_nfl_scores_fetcher.py
timeout 10 .venv\Scripts\python.exe run_starter_helper.py
```

### ⚠️ AUTOMATED Pre-Commit Validation (RECOMMENDED)
**FASTEST WAY**: Run the automated validation script that checks EVERYTHING:

```bash
# Run complete validation suite (3-5 minutes)
python run_pre_commit_validation.py

# This automatically runs:
#   ✅ All unit tests (pytest)
#   ✅ Startup validation tests
#   ✅ Interactive integration tests
#   ✅ Prints colored summary with pass/fail status
```

**Exit Codes**:
- `0` = All tests passed, safe to commit
- `1` = Some tests failed, DO NOT COMMIT

### Manual Pre-Commit Validation (Alternative)
If you prefer to run tests manually:

**1. Unit Tests**:
```bash
python -m pytest --tb=short
```

**2. Startup Tests**:
```bash
timeout 10 python run_player_data_fetcher.py
timeout 10 python run_nfl_scores_fetcher.py
```

**3. Interactive Integration Tests (MANDATORY)**:
```bash
# Run automated integration test sequence
echo -e "2\nHunt\n1\nexit\n3\n\n4\nHunt\n1\nHampton\n1\nexit\n1\n1\n5\n15\n16\n3\n\n5\n15\n16\n6\n\n7\n4\n8\n" | python run_draft_helper.py

# Verify success: Look for "✅ Marked", "✅ Dropped", "✅ Successfully added", "Goodbye!"
```

**Why Interactive Tests Are Required**: They catch menu bugs, CSV persistence issues, and workflow problems that unit tests miss.

### Pre-Commit Validation Checklist
Complete checklist available in `tests/pre_commit_validation_checklist.md`

**DO NOT SKIP** the interactive tests. They are required for every commit.

---

## Key Classes & Components

**FantasyPlayer** (`shared_files/FantasyPlayer.py`)
- Player data model with projections, injury status, team info
- Weeks 1-17 projections, drafted status (0=available, 1=drafted by others, 2=your team)

**DraftHelper** (`draft_helper/draft_helper.py`)
- Core draft/trade logic with 8-option interactive menu
- Integrates scoring engine, roster manager, menu system

**ScoringEngine** (`draft_helper/core/scoring_engine.py`)
- Implements 7-step Add to Roster and 6-step Trade/Waiver scoring
- Manages NormalizationCalculator, DraftOrderCalculator, enhanced scorers

**ByeWeekVisualizer** (`draft_helper/core/bye_week_visualizer.py`)
- Generates bye week summaries for roster display
- Detects bye week conflicts (multiple starters at same position)
- Shows weeks >= current week through week 18
- Used in waiver optimizer and trade simulator

**LineupOptimizer** (`starter_helper/lineup_optimizer.py`)
- Optimal lineup generation with 3-step scoring
- FLEX optimization, matchup calculations, bench recommendations

**MatchupCalculator** (`starter_helper/matchup_calculator.py`)
- Calculates matchup multipliers (team offense vs opponent defense)
- Reads from teams.csv, applies position-specific adjustments

---

## Troubleshooting

### Common Issues

**Player data fetcher timeouts** → Set `USE_WEEK_BY_WEEK_PROJECTIONS = False`
**Inconsistent player points** → Verify `CURRENT_NFL_WEEK` is correct
**Import errors in tests** → Run tests from repository root
**Flaky tests** → Some tests have import path dependencies, run individually
**Roster math errors** → Verify `MAX_POSITIONS` sums correctly

### Configuration Validation
Each config file has built-in validation. Check logs for specific errors.

---

## Performance Optimizations

**API Calls**: 646 (week-by-week) vs 10,336 (legacy)
**Optimizations**:
- Skip drafted=1 players: ~100-200 fewer calls
- Score threshold: Only update high-scoring players
- Concurrent export: Async file writing
- Smart caching: Preserves existing data

**File Management**: Auto-cleanup keeps ~5 files per type (vs 270+ without)

---

## Dependencies

**Core**:
- `httpx>=0.24.0` - Async HTTP
- `aiofiles>=23.0.0` - Async file I/O
- `pandas>=2.0.0` - Data manipulation
- `pydantic>=2.0.0` - Type validation
- `tenacity>=8.2.0` - Retry logic
- `openpyxl>=3.1.0` - Excel export

---

## Project-Specific Rules

### When User Requests "Update" from File
1. Read file from `potential_updates/` folder
2. Create TODO in `todo-files/` before starting
3. Follow `potential_updates/rules.txt`
4. Track progress for multi-session work

### Commit Standards
- Brief, descriptive messages (50 chars or less)
- No emojis or subjective prefixes
- Do NOT include "Generated with Claude Code" and co-author tag
- List major changes in body

### Pre-Commit Protocol
**🚨 MANDATORY BEFORE EVERY COMMIT**

When the user requests to commit changes (e.g., "commit changes", "verify and commit", "commit this"):

**STEP 1: Run Automated Validation Script (REQUIRED)**
```bash
python run_pre_commit_validation.py
```

This single command validates EVERYTHING:
- ✅ All unit tests across all modules
- ✅ Startup validation for core scripts
- ✅ Interactive integration tests
- ✅ Exit code 0 = safe to commit, 1 = DO NOT COMMIT

**Only proceed to commit if the script returns exit code 0.**

**STEP 2: If Validation Passes, Commit Changes**
1. Analyze all changes with `git status` and `git diff`
2. Update documentation (README.md, CLAUDE.md) if functionality changed
3. Stage and commit with clear, concise message
4. Follow commit standards (see below)

**STEP 3: If Validation Fails**
- **STOP** - Do NOT commit
- Fix failing tests or issues
- Re-run `python run_pre_commit_validation.py`
- Only commit when exit code is 0

**Alternative Manual Method**: If the automated script cannot be used, follow all steps in `tests/pre_commit_validation_checklist.md` manually.

**Do NOT skip validation**: The automated script ensures code quality and system stability

### Fantasy Football Development
After code changes:
- Update module README if functionality changed
- Run relevant test modules
- Test core functionality (player data, draft, starter helper)
- Update configuration docs for new settings

---

## File Structure

```
FantasyFootballHelperScripts/
├── run_*.py                        # Wrapper scripts
├── shared_files/                   # Shared utilities
│   ├── configs/                   # Centralized configuration
│   │   ├── shared_config.py       # Shared settings (CURRENT_NFL_WEEK, etc.)
│   │   ├── draft_helper_config.py
│   │   ├── starter_helper_config.py
│   │   ├── player_data_fetcher_config.py
│   │   └── nfl_scores_fetcher_config.py
│   ├── players.csv                # Master player DB
│   ├── bye_weeks.csv              # Bye schedule
│   ├── teams.csv                  # Team data
│   └── *.py                       # Shared classes
├── player-data-fetcher/           # ESPN data fetching
│   └── data/                      # Export files
├── draft_helper/                  # Draft/trade analysis
│   ├── core/                      # Scoring engine
│   ├── simulation/                # Parameter optimization
│   └── data/                      # Results
├── starter_helper/                # Weekly lineups
│   └── data/                      # Results
├── nfl-scores-fetcher/            # Game scores
│   └── data/                      # Export files
├── tests/                         # Root-level tests
├── potential_updates/             # Update tracking
│   ├── todo-files/                # Progress tracking
│   └── done/                      # Completed updates
└── .venv/                         # Virtual environment
```

---

## Recent Major Changes

**Bye Week Visualizer** (Oct 2025): Added bye week summaries to waiver optimizer and trade simulator with conflict detection
**Centralized Config** (Oct 2025): All config files moved to `shared_files/configs/` for better organization
**JSON-Based Simulation** (Sept 2025): Parameter configs now use JSON files, removed PARAMETER_RANGES from code
**Simulation Config** (Sept 2025): Reduced all parameters to 2-value ranges for efficient optimization
**Enhanced Scoring** (Sept 2025): Fixed missing config keys, 100% test pass rate
**Starter Helper Overhaul** (Sept 2025): 3-step scoring with matchup multipliers
**Modular Scoring** (Sept 2025): Separate calculator classes with 79 tests
**Week-by-Week System** (2025): 16x API performance improvement

---

## Additional Resources

**Full optimization strategy**: `potential_updates/simulation_optimization_strategy.md`
**Execution tracker**: `potential_updates/simulation_execution_tracker.md`
**Parent rules**: `C:\Users\kmgam\Code\CLAUDE.md`
**User rules**: `C:\Users\kmgam\.claude\CLAUDE.md`

---

**Version**: 2.0 Condensed
**Last Updated**: 2025-09-30
**Maintenance**: Update after major features, config changes, or workflow updates
