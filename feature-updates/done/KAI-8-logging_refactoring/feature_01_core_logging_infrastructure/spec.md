# Feature Specification: core_logging_infrastructure

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 01
**Created:** 2026-02-06
**Last Updated:** 2026-02-06

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 1: core_logging_infrastructure**

**Purpose:** Custom LineBasedRotatingHandler, centralized logs/ folder structure, 500-line rotation, max 50 files cleanup, .gitignore update

**Scope:**
- Custom LineBasedRotatingHandler (subclass logging.FileHandler)
- LoggingManager.py integration (modify setup_logger())
- logs/{script_name}/ folder structure with auto-creation
- Timestamped filenames: {script_name}-{YYYYMMDD_HHMMSS}.log
- 500-line rotation with eager counter
- Max 50 files per subfolder with oldest-file deletion
- .gitignore update to exclude logs/ folder
- Unit tests for new handler

**Dependencies:** None (foundation feature)

### Relevant Discovery Decisions

- **Solution Approach:** Custom LineBasedRotatingHandler with eager counter (in-memory line tracking)
- **Key Constraints:**
  - Must support 500-line cap per file
  - Max 50 files per subfolder with automatic oldest-file deletion
  - Counter resets on script restart (new timestamped file each run)
  - Must integrate with existing LoggingManager.py without breaking backward compatibility
- **Implementation Order:** Feature 1 is foundation - must be completed before Features 2-7

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q1: Timestamp format | Full timestamp YYYYMMDD_HHMMSS (Option B) | Log filenames use precise timestamps supporting multiple logs per day |
| Q2: Line-based rotation approach | Eager - maintain counter in memory (Option B) | Handler tracks line count in memory for better performance |
| Q4: CLI flag default | File logging OFF by default, --enable-log-file flag (Option A) | LoggingManager setup_logger() needs enable_log_file parameter |
| Q7: Counter persistence | Counter resets on restart (new file per run) | Simpler implementation - no persistent state needed |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 2 identified no built-in line-based rotation handler in Python logging - custom handler required
- **Based on User Answer:** Q1 (full timestamps), Q2 (eager counter), Q7 (counter reset) shaped handler design
- **Based on Finding:** Iteration 6 defined LoggingManager integration approach - modify setup_logger() to instantiate LineBasedRotatingHandler when enable_log_file=True

---

## Feature Overview

**What:** Foundation logging infrastructure providing line-based rotation, centralized folder structure, and automated cleanup

**Why:** Enables all 6 scripts to use improved logging with user control, prevents disk space bloat, provides better log organization

**Who:** All Fantasy Football Helper scripts (league_helper, player-data-fetcher, accuracy_sim, win_rate_sim, historical_data_compiler, schedule_fetcher) and their end users

---

## Functional Requirements

**Source:** Epic requirement + Discovery Q1, Q2, Q7 + RESEARCH_NOTES.md

### Requirement 1: Line-Based Log Rotation

**Source:** Epic requirement "500-line cap per file"

**Description:**
LineBasedRotatingHandler must rotate log files based on line count (not file size). When a log file reaches 500 lines, the handler closes the current file and creates a new timestamped file. The line counter resets to 0 for each new file and does NOT persist across script restarts.

**Acceptance Criteria:**
- ✅ Log file rotation triggers when line count reaches 500 (not before)
- ✅ Line counter starts at 0 for new files
- ✅ Line counter increments by 1 for each log record emitted
- ✅ Line counter resets to 0 after rotation
- ✅ Line counter does NOT persist across script restarts (each script run starts at 0)
- ✅ Rotation creates new timestamped file (does NOT rename existing file to .1, .2, etc.)
- ✅ Old log file remains intact after rotation (not overwritten)

**Example:**
```
Script emits 750 log messages:
- Lines 1-500 written to logs/league_helper/league_helper-20260206_143522.log
- Rotation triggered at line 500
- Lines 501-750 written to logs/league_helper/league_helper-20260206_143745.log
- Counter reset to 0 after rotation
```

**User Answer:** Q2 (eager counter in memory), Q7 (counter resets on restart)

---

### Requirement 2: Centralized Folder Structure

**Source:** Epic requirement "root-level logs/ folder with script-specific subfolders"

**Description:**
All log files must be organized in a centralized `logs/` folder at project root, with script-specific subfolders (e.g., `logs/league_helper/`, `logs/accuracy_simulation/`). The handler automatically creates the folder structure if it doesn't exist.

**Acceptance Criteria:**
- ✅ Root logs/ folder created at project root (not in simulation/, utils/, etc.)
- ✅ Script-specific subfolders created using logger name (logs/{logger_name}/)
- ✅ Example folder names: logs/league_helper/, logs/accuracy_simulation/, logs/simulation/ (for win_rate_sim)
- ✅ Folders created automatically using Path.mkdir(parents=True, exist_ok=True)
- ✅ No error if folder already exists (exist_ok=True)
- ✅ Parent folders created if missing (parents=True)

**Example:**
```
Project structure before:
/home/user/FantasyFootballHelperScriptsRefactored/
├── utils/
├── league_helper/
└── simulation/

Project structure after:
/home/user/FantasyFootballHelperScriptsRefactored/
├── logs/                                    # NEW: Root logs folder
│   ├── league_helper/                       # NEW: Script-specific subfolders
│   │   ├── league_helper-20260206_143522.log
│   │   └── league_helper-20260206_144105.log
│   ├── accuracy_simulation/
│   │   └── accuracy_simulation-20260206_090000.log
│   ├── simulation/
│   │   └── simulation-20260206_100000.log
│   └── ... (other script folders)
├── utils/
├── league_helper/
└── simulation/
```

**User Answer:** Epic requirement (no user question needed)

---

### Requirement 3: Timestamped Log Filenames

**Source:** Epic requirement "timestamped .log files" + Discovery Q1

**Description:**
Log filenames must use full timestamp format `{script_name}-{YYYYMMDD_HHMMSS}.log` (not daily YYYYMMDD format). This supports multiple log files per day and provides precise time tracking.

**Acceptance Criteria:**
- ✅ Filename format: {script_name}-{YYYYMMDD_HHMMSS}.log
- ✅ Script name matches logger name (e.g., "league_helper")
- ✅ Separator between name and timestamp is hyphen (not underscore)
- ✅ Timestamp format: YYYYMMDD_HHMMSS (8 digits + underscore + 6 digits)
- ✅ Example: league_helper-20260206_143522.log
- ✅ File extension: .log (lowercase)

**Example:**
```
# Valid filenames:
league_helper-20260206_143522.log
accuracy_simulation-20260206_090000.log
simulation-20260206_100000.log

# Invalid filenames (old format):
league_helper_20260206.log          # Missing time, using underscore
league_helper-20260206.log          # Missing time component
PlayerManager_20260206.log          # Old format (daily rotation)
```

**User Answer:** Q1 (full timestamp YYYYMMDD_HHMMSS, not daily YYYYMMDD)

---

### Requirement 4: Automated Cleanup (Max 50 Files)

**Source:** Epic requirement "max 50 logs per folder, auto-delete oldest"

**Description:**
Each script-specific subfolder can contain maximum 50 log files. When rotation creates a new file and the folder already contains 50 files, the handler deletes the oldest file(s) to maintain the 50-file limit. Age determination uses file modification time.

**Acceptance Criteria:**
- ✅ Max 50 log files per script subfolder (not 50 total across all folders)
- ✅ Cleanup triggered AFTER rotation (before opening new file)
- ✅ Oldest files determined by modification time (st_mtime)
- ✅ Multiple files deleted if needed (e.g., if 55 files exist, delete 5 oldest)
- ✅ Cleanup continues even if file deletion fails (e.g., permission denied)
- ✅ Only .log files counted (ignore other file types)
- ✅ Files sorted oldest-first before deletion

**Example:**
```
Scenario: logs/league_helper/ contains 50 files
- league_helper-20260101_100000.log (oldest)
- league_helper-20260101_103000.log
- ...
- league_helper-20260206_143522.log (newest, #50)

Script emits 500 more lines:
- Rotation triggered
- New file created: league_helper-20260206_143745.log
- Cleanup runs: 51 files exist (> 50)
- league_helper-20260101_100000.log deleted (oldest)
- Result: 50 files remain

Scenario: Folder contains 55 files (manually added):
- Cleanup runs
- 5 oldest files deleted
- Result: 50 files remain
```

**User Answer:** Epic requirement (no user question needed)

---

### Requirement 5: LoggingManager Integration

**Source:** Discovery Iteration 6 (integration approach)

**Description:**
Modify `LoggingManager.setup_logger()` to instantiate `LineBasedRotatingHandler` instead of `RotatingFileHandler` when `log_to_file=True`. Maintain backward compatibility with existing callers (setup_logger signature unchanged).

**Acceptance Criteria:**
- ✅ Replace RotatingFileHandler instantiation (utils/LoggingManager.py lines 107-115) with LineBasedRotatingHandler
- ✅ Pass parameters: log_file_path, max_lines=500, max_files=50, encoding='utf-8'
- ✅ Import LineBasedRotatingHandler from utils.LineBasedRotatingHandler
- ✅ setup_logger() signature unchanged (backward compatibility)
- ✅ max_file_size and backup_count parameters remain in signature (unused, for backward compatibility)
- ✅ Existing callers work without modification (e.g., run_accuracy_simulation.py)

**Example:**
```python
# Current code (utils/LoggingManager.py lines 107-115):
file_handler = logging.handlers.RotatingFileHandler(
    log_file_path,
    maxBytes=max_file_size,
    backupCount=backup_count,
    encoding='utf-8'
)

# New code:
from utils.LineBasedRotatingHandler import LineBasedRotatingHandler

file_handler = LineBasedRotatingHandler(
    log_file_path,
    max_lines=500,  # Hardcoded constant
    max_files=50,   # Hardcoded constant
    encoding='utf-8'
)
```

**User Answer:** Discovery Iteration 6 (LoggingManager is single integration point)

---

### Requirement 6: Updated Log File Path Generation

**Source:** Discovery Q1 (timestamp format change) + RESEARCH_NOTES.md

**Description:**
Modify `LoggingManager._generate_log_file_path()` to generate paths in new format: `logs/{logger_name}/{logger_name}-{YYYYMMDD_HHMMSS}.log` (not `{logger_name}_{YYYYMMDD}.log`).

**Acceptance Criteria:**
- ✅ Create script-specific subfolder: logs/{logger_name}/
- ✅ Generate filename: {logger_name}-{YYYYMMDD_HHMMSS}.log
- ✅ Use hyphen separator (not underscore)
- ✅ Timestamp includes time component (HHMMSS)
- ✅ Return full path: logs/{logger_name}/{logger_name}-{timestamp}.log

**Example:**
```python
# Current implementation (utils/LoggingManager.py lines 134-142):
def _generate_log_file_path(self, log_path: str, logger_name: str) -> Path:
    timestamp = datetime.now().strftime('%Y%m%d')
    filename = f"{logger_name}_{timestamp}.log"
    return log_path / filename

# New implementation:
def _generate_log_file_path(self, log_path: Path, logger_name: str) -> Path:
    log_dir = log_path / logger_name  # Script-specific subfolder
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Full timestamp
    filename = f"{logger_name}-{timestamp}.log"  # Hyphen separator
    return log_dir / filename
```

**User Answer:** Q1 (full timestamp YYYYMMDD_HHMMSS)

---

### Requirement 7: .gitignore Update

**Source:** Epic requirement ".gitignore update for logs folder"

**Description:**
Add `logs/` entry to `.gitignore` to exclude all log files from version control. This prevents accidental commits of potentially large or sensitive log data.

**Acceptance Criteria:**
- ✅ Add `logs/` entry to .gitignore
- ✅ Entry excludes entire logs/ folder and all contents
- ✅ Entry positioned at line 71 (after *.log pattern for logical grouping)
- ✅ No conflicts with existing patterns (logs/ takes precedence over *.log)

**User Decision (Q5):** Add at line 71 (after *.log) - logical grouping with log-related patterns

**Example:**
```gitignore
# Current .gitignore (line 70):
*.log

# After update (add below line 70):
*.log
logs/
```

**User Answer:** Epic requirement (no user question needed)

---

## Technical Requirements

**Source:** RESEARCH_NOTES.md (LineBasedRotatingHandler Design section)

### Class Hierarchy

```
logging.Handler (base, Python stdlib)
  ↓
logging.StreamHandler (Python stdlib)
  ↓
logging.FileHandler (Python stdlib, parent class)
  ↓
LineBasedRotatingHandler (NEW, custom implementation)
```

**Rationale:** Subclass `logging.FileHandler` (not `RotatingFileHandler`) because:
- FileHandler provides file I/O primitives (emit, _open, close)
- RotatingFileHandler's size-based rotation logic doesn't apply
- Cleaner to implement line-based logic from scratch

---

### Algorithms

#### Line Counting Algorithm

**Purpose:** Track number of lines written to current log file

**Data Structure:**
- `self.line_count`: int (instance variable)
- Initialized to 0 in `__init__()`
- Incremented after each successful `emit()`
- Reset to 0 after `doRollover()`

**Pseudocode:**
```
def emit(record):
    if line_count >= max_lines:
        doRollover()  # Rotate, reset counter

    write_record_to_file(record)
    line_count += 1
```

---

#### Rotation Algorithm

**Purpose:** Close current file, create new timestamped file, cleanup old files

**Trigger:** `shouldRollover()` returns True when `line_count >= max_lines`

**Steps:**
1. Close current file stream
2. Generate new timestamped filename
3. Run cleanup (_cleanup_old_files)
4. Open new file stream
5. Reset line_count to 0

**Pseudocode:**
```
def doRollover():
    if stream_open:
        stream.close()

    baseFilename = generate_new_filename()  # {script}-{timestamp}.log
    cleanup_old_files()                    # Delete oldest if >50 files
    stream = open(baseFilename)
    line_count = 0
```

---

#### Cleanup Algorithm

**Purpose:** Maintain max 50 files per script subfolder by deleting oldest

**Trigger:** Called during `doRollover()` (after rotation, before opening new file)

**Steps:**
1. Get all .log files in folder (e.g., logs/league_helper/)
2. Sort by modification time (oldest first)
3. While count > max_files (50):
   - Delete oldest file
   - Remove from list
4. Ignore errors (file may be locked/deleted externally)

**Pseudocode:**
```
def cleanup_old_files():
    folder = parent_directory(baseFilename)  # logs/league_helper/
    files = folder.glob('*.log')
    files = sorted(files, key=modification_time)

    while len(files) > max_files:
        oldest = files.pop(0)
        try:
            delete(oldest)
        except OSError:
            pass  # Ignore errors, continue cleanup
```

---

#### Timestamp Generation Algorithm

**Purpose:** Generate unique timestamped filenames for rotated log files

**Format:** `{script_name}-{YYYYMMDD_HHMMSS}.log`

**Implementation:**
```python
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"{script_name}-{timestamp}.log"
```

**Example Outputs:**
- `league_helper-20260206_143522.log`
- `accuracy_simulation-20260206_090000.log`
- `simulation-20260206_100000.log`

**Uniqueness:** Timestamp includes seconds, so rotation within same second creates duplicate filename (rare, acceptable trade-off)

---

### Data Structures

#### LineBasedRotatingHandler Instance Variables

| Variable | Type | Purpose | Initial Value | Reset Condition |
|----------|------|---------|---------------|-----------------|
| `baseFilename` | str | Current log file path | Constructor arg | After rotation (new filename) |
| `max_lines` | int | Max lines per file | Constructor arg (500) | Never |
| `max_files` | int | Max files per folder | Constructor arg (50) | Never |
| `line_count` | int | Lines written to current file | 0 | After rotation |
| `stream` | TextIOWrapper | Open file handle | None | After rotation (new file) |
| `mode` | str | File open mode | Constructor arg ('a') | Never |
| `encoding` | str | File encoding | Constructor arg ('utf-8') | Never |
| `delay` | bool | Delay file opening | Constructor arg (False) | Never |

---

### Interfaces

#### LineBasedRotatingHandler.__init__()

```python
def __init__(
    self,
    filename: str,
    mode: str = 'a',
    max_lines: int = 500,
    max_files: int = 50,
    encoding: Optional[str] = None,
    delay: bool = False
) -> None:
    """
    Initialize line-based rotating file handler.

    Args:
        filename: Log file path (e.g., logs/league_helper/league_helper-20260206_143522.log)
        mode: File open mode ('a' for append, 'w' for write)
        max_lines: Maximum lines per file before rotation (default 500)
        max_files: Maximum files per folder before cleanup (default 50)
        encoding: File encoding (default None = platform default, recommend 'utf-8')
        delay: Delay file opening until first emit (default False)
    """
```

**Call Site:** `LoggingManager.setup_logger()` (utils/LoggingManager.py line ~107)

**Example:**
```python
handler = LineBasedRotatingHandler(
    'logs/league_helper/league_helper-20260206_143522.log',
    max_lines=500,
    max_files=50,
    encoding='utf-8'
)
```

---

#### LineBasedRotatingHandler.emit()

```python
def emit(self, record: logging.LogRecord) -> None:
    """
    Emit a log record, with line-based rotation.

    Steps:
    1. Check if rotation needed (shouldRollover)
    2. If needed, perform rotation (doRollover)
    3. Write record to file (parent FileHandler.emit)
    4. Increment line counter

    Args:
        record: LogRecord to emit

    Raises:
        Catches all exceptions via handleError()
    """
```

**Caller:** Python logging framework (automatic)

---

#### LineBasedRotatingHandler.shouldRollover()

```python
def shouldRollover(self, record: logging.LogRecord) -> bool:
    """
    Determine if rollover should occur based on line count.

    Args:
        record: LogRecord about to be emitted (unused in line-based rotation)

    Returns:
        True if line_count >= max_lines, False otherwise
    """
```

**Caller:** `emit()` method (before writing record)

---

#### LineBasedRotatingHandler.doRollover()

```python
def doRollover(self) -> None:
    """
    Perform file rotation.

    Steps:
    1. Close current stream
    2. Generate new timestamped filename
    3. Cleanup old files (if >max_files)
    4. Open new file stream
    5. Reset line counter

    Side Effects:
    - Updates self.baseFilename
    - Updates self.stream
    - Resets self.line_count to 0
    - May delete old log files
    """
```

**Caller:** `emit()` method (when shouldRollover returns True)

---

#### LineBasedRotatingHandler._generate_new_filename()

```python
def _generate_new_filename(self) -> str:
    """
    Generate new timestamped filename for rotation.

    Format: {script_name}-{YYYYMMDD_HHMMSS}.log
    Example: logs/league_helper/league_helper-20260206_143522.log

    Returns:
        str: Full path to new log file

    Algorithm:
        1. Extract folder from current baseFilename
        2. Extract script_name from folder name (assumes folder = logs/{script_name}/)
        3. Generate timestamp (YYYYMMDD_HHMMSS)
        4. Construct filename: {script_name}-{timestamp}.log
        5. Return full path: {folder}/{filename}
    """
```

**Caller:** `doRollover()` method (during rotation)

---

#### LineBasedRotatingHandler._cleanup_old_files()

```python
def _cleanup_old_files(self) -> None:
    """
    Delete oldest log files if folder exceeds max_files limit.

    Steps:
    1. Get folder from current baseFilename
    2. Scan for all .log files in folder
    3. Sort by modification time (oldest first)
    4. While count > max_files, delete oldest
    5. Ignore errors (file may be locked/deleted)

    Side Effects:
    - May delete log files from disk
    - Catches and ignores OSError exceptions
    """
```

**Caller:** `doRollover()` method (after creating new filename, before opening)

---

## Integration Points

### Integration with Features 2-7 (All Script Logging Features)

**Direction:** This feature provides TO all script logging features

**Data Passed:**
- **Class:** `LineBasedRotatingHandler` (available via import from utils.LineBasedRotatingHandler)
- **API:** Modified `setup_logger()` function (existing signature, new behavior)
- **Folder Structure:** `logs/{script_name}/` folders (auto-created by handler)

**Interface:**

Features 2-7 call `setup_logger()` with same signature as before:
```python
from utils.LoggingManager import setup_logger

logger = setup_logger(
    name="league_helper",           # Script name (used for folder structure)
    level="INFO",                     # Log level
    log_to_file=True,                # Enable file logging (CLI-driven in Features 2-7)
    log_file_path=None,              # Auto-generated by LoggingManager
    log_format="standard"            # Format style
)
# Result: LineBasedRotatingHandler created, logs to logs/league_helper/league_helper-{timestamp}.log
```

**Example Flow:**
```
Feature 01 (core infrastructure)
  ↓ provides LineBasedRotatingHandler
  ↓ provides modified setup_logger() that instantiates LineBasedRotatingHandler
  ↓ provides logs/{script_name}/ folder structure

Features 02-07 (per-script logging)
  ↓ call setup_logger(name, level, log_to_file=args.enable_log_file, ...)
  ↓ CLI flag --enable-log-file controls log_to_file parameter

End Users
  ↓ run script with --enable-log-file flag
  ↓ logs written to logs/{script_name}/ folder
  ↓ 500-line rotation automatic
  ↓ max 50 files enforced automatically
```

**Key Contracts:**
1. **Logger name = folder name:** Features 2-7 must pass consistent logger name (e.g., "league_helper" not "LeagueHelper" or "lh")
   - **User Decision (DC1):** Documented as Features 2-7 responsibility (no enforcement in Feature 1)
2. **log_file_path=None:** Features 2-7 should NOT specify custom paths (let LoggingManager generate)
3. **log_to_file driven by CLI:** Features 2-7 wire --enable-log-file flag to log_to_file parameter

---

### Integration with Python Logging Framework

**Direction:** LineBasedRotatingHandler integrates WITH Python logging module

**Parent Class:** `logging.FileHandler`

**Inherited Behavior:**
- File I/O operations (_open, close, flush)
- Error handling (handleError)
- Formatter application (setFormatter, format)
- Level filtering (setLevel, filter)

**Overridden Methods:**
- `emit()` - Add line counting and rotation logic
- `shouldRollover()` - Line-based check (not size-based)
- `doRollover()` - Timestamped file creation + cleanup (not sequential renaming)

**Python Logging Call Chain:**
```
logger.info("message")
  ↓ Python logging framework
Logger.handle(record)
  ↓
Handler.handle(record)
  ↓
LineBasedRotatingHandler.emit(record)  # Our custom logic
  ↓
FileHandler.emit(record)               # Parent class (write to file)
  ↓
StreamHandler.emit(record)             # Grandparent (format record)
```

---

### File System Integration

**Direction:** LineBasedRotatingHandler interacts WITH file system

**Operations:**
- **Create folders:** `Path.mkdir(parents=True, exist_ok=True)` - logs/{script_name}/
- **Create files:** `open(filename, mode='a', encoding='utf-8')` - New log files
- **Delete files:** `Path.unlink()` - Old log files during cleanup
- **Scan folder:** `Path.glob('*.log')` - Find all log files for cleanup
- **Get file stats:** `Path.stat().st_mtime` - Modification time for sorting

**Error Handling:**
- **Permission denied (mkdir):** Caught by logging.FileHandler.handleError(), logs error to stderr
- **Permission denied (unlink):** Caught in _cleanup_old_files(), ignored (cleanup continues)
- **Disk full:** Caught by logging.FileHandler.handleError(), logs error to stderr
- **File locked:** Caught in _cleanup_old_files(), ignored (file skipped)

---

## Error Handling

**Source:** RESEARCH_NOTES.md (Edge Cases and Error Handling section)

### Error Scenario 1: Folder Creation Failure

**Trigger:** Permission denied or disk full when creating logs/{script_name}/ folder

**Handling:**
- `Path.mkdir(parents=True, exist_ok=True)` raises `OSError`
- Caught by `logging.FileHandler.handleError(record)`
- Error logged to stderr (not the log file, since file can't be created)
- Record not written (logging continues to console if enabled)

**User Impact:** Log messages not written to file (console logging unaffected)

**Mitigation:** Document requirement that user needs write permissions to project root

**Code:**
```python
# No explicit try/except needed - FileHandler.handleError() handles all exceptions
def emit(self, record):
    try:
        # ... emit logic ...
        logging.FileHandler.emit(self, record)  # May raise OSError
    except Exception:
        self.handleError(record)  # Parent class handles error
```

---

### Error Scenario 2: File Deletion Failure (_cleanup_old_files)

**Trigger:** File locked by another process or permission denied when deleting old logs

**Handling:**
- `Path.unlink()` raises `OSError`
- Caught explicitly in `_cleanup_old_files()`
- Error ignored (cleanup continues with next file)
- May result in folder exceeding 50-file limit temporarily

**User Impact:** Folder may contain 51-55 files temporarily (not critical, cleanup retries on next rotation)

**Mitigation:** Best-effort cleanup (tolerate failures)

**Code:**
```python
def _cleanup_old_files(self):
    log_files = sorted(log_dir.glob('*.log'), key=lambda p: p.stat().st_mtime)

    while len(log_files) > self.max_files:
        oldest = log_files.pop(0)
        try:
            oldest.unlink()  # May raise OSError
        except OSError:
            pass  # Ignore error, continue cleanup
```

---

### Error Scenario 3: Disk Full During Write

**Trigger:** Disk space exhausted when writing log record

**Handling:**
- `FileHandler.emit()` write operation raises `OSError`
- Caught by `logging.FileHandler.handleError(record)`
- Error logged to stderr
- Record not written (logging continues on next emit if space freed)

**User Impact:** Some log messages may be lost

**Mitigation:** User responsible for disk space management (standard logging behavior)

**Code:**
```python
# No explicit handling needed - FileHandler.handleError() handles this
```

---

### Error Scenario 4: Invalid Logger Name (Filename Special Characters)

**Trigger:** Logger name contains special characters (e.g., "../evil", "test:name")

**Handling:**
- `Path()` constructor handles path normalization
- Folder created as `logs/{normalized_name}/`
- Filenames sanitized by Path operations (invalid chars replaced/removed)

**User Impact:** Folder name may differ from logger name

**Mitigation:** Document recommendation that logger names should be filesystem-safe (alphanumeric + underscore/hyphen)

**Example:**
```python
# Logger name: "test:name" (colon invalid on Windows)
# Folder created: logs/testname/ (colon stripped)
# Filename: testname-20260206_143522.log
```

---

### Error Scenario 5: Rotation During Active Write (Multithreading)

**Trigger:** Two threads call `emit()` simultaneously, both trigger rotation

**Handling:**
- Python GIL (Global Interpreter Lock) prevents true concurrent execution
- First thread completes rotation, second thread uses new file
- Line counter may be slightly inaccurate (race condition)

**User Impact:** Minimal (may have 501-505 lines in file instead of exactly 500)

**Mitigation:** Acceptable trade-off (perfect accuracy not required, GIL provides sufficient protection)

**Note:** Python logging module is NOT thread-safe by default (standard limitation)

---

### Error Scenario 6: Timestamp Collision (Rotation Within Same Second)

**Trigger:** Script emits >500 lines within 1 second, multiple rotations occur

**Handling:**
- Timestamp format includes seconds (not milliseconds)
- Second rotation creates filename with same timestamp
- `open(filename, mode='a')` appends to existing file (does not overwrite)

**User Impact:** Two rotation files merged (not critical, rare scenario)

**Mitigation:** Accept trade-off (milliseconds not needed for typical usage)

**Example:**
```
# Rotation 1 at 14:35:22.123
# Creates: league_helper-20260206_143522.log

# Rotation 2 at 14:35:22.987 (same second)
# Creates: league_helper-20260206_143522.log (same filename)
# Result: Appends to existing file (both rotations in one file)
```

---

### Error Scenario 7: Line Counter Overflow

**Trigger:** Theoretical edge case where line_count exceeds int max value

**Handling:**
- Python integers have arbitrary precision (no overflow)
- Counter resets at 500 lines (never grows large)

**User Impact:** None (impossible scenario)

**Mitigation:** None needed

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

---

## Non-Functional Requirements

**Performance:**
- ✅ Line counter operations must be O(1) (in-memory integer increment, no file I/O)
- ✅ Rotation operations must complete in <100ms (close file, create new file, cleanup)
- ✅ Cleanup operations must scale linearly with file count O(n) where n = number of .log files
  - **User Decision (DC3):** No optimization needed (high-frequency rotation unrealistic for fantasy football scripts)
- ✅ No performance degradation for console-only logging (log_to_file=False)
- ✅ Minimal overhead per emit() call (<1ms additional latency vs RotatingFileHandler)

**Scalability:**
- ✅ Support folders with 50 log files without performance degradation
- ✅ Support log files with 500 lines without performance impact (eager counter, not lazy counting)
- ✅ Support multiple scripts logging concurrently (separate subfolders prevent conflicts)
- ✅ Handle high-frequency logging (1000+ messages/second) without losing records

**Reliability:**
- ✅ Zero data loss during rotation (all records written before file closed)
- ✅ Graceful degradation if cleanup fails (continue logging even if old files can't be deleted)
- ✅ Atomic rotation operations (no partial rotations or corrupted files)
- ✅ Self-healing behavior (auto-create folders if deleted during runtime)

**Maintainability:**
- ✅ Must follow project coding standards (CODING_STANDARDS.md)
- ✅ Must maintain backward compatibility with existing LoggingManager usage
- ✅ Must use type hints for all method signatures
- ✅ Must include comprehensive docstrings (class, methods, attributes)
- ✅ Must include inline comments for complex logic (rotation, cleanup algorithms)
- ✅ Must follow logging module naming conventions (shouldRollover, doRollover)

**Testability:**
- ✅ All methods must be testable in isolation (unit tests)
- ✅ Rotation logic must be testable without waiting for 500 records (mock line_count)
- ✅ Cleanup logic must be testable with controlled file sets (tmp_path fixture)
- ✅ 100% unit test coverage required for LineBasedRotatingHandler class

**User Decision (Q8):** Test coverage focused on happy path + critical errors (rotation, cleanup, permissions). Rare edge cases (timestamp collision, folder deletion) documented but not tested.

**Compatibility:**
- ✅ Python 3.8+ compatibility (use only stdlib features available in Python 3.8)
- ✅ Cross-platform compatibility (Windows, macOS, Linux) - use pathlib.Path for all file operations
  - **User Decision (DC2):** pathlib.Path confirmed sufficient for cross-platform support
- ✅ Backward compatibility with existing setup_logger() callers (no signature changes)

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Script-specific CLI integration (Features 2-7 handle this)
- Log quality improvements to existing debug/info calls (Features 2-7 handle this)
- Console logging changes (only affects file logging)
- Log format changes (keeping existing formats)
- Configurable line limits per script (hardcoded 500 for all scripts)
- Log compression for archived logs
- Persistent line counter across restarts (counter resets each run)

---

## Open Questions

{To be populated during S2 deep dive - questions will be tracked in checklist.md}

No open questions currently - to be identified during S2 research phase.

---

## Implementation Notes

**Source:** RESEARCH_NOTES.md + Discovery findings

### Design Decisions from Discovery

1. **Parent Class Choice:**
   - ✅ Subclass `logging.FileHandler` (not `RotatingFileHandler`)
   - **Rationale:** RotatingFileHandler's size-based rotation logic doesn't apply; cleaner to implement line-based logic from scratch
   - **Alternative Rejected:** Wrapping RotatingFileHandler would be more complex (converting lines to approximate bytes)

2. **Line Counter Storage:**
   - ✅ In-memory instance variable (`self.line_count`)
   - ✅ Eager counting (increment after each emit)
   - ✅ No persistence across script restarts
   - **Rationale:** User requirement Q7 (counter resets on restart), simpler implementation, aligns with timestamped-file-per-run model
   - **Alternative Rejected:** Persistent counter in file (unnecessary complexity, user doesn't need it)

3. **Rotation Strategy:**
   - ✅ Create new timestamped file on rotation (not sequential renaming)
   - ✅ Keep old files intact (not overwritten)
   - **Rationale:** User requirement Q1 (full timestamps), easier to implement than sequential renaming
   - **Alternative Rejected:** Sequential renaming (log.1, log.2, ...) like RotatingFileHandler (conflicts with timestamp requirement)

4. **Cleanup Strategy:**
   - ✅ Scan folder, sort by modification time, delete oldest
   - ✅ Trigger cleanup after rotation (before opening new file)
   - **Rationale:** Modification time is reliable sort key, cleanup before opening ensures we don't exceed limit
   - **Alternative Rejected:** Cleanup before rotation (may still exceed limit if rotation fails)

5. **Folder Structure:**
   - ✅ Script-specific subfolders (`logs/{logger_name}/`)
   - ✅ Auto-created by handler using `Path.mkdir(parents=True, exist_ok=True)`
   - **Rationale:** User requirement (script-specific subfolders), mkdir handles creation gracefully
   - **Alternative Rejected:** Flat structure (logs/*.log) - hard to manage, cluttered

6. **Timestamp Format:**
   - ✅ `YYYYMMDD_HHMMSS` format (8 digits + underscore + 6 digits)
   - ✅ Hyphen separator between script name and timestamp
   - **Rationale:** User requirement Q1 (full timestamp), hyphen improves readability
   - **Alternative Rejected:** Daily format (YYYYMMDD) - doesn't support multiple logs per day

7. **Hardcoded Constants:**
   - ✅ max_lines = 500 (hardcoded in LoggingManager)
   - ✅ max_files = 50 (hardcoded in LoggingManager)
   - **Rationale:** User specified exact values, no configurability requested
   - **Alternative Rejected:** Configurable parameters - over-engineering, YAGNI
   - **User Decision (Q2):** Hardcode 500/50 - simpler implementation, matches requirements exactly

8. **Backward Compatibility:**
   - ✅ Keep max_file_size and backup_count parameters in setup_logger() signature
   - ✅ Parameters unused by LineBasedRotatingHandler (ignored)
   - **Rationale:** Prevents breaking existing callers (e.g., run_accuracy_simulation.py)
   - **Alternative Rejected:** Remove parameters - breaking change for existing code

---

### Implementation Tips

**File Creation:**
- Use `Path.mkdir(parents=True, exist_ok=True)` for folder creation - handles missing parents and existing folders gracefully
- Use `mode='a'` (append) for file opening - if filename collision occurs, appends instead of overwriting

**Line Counting:**
- Increment `line_count` AFTER successful write (not before) - prevents counter drift if write fails
- Use `self.line_count >= self.max_lines` (not `==`) - handles edge cases where counter may skip values

**Rotation Timing:**
- Call `doRollover()` BEFORE writing record (not after) - ensures we don't exceed 500 lines
- Reset counter in `doRollover()` (not in `emit()`) - keeps rotation logic centralized

**Cleanup Timing:**
- Run `_cleanup_old_files()` in `doRollover()` AFTER setting new filename - ensures new file counted in total
- Use `while` loop (not `if`) for cleanup - handles cases where folder has 55+ files (delete 5+)

**Error Handling:**
- Wrap file operations in try/except within `_cleanup_old_files()` - ignore errors, continue cleanup
- Let `FileHandler.handleError()` handle emit errors - no explicit try/except in emit() needed

**Testing:**
- Use pytest tmp_path fixture for file system tests - provides clean isolated folder per test
- Mock `datetime.now()` for timestamp tests - ensures consistent filenames across test runs
- Test rotation by setting `line_count = 499` manually - avoids emitting 500 records

---

### Gotchas

**Gotcha 1: Timestamp Collision**
- **Issue:** Two rotations within same second create duplicate filename
- **Impact:** Second rotation appends to first rotation's file (merge two rotations)
- **Mitigation:** Acceptable trade-off (rare scenario, milliseconds not needed)

**Gotcha 2: Logger Name Contains Path Separators**
- **Issue:** Logger name like "../evil" or "test/../name" could escape logs/ folder
- **Impact:** Files created outside logs/ folder (security risk)
- **Mitigation:** Document requirement that logger names should be simple alphanumeric strings
- **User Decision (Q4):** No validation - trust internal callers, document in Features 2-7

**Gotcha 3: Folder Deletion During Runtime**
- **Issue:** User deletes logs/{script_name}/ while script running
- **Impact:** Next emit() recreates folder (self-healing behavior)
- **Mitigation:** None needed (automatic recovery)

**Gotcha 4: Multithreading Race Condition**
- **Issue:** Two threads call emit() simultaneously, both increment line_count
- **Impact:** Counter may be off by 1-2 (file may have 502 lines instead of 500)
- **Mitigation:** Acceptable trade-off (Python GIL provides some protection, perfect accuracy not critical)

**Gotcha 5: max_file_size and backup_count Parameters**
- **Issue:** setup_logger() still accepts these parameters but LineBasedRotatingHandler ignores them
- **Impact:** Confusing API (dead parameters)
- **Mitigation:** Keep for backward compatibility, document as unused
- **User Decision (Q1):** Keep parameters - backward compatibility prioritized over API cleanliness

**Gotcha 6: .log File Extension Filter in Cleanup**
- **Issue:** Cleanup only deletes .log files, ignores .log.1, .log.bak, etc.
- **Impact:** Other file types not cleaned up (may exceed 50-file limit)
- **Mitigation:** Document that only .log files managed (acceptable per user requirement)

**Gotcha 7: Modification Time vs Creation Time**
- **Issue:** Some systems don't preserve modification time accurately
- **Impact:** Cleanup may delete wrong files (not oldest)
- **Mitigation:** Use st_mtime (modification time) - reliable on all platforms, good enough for cleanup

**Gotcha 8: File Open Mode 'a' (Append)**
- **Issue:** If rotation creates duplicate filename, mode='a' appends (doesn't overwrite)
- **Impact:** File may contain more than one rotation's data
- **Mitigation:** Feature, not bug (prevents data loss in edge case)
- **User Decision (Q3):** Use append mode - data loss prevention prioritized over strict 500-line limit

---

### Code Organization

**File Structure:**
```
utils/
├── LoggingManager.py         # MODIFY: Replace RotatingFileHandler with LineBasedRotatingHandler
├── LineBasedRotatingHandler.py  # NEW: Custom handler class
└── ...

tests/utils/
├── test_LoggingManager.py             # UPDATE: Change handler type assertions
├── test_LineBasedRotatingHandler.py   # NEW: Comprehensive handler tests
└── ...

.gitignore                    # MODIFY: Add logs/ entry
```

**Import Dependencies:**
```python
# LineBasedRotatingHandler.py
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# LoggingManager.py (additions)
from utils.LineBasedRotatingHandler import LineBasedRotatingHandler
```

---

### Acceptance Criteria Cross-Reference

All functional requirements map to acceptance criteria:

| Requirement | Test Coverage | Implementation Location |
|-------------|---------------|-------------------------|
| Req 1: Line-Based Rotation | test_LineBasedRotatingHandler.py: test_rotation_at_500_lines | LineBasedRotatingHandler.emit(), shouldRollover() |
| Req 2: Centralized Folders | test_LineBasedRotatingHandler.py: test_folder_creation | LineBasedRotatingHandler.__init__, Path.mkdir() |
| Req 3: Timestamped Filenames | test_LineBasedRotatingHandler.py: test_filename_format | LineBasedRotatingHandler._generate_new_filename() |
| Req 4: Automated Cleanup | test_LineBasedRotatingHandler.py: test_cleanup_old_files | LineBasedRotatingHandler._cleanup_old_files() |
| Req 5: LoggingManager Integration | test_LoggingManager.py: test_creates_line_based_handler | LoggingManager.setup_logger() lines 107-115 |
| Req 6: Updated Path Generation | test_LoggingManager.py: test_generate_log_file_path | LoggingManager._generate_log_file_path() |
| Req 7: .gitignore Update | Manual verification | .gitignore line 71 |

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
| 2026-02-06 | Agent | Complete spec draft with all requirements, technical details, algorithms, integration points, error handling, and implementation notes | S2.P1.I1 (Feature-Level Discovery - research complete) |
