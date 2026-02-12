# Guide Update Proposal: S5 v1→v2 Terminology Migration

**Created:** 2026-02-12
**Source:** Post-Audit Round 2 Finding (Guide Audit Round 2, Sub-Round 2.1, D2 Terminology Consistency)
**Priority:** P0 (Critical)
**Effort Estimate:** 2-3 hours
**Status:** Pending User Approval

---

## Executive Summary

**Problem:** 16 reference/support files still use S5 v1 terminology (22 iterations, Rounds 1-3) while stage guides use S5 v2 (Draft Creation + Validation Loop with 11 dimensions).

**Impact:** Agents reading CLAUDE.md → reference files encounter outdated concepts (Iteration 21, Round 3) that conflict with current S5 v2 workflow, causing confusion and potential workflow errors.

**Solution:** Systematic migration of ~100+ iteration references to S5 v2 dimension/phase terminology across 16 files.

---

## Problem Statement

### Discovery Context

**Source:** Guide audit Round 2, Sub-Round 2.1 (Core Dimensions)
**Dimension:** D2 (Terminology Consistency)
**Scope:** Cross-file terminology validation

### The Issue

While stage guides correctly use S5 v2 terminology:
- `stages/s5/s5_v2_validation_loop.md` - Phase 1 (Draft Creation) + Phase 2 (Validation Loop with 11 dimensions)
- `stages/s1/s1_epic_planning.md` - References "Dimension 11: Spec Alignment"
- `stages/s10/s10_p1_guide_update_workflow.md` - Uses S5 v2 examples

Reference and support files still use S5 v1 terminology:
- `reference/mandatory_gates.md` - "Iteration 21 (Spec Validation Against Validated Documents)"
- `reference/glossary.md` - Defines "Iteration 22", "GO Decision (Iteration 22)"
- `templates/feature_readme_template.md` - Checklist items for "Iteration 20 PASSED"

### Real-World Impact

**Agent Confusion Scenario:**
```text
1. Agent reads CLAUDE.md: "See reference/mandatory_gates.md for gate details"
2. Agent opens mandatory_gates.md: "Gate 3: Iteration 21 - Spec Validation"
3. Agent checks current S5 guide: No "Iteration 21" exists
4. Agent confused: "Did I skip this? Is this outdated? What should I do?"
```

**Template Mismatch Scenario:**
```text
1. Agent creates implementation_plan.md from template
2. Template has: "□ Iteration 20: Pre-Implementation Spec Audit (ALL 4 PARTS PASSED)"
3. S5 v2 has no "Iteration 20" - just Validation Loop dimensions
4. Agent unsure: How to mark this complete? Should I skip it?
```

### Historical Context

**When S5 v2 was created:** Stage guides were updated to new structure
**What was missed:** Reference files, templates, prompts, and support documentation
**Why it matters now:** CLAUDE.md actively points agents to these outdated files

---

## S5 v1 → S5 v2 Concept Mapping

### Core Terminology Changes

| S5 v1 (OLD) | S5 v2 (NEW) | Context |
|-------------|-------------|---------|
| 22 iterations | Variable rounds (6-8 typical) | Total validation cycles |
| Round 1 (Iterations 1-7) | Phase 1 (Draft Creation) | Initial plan creation |
| Round 2 (Iterations 8-13) | Phase 2 Rounds 1-N | Validation Loop |
| Round 3 (Iterations 14-22) | Phase 2 continued | Until 3 consecutive clean |
| Iteration 2 | Dimension 2 | Interface & Dependency Verification |
| Iteration 4 | Dimension 3 | Algorithm Traceability |
| Iteration 7 | Dimension 7 | Integration & Compatibility |
| Iteration 9 | Dimension 6 | Error Handling & Edge Cases |
| Iteration 20 | Part of Validation Loop | Multiple dimensions checked |
| Iteration 21 | Dimension 11 | Spec Alignment & Cross-Validation |
| Iteration 22 | Phase 2 complete | 3 consecutive clean rounds achieved |
| Gate 4a | Part of Dimension 4 | Task Specification Quality |
| Gate 23a (Iteration 20) | Validation Loop | Pre-Implementation readiness |
| Gate 25 (Iteration 21) | Dimension 11 validation | Spec alignment check |

### Key Conceptual Shifts

**S5 v1 Fixed Sequence:**
```text
Always 22 iterations → Always 3 rounds → Predictable structure
Iteration 20 always happens → Gate 23a at fixed point
```

**S5 v2 Adaptive Validation:**
```text
Variable rounds until clean → 6-8 typical, max 10 → Exit when 3 consecutive clean
All 11 dimensions checked EVERY round → Not tied to specific iteration numbers
```

---

## Affected Files (16 Total)

### Tier 1: Critical (Referenced by CLAUDE.md)

**1. reference/mandatory_gates.md**
- **References:** 40+ (Iterations 20, 21, 22; Gates 23a, 25; Round 3)
- **CLAUDE.md link:** Line 462 - "See reference/mandatory_gates.md for complete gate reference"
- **Impact:** HIGH - Agents directed here for gate definitions
- **Changes needed:**
  - Rename "Gate 3: Iteration 21" → "Dimension 11: Spec Alignment & Cross-Validation"
  - Update "Gate 23a (Iteration 20)" → "Validation Loop Readiness Checks"
  - Replace "Iteration 22 GO/NO-GO" → "Phase 2 Complete (3 consecutive clean rounds)"
  - Rewrite all gate timing references from iterations to dimensions

**2. reference/glossary.md**
- **References:** 8+ definitions (Iteration 21, 22, GO Decision, NO-GO)
- **CLAUDE.md link:** Line 54 - "See glossary.md for complete term definitions"
- **Impact:** HIGH - Primary terminology reference
- **Changes needed:**
  - Remove definitions: "Iteration 20", "Iteration 21", "Iteration 22"
  - Add definitions: "Dimension 11", "Validation Loop", "Phase 1 (Draft Creation)", "Phase 2 (Validation Loop)"
  - Update cross-references from iterations to dimensions

### Tier 2: High Priority (Active Workflow Files)

**3. prompts/s5_s8_prompts.md**
- **References:** 2 (Iteration 22 in example prompts)
- **Impact:** HIGH - Used during S5 phase transitions
- **Changes needed:**
  - Update "Starting S5" prompt to reference Phase 1 (Draft Creation)
  - Update "S5 Complete" prompt to reference Phase 2 (Validation Loop complete)
  - Remove "Iteration 22: Implementation Readiness = PASSED" from examples

**4. templates/feature_readme_template.md**
- **References:** 2 (Iteration 20, Iteration 22 in checklist)
- **Impact:** HIGH - Used for all features
- **Changes needed:**
  - Replace "□ Iteration 20: Pre-Implementation Spec Audit" → "□ Validation Loop complete (3 consecutive clean rounds)"
  - Replace "□ Iteration 22: Implementation Readiness PASSED" → "□ All 11 dimensions validated"

**5. templates/spec_summary_template.md**
- **References:** 1 (Iteration 21 in usage note)
- **Impact:** MEDIUM - Created during S2
- **Changes needed:**
  - Update "During Iteration 21 (Spec Validation)" → "During S5 Dimension 11 validation"

**6. templates/epic_ticket_template.md**
- **References:** 1 (Iteration 21 in usage note)
- **Impact:** MEDIUM - Created during S1
- **Changes needed:**
  - Update "During Iteration 21 (Spec Validation)" → "During S5 Dimension 11 validation"

**7. reference/faq_troubleshooting.md**
- **References:** 12+ (Iterations 20, 21, 22; Rounds; Decision trees)
- **Impact:** MEDIUM - Referenced when agents are stuck
- **Changes needed:**
  - Section "What if Iteration 22 says NO-GO?" → "What if Validation Loop not converging?"
  - Update all iteration-based decision trees to dimension-based
  - Rewrite "Stuck 3: Iteration 22 NO-GO" protocol

### Tier 3: Medium Priority (Reference Documentation)

**8. reference/implementation_orchestration.md**
- **References:** 3 (Iteration 22, Round 3)
- **Changes:** Update orchestration examples to Phase 1/Phase 2 workflow

**9. reference/common_mistakes.md**
- **References:** 1 ("Begin Round 2 Iteration 8" example)
- **Changes:** Update example to "Begin Validation Round 4 - Dimension 6"

**10. reference/guide_update_tracking.md**
- **References:** 2 (Iteration 21 in historical lesson)
- **Changes:** Update historical context to Dimension 11

**11. reference/stage_5/stage_5_reference_card.md**
- **References:** 3 (Iteration 21 in pitfalls section)
- **Changes:** Rewrite pitfall examples using dimension terminology

**12. debugging/loop_back.md**
- **References:** 1 ("S5 Round 2, Iteration 9" example)
- **Changes:** Update example to "S5 Validation Round 4 - Dimension 6"

**13. debugging/root_cause_analysis.md**
- **References:** 5 (Iterations 4, 7, 9, 15, 20 in analysis questions)
- **Changes:** Map iterations to dimensions in root cause checklist

**14. reference/stage_10/lessons_learned_examples.md**
- **References:** 2 (Iteration 20 in examples)
- **Changes:** Update example lessons to use dimension terminology

**15. templates/pr_review_issues_template.md**
- **References:** 2 ("Round 2: Comprehensive Review (Iteration 1)")
- **Changes:** Update round labeling to match current workflow

**16. audit/reference/known_exceptions.md**
- **References:** 3 (Iteration 20, 21, 22 in exception types)
- **Changes:** Update exception type definitions to dimension-based

---

## Proposed Changes - Detailed Examples

### Example 1: reference/mandatory_gates.md (CRITICAL)

**Current State (BEFORE):**
```markdown
### Gate 3: Iteration 21 - Spec Validation Against Validated Documents (CRITICAL)

**When:** S5 Round 3, Iteration 21 (after Iteration 20 passed)

**What it checks:**
- Spec.md matches ALL three user-validated sources:
  1. Epic notes (user's original request)
  2. Epic ticket (user-validated outcomes from S1)
  3. Spec summary (user-validated feature outcomes from S2)

**How to execute:**
1. Open spec.md in one window
2. Open epic notes, epic ticket, spec summary in other windows
3. Compare each spec section against all three sources
4. Document discrepancies in Iteration 21 audit section

**Pass criteria:**
- 100% alignment OR user approves discrepancies

**If FAILED:**
- Cannot proceed to Iteration 22
- Must resolve all discrepancies first
```

**Proposed Change (AFTER):**
```markdown
### Dimension 11: Spec Alignment & Cross-Validation (CRITICAL)

**When:** S5 v2 Phase 2 (Validation Loop) - Checked EVERY validation round

**What it checks:**
- Implementation_plan.md aligns with spec.md
- Spec.md was validated against all three user-validated sources:
  1. Epic notes (user's original request)
  2. Epic ticket (user-validated outcomes from S1)
  3. Spec summary (user-validated feature outcomes from S2)

**How to execute:**
1. Read implementation_plan.md completely
2. Verify every task traces to spec.md requirement
3. Verify no spec.md requirements missing from plan
4. Cross-check spec.md consistency with epic sources

**Pass criteria:**
- 100% alignment between implementation_plan.md and spec.md
- All spec.md sections addressed in implementation tasks

**If FAILED:**
- Add to VALIDATION_LOOP_LOG.md
- Fix immediately (zero deferred issues)
- Re-run validation round
- Need 3 consecutive clean rounds to exit Phase 2
```

**Rationale:**
- Dimension 11 is checked EVERY validation round, not just once at "Iteration 21"
- S5 v2 validates implementation_plan.md against spec.md (not spec.md against sources - that's S2 work)
- Failures don't block a single iteration - they trigger another validation round
- Exit criteria is "3 consecutive clean rounds" not "pass Iteration 21"

---

### Example 2: templates/feature_readme_template.md

**Current State (BEFORE):**
```markdown
## S5: Implementation Planning Checklist

- [ ] Round 1 complete (Iterations 1-7)
- [ ] Round 2 complete (Iterations 8-13)
- [ ] Round 3 complete (Iterations 14-22)
- [ ] Iteration 20: Pre-Implementation Spec Audit (ALL 4 PARTS PASSED)
- [ ] Iteration 22: Implementation Readiness PASSED
- [ ] Gate 5: User approved implementation_plan.md
```

**Proposed Change (AFTER):**
```markdown
## S5 v2: Implementation Planning Checklist

- [ ] Phase 1: Draft Creation complete (~70% quality baseline)
- [ ] Phase 2: Validation Loop started
  - [ ] Validation rounds executed: {count}
  - [ ] All 11 dimensions validated every round
  - [ ] 3 consecutive clean rounds achieved: ✅
- [ ] Implementation_plan.md completeness: 100%
- [ ] All spec.md requirements have implementation tasks
- [ ] Gate 5: User approved implementation_plan.md
```

**Rationale:**
- Removes fixed iteration/round structure (no longer valid in S5 v2)
- Focuses on Phase 1/Phase 2 completion
- Tracks validation rounds dynamically (not fixed 22 iterations)
- Emphasizes "3 consecutive clean rounds" exit criteria

---

### Example 3: reference/glossary.md

**Current Definitions (REMOVE):**
```markdown
**Iteration 20**
Pre-Implementation Spec Audit gate in S5 Round 3. Four-part validation (completeness, specificity, interface contracts, integration).

**See:** Gate 23a, S5 Round 3

**Iteration 21**
Spec Validation Against Validated Documents in S5 Round 3. Three-way comparison of spec.md against epic notes, epic ticket, and spec summary.

**See:** Gate 25, Three-Way Validation

**Iteration 22**
GO/NO-GO decision point in S5 Round 3. Final implementation readiness check before proceeding to S6.

**See:** GO Decision, NO-GO, Gates
```

**New Definitions (ADD):**
```markdown
**Phase 1 (Draft Creation)**
S5 v2 first phase where implementation_plan.md is drafted in 60-90 minutes to ~70% quality baseline. Creates all 11 dimension sections with initial content.

**See:** S5 v2, Draft Creation, Validation Loop

**Phase 2 (Validation Loop)**
S5 v2 second phase where implementation_plan.md is systematically refined through validation rounds. Each round checks all 18 dimensions (7 master + 11 S5-specific). Exit after 3 consecutive clean rounds.

**See:** S5 v2, Validation Loop, 11 Dimensions

**Dimension 11: Spec Alignment & Cross-Validation**
S5 v2 validation dimension ensuring implementation_plan.md aligns 100% with spec.md. Checks that all spec requirements have implementation tasks and no spec sections are missed.

**See:** S5 v2 Validation Loop, Spec Validation

**Validation Loop (S5 v2)**
Iterative refinement process in S5 Phase 2. Each round checks all 18 dimensions, finds issues, fixes immediately, and re-runs until 3 consecutive rounds find zero issues. Typical: 6-8 rounds, max 10 rounds.

**See:** Phase 2, 11 Dimensions, 3 Consecutive Clean Rounds

**3 Consecutive Clean Rounds**
S5 v2 exit criteria for Validation Loop. Requires 3 validation rounds in a row where all 18 dimensions pass with zero issues found.

**See:** Validation Loop, Phase 2 Complete
```

---

### Example 4: prompts/s5_s8_prompts.md

**Current Prompt (BEFORE):**
```markdown
### Starting S5 (Implementation Planning)

I acknowledge:
- ✅ Read complete guide: stages/s5/s5_implementation_planning.md
- ✅ Prerequisites verified: S4 complete, spec.md complete, checklist.md resolved
- ✅ Ready to begin Round 1, Iteration 1
- ✅ Will execute all 22 iterations across 3 rounds
- ✅ Will pass mandatory gates: 4a, 23a (Iteration 20), 25 (Iteration 21)
- ✅ Will achieve GO decision at Iteration 22 before requesting user approval

Starting S5 implementation planning now.
```

**Proposed Prompt (AFTER):**
```markdown
### Starting S5 v2 (Implementation Planning)

I acknowledge:
- ✅ Read complete guide: stages/s5/s5_v2_validation_loop.md
- ✅ Prerequisites verified: S4 complete, spec.md complete, checklist.md resolved
- ✅ Understanding S5 v2 structure: Phase 1 (Draft Creation) + Phase 2 (Validation Loop)
- ✅ Ready to begin Phase 1: Draft implementation_plan.md to ~70% quality
- ✅ Will execute Phase 2: Validate across 11 dimensions until 3 consecutive clean rounds
- ✅ Typical: 6-8 validation rounds, max 10 rounds before escalation
- ✅ Will achieve Phase 2 complete (3 consecutive clean rounds) before requesting user approval

Starting S5 v2 implementation planning now.
```

---

## Implementation Strategy

### Approach: Systematic File-by-File Migration

**Phase 1: Critical Files (1-2 hours)**
1. reference/mandatory_gates.md - Rewrite all gate definitions
2. reference/glossary.md - Remove old, add new definitions
3. prompts/s5_s8_prompts.md - Update all S5 prompts
4. templates/feature_readme_template.md - Update checklist

**Phase 2: High Priority Templates (30-45 min)**
5. templates/spec_summary_template.md - Update usage note
6. templates/epic_ticket_template.md - Update usage note
7. reference/faq_troubleshooting.md - Rewrite S5-related FAQs

**Phase 3: Medium Priority References (30-45 min)**
8-14. Update remaining reference files with dimension terminology

**Phase 4: Audit References (15 min)**
15-16. Update audit/reference files for future consistency

### Quality Assurance

**After each file update:**
1. Search for remaining iteration references: `grep -n "Iteration [0-9]" {file}`
2. Verify S5 v2 concepts used correctly
3. Check cross-references still valid

**After all files updated:**
1. Run grep across all files: `grep -r "Iteration 2[012]" reference/ templates/ prompts/`
2. Should return ZERO matches
3. Verify new terminology used consistently

---

## Risk Assessment

### Risks

**Risk 1: Breaking Cross-References**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Systematic review of all internal file links after updates

**Risk 2: Introducing New Inconsistencies**
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Use consistent mapping table, review all changes before committing

**Risk 3: Missing Some Iteration References**
- **Probability:** Low
- **Impact:** Low
- **Mitigation:** Automated grep verification after completion

### Benefits

**Benefit 1: Eliminate Agent Confusion**
- Reference files match stage guides - no conflicting terminology
- Templates align with current workflow
- CLAUDE.md → reference files → consistent messaging

**Benefit 2: Enable Future Updates**
- All S5 documentation uses same terminology foundation
- Future S5 improvements don't need "find all old references" cleanup

**Benefit 3: Professional Documentation Quality**
- No outdated concepts lingering in reference materials
- Clear, consistent terminology across all guides

---

## Success Criteria

**Completion Checklist:**

- [ ] All 16 files updated with S5 v2 terminology
- [ ] Zero matches for: `grep -r "Iteration 2[012]" reference/ templates/ prompts/ debugging/`
- [ ] Zero matches for: `grep -r "Round [123].*Iteration" reference/ templates/`
- [ ] All new terminology uses consistent mapping (per table above)
- [ ] Cross-references verified (no broken links)
- [ ] Glossary definitions updated (old removed, new added)
- [ ] CLAUDE.md references point to updated content
- [ ] Agent Status updated in EPIC_README.md

**Verification Commands:**
```bash
# Should return 0 matches
grep -r "Iteration 20" reference/ templates/ prompts/ debugging/
grep -r "Iteration 21" reference/ templates/ prompts/ debugging/
grep -r "Iteration 22" reference/ templates/ prompts/ debugging/
grep -r "Round [123].*Iteration" reference/ templates/

# Should return multiple matches (new terminology)
grep -r "Dimension 11" reference/ templates/ prompts/
grep -r "Phase 2.*Validation Loop" reference/ templates/
grep -r "3 consecutive clean rounds" reference/ templates/
```

---

## Timeline

**Total Effort:** 2-3 hours

**Breakdown:**
- Phase 1 (Critical files): 1-2 hours
- Phase 2 (High priority): 30-45 min
- Phase 3 (Medium priority): 30-45 min
- Phase 4 (Audit files): 15 min
- Verification & QA: 15-30 min

**Dependencies:** None - can start immediately after user approval

---

## User Decision

**Priority:** P0 (Critical)

**Recommendation:** APPROVE - Critical for terminology consistency

**Options:**
- [ ] **APPROVE** - Proceed with systematic S5 v1→v2 migration across all 16 files
- [ ] **MODIFY** - Apply to subset of files only (specify which tier/files)
- [ ] **DEFER** - Document for future, accept current inconsistency
- [ ] **DISCUSS** - Questions or concerns about approach

**User Feedback:**
```
{User response here}
```

---

## Post-Approval Next Steps

**If approved:**
1. Execute Phase 1-4 file updates systematically
2. Run verification commands after each phase
3. Update EPIC_README.md Agent Status with progress
4. Create commit: "docs/guides: Migrate S5 v1→v2 terminology across reference files"
5. Report completion with verification results

**If modified:**
- Apply changes only to specified files
- Document remaining files for future update

**If deferred:**
- Add to guides_v2/TODO.md for future work
- Accept known inconsistency between stage guides and reference files
