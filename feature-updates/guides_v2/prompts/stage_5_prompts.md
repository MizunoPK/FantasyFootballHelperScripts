# Stage 5 Prompts: Feature Implementation

**Stage:** 5 (All sub-stages: 5a, 5b, 5c, 5d, 5e)
**Purpose:** Feature implementation workflow from implementation planning through epic test plan update

---

## Starting Stage 5a: Implementation Planning (Round 1)

**User says:** "Prepare for updates based on {feature_name}" or "Start implementation of feature_01" or "Create implementation plan"

**Prerequisite:** Stage 4 complete (Gate 4.5 passed - user approved test plan) AND feature spec.md complete AND checklist.md resolved

**Note:** Stage 5a is split into 5 separate guides for better digestibility:
- **stages/s5/s5_p1_planning_round1.md** - Round 1: Iterations 1-7 + 4a (START HERE)
- **stages/s5/s5_p2_planning_round2.md** - Round 2: Iterations 8-16
- **stages/s5/round3_todo_creation.md** - Round 3 router (links to Part 1/2a/2b)
- **stages/s5/s5_p3_planning_round3.md** - Round 3 Part 1: Iterations 17-22
- **stages/s5/5.1.3.2_round3_part2a.md** - Round 3 Part 2a: Iterations 23, 23a
- **stages/s5/5.1.3.3_round3_part2b.md** - Round 3 Part 2b: Iterations 25, 24

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p1_planning_round1.md` to ensure I follow all 8 iterations in Round 1...

**The guide requires:**
- **🚨 CRITICAL: IMPLEMENTATION TASKS MUST TRACE TO SPEC REQUIREMENTS**:
  - Every implementation task must map to explicit spec.md requirement
  - Do NOT add tasks based on "best practices" or assumptions
  - Do NOT add tasks the user didn't ask for
  - If uncertain about a task → create question in questions.md
  - Only create implementation tasks for confirmed, documented requirements
- **Round 1: 8 MANDATORY iterations** (NO SKIPPING):
  - Iterations 1-7 + iteration 4a (Implementation Plan Specification Audit)
- **Iteration 4a is a MANDATORY GATE**:
  - Every implementation task MUST have acceptance criteria
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
✅ Stage 4 complete (Gate 4.5 passed - user approved test plan)
✅ No pending questions from Stage 2

**I'll now proceed with Round 1 (iterations 1-7 + 4a). I'll create questions.md after Round 1 checkpoint if needed.**

**Updating feature README Agent Status:**
- Current Phase: IMPLEMENTATION_PLANNING
- Current Guide: stages/s5/s5_p1_planning_round1.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Implementation tasks MUST trace to spec requirements (no assumptions)", "8 iterations mandatory (Round 1)", "Iteration 4a is MANDATORY GATE", "STOP if confidence < Medium", "Interface verification: READ actual code"
- Progress: 0/8 iterations complete (Round 1)
- Next Action: Begin iteration 1 - Requirements Coverage Check

Starting iteration 1...
```

---

## Starting Stage 5a: Implementation Planning (Round 2)

**User says:** Agent detects Round 1 complete (8/8 iterations done, confidence >= MEDIUM)

**Prerequisite:** Round 1 complete (Part 5.1.1), Iteration 4a PASSED, confidence >= MEDIUM

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p2_planning_round2.md` to ensure I follow all 9 iterations in Round 2...

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
✅ implementation_plan.md created with acceptance criteria for all tasks

**I'll now proceed with Round 2 (iterations 8-16).**

**Updating feature README Agent Status:**
- Current Phase: IMPLEMENTATION_PLANNING
- Current Guide: stages/s5/s5_p2_planning_round2.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "9 iterations mandatory (Round 2)", "Re-verification iterations are CRITICAL", "Test coverage >90% required"
- Progress: 8/24 total iterations complete (starting Round 2)
- Next Action: Begin iteration 8 - Test Strategy Development

Starting iteration 8...
```

---

## Starting Stage 5a Round 3 Part 1: Implementation Planning (Preparation)

**User says:** Agent detects Round 2 complete (16/28 iterations done, confidence >= MEDIUM, test coverage >90%)

**Prerequisite:** Round 2 complete (Part 5.1.2), confidence >= MEDIUM, test coverage >90%

**Note:** Round 3 is split into 3 parts for better navigation:
- **stages/s5/s5_p3_planning_round3.md** - Iterations 17-22 (START HERE)
- **stages/s5/5.1.3.2_round3_part2a.md** - Iterations 23, 23a (Gates 1-2)
- **stages/s5/5.1.3.3_round3_part2b.md** - Iterations 25, 24 (Gate 3 + GO/NO-GO)

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p3_planning_round3.md` to ensure I follow all 6 preparation iterations in Round 3 Part 1...

**The guide requires:**
- **Part 1: 6 preparation iterations** (NO SKIPPING):
  - Iteration 17: Implementation Phasing
  - Iteration 18: Rollback Strategy
  - Iteration 19: Algorithm Traceability Matrix (Final)
  - Iteration 20: Performance Considerations
  - Iteration 21: Mock Audit & Integration Test Plan (CRITICAL)
  - Iteration 22: Output Consumer Validation
- **Implementation Phasing** (Iteration 17):
  - Break implementation into 5-6 phases with checkpoints
  - Prevents "big bang" integration failures
- **Mock Audit** (Iteration 21 - CRITICAL):
  - Verify EACH mock matches real interface (READ actual source code)
  - Plan at least 3 integration tests with REAL objects (NO MOCKS)
  - Prevents unit tests passing with wrong mocks
- **Performance Optimization** (Iteration 20):
  - Identify O(n²) algorithms, optimize to O(n)
  - Document performance requirements

**Why Round 3 Part 1 matters:**
- Preparation iterations ensure implementation is well-planned
- Final algorithm traceability prevents missing requirements
- Mock audit prevents interface mismatch bugs

**Prerequisites I'm verifying:**
✅ Round 2 complete (16/28 iterations)
✅ Test coverage: >90%
✅ Confidence: >= MEDIUM (from Round 2 checkpoint)
✅ Algorithm Traceability Matrix updated (Round 2)
✅ Integration Gap Check updated (Round 2)

**I'll now proceed with Round 3 Part 1 (iterations 17-22).**

**Updating feature README Agent Status:**
- Current Phase: IMPLEMENTATION_PLANNING
- Current Guide: stages/s5/s5_p3_planning_round3.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "6 preparation iterations mandatory", "Iteration 21: Verify mocks against ACTUAL source code", "Integration tests must use REAL objects"
- Progress: 16/24 total iterations complete (starting Round 3 Part 1)
- Next Action: Begin iteration 17 - Implementation Phasing

Starting iteration 17...
```

---

## Starting Stage 5a Round 3 Part 2: Implementation Planning (Final Gates)

**User says:** Agent detects Round 3 Part 1 complete (22/28 iterations done)

**Prerequisite:** Round 3 Part 1 complete (Part 5.1.3.1), Iterations 17-22 done

**Agent MUST respond:**

```
I'm reading `stages/s5/5.1.3.2_round3_part2a.md` (Part 2a) and `stages/s5/5.1.3.3_round3_part2b.md` (Part 2b) to ensure I follow all 4 final gate iterations in Round 3 Part 2...

**The guide requires:**
- **Part 2: 4 final gate iterations containing ALL 3 MANDATORY GATES**:
  - Iteration 23: Integration Gap Check (Final)
  - Iteration 23a: Pre-Implementation Spec Audit (MANDATORY GATE - 4 PARTS)
  - Iteration 25: Spec Validation Against Validated Documents (CRITICAL GATE)
  - Iteration 24: Implementation Readiness Protocol (FINAL GATE - GO/NO-GO)
- **Iteration 23a (Pre-Implementation Spec Audit) has 4 MANDATORY PARTS**:
  - Part 1: Completeness Audit (Coverage = 100%)
  - Part 2: Specificity Audit (Specificity = 100%)
  - Part 3: Interface Contracts Audit (Verification = 100%)
  - Part 4: Integration Evidence Audit (Integration = 100%)
  - ALL 4 PARTS must show 100% metrics with evidence (cite specific numbers)
- **Iteration 25 (Spec Validation) - CRITICAL GATE**:
  - Close spec.md first (avoid confirmation bias)
  - Re-read validated documents independently: epic notes + epic ticket + spec summary
  - Three-way comparison: spec.md vs all three validated sources
  - IF ANY DISCREPANCIES → STOP and report to user with 3 options
  - Prevents catastrophic bugs (Feature 02 bug: spec misinterpreted epic notes)
- **Iteration 24 (Implementation Readiness) - FINAL GATE**:
  - GO/NO-GO decision required
  - CANNOT proceed to Stage 5b without "GO" decision
  - GO requires: confidence >= MEDIUM, all gates PASSED, all checklists complete

**Why Round 3 Part 2 matters:**
- Contains ALL 3 mandatory gates that CANNOT be skipped
- Evidence-based verification (must cite specific numbers, provide proof)
- Three-way validation prevents implementing wrong solution
- GO/NO-GO framework prevents implementing with incomplete planning

**Prerequisites I'm verifying:**
✅ Round 3 Part 1 complete (22/28 iterations)
✅ Implementation phasing defined
✅ Rollback strategy documented
✅ Algorithm traceability matrix complete (final)
✅ Mock audit complete (all mocks verified against real interfaces)
✅ Integration test plan created (at least 3 tests with REAL objects)

**I'll now proceed with Round 3 Part 2 (iterations 23, 23a, 25, 24).**

**Updating feature README Agent Status:**
- Current Phase: IMPLEMENTATION_PLANNING
- Current Guide: stages/s5/5.1.3.2_round3_part2a.md (Part 2a, then Part 2b)
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "3 MANDATORY GATES (23a, 25, 24) - CANNOT skip", "Evidence-based verification (cite numbers)", "Close spec.md before Iteration 25", "User decision required if discrepancies"
- Progress: 22/24 total iterations complete (starting Round 3 Part 2)
- Next Action: Begin iteration 23 - Integration Gap Check (Final)

Starting iteration 23...
```

---

## User Approval of Implementation Plan

**User says:** "Review implementation plan" or Agent detects Stage 5a complete (28 iterations done, Iteration 24: Implementation Readiness = PASSED)

**Prerequisite:** Stage 5a complete (28 iterations passed, implementation_plan.md v3.0 created)

**🚨 MANDATORY CHECKPOINT - USER MUST APPROVE implementation_plan.md BEFORE Stage 5b**

**Agent MUST respond:**

```
Stage 5a (Implementation Planning) is complete. I've created implementation_plan.md v3.0 (~400 lines) with:

**Key Sections:**
- Implementation Tasks (mapped to spec.md requirements)
- Component Dependencies Matrix
- Algorithm Traceability Matrix
- Test Strategy (>90% coverage)
- Edge Cases and Error Handling
- Implementation Phasing (5-6 checkpoints)
- Performance Considerations
- Mock Audit Results
- Integration Test Plan

**File Location:** `feature-updates/KAI-{N}-{epic_name}/feature_{XX}_{name}/implementation_plan.md`

**Please review implementation_plan.md and confirm:**
1. Implementation approach makes sense
2. Phasing is reasonable (5-6 checkpoints)
3. Test coverage is adequate (>90%)
4. No missing requirements

**Say "approved" to proceed to Stage 5b (Implementation), or request changes.**

**Note:** This is your opportunity to adjust the implementation approach before code is written. Once approved, I'll create implementation_checklist.md and begin coding.
```

---

## Starting Stage 5b: Implementation

**User says:** "Approved" or "Implement the feature" or "Start coding"

**Prerequisite:** User approved implementation_plan.md from Stage 5a

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p4_execution.md` to ensure I follow the implementation workflow...

**The guide requires:**
- **Create implementation_checklist.md** from implementation_plan.md tasks
- **Keep spec.md VISIBLE** at all times (continuous verification)
- **Use implementation_plan.md as PRIMARY reference** (spec.md provides context)
- Execute implementation tasks in order (following Implementation Phasing)
- **Mini-QC checkpoints** after each major component:
  - Run unit tests
  - Verify against spec
  - Update code_changes.md
- **Run unit tests after each step** (100% pass required)
- **Interface Verification** before integration:
  - Verify interface matches ACTUAL dependency code
  - Do NOT assume - READ the actual source
- NO code-review tone (write production code, not suggestions)
- **Update code_changes.md INCREMENTALLY** (not at the end)
- STOP if stuck or blocked - ask user

**Prerequisites I'm verifying:**
✅ Stage 5a complete (EPIC_README.md shows 28 iterations done)
✅ Iteration 24: Implementation Readiness = PASSED
✅ implementation_plan.md v3.0 exists and user-approved
✅ questions.md resolved (or documented "no questions")

**I'll now create implementation_checklist.md from implementation_plan.md tasks and begin implementation...**

**Updating feature README Agent Status:**
- Current Phase: IMPLEMENTATION
- Current Guide: stages/s5/s5_p4_execution.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "spec.md visible at all times", "implementation_plan.md is PRIMARY reference", "Unit tests after each step (100% pass)", "Mini-QC checkpoints", "Update code_changes.md incrementally"
- Progress: 0/{N} implementation tasks complete
- Next Action: Create implementation_checklist.md from implementation_plan.md tasks

Starting implementation...
```

---

## Starting Stage 5c (Phase 1): Smoke Testing

**User says:** "Validate the implementation" or Agent detects Stage 5b complete

**Prerequisite:** Stage 5b complete (all implementation tasks done, all unit tests passing)

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p5_smoke_testing.md` to ensure I follow the 3-part smoke testing protocol...

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
✅ Stage 5b complete (all implementation tasks done)
✅ ALL unit tests passing (100% pass rate)
✅ code_changes.md updated with all changes
✅ implementation_checklist.md all items verified (all checked off)

**I'll now begin with Part 1: Import Test...**

**Updating feature README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_SMOKE_TESTING
- Current Guide: stages/s5/s5_p5_smoke_testing.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "3 parts MANDATORY", "Verify DATA VALUES not structure", "GATE before QC rounds"
- Progress: 0/3 parts complete
- Next Action: Smoke Test Part 1 - Import test

Running import test for {feature_name}...
```

---

## Starting Stage 5c (Phase 2): QC Rounds

**User says:** "Begin QC rounds" or Agent detects smoke testing passed

**Prerequisite:** Smoke testing complete (all 3 parts passed)

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p6_qc_rounds.md` to ensure I follow the 3-round QC protocol...

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
- Current Guide: stages/s5/s5_p6_qc_rounds.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "3 rounds (no exceptions)", "QC RESTART if critical issues", "Round 3 zero tolerance"
- Progress: 0/3 rounds complete
- Next Action: QC Round 1 - Basic Validation

Starting QC Round 1 for {feature_name}...
```

---

## Starting Stage 5c (Phase 3): Final Review

**User says:** "Begin final review" or Agent detects QC rounds passed

**Prerequisite:** QC rounds complete (all 3 rounds passed, zero issues found in Round 3)

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p7_final_review.md` to ensure I follow the final review protocol...

**The guide requires:**
- **PR Review Protocol** (Multi-round with fresh eyes - MANDATORY):
  - READ: `stages/s5/s5_pr_review_protocol.md` (complete protocol)
  - Hybrid approach: Round 1 (4 specialized reviews) + Rounds 2-5 (comprehensive reviews)
  - Fresh agent spawned for EACH review round (eliminates context bias)
  - Continue until 2 consecutive clean rounds
  - Maximum 5 rounds total
  - User escalation for multi-approach issues
- **Lessons Learned Capture**:
  - Document what worked well
  - Document what didn't work
  - **IMMEDIATELY UPDATE GUIDES** (not just document issues)
  - Example: If QC found zero data issue → update S5.P5 guide NOW
- **Final Verification**:
  - 100% requirement completion (from spec)
  - All code_changes.md items implemented
  - All lessons_learned.md captured
- **Completion Criteria**:
  - PR review: PASSED (2 consecutive clean rounds achieved)
  - Lessons learned: Updated (including guide updates if needed)
  - Final verification: 100% complete

**Prerequisites I'm verifying:**
✅ QC Round 3 complete (zero issues found)
✅ All smoke testing and QC documentation complete
✅ Feature fully functional with real data

**I'll now begin PR Review Protocol (multi-round fresh-eyes approach)...**

**Updating feature README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_FINAL_REVIEW
- Current Guide: stages/s5/s5_p7_final_review.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "PR review protocol MANDATORY", "Fresh agents for each round", "Update guides immediately", "100% completion required"
- Progress: PR Review Protocol starting
- Next Action: READ pr_review_protocol.md and begin Round 1 specialized reviews

Starting PR Review Protocol for {feature_name}...
```

---

## Starting Stage 5d: Cross-Feature Alignment

**User says:** "Review other feature specs" or Agent detects Stage 5c complete

**Prerequisite:** Stage 5c complete (smoke testing passed, QC rounds passed, final review complete)

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p8_cross_feature_alignment.md` to ensure I review all remaining feature specs...

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
  - Return to Stage 5a: >3 new implementation tasks needed, algorithm changes significantly
  - Minor Updates (continue): ≤3 implementation task adjustments, no algorithm changes
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
- Current Guide: stages/s5/s5_p8_cross_feature_alignment.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Review ALL remaining features", "Compare to ACTUAL implementation", "Update specs proactively", "Mark features needing significant rework"
- Next Action: Identify remaining features from Epic Progress Tracker

Starting cross-feature alignment review...
```

---

## Starting Stage 5e: Epic Testing Plan Update

**User says:** "Update epic test plan" or Agent detects Stage 5d complete

**Prerequisite:** Stage 5d complete (all remaining feature specs reviewed and updated)

**Agent MUST respond:**

```
I'm reading `stages/s5/s5_p9_epic_testing_update.md` to ensure I update the epic test plan based on actual implementation...

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
- Current Guide: stages/s5/s5_p9_epic_testing_update.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Review ACTUAL implementation", "Add integration scenarios", "Update History table", "Test plan evolves incrementally"
- Next Action: Read just-completed feature's actual code to identify test plan updates

Starting test plan update...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
