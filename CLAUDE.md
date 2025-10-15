# Fantasy Football Helper Scripts - Claude Code Guidelines

## Quick Start for New Agents

**FIRST**: Read `PROJECT_DOCUMENTATION.md` for complete architectural overview, system design, and implementation details.

**THIS FILE**: Contains workflow rules, coding standards, and commit protocols.

---

## Project-Specific Rules

### When User Requests "Update" or "Prepare for Updates Based on *.txt"

When the user requests to prepare for updates based on files in the `updates/` folder, follow this workflow:

1. **Read the update file** from `updates/` folder
2. **Create a questions file** (if needed) to clarify requirements
3. **Create TODO tracking file** in `updates/todo-files/` before starting
4. **Follow all rules** documented in `rules.txt`
5. **Track progress** for multi-session work
6. **Move completed files** to `updates/done/` when finished

### Workflow Details

The complete workflow for handling updates is documented in `rules.txt`. Key principles:

- **Ask questions first**: Create `{objective_name}_questions.md` in `updates/` folder
- **Plan systematically**: Create detailed TODO file in `updates/todo-files/`
- **Validate at every phase**: Run unit tests after each major step
- **Update documentation**: Modify README, CLAUDE.md, and rules files as needed
- **Test thoroughly**: 100% test pass rate required before completion
- **Complete the cycle**: Move update file to `updates/done/` when finished

See `rules.txt` for the complete protocol including pre-commit validation requirements.

### Commit Standards
- Brief, descriptive messages (50 chars or less)
- No emojis or subjective prefixes
- Do NOT include "Generated with Claude Code" and co-author tag
- List major changes in body

### Pre-Commit Protocol
**MANDATORY BEFORE EVERY COMMIT**

When the user requests to commit changes (e.g., "commit changes", "verify and commit", "commit this"):

**STEP 1: Run Unit Tests (REQUIRED)**
```bash
python tests/run_all_tests.py
```

**Test Requirements**:
- All unit tests must pass (100% pass rate)
- Tests located in `tests/` directory
- Exit code 0 = safe to commit, 1 = DO NOT COMMIT

**Only proceed to commit if all tests pass.**

**STEP 2: If Tests Pass, Commit Changes**
1. Analyze all changes with `git status` and `git diff`
2. Update documentation (README.md, CLAUDE.md) if functionality changed
3. Stage and commit with clear, concise message
4. Follow commit standards (see above)

**STEP 3: If Tests Fail**
- **STOP** - Do NOT commit
- Fix failing tests
- Re-run `python tests/run_all_tests.py`
- Only commit when all tests pass (exit code 0)

**Test Structure**:
- All tests in `tests/` directory (mirror source structure)
- See `tests/README.md` for test standards and guidelines
- Run with `--verbose` or `--detailed` flags for more output

**Do NOT skip validation**: 100% test pass rate is mandatory

## Current Project Structure

### Main Scripts
- `run_league_helper.py` - Main league helper application
- `run_player_fetcher.py` - Fetch player projection data
- `run_scores_fetcher.py` - Fetch NFL scores
- `run_simulation.py` - Run simulation system

### Source Code
- `league_helper/` - Main application logic
- `player-data-fetcher/` - Player data fetching
- `simulation/` - Simulation system
- `data/` - Data files (CSV, JSON)

### Tests
- `tests/` - All unit tests (mirrors source structure)
- `tests/run_all_tests.py` - Test runner (100% pass required)
- See `tests/README.md` for details

### Configuration & Updates
- `updates/` - Pending update specifications (*.txt files)
- `updates/todo-files/` - TODO tracking for updates in progress
- `updates/done/` - Completed updates
- `rules.txt` - Complete development workflow rules
- `CLAUDE.md` - This file (Claude Code guidelines)
- `PROJECT_DOCUMENTATION.md` - Complete architectural and implementation guide

---

## Coding Standards & Conventions

### Import Organization
```python
# Standard library (alphabetical)
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party (alphabetical)
import pandas as pd
import pytest

# Local with sys.path manipulation
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer
```

**Rules**:
- Always use `Path` for file operations, not string concatenation
- Use `sys.path.append()` for relative imports between modules
- Type hints required for all public methods

### Error Handling
```python
from utils.error_handler import (
    FantasyFootballError,
    DataProcessingError,
    create_component_error_handler,
    error_context
)

# Use context managers for error tracking
with error_context("operation_name", component="module_name") as ctx:
    # Operations that might fail
    if error_condition:
        raise DataProcessingError("Error message", context=ctx)

# Always log errors before raising
try:
    risky_operation()
except SpecificError as e:
    self.logger.error(f"Operation failed: {e}")
    raise
```

### Logging Standards
```python
from utils.LoggingManager import setup_logger, get_logger

# Setup once (in main or __init__)
logger = setup_logger(name="module", level="INFO")

# Use in modules
logger = get_logger()

# Logging levels:
logger.debug(f"Detailed info: {value}")      # Diagnostic details
logger.info(f"Operation complete: {count}")  # Progress updates
logger.warning(f"Unexpected: {issue}")       # Recoverable issues
logger.error(f"Failed: {e}", exc_info=True)  # Serious problems
```

### Docstring Format (Google Style)
```python
def method_name(self, param1: Type, param2: Optional[Type] = None) -> ReturnType:
    """
    Brief one-line description.

    Longer description explaining behavior, edge cases, and important details.

    Args:
        param1 (Type): Description of parameter
        param2 (Optional[Type]): Description with default behavior

    Returns:
        ReturnType: Description of return value
            - Special case 1
            - Special case 2

    Raises:
        ErrorType: When this occurs

    Example:
        >>> result = obj.method_name(value)
        >>> print(result)
    """
```

### Type Hinting
```python
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path

# All public methods must have type hints
def process_data(
    filepath: Union[str, Path],
    options: Optional[Dict[str, Any]] = None
) -> Tuple[bool, str]:
    pass

# Use Optional for nullable values
def get_player(self, player_id: int) -> Optional[FantasyPlayer]:
    pass
```

### CSV Operations
```python
from utils.csv_utils import (
    read_csv_with_validation,
    write_csv_with_backup,
    safe_csv_read
)

# Always validate required columns
df = read_csv_with_validation(
    filepath,
    required_columns=['id', 'name', 'position'],
    encoding='utf-8'
)

# Use backup when writing critical data
write_csv_with_backup(df, filepath, create_backup=True)
```

### Configuration Access
```python
from util.ConfigManager import ConfigManager

# Single source of truth
config = ConfigManager(data_folder)

# Use helper methods for calculations
multiplier, rating = config.get_adp_multiplier(adp_val)
penalty = config.get_injury_penalty(risk_level)
```

### Naming Conventions
- **Classes**: `PascalCase` (PlayerManager, ConfigManager)
- **Functions/Methods**: `snake_case` (load_players, get_score)
- **Constants**: `UPPER_SNAKE_CASE` (MAX_PLAYERS, LOGGING_LEVEL)
- **Private**: `_leading_underscore` (_validate_config)
- **Modules**: `snake_case` (error_handler.py, csv_utils.py)

### Path Handling
```python
from pathlib import Path

# Always use Path objects
base_path = Path(__file__).parent
data_path = base_path / "data"
config_file = data_path / "league_config.json"

# Convert to string only when required
with open(str(config_file), 'r') as f:
    pass
```

### Testing Patterns
```python
# tests/module_path/test_FileName.py
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def test_object(tmp_path):
    """Create test instance with temp data"""
    return ClassUnderTest(tmp_path)

class TestFeatureName:
    """Test Feature Name functionality"""

    def test_feature_normal_case(self, test_object):
        """Test feature with normal inputs"""
        result = test_object.method()
        assert result == expected
```

**Testing Rules**:
- Test file structure mirrors source code structure
- Use fixtures for reusable test data
- Mock external dependencies (APIs, file systems)
- 100% pass rate required before commits
- See `tests/README.md` for complete guidelines
