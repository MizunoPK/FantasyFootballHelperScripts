# D10: Stage 2 Fix Planning (Session 4) - Final 3 Files

**Session Date:** 2026-02-05
**Files Analyzed:** Files 9-11 (largest files: s3, s8, glossary)
**Session Time:** 2 hours analysis

---

## Executive Summary

**Status:** Session 4 complete - ALL 11 CRITICAL files analyzed (100%)

**Key Finding:** Final 3 files are the LARGEST in the guides system and require most aggressive reduction strategies:
- glossary.md = LARGEST overall file (1447 lines)
- s3_cross_feature_sanity_check.md = LARGEST workflow guide (1355 lines)
- s8_p2_epic_testing_update.md = second-largest stage guide (1345 lines)

**Reduction Strategies:** Mix of extraction and condensing across all 3 files
**Estimated Total Reduction:** ~775 lines across 3 files
**Total Execution Effort:** 10-13 hours (most complex reductions)

---

## FILE 9: stages/s3/s3_cross_feature_sanity_check.md

**Current Size:** 1355 lines (❌ CRITICAL - 355 over threshold)

**Analysis:**

**File Purpose:** Guide for systematic cross-feature comparison (S3 stage)

**Structure:**
- Overview + Critical Rules (lines 1-94)
- Prerequisites (lines 95-116)
- **Parallel Work Sync Verification (lines 117-326):** 210 lines ⚠️ EXTRACTION TARGET
- Workflow Overview (lines 327-374)
- Step 1: Comparison Matrix (lines 377-473)
- **Step 2: Systematic Comparison (lines 475-703):** 229 lines ⚠️ CONDENSING TARGET
- Step 3: Conflict Resolution (lines 705-843)
- Step 4-6: Plan + Sign-Off + Complete (lines 845-1140)
- Common Mistakes (lines 1175-1206): 32 lines (reasonable)
- Real-World Example (lines 1209-1256): 48 lines (reasonable)
- README updates + Next Stage (lines 1257-1354)

**Verbosity Analysis:**

### Target 1: Parallel Work Sync Verification (Lines 117-326)
**Current:** 210 lines of detailed parallel work coordination steps

**Content:**
- Step 0.1: Check Completion Messages (25 lines)
- Step 0.2: Verify STATUS Files (23 lines)
- Step 0.3: Verify Checkpoints (28 lines)
- Step 0.4: Verify Feature Specs Complete (25 lines)
- Step 0.5: Document Sync Verification (53 lines with full template)
- Step 0.6: Notify Secondary Agents (30 lines)

**Issue:** Parallel work is OPTIONAL feature (most epics are sequential)
- Only applies IF user chose parallel work in S1
- 210 lines of content most agents will skip
- Already documented in `parallel_work/` folder

**Reduction Strategy:** Extract to `reference/parallel_work/s3_sync_verification.md`
- Move entire Steps 0.1-0.6 to separate file
- Replace with brief section:
  ```markdown
  ## Parallel Work Sync Verification (If Applicable)

  **Skip this section if:** S2 was done sequentially (single agent)

  **If S2 was done in parallel mode (Primary + Secondaries):**

  You MUST verify all secondary agents completed S2 before starting S3 comparison.

  **Complete verification protocol:** See `reference/parallel_work/s3_sync_verification.md`

  **6-step verification includes:**
  1. Check completion messages from all secondaries
  2. Verify STATUS files (COMPLETE + READY_FOR_SYNC)
  3. Check agent checkpoints (not stale)
  4. Verify feature specs complete
  5. Document sync verification
  6. Notify secondary agents S3 starting

  **After verification passes:** Proceed to Step 1 (Prepare Comparison Matrix)
  ```
- Savings: 210 → 20 lines (190 lines saved)

---

### Target 2: Step 2 Systematic Comparison (Lines 475-703)
**Current:** 229 lines of detailed comparison examples

**Content:**
- Step 2.1: Compare Data Structures (33 lines with examples)
- Step 2.2: Compare Interfaces & Dependencies (55 lines with conflict example)
- Step 2.3: Compare File Locations (39 lines with conflict example)
- Step 2.4: Compare Configuration Keys (33 lines)
- Step 2.5: Compare Algorithms (28 lines)
- Step 2.6: Document All Conflicts (41 lines with summary template)

**Issue:** Extremely verbose examples for each comparison category
- Each category has full feature data examples
- Conflict examples are very detailed (40-50 lines each)
- Pattern is established - don't need full example for EVERY category

**Reduction Strategy:** Condense to essential guidance + brief examples
- Keep Step 2.1 with full example (establishes pattern)
- Condense Steps 2.2-2.5 (remove verbose examples)
- Keep Step 2.6 summary template
- Pattern:
  - What to extract from each feature
  - How to compare
  - What conflicts to look for
  - ONE brief example only

**Projected Condensing:**
- Step 2.1: Keep full (33 lines) - establishes pattern
- Step 2.2: 55 → 25 lines (30 saved) - remove verbose conflict example
- Step 2.3: 39 → 20 lines (19 saved) - condense conflict example
- Step 2.4: 33 → 15 lines (18 saved) - brief guidance only
- Step 2.5: 28 → 15 lines (13 saved) - brief guidance only
- Step 2.6: Keep (41 lines) - summary template needed
- **Total:** 229 → 149 lines (80 lines saved)

---

**Reduction Strategy Summary:**

**Strategy A: Extract Parallel Work Sync**
- Move lines 117-326 (210 lines) to `reference/parallel_work/s3_sync_verification.md`
- Replace with brief 20-line overview + reference
- Savings: 190 lines

**Strategy B: Condense Step 2 Examples**
- Condense Step 2.2-2.5 comparison examples
- Keep essential guidance, remove verbose examples
- Savings: 80 lines

**Total Reduction:** 270 lines

**Projected Outcome:** 1355 → 1085 lines (still 85 over threshold)

**Additional Optional Condensing:**
- Step 3 Conflict Resolution (lines 705-843): 139 lines
  - Could condense resolution examples to 100 lines (39 saved)
  - Would bring to ~1046 lines (46 over threshold)
- Step 5 User Sign-Off (lines 967-1084): 118 lines
  - Could condense presentation template to 80 lines (38 saved)
  - Would bring to ~1008 lines (8 over threshold)

**Recommended Strategy:** Extract + Condense + Additional Condensing
- Extract Parallel Work: 190 lines
- Condense Step 2: 80 lines
- Condense Step 3: 39 lines
- Condense Step 5: 38 lines
- **Total: 347 lines saved → Target: 1008 lines (just over threshold)**

**Final Polish:** Minor condensing in remaining sections to get under 1000

**Effort:** 4-5 hours (extraction + multiple condensing passes + cross-reference updates)

---

## FILE 10: stages/s8/s8_p2_epic_testing_update.md

**Current Size:** 1345 lines (❌ CRITICAL - 345 over threshold)

**Analysis:**

**File Purpose:** Guide for updating epic test plan after each feature completes

**Structure:**
- Overview + Critical Rules (lines 1-129)
- Critical Decisions Summary (lines 131-191): 61 lines (reasonable)
- Prerequisites + Workflow Overview (lines 193-253)
- Quick Navigation (lines 255-284): 30 lines (reasonable)
- **Detailed Workflow (lines 286-742):** 457 lines ⚠️ CONDENSING TARGET
  - STEP 1: Review Implementation (lines 288-401): 114 lines
  - STEP 2: Identify Gaps (lines 403-472): 70 lines
  - STEP 3: Update Plan (lines 474-674): 201 lines
  - STEP 4: Final Verification (lines 676-742): 67 lines
- Mandatory Checkpoint (lines 744-768)
- Commit Template (lines 770-795)
- Exit Criteria (lines 797-838)
- **Common Mistakes (lines 840-970):** 131 lines ⚠️ CONDENSING TARGET
- **Real-World Examples (lines 986-1249):** 264 lines ⚠️ EXTRACTION TARGET
- README Updates (lines 1251-1284)
- Prerequisites Next Stage (lines 1285-1315)
- Summary (lines 1316-1345)

**Verbosity Analysis:**

### Target 1: Common Mistakes Section (Lines 840-970)
**Current:** 131 lines covering 10 anti-patterns

**Content:**
- Anti-Pattern 1: Updating Based on Specs (14 lines)
- Anti-Pattern 2: Vague Test Scenarios (17 lines)
- Anti-Pattern 3: Skipping If "No Obvious Changes" (13 lines)
- Anti-Pattern 4: Duplicate Unit Tests (13 lines)
- Anti-Pattern 5: Not Updating Existing Scenarios (12 lines)
- Anti-Pattern 6: Missing Update Rationale (18 lines)
- Anti-Pattern 7: Forgetting to Commit (12 lines)
- Anti-Pattern 8: Deleting S1/4 Content (12 lines)
- Anti-Pattern 9: Not Reading Actual Code (11 lines)
- Anti-Pattern 10: Unclear Update History (9 lines)

**Issue:** Each anti-pattern is very verbose with examples
- Average 13 lines per anti-pattern
- Could condense to 7 lines per anti-pattern (essential mistake + correct approach)
- Remove verbose "Why it's wrong" explanations (obvious from context)

**Reduction Strategy:** Condense to essential guidance
- Format:
  ```markdown
  ### Anti-Pattern N: [Name]

  ❌ WRONG: [Brief description]
  ✅ CORRECT: [Brief fix]
  ```
- Target: 7 lines per anti-pattern × 10 = 70 lines
- Savings: 131 → 70 lines (61 lines saved)

---

### Target 2: Real-World Examples (Lines 986-1249)
**Current:** 264 lines covering 3 detailed examples

**Content:**
- Example 1: Adding Integration Point Test (lines 988-1105): 118 lines
  - Implementation code review (Python code blocks)
  - Current test plan (markdown template)
  - S8.P2 updates (updated scenario + new scenario)
  - Result summary
- Example 2: Adding Edge Case Test (lines 1107-1208): 102 lines
  - Implementation code review
  - Current test plan comparison
  - S8.P2 update with 2 edge case scenarios
- Example 3: Updating Success Criteria (lines 1210-1249): 40 lines
  - Original criteria
  - S8.P2 updated criteria with rationale

**Issue:** Extremely detailed examples with full code blocks
- Example 1: 118 lines including full Python implementation + test scenarios
- Example 2: 102 lines with full code + 2 detailed test scenarios
- Redundant with patterns already established in Detailed Workflow section

**Reduction Strategy:** Extract to separate reference file
- Create: `reference/stage_8/testing_update_examples.md`
- Move all 3 examples (264 lines) to new file
- Replace with brief overview + reference:
  ```markdown
  ## Real-World Examples

  **Complete examples with code:** See `reference/stage_8/testing_update_examples.md`

  **Example scenarios covered:**
  1. Adding integration point test after feature_01 (PlayerManager → ConfigManager)
  2. Adding edge case tests (missing data, boundary conditions)
  3. Updating epic success criteria based on implementation insights

  **Each example includes:**
  - Implementation code review
  - Current test plan state
  - S8.P2 updates applied
  - Rationale for changes
  ```
- Savings: 264 → 15 lines (249 lines saved)

---

### Target 3: STEP 1 Detailed Workflow (Lines 288-401)
**Current:** 114 lines for reviewing actual implementation

**Content:**
- 1a. Read Just-Completed Feature Code (lines 294-328): 35 lines with Python code
- 1b. Identify Integration Points (lines 330-370): 41 lines with full template
- 1c. Note Edge Cases and Behaviors (lines 372-401): 30 lines with full template

**Issue:** Very detailed with full templates and code examples
- Each sub-step has extensive example with code blocks
- Templates are 15-20 lines each (could be condensed)

**Reduction Strategy:** Condense to essential guidance
- 1a: Remove Python code example (12 lines saved)
- 1b: Condense integration points template (15 lines saved)
- 1c: Condense edge cases template (10 lines saved)
- Keep essential process, reference examples file for details
- Target: 114 → 77 lines (37 lines saved)

---

**Reduction Strategy Summary:**

**Strategy A: Condense Common Mistakes**
- Condense 10 anti-patterns to essential format (7 lines each)
- Savings: 61 lines

**Strategy B: Extract Real-World Examples**
- Move 3 detailed examples to `reference/stage_8/testing_update_examples.md`
- Replace with brief overview + reference
- Savings: 249 lines

**Strategy C: Condense STEP 1**
- Remove verbose code examples and templates
- Reference examples file for details
- Savings: 37 lines

**Total Reduction:** 347 lines

**Projected Outcome:** 1345 → 998 lines (✅ just under threshold)

**Effort:** 3-4 hours (condensing + extraction + cross-reference updates)

---

## FILE 11: reference/glossary.md

**Current Size:** 1447 lines (❌ CRITICAL - 447 over threshold, LARGEST file overall)

**Analysis:**

**File Purpose:** Comprehensive glossary of all workflow terms

**Structure:**
- Header + Usage Guide (lines 1-42)
- Alphabetical terms A-Z (lines 44-1323): ~1280 lines
- Abbreviations (lines 1326-1332): 7 lines
- Cross-References by Guide (lines 1334-1380): 47 lines
- Deprecated Terms (lines 1392-1447): 56 lines

**Verbosity Analysis:**

The glossary has **~100 term definitions** averaging 13 lines each. Many terms are extremely verbose with:
- Detailed examples (5-10 lines)
- Full bullet lists of sub-types
- Complete tables
- Multiple contexts explained
- Cross-references and guide links

### Verbose Terms Analysis

**Severely Verbose Terms (>20 lines each):**

1. **Discovery Phase** (lines 289-311): 23 lines
   - Definition + Purpose + 4-step process + Key Rules + Time-Box + See Also + Guide
   - Could condense to: 12 lines (11 saved)

2. **DISCOVERY.md** (lines 313-338): 26 lines
   - Location + Created/Immutable status + 9 sections listed + Purpose + See Also + Guide
   - Could condense to: 13 lines (13 saved)

3. **Gate** (lines 493-517): 25 lines
   - Two types explanation + Table with 11 gates + See Also + Guide
   - Could condense to: 15 lines (10 saved)

4. **Iteration** (lines 679-701): 23 lines
   - Total count + 3 rounds breakdown + Letter suffix explanation + Examples + See Also + Guide
   - Could condense to: 12 lines (11 saved)

5. **Phase** (lines 872-890): 19 lines
   - Multiple contexts warning + Table with 4 contexts + See Also
   - Could condense to: 11 lines (8 saved)

**Moderately Verbose Terms (15-20 lines each):**

6. **Algorithm Traceability Matrix** (lines 85-96): 12 lines (reasonable, keep)

7. **Checklist.md** (lines 131-150): 20 lines
   - Definition + Created/Updated timeline + Critical rule + Format + Purpose + See Also
   - Could condense to: 12 lines (8 saved)

8. **Discovery Context** (lines 247-267): 21 lines
   - Purpose + 4 Contents bullets + Created/Completed + See Also + Guide
   - Could condense to: 12 lines (9 saved)

9. **Discovery Loop** (lines 269-287): 19 lines
   - Loop Structure (6 steps) + Exit Condition + Time-Box + See Also + Guide
   - Could condense to: 11 lines (8 saved)

10. **Epic** (lines 388-403): 16 lines
    - Structure (3 bullets) + Lifecycle + Typical size + See Also + Guide
    - Could condense to: 10 lines (6 saved)

11. **Feature** (lines 454-473): 20 lines
    - Naming + Structure (6 bullets) + Lifecycle + See Also + Guide
    - Could condense to: 12 lines (8 saved)

12. **Implementation Phasing** (lines 592-610): 19 lines
    - Definition + Typical phases + 6 example phases + Purpose + See Also + Guide
    - Could condense to: 11 lines (8 saved)

13. **Integration Verification** (lines 628-640): 13 lines (reasonable, maybe trim 2-3)

14. **Interface Contracts** (lines 642-658): 17 lines
    - Verified in (3 bullets) + Critical rule + See Also + Guide
    - Could condense to: 11 lines (6 saved)

15. **ISSUES_CHECKLIST.md** (lines 660-677): 18 lines
    - Location (2 bullets) + 4 Statuses + See Also + Guide
    - Could condense to: 11 lines (7 saved)

16. **QC Rounds** (lines 966-984): 19 lines
    - Two contexts + Feature QC (3 rounds) + Epic QC (3 rounds) + Restart protocol + See Also + Guide
    - Could condense to: 12 lines (7 saved)

17. **Round** (lines 1071-1087): 17 lines
    - Two contexts + S5 rounds (3 bullets) + QC rounds definition + See Also
    - Could condense to: 11 lines (6 saved)

18. **Smoke Testing** (lines 1103-1121): 19 lines
    - Two contexts + Feature (3 parts) + Epic (4 parts) + Restart rule + See Also + Guide
    - Could condense to: 12 lines (7 saved)

19. **Spec.md** (lines 1123-1142): 20 lines
    - Created/Updated + 6 Sections + See Also + Guide
    - Could condense to: 12 lines (8 saved)

20. **Spec Validation** (lines 1144-1160): 17 lines
    - Definition + 3 validated sources + Critical rule + Purpose + See Also + Guide
    - Could condense to: 11 lines (6 saved)

21. **Stage** (lines 1162-1181): 20 lines
    - Definition + 10 stages listed + All mandatory + See Also + Guide
    - Could condense to: 12 lines (8 saved)

22. **S5 Sub-Stages** (lines 1183-1197): 15 lines
    - 5 sub-stages listed + Loop + See Also + Guide
    - Could condense to: 10 lines (5 saved)

23. **implementation_plan.md** (lines 1201-1221): 21 lines
    - Created/Approved/Used + 7 Structure bullets + See Also + Guide
    - Could condense to: 12 lines (9 saved)

**Additional Condensing Targets:**

24. **Cross-References by Guide** (lines 1334-1380): 47 lines
    - Lists relevant terms for each stage (S1-S10, Debugging, etc.)
    - Very repetitive format
    - Could condense to: 25 lines (22 saved)

25. **Deprecated Terms** (lines 1392-1447): 56 lines
    - Two large tables mapping old → new notation
    - Could condense to: 30 lines (26 saved)

---

**Reduction Strategy Summary:**

**Strategy: Aggressive Term Condensing (30+ terms)**

**Tier 1: Severely Verbose (>20 lines) - 5 terms**
- Discovery Phase: 23 → 12 (11 saved)
- DISCOVERY.md: 26 → 13 (13 saved)
- Gate: 25 → 15 (10 saved)
- Iteration: 23 → 12 (11 saved)
- Phase: 19 → 11 (8 saved)
- **Subtotal: 53 lines saved**

**Tier 2: Moderately Verbose (15-20 lines) - 18 terms**
- Checklist.md: 20 → 12 (8)
- Discovery Context: 21 → 12 (9)
- Discovery Loop: 19 → 11 (8)
- Epic: 16 → 10 (6)
- Feature: 20 → 12 (8)
- Implementation Phasing: 19 → 11 (8)
- Interface Contracts: 17 → 11 (6)
- ISSUES_CHECKLIST.md: 18 → 11 (7)
- QC Rounds: 19 → 12 (7)
- Round: 17 → 11 (6)
- Smoke Testing: 19 → 12 (7)
- Spec.md: 20 → 12 (8)
- Spec Validation: 17 → 11 (6)
- Stage: 20 → 12 (8)
- S5 Sub-Stages: 15 → 10 (5)
- implementation_plan.md: 21 → 12 (9)
- Plus 2 more at ~6 lines each
- **Subtotal: 130 lines saved**

**Tier 3: Additional Sections**
- Cross-References: 47 → 25 (22 saved)
- Deprecated Terms: 56 → 30 (26 saved)
- **Subtotal: 48 lines saved**

**Additional Condensing (Tier 4):** Many other terms could trim 2-5 lines each
- Target: ~50 more terms at 3 lines average = 150 lines
- Approach: Remove redundant examples, trim bullets, condense explanations

**Total Potential Reduction:**
- Tier 1: 53 lines
- Tier 2: 130 lines
- Tier 3: 48 lines
- Tier 4: 150 lines
- **Total: ~380 lines saved**

**Projected Outcome:** 1447 → 1067 lines (still 67 over threshold)

**Additional Condensing Needed:** 70 more lines
- Target: More aggressive trimming of ALL terms
- Remove ALL examples (just essential definitions)
- Condense "See Also" and "Guide" references
- Final target: 1447 → 997 lines

**Effort:** 5-6 hours (extremely tedious line-by-line condensing of 80+ terms)

---

## Session 4 Summary

| File | Current | Strategy | Target | Effort |
|------|---------|----------|--------|--------|
| s3_cross_feature_sanity_check.md | 1355 | Extract parallel work (190) + Condense Step 2 (80) + Additional (77) | ~1008 | 4-5h |
| s8_p2_epic_testing_update.md | 1345 | Condense mistakes (61) + Extract examples (249) + Condense STEP 1 (37) | ~998 | 3-4h |
| glossary.md | 1447 | Aggressive condensing of 80+ terms (450) | ~997 | 5-6h |

**Total Reduction Potential:** ~780 lines across 3 files
**Total Execution Effort:** 12-15 hours (most complex reductions)

**Key Insights:**

1. **Final 3 files are the most challenging:**
   - Largest files in system (1300-1450 lines each)
   - Require most aggressive reduction strategies
   - glossary.md will be most tedious (line-by-line condensing)

2. **Mixed strategies required:**
   - s3: Extraction (parallel work) + multiple condensing passes
   - s8: Extraction (examples) + condensing (mistakes + steps)
   - glossary: Pure condensing (80+ terms, ~450 lines)

3. **All 3 files will be JUST under threshold:**
   - s3: ~1008 lines (8 over, need final polish)
   - s8: ~998 lines (2 under)
   - glossary: ~997 lines (3 under)
   - Very tight margins - careful execution required

---

## Overall D10 Stage 2 Progress

**Analysis Status:** ✅ COMPLETE (11/11 files = 100%)

**Session Summary:**
- Session 1: Quick Wins (2 files) - EXECUTED ✅
- Session 2: Files 3-5 (s1, s2, s4) - Plans ready
- Session 3: Files 6-8 (s5 iteration files) - Plans ready
- Session 4: Files 9-11 (s3, s8, glossary) - Plans ready ✅

**Total Estimated Reduction (All 11 Files):**
- Quick Wins (executed): 1,649 lines eliminated ✅
- Files 3-5: 390 lines
- Files 6-8: ~2,400 lines
- Files 9-11: ~780 lines
- **Grand Total: ~5,200+ lines eliminated across 11 files**

**Total Execution Effort Remaining:**
- Files 3-5: 9 hours
- Files 6-8: 9-12 hours
- Files 9-11: 12-15 hours
- **Total: 30-36 hours of Stage 3 execution work**

---

**Session 4 Complete**
**Next:** Begin Stage 3 execution (files 3-11) OR continue with other audit dimensions
**Recommendation:** Execute reductions in priority order (files closest to threshold first, glossary last as most tedious)

