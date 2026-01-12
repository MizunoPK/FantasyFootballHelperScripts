# STAGE 2: Feature Deep Dive - Quick Reference Card

**Purpose:** One-page summary for quick consultation during Stage 2
**Use Case:** Quick lookup when you need to remember phase details, gates, or decision points
**Total Time:** 2-3 hours per feature (9 phases across 3 sub-stages)

---

## Sub-Stages Overview

```
Phase 2.1: Research Phase (45-60 min)
    Phase 0: Epic Intent Extraction (15 min)
    Phase 1: Targeted Research (30 min)
    Phase 1.5: Research Completeness Audit (20 min) ← MANDATORY GATE
    ↓
Phase 2.2: Specification Phase (30-45 min)
    Phase 2: Update Spec & Checklist (30 min)
    Phase 2.5: Spec-to-Epic Alignment Check (15 min) ← MANDATORY GATE
    ↓
Phase 2.3: Refinement Phase (45-60 min)
    Phase 3: Interactive Question Resolution (30-90 min)
    Phase 4: Dynamic Scope Adjustment (15 min)
    Phase 5: Cross-Feature Alignment (15-30 min)
    Phase 6: Acceptance Criteria & User Approval (15-30 min) ← MANDATORY
```

---

## Phase Summary Table

| Phase | Name | Sub-Stage | Duration | Key Output | Gate? |
|-------|------|-----------|----------|------------|-------|
| 0 | Epic Intent Extraction | 2a | 15 min | Epic Intent section in spec.md | No |
| 1 | Targeted Research | 2a | 30 min | DISCOVERY.md with evidence | No |
| 1.5 | Research Completeness Audit | 2a | 20 min | Audit PASSED (4 categories) | ✅ YES |
| 2 | Update Spec & Checklist | 2b | 30 min | spec.md + checklist.md with traceability | No |
| 2.5 | Spec-to-Epic Alignment Check | 2b | 15 min | Alignment check PASSED | ✅ YES |
| 3 | Interactive Question Resolution | 2c | 30-90 min | Resolved questions, updated spec | No |
| 4 | Dynamic Scope Adjustment | 2c | 15 min | Feature split decision (if >35 items) | No |
| 5 | Cross-Feature Alignment | 2c | 15-30 min | Alignment with completed features | No |
| 6 | Acceptance Criteria & User Approval | 2c | 15-30 min | User approval obtained | ✅ YES |

---

## Mandatory Gates

### Gate 1: Phase 1.5 - Research Completeness Audit
**Location:** stages/stage_2/phase_2.1_research.md
**What it checks:**
- Component Research: Have you found the code mentioned in epic?
- Pattern Research: Have you studied similar features?
- Data Research: Have you located data sources?
- Epic Research: Did you re-read epic notes during research?

**Pass Criteria:** ALL 4 categories answered with evidence (file paths, line numbers)
**If FAIL:** Return to Phase 1, research gaps, re-run audit

### Gate 2: Phase 2.5 - Spec-to-Epic Alignment Check
**Location:** stages/stage_2/phase_2.2_specification.md
**What it checks:**
- Scope Creep: Requirements NOT in epic notes
- Missing Requirements: Epic requests NOT in spec

**Pass Criteria:** Zero scope creep + zero missing requirements
**If FAIL:** Remove scope creep OR add missing requirements, re-run check

### Gate 3: Phase 6 - User Approval
**Location:** stages/stage_2/phase_2.3_refinement.md
**What it checks:**
- User explicitly approves acceptance criteria

**Pass Criteria:** User confirmation documented
**If FAIL:** Revise acceptance criteria, get user approval

---

## Decision Points

### Decision 1: Feature Splitting (Phase 4)
**When:** Checklist >35 items
**Options:**
- Split into sub-features (recommended if >35 items)
- Keep as single feature (if complexity is low despite item count)

**How to decide:** Evaluate natural boundaries, ask user

### Decision 2: Question Resolution Strategy (Phase 3)
**When:** Uncertain about requirements
**Options:**
- Ask user (ONE question at a time, wait for answer)
- Research codebase (if answerable from code/docs)
- Defer to implementation (if minor detail)

**How to decide:** If impacts design → ask user. If minor detail → defer

### Decision 3: Requirement Traceability Source (Phase 2)
**For EACH requirement, cite source:**
- Epic: From epic notes (user's original request)
- User Answer: From user response to your question
- Derived: Logical consequence of Epic/User Answer

**Always cite the source** - enables verification in Phase 2.5

---

## Common Pitfalls

### ❌ Pitfall 1: Skipping Phase 0 (Epic Intent Extraction)
**Problem:** Starting research without re-reading epic first
**Impact:** Miss user's actual intent, research wrong things
**Solution:** ALWAYS re-read epic in Phase 0, extract exact words

### ❌ Pitfall 2: Not Citing Sources for Requirements
**Problem:** Adding requirements without noting source (Epic/User/Derived)
**Impact:** Phase 2.5 alignment check fails (can't verify against epic)
**Solution:** For EVERY requirement, cite: Epic / User Answer / Derived

### ❌ Pitfall 3: Assuming Instead of Asking User
**Problem:** Making design decisions without user input
**Impact:** Implement wrong solution, rework in Stage 5c QC
**Solution:** When uncertain, ask user (Phase 3). Better to ask than assume

### ❌ Pitfall 4: Batching Questions
**Problem:** Asking user 5 questions at once
**Impact:** User overwhelmed, answers may be rushed/incomplete
**Solution:** ONE question at a time, wait for answer, ask next

### ❌ Pitfall 5: Shallow Research (No Evidence)
**Problem:** Saying "I researched X" without file paths/line numbers
**Impact:** Phase 1.5 audit fails (no evidence = didn't actually research)
**Solution:** Document file paths, line numbers, code snippets for ALL research

### ❌ Pitfall 6: Scope Creep in Spec
**Problem:** Adding "nice-to-have" features not requested in epic
**Impact:** Phase 2.5 alignment check fails (scope creep detected)
**Solution:** Only include what epic/user explicitly requested

### ❌ Pitfall 7: Comparing to Wrong Features (Phase 5)
**Problem:** Comparing to in-progress features instead of completed ones
**Impact:** Inherit bugs/inconsistencies from incomplete features
**Solution:** Only compare to features that completed Stage 5c (fully QC'd)

---

## Quick Checklist: "Am I Ready for Next Phase?"

**Phase 0 → Phase 1:**
- [ ] Re-read epic notes from scratch
- [ ] Extracted user's exact words to "Epic Intent" section
- [ ] Listed components mentioned in epic

**Phase 1 → Phase 1.5:**
- [ ] Created DISCOVERY.md file
- [ ] Documented file paths + line numbers for ALL research
- [ ] Found components mentioned in epic
- [ ] Studied similar features in codebase

**Phase 1.5 → Phase 2:**
- [ ] Research Completeness Audit PASSED (all 4 categories)
- [ ] Have evidence for component/pattern/data/epic research

**Phase 2 → Phase 2.5:**
- [ ] spec.md has all requirements with traceability (Epic/User/Derived)
- [ ] checklist.md created with open questions
- [ ] Every requirement cites source

**Phase 2.5 → Phase 3:**
- [ ] Alignment check PASSED (zero scope creep + zero missing requirements)
- [ ] Spec matches epic exactly

**Phase 3 → Phase 4:**
- [ ] All questions resolved (or documented in checklist)
- [ ] Spec updated based on user answers

**Phase 4 → Phase 5:**
- [ ] Feature split decision made (if checklist >35 items)
- [ ] Scope is manageable

**Phase 5 → Phase 6:**
- [ ] Compared to completed features (alignment verified)
- [ ] Patterns consistent with rest of codebase

**Phase 6 → Next Feature or Stage 3:**
- [ ] Acceptance criteria created
- [ ] User approval obtained
- [ ] Spec finalized

---

## File Outputs

**Phase 0:**
- spec.md (Epic Intent section)

**Phase 1:**
- epic/research/{FEATURE_NAME}_DISCOVERY.md

**Phase 2:**
- spec.md (complete with requirements + traceability)
- checklist.md (open questions)

**Phase 2.5:**
- spec.md (verified against epic)

**Phase 3:**
- spec.md (updated based on user answers)
- checklist.md (resolved items)

**Phase 6:**
- spec.md (with acceptance criteria)
- SPEC_SUMMARY.md (1-paragraph user-validated summary)

---

## When to Use Which Guide

| Current Phase | Guide to Read |
|---------------|---------------|
| Starting Stage 2 | stages/stage_2/phase_2.1_research.md |
| Phase 0, 1, or 1.5 | stages/stage_2/phase_2.1_research.md |
| Phase 2 or 2.5 | stages/stage_2/phase_2.2_specification.md |
| Phase 3, 4, 5, or 6 | stages/stage_2/phase_2.3_refinement.md |
| Need overview | stages/stage_2/feature_deep_dive.md (router) |

---

## Exit Conditions

**Stage 2 is complete when:**
- [ ] All 9 phases executed (0 through 6)
- [ ] All 3 mandatory gates PASSED (1.5, 2.5, 6)
- [ ] spec.md has user-approved acceptance criteria
- [ ] checklist.md has zero unresolved items
- [ ] SPEC_SUMMARY.md created and user-validated

**Next Stage:** Stage 3 (Cross-Feature Sanity Check) - if all features planned
**OR:** Stage 2 for next feature - if more features to plan

---

**Last Updated:** 2026-01-02
