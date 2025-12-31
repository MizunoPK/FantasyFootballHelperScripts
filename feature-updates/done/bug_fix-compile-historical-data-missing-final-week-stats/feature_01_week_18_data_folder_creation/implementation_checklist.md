# Feature 01: week_18_data_folder_creation - Implementation Checklist

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**Update this file IN REAL-TIME (not batched at end)**

---

## Requirements from spec.md

### Objective Requirements

- [x] **REQ-1:** Add VALIDATION_WEEKS = 18 constant to constants.py
  - TODO Task: Task 1
  - Implementation: constants.py:91 (new constant added)
  - Verified: 2025-12-31 12:42 ✅ Matches spec exactly

- [x] **REQ-2:** Keep REGULAR_SEASON_WEEKS = 17 unchanged
  - TODO Task: Task 1
  - Implementation: constants.py:88 (unchanged)
  - Verified: 2025-12-31 12:42 ✅ Value remains 17

- [x] **REQ-3:** Update create_output_directories() to create week_18 folder
  - TODO Task: Task 2
  - Implementation: compile_historical_data.py:143 (loop uses VALIDATION_WEEKS)
  - Verified: 2025-12-31 12:43 ✅ Creates week_01 through week_18

- [x] **REQ-4:** Update generate_all_weeks() to generate week_18 snapshot
  - TODO Task: Task 3
  - Implementation: weekly_snapshot_generator.py:136 (loop uses VALIDATION_WEEKS)
  - Verified: 2025-12-31 12:44 ✅ Generates snapshots for weeks 1-18

- [x] **REQ-5:** Week 18 contains week 17 actuals only (no projections)
  - TODO Task: Task 4
  - Implementation: weekly_snapshot_generator.py:215-227 (existing logic handles it)
  - Verified: 2025-12-31 12:50 ✅ For week 18, all weeks 1-17 < 18, so uses actuals

- [x] **REQ-6:** Week 18 players.csv = players_projected.csv (identical)
  - TODO Task: Task 4
  - Implementation: weekly_snapshot_generator.py:289-292 (special case added)
  - Verified: 2025-12-31 12:50 ✅ Calls same method for week 18

- [x] **REQ-7:** Week 18 generates CSV + JSON files (same as weeks 1-17)
  - TODO Task: Task 5
  - Implementation: Existing logic (no code changes needed)
  - Verified: 2025-12-31 12:52 ✅ Same generation logic for all weeks

---

### Algorithm Requirements

- [x] **ALG-1:** Folder creation loop uses VALIDATION_WEEKS instead of REGULAR_SEASON_WEEKS
  - Spec: Components Affected, item 2
  - TODO Task: Task 2
  - Implementation: compile_historical_data.py:143
  - Verified: 2025-12-31 12:43 ✅ Loop range(1, VALIDATION_WEEKS + 1)

- [x] **ALG-2:** Snapshot generation loop uses VALIDATION_WEEKS instead of REGULAR_SEASON_WEEKS
  - Spec: Components Affected, item 3
  - TODO Task: Task 3
  - Implementation: weekly_snapshot_generator.py:136
  - Verified: 2025-12-31 12:44 ✅ Loop range(1, VALIDATION_WEEKS + 1)

- [x] **ALG-3:** Special case for week 18: Use actuals for weeks 1-17 only
  - Spec: Implementation Approach
  - TODO Task: Task 4
  - Implementation: weekly_snapshot_generator.py:215-227 (_write_players_snapshot)
  - Verified: 2025-12-31 12:50 ✅ Existing conditional logic (week < current_week)

- [x] **ALG-4:** Special case for week 18: players_projected.csv identical to players.csv
  - Spec: Implementation Approach
  - TODO Task: Task 4
  - Implementation: weekly_snapshot_generator.py:289-292 (_write_projected_snapshot)
  - Verified: 2025-12-31 12:50 ✅ Special case calls _write_players_snapshot

---

### File Format Requirements

- [x] **FMT-1:** Week 18 CSV columns match weeks 1-17
  - Spec: Implementation Approach
  - TODO Task: Task 5
  - Implementation: Verification only (no code changes)
  - Verified: 2025-12-31 12:52 ✅ Both CSV files use PLAYERS_CSV_COLUMNS

- [x] **FMT-2:** Week 18 JSON structure matches weeks 1-17
  - Spec: Implementation Approach
  - TODO Task: Task 5
  - Implementation: Verification only (no code changes)
  - Verified: 2025-12-31 12:52 ✅ generate_json_snapshots() same for all weeks

- [x] **FMT-3:** Week 18 has 8 files total (2 CSV + 6 JSON)
  - Spec: Implementation Approach
  - TODO Task: Task 5
  - Implementation: Verification only (no code changes)
  - Verified: 2025-12-31 12:52 ✅ Same file count as weeks 1-17

---

### Import Requirements

- [x] **IMP-1:** Import VALIDATION_WEEKS in compile_historical_data.py
  - TODO Task: Task 2
  - Implementation: compile_historical_data.py:36 (added to import list)
  - Verified: 2025-12-31 12:43 ✅ Import added

- [x] **IMP-2:** Import VALIDATION_WEEKS in weekly_snapshot_generator.py
  - TODO Task: Task 3
  - Implementation: weekly_snapshot_generator.py:21 (added to import list)
  - Verified: 2025-12-31 12:44 ✅ Import added

---

### Log Message Requirements

- [x] **LOG-1:** Update log message in generate_all_weeks() to show 18 snapshots
  - TODO Task: Task 3
  - Implementation: weekly_snapshot_generator.py:132, 139 (log messages updated)
  - Verified: 2025-12-31 12:44 ✅ Logs show "weeks 1-18" and "18 weekly snapshots"

---

## Summary

**Total Requirements:** 17
**Implemented:** 17 ✅ ALL COMPLETE
**Remaining:** 0

**Last Updated:** 2025-12-31 12:52
