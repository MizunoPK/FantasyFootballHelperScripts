## Research Notes: integration_test_framework

**Created:** 2026-02-18
**Phase:** S2.P1.I1 — Feature-Level Discovery

---

## Existing Test Landscape

### tests/integration/ — Direct Python import tests (6 files)

| File | Pattern | Tests |
|------|---------|-------|
| `test_data_fetcher_integration.py` | Direct import (`from player_data_fetcher_main import NFLProjectionsCollector, Settings`) | 289 lines; uses mock/patch for ESPN API |
| `test_schedule_fetcher_integration.py` | **subprocess.run() CLI invocation** | 459 lines; tests --enable-log-file flag, log file creation |
| `test_historical_data_compiler_integration.py` | Mocks sys.argv + `import compile_historical_data` | 117 lines; 3 simple tests for --enable-log-file |
| `test_league_helper_integration.py` | Direct import (`from league_helper.LeagueHelperManager import LeagueHelperManager`) | 750 lines; extensive workflow tests |
| `test_simulation_integration.py` | Direct import (ConfigGenerator, SimulationManager, ParallelLeagueRunner) | 535 lines; most E2E tests skipped |
| `test_accuracy_simulation_integration.py` | Direct import (AccuracyCalculator, AccuracyResultsManager) | 711 lines; tests Python class behavior |

**Key insight:** Most existing tests/integration/ files test PYTHON CLASSES (not CLI invocation). Only `test_schedule_fetcher_integration.py` uses subprocess.run() for CLI tests. F08's new files all use subprocess.run().

### tests/root_scripts/ — CLI-focused tests (4 files)

| File | Pattern | Notes |
|------|---------|-------|
| `test_root_scripts.py` | Mocks subprocess + direct import | OLD pattern (pre-KAI-10); mocks subprocess.run() at the run_league_helper.py level |
| `test_run_accuracy_simulation.py` | Mix: subprocess.run(--help) + direct argparse recreation | CLI flag tests via --help invocation |
| `test_run_schedule_fetcher.py` | Source code inspection (reads .py files and asserts on content) | Tests logger naming, print removal |
| `test_run_win_rate_simulation.py` | Mix: subprocess.run(--help) + direct argparse + source inspection | 28 tests (6 flag unit + 8 flag integration + 12 DEBUG quality) |

**Key insight:** The root_scripts tests are NOT the same as what F08 builds. They test OLD features (logging refactoring). F08's new tests are CLI invocation with --e2e-test (KAI-10's new flag).

---

## Naming Conflict Analysis

F08 proposes these new filenames:
- `test_player_fetcher_cli.py` — NEW, no conflict
- `test_schedule_fetcher_cli.py` — NEW (existing `test_schedule_fetcher_integration.py` is different)
- `test_game_data_fetcher_cli.py` — NEW, no conflict
- `test_historical_compiler_cli.py` — NEW (existing `test_historical_data_compiler_integration.py` is different)
- `test_league_helper_cli.py` — NEW (existing `test_league_helper_integration.py` is different)

**No naming conflicts.** Existing files test different things (Python classes / logging) while new files test CLI invocation with --e2e-test.

---

## E2E Behavior Summary (from F01-F07 specs)

| Feature | Script | E2E Mode Behavior | Graceful Skip? |
|---------|--------|--------------------|----------------|
| F01 | run_player_fetcher.py | espn_player_limit=100 | YES — exit 0 if drafted_data.csv missing |
| F02 | run_schedule_fetcher.py | max_weeks=1 | NO — API calls (may exit 1 if API down) |
| F03 | run_game_data_fetcher.py | API calls only | NO — API calls (may exit 1 if API down) |
| F04 | compile_historical_data.py | tempfile for output | NO — always succeeds (tempfile) |
| F05 | run_win_rate_simulation.py | mode=single, sims=1, workers=1 | YES — exit 0 if sim data missing |
| F06 | run_accuracy_simulation.py | single run, minimal dataset | YES — exit 0 if data missing |
| F07 | run_league_helper.py | all 5 modes via execute_e2e() | YES — exit 0 if league_config.json missing |

**Implication for F08 tests:**
- F04 only: `assert result.returncode == 0` (exact exit 0 guaranteed)
- F01, F05, F06, F07: `assert result.returncode == 0` (graceful skip → exit 0; success → exit 0)
- F02, F03: `assert result.returncode in [0, 1]` (API may be unavailable)

---

## CLI Argument Summary (for help text assertions)

| Feature | Universal Args | Script-Specific Args | Total |
|---------|---------------|---------------------|-------|
| F01 | --e2e-test, --log-level | --week, --season, --my-team-name, --load-drafted-data, --drafted-data-path, --position-json-output, --team-data-folder, --game-data-csv, --enable-historical-save, --enable-game-data, --espn-player-limit, --request-timeout, --rate-limit-delay, --progress-frequency, --enable-log-file | 17 |
| F02 | --e2e-test, --log-level | --season, --output-path, --enable-log-file | 5 |
| F03 | --e2e-test, --log-level | 4 existing + --request-timeout + --historical-season | 8 |
| F04 | --e2e-test, --log-level | --year, --verbose, --enable-log-file, --output-dir, --timeout, --rate-limit-delay | 8 |
| F05 | --e2e-test, --log-level | 9 existing args | 11 |
| F06 | --e2e-test | 10 existing args (has --log-level already; normalizes via str.upper) | 11 |
| F07 | --e2e-test, --log-level | --my-team-name, --recommendation-count, --min-waiver-improvement, --num-runners-up, --min-trade-improvement, --data-folder, --mode, --week, --season, --enable-log-file | 12 |

---

## subprocess.run() Pattern (from test_schedule_fetcher_integration.py)

```python
result = subprocess.run(
    [sys.executable, str(script_path), '--enable-log-file'],
    capture_output=True,
    text=True,
    timeout=60
)
assert result.returncode in [0, 1]
```

F08's pattern uses `--e2e-test` instead of `--enable-log-file`, and timeout=180.

---

## Master Runner Precedents

No existing `run_all_integration_tests.py` in codebase. The DISCOVERY.md specifies its creation as a deliverable of F08. Closest analog is `run_player_fetcher.py` (runner scripts that invoke other scripts), but those are production scripts.

The master runner should:
1. Run pytest on the 7 CLI test files
2. Report 7/7 pass
3. Exit code 0 if all pass, 1 if any fail
