# Epic Ticket Template

**Filename:** `EPIC_TICKET.md`
**Location:** `feature-updates/KAI-{N}-{epic_name}/EPIC_TICKET.md`
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
This epic integrates JSON player data files into both the win rate simulation and accuracy simulation systems. Currently, simulations use CSV files with incomplete data. After this epic, simulations will use comprehensive JSON files with week-by-week projected and actual player points, enabling more accurate simulation results and historical backtesting.

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
- [ ] All 18 weeks of 2025 season data are accessible and used correctly for both simulations
- [ ] Win rate simulation loads projected points from JSON files (not CSV)
- [ ] Accuracy simulation loads both projected AND actual points from JSON files
- [ ] Actual points for all players across all 18 weeks contain realistic non-zero values
- [ ] Both simulations produce results comparable to or better than CSV-based baseline
- [ ] All unit tests pass (100% pass rate)
- [ ] Epic smoke testing passes (all scenarios)

---

## Success Indicators

**Measurable metrics that show epic succeeded:**

- {Measurable metric 1 with threshold}
- {Measurable metric 2 with threshold}
- {Measurable metric 3 with threshold}

{Example:}
- Week coverage: 18/18 weeks accessible (100% coverage)
- Data completeness: >90% of players have non-zero actual_points for completed weeks
- Simulation accuracy: Mean absolute error improved by >=10% vs CSV baseline
- Test coverage: 100% test pass rate maintained
- Performance: Simulation runtime within 10% of CSV baseline

---

## Failure Patterns (How We'd Know Epic Failed)

**These symptoms indicate the epic FAILED its goals:**

❌ {Symptom of failure 1 - specific and observable}
❌ {Symptom of failure 2}
❌ {Symptom of failure 3}

{Example:}
❌ >90% of actual_points are 0.0 (data loading issue - week offset bug)
❌ Only weeks 17-18 work while other weeks have zeros (week offset logic missing)
❌ Simulations crash when using JSON files but work with CSV
❌ Simulation results drastically different from CSV baseline (>50% variance)
❌ Critical features from epic request not implemented

---

## Scope Boundaries

✅ **In Scope (What IS included):**
- {Item 1 included in epic}
- {Item 2 included in epic}
- {Item 3 included in epic}

{Example:}
✅ Loading JSON files from simulation/sim_data/{year}/weeks/week_{NN}/ folders
✅ Week offset logic (week N loads projected from week_N, actual from week_N+1)
✅ Integration with both win rate and accuracy simulation systems
✅ Comprehensive smoke testing for all 18 weeks

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
This ticket serves as the source of truth for epic-level outcomes. It's created BEFORE folder structure to ensure agent understands WHAT the epic achieves. During Iteration 21 (Spec Validation Against Validated Documents), spec.md will be validated against this ticket to catch misinterpretation.

**Historical context:**
Feature 02 catastrophic bug - agent misinterpreted epic notes line 8, stating "no code changes needed" when epic required week_N+1 folder logic. If epic ticket had existed with "All 18 weeks accessible" criterion, misinterpretation would have been obvious.

**Outcome-focused approach:**
- Epic ticket describes WHAT (outcomes), not HOW (implementation)
- Allows agent to research and design solution in S2
- Prevents premature specification before understanding codebase
```