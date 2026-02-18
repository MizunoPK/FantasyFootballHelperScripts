## Feature Spec: game_data_fetcher_cli

**Status:** APPROVED (Gate 3 — 2026-02-18)
**Last Updated:** 2026-02-18

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 2 — Enhance existing argparse with universal args + debug/E2E modes. References Feature 01 spec for design patterns.

**Key scope items:**
- Add universal args to `run_game_data_fetcher.py`: `--e2e-test`, `--log-level` (NO `--debug` flag — see design note)
- Add script-specific args: `--request-timeout`, `--historical-season`
- Existing args preserved: `--season`, `--output`, `--weeks`, `--current-week`
- Remove `from config import NFL_SEASON, CURRENT_NFL_WEEK` from runner — replace with argparse defaults
- Remove `os.chdir()` from runner — use sys.path manipulation only (Feature 01 pattern)
- Wire `--log-level` to `setup_logger()` call (currently hardcoded `"INFO"`)
- Implement `--e2e-test` mode completing in ≤180 seconds (Week 1 data only)

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern; argparse defaults are single source of truth
- **Key Constraints:** Preserve backward compatibility of existing 4 args (no regressions); all 2,744+ unit tests must pass
- **Dependencies:** Feature 01 refactors `player-data-fetcher/game_data_fetcher.py` (REQ-09) — Feature 03 runner must align with post-Feature-01 `fetch_game_data()` signature
- **Universal args established by Feature 01:** `--e2e-test` (flag), `--log-level` (str, choices: DEBUG/INFO/WARNING/ERROR/CRITICAL) — NO `--debug` flag per design correction 2026-02-18

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 |

### Relevant S2.P1.I2 Decisions

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| `--request-timeout` / `--rate-limit-delay` as CLI args? | Option C — `--request-timeout` only; rate-limit-delay unused in code | REQ-10 added |
| `--data-folder`, `--validate`, `--clean` in scope? | Option B — skip all 3; follow DISCOVERY scope | Not in spec |
| E2E test week? | Option A — Week 1 (deterministic, reliable) | REQ-06 uses `weeks=[1]` |
| Historical season detection after config removal? | Option C — add `--historical-season` flag | REQ-09 added |

---

## Requirements

### REQ-01: Add Universal CLI Args — run_game_data_fetcher.py

**Source:** Epic Request (universal args for all 7 scripts) + Feature 01 precedent

Add the following universal CLI arguments to `run_game_data_fetcher.py` via argparse:

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--e2e-test` | flag | False | E2E test mode: reduces data scope to complete in ≤180 seconds; also used for debugging |
| `--log-level` | str | 'INFO' | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

**Total args after:** 8 (4 existing + 2 universal + 2 script-specific: --request-timeout from Q1, --historical-season from Q5)

**Design note (from handoff correction 2026-02-18):** There is NO `--debug` flag in this epic. `--e2e-test` serves both purposes — E2E testing and development debugging. For verbose debug logging, developers use `--e2e-test --log-level DEBUG`.

---

### REQ-02: Argparse Defaults as Single Source of Truth

**Source:** Epic Request ("argparse defaults = single source of truth") + DISCOVERY.md Architecture

Change existing `--season` and `--current-week` to have hardcoded defaults instead of config fallbacks:

| Argument | Current Default | New Default | Source Removed |
|----------|-----------------|-------------|----------------|
| `--season` | `None` (→ `NFL_SEASON` from config) | `2025` | `config.NFL_SEASON` |
| `--current-week` | `None` (→ `CURRENT_NFL_WEEK` from config) | `17` | `config.CURRENT_NFL_WEEK` |

**Behavior change:** Currently, omitting `--season` causes the runner to fall back to `NFL_SEASON=2025` from config. After refactor, omitting `--season` uses the argparse default of `2025` directly. Behavior is identical from the user's perspective.

Remove the fallback pattern:
```python
# BEFORE
season = args.season if args.season else NFL_SEASON
current_week = args.current_week if args.current_week else CURRENT_NFL_WEEK

# AFTER
season = args.season   # already 2025 if not provided
current_week = args.current_week  # already 17 if not provided
```

---

### REQ-03: Remove Config Imports from Runner

**Source:** Epic Request ("Zero CLI constants in config files")

Remove from `run_game_data_fetcher.py`:
```python
# REMOVE (currently line 105 inside try/chdir block)
from config import NFL_SEASON, CURRENT_NFL_WEEK
```

After this change, the runner no longer needs the `player-data-fetcher/config.py` module at runtime for config values.

---

### REQ-04: Remove os.chdir() from Runner

**Source:** Feature 01 design pattern (anti-pattern elimination)

The current runner uses `os.chdir(fetcher_dir)` before imports. This has two problems:
1. Mutates global process state (working directory) — side effect risk
2. Creates a dependency on working directory that the internal module doesn't actually need (game_data_fetcher.py uses `Path(__file__).parent` for its own paths)

**After refactor:**
```python
# BEFORE
os.chdir(fetcher_dir)          # BAD: changes working directory
sys.path.insert(0, str(fetcher_dir))

# AFTER
sys.path.insert(0, str(fetcher_dir))   # sys.path only — no chdir
```

Remove: `os.chdir(fetcher_dir)` call
Remove: `original_cwd = os.getcwd()` + `os.chdir(original_cwd)` in finally
Keep: `sys.path.insert()` for import resolution
Import `os` can be removed if no longer used; keep if still needed for anything else.

---

### REQ-05: Wire --log-level to setup_logger

**Source:** Epic Request (universal log-level support)

The current runner hardcodes `"INFO"` in the setup_logger call:
```python
# BEFORE (line 109)
logger = setup_logger("game_data_fetcher", "INFO", False, None, "standard")

# AFTER
logger = setup_logger("game_data_fetcher", args.log_level, False, None, "standard")
```

**Note:** No `--debug` flag exists in this epic. Users who want DEBUG logging pass `--log-level DEBUG` directly.

---

### REQ-06: E2E Test Mode (--e2e-test)

**Source:** Epic Request (Section 3: E2E Test Modes) + handoff correction 2026-02-18

When `--e2e-test` flag is set:
- Limit fetch to **Week 1 only** (reliable past data, always exists — Q3 resolved: Option A)
- Script must complete in ≤180 seconds
- Exit code 0 on success
- **Also serves as debugging mode** — developers use `--e2e-test --log-level DEBUG` for verbose debugging

**Implementation pattern:**
```python
if args.e2e_test:
    weeks = [1]  # Week 1 — deterministic, reliable historical data
    logger.info("E2E test mode: limiting to week 1")
```

**Note:** `--e2e-test` takes precedence over `--weeks` (data limits override explicit week selection)

---

### REQ-07: --log-level Behavior

**Source:** Epic Request (universal argument spec) + Feature 01 precedent

- `--log-level` accepts: DEBUG, INFO, WARNING, ERROR, CRITICAL (case-sensitive per argparse choices)
- Default: INFO
- No `--debug` flag exists — users pass `--log-level DEBUG` explicitly for verbose output
- Consistent with Feature 01 pattern

---

### REQ-08: Backward Compatibility

**Source:** Derived requirement (zero regression requirement)

- `python run_game_data_fetcher.py` (no args) must behave identically to current behavior
  - Same season (2025), same current_week (17), same output path, same log level (INFO)
- `python run_game_data_fetcher.py --season 2024 --output sim_data/game_data.csv` must work identically
- All 2,744+ existing unit tests must pass after changes

---

### REQ-09: Add --historical-season Flag

**Source:** User Answer to Q5 (Option C)

Replace the current implicit year-comparison logic with an explicit `--historical-season` flag:

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--historical-season` | flag | False | Fetch a past season — sets current_week to 18 (all weeks) |

**Behavior:**
```python
# BEFORE (implicit, depended on NFL_SEASON from config)
if args.season and args.season < NFL_SEASON:
    current_week = 18

# AFTER (explicit flag)
if args.historical_season:
    current_week = 18
    logger.info(f"Historical season mode: fetching all 18 weeks for {args.season}")
```

**Usage example:**
```bash
python run_game_data_fetcher.py --season 2024 --historical-season
```

**Note:** `--historical-season` overrides `--current-week`. If both are provided, `--historical-season` wins (sets to 18).

---

### REQ-10: Add --request-timeout CLI Arg

**Source:** User Answer to Q1 (Option C)

Add `--request-timeout` to `run_game_data_fetcher.py`:

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--request-timeout` | int | 30 | HTTP request timeout in seconds (ESPN and Open-Meteo APIs) |

Pass to `fetch_game_data()` after Feature 01 REQ-09 adds it to the signature:
```python
fetch_game_data(
    output_path=output_path,
    season=args.season,
    current_week=current_week,
    weeks=weeks,
    request_timeout=args.request_timeout  # NEW
)
```

**Note:** `--rate-limit-delay` is NOT added (imported but unused in game_data_fetcher.py — Q1 Option C decision).

---

## Open Scope Questions

All checklist questions resolved. No open scope questions remain.

**Decisions made (see `checklist.md`):**
1. **`--request-timeout`:** Exposed as CLI arg; `--rate-limit-delay` skipped (unused in code) — Q1 → Option C
2. **`--data-folder`, `--validate`, `--clean`:** Dropped — follow DISCOVERY scope strictly — Q2 → Option B
3. **E2E test week:** Week 1 always — deterministic, reliable — Q3 → Option A
4. **`--debug` flag:** N/A — no `--debug` flag in this epic (design correction 2026-02-18)
5. **Historical season detection:** Add `--historical-season` flag — Q5 → Option C

---

## Files to Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_game_data_fetcher.py` | Refactor (add 4 args, remove os.chdir, fix defaults, remove config import) | Medium |

**Total: 1 file to modify**

Note: `player-data-fetcher/game_data_fetcher.py` is modified by Feature 01 (REQ-09 in that spec), not Feature 03.

---

## Acceptance Criteria

*(Draft — to be finalized after checklist resolution)*

- [ ] `python run_game_data_fetcher.py --help` displays all 8 arguments (4 existing + 2 universal + 2 script-specific)
- [ ] `python run_game_data_fetcher.py --e2e-test` exits 0 in ≤180s
- [ ] `python run_game_data_fetcher.py --e2e-test --log-level DEBUG` exits 0 with DEBUG output
- [ ] `python run_game_data_fetcher.py` (no args) behavior identical to current (season=2025, week=17, output=data/game_data.csv, level=INFO)
- [ ] `python run_game_data_fetcher.py --season 2024 --historical-season` sets current_week to 18
- [ ] `grep "from config import" run_game_data_fetcher.py` returns empty
- [ ] `grep "os.chdir" run_game_data_fetcher.py` returns empty
- [ ] `pytest tests/` reports all 2,744+ passed, 0 failed
