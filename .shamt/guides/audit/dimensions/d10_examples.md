# D10: Intra-File Consistency — Real Examples

Real examples of D10 violations and fixes, organized by pattern type.

**Referenced from:** `d10_intra_file_consistency.md` → "Real Examples" section

---

## Example 1: Mixed Notation in S5 Guide

**Issue Found During SHAMT-7 Audit Round 3:**

**File:** `stages/s5/s5_v2_validation_loop.md`

**Mixed Content:**
```markdown
# S5.P1: Planning Round 1

This phase covers iterations I1-I7...

## Round 1 Iterations

Complete S5a iterations first...  ← ERROR: Mixed "S5a" with "S5.P1"

## Iteration I1: Requirements

Refer to S5.P1 guide for details...  ← Consistent notation
```diff

**Problem:**
- File header uses "S5.P1"
- Most content uses "S5.P1"
- One section uses "S5a" (old notation)
- Inconsistent within same file

**Fix:**
```diff
## Round 1 Iterations

-Complete S5a iterations first...
+Complete S5.P1 iterations first...
```

**Root Cause:** Content copy-pasted from old guide during update, old notation not replaced

**How D10 Detects:**
- Type 1: Mixed Notation Within Single File
- Automated: CHECK 16 detects files with both old and new notation

---

## Example 2: Contradictory Instructions in Debugging Protocol

**Issue Found During SHAMT-6 Debugging:**

**File:** `debugging/debugging_protocol.md`

**Contradictory Content:**
```markdown
## Section 2: Issue Discovery

ALWAYS create a dedicated issue file for each problem found.

## Section 5: Minor Issues

For minor issues, you can document them in the main checklist without creating separate files.  ← CONTRADICTION
```diff

**Problem:**
- Section 2: ALWAYS create file
- Section 5: Can skip file creation for minor issues
- Agents confused about when files are required

**Fix:**
```diff
## Section 2: Issue Discovery

-ALWAYS create a dedicated issue file for each problem found.
+Create a dedicated issue file for each problem found (exceptions noted below).

## Section 5: Minor Issues

For minor issues (typos, formatting), you can document them in the main checklist without creating separate files.
+This is the ONLY exception to the issue file requirement.
```

**Root Cause:** Rule made absolute, exception added later without updating original rule

**How D10 Detects:**
- Type 2: Contradictory Instructions Within File
- Manual validation: Find ALWAYS statements, check for contradicting permissive statements

---

## Example 3: Terminology Inconsistency in Template

**Issue Found During Template Review:**

**File:** `templates/feature_spec_template.md`

**Mixed Terminology:**
```markdown
# Feature Specification

## Epic Context

This feature is part of the [EPIC_NAME] epic...

## Project Background

The project aims to...  ← INCONSISTENT (epic or project?)

## Initiative Goals

The initiative will deliver...  ← INCONSISTENT (epic, project, or initiative?)
```diff

**Problem:**
- Uses "epic," "project," and "initiative" interchangeably
- No explanation that these are synonyms
- Creates confusion about scope

**Fix:**
```diff
# Feature Specification

## Epic Context

-This feature is part of the [EPIC_NAME] epic...
+This feature is part of the [EPIC_NAME] epic.

-## Project Background
+## Epic Background

-The project aims to...
+The epic aims to...

-## Initiative Goals
+## Epic Goals

-The initiative will deliver...
+The epic will deliver...
```

**Root Cause:** Template created from multiple sources, each using different terminology

**How D10 Detects:**
- Type 3: Inconsistent Terminology Within File
- Automated: CHECK 17 detects high variation in workflow unit terms

---

## Example 4: Structural Inconsistency in Examples

**Issue Found During S7 Guide Review:**

**File:** `stages/s7/s7_p2_qc_rounds.md`

**Inconsistent Example Structure:**
```markdown
### Example 1: Missing Import

**Scenario:** Implementation missing required import
**Problem:** Code fails to run
**Solution:** Add import statement
**Result:** Code executes successfully

### Example 2: Logic Error

**Scenario:** Calculation produces wrong result
**Problem:** Off-by-one error in loop
**Fix:** Update loop condition  ← INCONSISTENT (should be "Solution")
[No Result section]  ← INCONSISTENT (missing)
```diff

**Problem:**
- Example 1: Uses Scenario/Problem/Solution/Result
- Example 2: Uses Scenario/Problem/Fix (not "Solution"), missing Result
- Inconsistent structure confuses readers

**Fix:**
```diff
### Example 2: Logic Error

**Scenario:** Calculation produces wrong result
**Problem:** Off-by-one error in loop
-**Fix:** Update loop condition
+**Solution:** Update loop condition
+**Result:** Calculation produces correct result
```

**Root Cause:** Examples written at different times, structure evolved, old examples not updated

**How D10 Detects:**
- Type 4: Structural Pattern Inconsistencies
- Manual validation: Compare structure of all examples in file

---

## Example 5: Broken Internal Reference After Reorganization

**Issue Found During Guide Reorganization:**

**File:** `stages/s3/s3_epic_planning_approval.md`

**Broken Reference:**
```markdown
## Section 3: Testing Strategy

For detailed testing patterns, see Section 7: Advanced Testing Techniques.

[File only has 5 sections - Section 7 doesn't exist]
```diff

**What Happened:**
- Original file had 8 sections
- During reorganization, Sections 6-8 moved to separate file
- Internal references not updated

**Fix Option 1 (Update Reference):**
```diff
## Section 3: Testing Strategy

-For detailed testing patterns, see Section 7: Advanced Testing Techniques.
+For detailed testing patterns, see `stages/s4/s4_feature_testing_strategy.md`.
```

**Fix Option 2 (Remove Reference if No Longer Relevant):**
```diff
## Section 3: Testing Strategy

-For detailed testing patterns, see Section 7: Advanced Testing Techniques.
+For detailed testing patterns, refer to S4: Feature Testing Strategy.
```

**Root Cause:** File reorganization without updating internal references

**How D10 Detects:**
- Type 5: Internal Reference Accuracy
- Automated: CHECK 18 detects references to non-existent sections

---

**Last Updated:** 2026-02-06
**Version:** 1.1
