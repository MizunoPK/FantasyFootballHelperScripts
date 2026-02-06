# Audit Round Example 3: Notation Standardization

**Epic:** KAI-7 (S10.P1 Guide Updates)
**Audit Context:** After Rounds 1-2 fixes applied (14 issues fixed total)
**Round Date:** 2026-02-04
**Duration:** 120 minutes
**Focus:** Old notation to new notation standardization (S#a → S#.P#)

---

## Round Overview

**Trigger Event:** Rounds 1-2 focused on step numbers and file paths → Fresh eyes for notation

**Why This Round:**
- Different dimension focus: D2 (Terminology Consistency) vs D1 (Cross-References)
- Known risk area: Notation changes typically leave stragglers
- Fresh pattern approach: Search for actual old notation patterns

**Sub-Round:** Round 1.1 completion (Core Dimensions - D2 Terminology Consistency)

---

## Discovery Process

### Notation Patterns Used

**Pattern Set 1: Basic Old Notation**
```bash
# Old letter suffix notation (S5a, S6a, etc.)
grep -rn "\bS[0-9][a-z]\b" --include="*.md" ../../

# Old "Stage Xa" format
grep -rn "Stage [0-9][a-z]" --include="*.md" ../../

# Bare number+letter (5a, 6b)
grep -rn "\b[0-9][a-z]\b" --include="*.md" ../../ | grep -v "2026\|2025"
```

**Pattern Set 2: Notation with Punctuation**
```bash
# Colon after old notation
grep -rn "S[0-9][a-z]:" --include="*.md" ../../

# Dash/hyphen
grep -rn "S[0-9][a-z]-" --include="*.md" ../../

# Parentheses
grep -rn "(S[0-9][a-z])" --include="*.md" ../../
```

**Pattern Set 3: All Caps Variants**
```bash
# STAGE_5a format
grep -rn "STAGE_[0-9][a-z]" --include="*.md" ../../
```

### Issues Found

**Total Issues:** 70+ instances across 30+ files

**Breakdown by Pattern:**

| Pattern Type | Count | Example | Files Affected |
|--------------|-------|---------|----------------|
| S#a notation | 60 | "S5a", "S6a", "S7a", "S8a", "S9a" | 25 files |
| Stage #a format | 5 | "Stage 5a", "Stage 6a" | 3 files |
| With punctuation | 4 | "S5a:", "back to S5a" | 2 files |
| STAGE_#a format | 1 | "STAGE_5a" | 1 file |
| Wrong header | 1 | "STAGE 7" in S10 file | 1 file |

**Files with Most Issues:**
1. s5_update_notes.md - 12 instances
2. s8_p2_epic_testing_update.md - 8 instances
3. s7_p2_qc_rounds.md - 6 instances
4. prompts_reference_v2.md - 5 instances
5. EPIC_WORKFLOW_USAGE.md - 5 instances

---

## Sample Issues & Context Analysis

### Group 1: S5a → S5 Conversion (25 instances)

**Old Notation:** "S5a" (meaning first phase/round of Stage 5)
**New Notation:** "S5" (stage-level reference) OR "S5.P1" (if phase-specific)

**Context Example 1 - Current Content:**
```markdown
## Workflow Overview

After completing S5a iterations, proceed to S5b alignment...
```

**Analysis:** This is NOT historical, it's current workflow
**Decision:** ERROR - Replace with "S5.P1" and "S5.P2"

**Context Example 2 - Historical Reference:**
```markdown
## Historical Note

The old workflow (pre-2025) used S5a/S5b notation for planning rounds.
```

**Analysis:** Explicitly marked as historical
**Decision:** INTENTIONAL - Keep (has proper context marker)

**Result of Analysis:**
- 25 instances total found
- 23 were in current content → Fix to S5.P# notation
- 2 were in historical sections with markers → Document as intentional

---

### Group 2: S6a, S7a, S8a, S9a → S6-S9 Conversion (30 instances)

**These old stage notations map to:**
- S6a → S6 (old Stage 6 kept numbering)
- S7a → S7 (old Stage 7 kept numbering)
- S8a → S8 (was added post-renumbering)
- S9a → S9 (was old S6, got renumbered)

**All 30 instances were in current content, none historical**

---

### Group 3: STAGE_Xx Format (1 instance)

**File:** s8_p2_epic_testing_update.md
**Line:** 45
**Content:** "STAGE_5a test strategy"

**Context:**
```markdown
## Prerequisites

Before starting epic testing, ensure:
- STAGE_5a test strategy complete
```

**Analysis:**
- All-caps format is non-standard
- "5a" is old notation
- Should be "S5.P1" or just "S5"

**Decision:** ERROR - Replace with "S5"

---

### Group 4: Wrong Stage Header (1 instance)

**File:** s10_epic_cleanup.md
**Line:** 234

**Context:**
```markdown
## CRITICAL RULES FOR STAGE 7

These rules apply to epic cleanup...
```

**Analysis:**
- This file IS s10_epic_cleanup.md (Stage 10)
- Header says "STAGE 7"
- Content is about S10 cleanup, not S7
- Likely copy-pasted from old S7 guide

**Decision:** ERROR - Replace with "STAGE 10"

---

## Fix Planning

### Mapping Rules

**S5 notation conversions:**
- "S5a" → "S5.P1" (if referring to Round 1 specifically)
- "S5a" → "S5" (if referring to stage generally)
- "S5b" → "S5.P2" (Round 2)
- "S5c" → "S5.P3" (Round 3)

**Other stage conversions:**
- "S6a", "S7a", "S8a" → "S6", "S7", "S8" (just remove letter)
- "S9a" → "S9" (was renumbered from old S6)

**Format conversions:**
- "Stage 5a" → "S5.P1" or "S5"
- "STAGE_5a" → "S5.P1" or "S5"
- "S5a:" → "S5.P1:" (keep punctuation)

---

## Automated Fix Strategy

### Sed Commands Used

```bash
# Group 1: Basic notation fixes (careful to preserve intentional cases)
# Manual review required for each, but these patterns guided fixes:

# S5a/b/c (checked context first)
find ../../ -name "*.md" -type f -exec sed -i 's/\bS5a\b/S5.P1/g' {} \;
find ../../ -name "*.md" -type f -exec sed -i 's/\bS5b\b/S5.P2/g' {} \;
find ../../ -name "*.md" -type f -exec sed -i 's/\bS5c\b/S5.P3/g' {} \;

# S6a, S7a, S8a, S9a (remove letter)
find ../../ -name "*.md" -type f -exec sed -i 's/\bS6a\b/S6/g' {} \;
find ../../ -name "*.md" -type f -exec sed -i 's/\bS7a\b/S7/g' {} \;
find ../../ -name "*.md" -type f -exec sed -i 's/\bS8a\b/S8/g' {} \;
find ../../ -name "*.md" -type f -exec sed -i 's/\bS9a\b/S9/g' {} \;

# Note: Historical sections were manually excluded before running these
```

---

## Sample Fixes

### Fix Set 1: s5_update_notes.md (12 instances)

**All instances were straightforward S5a/S5b/S5c conversions:**
- Line 23: "S5a iterations" → "S5.P1 iterations"
- Line 45: "After S5a" → "After S5.P1"
- Line 67: "S5b alignment" → "S5.P2 alignment"
- Line 89: "S5c final review" → "S5.P3 final review"
- [... 8 more similar]

---

### Fix Set 2: s8_p2_epic_testing_update.md (8 instances)

**Mixed notation types:**
- Line 12: "S5a" → "S5.P1"
- Line 34: "S6a" → "S6"
- Line 45: "STAGE_5a" → "S5" (special case)
- Line 56: "S7a" → "S7"
- [... 4 more]

---

### Fix Set 3: Header Correction

**File:** s10_epic_cleanup.md:234

**Before:**
```markdown
## CRITICAL RULES FOR STAGE 7
```

**After:**
```markdown
## CRITICAL RULES FOR STAGE 10
```

---

## Verification Results

### Pattern Re-Run

**Old notation remaining:**
```bash
$ grep -rn "\bS[0-9][a-z]\b" --include="*.md" ../../
../../stages/s1/s1_p3_discovery_phase.md:123: Historical Note: The old S5a notation...
../../EPIC_WORKFLOW_USAGE.md:456: Before 2025, S5a referred to...
# ✅ Only 2 instances, both in historical sections with markers
```

**New notation present:**
```bash
$ grep -rn "S5\.P1" --include="*.md" ../../ | wc -l
42
# ✅ 42 instances of new notation (roughly matches 40+ S5a fixes)
```

**All caps format:**
```bash
$ grep -rn "STAGE_[0-9]" --include="*.md" ../../
[no output]
# ✅ Zero instances (STAGE_5a fixed)
```

### Counts

| Metric | Value |
|--------|-------|
| N_found (Stage 1) | 72 |
| N_fixed (Stage 3) | 70 |
| N_remaining (Stage 4) | 2 (intentional, documented) |
| N_new (Stage 4) | 0 |

### Remaining Intentional Instances

| File | Line | Content | Reason |
|------|------|---------|--------|
| s1_p3_discovery_phase.md | 123 | "Historical Note: The old S5a notation..." | Historical reference with marker |
| EPIC_WORKFLOW_USAGE.md | 456 | "Before 2025, S5a referred to..." | Historical reference with marker |

---

## Lessons Learned

### What Worked

✅ **Multiple pattern variations** - Caught punctuation variants (S5a:, S5a-)
✅ **All-caps check** - Found the STAGE_5a outlier
✅ **Context analysis** - Distinguished historical refs from errors
✅ **Systematic mapping** - Clear S5a → S5.P1 rules prevented inconsistency

### What Was Missed (Found in Round 4)

❌ **Cross-file dependencies** - Fixed notation but didn't verify cross-references still valid
❌ **Template synchronization** - Fixed guides but didn't check if templates need same fix
❌ **Root file exhaustive check** - Found some in README/EPIC_WORKFLOW, but more in CLAUDE.md (Round 4)

### For Next Round

**Round 4 focus:**
- Cross-reference validation (do all references still work after notation changes?)
- Template currency (do templates use new notation?)
- Root file deep dive (exhaustive check of CLAUDE.md)

---

## Round Summary

**Issues Found:** 72
**Issues Fixed:** 70
**Intentional Remaining:** 2 (documented)
**Files Modified:** 30+
**Duration:** 120 minutes
**Next Action:** Round 4 (cross-reference validation and templates)

**Key Takeaway:** Notation changes require multiple pattern types. Basic search found 60, but punctuation/caps variants found 10+ more. Context analysis prevented false positives (2 historical refs preserved).
