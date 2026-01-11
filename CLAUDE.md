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

**Example prompts:** See `prompts_reference_v2.md` for phase transition examples

---

## Example Epic Conventions

Examples in this documentation use consistent epic names for clarity:
- **improve_draft_helper (KAI-1)** - Primary example (3 features, medium complexity)
- **add_player_validation (KAI-2)** - Secondary example (2 features, simple)
- **integrate_matchup_data (KAI-3)** - Tertiary example (4 features, complex)

**See:** `feature-updates/guides_v2/reference/example_epics.md` for complete example specifications

---

## Stage 1: When User Says "Help Me Develop {epic-name}"

**Trigger phrases:** "Help me develop...", "I want to plan...", "Let's work on..."

**Prerequisites:** User has created `feature-updates/{epic_name}.txt` with initial scratchwork notes.

**🚨 FIRST ACTION:** Use the "Starting Stage 1" prompt from `feature-updates/guides_v2/prompts_reference_v2.md`

**Workflow:**
1. READ: `stages/stage_1/epic_planning.md`
2. Assign KAI number from EPIC_TRACKER.md
3. Create git branch (see Git Branching Workflow below)
4. Analyze epic, propose feature breakdown (user confirms)
5. Create epic folder structure: `KAI-{N}-{epic_name}/` with `feature_XX_{name}/` folders
6. Create epic files: `EPIC_README.md`, `epic_smoke_test_plan.md`, `epic_lessons_learned.md`
7. Create feature files: `README.md`, `spec.md`, `checklist.md`, `lessons_learned.md`

**Next:** Stage 2 (Feature Deep Dives)

---

## Stage 2-4: Planning & Testing Strategy

**Stage 2: Feature Deep Dives** (Loop through ALL features - 4 mandatory gates per feature)

**🚨 CRITICAL CHANGE:** checklist.md is now QUESTION-ONLY format. Agents create QUESTIONS, user provides answers (Gate 2).

- **READ:** `stages/stage_2/feature_deep_dive.md` (router to sub-phases)
- **Sub-phases:**
  - Stage 2 Phase 0-1 (Research): Epic intent extraction, targeted research, research audit - Gate 1: Research Completeness Audit
  - Stage 2 Phase 2 (Specification): Spec with traceability, alignment check - Gate 2: Spec-to-Epic Alignment + **Gate 3: User Checklist Approval (NEW)**
  - Stage 2 Phase 3-6 (Refinement): Questions, scope, cross-feature alignment, user approval - Gate 4: User Approval of Acceptance Criteria

**Key Outputs:**
- `spec.md` with requirement traceability (every requirement has source: Epic/User Answer/Derived)
- `checklist.md` with QUESTIONS ONLY (agents cannot mark items resolved autonomously)
- **🚨 Gate 3 (User Checklist Approval - MANDATORY):** User answers ALL questions before Stage 5a
  - Agents present checklist.md to user using prompt from `prompts/stage_2_prompts.md`
  - User provides answers to ALL questions
  - Agent updates spec.md based on user answers
  - Cannot proceed to Stage 5a without user approval
  - See `mandatory_gates.md` Gate 3 for details

**Stage 2b.5: Specification Validation** (After each feature spec)
- **READ:** `stages/stage_2/phase_2b5_specification_validation.md`
- Assume everything in spec is wrong, validate with deep research
- Self-resolve checklist questions through additional codebase investigation
- Only leave genuine unknowns or multi-approach decisions for user
- Expected impact: 50-70% reduction in user questions

**Stage 3: Cross-Feature Sanity Check** (After ALL features planned)
- **READ:** `stages/stage_3/cross_feature_sanity_check.md`
- Systematic pairwise comparison of all feature specs
- Resolve conflicts and inconsistencies
- Get user sign-off on complete plan

**Stage 4: Epic Testing Strategy** (Update test plan + Gate 4.5: User approval)
- **READ:** `stages/stage_4/epic_testing_strategy.md`
- Update `epic_smoke_test_plan.md` based on deep dive findings
- Identify integration points between features
- Define epic success criteria
- **🚨 Gate 4.5 (MANDATORY):** User approves epic_smoke_test_plan.md before Stage 5a

**Next:** Stage 5 (Feature Implementation - first feature)

---

## Stage 5: Feature Implementation (Loop per feature: 5a→5b→5c→5d→5e)

**🚨 CRITICAL CHANGE:** Replaced todo.md (3,896 lines) with implementation_plan.md (~400 lines) + implementation_checklist.md (~50 lines) approach.

**Stage 5a: Implementation Planning** (28 total iterations across 3 rounds)

**Iteration Breakdown:**
- **Round 1:** 9 iterations (1-7 + 4a + 7a) - Initial analysis, requirements, dependencies, algorithms
- **Round 2:** 9 iterations (8-16) - Test strategy, edge cases, re-verification
- **Round 3:** 10 iterations (17-25) - Preparation (17-22), Gates 1-2 (23, 23a), Gate 3 + GO/NO-GO (25, 24)
- **Total:** 28 iterations with 5 mandatory gates (4a, 7a, 23a, 24, 25)

**Note:** Gates (4a, 7a, 23a) are verification checkpoints that occur as part of the iteration flow. The term "24 iterations" in some docs refers to base iterations excluding gate checkpoints, but guides count all steps as iterations for completeness.

**🚨 FIRST ACTION:** Use the "Starting Stage 5a Round 1" prompt from `prompts_reference_v2.md`

- **Round 1:** READ `stages/stage_5/round1_todo_creation.md` (Iterations 1-7 + **Gate 4a + Gate 7a**)
- **Round 2:** READ `stages/stage_5/round2_todo_creation.md` (Iterations 8-16, >90% test coverage required)
- **Round 3:** READ `stages/stage_5/round3_todo_creation.md` (Router to Part 1/Part 2a/Part 2b)
  - Part 1: Iterations 17-22 (Preparation)
  - Part 2a: Iterations 23, 23a (**Gate 23a: Integration + Spec Audit**)
  - Part 2b: Iterations 25, 24 (**Gate 25: Spec Validation** + **Gate 24: GO/NO-GO**)
- Create `implementation_plan.md` (grows from ~150→300→400 lines through 3 rounds)
- **🚨 Gate 5 (User Approval - MANDATORY):** Present implementation_plan.md to user for approval
  - User reviews complete implementation plan (~400 lines)
  - User must explicitly approve before Stage 5b begins
  - Agent uses prompt from `prompts/stage_5_prompts.md`
  - Cannot proceed to Stage 5b without user approval
  - See `mandatory_gates.md` Gate 5 for details

**Key Files:**
- `implementation_plan.md` = PRIMARY reference (~400 lines) - user-approved build guide
- `spec.md` = Context reference (requirements specification)
- `questions.md` = Created only if NEW questions arise during iterations

**Stage 5b: Implementation Execution**

**🚨 FIRST ACTION:** Use the "Starting Stage 5b" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_5/implementation_execution.md`
- Create `implementation_checklist.md` from implementation_plan.md tasks
- **Implement from implementation_plan.md (PRIMARY reference)**, spec.md (context/verification)
- Update implementation_checklist.md in real-time as tasks complete
- Mini-QC checkpoints every 5-7 tasks, 100% test pass required after each phase

**Key Principle:** implementation_plan.md tells you HOW to build (primary reference), spec.md tells you WHAT to build (verification)

**Stage 5c: Post-Implementation** (4 phases - smoke testing, QC rounds, final review, commit)

**🚨 FIRST ACTION:** Use the "Starting Stage 5c Smoke Testing" prompt from `prompts_reference_v2.md`

- **Phase 1:** READ `stages/stage_5/smoke_testing.md` - Import/Entry Point/E2E tests (MANDATORY GATE)
  - If issues found → Enter debugging protocol → LOOP BACK to Stage 5ca Part 1
- **Phase 2:** READ `stages/stage_5/qc_rounds.md` - 3 QC rounds
  - If ANY issues → Enter debugging protocol → LOOP BACK to Stage 5ca Part 1 (NOT mid-QC)
- **Phase 3:** READ `stages/stage_5/final_review.md` - PR review, lessons learned, zero tech debt tolerance
- **Phase 4:** **COMMIT FEATURE** - Commit source code changes for this feature only (feature-level commits)

**Stage 5d: Cross-Feature Spec Alignment** (After feature completes)

**🚨 FIRST ACTION:** Use the "Starting Stage 5d" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_5/post_feature_alignment.md`
- Update remaining feature specs based on completed feature implementation

**Stage 5e: Epic Testing Plan Reassessment** (After Stage 5d)

**🚨 FIRST ACTION:** Use the "Starting Stage 5e" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_5/post_feature_testing_update.md`
- Reassess epic_smoke_test_plan.md after each feature completion

**Repeat Stage 5 (5a→5b→5c→5d→5e) for EACH feature**

---

## Stage 6-7: Epic Finalization

**Stage 6: Epic-Level Final QC** (After ALL features complete - includes user testing)

**🚨 FIRST ACTION:** Use the "Starting Stage 6" prompt from `prompts_reference_v2.md`

- READ: `stages/stage_6/epic_final_qc.md`
- Execute epic_smoke_test_plan.md, 3 QC rounds, validate against epic request
- **🔴 USER TESTING (MANDATORY - Step 6):**
  - User tests complete system with real workflows
  - User reports findings: bugs or "no bugs found"
  - If bugs → Fix → Loop back to Stage 6a → Re-test
  - Proceed to Stage 7 only when user reports ZERO bugs
- If issues found → Enter debugging protocol → LOOP BACK to Stage 6a (Epic Smoke Testing)

**Stage 7: Epic Cleanup** (User testing ALREADY PASSED in Stage 6)

**🚨 FIRST ACTION:** Use the "Starting Stage 7" prompt from `prompts_reference_v2.md`

**Prerequisites:** Stage 6 complete (including user testing with ZERO bugs reported)

- READ: `stages/stage_7/epic_cleanup.md`
- Run unit tests (100% pass)
- **Stage 7.5 (MANDATORY):** Guide update from lessons learned
  - READ: `stages/stage_7/guide_update_workflow.md` for complete 9-step workflow
  - Analyze ALL lesson sources:
    - Epic and feature lessons_learned.md files
    - Debugging lessons from guide_update_recommendations.md (Phase 4b per-issue + Phase 5 patterns)
    - Debugging lessons from process_failure_analysis.md
  - Create GUIDE_UPDATE_PROPOSAL.md with prioritized proposals (P0-P3)
  - Debugging lessons automatically map to P0/P1 (higher priority than general lessons)
  - Present each proposal to user for individual approval
  - Apply only approved changes, create separate commit for guide updates
- Commit epic changes, create PR for user review, user merges
- Update EPIC_TRACKER.md after user merges, move epic to done/

**Note:** User testing completed in Stage 6 (Step 6) before Stage 7 begins

---

## Missed Requirement Protocol

If missing scope/requirements discovered at ANY point after first Stage 5 starts (and you KNOW the solution):

**🚨 FIRST ACTION:** Use the "Creating Missed Requirement" prompt from `prompts_reference_v2.md`

- **READ:** `missed_requirement/missed_requirement_protocol.md`
- **When to use:** Missing scope discovered at ANY time (implementation, QA, debugging, epic testing, user testing), solution is KNOWN
- **Before Stage 5:** Just update specs directly during Stage 2/3/4
- **Two options:** Create new `feature_{XX}_{name}/` folder OR update unstarted feature
- **User decides:** Which approach + priority (high/medium/low)
- **Pause current work** → Return to planning stages
- **Stage 2** (Deep Dive): Flesh out new/updated feature spec
- **Stage 3** (Sanity Check): Re-align ALL features (not just new one)
- **Stage 4** (Test Strategy): Update epic_smoke_test_plan.md
- **Resume paused work** → Implement new/updated feature when its turn comes in sequence
- **Full Stage 5** (5a → 5b → 5c → 5d → 5e) when feature gets implemented
- **Priority determines sequence:** high = before current, medium = after current, low = at end
- **Special case:** If discovered during Stage 6/7 → Complete all features → **RESTART epic testing from Stage 6a**

---

## 🔀 Decision Tree: Which Protocol to Use?

**When you discover an issue or gap, follow this decision tree:**

```
Issue/Gap Discovered
│
├─ Question 1: Do you know the SOLUTION?
│  │
│  ├─ YES → Is it a NEW requirement the user didn't ask for?
│  │  │
│  │  ├─ YES → MISSED REQUIREMENT PROTOCOL
│  │  │  Example: "We need to add email validation"
│  │  │  → Create feature_{XX}_{name}/ folder
│  │  │  → User decides priority
│  │  │  → Return to Stage 2 for planning
│  │  │
│  │  └─ NO → Just implement it (regular work)
│  │     Example: "Refactor this method"
│  │     → Not a missing requirement, just implementation detail
│  │
│  └─ NO → Requires investigation?
│     │
│     ├─ YES → DEBUGGING PROTOCOL
│     │  Example: "Player scores are incorrect but we don't know why"
│     │  → Create debugging/ISSUES_CHECKLIST.md
│     │  → Investigation rounds (Phase 2)
│     │  → Root cause analysis (Phase 4b)
│     │
│     └─ NO → Ask user for clarification
│        Example: "Should we handle this edge case?"
│        → Add to questions.md
│        → Wait for user answer
```

### Protocol Selection Examples

**Scenario 1: Empty Player Name Bug**

**Discovery:** During QC testing, system crashes when player name is empty

**Analysis:**
- Do we know the solution? → NO (need to investigate why it crashes)
- Requires investigation? → YES

**Decision:** ✅ DEBUGGING PROTOCOL
- Root cause unknown (could be validation missing, could be null pointer, could be data structure issue)
- Need investigation rounds to find root cause
- Phase 4b will identify which stage should have caught this

---

**Scenario 2: Forgot Email Validation**

**Discovery:** During implementation, realize spec didn't include email validation

**Analysis:**
- Do we know the solution? → YES (add email regex validation)
- Is it a NEW requirement? → YES (not in original spec)

**Decision:** ✅ MISSED REQUIREMENT PROTOCOL
- Solution is known (email validation)
- User didn't ask for it originally
- Need user to confirm this requirement
- Return to Stage 2 to plan properly

---

**Scenario 3: Refactor Long Method**

**Discovery:** During implementation, notice method is 200 lines long

**Analysis:**
- Do we know the solution? → YES (break into smaller methods)
- Is it a NEW requirement? → NO (implementation detail)

**Decision:** ✅ Just implement it (regular work)
- Not a missing requirement (just code quality)
- Not a bug requiring investigation
- Part of normal implementation process

---

**Scenario 4: Unclear Edge Case**

**Discovery:** During planning, unsure if we should handle negative ADP values

**Analysis:**
- Do we know the solution? → NO (need user input)
- Requires investigation? → NO (need clarification)

**Decision:** ✅ Add to questions.md, ask user
- Not a bug (hasn't been implemented yet)
- Not a missing requirement (unclear if it should exist)
- Need user decision before proceeding

---

## Debugging Protocol

**INTEGRATED WITH QC/SMOKE TESTING** - When issues discovered with UNKNOWN root cause:

**🚨 FIRST ACTION:** Use the "Starting Debugging Protocol" prompt from `prompts_reference_v2.md`

- **READ:** `debugging/debugging_protocol.md`
- **When to use:** Issues discovered during QC/Smoke testing with unknown root cause requiring investigation

**File Structure:**
- Feature-level issues: `feature_XX_{name}/debugging/` folder
- Epic-level issues: `KAI-{N}-{epic_name}/debugging/` folder
- Contains: ISSUES_CHECKLIST.md, issue_XX_{name}.md files, investigation_rounds.md, code_changes.md, process_failure_analysis.md (Phase 5 cross-pattern), guide_update_recommendations.md (Phase 4b per-issue + Phase 5 patterns), lessons_learned.md (Phase 5)

**Workflow Integration:**
1. **Issue Discovery** - During Smoke Testing (Stage 5ca/6a) or QC Rounds (Stage 5cb/6b), add issues to ISSUES_CHECKLIST.md
2. **Enter Debugging Protocol** - Work through checklist systematically (Phase 1-3: investigate and fix)
3. **User Verification** - User confirms each fix (Phase 4)
4. **🚨 CRITICAL: Per-Issue Root Cause Analysis (Phase 4b - MANDATORY)**
   - **TIMING:** IMMEDIATELY after each issue's user verification (NOT batched)
   - **WHY:** Captures lessons while investigation context is fresh (3x higher quality than delayed analysis)
   - **WHAT:** 5-why analysis → identify prevention point → draft guide improvement
   - **OUTPUT:** guide_update_recommendations.md per-issue entry
   - **DURATION:** 10-20 minutes per issue
   - **DO NOT proceed to next issue without completing Phase 4b for current issue**
5. **Cross-Pattern Analysis (Phase 5)** - After ALL issues resolved, identify patterns across bugs and generate systemic guide updates
6. **Loop Back to Testing** - RESTART testing from beginning (not mid-testing)
7. **Zero Issues Required** - Cannot proceed to next stage with any open issues

**6-Phase Process:**
- Phase 1: Issue Discovery & Checklist Update
- Phase 2: Investigation (Round 1 → Code Tracing, Round 2 → Hypothesis, Round 3 → Testing)
- Phase 3: Solution Design & Implementation
- Phase 4: User Verification (MANDATORY - user must confirm each fix)
- Phase 4b: Root Cause Analysis (MANDATORY - per-issue, 5-why analysis, guide improvements while context fresh)
- Phase 5: Loop Back to Testing (includes cross-bug pattern analysis and lessons learned)

**Key Requirements:**
- **Issue-centric tracking:** Each issue has dedicated file with investigation history
- **Max 5 investigation rounds** per issue before user escalation
- **Feature vs Epic separation:** Feature bugs vs epic integration bugs tracked separately
- **User testing integration:** Stage 7 user-reported bugs → epic checklist → loop back to Stage 6 (NOT Stage 7)
- **Resumability:** investigation_rounds.md preserves state across session compaction

---

## Key Principles

- **Epic-first thinking**: Top-level work unit is an epic (collection of features)
- **Mandatory reading protocol**: ALWAYS read guide before starting stage
- **Phase transition prompts**: MANDATORY acknowledgment (proves guide was read)
- **User approval gates**: Three early approval gates (Gate 3: checklist after Stage 2, Gate 4.5: epic test plan after Stage 4, Gate 5: implementation plan after Stage 5a)
- **Zero autonomous resolution**: Agents create QUESTIONS, user provides ANSWERS (no assumptions)
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

## Gate Numbering System

### Understanding Gate Numbers

The workflow uses two types of gates:

**Type 1: Stage-Level Gates (whole numbers or decimals)**
- Named after the stage they occur in or between
- Most require user approval
- Examples: Gate 3 (Stage 2), Gate 4.5 (between Stage 4-5), Gate 5 (Stage 5a)
- **Naming logic:** "Gate 5" = "Stage 5 approval gate", "Gate 4.5" = "Between Stage 4 and 5"

**Type 2: Iteration-Level Gates (iteration numbers)**
- Named after the iteration they occur in
- Agent self-validates (using checklists)
- Examples: Gate 4a (Iteration 4a), Gate 23a (Iteration 23a), Gate 24 (Iteration 24)
- **Naming logic:** Uses actual iteration number from Stage 5a

### Complete Gate List

| Gate | Type | Stage | Purpose | Approver |
|------|------|-------|---------|----------|
| Gate 3 | Stage | Stage 2 | User Checklist Approval | User |
| Gate 4.5 | Stage | Stage 4 | Epic Test Plan Approval | User |
| Gate 5 | Stage | Stage 5a | Implementation Plan Approval | User |
| Gate 4a | Iteration | Stage 5a R1 | TODO Specification Audit | Agent (checklist) |
| Gate 7a | Iteration | Stage 5a R1 | Backward Compatibility Check | Agent (checklist) |
| Gate 23a | Iteration | Stage 5a R3 | Pre-Implementation Spec Audit (4 parts) | Agent (checklist) |
| Gate 24 | Iteration | Stage 5a R3 | GO/NO-GO Decision | Agent (confidence check) |
| Gate 25 | Iteration | Stage 5a R3 | Spec Validation Check | Agent (checklist) |

### Why This Numbering?

**Stage gates use whole/decimal numbers:**
- Easier to remember major checkpoints
- "Gate 5" = "Stage 5 approval gate"
- Decimal (4.5) when gate falls between stages

**Iteration gates use iteration numbers:**
- "Gate 4a" = "Gate at Iteration 4a"
- "Gate 23a" = "Gate at Iteration 23a"
- Matches actual iteration naming in guides

**Benefits:**
- Clear distinction between user gates (3, 4.5, 5) and agent gates (4a, 7a, 23a, 24, 25)
- Iteration gates are self-explanatory (matches iteration number)
- Stage gates align with workflow stages

**See:** `reference/mandatory_gates.md` for complete gate reference card with timing, checklists, and guide locations.

---

## Feature File Structure (Critical for Resuming Work)

**🚨 BEFORE READING THIS SECTION:**

If you're working with an epic that was started **before 2026-01-10**, be aware of critical file changes that affect resumption:

### 🚨 Critical File Changes (2026-01-10)

**⚠️ IMPORTANT FOR RESUMING OLD EPICS:**

```
┌─────────────────────────────────────────────────────────────────┐
│ 🚨 CRITICAL: RESUMING OLD EPICS (Before 2026-01-10)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ If you see `todo.md` in a feature folder:                       │
│                                                                  │
│ 1. Epic was started BEFORE file structure change               │
│ 2. Use todo.md as reference (don't update it)                  │
│ 3. Don't expect new files (implementation_plan.md, etc.)       │
│ 4. Follow old workflow patterns from README.md Agent Status    │
│                                                                  │
│ If you see `implementation_plan.md`:                            │
│                                                                  │
│ 1. Epic uses NEW workflow (after 2026-01-10)                   │
│ 2. Use implementation_plan.md as PRIMARY reference             │
│ 3. Follow new workflow as documented in current guides         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**How to quickly identify epic age:**
```bash
ls feature-updates/{epic_name}/feature_01_*/
# If you see: todo.md → Old epic (before 2026-01-10)
# If you see: implementation_plan.md → New epic (after 2026-01-10)
```

**Replaced:**
- ❌ `todo.md` (3,896 lines) - DELETED, no longer used

**New Files:**
- ✅ `implementation_plan.md` (~400 lines) - PRIMARY reference during Stage 5b
  - Created: Stage 5a (grows through 24 iterations)
  - Purpose: User-approved implementation build guide
  - Contains: Implementation tasks, dependencies, test strategy, phasing, performance
  - User approval: MANDATORY before Stage 5b (Gate 5)

- ✅ `implementation_checklist.md` (~50 lines) - Progress tracker
  - Created: Stage 5b (extracted from implementation_plan.md)
  - Purpose: Real-time progress tracking during implementation
  - Format: Simple checkboxes linking spec requirements → implementation tasks

- ✅ `questions.md` (optional) - Only if NEW questions arise during Stage 5a iterations
  - Created: Stage 5a (if needed)
  - Purpose: NEW questions discovered during 24 verification iterations
  - Note: Most questions should be in checklist.md (answered during Stage 2)

**Changed Files:**
- ✅ `checklist.md` - NOW QUESTION-ONLY FORMAT
  - Created: Stage 1
  - Updated: Stage 2 (agents add QUESTIONS, not decisions)
  - **🚨 CRITICAL:** Agents CANNOT mark items `[x]` autonomously
  - User approval: MANDATORY before Stage 5a (Gate 3)
  - Format: Each question has Context + User Answer (blank) + Impact on spec.md
  - After user answers: Agent updates spec.md, marks items `[x]`

**File Roles Summary:**
- `spec.md` = WHAT to build (requirements) - user-approved Stage 2
- `checklist.md` = QUESTIONS to answer (user input) - user-approved Stage 2 (Gate 3)
- `implementation_plan.md` = HOW to build (implementation guide) - user-approved Stage 5a (Gate 5)
- `implementation_checklist.md` = PROGRESS tracker (real-time updates) - created Stage 5b
- `code_changes.md` = ACTUAL changes (what was done) - updated Stage 5b

**Why This Matters for Resuming:**
- Old epics: Use todo.md as reference, don't expect new files
- New epics: Use implementation_plan.md as PRIMARY reference
- File structure tells you which workflow version was used

---

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

---

## Resuming In-Progress Epic Work

**🚨 FIRST: Check epic age** - See "Feature File Structure → Critical File Changes" section above to understand if this is an old epic (before 2026-01-10) or new epic.

**Quick check:**
```bash
ls feature-updates/{epic_name}/feature_01_*/
# If you see: todo.md → Old epic
# If you see: implementation_plan.md → New epic
```

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

**During epic work (Stages 1-6):**
- All work happens on the epic branch
- Commits use format: `{commit_type}/KAI-{number}: {message}`
  - `commit_type` is either `feat` or `fix` (NOT `epic`)
  - `feat` - Feature-related commits
  - `fix` - Bug fix commits
- Commit at normal times (currently Stage 7 Step 6)

**When completing an epic (Stage 7):**

1. **Commit changes on branch** (after user testing passes)

2. **Push branch to remote:**
   ```bash
   git push origin {work_type}/KAI-{number}
   ```

3. **Create Pull Request for user review:**
   ```bash
   gh pr create --base main --head {work_type}/KAI-{number} \
     --title "{commit_type}/KAI-{number}: Complete {epic_name} epic" \
     --body "{Epic summary with features, tests, review instructions}"
   ```

4. **User reviews and merges PR:**
   - User reviews PR in GitHub UI, VS Code extension, or CLI
   - User approves and merges when satisfied
   - See `feature-updates/USER_PR_REVIEW_GUIDE.md` for review options

5. **Update EPIC_TRACKER.md** (after user merges PR):
   - Pull latest from main: `git checkout main && git pull origin main`
   - Move epic from "Active" to "Completed" table
   - Add epic detail section with commits
   - Increment "Next Available Number"
   - Commit and push EPIC_TRACKER.md update

6. **Delete branch (optional):**
   ```bash
   git branch -d {work_type}/KAI-{number}
   ```

### Branch Naming Convention

**Format:** `{work_type}/KAI-{number}` (epic/feat/fix tracked in EPIC_TRACKER.md)
**Examples:** `epic/KAI-1`, `feat/KAI-2`, `fix/KAI-3`

### Epic Folder Naming Convention

**Format:** `feature-updates/KAI-{N}-{epic_name}/`
**Examples:**
- `feature-updates/KAI-1-improve_draft_helper/`
- `feature-updates/KAI-3-integrate_new_player_data_into_simulation/`

**Original Request File:** `feature-updates/{epic_name}.txt` (no KAI number)
**Why include KAI number:** Ensures unique folder names, matches branch naming, enables quick identification

### Commit Message Convention

**Format:** `{commit_type}/KAI-{number}: {message}` (feat or fix)
**Example:** `feat/KAI-1: Add ADP integration to PlayerManager`
**Rules:** Brief (100 chars), no emojis, imperative mood, all features in epic use same KAI number

### EPIC_TRACKER.md Management

**Location:** `feature-updates/EPIC_TRACKER.md`
**Updates:** Stage 1 (add to Active table), Stage 7 (move to Completed, add details), after commits (track for docs)

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

### STEP 2: If Tests Pass, Review ALL Changes

**⚠️ CRITICAL: Include ALL modified source code files**
```bash
git status  # Check ALL modified files
git diff    # Review changes
```

**Common mistake:** Missing test files that were updated to use new interfaces

**Verify all source files are included:**
- [ ] Main source files (*.py in league_helper/, simulation/, etc.)
- [ ] ALL test files that were modified (tests/**/*.py)
- [ ] Configuration files if modified (data/*.json, data/*.csv)

### STEP 3: Stage and Commit Changes

1. Analyze all changes with `git status` and `git diff`
2. **Verify ALL modified source files are included** (main code AND test files)
3. Update documentation if functionality changed
4. Stage and commit with clear, concise message
5. Follow commit standards:
   - Format: `{commit_type}/KAI-{number}: {message}`
   - Brief, descriptive messages (100 chars or less)
   - No emojis or subjective prefixes
   - commit_type is `feat` or `fix`
   - List major changes in body

### STEP 4: If Tests Fail

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
✅ **User testing approval** before Stage 7 begins (completed in Stage 6)

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

**See:** `feature-updates/guides_v2/reference/common_mistakes.md` for comprehensive anti-pattern reference across all stages

---

## Additional Resources

**Primary references:**
- **EPIC_WORKFLOW_USAGE.md**: Comprehensive usage guide with setup, patterns, FAQs
- **prompts_reference_v2.md**: All phase transition prompts (MANDATORY)
- **templates_v2.md**: File templates for epic, feature, and bug fix folders
- **README.md**: Guide index and quick reference
- **PLAN.md**: Complete workflow specification

---

**Remember:** This workflow exists to ensure quality, completeness, and maintainability. Follow it rigorously, learn from each epic, and continuously improve the guides based on lessons learned.

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
- `feature-updates/` - Epic-driven development (see CLAUDE_EPICS.md)

**See:** `ARCHITECTURE.md` for complete architectural details, `README.md` for installation/usage.

---

## Coding Standards & Conventions

### Import Organization
```python
# Standard library (alphabetical)
import csv, json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party (alphabetical)
import pandas as pd

# Local with sys.path manipulation
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger
```

**Rules:** Use `Path` for file operations, `sys.path.append()` for relative imports, type hints required

### Error Handling
```python
from utils.error_handler import error_context, DataProcessingError

# Use context managers for error tracking
with error_context("operation_name", component="module_name") as ctx:
    if error_condition:
        raise DataProcessingError("Error message", context=ctx)
```

### Logging Standards
```python
from utils.LoggingManager import setup_logger, get_logger

logger = setup_logger(name="module", level="INFO")  # Setup once
logger = get_logger()  # Use in modules

# Levels: debug, info, warning, error (with exc_info=True)
```

### Docstring Format (Google Style)
```python
def method_name(self, param1: Type, param2: Optional[Type] = None) -> ReturnType:
    """Brief one-line description.

    Args:
        param1 (Type): Description
        param2 (Optional[Type]): Description with default

    Returns:
        ReturnType: Description of return value
    """
```

### Type Hinting
```python
from typing import Dict, List, Optional, Union
from pathlib import Path

def process_data(filepath: Union[str, Path],
                 options: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    pass
```

### CSV Operations
```python
from utils.csv_utils import read_csv_with_validation, write_csv_with_backup

df = read_csv_with_validation(filepath, required_columns=['id', 'name'])
write_csv_with_backup(df, filepath, create_backup=True)
```

### Configuration Access
```python
from util.ConfigManager import ConfigManager

config = ConfigManager(data_folder)
multiplier, rating = config.get_adp_multiplier(adp_val)
```

### Naming Conventions
- **Classes**: `PascalCase` (PlayerManager, ConfigManager)
- **Functions/Methods**: `snake_case` (load_players, get_score)
- **Constants**: `UPPER_SNAKE_CASE` (RECOMMENDATION_COUNT, LOGGING_LEVEL)
- **Private**: `_leading_underscore` (_validate_config)
- **Modules**: `snake_case` (error_handler.py, csv_utils.py)

### Path Handling
```python
from pathlib import Path

base_path = Path(__file__).parent
config_file = base_path / "data" / "league_config.json"
with open(str(config_file), 'r') as f:  # Convert to string when needed
    pass
```

### Testing Standards

**Test Suite:** 2,200+ tests (100% pass rate required before commits)
- **Unit Tests:** Test individual functions/classes in isolation, mock dependencies
- **Integration Tests:** Test cross-module workflows (25 tests)

**Test Execution:**
```bash
# Run all tests (REQUIRED before commits)
python tests/run_all_tests.py

# Run specific file/class
python -m pytest tests/path/test_file.py::TestClass -v
```

**Requirements:**
- Test file structure mirrors source code
- Use pytest fixtures for reusable test data
- Mock external dependencies (files, APIs, datetime)
- AAA pattern (Arrange, Act, Assert)
- Tests must be independent (no shared state)

**See:** `tests/README.md` for complete testing guidelines and examples.
