# Fantasy Football Helper - Unit Tests

This directory contains all unit tests for the Fantasy Football Helper project.

## Directory Structure

The test directory structure **mirrors the source code structure**:

```
tests/
├── README.md                          # This file
├── conftest.py                        # Pytest configuration (path setup)
├── run_all_tests.py                   # Test runner script (100% pass requirement)
├── league_helper/                     # Tests mirroring league_helper/ (modes + util/)
├── utils/                             # Shared utility / helper tests
├── player_data_fetcher/               # Player-data fetcher tests
├── historical_data_compiler/          # Historical-data compiler tests
├── schedule_data_fetcher/             # Schedule-data fetcher tests
├── simulation/                        # Win-rate + accuracy engine tests
├── integration/                       # Offline end-to-end fetcher/compiler tests
├── unit/                              # Standalone unit tests
├── root_scripts/                      # Repo-root runner-script tests
└── fixtures/                          # Committed offline JSON/CSV fixtures
```

For each source file, create a corresponding test file:
- Source: `league_helper/util/PlayerManager.py`
- Tests: `tests/league_helper/util/test_PlayerManager.py`

## Running Tests

### Option 1: Use the Test Runner Script (Recommended)

The `run_all_tests.py` script automatically discovers and runs all tests with a **strict 100% pass requirement**:

```bash
# Run all tests (default mode - shows summary)
python tests/run_all_tests.py

# Run with verbose output (shows individual test names)
python tests/run_all_tests.py --verbose

# Run with detailed output (includes full test output)
python tests/run_all_tests.py --detailed

# Run all tests in single command (faster, less granular reporting)
python tests/run_all_tests.py --single

# Show help
python tests/run_all_tests.py --help
```

**Exit Codes**:
- `0` = All tests passed (100%)
- `1` = One or more tests failed (< 100%)

### Option 2: Use Pytest Directly

```bash
# Run all tests in tests directory
.venv/bin/python -m pytest tests/ -v

# Run specific test file
.venv/bin/python -m pytest tests/league_helper/util/test_PlayerManager_scoring.py -v

# Run specific test class
.venv/bin/python -m pytest tests/league_helper/util/test_PlayerManager_scoring.py::TestConsistencyMultiplier -v

# Run specific test method
.venv/bin/python -m pytest tests/league_helper/util/test_PlayerManager_scoring.py::TestConsistencyMultiplier::test_consistency_excellent_low_cv -v

# Run with detailed output
.venv/bin/python -m pytest tests/ -vv --tb=short
```

## Test Standards

### Strict Requirements

1. **100% Pass Rate**: All tests must pass. No exceptions.
2. **Mirror Structure**: Test files must mirror source code directory structure
3. **Naming Convention**: Test files must be named `test_<module>.py`
4. **Comprehensive Coverage**: Each source file should have corresponding tests

### Test File Template

```python
"""
Unit Tests for <Module Name>

Description of what this test file covers.

Author: <Your Name>
Date: YYYY-MM-DD
"""

import pytest
from unittest.mock import Mock, MagicMock, patch

# Imports work via conftest.py which puts the project root on sys.path
from utils.FantasyPlayer import FantasyPlayer
from league_helper.util.PlayerManager import PlayerManager

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_object():
    """Description of fixture"""
    return Mock()

# ============================================================================
# TEST CLASS
# ============================================================================

class TestClassName:
    """Tests for ClassName"""

    def test_method_name(self, mock_object):
        """Test description"""
        # Arrange
        expected = "value"

        # Act
        result = mock_object.method()

        # Assert
        assert result == expected
```

## Current Test Coverage

The suite mirrors the source tree across several buckets and spans many `test_<module>.py`
files (as of this refresh, ~143 test files). Rather than freeze a snapshot
that will drift, run the canonical runner for the authoritative live picture — `python
tests/run_all_tests.py` (full suite, strict 100% pass gate) or `python tests/run_all_tests.py
--verbose` (individual test names).

Coverage buckets (each mirrors the corresponding source package):

- `tests/league_helper/` — League Helper modes and `util/` (scoring, config, roster, team data, …)
- `tests/utils/` — shared utility / helper modules
- `tests/player_data_fetcher/` — player-data fetcher
- `tests/historical_data_compiler/` — historical-data compiler
- `tests/schedule_data_fetcher/` — schedule-data fetcher
- `tests/simulation/` — win-rate and accuracy simulation engines
- `tests/integration/` — offline end-to-end fetcher/compiler flows (via committed fixtures)
- `tests/unit/` — standalone unit tests
- `tests/root_scripts/` — repo-root runner scripts
- `tests/fixtures/` — committed offline JSON/CSV fixtures (data the suite reads, not tests)

Run `python tests/run_all_tests.py` for the current total and per-file breakdown.

## Configuration

### conftest.py

The `conftest.py` file sets up the Python path for test imports. It adds:
- Project root directory
- `league_helper/` directory
- `league_helper/util/` directory

This allows tests to import modules the same way the application does.

### Never write into the repository's `data/` tree

`data/` holds the **tracked, live** season dataset (~800 players). A test that writes
into it destroys real committed data, and the damage is silent — the suite can pass
and exit `0` while the dataset is being overwritten.

**The rule:** any test that causes a write must redirect the data root to a temp dir.

Two environment seams exist for this:

| Variable | Redirects | Consumed by |
|---|---|---|
| `PLAYER_DATA_DIR` | the fetcher's data **root** — the directory *containing* `player_data/`, `team_data/`, and `game_data.csv` | `player_data_fetcher/config.py:data_root()` |
| `LEAGUE_DATA_DIR` | the League Helper's data tree | `league_helper/LeagueHelperManager.py` |

```python
def test_something_that_writes(tmp_path, monkeypatch):
    monkeypatch.setenv('PLAYER_DATA_DIR', str(tmp_path))
    ...
```

Both are resolved **at construction time**, so setting them after the module is
imported still works. When unset, the production repo-anchored defaults apply
unchanged.

Note `PLAYER_DATA_DIR` names the data *root*, not the `player_data/` subdirectory —
setting it to `tmp_path` gives you `tmp_path/player_data/`, `tmp_path/team_data/`,
and so on.

**Injection beats redirection where a parameter exists.** Most components
(`ConfigManager`, `PlayerManager`, `TeamDataManager`, `ScheduleFetcher`, …) take a
required data-folder argument — pass `tmp_path` directly rather than reaching for an
env var. The seams above exist for the paths that carry defaults.

**The runner enforces this.** `tests/run_all_tests.py` snapshots `git status
--porcelain -- data/` before and after the run and fails if the run *newly* dirtied
anything there. It is a baseline diff, so pre-existing local `data/` edits do not
false-red it, and it degrades to a notice when git is unavailable.

### Pytest Settings

Pytest is configured to:
- Discover tests starting with `test_`
- Run in strict mode (all tests must pass)
- Show detailed output on failures
- Use short tracebacks for readability

## Adding New Tests

1. **Create test file** in the appropriate directory:
   ```bash
   # For source file: league_helper/util/NewModule.py
   # Create test file: tests/league_helper/util/test_NewModule.py
   touch tests/league_helper/util/test_NewModule.py
   ```

2. **Write comprehensive tests**:
   - Test all public methods
   - Test edge cases and boundary conditions
   - Test error handling
   - Use mocks to isolate functionality

3. **Run tests** to verify:
   ```bash
   python tests/run_all_tests.py
   ```

4. **Ensure 100% pass rate** before committing

## CI/CD Integration

The test runner script can be integrated into CI/CD pipelines:

```bash
# In CI/CD script
python tests/run_all_tests.py
if [ $? -ne 0 ]; then
    echo "Tests failed! Build cancelled."
    exit 1
fi
```

## Test Development Guidelines

1. **One Test File Per Source File**: Each source module should have a corresponding test file
2. **Descriptive Test Names**: Use clear, descriptive test method names (e.g., `test_consistency_excellent_low_cv`)
3. **Arrange-Act-Assert Pattern**: Structure tests clearly with setup, execution, and verification
4. **Mock External Dependencies**: Use mocks to isolate the code under test
5. **Test Edge Cases**: Include boundary conditions, None values, empty lists, etc.
6. **Document Complex Tests**: Add docstrings explaining what complex tests verify

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:
1. Ensure `conftest.py` exists in `tests/` directory
2. Check that `__init__.py` files exist in package directories
3. Verify you're running tests from project root

### Path Issues

If tests can't find source files:
1. Check that `conftest.py` is setting up paths correctly
2. Ensure you're using package-rooted imports like `from utils.FantasyPlayer import FantasyPlayer` or `from league_helper.util.PlayerManager import PlayerManager`
3. Run pytest from project root directory

### Test Discovery Issues

If tests aren't being discovered:
1. Ensure test files start with `test_`
2. Ensure test methods start with `test_`
3. Check that test files are in proper directories

## Future Test Additions

As the project grows, add a mirrored `test_<module>.py` under the matching `tests/` path for
each new source module (see **Adding New Tests** above) — covering the happy path, edge cases,
and error handling — and keep the suite at a 100% pass rate. The modules once listed here as
pending (`ConfigManager`, `TeamDataManager`, `FantasyTeam`, `DraftModeManager`, and the
other mode managers) are now covered.

---

**Last refreshed**: 2026-07-18 — counts are not frozen in this doc; run `python tests/run_all_tests.py` for the authoritative live total and pass rate (strict 100% pass gate). As of this refresh: ~3073 tests across 143 `test_*.py` files (point-in-time snapshot).
