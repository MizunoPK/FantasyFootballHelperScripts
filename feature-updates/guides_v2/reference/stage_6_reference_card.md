# STAGE 6: Epic-Level Final QC - Quick Reference Card

**Purpose:** One-page summary for epic-level testing, QC rounds, and final review
**Use Case:** Quick lookup when validating entire epic as cohesive system
**Total Time:** 4-6 hours (8 steps across 3 sub-stages)

---

## Workflow Overview

```
STAGE_6a: Epic Smoke Testing (60-90 min)
    ├─ Step 1: Pre-QC Verification (15 min)
    │   ├─ Verify all features at Stage 5e
    │   ├─ No pending bug fixes
    │   └─ All unit tests passing
    ├─ Step 2: Epic Smoke Testing (45-75 min)
    │   ├─ Part 1: Import Test (all features import successfully)
    │   ├─ Part 2: Entry Point Test (main entry points work)
    │   ├─ Part 3: E2E Execution Test (verify DATA VALUES)
    │   └─ Part 4: Cross-Feature Integration Test ← MANDATORY GATE
    │       └─ If FAIL → Fix and restart from Part 1
    ↓
STAGE_6b: Epic QC Rounds (2-3 hours)
    ├─ Step 3: QC Round 1 - Cross-Feature Integration (45-60 min)
    │   ├─ Integration points tested
    │   ├─ Data flow verification
    │   ├─ Interface compatibility
    │   └─ Error propagation across features
    ├─ Step 4: QC Round 2 - Epic Cohesion & Consistency (45-60 min)
    │   ├─ Code style consistency
    │   ├─ Naming conventions alignment
    │   ├─ Error handling patterns
    │   └─ Architectural patterns
    ├─ Step 5: QC Round 3 - End-to-End Success Criteria (30-45 min)
    │   ├─ Original epic goals validated
    │   ├─ All success criteria met (100%)
    │   ├─ UX flow validated
    │   └─ Performance benchmarks met
    │       └─ If ANY ISSUES → Create bug fix → RESTART Stage 6a
    ↓
STAGE_6c: Epic Final Review (60-90 min + bug fixes if needed)
    ├─ Step 6: Epic PR Review - 11 Categories (45-60 min)
    │   ├─ Architecture (MOST IMPORTANT - epic-wide patterns)
    │   ├─ Code Quality, Security, Error Handling, etc.
    │   └─ All 11 categories PASSED
    ├─ Step 7: Handle Issues (If Any) (Variable)
    │   ├─ Create bug fixes (Stage 2 → 5a → 5b → 5c)
    │   └─ RESTART Stage 6 from STAGE_6a (COMPLETE restart)
    └─ Step 8: Final Verification & README Update (15-30 min)
        ├─ Verify all steps complete
        ├─ Update EPIC_README.md (Stage 6 complete)
        └─ Update epic_lessons_learned.md
```

---

## Sub-Stage Summary Table

| Sub-Stage | Steps | Time | Key Activities | Mandatory Gates |
|-----------|-------|------|----------------|-----------------|
| STAGE_6a | 1-2 | 60-90 min | Pre-QC verification, Epic smoke testing (4 parts) | Part 4 data values |
| STAGE_6b | 3-5 | 2-3 hrs | 3 QC rounds (integration, consistency, success criteria) | All 3 rounds PASS |
| STAGE_6c | 6-8 | 1-2 hrs | Epic PR review (11 categories), bug fixes, final verification | All 11 categories PASS |

---

## Mandatory Restart Protocol 🔄

**CRITICAL:** If ANY issues found during Stage 6:

### Restart Steps:
1. **Create bug fix** using bug fix workflow (Stage 2 → 5a → 5b → 5c)
2. **RESTART Stage 6 from STAGE_6a** (cannot partially continue)
3. **Re-run ALL 8 steps:**
   - STAGE_6a: Epic Smoke Testing (all 4 parts)
   - STAGE_6b: QC Rounds 1, 2, 3
   - STAGE_6c: Epic PR Review (all 11 categories)
4. **Document restart** in epic_lessons_learned.md

### Why COMPLETE Restart?
- Bug fixes may have affected areas already checked
- Cannot assume previous QC results still valid
- Ensures epic-level quality maintained

**Cannot proceed to Stage 7 without passing Stage 6 restart.**

---

## Epic vs Feature Testing Differences

### Feature-Level Testing (Stage 5c)
**Focus:** Individual feature in ISOLATION
**Tests:**
- Smoke testing: Part 1-3 (Import, Entry Point, E2E)
- QC rounds: Feature-specific validation
- PR review: Single feature scope

**Scope:** One feature at a time

### Epic-Level Testing (Stage 6)
**Focus:** All features working TOGETHER as system
**Tests:**
- Smoke testing: Part 1-4 (adds Cross-Feature Integration)
- QC rounds: Cross-feature integration, epic cohesion, success criteria
- PR review: Epic-wide architectural consistency

**Scope:** Entire epic as cohesive whole

---

## Stage 6 Critical Rules

- ✅ ALWAYS use EVOLVED epic_smoke_test_plan.md (not original from Stage 1)
- ✅ Verify DATA VALUES, not just file existence
- ✅ Epic-level validation focuses on INTEGRATION (not individual features)
- ✅ ALL 3 QC rounds are MANDATORY (cannot skip)
- ✅ If ANY issues found → create bug fix → RESTART Stage 6 from STAGE_6a
- ✅ Epic PR review has 11 categories (all mandatory, Architecture MOST IMPORTANT)
- ✅ Validate against ORIGINAL epic request (re-read {epic_name}.txt)
- ✅ 100% test pass rate required throughout Stage 6
- ✅ Zero tolerance for epic-level quality issues

---

## Epic Smoke Testing Parts (Step 2)

### Part 1: Import Test
**What:** All epic features import successfully
**Commands:** Import each feature module
**Pass:** No import errors

### Part 2: Entry Point Test
**What:** Main entry points work
**Commands:** Run main scripts (run_league_helper.py, etc.)
**Pass:** Scripts execute without errors

### Part 3: E2E Execution Test
**What:** End-to-end workflows with DATA VALUE verification
**Commands:** Run epic_smoke_test_plan.md scenarios
**Pass:** Correct data values in outputs (not just file existence)

### Part 4: Cross-Feature Integration Test ← MANDATORY GATE
**What:** Features work TOGETHER
**Commands:** Integration scenarios from epic_smoke_test_plan.md
**Pass:** Data flows between features correctly

**If FAIL:** Fix issues, restart from Part 1

---

## QC Round Focus Areas (Steps 3-5)

### QC Round 1: Cross-Feature Integration (Step 3)
**Check:**
- Integration points tested (features communicate correctly)
- Data flow verification (data passed correctly between features)
- Interface compatibility (features use correct interfaces)
- Error propagation (errors handled across features)

**Pass Criteria:** All integration points working, no cross-feature errors

### QC Round 2: Epic Cohesion & Consistency (Step 4)
**Check:**
- Code style consistency (same style across all features)
- Naming conventions alignment (consistent naming)
- Error handling patterns (same error handling approach)
- Architectural patterns (consistent architecture)

**Pass Criteria:** Epic is cohesive, no inconsistencies

### QC Round 3: End-to-End Success Criteria (Step 5)
**Check:**
- Original epic goals validated (re-read epic request)
- ALL success criteria met (100% - defined in epic_smoke_test_plan.md)
- UX flow validated (user workflows work end-to-end)
- Performance benchmarks met (no regressions >100%)

**Pass Criteria:** 100% of success criteria met, user goals achieved

**If ANY ISSUES in any round:** Create bug fix → RESTART Stage 6a

---

## Epic PR Review Categories (Step 6)

### 11 Mandatory Categories:
1. **Architecture** ← MOST IMPORTANT (epic-wide patterns, consistency)
2. Code Quality (readability, maintainability)
3. Security (no vulnerabilities across epic)
4. Error Handling (consistent error patterns)
5. Performance (no regressions >100%)
6. Testing (integration test coverage)
7. Documentation (epic-wide docs)
8. Configuration (config consistency)
9. Dependencies (no conflicts)
10. Logging (consistent logging patterns)
11. User Experience (epic-wide UX flow)

**Pass Criteria:** ALL 11 categories PASSED
**If FAIL:** Create bug fix → RESTART Stage 6a

---

## Common Pitfalls

### ❌ Pitfall 1: Using Original Test Plan (Stage 1)
**Problem:** "I'll use the epic_smoke_test_plan.md from Stage 1"
**Impact:** Test plan is outdated (assumptions, not reality)
**Solution:** Use EVOLVED test plan (updated in Stage 4 and Stage 5e)

### ❌ Pitfall 2: Only Checking File Existence
**Problem:** "File exists, so test passed"
**Impact:** File has incorrect data, bugs escape to Stage 7
**Solution:** Verify DATA VALUES (not just file existence)

### ❌ Pitfall 3: Skipping QC Rounds
**Problem:** "Smoke testing passed, I'll skip QC rounds"
**Impact:** Quality issues slip through, fail in user testing
**Solution:** ALL 3 QC rounds are MANDATORY

### ❌ Pitfall 4: Inline Bug Fixes
**Problem:** "Small bug, I'll fix it inline without bug fix workflow"
**Impact:** No documentation, fix not properly tested, may break other areas
**Solution:** Create bug fix using bug fix workflow, RESTART Stage 6a

### ❌ Pitfall 5: Partial Restart After Bug Fix
**Problem:** "I'll just re-run the QC round that failed"
**Impact:** Bug fix may have affected other areas, incomplete validation
**Solution:** COMPLETE restart from STAGE_6a (all 8 steps)

### ❌ Pitfall 6: Feature-Level Focus
**Problem:** Testing features individually instead of together
**Impact:** Integration bugs slip through
**Solution:** Focus on cross-feature workflows and integration points

### ❌ Pitfall 7: Ignoring Original Epic Request
**Problem:** "I'll validate against final specs, not original request"
**Impact:** Scope creep validated, original goals missed
**Solution:** Re-read {epic_name}.txt, validate against user's original intent

---

## Quick Checklist: "Am I Ready for Next Step?"

**Before STAGE_6a:**
- [ ] ALL features completed Stage 5e
- [ ] No pending bug fixes
- [ ] All unit tests passing (100%)
- [ ] EVOLVED epic_smoke_test_plan.md exists

**STAGE_6a → STAGE_6b:**
- [ ] Pre-QC verification complete
- [ ] Epic smoke testing PASSED (all 4 parts)
- [ ] DATA VALUES verified (not just file existence)
- [ ] Cross-feature integration tested

**STAGE_6b → STAGE_6c:**
- [ ] QC Round 1 PASSED (Cross-Feature Integration)
- [ ] QC Round 2 PASSED (Epic Cohesion & Consistency)
- [ ] QC Round 3 PASSED (End-to-End Success Criteria, 100%)
- [ ] All QC findings resolved

**STAGE_6c → Stage 7:**
- [ ] Epic PR review PASSED (all 11 categories)
- [ ] Architecture validation complete
- [ ] No issues requiring bug fixes OR bug fixes complete and Stage 6 restarted
- [ ] Final verification complete
- [ ] EPIC_README.md updated (Stage 6 complete)
- [ ] epic_lessons_learned.md updated

---

## File Outputs

**STAGE_6a:**
- Epic smoke testing results (documented in epic_lessons_learned.md)

**STAGE_6b:**
- QC Round 1, 2, 3 findings (documented in epic_lessons_learned.md)

**STAGE_6c:**
- Epic PR review results (documented in epic_lessons_learned.md)
- Bug fixes (if issues found) - in bugfix_{priority}_{name}/ folders
- Updated EPIC_README.md (Stage 6 complete)
- Updated epic_lessons_learned.md (final insights)

---

## When to Use Which Guide

| Current Step | Guide to Read | Time Estimate |
|--------------|---------------|---------------|
| Starting Stage 6 | stages/stage_6/epic_smoke_testing.md | 60-90 min |
| Step 1-2 | stages/stage_6/epic_smoke_testing.md | 60-90 min |
| Step 3-5 | stages/stage_6/epic_qc_rounds.md | 2-3 hours |
| Step 6-8 | stages/stage_6/epic_final_review.md | 1-2 hours |
| Overview/navigation | stages/stage_6/epic_final_qc.md (router) | 5 min |

---

## Exit Conditions

**Stage 6 is complete when:**
- [ ] All 8 steps complete (1-8)
- [ ] Epic smoke testing PASSED (all 4 parts with data values)
- [ ] All 3 QC rounds PASSED (integration, consistency, success criteria)
- [ ] Epic PR review PASSED (all 11 categories)
- [ ] All bug fixes complete (if any) + Stage 6 restarted
- [ ] epic_lessons_learned.md updated
- [ ] EPIC_README.md shows Stage 6 complete
- [ ] All unit tests passing (100%)
- [ ] Original epic goals validated and achieved
- [ ] Ready to proceed to Stage 7 (Epic Cleanup)

**Next Stage:** Stage 7 (Epic Cleanup) - user testing, commit, archive

---

**Last Updated:** 2026-01-04
