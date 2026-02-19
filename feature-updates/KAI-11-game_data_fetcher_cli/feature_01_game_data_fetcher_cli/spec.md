## Feature Spec: game_data_fetcher_cli

**Status:** IN PROGRESS — S2 pending
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

### Relevant Discovery Decisions

- **Solution Approach:** KAI-10 player fetcher pattern — argparse + sys.path only; no config
- **Key Constraints:** Preserve backward compatibility; all existing tests must pass
- **Dependencies:** KAI-10 F01 already modified `game_data_fetcher.py` (REQ-09) — runner must pass `request_timeout` to `fetch_game_data()`

### Relevant User Answers (from Discovery — resolved in KAI-10 S2)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| `--request-timeout` / `--rate-limit-delay` as CLI args? | `--request-timeout` only (rate-limit-delay unused in code) | REQ-10 adds only `--request-timeout` |
| `--data-folder`, `--validate`, `--clean` in scope? | No — follow DISCOVERY scope strictly | Not in spec |
| E2E test week? | Week 1 — deterministic, reliable historical data | E2E mode uses `weeks=[1]` |
| `--debug` flag? | No — use `--e2e-test --log-level DEBUG` | No `--debug` arg |
| Historical season detection after config removal? | Add `--historical-season` flag explicitly | REQ-09 adds `--historical-season` flag |

---

## Feature Requirements

**Note:** Requirements ported from KAI-10 Feature 03 approved spec (Gate 3, 2026-02-18).
S2 will verify these against current code state and finalize.

{To be completed in S2 — reference:
feature-updates/done/KAI-10-architectural_refactoring_configuration_management/feature_03_game_data_fetcher_cli/spec.md}

---

## Files to Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_game_data_fetcher.py` | Refactor (add 4 args, remove os.chdir, fix defaults, remove config import) | Medium |
| `tests/root_scripts/test_run_game_data_fetcher.py` | Create (new file) | Medium |

**Total: 2 files**

---

## Acceptance Criteria

{To be finalized in S2}

- [ ] `python run_game_data_fetcher.py --help` displays all 8 arguments
- [ ] `python run_game_data_fetcher.py --e2e-test` exits 0 in ≤180s, writes to `/tmp/game_data_e2e_test.csv`
- [ ] `python run_game_data_fetcher.py --e2e-test --log-level DEBUG` exits 0 with DEBUG output
- [ ] `python run_game_data_fetcher.py` (no args) behavior identical to current
- [ ] `python run_game_data_fetcher.py --season 2024 --historical-season` sets current_week to 18
- [ ] `grep "from config import" run_game_data_fetcher.py` returns empty
- [ ] `grep "os.chdir" run_game_data_fetcher.py` returns empty
- [ ] `pytest tests/` reports 100% passed, 0 failed
