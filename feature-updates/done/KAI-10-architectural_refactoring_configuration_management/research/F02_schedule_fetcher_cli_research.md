# Research Notes: Feature 02 — schedule_fetcher_cli

**Created:** 2026-02-18
**Phase:** S2.P1.I1

---

## Files Researched

| File | Location | Line Range | Purpose |
|------|----------|------------|---------|
| `run_schedule_fetcher.py` | `/run_schedule_fetcher.py` | 1-88 | Entry-point runner — argparse, main() |
| `ScheduleFetcher.py` | `schedule-data-fetcher/ScheduleFetcher.py` | 1-241 | Core fetcher class |
| `test_run_schedule_fetcher.py` | `tests/root_scripts/` | 1-339 | Existing CLI + log tests |
| `test_schedule_fetcher_integration.py` | `tests/integration/` | 1-459 | E2E integration tests (subprocess) |
| `test_schedule_fetcher_logs.py` | `tests/unit/` | 1-71 | Log quality tests (different ScheduleFetcher) |

---

## Gate 1 Verification (Research Completeness Audit)

- **Category 1 — Exact files/classes to modify (with line numbers):**
  - `run_schedule_fetcher.py` — lines 31, 38-52, 56, 64 (NFL_SEASON, argparse, output_path, fetch call)
  - `schedule-data-fetcher/ScheduleFetcher.py` — line 27 (`__init__`), line 41 (timeout), line 76 (`fetch_full_schedule`)
  - May need test updates: `tests/root_scripts/test_run_schedule_fetcher.py`

- **Category 2 — Read source code (actual method signatures):**
  - `ScheduleFetcher.__init__(self, output_path: Path)` — line 27
  - `ScheduleFetcher.fetch_full_schedule(self, season: int)` — line 76
  - `ScheduleFetcher.export_to_csv(self, schedule: Dict[int, Dict[str, str]])` — line 190
  - `run_schedule_fetcher.main()` — async, lines 34-82

- **Category 3 — Verified data structures from source:**
  - `schedule` type: `Dict[int, Dict[str, str]]` (week → team_abbr → opponent_abbr)
  - Output: CSV with columns `week,team,opponent`
  - ScheduleFetcher constructor: only `output_path: Path` (NO config.py imports)

- **Category 4 — Reviewed DISCOVERY.md:**
  - Finding 5: schedule-data-fetcher has no config.py, NFL_SEASON=2025 hardcoded in runner ✅
  - Notes file Feature 02 scope: `--season, --output-path, --data-folder, --output-format (CSV/JSON/both)` ✅
  - E2E scope: "1 week, 1 league, or minimal dataset" for fetchers ✅

---

## run_schedule_fetcher.py — Key Findings

### Current State
- **Lines 19-22:** Imports — `argparse`, `asyncio`, `sys`, `Path`
- **Line 27-30:** Path manipulation to add `schedule-data-fetcher/` and `player-data-fetcher/` to sys.path
- **Line 30:** `from ScheduleFetcher import ScheduleFetcher` — DIRECT import (NOT subprocess)
- **Line 31:** `NFL_SEASON = 2025` — hardcoded module-level constant ← PRIMARY target for CLI

### Current argparse (lines 37-43)
```python
parser.add_argument('--enable-log-file', action='store_true', ...)
```
Only 1 arg. No --season, no --output-path, nothing else.

### Logger setup (lines 46-52)
```python
logger = setup_logger(
    name="schedule_fetcher",
    level="INFO",      # ← hardcoded 'INFO' — target for --log-level
    log_to_file=args.enable_log_file,
    log_file_path=None,
    log_format="standard"
)
```

### Output path (line 56)
```python
output_path = Path(__file__).parent / "data" / "season_schedule.csv"
```
Hardcoded relative path. No config source — target for `--output-path`.

### Fetch call (lines 64-65)
```python
schedule = await fetcher.fetch_full_schedule(NFL_SEASON)
```
Passes `NFL_SEASON` (module constant). After refactor: passes `args.season`.

### Pattern observation
Runner already uses DIRECT import (not subprocess). **NO subprocess→import migration needed** — unlike Feature 01 which required subprocess removal.

---

## ScheduleFetcher.py — Key Findings

### Constructor (line 27)
```python
def __init__(self, output_path: Path):
    self.output_path = output_path
    self.logger = get_logger()
    self.client: Optional[httpx.AsyncClient] = None
```
Simple constructor — no config imports whatsoever. No config.py exists in schedule-data-fetcher/.

### Hardcoded internal values
- **Line 41:** `timeout=30.0` in `_create_client()` — httpx client timeout, NOT imported from config
- **Line 93:** `for week in range(1, 19)` — always fetches weeks 1-18
- **Line 144:** `await asyncio.sleep(0.2)` — rate limiting between requests
- **Line 97:** ESPN API URL hardcoded — `"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"`

### fetch_full_schedule signature (line 76)
```python
async def fetch_full_schedule(self, season: int) -> Dict[int, Dict[str, str]]:
```
Takes `season` as a parameter — already parameterized! ✅

### export_to_csv signature (line 190)
```python
def export_to_csv(self, schedule: Dict[int, Dict[str, str]]):
```
Always writes CSV. No format option. Output path from `self.output_path`.

### No config imports
ScheduleFetcher has ZERO config file imports. Only imports: asyncio, csv, Path, Dict, Optional, Set, get_logger, httpx. **No CLI-configurable constants to strip from a config file.**

---

## Tests — Key Findings

### test_run_schedule_fetcher.py (tests/root_scripts/)
- Tests CLI flag parsing by constructing an IDENTICAL argparse parser (not importing run_schedule_fetcher)
- Tests verify `--enable-log-file` behavior, logger name, logger setup, print replacement
- **Impact of new CLI args:** Tests creating "identical parser" will need updating (they define the parser themselves); tests checking source code patterns should still pass

### test_schedule_fetcher_integration.py (tests/integration/)
- Subprocess-based E2E tests — runs `python run_schedule_fetcher.py [--enable-log-file]`
- Tests check exit code (0 or 1), log file creation, log content
- **Impact:** These tests use `--enable-log-file` or no args — backward compatible since new args have defaults. Tests should continue to pass.

### test_schedule_fetcher_logs.py (tests/unit/)
- Imports from `historical_data_compiler.schedule_fetcher` — this is a DIFFERENT ScheduleFetcher class (historical data compiler's internal ScheduleFetcher, not `schedule-data-fetcher/ScheduleFetcher.py`)
- No impact on Feature 02

---

## Feature 01 Spec Alignment (Design Patterns)

Key patterns from Feature 01 to follow for Feature 02:

| Pattern | Feature 01 | Feature 02 (plan) |
|---------|------------|------------------|
| Runner→main flow | `asyncio.run(main(settings_dict))` via `player_data_fetcher_main.py` | Runner IS the main() — no separate module; settings passed directly |
| Settings class | `@dataclass Settings` + `create_settings_from_dict()` in player_data_fetcher_main.py | `@dataclass Settings` + `create_settings_dict()` in run_schedule_fetcher.py |
| Subprocess migration | Yes (subprocess→direct import) | NOT needed — already direct import |
| Config stripping | 15 constants from config.py | None — no config.py exists |
| Universal args | --debug, --e2e-test, --log-level | Same |
| E2E data limit | espn_player_limit=100 | max_weeks=1 (fetch 1 week only) |
| E2E file handling | Option C: graceful skip if missing | Not applicable (output file always created) |

---

## Open Questions Identified

| Q# | Question | Reason Raised |
|----|----------|---------------|
| Q1 | Does `--data-folder` mean a directory (and filename is fixed `season_schedule.csv`), or is it redundant with `--output-path`? | Notes list BOTH. Code has one combined path: `data/season_schedule.csv`. |
| Q2 | Should `--output-format` support JSON (or CSV/both)? | Notes say `CSV/JSON/both`. ScheduleFetcher only has `export_to_csv()`. Adding JSON = new feature. |
| Q3 | Should `--request-timeout` and/or `--rate-limit-delay` be exposed as CLI args? | Hardcoded in ScheduleFetcher at lines 41, 144. Notes don't explicitly list them for Feature 02. |
| Q4 | Should ScheduleFetcher constructor be extended to accept additional parameters (timeout, rate_limit_delay), or are these purely internal? | No config.py exists — no stripping needed. But "constructor parameter pattern" principle could apply. |
| Q5 | For `--debug` mode, what is the behavioral data limit? (E.g., 3 weeks instead of 18? Same as E2E's 1 week?) | Notes say "reduce data scope" for debug, but don't specify for schedule_fetcher specifically. |

---

## Summary of Confirmed Scope

**Confirmed CLI args to add:**
1. `--season` (int, default 2025) — replaces `NFL_SEASON = 2025` at line 31
2. `--output-path` (str, default `'../data/season_schedule.csv'`) — replaces hardcoded path at line 56
3. `--log-level` (str, default 'INFO') — universal arg; replaces hardcoded 'INFO' at line 49
4. `--debug` (flag, default False) — universal arg
5. `--e2e-test` (flag, default False) — universal arg
6. `--enable-log-file` (flag, default False) — preserved existing arg

**Confirmed NOT needed:**
- Subprocess→import migration (already direct import)
- Config.py stripping (no config.py exists)

**Pending user input (Q1-Q5 above):**
- `--data-folder` (Q1)
- `--output-format` (Q2)
- `--request-timeout` / `--rate-limit-delay` (Q3)
- ScheduleFetcher constructor expansion (Q4)
- Debug mode behavioral scope (Q5)
