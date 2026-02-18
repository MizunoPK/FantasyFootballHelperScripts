# Feature 04: historical_compiler_cli — Checklist

**Status:** APPROVED — Gate 3 passed 2026-02-18
**Last Updated:** 2026-02-18

---

## Questions

### Q1: E2E Mode — Data Limiting Strategy

**Status:** RESOLVED — User Answer: Option A (limit players to 100)

- [x] Answered: Limit player count to 100 in E2E mode (consistent with Feature 01 pattern)

---

### Q2: --debug Mode — Reduced Scope for This Script

**Status:** NOT APPLICABLE — Design correction confirmed 2026-02-18

- [x] N/A: No `--debug` flag in this epic. Universal args are `--e2e-test` and `--log-level` only.

---

### Q3: Additional Script-Specific Args — Are These In Scope?

**Status:** RESOLVED — User Answer: Option A (no additional args)

- [x] Answered: Only DISCOVERY-confirmed args in scope. `--weeks`, `--validate`, `--clean`, `--skip-backups`, `--generate-csv`, `--no-json`, `--max-retries` all out of scope.

---

### Q4: Settings Dataclass Pattern — Apply or Skip for This Script?

**Status:** RESOLVED — User Answer: Option A (direct params)

- [x] Answered: Pass `timeout`, `rate_limit_delay`, `e2e_test` as explicit function params to `compile_season_data()`. No Settings dataclass.

---

### Q5: E2E Mode — Output Directory Behavior

**Status:** RESOLVED — User Answer: Option A (temp directory)

- [x] Answered: E2E mode writes to `tempfile.TemporaryDirectory()`. Real `simulation/sim_data/` is never touched.

---

## Summary

| Q# | Topic | Status |
|----|-------|--------|
| Q1 | E2E mode data limiting | [x] RESOLVED — Option A (players=100) |
| Q2 | --debug reduced scope | [x] N/A — no --debug flag |
| Q3 | Additional args scope | [x] RESOLVED — Option A (none) |
| Q4 | Settings dataclass vs direct params | [x] RESOLVED — Option A (direct params) |
| Q5 | E2E output directory | [x] RESOLVED — Option A (temp dir) |

**Gate 3: USER APPROVED 2026-02-18**
