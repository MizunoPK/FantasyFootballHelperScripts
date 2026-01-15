# S2: Feature Deep Dives
## S2.P3: Refinement Phase

**File:** `s2_p3_refinement.md`

---

🚨 **MANDATORY READING PROTOCOL**

**Before starting this phase:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**What is this phase?**
Refinement Phase is where you resolve all open questions through interactive dialogue (ONE at a time), adjust scope if needed, align with completed features, and get user approval on acceptance criteria. This phase ensures the spec is complete, validated, and ready for implementation.

**When do you use this guide?**
- S2.P2 (Specification Phase) complete
- spec.md has Epic Intent section and requirement traceability
- checklist.md has open questions
- Phase 2.5 (Spec-to-Epic Alignment Check) passed

**Key Outputs:**
- ✅ All checklist questions resolved (zero open items)
- ✅ Spec updated in real-time after each answer
- ✅ Feature scope validated (not too large, properly scoped)
- ✅ Cross-feature alignment complete (no conflicts with other features)
- ✅ Acceptance criteria created and user-approved

**Time Estimate:**
1-2 hours per feature (depends on number of questions and feature complexity)

**Exit Condition:**
Refinement Phase is complete when all checklist questions are resolved, scope is validated, cross-feature alignment is done, and user has approved acceptance criteria

**Examples:** For detailed examples and templates, see `reference/stage_2/refinement_examples.md`

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ONE question at a time (NEVER batch questions)
   - Ask question
   - Wait for user answer
   - Update spec/checklist IMMEDIATELY
   - Evaluate for new questions
   - Then ask next question

1.5. ⚠️ INVESTIGATION COMPLETE ≠ QUESTION RESOLVED
   - Agent investigates → Status: PENDING USER APPROVAL
   - User explicitly approves → Status: RESOLVED
   - NEVER mark questions as resolved without explicit approval
   - Research findings ≠ User approval

   WRONG: Investigate → Mark RESOLVED → Add requirement
   CORRECT: Investigate → Mark PENDING → User approves →
            Mark RESOLVED → Add requirement

2. ⚠️ Update spec.md and checklist.md IMMEDIATELY after each answer
   - Do NOT batch updates
   - Keep files current in real-time
   - Document user's exact answer or paraphrase

3. ⚠️ If checklist grows >35 items, STOP and propose split
   - Trigger: More than 35 checklist items
   - Action: Propose splitting into multiple features
   - Requirement: Get user approval before splitting
   - If approved: Return to S1 to create new features

4. ⚠️ Cross-feature alignment is MANDATORY (not optional)
   - Compare to ALL features with "S2 Complete"
   - Look for: Conflicts, duplicates, incompatible assumptions
   - Resolve conflicts before proceeding
   - Document alignment verification

5. ⚠️ Acceptance criteria require USER APPROVAL (mandatory gate)
   - Create "Acceptance Criteria" section in spec.md
   - List EXACT files, structures, behaviors
   - Present to user for approval
   - Wait for explicit approval
   - Document approval timestamp

6. ⚠️ Every user answer creates new requirement with traceability
   - Source: "User Answer to Question N (checklist.md)"
   - Add to spec.md immediately
   - Update checklist to mark question resolved
```

---

## Critical Decisions Summary

**This phase has ONE critical decision point:**

### Decision Point: Phase 6 - User Approval (MANDATORY)

**Question:** Does user approve acceptance criteria?
- **If YES:** Mark approval timestamp, proceed to mark feature complete
- **If NO:** Update spec based on feedback, re-present for approval
- **Impact:** Cannot proceed to S3 or implementation without user approval

---

## Prerequisites Checklist

**Before starting Refinement Phase (STAGE_2c), verify:**

□ **STAGE_2b complete:**
  - Phase 2 complete: spec.md has Epic Intent section, requirements with traceability
  - Phase 2 complete: checklist.md exists with open questions
  - Phase 2.5 complete: Spec-to-Epic Alignment Check PASSED
  - spec.md has valid sources for all requirements (Epic/User Answer/Derived)

□ **Files exist and are current:**
  - feature_{N}_{name}/spec.md exists with Epic Intent section
  - feature_{N}_{name}/checklist.md exists with questions
  - feature_{N}_{name}/README.md has Agent Status

□ **Research foundation exists:**
  - epic/research/{FEATURE_NAME}_DISCOVERY.md exists (from Phase 1)
  - Research completeness audit passed (Phase 1.5)

□ **Agent Status updated:**
  - Last guide: stages/s_2/phase_1_specification.md
  - Current phase: Ready to start Phase 3 (Interactive Question Resolution)

**If any prerequisite fails:**
- ❌ Do NOT start Refinement Phase
- Complete missing prerequisites first
- Return to STAGE_2b if Phase 2.5 not passed

---

## Phase 3: Interactive Question Resolution

**Goal:** Resolve ALL checklist questions ONE AT A TIME

**⚠️ CRITICAL:** This is the heart of the refinement phase. Do NOT batch questions. Ask one, wait, update, then ask next.

---

### Step 3.1: Select Next Question

**Priority order:**
1. **Blocking questions** - Must be answered before other questions make sense
2. **High-impact questions** - Affect algorithm or data structure design
3. **Low-impact questions** - Implementation details

**How to identify priority:**
- Read all open questions in checklist.md
- Identify dependencies (some questions depend on others)
- Start with questions that unlock other questions

**Examples:** See `reference/stage_2/refinement_examples.md` → Phase 3 Examples for question prioritization examples

---

### Step 3.2: Ask ONE Question

**Format:**

```markdown
I have a question about Feature {N} ({Name}):

## Question {N}: {Title}

**Context:** {Why this matters, what we're trying to accomplish}

**Options:**

A. **{Option A}**
   - Pros: {benefits}
   - Cons: {drawbacks}

B. **{Option B}**
   - Pros: {benefits}
   - Cons: {drawbacks}

C. **{Option C}**
   - Pros: {benefits}
   - Cons: {drawbacks}

**My recommendation:** Option {X} because {reason}

**What do you prefer?** (or suggest a different approach)
```

**Best practices:**
- Provide 2-4 well-defined options
- Include pros/cons for each option
- Give your recommendation with reasoning
- Allow user to suggest alternative
- Keep context brief but informative

**Examples:** See `reference/stage_2/refinement_examples.md` → Phase 3 Examples for complete question-answer cycles

---

### Step 3.3: WAIT for User Answer

⚠️ **STOP HERE - Do NOT proceed without user answer**

**Do NOT:**
- Ask multiple questions in one message
- Proceed to next question while waiting
- Make assumptions about what user will choose
- Continue working on other phases

**DO:**
- Wait for user response
- Be ready to answer follow-up questions
- Be ready to present additional options if user asks

**Update Agent Status:**
```markdown
**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE
**Current Step:** Phase 3 - Waiting for answer to Question {N}
**Current Guide:** stages/s_2/phase_2_refinement.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- ONE question at a time
- Update immediately after answer
- Wait for user before proceeding

**Progress:** {M}/{N} questions resolved
**Next Action:** Wait for user answer to Question {current_question_number}
**Blockers:** Waiting for user input on {question_topic}
```

---

### Step 3.4: Update Spec & Checklist Immediately

**After user answers**, update files IMMEDIATELY (before asking next question):

**Update checklist.md:**
```markdown
### Question {N}: {Title}
- [x] **RESOLVED:** {User's choice}

**User's Answer:**
{Paste user's exact answer or paraphrase}

**Implementation Impact:**
- {How this affects the implementation}
- {What needs to be added to spec}
- {Any new questions this creates}
```

**Update spec.md:**

Add requirement with new source:

```markdown
### Requirement {N}: {Name}

**Description:** {What this requirement does}

**Source:** User Answer to Question {N} (checklist.md)
**Traceability:** User confirmed preference on {date}

**Implementation:**
{Details based on user's answer}

**Technical Details:**
- {Specific implementation notes}
- {Edge cases to handle}
- {Dependencies or prerequisites}
```

**Examples:** See `reference/stage_2/refinement_examples.md` → Phase 3 Examples for complete update examples

---

### Step 3.5: Evaluate for New Questions

**After updating files, ask:**
- Did this answer create NEW questions?
- Did this answer resolve OTHER questions?
- Do we need clarification on any part of the answer?

**Update checklist.md if needed:**
- Add new questions that arose from answer
- Mark other questions resolved if answer made them N/A
- Document dependencies between questions

**Examples:** See `reference/stage_2/refinement_examples.md` → Phase 3 Examples for question evaluation examples

---

### Step 3.6: Repeat Until ALL Questions Resolved

Continue asking questions ONE AT A TIME until checklist shows:

```markdown
**Checklist Status:** 0 open questions, {N} resolved
```

**After each question, follow this cycle:**
1. Ask ONE question (Step 3.2)
2. Wait for answer (Step 3.3)
3. Update spec & checklist immediately (Step 3.4)
4. Evaluate for new questions (Step 3.5)
5. Select next question (Step 3.1)
6. Repeat

**Update Agent Status after each question:**
```markdown
**Progress:** Phase 3 - Question {M}/{N} answered ({M} resolved, {remaining} open)
**Next Action:** Ask Question {M+1}
**Blockers:** None
```

**When all questions resolved:**
```markdown
**Progress:** Phase 3 - COMPLETE (all {N} questions resolved)
**Next Action:** Phase 4 - Dynamic Scope Adjustment
**Blockers:** None
```

---

## Phase 4: Dynamic Scope Adjustment

**Goal:** Ensure feature scope is reasonable and properly categorized

**⚠️ CRITICAL:** Features with >35 checklist items become unmaintainable. Split if needed.

---

### Step 4.1: Count Checklist Items

**Count all resolved and open items in checklist.md**

**Document the count:**
```markdown
**Checklist Item Count:** {total} items ({resolved} resolved, {open} open)
```

---

### Step 4.2: Evaluate Feature Size

**Decision tree:**

**If checklist has >35 items:**
- ✋ **STOP** - Feature is too large
- Action: Propose split into multiple features
- Requirement: Get user approval before splitting
- Next: Step 4.3 (Propose Split)

**If checklist has 20-35 items:**
- ✅ **OK** - Feature is appropriately sized
- Action: Document as "medium complexity"
- Next: Step 4.4 (Check for New Work)

**If checklist has <20 items:**
- ✅ **OK** - Feature is reasonably sized
- Action: Document as "straightforward"
- Next: Step 4.4 (Check for New Work)

**Update Agent Status:**
```markdown
**Progress:** Phase 4 - Scope evaluation ({total} checklist items)
**Next Action:** {Propose split / Check for new work}
**Blockers:** None
```

---

### Step 4.3: Propose Feature Split (If >35 Items)

**If checklist >35 items, present split proposal to user**

**Use format from:** `reference/stage_2/refinement_examples.md` → Phase 4 Examples → Feature Too Large

**If user approves split:**
- Document approval in current feature README.md
- Return to S1 (Epic Planning) to restructure
- Create new feature folders
- Split spec and checklist content
- Update epic EPIC_README.md
- Resume S2 for each new feature

**If user rejects split:**
- Document user decision to keep as single feature
- Note in feature README.md: "User approved large scope ({total} items)"
- Proceed to Step 4.4
- Be aware of increased implementation complexity

---

### Step 4.4: Check for New Work Discovered

**During question resolution, you may have discovered new work not in original epic**

**Decision tree for new work:**

**Option A: New work is independent subsystem**
- Example: "We need a new CSV parser module"
- **Action:** Propose as NEW FEATURE (separate from current feature)
- **Rationale:** Independent subsystems should be their own features
- **Next:** Present to user, if approved return to S1

**Option B: New work extends current feature**
- Example: "We need to add logging to ADP loader"
- **Action:** Add to current feature's spec (expanded scope)
- **Rationale:** These are implementation details, not separate features
- **Next:** Update spec.md and checklist.md, continue with current feature

**Option C: No new work discovered**
- **Action:** Document "No scope creep identified"
- **Next:** Proceed to Phase 5

**Examples:** See `reference/stage_2/refinement_examples.md` → Phase 4 Examples for new work discovery examples

**Update Agent Status:**
```markdown
**Progress:** Phase 4 - COMPLETE (scope validated, no split needed)
**Next Action:** Phase 5 - Cross-Feature Alignment
**Blockers:** None
```

---

## Phase 5: Cross-Feature Alignment

**Goal:** Compare this feature's spec to all completed features, resolve conflicts

**⚠️ CRITICAL:** This prevents features from having incompatible assumptions or duplicate work.

**Skip if:** This is the FIRST feature in the epic (no other features to compare to)

---

### Step 5.1: Identify Completed Features

**Check epic EPIC_README.md Feature Tracking table:**

Look for features with "S2 Complete" marked [x]

**Document:**
```markdown
**Features to Compare:**
- Feature {M}: {Name} (completed S2)

**Current Feature:**
- Feature {N}: {Name}
```

**If this is the first feature:**
```markdown
**Features to Compare:** None (this is first feature)

**Action:** Skip Phase 5 (Cross-Feature Alignment)
**Next:** Phase 6 (Acceptance Criteria & User Approval)
```

---

### Step 5.2: Compare Specs Systematically

**For EACH completed feature, perform pairwise comparison:**

**Read completed feature's spec.md:**
- Use Read tool to load entire spec
- Focus on: Components Affected, Data Structures, Requirements, Algorithms

**Create comparison document:**

`epic/research/ALIGNMENT_{current_feature}_vs_{other_feature}.md`

**Use template from:** `reference/stage_2/refinement_examples.md` → Phase 5 Examples → Complete Feature Comparison

**Comparison categories:**
1. Components Affected (overlapping files/modules)
2. Data Structures (overlapping data formats)
3. Requirements (duplicate work)
4. Assumptions (incompatible assumptions)
5. Integration Points (dependencies)

---

### Step 5.3: Resolve Conflicts

**For EACH conflict found:**

**Option A: Update current feature (Feature N)**
- Modify spec.md to align with completed feature
- Update checklist.md if new questions arise
- Document change with reason

**Option B: Update completed feature (Feature M)**
- **CAUTION:** Completed feature may already be in implementation
- Check if other feature is in S5 (implementation)
- If yes, coordinate changes with implementation
- If no (only S2 complete), update its spec

**Option C: Create shared utility**
- If both features need same functionality
- Create new Feature X: Shared Utility
- Both features depend on Feature X
- Return to S1 to create new feature

**Document resolution in both specs**

**Examples:** See `reference/stage_2/refinement_examples.md` → Phase 5 Examples → Alignment with Conflicts Found

---

### Step 5.4: Get User Confirmation on Conflicts (If Any)

**If CRITICAL conflicts found, present to user using format from:**
`reference/stage_2/refinement_examples.md` → Phase 5 Examples

**If user approves resolution:**
- Update spec.md and checklist.md
- Document approval in alignment report
- Update completed feature if needed
- Continue to Step 5.5

**If NO conflicts found:**
- Document "Zero conflicts with Feature {M}"
- No user confirmation needed
- Continue to Step 5.5

---

### Step 5.5: Document Alignment Verification

**Create summary in current feature's spec.md:**

```markdown
## Cross-Feature Alignment

**Compared To:**
- Feature {M}: {Name} (S2 Complete) - {Date}

**Alignment Status:** ✅ No conflicts / ⚠️ Conflicts resolved

**Details:**
{Brief summary of comparison}

**Changes Made:**
{Any changes to this spec based on alignment}

**Verified By:** Agent
**Date:** {YYYY-MM-DD}
```

**Update Agent Status:**
```markdown
**Progress:** Phase 5 - COMPLETE (aligned with {N} features, {M} conflicts resolved)
**Next Action:** Phase 6 - Acceptance Criteria & User Approval
**Blockers:** None
```

---

## Phase 6: Acceptance Criteria & User Approval

**Goal:** Create user-facing summary of what this feature will do, get explicit approval

**⚠️ CRITICAL:** This is a MANDATORY gate. Cannot proceed to S3 without user approval.

**Why this matters:**
- User needs to understand EXACTLY what will be implemented
- This is the last chance to adjust before implementation planning
- User approval locks the spec (changes after this require returning to S2)

**When user requests investigation (e.g., "check compatibility"), use systematic framework:**

**Comprehensive Investigation Checklist:**

**Category 1: Method/Function Calls**
- Where does X call the new code?
- Do they pass new parameters?
- Are default values correct?

**Category 2: Configuration/Data Loading** ⚠️ (commonly missed)
- Where does X create ConfigManager/DataManager?
- How does it load new config keys?
- What if JSON missing keys?

**Category 3: Integration Points**
- Does new code affect X's flow?
- Other X files affected?

**Category 4: Timing/Dependencies**
- Transition period issues?
- Implementation sequencing?

**Category 5: Edge Cases**
- Old config with new code?
- New config with old code?

**After investigation:**
- Mark checklist status: PENDING USER APPROVAL
- Present findings covering ALL 5 categories
- Wait for explicit user approval
- ONLY THEN mark as RESOLVED

---

### Step 6.1: Create Acceptance Criteria Section

**Add to spec.md (near the end, before any appendices):**

**Use template from:** `reference/stage_2/refinement_examples.md` → Phase 6 Examples → Complete Acceptance Criteria

**Required sections:**
1. **Behavior Changes** (new functionality, modified functionality, no changes)
2. **Files Modified** (new files, existing files modified, data files)
3. **Data Structures** (new structures, modified structures)
4. **API/Interface Changes** (new methods, modified methods, no changes)
5. **Testing** (test counts, coverage targets, edge cases)
6. **Dependencies** (depends on, blocks, external dependencies)
7. **Edge Cases & Error Handling** (edge cases handled, error conditions)
8. **Documentation** (user-facing, developer documentation)
9. **User Approval** (checkbox, timestamp placeholder, notes)

---

### Step 6.2: Present to User for Approval

**Message to user:**

```markdown
## Feature {N} ({Name}) - Ready for Approval

I've completed the deep dive for Feature {N}. Here's a summary:

**Spec Status:**
- All {N} checklist questions resolved
- Cross-feature alignment complete (compared to {M} features)
- Scope validated ({item_count} checklist items)

**What This Feature Will Do:**

{Brief 2-3 sentence summary}

**Impact:**
- Files modified: {count} new, {count} modified
- API changes: {summary}
- Dependencies: {summary}

**Full Details:**

Please review the "Acceptance Criteria" section in spec.md:
`feature-updates/KAI-{N}-{epic_name}/feature_{N}_{name}/spec.md`

**Acceptance Criteria Section includes:**
- Exact behavior changes
- All files that will be modified
- Data structure changes
- API/interface changes
- Testing approach
- Edge cases and error handling

**Next Steps:**

If you approve these acceptance criteria:
- I'll mark the approval checkbox and timestamp
- I'll mark Feature {N} as "S2 Complete" in epic tracking
- I'll proceed to next feature (if any) or S3 (Cross-Feature Sanity Check)

If you want changes:
- Let me know what to modify
- I'll update the spec and re-present for approval

**Do you approve these acceptance criteria?**
```

**Examples:** See `reference/stage_2/refinement_examples.md` → Phase 6 Examples → User Approval Process

---

### Step 6.3: WAIT for User Approval

⚠️ **STOP HERE - Do NOT proceed without explicit user approval**

**Do NOT:**
- Mark feature complete without approval
- Proceed to next feature without approval
- Proceed to S3 without approval
- Assume approval if user is silent

**DO:**
- Wait for explicit "yes", "approved", "looks good", etc.
- Answer any questions about acceptance criteria
- Make modifications if user requests changes
- Re-present if spec is updated

**Update Agent Status:**
```markdown
**Progress:** Phase 6 - Waiting for user approval of acceptance criteria
**Next Action:** Wait for user to approve/request changes
**Blockers:** Waiting for user approval on acceptance criteria
```

---

### Step 6.4: Handle User Response

**If user APPROVES:**

Update spec.md:
```markdown
## User Approval

- [x] **I approve these acceptance criteria**

**Approval Timestamp:** {YYYY-MM-DD HH:MM}

**Approval Notes:**
User approved on {date} with no modifications requested.
```

Continue to Step 6.5 (Mark Feature Complete)

---

**If user REQUESTS CHANGES:**

1. Document requested changes
2. Update spec.md based on feedback
3. Update checklist.md if new questions arose
4. Re-present updated acceptance criteria
5. Wait for approval again (return to Step 6.3)

**Examples:** See `reference/stage_2/refinement_examples.md` → Phase 6 Examples for change handling

---

**If user REJECTS (major changes needed):**

1. Document rejection
2. Determine what phase to return to:
   - Fundamental misunderstanding → Return to Phase 0 (Epic Intent)
   - Research gap → Return to Phase 1 (Targeted Research)
   - Wrong requirements → Return to Phase 2 (Spec & Checklist)
   - Wrong answers to questions → Return to Phase 3 (Question Resolution)
3. Update Agent Status
4. Return to appropriate phase and restart from there

---

### Step 6.5: Mark Feature Complete (After Approval)

**Update feature README.md:**

```markdown
## Feature Completion Checklist

### S2: Feature Deep Dive
- [x] Phase 0: Epic Intent Extraction
- [x] Phase 1: Targeted Research
- [x] Phase 1.5: Research Completeness Audit
- [x] Phase 2: Spec & Checklist Creation
- [x] Phase 2.5: Spec-to-Epic Alignment Check
- [x] Phase 3: Interactive Question Resolution
- [x] Phase 4: Dynamic Scope Adjustment
- [x] Phase 5: Cross-Feature Alignment
- [x] Phase 6: Acceptance Criteria & User Approval
- **S2 Status:** ✅ COMPLETE
- **Completion Date:** {YYYY-MM-DD}

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE_COMPLETE
**Current Step:** S2 complete, ready for S3
**Current Guide:** N/A (between stages)
**Critical Rules:** S2 complete, await next feature or S3

**Progress:** S2 COMPLETE
**Next Action:** {Proceed to next feature / Proceed to S3}
**Blockers:** None
```

---

**Update epic EPIC_README.md:**

Find Feature Tracking table and mark S2 complete:

```markdown
## Feature Tracking

| Feature | Name | S2 Complete | S5 Complete | Status |
|---------|------|------------------|------------------|--------|
| 01      | {Name} | [x] {Date} | [ ] | S2 Done |
```

---

**Update Epic Completion Checklist:**

```markdown
## Epic Completion Checklist

### S2: Feature Deep Dives (Loop for each feature)
- [x] Feature 01: Spec complete, user approved ({Date})
- [ ] Feature 02: Spec complete, user approved
```

---

**Announce completion to user:**

```markdown
✅ **Feature {N} ({Name}) - S2 Complete**

**Summary:**
- Epic intent extracted and documented
- {N} questions resolved
- {M} requirements documented with traceability
- Cross-feature alignment complete ({K} features compared, {L} conflicts resolved)
- Acceptance criteria approved by user

**Files Updated:**
- spec.md: Complete with user approval
- checklist.md: All questions resolved
- README.md: S2 marked complete
- epic/research/{FEATURE_NAME}_DISCOVERY.md: Research findings
- {epic}/EPIC_README.md: Feature tracking updated

**Next Steps:**

{IF more features remain:}
- Begin S2 for next feature: Feature {N+1} ({Name})
- Repeat deep dive process

{IF all features complete S2:}
- Transition to S3 (Cross-Feature Sanity Check)
- Systematic comparison of all feature specs
- Get user sign-off on complete plan

**Ready to proceed?**
```

---

## S2 Complete Checklist (Per Feature)

**Refinement Phase (STAGE_2c) is COMPLETE when ALL of these are true:**

### Phase Completion
- [ ] Phase 3: Interactive Question Resolution complete
  - All checklist questions resolved (zero open items)
  - Spec/checklist updated after each answer
  - No batched questions

- [ ] Phase 4: Dynamic Scope Adjustment complete
  - Checklist item count documented
  - If >35 items: Split proposed and user decided
  - New work evaluated (new feature vs expanded scope)

- [ ] Phase 5: Cross-Feature Alignment complete
  - Compared to all features with "S2 Complete"
  - Conflicts identified and resolved
  - Alignment documented in spec.md

- [ ] Phase 6: Acceptance Criteria & User Approval complete
  - Acceptance Criteria section created in spec.md
  - Presented to user
  - User APPROVED (checkbox marked [x])
  - Approval timestamp documented

### File Outputs
- [ ] spec.md updated with:
  - All user answers incorporated as requirements
  - Cross-feature alignment notes
  - Acceptance Criteria section (user approved)
  - User approval checkbox marked [x]
  - Approval timestamp

- [ ] checklist.md shows:
  - ALL questions marked [x] (resolved)
  - User answers documented
  - No open [ ] questions

- [ ] README.md updated:
  - Feature Completion Checklist: S2 marked complete
  - Agent Status: Phase = DEEP_DIVE_COMPLETE

### Epic-Level Updates
- [ ] Epic EPIC_README.md updated:
  - Feature Tracking table: "[x]" for this feature's S2
  - Completion date documented

### Mandatory Gate
- [ ] ✅ Phase 6: User APPROVED acceptance criteria

**If ANY item unchecked → Refinement Phase NOT complete**

**When ALL items checked:**
✅ Refinement Phase COMPLETE
✅ S2 COMPLETE for this feature
→ Proceed to next feature's S2 OR S3 (if all features done)

---

## Completion Criteria

**STAGE_2c (Refinement Phase) is complete when:**

1. **All phases complete:**
   - Step 3: All questions resolved
   - Step 4: Scope validated
   - Step 5: Cross-feature alignment done
   - Step 6: Acceptance criteria user-approved

2. **Files current:**
   - spec.md has acceptance criteria + user approval
   - checklist.md has zero open questions
   - README.md shows S2 complete

3. **Epic updated:**
   - EPIC_README.md Feature Tracking shows "[x]" for S2
   - No blockers or waiting states

4. **User approval obtained:**
   - Acceptance criteria approved
   - Approval checkbox marked [x]
   - Approval timestamp documented

**Next Stage:** Either next feature's Research Phase (stages/s_2/phase_0_research.md) OR Cross-Feature Sanity Check (stages/s_3/cross_feature_sanity_check.md) if all features complete

---

## Next Steps

**After Refinement Phase completes:**

**If more features remain:**
- Begin S2 for next feature
- Start with STAGE_2a (Research Phase)
- Repeat all phases (0 through 6)

**If ALL features complete S2:**
- Transition to S3 (Cross-Feature Sanity Check)

📖 **READ:** `stages/s_3/cross_feature_sanity_check.md`
🎯 **GOAL:** Systematic comparison of all feature specs, final epic-level validation
⏱️ **ESTIMATE:** 30-60 minutes (for entire epic)

**S3 will:**
- Verify acceptance criteria approved for ALL features (mandatory pre-check)
- Compare all feature specs side-by-side
- Identify remaining conflicts (missed in per-feature alignment)
- Ensure requirements are aligned across all features
- Get user sign-off on complete plan before S4

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting next feature or S3.

---

*End of stages/s_2/phase_2_refinement.md*
