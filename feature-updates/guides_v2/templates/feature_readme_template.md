# Feature Readme Template

**Filename:** `README.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/feature_XX_{name}/README.md`
**Created:** {YYYY-MM-DD}
**Updated:** Throughout feature implementation (Stages 2-5e)

**Purpose:** Central tracking document for a single feature, containing Agent Status, progress tracker, and feature-specific context.

---

## Template

```markdown
# Feature: {feature_name}

**Created:** {YYYY-MM-DD}
**Status:** {Stage X complete}

---

## Feature Context

**Part of Epic:** {epic_name}
**Feature Number:** {N} of {total}
**Created:** {YYYY-MM-DD}

**Purpose:**
{1-2 sentence description of what this feature does and why it's needed}

**Dependencies:**
- **Depends on:** {List features this depends on, or "None"}
- **Required by:** {List features that depend on this, or "Unknown yet" or "None"}

**Integration Points:**
- {Other features this integrates with, or "None (standalone feature)"}

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** {PLANNING / IMPLEMENTATION_PLANNING / IMPLEMENTATION / POST_IMPLEMENTATION / COMPLETE}
**Current Step:** {Specific step - e.g., "Iteration 12/24", "QC Round 2"}
**Current Guide:** `{guide_name}.md`
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** {X/Y items complete}
**Next Action:** {Exact next task - e.g., "Complete Iteration 13: Integration Gap Check"}
**Blockers:** {List any issues or "None"}

---

## Feature Stages Progress

**S2 - Feature Deep Dive:**
- [ ] `spec.md` created and complete
- [ ] `checklist.md` created (all items resolved or marked pending)
- [ ] `lessons_learned.md` created
- [ ] README.md created (this file)
- [ ] S2 complete: {✅/◻️}

**S5 - Implementation Planning:**
- [ ] 28 verification iterations complete
- [ ] Iteration 4a: TODO Specification Audit PASSED
- [ ] Iteration 23a: Pre-Implementation Spec Audit (ALL 4 PARTS PASSED)
- [ ] Iteration 24: Implementation Readiness PASSED
- [ ] `implementation_plan.md` created and user-approved
- [ ] `questions.md` created (or documented "no questions")
- [ ] S5 complete: {✅/◻️}

**S6 - Implementation Execution:**
- [ ] All implementation tasks complete
- [ ] All unit tests passing (100%)
- [ ] `implementation_checklist.md` created and all verified
- [ ] S6 complete: {✅/◻️}

**S7 - Implementation Testing & Review:**
- [ ] Smoke testing (3 parts) passed
- [ ] QC Round 1 passed
- [ ] QC Round 2 passed
- [ ] QC Round 3 passed
- [ ] PR Review (11 categories) passed
- [ ] `lessons_learned.md` updated with S7 insights
- [ ] S7 complete: {✅/◻️}

**S8.P1 - Cross-Feature Alignment:**
- [ ] Reviewed all remaining feature specs
- [ ] Updated remaining specs based on THIS feature's actual implementation
- [ ] Documented features needing rework (or "none")
- [ ] No significant rework needed for other features
- [ ] S8.P1 complete: {✅/◻️}

**S8.P2 - Epic Testing Plan Update:**
- [ ] `epic_smoke_test_plan.md` reviewed
- [ ] Test scenarios updated based on actual implementation
- [ ] Integration points added to epic test plan
- [ ] Update History table in epic test plan updated
- [ ] S8.P2 complete: {✅/◻️}

---

## Files in this Feature

**Core Files:**
- `README.md` - This file (feature overview and status)
- `spec.md` - **Primary specification** (detailed requirements)
- `checklist.md` - Tracks resolved vs pending decisions
- `lessons_learned.md` - Feature-specific insights

**Planning Files (S5):**
- `implementation_plan.md` - Implementation build guide (created in S5, user-approved)
- `questions.md` - Questions for user (created in S5, or documented "no questions")

**Implementation Files (S6):**
- `implementation_checklist.md` - Continuous spec verification during coding

**Research Files (if needed):**
- `research/` - Directory containing research documents

---

## Feature-Specific Notes

{Optional section for any feature-specific context, gotchas, or important notes}

{Example:}
**Design Decisions:**
- {Decision 1 and rationale}
- {Decision 2 and rationale}

**Known Limitations:**
- {Limitation 1}
- {Limitation 2}

**Testing Notes:**
- {Important testing considerations}

---

## Completion Summary

{This section filled out after S8.P2}

**Completion Date:** {YYYY-MM-DD}
**Start Date:** {YYYY-MM-DD}
**Duration:** {N days}

**Lines of Code Changed:** {~N} (approximate)
**Tests Added:** {N}
**Files Modified:** {N}

**Key Accomplishments:**
- {Accomplishment 1}
- {Accomplishment 2}
- {Accomplishment 3}

**Challenges Overcome:**
- {Challenge 1 and solution}
- {Challenge 2 and solution}

**S8.P1 Impact on Other Features:**
- {Feature X: Updated spec.md to reflect...}
- {Or: "No impact on other features"}
```