# Epic Lessons Learned Template

**Filename:** `epic_lessons_learned.md`
**Location:** `feature-updates/{epic_name}/epic_lessons_learned.md`
**Created:** Stage 1 (Epic Planning)
**Updated:** Throughout all stages (after each feature completion)

**Purpose:** Cross-feature insights, systemic issues, guide improvements, and workflow refinements for the entire epic.

---

## Template

```markdown
# Epic Lessons Learned: {epic_name}

**Epic Overview:** {Brief description of epic}
**Date Range:** {start_date} - {end_date}
**Total Features:** {N}
**Total Bug Fixes:** {N}

---

## Purpose

This document captures:
- **Cross-feature insights** (patterns observed across multiple features)
- **Systemic issues** (problems affecting multiple features)
- **Guide improvements** (updates needed for guides_v2/)
- **Workflow refinements** (process improvements for future epics)

**This is separate from per-feature lessons_learned.md files** (which capture feature-specific insights).

---

## Stage 1 Lessons Learned (Epic Planning)

**What Went Well:**
- {Positive observation 1}
- {Positive observation 2}

**What Could Be Improved:**
- {Improvement opportunity 1}
- {Improvement opportunity 2}

**Insights for Future Epics:**
- {Insight 1}
- {Insight 2}

**Guide Improvements Needed:**
- {Guide file name}: {Specific improvement needed}
- {Or: "None identified"}

---

## Stage 2 Lessons Learned (Feature Deep Dives)

{Lessons captured AFTER all features complete Stage 2}

### Cross-Feature Patterns

**Pattern 1:** {Pattern observed across features}
- Observed in: {List features}
- Impact: {How this affected development}
- Recommendation: {What to do differently}

**Pattern 2:** {Another pattern}
- {Details...}

### Feature-Specific Highlights

**Feature 01 ({name}):**
- Key lesson: {Lesson from this feature's Stage 2}
- Application to other features: {How this applies beyond Feature 01}

**Feature 02 ({name}):**
- Key lesson: {Lesson}
- Application: {Application}

{Repeat for all features}

### What Went Well

- {Positive observation 1}
- {Positive observation 2}

### What Could Be Improved

- {Improvement 1}
- {Improvement 2}

### Guide Improvements Needed

- `stages/stage_2/feature_deep_dive.md`: {Specific improvement}
- {Or: "None identified"}

---

## Stage 3 Lessons Learned (Cross-Feature Sanity Check)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Conflicts Discovered:**
- {Conflict 1 and resolution}
- {Conflict 2 and resolution}
- {Or: "No conflicts discovered"}

**Insights for Future Epics:**
- {Insight}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## Stage 4 Lessons Learned (Epic Testing Strategy)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**epic_smoke_test_plan.md Evolution:**
- Changes from Stage 1 → Stage 4: {Summary of how test plan evolved}
- Integration points discovered: {N}
- Key insights: {Insights about testing strategy}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## Stage 5 Lessons Learned (Feature Implementation)

{Capture lessons AFTER EACH feature completes Stage 5e}

### Feature 01 ({name}) - Stages 5a through 5e

**Stage 5a (TODO Creation):**
- What went well: {Observation}
- What could improve: {Improvement}
- 24 iterations experience: {Any issues with specific iterations}

**Stage 5b (Implementation):**
- What went well: {Observation}
- Challenges: {Challenges encountered and solutions}

**Stage 5c (Post-Implementation):**
- Smoke testing results: {Summary}
- QC rounds: {Any issues found and resolved}
- PR review: {Insights}

**Stage 5d (Cross-Feature Alignment):**
- Features affected: {List features whose specs were updated}
- Key updates: {Summary of spec updates}

**Stage 5e (Epic Testing Plan Update):**
- Test scenarios added: {N}
- Integration scenarios: {Summary}

---

### Feature 02 ({name}) - Stages 5a through 5e

{Repeat structure for Feature 02}

---

### Feature 03 ({name}) - Stages 5a through 5e

{Repeat structure for Feature 03}

---

### Cross-Feature Implementation Patterns

**Pattern 1:** {Pattern observed during implementation}
- Observed in: {List features}
- Impact: {How this affected development}
- Recommendation: {What to do differently}

---

### Guide Improvements Needed from Stage 5

**From Feature 01:**
- `stages/stage_5/round1_todo_creation.md`: {Specific improvement}
- `stages/stage_5/smoke_testing.md`: {Specific improvement}

**From Feature 02:**
- {Guide improvements}

**From Feature 03:**
- {Guide improvements}

---

## Stage 6 Lessons Learned (Epic Final QC)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Epic-Level Issues Found:**
- {Issue 1 and resolution}
- {Or: "No epic-level issues found"}

**epic_smoke_test_plan.md Effectiveness:**
- Scenarios that caught issues: {List}
- Scenarios that should be added: {List or "None"}
- Overall assessment: {Assessment of test plan quality}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## Stage 7 Lessons Learned (Epic Cleanup)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Documentation Quality:**
- {Assessment of final documentation completeness}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## Cross-Epic Insights

{High-level insights applicable beyond this epic}

**Systemic Patterns:**
- {Pattern 1 observed across ALL features}
- {Pattern 2}

**Workflow Refinements:**
- {Refinement 1 for future epics}
- {Refinement 2}

**Tool/Process Improvements:**
- {Improvement 1}
- {Improvement 2}

---

## Recommendations for Future Epics

**Top 5 Recommendations:**
1. {Recommendation 1 - actionable and specific}
2. {Recommendation 2}
3. {Recommendation 3}
4. {Recommendation 4}
5. {Recommendation 5}

**Do These Things:**
- {Practice to continue}
- {Practice to continue}

**Avoid These Things:**
- {Anti-pattern to avoid}
- {Anti-pattern to avoid}

---

## Guide Updates Applied

{Track which guides were updated based on lessons from THIS epic}

**Guides Updated:**
- `{guide_name}.md` (v2.{X}): {What was updated}
- `{guide_name}.md` (v2.{X}): {What was updated}

**CLAUDE.md Updates:**
- {Updates made or "None"}

**Date Applied:** {YYYY-MM-DD}

---

## Metrics

**Epic Duration:** {N} days
**Features:** {N}
**Bug Fixes:** {N}
**Tests Added:** {N}
**Files Modified:** {N}
**Lines of Code Changed:** ~{N}

**Stage Durations:**
- Stage 1: {N} days
- Stage 2: {N} days (all features)
- Stage 3: {N} days
- Stage 4: {N} days
- Stage 5: {N} days (all features)
- Stage 6: {N} days
- Stage 7: {N} days

**QC Restart Count:**
- Stage 5c restarts: {N} (across all features)
- Stage 6 restarts: {N}

**Test Pass Rates:**
- Final pass rate: {percentage}% ({X}/{Y} tests)
- Tests added by this epic: {N}
```