# FantasyFootballHelperScripts — Coding Standards

**Version:** 1.0
**Last Updated:** 2026-03-09
**Supplements:** Root-level `CODING_STANDARDS.md` (393 lines — read for full detail)

---

## Quick Reference

| Rule | Requirement |
|------|-------------|
| Python version | 3.14.2 (min 3.13.6) |
| Type hints | Required on ALL function parameters and return values |
| Docstrings | Google style; required on ALL public functions/classes |
| Error handling | Use `error_context()` from `utils/error_handler.py` |
| Logging | Use `LoggingManager`; no bare `print()` in production code |
| CSV operations | Use `csv_utils` helpers; never raw `open()` on CSV files |
| Config access | Use `ConfigManager`; never read JSON directly |
| Test pass rate | 100% required before every commit |

---

## Import Organization

```python
# 1. Standard library (alphabetical)
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

# 2. Third-party (alphabetical)
import pandas as pd
from pydantic import BaseModel

# 3. Local — sys.path manipulation then imports
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger
from utils.error_handler import error_context, DataProcessingError
```

**Rules:**
- Always use `pathlib.Path` for file paths (no string concatenation)
- Use `sys.path.append()` for cross-module imports (not relative imports)
- Keep each section alphabetically sorted

---

## Error Handling

```python
from utils.error_handler import error_context, DataProcessingError

def process_players(filepath: Path) -> List[Dict]:
    """Process player data from CSV."""
    with error_context("process_players", component="PlayerManager") as ctx:
        if not filepath.exists():
            raise DataProcessingError(
                f"Player file not found: {filepath}",
                context=ctx
            )
        # ... processing logic
```

**Custom exception types** (from `utils/error_handler.py`):
- `DataProcessingError` — data loading/transformation failures
- `APIError` — API call failures (ESPN API, external services)
- `FileOperationError` — file read/write failures
- `ConfigurationError` — config loading/parsing failures

**Rules:**
- Always use `error_context()` context manager — never bare `except Exception`
- Include the failing value in error messages: `f"Invalid ADP value {adp}: must be between 1 and 300"`
- Always pass `context=ctx` to custom exceptions
- Always use `exc_info=True` for `logger.error()` calls

---

## Logging

```python
from utils.LoggingManager import setup_logger, get_logger

# Module-level setup (once per module, at top)
logger = setup_logger(name="PlayerManager", level="INFO")

# In functions (access without re-configuring)
logger = get_logger()
logger.debug("Loading players from %s", filepath)
logger.info("Loaded %d players", len(players))
logger.warning("Missing field %r for player %r", field, name)
logger.error("Failed to load players: %s", err, exc_info=True)
```

**Log level guidance:**
- `debug` — detailed execution trace, loop internals, intermediate values
- `info` — operation progress ("Loaded 150 players", "Simulation complete")
- `warning` — recoverable issues, missing optional data, fallback triggered
- `error` — operation failed; always include `exc_info=True`

**Rules:**
- No `print()` statements in production code (only in CLI entry points for user-facing output)
- No `logging.basicConfig()` — always use `setup_logger()`/`get_logger()`

---

## Docstrings (Google Style)

```python
def calculate_player_score(
    self,
    player: FantasyPlayer,
    week: Optional[int] = None
) -> ScoredPlayer:
    """Calculate the composite score for a fantasy player.

    Applies the 10-step scoring algorithm using projected points,
    ADP, consistency, matchup, and penalty factors.

    Args:
        player (FantasyPlayer): Player dataclass with projection data.
        week (Optional[int]): Target week for matchup scoring.
            If None, uses current week from config.

    Returns:
        ScoredPlayer: Player with computed composite score and breakdown.

    Raises:
        DataProcessingError: If player data is missing required fields.
    """
```

**Required sections:**
- One-line summary (imperative: "Calculate...", "Load...", "Return...")
- Blank line after summary if body follows
- `Args:` section for all parameters (with types)
- `Returns:` section describing return value
- `Raises:` section if exceptions are raised

**Optional sections:**
- `Examples:` for complex public APIs

---

## Type Hints

```python
from typing import Dict, List, Optional, Union, Tuple, Any
from pathlib import Path

# All parameters and return values require type hints
def load_players(
    filepath: Union[str, Path],
    positions: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    ...

# Dataclasses use field-level type hints
from dataclasses import dataclass

@dataclass
class ScoredPlayer:
    name: str
    position: str
    score: float
    breakdown: Dict[str, float]
```

**Rules:**
- Use `Optional[T]` for parameters that default to `None`
- Use `Union[str, Path]` when accepting both types (common for filepaths)
- Use `Dict[str, Any]` for config/data dictionaries with dynamic keys
- Never use `dict`, `list`, `tuple` without parameters in type hints (use `Dict`, `List`, `Tuple`)

---

## Naming Conventions

| Element | Convention | Examples |
|---------|-----------|---------|
| Classes | `PascalCase` | `PlayerManager`, `ConfigManager`, `DraftHelperTeam` |
| Functions / methods | `snake_case` | `load_players()`, `get_adp_multiplier()`, `calculate_score()` |
| Constants | `UPPER_SNAKE_CASE` | `RECOMMENDATION_COUNT`, `MAX_ITERATIONS`, `DEFAULT_TIMEOUT` |
| Private methods | `_leading_underscore` | `_validate_config()`, `_parse_row()` |
| Module files | `PascalCase` for class modules | `PlayerManager.py`, `ConfigManager.py` |
| Module files | `snake_case` for utility modules | `error_handler.py`, `csv_utils.py`, `player_scoring.py` |
| Test files | `test_{SourceFileName}.py` (mirrors source casing) | `test_PlayerManager.py`, `test_player_scoring.py` |

---

## Path Handling

```python
from pathlib import Path

# Always use Path objects
base_path = Path(__file__).parent
config_file = base_path / "data" / "configs" / "league_config.json"

# Existence checks
if not config_file.exists():
    raise DataProcessingError(f"Config not found: {config_file}")

# Directory creation
output_dir = base_path / "output"
output_dir.mkdir(parents=True, exist_ok=True)

# Convert to str only when a library requires it
with open(str(config_file), "r") as f:
    data = json.load(f)
```

**Rules:**
- Always use `/` operator for path joining — never `os.path.join()` or string concatenation
- Always use `Path.exists()` not `os.path.exists()`
- Use `Path.mkdir(parents=True, exist_ok=True)` for safe directory creation

---

## CSV Operations

```python
from utils.csv_utils import read_csv_with_validation, write_csv_with_backup

# Reading — always validate required columns
df = read_csv_with_validation(
    filepath,
    required_columns=["name", "position", "projected_points"]
)

# Writing — always create backup
write_csv_with_backup(
    df,
    filepath,
    create_backup=True
)
```

**Rules:**
- Always use `read_csv_with_validation()` — never raw `pd.read_csv()` or `open()`
- Always use `write_csv_with_backup()` for data files
- Specify `required_columns` to catch schema drift early

---

## Configuration Access

```python
from util.ConfigManager import ConfigManager

config = ConfigManager(data_folder=Path("data"))

# Access typed values (cached)
multiplier, rating = config.get_adp_multiplier(adp_val)
bye_penalty = config.get_bye_week_penalty(same_pos_players, diff_pos_players)
```

**Rules:**
- Never read `league_config.json` directly — always use `ConfigManager`
- Config values are cached — instantiate once per run, share the instance
- Week-specific overrides are handled automatically by `ConfigManager`

---

## Testing Standards

**Run all tests:** `python tests/run_all_tests.py`
**100% pass rate required before every commit.**

**Test structure (Arrange-Act-Assert):**

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

class TestPlayerManager:
    """Tests for PlayerManager class."""

    @pytest.fixture
    def sample_players_df(self):
        """Fixture: minimal valid players DataFrame."""
        return pd.DataFrame([{
            "name": "Patrick Mahomes",
            "position": "QB",
            "team": "KC",
            "projected_points": 28.5,
            "adp": 5.0
        }])

    def test_load_players_returns_list(self, sample_players_df, tmp_path):
        """Test that load_players returns a non-empty list."""
        # Arrange
        manager = PlayerManager(data_folder=str(tmp_path))

        # Act
        with patch("utils.csv_utils.read_csv_with_validation",
                   return_value=sample_players_df):
            result = manager.load_players()

        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "Patrick Mahomes"
```

**Mock guidelines:**
- Mock at the boundary: mock file reads, API calls, datetime — not internal classes
- Use `pytest.fixture` for reusable test data
- Use `tmp_path` (pytest built-in) for file system tests
- Tests must be independent — no shared mutable state between tests

**Naming:**
- File: `test_{SourceFileName}.py` — casing mirrors the source file (e.g., `test_PlayerManager.py` for `PlayerManager.py`, `test_player_scoring.py` for `player_scoring.py`)
- Class: `Test{ClassName}` (e.g., `TestPlayerManager`)
- Method: `test_{method}_{scenario}` (e.g., `test_load_players_returns_list`)

---

## Code Quality Rules

- **Function length:** Keep under 50 lines; extract helpers for complex logic
- **Single responsibility:** One function = one purpose
- **Comments:** Explain *why*, not *what*; avoid obvious comments
- **No debug prints:** Remove all `print()` before committing
- **No commented-out code:** Delete dead code; git history preserves it
- **Error messages:** Include the failing value: `f"Invalid rank {rank}: must be 1–500"`

---

## Pre-Commit Checklist

```
[ ] python tests/run_all_tests.py  →  100% pass
[ ] All new functions have type hints
[ ] All new public functions/classes have Google-style docstrings
[ ] No print() statements in non-entry-point files
[ ] No commented-out code
[ ] Error handling uses error_context() pattern
[ ] Logging uses LoggingManager (no logging.basicConfig)
[ ] File paths use pathlib.Path
[ ] CSV reads use read_csv_with_validation()
```

---

*For complete standards with additional examples, read the root-level `CODING_STANDARDS.md`.*
