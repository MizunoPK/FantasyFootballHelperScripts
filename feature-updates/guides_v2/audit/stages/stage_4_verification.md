# Stage 4: Verification

**Purpose:** Comprehensively verify all fixes applied correctly with zero new issues introduced
**Duration:** 30-45 minutes
**Input:** Fixed files from Stage 3
**Output:** Verification report with counts (N_found, N_fixed, N_remaining, N_new)
**Reading Time:** 10-15 minutes

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Verification Strategy](#verification-strategy)
4. [Re-Running Discovery Patterns](#re-running-discovery-patterns)
5. [Trying New Pattern Variations](#trying-new-pattern-variations)
6. [Spot-Check Random Files](#spot-check-random-files)
7. [Calculating Counts](#calculating-counts)
8. [Exit Criteria](#exit-criteria)
9. [If New Issues Found](#if-new-issues-found)

---

## Overview

### Purpose

**Stage 4: Verification** ensures fixes were applied correctly and no new issues were introduced.

**Key Principle:** Don't trust that fixes worked - **PROVE** they worked.

### What Gets Verified

**Three verification levels:**

1. **Re-Run Original Patterns** - Issues from Stage 1 should be gone
2. **Try New Pattern Variations** - Catch variations missed in Stage 1
3. **Spot-Check Random Files** - Visual inspection catches grep misses

**Success Criteria:**
- N_remaining = 0 OR only intentional cases
- N_new = 0 (no new issues introduced)
- Random spot-checks clean

---

## Prerequisites

### Before Starting Verification

**Verify you have:**

- [ ] Completed Stage 3 (Apply Fixes)
- [ ] All fix groups applied and verified incrementally
- [ ] Before/after documentation for each group
- [ ] Git diff reviewed
- [ ] Discovery report from Stage 1 (to re-run patterns)
- [ ] Fix plan from Stage 2 (to verify all groups completed)

**If missing any:** Return to Stage 3 and complete fixes fully.

---

## Verification Strategy

### The Three-Tier Approach

```
Tier 1: RE-RUN Discovery Patterns
  ↓
  Should find ZERO (or only intentional)
  ↓
Tier 2: TRY New Pattern Variations
  ↓
  Brainstorm variations not tried in Stage 1
  ↓
Tier 3: SPOT-CHECK Random Files
  ↓
  Manual reading catches what grep misses
  ↓
SUCCESS: Zero new issues, all original issues fixed
```

---

## Re-Running Discovery Patterns

### STEP 1: Load Original Patterns

**From Stage 1 discovery report:**

```bash
# Extract all patterns used in Stage 1
grep "Pattern:" DISCOVERY_REPORT_ROUND_N.md

# Example patterns from Round 1:
# - grep -rn "\bS5a\b" --include="*.md"
# - grep -rn "stages/s5/round1/" --include="*.md"
# - grep -rn "5a:" --include="*.md"
```

### STEP 2: Re-Run Each Pattern

**For each pattern from Stage 1:**

```bash
echo "=== Re-running Pattern 1: S5a notation ==="
grep -rn "\bS5a\b" --include="*.md" | wc -l

# Expected: 0 (or only intentional cases documented in Stage 3)
# Actual: [count]

# If 0: ✅ Pattern verified clean
# If > 0: Analyze each match
```

### STEP 3: Analyze Remaining Matches

**For each remaining match:**

```bash
# Get context
grep -rn -A2 -B2 "\bS5a\b" file.md

# Determine:
# - Is this intentional? (historical example, quote, etc.)
# - Was this missed in Stage 3?
# - Is this a new variation?

# If intentional: Document in verification report
# If missed: Add to fix list, loop back to Stage 3
# If new variation: Add to new patterns list
```

---

## Trying New Pattern Variations

### Why New Patterns Matter

**Issue:** Stage 1 used Pattern A, fixed all instances, but Pattern B exists

**Example:**
```
Stage 1 pattern: "5a" (space before/after)
Missed variation: "5a:" (colon after)
Missed variation: "(5a)" (in parentheses)
```

**Solution:** Brainstorm variations not tried in Stage 1

### STEP 1: Brainstorm Variations

**Ask yourself:**
- What punctuation might follow the pattern?
- What punctuation might precede it?
- What context might surround it?
- What case variations exist?

**Example for "5a" pattern:**
```bash
# Original patterns (from Stage 1)
grep -rn "\b5a\b"

# NEW variations to try
grep -rn "5a:" --include="*.md"        # colon after
grep -rn "5a-" --include="*.md"        # dash after
grep -rn "5a\." --include="*.md"       # period after
grep -rn "5a," --include="*.md"        # comma after
grep -rn "\(5a\)" --include="*.md"     # in parentheses
grep -rn "back to 5a" --include="*.md" # in sentence
```

### STEP 2: Run Each New Pattern

```bash
echo "=== Trying NEW Pattern Variations ==="

# Pattern 1: Colon after
grep -rn "5a:" --include="*.md"
# Result: 0 matches → ✅ Clean

# Pattern 2: Dash after
grep -rn "5a-" --include="*.md"
# Result: 3 matches → ⚠️ Analyze

# Pattern 3: Period after
grep -rn "5a\." --include="*.md"
# Result: 0 matches → ✅ Clean
```

### STEP 3: Track New Discoveries

```bash
# If new patterns find issues:
N_new = [count of issues found in verification not in original discovery]

# These indicate:
# - Stage 1 discovery was incomplete
# - Pattern variations were missed
# - Round N+1 needed with better patterns
```

---

## Spot-Check Random Files

### Why Visual Inspection Matters

**What grep misses:**
- Context issues (technically correct pattern, wrong context)
- Formatting broken by sed
- Partial matches (e.g., "S5.P1a" instead of "S5.P1")
- File-level issues (structure, completeness)

### STEP 1: Random File Selection

```bash
echo "=== Random Spot-Check ==="

# Select 10+ random files
find stages templates reference -name "*.md" -type f | shuf -n 10

# Example output:
# stages/s5/s5_p2_planning_round2.md
# stages/s9/s9_p3_user_testing.md
# templates/feature_spec_template.md
# reference/mandatory_gates.md
# ...
```

### STEP 2: Manual Reading

**For each random file:**

```bash
# Read different sections
file="stages/s5/s5_p2_planning_round2.md"

# Beginning
sed -n '1,50p' "$file"

# Middle
line_count=$(wc -l < "$file")
mid=$((line_count / 2))
sed -n "${mid},$((mid+50))p" "$file"

# End
tail -n 50 "$file"
```

**What to look for:**
- [ ] Patterns look correct in context
- [ ] No broken markdown formatting
- [ ] Headers are properly leveled
- [ ] Cross-references make sense
- [ ] No obvious typos or errors
- [ ] Consistent terminology within file
- [ ] Code blocks properly formatted
- [ ] Lists and checklists consistent

### STEP 3: Document Spot-Check Results

```markdown
## Spot-Check Results

**Files Checked:** 10 files

### File 1: stages/s5/s5_p2_planning_round2.md
**Sections:** Lines 1-50, 200-250, end
**Issues:** None
**Notes:** Notation consistent, formatting good

### File 2: templates/feature_spec_template.md
**Sections:** Full file (250 lines)
**Issues:** 1 - Old stage reference on line 67
**Notes:** "Stage 5a" should be "S5.P1"

[Continue for all spot-checked files]
```

---

## Calculating Counts

### The Four Critical Counts

**Track these numbers:**

```markdown
## Verification Counts

**N_found:** [Number of issues found in Stage 1 Discovery]
- Example: 60 instances of old notation

**N_fixed:** [Number of issues fixed in Stage 3]
- Example: 60 instances replaced in Stage 3

**N_remaining:** [Number of instances still found after fixes]
- Example: 5 instances still found (all intentional)

**N_new:** [Number of NEW issues found in Stage 4 Verification]
- Example: 3 issues found during spot-checks not in original discovery
```

### Expected Outcomes

**Perfect verification:**
```
N_found = 60
N_fixed = 60
N_remaining = 0
N_new = 0
→ ✅ Complete success
```

**Good verification (with intentional cases):**
```
N_found = 60
N_fixed = 55
N_remaining = 5 (all documented as intentional)
N_new = 0
→ ✅ Success with acceptable exceptions
```

**Failed verification (new issues found):**
```
N_found = 60
N_fixed = 60
N_remaining = 0
N_new = 8 (found during new pattern variations)
→ ❌ MUST loop back - discovery was incomplete
```

**Failed verification (issues not fixed):**
```
N_found = 60
N_fixed = 45
N_remaining = 15 (errors, not intentional)
N_new = 0
→ ❌ MUST loop back - fixes incomplete
```

---

## Exit Criteria

### Stage 4 Complete When ALL These Are True

- [ ] All Stage 1 patterns re-run
- [ ] N_remaining = 0 OR only intentional (documented)
- [ ] Tried at least 5 new pattern variations
- [ ] N_new = 0 (no new issues discovered)
- [ ] Spot-checked 10+ random files
- [ ] Spot-checks found zero issues OR issues added to fix list
- [ ] All counts calculated (N_found, N_fixed, N_remaining, N_new)
- [ ] Verification report created
- [ ] Ready to proceed to Stage 5 (Loop Decision)

**If ANY criterion fails:** Address issues and re-verify.

### Critical Decision Point

```
IF N_new > 0:
  └─> ❌ LOOP BACK to Round N+1 Stage 1
      - Discovery was incomplete
      - New patterns needed
      - Cannot proceed to Stage 5

IF N_remaining > 0 AND not all intentional:
  └─> ❌ LOOP BACK to Stage 3
      - Fixes incomplete
      - Apply missing fixes
      - Re-run Stage 4

IF N_new = 0 AND N_remaining acceptable:
  └─> ✅ PROCEED to Stage 5
      - Verification passed
      - Ready for loop decision
```

---

## If New Issues Found

### When N_new > 0

**This means:** Stage 1 Discovery was incomplete

**Required Action:**

```
1. STOP - Do not proceed to Stage 5
   ↓
2. Document all new issues found
   ↓
3. Analyze why they were missed
   - Wrong patterns used?
   - Wrong folders searched?
   - Insufficient pattern variations?
   ↓
4. LOOP BACK to Round N+1 Stage 1
   - Use fresh patterns
   - Include variations that found N_new
   - More comprehensive search
   ↓
5. Complete full loop again
   - Stage 1: Discovery (with better patterns)
   - Stage 2: Fix Planning
   - Stage 3: Apply Fixes
   - Stage 4: Verification
   - Stage 5: Loop Decision
```

**Example:**

```markdown
## New Issues Found (N_new = 8)

**Analysis:**
Stage 1 used pattern "\bS5a\b" which missed:
- "S5a:" (with colon) - 3 instances
- "(S5a)" (in parentheses) - 2 instances
- "back to S5a" (in sentence) - 3 instances

**Why Missed:**
- Pattern variations not tried
- Context-based patterns not used
- Assumed word-boundary was sufficient

**Next Round Patterns:**
1. "\bS5a\b" (original)
2. "S5a:" (with colon)
3. "S5a[-,.]" (with punctuation)
4. "(S5a)" (in parentheses)
5. "to S5a\|from S5a\|back to S5a" (in context)

**Action:** LOOP BACK to Round N+1 with enhanced patterns
```

---

## Verification Report Example

```markdown
# Verification Report - Round N

**Date:** 2026-02-01
**Round:** 3
**Duration:** 35 minutes

---

## Verification Summary

**N_found:** 70 (issues from Stage 1)
**N_fixed:** 70 (issues fixed in Stage 3)
**N_remaining:** 0
**N_new:** 0 (no new issues discovered)

**Status:** ✅ VERIFICATION PASSED

---

## Tier 1: Re-Run Original Patterns

### Pattern 1: Old notation "\bS5a\b"
```bash
$ grep -rn "\bS5a\b" --include="*.md"
# Result: 0 matches
```
**Status:** ✅ Clean

### Pattern 2: Old paths "stages/s5/round1/"
```bash
$ grep -rn "stages/s5/round1/" --include="*.md"
# Result: 0 matches
```
**Status:** ✅ Clean

[Continue for all Stage 1 patterns]

---

## Tier 2: New Pattern Variations

Tried 5 new patterns not used in Stage 1:

### New Pattern 1: "S5a:" (with colon)
```bash
$ grep -rn "S5a:" --include="*.md"
# Result: 0 matches
```
**Status:** ✅ Clean

### New Pattern 2: "S5a-" (with dash)
```bash
$ grep -rn "S5a-" --include="*.md"
# Result: 0 matches
```
**Status:** ✅ Clean

[Continue for all new patterns]

**New Issues Found:** 0

---

## Tier 3: Spot-Check Results

**Files Checked:** 12 files (random selection)

All spot-checks CLEAN:
- stages/s5/s5_p1_planning_round1.md ✅
- stages/s9/s9_p3_user_testing.md ✅
- templates/feature_spec_template.md ✅
- reference/mandatory_gates.md ✅
[List all 12 files]

**Issues Found in Spot-Checks:** 0

---

## Final Counts

- **N_found:** 70
- **N_fixed:** 70
- **N_remaining:** 0
- **N_new:** 0

---

## Decision

**Verification PASSED** - Ready for Stage 5 (Loop Decision)

**Confidence:** High (100%)
- All original patterns clean
- 5 new pattern variations tried
- 12 random files spot-checked
- Zero new issues discovered

**Next Step:** Proceed to Stage 5
```

---

## See Also

**Previous Stage:**
- `stage_3_apply_fixes.md` - Applied fixes that are now verified

**Next Stage:**
- `stage_5_loop_decision.md` - Decide whether to exit or continue to next round

**Templates:**
- `../templates/verification_report_template.md` - Use this for output

**Reference:**
- `../reference/verification_commands.md` - Additional verification commands

---

**After completing Stage 4:** Proceed to `stages/stage_5_loop_decision.md`
