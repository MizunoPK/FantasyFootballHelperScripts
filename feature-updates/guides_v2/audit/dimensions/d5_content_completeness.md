# D5: Content Completeness

**Dimension Number:** 5
**Category:** Content Quality Dimensions
**Automation Level:** 85% automated
**Priority:** HIGH
**Last Updated:** 2026-02-04

**Focus:** Ensure all required content is present, complete, and not stubbed out
**Typical Issues Found:** 10-15 per audit

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Incomplete Content Happens](#how-incomplete-content-happens)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)

---

## What This Checks

**Content Completeness** validates that all required content exists and is substantive:

✅ **Required Sections Present:**
- All expected sections exist (not just mentioned in TOC)
- Sections have content (not empty or stub)
- Cross-referenced sections actually exist

✅ **No Stub Content:**
- Sections have >3 lines of meaningful content
- No "TODO: Fill this in" or similar placeholders
- No "Coming Soon" or "⏳" markers in published content
- No sections with just bullets and no explanatory text

✅ **Examples and References Complete:**
- Promised examples actually provided
- "See below" has content below
- "See section X" - section X exists
- All checklist items explained

✅ **Template Fields Filled:**
- Templates don't have [placeholder] text
- Required template sections completed
- No <fill in> or similar markers

✅ **Root-Level File Completeness:**
- README.md has all announced sections
- EPIC_WORKFLOW_USAGE.md has S1-S10 details
- prompts_reference_v2.md has all stage prompts
- No sections announced in TOC but missing in body

---

## Why This Matters

### Impact of Incomplete Content

**Critical Impact:**
- **Workflow Blocked:** Missing prerequisites prevents agents from knowing what to do first
- **Agent Confusion:** Stub sections leave critical questions unanswered
- **Circular References:** "See section X" but section X is stub
- **Template Unusable:** Placeholders in templates copied to actual files

**Example Failure (Hypothetical):**
```markdown
Guide: stages/s5/s5_p3_i2_gates_part1.md

## Gate 23a: Pre-Implementation Spec Audit

**Purpose:** Validate planning completeness before implementation

**Checklist:**
Coming soon - will add after testing this workflow

**Impact:** Agent reaches Gate 23a, no checklist to validate against, proceeds without validation
**Result:** Implementation starts with incomplete planning (historical: 60% rework rate)
```

### Completeness vs Quality

**D5 (Content Completeness):** Is content PRESENT?
- Section exists in file
- Section has substantive content (not stub)
- Promised content delivered

**D13 (Documentation Quality):** Does present content meet STANDARDS?
- Formatting quality
- Example quality
- Code block language tags
- TODO markers

**Overlap:** Both check for TODOs, but D5 focuses on "missing content" while D13 focuses on "quality of present content"

---

## Pattern Types

### Type 0: Root-Level File Section Completeness

**Critical Files:**
```text
README.md
EPIC_WORKFLOW_USAGE.md
prompts_reference_v2.md
audit/README.md
```

**What to Check:**

**README.md:**
- [ ] Quick Start section has actual quick start steps (not just "See guides")
- [ ] 10 Stages overview describes all 10 stages (not placeholder for S8-S10)
- [ ] Guide Index lists all guide categories
- [ ] Last Updated is recent

**EPIC_WORKFLOW_USAGE.md:**
- [ ] Stage-by-Stage section has details for ALL stages (S1-S10)
- [ ] Each stage has: phases, iterations, duration, gates
- [ ] No "Coming Soon" for any stage

**prompts_reference_v2.md:**
- [ ] All 10 stage prompts present
- [ ] Debugging protocol prompt present
- [ ] Missed requirement prompt present
- [ ] Special workflow prompts present

**Search Commands:**
```bash
# Check README.md for incomplete sections
grep -A 5 "## Quick Start" README.md | grep -i "coming soon\|todo\|⏳"

# Check EPIC_WORKFLOW_USAGE for missing stage sections
for stage in {1..10}; do
  grep -q "### S$stage:" EPIC_WORKFLOW_USAGE.md || echo "Missing S$stage details"
done

# Check prompts_reference for missing prompts
for stage in {1..10}; do
  grep -q "Starting S$stage" prompts_reference_v2.md || echo "Missing S$stage prompt"
done
```markdown

**Automated:** ⚠️ Partial (section presence automated, content depth manual)

### Type 1: Empty or Near-Empty Sections

**Pattern:**
```markdown
## Prerequisites

[None]

## Examples

TBD

## Critical Rules

[To be added]
```text

**What Makes Section "Empty":**
- Section header exists
- Content is ≤3 lines
- Content is placeholder text (TBD, TODO, Coming Soon, etc.)
- No substantive information provided

**Search Commands:**
```bash
# Find sections with common placeholder patterns
grep -A 3 "^## " stages/**/*.md | grep -B 1 "TBD\|TODO\|Coming Soon\|\[None\]\|\[To be added\]"

# Find very short sections (may indicate stub)
# (Requires manual script - check section length)
```markdown

**Automated:** ✅ Yes (placeholder detection), ⚠️ Partial (short section detection)

### Type 2: Promised Content Not Delivered

**Patterns:**

**"See below" with no content below:**
```markdown
## Overview
For detailed steps, see below.

## Next Stage
[No "detailed steps" section exists]
```text

**"See examples" with no examples:**
```markdown
## Creating Spec
Follow template structure. See examples in Appendix A.

[No Appendix A in file]
```text

**Forward reference to missing section:**
```markdown
We'll cover prerequisites in the Prerequisites section.

[No Prerequisites section in file]
```text

**Search Commands:**
```bash
# Find "see below" or "see section" references
grep -in "see below\|see section\|see.*examples\|see appendix" stages/**/*.md

# Manually verify referenced content exists
```bash

**Automated:** ⚠️ Partial (can find promises, manual to verify delivery)

### Type 3: TOC Entries Without Corresponding Sections

**Pattern:**
```markdown
## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Examples](#examples)
4. [Next Steps](#next-steps)

## Overview
[content]

## Prerequisites
[content]

[MISSING: Examples section]
[MISSING: Next Steps section]
```text

**Search Commands:**
```bash
# Extract TOC links
grep -A 50 "## Table of Contents" file.md | grep -o "\](#[^)]*)" | sed 's/](#//; s/)//'

# For each TOC link, verify section exists
# (Requires script to parse and validate)
```markdown

**Automated:** ✅ Yes (can extract TOC and check section existence)

### Type 4: Template Placeholders in Published Files

**Pattern:**
```markdown
# Actual guide file (NOT template)

## Purpose
[Describe the purpose of this stage]

## Duration
<fill in estimated time>

## Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]
```text

**Why This is Wrong:**
- File is published guide (not template)
- Contains template placeholder text
- Indicates file created from template but not filled in

**Search Commands:**
```bash
# Find template placeholder patterns in non-template files
grep -rn "\[Describe\|<fill in\|\[Prerequisite\|\[Step\|\[Example" stages/ | grep -v "_template.md"

# Should return minimal results (only in intentional examples)
```markdown

**Automated:** ✅ Yes (pattern matching)

### Type 5: Checklist Items Without Explanations

**Pattern:**
```markdown
## Gate 23a Checklist

**Part 1: Requirements Completeness**
- [ ] All spec.md requirements have implementation steps
- [ ] All checklist.md items addressed
- [ ] Edge cases covered

[No explanation of HOW to verify each item]
```text

**What's Missing:**
- Checklist items listed
- But no guidance on HOW to verify each item
- No examples of what "passing" looks like

**Better:**
```markdown
## Gate 23a Checklist

**Part 1: Requirements Completeness**

**Item 1: All spec.md requirements have implementation steps**
- What to check: Open spec.md, extract each requirement
- Validation: Search implementation_plan.md for each requirement
- Pass criteria: Every spec requirement has 1+ corresponding step

[Repeat for each checklist item]
```markdown

**Automated:** ❌ No (requires content understanding)

---

## How Incomplete Content Happens

### Root Cause 1: Rapid Scaffolding Without Filling In

**Scenario:** Create file structure quickly, plan to fill in later

**What Happens:**
```markdown
# Day 1: Create structure
## Overview
TODO

## Prerequisites
TBD

## Steps
Coming soon

# Day 2-10: Work on other files
[Original file forgotten]

# Day 11: Audit finds incomplete sections
```text

**Why It Happens:**
- Focus on creating files, not completing them
- "I'll come back and fill this in" never happens
- No validation that sections are complete

**Prevention:**
- Don't create sections until ready to fill them
- If section created, mark file as DRAFT
- Automated check for placeholder text

### Root Cause 2: Content Moved, Reference Not Updated

**Scenario:** Section extracted to separate file, original reference remains

**Before refactoring:**
```markdown
# s5_planning.md (monolithic file)

## Examples
[10 detailed examples]
```text

**After refactoring:**
```markdown
# s5_p1_planning_round1.md (new file)

## Creating Plan
See examples below.

[Examples extracted to reference/stage_5/examples.md]
[Reference not updated to point to new location]
```markdown

**Result:** "See examples below" but examples not present

### Root Cause 3: TOC Created First, Sections Never Added

**Scenario:** Generate TOC based on planned structure, never create sections

**What Happens:**
```markdown
## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Advanced Topics](#advanced-topics)  ← Planned but never added
4. [Troubleshooting](#troubleshooting)     ← Planned but never added

## Overview
[content]

## Prerequisites
[content]

[Missing: Advanced Topics, Troubleshooting]
```text

**Why It Happens:**
- TOC created as roadmap, not all sections implemented
- Time ran out before completing all planned sections
- No validation that TOC matches actual sections

### Root Cause 4: Template Copied But Not Customized

**Scenario:** Copy template to create new file, forget to fill in

**What Happens:**
```bash
# Copy template
cp templates/feature_spec_template.md feature_01_name/spec.md

# Edit title, but forget to fill in [placeholder] fields
# Result: Published file has template placeholders
```text

**Why It Happens:**
- Quick copy-paste workflow
- Focus on new content, skip template fields
- No automated check for template markers in published files

---

## Automated Validation

### Script 1: Placeholder Text Detection (SHOULD ADD to pre_audit_checks.sh)

```bash
# CHECK: Content Completeness - Placeholder Detection (D5)
# ============================================================================

echo "=== Content Completeness - Placeholder Detection (D5) ==="

# Find template placeholders in non-template files
PLACEHOLDERS=$(grep -rn "\[Describe\|<fill in\|\[Prerequisite\|\[Step\|\[Example\|Coming Soon\|⏳" \
  stages/ reference/ prompts/ 2>/dev/null | \
  grep -v "_template.md" | \
  grep -v "historical\|before\|example of wrong" | \
  wc -l)

if [ "$PLACEHOLDERS" -gt 0 ]; then
  echo "⚠️  Placeholder text found in published files: $PLACEHOLDERS instances"
  grep -rn "\[Describe\|<fill in\|\[Prerequisite\|\[Step" stages/ 2>/dev/null | \
    grep -v "_template.md" | head -10
else
  echo "✅ No placeholder text in published files"
fi

# Find "Coming Soon" markers
COMING_SOON=$(grep -rn "Coming Soon\|⏳" stages/ reference/ prompts/ 2>/dev/null | \
  grep -v "historical" | wc -l)

if [ "$COMING_SOON" -gt 0 ]; then
  echo "⚠️  'Coming Soon' markers found: $COMING_SOON instances"
  grep -rn "Coming Soon\|⏳" stages/ 2>/dev/null | head -5
fi
```markdown

### Script 2: TOC vs Section Validation (SHOULD ADD)

```bash
# CHECK: Content Completeness - TOC Validation (D5)
# ============================================================================

echo "=== TOC vs Section Validation ==="

# For files with TOC, verify all linked sections exist
# (This is a simplified version - full implementation would parse markdown)

for file in $(grep -l "## Table of Contents" stages/**/*.md); do
  echo "Checking $file..."

  # Extract section anchors from TOC
  # Compare with actual section headers
  # Report missing sections

  # Simplified: count TOC entries vs actual sections
  toc_entries=$(grep -A 50 "## Table of Contents" "$file" | grep "](#" | wc -l)
  sections=$(grep -c "^## " "$file")

  if [ "$toc_entries" -gt "$sections" ]; then
    echo "  ⚠️  $file: TOC has $toc_entries entries but file has $sections sections"
  fi
done
```markdown

### Script 3: Empty Section Detection (SHOULD ADD)

```bash
# CHECK: Content Completeness - Empty Sections (D5)
# ============================================================================

echo "=== Empty Section Detection ==="

# Find sections followed immediately by another section (empty content)
EMPTY_SECTIONS=$(grep -A 1 "^## " stages/**/*.md | \
  grep -B 1 "^## " | \
  grep "^## " | \
  wc -l)

if [ "$EMPTY_SECTIONS" -gt 0 ]; then
  echo "⚠️  Potentially empty sections: $EMPTY_SECTIONS"
  echo "   (Sections immediately followed by another section - may be empty)"
fi

# Find very short sections (< 3 lines of content)
# (Requires more sophisticated parsing)
```markdown

### Script 4: Root File Completeness Check (SHOULD ADD)

```bash
# CHECK: Content Completeness - Root Files (D5)
# ============================================================================

echo "=== Root File Completeness Check ==="

# Check EPIC_WORKFLOW_USAGE.md has all 10 stages
for stage in {1..10}; do
  if ! grep -q "### S$stage:" EPIC_WORKFLOW_USAGE.md; then
    echo "⚠️  EPIC_WORKFLOW_USAGE.md missing S$stage section"
  fi
done

# Check prompts_reference_v2.md has all stage prompts
for stage in {1..10}; do
  if ! grep -q "Starting S$stage" prompts_reference_v2.md; then
    echo "⚠️  prompts_reference_v2.md missing S$stage prompt"
  fi
done

# Check README.md has announced sections
for section in "Quick Start" "The 10 Stages" "Guide Index"; do
  if ! grep -q "## $section" README.md; then
    echo "⚠️  README.md missing section: $section"
  fi
done
```markdown

---

## Manual Validation

### ⚠️ CRITICAL: Root-Level File Content Depth Review

**Mandatory deep completeness check:**

```markdown
STEP 0: Verify root files have COMPLETE content (not stubs)

For README.md:
- [ ] Quick Start has actual steps (not "see guides")
- [ ] 10 Stages section describes all 10 (not just S1-S5)
- [ ] Guide Index lists all categories (stages, reference, templates, etc.)
- [ ] No "Coming Soon" or "⏳" in any section

For EPIC_WORKFLOW_USAGE.md:
- [ ] Stage-by-Stage has complete details for S1-S10
- [ ] Each stage section has: overview, phases, iterations, duration, gates
- [ ] No placeholders or incomplete stage sections

For prompts_reference_v2.md:
- [ ] All 10 stage prompts present
- [ ] All special workflow prompts present (debugging, missed requirement)
- [ ] Each prompt has: full text, when to use, expected outcome
```markdown

### Manual Validation Process

**For each guide file:**

```markdown
STEP 1: Check all sections have substantive content
- Read each section header
- Verify section has >3 lines of meaningful content
- Check for placeholder patterns (TBD, TODO, Coming Soon, ⏳)

STEP 2: Verify TOC matches actual sections
- If file has TOC, extract all linked sections
- For each TOC entry, verify section exists in file
- Check section has content (not just header)

STEP 3: Validate forward references
- Search for "see below", "see section X", "see examples"
- For each reference, verify content actually exists
- No circular references (Section A says see B, B says see A)

STEP 4: Check promised content delivered
- Look for phrases like "we'll cover", "discussed later", "see appendix"
- Verify promised content exists in file or referenced file
- No broken promises

STEP 5: Validate checklists and procedures
- Checklist items have explanations (HOW to verify)
- Procedures have all steps (not just steps 1, 2, 5)
- Examples are complete (not "example coming soon")

STEP 6: Document incomplete content
- List sections that are stubs
- Note missing promised content
- Identify template placeholders in published files
- Add to discovery report with severity
```text

**For templates:**

```markdown
STEP 1: Verify template completeness
- Template has all expected sections for its type
- Placeholder text is HELPFUL (not just [fill in])
- Examples show realistic values

STEP 2: Check template is not stub
- Template provides guidance on what to include
- Not just empty section headers
- Has explanatory text for each section

STEP 3: Validate against actual usage
- Compare template to actual files created from it
- Verify template has all sections users need
- Check template isn't missing sections users had to add
```markdown

---

## Context-Sensitive Rules

### When Incomplete Content is Acceptable

**1. Intentionally Brief Sections:**
```markdown
## Prerequisites

None - this is the first stage.
```text
**Verdict:** ✅ ACCEPTABLE (brief but complete answer)

**2. Forward References to Separate Files:**
```markdown
## Examples

See `reference/stage_5/specification_examples.md` for detailed examples.
```text
**Verdict:** ✅ ACCEPTABLE (content exists in referenced file)

**3. Work in Progress Clearly Marked:**
```markdown
File: _internal/DRAFT_new_dimension.md (clearly marked as draft)

## Section 3
Coming Soon
```markdown
**Verdict:** ✅ ACCEPTABLE (draft file, not published)

### When Incomplete Content is Error

**1. Stub Sections in Published Guides:**
```markdown
File: stages/s5/s5_p3_i2_gates_part1.md (published guide)

## Gate 23a Checklist
Coming Soon
```text
**Verdict:** ❌ ERROR (published guide, critical section incomplete)

**2. Template Placeholders in Actual Files:**
```markdown
File: feature_01_name/spec.md (actual feature spec, not template)

## Purpose
[Describe the purpose of this feature]
```text
**Verdict:** ❌ ERROR (should be filled in, not placeholder)

**3. TOC Entries Without Sections:**
```markdown
File: stages/s1/s1_epic_planning.md

## Table of Contents
1. [Overview](#overview)
2. [Discovery Phase](#discovery-phase)

## Overview
[content]

[Missing: Discovery Phase section]
```text
**Verdict:** ❌ ERROR (TOC promises section that doesn't exist)

**4. Broken Forward References:**
```markdown
## Creating Spec
Follow template. See examples below.

## Next Steps
[No examples section]
```markdown
**Verdict:** ❌ ERROR (promised "examples below" but not delivered)

---

## Real Examples

### Example 1: TOC Entry Without Corresponding Section

**Issue Found:**
```markdown
File: stages/s5/s5_p1_planning_round1.md

## Table of Contents

1. [Overview](#overview)
2. [I1: Requirements](#i1-requirements)
3. [I2: Algorithms](#i2-algorithms)
4. [I3: Integration](#i3-integration)
5. [Validation Loop](#validation-loop)
6. [Troubleshooting](#troubleshooting)  ← Missing in file

[File has sections 1-5 but no Troubleshooting section]
```text

**Analysis:**
- TOC lists 6 sections
- File only has 5 sections
- "Troubleshooting" section planned but never added
- Clicking TOC link leads nowhere

**Impact:** ⚠️ MEDIUM - Broken navigation, missing potentially useful content

**Fix:**
```markdown
# Option 1: Add the missing section
## Troubleshooting

**Common Issues:**
- [Add troubleshooting content]

# Option 2: Remove from TOC if not needed
[Delete Troubleshooting TOC entry]
```markdown

### Example 2: Stub Section in Critical Location

**Issue Found:**
```markdown
File: stages/s5/s5_p3_i2_gates_part1.md

## Gate 23a: Pre-Implementation Spec Audit

**Purpose:** Validate planning completeness before S6

**Checklist:**
Coming Soon - will add after testing this gate in practice

## Next
Continue to [Gate 24](s5_p3_i3_gates_part2.md)
```text

**Analysis:**
- Gate 23a is critical validation point
- Checklist is stub ("Coming Soon")
- Agents cannot validate planning without checklist
- Workflow effectively broken at this gate

**Impact:** ❌ CRITICAL - Blocks workflow progression

**Fix:**
```markdown
## Gate 23a: Pre-Implementation Spec Audit

**Purpose:** Validate planning completeness before S6

**Checklist:**

**Part 1: Requirements Completeness**
- [ ] All spec.md requirements have implementation steps
- [ ] All checklist.md questions resolved
- [ ] Edge cases from test_strategy.md covered

**Part 2: Algorithm Detail**
[Complete 5-part checklist]
```markdown

### Example 3: Template Placeholder in Published File

**Issue Found:**
```bash
$ grep -rn "\[Describe the purpose" feature_01_player_fetcher/spec.md
feature_01_player_fetcher/spec.md:8:[Describe the purpose of this feature]
```text

**Analysis:**
- File is actual feature spec (not template)
- Contains template placeholder text
- Spec created by copying template but not filled in
- Purpose section is critical but empty

**Impact:** ❌ HIGH - Core section incomplete in published file

**Fix:**
```markdown
# Before
## Purpose
[Describe the purpose of this feature]

# After
## Purpose
Enable users to fetch player data from ESPN API with configurable
date ranges and data types (stats, projections, rankings).
```markdown

### Example 4: Forward Reference Without Content

**Issue Found:**
```markdown
File: stages/s2/s2_p1_spec_creation_refinement.md

## Creating Feature Spec

Follow the template structure. For detailed examples of each section,
see the Examples appendix at the end of this guide.

[Rest of guide content]

## See Also
- [S2.P2 Specification](s2_p2_specification.md)

[No Examples appendix in file]
```bash

**Analysis:**
- Guide promises "Examples appendix at the end of this guide"
- Appendix does not exist in file
- Agents expecting examples will not find them

**Impact:** ⚠️ MEDIUM - Missing helpful content, not blocking

**Fix:**
```markdown
# Option 1: Add the promised appendix
## Appendix: Examples

### Example 1: Simple Feature Spec
[Add examples]

# Option 2: Update reference to point to correct location
For detailed examples of each section,
see `reference/stage_2/specification_examples.md`.

# Option 3: Remove the promise if examples not ready
Follow the template structure.
```markdown

### Example 5: Root File Missing Stage Details

**Issue Found:**
```bash
$ grep "### S9:" EPIC_WORKFLOW_USAGE.md
[No results]

$ grep "### S10:" EPIC_WORKFLOW_USAGE.md
[No results]
```text

**Analysis:**
- EPIC_WORKFLOW_USAGE.md advertises "Stage-by-Stage Detailed Workflows"
- S1-S8 have detailed sections
- S9 and S10 missing entirely
- File incomplete

**Impact:** ⚠️ MEDIUM - Incomplete reference doc

**Fix:**
```markdown
## Stage-by-Stage Detailed Workflows

[S1-S8 content exists]

### S9: Epic-Level Final QC (Detailed)

**Purpose:** Comprehensive quality validation at epic level

**Phases:**
- S9.P1: Epic Smoke Testing (30-45 min)
- S9.P2: Epic QC Rounds (3 rounds, 90-135 min)
- S9.P3: User Testing (variable)
- S9.P4: Epic Final Review (20-30 min)

[Complete detailed breakdown]

### S10: Epic Cleanup (Detailed)

[Complete detailed breakdown]
```

---

## Integration with Other Dimensions

**Works With:**
- **D13: Documentation Quality** - D5 checks "is content present", D13 checks "is present content high quality"
- **D1: Cross-Reference Accuracy** - Validates forward references point to existing content

**Complementary:**
- **D11: Structural Patterns** - Required sections (D11) must also be complete (D5)

**Difference from D13:**
- **D5:** Missing sections, stub content, unfulfilled promises
- **D13:** TODOs, code tags, formatting quality of present content
- **Overlap:** Both flag TODOs, but different focus

---

## See Also

**Related Dimensions:**
- `d13_documentation_quality.md` - Quality of present content
- `d1_cross_reference_accuracy.md` - Validates promised content exists
- `d11_structural_patterns.md` - Required sections must be complete

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to discover incomplete content
- `../stages/stage_4_verification.md` - Verify completeness after fixes

**Templates:**
- `../templates/` - Reference for what template files should contain

---

**When to Use:** Run D5 validation after major content additions, file reorganizations, or when guides seem incomplete. Completeness issues must be resolved before audit completion - stub content blocks workflow execution.
