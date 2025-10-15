# Fantasy Football League Helper - Project Documentation

**For Claude Agents: Complete Guide to Understanding and Contributing**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Current Status & Refactor Progress](#current-status--refactor-progress)
3. [Architecture & Design Philosophy](#architecture--design-philosophy)
4. [Project Structure](#project-structure)
5. [Core Systems](#core-systems)
6. [Configuration Management](#configuration-management)
7. [Data Flow & Dependencies](#data-flow--dependencies)
8. [Mode Managers (League Helper Modules)](#mode-managers-league-helper-modules)
9. [Scoring System](#scoring-system)
10. [Testing Strategy](#testing-strategy)
11. [Development Guidelines](#development-guidelines)
12. [Migration Reference (Old → New)](#migration-reference-old--new)
13. [Common Tasks & Examples](#common-tasks--examples)

---

## Project Overview

### Purpose
A comprehensive suite of tools for managing a **"Start 7 Fantasy League"** (10-team fantasy football league) through data-driven analysis, draft assistance, and weekly roster optimization.

### League Format
- **Total Roster**: 15 players (14 players + 1 DST)
- **Starting Lineup**: 1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX (RB/WR only), 1 K, 1 DST
- **Bench**: 6 slots
- **Reserve**: 3 slots (injured players)
- **League Size**: 10 teams

### Key Features
- **League Helper**: Interactive multi-mode application for draft, roster management, and analysis
- **Player Data Fetcher**: Automated ESPN API data collection with week-by-week projections
- **NFL Scores Fetcher**: Game score compilation for analysis
- **Simulation System**: (Future) Parameter optimization through season simulations

---

## Current Status & Refactor Progress

### 🚧 **ACTIVE REFACTOR IN PROGRESS** 🚧

The project is undergoing a major architectural redesign from a monolithic "Draft Helper" to a modular "League Helper" system.

### Completion Status

#### ✅ **Fully Migrated** (Production Ready)
- **Player Data Fetcher** (`player-data-fetcher/`)
  - ESPN API integration with week-by-week projections
  - Multi-format export (CSV, JSON, Excel)
  - Entry point: `run_player_fetcher.py`

- **NFL Scores Fetcher** (`nfl-scores-fetcher/`)
  - Game score collection
  - Entry point: `run_scores_fetcher.py`

#### 🏗️ **In Development** (Partially Complete)
- **League Helper Core Architecture** (`league_helper/`)
  - ✅ Main entry point: `run_league_helper.py`
  - ✅ Core managers: `LeagueHelperManager`, `ConfigManager`, `PlayerManager`, `TeamDataManager`
  - ✅ Scoring system fully replicated in `PlayerManager.score_player()`
  - ⚠️ **Needs testing** - Scoring logic needs validation

- **Add to Roster Mode** (`league_helper/add_to_roster_mode/`)
  - ✅ Basic implementation complete
  - ⚠️ **Needs testing** - Requires validation before production use
  - Status: First mode implemented, others will follow this pattern

#### ❌ **Not Yet Implemented** (Stub Files Only)
- **Mark Drafted Player Mode** (`league_helper/mark_drafted_player_mode/`)
- **Waiver Optimizer Mode** (`league_helper/waiver_optimizer_mode/`)
- **Drop Player Mode** (`league_helper/drop_player_mode/`)
- **Lock/Unlock Player Mode** (`league_helper/lock_player_mode/`)
- **Starter Helper Mode** (`league_helper/starter_helper_mode/`)
- **Trade Simulator Mode** (`league_helper/trade_simulator_mode/`)

#### 🔮 **Future Work** (Planned Overhaul)
- **Simulation System** (`simulation/`)
  - Will be completely redesigned to match new architecture
  - Will remain a separate tool (not integrated into League Helper)

### Old Structure Reference
- **Location**: `old_structure/` directory
- **Status**: Reference only - will be deleted after refactor completes
- **Use cases**:
  - Understanding unimplemented mode logic
  - Migration reference for stub modes
  - Testing behavior comparison

---

## Architecture & Design Philosophy

### Design Goals

1. **Modularity**: Each mode is an independent manager with clear responsibilities
2. **Maintainability**: Clean separation of concerns, explicit dependencies
3. **Testability**: Each component can be tested independently
4. **Extensibility**: Easy to add new modes without affecting existing code
5. **Simulation-Friendly**: JSON configuration enables easy parameter testing

### Why the Refactor?

The original `draft_helper` was organically grown:
- Started as a single mode (Add to Roster)
- Features were continuously patched in without architectural planning
- Became monolithic and hard to maintain
- Mixed responsibilities across modules

The new `league_helper` is intentionally designed:
- Purpose-built architecture based on known requirements
- Modular mode system for easy extension
- Clear data flow and responsibility boundaries
- Eliminates unnecessary or poorly-designed code

### Architectural Principles

#### Separation of Concerns
```
LeagueHelperManager (orchestration)
    ↓
ModeManagers (business logic)
    ↓
PlayerManager/ConfigManager/TeamDataManager (domain logic)
    ↓
FantasyPlayer/FantasyTeam (data models)
```

#### Dependency Flow
- **Root `utils/`**: Shared across ALL top-level scripts (league_helper, player-fetcher, scores-fetcher)
- **`league_helper/util/`**: Shared across ALL modes within League Helper
- **Mode managers**: Can depend on both `utils/` and `league_helper/util/`

#### Configuration Philosophy
- **Single Source of Truth**: `data/league_config.json`
- **JSON-Based**: Enables easy config swapping for simulations
- **Validated on Load**: ConfigManager validates structure and required fields
- **No Environment Variations**: One config file for all environments

---

## Project Structure

```
FantasyFootballHelperScripts/
├── run_league_helper.py          # 🎯 NEW: Main entry point for League Helper
├── run_player_fetcher.py         # ✅ MIGRATED: Player data fetcher entry
├── run_scores_fetcher.py         # ✅ MIGRATED: NFL scores fetcher entry
├── run_simulation.py             # 🔮 FUTURE: Simulation entry (to be redesigned)
│
├── data/                         # 🎯 NEW: Central data storage
│   ├── league_config.json        # ✅ Single source of truth for all settings
│   ├── players.csv               # Player database (updated by player-fetcher)
│   ├── teams.csv                 # Team rankings (manually updated weekly)
│   └── bye_weeks.csv             # Bye week schedule (manual, pre-season)
│
├── league_helper/                # 🎯 NEW: Main application
│   ├── LeagueHelperManager.py   # ✅ Main orchestrator, runs interactive menu
│   ├── constants.py              # ✅ League-wide constants
│   │
│   ├── util/                     # ✅ Shared utilities for all modes
│   │   ├── ConfigManager.py     # ✅ JSON config loader & validator
│   │   ├── PlayerManager.py     # ✅ Player scoring & management
│   │   ├── TeamDataManager.py   # ✅ Team rankings & matchup data
│   │   └── FantasyTeam.py       # ✅ Roster management & validation
│   │
│   ├── add_to_roster_mode/      # 🏗️ IN PROGRESS (needs testing)
│   │   └── AddToRosterModeManager.py
│   │
│   ├── mark_drafted_player_mode/  # ❌ STUB
│   │   └── MarkDraftedPlayerModeManager.py
│   │
│   ├── waiver_optimizer_mode/   # ❌ STUB (formerly "Trade Analysis")
│   │   └── WaiverOptimizerModeManager.py
│   │
│   ├── drop_player_mode/        # ❌ STUB
│   │   └── DropPlayerModeManager.py
│   │
│   ├── lock_player_mode/        # ❌ STUB
│   │   └── LockPlayerModeManager.py
│   │
│   ├── starter_helper_mode/     # ❌ STUB
│   │   └── StarterHelperModeManager.py
│   │
│   └── trade_simulator_mode/    # ❌ STUB
│       └── TradeSimulatorModeManager.py
│
├── utils/                        # ✅ MIGRATED: Shared across all top-level scripts
│   ├── FantasyPlayer.py         # ✅ Canonical player data model
│   ├── LoggingManager.py        # ✅ Logging configuration
│   ├── TeamData.py              # ✅ Team data structures
│   ├── csv_utils.py             # ✅ CSV operations
│   ├── data_file_manager.py     # ✅ File management utilities
│   └── error_handler.py         # ✅ Error handling utilities
│
├── player-data-fetcher/         # ✅ MIGRATED: ESPN API data collection
│   ├── config.py                # Player fetcher configuration
│   ├── player_fetcher_main.py   # Main fetcher logic
│   ├── espn_client.py           # ESPN API client
│   └── data/                    # Export directory (timestamped files)
│
├── nfl-scores-fetcher/          # ✅ MIGRATED: Game score collection
│   ├── config.py                # Scores fetcher configuration
│   ├── nfl_scores_fetcher_main.py
│   ├── nfl_api_client.py        # NFL API client
│   └── data/                    # Export directory
│
├── simulation/                   # 🔮 FUTURE: To be redesigned
│   └── SimulationManager.py     # (Current simulation - will be replaced)
│
├── old_structure/                # 📚 REFERENCE ONLY (will be deleted)
│   ├── draft_helper/            # Old monolithic implementation
│   ├── player-data-fetcher/     # (Already migrated)
│   ├── nfl-scores-fetcher/      # (Already migrated)
│   └── CLAUDE.md                # Old project documentation
│
└── 2025_compiled_data/           # ⏸️ IGNORE: Season data archive (future use)
```

---

## Core Systems

### 1. League Helper Manager

**File**: `league_helper/LeagueHelperManager.py`

**Purpose**: Main orchestrator for the interactive League Helper application.

**Responsibilities**:
- Initialize all managers (Config, Player, TeamData, Mode Managers)
- Display main menu and route user choices to appropriate mode
- Reload player data before each menu display (ensures fresh data)
- Coordinate data flow between modes

**Key Methods**:
```python
__init__(data_folder: Path)
    # Initialize all managers and mode managers

start_interactive_mode()
    # Main loop: show menu → route to mode → reload data

show_main_menu() → int
    # Display 8-option menu, return user choice

run_add_to_roster_mode()
    # Delegate to AddToRosterModeManager

# Similar methods for other 6 modes (stubs)
```

**Menu Options**:
1. Add to Roster (Draft players)
2. Mark Drafted Player (Track opponents' picks)
3. Waiver Optimizer (Weekly roster optimization)
4. Drop Player (Remove players from roster)
5. Lock/Unlock Player (Protect players from trades)
6. Starter Helper (Weekly lineup recommendations)
7. Trade Simulator (Simulate trades)
8. Quit

---

### 2. Configuration Manager

**File**: `league_helper/util/ConfigManager.py`

**Purpose**: Load, validate, and provide access to all configuration from `league_config.json`.

**Key Features**:
- **JSON-Based Configuration**: Single source of truth
- **Validation on Load**: Ensures all required fields exist
- **Type Safety**: Validates structure and data types
- **Convenience Methods**: Easy access to complex scoring parameters

**Structure**:
```python
class ConfigManager:
    # League Settings
    current_nfl_week: int
    nfl_season: int
    nfl_scoring_format: str  # "ppr", "std", "half"

    # Scoring Parameters
    normalization_max_scale: float
    base_bye_penalty: float
    injury_penalties: Dict[str, float]
    adp_scoring: Dict[str, Any]
    player_rating_scoring: Dict[str, Any]
    team_quality_scoring: Dict[str, Any]
    consistency_scoring: Dict[str, Any]
    matchup_scoring: Dict[str, Any]

    # Add to Roster Mode Settings
    draft_order_bonuses: Dict[str, float]
    draft_order: List[Dict[str, str]]
```

**Key Methods**:
```python
get_adp_multiplier(adp_val) → float
    # Return multiplier based on ADP thresholds

get_player_rating_multiplier(rating) → float
get_team_quality_multiplier(quality_rank) → float
get_consistency_multiplier(value) → float
get_matchup_multiplier(value) → float

get_draft_order_bonus(position, draft_round) → float
    # Return bonus points for position in given round

get_bye_week_penalty(num_matching_byes) → float
get_injury_penalty(risk_level) → float

get_ideal_draft_position(round_num) → str
    # Return PRIMARY position for given round
```

---

### 3. Player Manager

**File**: `league_helper/util/PlayerManager.py`

**Purpose**: Core player scoring, management, and roster operations.

**Responsibilities**:
- Load players from CSV
- Calculate consistency scores from weekly data
- Enrich players with team ranking data
- Provide player scoring (9-step system)
- Manage roster operations (draft, can_draft)
- Reload player data on demand

**Key Methods**:
```python
load_players_from_csv()
    # Load from data/players.csv, enrich with scoring data

load_team()
    # Load roster (drafted=2 players) into FantasyTeam

reload_player_data()
    # Reload CSV and refresh team (called before each menu)

score_player(player, **flags) → float
    # 9-step scoring with optional flag controls
    # Flags: adp, player_rating, team_quality, consistency,
    #        matchup, draft_round, bye, injury

can_draft(player) → bool
    # Check if player can be added to roster

draft_player(player) → bool
    # Add player to roster, update CSV

update_players_file()
    # Save players back to CSV (sorted by drafted status)

display_roster_by_draft_order()
    # Show roster organized by position slots
```

**Scoring Flags**:
Different modes use different flag combinations:
- **Add to Roster**: All enabled, draft_round > 0
- **Waiver Optimizer**: All except draft_round
- **Starter Helper**: Only matchup, consistency (no draft_round, bye, injury)
- **Trade Simulator**: Similar to Waiver Optimizer

---

### 4. Team Data Manager

**File**: `league_helper/util/TeamDataManager.py`

**Purpose**: Provide team offensive/defensive rankings and matchup calculations.

**Responsibilities**:
- Load team rankings from `data/teams.csv`
- Provide offensive and defensive rank lookups
- Calculate matchup scores (offense vs opponent defense)

**Key Methods**:
```python
get_team_offensive_rank(team_abbr) → int
    # Return offensive rank (1 = best)

get_team_defensive_rank(team_abbr) → int
    # Return defensive rank (1 = best)

get_rank_difference(team_abbr, is_defense) → int
    # Calculate matchup advantage
    # Positive = favorable matchup, Negative = unfavorable
```

---

### 5. Fantasy Team

**File**: `league_helper/util/FantasyTeam.py`

**Purpose**: Roster management, position validation, bye week tracking.

**Responsibilities**:
- Enforce roster limits by position
- Track slot assignments (handle FLEX logic)
- Validate draft eligibility
- Calculate bye week conflicts

**Key Data**:
```python
roster: List[FantasyPlayer]
    # Players on your team (drafted=2)

slot_assignments: Dict[str, List[int]]
    # Maps position slots to player IDs
    # Example: {"QB": [12345], "RB": [23456, 34567], "FLEX": [45678]}

pos_counts: Dict[str, int]
    # Current count by position
```

**Key Methods**:
```python
can_draft(player) → bool
    # Check position limits and FLEX logic

draft_player(player) → bool
    # Add to roster, update slots and counts

get_matching_byes_in_roster(bye_week, position, is_rostered) → int
    # Count roster players with same bye week and position
```

---

## Configuration Management

### league_config.json Structure

**Location**: `data/league_config.json`

**Top-Level Structure**:
```json
{
  "config_name": "Default",
  "description": "Initial default parameters",
  "parameters": {
    // All configuration goes here
  }
}
```

### Parameters Breakdown

#### League Settings
```json
"CURRENT_NFL_WEEK": 6,           // Update weekly
"NFL_SEASON": 2025,
"NFL_SCORING_FORMAT": "ppr",     // "ppr", "std", "half"
```

#### Scoring Basics
```json
"NORMALIZATION_MAX_SCALE": 123.54,  // Scale for normalized fantasy points
"BASE_BYE_PENALTY": 28.85,          // Base penalty per bye week conflict
```

#### Injury Penalties
```json
"INJURY_PENALTIES": {
  "LOW": 0,        // Healthy players (ACTIVE)
  "MEDIUM": 9.68,  // Questionable, Day-to-Day
  "HIGH": 78.22    // Out, IR, Suspended
}
```

#### Draft Order (Add to Roster Mode)
```json
"DRAFT_ORDER_BONUSES": {
  "PRIMARY": 71,    // Bonus for primary position
  "SECONDARY": 52   // Bonus for secondary position
},

"DRAFT_ORDER": [
  {"FLEX": "P", "QB": "S"},  // Round 1: Prefer FLEX, consider QB
  {"FLEX": "P", "QB": "S"},  // Round 2: Same
  ...
  {"QB": "P", "FLEX": "S"},  // Round 5: Prioritize QB
  {"K": "P"},                // Round 12: Kicker only
  {"DST": "P"}               // Round 13: Defense only
]
```

#### Threshold/Multiplier Scoring
All scoring categories follow this pattern:
```json
"ADP_SCORING": {
  "THRESHOLDS": {
    "VERY_POOR": 150,   // Lower ADP = higher threshold
    "POOR": 100,
    "GOOD": 50,
    "EXCELLENT": 20
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.5,   // 50% of base score
    "POOR": 0.82,
    "GOOD": 1.08,
    "EXCELLENT": 1.18   // 18% boost
  }
}
```

#### Scoring Categories
- **ADP_SCORING**: Average Draft Position (lower ADP = better)
- **PLAYER_RATING_SCORING**: Player rank within position (higher = better)
- **TEAM_QUALITY_SCORING**: Team offensive/defensive rank (lower = better)
- **CONSISTENCY_SCORING**: Coefficient of variation (lower = more consistent)
  - Includes `"MIN_WEEKS": 3` (minimum weeks of data required)
- **MATCHUP_SCORING**: Matchup advantage score (higher = better matchup)

### Configuration Access Pattern

```python
# In any mode manager or utility
config = ConfigManager(data_folder)

# Access league settings
week = config.current_nfl_week
season = config.nfl_season

# Get multipliers (handles threshold logic internally)
adp_mult = config.get_adp_multiplier(player.adp)
team_mult = config.get_team_quality_multiplier(player.team_offensive_rank)

# Get penalties/bonuses
injury_penalty = config.get_injury_penalty("MEDIUM")
draft_bonus = config.get_draft_order_bonus("RB", draft_round=3)
```

---

## Data Flow & Dependencies

### Application Startup Flow

```
1. User runs: python run_league_helper.py
2. run_league_helper.py imports LeagueHelperManager
3. LeagueHelperManager.__init__():
   a. Create ConfigManager(data_folder)
      → Loads & validates data/league_config.json
   b. Create TeamDataManager(data_folder)
      → Loads data/teams.csv
   c. Create PlayerManager(data_folder, config, team_data_manager)
      → Loads data/players.csv
      → Enriches each player:
         - Calculate consistency from weekly data
         - Add team offensive/defensive ranks
         - Calculate matchup scores
      → Load team (drafted=2 players)
   d. Create all 7 ModeManagers
      → Pass config, player_manager, team_data_manager as needed
4. LeagueHelperManager.start_interactive_mode()
   → Display menu loop
```

### Data Update Flow

```
Player Data Fetcher (Independent)
    ↓
Updates data/players.csv
    ↓
League Helper reloads before each menu
    ↓
PlayerManager.reload_player_data()
    ↓
Fresh data for all modes
```

### Scoring Data Flow

```
User selects "Add to Roster"
    ↓
AddToRosterModeManager.get_recommendations()
    ↓
PlayerManager.score_player(player, draft_round=current_round)
    ↓
9-Step Scoring Calculation:
    1. Normalize fantasy points (weighted_projection)
    2. Apply ADP multiplier (ConfigManager)
    3. Apply player rating multiplier (ConfigManager)
    4. Apply team quality multiplier (ConfigManager + TeamDataManager)
    5. Apply consistency multiplier (ConfigManager + PlayerManager calc)
    6. Apply matchup multiplier (ConfigManager + TeamDataManager)
    7. Add draft order bonus (ConfigManager)
    8. Subtract bye week penalty (ConfigManager + FantasyTeam)
    9. Subtract injury penalty (ConfigManager + FantasyPlayer)
    ↓
Return final score → Sort → Display top 10
```

### Dependency Graph

```
LeagueHelperManager
    ├── ConfigManager ✅
    │   └── data/league_config.json ✅
    │
    ├── TeamDataManager ✅
    │   └── data/teams.csv ✅
    │
    ├── PlayerManager ✅
    │   ├── ConfigManager ✅
    │   ├── TeamDataManager ✅
    │   ├── data/players.csv ✅
    │   └── FantasyTeam ✅
    │       └── FantasyPlayer (utils/) ✅
    │
    └── ModeManagers
        ├── AddToRosterModeManager 🏗️
        │   ├── ConfigManager ✅
        │   ├── PlayerManager ✅
        │   └── TeamDataManager ✅
        │
        ├── MarkDraftedPlayerModeManager ❌
        ├── WaiverOptimizerModeManager ❌
        ├── DropPlayerModeManager ❌
        ├── LockPlayerModeManager ❌
        ├── StarterHelperModeManager ❌
        └── TradeSimulatorModeManager ❌
```

**Legend**:
- ✅ Complete and working
- 🏗️ Implemented but needs testing
- ❌ Stub only (not implemented)

---

## Mode Managers (League Helper Modules)

### General Mode Manager Pattern

All mode managers follow this structure:

```python
class XxxModeManager:
    def __init__(self, config: ConfigManager,
                 player_manager: PlayerManager = None,
                 team_data_manager: TeamDataManager = None):
        self.config = config
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager
        self.logger = get_logger()

    def start_interactive_mode(self, player_manager, team_data_manager):
        """
        Main entry point called by LeagueHelperManager.

        Pattern:
        1. Set managers (in case they were updated)
        2. Display mode banner
        3. Show current roster state
        4. Enter mode-specific loop
        5. Return to main menu when done
        """
        self.set_managers(player_manager, team_data_manager)
        print("\n" + "="*50)
        print("MODE NAME")
        print("="*50)

        # Mode-specific logic here

        print("Returning to Main Menu...")
```

---

### 1. Add to Roster Mode

**File**: `league_helper/add_to_roster_mode/AddToRosterModeManager.py`

**Status**: 🏗️ **Implemented, needs testing**

**Purpose**: Draft players to your roster during initial season setup or when adding free agents.

**User Flow**:
1. Display roster by draft rounds (shows filled/empty slots)
2. Show top 10 recommended players (scored for current round)
3. User selects player or backs out
4. Update roster and CSV if player added
5. Loop until user returns to main menu

**Key Features**:
- **Round-Aware Scoring**: Uses draft position bonuses based on current round
- **Draft Round Tracking**: Automatically determines current round from roster slots
- **Roster Display**: Shows ideal vs actual position assignments
- **Consistency Ratings**: Displays player consistency labels (EXCELLENT/GOOD/POOR)

**Scoring Flags** (via `PlayerManager.score_player`):
```python
score_player(
    player,
    adp=True,
    player_rating=True,
    team_quality=True,
    consistency=True,
    matchup=False,      # Not used in Add to Roster
    draft_round=current_round,  # IMPORTANT: Adds draft bonus
    bye=True,
    injury=True
)
```

**Implementation Notes**:
- Uses `_match_players_to_rounds()` to assign existing roster to draft rounds
- Only PRIMARY positions from `DRAFT_ORDER` get bonuses
- FLEX eligibility: RB and WR only

**Reference**: See `old_structure/draft_helper/core/roster_manager.py` for detailed logic.

---

### 2. Mark Drafted Player Mode

**File**: `league_helper/mark_drafted_player_mode/MarkDraftedPlayerModeManager.py`

**Status**: ❌ **Stub - Not Implemented**

**Purpose**: Track opponents' draft picks by marking players as drafted=1 (unavailable).

**Expected User Flow**:
1. Prompt user for player name (partial match support)
2. Show fuzzy search results
3. User selects correct player
4. Mark player as drafted=1
5. Update CSV
6. Return to main menu or continue marking

**Key Features to Implement**:
- **Fuzzy Name Search**: Match partial first/last names (see `PlayerSearch` in old structure)
- **Confirmation**: Show player details before marking
- **Batch Mode**: Allow marking multiple players before returning
- **Undo**: Option to unmark if mistake made

**Scoring**: N/A (no scoring needed)

**CSV Update**: Set `drafted=1` for selected player

**Reference**: `old_structure/draft_helper/core/player_search.py`

---

### 3. Waiver Optimizer Mode

**File**: `league_helper/waiver_optimizer_mode/WaiverOptimizerModeManager.py`

**Status**: ❌ **Stub - Not Implemented**

**Purpose**: Weekly roster optimization - suggest beneficial trades to improve overall team score.

**Expected User Flow**:
1. Display current roster with total score
2. Run optimization algorithm
3. Show suggested trades (drop X, add Y) with score improvements
4. Show runner-up alternatives
5. User can simulate trades or return to main menu

**Key Features to Implement**:
- **Pure Greedy Algorithm**: Iteratively find best single trade
- **No Draft Bonuses**: Fair comparison without round bias
- **Locked Player Support**: Skip locked players
- **Bye Week Visualization**: Show bye week conflicts in roster
- **Trade Impact Analysis**: Before/after roster comparison

**Scoring Flags** (via `PlayerManager.score_player`):
```python
score_player(
    player,
    adp=True,
    player_rating=True,
    team_quality=True,
    consistency=True,
    matchup=True,       # Use matchup data
    draft_round=0,      # NO draft bonuses (fair comparison)
    bye=True,
    injury=True         # Might want injury=False for rostered players
)
```

**Algorithm Outline**:
```python
1. Score all roster players (without draft bonus)
2. Score all available players (drafted=0, locked=0)
3. For each roster player (if not locked):
   a. For each available player:
      b. Calculate score_diff = available_score - roster_score
      c. Track best trade
4. If improvement > MIN_TRADE_IMPROVEMENT:
   a. Show trade suggestion
   b. Show runner-ups (top N alternatives)
5. Repeat until no improvements found
```

**Reference**: `old_structure/draft_helper/core/trade_analyzer.py`

---

### 4. Drop Player Mode

**File**: `league_helper/drop_player_mode/DropPlayerModeManager.py`

**Status**: ❌ **Stub - Not Implemented**

**Purpose**: Remove player from roster (set drafted=0, make available).

**Expected User Flow**:
1. Display current roster
2. User selects player to drop
3. Confirmation prompt
4. Update player to drafted=0
5. Update CSV
6. Show updated roster
7. Return to main menu

**Key Features to Implement**:
- **Roster Display**: Show all rostered players with scores
- **Confirmation**: Prevent accidental drops
- **Locked Player Warning**: Warn if trying to drop locked player (or prevent)
- **Immediate Update**: Update FantasyTeam roster in memory

**Scoring**: N/A

**CSV Update**: Set `drafted=0` for dropped player

**Reference**: `old_structure/draft_helper/core/player_search.py` (search_and_drop_player_interactive)

---

### 5. Lock/Unlock Player Mode

**File**: `league_helper/lock_player_mode/LockPlayerModeManager.py`

**Status**: ❌ **Stub - Not Implemented**

**Purpose**: Protect key players from being suggested in Waiver Optimizer trades.

**Expected User Flow**:
1. Display roster grouped by lock status:
   - Unlocked players
   - Locked players
2. User selects player to toggle
3. Toggle locked field (0 → 1 or 1 → 0)
4. Update CSV immediately
5. Show updated list
6. User can toggle more or return to main menu

**Key Features to Implement**:
- **Visual Grouping**: Separate locked/unlocked sections
- **Lock Indicator**: Show 🔒/🔓 or (LOCKED)/(UNLOCKED)
- **No Confirmation Needed**: Instant toggle (easy to undo)
- **Locked Count**: Display count in each section

**Scoring**: N/A

**CSV Update**: Toggle `locked` field (0 ↔ 1)

**Reference**: `old_structure/draft_helper/draft_helper.py` (run_lock_unlock_player_mode)

---

### 6. Starter Helper Mode

**File**: `league_helper/starter_helper_mode/StarterHelperModeManager.py`

**Status**: ❌ **Stub - Not Implemented**

**Purpose**: Generate optimal weekly starting lineup based on current week projections.

**Expected User Flow**:
1. Display week and scoring format
2. Load roster players (drafted=2)
3. Score each player for current week
4. Optimize lineup (QB, RB1, RB2, WR1, WR2, TE, FLEX, K, DST)
5. Display optimal starters with projected points
6. Display bench alternatives
7. Optionally save to file
8. Return to main menu

**Key Features to Implement**:
- **Week-Specific Scoring**: Use `week_N_points` from CSV
- **FLEX Optimization**: Choose best RB or WR for FLEX slot
- **Injury Filtering**: Zero out non-ACTIVE/QUESTIONABLE players
- **Matchup Emphasis**: Heavily weight matchup multipliers
- **Bench Recommendations**: Show top alternatives from bench

**Scoring Flags** (via `PlayerManager.score_player`):
```python
score_player(
    player,
    adp=False,          # Not relevant for weekly
    player_rating=False,
    team_quality=False,
    consistency=True,   # Consistency still matters
    matchup=True,       # MOST IMPORTANT for weekly
    draft_round=0,
    bye=False,          # Bye week already in week_N_points (0 or None)
    injury=False        # Handle as binary filter instead
)
```

**Special Logic**:
- Filter players where `injury_status not in ["ACTIVE", "QUESTIONABLE"]`
- Use `week_{CURRENT_NFL_WEEK}_points` instead of `fantasy_points`
- Apply matchup multipliers from `TeamDataManager`

**Reference**: `old_structure/starter_helper/lineup_optimizer.py`

---

### 7. Trade Simulator Mode

**File**: `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`

**Status**: ❌ **Stub - Not Implemented**

**Purpose**: Simulate hypothetical trades without modifying actual roster data.

**Expected User Flow**:
1. Create temporary roster copy
2. Show current roster
3. User selects player to drop from roster
4. User selects player to add (fuzzy search)
5. Show before/after comparison
6. User can simulate more trades or reset
7. Return to main menu (all changes discarded)

**Key Features to Implement**:
- **Sandbox Mode**: All changes in memory only
- **Before/After Comparison**: Show score differences
- **Multiple Trades**: Chain multiple trades in simulation
- **Reset Option**: Revert to original roster
- **No CSV Updates**: Simulation only

**Scoring Flags**: Same as Waiver Optimizer (no draft bonus)

**Implementation Notes**:
- Create deep copy of `PlayerManager.players` and `FantasyTeam.roster`
- All operations on copies
- Discard copies on exit

**Reference**: `old_structure/draft_helper/core/trade_simulator.py`

---

## Scoring System

### Overview

The scoring system evaluates players through a multi-step calculation that combines projections, market data, consistency, matchups, and penalties.

**Location**: `league_helper/util/PlayerManager.score_player()`

**Key Principle**: Each mode uses the same scoring function but enables/disables steps via flags.

---

### 9-Step Scoring Breakdown

#### Step 1: Normalization
**Formula**: `(player.fantasy_points / max_fantasy_points) * NORMALIZATION_MAX_SCALE`

**Purpose**: Scale all players to a 0-N range for consistent baseline comparison.

**Example**:
- Max player: 250 points → 123.54 (scale)
- Player with 125 points → 61.77

**Config**: `NORMALIZATION_MAX_SCALE` (e.g., 123.54)

**Flag**: Always enabled (no flag control)

---

#### Step 2: ADP Multiplier
**Formula**: `score * get_adp_multiplier(player.adp)`

**Purpose**: Apply market wisdom - earlier ADP = higher multiplier.

**Thresholds** (lower ADP = better):
- ADP ≤ 20: EXCELLENT → 1.18× boost
- ADP ≤ 50: GOOD → 1.08× boost
- ADP ≥ 100: POOR → 0.82× penalty
- ADP ≥ 150: VERY_POOR → 0.5× penalty

**Config**: `ADP_SCORING.THRESHOLDS` and `MULTIPLIERS`

**Flag**: `adp=True/False`

---

#### Step 3: Player Rating Multiplier
**Formula**: `score * get_player_rating_multiplier(player.player_rating)`

**Purpose**: Boost high-ranked players within their position.

**Thresholds** (higher rating = better):
- Rating ≥ 80: EXCELLENT → 1.21× boost
- Rating ≥ 60: GOOD → 1.15× boost
- Rating ≤ 40: POOR → 0.94× penalty
- Rating ≤ 20: VERY_POOR → 0.7× penalty

**Config**: `PLAYER_RATING_SCORING.THRESHOLDS` and `MULTIPLIERS`

**Flag**: `player_rating=True/False`

---

#### Step 4: Team Quality Multiplier
**Formula**: `score * get_team_quality_multiplier(player.team_offensive_rank)`

**Purpose**: Favor players on better offensive teams (or better defensive teams for DST).

**Thresholds** (lower rank = better):
- Rank ≤ 5: EXCELLENT → 1.32× boost
- Rank ≤ 10: GOOD → 1.14× boost
- Rank ≥ 18: POOR → 0.64× penalty
- Rank ≥ 25: VERY_POOR → 0.5× penalty

**Special Case**: DST positions use `team_defensive_rank` instead.

**Config**: `TEAM_QUALITY_SCORING.THRESHOLDS` and `MULTIPLIERS`

**Flag**: `team_quality=True/False`

---

#### Step 5: Consistency Multiplier
**Formula**: `score * get_consistency_multiplier(player.consistency)`

**Purpose**: Reward consistent performers, penalize volatile "boom/bust" players.

**Consistency Calculation**:
```python
# Coefficient of Variation (CV) = std_dev / mean
# Lower CV = more consistent

weekly_points = [week_1_points, week_2_points, ..., week_N_points]
mean = average(weekly_points)
std_dev = stdev(weekly_points)
cv = std_dev / mean

# Requires MIN_WEEKS (default: 3) of data
```

**Thresholds** (lower CV = better):
- CV ≤ 0.8: EXCELLENT → 1.50× boost
- CV ≤ 0.6: GOOD → 1.19× boost
- CV ≥ 0.4: POOR → 0.66× penalty
- CV ≥ 0.2: VERY_POOR → 0.5× penalty

**Default**: If < MIN_WEEKS of data, use CV = 0.5 (neutral)

**Config**: `CONSISTENCY_SCORING` (includes `MIN_WEEKS`, `THRESHOLDS`, `MULTIPLIERS`)

**Flag**: `consistency=True/False`

---

#### Step 6: Matchup Multiplier
**Formula**: `score * get_matchup_multiplier(player.matchup_score)`

**Purpose**: Boost players with favorable weekly matchups.

**Matchup Score Calculation**:
```python
# For offensive players:
matchup_score = player_team_offensive_rank - opponent_team_defensive_rank

# For DST:
matchup_score = player_team_defensive_rank - opponent_team_offensive_rank

# Positive = favorable, Negative = unfavorable
```

**Thresholds**:
- Score ≥ 15: EXCELLENT → 1.28× boost
- Score ≥ 6: GOOD → 1.14× boost
- Score ≤ -6: POOR → 0.92× penalty
- Score ≤ -15: VERY_POOR → 0.76× penalty

**Config**: `MATCHUP_SCORING.THRESHOLDS` and `MULTIPLIERS`

**Flag**: `matchup=True/False`

---

#### Step 7: Draft Order Bonus
**Formula**: `score + get_draft_order_bonus(player.position, draft_round)`

**Purpose**: Prioritize positions based on draft strategy for current round.

**How It Works**:
```python
# Check if player's position (with FLEX conversion) matches DRAFT_ORDER[round]
ideal_positions = DRAFT_ORDER[draft_round]

# Example Round 1: {"FLEX": "P", "QB": "S"}
# RB/WR players get PRIMARY bonus (71 points)
# QB players get SECONDARY bonus (52 points)
# Other positions get 0 bonus
```

**FLEX Conversion**:
- RB → FLEX
- WR → FLEX
- All other positions → unchanged

**Config**:
- `DRAFT_ORDER_BONUSES.PRIMARY` (e.g., 71)
- `DRAFT_ORDER_BONUSES.SECONDARY` (e.g., 52)
- `DRAFT_ORDER` (15-round strategy)

**Flag**: `draft_round=N` (if N > 0, bonus applied; if N = 0, skipped)

**Important**: This is the **only additive step** (not a multiplier).

---

#### Step 8: Bye Week Penalty
**Formula**: `score - (BASE_BYE_PENALTY * num_matching_byes)`

**Purpose**: Penalize players who create bye week stacking.

**How Matching Byes Are Calculated**:
```python
# Count roster players with:
# - Same bye week as candidate player
# - Same position (with FLEX conversion)
# - Excluding self if already rostered

num_matching_byes = count_roster_matching_byes(
    player.bye_week,
    player.position,
    is_rostered=player.drafted == 2
)
```

**Example**:
- Roster has 2 RBs on bye week 7
- Candidate is RB with bye week 7
- Penalty = 28.85 * 2 = 57.7 points

**Config**: `BASE_BYE_PENALTY` (e.g., 28.85)

**Flag**: `bye=True/False`

---

#### Step 9: Injury Penalty
**Formula**: `score - get_injury_penalty(player.injury_risk_level)`

**Purpose**: Penalize injured or high-risk players.

**Injury Risk Levels**:
```python
# Determined by player.injury_status
LOW:    ["ACTIVE"]
MEDIUM: ["QUESTIONABLE", "DOUBTFUL", "DAY_TO_DAY"]
HIGH:   ["OUT", "IR", "SUSPENDED", "PUP"]
```

**Penalties**:
- LOW: 0 points (no penalty)
- MEDIUM: 9.68 points
- HIGH: 78.22 points

**Config**: `INJURY_PENALTIES.LOW/MEDIUM/HIGH`

**Flag**: `injury=True/False`

---

### Mode-Specific Scoring Configurations

| Mode | ADP | Rating | Team | Consist | Matchup | Draft Bonus | Bye | Injury |
|------|-----|--------|------|---------|---------|-------------|-----|--------|
| **Add to Roster** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ (round-based) | ✅ | ✅ |
| **Waiver Optimizer** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ (no draft bonus) | ✅ | ✅* |
| **Trade Simulator** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅* |
| **Starter Helper** | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌** |

**Notes**:
- \* Waiver/Trade might disable injury penalty for rostered players (TBD during implementation)
- \*\* Starter Helper uses binary injury filter instead (only ACTIVE/QUESTIONABLE allowed)

---

### Scoring Code Example

```python
# Add to Roster Mode
score = player_manager.score_player(
    player,
    adp=True,
    player_rating=True,
    team_quality=True,
    consistency=True,
    matchup=False,
    draft_round=current_round,  # Adds draft bonus
    bye=True,
    injury=True
)

# Waiver Optimizer Mode
score = player_manager.score_player(
    player,
    adp=True,
    player_rating=True,
    team_quality=True,
    consistency=True,
    matchup=True,
    draft_round=0,  # NO draft bonus
    bye=True,
    injury=True
)

# Starter Helper Mode
# (After filtering for ACTIVE/QUESTIONABLE only)
score = player_manager.score_player(
    player,
    adp=False,
    player_rating=False,
    team_quality=False,
    consistency=True,
    matchup=True,      # Most important for weekly
    draft_round=0,
    bye=False,         # Already handled in week_N_points
    injury=False       # Already filtered
)
```

---

## Testing Strategy

### Current State
- ✅ **Unit tests created** for PlayerManager scoring system (60 tests, 100% passing)
- ✅ Test infrastructure set up with conftest.py and test runner
- ✅ Root-level `tests/` directory mirrors source structure
- ⏳ **Additional tests needed** for other managers and modes
- ✅ Old structure has comprehensive tests in `old_structure/draft_helper/tests/`
- ❌ Pre-commit validation script needs updating

### Testing Goals

**Test Coverage Target**: Every file and function should have associated tests.

**Test Structure**:
```
tests/                                    # ✅ Root-level test directory
├── README.md                            # ✅ Test documentation
├── conftest.py                          # ✅ Pytest configuration
├── run_all_tests.py                     # ✅ Test runner (100% pass requirement)
└── league_helper/
    └── util/
        ├── test_PlayerManager_scoring.py  # ✅ 60 tests (COMPLETE)
        ├── test_ConfigManager.py           # ⏳ TODO
        ├── test_TeamDataManager.py         # ⏳ TODO
        └── test_FantasyTeam.py             # ⏳ TODO

    # Mode tests (TODO)
    └── add_to_roster_mode/
        └── test_AddToRosterModeManager.py  # ⏳ TODO
```

### Running Tests

**Quick Start**:
```bash
# Run all tests with strict 100% pass requirement
python tests/run_all_tests.py

# Run with verbose output
python tests/run_all_tests.py --verbose

# Run specific test file
.venv/bin/python -m pytest tests/league_helper/util/test_PlayerManager_scoring.py -v
```

See `tests/README.md` for complete testing documentation.

---

### Unit Testing Approach

#### 1. ConfigManager Tests
**Focus**: JSON loading, validation, error handling

```python
# Test cases:
- Load valid config successfully
- Validate required fields exist
- Reject invalid JSON structure
- Handle missing parameters gracefully
- Multiplier calculation correctness
- Threshold boundary conditions
```

**Example**:
```python
def test_config_loads_successfully():
    config = ConfigManager(data_folder)
    assert config.current_nfl_week > 0
    assert config.normalization_max_scale > 0

def test_adp_multiplier_excellent_threshold():
    config = ConfigManager(data_folder)
    mult = config.get_adp_multiplier(adp_val=15)
    assert mult == 1.18  # EXCELLENT multiplier

def test_config_rejects_missing_required_field():
    # Create invalid config JSON missing CURRENT_NFL_WEEK
    with pytest.raises(ValueError, match="missing required parameters"):
        config = ConfigManager(invalid_data_folder)
```

---

#### 2. PlayerManager Tests
**Focus**: Scoring logic, consistency calculation, roster operations

```python
# Test cases:
- Load players from CSV correctly
- Calculate consistency (CV) accurately
- Enrich players with team data
- Score player with all flags enabled
- Score player with selective flags
- Verify normalization scaling
- Test draft eligibility logic
- Test draft player operation
```

**Example**:
```python
def test_consistency_calculation_with_sufficient_data():
    # Create player with 5 weeks of data
    player = FantasyPlayer(...)
    player.week_1_points = 10
    player.week_2_points = 12
    player.week_3_points = 11
    player.week_4_points = 13
    player.week_5_points = 14

    cv, weeks = player_manager._calculate_consistency(player)
    assert weeks == 5
    assert 0 < cv < 1  # Valid CV range

def test_score_player_with_draft_bonus():
    player = create_test_player(position="RB")
    score = player_manager.score_player(
        player,
        draft_round=1  # Round 1: FLEX gets PRIMARY bonus
    )
    # Should include 71-point bonus (RB → FLEX → PRIMARY)
    assert score > player.weighted_projection + 50

def test_score_player_without_draft_bonus():
    player = create_test_player(position="RB")
    score = player_manager.score_player(
        player,
        draft_round=0  # No draft bonus
    )
    # Should not include draft bonus
    assert score < player.weighted_projection + 50
```

---

#### 3. FantasyTeam Tests
**Focus**: Roster validation, position limits, FLEX logic

```python
# Test cases:
- Can draft player within position limits
- Cannot exceed position limits
- FLEX slot assignment logic
- RB/WR eligibility for FLEX
- Bye week conflict counting
- Slot assignment tracking
```

**Example**:
```python
def test_can_draft_within_position_limit():
    team = FantasyTeam(config, [])
    rb_player = create_test_player(position="RB")

    # Roster 3 RBs (limit is 4)
    for _ in range(3):
        team.draft_player(create_test_player(position="RB"))

    # Should be able to draft 4th RB
    assert team.can_draft(rb_player) == True

def test_cannot_exceed_position_limit():
    team = FantasyTeam(config, [])

    # Fill RB slots (4 max)
    for _ in range(4):
        team.draft_player(create_test_player(position="RB"))

    # Should NOT be able to draft 5th RB
    rb_player = create_test_player(position="RB")
    assert team.can_draft(rb_player) == False

def test_flex_slot_accepts_rb_and_wr():
    team = FantasyTeam(config, [])

    # Fill 4 RBs + 4 WRs
    for _ in range(4):
        team.draft_player(create_test_player(position="RB"))
        team.draft_player(create_test_player(position="WR"))

    # FLEX slot should accommodate RB
    rb_player = create_test_player(position="RB")
    assert team.can_draft(rb_player) == True

    # FLEX slot should accommodate WR
    wr_player = create_test_player(position="WR")
    assert team.can_draft(wr_player) == True
```

---

#### 4. Mode Manager Tests
**Focus**: User flow, integration with PlayerManager, CSV updates

```python
# Test cases (using mocks):
- Display roster correctly
- Get recommendations with correct scoring flags
- Draft player updates roster
- CSV file updated after operations
- Return to main menu gracefully
```

**Example**:
```python
def test_add_to_roster_shows_recommendations(mocker):
    mode = AddToRosterModeManager(config, player_manager, team_data_manager)

    # Mock player_manager.can_draft to return True
    mocker.patch.object(player_manager, 'can_draft', return_value=True)

    recommendations = mode.get_recommendations()

    # Should return 10 recommendations (RECOMMENDATION_COUNT)
    assert len(recommendations) == 10

    # Should be sorted by score descending
    assert recommendations[0].score >= recommendations[1].score

def test_draft_player_updates_csv(mocker):
    mode = AddToRosterModeManager(config, player_manager, team_data_manager)

    player = create_test_player()

    # Mock CSV update
    mock_update = mocker.patch.object(player_manager, 'update_players_file')

    # Simulate drafting player
    player_manager.draft_player(player)
    player_manager.update_players_file()

    # Verify CSV update called
    mock_update.assert_called_once()
```

---

### Integration Testing

#### Interactive Tests (Manual)

Similar to old structure's `draft_helper_validation_checklist.md`, create:

**File**: `tests/league_helper_validation_checklist.md`

**Test Flow**:
```bash
# Start League Helper
python run_league_helper.py

# Test Add to Roster Mode
# 1. Select "1. Add to Roster"
# 2. Verify roster display shows correct slots
# 3. Verify recommendations shown (top 10)
# 4. Draft a player
# 5. Verify roster updated
# 6. Verify CSV updated (check data/players.csv)
# 7. Return to main menu

# Test data reload
# 8. Externally modify data/players.csv (change a player's points)
# 9. Go back to "Add to Roster"
# 10. Verify updated data reflected in recommendations

# Continue for each mode as implemented...
```

---

### Pre-Commit Validation Script

**Current**: `run_pre_commit_validation.py` tests old structure only

**Needed**: New version or update existing to test both structures during transition

**Requirements**:
1. **Unit Tests**: Run all `league_helper/tests/` (when created)
2. **Startup Tests**: Verify `run_league_helper.py` starts without errors
3. **Integration Tests**: Automated interactive test sequence
4. **Exit Codes**: Return 0 for success, 1 for failures

**Example Structure**:
```python
def validate_league_helper():
    """Validate new League Helper structure"""
    print("="*60)
    print("VALIDATING LEAGUE HELPER")
    print("="*60)

    # 1. Unit tests
    result = run_unit_tests("league_helper/tests/")
    if result != 0:
        return result

    # 2. Startup test
    result = test_startup("run_league_helper.py", timeout=10)
    if result != 0:
        return result

    # 3. Interactive tests (when modes implemented)
    result = run_interactive_tests()
    if result != 0:
        return result

    print("✅ All League Helper tests passed")
    return 0
```

---

## Development Guidelines

### Adding a New Mode

Follow this checklist when implementing stub modes:

#### 1. Study the Reference Implementation
```bash
# Find the old mode implementation
cd old_structure/draft_helper/core/

# Key files:
- roster_manager.py      # For Add to Roster
- player_search.py       # For Mark Drafted, Drop Player
- trade_analyzer.py      # For Waiver Optimizer
- trade_simulator.py     # For Trade Simulator
# (Starter helper in old_structure/starter_helper/)
```

#### 2. Understand Scoring Requirements
Determine which scoring flags your mode needs:
```python
# Example: Waiver Optimizer
score = player_manager.score_player(
    player,
    adp=True,           # ✅ Use ADP
    player_rating=True, # ✅ Use player rating
    team_quality=True,  # ✅ Use team quality
    consistency=True,   # ✅ Use consistency
    matchup=True,       # ✅ Use matchup (weekly context)
    draft_round=0,      # ❌ NO draft bonus (fair comparison)
    bye=True,           # ✅ Consider bye weeks
    injury=True         # ✅ Consider injuries
)
```

#### 3. Implement the Mode Manager

**Template**:
```python
# league_helper/xxx_mode/XxxModeManager.py

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from util.ConfigManager import ConfigManager
from util.PlayerManager import PlayerManager
from util.TeamDataManager import TeamDataManager

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger

class XxxModeManager:
    def __init__(self, config: ConfigManager,
                 player_manager: PlayerManager = None,
                 team_data_manager: TeamDataManager = None):
        self.config = config
        self.logger = get_logger()
        self.set_managers(player_manager, team_data_manager)

    def set_managers(self, player_manager, team_data_manager):
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager

    def start_interactive_mode(self, player_manager, team_data_manager):
        """Main entry point called by LeagueHelperManager"""
        self.set_managers(player_manager, team_data_manager)

        print("\n" + "="*50)
        print("XXX MODE NAME")
        print("="*50)

        # Your mode logic here

        print("Returning to Main Menu...")
```

#### 4. Add to LeagueHelperManager

```python
# league_helper/LeagueHelperManager.py

from xxx_mode.XxxModeManager import XxxModeManager

class LeagueHelperManager:
    def __init__(self, data_folder: Path):
        # ... existing init ...
        self.xxx_mode_manager = XxxModeManager(self.config)

    def start_interactive_mode(self):
        # ... existing menu loop ...
        elif choice == N:  # Replace N with menu number
            self.run_xxx_mode()

    def run_xxx_mode(self):
        self.xxx_mode_manager.start_interactive_mode(
            self.player_manager,
            self.team_data_manager
        )
```

#### 5. Write Unit Tests

Create `league_helper/tests/xxx_mode/test_XxxModeManager.py`:
```python
import pytest
from league_helper.xxx_mode.XxxModeManager import XxxModeManager

def test_xxx_mode_initializes():
    mode = XxxModeManager(mock_config)
    assert mode.config is not None

# Add more tests...
```

#### 6. Update Documentation

Add your mode to this document:
- Mode description
- User flow
- Scoring flags used
- Key features
- CSV updates (if any)

#### 7. Test Interactive Flow

Add to validation checklist:
```markdown
## Test Xxx Mode

1. Select "N. Xxx Mode" from main menu
2. Verify [expected behavior]
3. Perform [mode operation]
4. Verify [expected result]
5. Return to main menu
```

---

### Modifying Scoring Logic

**⚠️ CAUTION**: Scoring changes affect ALL modes.

#### Before Changing:
1. **Understand Impact**: Which modes use which flags?
2. **Check Tests**: Run all scoring-related tests
3. **Document**: Update this documentation
4. **Update Config**: Modify `league_config.json` if needed

#### Common Changes:

##### Adding a New Scoring Step
```python
# 1. Add new parameter to league_config.json
"NEW_SCORING": {
    "THRESHOLDS": { ... },
    "MULTIPLIERS": { ... }
}

# 2. Update ConfigManager to load it
def _extract_parameters(self):
    # ... existing ...
    self.new_scoring = self.parameters[self.keys.NEW_SCORING]

def get_new_multiplier(self, value):
    return self._get_multiplier(self.new_scoring, value)

# 3. Update PlayerManager.score_player()
def score_player(self, p, ..., new_scoring=True, ...):
    # ... existing steps ...

    # STEP X: Apply New Scoring
    if new_scoring:
        player_score = self._apply_new_scoring_multiplier(p, player_score)

    # ... continue ...

def _apply_new_scoring_multiplier(self, p, player_score):
    multiplier = self.config.get_new_multiplier(p.new_attribute)
    return player_score * multiplier

# 4. Update all mode managers to pass new_scoring flag
```

##### Modifying Existing Thresholds
```json
// In data/league_config.json

"ADP_SCORING": {
    "THRESHOLDS": {
        "EXCELLENT": 15,  // Changed from 20
        // ... rest unchanged
    }
}
```

**No code changes needed** - ConfigManager automatically picks up new values!

---

### Adding New Data Sources

#### Adding a New CSV File

**Example**: Add `matchups.csv` for weekly opponent tracking

```python
# 1. Create CSV structure
# data/matchups.csv
# week,team,opponent
# 6,KC,LV
# 6,BUF,NYJ

# 2. Create data manager (if complex logic needed)
# league_helper/util/MatchupManager.py

class MatchupManager:
    def __init__(self, data_folder: Path):
        self.matchups = self._load_matchups(data_folder / 'matchups.csv')

    def _load_matchups(self, file_path):
        # Load CSV logic
        pass

    def get_opponent(self, week: int, team: str) -> str:
        # Return opponent for team in given week
        pass

# 3. Add to LeagueHelperManager
self.matchup_manager = MatchupManager(data_folder)

# 4. Pass to modes that need it
self.starter_helper_manager = StarterHelperModeManager(
    self.config,
    matchup_manager=self.matchup_manager
)
```

#### Adding a New Player Attribute

**Example**: Add "yards_per_game" to FantasyPlayer

```python
# 1. Update utils/FantasyPlayer.py
class FantasyPlayer:
    def __init__(self, ...):
        # ... existing ...
        self.yards_per_game: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
        # ... existing ...
        player.yards_per_game = float(data.get('yards_per_game', 0))

# 2. Update player-fetcher to populate field
# (Fetch from ESPN API and add to CSV export)

# 3. Update PlayerManager CSV field list
fieldnames = [
    # ... existing fields ...
    'yards_per_game',
]

# 4. Use in scoring if needed
def score_player(self, p, ...):
    # ... can now use p.yards_per_game ...
```

---

### Debugging Tips

#### Config Issues
```python
# Enable debug logging
# In league_helper/constants.py
LOGGING_LEVEL = 'DEBUG'  # Instead of WARNING

# Check config loading
config = ConfigManager(data_folder)
print(config.parameters)  # See all loaded params
print(config.get_adp_multiplier(25))  # Test specific lookups
```

#### Scoring Issues
```python
# Enable detailed scoring logs
player_manager.score_player(player, draft_round=1)

# Check logs for step-by-step breakdown:
# Step 1 - Normalized score for Player: 75.23
# Step 2 - ADP Enhanced score for Player: 81.25
# Step 3 - Player Rating Enhanced score for Player: 93.03
# ... etc
```

#### CSV Issues
```python
# Check CSV structure
import csv
with open('data/players.csv', 'r') as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)  # Verify column names
    print(next(reader))  # See first row

# Check for missing data
player = player_manager.players[0]
print(f"ADP: {player.adp}")
print(f"Rating: {player.player_rating}")
print(f"Consistency: {player.consistency}")
```

#### Mode Flow Issues
```python
# Add print statements in mode manager
def start_interactive_mode(self, player_manager, team_data_manager):
    print(f"DEBUG: player_manager has {len(player_manager.players)} players")
    print(f"DEBUG: roster has {len(player_manager.team.roster)} players")

    recommendations = self.get_recommendations()
    print(f"DEBUG: got {len(recommendations)} recommendations")
    for i, p in enumerate(recommendations[:3]):
        print(f"  {i+1}. {p.name}: {p.score:.1f}")
```

---

## Migration Reference (Old → New)

### File Mappings

| Old Structure | New Structure | Status |
|---------------|---------------|--------|
| `old_structure/draft_helper/draft_helper.py` | `league_helper/LeagueHelperManager.py` | 🏗️ Partial |
| `old_structure/draft_helper/FantasyTeam.py` | `league_helper/util/FantasyTeam.py` | ✅ Migrated |
| `old_structure/draft_helper/draft_helper_constants.py` | `league_helper/constants.py` | ✅ Migrated |
| `old_structure/draft_helper/core/roster_manager.py` | `league_helper/add_to_roster_mode/AddToRosterModeManager.py` | 🏗️ Partial |
| `old_structure/draft_helper/core/player_search.py` | `league_helper/mark_drafted_player_mode/` | ❌ Not started |
| `old_structure/draft_helper/core/trade_analyzer.py` | `league_helper/waiver_optimizer_mode/` | ❌ Not started |
| `old_structure/draft_helper/core/trade_simulator.py` | `league_helper/trade_simulator_mode/` | ❌ Not started |
| `old_structure/draft_helper/core/scoring_engine.py` | `league_helper/util/PlayerManager.score_player()` | ✅ Migrated |
| `old_structure/shared_files/FantasyPlayer.py` | `utils/FantasyPlayer.py` | ✅ Migrated |
| `old_structure/shared_files/parameters.json` | `data/league_config.json` | ✅ Migrated (redesigned) |
| `old_structure/shared_files/configs/*.py` | `data/league_config.json` | ✅ Migrated (consolidated) |

### Concept Mappings

| Old Concept | New Concept | Notes |
|-------------|-------------|-------|
| DraftHelper | LeagueHelper | Renamed to reflect broader purpose |
| Trade Analysis Mode | Waiver Optimizer Mode | Renamed for clarity |
| `TRADE_HELPER_MODE` flag | N/A | No mode toggle needed (separate modes) |
| Python config files | JSON config | Easier for simulation swapping |
| `shared_files/` | `utils/` + `league_helper/util/` | Two-tier utility structure |
| Mode methods in DraftHelper | Separate ModeManager classes | Better modularity |
| Monolithic scoring_engine | PlayerManager.score_player() | Simplified, flag-based |

### Breaking Changes

#### Configuration
```python
# OLD (Python config)
from draft_helper_config import NORMALIZATION_MAX_SCALE

# NEW (JSON via ConfigManager)
config = ConfigManager(data_folder)
scale = config.normalization_max_scale
```

#### Scoring
```python
# OLD (Separate engine)
scoring_engine = ScoringEngine(team, players, logger, param_manager)
score = scoring_engine.score_player(player, enhanced_scorer=...)

# NEW (PlayerManager method)
player_manager = PlayerManager(data_folder, config, team_data_manager)
score = player_manager.score_player(player, draft_round=1)
```

#### Mode Access
```python
# OLD (Methods on DraftHelper)
draft_helper.run_add_to_roster_mode()
draft_helper.run_trade_analysis_mode()

# NEW (Separate managers)
league_helper.run_add_to_roster_mode()  # Delegates to AddToRosterModeManager
league_helper.run_waiver_optimizer_mode()  # Delegates to WaiverOptimizerModeManager
```

---

## Common Tasks & Examples

### Task: Update League Configuration for New Week

```bash
# 1. Open config file
nano data/league_config.json

# 2. Update CURRENT_NFL_WEEK
"CURRENT_NFL_WEEK": 7,  # Changed from 6

# 3. (Optional) Update team rankings
nano data/teams.csv
# Update offensive/defensive ranks based on current standings

# 4. Run player fetcher to get new projections
python run_player_fetcher.py

# 5. Run League Helper
python run_league_helper.py
# Use Starter Helper mode for weekly lineup
```

### Task: Add a New Player to Roster

```bash
# Run League Helper
python run_league_helper.py

# From menu:
1. Add to Roster
# View recommendations (automatically scored for current draft round)
# Enter number of player to draft
# Verify roster updated
# Return to main menu

# Verify CSV updated
cat data/players.csv | grep "drafted,2"
```

### Task: Simulate Parameter Changes

```bash
# 1. Create new config
cp data/league_config.json data/league_config_test.json

# 2. Edit test config
nano data/league_config_test.json
# Change "NORMALIZATION_MAX_SCALE": 200  (was 123.54)
# Change "config_name": "Test High Normalization"

# 3. Update ConfigManager to use test config (temporarily)
# Or pass config path as argument (if implemented)

# 4. Run League Helper with test config
python run_league_helper.py

# 5. Compare scoring differences
```

### Task: Debug Scoring Issues

```python
# Create a test script: test_scoring.py

from pathlib import Path
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager

# Initialize managers
data_folder = Path("./data")
config = ConfigManager(data_folder)
team_data = TeamDataManager(data_folder)
player_manager = PlayerManager(data_folder, config, team_data)

# Get a specific player
player = next(p for p in player_manager.players if p.name == "Patrick Mahomes")

# Score with full details (enable DEBUG logging first)
score = player_manager.score_player(
    player,
    adp=True,
    player_rating=True,
    team_quality=True,
    consistency=True,
    matchup=False,
    draft_round=1,
    bye=True,
    injury=True
)

print(f"Final score for {player.name}: {score:.2f}")
print(f"Breakdown:")
print(f"  Normalized: {player.weighted_projection:.2f}")
print(f"  ADP: {player.adp}")
print(f"  Rating: {player.player_rating}")
print(f"  Consistency: {player.consistency:.3f}")
print(f"  Injury: {player.injury_status}")
```

```bash
# Run test
python test_scoring.py

# Check detailed logs
tail -f data/log.txt  # If logging to file
```

### Task: Export Roster for External Analysis

```python
# Create export script: export_roster.py

import csv
from pathlib import Path
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager

# Initialize
data_folder = Path("./data")
config = ConfigManager(data_folder)
team_data = TeamDataManager(data_folder)
player_manager = PlayerManager(data_folder, config, team_data)

# Get roster players
roster = [p for p in player_manager.players if p.drafted == 2]

# Export to CSV
with open('my_roster_export.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Position', 'Team', 'Points', 'Bye Week', 'Injury'])

    for p in roster:
        writer.writerow([
            p.name,
            p.position,
            p.team,
            p.fantasy_points,
            p.bye_week,
            p.injury_status
        ])

print(f"Exported {len(roster)} players to my_roster_export.csv")
```

---

## Quick Reference

### Essential File Locations

```
📍 Main Entry: run_league_helper.py
📍 Config: data/league_config.json
📍 Player Data: data/players.csv
📍 Team Data: data/teams.csv
📍 Bye Weeks: data/bye_weeks.csv
📍 Core Manager: league_helper/LeagueHelperManager.py
📍 Scoring: league_helper/util/PlayerManager.py
📍 Logs: data/log.txt (if logging to file)
```

### Key Commands

```bash
# Run League Helper
python run_league_helper.py

# Update player data
python run_player_fetcher.py

# Get NFL scores
python run_scores_fetcher.py

# Run tests (when implemented)
pytest league_helper/tests/

# Run pre-commit validation (when updated)
python run_pre_commit_validation.py
```

### Key Constants

```python
# league_helper/constants.py
MAX_PLAYERS = 15  # Total roster size
RECOMMENDATION_COUNT = 10  # Top players to show

MAX_POSITIONS = {
    "QB": 2, "RB": 4, "WR": 4, "FLEX": 1,
    "TE": 2, "K": 1, "DST": 1
}

STARTING_LINEUP_REQUIREMENTS = {
    "QB": 1, "RB": 2, "WR": 2, "TE": 1,
    "FLEX": 1, "K": 1, "DST": 1
}

FLEX_ELIGIBLE_POSITIONS = ["RB", "WR"]
```

### Scoring Quick Reference

**Enabled in Add to Roster**:
- ✅ Normalization
- ✅ ADP
- ✅ Player Rating
- ✅ Team Quality
- ✅ Consistency
- ❌ Matchup
- ✅ Draft Bonus (round-based)
- ✅ Bye Penalty
- ✅ Injury Penalty

**Enabled in Waiver Optimizer**:
- ✅ Normalization
- ✅ ADP
- ✅ Player Rating
- ✅ Team Quality
- ✅ Consistency
- ✅ Matchup
- ❌ Draft Bonus (NO - fair comparison)
- ✅ Bye Penalty
- ✅ Injury Penalty

---

## Additional Resources

### Old Structure Documentation
- **Main Doc**: `old_structure/CLAUDE.md`
- **README**: `old_structure/README.md`
- **Rules**: `old_structure/potential_updates/rules.txt`

### Code References
- **Old Draft Helper**: `old_structure/draft_helper/draft_helper.py` (1173 lines)
- **Old Scoring Engine**: `old_structure/draft_helper/core/scoring_engine.py`
- **Old Roster Manager**: `old_structure/draft_helper/core/roster_manager.py`

### Testing References
- **Old Unit Tests**: `old_structure/draft_helper/tests/`
- **Old Validation**: `old_structure/tests/pre_commit_validation_checklist.md`

---

## Document Maintenance

**Last Updated**: 2025-10-15

**Update Triggers**:
- New mode implemented
- Scoring system changes
- Configuration structure changes
- New data sources added
- Testing approach modified

**Maintainers**: Keep this document in sync with code changes!

---

## Summary for Claude Agents

**TL;DR**:
1. **Project**: Fantasy Football League Helper - 10-team "Start 7" league manager
2. **Current State**: Mid-refactor from monolithic Draft Helper to modular League Helper
3. **What Works**: Player/Scores fetchers, core managers, Add to Roster mode (needs testing)
4. **What's Stub**: 6 other modes (Mark Drafted, Waiver Optimizer, Drop, Lock, Starter, Trade Sim)
5. **Key Files**:
   - Entry: `run_league_helper.py`
   - Config: `data/league_config.json`
   - Main: `league_helper/LeagueHelperManager.py`
   - Scoring: `league_helper/util/PlayerManager.score_player()`
6. **Architecture**: Manager hierarchy with JSON config, modular mode system
7. **Next Steps**: Complete stub modes following AddToRosterModeManager pattern
8. **Reference**: Use `old_structure/` for understanding unimplemented logic

**When Making Changes**:
- Read `CLAUDE.md` for coding standards and workflow rules
- Update config in `data/league_config.json` (single source of truth)
- Scoring changes go in `PlayerManager.score_player()`
- New modes get their own ModeManager class
- Follow error handling and logging patterns from `utils/`
- Test everything (unit tests via `python tests/run_all_tests.py`)
- Update this documentation and CLAUDE.md!

**Coding Standards**:
- Type hints required for all public methods
- Use `Path` objects for file operations
- Centralized error handling via `utils/error_handler.py`
- Logging via `utils/LoggingManager.py`
- CSV operations via `utils/csv_utils.py`
- Google-style docstrings
- See `CLAUDE.md` for complete standards
