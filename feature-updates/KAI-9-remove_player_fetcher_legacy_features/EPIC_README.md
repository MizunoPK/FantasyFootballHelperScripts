## Epic: remove_player_fetcher_legacy_features

**Created:** 2026-02-13
**Status:** IN PROGRESS
**Total Features:** 1 (atomic removal approach - all deletions in one feature)

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 1 - Epic Planning
**Active Guide:** `guides_v2/stages/s1/s1_epic_planning.md`
**Last Guide Read:** 2026-02-13 (current time)

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
 ↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** ➜ Stage 1 (Epic Planning)

**Critical Rules for Current Stage:**
1. CREATE GIT BRANCH BEFORE ANY CHANGES (Step 1.0) - COMPLETE
2. DISCOVERY PHASE IS MANDATORY (Step 3) - Starting after Step 2
3. DISCOVERY LOOP UNTIL 3 CONSECUTIVE CLEAN ITERATIONS - Required
4. USER MUST APPROVE feature breakdown before creating epic ticket
5. CREATE EPIC TICKET and get user validation (Steps 4.6-4.7)

**Before Proceeding to Next Step:**
- [x] Read guide: `guides_v2/stages/s1/s1_epic_planning.md`
- [x] Acknowledge critical requirements
- [x] Verify prerequisites from guide
- [x] Update this Quick Reference Card

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** 2026-02-13 (S3 COMPLETE - Gate 4.5 passed, ready for S4)
**Current Stage:** Stage 4 - Feature Testing Strategy
**Current Phase:** S4_READY
**Current Step:** S3 complete, ready to transition to S4 (Feature 01 Testing Strategy)
**Current Guide:** `stages/s4/s4_feature_testing_strategy.md`
**Guide Last Read:** 2026-02-13 (about to read S4 guide)

**Critical Rules from S4 (Preview):**
- Test-driven development: Plan tests BEFORE implementation
- 4-iteration Validation Loop for test strategy
- >90% coverage goal
- Create test_strategy.md for Feature 01

**Progress:** S1 complete, S2 complete, S3 complete (all gates passed: 1, 2, 3, 4.5)
**Next Action:** Read S4 guide, use phase transition prompt, create test_strategy.md for Feature 01
**Blockers:** None

**Notes:**
- Branch created: epic/KAI-9
- EPIC_TRACKER.md updated with KAI-9
- Epic folder created: KAI-9-remove_player_fetcher_legacy_features/
- Epic structure complete: 1 feature folder + epic-level files
- Discovery Phase complete: 5 rounds (3 consecutive clean rounds achieved)
- Epic Ticket validated by user
- Feature breakdown: 1 atomic feature (all removals together)
- Parallelization: N/A (single feature, no benefit)

---

## Epic Overview

**Epic Goal:**
Simplify the player data fetcher by removing legacy features that are no longer needed: locked player preservation, multiple output format support (CSV/Excel), Excel position sheets, configurable export columns, and file caps management. Streamline the codebase to support only position-based JSON output, reducing complexity and maintenance burden.

**Epic Scope:**
Remove unused export formats (CSV, JSON, Excel), locked player preservation logic, file caps management, fix broken imports from deleted config values, clean up Settings class, update tests, and maintain zero regressions in position JSON export (the only remaining export format).

**Key Outcomes:**
1. Simplified codebase - Remove ~600-900 lines of dead code
2. Zero broken imports - Fix all imports referencing deleted config values
3. Streamlined export interface - Only position JSON export remains (6 files: QB, RB, WR, TE, K, DST)
4. Maintained stability - Zero regressions in position JSON functionality
5. Updated tests - All tests passing with removed features

**Original Request:** `remove_player_fetcher_legacy_features_notes.txt`

---

## Initial Scope Assessment

**Epic Size:** SMALL-MEDIUM (1 atomic feature, but significant scope)
**Complexity:** MEDIUM (removal work with multiple interconnected areas)
**Risk Level:** MEDIUM (import fixes required, test updates needed, zero regression tolerance)

**Estimated Components Affected:**
- player_data_exporter.py (export methods, imports)
- player_data_fetcher_main.py (Settings class, main logic, imports)
- tests/ (test updates for removed features)
- Documentation (README.md, ARCHITECTURE.md)

**Similar Existing Patterns:**
- KAI-7: Similar configuration cleanup work
- Previous refactoring epics with import fixes and test updates

---

## Epic-Level Architecture Decisions

**Architectural Approach:** Atomic Removal Strategy

**Decision 1: Single Atomic Feature vs. Phased Approach**
- **Chosen:** Single atomic feature (all deletions together)
- **Rationale:** Prevents broken intermediate states where config deleted but code still references it
- **Alternative Rejected:** Phased approach (config → code → tests) would create broken states between phases
- **Impact:** Larger changeset but guaranteed consistency

**Decision 2: Import-Driven Cleanup Strategy**
- **Chosen:** Delete config → Fix imports → Remove dependent code
- **Rationale:** Import errors provide immediate feedback on missed dependencies
- **Implementation Order:** Config.py deletions first, then import fixes, then method removals
- **Impact:** Clear validation at each step (import errors = incomplete cleanup)

**Decision 3: Zero Regression Tolerance**
- **Chosen:** Position JSON and team exports must work identically to pre-removal baseline
- **Rationale:** These are the only remaining export formats, any regression breaks production
- **Verification:** Manual testing + unit tests + epic smoke testing (3-layer validation)
- **Impact:** Extensive testing required, but ensures production stability

**Decision 4: DataFileManager Integration Pattern**
- **Chosen:** Pass None to DataFileManager instead of DEFAULT_FILE_CAPS
- **Rationale:** DataFileManager already supports None (falls back to shared_config)
- **Alternative Rejected:** Modifying DataFileManager class (out of scope, unnecessary)
- **Impact:** Minimal change, leverages existing functionality

**Decision 5: Test Cleanup Strategy**
- **Chosen:** Delete test classes for removed methods (5 classes), keep tests for remaining functionality (6 classes)
- **Rationale:** User approved in Discovery Q4, aligns with removal scope
- **Alternative Rejected:** Updating tests to skip removed features (leaves dead code)
- **Impact:** Cleaner test suite, maintains 100% pass rate

**Scope Boundaries (What's Preserved):**
- Position JSON export: export_position_json_files() + helpers (UNTOUCHED)
- Team data export: export_teams_to_data() + setters (UNTOUCHED)
- Drafted data loading: LOAD_DRAFTED_DATA_FROM_FILE functionality (OUT OF SCOPE)
- ESPN API calls: All data fetching logic (OUT OF SCOPE)
- DataFileManager class: Implementation (OUT OF SCOPE, only callers updated)

**Integration Approach:**
- **Primary Integration Point:** NFLProjectionsCollector.export_data()
- **Strategy:** Replace export_all_formats_with_teams() call with direct calls to export_position_json_files() + export_teams_to_data()
- **Verification:** Integration point tested in epic smoke testing (Test Scenario 7)

---

## Epic Progress Tracker

**Overall Status:** 0/1 features complete

| Feature | Status | S2 | S3 | S4 | S5 | S6 | S7 | S8 |
|---------|--------|----|----|----|----|----|----|---- |
| Feature 01: Remove Legacy Player Fetcher Features | S3 COMPLETE | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | N/A |

**Legend:** ⬜ Not Started | 🟡 In Progress | ✅ Complete | N/A (S3/S8 not applicable for single-feature epic)

---

## Feature Summary

### Feature 01: Remove Legacy Player Fetcher Features

**Folder:** `feature_01_remove_legacy_player_fetcher_features/`
**Status:** S2 COMPLETE (spec approved, ready for S4)
**Approach:** Atomic removal - all legacy deletions in single feature to avoid broken intermediate states

**Summary:** Remove all legacy export formats (CSV, JSON, Excel), locked player preservation, and file caps management from player data fetcher. Uses import-driven cleanup strategy (delete config → fix imports → remove dependent code) with zero regression requirement for position JSON and team exports.

**Scope:**
- Delete 9 config values + 1 dataclass import from config.py (22 lines)
- Remove 6 export methods + 2 helpers from player_data_exporter.py (~228 lines)
- Remove locked player preservation logic (~100-120 lines)
- Fix 9 broken imports (5 in exporter, 4 in main)
- Remove 4 Settings class fields + update docstring
- Update 2 DataFileManager calls (pass None instead of DEFAULT_FILE_CAPS)
- Update NFLProjectionsCollector.export_data() integration point
- Delete 5 test classes for removed features
- Maintain position JSON export functionality (zero regressions)
- Maintain team data export functionality (export_teams_to_data)

**Key Data Structures:**
- Config deletions: PRESERVE_LOCKED_VALUES, OUTPUT_DIRECTORY, CREATE_CSV/JSON/EXCEL variants, DEFAULT_FILE_CAPS, EXCEL_POSITION_SHEETS, EXPORT_COLUMNS
- Preserved exports: export_position_json_files(), export_teams_to_data()
- Integration: NFLProjectionsCollector → DataExporter → DataFileManager

**Acceptance Criteria:** 13 criteria defined (AC1-AC13) covering config cleanup, import health, method removal, preservation removal, Settings cleanup, DataFileManager updates, integration updates, test cleanup, position JSON integrity, team export preservation, unit test pass rate, code quality, and scope boundaries

**Key Outcomes:**
- ~350-370 lines of dead code removed (228 methods + 120 preservation + 22 config)
- 9 config values deleted, 9 broken imports fixed
- 5 test classes deleted, 6 remaining classes pass at 100%
- 6 position JSON files generate correctly (QB, RB, WR, TE, K, DST)
- 32 team CSV files generate correctly
- Zero regressions in remaining functionality

**Discovery Context:** All findings documented in `../DISCOVERY.md` (user approved), comprehensive research in `RESEARCH_NOTES.md` (9 sections, all code verified)

---

## Epic-Level Files

**Created in S1:**
- `EPIC_README.md` (this file) ✅
- `remove_player_fetcher_legacy_features_notes.txt` ✅
- `epic_smoke_test_plan.md` ✅ (initial placeholder, updated in S4)
- `epic_lessons_learned.md` ✅ (template, populated in S10)
- `DISCOVERY.md` ✅ (user approved)
- `EPIC_TICKET.md` ✅ (user validated)
- `GUIDE_ANCHOR.md` ✅ (for session resumption)
- `research/` folder ✅ (with README.md)

**Feature Folders:**
- `feature_01_remove_legacy_player_fetcher_features/` ✅
  - `README.md` ✅ (Agent Status tracker)
  - `checklist.md` ✅ (template, populated in S2)
  - `lessons_learned.md` ✅ (template, populated in S7.P3)
  - `spec.md` - To be created in S2
  - `test_strategy.md` - To be created in S4
  - `implementation_plan.md` - To be created in S5
  - `implementation_checklist.md` - To be created in S6

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Git branch created (epic/KAI-9)
- [x] EPIC_TRACKER.md updated
- [x] Epic folder created
- [x] Epic notes moved to folder
- [x] EPIC_README.md created (this file)
- [x] Epic Analysis complete (Step 2)
- [x] Discovery Phase complete (Step 3) - MANDATORY ✅
- [x] User approved Discovery findings ✅
- [x] Feature breakdown proposed and user-approved (Step 4) ✅
- [x] Epic ticket created and user-validated (Step 4.6-4.7) ✅
- [x] All feature folders created (Step 5) ✅
- [x] Initial `epic_smoke_test_plan.md` created (Step 5) ✅
- [x] `epic_lessons_learned.md` created (Step 5) ✅
- [x] `GUIDE_ANCHOR.md` created (Step 5) ✅
- [x] `research/` folder created (Step 5) ✅
- [x] Parallelization assessment completed (Step 5.8-5.9) ✅ (N/A - single feature)
- [x] S1 complete, ready for S2 ✅

**S2 - Feature Deep Dives:**
- [x] ALL features have `spec.md` complete ✅
- [x] ALL features have `checklist.md` resolved ✅
- [x] ALL feature `README.md` files created ✅
- [x] S2.P2 Cross-Feature Alignment complete (N/A - single feature) ✅

**S3 - Cross-Feature Sanity Check:**
- [x] S3.P1: Epic testing strategy developed (epic_smoke_test_plan.md - 9 criteria, 8 scenarios) ✅
- [x] S3.P2: Epic documentation refined (EPIC_README.md - architecture decisions, scope boundaries) ✅
- [x] S3.P3: Gate 4.5 passed (user approved epic plan and testing strategy) ✅
- [x] All specs compared systematically (N/A - single feature epic) ✅
- [x] Conflicts resolved (N/A - single feature epic) ✅
- [x] User sign-off obtained (Gate 4.5 passed) ✅

**S4 - Epic Testing Strategy:**
- [ ] `epic_smoke_test_plan.md` updated based on deep dives
- [ ] Integration points identified
- [ ] Epic success criteria defined

**S5-S8 - Feature Implementation:**
{Will be populated after feature breakdown}

**S9 - Epic Final QC:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] Epic QC rounds passed (all 3 rounds)
- [ ] Epic PR review passed (all 11 categories)
- [ ] End-to-end validation vs original request passed

**S10 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned (if needed)
- [ ] Final commits made
- [ ] Epic moved to `feature-updates/done/KAI-9-remove_player_fetcher_legacy_features/`

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| - | - | - | - | - |

**Rule:** If you deviate from guide, DOCUMENT IT HERE immediately.

{No deviations from guides yet}

---

## Epic Completion Summary

{This section will be filled out in S10}
