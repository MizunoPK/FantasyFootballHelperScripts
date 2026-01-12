# Stage 5: Feature Implementation
## Phase 5.3: Post-Implementation

**File:** `phase_5.3_post_implementation.md`

**Part of:** Epic-Driven Development Workflow v2
**Prerequisites:** Phase 5.2 complete (implementation execution finished)
**Next Phase:** `stages/stage_5/phase_5.4_post_feature_alignment.md`

---

## 🚨 MANDATORY READING PROTOCOL

**CRITICAL:** You MUST read this guide AND the appropriate phase guide before starting Stage 5c work.

**Why this matters:**
- Stage 5c is the QUALITY GATE before features are considered complete
- Missing steps here means shipping incorrect or incomplete features
- Thoroughness prevents rework and tech debt

**Reading Checkpoint:**
Before proceeding, you must have:
- [ ] Read this ENTIRE router guide (use Read tool, not memory)
- [ ] Verified STAGE_5b complete (all implementation tasks done)
- [ ] Verified all unit tests passing (100% pass rate)
- [ ] Identified which phase to start (usually Phase 1: Smoke Testing)

**If resuming after session compaction:**
1. Check feature README.md "Agent Status" section for current step
2. Re-read this router guide from the beginning
3. Read the specific phase guide for where you left off
4. Continue from documented checkpoint

---

## Quick Start

### What is this sub-stage?

**STAGE_5c - Post-Implementation** is the comprehensive validation phase after implementation, consisting of 3 sequential phases that ensure feature quality, correctness, and production readiness.

**This is feature-level validation** (not epic-level). Each feature goes through Stage 5c independently:
- Phase 1 (Part 5.3.1): Smoke Testing - Verify feature actually runs
- Phase 2 (Part 5.3.2): QC Rounds - Deep quality validation (3 rounds)
- Phase 3 (Part 5.3.3): Final Review - PR review, lessons learned, completion

**All 3 phases are MANDATORY** - you cannot skip any phase.

### When do you use this guide?

**Use this guide when:**
- STAGE_5b is complete (implementation execution finished)
- All implementation tasks marked done in implementation_checklist.md
- All unit tests passing (python tests/run_all_tests.py → exit code 0)
- Ready to validate feature quality before moving to cross-feature alignment

**Do NOT use this guide if:**
- STAGE_5b not complete (implementation still in progress)
- Unit tests failing
- implementation_checklist.md has pending tasks
- code_changes.md not fully updated

### What are the key outputs?

**After completing all 3 phases:**

1. **Smoke Testing Results** (Phase 1)
   - Import test passed
   - Entry point test passed
   - E2E execution test passed with data values verified

2. **QC Round Results** (Phase 2)
   - Round 1: Basic validation passed
   - Round 2: Deep verification passed
   - Round 3: Final skeptical review passed (zero issues)

3. **PR Review Results** (Phase 3)
   - 11 categories reviewed
   - Zero critical issues found
   - Minor issues documented (if any)

4. **Lessons Learned** (Phase 3)
   - lessons_learned.md updated
   - Guides updated if gaps found (applied immediately)

5. **Production-Ready Feature**
   - 100% requirement completion
   - Zero tech debt
   - Ready for Stage 5d (Cross-Feature Alignment)

### Time estimate

**Total: 1.5-2.5 hours** (all 3 phases, assuming no major issues)
- Phase 1 (Smoke Testing): 15-30 minutes
- Phase 2 (QC Rounds): 30-60 minutes
- Phase 3 (Final Review): 30-45 minutes

**+2-4 hours per restart** (if issues found requiring QC restart)

### Exit Condition

Stage 5c is complete when **ALL** of the following are true:
- All 3 phases completed (Part 5.3.1 → Part 5.3.2 → Part 5.3.3)
- Smoke testing passed (all 3 parts)
- QC rounds passed (all 3 rounds with zero issues in Round 3)
- PR review passed (11 categories, zero critical issues)
- Lessons learned captured and guides updated
- Feature is production-ready (100% complete, zero tech debt)

**If ANY criterion not met:** Stage 5c is INCOMPLETE

---

## Quick Navigation

**Use this table to find the right guide:**

| Current Part | Guide to Read | Time Estimate |
|--------------|---------------|---------------|
| Starting Phase 5.3 | `stages/stage_5/part_5.3.1_smoke_testing.md` | 15-30 min |
| Part 5.3.1: Smoke Testing | `stages/stage_5/part_5.3.1_smoke_testing.md` | 15-30 min |
| Part 5.3.2: QC Rounds | `stages/stage_5/part_5.3.2_qc_rounds.md` | 30-60 min |
| Part 5.3.3: Final Review | `stages/stage_5/part_5.3.3_final_review.md` | 30-45 min |

**Total Time:** 1.5-2.5 hours (all 3 parts, assuming no issues)


## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│         STAGE 5c: POST-IMPLEMENTATION WORKFLOW              │
│                    (3 Sequential Phases)                     │
└──────────────────────────────────────────────────────────────┘

PHASE 1: Smoke Testing (Part 5.3.1)
    │
    ├─ Part 1: Import Test (all modules load)
    ├─ Part 2: Entry Point Test (script starts correctly)
    ├─ Part 3: E2E Execution Test (CRITICAL - verify DATA VALUES)
    │
    ├─ GATE: ALL 3 parts must pass
    │
    ↓ If PASS → Phase 2
    ↓ If FAIL → Fix issues, RE-RUN ALL 3 PARTS

PHASE 2: QC Rounds (Part 5.3.2)
    │
    ├─ Round 1: Basic Validation (<3 critical issues, 100% requirements)
    ├─ Round 2: Deep Verification (all Round 1 resolved, zero new critical)
    ├─ Round 3: Final Skeptical Review (ZERO issues - strict)
    │
    ├─ GATE: ALL 3 rounds must pass (Round 3 = zero issues)
    │
    ↓ If PASS → Phase 3
    ↓ If FAIL → Fix issues, RESTART from Phase 1 (smoke testing)

PHASE 3: Final Review (Part 5.3.3)
    │
    ├─ PR Review (11 categories, multi-round with fresh agents)
    ├─ Lessons Learned Capture (update guides immediately)
    ├─ Final Verification (100% completion confirmed)
    │
    ├─ GATE: PR review passed, lessons applied, 100% complete
    │
    ↓ If PASS → Stage 5c COMPLETE → Proceed to Stage 5d
    ↓ If FAIL (critical issues) → RESTART from Phase 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY PRINCIPLES:

1. SEQUENTIAL EXECUTION - Phases must run in order (1→2→3)
2. NO SKIPPING - All 3 phases mandatory, no exceptions
3. RESTART PROTOCOL - Issues found → Restart from Phase 1
4. ZERO TECH DEBT - 100% completion required, no partial work
5. DATA VALUES - Verify actual data correctness, not just structure
```

---

## 🛑 Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 3 PHASES ARE MANDATORY
   - Cannot skip any phase
   - Cannot reorder phases
   - Each phase has specific purpose and catches different issues

2. ⚠️ QC RESTART PROTOCOL
   - If ANY phase fails → Fix issues → RESTART from Phase 1
   - "Fix and continue" is NOT allowed
   - Full restart ensures comprehensive validation

3. ⚠️ VERIFY DATA VALUES (Not Just Structure)
   - Phase 1 Part 3: Check output data CORRECTNESS
   - Phase 2 Round 2: Validate data values match spec
   - Common failure: "File exists" ≠ "Data is correct"

4. ⚠️ ZERO TECH DEBT TOLERANCE
   - Feature is COMPLETE or INCOMPLETE (no partial credit)
   - "90% done" = INCOMPLETE = RESTART
   - All spec requirements must be 100% implemented

5. ⚠️ UPDATE GUIDES IMMEDIATELY (Phase 3)
   - Don't just document lessons learned
   - Apply guide improvements BEFORE completing Phase 3
   - This is NOT optional

6. ⚠️ FRESH AGENTS FOR PR REVIEW (Phase 3)
   - Use Task tool to spawn fresh agents
   - Prevents context bias
   - Follow pr_review_protocol.md exactly

7. ⚠️ RE-READING CHECKPOINTS
   - Phase 1: Re-read critical rules after Part 3
   - Phase 2: Re-read critical rules after each round
   - Phase 3: Re-read completion criteria before declaring done
```

---

## Phase Navigation

### 📖 Phase 1: Smoke Testing (Part 5.3.1)

**Guide:** `stages/stage_5/smoke_testing.md`

**Purpose:** Verify the feature actually runs and produces correct output

**Key Activities:**
- Part 1: Import Test (all modules load without errors)
- Part 2: Entry Point Test (script starts correctly)
- Part 3: E2E Execution Test (feature runs end-to-end, **DATA VALUES verified**)

**Pass Criteria:**
- ALL 3 parts pass
- Part 3 verifies OUTPUT DATA VALUES (not just "file exists")

**If FAIL:**
- Fix ALL issues
- RE-RUN ALL 3 PARTS (not just failed part)
- Do NOT proceed to Phase 2 until all parts pass

**Time:** 15-30 minutes

**Read guide:** `stages/stage_5/smoke_testing.md`

---

### 📖 Phase 2: QC Rounds (Part 5.3.2)

**Guide:** `stages/stage_5/qc_rounds.md`

**Purpose:** Comprehensive quality control through 3 progressively deeper validation rounds

**Key Activities:**
- Round 1: Basic Validation (unit tests, code structure, output files, interfaces, docs)
- Round 2: Deep Verification (baseline comparison, data validation, regression, edge cases, semantic diff)
- Round 3: Final Skeptical Review (fresh-eyes spec review, algorithm traceability, integration gap check, zero issues scan)

**Pass Criteria:**
- Round 1: <3 critical issues, 100% requirements met
- Round 2: ALL Round 1 issues resolved + zero new critical issues
- Round 3: **ZERO issues found** (critical, medium, OR minor)

**If FAIL:**
- Fix ALL issues identified
- **RESTART from Phase 1** (smoke testing)
- Re-run smoke testing → Round 1 → Round 2 → Round 3

**Time:** 30-60 minutes (all 3 rounds)

**Read guide:** `stages/stage_5/qc_rounds.md`

---

### 📖 Phase 3: Final Review (Part 5.3.3)

**Guide:** `stages/stage_5/final_review.md`

**Purpose:** Production readiness validation through PR review, lessons learned, and final verification

**Key Activities:**
- PR Review (11 categories, multi-round with fresh agents via Task tool)
- Lessons Learned Capture (update guides immediately, not just document)
- Final Verification (confirm 100% completion and production readiness)

**Pass Criteria:**
- PR review passed (11 categories, zero critical issues)
- Lessons learned captured AND guides updated
- Final verification passed (all boxes checked)
- Feature is ACTUALLY complete (100% requirements, zero tech debt)

**If FAIL (critical issues found in PR review):**
- Fix ALL critical issues
- **RESTART from Phase 1** (smoke testing)
- Re-run entire validation sequence

**Time:** 30-45 minutes

**Read guide:** `stages/stage_5/final_review.md`

---

## Completion Criteria

**Stage 5c is complete when ALL of the following are true:**

### Phase 1 (Smoke Testing)
- [ ] Part 1 (Import Test): PASSED
- [ ] Part 2 (Entry Point Test): PASSED
- [ ] Part 3 (E2E Execution Test): PASSED with data values verified

### Phase 2 (QC Rounds)
- [ ] Round 1 (Basic Validation): PASSED
- [ ] Round 2 (Deep Verification): PASSED
- [ ] Round 3 (Final Skeptical Review): PASSED (zero issues)

### Phase 3 (Final Review)
- [ ] PR review complete (11 categories reviewed)
- [ ] Zero critical issues found
- [ ] Lessons learned captured and guides updated
- [ ] Final verification passed (all boxes checked)

### Overall Feature Status
- [ ] 100% requirement completion (no partial work)
- [ ] Zero tech debt (no deferred issues)
- [ ] Production-ready (would ship with confidence)
- [ ] All unit tests passing (python tests/run_all_tests.py → exit code 0)
- [ ] Git clean (all changes committed)

**If ALL boxes checked:** Ready to proceed to Stage 5d (Cross-Feature Alignment)

**If ANY box unchecked:** Stage 5c is INCOMPLETE - complete missing items first

---

## Prerequisites for Next Stage

**Before transitioning to Stage 5d (Cross-Feature Alignment), verify:**

### Completion Verification
- [ ] All 3 phases complete (Part 5.3.1 → Part 5.3.2 → Part 5.3.3)
- [ ] All completion criteria met (see section above)
- [ ] Feature is production-ready

### Files Updated
- [ ] lessons_learned.md updated (Phase 3)
- [ ] code_changes.md complete (from Phase 5b)
- [ ] implementation_checklist.md all verified (from Phase 5b)
- [ ] Guides updated if gaps found (Phase 3)

### Unit Tests
- [ ] Run `python tests/run_all_tests.py` → exit code 0
- [ ] 100% pass rate maintained

### Git Status
- [ ] All implementation changes committed
- [ ] Working directory clean (`git status`)
- [ ] Descriptive commit messages

### README Agent Status
- [ ] Updated to reflect Stage 5c completion
- [ ] Next action set to "Read stages/stage_5/post_feature_alignment.md"

**If ALL verified:** Ready for Stage 5d

**Stage 5d Preview:**
- Review all REMAINING (not-yet-implemented) feature specs
- Compare to ACTUAL implementation of just-completed feature
- Update specs based on implementation insights
- Ensure remaining features align with reality

**Next step:** Read `stages/stage_5/post_feature_alignment.md` and use phase transition prompt

---

## Summary

**Stage 5c validates feature quality through 3 sequential phases:**

1. **Smoke Testing (Part 5.3.1)** - Feature actually runs with correct data
2. **QC Rounds (Part 5.3.2)** - Deep quality validation (3 rounds)
3. **Final Review (Part 5.3.3)** - PR review, lessons learned, completion verification

**Critical protocols:**
- All 3 phases mandatory (no skipping)
- Sequential execution (1→2→3)
- Restart from Phase 1 if ANY phase fails
- Zero tech debt tolerance (100% or INCOMPLETE)
- Verify DATA VALUES (not just structure)
- Update guides immediately when gaps found

**Success criteria:**
- All smoke tests passed
- All QC rounds passed (Round 3 = zero issues)
- PR review passed (11 categories, zero critical)
- Lessons learned captured and applied
- Feature is production-ready (100% complete)

**After Stage 5c:** Proceed to Stage 5d (Cross-Feature Alignment) to ensure remaining feature specs align with actual implementation.

---

**END OF STAGE 5c ROUTER GUIDE**
