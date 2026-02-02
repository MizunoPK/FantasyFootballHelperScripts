# Feature 10 Specification: Refactor Player Fetcher to Constructor Pattern

**Status:** S2 IN PROGRESS
**Created:** 2026-01-31
**Last Updated:** 2026-01-31

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`
**Additional Context:** S8.P1 alignment analysis (Feature 01 vs Feature 02 comparison)

### This Feature's Scope (Missed Requirement)

**Feature 10: refactor_player_fetcher**

Refactor Feature 01 (player_fetcher) from config override pattern to constructor parameter pattern for architectural consistency across the epic.

**Type:** Missed Requirement (architectural improvement discovered during S8.P1 alignment)

**Background:**
- Feature 01 implemented during S5-S7 using config override pattern
- Pattern involves runtime modification of module constants via importlib
- During S8.P1 (cross-feature alignment), compared Feature 01 actual code to Feature 02 spec
- Constructor parameter pattern identified as better design (standard Python, clearer data flow)
- User decision: Refactor Feature 01 for consistency before Features 02-09 implement

**Dependencies:** Feature 01 complete through S7 (refactoring existing working code)

**Sequence Position:** Between Feature 07 and Feature 08 (establish pattern before integration testing)

**Estimated Size:** LARGE (refactoring 7+ files + 4 internal modules + rerunning 2518 tests)
**Note:** Scope expanded in S2.P3 (Question 4) to include refactoring internal modules that import CLI constants

---

### Relevant Discovery Decisions (from ../DISCOVERY.md)

**Epic Approach:** Comprehensive Script-Specific Argparse (Option 2)

**From DISCOVERY.md Iteration 1 (lines 40-61):**
- Epic request: Make 7 runner scripts configurable via CLI arguments
- Finding: 4 scripts have NO argparse (league_helper, player_fetcher, schedule_fetcher)
- Finding: 3 scripts HAVE argparse (simulations, game_data_fetcher, historical_compiler)
- Pattern inconsistency identified but no implementation pattern prescribed

**From DISCOVERY.md Iteration 2 (lines 68-86):**
- Player fetcher constants identified: 11 configurable constants in config.py
- Constants include: CURRENT_NFL_WEEK, PRESERVE_LOCKED_VALUES, OUTPUT_DIRECTORY, CREATE_CSV, etc.
- Schedule fetcher: NO config file found (would need arguments for season, output-path)

**Key Observation:** Original Discovery specified WHAT arguments to add, not HOW to architecturally implement configuration. Implementation pattern was left as implementation detail.

**From DISCOVERY.md User Answer Q1 (lines 24):**
> "Script-specific args focusing on constants.py settings for configurability"

This answer guided using constants.py as basis for arguments, but didn't specify whether to:
- **Option A:** Override constants at runtime (what Feature 01 did)
- **Option B:** Pass as constructor parameters (what should be done)

---

### Architectural Pattern Discovery (from S8.P1 Alignment)

**Source:** `../feature_02_schedule_fetcher/S8_P1_ALIGNMENT_ANALYSIS.md`

**What happened during S8.P1:**
1. Feature 01 completed S5-S7 using config override pattern
2. During S8.P1, compared Feature 01 actual code to Feature 02 spec
3. Feature 02 spec (written during S2) planned constructor parameter approach
4. Feature 01 actual implementation used config override approach
5. Architectural pattern mismatch identified

**Feature 01 Current Pattern (Config Override):**
```python
# run_player_fetcher.py lines 319-442
script_dir = Path(__file__).parent
fetcher_dir = script_dir / "player-data-fetcher"
sys.path.insert(0, str(fetcher_dir))

# Import config module
config = importlib.import_module('config')

# Override constants at runtime
if args.debug:
    config.LOGGING_LEVEL = 'DEBUG'
    config.ESPN_PLAYER_LIMIT = 100
    # ... more overrides

# Import main module (uses already-modified config)
player_data_fetcher_main = importlib.import_module('player_data_fetcher_main')
asyncio.run(player_data_fetcher_main.main())
```

**Feature 02 Planned Pattern (Constructor Parameters):**
```python
# From Feature 02 spec.md Algorithm 2 (lines 377-430)
parser.add_argument('--log-level', default='INFO')
args = parser.parse_args()

# Create fetcher with parameters
fetcher = ScheduleFetcher(
    output_path=args.output_path,
    log_level=args.log_level
)
await fetcher.fetch_full_schedule(season=args.season, weeks=args.weeks)
```

**User Decision (from S8.P1 discussion):**
> "I believed it'd likely be better to remove the constants from config.py files entirely and have them be parameters passed to the scripts via the arguments and defaults in the runner scripts. Would that be more consistent and better design? I feel like overriding the config variables would just be confusing."

**Answer:** Constructor parameter pattern is better design

**Rationale:**
- ✅ Explicit data flow: arguments → constructor → implementation
- ✅ Standard Python: direct parameter passing (dependency injection)
- ✅ No "magic": no runtime module constant overriding
- ✅ Better testability: instantiate classes with any config
- ✅ Single source of truth: defaults in argparse only
- ✅ Self-documenting: constructor signatures show what's configurable

---

### Relevant User Answers

**Question (S8.P1):** Should Feature 01 be refactored to match constructor pattern?
- **Answer:** "create a missed requirements feature for refactoring feature 1"
- **Impact:** Feature 10 created to refactor Feature 01

**Question (S8.P1):** Where in sequence should Feature 10 be implemented?
- **Answer:** "new feature that should be done between features 7 and 8"
- **Priority:** Medium (establish pattern after new implementations, before integration testing)
- **Impact:** Features 02-09 will use constructor pattern; Feature 01 refactored to match

---

## Components Affected

**Research Reference:** `../research/REFACTOR_PLAYER_FETCHER_RESEARCH.md`

### Files to Modify

**1. run_player_fetcher.py** (445 lines - MAJOR REFACTORING)

**Current State:**
- Lines 62-314: ArgumentParser setup (23 arguments)
- Lines 319-332: Config module import via importlib
- Lines 334-431: Config override logic (runtime constant modification)
- Lines 433-442: Import player_data_fetcher_main and run async main()

**Modifications Required:**
- **KEEP:** Lines 62-317 (ArgumentParser setup - no changes)
- **REMOVE:** Lines 319-332 (config import via importlib)
- **REMOVE:** Lines 334-431 (config override logic)
- **REPLACE:** Lines 433-442 with new approach (create settings dict, pass to main)

**New Code Required:**
- Function to create settings dictionary from parsed args
- Import player-data-fetcher/ as package (not via importlib tricks)
- Call main() with settings dictionary parameter

**Source:** Research - run_player_fetcher.py lines documented in REFACTOR_PLAYER_FETCHER_RESEARCH.md

---

**2. player-data-fetcher/player_data_fetcher_main.py** (615+ lines - MAJOR REFACTORING)

**Current State:**
- Lines 33-39: Import config constants (15 constants)
- Lines 42-98: Settings class (reads from config constants)
- Lines 100-130: NFLProjectionsCollector.__init__ (takes Settings parameter) ✅ GOOD
- Lines 537-550: main() function (NO parameters, creates Settings from config)
- Lines 565, 576: Direct config constant usage in main()

**Modifications Required:**
- **Line 537:** Change `async def main():` to `async def main(settings_dict: dict | None = None):`
- **Lines 546:** Change `settings = Settings()` to `settings = create_settings_from_dict(settings_dict)`
- **Lines 540, 565, 576:** Remove direct config constant usage (pass via Settings or parameters)
- **Lines 33-39:** Remove or modify config imports (TBD - see Question 3 in checklist)
- **Lines 42-98:** Modify Settings class to accept constructor parameters (TBD - see Question 2)

**New Code Required:**
- Factory function to create Settings from dictionary
- Settings class modifications to accept constructor kwargs
- Logging setup that doesn't rely on module-level constants

**Source:** Research - player_data_fetcher_main.py lines documented in REFACTOR_PLAYER_FETCHER_RESEARCH.md

---

**3. player-data-fetcher/config.py** (90 lines - MINOR CHANGES)

**Current State:**
- Contains 23 constants exposed to CLI (CURRENT_NFL_WEEK, NFL_SEASON, OUTPUT_DIRECTORY, etc.)
- Contains additional constants NOT exposed to CLI (LOG_NAME, LOGGING_FORMAT, EXPORT_COLUMNS, etc.)

**Modifications Required (User Answer: Option C from Question 1):**
- **Keep non-CLI constants** (LOG_NAME, LOGGING_FORMAT, DEFAULT_FILE_CAPS, EXPORT_COLUMNS, COORDINATES_JSON, ESPN_USER_AGENT, REQUEST_TIMEOUT, RATE_LIMIT_DELAY)
- **Remove or document CLI-configurable constants** (can be deleted since argparse has defaults)
- **Add clear comments** marking which constants are internal-only
- **Update header comments** to clarify purpose (internal constants, not CLI-configurable)

**New Structure:**
```python
# player-data-fetcher/config.py (after refactoring)
"""
Internal Configuration Constants

These constants are NOT configurable via CLI arguments.
For CLI-configurable settings, see run_player_fetcher.py argparse defaults.
"""

# Logging Configuration (internal - not CLI-configurable)
LOG_NAME = "player_data_fetcher"
LOGGING_FORMAT = 'standard'

# Export Configuration (internal - not CLI-configurable)
DEFAULT_FILE_CAPS = {'csv': 5, 'json': 18, 'xlsx': 5, 'txt': 5}
EXCEL_POSITION_SHEETS = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
EXPORT_COLUMNS = ['id', 'name', 'team', ...]
COORDINATES_JSON = 'coordinates.json'

# API Configuration (internal - not CLI-configurable)
ESPN_USER_AGENT = "Mozilla/5.0..."
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.2

# NOTE: CLI-configurable constants removed (defaults now in argparse)
```

**Source:** Research + User Answer (Question 1: Option C, Question 4: Hybrid approach)

**Note:** Since internal modules import CLI constants from config.py, those constants will be REMOVED from config.py per Question 4 resolution. Internal modules will be refactored to receive Settings object instead.

---

**4. player-data-fetcher/espn_client.py** (MODERATE REFACTORING - Added per Question 4)

**Current State:**
- Line 27: Imports ESPN_USER_AGENT, ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK from config.py
- Multiple other imports of NFL_SEASON, CURRENT_NFL_WEEK throughout file (lines 617, 651, 914, 981, 1068, 1469, 1878)

**Modifications Required:**
- **Remove:** Import statements for CLI-configurable constants (ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK, NFL_SEASON)
- **Keep:** Import ESPN_USER_AGENT (non-CLI constant, stays in config.py)
- **Add:** Constructor parameter to accept Settings object
- **Refactor:** Replace all references to CLI constants with self.settings.field_name

**New Pattern:**
```python
from config import ESPN_USER_AGENT, REQUEST_TIMEOUT, RATE_LIMIT_DELAY  # Non-CLI only

class ESPNClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        # Use self.settings.espn_player_limit instead of ESPN_PLAYER_LIMIT
        # Use self.settings.current_nfl_week instead of CURRENT_NFL_WEEK
```

**Source:** Research Finding (Question 4 backward compatibility check)

---

**5. player-data-fetcher/player_data_exporter.py** (MAJOR REFACTORING - Added per Question 4)

**Current State:**
- Lines 31-32: Imports 11 constants from config.py (mix of CLI and non-CLI)
  - Non-CLI: DEFAULT_FILE_CAPS, EXCEL_POSITION_SHEETS, EXPORT_COLUMNS
  - CLI: CREATE_POSITION_JSON, POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK, PRESERVE_LOCKED_VALUES, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME

**Modifications Required:**
- **Remove:** Import statements for CLI-configurable constants (8 constants)
- **Keep:** Import non-CLI constants (DEFAULT_FILE_CAPS, EXCEL_POSITION_SHEETS, EXPORT_COLUMNS)
- **Add:** Constructor parameter to accept Settings object
- **Refactor:** Replace all references to CLI constants with self.settings.field_name

**New Pattern:**
```python
from config import DEFAULT_FILE_CAPS, EXCEL_POSITION_SHEETS, EXPORT_COLUMNS  # Non-CLI only

class PlayerDataExporter:
    def __init__(self, settings: Settings, ...):
        self.settings = settings
        # Use self.settings.create_position_json instead of CREATE_POSITION_JSON
```

**Source:** Research Finding (Question 4 backward compatibility check)

---

**6. player-data-fetcher/game_data_fetcher.py** (MODERATE REFACTORING - Added per Question 4)

**Current State:**
- Lines 30-33: Imports 6 constants from config.py
  - Non-CLI: COORDINATES_JSON, REQUEST_TIMEOUT, RATE_LIMIT_DELAY
  - CLI: CURRENT_NFL_WEEK, NFL_SEASON, GAME_DATA_CSV

**Modifications Required:**
- **Remove:** Import statements for CLI-configurable constants (3 constants)
- **Keep:** Import non-CLI constants (COORDINATES_JSON, REQUEST_TIMEOUT, RATE_LIMIT_DELAY)
- **Add:** Constructor parameter to accept Settings object
- **Refactor:** Replace all references to CLI constants with self.settings.field_name

**New Pattern:**
```python
from config import COORDINATES_JSON, REQUEST_TIMEOUT, RATE_LIMIT_DELAY  # Non-CLI only

class GameDataFetcher:
    def __init__(self, settings: Settings, ...):
        self.settings = settings
        # Use self.settings.current_nfl_week instead of CURRENT_NFL_WEEK
```

**Source:** Research Finding (Question 4 backward compatibility check)

---

**7. player-data-fetcher/fantasy_points_calculator.py** (MINOR REFACTORING - Added per Question 4)

**Current State:**
- Line 30: Imports NFL_SEASON from config.py (CLI-configurable)

**Modifications Required:**
- **Remove:** Import statement for NFL_SEASON
- **Add:** Constructor parameter to accept Settings object
- **Refactor:** Replace NFL_SEASON references with self.settings.nfl_season

**New Pattern:**
```python
class FantasyPointsCalculator:
    def __init__(self, settings: Settings, ...):
        self.settings = settings
        # Use self.settings.nfl_season instead of NFL_SEASON
```

**Source:** Research Finding (Question 4 backward compatibility check)

---

### Files to Create

**None** - This is a refactoring feature, not new functionality

**Source:** Derived - Refactoring existing code doesn't require new files

---

## Requirements

### R1: Remove Config Override Pattern from run_player_fetcher.py

**Description:** Remove all config module import and runtime constant modification code from run_player_fetcher.py

**Source:** User Answer (S8.P1 discussion): "I believed it'd likely be better to remove the constants from config.py files entirely and have them be parameters passed to the scripts via the arguments"

**Current Implementation (TO BE REMOVED):**
```python
# Lines 319-332: Config import via importlib
config = importlib.import_module('config')

# Lines 334-431: Runtime constant modification
if args.debug:
    config.LOGGING_LEVEL = 'DEBUG'
    config.ESPN_PLAYER_LIMIT = 100
    # ... 20+ more overrides
```

**Why Removing:**
- User identified as confusing pattern
- Non-standard Python (runtime module constant modification)
- Constructor parameter pattern preferred

**Implementation:**
- Remove lines 319-332 (config import)
- Remove lines 334-431 (config override logic)
- Remove `import importlib` and `import sys` if no longer needed

**Acceptance Criteria:**
- No `importlib.import_module('config')` in run_player_fetcher.py
- No `config.CONSTANT_NAME = value` assignments
- Code still passes all 2518 tests

**Traceability:** User Answer → S8.P1 discussion

---

### R2: Create Settings Dictionary from Parsed Arguments

**Description:** Create a function or code block that converts argparse Namespace to settings dictionary for passing to main()

**Source:** Derived Requirement - Necessary to implement R1 (need way to pass args to main)

**Derivation:** If removing config override pattern, must pass arguments another way. Constructor parameter pattern requires creating settings dict from parsed args.

**Implementation:**
```python
# New code in run_player_fetcher.py (after args = parser.parse_args())
def create_settings_dict(args) -> dict:
    """Create settings dictionary from parsed arguments"""
    settings = {}

    # Map CLI args to settings keys
    if args.week is not None:
        settings['current_nfl_week'] = args.week
    if args.season is not None:
        settings['season'] = args.season
    # ... map all 23 arguments

    # Apply debug mode overrides
    if args.debug:
        settings['logging_level'] = 'DEBUG'
        settings['espn_player_limit'] = 100
        # ... other debug overrides

    # Apply E2E mode overrides
    if args.e2e_test:
        settings['espn_player_limit'] = 100
        # ... other E2E overrides

    return settings
```

**Acceptance Criteria:**
- Function maps all 23 CLI arguments to settings dictionary
- Debug mode overrides applied correctly (precedence maintained)
- E2E mode overrides applied correctly (precedence maintained)
- Returns dictionary suitable for passing to main()

**Traceability:** Derived from R1

---

### R3: Modify main() to Accept Settings Parameter

**Description:** Change player_data_fetcher_main.main() signature from `async def main():` to `async def main(settings_dict: dict | None = None):`

**Source:** Derived Requirement - Necessary to implement R2 (need main to accept settings)

**Derivation:** Constructor parameter pattern requires main() to accept parameters instead of reading from module-level config constants.

**Current Signature:**
```python
# player_data_fetcher_main.py line 537
async def main():
    """Main application entry point"""
    logger = setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
    settings = Settings()  # ← NO parameters
```

**New Signature:**
```python
async def main(settings_dict: dict | None = None):
    """Main application entry point

    Args:
        settings_dict: Optional settings dictionary from CLI args.
                      If None, uses defaults from config.py (for backward compatibility).
    """
    # Create logging config from settings_dict or defaults
    log_config = extract_logging_config(settings_dict)
    logger = setup_logger(**log_config)

    # Create Settings object from settings_dict or defaults
    settings = create_settings_from_dict(settings_dict)
```

**Acceptance Criteria:**
- main() signature accepts optional settings_dict parameter
- If settings_dict is None, uses defaults (backward compatibility)
- If settings_dict provided, creates Settings from it
- No direct usage of module-level config constants in main()

**Traceability:** Derived from R2

---

### R4: Create Settings from Dictionary (Not Config Constants)

**Description:** Implement function/method to create Settings object from settings dictionary instead of reading config module constants

**Source:** Derived Requirement - Necessary to implement R3 (main needs way to create Settings from dict)

**Derivation:** Settings class currently reads from config constants as defaults. Need way to override those defaults with values from settings_dict.

**Current Pattern (TO BE CHANGED):**
```python
# player_data_fetcher_main.py line 42-98
class Settings(BaseSettings):
    season: int = NFL_SEASON  # ← Reads from config constant
    current_nfl_week: int = CURRENT_NFL_WEEK  # ← Reads from config constant
    # ... all fields read from config constants
```

**Implementation Options (TBD - see checklist.md Question 2):**
- **Option A:** Modify Settings.__init__ to accept kwargs
- **Option B:** Create factory function `create_settings_from_dict(settings_dict)`
- **Option C:** Use pydantic's model_validate() method

**Acceptance Criteria:**
- Settings object created from settings_dict (not config constants)
- All 23 configurable fields properly mapped
- Non-CLI fields use appropriate defaults
- Validation still works (pydantic validation preserved)

**Traceability:** Derived from R3

---

### R5: Maintain 100% Test Pass Rate

**Description:** All 2518 existing tests must continue to pass after refactoring

**Source:** Epic Quality Requirement - Feature 01 had 2518/2518 tests passing; refactoring must maintain quality

**Why Critical:**
- Refactoring existing working code (Feature 01 is production-ready)
- Zero tolerance for breaking changes
- Tests validate all functionality still works

**Acceptance Criteria:**
- Run `python tests/run_all_tests.py` → exit code 0
- All 2518 tests pass (100% pass rate)
- No new test failures introduced
- No existing tests skipped or removed

**Test Categories to Verify:**
- run_player_fetcher.py argument parsing (12 tests)
- Player data fetcher E2E functionality
- Debug mode behavior
- E2E test mode behavior
- All other existing tests

**Traceability:** Epic Quality Standard + Feature 01 complete status

---

### R6: Preserve All Existing Functionality

**Description:** After refactoring, all 23 CLI arguments, debug mode, and E2E mode must work identically

**Source:** Epic Requirement - Feature 01 implements 23 args + debug + E2E; refactoring must preserve

**Functionality to Preserve:**
- All 23 CLI arguments (--week, --season, --output-dir, etc.)
- Debug mode behavior (DEBUG logging + ESPN_PLAYER_LIMIT=100 + minimal formats)
- E2E test mode behavior (ESPN_PLAYER_LIMIT=100 + disabled features)
- Mode precedence (debug → E2E → individual args)
- Validation (week 1-18, season warnings)
- Help text (argparse --help output)

**Acceptance Criteria:**
- `python run_player_fetcher.py --help` shows all 23 args
- `python run_player_fetcher.py --debug` works identically
- `python run_player_fetcher.py --e2e-test` works identically
- `python run_player_fetcher.py --week 12 --season 2025` works
- All argument combinations work as before

**Verification Method:**
- Manual smoke testing (run with different arg combinations)
- Compare output before/after refactoring
- All existing integration tests pass

**Traceability:** Feature 01 Implementation (run_player_fetcher.py 445 lines with 23 args)

---

### R7: Improve Code Clarity (Architectural Goal)

**Description:** Refactored code should be more maintainable and follow standard Python patterns

**Source:** User Decision (S8.P1): Constructor pattern is "better design" and config override is "confusing"

**Improvements Expected:**
- ✅ Explicit data flow: arguments → dict → Settings → Collector
- ✅ Standard Python: No importlib tricks, no runtime constant modification
- ✅ Self-documenting: main(settings_dict) signature shows what's configurable
- ✅ Better testability: Can call main() with any settings dict in tests
- ✅ Single source of truth: Defaults in one place (argparse or Settings defaults)

**Non-Goals:**
- NOT adding new features
- NOT changing behavior (only implementation)
- NOT optimizing performance

**Acceptance Criteria:**
- No `importlib.import_module()` usage in run_player_fetcher.py
- main() signature shows it accepts configuration
- Code review shows improved clarity (subjective but documentable)

**Traceability:** User Answer → S8.P1 architectural decision

---

### R8: Handle Non-CLI Constants

**Description:** Keep non-CLI constants in config.py, remove CLI-configurable constants

**Source:** Research Finding + User Answer (Question 1: Option C)

**Decision:** Keep config.py for internal constants only, remove CLI-configurable constants

**Constants to Keep in config.py (NOT CLI-configurable):**
- LOG_NAME = "player_data_fetcher"
- LOGGING_FORMAT = 'standard'
- DEFAULT_FILE_CAPS = {'csv': 5, 'json': 18, 'xlsx': 5, 'txt': 5}
- EXCEL_POSITION_SHEETS = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
- EXPORT_COLUMNS = ['id', 'name', 'team', 'position', ...]
- COORDINATES_JSON = 'coordinates.json'
- ESPN_USER_AGENT = "Mozilla/5.0..."
- REQUEST_TIMEOUT = 30
- RATE_LIMIT_DELAY = 0.2

**Constants to Remove from config.py (CLI-configurable - defaults in argparse):**
- CURRENT_NFL_WEEK (default: 17 in argparse)
- NFL_SEASON (default: 2025 in argparse)
- PRESERVE_LOCKED_VALUES (default: False in argparse)
- LOAD_DRAFTED_DATA_FROM_FILE (default: True in argparse)
- DRAFTED_DATA (default: "../data/drafted_data.csv" in argparse)
- MY_TEAM_NAME (default: "Sea Sharp" in argparse)
- OUTPUT_DIRECTORY (default: "./data" in argparse)
- CREATE_CSV, CREATE_JSON, CREATE_EXCEL, etc. (defaults in argparse)
- ENABLE_HISTORICAL_DATA_SAVE (default: False in argparse)
- ENABLE_GAME_DATA_FETCH (default: True in argparse)
- LOGGING_LEVEL (default: 'INFO' in argparse)
- LOGGING_TO_FILE (default: False in argparse)
- LOGGING_FILE (default: './data/log.txt' in argparse)
- PROGRESS_UPDATE_FREQUENCY (default: 10 in argparse)
- ESPN_PLAYER_LIMIT (default: 2000 in argparse)

**Implementation:**
- Refactor config.py to only contain non-CLI constants
- Add clear header comments explaining purpose
- player_data_fetcher_main.py imports non-CLI constants from config.py (Question 3: Option A)
- Settings class uses hardcoded defaults (or from settings_dict parameter)

**Acceptance Criteria:**
- config.py contains only non-CLI constants (9 constants)
- Clear comments mark internal-only constants
- player_data_fetcher_main.py imports work correctly
- No broken references

**Traceability:** Research Finding → User Answer (Question 1: Option C, Question 3: Option A, Question 4: Hybrid approach)

---

### R9: Refactor espn_client.py to Accept Settings Object

**Description:** Modify ESPNClient class to receive Settings object via constructor instead of importing CLI constants from config.py

**Source:** Question 4 Research Finding (backward compatibility check)

**Why Required:** espn_client.py currently imports ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK, NFL_SEASON from config.py. Since these constants will be removed from config.py (R8), ESPNClient must receive them via Settings object.

**Current Pattern (TO BE CHANGED):**
```python
from config import ESPN_USER_AGENT, ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK
# ... multiple other imports of NFL_SEASON, CURRENT_NFL_WEEK
```

**New Pattern:**
```python
from config import ESPN_USER_AGENT, REQUEST_TIMEOUT, RATE_LIMIT_DELAY  # Non-CLI only

class ESPNClient:
    def __init__(self, settings: Settings, ...):
        self.settings = settings
        # Use self.settings.espn_player_limit instead of ESPN_PLAYER_LIMIT
        # Use self.settings.current_nfl_week instead of CURRENT_NFL_WEEK
        # Use self.settings.nfl_season instead of NFL_SEASON
```

**Acceptance Criteria:**
- ESPNClient.__init__ accepts Settings object as parameter
- All references to ESPN_PLAYER_LIMIT replaced with self.settings.espn_player_limit
- All references to CURRENT_NFL_WEEK replaced with self.settings.current_nfl_week
- All references to NFL_SEASON replaced with self.settings.nfl_season
- ESPN_USER_AGENT still imported from config.py (non-CLI constant)
- All existing tests pass (100% pass rate maintained)

**Traceability:** Question 4 Answer (Hybrid approach) → Backward compatibility requirement

---

### R10: Refactor player_data_exporter.py to Accept Settings Object

**Description:** Modify PlayerDataExporter class to receive Settings object via constructor instead of importing CLI constants from config.py

**Source:** Question 4 Research Finding (backward compatibility check)

**Why Required:** player_data_exporter.py imports 8 CLI-configurable constants from config.py. These constants will be removed from config.py (R8), so PlayerDataExporter must receive them via Settings object.

**Current Pattern (TO BE CHANGED):**
```python
from config import DEFAULT_FILE_CAPS, CREATE_POSITION_JSON, POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK
from config import EXCEL_POSITION_SHEETS, EXPORT_COLUMNS, PRESERVE_LOCKED_VALUES, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME
```

**New Pattern:**
```python
from config import DEFAULT_FILE_CAPS, EXCEL_POSITION_SHEETS, EXPORT_COLUMNS  # Non-CLI only

class PlayerDataExporter:
    def __init__(self, settings: Settings, ...):
        self.settings = settings
        # Use self.settings.create_position_json instead of CREATE_POSITION_JSON
        # Use self.settings.current_nfl_week instead of CURRENT_NFL_WEEK
        # ... etc for all 8 CLI constants
```

**Acceptance Criteria:**
- PlayerDataExporter.__init__ accepts Settings object as parameter
- All references to CLI constants replaced with self.settings.field_name
- Non-CLI constants (DEFAULT_FILE_CAPS, EXCEL_POSITION_SHEETS, EXPORT_COLUMNS) still imported from config.py
- All existing tests pass (100% pass rate maintained)

**Traceability:** Question 4 Answer (Hybrid approach) → Backward compatibility requirement

---

### R11: Refactor game_data_fetcher.py to Accept Settings Object

**Description:** Modify GameDataFetcher class to receive Settings object via constructor instead of importing CLI constants from config.py

**Source:** Question 4 Research Finding (backward compatibility check)

**Why Required:** game_data_fetcher.py imports 3 CLI-configurable constants from config.py. These constants will be removed from config.py (R8), so GameDataFetcher must receive them via Settings object.

**Current Pattern (TO BE CHANGED):**
```python
from config import (
    CURRENT_NFL_WEEK, NFL_SEASON, GAME_DATA_CSV, COORDINATES_JSON,
    REQUEST_TIMEOUT, RATE_LIMIT_DELAY
)
```

**New Pattern:**
```python
from config import COORDINATES_JSON, REQUEST_TIMEOUT, RATE_LIMIT_DELAY  # Non-CLI only

class GameDataFetcher:
    def __init__(self, settings: Settings, ...):
        self.settings = settings
        # Use self.settings.current_nfl_week instead of CURRENT_NFL_WEEK
        # Use self.settings.nfl_season instead of NFL_SEASON
        # Use self.settings.game_data_csv instead of GAME_DATA_CSV
```

**Acceptance Criteria:**
- GameDataFetcher.__init__ accepts Settings object as parameter
- All references to CLI constants replaced with self.settings.field_name
- Non-CLI constants (COORDINATES_JSON, REQUEST_TIMEOUT, RATE_LIMIT_DELAY) still imported from config.py
- All existing tests pass (100% pass rate maintained)

**Traceability:** Question 4 Answer (Hybrid approach) → Backward compatibility requirement

---

### R12: Refactor fantasy_points_calculator.py to Accept Settings Object

**Description:** Modify FantasyPointsCalculator class to receive Settings object via constructor instead of importing CLI constants from config.py

**Source:** Question 4 Research Finding (backward compatibility check)

**Why Required:** fantasy_points_calculator.py imports NFL_SEASON from config.py. This constant will be removed from config.py (R8), so FantasyPointsCalculator must receive it via Settings object.

**Current Pattern (TO BE CHANGED):**
```python
from config import NFL_SEASON
```

**New Pattern:**
```python
class FantasyPointsCalculator:
    def __init__(self, settings: Settings, ...):
        self.settings = settings
        # Use self.settings.nfl_season instead of NFL_SEASON
```

**Acceptance Criteria:**
- FantasyPointsCalculator.__init__ accepts Settings object as parameter
- All references to NFL_SEASON replaced with self.settings.nfl_season
- All existing tests pass (100% pass rate maintained)

**Traceability:** Question 4 Answer (Hybrid approach) → Backward compatibility requirement

---

## Data Structures

### Settings Dictionary (New - Created in run_player_fetcher.py)

**Type:** `dict[str, Any]`

**Purpose:** Transfer parsed CLI arguments to player_data_fetcher_main.main()

**Structure:**
```python
{
    # Week/Season
    'season': int | None,                    # NFL season year (e.g., 2025)
    'current_nfl_week': int | None,         # Current NFL week (1-18)

    # Data Preservation
    'preserve_locked_values': bool | None,
    'load_drafted_data_from_file': bool | None,
    'drafted_data': str | None,             # File path
    'my_team_name': str | None,

    # Output Settings
    'output_directory': str | None,
    'create_csv': bool | None,
    'create_json': bool | None,
    'create_excel': bool | None,
    'create_condensed_excel': bool | None,
    'create_position_json': bool | None,
    'position_json_output': str | None,

    # File Paths
    'team_data_folder': str | None,
    'game_data_csv': str | None,

    # Feature Toggles
    'enable_historical_data_save': bool | None,
    'enable_game_data_fetch': bool | None,

    # Logging
    'logging_level': str | None,            # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    'logging_to_file': bool | None,
    'logging_file': str | None,
    'progress_update_frequency': int | None,

    # API Settings (from debug/E2E modes)
    'espn_player_limit': int | None,        # Overridden by debug/E2E modes
}
```

**Notes:**
- All values are optional (None if not provided by CLI)
- Keys match Settings class field names (snake_case)
- Created by create_settings_dict() function in run_player_fetcher.py

**Source:** Research - All 23 CLI arguments mapped to dictionary keys

---

### Settings Class (Modified - player_data_fetcher_main.py)

**Type:** `pydantic.BaseSettings`

**Current State:**
```python
class Settings(BaseSettings):
    season: int = NFL_SEASON  # ← Reads from config constant
    current_nfl_week: int = CURRENT_NFL_WEEK  # ← Reads from config constant
    # ... all fields read from config module constants
```

**Target State (TBD - see checklist.md Question 2):**
```python
class Settings(BaseSettings):
    season: int = 2025  # ← Hardcoded default or from constructor
    current_nfl_week: int = 17  # ← Hardcoded default or from constructor
    # ... all fields with defaults not from config module

    # Option A: Accept kwargs in __init__
    # Option B: Use factory function create_settings_from_dict()
    # Option C: Use pydantic's model_validate()
```

**Fields (23 configurable + others):**
- Same fields as current Settings class
- Defaults changed from config constants to hardcoded or constructor-provided
- Pydantic validation preserved

**Source:** Research - Settings class documented in REFACTOR_PLAYER_FETCHER_RESEARCH.md lines 42-98

---

### Logging Configuration (New - Extracted from settings_dict)

**Type:** `dict[str, Any]`

**Purpose:** Pass logging configuration to setup_logger() without using module-level constants

**Structure:**
```python
{
    'name': str,        # Logger name (e.g., "player_data_fetcher")
    'level': str,       # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    'to_file': bool,    # Whether to log to file
    'log_file': str,    # File path for file logging
    'format': str,      # 'standard', 'detailed', 'simple'
}
```

**Created by:** extract_logging_config(settings_dict) function in player_data_fetcher_main.py

**Source:** Derived - Necessary to call setup_logger() without module-level constants

---

## Algorithms

### Algorithm 1: Create Settings Dictionary from Parsed Args

**Location:** run_player_fetcher.py (new function)

**Purpose:** Convert argparse Namespace to settings dictionary for passing to main()

```
def create_settings_dict(args: argparse.Namespace) -> dict:
    """
    Create settings dictionary from parsed CLI arguments.

    Applies mode precedence: debug → E2E → individual args
    """
    settings = {}

    # PHASE 1: Apply debug mode overrides (if --debug flag set)
    if args.debug:
        settings['logging_level'] = 'DEBUG'
        settings['espn_player_limit'] = 100
        settings['progress_update_frequency'] = 5
        settings['enable_game_data_fetch'] = False
        settings['enable_historical_data_save'] = False
        settings['create_csv'] = True
        settings['create_json'] = False
        settings['create_excel'] = False
        settings['create_condensed_excel'] = False
        settings['create_position_json'] = True

    # PHASE 2: Apply E2E mode overrides (if --e2e-test flag set)
    # Note: E2E overrides data limits, preserves debug logging if --debug also set
    if args.e2e_test:
        settings['espn_player_limit'] = 100  # E2E precedence over debug
        settings['enable_game_data_fetch'] = False
        settings['enable_historical_data_save'] = False
        settings['create_excel'] = False
        settings['create_json'] = False

    # PHASE 3: Apply individual CLI argument overrides
    # Note: Only override if arg is not None (user explicitly provided it)
    if args.week is not None:
        settings['current_nfl_week'] = args.week
    if args.season is not None:
        settings['season'] = args.season
    if args.preserve_locked is not None:
        settings['preserve_locked_values'] = args.preserve_locked
    # ... apply all 23 arguments if not None

    return settings
```

**Mode Precedence:**
1. Debug mode sets defaults for logging + data limits
2. E2E mode overrides data limits (but not debug logging)
3. Individual args override everything

**Source:** Derived from Feature 01's config override logic (run_player_fetcher.py lines 334-431)

---

### Algorithm 2: Create Settings Object from Dictionary

**Location:** player_data_fetcher_main.py (new function)

**Purpose:** Create pydantic Settings object from settings dictionary (not config constants)

**Implementation (User Answer: Option B from Question 2):**

```python
def create_settings_from_dict(settings_dict: dict | None) -> Settings:
    """
    Create Settings object from dictionary or use defaults.

    Args:
        settings_dict: Optional dictionary with settings from CLI args.
                      If None, uses Settings class field defaults.

    Returns:
        Settings object with values from settings_dict or defaults
    """
    if settings_dict is None:
        # No settings provided - use Settings class defaults
        return Settings()

    # Create Settings from dictionary using pydantic's model_validate
    # This validates all fields according to Settings class definition
    return Settings.model_validate(settings_dict)
```

**Usage:**
```python
# In main()
settings = create_settings_from_dict(settings_dict)
settings.validate_settings()
```

**Benefits:**
- Clean separation (Settings class stays simple)
- Handles None case gracefully
- Leverages pydantic's validation
- Easy to test
- Settings class field definitions remain unchanged

**Source:** Derived from R4 requirement + User Answer (Question 2: Option B)

---

### Algorithm 3: Extract Logging Configuration

**Location:** player_data_fetcher_main.py (new function)

**Purpose:** Extract logging config from settings_dict for setup_logger() call

```python
# Import non-CLI constants from config.py (per Question 3: Option A)
from config import LOG_NAME, LOGGING_FORMAT

def extract_logging_config(settings_dict: dict | None) -> dict:
    """
    Extract logging configuration from settings dictionary.

    Returns dictionary suitable for setup_logger() function.
    Uses LOG_NAME and LOGGING_FORMAT from config.py (not CLI-configurable).
    """
    if settings_dict is None:
        # Use defaults (from config.py or hardcoded)
        return {
            'name': LOG_NAME,  # From config.py
            'level': 'INFO',
            'to_file': False,
            'log_file': './data/log.txt',
            'format': LOGGING_FORMAT  # From config.py
        }

    return {
        'name': LOG_NAME,  # From config.py (not CLI-configurable)
        'level': settings_dict.get('logging_level', 'INFO'),
        'to_file': settings_dict.get('logging_to_file', False),
        'log_file': settings_dict.get('logging_file', './data/log.txt'),
        'format': LOGGING_FORMAT  # From config.py (not CLI-configurable)
    }
```

**Source:** Derived from main() requirement (R3)
**Answer:** Question 3 (keep non-CLI constants in config.py, import them)

---

### Algorithm 4: Main Execution Flow (Refactored)

**Location:** player_data_fetcher_main.py main() function

**Current Flow (TO BE CHANGED):**
```python
async def main():
    logger = setup_logger(LOG_NAME, LOGGING_LEVEL, ...)  # ← Reads globals
    settings = Settings()  # ← Reads from config constants
    collector = NFLProjectionsCollector(settings)
    # ... rest of execution
```

**New Flow:**
```python
async def main(settings_dict: dict | None = None):
    # Extract logging config from settings_dict (not module constants)
    log_config = extract_logging_config(settings_dict)
    logger = setup_logger(**log_config)

    # Create Settings from settings_dict (not config constants)
    settings = create_settings_from_dict(settings_dict)
    settings.validate_settings()

    # Rest of execution unchanged (already uses Settings object)
    collector = NFLProjectionsCollector(settings)
    projection_data = await collector.collect_all_projections()

    # Game data fetch (use settings, not ENABLE_GAME_DATA_FETCH global)
    if settings.enable_game_data_fetch:  # ← From Settings, not global
        game_data_fetched = collector.fetch_game_data()
        # ...

    # Historical data save (use settings, not ENABLE_HISTORICAL_DATA_SAVE global)
    if settings.enable_historical_data_save:  # ← From Settings, not global
        saved = collector.save_to_historical_data()
        # ...

    # ... rest unchanged
```

**Key Changes:**
- Accepts settings_dict parameter
- Creates logging config from settings_dict (not module globals)
- Creates Settings from settings_dict (not config constants)
- Uses settings fields instead of module globals (lines 565, 576)

**Source:** Derived from R3 requirement

---

### Algorithm 5: Runner Script Main Flow (Refactored)

**Location:** run_player_fetcher.py main() function

**Current Flow (TO BE CHANGED):**
```python
def main(argv: list[str] | None = None) -> None:
    args = parser.parse_args(argv)

    # Import config module
    config = importlib.import_module('config')

    # Override config constants
    if args.debug:
        config.LOGGING_LEVEL = 'DEBUG'
        # ... 20+ overrides

    # Import and run main
    player_data_fetcher_main = importlib.import_module('player_data_fetcher_main')
    asyncio.run(player_data_fetcher_main.main())
```

**New Flow:**
```python
def main(argv: list[str] | None = None) -> None:
    args = parser.parse_args(argv)

    # Create settings dictionary from parsed arguments
    settings_dict = create_settings_dict(args)

    # Import player-data-fetcher module (normal import, not importlib)
    sys.path.insert(0, str(Path(__file__).parent / "player-data-fetcher"))
    from player_data_fetcher_main import main as fetcher_main

    # Run main with settings dictionary
    asyncio.run(fetcher_main(settings_dict))
```

**Key Changes:**
- No config import
- No config override
- Create settings_dict from args
- Pass settings_dict to main()
- Normal import instead of importlib.import_module()

**Source:** Derived from R1 and R2 requirements

---

## Dependencies

### Internal Dependencies

**1. player-data-fetcher/player_data_fetcher_main.py**
- **Status:** EXISTS (615+ lines)
- **Used by:** run_player_fetcher.py (imports and calls main())
- **Modifications Required:** Change main() signature, remove config constant usage
- **Source:** Research - player_data_fetcher_main.py documented

**2. player-data-fetcher/config.py**
- **Status:** EXISTS (90 lines with 23 constants)
- **Current Role:** Provides module-level constants read by Settings class
- **Future Role:** TBD (see checklist.md Question 1 - keep/modify/remove)
- **Source:** Research - config.py constants documented

**3. utils/LoggingManager.py**
- **Status:** EXISTS (verified in Feature 01 research)
- **Used by:** player_data_fetcher_main.py (setup_logger function)
- **Modifications Required:** None (already accepts parameters)
- **Source:** Feature 01 research

**4. tests/test_run_player_fetcher.py**
- **Status:** EXISTS (12 tests for Feature 01)
- **Used for:** Testing argument parsing and CLI functionality
- **Modifications Required:** May need updates if import changes affect test mocking
- **Dependency:** All 12 tests must continue passing after refactoring
- **Source:** Feature 01 implementation (tests created in S6)

**5. tests/run_all_tests.py**
- **Status:** EXISTS (verified - runs all 2518 tests)
- **Used for:** Validating no regressions introduced by refactoring
- **Requirement:** Must show 2518/2518 passing after refactoring (R5)
- **Source:** Feature 01 completion status (2518/2518 tests passing)

---

### External Dependencies

**1. argparse** (Python stdlib)
- **Status:** Available in Python 3.x
- **Used by:** run_player_fetcher.py (existing - no changes)
- **Source:** Standard library

**2. pydantic** (third-party)
- **Status:** Already in use (Settings class inherits from BaseSettings)
- **Used by:** player_data_fetcher_main.py Settings class
- **Modifications:** May use model_validate() method (see checklist.md Question 2)
- **Source:** Research - Settings class uses pydantic

**3. asyncio** (Python stdlib)
- **Status:** Available in Python 3.x
- **Used by:** run_player_fetcher.py (asyncio.run() call - no changes)
- **Source:** Standard library

---

### Feature Dependencies

**Depends on:**
- **Feature 01 (player_fetcher)** - COMPLETE through S7
  - Reason: Refactoring Feature 01's implementation
  - Requirement: Must be production-ready before refactoring
  - Status: ✅ Complete (2518/2518 tests passing, zero tech debt)
  - Source: Feature 01 README.md Agent Status

**Blocks:**
- **None** - This is an architectural improvement to existing code
- Features 02-09 can proceed independently with constructor pattern
- Feature 10 refactors Feature 01 to match their pattern

**Benefits from:**
- **Feature 01 lessons learned** (../feature_01_player_fetcher/lessons_learned.md)
  - Understanding current implementation
  - Test coverage details
  - Known issues (none - zero tech debt)
- **S8.P1 alignment analysis** (../feature_02_schedule_fetcher/S8_P1_ALIGNMENT_ANALYSIS.md)
  - Pattern comparison documentation
  - User decision rationale

**Backward Compatibility Considerations:**
- Must check if any other code imports from player-data-fetcher/config.py
- If yes, need to maintain config.py (see checklist.md Question 4)
- If no, can remove/modify freely

**Source:** Feature 10 README.md "Dependencies" section

---

## Acceptance Criteria

**Will be defined in S2.P3 Phase after checklist questions are resolved.**

---

**Specification Status:** S2 IN PROGRESS (Research Phase starting)
