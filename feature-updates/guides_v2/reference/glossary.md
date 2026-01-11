# Glossary - Epic-Driven Development Workflow v2

**Purpose:** Definitions of all key terms, abbreviations, and context-specific terminology used in the workflow

**Last Updated:** 2026-01-04

---

## How to Use This Glossary

Terms are organized alphabetically. Terms with multiple context-specific meanings show all contexts with clear labels.

**Notation:**
- **[Context]** indicates where term is used differently
- **See:** points to related terms
- **Guide:** references specific guide files

---

## A

### Acceptance Criteria
Requirements that define when a feature or task is considered complete. Documented in spec.md and used to verify implementation in Stage 5c QC rounds.

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

**Created in:** Iteration 2 (Stage 5a Round 1)
**Finalized in:** Iteration 19 (Stage 5a Round 3)

**Purpose:** Ensures 100% coverage of algorithms in implementation plan

**See:** implementation_plan.md, Iteration

**Guide:** round1_todo_creation.md, round3_part1_preparation.md

---

### Alignment
Process of ensuring consistency across features (Stage 3) or updating specs after implementation (Stage 5d).

**Two contexts:**
- **[Stage 3]** Cross-Feature Alignment: Pairwise comparison of all feature specs
- **[Stage 5d]** Post-Feature Alignment: Update remaining feature specs after one feature completes

**See:** Cross-Feature Sanity Check, Post-Feature Alignment

**Guide:** cross_feature_sanity_check.md, post_feature_alignment.md

---

## B

### Bug Fix
Code correction following the bug fix workflow (Stage 2 → 5a → 5b → 5c only).

**When used:** Bugs found during Stage 7 user testing

**Folder structure:** `bugfix_{priority}_{name}/` inside epic folder

**Priority levels:** high, medium, low

**See:** Debugging Protocol, Missed Requirement

**Guide:** bugfix_workflow.md

---

## C

### Checklist.md
Implementation checklist in each feature folder mapping spec requirements to TODO tasks.

**Created:** Stage 2 (Feature Deep Dives)
**Updated:** Throughout Stage 5a (Implementation Planning)
**Verified:** Stage 5b (Implementation Execution)

**Purpose:** Dual verification that spec and implementation plan are aligned

**See:** Spec.md, implementation_plan.md

---

### Code Changes
Documentation of all code modifications during implementation.

**File:** `code_changes.md` in feature folder

**Updated during:** Stage 5b (Implementation), Debugging

**Contents:** File modified, function/method changed, reason for change, before/after state

**See:** Implementation Execution

**Guide:** implementation_execution.md

---

### Compaction
See: Session Compaction

---

### Component
**[Stage 5b Implementation]** A logical piece of functionality implemented in a single phase.

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
- **Required:** >90% for Stage 5a completion
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

**[Stage 5c]** Part 4 of smoke testing (feature-level, checking for conflicts)
**[Stage 6a]** Part 4 of epic smoke testing (epic-level, validating workflows)

**See:** Epic Testing, Smoke Testing

**Guide:** smoke_testing.md, epic_smoke_testing.md

---

### Cross-Feature Sanity Check
Stage 3 process of systematic pairwise comparison of all feature specs.

**Purpose:** Identify conflicts, overlaps, gaps before implementation

**See:** Stage 3, Alignment

**Guide:** cross_feature_sanity_check.md

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
- After Stage 5c: Skip 5d/5e if last feature
- After Stage 5e: Next feature or Stage 6
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

**Documented in:** spec.md, Iteration 5 (Stage 5a)

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

**Guide:** epic_planning.md

---

### Epic Progress Tracker
Table in EPIC_README.md tracking each feature through all stages.

**Columns:** Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e

**Symbols:**
- ✅ Complete
- 🔄 In Progress
- ◻️ Not Started

**Updated:** After each stage completes

**See:** EPIC_README.md

---

### Epic Testing
Stage 6 process testing entire epic as cohesive system.

**Three sub-stages:**
- 6a: Epic Smoke Testing (4 parts)
- 6b: Epic QC Rounds (3 rounds)
- 6c: Epic Final Review

**Different from feature testing:** Tests cross-feature integration, epic-level workflows

**See:** Stage 6, Feature Testing

**Guide:** epic_final_qc.md

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

**Lifecycle:** Stage 2 → Stage 5 (5a → 5b → 5c → 5d → 5e per feature)

**See:** Epic, Stage 5

**Guide:** feature_deep_dive.md

---

### Feature Testing
Stage 5c process testing single feature in isolation.

**Three phases:**
- Phase 1: Smoke Testing (3 parts)
- Phase 2: QC Rounds (3 rounds)
- Phase 3: Final Review

**Different from epic testing:** Tests feature alone, not cross-feature integration

**See:** Stage 5c, Epic Testing

**Guide:** stages/stage_5/smoke_testing.md, qc_rounds.md, final_review.md

---

## G

### Gate
Mandatory checkpoint that must PASS before proceeding.

**Mandatory gates in workflow:**
- **Gate 4a (Iteration 4a):** TODO Specification Audit
- **Gate 23a (Iteration 23a):** Pre-Implementation Spec Audit (4 PARTS, 100% metrics)
- **Gate 25 (Iteration 25):** Spec Validation Against Validated Documents
- **Gate 24 (Iteration 24):** Implementation Readiness Protocol (GO/NO-GO)
- **Smoke Testing Part 3:** E2E Execution Test (both feature and epic)
- **User Testing:** Zero bugs required (Stage 7)

**See:** Mandatory Gates, Iteration

**Guide:** round1_todo_creation.md, round3_part2a_gates_1_2.md, round3_part2b_gate_3.md

---

### GO Decision
Iteration 24 outcome indicating readiness to proceed to Stage 5b implementation.

**Requirements for GO:**
- ALL checklist items ✅
- Confidence ≥ MEDIUM
- ALL mandatory gates PASSED (4a, 23a, 25)
- Integration verification complete
- Quality gates met (test coverage >90%, performance acceptable)

**If NO-GO:** Return to appropriate iteration, fix issues, re-run gates

**See:** Iteration 24, NO-GO, Gates

**Guide:** round3_part2b_gate_3.md

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
Stage 5b process of writing feature code following implementation_plan.md.

**Key requirements:**
- Interface verification FIRST (before writing any code)
- Keep spec.md VISIBLE at all times
- Run tests after EACH phase (100% pass required)
- Mini-QC checkpoints every 5-7 tasks
- Update code_changes.md in real-time
- Update implementation_checklist.md in real-time

**Typical time:** 1-4 hours per feature

**See:** Stage 5b, implementation_plan.md

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

**Purpose:** Allows testing after each phase (catch bugs early)

**See:** Iteration 17, Stage 5b

**Guide:** round3_part1_preparation.md

---

### Integration Point
Location where features or components interact.

**Documented in:**
- Iteration 9 (Stage 5a Round 2)
- Stage 5d (Post-Feature Alignment)
- Stage 5e (Testing Plan Update)

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

**Guide:** round3_part2a_gates_1_2.md

---

### Interface Contracts
Agreements defining method signatures, parameters, return types.

**Verified in:**
- Iteration 8 (Interface Contracts)
- Gate 23a Part 3 (Interface Contracts Audit)
- Stage 5b before implementation (Interface Verification First)

**Critical rule:** Read source code to verify (never assume)

**See:** Hands-On Data Inspection

**Guide:** round2_todo_creation.md, round3_part2a_gates_1_2.md

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
**[Stage 5a]** Single verification step in TODO Creation process.

**Total:** 24 iterations across 3 rounds
- **Round 1:** Iterations 1-7 + Gate 4a
- **Round 2:** Iterations 8-16
- **Round 3:** Iterations 17-24 (includes Gates 23a, 25, 24)

**All iterations mandatory** - skipping not allowed

**See:** Round, Stage 5a

**Guide:** round1_todo_creation.md, round2_todo_creation.md, round3_part1_preparation.md, round3_part2a_gates_1_2.md, round3_part2b_gate_3.md

---

## L

### Lessons Learned
Insights and improvements documented after feature or epic completion.

**Files:**
- `feature_XX_{name}/lessons_learned.md` (per feature)
- `{epic_name}/epic_lessons_learned.md` (epic-level)

**Updated:** Stage 5c Phase 3 (Final Review), Stage 6c (Epic Final Review)

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
- Issues in Epic Testing → Fix → Restart Stage 6a Part 1
- User Testing finds bugs → Fix → Restart Stage 6 (not Stage 7)

**Principle:** Always restart from BEGINNING of testing after fixes

**See:** Debugging Protocol, Restart Protocol

**Guide:** debugging/debugging_protocol.md, workflow_diagrams.md

---

## M

### Mandatory Gates
Checkpoints that CANNOT be skipped and must PASS before proceeding.

**All mandatory gates:**
1. Gate 4a: TODO Specification Audit (Stage 5a Round 1)
2. Gate 23a: Pre-Implementation Spec Audit - 4 PARTS (Stage 5a Round 3)
3. Gate 25: Spec Validation Against Validated Documents (Stage 5a Round 3)
4. Gate 24: Implementation Readiness (GO/NO-GO) (Stage 5a Round 3)
5. Smoke Testing Part 3: E2E Execution (Stage 5c, Stage 6a)
6. User Testing: ZERO bugs required (Stage 7)

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
Lightweight validation during Stage 5b implementation.

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
- >3 tasks needed → Return to Stage 5a Round 3

**See:** Bug Fix, Debugging Protocol

**Guide:** missed_requirement_workflow.md

---

### Mock
Test double that simulates real object behavior.

**Audited in:** Iteration 21 (Mock Audit & Integration Test Plan)

**Critical rule:** Mocks must match REAL interfaces (verify from source code)

**See:** Integration Test, Iteration 21

**Guide:** round3_part1_preparation.md

---

## N

### NO-GO Decision
Iteration 24 outcome indicating NOT ready to proceed to Stage 5b.

**Causes:**
- Confidence < MEDIUM
- Gate 4a failed
- Gate 23a failed (any of 4 parts <100%)
- Gate 25 failed (discrepancies found)
- Integration verification incomplete
- Quality gates not met

**Action:** Return to appropriate iteration, fix issues, re-run gates

**See:** GO Decision, Iteration 24

**Guide:** round3_part2b_gate_3.md

---

## O

### Orchestration
**[Implementation]** Coordinating the complete feature lifecycle (5b → 5c → 5d → 5e).

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
**[Multiple contexts]** Term for distinct sections within a stage/round.

**[Stage 2]** Feature Deep Dive has 3 phases:
- Phase 0: Research (Iterations 0-1.5)
- Phase 1: Specification (Iterations 2-2.5)
- Phase 2: Refinement (Iterations 3-6)

**[Stage 5b]** Implementation has 5-6 phases:
- Example: Data structures → Core algorithm → Integration → Error handling → Edge cases → Tests

**[Stage 5c]** Post-Implementation has 3 phases:
- Phase 1: Smoke Testing
- Phase 2: QC Rounds
- Phase 3: Final Review

**[Debugging]** Debugging Protocol has 5 phases:
- Discovery → Investigation → Root Cause → Fix → Verification

**See:** Stage, Round, Iteration

---

### Phase Transition Prompt
Mandatory acknowledgment prompt used when transitioning between stages/phases.

**Location:** prompts_reference_v2.md (router), prompts/*.md (actual prompts)

**Examples:**
- "Starting Stage 1" prompt
- "Starting Stage 5a Round 1" prompt
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
Stage 5d process of updating remaining feature specs after completing one feature.

**Purpose:** Incorporate insights from ACTUAL implementation (not plans)

**Skipped if:** Completed feature was the LAST feature (no specs to update)

**See:** Stage 5d, Alignment

**Guide:** post_feature_alignment.md

---

### Post-Implementation
Stage 5c process of validating implemented feature.

**Three phases:**
1. Smoke Testing (3 parts, Part 3 is mandatory gate)
2. QC Rounds (3 rounds)
3. Final Review

**Restart protocol:** ANY issues = restart from Smoke Testing Part 1

**See:** Stage 5c, Feature Testing

**Guide:** stages/stage_5/ (smoke_testing.md, qc_rounds.md, final_review.md)

---

### PR Review
Pull Request review (7 categories) in Stage 5c Phase 3 Final Review.

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

**[Stage 5c - Feature QC]** Three rounds testing single feature:
- Round 1: Algorithm Verification (spec vs code line-by-line)
- Round 2: Consistency & Standards (coding standards, error handling)
- Round 3: Integration & Edge Cases (integration points, edge cases)

**[Stage 6b - Epic QC]** Three rounds testing entire epic:
- Round 1: Epic Algorithm Verification (epic requirements vs implementation)
- Round 2: Epic Consistency & Standards (cross-feature consistency)
- Round 3: Epic Integration & Success Criteria (epic success criteria met)

**Restart protocol:** Issues in ANY round = restart from smoke testing (not Round 1)

**See:** Stage 5c, Stage 6b, Round

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
- Issues in Epic QC → Restart Stage 6a Part 1
- User finds bugs → Fix, then restart Stage 6 (NOT Stage 7)

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

**[Stage 5a TODO Creation]** Collection of iterations:
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

**[Stage 5c - Feature Smoke Testing]** Three parts:
- Part 1: Import Test
- Part 2: Entry Point Test
- Part 3: E2E Execution Test (MANDATORY GATE)

**[Stage 6a - Epic Smoke Testing]** Four parts:
- Part 1-3: Same as feature
- Part 4: Cross-Feature Integration (epic-specific)

**Restart rule:** Failure in ANY part = restart from Part 1

**See:** E2E, Stage 5c, Stage 6a

**Guide:** smoke_testing.md (feature), epic_smoke_testing.md (epic)

---

### Spec.md
Specification document in each feature folder containing all requirements.

**Created:** Stage 2 (Feature Deep Dives)
**Updated:** Throughout Stage 2 as requirements clarified
**Used during:** Stage 5b (implementation reference), Stage 5c (QC verification)

**Sections:**
- Feature Overview
- Requirements (numbered for traceability)
- Edge Cases
- Integration Points
- Acceptance Criteria
- Updates History

**See:** Feature, Checklist.md

**Guide:** feature_deep_dive.md

---

### Spec Validation
**[Gate 25 Iteration 25]** Three-way validation of spec.md against validated documents.

**Three validated sources:**
1. Epic notes (user's original request in {epic_name}.txt)
2. Epic ticket (user-validated outcomes from Stage 1)
3. Spec summary (user-validated feature outcomes from Stage 2)

**Critical rule:** Close spec.md before reading validated docs (avoid confirmation bias)

**Purpose:** Prevents catastrophic bugs (Feature 02 bug: spec misinterpreted epic notes)

**See:** Gate 25, Iteration 25

**Guide:** round3_part2b_gate_3.md, spec_validation.md

---

### Stage
Top-level workflow division. 7 stages total:
1. Epic Planning
2. Feature Deep Dives (per feature)
3. Cross-Feature Sanity Check
4. Epic Testing Strategy
5. Feature Implementation (5a → 5b → 5c → 5d → 5e per feature)
6. Epic-Level Final QC
7. Epic Cleanup

**All stages mandatory** - cannot skip

**See:** Epic, Feature

**Guide:** README.md (guide index)

---

### Stage 5 Sub-Stages
Stage 5 (Feature Implementation) has 5 sub-stages per feature:
- **5a:** TODO Creation (24 iterations across 3 rounds)
- **5b:** Implementation Execution (write code)
- **5c:** Post-Implementation (smoke testing + QC rounds + final review)
- **5d:** Post-Feature Alignment (update remaining feature specs) - skip if last feature
- **5e:** Testing Plan Update (update epic_smoke_test_plan.md) - skip if last feature

**Loop:** Repeat 5a → 5b → 5c → 5d → 5e for EACH feature

**See:** Stage 5, Feature

**Guide:** stages/stage_5/ folder

---

## T

### implementation_plan.md
Implementation plan (~400 lines) in each feature folder containing comprehensive build guide.

**Created:** Stage 5a (Implementation Planning - 24 iterations across 3 rounds)
**User-Approved:** After Stage 5a (MANDATORY Gate 5)
**Used:** Stage 5b (Implementation Execution - PRIMARY reference)

**Structure:**
- Phased implementation (5-6 phases)
- Implementation tasks with acceptance criteria
- Dependencies documented
- Test strategy (>90% coverage required)
- Integration points
- Performance considerations
- Rollback strategy

**See:** Stage 5a, Implementation Execution, implementation_checklist.md

**Guide:** round1_todo_creation.md, round2_todo_creation.md, round3 guides

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
Stage 7 mandatory testing by the user before commit.

**Requirements:**
- ZERO bugs found
- 100% unit test pass rate
- User approval explicit

**If bugs found:**
- Document in epic debugging/ISSUES_CHECKLIST.md
- Fix ALL bugs
- Restart Stage 6 (not Stage 7)
- Return to user testing
- Repeat until zero bugs

**See:** Stage 7, Mandatory Gates

**Guide:** epic_cleanup.md

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
- Bug found in Stage 7 → Bug Fix Workflow
- New epic → Regular workflow (Stages 1-7)

**See:** Debugging Protocol, Missed Requirement

**Guide:** faq_troubleshooting.md

---

## Z

### Zero Tech Debt Tolerance
Principle that ALL issues must be fixed immediately (no deferrals).

**Applied in:**
- Stage 5c QC Rounds (no "we'll fix it later")
- Stage 6 Epic QC (no skipping issues)
- Stage 7 User Testing (ZERO bugs required)

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

**For Stage 1:**
- Epic, EPIC_README.md, Feature, Agent Status

**For Stage 2:**
- Feature, Spec.md, Checklist.md, Phase [Stage 2]

**For Stage 3:**
- Alignment [Stage 3], Cross-Feature Sanity Check

**For Stage 4:**
- Epic Testing, Integration Point

**For Stage 5a:**
- Round, Iteration, implementation_plan.md, Gates, GO Decision, NO-GO Decision
- Algorithm Traceability Matrix, Spec Validation

**For Stage 5b:**
- Implementation Execution, Component, Phase [Implementation], Mini-QC Checkpoint

**For Stage 5c:**
- Post-Implementation, Smoke Testing, QC Rounds, E2E, PR Review

**For Stage 5d:**
- Post-Feature Alignment, Alignment [Stage 5d]

**For Stage 5e:**
- Testing Plan Update, Integration Point

**For Stage 6:**
- Epic Testing, Smoke Testing [Epic], QC Rounds [Epic]

**For Stage 7:**
- User Testing, Bug Fix, Mandatory Gates

**For Debugging:**
- Debugging Protocol, ISSUES_CHECKLIST.md, Loop-Back, Restart Protocol

**For Missed Requirements:**
- Missed Requirement, Workflow Selection

**For Session Management:**
- Session Compaction, Resumption, Agent Status, Context Window

---

**Last Updated:** 2026-01-04

**See Also:**
- faq_troubleshooting.md - Common questions and troubleshooting
- workflow_diagrams.md - Visual workflow diagrams
- README.md - Complete guide index
