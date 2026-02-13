## Feature 01: Remove Legacy Player Fetcher Features

**Epic:** KAI-9 - remove_player_fetcher_legacy_features
**Created:** 2026-02-13
**Status:** NOT STARTED

---

## Agent Status

**Last Updated:** 2026-02-13 (S7.P3 STARTING - PR VALIDATION LOOP)
**Current Stage:** S7 - Feature Testing & QC
**Current Phase:** S7.P3 - Final Review (PR Validation Loop)
**Current Step:** Beginning PR Validation Loop Round 1
**Current Guide:** `reference/validation_loop_qc_pr.md`
**Guide Last Read:** 2026-02-13

**Critical Rules from S7.P3 Guide:**
- All 11 PR categories checked every round
- 3 consecutive clean rounds required
- Update guides immediately (not just document)
- 100% completion required

**Critical Rules from S6 Guide:**
- Keep spec.md VISIBLE at all times during implementation
- Interface Verification Protocol FIRST (before ANY code) ✅ COMPLETE
- Dual verification for EVERY requirement (before AND after)
- Run unit tests after each step (100% pass required)
- Mini-QC checkpoints after each major component
- Update implementation_checklist.md in REAL-TIME
- NO coding from memory - always consult actual spec text
- If ANY test fails → STOP, fix, re-run before proceeding

**Interface Verification Results:**
- ✅ DataFileManager.__init__() - Accepts None, has fallback logic
- ✅ DataExporter.export_position_json_files() - Creates 6 position JSON files
- ✅ DataExporter.export_teams_to_data() - Creates team CSV files
- ✅ NFLProjectionsCollector.export_data() - Integration point identified
- ✅ All 4/4 assumptions validated (100% match reality)

**S5 Complete Summary:**
- implementation_plan.md created and validated ✅
- 6 validation rounds (3 fixing + 3 clean rounds)
- 15 issues found and fixed (100% resolution)
- 17 feature tasks + 13 test tasks = 30 total
- Quality: 99%+ (validated by 3 consecutive clean rounds)
- Gate 5: User approval obtained ✅

**Progress:** S2 complete, S3 complete (Gate 4.5 passed), S4 COMPLETE (4/4 iterations), S5 COMPLETE (Gate 5 passed), S6 Steps 1-2 COMPLETE
**Next Action:** Begin S6 Step 3 - Phase-by-Phase Implementation starting with Phase 1 (Config cleanup - Tasks 1-3)
**Blockers:** None

**S4 Summary:**
- **S4.I1:** Test coverage matrix created (39 tests: 27 unit, 12 integration)
- **S4.I2:** Edge case catalog created (10 edge cases added, 49 total tests)
- **S4.I3:** Config test matrix created (5 config tests added, 54 total tests)
- **S4.I4:** Validation Loop PASSED (3 consecutive clean rounds, 0 issues found)

**S4 Final Results:**
- test_strategy.md created and validated ✅
- Total tests planned: 54 (27 unit, 12 integration, 10 edge case, 5 config)
- Coverage: 100% requirement coverage (15/15 items: 13 requirements + 2 acceptance criteria)
- Exceeds 90% goal ✅
- All 10 dimensions validated (7 master + 3 test strategy-specific)
- Ready for S5 (Implementation Planning)

**Previous Stages Summary:**
- **S2:** spec.md (13 requirements + 13 acceptance criteria, user-approved), Gates 1, 2, 3 PASSED ✅
- **S3:** Epic test plan approved (Gate 4.5 PASSED ✅), epic_smoke_test_plan.md (9 criteria, 8 scenarios)
- **S4:** Starting now - will create test_strategy.md with >90% coverage goal

**Notes:**
- Single atomic feature containing all legacy removal work
- Discovery Phase complete, findings documented in epic DISCOVERY.md
- 9 config values + 1 import to delete
- 9 export methods + 2 helpers to remove (~700-950 lines)
- Locked player preservation logic to remove (~100-150 lines)
- 9 broken imports to fix (5 in exporter, 4 in main)
- 4 Settings class fields to remove
- 5 test classes to delete
- Position JSON export must remain functional (zero regressions)

---

## Feature Overview

**Feature Goal:**
Remove all legacy export formats (CSV, JSON, Excel), locked player preservation logic, file caps management, and configurable export columns from the player data fetcher. Streamline the codebase to support only position-based JSON output (QB, RB, WR, TE, K, DST files), eliminating ~700-950 lines of dead code.

**Feature Scope:**
Delete 9 config values + dataclass import, remove 9 export methods + 2 helpers, remove locked preservation (method + dict + logic), fix 9 broken imports, clean Settings class (4 fields + docstring), update DataFileManager calls (2 locations), update integration point (NFLProjectionsCollector.export_data), delete 5 test classes, maintain position JSON and team export functionality.

**Key Outcomes:**
1. Config cleanup - 9 values + 1 import removed from config.py
2. Import health - 0 broken imports (9 imports fixed across 2 files)
3. Simplified exporter - 9 methods + 2 helpers deleted (~700-950 lines)
4. Streamlined Settings - 4 fields removed, docstring updated
5. Updated tests - 5 test classes deleted, remaining tests pass
6. Zero regressions - Position JSON works perfectly (6 files with correct data)

---

## Feature Files

**Created in S1:**
- `README.md` (this file) ✅
- `spec.md` - To be created in S2
- `checklist.md` - To be created in S2
- `lessons_learned.md` ✅

**Created in S4:**
- `test_strategy.md` - To be created in S4

**Created in S5:**
- `implementation_plan.md` - To be created in S5

**Created in S6:**
- `implementation_checklist.md` - To be created in S6

**Created in S7 (if needed):**
- `debugging/` folder - Only if issues found during testing

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Feature folder created
- [x] README.md created (this file)
- [x] checklist.md template created
- [x] lessons_learned.md template created
- [ ] spec.md created in S2

**S2 - Feature Deep Dive:**
- [ ] spec.md created with Discovery Context
- [ ] checklist.md populated with questions
- [ ] User answers all checklist questions
- [ ] All checklist items marked RESOLVED
- [ ] Gate 3: User approval of checklist

**S3 - Cross-Feature Sanity Check:**
- [ ] N/A (single feature epic, no conflicts possible)

**S4 - Feature Testing Strategy:**
- [ ] test_strategy.md created (4 iterations + Validation Loop)
- [ ] Testing approach defined
- [ ] User approval obtained

**S5 - Feature Implementation Planning:**
- [ ] implementation_plan.md created (Draft + Validation Loop)
- [ ] Gate 5: User approval of implementation plan

**S6 - Feature Execution:**
- [ ] implementation_checklist.md created
- [ ] All code changes implemented
- [ ] All unit tests passing

**S7 - Feature Testing & QC:**
- [ ] Smoke testing passed (S7.P1)
- [ ] QC Round 1 passed (S7.P2)
- [ ] QC Round 2 passed (S7.P2)
- [ ] QC Round 3 passed (S7.P2)
- [ ] Final review passed (S7.P3)
- [ ] Feature committed to git

**S8 - Cross-Feature Alignment:**
- [ ] N/A (single feature epic, no alignment needed)

---

## Discovery Context Reference

**Key findings from epic DISCOVERY.md (approved by user):**

1. **Config State:** Values NOT yet deleted - deletion IS part of this epic
2. **Import Dependencies:** 9 broken imports after config deletion (5 in exporter, 4 in main)
3. **Export Methods:** 9 methods + 2 helpers to delete (~700-950 lines total)
4. **Locked Preservation:** ~100-150 lines to remove (method, dict, logic checks)
5. **DataFileManager:** Accepts None parameter (no refactoring needed)
6. **Settings Class:** 4 fields to remove (lines 95-98) + docstring update
7. **Integration Point:** NFLProjectionsCollector.export_data() lines 349-354

**See:** `../DISCOVERY.md` for complete research findings and validation loop results.

---

## Feature Completion Summary

{This section will be filled out in S7.P3 - Final Review}
