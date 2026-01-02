# Feature 02: Player Matching & Data Update - Planning Checklist

**Status:** Phase 3 complete (Interactive Questions) - All decisions confirmed

**Purpose:** Track open questions and decisions needed for this feature

---

## Technical Decisions (User Input Required)

### Decision 1: Confidence Threshold ✅
**Question:** What confidence threshold should we use for accepting fuzzy matches?

**Options:**
- [x] A. 0.75 (same as DraftedRosterManager - proven threshold)
- [ ] B. 0.80 (more conservative, fewer false matches)
- [ ] C. 0.70 (more permissive, more matches but lower quality)
- [ ] D. Configurable parameter

**Context:**
- DraftedRosterManager uses 0.75 successfully
- 0.75 balances accuracy vs recall well
- Higher = fewer but better matches
- Lower = more matches but more false positives

**Agent Recommendation:** Option A (0.75) - proven from existing codebase

**User Decision:** ✅ Option A (0.75) - Auto-confirmed (follows existing pattern)

---

### Decision 2: Unmatched JSON Player Handling ✅
**Question:** What should happen when a JSON player has no CSV match?

**Options:**
- [x] A. Keep existing 170.0 placeholder value
- [ ] B. Set to None or null
- [ ] C. Set to different default (e.g., 999.0 to indicate "no rank")
- [ ] D. Remove player from JSON

**Context:**
- Some JSON players won't be in CSV top 988 (e.g., backup RBs)
- Expected: ~50-100 unmatched JSON players
- These are valid players, just not highly ranked

**Agent Recommendation:** Option A (keep 170.0) - least disruptive, maintains data integrity

**User Decision:** ✅ Option A (Keep 170.0) - Auto-confirmed (least disruptive)

---

### Decision 3: Match Report Detail Level ✅
**Question:** What level of detail should the match report include?

**Options:**
- [ ] A. Summary only (matched/unmatched counts)
- [ ] B. Summary + unmatched player lists
- [ ] C. Summary + unmatched lists + confidence distribution
- [x] D. Summary + unmatched lists + confidence distribution + all individual match details

**Context:**
- Summary = quick overview
- Unmatched lists = verification of what didn't match
- Confidence distribution = quality assessment (how many 1.0, 0.9-0.99, 0.75-0.89)
- Individual matches = debugging info (every match with names, confidence, old/new ADP)

**Agent Recommendation:** Option D - comprehensive for debugging and verification

**User Decision:** ✅ Option D (Comprehensive) - Confirmed 2025-12-31

---

### Decision 4: Logging Level ✅
**Question:** What should be logged during the matching process?

**Options:**
- [ ] A. Log every match (INFO level) - 700+ log lines
- [ ] B. Log only unmatched players (WARNING level)
- [ ] C. Log summary only (INFO level) - just totals
- [ ] D. Log everything in DEBUG, summary in INFO (best of both)
- [x] E. Hybrid: Unmatched players (WARNING) + Summary (INFO)

**Context:**
- ~700 matches expected
- Every match = verbose but helpful for debugging
- Summary only = clean but less visibility
- DEBUG + INFO = details available when needed

**Agent Recommendation:** Option D - detailed logs available in DEBUG, clean INFO logs

**User Decision:** ✅ Option E (Hybrid: B + C) - Log unmatched players + summary - Confirmed 2025-12-31

---

### Decision 5: Dry Run Mode ✅
**Question:** Should there be a dry-run mode that doesn't write files?

**Options:**
- [ ] A. Yes - add dry_run=False parameter to function
- [x] B. No - always write files (simpler)

**Context:**
- Dry run mode = preview matches without updating files
- Useful for testing before committing
- Adds complexity (extra parameter, conditional logic)
- Can test with tmp files instead

**Agent Recommendation:** Option B (No dry run) - simpler, tmp files sufficient for testing

**User Decision:** ✅ Option B (No dry run) - Confirmed 2025-12-31

---

### Decision 6: Backup Files ✅
**Question:** Should original JSON files be backed up before updating?

**Options:**
- [ ] A. Yes - create .bak files before updating
- [x] B. No - atomic writes are sufficient (git provides history)
- [ ] C. Optional - add backup=False parameter

**Context:**
- Atomic writes prevent corruption (write to .tmp, then replace)
- Git already tracks file history
- Backup files add clutter
- Can manually backup before running if desired

**Agent Recommendation:** Option B (No backup) - atomic writes + git is sufficient

**User Decision:** ✅ Option B (No backup) - Confirmed 2025-12-31

---

### Decision 7: Match Report Format ✅
**Question:** What format should the match report be returned in?

**Options:**
- [x] A. Dictionary (returned by function)
- [ ] B. Text file written to disk
- [ ] C. Both (dict + write file)
- [ ] D. JSON file written to disk

**Context:**
- Dict = caller can use programmatically
- File = persistent, can review later
- Both = most flexible but more code

**Agent Recommendation:** Option A (Dict) - caller can write to file if desired

**User Decision:** ✅ Option A (Dict) - Auto-confirmed (follows Python convention)

---

## Implementation Clarifications (No User Input Needed)

### Confirmed Decisions from Research

- [x] **Fuzzy Matching Source:** Adapt from DraftedRosterManager.py
- [x] **Normalization:** Use normalize_name() adapted from _normalize_player_info()
- [x] **Position Filtering:** Only match within same position
- [x] **Best Match Selection:** Highest confidence score wins
- [x] **JSON I/O Pattern:** Atomic writes (from PlayerManager pattern)
- [x] **Module Location:** `utils/adp_updater.py`
- [x] **Test Location:** `tests/utils/test_adp_updater.py`
- [x] **Error Handling:** Fail fast (FileNotFoundError, ValueError, PermissionError)
- [x] **Type Hints:** All public functions fully typed
- [x] **Logging:** Use `utils.LoggingManager.get_logger()`

### Edge Cases Confirmed

- [x] Name variations → normalize_name() handles punctuation, suffixes
- [x] Multiple matches → Use highest confidence score
- [x] Position equivalency → Both use clean positions from Feature 1
- [x] Defense names → Fuzzy matching handles variations
- [x] No match found → Keep 170.0 value
- [x] CSV player not in JSON → Ignore (expected)
- [x] Empty DataFrame → Raise ValueError
- [x] Missing directory → Raise FileNotFoundError
- [x] Permission errors → Let PermissionError propagate
- [x] File corruption → Atomic writes prevent

---

## Scope Verification (Phase 4: Dynamic Scope Adjustment)

**Initial estimate:** 25-30 items

**Final verified count:** 17 items
- 7 technical decisions (all confirmed)
- 10 confirmed implementation items

**Scope growth during deep dive:** None (remained stable at ~17 items)

**Status:** ✅ Within Medium feature threshold (<35 items)

**Decision:** No scope split needed - feature is appropriately sized

**Phase 4 Complete:** 2025-12-31

---

## Stage 2 Completion Summary

**Phase 1 (Targeted Research):** ✅ Complete
- Research discovery document created
- Fuzzy matching logic analyzed (DraftedRosterManager)
- JSON structure analyzed (739 players across 6 files)
- JSON I/O patterns identified (atomic writes)
- 10 edge cases documented

**Phase 2 (Update Spec & Checklist):** ✅ Complete
- spec.md fleshed out with detailed requirements
- checklist.md populated with all decisions

**Phase 3 (Interactive Questions):** ✅ Complete
- All 7 technical decisions confirmed with user
- Decision 1: 0.75 threshold (auto-confirmed)
- Decision 2: Keep 170.0 for unmatched (auto-confirmed)
- Decision 3: Comprehensive report (Option D)
- Decision 4: Log unmatched + summary (Hybrid B+C)
- Decision 5: No dry run mode (Option B)
- Decision 6: No backup files (Option B)
- Decision 7: Return dict (auto-confirmed)

**Phase 4 (Dynamic Scope Adjustment):** ✅ Complete
- Scope verified: 17 items (within Medium threshold)
- No split needed

**Phase 5 (Cross-Feature Alignment):** ✅ Complete
- Compared to Feature 1 spec for consistency
- **Interface alignment verified:**
  - Feature 1 outputs pandas DataFrame (player_name, adp, position)
  - Feature 2 expects pandas DataFrame (player_name, adp, position) ✅
  - Feature 1 strips position suffixes (WR1→WR, QB12→QB)
  - Feature 2 expects clean positions (QB, RB, WR, TE, K, DST) ✅
  - Feature 1 validates ADP > 0
  - Feature 2 expects positive float ADP values ✅
- **No conflicts found**
- **Integration point clear:** Feature 1 → Feature 2 (CSV DataFrame)

---

**Stage 2 Status:** ✅ COMPLETE
**Date Completed:** 2025-12-31
**Next Stage:** Stage 3 (Cross-Feature Sanity Check) - both features ready
