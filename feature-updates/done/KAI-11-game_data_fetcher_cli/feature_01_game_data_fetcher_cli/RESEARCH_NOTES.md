## Research Notes: game_data_fetcher_cli

**Feature:** feature_01_game_data_fetcher_cli
**Created:** 2026-02-19 (S2.P1.I1)

---

## Files Researched

### 1. run_game_data_fetcher.py (to modify)

**Path:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/run_game_data_fetcher.py`
**Lines:** 174

**Key locations:**

| Anti-pattern | Location | Notes |
|-------------|----------|-------|
| `import os` | Line 23 | Remove if os.chdir is only use |
| `--season` default=None | Line 60, 63 | Change default to 2025 |
| `--current-week` default=None | Line 79, 82 | Change default to 17 |
| `original_cwd = os.getcwd()` | Line 93 | Remove |
| `os.chdir(fetcher_dir)` | Line 97 | Remove |
| `sys.path.insert(0, str(fetcher_dir))` | Line 100 | Keep — move to module level |
| `sys.path.insert(0, str(script_dir))` | Line 101 | Keep — move to module level |
| `from config import NFL_SEASON, CURRENT_NFL_WEEK` | Line 105 | Remove |
| `setup_logger("game_data_fetcher", "INFO", ...)` | Line 109 | Change "INFO" → args.log_level |
| `season = args.season if args.season else NFL_SEASON` | Line 112 | Simplify to `season = args.season` |
| `current_week = args.current_week if args.current_week else CURRENT_NFL_WEEK` | Line 113 | Simplify to `current_week = args.current_week` |
| `if args.season and args.season < NFL_SEASON:` | Line 116 | Replace with `if args.historical_season:` |
| `fetch_game_data(...)` call (no request_timeout) | Lines 143-148 | Add `request_timeout=args.request_timeout` |
| `os.chdir(original_cwd)` | Line 169 | Remove |

**Functions/blocks to preserve:**
- `parse_weeks()` helper function (lines 28-51) — keep as-is
- argparse setup (lines 56-84) — refactor: extract to `parse_args()`, add 4 new args, fix defaults
- Script/fetcher dir construction (lines 87-90) — keep, move before try block
- Output path construction (lines 121-124) — keep logic
- fetch_game_data call (lines 143-148) — keep, add request_timeout param
- Summary/print block (lines 153-160) — keep as-is
- Error handling (lines 162-166) — keep
- `if __name__ == "__main__":` block (lines 172-173) — keep

---

### 2. run_player_fetcher.py (pattern reference)

**Path:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/run_player_fetcher.py`
**Lines:** 194

**Key patterns to follow:**

| Pattern | Location | Notes |
|---------|----------|-------|
| Module-level sys.path inserts | Lines 22-23 | Before imports, no try/finally |
| `parse_args(argv=None)` function | Lines 28-149 | Module-level, not inside main() |
| `--e2e-test` flag definition | Lines 35-40 | `action='store_true'` |
| `--log-level` with choices | Lines 41-47 | choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'] |
| `--request-timeout` int arg | Lines 124-128 | default=30 |
| `if __name__ == "__main__"` | Lines 190-193 | calls parse_args() + main logic |

**E2E override pattern (player fetcher uses temp dir, game fetcher uses fixed path):**
```python
# player_fetcher pattern (random tmp dir):
if args.e2e_test:
    tmp_dir = tempfile.mkdtemp(prefix='player_fetcher_e2e_')

# game_fetcher pattern (fixed path — simpler, from epic plan):
if args.e2e_test:
    output_path = Path("/tmp/game_data_e2e_test.csv")
    weeks = [1]
```

---

### 3. player-data-fetcher/game_data_fetcher.py (KAI-10 REQ-09 — already done)

**Path:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/player-data-fetcher/game_data_fetcher.py`

**KAI-10 REQ-09 confirmed applied:**
- Constructor: `def __init__(self, data_folder, season=2025, current_week=17, request_timeout=30, rate_limit_delay=0.2)`
- `fetch_game_data()`: `def fetch_game_data(output_path=None, season=2025, current_week=17, weeks=None, request_timeout=30, rate_limit_delay=0.2) -> Path`

**This file is NOT modified by KAI-11.** Runner just needs to pass `request_timeout=args.request_timeout`.

---

### 4. tests/root_scripts/test_root_scripts.py (test pattern)

**Path:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/tests/root_scripts/test_root_scripts.py`
**Lines:** 778

**TestRunPlayerFetcher (pattern to follow, lines 95-113):**
```python
class TestRunPlayerFetcher:
    def test_run_player_fetcher_has_parse_args(self):
        import run_player_fetcher
        assert hasattr(run_player_fetcher, 'parse_args')
        assert callable(run_player_fetcher.parse_args)

    def test_run_player_fetcher_has_create_settings_dict(self):
        import run_player_fetcher
        assert hasattr(run_player_fetcher, 'create_settings_dict')
        assert callable(run_player_fetcher.create_settings_dict)

    def test_run_player_fetcher_no_subprocess(self):
        import run_player_fetcher
        assert not hasattr(run_player_fetcher, 'subprocess')
```

**New test file location:** `tests/root_scripts/test_run_game_data_fetcher.py`
**This file is NOT modified.** New test file is a separate file.

---

## Integration Points

- `fetch_game_data()` call: runner passes `request_timeout=args.request_timeout` — already-compatible signature
- `setup_logger()`: same call, just changes second arg from `"INFO"` to `args.log_level`
- `parse_weeks()`: unchanged helper function (preserved)
- sys.path: moves from inside try block to module level (behavior identical)

---

## Key Design Decisions Confirmed

1. **No `create_settings_dict()`** needed (unlike player fetcher) — game data fetcher calls `fetch_game_data()` directly, no settings dict bridge
2. **E2E output: `/tmp/game_data_e2e_test.csv`** — hardcoded fixed path (not random tmpdir like player fetcher)
3. **`parse_args()` extracted** — required for REQ-11 unit tests
4. **`os.chdir()` fully removed** — try/finally block simplified (may eliminate try entirely if no other errors to catch)
5. **`import os` removed** — no longer needed after removing os.chdir/os.getcwd
