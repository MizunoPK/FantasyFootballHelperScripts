# Feature Lessons Learned Template

**Filename:** `lessons_learned.md`
**Location:** `feature-updates/{epic_name}/feature_XX_{name}/lessons_learned.md`
**Created:** {YYYY-MM-DD}
**Updated:** After Stages 5a, 5b, 5c

**Purpose:** Lessons specific to a single feature's development, separate from epic-level lessons.

---

## Template

```markdown
# Feature Lessons Learned: {feature_name}

**Part of Epic:** {epic_name}
**Feature Number:** {N}
**Created:** {YYYY-MM-DD}
**Last Updated:** {YYYY-MM-DD}

---

## Purpose

This document captures lessons specific to THIS feature's development. This is separate from epic_lessons_learned.md (which captures cross-feature patterns).

---

## Stage 2 Lessons Learned (Feature Deep Dive)

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

## Stage 5a Lessons Learned (TODO Creation)

**24 Verification Iterations Experience:**
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

## Stage 5b Lessons Learned (Implementation)

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

## Stage 5c Lessons Learned (Post-Implementation)

**Smoke Testing Results:**
- Part 1 (Import): {PASSED / Issues found and fixed}
- Part 2 (Entry Point): {PASSED / Issues found and fixed}
- Part 3 (E2E Execution): {PASSED / Issues found and fixed}

**QC Rounds Results:**
- QC Round 1: {PASSED / Issues found and fixed}
- QC Round 2: {PASSED / Issues found and fixed}
- QC Round 3: {PASSED / Issues found and fixed}

**PR Review Results:**
- Categories with issues: {List or "None"}
- Key improvements made: {List}

**QC Restart Count:** {N} (if > 0, explain why restart was needed)

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

**Stage 5a TODO Creation:**
- stages/stage_5/round1_todo_creation.md: {Improvement 1 or "None"}
- stages/stage_5/round2_todo_creation.md: {Improvement 1 or "None"}
- stages/stage_5/round3_part1_preparation.md: {Improvement 1 or "None"}
- stages/stage_5/round3_part2_final_gates.md: {Improvement 1 or "None"}

**stages/stage_5/implementation_execution.md:**
- {Improvement 1 or "None"}

**Stage 5c Post-Implementation:**
- stages/stage_5/smoke_testing.md: {Improvement 1 or "None"}
- stages/stage_5/qc_rounds.md: {Improvement 1 or "None"}
- stages/stage_5/final_review.md: {Improvement 1 or "None"}

{If no guide improvements needed: "No guide improvements identified from this feature"}

---

## Metrics

**Feature Duration:** {N} days
**LOC Changed:** ~{N}
**Tests Added:** {N}
**Files Modified:** {N}

**Stage Durations:**
- Stage 2: {N} days
- Stage 5a: {N} days
- Stage 5b: {N} days
- Stage 5c: {N} days
- Stage 5d: {N} days
- Stage 5e: {N} days

**Test Pass Rate:** {percentage}% ({X}/{Y} tests)
```