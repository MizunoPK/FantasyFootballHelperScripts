# Feature 01: CSV Data Loading - Planning Checklist

**Status:** Phase 3 complete (Interactive Questions) - All decisions confirmed

**Purpose:** Track open questions and decisions needed for this feature

---

## Technical Decisions (User Input Required)

### Decision 1: CSV File Path Configuration ✅
**Question:** Should the CSV file path be hardcoded or passed as a parameter?

**Options:**
- [ ] A. Hardcoded: `feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv`
- [x] B. Passed as function parameter (more flexible, better for testing)
- [ ] C. Read from config file

**Context:**
- Hardcoded is simpler but less flexible
- Parameter makes testing easier (can pass tmp_path in tests)
- Config file adds complexity for one-time use

**Agent Recommendation:** Option B (parameter) - better testability and flexibility

**User Decision:** ✅ Option B (Parameter) - Confirmed 2025-12-31

---

### Decision 2: Position Suffix Handling ✅
**Question:** Should position tier suffixes (WR1, RB2, QB12) be stripped in this feature or Feature 2?

**Options:**
- [x] A. Strip here - return clean positions (WR, RB, QB)
- [ ] B. Keep raw values - let Feature 2 handle cleaning
- [ ] C. Return both raw and clean positions

**Context:**
- CSV has: "WR1", "RB2", "TE1", "QB12"
- Need: "WR", "RB", "TE", "QB"
- Stripping here creates cleaner interface for Feature 2

**Agent Recommendation:** Option A (strip here) - cleaner separation of concerns

**User Decision:** ✅ Option A (Strip here) - Confirmed 2025-12-31

---

### Decision 3: Output Data Structure ✅
**Question:** What data structure should be returned for Feature 2 to consume?

**Options:**
- [x] A. pandas DataFrame with columns: player_name, adp, position
- [ ] B. Dictionary: `{player_name: {"adp": float, "position": str}}`
- [ ] C. List of tuples: `[(player_name, adp, position), ...]`
- [ ] D. Custom dataclass/NamedTuple

**Context:**
- Already using pandas for CSV reading
- Feature 2 will iterate through players for matching
- 988 rows total (performance not a concern)

**Agent Recommendation:** Option A (DataFrame) - already using pandas, standard format

**User Decision:** ✅ Option A (DataFrame) - Confirmed 2025-12-31

---

### Decision 4: Empty Team Field Handling ✅
**Question:** How should empty Team fields be handled in the CSV?

**Options:**
- [ ] A. Skip rows with empty Team (might lose valid player data)
- [ ] B. Use None or "" for Team field
- [x] C. Don't include Team in output at all (recommended)

**Context:**
- Research found some CSV rows have empty Team values
- Team field is unreliable and not needed for player matching
- Feature 2 uses fuzzy matching on name only

**Agent Recommendation:** Option C (exclude Team) - unreliable field, not needed

**User Decision:** ✅ Option C (Exclude Team) - Confirmed 2025-12-31

---

### Decision 5: ADP Value Validation ✅
**Question:** Should we validate that all ADP values are positive floats?

**Options:**
- [x] A. Yes - raise ValueError if ADP <= 0 or invalid
- [ ] B. No - accept any float value
- [ ] C. Yes - but log warning and skip row instead of raising

**Context:**
- All current ADP values are positive (1.0 to 988.0 range)
- Invalid ADP would indicate data corruption
- Fail fast prevents bad data propagating to Feature 2

**Agent Recommendation:** Option A (validate and raise) - fail fast on bad data

**User Decision:** ✅ Option A (Validate and raise) - Confirmed 2025-12-31

---

### Decision 6: Duplicate Player Name Handling ✅
**Question:** What should happen if the CSV has duplicate player names?

**Options:**
- [ ] A. Keep first occurrence, skip duplicates
- [ ] B. Raise ValueError on duplicates
- [x] C. Keep all, let Feature 2 handle duplicates

**Context:**
- Unlikely scenario but possible (e.g., two "Mike Williams" on different teams)
- Current CSV has no duplicates (verified)
- Feature 2 fuzzy matching might need all candidates

**Agent Recommendation:** Option C (keep all) - Feature 2 can use Team as tiebreaker

**User Decision:** ✅ Option C (Keep all) - Confirmed 2025-12-31

---

## Implementation Clarifications (No User Input Needed)

### Confirmed Decisions from Research

- [x] **CSV Encoding:** UTF-8 (standard, handles special characters)
- [x] **Existing Utilities:** Leverage `utils/csv_utils.py` functions
- [x] **Required Columns:** Player, POS, AVG (validated before processing)
- [x] **Error Handling:** Fail fast on missing file or invalid data
- [x] **Module Location:** `utils/adp_csv_loader.py` (follows existing patterns)
- [x] **Test Location:** `tests/utils/test_adp_csv_loader.py` (mirrors source structure)
- [x] **Logging:** Use `utils.LoggingManager.get_logger()`
- [x] **Type Hints:** All public functions fully typed

### Edge Cases Confirmed

- [x] Empty Team fields → Handled by not including Team in output
- [x] Trailing spaces in Bye column → Ignored (not using Bye)
- [x] Position tier suffixes → Stripped (pending Decision 2 confirmation)
- [x] Decimal ADP values → Parsed as float
- [x] Player name punctuation → Passed through as-is (Feature 2 handles)

---

## Scope Verification (Phase 4: Dynamic Scope Adjustment)

**Initial estimate:** 15-20 items

**Final verified count:** 14 items
- 6 technical decisions (all confirmed)
- 8 confirmed implementation items

**Scope growth during deep dive:** None (remained stable at ~14 items)

**Status:** ✅ Within Small feature threshold (<35 items)

**Decision:** No scope split needed - feature is appropriately sized

**Phase 4 Complete:** 2025-12-31

---

## Stage 2 Completion Summary

**Phase 1 (Targeted Research):** ✅ Complete
- Research discovery document created
- CSV structure analyzed
- Existing utilities identified
- Edge cases documented

**Phase 2 (Update Spec & Checklist):** ✅ Complete
- spec.md fleshed out with detailed requirements
- checklist.md populated with all decisions

**Phase 3 (Interactive Questions):** ✅ Complete
- All 6 technical decisions confirmed with user
- spec.md and checklist.md updated with decisions

**Phase 4 (Dynamic Scope Adjustment):** ✅ Complete
- Scope verified: 14 items (within Small threshold)
- No split needed

**Phase 5 (Cross-Feature Alignment):** N/A
- This is Feature 1 (first feature in epic)
- No other completed features to compare against

---

**Stage 2 Status:** ✅ COMPLETE
**Date Completed:** 2025-12-31
**Next Stage:** Stage 3 (Cross-Feature Sanity Check) - after Feature 2 completes Stage 2
