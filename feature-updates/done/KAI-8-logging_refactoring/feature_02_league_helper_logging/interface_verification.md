# Interface Verification: league_helper_logging

**Purpose:** Document ALL external interfaces verified from source code before implementation

**Verification Date:** 2026-02-08 18:20

---

## Interface 1: setup_logger()

**Source:** utils/LoggingManager.py:190-208

**Signature:**
```python
def setup_logger(name: str,
                level: Union[str, int] = 'INFO',
                log_to_file: bool = False,
                log_file_path: Optional[Union[str, Path]] = None,
                log_format: str = 'standard',
                enable_console: bool = True,
                max_file_size: int = 10 * 1024 * 1024,
                backup_count: int = 5) -> logging.Logger
```

**Parameters:**
- `name` (str): Logger name (required)
- `level` (Union[str, int]): Log level (default='INFO')
  - Accepts: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' or numeric levels
- `log_to_file` (bool): Enable file logging (default=False)
  - ✅ This is what Task 4 will wire to args.enable_log_file
- `log_file_path` (Optional[Union[str, Path]]): Log file path (default=None)
  - None = auto-generate path (Feature 01 behavior)
  - ✅ Task 4 will pass None for auto-generation
- `log_format` (str): Format style (default='standard')
  - Options: 'detailed', 'standard', 'simple'
- `enable_console` (bool): Enable console logging (default=True)
- `max_file_size` (int): Max file size before rotation (default=10MB)
- `backup_count` (int): Max backup files (default=5)

**Returns:**
- logging.Logger: Configured logger instance
  - ✅ Feature 02 doesn't need return value but it's available

**Current Usage (LeagueHelperManager.py:205):**
```python
setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, constants.LOGGING_TO_FILE, constants.LOGGING_FILE, constants.LOGGING_FORMAT)
```

**After Task 4 (implementation_plan.md assumption):**
```python
logger = setup_logger(
    constants.LOG_NAME,
    constants.LOGGING_LEVEL,
    log_to_file=args.enable_log_file,  # NEW: CLI flag
    log_file_path=None,  # NEW: Auto-generate
    log_format=constants.LOGGING_FORMAT
)
```

**Verified:** ✅ Interface matches implementation_plan.md Task 4 assumptions

---

## Interface 2: subprocess.run()

**Source:** Python stdlib subprocess module

**Signature:**
```python
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None,
               capture_output=False, shell=False, cwd=None, timeout=None,
               check=False, encoding=None, errors=None, text=None, env=None,
               universal_newlines=None, **other_popen_kwargs)
```

**Current Usage (run_league_helper.py:48-52):**
```python
result = subprocess.run([
    sys.executable,              # Python interpreter
    str(league_helper_script),   # LeagueHelperManager.py path
    DATA_FOLDER                  # Data folder argument
], check=True)
```

**After Task 2 (implementation_plan.md assumption):**
```python
result = subprocess.run([
    sys.executable,
    str(league_helper_script),
    DATA_FOLDER
] + sys.argv[1:],  # NEW: Forward all CLI args
check=True)
```

**Verified:** ✅ Interface matches implementation_plan.md Task 2 assumptions

---

## Interface 3: argparse.ArgumentParser

**Source:** Python stdlib argparse module

**Usage Pattern (from Task 1, 3 assumptions):**
```python
import argparse

parser = argparse.ArgumentParser(description="Fantasy Football League Helper")
parser.add_argument(
    '--enable-log-file',
    action='store_true',  # Boolean flag (no value needed)
    default=False,        # Default to OFF
    help='Enable file logging (logs written to logs/league_helper/)'
)
args = parser.parse_args()

# Access flag value
if args.enable_log_file:
    # File logging enabled
```

**Verified:** ✅ Standard argparse pattern - no interface assumptions to verify

---

## Interface 4: league_helper/constants.py

**Source:** league_helper/constants.py:24-28

**Current Constants:**
```python
LOGGING_LEVEL = 'INFO'          # Will be RETAINED (used in Task 4)
LOGGING_TO_FILE = False         # Will be DELETED (Task 12)
LOG_NAME = "league_helper"      # Will be RETAINED (used in Task 4)
LOGGING_FILE = './data/log.txt' # Will be DELETED (Task 12)
LOGGING_FORMAT = 'detailed'     # Will be RETAINED (used in Task 4)
```

**After Task 12:**
```python
LOGGING_LEVEL = 'INFO'
LOG_NAME = "league_helper"
LOGGING_FORMAT = 'detailed'
# LOGGING_TO_FILE removed - replaced by --enable-log-file CLI flag
# LOGGING_FILE removed - Feature 01 auto-generates paths
```

**Verified:** ✅ Constants match implementation_plan.md assumptions
- Task 4 uses: LOG_NAME, LOGGING_LEVEL, LOGGING_FORMAT
- Task 12 deletes: LOGGING_TO_FILE, LOGGING_FILE

---

## Verification Summary

**Total Interfaces Verified:** 4
- setup_logger(): ✅ VERIFIED (utils/LoggingManager.py:190)
- subprocess.run(): ✅ VERIFIED (stdlib)
- argparse.ArgumentParser: ✅ VERIFIED (stdlib, standard pattern)
- constants: ✅ VERIFIED (league_helper/constants.py:24-28)

**Mismatches Found:** 0
**Assumptions Confirmed:** 4/4

**Ready for Implementation:** ✅ YES

---

*Last updated: 2026-02-08 18:20*
