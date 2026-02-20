## Expected Results: game_data_fetcher_cli (KAI-11 Feature 01)

**Feature:** run_game_data_fetcher.py CLI refactoring
**Stage:** S7.P1 Smoke Testing
**Created:** 2026-02-19

---

## Part 1: Import Test — Expected Results

**Command:** `python -c "import run_game_data_fetcher; print('OK')"`

**Expected:**
- Exit code 0
- Output: `OK`
- No import errors, no ModuleNotFoundError, no AttributeError

**Anti-patterns to detect:**
- `ModuleNotFoundError: No module named 'os'` (removed — good)
- `ImportError: cannot import name 'NFL_SEASON' from 'config'` (removed — good)
- Any unexpected `DeprecationWarning` at import time

---

## Part 2: Entry Point Test — Expected Results

**Command:** `python run_game_data_fetcher.py --help`

**Expected output includes all 8 args:**
- `--season` (default: 2025)
- `--output` (default: None → data/game_data.csv)
- `--weeks`
- `--current-week` (default: 17)
- `--e2e-test` (flag)
- `--log-level` (choices: DEBUG INFO WARNING ERROR CRITICAL, default: INFO)
- `--request-timeout` (default: 30)
- `--historical-season` (flag)

**Expected exit code:** 0 (help always exits 0)

---

## Part 3: E2E Test — Expected Results

**Command:** `python run_game_data_fetcher.py --e2e-test`

### Output File
- **Path:** `/tmp/game_data_e2e_test.csv`
- **Format:** CSV with header row
- **Minimum rows:** 1 (week 1 has NFL games)
- **Expected week column values:** 1 (only week 1 in E2E mode per REQ-06)

### Data Value Ranges
| Column | Expected | Notes |
|--------|----------|-------|
| `week` | 1 | E2E mode forces week 1 |
| `home_team` | non-empty string | NFL team abbreviation |
| `away_team` | non-empty string | NFL team abbreviation |
| `season` | 2025 | default season |

### Log Messages (Required)
- Must contain: `E2E test mode: limiting to week 1`
- Must contain: `Game Data Fetcher Configuration:`
- Must contain: `Season: 2025`
- Must contain: `Current Week: 17`
- Must not contain ERROR level messages (unless API unavailable)

### Exit Code
- **Success:** 0
- **API failure:** Non-zero with `[ERROR]` prefix on stdout (acceptable in E2E if network unavailable)

---

## Pass/Fail Criteria Summary

| Check | Pass Condition | Fail Condition |
|-------|---------------|----------------|
| P1 Import | Exit 0, "OK" printed | Any import error |
| P2 Help | 8 args listed, exit 0 | Missing args, crash |
| P3 File exists | `/tmp/game_data_e2e_test.csv` created | File not created |
| P3 Data rows | len(df) > 0 | Empty CSV |
| P3 Week column | df['week'] == 1 | Wrong week values |
| P3 Team columns | Non-empty strings | Null/empty teams |
| P3 Logs | E2E mode message present | Missing log message |
