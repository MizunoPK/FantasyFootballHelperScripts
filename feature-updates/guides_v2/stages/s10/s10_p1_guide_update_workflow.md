# S10: Epic Cleanup
## S10.P1: Guide Update from Lessons Learned

**File:** `s10_p1_guide_update_workflow.md`

---

🚨 **MANDATORY READING PROTOCOL**

**Before starting this guide:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update EPIC_README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check EPIC_README.md Agent Status for current step
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Overview

**What is this phase?**
S10.P1 is the mandatory guide improvement workflow where you analyze lessons learned from the epic and propose specific guide updates to help future agents, with user approval for each change individually.

**When do you use this guide?**
- S10 user testing passed (Gate 7.2 - zero bugs found)
- All lessons_learned.md files are complete
- Before creating final epic commit

**Key Outputs:**
- ✅ GUIDE_UPDATE_PROPOSAL.md created with prioritized proposals (P0-P3)
- ✅ User reviewed and approved/rejected each proposal individually
- ✅ Approved guide updates applied to guides
- ✅ Separate commit created for guide updates
- ✅ reference/guide_update_tracking.md updated

**Time Estimate:**
20-45 minutes (depends on number of lessons and proposals)

**Exit Condition:**
S10.5 is complete when all proposals have been reviewed by user, approved changes applied to guides, separate commit created, and tracking updated

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL REQUIREMENTS - READ BEFORE PROCEEDING              │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Analyze ALL lessons_learned.md files
   - epic_lessons_learned.md (epic-level)
   - feature_XX_{name}/lessons_learned.md (ALL features)
   - Do NOT skip any lessons

2. ⚠️ Individual approval for EACH proposal
   - User reviews proposals one at a time
   - User can: Approve / Modify / Reject / Discuss
   - Do NOT batch approvals or assume approval

3. ⚠️ Apply ONLY approved changes
   - If user approves → apply proposal as-is
   - If user modifies → apply user's version
   - If user rejects → skip that change
   - Do NOT apply rejected proposals

4. ⚠️ Prioritize ALL proposals (P0-P3)
   - P0 (Critical): Prevents catastrophic bugs, mandatory gate gaps
   - P1 (High): Significantly improves quality, reduces major rework
   - P2 (Medium): Moderate improvements, clarifies ambiguity
   - P3 (Low): Minor improvements, cosmetic fixes

5. ⚠️ Separate commit for guide updates
   - Guide updates committed separately from epic code
   - Commit message: "docs(guides): Apply lessons from KAI-{N}-{epic_name}"
   - Do NOT mix guide updates with epic commits

6. ⚠️ Update tracking after applying changes
   - Add entries to reference/guide_update_tracking.md
   - Document approved, modified, and rejected proposals
   - Update metrics section

7. ⚠️ Scope: ENTIRE guides_v2/ directory + CLAUDE.md
   - 🚨 CRITICAL: "Guides" = EVERY FILE in feature-updates/guides_v2/
   - This includes: stages/, reference/, templates/, debugging/,
     missed_requirement/, prompts/, and ALL root-level .md files
   - CLAUDE.md (root project instructions)
   - DO NOT limit to just stages/ folder
   - Use Glob pattern="**/*.md" path="feature-updates/guides_v2" to discover all files
   - Historical issue: 60% of updates missed non-stages/ files
```

---

## Prerequisites Checklist

**Verify BEFORE starting S10.5:**

□ S10 user testing passed (Gate 7.2)
□ Zero bugs found by user
□ epic_lessons_learned.md exists and is complete
□ All feature lessons_learned.md files exist and are complete
□ Ready to analyze lessons and create proposals

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S10.5
- Return to previous step to complete prerequisites

---

## Step-by-Step Workflow

### Step 1: Read All Lessons Learned

**Purpose:** Gather all lessons from epic to identify guide improvement opportunities

**Actions:**

1.1. **Read epic-level lessons:**
```bash
# Read epic lessons
cat {epic_folder}/epic_lessons_learned.md
```

Note:
- How many lessons documented?
- Which lessons are about process/guides vs domain-specific?
- Any patterns emerging?

1.2. **Read all feature-level lessons:**
```bash
# Read each feature's lessons
cat {epic_folder}/feature_01_{name}/lessons_learned.md
cat {epic_folder}/feature_02_{name}/lessons_learned.md
...
```

Note:
- Common issues across features?
- Feature-specific vs generalizable lessons?
- Any repeated mistakes?

1.3. **Tally total lessons:**
- Epic lessons: {N}
- Feature lessons: {N} across {N} features
- Total: {N} lessons to analyze

**Checkpoint:**
- [ ] All epic_lessons_learned.md read
- [ ] All feature lessons_learned.md read
- [ ] Total lesson count documented

---

### Step 2: Identify Guide Gaps

**Purpose:** For each lesson, determine which guide(s) could have prevented the issue

**Actions:**

2.1. **For each lesson, ask:**
- What went wrong? (or what went right?)
- Why did it occur? (root cause)
- Which guide(s) could have prevented this?
- What specific guidance was missing/unclear/wrong?
- Is this a one-time issue or systemic pattern?

2.2. **Use common lesson → guide mappings:**

| Lesson Pattern | Likely Affected Guide(s) |
|----------------|--------------------------|
| Missed requirement in spec | stages/s2/s2_p2_specification.md |
| Wrong interface assumed | stages/s5/s5_p1_planning_round1.md (Iteration 2) |
| Algorithm traceability incomplete | stages/s5/s5_p1_planning_round1.md (Iteration 4) |
| Integration gap not identified | stages/s5/s5_p1_planning_round1.md (Iteration 7) |
| Test coverage insufficient | stages/s5/s5_p2_planning_round2.md (Iterations 8-10) |
| Gate not enforced | reference/mandatory_gates.md |
| QC round missed issue | stages/s7/s7_p2_qc_rounds.md |
| Smoke test didn't catch bug | stages/s7/s7_p1_smoke_testing.md |
| Epic integration issue | stages/s9/s9_p2_epic_qc_rounds.md |
| Spec misinterpretation | stages/s5/s5_p3_i3_gates_part2.md (Iteration 21) |
| Checklist question unclear | templates/feature_checklist_template.md |
| Implementation plan vague | templates/implementation_plan_template.md |
| Prompt not followed | prompts/{stage}_prompts.md |
| Workflow diagram unclear | reference/workflow_diagrams.md |
| Reference card missing info | reference/stage_{N}_reference_card.md |

2.3. **Determine priority for each:**

**P0 (Critical) - Must fix:**
- Prevents catastrophic bugs (week+ of rework)
- Mandatory gate was missing/unclear and caused major issue
- Spec misinterpretation led to implementing wrong solution
- Safety/security vulnerability in process

**P1 (High) - Strongly recommended:**
- Significantly improves quality
- Reduces common rework patterns (days of rework)
- Prevents moderate bugs
- Clarifies ambiguous requirements that caused confusion

**P2 (Medium) - Consider:**
- Moderate quality improvement
- Clarifies minor ambiguity
- Improves workflow efficiency
- Better examples/templates

**P3 (Low) - Nice-to-have:**
- Minor improvement
- Cosmetic/formatting
- Adds optional convenience
- Reduces minor friction

2.4. **Filter out non-actionable lessons:**

**Skip if lesson is:**
- Domain-specific (only applies to this epic's subject matter)
- Already covered by guides (no gap to fill)
- User-specific decision (not a guide issue)
- One-time environmental issue (not preventable by guides)

**Checkpoint:**
- [ ] Each lesson analyzed for guide impact
- [ ] Guide gaps identified and documented
- [ ] Priorities assigned (P0/P1/P2/P3)
- [ ] Non-actionable lessons filtered out
- [ ] Ready to create proposals

---

### Step 3: Create GUIDE_UPDATE_PROPOSAL.md

**Purpose:** Document all proposed guide changes in structured format for user review

**Actions:**

3.1. **Create file using template:**
```bash
# Copy template
cp feature-updates/guides_v2/templates/guide_update_proposal_template.md \
   {epic_folder}/GUIDE_UPDATE_PROPOSAL.md
```

3.2. **Fill in summary section:**
- Epic name and KAI number
- Total lessons analyzed (epic + feature counts)
- Total proposals (breakdown by P0/P1/P2/P3)
- Recommended action (prioritize P0 and P1)

3.3. **Create proposals grouped by priority:**

**For each guide gap identified:**

a. **Write proposal header:**
   - Proposal ID (P0-1, P1-2, etc.)
   - Short descriptive title

b. **Quote lesson learned:**
   - Direct quote from lessons_learned.md
   - Source file and lesson number

c. **Explain root cause:**
   - Why this issue occurred
   - What was missing/unclear in guides

d. **Identify affected guide(s):**
   - Path to guide file
   - Section name
   - Line numbers (if known)

e. **Show before/after:**
   - Current state: exact text from guide
   - Proposed change: new text with improvements
   - Make differences clear (use formatting if helpful)

f. **Provide rationale:**
   - How this specific change prevents future issues
   - Why this guidance helps

g. **Assess impact:**
   - Who benefits (which agents/stages)
   - When it helps (specific situations)
   - Severity if unfixed (specific bad outcome)

h. **Add user decision checkboxes:**
   - [ ] Approve
   - [ ] Modify
   - [ ] Reject
   - [ ] Discuss

3.4. **Group proposals by priority:**
- Start with P0 (Critical)
- Then P1 (High)
- Then P2 (Medium)
- Then P3 (Low)

Within each priority, order by impact (highest impact first)

**Checkpoint:**
- [ ] GUIDE_UPDATE_PROPOSAL.md created
- [ ] All proposals documented with before/after
- [ ] Proposals grouped and ordered by priority
- [ ] User decision sections included
- [ ] File is clear and ready for user review

---

### Step 4: Present Proposals to User

**Purpose:** Get user approval for each proposal individually

**Actions:**

4.1. **Use the presentation prompt:**
- Read prompts/guide_update_prompts.md
- Use "Presenting Proposals to User" prompt
- Present summary first, then individual proposals

4.2. **Present P0 proposals first:**
- These are critical fixes
- User should prioritize reviewing these
- Explain why each is P0 priority

4.3. **For each proposal, show:**
- Lesson learned (what went wrong)
- Problem (why it occurred)
- Affected guide and section
- Before/after comparison
- Rationale (how this helps)
- Ask: "Your decision for Proposal P{X}-{N}: Approve / Modify / Reject / Discuss?"

4.4. **Collect user decisions:**

**If user says "Approve":**
- Mark proposal as approved
- Continue to next proposal

**If user says "Modify":**
- Ask user to provide alternative text
- Document user's modification
- Mark proposal as modified
- Continue to next proposal

**If user says "Reject":**
- Mark proposal as rejected
- Ask for brief rationale (optional)
- Continue to next proposal

**If user says "Discuss":**
- Answer user's questions
- Provide additional context/examples
- Revise proposal if needed
- Re-present for decision
- Do NOT proceed until decision made

4.5. **Continue through all priorities:**
- After P0, present P1 proposals
- After P1, present P2 proposals
- After P2, present P3 proposals

4.6. **Summarize decisions:**
```
Total proposals: {N}
Approved: {N}
Modified: {N}
Rejected: {N}
```

**Checkpoint:**
- [ ] All proposals presented to user
- [ ] User made decision for each proposal
- [ ] Modified proposals have user's alternative text
- [ ] Rejected proposals have rationale (if provided)
- [ ] Decision summary documented

---

### Step 5: Apply Approved Changes

**Purpose:** Update guides with approved changes and user modifications

**🚨 CRITICAL REMINDER BEFORE APPLYING CHANGES:**
```
When applying changes to "guides", remember:
- "Guides" = EVERY FILE in feature-updates/guides_v2/
- NOT just stages/ folder
- Includes: stages/, reference/, templates/, debugging/,
  missed_requirement/, prompts/, README.md, etc.
- If a proposal affects reference/, templates/, or other non-stages/
  folders, you MUST update those files
- Use Glob pattern="**/*.md" path="feature-updates/guides_v2"
  to see all files if unsure where to apply changes
```

**Actions:**

5.1. **For each approved proposal:**
- Read the affected guide file
- Locate the section to update
- Apply the proposed change using Edit tool
- Verify change applied correctly

5.2. **For each modified proposal:**
- Read the affected guide file
- Locate the section to update
- Apply user's modification (not original proposal)
- Verify change applied correctly

5.3. **Skip rejected proposals:**
- Do NOT apply rejected changes
- Document rejection in tracking (next step)

5.4. **Verify all changes:**
- Re-read updated guides
- Ensure changes are correct
- Check for any formatting issues

**Checkpoint:**
- [ ] All approved proposals applied to guides
- [ ] All modified proposals applied with user's text
- [ ] Rejected proposals skipped
- [ ] All changes verified correct

---

### Step 6: Create Separate Commit

**Purpose:** Commit guide updates separately from epic code for clear history

**Actions:**

6.1. **Stage guide changes:**
```bash
git add feature-updates/guides_v2/
git add CLAUDE.md  # if modified
```

6.2. **Create commit:**
```bash
git commit -m "docs(guides): Apply lessons from KAI-{N}-{epic_name}

Proposals applied:
- P0: {N} critical fixes
- P1: {N} high priority improvements
- P2: {N} medium priority improvements
- P3: {N} low priority improvements

Total: {N} approved + {N} modified

Guides updated:
- {guide1.md}: {brief description}
- {guide2.md}: {brief description}
...

See {epic_folder}/GUIDE_UPDATE_PROPOSAL.md for details."
```

6.3. **Verify commit:**
```bash
git log -1 --stat
```

Check:
- Commit message is clear
- Only guide files committed (not epic code)
- All updated guides included

**Checkpoint:**
- [ ] Guide changes staged
- [ ] Separate commit created
- [ ] Commit message documents what was applied
- [ ] Commit verified correct

---

### Step 7: Update Tracking

**Purpose:** Document applied lessons in tracking file for history and pattern analysis

**Actions:**

7.1. **Open tracking file:**
```bash
# Edit tracking file
# Add entries to Applied Lessons Log, Rejected Lessons, and Metrics
```

7.2. **Add to Applied Lessons Log:**
- For each approved/modified proposal:
  - Epic: KAI-{N}-{epic_name}
  - Priority: P0/P1/P2/P3
  - Lesson Summary: {brief description}
  - Guide(s) Updated: {paths}
  - Date Applied: {YYYY-MM-DD}
  - Commit: {commit_hash}

7.3. **Add to Rejected Lessons:**
- For each rejected proposal:
  - Epic: KAI-{N}-{epic_name}
  - Priority: P0/P1/P2/P3
  - Lesson Summary: {brief description}
  - Proposed Guide(s): {paths}
  - Date Rejected: {YYYY-MM-DD}
  - User Rationale: {user's reason}

7.4. **Update Metrics:**
- Increment total epics completed
- Add proposal counts to totals
- Update approval rates by priority
- Update most frequently updated guides list

7.5. **Check for patterns:**
- If same lesson appears 2+ times, consider creating Pattern Analysis entry
- Document common patterns in Pattern Analysis section

7.6. **Commit tracking update:**
```bash
git add feature-updates/guides_v2/reference/guide_update_tracking.md
git commit -m "docs(tracking): Update guide tracking for KAI-{N}-{epic_name}"
```

**Checkpoint:**
- [ ] Applied Lessons Log updated
- [ ] Rejected Lessons documented
- [ ] Metrics updated
- [ ] Patterns checked
- [ ] Tracking commit created

---

### Step 8: Update guide-updates.txt (If Applicable)

**Purpose:** If any approved changes relate to items in guide-updates.txt, update their status

**Actions:**

8.1. **Check if any proposals address guide-updates.txt items:**
- Read feature-updates/guide-updates.txt
- Check if any approved proposals relate to ❌ NOT ADDRESSED or ⚠️ PARTIALLY ADDRESSED items

8.2. **If relevant, update guide-updates.txt:**
- Update item status (e.g., ❌ → ⚠️ or ⚠️ → ✅)
- Add documentation of what was implemented
- Add reference to epic that drove the change

8.3. **Commit if updated:**
```bash
git add feature-updates/guide-updates.txt
git commit -m "docs(guide-updates): Update status for items addressed in KAI-{N}-{epic_name}"
```

**Checkpoint:**
- [ ] guide-updates.txt checked
- [ ] Relevant items updated (if any)
- [ ] Commit created (if updated)

---

### Step 9: Mark S10.5 Complete

**Purpose:** Update EPIC_README.md and announce completion

**Actions:**

9.1. **Update EPIC_README.md Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** EPIC_FINALIZATION
**Current Step:** Ready for final commit and PR
**Current Guide:** stages/s10/s10_epic_cleanup.md
**Guide Last Read:** NOT YET (will read when starting Step 7)

**Progress:** S10.5 complete (guide updates applied)
**Next Action:** Proceed to S10 Step 7 (Final Commit & Pull Request)
**Blockers:** None

**S10.5 Summary:**
- Proposals: {N} ({approved} approved, {modified} modified, {rejected} rejected)
- Guides updated: {N} files
- Commits: {N} (guide updates + tracking)
```

9.2. **Announce completion:**

Use prompt from prompts/guide_update_prompts.md "After Applying Changes" section

**Checkpoint:**
- [ ] EPIC_README.md updated
- [ ] Agent Status shows S10.5 complete
- [ ] Next action is S10 Step 7
- [ ] Completion announced to user

---

## Exit Criteria

**S10.5 is complete when:**
- [ ] All lessons_learned.md files analyzed
- [ ] GUIDE_UPDATE_PROPOSAL.md created with all proposals
- [ ] User reviewed all proposals individually
- [ ] All approved/modified proposals applied to guides
- [ ] Separate commit created for guide updates
- [ ] reference/guide_update_tracking.md updated
- [ ] guide-updates.txt updated (if applicable)
- [ ] EPIC_README.md shows S10.5 complete
- [ ] Ready to proceed to S10 Step 7

**Next Stage:** S10 Step 7 (Final Commit & Pull Request)

---

## Common Pitfalls

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "This lesson seems minor, I'll skip it"
   ✅ STOP - Analyze ALL lessons, let priority system categorize

❌ "User will probably approve all P0, I'll batch apply"
   ✅ STOP - Get individual approval for EACH proposal

❌ "This guide change is obvious, I'll just apply it"
   ✅ STOP - User must approve ALL changes

❌ "I'll combine guide updates with epic commit"
   ✅ STOP - Separate commits required for clarity

❌ "No guide gaps found, lessons are all domain-specific"
   ✅ VERIFY - Re-read lessons with fresh eyes, look for patterns

❌ "User rejected P0, I'll apply it anyway since it's critical"
   ✅ STOP - User decision is final, document rejection

❌ "I'll update tracking later"
   ✅ STOP - Update tracking immediately while context fresh
```

---

## Quick Reference: Proposal Quality Checklist

**Each proposal should have:**
- [ ] Clear lesson quote from lessons_learned.md
- [ ] Specific root cause explanation
- [ ] Exact guide path and section
- [ ] Before/after comparison (exact text)
- [ ] Rationale linking lesson → guide fix
- [ ] Impact assessment (who/when/severity)
- [ ] Priority correctly assigned (P0/P1/P2/P3)
- [ ] User decision checkboxes

**Red flags (fix before presenting):**
- Vague before/after ("improve clarity" without specific text)
- No clear connection between lesson and guide change
- Priority doesn't match severity description
- Missing rationale or impact assessment
- Proposing changes to code instead of guides

---

## Example Proposal (For Reference)

### Proposal P0-1: Add Spec Validation Historical Context to Mandatory Gates

**Lesson Learned:**
> "Iteration 21 (Spec Validation Against Validated Documents) caught that spec.md misinterpreted epic notes about week_N+1 folder logic. Epic said 'create week folders' but spec said 'no code changes needed for folders.' This gate prevented a week+ of rework implementing the wrong solution."

**Source File:** `epic_lessons_learned.md` - Lesson #3

**Root Cause:**
Agent rushed through S2 spec creation and made assumptions about folder handling instead of carefully reading epic notes. Iteration 21's three-way comparison (epic notes, epic ticket, spec summary) caught the discrepancy before implementation.

**Affected Guide(s):**
- `reference/mandatory_gates.md` - Section: "Gate 3: Iteration 21 - Spec Validation Against Validated Documents" (Lines 281-327)

**Current State (BEFORE):**
```markdown
### Gate 3: Iteration 21 - Spec Validation Against Validated Documents (CRITICAL)

**What it checks:**
- Spec.md matches ALL three user-validated sources:
  1. Epic notes (user's original request)
  2. Epic ticket (user-validated outcomes from S1)
  3. Spec summary (user-validated feature outcomes from S2)
```

**Proposed Change (AFTER):**
```markdown
### Gate 3: Iteration 21 - Spec Validation Against Validated Documents (CRITICAL)

**Historical Context:**
- Feature 02 catastrophic bug: spec.md misinterpreted epic notes
- Spec stated "no code changes needed" when epic actually required week_N+1 folder logic
- Iteration 21 specifically designed to prevent this type of bug
- Three-way comparison catches spec misinterpretations before implementation

**What it checks:**
- Spec.md matches ALL three user-validated sources:
  1. Epic notes (user's original request)
  2. Epic ticket (user-validated outcomes from S1)
  3. Spec summary (user-validated feature outcomes from S2)
```

**Rationale:**
Adding historical context shows future agents WHY this gate exists and what happens if it's skipped. Real example makes the importance concrete instead of abstract.

**Impact Assessment:**
- **Who benefits:** All agents doing S5 Round 3 (Iteration 21)
- **When it helps:** When validating spec.md against user-approved documents
- **Severity if unfixed:** Critical - agents may skip or rush through Iteration 21 without understanding its importance, leading to week+ of rework from spec misinterpretation

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```
{User writes response here}
```

---

**Last Updated:** 2026-01-11
