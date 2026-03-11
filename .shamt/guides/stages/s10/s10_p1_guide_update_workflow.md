# S10.P1: Guide Update from Lessons Learned

**File:** `s10_p1_guide_update_workflow.md`

---


## Table of Contents

1. [S10.P1: Guide Update from Lessons Learned](#s10p1-guide-update-from-lessons-learned)
2. [Overview](#overview)
3. [Critical Rules](#critical-rules)
4. [Prerequisites Checklist](#prerequisites-checklist)
5. [Step-by-Step Workflow](#step-by-step-workflow)
6. [Agent Status](#agent-status)
7. [Exit Criteria](#exit-criteria)
8. [Common Pitfalls](#common-pitfalls)
9. [Quick Reference: Proposal Quality Checklist](#quick-reference-proposal-quality-checklist)
10. [Example Proposal (For Reference)](#example-proposal-for-reference)

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
- S9 user testing passed (S9 Step 6 - zero bugs found)
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
S10.P1 is complete when all proposals have been reviewed by user, approved changes applied to guides, separate commit created, and tracking updated

---

## Critical Rules

```text
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
   - Commit message: "docs(guides): Apply lessons from SHAMT-{N}-{epic_name}"
   - Do NOT mix guide updates with epic commits

6. ⚠️ Check gitignore BEFORE committing guide updates
   - Run `git check-ignore .shamt/guides/` before staging
   - If guides are gitignored → apply changes locally, skip commit, inform user
   - NEVER use `git add -f` to force-commit gitignored files
   - If guides are NOT gitignored → proceed with normal `git add` and `git commit`

7. ⚠️ Update tracking after applying changes
   - Add entries to reference/guide_update_tracking.md
   - Document approved, modified, and rejected proposals
   - Update metrics section

8. ⚠️ Scope: ENTIRE .shamt/guides/ directory + CLAUDE.md
   - 🚨 CRITICAL: "Guides" = EVERY FILE in .shamt/guides/
   - This includes: stages/, reference/, templates/, debugging/,
     missed_requirement/, prompts/, and ALL root-level .md files
   - CLAUDE.md (root project instructions)
   - DO NOT limit to just stages/ folder
   - Use Glob pattern="**/*.md" path=".shamt/guides" to discover all files
   - Historical issue: 60% of updates missed non-stages/ files
```

---

## Prerequisites Checklist

**Verify BEFORE starting S10.P1:**

- [ ] S9 user testing passed (S9 Step 6) — user reported ZERO bugs
- [ ] S9 complete (EPIC_README.md shows S9 ✅ COMPLETE)
- [ ] epic_lessons_learned.md exists and is complete
- [ ] All feature lessons_learned.md files exist and are complete
- [ ] Ready to analyze lessons and create proposals

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S10.P1
- Return to previous step to complete prerequisites

---

## Step-by-Step Workflow

### Step 1: Read All Lessons Learned

**Purpose:** Gather all lessons from epic to identify guide improvement opportunities

**Actions:**

1.1. **Read epic-level lessons:**
```bash
## Read epic lessons
cat {epic_folder}/epic_lessons_learned.md
```

Note:
- How many lessons documented?
- Which lessons are about process/guides vs domain-specific?
- Any patterns emerging?

1.2. **Read all feature-level lessons:**
```bash
## Read each feature's lessons
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
| Missed requirement in spec | stages/s2/s2_p1_spec_creation_refinement.md |
| Wrong interface assumed | stages/s5/s5_v2_validation_loop.md (Dimension 2) |
| Algorithm traceability incomplete | stages/s5/s5_v2_validation_loop.md (Dimension 3) |
| Integration gap not identified | stages/s5/s5_v2_validation_loop.md (Dimension 7) |
| Test coverage insufficient | stages/s5/s5_v2_validation_loop.md (Dimension 8) |
| Gate not enforced | reference/mandatory_gates.md |
| QC round missed issue | stages/s7/s7_p2_qc_rounds.md |
| Smoke test didn't catch bug | stages/s7/s7_p1_smoke_testing.md |
| Epic integration issue | stages/s9/s9_p2_epic_qc_rounds.md |
| Spec misinterpretation | stages/s5/s5_v2_validation_loop.md (D11: Gate 23a - Spec Alignment) |
| Checklist question unclear | templates/feature_checklist_template.md |
| Implementation plan vague | templates/implementation_plan_template.md |
| Prompt not followed | prompts/{stage}_prompts.md |
| Workflow diagram unclear | EPIC_WORKFLOW_USAGE.md → "Workflow Stages" |
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
## Copy template
cp .shamt/guides/templates/guide_update_proposal_template.md \
   {epic_folder}/GUIDE_UPDATE_PROPOSAL.md
```

3.2. **Fill in summary section:**
- Epic name and SHAMT number
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
- Ask: "Your decision for Proposal P{X}-{N}:
  - **Approve** — apply exactly as written
  - **Modify** — apply with changes (you provide alternative text)
  - **Reject** — skip this proposal
  - **Discuss** — ask questions or request clarification first"

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
```text
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
```bash
When applying changes to "guides", remember:
- "Guides" = EVERY FILE in .shamt/guides/
- NOT just stages/ folder
- Includes: stages/, reference/, templates/, debugging/,
  missed_requirement/, prompts/, README.md, etc.
- If a proposal affects reference/, templates/, or other non-stages/
  folders, you MUST update those files
- Use Glob pattern="**/*.md" path=".shamt/guides"
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

6.0. **Check if guides are gitignored (MANDATORY before staging):**
```bash
git check-ignore .shamt/guides/ .github/copilot-instructions.md CLAUDE.md 2>/dev/null
```

- If ANY guide file is reported as ignored → **STOP. Do NOT commit guide changes.**
  - Changes are applied locally (files are updated on disk)
  - Inform user: "Guide updates applied locally but not committed — guide files are gitignored in this project."
  - Skip Steps 6.1–6.3 entirely and proceed to Step 7
- If NO output (files are not ignored) → proceed with Steps 6.1–6.3

🚨 **NEVER use `git add -f` or `git add --force` to bypass gitignore for guide files.** If guides are gitignored, the project has intentionally excluded them from version control. Respect that decision.

6.1. **Stage guide changes:**
```bash
git add .shamt/guides/
git add CLAUDE.md  # if modified
```

6.2. **Create commit:**
```bash
git commit -m "docs(guides): Apply lessons from SHAMT-{N}-{epic_name}

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
## Edit tracking file
## Add entries to Applied Lessons Log, Rejected Lessons, and Metrics
```

7.2. **Add to Applied Lessons Log:**
- For each approved/modified proposal:
  - Epic: SHAMT-{N}-{epic_name}
  - Priority: P0/P1/P2/P3
  - Lesson Summary: {brief description}
  - Guide(s) Updated: {paths}
  - Date Applied: {YYYY-MM-DD}
  - Commit: {commit_hash}

7.3. **Add to Rejected Lessons:**
- For each rejected proposal:
  - Epic: SHAMT-{N}-{epic_name}
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
git add .shamt/guides/reference/guide_update_tracking.md
git commit -m "docs(tracking): Update guide tracking for SHAMT-{N}-{epic_name}"
```

**Checkpoint:**
- [ ] Applied Lessons Log updated
- [ ] Rejected Lessons documented
- [ ] Metrics updated
- [ ] Patterns checked
- [ ] Tracking commit created

---

### Step 8: Consider Exporting Improvements to Master

**Purpose:** If guide improvements are generic enough to benefit other projects, record them for export to the master Shamt repo.

**When to record for export:**
- The improvement addresses a genuine gap or error in the guide system
- The change would benefit any project using Shamt (not just this project's tech stack)
- The improvement is to core workflow steps, gates, or clarifications — not project-specific examples

**When NOT to export:**
- The change is domain-specific (only makes sense for this project's language/framework)
- The change is minor wording tweaks with no functional impact
- The change contradicts a deliberate Shamt design decision

**Always do first (regardless of export decision):**

8.0. **Review your rules file against the master template:**

Compare your project's rules file (wherever it lives: `CLAUDE.md`, `.github/copilot-instructions.md`, etc.) against `.shamt/scripts/initialization/RULES_FILE.template.md`. For each section in your rules file not present in the template, ask: *would this apply to any Shamt project regardless of tech stack?*

- **If generic additions exist** → add them to the template (replace your epic tag with `{{EPIC_TAG}}`), then add a `CHANGES.md` entry for each:
  ```markdown
  ## YYYY-MM-DD — Rules file template: [section name]
  - Modified: `scripts/initialization/RULES_FILE.template.md`
  - Rules file section: [section name or brief description]
  - Reason: [why this is generic]
  ```
- **If no generic additions** → note "Rules file compared — no template updates needed" and continue.

**Do this step regardless of whether you plan to export.** The rules file template is not touched by the export script (it lives outside `.shamt/guides/` and `.shamt/scripts/`), so it must be updated manually here before any export opportunity is presented to the user.

---

**If improvements are worth exporting:**

8.1. Verify that `CHANGES.md` entries exist for each shared file you modified (see `sync/separation_rule.md` for the required format). Add any missing entries:

```markdown
## YYYY-MM-DD — [brief description]
- Modified: `.shamt/guides/path/to/guide.md`
- Reason: [one line]
```

8.2. Inform the user: "Guide improvements were made that could benefit other Shamt projects. When ready, run `bash .shamt/scripts/export/export.sh` and open a PR to the master repo."

**If improvements are project-specific only:** Note "No export warranted — changes are project-specific" in your completion announcement and proceed.

**Reference:** See `sync/export_workflow.md` for the full export process.

**Checkpoint:**
- [ ] Rules file compared against `RULES_FILE.template.md`; template updated with generic additions (or "no updates needed" noted)
- [ ] Assessed whether guide improvements are generic/universal
- [ ] `CHANGES.md` updated for all shared file modifications (if applicable)
- [ ] User informed about export opportunity (if applicable) or reason noted (if not)

---

### Step 9: Mark S10.P1 Complete

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

**Progress:** S10.P1 complete (guide updates applied)
**Next Action:** Proceed to S10 Step 7 (Final Commit & Pull Request)
**Blockers:** None

**S10.P1 Summary:**
- Proposals: {N} ({approved} approved, {modified} modified, {rejected} rejected)
- Guides updated: {N} files
- Commits: {N} (guide updates + tracking)
```

9.2. **Announce completion:**

Use prompt from prompts/guide_update_prompts.md "After Applying Changes" section

**Checkpoint:**
- [ ] EPIC_README.md updated
- [ ] Agent Status shows S10.P1 complete
- [ ] Next action is S10 Step 7
- [ ] Completion announced to user

---

## Exit Criteria

**S10.P1 is complete when:**
- [ ] All lessons_learned.md files analyzed
- [ ] GUIDE_UPDATE_PROPOSAL.md created with all proposals
- [ ] User reviewed all proposals individually
- [ ] All approved/modified proposals applied to guides
- [ ] Separate commit created for guide updates
- [ ] reference/guide_update_tracking.md updated
- [ ] Export assessed: CHANGES.md updated if improvements are generic (or project-specific noted)
- [ ] EPIC_README.md shows S10.P1 complete
- [ ] Ready to proceed to S10 Step 7

---

## Common Pitfalls

```text
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

❌ "git add isn't working for guides, I'll use git add -f"
   ✅ STOP - Guides are likely gitignored. Apply changes locally, skip commit, inform user. NEVER force-add.

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
> "S5 Validation Loop Dimension 11 (Spec Alignment & Cross-Validation) caught that implementation_plan.md misinterpreted spec.md about week_N+1 folder logic. Spec said 'create week folders' but implementation plan said 'no code changes needed for folders.' This validation dimension prevented a week+ of rework implementing the wrong solution."

**Source File:** `epic_lessons_learned.md` - Lesson #3

**Root Cause:**
Agent rushed through S5 Phase 1 (Draft Creation) and made assumptions about folder handling instead of carefully reading spec.md. Dimension 11's cross-validation (spec.md, test_strategy.md, epic context) caught the discrepancy during Validation Loop.

**Affected Guide(s):**
- `stages/s5/s5_v2_validation_loop.md` - Section: "Dimension 11: Spec Alignment & Cross-Validation" (Lines 725-750)

**Current State (BEFORE):**
```markdown
### Dimension 11: Spec Alignment & Cross-Validation (CRITICAL)

**What to Check:**
- [ ] Implementation plan matches spec.md requirements
- [ ] All spec.md sections referenced in implementation tasks
- [ ] No spec.md requirements missing from plan
- [ ] Test strategy aligns with spec.md test requirements
```

**Proposed Change (AFTER):**
```markdown
### Dimension 11: Spec Alignment & Cross-Validation (CRITICAL)

**Historical Context:**
- Feature 02 catastrophic bug: implementation_plan.md misinterpreted spec.md
- Plan stated "no code changes needed" when spec actually required week_N+1 folder logic
- Dimension 11 specifically designed to prevent this type of bug
- Cross-validation catches spec misinterpretations before implementation

**What to Check:**
- [ ] Implementation plan matches spec.md requirements
- [ ] All spec.md sections referenced in implementation tasks
- [ ] No spec.md requirements missing from plan
- [ ] Test strategy aligns with spec.md test requirements
```

**Rationale:**
Adding historical context shows future agents WHY this dimension exists and what happens if it's skipped. Real example makes the importance concrete instead of abstract.

**Impact Assessment:**
- **Who benefits:** All agents doing S5 v2 Validation Loop (Dimension 11)
- **When it helps:** When validating implementation_plan.md against spec.md
- **Severity if unfixed:** Critical - agents may skip or rush through Dimension 11 without understanding its importance, leading to week+ of rework from spec misinterpretation

**User Decision:** [ ] Approve  [ ] Modify  [ ] Reject  [ ] Discuss

**User Feedback/Modifications:**
```json
{User writes response here}
```

---

## Next Phase

**This is a sub-workflow of S10 (Epic Cleanup).**

**After completing S10.P1 (Guide Updates):** Return to `stages/s10/s10_epic_cleanup.md` to continue with:
- S10.P2: Create PR
- S10.P3: Update .shamt/epics/EPIC_TRACKER.md
- S10.P4: Move epic to done/

**📖 RETURN TO:** `stages/s10/s10_epic_cleanup.md`

---

*End of s10_p1_guide_update_workflow.md*

**Last Updated:** 2026-01-11
