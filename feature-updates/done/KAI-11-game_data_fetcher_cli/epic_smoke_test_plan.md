## Epic Smoke Test Plan: game_data_fetcher_cli

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** 2026-02-19 (S1)
**Last Updated:** 2026-02-19 (S8.P2 — NO CHANGE: implementation matched spec exactly)

> S8.P2 REVIEW COMPLETE — All 8 scenarios, integration points, and success criteria verified against
> actual implementation. No changes required: implementation matched S3 spec plan exactly.

---

## Integration Points

### Integration Point 1: run_game_data_fetcher.py → fetch_game_data()

**Features Involved:** feature_01_game_data_fetcher_cli
**Type:** Direct function call (no subprocess)
**Flow:**
- Runner: parses CLI args, builds params, calls `fetch_game_data()`
- `fetch_game_data()`: accepts `request_timeout` (KAI-10 REQ-09 already applied)
- Runner: passes `request_timeout=args.request_timeout` (REQ-10)

**Test Need:** Verify runner correctly passes all args to fetch_game_data() including new request_timeout param.

### Integration Point 2: run_game_data_fetcher.py → setup_logger()

**Features Involved:** feature_01_game_data_fetcher_cli
**Type:** Direct function call
**Flow:**
- Runner: passes `args.log_level` (not hardcoded "INFO") to setup_logger()

**Test Need:** Verify --log-level DEBUG produces DEBUG output, default produces INFO output.

---

## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: All 8 CLI Args Present
✅ **MEASURABLE:** `python run_game_data_fetcher.py --help` output contains all 8 args with correct defaults

**Verification:**
```bash
python run_game_data_fetcher.py --help | grep -E "(season|current-week|output|weeks|e2e-test|log-level|request-timeout|historical-season)"
```
Expected: 8 lines, each showing an argument name

### Criterion 2: E2E Mode Completes and Writes to /tmp Only
✅ **MEASURABLE:** `--e2e-test` completes in ≤180s AND writes `/tmp/game_data_e2e_test.csv` AND does NOT modify `data/game_data.csv`

**Verification:**
```bash
# Record data/ file state before
md5sum data/game_data.csv > /tmp/before.md5

# Run E2E
time python run_game_data_fetcher.py --e2e-test

# Verify /tmp file created, data/ unchanged
ls -la /tmp/game_data_e2e_test.csv
md5sum -c /tmp/before.md5
```

### Criterion 3: Config Imports Removed
✅ **MEASURABLE:** grep returns empty for both config import and os.chdir patterns

**Verification:**
```bash
grep "from config import" run_game_data_fetcher.py  # must return empty
grep "os.chdir" run_game_data_fetcher.py             # must return empty
```

### Criterion 4: Backward Compatibility Preserved
✅ **MEASURABLE:** Default argparse values match pre-refactor config values exactly

**Verification:**
```bash
python run_game_data_fetcher.py --help | grep -A1 "\-\-season"    # default: 2025
python run_game_data_fetcher.py --help | grep -A1 "\-\-current-week"  # default: 17
```

### Criterion 5: Unit Test Suite 100% Pass
✅ **MEASURABLE:** pytest reports 0 failures, all tests pass

**Verification:**
```bash
pytest tests/ -v 2>&1 | tail -5
```
Expected: `X passed, 0 failed`

---

## Specific Test Scenarios

### Scenario 1: Import Test

**Purpose:** Verify runner imports without error after removing config dependency

**Steps:**
1. Navigate to project root
2. Run: `python -c "import run_game_data_fetcher; print('OK')"`

**Expected Results:**
✅ Output: `OK`
✅ No ImportError for config module
✅ No ImportError for any other module

**Failure Indicators:**
❌ `ModuleNotFoundError: No module named 'config'` → config import not fully removed
❌ Any other ImportError → sys.path setup broken

---

### Scenario 2: Help Output

**Purpose:** Verify all 8 arguments are present with correct defaults

**Steps:**
1. Run: `python run_game_data_fetcher.py --help`

**Expected Results:**
✅ `--season` shown with default `2025` (not `None`)
✅ `--current-week` shown with default `17` (not `None`)
✅ `--e2e-test` shown as flag
✅ `--log-level` shown with choices `{DEBUG,INFO,WARNING,ERROR,CRITICAL}` and default `INFO`
✅ `--request-timeout` shown with default `30`
✅ `--historical-season` shown as flag
✅ `--output` shown
✅ `--weeks` shown

**Failure Indicators:**
❌ Any argument missing → not added to parse_args()
❌ `--season` default is `None` → argparse default not updated (REQ-02 not implemented)

---

### Scenario 3: E2E Test Mode

**Purpose:** Verify E2E mode completes fast, writes to /tmp only, leaves data/ unchanged

**Steps:**
1. `md5sum data/game_data.csv > /tmp/game_data_before.md5` (save checksum)
2. `time python run_game_data_fetcher.py --e2e-test`
3. `ls -la /tmp/game_data_e2e_test.csv`
4. `md5sum -c /tmp/game_data_before.md5` (verify data/ unchanged)

**Expected Results:**
✅ Exit code 0
✅ Completes in ≤180 seconds
✅ `/tmp/game_data_e2e_test.csv` exists and is non-empty
✅ `data/game_data.csv` checksum unchanged
✅ Log output shows "E2E test mode: limiting to week 1"

**Failure Indicators:**
❌ Exceeds 180s → E2E scope not limited to Week 1
❌ `/tmp/game_data_e2e_test.csv` not created → output path override not implemented
❌ `data/game_data.csv` checksum changed → E2E output path not redirected to /tmp

---

### Scenario 4: Log-Level Passthrough

**Purpose:** Verify --log-level is wired to setup_logger() (not hardcoded INFO)

**Steps:**
1. `python run_game_data_fetcher.py --e2e-test --log-level DEBUG 2>&1 | head -20`

**Expected Results:**
✅ Exit code 0
✅ DEBUG-level log lines visible (e.g., lines containing `DEBUG`)
✅ More verbose output than default INFO run

**Failure Indicators:**
❌ No DEBUG lines → log_level not passed to setup_logger() (REQ-05 not implemented)

---

### Scenario 5: Historical Season Flag

**Purpose:** Verify --historical-season sets current_week to 18 explicitly

**Steps:**
1. `python run_game_data_fetcher.py --season 2024 --historical-season --e2e-test --log-level INFO 2>&1 | grep -i "week\|historical"`

**Expected Results:**
✅ Exit code 0
✅ Log contains "Historical season mode" message
✅ Log shows current_week=18 or fetches week 1 with historical context

**Failure Indicators:**
❌ No "historical" log message → --historical-season not implemented (REQ-09 missing)
❌ Implicit year-comparison still present → old logic not replaced

---

### Scenario 6: Backward Compatibility

**Purpose:** Verify no-args behavior is identical to pre-refactor

**Steps:**
1. `python run_game_data_fetcher.py --help | grep -E "default|Default"`

**Expected Results:**
✅ `--season` default: `2025`
✅ `--current-week` default: `17`
✅ `--output` behavior unchanged
✅ `--log-level` default: `INFO`

**Failure Indicators:**
❌ Any default differs from above → backward compatibility broken (REQ-08 violated)

---

### Scenario 7: Grep Checks (Anti-Pattern Removal)

**Purpose:** Verify both anti-patterns fully removed from source

**Steps:**
```bash
grep "from config import" run_game_data_fetcher.py
grep "os.chdir" run_game_data_fetcher.py
```

**Expected Results:**
✅ Both commands return empty (exit code 1 / no matches)

**Failure Indicators:**
❌ Any output → anti-pattern not fully removed

---

### Scenario 8: Full Unit Test Suite

**Purpose:** Verify 100% pass rate including new test class

**Steps:**
1. `pytest tests/ -v`

**Expected Results:**
✅ `tests/root_scripts/test_run_game_data_fetcher.py` listed with 3 tests
✅ All 3 new tests pass: `test_has_parse_args`, `test_parse_args_defaults`, `test_no_subprocess`
✅ All existing tests pass (0 failures, 0 errors)

**Failure Indicators:**
❌ test_run_game_data_fetcher.py not found → test file not created (REQ-11 missing)
❌ test_parse_args_defaults fails → parse_args() not extracted or defaults wrong
❌ Any other failure → regression introduced

---

## Execution Checklist (For S9)

**Part 1: Import / Structure**
- [x] Scenario 1: Import test — ✅ PASSED (S7.P1 Part 1 — import OK, parse_args callable)
- [x] Scenario 2: Help output — ✅ PASSED (S7.P1 Part 2 — all 8 args, correct defaults)

**Part 2: CLI Argument Tests**
- [x] Scenario 3: E2E test mode — ✅ PASSED (S7.P1 Part 3 — 16 games, ~8s, /tmp path, data/ unchanged)
- [x] Scenario 4: Log-level passthrough — ✅ PASSED (S7.P2 Round 1 — DEBUG lines visible)
- [x] Scenario 5: Historical season flag — ✅ PASSED (S7.P2 Round 1 — current_week=18 confirmed)

**Part 3: Backward Compatibility**
- [x] Scenario 6: No-args behavior — ✅ PASSED (S7.P1 Part 2 — defaults: season=2025, week=17)
- [x] Scenario 7: Grep checks — ✅ PASSED (S7.P2 Round 1 — no config import, no os.chdir)

**Part 4: Unit Test Suite**
- [x] Scenario 8: Full test suite — ✅ PASSED (S7.P1 Part 1 — 2714/2714 tests, 3 new tests)

**Overall Status:** ALL SCENARIOS PRE-VERIFIED (S7.P1 smoke test + S7.P2 QC rounds)
**S9.P3 User Testing:** PENDING — scenarios ready for user to re-run as acceptance tests

---

## Update History

| Date | Stage | What Changed | Why |
|------|-------|-------------|-----|
| 2026-02-19 | S1 | Initial plan created | Epic planning based on S1 assumptions |
| 2026-02-19 | S3 | Updated to S3 version | Refined with approved spec.md details; added integration points, measurable success criteria, concrete commands |
| 2026-02-19 | S8.P2 | NO CHANGE to scenarios; updated header note, execution checklist with S7 results | Implementation matched S3 plan exactly; all 8 scenarios pre-verified in S7.P1 + S7.P2 |
