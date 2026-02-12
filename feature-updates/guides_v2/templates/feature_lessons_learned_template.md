# Feature Lessons Learned Template

**Filename:** `lessons_learned.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/feature_XX_{name}/lessons_learned.md`
**Created:** {YYYY-MM-DD}
**Updated:** After Stages S5, S6, S7

**Purpose:** Lessons specific to a single feature's development, separate from epic-level lessons.

---

## Template

```markdown
## Feature Lessons Learned: {feature_name}

**Part of Epic:** {epic_name}
**Feature Number:** {N}
**Created:** {YYYY-MM-DD}
**Last Updated:** {YYYY-MM-DD}

---

## Purpose

This document captures lessons specific to THIS feature's development. This is separate from epic_lessons_learned.md (which captures cross-feature patterns).

---

## S2 Lessons Learned (Feature Deep Dive)

**What Went Well:**
- {Positive observation 1}
- {Positive observation 2}

**What Could Be Improved:**
- {Improvement opportunity 1}
- {Improvement opportunity 2}

**Key Decisions:**
- {Decision 1 and rationale}
- {Decision 2 and rationale}

**Gotchas Discovered:**
- {Gotcha 1}
- {Gotcha 2}

---

## S5 Lessons Learned (TODO Creation)

**22 Verification Iterations Experience:**
- Iterations that were most valuable: {List iterations and why}
- Iterations where issues were found: {List and what was caught}
- Iterations that seemed redundant: {List and why - helps improve guide}

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Complexity Assessment:**
- Initial complexity estimate: {LOW / MEDIUM / HIGH}
- Actual complexity: {LOW / MEDIUM / HIGH}
- Variance explanation: {Why estimate was off, if applicable}

---

## S6 Lessons Learned (Implementation)

**What Went Well:**
- {Positive observation}

**Challenges Encountered:**
- **Challenge 1:** {Description}
  - Solution: {How it was resolved}
  - Time impact: {How much extra time}

- **Challenge 2:** {Description}
  - Solution: {Solution}
  - Time impact: {Impact}

**Deviations from Spec:**
- {Deviation 1 and justification}
- {Or: "No deviations from spec"}

**Code Quality Notes:**
- {Note 1}
- {Note 2}

---

## S7 Lessons Learned (Post-Implementation)

**Smoke Testing Results:**
- Part 1 (Import): {PASSED / Issues found and fixed}
- Part 2 (Entry Point): {PASSED / Issues found and fixed}
- Part 3 (E2E Execution): {PASSED / Issues found and fixed}

**Validation Loop Results:**
- Total Rounds: {N}
- Consecutive Clean Rounds: 3 (exit criteria met)
- Issues Found & Fixed: {count}
- All 11 dimensions validated: YES

**PR Review Results:**
- Categories with issues: {List or "None"}
- Key improvements made: {List}

**Issues Found During Validation:** {N} (if > 0, list what was fixed)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

---

## Implementation Insights

**Algorithm Performance:**
- {Algorithm 1}: {Performance notes}
- {Algorithm 2}: {Performance notes}

**Data Structure Choices:**
- {Choice 1 and rationale}
- {Choice 2 and rationale}

**Integration Challenges:**
- {Challenge 1 with other features and solution}
- {Or: "No integration challenges"}

**Testing Insights:**
- {Insight 1}
- {Insight 2}

---

## Recommendations

**For Similar Features in Future Epics:**
- Do: {Recommendation 1}
- Do: {Recommendation 2}
- Avoid: {Anti-pattern 1}
- Avoid: {Anti-pattern 2}

**For This Feature's Maintenance:**
- {Maintenance note 1}
- {Maintenance note 2}

---

## Guide Improvements Needed

{Specific improvements needed for guides_v2/ based on THIS feature's experience}

**S5 Implementation Planning:**
- stages/s5/s5_v2_validation_loop.md: {Improvement 1 or "None"}

**stages/s6/s6_execution.md:**
- {Improvement 1 or "None"}

**S7 Post-Implementation:**
- stages/s7/s7_p1_smoke_testing.md: {Improvement 1 or "None"}
- stages/s7/s7_p2_qc_rounds.md: {Improvement 1 or "None"}
- stages/s7/s7_p3_final_review.md: {Improvement 1 or "None"}

{If no guide improvements needed: "No guide improvements identified from this feature"}

---

## Metrics

**Feature Duration:** {N} days
**LOC Changed:** ~{N}
**Tests Added:** {N}
**Files Modified:** {N}

**Stage Durations:**
- S2: {N} days
- S5: {N} days
- S6: {N} days
- S7: {N} days
- S8.P1: {N} days
- S8.P2: {N} days

**Test Pass Rate:** {percentage}% ({X}/{Y} tests)
```