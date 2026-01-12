# PHASE 4b: Root Cause Analysis (Per Issue) - MANDATORY

**Purpose:** Analyze WHY the bug existed and HOW to prevent it in future epics through guide improvements

**When to Use:** Immediately after user confirms fix (Phase 4), before moving to next issue

**Previous Phase:** PHASE 4 (User Verification) - See `debugging/resolution.md`

**Next Phase:** Next issue OR PHASE 5 (Loop Back) if all issues resolved

**Time Required:** 10-20 minutes per issue (captures lessons while context is fresh)

---

## 🚨 CRITICAL: Why This Phase Is Mandatory

**Historical Problem:**
- Bugs were fixed but lessons learned only at S7.P1 (weeks later)
- Root cause analysis happened in aggregate (Phase 5), losing individual context
- Guide improvements were generic, not tied to specific bugs

**New Approach (#12 Requirement):**
- **IMMEDIATE** root cause analysis while context is fresh
- **USER CONFIRMS** root cause before documenting
- **INCREMENTAL** guide improvements captured per bug
- **PRIORITIZED** lessons (debugging bugs → P0/P1 priority in S7.P1)

**Result:** Higher quality guide improvements that prevent same bugs in future epics

---

## Trigger Condition

This process is triggered when:
- ✅ Issue fix implemented (Phase 3 complete)
- ✅ User confirmed fix (Phase 4 complete - user said "YES, fixed")
- ✅ Issue marked 🟢 FIXED in ISSUES_CHECKLIST.md

**Do NOT skip this phase.** Every user-confirmed bug fix MUST have root cause analysis.

---

## Step 1: 5-Why Root Cause Analysis

**Goal:** Understand the REAL reason the bug existed (not just the technical cause)

### 1.1: Start with the Bug Symptom

**Ask yourself:**
```
WHY #1: Why did this bug occur?
→ {Technical answer - e.g., "Null pointer exception in calculate_score()"}

WHY #2: Why did that technical issue exist?
→ {Implementation answer - e.g., "Missing null check for injured players"}

WHY #3: Why was that missing from implementation?
→ {Planning answer - e.g., "Edge case not identified in implementation_plan.md"}

WHY #4: Why wasn't that edge case identified?
→ {Process answer - e.g., "Iteration 9 (Edge Case Analysis) didn't consider injury status"}

WHY #5: Why didn't Iteration 9 catch it?
→ {Guide gap - e.g., "s5_p2_planning_round2.md doesn't mention checking player status fields"}
```

**Continue until you reach a PROCESS or GUIDE gap (not just technical cause).**

---

### 1.2: Categorize the Root Cause

**Select ONE primary category:**

**A. Missing Guide Section**
- Guide exists but doesn't cover this scenario
- Example: "s5_p2_planning_round2.md Iteration 9 doesn't mention checking entity status fields"

**B. Unclear Guide Instruction**
- Guide mentions it but not clearly enough
- Example: "smoke_testing.md Part 3 says 'verify output data' but doesn't specify checking for nulls"

**C. Missing Mandatory Gate**
- No checkpoint to catch this type of issue
- Example: "No gate between Stage 5a and 5b to verify edge cases were actually tested"

**D. Process Gap**
- No workflow step covers this scenario
- Example: "No step to verify API contract assumptions against actual API behavior"

**E. Tool/Template Gap**
- Missing template, checklist, or tool support
- Example: "No edge case checklist template to systematically identify scenarios"

**F. Not a Process Issue** (User can override this)
- Domain-specific knowledge required (not preventable by guides)
- Example: "Fantasy football scoring rules are complex and context-dependent"

---

## Step 2: Identify Prevention Point

**Goal:** Determine which stage/guide SHOULD have caught this bug

### 2.1: Trace Back Through Workflow

**For each stage, ask: "Could this guide have caught this bug?"**

**Stage 5a (Implementation Planning):**
- Round 1, Iteration 4 (Algorithm Traceability): Should algorithm have included this?
- Round 1, Iteration 7 (Integration Gap Check): Should integration point have been verified?
- Round 2, Iteration 9 (Edge Case Analysis): Should edge case have been identified?
- Round 2, Iteration 15 (Test Coverage): Should test have covered this?
- Round 3, Iteration 23a (Spec Audit): Should spec have included this requirement?

**Stage 5b (Implementation Execution):**
- Mini-QC checkpoints: Should QC have caught this?
- Unit tests: Should test have existed for this?

**S5.P5 (Smoke Testing):**
- Part 1 (Import Test): Should import have failed?
- Part 2 (Entry Point Test): Should entry point have caught this?
- Part 3 (E2E Test): Should E2E test have caught this? (This is where it WAS caught)

**S5.P6 (QC Rounds):**
- Round 1-3: Which round should have caught this?

**Stage 2 (Specification):**
- Should spec.md have included this requirement?

---

### 2.2: Identify the "Should Have Caught" Stage

**Record:**
```markdown
## Prevention Point

**This bug SHOULD have been caught at:**
- Stage: {Stage 5a / 5b / S5.P5 / S5.P6 / 2 / etc.}
- Specific Step: {Iteration 9 / QC Round 1 / etc.}
- Guide: {s5_p2_planning_round2.md / qc_rounds.md / etc.}
- Specific Section: {Iteration 9: Edge Case Analysis}

**Why it wasn't caught:**
{Specific guide gap, unclear instruction, or missing checkpoint}
```

---

## Step 3: Draft Guide Improvement Proposal

**Goal:** Create a SPECIFIC, ACTIONABLE guide improvement

### 3.1: Define the Improvement

**Template:**
```markdown
## Proposed Guide Improvement for Issue #{number}

**Affected Guide:** `{path/to/guide.md}`
**Section:** {specific section name}
**Lines:** {approximate line numbers if known}

**Current State (PROBLEM):**
```
{Quote current text from guide, OR note "Section doesn't exist"}
```

**Proposed Change (SOLUTION):**
```
{Write NEW text OR addition to guide}

**Additions/changes in BOLD for clarity:**
- Add new checkpoint: **"Verify all entity status fields (active, injured, etc.)"**
- Add to iteration 9 checklist: **"[ ] Player status edge cases (injured, bye week, inactive)"**
```

**Rationale:**
This bug ({brief description}) occurred because {reason}. Adding this checkpoint would force agents to systematically verify all entity status fields during edge case analysis, preventing similar bugs in future epics.

**Impact if Not Fixed:**
{What happens if this guide gap remains}
- Future epics will likely encounter same bug with player status
- Wasted debugging time (estimated {X} hours per epic)
- User frustration
```

---

### 3.2: Assign Priority Level

**Priority Guidelines:**

**P0 (Critical):**
- Prevents catastrophic bugs (data loss, system crash, security issues)
- Prevents bugs that reached user testing or production
- Prevents bugs that caused epic restart

**P1 (High):**
- Prevents bugs that reached QC rounds or smoke testing
- Significantly improves quality (prevents major rework)
- Prevents bugs that took >4 hours to debug

**P2 (Medium):**
- Prevents bugs that were caught quickly (<2 hours debug)
- Moderate improvement (clarifies ambiguous instruction)
- Prevents minor bugs (cosmetic, non-critical)

**P3 (Low):**
- Minor improvement (better wording)
- Edge case that's unlikely to recur
- Cosmetic guide fixes

**For debugging bugs discovered during testing:**
- Smoke Testing → Usually P1 (caught early but still got through planning)
- QC Rounds → Usually P1 (got through implementation)
- User Testing → Always P0 (got through ALL our gates)

**Record:**
```markdown
**Recommended Priority:** P1 (High)
**Reasoning:** Bug reached smoke testing (got through Stage 5a + 5b), 3 hours debugging time
```

---

## Step 4: Present to User for Confirmation

**Goal:** Get user to confirm root cause analysis before documenting

### 4.1: Present Analysis to User

**Use this template:**

````markdown
## Root Cause Analysis for Issue #{number}

I've analyzed why this bug existed and how we can prevent it in future epics.

---

### 5-Why Analysis

**WHY did this bug occur?**

1. **Technical Cause:** {immediate technical reason}
2. **Implementation Gap:** {why implementation had this gap}
3. **Planning Gap:** {why planning didn't catch it}
4. **Process Gap:** {which iteration/stage should have caught it}
5. **Guide Gap:** {what's missing or unclear in guides}

**Root Cause Category:** {A/B/C/D/E/F from Step 1.2}

---

### Prevention Point

**This bug SHOULD have been caught at:**
- **Stage:** {Stage 5a/5b/etc.}
- **Step:** {Iteration X / QC Round X}
- **Guide:** `{guide name}`
- **Why it wasn't caught:** {specific gap}

---

### Proposed Guide Improvement

**Guide to Update:** `{path/to/guide.md}`

**Current State (BEFORE):**
```
{current text or "Section doesn't exist"}
```

**Proposed Addition/Change (AFTER):**
```
{proposed new text with **BOLD** for changes}
```

**Rationale:**
{Why this prevents future bugs}

**Recommended Priority:** {P0/P1/P2/P3} ({reasoning})

---

## Question for You

**Do you agree with this root cause analysis?**

Options:
1. **AGREE** - Root cause is accurate, guide improvement is appropriate
2. **MODIFY** - Root cause is close but needs adjustment (please provide feedback)
3. **DISAGREE** - This is not a process/guide issue (it's domain-specific or unavoidable)
4. **DISCUSS** - I have questions or want to explore alternative improvements

If you choose MODIFY or DISAGREE, please explain:
- What's inaccurate about the analysis?
- What would be a better root cause?
- What guide improvement would you prefer?
````

**Wait for user response before proceeding.**

---

### 4.2: Process User Response

#### If User Says AGREE

**Action:**
1. Proceed to Step 5 (Document in guide_update_recommendations.md)
2. Mark root cause analysis as confirmed
3. Move to next issue or Phase 5

---

#### If User Says MODIFY

**User provides feedback like:**
> "The root cause is close, but I think the issue is actually in Iteration 4 (Algorithm Traceability), not Iteration 9. The algorithm should have explicitly included status field checks."

**Action:**
1. Revise the root cause analysis based on user feedback
2. Update:
   - Prevention point (Iteration 4 instead of 9)
   - Guide improvement (update s5_p1_planning_round1.md instead)
   - Priority if needed
3. Present revised analysis to user
4. Repeat until user AGREES

---

#### If User Says DISAGREE

**User provides reasoning like:**
> "This isn't a process gap - fantasy football has hundreds of edge cases and we can't enumerate them all in guides. This is just domain complexity."

**Action:**
1. Mark root cause as "Not a Process Issue" in issue file
2. **Do NOT add to guide_update_recommendations.md**
3. Document user's reasoning in issue_{number}_{name}.md
4. Move to next issue or Phase 5

**Update issue file:**
```markdown
## Root Cause Analysis

**Status:** NOT A PROCESS ISSUE (User Confirmed)
**User Reasoning:** {quote user's explanation}
**Technical Root Cause:** {keep the technical cause for reference}

**No guide improvement proposed.**
```

---

#### If User Says DISCUSS

**User asks questions like:**
> "Wouldn't it be better to create a separate edge case checklist template instead of adding to Iteration 9?"

**Action:**
1. Discuss the alternative with user
2. Collaborate on the best guide improvement approach
3. Update proposal based on discussion
4. Present revised proposal
5. Repeat until user AGREES or DISAGREES

---

## Step 5: Document in guide_update_recommendations.md

**Goal:** Add user-confirmed guide improvement to recommendations file for S7.P1

### 5.1: Create or Update File

**File Location:**
- Feature-level: `feature_XX_{name}/debugging/guide_update_recommendations.md`
- Epic-level: `{epic_name}/debugging/guide_update_recommendations.md`

**If file doesn't exist, create with template below.**

---

### 5.2: File Template (First Time)

```markdown
# Guide Update Recommendations - {Feature/Epic Name}

**Purpose:** Concrete, actionable guide improvements identified during debugging

**Source:** Per-issue root cause analysis (Phase 4b of debugging protocol)

**Usage:** These recommendations will be presented to user in S7.P1 for approval

**Priority Levels:**
- **P0 (Critical):** Prevents catastrophic bugs, user testing failures
- **P1 (High):** Prevents bugs reaching QC/smoke testing, major rework
- **P2 (Medium):** Moderate improvements, clarifies ambiguity
- **P3 (Low):** Minor improvements, cosmetic fixes

---

## Recommendation #1: {Short Title}

**Source Issue:** Issue #{number} - {issue name}
**Affected Guide:** `{path/to/guide.md}`
**Section:** {section name}
**Priority:** {P0/P1/P2/P3}
**User Confirmed:** ✅ YES (Date: {YYYY-MM-DD})

### Root Cause

{Brief summary of why bug existed}

**5-Why Analysis:**
1. {Technical cause}
2. {Implementation gap}
3. {Planning gap}
4. {Process gap}
5. {Guide gap} ← ROOT CAUSE

### Current State (BEFORE)

```markdown
{Current text from guide, OR "Section doesn't exist"}
```

### Proposed Change (AFTER)

```markdown
{Proposed new text with **BOLD** for additions/changes}
```

### Rationale

{Why this prevents future bugs}

### Impact Assessment

**Who benefits:** {Which agents/stages benefit}
**When it helps:** {Specific situations}
**Severity if unfixed:** {What happens without this fix}
**Estimated debugging time saved:** {X hours per epic}

---

{Repeat for each issue}
```

---

### 5.3: Add Recommendation for Current Issue

**Append to file:**

```markdown
## Recommendation #{next_number}: {Short Title from User-Confirmed Analysis}

**Source Issue:** Issue #{issue_number} - {issue_name}
**Affected Guide:** `{guide_path}`
**Section:** {section}
**Priority:** {P0/P1/P2/P3}
**User Confirmed:** ✅ YES (Date: {YYYY-MM-DD HH:MM})

{Rest of template filled from user-confirmed analysis}
```

---

## Step 6: Update Issue File

**Goal:** Record completed root cause analysis in issue file

### 6.1: Add Root Cause Section

**File:** `debugging/issue_{number}_{name}.md`

**Add after "User Verification" section:**

```markdown
## Root Cause Analysis (Phase 4b)

**Status:** ✅ COMPLETED
**Date:** {YYYY-MM-DD HH:MM}
**User Confirmed:** ✅ YES

### 5-Why Analysis

1. **Technical Cause:** {answer}
2. **Implementation Gap:** {answer}
3. **Planning Gap:** {answer}
4. **Process Gap:** {answer}
5. **Guide Gap:** {answer} ← ROOT CAUSE

**Root Cause Category:** {A/B/C/D/E/F}

### Prevention Point

**Should have been caught at:**
- Stage: {stage}
- Step: {step/iteration}
- Guide: `{guide}`
- Why missed: {reason}

### Guide Improvement

**Added to:** `debugging/guide_update_recommendations.md` - Recommendation #{number}
**Priority:** {P0/P1/P2/P3}
**Will be presented to user in S7.P1 for final approval**

### User Feedback

**User Response:** AGREE
**Additional Comments:** {any comments user provided}
```

---

## Step 7: Update ISSUES_CHECKLIST.md

**Goal:** Mark root cause analysis complete for this issue

### 7.1: Add New Column (If First Time)

**If ISSUES_CHECKLIST.md doesn't have "Root Cause?" column, add it:**

```markdown
| # | Issue Name | Status | Current Phase | User Confirmed? | Root Cause? | Discovery | Notes |
|---|------------|--------|---------------|-----------------|-------------|-----------|-------|
```

---

### 7.2: Mark Root Cause Complete

**Update the row for this issue:**

```markdown
| 1 | player_scoring_returns_null | 🟢 FIXED | Phase 4b | ✅ YES | ✅ YES | Smoke Part 3 | User confirmed fix + root cause |
```

**Key:**
- Root Cause?: ✅ YES = Analysis complete, user confirmed
- Root Cause?: ⏭️ SKIP = User said "Not a process issue"
- Root Cause?: (blank) = Not yet analyzed

---

## Step 8: Determine Next Action

**Goal:** Decide whether to move to next issue or Phase 5

### 8.1: Check for More Issues

```
Are there more issues in ISSUES_CHECKLIST.md with status NOT 🟢 FIXED?
├─ YES (more issues to resolve)
│  └─ Move to next issue (back to Phase 2 Investigation for that issue)
│     Update "Current Focus" in ISSUES_CHECKLIST.md
│     Read debugging/investigation.md for next issue
│
└─ NO (all issues resolved)
   └─ Move to Phase 5 (Loop Back to Testing)
      Read debugging/loop_back.md
```

**CRITICAL:** Phase 5 Step 3 (Cross-Bug Pattern Analysis) will review ALL the guide_update_recommendations.md entries you created here and identify patterns across bugs.

---

## Completion Checklist

**Step 4b is complete for this issue when:**

- [ ] 5-Why analysis performed (reached guide/process gap)
- [ ] Root cause category identified (A/B/C/D/E/F)
- [ ] Prevention point determined (stage/step/guide)
- [ ] Guide improvement drafted (before/after with rationale)
- [ ] Priority assigned (P0/P1/P2/P3)
- [ ] Presented to user for confirmation
- [ ] User response processed (AGREE/MODIFY/DISAGREE/DISCUSS)
- [ ] If AGREE or MODIFY: Added to guide_update_recommendations.md
- [ ] If DISAGREE: Documented as "Not a Process Issue"
- [ ] Issue file updated with root cause section
- [ ] ISSUES_CHECKLIST.md updated with "Root Cause?: ✅ YES or ⏭️ SKIP"
- [ ] Next action determined (next issue or Phase 5)

---

## Common Mistakes to Avoid

❌ **Stopping at technical cause**
- BAD: "Root cause: Missing null check"
- GOOD: "Root cause: s5_p2_planning_round2.md Iteration 9 doesn't mention verifying entity status fields"

❌ **Skipping user confirmation**
- BAD: Agent decides root cause and adds to recommendations
- GOOD: Present analysis, wait for user, process response

❌ **Generic guide improvements**
- BAD: "Add more edge case checks"
- GOOD: "Add checkbox to Iteration 9: '[ ] Entity status fields (active, injured, suspended, bye week)'"

❌ **Wrong priority level**
- BAD: P3 for bug that reached user testing
- GOOD: P0 for bug that reached user testing (got through all our gates)

❌ **Forgetting to update checklist**
- Checklist must show ✅ YES in "Root Cause?" column before moving on

---

## Why This Matters

**Before Phase 4b:**
- Root cause analysis happened weeks later (Phase 5, S7.P1)
- Context was lost ("Why did we make that decision?")
- Guide improvements were generic and vague
- User wasn't involved in root cause validation

**After Phase 4b:**
- Root cause analyzed IMMEDIATELY (while context is fresh)
- User confirms REAL reason (not agent assumptions)
- Guide improvements are SPECIFIC and ACTIONABLE
- S7.P1 presents high-quality, pre-validated proposals
- Future epics benefit from concrete, tested improvements

**Historical evidence:** Bugs analyzed immediately have 3x higher quality guide improvements vs. bugs analyzed weeks later.

---

**Next Phase:** Move to next issue OR Phase 5 (Loop Back to Testing)
