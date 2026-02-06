# D13: Documentation Quality

**Dimension Number:** 13
**Category:** Content Quality Dimensions
**Automation Level:** 90% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-05

**Focus:** Ensure guides have required sections, complete content, no TODOs, and meet quality standards
**Typical Issues Found:** 5-15 per audit

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Quality Issues Happen](#how-quality-issues-happen)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)

---

## What This Checks

**Documentation Quality** validates that guides meet completeness and quality standards:

✅ **Required Sections Present:**
- Stage guides have Table of Contents, Purpose, Prerequisites, Steps, Next Stage
- Dimension guides have What This Checks, Why This Matters, Pattern Types, Examples
- Templates have all expected sections for their type

✅ **No Unresolved TODOs:**
- No TODO, TBD, FIXME markers in published guides
- All placeholders replaced with actual content
- No "[Coming Soon]" or "⏳" markers in completed files

✅ **Content Completeness:**
- All sections have substantive content (not just headers)
- Examples provided where appropriate
- Commands/scripts are complete (not pseudocode)

✅ **Documentation Standards:**
- Code blocks have language tags
- Tables properly formatted
- Links are descriptive (not raw URLs)
- Consistent header hierarchy

✅ **Root-Level File Quality:**
- README.md has current overview
- EPIC_WORKFLOW_USAGE.md has complete workflows
- prompts_reference_v2.md has all stage prompts

---

## Why This Matters

### Impact of Poor Documentation Quality

**Critical Impact:**
- **Agent Confusion:** Incomplete sections leave questions unanswered
- **Workflow Blocked:** TODOs indicate missing critical information
- **Poor Usability:** Missing sections force agents to search elsewhere
- **Trust Erosion:** Placeholders and TODOs appear unfinished

**Example Failure (Hypothetical):**
```markdown
Guide: stages/s5/s5_p3_planning_round3.md
Section: ## Gate 23a Checklist
Content: TODO: Add complete checklist items

Problem: Agent reaches Gate 23a, finds TODO instead of checklist
Result: Cannot validate planning completeness, workflow stuck
```diff

### Common Quality Issues

**After Rapid Development:**
- TODOs added as placeholders during fast iteration
- Sections stubbed out but never filled in
- Examples promised but not added

**After Restructuring:**
- Old content removed, new content not added yet
- Templates updated but guides still reference old structure
- Cross-references broken by file moves

**After Feature Additions:**
- New sections added quickly without full documentation
- Edge cases mentioned but not explained
- Integration points noted but not detailed

---

## Pattern Types

### Type 0: Root-Level File Completeness (CRITICAL)

**Files to Check:**
```text
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
feature-updates/guides_v2/prompts_reference_v2.md
feature-updates/guides_v2/audit/README.md
```

**Required Sections:**

**README.md:**
- [ ] Quick Start section
- [ ] What is v2 Workflow section
- [ ] 10 Stages overview
- [ ] Guide Index (complete)
- [ ] Last Updated (current)

**EPIC_WORKFLOW_USAGE.md:**
- [ ] Complete S1-S10 workflow details
- [ ] Stage-by-stage breakdowns
- [ ] Phase/iteration structures
- [ ] Duration estimates

**prompts_reference_v2.md:**
- [ ] All 10 stage prompts
- [ ] Debugging protocol prompts
- [ ] Missed requirement prompts
- [ ] Special workflow prompts

**Automated:** ⚠️ Partial (section presence can be checked, completeness is manual)

### Type 1: TODO/TBD/FIXME Markers

**What to Check:**
- Any occurrence of TODO, TBD, FIXME in guides
- Indicates incomplete content
- Must be resolved before audit completion

**Search Commands:**
```bash
# Find all TODOs
grep -rn "TODO\|TBD\|FIXME" stages templates prompts reference

# Find placeholders
grep -rn "\[placeholder\]\|\[Coming Soon\]" stages templates prompts reference

# Find ⏳ markers (work in progress)
grep -rn "⏳" stages templates prompts reference
```markdown

**Automated:** ✅ Yes (CHECK 3 in pre_audit_checks.sh)

### Type 2: Required Sections for Stage Guides

**Standard Stage Guide Structure:**
```markdown
# Stage N: [Name]

## Table of Contents

## Overview
- **Purpose:**
- **Duration:**
- **Prerequisites:**
- **Outputs:**

## Phases (or Steps)

## Critical Rules

## Common Mistakes

## Next Stage

## See Also
```

**Validation:**
```bash
# Check for required sections in stage guides
for file in stages/s*/s*_*.md; do
  echo "Checking $file..."
  grep -q "## Table of Contents" "$file" || echo "  MISSING: Table of Contents"
  grep -q "## Overview" "$file" || echo "  MISSING: Overview"
  grep -q "## Critical Rules\|## Key Principles" "$file" || echo "  MISSING: Critical Rules"
  grep -q "## Next Stage\|## Next" "$file" || echo "  MISSING: Next Stage"
done
```markdown

**Automated:** ✅ Yes (structural pattern check possible)

### Type 3: Required Sections for Dimension Guides

**Standard Dimension Guide Structure:**
```markdown
# Dimension N: [Name]

**Focus:**
**Automation Level:**
**Typical Issues Found:**
**Reading Time:**

## Table of Contents

## What This Checks

## Why This Matters

## Pattern Types

## How Errors Happen (or How [Issue] Happens)

## Automated Validation

## Manual Validation

## Context-Sensitive Rules

## Real Examples

## See Also
```

**Validation:**
```bash
# Check for required sections in dimension guides
for file in audit/dimensions/d*.md; do
  echo "Checking $file..."
  grep -q "^\*\*Focus:\*\*" "$file" || echo "  MISSING: Focus metadata"
  grep -q "## What This Checks" "$file" || echo "  MISSING: What This Checks"
  grep -q "## Why This Matters" "$file" || echo "  MISSING: Why This Matters"
  grep -q "## Pattern Types" "$file" || echo "  MISSING: Pattern Types"
  grep -q "## Real Examples" "$file" || echo "  MISSING: Real Examples"
done
```markdown

**Automated:** ✅ Yes (structural pattern check possible)

### Type 4: Code Block Language Tags

**What to Check:**
- All code blocks have language tags
- Enables syntax highlighting
- Improves readability

**Pattern:**
```markdown
# WRONG (no language tag)
```
command here
```text

# CORRECT (with language tag)
```text
command here
```text
```

**Search Command:**
```bash
# Find code blocks without language tags
grep -rn "^\`\`\`$" stages templates prompts reference

# Should have minimal results (only intentional blank tags)
```markdown

**Automated:** ✅ Yes (CHECK 7 in pre_audit_checks.sh)

### Type 5: Empty or Stub Sections

**What to Check:**
- Sections with only header, no content
- Sections with placeholder text only
- Sections referencing "see below" but no content below

**Pattern:**
```markdown
## Prerequisites

[None yet - TODO]

## Output

TBD

## Examples

See examples below.

<!-- No examples actually provided -->
```

**Search Command:**
```bash
# Find sections followed by TODO/TBD/placeholder
grep -A 3 "^## " stages/*.md | grep -B 1 "TODO\|TBD\|placeholder"
```markdown

**Automated:** ⚠️ Partial (markers automated, stub detection manual)

---

## How Quality Issues Happen

### Root Cause 1: Rapid Iteration Leaves TODOs

**Scenario:** Adding new stage quickly during epic

**What Happens:**
```markdown
# Day 1: Create file structure
## Gate 23a
TODO: Define checklist items

# Day 2-10: Work on other stages
[Gate 23a TODO forgotten]

# Day 11: Audit finds TODO still present
```

**Why It Happens:**
- Focus on getting structure in place first
- Plan to "come back and fill in details"
- TODOs forgotten as work progresses elsewhere

**Prevention:**
- Explicit TODO audit before completing stage
- No TODOs allowed in files marked "complete"
- Regular grep for TODO markers

### Root Cause 2: Examples Promised But Not Added

**Scenario:** Guide mentions "see examples" but examples not created

**Before:**
```markdown
## Step 3: Create Spec

Follow the specification template structure. See examples below for guidance.

## Next Steps
[No examples section ever added]
```markdown

**Why It Happens:**
- Intended to add examples later
- Forgot about promise in earlier section
- No validation that "see below" actually has content below

**Prevention:**
- Add examples immediately when mentioned
- Grep for "see.*example" and verify examples exist
- Manual validation of forward references

### Root Cause 3: Restructuring Removes Content

**Scenario:** File reorganization deletes sections without replacement

**Before restructure:**
```markdown
# s5_planning.md (1200 lines)

## Gate 4a Checklist
[Complete 10-item checklist]
```

**After restructure:**
```markdown
# s5_p1_i2_algorithms.md (400 lines)

## Gate 4a Checklist
TODO: Move checklist from old file
[Forgot to actually move it]
```markdown

**Why It Happens:**
- Content assumed to be moved during split
- No verification that all sections transferred
- TODOs added as placeholders but not resolved

### Root Cause 4: Template Drift

**Scenario:** Template format changes, existing guides not updated

**New template standard (2026-01):**
```markdown
# Stage Guide Template

**Duration:** [X hours]
**Prerequisites:** [List]
**Outputs:** [List]
```

**Old guides (created 2025-11):**
```markdown
# Stage Guide

Prerequisites: None documented
[Missing Duration and Outputs sections]
```bash

**Why It Happens:**
- Template updated, existing files not backfilled
- No systematic check for template compliance
- Incremental template improvements not applied retroactively

---

## Automated Validation

### Script 1: TODO/Placeholder Detection (IN pre_audit_checks.sh)

```bash
# CHECK 3: Documentation Quality (D13)
# ============================================================================

echo "=== Documentation Quality (D13) ==="

TODO_COUNT=$(grep -rc "TODO\|TBD\|FIXME" stages templates prompts reference 2>/dev/null | grep -v ":0" | wc -l)
PLACEHOLDER_COUNT=$(grep -rc "\[placeholder\]\|\.\.\." stages templates prompts 2>/dev/null | grep -v ":0" | wc -l)

if [ "$TODO_COUNT" -gt 0 ]; then
  echo "❌ TODOs found:"
  grep -rn "TODO\|TBD\|FIXME" stages templates prompts reference 2>/dev/null | head -10
  echo ""
fi

if [ "$PLACEHOLDER_COUNT" -gt 0 ]; then
  echo "⚠️  Placeholders found:"
  grep -rn "\[placeholder\]" stages templates prompts 2>/dev/null | head -10
  echo ""
fi

echo "TODOs remaining: $TODO_COUNT"
echo "Placeholders found: $PLACEHOLDER_COUNT"
```

### Script 2: Code Block Language Tags (IN pre_audit_checks.sh)

```bash
# CHECK 7: Code Block Language Tags (D16 / D13 overlap)
# ============================================================================

echo "=== Code Block Language Tags ==="

# Find code blocks without language specification
UNTAGGED_BLOCKS=$(grep -rn "^\`\`\`$" stages templates prompts reference 2>/dev/null | wc -l)

if [ "$UNTAGGED_BLOCKS" -gt 5 ]; then
  echo "⚠️  Untagged code blocks found: $UNTAGGED_BLOCKS"
  grep -rn "^\`\`\`$" stages templates prompts reference 2>/dev/null | head -10
else
  echo "✅ Most code blocks properly tagged"
fi
```bash

### Script 3: Required Sections Check (SHOULD ADD)

```bash
# CHECK 3b: Required Sections Validation (D13)
# ============================================================================

echo "=== Required Sections Validation ==="

# Check stage guides for required sections
for file in $(find stages -name "s*_*.md" ! -name "*_template.md"); do
  missing_sections=""

  grep -q "## Table of Contents\|## TOC" "$file" || missing_sections="$missing_sections TOC"
  grep -q "## Overview\|## Purpose" "$file" || missing_sections="$missing_sections Overview"
  grep -q "## Prerequisites" "$file" || missing_sections="$missing_sections Prerequisites"
  grep -q "## Next\|## See Also" "$file" || missing_sections="$missing_sections Navigation"

  if [ -n "$missing_sections" ]; then
    echo "⚠️  $file missing:$missing_sections"
  fi
done

# Check dimension guides for required sections
for file in $(find audit/dimensions -name "d*.md"); do
  missing_sections=""

  grep -q "^\*\*Focus:\*\*" "$file" || missing_sections="$missing_sections Metadata"
  grep -q "## What This Checks" "$file" || missing_sections="$missing_sections WhatThisChecks"
  grep -q "## Real Examples" "$file" || missing_sections="$missing_sections Examples"

  if [ -n "$missing_sections" ]; then
    echo "⚠️  $file missing:$missing_sections"
  fi
done
```

---

## Manual Validation

### ⚠️ CRITICAL: Root-Level File Content Review

**Mandatory root file quality check:**

```bash
# Step 0: Verify root files have complete, current content
cd feature-updates/guides_v2

echo "=== Root File Quality Check ==="
for file in README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md; do
  echo "Checking $file..."

  # Check metadata
  grep -q "Last Updated" "$file" || echo "  MISSING: Last Updated field"

  # Check key sections (file-specific)
  if [ "$file" = "README.md" ]; then
    grep -q "## Quick Start" "$file" || echo "  MISSING: Quick Start"
    grep -q "## The 10 Stages" "$file" || echo "  MISSING: 10 Stages overview"
    grep -q "## Guide Index" "$file" || echo "  MISSING: Guide Index"
  fi

  if [ "$file" = "EPIC_WORKFLOW_USAGE.md" ]; then
    grep -q "## Stage-by-Stage" "$file" || echo "  MISSING: Detailed workflows"
  fi

  if [ "$file" = "prompts_reference_v2.md" ]; then
    for stage in {1..10}; do
      grep -q "Starting S$stage" "$file" || echo "  MISSING: S$stage prompt"
    done
  fi

  echo ""
done
```diff

### Manual Validation Process

**For each guide file:**

```markdown
STEP 1: Check required sections present
- Compare against template for that guide type
- Verify all sections have headers

STEP 2: Check section completeness
- Each section has >3 lines of content (not just header)
- No TODOs, TBDs, placeholders
- No "see below" without actual content below

STEP 3: Check examples quality
- Examples are concrete (not pseudocode)
- Examples show real file paths, commands
- Examples have before/after or input/output

STEP 4: Check navigation completeness
- "Next Stage" points to actual next stage
- "See Also" references exist
- Prerequisites listed are accurate

STEP 5: Document issues found
- Add to discovery report
- Categorize by severity (missing section = HIGH, minor formatting = LOW)
```

**For templates:**

```markdown
STEP 1: Verify template has all expected sections
- Check against actual usage (what do agents need?)
- Verify no sections missing compared to similar templates

STEP 2: Check for placeholder content
- Templates should have helpful placeholder text
- No TODOs in templates (templates are guides for users)

STEP 3: Verify template examples
- If template includes example values, ensure they're realistic
- Check that example values are clearly marked as examples
```markdown

---

## Context-Sensitive Rules

### When TODOs Are Acceptable

**1. In Draft/WIP Files:**
```markdown
File: _internal/DRAFT_new_dimension.md
Status: Clearly marked as draft
Verdict: ✅ ACCEPTABLE (work in progress, not published)
```

**2. In Comments (Not Content):**
```markdown
<!-- TODO for guide author: Consider adding edge case example -->

# Actual Guide Content Here
```markdown
**Verdict:** ✅ ACCEPTABLE (comment, not visible content)

**3. In Historical Examples:**
```markdown
**Before fix:**
## Prerequisites
TODO: Add prerequisites

**After fix:**
## Prerequisites
- S1 complete
- DISCOVERY.md created
```
**Verdict:** ✅ ACCEPTABLE (showing what was wrong)

### When TODOs Are Errors

**1. In Published Stage Guides:**
```markdown
File: stages/s5/s5_p3_i2_gates_part1.md
Status: Active guide used in workflow

## Gate 23a Checklist
TODO: Add checklist items
```markdown
**Verdict:** ❌ ERROR (blocks workflow)

**2. In Templates:**
```markdown
File: templates/feature_spec_template.md

## Acceptance Criteria
TODO: Define what constitutes done
```
**Verdict:** ❌ ERROR (template should guide user)

**3. In Root Files:**
```markdown
File: README.md

## Guide Index
TODO: Complete this section
```markdown
**Verdict:** ❌ CRITICAL (entry point must be complete)

---

## Real Examples

### Example 1: TODO in Critical Section

**Issue Found:**
```markdown
File: stages/s5/s5_p3_i2_gates_part1.md
Line: 145
Section: ## Gate 23a: Pre-Implementation Spec Audit

Content:
## Gate 23a Checklist

TODO: Add complete 5-part checklist from original guide
```

**Analysis:**
- Gate 23a is critical validation point before S6
- Checklist missing means agents can't validate planning
- Workflow blocked at this gate

**Impact:** ❌ CRITICAL - Blocks S5→S6 transition

**Fix:**
```markdown
## Gate 23a Checklist

**Part 1: Requirements Completeness**
- [ ] All spec.md requirements have implementation steps
- [ ] All checklist.md items addressed in plan
- [ ] Edge cases from test_strategy.md covered

**Part 2: Algorithm Detail**
[Complete 5-part checklist added]
```markdown

### Example 2: Missing Required Section

**Issue Found:**
```bash
$ grep -A 20 "## Overview" stages/s7/s7_p2_qc_rounds.md

[No match found - section missing entirely]
```

**Analysis:**
- Stage guides require Overview section
- Agents expect to find purpose, duration, prerequisites
- Missing overview forces agents to infer from other sections

**Impact:** ⚠️ MEDIUM - Reduces usability, not blocking

**Fix:**
```markdown
## Overview

**Purpose:** Systematic quality validation through 3 rounds of inspection

**Duration:** 30-45 minutes per round (90-135 minutes total)

**Prerequisites:**
- S7.P1 Smoke Testing passed (zero failures)
- All smoke test issues resolved

**Outputs:**
- 3 QC round reports
- All issues resolved or documented
- Confidence in implementation quality
```markdown

### Example 3: Code Blocks Missing Language Tags

**Issue Found:**
```bash
$ grep -rn "^\`\`\`$" stages/s5/s5_p1_i1_requirements.md

stages/s5/s5_p1_i1_requirements.md:234:```text
stages/s5/s5_p1_i1_requirements.md:237:```
stages/s5/s5_p1_i1_requirements.md:289:```text
stages/s5/s5_p1_i1_requirements.md:292:```

[8 code blocks without language tags]
```

**Analysis:**
- Code blocks without tags don't get syntax highlighting
- Harder to read, especially for long command examples
- Simple fix: add language identifier

**Impact:** ⚠️ LOW - Cosmetic, but affects readability

**Fix:**
```markdown
# Before
```bash
grep -rn "pattern" files/
```text

# After
```
grep -rn "pattern" files/
```text
```bash

### Example 4: Root File Missing Section

**Issue Found:**
```bash
$ grep -n "## Guide Index" README.md
[No results]

# Section promised in Table of Contents but not present
$ grep -n "Guide Index" README.md
12:- [Guide Index](#guide-index)
```

**Analysis:**
- **CRITICAL** - README.md is entry point (referenced in CLAUDE.md)
- Table of Contents links to section that doesn't exist
- Users clicking link get broken navigation

**Impact:** ❌ HIGH - Root file broken navigation

**Fix:**
```markdown
## Guide Index

### Stage Guides
- [S1: Epic Planning](../../stages/s1/s1_epic_planning.md)
- [S2: Feature Planning](../../stages/s2/s2_feature_deep_dive.md)
[Complete index of all guides]
```markdown

---

## Integration with Other Dimensions

**Works With:**
- **D1: Cross-Reference Accuracy** - Validates "See Also" references exist
- **D11: Structural Patterns** - Validates required sections (template compliance)
- **D14: Content Accuracy** - Validates claims match reality

**Complementary:**
- **D5: Content Completeness** (not implemented) - Would check for missing content within sections
- **D16: Accessibility** - TOC requirement overlaps

---

## Known Exceptions

**Updated:** 2026-02-05 (Round 3 audit)

### Prerequisites and Exit Criteria Exceptions

**17 files intentionally lack formal "## Prerequisites" or "## Exit Criteria" sections** due to established design patterns.

**Documentation:** `../reference/known_exceptions.md` (complete list with rationale)

**Categories:**

**Category A: S5 Iteration Files (14 files)**
- Pattern: Router files and detailed iteration guides
- Prerequisites: Inline statements (e.g., "**Prerequisites:** Previous iterations complete")
- Exit Criteria: Inherited from parent round guides (s5_p1, s5_p2, s5_p3)
- Examples: s5_p1_i3_integration.md, s5_p1_i3_iter5_dataflow.md, s5_p3_i1_iter17_phasing.md
- Design: Sequential steps within larger workflow, formal sections would be redundant

**Category B: Optional/Auxiliary Files (3 files)**
- Pattern: Conditional or reference guides, not standard workflows
- Examples: s3_parallel_work_sync.md (optional), s4_feature_testing_card.md (reference card)
- Design: Not part of standard epic workflow sequence

**Audit Workflow:**

When checking Prerequisites/Exit Criteria (Type 1, Type 2):
1. Generate violation list using automated patterns
2. **Cross-reference with known_exceptions.md** before flagging
3. Filter out 17 known exceptions
4. Investigate remaining violations as potential real issues

**Automation:**

The `pre_audit_checks.sh` script (CHECK 2) now includes exception filtering:
```bash
# Known exceptions array (17 files)
declare -a known_exceptions=(
  "stages/s5/s5_p1_i3_integration.md"
  "stages/s5/s5_p1_i3_iter5_dataflow.md"
  # ... (14 S5 iteration files)
  "stages/s3/s3_parallel_work_sync.md"
  "stages/s4/s4_feature_testing_card.md"
  "stages/s4/s4_test_strategy_development.md"
)

# Skip known exceptions in check loop
for file in stages/*/*.md; do
  skip=false
  for exception in "${known_exceptions[@]}"; do
    if [ "$file" == "$exception" ]; then
      skip=true
      break
    fi
  done

  if [ "$skip" = true ]; then
    continue
  fi

  # Check for Prerequisites/Exit Criteria...
done
```

**History:**
- Round 2: Flagged 34 files missing Prerequisites/Exit Criteria
- Round 3: Investigated all 34, categorized as 4 real issues + 30 intentional exceptions
- Post-Round 3: Documented exceptions, updated automation to filter them

**Why This Matters:**
- Prevents false positives in future audits
- Documents design decisions
- Enables accurate quality metrics (real issues vs. design patterns)

---

## See Also

**Related Dimensions:**
- `d1_cross_reference_accuracy.md` - Verify "See Also" links
- `d11_structural_patterns.md` - Template compliance validation
- `d16_accessibility_usability.md` - Navigation and TOC requirements

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to discover quality issues
- `../stages/stage_4_verification.md` - Re-verify quality after fixes

**Templates:**
- `../templates/` - Reference for required template sections

**Scripts:**
- `../scripts/pre_audit_checks.sh` - Automated quality validation (CHECK 3, CHECK 7)

---

**When to Use:** Run D13 validation during every audit. Documentation quality issues (especially TODOs and missing sections) must be resolved before audit completion.
