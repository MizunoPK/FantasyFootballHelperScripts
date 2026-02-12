# Feature Loop Prompts: S5-S8

**Stages:** S5-S8 (Feature Loop: S5 Planning, S6 Execution, S7 Testing, S8 Alignment)
**Purpose:** Per-feature workflow from implementation planning through post-feature alignment

---

## Table of Contents

1. [Starting S5 v2: Implementation Planning](#starting-s5-v2-implementation-planning)
1. [Starting S5 v2: Validation Loop Phase](#starting-s5-v2-validation-loop-phase)
1. [Reporting S5 v2: Validation Round Results](#reporting-s5-v2-validation-round-results)
1. [Exiting S5 v2: Validation Loop Complete](#exiting-s5-v2-validation-loop-complete)
1. [S5 v2: Gate 5 - User Approval of Implementation Plan](#s5-v2-gate-5-user-approval-of-implementation-plan)
1. [Starting S6: Implementation](#starting-s6-implementation)
1. [Starting S7.P1: Smoke Testing](#starting-s7p1-smoke-testing)
1. [Starting S7.P2: Feature QC Validation Loop](#starting-s7p2-feature-qc-validation-loop)
1. [Starting S7.P3: Final Review (PR Validation Loop)](#starting-s7p3-final-review-pr-validation-loop)
1. [Starting S8.P1: Cross-Feature Alignment](#starting-s8p1-cross-feature-alignment)
1. [Starting S8.P2: Epic Testing Plan Update](#starting-s8p2-epic-testing-plan-update)

---

## Starting S5 v2: Implementation Planning

**User says:** "Prepare for updates based on {feature_name}" or "Start implementation of feature_01" or "Create implementation plan"

**Prerequisite:** S4 complete (Gate 4.5 passed - user approved test plan) AND feature spec.md complete AND checklist.md resolved

**Note:** S5 v2 uses Validation Loop approach (replaces 22-iteration v1 structure)

**Agent MUST respond:**

```markdown
I'm beginning S5 (Implementation Planning) for {feature_name}.

**Guide I'm following:** stages/s5/s5_v2_validation_loop.md (from CLAUDE.md Stage Workflow table)
**Prerequisites verified:**
- [x] Prior stage (S4) fully complete - test_strategy.md approved by user (Gate 4.5)
- [x] Guide path matches CLAUDE.md Stage Workflow table
- [x] Read ENTIRE guide using Read tool

**The guide requires:**

**Phase 1: Draft Creation (60-90 minutes)**
- Use template: `templates/implementation_plan_template.md`
- Create all 11 dimension sections in implementation_plan.md
- Target: ~70% completeness (known gaps acceptable)
- Time limit: Stop at 90 minutes even if only 70% complete
- Copy VALIDATION_LOOP_LOG_S5_template.md to feature folder

**Phase 2: Validation Loop (3.5-6 hours, typically 6-8 rounds)**
- Validate against 18 dimensions EVERY round (7 master + 11 S5-specific):
- **11 S5-specific dimensions** (create sections in implementation_plan.md):
  1. Requirements Completeness
  2. Interface & Dependency Verification
  3. Algorithm Traceability
  4. Task Specification Quality (embeds Gate 4a)
  5. Data Flow & Consumption
  6. Error Handling & Edge Cases
  7. Integration & Compatibility (embeds Gate 7a)
  8. Test Coverage Quality
  9. Performance & Dependencies
  10. Implementation Readiness
  11. Spec Alignment & Cross-Validation (embeds Gate 23a)
- Fix ALL issues before next round (zero deferred issues)
- Exit when 3 consecutive rounds find zero issues
- Document each round in VALIDATION_LOOP_LOG.md

**🚨 CRITICAL: IMPLEMENTATION TASKS MUST TRACE TO SPEC REQUIREMENTS**:
- Every implementation task must map to explicit spec.md requirement
- Do NOT add tasks based on "best practices" or assumptions
- Do NOT add tasks the user didn't ask for
- If uncertain → document in questions.md

**Interface Verification Protocol**:
- READ actual source code for every dependency
- Do NOT assume interfaces - verify them with file:line references

**Benefits vs S5 v1:**
- 35-50% time reduction (4.5-7 hours vs 9-11 hours)
- No redundancy (v1 had 3x re-verifications)
- Systematic validation (impossible to skip checks)
- Objective quality metric (3 clean rounds prove completeness)

**Prerequisites I'm verifying:**
✅ spec.md exists and is complete
✅ checklist.md all items resolved (all [x])
✅ S4 complete (Gate 4.5 passed - user approved test plan)
✅ No pending questions from S2

**Updating feature README Agent Status:**
- Current Phase: S5_V2_DRAFT_CREATION
- Current Guide: stages/s5/s5_v2_validation_loop.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Implementation tasks MUST trace to spec requirements", "Draft = 70% in 90 min", "Validation Loop: 3 consecutive clean rounds", "18 dimensions ALL rounds (7 master + 11 S5)", "Zero deferred issues", "Interface verification: READ actual code"
- Progress: Phase 1 - Draft Creation
- Next Action: Begin draft creation (target 90 minutes)

Starting Phase 1: Draft Creation...
```

---

## Starting S5 v2: Validation Loop Phase

**User says:** Agent completes draft creation (Phase 1)

**Prerequisite:** Draft implementation_plan.md created with all 11 dimension sections

**Agent MUST respond:**

```markdown
I'm starting S5 v2 Phase 2: Validation Loop...

**The guide requires:**
- **Validation Loop Protocol**: 3 consecutive clean rounds required
- **Check ALL 18 dimensions EVERY round** (7 master + 11 S5-specific, no skipping):
- **11 S5-specific dimensions** (detailed in guide):
  1. Requirements Completeness
  2. Interface & Dependency Verification
  3. Algorithm Traceability
  4. Task Specification Quality
  5. Data Flow & Consumption
  6. Error Handling & Edge Cases
  7. Integration & Compatibility
  8. Test Coverage Quality
  9. Performance & Dependencies
  10. Implementation Readiness
  11. Spec Alignment & Cross-Validation
- **Fix ALL issues immediately** before next round (zero deferral)
- **Document each round** in VALIDATION_LOOP_LOG.md with:
  - Reading pattern used
  - Issues found (count and description)
  - Fixes applied
  - Consecutive clean count
- **Exit criteria**: 3 consecutive rounds with zero issues
- **Escalation**: If >10 rounds, escalate to user

**Reading Patterns (vary each round):**
- Round 1: Sequential (top-to-bottom), focus D1-D4
- Round 2: Reverse (bottom-to-top), focus D5-D8
- Round 3: Spot-checks, focus D9-D11
- Round 4+: Alternate patterns

**Updating feature README Agent Status:**
- Current Phase: S5_V2_VALIDATION_LOOP
- Progress: Round {N}, Clean Count: {X}
- Next Action: Validation Round {N}

Starting Validation Round 1...
```

---

## Reporting S5 v2: Validation Round Results

**After completing each validation round:**

**Agent MUST respond:**

```markdown
**Validation Round {N} Complete**

**Reading Pattern:** {pattern used}
**Duration:** {X minutes}

**Issues Found:** {count}

{If count > 0:}
| Dimension | Issue | Fix Applied |
|-----------|-------|-------------|
| D{N} | {description} | {fix description} |
| ... | ... | ... |

**All issues fixed:** ✅

**Consecutive Clean Count:** RESET to 0 (issues found)

**Next:** Starting Round {N+1} after 2-minute break...

{If count = 0:}
**Zero issues found** ✅

**Consecutive Clean Count:** {X}

{If X < 3:}
**Next:** Proceeding to Round {N+1} (need {3-X} more clean rounds)

{If X = 3:}
**Validation Loop PASSED** - 3 consecutive clean rounds achieved!

**Proceeding to Gate 5: User Approval**
```

---

## Exiting S5 v2: Validation Loop Complete

**When 3 consecutive clean rounds achieved:**

**Agent MUST respond:**

```markdown
**S5 v2 Validation Loop COMPLETE**

**Final Metrics:**
- Total Rounds: {N}
- Total Time: {X hours Y minutes}
- Issues Found Total: {count across all rounds}
- Final Quality: 99%+ (validated by 3 consecutive clean rounds)

**Validation Summary:**
- Draft Creation: {X minutes}
- Validation Rounds: {N rounds in Y hours}
- First Clean Round: Round {N}
- Final Clean Streak: Rounds {N-2}, {N-1}, {N}

**All 11 Dimensions Validated:**
✅ Requirements Completeness
✅ Interface & Dependency Verification
✅ Algorithm Traceability
✅ Task Specification Quality
✅ Data Flow & Consumption
✅ Error Handling & Edge Cases
✅ Integration & Compatibility
✅ Test Coverage Quality
✅ Performance & Dependencies
✅ Implementation Readiness
✅ Spec Alignment & Cross-Validation

**implementation_plan.md is ready for Gate 5: User Approval**

**Updating feature README Agent Status:**
- Current Phase: S5_V2_COMPLETE_AWAITING_GATE_5
- Validation Loop: PASSED (3 consecutive clean rounds)
- Next Action: Present implementation_plan.md to user for Gate 5 approval

Presenting implementation_plan.md to user for approval...
- Next Action: Begin iteration 8 - Test Strategy Development

Starting iteration 8...
```

---

## S5 v2: Gate 5 - User Approval of Implementation Plan

**When:** After S5 v2 validation loop achieves 3 consecutive clean rounds

**Prerequisite:** S5 v2 validation loop complete (PASSED), implementation_plan.md validated to 99%+ quality

**🚨 MANDATORY GATE 5 - USER MUST APPROVE implementation_plan.md BEFORE S6**

**Agent MUST respond:**

```markdown
**S5 v2 (Implementation Planning) Complete**

I've completed the validation loop with 3 consecutive clean rounds. implementation_plan.md is ready for your review (~400 lines):

**Key Sections (validated by 11 dimensions):**
- Implementation Tasks (100% requirements coverage, all with acceptance criteria)
- Component Dependencies Matrix (all interfaces verified from source code)
- Algorithm Traceability Matrix (40+ mappings with file:line references)
- Test Strategy (>90% coverage, includes resume/persistence tests)
- Edge Cases and Error Handling (all enumerated with handling strategy)
- Implementation Phasing (4-6 checkpoints with test validation)
- Performance Considerations (regression analysis, optimization strategy)
- Mock Audit Results (all mocks verified against real interfaces)
- Integration Test Plan (3+ real-object tests, no mocks)
- Data Flow & Consumption (verified downstream consumers)
- Spec Alignment (validated against epic notes, epic ticket, spec summary)

**Validation Metrics:**
- Total Rounds: {N}
- Total Time: {X hours Y minutes}
- Issues Found & Fixed: {count}
- Final Quality: 99%+ (3 consecutive clean validation rounds)

**File Location:** `feature-updates/KAI-{N}-{epic_name}/feature_{XX}_{name}/implementation_plan.md`

**Please review implementation_plan.md and confirm:**
1. Implementation approach makes sense
2. Phasing is reasonable (4-6 checkpoints)
3. Test coverage is adequate (>90%)
4. No missing requirements
5. All 11 validation dimensions look complete

**Say "approved" to proceed to S6 (Implementation), or request changes.**

**Note:** This is your opportunity to adjust the implementation approach before code is written. The validation loop has ensured 99%+ quality, but you have final approval.
```

---

## Starting S6: Implementation

**User says:** "Approved" or "Implement the feature" or "Start coding"

**Prerequisite:** User approved implementation_plan.md from S5

**Agent MUST respond:**

```markdown
I'm reading `stages/s6/s6_execution.md` to ensure I follow the implementation workflow...

**The guide requires:**
- **Create implementation_checklist.md** from implementation_plan.md tasks
- **Keep spec.md VISIBLE** at all times (continuous verification)
- **Use implementation_plan.md as PRIMARY reference** (spec.md provides context)
- Execute implementation tasks in order (following Implementation Phasing)
- **Mini-QC checkpoints** after each major component:
  - Run unit tests
  - Verify against spec
- **Run unit tests after each step** (100% pass required)
- **Interface Verification** before integration:
  - Verify interface matches ACTUAL dependency code
  - Do NOT assume - READ the actual source
- NO code-review tone (write production code, not suggestions)
- STOP if stuck or blocked - ask user

**Prerequisites I'm verifying:**
✅ S5 v2 complete (EPIC_README.md shows Validation Loop passed: 3 consecutive clean rounds)
✅ Phase 2 (Validation Loop) complete: All 11 dimensions validated
✅ implementation_plan.md exists and user-approved (Gate 5)
✅ questions.md resolved (or documented "no questions")

**I'll now create implementation_checklist.md from implementation_plan.md tasks and begin implementation...**

**Updating feature README Agent Status:**
- Current Phase: IMPLEMENTATION
- Current Guide: stages/s6/s6_execution.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "spec.md visible at all times", "implementation_plan.md is PRIMARY reference", "Unit tests after each step (100% pass)", "Mini-QC checkpoints"
- Progress: 0/{N} implementation tasks complete
- Next Action: Create implementation_checklist.md from implementation_plan.md tasks

Starting implementation...
```

---

## Starting S7.P1: Smoke Testing

**User says:** "Validate the implementation" or Agent detects S6 complete

**Prerequisite:** S6 complete (all implementation tasks done, all unit tests passing)

**Agent MUST respond:**

```python
I'm reading `stages/s7/s7_p1_smoke_testing.md` to ensure I follow the 3-part smoke testing protocol...

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
✅ S6 complete (all implementation tasks done)
✅ ALL unit tests passing (100% pass rate)
✅ implementation_checklist.md all items verified (all checked off)

**I'll now begin with Part 1: Import Test...**

**Updating feature README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_SMOKE_TESTING
- Current Guide: stages/s7/s7_p1_smoke_testing.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "3 parts MANDATORY", "Verify DATA VALUES not structure", "GATE before QC rounds"
- Progress: 0/3 parts complete
- Next Action: Smoke Test Part 1 - Import test

Running import test for {feature_name}...
```

---

## Starting S7.P2: Feature QC Validation Loop

**User says:** "Begin QC" or Agent detects smoke testing passed

**Prerequisite:** Smoke testing complete (all 3 parts passed)

**Agent MUST respond:**

```markdown
I'm reading `stages/s7/s7_p2_qc_rounds.md` and `reference/validation_loop_s7_feature_qc.md` to follow the Feature QC Validation Loop...

**The guide requires:**
- **Validation Loop Protocol** (extends Master Validation Loop):
  - Check ALL 12 dimensions EVERY round (7 master + 5 S7 QC-specific)
  - Exit when 3 consecutive rounds find ZERO issues
  - Fix ALL issues immediately before next round (no deferring)
  - Typical: 6-8 rounds total to achieve 3 consecutive clean

- **12 Dimensions Checked Every Round:**
  - Master (7): Empirical Verification, Completeness, Internal Consistency, Traceability, Clarity & Specificity, Upstream Alignment, Standards Compliance
  - S7 QC (5): Cross-Feature Integration, Error Handling Completeness, End-to-End Functionality, Test Coverage Quality, Requirements Completion

- **Key Difference from Old Approach:**
  - OLD: Sequential rounds checking different concerns → Any issue → Restart from S7.P1
  - NEW: All dimensions checked every round → Fix immediately → Continue until 3 consecutive clean
  - Time savings: 60-180 min per bug (no restart overhead)

- **Fresh Eyes Every Round:**
  - Take 2-5 minute break between rounds
  - Re-read ENTIRE codebase using Read tool
  - Use different reading patterns (sequential, reverse, spot-checks)

**Prerequisites I'm verifying:**
✅ Smoke testing complete (all 3 parts passed)
✅ Part 3 verified OUTPUT DATA VALUES (not just structure)
✅ All unit tests passing (100% pass rate)

**I'll now begin Validation Round 1...**

**Updating feature README Agent Status:**
- Current Phase: S7.P2 (Feature QC Validation Loop)
- Current Guide: reference/validation_loop_s7_feature_qc.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "12 dimensions checked every round", "3 consecutive clean rounds required", "Fix issues immediately (no restart)", "100% tests passing"
- Progress: Round 1, Clean Count: 0
- Next Action: Validation Round 1 - Sequential Review + Test Verification

Starting Validation Round 1 for {feature_name}...
```

---

## Starting S7.P3: Final Review (PR Validation Loop)

**User says:** "Begin final review" or Agent detects S7.P2 complete

**Prerequisite:** S7.P2 Feature QC complete (3 consecutive clean rounds achieved)

**Agent MUST respond:**

```markdown
I'm reading `stages/s7/s7_p3_final_review.md` and `reference/validation_loop_qc_pr.md` to follow the PR Validation Loop...

**The guide requires:**
- **PR Validation Loop Protocol** (extends Master Validation Loop):
  - READ: `reference/validation_loop_qc_pr.md` (complete protocol)
  - Check ALL 11 PR categories + 7 master dimensions EVERY round
  - Exit when 3 consecutive rounds find ZERO issues
  - Fresh eyes through re-reading and breaks (NOT agent spawning)
  - Fix ALL issues immediately before next round (no deferring)
  - Typical: 4-6 rounds to achieve 3 consecutive clean
- **11 PR Categories:**
  1. Code Quality & Standards
  2. Test Coverage & Quality
  3. Security & Data Handling
  4. Documentation Completeness
  5. Error Handling
  6. Integration Points
  7. Performance Considerations
  8. Backwards Compatibility
  9. Configuration & Dependencies
  10. Edge Cases & Validation
  11. Commit History & Messages
- **Lessons Learned Capture**:
  - Document what worked well
  - Document what didn't work
  - **IMMEDIATELY UPDATE GUIDES** (not just document issues)
- **Completion Criteria**:
  - PR validation: PASSED (3 consecutive clean rounds achieved)
  - Lessons learned: Updated (including guide updates if needed)
  - Final verification: 100% complete

**Prerequisites I'm verifying:**
- S7.P2 complete (3 consecutive clean rounds achieved in Feature QC)
- All smoke testing and QC documentation complete
- Feature fully functional with real data

**I'll now begin PR Validation Loop (re-reading fresh-eyes approach)...**

**Updating feature README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_FINAL_REVIEW
- Current Guide: stages/s7/s7_p3_final_review.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "PR Validation Loop MANDATORY", "3 consecutive clean rounds to exit", "Update guides immediately", "100% completion required"
- Progress: PR Validation Loop starting
- Next Action: Begin Round 1 - check all 11 PR categories + 7 master dimensions

Starting PR Validation Loop for {feature_name}...
```

---

## Starting S8.P1: Cross-Feature Alignment

**User says:** "Review other feature specs" or Agent detects S7 complete

**Prerequisite:** S7 complete (smoke testing passed, QC rounds passed, final review complete)

**Agent MUST respond:**

```markdown
I'm reading `stages/s8/s8_p1_cross_feature_alignment.md` to ensure I review all remaining feature specs...

**The guide requires:**
- Review ALL remaining features (not yet at S7)
  - Identify remaining features from EPIC_README.md Epic Progress Tracker
- For EACH remaining feature (SEQUENTIAL):
  - Read feature spec.md with fresh eyes
  - Read just-completed feature's ACTUAL code (not plans)
  - Compare spec assumptions to actual implementation
  - Identify misalignments
  - Update spec.md and checklist.md
  - Mark for rework if significant changes needed
- **Significant Rework Criteria:**
  - Return to S1: Feature should be split, or no longer needed
  - Return to S2: Spec assumptions fundamentally wrong
  - Return to S5: >3 new implementation tasks needed, algorithm changes significantly
  - Minor Updates (continue): ≤3 implementation task adjustments, no algorithm changes
- **Compare to ACTUAL implementation** (not the plan from S5)
- Document insights in just-completed feature's spec.md
- Final verification: No remaining features need significant rework

**Why this matters:**
- Implementation reveals reality (assumptions often wrong)
- Prevents cascading issues
- Ensures remaining features align with actual code

**Prerequisites I'm verifying:**
✅ S7 complete (smoke testing, QC, PR review all passed)
✅ EPIC_README.md shows which features are remaining
✅ Just-completed feature's code accessible for review

**I'll now identify remaining features and review them sequentially...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: S8.P1 - Cross-Feature Alignment
- Current Guide: stages/s8/s8_p1_cross_feature_alignment.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Review ALL remaining features", "Compare to ACTUAL implementation", "Update specs proactively", "Mark features needing significant rework"
- Next Action: Identify remaining features from Epic Progress Tracker

Starting cross-feature alignment review...
```

---

## Starting S8.P2: Epic Testing Plan Update

**User says:** "Update epic test plan" or Agent detects S8.P1 complete

**Prerequisite:** S8.P1 complete (all remaining feature specs reviewed and updated)

**Agent MUST respond:**

```bash
I'm reading `stages/s8/s8_p2_epic_testing_update.md` to ensure I update the epic test plan based on actual implementation...

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
  - S1: Placeholder
  - S4: Based on specs
  - S8.P2: Based on actual implementation (THIS stage)
  - S9: Execute evolved plan

**Why this matters:**
- Implementation often differs from specs
- New integration points discovered during coding
- Test plan must reflect REALITY for S9 to be effective

**Prerequisites I'm verifying:**
✅ S8.P1 complete (all remaining features reviewed)
✅ Just-completed feature fully implemented and QC'd
✅ epic_smoke_test_plan.md accessible

**I'll now review the actual implementation and identify test plan updates...**

**Updating EPIC_README.md Agent Status:**
- Current Stage: S8.P2 - Epic Testing Plan Update
- Current Guide: stages/s8/s8_p2_epic_testing_update.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Critical Rules: "Review ACTUAL implementation", "Add integration scenarios", "Update History table", "Test plan evolves incrementally"
- Next Action: Read just-completed feature's actual code to identify test plan updates

Starting test plan update...
```

---

*For prompts for other stages, see the [prompts index](../prompts_reference_v2.md)*
