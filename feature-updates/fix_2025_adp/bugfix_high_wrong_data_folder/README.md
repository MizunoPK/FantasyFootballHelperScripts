# Bug Fix: Wrong Data Folder

**Created:** 2025-12-31
**Priority:** HIGH
**Status:** Stage 5a - TODO Creation (Round 1)

---

## Bug Context

**Issue:** Epic targets wrong data folder entirely

**Current Implementation (WRONG):**
- Targets: `data/player_data/*.json` (6 files)

**Required Implementation (CORRECT):**
- Targets: `simulation/sim_data/2025/weeks/week_XX/*.json`
- All 18 weeks (week_01 through week_18)
- 6 position files per week
- Total: 108 files (18 weeks × 6 positions)

**Impact:** CRITICAL - Entire epic functionality targets wrong files

---

## Agent Status

**Last Updated:** 2026-01-01 00:45
**Current Phase:** STAGE_5B_IMPLEMENTATION
**Current Step:** Phase 1 - Core Function Update (Tasks 1-3)
**Current Guide:** STAGE_5b_implementation_execution_guide.md
**Guide Last Read:** 2026-01-01 00:35

**Implementation Progress:**
- ✅ Step 1: Interface Verification Protocol complete
- ✅ Step 2: Implementation Checklist created
- ➜ Step 3: Phase 1 starting (Tasks 1-3)

**Critical Rules from Guide:**
- ⚠️ Keep spec.md VISIBLE at all times during implementation
- ⚠️ Interface Verification Protocol FIRST (before writing ANY code)
- ⚠️ Dual verification for EVERY requirement (before & after)
- ⚠️ Run unit tests after EVERY phase (100% pass required)
- ⚠️ Mini-QC checkpoints after each major component
- ⚠️ Update implementation_checklist.md in REAL-TIME
- ⚠️ NO coding from memory - always consult spec
- ⚠️ Update code_changes.md INCREMENTALLY

**Stage 5a Completion Summary:**
- ✅ Round 1 (Iterations 1-7 + 4a): COMPLETE - HIGH confidence
- ✅ Round 2 (Iterations 8-16): COMPLETE - HIGH confidence
- ✅ Round 3 (Iterations 17-24 + 23a): COMPLETE - HIGH confidence
- ✅ Iteration 4a: TODO Specification Audit - PASSED
- ✅ Iteration 23a: Pre-Implementation Spec Audit - ALL 4 PARTS PASSED
- ✅ Iteration 24: Implementation Readiness Protocol - GO DECISION

**Quality Metrics:**
- Requirements coverage: 100% (17/17)
- TODO tasks: 17 (all with acceptance criteria)
- Test coverage: 95%
- Algorithm mappings: 12
- Integration verification: 4/4 methods (no orphans)
- Interface verification: 5/5 dependencies

**Progress:** Stage 2 ✅, Stage 5a ✅
**Next Action:** Read Stage 5b guide and begin implementation (Phase 1)
**Blockers:** None

---

## Files in This Bug Fix

**Created in Stage 1 (Bug Fix Creation):**
- README.md (this file)
- notes.txt (user-verified issue description)

**Created in Stage 2 (Deep Dive):**
- spec.md (complete technical requirements)
- checklist.md (all 6 decision questions resolved)

**Will be created in Stage 5a (TODO Creation):**
- todo.md (implementation tracking)
- questions.md (if needed)

**Will be created in Stage 5b (Implementation):**
- implementation_checklist.md (continuous spec verification)
- code_changes.md (documentation of changes)

---

## Bug Fix Completion Checklist

**Stage 2 - Deep Dive:** ✅ COMPLETE (2026-01-01)
- [x] spec.md fleshed out with detailed requirements
- [x] checklist.md all items resolved (6/6 questions answered)
- [x] Research complete (5/5 research questions answered)

**Stage 5a - TODO Creation:**
- [ ] Round 1 complete (iterations 1-7 + 4a)
- [ ] Round 2 complete (iterations 8-16)
- [ ] Round 3 complete (iterations 17-24 + 23a)
- [ ] Algorithm Traceability Matrix created
- [ ] Implementation Readiness Protocol (GO/NO-GO decision)

**Stage 5b - Implementation:**
- [ ] Production code written
- [ ] Tests written
- [ ] All unit tests passing (100%)

**Stage 5c - Post-Implementation:**
- [ ] Smoke testing passed (3 parts)
- [ ] QC rounds passed (3 rounds)
- [ ] Final review passed

---

## Bug Fix Summary

**Root Cause:**
- Epic scope misunderstood during planning stages
- Feature 2 (utils/adp_updater.py) hardcoded to wrong path

**Required Changes:**
1. Update Feature 2 to target simulation/sim_data/2025/weeks/
2. Iterate through all 18 week folders
3. Handle direct JSON array structure (no wrapper dict)
4. Maintain atomic writes for all 108 files
5. Update all unit tests (18 tests)
6. Update epic E2E test
7. Update user test script

**Acceptance Criteria:**
- All 18 week folders processed
- All 108 files updated
- ADP values match FantasyPros CSV
- Direct JSON array structure preserved
- Atomic writes used for all files
- Unit tests pass (100%)
