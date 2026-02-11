# Feature Specification: win_rate_sim_logging

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 05
**Created:** 2026-02-06
**Last Updated:** 2026-02-06

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 5: win_rate_sim_logging**

**Purpose:** CLI integration and log quality improvements for win rate simulation script

**Scope:**
- Add --enable-log-file flag to run_win_rate_simulation.py (direct entry)
- Replace hardcoded LOGGING_TO_FILE constant with CLI flag
- Apply DEBUG/INFO quality criteria to simulation/win_rate/ modules
- Review shared simulation utilities: ResultsManager, ConfigGenerator
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

### Relevant Discovery Decisions

- **Solution Approach:** Direct entry script, replace hardcoded LOGGING_TO_FILE constant
- **Key Constraints:**
  - Must replace hardcoded constant with CLI flag
  - Must preserve existing script behavior when flag not provided
  - Log quality improvements must not break functionality
- **Implementation Order:** After Feature 1 (depends on LineBasedRotatingHandler)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q3: Log quality criteria | Agent to propose criteria | Must apply DEBUG (tracing) and INFO (user awareness) criteria |
| Q4: CLI flag default | File logging OFF by default | Replace LOGGING_TO_FILE constant with CLI flag (default False) |
| Q5: Script coverage | Just those 6 scripts | Confirms win_rate_sim in scope |
| Q6: Log quality scope | System-wide (Option B) | Affects simulation/win_rate/ AND shared simulation utilities |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 1 identified hardcoded LOGGING_TO_FILE constant that needs replacement
- **Based on User Answer:** Q4 (OFF by default) replaces hardcoded constant with CLI flag defaulting to False
- **Based on Finding:** Iteration 3 proposed DEBUG/INFO criteria that guide log quality improvements

---

## Feature Overview

**What:** Add CLI flag control for file logging and improve log quality in win rate simulation modules

**Why:** Enables users to control file logging for simulations, improves debugging and runtime awareness

**Who:** Users running win rate simulation to optimize parameters

---

## Functional Requirements

**Source:** Epic requirement + Discovery Phase + RESEARCH_NOTES.md

### Requirement 1: CLI Flag Integration (Replace Hardcoded Constant)

**Source:** Epic requirement "CLI toggle for file logging" + Discovery Q4

**Description:**
Replace hardcoded `LOGGING_TO_FILE = False` constant in run_win_rate_simulation.py with --enable-log-file CLI argument. When flag is provided, file logging is enabled and logs are written to logs/win_rate_simulation/ folder using Feature 01's LineBasedRotatingHandler. When flag is omitted, file logging is disabled (default behavior).

**Acceptance Criteria:**
- ✅ Remove LOGGING_TO_FILE constant from run_win_rate_simulation.py (line 34)
- ✅ Add --enable-log-file argument to argparse parser
- ✅ Argument is action='store_true' (boolean flag, no value needed)
- ✅ Argument defaults to False (file logging OFF by default)
- ✅ Update setup_logger() call (line 117) to use args.enable_log_file parameter
- ✅ Pass log_to_file=args.enable_log_file to setup_logger()
- ✅ Logger name is consistent for folder structure (see checklist Q1)
- ✅ Existing script behavior preserved when flag not provided (console logging only)

**Example:**
```bash
# No flag → console logging only (current behavior)
python run_win_rate_simulation.py iterative --sims 100

# With flag → file logging enabled (new behavior)
python run_win_rate_simulation.py iterative --sims 100 --enable-log-file

# Result: logs/win_rate_simulation/win_rate_simulation-20260206_143522.log created
```

**Code Changes:**
```python
# Current code (run_win_rate_simulation.py lines 33-37):
LOGGING_LEVEL = 'INFO'
LOGGING_TO_FILE = False         # ❌ REMOVE THIS LINE
LOG_NAME = "simulation"         # ❓ May change based on Q1
LOGGING_FILE = './simulation/log.txt'  # No longer used (Feature 01 auto-generates)
LOGGING_FORMAT = 'standard'

# New code (add to argparse):
parser.add_argument(
    '--enable-log-file',
    action='store_true',
    default=False,
    help='Enable logging to file (default: console only)'
)

# Update setup_logger() call (line 117):
# OLD: setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
# NEW: setup_logger(LOG_NAME, LOGGING_LEVEL, args.enable_log_file, None, LOGGING_FORMAT)
```

**User Answer:** Q4 (file logging OFF by default)

---

### Requirement 2: Log Quality - DEBUG Level

**Source:** Discovery Iteration 3 DEBUG criteria

**Description:**
Audit and improve DEBUG-level logging calls across all simulation/win_rate/ modules to meet quality criteria. DEBUG logs should provide tracing details for debugging complex simulation flows without excessive noise.

**Acceptance Criteria:**
- ✅ Function entry/exit logs ONLY for complex flows (not every function)
- ✅ Data transformations log before/after values (e.g., "Config updated: old_value → new_value")
- ✅ Conditional branch logs show which path executed (e.g., "Using Process mode" vs "Using Thread mode")
- ❌ NOT every variable assignment (avoid spam)
- ❌ NOT logging inside tight loops without throttling (performance impact)
- ✅ All 69 DEBUG calls audited using systematic review

**Modules in Scope:**
- SimulationManager.py (9 DEBUG calls)
- ParallelLeagueRunner.py (16 DEBUG calls)
- SimulatedLeague.py (27 DEBUG calls)
- DraftHelperTeam.py (6 DEBUG calls)
- SimulatedOpponent.py (5 DEBUG calls)
- Week.py (6 DEBUG calls)
- manual_simulation.py (0 DEBUG calls)

**Example Current Code (from RESEARCH_NOTES):**
```python
# ✅ GOOD: Iteration details
self.logger.debug(f"Season {season_idx + 1}/{total_seasons}: {season_name}")

# ✅ GOOD: Data validation
self.logger.debug(f"Season {season_folder.name}: {valid_count} valid players - OK")

# Audit needed to verify all calls meet criteria
```

**Review Process:**
- **Comprehensive manual audit** (all 69 calls reviewed individually)
- Systematic file-by-file audit (7 files)
- Categorize each DEBUG call: KEEP, IMPROVE, REMOVE
- Document violations found in implementation checklist
- Fix all violations before commit

**User Decision:** Q1 Answer - Option A (Comprehensive Manual Audit) - Review all 69 calls for complete quality assurance

---

### Requirement 3: Log Quality - INFO Level

**Source:** Discovery Iteration 3 INFO criteria

**Description:**
Audit and improve INFO-level logging calls to meet quality criteria. INFO logs should provide user-facing awareness of script progress, major phases, and significant outcomes without implementation details.

**Acceptance Criteria:**
- ✅ Script start/complete logs with configuration summary
- ✅ Major phase transitions (e.g., "Starting full optimization", "Registering configurations")
- ✅ Significant outcomes (e.g., "Generated 46,656 configurations", "Win rate: 75%")
- ❌ NOT implementation details (move to DEBUG level)
- ❌ NOT every function call (only major phases)
- ✅ All 100 INFO calls audited using systematic review

**Example Current Code (from RESEARCH_NOTES):**
```python
# ✅ GOOD: Script start
self.logger.info("Initializing SimulationManager")

# ✅ GOOD: Major phase
self.logger.info(f"Generated {len(combinations)} parameter combinations")

# ✅ GOOD: Significant outcome
self.logger.info(f"Registered {len(combinations)} configurations")

# Audit needed to verify all calls meet criteria
```

**Review Process:**
- **Comprehensive manual audit** (all 100 calls reviewed individually)
- Same systematic file-by-file audit as DEBUG level
- Categorize each INFO call: KEEP, IMPROVE, REMOVE, DOWNGRADE_TO_DEBUG
- Ensure INFO logs remain user-friendly (avoid technical jargon)
- Fix all violations before commit

**User Decision:** Q1 Answer - Option A (Comprehensive Manual Audit) - Review all 100 calls for complete quality assurance

---

## Technical Requirements

**Source:** RESEARCH_NOTES.md (Code Locations and LoggingManager Integration sections)

### File Modifications

**File 1: run_win_rate_simulation.py**
- **Action:** Modify
- **Lines affected:** 34 (remove), 117 (update), argparse section (add flag)
- **Changes:**
  - Remove: `LOGGING_TO_FILE = False` constant
  - Add: --enable-log-file argument to parser (boolean, action='store_true', default=False)
  - Update: setup_logger() call to use args.enable_log_file
  - Update: LOG_NAME constant from "simulation" to "win_rate_simulation"

**Files 2-8: simulation/win_rate/*.py (7 modules)**
- **Action:** Audit and improve logging calls
- **Files:** SimulationManager.py, ParallelLeagueRunner.py, SimulatedLeague.py, DraftHelperTeam.py, SimulatedOpponent.py, Week.py, manual_simulation.py
- **Changes:** TBD based on audit findings (Requirements 2-3)
- **No structural changes** - only log message improvements

**File 9: tests/root_scripts/test_root_scripts.py**
- **Action:** Modify
- **Lines affected:** Assertion for LOGGING_TO_FILE constant
- **Changes:** Remove assertion `assert hasattr(run_win_rate_simulation, 'LOGGING_TO_FILE')`

### Logger Configuration

**Logger Name:** "win_rate_simulation" (changed from "simulation")
- LOG_NAME constant: "win_rate_simulation"
- Folder: logs/win_rate_simulation/
- Rationale: More specific, avoids conflicts with other simulation types

**Logger Setup:**
```python
# Entry script (run_win_rate_simulation.py):
# Update LOG_NAME constant (line 35):
LOG_NAME = "win_rate_simulation"  # Changed from "simulation"

# setup_logger call (line 117):
logger = setup_logger(
    name=LOG_NAME,                  # "win_rate_simulation"
    level=LOGGING_LEVEL,            # "INFO" (unchanged)
    log_to_file=args.enable_log_file,  # NEW: from CLI flag
    log_file_path=None,             # Feature 01 auto-generates
    log_format=LOGGING_FORMAT       # "standard" (unchanged)
)
```

**Internal Modules (no changes needed):**
```python
# simulation/win_rate/*.py files (unchanged):
from utils.LoggingManager import get_logger

class SomeClass:
    def __init__(self):
        self.logger = get_logger()  # Gets logger configured by entry script
```

### Integration with Feature 01

**Feature 01 Provides:**
- LineBasedRotatingHandler (500-line rotation)
- Modified setup_logger() function
- logs/{script_name}/ folder structure
- Timestamped log files

**This Feature Consumes:**
- setup_logger() API with log_to_file parameter
- Automatic log file path generation
- 500-line rotation (transparent to this feature)
- Max 50 files cleanup (transparent to this feature)

**Integration Contracts (from Feature 01 spec):**
1. **Logger name = folder name:** Use consistent name (Q1 determines this)
2. **log_file_path=None:** Don't specify custom paths
3. **log_to_file from CLI:** Wire --enable-log-file flag to log_to_file parameter

**Result when --enable-log-file provided:**
```
logs/
└── win_rate_simulation/
    ├── win_rate_simulation-20260206_143522.log  (500 lines)
    ├── win_rate_simulation-20260206_144015.log  (500 lines)
    └── ...  (max 50 files, oldest auto-deleted)
```

**User Decision:** Q2 Answer - Option B (Logger name "win_rate_simulation")

---

## Integration Points

### Integration with Feature 1 (Core Infrastructure)

**Direction:** This feature consumes FROM Feature 1

**What Feature 1 Provides:**
- LineBasedRotatingHandler class (custom logging handler)
- Modified setup_logger() function (integrates new handler)
- logs/{script_name}/ folder structure (auto-created)
- 500-line rotation logic (transparent)
- Max 50 files cleanup (transparent)

**Interface Contract:**

**Complete setup_logger() Signature (from Feature 01 actual implementation):**
```python
def setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    log_format: str = 'standard',
    enable_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # Backward compatibility (not used)
    backup_count: int = 5  # Backward compatibility (not used)
) -> logging.Logger
```

**Feature 05 Usage:**
```python
# This feature calls (run_win_rate_simulation.py):
from utils.LoggingManager import setup_logger

logger = setup_logger(
    name="win_rate_simulation",     # Logger name (folder name)
    level="INFO",                    # Log level
    log_to_file=args.enable_log_file,  # ← CLI flag controls this
    log_file_path=None,              # ← Must be None (auto-generated)
    log_format="standard"            # Format style
    # enable_console=True (default, can omit)
    # max_file_size, backup_count (optional, can omit)
)

# Feature 01's setup_logger() creates:
# - logs/win_rate_simulation/ folder (if doesn't exist)
# - Initial file: logs/win_rate_simulation/win_rate_simulation-{YYYYMMDD_HHMMSS}.log
# - Rotated files: logs/win_rate_simulation/win_rate_simulation-{YYYYMMDD_HHMMSS_microseconds}.log
# - LineBasedRotatingHandler with 500-line rotation
# - Max 50 files cleanup when rotation occurs
```

**Note:** Updated based on feature_01 actual implementation. Rotated files include microsecond precision.

**Dependencies:**
- Feature 01 MUST be implemented first (foundation)
- This feature cannot be tested until Feature 01 complete
- Integration contract violations will cause errors (see Error Handling)

---

### Integration with Internal Win Rate Modules

**Direction:** Entry script PROVIDES configured logger TO internal modules

**Flow:**
```
run_win_rate_simulation.py (entry script)
  ↓ calls setup_logger(log_to_file=args.enable_log_file)
  ↓ logger configured and stored in LoggingManager singleton
  ↓
simulation/win_rate/*.py (internal modules)
  ↓ call get_logger()
  ↓ receive configured logger from LoggingManager singleton
  ↓ use logger.debug/info/warning/error/critical
  ↓ logs written to file (if --enable-log-file) or console (if not)
```

**No Changes Required:**
- Internal modules already use `from utils.LoggingManager import get_logger`
- get_logger() returns the logger configured by entry script
- CLI flag only affects entry script, not internal modules

---

### Integration with Test Suite

**Direction:** This feature MODIFIES tests

**Affected Test:** tests/root_scripts/test_root_scripts.py

**Current Behavior:**
```python
# Test checks for LOGGING_TO_FILE constant:
assert hasattr(run_win_rate_simulation, 'LOGGING_TO_FILE')
```

**After This Feature:**
- LOGGING_TO_FILE constant removed
- Test assertion removed (no longer needed)

**Required Action:** Remove assertion line from test_root_scripts.py

**User Decision:** Q3 Answer - Option A (Remove assertion entirely)

---

## Error Handling

**Source:** Feature 01 error handling patterns + RESEARCH_NOTES.md

### Error Scenario 1: Missing --enable-log-file Flag (Not an Error)

**Trigger:** User runs script without --enable-log-file flag

**Handling:**
- argparse default: `action='store_true', default=False`
- args.enable_log_file = False
- setup_logger() called with log_to_file=False
- Logging goes to console only (existing behavior)

**User Impact:** None (expected behavior)

**Code:** No explicit handling needed (argparse provides default)

---

### Error Scenario 2: Feature 01 Not Implemented (Setup Error)

**Trigger:** This feature runs before Feature 01 implemented

**Handling:**
- setup_logger() tries to instantiate LineBasedRotatingHandler
- Import fails: `ModuleNotFoundError: No module named 'utils.LineBasedRotatingHandler'`
- Script exits with stack trace

**User Impact:** Script cannot run

**Mitigation:** Feature 01 MUST be implemented first (implementation order constraint)

**Code:** No handling needed (dependency order prevents this)

---

### Error Scenario 3: Permission Denied (Folder Creation)

**Trigger:** Script tries to create logs/ folder but lacks permissions

**Handling:**
- Feature 01's LineBasedRotatingHandler handles this
- OSError caught by logging.FileHandler.handleError()
- Error logged to stderr
- Logging continues to console (file logging fails gracefully)

**User Impact:** No file logs (console logging unaffected)

**Mitigation:** Feature 01 handles this (transparent to this feature)

---

### Error Scenario 4: Logger Name Contains Invalid Characters

**Trigger:** LOG_NAME constant contains path separators (e.g., "../evil")

**Handling:**
- Feature 01's LineBasedRotatingHandler sanitizes filename
- Folder created with normalized name
- Logging continues (with unexpected folder name)

**User Impact:** Folder name may differ from expected

**Mitigation:**
- Use simple alphanumeric logger names (e.g., "win_rate_simulation")
- Feature 01 spec documents this requirement (follows contract)

**Prevention:** "win_rate_simulation" is a valid, filesystem-safe name (alphanumeric + underscore)

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

---

## Non-Functional Requirements

**Maintainability:**
- Must follow project coding standards
- Must preserve existing win_rate_sim behavior

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Core infrastructure changes (Feature 1)
- Other scripts' CLI integration (Features 2-4, 6-7)
- Console logging changes (only file logging affected)

---

## User Decisions (All Resolved)

**All questions answered - spec updated with user decisions**

**Q1: Log Quality Audit Scope** ✅ RESOLVED
- **Answer:** Option A - Comprehensive Manual Audit
- **Decision:** Review all 197 logging calls individually for complete quality assurance
- **Impact:** Thorough audit ensures highest log quality, 2-3 hour implementation time

**Q2: Logger Name Selection** ✅ RESOLVED
- **Answer:** Option B - "win_rate_simulation"
- **Decision:** Change LOG_NAME constant to "win_rate_simulation"
- **Impact:** Folder path: logs/win_rate_simulation/, more specific naming, no conflicts

**Q3: Test Assertion Handling** ✅ RESOLVED
- **Answer:** Option A - Remove assertion entirely
- **Decision:** Remove `assert hasattr(run_win_rate_simulation, 'LOGGING_TO_FILE')` from test_root_scripts.py
- **Impact:** One less assertion, constant check not valuable

---

## Open Questions (None Remaining)

**Q1: Logger Name** - Should logger name be "win_rate_simulation" or "simulation"?
- Current: "simulation" (LOG_NAME constant line 35)
- Impact: Becomes folder name (logs/{name}/)
- Options:
  - A) Keep "simulation" → logs/simulation/ (may conflict with other sim types)
  - B) Change to "win_rate_simulation" → logs/win_rate_simulation/ (more specific)
- **Status:** OPEN (user decision needed)

**Q2: Test Assertion Handling** - How to handle failing test in test_root_scripts.py?
- Current assertion: `assert hasattr(run_win_rate_simulation, 'LOGGING_TO_FILE')`
- This will FAIL after removing constant
- Options:
  - A) Remove assertion entirely (constant check not valuable)
  - B) Update to check for argparse --enable-log-file flag
  - C) Keep constant as deprecated (backward compatibility)
- **Status:** OPEN (user decision needed)

**Q3: Log Quality Audit Scope** - How thorough should the audit be?
- 197 logging calls across 7 files
- Options:
  - A) Audit all 197 calls manually (2-3 hours, comprehensive)
  - B) Spot-check ~20% (30-40 calls), document patterns (30-45 min)
  - C) Fix only obvious violations found during implementation (fastest)
- **Status:** OPEN (user decision needed)

---

## Implementation Notes

**Design Decisions from Discovery:**
- Replace LOGGING_TO_FILE constant with argparse --enable-log-file flag
- CLI flag defaults to False (file logging OFF by default) per Q4 answer
- Entry script calls setup_logger(), internal modules call get_logger() (established pattern)
- No changes needed to internal modules for CLI integration (only entry script)

**Implementation Tips:**

**CLI Flag Addition:**
- Add to main parser (not subparsers) for availability across all modes
- Use `action='store_true'` (no value needed, presence = True)
- Default=False ensures backward compatibility
- Help text: "Enable logging to file (default: console only)"

**setup_logger() Call:**
- Replace LOGGING_TO_FILE constant with args.enable_log_file
- Set log_file_path=None (Feature 01 auto-generates path)
- Remove old LOGGING_FILE constant reference (no longer used)

**Logger Name Decision:**
- Follow Feature 01 contract: logger name becomes folder name
- Chosen: "win_rate_simulation" (specific, avoids conflicts)
- Update LOG_NAME constant from "simulation" to "win_rate_simulation"

**Log Quality Audit:**
- Comprehensive manual audit (all 197 calls reviewed)
- Use systematic file-by-file review (not ad-hoc)
- Categorize each call: KEEP, IMPROVE, REMOVE, DOWNGRADE
- Apply Discovery Phase criteria consistently
- Document violations found in implementation checklist
- Time estimate: 2-3 hours for thorough review

**Test Updates:**
- Remove test_root_scripts.py assertion for LOGGING_TO_FILE constant
- Run full test suite after changes (verify no breakage)
- Update test assertions if log messages changed during audit

**Gotchas:**

**Gotcha 1: argparse Scope**
- --enable-log-file must be on main parser (not subparser)
- Ensures flag works for all modes (single, full, iterative)
- Test each mode after implementation

**Gotcha 2: Logger Name Consistency**
- LOG_NAME constant used for logger name
- If changing from "simulation" to "win_rate_simulation", update constant
- Folder name will change (logs/win_rate_simulation/)

**Gotcha 3: Test Failures**
- test_root_scripts.py will fail if LOGGING_TO_FILE assertion not removed
- Remove the assertion: `assert hasattr(run_win_rate_simulation, 'LOGGING_TO_FILE')`
- Verify test updates before committing

**Gotcha 4: Log Quality Subjectivity**
- DEBUG/INFO criteria have some subjective interpretation
- When in doubt, keep existing logs (avoid breaking changes)
- Document rationale for any removed logs

**Gotcha 5: Shared Utilities Overlap**
- simulation/shared/ utilities used by both accuracy_sim and win_rate_sim
- Feature 4 may also modify these utilities
- Coordinate during S8.P1 to avoid conflicts

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent (Primary) | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
| 2026-02-06 | Agent (Secondary-D) | Complete spec draft with all requirements, technical details, integration points, error handling, open questions | S2.P1.I1 (Feature-Level Discovery complete) |
| 2026-02-06 | Agent (Secondary-D) | Updated spec with user decisions: comprehensive audit, "win_rate_simulation" logger name, remove test assertion | S2.P1.I2 (Checklist Resolution complete) |
| 2026-02-08 12:15 | Agent | Updated setup_logger() signature, type hints, return type, filename formats based on Feature 01 actual implementation | S8.P1 (Cross-Feature Alignment - Feature 01 complete) |
