## Feature Spec: schedule_fetcher_cli

**Status:** APPROVED (Gate 3 — 2026-02-18)
**Last Updated:** 2026-02-18

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Add CLI args to `run_schedule_fetcher.py` + E2E mode. References Feature 01 spec for design patterns.

**Key scope items:**
- Add argparse to `run_schedule_fetcher.py`: --season, --output-path, plus universal args
- Add universal args: --e2e-test, --log-level (NO separate --debug flag — see design correction below)
- Remove `NFL_SEASON=2025` hardcoded directly in runner (replace with argparse default)
- No config.py to strip (schedule-data-fetcher/ has only ScheduleFetcher.py — no config.py)
- Implement --e2e-test mode completing in ≤180 seconds

**Design correction (HANDOFF_PACKAGE.md update 2026-02-18):**
There is NO separate `--debug` flag in this epic. Universal args are `--e2e-test` and `--log-level` only.
For verbose debugging, developers use `--e2e-test --log-level DEBUG`. Feature 01 spec is the authoritative reference.

**Key finding from S2.P1.I1 research:**
- Runner already uses DIRECT import (NOT subprocess) — no subprocess migration needed
- ScheduleFetcher has zero config imports — simpler than Feature 01

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern; argparse defaults are single source of truth
- **Key Constraints:** No config.py to strip; NFL_SEASON is directly in runner; runner is already direct-import
- **Dependencies:** None (Wave 2 — uses Feature 01 spec as design reference)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

### Relevant S2.P1.I2 Decisions

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| `--data-folder` vs `--output-path`? | Option A: `--output-path` only, `--data-folder` dropped | Single output path arg; no directory/filename split |

---

## Requirements

### REQ-01: CLI Arguments — run_schedule_fetcher.py

**Source:** Epic Request (notes file — "schedule_fetcher ~5 args" section) + S2 research (runner source verified)

Add the following CLI arguments to `run_schedule_fetcher.py` via argparse:

**Universal arguments (all 7 scripts):**
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--e2e-test` | flag | False | E2E test mode: fetches 1 week only, completes in ≤180 seconds |
| `--log-level` | str | 'INFO' | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

**Script-specific arguments:**
| Argument | Type | Default | Source Replaced |
|----------|------|---------|-----------------|
| `--season` | int | 2025 | `NFL_SEASON = 2025` (module-level constant at line 31) |
| `--output-path` | str | `'data/season_schedule.csv'` | Hardcoded `output_path` at line 56 in runner (relative to project root / CWD) |

**Backward-compatible arguments (preserved):**
| Argument | Type | Default | Note |
|----------|------|---------|------|
| `--enable-log-file` | flag | False | Pre-existing arg — preserved as-is |

**RESOLVED Q1:** `--output-path` only. `--data-folder` dropped (redundant for this script's single-file output).
**RESOLVED Q1:** `--output-path` only. `--data-folder` dropped.
**RESOLVED Q2:** `--output-format` dropped. CSV-only output.
**RESOLVED Q3:** `--request-timeout` not exposed — internal constant (30.0s).
**RESOLVED Q4:** `--rate-limit-delay` not exposed — internal constant (0.2s).

**Final total: 5 CLI arguments** (2 script-specific + 2 universal + 1 preserved)

---

### REQ-02: Remove NFL_SEASON Module-Level Constant

**Source:** Epic Request ("Zero CLI constants" principle) + S2 research (line 31 verified)

Remove `NFL_SEASON = 2025` from module level of `run_schedule_fetcher.py` (currently line 31).
Replace all references to `NFL_SEASON` with the argparse `--season` value.

**Currently references at:**
- Line 61: `logger.info(f"Fetching NFL season schedule for {NFL_SEASON}...")`
- Line 64: `schedule = await fetcher.fetch_full_schedule(NFL_SEASON)`
- Line 74: `logger.info(f"  Weeks: {len(schedule)}, Season: {NFL_SEASON}")`

All three replaced with `args.season`.

---

### REQ-03: Architecture — Settings flow in runner

**Source:** Epic Request ("constructor parameter pattern") + Feature 01 design precedent

**Note:** Unlike Feature 01, `run_schedule_fetcher.py` IS the main entry point (no separate module like `player_data_fetcher_main.py`). There is no runner→module settings handoff. The runner passes values directly to ScheduleFetcher and fetch_full_schedule. No `@dataclass Settings` or `create_settings_dict()` needed.

**Pattern for this feature:**
```python
# run_schedule_fetcher.py
args = parser.parse_args()

# Setup logger with CLI-controlled level
logger = setup_logger(
    name="schedule_fetcher",
    level=args.log_level,
    log_to_file=args.enable_log_file,
    ...
)

# Derive output path from CLI
output_path = Path(args.output_path)

# Create fetcher (output_path is the only constructor param)
fetcher = ScheduleFetcher(output_path)

# Determine week limit (1 week in e2e mode, 18 normally)
max_weeks = 1 if args.e2e_test else 18

# Pass season and week limit from CLI
schedule = await fetcher.fetch_full_schedule(args.season, max_weeks=max_weeks)
```

**Note:** `request_timeout` (30.0s) and `rate_limit_delay` (0.2s) remain as internal constants in ScheduleFetcher — not passed from runner.

---

### REQ-04: E2E Test Mode (--e2e-test)

**Source:** Epic Request (Section 3: E2E Test Modes) + notes file ("Fetchers: Limited data scope (1 week)")

When `--e2e-test` flag is set:
- Limit fetch to 1 week only (week 1, not weeks 1-18)
- Script must complete in ≤180 seconds
- Exit code 0 on success
- No errors in output

**Also serves as debug mode** (per design correction): developers use `--e2e-test --log-level DEBUG` when they want a fast, verbose debugging run.

**Implementation requires:** Adding `max_weeks: int = 18` parameter to `ScheduleFetcher.fetch_full_schedule()`. Runner passes `max_weeks=1` when `--e2e-test` is set.

---

### REQ-05: --log-level behavior

**Source:** Epic Request (universal argument spec)

- `--log-level` accepts: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Default: INFO
- Passed as `level=` parameter to `setup_logger()` (replaces hardcoded `level="INFO"` at line 49)
- No override precedence rule needed (no --debug flag)

---

### REQ-06: Backward Compatibility

**Source:** Derived requirement (zero regression from EPIC_TICKET)

- Running `python run_schedule_fetcher.py` (no args) must behave identically to current behavior
- Running `python run_schedule_fetcher.py --enable-log-file` must preserve existing behavior
- All 2,744+ existing unit tests must pass

---

### REQ-07: Update test_run_schedule_fetcher.py — Argparse tests

**Source:** S2 research (test_run_schedule_fetcher.py constructs identical argparse parsers)

`tests/root_scripts/test_run_schedule_fetcher.py` contains `TestCLIFlagParsing` class that constructs an "identical parser" to run_schedule_fetcher.py with only `--enable-log-file`. Existing tests test `--enable-log-file` specifically — adding new args to the real parser doesn't break these tests (argparse allows additional args). New tests should cover new args.

**Likely outcome:** Existing 15 tests continue to pass (no deletions needed). Add new tests for `--season`, `--output-path`, `--e2e-test`, `--log-level`.

---

## Open Scope Questions

All checklist questions resolved. No open scope questions remain.

**Decisions made (see `checklist.md`):**
1. **`--data-folder`:** Dropped — `--output-path` only (Q1 → A)
2. **`--output-format`:** Dropped — CSV only, no JSON (Q2 → A)
3. **`--request-timeout`:** Internal constant, not exposed (Q3 → A)
4. **`--rate-limit-delay`:** Internal constant, not exposed (Q4 → A)
5. **`--debug`:** No such flag in this epic (design correction)

---

## Files to Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_schedule_fetcher.py` | Add argparse, remove NFL_SEASON constant, wire --log-level and --e2e-test | Low |
| `schedule-data-fetcher/ScheduleFetcher.py` | Add `max_weeks` param to `fetch_full_schedule()` for E2E limiting | Low |
| `tests/root_scripts/test_run_schedule_fetcher.py` | Add new tests for new CLI args (existing tests preserved) | Low |

**Total: 3 files to modify** (all checklist questions resolved — scope is final)

---

## Acceptance Criteria

*(Draft — to be finalized after checklist resolution)*

- [ ] `python run_schedule_fetcher.py --help` displays --season, --output-path, --e2e-test, --log-level, --enable-log-file
- [ ] `python run_schedule_fetcher.py --season 2024` uses season 2024 (not hardcoded 2025)
- [ ] `python run_schedule_fetcher.py --output-path /tmp/test_schedule.csv` writes to specified path
- [ ] `python run_schedule_fetcher.py --e2e-test` fetches 1 week only, completes in ≤180 seconds with exit code 0
- [ ] `python run_schedule_fetcher.py --log-level WARNING` uses WARNING level logging
- [ ] `python run_schedule_fetcher.py --e2e-test --log-level DEBUG` produces DEBUG-level output for a 1-week fetch
- [ ] `python run_schedule_fetcher.py` (no args) behavior identical to current
- [ ] `python run_schedule_fetcher.py --enable-log-file` preserves existing behavior
- [ ] `grep "NFL_SEASON" run_schedule_fetcher.py` returns empty (constant removed)
- [ ] `pytest tests/` reports all 2,744+ passed, 0 failed
