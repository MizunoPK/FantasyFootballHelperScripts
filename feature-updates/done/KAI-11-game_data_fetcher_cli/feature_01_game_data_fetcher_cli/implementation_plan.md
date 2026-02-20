## Implementation Plan: game_data_fetcher_cli

**Created:** 2026-02-19 S5 v2 - Phase 1 (Draft Creation)
**Last Updated:** 2026-02-19
**Status:** PENDING USER APPROVAL (Gate 5)
**Version:** v1.0

---

## Implementation Tasks

### Task 1: Move sys.path to Module Level + Remove os.chdir

**Requirement:** `spec.md` REQ-04 — Remove `os.chdir()` anti-pattern; move sys.path to module level

**Description:**
Move `sys.path.insert()` calls from inside the try/finally block to module level (before any
non-standard imports). Remove `os.chdir(fetcher_dir)`, `os.getcwd()`, `os.chdir(original_cwd)`,
the try/finally wrapper, and `import os`.

**File:** `run_game_data_fetcher.py`
**Method:** Module-level (not inside a function)
**Line:** 22-101 (current anti-pattern span)

**Change:**
```
## Current (anti-pattern)
import os          # line 23
...
original_cwd = os.getcwd()        # line 93
try:
    os.chdir(fetcher_dir)         # line 97
    sys.path.insert(0, str(fetcher_dir))  # line 100
    sys.path.insert(0, str(script_dir))   # line 101
    from game_data_fetcher import ...     # line 104
    from config import NFL_SEASON, ...   # line 105
    from utils.LoggingManager import ... # line 106
    ...
finally:
    os.chdir(original_cwd)        # line 169

## New (module-level)
import sys                         # keep existing
from pathlib import Path           # keep existing
# (import os REMOVED)

# Module-level sys.path
_script_dir = Path(__file__).parent
_fetcher_dir = _script_dir / "player-data-fetcher"
sys.path.insert(0, str(_fetcher_dir))
sys.path.insert(0, str(_script_dir))

from game_data_fetcher import fetch_game_data, GameDataFetcher  # noqa: E402
from utils.LoggingManager import setup_logger                    # noqa: E402
# (from config import ... REMOVED — see Task 2)
```

**Acceptance Criteria:**
- [ ] `import os` removed from file (no remaining os usage)
- [ ] `_script_dir = Path(__file__).parent` at module level (before any imports from player-data-fetcher)
- [ ] `_fetcher_dir = _script_dir / "player-data-fetcher"` at module level
- [ ] `sys.path.insert(0, str(_fetcher_dir))` at module level
- [ ] `sys.path.insert(0, str(_script_dir))` at module level
- [ ] `from game_data_fetcher import fetch_game_data, GameDataFetcher` at module level
- [ ] `from utils.LoggingManager import setup_logger` at module level
- [ ] `original_cwd = os.getcwd()` removed (line 93)
- [ ] `os.chdir(fetcher_dir)` removed (line 97)
- [ ] `os.chdir(original_cwd)` removed (line 169)
- [ ] try/finally wrapper removed; code formerly inside try now runs in main() directly
- [ ] `grep "os.chdir" run_game_data_fetcher.py` returns empty

**Dependencies:** None (first task)

**Tests:** S2 (grep os.chdir), S2 structural check, C1 (import test), E6 (CWD independence)

---

### Task 2: Remove Config Import + Config Fallback Patterns

**Requirement:** `spec.md` REQ-03 — Remove `from config import NFL_SEASON, CURRENT_NFL_WEEK`

**Description:**
Remove the config import (line 105 in current file, inside try block). Remove config fallback
patterns (lines 112-113: `season = args.season if args.season else NFL_SEASON` etc.).
Config-sourced defaults will be replaced by argparse defaults in Task 3.

**File:** `run_game_data_fetcher.py`
**Method:** Module-level import section + main() body
**Line:** 105 (import), 112-113 (fallback patterns)

**Change:**
```
## Current
from config import NFL_SEASON, CURRENT_NFL_WEEK   # line 105 — REMOVE
...
season = args.season if args.season else NFL_SEASON           # line 112 — REMOVE
current_week = args.current_week if args.current_week else CURRENT_NFL_WEEK  # line 113 — REMOVE

## New
# (config import removed — no replacement needed here)
# (fallback patterns removed — argparse defaults handle this, see Task 3)
season = args.season          # already 2025 if not provided (argparse default)
current_week = args.current_week  # already 17 if not provided (argparse default)
```

**Acceptance Criteria:**
- [ ] `from config import NFL_SEASON, CURRENT_NFL_WEEK` removed
- [ ] Config fallback pattern `args.season if args.season else NFL_SEASON` removed
- [ ] Config fallback pattern `args.current_week if args.current_week else CURRENT_NFL_WEEK` removed
- [ ] `grep "from config import" run_game_data_fetcher.py` returns empty
- [ ] `grep "NFL_SEASON" run_game_data_fetcher.py` returns empty
- [ ] `grep "CURRENT_NFL_WEEK" run_game_data_fetcher.py` returns empty

**Dependencies:** Task 1 (module-level imports restructured)

**Tests:** S1 (grep config import), C1 (import test succeeds), U2 (defaults correct)

---

### Task 3: Extract parse_args() + Add 4 New CLI Args

**Requirement:** `spec.md` REQ-01, REQ-02, REQ-07, REQ-09, REQ-10

**Description:**
Extract argparse logic from `main()` into a module-level `parse_args(argv=None)` function.
Fix `--season` and `--current-week` defaults from `None` to hardcoded values. Add 4 new args:
`--e2e-test`, `--log-level`, `--request-timeout`, `--historical-season`.

**File:** `run_game_data_fetcher.py`
**Method:** New function `parse_args(argv=None)` at module level (between `parse_weeks()` and `main()`)
**Line:** New function inserted ~line 54 (before current `def main():`)

**Change:**
```
## Current (argparse inline in main)
def main():
    parser = argparse.ArgumentParser(...)
    parser.add_argument('--season', type=int, default=None, ...)   # default=None
    parser.add_argument('--output', type=str, default=None, ...)
    parser.add_argument('--weeks', type=str, default=None, ...)
    parser.add_argument('--current-week', type=int, default=None, ...)   # default=None
    args = parser.parse_args()
    ...

## New (module-level parse_args function, called from main)
def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch NFL game data (venue, weather, scores) from ESPN and Open-Meteo APIs"
    )
    # Existing args — with FIXED defaults (REQ-02)
    parser.add_argument('--season', type=int, default=2025, ...)     # was None
    parser.add_argument('--output', type=str, default=None, ...)
    parser.add_argument('--weeks', type=str, default=None, ...)
    parser.add_argument('--current-week', type=int, default=17, ...) # was None

    # New universal args (REQ-01)
    parser.add_argument('--e2e-test', action='store_true', default=False, ...)
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'], ...)

    # New script-specific args (REQ-09, REQ-10)
    parser.add_argument('--request-timeout', type=int, default=30, ...)
    parser.add_argument('--historical-season', action='store_true', default=False, ...)

    return parser.parse_args(argv)

def main():
    args = parse_args()   # replaces inline argparse
    ...
```

**Acceptance Criteria:**
- [ ] `parse_args(argv=None)` function exists at module level and is callable (REQ-01)
- [ ] `parse_args([]).season == 2025` (REQ-02: was None)
- [ ] `parse_args([]).current_week == 17` (REQ-02: was None)
- [ ] `parse_args([]).log_level == 'INFO'` (REQ-07)
- [ ] `parse_args([]).e2e_test is False` (REQ-01)
- [ ] `parse_args([]).request_timeout == 30` (REQ-10)
- [ ] `parse_args([]).historical_season is False` (REQ-09)
- [ ] `--log-level` has `choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL']` (REQ-07)
- [ ] `--e2e-test` uses `action='store_true'` (flag, not value arg) (REQ-01)
- [ ] `--historical-season` uses `action='store_true'` (REQ-09)
- [ ] `--request-timeout` uses `type=int` (REQ-10)
- [ ] `main()` calls `parse_args()` instead of inline `parser.parse_args()` (REQ-01)
- [ ] `python run_game_data_fetcher.py --help` shows all 8 args

**Dependencies:** Task 1 (module restructure complete)

**Tests:** U1, U2 (all 6 defaults), C2 (help output — 8 args), E1 (invalid log-level → SystemExit), E4 (non-int request-timeout → SystemExit), E5 (non-int season → SystemExit)

---

### Task 4: Wire New Args in main() Body

**Requirement:** `spec.md` REQ-05, REQ-06, REQ-08, REQ-09

**Description:**
Update `main()` to use new args: wire `args.log_level` to `setup_logger()`, implement E2E mode
(weeks=[1] + output override), replace implicit historical detection with `--historical-season`
flag, and pass `request_timeout` to `fetch_game_data()`.

**File:** `run_game_data_fetcher.py`
**Method:** `main()`
**Line:** ~109 (setup_logger), ~115-118 (historical detection), ~120-124 (output path), ~127-130 (weeks), ~143-148 (fetch_game_data call)

**Change:**
```
## REQ-05: Wire log_level (was hardcoded "INFO")
# BEFORE
logger = setup_logger("game_data_fetcher", "INFO", False, None, "standard")
# AFTER
logger = setup_logger("game_data_fetcher", args.log_level, False, None, "standard")

## REQ-09: Replace implicit historical detection with explicit flag
# BEFORE (lines 116-118)
if args.season and args.season < NFL_SEASON:
    current_week = 18
    logger.info(f"Historical season {season}: setting current_week to 18")
# AFTER
if args.historical_season:
    current_week = 18
    logger.info(f"Historical season mode: fetching all 18 weeks for {args.season}")

## REQ-06: E2E mode — limit to week 1 + override output path
# AFTER parse_args() and output_path determination:
if args.e2e_test:
    weeks = [1]
    logger.info("E2E test mode: limiting to week 1")
    output_path = Path("/tmp/game_data_e2e_test.csv")
elif args.weeks:
    weeks = parse_weeks(args.weeks)
    logger.info(f"Fetching specific weeks: {weeks}")
else:
    weeks = None

## REQ-10: Pass request_timeout to fetch_game_data
# BEFORE
result_path = fetch_game_data(
    output_path=output_path,
    season=season,
    current_week=current_week,
    weeks=weeks
)
# AFTER
result_path = fetch_game_data(
    output_path=output_path,
    season=season,
    current_week=current_week,
    weeks=weeks,
    request_timeout=args.request_timeout
)
```

**Acceptance Criteria:**
- [ ] `setup_logger("game_data_fetcher", args.log_level, ...)` — not hardcoded "INFO" (REQ-05)
- [ ] `--log-level DEBUG` produces DEBUG lines in output (REQ-05 smoke test)
- [ ] `args.historical_season` flag triggers `current_week = 18` logic (REQ-09)
- [ ] Log message: `"Historical season mode: fetching all 18 weeks for {args.season}"` (REQ-09)
- [ ] `--historical-season` overrides `--current-week` (historical wins: REQ-09 precedence)
- [ ] `--e2e-test` sets `weeks = [1]` (REQ-06)
- [ ] `--e2e-test` sets `output_path = Path("/tmp/game_data_e2e_test.csv")` (REQ-06)
- [ ] `--e2e-test` takes precedence over `--weeks` (REQ-06 precedence)
- [ ] Log message: `"E2E test mode: limiting to week 1"` (REQ-06)
- [ ] `fetch_game_data()` called with `request_timeout=args.request_timeout` (REQ-10)
- [ ] No-args behavior: season=2025, current_week=17, output=data/game_data.csv, log=INFO (REQ-08)
- [ ] `python run_game_data_fetcher.py --e2e-test` exits 0, writes /tmp/game_data_e2e_test.csv (REQ-06)
- [ ] `data/game_data.csv` NOT modified during E2E mode (REQ-06)

**Dependencies:** Task 2 (config fallback removed), Task 3 (parse_args() created)

**Tests:** C3 (E2E smoke), C4 (log-level passthrough), C5 (historical season), C6 (backward compat), E2 (e2e overrides weeks), E3 (historical overrides current-week)

---

### Task 5: Create Test File

**Requirement:** `spec.md` REQ-11 — Create `tests/root_scripts/test_run_game_data_fetcher.py`

**Description:**
Create new test file with class `TestRunGameDataFetcher` containing 3 tests that verify
the structural properties of the refactored runner: parse_args callable at module level,
all 6 default values correct, and no subprocess import.

**File:** `tests/root_scripts/test_run_game_data_fetcher.py` (CREATE)
**Pattern reference:** `TestRunPlayerFetcher` in `tests/root_scripts/test_root_scripts.py:95-113`

**New File Content:**
```python
"""
Tests for run_game_data_fetcher.py (KAI-11: CLI refactoring pattern)
"""


class TestRunGameDataFetcher:
    """Test run_game_data_fetcher.py (KAI-11: parse_args extraction, no subprocess)"""

    def test_has_parse_args(self):
        """Test run_game_data_fetcher has parse_args function (KAI-11 refactoring)"""
        import run_game_data_fetcher
        assert hasattr(run_game_data_fetcher, 'parse_args')
        assert callable(run_game_data_fetcher.parse_args)

    def test_parse_args_defaults(self):
        """Test parse_args([]) returns correct defaults (argparse as single source of truth)"""
        import run_game_data_fetcher
        args = run_game_data_fetcher.parse_args([])
        assert args.season == 2025
        assert args.current_week == 17
        assert args.log_level == 'INFO'
        assert args.e2e_test is False
        assert args.request_timeout == 30
        assert args.historical_season is False

    def test_no_subprocess(self):
        """Test run_game_data_fetcher does not use subprocess (KAI-11 direct import)"""
        import run_game_data_fetcher
        assert not hasattr(run_game_data_fetcher, 'subprocess')
```

**Acceptance Criteria:**
- [ ] File created at `tests/root_scripts/test_run_game_data_fetcher.py`
- [ ] Class `TestRunGameDataFetcher` with exactly 3 test methods
- [ ] `test_has_parse_args`: verifies `hasattr` + `callable` (REQ-11)
- [ ] `test_parse_args_defaults`: checks all 6 defaults: season=2025, current_week=17, log_level='INFO', e2e_test=False, request_timeout=30, historical_season=False (REQ-11)
- [ ] `test_no_subprocess`: verifies subprocess not imported (REQ-11)
- [ ] `pytest tests/root_scripts/test_run_game_data_fetcher.py -v` shows 3 tests passed
- [ ] `pytest tests/ -v` 100% pass, 0 failures (REQ-08 regression check)

**Dependencies:** Task 1, 2, 3 (run_game_data_fetcher.py fully refactored before tests can pass)

**Tests:** U1 (test_has_parse_args), U2 (test_parse_args_defaults), U3 (test_no_subprocess), C7 (full regression suite)

---

## Requirement-to-Task Mapping (Dimension 1 Evidence)

| Spec Requirement | Implementation Task(s) | Coverage |
|------------------|------------------------|----------|
| REQ-01: parse_args() + --e2e-test + --log-level | Task 3 (extract + add args) | 100% |
| REQ-02: Fix defaults (season=2025, week=17) | Task 3 (default= in argparse) | 100% |
| REQ-03: Remove config import | Task 2 (remove from config import) | 100% |
| REQ-04: Remove os.chdir() + sys.path to module level | Task 1 (module restructure) | 100% |
| REQ-05: Wire --log-level to setup_logger | Task 4 (args.log_level) | 100% |
| REQ-06: E2E mode (weeks=[1], /tmp output, ≤180s) | Task 4 (e2e block in main) | 100% |
| REQ-07: --log-level choices + default 'INFO' | Task 3 (choices=, default=) | 100% |
| REQ-08: Backward compatibility | Task 3 + Task 4 (defaults match pre-refactor) | 100% |
| REQ-09: --historical-season flag + precedence | Task 3 (add arg) + Task 4 (flag logic) | 100% |
| REQ-10: --request-timeout arg + pass-through | Task 3 (add arg) + Task 4 (pass to fetch) | 100% |
| REQ-11: Create test file (3 tests) | Task 5 (new test file) | 100% |

**Total Requirements:** 11/11 covered (100%) ✅

## Test-to-Task Mapping (Dimension 1 Evidence — test_strategy.md coverage)

| test_strategy.md Test | Implementation Task | Coverage |
|----------------------|---------------------|----------|
| U1: test_has_parse_args | Task 5 (create test file) | 100% |
| U2: test_parse_args_defaults | Task 5 (create test file) | 100% |
| U3: test_no_subprocess | Task 5 (create test file) | 100% |
| S1: grep config import | Task 2 (remove import) | 100% |
| S2: grep os.chdir | Task 1 (remove chdir) | 100% |
| C1: Import test | Task 1 + 2 (restructure complete) | 100% |
| C2: Help output (8 args) | Task 3 (parse_args function) | 100% |
| C3: E2E mode | Task 4 (e2e logic in main) | 100% |
| C4: Log-level passthrough | Task 4 (args.log_level wired) | 100% |
| C5: Historical season | Task 3 + 4 (flag + logic) | 100% |
| C6: Backward compat | Task 3 + 4 (defaults) | 100% |
| C7: Regression suite | All tasks (no regressions) | 100% |
| E1: Invalid log-level → SystemExit | Task 3 (choices= enforced by argparse) | 100% |
| E2: --e2e-test + --weeks conflict | Task 4 (e2e precedence) | 100% |
| E3: --historical-season + --current-week | Task 4 (historical precedence) | 100% |
| E4: --request-timeout non-int | Task 3 (type=int enforced by argparse) | 100% |
| E5: --season non-int | Task 3 (type=int enforced by argparse) | 100% |
| E6: Import from any CWD | Task 1 (Path(__file__).parent — absolute) | 100% |

**Total Test Scenarios:** 18/18 covered (100%) ✅

---

## Algorithm Traceability Matrix

Maps every algorithm/behavior in spec.md to exact code location in refactored file.

| Algorithm (from spec) | Spec Section | Implementation Task | File:Method | Notes |
|-----------------------|--------------|---------------------|-------------|-------|
| Module-level sys.path insert (_fetcher_dir) | REQ-04 | Task 1 | run_game_data_fetcher.py:module-level | `_fetcher_dir = _script_dir / "player-data-fetcher"` |
| Module-level sys.path insert (_script_dir) | REQ-04 | Task 1 | run_game_data_fetcher.py:module-level | Needed for utils.LoggingManager |
| Remove os.chdir(fetcher_dir) | REQ-04 | Task 1 | run_game_data_fetcher.py:93,97 (remove) | Eliminates global state mutation |
| Remove original_cwd + os.chdir(original_cwd) | REQ-04 | Task 1 | run_game_data_fetcher.py:93,169 (remove) | Eliminates finally block |
| Remove import os | REQ-04 | Task 1 | run_game_data_fetcher.py:23 (remove) | os no longer used |
| Move imports to module level | REQ-04 | Task 1 | run_game_data_fetcher.py:module-level | game_data_fetcher + setup_logger |
| Remove from config import | REQ-03 | Task 2 | run_game_data_fetcher.py:105 (remove) | NFL_SEASON + CURRENT_NFL_WEEK |
| Remove config fallback: season | REQ-02 | Task 2 | run_game_data_fetcher.py:112 (remove) | args.season used directly |
| Remove config fallback: current_week | REQ-02 | Task 2 | run_game_data_fetcher.py:113 (remove) | args.current_week used directly |
| parse_args(argv=None) — module-level function | REQ-01 | Task 3 | run_game_data_fetcher.py:parse_args() | Enables unit testing without running main() |
| --season arg (default=2025, type=int) | REQ-02 | Task 3 | parse_args():parser.add_argument | Fixed default replaces config lookup |
| --output arg (default=None) | existing | Task 3 | parse_args():parser.add_argument | No change to default |
| --weeks arg (default=None) | existing | Task 3 | parse_args():parser.add_argument | No change to default |
| --current-week arg (default=17, type=int) | REQ-02 | Task 3 | parse_args():parser.add_argument | Fixed default replaces config lookup |
| --e2e-test arg (action=store_true) | REQ-01 | Task 3 | parse_args():parser.add_argument | Flag, default=False |
| --log-level arg (choices=5 levels, default='INFO') | REQ-01, REQ-07 | Task 3 | parse_args():parser.add_argument | Enforced by argparse choices= |
| --request-timeout arg (type=int, default=30) | REQ-10 | Task 3 | parse_args():parser.add_argument | Passed to fetch_game_data |
| --historical-season arg (action=store_true) | REQ-09 | Task 3 | parse_args():parser.add_argument | Replaces implicit year comparison |
| Wire args.log_level to setup_logger() | REQ-05 | Task 4 | main():setup_logger call | Replaces hardcoded "INFO" |
| E2E: weeks = [1] override | REQ-06 | Task 4 | main():e2e block | Deterministic week, ≤180s |
| E2E: output_path = /tmp/game_data_e2e_test.csv | REQ-06 | Task 4 | main():e2e block | Fixed path per user preference |
| E2E: log "E2E test mode: limiting to week 1" | REQ-06 | Task 4 | main():e2e block | Required log message |
| E2E takes precedence over --weeks | REQ-06 | Task 4 | main():if args.e2e_test before elif args.weeks | if/elif ordering |
| Historical: if args.historical_season → current_week=18 | REQ-09 | Task 4 | main():historical block | Replaces implicit comparison |
| Historical: log "Historical season mode: fetching all 18 weeks for {season}" | REQ-09 | Task 4 | main():historical block | Explicit log message |
| Historical overrides --current-week | REQ-09 | Task 4 | main():historical block after parse_args | current_week reassigned to 18 |
| Pass request_timeout=args.request_timeout to fetch_game_data | REQ-10 | Task 4 | main():fetch_game_data() call | Interface: game_data_fetcher.py:520 |
| No-args: season=2025, week=17, output=data/game_data.csv, log=INFO | REQ-08 | Task 3+4 | parse_args defaults + main() | Backward compat preserved |
| Create TestRunGameDataFetcher class | REQ-11 | Task 5 | tests/root_scripts/test_run_game_data_fetcher.py | 3 test methods |
| test_has_parse_args | REQ-11 | Task 5 | TestRunGameDataFetcher | hasattr + callable check |
| test_parse_args_defaults | REQ-11 | Task 5 | TestRunGameDataFetcher | all 6 defaults verified |
| test_no_subprocess | REQ-11 | Task 5 | TestRunGameDataFetcher | not hasattr(module, 'subprocess') |

**Total Mappings:** 32 ✅

---

## Component Dependencies

### Verified Interfaces (from actual source code)

**1. `fetch_game_data()` — `player-data-fetcher/game_data_fetcher.py:520-527`**
```python
def fetch_game_data(
    output_path: Optional[Path] = None,
    season: int = 2025,
    current_week: int = 17,
    weeks: Optional[List[int]] = None,
    request_timeout: int = 30,
    rate_limit_delay: float = 0.2
) -> Path:
```
- **Used in:** Task 4 (pass `request_timeout=args.request_timeout`)
- **Status:** Interface verified from source ✅
- **Impact:** Add `request_timeout=args.request_timeout` kwarg to call (currently missing)
- **Note:** `rate_limit_delay` NOT passed — unused per KAI-10 S2 decision (Q1 Option C)

**2. `setup_logger()` — `utils/LoggingManager.py:190-197`**
```python
def setup_logger(name: str,
                level: Union[str, int] = 'INFO',
                log_to_file: bool = False,
                log_file_path: Optional[Union[str, Path]] = None,
                log_format: str = 'standard',
                enable_console: bool = True,
                max_file_size: int = 10 * 1024 * 1024,
                backup_count: int = 5) -> logging.Logger:
```
- **Used in:** Task 4 (wire `args.log_level` to `level` parameter)
- **Status:** Interface verified from source ✅
- **Current call:** `setup_logger("game_data_fetcher", "INFO", False, None, "standard")`
- **New call:** `setup_logger("game_data_fetcher", args.log_level, False, None, "standard")`
- **Note:** `utils/LoggingManager.py` is in project root `utils/`, requires `_script_dir` in sys.path

**3. `game_data_fetcher.GameDataFetcher` — `player-data-fetcher/game_data_fetcher.py`**
- **Used in:** Task 1 (module-level import alongside `fetch_game_data`)
- **Status:** Currently imported at line 104; moved to module level
- **Note:** `GameDataFetcher` imported but only `fetch_game_data()` called directly

**This Feature Depends On:**
- `player-data-fetcher/game_data_fetcher.py` — already modified by KAI-10; `fetch_game_data()` already accepts `request_timeout=30` ✅
- `utils/LoggingManager.py` — `setup_logger()` at project root ✅

**This Feature Blocks:** None (only feature in epic)

**Integration Points:**
- `parse_args()` → `main()`: main() calls parse_args() instead of inline argparse
- `main()` → `fetch_game_data()`: adds request_timeout kwarg
- `main()` → `setup_logger()`: replaces hardcoded "INFO" with args.log_level

---

## Data Flow & Consumption

**Overview:** CLI args → `parse_args()` → `main()` logic → `fetch_game_data()` → `result_path`

### Step-by-Step Data Flow

1. **Input:** `sys.argv` passed to `parse_args(argv=None)` → returns `args` namespace with 8 fields:
   - `args.season` (int, default 2025), `args.current_week` (int, default 17)
   - `args.log_level` (str, default 'INFO'), `args.e2e_test` (bool, default False)
   - `args.request_timeout` (int, default 30), `args.historical_season` (bool, default False)
   - `args.output` (str or None), `args.weeks` (str or None)

2. **Logger Setup:** `args.log_level` → `setup_logger("game_data_fetcher", args.log_level, False, None, "standard")` → `logger`
   - Previously: hardcoded "INFO" (anti-pattern); After: user-controlled

3. **Derived Variables (local vars from args):**
   - `season = args.season` (was: `args.season if args.season else NFL_SEASON`)
   - `current_week = args.current_week` (was: `args.current_week if args.current_week else CURRENT_NFL_WEEK`)
   - `output_path = Path(args.output) if args.output else None` (existing logic preserved)

4. **Historical Override:** If `args.historical_season`:
   - `current_week` overridden to `18` (all 18 weeks)
   - Log: `"Historical season mode: fetching all 18 weeks for {args.season}"`

5. **Weeks + Output Path Resolution (if/elif/else):**
   - If `args.e2e_test`: `weeks = [1]`, `output_path = Path("/tmp/game_data_e2e_test.csv")`
   - elif `args.weeks`: `weeks = parse_weeks(args.weeks)`, `output_path` unchanged
   - else: `weeks = None`, `output_path` unchanged

6. **Fetch Call:**
   ```python
   fetch_game_data(output_path, season, current_week, weeks, request_timeout=args.request_timeout)
   ```
   - Interface: `player-data-fetcher/game_data_fetcher.py:520-527`
   - `rate_limit_delay` NOT passed (unused per KAI-10 S2 Q1 Option C decision)

7. **Output:** `result_path` — logged/displayed (existing behavior preserved)

### Data Consumers

| Data Item | Producer | Consumer | Notes |
|-----------|----------|----------|-------|
| `args.log_level` | `parse_args()` | `setup_logger()` | Controls logging verbosity |
| `args.season` | `parse_args()` | `fetch_game_data()` | Via local `season` variable |
| `args.current_week` | `parse_args()` | `fetch_game_data()` | Via local `current_week`; overrideable to 18 by `--historical-season` |
| `args.historical_season` | `parse_args()` | `main()` logic | Overrides `current_week` to 18 |
| `args.e2e_test` | `parse_args()` | `main()` logic | Overrides `weeks` to `[1]` and `output_path` to `/tmp` |
| `args.weeks` | `parse_args()` | `parse_weeks()` | Only consumed when `e2e_test=False` |
| `args.output` | `parse_args()` | `fetch_game_data()` | Via `output_path`; overridden by `--e2e-test` |
| `args.request_timeout` | `parse_args()` | `fetch_game_data()` | Passed as `request_timeout=` kwarg directly |
| `output_path` (resolved) | `main()` logic | `fetch_game_data()` | `/tmp` in E2E mode, `None`/custom otherwise |
| `weeks` (resolved) | `main()` logic | `fetch_game_data()` | `[1]` in E2E, parsed list or `None` otherwise |

---

## Test Strategy

*(Defined in `test_strategy.md` — S4 output. Full detail there.)*

### Unit Tests (tests/root_scripts/test_run_game_data_fetcher.py — Task 5)

**1. test_has_parse_args**
- Purpose: Verify parse_args exists at module level and is callable
- File: `tests/root_scripts/test_run_game_data_fetcher.py`
- Expected: `callable(run_game_data_fetcher.parse_args) is True`

**2. test_parse_args_defaults**
- Purpose: Verify all 6 defaults correct (argparse as single source of truth)
- File: `tests/root_scripts/test_run_game_data_fetcher.py`
- Expected: season=2025, current_week=17, log_level='INFO', e2e_test=False, request_timeout=30, historical_season=False

**3. test_no_subprocess**
- Purpose: Verify runner does not import subprocess
- File: `tests/root_scripts/test_run_game_data_fetcher.py`
- Expected: `not hasattr(run_game_data_fetcher, 'subprocess')`

### Coverage Matrix

| Method/Behavior | Unit Test | Structural | CLI Smoke | Edge Case | Coverage |
|---|---|---|---|---|---|
| parse_args() callable at module level | U1 ✅ | — | — | — | 100% |
| All 6 defaults correct | U2 ✅ | — | C2 ✅ | — | 100% |
| No subprocess import | U3 ✅ | — | — | — | 100% |
| No config import | — | S1 ✅ | C1 ✅ | — | 100% |
| No os.chdir | — | S2 ✅ | C1 ✅ | E6 ✅ | 100% |
| E2E mode (/tmp, week 1) | — | — | C3 ✅ | E2 ✅ | 100% |
| Log-level wired | — | — | C4 ✅ | — | 100% |
| Historical season | U2 ✅ | — | C5 ✅ | E3 ✅ | 100% |
| Backward compat | U2 ✅ | — | C6 ✅ | — | 100% |
| Request-timeout passthrough | U2 ✅ | — | C3 ✅ | E4 ✅ | 100% |
| Regression suite | — | — | C7 ✅ | — | 100% |

**Overall Coverage:** 100% (18/18 test scenarios mapped to tasks)

---

## Edge Cases

**Total Identified:** 7 edge cases from test_strategy.md (all covered by Tasks 3 and 4)

### Argparse Validation (4 cases)

**1. --log-level lowercase (debug) → SystemExit**
- Scenario: User passes lowercase log level
- Handling: argparse `choices=` enforces uppercase values; rejects case-insensitively ✅
- Status: Handled by Task 3 (argparse choices= mechanism)
- Test: E1

**2. --log-level invalid (VERBOSE) → SystemExit**
- Scenario: User passes unrecognized log level
- Handling: argparse `choices=` enforces list; SystemExit code 2 ✅
- Status: Handled by Task 3 (argparse choices= mechanism)
- Test: E1

**3. --request-timeout non-int (abc) → SystemExit**
- Scenario: User passes non-integer timeout
- Handling: argparse `type=int` rejects; SystemExit code 2 ✅
- Status: Handled by Task 3 (argparse type=int mechanism)
- Test: E4

**4. --season non-int (abc) → SystemExit**
- Scenario: User passes non-integer season
- Handling: argparse `type=int` rejects; SystemExit code 2 ✅
- Status: Handled by Task 3 (existing type=int, unchanged)
- Test: E5

### Precedence Rules (2 cases)

**5. --e2e-test + --weeks conflict**
- Scenario: User passes both --e2e-test and --weeks flags
- Handling: `if args.e2e_test:` block comes BEFORE `elif args.weeks:` → e2e wins (weeks=[1])
- Status: Handled by Task 4 (if/elif ordering in main())
- Test: E2

**6. --historical-season + --current-week conflict**
- Scenario: User passes both --historical-season and --current-week
- Handling: historical block runs after `current_week = args.current_week` → overrides to 18
- Status: Handled by Task 4 (historical block after initial assignment)
- Test: E3

### Path Handling (1 case)

**7. Import from any CWD (no os.chdir)**
- Scenario: User runs `python run_game_data_fetcher.py` from a non-project-root directory
- Handling: `_script_dir = Path(__file__).parent` is absolute, not CWD-relative
- Status: Handled by Task 1 (Path(__file__).parent guarantees correct path)
- Test: E6

**Handling Summary:**
- Handled by argparse mechanism (Tasks 3): 4 cases
- Handled by if/elif ordering (Task 4): 2 cases
- Handled by Path(__file__).parent (Task 1): 1 case

---

## Performance Considerations

**Analysis:**
- This refactoring adds no new computation — only argument parsing changes
- `parse_args()` is O(1) relative to existing inline argparse
- E2E mode reduces scope to Week 1 only: completes in ≤180s (much less than full run)
- sys.path.insert() at module level: same cost as inside try block (negligible, ~0.001s)

**Impact Assessment:**
- No performance regression introduced
- E2E mode is a net positive (enables fast testing)
- Module-level imports: loaded once at import time (same as before)

**Conclusion:** No performance concerns. No optimization tasks needed.

---

## Mock Audit

**External Dependencies Requiring Mocks:** None

**Rationale:**
The 3 unit tests (test_strategy.md U1, U2, U3) only test:
- Module attributes (parse_args callable): no external calls needed
- parse_args([]) with empty argv: pure argparse, no I/O
- hasattr for subprocess: no external calls needed

No mocking required for the unit tests. The CLI smoke tests (C1-C7) run the actual script
with real data — no mocks.

**Mocking Strategy:** Not needed for this feature. Tests designed to avoid mocking by:
1. Testing parse_args([]) directly (no main() needed)
2. Using hasattr/callable introspection (no execution needed)

---

## Implementation Phasing

**Phase 1: Module restructure + import removal (Tasks 1, 2)**
- Duration: ~15 minutes
- Tasks: Remove os.chdir/original_cwd, move sys.path + imports to module level, remove config import
- Checkpoint: `python -c "import run_game_data_fetcher; print('OK')"` must succeed
- Rollback: git checkout run_game_data_fetcher.py

**Phase 2: Extract parse_args() + add 4 new args (Task 3)**
- Duration: ~20 minutes
- Tasks: Create parse_args(argv=None) function, fix defaults, add --e2e-test/--log-level/--request-timeout/--historical-season
- Checkpoint: `python run_game_data_fetcher.py --help` shows 8 args; `parse_args([])` returns correct defaults
- Rollback: git checkout run_game_data_fetcher.py

**Phase 3: Wire new args in main() (Task 4)**
- Duration: ~20 minutes
- Tasks: Wire log_level to setup_logger, replace historical detection, add E2E mode block, pass request_timeout to fetch_game_data
- Checkpoint: `pytest tests/ -v` 100% pass (existing tests)
- Rollback: git checkout run_game_data_fetcher.py

**Phase 4: Create test file (Task 5)**
- Duration: ~10 minutes
- Tasks: Create test_run_game_data_fetcher.py with 3 tests
- Checkpoint: `pytest tests/root_scripts/test_run_game_data_fetcher.py -v` shows 3 tests passed
- Rollback: rm tests/root_scripts/test_run_game_data_fetcher.py

**Rollback Strategy:**
- All changes to `run_game_data_fetcher.py` → `git checkout run_game_data_fetcher.py`
- New test file → `rm tests/root_scripts/test_run_game_data_fetcher.py`
- Both rollbacks fully restore pre-refactor state

---

## S5 v2 Validation Loop Completion

**Phase 1 Status:**
- [x] Draft Creation complete (~70% quality baseline)
- [x] All 11 dimension sections created
- [x] Requirements mapping tables complete (11/11 requirements, 18/18 tests)
- [x] Algorithm traceability matrix drafted (32 mappings)

**Phase 2 Status:**
- [x] Validation Loop complete (3 consecutive clean rounds — Rounds 2, 3, 4)
- [x] Total validation rounds executed: 4
- [x] All 7 master dimensions validated
- [x] All 11 S5-specific dimensions validated

**11 Dimension Validation Summary (after validation loop):**
1. Requirements Completeness: ✅ (11/11 reqs, 18/18 tests traced)
2. Interface & Dependency Verification: ✅ (2 interfaces from source: game_data_fetcher.py:520, LoggingManager.py:190)
3. Algorithm Traceability: ✅ (32 mappings)
4. Task Specification Quality: ✅ (5 tasks with ACs, locations, deps, tests)
5. Data Flow & Consumption: ✅ (7-step flow + data consumers table — added Round 1)
6. Error Handling & Edge Cases: ✅ (7 edge cases with handling strategy)
7. Integration & Compatibility: ✅ (backward compat, no scope creep, interfaces unchanged)
8. Test Coverage Quality: ✅ (Coverage Matrix 18/18, Mock Audit complete)
9. Performance & Dependencies: ✅ (no new computation, E2E ≤180s documented)
10. Implementation Readiness: ✅ (4-phase plan with checkpoint + rollback per phase)
11. Spec Alignment & Cross-Validation: ✅ (all 9 spec ACs traced, all REQs covered)

**Completeness Metrics:**
- Requirements in spec.md: 11
- Requirements with implementation tasks: 11
- Coverage: 11/11 = 100%
- Algorithm mappings: 32
- External dependencies verified: 2/2 = 100%

**Quality Metrics:**
- Tasks with acceptance criteria: 5/5 = 100%
- Tasks with implementation location: 5/5 = 100%
- Tasks with test coverage: 5/5 = 100%
- Edge cases identified: 7

**Confidence Assessment:**
- [x] Confidence level: HIGH (validation loop complete — 4 rounds, 1 issue fixed, 3 consecutive clean)
- [x] No blockers identified
- [x] No open questions
- [x] No deferred issues

**Gate 5 Ready:** ✅ YES — Validation Loop passed, presenting to user for approval

---

## Version History

**v1.0 (2026-02-19) - Validation Loop Passed:**
- Data Flow & Consumption section added (D5 gap fixed — Round 1)
- All 18 dimensions validated (4 rounds, 1 issue found and fixed, 3 consecutive clean)
- Confidence: HIGH

**v0.1 (2026-02-19) - Phase 1 Complete (Draft Creation):**
- Initial draft created
- All 11 dimension sections included
- 5 implementation tasks (11/11 requirements, 18/18 test scenarios covered)
- 32 algorithm mappings
- 2 external interfaces verified from actual source code
- 7 edge cases documented

---

## User Approval

**Approval Status:** ⏳ PENDING REVIEW

**STATUS:** ⏳ PENDING USER APPROVAL

**Next Step:** Complete Validation Loop (Phase 2), then present for Gate 5 approval
