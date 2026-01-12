# Fantasy Football Helper Scripts - Coding Standards & Conventions

This document defines the coding standards and conventions for the Fantasy Football Helper Scripts project. All code contributions must follow these standards to ensure consistency, maintainability, and quality.

---

## Import Organization

```python
# Standard library (alphabetical)
import csv, json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party (alphabetical)
import pandas as pd

# Local with sys.path manipulation
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger
```

**Rules:**
- Use `Path` for file operations
- Use `sys.path.append()` for relative imports
- Type hints required for all functions

---

## Error Handling

```python
from utils.error_handler import error_context, DataProcessingError

# Use context managers for error tracking
with error_context("operation_name", component="module_name") as ctx:
    if error_condition:
        raise DataProcessingError("Error message", context=ctx)
```

**Rules:**
- Always use `error_context` for error tracking
- Raise appropriate error types (DataProcessingError, ValidationError, etc.)
- Include context information in error messages

---

## Logging Standards

```python
from utils.LoggingManager import setup_logger, get_logger

logger = setup_logger(name="module", level="INFO")  # Setup once
logger = get_logger()  # Use in modules

# Levels: debug, info, warning, error (with exc_info=True)
```

**Rules:**
- Use `setup_logger()` once at module initialization
- Use `get_logger()` to access logger in functions
- Log levels: debug (detailed), info (progress), warning (issues), error (failures)
- Always include `exc_info=True` for error logs

---

## Docstring Format (Google Style)

```python
def method_name(self, param1: Type, param2: Optional[Type] = None) -> ReturnType:
    """Brief one-line description.

    Args:
        param1 (Type): Description
        param2 (Optional[Type]): Description with default

    Returns:
        ReturnType: Description of return value

    Raises:
        DataProcessingError: When data processing fails
    """
```

**Rules:**
- One-line summary followed by blank line
- Args section with type annotations
- Returns section describing return value
- Raises section for exceptions (if applicable)
- Examples section for complex functions (optional)

---

## Type Hinting

```python
from typing import Dict, List, Optional, Union, Tuple
from pathlib import Path

def process_data(filepath: Union[str, Path],
                 options: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    """Process data from file.

    Args:
        filepath: Path to data file
        options: Optional processing options

    Returns:
        Tuple of (success, message)
    """
    pass
```

**Rules:**
- All function parameters must have type hints
- All function return values must have type hints
- Use Optional[T] for parameters that can be None
- Use Union[T1, T2] for parameters accepting multiple types
- Import types from typing module

---

## CSV Operations

```python
from utils.csv_utils import read_csv_with_validation, write_csv_with_backup

# Reading CSV with validation
df = read_csv_with_validation(
    filepath,
    required_columns=['id', 'name']
)

# Writing CSV with backup
write_csv_with_backup(
    df,
    filepath,
    create_backup=True
)
```

**Rules:**
- Always use `read_csv_with_validation()` for CSV reads
- Always use `write_csv_with_backup()` for CSV writes
- Specify `required_columns` for validation
- Enable backups for data files

---

## Configuration Access

```python
from util.ConfigManager import ConfigManager

config = ConfigManager(data_folder)
multiplier, rating = config.get_adp_multiplier(adp_val)
```

**Rules:**
- Use ConfigManager for all configuration access
- Do not read config files directly
- Config values are cached for performance

---

## Naming Conventions

### Classes
- **Format:** `PascalCase`
- **Examples:** `PlayerManager`, `ConfigManager`, `DraftHelper`

### Functions/Methods
- **Format:** `snake_case`
- **Examples:** `load_players()`, `get_score()`, `calculate_points()`

### Constants
- **Format:** `UPPER_SNAKE_CASE`
- **Examples:** `RECOMMENDATION_COUNT`, `LOGGING_LEVEL`, `MAX_ITERATIONS`

### Private Methods/Variables
- **Format:** `_leading_underscore`
- **Examples:** `_validate_config()`, `_internal_state`

### Modules
- **Format:** `snake_case`
- **Examples:** `error_handler.py`, `csv_utils.py`, `player_manager.py`

---

## Path Handling

```python
from pathlib import Path

# Use Path objects for file operations
base_path = Path(__file__).parent
config_file = base_path / "data" / "league_config.json"

# Convert to string when needed for APIs that require strings
with open(str(config_file), 'r') as f:
    data = json.load(f)
```

**Rules:**
- Always use `pathlib.Path` for path operations
- Use `/` operator for path joining (not string concatenation)
- Convert to string only when required by APIs
- Use `Path.exists()` for existence checks
- Use `Path.mkdir(parents=True, exist_ok=True)` for directory creation

---

## Testing Standards

### Test Suite Overview

**Test Suite:** 2,200+ tests (100% pass rate required before commits)
- **Unit Tests:** Test individual functions/classes in isolation, mock dependencies
- **Integration Tests:** Test cross-module workflows (25 tests)

### Test Execution

```bash
# Run all tests (REQUIRED before commits)
python tests/run_all_tests.py

# Run specific file
python -m pytest tests/path/test_file.py -v

# Run specific class
python -m pytest tests/path/test_file.py::TestClass -v

# Run with coverage
python -m pytest tests/ --cov=league_helper --cov-report=html
```

### Test Structure Requirements

**File Organization:**
- Test file structure mirrors source code
- Test file naming: `test_{module_name}.py`
- Test class naming: `Test{ClassName}`
- Test method naming: `test_{method_name}_{scenario}`

**Test Patterns:**

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

class TestPlayerManager:
    """Tests for PlayerManager class."""

    @pytest.fixture
    def sample_player_data(self):
        """Fixture providing sample player data."""
        return {
            'id': '123',
            'name': 'Player One',
            'position': 'QB'
        }

    def test_load_players_success(self, sample_player_data):
        """Test loading players successfully."""
        # Arrange
        manager = PlayerManager(data_folder='test_data')
        expected = [sample_player_data]

        # Act
        with patch('utils.csv_utils.read_csv_with_validation') as mock_read:
            mock_read.return_value = pd.DataFrame([sample_player_data])
            result = manager.load_players()

        # Assert
        assert len(result) == 1
        assert result[0]['name'] == 'Player One'
```

### Test Requirements

**AAA Pattern (Arrange, Act, Assert):**
- **Arrange:** Set up test data and mocks
- **Act:** Execute the code under test
- **Assert:** Verify expected outcomes

**Mocking Requirements:**
- Use pytest fixtures for reusable test data
- Mock external dependencies (files, APIs, datetime)
- Mock at the boundary (mock file reads, not Path objects)
- Use `patch()` for module-level mocks
- Use `Mock()` or `MagicMock()` for object mocks

**Test Independence:**
- Tests must be independent (no shared state)
- Each test sets up its own data
- Use fixtures or setUp/tearDown for common setup
- Never rely on test execution order

**Coverage Requirements:**
- Aim for >90% code coverage
- Test happy paths and error paths
- Test edge cases and boundary conditions
- Test invalid inputs and error handling

### Common Test Patterns

**Testing File Operations:**
```python
def test_save_data(tmp_path):
    """Test saving data to file."""
    # tmp_path is a pytest fixture providing temp directory
    test_file = tmp_path / "test_data.csv"
    manager = DataManager(str(tmp_path))

    manager.save_data(test_file, sample_data)

    assert test_file.exists()
```

**Testing Exceptions:**
```python
def test_invalid_input_raises_error():
    """Test that invalid input raises DataProcessingError."""
    manager = PlayerManager()

    with pytest.raises(DataProcessingError, match="Invalid player ID"):
        manager.get_player(None)
```

**Testing with Mocks:**
```python
@patch('utils.csv_utils.read_csv_with_validation')
def test_load_from_csv(mock_read):
    """Test loading data from CSV."""
    mock_read.return_value = pd.DataFrame([{'id': '1', 'name': 'Test'}])

    manager = DataManager()
    result = manager.load_data('test.csv')

    assert len(result) == 1
    mock_read.assert_called_once()
```

---

## Code Quality Standards

### Function Length
- Keep functions under 50 lines when possible
- Extract complex logic into helper functions
- Single Responsibility Principle: one function, one purpose

### Code Comments
- Use docstrings for all public functions/classes
- Add inline comments for complex logic only
- Avoid obvious comments ("increment counter" for `i += 1`)
- Explain WHY, not WHAT (code shows what, comments explain why)

### Error Messages
- Include context in error messages
- Specify what went wrong and what was expected
- Include relevant values for debugging
- Example: `f"Invalid ADP value {adp}: must be between 1 and 300"`

### Performance Considerations
- Avoid O(n²) algorithms when O(n log n) is possible
- Cache expensive computations
- Use generators for large data sets
- Profile before optimizing

---

## Pre-Commit Checklist

Before committing code, ensure:

- [ ] All unit tests pass (100% pass rate required)
- [ ] Code follows naming conventions
- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] No debug print statements
- [ ] No commented-out code
- [ ] Error handling is comprehensive
- [ ] Logging is appropriate for debugging

---

**See Also:**
- `tests/README.md` - Complete testing guidelines and examples
- `ARCHITECTURE.md` - System architecture and design patterns
- `CLAUDE.md` - Epic development workflow and commit protocols
