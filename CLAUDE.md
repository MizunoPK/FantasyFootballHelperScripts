# Fantasy Football Helper Scripts - Claude Code Guidelines

## 🚨 CRITICAL: TRUST FILE STATE OVER CONVERSATION SUMMARIES

**ALWAYS prioritize actual file contents over conversation summaries when determining project state:**

1. **Check README.md files FIRST** - These contain the authoritative current status
2. **Verify with actual source code** - Check what's actually implemented
3. **Read Agent Status sections** - These are updated to reflect true current state
4. **Conversation summaries can be outdated** - Files are the source of truth

**Example workflow:**
- User says "proceed" → Read current README.md Agent Status → Determine actual next step
- Don't assume conversation summary reflects current file state
- Always verify implementation status by checking actual code files

---

## Quick Start for New Agents

**FIRST**: Read `ARCHITECTURE.md` for complete architectural overview, system design, and implementation details.

**SECOND**: Read `README.md` for project overview, installation instructions, and usage guide.

**THIS FILE**: Contains workflow rules, coding standards, and commit protocols.

---

## Epic-Driven Development Workflow (v2)

The v2 workflow is a **10-stage epic-driven development process** for managing large projects:

**Workflow Overview:**
```
S1: Epic Planning → S2: Feature Deep Dives → S3: Cross-Feature Sanity Check →
S4: Epic Testing Strategy → S5-S8: Feature Loop (per feature) → S9: Epic-Level Final QC →
S10: Epic Cleanup (includes S10.P1: Guide Updates)

Per-feature loop: S5 (Planning) → S6 (Execution) → S7 (Testing) → S8 (Alignment) → Repeat or S9
```

**Notation System:**
- **S#** = Stage (Level 1) - e.g., S1, S5
- **S#.P#** = Phase (Level 2) - e.g., S2.P1, S5.P1
- **S#.P#.I#** = Iteration (Level 3) - e.g., S5.P1.I2
- Stages/Phases/Iterations reserved for hierarchy only; use "Step" for implementation tasks

**Terminology:**
- **Epic** = Top-level work unit (collection of related features)
- **Feature** = Individual component within an epic
- **KAI Number** = Unique epic identifier (tracked in EPIC_TRACKER.md)
- User creates `{epic_name}.txt` → Agent creates `KAI-{N}-{epic_name}/` folder with multiple `feature_XX_{name}/` folders

**See:** `feature-updates/guides_v2/reference/glossary.md` for complete term definitions and alphabetical index

---

## 🚨 MANDATORY: Phase Transition Protocol

**When transitioning between ANY stage, you MUST:**

1. **READ the guide FIRST** - Use Read tool to load the ENTIRE guide for that stage
2. **ACKNOWLEDGE what you read** - Use the phase transition prompt from `feature-updates/guides_v2/prompts_reference_v2.md`
3. **VERIFY prerequisites** - Check prerequisites checklist in guide
4. **UPDATE Agent Status** - Update EPIC_README.md or feature README.md with current guide + timestamp
5. **THEN proceed** - Follow the guide step-by-step

**Phase transition prompts are MANDATORY for:**
- Starting any of the 10 stages (S1, S2, S3, S4, S5, S6, S7, S8, S9, S10)
- Starting S5 rounds (Round 1, 2, 3)
- Starting S7 phases (Smoke Testing, QC Rounds, Final Review)
- Creating missed requirements or entering debugging protocol
- Resuming after session compaction

**See:** `feature-updates/guides_v2/prompts_reference_v2.md` → Complete prompt library

**Why this matters:** Reading the guide first ensures you don't miss mandatory steps. The prompt acknowledgment confirms you understand requirements. Historical evidence: 40% guide abandonment rate without mandatory prompts.

---

## 🚨 CRITICAL: Stage Workflows Are Quick Reference ONLY

```
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️ DO NOT use Stage Workflows below as substitute for guides   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Stage Workflows section provides NAVIGATION ONLY                │
│ - Shows which guide to read                                     │
│ - Shows first action (prompt) to use                            │
│ - Shows next stage                                              │
│                                                                  │
│ You MUST read the FULL guide for each stage                     │
│ - Use Read tool to load ENTIRE guide                            │
│ - Follow ALL steps in guide                                     │
│ - Do NOT work from this quick reference alone                   │
│                                                                  │
│ Skipping guide reading = 40% abandonment rate (historical data) │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stage Workflows Quick Reference

**S1: Epic Planning**
- **Trigger:** "Help me develop {epic-name}"
- **First Action:** Use "Starting S1" prompt
- **Guide:** `stages/s1/s1_epic_planning.md`
- **Actions:** Assign KAI number, create git branch, analyze epic, create folder structure
- **Next:** S2

**S2: Feature Deep Dives** (Loop through ALL features)
- **First Action:** Use "Starting S2" prompt
- **Guide:** `stages/s2/s2_feature_deep_dive.md` (router to phases)
- **Phases:**
  - S2.P1: Research (Gate 1: Research Audit)
  - S2.P2: Specification (Gate 2: Spec Alignment + **Gate 3: User Checklist Approval**)
    - S2.P2.5: Specification Validation (self-validate spec, resolve questions, reduce user burden)
  - S2.P3: Refinement (Gate 4: User Approval of Acceptance Criteria)
- **Key Outputs:** spec.md, checklist.md (QUESTIONS ONLY - agents CANNOT mark [x] autonomously)
- **Next:** S3 (after ALL features)

**S3: Cross-Feature Sanity Check**
- **First Action:** Use "Starting S3" prompt
- **Guide:** `stages/s3/s3_cross_feature_sanity_check.md`
- **Actions:** Pairwise comparison, resolve conflicts, user sign-off
- **Next:** S4

**S4: Epic Testing Strategy**
- **First Action:** Use "Starting S4" prompt
- **Guide:** `stages/s4/s4_epic_testing_strategy.md`
- **Actions:** Update epic_smoke_test_plan.md
- **Gate 4.5:** User approves test plan (MANDATORY)
- **Next:** S5 (first feature)

**S5-S8: Feature Loop** (Repeat for each feature)

**S5: Implementation Planning** (28 iterations, 3 rounds)
- **First Action:** Use "Starting S5 Round 1/2/3" prompt
- **🚨 CRITICAL:** Execute iterations ONE at a time, IN ORDER (no batching, no skipping)
- **Guides:**
  - Round 1: `stages/s5/s5_p1_planning_round1.md` (router to I1-I3)
    - S5.P1.I1: `stages/s5/s5_p1_i1_requirements.md` (Iterations 1-3)
    - S5.P1.I2: `stages/s5/s5_p1_i2_algorithms.md` (Iterations 4-6 + Gate 4a)
    - S5.P1.I3: `stages/s5/s5_p1_i3_integration.md` (Iteration 7 + Gate 7a)
  - Round 2: `stages/s5/s5_p2_planning_round2.md` (router to I1-I3)
    - S5.P2.I1: `stages/s5/s5_p2_i1_test_strategy.md` (Iterations 8-10)
    - S5.P2.I2: `stages/s5/s5_p2_i2_reverification.md` (Iterations 11-12)
    - S5.P2.I3: `stages/s5/s5_p2_i3_final_checks.md` (Iterations 13-16, >90% test coverage)
  - Round 3: `stages/s5/s5_p3_planning_round3.md` (router to I1-I3)
    - S5.P3.I1: `stages/s5/s5_p3_i1_preparation.md` (Iterations 17-22)
    - S5.P3.I2: `stages/s5/s5_p3_i2_gates_part1.md` (Iterations 23, 23a - Gate 23a: Spec Audit)
    - S5.P3.I3: `stages/s5/s5_p3_i3_gates_part2.md` (Iterations 24-25 - Gate 25 + Gate 24: GO/NO-GO)
- **Output:** implementation_plan.md (~400 lines) - PRIMARY reference
- **Gate 5:** User approves implementation plan (MANDATORY)
- **Next:** S6

**S6: Implementation Execution**
- **First Action:** Use "Starting S6" prompt
- **Guide:** `stages/s6/s6_execution.md`
- **Actions:** Create implementation_checklist.md, implement from implementation_plan.md
- **Key Principle:** implementation_plan.md = HOW to build (primary), spec.md = WHAT to build (verify)
- **Next:** S7

**S7: Implementation Testing & Review** (3 phases + commit)
- **First Action:** Use "Starting S7.P1 Smoke Testing" prompt
- **🚨 RESTART PROTOCOL:** If ANY issues found → Restart from S7.P1 (NOT mid-QC)
- **Guides:**
  - S7.P1: `stages/s7/s7_p1_smoke_testing.md` (MANDATORY GATE - if issues → enter debugging, fix, restart S7.P1)
  - S7.P2: `stages/s7/s7_p2_qc_rounds.md` (3 QC rounds - if issues → enter debugging, fix, restart S7.P1)
  - S7.P3: `stages/s7/s7_p3_final_review.md` (PR review, lessons learned)
- **After S7.P3:** COMMIT FEATURE (feature-level commit)
- **Next:** S8

**S8: Post-Feature Alignment** (2 phases)
- **First Action:** Use "Starting S8.P1" prompt
- **Guides:**
  - S8.P1: `stages/s8/s8_p1_cross_feature_alignment.md` (Update remaining feature specs)
  - S8.P2: `stages/s8/s8_p2_epic_testing_update.md` (Reassess epic_smoke_test_plan.md)
- **Actions:** Update remaining feature specs and epic testing plan based on completed feature
- **Next:** Repeat S5 for next feature OR S9 (if all features done)

**S9: Epic-Level Final QC**
- **First Action:** Use "Starting S9" prompt
- **🚨 RESTART PROTOCOL:** If ANY issues found → Restart from S9.P1 (NOT mid-QC)
- **Guide:** `stages/s9/s9_epic_final_qc.md` (router to phases)
- **Phases:**
  - S9.P1: `stages/s9/s9_p1_epic_smoke_testing.md` (Epic smoke testing)
  - S9.P2: `stages/s9/s9_p2_epic_qc_rounds.md` (3 QC rounds)
  - S9.P3: `stages/s9/s9_p3_user_testing.md` (User tests, reports bugs or "no bugs found")
  - S9.P4: `stages/s9/s9_p4_epic_final_review.md` (Final review)
- **If issues:** Enter debugging protocol → Fix all issues → Restart from S9.P1
- **Next:** S10 (only when user reports ZERO bugs)

**S10: Epic Cleanup**
- **First Action:** Use "Starting S10" prompt
- **Prerequisites:** S9 complete (user testing PASSED with ZERO bugs)
- **Guide:** `stages/s10/s10_epic_cleanup.md`
- **Actions:** Run unit tests (100% pass), S10.P1 guide updates, commit, create PR
- **S10.P1 (MANDATORY):** `stages/s10/s10_p1_guide_update_workflow.md` - Analyze lessons, create GUIDE_UPDATE_PROPOSAL.md, user approval, apply
- **After PR merged:** Update EPIC_TRACKER.md, move epic to done/

**See:** `feature-updates/guides_v2/README.md` for complete workflow overview and guide index.

---

## Missed Requirement Protocol

**When to use:** Missing scope discovered at ANY time (implementation, QA, epic testing), solution is KNOWN

**🚨 FIRST ACTION:** Use "Creating Missed Requirement" prompt

- **Guide:** `missed_requirement/missed_requirement_protocol.md`
- **Before S5:** Update specs directly during S2/S3/S4
- **After S5 starts:** Create new feature OR update unstarted feature
- **User decides:** Approach + priority (high/medium/low)
- **Process:** Pause work → S2/S3/S4 for new feature → Resume
- **Priority determines sequence:** high = before current, medium = after current, low = at end

---

## 🔀 Protocol Decision Tree

**When you discover an issue or gap:**

**Quick Summary:**
- **Known solution + NEW requirement** → Missed Requirement Protocol
- **Unknown root cause** → Debugging Protocol
- **Known solution + NOT new requirement** → Just implement it (regular work)
- **Need user input** → Add to questions.md, ask user

**See:** `feature-updates/guides_v2/reference/PROTOCOL_DECISION_TREE.md` for complete decision tree with:
- Issue/Gap discovery flowchart
- 4 detailed scenario examples with analysis
- Protocol selection criteria and common mistakes

---

## Debugging Protocol

**When to use:** Issues discovered during QC/Smoke testing with UNKNOWN root cause requiring investigation

**🚨 FIRST ACTION:** Use "Starting Debugging Protocol" prompt

- **Guide:** `debugging/debugging_protocol.md`
- **File Structure:** Feature-level or epic-level `debugging/` folder
- **6-Step Process:**
  1. Issue Discovery & Checklist Update
  2. Investigation (3 rounds: Code Tracing, Hypothesis, Testing)
  3. Solution Design & Implementation
  4. User Verification (MANDATORY)
  5. **Step 4b: Root Cause Analysis** (MANDATORY per-issue, 5-why analysis)
  6. Loop Back to Testing (cross-pattern analysis)

**Key Requirements:**
- Issue-centric tracking (dedicated file per issue)
- Max 5 investigation rounds before user escalation
- User must confirm each fix
- **Step 4b IMMEDIATELY after user verification** (NOT batched)
- Zero issues required to proceed

---

## Key Principles

- **Epic-first thinking**: Top-level work unit is an epic (collection of features)
- **Mandatory reading protocol**: ALWAYS read guide before starting each guide
- **Phase transition prompts**: MANDATORY acknowledgment (proves guide was read)
- **User approval gates**: Gates 3, 4.5, 5 (early approval prevents rework)
- **Zero autonomous resolution**: Agents create QUESTIONS, user provides ANSWERS
- **Continuous alignment**: S8.P1 updates specs after each feature
- **Continuous testing**: Test plan evolves (S1 → S4 → S8.P2 → S9)
- **28 verification iterations**: All mandatory (S5 Rounds 1-3)
- **QC restart protocol**: If ANY issues → restart completely
- **100% test pass**: Required before commits and transitions
- **Zero tech debt tolerance**: Fix ALL issues immediately

---

## Common Anti-Patterns to Avoid

### Anti-Pattern 1: Autonomous Checklist Resolution

**WRONG WORKFLOW:**
1. User asks question
2. Agent investigates
3. Agent marks question as RESOLVED
4. Agent adds requirement to spec
5. User sees requirement added without approval

**CORRECT WORKFLOW:**
1. User asks question
2. Agent investigates
3. Agent marks question as PENDING USER APPROVAL
4. Agent presents findings
5. User says "approved"
6. ONLY THEN agent marks RESOLVED and adds requirement

**Key Distinction:** Research findings ≠ User approval

**Example from KAI-6:**
- ❌ WRONG: "I checked simulations. Question 1 RESOLVED. Added Requirement 9."
- ✅ CORRECT: "I checked simulations. My findings: [details]. Status: PENDING. Approve?"

### Anti-Pattern 2: Narrow Investigation Scope

**WRONG APPROACH:**
1. User asks "check if this works with simulations"
2. Agent checks method calls only
3. Agent declares investigation complete
4. User asks "what about config loading?"
5. Agent realizes investigation was incomplete

**CORRECT APPROACH:**
1. User asks "check if this works with simulations"
2. Agent uses systematic 5-category checklist:
   - Category 1: Method/function calls ✓
   - Category 2: Configuration/data loading ✓
   - Category 3: Integration points ✓
   - Category 4: Timing/dependencies ✓
   - Category 5: Edge cases ✓
3. Agent presents comprehensive findings covering all categories
4. User approves once (not multiple follow-ups needed)

**Key Distinction:** Use systematic frameworks, don't rely on intuition

**When investigating compatibility/integration:**
- DON'T check just the most obvious aspect
- DO use 5-category investigation checklist (see S2.P3 guide)
- DON'T assume first answer is complete
- DO ask "what else?" at least 3 times

---

## Gate Numbering System

The workflow uses two types of gates:

**Type 1: Stage-Level Gates** (whole numbers or decimals)
- Named after the stage they occur in or between
- Most require user approval
- Examples: Gate 3 (S2), Gate 4.5 (S4), Gate 5 (S5)

**Type 2: Iteration-Level Gates** (iteration numbers)
- Named after the iteration they occur in
- Agent self-validates (using checklists)
- Examples: Gate 4a, Gate 7a, Gate 23a, Gate 24, Gate 25

### Complete Gate List

| Gate | Type | Location | Purpose | Approver |
|------|------|----------|---------|----------|
| Gate 1 | Stage | S2 | Research Completeness Audit | Agent (checklist) |
| Gate 2 | Stage | S2 | Spec-to-Epic Alignment | Agent (checklist) |
| Gate 3 | Stage | S2 | User Checklist Approval | User |
| Gate 4.5 | Stage | S4 | Epic Test Plan Approval | User |
| Gate 5 | Stage | S5.P1 | Implementation Plan Approval | User |
| Gate 4a | Iteration | S5.P1.I2 | TODO Specification Audit | Agent (checklist) |
| Gate 7a | Iteration | S5.P1.I3 | Backward Compatibility Check | Agent (checklist) |
| Gate 23a | Iteration | S5.P3.I2 | Pre-Implementation Spec Audit (5 parts) | Agent (checklist) |
| Gate 24 | Iteration | S5.P3.I3 | GO/NO-GO Decision | Agent (confidence) |
| Gate 25 | Iteration | S5.P3.I3 | Spec Validation Check | Agent (checklist) |

**See:** `reference/mandatory_gates.md` for complete gate reference with timing, checklists, and guide locations.

---

## Feature File Structure (Critical for Resuming Work)

### Standard Feature Folder Structure

```
feature_XX_{name}/
├── README.md                      (Agent Status - current guide, next action)
├── spec.md                        (Requirements specification - user-approved S2)
├── checklist.md                   (QUESTIONS ONLY - user answers ALL before S5.P1)
├── implementation_plan.md         (Implementation build guide ~400 lines - user-approved S5.P1)
├── implementation_checklist.md    (Progress tracker ~50 lines - created S6)
├── code_changes.md                (Actual changes - updated S6)
├── lessons_learned.md             (Retrospective - created S7.P3)
└── debugging/                     (Created if issues found during testing)
    ├── ISSUES_CHECKLIST.md
    ├── issue_XX_{name}.md
    └── ...
```

**File Roles:**
- `spec.md` = WHAT to build (requirements) - user-approved S2
- `checklist.md` = QUESTIONS to answer (user input) - user-approved S2 (Gate 3)
- `implementation_plan.md` = HOW to build (implementation guide) - user-approved S5 (Gate 5)
- `implementation_checklist.md` = PROGRESS tracker (real-time updates) - created S6
- `code_changes.md` = ACTUAL changes (what was done) - updated S6

---

## Resuming In-Progress Epic Work

**BEFORE starting any epic-related work**, check for in-progress epics:

1. **Check for active epic folders:** Look in `feature-updates/` for any folders (excluding `done/` and `guides_v2/`)

2. **If found, use the "Resuming In-Progress Epic" prompt** from `prompts_reference_v2.md`

3. **READ THE EPIC_README.md FIRST:** Check "Agent Status" section:
   - Current guide (S#.P#.I# notation)
   - Current step/iteration
   - Next action to take
   - Critical rules from current guide

4. **READ THE CURRENT GUIDE:** Use Read tool to load the guide listed in Agent Status

5. **Continue from where previous agent left off** - Don't restart the workflow

**Why this matters:** Session compaction can interrupt agents mid-workflow. EPIC_README.md Agent Status survives context window limits and provides exact resumption point.

---

## Workflow Guides Location

**All guides:** `feature-updates/guides_v2/`

**Directory Structure:**
- `stages/` - Core workflow guides (s1 through s10 with S#.P#.I# notation)
- `reference/` - Reference cards and supporting materials
- `templates/` - File templates for epics, features, bug fixes
- `_internal/` - Internal tracking and completion documents

**Key Files:**
- README.md - Workflow overview and guide index
- prompts_reference_v2.md - MANDATORY phase transition prompts
- EPIC_WORKFLOW_USAGE.md - Comprehensive usage guide
- reference/naming_conventions.md - S#.P#.I# notation system rules

---

## Git Branching Workflow

**All epic work must be done on feature branches** (not directly on main).

**Branch format:** `{work_type}/KAI-{number}` (epic/feat/fix)
**Commit format:** `{commit_type}/KAI-{number}: {message}` (feat or fix)

**S1:** Create branch: `git checkout -b {work_type}/KAI-{number}`
**S10:** Create PR for user review, user merges, update EPIC_TRACKER.md

**See:** `feature-updates/guides_v2/reference/GIT_WORKFLOW.md` for complete branching workflow including:
- Detailed branch management steps
- Commit message conventions and examples
- PR creation and review process
- EPIC_TRACKER.md management
- Common scenarios and troubleshooting

---

## Pre-Commit Protocol

**MANDATORY BEFORE EVERY COMMIT**

### STEP 1: Run Unit Tests (REQUIRED)

**PROJECT-SPECIFIC: Update this command for your project**
```bash
python tests/run_all_tests.py
```

**Requirements:**
- All unit tests must pass (100% pass rate)
- Exit code 0 = safe to commit, 1 = DO NOT COMMIT
- **Only proceed to commit if all tests pass**

### STEP 2: If Tests Pass, Review ALL Changes

**⚠️ CRITICAL: Include ALL modified source code files**
```bash
git status  # Check ALL modified files
git diff    # Review changes
```

**Verify all source files are included:**
- [ ] Main source files (*.py in league_helper/, simulation/, etc.)
- [ ] ALL test files that were modified (tests/**/*.py)
- [ ] Configuration files if modified (data/*.json, data/*.csv)

### STEP 3: Stage and Commit Changes

**Follow commit standards:**
- Format: `{commit_type}/KAI-{number}: {message}`
- Brief, descriptive messages (100 chars or less)
- No emojis or subjective prefixes
- commit_type is `feat` or `fix`

### STEP 4: If Tests Fail

- **STOP** - Do NOT commit
- Fix failing tests (including pre-existing failures)
- Re-run tests
- Only commit when all tests pass (exit code 0)

**See:** `feature-updates/guides_v2/reference/GIT_WORKFLOW.md` for detailed commit guidelines and examples

---

## Critical Rules Summary

### Always Required

✅ **Read guide before starting** (use Read tool for ENTIRE guide)
✅ **Use phase transition prompts** from `prompts_reference_v2.md`
✅ **Verify prerequisites** before proceeding
✅ **Update Agent Status** in README files at checkpoints
✅ **100% unit test pass rate** before commits and transitions
✅ **Fix ALL issues immediately** (zero tech debt tolerance)
✅ **User testing approval** before S10 begins (completed in S9.P3)

### Never Allowed

❌ **Skip stages** (all stages have dependencies)
❌ **Skip iterations** in S5 (all 28 mandatory)
❌ **Batch iterations** (execute ONE at a time, sequentially)
❌ **Defer issues for "later"** (fix immediately)
❌ **Skip QC restart** when issues found (restart from beginning)
❌ **Commit without running tests**
❌ **Commit without user testing approval** (S10)

### Quality Gates

**🛑 MANDATORY GATES (cannot proceed without passing):**
- Gate 3: User Checklist Approval (S2)
- Gate 4.5: Epic Test Plan Approval (S4)
- Gate 5: Implementation Plan Approval (S5)
- Gate 23a: Pre-Implementation Spec Audit (S5.P3 Round 3)
- Smoke Testing: Must pass before QC rounds (S7.P1)
- User Testing: Must pass before S10 (S9.P3)

**See:** `feature-updates/guides_v2/reference/common_mistakes.md` for comprehensive anti-pattern reference

---

## Additional Resources

**Primary references:**
- **EPIC_WORKFLOW_USAGE.md**: Comprehensive usage guide with setup, patterns, FAQs
- **prompts_reference_v2.md**: All phase transition prompts (MANDATORY)
- **README.md**: Guide index and quick reference

**Extracted references:**
- **CODING_STANDARDS.md**: Import organization, error handling, logging, docstrings, type hints, testing standards, naming conventions
- **feature-updates/guides_v2/reference/GIT_WORKFLOW.md**: Branch management, commit conventions, PR creation, EPIC_TRACKER.md updates
- **feature-updates/guides_v2/reference/PROTOCOL_DECISION_TREE.md**: Issue/gap discovery flowchart, 4 scenario examples, protocol selection

---

**Remember:** This workflow exists to ensure quality, completeness, and maintainability. Follow it rigorously, learn from each epic, and continuously improve the guides based on lessons learned.

---

## Current Project Structure

**Core Scripts:** `run_league_helper.py`, `run_simulation.py`, `run_player_fetcher.py`, `run_scores_fetcher.py`

**Main Modules:**
- `league_helper/` - 4 interactive modes (draft, optimizer, trade, data editor) + utilities
- `simulation/` - Parameter optimization through league simulation
- `player-data-fetcher/` - API data collection
- `nfl-scores-fetcher/` - NFL scores and team rankings
- `utils/` - Shared utilities (logging, error handling, CSV I/O)
- `tests/` - 2,200+ tests (100% pass rate required)
- `data/` - League config, player stats, team rankings
- `docs/scoring/` - 10-step scoring algorithm documentation
- `feature-updates/` - Epic-driven development

**See:**
- `ARCHITECTURE.md` - Complete architectural details
- `README.md` - Installation and usage
- `CODING_STANDARDS.md` - Complete coding standards and testing guidelines
