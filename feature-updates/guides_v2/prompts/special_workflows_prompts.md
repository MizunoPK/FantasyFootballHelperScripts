# Special Workflows Prompts

**Purpose:** Prompts for bug fixes, missed requirements, debugging protocol, and resuming work

---

## Creating a Bug Fix

**User says:** "I found a bug" or "There's an issue with..." or Agent discovers issue during QC

**Can occur during:** ANY stage

**Agent MUST respond:**

```
I've identified an issue that requires a bug fix. Let me present it to you for approval...

**Issue Summary:**
- **What's wrong:** {Brief description of symptom}
- **Discovered during:** Stage {X} - {feature_name or "epic-level"}
- **Impact:** {What doesn't work because of this - e.g., "Epic smoke testing fails", "Feature produces incorrect results"}
- **Priority recommendation:** {high/medium/low}
  - high: Breaks epic functionality → Interrupt current work immediately
  - medium: Affects quality but not functionality → Finish current step first
  - low: Minor issues → Fix after current step completes
  - ALL bugs found during epic development MUST be fixed before Stage 7 (no deferred tech debt)

**Root Cause (if known):**
{Analysis of why the bug exists, or "Root cause not yet determined - will investigate in bug fix Stage 2"}

**Proposed Solution:**
{How to fix it, or "Solution TBD - will design in bug fix Stage 2"}

**Should I create a bug fix for this issue?**
- If yes: I'll create bugfix_{priority}_{name}/ folder and notes.txt and fix it before Stage 7
- If no: Please confirm this is NOT a bug and the behavior is correct as-is
- NOTE: All bugs found during epic development MUST be fixed - no deferring to "later" or leaving tech debt

Waiting for your approval...
```

**After user approves:**

```
I'm reading `stages/stage_5/bugfix_workflow.md` to ensure I follow the bug fix workflow...

**The guide requires:**
- PHASE 1: Bug Fix Creation
  - Create bugfix_{priority}_{name}/ folder in epic directory
  - Create notes.txt with issue description
  - User verifies/updates notes.txt
  - Update epic EPIC_README.md to track bug fix
  - Save current work state in README
- PHASE 2: Bug Fix Implementation
  - Stage 2: Deep Dive (adapted for bug fix)
  - Stage 5a: TODO Creation (24 iterations)
  - Stage 5b: Implementation
  - Stage 5c: Post-Implementation
  - SKIP: Stages 1, 3, 4, 5d, 5e, 6, 7 (epic-level stages)
- PHASE 3: Resume Previous Work
  - Mark bug fix complete
  - Verify bug fix doesn't affect paused work
  - Resume from saved state
- **Priority Handling:**
  - high: Interrupt immediately
  - medium: Finish current sub-stage first
  - low: Finish current feature first

**I'll now create the bug fix folder and notes.txt...**

Creating bugfix_{priority}_{name}/ folder...
```

---

## Creating Missed Requirement

**When to use:** Discovered missing scope/requirement at ANY point after first Stage 5 starts, where solution is KNOWN (can happen during implementation, QA, debugging, epic testing, or user testing)

**Prerequisites:**
- At least one feature has entered Stage 5 (not before any feature enters Stage 5)
- Missing requirement discovered (you know what needs to be built)
- Root cause is clear (just forgot to include it in spec)
- Solution approach is obvious
- There are unstarted features available (if considering Option 2)

**Agent MUST respond:**

```
I'm reading `missed_requirement/missed_requirement_protocol.md` to ensure I follow the complete missed requirement protocol...

**The guide requires:**
- Phase 1: Discovery & User Decision
  - Step 1: Discover missing scope
  - Step 2: Present TWO options to user (new feature vs update unstarted)
  - Step 3: User decides approach + priority + sequence (if new feature)
- Phase 2: Pause Current Work
  - Step 1-2: Save current feature state, update EPIC_README
- Phase 3: Return to Planning Stages (2/3/4)
  - Stage 2: Flesh out new/updated feature spec (full deep dive)
  - Stage 3: Re-align ALL features (cross-feature sanity check)
  - Stage 4: Update epic_smoke_test_plan.md
- Phase 4: Resume Previous Work
  - Mark planning complete
  - Verify no spec changes affect paused feature
  - Resume from saved state
  - New/updated feature implemented LATER when its turn comes
- Two options: Create new feature_{XX}_{name}/ OR update unstarted feature
- ALWAYS return to Stage 2/3/4 for planning
- Full Stage 5 (5a → 5b → 5c → 5d → 5e) when feature gets implemented
- Priority determines sequence: high = before current, medium = after current, low = at end
- SPECIAL CASE: If discovered during Stage 6/7 → Complete all features → Restart epic testing from Stage 6a
- Can be discovered during: Implementation (5a/5b/5c), Debugging, Epic Testing (6a/6b/6c), User Testing (7)

**Prerequisites I'm verifying:**
✅ At least one feature has entered Stage 5 (can only use after first Stage 5 starts)
✅ Missing requirement clearly identified
✅ Solution approach is known (not a debugging situation)
✅ Can articulate what needs to be built
✅ Not an unknown bug (would use debugging/debugging_protocol.md instead)
✅ Have unstarted features to potentially update

**I'll now present options to the user...**

**Will update README Agent Status after user decision:**
- Current Phase: MISSED_REQUIREMENT_HANDLING
- Current Guide: missed_requirement/missed_requirement_protocol.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Get user approval first", "Return to Stage 2/3/4", "Update epic docs", "Implement in sequence"
- Next Action: Present options (new feature vs update unstarted feature)

Presenting to user...
```

---

## Starting Debugging Protocol

**When to use:** Issues discovered during QC/Smoke Testing with unknown root cause

**Prerequisites:**
- Issues found during Smoke Testing or QC Rounds
- Root cause is unknown - requires investigation
- May have multiple related issues

**Agent MUST respond:**

```
I'm reading `debugging/debugging_protocol.md` to ensure I follow the complete debugging protocol...

**The guide requires:**
- Integrated with testing stages - Loop-back mechanism
  - QC/Smoke finds issues → Add to debugging/ISSUES_CHECKLIST.md
  - Enter Debugging Protocol
  - After ALL issues resolved → Loop back to START of testing stage
  - Repeat testing → If new issues, repeat debugging
- Phase 1: Issue Discovery & Checklist Update
  - Create feature_XX/debugging/ or epic_name/debugging/ folder
  - Create/update ISSUES_CHECKLIST.md (track ALL issues)
  - Update README Agent Status
- Phase 2: Issue Investigation (PER ISSUE, ITERATIVE)
  - Round 1: Code Tracing (identify 2-3 suspicious areas)
  - Round 2: Hypothesis Formation (max 3 hypotheses)
  - Round 3: Diagnostic Testing (confirm root cause)
  - Max 5 rounds per issue before user escalation
  - Max 2 hours per round
- Phase 3: Solution Design & Implementation (PER ISSUE)
  - Design and implement fix
  - Add/update tests
  - Document in debugging/code_changes.md
- Phase 4: User Verification (PER ISSUE) - MANDATORY
  - User MUST confirm EACH issue is resolved
  - Present before/after state clearly
  - No agent self-declared victories
- **Phase 4b: Root Cause Analysis (PER ISSUE) - MANDATORY (NEW #12)**
  - Perform 5-why analysis (reach process/guide gap)
  - Identify prevention point (which stage should have caught it)
  - Draft guide improvement proposal
  - Present to user for confirmation
  - Document in guide_update_recommendations.md
  - Time: 10-20 minutes per issue (captures lessons while context fresh)
- Phase 5: Loop Back to Testing (After ALL issues resolved)
  - After ALL issues resolved → Loop back to testing START
  - Re-run testing from beginning
  - If new issues → Repeat debugging
  - If zero issues → Proceed to next stage
- Feature vs Epic separation
  - Feature issues: feature_XX/debugging/
  - Epic issues: epic_name/debugging/
  - Each has own ISSUES_CHECKLIST.md
- Investigation history preserved (prevents circular debugging)
- All issues must be resolved before proceeding

**Prerequisites I'm verifying:**
✅ Issues discovered during testing (Smoke/QC)
✅ Root cause unknown (requires investigation)
✅ Issues documented in testing failure
✅ Ready to create debugging/ folder

**Updating README Agent Status:**
- Current Phase: DEBUGGING_PROTOCOL
- Current Guide: debugging/debugging_protocol.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Testing Stage Paused: {Stage 5ca Smoke Part 3 / Stage 5cb QC Round 1 / etc}
- Issues Found: {count}
- Loop Back To: {Testing stage to return to}
- Critical Rules: "Issue checklist workflow", "Loop back to testing after resolution", "User verification required"
- Next Action: Create/update debugging/ISSUES_CHECKLIST.md

Creating debugging structure and checklist...
```

**Note:** Debugging protocol phase transitions are handled within the debugging workflow. See debugging/debugging_protocol.md for detailed phase transition requirements.

---

## Resuming In-Progress Epic

**After session compaction during any stage**

**Agent MUST respond:**

```
I'm resuming work on the {epic_name} epic after session compaction. Let me check the current state...

**Reading EPIC_README.md Agent Status:**
- Last Updated: {YYYY-MM-DD HH:MM}
- Current Stage: Stage {X} - {stage name}
- Current Step: {specific step}
- Current Guide: {guide_name}.md
- Progress: {X/Y items complete}
- Next Action: {exact next task}

**I'm now re-reading `{guide_name}.md` to ensure I continue correctly...**

**The guide requires:**
{List 5-7 critical requirements from the guide for THIS stage}

**Verification before continuing:**
✅ {Prerequisite 1}
✅ {Prerequisite 2}
✅ {Prerequisite 3}

**Picking up from where I left off:**
- Current step: {specific step from Agent Status}
- Next action: {next action from Agent Status}

Continuing with {next action}...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
