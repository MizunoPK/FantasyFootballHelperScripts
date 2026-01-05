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

**Created During:** Stage 5ca (Smoke Testing) or Stage 5cb (QC Rounds) when bugs are discovered

**Workflow:**
1. Issues discovered during testing
2. Enter debugging protocol
3. Resolve all issues
4. **Step 3 (MANDATORY):** Systematic root cause analysis
   - Create `process_failure_analysis.md` (analyze why bugs got through)
   - Create `guide_update_recommendations.md` (propose concrete fixes)
   - Create/update `lessons_learned.md` (technical insights)
5. Loop back to testing

**Files Created:**
```
feature_XX_{name}/debugging/
├── ISSUES_CHECKLIST.md
├── investigation_rounds.md
├── issue_01_{name}.md
├── issue_02_{name}.md
├── code_changes.md
├── process_failure_analysis.md         ← Process gap analysis
├── guide_update_recommendations.md     ← Actionable guide updates
├── lessons_learned.md                  ← Technical insights
└── diagnostic_logs/
```

---

### Epic-Level Debugging

**Location:** `{epic_name}/debugging/`

**Created During:** Stage 6a (Epic Smoke Testing) or Stage 6b (Epic QC Rounds) or Stage 7 (User Testing)

**Workflow:** Same as feature-level but for epic integration issues

**Files Created:**
```
{epic_name}/debugging/
├── ISSUES_CHECKLIST.md
├── investigation_rounds.md
├── issue_01_{name}.md
├── code_changes.md
├── process_failure_analysis.md         ← Epic-level process gaps
├── guide_update_recommendations.md     ← Epic-level guide updates
├── lessons_learned.md                  ← Epic-level technical insights
└── diagnostic_logs/
```

---

## Where Debugging Lessons Are Aggregated

### Stage 5cc: Final Review (Per Feature)

**File Updated:** `feature_XX_{name}/lessons_learned.md`

**What's Added:**
- Brief summary of debugging that occurred (if any)
- Link to debugging/ folder for details
- Key process gaps identified

**Format:**
```markdown
## Post-Implementation Lessons (Stage 5c)

### Debugging (If Occurred):
- Issues discovered: {count}
- Testing stage: {Stage 5ca / 5cb}
- Total time: {hours}
- Key insights: See debugging/lessons_learned.md
- Process gaps: See debugging/process_failure_analysis.md
- Guide updates: See debugging/guide_update_recommendations.md
```

---

### Stage 5d: Cross-Feature Alignment (After Each Feature)

**NOT CURRENTLY UPDATED** - epic_lessons_learned.md is NOT updated here

**Reasoning:** Too early - not all features complete yet

---

### Stage 6c: Epic Final Review (Epic Level)

**File Updated:** `epic_lessons_learned.md`

**What's Added:**

**Per-Feature Debugging Section:**
```markdown
## Stage 5 Lessons Learned (Feature Implementation)

### Feature 01 ({name})

**Debugging (If Occurred):**
- Issues discovered: {count}
- Testing stage: Stage 5ca / 5cb
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
## Stage 6 Lessons Learned (Epic Final QC)

**Debugging (If Occurred at Epic Level):**
- Issues discovered: {count}
- Testing stage: Stage 6a / 6b
- Total time: {hours}
- Key insights: {from {epic_name}/debugging/lessons_learned.md}
- Process gaps: {from {epic_name}/debugging/process_failure_analysis.md}
- Guide updates: {from {epic_name}/debugging/guide_update_recommendations.md}
```

---

## Where Debugging Lessons Are Applied to Guides

### Stage 7 Step 4: Update Guides (MANDATORY)

**This is where ALL debugging lessons are systematically applied to guides**

**Process:**

**Step 4a: Find ALL Lesson Files**
```bash
# Standard lessons
find feature-updates/done/{epic_name} -name "lessons_learned.md" -type f

# Debugging process analysis
find feature-updates/done/{epic_name} -path "*/debugging/process_failure_analysis.md" -type f

# Debugging guide recommendations (HIGHEST PRIORITY)
find feature-updates/done/{epic_name} -path "*/debugging/guide_update_recommendations.md" -type f
```

**Step 4b: Extract Lessons from EACH File**

**From lessons_learned.md files:**
- "Guide Improvements Needed" sections

**From debugging/process_failure_analysis.md files:**
- "Guide Updates Required" from each bug analysis
- "High-Priority Guide Updates" from cross-bug patterns

**From debugging/guide_update_recommendations.md files:**
- ALL recommendations (Critical/Moderate/Low)
- "New Sections Needed"
- "Template/Checklist Updates"
- **THESE ARE THE MOST ACTIONABLE**

**Step 4c: Create Master Checklist**

**Priority Order:**
1. **HIGHEST:** debugging/guide_update_recommendations.md (concrete, actionable)
2. **HIGH:** debugging/process_failure_analysis.md (systematic process gaps)
3. **MEDIUM:** lessons_learned.md "Guide Improvements Needed"

**Template:**
```markdown
## Master Guide Update Checklist - {epic_name}

**Sources Checked:**
- [ ] epic_lessons_learned.md
- [ ] feature_01_{name}/lessons_learned.md
- [ ] feature_01_{name}/debugging/lessons_learned.md
- [ ] feature_01_{name}/debugging/process_failure_analysis.md
- [ ] feature_01_{name}/debugging/guide_update_recommendations.md
- [ ] {epic_name}/debugging/lessons_learned.md
- [ ] {epic_name}/debugging/process_failure_analysis.md
- [ ] {epic_name}/debugging/guide_update_recommendations.md

### Critical Priority Updates (from guide_update_recommendations.md)
{List with source, current text, proposed text, rationale}

### High Priority Updates (from process_failure_analysis.md)
{List with bugs prevented, process gap, proposed change}

### Medium Priority Updates (from lessons_learned.md)
{List standard lessons}
```

**Step 4d: Apply EACH Lesson**
- Read current guide
- Make Edit
- Mark [x] APPLIED in checklist

**Step 4e: Verify 100% Application**
```markdown
□ Read ALL debugging/guide_update_recommendations.md files
□ Read ALL debugging/process_failure_analysis.md files
□ Read ALL lessons_learned.md files
□ Created master checklist
□ Applied ALL lessons (100% application rate)
```

**⚠️ CRITICAL:** Application rate MUST be 100%. Cannot skip debugging lessons.

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
- **Content:** Systematic analysis of each phase (5a, 5b, 5c)
- **Output:** Specific process gaps identified

**2. guide_update_recommendations.md**
- **Audience:** Guide maintainers (Stage 7 agents)
- **Purpose:** ACTIONABLE guide improvements
- **Content:** Exact text proposals with priority
- **Output:** Ready-to-apply guide updates

**3. lessons_learned.md**
- **Audience:** Future developers
- **Purpose:** Technical insights
- **Content:** Bug patterns, investigation techniques
- **Output:** Debugging knowledge base

---

## Verification That Lessons Are Applied

### At Stage 7 Step 4e

Agents MUST verify:
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

**Stage 5ca Part 3:**
- Bugs discovered → Add to ISSUES_CHECKLIST.md
- Enter debugging protocol

**Debugging Protocol:**
- Phase 1-4: Investigate and fix bugs
- **Phase 5:** Systematic root cause analysis
  - Analyze why bugs got through Stage 5a (TODO creation)
  - Analyze why bugs got through Stage 5b (Implementation)
  - Analyze why bugs got through Stage 5ca (Smoke testing)
  - Create process_failure_analysis.md with specific gaps
  - Create guide_update_recommendations.md with 5 critical updates
  - Create lessons_learned.md with technical insights

**Stage 5cc (Final Review):**
- Update feature_02_{name}/lessons_learned.md
- Add brief debugging summary

**Stage 6c (Epic Final Review):**
- Update epic_lessons_learned.md
- Aggregate Feature 02 debugging insights
- Include in cross-feature patterns

**Stage 7 Step 4 (Update Guides):**
- Find debugging/guide_update_recommendations.md
- Extract 5 critical updates
- Create master checklist (with high priority)
- Apply ALL 5 updates to guides
- Verify 100% application
- Future epics now have improved guides

---

## Summary

**Debugging lessons are collected at:**
- Stage 5c (feature debugging)
- Stage 6 (epic debugging)

**Debugging lessons are aggregated at:**
- Stage 5cc (feature lessons_learned.md)
- Stage 6c (epic_lessons_learned.md)

**Debugging lessons are applied at:**
- **Stage 7 Step 4 (Update Guides)** ← ONLY place where guides are updated

**Critical Requirements:**
1. Must find ALL debugging files (3 types × N features + epic)
2. Must create master checklist with priority
3. Must apply 100% of lessons (no skipping)
4. Debugging lessons have HIGHER priority than general lessons

**Result:** Every debugging session improves the workflow, preventing same bugs in future epics.

---

*End of DEBUGGING_LESSONS_INTEGRATION.md*
