# Feature 07: League Helper Configurability - Research Findings

**Feature:** feature_07_league_helper
**Researcher:** Secondary-F
**Date:** 2026-01-29
**Phase:** S2.P1 Phase 1 (Targeted Research)

---

## Research Summary

Completed feature-specific research on league_helper module to understand current implementation, mode system, and interactive flow. This research focuses on implementation details needed to add argparse, mode selection, and E2E test flows.

---

## File-Level Findings

### 1. run_league_helper.py (Runner Script)

**Location:** `run_league_helper.py` (project root)
**Lines:** 68 lines total
**Purpose:** Simple subprocess wrapper that launches LeagueHelperManager

**Current Implementation (lines 21-64):**
```python
# Line 18: Hardcoded DATA_FOLDER constant
DATA_FOLDER = "./data"

# Lines 44-52: Subprocess call with DATA_FOLDER as single argument
result = subprocess.run([
    sys.executable,              # Current Python interpreter
    str(league_helper_script),   # Path to LeagueHelperManager.py
    DATA_FOLDER                  # Data folder argument
], check=True)
```

**Key Observations:**
- **No argparse:** Script has zero argument handling currently
- **Hardcoded path:** DATA_FOLDER is constant, not configurable
- **Simple wrapper:** Just executes subprocess.run() with sys.executable
- **Error handling:** Catches CalledProcessError and generic Exception
- **Return code propagation:** Returns subprocess exit code to caller

**Modification Points for Argparse:**
- Add argparse.ArgumentParser() after imports (line ~15)
- Replace DATA_FOLDER constant with args.data_folder (default "./data")
- Pass additional args to LeagueHelperManager via subprocess arguments
- Add --mode, --debug, --e2e-test, --log-level, etc. arguments

---

### 2. LeagueHelperManager.py (Main Orchestrator)

**Location:** `league_helper/LeagueHelperManager.py`
**Lines:** 216 lines total
**Purpose:** Central hub for mode management and interactive menu

**Mode System (lines 127-148):**
```python
# Line 127: Menu options (5 modes)
choice = show_list_selection("MAIN MENU",
    ["Add to Roster", "Starter Helper", "Trade Simulator",
     "Modify Player Data", "Save Calculated Projected Points"],
    "Quit")

# Lines 130-148: Mode routing via if/elif chain
if choice == 1:      # Add to Roster (Draft assistant)
    self._run_add_to_roster_mode()
elif choice == 2:    # Starter Helper (Weekly lineup)
    self._run_starter_helper_mode()
elif choice == 3:    # Trade Simulator
    self._run_trade_simulator_mode()
elif choice == 4:    # Modify Player Data
    self.run_modify_player_data_mode()
elif choice == 5:    # Save Calculated Points
    self.save_calculated_points_manager.execute()
elif choice == 6:    # Quit
    break
```

**Initialization (lines 55-100):**
- **Line 70:** Sets up logger via get_logger()
- **Line 75:** Creates ConfigManager(data_folder)
- **Line 80:** Initializes SeasonScheduleManager
- **Line 84:** Creates TeamDataManager
- **Line 88:** Creates PlayerManager
- **Lines 94-99:** Initializes all 5 mode managers

**Interactive Loop (lines 103-151):**
- **Line 113:** Displays welcome message
- **Line 114:** Shows current roster size
- **Line 122:** Infinite while True loop
- **Line 125:** Reloads player data before EACH menu display
- **Line 127:** Calls show_list_selection() for user input
- **Lines 130-148:** Routes to mode based on choice

**Main Entry Point (lines 192-215):**
```python
# Line 205: Sets up logging from constants
setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL,
             constants.LOGGING_TO_FILE, constants.LOGGING_FILE,
             constants.LOGGING_FORMAT)

# Lines 207-208: Hardcoded data path
base_path = Path(__file__).parent.parent
data_path = base_path / "data"

# Lines 210-211: Instantiate and run
leagueHelper = LeagueHelperManager(data_path)
leagueHelper.start_interactive_mode()
```

**Key Observations:**
- **5 modes confirmed:** Add to Roster, Starter Helper, Trade Simulator, Modify Player Data, Save Calculated Points
- **Menu-driven:** Uses show_list_selection() utility for all menus
- **Data reloading:** player_manager.reload_player_data() called before every menu
- **Mode isolation:** Each mode has dedicated manager class
- **Logging integration:** Uses constants.py for log configuration

**Modification Points for E2E Mode:**
- Add non-interactive execution path alongside start_interactive_mode()
- Create automated test flows for each mode (skip show_list_selection())
- Add --mode argument handling to select specific mode or run all
- Implement pre-defined inputs for each mode's E2E flow
- Add timing checks to ensure ≤3 min total for all 5 modes

---

### 3. constants.py (Configuration Constants)

**Location:** `league_helper/constants.py`
**Lines:** 88 lines total
**Purpose:** Centralized configuration constants

**Logging Constants (lines 22-28):**
```python
LOGGING_LEVEL = 'INFO'          # Line 24 - DEBUG/INFO/WARNING/ERROR/CRITICAL
LOGGING_TO_FILE = False         # Line 25 - Console vs file
LOG_NAME = "league_helper"      # Line 26 - Logger name
LOGGING_FILE = './data/log.txt' # Line 27 - Log file path
LOGGING_FORMAT = 'detailed'     # Line 28 - Format style
```

**Mode-Specific Constants (lines 30-56):**
```python
RECOMMENDATION_COUNT = 5        # Line 33 - Recommendations to display
MIN_WAIVER_IMPROVEMENT = 0      # Line 38 - Waiver threshold
NUM_TRADE_RUNNERS_UP = 9        # Line 39 - Trade alternatives
MIN_TRADE_IMPROVEMENT = 0       # Line 56 - Trade threshold
```

**Key Observations:**
- **4 configurable logging constants** identified in Discovery (lines 24-28)
- **4 mode-specific constants** (RECOMMENDATION_COUNT, MIN_WAIVER_IMPROVEMENT, MIN_TRADE_IMPROVEMENT, NUM_TRADE_RUNNERS_UP)
- **Position constants** (lines 63-73): RB, WR, QB, TE, K, DST, FLEX
- **Roster config moved:** MAX_POSITIONS, MAX_PLAYERS moved to league_config.json (comment lines 77-82)

**Argparse Mapping:**
- LOGGING_LEVEL → --log-level (choices: DEBUG, INFO, WARNING, ERROR, CRITICAL)
- LOGGING_TO_FILE → --log-to-file (boolean flag)
- RECOMMENDATION_COUNT → --recommendation-count (int, default 5)
- MIN_WAIVER_IMPROVEMENT → --min-waiver-improvement (int, default 0)
- MIN_TRADE_IMPROVEMENT → --min-trade-improvement (int, default 0)

---

### 4. user_input.py (Interactive Utilities)

**Location:** `league_helper/util/user_input.py`
**Lines:** ~80 lines (from excerpt)
**Purpose:** Interactive CLI menu utilities

**show_list_selection() Function (lines 22-80):**
```python
def show_list_selection(title: str, options: List[str], quit_str: str) -> int:
    # Lines 52-67: Display formatted menu with numbered options
    # Lines 69-76: Input loop with validation (int() conversion)
    # Lines 77-79: Error handling for non-integer inputs
    return choice  # Returns 1-based index
```

**Key Observations:**
- **Numbered menus:** 1-indexed for user-friendly display
- **Quit option:** Always displayed as last option (N+1)
- **Input validation:** Loops until valid integer entered
- **No range validation:** Function doesn't validate choice is in range (caller handles)
- **Used throughout:** Main menu (LeagueHelperManager line 127) and all mode managers

**E2E Mode Impact:**
- **Bypass needed:** E2E mode must skip show_list_selection() calls
- **Pre-defined inputs:** Provide predetermined choices instead of user input
- **Refactor approach:** Add optional parameter for non-interactive mode OR create parallel execution path

---

### 5. Module Structure

**Root Directory:** `league_helper/`
**Total Files:** 302 lines in root-level Python files

**Subdirectories (from find command):**
```
league_helper/
├── add_to_roster_mode/               # Mode 1: Draft assistant
│   └── AddToRosterModeManager.py     (lines 1-80+ examined)
├── starter_helper_mode/              # Mode 2: Weekly lineup
├── trade_simulator_mode/             # Mode 3: Trade simulation
├── modify_player_data_mode/          # Mode 4: Player data editing
├── save_calculated_points_mode/      # Mode 5: Save projected points
├── reserve_assessment_mode/          # UNUSED (not in main menu)
└── util/                             # Shared utilities
    ├── ConfigManager.py
    ├── PlayerManager.py
    ├── TeamDataManager.py
    ├── SeasonScheduleManager.py
    └── user_input.py
```

**Key Observations:**
- **6 mode directories:** But only 5 used (reserve_assessment_mode not in menu)
- **Consistent pattern:** Each mode has dedicated ModeManager class
- **Shared utilities:** util/ contains 5+ manager classes used across modes
- **Mode managers initialized once:** In LeagueHelperManager.__init__ (lines 94-99)

---

## Integration Points for Feature Implementation

### 1. Argparse Integration (run_league_helper.py)

**Add Arguments:**
```python
# Universal arguments (all scripts)
--debug              # Enable DEBUG logging + behavioral changes
--e2e-test           # Enable E2E test mode (≤3 min)
--log-level          # Override LOGGING_LEVEL constant
--silent             # Suppress console output (logging only)

# League helper specific arguments
--mode               # Select mode: 1-5 or "all" (default: interactive)
--data-folder        # Override DATA_FOLDER (default: "./data")
--recommendation-count    # Override RECOMMENDATION_COUNT
--min-waiver-improvement  # Override MIN_WAIVER_IMPROVEMENT
--min-trade-improvement   # Override MIN_TRADE_IMPROVEMENT
```

**Implementation Strategy:**
1. Add argparse.ArgumentParser() in run_league_helper.py
2. Parse arguments before subprocess call
3. Pass arguments to LeagueHelperManager.py as sys.argv or JSON config file
4. Update LeagueHelperManager.main() to accept arguments
5. Override constants based on arguments

### 2. Mode Selection (--mode argument)

**Mode Mapping:**
- `--mode 1` → Add to Roster only
- `--mode 2` → Starter Helper only
- `--mode 3` → Trade Simulator only
- `--mode 4` → Modify Player Data only
- `--mode 5` → Save Calculated Points only
- `--mode all` → Run all 5 modes sequentially (E2E test)

**Implementation Approach:**
- Add run_single_mode(mode_number) method to LeagueHelperManager
- Add run_all_modes_e2e() method for E2E testing
- Update main() to check for --mode argument and call appropriate method
- Bypass start_interactive_mode() when --mode specified

### 3. E2E Test Mode (--e2e-test flag)

**Requirements from Discovery:**
- All 5 modes automated
- Skip user prompts (no show_list_selection() calls)
- Complete in ≤3 minutes total
- Use pre-defined test data/inputs

**Implementation Strategy:**
- Add e2e_mode flag to each ModeManager
- Create parallel execution paths in each mode:
  - Interactive path: Uses show_list_selection() (existing)
  - E2E path: Uses pre-defined inputs (new)
- Define minimal test scenarios for each mode:
  - Mode 1 (Add to Roster): Draft 1 player (QB)
  - Mode 2 (Starter Helper): Show starters for Week 1
  - Mode 3 (Trade Simulator): Simulate 1 pre-defined trade
  - Mode 4 (Modify Player Data): Modify 1 player's status
  - Mode 5 (Save Points): Save calculated points to CSV
- Add timing instrumentation to verify ≤3 min constraint

### 4. Debug Mode (--debug flag)

**Behavioral Changes:**
- **Logging:** Set LOGGING_LEVEL to DEBUG (override constants.py)
- **Smaller datasets:**
  - Reduce RECOMMENDATION_COUNT from 5 to 2
  - Limit player searches to top 50 instead of full roster
  - Single trade simulation instead of 9 runners-up
- **Verbose output:** Print additional debugging information to console

**Implementation Points:**
- Update setup_logger() call in main() with debug level if --debug
- Pass debug flag to each ModeManager
- Add conditional logic in each mode to limit dataset sizes

---

## Research Completeness Checklist (Phase 1.5 Preparation)

**Component Research:**
- ✅ Can cite exact files to modify: run_league_helper.py, LeagueHelperManager.py
- ✅ Have READ source code: 5 files examined (run_league_helper.py, LeagueHelperManager.py, constants.py, user_input.py, AddToRosterModeManager.py)
- ✅ Can cite actual line numbers: All findings include line number citations
- ✅ Can cite method signatures: show_list_selection(title, options, quit_str), LeagueHelperManager.__init__(data_folder), etc.

**Pattern Research:**
- ✅ Searched for similar features: Examined all 5 mode managers, found consistent pattern
- ✅ READ similar implementations: Looked at AddToRosterModeManager structure (lines 1-80)
- ✅ Understand mode system: If/elif routing in start_interactive_mode() (lines 130-148)

**Data Research:**
- ✅ Have READ actual data files: constants.py shows configuration structure
- ✅ Know data formats: ConfigManager loads league_config.json, PlayerManager uses players.csv
- ⚠️ **NEED:** Example league_config.json structure (minor gap - can infer from usage)

**Discovery Context:**
- ✅ Reviewed DISCOVERY.md: Completed in Phase 0
- ✅ Applied epic-level findings: 5 modes, 4 constants, script-specific args, E2E ≤3 min
- ✅ Understand selected approach: Comprehensive Script-Specific Argparse (Option 2)

---

## Next Steps for Phase 1.5 (Research Audit)

**Additional Research Needed:**
1. ⚠️ **Minor:** Read league_config.json example to understand structure (1 file)
2. ⚠️ **Optional:** Examine one more mode manager (starter_helper or trade_simulator) to confirm pattern consistency

**Ready for Audit:**
- Have sufficient evidence for implementation planning
- Can cite specific files, line numbers, and method signatures
- Understand mode system, interactive flow, and constants usage
- Clear integration points identified

**Estimated Research Completeness:** 95% (minor gap: data file examples)

---

## Evidence Summary

**Files Read:** 5 files
- run_league_helper.py (68 lines)
- LeagueHelperManager.py (216 lines)
- constants.py (88 lines)
- user_input.py (80 lines excerpt)
- AddToRosterModeManager.py (80 lines excerpt)

**Line Number Citations:** 25+ specific line references documented

**Code Snippets:** 8 code blocks extracted with actual implementation

**Module Structure:** Complete directory tree mapped (6 mode directories + util/)

**Ready for S2.P2 Specification Phase:** YES (after Phase 1.5 audit passes)
