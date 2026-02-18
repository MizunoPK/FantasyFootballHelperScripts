## Feature Spec: historical_compiler_cli

**Status:** APPROVED — Gate 3 passed 2026-02-18
**Last Updated:** 2026-02-18

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Enhance existing argparse with 5 new args + debug/E2E modes. References Feature 01 spec for design patterns.

**Key scope items (DISCOVERY.md — Finding 7, Feature Breakdown row 04 + Design Correction 2026-02-18):**
- Enhance `compile_historical_data.py`: add --e2e-test, --log-level, --timeout, --rate-limit-delay
- **NO separate `--debug` flag** — `--e2e-test` serves both E2E testing and debugging purposes
- Existing args: --year, --verbose, --enable-log-file, --output-dir
- Move REQUEST_TIMEOUT=30.0 and RATE_LIMIT_DELAY=0.3 from `historical_data_compiler/constants.py` to argparse defaults
- Refactor `BaseHTTPClient` construction to accept timeout/rate_limit_delay via constructor params (already supported — needs wiring)
- Implement --e2e-test mode completing in ≤180 seconds (used for both E2E testing and debugging)
- Backward compatibility: --verbose flag preserved (maps to --log-level DEBUG behavior)

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern; argparse defaults are single source of truth
- **Key Constraints:** REQUEST_TIMEOUT and RATE_LIMIT_DELAY are in `historical_data_compiler/constants.py`; backward compatibility for --verbose; all 2,744+ existing tests must pass
- **Dependencies:** Feature 01 spec provides design pattern precedents (Settings class, universal arg conventions)
- **Verification:** `historical_data_compiler/http_client.py` `BaseHTTPClient.__init__` already accepts `timeout` and `rate_limit_delay` constructor params (lines 62-82) — no refactor needed on http_client.py itself

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

### Design Pattern Precedents from Feature 01

| Decision | Feature 01 Pattern | Applied to Feature 04 |
|----------|-------------------|----------------------|
| Universal args | --e2e-test, --log-level ONLY (no --debug) | Same — 2 universal args only |
| --e2e-test behavior | Reduce data scope + ≤180s; also used for debugging | 1 season + player_limit=100, ≤180s (Q5 — see checklist) |
| --log-level | choices: DEBUG/INFO/WARNING/ERROR/CRITICAL, default INFO | Identical |
| Debugging workflow | `--e2e-test --log-level DEBUG` | Same pattern |

---

## Requirements

### REQ-01: CLI Arguments — compile_historical_data.py

**Source:** Epic Request (universal args + script-specific), DISCOVERY.md Finding 7, Feature 01 spec pattern

Add the following CLI arguments to `compile_historical_data.py` via argparse:

**Universal arguments (all 7 scripts — consistent with Feature 01):**
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--e2e-test` | flag | False | E2E test mode: reduces data scope, completes in ≤180 seconds; also used for debugging |
| `--log-level` | str | 'INFO' | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

**NOTE: NO `--debug` flag** — per user decision (2026-02-18). `--e2e-test` serves both E2E testing and debugging purposes. For verbose debug output, use `--e2e-test --log-level DEBUG`.

**Script-specific new arguments (replacing constants.py values):**
| Argument | Type | Default | Source Constant Removed |
|----------|------|---------|------------------------|
| `--timeout` | float | 30.0 | `REQUEST_TIMEOUT` in `historical_data_compiler/constants.py` |
| `--rate-limit-delay` | float | 0.3 | `RATE_LIMIT_DELAY` in `historical_data_compiler/constants.py` |

**Existing arguments (preserved as-is — backward compatibility):**
| Argument | Type | Default | Note |
|----------|------|---------|------|
| `--year` | int | None | Pre-existing — preserved |
| `--verbose` / `-v` | flag | False | Pre-existing — preserved, maps to DEBUG logging (see REQ-07) |
| `--enable-log-file` | flag | False | Pre-existing — preserved |
| `--output-dir` | Path | None | Pre-existing — preserved |

**Total: 8 CLI arguments** (4 new + 4 preserved)

**NOTE:** Additional script-specific args (--weeks, --validate, --clean, --skip-backups) were considered but are OUT OF SCOPE (RESOLVED Q3 — Option A). Only DISCOVERY-confirmed args are included.

---

### REQ-02: Wire timeout/rate_limit_delay to BaseHTTPClient

**Source:** Epic Request (constructor parameter pattern) + S2 research (BaseHTTPClient already accepts params)

**Current (compile_historical_data.py line 188):**
```python
http_client = BaseHTTPClient()  # Uses REQUEST_TIMEOUT, RATE_LIMIT_DELAY from constants
```

**After (inside compile_season_data — using function params, not args.*):**
```python
http_client = BaseHTTPClient(
    timeout=timeout,
    rate_limit_delay=rate_limit_delay
)
```

**Sub-requirements (RESOLVED Q4 — Option A: direct params):**
- REQ-02a: `compile_season_data()` signature updated to accept `timeout`, `rate_limit_delay`, and `e2e_test` as explicit parameters:
  ```python
  async def compile_season_data(year: int, output_dir: Path, timeout: float, rate_limit_delay: float, e2e_test: bool) -> None:
  ```
- REQ-02b: `BaseHTTPClient` already supports these constructor params (lines 62-82 in http_client.py) — no changes needed to http_client.py
- REQ-02c: Values flow from CLI args through `main()` → `compile_season_data()` → `BaseHTTPClient()`
- REQ-02d: Call site in `main()`:
  ```python
  asyncio.run(compile_season_data(current_year, output_dir, args.timeout, args.rate_limit_delay, args.e2e_test))
  ```

---

### REQ-03: Remove REQUEST_TIMEOUT and RATE_LIMIT_DELAY from constants.py

**Source:** Epic Request ("Zero CLI constants in config files") + S2 research (constants.py verified)

**Remove from `historical_data_compiler/constants.py`:**
1. `REQUEST_TIMEOUT = 30.0` (line 98) — moves to argparse default for `--timeout`
2. `RATE_LIMIT_DELAY = 0.3` (line 101) — moves to argparse default for `--rate-limit-delay`

**Keep in `historical_data_compiler/constants.py`:**
- `MAX_RETRY_ATTEMPTS = 3` (non-CLI constant — keeps in constants.py)
- `ESPN_USER_AGENT` (non-CLI constant — keeps)
- All other constants (ESPN mappings, season config, file names, etc.)

**Impact on http_client.py:**
- Remove `REQUEST_TIMEOUT` and `RATE_LIMIT_DELAY` from the import on line 18-23
- Replace constants-based defaults with inline defaults in `BaseHTTPClient.__init__`:
  ```python
  # BEFORE:
  def __init__(self, timeout: float = REQUEST_TIMEOUT, rate_limit_delay: float = RATE_LIMIT_DELAY, ...):
  # AFTER:
  def __init__(self, timeout: float = 30.0, rate_limit_delay: float = 0.3, ...):
  ```
- Inline defaults preserve backward compatibility for any code calling `BaseHTTPClient()` without params

**Impact on tests:**
- `tests/historical_data_compiler/test_constants.py` does NOT test REQUEST_TIMEOUT or RATE_LIMIT_DELAY — **no test deletion required**
- All other constants tests remain valid

---

### REQ-04: E2E Test Mode (--e2e-test)

**Source:** Epic Request (Section 3: E2E Test Modes) + DISCOVERY.md (Feature 04 row: "E2E mode")

When `--e2e-test` flag is set:
- Compile exactly 1 NFL season (use `--year` if provided; otherwise use `max(YEARS)` — currently 2025)
- Set player limit to 100 (reduces ESPN Fantasy API calls — consistent with Feature 01 pattern)
- Write output to a system temp directory — real `simulation/sim_data/` is never touched
- Auto-cleanup temp directory after compilation completes (success or failure)
- Script must complete in ≤180 seconds
- Exit code 0 on success
- No errors in output

**Data limiting strategy (RESOLVED Q1 — Option A):**
- `ESPN_PLAYER_LIMIT` in `historical_data_compiler/player_data_fetcher.py` is currently a module-level constant (1500)
- In E2E mode, override this to 100 — pass `player_limit` as a parameter to `fetch_player_data()`
- Consistent with Feature 01's `espn_player_limit = 100` pattern

**Output directory behavior (RESOLVED Q5 — Option A):**
- Use `tempfile.mkdtemp()` to create a temp output directory
- Pass temp dir as `output_dir` to `compile_season_data()` instead of `simulation/sim_data/{year}/`
- Skip the `shutil.rmtree()` cleanup check (temp dir is always empty/new)
- Use `try/finally` to ensure temp dir is removed after E2E run:
  ```python
  import tempfile
  with tempfile.TemporaryDirectory() as tmp_dir:
      output_dir = Path(tmp_dir) / str(current_year)
      asyncio.run(compile_season_data(current_year, output_dir, args.timeout, args.rate_limit_delay, args.e2e_test))
  ```

---

### REQ-05: No Separate Debug Flag — --e2e-test Serves Both Purposes

**Source:** User decision (2026-02-18) — same as Feature 01 REQ-12

There is **no separate `--debug` flag** in this epic. The `--e2e-test` flag is used for both E2E testing and debugging. When a developer wants to debug the script with a fast, data-limited run, they use `--e2e-test`. For verbose log output, they combine: `--e2e-test --log-level DEBUG`.

---

### REQ-06: --log-level behavior

**Source:** Epic Request (universal argument spec) + Feature 01 spec pattern

- `--log-level` accepts: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Default: INFO
- `--verbose` maps to DEBUG logging (backward compat — same effect as `--log-level DEBUG`)

**Precedence order (highest first):**
1. `--verbose` flag → DEBUG (backward compat only — pre-existing arg; equivalent to `--log-level DEBUG`)
2. `--log-level` value → user-specified level
3. Default → INFO

**Note:** `--e2e-test` does NOT change the log level. Use `--e2e-test --log-level DEBUG` for verbose debug output.

**Alignment note (vs Feature 01 REQ-13):** Feature 01 establishes "no flag overrides log level" as the universal pattern. The `--verbose` override in Feature 04 is a **pre-existing backward compat exception** specific to this script — not a new design decision and not a pattern for other scripts. All other Wave 2 features without `--verbose` follow the F01 pattern exactly.

---

### REQ-07: Backward Compatibility — --verbose flag

**Source:** S2 research + spec.md seed + existing tests

- `--verbose` / `-v` flag preserved as-is in argparse
- Behavior: maps to DEBUG logging (current behavior: `log_level = "DEBUG" if args.verbose else "INFO"` at line 264)
- After refactor: `--verbose` is equivalent to `--log-level DEBUG`
- Existing tests for `--verbose` behavior must continue to pass:
  - `test_compile_historical_data_logger.py` T2.1: `log_level == "DEBUG"` when verbose=True
  - `test_compile_historical_data_logger.py` T2.2: `log_level == "INFO"` when verbose=False

---

### REQ-08: Backward Compatibility — no-args behavior

**Source:** Derived requirement (zero regression requirement)

- Running `python compile_historical_data.py` (no args) must behave identically to current behavior:
  - No `--year` → falls back to compiling all years in YEARS array
  - No `--verbose` → INFO logging
  - No `--enable-log-file` → console-only logging
  - No `--output-dir` → default `simulation/sim_data/{year}` path
- All 2,744+ existing unit tests must pass after refactoring

---

## Acceptance Criteria

- [ ] `python compile_historical_data.py --help` displays all 8 arguments (4 existing + 4 new)
- [ ] `python compile_historical_data.py --year 2024 --e2e-test` exits 0 in ≤180s
- [ ] `python compile_historical_data.py --e2e-test --log-level DEBUG` enables DEBUG logging with reduced scope
- [ ] `python compile_historical_data.py` (no args) behavior identical to current
- [ ] `python compile_historical_data.py --verbose` behavior identical to current (DEBUG logging)
- [ ] `python compile_historical_data.py --year 2024 --timeout 60.0 --rate-limit-delay 0.5` uses those values for BaseHTTPClient
- [ ] `grep "REQUEST_TIMEOUT\|RATE_LIMIT_DELAY" historical_data_compiler/constants.py` returns empty
- [ ] `pytest tests/` reports all 2,744+ passed, 0 failed
- [ ] (Pending Q1/Q5) E2E mode-specific acceptance criteria to be added after Q1/Q5 resolved

---

## Resolved Questions

All checklist questions resolved. See `checklist.md` for full details.

| Q# | Topic | Resolution |
|----|-------|-----------|
| Q1 | E2E mode data limiting | Option A — player_limit=100 |
| Q2 | --debug reduced scope | N/A — no --debug flag in this epic |
| Q3 | Additional script-specific args | Option A — none (DISCOVERY scope only) |
| Q4 | Settings dataclass vs direct params | Option A — direct params |
| Q5 | E2E output directory | Option A — temp directory |

---

## Files to Modify

| File | Change Type | Complexity | Notes |
|------|-------------|------------|-------|
| `compile_historical_data.py` | Add CLI args, wire to BaseHTTPClient, E2E temp dir | Medium | parse_args() + main() + compile_season_data() signature |
| `historical_data_compiler/constants.py` | Remove 2 constants | Low | Lines 98-101 |
| `historical_data_compiler/http_client.py` | Remove constants import, use inline defaults | Low | Line 18-23 only |
| `historical_data_compiler/player_data_fetcher.py` | Add player_limit param to fetch_player_data() | Low | Line 38 module constant + function signature |

**Total: 4 files to modify**
