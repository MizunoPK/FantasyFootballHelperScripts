# Stage 2: Fix Planning

**Purpose:** Organize discovered issues into executable fix groups with clear priorities
**Duration:** 15-30 minutes
**Input:** Discovery report from Stage 1
**Output:** Fix plan with grouped patterns and sed commands
**Reading Time:** 10-15 minutes

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Fix Planning Strategy](#fix-planning-strategy)
4. [Grouping Issues](#grouping-issues)
5. [Creating Fix Commands](#creating-fix-commands)
6. [Exit Criteria](#exit-criteria)

---

## Overview

### Purpose

**Stage 2: Fix Planning** transforms the discovery report into an actionable fix plan. The goals are:
- Group similar issues together for batch fixing
- Prioritize by severity (Critical → High → Medium → Low)
- Create sed commands for automated fixes
- Identify issues requiring manual review
- Minimize number of file edits

### Why Planning Matters

**Without planning:**
- Fix issues randomly → inefficient
- Touch same file multiple times → error-prone
- Miss pattern variations → incomplete fixes
- No prioritization → critical issues delayed

**With planning:**
- Fix by pattern group → efficient
- Touch each file once → clean commits
- Catch all variations → complete fixes
- Critical first → faster impact

---

## Prerequisites

### Before Starting Fix Planning

**Verify you have:**

- [ ] Completed Stage 1 (Discovery)
- [ ] Discovery report with ALL issues documented
- [ ] Issues categorized by dimension
- [ ] Severity assigned to each issue
- [ ] File paths and line numbers for each issue
- [ ] Pattern that found each issue documented

**If missing any:** Return to Stage 1 and complete discovery fully.

---

## Fix Planning Strategy

### The Grouping Process

```
Step 1: Review All Issues
  ↓
Step 2: Group by Pattern Similarity (not by file)
  ↓
Step 3: Prioritize Groups by Severity
  ↓
Step 4: Create Sed Commands for Each Group
  ↓
Step 5: Identify Manual Review Cases
  ↓
Step 6: Document Fix Order
```

---

## Grouping Issues

### Group by Pattern, Not by File

**❌ WRONG: Group by File**
```markdown
Group 1: Fix s5_p1_planning_round1.md
  - Issue #5: "5a" → "S5.P1"
  - Issue #12: "stages/s5/round1/" → "stages/s5/s5_p1_"

Group 2: Fix s5_p2_planning_round2.md
  - Issue #6: "5a" → "S5.P1"
  - Issue #13: "stages/s5/round2/" → "stages/s5/s5_p2_"
```
**Problem:** Same pattern fixed multiple times, inefficient

**✅ CORRECT: Group by Pattern**
```markdown
Group 1: Old Notation "5a/5b/5c" → "S5.P1/P2/P3"
  - Issue #5: s5_p1_planning_round1.md:45
  - Issue #6: s5_p2_planning_round2.md:78
  - Issue #18: s5_bugfix_workflow.md:123
  [20 instances across 8 files]

Group 2: Old Paths "stages/s5/round1/" → "stages/s5/s5_p1_"
  - Issue #12: s5_p1_planning_round1.md:155
  - Issue #19: s5_p1_i1_requirements.md:67
  [15 instances across 6 files]
```
**Benefit:** Fix all instances of pattern at once with single sed command

### Grouping Criteria

**Group issues together if:**
1. Same OLD pattern (exact match)
2. Same NEW replacement (deterministic)
3. Same context (all errors, or all intentional exceptions)

**Separate into different groups if:**
1. Different OLD patterns
2. Different NEW replacements
3. Mixed context (some errors, some intentional)
4. Requires manual review

### Example Grouping

**From Discovery Report:**
```
Total Issues: 45
- D1 (Cross-Reference): 20 issues
- D2 (Terminology): 18 issues
- D10 (File Size): 2 issues
- D13 (Documentation Quality): 5 issues
```

**Grouped by Pattern:**
```markdown
## Fix Groups

### Group 1: Old Stage Notation (D2)
**Pattern:** \bS[5-9]a\b → S[5-9].P1 (and b/c/d/e variations)
**Count:** 18 instances
**Files:** 12 files
**Severity:** High
**Automated:** Yes

### Group 2: Broken File References (D1)
**Pattern:** stages/s5/round1/file.md → stages/s5/s5_p1_file.md
**Count:** 12 instances
**Files:** 8 files
**Severity:** Critical
**Automated:** Yes

### Group 3: Missing Prerequisites Sections (D13)
**Pattern:** N/A (requires manual addition)
**Count:** 5 instances
**Files:** 5 files
**Severity:** Medium
**Automated:** No

### Group 4: Oversized Files (D10)
**Pattern:** N/A (requires file split)
**Count:** 2 instances
**Files:** 2 files
**Severity:** Medium
**Automated:** No
```

---

## Prioritizing Groups

### Priority Levels

**P0 - Critical (Fix Immediately):**
- Breaks workflow
- Wrong file paths
- Template errors
- CLAUDE.md sync issues

**P1 - High (Fix in Same Session):**
- Causes confusion
- Inconsistent terminology
- Missing required sections
- Wrong stage references

**P2 - Medium (Fix Soon):**
- Cosmetic but important
- Minor inconsistencies
- Non-critical counts

**P3 - Low (Fix When Time Allows):**
- Nice-to-have
- Minor formatting

### Fix Order

**Execute groups in this order:**

```
1. P0 groups (all)
   ↓
2. P1 groups (all)
   ↓
3. P2 groups (all)
   ↓
4. P3 groups (if time)
```

**Within same priority:**
```
1. Automated fixes first (faster)
   ↓
2. Manual fixes second (require thought)
```

---

## Creating Fix Commands

### Sed Command Template

**For automated fixes:**

```bash
# Group X: [Description]
# Pattern: [OLD] → [NEW]
# Count: N instances across M files
# Severity: [Critical/High/Medium/Low]

# Approach 1: Single file
sed -i 's|OLD_PATTERN|NEW_PATTERN|g' path/to/file.md

# Approach 2: Multiple files (same pattern)
sed -i 's|OLD_PATTERN|NEW_PATTERN|g' file1.md file2.md file3.md

# Approach 3: All files in folder
sed -i 's|OLD_PATTERN|NEW_PATTERN|g' stages/s5/*.md

# Approach 4: All markdown files
find . -name "*.md" -exec sed -i 's|OLD_PATTERN|NEW_PATTERN|g' {} +
```

### Pattern Escaping

**Special characters that need escaping:**

```bash
# In sed patterns, escape these: . * [ ] ^ $ / \

# Example: Replacing file paths
# Path: stages/s5/round1_todo.md
# Escaped: stages\/s5\/round1_todo\.md

sed -i 's|stages/s5/round1_todo\.md|stages/s5/s5_p1_planning.md|g' file.md

# Using | as delimiter (recommended for paths)
sed -i 's|stages/s5/round1_todo.md|stages/s5/s5_p1_planning.md|g' file.md
```

### Word Boundary Regex

**Prevent partial matches:**

```bash
# Wrong: Will match "5ab", "15a", etc.
sed -i 's/5a/S5.P1/g' file.md

# Correct: Only matches standalone "5a"
sed -i 's/\b5a\b/S5.P1/g' file.md
```

### Example Fix Plan

```markdown
# Fix Plan - Round N

## Execution Order

### Group 1: Critical File References (P0)
```bash
# Fix broken stages/s5/round1/ references
sed -i 's|stages/s5/round1/iterations_1_3\.md|stages/s5/s5_p1_i1_requirements.md|g; \
        s|stages/s5/round1/iteration_4\.md|stages/s5/s5_p1_i2_algorithms.md|g; \
        s|stages/s5/round1/iteration_7\.md|stages/s5/s5_p1_i3_integration.md|g' \
    stages/s5/s5_p1_*.md
```

**Verification:**
```bash
# Should return 0
grep -rn "stages/s5/round1/" stages/s5/ --include="*.md" | wc -l
```

### Group 2: Old Notation (P1)
```bash
# Fix S5a/5b/5c notation
sed -i 's/\bS5a\b/S5.P1/g; s/\bS5b\b/S5.P2/g; s/\bS5c\b/S5.P3/g' \
    stages/s5/*.md stages/s2/*.md stages/s10/*.md
```

**Verification:**
```bash
# Should return 0 (or only intentional cases)
grep -rn "\bS5[a-e]\b" stages --include="*.md" | wc -l
```

### Group 3: Missing Prerequisites (P2 - MANUAL)
**Files needing Prerequisites section:**
1. stages/s5/s5_bugfix_workflow.md (line 45 - add after Overview)
2. stages/s7/s7_p2_qc_rounds.md (line 67 - add after Overview)
3. stages/s9/s9_p3_user_testing.md (line 89 - add after Overview)

**Action:** Manually add using Edit tool, following template structure
```
```

---

## Manual Review Cases

### When Manual Review Required

**Flag for manual review if:**

1. **Context-Sensitive:**
   - Pattern appears in both error and intentional contexts
   - Requires reading surrounding lines to determine
   - Example: "5a" in historical example vs current workflow

2. **Complex Replacement:**
   - No simple OLD→NEW mapping
   - Requires understanding file purpose
   - Example: Restructuring oversized files

3. **Adds New Content:**
   - Missing sections need to be written
   - Cannot use sed (no OLD pattern to replace)
   - Example: Adding Prerequisites section

4. **User Decision Needed:**
   - Multiple valid fix options
   - Trade-offs to consider
   - Example: Split large file or use router pattern?

### Manual Review Documentation

**For each manual case, document:**

```markdown
## Manual Review #X

**Issue:** [Description]
**File:** path/to/file.md
**Line:** 123
**Reason for Manual:** [Context-sensitive / Complex / New content / User decision]

**Options:**
1. [Option 1 description]
   - Pros: [benefits]
   - Cons: [drawbacks]

2. [Option 2 description]
   - Pros: [benefits]
   - Cons: [drawbacks]

**Recommendation:** [Your recommendation with rationale]

**Action Required:**
- [ ] Analyze context
- [ ] Choose option
- [ ] Apply fix
- [ ] Verify
```

---

## Exit Criteria

### Stage 2 Complete When ALL These Are True

- [ ] All issues from discovery report reviewed
- [ ] Issues grouped by pattern similarity
- [ ] Groups prioritized (P0 → P1 → P2 → P3)
- [ ] Sed commands created for automated fixes
- [ ] Word boundaries used where appropriate (\b)
- [ ] Verification commands written for each group
- [ ] Manual review cases identified and documented
- [ ] Fix plan document created with:
  - [ ] Group number and description
  - [ ] Old pattern → New pattern
  - [ ] Count and file list
  - [ ] Sed command
  - [ ] Verification command
  - [ ] Estimated duration
- [ ] Ready to proceed to Stage 3 (Apply Fixes)

**If ANY criterion incomplete:** Continue planning until all complete.

---

## See Also

**Next Stage:**
- `stage_3_apply_fixes.md` - Execute the fix plan incrementally

**Reference:**
- `../reference/verification_commands.md` - More verification examples
- `../templates/fix_plan_template.md` - Use this template for fix plan output

**Dimensions:**
- Relevant dimension guides for context on each issue type

---

**After completing Stage 2:** Proceed to `stages/stage_3_apply_fixes.md`
