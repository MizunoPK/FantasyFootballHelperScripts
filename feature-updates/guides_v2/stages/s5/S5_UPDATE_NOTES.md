# S5 Update Notes - Proposal 7

**Status:** Documented (Full implementation requires detailed file updates)

---

## Prerequisites

**Before reading this document:**

- [ ] Familiar with S5 (Implementation Planning) workflow structure
- [ ] Understanding of what testing iterations (I8-I10) were before they moved to S4
- [ ] Context: This document describes changes already implemented in S5 guides

**Note:** This is a historical reference document, not an active workflow guide.

---

## Overview

**What is this document?**
S5 Update Notes (Proposal 7) documents the structural changes made to S5 (Implementation Planning) when testing iterations (I8-I10) were moved to S4, requiring iteration renumbering and Validation Loop additions.

**Purpose:** Implementation reference for understanding S5's current 22-iteration structure.

---

## Summary of Required Changes

**Proposal 7** requires updating S5 to:
1. Remove testing iterations (I8-I10 moved to S4)
2. Renumber remaining 22 iterations sequentially
3. Add Validation Loops at 2 locations
4. Add test_strategy.md validation in I1
5. Update Gate 5 definition with 3-tier rejection

---

## 1. Testing Iterations Removed (Moved to S4)

**These S5 files are DEPRECATED:**
- `s5_p2_i1_test_strategy.md` (old I8) → Moved to S4.I1
- `s5_p2_i2_reverification.md` (old I9) → Moved to S4.I2
- `s5_p2_i3_final_checks.md` (old I10) → Moved to S4.I3

**Rationale:** Test-driven development - tests planned BEFORE implementation (S4), not during planning (S5)

---

## 2. Iteration Renumbering

**Old Structure (with gaps):**
- Round 1: I1-I7 (7 iterations)
- *Skip I8-I10 (moved to S4)*
- Round 1 cont: I11-I12 (2 iterations)
- Round 2: I13-I16 (4 iterations)
- Round 3: I17-I25 (9 iterations)
- **Total: 22 iterations**

**New Structure (sequential):**
- **Round 1:** I1-I7 (7 iterations) + Validation Loop
- **Round 2:** I8-I13 (6 iterations)
- **Round 3:** I14-I22 (9 iterations)
- **Total: 22 iterations**

**Detailed Mapping:**
```text
Old → New
I1  → I1   (unchanged)
I2  → I2   (unchanged)
I3  → I3   (unchanged)
I4  → I4   (unchanged)
I5  → I5   (unchanged)
I6  → I6   (unchanged)
I7  → I7   (unchanged)
I11 → I8   (renumbered)
I12 → I9   (renumbered)
I13 → I10  (renumbered)
I14 → I11  (renumbered)
I15 → I12  (renumbered)
I16 → I13  (renumbered)
I17 → I14  (renumbered)
I18 → I15  (renumbered)
I19 → I16  (renumbered)
I20 → I17  (renumbered)
I21 → I18  (renumbered)
I22 → I19  (renumbered)
I23 → I20  (renumbered)
I24 → I21  (renumbered)
I25 → I22  (renumbered)
```markdown

**Files Requiring Renumbering:**
- All iteration guides (I8-I22)
- All router files (s5_p1_planning_round1.md, s5_p2_planning_round2.md, s5_p3_planning_round3.md)
- Cross-references in other stages

---

## 3. Add Validation Loop to Round 1 End

**Location:** End of `s5_p1_planning_round1.md` (after I7 completes)

**Purpose:** Validate Round 1 work before proceeding to Round 2

**Steps:**
1. After completing I7 (Integration Points Check)
2. Run Validation Loop validation:
   - **Round 1:** Sequential read, check all Round 1 criteria
     - Verify Gates 4a, 7a embedded and passed
     - Check requirements, algorithms, integration points all validated
   - **Round 2:** Fresh review, find gaps
   - **Round 3:** Final validation
   - **Exit:** 3 consecutive clean rounds
3. Only proceed to Round 2 after Validation Loop passes

**Reference:** Create context guide or use generic validation checklist

---

## 4. Add Validation Loop to Round 3 (Pre-Gate 23a)

**Location:** `s5_p3_planning_round3.md` before Gate 23a (Pre-Implementation Spec Audit)

**Purpose:** Validate implementation plan before final gates

**Steps:**
1. After completing preparation iterations (I14-I19)
2. Before Gate 23a (I20)
3. Run Validation Loop validation:
   - **Round 1:** Sequential read of entire implementation_plan.md
     - Check completeness, consistency, traceability
   - **Round 2:** Fresh review, different patterns
   - **Round 3:** Final validation
   - **Exit:** 3 consecutive clean rounds
4. Only proceed to Gate 23a after Validation Loop passes

**Reference:** Similar to Round 1 Validation Loop

---

## 5. Add test_strategy.md Validation to S5.P1.I1

**Location:** `s5_p1_i1_requirements.md`

**New Step 0:** Merge Test Strategy from S4 (5-10 min)

**Prerequisites Check:**

1. **Verify file exists:**
   ```bash
   ls feature_{N}_{name}/test_strategy.md
   ```

2. **If file missing:**
   - STOP immediately
   - Output error: "test_strategy.md not found - S4 may not have completed"
   - Escalate to user: "S4 test strategy file is missing. Should I:"
     - (A) Go back to S4 to create test strategy
     - (B) Create placeholder test strategy now (not recommended)
     - (C) Investigate why S4 didn't create file
   - **Do NOT proceed without test strategy**

3. **If file exists, validate content:**
   - Read file to verify not empty
   - Check file contains required sections:
     - "Unit Tests" or "Test Strategy" section header
     - At least 50 bytes of content
   - **If empty/invalid:**
     - STOP immediately
     - Escalate to user with same options as above
     - **Do NOT proceed with empty file**

4. **If file exists and valid:**
   - Read `feature_{N}_{name}/test_strategy.md`
   - Incorporate into implementation_plan.md "Test Strategy" section
   - Include: All test categories, representative cases, coverage goal, traceability matrix
   - Reference S4 test strategy throughout implementation tasks

**Rationale:** test_strategy.md is foundation for implementation planning (Issue #39, #45)

---

## 6. Update Gate 5 Definition (3-Tier Rejection)

**Location:** End of `s5_p3_planning_round3.md` (after I22/new numbering)

**Current:** Simple user approval

**New:** 3-tier rejection handling (Issue #48)

**Gate 5: User Approval of Implementation Plan**

Present implementation_plan.md to user.

**If User Approves:** Proceed to S6 (Execution)

**If User Requests Changes:**
- Update implementation_plan.md based on feedback
- LOOP BACK to appropriate round:
  - Minor changes (wording, order) → Re-present immediately
  - Requirements issues → Loop back to Round 1 (I1)
  - Algorithm issues → Loop back to Round 1 (I4)
  - Major structural issues → Loop back to S4 (test strategy may need revision)
- Re-validate with Validation Loop
- Re-present for approval (Gate 5 again)

**If User Rejects Entire Approach (3-Tier):**

User says: "This implementation approach is fundamentally wrong"

**STOP - Do not loop back within S5**

Ask user for guidance:
1. **(Tier 1) Re-do S4 (test strategy)** - Test-driven approach was wrong
2. **(Tier 2) Re-do S2 (spec)** - Requirements misunderstood
3. **(Tier 3) Exit feature planning** - Feature should not proceed

Await user decision before proceeding.

**Rationale:** Total rejection indicates problem earlier than S5, not implementation detail issue

---

## 7. Round 3 Exit Sequence Clarification (Issue #49)

**Current confusion:** Order of I23→I25→I24→Gate 5 unclear

**Clarified sequence (with new numbering):**
1. Complete I14-I19 (preparation iterations)
2. Run Pre-Gate 23a Validation Loop
3. I20: Gate 23a (Pre-Implementation Spec Audit - 5 parts)
4. I21: Gate 25 (Spec Validation Check)
5. I22: Gate 24 (GO/NO-GO Decision based on confidence)
6. **Exit Round 3**
7. Present to user for Gate 5 approval

**Rationale:** Gates execute in this order for logical validation flow

---

## Implementation Status

**Current Status:** Documented

**Files Requiring Updates:**
- [ ] s5_p1_i1_requirements.md (add test_strategy.md validation)
- [ ] s5_p1_planning_round1.md (add Validation Loop at end, update router)
- [ ] s5_p2_planning_round2.md (remove I8-I10 references, update router, renumber I11-I13 to I8-I10)
- [ ] s5_p3_planning_round3.md (add Validation Loop before Gate 23a, clarify exit sequence, add Gate 5 3-tier rejection)
- [ ] All I8-I22 iteration files (renumber references)
- [ ] s5_p3_i2_gates_part1.md (renumber from old I23 to new I20)
- [ ] s5_p3_i3_gates_part2.md (renumber from old I24-I25 to new I21-I22)

**Deprecated Files:**
- [ ] Mark s5_p2_i1_test_strategy.md as DEPRECATED (moved to S4.I1)
- [ ] Mark s5_p2_i2_reverification.md as DEPRECATED (moved to S4.I2)
- [ ] Mark s5_p2_i3_final_checks.md as DEPRECATED (moved to S4.I3)

**Estimated Effort:** 3-4 hours for detailed updates across all files

**Note:** CLAUDE.md (Proposal 9) will reflect the updated S5 structure in Stage Workflows section.

---

**Source:** PROPOSAL_FIXES_V3.md (Proposal 7)
**Issues Fixed:** #35 (renumbering), #39 (test strategy validation), #45 (validation complete), #48 (Gate 5 rejection), #49 (exit sequence)

---

## Exit Criteria

**You have fully reviewed this document when ALL of these are true:**

- [ ] Understood why testing iterations (I8-I10) moved to S4
- [ ] Reviewed the old vs new iteration numbering structure
- [ ] Noted which files were deprecated vs renumbered
- [ ] Understanding of Validation Loop additions at 2 locations
- [ ] Aware that these changes are already implemented in S5 guides

**Note:** This is a reference document - no action required unless implementing future S5 updates.

---

*This document serves as implementation guide for future S5 updates. The structural changes are documented and will be reflected in CLAUDE.md workflow documentation.*
