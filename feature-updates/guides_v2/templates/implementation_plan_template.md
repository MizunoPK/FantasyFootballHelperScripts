# Implementation Plan Template

**Instructions for Agents:**
This template is used during S5 v2 (Implementation Planning) created through Draft Creation phase and validated through the Validation Loop. The plan is drafted in Phase 1, then systematically validated across 11 dimensions until 3 consecutive clean rounds are achieved.

**Key Principles:**
- Add sections as iterations complete (not all at once)
- User will review and approve this before S6
- Keep sections concise and actionable
- Use tables for matrices and coverage data

---

## Template

```markdown
## Implementation Plan: {feature_name}

**Created:** {YYYY-MM-DD} S5 v2 - Phase 1 (Draft Creation)
**Last Updated:** {YYYY-MM-DD HH:MM}
**Status:** {Draft / Validation Loop / Complete}
**Version:** {v1.0 / v2.0 / v3.0}

---

## Implementation Tasks
*Created during Phase 1 (Draft Creation)*

### Task 1: {task_name}

**Requirement:** {Link to spec.md requirement - e.g., "Requirement 1 - spec.md line 167"}

**Description:** {Brief description of what this task does}

**File:** `{path/to/file.py}`
**Method:** `{method_name()}`
**Line:** {line_number}

**Change:**
```
## Current
{current_code}

## New
{new_code}
```markdown

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
*Created during Phase 1, validated during Phase 2*

Maps every algorithm in spec.md to exact code location for quick reference during implementation.

| Algorithm | File | Method | Lines | Notes |
|-----------|------|--------|-------|-------|
| {Algorithm 1} | {file.py} | {method()} | {start-end} | {Key notes} |
| {Algorithm 2} | {file.py} | {method()} | {start-end} | {Key notes} |

**Total Mappings:** {count}
**Verification Status:** ✅ All algorithms mapped to code

---

## Component Dependencies
*Created during Phase 1 (Draft Creation)*

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
*Created during Phase 1, refined during Phase 2*

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
*Created during Phase 1, refined during Phase 2*

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
*Validated during Phase 2 (Validation Loop)*

**Analysis:**
- {Performance factor 1}: {Description and measurement}
- {Performance factor 2}: {Description and measurement}
- {Comparison to existing}: {How this compares}

**Impact Assessment:**
- {Impact description with numbers/percentages}

**Conclusion:** {No performance concerns / Optimization needed in X}

---

## Mock Audit
*Validated during Phase 2 (Validation Loop)*

**External Dependencies Requiring Mocks:** {List or "None"}

**Rationale:**
{Why mocking is or isn't needed}

**Mocking Strategy:** {Description or "Not needed for this feature"}

---

## Implementation Phasing
*Added during Draft Creation (Phase 1)*

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

## S5 v2 Validation Loop Completion
*Completed during Phase 2 (Validation Loop) - MANDATORY GATE*

**Phase 1 Status:**
- [ ] Draft Creation complete (~70% quality baseline)
- [ ] All 11 dimension sections created
- [ ] Requirements mapping tables complete
- [ ] Algorithm traceability matrix drafted

**Phase 2 Status:**
- [ ] Validation Loop complete (3 consecutive clean rounds)
- [ ] Total validation rounds executed: {count}
- [ ] All 7 master dimensions validated: ✅
- [ ] All 11 S5-specific dimensions validated: ✅

**11 Dimension Validation Summary:**
1. Requirements Completeness: ✅
2. Interface & Dependency Verification: ✅
3. Algorithm Traceability: ✅
4. Task Specification Quality: ✅
5. Data Flow & Consumption: ✅
6. Error Handling & Edge Cases: ✅
7. Integration & Compatibility: ✅
8. Test Coverage Quality: ✅
9. Performance & Dependencies: ✅
10. Implementation Readiness: ✅
11. Spec Alignment & Cross-Validation: ✅

**Completeness Metrics:**
- Requirements in spec.md: {count}
- Requirements with implementation tasks: {count}
- Coverage: {count}/{total} = {percentage}% (Must be 100%)
- Algorithm mappings: {count}
- External dependencies verified: {count}/{count} = 100%

**Quality Metrics:**
- Tasks with acceptance criteria: {count}/{total} = {percentage}%
- Tasks with implementation location: {count}/{total} = {percentage}%
- Tasks with test coverage: {count}/{total} = {percentage}%
- Edge cases identified: {count}

**Confidence Assessment:**
- [ ] Confidence level: {HIGH/MEDIUM/LOW}
- [ ] No blockers identified
- [ ] No open questions
- [ ] No deferred issues

**Gate 5 Ready:** {✅ YES / ❌ NO} - {Brief explanation}

---

## Version History

**v1.0 ({YYYY-MM-DD HH:MM}) - Phase 1 Complete (Draft Creation):**
- Initial draft created (~70% quality baseline)
- All 11 dimension sections included
- Requirements mapping and algorithm traceability drafted

**v2.0+ ({YYYY-MM-DD HH:MM}) - Phase 2 Validation Loop:**
- Validation Round {N}: {Summary of issues found and fixed}
- {Continue tracking validation rounds until 3 consecutive clean rounds}

**v{Final} ({YYYY-MM-DD HH:MM}) - Validation Loop Complete:**
- 3 consecutive clean validation rounds achieved
- All 18 dimensions validated (7 master + 11 S5-specific)
- Ready for Gate 5 (User Approval)

---

## User Approval
*Added after user reviews and approves plan (Gate 5)*

**Approval Status:** {✅ APPROVED / ⏳ PENDING REVIEW / 🔄 REVISIONS REQUESTED}

**Approved By:** {User}
**Approval Date:** {YYYY-MM-DD HH:MM}
**Approved Version:** v{Final}

**User Comments:** {Any comments or conditions from user, or "None - approved as-is"}

**Revisions Made (if any):**
- {List any changes made based on user feedback}
- {Or: "None - approved as initially presented"}

---

**STATUS:** {✅ APPROVED - Ready for S6 / ⏳ PENDING USER APPROVAL / 🔄 IN PROGRESS / ❌ BLOCKED}

**Next Step:** {Proceed to S6 (Implementation) / Awaiting user approval / Continue to Round {N} / Fix blocking issues}
```

---

## Usage Notes

**When to create:** Start of S5 v2, Phase 1 (Draft Creation)

**How it grows:**
- After Phase 1 (Draft Creation): ~300-400 lines (~70% quality baseline)
- During Phase 2 (Validation Loop): Incremental refinement through validation rounds
- After Validation Loop complete: ~400-500 lines (99%+ quality, ready for Gate 5)

**User approval:** Show complete plan after Phase 2 validation complete (Gate 5), before S6

**File location:** `feature_XX_{name}/implementation_plan.md`

**Reference during implementation:** This is the PRIMARY reference for S6 (not spec.md alone)
