# Feature 01: Player Fetcher Configurability - Verified Interface Contracts

**Purpose:** Document ALL external interfaces verified from source code

**Verification Date:** 2026-01-31

**Note:** This feature is a simple CLI wrapper using standard library modules (argparse, asyncio, sys, pathlib) and internal modules. Standard library interfaces are well-documented and not verified here.

---

## Interface 1: player-data-fetcher/config.py - Module-Level Constants

**Source:** player-data-fetcher/config.py (lines 12-67)

**Verification Method:** Direct source code inspection (Read tool)

**Constants to Override (21 total):**

### Week/Season Constants
```python
CURRENT_NFL_WEEK = 17     # Line 12 - int, default 17
NFL_SEASON = 2025        # Line 13 - int, default 2025
```

### Data Preservation Constants
```python
PRESERVE_LOCKED_VALUES = False    # Line 16 - bool, default False
```

### Drafted Data Loading Constants
```python
LOAD_DRAFTED_DATA_FROM_FILE = True  # Line 19 - bool, default True
DRAFTED_DATA = "../data/drafted_data.csv"  # Line 20 - str path, default "../data/drafted_data.csv"
MY_TEAM_NAME = "Sea Sharp"  # Line 21 - str, default "Sea Sharp"
```

### Output Settings Constants
```python
OUTPUT_DIRECTORY = "./data"  # Line 24 - str path, default "./data"
CREATE_CSV = True  # Line 25 - bool, default True
CREATE_JSON = False  # Line 26 - bool, default False
CREATE_EXCEL = False  # Line 27 - bool, default False
CREATE_CONDENSED_EXCEL = False  # Line 28 - bool, default False
CREATE_POSITION_JSON = True  # Line 29 - bool, default True
```

### Position JSON Output Constants
```python
POSITION_JSON_OUTPUT = "../data/player_data"  # Line 33 - str path, default "../data/player_data"
```

### File Paths Constants
```python
TEAM_DATA_FOLDER = '../data/team_data'  # Line 36 - str path
GAME_DATA_CSV = '../data/game_data.csv'  # Line 37 - str path
```

### Feature Toggle Constants
```python
ENABLE_HISTORICAL_DATA_SAVE = False  # Line 41 - bool, default False
ENABLE_GAME_DATA_FETCH = True  # Line 44 - bool, default True
```

### Logging Configuration Constants
```python
LOGGING_LEVEL = 'INFO'  # Line 50 - str, choices: DEBUG/INFO/WARNING/ERROR/CRITICAL
LOGGING_TO_FILE = False  # Line 51 - bool, default False
LOGGING_FILE = './data/log.txt'  # Line 53 - str path
```

### Progress Tracking Constants
```python
PROGRESS_UPDATE_FREQUENCY = 10  # Line 57 - int, default 10
```

### ESPN API Constants
```python
ESPN_PLAYER_LIMIT = 2000  # Line 67 - int, default 2000
```

**Verification Status:** ✅ All 21 constants verified

**Interface Matches implementation_plan.md Assumptions:** ✅ YES
- All constants are module-level (can be overridden before importing main)
- Types match expectations (int, str, bool)
- Default values match spec.md descriptions

**Usage Pattern:**
```python
# After parsing CLI arguments
import sys
sys.path.insert(0, str(fetcher_dir))

# Import config module
from player-data-fetcher import config

# Override constants with CLI arguments
if args.week is not None:
    config.CURRENT_NFL_WEEK = args.week
if args.season is not None:
    config.NFL_SEASON = args.season
# ... etc for all 21 arguments

# Then import main (config overrides will be picked up by Settings class)
from player-data-fetcher import player_data_fetcher_main
```

---

## Interface 2: player-data-fetcher/player_data_fetcher_main.py - main() Function

**Source:** player-data-fetcher/player_data_fetcher_main.py:537

**Signature:**
```python
async def main():
    """Main application entry point"""
```

**Parameters:**
- None

**Returns:**
- None (implicit return, function completes successfully or raises exceptions)

**Side Effects:**
- Reads config module constants (CURRENT_NFL_WEEK, NFL_SEASON, LOGGING_LEVEL, etc.)
- Calls ESPN API to fetch player data
- Writes output files (CSV, JSON, Excel, Position JSON based on config settings)
- May write game data CSV if ENABLE_GAME_DATA_FETCH = True
- Logs to console or file based on LOGGING_TO_FILE setting

**Exceptions:**
- May raise exceptions from ESPN API calls (network errors, API errors)
- May raise exceptions from file I/O (disk full, permission errors)
- Exception handling is internal to main() - prints error messages and returns None

**Verified:** ✅ Interface matches implementation_plan.md assumptions
- Function is async (requires asyncio.run() to call)
- No parameters (all configuration via module-level constants)
- No explicit return value (returns None)

**Usage Pattern:**
```python
# After overriding config constants
from player-data-fetcher import player_data_fetcher_main
import asyncio

# Run async main
asyncio.run(player_data_fetcher_main.main())
```

---

## Interface 3: Standard Library Modules

**Modules Used:**
- `argparse` - CLI argument parsing (standard library, no verification needed)
- `asyncio` - Async execution support (standard library, no verification needed)
- `sys` - Python path manipulation (standard library, no verification needed)
- `pathlib.Path` - Path operations (standard library, no verification needed)

**Verification Status:** ✅ Standard library modules - well-documented, no verification needed

---

## Interface Verification Summary

**Total External Dependencies:** 3
- ✅ config.py (21 module-level constants) - VERIFIED
- ✅ player_data_fetcher_main.main() - VERIFIED
- ✅ Standard library modules (argparse, asyncio, sys, pathlib) - NO VERIFICATION NEEDED

**All interfaces match implementation_plan.md assumptions:** ✅ YES

**No interface mismatches found:** ✅ CORRECT

**Ready to proceed with implementation:** ✅ YES

---

## Notes

- Feature 01 is a simple CLI wrapper - minimal external dependencies
- All dependencies verified in S5 Round 1 Iteration 2 (original verification)
- This document re-verifies and documents interfaces before implementation (S6 Step 2)
- No mocks needed for production code (only for unit tests)
- Config override pattern verified (override before import)

---

**Last Updated:** 2026-01-31 12:40 (S6 Step 2 - Interface Verification Protocol)
