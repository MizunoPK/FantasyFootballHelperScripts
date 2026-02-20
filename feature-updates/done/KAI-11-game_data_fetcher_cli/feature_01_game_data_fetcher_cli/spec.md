## Feature Spec: game_data_fetcher_cli

**Status:** APPROVED (Gate 3 — 2026-02-19)
**Last Updated:** 2026-02-19

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Refactor `run_game_data_fetcher.py` to add 4 new CLI args (2 universal + 2 script-specific),
remove `os.chdir()` anti-pattern, remove config imports, wire `--log-level` to `setup_logger()`,
implement E2E test mode (Week 1 only, ≤180s, /tmp output), and create a test file.

**Key scope items:**
- Add universal args: `--e2e-test` (flag), `--log-level` (str, choices: DEBUG/INFO/WARNING/ERROR/CRITICAL)
- Add script-specific args: `--request-timeout` (int, default 30), `--historical-season` (flag)
- Preserve existing args: `--season`, `--output`, `--weeks`, `--current-week`
- Remove `from config import NFL_SEASON, CURRENT_NFL_WEEK`
- Remove `os.chdir(fetcher_dir)` and `os.chdir(original_cwd)` — sys.path only
- Wire `--log-level` to `setup_logger()` (currently hardcoded "INFO")
- E2E mode: `weeks=[1]`, output overridden to `/tmp/game_data_e2e_test.csv`
- Fix argparse defaults: `--season` None → 2025, `--current-week` None → 17
- Replace implicit year-comparison logic with `--historical-season` flag
- Create `tests/root_scripts/test_run_game_data_fetcher.py`

### Relevant Discovery Decisions

- **Solution Approach:** KAI-10 player fetcher pattern — argparse + sys.path only; no config
- **Key Constraints:** Preserve backward compatibility; all existing tests must pass (100%)
- **Dependencies:** KAI-10 F01 already modified `game_data_fetcher.py` (REQ-09) — runner must pass `request_timeout` to `fetch_game_data()`

### Relevant User Answers (from Discovery — resolved in KAI-10 S2)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| `--request-timeout` / `--rate-limit-delay` as CLI args? | `--request-timeout` only (rate-limit-delay unused in code) | REQ-10 adds only `--request-timeout` |
| `--data-folder`, `--validate`, `--clean` in scope? | No — follow DISCOVERY scope strictly | Not in spec |
| E2E test week? | Week 1 — deterministic, reliable historical data | E2E mode uses `weeks=[1]` |
| `--debug` flag? | No — use `--e2e-test --log-level DEBUG` | No `--debug` arg |
| Historical season detection after config removal? | Add `--historical-season` flag explicitly | REQ-09 adds `--historical-season` flag |

### S2 Verification Items (all confirmed before spec finalization)

| Item | Status | Evidence |
|------|--------|---------|
| `fetch_game_data()` accepts `request_timeout` | ✅ Confirmed | KAI-10 applied; signature: `fetch_game_data(..., request_timeout=30, ...)` |
| No new args added to runner since KAI-10 spec | ✅ Confirmed | Still 4 args, all `default=None` |
| `/tmp/game_data_e2e_test.csv` — no conflicts | ✅ Confirmed | Standard /tmp location |
| Test file naming: `test_run_game_data_fetcher.py` | ✅ Confirmed | Consistent with project convention |

---

## Requirements

**Source:** Ported from KAI-10 Feature 03 approved spec (Gate 3, 2026-02-18), verified against
current code state 2026-02-19. REQ-11 (test file) is KAI-11 addition.

---

### REQ-01: Add Universal CLI Args to run_game_data_fetcher.py

**Source:** Epic Request (universal args for all 7 scripts) + KAI-10 F01 precedent

Add the following universal CLI arguments to `run_game_data_fetcher.py` via argparse:

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--e2e-test` | flag | False | E2E test mode: limits to week 1, outputs to /tmp; also used for debug |
| `--log-level` | str | 'INFO' | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

**Total args after refactor:** 8 (4 existing + 2 universal + 2 script-specific)

**Design note:** No `--debug` flag in this epic. `--e2e-test --log-level DEBUG` serves that purpose.

**Derived requirement (testability):** Extract argparse into a module-level `parse_args(argv=None)`
function (same pattern as `run_player_fetcher.py`). This allows unit tests to call
`parse_args([])` directly and verify defaults without running `main()`.

**Pattern reference:** `run_player_fetcher.py` lines 28-149.

---

### REQ-02: Argparse Defaults as Single Source of Truth

**Source:** Epic Request ("argparse defaults = single source of truth")

Change existing `--season` and `--current-week` argparse defaults from `None` to hardcoded values:

| Argument | Current Default | New Default | Config Reference Removed |
|----------|-----------------|-------------|--------------------------|
| `--season` | `None` (→ `NFL_SEASON` from config) | `2025` | `config.NFL_SEASON` |
| `--current-week` | `None` (→ `CURRENT_NFL_WEEK` from config) | `17` | `config.CURRENT_NFL_WEEK` |

Remove the fallback pattern:
```python
# BEFORE (lines 112-113)
season = args.season if args.season else NFL_SEASON
current_week = args.current_week if args.current_week else CURRENT_NFL_WEEK

# AFTER
season = args.season   # already 2025 if not provided
current_week = args.current_week  # already 17 if not provided
```

**Behavior:** Identical to current from the user's perspective (same defaults). Internal source changes from config to argparse.

---

### REQ-03: Remove Config Imports from Runner

**Source:** Epic Request ("Zero CLI constants in config files")

Remove from `run_game_data_fetcher.py`:
```python
# REMOVE (currently line 105 inside try/chdir block)
from config import NFL_SEASON, CURRENT_NFL_WEEK
```

After this change the runner no longer needs `player-data-fetcher/config.py` at runtime.

**Verification:** `grep "from config import" run_game_data_fetcher.py` must return empty.

---

### REQ-04: Remove os.chdir() from Runner

**Source:** KAI-10 F01 design pattern (anti-pattern elimination)

The current runner uses `os.chdir(fetcher_dir)` before imports and restores in finally. This
mutates global process state and creates an implicit working-directory dependency.

**Remove:**
- Line 93: `original_cwd = os.getcwd()`
- Line 97: `os.chdir(fetcher_dir)` (inside try block)
- Line 169: `os.chdir(original_cwd)` (inside finally block)

**Keep:**
- Lines 100-101: `sys.path.insert()` calls — these are correct (sys.path only)

**Move sys.path inserts to module level** (before any imports), consistent with `run_player_fetcher.py` lines 22-23:
```python
# Module-level (before imports)
_script_dir = Path(__file__).parent
_fetcher_dir = _script_dir / "player-data-fetcher"
sys.path.insert(0, str(_fetcher_dir))
sys.path.insert(0, str(_script_dir))
```

**Remove `import os`** if `os` is no longer used anywhere in the file.

**Verification:** `grep "os.chdir" run_game_data_fetcher.py` must return empty.

---

### REQ-05: Wire --log-level to setup_logger

**Source:** Epic Request (universal log-level support)

Change the hardcoded `"INFO"` in setup_logger call:
```python
# BEFORE (line 109)
logger = setup_logger("game_data_fetcher", "INFO", False, None, "standard")

# AFTER
logger = setup_logger("game_data_fetcher", args.log_level, False, None, "standard")
```

**Note:** No `--debug` flag. Users who want DEBUG logging pass `--log-level DEBUG`.

---

### REQ-06: E2E Test Mode (--e2e-test)

**Source:** Epic Request (Section 3: E2E Test Modes) + KAI-10 S2 decisions

When `--e2e-test` flag is set:

1. **Limit fetch to Week 1 only** (reliable past data, always exists):
   ```python
   if args.e2e_test:
       weeks = [1]  # Week 1 — deterministic, reliable historical data
       logger.info("E2E test mode: limiting to week 1")
   ```

2. **Override output path to fixed /tmp path** (user preference: always fixed paths, never random tmpdirs):
   ```python
   if args.e2e_test:
       output_path = Path("/tmp/game_data_e2e_test.csv")
   ```

3. **Script must complete in ≤180 seconds** (exit code 0 on success)

4. **`data/game_data.csv` must NOT be modified** during E2E mode (output goes to /tmp only)

5. **--e2e-test takes precedence over --weeks** (data scope override)

**Also serves as debugging mode:** `--e2e-test --log-level DEBUG` gives verbose debug output.

---

### REQ-07: --log-level Behavior

**Source:** Epic Request (universal argument spec) + KAI-10 F01 precedent

- `--log-level` accepts: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (argparse `choices=`)
- Default: `INFO`
- No `--debug` flag — users pass `--log-level DEBUG` explicitly
- Consistent with `run_player_fetcher.py` pattern (lines 41-47)

---

### REQ-08: Backward Compatibility

**Source:** Derived requirement (zero regression requirement)

- `python run_game_data_fetcher.py` (no args) must behave identically to pre-refactor behavior:
  - `season=2025`, `current_week=17`, `output=data/game_data.csv`, `log_level=INFO`
- `python run_game_data_fetcher.py --season 2024 --output sim_data/game_data.csv` must work identically
- All existing unit tests must pass (100% pass rate, 0 failures)

---

### REQ-09: Add --historical-season Flag

**Source:** User Answer to Q5 (KAI-10 S2) — Option C

Replace the current implicit year-comparison logic (line 116) with an explicit `--historical-season` flag:

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--historical-season` | flag | False | Fetch a past season — overrides current_week to 18 (all weeks) |

**Behavior:**
```python
# BEFORE (implicit, depended on NFL_SEASON from config)
if args.season and args.season < NFL_SEASON:
    current_week = 18
    logger.info(f"Historical season {season}: setting current_week to 18")

# AFTER (explicit flag)
if args.historical_season:
    current_week = 18
    logger.info(f"Historical season mode: fetching all 18 weeks for {args.season}")
```

**Precedence:** `--historical-season` overrides `--current-week` (if both provided, historical wins: current_week=18).

**Usage example:**
```bash
python run_game_data_fetcher.py --season 2024 --historical-season
```

---

### REQ-10: Add --request-timeout CLI Arg

**Source:** User Answer to Q1 (KAI-10 S2) — Option C

Add `--request-timeout` to `run_game_data_fetcher.py`:

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--request-timeout` | int | 30 | HTTP request timeout in seconds (ESPN and Open-Meteo APIs) |

Pass to `fetch_game_data()` (KAI-10 REQ-09 already added this parameter to the signature):
```python
result_path = fetch_game_data(
    output_path=output_path,
    season=args.season,
    current_week=current_week,
    weeks=weeks,
    request_timeout=args.request_timeout  # NEW
)
```

**Note:** `--rate-limit-delay` is NOT added (rate_limit_delay is unused in game_data_fetcher.py — Q1 Option C decision from KAI-10 S2).

---

### REQ-11: Create Test File

**Source:** KAI-11 addition (KAI-10 F03 spec did not include test file)

Create `tests/root_scripts/test_run_game_data_fetcher.py` with class `TestRunGameDataFetcher`.

**Pattern reference:** `TestRunPlayerFetcher` in `tests/root_scripts/test_root_scripts.py` lines 95-113.

**Required tests:**

| Test | What it Verifies |
|------|-----------------|
| `test_has_parse_args` | `parse_args` function exists at module level and is callable |
| `test_parse_args_defaults` | `parse_args([])` produces: season=2025, current_week=17, log_level='INFO', e2e_test=False, request_timeout=30, historical_season=False |
| `test_no_subprocess` | `run_game_data_fetcher` does not import `subprocess` |

**Implementation note:** `parse_args(argv=None)` is defined as a module-level function (REQ-01
derived requirement) — this is what makes these tests possible without mocking.

---

## Files to Modify/Create

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_game_data_fetcher.py` | Refactor (add 4 args, remove os.chdir + config imports, fix defaults, wire log-level, E2E mode, extract parse_args) | Medium |
| `tests/root_scripts/test_run_game_data_fetcher.py` | Create (new test class with 3 tests) | Low |

**Total: 1 file modified + 1 file created**

**Explicitly OUT of scope:**
- `player-data-fetcher/game_data_fetcher.py` — already modified by KAI-10 F01
- `player-data-fetcher/config.py` — not modified (runner just stops importing from it)
- `tests/root_scripts/test_root_scripts.py` — not modified (new file created separately)

---

## Acceptance Criteria

*Finalized — Gate 3 approved 2026-02-19*

- [ ] `python run_game_data_fetcher.py --help` displays all 8 arguments with correct defaults
- [ ] `python run_game_data_fetcher.py --e2e-test` exits 0 in ≤180s; writes to `/tmp/game_data_e2e_test.csv`; `data/game_data.csv` NOT modified
- [ ] `python run_game_data_fetcher.py --e2e-test --log-level DEBUG` exits 0 with DEBUG-level log lines visible
- [ ] `python run_game_data_fetcher.py` (no args) behavior identical to pre-refactor (season=2025, week=17, output=data/game_data.csv, log_level=INFO)
- [ ] `python run_game_data_fetcher.py --season 2024 --historical-season` sets current_week to 18 (visible in log)
- [ ] `grep "from config import" run_game_data_fetcher.py` returns empty
- [ ] `grep "os.chdir" run_game_data_fetcher.py` returns empty
- [ ] `pytest tests/root_scripts/test_run_game_data_fetcher.py -v` shows 3 tests passed
- [ ] `pytest tests/ -v` reports 100% passed, 0 failed (all existing tests plus new tests)
