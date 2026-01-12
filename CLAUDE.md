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

## Project-Specific Rules

### Epic-Driven Development Workflow (v2)

**Note:** CLAUDE_EPICS.md is kept as a separate portable file for copying to other projects. The complete content is also inlined below to ensure all agents always have these instructions loaded.

---

## Epic-Driven Development Workflow (v2)

The v2 workflow is a **7-stage epic-driven development process** for managing large projects:

**Workflow Overview:**
```
Stage 1: Epic Planning → Stage 2: Feature Deep Dives → Stage 3: Cross-Feature Sanity Check →
Stage 4: Epic Testing Strategy → Stage 5: Feature Implementation (5a→5b→5c→5d→5e per feature) →
Stage 6: Epic-Level Final QC → Stage 7: Epic Cleanup (includes Stage 7.5: Guide Updates)
```

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
- Starting any of the 7 stages (1, 2, 3, 4, 5a, 5b, 5c, 5d, 5e, 6, 7)
- Starting Stage 5a rounds (Round 1, 2, 3)
- Starting Stage 5c phases (Smoke Testing, QC Rounds, Final Review)
- Creating missed requirements or entering debugging protocol
- Resuming after session compaction

**See:** `feature-updates/guides_v2/prompts_reference_v2.md` → Complete prompt library

**Why this matters:** Reading the guide first ensures you don't miss mandatory steps. The prompt acknowledgment confirms you understand requirements. Historical evidence: 40% guide abandonment rate without mandatory prompts.

---

## Stage Workflows Quick Reference

**Stage 1: Epic Planning**
- **Trigger:** "Help me develop {epic-name}"
- **First Action:** Use "Starting Stage 1" prompt
- **Guide:** `stages/stage_1/epic_planning.md`
- **Actions:** Assign KAI number, create git branch, analyze epic, create folder structure
- **Next:** Stage 2

**Stage 2: Feature Deep Dives** (Loop through ALL features)
- **First Action:** Use "Starting Stage 2" prompt
- **Guide:** `stages/stage_2/feature_deep_dive.md` (router to phases)
- **Phases:**
  - Phase 2.1: Research (Gate 1: Research Audit)
  - Phase 2.2: Specification (Gate 2: Spec Alignment + **Gate 3: User Checklist Approval**)
  - Phase 2.3: Refinement (Gate 4: User Approval of Acceptance Criteria)
- **Key Outputs:** spec.md, checklist.md (QUESTIONS ONLY - user answers ALL)
- **Next:** Stage 3 (after ALL features)

**Stage 3: Cross-Feature Sanity Check**
- **First Action:** Use "Starting Stage 3" prompt
- **Guide:** `stages/stage_3/cross_feature_sanity_check.md`
- **Actions:** Pairwise comparison, resolve conflicts, user sign-off
- **Next:** Stage 4

**Stage 4: Epic Testing Strategy**
- **First Action:** Use "Starting Stage 4" prompt
- **Guide:** `stages/stage_4/epic_testing_strategy.md`
- **Actions:** Update epic_smoke_test_plan.md
- **Gate 4.5:** User approves test plan (MANDATORY)
- **Next:** Stage 5 (first feature)

**Stage 5: Feature Implementation** (Loop per feature: 5a→5b→5c→5d→5e)

**Stage 5a: Implementation Planning** (28 iterations, 3 rounds)
- **First Action:** Use "Starting Stage 5a Round 1/2/3" prompt
- **Guides:**
  - Round 1: `stages/stage_5/part_5.1.1_round1.md` (Iterations 1-7 + Gates 4a, 7a)
  - Round 2: `stages/stage_5/part_5.1.2_round2.md` (Iterations 8-16, >90% test coverage)
  - Round 3: `stages/stage_5/part_5.1.3_round3.md` (router to Part 1/2a/2b)
    - Part 1: Iterations 17-22 (Preparation)
    - Part 2a: Iterations 23, 23a (Gate 23a: Spec Audit)
    - Part 2b: Iterations 25, 24 (Gate 25: Spec Validation + Gate 24: GO/NO-GO)
- **Output:** implementation_plan.md (~400 lines) - PRIMARY reference
- **Gate 5:** User approves implementation plan (MANDATORY)
- **Next:** Stage 5b

**Stage 5b: Implementation Execution**
- **First Action:** Use "Starting Stage 5b" prompt
- **Guide:** `stages/stage_5/phase_5.2_implementation_execution.md`
- **Actions:** Create implementation_checklist.md, implement from implementation_plan.md
- **Key Principle:** implementation_plan.md = HOW to build (primary), spec.md = WHAT to build (verify)
- **Next:** Stage 5c

**Stage 5c: Post-Implementation** (3 parts + commit)
- **First Action:** Use "Starting Stage 5c Smoke Testing" prompt
- **Guides:**
  - Part 5.3.1: `part_5.3.1_smoke_testing.md` (MANDATORY GATE - if issues → loop back)
  - Part 5.3.2: `part_5.3.2_qc_rounds.md` (3 QC rounds - if issues → loop back to 5.3.1)
  - Part 5.3.3: `part_5.3.3_final_review.md` (PR review, lessons learned)
- **After Part 5.3.3:** COMMIT FEATURE (feature-level commit)
- **Next:** Stage 5d

**Stage 5d: Cross-Feature Spec Alignment**
- **First Action:** Use "Starting Stage 5d" prompt
- **Guide:** `stages/stage_5/phase_5.4_post_feature_alignment.md`
- **Actions:** Update remaining feature specs based on completed feature
- **Next:** Stage 5e

**Stage 5e: Epic Testing Plan Reassessment**
- **First Action:** Use "Starting Stage 5e" prompt
- **Guide:** `stages/stage_5/phase_5.5_post_feature_testing_update.md`
- **Actions:** Reassess epic_smoke_test_plan.md after feature completion
- **Next:** Repeat Stage 5 for next feature OR Stage 6 (if all features done)

**Stage 6: Epic-Level Final QC**
- **First Action:** Use "Starting Stage 6" prompt
- **Guide:** `stages/stage_6/epic_final_qc.md`
- **Actions:** Execute epic_smoke_test_plan.md, 3 QC rounds
- **USER TESTING (MANDATORY - Step 6):** User tests, reports bugs or "no bugs found"
- **If issues:** Enter debugging protocol → Loop back to Phase 6.1
- **Next:** Stage 7 (only when user reports ZERO bugs)

**Stage 7: Epic Cleanup**
- **First Action:** Use "Starting Stage 7" prompt
- **Prerequisites:** Stage 6 complete (user testing PASSED with ZERO bugs)
- **Guide:** `stages/stage_7/epic_cleanup.md`
- **Actions:** Run unit tests (100% pass), Stage 7.5 guide updates, commit, create PR
- **Stage 7.5 (MANDATORY):** Analyze lessons, create GUIDE_UPDATE_PROPOSAL.md, user approval, apply
- **After PR merged:** Update EPIC_TRACKER.md, move epic to done/

**See:** `feature-updates/guides_v2/README.md` for complete workflow overview and guide index.

---

## Missed Requirement Protocol

**When to use:** Missing scope discovered at ANY time (implementation, QA, epic testing), solution is KNOWN

**🚨 FIRST ACTION:** Use "Creating Missed Requirement" prompt

- **Guide:** `missed_requirement/missed_requirement_protocol.md`
- **Before Stage 5:** Update specs directly during Stage 2/3/4
- **After Stage 5 starts:** Create new feature OR update unstarted feature
- **User decides:** Approach + priority (high/medium/low)
- **Process:** Pause work → Stage 2/3/4 for new feature → Resume
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
- **6-Phase Process:**
  1. Issue Discovery & Checklist Update
  2. Investigation (3 rounds: Code Tracing, Hypothesis, Testing)
  3. Solution Design & Implementation
  4. User Verification (MANDATORY)
  5. **Phase 4b: Root Cause Analysis** (MANDATORY per-issue, 5-why analysis)
  6. Loop Back to Testing (cross-pattern analysis)

**Key Requirements:**
- Issue-centric tracking (dedicated file per issue)
- Max 5 investigation rounds before user escalation
- User must confirm each fix
- **Phase 4b IMMEDIATELY after user verification** (NOT batched)
- Zero issues required to proceed

---

## Key Principles

- **Epic-first thinking**: Top-level work unit is an epic (collection of features)
- **Mandatory reading protocol**: ALWAYS read guide before starting stage
- **Phase transition prompts**: MANDATORY acknowledgment (proves guide was read)
- **User approval gates**: Gates 3, 4.5, 5 (early approval prevents rework)
- **Zero autonomous resolution**: Agents create QUESTIONS, user provides ANSWERS
- **Continuous alignment**: Stage 5d updates specs after each feature
- **Iterative testing**: Test plan evolves (Stage 1 → 4 → 5e → 6)
- **28 verification iterations**: All mandatory (Stage 5a Rounds 1-3)
- **QC restart protocol**: If ANY issues → restart completely
- **100% test pass**: Required before commits and stage transitions
- **Zero tech debt tolerance**: Fix ALL issues immediately

---

## Gate Numbering System

The workflow uses two types of gates:

**Type 1: Stage-Level Gates** (whole numbers or decimals)
- Named after the stage they occur in or between
- Most require user approval
- Examples: Gate 3 (Stage 2), Gate 4.5 (Stage 4), Gate 5 (Stage 5a)

**Type 2: Iteration-Level Gates** (iteration numbers)
- Named after the iteration they occur in
- Agent self-validates (using checklists)
- Examples: Gate 4a, Gate 7a, Gate 23a, Gate 24, Gate 25

### Complete Gate List

| Gate | Type | Stage | Purpose | Approver |
|------|------|-------|---------|----------|
| Gate 3 | Stage | Stage 2 | User Checklist Approval | User |
| Gate 4.5 | Stage | Stage 4 | Epic Test Plan Approval | User |
| Gate 5 | Stage | Stage 5a | Implementation Plan Approval | User |
| Gate 4a | Iteration | Stage 5a R1 | TODO Specification Audit | Agent |
| Gate 7a | Iteration | Stage 5a R1 | Backward Compatibility Check | Agent |
| Gate 23a | Iteration | Stage 5a R3 | Pre-Implementation Spec Audit (5 parts) | Agent |
| Gate 24 | Iteration | Stage 5a R3 | GO/NO-GO Decision | Agent |
| Gate 25 | Iteration | Stage 5a R3 | Spec Validation Check | Agent |

**See:** `reference/mandatory_gates.md` for complete gate reference with timing, checklists, and guide locations.

---

## Feature File Structure (Critical for Resuming Work)

**🚨 For epics started before 2026-01-10:** See `feature-updates/guides_v2/reference/OLD_EPIC_COMPATIBILITY.md`

**Quick check:**
```bash
ls feature-updates/{epic_name}/feature_01_*/
# If you see: todo.md → Old epic (use OLD_EPIC_COMPATIBILITY.md)
# If you see: implementation_plan.md → New epic (use structure below)
```

### Standard Feature Folder Structure (NEW EPICS, 2026-01-10 onwards)

```
feature_XX_{name}/
├── README.md                      (Agent Status - current phase, guide, next action)
├── spec.md                        (Requirements specification - user-approved Stage 2)
├── checklist.md                   (QUESTIONS ONLY - user answers ALL before Stage 5a)
├── implementation_plan.md         (Implementation build guide ~400 lines - user-approved Stage 5a)
├── implementation_checklist.md    (Progress tracker ~50 lines - created Stage 5b)
├── code_changes.md                (Actual changes - updated Stage 5b)
├── lessons_learned.md             (Retrospective - created Stage 5c)
└── debugging/                     (Created if issues found during testing)
    ├── ISSUES_CHECKLIST.md
    ├── issue_XX_{name}.md
    └── ...
```

**File Roles:**
- `spec.md` = WHAT to build (requirements) - user-approved Stage 2
- `checklist.md` = QUESTIONS to answer (user input) - user-approved Stage 2 (Gate 3)
- `implementation_plan.md` = HOW to build (implementation guide) - user-approved Stage 5a (Gate 5)
- `implementation_checklist.md` = PROGRESS tracker (real-time updates) - created Stage 5b
- `code_changes.md` = ACTUAL changes (what was done) - updated Stage 5b

---

## Resuming In-Progress Epic Work

**🚨 FIRST: Check epic age** - See OLD_EPIC_COMPATIBILITY.md if epic started before 2026-01-10

**BEFORE starting any epic-related work**, check for in-progress epics:

1. **Check for active epic folders:** Look in `feature-updates/` for any folders (excluding `done/` and `guides_v2/`)

2. **If found, use the "Resuming In-Progress Epic" prompt** from `prompts_reference_v2.md`

3. **READ THE EPIC_README.md FIRST:** Check "Agent Status" section:
   - Current stage and guide
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
- `stages/` - Core workflow guides (stage_1 through stage_7)
- `reference/` - Reference cards and supporting materials
- `templates/` - File templates for epics, features, bug fixes
- `_internal/` - Internal tracking and completion documents

**Key Files:**
- README.md - Workflow overview and guide index
- prompts_reference_v2.md - MANDATORY phase transition prompts
- EPIC_WORKFLOW_USAGE.md - Comprehensive usage guide
- reference/naming_conventions.md - Hierarchical notation rules

---

## Git Branching Workflow

**All epic work must be done on feature branches** (not directly on main).

**Branch format:** `{work_type}/KAI-{number}` (epic/feat/fix)
**Commit format:** `{commit_type}/KAI-{number}: {message}` (feat or fix)

**Stage 1:** Create branch: `git checkout -b {work_type}/KAI-{number}`
**Stage 7:** Create PR for user review, user merges, update EPIC_TRACKER.md

**See:** `GIT_WORKFLOW.md` for complete branching workflow including:
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

**See:** `GIT_WORKFLOW.md` for detailed commit guidelines and examples

---

## Critical Rules Summary

### Always Required

✅ **Read guide before starting stage** (use Read tool for ENTIRE guide)
✅ **Use phase transition prompts** from `prompts_reference_v2.md`
✅ **Verify prerequisites** before proceeding
✅ **Update Agent Status** in README files at checkpoints
✅ **100% unit test pass rate** before commits and stage transitions
✅ **Fix ALL issues immediately** (zero tech debt tolerance)
✅ **User testing approval** before Stage 7 begins (completed in Stage 6)

### Never Allowed

❌ **Skip stages** (all stages have dependencies)
❌ **Skip iterations** in Stage 5a (all 28 mandatory)
❌ **Defer issues for "later"** (fix immediately)
❌ **Skip QC restart** when issues found
❌ **Commit without running tests**
❌ **Commit without user testing approval** (Stage 7)

### Quality Gates

**🛑 MANDATORY GATES (cannot proceed without passing):**
- Gate 3: User Checklist Approval (Stage 2)
- Gate 4.5: Epic Test Plan Approval (Stage 4)
- Gate 5: Implementation Plan Approval (Stage 5a)
- Gate 23a: Pre-Implementation Spec Audit (Stage 5a Round 3)
- Smoke Testing: Must pass before QC rounds (Stage 5c)
- User Testing: Must pass before commit (Stage 7)

**See:** `feature-updates/guides_v2/reference/common_mistakes.md` for comprehensive anti-pattern reference

---

## Additional Resources

**Primary references:**
- **EPIC_WORKFLOW_USAGE.md**: Comprehensive usage guide with setup, patterns, FAQs
- **prompts_reference_v2.md**: All phase transition prompts (MANDATORY)
- **README.md**: Guide index and quick reference
- **PLAN.md**: Complete workflow specification

**Extracted references:**
- **CODING_STANDARDS.md**: Import organization, error handling, logging, docstrings, type hints, testing standards, naming conventions
- **GIT_WORKFLOW.md**: Branch management, commit conventions, PR creation, EPIC_TRACKER.md updates
- **PROTOCOL_DECISION_TREE.md**: Issue/gap discovery flowchart, 4 scenario examples, protocol selection
- **OLD_EPIC_COMPATIBILITY.md**: Working with epics started before 2026-01-10 (todo.md approach)

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
