# Debugging Protocol (Router)

**Purpose:** Structured investigation-centric protocol for resolving bugs discovered during QC/Smoke Testing. Integrated into feature and epic testing with loop-back mechanism.

**When to Use:** Issues discovered during Smoke Testing or QC Rounds with unknown root cause

**Integration Point:** Called from S7.P1 or S7.P2 when issues are found

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting debugging protocol, you MUST:**

1. **Use the phase transition prompt** from `prompts/special_workflows_prompts.md`
   - Find "Starting Debugging Protocol" prompt
   - Speak it out loud (acknowledge requirements)

2. **Update README Agent Status** with:
   - Current Phase: DEBUGGING_PROTOCOL
   - Current Guide: debugging/debugging_protocol.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "Issue checklist workflow", "Loop back to testing after resolution", "User verification required"
   - Next Action: Create/update debugging/ISSUES_CHECKLIST.md

3. **Verify prerequisites** (issues exist in checklist)

4. **THEN AND ONLY THEN** proceed with debugging protocol

---

## Step 0: Update EPIC_README.md Agent Status (MANDATORY)

**When entering debugging protocol, you MUST update EPIC_README.md Agent Status:**

```markdown
## Agent Status

**Debugging Active:** YES - see debugging/ISSUES_CHECKLIST.md
**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** {stage where issue was found, e.g., S9.P3}
**Current Phase:** IN DEBUGGING PROTOCOL
**Current Guide:** debugging/debugging_protocol.md
**Next Action:** {current investigation step}
```bash

**Why this is mandatory:**
- Future agents rely on EPIC_README.md to determine state
- Without explicit "Debugging Active: YES", new agents assume normal workflow
- Critical investigation context is lost without this update
- Historical case: New agent missed active debugging, causing confusion

---

## Quick Start

**What is this protocol?**
Debugging Protocol is an investigation-centric process integrated into QC/Smoke Testing that uses an issue checklist, structured investigation rounds, and loop-back mechanism to ensure all bugs are resolved before proceeding.

**When do you use this protocol?**
- During Smoke Testing (S7.P1): Issues discovered in Part 3 E2E test
- During QC Rounds (S7.P2): Issues discovered in any round
- During Epic Testing (S9): Issues discovered during epic smoke/QC
- Issues have UNKNOWN root cause requiring investigation

**When NOT to use this protocol?**
- Missing requirement where solution is known (use missed_requirement_workflow.md)
- Example: "We forgot to add validation" ← This is a missed requirement, not a bug

---

## 🔀 When to Use This Protocol vs Missed Requirement Protocol

**Use DEBUGGING PROTOCOL when:**
- ✅ Issue discovered during testing (Smoke/QC/Epic Testing)
- ✅ Root cause is UNKNOWN (requires investigation)
- ✅ System behaving unexpectedly

**Use MISSED REQUIREMENT PROTOCOL when:**
- ✅ Gap discovered during planning or implementation
- ✅ Solution is KNOWN (you know what needs to be added)
- ✅ It's a NEW requirement (user didn't ask for it)

**Quick Test:**
- If you need to ask "Why is this happening?" → Debugging Protocol
- If you need to ask "Should we add this feature?" → Missed Requirement Protocol

**See:** CLAUDE.md → "Decision Tree: Which Protocol to Use?" for detailed decision tree with examples

---

**Key Outputs:**
- ✅ debugging/ISSUES_CHECKLIST.md tracking all discovered issues
- ✅ debugging/issue_{number}_{name}.md per issue with investigation history
- ✅ debugging/investigation_rounds.md tracking investigation progress
- ✅ All issues resolved with user confirmation
- ✅ Loop back to testing stage that discovered issues

**Time Estimate:**
Varies (1-8 hours per issue depending on complexity)

**Exit Condition:**
Debugging Protocol complete when ALL issues in ISSUES_CHECKLIST.md are marked 🟢 FIXED with user confirmation, then loop back to testing stage

---

## 🛑 Critical Rules

```bash
1. ⚠️ INTEGRATED WITH TESTING - LOOP-BACK MECHANISM
   - QC/Smoke finds issues → Add to debugging/ISSUES_CHECKLIST.md
   - Enter Debugging Protocol (work through checklist)
   - After ALL issues resolved → Loop back to START of testing stage
   - Repeat testing → If new issues found, repeat debugging
   - Only proceed when testing passes with ZERO new issues

2. ⚠️ ISSUE CHECKLIST WORKFLOW
   - ALL issues tracked in debugging/ISSUES_CHECKLIST.md
   - One issue_{number}_{name}.md file per issue
   - New issues discovered during debugging → add to checklist immediately
   - Work through checklist systematically (one issue at a time)
   - Update checklist status continuously

3. ⚠️ USER VERIFICATION REQUIRED
   - User MUST confirm EACH issue is resolved
   - Present before/after state clearly
   - No agent self-declared victories
   - "Partially fixed" requires new investigation rounds

4. ⚠️ INVESTIGATION ROUND STRUCTURE
   - Round 1: Code Tracing (identify suspicious areas)
   - Round 2: Hypothesis Formation (max 3 testable hypotheses)
   - Round 3: Diagnostic Testing (confirm root cause)
   - Max 5 rounds per issue before user escalation
   - Max 2 hours per round (alert if exceeded)

5. ⚠️ FEATURE-LEVEL VS EPIC-LEVEL
   - Feature issues: feature_XX_name/debugging/
   - Epic issues: epic_name/debugging/
   - Each has its own ISSUES_CHECKLIST.md
   - Feature debugging loops back to feature testing
   - Epic debugging loops back to epic testing

6. ⚠️ PRESERVE INVESTIGATION HISTORY
   - Complete investigation history in issue_{number}_{name}.md
   - Failed hypotheses documented (prevents circular debugging)
   - Diagnostic logs saved to debugging/diagnostic_logs/
   - Code changes tracked via git commit history

7. ⚠️ ALL ISSUES MUST BE RESOLVED BEFORE PROCEEDING
   - Cannot skip issues ("we'll fix it later" is not acceptable)
   - Cannot proceed to next stage with open issues
   - Loop back to testing until ZERO issues remain
```markdown

---

## Debugging Protocol Phases (Overview)

The debugging protocol consists of 5 phases:

### PHASE 1: Issue Discovery & Checklist Update
**See:** `debugging/discovery.md`

**Purpose:** Create/update ISSUES_CHECKLIST.md with discovered issues

**Key Activities:**
- Create debugging/ folder if needed
- Create or update ISSUES_CHECKLIST.md
- Add issues discovered during testing
- Update README Agent Status
- Set up folder structure (feature vs epic)

**Output:** ISSUES_CHECKLIST.md with all issues tracked

---

### PHASE 2: Issue Investigation (Per Issue)
**See:** `debugging/investigation.md`

**Purpose:** Find root cause through structured investigation rounds

**Key Activities:**
- Round 1: Code Tracing & Root Cause Analysis
- Round 2: Hypothesis Formation (max 3 hypotheses)
- Round 3: Diagnostic Testing (confirm root cause)
- Max 5 rounds per issue, max 2 hours per round
- Escalate to user if root cause not found after 5 rounds

**Output:** Confirmed root cause with evidence

---

### PHASE 3: Solution Design & Implementation (Per Issue)
**See:** `debugging/resolution.md`

**Purpose:** Design and implement fix based on confirmed root cause

**Key Activities:**
- Design solution approach
- Implement code changes incrementally
- Add/update tests
- Remove diagnostic logging
- Run full test suite (100% pass required)

**Output:** Solution implemented with passing tests

---

### PHASE 4: User Verification (Per Issue) - MANDATORY
**See:** `debugging/resolution.md`

**Purpose:** Get user confirmation that issue is truly resolved

**Key Activities:**
- Present before/after state to user
- Show test results
- Provide verification steps for user
- Wait for user confirmation
- Handle PARTIALLY/NO responses

**Output:** User-confirmed issue resolution (or back to investigation)

---

### PHASE 4b: Root Cause Analysis (Per Issue) - MANDATORY
**See:** `debugging/root_cause_analysis.md`

**Purpose:** Analyze WHY bug existed and HOW to prevent it through guide improvements

**Key Activities:**
- Perform 5-why analysis (reach process/guide gap)
- Identify prevention point (which stage should have caught it)
- Draft guide improvement proposal
- Present to user for confirmation
- Document in guide_update_recommendations.md

**Output:** User-confirmed root cause + guide improvement (added to recommendations)

**Time:** 10-20 minutes per issue (captures lessons while context fresh)

**Why Mandatory:** Immediate analysis produces 3x higher quality guide improvements vs. delayed analysis

---

### 🚨 CRITICAL: Phase 4b Timing and Importance

**MANDATORY RULE:** Phase 4b MUST be completed IMMEDIATELY after user confirms each issue is fixed.

**DO NOT:**
- ❌ Batch Phase 4b until all issues are fixed
- ❌ Skip Phase 4b "to save time"
- ❌ Delay Phase 4b until Phase 5
- ❌ Write generic "we should be more careful" lessons

**DO:**
- ✅ Complete Phase 4b for Issue 1 → Then start investigating Issue 2
- ✅ Capture specific prevention points (which stage should have caught it)
- ✅ Write actionable guide improvements
- ✅ Get user confirmation of root cause

**WHY THIS MATTERS:**
- Investigation context is fresh (3x better quality analysis)
- Specific details are remembered
- Guide improvements are precise
- Prevents "we'll analyze later" which often becomes "never"

**DATA:** Immediate Phase 4b analysis produces 3x higher quality guide improvements compared to batched analysis (based on historical comparison).

---

### PHASE 5: Loop Back to Testing
**See:** `debugging/loop_back.md`

**Purpose:** After ALL issues resolved, loop back to testing stage

**Key Activities:**
- Verify all issues in checklist are 🟢 FIXED
- Verify Phase 4b root cause analysis completed for ALL issues
- Final code review (remove debug artifacts)
- Run full test suite
- **Cross-bug pattern analysis (MANDATORY)**
  - Review per-issue root causes from Phase 4b
  - Identify patterns across multiple bugs
  - Generate pattern-based guide update recommendations
  - Create process_failure_analysis.md
- Update lessons learned (technical focus)
- Loop back to START of testing stage
- Re-run testing from beginning

**Output:** Clean codebase, process improvements, guide updates, lessons learned, ready to re-test

---

## File Structure

### Feature-Level Debugging

```text
feature_01_player_integration/
├── README.md
├── spec.md
├── checklist.md
├── implementation_plan.md
├── debugging/                          ← Created when first issue found
│   ├── ISSUES_CHECKLIST.md            (Master checklist - ALWAYS CURRENT)
│   ├── investigation_rounds.md         (Meta-tracker)
│   ├── issue_01_scoring_returns_null.md
│   ├── issue_02_projection_calculation_wrong.md
│   ├── process_failure_analysis.md     (Why bugs got through - Phase 5 cross-pattern)
│   ├── guide_update_recommendations.md (Guide improvements - Phase 4b per-issue + Phase 5 patterns)
│   ├── lessons_learned.md              (Technical retrospective)
│   └── diagnostic_logs/
│       ├── issue_01_round1.log
│       ├── issue_01_round2.log
│       └── issue_02_round1.log
└── implementation_checklist.md
```markdown

### Epic-Level Debugging

```text
epic_name/
├── EPIC_README.md
├── epic_smoke_test_plan.md
├── feature_01_player_integration/
├── feature_02_accuracy_simulation/
└── debugging/                          ← Created during epic testing
    ├── ISSUES_CHECKLIST.md
    ├── investigation_rounds.md
    ├── issue_01_integration_conflict.md
    ├── issue_02_data_mismatch.md
    ├── process_failure_analysis.md     (Why bugs got through - Phase 5 cross-pattern)
    ├── guide_update_recommendations.md (Guide improvements - Phase 4b per-issue + Phase 5 patterns)
    ├── lessons_learned.md
    └── diagnostic_logs/
```markdown

---

## Which Phase Should I Use?

**Use this decision tree to navigate to the right guide:**

```text
Starting debugging?
└─ Read debugging/discovery.md (PHASE 1)
   └─ Create ISSUES_CHECKLIST.md

Have issues in checklist, need to investigate?
└─ Read debugging/investigation.md (PHASE 2)
   └─ Rounds 1-3 per issue

Found root cause, need to implement fix?
└─ Read debugging/resolution.md (PHASE 3 & 4)
   └─ Design solution → Implement → Get user verification → Phase 4b

User confirmed fix?
└─ Read debugging/root_cause_analysis.md (PHASE 4b - MANDATORY)
   └─ 5-why analysis → Guide improvement → User confirms root cause
   └─ Repeat for each issue in checklist

All issues fixed and root causes analyzed?
└─ Read debugging/loop_back.md (PHASE 5)
   └─ Cross-bug pattern analysis → Final review → Loop back to testing
```

---

## Summary

**Debugging Protocol is integrated into testing with loop-back mechanism:**

1. **QC/Smoke finds issues** → Add to debugging/ISSUES_CHECKLIST.md
2. **Enter Debugging Protocol** → Work through checklist systematically
3. **Per issue:** Investigation (Rounds 1-3, max 5) → Solution → User Verification
4. **After ALL issues resolved** → Systematic root cause analysis (MANDATORY)
   - Analyze why each bug got through research/implementation
   - Identify cross-bug patterns
   - Generate guide update recommendations
5. **Loop back to START of testing stage**
6. **Re-run testing** → If new issues, repeat; if zero issues, proceed

**Key Features:**
- Issue checklist tracks all bugs
- Structured investigation rounds (trace → hypothesize → test)
- User verification mandatory (no agent self-declaration)
- Investigation history preserved (prevents circular debugging)
- **Process improvement analysis (NEW)** - systematically improve guides based on bugs found
- Loop-back ensures fixes don't introduce new issues

**Sub-Guides:**
- `debugging/discovery.md` - Issue discovery and checklist setup
- `debugging/investigation.md` - Investigation rounds (1-3, max 5)
- `debugging/resolution.md` - Solution design, implementation, user verification
- `debugging/loop_back.md` - Loop-back to testing, lessons learned

**Integration Points:**
- S7.P1 → debugging → loop back
- S7.P2 → debugging → loop back
- S9 (Epic Testing) → debugging → loop back
- S10 (User Testing) → add bugs to epic debugging → loop back to S9

---

**READ THE APPROPRIATE SUB-GUIDE FOR DETAILED INSTRUCTIONS**

*End of debugging/debugging_protocol.md (Router)*
