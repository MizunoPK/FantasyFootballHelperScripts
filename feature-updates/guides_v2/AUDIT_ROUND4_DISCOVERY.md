# AUDIT ROUND 4 - CROSS-REFERENCE VALIDATION

**Date:** 2026-02-01
**Focus:** Verify all file path references actually exist
**Method:** Automated link checking + manual categorization

---

## Discovery Approach

**Fresh Eyes Method:** Completely different from Rounds 1-3

**Round 1:** Step number mapping validation
**Round 2:** Router links and path formats
**Round 3:** Notation standardization (manual reading)
**Round 4:** Cross-reference validation (automated checking)

**Process:**
1. Extract all file path references from all stage guides
2. Verify each referenced file actually exists
3. Categorize broken references by pattern
4. Identify source files containing each broken reference

---

## Summary

**Total Broken References:** 20 unique broken file paths
**Total Reference Instances:** 31+ occurrences across guides
**Categories:** 4 distinct patterns

---

## Category 1: Missing "s#_" Prefix

**Pattern:** File names missing the stage prefix
**Impact:** 5 broken references

### 1.1: stages/s10/epic_cleanup.md
**Should be:** stages/s10/s10_epic_cleanup.md
**Referenced in:**
- stages/s10/s10_p1_guide_update_workflow.md (1 occurrence)

### 1.2: stages/s2/feature_deep_dive.md
**Should be:** stages/s2/s2_feature_deep_dive.md
**Referenced in:**
- stages/s2/s2_feature_deep_dive.md (self-reference - 1 occurrence)
- stages/s5/s5_bugfix_workflow.md (1 occurrence)

### 1.3: stages/s3/cross_feature_sanity_check.md
**Should be:** stages/s3/s3_cross_feature_sanity_check.md
**Referenced in:**
- stages/s2/s2_feature_deep_dive.md (1 occurrence)
- stages/s2/s2_p3_refinement.md (1 occurrence)
- stages/s3/s3_cross_feature_sanity_check.md (self-reference - 1 occurrence)

### 1.4: stages/s4/epic_testing_strategy.md
**Should be:** stages/s4/s4_epic_testing_strategy.md
**Referenced in:**
- stages/s3/s3_cross_feature_sanity_check.md (1 occurrence)
- stages/s4/s4_epic_testing_strategy.md (self-reference - 1 occurrence)

### 1.5: stages/s9/epic_final_qc.md
**Should be:** stages/s9/s9_epic_final_qc.md
**Referenced in:**
- stages/s9/s9_epic_final_qc.md (self-reference - 1 occurrence)

---

## Category 2: Old File Names (Pre-Refactor)

**Pattern:** References using old file naming conventions
**Impact:** 1 broken reference

### 2.1: stages/s2/phase_1_specification.md
**Should be:** stages/s2/s2_p2_specification.md
**Referenced in:**
- stages/s10/s10_p1_guide_update_workflow.md (1 occurrence)

---

## Category 3: Wrong Stage Number

**Pattern:** File referenced in wrong stage folder
**Impact:** 2 broken references

### 3.1: stages/s6/epic_smoke_testing.md
**Should be:** stages/s9/s9_p1_epic_smoke_testing.md
**Context:** Epic smoke testing is S9.P1, not S6
**Referenced in:**
- stages/s8/s8_p2_epic_testing_update.md (1 occurrence)

### 3.2: stages/s6/epic_qc_rounds.md
**Should be:** stages/s9/s9_p2_epic_qc_rounds.md
**Context:** Epic QC rounds is S9.P2, not S6
**Referenced in:**
- stages/s10/s10_p1_guide_update_workflow.md (1 occurrence)

---

## Category 4: Old Guide Names (S5/S7/S9)

**Pattern:** References to guides that were renamed or moved
**Impact:** 12 broken references

### S5 Old Names (5 references)

#### 4.1: stages/s5/bugfix_workflow.md
**Should be:** stages/s5/s5_bugfix_workflow.md
**Referenced in:**
- stages/s5/s5_bugfix_workflow.md (self-reference - 1 occurrence)
- stages/s9/s9_p3_user_testing.md (1 occurrence)

#### 4.2: stages/s5/implementation_execution.md
**Should be:** stages/s6/s6_execution.md
**Context:** Implementation execution is S6, not S5
**Referenced in:**
- stages/s5/s5_bugfix_workflow.md (1 occurrence)
- stages/s5/s5_p3_i3_gates_part2.md (1 occurrence)
- stages/s6/s6_execution.md (self-reference - 1 occurrence)

#### 4.3: stages/s5/pr_review_protocol.md
**Should be:** stages/s5/s5_pr_review_protocol.md
**Referenced in:**
- stages/s9/s9_p4_epic_final_review.md (1 occurrence)

#### 4.4: stages/s5/qc_rounds.md
**Should be:** stages/s7/s7_p2_qc_rounds.md
**Context:** QC rounds is S7.P2, not S5
**Referenced in:**
- stages/s10/s10_p1_guide_update_workflow.md (1 occurrence)

#### 4.5: stages/s5/smoke_testing.md
**Should be:** stages/s7/s7_p1_smoke_testing.md
**Context:** Smoke testing is S7.P1, not S5
**Referenced in:**
- stages/s10/s10_p1_guide_update_workflow.md (1 occurrence)

### S7 Old Names (3 references)

#### 4.6: stages/s7/epic_cleanup.md
**Should be:** stages/s10/s10_epic_cleanup.md
**Context:** Epic cleanup is S10, not S7
**Referenced in:**
- stages/s9/s9_epic_final_qc.md (1 occurrence)
- stages/s9/s9_p4_epic_final_review.md (1 occurrence)

#### 4.7: stages/s7/implementation_execution.md
**Should be:** stages/s6/s6_execution.md
**Context:** Implementation execution is S6, not S7
**Referenced in:**
- stages/s7/s7_p3_final_review.md (1 occurrence)

#### 4.8: stages/s7/post_feature_alignment.md
**Should be:** stages/s8/s8_p1_cross_feature_alignment.md
**Context:** Post-feature alignment is S8.P1, not S7
**Referenced in:**
- stages/s7/s7_p3_final_review.md (1 occurrence)

### S9 Old Names (4 references)

#### 4.9: stages/s9/epic_final_review.md
**Should be:** stages/s9/s9_p4_epic_final_review.md
**Referenced in:**
- stages/s9/s9_epic_final_qc.md (1 occurrence)

#### 4.10: stages/s9/epic_qc_rounds.md
**Should be:** stages/s9/s9_p2_epic_qc_rounds.md
**Referenced in:**
- stages/s9/s9_epic_final_qc.md (1 occurrence)
- stages/s9/s9_p2_epic_qc_rounds.md (self-reference - 1 occurrence)
- stages/s9/s9_p3_user_testing.md (1 occurrence)

#### 4.11: stages/s9/epic_smoke_testing.md
**Should be:** stages/s9/s9_p1_epic_smoke_testing.md
**Referenced in:**
- stages/s9/s9_epic_final_qc.md (2 occurrences)
- stages/s9/s9_p3_user_testing.md (1 occurrence)

#### 4.12: stages/s9/user_testing.md
**Should be:** stages/s9/s9_p3_user_testing.md
**Referenced in:**
- stages/s9/s9_epic_final_qc.md (1 occurrence)

---

## Severity Assessment

**Severity:** CRITICAL - Broken links prevent navigation between guides

**Impact:**
- Agents cannot follow guide references
- Router files link to non-existent guides
- Cross-stage navigation broken
- Historical inconsistency from multiple refactoring waves

**User Impact:** HIGH
- Confusion when following guide instructions
- Manual file searching required
- Reduced guide usability

---

## Root Cause Analysis

**Primary Cause:** Multiple refactoring waves without comprehensive link updates

**Contributing Factors:**
1. **S5-S8 Expansion:** When S5 was split into S5-S8, many references weren't updated
2. **Stage Renaming:** When S6→S9, S7→S10, references used old stage numbers
3. **File Prefix Addition:** When s#_ prefix was added, not all references updated
4. **Self-References:** Some files reference themselves with old names

**Historical Context:**
- Original workflow: S1-S7 (7 stages)
- Refactor 1: S5 split into S5a-S8a (8 stages)
- Refactor 2: Added S9, renamed S7→S10 (10 stages)
- Refactor 3: Notation change (S5a→S5.P1, added s#_ prefix)
- Each refactor left broken links

---

## Next Steps

**Recommended Action:** Systematic fix of all 20 broken references

**Fix Strategy:**
1. Group fixes by source file (minimize file edits)
2. Use precise string replacement (old path → new path)
3. Verify all fixes with automated re-check
4. Commit with detailed change log

**Estimated Fixes:** 31+ individual replacements across 15+ files
