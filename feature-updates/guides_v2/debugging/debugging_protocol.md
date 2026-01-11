# Debugging Protocol (Router)

**Purpose:** Structured investigation-centric protocol for resolving bugs discovered during QC/Smoke Testing. Integrated into feature and epic testing with loop-back mechanism.

**When to Use:** Issues discovered during Smoke Testing or QC Rounds with unknown root cause

**Integration Point:** Called from Stage 5ca (Smoke Testing) or Stage 5cb (QC Rounds) when issues are found

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

## Quick Start

**What is this protocol?**
Debugging Protocol is an investigation-centric process integrated into QC/Smoke Testing that uses an issue checklist, structured investigation rounds, and loop-back mechanism to ensure all bugs are resolved before proceeding.

**When do you use this protocol?**
- During Smoke Testing (Stage 5ca): Issues discovered in Part 3 E2E test
- During QC Rounds (Stage 5cb): Issues discovered in any round
- During Epic Testing (Stage 6): Issues discovered during epic smoke/QC
- Issues have UNKNOWN root cause requiring investigation

**When NOT to use this protocol?**
- Missing requirement where solution is known (use missed_requirement_workflow.md)
- Example: "We forgot to add validation" ← This is a missed requirement, not a bug

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

```
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
   - Code changes documented in debugging/code_changes.md

7. ⚠️ ALL ISSUES MUST BE RESOLVED BEFORE PROCEEDING
   - Cannot skip issues ("we'll fix it later" is not acceptable)
   - Cannot proceed to next stage with open issues
   - Loop back to testing until ZERO issues remain
```

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
- Document in debugging/code_changes.md
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

### PHASE 5: Loop Back to Testing
**See:** `debugging/loop_back.md`

**Purpose:** After ALL issues resolved, loop back to testing stage

**Key Activities:**
- Verify all issues in checklist are 🟢 FIXED
- Final code review (remove debug artifacts)
- Run full test suite
- **Systematic root cause analysis (MANDATORY)**
  - Analyze why each bug got through research/implementation
  - Identify cross-bug patterns
  - Generate guide update recommendations
- Update lessons learned (technical focus)
- Loop back to START of testing stage
- Re-run testing from beginning

**Output:** Clean codebase, process improvements, guide updates, lessons learned, ready to re-test

---

## File Structure

### Feature-Level Debugging

```
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
│   ├── code_changes.md                 (All fixes for this feature)
│   ├── process_failure_analysis.md     (Why bugs got through process - NEW)
│   ├── guide_update_recommendations.md (Concrete guide updates - NEW)
│   ├── lessons_learned.md              (Technical retrospective)
│   └── diagnostic_logs/
│       ├── issue_01_round1.log
│       ├── issue_01_round2.log
│       └── issue_02_round1.log
├── implementation_checklist.md
└── code_changes.md
```

### Epic-Level Debugging

```
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
    ├── code_changes.md
    ├── process_failure_analysis.md     (Why bugs got through process - NEW)
    ├── guide_update_recommendations.md (Concrete guide updates - NEW)
    ├── lessons_learned.md
    └── diagnostic_logs/
```

---

## Which Phase Should I Use?

**Use this decision tree to navigate to the right guide:**

```
Starting debugging?
└─ Read debugging/discovery.md (PHASE 1)
   └─ Create ISSUES_CHECKLIST.md

Have issues in checklist, need to investigate?
└─ Read debugging/investigation.md (PHASE 2)
   └─ Rounds 1-3 per issue

Found root cause, need to implement fix?
└─ Read debugging/resolution.md (PHASE 3 & 4)
   └─ Design solution → Implement → Get user verification

All issues fixed, ready to loop back?
└─ Read debugging/loop_back.md (PHASE 5)
   └─ Final review → Loop back to testing
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
- Stage 5ca (Smoke Testing) → debugging → loop back
- Stage 5cb (QC Rounds) → debugging → loop back
- Stage 6 (Epic Testing) → debugging → loop back
- Stage 7 (User Testing) → add bugs to epic debugging → loop back to Stage 6

---

**READ THE APPROPRIATE SUB-GUIDE FOR DETAILED INSTRUCTIONS**

*End of debugging/debugging_protocol.md (Router)*
