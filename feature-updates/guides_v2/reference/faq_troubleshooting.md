# FAQ & Troubleshooting Hub

**Purpose:** Central FAQ and troubleshooting resource for agents navigating the Epic-Driven Development v2 workflow

**Last Updated:** 2026-01-04

---

## Table of Contents

1. [General Workflow FAQs](#general-workflow-faqs)
2. [Stage-Specific FAQs](#stage-specific-faqs)
3. [Troubleshooting Decision Trees](#troubleshooting-decision-trees)
4. [Workflow Selection Guide](#workflow-selection-guide)
5. ["I'm Stuck" Protocols](#im-stuck-protocols)
6. [Agent-Specific Issues](#agent-specific-issues)

---

## General Workflow FAQs

### Q: What's the difference between an "epic" and a "feature"?

**A:**
- **Epic** = Top-level work unit containing multiple related features
- **Feature** = Individual component within an epic (Feature 01, Feature 02, etc.)
- **Example:** Epic "Integrate Player Data" might contain features "Add ADP Weighting", "Position-Specific Evaluations", "Cross-Simulation Testing"

### Q: Can I skip stages if they seem unnecessary?

**A:** NO. All stages have dependencies and must be completed in order:
- Stage 1 creates the structure needed for Stage 2
- Stage 2 specs are validated in Stage 3
- Stage 3 alignment feeds into Stage 4 test plan
- Stage 4 test plan evolves through Stage 5 → Stage 6
- Skipping stages leads to incomplete planning and rework

### Q: What's the difference between a "round", "iteration", and "phase"?

**A:**
- **Round:** Collection of iterations (Stage 5a has 3 rounds)
- **Iteration:** Single verification step (Round 1 has Iterations 1-7 + Gate 4a)
- **Phase:** Distinct workflow section (Stage 5c has 3 phases: Smoke Testing, QC Rounds, Final Review)
- **Stage:** Top-level workflow division (7 stages total)

### Q: When do I update EPIC_README.md vs feature README.md?

**A:**
- **EPIC_README.md:** Epic-level status, Epic Progress Tracker, epic-level decisions
- **Feature README.md:** Feature-level status, current guide being followed, implementation progress

Update EPIC_README.md after completing each major stage (1, 2, 3, 4, 5, 6, 7).
Update feature README.md during Stage 5 sub-stages (5a, 5b, 5c, 5d, 5e).

### Q: What happens if I find a bug during implementation?

**A:** Depends on WHEN you find it:
- **During Stage 5b (Implementation):** Fix immediately, run tests, continue
- **During Stage 5c (Smoke/QC):** Enter Debugging Protocol, restart from smoke testing
- **During Stage 6 (Epic QC):** Enter Debugging Protocol, restart entire Stage 6
- **During Stage 7 (User Testing):** Document in ISSUES_CHECKLIST.md, fix ALL bugs, restart Stage 6

### Q: How many features should an epic have?

**A:** Typical range: 3-5 features
- **Too few (<3):** Consider if this is really an epic or just a single feature
- **Too many (>7):** Consider splitting into multiple epics
- **Sweet spot:** 3-5 features that are cohesive but not tightly coupled

### Q: What if I'm asked to do something not covered in the guides?

**A:** Follow this protocol:
1. Check if it's a variation of existing workflows (debugging, missed requirement)
2. Search guides for similar scenarios
3. If truly unique, ask user for clarification
4. Document the approach in lessons_learned.md for future reference
5. Update guides if this becomes a common pattern

---

## Stage-Specific FAQs

### Stage 1: Epic Planning

**Q: User didn't create {epic_name}.txt - what do I do?**

A: Ask user to create the file first:
```
I need you to create feature-updates/{epic_name}.txt with your initial notes about what you want to accomplish. This file should contain:
- What problem are you trying to solve?
- What outcomes do you want?
- Any specific requirements or constraints?

Once you've created this file, I can start Stage 1.
```

**Q: User's epic notes are vague - how detailed do they need to be?**

A: Minimal details acceptable:
- Problem statement (1-2 sentences)
- Desired outcomes (bullet points OK)
- Stage 1 will flesh out details through interactive questions

**Q: How do I know if feature breakdown is too granular or too coarse?**

A: Use these guidelines:
- **Too granular:** Tasks that take <2 hours of implementation (combine into single feature)
- **Too coarse:** Feature needs >7 TODO phases in Stage 5a (split into multiple features)
- **Good granularity:** Feature takes 2-5 hours implementation, 30-50 TODO tasks

**Q: Should I create feature folders for all features at once or one at a time?**

A: Create ALL feature folders in Stage 1:
- Gives user complete picture of epic scope
- Allows Stage 2 to work through features systematically
- Enables cross-feature comparisons during Stage 3

---

### Stage 2: Feature Deep Dives

**Q: User keeps changing requirements during Stage 2 - is this OK?**

A: YES, this is expected during planning:
- Update spec.md with changes immediately
- Document why requirement changed in "Updates History" section
- If changes affect other features, note for Stage 3 alignment
- If scope grows significantly (>35 items), propose feature split

**Q: What if spec.md requirements seem contradictory?**

A: Address immediately:
1. Document the contradiction clearly
2. Ask user which requirement takes priority
3. Update spec.md with resolution
4. Note in checklist.md for Stage 3 review

**Q: How detailed should spec.md be?**

A: Specific enough to create implementation_plan.md in Stage 5a:
- Every user-facing outcome described
- Input/output formats specified
- Edge cases documented
- Integration points identified
- Acceptance criteria clear

**Too vague:** "Add better scoring"
**Good:** "Modify scoring algorithm to weight ADP by position: QB weight 0.8, RB/WR weight 1.0, TE weight 1.2"

**Q: When do I move from Phase 0 to Phase 1 to Phase 2 in Stage 2?**

A: Follow the guide progression:
- **Phase 0 (Research):** Understand epic intent, research codebase, audit existing patterns
- **Phase 1 (Specification):** Write spec.md, create traceability matrix, alignment check
- **Phase 2 (Refinement):** Interactive questions, scope management, user approval

All phases are mandatory - don't skip.

---

### Stage 3: Cross-Feature Sanity Check

**Q: What counts as a "conflict" between features?**

A: Examples of conflicts:
- Both features modify same file/function for different purposes
- Feature A assumes data format that Feature B changes
- Features have overlapping scope (duplicate work)
- Dependency order unclear (Feature A needs Feature B's output)

**Q: How do I resolve conflicts?**

A: Options (user decides):
1. **Merge features:** Combine into single feature
2. **Adjust scope:** Clarify boundaries, remove overlap
3. **Define order:** Specify which feature implements first
4. **Refactor approach:** Change implementation strategy to avoid conflict

**Q: Is it OK to skip pairwise comparison if features seem unrelated?**

A: NO - Always do complete pairwise comparison:
- Features that seem unrelated often have hidden integration points
- Stage 3 catches issues that would be expensive to fix in Stage 5
- Historical evidence: 30% of "unrelated" features had conflicts

---

### Stage 4: Epic Testing Strategy

**Q: How is epic_smoke_test_plan.md different from feature smoke testing?**

A: Key differences:
- **Feature smoke testing (Stage 5c):** Tests single feature in isolation
- **Epic smoke testing (Stage 6):** Tests ALL features working together
- **Epic plan includes:** Cross-feature integration scenarios, epic-level workflows

**Q: What if I don't know integration points yet (haven't implemented)?**

A: Make best predictions in Stage 4:
- Based on spec.md analysis
- Stage 5e will update plan with ACTUAL integration points discovered
- Plan evolves as implementation reveals reality

---

### Stage 5a: TODO Creation

**Q: Can I skip iterations if they don't seem relevant?**

A: NO - All 28 iterations are mandatory:
- Designed based on historical bugs and missed requirements
- Each iteration catches specific issue types
- Skipping iterations = high risk of bugs in Stage 5c

**Q: What if Iteration 24 (GO/NO-GO) says NO-GO?**

A: Follow the guidance in the NO-GO section:
1. Review which criteria failed
2. Determine which iteration to return to
3. Fix issues
4. Re-run affected iterations and gates
5. Make GO decision again
6. DO NOT proceed to Stage 5b with NO-GO

**Q: What's the difference between the 3 mandatory gates?**

A:
- **Gate 4a (Iteration 4a):** TODO Specification Audit - basic quality check (after Round 1)
- **Gate 23a (Iteration 23a):** Pre-Implementation Spec Audit - evidence-based verification (4 PARTS, 100% metrics required)
- **Gate 25 (Iteration 25):** Spec Validation Against Validated Documents - prevents catastrophic bugs (three-way validation)

All three must PASS before Stage 5b.

**Q: How long should Round 3 take?**

A: Total Round 3 time: 2.5-4 hours
- Part 1 (Iterations 17-22): 60-90 minutes
- Part 2a (Gates 1-2): 30-40 minutes
- Part 2b (Gate 3): 30-50 minutes

If taking significantly longer, may indicate:
- TODO plan needs simplification
- Spec has gaps or ambiguities
- Missing prerequisite information

---

### Stage 5b: Implementation Execution

**Q: Tests are failing after implementing a component - what do I do?**

A: Follow this protocol:
1. **STOP** - Do not continue to next component
2. **Fix failing tests** immediately
3. **Identify root cause:** Implementation bug vs test bug vs spec mismatch
4. **Update code_changes.md** with fix
5. **Run ALL tests again** (100% pass required)
6. **Only then** proceed to next component

**Q: Spec requirement seems wrong during implementation - can I change it?**

A: NO - Follow spec exactly during Stage 5b:
- If spec is truly wrong, this is a MISSED REQUIREMENT
- Document in notes
- Complete Stage 5b as spec'd
- Raise in Stage 5c QC rounds
- Will be addressed via missed requirement workflow

**Q: How often should I run tests?**

A: After EVERY component/phase:
- Implement phase 1 → run tests → 100% pass → phase 2
- Typical feature: 5-6 phases, so 5-6 test runs minimum
- More frequent testing = easier debugging

---

### Stage 5c: Post-Implementation

**Q: Smoke testing Part 3 (E2E) failed - do I restart from Part 1?**

A: YES - Complete restart protocol:
1. Enter Debugging Protocol (fix issues)
2. After fixes, restart from Smoke Testing Part 1
3. Re-run Part 1 → Part 2 → Part 3
4. Only proceed to QC rounds if all 3 parts pass

**Q: QC Round 2 found issues - do I restart from Round 1?**

A: NO - Restart from Smoke Testing Part 1:
- Any issues in ANY QC round = restart entire Stage 5c
- Restart from smoke testing (not QC Round 1)
- Zero tolerance for incomplete validation

**Q: What if issues found are "minor" like missing type hint?**

A: Fix immediately - no deferrals:
- Minor issues compound over time
- Zero tech debt tolerance
- Fix now = faster than fixing later

**Q: Can I defer PR review issues to "later"?**

A: NO - Zero tech debt tolerance:
- Fix ALL PR review issues before completing Stage 5c
- This is the LAST checkpoint before Stage 5d/5e
- Deferring issues = they'll appear in Stage 6

---

### Stage 5d/5e: Post-Feature Alignment

**Q: When do I skip Stages 5d and 5e?**

A: Skip ONLY if this was the LAST feature:
- No more features to implement = no specs to update (5d)
- Epic test plan will be validated in Stage 6 anyway (5e)
- Proceed directly to Stage 6

**Q: What if I already updated other feature specs during Stage 5b?**

A: Still do Stage 5d formally:
- Review ALL remaining features systematically
- Capture insights from ACTUAL implementation
- Document integration points discovered
- Update test plan in Stage 5e

**Q: How do I know which specs need updating in Stage 5d?**

A: Review ALL remaining features, but focus on:
- Features that share integration points with completed feature
- Features that made assumptions about completed feature
- Features that depend on completed feature's outputs

---

### Stage 6: Epic-Level Final QC

**Q: What's the difference between Stage 5c and Stage 6?**

A:
- **Stage 5c:** Tests single feature in isolation
- **Stage 6:** Tests ALL features working together as cohesive epic
- **Stage 6 includes Part 4:** Cross-Feature Integration (Stage 5c only has 3 parts)

**Q: Issues found in Stage 6 - do I go back to Stage 5c for that feature?**

A: NO - Enter Debugging Protocol at epic level:
1. Document in epic-level debugging/ISSUES_CHECKLIST.md
2. Fix ALL issues
3. RESTART entire Stage 6 from Phase 6.1 Part 1
4. Re-run epic smoke testing → epic QC rounds → epic final review

**Q: Can I skip epic QC if all features passed their Stage 5c QC?**

A: NO - Epic QC is mandatory:
- Tests integration points (not tested in Stage 5c)
- Tests epic-level workflows
- Validates against original epic request (not individual feature specs)

---

### Stage 7: Epic Cleanup

**Q: User found bugs during testing - what do I do?**

A: Follow Stage 7 bug fix protocol:
1. Document ALL bugs in epic debugging/ISSUES_CHECKLIST.md
2. Create bugfix folders for each bug
3. Fix ALL bugs (each follows Stage 2 → 5a → 5b → 5c)
4. After ALL bugs fixed → RESTART Stage 6 (not Stage 7)
5. Complete Stage 6 validation again
6. Return to Stage 7 user testing
7. ZERO bugs required to commit

**Q: Can I commit if "only minor bugs" remain?**

A: NO - Zero bugs required:
- User testing is the final gate
- ANY bugs = restart Stage 6 after fixing
- Committing with known bugs violates workflow

**Q: Tests were passing in Stage 5b/5c/6 but fail in Stage 7 - how?**

A: Possible causes:
- Environment differences
- Pre-existing test failures from other epics (must fix all tests)
- New edge case discovered
- Fix all failures, run tests again, 100% pass required

---

## Troubleshooting Decision Trees

### Decision Tree 1: "Issues Found During Testing"

```
Issues found during testing
         ↓
    [Do you know the root cause?]
         ↓
    ├─ NO (need investigation)
    │    ↓
    │  [Use Debugging Protocol]
    │    - debugging/debugging_protocol.md
    │    - 5 phases: Discovery, Investigation, Root Cause, Fix, Verification
    │    - Loop back to testing after resolution
    │
    └─ YES (solution is clear)
         ↓
    [Was this requirement in spec?]
         ↓
    ├─ YES (implementation bug)
    │    ↓
    │  [Use Debugging Protocol]
    │    - Clear root cause but still needs documentation
    │    - Skip heavy investigation rounds
    │
    └─ NO (missed requirement)
         ↓
    [Use Missed Requirement Workflow]
         - debugging/missed_requirement_workflow.md
         - Update spec.md
         - Add to implementation_plan.md (if ≤3 tasks) OR return to Stage 5a (if >3 tasks)
```

### Decision Tree 2: "Choosing Between Workflows"

```
Need to fix something
         ↓
    [Where are you in workflow?]
         ↓
    ├─ Stage 5b (Implementation)
    │    ↓
    │  Fix immediately, run tests, continue
    │  (No formal workflow needed)
    │
    ├─ Stage 5c (Smoke/QC)
    │    ↓
    │  [Use Debugging Protocol]
    │    → Fix issues
    │    → RESTART from Smoke Testing Part 1
    │
    ├─ Stage 6 (Epic QC)
    │    ↓
    │  [Use Debugging Protocol at epic level]
    │    → Fix issues
    │    → RESTART from Phase 6.1 Part 1
    │
    └─ Stage 7 (User Testing)
         ↓
    [Use Stage 7 Bug Fix Protocol]
         → Fix ALL bugs
         → RESTART Stage 6
```

### Decision Tree 3: "GO vs NO-GO Decision (Iteration 24)"

```
Iteration 24: GO/NO-GO Decision
         ↓
    [Review all criteria]
         ↓
    ├─ Confidence < MEDIUM
    │    ↓
    │  NO-GO → Return to Round 3 Part 1 (Iteration 17)
    │
    ├─ Gate 4a FAILED
    │    ↓
    │  NO-GO → Return to Round 1 (fix issues, re-run Gate 4a)
    │
    ├─ Gate 23a FAILED (any of 4 parts <100%)
    │    ↓
    │  NO-GO → Return to Round 3 Part 2a (fix issues, re-run Gate 23a)
    │
    ├─ Gate 25 FAILED (discrepancies found)
    │    ↓
    │  NO-GO → Present 3 options to user, fix spec, re-run Gate 25
    │
    └─ ALL criteria met
         ↓
    GO → Proceed to Stage 5b
```

### Decision Tree 4: "Session Compaction - Where Do I Resume?"

```
Context window limit reached → Session compacted
         ↓
    [Check for in-progress epic]
         ↓
    ├─ NO epic folder found
    │    ↓
    │  Check for {epic_name}.txt
    │    → If exists, start Stage 1
    │    → If not, wait for user request
    │
    └─ Epic folder exists
         ↓
    [Read EPIC_README.md Agent Status section]
         ↓
    [Follow "Resuming In-Progress Epic" prompt]
         ↓
    [Read current guide listed in Agent Status]
         ↓
    [Continue from "Next Action" listed]
```

---

## Workflow Selection Guide

### When to Use: Regular Implementation (Stages 1-7)

**Use for:**
- New epic development
- New feature within epic
- Complete implementation cycle

**DO NOT use for:**
- Fixing bugs found during testing (use Debugging)
- Adding missed requirements (use Missed Requirement)
- Quick fixes without epic structure

**Indicators:**
- User says "Help me develop..."
- User created {epic_name}.txt
- Work involves multiple related changes

---

### When to Use: Debugging Protocol

**Use for:**
- Issues found during Smoke Testing (Stage 5c Part 3)
- Issues found during QC Rounds (Stage 5c Phase 2)
- Issues found during Epic Testing (Stage 6)
- Issues found during User Testing (Stage 7)
- Root cause is UNKNOWN (requires investigation)

**DO NOT use for:**
- Quick fixes during implementation (just fix and continue)
- Known missed requirements (use Missed Requirement)
- Spec clarifications (update spec in Stage 2)

**Indicators:**
- Testing revealed unexpected behavior
- Bug is reproducible but cause unclear
- Need investigation rounds to identify root cause

**Entry point:** `debugging/debugging_protocol.md`

---

### When to Use: Missed Requirement Workflow

**Use for:**
- Requirement was NOT in spec.md originally
- Solution is clear (no investigation needed)
- QC/testing revealed missing functionality

**DO NOT use for:**
- Implementation bugs (use Debugging)
- Spec was correct but implementation wrong (use Debugging)
- Unknown root cause (use Debugging)

**Decision threshold:**
- **≤3 tasks needed:** Add tasks, implement, continue
- **>3 tasks needed:** Return to Stage 5a Round 3

**Indicators:**
- "We forgot to add validation"
- "Spec didn't mention error handling for this edge case"
- "This requirement wasn't in the original spec"

**Entry point:** `debugging/missed_requirement_workflow.md`

---

### When to Use: Bug Fix Workflow

**Use for:**
- Bugs found during Stage 7 (User Testing)
- Each bug gets its own bugfix folder
- Bugs go through: Stage 2 → 5a → 5b → 5c (no Stage 1, 3, 4, 6, 7)

**DO NOT use for:**
- Bugs found earlier than Stage 7 (use Debugging)
- Quick fixes during implementation

**Indicators:**
- User says "I found a bug during testing"
- Stage 7 user testing revealed issues
- Need systematic bug tracking and fixes

**Entry point:** `stages/stage_5/bugfix_workflow.md`

---

## "I'm Stuck" Protocols

### Stuck 1: "I don't know which guide to read next"

**Solution:**
1. Check current stage's Agent Status in README (EPIC_README.md or feature README.md)
2. Look at "Next Action" field → tells you which guide to read
3. If Agent Status not updated, check EPIC_README.md "Epic Progress Tracker"
4. Find current feature, see which stage columns are ✅ vs ◻️
5. Read guide for next uncompleted stage

**Common pattern:**
- If Stage 5c just completed → Check if more features remaining
  - YES → Stage 5d
  - NO → Stage 6

### Stuck 2: "Tests are failing and I don't know why"

**Solution:**
1. **Stop** implementing new code
2. **Identify** which tests are failing
3. **Check** if tests were passing before (regression) or new failures
4. **Debugging steps:**
   - Read test failure messages completely
   - Identify which component/function failing
   - Trace data flow to find mismatch
   - Check if recent code change broke tests
5. **Fix** root cause (not just symptoms)
6. **Run ALL tests** again (100% pass required)
7. **Document** fix in code_changes.md

**If still stuck after 30 minutes:**
- Enter Debugging Protocol
- Create issue in debugging/ISSUES_CHECKLIST.md
- Use investigation rounds to systematically identify cause

### Stuck 3: "Iteration 24 says NO-GO but I don't know what to fix"

**Solution:**
1. **Read the failure message** from Iteration 24 decision
2. **Identify specific criteria that failed:**
   - Confidence < MEDIUM → Need more planning (return to Round 3 Part 1)
   - Gate 4a failed → TODO quality issues (return to Round 1)
   - Gate 23a failed → Spec/integration issues (return to Round 3 Part 2a)
   - Gate 25 failed → Spec validation issues (fix spec, re-run Gate 25)
3. **Return to appropriate iteration** as indicated
4. **Fix issues systematically**
5. **Re-run affected gates**
6. **Make GO decision again**

### Stuck 4: "User keeps changing requirements and spec.md is a mess"

**Solution:**
1. **This is normal during Stage 2** - embrace iterative refinement
2. **Update spec.md immediately** with each change
3. **Document changes in "Updates History" section**
4. **If scope growing significantly:**
   - Count total checklist items
   - If >35 items, propose feature split to user
   - Get user approval on split
5. **Continue Stage 2** until user approves spec
6. **Stage 3 Cross-Feature Sanity Check** will catch conflicts

### Stuck 5: "Context window limit reached mid-implementation"

**Solution:**
1. **Update Agent Status** BEFORE session compaction
   - Current stage and guide
   - Current step/iteration
   - Next specific action
   - Critical rules from current guide
2. **When resumed:**
   - New agent will read EPIC_README.md Agent Status
   - Use "Resuming In-Progress Epic" prompt
   - Read current guide to restore context
   - Continue from "Next Action"

**Prevention:**
- Update Agent Status frequently (after each major step)
- Keep "Next Action" specific ("Implement Phase 3 of TODO", not "Continue implementing")

### Stuck 6: "I found an issue but don't know if it's debugging vs missed requirement"

**Decision tree:**
```
Issue found
    ↓
[Was this requirement in spec.md?]
    ↓
├─ YES → Implementation bug → Use Debugging Protocol
└─ NO → Missed requirement
    ↓
[Do you know the solution?]
    ↓
├─ YES → Use Missed Requirement Workflow
└─ NO → Use Debugging Protocol (even though missed req)
```

---

## Agent-Specific Issues

### Issue 1: Context Window Limits

**Symptom:** Session compacted, lost context of current work

**Prevention:**
- Update Agent Status section after each major step
- Keep "Next Action" very specific
- Document current iteration/phase clearly

**Recovery:**
1. Read EPIC_README.md Agent Status section
2. Use "Resuming In-Progress Epic" prompt from prompts_reference_v2.md
3. Read current guide listed in Agent Status
4. Continue from "Next Action"

**Best practices:**
- Update Agent Status every 15-20 minutes during long stages
- Use specific language ("Implementing Phase 3/6 of TODO", not "Working on implementation")
- Include current file being modified if mid-component

---

### Issue 2: Guide Abandonment

**Symptom:** Agent stopped following guide mid-stage

**Causes:**
- Didn't use phase transition prompt
- Assumed guide read from memory instead of using Read tool
- Skipped mandatory reading protocol

**Prevention:**
- ALWAYS use Read tool to load ENTIRE guide before starting stage
- Use phase transition prompts (mandatory acknowledgment)
- Update Agent Status immediately after reading guide

**Recovery:**
1. Check Agent Status - which guide should be followed?
2. Read ENTIRE guide using Read tool
3. Identify current step in guide
4. Resume from that step (don't restart unless required)

**Historical evidence:** 40% guide abandonment rate without mandatory prompts

---

### Issue 3: Resuming After Long Break

**Symptom:** Unclear where previous agent left off

**Solution:**
1. **Read EPIC_README.md completely** (top to bottom)
   - Agent Status section (current guide, next action)
   - Epic Progress Tracker (which features complete)
   - Quick Reference Card (stage/feature/phase summary)
2. **Use "Resuming In-Progress Epic" prompt** (mandatory)
3. **Read current guide** listed in Agent Status
4. **Check feature README.md** if in Stage 5 (feature-level status)
5. **Review recent file changes** (git diff or code_changes.md)
6. **Continue from "Next Action"** (don't backtrack unless necessary)

---

### Issue 4: Conflicting Information Across Guides

**Symptom:** Two guides seem to give different instructions

**Resolution priority (highest to lowest):**
1. **Current stage's main guide** (e.g., implementation_execution.md for Stage 5b)
2. **Reference patterns** (e.g., smoke_testing_pattern.md)
3. **Reference cards** (quick reference, may be abbreviated)
4. **EPIC_WORKFLOW_USAGE.md** (overview, may lack stage-specific details)

**If still conflicting:**
- Follow the guide for your CURRENT stage
- Document conflict in lessons_learned.md
- Propose guide update after epic completes

---

### Issue 5: User Skips Ahead Without Completing Stages

**Symptom:** User asks to implement without completing planning stages

**Response:**
```
I understand you want to move quickly, but the Epic-Driven Development v2 workflow requires completing planning stages before implementation:

Current status: Stage 2 (Feature Deep Dives)
Remaining before implementation:
- Stage 3: Cross-Feature Sanity Check (30-60 min)
- Stage 4: Epic Testing Strategy (30-45 min)
- Stage 5a: TODO Creation (2.5-4 hours)

These stages prevent costly rework by catching issues early.

Would you like to:
1. Continue with current stage (recommended)
2. Discuss specific concerns about the workflow
3. Create a simplified workflow for urgent changes (loses some protections)
```

**Do NOT:**
- Skip stages silently
- Implement without implementation_plan.md (Stage 5a output)
- Bypass mandatory gates

---

### Issue 6: Unsure Which Iteration You're On (Stage 5a)

**Solution:**
1. **Check feature README.md Agent Status:**
   - Should list current iteration (e.g., "Iteration 17: Implementation Phasing")
2. **Check implementation_plan.md file:**
   - Look for "Iteration X" markers in document
   - Last completed iteration marked with ✅
3. **Review Round 3 sub-stage guides:**
   - Part 1 = Iterations 17-22
   - Part 2a = Iterations 23, 23a
   - Part 2b = Iterations 25, 24
4. **If still unclear:**
   - Read last 50 lines of implementation_plan.md
   - Identify which iteration's output was last documented
   - Continue with next iteration

---

## Quick Reference: Common Error Messages

### Error: "Cannot proceed to Stage 5b - Iteration 24 = NO-GO"

**Meaning:** GO/NO-GO decision failed, implementation not ready

**Fix:** See "Stuck 3: Iteration 24 NO-GO" protocol above

---

### Error: "Smoke Testing Part 3 failed - must restart from Part 1"

**Meaning:** E2E test failed, requires complete smoke test restart

**Fix:**
1. Enter Debugging Protocol
2. Fix ALL issues in ISSUES_CHECKLIST.md
3. RESTART from Smoke Testing Part 1 (not Part 3)
4. Re-run all 3 parts

---

### Error: "Gate 23a failed - Completeness = 95% (require 100%)"

**Meaning:** implementation_plan.md doesn't cover all spec requirements

**Fix:**
1. Re-read spec.md completely
2. Identify missing requirements
3. Add TODO tasks for missing requirements
4. Re-run Iteration 23a Part 1 (Completeness Audit)
5. Achieve 100% before proceeding

---

### Error: "Tests failing - cannot proceed with Stage 7 commit"

**Meaning:** Unit tests must have 100% pass rate before commit

**Fix:**
1. DO NOT commit
2. Identify failing tests
3. Fix root cause (not just tests)
4. Run tests again (100% pass required)
5. Only commit when all tests pass

Note: It's acceptable to fix pre-existing test failures from other epics during Stage 7.

---

### Error: "User found bugs during Stage 7 testing"

**Meaning:** Must restart Stage 6 after fixing bugs

**Fix:** See Stage 7 FAQ above - follow bug fix protocol, restart Stage 6

---

## When to Ask User vs. Decide Autonomously

### Ask User (user decision required):

- Feature breakdown looks correct? (Stage 1)
- Spec requirements clear? (Stage 2)
- How to resolve spec conflicts? (Stage 3)
- Iteration 25 found discrepancies - which approach to take? (Stage 5a)
- Scope growing >35 items - split feature? (Stage 2)
- Bug fix vs missed requirement (if ambiguous)

### Decide Autonomously (follow guide rules):

- Which guide to read next (follow Agent Status)
- Whether to restart testing after issues (always restart)
- Whether to fix issues immediately (always fix)
- Which iteration comes next in Stage 5a (follow sequence)
- Whether to skip Stages 5d/5e (decision tree in guide)
- Update Agent Status (always update after major steps)

**Golden Rule:** If guide says "user decision required" or "present options to user" → ASK. Otherwise, follow guide autonomously.

---

## Additional Resources

**For detailed workflows:**
- README.md - Guide index and quick start
- EPIC_WORKFLOW_USAGE.md - Comprehensive usage guide with patterns
- workflow_diagrams.md - Visual diagrams of all workflows

**For specific stages:**
- See `stages/stage_X/` folders for detailed guides

**For reference:**
- `reference/` folder contains patterns, reference cards, and supporting materials

**For prompts:**
- `prompts_reference_v2.md` - Router to phase transition prompts
- `prompts/` folder - Stage-specific prompt files

---

**Last Updated:** 2026-01-04

**Maintenance:** Update this FAQ when common issues are discovered in lessons_learned.md files across epics.
