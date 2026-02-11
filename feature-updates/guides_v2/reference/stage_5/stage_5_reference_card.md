# STAGE 5: Feature Implementation - Quick Reference Card (v2)

**Purpose:** Visual map of S5 v2 Validation Loop workflow and mandatory gates
**Use Case:** Quick lookup for workflow navigation, restart points, and gate requirements
**Total Time:** 4.5-7 hours typical per feature (varies by complexity)
**Version:** S5 v2 Validation Loop (replaces 22-iteration structure)

---

## Workflow Diagram (S5 v2 Validation Loop)

```text
STAGE 5: Implementation Planning (4.5-7 hours typical, 6-8 validation rounds)
    │
    ├─ Phase 1: Draft Creation (stages/s5/s5_v2_validation_loop.md)
    │   Duration: 60-90 minutes
    │   ├─ Merge test_strategy.md from S4
    │   ├─ Cover all 11 validation dimensions
    │   ├─ Create implementation_plan.md draft (~400 lines)
    │   └─ Output: Ready-for-validation draft
    │
    └─ Phase 2: Validation Loop (stages/s5/s5_v2_validation_loop.md)
        Duration: 3.5-6 hours (typically 6-8 rounds, max 10)
        Exit Criteria: 3 consecutive clean rounds ← MANDATORY
        │
        ├─ Round N: Validate ALL 11 Dimensions
        │   ├─ D1: Requirements Completeness
        │   ├─ D2: Interface & Dependency Verification
        │   ├─ D3: Algorithm Traceability
        │   ├─ D4: Task Specification Quality ← EMBEDS Gate 3a
        │   ├─ D5: Data Flow & Consumption
        │   ├─ D6: Error Handling & Edge Cases
        │   ├─ D7: Integration & Compatibility
        │   ├─ D8: Test Coverage Quality
        │   ├─ D9: Performance & Dependencies
        │   ├─ D10: Implementation Readiness ← EMBEDS Gate 24
        │   └─ D11: Spec Alignment & Cross-Validation ← EMBEDS Gates 23a, 25
        │
        ├─ Fix ALL Issues Immediately (ZERO deferred issues)
        ├─ Count consecutive clean rounds
        └─ Exit when 3 consecutive clean rounds achieved
        ↓
STAGE 5b: Implementation Execution (stages/s6/s6_execution.md)
    1-4 hours (varies by complexity)
    ├─ Create implementation_checklist.md from implementation_plan.md tasks
    ├─ Execute implementation_plan.md tasks (PRIMARY reference)
    ├─ Keep spec.md visible (continuous verification)
    ├─ Mini-QC checkpoints every 5-7 tasks
    └─ 100% test pass required before completing
        ↓
STAGE 5c: Post-Implementation (1.5-2.5 hours, 3 phases)
    │
    ├─ Phase 1: Smoke Testing (stages/s7/s7_p1_smoke_testing.md)
    │   ├─ Part 1: Import Test
    │   ├─ Part 2: Entry Point Test
    │   └─ Part 3: E2E Test (verify DATA VALUES) ← MANDATORY GATE
    │
    ├─ Phase 2: Validation Loop (stages/s7/s7_p2_qc_rounds.md)
    │   ├─ Check ALL 11 dimensions every round
    │   ├─ Fix issues immediately, reset clean counter
    │   └─ 3 consecutive clean rounds required ← MANDATORY
    │
    └─ Phase 3: Final Review (stages/s7/s7_p3_final_review.md)
        ├─ PR review (11 categories)
        ├─ Lessons learned documentation
        └─ Zero tech debt tolerance
        ↓
STAGE 5d: Cross-Feature Spec Alignment (stages/s8/s8_p1_cross_feature_alignment.md)
    15-30 minutes
    └─ Update remaining feature specs based on actual implementation
        ↓
STAGE 5e: Testing Plan Update (stages/s8/s8_p2_epic_testing_update.md)
    15-30 minutes
    └─ Reassess epic_smoke_test_plan.md
        ↓
Next Feature (loop S5→S6→S7→S8) OR STAGE 6 (if all features done)
```

---

## Sub-Stage Summary Table (S5 v2)

| Stage | Guide | Time | Key Activities | Mandatory Gates |
|-------|-------|------|----------------|-----------------|
| S5.P1 | stages/s5/s5_v2_validation_loop.md | 60-90 min | Draft creation, merge S4 test strategy | Draft ready |
| S5.P2 | stages/s5/s5_v2_validation_loop.md | 3.5-6 hrs | Validation Loop (11 dimensions × 6-8 rounds) | 3 consecutive clean rounds, Gates 3a/23a/24/25 embedded |
| S6 | stages/s6/s6_execution.md | 1-4 hrs | Execute implementation_plan.md tasks | 100% test pass |
| S7.P1 | stages/s7/s7_p1_smoke_testing.md | 30-45 min | Import, entry point, E2E tests | Part 3 data values |
| S7.P2 | stages/s7/s7_p2_qc_rounds.md | 45-75 min | Validation Loop, 11 dimensions | 3 consecutive clean rounds |
| S7.P3 | stages/s7/s7_p3_final_review.md | 30-45 min | PR review, lessons learned | Zero tech debt |
| S8.P1 | stages/s8/s8_p1_cross_feature_alignment.md | 15-30 min | Update remaining specs | None |
| S8.P2 | stages/s8/s8_p2_epic_testing_update.md | 15-30 min | Update epic test plan | None |

---

## Mandatory Gates Across S5

### S5: TODO Creation (4 gates)

**Gate 1: Iteration 4a - TODO Specification Audit**
- **Location:** stages/s5/s5_v2_validation_loop.md
- **Criteria:** ALL TODO tasks have acceptance criteria
- **Evidence:** Task count, criteria count, 100% coverage
- **If FAIL:** Add missing acceptance criteria, re-run Iteration 4a

**Gate 2 (Gate 23a): Pre-Implementation Spec Audit**
- **Location:** stages/s5/s5_v2_validation_loop.md (Dimension 11)
- **Embedded in:** Dimension 11 (Spec Alignment & Cross-Validation)
- **Criteria:** ALL 5 PARTS must PASS with 100% metrics
  - Part 1: Completeness Audit (all requirements have implementation tasks)
  - Part 2: Specificity Audit (all tasks have criteria, location, tests)
  - Part 3: Interface Contracts Audit (all dependencies verified from source)
  - Part 4: Integration Evidence Audit (all methods have callers)
  - Part 5: Cross-validation (spec.md matches validated sources)
- **Evidence:** Cite specific numbers (N requirements, M tasks, coverage %)
- **If FAIL:** Fix issues immediately, re-validate in next round

**Gate 3 (Gate 25): Spec Validation Check**
- **Location:** stages/s5/s5_v2_validation_loop.md (Dimension 11)
- **Embedded in:** Dimension 11 (Spec Alignment & Cross-Validation)
- **Criteria:** Spec.md matches ALL three validated sources (epic notes + epic ticket + spec summary)
- **Process:** Close spec.md first, re-read validated docs independently, three-way comparison
- **If ANY DISCREPANCIES:** STOP, report to user with 3 options
- **Critical:** Prevents spec misinterpretation bugs
- **If FAIL:** User decides next action (fix spec + restart, fix spec + continue, discuss)

**Gate 4 (Gate 24): Implementation Readiness (GO/NO-GO)**
- **Location:** stages/s5/s5_v2_validation_loop.md (Dimension 10)
- **Embedded in:** Dimension 10 (Implementation Readiness)
- **Criteria:** GO decision required (confidence >= MEDIUM, all embedded gates PASSED, checklists complete)
- **If NO-GO:** Address concerns, cannot proceed to S6
- **If GO:** Proceed to S6 implementation

### S7: Post-Implementation (2 gates)

**Gate 5: S7.P1 Part 3 - E2E Smoke Test (Data Values)**
- **Location:** stages/s7/s7_p1_smoke_testing.md
- **Criteria:** E2E test with REAL data, verify DATA VALUES (not just file existence)
- **If FAIL:** Restart from S7.P1 Step 1

**Gate 6: S7.P2 Validation Loop - 3 Consecutive Clean Rounds**
- **Location:** stages/s7/s7_p2_qc_rounds.md
- **Criteria:** 3 consecutive rounds with ZERO issues found
- **If issues found:** Fix immediately, reset counter, continue (fix-and-continue approach)

---

## Validation Loop Protocol

**If smoke testing fails (S7.P1):**
→ Fix issues, restart from S7.P1 Step 1 (Import Test)

**If issues found during Validation Loop (S7.P2):**
→ Fix issues immediately, reset clean counter to 0, continue validation
→ No restart needed - fix-and-continue approach
→ Continue until 3 consecutive clean rounds achieved

**If PR review finds critical issues (S7.P3):**
→ Fix issues, restart from S7.P1 Step 1 (smoke testing)

**Why fix-and-continue?**
- Check ALL 11 dimensions every round
- Fix issues immediately when found
- More efficient than full restart protocol
- Zero tech debt tolerance - no deferring issues

---

## Time Estimates by Complexity

### Simple Feature (10-15 TODO tasks)
- 5a: 2 hours
- 5b: 1 hour
- 5c: 1.5 hours
- 5d+5e: 30 minutes
- **Total:** ~5 hours

### Medium Feature (20-30 TODO tasks)
- 5a: 2.5 hours
- 5b: 2 hours
- 5c: 2 hours
- 5d+5e: 45 minutes
- **Total:** ~7 hours

### Complex Feature (35+ TODO tasks - consider splitting)
- 5a: 3 hours
- 5b: 3-4 hours
- 5c: 2.5 hours
- 5d+5e: 1 hour
- **Total:** ~10 hours

---

## Critical Rules Summary

### S5 (TODO Creation)
- ✅ Complete Validation Loop: all 11 dimensions, 3 consecutive clean rounds (no skipping)
- ✅ Execute iterations IN ORDER (not parallel)
- ✅ Pass ALL 4 mandatory gates (4a, 23a, 25, 24)
- ✅ Achieve >90% test coverage (Round 2)
- ✅ Evidence-based verification (cite specific numbers)
- ✅ Close spec.md before Iteration 21 (avoid confirmation bias)

### S6 (Implementation)
- ✅ Keep spec.md VISIBLE at all times
- ✅ Mini-QC checkpoints every 5-7 TODO tasks
- ✅ 100% unit test pass after each step
- ✅ Interface verification against ACTUAL source code

### S7 (Post-Implementation)
- ✅ Verify DATA VALUES in smoke testing (not just file existence)
- ✅ Validation Loop requires 3 consecutive clean rounds
- ✅ If issues found → fix immediately, reset counter, continue
- ✅ Zero tech debt tolerance (fix ALL issues immediately)
- ✅ PR review covers all 11 categories

### S8.P1 & 5e
- ✅ Update specs ONLY for remaining (not yet implemented) features
- ✅ Reassess epic test plan after EACH feature completes

---

## Common Pitfalls

### ❌ Pitfall 1: Skipping Iterations
**Problem:** "Iteration 19 looks similar to 4, I'll skip it"
**Impact:** Missing algorithm mappings, bugs escape to QC
**Solution:** ALL 11 dimensions are mandatory (each catches different issue types), and 3 consecutive clean rounds required

### ❌ Pitfall 2: Just Checking Boxes (No Evidence)
**Problem:** Saying "Coverage = 100%" without citing N requirements, M tasks
**Impact:** Gates FAIL (no evidence = didn't actually verify)
**Solution:** Cite specific numbers for every verification

### ❌ Pitfall 3: Not Closing Spec.md in Iteration 21
**Problem:** Reading spec.md while comparing to epic notes
**Impact:** Confirmation bias - see what you expect, not what's written
**Solution:** Close spec.md FIRST, re-read validated docs independently

### ❌ Pitfall 4: Skipping Smoke Testing After Bug Fix
**Problem:** "I only changed one line, smoke testing not needed"
**Impact:** Small change breaks integration, bugs escape to S9
**Solution:** ALWAYS restart from smoke testing after ANY code change

### ❌ Pitfall 5: Deferring QC Issues to "Later"
**Problem:** "This is minor, I'll fix it after S9"
**Impact:** Tech debt accumulates, bugs compound, rework in production
**Solution:** Zero tech debt tolerance - fix ALL issues immediately

### ❌ Pitfall 6: Mock Audit Assumptions (Iteration 21)
**Problem:** "I assume this mock matches the real interface"
**Impact:** Unit tests pass with wrong mocks, integration tests fail
**Solution:** READ actual source code, verify EACH mock against real interface

---

## When to Use Which Guide (S5 v2)

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting implementation planning | stages/s5/s5_v2_validation_loop.md (Phase 1: Draft Creation) |
| Draft complete, starting validation | stages/s5/s5_v2_validation_loop.md (Phase 2: Validation Loop) |
| Validation round N complete | stages/s5/s5_v2_validation_loop.md (continue to Round N+1) |
| 3 consecutive clean rounds achieved | stages/s6/s6_execution.md (proceed to implementation) |
| Implementation complete | stages/s7/s7_p1_smoke_testing.md |
| Smoke testing passed | stages/s7/s7_p2_qc_rounds.md |
| Validation Loop passed | stages/s7/s7_p3_final_review.md |
| PR review passed | stages/s8/s8_p1_cross_feature_alignment.md |
| Alignment updated | stages/s8/s8_p2_epic_testing_update.md |

---

## Exit Conditions

**S5 is complete for a feature when (v2):**
- [ ] Draft creation complete (implementation_plan.md created)
- [ ] Validation Loop complete (3 consecutive clean rounds, all 11 dimensions passing)
- [ ] All embedded gates passed (Gates 3a, 23a, 24, 25)
- [ ] User approval received (Gate 5)
- [ ] Implementation ready to execute in S6
- [ ] Validation Loop passed (3 consecutive clean rounds)
- [ ] PR review passed (all 11 categories)
- [ ] Lessons learned documented
- [ ] Remaining feature specs updated (S8.P1)
- [ ] Epic test plan updated (S8.P2)

**Next Action:**
- If more features to implement → Loop to S5 for next feature
- If all features complete → Proceed to S9 (Epic-Level Final QC)

---

**Last Updated:** 2026-01-02
