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
10. [Common Patterns](#common-patterns)

---

## ⚡ Quick Jump Navigation

**Jump directly to specific sections:**

| Section | Purpose | Jump |
|---------|---------|------|
| Overview | What is the workflow | [Go](#overview) |
| Quick Start | Starting a new epic | [Go](#quick-start) |
| File Structure | Epic and feature folders | [Go](#file-structure) |
| Workflow Stages | All 10 stages explained | [Go](#workflow-stages) |
| Critical Protocols | Mandatory protocols | [Go](#critical-protocols) |
| Phase Transition | How to transition stages | [Go](#phase-transition-protocol) |
| Using the Guides | How to read guides | [Go](#using-the-guides) |
| Key Principles | Core workflow principles | [Go](#key-principles) |
| Setting Up | New project setup | [Go](#setting-up-in-a-new-project) |
| Common Patterns | Workflow patterns | [Go](#common-patterns) |

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

## Common Patterns

### Pattern 1: Starting from User Request

**User says:** "Help me develop {feature_name}"

**Your response:**
```text
I'll help you develop {feature_name} using the Epic-Driven Development Workflow.

First, I need to check if there are any in-progress epics...
[Check feature-updates/ folder]

No in-progress epics found. Let me verify you have a request file...

I see you have feature-updates/{epic_name}.txt. Let me start S1.

[Use "Starting S1" prompt from prompts_reference_v2.md]
[Read stages/s1/s1_epic_planning.md]

I'm reading stages/s1/s1_epic_planning.md to ensure I follow the complete epic planning process...

The guide requires:
- Analyze epic request and perform codebase reconnaissance
- Propose feature breakdown (get user approval)
- Create epic folder structure with all required files
- Create feature folders with initial documentation
- Generate initial epic_smoke_test_plan.md

Prerequisites I'm verifying:
✅ User created feature-updates/{epic_name}.txt with initial notes
✅ feature-updates/guides_v2/ folder exists
✅ No conflicting in-progress epics

I'll now proceed with S1...

[Begin S1 workflow]
```

### Pattern 2: Resuming In-Progress Epic

**You notice epic folder exists in feature-updates/**

**Your response:**
```text
I notice there's an in-progress epic: {epic_name}

Let me check its current status...

[Read feature-updates/KAI-{N}-{epic_name}/EPIC_README.md Agent Status section]

I see the epic is currently at:
- Current Stage: S6 - Implementation Execution
- Current Step: Implementing Feature 2, component 3 of 5
- Next Action: Complete PlayerManager.calculate_score() method

[Use "Resuming In-Progress Epic" prompt from prompts_reference_v2.md]

I'm resuming the in-progress epic {epic_name}. Let me read the current guide to restore context...

[Read stages/s6/s6_execution.md]

The guide requires:
- Keep spec.md VISIBLE at all times
- Run unit tests after EVERY component (100% pass required)
- Continuous spec verification via implementation_checklist.md

Current status:
- Feature: feature_02_{name}
- Component: 3 of 5 complete
- Next: Complete PlayerManager.calculate_score() method

I'll now continue with the implementation...

[Continue from next action listed in Agent Status]
```

### Pattern 3: Transitioning Between Stages

**Completing S2, moving to S3**

**Your response:**
```text
I've completed S2 (Feature Deep Dives) for all features.

Let me verify completion criteria before moving to S3...

S2 Completion Criteria:
✅ All features have complete spec.md files
✅ All checklist.md items resolved
✅ Feature README.md files updated
✅ User questions answered

All criteria met. Ready to proceed to S3.

[Update EPIC_README.md Agent Status to show S2 complete]

[Use "Starting S3" prompt from prompts_reference_v2.md]

I'm reading stages/s3/s3_cross_feature_sanity_check.md to ensure I perform thorough cross-feature validation...

The guide requires:
- Systematic pairwise comparison of all feature specs
- Identify conflicts, overlaps, and gaps
- Resolve all inconsistencies
- Get explicit user sign-off on complete plan

Prerequisites I'm verifying:
✅ ALL features have complete specs (S2 done)
✅ All checklist.md items resolved
✅ Feature dependencies identified

I'll now proceed with S3...

[Begin S3 workflow]
```

### Pattern 4: Handling QC Failures

**QC Round 2 finds issues**

**Your response:**
```text
QC Round 2 found the following issues:

CRITICAL:
1. PlayerManager.calculate_score() returns incorrect value for edge case (injured player with bye week)

MINOR:
2. Missing type hint on helper function _normalize_score()

These issues require fixes before proceeding.

Following QC Restart Protocol from stages/s7/s7_p2_qc_rounds.md:
- Fix ALL issues immediately (no deferrals)
- RESTART from smoke testing (Part 1)
- Re-run all 3 QC rounds

Fixing issues now...

[Fix issue 1 - calculate_score() edge case]
[Fix issue 2 - add type hint]
[Run unit tests - verify 100% pass]

All issues fixed. Restarting QC process from smoke testing...

[Execute stages/s7/s7_p1_smoke_testing.md Part 1]
[Execute Part 2]
[Execute Part 3]

Smoke testing passed. Moving to QC rounds...

[Execute QC Round 1]
[Execute QC Round 2 - verify no issues]
[Execute QC Round 3]

All QC rounds passed. Proceeding to Final Review...
```

### Pattern 5: User Testing Finds Bugs (S10)

**User reports bugs during mandatory testing**

**Your response:**
```text
You reported the following bugs during testing:

1. Draft recommendations show incorrect player rankings
2. Export file has wrong column headers

Following S10 bug fix protocol from stages/s10/s10_epic_cleanup.md:

Step 1: Document Bugs

Creating bug fix folders:
- bugfix_high_incorrect_rankings/
- bugfix_low_wrong_headers/

[Create notes.txt for each bug]

Please verify these notes.txt files accurately describe the bugs...

[Wait for user verification]

Step 2: Fix ALL Bugs

[For each bug fix, follow stages/s5/s5_bugfix_workflow.md]
[S2: Create spec.md]
[S5: Create implementation_plan.md, get user approval]
[S6: Implement fix]
[S7: Smoke testing + QC rounds]

Both bug fixes complete.

Step 3: RESTART S9 (Epic Final QC)

Following guide requirement: After bug fixes, must restart ENTIRE S9.

[Read stages/s9/s9_p1_epic_smoke_testing.md]
[Execute epic smoke testing - 4 parts]
[Read stages/s9/s9_p2_epic_qc_rounds.md]
[Execute epic QC rounds - 3 rounds]
[Read stages/s9/s9_p4_epic_final_review.md]
[Execute epic PR review and final verification]

S9 complete with zero issues.

Step 4: Return to User Testing

I've fixed both bugs and re-validated the epic (S9 passed).

Bugs fixed:
- Bug 1: Draft recommendations now show correct rankings (sorted by score DESC)
- Bug 2: Export headers now match expected format (Name, Position, Team, Score)

Please test the system again to verify the bugs are fixed and no new issues introduced.

[Wait for user testing results]
```

### Pattern 6: Session Compaction Mid-Epic

**You start conversation and notice in-progress epic but no context**

**Your response:**
```text
I notice there's an in-progress epic but I don't have the conversation history.

Let me check the epic status to understand where we are...

[Read feature-updates/KAI-{N}-{epic_name}/EPIC_README.md Agent Status]

The epic is currently at:
- Stage: S5 - Implementation Planning
- Round: Round 2
- Iteration: 11 of 16
- Guide: stages/s5/s5_p2_planning_round2.md
- Next Action: Complete Algorithm Traceability Matrix (iteration 11)

Session compaction occurred. Following resumption protocol...

[Use "Resuming After Session Compaction" prompt from prompts_reference_v2.md]

I'm resuming work on {epic_name} after session compaction. Let me restore context...

[Read stages/s5/s5_p2_planning_round2.md]
[Read feature spec.md]
[Read current implementation_plan.md]

Context restored. Current task: Iteration 11 (Algorithm Traceability Matrix)

The guide requires:
- Re-verify algorithm traceability from iteration 4
- Check for any new algorithms discovered during iterations 8-10
- Update traceability matrix if needed

I'll now continue with iteration 11...

[Resume work from iteration 11]
```


### Pattern 7: S2 Parallel Work (3+ Features)

**Scenario:** Epic has 3+ features, Primary offers parallel work to user

**Overview:**
When an epic has 3 or more features, S2 (Feature Deep Dives) can be parallelized with multiple agents working simultaneously. This reduces S2 time by 40-60% (e.g., 3-feature epic saves ~4 hours).

**Key Roles:**
- **Primary Agent**: Coordinator + Feature 01 owner (85% feature work, 15% coordination)
- **Secondary Agents**: Feature owners (90% feature work, 10% coordination)

---

#### Phase 1: Offering Parallel Work (Primary, during S1)

**At S1 Step 5.8 (Analyze Features for Parallelization):**

```text
I've created {N} features for this epic.

Let me analyze if parallel work would be beneficial...

Feature count: {N} features
Expected S2 time (sequential): {N × 2.5} hours = {total} hours
Expected S2 time (parallel): ~3 hours with {N} agents
Time savings: ~{savings} hours (40-60% reduction)

Decision: {N} >= 3, parallel work recommended.

[Continue to S1 Step 5.9]
```

**At S1 Step 5.9 (Offer Parallel Work to User):**

```markdown
I can offer parallel work for S2 (Feature Deep Dives):

**Parallel Mode:**
- Multiple agents work on S2 simultaneously
- Each agent owns one feature completely
- I coordinate and own Feature 01
- Time: ~3 hours total (vs {sequential_time} hours sequential)
- Complexity: Requires spawning additional agents

**Sequential Mode:**
- I complete all features one by one
- Simpler coordination (just me)
- Time: ~{sequential_time} hours
- Standard workflow

**Recommendation:** Parallel mode saves ~{savings} hours for {N} features.

Would you like to:
1. ✅ Enable parallel work for S2 (I'll provide setup instructions)
2. ❌ Continue sequential (I'll do all features one by one)
3. ❓ Discuss parallelization approach
```

**If user chooses Option 1 (Enable parallel):**

```text
Great! I'll coordinate parallel S2 work.

After completing S1, I'll:
1. Generate handoff packages for secondary agents
2. Provide spawn commands for you to create secondary agents
3. Begin S2.P1 for Feature 01 while secondaries work on their features
4. Coordinate via checkpoints and message files

You'll need to spawn {N-1} secondary agents (I'll provide exact commands).

Continuing with S1...

[Complete S1 as normal]
```

---

#### Phase 2: Generating Handoff Packages (Primary, after S1)

**After S1 completes, Primary generates handoff packages and awaits secondary agent spawn.**

This reduced section focuses on the workflow without showing all the detailed coordination mechanics (those are in the dedicated guides).

---

#### Phase 3: Coordination During S2 (Primary)

**Primary performs coordination heartbeat every 15 minutes:**
- Update own checkpoint
- Check secondary inboxes for messages/escalations
- Process any escalations (answer questions, clarify specs)
- Verify no stale agents (checkpoint age < 30 min warning, < 60 min failure)
- Update EPIC_README.md with progress
- Continue Feature 01 work

**Coordination overhead:** <10% of time (15 min coordination per hour)

---

#### Phase 4: Secondary Agent Workflow

**Secondary receives handoff from user, executes startup:**
1. Parse handoff configuration
2. Create communication and coordination files
3. Send startup confirmation to Primary
4. Begin S2.P1 for assigned feature

**During S2 work:**
- Execute S2.P1, S2.P2, S2.P3 for assigned feature
- Coordinate every 15 minutes (update checkpoint, check inbox, update STATUS)
- Escalate blockers to Primary within 15 minutes
- Focus 90% on feature work, 10% on coordination

**After completing S2.P3:**
- Send completion message to Primary
- Update STATUS: READY_FOR_SYNC
- Update checkpoint: WAITING_FOR_SYNC
- WAIT for Primary to run S3

---

#### Phase 5: Sync Point - Transition to S3

**Primary verifies all agents completed S2:**
1. Check all completion messages received
2. Verify all STATUS files: READY_FOR_SYNC = true
3. Verify all checkpoints fresh and WAITING_FOR_SYNC
4. Create sync verification document
5. Notify secondaries that S3 is starting
6. Run S3 solo (secondaries wait)
7. After S3+S4 complete, notify secondaries to proceed

**S3 and S4 run sequentially by Primary only** (requires epic-level view)

---

#### Phase 6: Common Issues

**Stale Agent (checkpoint > 60 minutes old):**
- Primary detects during coordination heartbeat
- Sends status check message (wait 15 min)
- If no response, escalates to user
- Recovery: Same agent resumes, new agent takes over, or Primary absorbs feature
- See: `parallel_work/stale_agent_protocol.md`

**Sync Timeout (S2 not all complete within expected time):**
- Soft timeout: 4 hours (send reminder, request ETA)
- Hard timeout: 6 hours (escalate to user)
- Recovery: Wait with ETA, investigate blocker, abort parallel for late feature
- See: `parallel_work/sync_timeout_protocol.md`

**Escalation Handling:**
- Secondary escalates blocker to Primary
- Primary attempts to resolve (answer question, clarify spec)
- If requires user input, Primary escalates to user
- SLA: 15-minute response time
- See: `parallel_work/communication_protocol.md`

---

#### Summary: Benefits and Requirements

**Benefits:**
- 40-60% time reduction for S2 phase
- Scales with feature count (3 features = 4 hours vs 7.5 hours)
- Each agent focuses deeply on one feature
- Maintains quality through individual feature ownership

**Requirements:**
- User must spawn secondary agents (Primary provides commands)
- All agents coordinate via files (checkpoints, messages, STATUS)
- Primary dedicates 15% time to coordination
- Checkpoint updates every 15 minutes (enables recovery)

**When to Use:**
- 3+ features: Recommended (good time savings)
- 2 features: Optional (modest savings, user decides)
- 1 feature: Not applicable (no parallelization possible)

**See Complete Guides:**
- `parallel_work/s2_parallel_protocol.md` - Master protocol overview
- `parallel_work/s2_primary_agent_guide.md` - Primary agent complete workflow
- `parallel_work/s2_secondary_agent_guide.md` - Secondary agent complete workflow
- `parallel_work/stale_agent_protocol.md` - Stale agent detection and recovery
- `parallel_work/sync_timeout_protocol.md` - Sync point timeout handling
- `parallel_work/communication_protocol.md` - Message formats and channels
- `parallel_work/checkpoint_protocol.md` - Checkpoint structure and updates
- `parallel_work/lock_file_protocol.md` - File locking for shared resources

---

---

## Frequently Asked Questions

### Q: Can I skip stages for small changes?

**A:** No. The workflow is designed for consistency and quality. However:
- Very small bug fixes can use the Bug Fix Workflow (skips some stages)
- Each stage has clear purpose - skipping leads to issues
- Historical data: 80% of "small changes" that skip stages require rework

### Q: What if spec.md is wrong after implementation?

**A:** Update it. Document why.
- S8.P1 specifically addresses this (Cross-Feature Spec Alignment)
- Implementation reveals reality that planning couldn't predict
- Update spec.md to reflect actual implementation
- Document reason for change in spec.md

### Q: How long does a typical epic take?

**A:** Depends on complexity:
- Small epic (2 features): 1-2 days
- Medium epic (3-5 features): 3-5 days
- Large epic (6+ features): 1-2 weeks

**Time breakdown:**
- Stages 1-4 (Planning): 20% of time
- S5 (Implementation): 60% of time
- Stages 6-7 (Validation/Cleanup): 20% of time

### Q: What if user wants changes during implementation?

**A:** Update the spec, restart affected stages:
1. Pause current work
2. Update spec.md with new requirements
3. Determine impact (which stages affected)
4. Restart from earliest affected stage
5. Example: New requirement in S6 → Return to S5

### Q: Can multiple agents work on one epic?

**A:** Yes, but coordinate carefully:
- Each agent should work on different feature (S5)
- Stages 1-4 and 6-7 should be single agent
- Use Agent Status to avoid conflicts
- Epic README tracks all feature progress

### Q: What if tests are failing from unrelated changes?

**A:** Fix them.
- S10 requires 100% test pass rate
- It's acceptable to fix pre-existing failures
- Document in epic_lessons_learned.md
- Goal: Clean test suite for everyone

### Q: How do I handle dependencies between features?

**A:** Plan them in S1, implement in order:
- S1: Identify dependencies
- S4: Plan integration testing
- S5: Implement features sequentially (dependency first)
- S9: Validate integration

### Q: What if S9 finds major architectural issues?

**A:** Create bug fixes, potentially refactor:
1. Document issues as high-priority bug fixes
2. Determine if architectural change needed
3. If major refactor: May need new epic
4. If fixable: Create bug fixes, restart S9
5. No shortcuts - quality is non-negotiable

### Q: How does the guide improvement workflow work?

**A:** Every epic includes mandatory guide updates (S10.P1):

**When:** After S10 user testing passes, before final commit

**What gets updated:**
- All files in `feature-updates/guides_v2/` (16 guides + supporting files)
- `CLAUDE.md` (root project instructions)
- Any files that support future agents

**Process:**
1. **Analyze lessons learned:** Agent reads ALL `lessons_learned.md` files (epic + features)
2. **Identify guide gaps:** For each lesson, determine which guide(s) could have prevented the issue
3. **Create proposals:** Agent creates `GUIDE_UPDATE_PROPOSAL.md` with prioritized improvements:
   - **P0 (Critical):** Prevents catastrophic bugs, mandatory gate gaps
   - **P1 (High):** Significantly improves quality, reduces major rework
   - **P2 (Medium):** Moderate improvements, clarifies ambiguity
   - **P3 (Low):** Minor improvements, cosmetic fixes
4. **User approval:** Agent presents EACH proposal individually with before/after comparison
5. **User decides:** For each proposal: Approve / Modify / Reject / Discuss
6. **Apply changes:** Agent applies ONLY approved changes (or user modifications)
7. **Separate commit:** Guide updates committed separately from epic code

**Why mandatory:**
- Continuous guide improvement based on real implementation experience
- Future agents benefit from lessons learned in this epic
- Systematic feedback loop: implementation → lessons → guide updates
- User has full control over guide evolution

**Time estimate:** 20-45 minutes per epic (depending on lessons count)

**See:** `stages/s10/s10_p1_guide_update_workflow.md` for complete workflow

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

## Stage-by-Stage Detailed Workflows

**Purpose:** Complete workflow details for all 10 stages (extracted from CLAUDE.md for reference)

**When to use:** When you need detailed phase/iteration structure for a specific stage beyond the quick reference in CLAUDE.md

---

### S1: Epic Planning (Detailed)

**Trigger:** "Help me develop {epic-name}"
**First Action:** Use "Starting S1" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s1/s1_epic_planning.md`

⚠️ **CRITICAL: S1 HAS 6 PHASES (NOT 5 STEPS)**

**S1 Phase Structure:**
- **S1.P1:** Initial Setup (Steps 1.0-1.4)
  - Assign KAI number
  - Create git branch
  - Create epic folder structure

- **S1.P2:** Epic Analysis (Step 2)
  - Analyze epic request
  - Identify scope and constraints

- **S1.P3: DISCOVERY PHASE (Step 3)** ← MANDATORY, CANNOT SKIP
  - Guide: `stages/s1/s1_p3_discovery_phase.md`
  - Output: DISCOVERY.md (epic-level source of truth)
  - Time-Box: SMALL 1-2hrs, MEDIUM 2-3hrs, LARGE 3-4hrs
  - Feature folders NOT created until Discovery approved
  - Iterative research and Q&A loop until 3 consecutive iterations with no new questions
  - Re-read code/requirements with fresh perspective each iteration
  - **Historical failure:** KAI-7 agent skipped S1.P3 entirely, blocked 8 secondary agents for 4 hours

- **S1.P4:** Feature Breakdown Proposal (Step 4)
  - Propose feature breakdown
  - Get user approval

- **S1.P5:** Epic Structure Creation (Step 5)
  - Create feature folders
  - Create initial documentation

- **S1.P6:** Transition to S2 (Step 6)
  - Verify structure complete
  - Prepare for S2

**You CANNOT skip S1.P3 Discovery Phase:**
- Must create DISCOVERY.md before feature breakdown
- Must get user approval before creating feature folders
- Feature specs will reference DISCOVERY.md findings
- S2.P1 Phase 0 requires DISCOVERY.md to exist

**Next:** S2

---

### S2: Feature Planning (Detailed)

**First Action:** Use "Starting S2" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s2/s2_feature_deep_dive.md` (router to phases)
**Duration:** 2.25-4 hours per feature (3 iterations)

**Phases:**

**S2.P1: Spec Creation and Refinement** (3 iterations)
- **S2.P1.I1: Feature-Level Discovery** (60-90 min)
  - Embeds Gate 1 (Research Completeness Audit)
  - Research and document feature requirements
  - Create initial spec.md

- **S2.P1.I2: Checklist Resolution** (45-90 min)
  - 9-step protocol for resolving questions
  - User answers questions (agents CANNOT mark [x] autonomously)
  - Update spec.md with answers

- **S2.P1.I3: Refinement & Alignment** (30-60 min)
  - Embeds Gate 2 (Spec-to-Epic Alignment)
  - Includes Gate 3 (User Checklist Approval)
  - Refine spec based on alignment check
  - Get user approval on checklist

**S2.P2: Cross-Feature Alignment** (20-60 min)
- Primary agent only
- Pairwise comparison of feature specs
- Alignment validation

**Key Outputs:**
- spec.md (requirements specification - user-approved)
- checklist.md (QUESTIONS ONLY - user answers ALL before S5.P1)
- RESEARCH_NOTES.md (REQUIRED)

**Validation Loops:**
- S2.P1.I1 (embeds Gate 1)
- S2.P1.I3 (embeds Gate 2)
- S2.P2 (alignment validation)

**Gates:**
- Gate 1: Research Completeness Audit (S2.P1.I1)
- Gate 2: Spec-to-Epic Alignment (S2.P1.I3)
- Gate 3: User Checklist Approval (S2.P1.I3 - explicit user approval)

**Next:** S3 (after ALL features in all groups complete S2)

---

### S3: Epic-Level Documentation, Testing Plans, and Approval (Detailed)

**First Action:** Use "Starting S3" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s3/s3_epic_planning_approval.md`
**Duration:** 75-105 minutes total

**Phases:**

**S3.P1: Epic Testing Strategy Development** (45-60 min)
- Epic-level integration tests
- Cross-feature test scenarios
- Define epic success criteria

**S3.P2: Epic Documentation Refinement** (20-30 min)
- Review epic-level documentation
- Ensure consistency across features
- Update EPIC_README.md

**S3.P3: Epic Plan Approval** (10-15 min)
- Gate 4.5 with 3-tier rejection handling
- User reviews complete epic plan
- User approves or requests changes

**Key Changes from Old Workflow:**
- Pairwise comparison moved to S2.P2
- Old S4 content moved here

**Validation Loops:**
- S3.P1 (testing strategy validation)
- S3.P2 (documentation validation)

**Gates:**
- Gate 4.5: User approves epic plan (MANDATORY, 3-tier rejection handling)

**Next:** S4 (first feature testing strategy)

---

### S4: Feature Testing Strategy (Detailed)

**First Action:** Use "Starting S4" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s4/s4_feature_testing_strategy.md` (router to 4 iterations)
**Purpose:** Test-driven development - plan tests BEFORE implementation
**Duration:** 45-60 minutes per feature

**Iterations:**

**S4.I1: Test Strategy Development** (15-20 min)
- Unit tests planning
- Integration tests planning
- Edge tests planning
- Goal: >90% coverage

**S4.I2: Edge Case Enumeration** (10-15 min)
- Boundary conditions
- Error paths
- Invalid inputs
- State transitions

**S4.I3: Configuration Change Impact** (10-15 min)
- Config test matrix
- Environment variations
- Parameter combinations

**S4.I4: Validation Loop** (15-20 min)
- Validate test strategy completeness
- 3 consecutive clean rounds required
- Zero deferred issues

**Key Output:**
- test_strategy.md (>90% coverage goal)
- Merged into implementation_plan.md in S5.P1.I1

**Next:** S5 (Implementation Planning)

---

### S5: Implementation Planning (Detailed)

**First Action:** Use "Starting S5 Round 1/2/3" prompt from `prompts_reference_v2.md`
**🚨 CRITICAL:** Execute iterations ONE at a time, IN ORDER (no batching, no skipping)
**Duration:** 22 iterations across 3 rounds
**Key Change:** Testing iterations (old I8-I10) moved to S4, remaining iterations renumbered sequentially

**Round 1: Planning Foundation** (7 iterations)
- **Guide:** `stages/s5/s5_p1_planning_round1.md` (router to I1-I3)

**S5.P1.I1: Requirements Analysis** (I1-I3)
- Guide: `stages/s5/s5_p1_i1_requirements.md`
- Merges test_strategy.md from S4
- I1: Requirements review
- I2: Dependencies analysis
- I3: Interface contracts

**S5.P1.I2: Algorithm Planning** (I4-I6 + Gate 4a)
- Guide: `stages/s5/s5_p1_i2_algorithms.md`
- I4: Algorithm design
- I5: Data structures
- I6: Performance considerations
- Gate 4a: TODO Specification Audit

**S5.P1.I3: Integration Planning** (I7 + Gate 7a)
- Guide: `stages/s5/s5_p1_i3_integration.md`
- I7: Integration points
- Gate 7a: Backward Compatibility Check

**Validation Loop:** Added at end of Round 1 (validates Gates 4a, 7a)

**Round 2: Verification** (6 iterations)
- **Guide:** `stages/s5/s5_p2_planning_round2.md` (router, I8-I13)

**S5.P2.I1: First Verification** (I8-I9, formerly I11-I12)
- I8: Requirements verification
- I9: Design verification

**S5.P2.I2: Reverification** (I10-I13, formerly I13-I16)
- I10: Cross-reference check
- I11: Dependency validation
- I12: Risk assessment
- I13: Resource estimation

**Round 3: Final Preparation** (9 iterations)
- **Guide:** `stages/s5/s5_p3_planning_round3.md` (router, I14-I22)

**S5.P3.I1: Implementation Preparation** (I14-I19, formerly I17-I22)
- Guide: `stages/s5/s5_p3_i1_preparation.md`
- I14: Implementation order
- I15: Error handling strategy
- I16: Logging strategy
- I17: Documentation plan
- I18: Code review checklist
- I19: Rollback plan

**Validation Loop:** Added before Gate 23a (validates complete plan)

**S5.P3.I2: Pre-Implementation Audit** (I20)
- Guide: `stages/s5/s5_p3_i2_gates_part1.md`
- Gate 23a: Pre-Implementation Spec Audit (5 parts)
  - Part 1: Completeness check
  - Part 2: Consistency check
  - Part 3: Feasibility check
  - Part 4: Testability check
  - Part 5: Maintainability check

**S5.P3.I3: Final Gates** (I21-I22)
- Guide: `stages/s5/s5_p3_i3_gates_part2.md`
- I21: Gate 25 (Spec Validation Check)
- I22: Gate 24 (GO/NO-GO Decision based on confidence)

**Key Output:**
- implementation_plan.md (~400 lines) - PRIMARY reference for S6
- Includes merged test strategy from S4
- User-approved via Gate 5

**Gates:**
- Gate 4a: TODO Specification Audit (S5.P1.I2)
- Gate 7a: Backward Compatibility Check (S5.P1.I3)
- Gate 23a: Pre-Implementation Spec Audit (S5.P3.I2)
- Gate 25: Spec Validation Check (S5.P3.I3)
- Gate 24: GO/NO-GO Decision (S5.P3.I3)
- Gate 5: User approves implementation plan (MANDATORY, 3-tier rejection handling)

**Next:** S6 (Implementation Execution)

---

### S6: Implementation Execution (Detailed)

**First Action:** Use "Starting S6" prompt from `prompts_reference_v2.md`
**Guide:** `stages/s6/s6_execution.md`
**Duration:** Varies by feature complexity

**Key Actions:**
- Create implementation_checklist.md from implementation_plan.md
- Implement code following implementation_plan.md (PRIMARY reference)
- Use spec.md to verify WHAT to build (verification only)
- Update implementation_checklist.md as work progresses

**Key Principle:**
- implementation_plan.md = HOW to build (primary guide)
- spec.md = WHAT to build (verification)

**Next:** S7 (Testing & Review)

---

### S7: Implementation Testing & Review (Detailed)

**First Action:** Use "Starting S7.P1 Smoke Testing" prompt from `prompts_reference_v2.md`
**🚨 RESTART PROTOCOL:** If ANY issues found → Restart from S7.P1 (NOT mid-QC)
**Duration:** 3 phases + commit

**Phases:**

**S7.P1: Smoke Testing** (MANDATORY GATE)
- Guide: `stages/s7/s7_p1_smoke_testing.md`
- Run basic functionality tests
- If issues found → Enter debugging protocol → Fix all issues → Restart from S7.P1
- MUST pass before proceeding to QC rounds

**S7.P2: QC Rounds** (3 rounds)
- Guide: `stages/s7/s7_p2_qc_rounds.md`
- Round 1: Functional QC
- Round 2: Integration QC
- Round 3: Edge case QC
- If issues found → Enter debugging protocol → Fix all issues → Restart from S7.P1 (NOT mid-QC)

**S7.P3: Final Review**
- Guide: `stages/s7/s7_p3_final_review.md`
- PR-style review of code
- Create lessons_learned.md
- Document what worked, what didn't

**After S7.P3:**
- COMMIT FEATURE (feature-level commit)
- Use git commit protocol from CLAUDE.md

**Next:** S8 (Post-Feature Alignment)

---

### S8: Post-Feature Alignment (Detailed)

**First Action:** Use "Starting S8.P1" prompt from `prompts_reference_v2.md`
**Duration:** 2 phases

**Phases:**

**S8.P1: Cross-Feature Alignment**
- Guide: `stages/s8/s8_p1_cross_feature_alignment.md`
- Update remaining feature specs based on completed feature
- Identify conflicts or dependencies
- Adjust upcoming features as needed

**S8.P2: Epic Testing Update**
- Guide: `stages/s8/s8_p2_epic_testing_update.md`
- Reassess epic_smoke_test_plan.md
- Update based on completed feature
- Adjust integration test scenarios

**Key Actions:**
- Update remaining feature specs
- Update epic testing plan
- Ensure alignment across all features

**Next:**
- Repeat S5 for next feature
- OR S9 (if all features done)

---

### S9: Epic-Level Final QC (Detailed)

**First Action:** Use "Starting S9" prompt from `prompts_reference_v2.md`
**🚨 RESTART PROTOCOL:** If ANY issues found → Restart from S9.P1 (NOT mid-QC)
**Guide:** `stages/s9/s9_epic_final_qc.md` (router to phases)

**Phases:**

**S9.P1: Epic Smoke Testing**
- Guide: `stages/s9/s9_p1_epic_smoke_testing.md`
- Run epic-level smoke tests
- Test feature integration
- If issues found → Enter debugging protocol → Fix all issues → Restart from S9.P1

**S9.P2: Epic QC Rounds** (3 rounds)
- Guide: `stages/s9/s9_p2_epic_qc_rounds.md`
- Round 1: Epic functionality QC
- Round 2: Epic integration QC
- Round 3: Epic edge case QC
- If issues found → Enter debugging protocol → Fix all issues → Restart from S9.P1

**S9.P3: User Testing**
- Guide: `stages/s9/s9_p3_user_testing.md`
- User runs tests
- User reports bugs OR "no bugs found"
- ZERO bugs required to proceed to S10

**S9.P4: Epic Final Review**
- Guide: `stages/s9/s9_p4_epic_final_review.md`
- Review epic as a whole
- Document epic-level lessons learned
- Prepare for S10

**If Issues Found:**
- Enter debugging protocol
- Fix ALL issues
- Restart from S9.P1 (complete restart, not mid-QC)

**Next:** S10 (only when user reports ZERO bugs in S9.P3)

---

### S10: Epic Cleanup (Detailed)

**First Action:** Use "Starting S10" prompt from `prompts_reference_v2.md`
**Prerequisites:** S9 complete (user testing PASSED with ZERO bugs)
**Guide:** `stages/s10/s10_epic_cleanup.md`

**Key Actions:**

1. **Run Unit Tests** (100% pass required)
   - All tests must pass
   - No test failures allowed
   - Fix any failures before proceeding

2. **S10.P1: Guide Updates** (MANDATORY)
   - Guide: `stages/s10/s10_p1_guide_update_workflow.md`
   - Analyze lessons learned from epic
   - Create GUIDE_UPDATE_PROPOSAL.md
   - User approval required
   - Apply approved guide updates

3. **Commit Epic**
   - Create epic-level commit
   - Follow git commit protocol

4. **Create Pull Request**
   - Create PR for user review
   - User merges when ready

5. **After PR Merged:**
   - Update EPIC_TRACKER.md
   - Move epic to done/
   - Archive working files

**S10.P1 (MANDATORY):**
- Cannot skip guide update workflow
- Must analyze lessons learned
- Must propose guide improvements
- Must get user approval
- Must apply approved updates

**Next:** Epic complete!

---

**For more information:**
- Complete guide index: `README.md`
- Phase transition prompts: `prompts_reference_v2.md`
- File templates: `templates/`
- Detailed workflow spec: `PLAN.md`

**Questions or feedback?** Update `epic_lessons_learned.md` with guide improvement suggestions.

---

**END OF EPIC WORKFLOW USAGE GUIDE**
