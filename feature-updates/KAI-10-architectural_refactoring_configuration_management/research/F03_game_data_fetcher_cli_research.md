## Research Notes: Feature 03 — game_data_fetcher_cli

**Created:** 2026-02-18 (S2.P1.I1)
**Feature:** feature_03_game_data_fetcher_cli
**Researcher:** Secondary-B

---

## Files Researched

### 1. `run_game_data_fetcher.py` (Runner Script)

**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/run_game_data_fetcher.py`

**Current architecture:**
- Uses `os.chdir(fetcher_dir)` + `sys.path.insert()` then imports — same anti-pattern as Feature 01's subprocess approach
- Has argparse with 4 args (all default=None, relying on config fallback)
- Config fallback pattern: `from config import NFL_SEASON, CURRENT_NFL_WEEK` inside try/chdir block, then `season = args.season if args.season else NFL_SEASON`
- Hardcoded `setup_logger("game_data_fetcher", "INFO", False, None, "standard")` — log level not wired to CLI
- Calls `fetch_game_data(output_path, season, current_week, weeks)` directly (sync — not asyncio)
- Historical season logic: `if args.season and args.season < NFL_SEASON: current_week = 18`
- Has `finally: os.chdir(original_cwd)` to restore directory

**Existing args (4):**

| Argument | Type | Current Default | Issue |
|----------|------|-----------------|-------|
| `--season` | int | None (→ NFL_SEASON from config) | Config fallback |
| `--output` | str | None (→ "data/game_data.csv") | OK |
| `--weeks` | str | None (→ all weeks 1..current) | OK |
| `--current-week` | int | None (→ CURRENT_NFL_WEEK from config) | Config fallback |

**Missing universal args:** `--debug`, `--e2e-test`, `--log-level`

**os.chdir issue:** After removing config import and passing season/current_week as CLI args, os.chdir() is no longer needed. The internal `game_data_fetcher.py` uses `Path(__file__).parent` for its own paths (COORDINATES_JSON), not the working directory. sys.path.insert() alone is sufficient.

### 2. `player-data-fetcher/game_data_fetcher.py` (Internal Module — Feature 01 scope)

**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/player-data-fetcher/game_data_fetcher.py`

**IMPORTANT:** This module is being refactored by Feature 01 (REQ-09). Feature 03 does NOT re-refactor it — only the runner script.

**Current interface:**
```python
class GameDataFetcher:
    def __init__(
        self,
        data_folder: Path,
        season: int = NFL_SEASON,       # Currently from config
        current_week: int = CURRENT_NFL_WEEK  # Currently from config
    ):

def fetch_game_data(
    output_path: Optional[Path] = None,
    season: int = NFL_SEASON,           # Currently from config
    current_week: int = CURRENT_NFL_WEEK, # Currently from config
    weeks: Optional[List[int]] = None
) -> Path:
```

**Config imports (line 30-33):**
```python
from config import (
    CURRENT_NFL_WEEK, NFL_SEASON, GAME_DATA_CSV, COORDINATES_JSON,
    REQUEST_TIMEOUT, RATE_LIMIT_DELAY
)
```

**After Feature 01 REQ-09 (interface will change):**
- `CURRENT_NFL_WEEK`, `NFL_SEASON` defaults will be hardcoded values (not from config)
- `REQUEST_TIMEOUT` and `RATE_LIMIT_DELAY` will become constructor parameters per REQ-09
- Feature 01 spec REQ-09 says: "Add `request_timeout` and `rate_limit_delay` as parameters to `fetch_game_data()`"
- COORDINATES_JSON stays in config (non-CLI internal constant)

**REQUEST_TIMEOUT usage:** Lines 174 and 286 — used directly in httpx.get() calls (not via self)
**RATE_LIMIT_DELAY:** Imported at line 32 but NOT used anywhere in the file (no calls found)

**Key implication for Feature 03:** After Feature 01, `fetch_game_data()` will accept `request_timeout` and `rate_limit_delay` parameters. Feature 03's runner will need to decide whether to pass these from CLI args or use defaults. DISCOVERY.md is silent on this for Feature 03.

### 3. `player-data-fetcher/config.py`

**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/player-data-fetcher/config.py`

**Constants used by runner:**
- `NFL_SEASON = 2025` — runner fallback default
- `CURRENT_NFL_WEEK = 17` — runner fallback default
- `REQUEST_TIMEOUT = 30` — used in internal module methods
- `RATE_LIMIT_DELAY = 0.2` — imported by internal module but not used

**Constants needed for runner's argparse defaults:**
- `--season` default: **2025**
- `--current-week` default: **17**

### 4. `utils/LoggingManager.py` — `setup_logger()` signature

```python
def setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    log_format: str = 'standard',
    enable_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> logging.Logger:
```

**Current runner call:** `setup_logger("game_data_fetcher", "INFO", False, None, "standard")`
**After refactor:** `setup_logger("game_data_fetcher", log_level, False, None, "standard")`
where `log_level = "DEBUG" if args.debug else args.log_level`

### 5. Tests

**`tests/player-data-fetcher/test_game_data_fetcher.py`:**
- Tests internal `GameDataFetcher` class only
- Bypasses `__init__` using `patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None)`
- Uses `with patch('game_data_fetcher.REQUEST_TIMEOUT', 30)` — will need updating after Feature 01 REQ-09
- No tests for `run_game_data_fetcher.py` runner script

**No tests exist for `run_game_data_fetcher.py`** — tests are out of scope for Feature 03 (runner scripts are tested via E2E mode per DISCOVERY.md).

---

## Integration Points

1. **Feature 01 dependency:** Feature 03 runner will call the refactored `fetch_game_data()` with parameters from CLI args, NOT from config. Must align with Feature 01's final `fetch_game_data()` signature (especially request_timeout/rate_limit_delay params).

2. **Feature 08 dependency:** Feature 08 wraps Feature 03's `--e2e-test` mode in integration test runner. The E2E behavior (1 week, ≤180s, exit code 0) must be precisely specified.

---

## Open Questions (Checklist)

1. Should `--request-timeout` and `--rate-limit-delay` be CLI args on `run_game_data_fetcher.py`? After Feature 01 REQ-09, `fetch_game_data()` will accept these — Feature 03 runner needs to decide pass-through vs defaults.

2. Are `--data-folder`, `--validate`, `--clean` in scope? (seeded in feature README, absent from DISCOVERY.md)

3. E2E test data limit: Week 1 only, or 1 week at current position?

4. Debug mode data scope: What does "reduced data scope" mean for game data fetcher?

5. Historical season detection after config removal: How should `if season < NFL_SEASON: current_week = 18` behave when NFL_SEASON is no longer importable?
