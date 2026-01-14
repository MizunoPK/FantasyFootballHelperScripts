# Glossary - Epic-Driven Development Workflow v2

**Purpose:** Definitions of all key terms, abbreviations, and context-specific terminology used in the workflow

**Last Updated:** 2026-01-11

---

## How to Use This Glossary

Terms are organized alphabetically. Terms with multiple context-specific meanings show all contexts with clear labels.

**Notation:**
- **[Context]** indicates where term is used differently
- **See:** points to related terms
- **Guide:** references specific guide files


## Hierarchical Notation System

**The workflow uses a 4-level hierarchical notation system:**

| Level | Notation | Format | Example | Description |
|-------|----------|--------|---------|-------------|
| **Level 1** | X | Single number | `5` | Stage (top-level) |
| **Level 2** | X.Y | Two numbers | `5.1` | Phase (major subdivision) |
| **Level 3** | X.Y.Z | Three numbers | `5.1.3` | Part (focused guide) |
| **Level 4** | X.Y.Z.W | Four numbers | `5.1.3.2` | Step (detailed task) |

**Examples in practice:**
- **S5** = Feature Implementation (Level 1 - Stage)
- **S5.P1** = Implementation Planning Round 1 (Level 2 - Phase)
- **S5.P1.I2** = Iteration 2 within Round 1 (Level 3 - Iteration)

**File naming:**
- Stages: `stage_X/`
- Phases: `phase_X.Y_name.md`
- Parts: `part_X.Y.Z_name.md`
- Steps: Contained within part files

**See:** `reference/naming_standards.md` for complete specification


## A

### Acceptance Criteria
Requirements that define when a feature or task is considered complete. Documented in spec.md and used to verify implementation in S7 QC rounds.

**Example:** "Acceptance Criteria: Player scores are calculated with ADP weighting applied, ±0.1 tolerance"

**See:** Spec.md, QC Rounds

---

### ADP (Average Draft Position)
Fantasy football term for player ranking used in project examples. Not a workflow term.

---

### Agent
The Claude Code assistant executing the workflow. This glossary refers to "you" as the agent.

**See:** Agent Status, Session Compaction

---

### Agent Status
Section in EPIC_README.md and feature README.md tracking current workflow position.

**Contains:**
- Current Stage/Phase
- Current Guide being followed
- Guide Last Read timestamp
- Critical Rules from current guide
- Next Action to take

**Purpose:** Enables resumption after session compaction

**See:** Session Compaction, Resumption

**Guide:** All README.md files

---

### Algorithm Traceability Matrix
Table mapping algorithm requirements from spec.md to implementation_plan.md tasks.

**Created in:** Iteration 2 (S5 Round 1)
**Finalized in:** Iteration 19 (S5 Round 3)

**Purpose:** Ensures 100% coverage of algorithms in implementation plan

**See:** implementation_plan.md, Iteration

**Guide:** s5_p1_planning_round1.md, s5_p3_planning_round3.md

---

### Alignment
Process of ensuring consistency across features (S3) or updating specs after implementation (S8.P1).

**Two contexts:**
- **[S3]** Cross-Feature Alignment: Pairwise comparison of all feature specs
- **[S8.P1]** Post-Feature Alignment: Update remaining feature specs after one feature completes

**See:** Cross-Feature Sanity Check, Post-Feature Alignment

**Guide:** s3_cross_feature_sanity_check.md, post_feature_alignment.md

---

## B

### Bug Fix
Code correction following the bug fix workflow (S2 → S5 → S6 → S7 only).

**When used:** Bugs found during S10 user testing

**Folder structure:** `bugfix_{priority}_{name}/` inside epic folder

**Priority levels:** high, medium, low

**See:** Debugging Protocol, Missed Requirement

**Guide:** s5_bugfix_workflow.md

---

## C

### Checklist.md
**QUESTION-ONLY** format file in each feature folder where agents create questions and users provide answers.

**Created:** S1 (Epic Planning)
**Updated:** S2 (Feature Deep Dives) - agents add QUESTIONS
**User Answers:** S2 Gate 3 (MANDATORY) - user answers ALL questions
**After User Answers:** Agent updates spec.md based on answers

**🚨 CRITICAL:** Agents CANNOT mark items `[x]` autonomously - only user can answer questions

**Format:**
- Each question has: Context + User Answer (blank until user fills) + Impact on spec.md
- Agents create questions, NOT decisions
- Zero autonomous resolution allowed

**Purpose:** Capture all unknowns and decisions that require user input

**See:** Spec.md, Gate 3 (mandatory_gates.md)

---

### Code Changes
Documentation of all code modifications during implementation.

**File:** `code_changes.md` in feature folder

**Updated during:** S6 (Implementation), Debugging

**Contents:** File modified, function/method changed, reason for change, before/after state

**See:** Implementation Execution

**Guide:** implementation_execution.md

---

### Compaction
See: Session Compaction

---

### Component
**[S6 Implementation]** A logical piece of functionality implemented in a single phase.

**Example:** "Component 3: PlayerManager.calculate_score() method"

**Usage:** Tests run after EACH component (100% pass required)

**See:** Phase [Implementation]

---

### Context Window
Memory limit of the agent that can lead to session compaction.

**Mitigation:** Update Agent Status frequently, use Read tool to reload guides

**See:** Session Compaction, Agent Status

---

### Coverage
**Two contexts:**

**[Tests]** Percentage of code covered by tests
- **Required:** >90% for S5 completion
- **Measured:** Using test coverage tools

**[Traceability]** Percentage of spec requirements with TODO tasks
- **Required:** 100% for Gate 23a Part 1
- **Measured:** Count requirements vs tasks

**See:** Test Coverage, Gate 23a

---

### Critical Rules
Mandatory rules that cannot be violated, marked with 🛑 symbol in guides.

**Example:** "⚠️ RESTART from Smoke Testing Part 1 if ANY QC round finds issues"

**Context:** Each guide has stage-specific critical rules

**See:** Mandatory Gates

---

### Cross-Feature Integration
Testing how multiple features interact together.

**[S7]** Part 4 of smoke testing (feature-level, checking for conflicts)
**[S9.P1]** Part 4 of epic smoke testing (epic-level, validating workflows)

**See:** Epic Testing, Smoke Testing

**Guide:** smoke_testing.md, epic_smoke_testing.md

---

### Cross-Feature Sanity Check
S3 process of systematic pairwise comparison of all feature specs.

**Purpose:** Identify conflicts, overlaps, gaps before implementation

**See:** S3, Alignment

**Guide:** s3_cross_feature_sanity_check.md

---

## D

### Debugging Protocol
Investigation-centric workflow for resolving bugs with unknown root cause.

**Five phases:**
1. Issue Discovery & Checklist Update
2. Investigation Rounds (max 5 rounds, max 2 hours per round)
3. Root Cause Analysis
4. Fix Implementation
5. User Verification

**When used:** Issues found during Smoke Testing, QC Rounds, Epic Testing, User Testing

**Loop-back:** After resolution, restart testing from beginning

**See:** Bug Fix, Missed Requirement, ISSUES_CHECKLIST.md

**Guide:** debugging/debugging_protocol.md

---

### Decision Point
Location in workflow where path diverges based on conditions.

**Major decision points:**
- After S7: Skip S8 if last feature
- After S8.P2: Next feature or S9
- After QC failure: Restart protocol
- Iteration 24: GO vs NO-GO

**See:** Workflow Diagrams

**Guide:** workflow_diagrams.md

---

## E

### E2E (End-to-End)
Testing complete workflow from start to finish with real data.

**[Smoke Testing Part 3]** Mandatory gate before QC rounds

**[Epic Smoke Testing Part 3]** Epic-level E2E workflow

**Requirements:**
- Real data (not mocks)
- Real objects (not stubs)
- Complete workflow execution
- Output verification

**See:** Smoke Testing, Mandatory Gates

**Guide:** smoke_testing_pattern.md

---

### Edge Case
Unusual input or scenario that tests boundaries of implementation.

**Documented in:** spec.md, Iteration 5 (S5)

**Tested in:** QC Round 3 (Integration & Edge Cases)

**See:** QC Rounds

---

### Epic
Top-level work unit containing multiple related features.

**Structure:**
- `{epic_name}/` folder in feature-updates/
- Contains multiple `feature_XX_{name}/` folders
- Has EPIC_README.md, epic_smoke_test_plan.md, epic_lessons_learned.md

**Lifecycle:** Stages 1-7

**Typical size:** 3-5 features

**See:** Feature, Stage

**Guide:** s1_epic_planning.md

---

### Epic Progress Tracker
Table in EPIC_README.md tracking each feature through all stages.

**Columns:** Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2

**Symbols:**
- ✅ Complete
- 🔄 In Progress
- ◻️ Not Started

**Updated:** After each stage completes

**See:** EPIC_README.md

---

### Epic Testing
S9 process testing entire epic as cohesive system.

**Three sub-stages:**
- S9.P1: Epic Smoke Testing (4 parts)
- S9.P2: Epic QC Rounds (3 rounds)
- S9.P3: Epic Final Review

**Different from feature testing:** Tests cross-feature integration, epic-level workflows

**See:** S9, Feature Testing

**Guide:** s6_epic_final_qc.md

---

### EPIC_README.md
Main README file for epic containing:
- Agent Status
- Epic Progress Tracker
- Quick Reference Card
- Epic overview

**Updated:** After each stage completes

**Critical for:** Resumption after session compaction

**See:** Agent Status, Epic Progress Tracker

---

## F

### Feature
Individual component within an epic.

**Naming:** `feature_XX_{name}` where XX is 01, 02, 03, etc.

**Structure:**
- README.md (feature status)
- spec.md (requirements)
- implementation_plan.md (implementation plan ~400 lines)
- implementation_checklist.md (progress tracking ~50 lines)
- checklist.md (question-only format - user answers)
- code_changes.md (implementation log)
- lessons_learned.md (insights)

**Lifecycle:** S2 → S5 (S5 → S6 → S7 → S8 per feature)

**See:** Epic, S5

**Guide:** s2_feature_deep_dive.md

---

### Feature Testing
S7 process testing single feature in isolation.

**Three phases:**
- Step 1: Smoke Testing (3 parts)
- Step 2: QC Rounds (3 rounds)
- Step 3: Final Review

**Different from epic testing:** Tests feature alone, not cross-feature integration

**See:** S7, Epic Testing

**Guide:** stages/s7/s7_p1_smoke_testing.md, s7_p2_qc_rounds.md, s7_p3_final_review.md

---

## G

### Gate
Mandatory checkpoint that must PASS before proceeding.

**Two Types of Gates:**

**1. Iteration-Level Gates (part of iteration sequence):**
- **Gate 4a = Iteration 4a** - TODO Specification Audit
- **Gate 7a = Iteration 7a** - Backward Compatibility Check
- **Gate 23a = Iteration 23a** - Pre-Implementation Spec Audit (5 PARTS, 100% metrics)
- **Gate 24 = Iteration 24** - Implementation Readiness Protocol (GO/NO-GO)
- **Gate 25 = Iteration 25** - Spec Validation Against Validated Documents
- **⚠️ CRITICAL:** These ARE iterations, not additional steps. Don't count them separately.

**2. Stage-Level Gates (between stages):**
- **Gate 3:** User Checklist Approval (S2 → S3)
- **Gate 4.5:** Epic Test Plan Approval (S4 → S5)
- **Gate 5:** Implementation Plan Approval (S5 → S6)
- **Smoke Testing Part 3:** E2E Execution Test (both feature and epic)
- **User Testing:** Zero bugs required (S10)

**See:** Mandatory Gates (reference/mandatory_gates.md), Iteration

**Guide:** s5_p1_planning_round1.md, s5_p3_i2_gates_part1.md, s5_p3_i3_gates_part2.md

---

### GO Decision
Iteration 24 outcome indicating readiness to proceed to S6 implementation.

**Requirements for GO:**
- ALL checklist items ✅
- Confidence ≥ MEDIUM
- ALL mandatory gates PASSED (4a, 23a, 25)
- Integration verification complete
- Quality gates met (test coverage >90%, performance acceptable)

**If NO-GO:** Return to appropriate iteration, fix issues, re-run gates

**See:** Iteration 24, NO-GO, Gates

**Guide:** s5_p3_i3_gates_part2.md

---

### Guide Abandonment
Problem where agent stops following guide mid-stage.

**Causes:**
- Didn't use Read tool to load guide
- Assumed guide read from memory
- Skipped phase transition prompt

**Historical rate:** 40% without mandatory prompts

**Prevention:** Use Read tool, phase transition prompts, Agent Status updates

**See:** Phase Transition Prompt, Mandatory Reading Protocol

---

## H

### Hands-On Data Inspection
Process of reading actual source code to verify interfaces (not relying on memory or assumptions).

**Used in:**
- Iteration 8 (Interface Contracts)
- Iteration 21 (Mock Audit)
- Gate 23a Part 3 (Interface Contracts Audit)

**Critical rule:** ALWAYS read source files, never assume

**See:** Interface Verification

**Guide:** hands_on_data_inspection.md

---

## I

### Implementation Execution
S6 process of writing feature code following implementation_plan.md.

**Key requirements:**
- Interface verification FIRST (before writing any code)
- Keep spec.md VISIBLE at all times
- Run tests after EACH phase (100% pass required)
- Mini-QC checkpoints every 5-7 tasks
- Update code_changes.md in real-time
- Update implementation_checklist.md in real-time

**Typical time:** 1-4 hours per feature

**See:** S6, implementation_plan.md

**Guide:** implementation_execution.md

---

### Implementation Phasing
Iteration 17 process of breaking implementation into incremental phases for validation.

**Typical phases:** 5-6 phases per feature

**Example phases:**
1. Data structures and models
2. Core algorithm implementation
3. Integration points
4. Error handling
5. Edge case handling
6. Tests and validation

**Purpose:** Allows testing after each step (catch bugs early)

**See:** Iteration 17, S6

**Guide:** s5_p3_planning_round3.md

---

### Integration Point
Location where features or components interact.

**Documented in:**
- Iteration 9 (S5 Round 2)
- S8.P1 (Post-Feature Alignment)
- S8.P2 (Testing Plan Update)

**Tested in:**
- QC Round 3 (Integration & Edge Cases)
- Epic Smoke Testing Part 4 (Cross-Feature Integration)

**See:** Cross-Feature Integration

---

### Integration Verification
Process ensuring all new methods/functions have identified callers (no orphan code).

**Performed in:**
- Iteration 9 (Integration Points Identification)
- Iteration 23 (Integration Gap Check - Final)

**Critical for:** Preventing unused code, ensuring complete workflows

**See:** Iteration 23

**Guide:** s5_p3_i2_gates_part1.md

---

### Interface Contracts
Agreements defining method signatures, parameters, return types.

**Verified in:**
- Iteration 8 (Interface Contracts)
- Gate 23a Part 3 (Interface Contracts Audit)
- S6 before implementation (Interface Verification First)

**Critical rule:** Read source code to verify (never assume)

**See:** Hands-On Data Inspection

**Guide:** s5_p2_planning_round2.md, s5_p3_i2_gates_part1.md

---

### ISSUES_CHECKLIST.md
Central tracking file for all discovered issues during debugging.

**Location:**
- Feature-level: `feature_XX_{name}/debugging/ISSUES_CHECKLIST.md`
- Epic-level: `{epic_name}/debugging/ISSUES_CHECKLIST.md`

**Statuses:**
- 🔴 CRITICAL (blocks functionality)
- 🟡 MAJOR (significant impact)
- 🟢 MINOR (low impact)
- 🟢 FIXED (user verified)

**See:** Debugging Protocol

**Guide:** debugging/debugging_protocol.md

---

### Iteration
**[S5]** Single verification step in TODO Creation process.

**Total:** 28 iterations across 3 rounds
- **Round 1:** Iterations 1-7 + Gate 4a + Gate 7a (9 iterations)
- **Round 2:** Iterations 8-16 (9 iterations)
- **Round 3:** Iterations 17-25 (includes Gates 23a, 24, 25) (10 iterations)

**Iteration Numbering with Letter Suffixes:**
- **Letter suffix (4a, 5a, 7a, 23a):** Indicates a gate checkpoint or critical sub-iteration
- **Examples:**
  - Iteration 5a: Downstream Consumption Tracing (critical sub-step after Iteration 5)
  - Iteration 4a: Gate checkpoint for TODO Specification Audit
  - Iteration 7a: Gate checkpoint for Backward Compatibility
  - Iteration 23a: Gate checkpoint for Pre-Implementation Spec Audit
- **Numbering:** Iterations with "a" suffix occur BETWEEN base iterations or AS gate checkpoints within iterations

**All iterations mandatory** - skipping not allowed

**See:** Round, S5, Gate

**Guide:** s5_p1_planning_round1.md, s5_p2_planning_round2.md, s5_p3_planning_round3.md, s5_p3_i2_gates_part1.md, s5_p3_i3_gates_part2.md

---

## L

### Lessons Learned
Insights and improvements documented after feature or epic completion.

**Files:**
- `feature_XX_{name}/lessons_learned.md` (per feature)
- `{epic_name}/epic_lessons_learned.md` (epic-level)

**Updated:** S7 Phase 3 (Final Review), S9.P3 (Epic Final Review)

**Contents:**
- What worked well
- What didn't work
- Improvements for future epics
- Guide updates needed

**See:** Final Review

**Guide:** final_review.md, epic_final_review.md

---

### Loop-Back
Workflow pattern where issues force restart of testing.

**Examples:**
- Issues in Smoke Testing → Fix → Restart Smoke Testing Part 1
- Issues in QC Rounds → Fix → Restart Smoke Testing Part 1 (not QC Round 1)
- Issues in Epic Testing → Fix → Restart S9.P1 Part 1
- User Testing finds bugs → Fix → Restart S9 (not S10)

**Principle:** Always restart from BEGINNING of testing after fixes

**See:** Debugging Protocol, Restart Protocol

**Guide:** debugging/debugging_protocol.md, workflow_diagrams.md

---

## M

### Mandatory Gates
Checkpoints that CANNOT be skipped and must PASS before proceeding.

**All mandatory gates:**
1. Gate 4a: TODO Specification Audit (S5 Round 1)
2. Gate 23a: Pre-Implementation Spec Audit - 4 PARTS (S5 Round 3)
3. Gate 25: Spec Validation Against Validated Documents (S5 Round 3)
4. Gate 24: Implementation Readiness (GO/NO-GO) (S5 Round 3)
5. Smoke Testing Part 3: E2E Execution (S7, S9.P1)
6. User Testing: ZERO bugs required (S10)

**See:** Gates, Critical Rules

---

### Mandatory Reading Protocol
Required process before starting any stage/phase.

**Steps:**
1. Use Read tool to load ENTIRE guide
2. Use phase transition prompt
3. Acknowledge requirements
4. Update Agent Status
5. THEN proceed

**Purpose:** Prevents guide abandonment (40% abandonment rate without prompts)

**See:** Phase Transition Prompt, Guide Abandonment

---

### Mini-QC Checkpoint
Lightweight validation during S6 implementation.

**Frequency:** Every 5-7 TODO items

**Checks:**
- Spec requirement addressed correctly
- Code matches TODO task description
- No obvious bugs introduced

**See:** Implementation Execution

**Guide:** implementation_execution.md

---

### Missed Requirement
Functionality that was NOT in spec.md but should have been.

**Different from bug:** Bug = spec was correct, implementation wrong. Missed req = spec was incomplete.

**Workflow:** debugging/missed_requirement_workflow.md

**Decision threshold:**
- ≤3 tasks needed → Add to TODO, implement, continue
- >3 tasks needed → Return to S5 Round 3

**See:** Bug Fix, Debugging Protocol

**Guide:** missed_requirement_workflow.md

---

### Mock
Test double that simulates real object behavior.

**Audited in:** Iteration 21 (Mock Audit & Integration Test Plan)

**Critical rule:** Mocks must match REAL interfaces (verify from source code)

**See:** Integration Test, Iteration 21

**Guide:** s5_p3_planning_round3.md

---

## N

### NO-GO Decision
Iteration 24 outcome indicating NOT ready to proceed to S6.

**Causes:**
- Confidence < MEDIUM
- Gate 4a failed
- Gate 23a failed (any of 4 parts <100%)
- Gate 25 failed (discrepancies found)
- Integration verification incomplete
- Quality gates not met

**Action:** Return to appropriate iteration, fix issues, re-run gates

**See:** GO Decision, Iteration 24

**Guide:** s5_p3_i3_gates_part2.md

---

## O

### Orchestration
**[Implementation]** Coordinating the complete feature lifecycle (S6 → S7 → S8).

**See:** Implementation Orchestration Guide

**Guide:** implementation_orchestration.md

---

## P

### Pattern
**[Guides]** Extracted common content referenced by multiple guides.

**Examples:**
- smoke_testing_pattern.md (3-4 part smoke testing workflow)
- qc_rounds_pattern.md (3-round QC workflow)

**Purpose:** Single source of truth, reduce duplication

**See:** Reference

**Guide:** smoke_testing_pattern.md, qc_rounds_pattern.md

---

### Phase
**[Multiple contexts - OVERLOADED TERM]** Term for distinct sections within a stage/round.

**⚠️ IMPORTANT:** Always qualify "Phase" with stage name to avoid ambiguity.
- ✅ CORRECT: "S2.P1", "S10.P2", "Debugging Phase 3"
- ❌ AMBIGUOUS: "Phase 3" (could mean S2.P3, S10.P3, or Debugging Phase 3)

**Context-Specific Definitions:**

| Context | Number of Phases | Phase Names | Notes |
|---------|------------------|-------------|-------|
| **S2** | 3 | S2.P1 (Research)<br>S2.P2 (Specification)<br>S2.P3 (Refinement) | Level 2 workflow divisions |
| **S6** | 5-6 | Data structures → Core algorithm → Integration → Error handling → Edge cases → Tests | Implementation sequence |
| **S7** | 3 | S7.P1<br>S7.P2<br>S7.P3 | Post-implementation validation |
| **Debugging** | 5 | Phase 1 (Issue Discovery)<br>Phase 2 (Investigation)<br>Phase 3 (Solution Design)<br>Phase 4 (User Verification)<br>Phase 5 (Loop Back) | Debugging protocol steps |

**See:** Stage, Part, Round, Iteration

---

### Phase Transition Prompt
Mandatory acknowledgment prompt used when transitioning between stages/phases.

**Location:** prompts_reference_v2.md (router), prompts/*.md (actual prompts)

**Examples:**
- "Starting S1" prompt
- "Starting S5 Round 1" prompt
- "Resuming In-Progress Epic" prompt

**Format:**
1. Read guide
2. Acknowledge what guide requires
3. List critical rules
4. Update Agent Status
5. Proceed

**Purpose:** Prevents guide abandonment (40% rate without prompts)

**See:** Mandatory Reading Protocol

**Guide:** prompts_reference_v2.md

---

### Post-Feature Alignment
S8.P1 process of updating remaining feature specs after completing one feature.

**Purpose:** Incorporate insights from ACTUAL implementation (not plans)

**Skipped if:** Completed feature was the LAST feature (no specs to update)

**See:** S8.P1, Alignment

**Guide:** post_feature_alignment.md

---

### Post-Implementation
S7 process of validating implemented feature.

**Three phases:**
1. Smoke Testing (3 parts, Part 3 is mandatory gate)
2. QC Rounds (3 rounds)
3. Final Review

**Restart protocol:** ANY issues = restart from Smoke Testing Part 1

**See:** S7, Feature Testing

**Guide:** stages/s5/ (smoke_testing.md, qc_rounds.md, final_review.md)

---

### PR Review
Pull Request review (7 categories) in S7 Phase 3 Final Review.

**Categories:**
1. Code quality
2. Test coverage
3. Documentation
4. Error handling
5. Performance
6. Security
7. Maintainability

**See:** Final Review

**Guide:** final_review.md

---

## Q

### QC (Quality Control) Rounds
**[Two contexts]**

**[S7 - Feature QC]** Three rounds testing single feature:
- Round 1: Algorithm Verification (spec vs code line-by-line)
- Round 2: Consistency & Standards (coding standards, error handling)
- Round 3: Integration & Edge Cases (integration points, edge cases)

**[S9.P2 - Epic QC]** Three rounds testing entire epic:
- Round 1: Epic Algorithm Verification (epic requirements vs implementation)
- Round 2: Epic Consistency & Standards (cross-feature consistency)
- Round 3: Epic Integration & Success Criteria (epic success criteria met)

**Restart protocol:** Issues in ANY round = restart from smoke testing (not Round 1)

**See:** S7, S9.P2, Round

**Guide:** qc_rounds.md (feature), epic_qc_rounds.md (epic)

---

### Quick Reference Card
Summary section in EPIC_README.md showing current epic status at a glance.

**Contains:**
- Epic name and description
- Total features
- Current stage
- Features completed vs remaining
- Next action

**See:** EPIC_README.md

---

## R

### README.md
**[Two contexts]**

**[Epic-level]** EPIC_README.md containing:
- Agent Status
- Epic Progress Tracker
- Quick Reference Card

**[Feature-level]** feature_XX_{name}/README.md containing:
- Feature status
- Current guide
- Implementation progress

**Updated:** After each major stage/sub-stage

**See:** EPIC_README.md, Agent Status

---

### Reference
**[Guides]** Supporting materials in reference/ folder.

**Types:**
- Patterns (smoke_testing_pattern.md, qc_rounds_pattern.md)
- Reference cards (stage_1_reference_card.md, etc.)
- Orchestration guides (implementation_orchestration.md)
- Supporting materials (hands_on_data_inspection.md, spec_validation.md)

**Purpose:** Extracted common content, quick reference

**See:** Pattern

---

### Restart Protocol
Rules for when to restart testing after finding issues.

**Key principle:** Always restart from BEGINNING of testing (not from where issue found)

**Examples:**
- Issues in Smoke Part 3 → Restart Smoke Part 1
- Issues in QC Round 2 → Restart Smoke Part 1 (NOT QC Round 1)
- Issues in Epic QC → Restart S9.P1 Part 1
- User finds bugs → Fix, then restart S9 (NOT S10)

**See:** Loop-Back, Debugging Protocol

**Guide:** workflow_diagrams.md

---

### Resumption
Process of continuing work after session compaction.

**Steps:**
1. Read EPIC_README.md Agent Status
2. Use "Resuming In-Progress Epic" prompt
3. Read current guide
4. Continue from "Next Action"

**Critical for:** Context window recovery

**See:** Session Compaction, Agent Status

**Guide:** prompts/special_workflows_prompts.md

---

### Round
**[Two contexts]**

**[S5 TODO Creation]** Collection of iterations:
- Round 1: Iterations 1-7 + Gate 4a (Initial TODO)
- Round 2: Iterations 8-16 (Integration Verification)
- Round 3: Iterations 17-24 (Preparation + Gates)

**[QC Rounds]** Quality control verification rounds:
- Round 1: Algorithm Verification
- Round 2: Consistency & Standards
- Round 3: Integration & Edge Cases (or Success Criteria for epic)

**See:** Iteration, Phase, QC Rounds

---

## S

### Session Compaction
Context window limit forcing conversation summarization.

**Effect:** Loses immediate context but preserves Agent Status

**Mitigation:**
- Update Agent Status frequently
- Keep "Next Action" specific
- Use Read tool to reload guides after resumption

**See:** Agent Status, Resumption

---

### Smoke Testing
**[Two contexts]**

**[S7 - Feature Smoke Testing]** Three parts:
- Part 1: Import Test
- Part 2: Entry Point Test
- Part 3: E2E Execution Test (MANDATORY GATE)

**[S9.P1 - Epic Smoke Testing]** Four parts:
- Part 1-3: Same as feature
- Part 4: Cross-Feature Integration (epic-specific)

**Restart rule:** Failure in ANY part = restart from Part 1

**See:** E2E, S7, S9.P1

**Guide:** smoke_testing.md (feature), epic_smoke_testing.md (epic)

---

### Spec.md
Specification document in each feature folder containing all requirements.

**Created:** S2 (Feature Deep Dives)
**Updated:** Throughout S2 as requirements clarified
**Used during:** S6 (implementation reference), S7 (QC verification)

**Sections:**
- Feature Overview
- Requirements (numbered for traceability)
- Edge Cases
- Integration Points
- Acceptance Criteria
- Updates History

**See:** Feature, Checklist.md

**Guide:** s2_feature_deep_dive.md

---

### Spec Validation
**[Gate 25 Iteration 25]** Three-way validation of spec.md against validated documents.

**Three validated sources:**
1. Epic notes (user's original request in {epic_name}.txt)
2. Epic ticket (user-validated outcomes from S1)
3. Spec summary (user-validated feature outcomes from S2)

**Critical rule:** Close spec.md before reading validated docs (avoid confirmation bias)

**Purpose:** Prevents catastrophic bugs (Feature 02 bug: spec misinterpreted epic notes)

**See:** Gate 25, Iteration 25

**Guide:** s5_p3_i3_gates_part2.md, spec_validation.md

---

### Stage
Top-level workflow division. 7 stages total:
1. Epic Planning
2. Feature Deep Dives (per feature)
3. Cross-Feature Sanity Check
4. Epic Testing Strategy
5. Feature Implementation (S5 → S6 → S7 → S8 per feature)
6. Epic-Level Final QC
7. Epic Cleanup

**All stages mandatory** - cannot skip

**See:** Epic, Feature

**Guide:** README.md (guide index)

---

### S5 Sub-Stages
S5 (Feature Implementation) has 5 sub-stages per feature:
- **5a:** TODO Creation (28 iterations across 3 rounds)
- **5b:** Implementation Execution (write code)
- **5c:** Post-Implementation (smoke testing + QC rounds + final review)
- **5d:** Post-Feature Alignment (update remaining feature specs) - skip if last feature
- **5e:** Testing Plan Update (update epic_smoke_test_plan.md) - skip if last feature

**Loop:** Repeat S5 → S6 → S7 → S8 for EACH feature

**See:** S5, Feature

**Guide:** stages/s5/ folder

---

## T

### implementation_plan.md
Implementation plan (~400 lines) in each feature folder containing comprehensive build guide.

**Created:** S5 (Implementation Planning - 28 iterations across 3 rounds)
**User-Approved:** After S5 (MANDATORY Gate 5)
**Used:** S6 (Implementation Execution - PRIMARY reference)

**Structure:**
- Phased implementation (5-6 phases)
- Implementation tasks with acceptance criteria
- Dependencies documented
- Test strategy (>90% coverage required)
- Integration points
- Performance considerations
- Rollback strategy

**See:** S5, Implementation Execution, implementation_checklist.md

**Guide:** s5_p1_planning_round1.md, s5_p2_planning_round2.md, round3 guides

---

### Traceability
**[Multiple contexts]**

**[Algorithm Traceability]** Mapping algorithms from spec to TODO tasks
- Created: Iteration 2
- Finalized: Iteration 19

**[Spec Traceability]** Mapping requirements to implementation
- Via checklist.md
- Verified in QC Round 1

**Purpose:** Ensure 100% requirement coverage

**See:** Algorithm Traceability Matrix, Checklist.md

---

## U

### User Testing
S10 mandatory testing by the user before commit.

**Requirements:**
- ZERO bugs found
- 100% unit test pass rate
- User approval explicit

**If bugs found:**
- Document in epic debugging/ISSUES_CHECKLIST.md
- Fix ALL bugs
- Restart S9 (not S10)
- Return to user testing
- Repeat until zero bugs

**See:** S10, Mandatory Gates

**Guide:** s7_epic_cleanup.md

---

## V

### Validation
**[Multiple contexts]**

**[Spec Validation]** Gate 25 - three-way validation against epic notes, epic ticket, spec summary

**[Data Validation]** Iteration 7 - planning data validation strategies

**[Output Validation]** Iteration 22 - verify outputs match consumer expectations

**See:** Spec Validation, Gates

---

## W

### Workflow
**[General]** The Epic-Driven Development v2 process (Stages 1-7)

**[Sub-workflows]** Specialized processes:
- Debugging Protocol
- Missed Requirement Workflow
- Bug Fix Workflow

**See:** Stage, Debugging Protocol

**Guide:** README.md, EPIC_WORKFLOW_USAGE.md

---

### Workflow Selection
Decision process for choosing which workflow to use.

**Decision tree:**
- Unknown root cause → Debugging Protocol
- Known solution, NOT in spec → Missed Requirement Workflow
- Bug found in S10 → Bug Fix Workflow
- New epic → Regular workflow (Stages 1-7)

**See:** Debugging Protocol, Missed Requirement

**Guide:** faq_troubleshooting.md

---

## Z

### Zero Tech Debt Tolerance
Principle that ALL issues must be fixed immediately (no deferrals).

**Applied in:**
- S7 QC Rounds (no "we'll fix it later")
- S9 Epic QC (no skipping issues)
- S10 User Testing (ZERO bugs required)

**Rationale:** Technical debt compounds, fixing now is faster than fixing later

**See:** Critical Rules

---

## Abbreviations

- **ADP:** Average Draft Position (fantasy football term, not workflow)
- **E2E:** End-to-End
- **PR:** Pull Request
- **QC:** Quality Control

---

## Cross-References by Guide

**For S1:**
- Epic, EPIC_README.md, Feature, Agent Status

**For S2:**
- Feature, Spec.md, Checklist.md, Phase [S2]

**For S3:**
- Alignment [S3], Cross-Feature Sanity Check

**For S4:**
- Epic Testing, Integration Point

**For S5:**
- Round, Iteration, implementation_plan.md, Gates, GO Decision, NO-GO Decision
- Algorithm Traceability Matrix, Spec Validation

**For S6:**
- Implementation Execution, Component, Phase [Implementation], Mini-QC Checkpoint

**For S7:**
- Post-Implementation, Smoke Testing, QC Rounds, E2E, PR Review

**For S8.P1:**
- Post-Feature Alignment, Alignment [S8.P1]

**For S8.P2:**
- Testing Plan Update, Integration Point

**For S9:**
- Epic Testing, Smoke Testing [Epic], QC Rounds [Epic]

**For S10:**
- User Testing, Bug Fix, Mandatory Gates

**For Debugging:**
- Debugging Protocol, ISSUES_CHECKLIST.md, Loop-Back, Restart Protocol

**For Missed Requirements:**
- Missed Requirement, Workflow Selection

**For Session Management:**
- Session Compaction, Resumption, Agent Status, Context Window

---

**Last Updated:** 2026-01-11

**See Also:**
- `reference/faq_troubleshooting.md` - Common questions and troubleshooting
- `reference/workflow_diagrams.md` - Workflow reference diagrams
- `diagrams/workflow_diagrams.md` - Visual workflow diagrams (ASCII art)
- `README.md` - Complete guide index
- `reference/naming_conventions.md` - File naming and notation rules


---

## Deprecated Terms (Old Notation → New Notation)

**The following terms were used before 2026-01-10 and have been replaced:**

### Old Stage Notation

| Deprecated | Current | Description |
|------------|---------|-------------|
| STAGE_2a | S2.P1 | Research Phase |
| STAGE_2b | S2.P2 | Specification Phase |
| STAGE_2c | S2.P3 | Refinement Phase |
| STAGE_5a | S5 | Implementation Planning (28 iterations) |
| STAGE_5b | S6 | Implementation Execution |
| STAGE_5c | S7 | Implementation Testing & Review |
| STAGE_5d | S8.P1 | Cross-Feature Alignment |
| STAGE_5e | S8.P2 | Epic Testing Plan Update |
| S9a | S9.P1 | Epic Smoke Testing |
| S9b | S9.P2 | Epic QC Rounds |
| S9c | S9.P3 | User Testing |
| S9d | S9.P4 | Epic Final Review |

### Old File Names

| Deprecated | Current | Description |
|------------|---------|-------------|
| phase_0_research.md | s2_p1_research.md | S2 Research |
| phase_1_specification.md | s2_p2_specification.md | S2 Specification |
| phase_2_refinement.md | s2_p3_refinement.md | S2 Refinement |
| round1_todo_creation.md | s5_p1_planning_round1.md | Round 1 guide |
| round2_todo_creation.md | s5_p2_planning_round2.md | Round 2 guide |
| round3_part1_preparation.md | s5_p3_planning_round3.md | Round 3 router |
| round3_part2a_gates_1_2.md | s5_p3_i2_gates_part1.md | Round 3 Part 2a |
| round3_part2b_gate_3.md | s5_p3_i3_gates_part2.md | Round 3 Part 2b |
| implementation_execution.md | s6_execution.md | Implementation guide |
| smoke_testing.md | s7_p1_smoke_testing.md | Smoke testing |
| qc_rounds.md | s7_p2_qc_rounds.md | QC rounds |
| final_review.md | s7_p3_final_review.md | Final review |
| post_feature_alignment.md | s8_p1_cross_feature_alignment.md | Cross-feature alignment |
| epic_testing_plan_update.md | s8_p2_epic_testing_update.md | Epic testing update |
| epic_smoke_testing.md | s9_p1_epic_smoke_testing.md | Epic smoke tests |
| epic_qc_rounds.md | s9_p2_epic_qc_rounds.md | Epic QC |
| user_testing.md | s9_p3_user_testing.md | User testing |
| epic_final_review.md | s9_p4_epic_final_review.md | Epic final review |
| epic_cleanup.md | s10_epic_cleanup.md | Epic cleanup |
| guide_update_workflow.md | s10_p1_guide_update_workflow.md | Guide updates |

**Note:** If you encounter old notation in conversation summaries or older documentation, always use the current notation shown above.

**See:** `reference/naming_standards.md` for migration guidance

---

