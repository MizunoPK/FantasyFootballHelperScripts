# D1: Cross-Reference Accuracy

**Dimension Number:** 1
**Category:** Core Dimensions (Always Check)
**Automation Level:** 90% automated
**Priority:** HIGH
**Last Updated:** 2026-02-04

**Focus:** Ensure all file paths, stage references, and cross-links point to existing, correct locations
**Typical Issues Found:** 15-30 per major restructuring

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

**Cross-Reference Accuracy** validates that all references to other files are correct:

✅ **File Paths:**
- `stages/sN/file.md` points to existing file
- Relative paths (`../folder/file.md`) resolve correctly
- Template paths are current

✅ **Stage References:**
- `S#`, `S#.P#`, `S#.P#.I#` reference existing stages/phases/iterations
- "Next stage" points to correct successor
- Prerequisites reference correct predecessor stages

✅ **Cross-Links:**
- Markdown links `[text](path.md)` point to existing files
- Internal anchors `[text](#section)` point to existing sections
- External links are valid (if checked)

✅ **No Orphaned References:**
- No references to deleted files
- No references to renamed files (old names)
- No references to moved files (old locations)

---

## Why This Matters

### Impact of Broken References

**Critical Impact:**
- **Agent Confusion:** "Read stages/s5/round1/file.md" but file doesn't exist
- **Workflow Broken:** Cannot proceed to next stage (wrong path given)
- **Template Propagation:** Error in template = error in ALL new epics
- **Trust Erosion:** Multiple broken links = user loses confidence in guides

**Example Failure (Real):**
```bash
Guide said: "Read stages/s6/epic_smoke_testing.md"
Reality: File is at stages/s9/s9_p1_epic_smoke_testing.md
Result: Agent couldn't find file, workflow stuck
```markdown

### Common Trigger Events

**After Stage Renumbering:**
- S6 → S9 leaves references to "stages/s6/"
- S7 → S10 leaves "Next: S7" in guides

**After File Renaming:**
- epic_cleanup.md → s10_epic_cleanup.md
- phase_1_specification.md → s2_p2_specification.md

**After Folder Reorganization:**
- stages/s5/round1/ → stages/s5/s5_p1_*
- stages/s5/alignment/ → content integrated into guides

---

## Pattern Types

### Type 0: Root-Level Files (CRITICAL - Often Missed)

**Files to Always Check:**
```text
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
feature-updates/guides_v2/prompts_reference_v2.md
feature-updates/guides_v2/audit/README.md (modular audit system entry point)
```

**Why These Matter:**
- **README.md** = Main entry point, referenced in CLAUDE.md
- **EPIC_WORKFLOW_USAGE.md** = Detailed workflow reference
- **prompts_reference_v2.md** = MANDATORY prompts, referenced in CLAUDE.md
- These files contain high-density cross-references to stages/, templates/, reference/

**Search Command:**
```bash
# Check root-level files for cross-references
cd feature-updates/guides_v2
for file in README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md; do
  echo "=== Checking $file ==="
  grep -n "stages/s[0-9].*\.md\|templates/.*\.md\|reference/.*\.md\|parallel_work/.*\.md\|debugging/.*\.md" "$file" || echo "No paths found"
done
```bash

**Validation:**
```bash
# Extract all paths from root files and verify they exist
grep -h "stages/s[0-9].*\.md\|templates/.*\.md\|reference/.*\.md" \
  README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md 2>/dev/null | \
  grep -o "[a-z_/]*\.md" | \
  sort -u | \
  while read path; do
    [ ! -f "$path" ] && echo "BROKEN in root file: $path"
  done
```

**Historical Issue:**
- Root-level files were NOT checked in original audit implementation
- D1 only searched `guides_v2/stages` directory
- Result: README.md references could be broken without detection

### Type 1: Direct File Paths

**Pattern:**
```text
stages/sN/file_name.md
templates/template_name.md
reference/reference_name.md
```bash

**Search Command:**
```bash
# Extract all file paths (INCLUDING root-level files)
grep -rh "stages/s[0-9].*\.md\|templates/.*\.md\|reference/.*\.md" \
  --include="*.md" | \
  grep -o "stages/s[0-9][^)]*\.md\|templates/[^)]*\.md\|reference/[^)]*\.md" | \
  sort -u
```

**Validation:**
```bash
# Check each path exists
while read path; do
  [ ! -f "$path" ] && echo "BROKEN: $path"
done < paths.txt
```markdown

### Type 2: Stage References

**Pattern:**
```text
S#, S#.P#, S#.P#.I# (S1, S5.P2, S5.P2.I3)
Stage N, Stage N.P#
```

**Search Command:**
```bash
# Find all stage references
grep -rn "\bS[0-9]\{1,2\}\(\.[A-Z][0-9]\{1,2\}\(\.[A-Z][0-9]\{1,2\}\)\?\)\?\b" \
  --include="*.md"

# Find old notation
grep -rn "Stage [0-9][a-z]\|S[0-9][a-z]" --include="*.md"
```markdown

**Validation:**
- Verify stage numbers are 1-10 (current workflow)
- Verify phases exist for referenced stage
- Verify iterations exist for referenced phase

### Type 3: Markdown Links

**Pattern:**
```markdown
[Link text](path/to/file.md)
[Link text](../relative/path.md)
[Link text](#internal-anchor)
```

**Search Command:**
```bash
# Extract all markdown links
grep -rh "\[.*\](.*\.md)" --include="*.md" | \
  grep -o "](.*)" | \
  sed 's/^](//; s/)$//' | \
  sort -u
```markdown

**Validation:**
```bash
# Check each link target exists
# (requires resolving relative paths from source file location)
```

### Type 4: Stage Transition References

**Pattern:**
```text
"Next stage: S#"
"After S# complete"
"Before starting S#"
"Proceed to S#"
```bash

**Search Command:**
```bash
# Find transition references
grep -rn "Next.*S[0-9]\|After S[0-9]\|Before.*S[0-9]\|Proceed to S[0-9]" \
  --include="*.md" -i
```

**Validation:**
- Verify stage order correct (S5 next is S6, not S7)
- Verify prerequisites match previous stage outputs

---

## How Errors Happen

### Root Cause 1: Incomplete Bulk Replacement

**Scenario:** Stage 5 split into S5-S8

**Intended Change:**
```text
Stage 5a → S5
Stage 5b → S6
Stage 5c → S7
Stage 5d → S8
```bash

**What Happens:**
```bash
# Agent runs
sed -i 's/Stage 5a/S5/g' *.md

# But forgets variations:
# - "5a:" (with colon)
# - "back to 5a" (in sentence)
# - "stages/s5/5a_file.md" (in path)
# - "STAGE_5a" (all caps)
```

**Result:** 70% fixed, 30% remain (stragglers)

### Root Cause 2: File Renamed But References Not Updated

**Scenario:** epic_cleanup.md → s10_epic_cleanup.md

**Files Referencing It:**
```text
stages/s9/s9_epic_final_qc.md:45: "stages/s7/epic_cleanup.md"
stages/s9/s9_p4_epic_final_review.md:67: "stages/s7/epic_cleanup.md"
```markdown

**What Happens:** File renamed, but references still use old name

**Result:** 2 broken links

### Root Cause 3: Stage Renumbering Cascade

**Scenario:** S6 → S9, S7 → S10

**Impact:**
```text
Every reference to "S6" needs → "S9"
Every reference to "S7" needs → "S10"
Every reference to "stages/s6/" needs → "stages/s9/"
Every reference to "stages/s7/" needs → "stages/s10/"
```

**What Happens:** Some references missed in different files

**Result:** 10-20 broken references across guides

### Root Cause 4: Template Not Updated

**Scenario:** Workflow gains new stage (S9 added)

**Templates Still Show:**
```text
Workflow: S1 → S2 → S3 → S4 → S5 → S6 → S7
```markdown

**Should Show:**
```text
Workflow: S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9 → S10
```

**Result:** All new epics created use outdated workflow diagram

---

## Automated Validation

### Script 1: Validate All File Paths

```bash
#!/bin/bash
# validate_file_paths.sh
# Extracts all file paths and verifies they exist

echo "=== Validating File Paths ==="

# Extract all paths
grep -rh "stages/s[0-9].*\.md\|templates/.*\.md\|reference/.*\.md" \
  --include="*.md" guides_v2/ | \
  grep -o "[a-z_/]*\.md" | \
  sort -u > /tmp/all_paths.txt

total=$(wc -l < /tmp/all_paths.txt)
broken=0

# Verify each
while read path; do
  if [ ! -f "$path" ]; then
    echo "❌ BROKEN: $path"
    ((broken++))
  fi
done < /tmp/all_paths.txt

echo ""
echo "Total paths: $total"
echo "Broken paths: $broken"

if [ $broken -eq 0 ]; then
  echo "✅ All file paths valid"
  exit 0
else
  echo "❌ Found broken paths"
  exit 1
fi
```bash

### Script 2: Find References to Non-Existent Files

```bash
#!/bin/bash
# find_broken_refs.sh
# More sophisticated - extracts paths and checks from source file context

# Check all directories AND root-level files
{
  find guides_v2/stages guides_v2/templates guides_v2/reference \
       guides_v2/debugging guides_v2/missed_requirement guides_v2/parallel_work \
       guides_v2/prompts guides_v2/audit -name "*.md" 2>/dev/null
  # Add root-level files explicitly
  ls guides_v2/*.md 2>/dev/null
} | while read source_file; do
  # Extract paths from this file
  grep -o "stages/s[0-9][^)]*\.md\|templates/[^)]*\.md\|reference/[^)]*\.md\|debugging/[^)]*\.md" \
    "$source_file" | sort -u | while read ref_path; do
    # Check if referenced file exists (relative to guides_v2/)
    full_path="guides_v2/$ref_path"
    if [ ! -f "$full_path" ]; then
      echo "BROKEN in $source_file"
      echo "  References: $ref_path"
      echo "  File does not exist: $full_path"
      echo ""
    fi
  done
done
```

### Script 3: Validate Stage Number References

```bash
#!/bin/bash
# validate_stage_numbers.sh
# Checks stage references are within valid range (S1-S10)

echo "=== Validating Stage Numbers ==="

# Find references to stage numbers > 10
grep -rn "S\(1[1-9]\|[2-9][0-9]\)" --include="*.md" guides_v2/ | \
  grep -v "S10" | \
  while read line; do
    echo "❌ INVALID STAGE: $line"
  done

# Find old notation (5a, 5b, etc)
grep -rn "\bS[0-9][a-z]\b\|Stage [0-9][a-z]" --include="*.md" guides_v2/ | \
  while read line; do
    echo "⚠️  OLD NOTATION: $line"
  done
```markdown

---

## Manual Validation

### When Manual Check Needed

**Automated scripts can't catch:**

1. **Context-Sensitive References:**
   - Historical examples using old notation intentionally
   - "Before we changed S5a to S5.P1..." (intentional)

2. **Relative Paths:**
   - `../folder/file.md` depends on source file location
   - Requires resolving from each source file

3. **Internal Anchors:**
   - `[link](#section-name)` requires checking target file has section
   - Automated checking complex

4. **Semantic Correctness:**
   - Path exists BUT wrong stage referenced
   - "After S5 complete" but should be "After S6 complete"

### Manual Validation Process

**⚠️ CRITICAL: Always Check Root-Level Files First**

```bash
# Step 0: Validate root files (often skipped, high-impact if broken)
cd feature-updates/guides_v2
for file in README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md; do
  echo "Checking $file for broken references..."
  # Manual review - these files are entry points referenced in CLAUDE.md
done
```

```markdown
**For each reference found:**

STEP 1: Read context (5 lines before/after)
  ↓
STEP 2: Determine if error or intentional
  ├─> Error: Add to fix list
  └─> Intentional: Document as acceptable
      ↓
STEP 3: For errors, determine correct reference
  ↓
STEP 4: Verify replacement is correct
  ↓
STEP 5: Document fix
```markdown

---

## Context-Sensitive Rules

### Intentional Old References

**Acceptable in these contexts:**

**1. Historical Examples:**
```markdown
**Before restructuring:**
```
Old workflow: S5a → S5b → S5c
```text

**After restructuring:**
```text
New workflow: S5.P1 → S5.P2 → S5.P3
```text
```
**Verdict:** ✅ ACCEPTABLE (clearly marked as historical)

**2. Comparison/Migration Guides:**
```markdown
If you see references to "Stage 5a" in old epics:
- Old: Stage 5a
- New: S5.P1
```markdown
**Verdict:** ✅ ACCEPTABLE (teaching migration)

**3. Quoted Error Messages:**
```markdown
User reported: "Cannot find stages/s5/round1/file.md"
```
**Verdict:** ✅ ACCEPTABLE (quoting user input)

### Always Errors

**Never acceptable in these contexts:**

**1. Current Workflow Instructions:**
```markdown
Next, read stages/s5/round1/planning.md
```markdown
**Verdict:** ❌ ERROR (should be stages/s5/s5_p1_planning_round1.md)

**2. Prerequisites:**
```markdown
Before starting S5a, ensure S4 is complete
```
**Verdict:** ❌ ERROR (should be S5.P1 or S5)

**3. Navigation:**
```markdown
After completing this stage, proceed to S6a
```markdown
**Verdict:** ❌ ERROR (should be S6.P1 or S9 depending on context)

---

## Real Examples

### Example 1: After S6→S9 Renumbering

**Issue Found:**
```markdown
File: stages/s8/s8_p2_epic_testing_update.md
Line: 830
Content: "Read stages/s6/epic_smoke_testing.md"
```

**Analysis:**
- Context: Current workflow instruction (not historical)
- Stage 6 was renumbered to S9
- Epic smoke testing is S9.P1
- File was renamed: epic_smoke_testing.md → s9_p1_epic_smoke_testing.md

**Fix:**
```bash
sed -i 's|stages/s6/epic_smoke_testing\.md|stages/s9/s9_p1_epic_smoke_testing.md|g' \
  stages/s8/s8_p2_epic_testing_update.md
```bash

**Verification:**
```bash
# Check fix applied
grep -n "s9_p1_epic_smoke_testing" stages/s8/s8_p2_epic_testing_update.md

# Check file exists
ls stages/s9/s9_p1_epic_smoke_testing.md
```

### Example 2: Missing s#_ Prefix

**Issue Found:**
```markdown
File: stages/s10/s10_p1_guide_update_workflow.md
Line: 45
Content: "stages/s10/epic_cleanup.md"
```markdown

**Analysis:**
- File exists at: stages/s10/s10_epic_cleanup.md (with s10_ prefix)
- Reference missing prefix

**Fix:**
```bash
sed -i 's|stages/s10/epic_cleanup\.md|stages/s10/s10_epic_cleanup.md|g' \
  stages/s10/s10_p1_guide_update_workflow.md
```

### Example 3: Old Round Path Structure

**Issue Found:**
```markdown
File: stages/s5/s5_p1_planning_round1.md
Line: 155
Content: "READ: stages/s5/round1/iterations_1_3_requirements.md"
```diff

**Analysis:**
- Old structure: stages/s5/round1/
- New structure: stages/s5/s5_p1_i1_requirements.md
- Workflow was refactored, files reorganized

**Fix:**
```bash
sed -i 's|stages/s5/round1/iterations_1_3_requirements\.md|stages/s5/s5_p1_i1_requirements.md|g' \
  stages/s5/s5_p1_planning_round1.md
```

### Example 4: Root-Level File Reference (High Priority)

**Issue Found:**
```markdown
File: feature-updates/guides_v2/README.md
Line: 39
Content: "audit/README.md (modular audit system entry point)"
```diff

**Historical Context (Feb 2026):**
- The monolithic GUIDES_V2_FORMAL_AUDIT_GUIDE.md (30,568 tokens) was replaced by modular audit/ system
- Modular system location: audit/README.md, audit/audit_overview.md, audit/dimensions/, etc.
- Root-level files should now reference audit/README.md as the entry point

**Impact:**
- **CRITICAL** - README.md is main entry point (referenced in CLAUDE.md)
- Users/agents reading README get wrong information about audit system
- "Last Updated: 2025-12-30" is stale (over 1 month old)

**Fix:**
```bash
# Update README.md to reference new modular audit system
# Update "Last Updated" field to current date
# Remove or deprecate reference to old monolithic guide
```

**Why This Was Missed:**
- Original D1 validation only searched `guides_v2/stages/`
- Root-level files (README, EPIC_WORKFLOW_USAGE, prompts_reference) were not checked
- **High-impact gap** - these are entry point files

---

## See Also

**Next Dimension (Recommended Reading Order):**
- **D2: Terminology Consistency** - After fixing cross-references, verify paths use correct notation (e.g., "S5.P1" not "S5a")

**Related Dimensions (Coming Soon):**
- D3: Workflow Integration ⏳ - Prerequisites and transitions must match file paths
- D11: Structural Patterns ⏳ - Expected file structures validate reference targets exist

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to search for broken references
- `../stages/stage_4_verification.md` - Re-verify all paths after fixes

**Reference:**
- `../reference/verification_commands.md` - Validation scripts and patterns
- `../reference/context_analysis_guide.md` - Determining intentional vs error

---

**When to Use:** Run D1 validation after any file renaming, stage renumbering, or folder reorganization.
