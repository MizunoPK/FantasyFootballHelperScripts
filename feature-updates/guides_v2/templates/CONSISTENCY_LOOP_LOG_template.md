# Consistency Loop Log - {Stage}.{Phase} - {Feature/Epic Name}

**Date:** {YYYY-MM-DD}
**Stage:** {S#.P#.I# or S#.P#}
**Context:** {Feature-level | Epic-level}
**Consistency Loop Variant:** {discovery | spec_refinement | alignment | test_strategy | qc_pr}

---

## Overview

**Purpose:** Track Consistency Loop validation rounds and demonstrate "no deferred issues" principle

**Exit Criteria:** 3 consecutive clean rounds (zero issues/gaps found)

**Maximum Rounds:** 10 (escalate to user if exceeded)

---

## Round Tracking

| Round | Date | Reading Pattern | Issues Found | Fixes Applied | Clean? | Consecutive Clean Count |
|-------|------|-----------------|--------------|---------------|--------|------------------------|
| 1 | {YYYY-MM-DD} | Sequential | {N} | {N} | NO | 0 |
| 2 | {YYYY-MM-DD} | {pattern} | {N} | {N} | NO | 0 |
| 3 | {YYYY-MM-DD} | {pattern} | 0 | 0 | YES | 1 |
| 4 | {YYYY-MM-DD} | {pattern} | 0 | 0 | YES | 2 |
| 5 | {YYYY-MM-DD} | {pattern} | 0 | 0 | YES | 3 |

**Exit Round:** {N}
**Exit Condition Met:** 3 consecutive clean rounds (Rounds {N}, {N+1}, {N+2})

---

## Round 1: {Reading Pattern}

**Date:** {YYYY-MM-DD HH:MM}
**Reading Pattern:** Sequential (top to bottom)

### Issues/Gaps Identified

#### Issue 1: {Issue Title}
- **Category:** {Missing Research | Incomplete Section | Unanswered Question | Unverified Assumption | Integration Gap | Unclear Scope}
- **Description:** {Detailed description of issue}
- **Location:** {File/section where issue found}
- **Severity:** {High | Medium | Low}

#### Issue 2: {Issue Title}
- **Category:** {category}
- **Description:** {description}
- **Location:** {location}
- **Severity:** {severity}

[Continue for all issues...]

**Total Issues Found:** {N}

### Fixes Applied

#### Fix for Issue 1:
- **Action Taken:** {What was done to fix}
- **Files Updated:** {List of files modified}
- **Verification:** {How fix was verified}
- **Completed:** {YYYY-MM-DD HH:MM}

#### Fix for Issue 2:
- **Action Taken:** {action}
- **Files Updated:** {files}
- **Verification:** {verification}
- **Completed:** {timestamp}

[Continue for all fixes...]

**All Issues Fixed:** YES (zero deferred issues)
**Clean Round:** NO (issues were found)
**Consecutive Clean Count:** 0 (reset)

---

## Round 2: {Reading Pattern}

**Date:** {YYYY-MM-DD HH:MM}
**Reading Pattern:** {Reverse order | Different focus | Thematic clustering}

### Issues/Gaps Identified

#### Issue 3: {Issue Title}
- **Category:** {category}
- **Description:** {description}
- **Location:** {location}
- **Severity:** {severity}

[Continue for all issues...]

**Total Issues Found:** {N}

### Fixes Applied

[Same structure as Round 1...]

**All Issues Fixed:** YES (zero deferred issues)
**Clean Round:** {YES/NO}
**Consecutive Clean Count:** {0 or incremented}

---

## Round 3: {Reading Pattern}

**Date:** {YYYY-MM-DD HH:MM}
**Reading Pattern:** {pattern}

### Issues/Gaps Identified

**NO ISSUES FOUND**

**Total Issues Found:** 0

### Fixes Applied

**NO FIXES NEEDED**

**All Issues Fixed:** N/A (no issues)
**Clean Round:** YES
**Consecutive Clean Count:** 1

---

## Round 4: {Reading Pattern}

**Date:** {YYYY-MM-DD HH:MM}
**Reading Pattern:** {pattern}

### Issues/Gaps Identified

**NO ISSUES FOUND**

**Total Issues Found:** 0

**Clean Round:** YES
**Consecutive Clean Count:** 2

---

## Round 5: {Reading Pattern}

**Date:** {YYYY-MM-DD HH:MM}
**Reading Pattern:** {pattern}

### Issues/Gaps Identified

**NO ISSUES FOUND**

**Total Issues Found:** 0

**Clean Round:** YES
**Consecutive Clean Count:** 3

**EXIT CRITERIA MET:** 3 consecutive clean rounds (Rounds 3, 4, 5)

---

## Summary

**Total Rounds:** 5
**Total Issues Found:** {N} (all fixed immediately)
**Total Fixes Applied:** {N}
**Deferred Issues:** 0 (zero tolerance policy enforced)
**Consecutive Clean Rounds:** 3 (Rounds 3-5)
**Exit Condition:** MET

**Time Spent:**
- Total: {X} hours
- Per Round Average: {Y} minutes

**Outcome:** Document/work validated through Consistency Loop - ready to proceed

---

## Reading Patterns Used

**Reference:** `reference/consistency_loop_{variant}.md`

**Patterns applied:**
- Round 1: {pattern and purpose}
- Round 2: {pattern and purpose}
- Round 3: {pattern and purpose}
- Round 4: {pattern and purpose}
- Round 5: {pattern and purpose}

---

## Notes

**Key Insights:**
- {Insight 1: What types of issues were commonly found}
- {Insight 2: What patterns helped catch issues}
- {Insight 3: Lessons for future Consistency Loops}

**Recommendations:**
- {Recommendation for future use}
- {Improvement suggestion}

---

*This log demonstrates the "no deferred issues" principle: ALL issues fixed immediately in the round they were found, with 3 consecutive clean rounds required to exit.*
