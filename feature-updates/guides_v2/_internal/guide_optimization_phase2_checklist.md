# Workflow Guide Optimization - Phase 2 Checklist

**Created:** 2026-01-02
**Purpose:** Advanced optimizations for guide splitting, reference materials, and navigation aids
**Phase 1 Status:** Complete (Quick Wins, High Priority, Medium Priority all done)
**Estimated Total Time:** 15-20 hours

---

## How to Use This Checklist

1. **Start with Priority 1** (Split STAGE_2) - Highest impact
2. **Then Priority 2** (Split STAGE_6) - Consistency with Stage 5c
3. **Continue with Priority 3** (Split STAGE_5ac) - Final Round 3 clarity
4. **Finish with supporting materials** (Reference cards, diagrams, index)
5. **Mark items complete** as you finish them (change `[ ]` to `[x]`)
6. **Update "Last Updated" date** when making changes

---

## Section 1: PRIORITY 1 - Split STAGE_2 into Sub-Stages (4-5 hours)

**Goal:** Break 2,348-line STAGE_2 into 3 focused sub-stages
**Impact:** 66% reduction per guide (2,348 → ~800 lines each)
**Benefit:** Most frequently used stage, natural breakpoints at mandatory gates

---

### Priority 1.1: Create STAGE_2a - Research Phase (90 minutes)

**New File:** `stages/stage_2/phase_0_research.md`
**Content:** Phases 0, 1, and 1.5 (Epic Intent → Research → Audit)
**Estimated Length:** ~800 lines
**Time Estimate:** 45-60 minutes to complete phase

- [ ] **Step 1.1:** Read STAGE_2 lines 1-1200 to understand Research Phase content
- [ ] **Step 1.2:** Create new file `stages/stage_2/phase_0_research.md`
- [ ] **Step 1.3:** Add standard guide header (Mandatory Reading Protocol, Quick Start)
- [ ] **Step 1.4:** Extract and adapt Phase 0 (Epic Intent Extraction)
  - Include all Step 0.1 through 0.5 content
  - Include Phase 0 Verification Checklist
  - Include Agent Status update template
- [ ] **Step 1.5:** Extract and adapt Phase 1 (Targeted Research)
  - Include all research methodology
  - Include DISCOVERY.md template
  - Include research scope guidelines
- [ ] **Step 1.6:** Extract and adapt Phase 1.5 (Research Completeness Audit - MANDATORY GATE)
  - Include all 4 audit categories
  - Include audit questions and evidence requirements
  - Include Phase 1.5 Audit Summary template
  - Include GO/NO-GO decision logic
- [ ] **Step 1.7:** Add Critical Rules section specific to Research Phase
- [ ] **Step 1.8:** Add Critical Decisions Summary
  - Decision Point 1: Phase 1.5 Audit (GO/NO-GO)
- [ ] **Step 1.9:** Add Completion Criteria
  - Epic intent extracted
  - Research complete
  - Audit PASSED (all 4 categories)
- [ ] **Step 1.10:** Add "Next Stage" section pointing to STAGE_2b
- [ ] **Step 1.11:** Test all internal links and verify structure

**Verification:**
- [ ] Guide is ~800 lines
- [ ] All phase content is complete and coherent
- [ ] Mandatory gate (Phase 1.5) is clearly marked
- [ ] Agent Status templates are included
- [ ] Links to STAGE_2b work correctly

**Last Updated:** _________

---

### Priority 1.2: Create STAGE_2b - Specification Phase (90 minutes)

**New File:** `stages/stage_2/phase_1_specification.md`
**Content:** Phases 2 and 2.5 (Update Spec → Alignment Check)
**Estimated Length:** ~700 lines
**Time Estimate:** 30-45 minutes to complete phase

- [ ] **Step 2.1:** Read STAGE_2 lines 1200-1900 to understand Specification Phase
- [ ] **Step 2.2:** Create new file `stages/stage_2/phase_1_specification.md`
- [ ] **Step 2.3:** Add standard guide header
- [ ] **Step 2.4:** Add Prerequisites section
  - STAGE_2a complete (Phase 1.5 audit PASSED)
  - Research findings documented
- [ ] **Step 2.5:** Extract and adapt Phase 2 (Update Spec & Checklist)
  - Include requirement traceability methodology
  - Include spec.md template structure
  - Include checklist.md creation guidelines
  - Include all 3 source types (Epic/User Answer/Derived)
- [ ] **Step 2.6:** Extract and adapt Phase 2.5 (Spec-to-Epic Alignment Check - MANDATORY GATE)
  - Include scope creep detection steps
  - Include missing requirements check
  - Include alignment verification process
  - Include Phase 2.5 Alignment Summary template
  - Include GO/NO-GO decision logic
- [ ] **Step 2.7:** Add Critical Rules section specific to Specification Phase
- [ ] **Step 2.8:** Add Critical Decisions Summary
  - Decision Point 1: Phase 2.5 Alignment Check (GO/NO-GO)
  - Scope creep vs missing requirements decisions
- [ ] **Step 2.9:** Add Completion Criteria
  - Spec.md complete with traceability
  - All requirements have sources
  - Alignment check PASSED
  - No scope creep, no missing requirements
- [ ] **Step 2.10:** Add "Next Stage" section pointing to STAGE_2c
- [ ] **Step 2.11:** Test all internal links

**Verification:**
- [ ] Guide is ~700 lines
- [ ] Both phases are complete
- [ ] Mandatory gate (Phase 2.5) is clearly marked
- [ ] Traceability requirements are emphasized
- [ ] Links to STAGE_2c work correctly

**Last Updated:** _________

---

### Priority 1.3: Create STAGE_2c - Refinement Phase (90 minutes)

**New File:** `stages/stage_2/phase_2_refinement.md`
**Content:** Phases 3, 4, 5, and 6 (Questions → Scope → Alignment → Approval)
**Estimated Length:** ~800 lines
**Time Estimate:** 45-60 minutes to complete phase

- [ ] **Step 3.1:** Read STAGE_2 lines 1900-2348 to understand Refinement Phase
- [ ] **Step 3.2:** Create new file `stages/stage_2/phase_2_refinement.md`
- [ ] **Step 3.3:** Add standard guide header
- [ ] **Step 3.4:** Add Prerequisites section
  - STAGE_2b complete (Phase 2.5 alignment check PASSED)
  - Spec.md complete with traceability
- [ ] **Step 3.5:** Extract and adapt Phase 3 (Interactive Question Resolution)
  - Include ONE question at a time methodology
  - Include update-after-each-answer protocol
  - Include question batching prevention
- [ ] **Step 3.6:** Extract and adapt Phase 4 (Dynamic Scope Adjustment)
  - Include 35-item threshold guideline
  - Include feature splitting criteria
- [ ] **Step 3.7:** Extract and adapt Phase 5 (Cross-Feature Alignment)
  - Include comparison to completed features
  - Include pattern consistency checks
- [ ] **Step 3.8:** Extract and adapt Phase 6 (Acceptance Criteria & User Approval)
  - Include acceptance criteria template
  - Include user approval protocol
  - Include MANDATORY approval requirement
- [ ] **Step 3.9:** Add Critical Rules section specific to Refinement Phase
- [ ] **Step 3.10:** Add Critical Decisions Summary
  - Decision Point 1: Scope adjustment (split feature?)
  - Decision Point 2: User approval (acceptance criteria)
- [ ] **Step 3.11:** Add Stage 2 Complete Checklist (full feature checklist)
  - All phases 0-6 complete
  - Both mandatory gates passed
  - User approval obtained
- [ ] **Step 3.12:** Add Completion Criteria
- [ ] **Step 3.13:** Add "Next Stage" section pointing to STAGE_3 or next feature's STAGE_2a
- [ ] **Step 3.14:** Test all internal links

**Verification:**
- [ ] Guide is ~800 lines
- [ ] All 4 phases are complete
- [ ] User approval requirement is emphasized
- [ ] Full Stage 2 Complete Checklist included
- [ ] Links to next stage work correctly

**Last Updated:** _________

---

### Priority 1.4: Update STAGE_2 as Router/Deprecated (30 minutes)

**File:** `stages/stage_2/feature_deep_dive.md`
**Action:** Convert to router guide pointing to 2a/2b/2c

- [ ] **Step 4.1:** Read current STAGE_2 guide
- [ ] **Step 4.2:** Rename current file to `STAGE_2_feature_deep_dive_guide_ORIGINAL_BACKUP.md`
- [ ] **Step 4.3:** Create new slim `stages/stage_2/feature_deep_dive.md` as router
- [ ] **Step 4.4:** Add deprecation notice at top
- [ ] **Step 4.5:** Add overview of 3-phase split
- [ ] **Step 4.6:** Add navigation table to sub-stages
- [ ] **Step 4.7:** Keep Stage 2 Complete Checklist for reference
- [ ] **Step 4.8:** Add redirect guidance for agents

**Template for new STAGE_2:**

```markdown
# STAGE 2: Feature Deep Dive Guide

**⚠️ IMPORTANT: This guide has been split into 3 focused sub-stages**

**Use the sub-stage guides instead of this file:**
- **STAGE_2a:** Research Phase (Phases 0-1.5)
- **STAGE_2b:** Specification Phase (Phases 2-2.5)
- **STAGE_2c:** Refinement Phase (Phases 3-6)

---

## Why This Guide Was Split

**Problem:** Original STAGE_2 was 2,348 lines - too large for efficient agent navigation
**Solution:** Split into 3 focused guides with natural breakpoints at mandatory gates

**Benefits:**
- 66% size reduction per guide (2,348 → ~800 lines each)
- Clearer phase transitions at mandatory gates
- Easier to resume after session compaction
- Reduced cognitive load

---

## Stage 2 Sub-Stages Overview

**STAGE_2a: Research Phase (45-60 minutes)**
- Phase 0: Epic Intent Extraction
- Phase 1: Targeted Research
- Phase 1.5: Research Completeness Audit (MANDATORY GATE)
- **Exit:** Audit PASSED → Proceed to STAGE_2b
- **Guide:** stages/stage_2/phase_0_research.md

**STAGE_2b: Specification Phase (30-45 minutes)**
- Phase 2: Update Spec & Checklist
- Phase 2.5: Spec-to-Epic Alignment Check (MANDATORY GATE)
- **Exit:** Alignment check PASSED → Proceed to STAGE_2c
- **Guide:** stages/stage_2/phase_1_specification.md

**STAGE_2c: Refinement Phase (45-60 minutes)**
- Phase 3: Interactive Question Resolution
- Phase 4: Dynamic Scope Adjustment
- Phase 5: Cross-Feature Alignment
- Phase 6: Acceptance Criteria & User Approval (MANDATORY)
- **Exit:** User approval obtained → Proceed to next feature or STAGE_3
- **Guide:** stages/stage_2/phase_2_refinement.md

**Total Time:** 2-3 hours per feature (unchanged from original)

---

## How to Navigate

**Starting Stage 2:**
→ Use stages/stage_2/phase_0_research.md

**Resuming mid-Stage 2:**
- If on Phases 0-1.5 → Use STAGE_2a
- If on Phases 2-2.5 → Use STAGE_2b
- If on Phases 3-6 → Use STAGE_2c

---

## Stage 2 Complete Checklist

[Keep the full checklist from original STAGE_2 here for reference]

---

**Original guide preserved at:** STAGE_2_feature_deep_dive_guide_ORIGINAL_BACKUP.md
```

**Verification:**
- [ ] Router guide is clear and concise
- [ ] Links to all 3 sub-stages work
- [ ] Deprecation notice is prominent
- [ ] Original guide is backed up

**Last Updated:** _________

---

### Priority 1.5: Update References to STAGE_2 in Other Guides (30 minutes)

**Files to Update:**
- `stages/stage_1/epic_planning.md`
- `stages/stage_3/cross_feature_sanity_check.md`
- `prompts_reference_v2.md`
- `README.md`
- `EPIC_WORKFLOW_USAGE.md`
- Any other files referencing STAGE_2

- [ ] **Step 5.1:** Search for all references to "STAGE_2" in guides_v2 folder
- [ ] **Step 5.2:** Update STAGE_1 "Next Stage" section to point to STAGE_2a
- [ ] **Step 5.3:** Update STAGE_3 prerequisites to mention STAGE_2c completion
- [ ] **Step 5.4:** Update prompts_reference_v2.md with new phase transition prompts
  - Add "Starting Stage 2a" prompt
  - Add "Starting Stage 2b" prompt
  - Add "Starting Stage 2c" prompt
- [ ] **Step 5.5:** Update README.md guide index with 2a/2b/2c
- [ ] **Step 5.6:** Update workflow documentation
- [ ] **Step 5.7:** Test all updated references

**Verification:**
- [ ] All references updated
- [ ] No broken links
- [ ] Phase transition prompts added

**Last Updated:** _________

---

## Section 2: PRIORITY 2 - Split STAGE_6 into Sub-Stages (3-4 hours)

**Goal:** Break 1,644-line STAGE_6 into 3 focused sub-stages (mirroring Stage 5c)
**Impact:** ~55% reduction per guide (1,644 → ~500 lines each)
**Benefit:** Mirrors Stage 5c structure for consistency, clearer QC restart protocol

---

### Priority 2.1: Create STAGE_6a - Epic Smoke Testing (60 minutes)

**New File:** `stages/stage_6/epic_smoke_testing.md`
**Content:** Epic-level smoke testing using evolved epic_smoke_test_plan.md
**Estimated Length:** ~500 lines
**Time Estimate:** 20-30 minutes to complete

- [ ] **Step 1.1:** Read STAGE_6 Steps 1-2 to understand Epic Smoke Testing
- [ ] **Step 1.2:** Create new file `stages/stage_6/epic_smoke_testing.md`
- [ ] **Step 1.3:** Add standard guide header
- [ ] **Step 1.4:** Extract Step 1: Pre-QC Verification
- [ ] **Step 1.5:** Extract Step 2: Epic Smoke Testing
  - Include epic_smoke_test_plan.md execution steps
  - Include cross-feature integration testing
  - Include end-to-end workflow validation
- [ ] **Step 1.6:** Add Critical Rules section
- [ ] **Step 1.7:** Add Critical Decisions Summary
  - Decision Point 1: Smoke Testing Result (PASS/FAIL)
  - If FAIL → Create bug fix, restart Stage 6a
- [ ] **Step 1.8:** Add Completion Criteria
  - Pre-QC verification passed
  - Epic smoke testing passed
  - All cross-feature workflows tested
- [ ] **Step 1.9:** Add "Next Stage" section pointing to STAGE_6b
- [ ] **Step 1.10:** Test all internal links

**Verification:**
- [ ] Guide is ~500 lines
- [ ] Smoke testing methodology is complete
- [ ] Restart protocol is clear
- [ ] Links to STAGE_6b work correctly

**Last Updated:** _________

---

### Priority 2.2: Create STAGE_6b - Epic QC Rounds (90 minutes)

**New File:** `stages/stage_6/epic_qc_rounds.md`
**Content:** 3 QC rounds for epic-wide validation
**Estimated Length:** ~700 lines
**Time Estimate:** 30-60 minutes to complete

- [ ] **Step 2.1:** Read STAGE_6 Steps 3-5 to understand Epic QC Rounds
- [ ] **Step 2.2:** Create new file `stages/stage_6/epic_qc_rounds.md`
- [ ] **Step 2.3:** Add standard guide header
- [ ] **Step 2.4:** Add Prerequisites section (STAGE_6a complete)
- [ ] **Step 2.5:** Extract Step 3: QC Round 1 - Cross-Feature Integration
- [ ] **Step 2.6:** Extract Step 4: QC Round 2 - Epic-Wide Data Quality
- [ ] **Step 2.7:** Extract Step 5: QC Round 3 - Final Skeptical Review
- [ ] **Step 2.8:** Add QC Restart Protocol
  - If ANY issues → Create bug fix, restart from STAGE_6a
- [ ] **Step 2.9:** Add Critical Rules section
- [ ] **Step 2.10:** Add Critical Decisions Summary
  - All 3 rounds must pass
  - Round 3 requires ZERO issues
- [ ] **Step 2.11:** Add Completion Criteria
- [ ] **Step 2.12:** Add "Next Stage" section pointing to STAGE_6c
- [ ] **Step 2.13:** Test all internal links

**Verification:**
- [ ] Guide is ~700 lines
- [ ] All 3 QC rounds are complete
- [ ] Restart protocol is emphasized
- [ ] Links to STAGE_6c work correctly

**Last Updated:** _________

---

### Priority 2.3: Create STAGE_6c - Epic Final Review (60 minutes)

**New File:** `stages/stage_6/epic_final_review.md`
**Content:** Epic PR review, validation against original request, lessons learned
**Estimated Length:** ~400 lines
**Time Estimate:** 20-30 minutes to complete

- [ ] **Step 3.1:** Read STAGE_6 Steps 6-7 to understand Epic Final Review
- [ ] **Step 3.2:** Create new file `stages/stage_6/epic_final_review.md`
- [ ] **Step 3.3:** Add standard guide header
- [ ] **Step 3.4:** Add Prerequisites section (STAGE_6b complete)
- [ ] **Step 3.5:** Extract Step 6: Epic PR Review (11 categories)
- [ ] **Step 3.6:** Extract Step 7: Validate Against Original Epic Request
- [ ] **Step 3.7:** Add Epic Lessons Learned capture
- [ ] **Step 3.8:** Add Critical Rules section
- [ ] **Step 3.9:** Add Critical Decisions Summary
  - Decision Point 1: PR review finds critical issues? → Restart
- [ ] **Step 3.10:** Add Stage 6 Complete Checklist
- [ ] **Step 3.11:** Add Completion Criteria
- [ ] **Step 3.12:** Add "Next Stage" section pointing to STAGE_7
- [ ] **Step 3.13:** Test all internal links

**Verification:**
- [ ] Guide is ~400 lines
- [ ] Epic PR review is complete
- [ ] Validation against original request is clear
- [ ] Links to STAGE_7 work correctly

**Last Updated:** _________

---

### Priority 2.4: Update STAGE_6 as Router/Deprecated (30 minutes)

**File:** `stages/stage_6/epic_final_qc.md`
**Action:** Convert to router guide pointing to 6a/6b/6c

- [ ] **Step 4.1:** Rename current file to `STAGE_6_epic_final_qc_guide_ORIGINAL_BACKUP.md`
- [ ] **Step 4.2:** Create new slim `stages/stage_6/epic_final_qc.md` as router
- [ ] **Step 4.3:** Add deprecation notice
- [ ] **Step 4.4:** Add overview of 3-phase split (mirrors Stage 5c)
- [ ] **Step 4.5:** Add navigation table to sub-stages
- [ ] **Step 4.6:** Keep Stage 6 Complete Checklist for reference

**Verification:**
- [ ] Router guide is clear
- [ ] Links to all 3 sub-stages work
- [ ] Original guide is backed up

**Last Updated:** _________

---

### Priority 2.5: Update References to STAGE_6 (30 minutes)

**Files to Update:**
- `stages/stage_5/post_feature_testing_update.md`
- `stages/stage_7/epic_cleanup.md`
- `prompts_reference_v2.md`
- `README.md`

- [ ] **Step 5.1:** Search for all references to "STAGE_6"
- [ ] **Step 5.2:** Update STAGE_5e "Next Stage" to point to STAGE_6a
- [ ] **Step 5.3:** Update STAGE_7 prerequisites to mention STAGE_6c completion
- [ ] **Step 5.4:** Update prompts_reference_v2.md with new prompts
- [ ] **Step 5.5:** Update README.md guide index
- [ ] **Step 5.6:** Test all updated references

**Verification:**
- [ ] All references updated
- [ ] No broken links

**Last Updated:** _________

---

## Section 3: PRIORITY 3 - Split STAGE_5ac into Parts (2-3 hours)

**Goal:** Break 1,957-line Round 3 into 2 parts
**Impact:** ~50% reduction per guide (1,957 → ~1,000 lines each)
**Benefit:** Clearer focus on preparation vs final gates

---

### Priority 3.1: Create STAGE_5ac_part1 - Pre-Implementation Preparation (60 minutes)

**New File:** `stages/stage_5/round3_part1_preparation.md`
**Content:** Iterations 17-22 (preparation iterations)
**Estimated Length:** ~900 lines

- [ ] **Step 1.1:** Read STAGE_5ac iterations 17-22
- [ ] **Step 1.2:** Create new file `stages/stage_5/round3_part1_preparation.md`
- [ ] **Step 1.3:** Add standard guide header
- [ ] **Step 1.4:** Extract Iterations 17-22
  - Iteration 17: Implementation Phasing
  - Iteration 18: Rollback Strategy
  - Iteration 19: Algorithm Traceability (Final)
  - Iteration 20: Performance Considerations
  - Iteration 21: Mock Audit
  - Iteration 22: Output Consumer Validation
- [ ] **Step 1.5:** Add Critical Rules section
- [ ] **Step 1.6:** Add Completion Criteria
- [ ] **Step 1.7:** Add "Next Stage" section pointing to STAGE_5ac_part2

**Verification:**
- [ ] Guide is ~900 lines
- [ ] All 6 iterations complete
- [ ] Links to part 2 work

**Last Updated:** _________

---

### Priority 3.2: Create STAGE_5ac_part2 - Final Gates & GO/NO-GO (60 minutes)

**New File:** `stages/stage_5/round3_part2_final_gates.md`
**Content:** Iterations 23, 23a, 25, 24 (final validation and decision)
**Estimated Length:** ~1,000 lines

- [ ] **Step 2.1:** Read STAGE_5ac iterations 23-25 + 23a + 24
- [ ] **Step 2.2:** Create new file `stages/stage_5/round3_part2_final_gates.md`
- [ ] **Step 2.3:** Add standard guide header
- [ ] **Step 2.4:** Add Prerequisites section (Part 1 complete)
- [ ] **Step 2.5:** Extract critical iterations
  - Iteration 23: Integration Gap Check (Final)
  - Iteration 23a: Pre-Implementation Spec Audit (MANDATORY GATE - 4 PARTS)
  - Iteration 25: Spec Validation Against Validated Documents (CRITICAL)
  - Iteration 24: Implementation Readiness Protocol (GO/NO-GO)
- [ ] **Step 2.6:** Emphasize mandatory gates (23a and 25)
- [ ] **Step 2.7:** Add Critical Decisions Summary
- [ ] **Step 2.8:** Add Round 3 Complete Checklist
- [ ] **Step 2.9:** Add "Next Stage" section pointing to STAGE_5b

**Verification:**
- [ ] Guide is ~1,000 lines
- [ ] Mandatory gates are prominent
- [ ] GO/NO-GO decision is clear

**Last Updated:** _________

---

### Priority 3.3: Update STAGE_5ac as Router (30 minutes)

**File:** `stages/stage_5/round3_todo_creation.md`
**Action:** Convert to router pointing to part1/part2

- [ ] **Step 3.1:** Rename current file to `STAGE_5ac_round3_guide_ORIGINAL_BACKUP.md`
- [ ] **Step 3.2:** Create new slim `stages/stage_5/round3_todo_creation.md` as router
- [ ] **Step 3.3:** Add deprecation notice
- [ ] **Step 3.4:** Add navigation to both parts
- [ ] **Step 3.5:** Update references in other guides

**Verification:**
- [ ] Router guide is clear
- [ ] Original guide is backed up

**Last Updated:** _________

---

## Section 4: SUPPORTING MATERIALS - Reference Cards (2-3 hours)

**Goal:** Create quick reference summaries for complex workflows
**Impact:** Faster navigation, better agent understanding
**Benefit:** 1-page summaries for quick consultation

---

### Supporting Material 1: STAGE_2 Reference Card (30 minutes)

**New File:** `STAGE_2_REFERENCE_CARD.md`
**Content:** 1-page summary of all 9 phases

- [ ] **Step 1.1:** Create `STAGE_2_REFERENCE_CARD.md`
- [ ] **Step 1.2:** Add visual overview of 3 sub-stages
- [ ] **Step 1.3:** Create phase summary table
  - Phase number, name, duration, key output
- [ ] **Step 1.4:** Add mandatory gate indicators
- [ ] **Step 1.5:** Add decision tree (when to split features)
- [ ] **Step 1.6:** Add common pitfalls section
- [ ] **Step 1.7:** Keep to 1 page (200-300 lines max)

**Template Structure:**
```markdown
# STAGE 2: Feature Deep Dive - Quick Reference Card

## Sub-Stages Overview
[Visual diagram showing 2a → 2b → 2c]

## Phase Summary Table
| Phase | Name | Sub-Stage | Duration | Key Output | Gate? |
|-------|------|-----------|----------|------------|-------|
| 0 | Epic Intent | 2a | 15 min | Epic Intent section | No |
| 1 | Research | 2a | 30 min | DISCOVERY.md | No |
| 1.5 | Audit | 2a | 20 min | Audit PASSED | ✅ YES |
[...]

## Mandatory Gates
- Phase 1.5: Research Completeness Audit
- Phase 2.5: Spec-to-Epic Alignment Check
- Phase 6: User Approval

## Decision Points
- Split feature if >35 checklist items
- Create questions if ANY uncertainty
- Compare to completed features in Phase 5

## Common Pitfalls
- Skipping Phase 0 (epic intent extraction)
- Not citing sources for requirements
- Assuming instead of asking user
- Batch questions instead of one-at-a-time
```

**Verification:**
- [ ] Card fits on 1 page
- [ ] All phases represented
- [ ] Easy to scan quickly

**Last Updated:** _________

---

### Supporting Material 2: STAGE_5 Reference Card (45 minutes)

**New File:** `STAGE_5_REFERENCE_CARD.md`
**Content:** Visual map of all Stage 5 sub-stages

- [ ] **Step 2.1:** Create `STAGE_5_REFERENCE_CARD.md`
- [ ] **Step 2.2:** Add visual workflow diagram
  - 5a (3 rounds) → 5b → 5c (3 phases) → 5d → 5e
- [ ] **Step 2.3:** Add sub-stage summary table
- [ ] **Step 2.4:** Add mandatory gates across all sub-stages
- [ ] **Step 2.5:** Add restart points (where to restart after bug fix)
- [ ] **Step 2.6:** Add time estimates

**Template Structure:**
```markdown
# STAGE 5: Feature Implementation - Quick Reference Card

## Workflow Diagram
```
5a: TODO Creation (3 rounds, 24 iterations)
    Round 1: Initial Analysis (9 iterations)
    Round 2: Deep Verification (9 iterations)
    Round 3: Final Readiness (10 iterations + 2 gates)
    ↓
5b: Implementation Execution (phased)
    ↓
5c: Post-Implementation (3 phases)
    5ca: Smoke Testing
    5cb: QC Rounds (3 rounds)
    5cc: Final Review
    ↓
5d: Cross-Feature Alignment
    ↓
5e: Testing Plan Update
    ↓
Next Feature or STAGE_6
```

## Mandatory Gates
- Iteration 4a: TODO Specification Audit
- Iteration 23a: Pre-Implementation Spec Audit (4 PARTS)
- Iteration 25: Spec Validation Against Validated Documents
- Stage 5ca: Smoke Testing (Part 3 data validation)
- Stage 5cb Round 3: ZERO issues required

## Restart Points
- If smoke testing fails → Restart from 5ca Part 1
- If QC finds issues → Restart from 5ca Part 1
- If PR review finds critical issues → Restart from 5ca Part 1

## Time Estimates
- 5a: 2.5-3 hours (24 iterations)
- 5b: 1-4 hours (varies by complexity)
- 5c: 1.5-2.5 hours (3 phases)
- 5d: 15-30 minutes
- 5e: 15-30 minutes
**Total:** 5-10 hours per feature
```

**Verification:**
- [ ] Visual diagram is clear
- [ ] All sub-stages represented
- [ ] Restart protocol is obvious

**Last Updated:** _________

---

### Supporting Material 3: Mandatory Gates Reference (30 minutes)

**New File:** `MANDATORY_GATES_REFERENCE.md`
**Content:** All gates across entire workflow

- [ ] **Step 3.1:** Create `MANDATORY_GATES_REFERENCE.md`
- [ ] **Step 3.2:** List all mandatory gates by stage
- [ ] **Step 3.3:** Add gate criteria (what must be true to pass)
- [ ] **Step 3.4:** Add failure consequences (what happens if gate fails)
- [ ] **Step 3.5:** Add gate locations (which guide, which section)

**Template Structure:**
```markdown
# Mandatory Gates Across Epic Workflow - Quick Reference

## Stage 1: Epic Planning
No mandatory gates (user confirmation recommended)

## Stage 2: Feature Deep Dive
**Gate 1: Phase 1.5 - Research Completeness Audit**
- Location: stages/stage_2/phase_0_research.md
- Criteria: All 4 categories PASSED (Component, Pattern, Data, Epic)
- Evidence: File paths, line numbers, code snippets
- If FAIL: Return to Phase 1, research gaps, re-run audit

**Gate 2: Phase 2.5 - Spec-to-Epic Alignment Check**
- Location: stages/stage_2/phase_1_specification.md
- Criteria: Zero scope creep, zero missing requirements
- Evidence: All requirements trace to epic
- If FAIL: Remove scope creep or add missing requirements, re-run check

**Gate 3: Phase 6 - User Approval**
- Location: stages/stage_2/phase_2_refinement.md
- Criteria: User explicitly approves acceptance criteria
- Evidence: User confirmation documented
- If FAIL: Revise acceptance criteria, get approval

## Stage 3: Cross-Feature Sanity Check
**Gate 1: User Sign-Off**
- Criteria: User approves complete epic plan
- If FAIL: Address user concerns, re-run sanity check

## Stage 5a: TODO Creation
**Gate 1: Iteration 4a - TODO Specification Audit**
- Location: stages/stage_5/round1_todo_creation.md
- Criteria: All TODO tasks have acceptance criteria
- If FAIL: Fix tasks, re-run Iteration 4a

**Gate 2: Iteration 23a - Pre-Implementation Spec Audit (4 PARTS)**
- Location: stages/stage_5/round3_part2_final_gates.md
- Criteria: ALL 4 PARTS must PASS
- If FAIL: Fix failing part, re-run Iteration 23a

**Gate 3: Iteration 25 - Spec Validation Against Validated Documents**
- Location: stages/stage_5/round3_part2_final_gates.md
- Criteria: Spec matches epic + ticket + spec summary
- If FAIL: Report to user, user decides next action

**Gate 4: Iteration 24 - Implementation Readiness (GO/NO-GO)**
- Location: stages/stage_5/round3_part2_final_gates.md
- Criteria: GO decision required
- If NO-GO: Address concerns, re-evaluate

## Stage 5c: Post-Implementation
**Gate 1: Smoke Testing Part 3 - Data Validation**
- Location: stages/stage_5/smoke_testing.md
- Criteria: ALL 3 parts pass, data values verified
- If FAIL: Fix issues, restart from Part 1

**Gate 2: QC Round 3 - Zero Issues**
- Location: stages/stage_5/qc_rounds.md
- Criteria: ZERO issues found in Round 3
- If FAIL: Fix issues, restart from smoke testing

## Stage 7: Epic Cleanup
**Gate 1: Unit Tests (100% pass)**
- Location: stages/stage_7/epic_cleanup.md
- Criteria: python tests/run_all_tests.py exits with 0
- If FAIL: Fix tests, re-run

**Gate 2: User Testing (ZERO bugs)**
- Location: stages/stage_7/epic_cleanup.md
- Criteria: User finds zero bugs
- If FAIL: Create bug fix, restart Stage 6

## Summary Statistics
- Total Mandatory Gates: 13
- Gates with Evidence Requirements: 7
- Gates with Restart Protocol: 6
- Gates Requiring User Input: 3
```

**Verification:**
- [ ] All gates are listed
- [ ] Failure consequences are clear
- [ ] Easy to scan for specific gate

**Last Updated:** _________

---

## Section 5: SUPPORTING MATERIALS - Visual Diagrams (2 hours)

**Goal:** Create ASCII/text flowcharts showing workflow navigation
**Impact:** Visual understanding of stage flow
**Benefit:** Easier to understand transitions and decision points

---

### Supporting Material 4: Epic Workflow Visual Diagram (60 minutes)

**New File:** `EPIC_WORKFLOW_DIAGRAM.md`
**Content:** Full workflow from Stage 1 → 7 with decision points

- [ ] **Step 4.1:** Create `EPIC_WORKFLOW_DIAGRAM.md`
- [ ] **Step 4.2:** Create ASCII diagram showing all stages
- [ ] **Step 4.3:** Add decision diamonds for gates
- [ ] **Step 4.4:** Show loop points (feature iteration, QC restart)
- [ ] **Step 4.5:** Add color/symbol legend
- [ ] **Step 4.6:** Create separate diagram for bug fix workflow

**Template Structure:**
```markdown
# Epic Workflow - Visual Diagram

## Main Workflow (All Features)

```
START
  ↓
┌─────────────────────────┐
│   STAGE 1: Epic Planning │
│   - Git branch          │
│   - Epic ticket         │
│   - Folder structure    │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│ FOR EACH FEATURE:       │  ←──────────────┐
│                         │                  │
│ STAGE 2a: Research      │                  │
│   Gate: Phase 1.5 ✅    │                  │
│     ↓                   │                  │
│ STAGE 2b: Specification │                  │
│   Gate: Phase 2.5 ✅    │                  │
│     ↓                   │                  │
│ STAGE 2c: Refinement    │                  │
│   Gate: User Approval ✅│                  │
└──────────┬──────────────┘                  │
           ↓                                  │
    [More features?] ──YES───────────────────┘
           │
          NO
           ↓
┌─────────────────────────┐
│ STAGE 3: Sanity Check   │
│   Gate: User Sign-Off ✅│
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│ STAGE 4: Testing Plan   │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│ FOR EACH FEATURE:       │  ←──────────────┐
│                         │                  │
│ STAGE 5a: TODO (3 rds)  │                  │
│   Gates: 4a, 23a, 25 ✅ │                  │
│     ↓                   │                  │
│ STAGE 5b: Implementation│                  │
│     ↓                   │                  │
│ STAGE 5c: Post-Impl     │ ←─────┐          │
│   5ca: Smoke ✅         │       │          │
│   5cb: QC (3 rds) ✅    │       │          │
│   5cc: Final Review     │       │          │
│     ↓                   │       │          │
│   [Issues?] ──YES───────┘       │          │
│     │                           │          │
│    NO                           │          │
│     ↓                           │          │
│ STAGE 5d: Alignment     │       │          │
│     ↓                   │       │          │
│ STAGE 5e: Test Update   │       │          │
└──────────┬──────────────┘       │          │
           ↓                      │          │
    [More features?] ──YES────────┼──────────┘
           │                      │
          NO                      │
           ↓                      │
┌─────────────────────────┐       │
│ STAGE 6: Epic QC        │       │
│   6a: Epic Smoke ✅     │       │
│   6b: Epic QC (3 rds) ✅│       │
│   6c: Epic Review       │       │
│     ↓                   │       │
│   [Issues?] ──YES───────────────┘
│     │                   │
│    NO                   │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│ STAGE 7: Cleanup        │
│   Gate: Tests ✅        │
│   Gate: User Test ✅    │
│     ↓                   │
│   [User bugs?] ──YES────┘
│     │                   │
│    NO                   │
└──────────┬──────────────┘
           ↓
         DONE
    Move to done/
```

## Legend
- ✅ = Mandatory Gate
- ┌─┐ = Stage/Process
- ◆ = Decision Point
- → = Flow Direction
- ←─ = Loop Back

## Bug Fix Workflow

```
BUG DISCOVERED
       ↓
Create bugfix_{priority}_{name}/
       ↓
┌──────────────────┐
│ STAGE 2 (Slim)   │
│ - Spec only      │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ STAGE 5a (Full)  │
│ - All 24 iters   │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ STAGE 5b (Full)  │
│ - Implementation │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ STAGE 5c (Full)  │
│ - All QC rounds  │
└────────┬─────────┘
         ↓
    RESUME EPIC
(Skip 5d, 5e, 6, 7)
```
```

**Verification:**
- [ ] ASCII diagram renders correctly
- [ ] All stages represented
- [ ] Decision points are clear
- [ ] Loop backs are visible

**Last Updated:** _________

---

### Supporting Material 5: Stage Transition Decision Tree (45 minutes)

**New File:** `STAGE_TRANSITION_DECISION_TREE.md`
**Content:** Decision tree for "where do I go next?"

- [ ] **Step 5.1:** Create `STAGE_TRANSITION_DECISION_TREE.md`
- [ ] **Step 5.2:** Create decision tree for each stage
- [ ] **Step 5.3:** Include error handling paths
- [ ] **Step 5.4:** Add "resuming work" scenarios

**Template Structure:**
```markdown
# Stage Transition Decision Tree

## I just finished... what's next?

### Finished STAGE 1
→ Go to STAGE 2a (first feature)

### Finished STAGE 2a (Research Phase)
→ Phase 1.5 audit PASSED?
  - YES → Go to STAGE 2b
  - NO → Return to Phase 1, research gaps

### Finished STAGE 2b (Specification Phase)
→ Phase 2.5 alignment check PASSED?
  - YES → Go to STAGE 2c
  - NO → Fix scope creep/missing requirements

### Finished STAGE 2c (Refinement Phase)
→ User approved acceptance criteria?
  - YES → Are there more features?
    - YES → Go to STAGE 2a for next feature
    - NO → Go to STAGE 3
  - NO → Revise acceptance criteria

### Finished STAGE 3
→ User signed off on complete plan?
  - YES → Go to STAGE 4
  - NO → Address user concerns

### Finished STAGE 4
→ Go to STAGE 5a (first feature)

[Continue for all stages...]

## I encountered an error... what do I do?

### Smoke Testing Failed (5ca)
→ Fix issue → Restart from STAGE 5ca Part 1

### QC Round 1 or 2 Found Issues (5cb)
→ Fix issues → Restart from STAGE 5ca Part 1

### QC Round 3 Found Issues (5cb)
→ Fix issues → Restart from STAGE 5ca Part 1

### PR Review Found Critical Issues (5cc)
→ Follow QC Restart Protocol → Restart from STAGE 5ca Part 1

### Epic Smoke Testing Failed (6a)
→ Create bug fix → After bug fix, restart STAGE 6a

### Epic QC Found Issues (6b)
→ Create bug fix → After bug fix, restart STAGE 6a

### User Testing Found Bugs (7)
→ Create bug fix → After bug fix, restart STAGE 6a

## I need to resume work... where was I?

### Check EPIC_README.md Agent Status
1. Look at "Current Guide" field
2. Look at "Next Action" field
3. Go to that guide and continue from that action

### If Agent Status says "STAGE_2"
- Check "Current Step" to determine which phase
- Phases 0-1.5 → Use STAGE_2a
- Phases 2-2.5 → Use STAGE_2b
- Phases 3-6 → Use STAGE_2c
```

**Verification:**
- [ ] All transition scenarios covered
- [ ] Error paths are clear
- [ ] Resume logic is explicit

**Last Updated:** _________

---

## Section 6: SUPPORTING MATERIALS - Cross-Reference Index (1 hour)

**Goal:** Map common scenarios to appropriate guides
**Impact:** Faster guide selection
**Benefit:** "I need to..." → "Use this guide"

---

### Supporting Material 6: Scenario-to-Guide Index (60 minutes)

**New File:** `SCENARIO_TO_GUIDE_INDEX.md`
**Content:** Common scenarios mapped to guides

- [ ] **Step 6.1:** Create `SCENARIO_TO_GUIDE_INDEX.md`
- [ ] **Step 6.2:** Create "I need to..." section
- [ ] **Step 6.3:** Create "I found a bug..." section
- [ ] **Step 6.4:** Create "I'm confused about..." section
- [ ] **Step 6.5:** Create "Error type..." section

**Template Structure:**
```markdown
# Scenario-to-Guide Index

## "I need to..."

**"I need to start a new epic"**
→ Use: stages/stage_1/epic_planning.md
- Create git branch
- Create epic ticket
- Set up folder structure

**"I need to understand a feature's requirements"**
→ Use: stages/stage_2/phase_0_research.md
- Extract epic intent
- Research codebase
- Pass research audit

**"I need to create a spec for a feature"**
→ Use: stages/stage_2/phase_1_specification.md
- Document requirements with traceability
- Verify alignment with epic

**"I need to resolve user questions"**
→ Use: stages/stage_2/phase_2_refinement.md
- ONE question at a time
- Update spec after each answer

**"I need to create a TODO list for implementation"**
→ Use: STAGE_5a guides (5aa, 5ab, 5ac)
- Round 1: Initial analysis
- Round 2: Deep verification
- Round 3: Final gates

**"I need to implement a feature"**
→ Use: stages/stage_5/implementation_execution.md
- Keep spec.md visible
- Run tests after every phase

**"I need to test my implementation"**
→ Use: STAGE_5c guides (5ca, 5cb, 5cc)
- 5ca: Smoke testing
- 5cb: QC rounds (3 rounds)
- 5cc: Final review

**"I need to update remaining feature specs"**
→ Use: stages/stage_5/post_feature_alignment.md
- Align specs with actual implementation

**"I need to update the test plan"**
→ Use: stages/stage_5/post_feature_testing_update.md
- Add discovered integration points

**"I need to validate the entire epic"**
→ Use: STAGE_6 guides (6a, 6b, 6c)
- 6a: Epic smoke testing
- 6b: Epic QC rounds
- 6c: Epic final review

**"I need to commit and finish the epic"**
→ Use: stages/stage_7/epic_cleanup.md
- Run tests (100% pass)
- User testing (ZERO bugs)
- Commit and move to done/

---

## "I found a bug..."

**"I found a bug during implementation (Stage 5b)"**
→ Use: stages/stage_5/bugfix_workflow.md
- Get user approval first
- Create bugfix_{priority}_{name}/ folder
- Follow Stage 2 → 5a → 5b → 5c
- Resume epic work after

**"I found a bug during smoke testing (5ca)"**
→ Fix issue → Restart from STAGE_5ca Part 1
- Do NOT create separate bug fix folder
- Fix in place, re-run smoke testing

**"I found a bug during QC rounds (5cb)"**
→ Fix issue → Restart from STAGE_5ca Part 1
- Follow QC Restart Protocol
- Re-run all 3 parts of smoke testing
- Then re-run all 3 QC rounds

**"I found a bug during user testing (Stage 7)"**
→ Use: stages/stage_5/bugfix_workflow.md
- Create bug fix
- After bug fix complete, restart STAGE_6a

---

## "I'm confused about..."

**"I'm confused about which guide to use for Stage 2"**
→ Check your current phase:
- Phases 0-1.5 → stages/stage_2/phase_0_research.md
- Phases 2-2.5 → stages/stage_2/phase_1_specification.md
- Phases 3-6 → stages/stage_2/phase_2_refinement.md

**"I'm confused about which Stage 5 guide to use"**
→ Check your current step:
- Creating TODO → STAGE_5a (5aa, 5ab, 5ac)
- Implementing code → STAGE_5b
- Testing implementation → STAGE_5c (5ca, 5cb, 5cc)
- After feature complete → STAGE_5d then STAGE_5e

**"I'm confused about whether to restart or continue"**
→ Check the stage you're in:
- Smoke testing failed (5ca) → Restart from 5ca Part 1
- QC found issues (5cb) → Restart from 5ca Part 1
- PR review found critical (5cc) → Restart from 5ca Part 1
- Epic QC found issues (6b) → Create bug fix, restart from 6a
- User found bugs (7) → Create bug fix, restart from 6a

---

## "Error type: ..."

**"Error: Spec doesn't match epic intent"**
→ Use: reference/spec_validation.md (optional)
- Assume spec is wrong
- Re-read epic with fresh eyes
- Validate against actual code and data

**"Error: Data assumptions are wrong"**
→ Use: reference/hands_on_data_inspection.md
- Open Python REPL
- Inspect actual data files
- Verify assumptions against reality

**"Error: Implementation loads wrong data"**
→ Likely missed STAGE_5a.5
- Go back and inspect data files
- Fix TODO and spec
- Re-implement with correct understanding

**"Error: Tests pass but data values are wrong"**
→ Smoke testing Part 3 failed
- Inspect actual output data values
- Verify correctness (not just file exists)
- Fix implementation
- Restart from 5ca Part 1

**"Error: Feature works in isolation but breaks with other features"**
→ Epic-level integration issue
- Check STAGE_6a (Epic Smoke Testing)
- Check cross-feature integration points
- Fix integration issue
- Restart Stage 6a

**"Error: Committed code but user found bug"**
→ Stage 7 User Testing failed
- Create bug fix using bug fix workflow
- After bug fix, restart STAGE_6a
- Re-validate entire epic

---

## Quick Reference

**Most Common Paths:**
1. Starting epic → STAGE_1
2. Researching feature → STAGE_2a
3. Writing spec → STAGE_2b
4. Planning implementation → STAGE_5a
5. Implementing → STAGE_5b
6. Testing feature → STAGE_5c
7. Testing epic → STAGE_6
8. Finishing epic → STAGE_7

**Most Common Restart Points:**
1. Smoke testing failed → Restart 5ca Part 1
2. QC found issues → Restart 5ca Part 1
3. Epic QC found issues → Create bug fix, restart 6a
4. User found bugs → Create bug fix, restart 6a
```

**Verification:**
- [ ] All common scenarios covered
- [ ] Clear guide recommendations
- [ ] Error scenarios mapped

**Last Updated:** _________

---

## Section 7: COMPLETION & VALIDATION (1 hour)

**Goal:** Ensure all changes are complete, tested, and documented
**Impact:** Quality assurance
**Benefit:** No broken links, consistent structure

---

### Final Validation 1: Test All Links (30 minutes)

- [ ] **Step 1.1:** Create list of all new/modified files
- [ ] **Step 1.2:** Test all internal links (jump links within files)
- [ ] **Step 1.3:** Test all cross-file links (links between guides)
- [ ] **Step 1.4:** Test all "Next Stage" links
- [ ] **Step 1.5:** Verify all backup files created
- [ ] **Step 1.6:** Document any broken links found and fix

**Files to Test:**
- [ ] stages/stage_2/phase_0_research.md
- [ ] stages/stage_2/phase_1_specification.md
- [ ] stages/stage_2/phase_2_refinement.md
- [ ] stages/stage_2/feature_deep_dive.md (router)
- [ ] stages/stage_6/epic_smoke_testing.md
- [ ] stages/stage_6/epic_qc_rounds.md
- [ ] stages/stage_6/epic_final_review.md
- [ ] stages/stage_6/epic_final_qc.md (router)
- [ ] stages/stage_5/round3_part1_preparation.md
- [ ] stages/stage_5/round3_part2_final_gates.md
- [ ] stages/stage_5/round3_todo_creation.md (router)
- [ ] All reference cards
- [ ] All diagrams
- [ ] Index files

**Last Updated:** _________

---

### Final Validation 2: Verify Structure Consistency (20 minutes)

**Check each new guide has:**
- [ ] Mandatory Reading Protocol section
- [ ] Quick Start section (standardized format)
- [ ] Critical Rules section
- [ ] Critical Decisions Summary section (if applicable)
- [ ] Prerequisites section (for sub-stages)
- [ ] Completion Criteria section
- [ ] Next Stage section
- [ ] Agent Status templates

**Files to Check:**
- [ ] All new STAGE_2 sub-guides (2a, 2b, 2c)
- [ ] All new STAGE_6 sub-guides (6a, 6b, 6c)
- [ ] All new STAGE_5ac sub-guides (part1, part2)

**Last Updated:** _________

---

### Final Validation 3: Update Master Documentation (10 minutes)

**Update these files:**
- [ ] `README.md` - Update guide index with all new files
- [ ] `prompts_reference_v2.md` - Add new phase transition prompts
- [ ] `PLAN.md` - Update workflow specification if needed
- [ ] `EPIC_WORKFLOW_USAGE.md` - Update usage examples

**Verify:**
- [ ] All new guides listed in index
- [ ] All new prompts documented
- [ ] File count is correct (should have 18+ guides now)

**Last Updated:** _________

---

## Post-Implementation Notes

**Implementation Date:** _________
**Agent/User:** _________

**Summary of changes:**
- [ ] STAGE_2 split into 3 sub-stages (2a, 2b, 2c)
- [ ] STAGE_6 split into 3 sub-stages (6a, 6b, 6c)
- [ ] STAGE_5ac split into 2 parts (part1, part2)
- [ ] Reference cards created (3 files)
- [ ] Visual diagrams created (2 files)
- [ ] Cross-reference index created (1 file)

**Total new files created:** _____ (expected: ~15)
**Total files modified:** _____ (expected: ~10)

**Time spent:**
- Priority 1 (STAGE_2 split): _____ hours
- Priority 2 (STAGE_6 split): _____ hours
- Priority 3 (STAGE_5ac split): _____ hours
- Supporting materials: _____ hours
- Validation: _____ hours
**Total:** _____ hours (estimated 15-20 hours)

**Challenges encountered:**
[Document any issues or deviations]

**Additional improvements made:**
[Document any extra work beyond checklist]

**Recommendations for future:**
[Suggestions for maintaining guide quality]

---

**END OF PHASE 2 CHECKLIST**
