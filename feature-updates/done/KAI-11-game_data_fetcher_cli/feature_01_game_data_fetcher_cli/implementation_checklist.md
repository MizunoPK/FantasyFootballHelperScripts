## Implementation Checklist: game_data_fetcher_cli

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**Update this file IN REAL-TIME (not batched at end)**

---

## Requirements from spec.md

- [x] **REQ-01:** `parse_args(argv=None)` at module level + `--e2e-test` (flag) + `--log-level` (choices)
  - Task: Task 3 | File: `run_game_data_fetcher.py:parse_args()`
  - Verified: `--help` shows 8 args; `callable(parse_args) is True` ✅ (2026-02-19)

- [x] **REQ-02:** `--season` default None → `2025`; `--current-week` default None → `17`
  - Task: Task 3 | File: `run_game_data_fetcher.py:parse_args()`
  - Verified: `parse_args([]).season == 2025`, `.current_week == 17` ✅ (2026-02-19)

- [x] **REQ-03:** Remove `from config import NFL_SEASON, CURRENT_NFL_WEEK` (line 105)
  - Task: Task 2 | File: `run_game_data_fetcher.py`
  - Verified: `grep "from config import"` returns empty ✅ (2026-02-19)

- [x] **REQ-04:** Remove `os.chdir()` + `import os`; move `sys.path` inserts to module level
  - Task: Task 1 | File: `run_game_data_fetcher.py:module-level`
  - Verified: `grep "os.chdir"` returns empty ✅; import test passes ✅ (2026-02-19)

- [x] **REQ-05:** Wire `args.log_level` → `setup_logger()` (replace hardcoded `"INFO"`)
  - Task: Task 4 | File: `run_game_data_fetcher.py:main()`
  - Verified: `setup_logger("game_data_fetcher", args.log_level, ...)` ✅ (2026-02-19)

- [x] **REQ-06:** E2E mode: `weeks=[1]`, output → `/tmp/game_data_e2e_test.csv`, precedence over `--weeks`
  - Task: Task 4 | File: `run_game_data_fetcher.py:main()`
  - Verified: `if args.e2e_test:` block with if/elif/else ordering ✅ (2026-02-19)

- [x] **REQ-07:** `--log-level` choices `['DEBUG','INFO','WARNING','ERROR','CRITICAL']`, default `'INFO'`
  - Task: Task 3 | File: `run_game_data_fetcher.py:parse_args()`
  - Verified: `--help` shows choices; `parse_args([]).log_level == 'INFO'` ✅ (2026-02-19)

- [x] **REQ-08:** Backward compat: no-args → season=2025, week=17, output=data/game_data.csv, log=INFO
  - Task: Tasks 3+4 | File: `run_game_data_fetcher.py`
  - Verified: argparse defaults + output path logic preserved; 2711 tests pass ✅ (2026-02-19)

- [x] **REQ-09:** `--historical-season` flag → `current_week=18`, log message, overrides `--current-week`
  - Task: Tasks 3+4 | File: `run_game_data_fetcher.py`
  - Verified: historical block added after `current_week = args.current_week` ✅ (2026-02-19)

- [x] **REQ-10:** `--request-timeout` (int, default 30) → pass as `request_timeout=` to `fetch_game_data()`
  - Task: Tasks 3+4 | File: `run_game_data_fetcher.py`
  - Verified: `request_timeout=args.request_timeout` kwarg added to fetch call ✅ (2026-02-19)

- [x] **REQ-11:** Create `tests/root_scripts/test_run_game_data_fetcher.py` with `TestRunGameDataFetcher` (3 tests)
  - Task: Task 5 | File: `tests/root_scripts/test_run_game_data_fetcher.py` (new)
  - Verified: 3/3 tests pass (`test_has_parse_args`, `test_parse_args_defaults`, `test_no_subprocess`) ✅ (2026-02-19)

---

## Edge Cases

- [x] **EDGE-01:** `--log-level` lowercase/invalid → SystemExit 2 (argparse `choices=`) — Task 3 ✅
- [x] **EDGE-02:** `--e2e-test` + `--weeks` → e2e wins: `weeks=[1]` (if/elif ordering) — Task 4 ✅
- [x] **EDGE-03:** `--historical-season` + `--current-week` → historical wins: `current_week=18` — Task 4 ✅
- [x] **EDGE-04:** `--request-timeout` non-int → SystemExit 2 (argparse `type=int`) — Task 3 ✅
- [x] **EDGE-05:** `--season` non-int → SystemExit 2 (argparse `type=int`) — Task 3 ✅
- [x] **EDGE-06:** Import from any CWD (`Path(__file__).parent` absolute, not CWD-relative) — Task 1 ✅
- [x] **EDGE-07:** `--historical-season --e2e-test` combined → `current_week=18` + `weeks=[1]` (non-conflicting) — Task 4 ✅

---

## Task Status

| Task | Description | Phase | Status |
|------|-------------|-------|--------|
| Task 1 | Move sys.path to module level + remove os.chdir | 1 | ✅ |
| Task 2 | Remove config import + fallback patterns | 1 | ✅ |
| Task 3 | Extract parse_args() + 4 new args | 2 | ✅ |
| Task 4 | Wire new args in main() | 3 | ✅ |
| Task 5 | Create test file | 4 | ✅ |

---

## Phase Test Results

| Phase | Tests Run | Passed | Status |
|-------|-----------|--------|--------|
| Phase 1 (Tasks 1+2) | 2711 (full suite) | 2711 | ✅ 100% |
| Phase 2 (Task 3) | --help + parse_args([]) | pass | ✅ 100% |
| Phase 3 (Task 4) | 2711 (full suite) | 2711 | ✅ 100% |
| Phase 4 (Task 5) | 3 new unit tests | 3 | ✅ 100% |
| Final (full suite) | 2714 | 2714 | ✅ 100% |

---

## Summary

**Requirements:** 11 / 11 complete ✅
**Edge Cases:** 7 / 7 complete ✅
**Tasks:** 5 / 5 complete ✅

**Last Updated:** 2026-02-19 (S6 complete — all tasks done, 2714/2714 tests pass)
