# S2 Refinement Phase - Example Library (Router)

**Guide Version:** 2.0
**Last Updated:** 2026-02-05 (Restructured for improved navigation)
**Purpose:** Quick navigation to phase-specific refinement examples
**Prerequisites:** Read stages/s2/s2_p3_refinement.md first
**Main Guide:** stages/s2/s2_p3_refinement.md

---

## Purpose

This reference library provides detailed examples for executing **S2.P3: Refinement Phase**. The examples have been organized by phase for easier navigation and focused reference.

**How to Use This Library:**
1. Identify which phase you're currently executing in S2.P3
2. Click the link to the relevant phase-specific example file
3. Review examples relevant to your current task
4. Return to the main guide (s2_p3_refinement.md) to continue execution

**Always read the main guide first.** This library is a reference supplement, not a standalone guide.

---

## Phase 3: Interactive Question Resolution

**Example File:** [refinement_examples_phase3_questions.md](refinement_examples_phase3_questions.md)

**File Size:** 420 lines

**What's Covered:**
- Complete question-answer cycles (5+ detailed examples)
- Agent behavior patterns for different question types
- Immediate spec/checklist update protocols after receiving answers
- Common question patterns and anti-patterns
- Traceability and documentation of user answers
- Handling clarification requests and follow-up questions

**When to Use:**
- During S2.P3 Phase 3 when formulating questions for the user
- When updating specs and checklists after receiving user answers
- When evaluating if new questions emerged from user answers
- When verifying question resolution completeness

**Key Examples:**
- Example 1: Complete question-answer cycle (CSV column names)
- Example 2: User requests clarification (agent provides more context)
- Example 3: User suggests alternative approach (agent adapts)

---

## Phase 4: Dynamic Scope Adjustment

**Example File:** [refinement_examples_phase4_scope.md](refinement_examples_phase4_scope.md)

**File Size:** 223 lines

**What's Covered:**
- Feature too large - proposing splits to user with justification
- New work discovered during deep dive - evaluating separate feature vs expanded scope
- Scope reduction strategies and communication patterns
- Checklist item count thresholds and split triggers

**When to Use:**
- During S2.P3 Phase 4 when evaluating feature scope
- When checklist exceeds 35 items (split threshold)
- When discovering substantial new work not in original feature description
- When determining if work should be separate feature or part of current feature

**Key Examples:**
- Example 1: Feature too large (>35 items) - propose split with clear justification
- Example 2: New work discovered (player name matching utility) - create separate feature

---

## Phase 5: Cross-Feature Alignment

**Example File:** [refinement_examples_phase5_alignment.md](refinement_examples_phase5_alignment.md)

**File Size:** 365 lines

**What's Covered:**
- Complete pairwise feature comparison workflows
- Systematic comparison across 5 categories (components, data structures, requirements, assumptions, integration points)
- Conflict identification and resolution examples
- Clean alignment examples (no conflicts found)
- Conflict resolution strategies and user escalation patterns

**When to Use:**
- During S2.P3 Phase 5 when comparing current feature to all completed features
- When performing pairwise comparison with systematic category checks
- When identifying conflicts between features
- When resolving conflicts or escalating to user for decisions

**Key Examples:**
- Example 1: Complete feature comparison (Feature 01 vs Feature 02) with conflict resolution
- Example 2: Alignment without conflicts (Feature 02 vs Feature 03) - clean comparison

---

## Phase 6: Acceptance Criteria & User Approval

**Example File:** [refinement_examples_phase6_approval.md](refinement_examples_phase6_approval.md)

**File Size:** 477 lines

**What's Covered:**
- Comprehensive acceptance criteria templates for different feature types
- Complete acceptance criteria structure (behavior changes, files modified, data structures, API changes, testing, edge cases, documentation)
- User approval workflows (presenting for approval, handling feedback)
- Approval with modifications (user requests changes during approval)
- Final spec validation before S3 transition

**When to Use:**
- During S2.P3 Phase 6 when creating acceptance criteria for spec.md
- When preparing to present feature for Gate 3 (User Checklist Approval)
- When handling user approval feedback and iterations
- When finalizing spec.md before transitioning to S3

**Key Examples:**
- Example 1: Complete acceptance criteria (Feature 01: ADP Integration) - comprehensive template with all sections
- Example 2: User approval process (presentation → approval with minor modification → final approval)

---

## Quick Navigation

| Phase | Focus | Example File | Lines |
|-------|-------|--------------|-------|
| **Phase 3** | Interactive Question Resolution | [refinement_examples_phase3_questions.md](refinement_examples_phase3_questions.md) | 420 |
| **Phase 4** | Dynamic Scope Adjustment | [refinement_examples_phase4_scope.md](refinement_examples_phase4_scope.md) | 223 |
| **Phase 5** | Cross-Feature Alignment | [refinement_examples_phase5_alignment.md](refinement_examples_phase5_alignment.md) | 365 |
| **Phase 6** | Acceptance Criteria & User Approval | [refinement_examples_phase6_approval.md](refinement_examples_phase6_approval.md) | 477 |

**Total Examples:** 1,485 lines of detailed examples across 4 phase-specific files

---

## Success Criteria Summary

**Refinement Phase (S2.P3) passes when:**

✅ **Phase 3 (Interactive Question Resolution):**
- All checklist questions resolved (zero open items)
- Each question asked ONE AT A TIME
- Spec and checklist updated IMMEDIATELY after each answer
- New questions evaluated after each answer
- User answers documented verbatim or paraphrased

✅ **Phase 4 (Dynamic Scope Adjustment):**
- Checklist item count documented
- If >35 items: Split proposed to user, user decided
- If new work discovered: Evaluated (new feature vs expanded scope)
- Scope adjustments documented

✅ **Phase 5 (Cross-Feature Alignment):**
- Compared to ALL features with "S2 Complete"
- Systematic pairwise comparison performed
- Conflicts identified (if any)
- Conflicts resolved or user consulted
- Alignment verification documented in spec.md

✅ **Phase 6 (Acceptance Criteria & User Approval):**
- Acceptance Criteria section created in spec.md
- Complete coverage: behavior, files, structures, API, tests, edge cases, docs
- Presented to user for approval
- User APPROVED (explicit confirmation)
- Approval checkbox marked [x]
- Approval timestamp documented

**Ready for next feature or S3 when all phases complete with user approval.**

---

## Navigation Back to Main Guide

**Return to:** [stages/s2/s2_p3_refinement.md](../../stages/s2/s2_p3_refinement.md)

**See Also:**
- [S2.P1: Research Phase Examples](research_examples.md)
- [S2.P2: Specification Phase Examples](specification_examples.md)

---

*Refinement examples library restructured 2026-02-05 for improved navigation and focused reference.*
