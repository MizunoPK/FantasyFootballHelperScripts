# Research: Feature 10 - Refactor Player Fetcher Architecture

**Feature:** feature_10_refactor_player_fetcher
**Created:** 2026-01-31
**Research Phase:** S2.P1

---

## Research Summary

**Goal:** Understand Feature 01's current config override pattern to plan refactoring to constructor parameter pattern

**Files Researched:**
1. `run_player_fetcher.py` (445 lines) - Runner script with argparse
2. `player-data-fetcher/config.py` (90 lines) - Module-level constants
3. `player-data-fetcher/player_data_fetcher_main.py` (lines 1-130, 537-615) - Main module with Settings and NFLProjectionsCollector

---

## Current Architecture (Config Override Pattern)

### Flow Diagram

```
run_player_fetcher.py
│
├─→ Parse CLI arguments (argparse)
│   ├─ --week, --season, --debug, --e2e-test, etc. (23 args total)
│   └─ Returns: args object
│
├─→ Import config module
│   ├─ sys.path.insert(0, str(fetcher_dir))
│   ├─ config = importlib.import_module('config')
│   └─ config now accessible as module object
│
├─→ Override config constants at runtime
│   ├─ if args.debug: config.LOGGING_LEVEL = 'DEBUG'
│   ├─ if args.debug: config.ESPN_PLAYER_LIMIT = 100
│   ├─ if args.week is not None: config.CURRENT_NFL_WEEK = args.week
│   └─ ... (22 constants potentially overridden)
│
├─→ Import player_data_fetcher_main module
│   ├─ player_data_fetcher_main = importlib.import_module('player_data_fetcher_main')
│   └─ This module imports from config (sees already-modified constants)
│
└─→ Run main
    └─ asyncio.run(player_data_fetcher_main.main())
        └─ main() takes NO parameters
        └─ main() reads from already-modified config constants
```

---

## File Details

### File 1: run_player_fetcher.py

**Location:** `run_player_fetcher.py`
**Lines:** 445
**Purpose:** CLI wrapper with argparse

**Key Code Sections:**

**Lines 62-314: Argument Parser Setup**
```python
parser = argparse.ArgumentParser(
    description='Player Data Fetcher - Fetch NFL player projections from ESPN API',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

# 23 arguments total:
parser.add_argument('--week', type=int, default=None, ...)
parser.add_argument('--season', type=int, default=None, ...)
# ... 21 more arguments
```

**Lines 319-332: Config Import**
```python
# Get fetcher directory
script_dir = Path(__file__).parent
fetcher_dir = script_dir / "player-data-fetcher"

# Add fetcher directory to Python path
sys.path.insert(0, str(fetcher_dir))

# Import config module (must import before applying overrides)
try:
    config = importlib.import_module('config')
except ImportError as e:
    print(f"[ERROR] Failed to import config module: {e}")
    sys.exit(1)
```

**Lines 334-431: Config Override Logic**
```python
# Apply debug mode config overrides FIRST
if args.debug:
    config.LOGGING_LEVEL = 'DEBUG'
    config.ESPN_PLAYER_LIMIT = 100
    config.PROGRESS_UPDATE_FREQUENCY = 5
    config.ENABLE_GAME_DATA_FETCH = False
    config.ENABLE_HISTORICAL_DATA_SAVE = False
    config.CREATE_CSV = True
    config.CREATE_JSON = False
    config.CREATE_EXCEL = False
    config.CREATE_CONDENSED_EXCEL = False
    config.CREATE_POSITION_JSON = True

# Apply E2E test mode config overrides SECOND
if args.e2e_test:
    config.ESPN_PLAYER_LIMIT = 100
    config.ENABLE_GAME_DATA_FETCH = False
    config.ENABLE_HISTORICAL_DATA_SAVE = False
    config.CREATE_EXCEL = False
    config.CREATE_JSON = False

# Apply individual CLI argument overrides (22 constants)
if args.week is not None:
    config.CURRENT_NFL_WEEK = args.week
if args.season is not None:
    config.NFL_SEASON = args.season
# ... 20 more overrides
```

**Lines 433-442: Import and Run Main**
```python
# Import and run player_data_fetcher_main (after all config overrides applied)
try:
    player_data_fetcher_main = importlib.import_module('player_data_fetcher_main')
except ImportError as e:
    print(f"[ERROR] Failed to import player_data_fetcher_main: {e}")
    sys.exit(1)

# Run async main
asyncio.run(player_data_fetcher_main.main())
```

---

### File 2: player-data-fetcher/config.py

**Location:** `player-data-fetcher/config.py`
**Lines:** 90
**Purpose:** Module-level configuration constants

**All Constants (23 used by CLI):**

```python
# Week/Season (2)
CURRENT_NFL_WEEK = 17
NFL_SEASON = 2025

# Data Preservation (4)
PRESERVE_LOCKED_VALUES = False
LOAD_DRAFTED_DATA_FROM_FILE = True
DRAFTED_DATA = "../data/drafted_data.csv"
MY_TEAM_NAME = "Sea Sharp"

# Output Settings (5)
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = False
CREATE_CONDENSED_EXCEL = False
CREATE_POSITION_JSON = True

# Position JSON Output (1)
POSITION_JSON_OUTPUT = "../data/player_data"

# File Paths (2)
TEAM_DATA_FOLDER = '../data/team_data'
GAME_DATA_CSV = '../data/game_data.csv'

# Feature Toggles (2)
ENABLE_HISTORICAL_DATA_SAVE = False
ENABLE_GAME_DATA_FETCH = True

# Logging (4)
LOGGING_LEVEL = 'INFO'
LOGGING_TO_FILE = False
LOGGING_FILE = './data/log.txt'
PROGRESS_UPDATE_FREQUENCY = 10

# API Settings (1)
ESPN_PLAYER_LIMIT = 2000
```

**Total:** 23 constants overridable via CLI (+ additional constants not exposed to CLI)

---

### File 3: player-data-fetcher/player_data_fetcher_main.py

**Location:** `player-data-fetcher/player_data_fetcher_main.py`
**Purpose:** Main module with Settings class and collector logic

**Lines 33-39: Config Imports**
```python
from config import (
    NFL_SEASON, CURRENT_NFL_WEEK,
    OUTPUT_DIRECTORY, CREATE_CSV, CREATE_JSON, CREATE_EXCEL,
    REQUEST_TIMEOUT, RATE_LIMIT_DELAY, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE,
    LOG_NAME, LOGGING_FORMAT,
    ENABLE_HISTORICAL_DATA_SAVE, ENABLE_GAME_DATA_FETCH
)
```

**Lines 42-98: Settings Class**
```python
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.

    Supports configuration via environment variables with NFL_PROJ_ prefix.
    Falls back to default values if environment variables are not set.
    """
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        env_prefix='NFL_PROJ_',
        extra='ignore'
    )

    # Data Parameters
    scoring_format: ScoringFormat = ScoringFormat.PPR
    season: int = NFL_SEASON  # ← Reads from config constant
    current_nfl_week: int = CURRENT_NFL_WEEK  # ← Reads from config constant

    # Output Configuration
    output_directory: str = OUTPUT_DIRECTORY  # ← Reads from config constant
    create_csv: bool = CREATE_CSV  # ← Reads from config constant
    create_json: bool = CREATE_JSON  # ← Reads from config constant
    create_excel: bool = CREATE_EXCEL  # ← Reads from config constant

    # API Settings
    request_timeout: int = REQUEST_TIMEOUT
    rate_limit_delay: float = RATE_LIMIT_DELAY
```

**Lines 100-130: NFLProjectionsCollector Constructor**
```python
class NFLProjectionsCollector:
    """Main collector class that coordinates data collection and export"""

    def __init__(self, settings: Settings):
        """
        Initialize the NFL projections collector.

        Args:
            settings: Application settings including API configuration and output options
        """
        self.settings = settings
        self.logger = get_logger()
        self.script_dir = Path(__file__).parent
        # ... rest of initialization
```

**Lines 537-550: main() Function**
```python
async def main():
    """Main application entry point"""

    logger = setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
    # ↑ Reads from module-level constants (already overridden by run_player_fetcher.py)

    try:
        logger.info("Starting NFL projections collection with ESPN API")

        # Load and validate settings
        settings = Settings()  # ← NO parameters - reads from config constants
        settings.validate_settings()

        # Create collector and gather data
        collector = NFLProjectionsCollector(settings)  # ← Dependency injection (good!)
        projection_data = await collector.collect_all_projections()
        # ...
```

**Lines 565, 576: Direct Config Constant Usage**
```python
# Line 565
elif not ENABLE_GAME_DATA_FETCH:  # ← Reads module-level constant directly
    logger.debug("Game data fetching disabled via config")

# Line 576
elif not ENABLE_HISTORICAL_DATA_SAVE:  # ← Reads module-level constant directly
    logger.debug("Historical data auto-save disabled via config")
```

---

## Key Observations

### What Works Well (Keep)

1. **NFLProjectionsCollector uses dependency injection** (line 107)
   - Constructor takes `Settings` object as parameter
   - No direct config constant usage inside collector
   - ✅ This pattern is good - keep it

2. **Settings class is pydantic BaseSettings** (line 42)
   - Supports environment variable overrides
   - Has validation capabilities
   - ✅ Can be extended to accept constructor parameters

3. **Argument parsing is comprehensive** (lines 62-314)
   - 23 arguments covering all configurable constants
   - Good help text, validation, default=None pattern
   - ✅ Keep argparse setup, change where args flow

### What Needs Refactoring (Fix)

1. **main() takes NO parameters** (line 537)
   - Currently: `async def main():`
   - Problem: Cannot pass arguments directly
   - ❌ Needs: `async def main(args) → settings`

2. **Settings() constructor takes NO parameters** (line 546)
   - Currently: `settings = Settings()`
   - Reads from module-level constants as defaults
   - ❌ Needs: `settings = create_settings_from_args(args)`

3. **Direct module constant usage in main()** (lines 540, 565, 576)
   - `setup_logger(LOG_NAME, LOGGING_LEVEL, ...)` - uses globals
   - `if not ENABLE_GAME_DATA_FETCH:` - uses globals
   - ❌ Needs: Pass via Settings or parameters

4. **Runtime config override** (run_player_fetcher.py lines 334-431)
   - Modifies imported module's constants at runtime
   - Non-standard Python pattern
   - ❌ Needs: Direct parameter passing

---

## Refactoring Plan (High-Level)

### Target Architecture (Constructor Parameter Pattern)

```
run_player_fetcher.py
│
├─→ Parse CLI arguments (argparse)
│   └─ Returns: args object
│
├─→ Create settings dictionary from args
│   ├─ settings_dict = {
│   │     'season': args.season if args.season is not None else 2025,
│   │     'current_nfl_week': args.week if args.week is not None else 17,
│   │     'logging_level': 'DEBUG' if args.debug else (args.log_level or 'INFO'),
│   │     ...
│   │ }
│   └─ All 23 constants mapped to dictionary
│
├─→ Import player_data_fetcher_main module
│   └─ No config override needed
│
└─→ Run main with settings
    └─ asyncio.run(player_data_fetcher_main.main(settings_dict))
        └─ main(settings_dict) takes parameters
        └─ main() creates Settings from settings_dict
        └─ No config constant usage
```

### Files to Modify

**1. run_player_fetcher.py (MAJOR changes)**
- Keep: Argparse setup (lines 62-317)
- Remove: Config import and override (lines 319-431)
- Add: Create settings dictionary from args
- Change: Pass settings_dict to main()

**2. player-data-fetcher/player_data_fetcher_main.py (MAJOR changes)**
- Change: `main()` signature to accept parameters
- Change: Create Settings from parameters (not config constants)
- Remove: Direct config constant usage in main()
- Keep: NFLProjectionsCollector constructor (already uses dependency injection)

**3. player-data-fetcher/config.py (MINOR changes or NO changes)**
- Option A: Keep as fallback defaults (not imported by runner)
- Option B: Remove entirely (all defaults in argparse)
- Decision needed: What to do with constants not exposed to CLI?

---

## Evidence Collected

**File paths cited:** 3 files
- `run_player_fetcher.py` (445 lines)
- `player-data-fetcher/config.py` (90 lines)
- `player-data-fetcher/player_data_fetcher_main.py` (615+ lines)

**Line numbers cited:** 15+ specific line ranges
- run_player_fetcher.py: 62-314, 319-332, 334-431, 433-442
- config.py: 13-90 (all constants listed)
- player_data_fetcher_main.py: 33-39, 42-98, 100-130, 537-550, 565, 576

**Method signatures copied:**
- `async def main():` (player_data_fetcher_main.py:537)
- `def __init__(self, settings: Settings):` (NFLProjectionsCollector line 107)
- `class Settings(BaseSettings):` (line 42)

**Code snippets preserved:** 8 code blocks showing current implementation

---

## Open Questions (for checklist.md)

**Question 1: What to do with config.py file after refactoring?**
- Option A: Keep as fallback defaults (not imported by runner, used by tests?)
- Option B: Remove entirely (all defaults in argparse)
- Option C: Keep for constants not exposed to CLI (LOG_NAME, LOGGING_FORMAT, etc.)

**Question 2: Should Settings class accept constructor parameters or use factory function?**
- Option A: Modify Settings.__init__ to accept kwargs
- Option B: Create factory function `create_settings_from_dict(settings_dict)`
- Option C: Use pydantic's model_validate() method

**Question 3: How to handle constants not exposed to CLI?**
- Constants like LOG_NAME, LOGGING_FORMAT, DEFAULT_FILE_CAPS, EXPORT_COLUMNS
- Option A: Keep in config.py, import in player_data_fetcher_main.py
- Option B: Move to player_data_fetcher_main.py as module-level constants
- Option C: Make them class-level constants in appropriate classes

**Question 4: Backward compatibility for other code importing config.py?**
- Need to check if any other scripts/tests import from player-data-fetcher/config.py
- If yes, need to maintain config.py for backward compatibility
- If no, can remove/modify freely

---

## Phase 1.5 Readiness

**Can I proceed to specification?**

✅ YES - Research is thorough enough to create detailed spec

**Evidence:**
- ✅ Can cite EXACT files that will be modified (3 files with line numbers)
- ✅ Have READ source code (not just searched) - copied actual signatures
- ✅ Can cite actual method signatures from source (main(), __init__, Settings class)
- ✅ Have searched for similar patterns (Feature 02's planned approach documented)
- ✅ Have reviewed Discovery Context (both DISCOVERY.md and S8.P1 findings)
- ✅ Understand current architecture completely (flow diagram created)

**Ready for S2.P2 (Specification Phase):** YES

---

**Research Complete:** 2026-01-31
**Next Phase:** S2.P2 Specification (create requirements with traceability)
