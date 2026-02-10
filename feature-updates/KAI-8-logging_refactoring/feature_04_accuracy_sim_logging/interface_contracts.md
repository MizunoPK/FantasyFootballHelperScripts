# Feature 04: accuracy_sim_logging - Verified Interface Contracts

**Part of Epic:** KAI-8-logging_refactoring
**Feature:** accuracy_sim_logging
**Purpose:** Document ALL external interfaces verified from source code
**Verification Date:** 2026-02-09

---

## Interface 1: LoggingManager.setup_logger

**Source:** utils/LoggingManager.py lines 190-208

**Signature:**
```python
def setup_logger(name: str,
                level: Union[str, int] = 'INFO',
                log_to_file: bool = False,
                log_file_path: Optional[Union[str, Path]] = None,
                log_format: str = 'standard',
                enable_console: bool = True,
                max_file_size: int = 10 * 1024 * 1024,  # 10MB
                backup_count: int = 5) -> logging.Logger
```

**Parameters:**
- `name` (str): Logger name - will become folder name (e.g., "accuracy_simulation" → logs/accuracy_simulation/)
- `level` (Union[str, int]): Log level - 'DEBUG', 'INFO', 'WARNING', 'ERROR', or int equivalent (default: 'INFO')
- `log_to_file` (bool): Enable file logging (default: False)
  - **Key:** This is the parameter we wire to --enable-log-file CLI flag
  - **Behavior:** True = file + console, False = console only
- `log_file_path` (Optional[Union[str, Path]]): Path to log file (default: None)
  - **Key:** Should be None to let LoggingManager auto-generate path
  - **Auto-generated format:** logs/{name}/{name}-{YYYYMMDD_HHMMSS}.log
- `log_format` (str): Format style - 'standard' or 'detailed' (default: 'standard')
- `enable_console` (bool): Enable console logging (default: True)
- `max_file_size` (int): Max file size in bytes before rotation (default: 10MB)
- `backup_count` (int): Max backup files to keep (default: 5)

**Returns:**
- `logging.Logger`: Configured logger instance

**Exceptions:**
- None documented (errors logged internally)

**Example Usage (from implementation_plan.md Task 2.1):**
```python
# run_accuracy_simulation.py line 229
setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)

# Parameter mapping:
#   name = "accuracy_simulation" (LOG_NAME constant)
#   level = args.log_level.upper() (CLI argument, default 'info')
#   log_to_file = args.enable_log_file (NEW CLI flag, default False)
#   log_file_path = None (let LoggingManager generate: logs/accuracy_simulation/accuracy_simulation-{timestamp}.log)
#   log_format = "standard" (LOGGING_FORMAT constant)
```

**Verified:** ✅ Interface matches implementation_plan.md Task 2.1 assumptions

**Integration Contracts (Feature 01):**
1. **Logger name = folder name:** "accuracy_simulation" → logs/accuracy_simulation/
2. **log_file_path = None:** Auto-generated path (no hardcoded paths)
3. **log_to_file CLI-driven:** args.enable_log_file controls file logging on/off

---

## Interface 2: LineBasedRotatingHandler

**Source:** utils/LineBasedRotatingHandler.py lines 52-60

**Signature:**
```python
class LineBasedRotatingHandler(FileHandler):
    def __init__(
        self,
        filename: str,
        mode: str = 'a',
        max_lines: int = 500,
        max_files: int = 50,
        encoding: Optional[str] = 'utf-8',
        delay: bool = False
    )
```

**Parameters:**
- `filename` (str): Path to log file
- `mode` (str): File open mode (default: 'a' for append)
- `max_lines` (int): Max lines per file before rotation (default: 500)
- `max_files` (int): Max files per folder before cleanup (default: 50)
- `encoding` (Optional[str]): File encoding (default: 'utf-8')
- `delay` (bool): Delay file opening until first emit (default: False)

**Key Behaviors:**
- **Line-based rotation:** Rotates at 500 lines (not size-based)
- **Automatic cleanup:** Deletes oldest files when folder exceeds 50 files
- **Timestamped filenames:** {script_name}-{YYYYMMDD_HHMMSS}.log (initial) or {script_name}-{YYYYMMDD_HHMMSS_microseconds}.log (rotated)
- **In-memory counter:** Line counter resets on script restart

**Usage in Feature 04:**
- LoggingManager creates LineBasedRotatingHandler internally
- Feature 04 doesn't instantiate handler directly
- Handler used when log_to_file=True and log_file_path=None
- Auto-generated filename: logs/accuracy_simulation/accuracy_simulation-{YYYYMMDD_HHMMSS}.log

**Verified:** ✅ Handler behavior matches expectations (500-line rotation, 50-file max)

---

## Interface 3: Python stdlib logging module

**Source:** Python standard library

**Key Components Used:**
- `logging.Logger`: Logger class returned by setup_logger()
- `logger.debug()`, `logger.info()`, `logger.error()`: Logging methods
- `exc_info=True`: Parameter for ERROR logging with exception traceback

**Example Usage (from implementation_plan.md Tasks 3.x, 4.x, 5.x):**
```python
logger = setup_logger(...)  # Get logger instance

# DEBUG logging
logger.debug(f"Method entry: {method_name} - param1={value1}")
logger.debug(f"Data transformation: before={before_count}, after={after_count}")

# INFO logging
logger.info("Simulation started")
logger.info(f"Results saved to {filepath}")

# ERROR logging
logger.error(f"Failed to load baseline config from {path}", exc_info=True)
```

**Verified:** ✅ Standard library interface (no verification needed)

---

## Verification Summary

**Total Interfaces:** 3
**Verified from Source:** 2 (LoggingManager.setup_logger, LineBasedRotatingHandler)
**Standard Library:** 1 (logging module)

**Mismatches Found:** ZERO
- All implementation_plan.md assumptions match actual source code
- All Feature 01 integration contracts verified
- Ready to proceed with implementation

**Key Findings:**
1. setup_logger() signature unchanged since S5 Gate 23a verification
2. LineBasedRotatingHandler parameters match implementation_plan.md assumptions
3. No interface changes needed in implementation_plan.md

**Next Step:** Proceed to Step 3 (Phase-by-Phase Implementation)

---

**End of Interface Contracts**
