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
- Starting S1.P3 Discovery Phase
- Starting S5 phases (Draft Creation, Validation Loop)
- Starting S7 phases (Smoke Testing, QC Rounds, Final Review)
- Creating missed requirements or entering debugging protocol
- Resuming after session compaction

**Agent Status updates are MANDATORY at phase boundaries:**

When to update:
- After completing ANY phase (S#.P#)
- After completing ANY iteration (S#.P#.I#)
- Before requesting user approval
- After user provides input
- At EVERY checkpoint completion

What to update in Agent Status section:
- Last Updated: [current timestamp]
- Current Stage: [S#.P# notation]
- Current Step: [what you just completed]
- Next Action: [what you're about to do]
- Current Guide: [guide file path]
- Guide Last Read: [timestamp]

**DO NOT batch updates** - Update after EACH phase/iteration, not at end of day.

**Why this matters:**
- Agent Status survives session compaction (context window limits)
- Enables precise resumption if session interrupted
- Provides user visibility into progress
- Proves work was completed (accountability)

**Historical failure:** KAI-7 agent completed entire S1.P3 Discovery Phase (4 sub-phases, 2 iterations, multiple hours of work) without a SINGLE Agent Status update. EPIC_README.md timestamp showed work from previous day, giving no indication of current progress.

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

## 🚨 Checkpoint Requirements

Guides contain mandatory checkpoints marked with 🛑 or "CHECKPOINT".

**What a checkpoint means:**
1. STOP all work immediately
2. Use Read tool to re-read specified guide section(s)
3. Output acknowledgment: "✅ CHECKPOINT [N]: Re-read [sections]"
4. Update Agent Status in README (current step, timestamp)
5. ONLY THEN continue with next section

**Checkpoints are NOT optional:**
- "Checkpoint" = blocking requirement (not advisory)
- Must perform re-reading BEFORE continuing
- Must output acknowledgment to prove completion
- Historical evidence: 80% skip rate without explicit acknowledgment

**Why checkpoints exist:**
- Agents (including you) work from memory after initial guide reading
- Memory-based execution causes 40%+ violation rate
- Re-reading takes 30 seconds, prevents hours of rework
- Acknowledgment proves checkpoint was performed

**Example checkpoint execution:**

❌ WRONG:
- Read guide once at beginning
- Execute all steps from memory
- See checkpoint marker, think "I remember this"
- Skip checkpoint re-reading
- Discover violations later during QC

✅ CORRECT:
- Read guide section
- Execute steps for that section
- See 🛑 MANDATORY CHECKPOINT marker
- STOP immediately (do not proceed)
- Use Read tool to re-read specified sections
- Output: "✅ CHECKPOINT 1: Re-read Critical Rules and Discovery Loop sections"
- Update Agent Status with completion timestamp
- ONLY THEN continue with next section

**Historical failure:** KAI-7 agent completed entire S1.P3 Discovery Phase (4 sub-phases, 2 iterations, 3 mandatory checkpoints) without performing a SINGLE checkpoint re-reading or Agent Status update. All 3 checkpoints were skipped despite being clearly marked in guide.

---

## Stage Workflows Quick Reference

**🚨 READ THE FULL GUIDE** before starting each stage - this is navigation only.

### 🚨 Guide Selection Protocol

**CLAUDE.md Stage Workflow table is the authoritative source for guide paths.**

When transitioning between stages:
1. ✅ Check EPIC_README.md Epic Completion Checklist - is current stage FULLY complete?
2. ✅ Read CLAUDE.md Stage Workflow table - which guide for next stage?
3. ✅ Use Read tool on EXACT guide listed in CLAUDE.md (ignore other files)
4. ❌ Do NOT glob for guides and pick one - always use CLAUDE.md reference
5. ❌ Do NOT skip phase/iteration checks within stages

**If you find multiple guides in a stage folder:**
- Trust CLAUDE.md Stage Workflow table (source of truth)
- Old guides may exist temporarily during refactors
- When in doubt, ask user which guide to use

**If CLAUDE.md and filesystem conflict:**
- CLAUDE.md wins (user updates CLAUDE.md first during refactors)
- Report discrepancy to user
- Use the guide path from CLAUDE.md

---

| Stage | Trigger | Guide | Key Actions | Next |
|-------|---------|-------|-------------|------|
| **S1** | "Help me develop {epic}" | `stages/s1/s1_epic_planning.md` | KAI number, git branch, **Discovery Phase (MANDATORY)**, folder structure | S2 |
| **S2** | Complete S1 | `stages/s2/s2_feature_deep_dive.md` | spec.md, checklist.md, RESEARCH_NOTES.md (Gate 3: User approval) | S3 |
| **S3** | All features done S2 | `stages/s3/s3_epic_planning_approval.md` | Epic testing strategy, documentation (Gate 4.5: User approval) | S4 |
| **S4** | S3 approved | `stages/s4/s4_feature_testing_strategy.md` | test_strategy.md (4 iterations, Validation Loop) | S5 |
| **S5** | S4 complete | `stages/s5/s5_v2_validation_loop.md` | implementation_plan.md (Draft + Validation Loop, Gate 5: User approval) | S6 |
| **S6** | S5 approved | `stages/s6/s6_execution.md` | implementation_checklist.md, implement code | S7 |
| **S7** | S6 complete | `stages/s7/s7_p1_smoke_testing.md` | Smoke test, 3 QC rounds, commit feature | S8 |
| **S8** | S7 complete | `stages/s8/s8_p1_cross_feature_alignment.md` | Update remaining specs, update epic testing plan | S5 (next) or S9 |
| **S9** | All features done | `stages/s9/s9_epic_final_qc.md` | Epic smoke test, 3 QC rounds, user testing (ZERO bugs required) | S10 |
| **S10** | S9 passed | `stages/s10/s10_epic_cleanup.md` | Unit tests (100% pass), guide updates (S10.P1 MANDATORY), PR | Done |

**Critical Workflows:**
- **S1.P3 Discovery Phase:** MANDATORY for ALL epics - research loop until 3 consecutive iterations with no new questions
- **S5 v2 Structure:** 2-phase approach (Draft Creation 60-90 min + Validation Loop 3.5-6 hours with 11 dimensions, 3 consecutive clean rounds required)
- **🚨 RESTART PROTOCOL:** S7/S9 - If ANY issues found → Restart from phase beginning (S7.P1 or S9.P1)

**Phase Transition Prompts:** `feature-updates/guides_v2/prompts_reference_v2.md` (MANDATORY)

**Complete Workflow Details:** `feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md` → "Stage-by-Stage Detailed Workflows"

---

## 🔀 S2 Parallel Work (Optional for 3+ Features)

**When Offered:** During S1 Step 5.9 (if epic has 3+ features)
**Benefits:** 40-60% time reduction for S2 phase
**Complexity:** Requires spawning secondary agents and coordination

### Quick Decision

**OFFER parallel work if:**
- Epic has 3+ features (significant time savings)
- User is time-constrained

**SKIP parallel work if:**
- Only 1-2 features (minimal benefit)
- User prefers simplicity

**User decides:** Always present options, let user choose

### Parallelization Modes

**Group-Based (dependency groups exist):**
- Features organized into groups based on spec-level dependencies
- Wave 1: Group 1 completes S2 first
- Wave 2: Group 2 starts after Group 1 S2 complete
- See: `parallel_work/s2_primary_agent_group_wave_guide.md`

**Full Parallelization (all features independent):**
- All features execute S2 simultaneously
- No dependency waves needed
- See: `parallel_work/s2_primary_agent_guide.md`

### 🚨 S2 Parallel Work Structure Rules

**When executing parallel S2 work, you MUST follow this structure EXACTLY:**

**Allowed Coordination Directories (3 only):**
1. `.epic_locks/` - Lock files
2. `agent_comms/` - Communication FILES (no subdirectories)
3. `agent_checkpoints/` - Checkpoint .json FILES (no subdirectories)

**Prohibited:**
- ❌ `parallel_work/` directory
- ❌ `agent_comms/inboxes/` subdirectories
- ❌ `agent_comms/agent_checkpoints/` nesting
- ❌ `agent_comms/coordination/` or any nested coordination dirs
- ❌ Checkpoint files with .md extension
- ❌ Communication channel directories (must be files)

**Required:**
- ✅ ALL features (including Feature 01) MUST have STATUS file
- ✅ ALL checkpoint files MUST use .json extension (not .md)
- ✅ ALL communication channels MUST be individual .md files in agent_comms/
- ✅ Handoff packages saved in feature folders: `feature_XX_{name}/HANDOFF_PACKAGE.md`
- ✅ Primary creates ALL directories, secondaries create FILES only
- ✅ Run validation script after infrastructure setup: `bash feature-updates/guides_v2/parallel_work/scripts/validate_structure.sh .`

**File Format Requirements:**
- Checkpoint files: `.json` extension (e.g., `secondary_a.json`)
- Communication files: `.md` files directly in `agent_comms/` (e.g., `primary_to_secondary_a.md`)
- STATUS files: Plain text key-value in each feature folder
- Handoff packages: `.md` files in feature folders (e.g., `feature_02_{name}/HANDOFF_PACKAGE.md`)

**Validation:**
```bash
# After Primary creates infrastructure, run:
bash feature-updates/guides_v2/parallel_work/scripts/validate_structure.sh .

# Expected: ✅ PASSED - structure valid
# If errors: Fix before generating handoff packages
```

### If User Chooses Parallel Work

**Primary Agent (you):**
- Create ALL coordination directories (`.epic_locks/`, `agent_comms/`, `agent_checkpoints/`)
- Create STATUS file for Feature 01
- Run validation script
- Generate and save handoff packages to feature folders
- Execute S2 for Feature 01
- Coordinate with secondaries every 15 min
- Run S3/S4 solo after all features complete S2

**Secondary Agent (if joining):**
- Receive one-line startup instruction from user
- Read handoff package from feature folder automatically
- Create ONLY your checkpoint.json and STATUS files (NOT directories)
- Execute S2 for assigned feature
- Coordinate every 15 min
- WAIT for Primary to run S3/S4

**Complete Protocols:** `feature-updates/guides_v2/parallel_work/`
- `s2_parallel_protocol.md` - Complete 9-phase workflow + structure requirements
- `s2_primary_agent_guide.md` - Primary agent workflow (full parallelization)
- `s2_primary_agent_group_wave_guide.md` - Primary agent workflow (group-based waves)
- `s2_secondary_agent_guide.md` - Secondary agent workflow
- `scripts/validate_structure.sh` - Structure validation script
- Infrastructure, recovery, and template files

**Parallel work is OPTIONAL** - workflow works identically in sequential mode.

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

**Planning & Discovery:**
- Epic-first thinking, S1.P3 Discovery Phase MANDATORY (research + Q&A loop until 3 consecutive clean iterations), continuous alignment (S8.P1)

**Execution & Quality:**
- Read guide before starting, use phase transition prompts, update Agent Status at checkpoints
- User approval gates (Gates 3, 4.5, 5), zero autonomous resolution, continuous testing

**Implementation:**
- Test-driven development (S4 before S5), 22 verification iterations (S5 Rounds 1-3)
- Validation Loop validation (3 consecutive clean rounds, zero deferred issues, max 10 rounds)
- QC restart protocol (if ANY issues → restart), 100% test pass, zero tech debt tolerance

---

## Common Anti-Patterns to Avoid

**🚨 CRITICAL: Avoid these anti-patterns** - Historical evidence shows these cause 80%+ of epic failures.

### Anti-Pattern 1: Autonomous Checklist Resolution
**Wrong:** Agent researches → Marks RESOLVED → Adds requirement
**Correct:** Agent researches → Marks PENDING → Presents findings → User approves → THEN mark RESOLVED
**Key:** Research findings ≠ User approval

### Anti-Pattern 2: Narrow Investigation Scope
**Wrong:** Check obvious aspect → Declare complete
**Correct:** Use systematic 5-category checklist (method calls, config, integration, timing, edge cases)
**Key:** Use systematic frameworks, don't rely on intuition

### Anti-Pattern 3: Deferring Issues During Validation Loop
**Wrong:** Find 5 issues → Note for later → Continue to next round
**Correct:** Find 5 issues → Fix ALL immediately → Then continue
**Key:** Validation Loop has ZERO TOLERANCE for deferred issues

**Complete Anti-Pattern Reference:** `feature-updates/guides_v2/reference/common_mistakes.md`
- Detailed workflows with step-by-step examples
- Recovery protocols for each anti-pattern
- Additional anti-patterns and edge cases
- Historical failure case studies

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
| Gate 1 | Stage | S2.P1.I1 | Research Completeness Audit (embedded in Validation Loop) | Agent (checklist) |
| Gate 2 | Stage | S2.P1.I3 | Spec-to-Epic Alignment (embedded in Validation Loop) | Agent (checklist) |
| Gate 3 | Stage | S2.P1.I3 | User Checklist Approval (separate from Validation Loop) | User |
| Gate 4.5 | Stage | S3.P3 | Epic Plan Approval (3-tier rejection handling) | User |
| Gate 5 | Stage | S5.P3 | Implementation Plan Approval (3-tier rejection handling) | User |
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

**Note:** Git commit history provides all change tracking, eliminating need for separate change documentation.

---

## Resuming In-Progress Epic Work

**BEFORE starting any epic-related work**, check for in-progress epics:

1. **Check for active epic folders:** Look in `feature-updates/` for any folders (excluding `done/` and `guides_v2/`)

2. **CHECK FOR ACTIVE DEBUGGING:** Look for `debugging/` folder in epic or feature folders
   - If `debugging/` folder exists, read `debugging/ISSUES_CHECKLIST.md` FIRST
   - Active debugging takes priority over Agent Status in EPIC_README.md
   - You may be mid-investigation or have unresolved issues

3. **If found, use the "Resuming In-Progress Epic" prompt** from `prompts_reference_v2.md`

4. **READ THE EPIC_README.md FIRST:** Check "Agent Status" section:
   - Current guide (S#.P#.I# notation)
   - Current step/iteration
   - Next action to take
   - Critical rules from current guide
   - **Debugging Active field** (if YES, check debugging/ folder)

5. **READ THE CURRENT GUIDE:** Use Read tool to load the guide listed in Agent Status

6. **Continue from where previous agent left off** - Don't restart the workflow

**Why this matters:** Session compaction can interrupt agents mid-workflow. EPIC_README.md Agent Status survives context window limits and provides exact resumption point. Active debugging must be detected to avoid missing critical investigation context.

---

## Workflow Guides Location

**🚨 CRITICAL:** When user says "guides" = EVERY FILE in `feature-updates/guides_v2/`

**Complete guide structure:**
- `stages/` - Core workflow (s1-s10)
- `reference/` - Mandatory gates, common mistakes, glossary, consistency loop protocols
- `templates/` - File templates
- `debugging/` - Debugging protocol
- `missed_requirement/` - Missed requirement protocol
- `prompts/` - Phase transition prompts (MANDATORY)
- `parallel_work/` - Parallel work coordination
- `audit/` - Modular audit system

**Key files:**
- `README.md` - Guide index
- `prompts_reference_v2.md` - MANDATORY phase transition prompts
- `EPIC_WORKFLOW_USAGE.md` - Comprehensive usage guide

**When user says "audit the guides":**
1. Read `audit/README.md` - Entry point
2. Run `bash feature-updates/guides_v2/audit/scripts/pre_audit_checks.sh`
3. Read `audit/stages/stage_1_discovery.md` - Begin Round 1

**Find all guides:** `Glob pattern="**/*.md" path="feature-updates/guides_v2"`

**See:** `feature-updates/guides_v2/README.md` for complete file index

---

## 🚨 Git Safety Rules

**CRITICAL: NEVER destroy uncommitted changes**

**BEFORE running ANY destructive git command, you MUST:**

1. **Check for uncommitted changes:**
   ```bash
   git status
   ```

2. **If uncommitted changes exist, NEVER run:**
   - `git reset --hard` (destroys uncommitted changes)
   - `git checkout <branch>` without stashing first (may lose changes)
   - `git checkout -- <file>` (discards file changes)
   - `git clean` (deletes untracked files)
   - `git reset HEAD~` combined with checkout (loses commits and changes)
   - ANY command that would discard or lose uncommitted work

3. **If you need to switch context with uncommitted changes:**
   - **OPTION 1:** Commit the changes first
   - **OPTION 2:** Use `git stash` to save changes temporarily
   - **OPTION 3:** Ask user what to do with uncommitted changes

**Why this matters:**
- Uncommitted changes represent active work (often hours of effort)
- Once destroyed, changes are unrecoverable (not in git history)
- Historical failure: agents running `git reset --hard` destroyed in-progress features

**Safe git operations (always allowed):**
- `git status` (read-only)
- `git diff` (read-only)
- `git log` (read-only)
- `git add` (stages changes, non-destructive)
- `git commit` (saves changes, non-destructive)
- `git stash` (saves changes for later, non-destructive)

**Example of WRONG behavior:**
```bash
git status  # Shows uncommitted changes
git reset --hard origin/main  # ❌ DESTROYS uncommitted work
```

**Example of CORRECT behavior:**
```bash
git status  # Shows uncommitted changes
# Agent: "You have uncommitted changes. Should I commit them, stash them, or discard them?"
# Wait for user decision before proceeding
```

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

## Critical Rules Summary

### Always Required

✅ **Read guide before starting** (use Read tool for ENTIRE guide)
✅ **Use phase transition prompts** from `prompts_reference_v2.md`
✅ **Verify prerequisites** before proceeding
✅ **Update Agent Status** in README files at checkpoints
✅ **Validation Loop validation** (3 consecutive clean rounds, zero deferred issues)
✅ **100% unit test pass rate** before commits and transitions
✅ **Fix ALL issues immediately** (zero tech debt tolerance, includes Validation Loop issues)
✅ **User testing approval** before S10 begins (completed in S9.P3)

### Never Allowed

❌ **Skip stages** (all stages have dependencies)
❌ **Skip iterations** in S5 (all 22 mandatory)
❌ **Batch iterations** (execute ONE at a time, sequentially)
❌ **Defer issues for "later"** (fix immediately, includes Validation Loop issues)
❌ **Skip Validation Loop rounds** (must complete 3 consecutive clean rounds)
❌ **Exit Validation Loop early** (before 3 consecutive clean rounds)
❌ **Skip QC restart** when issues found (restart from beginning)
❌ **Commit without running tests**
❌ **Commit without user testing approval** (S10)

### Quality Gates

**🛑 MANDATORY GATES (cannot proceed without passing):**
- Gate 1: Research Completeness Audit (S2.P1.I1 - embedded in Validation Loop)
- Gate 2: Spec-to-Epic Alignment (S2.P1.I3 - embedded in Validation Loop)
- Gate 3: User Checklist Approval (S2.P1.I3)
- Gate 4.5: Epic Plan Approval (S3.P3 - 3-tier rejection)
- Gate 5: Implementation Plan Approval (S5.P3 - 3-tier rejection)
- Gate 23a: Pre-Implementation Spec Audit (S5.P3.I2 Round 3)
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
