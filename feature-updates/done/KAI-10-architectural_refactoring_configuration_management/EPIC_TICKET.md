## Epic Ticket: Architectural Refactoring — Configuration Management (KAI-10)

## Description

Refactor all 7 runner scripts from scattered, hardcoded configuration to a consistent CLI-based architecture using dependency injection. After this epic, every configurable constant across all scripts is exposed as a CLI argument (single source of truth in argparse defaults), configuration flows explicitly from runner → main → internal modules via constructor parameters, and each script supports fast E2E test modes (≤3 minutes) and consistent debug behavior. An integration test framework validates all argument combinations automatically.

## Acceptance Criteria (Epic-level)

- [ ] All 7 runner scripts expose their configurable constants exclusively as CLI arguments — zero CLI-configurable constants remain in config/constants files
- [ ] All 7 runner scripts use the constructor parameter pattern — no config module imports for CLI-configurable values in internal modules
- [ ] All 7 runner scripts support `--e2e-test` mode completing successfully in ≤180 seconds
- [ ] All 7 runner scripts support `--debug` and `--log-level` with consistent behavior (DEBUG logging + reduced data scope)
- [ ] 7 CLI integration test runners exist (5 new + 2 enhanced) and all pass via master runner
- [ ] All 2,744+ existing unit tests continue to pass (100% pass rate — zero regressions)
- [ ] INTEGRATION_TESTING_GUIDE.md created covering all 7 scripts and usage patterns

## Success Indicators

- `python run_player_fetcher.py --week 1 --espn-player-limit 100 --e2e-test` exits 0 in <180s
- `python run_league_helper.py --mode draft --e2e-test` exits 0 in <180s (all 5 modes via automation)
- `grep -r "CURRENT_NFL_WEEK\|NFL_SEASON\|ESPN_PLAYER_LIMIT" player-data-fetcher/config.py` returns empty
- `python run_all_integration_tests.py` reports 7/7 passed, exit code 0
- `pytest tests/` reports 2,744+ passed, 0 failed

## Failure Patterns (How we'd know epic failed)

❌ Config constants still exist in config.py/constants.py alongside argparse defaults (duplication, not single source of truth)
❌ Internal modules still import from config at module level (e.g., `from config import CURRENT_NFL_WEEK`)
❌ `--e2e-test` mode hangs >3 minutes or raises an exception
❌ Any of the 2,744 existing unit tests fail after refactoring (behavioral regression)
❌ `--debug` on one script causes DEBUG logging while another script ignores it (inconsistent behavior)
❌ `run_all_integration_tests.py` exits non-zero or any individual test runner fails
