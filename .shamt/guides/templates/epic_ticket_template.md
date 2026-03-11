# Epic Ticket Template

**Filename:** `EPIC_TICKET.md`
**Location:** `.shamt/epics/SHAMT-{N}-{epic_name}/EPIC_TICKET.md`
**Created:** {YYYY-MM-DD}
**Updated:** Never (immutable after user validation)

**Purpose:** User-validated epic-level outcomes. Validates agent understands WHAT the epic achieves before folder creation.

---

## Template

```markdown
## Epic Ticket: {epic_name}

**Created:** {YYYY-MM-DD}
**Status:** {VALIDATED / DRAFT}

---

## Description

{2-3 sentences describing what this epic achieves and why it matters}

{Focus on OUTCOMES, not implementation details}

{Example:}
This epic integrates JSON record data files into both processing modules. Currently, modules use CSV files with incomplete data. After this epic, modules will use comprehensive JSON files with period-by-period projected and actual values, enabling more accurate processing results and historical analysis.

---

## Acceptance Criteria (Epic-Level)

**The epic is successful when ALL of these are true:**

- [ ] {Testable outcome 1 - applies to ENTIRE epic, not just one feature}
- [ ] {Testable outcome 2}
- [ ] {Testable outcome 3}
- [ ] {Testable outcome 4}
- [ ] {Testable outcome 5}

{Add 5-10 acceptance criteria}

{Important: These should be TESTABLE and OBSERVABLE}

{Example:}
- [ ] All {N} periods of data are accessible and used correctly for both processing modules
- [ ] Processing module A loads projected values from JSON files (not CSV)
- [ ] Processing module B loads both projected AND actual values from JSON files
- [ ] Actual values for all records across all {N} periods contain realistic non-zero values
- [ ] Both processing modules produce results comparable to or better than CSV-based baseline
- [ ] All unit tests pass (100% pass rate)
- [ ] Epic smoke testing passes (all scenarios)

---

## Success Indicators

**Measurable metrics that show epic succeeded:**

- {Measurable metric 1 with threshold}
- {Measurable metric 2 with threshold}
- {Measurable metric 3 with threshold}

{Example:}
- Data coverage: {N}/{N} periods accessible (100% coverage)
- Data completeness: >90% of records have non-zero actual_values for completed periods
- Accuracy: Error metric improved by >=10% vs baseline
- Test coverage: 100% test pass rate maintained
- Performance: Processing runtime within 10% of baseline

---

## Failure Patterns (How We'd Know Epic Failed)

**These symptoms indicate the epic FAILED its goals:**

❌ {Symptom of failure 1 - specific and observable}
❌ {Symptom of failure 2}
❌ {Symptom of failure 3}

{Example:}
❌ >90% of actual_values are 0.0 (data loading issue - period offset bug)
❌ Only last 1-2 periods work while earlier periods have zeros (offset logic missing)
❌ Processing crashes when using new format but works with old format
❌ Results drastically different from baseline (>50% variance)
❌ Critical features from epic request not implemented

---

## Scope Boundaries

✅ **In Scope (What IS included):**
- {Item 1 included in epic}
- {Item 2 included in epic}
- {Item 3 included in epic}

{Example:}
✅ Loading data files from {data_dir}/{period}/ folders
✅ Offset logic (period N loads projected from period_N, actual from period_N+1)
✅ Integration with both subsystem A and subsystem B
✅ Comprehensive smoke testing for all {N} periods

❌ **Out of Scope (What is NOT included):**
- {Item 1 NOT included in epic}
- {Item 2 NOT included in epic}
- {Item 3 NOT included in epic}

{Example:}
❌ Generating NEW JSON files from external APIs (uses existing files only)
❌ UI changes for displaying JSON-based results
❌ Performance optimization beyond maintaining parity with CSV baseline
❌ Support for seasons other than 2025 (can be future work)

---

## User Validation

**This section filled out by USER - agent presents ticket and asks user to verify/approve**

**User comments:**
{User adds any clarifications, corrections, or additional context}

**User approval:** {YES / NO / NEEDS CHANGES}
**Approved by:** {Username}
**Approved date:** {YYYY-MM-DD}

---

## Notes

**Why this ticket matters:**
This ticket serves as the source of truth for epic-level outcomes. It's created BEFORE folder structure to ensure agent understands WHAT the epic achieves. During S5 v2 Validation Loop (Dimension 11: Spec Alignment & Cross-Validation), implementation_plan.md will be validated against spec.md, which was validated against this ticket to catch misinterpretation.

**Historical context:**
Feature 02 catastrophic bug - agent misinterpreted epic notes line 8, stating "no code changes needed" when epic required week_N+1 folder logic. If epic ticket had existed with "All 18 weeks accessible" criterion, misinterpretation would have been obvious.

**Outcome-focused approach:**
- Epic ticket describes WHAT (outcomes), not HOW (implementation)
- Allows agent to research and design solution in S2
- Prevents premature specification before understanding codebase
```