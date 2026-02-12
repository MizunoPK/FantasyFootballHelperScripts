## Feature 07: schedule_fetcher_logging - Verified Interface Contracts

**Purpose:** Document ALL external interfaces verified from source code

**Verification Date:** 2026-02-12 03:12

---

## Interface 1: setup_logger

**Source:** utils/LoggingManager.py:190-208

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
- `name` (str): Logger name (becomes folder name if file logging enabled)
  - Required: Yes
  - Type: str (NOT None, NOT int)
  - Example: "schedule_fetcher" (snake_case for folder naming)
- `level` (Union[str, int]): Log level
  - Required: No
  - Default: 'INFO'
  - Type: Union[str, int]
  - Example: "INFO", "DEBUG", logging.INFO
- `log_to_file` (bool): Enable file logging
  - Required: No
  - Default: False
  - Type: bool (NOT int, NOT None)
  - Example: True, False, args.enable_log_file
- `log_file_path` (Optional[Union[str, Path]]): Custom log file path
  - Required: No
  - Default: None (auto-generate)
  - Type: Optional[Union[str, Path]]
  - Example: None (let LoggingManager generate path)
- `log_format` (str): Log format
  - Required: No
  - Default: 'standard'
  - Type: str
  - Example: "standard"
- `enable_console` (bool): Enable console logging
  - Required: No
  - Default: True
  - Type: bool
  - Example: True (always enable console)
- `max_file_size` (int): Max file size before rotation
  - Required: No
  - Default: 10 * 1024 * 1024 (10MB)
  - Type: int
  - Example: Keep default
- `backup_count` (int): Number of backup files
  - Required: No
  - Default: 5
  - Type: int
  - Example: Keep default

**Returns:**
- logging.Logger: Configured logger instance
  - Type: logging.Logger (NOT None)
  - Use returned logger for logging calls

**Exceptions:**
- None documented (handles errors internally)

**Usage in This Feature:**
```python
## run_schedule_fetcher.py (Task 2)
from utils.LoggingManager import setup_logger

logger = setup_logger(
    name="schedule_fetcher",        # Required: logger name
    level="INFO",                   # Default: INFO
    log_to_file=args.enable_log_file,  # CLI-driven
    log_file_path=None,            # Auto-generate path
    log_format="standard"          # Default format
)
```

**Verified:** ✅ Interface matches implementation_plan.md Task 2 assumptions

---

## Interface 2: get_logger

**Source:** utils/LoggingManager.py:210-211

**Signature:**
```python
def get_logger() -> logging.Logger
```

**Parameters:**
- None (retrieves singleton logger configured by setup_logger)

**Returns:**
- logging.Logger: Previously configured logger instance
  - Type: logging.Logger
  - Returns logger configured by setup_logger() call

**Exceptions:**
- None documented

**Usage in This Feature:**
```python
## schedule-data-fetcher/ScheduleFetcher.py (Task 4)
from utils.LoggingManager import get_logger

class ScheduleFetcher:
    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.logger = get_logger()  # No parameters - retrieves singleton
        self.client: Optional[httpx.AsyncClient] = None
```

**Verified:** ✅ Interface matches implementation_plan.md Task 4 assumptions

---

## Interface 3: LineBasedRotatingHandler

**Source:** utils/LineBasedRotatingHandler.py (Feature 01)

**Usage:** Internal to setup_logger() - transparent to this feature

**Integration:**
- setup_logger() automatically creates LineBasedRotatingHandler when log_to_file=True
- Handler provides 500-line rotation with max 50 backup files
- No direct interaction needed from this feature
- Folder structure: logs/{logger_name}/{logger_name}-{timestamp}.log

**Verified:** ✅ Integration tested in Feature 01, transparent to Feature 07

---

## Verification Summary

**Total Interfaces:** 3
**All Verified:** ✅ Yes (from actual source code)

**Implementation Plan Assumptions:**
- setup_logger() signature: ✅ MATCH (utils/LoggingManager.py:190-197)
- get_logger() signature: ✅ MATCH (utils/LoggingManager.py:210-211)
- LineBasedRotatingHandler integration: ✅ MATCH (transparent, handled by Feature 01)

**Confidence Level:** HIGH (all interfaces verified from actual source code with file:line references)

**Ready for Implementation:** ✅ YES

---

*End of interface_contracts.md*
