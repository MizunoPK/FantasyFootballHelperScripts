# Spec Summary Template

**Filename:** `SPEC_SUMMARY.md`
**Location:** `.shamt/epics/SHAMT-{N}-{epic_name}/feature_XX_{name}/SPEC_SUMMARY.md`
**Created:** {YYYY-MM-DD}
**Updated:** Never (immutable after user validation)

**Purpose:** User-validated feature-level outcomes. Validates agent understands WHAT the feature delivers after research but before implementation.

---

## Template

```markdown
## Feature Spec Summary: {feature_name}

**Part of Epic:** {epic_name}
**Created:** {YYYY-MM-DD}
**Status:** {VALIDATED / DRAFT}

---

## Feature Description

{2-3 sentences describing what this specific feature does and why it's needed}

{Focus on OUTCOMES and USER VALUE, not implementation details}

{Example:}
This feature updates the data processing system to load record data from JSON files instead of CSV files. The JSON files contain period-by-period projected and actual values for all records across all {N} periods. This enables historical accuracy analysis by comparing projected values (from period N) against actual values (from period N+1).

---

## What Users Will Be Able To Do

**After this feature, users can:**

- {User-facing capability 1}
- {User-facing capability 2}
- {User-facing capability 3}

{Example:}
- Run analysis using comprehensive JSON record data (not limited CSV data)
- Backtest accuracy across all {N} periods
- See realistic actual values (non-zero) for all records in completed periods
- Compare projected vs actual values for every record every period

---

## Technical Changes

**High-level technical changes (WHAT, not detailed HOW):**

- {High-level change 1 - what's being modified/added}
- {High-level change 2}
- {High-level change 3}

{Example:}
- Period offset logic implemented: period N loads projected from period_N folder, actual from period_N+1 folder
- JSON file loading replaces CSV loading in DataProcessingManager
- Record data structure updated to access period-specific values via getattr(record, f'period_{N}_values')
- All {N} periods accessible (not just the last 1-2)

---

## Acceptance Criteria

**The feature is successful when ALL of these are true:**

- [ ] {Testable requirement 1}
- [ ] {Testable requirement 2}
- [ ] {Testable requirement 3}
- [ ] {Testable requirement 4}

{Add 5-8 acceptance criteria}

{Example:}
- [ ] All {N} periods accessible with non-zero actual and projected values
- [ ] Period offset handled correctly (period N actual comes from period N+1 folder, not period N)
- [ ] DataProcessingManager loads JSON files (not CSV files)
- [ ] Record objects have period-specific values accessible via getattr()
- [ ] Processing results comparable to CSV baseline (within 10% variance)
- [ ] All unit tests pass (100% pass rate)
- [ ] Smoke testing passes (import, entry point, E2E execution with data validation)

---

## Success Metrics

**Measurable indicators with thresholds:**

- {Measurable indicator 1 with threshold}
- {Measurable indicator 2 with threshold}
- {Measurable indicator 3 with threshold}

{Example:}
- Data coverage: {N}/{N} periods accessible (100%)
- Data sanity: <10% of actual_values are 0.0 for completed periods
- Variance check: std_dev > 0 for all record actual_value arrays
- Realistic range: All actual_values within expected domain range
- Performance: Processing runtime within 10% of baseline

---

## Failure Indicators

**These symptoms would mean the feature is BROKEN:**

❌ {Specific symptom that would mean feature is broken}
❌ {Another failure pattern}
❌ {Another failure pattern}

{Example:}
❌ >90% of actual_values are 0.0 (wrong period offset - loading period N instead of N+1)
❌ getattr(record, '{field_name}') returns None (old API still used, consumption code not updated)
❌ Only the last 1-2 periods work while other periods have all zeros (offset not generalized)
❌ Simulation crashes when loading JSON files
❌ Simulation results >50% different from CSV baseline (major logic error)

---

## Scope Boundaries

✅ **In Scope (What IS included in this feature):**
- {Item 1 included}
- {Item 2 included}
- {Item 3 included}

{Example:}
✅ JSON file loading for data processing (DataProcessingManager)
✅ Period offset logic for all {N} periods
✅ Record data structure updates for period-specific access
✅ Unit tests and smoke tests for JSON loading

❌ **Out of Scope (What is NOT included in this feature):**
- {Item 1 NOT included}
- {Item 2 NOT included}
- {Item 3 NOT included}

{Example:}
❌ Processing pipeline updates for other modules (separate features)
❌ UI changes for displaying results
❌ JSON file generation (uses existing files)
❌ Support for historical data from prior configurations

---

## Integration Points

**Where this feature touches other code:**

- {Integration point 1 - where this feature connects to other code}
- {Integration point 2}
- {Integration point 3}

{Example:}
- DataProcessor._load_records() - modified to use JSON loader
- RecordManager (JSON loader) - provides period-specific record data
- ParallelProcessor - consumes updated records from DataProcessor
- Feature 01 (report gen) - shares JSON loading patterns, must align on period offset logic

---

## Dependencies

**Prerequisites for this feature:**

- {Dependency 1}
- {Dependency 2}

{Example:}
- Data files exist in {data_dir}/{period}/ folders
- Data loader supports the required format (if not, must implement)
- Offset pattern understood (period N projected from period_N, actual from period_N+1)

---

## User Validation

**This section filled out by USER - agent presents summary and asks user to verify/approve**

**User comments:**
{User adds any clarifications, corrections, or additional context}

**User approval:** {YES / NO / NEEDS CHANGES}
**Approved by:** {Username}
**Approved date:** {YYYY-MM-DD}

---

## Notes

**Why this summary matters:**
This summary serves as source of truth for feature-level outcomes. It's created AFTER multi-phase research (S2) but BEFORE implementation (S5). During S5 v2 Validation Loop (Dimension 11: Spec Alignment & Cross-Validation), implementation_plan.md will be validated against spec.md, which was validated against this summary to catch misinterpretation.

**Historical context:**
Feature 02 catastrophic bug - spec.md stated "no code changes needed" for week 17/18 logic when it actually required week_N+1 offset for ALL weeks. If spec summary had existed with "week N+1 offset applies to ALL weeks" in Technical Changes, misinterpretation would have been obvious.

**Outcome-focused approach:**
- Spec summary describes WHAT the feature delivers, not detailed implementation
- Created after research (informed by codebase understanding)
- Provides high-level technical changes without premature implementation decisions
- Allows detailed design to happen in S5 (Implementation Planning)
```