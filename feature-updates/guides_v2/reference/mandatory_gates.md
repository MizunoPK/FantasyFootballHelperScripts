# Mandatory Gates Across Epic Workflow - Quick Reference

**Purpose:** Comprehensive list of ALL mandatory gates from S1-S10
**Use Case:** Quick lookup for gate requirements, criteria, and failure consequences
**Total Gates:** 16 across 10 stages (NEW: Gate 4.5 added for early test plan approval)

---

## 🔢 Understanding Gate Numbering

**The workflow uses two gate numbering systems:**

### Type 1: Stage-Level Gates (whole/decimal numbers)
- **Examples:** Gate 3, Gate 4.5, Gate 5
- **Naming:** Based on stage number or position between stages
- **Approver:** Usually requires user approval
- **Purpose:** Major workflow checkpoints
- **Relationship to workflow:** BETWEEN stages (not part of iteration count)

**Logic:**
- Gate 3 = S2 gate (named after target stage)
- Gate 4.5 = Between S4 and 5 (decimal indicates "between")
- Gate 5 = S5 gate

### Type 2: Iteration-Level Gates (iteration numbers)
- **Examples:** Gate 4a, Gate 7a, Gate 23a, Gate 24, Gate 25
- **Naming:** Uses actual iteration number from S5
- **Approver:** Agent self-validates using checklists
- **Purpose:** Verification checkpoints during planning
- **⚠️ CRITICAL:** These ARE iterations, not additional steps
  - Gate 4a = Iteration 4a (same thing, counted as 1 iteration)
  - Gate 23a = Iteration 23a (same thing, counted as 1 iteration)
  - Don't count gates separately from iterations

**Logic:**
- Gate 4a = Occurs at Iteration 4a in S5 Round 1
- Gate 23a = Occurs at Iteration 23a in S5 Round 3
- Gate 24 = Occurs at Iteration 24 in S5 Round 3

**Example:** Round 1 has 9 iterations total:
- Iterations: 1, 2, 3, 4, 5, 5a, 6, 7
- Gates: 4a (within Iteration 4 guide), 7a (within Iteration 7 guide)
- Count: 9 iterations (not 9 + 2 gates = 11)

### Quick Identification

**How to tell which type:**
- **User gates:** 3, 4.5, 5, Phase X.X gates → User approval required
- **Agent gates:** 4a, 7a, 23a, 24, 25 → Agent validates using checklist
- **Stage gates:** Named after stages (3, 4.5, 5)
- **Iteration gates:** Named after iterations (4a, 7a, 23a, 24, 25)

---

## Quick Summary Table

| Stage | Gate | Location | Pass Criteria | Restart if Fail? |
|-------|------|----------|---------------|------------------|
| 1 | None | - | User confirmation recommended | No |
| 2a | Gate 1: Research Audit | S2.P1 | All 4 categories with evidence | Yes (Redo research) |
| 2b | Gate 2: Spec Alignment | S2.P2 | Zero scope creep + zero missing | Yes (Revise spec) |
| **3** | **Gate 3: Checklist Approval (NEW)** | **S2.P2** | **User answers ALL questions (100%)** | **Yes (Revise/Re-present)** |
| 4 | Gate 4: User Approval | S2.P3 | User explicitly approves | Yes (Revise criteria) |
| 4.5 | User Sign-Off | S3 | User approves complete plan | Yes (S3) |
| **5** | **Gate 5: Epic Test Plan Approval (NEW)** | **After S4** | **User approves epic_smoke_test_plan.md** | **Yes (Revise test plan)** |
| 5aa | Iteration 4a | Round 1 | All tasks have acceptance criteria | Yes (Iteration 4) |
| 5ac | Iteration 23a | Part 2 | ALL 4 PARTS pass with 100% | Yes (Iteration 23a) |
| 5ac | Iteration 25 | Part 2 | Spec matches validated docs | Yes (User decides) |
| 5ac | Iteration 24 | Part 2 | GO decision (confidence >= MEDIUM) | Yes (Fix + redo) |
| 5a-5b | User Approval | After 5a | User approves implementation_plan.md | Yes (Revise plan) |
| S7.P1 | Smoke Part 3 | Smoke Testing | Data values verified | Yes (Part 1) |
| S7.P2 | QC Round 3 | QC Rounds | ZERO issues found | Yes (Smoke Part 1) |
| 7 | Unit Tests | Cleanup | 100% test pass (exit code 0) | Yes (Fix tests) |
| 7 | User Testing | Cleanup | ZERO bugs found by user | Yes (S9) |

---

## S1: Epic Planning

### No Mandatory Gates

**User confirmation recommended for:**
- Epic ticket content
- Feature breakdown
- Folder structure

**If user disagrees:** Revise and re-confirm

---

## S2: Feature Deep Dive (4 gates per feature - NEW: Checklist Approval added)

### Gate 1: Phase 1.5 - Research Completeness Audit

**Location:** stages/s2/s2_p1_research.md
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

**Location:** stages/s2/s2_p2_specification.md
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

### Gate 3: User Checklist Approval (🚨 NEW MANDATORY GATE)

**Location:** stages/s2/s2_p2_specification.md (S2.P2)
**When:** After Gate 2 (Spec-to-Epic Alignment Check) passes

**What it checks:**
- User reviews ALL questions in checklist.md
- User provides answers to ALL questions
- Zero autonomous agent resolution

**Pass Criteria:**
- Agent presents checklist.md with N questions to user
- User answers all N questions
- Agent updates spec.md based on user answers
- Agent marks items `[x]` only after user provides answer
- User explicitly confirms all questions answered
- Total questions = Total answered (100%)

**Evidence Required:**
- checklist.md shows {N} total questions
- checklist.md shows {N} user answered
- Pending = 0
- User Approval section completed with timestamp
- Gate 2 Status: ✅ PASSED documented in checklist.md

**If FAIL (user requests changes or clarification):**
- Provide clarification on questions
- Revise questions based on user feedback
- Re-present checklist for user approval
- Cannot proceed to S5 without user approval of ALL questions

**Why it matters:**
- Addresses guide-updates.txt #2: "Require ALL checklist items to be confirmed by the user"
- Prevents autonomous agent resolution of uncertainties
- Ensures user visibility into ALL questions before implementation planning
- Stops agents from "researching and deciding" without user input
- Creates clear approval gate early in workflow

**From Proposal:** This gate ensures agents create QUESTIONS (not decisions) and user confirms ALL answers before proceeding.

---

### Gate 4: User Approval (Acceptance Criteria)

**Location:** stages/s2/s2_p3_refinement.md (S2.P3)
**When:** After creating acceptance criteria

**What it checks:**
- User explicitly approves acceptance criteria

**Pass Criteria:**
- User says "yes" or "approved" or equivalent
- User confirmation documented in spec.md or chat

**If FAIL:**
- Revise acceptance criteria based on user feedback
- Get user approval
- Cannot proceed to next feature or S3 without approval

**Why it matters:** Ensures you and user agree on what "done" means before implementation

---

## S3: Cross-Feature Sanity Check (1 gate per epic)

### Gate 1: User Sign-Off on Complete Epic Plan

**Location:** stages/s3/s3_cross_feature_sanity_check.md
**When:** After all features planned and conflicts resolved

**What it checks:**
- User approves complete epic plan (all features together)

**Pass Criteria:**
- User reviews epic plan
- User explicitly approves proceeding to implementation

**If FAIL:**
- Address user concerns
- Revise affected feature specs
- Re-run S3 sanity check
- Cannot proceed to S4 without sign-off

**Why it matters:** Last checkpoint before significant implementation work begins

---

## S4: Epic Testing Strategy (1 gate per epic - NEW)

### Gate 4.5: Epic Test Plan Approval (🚨 NEW MANDATORY GATE)

**Location:** stages/s4/s4_epic_testing_strategy.md
**When:** After updating epic_smoke_test_plan.md (before S5 begins)

**What it checks:**
- User reviews updated epic_smoke_test_plan.md
- User approves epic testing strategy BEFORE implementation planning begins
- Agent knows testing requirements before creating implementation plans

**Pass Criteria:**
- Agent presents epic_smoke_test_plan.md with:
  - Measurable success criteria (5-10 criteria)
  - Specific test scenarios (4-8 scenarios)
  - Integration points between features
  - Data quality checks (verify VALUES not just structure)
  - Concrete commands and expected outputs
- User explicitly approves test plan
- User says "approved" or "looks good" or equivalent

**Evidence Required:**
- epic_smoke_test_plan.md shows N measurable success criteria
- epic_smoke_test_plan.md shows N test scenarios
- All integration points from S3 incorporated
- User Approval section completed with timestamp
- Gate 4.5 Status: ✅ PASSED documented in EPIC_README.md

**If FAIL (user requests changes):**
- Revise epic_smoke_test_plan.md based on user feedback
- Re-present test plan for user approval
- Cannot proceed to S5 without user approval

**Why it matters:**
- Addresses guide-updates.txt #10: "Have the testing plan be presented to the user and confirmed for each feature and the epic as a whole. Do this EARLY so that the agent knows how to test the work itself."
- Agent knows EXACTLY how to test work BEFORE creating implementation plans
- User can adjust test strategy early (S4 vs S5 Round 3)
- Prevents creating implementation plans without knowing testing requirements
- Separates test WHAT (S4) from implement HOW (S5)
- Earlier feedback loop (S4 approval vs S5 Round 3 approval)

**Benefits:**
- Agent creates better implementation plans knowing exact testing requirements
- User sees test strategy early (cheap to change)
- Prevents discovering test strategy misalignment late (expensive to fix)
- Test strategy guides implementation planning (not vice versa)
- Clear separation: test plan approval (Gate 4.5) vs implementation plan approval (Gate 5)

**From Enhancement:** This gate ensures agents know HOW to test work BEFORE planning implementation, creating earlier user visibility and control.

---

## S5: Implementation Planning (5 gates per feature)

### Gate 1: Iteration 4a - Implementation Plan Specification Audit

**Location:** stages/s5/s5_p1_planning_round1.md (Round 1)
**When:** After creating initial implementation_plan.md (Iteration 4)

**What it checks:**
1. All implementation tasks have acceptance criteria
2. All tasks have implementation location specified
3. All tasks have test coverage noted

**Pass Criteria:**
- Count implementation tasks: N
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

### Gate 2: Iteration 23a - Pre-Implementation Spec Audit (5 PARTS)

**Location:** stages/s5/5.1.3.2_round3_part2a.md (Round 3 Part 2a)
**When:** After preparation iterations (Iterations 17-22)

**ALL 5 PARTS must PASS:**

**PART 1: Completeness Audit**
- Requirements in spec.md: N
- Requirements with implementation tasks: M
- Coverage: M/N × 100%
- ✅ PASS if coverage = 100%

**PART 2: Specificity Audit**
- Total implementation tasks: N
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

**PART 5: Design Decision Scrutiny**
- Challenge all "for backward compatibility" or "fallback" design decisions
- ✅ PASS if all of:
  - Necessity proven (not premature optimization)
  - User-validated need or historical bug evidence
  - Clean separation between old/new paths
  - No mixing incompatible data formats

**Evidence Required:**
- Cite specific numbers for ALL 5 parts
- Cannot proceed if ANY part < 100%

**If FAIL:**
- Fix the failing part(s)
- Re-run Iteration 23a (all 5 parts)
- Must PASS before proceeding to Iteration 25

**Why it matters:** Final verification that implementation_plan.md is complete and correct before validating against user-approved documents

---

### Gate 3: Iteration 25 - Spec Validation Against Validated Documents (CRITICAL)

**Location:** stages/s5/5.1.3.3_round3_part2b.md (Round 3 Part 2b)
**When:** After Iteration 23a passes

**What it checks:**
- Spec.md matches ALL three user-validated sources:
  1. Epic notes (user's original request)
  2. Epic ticket (user-validated outcomes from S1)
  3. Spec summary (user-validated feature outcomes from S2)

**Process (8 steps):**
1. **Close spec.md and implementation_plan.md** (avoid confirmation bias)
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
   - Option A: Fix spec, restart implementation planning iterations (recommended)
   - Option B: Fix spec and implementation plan, continue (faster but riskier)
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

**Location:** stages/s5/5.1.3.3_round3_part2b.md (Round 3 Part 2b)
**When:** After Iteration 25 passes

**What it checks (comprehensive checklist):**
- Spec Verification: Complete, validated
- Implementation Plan Verification: All requirements have tasks, specificity 100%
- Iteration Completion: All 25 iterations complete
- Mandatory Gates: Iterations 4a, 23a (ALL 4 PARTS), 25 all PASSED
- Confidence Assessment: >= MEDIUM
- Integration Verification: Algorithm traceability, integration gaps, interfaces, mocks
- Quality Gates: Test coverage >90%, performance acceptable

**Decision:**
- ✅ **GO** if ALL checklist items checked, confidence >= MEDIUM, all gates PASSED
- ❌ **NO-GO** if ANY item unchecked, confidence < MEDIUM, any gate FAILED, blockers exist

**If GO:**
- Proceed to S6 (Implementation Execution)

**If NO-GO:**
- Address concerns/blockers
- Fix failing items
- Re-evaluate Iteration 24
- Cannot proceed to S6 without GO decision

**Why it matters:** Final checkpoint before writing code (prevents implementing with incomplete/incorrect planning)

---

### Gate 5: User Approval of Implementation Plan (MANDATORY CHECKPOINT)

**Location:** Between S5 and S6
**When:** After Iteration 24 returns GO decision

**What it checks:**
- User reviews implementation_plan.md (~400 lines)
- User approves implementation approach before coding begins

**Pass Criteria:**
- User reviews implementation_plan.md containing:
  - Implementation tasks with acceptance criteria
  - Component dependencies matrix
  - Algorithm traceability matrix
  - Test strategy (>90% coverage)
  - Edge cases and error handling
  - Implementation phasing (5-6 checkpoints)
  - Performance considerations
  - Mock audit results
- User explicitly approves proceeding to S6
- User says "approved" or "looks good" or equivalent

**If FAIL (user requests changes):**
- Revise implementation_plan.md based on user feedback
- Re-run affected iterations from S5 if needed
- Get user approval before proceeding
- Cannot proceed to S6 without user approval

**Why it matters:** Gives user visibility and control over implementation approach before code is written. User can request changes to phasing, test strategy, or approach without wasting implementation effort.

**Benefits:**
- User sees full implementation plan before coding
- User can adjust approach early (cheap to change)
- Prevents implementing wrong approach (expensive to fix later)
- Creates shared understanding of implementation strategy

---

## S6: Implementation Execution

### No Mandatory Gates

**Requirements:**
- 100% unit test pass after each step (not a formal gate, but required)
- Mini-QC checkpoints every 5-7 tasks

---

## S7: Post-Implementation (2 gates per feature)

### Gate 5: S7.P1 Part 3 - E2E Smoke Test (Data Validation)

**Location:** stages/s7/s7_p1_smoke_testing.md
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
- **Restart from S10.P1 Step 1** (Import Test)
- Must re-run all 3 parts

**Why it matters:** Ensures feature actually works end-to-end with real data before QC rounds

---

### Gate 6: S7.P2 QC Round 3 - ZERO Issues Required

**Location:** stages/s7/s7_p2_qc_rounds.md
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
- **Restart from S7.P1 Step 1** (smoke testing)
- Re-run smoke testing → QC Round 1 → QC Round 2 → QC Round 3
- ZERO tolerance for issues

**QC Restart Protocol:**
- Any code change invalidates QC rounds
- Must re-verify entire feature works end-to-end
- Cannot defer issues to "later"

**Why it matters:** Ensures feature is production-ready with zero known issues before final review

---

## S8.P1 & 5e: Post-Feature Updates

### No Mandatory Gates

**S8.P1:** Update remaining feature specs
**S8.P2:** Update epic test plan

---

## S9: Epic-Level Final QC

### No Mandatory Gates (but similar to S7 protocol)

**Requirements:**
- Epic smoke testing passes
- QC Round 3 passes with zero issues
- If ANY issues → restart S9

---

## S10: Epic Cleanup (2 gates per epic)

### Gate 7.1: Unit Tests (100% Pass)

**Location:** stages/s10/s10_epic_cleanup.md
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

**Location:** stages/s10/s10_epic_cleanup.md
**When:** After unit tests pass (final gate before commit)

**What it checks:**
- User tests the complete epic
- User finds zero bugs

**Pass Criteria:**
- User explicitly confirms zero bugs found
- User approves epic for commit

**If FAIL (user finds ANY bugs):**
- Create bug fix following stages/s5/s5_bugfix_workflow.md
- Bug fix goes through: S2 → 5a → 5b → 5c
- After bug fix complete: **Restart S9** (Epic-Level Final QC)
- Re-run S9 → S10 → User testing
- Cannot commit without user approval

**Why it matters:** Final validation that epic meets user requirements before merging to main

---

## Summary Statistics

**Total Mandatory Gates:** 16
- S1: 0
- S2: 3 (per feature, so 3×N for N features)
- S3: 1
- S4: 1 (Gate 4.5 - Epic Test Plan Approval - NEW)
- S5: 5 (per feature, including user approval)
- S7: 2 (per feature)
- S9: 0 (but restart protocol similar)
- S10: 2

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

**Gates Requiring User Input:** 6
- Gate 3: User approval (checklist questions)
- Gate 4: User approval (acceptance criteria)
- Gate 4.5 (S3): User sign-off (epic plan)
- Gate 5: User approval (epic test plan - NEW)
- Iteration 25: User decision (if discrepancies)
- Gate 6: User approval (implementation plan)
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

**Last Updated:** 2026-01-10
