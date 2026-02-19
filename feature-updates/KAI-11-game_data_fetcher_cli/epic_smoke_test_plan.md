## Epic Smoke Test Plan: game_data_fetcher_cli

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** 2026-02-19 (S1)
**Last Updated:** 2026-02-19 (S1 — INITIAL)

> ⚠️ INITIAL VERSION — Based on S1 assumptions. Will be updated in S4 and after S8.P2.

---

## Epic Success Criteria

**The epic is successful if:**

1. `run_game_data_fetcher.py --help` shows all 8 CLI arguments (4 existing + 4 new)
2. `run_game_data_fetcher.py --e2e-test` completes in ≤180s and writes only to `/tmp/`
3. `run_game_data_fetcher.py` (no args) behaves identically to pre-refactor (season=2025, week=17)
4. `grep "from config import" run_game_data_fetcher.py` returns empty
5. `grep "os.chdir" run_game_data_fetcher.py` returns empty
6. All existing tests continue to pass (100% pass rate)

**Epic is considered SUCCESSFUL when ALL criteria above are met.**

---

## Update History

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| 2026-02-19 | S1 | (initial) | Initial plan created | Epic planning based on S1 assumptions |

---

## Test Scenarios (INITIAL — Will Refine in S4/S8.P2)

### Part 1: Import / Structure Tests

**Scenario 1: Import test**
```bash
python -c "import run_game_data_fetcher; print('OK')"
```
**Expected:** No import errors

**Scenario 2: Help output**
```bash
python run_game_data_fetcher.py --help
```
**Expected:** 8 arguments shown, no crashes

---

### Part 2: CLI Argument Tests

**Scenario 3: E2E test mode**
```bash
python run_game_data_fetcher.py --e2e-test
```
**Expected:** Exits 0 in ≤180s; `/tmp/game_data_e2e_test.csv` created; `data/game_data.csv` NOT modified

**Scenario 4: Log-level passthrough**
```bash
python run_game_data_fetcher.py --e2e-test --log-level DEBUG
```
**Expected:** Exits 0; DEBUG-level log lines visible

**Scenario 5: Historical season flag**
```bash
python run_game_data_fetcher.py --season 2024 --historical-season --e2e-test
```
**Expected:** Exits 0; current_week set to 18 (visible in log)

---

### Part 3: Backward Compatibility

**Scenario 6: No-args behavior**
```bash
python run_game_data_fetcher.py --help | grep -E "(season|current-week|output|weeks)"
```
**Expected:** Same default values as before refactor (season=2025, current-week=17)

**Scenario 7: Grep checks**
```bash
grep "from config import" run_game_data_fetcher.py  # should return empty
grep "os.chdir" run_game_data_fetcher.py             # should return empty
```
**Expected:** Both return empty

---

### Part 4: Unit Test Suite

**Scenario 8: Full test suite**
```bash
pytest tests/ -v
```
**Expected:** 100% passed, 0 failed

---

## Execution Checklist (For S9)

**Part 1: Import / Structure**
- [ ] Scenario 1: Import test — ◻️
- [ ] Scenario 2: Help output — ◻️

**Part 2: CLI Argument Tests**
- [ ] Scenario 3: E2E test mode — ◻️
- [ ] Scenario 4: Log-level passthrough — ◻️
- [ ] Scenario 5: Historical season flag — ◻️

**Part 3: Backward Compatibility**
- [ ] Scenario 6: No-args behavior — ◻️
- [ ] Scenario 7: Grep checks — ◻️

**Part 4: Unit Test Suite**
- [ ] Scenario 8: Full test suite — ◻️

**Overall Status:** NOT STARTED
