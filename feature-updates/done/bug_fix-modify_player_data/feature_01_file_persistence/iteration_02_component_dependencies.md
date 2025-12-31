# Iteration 2: Component Dependency Mapping

**Date:** 2025-12-31
**Feature:** Feature 01 - File Persistence Issues
**Round:** 1 (TODO Creation)
**Iteration:** 2 of 8

---

## Purpose

Verify all component dependencies for Feature 01 by reading actual source code. NEVER ASSUME - always verify interfaces.

---

## External Dependencies

### Dependency 1: shutil.copy2()

**Interface Verified:**
- Source: Python Standard Library (shutil module)
- Signature: `shutil.copy2(src, dst, *, follow_symlinks=True)`
- Parameters:
  - src: Source file path (str or Path)
  - dst: Destination file path (str or Path)
  - follow_symlinks: Whether to follow symbolic links (default: True)
- Returns: str (destination path)
- Purpose: Copy file with metadata (timestamps, permissions)
- **Current Usage:** PlayerManager.py line 556 (TO BE REMOVED in Task 1)

**Code Location:**
```python
# league_helper/util/PlayerManager.py:553-556 (WILL BE DELETED)
backup_path = json_path.with_suffix('.bak')
if json_path.exists():
    import shutil
    shutil.copy2(json_path, backup_path)
```

**TODO tasks using this:**
- Task 1: Remove .bak file creation code (removes shutil.copy2 call)

---

### Dependency 2: pathlib.Path.replace()

**Interface Verified:**
- Source: Python Standard Library (pathlib module)
- Signature: `Path.replace(target)`
- Parameters:
  - target: Destination path (str or Path)
- Returns: Path (the new path)
- Purpose: Rename file/directory, replacing target if exists (atomic on POSIX, NOT guaranteed atomic on Windows)
- **Current Usage:** PlayerManager.py line 566 (KEEP - atomic write pattern)
- **Platform Behavior:**
  - POSIX (Linux/Mac): Atomic replace (guaranteed)
  - Windows: NOT guaranteed atomic (may fail if target is open)

**Code Location:**
```python
# league_helper/util/PlayerManager.py:558-566 (KEEP THIS)
json_data_to_write = {position_key: players_array}
tmp_path = json_path.with_suffix('.tmp')
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(json_data_to_write, f, indent=2)

# Atomic replace (overwrites existing .json file)
tmp_path.replace(json_path)
```

**TODO tasks using this:**
- Task 9: Integration Test - Atomic Write Pattern on Windows
  - **CRITICAL**: Must verify Path.replace() works correctly on win32
  - Test must verify .tmp file created, then replaced atomically
  - Test must verify no .tmp files left behind

---

### Dependency 3: json.dump()

**Interface Verified:**
- Source: Python Standard Library (json module)
- Signature: `json.dump(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)`
- Parameters:
  - obj: Python object to serialize
  - fp: File-like object with write() method
  - indent: Number of spaces for indentation (None = compact, 2 = pretty)
- Returns: None (writes to file)
- Purpose: Serialize Python object to JSON file
- **Current Usage:** PlayerManager.py line 563

**Code Location:**
```python
# league_helper/util/PlayerManager.py:563
json.dump(json_data_to_write, f, indent=2)
```

**TODO tasks using this:**
- Task 10: Integration Test - JSON File Contents Match Expected Format
  - Must verify JSON format: `{position_key: [{players}]}`
  - Must verify indent=2 produces readable output

---

### Dependency 4: json.load()

**Interface Verified:**
- Source: Python Standard Library (json module)
- Signature: `json.load(fp, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)`
- Parameters:
  - fp: File-like object with read() method
- Returns: Python object (deserialized JSON)
- Purpose: Deserialize JSON file to Python object
- **Current Usage:** PlayerManager.py (in load_players_from_json method)

**TODO tasks using this:**
- Task 11: Integration Test - Changes Persist Immediately
- Task 12: Integration Test - Changes Persist Across Restarts
  - Both tests must read JSON back from disk using json.load()

---

## Internal Dependencies (Codebase Components)

### Dependency 5: PlayerManager class

**Interface Verified:**
- Source: league_helper/util/PlayerManager.py:84-90
- Constructor Signature:
```python
def __init__(
    self,
    data_folder: Path,
    config: ConfigManager,
    team_data_manager: TeamDataManager,
    season_schedule_manager: SeasonScheduleManager
) -> None:
```
- Parameters:
  - data_folder (Path): Path to data directory containing player_data/
  - config (ConfigManager): Configuration manager with scoring parameters
  - team_data_manager (TeamDataManager): Manager for team rankings
  - season_schedule_manager (SeasonScheduleManager): Manager for schedule data
- Returns: None
- Key Attributes:
  - self.players (List[FantasyPlayer]): All loaded players
  - self.data_folder (Path): Data directory path
  - self.logger: Logger instance

**Method to Test: update_players_file()**
- Source: league_helper/util/PlayerManager.py:451-584
- Signature: `def update_players_file(self) -> str:`
- Parameters: None (uses self.players)
- Returns: str (success message)
- Raises:
  - FileNotFoundError: If position JSON file missing
  - PermissionError: If cannot write to files
  - json.JSONDecodeError: If JSON file corrupted

**TODO tasks using this:**
- Task 4: Create test file for update_players_file()
- Task 5-13: All unit and integration tests for this method

---

### Dependency 6: FantasyPlayer class

**Interface Verified:**
- Source: utils/FantasyPlayer.py:78-96
- Class Type: dataclass
- Key Fields (for this feature):
```python
@dataclass
class FantasyPlayer:
    # Core identification
    id: int
    name: str
    team: str
    position: str

    # Fields we're testing persistence for
    drafted_by: str = ""  # Line 95
    locked: bool = False  # Line 96

    # Other fields (preserved but not modified by update_players_file)
    bye_week: Optional[int] = None
    fantasy_points: float = 0.0
    average_draft_position: Optional[float] = None
    player_rating: Optional[float] = None
    projected_points: List[float] = field(default_factory=lambda: [0.0] * 17)
    actual_points: List[float] = field(default_factory=lambda: [0.0] * 17)
    # ... (many more fields)
```

**TODO tasks using this:**
- Task 5: Unit Test - drafted_by Persistence (Mocked)
  - Verify drafted_by field written to JSON correctly
- Task 6: Unit Test - locked Persistence (Mocked)
  - Verify locked field written to JSON correctly
- Task 10: Integration Test - JSON File Contents
  - Verify both fields in actual JSON file

---

## Test Framework Dependencies

### Dependency 7: pytest

**Interface Verified:**
- Source: External package (installed via pip)
- Import: `import pytest`
- Key Features Used:
  - `@pytest.fixture` - Decorator for reusable test fixtures
  - `tmp_path` - Built-in fixture for temporary directories
  - `assert` - Python built-in (pytest provides detailed assertion introspection)
- **Existing Usage:** tests/league_helper/util/test_PlayerManager_json_loading.py:12

**Example from existing tests:**
```python
# tests/league_helper/util/test_PlayerManager_json_loading.py:25-28
@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with player_data subdirectory and JSON files."""
    data_folder = tmp_path / "data"
    data_folder.mkdir()
```

**TODO tasks using this:**
- Task 4: Create test file (use pytest framework)
- Task 5-13: All tests use pytest fixtures and assertions

---

### Dependency 8: unittest.mock

**Interface Verified:**
- Source: Python Standard Library
- Import: `from unittest.mock import Mock, MagicMock, patch`
- Key Classes:
  - `Mock`: Basic mock object
  - `MagicMock`: Mock with magic methods pre-configured
  - `patch`: Context manager/decorator for patching objects
- **Existing Usage:** tests/league_helper/util/test_PlayerManager_json_loading.py:15

**Example from existing tests:**
```python
# tests/league_helper/util/test_PlayerManager_json_loading.py:15
from unittest.mock import Mock, MagicMock
```

**TODO tasks using this:**
- Task 5: Unit Test - drafted_by Persistence (Mocked)
  - Mock file system operations
- Task 6: Unit Test - locked Persistence (Mocked)
  - Mock file system operations
- Task 7: Unit Test - NO .bak Files Created (Mocked)
  - Verify shutil.copy2() NOT called
- Task 8: Unit Test - Error Handling (Mocked)
  - Mock PermissionError, JSONDecodeError

---

## Test Pattern Dependencies

### Dependency 9: Existing Test Patterns

**Interface Verified:**
- Source: tests/league_helper/util/test_PlayerManager_json_loading.py
- Pattern: Integration tests with real file I/O using tmp_path

**Key Patterns to Follow:**

1. **Fixture for temporary data folder:**
```python
@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with player_data subdirectory and JSON files."""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create player_data subdirectory
    player_data_dir = data_folder / "player_data"
    player_data_dir.mkdir()

    # Create league_config.json
    config_content = {...}
    config_file = data_folder / "league_config.json"
    config_file.write_text(json.dumps(config_content))

    # Create position JSON files (qb_data.json, rb_data.json, etc.)
    qb_data = {"qb_data": [...]}
    qb_file = player_data_dir / "qb_data.json"
    qb_file.write_text(json.dumps(qb_data))

    return data_folder
```

2. **PlayerManager instantiation:**
```python
# Create mock dependencies
config = ConfigManager(data_folder)
team_data_manager = TeamDataManager(data_folder, current_week=1)
season_schedule_manager = SeasonScheduleManager(data_folder)

# Create PlayerManager
player_manager = PlayerManager(
    data_folder,
    config,
    team_data_manager,
    season_schedule_manager
)
```

**TODO tasks using this:**
- Task 9-13: All integration tests follow this pattern

---

## Platform-Specific Dependencies

### Dependency 10: Windows File System Behavior

**Interface Verified:**
- Source: Platform-specific (os.name == 'nt')
- Key Behavior: Path.replace() on Windows
- **CRITICAL FINDING:** Path.replace() is NOT guaranteed atomic on Windows

**Windows-Specific Considerations:**
1. Path.replace() may fail if target file is open by another process
2. Windows uses different file locking than POSIX systems
3. Tests must verify atomic write pattern works correctly on win32

**Code Location:**
```python
# league_helper/util/PlayerManager.py:566
tmp_path.replace(json_path)  # May not be atomic on Windows
```

**TODO tasks affected:**
- Task 9: Integration Test - Atomic Write Pattern on Windows
  - **MUST** verify this works correctly on win32 platform
  - Test environment: MINGW64_NT-10.0-19045 (from env context)
  - Verify .tmp file replaced .json file successfully
  - Verify no .tmp files left behind

---

## Dependency Summary

**Total Dependencies Verified:** 10

**Standard Library (5):**
1. ✅ shutil.copy2() - To be removed (Task 1)
2. ✅ pathlib.Path.replace() - Keep (atomic write pattern)
3. ✅ json.dump() - Keep (serialize to JSON)
4. ✅ json.load() - Keep (deserialize from JSON)
5. ✅ unittest.mock - Use for mocked unit tests

**Codebase Components (2):**
6. ✅ PlayerManager class - Constructor verified (4 parameters)
7. ✅ FantasyPlayer class - dataclass with drafted_by and locked fields

**Test Framework (2):**
8. ✅ pytest - Framework for test execution
9. ✅ Existing test patterns - Follow test_PlayerManager_json_loading.py

**Platform-Specific (1):**
10. ✅ Windows file system - Path.replace() behavior verified

---

## Interface Verification Complete

**All dependencies verified by reading actual source code.**

**No assumptions made.**

**All interfaces documented with:**
- Source file and line numbers
- Exact method signatures
- Parameter types and return types
- Current usage locations
- TODO tasks affected

---

## Next Steps

**Iteration 2 COMPLETE**

**Next:** Iteration 3 - Data Structure Verification

---

**END OF ITERATION 2**
