# Stage 3: Apply Fixes

**Purpose:** Execute fix plan incrementally with immediate verification after each change
**Duration:** 30-90 minutes (depends on issue count)
**Input:** Fix plan from Stage 2
**Output:** Fixed files with documented before/after evidence
**Reading Time:** 10-15 minutes

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [The Incremental Approach](#the-incremental-approach)
4. [Fix Execution Process](#fix-execution-process)
5. [Verification After Each Fix](#verification-after-each-fix)
6. [Manual Fix Guidelines](#manual-fix-guidelines)
7. [Exit Criteria](#exit-criteria)
8. [Common Pitfalls](#common-pitfalls)

---

## Overview

### Purpose

**Stage 3: Apply Fixes** is where you execute the fix plan from Stage 2. The critical principle:

**Fix ONE group at a time, verify IMMEDIATELY, then move to next group.**

**Never batch all fixes** - incremental verification catches errors early.

### Why Incremental Matters

**Without incremental verification:**
```bash
# Bad: Apply all 10 fix groups at once
sed -i 's/OLD1/NEW1/g' *.md
sed -i 's/OLD2/NEW2/g' *.md
sed -i 's/OLD3/NEW3/g' *.md
...
sed -i 's/OLD10/NEW10/g' *.md

# Problem: If fix #3 broke something, you don't know until the end
# Problem: Hard to isolate which fix caused the issue
# Problem: No checkpoints to rollback to
```

**With incremental verification:**
```bash
# Good: Fix group 1, verify immediately
sed -i 's/OLD1/NEW1/g' file1.md file2.md
grep -n "NEW1" file1.md  # Verify new pattern exists
grep -n "OLD1" file1.md  # Verify old pattern gone (should be empty)

# Good: Pattern verified, move to group 2
sed -i 's/OLD2/NEW2/g' file3.md
grep -n "NEW2" file3.md
grep -n "OLD2" file3.md

# Continue...
```

**Benefits:**
- Catch errors immediately (not at the end)
- Easy to rollback (git reset last group)
- Build confidence incrementally
- Clear audit trail

---

## Prerequisites

### Before Starting Fix Application

**Verify you have:**

- [ ] Completed Stage 2 (Fix Planning)
- [ ] Fix plan with grouped issues
- [ ] Priority order defined (P0 → P1 → P2 → P3)
- [ ] Sed commands prepared for automated fixes
- [ ] Manual review cases identified
- [ ] Verification commands ready for each group
- [ ] Git working directory clean (can rollback if needed)

**If missing any:** Return to Stage 2 and complete planning fully.

### Git Safety Check

```bash
# Ensure clean state
git status

# Should show:
# On branch epic/KAI-X
# nothing to commit, working tree clean

# If changes exist, commit or stash first
git stash  # if you want to save changes
# OR
git reset --hard  # if you want to discard (DANGEROUS)
```

---

## The Incremental Approach

### The Fix-Verify Loop

```
FOR each fix group (in priority order):
  ↓
STEP 1: Apply fix to group
  ↓
STEP 2: Verify new pattern exists
  ↓
STEP 3: Verify old pattern gone
  ↓
STEP 4: Spot-read actual file contents
  ↓
STEP 5: Document before/after
  ↓
STEP 6: Move to next group
```

### Why This Order Matters

**Priority Order:**
```
P0 (Critical) → P1 (High) → P2 (Medium) → P3 (Low)
```

**Within Priority:**
```
Automated fixes → Manual fixes
```

**Rationale:**
- Critical issues fixed first (biggest impact)
- Automated first (faster, build momentum)
- Manual last (require thought, slower)

---

## Fix Execution Process

### Step-by-Step for Each Fix Group

#### STEP 1: Apply Fix

**For automated fixes (sed):**

```bash
# Group N: [Description]
echo "=== Applying Fix Group N: [Description] ==="

# Run sed command from fix plan
sed -i 's|OLD_PATTERN|NEW_PATTERN|g' file1.md file2.md file3.md

# Example:
sed -i 's|stages/s5/round1/|stages/s5/s5_p1_|g' stages/s5/*.md
```

**For manual fixes:**
```bash
# Use Edit tool with precise old_string → new_string
# Document each manual edit
```

#### STEP 2: Verify New Pattern Exists

```bash
echo "=== Verifying new pattern exists ==="

# Check new pattern appears in files
grep -n "NEW_PATTERN" file1.md file2.md file3.md

# Example output:
# file1.md:45:stages/s5/s5_p1_planning.md
# file2.md:67:stages/s5/s5_p1_i1_requirements.md
# file3.md:89:stages/s5/s5_p1_i2_algorithms.md

# Count matches (should equal expected count from fix plan)
grep -c "NEW_PATTERN" file1.md file2.md file3.md
```

**Red flags:**
- No matches found (sed didn't work)
- Too few matches (some instances missed)
- Wrong file shows matches (sed affected wrong files)

#### STEP 3: Verify Old Pattern Gone

```bash
echo "=== Verifying old pattern removed ==="

# Search for old pattern (should return ZERO)
grep -n "OLD_PATTERN" file1.md file2.md file3.md

# If returns results:
# - Check if intentional (historical examples, etc.)
# - Check if pattern needs refinement
# - Check if additional variations exist

# Example: Expected 0, found 5
# file1.md:123:old_pattern (in historical example)
# → Intentional, document as acceptable
```

**Expected result:** Zero matches OR only intentional cases

#### STEP 4: Spot-Read Actual File Contents

**CRITICAL:** Don't trust grep - read actual files

```bash
echo "=== Spot-reading actual changes ==="

# Pick 2-3 files, read changed lines in context
sed -n '40,50p' file1.md  # Lines around first change
sed -n '60,70p' file2.md  # Lines around second change

# Check:
# - Change looks correct in context
# - Formatting preserved
# - No unintended side effects
```

**What to look for:**
- Broken markdown formatting
- Partial matches (e.g., "S5a" → "S5.P1a" instead of "S5.P1")
- Context makes sense
- No accidental replacements

#### STEP 5: Document Before/After

**For each group, document:**

```markdown
## Fix Group N: [Description]

**Pattern:** OLD → NEW
**Files Modified:** N files
**Instances Fixed:** N instances

### Before
```bash
$ grep -n "OLD" file1.md
45:stages/s5/round1/planning.md
```

### After
```bash
$ grep -n "NEW" file1.md
45:stages/s5/s5_p1_planning_round1.md
```

### Verification
```bash
$ grep -n "OLD" file1.md
# No matches (or only intentional cases)
```

**Status:** ✅ Fixed and verified
**Issues:** None
```

#### STEP 6: Decision Point

**After verifying group:**

```
IF verification passed:
  └─> Continue to next group

IF verification failed:
  ├─> Rollback this group (git restore)
  ├─> Analyze why it failed
  ├─> Refine pattern
  └─> Retry
```

---

## Verification After Each Fix

### Three-Level Verification

**Level 1: Pattern Count**
```bash
# Quick check: Did number change as expected?
before=$(cat fix_plan.md | grep "Group N" | grep -o "[0-9]* instances")
after=$(grep -rc "NEW_PATTERN" affected_files | paste -sd+ | bc)

echo "Expected: $before"
echo "Found: $after"
```

**Level 2: File Content Grep**
```bash
# Medium check: Do files show correct pattern?
grep -n "NEW_PATTERN" file1.md file2.md
grep -n "OLD_PATTERN" file1.md file2.md  # Should be 0 or intentional
```

**Level 3: Visual Inspection**
```bash
# Deep check: Read actual content
sed -n 'LINE_NUMp' file.md  # Read specific lines
git diff file.md  # See exactly what changed
```

**All three must pass before moving to next group.**

### Rollback If Needed

```bash
# If verification fails, rollback this group
git restore file1.md file2.md file3.md

# Analyze why it failed
# - Wrong pattern?
# - Wrong files?
# - Need word boundaries?
# - Context-sensitive issue?

# Refine and retry
```

---

## Manual Fix Guidelines

### When Manual Fixing Required

**Cases requiring manual intervention:**

1. **Context-Sensitive Replacements**
   - Same pattern in error and intentional contexts
   - Requires reading context to determine

2. **Adding New Content**
   - Missing sections (can't sed something that doesn't exist)
   - Requires writing new content

3. **Complex Restructuring**
   - File splits
   - Section reorganization
   - Template structure changes

4. **User Decisions**
   - Multiple valid options
   - Trade-offs to consider

### Manual Fix Process

**For each manual fix:**

```markdown
## Manual Fix #N

**File:** path/to/file.md
**Issue:** [Description]
**Line:** 123 (approximate)

### Analysis
[Read context, understand issue]

### Decision
[Chosen approach with rationale]

### Action Taken
**Before:**
```
[Old content]
```

**After:**
```
[New content]
```

### Verification
- [ ] New content added correctly
- [ ] Formatting consistent with file
- [ ] No typos or errors
- [ ] Cross-references updated if needed
```

---

## Exit Criteria

### Stage 3 Complete When ALL These Are True

- [ ] All P0 (Critical) groups fixed and verified
- [ ] All P1 (High) groups fixed and verified
- [ ] All P2 (Medium) groups fixed and verified
- [ ] P3 (Low) groups fixed OR deferred (documented)
- [ ] Each group verified immediately after fix
- [ ] Before/after documented for each group
- [ ] Manual fixes completed and verified
- [ ] No verification failures remaining
- [ ] Git diff reviewed (sanity check all changes)
- [ ] Ready to proceed to Stage 4 (Comprehensive Verification)

**If ANY criterion incomplete:** Continue fixing until all complete.

### Final Git Diff Review

```bash
# Review ALL changes made
git diff

# Check:
# - All changes are intentional
# - No accidental modifications
# - Formatting preserved
# - No syntax errors introduced

# If satisfied, ready for Stage 4
# (Don't commit yet - wait until after Stage 4 verification)
```

---

## Common Pitfalls

### Pitfall 1: Batching All Fixes

**Symptom:** Run all 10 sed commands, verify at end

**Problem:** Can't isolate which fix caused issue if verification fails

**Solution:** Fix → Verify → Fix → Verify (incremental)

### Pitfall 2: Trusting Sed Without Reading Files

**Symptom:** "Sed returned exit 0, must be fine"

**Problem:** Sed can succeed but produce wrong output

**Solution:** Always read actual file contents after sed

### Pitfall 3: Skipping Verification

**Symptom:** "I know this pattern is correct, skip verification"

**Problem:** Assumptions wrong, errors propagate

**Solution:** Verify EVERY group, no exceptions

### Pitfall 4: Not Documenting Before/After

**Symptom:** "I fixed it, move on to next"

**Problem:** Can't remember what was changed if issue found later

**Solution:** Document every group with before/after evidence

### Pitfall 5: Fixing Wrong Priority Order

**Symptom:** Fix P3 issues before P0 issues

**Problem:** Waste time on low-priority while critical broken

**Solution:** Always fix P0 → P1 → P2 → P3

### Pitfall 6: No Rollback Plan

**Symptom:** "Fix broke something, how do I undo?"

**Problem:** No clean state to rollback to

**Solution:** Start with clean git state, rollback per group if needed

---

## Example Execution

### Real Example: Fixing Old Stage Notation

**From Fix Plan:**
```
Group 1: Old Notation S5a/S6a/S7a → S5/S6/S7
Pattern: \bS[5-9]a\b
Count: 60+ instances across 30+ files
Priority: P1 (High)
```

**Execution:**

```bash
# STEP 1: Apply fix
echo "=== Applying Group 1: Old Notation ==="
sed -i 's/\bS5a\b/S5/g; s/\bS6a\b/S6/g; s/\bS7a\b/S7/g; s/\bS8a\b/S8/g; s/\bS9a\b/S9/g' \
  stages/**/*.md templates/*.md reference/*.md

# STEP 2: Verify new patterns exist
echo "=== Verifying S5 appears (should be many) ==="
grep -rn "\bS5\b" stages/s5/*.md | wc -l
# Output: 150 (many references to S5, looks good)

# STEP 3: Verify old patterns gone
echo "=== Verifying S5a removed (should be 0) ==="
grep -rn "\bS5a\b" stages --include="*.md" | wc -l
# Output: 0 (perfect!)

# STEP 4: Spot-read actual changes
echo "=== Reading actual changed lines ==="
grep -n "\bS5\b" stages/s5/s5_bugfix_workflow.md | head -5
# 45:After completing S5 (Implementation Planning)
# 67:Proceed to S5 for bug fix
# Looks correct in context!

# STEP 5: Document
echo "Group 1: ✅ Fixed and verified - 60+ instances of old notation removed"

# STEP 6: Move to Group 2
echo "=== Ready for Group 2 ==="
```

---

## See Also

**Previous Stage:**
- `stage_2_fix_planning.md` - Fix plan that drives this stage

**Next Stage:**
- `stage_4_verification.md` - Comprehensive verification after all fixes applied

**Reference:**
- `../reference/verification_commands.md` - More verification examples
- `../templates/verification_report_template.md` - Document results for Stage 4

**Dimensions:**
- Read relevant dimension guides for context on fix types

---

**After completing Stage 3:** Proceed to `stages/stage_4_verification.md`
