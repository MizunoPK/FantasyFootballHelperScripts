# Audit Round Example 2: Router Links and Path Formats

**Epic:** KAI-7 (S10.P1 Guide Updates)
**Audit Context:** After Round 1 fixes applied
**Round Date:** 2026-02-04
**Duration:** 75 minutes
**Focus:** Router links, path formats, and file location references

---

## Round Overview

**Trigger Event:** Round 1 complete (4 issues fixed), continuing with fresh patterns

**Why This Round:**
- Round 1 found step number issues → Check for related path format issues
- Fresh eyes approach: Use DIFFERENT patterns than Round 1
- Expand scope from root files to all guide files

**Sub-Round:** Round 1.1 continuation (Core Dimensions - D1 Cross-Reference Accuracy)

---

## Discovery Process

### New Patterns (Not Used in Round 1)

**Pattern 1: All .md File Paths**
```bash
# Extract ALL file path references
grep -rh "stages/.*\.md\|templates/.*\.md\|reference/.*\.md" \
  --include="*.md" ../../ | \
  grep -o "[a-z_/]*\.md" | \
  sort -u > all_paths.txt

# Check which don't exist
while read path; do
  [ ! -f "../../$path" ] && echo "BROKEN: $path"
done < all_paths.txt
```

**Pattern 2: Specific Directory Patterns**
```bash
# Check stages/ references in detail
grep -rn "stages/s[0-9]" --include="*.md" ../../ | head -50

# Check templates/ references
grep -rn "templates/" --include="*.md" ../../ | head -50

# Check reference/ references
grep -rn "reference/" --include="*.md" ../../ | head -50
```

**Pattern 3: Relative Path Validation**
```bash
# Find ../ relative paths
grep -rn "\.\./.*\.md" --include="*.md" ../../ | head -50
```

### Issues Found

**Total Issues:** 10 instances

| Issue # | File | Line | Problem | Severity |
|---------|------|------|---------|----------|
| 1 | s1_epic_planning.md | 340 | Links to "templates/epic_readme_template.md" but file is "EPIC_README_template.md" (case) | 🔴 CRITICAL |
| 2 | s2_feature_deep_dive.md | 125 | References "stages/s2/validation/" directory that doesn't exist | 🟠 HIGH |
| 3 | s3_epic_planning_approval.md | 89 | Path "reference/common_mistakes.md" correct but relative path wrong | 🟡 MEDIUM |
| 4 | s5_p1_planning.md | 412 | References "templates/implementation_plan_v2.md" (old version) | 🔴 CRITICAL |
| 5 | prompts_reference_v2.md | 234 | Links to "stages/s5/s5_planning.md" but file split into multiple | 🔴 CRITICAL |
| 6 | EPIC_WORKFLOW_USAGE.md | 567 | References "parallel_work/coordinator_guide.md" with wrong path | 🟠 HIGH |
| 7-10 | Multiple guides | Various | 4 instances of "stages/s6/" that should be "stages/s9/" | 🔴 CRITICAL |

---

## Context Analysis

### Issue #1: Template Filename Case Mismatch

**Pattern Found:** "templates/epic_readme_template.md"

**Context:**
```markdown
## Step 5.4: Create Epic Folder Structure

Use the template:
- `templates/epic_readme_template.md` → `feature-updates/KAI-{N}-{epic}/EPIC_README.md`
```

**Analysis:**
- Guide references "epic_readme_template.md" (lowercase)
- Actual file: "EPIC_README_template.md" (uppercase "EPIC_README")
- File system is case-sensitive on Linux
- This would break on case-sensitive systems

**Decision:** ERROR (broken reference on case-sensitive systems)

---

### Issue #2: Non-Existent Directory Reference

**Pattern Found:** "stages/s2/validation/"

**Context:**
```markdown
For validation protocols, see the validation directory:
- `stages/s2/validation/` - Contains validation checklists and procedures
```

**Analysis:**
- Guide claims validation/ subdirectory exists under stages/s2/
- Checked: No such directory
- Validation content is embedded in s2_p1_spec_creation_refinement.md
- Directory existed in old structure, was consolidated

**Decision:** ERROR (outdated directory reference)

---

### Issues #7-10: Old Stage Number References

**Pattern Found:** "stages/s6/" (4 instances across multiple files)

**Files Affected:**
1. s7_p1_smoke_testing.md: "stages/s6/execution" (line 145)
2. s8_p1_cross_feature_alignment.md: "stages/s6/s6_execution.md" (line 89)
3. EPIC_WORKFLOW_USAGE.md: "see stages/s6/ for..." (line 423)
4. README.md: "Stage 6 (S6): Execution" (line 234)

**Analysis:**
- S6 → S9 renumbering occurred during workflow restructuring
- References to stages/s6/ are now invalid
- Correct path: stages/s9/
- These are in current workflow content (not historical)

**Decision:** ERROR (all 4 instances need updating)

---

## Fix Planning

### Group 1: Critical Path Fixes (6 issues: #1, #4, #5, #7-10)

**Priority:** CRITICAL - These break file references

**Fixes:**
1. "epic_readme_template.md" → "EPIC_README_template.md"
2. "implementation_plan_v2.md" → "implementation_plan_template.md" (current version)
3. "s5_planning.md" → List all split files (s5_p1, s5_p2, s5_p3)
4-7. All "stages/s6/" → "stages/s9/"

---

### Group 2: High Priority (2 issues: #2, #6)

**Priority:** HIGH - Cause confusion but have workarounds

**Fixes:**
1. Remove directory reference, point to specific file instead
2. Fix parallel_work path

---

### Group 3: Medium Priority (1 issue: #3)

**Priority:** MEDIUM - Relative path works but inconsistent

**Fix:**
1. Standardize relative path format

---

## Fixes Applied

### Fix 1: Template Case Correction

**Before:**
```markdown
- `templates/epic_readme_template.md` → `feature-updates/KAI-{N}-{epic}/EPIC_README.md`
```

**After:**
```markdown
- `templates/EPIC_README_template.md` → `feature-updates/KAI-{N}-{epic}/EPIC_README.md`
```

**File:** s1_epic_planning.md:340

---

### Fix 2: Remove Non-Existent Directory Reference

**Before:**
```markdown
For validation protocols, see the validation directory:
- `stages/s2/validation/` - Contains validation checklists and procedures
```

**After:**
```markdown
For validation protocols, see:
- `stages/s2/s2_p1_spec_creation_refinement.md` - Section: Validation Loop
```

**File:** s2_feature_deep_dive.md:125

---

### Fix 3: S6 → S9 Path Updates (4 instances)

**Instance 1:**
**Before:** "stages/s6/execution"
**After:** "stages/s9/execution"
**File:** s7_p1_smoke_testing.md:145

**Instance 2:**
**Before:** "stages/s6/s6_execution.md"
**After:** "stages/s9/s9_execution.md"
**File:** s8_p1_cross_feature_alignment.md:89

**Instance 3:**
**Before:** "see stages/s6/ for..."
**After:** "see stages/s9/ for..."
**File:** EPIC_WORKFLOW_USAGE.md:423

**Instance 4:**
**Before:** "Stage 6 (S6): Execution"
**After:** "Stage 9 (S9): Execution"
**File:** README.md:234

---

### Fix 4: Template Version Update

**Before:**
```markdown
Use template: `templates/implementation_plan_v2.md`
```

**After:**
```markdown
Use template: `templates/implementation_plan_template.md`
```

**File:** s5_p1_planning.md:412

---

### Fix 5: Split File Reference

**Before:**
```markdown
For S5 planning details, see: `stages/s5/s5_planning.md`
```

**After:**
```markdown
For S5 planning details, see:
- `stages/s5/s5_v2_validation_loop.md` - Round 1 (Iterations 1-7)
- `stages/s5/s5_v2_validation_loop.md` - Round 2 (Iterations 8-13)
- `stages/s5/s5_v2_validation_loop.md` - Round 3 (Iterations 14-22)
```

**File:** prompts_reference_v2.md:234

---

### Fix 6: Parallel Work Path

**Before:**
```markdown
See: `parallel_work/coordinator_guide.md`
```

**After:**
```markdown
See: `parallel_work/s2_primary_agent_guide.md` - Coordinator workflow
```

**File:** EPIC_WORKFLOW_USAGE.md:567

---

### Fix 7: Relative Path Standardization

**Before:**
```markdown
See: `../../reference/common_mistakes.md`
```

**After:**
```markdown
See: `reference/common_mistakes.md` (from guides_v2 root)
```

**File:** s3_epic_planning_approval.md:89

---

## Verification Results

### Re-Run Discovery Patterns

**Pattern 1: Template References**
```bash
$ grep -rn "epic_readme_template\.md" --include="*.md" ../../
[no output - lowercase version no longer referenced]

$ grep -rn "EPIC_README_template\.md" --include="*.md" ../../
s1_epic_planning.md:340: - `templates/EPIC_README_template.md`
# ✅ Correct case now used
```

**Pattern 2: S6 References**
```bash
$ grep -rn "stages/s6/" --include="*.md" ../../
[no output]
# ✅ Zero instances (all updated to S9)

$ grep -rn "stages/s9/" --include="*.md" ../../
s7_p1_smoke_testing.md:145: ...stages/s9/execution...
s8_p1_cross_feature_alignment.md:89: ...stages/s9/s9_execution.md...
# ✅ Updated references present
```

**Pattern 3: Non-Existent Paths**
```bash
$ grep -rh "stages/.*\.md\|templates/.*\.md" --include="*.md" ../../ | \
    grep -o "[a-z_/]*\.md" | \
    sort -u | \
    while read path; do [ ! -f "../../$path" ] && echo "BROKEN: $path"; done

[no output]
# ✅ All referenced files exist
```

### Counts

| Metric | Value |
|--------|-------|
| N_found (Stage 1) | 10 |
| N_fixed (Stage 3) | 10 |
| N_remaining (Stage 4) | 0 |
| N_new (Stage 4) | 0 |

---

## Spot-Check Results

**Random files checked:** 12 files

- ✅ s1_epic_planning.md - Template reference correct
- ✅ s2_feature_deep_dive.md - No validation/ directory reference
- ✅ s7_p1_smoke_testing.md - Uses s9/ not s6/
- ✅ s8_p1_cross_feature_alignment.md - Uses s9/ not s6/
- ✅ EPIC_WORKFLOW_USAGE.md - All stage references correct
- ✅ README.md - Stage numbers correct (S9 not S6)
- ✅ prompts_reference_v2.md - S5 split files listed
- ✅ s5_p1_planning.md - Template version correct
- ✅ s3_epic_planning_approval.md - Relative path clarified
- ✅ templates/ directory - Files exist as referenced
- ✅ stages/s9/ directory - Files exist as referenced
- ✅ parallel_work/ directory - Files exist as referenced

**All spot-checks clean** ✅

---

## Lessons Learned

### What Worked

✅ **Expanded pattern scope** - Used file path extraction, not just specific searches
✅ **Directory validation** - Checked that referenced directories/files actually exist
✅ **Fresh patterns** - Round 2 used completely different search strategies than Round 1
✅ **Spot-checks** - Random file verification caught no new issues (good sign)

### What Was Missed (Found in Later Rounds)

❌ **Notation issues** - Focused on paths, didn't check for "S6a" old notation (found in Round 3)
❌ **Count accuracy** - Didn't verify claimed file counts (e.g., "10 stages") - would find in Round 3
❌ **Template content** - Checked template references but not template internal content

### For Next Round

**Different focus:**
- Round 1: Step numbers
- Round 2: File paths
- Round 3: Notation consistency (S#a → S#.P#)

**Pattern ideas for Round 3:**
- Search for old notation: "S5a", "S6a", "S7a", etc.
- Search for notation variations: "S5a:", "back to S5a", "(S5a)"
- Check count claims: "10 stages", "7 stages", "16 dimensions"

---

## Round Summary

**Issues Found:** 10
**Issues Fixed:** 10
**Files Modified:** 8
- s1_epic_planning.md
- s2_feature_deep_dive.md
- s3_epic_planning_approval.md
- s5_p1_planning.md
- s7_p1_smoke_testing.md
- s8_p1_cross_feature_alignment.md
- EPIC_WORKFLOW_USAGE.md
- README.md

**Duration:** 75 minutes
**Next Action:** Round 3 (notation standardization focus)

**Key Takeaway:** Automated path extraction and existence verification is highly effective. Found 10 broken references that manual reading would likely miss.
