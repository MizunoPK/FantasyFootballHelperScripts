# D11: Structural Patterns

**Dimension Number:** 11
**Category:** Structural Dimensions
**Automation Level:** 60% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-04

**Focus:** Ensure guides follow consistent structural patterns and template compliance
**Typical Issues Found:** 8-12 per audit

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Structural Issues Happen](#how-structural-issues-happen)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)

---

## What This Checks

**Structural Patterns** validates that guides follow consistent organizational patterns:

✅ **Required Sections:**
- Stage guides have Prerequisites, Overview, Exit Criteria
- Router files have Sub-Guide Table, Navigation
- Dimension guides have required metadata (Focus, Automation Level, etc.)

✅ **Section Ordering:**
- Prerequisites come before main content
- Exit Criteria at end before Next Stage
- Consistent order across similar files

✅ **Header Hierarchy:**
- Proper h2 (##) and h3 (###) nesting
- No skipping levels (h2 → h4)
- Single h1 (#) at top only

✅ **Template Compliance:**
- Stage guides match stage template structure
- Feature files match feature template structure
- Dimension guides match dimension template structure

✅ **Naming Conventions:**
- Files follow naming pattern: `s#_p#_i#_description.md`
- Folders follow pattern: `stages/s#/`
- Consistent underscore vs hyphen usage

---

## Why This Matters

### Impact of Structural Inconsistency

**Critical Impact:**
- **Agent Confusion:** Can't find expected sections (looks for Prerequisites, not in standard location)
- **Workflow Inefficiency:** Time wasted searching for information in non-standard structure
- **Template Propagation:** Inconsistent structure copied to new files
- **Maintainability:** Hard to update guides systematically if structure varies

**Example Failure (Hypothetical):**
```text
File: stages/s5/s5_p1_i1_requirements.md (follows standard structure)
Sections: Prerequisites → Overview → Steps → Exit Criteria

File: stages/s5/s5_p1_i2_algorithms.md (non-standard structure)
Sections: Overview → Steps → Prerequisites (at end) → No Exit Criteria

Agent: Reads i1, expects i2 to have same structure
Result: Starts reading steps before seeing prerequisites, misses context
```

### Benefits of Consistent Structure

**Agent Effectiveness:**
- Knows where to find information (Prerequisites always at top)
- Can skip to relevant sections quickly
- Reduced cognitive load (familiar pattern)

**Maintainability:**
- Easy to update all guides systematically
- Scripts can validate structure programmatically
- New guides follow established pattern

---

## Pattern Types

### Type 0: Root-Level File Structural Expectations

**Files with Expected Structure:**

**README.md:**
```markdown
# Title

**Metadata (Version, Last Updated, Purpose)**

## Quick Start

## What is v2 Workflow

## The 10 Stages

## Guide Index
```

**EPIC_WORKFLOW_USAGE.md:**
```markdown
# Title

## Setup Instructions

## Common Patterns

## Stage-by-Stage Detailed Workflows
  ### S1: Epic Planning
  ### S2: Feature Planning
  [S3-S10]
```

**Automated:** ⚠️ Partial (section presence automated, order manual)

### Type 1: Required Sections for Stage Guides

**Standard Pattern:**
```markdown
# Stage N.P#: [Name]

## Table of Contents

## Overview
**Purpose:**
**Duration:**
**Prerequisites:**
**Outputs:**

## [Main Content Sections]

## Critical Rules (or Key Principles)

## Exit Criteria (or Next Stage)

## See Also
```

**Validation:**
```bash
# Check for required sections
for file in stages/s*/*.md; do
  grep -q "## Prerequisites" "$file" || echo "MISSING Prerequisites: $file"
  grep -q "## Exit Criteria\|## Next" "$file" || echo "MISSING Exit Criteria: $file"
  grep -q "## Overview" "$file" || echo "MISSING Overview: $file"
done
```

**Automated:** ✅ Yes (CHECK 2 in pre_audit_checks.sh)

### Type 2: Router File Pattern

**Standard Router Pattern:**
```markdown
# [Stage/Phase Name] - Router

**Purpose:** Navigate to sub-guides for this [stage/phase]

## Sub-Guide Table

| Sub-Guide | File | Purpose | Reading Time |
|-----------|------|---------|--------------|
| ... | ... | ... | ... |

## Navigation

**If you are:**
- [Scenario 1] → Read [guide A]
- [Scenario 2] → Read [guide B]

## See Also
```

**Examples:**
- `stages/s5/s5_p1_planning_round1.md` (router to I1, I2, I3)
- `stages/s2/s2_feature_deep_dive.md` (router to P1, P2, P3)

**Validation:**
```bash
# Router files should have Sub-Guide Table or Navigation
for file in $(grep -l "router\|Router" stages/*/*.md); do
  if ! grep -q "## Sub-Guide Table\|## Navigation" "$file"; then
    echo "Router missing navigation: $file"
  fi
done
```

**Automated:** ⚠️ Partial (pattern detection possible)

### Type 3: File Naming Conventions

**Standard Patterns:**

**Stage guides:**
```text
s#_stage_name.md          (e.g., s1_epic_planning.md)
s#_p#_phase_name.md       (e.g., s2_p1_research.md)
s#_p#_i#_iteration_name.md (e.g., s5_p1_i1_requirements.md)
```

**Reference files:**
```text
reference/category/description.md
reference/stage_#/stage_reference_card.md
```

**Templates:**
```text
templates/type_name_template.md
```

**Validation:**
```bash
# Find files not following naming convention in stages/
find stages -name "*.md" | grep -v "s[0-9]_" | grep -v "README.md"
# Should return minimal results

# Check for hyphens instead of underscores
find stages -name "*-*-*.md"
# Should return no results (underscores preferred)
```

**Automated:** ✅ Yes (pattern matching with find)

### Type 4: Header Hierarchy

**Standard Hierarchy:**
```markdown
# Title (h1 - once only at top)

## Major Section (h2)

### Subsection (h3)

#### Detail (h4 - rare, only if needed)
```

**Anti-Pattern:**
```markdown
# Title

### Subsection (ERROR: skipped h2)

#### Detail (ERROR: skipped from h1 to h4)
```

**Validation:**
```bash
# Find files with h4 or deeper (check if appropriate)
grep -rn "^####" stages/ | wc -l
# High count may indicate over-nesting

# Find files with multiple h1
grep -rn "^# " stages/*.md | awk -F: '{print $1}' | uniq -c | awk '$1 > 1'
# Should return nothing (one h1 per file)
```

**Automated:** ✅ Yes (regex pattern matching)

### Type 5: Section Ordering

**Standard Order for Stage Guides:**
```text
1. Title
2. Metadata (if applicable)
3. Table of Contents
4. Overview (Purpose, Duration, Prerequisites, Outputs)
5. Main Content
6. Critical Rules / Key Principles
7. Exit Criteria / Next Stage
8. See Also
```

**Anti-Pattern:**
```text
1. Title
2. Main Content (ERROR: jumped into content before prerequisites)
3. Prerequisites (ERROR: too late)
4. Overview (ERROR: should be at top)
```

**Validation:** Manual (order checking requires understanding section purpose)

**Automated:** ❌ No (requires semantic understanding)

---

## How Structural Issues Happen

### Root Cause 1: Copy-Paste Without Adjustment

**Scenario:** Create new guide by copying existing guide

**What Happens:**
```bash
# Copy s5_p1_i1 to create s5_p1_i2
cp s5_p1_i1_requirements.md s5_p1_i2_algorithms.md

# Edit content but forget to update section order
# Result: i2 has i1's structure even though content is different
```

**Why It Happens:**
- Focus on content changes, not structure review
- Assume copied structure is appropriate
- Don't verify structure matches intended purpose

### Root Cause 2: Incremental Additions Without Reordering

**Scenario:** Guide evolves over time, sections added ad-hoc

**Evolution:**
```markdown
# Version 1 (basic)
## Overview
## Steps

# Version 2 (add prerequisites)
## Overview
## Steps
## Prerequisites (ERROR: added at end instead of top)

# Version 3 (add exit criteria)
## Overview
## Steps
## Prerequisites
## Critical Rules (ERROR: between Prerequisites and Exit Criteria)
## Exit Criteria
```

**Result:** Sections in random order, not standard pattern

### Root Cause 3: Template Drift

**Scenario:** Template updated, existing files not refactored

**2025-11 Template:**
```markdown
## Overview
Purpose: ...
Prerequisites: ...
```

**2026-01 Template Update:**
```markdown
## Overview
**Purpose:** ...
**Duration:** ... (NEW)
**Prerequisites:** ...
**Outputs:** ... (NEW)
```

**Problem:** Existing guides still use old format

### Root Cause 4: Special Case Becomes Standard

**Scenario:** One-off structural deviation copied to other files

**File A (intentional deviation):**
```markdown
# Router File (intentional special structure)
## Navigation Table
## See Also
```

**File B (copied A, but shouldn't be router):**
```markdown
# Regular Guide (ERROR: using router structure)
## Navigation Table (ERROR: not a router)
## See Also
# Missing Prerequisites, Exit Criteria
```

---

## Automated Validation

### Script 1: Required Sections Validation (IN pre_audit_checks.sh)

```bash
# CHECK 2: Structure Validation (D11)
# ============================================================================

echo "=== Structure Validation (D11) ==="

MISSING_PREREQ=0
MISSING_EXIT=0

required_sections=("Prerequisites" "Exit Criteria" "Overview")

for file in stages/*/*.md; do
  # Skip router files (they have different structure)
  if grep -q "## Sub-Guide Table\|## Navigation" "$file"; then
    continue
  fi

  for section in "${required_sections[@]}"; do
    if ! grep -qi "^## $section\|^### $section" "$file"; then
      echo "❌ MISSING $section: $file"

      if [ "$section" == "Prerequisites" ]; then
        ((MISSING_PREREQ++))
      elif [ "$section" == "Exit Criteria" ]; then
        ((MISSING_EXIT++))
      fi
    fi
  done
done

echo "Missing Prerequisites: $MISSING_PREREQ"
echo "Missing Exit Criteria: $MISSING_EXIT"
```

### Script 2: Naming Convention Validation (SHOULD ADD)

```bash
# CHECK 2b: File Naming Conventions (D11)
# ============================================================================

echo "=== File Naming Convention Validation ==="

# Check stage files follow s#_* pattern
WRONGLY_NAMED=$(find stages -name "*.md" ! -name "s[0-9]*" ! -name "README.md" | wc -l)

if [ "$WRONGLY_NAMED" -gt 0 ]; then
  echo "⚠️  Files not following s#_* pattern:"
  find stages -name "*.md" ! -name "s[0-9]*" ! -name "README.md"
fi

# Check for hyphens instead of underscores
HYPHENATED=$(find stages -name "*-*-*.md" | wc -l)

if [ "$HYPHENATED" -gt 0 ]; then
  echo "⚠️  Files using hyphens instead of underscores:"
  find stages -name "*-*-*.md"
fi

# Check template files end with _template.md
WRONG_TEMPLATES=$(find templates -name "*.md" ! -name "*_template.md" ! -name "README.md" ! -name "*.txt" | wc -l)

if [ "$WRONG_TEMPLATES" -gt 0 ]; then
  echo "⚠️  Template files not ending with _template.md:"
  find templates -name "*.md" ! -name "*_template.md" ! -name "README.md"
fi
```

### Script 3: Header Hierarchy Validation (SHOULD ADD)

```bash
# CHECK 2c: Header Hierarchy Validation (D11)
# ============================================================================

echo "=== Header Hierarchy Validation ==="

# Find files with multiple h1 headers
MULTI_H1=$(grep -rl "^# " stages/ | while read file; do
  count=$(grep -c "^# " "$file")
  if [ "$count" -gt 1 ]; then
    echo "$file has $count h1 headers"
  fi
done | wc -l)

if [ "$MULTI_H1" -gt 0 ]; then
  echo "⚠️  Files with multiple h1 headers: $MULTI_H1"
fi

# Find excessive nesting (h5 or deeper)
DEEP_NESTING=$(grep -rn "^#####" stages/ | wc -l)

if [ "$DEEP_NESTING" -gt 0 ]; then
  echo "⚠️  Instances of h5 or deeper nesting: $DEEP_NESTING"
  echo "   (May indicate over-nesting, consider restructuring)"
fi
```

---

## Manual Validation

### Manual Structural Review Process

**For each stage guide:**

```markdown
STEP 1: Check section presence and order
- [ ] Title (h1) at top
- [ ] Table of Contents (if file >300 lines)
- [ ] Overview section (with Purpose, Duration, Prerequisites, Outputs)
- [ ] Main content sections
- [ ] Critical Rules or Key Principles
- [ ] Exit Criteria or Next Stage
- [ ] See Also

STEP 2: Verify section completeness
- Prerequisites lists what must be done before
- Overview explains purpose clearly
- Exit Criteria defines when stage is complete
- See Also provides navigation to related content

STEP 3: Check header hierarchy
- One h1 only (title)
- h2 for major sections
- h3 for subsections (if needed)
- No skipping levels (h2 → h4)

STEP 4: Compare to template
- Does structure match template for this guide type?
- Are any required sections missing?
- Are sections in standard order?

STEP 5: Document deviations
- If structure differs, is it intentional? (router files)
- If intentional, is it documented? (comment at top)
- If unintentional, add to fix list
```

**For router files:**

```markdown
STEP 1: Verify router pattern
- [ ] File clearly marked as router (in title or at top)
- [ ] Sub-Guide Table present (lists all sub-guides)
- [ ] Navigation section present (guides user to correct file)
- [ ] See Also section (links back to parent)

STEP 2: Check sub-guide references
- All sub-guides listed exist
- Table includes: name, file path, purpose, reading time
- Navigation section provides clear decision tree

STEP 3: Verify router doesn't have regular guide sections
- Router should NOT have Prerequisites (sub-guides have those)
- Router should NOT have Exit Criteria (sub-guides have those)
- Router is navigation only
```

---

## Context-Sensitive Rules

### When Structural Deviations Are Acceptable

**1. Router Files (Intentional Special Structure):**
```markdown
File: stages/s5/s5_p1_planning_round1.md
Structure: Sub-Guide Table, Navigation (no Prerequisites)
Verdict: ✅ ACCEPTABLE (router pattern)
```

**2. Reference Files (List Structure):**
```markdown
File: reference/glossary.md
Structure: Alphabetical term list (no Prerequisites/Exit Criteria)
Verdict: ✅ ACCEPTABLE (reference material, not sequential guide)
```

**3. Templates (Example Structure):**
```markdown
File: templates/feature_spec_template.md
Structure: Template sections with placeholder text
Verdict: ✅ ACCEPTABLE (template, not actual guide)
```

### When Structural Deviations Are Errors

**1. Regular Guide Missing Required Sections:**
```markdown
File: stages/s7/s7_p2_qc_rounds.md (regular guide)
Structure: Overview, Steps, See Also (MISSING Prerequisites and Exit Criteria)
Verdict: ❌ ERROR (not a router, must have all required sections)
```

**2. File Name Doesn't Match Convention:**
```markdown
File: stages/s5/planning-round-1.md (ERROR: hyphens instead of underscores)
Should be: stages/s5/s5_p1_planning_round1.md
Verdict: ❌ ERROR (violates naming convention)
```

**3. Multiple h1 Headers:**
```markdown
File: stages/s1/s1_epic_planning.md

# Stage 1: Epic Planning

[content]

# Discovery Phase (ERROR: second h1)
```
**Verdict:** ❌ ERROR (should be h2: ## Discovery Phase)

---

## Real Examples

### Example 1: Missing Prerequisites Section

**Issue Found:**
```bash
$ grep -l "## Prerequisites" stages/s7/s7_p2_qc_rounds.md

[No results - section missing]
```

**Analysis:**
- File is regular stage guide (not router)
- Missing Prerequisites section
- Agents don't know what must be complete before starting

**Impact:** ⚠️ MEDIUM - Reduces clarity, not blocking

**Fix:**
```markdown
## Prerequisites

**Required:**
- S7.P1 Smoke Testing complete and passed
- All smoke test failures resolved
- implementation_checklist.md fully checked off

**Before Starting QC Rounds:**
- Commit your latest changes
- Clean working directory
- Tests passing locally
```

### Example 2: Wrong File Naming Convention

**Issue Found:**
```bash
$ find stages -name "*-*-*.md"
stages/s5/planning-round-1.md
stages/s5/planning-round-2.md
```

**Analysis:**
- Files use hyphens instead of underscores
- Doesn't match convention: `s#_p#_description.md`
- May cause grep pattern failures

**Impact:** ⚠️ LOW - Cosmetic, but violates consistency

**Fix:**
```bash
git mv stages/s5/planning-round-1.md stages/s5/s5_p1_planning_round1.md
git mv stages/s5/planning-round-2.md stages/s5/s5_p2_planning_round2.md

# Update all references
sed -i 's|planning-round-1\.md|s5_p1_planning_round1.md|g' stages/**/*.md
sed -i 's|planning-round-2\.md|s5_p2_planning_round2.md|g' stages/**/*.md
```

### Example 3: Sections in Wrong Order

**Issue Found:**
```markdown
File: stages/s5/s5_p1_i3_integration.md

# S5.P1.I3: Integration Planning

## Overview
Purpose: ...

## Steps
[15 detailed steps]

## Prerequisites (ERROR: Should be before Steps)
- S5.P1.I2 complete
- Algorithms documented

## Exit Criteria
...
```

**Analysis:**
- Prerequisites section after Steps section
- Violates standard order (Prerequisites should be in Overview or right after)
- Agent may start Steps before seeing prerequisites

**Impact:** ⚠️ MEDIUM - Structural inconsistency, potential confusion

**Fix:**
```markdown
# S5.P1.I3: Integration Planning

## Overview
**Purpose:** ...
**Duration:** ...
**Prerequisites:**
- S5.P1.I2 complete
- Algorithms documented
**Outputs:** ...

## Steps
[15 detailed steps]

## Exit Criteria
...
```

### Example 4: Router File Misidentified as Regular Guide

**Issue Found:**
```bash
$ grep -l "Sub-Guide Table" stages/s2/s2_feature_deep_dive.md
stages/s2/s2_feature_deep_dive.md

# File has Sub-Guide Table (router pattern)
# But automated check flagged it as missing Prerequisites

$ grep "## Prerequisites" stages/s2/s2_feature_deep_dive.md
[No results]
```

**Analysis:**
- File is actually a router (has Sub-Guide Table)
- Automated script didn't detect router pattern correctly
- False positive: router files don't need Prerequisites

**Impact:** ❌ False positive in automation

**Fix to Automation:**
```bash
# Update CHECK 2 in pre_audit_checks.sh
# Skip files with router indicators

for file in stages/*/*.md; do
  # Skip router files (they have different structure)
  if grep -q "## Sub-Guide Table\|## Navigation\|router" "$file"; then
    continue
  fi

  # Check regular guides for required sections
  [validation logic]
done
```

---

## Integration with Other Dimensions

**Works With:**
- **D13: Documentation Quality** - Required sections overlap
- **D1: Cross-Reference Accuracy** - File naming affects path validation

**Complementary:**
- **D6: Template Currency** (not implemented) - Template compliance validation
- **D9: Intra-File Consistency** (not implemented) - Section content quality

---

## See Also

**Related Dimensions:**
- `d1_cross_reference_accuracy.md` - File path and naming validation
- `d13_documentation_quality.md` - Required sections overlap

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to discover structural issues
- `../stages/stage_4_verification.md` - Re-verify structure after fixes

**Templates:**
- `../templates/` - Reference for structural patterns

**Scripts:**
- `../scripts/pre_audit_checks.sh` - Automated structure validation (CHECK 2)

---

**When to Use:** Run D11 validation after any template changes, file reorganization, or when creating new guides to ensure structural consistency.
