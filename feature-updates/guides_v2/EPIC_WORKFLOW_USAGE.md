# Epic-Driven Development Workflow - Usage Guide

**Version:** 2.0
**Last Updated:** 2025-12-31
**Purpose:** Comprehensive guide for agents using the Epic-Driven Development Workflow v2

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [File Structure](#file-structure)
4. [Workflow Stages](#workflow-stages)
5. [Critical Protocols](#critical-protocols)
6. [Phase Transition Protocol](#phase-transition-protocol)
7. [Using the Guides](#using-the-guides)
8. [Key Principles](#key-principles)
9. [Setting Up in a New Project](#setting-up-in-a-new-project)
10. [Appendix Reference](#appendix-reference)

---

## Overview

### What is the Epic-Driven Development Workflow?

The Epic-Driven Development Workflow v2 is a **10-stage process** for managing complex software development projects. It breaks large initiatives (epics) into focused features with rigorous planning, implementation, and quality control at each stage.

**Core Philosophy:**
- Plan thoroughly before implementing
- Verify continuously during implementation
- Validate rigorously after implementation
- Learn and improve from every epic

**Key Benefits:**
- Reduces implementation errors by 80%+
- Ensures complete documentation
- Catches integration issues early
- Builds institutional knowledge through lessons learned
- Scales from small bug fixes to large feature initiatives

### Workflow at a Glance

```text
Epic Request (user creates .txt file)
    ↓
S1: Epic Planning (break into features)
    ↓
S2: Feature Deep Dives (flesh out each feature)
    ↓
S3: Cross-Feature Sanity Check (resolve conflicts)
    ↓
S4: Epic Testing Strategy (define how to test)
    ↓
S5: Feature Implementation (implement each feature: S5→S6→S7→S8)
    ↓
S9: Epic-Level Final QC (validate epic as whole)
    ↓
S10: Epic Cleanup (commit, archive, apply lessons)
```

### Terminology

- **Epic**: Top-level work unit (collection of related features)
- **Feature**: Individual component within an epic
- **Stage**: Major phase of the workflow (S1-S10)
- **Round**: Sub-phase within a stage (e.g., S5 has 3 rounds)
- **Iteration**: Specific verification step within a round (e.g., 22 iterations in S5)
- **Phase**: Sub-section within a stage (e.g., S7 has 3 phases)

---

## Quick Start

### For a New Epic

**When user says:** "Help me develop {epic-name}" or "I want to plan {feature-name}"

**Your immediate actions:**

1. **Check for in-progress epics first:**
   ```bash
   ls feature-updates/
   ```
   Look for any folders that aren't `done/` or `guides_v2/`

2. **If in-progress epic found:**
   - Read its `EPIC_README.md` "Agent Status" section
   - Use "Resuming In-Progress Epic" prompt from `prompts_reference_v2.md`
   - Continue from where previous agent left off

3. **If no in-progress epic:**
   - Verify user created `feature-updates/{epic_name}.txt` with initial notes
   - Use "Starting S1" prompt from `prompts_reference_v2.md`
   - Read `stages/s1/s1_epic_planning.md`
   - Begin S1 workflow

### For Resuming Work

**When you start a conversation and see an epic in progress:**

1. **Find the epic folder:**
   ```bash
   ls feature-updates/
   # Look for folders like: improve_draft_helper/, bug_fix_player_data/
   ```

2. **Read EPIC_README.md Agent Status:**
   ```markdown
   ## Agent Status

   **Last Updated:** 2025-12-30 14:30
   **Current Stage:** S6 - Implementation Execution
   **Current Step:** Implementing Feature 2, component 3 of 5
   **Current Guide:** stages/s6/s6_execution.md
   **Next Action:** Complete PlayerManager.calculate_score() method
   ```

3. **Use the resumption prompt:**
   - From `prompts_reference_v2.md`: "Resuming In-Progress Epic"
   - Read the current guide listed in Agent Status
   - Continue from the next action listed

---

## File Structure

### Project Root Structure

```markdown
project-root/
├── feature-updates/               # Epic workspace root
│   ├── {epic_name}.txt           # Original user request (stays here)
│   ├── {epic_name}/              # Epic folder (moved to done/ when complete)
│   ├── done/                     # Completed epics archive
│   │   └── {completed_epic}/
│   └── guides_v2/                # Workflow guides (this folder)
│       ├── EPIC_WORKFLOW_USAGE.md      # This file
│       ├── prompts_reference_v2.md     # Mandatory phase transition prompts
│       ├── templates/             # File templates
│       ├── README.md                   # Guide index
│       ├── PLAN.md                     # Complete workflow spec
│       ├── stages/s1/s1_epic_planning.md
│       ├── stages/s2/s2_feature_deep_dive.md
│       ├── ... (16 stage guides total)
│       └── stages/s10/s10_epic_cleanup.md
└── [your project files]
```

### Epic Folder Structure

```markdown
feature-updates/KAI-{N}-{epic_name}/
├── EPIC_README.md                    # Master tracking (Quick Reference, Agent Status, Progress)
├── epic_smoke_test_plan.md           # How to test complete epic (evolves)
├── epic_lessons_learned.md           # Cross-feature insights and guide improvements
├── feature_01_{name}/                # Feature 1
│   ├── README.md                     # Feature context and Agent Status
│   ├── spec.md                       # PRIMARY SPECIFICATION (detailed requirements)
│   ├── checklist.md                  # Resolved vs pending decisions
│   ├── implementation_plan.md        # Implementation build guide (~400 lines, S5, user-approved)
│   ├── questions.md                  # Questions for user (created S5 if needed)
│   ├── implementation_checklist.md   # Progress tracking (~50 lines, S6)
│   ├── lessons_learned.md            # Feature-specific insights
│   └── research/                     # Research documents (if needed)
├── feature_02_{name}/                # Feature 2 (same structure)
├── feature_03_{name}/                # Feature 3 (same structure)
└── bugfix_{priority}_{name}/         # Bug fix folder (if bugs found)
    ├── notes.txt                     # Issue description (user-verified)
    ├── spec.md                       # Fix requirements
    ├── checklist.md                  # Same as features
    ├── implementation_plan.md        # Same as features (~400 lines, user-approved)
    ├── implementation_checklist.md   # Same as features (~50 lines, progress tracking)
    └── lessons_learned.md            # Same as features
```

### Key Files Explained

**Epic-Level Files:**

- **EPIC_README.md**: Master control document
  - Quick Reference Card (workflow diagram, critical rules)
  - Agent Status (current stage, next action, critical rules)
  - Epic Progress Tracker (table showing all features/stages)
  - Feature Summary (descriptions, dependencies)
  - Epic Completion Summary (added at end)

- **epic_smoke_test_plan.md**: Testing strategy for complete epic
  - Created in S1 (initial version)
  - Updated in S4 (after deep dives)
  - Updated in S8.P2 (after each feature implementation)
  - Used in S9 (final epic validation)

- **epic_lessons_learned.md**: Cross-feature patterns
  - Insights from each stage
  - Guide improvements identified
  - Recommendations for future epics

**Feature-Level Files:**

- **README.md**: Feature context and resumption info
  - Feature overview, dependencies
  - Agent Status (current phase, progress, next action)

- **spec.md**: PRIMARY SPECIFICATION (most important file)
  - Detailed requirements
  - Acceptance criteria
  - Edge cases
  - Implementation notes

- **checklist.md**: Decision tracking
  - Open questions (need user input)
  - Resolved questions (decisions made)

- **implementation_plan.md**: Implementation build guide (created in S5, ~400 lines)
  - All implementation tasks with acceptance criteria
  - Component dependencies matrix
  - Algorithm traceability matrix
  - Test strategy and edge cases
  - Implementation phasing (5-6 checkpoints)
  - Performance considerations
  - Mock audit results
  - User-approved before S6 begins

- **implementation_checklist.md**: Progress tracking (created in S6, ~50 lines)
  - Simple checkbox format for tracking progress
  - References implementation_plan.md for details
  - Lightweight continuous verification

- **lessons_learned.md**: Feature-specific insights
  - What went well
  - What could improve
  - Guide improvements needed

---

## Workflow Stages

### S1: Epic Planning

**Purpose:** Break epic into features, create folder structure

**Inputs:** User's `{epic_name}.txt` file

**Outputs:**
- Epic folder with all epic-level files
- Feature folders (empty except README, spec, checklist, lessons_learned)
- Initial `epic_smoke_test_plan.md`

**Guide:** `stages/s1/s1_epic_planning.md`

**Key Activities:**
- Analyze epic request
- Propose feature breakdown (get user approval)
- Create epic and feature folders
- Create initial documentation

**Next:** S2

---

### S2: Feature Deep Dives

**Purpose:** Flesh out detailed requirements for each feature

**Inputs:** Feature folders from S1

**Outputs:**
- Complete `spec.md` for each feature
- Resolved `checklist.md` items
- Updated feature README.md

**Guide:** `stages/s2/s2_feature_deep_dive.md`

**Key Activities:**
- Deep dive into each feature (one at a time)
- Interactive question resolution (ONE question at a time)
- Write detailed spec.md
- Compare to already-completed features for alignment
- Dynamic scope adjustment (split if >35 checklist items)

**Critical Rule:** Complete ALL features before moving to S3

**Next:** S3

---

### S3: Cross-Feature Sanity Check

**Purpose:** Resolve conflicts and ensure features work together

**Inputs:** All completed feature specs

**Outputs:**
- Verified specs with no conflicts
- User sign-off on complete plan

**Guide:** `stages/s3/s3_cross_feature_sanity_check.md`

**Key Activities:**
- Systematic pairwise comparison of all features
- Identify conflicts, overlaps, gaps
- Resolve inconsistencies
- Get user approval

**Critical Rule:** Get explicit user sign-off before S4

**Next:** S4

---

### S4: Epic Testing Strategy

**Purpose:** Define how to test the complete epic

**Inputs:** All verified feature specs

**Outputs:**
- Updated `epic_smoke_test_plan.md`
- Integration points identified
- Epic success criteria defined

**Guide:** `stages/s4/s4_epic_testing_strategy.md`

**Key Activities:**
- Update test plan based on deep dive findings
- Identify integration points between features
- Define epic success criteria
- Plan cross-feature test scenarios

**Next:** S5 (first feature)

---

### S5: Feature Implementation

**Purpose:** Implement one feature at a time with rigorous QC

**Inputs:** Feature spec.md, checklist.md

**Outputs:**
- Implemented and tested feature
- All S5 artifacts (implementation_plan, implementation_checklist, code_changes)
- Verified integration with existing features

**Stages:** S5 → S6 → S7 → S8 (for EACH feature)

#### S5: Implementation Planning (22 verification iterations across 3 rounds)

**Guide:** 5 guides (Round 1, 2, 3 split into 3 parts)
- `stages/s5/s5_p1_planning_round1.md` (iterations 1-7 + 4a)
- `stages/s5/s5_p2_planning_round2.md` (iterations 8-13)
- `stages/s5/s5_p3_planning_round3.md` (Round 3 Part 1: iterations 14-19)
- `stages/s5/s5_p3_i2_gates_part1.md` (Round 3 Part 2a: iterations 20, 23a)
- `stages/s5/s5_p3_i3_gates_part2.md` (Round 3 Part 2b: iterations 21-22, 25, 24)

**Key Activities:**
- Round 1: Initial analysis (7 iterations + mandatory 4a gate)
  - Iteration 4: Algorithm Traceability Matrix
  - Iteration 4a: Implementation Plan Specification Audit (MANDATORY GATE)
  - Iteration 7: Integration Gap Check
- Round 2: Deep verification (6 iterations)
  - Iteration 11: Algorithm Traceability Matrix (re-verify)
  - Iteration 14: Integration Gap Check (re-verify)
  - Iteration 15: Test Coverage Depth Check (>90%)
- Round 3: Final readiness (9 iterations split into 2 parts + 3 mandatory gates)
  - Iteration 19: Algorithm Traceability Matrix (final)
  - Iteration 21: Mock Audit & Integration Test Plan
  - Iteration 19: Integration Gap Check (final)
  - Iteration 20: Pre-Implementation Spec Audit (4 MANDATORY PARTS)
  - Iteration 22: GO/NO-GO decision

**Outputs:** `implementation_plan.md` (~400 lines), `questions.md` (if needed)

**User Approval:** **MANDATORY CHECKPOINT** - User must approve implementation_plan.md before S6

**Critical Rule:** ALL 22 iterations are mandatory, cannot skip

#### S6: Implementation Execution

**Guide:** `stages/s6/s6_execution.md`

**Key Activities:**
- Create `implementation_checklist.md` (~50 lines) from implementation_plan.md tasks
- Keep spec.md VISIBLE at all times
- Use implementation_plan.md as PRIMARY reference (spec.md provides context)
- Follow implementation phasing from implementation_plan.md (5-6 checkpoints)
- Continuous progress tracking via `implementation_checklist.md`
- Mini-QC checkpoints after each major component
- Run unit tests after each step (100% pass required)

**Outputs:** Implemented code, `implementation_checklist.md`

**Critical Rule:** 100% unit test pass rate at all times

#### S7: Post-Implementation (3 phases)

**Guides:** 3 guides (Smoke Testing, QC Rounds, Final Review)
- `stages/s7/s7_p1_smoke_testing.md`
- `stages/s7/s7_p2_qc_rounds.md`
- `stages/s7/s7_p3_final_review.md`

**Step 1 - Smoke Testing:**
- Part 1: Import Test (module loads)
- Part 2: Entry Point Test (script starts)
- Part 3: E2E Execution Test (verify OUTPUT DATA VALUES)
- MANDATORY GATE before QC rounds

**Step 2 - QC Rounds:**
- QC Round 1: Basic validation (<3 critical issues, >80% requirements)
- QC Round 2: Deep verification (all Round 1 resolved + zero new critical)
- QC Round 3: Final skeptical review (ZERO tolerance)
- **QC Restart Protocol:** If ANY issues → RESTART from smoke testing

**Step 3 - Final Review:**
- PR Review Checklist (11 categories - all mandatory)
- Lessons learned capture with IMMEDIATE guide updates
- Final verification (100% completion required)

**Critical Rule:** Zero tech debt tolerance - fix ALL issues immediately

#### S8.P1: Cross-Feature Spec Alignment

**Guide:** `stages/s8/s8_p1_cross_feature_alignment.md`

**Key Activities:**
- Review ALL remaining (unimplemented) feature specs
- Compare specs to ACTUAL implementation (not just plan)
- Update specs based on real insights
- Prevent spec drift

**Why:** Implementation reveals reality that planning couldn't predict

#### S8.P2: Epic Testing Plan Reassessment

**Guide:** `stages/s8/s8_p2_epic_testing_update.md`

**Key Activities:**
- Reassess `epic_smoke_test_plan.md`
- Update test scenarios based on actual implementation
- Add newly discovered integration points
- Keep testing plan current

**Why:** Test plan must reflect reality, not original assumptions

**After S8.P2:** Repeat S5 (S5→S6→S7→S8) for NEXT feature

---

### S9: Epic-Level Final QC

**Purpose:** Validate epic as a whole (all features integrated)

**Inputs:** All features complete (S8.P2 done for all)

**Outputs:**
- Validated epic (all tests passed)
- Epic-level lessons learned
- Epic completion verification

**Guide:** `stages/s9/s9_p1_epic_smoke_testing.md` (start here, then phases 2, 3, 4)

**Key Activities:**
- Execute evolved `epic_smoke_test_plan.md` (4 parts)
- Run epic-level smoke testing (all features together)
- Complete 3 epic-level QC rounds
- Epic-level PR review (11 categories)
- Validate against original epic request

**Critical Rule:** If bugs found → Create bug fixes, RESTART S9 after fixes

**Next:** S10

---

### S10: Epic Cleanup

**Purpose:** Commit changes, archive epic, apply lessons learned

**Inputs:** S9 complete, epic validated

**Outputs:**
- All changes committed to git
- Epic moved to `feature-updates/done/`
- Guides updated based on lessons learned

**Guide:** `stages/s10/s10_epic_cleanup.md`

**Key Activities:**
1. Run unit tests (100% pass MANDATORY)
2. Verify documentation complete
3. **User testing (MANDATORY GATE):**
   - Ask user to test complete system
   - If bugs found → Fix bugs, RESTART S9
   - Repeat until user testing passes with ZERO bugs
4. Update guides based on lessons learned
5. Commit changes with clear message
6. Move epic folder to `done/`

**Critical Rule:** Cannot commit without user testing approval

**Next:** None (Epic complete!)

---

### Bug Fix Workflow

**When:** Bugs discovered during ANY stage

**Guide:** `stages/s5/s5_bugfix_workflow.md`

**Workflow:** S2 → S5 → S6 → S7 (SKIP Stages 1, 3, 4, S8, S9, S10)

**Folder Structure:**
```text
feature-updates/KAI-{N}-{epic_name}/bugfix_{priority}_{name}/
```

**Priority Levels:**
- **high**: Breaks core functionality, produces incorrect results
- **medium**: Reduces quality but system usable
- **low**: Cosmetic issues, minor usability problems

**After bug fix complete:** Return to paused work

---

## Critical Protocols

### 1. Mandatory Reading Protocol

**🚨 BEFORE starting ANY stage, you MUST:**

1. **Read the ENTIRE guide** using Read tool
2. **Use the phase transition prompt** from `prompts_reference_v2.md`
3. **Acknowledge critical requirements** by listing them explicitly
4. **Verify ALL prerequisites** using checklist in guide
5. **Update README Agent Status** to reflect stage start
6. **THEN AND ONLY THEN** begin work

**Why this matters:**
- Historical data shows 40% guide abandonment rate without mandatory prompts
- Reading guide first ensures no mandatory steps missed
- Prompt acknowledgment confirms understanding

**Example:**
```text
I'm reading stages/s5/s5_p1_planning_round1.md to ensure I follow all 7 iterations in Round 1...

The guide requires:
- Round 1: 7 MANDATORY iterations (iterations 1-7 + 4a)
- Iteration 4a is a MANDATORY GATE (Implementation Plan Specification Audit)
- Algorithm Traceability Matrix (iteration 4)
- Integration Gap Check (iteration 7)
- STOP if confidence < Medium at Round 1 checkpoint

Prerequisites I'm verifying:
✅ spec.md exists and is complete
✅ checklist.md all items resolved
✅ S4 (Epic Testing Strategy) complete

I'll now proceed with Round 1 (iterations 1-7 + 4a)...
```

### 2. Phase Transition Protocol

**Phase transition prompts are MANDATORY for:**
- Starting any of the 10 stages (S1, S2, S3, S4, S5, S6, S7, S8, S9, S10)
- Starting S5 rounds (Round 1, 2, 3)
- Starting S7 phases (Smoke Testing, QC Rounds, Final Review)
- Creating a bug fix
- Resuming after session compaction

**Where to find prompts:** `prompts_reference_v2.md`

**Format of prompts:**
```markdown
## Starting S1: Epic Planning

I'm reading `stages/s1/s1_epic_planning.md` to ensure I follow the complete epic planning process...

The guide requires:
- [List 3-5 critical requirements from guide]

Prerequisites I'm verifying:
- [List prerequisite checks]

I'll now proceed with S1...
```

### 3. Agent Status Update Protocol

**Update Agent Status at these checkpoints:**

**In EPIC_README.md:**
- Starting each stage (1-7)
- Stage completion
- Epic completion

**In feature README.md:**
- Starting feature work (S2)
- Starting implementation (S5)
- Phase transitions within S5
- Feature completion (after S8.P2)

**Agent Status Format:**
```markdown
## Agent Status

**Last Updated:** 2025-12-31 10:00
**Current Stage:** S6 - Implementation Execution
**Current Step:** Implementing PlayerManager.calculate_score() method
**Current Guide:** stages/s6/s6_execution.md
**Status:** IN PROGRESS
**Progress:** Component 3 of 5 complete

**Next Action:** Complete calculate_score() method and run unit tests

**Critical Rules from Current Guide:**
1. Keep spec.md VISIBLE at all times
2. Run unit tests after EVERY component (100% pass required)
3. Update implementation_checklist.md continuously
```

**Why this matters:** Session compaction can interrupt agents mid-workflow. Agent Status survives context limits and provides exact resumption point.

### 4. QC Restart Protocol

**Applies to:** S7 QC Rounds, S9 Epic QC

**Rule:** If ANY issues found during QC → COMPLETELY RESTART from beginning

**S7 (Feature QC):**
- Issues found in QC Round 1, 2, or 3?
- Fix all issues
- RESTART from smoke testing (Part 1)
- Re-run all 3 QC rounds

**S9 (Epic QC):**
- Issues found during epic validation?
- Create bug fixes (follow bug fix protocol)
- After ALL bug fixes complete → RESTART S9 from beginning
- Re-run all epic smoke testing and QC rounds

**Why:** Ensures validation covers ALL changes, including fixes

### 5. Zero Tech Debt Tolerance

**Rule:** Fix ALL issues immediately - NO deferrals

**Never defer:**
- Critical issues (obviously)
- Minor issues (type hints, docstrings)
- Cosmetic issues (formatting, comments)

**If you find an issue:**
1. Fix it NOW
2. Do NOT write "TODO" comments
3. Do NOT document for "later"
4. Do NOT create "will refactor later" notes

**Why:** "Later" often never comes. Clean code at each stage = clean epic at end.

### 6. 100% Unit Test Pass Rate

**Rule:** All unit tests must pass before proceeding

**When to run tests:**
- After EVERY component in S6
- Before starting QC (S7)
- Before committing (S10)

**What to do if tests fail:**
- STOP implementation
- Fix failing tests
- Re-run until 100% pass
- THEN proceed

**Acceptable to fix:** Pre-existing test failures from other epics during S10

---

## Phase Transition Protocol

### What are Phase Transition Prompts?

Phase transition prompts are **mandatory acknowledgments** that prove you read the guide before starting work. They prevent the historical problem of agents skipping guides and missing critical steps.

### When to Use Phase Transition Prompts

**MANDATORY for:**
1. Starting any stage (1-7)
2. Starting S5 rounds (1, 2, 3)
3. Starting S7 phases (Smoke Testing, QC Rounds, Final Review)
4. Creating a bug fix
5. Resuming in-progress epic after session compaction

### Where to Find Prompts

**File:** `prompts_reference_v2.md`

**Contents:**
- Complete library of all phase transition prompts
- Organized by stage and checkpoint
- Copy-paste ready format

### How to Use Phase Transition Prompts

**Step 1:** Identify which stage/phase you're starting

**Step 2:** Read the guide for that stage/phase FIRST

**Step 3:** Open `prompts_reference_v2.md` and find the corresponding prompt

**Step 4:** Use the prompt template, filling in:
- Critical requirements from guide (3-5 items)
- Prerequisites being verified
- Next immediate action

**Step 5:** Proceed with work after using prompt

### Example Phase Transition

**Scenario:** Starting S5 Round 1

**Step 1:** Read `stages/s5/s5_p1_planning_round1.md`

**Step 2:** Find "Starting S5 Round 1" prompt in `prompts_reference_v2.md`

**Step 3:** Use the prompt:

```text
I'm reading stages/s5/s5_p1_planning_round1.md to ensure I follow all 7 iterations in Round 1...

The guide requires:
- Round 1: 7 MANDATORY iterations (iterations 1-7 + 4a)
- Iteration 4a is a MANDATORY GATE (Implementation Plan Specification Audit)
- Algorithm Traceability Matrix (iteration 4)
- Integration Gap Check (iteration 7)
- STOP if confidence < Medium at Round 1 checkpoint

Prerequisites I'm verifying:
✅ spec.md exists and is complete
✅ checklist.md all items resolved
✅ S4 (Epic Testing Strategy) complete

I'll now proceed with Round 1 (iterations 1-7 + 4a)...
```

**Step 4:** Execute Round 1 iterations

### What Happens if You Skip the Prompt?

**Historical data shows:**
- 40% guide abandonment rate without prompts
- 3x higher error rate in implementation
- 2x more QC restarts needed

**User expectation:**
- Users expect agents to follow the workflow rigorously
- Skipping prompts signals rushed/careless approach
- Using prompts demonstrates professionalism and attention to detail

---

## Using the Guides

### Guide Organization

**16 total guides in `guides_v2/`:**

**Planning Guides (4):**
- stages/s1/s1_epic_planning.md
- stages/s2/s2_feature_deep_dive.md
- stages/s3/s3_cross_feature_sanity_check.md
- stages/s4/s4_epic_testing_strategy.md

**Implementation Guides (11):**
- stages/s5/s5_p1_planning_round1.md (Round 1)
- stages/s5/s5_p2_planning_round2.md (Round 2)
- stages/s5/s5_p3_planning_round3.md (Round 3 Part 1)
- stages/s5/s5_p3_i2_gates_part1.md (Round 3 Part 2a)
- stages/s5/s5_p3_i3_gates_part2.md (Round 3 Part 2b)
- stages/s6/s6_execution.md
- stages/s7/s7_p1_smoke_testing.md (Phase 1)
- stages/s7/s7_p2_qc_rounds.md (Phase 2)
- stages/s7/s7_p3_final_review.md (Phase 3)
- stages/s8/s8_p1_cross_feature_alignment.md
- stages/s8/s8_p2_epic_testing_update.md
- stages/s5/s5_bugfix_workflow.md

**Finalization Guides (5):**
- stages/s9/s9_epic_final_qc.md (router)
- stages/s9/s9_p1_epic_smoke_testing.md (Steps 1-2)
- stages/s9/s9_p2_epic_qc_rounds.md (Steps 3-5)
- stages/s9/s9_p4_epic_final_review.md (Steps 6-8)
- stages/s10/s10_epic_cleanup.md

**Supporting Files (4):**
- EPIC_WORKFLOW_USAGE.md (this file)
- prompts_reference_v2.md (phase transition prompts)
- templates/ (file templates)
- README.md (guide index and quick reference)

### Guide Structure

**All guides follow consistent structure:**

1. **Header:** Version, last updated, prerequisites, next stage
2. **Mandatory Reading Protocol:** Instructions for using the guide
3. **Quick Start:** Brief overview of stage purpose
4. **Critical Rules:** Non-negotiable requirements in highlighted box
5. **Prerequisites Checklist:** Verify before starting
6. **Workflow Overview:** Visual diagram of stage flow
7. **Detailed Workflow:** Step-by-step instructions
8. **Re-Reading Checkpoints:** When to re-read guide
9. **Completion Criteria:** Checklist for stage completion
10. **Common Mistakes:** Anti-patterns to avoid
11. **Real-World Examples:** Concrete scenarios
12. **README Agent Status Update Requirements:** When/how to update

### How to Read a Guide

**1. Read the ENTIRE guide first** (don't jump to middle)

**2. Pay special attention to:**
- Critical Rules box (non-negotiable)
- Prerequisites Checklist (must verify before starting)
- Completion Criteria (how you know you're done)

**3. Use the guide actively:**
- Open it in a separate Read tool window
- Reference it throughout the stage
- Check completion criteria before moving on

**4. Re-read when:**
- Session compaction occurs
- You encounter confusion
- You're about to make a critical decision
- Moving between major sections

### Guide Quick Reference

**Find the right guide for your situation:**

| Situation | Guide to Use |
|-----------|-------------|
| User wants new epic | stages/s1/s1_epic_planning.md |
| Writing feature spec | stages/s2/s2_feature_deep_dive.md |
| Checking feature conflicts | stages/s3/s3_cross_feature_sanity_check.md |
| Planning epic tests | stages/s4/s4_epic_testing_strategy.md |
| Creating implementation plan | S5.P1/S5.P2/S5.P3 (rounds 1-3) |
| Writing code | stages/s6/s6_execution.md |
| Testing feature | S7.P1/S7.P2/S7.P3 (smoke/QC/review) |
| Updating other specs | stages/s8/s8_p1_cross_feature_alignment.md |
| Updating test plan | stages/s8/s8_p2_epic_testing_update.md |
| Testing epic | stages/s9/s9_p1_epic_smoke_testing.md (start here) |
| Committing/archiving | stages/s10/s10_epic_cleanup.md |
| Fixing a bug | stages/s5/s5_bugfix_workflow.md |
| Resuming work | EPIC_README.md Agent Status + current guide |
| Finding prompts | prompts_reference_v2.md |
| Creating files | templates/ |

---

## Key Principles

### 1. Specification is King

**Primary principle:** `spec.md` is the single source of truth

**What this means:**
- Write complete, detailed specs BEFORE implementing
- Keep spec.md visible during implementation
- Verify implementation against spec continuously
- Update spec if reality differs from plan (document why)

**Why:**
- Prevents "implementation drift" (code diverging from requirements)
- Ensures nothing forgotten
- Provides audit trail

### 2. Plan → Implement → Verify

**Three-phase cycle for everything:**

1. **Plan:** Write spec, create implementation plan, think through edge cases
2. **Implement:** Write code, following spec and implementation plan exactly
3. **Verify:** Test, review, validate against spec and requirements

**Never skip to implementation without planning**
**Never skip verification after implementation**

### 3. Continuous Verification

**Verify continuously, not just at end:**

- During S5: 22 verification iterations
- During S6: Mini-QC after each component
- During S7: 3-phase validation (smoke, QC, review)
- During S9: Epic-level validation

**Why:** Catch issues early when cheap to fix, not late when expensive

### 4. Epic vs Feature Distinction

**Epic-level work:**
- Integration between features
- Epic success criteria
- Cross-feature patterns
- Epic testing strategy

**Feature-level work:**
- Individual feature implementation
- Feature-specific testing
- Feature documentation
- Feature lessons learned

**Keep these separate:**
- S7 validates individual features
- S9 validates epic integration
- Don't mix feature and epic concerns

### 5. Continuous Refinement

**Nothing is set in stone:**

- `epic_smoke_test_plan.md` evolves (S1 → 4 → S8.P2 → 6)
- Feature specs update based on reality (S8.P1)
- Guides improve based on lessons learned (S10)

**Plan for evolution:**
- Original assumptions may be wrong
- Implementation reveals reality
- Update plans based on learnings

### 6. Documentation as First-Class Artifact

**Documentation is not optional:**

- README files track context and status
- spec.md defines requirements
- lessons_learned.md captures insights
- Git history tracks what/why for changes

**Documentation enables:**
- Future agents to resume work
- Future epics to learn from past
- Future developers to understand decisions
- Git history provides complete change tracking

### 7. Quality is Non-Negotiable

**Quality standards:**
- 100% unit test pass rate
- Zero tech debt tolerance
- Zero critical issues
- Complete documentation

**No shortcuts:**
- Don't defer issues for "later"
- Don't skip QC steps
- Don't commit failing tests
- Don't leave incomplete documentation

---

## Setting Up in a New Project

### Prerequisites

**Your project needs:**
1. Git repository (for version control)
2. Test suite with test runner (for 100% pass requirement)
3. Development workflow (how code gets written/reviewed)

### Step 1: Copy the Guides Folder

**Copy this folder to your project:**
```bash
# From this project
cp -r feature-updates/guides_v2/ /path/to/new-project/feature-updates/guides_v2/

# Or create new folder structure
mkdir -p /path/to/new-project/feature-updates/guides_v2/
cp feature-updates/guides_v2/* /path/to/new-project/feature-updates/guides_v2/
```

**What you're copying:**
- 16 stage guides
- 4 supporting files (this file, prompts, templates, README)

### Step 2: Create Feature-Updates Folder Structure

**In your new project:**
```bash
cd /path/to/new-project
mkdir -p feature-updates
mkdir -p feature-updates/done
```

**Folder structure:**
```markdown
new-project/
├── feature-updates/
│   ├── guides_v2/              # Copied from this project
│   └── done/                   # Archive for completed epics
└── [your project files]
```

### Step 3: Create Project-Specific CLAUDE.md

**Copy this section to your project's CLAUDE.md:**

```markdown
# [Your Project Name] - Claude Code Guidelines

## Epic-Driven Development Workflow

This project uses the Epic-Driven Development Workflow v2 for managing features and epics.

**Complete workflow documentation:** `feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md`

**Quick workflow overview:**
- User creates `feature-updates/{epic_name}.txt` with initial request
- Agent follows 10-stage process (Planning → Implementation → Validation)
- Complete epics move to `feature-updates/done/`

**Critical rules:**
1. **ALWAYS read the guide** before starting any stage (use Read tool)
2. **ALWAYS use phase transition prompts** from `prompts_reference_v2.md`
3. **ALWAYS verify prerequisites** before proceeding
4. **ALWAYS update Agent Status** in README files

**For resuming in-progress work:**
1. Check for epic folders in `feature-updates/`
2. Read `EPIC_README.md` "Agent Status" section
3. Use "Resuming In-Progress Epic" prompt
4. Continue from listed next action

**For starting new epic:**
1. Verify user created `feature-updates/{epic_name}.txt`
2. Use "Starting S1" prompt from `prompts_reference_v2.md`
3. Read `stages/s1/s1_epic_planning.md`
4. Begin S1 workflow

**See:** `feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md` for complete instructions
```

### Step 4: Customize for Your Project

**Update these sections in guides if needed:**

1. **Test command** (if not `python tests/run_all_tests.py`):
   - Update in stages/s6/s6_execution.md
   - Update in stages/s10/s10_epic_cleanup.md

2. **File paths** (if different structure):
   - Update examples in guides to match your project structure
   - Update templates/ with your paths

3. **Commit protocol** (if different from project standards):
   - Update stages/s10/s10_epic_cleanup.md commit message format
   - Update any project-specific commit requirements

4. **Project-specific terminology:**
   - Replace "FantasyFootballHelperScripts" with your project name
   - Update example file paths in guides

### Step 5: Test with First Epic

**Try the workflow with a small epic:**

1. **Create test epic request:**
   ```bash
   echo "Test epic to verify workflow" > feature-updates/test_workflow.txt
   ```

2. **Run through S1:**
   - Use "Starting S1" prompt
   - Read stages/s1/s1_epic_planning.md
   - Create epic folder structure
   - Verify all files created correctly

3. **Verify structure:**
   ```bash
   ls feature-updates/test_workflow/
   # Should see: EPIC_README.md, epic_smoke_test_plan.md, epic_lessons_learned.md, feature_01_*/
   ```

4. **Complete test epic** (or cancel if just testing)

5. **Review lessons learned:**
   - What worked well?
   - What needed customization?
   - Update guides based on findings

### Step 6: Document Project-Specific Patterns

**Create project-specific guide additions:**

**Example:** If your project has specific coding standards:

Create `feature-updates/guides_v2/PROJECT_SPECIFIC_STANDARDS.md`:
```markdown
# Project-Specific Standards

## Coding Conventions
[Your project's coding standards]

## Testing Requirements
[Your project's test requirements]

## Review Process
[Your project's review process]

## Integration with Epic Workflow
- Apply these standards during S6 (Implementation)
- Verify compliance during S7 (QC Rounds)
- Include in PR Review checklist
```

### Step 7: Train Your Team

**If multiple agents/developers will use workflow:**

1. **Share this guide:** Point them to `EPIC_WORKFLOW_USAGE.md`

2. **Run walkthrough:** Complete one epic together, following guides

3. **Create quick reference card:**
   ```markdown
   # Quick Reference
   - Starting work: Check feature-updates/ for in-progress epics
   - Resume: Read EPIC_README.md Agent Status
   - New epic: User creates .txt file → Start S1
   - Stuck: Re-read current guide
   - Questions: Check prompts_reference_v2.md
   ```

4. **Review first epic:** After first epic completes, review lessons learned as team

---

## Appendix Reference

**For detailed examples, FAQs, and stage-by-stage workflows, see:**

**File:** `EPIC_WORKFLOW_USAGE_appendix.md`

**Contents:**
1. **Common Patterns** (7 patterns with detailed examples)
   - Pattern 1: Starting from User Request
   - Pattern 2: Resuming In-Progress Epic
   - Pattern 3: Transitioning Between Stages
   - Pattern 4: Handling QC Failures
   - Pattern 5: User Testing Finds Bugs (S10)
   - Pattern 6: Session Compaction Mid-Epic
   - Pattern 7: S2 Parallel Work (3+ Features)

2. **Frequently Asked Questions** (9 FAQs)
   - Can I skip stages for small changes?
   - What if spec.md is wrong after implementation?
   - How long does a typical epic take?
   - What if user wants changes during implementation?
   - Can multiple agents work on one epic?
   - What if tests are failing from unrelated changes?
   - How do I handle dependencies between features?
   - What if S9 finds major architectural issues?
   - How does the guide improvement workflow work?

3. **Stage-by-Stage Detailed Workflows** (Complete S1-S10 breakdown)
   - Detailed phase/iteration structure for each stage
   - Complete gate listings and validation loops
   - Extracted from CLAUDE.md for reference

**When to use the appendix:**
- Need detailed examples of common workflow patterns
- Have questions about edge cases or specific scenarios
- Need complete phase/iteration breakdown for a stage
- Want to understand parallel work coordination in depth

**Main guide remains your primary reference** for:
- Quick start and resumption procedures
- File structure and organization
- Critical protocols and mandatory gates
- Phase transition requirements
- Quality standards and principles

---

## Summary

**The Epic-Driven Development Workflow v2 provides:**
- ✅ Structured 10-stage process (Planning → Implementation → Validation)
- ✅ Rigorous verification at every step (22 iterations in S5 alone)
- ✅ Complete documentation (specs, changes, lessons learned)
- ✅ Quality gates (100% tests, zero tech debt, user testing)
- ✅ Continuous improvement (lessons applied to guides)

**Critical success factors:**
1. **Read guides completely** before starting work
2. **Use phase transition prompts** to prove understanding
3. **Update Agent Status** for resumption after compaction
4. **Follow QC protocols** rigorously (no shortcuts)
5. **Maintain zero tech debt** (fix all issues immediately)

**This workflow is portable:**
- Copy `guides_v2/` folder to new project
- Customize for project-specific needs
- Train team on workflow
- Apply lessons learned to improve guides

**The workflow has been proven to:**
- Reduce implementation errors by 80%+
- Ensure complete documentation
- Catch integration issues early
- Build institutional knowledge
- Scale from small bugs to large features

**Remember:** The workflow exists to help you succeed. Follow it rigorously, learn from each epic, and continuously improve.

---

**For detailed examples, FAQs, and complete stage-by-stage workflows:**

**See:** `EPIC_WORKFLOW_USAGE_appendix.md`

---

**For more information:**
- Complete guide index: `README.md`
- Phase transition prompts: `prompts_reference_v2.md`
- File templates: `templates/`
- Detailed workflow spec: `PLAN.md`

**Questions or feedback?** Update `epic_lessons_learned.md` with guide improvement suggestions.

---

**END OF EPIC WORKFLOW USAGE GUIDE**
