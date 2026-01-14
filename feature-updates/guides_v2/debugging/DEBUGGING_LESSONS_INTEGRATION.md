# Debugging Lessons Integration into Guide Updates

**Purpose:** Explains how debugging lessons flow through the workflow and are applied to improve guides

**Date Created:** 2026-01-04

---

## Overview

The debugging workflow generates three key documents that feed into guide improvements:

1. **debugging/lessons_learned.md** - Technical insights (WHAT bugs were, HOW we found them)
2. **debugging/process_failure_analysis.md** - Process gaps (WHY bugs got through workflow)
3. **debugging/guide_update_recommendations.md** - Concrete guide updates (ACTIONABLE fixes)

These documents are systematically collected and applied at multiple points in the workflow.

---

## Where Debugging Lessons Are Created

### Feature-Level Debugging

**Location:** `feature_XX_{name}/debugging/`

**Created During:** S7.P1 or S7.P2 when bugs are discovered

**Workflow:**
1. Issues discovered during testing
2. Enter debugging protocol (Phase 1-3: Investigation and fix)
3. User verification (Step 4: Confirm each fix)
4. **Step 4b (MANDATORY - NEW):** Per-issue root cause analysis
   - Immediately after each fix confirmed (while context fresh)
   - 5-why analysis to reach process/guide gap
   - Draft guide improvement proposal
   - User confirms root cause
   - Append to `guide_update_recommendations.md` incrementally
5. **Step 5:** Loop back to testing with cross-pattern analysis
   - After ALL issues resolved
   - Identify patterns across multiple bugs
   - Create `process_failure_analysis.md` (cross-bug patterns)
   - Append cross-pattern recommendations to `guide_update_recommendations.md`
   - Create/update `lessons_learned.md` (technical insights)

**Files Created:**
```
feature_XX_{name}/debugging/
├── ISSUES_CHECKLIST.md
├── investigation_rounds.md
├── issue_01_{name}.md
├── issue_02_{name}.md
├── code_changes.md
├── process_failure_analysis.md         ← Process gap analysis (Phase 5)
├── guide_update_recommendations.md     ← Actionable guide updates (Phase 4b + Phase 5)
├── lessons_learned.md                  ← Technical insights (Phase 5)
└── diagnostic_logs/
```

**File Creation Timing:**
- **guide_update_recommendations.md** - Created incrementally:
  - **Step 4b:** Per-issue recommendations added immediately after each fix confirmed
  - **Step 5:** Cross-pattern recommendations appended after all issues resolved
- **process_failure_analysis.md** - Created in Phase 5 (cross-bug pattern analysis)
- **lessons_learned.md** - Created in Phase 5 (technical insights summary)

---

### Epic-Level Debugging

**Location:** `{epic_name}/debugging/`

**Created During:** S9.P1 (Epic Smoke Testing) or S9.P2 (Epic QC Rounds) or S10 (User Testing)

**Workflow:** Same as feature-level but for epic integration issues

**Files Created:**
```
{epic_name}/debugging/
├── ISSUES_CHECKLIST.md
├── investigation_rounds.md
├── issue_01_{name}.md
├── code_changes.md
├── process_failure_analysis.md         ← Epic-level process gaps (Phase 5)
├── guide_update_recommendations.md     ← Epic-level guide updates (Phase 4b + Phase 5)
├── lessons_learned.md                  ← Epic-level technical insights (Phase 5)
└── diagnostic_logs/
```

**File Creation Timing:** Same as feature-level (Phase 4b per-issue + Phase 5 cross-pattern)

---

## Where Debugging Lessons Are Aggregated

### S10.P3: Final Review (Per Feature)

**File Updated:** `feature_XX_{name}/lessons_learned.md`

**What's Added:**
- Brief summary of debugging that occurred (if any)
- Link to debugging/ folder for details
- Key process gaps identified

**Format:**
```markdown
## Post-Implementation Lessons (S7)

### Debugging (If Occurred):
- Issues discovered: {count}
- Testing stage: {S7.P1 / S7.P2}
- Total time: {hours}
- Key insights: See debugging/lessons_learned.md
- Process gaps: See debugging/process_failure_analysis.md
- Guide updates: See debugging/guide_update_recommendations.md
```

---

### S8.P1: Cross-Feature Alignment (After Each Feature)

**NOT CURRENTLY UPDATED** - epic_lessons_learned.md is NOT updated here

**Reasoning:** Too early - not all features complete yet

---

### S9.P3: Epic Final Review (Epic Level)

**File Updated:** `epic_lessons_learned.md`

**What's Added:**

**Per-Feature Debugging Section:**
```markdown
## S5 Lessons Learned (Feature Implementation)

### Feature 01 ({name})

**Debugging (If Occurred):**
- Issues discovered: {count}
- Testing stage: S7.P1 / S7.P2
- Total time: {hours}
- Key insights: {from debugging/lessons_learned.md}
- Process gaps: {from debugging/process_failure_analysis.md}
- Guide updates proposed: {count from debugging/guide_update_recommendations.md}
```

**Cross-Feature Debugging Insights Section:**
```markdown
### Debugging Insights Across Features

**Total Debugging Sessions:** {N}

**Common Bug Patterns:**
{from multiple process_failure_analysis.md files}

**Common Process Gaps:**
{from multiple process_failure_analysis.md files}

**Most Impactful Guide Updates:**
{top updates proposed by multiple features}
```

**Epic-Level Debugging Section:**
```markdown
## S9 Lessons Learned (Epic Final QC)

**Debugging (If Occurred at Epic Level):**
- Issues discovered: {count}
- Testing stage: S9.P1 / 6b
- Total time: {hours}
- Key insights: {from {epic_name}/debugging/lessons_learned.md}
- Process gaps: {from {epic_name}/debugging/process_failure_analysis.md}
- Guide updates: {from {epic_name}/debugging/guide_update_recommendations.md}
```

---

## Where Debugging Lessons Are Applied to Guides

### S10.P1: Guide Update from Lessons Learned (MANDATORY)

**This is where ALL debugging lessons are systematically applied to guides**

**Note:** Previously S10 Step 4, now a dedicated S10.P1 workflow with user approval for each proposal.

**Complete Workflow Guide:** `stages/s10/s7_p1_guide_update_workflow.md`

**Process Summary:**

1. **Analyze ALL lessons_learned.md files** (epic + features + debugging)
   - Standard lessons from epic_lessons_learned.md and feature lessons_learned.md
   - Debugging lessons from debugging/lessons_learned.md
   - Process failure analysis from debugging/process_failure_analysis.md
   - Guide recommendations from debugging/guide_update_recommendations.md (HIGHEST PRIORITY)

2. **Identify guide gaps** - For each lesson, determine which guide(s) could have prevented the issue

3. **Create GUIDE_UPDATE_PROPOSAL.md** with prioritized proposals:
   - **P0 (Critical):** Prevents catastrophic bugs, mandatory gate gaps
   - **P1 (High):** Significantly improves quality, reduces major rework
   - **P2 (Medium):** Moderate improvements, clarifies ambiguity
   - **P3 (Low):** Minor improvements, cosmetic fixes
   - **Note:** Debugging lessons from guide_update_recommendations.md typically map to P0/P1

4. **Present each proposal to user** with before/after comparison

5. **User decides** for each proposal: Approve / Modify / Reject / Discuss

6. **Apply only approved changes** (or user modifications)

7. **Create separate commit** for guide updates (before epic commit)

8. **Update guide_update_tracking.md** with applied/pending/rejected lessons

**Debugging-Specific Priority Mapping:**
- debugging/guide_update_recommendations.md → P0 (Critical) or P1 (High)
- debugging/process_failure_analysis.md → P1 (High) or P2 (Medium)
- lessons_learned.md "Guide Improvements Needed" → P2 (Medium) or P3 (Low)

**Why this matters:** Debugging lessons are the MOST ACTIONABLE because they come from actual bugs that reached testing. S10.P1 ensures these lessons get prioritized (P0/P1) and user-approved before being applied to guides.

**See:** `stages/s10/s7_p1_guide_update_workflow.md` for complete 9-step workflow

---

## Why This Matters

### Debugging Lessons Are Higher Priority Than General Lessons

**Reason:** Debugging lessons identify PROVEN process gaps
- Regular lessons: "We think this could be better"
- Debugging lessons: "This gap LET BUGS THROUGH our process"

**Impact:**
- Bugs got through research phase → Process gap proven
- Bugs got through implementation → Process gap proven
- Bugs got through testing → Process gap proven

**Result:** Fixing these gaps prevents same bugs in future epics

---

### The Three-Document System

**1. process_failure_analysis.md**
- **Audience:** Process designers
- **Purpose:** Understand WHY bugs got through
- **Content:** Systematic analysis of each stage (S5, S6, S7)
- **Output:** Specific process gaps identified

**2. guide_update_recommendations.md**
- **Audience:** Guide maintainers (S10.P1 agents)
- **Purpose:** ACTIONABLE guide improvements
- **Content:** Exact text proposals with priority (per-issue from Phase 4b + patterns from Phase 5)
- **Created:** Incrementally (Phase 4b adds per-issue, Phase 5 appends patterns)
- **Output:** Ready-to-apply guide updates

**3. lessons_learned.md**
- **Audience:** Future developers
- **Purpose:** Technical insights
- **Content:** Bug patterns, investigation techniques
- **Output:** Debugging knowledge base

---

## Verification That Lessons Are Applied

### During S10.P1 (Guide Update Workflow)

Agents MUST verify (as part of guide_update_tracking.md):
```markdown
□ Total sources checked: {N}
  - lessons_learned.md files: {N}
  - debugging/process_failure_analysis.md files: {N}
  - debugging/guide_update_recommendations.md files: {N}
□ Total lessons identified: {N}
  - Critical (debugging): {N}
  - High (debugging): {N}
  - Medium (feature): {N}
□ Lessons applied: {N}
□ Application rate: 100% ✅
```

**If application rate < 100%:** ❌ STOP - Cannot proceed to commit

---

## Example Flow

### Scenario: Feature 02 has 2 bugs during smoke testing

**S10.P1 Part 3:**
- Bugs discovered → Add to ISSUES_CHECKLIST.md
- Enter debugging protocol

**Debugging Protocol:**
- Phase 1-3: Investigate and fix bugs (2 issues identified and fixed)
- **Step 4:** User verifies each fix
- **Step 4b (NEW - MANDATORY):** Per-issue root cause analysis
  - Issue #1: 5-why analysis → guide gap identified → user confirms → append to guide_update_recommendations.md
  - Issue #2: 5-why analysis → guide gap identified → user confirms → append to guide_update_recommendations.md
  - Time: 10-20 minutes per issue (captures lessons while context fresh)
- **Step 5:** Loop back to testing with cross-pattern analysis
  - Analyze why bugs got through S5 (Implementation Planning)
  - Analyze why bugs got through S6 (Implementation Execution)
  - Analyze why bugs got through S7.P1 (Smoke testing)
  - Identify patterns across Issue #1 and Issue #2
  - Create process_failure_analysis.md with cross-bug patterns
  - Append 3 pattern-based recommendations to guide_update_recommendations.md
  - Create lessons_learned.md with technical insights
  - **Total guide recommendations:** 5 (2 per-issue from Phase 4b + 3 pattern-based from Phase 5)

**S7.P3:**
- Update feature_02_{name}/lessons_learned.md
- Add brief debugging summary

**S9.P3 (Epic Final Review):**
- Update epic_lessons_learned.md
- Aggregate Feature 02 debugging insights
- Include in cross-feature patterns

**S10.P1 (Guide Update from Lessons Learned):**
- Find debugging/guide_update_recommendations.md
- Extract 5 critical updates (map to P0/P1 priority)
- Create GUIDE_UPDATE_PROPOSAL.md with proposals
- Present each proposal to user for approval
- User approves all 5 critical updates
- Apply approved updates to guides
- Update guide_update_tracking.md with applied lessons
- Future epics now have improved guides

---

## Summary

**Debugging lessons are collected at:**
- S7 (feature debugging)
- S9 (epic debugging)

**Debugging lessons are aggregated at:**
- S10.P3 (feature lessons_learned.md)
- S9.P3 (epic_lessons_learned.md)

**Debugging lessons are applied at:**
- **S10.P1 (Guide Update from Lessons Learned)** ← ONLY place where guides are updated

**Critical Requirements:**
1. Must find ALL debugging files (3 types × N features + epic)
2. Must create GUIDE_UPDATE_PROPOSAL.md with P0-P3 prioritization
3. Must present each proposal to user for individual approval
4. Must apply only approved changes (user has full control)
5. Debugging lessons have HIGHER priority (P0/P1) than general lessons (P2/P3)

**Result:** Every debugging session improves the workflow, preventing same bugs in future epics.

---

*End of DEBUGGING_LESSONS_INTEGRATION.md*
