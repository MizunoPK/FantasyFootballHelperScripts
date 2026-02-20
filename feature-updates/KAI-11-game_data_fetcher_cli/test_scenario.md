## Test Scenario: game_data_fetcher_cli (KAI-11 Feature 01)

**Feature:** run_game_data_fetcher.py CLI refactoring
**Stage:** S7.P1 Smoke Testing
**Created:** 2026-02-19

---

## Test Scenario: E2E CLI Execution

**Entry Point:** `python run_game_data_fetcher.py --e2e-test`

**Input Data:**
- No local input files needed — script fetches from ESPN + Open-Meteo APIs
- `--e2e-test` mode limits to week 1 only (faster execution, ≤180s per spec)
- Output written to `/tmp/game_data_e2e_test.csv` (hardcoded override per REQ-06)

**Expected Behavior:**
- Script imports cleanly (no os, no config, no subprocess)
- `--help` shows 8 args: --season, --output, --weeks, --current-week, --e2e-test, --log-level, --request-timeout, --historical-season
- E2E mode fetches week 1 data from live APIs
- Output CSV written to `/tmp/game_data_e2e_test.csv`
- Script exits with code 0

**Validation Criteria:**
1. `/tmp/game_data_e2e_test.csv` exists after execution
2. CSV has at least 1 row (week 1 has real games)
3. `week` column contains value 1 (correct week)
4. Game-related columns are populated (home_team, away_team, etc.)
5. Logs show E2E test mode activation message

**Scope:** Feature in ISOLATION — no cross-feature tests (saved for S9)
