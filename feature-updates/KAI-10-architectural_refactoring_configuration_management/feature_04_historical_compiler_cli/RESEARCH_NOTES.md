# Research Notes: Feature 04 — historical_compiler_cli

**Created:** 2026-02-18
**Stage:** S2.P1.I1 — Feature-Level Discovery

---

## Files Researched

| File | Lines Read | Purpose |
|------|-----------|---------|
| `compile_historical_data.py` | All (322 lines) | Main runner — current args, main(), compile_season_data() |
| `historical_data_compiler/constants.py` | All (157 lines) | Constants to remove + keep |
| `historical_data_compiler/http_client.py` | All (204 lines) | BaseHTTPClient constructor — already accepts params |
| `historical_data_compiler/player_data_fetcher.py` | Lines 1-60 | ESPN_PLAYER_LIMIT location |
| `tests/unit/test_compile_historical_data_cli.py` | All (79 lines) | Existing CLI tests |
| `tests/unit/test_compile_historical_data_logger.py` | All (139 lines) | Logger setup tests |
| `tests/unit/test_compile_historical_data_info_logs.py` | All (70 lines) | INFO log tests |
| `tests/integration/test_historical_data_compiler_integration.py` | All (116 lines) | Integration tests |
| `tests/historical_data_compiler/test_constants.py` | All (178 lines) | Constants tests |
| `feature_01_refactor_player_data_fetcher/spec.md` | All | Design pattern reference |
| `DISCOVERY.md` | All | Epic context, Finding 7 |

---

## Key Findings

### F1: Existing CLI Args in compile_historical_data.py

Found at lines 59-101 in `parse_args()`:
```python
--year       (int, optional) — NFL season year
--verbose    (-v, flag) — Enable verbose logging
--enable-log-file (flag) — Enable file logging
--output-dir (Path, default None) — Override output directory
```

**--verbose behavior (line 264):**
```python
log_level = "DEBUG" if args.verbose else "INFO"
```
This maps `--verbose` directly to DEBUG logging level.

**No Settings class** — args used directly via `args.xxx` in main().

### F2: constants.py — Constants to Remove

Two CLI-configurable constants in `historical_data_compiler/constants.py`:
- Line 98: `REQUEST_TIMEOUT = 30.0` → becomes argparse default for `--timeout`
- Line 101: `RATE_LIMIT_DELAY = 0.3` → becomes argparse default for `--rate-limit-delay`

**Constants to KEEP** (non-CLI):
- `MAX_RETRY_ATTEMPTS = 3` (line 104) — internal, non-configurable
- `ESPN_USER_AGENT` (line 106-110) — internal, non-configurable
- `MIN_SUPPORTED_YEAR = 2021`, `REGULAR_SEASON_WEEKS = 17`, `VALIDATION_WEEKS = 18` — non-CLI
- All ESPN mappings, file name constants — non-CLI

### F3: http_client.py — Already Has Constructor Params

`BaseHTTPClient.__init__` at lines 62-82 **already accepts** constructor params:
```python
def __init__(
    self,
    timeout: float = REQUEST_TIMEOUT,      # default from constants
    rate_limit_delay: float = RATE_LIMIT_DELAY,  # default from constants
    user_agent: str = ESPN_USER_AGENT
):
```

**Key finding:** No refactoring needed in http_client.py beyond removing the constants import. The defaults currently come from constants, but these defaults will move to argparse after the refactor.

**BaseHTTPClient creation (compile_historical_data.py line 188):**
```python
http_client = BaseHTTPClient()  # ← Change to pass args.timeout, args.rate_limit_delay
```

### F4: compile_season_data() Signature

Current (line 170):
```python
async def compile_season_data(year: int, output_dir: Path) -> None:
```

After refactor: needs to accept timeout and rate_limit_delay to pass to BaseHTTPClient.
- **Option A:** Add explicit params: `compile_season_data(year, output_dir, timeout, rate_limit_delay)`
- **Option B:** Accept a Settings object: `compile_season_data(year, output_dir, settings)`

Decision pending user input (Q4 in checklist).

### F5: Test Coverage — No Test Deletion Required

`tests/historical_data_compiler/test_constants.py` does **NOT** test REQUEST_TIMEOUT or RATE_LIMIT_DELAY. Tests in this file cover:
- ESPN team mappings, position mappings, ALL_NFL_TEAMS, FANTASY_POSITIONS
- Season config (REGULAR_SEASON_WEEKS, MIN_SUPPORTED_YEAR)
- normalize_team_abbrev function
- JSON file name constants

**Result:** No test deletion required for historical_data_compiler. Compare to Feature 01 where 11 tests were deleted from test_config.py.

Existing CLI tests cover:
- `--enable-log-file` flag parsing (test_compile_historical_data_cli.py — 3 tests)
- setup_logger() integration with `--verbose` logic (test_compile_historical_data_logger.py — 4 tests)
- INFO log quality (test_compile_historical_data_info_logs.py — 2 tests)
- Integration: flag parsing with/without `--enable-log-file` (integration test — 3 tests)

**Total existing CLI-related tests: 12 tests** — all must continue to pass.

### F6: player_data_fetcher.py — Player Limit

`historical_data_compiler/player_data_fetcher.py` has:
```python
ESPN_PLAYER_LIMIT = 1500  # Max players to fetch (line 38)
```

This is a **module-level constant**, NOT from constants.py, NOT a CLI arg in current code. If E2E mode or debug mode needs to reduce player count, this module would need to be refactored to accept a player limit parameter. This is a potential scope addition (addressed in Q1).

### F7: E2E Mode — Execution Path

In E2E mode, the script should compile 1 year. The compile_season_data() function executes 5 phases:
1. Fetch schedule (1 ESPN API call)
2. Fetch game data (multiple ESPN API calls + weather calls)
3. Fetch player data (multiple ESPN Fantasy API calls — main bottleneck with 1500 player limit)
4. Calculate team data (local, fast)
5. Generate weekly snapshots (local, fast)

The rate limiting (RATE_LIMIT_DELAY = 0.3s) is applied per request in `http_client.py`. With 1500 players and multiple API calls, the timing depends heavily on request count.

### F8: Output Directory Behavior (for E2E)

Current main() at lines 292-295:
```python
if output_dir.exists():
    logger.warning(f"Output directory already exists: {output_dir}")
    logger.warning("Existing data will be overwritten")
    shutil.rmtree(output_dir)  # ← deletes existing data
```

"Skip backups" in spec seed likely means: in E2E mode, either use temp dir OR skip this deletion. Decision pending Q5.

### F9: Design Pattern Alignment with Feature 01

| Aspect | Feature 01 | Feature 04 | Notes |
|--------|-----------|-----------|-------|
| Universal args | ✅ --debug, --e2e-test, --log-level | Same | Consistent |
| Settings class | ✅ @dataclass in separate module | Pending Q4 | Simpler architecture here |
| E2E data limiting | espn_player_limit=100 | Pending Q1 | Different script, similar concept |
| --verbose | N/A (no --verbose before) | Preserve + map to DEBUG | Backward compat |
| Constants removed | 15 from config.py | 2 from constants.py | Smaller scope |
| Test deletions | 11 tests deleted | 0 tests deleted | constants.py tests don't cover the 2 removed constants |

---

## Integration Points

- `historical_data_compiler/http_client.py` — Primary integration point for timeout/rate_limit_delay
- `tests/unit/test_compile_historical_data_*.py` — 9 existing tests must continue to pass
- `tests/integration/test_historical_data_compiler_integration.py` — 3 integration tests must continue to pass
- `tests/historical_data_compiler/test_constants.py` — Must pass after constant removal (doesn't test removed constants)
- Feature 08 (integration_test_framework) — Will wrap E2E mode in master runner

---

## Open Questions (→ checklist.md)

1. **Q1** — E2E mode data limiting: player limit reduction needed?
2. **Q2** — --debug reduced scope: what limits apply to this script?
3. **Q3** — Additional args: --weeks/--validate/--clean/--skip-backups in scope?
4. **Q4** — Settings dataclass: apply pattern or pass args directly as function params?
5. **Q5** — E2E output directory: temp dir vs real sim_data?

---

## Gate 1 Verification

- [x] Can cite EXACT files/classes to modify (with line numbers) ✅
- [x] Have READ source code (actual method signatures) ✅
- [x] Have verified data structures from source ✅
- [x] Have reviewed DISCOVERY.md for context ✅
