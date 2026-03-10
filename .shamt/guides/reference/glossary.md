# Glossary - Epic-Driven Development Workflow v2

**Purpose:** Definitions of all key terms, abbreviations, and context-specific terminology used in the workflow

**Last Updated:** 2026-01-20

---

## Table of Contents

1. [How to Use This Glossary](#how-to-use-this-glossary)
2. [Hierarchical Notation System](#hierarchical-notation-system)
3. [A](#a)
4. [P](#p)
5. [W](#w)

---

## How to Use This Glossary

Terms are organized alphabetically. Terms with multiple context-specific meanings show all contexts with clear labels.

## Hierarchical Notation System

**The workflow uses a 3-level hierarchical S#.P#.I# notation system:**

| Level | Notation | Prefix | Example | Description | Term |
|-------|----------|--------|---------|-------------|------|
| **Level 1** | S# | S | `S5` | Top-level workflow stage | **Stage** |
| **Level 2** | S#.P# | P | `S5.P1` | Major subdivision within stage | **Phase** |
| **Level 3** | S#.P#.I# | I | `S5.P1.I2` | Specific iteration/task within phase | **Iteration** |

**Within files (not part of file hierarchy):**
- **Steps** — Numbered tasks within a guide (Step 1, Step 2, etc.)

**Examples in practice:**
- **S5** = Feature Implementation (Level 1 - Stage)
- **S5.P1** = Implementation Planning Round 1 (Level 2 - Phase)
- **S5.P1.I2** = Iteration 2 within Round 1 (Level 3 - Iteration)

**File naming:**
- Stages: `s{N}/` (e.g., `s1/`, `s5/`)
- Phases: `s{N}_p{M}_{name}.md` (e.g., `s8_p1_cross_feature_alignment.md`)
- Iterations: `s{N}_p{M}_i{K}_{name}.md` (e.g., `s5_p1_i2_validation.md`)

**See:** `reference/naming_conventions.md` for complete specification

## A
### Acceptance Criteria
Requirements that define when a feature or task is considered complete. Documented in spec.md and used to verify implementation in S7 Validation Loop.

**See:** Spec.md, Validation Loop

---

### rank (external rank priority)
External rank priority term used in project examples. Not a workflow term.

---

### Agent
The Claude Code assistant executing the workflow. This glossary refers to "you" as the agent.

**See:** Agent Status, Session Compaction

---

### Agent Status
Section in EPIC_README.md and feature README.md tracking current workflow position.

**See:** Session Compaction, Resumption

**Guide:** All README.md files

---

### Algorithm Traceability Matrix
Table mapping algorithm requirements from spec.md to implementation_plan.md tasks.

**See:** implementation_plan.md, Iteration

**Guide:** stages/s5/s5_v2_validation_loop.md, stages/s5/s5_v2_validation_loop.md (Validation Loop Round 3)

---

### Alignment
Process of ensuring consistency across features (S2.P2: cross-feature alignment) or updating specs after implementation (S8.P1). S3 does epic-level test planning and approval (Gate 4.5) after S2.P2 alignment is complete.

**See:** Cross-Feature Sanity Check, Post-Feature Alignment

**Guide:** stages/s3/s3_epic_planning_approval.md, stages/s8/s8_p1_cross_feature_alignment.md

---

### Bug Fix
Code correction following the bug fix workflow (S2 → S5 → S6 → S7 only).

**See:** Debugging Protocol, Missed Requirement

**Guide:** stages/s5/s5_bugfix_workflow.md

---

### Checklist.md

**🚨 CRITICAL:** Agents CANNOT mark items `[x]` autonomously - only user can answer questions

**See:** Spec.md, Gate 3 (mandatory_gates.md)

---

### Compaction
See: Session Compaction

---

### Component

**[S6 Implementation]** A logical piece of functionality implemented in a single phase.

**See:** Phase [Implementation]

---

### Context Window
Memory limit of the agent that can lead to session compaction.

**See:** Session Compaction, Agent Status

---

### Coverage

**[Tests]** Percentage of code covered by tests

- **Required:** >90% for S5 completion

- **Measured:** Using test coverage tools

**[Traceability]** Percentage of spec requirements with TODO tasks

- **Required:** 100% for Gate 23a Part 1

**See:** Test Coverage, Gate 23a

---

### Critical Rules
Mandatory rules that cannot be violated, marked with 🛑 symbol in guides.

**See:** Mandatory Gates

---

### Cross-Feature Integration
Testing how multiple features interact together.

**[S7]** Part 4 of smoke testing (feature-level, checking for conflicts)

**[S9.P1]** Part 4 of epic smoke testing (epic-level, validating workflows)

**See:** Epic Testing, Smoke Testing

**Guide:** stages/s7/s7_p1_smoke_testing.md, stages/s9/s9_p1_epic_smoke_testing.md

---

### Cross-Feature Sanity Check
S3 process of validating epic-level consistency across all feature specs. Note: Pairwise comparison of feature specs is performed in S2.P2 (moved from old S3). S3 focuses on epic-level testing strategy, documentation, and user approval (Gate 4.5).

**See:** S3, Alignment

**Guide:** stages/s3/s3_epic_planning_approval.md

---

### Debugging Protocol
Investigation-centric workflow for resolving bugs with unknown root cause.

**See:** Bug Fix, Missed Requirement, ISSUES_CHECKLIST.md

**Guide:** debugging/debugging_protocol.md

---

### Discovery Context
Section at the beginning of each feature spec.md that references DISCOVERY.md.

**See:** DISCOVERY.md, Spec.md, Discovery Phase

**Guide:** templates/feature_spec_template.md

---

### Discovery Loop
Iterative research process within S1.P3 Discovery Phase.

**See:** Discovery Phase, DISCOVERY.md

**Guide:** stages/s1/s1_p3_discovery_phase.md

---

### Discovery Phase
S1.P3 - MANDATORY phase for exploring epic problem space before feature breakdown.

**See:** DISCOVERY.md, Discovery Loop, Discovery Context

**Guide:** stages/s1/s1_p3_discovery_phase.md

---

### DISCOVERY.md
Epic-level source of truth document created during S1.P3 Discovery Phase.

**See:** Discovery Phase, Discovery Context

**Guide:** templates/discovery_template.md, stages/s1/s1_p3_discovery_phase.md

---

### Decision Point
Location in workflow where path diverges based on conditions.

**See:** EPIC_WORKFLOW_USAGE.md → "Workflow Stages" (stage flow diagrams)

---

### E2E (End-to-End)
Testing complete workflow from start to finish with real data.

**[Smoke Testing Part 3]** Mandatory gate before QC rounds

**[Epic Smoke Testing Part 3]** Epic-level E2E workflow

**See:** Smoke Testing, Mandatory Gates

**Guide:** reference/smoke_testing_pattern.md

---

### Edge Case
Unusual input or scenario that tests boundaries of implementation.

**See:** Validation Loop

---

### Epic
Top-level work unit containing multiple related features.

**See:** Feature, Stage

**Guide:** stages/s1/s1_epic_planning.md

---

### Epic Progress Tracker
Table in EPIC_README.md tracking each feature through all stages.

**See:** EPIC_README.md

---

### Epic Testing
S9 process testing entire epic as cohesive system.

**See:** S9, Feature Testing

**Guide:** stages/s9/s9_epic_final_qc.md

---

### EPIC_README.md
Main README file for epic containing:

**See:** Agent Status, Epic Progress Tracker

---

### Feature
Individual component within an epic.

**See:** Epic, S5

**Guide:** stages/s2/s2_feature_deep_dive.md

---

### Feature Testing
S7 process testing single feature in isolation.

**See:** S7, Epic Testing

**Guide:** stages/s7/s7_p1_smoke_testing.md, stages/s7/s7_p2_qc_rounds.md, stages/s7/s7_p3_final_review.md

---

### Gate
Mandatory checkpoint that must PASS before proceeding.

**See:** Mandatory Gates (reference/mandatory_gates.md), Iteration

**Guide:** stages/s5/s5_v2_validation_loop.md, stages/s5/s5_v2_validation_loop.md (Dimension 11: Gate 23a), stages/s5/s5_v2_validation_loop.md (Dimensions 10, 11: Gates 24, 25)

---

### GO Decision
S5 v2 Phase 2 complete - indicates readiness to proceed to S6 implementation after achieving 3 consecutive clean validation rounds across all 11 dimensions.

**See:** S5 v2 Validation Loop, Phase 2, NO-GO, 3 Consecutive Clean Rounds

**Guide:** stages/s5/s5_v2_validation_loop.md (Dimension 10: Implementation Readiness)

---

### Guide Abandonment
Problem where agent stops following guide mid-stage.

**See:** Phase Transition Prompt, Mandatory Reading Protocol

---

### Hands-On Data Inspection
Process of reading actual source code to verify interfaces (not relying on memory or assumptions).

**See:** Interface Verification

**Guide:** reference/hands_on_data_inspection.md

---

### Implementation Execution
S6 process of writing feature code following implementation_plan.md.

**See:** S6, implementation_plan.md

**Guide:** stages/s6/s6_execution.md

---

### Implementation Phasing
Iteration 17 process of breaking implementation into incremental phases for validation.

**See:** Iteration 17, S6

**Guide:** stages/s5/s5_v2_validation_loop.md (Validation Loop Round 3)

---

### Integration Point
Location where features or components interact.

**See:** Cross-Feature Integration

---

### Integration Verification
Process ensuring all new methods/functions have identified callers (no orphan code).

**See:** Iteration 23

**Guide:** stages/s5/s5_v2_validation_loop.md (Dimension 11: Gate 23a)

---

### Interface Contracts
Agreements defining method signatures, parameters, return types.

**See:** Hands-On Data Inspection

**Guide:** stages/s5/s5_v2_validation_loop.md, stages/s5/s5_v2_validation_loop.md (Dimension 11: Gate 23a)

---

### ISSUES_CHECKLIST.md
Central tracking file for all discovered issues during debugging.

**See:** Debugging Protocol

**Guide:** debugging/debugging_protocol.md

---

### Iteration

**[S5]** Not used in S5 v2 (replaced by Validation Loop dimensions).

**Historical Context (S5 v1):**
- S5 v1 had 22 iterations across 3 rounds
- S5 v2 uses 11 dimensions in Validation Loop instead

**See:** Dimension, Validation Loop, S5

**Guide:** stages/s5/s5_v2_validation_loop.md, stages/s5/s5_v2_validation_loop.md, stages/s5/s5_v2_validation_loop.md (Validation Loop Round 3), stages/s5/s5_v2_validation_loop.md (Dimension 11: Gate 23a), stages/s5/s5_v2_validation_loop.md (Dimensions 10, 11: Gates 24, 25)

---

### Lessons Learned
Insights and improvements documented after feature or epic completion.

**See:** Final Review

**Guide:** stages/s7/s7_p3_final_review.md, stages/s9/s9_p4_epic_final_review.md

---

### Loop-Back
Workflow pattern where issues force restart of testing.

**See:** Debugging Protocol, Restart Protocol

**Guide:** debugging/debugging_protocol.md

---

### Mandatory Gates
Checkpoints that CANNOT be skipped and must PASS before proceeding.

**See:** Gates, Critical Rules

---

### Mandatory Reading Protocol
Required process before starting any stage/phase.

**See:** Phase Transition Prompt, Guide Abandonment

---

### Mini-QC Checkpoint
Lightweight validation during S6 implementation.

**See:** Implementation Execution

**Guide:** stages/s6/s6_execution.md

---

### Missed Requirement
Functionality that was NOT in spec.md but should have been.

**See:** Bug Fix, Debugging Protocol

**Guide:** missed_requirement/missed_requirement_protocol.md

---

### Mock
Test double that simulates real object behavior.

**See:** Integration Test, Dimension 11

**Guide:** stages/s5/s5_v2_validation_loop.md (Validation Loop Round 3)

---

### NO-GO Decision
S5 v2 Validation Loop not converging - indicates NOT ready to proceed to S6. Occurs when unable to achieve 3 consecutive clean rounds within 10 rounds, or when critical dimensions repeatedly fail.

**See:** GO Decision, S5 v2 Validation Loop, Escalation Protocol

**Guide:** stages/s5/s5_v2_validation_loop.md (Special Cases: "If Validation Loop Exceeds 10 Rounds")

---

### Orchestration

**[Implementation]** Coordinating the complete feature lifecycle (S6 → S7 → S8).

**See:** Implementation Orchestration Guide

**Guide:** reference/implementation_orchestration.md

---

## P

### Pattern

**[Guides]** Extracted common content referenced by multiple guides.

- reference/smoke_testing_pattern.md (3-4 part smoke testing workflow)

**See:** Reference

**Guide:** reference/smoke_testing_pattern.md, reference/qc_rounds_pattern.md

---

### Phase

**[Multiple contexts - OVERLOADED TERM]** Term for distinct sections within a stage/round.

- ✅ CORRECT: "S2.P1", "S10.P2", "Debugging Phase 3"

**See:** Stage, Part, Round, Iteration

---

### Phase Transition Prompt
Mandatory acknowledgment prompt used when transitioning between stages/phases.

**See:** Mandatory Reading Protocol

**Guide:** prompts_reference_v2.md

---

### Post-Feature Alignment
S8.P1 process of updating remaining feature specs after completing one feature.

**See:** S8.P1, Alignment

**Guide:** stages/s8/s8_p1_cross_feature_alignment.md

---

### Post-Implementation
S7 process of validating implemented feature.

**See:** S7, Feature Testing

**Guide:** stages/s7/s7_p1_smoke_testing.md, stages/s7/s7_p2_qc_rounds.md, stages/s7/s7_p3_final_review.md

---

### PR Review
Pull Request review (7 categories) in S7 Phase 3 Final Review.

**See:** Final Review

**Guide:** stages/s7/s7_p3_final_review.md

---

### QC (Quality Control) Rounds

**[Two contexts]**

**[S7 - Feature QC]** Three rounds testing single feature:

- Round 1: Algorithm Verification (spec vs code line-by-line)

- Round 2: Consistency & Standards (coding standards, error handling)

**[S9.P2 - Epic QC]** Three rounds testing entire epic:

- Round 1: Epic Algorithm Verification (epic requirements vs implementation)

**See:** S7, S9.P2, Round

**Guide:** stages/s7/s7_p2_qc_rounds.md (feature), stages/s9/s9_p2_epic_qc_rounds.md (epic)

---

### Quick Reference Card
Summary section in EPIC_README.md showing current epic status at a glance.

**See:** EPIC_README.md

---

### README.md

**[Two contexts]**

**[Epic-level]** EPIC_README.md containing:

- Agent Status

- Epic Progress Tracker

**[Feature-level]** feature_XX_{name}/README.md containing:

- Feature status

**See:** EPIC_README.md, Agent Status

---

### Reference

**[Guides]** Supporting materials in reference/ folder.

- Patterns (reference/smoke_testing_pattern.md, reference/qc_rounds_pattern.md)

**See:** Pattern

---

### Restart Protocol
Rules for when to restart testing after finding issues.

**See:** Loop-Back, Debugging Protocol

**Guide:** debugging/debugging_protocol.md, stages/s7/s7_p1_smoke_testing.md

---

### Resumption
Process of continuing work after session compaction.

**See:** Session Compaction, Agent Status

**Guide:** prompts/special_workflows_prompts.md

---

### Round

**[Two contexts]**

**[S5 v2]** Not used (replaced by Phase 1: Draft Creation, Phase 2: Validation Loop)

**[Validation Loop]** Iterative quality control validation:

- Check ALL dimensions every round until 3 consecutive clean rounds

**Historical Context (S5 v1):**
- S5 v1 had "rounds" (Round 1: I1-I7, Round 2: I8-I13, Round 3: I14-I22)
- S5 v2 uses phases (Phase 1: Draft Creation, Phase 2: Validation Loop)

**See:** Iteration, Phase, Validation Loop

---

### Session Compaction
Context window limit forcing conversation summarization.

**See:** Agent Status, Resumption

---

### Smoke Testing

**[Two contexts]**

**[S7 - Feature Smoke Testing]** Three parts:

- Part 1: Import Test

- Part 2: Entry Point Test

**[S9.P1 - Epic Smoke Testing]** Four parts:

- Part 1-3: Same as feature

**See:** E2E, S7, S9.P1

**Guide:** stages/s7/s7_p1_smoke_testing.md (feature), stages/s9/s9_p1_epic_smoke_testing.md (epic)

---

### Spec.md
Specification document in each feature folder containing all requirements.

**See:** Feature, Checklist.md

**Guide:** stages/s2/s2_feature_deep_dive.md

---

### Spec Validation

**[Gate 25 Dimension 11]** Three-way validation of spec.md against validated documents.

1. Epic notes (user's original request in `.shamt/epics/requests/{epic_name}.txt`)

**See:** Gate 25, Dimension 11

**Guide:** stages/s5/s5_v2_validation_loop.md (Dimensions 10, 11: Gates 24, 25), reference/spec_validation.md

---

### Stage
Top-level workflow division. 10 stages total:

**See:** Epic, Feature

**Guide:** README.md (guide index)

---

### S5 Sub-Stages
S5 (Feature Implementation) has 5 sub-stages per feature:

**See:** S5, Feature

**Guide:** stages/s5/ folder

---

### implementation_plan.md
Implementation plan (~400 lines) in each feature folder containing comprehensive build guide.

**See:** S5, Implementation Execution, implementation_checklist.md

**Guide:** stages/s5/s5_v2_validation_loop.md

---

### Traceability

**[Multiple contexts]**

**[Algorithm Traceability]** Mapping algorithms from spec to TODO tasks

- Created: Iteration 2

- Finalized: Iteration 19

**[Spec Traceability]** Mapping requirements to implementation

- Via checklist.md

**See:** Algorithm Traceability Matrix, Checklist.md

---

### User Testing
S10 mandatory testing by the user before commit.

**See:** S10, Mandatory Gates

**Guide:** stages/s10/s10_epic_cleanup.md

---

### Validation

**[Multiple contexts]**

**[Spec Validation]** Gate 25 - three-way validation against epic notes, epic ticket, spec summary

**[Data Validation]** Iteration 7 - planning data validation strategies

**[Output Validation]** Validation Loop complete - verify outputs match consumer expectations

**See:** Spec Validation, Gates

---

## W

### Workflow

**[General]** The Epic-Driven Development v2 process (Stages 1-7)

**[Sub-workflows]** Specialized processes:

- Debugging Protocol

- Missed Requirement Workflow

**See:** Stage, Debugging Protocol

**Guide:** README.md, EPIC_WORKFLOW_USAGE.md

---

### Workflow Selection
Decision process for choosing which workflow to use.

**See:** Debugging Protocol, Missed Requirement

**Guide:** reference/faq_troubleshooting.md

---

### Zero Tech Debt Tolerance
Principle that ALL issues must be fixed immediately (no deferrals).

**See:** Critical Rules

---

---
