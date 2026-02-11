# Feature 05: win_rate_sim_logging - Implementation Checklist

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**Update this file IN REAL-TIME (not batched at end)**

---

## R1: CLI Flag Integration

- [x] **R1.1:** Add --enable-log-file argument to argparse parser (action='store_true', default=False)
- [x] **R1.2:** Remove LOGGING_TO_FILE constant from run_win_rate_simulation.py
- [x] **R1.3:** Remove LOGGING_FILE constant (no longer used, Feature 01 auto-generates)
- [x] **R1.4:** Update LOG_NAME from "simulation" to "win_rate_simulation"
- [x] **R1.5:** Update setup_logger() call to use args.enable_log_file, log_file_path=None
- [x] **R1.6:** Move setup_logger() call to AFTER args are parsed
- [x] **R1.7:** Existing script behavior preserved when flag not provided
- [x] **R1.8:** Flag works across all modes (single, full, iterative)
- [x] **R1.9:** Remove test assertion for LOGGING_TO_FILE in test_root_scripts.py
- [x] **R1.10:** Update test assertion for LOG_NAME value in test_root_scripts.py

## R2: DEBUG Level Quality

- [x] **R2.1:** Audit SimulationManager.py DEBUG calls (9 calls) - 8 kept, 1 removed
- [x] **R2.2:** Audit ParallelLeagueRunner.py DEBUG calls (16 calls) - 7 kept, 8 removed
- [x] **R2.3:** Audit SimulatedLeague.py DEBUG calls (27 calls) - 12 kept, 15 removed
- [x] **R2.4:** Audit DraftHelperTeam.py DEBUG calls (6 calls) - 1 kept, 4 removed
- [x] **R2.5:** Audit SimulatedOpponent.py DEBUG calls (5 calls) - 2 kept, 3 removed
- [x] **R2.6:** Audit Week.py DEBUG calls (6 calls) - 3 kept, 3 removed
- [x] **R2.7:** Audit manual_simulation.py DEBUG calls (0 calls) - confirmed 0
- [x] **R2.8:** All existing tests pass after DEBUG changes (100%)

## R3: INFO Level Quality

- [ ] **R3.1:** Audit SimulationManager.py INFO calls
- [ ] **R3.2:** Audit ParallelLeagueRunner.py INFO calls (6 calls)
- [ ] **R3.3:** Audit SimulatedLeague.py INFO calls (1 call)
- [ ] **R3.4:** Audit DraftHelperTeam.py INFO calls (0 calls)
- [ ] **R3.5:** Audit SimulatedOpponent.py INFO calls (0 calls)
- [ ] **R3.6:** Audit Week.py INFO calls (0 calls)
- [ ] **R3.7:** Audit manual_simulation.py INFO calls (6 calls)
- [ ] **R3.8:** All existing tests pass after INFO changes (100%)

## Test Coverage

- [x] **T1:** R1 CLI flag unit tests created (6 tests)
- [x] **T2:** R1 CLI flag integration tests created (8 tests)
- [x] **T3:** R2 DEBUG quality tests created (14 tests: 12 unit + 2 integration)
- [ ] **T4:** R3 INFO quality tests created (14 tests)
- [ ] **T5:** Edge case and config tests created (9 tests)

---

## Summary

**Total Requirements:** 33
**Implemented:** 21
**Remaining:** 12

**Last Updated:** 2026-02-11 (Phase 2 complete)
