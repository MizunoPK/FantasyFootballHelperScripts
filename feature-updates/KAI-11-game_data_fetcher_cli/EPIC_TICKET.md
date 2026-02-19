## Epic Ticket: game_data_fetcher_cli

**Created:** 2026-02-19
**Status:** DRAFT

---

## Description

This epic refactors `run_game_data_fetcher.py` to bring it in line with the KAI-10 player fetcher
pattern: universal CLI args (`--e2e-test`, `--log-level`), script-specific args
(`--request-timeout`, `--historical-season`), elimination of the `os.chdir()` anti-pattern, and
removal of config imports in favor of argparse defaults. After this epic, the game data fetcher
runner will be fully self-contained via CLI args, support an automated E2E test mode (Week 1 only,
≤180s, writes to /tmp), and have a complete unit test file covering all CLI behavior.

---

## Acceptance Criteria (Epic-Level)

**The epic is successful when ALL of these are true:**

- [ ] `python run_game_data_fetcher.py --help` shows all 8 arguments (4 existing + 4 new)
- [ ] `python run_game_data_fetcher.py --e2e-test` exits 0 in ≤180s, writes to `/tmp/game_data_e2e_test.csv` (not `data/`)
- [ ] `python run_game_data_fetcher.py --e2e-test --log-level DEBUG` exits 0 with DEBUG output visible
- [ ] `python run_game_data_fetcher.py` (no args) behavior identical to current (season=2025, week=17, output=data/game_data.csv, level=INFO)
- [ ] `python run_game_data_fetcher.py --season 2024 --historical-season` sets current_week to 18
- [ ] `grep "from config import" run_game_data_fetcher.py` returns empty
- [ ] `grep "os.chdir" run_game_data_fetcher.py` returns empty
- [ ] `pytest tests/` reports 100% passed, 0 failed

---

## Success Indicators

- CLI args: All 8 args present in `--help` output
- E2E mode: Completes in ≤180s writing only to `/tmp/` (never `data/`)
- Clean runner: Zero config imports, zero os.chdir calls
- Backward compat: No-args behavior unchanged
- Tests: 100% pass rate maintained; new test file covers all 4 new args

---

## Failure Patterns (How We'd Know Epic Failed)

❌ `--e2e-test` writes to `data/game_data.csv` instead of `/tmp/` (contaminating production data)
❌ `run_game_data_fetcher.py` (no args) fails or behaves differently than before the refactor
❌ `from config import` still present in runner after refactor
❌ `os.chdir` still present in runner after refactor
❌ Any existing unit tests broken by the changes

---

## Scope Boundaries

✅ **In Scope:**
- `run_game_data_fetcher.py` — add 4 args, remove anti-patterns, fix defaults, wire log-level, implement E2E mode
- `tests/root_scripts/test_run_game_data_fetcher.py` — new test file covering all CLI args

❌ **Out of Scope:**
- `player-data-fetcher/game_data_fetcher.py` — already refactored by KAI-10
- `--rate-limit-delay` arg — unused in module code
- `--debug` flag — not in this epic; use `--e2e-test --log-level DEBUG`
- Documentation (README.md, ARCHITECTURE.md) — handled in S7.P3
- Integration test framework — separate successor epic

---

## User Validation

**User comments:** —
**User approval:** YES
**Approved by:** User
**Approved date:** 2026-02-19
