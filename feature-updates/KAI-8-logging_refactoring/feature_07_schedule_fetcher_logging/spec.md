# Feature Specification: schedule_fetcher_logging

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 07
**Created:** 2026-02-06
**Last Updated:** 2026-02-06 (S2.P1.I1 - Draft complete)

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 7: schedule_fetcher_logging**

**Purpose:** CLI integration and log quality improvements for schedule fetcher script

**Scope:**
- Add --enable-log-file flag to run_schedule_fetcher.py (async main)
- Apply DEBUG/INFO criteria to schedule-data-fetcher/ modules logs
- Review and improve logs in ScheduleFetcher and related modules
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

### Relevant Discovery Decisions

- **Solution Approach:** Async main entry point
- **Key Constraints:**
  - Must work with async entry point
  - Must preserve existing script behavior when flag not provided
  - Log quality improvements must not break functionality
- **Implementation Order:** After Feature 1 (depends on LineBasedRotatingHandler)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q3: Log quality criteria | Agent to propose criteria | Must apply DEBUG (tracing) and INFO (user awareness) criteria |
| Q4: CLI flag default | File logging OFF by default | Flag must explicitly enable file logging |
| Q5: Script coverage | Just those 6 scripts | Confirms schedule_fetcher in scope |
| Q6: Log quality scope | System-wide (Option B) | Affects schedule-data-fetcher/ modules |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 1 identified run_schedule_fetcher.py as async main script
- **Based on Finding:** Iteration 3 proposed DEBUG/INFO criteria that guide log quality improvements
- **Based on User Answer:** Q5 explicitly includes schedule-data-fetcher in scope

---

## Feature Overview

**What:** Add CLI flag control for file logging and improve log quality in schedule fetcher modules

**Why:** Enables users to control file logging for schedule fetching, improves debugging and runtime awareness

**Who:** Users running schedule fetcher to collect NFL schedule data

---

## Functional Requirements

**Source:** RESEARCH_NOTES.md + Feature 01 spec.md

### Requirement 1: CLI Flag Integration (Async Main)

**Source:** Epic requirement "CLI toggle for file logging" + Discovery Q4

**Description:**
Add `--enable-log-file` CLI flag to `run_schedule_fetcher.py` to control file logging. When flag is provided, logs are written to `logs/schedule_fetcher/schedule_fetcher-{timestamp}.log` with 500-line rotation. When flag is omitted, logs are written to console only (stderr). Script must work with async main entry point.

**Acceptance Criteria:**
- ✅ Add argparse setup to run_schedule_fetcher.py main() function
- ✅ Flag name: `--enable-log-file` (consistent with other features)
- ✅ Flag type: action='store_true' (boolean flag, no argument)
- ✅ Flag default: False (file logging OFF by default per Q4)
- ✅ Flag help text: "Enable logging to file (default: console only)"
- ✅ Call setup_logger() in main() before instantiating ScheduleFetcher
- ✅ Logger name: "schedule_fetcher" (lowercase with underscore, per naming convention)
- ✅ Pass log_to_file=args.enable_log_file to setup_logger()
- ✅ Pass log_file_path=None to setup_logger() (let LoggingManager generate path)
- ✅ Pass enable_log_file=args.enable_log_file to ScheduleFetcher constructor
- ✅ Works with asyncio.run(main()) pattern (no async/await conflicts with argparse)

**Example:**
```python
# Before (run_schedule_fetcher.py lines 28-59):
async def main():
    """Main entry point for schedule fetcher."""
    try:
        output_path = Path(__file__).parent / "data" / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)
        print(f"Fetching NFL season schedule for {NFL_SEASON}...")
        # ... rest of logic ...

# After:
import argparse
from utils.LoggingManager import setup_logger

async def main():
    """Main entry point for schedule fetcher."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Fetch NFL season schedule from ESPN API")
    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        help='Enable logging to file (default: console only)'
    )
    args = parser.parse_args()

    # Setup logger
    logger = setup_logger(
        name="schedule_fetcher",
        level="INFO",
        log_to_file=args.enable_log_file,
        log_file_path=None,
        log_format="standard"
    )

    try:
        output_path = Path(__file__).parent / "data" / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path, enable_log_file=args.enable_log_file)
        logger.info(f"Fetching NFL season schedule for {NFL_SEASON}...")
        # ... rest of logic ...
```

**Usage Examples:**
```bash
# Console logging only (default):
python run_schedule_fetcher.py

# File logging enabled:
python run_schedule_fetcher.py --enable-log-file
# Logs to: logs/schedule_fetcher/schedule_fetcher-20260206_143522.log
```

**User Answer:** Discovery Q4 (file logging OFF by default)

---

### Requirement 2: Logger Name Consistency

**Source:** Feature 01 integration contract + RESEARCH_NOTES.md

**Description:**
Update logger name from "ScheduleFetcher" (PascalCase) to "schedule_fetcher" (snake_case) to follow project naming conventions and ensure consistent folder naming in logs/ directory.

**Acceptance Criteria:**
- ✅ Update ScheduleFetcher.__init__() line 35: setup_logger(name="schedule_fetcher")
- ✅ Logger name matches folder name convention (snake_case)
- ✅ Folder created: logs/schedule_fetcher/ (not logs/ScheduleFetcher/)
- ✅ Filenames use snake_case: schedule_fetcher-{timestamp}.log
- ✅ No mixed-case logger names in codebase

**Example:**
```python
# Before (ScheduleFetcher.py line 35):
self.logger = setup_logger(name="ScheduleFetcher", level="INFO")

# After:
self.logger = setup_logger(
    name="schedule_fetcher",
    level="INFO",
    log_to_file=enable_log_file,
    log_file_path=None,
    log_format="standard"
)
```

**User Answer:** Feature 01 integration contract (logger name = folder name)

---

### Requirement 3: ScheduleFetcher Parameter Addition

**Source:** Epic requirement "CLI toggle per script" + RESEARCH_NOTES.md

**Description:**
Add `enable_log_file` parameter to ScheduleFetcher.__init__() to accept CLI flag value and pass it to setup_logger(). Default to False for backward compatibility with existing callers.

**Acceptance Criteria:**
- ✅ Add enable_log_file parameter to __init__() signature (line 27)
- ✅ Parameter type: bool
- ✅ Parameter default: False (backward compatibility)
- ✅ Pass enable_log_file to setup_logger(log_to_file=enable_log_file)
- ✅ Add log_file_path=None parameter to setup_logger() call
- ✅ Add log_format="standard" parameter to setup_logger() call
- ✅ Update docstring with new parameter description

**Example:**
```python
# Before (ScheduleFetcher.py lines 27-36):
def __init__(self, output_path: Path):
    """
    Initialize the ScheduleFetcher.

    Args:
        output_path: Path where season_schedule.csv will be written
    """
    self.output_path = output_path
    self.logger = setup_logger(name="ScheduleFetcher", level="INFO")
    self.client: Optional[httpx.AsyncClient] = None

# After:
def __init__(self, output_path: Path, enable_log_file: bool = False):
    """
    Initialize the ScheduleFetcher.

    Args:
        output_path: Path where season_schedule.csv will be written
        enable_log_file: Enable logging to file (default: False)
    """
    self.output_path = output_path
    self.logger = setup_logger(
        name="schedule_fetcher",
        level="INFO",
        log_to_file=enable_log_file,
        log_file_path=None,
        log_format="standard"
    )
    self.client: Optional[httpx.AsyncClient] = None
```

**User Answer:** Epic requirement (CLI control per script)

---

### Requirement 4: Replace Print Statements with Logger Calls

**Source:** Epic requirement "improved logging" + RESEARCH_NOTES.md

**Description:**
Replace print() statements in run_schedule_fetcher.py with logger calls (info/error) to provide consistent logging output and enable file logging control via CLI flag.

**Acceptance Criteria:**
- ✅ Replace line 37: print(f"Fetching...") → logger.info(f"Fetching...")
- ✅ Replace line 43: print("ERROR:...") → logger.error("Failed to fetch...")
- ✅ Replace lines 49-51: print(f"✓ Schedule...") → logger.info(f"Schedule successfully exported...")
- ✅ Replace line 56: print(f"ERROR:...") → logger.error(f"Unhandled error: {e}")
- ✅ No print() statements remain in main() function
- ✅ Console output behavior unchanged when --enable-log-file not provided
- ✅ File logging captures all output when --enable-log-file provided

**Example:**
```python
# Before (run_schedule_fetcher.py):
print(f"Fetching NFL season schedule for {NFL_SEASON}...")

if not schedule:
    print("ERROR: Failed to fetch schedule data")
    return 1

print(f"✓ Schedule successfully exported to {output_path}")
print(f"  - Weeks: {len(schedule)}")
print(f"  - Season: {NFL_SEASON}")

# After:
logger.info(f"Fetching NFL season schedule for {NFL_SEASON}...")

if not schedule:
    logger.error("Failed to fetch schedule data")
    return 1

logger.info(f"Schedule successfully exported to {output_path}")
logger.info(f"  Weeks: {len(schedule)}, Season: {NFL_SEASON}")
```

**User Answer:** Epic requirement (improved logging infrastructure)

---

### Requirement 5: Log Quality - DEBUG Level

**Source:** Discovery Iteration 3 (log quality criteria) + RESEARCH_NOTES.md

**Description:**
Review existing DEBUG-level logs in ScheduleFetcher.py and ensure they meet discovery criteria: function entry/exit with parameters (complex flows only), data transformations, conditional branches. Current DEBUG logs already meet criteria - no changes required.

**Acceptance Criteria:**
- ✅ Line 94: "Fetching schedule for week {week}/18" - Progress tracking (KEEP)
- ✅ Line 138: "Error parsing event in week {week}: {e}" - Error detail (KEEP)
- ✅ No excessive DEBUG logs (e.g., every variable assignment)
- ✅ No DEBUG logs inside tight loops without throttling
- ✅ DEBUG logs provide useful debugging information
- ✅ No functionality changes (log review only)

**Current DEBUG Logs (All Good ✅):**
```python
# Line 94 - Progress tracking (appropriate for async loop):
self.logger.debug(f"Fetching schedule for week {week}/18")

# Line 138 - Error detail for debugging:
self.logger.debug(f"Error parsing event in week {week}: {e}")
```

**Assessment:** Current DEBUG logs meet criteria. No changes needed.

**User Answer:** Discovery Iteration 3 (DEBUG criteria)

---

### Requirement 6: Log Quality - INFO Level

**Source:** Discovery Iteration 3 (log quality criteria) + RESEARCH_NOTES.md

**Description:**
Review existing INFO-level logs in ScheduleFetcher.py and ensure they meet discovery criteria: script start/complete with configuration, major phase transitions, significant outcomes. Current INFO logs already meet criteria - no changes required.

**Acceptance Criteria:**
- ✅ Line 91: "Fetching full season schedule (weeks 1-18)" - Major phase (KEEP)
- ✅ Line 146: "Successfully fetched schedule for {len(full_schedule)} weeks" - Significant outcome (KEEP)
- ✅ Line 236: "Schedule exported to {self.output_path}" - Completion status (KEEP)
- ✅ No implementation details in INFO logs (those are DEBUG)
- ✅ No excessive INFO logs (e.g., every function call)
- ✅ INFO logs provide user awareness of script progress
- ✅ No functionality changes (log review only)

**Current INFO Logs (All Good ✅):**
```python
# Line 91 - Major phase transition:
self.logger.info("Fetching full season schedule (weeks 1-18)")

# Line 146 - Significant outcome:
self.logger.info(f"Successfully fetched schedule for {len(full_schedule)} weeks")

# Line 236 - Completion status:
self.logger.info(f"Schedule exported to {self.output_path}")
```

**Assessment:** Current INFO logs meet criteria. No changes needed.

**User Answer:** Discovery Iteration 3 (INFO criteria)

---

### Requirement 7: Test Updates

**Source:** RESEARCH_NOTES.md (test file analysis)

**Description:**
Update test_ScheduleFetcher.py to handle new enable_log_file parameter. No caplog tests needed (per discovery, focus on functionality not log messages).

**Acceptance Criteria:**
- ✅ No test instantiation changes needed (enable_log_file defaults to False)
- ✅ Line 33 assertion unchanged: `assert fetcher.logger is not None`
- ✅ All existing tests pass with new parameter (backward compatible)
- ✅ No caplog tests added (not required per discovery)
- ✅ Optional: Add explicit enable_log_file=False to test instantiations for clarity

**Example:**
```python
# Before (test_ScheduleFetcher.py line 30):
fetcher = ScheduleFetcher(output_path)

# After (optional, for explicitness):
fetcher = ScheduleFetcher(output_path, enable_log_file=False)

# OR (same result, using default):
fetcher = ScheduleFetcher(output_path)
```

**User Answer:** Discovery Q8 (test coverage focused on functionality)

---

## Technical Requirements

**Source:** RESEARCH_NOTES.md

### File Modifications

**Files to modify:**
1. `run_schedule_fetcher.py` (lines 16-59)
   - Add argparse import
   - Add setup_logger import
   - Add argument parsing
   - Add logger setup
   - Replace print() statements with logger calls
   - Pass enable_log_file to ScheduleFetcher

2. `schedule-data-fetcher/ScheduleFetcher.py` (lines 27-36)
   - Add enable_log_file parameter to __init__()
   - Update logger name from "ScheduleFetcher" to "schedule_fetcher"
   - Add log_to_file, log_file_path, log_format parameters to setup_logger()
   - Update docstring

3. `tests/schedule-data-fetcher/test_ScheduleFetcher.py` (optional)
   - Add enable_log_file=False to test instantiations for clarity
   - No assertion changes needed

**Files NOT modified:**
- ScheduleFetcher.py methods (lines 38-240) - log quality already meets criteria

---

### Import Dependencies

```python
# run_schedule_fetcher.py additions:
import argparse
from utils.LoggingManager import setup_logger

# ScheduleFetcher.py (existing imports - no changes):
from utils.LoggingManager import setup_logger  # Already imported
```

---

### Data Flow

```
User runs script with --enable-log-file flag
  ↓
argparse parses args.enable_log_file = True
  ↓
main() calls setup_logger(name="schedule_fetcher", log_to_file=True, ...)
  ↓
Logger configured with LineBasedRotatingHandler (from Feature 01)
  ↓
main() instantiates ScheduleFetcher(output_path, enable_log_file=True)
  ↓
ScheduleFetcher.__init__() calls setup_logger(name="schedule_fetcher", log_to_file=True, ...)
  ↓
Logger writes to logs/schedule_fetcher/schedule_fetcher-{timestamp}.log
  ↓
500-line rotation automatic (LineBasedRotatingHandler)
  ↓
Max 50 files enforced (cleanup automatic)
```

---

## Integration Points

### Integration with Feature 1 (Core Infrastructure)

**Direction:** This feature consumes FROM Feature 1

**Data Passed:**
- **Class:** LineBasedRotatingHandler (used by LoggingManager automatically)
- **API:** Modified setup_logger() function with log_to_file parameter
- **Folder Structure:** logs/schedule_fetcher/ (auto-created by handler)

**Interface:**

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

**Feature 07 Usage:**
```python
from utils.LoggingManager import setup_logger

logger = setup_logger(
    name="schedule_fetcher",        # Logger name (becomes folder name)
    level="INFO",                    # Log level
    log_to_file=True,               # Enable file logging (CLI-driven)
    log_file_path=None,             # Let LoggingManager auto-generate path
    log_format="standard"           # Format style
    # enable_console=True (default, can omit)
    # max_file_size, backup_count (optional, can omit)
)
# Result:
#   Initial file: logs/schedule_fetcher/schedule_fetcher-{YYYYMMDD_HHMMSS}.log
#   Rotated files: logs/schedule_fetcher/schedule_fetcher-{YYYYMMDD_HHMMSS_microseconds}.log
#   500-line rotation automatic
```

**Note:** Updated based on feature_01 actual implementation. Rotated files include microsecond precision.

**Integration Contracts (from Feature 01):**
1. **Logger name = folder name:** Use "schedule_fetcher" consistently (not "ScheduleFetcher" or variations)
2. **log_file_path=None:** Don't specify custom paths (let LoggingManager generate)
3. **log_to_file from CLI:** Wire --enable-log-file flag to log_to_file parameter

**Example Flow:**
```
Feature 01 (core infrastructure)
  ↓ provides LineBasedRotatingHandler
  ↓ provides modified setup_logger() that instantiates LineBasedRotatingHandler
  ↓ provides logs/schedule_fetcher/ folder structure

Feature 07 (schedule_fetcher_logging)
  ↓ calls setup_logger(name="schedule_fetcher", level="INFO", log_to_file=args.enable_log_file, ...)
  ↓ CLI flag --enable-log-file controls log_to_file parameter

End Users
  ↓ run script with --enable-log-file flag
  ↓ logs written to logs/schedule_fetcher/ folder
  ↓ 500-line rotation automatic
  ↓ max 50 files enforced automatically
```

---

## Error Handling

**Source:** RESEARCH_NOTES.md + Feature 01 spec.md

### Error Scenario 1: Folder Creation Failure

**Trigger:** Permission denied or disk full when creating logs/schedule_fetcher/ folder

**Handling:**
- Handled by Feature 01 (LineBasedRotatingHandler)
- Error logged to stderr (not the log file, since file can't be created)
- Script continues (console logging unaffected)

**User Impact:** Log messages not written to file (console logging unaffected)

**Mitigation:** Document requirement that user needs write permissions to project root

---

### Error Scenario 2: Argparse Compatibility with Async

**Trigger:** User concerned about argparse usage in async main()

**Handling:**
- argparse.parse_args() is synchronous (no async/await needed)
- Called BEFORE asyncio.run(main()) or at start of async main()
- No compatibility issues

**User Impact:** None (works correctly)

**Mitigation:** None needed (standard pattern)

---

### Error Scenario 3: Backward Compatibility Break

**Trigger:** Existing code calls ScheduleFetcher(output_path) without enable_log_file parameter

**Handling:**
- enable_log_file defaults to False (backward compatible)
- Existing code works unchanged
- Console logging behavior preserved

**User Impact:** None (backward compatible)

**Mitigation:** Default parameter value ensures backward compatibility

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

**Notes for S4:**
- Test argparse flag parsing (--enable-log-file present/absent)
- Test ScheduleFetcher instantiation with enable_log_file=True/False
- Test backward compatibility (ScheduleFetcher without enable_log_file parameter)
- No caplog tests needed (per discovery)
- Focus on functionality, not log message content

---

## Non-Functional Requirements

**Performance:**
- ✅ No performance impact when --enable-log-file not provided (console logging only)
- ✅ Minimal overhead when --enable-log-file provided (<1ms per log call)
- ✅ Async main pattern unaffected (argparse synchronous, no blocking)

**Reliability:**
- ✅ Script behavior unchanged when flag not provided (backward compatibility)
- ✅ Graceful degradation if file logging fails (falls back to console)
- ✅ All error handling delegated to Feature 01 (LineBasedRotatingHandler)

**Maintainability:**
- ✅ Must follow project coding standards (CODING_STANDARDS.md)
- ✅ Must maintain backward compatibility with existing callers
- ✅ Must use type hints for new parameters
- ✅ Must include docstring updates for modified functions
- ✅ Consistent with other features' CLI integration patterns

**Testability:**
- ✅ All modifications testable via existing test suite
- ✅ Backward compatibility testable (run tests without changes)
- ✅ CLI flag parsing testable (argparse standard patterns)
- ✅ 100% test pass rate required before commit

**Compatibility:**
- ✅ Python 3.8+ compatibility (asyncio.run available)
- ✅ Cross-platform compatibility (argparse standard library)
- ✅ Backward compatibility with existing ScheduleFetcher callers

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Core infrastructure changes (Feature 1 responsibility)
- Other scripts' CLI integration (Features 2-6)
- Console logging changes (only file logging affected)
- Log format changes (keeping existing formats)
- New log calls (existing logs already meet quality criteria)
- Comprehensive log message refactoring (current logs sufficient)

---

## Open Questions

{To be populated during S2.P1.I2 (Checklist Resolution) - questions tracked in checklist.md}

No open questions currently - to be identified during checklist creation.

---

## Implementation Notes

**Source:** RESEARCH_NOTES.md + Discovery findings

### Design Decisions from Research

1. **Logger Name Change:**
   - ✅ Change from "ScheduleFetcher" to "schedule_fetcher"
   - **Rationale:** Consistency with project naming conventions, matches folder name pattern
   - **Alternative Rejected:** Keep "ScheduleFetcher" - inconsistent with other features

2. **Argparse in Async Main:**
   - ✅ Call argparse.parse_args() at start of async main()
   - **Rationale:** argparse is synchronous, no async/await needed, standard pattern
   - **Alternative Rejected:** Parse args before asyncio.run() - less encapsulated

3. **Parameter Default Value:**
   - ✅ enable_log_file defaults to False
   - **Rationale:** Backward compatibility with existing callers, matches discovery Q4
   - **Alternative Rejected:** No default - breaking change for tests

4. **Log Quality Changes:**
   - ✅ No changes to existing DEBUG/INFO logs
   - **Rationale:** Current logs already meet discovery criteria, changes unnecessary
   - **Alternative Rejected:** Comprehensive refactoring - over-engineering

5. **Print Statement Replacement:**
   - ✅ Replace all print() with logger.info/error
   - **Rationale:** Consistent with improved logging infrastructure goal
   - **Alternative Rejected:** Keep print statements - mixed output paradigm

6. **Test Coverage:**
   - ✅ No caplog tests added
   - **Rationale:** Discovery Q8 focuses on functionality not log messages
   - **Alternative Rejected:** Comprehensive caplog tests - not required

---

### Implementation Tips

**Argparse in Async:**
- Call parse_args() at START of async main() (before any await calls)
- No async/await needed for argparse operations
- Standard pattern used in other async CLI tools

**Logger Setup:**
- Call setup_logger() ONCE in main() (line-level logger)
- Call setup_logger() ONCE in ScheduleFetcher.__init__() (class-level logger)
- Both use same logger name "schedule_fetcher" for consistency

**Parameter Threading:**
- main() receives args.enable_log_file from argparse
- main() passes enable_log_file to ScheduleFetcher constructor
- ScheduleFetcher passes enable_log_file to setup_logger(log_to_file=...)

**Testing:**
- Run existing test suite WITHOUT changes first (verify backward compatibility)
- Tests should pass with default enable_log_file=False
- Optional: Add explicit enable_log_file=False for clarity

---

### Gotchas

**Gotcha 1: Logger Name Case Sensitivity**
- **Issue:** Folder name on Windows case-insensitive, Linux case-sensitive
- **Impact:** "ScheduleFetcher" vs "schedule_fetcher" may create duplicate folders on Linux
- **Mitigation:** Use lowercase "schedule_fetcher" consistently

**Gotcha 2: Argparse Called After asyncio.run()**
- **Issue:** If parse_args() called outside async main(), can't access args inside main()
- **Impact:** Need to pass args as parameter or global variable
- **Mitigation:** Call parse_args() INSIDE async main() function

**Gotcha 3: Two Loggers with Same Name**
- **Issue:** Both main() and ScheduleFetcher call setup_logger(name="schedule_fetcher")
- **Impact:** Python logging module reuses existing logger (same instance)
- **Mitigation:** Feature, not bug (both use same logger, same config)

---

### Code Organization

**File Structure:**
```
run_schedule_fetcher.py         # MODIFY: Add argparse, logger setup, replace prints
schedule-data-fetcher/
└── ScheduleFetcher.py          # MODIFY: Add enable_log_file parameter, update logger name
tests/schedule-data-fetcher/
└── test_ScheduleFetcher.py     # OPTIONAL: Add enable_log_file=False to instantiations
```

**Import Dependencies:**
```python
# run_schedule_fetcher.py (additions):
import argparse
from utils.LoggingManager import setup_logger

# ScheduleFetcher.py (no new imports needed):
from utils.LoggingManager import setup_logger  # Already imported
```

---

### Acceptance Criteria Cross-Reference

All functional requirements map to acceptance criteria:

| Requirement | Test Coverage | Implementation Location |
|-------------|---------------|-------------------------|
| Req 1: CLI Flag Integration | test_ScheduleFetcher.py: backward compatibility | run_schedule_fetcher.py: main() |
| Req 2: Logger Name Consistency | Manual verification (folder name) | ScheduleFetcher.py: __init__() line 35 |
| Req 3: Parameter Addition | test_ScheduleFetcher.py: existing tests pass | ScheduleFetcher.py: __init__() line 27 |
| Req 4: Replace Print Statements | Manual verification (script output) | run_schedule_fetcher.py: lines 37, 43, 49-51, 56 |
| Req 5: Log Quality DEBUG | Manual code review | ScheduleFetcher.py: lines 94, 138 (no changes) |
| Req 6: Log Quality INFO | Manual code review | ScheduleFetcher.py: lines 91, 146, 236 (no changes) |
| Req 7: Test Updates | test_ScheduleFetcher.py: all pass | test_ScheduleFetcher.py: optional updates |

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
| 2026-02-06 | Agent (Secondary-F) | Complete spec draft with all requirements, technical details, integration points, error handling, and implementation notes | S2.P1.I1 (Feature-Level Discovery - research complete) |
| 2026-02-08 12:25 | Agent | Updated setup_logger() signature, type hints, return type, filename formats based on Feature 01 actual implementation | S8.P1 (Cross-Feature Alignment - Feature 01 complete) |

---

*End of spec.md*
