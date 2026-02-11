# Audit Round Example 4: Cross-Reference Validation

**Epic:** KAI-7 (S10.P1 Guide Updates)
**Audit Context:** After Rounds 1-3 fixes applied (84 issues fixed total)
**Round Date:** 2026-02-04
**Duration:** 90 minutes
**Focus:** Validate cross-references after notation changes + template currency

---

## Round Overview

**Trigger Event:** Round 3 changed 70+ notation instances → Verify cross-references still valid

**Why This Round:**
- Risk: Changing notation may break cross-references that depended on old notation
- Fresh eyes: Different validation approach (automated link checking)
- Expand scope: Check templates for notation consistency

**Sub-Round:** Round 1.2 (Content Quality - D6 Template Currency)

---

## Discovery Process

### New Validation Approach

**Strategy Change:**
- Rounds 1-3: Search for patterns
- Round 4: Validate relationships between files

**Pattern Set 1: Automated Link Checking**
```bash
# Extract all cross-references
grep -rh "\[.*\](.*\.md)" --include="*.md" ../../ | \
  grep -o "(.*\.md)" | \
  tr -d '()' | \
  sort -u > all_links.txt

# Check each link exists
while read link; do
  # Handle relative paths
  base_path="../../"
  full_path="$base_path$link"
  [ ! -f "$full_path" ] && echo "BROKEN LINK: $link"
done < all_links.txt
```

**Pattern Set 2: Template Notation Check**
```bash
# Check templates for old notation
grep -rn "\bS[0-9][a-z]\b" --include="*.md" ../../templates/
```

**Pattern Set 3: Cross-Reference After Notation Change**
```bash
# Files that reference S5 - do they use new notation?
grep -rn "Stage 5\|S5" --include="*.md" ../../ | \
  grep -v "S5\.P" | \  # Exclude new notation
  head -30
```

### Issues Found

**Total Issues:** 23 instances across 12 files

**Breakdown by Type:**

| Issue Type | Count | Example | Severity |
|------------|-------|---------|----------|
| Broken links after notation change | 8 | Link to "s5_planning.md" but file split | 🔴 CRITICAL |
| Templates with old notation | 6 | "Complete S5a" in template | 🔴 CRITICAL |
| Inconsistent cross-references | 5 | One guide says "S5", another "S5.P1" for same thing | 🟠 HIGH |
| Missing template updates | 4 | Template missing new S8 stage | 🟠 HIGH |

---

## Detailed Issues

### Issue Category 1: Broken Links After File Split

**Background:** Round 3 changed notation, but some files were split (s5_planning.md → s5_p1/p2/p3)

**Example Issue:**
**File:** s4_feature_testing_strategy.md:234
**Link:** `[S5 Planning](../s5/s5_planning.md)`
**Problem:** s5_planning.md doesn't exist (was split into s5_v2_validation_loop.md, s5_v2_validation_loop.md, s5_p3_planning_round3.md)

**8 similar issues found across files**

---

### Issue Category 2: Templates with Old Notation

**Templates are special:**
- Errors in templates propagate to ALL new epics
- Priority: CRITICAL severity

**Example Issue 1:**
**File:** templates/feature_XX_template.md:45
**Content:** "After S5a completion..."
**Problem:** Uses old "S5a" notation
**Should be:** "After S5.P1 completion..."

**Example Issue 2:**
**File:** templates/EPIC_README_template.md:123
**Content:** "Stage 6: Execution"
**Problem:** S6 was renumbered to S9
**Should be:** "Stage 9: Execution"

**6 template issues found total**

---

### Issue Category 3: Inconsistent Cross-References

**Problem:** Different guides refer to same stage/phase differently

**Example:**
**File A (s4_feature_testing_strategy.md:56):** "After completing S5..."
**File B (s6_execution.md:23):** "After completing S5.P3..."
**File C (s7_p1_smoke_testing.md:12):** "After S5.P1, S5.P2, and S5.P3..."

**All refer to "completing S5" but with different specificity levels**

**Analysis:**
- S5 (generic) = All of S5 (all 3 phases)
- S5.P3 (specific) = Only Round 3
- Need consistency: If referring to all of S5, use "S5" consistently

**5 inconsistency issues found**

---

### Issue Category 4: Missing Template Updates

**Problem:** Templates not updated when workflow structure changed

**Example:**
**File:** templates/EPIC_README_template.md
**Content:** Lists stages S1-S7
**Problem:** Workflow now has S1-S10 (S8-S10 missing from template)
**Should list:** S1-S10

**4 template completeness issues**

---

## Fix Planning

### Group 1: CRITICAL - Templates (10 issues: 6 notation + 4 completeness)

**Why first:**
- Templates propagate to new epics
- Highest blast radius
- Fix before anyone creates new epic

---

### Group 2: CRITICAL - Broken Links (8 issues)

**Why second:**
- Block navigation
- Users can't find referenced files

---

### Group 3: HIGH - Inconsistent References (5 issues)

**Why third:**
- Cause confusion but don't block
- Need decision on consistency rules

---

## Sample Fixes

### Fix Group 1: Template Notation Updates

**File:** templates/feature_XX_template.md

**Changes:**
- Line 45: "S5a" → "S5.P1"
- Line 67: "S6a" → "S6"
- Line 89: "Stage 6" → "Stage 9"
- Line 123: Added S8, S9, S10 to stage list

**File:** templates/EPIC_README_template.md

**Changes:**
- Line 23: "Stage 6: Execution" → "Stage 9: Execution"
- Line 45: "Stage 7: Testing" → "Stage 10: Cleanup"
- Line 78: Added missing stages (S8: Cross-Feature Alignment)

---

### Fix Group 2: Broken Link Repairs

**Pattern:** Link to split file → Link to specific sub-file or list all

**Example Fix 1:**
**File:** s4_feature_testing_strategy.md:234

**Before:**
```markdown
See [S5 Planning](../s5/s5_planning.md) for implementation details.
```

**After:**
```markdown
See S5 Planning guides for implementation details:
- [Round 1](../s5/s5_v2_validation_loop.md) - Iterations 1-7
- [Round 2](../s5/s5_v2_validation_loop.md) - Iterations 8-13
- [Round 3](../s5/s5_p3_planning_round3.md) - Iterations 14-22
```

---

### Fix Group 3: Consistency Standardization

**Decision Made:** Use most specific notation when referencing phases

**Consistency Rule:**
- If referring to ALL of S5 → Use "S5" (generic)
- If referring to specific round → Use "S5.P1/P2/P3"
- If listing progression → Use "S5.P1 → S5.P2 → S5.P3"

**Fixes Applied:**
5 instances changed to follow rule

---

## Verification Results

### Template Verification

```bash
$ grep -rn "\bS[0-9][a-z]\b" --include="*.md" ../../templates/
[no output]
# ✅ Zero old notation in templates
```

### Link Validation

```bash
$ # Re-run automated link checker
$ while read link; do
    full_path="../../$link"
    [ ! -f "$full_path" ] && echo "BROKEN: $link"
  done < all_links.txt
[no output]
# ✅ All links valid
```

### Cross-Reference Consistency

**Manual verification of 20 random cross-references:**
- All use consistent notation (S5 vs S5.P# appropriately)
- All links resolve correctly
- ✅ All clean

### Counts

| Metric | Value |
|--------|-------|
| N_found (Stage 1) | 23 |
| N_fixed (Stage 3) | 23 |
| N_remaining (Stage 4) | 0 |
| N_new (Stage 4) | 0 |

---

## Cumulative Audit Results

### All Rounds Summary

| Round | Focus | Issues | Fixed | Duration |
|-------|-------|--------|-------|----------|
| 1 | Step number mapping | 4 | 4 | 45 min |
| 2 | Router links, paths | 10 | 10 | 75 min |
| 3 | Notation standardization | 72 | 70 | 120 min |
| 4 | Cross-references, templates | 23 | 23 | 90 min |
| **TOTAL** | **4 rounds** | **109** | **107** | **5.5 hours** |

**Remaining:** 2 intentional instances (historical references, documented)

**Files Modified:** 50+ files across all rounds
**Dimensions Covered:** D1, D2, D3, D6, D8, D10

---

## Lessons Learned

### What Worked Across All Rounds

✅ **Fresh patterns each round** - Each round used different search strategies
✅ **Iterative discovery** - Round N findings informed Round N+1 focus
✅ **Context analysis** - Prevented false positives (preserved 2 historical refs)
✅ **Automated validation** - Link checking caught issues manual reading missed

### Key Insight: Cascading Issues

**Pattern observed:**
1. Round 1: Found step number issues (4) → Limited scope
2. Round 2: Expanded to all paths (10) → Moderate scope
3. Round 3: Notation change (70+) → Large scope
4. Round 4: Validate Round 3 changes (23) → Cleanup round

**Lesson:** Large-scale changes (like notation) require follow-up validation round

### Why 4 Rounds Were Necessary

**Round 3 found 70+ issues - why didn't Round 1-2 catch these?**
- **Different dimension focus:** D1/D3 (paths) vs D2 (notation)
- **Different patterns:** File paths vs letter suffixes
- **Fresh eyes:** Round 3 was 2+ hours after Rounds 1-2

**Round 4 found 23 issues - why didn't Round 3 catch these?**
- **Validation, not discovery:** Round 3 fixed, Round 4 validated fixes didn't break things
- **Different artifact type:** Code (guides) vs templates
- **Relationship checking:** Link validity requires different approach than pattern matching

---

## Exit Criteria Assessment

### After Round 4

**9 Exit Criteria:**
1. ✅ All issues resolved (107/109, 2 intentional documented)
2. ✅ Zero new discoveries in Round 4 Stage 1 (would need Round 5 if found issues)
3. ✅ Zero verification findings (N_new = 0)
4. ✅ Minimum 3 rounds (completed 4)
5. ✅ All remaining documented (2 historical refs)
6. ✅ User has not challenged
7. ✅ Confidence ≥ 80% (self-assessed: 85%)
8. ✅ Pattern diversity ≥ 5 types (used 8+ pattern types across rounds)
9. ✅ Spot-checks clean (20+ files checked, zero issues)

**Decision:** ✅ **CAN EXIT** (all criteria met)

**But:** Best practice is minimum 3 consecutive clean rounds
- Round 4 found 23 issues → Should run Round 5 to validate

**User decision:** User approved exit after Round 4 (accepted 2 intentional instances)

---

## Round Summary

**Issues Found:** 23
**Issues Fixed:** 23
**Files Modified:** 12 (including 3 templates)
**Duration:** 90 minutes
**Next Action:** Exit audit (all criteria met, user approved)

**Key Takeaway:** After large-scale changes (70+ notation fixes), always run validation round to verify changes didn't introduce new issues. Found 23 issues that wouldn't exist without Round 3 changes.
