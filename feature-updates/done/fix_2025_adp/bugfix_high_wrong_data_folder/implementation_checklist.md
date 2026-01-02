# Bug Fix: Wrong Data Folder - Implementation Checklist

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**UPDATE THIS FILE IN REAL-TIME (not batched at end)**

---

## Core Implementation Requirements (spec.md sections 1-2)

- [x] **REQ-1:** Update function signature to accept sim_data_folder parameter
  - TODO Task: Task 1
  - Spec Location: spec.md lines 67-82
  - Implementation: update_player_adp_values() signature (utils/adp_updater.py:146-149)
  - Verified: 2026-01-01 00:50 ✅ Code matches spec exactly

- [x] **REQ-2:** Discover week folders dynamically using glob pattern
  - TODO Task: Task 2
  - Spec Location: spec.md lines 86-90
  - Implementation: Week folder discovery logic (utils/adp_updater.py:209-218)
  - Verified: 2026-01-01 00:50 ✅ Uses sorted glob('week_*') as specified

- [x] **REQ-3:** Iterate through each week folder sequentially
  - TODO Task: Task 3
  - Spec Location: spec.md lines 86-90
  - Implementation: Week iteration loop (utils/adp_updater.py:230-305)
  - Verified: 2026-01-01 00:50 ✅ Iterates through all discovered weeks

- [x] **REQ-4:** Load JSON as direct array (not wrapped dict)
  - TODO Task: Task 4
  - Spec Location: spec.md lines 91-95
  - Implementation: JSON loading logic (utils/adp_updater.py:243-258)
  - Verified: 2026-01-01 00:58 ✅ Loads as list, validates structure

- [x] **REQ-5:** Match players within each week using fuzzy matching
  - TODO Task: Task 5
  - Spec Location: spec.md lines 84
  - Implementation: Player matching per week (utils/adp_updater.py:262-296)
  - Verified: 2026-01-01 00:58 ✅ Works with direct arrays, no changes needed

- [x] **REQ-6:** Update ADP values in each week's player arrays
  - TODO Task: Task 6
  - Spec Location: spec.md lines 84
  - Implementation: ADP value assignment (utils/adp_updater.py:265-266)
  - Verified: 2026-01-01 00:58 ✅ Updates list elements directly

- [x] **REQ-7:** Write back as direct arrays using atomic write pattern
  - TODO Task: Task 7
  - Spec Location: spec.md lines 96-99
  - Implementation: Direct array write + atomic pattern (utils/adp_updater.py:305-318)
  - Verified: 2026-01-01 00:58 ✅ Writes list directly with atomic pattern

- [x] **REQ-8:** Aggregate match report across all weeks
  - TODO Task: Task 8
  - Spec Location: spec.md lines 101-104
  - Implementation: Match report aggregation (utils/adp_updater.py:220-354)
  - Verified: 2026-01-01 00:58 ✅ Accumulates across all weeks correctly

- [x] **REQ-9:** Log progress per week (INFO level)
  - TODO Task: Task 9
  - Spec Location: spec.md lines 105
  - Implementation: Per-week logging (utils/adp_updater.py:233, 305)
  - Verified: 2026-01-01 00:50 ✅ Logs "Processing {week_name}..." and final status

---

## Data Structure Requirements (spec.md section 1)

- [ ] **DATA-1:** Process all 18 weeks (week_01 through week_18)
  - Spec Location: spec.md lines 17-19
  - TODO Task: Task 2, 3
  - Implementation: Week iteration covers all 18 weeks
  - Verified: {Check after implementing}

- [ ] **DATA-2:** Process 6 position files per week
  - Spec Location: spec.md lines 17-19
  - TODO Task: Task 3
  - Implementation: Loop through POSITION_FILES dict
  - Verified: {Check after implementing}

- [ ] **DATA-3:** Total 108 files updated (18 weeks × 6 positions)
  - Spec Location: spec.md lines 17-19
  - TODO Task: Task 7
  - Implementation: Verify file count in logs
  - Verified: {Check after implementing}

- [ ] **DATA-4:** Direct JSON array structure preserved
  - Spec Location: spec.md lines 41-47
  - TODO Task: Task 4, 7
  - Implementation: Load as list, save as list
  - Verified: {Check after implementing}

---

## Edge Case Requirements (spec.md section 7)

- [x] **EDGE-1:** Handle missing week folders (< 18 weeks)
  - Spec Location: spec.md lines 193-196
  - TODO Task: Task 2
  - Implementation: Log WARNING if < 18 weeks found (utils/adp_updater.py:215-216)
  - Verified: 2026-01-01 00:50 ✅ Logs warning, continues with available weeks

- [x] **EDGE-2:** Handle malformed JSON in any file
  - Spec Location: spec.md lines 197-201
  - TODO Task: Task 4
  - Implementation: Try/except JSONDecodeError, FAIL entire operation (utils/adp_updater.py:255-258)
  - Verified: 2026-01-01 00:58 ✅ Raises ValueError with clear message

- [x] **EDGE-3:** Verify direct JSON array structure
  - Spec Location: spec.md lines 202-206
  - TODO Task: Task 4
  - Implementation: isinstance check, raise ValueError if wrapper dict (utils/adp_updater.py:249-254)
  - Verified: 2026-01-01 00:58 ✅ Validates structure is list

- [x] **EDGE-4:** Handle permission errors during atomic write
  - Spec Location: spec.md lines 207-211
  - TODO Task: Task 7
  - Implementation: Try/except PermissionError, cleanup temp file (utils/adp_updater.py:313-318)
  - Verified: 2026-01-01 00:58 ✅ Raises PermissionError, cleans up .tmp

---

## Testing Requirements (spec.md section 3)

- [x] **TEST-1:** Update unit tests for multi-week folder structure
  - Spec Location: spec.md lines 110-120
  - TODO Task: Task 10
  - Implementation: Updated test_sim_data_folder fixture (tests/utils/test_adp_updater.py:134-170)
  - Verified: 2026-01-01 01:05 ✅ Creates 3 weeks with direct arrays

- [x] **TEST-2:** Update unit tests for direct array JSON structure
  - Spec Location: spec.md lines 121-128
  - TODO Task: Task 11
  - Implementation: Removed wrapper dicts from fixture, updated all test assertions
  - Verified: 2026-01-01 01:05 ✅ All tests use direct array loading

- [x] **TEST-3:** Add test for all weeks being updated
  - Spec Location: spec.md lines 129-135
  - TODO Task: Task 12
  - Implementation: test_updates_all_week_folders() (tests/utils/test_adp_updater.py:267-287)
  - Verified: 2026-01-01 01:05 ✅ New test verifies all weeks processed

- [x] **TEST-4:** Add test for consistent updates across weeks
  - Spec Location: spec.md lines 136-143
  - TODO Task: Task 13
  - Implementation: test_consistent_updates_across_weeks() (tests/utils/test_adp_updater.py:289-308)
  - Verified: 2026-01-01 01:05 ✅ New test verifies data consistency

- [x] **TEST-5:** Update epic E2E test validation
  - Spec Location: spec.md lines 144-151
  - TODO Task: Task 14
  - Implementation: Updated epic_e2e_test.py paths and validation (lines 74, 154-155, 178-181, 206-225, 283, 300-328)
  - Verified: 2026-01-01 01:12 ✅ All paths use simulation/sim_data/2025/weeks/, direct arrays validated

- [x] **TEST-6:** Update user test script verification
  - Spec Location: spec.md lines 152-161
  - TODO Task: Task 15
  - Implementation: Updated test_full_csv.py paths (lines 26, 43-50, 106-150)
  - Verified: 2026-01-01 01:07 ✅ Steps 2, 4, 5 use simulation/sim_data/2025/weeks/

---

## Documentation Requirements (spec.md section 4)

- [x] **DOC-1:** Update function docstring for multi-week processing
  - Spec Location: spec.md lines 186-187
  - TODO Task: Task 16
  - Implementation: Enhanced docstring with 3 sections (utils/adp_updater.py:150-204)
  - Verified: 2026-01-01 01:16 ✅ MULTI-WEEK, DATA STRUCTURE, ATOMIC WRITES sections added

- [x] **DOC-2:** Update code comments for multi-week logic
  - Spec Location: spec.md lines 186-187
  - TODO Task: Task 17
  - Implementation: Enhanced inline comments at key locations (lines 220-342)
  - Verified: 2026-01-01 01:17 ✅ All critical sections commented

---

## Acceptance Criteria (spec.md section 9)

- [ ] **ACCEPT-1:** All 18 week folders processed
  - Spec Location: spec.md line 216
  - Verification: Check logs show 18 weeks
  - Verified: {Check after user testing}

- [ ] **ACCEPT-2:** All 108 files updated (18 weeks × 6 positions)
  - Spec Location: spec.md line 217
  - Verification: File count in logs
  - Verified: {Check after user testing}

- [ ] **ACCEPT-3:** ADP values match FantasyPros CSV data
  - Spec Location: spec.md line 218
  - Verification: Sample verification in user test
  - Verified: {Check after user testing}

- [ ] **ACCEPT-4:** Direct JSON array structure preserved
  - Spec Location: spec.md line 219
  - Verification: Manual inspection of JSON files
  - Verified: {Check after user testing}

- [ ] **ACCEPT-5:** Atomic writes used for all 108 files
  - Spec Location: spec.md line 220
  - Verification: Code review (tmp file pattern)
  - Verified: {Check after implementation}

- [ ] **ACCEPT-6:** Match report aggregates across all weeks
  - Spec Location: spec.md line 221
  - Verification: Match report structure
  - Verified: {Check after implementation}

- [ ] **ACCEPT-7:** Unmatched players retain default ADP 170.0
  - Spec Location: spec.md line 222
  - Verification: Check unmatched players in report
  - Verified: {Check after user testing}

- [ ] **ACCEPT-8:** Unit tests pass (100%)
  - Spec Location: spec.md line 223
  - Verification: Run test suite
  - Verified: {Check after all tests updated}

- [ ] **ACCEPT-9:** Epic E2E test validates all weeks
  - Spec Location: spec.md line 224
  - Verification: Run epic E2E test
  - Verified: {Check after Task 14}

- [ ] **ACCEPT-10:** User test script verifies correct folders
  - Spec Location: spec.md line 225
  - Verification: Run test_full_csv.py
  - Verified: {Check after Task 15}

---

## Summary

**Total Requirements:** 37
- Core Implementation: 9
- Data Structure: 4
- Edge Cases: 4
- Testing: 6
- Documentation: 2
- Acceptance Criteria: 10
- Additional (from spec): 2

**Implemented:** 21/37 (57%) - ALL 5 PHASES COMPLETE
**Remaining:** 16/37 (43%) - Acceptance criteria to verify during testing

**PHASE 1 Completed (5 items):**
- REQ-1: Function signature ✅
- REQ-2: Week folder discovery ✅
- REQ-3: Week iteration ✅
- REQ-9: Per-week logging ✅
- EDGE-1: Missing weeks handling ✅

**PHASE 2 Completed (7 items):**
- REQ-4: Load JSON as direct array ✅
- REQ-5: Match players per week ✅
- REQ-6: Update ADP values ✅
- REQ-7: Write as direct array ✅
- EDGE-2: Malformed JSON handling ✅
- EDGE-3: Structure validation ✅
- EDGE-4: Permission error handling ✅

**PHASE 3 Completed (1 item):**
- REQ-8: Aggregate match report ✅

**PHASE 4 Completed (6 items):**
- TEST-1: Multi-week test fixtures ✅
- TEST-2: Direct array test fixtures ✅
- TEST-3: test_updates_all_week_folders() ✅
- TEST-4: test_consistent_updates_across_weeks() ✅
- TEST-5: Epic E2E test update ✅
- TEST-6: User test script updated ✅

**PHASE 5 Completed (2 items):**
- DOC-1: Function docstring ✅
- DOC-2: Code comments ✅

**Last Updated:** 2026-01-01 01:18
