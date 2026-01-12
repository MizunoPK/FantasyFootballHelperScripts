# Implementation Plan Template

**Instructions for Agents:**
This template is used during Stage 5a (Implementation Planning) to accumulate findings from the 28 verification iterations. The plan grows incrementally as you progress through 3 rounds.

**Key Principles:**
- Add sections as iterations complete (not all at once)
- User will review and approve this before Stage 5b
- Keep sections concise and actionable
- Use tables for matrices and coverage data

---

## Template

```markdown
# Implementation Plan: {feature_name}

**Created:** {YYYY-MM-DD} Stage 5a - Round 1, Iteration 1
**Last Updated:** {YYYY-MM-DD HH:MM}
**Status:** {Round 1 / Round 2 / Round 3 / Complete}
**Version:** {v1.0 / v2.0 / v3.0}

---

## Implementation Tasks
*Added during iterations 1-7*

### Task 1: {task_name}

**Requirement:** {Link to spec.md requirement - e.g., "Requirement 1 - spec.md line 167"}

**Description:** {Brief description of what this task does}

**File:** `{path/to/file.py}`
**Method:** `{method_name()}`
**Line:** {line_number}

**Change:**
```python
# Current
{current_code}

# New
{new_code}
```

**Acceptance Criteria:**
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

**Dependencies:** {Task numbers this depends on, or "None"}

**Tests:** {Which tests verify this task}

---

### Task 2: {task_name}

{Repeat structure for all tasks}

---

[Continue for all tasks - typically 5-10 tasks per feature]

---

## Algorithm Traceability Matrix
*Added during iteration 4, verified in iterations 11 and 19*

Maps every algorithm in spec.md to exact code location for quick reference during implementation.

| Algorithm | File | Method | Lines | Notes |
|-----------|------|--------|-------|-------|
| {Algorithm 1} | {file.py} | {method()} | {start-end} | {Key notes} |
| {Algorithm 2} | {file.py} | {method()} | {start-end} | {Key notes} |

**Total Mappings:** {count}
**Verification Status:** ✅ All algorithms mapped to code

---

## Component Dependencies
*Added during iteration 2*

**Direct Dependencies:**
- **{Component 1}** ({path/to/file.py})
  - Status: {Already handles X / Requires changes}
  - Verified: {Line numbers where verified}
  - Impact: {What changes needed or why no changes needed}

**This Feature Depends On:**
- {External system / data files / other components}
- Status: {Exists / Needs creation / Verified}

**This Feature Blocks:** {List features that depend on this, or "None"}

**Integration Points:**
- {Method/location 1}: {Description of integration}
- {Method/location 2}: {Description of integration}

---

## Test Strategy
*Added during iterations 8-10*

### Unit Tests

**1. test_{test_name}**
- **Purpose:** {What this test validates}
- **File:** {tests/path/to/test_file.py}
- **Coverage:** {What method/functionality it covers}
- **Test Data:** {Brief description of test data}
- **Expected:** {Expected result}

**2. test_{test_name}**
{Repeat for all unit tests}

### Integration Tests

**{test_number}. test_{test_name}**
- **Purpose:** {E2E validation description}
- **File:** {tests/path/to/test_file.py}
- **Coverage:** {What integration points it validates}
- **Expected:** {Expected result}

### Coverage Matrix

| Method | Success Path | Failure Path | Edge Cases | Coverage |
|--------|--------------|--------------|------------|----------|
| {method_1()} | Task {N} ✅ | {Scenario} ✅ | {Case} ✅ | 100% |
| {method_2()} | Task {N} ✅ | N/A | {Case} ✅ | 100% |

**Overall Coverage:** {percentage}% ({m}/{n} methods tested)

---

## Edge Cases
*Added during iteration 9*

**Total Identified:** {count} edge cases

### {Category Name} ({count} cases)

**{Number}. {Edge Case Name}**
- **Scenario:** {Description of when this happens}
- **Handling:** {How code handles this}
- **Status:** ✅ {Already handled / Explicitly tested / Fixed by Task N}
- **Test:** {Which test covers this, if any}

**{Number}. {Edge Case Name}**
{Repeat for all edge cases in category}

### {Category Name} ({count} cases)
{Repeat for all categories}

**Handling Summary:**
- Already handled by existing code: {count} cases
- Explicitly tested in new tests: {count} cases
- Fixed by Task {N}: {count} cases

---

## Performance Considerations
*Added during iteration 20*

**Analysis:**
- {Performance factor 1}: {Description and measurement}
- {Performance factor 2}: {Description and measurement}
- {Comparison to existing}: {How this compares}

**Impact Assessment:**
- {Impact description with numbers/percentages}

**Conclusion:** {No performance concerns / Optimization needed in X}

---

## Mock Audit
*Added during iteration 21*

**External Dependencies Requiring Mocks:** {List or "None"}

**Rationale:**
{Why mocking is or isn't needed}

**Mocking Strategy:** {Description or "Not needed for this feature"}

---

## Implementation Phasing
*Added during iterations 17-18*

**Step 1: {Phase Name} (Tasks {X-Y})**
- Duration: ~{time estimate}
- Rollback: {How to rollback}

**Step 2: {Phase Name} (Tasks {X-Y})**
- Duration: ~{time estimate}
- Rollback: {How to rollback}

{Repeat for all phases}

**Rollback Strategy:**
- {Overall rollback approach}
- {Any special considerations}

---

## Pre-Implementation Audit (Iteration 23a)
*Added during iteration 23a - MANDATORY GATE*

**Part 1: Completeness Audit**
- Requirements in spec.md: {count}
- Requirements with implementation tasks: {count}
- Coverage: {count}/{total} = {percentage}% {✅/❌}

**Part 2: Specificity Audit**
- Total implementation tasks: {count}
- Tasks with acceptance criteria: {count}
- Tasks with implementation location: {count}
- Tasks with test coverage: {count}
- Specificity: {min}/{total} = {percentage}% {✅/❌}

**Part 3: Interface Contracts Audit**
- Total external dependencies: {count}
- Dependencies verified from source code: {count}
- Verification: {count}/{total} = {percentage}% {✅/❌}

**Part 4: Integration Evidence Audit**
- Total new methods added: {count}
- Methods with identified callers: {count}
- Integration: {count}/{total} = {percentage}% {✅/❌}

**GATE STATUS:** {✅ PASSED / ❌ FAILED} - {Summary}

---

## Implementation Readiness (Iteration 24)
*Added during iteration 24 - GO/NO-GO DECISION*

**Spec Verification:**
- [x/  ] Spec.md complete and validated
- [x/  ] Spec validated against epic notes (Iteration 25)
- [x/  ] Spec validated against epic ticket (Iteration 25)
- [x/  ] Spec validated against spec summary (Iteration 25)

**Implementation Task Verification:**
- [x/  ] All requirements have implementation tasks (100%)
- [x/  ] All tasks have acceptance criteria (100%)
- [x/  ] All tasks have implementation location (100%)
- [x/  ] All tasks have test coverage (100%)

**Iteration Completion:**
- [x/  ] All 25 iterations complete
- [x/  ] Round 1: Iterations 1-7 + 4a ✅
- [x/  ] Round 2: Iterations 8-16 ✅
- [x/  ] Round 3: Iterations 17-22 ✅
- [x/  ] Mandatory gates: 4a ✅, 23a ✅, 25 ✅

**Mandatory Gates:**
- [x/  ] Iteration 4a (TODO Audit): {PASSED/FAILED}
- [x/  ] Iteration 23a (Pre-Implementation Audit): {PASSED/FAILED}
- [x/  ] Iteration 25 (Spec Validation): {PASSED/FAILED}

**Confidence Assessment:**
- [x/  ] Confidence level: {HIGH/MEDIUM/LOW}
- [x/  ] No blockers identified
- [x/  ] No open questions

**Integration Verification:**
- [x/  ] Algorithm traceability: {percentage}%
- [x/  ] Integration gaps: {count}
- [x/  ] Interface contracts: {percentage}%
- [x/  ] Mock audit: {Complete/Incomplete}

**Quality Gates:**
- [x/  ] Test coverage: {percentage}%
- [x/  ] Edge cases: {count} identified, all handled
- [x/  ] Performance: {Analyzed/Not analyzed}

**DECISION:** {✅ GO / ❌ NO-GO} - {Brief explanation}

---

## Version History

**v1.0 ({YYYY-MM-DD HH:MM}) - Round 1 Complete:**
- {Summary of Round 1 additions}
- Iteration 4a GATE: {✅/❌} {PASSED/FAILED}

**v2.0 ({YYYY-MM-DD HH:MM}) - Round 2 Complete:**
- {Summary of Round 2 additions}

**v3.0 ({YYYY-MM-DD HH:MM}) - Round 3 Complete (FINAL):**
- {Summary of Round 3 additions}
- Iteration 23a GATE: {✅/❌} {PASSED/FAILED}
- Iteration 25 GATE: {✅/❌} {PASSED/FAILED}
- Iteration 24: {✅ GO / ❌ NO-GO}

---

## User Approval
*Added after user reviews and approves plan (Gate 5)*

**Approval Status:** {✅ APPROVED / ⏳ PENDING REVIEW / 🔄 REVISIONS REQUESTED}

**Approved By:** {User}
**Approval Date:** {YYYY-MM-DD HH:MM}
**Approved Version:** v3.0

**User Comments:** {Any comments or conditions from user, or "None - approved as-is"}

**Revisions Made (if any):**
- {List any changes made based on user feedback}
- {Or: "None - approved as initially presented"}

---

**STATUS:** {✅ APPROVED - Ready for Stage 5b / ⏳ PENDING USER APPROVAL / 🔄 IN PROGRESS / ❌ BLOCKED}

**Next Step:** {Proceed to Stage 5b (Implementation) / Awaiting user approval / Continue to Round {N} / Fix blocking issues}
```

---

## Usage Notes

**When to create:** Start of Stage 5a, Iteration 1

**How it grows:**
- After Round 1 (iteration 7): ~150 lines (tasks, matrix, dependencies)
- After Round 2 (iteration 16): ~300 lines (+ tests, edge cases)
- After Round 3 (iteration 24): ~400 lines (+ performance, audits, readiness)

**User approval:** Show complete plan after iteration 24, before Stage 5b

**File location:** `feature_XX_{name}/implementation_plan.md`

**Reference during implementation:** This is the PRIMARY reference for Stage 5b (not spec.md alone)
