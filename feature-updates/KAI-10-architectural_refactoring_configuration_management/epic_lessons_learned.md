## Epic Lessons Learned: architectural_refactoring_configuration_management

**Epic Overview:** Comprehensive architectural refactoring of all 7 runner scripts from scattered/hardcoded configuration to CLI-based configuration with dependency injection, fast E2E test modes, debug support, and an integration test framework.
**Date Range:** 2026-02-18 - {end_date}
**Total Features:** 8
**Total Bug Fixes:** {N — to be filled}

---

## Purpose

This document captures:
- **Cross-feature insights** (patterns observed across multiple features)
- **Systemic issues** (problems affecting multiple features)
- **Guide improvements** (updates needed for guides_v2/)
- **Workflow refinements** (process improvements for future epics)

**This is separate from per-feature lessons_learned.md files** (which capture feature-specific insights).

---

## S1 Lessons Learned (Epic Planning)

**What Went Well:**
- Discovery Phase Validation Loop caught several issues (wave grouping error, architecture pattern error) before they propagated to feature specs
- 3-wave structure decision (Feature 01 solo → Features 02-07 parallel → Feature 08) correctly applied "design precedent" rationale
- Merging Features 01+10 (player_fetcher argparse + DI) eliminated confusing execution ordering concern
- Dropping documentation as separate feature (integrating into workflow) aligned with guides' guidance against documentation features

**What Could Be Improved:**
- {To be filled after S1 complete and S2 begins}

**Insights for Future Epics:**
- When notes describe two features with "Feature X must execute before Feature Y" ordering, often a merge is more appropriate
- Spec dependency check ("can I write complete spec without upstream output structure?") is a critical tool — apply rigorously

**Guide Improvements Needed:**
- {To be filled}

---

## S2 Lessons Learned (Feature Deep Dives)

{Lessons captured AFTER all features complete S2}

### Cross-Feature Patterns

{To be filled}

### Feature-Specific Highlights

{To be filled}

### What Went Well

{To be filled}

### What Could Be Improved

{To be filled}

### Guide Improvements Needed

{To be filled}

---

## S3 Lessons Learned (Cross-Feature Sanity Check)

**What Went Well:**
{To be filled}

**What Could Be Improved:**
{To be filled}

**Conflicts Discovered:**
{To be filled}

**Insights for Future Epics:**
{To be filled}

**Guide Improvements Needed:**
{To be filled}

---

## S4 Lessons Learned (Epic Testing Strategy)

**What Went Well:**
{To be filled}

**What Could Be Improved:**
{To be filled}

**epic_smoke_test_plan.md Evolution:**
{To be filled}

**Guide Improvements Needed:**
{To be filled}

---

## S5 Lessons Learned (Feature Implementation)

{Capture lessons AFTER EACH feature completes S8.P2}

### Feature 01 (refactor_player_data_fetcher) — Stages S5 through S8

{To be filled after Feature 01 completes}

---

### Feature 02 (schedule_fetcher_cli) — Stages S5 through S8

{To be filled after Feature 02 completes}

---

### Feature 03 (game_data_fetcher_cli) — Stages S5 through S8

{To be filled after Feature 03 completes}

---

### Feature 04 (historical_compiler_cli) — Stages S5 through S8

{To be filled after Feature 04 completes}

---

### Feature 05 (win_rate_simulation_e2e) — Stages S5 through S8

{To be filled after Feature 05 completes}

---

### Feature 06 (accuracy_simulation_e2e) — Stages S5 through S8

{To be filled after Feature 06 completes}

---

### Feature 07 (league_helper_cli) — Stages S5 through S8

{To be filled after Feature 07 completes}

---

### Feature 08 (integration_test_framework) — Stages S5 through S8

{To be filled after Feature 08 completes}

---

### Cross-Feature Implementation Patterns

{To be filled after multiple features complete}

---

### Debugging Insights Across Features

**Total Debugging Sessions:** {N} features required debugging

**Common Bug Patterns:**
{To be filled}

**Common Process Gaps:**
{To be filled}

**Most Impactful Guide Updates:**
{To be filled}

**Testing Insights:**
{To be filled}

---

### Guide Improvements Needed from S5

{To be filled after features complete}

---

## S9 Lessons Learned (Epic Final QC)

**What Went Well:**
{To be filled}

**What Could Be Improved:**
{To be filled}

**Epic-Level Issues Found:**
{To be filled}

**epic_smoke_test_plan.md Effectiveness:**
{To be filled}

**Guide Improvements Needed:**
{To be filled}

---

## S10 Lessons Learned (Epic Cleanup)

**What Went Well:**
{To be filled}

**What Could Be Improved:**
{To be filled}

**Documentation Quality:**
{To be filled}

**Guide Improvements Needed:**
{To be filled}

---

## Cross-Epic Insights

{High-level insights applicable beyond this epic}

**Systemic Patterns:**
{To be filled}

**Workflow Refinements:**
{To be filled}

**Tool/Process Improvements:**
{To be filled}

---

## Recommendations for Future Epics

{To be filled after S10}

---

## Guide Updates Applied

{Track which guides were updated based on lessons from THIS epic}

**Guides Updated:**
{To be filled in S10.P1}

**CLAUDE.md Updates:**
{To be filled in S10.P1}

**Date Applied:** {YYYY-MM-DD}

---

## Metrics

**Epic Duration:** {N} days
**Features:** 8
**Bug Fixes:** {N}
**Tests Added:** {N}
**Files Modified:** {N}
**Lines of Code Changed:** ~{N}

**Stage Durations:**
- S1: {N} days
- S2: {N} days (all features)
- S3: {N} days
- S4: {N} days
- S5: {N} days (all features)
- S9: {N} days
- S10: {N} days

**QC Restart Count:**
- S7 restarts: {N} (across all features)
- S9 restarts: {N}

**Test Pass Rates:**
- Final pass rate: {percentage}% ({X}/{Y} tests)
- Tests added by this epic: {N}
