# Research Notes: core_logging_infrastructure

**Feature:** 01 - core_logging_infrastructure
**Part of Epic:** KAI-8-logging_refactoring
**Research Date:** 2026-02-06
**Status:** S2.P1.I1 (Feature-Level Discovery)

---

## Purpose

Document all technical research findings for implementing LineBasedRotatingHandler, centralized logs/ folder structure, 500-line rotation, max 50 files cleanup, and .gitignore update.

---

## Code Locations Identified

### Primary Implementation File

**File:** `utils/LoggingManager.py` (174 lines)
**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/utils/LoggingManager.py`

**Current Implementation:**
- **Lines 20-143:** LoggingManager class with setup_logger() method
- **Lines 45-118:** setup_logger() method - Creates logger, adds console/file handlers
- **Lines 95-115:** File handler creation - Uses `logging.handlers.RotatingFileHandler`
- **Lines 134-142:** _generate_log_file_path() method - Current format: `{logger_name}_{YYYYMMDD}.log`
- **Lines 107-115:** RotatingFileHandler instantiation:
  ```python
  file_handler = logging.handlers.RotatingFileHandler(
      log_file_path,
      maxBytes=max_file_size,  # Default 10MB before rotation
      backupCount=backup_count,  # Keep last 5 rotated files
      encoding='utf-8'
  )
  ```

**Modification Points:**
1. **Replace RotatingFileHandler** (Lines 107-115) with LineBasedRotatingHandler instantiation
2. **Update _generate_log_file_path()** (Lines 134-142) to use YYYYMMDD_HHMMSS format
3. **Add script_name parameter** to setup_logger() for folder structure (logs/{script_name}/)
4. **Import new handler class** at top of file

---

### Test File

**File:** `tests/utils/test_LoggingManager.py` (359 lines)
**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/tests/utils/test_LoggingManager.py`

**Current Test Coverage:**
- **Lines 92-103:** Test file handler creation with RotatingFileHandler
- **Lines 104-111:** Test log directory creation (verifies parent.mkdir())
- **Lines 205-237:** Test RotatingFileHandler max_size and backup_count
- **Lines 256-283:** Test _generate_log_file_path() output format

**Test Updates Needed:**
1. Replace `RotatingFileHandler` type checks with `LineBasedRotatingHandler`
2. Update _generate_log_file_path() assertions to expect YYYYMMDD_HHMMSS format
3. Add new tests for:
   - Line-based rotation (emit 501 logs, verify 2 files created)
   - Cleanup strategy (create 51 files, verify oldest deleted)
   - Folder structure (verify logs/{script_name}/ created)
   - Line counter behavior (verify counter increments, resets on rotation)

---

### Configuration File

**File:** `.gitignore` (221 lines)
**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/.gitignore`

**Current State:**
- **Line 70:** `*.log` - Excludes all .log files globally
- **No logs/ folder exclusion** - Need to add

**Modification:**
- **Add:** `logs/` entry (after line 70 or in "Project-specific" section at top)
- **Note:** `logs/` folder exclusion takes precedence over `*.log` pattern, so logs/ will exclude entire folder

---

## Python logging.handlers Research

### logging.FileHandler (Parent Class)

**Source:** Python standard library `logging.handlers`

**Key Methods:**
- `emit(record)` - Write a log record to file
  - Opens stream if not open
  - Calls `StreamHandler.emit(self, record)` to format and write
  - Line to override for line counting

**Implementation Pattern:**
```python
def emit(self, record):
    if self.stream is None:
        if self.mode != 'w' or not self._closed:
            self.stream = self._open()
    if self.stream:
        StreamHandler.emit(self, record)
```

---

### logging.handlers.RotatingFileHandler (Reference Implementation)

**Source:** Python standard library `logging.handlers`

**Key Methods:**
1. `shouldRollover(record)` - Check if rotation needed
   - Checks if file size would exceed maxBytes after writing record
   - Returns True if rotation needed, False otherwise

2. `doRollover()` - Perform rotation
   - Close current stream
   - Rename files: log → log.1 → log.2 → ... → log.N
   - Keep only backupCount files (delete log.N+1)
   - Reopen stream to new file

**Rotation Pattern (Sequential Renaming):**
```python
for i in range(self.backupCount - 1, 0, -1):
    sfn = "%s.%d" % (self.baseFilename, i)
    dfn = "%s.%d" % (self.baseFilename, i + 1)
    if os.path.exists(sfn):
        if os.path.exists(dfn):
            os.remove(dfn)
        os.rename(sfn, dfn)
```

**Our Approach (Timestamped Files):**
- Do NOT use sequential renaming (log.1, log.2, ...)
- Create new timestamped file on each rotation
- Scan folder, sort by modification time, delete oldest if >50 files

---

## Script Usage Patterns

### Current setup_logger() Calls

**run_accuracy_simulation.py:**
```python
LOGGING_TO_FILE = True           # Hardcoded boolean
LOG_NAME = "accuracy_simulation"
LOGGING_FILE = "./simulation/accuracy_log.txt"  # Hardcoded path
LOGGING_FORMAT = "detailed"

setup_logger(LOG_NAME, args.log_level.upper(), LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
```

**run_win_rate_simulation.py:**
```python
LOGGING_TO_FILE = False         # Hardcoded boolean
LOG_NAME = "simulation"
LOGGING_FILE = './simulation/log.txt'  # Hardcoded path
LOGGING_FORMAT = 'standard'

setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
```

**run_game_data_fetcher.py:**
```python
logger = setup_logger("game_data_fetcher", "INFO", False, None, "standard")
```

**Pattern Observations:**
- All scripts use module-level constants for LOGGING_TO_FILE (boolean)
- Scripts specify custom log file paths (e.g., "./simulation/accuracy_log.txt")
- Most scripts hardcode LOGGING_TO_FILE = True or False (no CLI control yet)

**What Needs to Change (in Features 2-7, NOT this feature):**
- Add `--enable-log-file` CLI flag to each script
- Remove hardcoded log file paths (let LoggingManager generate them)
- Pass script name to LoggingManager for folder structure

---

## LineBasedRotatingHandler Design

### Class Hierarchy

```
logging.Handler (base)
  ↓
logging.StreamHandler
  ↓
logging.FileHandler (parent class)
  ↓
LineBasedRotatingHandler (our custom handler)
```

### Key Design Decisions

**1. Parent Class:** Subclass `logging.FileHandler` (not RotatingFileHandler)
- FileHandler provides file I/O primitives
- RotatingFileHandler's size-based logic doesn't apply
- Cleaner to implement line-based logic from scratch

**2. Line Counter:**
- **Storage:** In-memory instance variable `self.line_count`
- **Initialization:** Set to 0 in __init__()
- **Increment:** On each emit() call
- **Reset:** On rotation (new file created)
- **Persistence:** Does NOT persist across script restarts (matches user requirement Q7)

**3. Rotation Threshold:**
- **Value:** 500 lines (hardcoded constant)
- **Check:** Before each emit(), check if `self.line_count >= 500`
- **Action:** If threshold reached, call doRollover(), reset counter

**4. File Naming:**
- **Format:** `{script_name}-{YYYYMMDD_HHMMSS}.log`
- **Example:** `league_helper-20260206_143522.log`
- **Timestamp:** Generated at rotation time using `datetime.now().strftime('%Y%m%d_%H%M%S')`

**5. Folder Structure:**
- **Root:** `logs/` folder at project root
- **Subfolders:** `logs/{script_name}/` (e.g., `logs/league_helper/`, `logs/accuracy_simulation/`)
- **Creation:** Auto-created by handler using `Path.mkdir(parents=True, exist_ok=True)`

**6. Cleanup Strategy:**
- **Trigger:** After each rotation, before opening new file
- **Method:** `_cleanup_old_files()`
- **Logic:**
  1. Scan `logs/{script_name}/` folder
  2. Get all .log files sorted by modification time (oldest first)
  3. If count > 50, delete oldest files until count == 50
- **Implementation:**
  ```python
  def _cleanup_old_files(self):
      log_dir = Path(self.baseFilename).parent
      log_files = sorted(log_dir.glob('*.log'), key=lambda p: p.stat().st_mtime)
      while len(log_files) > 50:
          oldest = log_files.pop(0)
          oldest.unlink()  # Delete file
  ```

**7. Integration with LoggingManager:**
- **Modification:** Replace RotatingFileHandler instantiation in setup_logger() (lines 107-115)
- **Parameters:** `LineBasedRotatingHandler(log_file_path, max_lines=500, max_files=50)`
- **Import:** Add `from utils.LineBasedRotatingHandler import LineBasedRotatingHandler`
- **Backward Compatibility:** setup_logger() signature unchanged (existing callers work)

---

## Method Signatures

### LineBasedRotatingHandler.__init__()

```python
def __init__(
    self,
    filename,
    mode='a',
    max_lines=500,
    max_files=50,
    encoding=None,
    delay=False
):
    """
    Initialize line-based rotating file handler.

    Args:
        filename: Log file path (e.g., logs/league_helper/league_helper-20260206_143522.log)
        mode: File open mode ('a' for append)
        max_lines: Maximum lines per file before rotation (default 500)
        max_files: Maximum files per folder before cleanup (default 50)
        encoding: File encoding (default None = platform default, recommend 'utf-8')
        delay: Delay file opening until first emit (default False)
    """
    super().__init__(filename, mode, encoding, delay)
    self.max_lines = max_lines
    self.max_files = max_files
    self.line_count = 0
```

### LineBasedRotatingHandler.emit()

```python
def emit(self, record):
    """
    Emit a record, with line-based rotation.

    - Increment line counter
    - Check if rotation needed (line_count >= max_lines)
    - If rotation needed, call doRollover()
    - Write record to file
    """
    try:
        if self.shouldRollover(record):
            self.doRollover()

        # Call parent emit() to write record
        logging.FileHandler.emit(self, record)

        # Increment line counter AFTER successful write
        self.line_count += 1

    except Exception:
        self.handleError(record)
```

### LineBasedRotatingHandler.shouldRollover()

```python
def shouldRollover(self, record):
    """
    Determine if rollover should occur based on line count.

    Returns:
        True if line_count >= max_lines, False otherwise
    """
    return self.line_count >= self.max_lines
```

### LineBasedRotatingHandler.doRollover()

```python
def doRollover(self):
    """
    Perform file rotation:
    1. Close current stream
    2. Generate new timestamped filename
    3. Cleanup old files (if >max_files)
    4. Open new file stream
    5. Reset line counter
    """
    if self.stream:
        self.stream.close()
        self.stream = None

    # Generate new timestamped filename
    self.baseFilename = self._generate_new_filename()

    # Cleanup old files
    self._cleanup_old_files()

    # Open new file
    if not self.delay:
        self.stream = self._open()

    # Reset line counter
    self.line_count = 0
```

### LineBasedRotatingHandler._generate_new_filename()

```python
def _generate_new_filename(self):
    """
    Generate new timestamped filename for rotation.

    Format: {script_name}-{YYYYMMDD_HHMMSS}.log
    Example: logs/league_helper/league_helper-20260206_143522.log

    Returns:
        str: Full path to new log file
    """
    log_dir = Path(self.baseFilename).parent
    script_name = log_dir.name  # Assumes folder name = script name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{script_name}-{timestamp}.log"
    return str(log_dir / new_filename)
```

### LineBasedRotatingHandler._cleanup_old_files()

```python
def _cleanup_old_files(self):
    """
    Delete oldest log files if folder exceeds max_files limit.

    Logic:
    1. Get all .log files in folder
    2. Sort by modification time (oldest first)
    3. While count > max_files, delete oldest
    """
    log_dir = Path(self.baseFilename).parent
    log_files = sorted(log_dir.glob('*.log'), key=lambda p: p.stat().st_mtime)

    while len(log_files) > self.max_files:
        oldest = log_files.pop(0)
        try:
            oldest.unlink()  # Delete file
        except OSError:
            # File may have been deleted externally, ignore error
            pass
```

---

## Integration Points

### LoggingManager.setup_logger() Modification

**Current Code (Lines 107-115):**
```python
file_handler = logging.handlers.RotatingFileHandler(
    log_file_path,
    maxBytes=max_file_size,
    backupCount=backup_count,
    encoding='utf-8'
)
```

**New Code:**
```python
from utils.LineBasedRotatingHandler import LineBasedRotatingHandler

# ... in setup_logger() method ...

file_handler = LineBasedRotatingHandler(
    log_file_path,
    max_lines=500,  # Hardcoded constant
    max_files=50,   # Hardcoded constant
    encoding='utf-8'
)
```

**Note:** max_file_size and backup_count parameters become unused (remove from signature? Or keep for backward compatibility?)

### LoggingManager._generate_log_file_path() Modification

**Current Code (Lines 134-142):**
```python
def _generate_log_file_path(self, log_path: str, logger_name: str) -> Path:
    """Generate a log file path with timestamp for daily log rotation."""
    timestamp = datetime.now().strftime('%Y%m%d')
    filename = f"{logger_name}_{timestamp}.log"
    return log_path / filename
```

**New Code:**
```python
def _generate_log_file_path(self, log_path: Path, logger_name: str) -> Path:
    """
    Generate a log file path with full timestamp.

    Creates folder structure: logs/{logger_name}/{logger_name}-{YYYYMMDD_HHMMSS}.log

    Args:
        log_path: Base log directory (e.g., Path('logs'))
        logger_name: Script name for subfolder (e.g., 'league_helper')

    Returns:
        Path to log file (e.g., logs/league_helper/league_helper-20260206_143522.log)
    """
    # Create script-specific subfolder
    log_dir = log_path / logger_name

    # Generate timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{logger_name}-{timestamp}.log"

    return log_dir / filename
```

**Key Changes:**
1. Timestamp format: `%Y%m%d` → `%Y%m%d_%H%M%S`
2. Filename format: `{name}_{timestamp}` → `{name}-{timestamp}` (underscore → hyphen separator)
3. Folder structure: `log_path/` → `log_path/{logger_name}/` (script-specific subfolder)

---

## File Structure

### New File Location

**File:** `utils/LineBasedRotatingHandler.py` (NEW FILE)
**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/utils/LineBasedRotatingHandler.py`

**Contents:**
- LineBasedRotatingHandler class (subclass of logging.FileHandler)
- __init__, emit, shouldRollover, doRollover methods
- _generate_new_filename, _cleanup_old_files helper methods
- Module docstring
- Import statements: logging, datetime, pathlib.Path, os

**Estimated Size:** ~150-200 lines (including docstrings and error handling)

---

## Folder Structure Example

**Before (Current State):**
```
/home/kai/code/FantasyFootballHelperScriptsRefactored/
├── simulation/
│   ├── accuracy_log.txt       # Hardcoded path in run_accuracy_simulation.py
│   └── log.txt                # Hardcoded path in run_win_rate_simulation.py
└── (other logs scattered)
```

**After (New Structure):**
```
/home/kai/code/FantasyFootballHelperScriptsRefactored/
├── logs/                                   # NEW: Root logs folder (.gitignored)
│   ├── league_helper/                      # Script-specific subfolder
│   │   ├── league_helper-20260206_143522.log
│   │   ├── league_helper-20260206_144105.log
│   │   └── ... (max 50 files, auto-cleanup)
│   ├── accuracy_simulation/
│   │   ├── accuracy_simulation-20260206_090000.log
│   │   └── ...
│   ├── simulation/                         # win_rate_simulation uses "simulation" name
│   │   └── ...
│   ├── game_data_fetcher/
│   │   └── ...
│   ├── player-data-fetcher/
│   │   └── ...
│   └── schedule_fetcher/
│       └── ...
└── simulation/
    └── (other files, no logs)
```

---

## External Dependencies

**Python Standard Library:**
- `logging` - Base logging module
- `logging.handlers` - Handler classes (FileHandler parent)
- `datetime` - Timestamp generation
- `pathlib.Path` - File path manipulation
- `os` - File operations (unlink for deletion)

**No External Libraries Required** - All functionality available in Python stdlib.

---

## Compatibility Verification

### Python Version Compatibility

**Target:** Python 3.8+ (project requirement)

**Feature Usage:**
- `logging.FileHandler` - Available since Python 2.3
- `pathlib.Path` - Available since Python 3.4
- `datetime.strftime()` - Available since Python 2.3
- `Path.glob()` - Available since Python 3.4
- `Path.unlink()` - Available since Python 3.4

**Verdict:** ✅ All features compatible with Python 3.8+

### Backward Compatibility with Existing Code

**setup_logger() Signature:**
- Current: `setup_logger(name, level, log_to_file, log_file_path, log_format, enable_console, max_file_size, backup_count)`
- New: Same signature (no changes required)
- **max_file_size, backup_count:** Parameters become unused for LineBasedRotatingHandler, but kept for backward compatibility

**Existing Callers:**
- ✅ No changes needed to existing setup_logger() calls
- ✅ Existing scripts continue to work (Feature 1 doesn't modify scripts)

**Test Compatibility:**
- ❌ test_LoggingManager.py will fail (expects RotatingFileHandler, not LineBasedRotatingHandler)
- ❌ Test assertions expect YYYYMMDD format, not YYYYMMDD_HHMMSS
- **Action:** Update test file as part of Feature 1

---

## Edge Cases and Error Handling

### Edge Case 1: Folder Creation Failure

**Scenario:** Parent directory creation fails (permission denied, disk full)
**Handling:** Path.mkdir() raises OSError, caught by logging.FileHandler.handleError()
**User Impact:** Log message not written, error logged to stderr
**Mitigation:** Document in spec that user needs write permissions to project root

### Edge Case 2: File Deletion Failure (_cleanup_old_files)

**Scenario:** Oldest log file locked by another process or permission denied
**Handling:** Catch OSError in _cleanup_old_files(), skip deletion, continue
**User Impact:** May exceed 50-file limit temporarily
**Mitigation:** Ignore error (will retry on next rotation)

### Edge Case 3: Counter Reset on Script Restart

**Scenario:** Script crashes at line 250, restarts
**Expected Behavior:** Counter resets to 0, new timestamped file created
**Actual Behavior:** Matches expected (per user requirement Q7)
**User Impact:** None (intended behavior)

### Edge Case 4: Multiple Scripts with Same logger_name

**Scenario:** Two scripts both call setup_logger("test", ...)
**Potential Issue:** Both write to logs/test/ folder
**Resolution:** Scripts should use unique logger names (e.g., script filename)
**Mitigation:** Document in Features 2-7 specs that scripts must use unique names

### Edge Case 5: Log Directory Deletion During Runtime

**Scenario:** User deletes logs/{script_name}/ folder while script running
**Handling:** Next emit() will call _open() which creates parent directory
**User Impact:** Folder recreated automatically
**Mitigation:** None needed (self-healing behavior)

### Edge Case 6: Line Counter Overflow

**Scenario:** Script runs for years, line_count exceeds int max value
**Likelihood:** Extremely low (counter resets at 500 lines)
**Handling:** Python ints have arbitrary precision, no overflow
**User Impact:** None
**Mitigation:** None needed

---

## Open Questions

**Q1:** Should max_file_size and backup_count parameters be removed from setup_logger() signature?
- **Option A:** Remove parameters (breaking change for callers who specify them)
- **Option B:** Keep parameters for backward compatibility (unused by LineBasedRotatingHandler)
- **Recommendation:** Keep parameters (Option B) - existing callers won't break
- **Tradeoff:** Dead parameters in signature (confusing), but no breaking changes

**Q2:** Should max_lines and max_files be configurable per setup_logger() call, or hardcoded constants?
- **Option A:** Add max_lines, max_files parameters to setup_logger() (flexible)
- **Option B:** Hardcode 500/50 in LineBasedRotatingHandler (simpler)
- **Discovery Note:** User said "500-line cap" and "max 50 logs" without mentioning configurability
- **Recommendation:** Hardcode constants (Option B) - matches user requirements, simpler
- **Future Work:** If configurability needed, add parameters later (non-breaking change)

**Q3:** Should _generate_log_file_path() create the subfolder, or should LineBasedRotatingHandler do it?
- **Current:** LoggingManager.setup_logger() creates parent directory (line 103)
- **Option A:** Keep current behavior (LoggingManager creates logs/{script_name}/)
- **Option B:** Move folder creation into LineBasedRotatingHandler.__init__()
- **Recommendation:** Keep current (Option A) - minimal changes to LoggingManager
- **Note:** Path.mkdir(parents=True, exist_ok=True) handles both cases gracefully

**Q4:** How should script names be determined for folder structure?
- **Current:** setup_logger() receives name parameter (e.g., "accuracy_simulation", "league_helper")
- **Issue:** Scripts may use different names (e.g., "simulation" vs "accuracy_simulation")
- **Requirement:** Folder structure uses script name (logs/{script_name}/)
- **Solution:** Use logger name as-is for folder name (Features 2-7 ensure scripts use consistent names)
- **Action:** Document in Features 2-7 specs that scripts should use script filename as logger name

**Q5:** Should .gitignore use `logs/` or `logs/**`?
- **Option A:** `logs/` - Excludes entire logs folder and contents
- **Option B:** `logs/**` - Explicit pattern for all contents
- **Recommendation:** `logs/` (Option A) - simpler, standard pattern for folder exclusion
- **Note:** Line 70 `*.log` pattern won't conflict (folder exclusion takes precedence)

---

## Testing Strategy

### Unit Tests for LineBasedRotatingHandler

**File:** `tests/utils/test_LineBasedRotatingHandler.py` (NEW FILE)

**Test Cases:**
1. **Initialization:**
   - Test handler initializes with correct max_lines, max_files
   - Test line_count starts at 0

2. **Line Counting:**
   - Emit 10 records, verify line_count == 10
   - Emit records, verify line_count increments correctly

3. **Rotation Trigger:**
   - Emit 500 records, verify no rotation yet (shouldRollover returns False at 499)
   - Emit 501st record, verify rotation triggered

4. **Rotation Behavior:**
   - After rotation, verify new timestamped file created
   - After rotation, verify line_count reset to 0
   - Verify old file still exists (not deleted)

5. **Cleanup Strategy:**
   - Create 50 log files, emit record (no cleanup)
   - Create 51 log files, emit record, verify oldest deleted
   - Create 55 log files, emit record, verify 5 oldest deleted (count == 50)

6. **File Naming:**
   - Verify filename format: {script_name}-{YYYYMMDD_HHMMSS}.log
   - Verify timestamp format (8 digits + underscore + 6 digits)

7. **Folder Structure:**
   - Verify handler creates logs/{script_name}/ folder
   - Verify parent folders created if missing

8. **Error Handling:**
   - Mock permission denied on file open, verify handleError() called
   - Mock permission denied on file delete, verify cleanup continues

### Unit Tests for LoggingManager (Updates)

**File:** `tests/utils/test_LoggingManager.py` (EXISTING FILE - UPDATE)

**Changes:**
1. Replace `RotatingFileHandler` type checks with `LineBasedRotatingHandler`
2. Update _generate_log_file_path() tests:
   - Expect YYYYMMDD_HHMMSS format (not YYYYMMDD)
   - Expect {name}-{timestamp}.log (not {name}_{timestamp}.log)
   - Expect logs/{name}/ folder structure
3. Remove tests for max_file_size and backup_count (unused by new handler)

**New Tests:**
- Test setup_logger() creates LineBasedRotatingHandler when log_to_file=True
- Test handler has max_lines=500, max_files=50

### Integration Tests (S7 Testing Phase)

**Smoke Test:**
1. Create script that emits 1000 log messages
2. Verify 2 log files created (500 lines each)
3. Verify files in logs/{script_name}/ folder
4. Verify oldest file deleted if >50 files exist

**QC Round Tests:**
- Run all 6 main scripts with --enable-log-file flag (Features 2-7 requirement)
- Verify log files created in correct folders
- Verify 500-line rotation works
- Verify max 50 files cleanup works

---

## Summary

**Research Complete:** ✅ All code locations identified, method signatures defined, edge cases analyzed

**Ready for Spec Creation:** ✅ Have all information needed to draft spec.md

**Key Findings:**
1. LoggingManager modification points clear (lines 107-115, 134-142)
2. LineBasedRotatingHandler design complete (parent class, methods, algorithm)
3. Test updates identified (test_LoggingManager.py changes needed)
4. .gitignore update trivial (add `logs/` entry)
5. No external dependencies required (Python stdlib sufficient)
6. Backward compatibility maintained (setup_logger signature unchanged)

**Open Questions Resolved:**
- Keep max_file_size/backup_count parameters for backward compatibility
- Hardcode max_lines=500, max_files=50 (no configurability needed)
- Use logger name for folder structure (Features 2-7 ensure consistency)
- Use `logs/` in .gitignore (standard folder exclusion pattern)

**Next Steps:**
1. Draft spec.md with requirements derived from research
2. Create checklist.md with questions for user
3. Run Validation Loop (Gate 1: Research Completeness Audit)
