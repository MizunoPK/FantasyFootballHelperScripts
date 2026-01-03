# Mandatory Gates Across Epic Workflow - Quick Reference

**Purpose:** Comprehensive list of ALL mandatory gates from Stage 1-7
**Use Case:** Quick lookup for gate requirements, criteria, and failure consequences
**Total Gates:** 13 across 7 stages

---

## Quick Summary Table

| Stage | Gate | Location | Pass Criteria | Restart if Fail? |
|-------|------|----------|---------------|------------------|
| 1 | None | - | User confirmation recommended | No |
| 2a | Phase 1.5 Audit | STAGE_2a | All 4 categories with evidence | Yes (Phase 1) |
| 2b | Phase 2.5 Alignment | STAGE_2b | Zero scope creep + zero missing | Yes (Phase 2) |
| 2c | Phase 6 User Approval | STAGE_2c | User explicitly approves | Yes (Phase 6) |
| 3 | User Sign-Off | STAGE_3 | User approves complete plan | Yes (Stage 3) |
| 4 | None | - | Update test plan | No |
| 5aa | Iteration 4a | Round 1 | All tasks have acceptance criteria | Yes (Iteration 4) |
| 5ac | Iteration 23a | Part 2 | ALL 4 PARTS pass with 100% | Yes (Iteration 23a) |
| 5ac | Iteration 25 | Part 2 | Spec matches validated docs | Yes (User decides) |
| 5ac | Iteration 24 | Part 2 | GO decision (confidence >= MEDIUM) | Yes (Fix + redo) |
| 5ca | Smoke Part 3 | Smoke Testing | Data values verified | Yes (Part 1) |
| 5cb | QC Round 3 | QC Rounds | ZERO issues found | Yes (Smoke Part 1) |
| 7 | Unit Tests | Cleanup | 100% test pass (exit code 0) | Yes (Fix tests) |
| 7 | User Testing | Cleanup | ZERO bugs found by user | Yes (Stage 6) |

---

## Stage 1: Epic Planning

### No Mandatory Gates

**User confirmation recommended for:**
- Epic ticket content
- Feature breakdown
- Folder structure

**If user disagrees:** Revise and re-confirm

---

## Stage 2: Feature Deep Dive (3 gates per feature)

### Gate 1: Phase 1.5 - Research Completeness Audit

**Location:** stages/stage_2/phase_0_research.md
**When:** After completing targeted research (Phase 1)

**What it checks:**
1. **Component Research:** Have you found the code components mentioned in epic?
2. **Pattern Research:** Have you studied similar features in codebase?
3. **Data Research:** Have you located data sources/structures?
4. **Epic Research:** Did you re-read epic notes during research?

**Pass Criteria:**
- ALL 4 categories answered "Yes"
- Evidence provided for each (file paths, line numbers, code snippets)
- Cannot proceed if ANY category = "No"

**Evidence Required:**
- File paths (e.g., `league_helper/util/PlayerManager.py`)
- Line numbers (e.g., `lines 180-215`)
- Code snippets showing what you found

**If FAIL:**
- Return to Phase 1 (Targeted Research)
- Research the gaps identified
- Re-run Phase 1.5 audit
- Must PASS before proceeding to Phase 2

**Why it matters:** Ensures research is thorough before writing spec (prevents spec based on assumptions)

---

### Gate 2: Phase 2.5 - Spec-to-Epic Alignment Check

**Location:** stages/stage_2/phase_1_specification.md
**When:** After updating spec.md and checklist.md (Phase 2)

**What it checks:**
1. **Scope Creep Detection:** Requirements in spec.md NOT in epic notes
2. **Missing Requirements:** Epic requests NOT in spec.md

**Pass Criteria:**
- Zero scope creep (no extra requirements beyond epic)
- Zero missing requirements (all epic requests in spec)
- Every requirement traces to: Epic / User Answer / Derived

**Evidence Required:**
- Cite source for EACH requirement
- Show alignment between epic notes and spec sections

**If FAIL:**
- Remove scope creep (delete extra requirements), OR
- Add missing requirements (include what epic requested)
- Re-run Phase 2.5 alignment check
- Must PASS before proceeding to Phase 3

**Why it matters:** Prevents implementing features user didn't request (scope creep) or missing what they did request

---

### Gate 3: Phase 6 - User Approval (Acceptance Criteria)

**Location:** stages/stage_2/phase_2_refinement.md
**When:** After creating acceptance criteria (Phase 6)

**What it checks:**
- User explicitly approves acceptance criteria

**Pass Criteria:**
- User says "yes" or "approved" or equivalent
- User confirmation documented in spec.md or chat

**If FAIL:**
- Revise acceptance criteria based on user feedback
- Get user approval
- Cannot proceed to next feature or Stage 3 without approval

**Why it matters:** Ensures you and user agree on what "done" means before implementation

---

## Stage 3: Cross-Feature Sanity Check (1 gate per epic)

### Gate 1: User Sign-Off on Complete Epic Plan

**Location:** stages/stage_3/cross_feature_sanity_check.md
**When:** After all features planned and conflicts resolved

**What it checks:**
- User approves complete epic plan (all features together)

**Pass Criteria:**
- User reviews epic plan
- User explicitly approves proceeding to implementation

**If FAIL:**
- Address user concerns
- Revise affected feature specs
- Re-run Stage 3 sanity check
- Cannot proceed to Stage 4 without sign-off

**Why it matters:** Last checkpoint before significant implementation work begins

---

## Stage 4: Epic Testing Strategy

### No Mandatory Gates

**Output:** Updated epic_smoke_test_plan.md

**User approval recommended** but not mandatory

---

## Stage 5a: TODO Creation (4 gates per feature)

### Gate 1: Iteration 4a - TODO Specification Audit

**Location:** stages/stage_5/round1_todo_creation.md (Round 1)
**When:** After creating initial TODO.md (Iteration 4)

**What it checks:**
1. All TODO tasks have acceptance criteria
2. All tasks have implementation location specified
3. All tasks have test coverage noted

**Pass Criteria:**
- Count TODO tasks: N
- Count tasks with acceptance criteria: M
- Coverage = M/N × 100%
- ✅ PASS if coverage = 100%

**Evidence Required:**
- Cite specific numbers (e.g., "25 tasks, 25 with criteria = 100%")
- Cannot just check box without numbers

**If FAIL:**
- Add missing acceptance criteria to tasks
- Re-run Iteration 4a
- Must PASS before proceeding to Iteration 5

**Why it matters:** Ensures every task has clear definition of "done" before deep verification begins

---

### Gate 2: Iteration 23a - Pre-Implementation Spec Audit (4 PARTS)

**Location:** stages/stage_5/round3_part2_final_gates.md (Round 3 Part 2)
**When:** After preparation iterations (Iterations 17-22)

**ALL 4 PARTS must PASS:**

**PART 1: Completeness Audit**
- Requirements in spec.md: N
- Requirements with TODO tasks: M
- Coverage: M/N × 100%
- ✅ PASS if coverage = 100%

**PART 2: Specificity Audit**
- Total TODO tasks: N
- Tasks with acceptance criteria: M1
- Tasks with implementation location: M2
- Tasks with test coverage: M3
- Specificity: min(M1, M2, M3) / N × 100%
- ✅ PASS if specificity = 100%

**PART 3: Interface Contracts Audit**
- Total external dependencies: N
- Dependencies verified from source code: M
- Verification: M/N × 100%
- ✅ PASS if verification = 100%
- **CRITICAL:** Must READ actual source code, not assume

**PART 4: Integration Evidence Audit**
- Total new methods: N
- Methods with identified callers: M
- Integration: M/N × 100%
- ✅ PASS if integration = 100%

**Evidence Required:**
- Cite specific numbers for ALL 4 parts
- Cannot proceed if ANY part < 100%

**If FAIL:**
- Fix the failing part(s)
- Re-run Iteration 23a (all 4 parts)
- Must PASS before proceeding to Iteration 25

**Why it matters:** Final verification that TODO.md is complete and correct before validating against user-approved documents

---

### Gate 3: Iteration 25 - Spec Validation Against Validated Documents (CRITICAL)

**Location:** stages/stage_5/round3_part2_final_gates.md (Round 3 Part 2)
**When:** After Iteration 23a passes

**What it checks:**
- Spec.md matches ALL three user-validated sources:
  1. Epic notes (user's original request)
  2. Epic ticket (user-validated outcomes from Stage 1)
  3. Spec summary (user-validated feature outcomes from Stage 2)

**Process (8 steps):**
1. **Close spec.md and TODO.md** (avoid confirmation bias)
2. **Re-read validated documents** from scratch
3. **Ask critical questions:**
   - Is this EXAMPLE or SPECIAL CASE?
   - What is LITERAL meaning vs my INTERPRETATION?
   - Did I make assumptions, or verify with code/data?
4. **Three-way comparison:**
   - Epic notes vs spec.md
   - Epic ticket vs spec.md
   - Spec summary vs spec.md
5. **Document ALL discrepancies**
6. **IF ANY DISCREPANCIES → STOP and report to user with 3 options:**
   - Option A: Fix spec, restart TODO iterations (recommended)
   - Option B: Fix spec and TODO, continue (faster but riskier)
   - Option C: Discuss discrepancies first
7. **Wait for user decision** (no autonomous decisions)
8. **IF ZERO DISCREPANCIES → Document validation:**
   - Spec alignment: 100% with ALL three validated sources ✅

**Pass Criteria:**
- Zero discrepancies with ALL three validated sources
- OR user decision on discrepancies

**If FAIL (discrepancies found):**
- User chooses Option A, B, or C
- Follow user's decision
- Cannot proceed to Iteration 24 until resolved

**Historical Context:**
- Feature 02 catastrophic bug: spec.md misinterpreted epic notes
- Spec stated "no code changes needed" when epic actually required week_N+1 folder logic
- Iteration 25 specifically designed to prevent this type of bug

**Why it matters:** Prevents implementing the wrong solution based on misinterpreted spec (most critical gate)

---

### Gate 4: Iteration 24 - Implementation Readiness Protocol (GO/NO-GO)

**Location:** stages/stage_5/round3_part2_final_gates.md (Round 3 Part 2)
**When:** After Iteration 25 passes

**What it checks (comprehensive checklist):**
- Spec Verification: Complete, validated
- TODO Verification: All requirements have tasks, specificity 100%
- Iteration Completion: All 25 iterations complete
- Mandatory Gates: Iterations 4a, 23a (ALL 4 PARTS), 25 all PASSED
- Confidence Assessment: >= MEDIUM
- Integration Verification: Algorithm traceability, integration gaps, interfaces, mocks
- Quality Gates: Test coverage >90%, performance acceptable

**Decision:**
- ✅ **GO** if ALL checklist items checked, confidence >= MEDIUM, all gates PASSED
- ❌ **NO-GO** if ANY item unchecked, confidence < MEDIUM, any gate FAILED, blockers exist

**If GO:**
- Proceed to Stage 5b (Implementation Execution)

**If NO-GO:**
- Address concerns/blockers
- Fix failing items
- Re-evaluate Iteration 24
- Cannot proceed to Stage 5b without GO decision

**Why it matters:** Final checkpoint before writing code (prevents implementing with incomplete/incorrect planning)

---

## Stage 5b: Implementation Execution

### No Mandatory Gates

**Requirements:**
- 100% unit test pass after every phase (not a formal gate, but required)
- Mini-QC checkpoints every 5-7 tasks

---

## Stage 5c: Post-Implementation (2 gates per feature)

### Gate 5: Stage 5ca Part 3 - E2E Smoke Test (Data Validation)

**Location:** stages/stage_5/smoke_testing.md
**When:** After Part 1 (Import) and Part 2 (Entry Point) tests pass

**What it checks:**
- E2E execution with REAL data
- Verify DATA VALUES (not just file existence)
- All integration points work together

**Pass Criteria:**
- Part 1: Import test passes
- Part 2: Entry point test passes
- Part 3: E2E test passes with correct data values

**Evidence Required:**
- Show actual data values from output
- Verify values are correct (not just that files exist)

**If FAIL:**
- Fix issues
- **Restart from Stage 5ca Part 1** (Import Test)
- Must re-run all 3 parts

**Why it matters:** Ensures feature actually works end-to-end with real data before QC rounds

---

### Gate 6: Stage 5cb QC Round 3 - ZERO Issues Required

**Location:** stages/stage_5/qc_rounds.md
**When:** After QC Rounds 1 and 2 pass

**What it checks:**
- ZERO issues found (critical, major, OR minor)
- Complete skeptical review of entire feature

**Pass Criteria:**
- QC Round 1: <3 critical issues, >80% requirements met, no unfixable architecture
- QC Round 2: All Round 1 issues resolved, zero new critical issues
- QC Round 3: ZERO issues (critical, major, or minor)

**If FAIL (ANY issues found in Round 3):**
- Fix ALL issues
- **Restart from Stage 5ca Part 1** (smoke testing)
- Re-run smoke testing → QC Round 1 → QC Round 2 → QC Round 3
- ZERO tolerance for issues

**QC Restart Protocol:**
- Any code change invalidates QC rounds
- Must re-verify entire feature works end-to-end
- Cannot defer issues to "later"

**Why it matters:** Ensures feature is production-ready with zero known issues before final review

---

## Stage 5d & 5e: Post-Feature Updates

### No Mandatory Gates

**Stage 5d:** Update remaining feature specs
**Stage 5e:** Update epic test plan

---

## Stage 6: Epic-Level Final QC

### No Mandatory Gates (but similar to Stage 5c protocol)

**Requirements:**
- Epic smoke testing passes
- QC Round 3 passes with zero issues
- If ANY issues → restart Stage 6

---

## Stage 7: Epic Cleanup (2 gates per epic)

### Gate 7.1: Unit Tests (100% Pass)

**Location:** stages/stage_7/epic_cleanup.md
**When:** Before user testing

**What it checks:**
- All unit tests pass
- Exit code = 0 from test runner

**Pass Criteria:**
- `python tests/run_all_tests.py` exits with code 0
- 100% test pass rate

**If FAIL:**
- Fix failing tests (including pre-existing failures from other epics)
- Re-run tests
- Only proceed to user testing when exit code = 0

**Why it matters:** Ensures no regressions in existing functionality

---

### Gate 7.2: User Testing (ZERO Bugs)

**Location:** stages/stage_7/epic_cleanup.md
**When:** After unit tests pass (final gate before commit)

**What it checks:**
- User tests the complete epic
- User finds zero bugs

**Pass Criteria:**
- User explicitly confirms zero bugs found
- User approves epic for commit

**If FAIL (user finds ANY bugs):**
- Create bug fix following stages/stage_5/bugfix_workflow.md
- Bug fix goes through: Stage 2 → 5a → 5b → 5c
- After bug fix complete: **Restart Stage 6** (Epic-Level Final QC)
- Re-run Stage 6 → Stage 7 → User testing
- Cannot commit without user approval

**Why it matters:** Final validation that epic meets user requirements before merging to main

---

## Summary Statistics

**Total Mandatory Gates:** 13
- Stage 1: 0
- Stage 2: 3 (per feature, so 3×N for N features)
- Stage 3: 1
- Stage 4: 0
- Stage 5a: 4 (per feature)
- Stage 5c: 2 (per feature)
- Stage 6: 0 (but restart protocol similar)
- Stage 7: 2

**Gates with Evidence Requirements:** 7
- Phase 1.5: File paths, line numbers
- Iteration 4a: Task count, criteria count
- Iteration 23a: 4 parts with specific numbers
- Iteration 25: Three-way comparison results
- Smoke Part 3: Data values
- QC Round 3: Zero issues count

**Gates with Restart Protocol:** 6
- Phase 1.5 → Phase 1
- Phase 2.5 → Phase 2
- Iteration 4a → Iteration 4
- Iteration 23a → Iteration 23a
- Smoke Part 3 → Smoke Part 1
- QC Round 3 → Smoke Part 1

**Gates Requiring User Input:** 3
- Phase 6: User approval
- Stage 3: User sign-off
- Iteration 25: User decision (if discrepancies)
- Gate 7.2: User testing approval

---

## When to Use This Reference

**During planning:**
- Check what gates are ahead
- Understand pass criteria before starting

**During execution:**
- Quick lookup for specific gate requirements
- Verify you have evidence before claiming "PASS"

**When stuck:**
- Understand why gate failed
- Know what to fix before re-running

**During resume:**
- After session compaction, check which gate you were on
- Review requirements for current gate

---

**Last Updated:** 2026-01-02
