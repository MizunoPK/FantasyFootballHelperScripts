# Phase Transition Prompts Reference (v2)

**Version:** 2.0
**Last Updated:** 2025-12-30
**Purpose:** MANDATORY prompts for stage transitions

---

## ⚠️ CRITICAL: When to Use These Prompts

**You MUST use these prompts when:**
- Starting ANY stage (Stages 1-7)
- Starting ANY sub-stage (5a, 5b, 5c, 5d, 5e)
- Resuming work after session compaction
- Creating a bug fix
- Encountering problems or blockers

**These prompts are MANDATORY. Do NOT skip them.**

**Why prompts are required:**
1. Proves you READ the guide (not working from memory)
2. Lists critical requirements for accountability
3. Verifies prerequisites before starting
4. Updates README Agent Status for persistence
5. Prevents guide abandonment (documented 40% failure rate without prompts)

---

## How to Use These Prompts

**STEP 1: Read the guide FIRST**
```
Use Read tool to load the ENTIRE guide for the stage you're starting
```

**STEP 2: Use the appropriate prompt from this file**
```
Copy the prompt template
Fill in {placeholders} with actual values
Include ALL sections (requirements, prerequisites, status update)
```

**STEP 3: Actually DO what the prompt says**
```
Don't just say it - verify prerequisites, update status, proceed with workflow
```

**STEP 4: Update EPIC_README.md or feature README.md Agent Status**
```
Document guide read, critical rules, next action
```

---

## Stage Transition Prompts

### Starting Stage 1: Epic Planning

**User says:** "Help me develop the {epic_name} epic" or "Let's plan {epic_name}"

**Prerequisite:** User has created `feature-updates/{epic_name}.txt` with initial scratchwork notes.

**Agent MUST respond:**

```
I'm reading `STAGE_1_epic_planning_guide.md` to ensure I follow the complete epic planning workflow...

**The guide requires:**
- Phase 1: Analyze epic request and codebase reconnaissance
- Phase 2: Propose feature breakdown to user (user MUST approve)
- Phase 3: Create epic folder structure
- Phase 4: Create initial epic_smoke_test_plan.md (placeholder)
- Phase 5: Create EPIC_README.md with Quick Reference Card
- Phase 6: Create epic_lessons_learned.md
- NO SKIPPING USER APPROVAL for feature breakdown
- If epic is large (>5 components): Propose feature breakdown early
- If epic is small (<3 components): Propose single-feature approach

**Prerequisites I'm verifying:**
✅ Epic request file exists: `feature-updates/{epic_name}.txt`
✅ Epic request contains user's initial notes
✅ Epic scope is clear from request

**I'll now proceed with Phase 1 (Analyze Epic Request & Reconnaissance)...**

**Creating initial EPIC_README.md status:**
- Current Stage: Stage 1 - Epic Planning
- Current Guide: STAGE_1_epic_planning_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "User must approve feature breakdown", "Create placeholder test plan", "No skipping reconnaissance"
- Next Action: Read epic request file and perform codebase reconnaissance

Starting Phase 1...
```

---

### Starting Stage 2: Feature Deep Dive

**User says:** "Help me develop the {feature_name} feature" or "Let's work on feature_01"

**Prerequisite:** Stage 1 complete (epic folder and feature folders created)

**Agent MUST respond:**

```
I'm reading `STAGE_2_feature_deep_dive_guide.md` to ensure I follow the complete deep dive workflow...

**The guide requires:**
- **🚨 CRITICAL: NEVER MAKE ASSUMPTIONS**
  - Do NOT assume requirements, methodologies, or behavior
  - ASK USER via checklist.md questions BEFORE asserting in spec.md
  - Only document requirements after explicit user confirmation
  - If uncertain → create question, do NOT assume answer
- Phase 1: Targeted research (ONLY for THIS feature's scope, not entire epic)
- Phase 2: Update spec.md and checklist.md with findings
  - Only write CONFIRMED information in spec.md (not assumptions)
  - Uncertain items go in checklist.md as questions
- Phase 3: Interactive question resolution
  - ONE question at a time (Lesson learned: don't batch questions)
  - Update spec/checklist after EACH answer
  - Evaluate for new questions after each resolution
- Phase 4: Feature complete + dynamic scope adjustment check
  - If feature grew >30% in complexity → Propose split into 2 features
  - If new dependencies discovered → Create new features if needed
- Phase 5: **Compare to completed feature specs** (if any features already done)
  - Ensure alignment with previous features
  - Maintain consistency in approach
- Checklist.md ALL items must be resolved (marked [x]) before Stage 2 complete

**Prerequisites I'm verifying:**
✅ Epic folder exists: `feature-updates/{epic_name}/`
✅ Feature folder exists: `feature_{NN}_{name}/`
✅ Stage 1 complete (EPIC_README.md shows Stage 1 complete)

**I'll now proceed with Phase 1 (Targeted Research for THIS feature only)...**

**Updating feature README Agent Status:**
- Current Phase: PLANNING
- Current Guide: STAGE_2_feature_deep_dive_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "NEVER assume - confirm with user first", "Targeted research only", "ONE question at a time", "Only confirmed info in spec.md", "Checklist all [x] required"
- Next Action: Begin targeted research for {feature_name}

Starting Phase 1...
```

---

### Starting Stage 3: Cross-Feature Sanity Check

**User says:** "Review all features" or "Run cross-feature sanity check" or Agent detects ALL features completed Stage 2

**Prerequisite:** ALL features have completed Stage 2 (all feature README.md files show "Stage 2 complete")

**Agent MUST respond:**

```
I'm reading `STAGE_3_cross_feature_sanity_check_guide.md` to ensure I perform systematic cross-feature validation...

**The guide requires:**
- Systematic pairwise comparison of ALL feature specs
- Interface validation between features
- Dependency graph creation and cycle detection
- Conflict resolution with user clarification
- **MANDATORY user sign-off** before proceeding to Stage 4
- NO SKIPPING comparisons (N×N matrix approach)
- Document conflicts and resolutions

**Prerequisites I'm verifying:**
✅ ALL features show "Stage 2 complete" in their README.md files
  - Feature 01 ({name}): ✅
  - Feature 02 ({name}): ✅
  - {Continue for all features}
✅ All feature spec.md files exist
✅ All feature checklist.md files resolved

**I'll now proceed with systematic pairwise comparison...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 3 - Cross-Feature Sanity Check
- Current Guide: STAGE_3_cross_feature_sanity_check_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Pairwise comparison mandatory", "User sign-off required", "No skipping comparisons"
- Next Action: Create Feature Comparison Matrix and begin pairwise validation

Starting cross-feature analysis...
```

---

### Starting Stage 4: Epic Testing Strategy

**User says:** "Update epic test plan" or "Define testing strategy" or Agent detects Stage 3 complete

**Prerequisite:** Stage 3 complete (user signed off on aligned specs)

**Agent MUST respond:**

```
I'm reading `STAGE_4_epic_testing_strategy_guide.md` to ensure I create a comprehensive epic testing strategy...

**The guide requires:**
- Review initial epic_smoke_test_plan.md (created in Stage 1)
- Update test plan based on Stage 2-3 findings:
  - Integration points identified in Stage 3
  - Actual feature implementations (not assumptions)
  - Cross-feature workflows that need testing
- Define epic success criteria (measurable)
- Create hybrid test scenarios:
  - Specific commands/scenarios (concrete tests to always run)
  - High-level categories (flexible areas for Stage 5e/6 updates)
- Identify data quality checks (verify VALUES not just structure)
- Plan evolves: Stage 1 (placeholder) → Stage 4 (based on specs) → Stage 5e (based on implementation)

**Prerequisites I'm verifying:**
✅ Stage 3 complete (EPIC_README.md shows user sign-off)
✅ All feature specs aligned
✅ Integration points documented
✅ epic_smoke_test_plan.md exists (from Stage 1)

**I'll now review the existing test plan and update based on Stages 2-3 findings...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 4 - Epic Testing Strategy
- Current Guide: STAGE_4_epic_testing_strategy_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Update test plan (don't recreate)", "Hybrid test scenarios", "Measurable success criteria", "Plan will evolve in Stage 5e"
- Next Action: Review current epic_smoke_test_plan.md and identify updates needed

Starting test plan update...
```

---

### Starting Stage 5a: TODO Creation (Round 1)

**User says:** "Prepare for updates based on {feature_name}" or "Start implementation of feature_01" or "Create TODO list"

**Prerequisite:** Stage 4 complete (epic_smoke_test_plan.md updated) AND feature spec.md complete AND checklist.md resolved

**Note:** Stage 5a is split into 3 separate round guides for better digestibility:
- **STAGE_5aa_round1_guide.md** - Round 1: Iterations 1-7 + 4a (START HERE)
- **STAGE_5ab_round2_guide.md** - Round 2: Iterations 8-16
- **STAGE_5ac_round3_guide.md** - Round 3: Iterations 17-24 + 23a

**Agent MUST respond:**

```
I'm reading `STAGE_5aa_round1_guide.md` to ensure I follow all 8 iterations in Round 1...

**The guide requires:**
- **🚨 CRITICAL: TODO TASKS MUST TRACE TO SPEC REQUIREMENTS**:
  - Every TODO task must map to explicit spec.md requirement
  - Do NOT add tasks based on "best practices" or assumptions
  - Do NOT add tasks the user didn't ask for
  - If uncertain about a task → create question in questions.md
  - Only create TODO tasks for confirmed, documented requirements
- **Round 1: 8 MANDATORY iterations** (NO SKIPPING):
  - Iterations 1-7 + iteration 4a (TODO Specification Audit)
- **Iteration 4a is a MANDATORY GATE**:
  - Every TODO task MUST have acceptance criteria
  - Cannot proceed to Round 2 without PASSING iteration 4a
- **Algorithm Traceability Matrix** (iteration 4):
  - Map EVERY algorithm in spec.md to exact code location
  - Typical matrix has 40+ mappings
- **Integration Gap Check** (iteration 7):
  - Verify all new methods have identified CALLERS
  - No orphan code allowed
- **Interface Verification Protocol**:
  - READ actual source code for every dependency
  - Do NOT assume interfaces - verify them
- **STOP if confidence < Medium at Round 1 checkpoint**:
  - Create questions.md
  - Wait for user answer
  - Do NOT proceed to Round 2

**Why Round 1 matters:**
- Establishes foundation for all subsequent rounds
- Algorithm Traceability Matrix created here (used in Rounds 2 & 3)
- Integration Gap Check ensures no orphan code

**Prerequisites I'm verifying:**
✅ spec.md exists and is complete
✅ checklist.md all items resolved (all [x])
✅ Stage 4 complete (epic_smoke_test_plan.md updated)
✅ No pending questions from Stage 2

**I'll now proceed with Round 1 (iterations 1-7 + 4a). I'll create questions.md after Round 1 checkpoint if needed.**

**Updating feature README Agent Status:**
- Current Phase: TODO_CREATION
- Current Guide: STAGE_5aa_round1_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "TODO tasks MUST trace to spec requirements (no assumptions)", "8 iterations mandatory (Round 1)", "Iteration 4a is MANDATORY GATE", "STOP if confidence < Medium", "Interface verification: READ actual code"
- Progress: 0/8 iterations complete (Round 1)
- Next Action: Begin iteration 1 - Requirements Coverage Check

Starting iteration 1...
```

---

### Starting Stage 5a: TODO Creation (Round 2)

**User says:** Agent detects Round 1 complete (8/8 iterations done, confidence >= MEDIUM)

**Prerequisite:** Round 1 complete (STAGE_5aa), Iteration 4a PASSED, confidence >= MEDIUM

**Agent MUST respond:**

```
I'm reading `STAGE_5ab_round2_guide.md` to ensure I follow all 9 iterations in Round 2...

**The guide requires:**
- **Round 2: 9 MANDATORY iterations** (NO SKIPPING):
  - Iterations 8-16 (Deep Verification)
- **Re-verification iterations (11, 12, 14) are CRITICAL**:
  - Algorithm Traceability Matrix re-verify (Iteration 11)
  - E2E Data Flow re-verify (Iteration 12)
  - Integration Gap Check re-verify (Iteration 14)
  - These catch bugs introduced during Round 1 updates
- **Test Coverage Depth Check** (Iteration 15):
  - Verify tests cover edge cases, not just happy path
  - Target: >90% coverage
- **STOP if confidence < Medium at Round 2 checkpoint**:
  - Update questions.md
  - Wait for user answer

**Why Round 2 matters:**
- Deep verification of test strategy
- Edge case enumeration
- Re-verification catches bugs from Round 1 updates

**Prerequisites I'm verifying:**
✅ Round 1 complete (8/8 iterations)
✅ Iteration 4a PASSED
✅ Confidence: >= MEDIUM (from Round 1 checkpoint)
✅ TODO file created with acceptance criteria for all tasks

**I'll now proceed with Round 2 (iterations 8-16).**

**Updating feature README Agent Status:**
- Current Phase: TODO_CREATION
- Current Guide: STAGE_5ab_round2_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "9 iterations mandatory (Round 2)", "Re-verification iterations are CRITICAL", "Test coverage >90% required"
- Progress: 8/24 total iterations complete (starting Round 2)
- Next Action: Begin iteration 8 - Test Strategy Development

Starting iteration 8...
```

---

### Starting Stage 5a: TODO Creation (Round 3)

**User says:** Agent detects Round 2 complete (16/24 iterations done, confidence >= MEDIUM, test coverage >90%)

**Prerequisite:** Round 2 complete (STAGE_5ab), confidence >= MEDIUM, test coverage >90%

**Agent MUST respond:**

```
I'm reading `STAGE_5ac_round3_guide.md` to ensure I follow all 9 iterations in Round 3...

**The guide requires:**
- **Round 3: 9 MANDATORY iterations** (NO SKIPPING):
  - Iterations 17-24 + iteration 23a (Final Verification & Readiness)
- **Iteration 23a (Pre-Implementation Spec Audit) has 4 MANDATORY PARTS**:
  - Part 1: Completeness Audit
  - Part 2: Specificity Audit
  - Part 3: Interface Contracts Audit
  - Part 4: Integration Evidence Audit
  - ALL 4 PARTS must PASS
- **Iteration 24 (Implementation Readiness Protocol) is FINAL GATE**:
  - Go/no-go decision required
  - CANNOT proceed to Stage 5b without "GO" decision
- **Implementation Phasing** (Iteration 17):
  - Break implementation into phases with checkpoints
  - Prevents "big bang" integration failures
- **Mock Audit** (Iteration 21):
  - Verify EACH mock matches real interface
  - Plan at least one integration test with REAL objects

**Why Round 3 matters:**
- Final verification before implementation
- Two mandatory gates (23a and 24)
- Implementation phasing prevents big bang failures

**Prerequisites I'm verifying:**
✅ Round 2 complete (16/24 iterations)
✅ Test coverage: >90%
✅ Confidence: >= MEDIUM (from Round 2 checkpoint)
✅ Algorithm Traceability Matrix updated (Round 2)
✅ Integration Gap Check updated (Round 2)

**I'll now proceed with Round 3 (iterations 17-24 + 23a).**

**Updating feature README Agent Status:**
- Current Phase: TODO_CREATION
- Current Guide: STAGE_5ac_round3_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "9 iterations mandatory (Round 3)", "Iteration 23a: ALL 4 PARTS must PASS", "Iteration 24: GO decision required"
- Progress: 16/24 total iterations complete (starting Round 3)
- Next Action: Begin iteration 17 - Implementation Phasing

Starting iteration 17...
```

---

### Starting Stage 5b: Implementation

**User says:** "Implement the feature" or "Start coding" or Agent detects Stage 5a complete (24 iterations done)

**Prerequisite:** Stage 5a complete (24 iterations passed, Iteration 24: Implementation Readiness = PASSED)

**Agent MUST respond:**

```
I'm reading `STAGE_5b_implementation_execution_guide.md` to ensure I follow the implementation workflow...

**The guide requires:**
- **Create implementation_checklist.md** from spec.md sections
- **Keep spec.md VISIBLE** at all times (continuous verification)
- Execute TODO tasks in order
- **Mini-QC checkpoints** after each major component:
  - Run unit tests
  - Verify against spec
  - Update code_changes.md
- **Run unit tests after EVERY phase** (100% pass required)
- **Interface Verification** before integration:
  - Verify interface matches ACTUAL dependency code
  - Do NOT assume - READ the actual source
- NO code-review tone (write production code, not suggestions)
- **Update code_changes.md INCREMENTALLY** (not at the end)
- STOP if stuck or blocked - ask user

**Prerequisites I'm verifying:**
✅ Stage 5a complete (EPIC_README.md shows 24 iterations done)
✅ Iteration 24: Implementation Readiness = PASSED
✅ todo.md exists with complete task list
✅ questions.md resolved (or documented "no questions")

**I'll now create implementation_checklist.md from spec.md and begin implementation...**

**Updating feature README Agent Status:**
- Current Phase: IMPLEMENTATION
- Current Guide: STAGE_5b_implementation_execution_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "spec.md visible at all times", "Unit tests after every phase (100% pass)", "Mini-QC checkpoints", "Update code_changes.md incrementally"
- Progress: 0/{N} TODO tasks complete
- Next Action: Create implementation_checklist.md from spec.md sections

Starting implementation...
```

---

### Starting Stage 5c (Phase 1): Smoke Testing

**User says:** "Validate the implementation" or Agent detects Stage 5b complete

**Prerequisite:** Stage 5b complete (all TODO tasks done, all unit tests passing)

**Agent MUST respond:**

```
I'm reading `STAGE_5ca_smoke_testing_guide.md` to ensure I follow the 3-part smoke testing protocol...

**The guide requires:**
- **Part 1: Import Test** (verify module loads without errors)
  - Import all new/modified modules
  - No import errors = pass
- **Part 2: Entry Point Test** (verify script starts correctly)
  - Run with --help flag
  - Verify help text displays correctly
- **Part 3: E2E Execution Test** (CRITICAL - verify OUTPUT DATA VALUES)
  - Run feature with REAL data (not mocks)
  - **Verify ACTUAL DATA VALUES** (not just file existence)
  - Example: df['score'].between(0, 500).all() AND df['projected_points'].sum() > 0
  - BAD: assert Path("output.csv").exists()  # Structure only
  - GOOD: assert df['projected_points'].sum() > 0  # Data values
- **Re-Reading Checkpoint**:
  - After Part 2, re-read "What Passes" criteria
  - After Part 3, re-read DATA VALUES examples
- **MANDATORY GATE**:
  - All 3 parts must pass to proceed to QC rounds
  - If ANY part fails → fix issue and restart smoke testing from Part 1

**Prerequisites I'm verifying:**
✅ Stage 5b complete (all TODO tasks done)
✅ ALL unit tests passing (100% pass rate)
✅ code_changes.md updated with all changes
✅ implementation_checklist.md all items verified

**I'll now begin with Part 1: Import Test...**

**Updating feature README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_SMOKE_TESTING
- Current Guide: STAGE_5ca_smoke_testing_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "3 parts MANDATORY", "Verify DATA VALUES not structure", "GATE before QC rounds"
- Progress: 0/3 parts complete
- Next Action: Smoke Test Part 1 - Import test

Running import test for {feature_name}...
```

---

### Starting Stage 5c (Phase 2): QC Rounds

**User says:** "Begin QC rounds" or Agent detects smoke testing passed

**Prerequisite:** Smoke testing complete (all 3 parts passed)

**Agent MUST respond:**

```
I'm reading `STAGE_5cb_qc_rounds_guide.md` to ensure I follow the 3-round QC protocol...

**The guide requires:**
- **QC Round 1: Basic Validation**
  - Pass criteria: <3 critical issues, >80% requirements met
  - Unit tests, code structure, output files, interfaces, documentation
- **QC Round 2: Deep Verification**
  - Pass criteria: ALL Round 1 issues resolved + zero new critical issues
  - Baseline comparison, data validation, regression testing, semantic diff, edge cases
- **QC Round 3: Final Skeptical Review**
  - Pass criteria: ZERO issues found (zero tolerance)
  - Re-read spec with fresh eyes, re-check matrices, re-run smoke test
- **QC Restart Protocol**:
  - If ANY critical issues found → COMPLETELY RESTART validation
  - Restart from: Smoke Testing Part 1 → QC Round 1 → QC Round 2 → QC Round 3
  - NO partial fixes - complete restart ensures proper validation
- **Re-Reading Checkpoints**:
  - After Round 1: Re-read Round 2 pass criteria
  - After Round 2: Re-read Round 3 zero-tolerance policy
  - After Round 3: Re-read restart protocol

**Prerequisites I'm verifying:**
✅ Smoke testing complete (all 3 parts passed)
✅ Part 3 verified OUTPUT DATA VALUES (not just structure)
✅ All unit tests still passing

**I'll now begin QC Round 1: Basic Validation...**

**Updating feature README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_QC_ROUNDS
- Current Guide: STAGE_5cb_qc_rounds_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "3 rounds (no exceptions)", "QC RESTART if critical issues", "Round 3 zero tolerance"
- Progress: 0/3 rounds complete
- Next Action: QC Round 1 - Basic Validation

Starting QC Round 1 for {feature_name}...
```

---

### Starting Stage 5c (Phase 3): Final Review

**User says:** "Begin final review" or Agent detects QC rounds passed

**Prerequisite:** QC rounds complete (all 3 rounds passed, zero issues found in Round 3)

**Agent MUST respond:**

```
I'm reading `STAGE_5cc_final_review_guide.md` to ensure I follow the final review protocol...

**The guide requires:**
- **PR Review Checklist** (11 categories - ALL MANDATORY):
  1. Correctness and Logic
  2. Code Quality and Readability
  3. Comments and Documentation
  4. Refactoring Concerns
  5. Testing
  6. Security
  7. Performance
  8. Error Handling
  9. Architecture and Design
  10. Compatibility and Integration
  11. Scope and Focus
- **Lessons Learned Capture**:
  - Document what worked well
  - Document what didn't work
  - **IMMEDIATELY UPDATE GUIDES** (not just document issues)
  - Example: If QC found zero data issue → update STAGE_5ca guide NOW
- **Final Verification**:
  - 100% requirement completion (from spec)
  - All code_changes.md items implemented
  - All lessons_learned.md captured
- **Completion Criteria**:
  - PR review: ZERO issues found
  - Lessons learned: Updated (including guide updates if needed)
  - Final verification: 100% complete

**Prerequisites I'm verifying:**
✅ QC Round 3 complete (zero issues found)
✅ All smoke testing and QC documentation complete
✅ Feature fully functional with real data

**I'll now begin PR Review (11 categories)...**

**Updating feature README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_FINAL_REVIEW
- Current Guide: STAGE_5cc_final_review_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "11 categories ALL mandatory", "Update guides immediately", "100% completion required"
- Progress: PR Review starting
- Next Action: PR Review Category 1 - Correctness and Logic

Starting PR Review for {feature_name}...
```

---

### Starting Stage 5d: Cross-Feature Alignment

**User says:** "Review other feature specs" or Agent detects Stage 5c complete

**Prerequisite:** Stage 5c complete (smoke testing passed, QC rounds passed, final review complete)

**Agent MUST respond:**

```
I'm reading `STAGE_5d_post_feature_alignment_guide.md` to ensure I review all remaining feature specs...

**The guide requires:**
- Review ALL remaining features (not yet at Stage 5c)
  - Identify remaining features from EPIC_README.md Epic Progress Tracker
- For EACH remaining feature (SEQUENTIAL):
  - Read feature spec.md with fresh eyes
  - Read just-completed feature's ACTUAL code (not plans)
  - Compare spec assumptions to actual implementation
  - Identify misalignments
  - Update spec.md and checklist.md
  - Mark for rework if significant changes needed
- **Significant Rework Criteria:**
  - Return to Stage 1: Feature should be split, or no longer needed
  - Return to Stage 2: Spec assumptions fundamentally wrong
  - Return to Stage 5a: >3 new TODO tasks needed, algorithm changes significantly
  - Minor Updates (continue): ≤3 TODO adjustments, no algorithm changes
- **Compare to ACTUAL implementation** (not the plan from Stage 5a)
- Document insights in just-completed feature's spec.md
- Final verification: No remaining features need significant rework

**Why this matters:**
- Implementation reveals reality (assumptions often wrong)
- Prevents cascading issues
- Ensures remaining features align with actual code

**Prerequisites I'm verifying:**
✅ Stage 5c complete (smoke testing, QC, PR review all passed)
✅ EPIC_README.md shows which features are remaining
✅ Just-completed feature's code accessible for review

**I'll now identify remaining features and review them sequentially...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 5d - Cross-Feature Alignment
- Current Guide: STAGE_5d_post_feature_alignment_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Review ALL remaining features", "Compare to ACTUAL implementation", "Update specs proactively", "Mark features needing significant rework"
- Next Action: Identify remaining features from Epic Progress Tracker

Starting cross-feature alignment review...
```

---

### Starting Stage 5e: Epic Testing Plan Update

**User says:** "Update epic test plan" or Agent detects Stage 5d complete

**Prerequisite:** Stage 5d complete (all remaining feature specs reviewed and updated)

**Agent MUST respond:**

```
I'm reading `STAGE_5e_post_feature_testing_update_guide.md` to ensure I update the epic test plan based on actual implementation...

**The guide requires:**
- Review ACTUAL implementation of just-completed feature:
  - Read actual code (not just plans)
  - Identify actual interfaces created
  - Note actual data structures used
  - Find integration points with other features
- Compare to current epic_smoke_test_plan.md:
  - Identify gaps (implementation vs plan)
  - Find scenarios that need updating
  - Discover new integration points
- Update epic_smoke_test_plan.md:
  - Add new test scenarios based on actual implementation
  - Update existing scenarios if needed
  - Add integration point tests (cross-feature)
  - Update "Last Updated" timestamp
  - Add entry to Update History table
- **Focus on ACTUAL implementation**:
  - Not what was PLANNED
  - What was ACTUALLY built
- Test plan evolves incrementally:
  - Stage 1: Placeholder
  - Stage 4: Based on specs
  - Stage 5e: Based on actual implementation (THIS stage)
  - Stage 6: Execute evolved plan

**Why this matters:**
- Implementation often differs from specs
- New integration points discovered during coding
- Test plan must reflect REALITY for Stage 6 to be effective

**Prerequisites I'm verifying:**
✅ Stage 5d complete (all remaining features reviewed)
✅ Just-completed feature fully implemented and QC'd
✅ epic_smoke_test_plan.md accessible

**I'll now review the actual implementation and identify test plan updates...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 5e - Epic Testing Plan Update
- Current Guide: STAGE_5e_post_feature_testing_update_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Review ACTUAL implementation", "Add integration scenarios", "Update History table", "Test plan evolves incrementally"
- Next Action: Read just-completed feature's actual code to identify test plan updates

Starting test plan update...
```

---

### Starting Stage 6: Epic Final QC

**User says:** "Run epic QC" or "Validate the entire epic" or Agent detects ALL features complete Stage 5e

**Prerequisite:** ALL features complete Stage 5e, no pending bug fixes

**Agent MUST respond:**

```
I'm reading `STAGE_6_epic_final_qc_guide.md` to ensure I validate the entire epic end-to-end...

**The guide requires:**
- **Epic Smoke Testing** (distinct from feature-level testing):
  - Part 1: Epic-level import tests (all features together)
  - Part 2: Epic-level entry point tests
  - Part 3: Epic E2E execution tests (complete workflows with REAL data)
  - Part 4: Cross-feature integration tests (features working together)
  - **CRITICAL:** Verify OUTPUT DATA VALUES (not just structure)
- **Epic-Level QC Rounds** (3 rounds):
  - Round 1: Cross-Feature Integration Validation
  - Round 2: Epic Cohesion & Consistency
  - Round 3: End-to-End Success Criteria
- **Epic PR Review** (11 categories at EPIC scope):
  - Focus: Architectural consistency across features
  - Review epic-wide changes (not individual features)
- **Validation Against Original Epic Request**:
  - Read ORIGINAL {epic_name}.txt file
  - Verify epic achieves user's goals
  - Validate expected outcomes delivered
- **Use EVOLVED epic_smoke_test_plan.md**:
  - Plan updated in Stages 1 → 4 → 5e (all features)
  - Reflects ACTUAL implementation (not assumptions)
- **QC RESTART if ANY issues**:
  - Create bug fixes for issues
  - COMPLETELY RESTART Stage 6 after bug fixes

**Critical Distinction:**
- Feature testing (Stage 5c): Tests feature in ISOLATION
- Epic testing (Stage 6): Tests ALL features TOGETHER

**Prerequisites I'm verifying:**
✅ ALL features show "Stage 5e complete" in EPIC_README.md
  - Feature 01 ({name}): ✅
  - Feature 02 ({name}): ✅
  - {Continue for all features}
✅ No pending bug fixes
✅ epic_smoke_test_plan.md shows recent Stage 5e updates
✅ All unit tests passing (100%)

**I'll now execute the evolved epic_smoke_test_plan.md...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 6 - Epic Final QC
- Current Guide: STAGE_6_epic_final_qc_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Use EVOLVED test plan", "Verify OUTPUT DATA VALUES", "3 epic QC rounds", "Validate vs original request", "RESTART if ANY issues"
- Next Action: Execute epic smoke testing (Part 1: Epic-level import tests)

Starting epic smoke testing...
```

---

### Starting Stage 7: Epic Cleanup

**User says:** "Finalize epic" or "Commit and archive" or Agent detects Stage 6 complete

**Prerequisite:** Stage 6 complete (epic smoke testing, QC rounds, PR review all passed)

**Agent MUST respond:**

```
I'm reading `STAGE_7_epic_cleanup_guide.md` to ensure I properly finalize and archive the epic...

**The guide requires:**
- **Run Unit Tests** (100% pass required):
  - Execute: python tests/run_all_tests.py
  - Verify exit code = 0
  - If ANY tests fail → Fix before committing
- **Documentation Verification**:
  - EPIC_README.md complete and accurate
  - epic_lessons_learned.md contains insights from all stages
  - epic_smoke_test_plan.md reflects final implementation
  - All feature README.md files complete
- **Update Guides** (if lessons identified):
  - Review epic_lessons_learned.md "Guide Improvements Needed"
  - Update guides_v2/ files if improvements identified
  - Update CLAUDE.md if workflow changed
  - Document guide updates
- **⚠️ USER TESTING (MANDATORY GATE - BEFORE COMMIT)**:
  - Ask user to test complete system themselves
  - User reports any bugs discovered during testing
  - If bugs found → Follow bug fix protocol (Stage 2→5a→5b→5c)
  - After ALL bug fixes → RESTART Stage 6 (Epic Final QC)
  - Return to user testing after Stage 6 passes
  - Repeat until user testing passes with ZERO bugs
  - CANNOT commit without user approval
- **Final Commit**:
  - Review all changes (git status, git diff)
  - Stage all epic-related changes
  - Create commit with clear, descriptive message
  - Format: "Complete {epic_name} epic" with features listed in body
  - Push to remote (if user requests)
- **Move Epic to done/**:
  - Move ENTIRE epic folder: feature-updates/{epic}/ → feature-updates/done/{epic}/
  - Leave original epic request (.txt) in root for reference
  - Verify folder structure intact after move
- **Final Verification**:
  - Epic in done/ folder
  - Original request still in root
  - Git shows clean state

**Prerequisites I'm verifying:**
✅ Stage 6 complete (EPIC_README.md shows epic QC passed)
✅ No pending features or bug fixes
✅ All tests passing (verified recently)

**I'll now run unit tests to verify 100% pass rate...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: Stage 7 - Epic Cleanup
- Current Guide: STAGE_7_epic_cleanup_guide.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Unit tests 100% pass before commit", "User testing MANDATORY before commit", "If bugs found → RESTART Stage 6", "Move ENTIRE epic folder", "Leave .txt in root"
- Next Action: Run python tests/run_all_tests.py

Running unit tests...
```

---

## Bug Fix Creation Prompts

### Creating a Bug Fix

**User says:** "I found a bug" or "There's an issue with..." or Agent discovers issue during QC

**Can occur during:** ANY stage

**Agent MUST respond:**

```
I've identified an issue that requires a bug fix. Let me present it to you for approval...

**Issue Summary:**
- **What's wrong:** {Brief description of symptom}
- **Discovered during:** Stage {X} - {feature_name or "epic-level"}
- **Impact:** {What doesn't work because of this - e.g., "Epic smoke testing fails", "Feature produces incorrect results"}
- **Priority recommendation:** {high/medium/low}
  - high: Breaks epic functionality → Interrupt current work immediately
  - medium: Affects quality but not functionality → Finish current step first
  - low: Minor issues → Fix after current step completes
  - ALL bugs found during epic development MUST be fixed before Stage 7 (no deferred tech debt)

**Root Cause (if known):**
{Analysis of why the bug exists, or "Root cause not yet determined - will investigate in bug fix Stage 2"}

**Proposed Solution:**
{How to fix it, or "Solution TBD - will design in bug fix Stage 2"}

**Should I create a bug fix for this issue?**
- If yes: I'll create bugfix_{priority}_{name}/ folder and notes.txt and fix it before Stage 7
- If no: Please confirm this is NOT a bug and the behavior is correct as-is
- NOTE: All bugs found during epic development MUST be fixed - no deferring to "later" or leaving tech debt

Waiting for your approval...
```

**After user approves:**

```
I'm reading `STAGE_5_bug_fix_workflow_guide.md` to ensure I follow the bug fix workflow...

**The guide requires:**
- PHASE 1: Bug Fix Creation
  - Create bugfix_{priority}_{name}/ folder in epic directory
  - Create notes.txt with issue description
  - User verifies/updates notes.txt
  - Update epic EPIC_README.md to track bug fix
  - Save current work state in README
- PHASE 2: Bug Fix Implementation
  - Stage 2: Deep Dive (adapted for bug fix)
  - Stage 5a: TODO Creation (24 iterations)
  - Stage 5b: Implementation
  - Stage 5c: Post-Implementation
  - SKIP: Stages 1, 3, 4, 5d, 5e, 6, 7 (epic-level stages)
- PHASE 3: Resume Previous Work
  - Mark bug fix complete
  - Verify bug fix doesn't affect paused work
  - Resume from saved state
- **Priority Handling:**
  - high: Interrupt immediately
  - medium: Finish current sub-stage first
  - low: Finish current feature first

**I'll now create the bug fix folder and notes.txt...**

Creating bugfix_{priority}_{name}/ folder...
```

---

## Resuming After Session Compaction

### Resuming In-Progress Epic

**After session compaction during any stage**

**Agent MUST respond:**

```
I'm resuming work on the {epic_name} epic after session compaction. Let me check the current state...

**Reading EPIC_README.md Agent Status:**
- Last Updated: {YYYY-MM-DD HH:MM}
- Current Stage: Stage {X} - {stage name}
- Current Step: {specific step}
- Current Guide: {guide_name}.md
- Progress: {X/Y items complete}
- Next Action: {exact next task}

**I'm now re-reading `{guide_name}.md` to ensure I continue correctly...**

**The guide requires:**
{List 5-7 critical requirements from the guide for THIS stage}

**Verification before continuing:**
✅ {Prerequisite 1}
✅ {Prerequisite 2}
✅ {Prerequisite 3}

**Picking up from where I left off:**
- Current step: {specific step from Agent Status}
- Next action: {next action from Agent Status}

Continuing with {next action}...
```

---

## Problem Situation Prompts

### When Tests Are Failing

**Situation:** Unit tests failing during Stage 5b or 5c

**Agent MUST respond:**

```
Unit tests are failing. Following the guide requirements, I need to fix these before proceeding...

**Test Failures:**
- Total tests: {N}
- Passing: {X}
- Failing: {Y}
- Failure rate: {percentage}%

**Failed Tests:**
1. {test_name}: {failure reason}
2. {test_name}: {failure reason}
{List all failures}

**Root Cause Analysis:**
{Analysis of why tests are failing}

**Fix Plan:**
1. {Fix step 1}
2. {Fix step 2}
3. {Fix step 3}

**I'll fix these issues and re-run the test suite. Will not proceed until exit code = 0 (100% pass rate).**

Fixing test failures...
```

---

### When Stuck or Blocked

**Situation:** Agent encounters blocker that prevents progress

**Agent MUST respond:**

```
I've encountered a blocker that prevents me from continuing. Following guide requirements (STOP when blocked), I need your help...

**Blocker Description:**
{Clear description of what's blocking progress}

**What I was trying to do:**
{Context - what task/step was being attempted}

**Why I'm blocked:**
{Explanation of the blocker}

**What I need to proceed:**
{Specific ask - e.g., "Clarification on...", "Decision on...", "Access to..."}

**Options:**
1. {Option 1 and implications}
2. {Option 2 and implications}
3. {Option 3 and implications}

Which option should I take, or do you have another approach?

Waiting for your guidance...
```

---

### When Confidence < Medium

**Situation:** Agent's confidence drops below Medium during Stage 5a (TODO Creation)

**Agent MUST respond:**

```
My confidence level has dropped below Medium. Following STAGE_5a requirements, I'm STOPPING to create a question...

**Low Confidence Area:**
{What area has low confidence - e.g., "Interface verification for Feature 02 integration"}

**Current Iteration:** {N}/24
**Current Task:** {Task description}

**Why Confidence is Low:**
{Explanation - e.g., "Interface documentation unclear", "Dependency code not found", "Multiple valid approaches"}

**Question for User:**
{Clear, specific question}

**Options (if applicable):**
1. {Option 1 and implications}
2. {Option 2 and implications}

**I'm creating/updating questions.md to track this question. Will wait for your answer before proceeding with iteration {N}.**

Creating question in questions.md...
```

---

## User Interaction Prompts

### Presenting Options to User

**Situation:** Agent needs user decision (e.g., feature breakdown in Stage 1)

**Agent MUST respond:**

```
I need your decision on {topic}. Here are the options I've identified...

**Context:**
{Brief context for why decision is needed}

**Option 1: {Option Name}**
**Description:** {What this option means}
**Pros:**
- {Pro 1}
- {Pro 2}
**Cons:**
- {Con 1}
- {Con 2}
**Implications:** {What happens if this option is chosen}

**Option 2: {Option Name}**
**Description:** {What this option means}
**Pros:**
- {Pro 1}
- {Pro 2}
**Cons:**
- {Con 1}
- {Con 2}
**Implications:** {What happens if this option is chosen}

{Continue for all options}

**My Recommendation:** Option {N} - {Option Name}
**Reason:** {Why this is recommended}

Which option would you like to proceed with?

Waiting for your decision...
```

---

### Asking for Clarification

**Situation:** Agent needs user to clarify requirements

**Agent MUST respond:**

```
I need clarification on {topic} before I can proceed correctly...

**What I'm trying to do:**
{Context - current task/step}

**What's unclear:**
{Specific area that needs clarification}

**Why this matters:**
{Impact of getting this wrong}

**My current understanding:**
{What agent thinks is meant}

**Please clarify:**
{Specific question}

**Examples (if helpful):**
- Scenario A: {example scenario 1}
- Scenario B: {example scenario 2}

Which scenario aligns with your intent, or is there a different approach?

Waiting for your clarification...
```

---

## Anti-Patterns to Avoid

**These are UNACCEPTABLE responses when starting a stage:**

### ❌ WRONG: "I'm familiar with the process"

```
❌ DON'T SAY THIS:
"I'm familiar with Stage 5a, let me start the TODO creation..."
```

**Why wrong:** No proof you read the guide. Leads to guide abandonment.

**✅ CORRECT:**
```
I'm reading `STAGE_5aa_round1_guide.md` to ensure I follow all 8 iterations in Round 1...
{List critical requirements for Round 1}
```

---

### ❌ WRONG: Generic acknowledgment

```
❌ DON'T SAY THIS:
"I'll follow the guide for Stage 5c..."
```

**Why wrong:** No proof you read it. No accountability for specific requirements.

**✅ CORRECT:**
```
I'm reading `STAGE_5ca_smoke_testing_guide.md`...
**The guide requires:**
- Part 1: Import test
- Part 2: Entry point test
- Part 3: E2E execution test (CRITICAL - verify OUTPUT DATA VALUES)
- Re-reading checkpoints after Parts 2 and 3
- MANDATORY GATE before QC rounds
{Continue with specific requirements}
```

---

### ❌ WRONG: Skipping prerequisite verification

```
❌ DON'T SAY THIS:
"Starting Stage 5b implementation..."
```

**Why wrong:** Might not be ready. Could be missing prerequisites.

**✅ CORRECT:**
```
**Prerequisites I'm verifying:**
✅ Stage 5a complete (24 iterations done)
✅ Iteration 24: Implementation Readiness = PASSED
✅ todo.md exists with complete task list
{Verify ALL prerequisites}
```

---

### ❌ WRONG: Not updating Agent Status

```
❌ DON'T SAY THIS:
{Just starts working without updating README}
```

**Why wrong:** Work is lost if session compacts. No resumability.

**✅ CORRECT:**
```
**Updating feature README Agent Status:**
- Current Phase: {PHASE}
- Current Guide: {guide_name}.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: {list 3-5 rules}
- Next Action: {exact next step}
```

---

## Summary

**When to use these prompts:**
- Starting ANY stage (1-7)
- Starting ANY sub-stage (5a-5e)
- Creating bug fixes
- Resuming after compaction
- Encountering problems

**Why prompts are mandatory:**
1. Proves guide was read
2. Lists critical requirements
3. Verifies prerequisites
4. Updates Agent Status for persistence
5. Prevents guide abandonment (40% failure rate without)

**Key principles:**
- READ the guide FIRST (use Read tool)
- LIST critical requirements (proves you read it)
- VERIFY prerequisites (ensures readiness)
- UPDATE Agent Status (enables resumability)
- THEN proceed with work

**Remember:** These prompts take 2-3 minutes but prevent hours of rework. NEVER skip them.

---

**END OF PROMPTS REFERENCE v2**
