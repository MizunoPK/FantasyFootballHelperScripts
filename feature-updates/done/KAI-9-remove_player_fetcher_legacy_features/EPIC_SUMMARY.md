## Epic Summary: KAI-9 - remove_player_fetcher_legacy_features

**Created:** 2026-02-13
**Status:** S3 Complete - Ready for User Approval (Gate 4.5)

---

## Epic Overview

**Goal:** Remove all legacy export formats (CSV, JSON, Excel), locked player preservation, and file caps management from the player data fetcher, streamlining to position-based JSON output only.

**Epic Size:** SMALL-MEDIUM (1 feature)
**Complexity:** MEDIUM (removal work with interconnected areas)
**Risk:** MEDIUM (import fixes required, zero regression tolerance)

---

## Features Summary

### Feature 01: Remove Legacy Player Fetcher Features
**Status:** S2 Complete (spec approved, 13 requirements + 13 acceptance criteria)

**Summary:** Remove all legacy export formats, locked player preservation, and file caps management using atomic removal strategy (all deletions together to avoid broken intermediate states). Uses import-driven cleanup approach with zero regression requirement for position JSON and team exports.

**What Gets Removed:**
- 9 config values + 1 dataclass import (22 lines)
- 6 export methods + 2 helpers (~228 lines)
- Locked preservation logic (~100-120 lines)
- 4 Settings class fields
- 5 test classes

**What Gets Fixed:**
- 9 broken imports (5 in exporter, 4 in main)
- 2 DataFileManager calls (pass None instead of DEFAULT_FILE_CAPS)
- 1 integration point (NFLProjectionsCollector.export_data)

**What Stays Untouched:**
- Position JSON export (6 files: QB, RB, WR, TE, K, DST) - ZERO REGRESSIONS
- Team data export (32 CSV files) - PRESERVED
- Drafted data loading - OUT OF SCOPE
- ESPN API calls - OUT OF SCOPE

**Total Impact:** ~350-370 lines of dead code removed, codebase simplified, 100% test pass rate maintained

---

## Epic-Level Architecture

**Key Architectural Decisions:**

1. **Atomic Removal:** All deletions in one feature (prevents broken intermediate states)
2. **Import-Driven Cleanup:** Delete config → Fix imports → Remove dependent code (clear validation)
3. **Zero Regression Tolerance:** Position JSON + team exports must work identically (3-layer validation: unit tests + manual + smoke testing)
4. **DataFileManager Pattern:** Pass None instead of DEFAULT_FILE_CAPS (leverages existing fallback)
5. **Test Cleanup:** Delete 5 test classes for removed features, keep 6 for remaining functionality

**Integration Points:**
- NFLProjectionsCollector.export_data() → Replace export_all_formats_with_teams() with direct calls to export_position_json_files() + export_teams_to_data()

---

## Epic Testing Strategy

**Epic Smoke Testing Plan** (S9.P1 execution):

**9 Success Criteria:**
1. Zero import errors (command exits cleanly)
2. Config cleanup complete (grep returns 0 for all 9 values)
3. Export methods removed (grep returns 0 for all 8 methods)
4. Locked preservation removed (grep returns 0)
5. Settings class cleanup (grep returns 0 for 4 fields)
6. Position JSON files generate (6 files created)
7. Position JSON data integrity (correct players, zero regressions)
8. Team export preserved (32 CSV files created)
9. Unit test pass rate 100% (6 classes pass, 0 failures)

**8 Specific Test Scenarios:**
1. Import Validation (--help command)
2. Config Cleanup Verification (grep all deleted values)
3. Method Removal Verification (grep all deleted methods)
4. Position JSON Generation End-to-End (run player fetcher, verify 6 files)
5. Team Export Verification (verify 32 CSV files)
6. Unit Test Cleanup and Pass Rate (pytest with 100% pass)
7. Integration Point Validation (verify NFLProjectionsCollector updated)
8. DataFileManager None Parameter (verify both locations pass None)

**Verification Approach:** All test scenarios have executable commands with clear pass/fail criteria

---

## Timeline Estimate

**Total Epic Estimate:** ~6-8 hours (1 feature × 6-8 hours per feature)

**Breakdown:**
- S1 (Epic Planning): COMPLETE (~2-3 hours: Discovery, Epic Ticket, Structure)
- S2 (Feature Deep Dive): COMPLETE (~2 hours: Research, Spec, Validation)
- S3 (Epic Documentation & Testing): IN PROGRESS (~1 hour: Testing strategy, Documentation, Approval)
- S4 (Feature Testing Strategy): ~1 hour (plan tests before implementation)
- S5 (Implementation Planning): ~2-3 hours (Validation Loop, user approval)
- S6 (Execution): ~2-3 hours (delete code, fix imports, update integration)
- S7 (Testing & QC): ~1-2 hours (smoke test, 3 QC rounds, commit)
- S8 (Alignment): N/A (single feature)
- S9 (Epic Final QC): ~1-2 hours (epic smoke test, 3 QC rounds, user testing)
- S10 (Cleanup): ~30 min (unit tests, guide updates if needed)

**Estimated Completion:** 2-4 hours remaining (S4-S10)

---

## Success Metrics

**Epic succeeds when ALL criteria met:**

✅ Config file contains NO legacy values (9 values + import deleted)
✅ Import health: Zero ImportError crashes (9 imports fixed)
✅ Export methods: All 6 methods + 2 helpers deleted (~228 lines)
✅ Locked preservation: All logic removed (~120 lines)
✅ Settings class: 4 fields removed, docstring updated
✅ DataFileManager: Both locations pass None (not DEFAULT_FILE_CAPS)
✅ Integration point: NFLProjectionsCollector calls position JSON + team exports directly
✅ Test cleanup: 5 test classes deleted, 6 remaining classes pass 100%
✅ Position JSON: 6 files generate with correct data (QB, RB, WR, TE, K, DST) - ZERO REGRESSIONS
✅ Team export: 32 CSV files generate with correct data - PRESERVED
✅ Unit tests: 100% pass rate maintained
✅ Code quality: No orphaned code, no broken imports
✅ Scope boundaries: Only deletions performed, no new features added

---

## Risk Mitigation

**Risks Identified & Mitigations:**

1. **Risk:** Import errors after config deletion
   - **Mitigation:** Import-driven cleanup strategy (fix imports immediately after config deletion)
   - **Validation:** Test Scenario 1 (--help command must exit cleanly)

2. **Risk:** Position JSON regression (data loss or corruption)
   - **Mitigation:** Zero regression tolerance policy, 3-layer validation
   - **Validation:** Test Scenario 4 (compare to baseline), Test Scenario 7 (integration point), Test Scenario 6 (unit tests)

3. **Risk:** Team export accidentally removed
   - **Mitigation:** Explicit preservation in architecture decisions, integration point adds call
   - **Validation:** Test Scenario 5 (32 CSV files verification)

4. **Risk:** Test suite breaks after test class deletions
   - **Mitigation:** Delete only test classes for removed methods, keep tests for remaining functionality
   - **Validation:** Test Scenario 6 (100% pass rate for 6 remaining classes)

5. **Risk:** DataFileManager breaks with None parameter
   - **Mitigation:** Verified in Discovery that DataFileManager accepts None (Q1 answer)
   - **Validation:** Test Scenario 8 (both locations work with None)

---

## Files Created

**Epic-Level:**
- EPIC_README.md (epic overview + feature tracking)
- EPIC_TICKET.md (acceptance criteria, user validated)
- DISCOVERY.md (research findings, 5 rounds, user approved)
- epic_smoke_test_plan.md (9 criteria + 8 test scenarios)
- epic_lessons_learned.md (template for S10)
- GUIDE_ANCHOR.md (for session resumption)
- EPIC_SUMMARY.md (this file - for user review)
- research/ folder (with S2_P2_CROSS_FEATURE_ALIGNMENT.md)

**Feature 01:**
- spec.md (13 requirements + 13 acceptance criteria, user approved)
- checklist.md (no open questions, user approved)
- README.md (Agent Status tracker)
- RESEARCH_NOTES.md (9 sections, comprehensive code verification)
- lessons_learned.md (template for S7.P3)

---

## Next Steps After Approval

**If approved (Gate 4.5 passed):**
1. Proceed to S4: Feature Testing Strategy
   - Plan unit tests, integration tests, edge cases
   - Create test_strategy.md for Feature 01
   - Validate with 4-iteration Validation Loop
   - Estimate: ~1 hour

2. Continue through S5-S10:
   - S5: Implementation planning (Validation Loop)
   - S6: Code execution (deletions, import fixes, integration updates)
   - S7: Feature testing & QC (smoke test, 3 QC rounds)
   - S8: N/A (single feature)
   - S9: Epic QC (epic smoke test, 3 QC rounds, user testing)
   - S10: Cleanup (100% unit tests, guide updates if needed)

**If changes requested:**
- Loop back to appropriate phase (S3.P1 for testing, S3.P2 for documentation)
- Re-run Validation Loop
- Re-present for approval

**If rejected (fundamental issue):**
- 3-tier rejection handling:
  - (A) Re-do Discovery Phase (S1.P3)
  - (B) Revise feature breakdown (S1.P4)
  - (C) Exit epic planning

---

## Approval Request

**This epic summary, along with:**
- epic_smoke_test_plan.md (8 test scenarios, 9 success criteria)
- EPIC_README.md (1 feature summary, 5 architecture decisions)
- Feature 01 spec.md (13 requirements, 13 acceptance criteria)

**...is ready for your review and approval (Gate 4.5).**
