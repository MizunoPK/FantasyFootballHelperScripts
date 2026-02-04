# D2: Terminology Consistency

**Dimension Number:** 2
**Category:** Core Dimensions (Always Check)
**Automation Level:** 80% automated
**Priority:** HIGH
**Last Updated:** 2026-02-04

**Focus:** Ensure notation, naming conventions, and terminology are uniform across all guides
**Typical Issues Found:** 50-100 per major notation change

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Errors Happen](#how-errors-happen)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)

---

## What This Checks

**Terminology Consistency** validates that notation and naming are uniform:

✅ **Stage Notation:**
- Correct hierarchy: S# (stage), S#.P# (phase), S#.P#.I# (iteration)
- No old notation: "Stage 5a", "S5a", "5a"
- Consistent formatting: "S5.P1" not "S5P1" or "S5-P1"

✅ **Reserved Terms:**
- "Stage" used only for top-level (S1-S10)
- "Phase" used only for second level (P1, P2, P3)
- "Iteration" used only for third level (I1, I2, I3)
- "Step" used for implementation tasks (not hierarchy)

✅ **Naming Conventions:**
- File names follow pattern: `s#_p#_i#_description.md`
- Folder names: `stages/s#/` not `stages/stage_#/`
- No mixed case in file names

✅ **Terminology Drift:**
- Same concept called same thing throughout
- No synonyms for technical terms (e.g., "spec" vs "specification")
- Consistent abbreviations

---

## Why This Matters

### Impact of Inconsistent Terminology

**Critical Impact:**
- **Agent Confusion:** "Is S5a the same as S5.P1?"
- **Wrong Navigation:** Looks for "Stage 5a" but file is "S5.P1"
- **Template Propagation:** Inconsistent notation in templates = all new epics broken
- **Trust Erosion:** Mixed notation = appears unprofessional

**Example Failure (Real):**
```
Guide used: "S5a", "S5.P1", "Stage 5a", "Round 1" all for same thing
User confusion: "Which notation is correct?"
Result: Lost confidence in guides, manual verification of every reference
```

### Common Trigger Events

**After Notation Change:**
- "Stage 5a" → "S5.P1" leaves stragglers in 40+ files
- Bulk replacement missed variations ("5a:", "back to 5a", etc.)

**After Refactoring:**
- S5 split into S5-S8 leaves old references
- S6 → S9, S7 → S10 leaves old stage numbers

**After Adding New Levels:**
- Added iteration level (S#.P#.I#) but some guides still use old two-level

---

## Pattern Types

### Type 0: Root-Level Files (CRITICAL - Often Missed)

**Files to Always Check:**
```
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
feature-updates/guides_v2/prompts_reference_v2.md
```

**Why These Matter:**
- **High-density references** - These files summarize entire workflow with stage notation throughout
- **Entry points** - Referenced in CLAUDE.md, must use correct current notation
- **Template sources** - Content copied to new files, notation errors propagate

**Common Issues in Root Files:**
- Old notation in workflow summaries ("Stage 5a" → "S5.P1")
- Inconsistent notation within same file (mixes "S5a" and "S5.P1")
- Last Updated dates stale, indicating content not reviewed during notation changes

**Search Commands:**
```bash
# Check root files specifically for old notation
cd feature-updates/guides_v2
grep -n "\bS[0-9][a-z]\b\|Stage [0-9][a-z]" README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md

# Check for mixed notation (both old and new in same file)
grep -n "S[0-9]\.[A-Z]" README.md | head -5  # Shows new notation
grep -n "S[0-9][a-z]" README.md | head -5    # Shows old notation
# If both return results → mixed notation issue
```

**Historical Issue:**
- D2 scripts searched `guides_v2/` BUT primary focus was on stages/ directory
- Root files were not explicitly called out for manual validation
- Result: Old notation persisted in README.md, EPIC_WORKFLOW_USAGE.md undetected

### Type 1: Old Notation Patterns

**Common old notations to find:**

```
"Stage 5a"
"S5a", "S6a", "S7a", "S8a", "S9a"
"5a", "5b", "5c", "5d", "5e"
"Round 1", "Round 2", "Round 3" (when should be S5.P1, S5.P2, S5.P3)
"STAGE_5a", "STAGE_6b" (all caps variants)
```

**Search Commands:**

```bash
# Basic old notation
grep -rn "\bS[0-9][a-z]\b" --include="*.md"

# With punctuation
grep -rn "S[0-9][a-z]:" --include="*.md"

# In text
grep -rn "Stage [0-9][a-z]" --include="*.md"

# All caps
grep -rn "STAGE_[0-9][a-z]" --include="*.md"

# Without S prefix
grep -rn "\b[0-9][a-z]\b" --include="*.md" | grep -v "S[0-9]"
```

### Type 2: Incorrect Hierarchy Usage

**Patterns:**

```
Using "Stage" for phase level: "Stage 5.P1" → Should be "S5.P1"
Using "Phase" for iteration level: "Phase 5.1.1" → Should be "S5.P1.I1"
Using "Round" for phase: "Round 1" → Should be "S5.P1" or just "P1"
```

**Search Commands:**

```bash
# "Stage" with dot notation (likely wrong)
grep -rn "Stage [0-9]\.[A-Z]" --include="*.md"

# "Phase" with full hierarchy (likely wrong)
grep -rn "Phase [0-9]\.[0-9]\.[0-9]" --include="*.md"

# "Round" as hierarchy (context-dependent)
grep -rn "Round [0-9]" --include="*.md"
```

### Type 3: Formatting Inconsistencies

**Patterns:**

```
Missing dots: "S5P1" → Should be "S5.P1"
Wrong separators: "S5-P1" → Should be "S5.P1"
Spaces: "S5 P1" → Should be "S5.P1"
Lowercase: "s5.p1" → Should be "S5.P1"
```

**Search Commands:**

```bash
# No dot between stage and phase
grep -rn "S[0-9][A-Z][0-9]" --include="*.md"

# Dash separator
grep -rn "S[0-9]-[A-Z][0-9]" --include="*.md"

# Space separator
grep -rn "S[0-9] [A-Z][0-9]" --include="*.md"

# Lowercase
grep -rn "s[0-9]\.p[0-9]" --include="*.md"
```

### Type 4: File Name Convention Violations

**Patterns:**

```
Missing s# prefix: "epic_planning.md" → Should be "s1_epic_planning.md"
Wrong separator: "s5-p1-planning.md" → Should be "s5_p1_planning.md"
Mixed case: "S5_Planning.md" → Should be "s5_planning.md"
```

**Search Commands:**

```bash
# Find files without s# prefix in stages folder
find stages/s[0-9] -name "*.md" ! -name "s[0-9]*"

# Find files with wrong separators
find stages -name "*-*-*.md"

# Find files with capital letters
find stages -name "*[A-Z]*.md"
```

---

## How Errors Happen

### Root Cause 1: Incomplete Bulk Replacement

**Scenario:** Notation changed from "5a" to "S5.P1"

**Intended Change:**
```
All instances of "5a" → "S5.P1"
All instances of "5b" → "S5.P2"
All instances of "5c" → "S5.P3"
```

**What Happens:**
```bash
# Agent runs basic replacement
sed -i 's/5a/S5.P1/g' *.md

# But forgets:
# - "5a:" (with punctuation)
# - " 5a " (with spaces)
# - "Stage 5a" (with prefix)
# - "S5a" (with S prefix already)
# - "back to 5a" (in sentence)
# - "5a_planning.md" (in file names)
```

**Result:** 60% updated, 40% stragglers

### Root Cause 2: Pattern Variation Blindness

**Scenario:** Searched for " 5a" but didn't think about variations

**Missed Variations:**
- "5a:" (colon after)
- "(5a)" (in parentheses)
- "5a-5b" (in range)
- "5a," (comma after)
- "5a." (period after)

**Result:** 20-30 instances per variation type

### Root Cause 3: Context-Specific Notation

**Scenario:** Some files use abbreviations, some use full names

**Example:**
```
File A: "spec" (abbreviated)
File B: "specification" (full)
File C: "spec.md" (file reference)
File D: "Spec" (capitalized in header)
```

**Problem:** Should standardize on one form

### Root Cause 4: Template Drift

**Scenario:** Guides updated but templates lag behind

**Result:** New epics created with old notation from templates

---

## Automated Validation

### Script 1: Find Old Notation

```bash
#!/bin/bash
# find_old_notation.sh
# Searches for common old notation patterns

echo "=== Finding Old Notation ==="

# Old letter-based notation
echo "Checking for S[0-9][a-z] patterns..."
grep -rn "\bS[0-9][a-z]\b" --include="*.md" guides_v2/

# Old "Stage Xa" format
echo "Checking for 'Stage Xa' patterns..."
grep -rn "Stage [0-9][a-z]" --include="*.md" guides_v2/

# Standalone letter notation
echo "Checking for standalone 'Xa' patterns..."
grep -rn "\b[5-9][a-z]\b" --include="*.md" guides_v2/ | grep -v "S[0-9]"

# All caps variants
echo "Checking for STAGE_Xa patterns..."
grep -rn "STAGE_[0-9][a-z]" --include="*.md" guides_v2/
```

### Script 2: Validate Notation Format

```bash
#!/bin/bash
# validate_notation.sh
# Ensures proper S#.P#.I# format

echo "=== Validating Notation Format ==="

# Check for missing dots
echo "Checking for S#P# (missing dot)..."
grep -rn "S[0-9][A-Z][0-9]" --include="*.md" guides_v2/ | grep -v "S[0-9]\.[A-Z]"

# Check for wrong separators
echo "Checking for S#-P# (wrong separator)..."
grep -rn "S[0-9]-[A-Z]" --include="*.md" guides_v2/

# Check for spaces
echo "Checking for S# P# (spaces)..."
grep -rn "S[0-9] [A-Z][0-9]" --include="*.md" guides_v2/
```

### Script 3: File Name Validation

```bash
#!/bin/bash
# validate_filenames.sh
# Checks file naming conventions

echo "=== Validating File Names ==="

# Files in stages/ should start with s#_
find guides_v2/stages/s[0-9] -name "*.md" ! -name "s[0-9]*" -print

# Should use underscores, not dashes
find guides_v2/stages -name "*-*-*.md" -print

# Should be lowercase
find guides_v2/stages -name "*[A-Z]*.md" ! -name "README.md" -print
```

---

## Manual Validation

###⚠️ CRITICAL: Always Check Root-Level Files First

**Mandatory root file validation:**

```bash
# Step 0: Check root files for notation consistency (high-priority, often skipped)
cd feature-updates/guides_v2

# Check each root file individually
for file in README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md; do
  echo "=== Checking $file ==="
  echo "Old notation instances:"
  grep -n "\bS[0-9][a-z]\b\|Stage [0-9][a-z]" "$file" 2>/dev/null | wc -l
  echo "New notation instances:"
  grep -n "S[0-9]\.[A-Z]" "$file" 2>/dev/null | wc -l
  echo "Last Updated:"
  grep -n "Last Updated" "$file" 2>/dev/null | head -1
  echo ""
done
```

**Red Flags:**
- Last Updated > 1 month old = likely missed during recent changes
- Both old AND new notation present = mixed notation issue
- Zero old notation + Last Updated recent = probably good

### When Manual Check Needed

**Automated scripts can't catch:**

1. **Context-Dependent Abbreviations:**
   - "spec" vs "specification" - both valid, but should be consistent
   - "impl" vs "implementation"
   - "prereq" vs "prerequisite"

2. **Synonym Usage:**
   - "check" vs "verify" vs "validate"
   - "error" vs "issue" vs "problem"
   - "guide" vs "document"

3. **Capitalization Consistency:**
   - "Stage" vs "stage" in prose
   - "Prerequisites" vs "prerequisites" as header

4. **Intentional Variations:**
   - Historical examples using old notation on purpose
   - Quoted text preserving original notation
   - Migration guides showing before/after

### Manual Validation Process

**For terminology drift:**

```markdown
STEP 1: Pick 5-10 core technical terms
- Example: specification, implementation, verification

STEP 2: Search for variations of each
$ grep -rn "spec\|specification" --include="*.md"

STEP 3: Identify inconsistencies
- File A uses "spec" 10 times
- File B uses "specification" 15 times
- Decision: Standardize on "specification" (full form)

STEP 4: Update to preferred form
- Replace casual "spec" with "specification"
- Exception: file names (spec.md stays as is)
```

---

## Context-Sensitive Rules

### Intentional Old Notation

**Acceptable in these contexts:**

**1. Historical Comparisons:**
```markdown
**Old notation (before v2.0):**
- Stage 5a → Implementation Planning
- Stage 5b → Execution

**New notation (v2.0+):**
- S5.P1 → Implementation Planning
- S6 → Execution
```
**Verdict:** ✅ ACCEPTABLE (clearly labeled as historical)

**2. Migration Guides:**
```markdown
If you see "S5a" in old epics, update to "S5.P1"
```
**Verdict:** ✅ ACCEPTABLE (teaching migration)

**3. User Quotes:**
```markdown
User reported: "Can't find Stage 5a in documentation"
```
**Verdict:** ✅ ACCEPTABLE (quoting user input)

### Always Errors

**Never acceptable:**

**1. Current Documentation:**
```markdown
Next, proceed to S5a for implementation planning
```
**Verdict:** ❌ ERROR (should be S5.P1 or S5)

**2. File Names:**
```
s5a_planning.md
```
**Verdict:** ❌ ERROR (should be s5_p1_planning.md)

**3. Prerequisites:**
```markdown
## Prerequisites
- S5a complete
```
**Verdict:** ❌ ERROR (should be S5.P1)

---

## Real Examples

### Example 1: Old Notation Stragglers (KAI-7 Round 3)

**Issue Found:**
```
Pattern: \bS[5-9]a\b
Instances: 60+ across 30+ files
```

**Sample Matches:**
```
stages/s5/s5_bugfix_workflow.md:45: "After S5a complete"
stages/s8/s8_p1_cross_feature_alignment.md:67: "Return to S5a"
templates/epic_readme_template.md:123: "Current: S6a"
```

**Analysis:**
- All are current workflow references (not historical)
- Should use S5.P1, S6.P1, etc. (phase level)
- Some could use just S5, S6 (stage level, context-dependent)

**Fix:**
```bash
# Used word boundaries to avoid partial matches
sed -i 's/\bS5a\b/S5/g; s/\bS6a\b/S6/g; s/\bS7a\b/S7/g; \
        s/\bS8a\b/S8/g; s/\bS9a\b/S9/g' \
  stages/**/*.md templates/*.md reference/*.md
```

**Verification:**
```bash
$ grep -rn "\bS[5-9]a\b" --include="*.md"
# 0 matches
```

### Example 2: Wrong Hierarchy Level

**Issue Found:**
```
File: stages/s2/s2_feature_deep_dive.md
Line: 45
Content: "Stage 2.P1 - Research Phase"
```

**Analysis:**
- Used "Stage" with phase notation
- Should be "S2.P1" (no "Stage" prefix for phases)
- "Stage" is reserved for top-level only (S1-S10)

**Fix:**
```bash
sed -i 's/Stage \([0-9]\)\.\([A-Z][0-9]\)/S\1.\2/g' \
  stages/s2/s2_feature_deep_dive.md
```

**Result:**
```
S2.P1 - Research Phase
```

### Example 3: File Name Convention

**Issue Found:**
```
File: stages/s5/round1_planning.md
```

**Analysis:**
- Missing s5_ prefix
- Old "round1" notation (should be p1 or s5_p1)
- Doesn't follow naming convention: s#_p#_description.md

**Fix:**
```bash
# Rename file
git mv stages/s5/round1_planning.md stages/s5/s5_p1_planning_round1.md

# Update all references
sed -i 's|stages/s5/round1_planning\.md|stages/s5/s5_p1_planning_round1.md|g' \
  stages/**/*.md
```

### Example 4: Root File Mixed Notation (High Priority)

**Issue Found:**
```markdown
File: feature-updates/guides_v2/README.md
Last Updated: 2025-12-30 (over 1 month stale)
```

**Search Results:**
```bash
$ grep -n "S[0-9][a-z]\|S[0-9]\.[A-Z]" README.md | head -10
84:Old workflow: S5a → S5b → S5c
88:New workflow: S5.P1 → S5.P2 → S5.P3
92:   Flesh out spec.md for each feature
156:STAGE 2: Feature Deep Dives (Loop per feature)
```

**Analysis:**
- **CRITICAL** - README.md is main entry point (referenced in CLAUDE.md)
- Line 84: Uses old notation "S5a" in context that appears to be current workflow
- Line 88: Uses new notation "S5.P1" for same section
- **Mixed notation** within same file = high confusion risk
- Stale "Last Updated" date indicates file not reviewed during notation changes

**Impact:**
- Users/agents reading README get conflicting information
- Unclear which notation is "official"
- Template content may be copied with wrong notation

**Fix:**
```bash
# Update to consistent new notation throughout
# Update "Last Updated" to current date
# Review entire file for other inconsistencies

# Example fix for mixed notation:
sed -i 's/Old workflow: S5a → S5b → S5c/Old workflow: Stage 5a → Stage 5b → Stage 5c (deprecated)/g' README.md
sed -i 's/S[0-9][a-z]\>/S5.P1/g' README.md  # Update remaining old notation

# Update Last Updated field
sed -i 's/Last Updated:.*$/Last Updated: 2026-02-04/g' README.md
```

**Why This Was Missed:**
- D2 scripts searched `guides_v2/` BUT agents focused on stages/ directory
- Root files not explicitly flagged for manual validation
- **High-impact oversight** - these files have highest visibility

---

## Pattern Library

### Most Common Patterns to Search

**After notation change from "Xa" to "S#.P#":**

```bash
# Pattern variations (try all)
grep -rn "\bS[0-9][a-z]\b"           # S5a, S6b, etc
grep -rn "\b[5-9][a-z]\b"            # 5a, 6b standalone
grep -rn "S[0-9][a-z]:"              # S5a: (with colon)
grep -rn "Stage [0-9][a-z]"          # Stage 5a
grep -rn "STAGE_[0-9][a-z]"          # STAGE_5a (all caps)
grep -rn "S[0-9][a-z] "              # S5a  (with space after)
grep -rn " S[0-9][a-z]"              # S5a (with space before)
grep -rn "back to [0-9][a-z]"        # Context phrases
grep -rn "restart [0-9][a-z]"
grep -rn "proceed to [0-9][a-z]"
```

**After stage renumbering (S6→S9, S7→S10):**

```bash
# All references to old stage numbers
grep -rn "\bS6\b" --include="*.md"
grep -rn "\bS7\b" --include="*.md"
grep -rn "Stage 6\|Stage 7"
grep -rn "stages/s6/\|stages/s7/"
```

---

## See Also

**Previous Dimension (If You Haven't Read It Yet):**
- **D1: Cross-Reference Accuracy** - Fix broken file paths BEFORE fixing notation (so fixes reference correct paths)

**Related Dimensions (Coming Soon):**
- D6: Template Currency ⏳ - After fixing notation, update templates to use new notation
- D9: Intra-File Consistency ⏳ - Verify notation is consistent within each file

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to search for notation issues
- `../stages/stage_3_apply_fixes.md` - Bulk notation replacement strategies

**Reference (Coming Soon):**
- `../reference/pattern_library.md` ⏳ - More search patterns (see examples in this guide for now)
- `../reference/context_analysis_guide.md` ⏳ - Determining intentional vs error

---

**When to Use:** Run D2 validation after any notation changes, terminology updates, or refactoring.
