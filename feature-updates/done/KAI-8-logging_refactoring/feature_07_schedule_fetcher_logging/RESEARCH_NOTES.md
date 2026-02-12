# Research Notes: Feature 07 - schedule_fetcher_logging

**Feature:** schedule_fetcher_logging
**Researched:** 2026-02-06 (Secondary-F)
**Part of Epic:** KAI-8-logging_refactoring

---

## Research Summary

Feature 07 adds --enable-log-file CLI flag to run_schedule_fetcher.py and improves log quality in schedule-data-fetcher/ modules.

**Scope:**
- Add CLI integration (argparse + --enable-log-file flag)
- Modify ScheduleFetcher class to accept log_to_file parameter
- Review and improve existing log quality
- Update logger name from "ScheduleFetcher" to "schedule_fetcher"
- Update test assertions if needed

---

## Code Locations

### Main Entry Point

**File:** `run_schedule_fetcher.py` (lines 1-64)

**Current State:**
- Async main entry point using `asyncio.run()`
- No argparse setup (no CLI flags)
- Uses `print()` statements (lines 37, 43, 49-51, 56)
- Instantiates ScheduleFetcher (line 35)

**Needs:**
- Add argparse setup with --enable-log-file flag
- Add logging setup (call setup_logger)
- Replace print() statements with logger calls
- Pass log_to_file parameter to ScheduleFetcher

**Example CLI Flag Pattern:** See Feature 02 (run_league_helper.py) for argparse pattern

---

### Main Module

**File:** `schedule-data-fetcher/ScheduleFetcher.py` (lines 1-240)

**Current State:**
- Already imports and uses setup_logger() (line 15, 35)
- Logger name: "ScheduleFetcher" (line 35) - ❌ Should be "schedule_fetcher" per naming convention
- Logger level: "INFO" (line 35)
- No log_to_file parameter (line 35) - defaults to console only

**Current Logging Calls:**
- Line 70: `self.logger.error(f"HTTP request failed: {e}")` - ✅ Good
- Line 73: `self.logger.error(f"Failed to parse response: {e}")` - ✅ Good
- Line 91: `self.logger.info("Fetching full season schedule (weeks 1-18)")` - ✅ Good (major phase)
- Line 94: `self.logger.debug(f"Fetching schedule for week {week}/18")` - ✅ Good (progress)
- Line 138: `self.logger.debug(f"Error parsing event in week {week}: {e}")` - ✅ Good (error detail)
- Line 146: `self.logger.info(f"Successfully fetched schedule for {len(full_schedule)} weeks")` - ✅ Good (outcome)
- Line 154: `self.logger.error(f"Failed to fetch full season schedule: {e}")` - ✅ Good
- Line 236: `self.logger.info(f"Schedule exported to {self.output_path}")` - ✅ Good (completion)
- Line 239: `self.logger.error(f"Failed to export schedule to CSV: {e}")` - ✅ Good

**Needs:**
- Update logger name from "ScheduleFetcher" to "schedule_fetcher" (line 35)
- Add log_to_file parameter to setup_logger() call (line 35)
- Add enable_log_file parameter to __init__() signature (line 27)
- Current logs already meet quality criteria - minimal changes needed

---

### Tests

**File:** `tests/schedule-data-fetcher/test_ScheduleFetcher.py` (lines 1-312)

**Current State:**
- Line 33: `assert fetcher.logger is not None` - Verifies logger exists
- No caplog usage (no log message assertions)
- Tests focus on functionality, not logging behavior

**Needs:**
- Update assertion on line 33 if logger verification changes
- No caplog tests needed (per discovery, test coverage focused on functionality)

---

## Integration Points

### Feature 01 Dependencies (Core Infrastructure)

**From Feature 01 spec.md:**

**API to use:**
```python
from utils.LoggingManager import setup_logger

logger = setup_logger(
    name="schedule_fetcher",        # Logger name (becomes folder name)
    level="INFO",                    # Log level
    log_to_file=True,               # Enable file logging (CLI-driven)
    log_file_path=None,             # Let LoggingManager auto-generate path
    log_format="standard"           # Format style
)
# Result: logs/schedule_fetcher/schedule_fetcher-{timestamp}.log with 500-line rotation
```

**Integration Contracts:**
1. **Logger name = folder name:** Use "schedule_fetcher" consistently (not "ScheduleFetcher" or variations)
2. **log_file_path=None:** Don't specify custom paths (let LoggingManager generate)
3. **log_to_file from CLI:** Wire --enable-log-file flag to log_to_file parameter

**Folder Structure:**
- Logs written to: `logs/schedule_fetcher/schedule_fetcher-{YYYYMMDD_HHMMSS}.log`
- 500-line rotation automatic (LineBasedRotatingHandler)
- Max 50 files per folder with auto-cleanup

---

## Log Quality Analysis

### DEBUG Level (Discovery Criteria)

**Current DEBUG logs:**
- Line 94: `f"Fetching schedule for week {week}/18"` - ✅ Good (progress tracking, not excessive)
- Line 138: `f"Error parsing event in week {week}: {e}"` - ✅ Good (error detail for debugging)

**Assessment:** Current DEBUG logs meet quality criteria (function progress, error details). No changes needed.

---

### INFO Level (Discovery Criteria)

**Current INFO logs:**
- Line 91: `"Fetching full season schedule (weeks 1-18)"` - ✅ Good (major phase transition)
- Line 146: `f"Successfully fetched schedule for {len(full_schedule)} weeks"` - ✅ Good (significant outcome)
- Line 236: `f"Schedule exported to {self.output_path}"` - ✅ Good (completion status)

**Assessment:** Current INFO logs meet quality criteria (major phases, outcomes). No changes needed.

---

### ERROR Level

**Current ERROR logs:**
- Line 70: `f"HTTP request failed: {e}"` - ✅ Good (captures exception)
- Line 73: `f"Failed to parse response: {e}"` - ✅ Good (captures exception)
- Line 154: `f"Failed to fetch full season schedule: {e}"` - ✅ Good (captures exception)
- Line 239: `f"Failed to export schedule to CSV: {e}"` - ✅ Good (captures exception)

**Assessment:** Current ERROR logs are comprehensive. No changes needed.

---

## Modification Summary

### run_schedule_fetcher.py Changes

**Add argparse setup:**
```python
import argparse

def main():
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

    # Replace print() with logger calls
    logger.info(f"Fetching NFL season schedule for {NFL_SEASON}...")

    # Pass log_to_file to ScheduleFetcher
    fetcher = ScheduleFetcher(output_path, enable_log_file=args.enable_log_file)
```

**Replace print() statements:**
- Line 37: `print(f"Fetching NFL season schedule...")` → `logger.info(...)`
- Line 43: `print("ERROR: Failed to fetch...")` → `logger.error(...)`
- Line 49-51: `print(f"✓ Schedule successfully exported...")` → `logger.info(...)`
- Line 56: `print(f"ERROR: {e}")` → `logger.error(...)`

---

### ScheduleFetcher.py Changes

**Update __init__() signature:**
```python
def __init__(self, output_path: Path, enable_log_file: bool = False):
    """
    Initialize the ScheduleFetcher.

    Args:
        output_path: Path where season_schedule.csv will be written
        enable_log_file: Enable logging to file (default: False)
    """
    self.output_path = output_path
    self.logger = setup_logger(
        name="schedule_fetcher",         # Changed from "ScheduleFetcher"
        level="INFO",
        log_to_file=enable_log_file,    # Added parameter
        log_file_path=None,              # Added parameter
        log_format="standard"            # Added parameter
    )
    self.client: Optional[httpx.AsyncClient] = None
```

**Changes:**
1. Add `enable_log_file` parameter to `__init__()` (line 27)
2. Update logger name from "ScheduleFetcher" to "schedule_fetcher" (line 35)
3. Add `log_to_file=enable_log_file` to setup_logger() call (line 35)
4. Add `log_file_path=None` to setup_logger() call (line 35)
5. Add `log_format="standard"` to setup_logger() call (line 35)

---

### test_ScheduleFetcher.py Changes

**Update test instantiation:**
- All `ScheduleFetcher(output_path)` calls need to pass `enable_log_file=False` or omit (defaults to False)
- No changes needed to assertion on line 33 (logger still exists)

**Example:**
```python
# Before:
fetcher = ScheduleFetcher(output_path)

# After:
fetcher = ScheduleFetcher(output_path, enable_log_file=False)
# OR (same result, using default):
fetcher = ScheduleFetcher(output_path)
```

---

## Open Questions

{To be populated during checklist resolution}

---

## External Library Compatibility

**httpx library (already used):**
- No mock/test environment issues found
- AsyncMock used in tests (line 108) - works correctly
- No compatibility concerns

---

## Implementation Complexity

**Estimated Size:** SMALL

**Justification:**
- Single script (run_schedule_fetcher.py) + single main module (ScheduleFetcher.py)
- Minimal log quality changes needed (current logs already meet criteria)
- Primary work: CLI integration (argparse + flag wiring)
- Test updates: Parameter addition only (no caplog tests needed)
- No new modules or complex logic

**Time Estimate:** 30-45 minutes implementation + 15 minutes testing

---

## Notes

- ScheduleFetcher is simplest feature in epic (1 script, 1 main module, minimal logging)
- Current log quality already meets Discovery criteria - no significant rewrites needed
- Main work is CLI integration and parameter threading
- Logger name change ("ScheduleFetcher" → "schedule_fetcher") aligns with project conventions

---

*End of RESEARCH_NOTES.md*
