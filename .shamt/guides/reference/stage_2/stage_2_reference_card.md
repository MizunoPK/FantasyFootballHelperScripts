# S2: Feature Planning - Quick Reference Card

**Purpose:** One-page summary for quick consultation during S2
**Use Case:** Quick lookup when you need to remember guide details, gates, or decision points
**Total Time:** 2.25-4 hours per feature (2 phases: S2.P1 with 3 iterations, S2.P2 pairwise comparison)

---

## Sub-Stages Overview

```text
S2.P1: Spec Creation and Refinement (2.25-4 hours)
  Guide: s2_p1_spec_creation_refinement.md
  │
  ├─ I1: Feature-Level Discovery (60-90 min)
  │     • Read Discovery Context (DISCOVERY.md)
  │     • Reference previously completed features
  │     • Targeted Research (files, line numbers, code snippets)
  │     • Draft spec.md with requirements + traceability
  │     • Research Completeness Audit ← GATE 1 (MANDATORY)
  │
  ├─ I2: Checklist Resolution (45-90 min)
  │     • Resolve checklist questions ONE at a time with user
  │     • Update spec.md in real-time after each answer
  │
  └─ I3: Refinement & Alignment (30-60 min)
        • Dynamic Scope Adjustment (split if >35 items)
        • Cross-feature comparison with completed features
        • Spec-to-Epic Alignment Check ← GATE 2 (MANDATORY)
        • Acceptance Criteria + User Approval ← GATE 3
  ↓
  (Secondary agents STOP here — S2.P2 is Primary agent only)
  ↓
S2.P2: Cross-Feature Alignment (20-60 min)
  Guide: s2_p2_cross_feature_alignment.md
        • Pairwise comparison of all features' specs
        • Validation Loop for systematic cross-feature checks
        • Primary agent only
```

---

## Phase Summary Table

| Step | Name | Iteration | Duration | Key Output | Gate? |
|------|------|-----------|----------|------------|-------|
| 1 | Read Discovery Context | S2.P1.I1 | 15 min | Discovery Context section in spec.md | No |
| 2 | Targeted Research | S2.P1.I1 | 30-45 min | DISCOVERY.md with evidence (file paths, line numbers) | No |
| 3 | Draft spec.md with traceability | S2.P1.I1 | 15-20 min | spec.md + checklist.md with requirement sources | No |
| 4 | Research Completeness Audit | S2.P1.I1 | 20 min | Audit PASSED (4 categories) | ✅ Gate 1 |
| 5 | Checklist Resolution | S2.P1.I2 | 45-90 min | All questions resolved, spec updated in real-time | No |
| 6 | Scope Adjustment | S2.P1.I3 | 15 min | Feature split decision (if >35 items) | No |
| 7 | Cross-Feature Comparison | S2.P1.I3 | 15-30 min | Alignment with completed features | No |
| 8 | Spec-to-Epic Alignment Check | S2.P1.I3 | 15 min | Alignment check PASSED | ✅ Gate 2 |
| 9 | Acceptance Criteria & User Approval | S2.P1.I3 | 15-30 min | User approval obtained | ✅ Gate 3 |

---

## Mandatory Gates

### Gate 1: Research Completeness Audit (S2.P1.I1)
**Location:** stages/s2/s2_p1_spec_creation_refinement.md
**What it checks:**
- Component Research: Have you found the code mentioned in epic?
- Pattern Research: Have you studied similar features?
- Data Research: Have you located data sources?
- Discovery Context Knowledge: Did you review DISCOVERY.md during research?

**Pass Criteria:** ALL 4 categories answered with evidence (file paths, line numbers)
**If FAIL:** Return to S2.P1.I1, research gaps, re-run audit

### Gate 2: Spec-to-Epic Alignment Check (S2.P1.I3)
**Location:** stages/s2/s2_p1_spec_creation_refinement.md (I3)
**What it checks:**
- Scope Creep: Requirements NOT in epic notes
- Missing Requirements: Epic requests NOT in spec

**Pass Criteria:** Zero scope creep + zero missing requirements
**If FAIL:** Remove scope creep OR add missing requirements, re-run check

### Gate 3: User Checklist Approval (S2.P1.I3)
**Location:** stages/s2/s2_p1_spec_creation_refinement.md (I3)
**What it checks:**
- User explicitly approves spec.md (including acceptance criteria)
- User explicitly approves checklist.md (all questions answered)
- Zero autonomous agent resolution of checklist questions

**Pass Criteria:** User confirms approval of both spec.md and checklist.md
**If FAIL:** Revise spec/checklist based on user feedback, re-present for approval

---

## Decision Points

### Decision 1: Feature Splitting (S2.P1.I3)
**When:** Checklist >35 items
**Options:**
- Split into sub-features (recommended if >35 items)
- Keep as single feature (if complexity is low despite item count)

**How to decide:** Evaluate natural boundaries, ask user

### Decision 2: Question Resolution Strategy (S2.P1.I2)
**When:** Uncertain about requirements
**Options:**
- Ask user (ONE question at a time, wait for answer)
- Research codebase (if answerable from code/docs)
- Defer to implementation (if minor detail)

**How to decide:** If impacts design → ask user. If minor detail → defer

### Decision 3: Requirement Traceability Source (S2.P1.I1)
**For EACH requirement, cite source:**
- Epic: From epic notes (user's original request)
- User Answer: From user response to your question
- Derived: Logical consequence of Epic/User Answer

**Always cite the source** - enables verification in S2.P1.I3 (Gate 2)

---

## Common Pitfalls

### ❌ Pitfall 1: Skipping Discovery Context Review (I1 Step 1)
**Problem:** Starting research without re-reading epic first
**Impact:** Miss user's actual intent, research wrong things
**Solution:** ALWAYS re-read epic at S2.P1.I1 start, extract exact words

### ❌ Pitfall 2: Not Citing Sources for Requirements
**Problem:** Adding requirements without noting source (Epic/User/Derived)
**Impact:** S2.P1.I3 alignment check (Gate 2) fails (can't verify against epic)
**Solution:** For EVERY requirement, cite: Epic / User Answer / Derived

### ❌ Pitfall 3: Assuming Instead of Asking User
**Problem:** Making design decisions without user input
**Impact:** Implement wrong solution, rework in S7 QC
**Solution:** When uncertain, ask user in S2.P1.I2 (Checklist Resolution). Better to ask than assume

### ❌ Pitfall 4: Batching Questions
**Problem:** Asking user 5 questions at once
**Impact:** User overwhelmed, answers may be rushed/incomplete
**Solution:** ONE question at a time, wait for answer, ask next

### ❌ Pitfall 5: Shallow Research (No Evidence)
**Problem:** Saying "I researched X" without file paths/line numbers
**Impact:** S2.P1.I1 Gate 1 audit fails (no evidence = didn't actually research)
**Solution:** Document file paths, line numbers, code snippets for ALL research

### ❌ Pitfall 6: Scope Creep in Spec
**Problem:** Adding "nice-to-have" features not requested in epic
**Impact:** S2.P1.I3 alignment check (Gate 2) fails (scope creep detected)
**Solution:** Only include what epic/user explicitly requested

### ❌ Pitfall 7: Comparing to Wrong Features (S2.P1.I3)
**Problem:** Comparing to in-progress features instead of completed ones
**Impact:** Inherit bugs/inconsistencies from incomplete features
**Solution:** Only compare to features that completed S7 (fully QC'd)

---

## Quick Checklist: "Am I Ready for Next Iteration?"

**I1 → Gate 1 (Research Completeness Audit):**
- [ ] Re-read epic notes / DISCOVERY.md from scratch
- [ ] Extracted user's exact words to "Discovery Context" section
- [ ] Created DISCOVERY.md with file paths + line numbers for ALL research
- [ ] Found and READ components mentioned in epic
- [ ] Studied similar features in codebase
- [ ] Drafted spec.md with all known requirements + traceability sources

**Gate 1 → I2 (Checklist Resolution):**
- [ ] Research Completeness Audit PASSED (all 4 categories with evidence)
- [ ] checklist.md created with valid open questions (not research gaps)

**I2 → I3 (Refinement & Alignment):**
- [ ] All checklist questions resolved ONE at a time with user
- [ ] spec.md updated in real-time after each answer

**I3 → Gate 2 (Spec-to-Epic Alignment Check):**
- [ ] Feature split decision made (if checklist >35 items)
- [ ] Compared to completed features (alignment verified)
- [ ] Patterns consistent with rest of codebase

**Gate 2 → Gate 3 (User Checklist Approval):**
- [ ] Alignment check PASSED (zero scope creep + zero missing requirements)
- [ ] Acceptance criteria drafted

**Gate 3 → S2.P2 (or next feature):**
- [ ] User explicitly approved spec.md (including acceptance criteria)
- [ ] User explicitly approved checklist.md (all questions answered)
- [ ] Spec finalized with all sources cited

---

## File Outputs

**I1 (Feature-Level Discovery):**
- spec.md (Discovery Context section + initial requirements with traceability)
- epic/research/{FEATURE_NAME}_DISCOVERY.md (research findings with evidence)
- checklist.md (open questions identified during research)

**I2 (Checklist Resolution):**
- spec.md (updated in real-time after each user answer)
- checklist.md (resolved items marked)

**I3 (Refinement & Alignment):**
- spec.md (scope-adjusted, cross-feature aligned, acceptance criteria added)
- SPEC_SUMMARY.md (1-paragraph user-validated summary)

---

## When to Use Which Guide

| Current Phase | Guide to Read |
|---------------|---------------|
| Starting S2 | stages/s2/s2_p1_spec_creation_refinement.md |
| Mid-S2.P1 (any iteration — I1, I2, or I3) | stages/s2/s2_p1_spec_creation_refinement.md |
| Mid-S2.P2 | stages/s2/s2_p2_cross_feature_alignment.md |
| Need overview | stages/s2/s2_feature_deep_dive.md (router) |

---

## Exit Conditions

**S2 is complete when:**
- [ ] All phases executed (S2.P1 iterations 1-3, S2.P2 alignment)
- [ ] All 3 mandatory gates PASSED (Gate 1, Gate 2, Gate 3)
- [ ] spec.md has user-approved acceptance criteria
- [ ] checklist.md has zero unresolved items
- [ ] SPEC_SUMMARY.md created and user-validated

**Next Stage:** S3 (Epic-Level Docs, Tests, and Approval) - if all features planned
**OR:** S2 for next feature - if more features to plan

---

**Last Updated:** 2026-02-21
