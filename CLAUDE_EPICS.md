# Epic-Driven Development Workflow - Agent Instructions

**Version:** 2.0
**Last Updated:** 2025-12-31
**Purpose:** Complete instructions for agents using the Epic-Driven Development Workflow v2

---

## Quick Start

**Complete workflow documentation:** `feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md`

**This file contains:** The essential instructions that should be in every project's CLAUDE.md file for agents using the Epic-Driven Development Workflow.

**For detailed guidance:** See `feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md` for comprehensive setup, patterns, and FAQs.

---

## Epic-Driven Development Workflow (v2)

The v2 workflow is a **7-stage epic-driven development process** for managing large projects:

**Workflow Overview:**
```
Stage 1: Epic Planning → Stage 2: Feature Deep Dives → Stage 3: Cross-Feature Sanity Check →
Stage 4: Epic Testing Strategy → Stage 5: Feature Implementation (5a→5b→5c→5d→5e per feature) →
Stage 6: Epic-Level Final QC → Stage 7: Epic Cleanup
```

**Terminology:**
- **Epic** = Top-level work unit (collection of related features)
- **Feature** = Individual component within an epic
- User creates `{epic_name}.txt` → Agent creates `{epic_name}/` folder with multiple `feature_XX_{name}/` folders

---

## 🚨 MANDATORY: Phase Transition Protocol

**When transitioning between ANY stage, you MUST:**

1. **READ the guide FIRST** - Use Read tool to load the ENTIRE guide for that stage
2. **ACKNOWLEDGE what you read** - Use the phase transition prompt from `feature-updates/guides_v2/prompts_reference_v2.md`
3. **VERIFY prerequisites** - Check prerequisites checklist in guide
4. **UPDATE Agent Status** - Update EPIC_README.md or feature README.md with current guide + timestamp
5. **THEN proceed** - Follow the guide step-by-step

**Phase transition prompts are MANDATORY for:**
- Starting any of the 7 stages (1, 2, 3, 4, 5a, 5b, 5c, 5d, 5e, 6, 7)
- Starting Stage 5a rounds (Round 1, 2, 3)
- Starting Stage 5c phases (Smoke Testing, QC Rounds, Final Review)
- Creating a bug fix
- Resuming after session compaction

**See:** `feature-updates/guides_v2/prompts_reference_v2.md` → Complete prompt library

**Why this matters:** Reading the guide first ensures you don't miss mandatory steps. The prompt acknowledgment confirms you understand requirements. Historical evidence: 40% guide abandonment rate without mandatory prompts.

**Example - Starting Stage 5a Round 1:**
```
I'm reading `STAGE_5aa_round1_guide.md` to ensure I follow all 8 iterations in Round 1...

The guide requires:
- Round 1: 8 MANDATORY iterations (iterations 1-7 + 4a)
- Iteration 4a is a MANDATORY GATE (TODO Specification Audit)
- Algorithm Traceability Matrix (iteration 4)
- Integration Gap Check (iteration 7)
- STOP if confidence < Medium at Round 1 checkpoint

Prerequisites I'm verifying:
✅ spec.md exists and is complete
✅ checklist.md all items resolved
✅ Stage 4 (Epic Testing Strategy) complete

I'll now proceed with Round 1 (iterations 1-7 + 4a)...
```

---

## Stage 1: When User Says "Help Me Develop {epic-name}"

**Trigger phrases:** "Help me develop...", "I want to plan...", "Let's work on..."

**Prerequisites:** User has created `feature-updates/{epic_name}.txt` with initial scratchwork notes.

**🚨 FIRST ACTION:** Use the "Starting Stage 1" prompt from `feature-updates/guides_v2/prompts_reference_v2.md`

**Workflow:**
1. **READ:** `feature-updates/guides_v2/STAGE_1_epic_planning_guide.md`
2. **Create git branch for epic** (BEFORE making any changes - see "Git Branching Workflow" section below)
3. **Analyze epic request** and perform codebase reconnaissance
4. **Propose feature breakdown** (agent → user confirms/modifies)
5. **Create epic folder:** `feature-updates/{epic_name}/`
6. **Create feature folders:** `feature_01_{name}/`, `feature_02_{name}/`, etc.
7. **Create epic-level files:**
   - `EPIC_README.md` (with Quick Reference Card, Agent Status, Epic Progress Tracker)
   - `epic_smoke_test_plan.md` (initial version, updated in Stages 4 and 5e)
   - `epic_lessons_learned.md` (cross-feature insights)
8. **Create feature-level files** for each feature:
   - `README.md`, `spec.md`, `checklist.md`, `lessons_learned.md`

**Next:** Stage 2 (Feature Deep Dives)

---

## Stage 2-4: Planning & Testing Strategy

**Stage 2: Feature Deep Dives** (Loop through ALL features)
- **READ:** `STAGE_2_feature_deep_dive_guide.md`
- Flesh out `spec.md` for each feature with detailed requirements
- Interactive question resolution (ONE question at a time)
- Compare to already-completed features for alignment
- Dynamic scope adjustment (if scope >35 items, propose split)

**Stage 3: Cross-Feature Sanity Check** (After ALL features planned)
- **READ:** `STAGE_3_cross_feature_sanity_check_guide.md`
- Systematic pairwise comparison of all feature specs
- Resolve conflicts and inconsistencies
- Get user sign-off on complete plan

**Stage 4: Epic Testing Strategy** (Update test plan)
- **READ:** `STAGE_4_epic_testing_strategy_guide.md`
- Update `epic_smoke_test_plan.md` based on deep dive findings
- Identify integration points between features
- Define epic success criteria

**Next:** Stage 5 (Feature Implementation - first feature)

---

## Stage 5: Feature Implementation (Loop per feature: 5a→5b→5c→5d→5e)

**Stage 5a: TODO Creation** (24 verification iterations across 3 rounds)

**🚨 FIRST ACTION:** Use the "Starting Stage 5a Round 1" prompt from `prompts_reference_v2.md`

- **Round 1:** READ `STAGE_5aa_round1_guide.md` - Iterations 1-7 + 4a
  - Iteration 4: Algorithm Traceability Matrix
  - Iteration 4a: TODO Specification Audit (MANDATORY GATE)
  - Iteration 7: Integration Gap Check
- **Round 2:** READ `STAGE_5ab_round2_guide.md` - Iterations 8-16
  - Iteration 11: Algorithm Traceability Matrix (re-verify)
  - Iteration 14: Integration Gap Check (re-verify)
  - Iteration 15: Test Coverage Depth Check (>90% required)
- **Round 3:** READ `STAGE_5ac_round3_guide.md` - Iterations 17-24 + 23a
  - Iteration 19: Algorithm Traceability Matrix (final verify)
  - Iteration 21: Mock Audit & Integration Test Plan
  - Iteration 23: Integration Gap Check (final verify)
  - Iteration 23a: Pre-Implementation Spec Audit (4 MANDATORY PARTS - ALL must PASS)
  - Iteration 24: Implementation Readiness Protocol (GO/NO-GO decision)
- Create `todo.md` and `questions.md`

**Stage 5b: Implementation Execution**

**🚨 FIRST ACTION:** Use the "Starting Stage 5b" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_5b_implementation_execution_guide.md`
- Keep `spec.md` VISIBLE at all times (not just "consult when needed")
- Continuous spec verification via `implementation_checklist.md`
- Mini-QC checkpoints after each major component
- Create `code_changes.md` documenting all changes
- Run unit tests after EVERY phase (100% pass required)

**Stage 5c: Post-Implementation** (3 phases - smoke testing, QC rounds, final review)

**🚨 FIRST ACTION:** Use the "Starting Stage 5c Smoke Testing" prompt from `prompts_reference_v2.md`

- **Phase 1 (Smoke Testing):** READ `STAGE_5ca_smoke_testing_guide.md`
  - Part 1: Import Test (module loads without errors)
  - Part 2: Entry Point Test (script starts correctly)
  - Part 3: E2E Execution Test (verify OUTPUT DATA VALUES, not just file structure)
  - MANDATORY GATE before QC rounds

- **Phase 2 (QC Rounds):** READ `STAGE_5cb_qc_rounds_guide.md`
  - QC Round 1: Basic validation (<3 critical issues, >80% requirements)
  - QC Round 2: Deep verification (all Round 1 resolved + zero new critical)
  - QC Round 3: Final skeptical review (ZERO tolerance)
  - **QC Restart Protocol:** If ANY issues → COMPLETELY RESTART from smoke testing

- **Phase 3 (Final Review):** READ `STAGE_5cc_final_review_guide.md`
  - PR Review Checklist (11 categories - all mandatory)
  - Lessons learned capture with IMMEDIATE guide updates
  - Final verification (100% completion required)
  - **Zero Tech Debt Tolerance:** Fix ALL issues immediately (no deferrals)

**Stage 5d: Cross-Feature Spec Alignment** (After feature completes)

**🚨 FIRST ACTION:** Use the "Starting Stage 5d" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_5d_post_feature_alignment_guide.md`
- Review ALL remaining (unimplemented) feature specs
- Compare specs to ACTUAL implementation (not just plan)
- Update specs based on real insights from completed feature
- Prevents spec drift as implementation reveals reality

**Stage 5e: Epic Testing Plan Reassessment** (After Stage 5d)

**🚨 FIRST ACTION:** Use the "Starting Stage 5e" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_5e_post_feature_testing_update_guide.md`
- Reassess `epic_smoke_test_plan.md` after EACH feature
- Update test scenarios based on actual implementation
- Add newly discovered integration points
- Keep testing plan current throughout implementation

**Repeat Stage 5 (5a→5b→5c→5d→5e) for EACH feature**

---

## Stage 6-7: Epic Finalization

**Stage 6: Epic-Level Final QC** (After ALL features complete)

**🚨 FIRST ACTION:** Use the "Starting Stage 6" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_6_epic_final_qc_guide.md`
- Execute evolved `epic_smoke_test_plan.md` (reflects all Stage 5e updates)
- Run epic-level smoke testing (tests ALL features integrated together)
- Complete 3 epic-level QC rounds
- Epic-level PR review (11 categories)
- Validate against original epic request
- Create bug fixes for any issues, RESTART Stage 6 after fixes

**Stage 7: Epic Cleanup** (After Stage 6 passes)

**🚨 FIRST ACTION:** Use the "Starting Stage 7" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_7_epic_cleanup_guide.md`
- Run unit tests (100% pass MANDATORY)
- Capture guide improvements
- **User testing (MANDATORY GATE):**
  - Ask user to test complete system themselves
  - If bugs found → Follow bug fix protocol
  - After bug fixes → RESTART Stage 6 (Epic Final QC)
  - Repeat until user testing passes with ZERO bugs
- Update guides based on lessons learned
- Commit changes (only after user testing passes) using new commit message format
- **Merge branch to main** (see "Git Branching Workflow" section below)
- Update EPIC_TRACKER.md with epic details
- Move entire epic folder to `feature-updates/done/{epic_name}/`

---

## Bug Fix Workflow

If bugs are discovered during ANY stage:

**🚨 FIRST ACTION:** Use the "Creating a Bug Fix" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_5_bug_fix_workflow_guide.md`
- Create `bugfix_{priority}_{name}/` folder inside epic
- Priority levels: high, medium, low
- Bug fixes go through: Stage 2 → 5a → 5b → 5c (SKIP Stages 1, 3, 4, 5d, 5e, 6, 7)
- After bug fix complete, return to paused work

---

## Key Principles

- **Epic-first thinking**: Top-level work unit is an epic (collection of features)
- **Mandatory reading protocol**: ALWAYS read guide before starting stage
- **Phase transition prompts**: MANDATORY acknowledgment (proves guide was read)
- **Continuous alignment**: Stage 5d updates specs after each feature
- **Iterative testing**: Test plan evolves (Stage 1 → 4 → 5e → 6)
- **Epic vs feature distinction**: Feature testing (5c) vs epic testing (6) are different
- **24 verification iterations**: All mandatory (across 3 rounds in Stage 5a)
- **QC restart protocol**: If ANY issues → restart completely
- **No skipping stages**: All stages have dependencies, must complete in order
- **100% test pass**: Required before commits and stage transitions
- **Zero tech debt tolerance**: Fix ALL issues immediately (no deferrals)

See `feature-updates/guides_v2/README.md` for complete workflow overview and guide index.

---

## Resuming In-Progress Epic Work

**BEFORE starting any epic-related work**, check for in-progress epics:

1. **Check for active epic folders:** Look in `feature-updates/` for any folders (excluding `done/` and `guides_v2/`)

2. **If found, use the "Resuming In-Progress Epic" prompt** from `feature-updates/guides_v2/prompts_reference_v2.md`

3. **READ THE EPIC_README.md FIRST:** Check the "Agent Status" section at the top with:
   - Current stage and guide
   - Current step/iteration
   - Next action to take
   - Critical rules from current guide

4. **READ THE CURRENT GUIDE:** Use Read tool to load the guide listed in Agent Status

5. **Continue from where previous agent left off** - Don't restart the workflow

**Why this matters:** Session compaction can interrupt agents mid-workflow. EPIC_README.md Agent Status survives context window limits and provides exact resumption point.

---

## Epic Folder Structure

### Epic-Level Files
```
feature-updates/{epic_name}/
├── EPIC_README.md                    # Master tracking (Quick Reference, Agent Status, Progress)
├── epic_smoke_test_plan.md           # How to test complete epic (evolves)
├── epic_lessons_learned.md           # Cross-feature insights and guide improvements
```

### Feature Folders
```
├── feature_01_{name}/                # Feature 1
│   ├── README.md                     # Feature context and Agent Status
│   ├── spec.md                       # PRIMARY SPECIFICATION (detailed requirements)
│   ├── checklist.md                  # Resolved vs pending decisions
│   ├── todo.md                       # Implementation tracking (created Stage 5a)
│   ├── questions.md                  # Questions for user (created Stage 5a if needed)
│   ├── implementation_checklist.md   # Continuous spec verification (Stage 5b)
│   ├── code_changes.md               # Documentation of changes (Stage 5b)
│   ├── lessons_learned.md            # Feature-specific insights
│   └── research/                     # Research documents (if needed)
├── feature_02_{name}/                # Feature 2 (same structure)
├── feature_03_{name}/                # Feature 3 (same structure)
```

### Bug Fix Folders (if any)
```
└── bugfix_{priority}_{name}/         # Bug fix folder
    ├── notes.txt                     # Issue description (user-verified)
    ├── spec.md                       # Fix requirements
    ├── checklist.md                  # Same as features
    ├── todo.md                       # Same as features
    ├── implementation_checklist.md   # Same as features
    ├── code_changes.md               # Same as features
    └── lessons_learned.md            # Same as features
```

---

## Workflow Guides Location

**All guides located in:** `feature-updates/guides_v2/`

**Stage Guides (16 guides):**
- `STAGE_1_epic_planning_guide.md` - Stage 1: Epic Planning
- `STAGE_2_feature_deep_dive_guide.md` - Stage 2: Feature Deep Dives
- `STAGE_3_cross_feature_sanity_check_guide.md` - Stage 3: Cross-Feature Sanity Check
- `STAGE_4_epic_testing_strategy_guide.md` - Stage 4: Epic Testing Strategy
- `STAGE_5aa_round1_guide.md` - Stage 5a Round 1: Iterations 1-7 + 4a
- `STAGE_5ab_round2_guide.md` - Stage 5a Round 2: Iterations 8-16
- `STAGE_5ac_round3_guide.md` - Stage 5a Round 3: Iterations 17-24 + 23a
- `STAGE_5b_implementation_execution_guide.md` - Stage 5b: Implementation
- `STAGE_5ca_smoke_testing_guide.md` - Stage 5c Phase 1: Smoke Testing
- `STAGE_5cb_qc_rounds_guide.md` - Stage 5c Phase 2: QC Rounds
- `STAGE_5cc_final_review_guide.md` - Stage 5c Phase 3: Final Review
- `STAGE_5d_post_feature_alignment_guide.md` - Stage 5d: Cross-Feature Alignment
- `STAGE_5e_post_feature_testing_update_guide.md` - Stage 5e: Testing Plan Update
- `STAGE_5_bug_fix_workflow_guide.md` - Bug Fix Workflow
- `STAGE_6_epic_final_qc_guide.md` - Stage 6: Epic-Level Final QC
- `STAGE_7_epic_cleanup_guide.md` - Stage 7: Epic Cleanup

**Supporting Files (5 files):**
- `EPIC_WORKFLOW_USAGE.md` - Complete usage guide (setup, patterns, FAQs)
- `prompts_reference_v2.md` - MANDATORY phase transition prompts
- `templates_v2.md` - File templates (epic, feature, bug fix)
- `README.md` - Workflow overview and guide index
- `PLAN.md` - Complete v2 workflow specification

---

## Git Branching Workflow

**All epic work must be done on feature branches** (not directly on main).

### Branch Management

**When starting an epic (Stage 1):**

1. **Verify you're on main:**
   ```bash
   git checkout main
   ```

2. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

3. **Assign KAI number:**
   - Check `feature-updates/EPIC_TRACKER.md` for next available number
   - Update EPIC_TRACKER.md with new epic in "Active Epics" table

4. **Determine work type:**
   - `epic` - Work with multiple features (most epics)
   - `feat` - Work with single feature only
   - `fix` - Bug fix work

5. **Create and checkout branch:**
   ```bash
   git checkout -b {work_type}/KAI-{number}
   ```
   Examples:
   - `git checkout -b epic/KAI-1`
   - `git checkout -b feat/KAI-2`
   - `git checkout -b fix/KAI-3`

**During epic work (Stages 1-6):**
- All work happens on the epic branch
- Commits use format: `{commit_type}/KAI-{number}: {message}`
  - `commit_type` is either `feat` or `fix` (NOT `epic`)
  - `feat` - Feature-related commits
  - `fix` - Bug fix commits
- Commit at normal times (currently Stage 7 Step 6)

**When completing an epic (Stage 7):**

1. **Commit changes on branch** (after user testing passes)

2. **Merge to main:**
   ```bash
   git checkout main
   git pull origin main
   git merge {work_type}/KAI-{number}
   ```

3. **Push to origin:**
   ```bash
   git push origin main
   ```

4. **Update EPIC_TRACKER.md:**
   - Move epic from "Active" to "Completed" table
   - Add epic detail section with commits
   - Increment "Next Available Number"

5. **Delete branch (optional):**
   ```bash
   git branch -d {work_type}/KAI-{number}
   ```

### Branch Naming Convention

**Format:** `{work_type}/KAI-{epic_number}`

**Work types:**
- `epic` - Epic with multiple features
- `feat` - Single feature (not a full epic)
- `fix` - Bug fix

**Epic number:**
- Unique sequential number starting from 1
- Tracked in `feature-updates/EPIC_TRACKER.md`
- Incremented for each new epic

**Examples:**
- `epic/KAI-1` - First epic (multi-feature)
- `feat/KAI-2` - Second work item (single feature)
- `fix/KAI-3` - Third work item (bug fix)

### Commit Message Convention

**Format:** `{commit_type}/KAI-{number}: {message}`

**Commit types:**
- `feat` - Feature implementation commits
- `fix` - Bug fix commits

**Epic number:**
- Same number as the branch
- All commits in an epic use the same KAI number

**Message:**
- Brief, descriptive (100 chars or less)
- No emojis or subjective prefixes
- Describe what was done (imperative mood)

**Examples:**
- `feat/KAI-1: Add ADP integration to PlayerManager`
- `feat/KAI-1: Create matchup difficulty calculation`
- `feat/KAI-1: Integrate schedule strength analysis`
- `fix/KAI-1: Correct bye week penalty calculation`
- `fix/KAI-2: Fix draft mode crash when no players available`

**Multi-feature epics:**
- All features in the same epic use the same KAI number
- No need to indicate feature number in commit message
- Example: epic/KAI-1 with features 1, 2, 3 all use `feat/KAI-1: {message}`

### EPIC_TRACKER.md Management

**Location:** `feature-updates/EPIC_TRACKER.md`

**Purpose:** Central log of all epics with KAI numbers, descriptions, and commit history

**When to update:**
1. **Starting epic (Stage 1):** Add to "Active Epics" table
2. **Completing epic (Stage 7):** Move to "Completed Epics" table and add detail section
3. **After each commit:** Track in EPIC_TRACKER for final documentation

**Required information:**
- KAI number
- Epic name
- Type (epic/feat/fix)
- Branch name
- Description
- Features implemented
- Key changes
- Commit history
- Testing results
- Lessons learned

See `feature-updates/EPIC_TRACKER.md` for template and examples.

---

## Pre-Commit Protocol

**MANDATORY BEFORE EVERY COMMIT**

**When the user requests to commit changes:**

### STEP 1: Run Unit Tests (REQUIRED)

**PROJECT-SPECIFIC: Update this command for your project**
```bash
python tests/run_all_tests.py
```

**Test Requirements:**
- All unit tests must pass (100% pass rate)
- Exit code 0 = safe to commit, 1 = DO NOT COMMIT
- **Only proceed to commit if all tests pass**

### STEP 2: If Tests Pass, Commit Changes

1. Analyze all changes with `git status` and `git diff`
2. Update documentation if functionality changed
3. Stage and commit with clear, concise message
4. Follow commit standards:
   - Format: `{commit_type}/KAI-{number}: {message}`
   - Brief, descriptive messages (100 chars or less)
   - No emojis or subjective prefixes
   - commit_type is `feat` or `fix`
   - List major changes in body

### STEP 3: If Tests Fail

- **STOP** - Do NOT commit
- Fix failing tests (including pre-existing failures from other epics)
- Re-run tests
- Only commit when all tests pass (exit code 0)

**Note:** It is acceptable to fix pre-existing test failures during Stage 7 to achieve 100% pass rate.

**Do NOT skip validation**: 100% test pass rate is mandatory

---

## Critical Rules Summary

### Always Required

✅ **Read guide before starting stage** (use Read tool for ENTIRE guide)
✅ **Use phase transition prompts** from `prompts_reference_v2.md`
✅ **Verify prerequisites** before proceeding
✅ **Update Agent Status** in README files at checkpoints
✅ **100% unit test pass rate** before commits and stage transitions
✅ **Fix ALL issues immediately** (zero tech debt tolerance)
✅ **User testing approval** before final commit (Stage 7)

### Never Allowed

❌ **Skip stages** (all stages have dependencies)
❌ **Skip iterations** in Stage 5a (all 24 mandatory)
❌ **Defer issues for "later"** (fix immediately)
❌ **Skip QC restart** when issues found
❌ **Commit without running tests**
❌ **Commit without user testing approval** (Stage 7)

### Quality Gates

**🛑 MANDATORY GATES (cannot proceed without passing):**
- Iteration 4a: TODO Specification Audit (Stage 5a Round 1)
- Iteration 23a: Pre-Implementation Spec Audit (Stage 5a Round 3)
- Smoke Testing: Part 3 must pass before QC rounds (Stage 5c)
- User Testing: Must pass before commit (Stage 7)

---

## For New Projects

**To use this workflow in a new project:**

1. **Copy the guides folder:**
   ```bash
   cp -r feature-updates/guides_v2/ /path/to/new-project/feature-updates/guides_v2/
   ```

2. **Create folder structure:**
   ```bash
   mkdir -p /path/to/new-project/feature-updates/done/
   ```

3. **Copy this file to new project:**
   ```bash
   cp CLAUDE_EPICS.md /path/to/new-project/CLAUDE_EPICS.md
   ```

4. **Add to project's CLAUDE.md:**
   ```markdown
   ## Epic-Driven Development Workflow

   See `CLAUDE_EPICS.md` for complete workflow instructions.

   **Quick reference:**
   - Complete documentation: `feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md`
   - New epic: Start with Stage 1 guide
   - Resume work: Check EPIC_README.md Agent Status
   ```

5. **Customize for your project:**
   - Update test command in "Pre-Commit Protocol" section
   - Add project-specific file paths if different
   - Add project-specific commit standards
   - Update any project-specific terminology

**See:** `feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md` for detailed setup instructions, common patterns, and FAQs.

---

## Additional Resources

**Primary references:**
- **EPIC_WORKFLOW_USAGE.md**: Comprehensive usage guide with setup, patterns, FAQs
- **prompts_reference_v2.md**: All phase transition prompts (MANDATORY)
- **templates_v2.md**: File templates for epic, feature, and bug fix folders
- **README.md**: Guide index and quick reference
- **PLAN.md**: Complete workflow specification

**When to read what:**
- **Starting new epic?** Read STAGE_1_epic_planning_guide.md
- **Resuming work?** Read EPIC_README.md Agent Status section
- **Confused about workflow?** Read EPIC_WORKFLOW_USAGE.md
- **Need a prompt?** Read prompts_reference_v2.md
- **Creating files?** Read templates_v2.md
- **Guide improvements?** Document in epic_lessons_learned.md

---

**END OF CLAUDE_EPICS.md**

---

**Remember:** This workflow exists to ensure quality, completeness, and maintainability. Follow it rigorously, learn from each epic, and continuously improve the guides based on lessons learned.
