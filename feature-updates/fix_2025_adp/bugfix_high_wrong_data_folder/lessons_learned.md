# Bug Fix: Wrong Data Folder - Lessons Learned

**Created:** 2026-01-01 18:52
**Bug Priority:** HIGH
**Status:** Implementation Complete (w/ DST fix)

---

## Critical Lessons

### 1. QC Round 3 Caught Critical Bug Missed in Earlier Rounds

**What Happened:**
- QC Rounds 1 and 2 validated that code exists and tests pass
- QC Round 3 (fresh-eyes review) caught that DST files weren't being updated
- Only 90/108 files were modified (5 positions × 18 weeks instead of 6 positions × 18 weeks)

**Root Cause:**
- CSV format: "Baltimore Ravens" (city + team name)
- JSON format: "Ravens D/ST" (team name + D/ST suffix)
- Fuzzy matching failed due to format mismatch
- Similarity score too low (< 0.75 threshold)

**Why Earlier Rounds Missed It:**
- Rounds 1-2 verified "code exists" and "tests pass"
- Did NOT verify actual data output for ALL positions
- DST position edge case not tested in manual verification

**Fix:**
- Added `extract_dst_team_name()` to extract team names from both formats
- Added DST special handling in `find_best_match()` for exact team name matching
- +7 tests to cover DST matching (extraction + matching logic)

**Lesson:**
- **QC Round 3 is MANDATORY** - Fresh eyes catch missed edge cases
- **Verify actual output data** - Not just file structure
- **Test ALL positions** - Don't assume similar code paths work the same

---

### 2. Spec Validation Requires Data-Level Verification

**What Happened:**
- Spec required "6 position files per week" (spec.md line 18)
- Implementation processed all 6 position types in POSITION_FILES dict
- Tests verified "all positions processed"
- BUT actual data showed only 5 positions getting updates

**Why Tests Passed But Bug Existed:**
- Tests verified code ITERATED through all 6 positions
- Tests did NOT verify all 6 positions GOT MATCHES
- DST matching silently failed - no errors, just no matches

**Lesson:**
- **Verify output data VALUES, not just structure**
- "File processed" ≠ "File updated with correct data"
- Check actual data samples during QC, not just counts

**Guide Update Needed:**
- QC Round 1 checklist: Add "Verify sample data for ALL categories/types"
- Smoke Testing: Add "Check data values for edge case categories"

---

### 3. Position-Specific Logic Needs Position-Specific Tests

**What Happened:**
- Code handled 6 positions: QB, RB, WR, TE, K, DST
- Tests covered QB, RB, WR (main positions)
- DST position has different name format - not tested

**Why:**
- Assumed fuzzy matching works the same for all positions
- DST has unique name format ("Team D/ST") not present in other positions
- Edge case not obvious during test design

**Fix:**
- Added DST-specific tests (format extraction + matching logic)
- Verified all team name formats (JSON vs CSV)

**Lesson:**
- **Each position type needs explicit test coverage**
- **Don't assume code paths are equivalent** - data format matters
- DST/K are often edge cases (different name formats)

**Guide Update Needed:**
- Stage 5a Iteration 15 (Test Coverage): Explicitly check position-specific tests
- Add requirement: "Verify edge case positions (DST, K) have dedicated tests"

---

### 4. Multi-File Operations Need Per-Category Verification

**What Happened:**
- Bug fix processes 108 files (18 weeks × 6 positions)
- Logs showed "108 files processed" but actually only 90 updated
- Missing 18 DST files (1 per week)

**Why:**
- Logs showed aggregate count - masked the missing position
- No per-position file count verification
- Assumed "all files processed" = "all files updated"

**Lesson:**
- **Multi-file operations: Verify per-category, not just total**
- Log per-position counts: "QB: 18 files, RB: 18 files, ..., DST: 0 files"
- Would have caught the issue immediately

**Code Improvement:**
- Could add per-position logging in update_player_adp_values()
- E.g., "Matched QB: 90 across 18 weeks, DST: 0 across 18 weeks"

---

### 5. Name Format Differences Are Common Edge Cases

**What Happened:**
- DST name format difference (JSON vs CSV) caused matching failure
- Similar issue could occur with other positions (e.g., "D/ST" vs "DEF")

**Common Name Format Issues:**
- Suffixes: "Jr.", "Sr.", "III", "II" (handled by normalize_name)
- Prefixes: "D/ST", "DEF" (DST-specific)
- City vs Team: "San Francisco 49ers" vs "49ers D/ST"
- Hyphenation: "Amon-Ra" vs "Amon Ra"

**Lesson:**
- **Document name format differences in spec**
- **Add name format section to deep dive (Stage 2)**
- Test with actual data samples from both sources

**Guide Update Needed:**
- Stage 2 checklist: Add "Document name format differences between data sources"
- Stage 5a Iteration 6 (Data Structure Validation): Add "Verify name formats match"

---

### 6. QC Restart Protocol Justification

**What Happened:**
- Critical bug found in QC Round 3
- Followed QC Restart Protocol: Fix bug → Restart from Smoke Testing
- Might seem excessive, but necessary

**Why Restart:**
- DST fix changed matching logic (new function + special handling)
- Could have introduced new bugs in other positions
- Smoke tests verify END-TO-END behavior with new code

**Lesson:**
- **QC Restart Protocol exists for good reason**
- Don't skip ahead after fixes - regressions can occur
- Fresh smoke test + QC rounds verify fix didn't break anything

---

## Process Improvements

### For Future Bug Fixes:

1. **During Spec Writing (Stage 2):**
   - Document ALL position types explicitly
   - Note name format differences between data sources
   - Include DST/K as explicit examples (not just QB/RB/WR)

2. **During TODO Creation (Stage 5a):**
   - Iteration 6: Add data format validation for all positions
   - Iteration 15: Require tests for each position type
   - Iteration 23a Part 2: Verify tests cover all categories

3. **During Implementation (Stage 5b):**
   - Log per-position counts (not just totals)
   - Test with actual data samples early
   - Verify edge case positions work (DST, K, etc.)

4. **During Smoke Testing (Stage 5ca):**
   - Part 3: Verify data values for ALL position types
   - Don't just check "file exists" - check "file has updates"
   - Sample check: Pick one position of each type

5. **During QC Rounds (Stage 5cb):**
   - Round 1: Verify per-category output (not just totals)
   - Round 2: Deep dive into edge case categories
   - Round 3: Fresh-eyes review of ALL categories

---

## Guide Updates Needed

### STAGE_5aa_round1_guide.md

**Iteration 6: Data Structure Validation**
- Add: "Verify name formats between data sources match or have handling"
- Add: "Document format differences in spec if found"

### STAGE_5ab_round2_guide.md

**Iteration 15: Test Coverage Depth Check**
- Add: "Verify tests cover ALL categories/types (e.g., all positions)"
- Add: "Edge case categories (DST, K) need dedicated tests"

### STAGE_5ac_round3_guide.md

**Iteration 23a Part 2: Test Coverage Audit**
- Add: "Verify position-specific tests exist for each position type"

### STAGE_5ca_smoke_testing_guide.md

**Part 3: E2E Execution Test**
- Add: "Verify data values for EACH category/type"
- Add: "Sample one item from each category - check actual data"

### STAGE_5cb_qc_rounds_guide.md

**QC Round 1: Section 3 - Output File Validation**
- Add: "Per-category verification (not just totals)"
- Example: "QB files: X updated, RB files: Y updated, ..., DST files: Z updated"

**QC Round 3: Section 1 - Re-read Spec**
- Add: "Verify EACH item in lists (e.g., all 6 positions if spec says 6)"

---

## Summary

**Bug Found:** DST files not being updated (18 missing files out of 108 total)

**Root Cause:** Name format mismatch between CSV ("Baltimore Ravens") and JSON ("Ravens D/ST")

**Detection:** QC Round 3 fresh-eyes review

**Fix:** Added DST-specific matching logic with team name extraction

**Key Takeaway:** QC Round 3 is CRITICAL - caught a bug that Rounds 1-2 missed

**Process Improvement:** Always verify per-category data, not just totals

**Guide Updates:** 6 guide enhancements to prevent similar issues

---

**Impact on Workflow:**
- QC Round 3 validated as essential (not optional)
- Data-level verification now emphasized in all QC rounds
- Position-specific tests now required in test coverage audits
