# Epic Lessons Learned Template

**Filename:** `epic_lessons_learned.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/epic_lessons_learned.md`
**Created:** S1 (Epic Planning)
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

## S1 Lessons Learned (Epic Planning)

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

## S2 Lessons Learned (Feature Deep Dives)

{Lessons captured AFTER all features complete S2}

### Cross-Feature Patterns

**Pattern 1:** {Pattern observed across features}
- Observed in: {List features}
- Impact: {How this affected development}
- Recommendation: {What to do differently}

**Pattern 2:** {Another pattern}
- {Details...}

### Feature-Specific Highlights

**Feature 01 ({name}):**
- Key lesson: {Lesson from this feature's S2}
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

- `stages/s2/s2_feature_deep_dive.md`: {Specific improvement}
- {Or: "None identified"}

---

## S3 Lessons Learned (Cross-Feature Sanity Check)

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

## S4 Lessons Learned (Epic Testing Strategy)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**epic_smoke_test_plan.md Evolution:**
- Changes from S1 → S4: {Summary of how test plan evolved}
- Integration points discovered: {N}
- Key insights: {Insights about testing strategy}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## S5 Lessons Learned (Feature Implementation)

{Capture lessons AFTER EACH feature completes S8.P2}

### Feature 01 ({name}) - Stages 5a through 5e

**S5 (TODO Creation):**
- What went well: {Observation}
- What could improve: {Improvement}
- 28 iterations experience: {Any issues with specific iterations}

**S6 (Implementation):**
- What went well: {Observation}
- Challenges: {Challenges encountered and solutions}

**S7 (Post-Implementation):**
- Smoke testing results: {Summary}
- QC rounds: {Any issues found and resolved}
- PR review: {Insights}

**Debugging (If Occurred):**
- Issues discovered: {Count and brief summary}
- Testing stage where found: {S10.P1 / S10.P2 / other}
- Total debugging time: {Hours}
- Key insights: {Brief insights from debugging/lessons_learned.md}
- Process improvements identified: {Brief summary of process gaps from debugging/process_failure_analysis.md}
- Guide updates proposed: {Count of critical/high/medium priority updates from debugging/guide_update_recommendations.md}

**S8.P1 (Cross-Feature Alignment):**
- Features affected: {List features whose specs were updated}
- Key updates: {Summary of spec updates}

**S8.P2 (Epic Testing Plan Update):**
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

### Debugging Insights Across Features

{Aggregate insights from ALL feature-level debugging/ folders}

**Total Debugging Sessions:** {N} features required debugging

**Common Bug Patterns:**
- {Pattern 1 from multiple features' debugging/process_failure_analysis.md}
- {Pattern 2}

**Common Process Gaps:**
- {Gap 1 identified across multiple debugging sessions}
- {Gap 2}

**Most Impactful Guide Updates:**
{List the top 3-5 guide updates that were proposed by multiple features' debugging}

1. {guide_name}.md - {section}: {why this is critical}
2. {guide_name}.md - {section}: {why this is critical}

**Testing Insights:**
- {What types of bugs were caught by smoke testing vs QC rounds}
- {What types of bugs should have been caught earlier}

---

### Guide Improvements Needed from S5

**From Feature 01:**
- `stages/s5/s5_p1_planning_round1.md`: {Specific improvement}
- `stages/s10/s7_p1_smoke_testing.md`: {Specific improvement}

**From Feature 01 Debugging (if occurred):**
- {List guide updates from feature_01_{name}/debugging/guide_update_recommendations.md}
- Priority: {Critical/High/Medium}

**From Feature 02:**
- {Guide improvements}

**From Feature 02 Debugging (if occurred):**
- {List guide updates}

**From Feature 03:**
- {Guide improvements}

**From Feature 03 Debugging (if occurred):**
- {List guide updates}

---

## S9 Lessons Learned (Epic Final QC)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Epic-Level Issues Found:**
- {Issue 1 and resolution}
- {Or: "No epic-level issues found"}

**Debugging (If Occurred at Epic Level):**
- Issues discovered: {Count and brief summary}
- Testing stage where found: {S9.P1 / 6b / other}
- Total debugging time: {Hours}
- Key insights: {Brief insights from {epic_name}/debugging/lessons_learned.md}
- Process improvements identified: {Brief summary from {epic_name}/debugging/process_failure_analysis.md}
- Guide updates proposed: {Count from {epic_name}/debugging/guide_update_recommendations.md}

**epic_smoke_test_plan.md Effectiveness:**
- Scenarios that caught issues: {List}
- Scenarios that should be added: {List or "None"}
- Overall assessment: {Assessment of test plan quality}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

**From Epic-Level Debugging (if occurred):**
- {List guide updates from {epic_name}/debugging/guide_update_recommendations.md}
- Priority: {Critical/High/Medium}

---

## S10 Lessons Learned (Epic Cleanup)

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
- S1: {N} days
- S2: {N} days (all features)
- S3: {N} days
- S4: {N} days
- S5: {N} days (all features)
- S9: {N} days
- S10: {N} days

**QC Restart Count:**
- S7 restarts: {N} (across all features)
- S9 restarts: {N}

**Test Pass Rates:**
- Final pass rate: {percentage}% ({X}/{Y} tests)
- Tests added by this epic: {N}
```