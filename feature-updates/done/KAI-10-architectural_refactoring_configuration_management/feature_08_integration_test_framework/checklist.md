## Feature Checklist: integration_test_framework

**Status:** ALL RESOLVED — Gate 3 pending
**Last Updated:** 2026-02-18

All 4 checklist items have been answered by user (2026-02-18).

---

## Q1: CLI test file location — tests/integration/ vs tests/cli/?

**Answer:** Option A — `tests/integration/`

**Rationale:** Follows the existing subprocess.run() CLI test pattern established by test_schedule_fetcher_integration.py. No new directory needed.

**Impact on spec:** REQ-01 confirmed — all 5 new files in tests/integration/.

[x] RESOLVED — 2026-02-18

---

## Q2: Exit code strictness for API-dependent tests

**Answer:** Option B — `returncode == 0` only (STRICT)

**Rationale:** User chose strict exit code assertion. All 7 test scripts must exit 0. For API-dependent scripts (F02 schedule_fetcher, F03 game_data_fetcher), this means the test environment must have ESPN API access. Tests will fail if the API is unavailable.

**Impact on spec:** REQ-02 updated — `assert result.returncode == 0` for ALL scripts (removed `returncode in [0,1]` pattern). REQ-04 and REQ-05 updated accordingly.

[x] RESOLVED — 2026-02-18

---

## Q3: Timeout warning implementation

**Answer:** Option A — Catch `TimeoutExpired` → `warnings.warn()`

**Rationale:** Catch `subprocess.TimeoutExpired`, emit a `warnings.warn(RuntimeWarning)`, and return (test passes with warning). Implements the Discovery "warn only" policy.

**Impact on spec:** REQ-02 updated with timeout implementation pattern.

[x] RESOLVED — 2026-02-18

---

## Q4: Master runner implementation approach

**Answer:** Option A — pytest subprocess, all 7 at once

**Rationale:** `subprocess.run([sys.executable, "-m", "pytest", "-v"] + TEST_FILES)`. Simple, leverages pytest reporting. Single exit code covers all 7 test files.

**Impact on spec:** REQ-10 confirmed — master runner uses single pytest invocation.

[x] RESOLVED — 2026-02-18

---

## Summary

| Q# | Question | Decision |
|----|----------|----------|
| Q1 | CLI test file location | ✅ tests/integration/ |
| Q2 | Exit code strictness | ✅ returncode == 0 (strict) |
| Q3 | Timeout warning implementation | ✅ Catch TimeoutExpired → warnings.warn() |
| Q4 | Master runner approach | ✅ pytest subprocess, all 7 at once |
