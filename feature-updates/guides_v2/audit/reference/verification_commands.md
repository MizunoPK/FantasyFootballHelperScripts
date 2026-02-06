# Verification Commands

**Purpose:** Command library for Stage 4 verification with before/after validation
**Audience:** Agents verifying audit fixes were applied correctly
**Last Updated:** 2026-02-05

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Verification Workflow](#verification-workflow)
3. [Count Tracking Commands](#count-tracking-commands)
4. [Before/After Comparison](#beforeafter-comparison)
5. [Spot-Check Commands](#spot-check-commands)
6. [Pattern Re-Run Commands](#pattern-re-run-commands)
7. [File Integrity Checks](#file-integrity-checks)
8. [Common Verification Scenarios](#common-verification-scenarios)

---

## Quick Start

### Verification Formula

```bash
# The 4-step verification process
1. Re-run discovery patterns → Count N_found_after
2. Compare to fix plan → N_fixed (from Stage 3)
3. Calculate: N_remaining = N_found_after
4. Spot-check random files → Verify no new issues introduced
```

### Key Metrics

**From Stage 1 (Discovery):**
- `N_found` = Issues found initially

**From Stage 3 (Apply Fixes):**
- `N_fixed` = Issues actually fixed

**From Stage 4 (Verification):**
- `N_remaining` = Issues still present after fixes
- `N_new` = New issues introduced by fixes (MUST be 0)

**Exit Condition:**
- `N_remaining = 0` (all issues resolved)
- `N_new = 0` (no new issues introduced)

---

## Verification Workflow

### Step 1: Re-Run Discovery Patterns

**Purpose:** Count how many instances remain after fixes

```bash
# Example: Re-run old notation search
PATTERN="S[0-9][a-z]"
N_found_after=$(grep -rn "$PATTERN" --include="*.md" . 2>/dev/null | wc -l)
echo "After fixes: $N_found_after instances remain"
```

### Step 2: Verify Against Fix Plan

**From fix_plan.md:**
```text
Group 1: Old Notation (60 instances)
- S5a → S5
- S6a → S6
```

**Verification:**
```bash
# Original discovery: N_found = 60
# Fix plan claimed: N_fixed = 60
# Verification count: N_found_after = ?

# If N_found_after = 0 → All fixed ✅
# If N_found_after > 0 → Incomplete fixes ❌
```

### Step 3: Document Remaining Instances

**If N_remaining > 0, must document each:**
```bash
# Find remaining instances with context
grep -rn "$PATTERN" --include="*.md" . -C 2 > remaining_instances.txt

# For each instance, determine:
# 1. File:line location
# 2. Is it intentional? (example, historical reference, etc.)
# 3. Why acceptable? (or should it be fixed?)
```

### Step 4: Check for New Issues

**Purpose:** Verify fixes didn't introduce new problems

```bash
# Spot-check 10 random modified files
git diff --name-only | shuf | head -10 | while read file; do
  echo "=== Checking: $file ==="
  # Manual read or automated checks
done
```

---

## Count Tracking Commands

### Basic Count

```bash
# Count pattern occurrences
PATTERN="your_pattern_here"
count=$(grep -rn "$PATTERN" --include="*.md" . 2>/dev/null | wc -l)
echo "Found: $count instances"
```

### Count by File

```bash
# Show counts per file
PATTERN="your_pattern_here"
grep -rn "$PATTERN" --include="*.md" . 2>/dev/null | \
  cut -d: -f1 | \
  sort | \
  uniq -c | \
  sort -rn
```

### Count by Directory

```bash
# Show counts per directory
PATTERN="your_pattern_here"
for dir in dimensions stages reference templates; do
  count=$(grep -rn "$PATTERN" --include="*.md" $dir 2>/dev/null | wc -l)
  echo "$dir: $count"
done
```

### Historical Comparison

```bash
# Compare counts across git commits
PATTERN="your_pattern_here"

# Before fixes
git checkout <before-commit>
before=$(grep -rn "$PATTERN" --include="*.md" . 2>/dev/null | wc -l)

# After fixes
git checkout <after-commit>
after=$(grep -rn "$PATTERN" --include="*.md" . 2>/dev/null | wc -l)

echo "Before: $before"
echo "After: $after"
echo "Fixed: $((before - after))"
```

---

## Before/After Comparison

### Single File Comparison

```bash
# Show before/after diff for specific file
FILE="stages/stage_1_discovery.md"
git diff HEAD~1 HEAD -- "$FILE"
```

### Pattern-Specific Diff

```bash
# Show only lines that changed matching pattern
PATTERN="S[0-9][a-z]"
git diff HEAD~1 HEAD | grep -E "^[-+].*$PATTERN"
```

### Summary of Changes

```bash
# Count added/removed lines per file
git diff HEAD~1 HEAD --numstat
```

---

## Spot-Check Commands

### Random File Selection

```bash
# Select 10 random .md files
find . -name "*.md" -type f | shuf | head -10
```

### Random Line Selection

```bash
# Read 20 random lines from file
FILE="your_file.md"
shuf -n 20 "$FILE" | sort -n
```

### Systematic Sampling

```bash
# Check every 5th file alphabetically
files=($(find . -name "*.md" -type f | sort))
for ((i=0; i<${#files[@]}; i+=5)); do
  echo "Checking: ${files[$i]}"
done
```

---

## Pattern Re-Run Commands

### Single Pattern Verification

```bash
# Re-run pattern from discovery phase
PATTERN="your_pattern"
echo "=== Re-running Pattern: $PATTERN ==="
grep -rn "$PATTERN" --include="*.md" .
count=$(grep -rn "$PATTERN" --include="*.md" . 2>/dev/null | wc -l)
echo "Total found: $count"
```

### Pattern Variations Check

```bash
# Check pattern variations that might have been missed
BASE_PATTERN="S5"
for variation in "${BASE_PATTERN}a" "${BASE_PATTERN}:" "${BASE_PATTERN}-" "${BASE_PATTERN} "; do
  count=$(grep -rn "$variation" --include="*.md" . 2>/dev/null | wc -l)
  echo "$variation: $count"
done
```

### Multi-Pattern Batch Check

```bash
# Check multiple patterns at once
PATTERNS=("S5a" "S6a" "S7a" "S8a" "S9a")
for pattern in "${PATTERNS[@]}"; do
  count=$(grep -rn "$pattern" --include="*.md" . 2>/dev/null | wc -l)
  echo "$pattern: $count instances"
done
```

---

## File Integrity Checks

### Validate File Exists

```bash
# Check all referenced files exist
grep -rh "stages/s[0-9].*\.md\|templates/.*\.md\|reference/.*\.md" \
  --include="*.md" . | \
  grep -o "[a-z_/]*\.md" | \
  sort -u | \
  while read path; do
    check_path="../$path"
    [ ! -f "$check_path" ] && echo "BROKEN: $path"
  done
```

### Check for Broken Anchors

```bash
# Find internal anchors and verify sections exist
# (Requires manual verification)
grep -rn "\[.*\](#[^)]*)" --include="*.md" . | \
  while IFS=: read file line content; do
    anchor=$(echo "$content" | grep -o "#[a-z0-9-]*" | tr -d '#')
    # Check if anchor target exists in file
    if ! grep -q "^## .*$anchor\|^### .*$anchor" "$file" 2>/dev/null; then
      echo "BROKEN ANCHOR: $file:$line → #$anchor"
    fi
  done
```

### Validate Markdown Syntax

```bash
# Check for common markdown errors
# Unclosed code blocks
for file in $(find . -name "*.md"); do
  backticks=$(grep -c "^\`\`\`" "$file")
  if [ $((backticks % 2)) -ne 0 ]; then
    echo "UNCLOSED CODE BLOCK: $file"
  fi
done
```

---

## Common Verification Scenarios

### Scenario 1: Verifying Notation Fix

**Discovery found:** 60 instances of "S5a"
**Fix plan:** Replace all "S5a" → "S5.P1"
**Verification:**

```bash
# Step 1: Re-run discovery pattern
N_remaining=$(grep -rn "S5a" --include="*.md" . 2>/dev/null | wc -l)
echo "Remaining S5a instances: $N_remaining"

# Step 2: Check variations that might remain
for var in "S5a:" "S5a-" "(S5a)" "S5a,"; do
  count=$(grep -rn "$var" --include="*.md" . 2>/dev/null | wc -l)
  [ $count -gt 0 ] && echo "Found: $var ($count instances)"
done

# Step 3: Verify new notation present
N_new=$(grep -rn "S5\.P1" --include="*.md" . 2>/dev/null | wc -l)
echo "New notation S5.P1 found: $N_new instances"

# Expected: N_new ≈ 60 (accounting for context variations)
```

### Scenario 2: Verifying File Path Fixes

**Discovery found:** 15 broken references to "stages/s6/"
**Fix plan:** Update all to "stages/s9/"
**Verification:**

```bash
# Step 1: Check old path no longer referenced
N_old=$(grep -rn "stages/s6/" --include="*.md" . 2>/dev/null | wc -l)
echo "Old path (stages/s6/) remaining: $N_old"

# Step 2: Check new path exists
N_new=$(grep -rn "stages/s9/" --include="*.md" . 2>/dev/null | wc -l)
echo "New path (stages/s9/) found: $N_new"

# Step 3: Validate all new paths actually exist
grep -rh "stages/s9/.*\.md" --include="*.md" . | \
  grep -o "stages/s9/[^)]*\.md" | \
  sort -u | \
  while read path; do
    [ ! -f "../$path" ] && echo "BROKEN: $path"
  done
```

### Scenario 3: Verifying File Size Reduction

**Discovery found:** 5 files >1250 lines
**Fix plan:** Split large files using reduction guide
**Verification:**

```bash
# Step 1: Check original files still >1250?
LARGE_FILES=("file1.md" "file2.md" "file3.md" "file4.md" "file5.md")
for file in "${LARGE_FILES[@]}"; do
  lines=$(wc -l < "$file" 2>/dev/null || echo 0)
  if [ $lines -gt 1250 ]; then
    echo "STILL LARGE: $file ($lines lines)"
  else
    echo "✅ FIXED: $file ($lines lines)"
  fi
done

# Step 2: Check new sub-files created
# (List expected from fix plan)

# Step 3: Verify cross-references updated
# Check that guides reference new split files, not old large files
```

### Scenario 4: Verifying TODO/TBD Removal

**Discovery found:** 12 TODO markers
**Fix plan:** Replace all TODOs with actual content
**Verification:**

```bash
# Step 1: Re-run TODO search
grep -rn "TODO\|TBD\|FIXME" --include="*.md" .

# Step 2: Count remaining
N_remaining=$(grep -rn "TODO\|TBD\|FIXME" --include="*.md" . 2>/dev/null | wc -l)
echo "Remaining placeholders: $N_remaining"

# Expected: 0 (all replaced with content)

# Step 3: Verify replacement content exists
# (Manual check of files that previously had TODOs)
```

---

## Verification Checklist Template

```markdown
## Verification Report - Round N

**Pattern:** [Pattern description]
**Files Checked:** [Number] files

### Counts

| Metric | Value | Expected | Pass? |
|--------|-------|----------|-------|
| N_found (Stage 1) | XX | - | - |
| N_fixed (Stage 3) | XX | XX | ✅/❌ |
| N_remaining (Stage 4) | XX | 0 | ✅/❌ |
| N_new (Stage 4) | XX | 0 | ✅/❌ |

### Pattern Re-Run Results

```bash
[Command used]
[Output showing count]
```

### Before/After Evidence

**Before (sample):**
```
[Line from file before fix]
```

**After (sample):**
```
[Line from file after fix]
```

### Spot-Check Files (10 random)

- [ ] file1.md - No issues
- [ ] file2.md - No issues
- [ ] file3.md - No issues
...

### Remaining Instances (if any)

| File | Line | Content | Intentional? | Reason |
|------|------|---------|--------------|--------|
| ... | ... | ... | Yes/No | ... |

### New Issues Introduced (if any)

| File | Line | Issue | Severity |
|------|------|-------|----------|
| ... | ... | ... | ... |

### Conclusion

✅ PASSED - All fixes verified, zero remaining, zero new issues
❌ FAILED - [Specific failures]
```

---

## Advanced Techniques

### Diff-Based Verification

```bash
# Show only the actual changes made
git diff HEAD~1 HEAD --word-diff=color | less
```

### Statistical Verification

```bash
# Calculate fix success rate
N_found=60
N_remaining=0
success_rate=$(awk "BEGIN {print (($N_found - $N_remaining) / $N_found) * 100}")
echo "Fix success rate: ${success_rate}%"
```

### Automated Full Verification

```bash
#!/bin/bash
# Full verification script

PATTERNS=("S5a" "S6a" "S7a" "TODO" "TBD")
echo "=== Full Verification ==="
for pattern in "${PATTERNS[@]}"; do
  count=$(grep -rn "$pattern" --include="*.md" . 2>/dev/null | wc -l)
  echo "$pattern: $count"
done
```

---

## See Also

- **Pattern Library:** `reference/pattern_library.md` - Discovery patterns to re-run
- **Stage 4 Verification:** `stages/stage_4_verification.md` - Complete verification workflow
- **Stage 3 Apply Fixes:** `stages/stage_3_apply_fixes.md` - How fixes were applied
