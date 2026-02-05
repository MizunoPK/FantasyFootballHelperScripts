# D16: Accessibility & Usability

**Dimension Number:** 16
**Category:** Advanced Dimensions
**Automation Level:** 80% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-04

**Focus:** Ensure guides are easy to navigate, read, and use effectively
**Typical Issues Found:** 10-20 per audit

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Usability Issues Happen](#how-usability-issues-happen)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)

---

## What This Checks

**Accessibility & Usability** validates that guides are easy to navigate and use:

✅ **Table of Contents:**
- Files >500 lines have TOC
- TOC links to all major sections
- TOC appears near top of file

✅ **Code Block Language Tags:**
- All code blocks have language identifiers (```bash, ```markdown, etc.)
- Enables syntax highlighting
- Improves readability

✅ **Navigation Quality:**
- Clear "Next Stage" or "See Also" links
- Breadcrumbs or context indicators
- Easy to find related content

✅ **Readability:**
- Appropriate line length (no lines >500 chars)
- Proper use of formatting (bold, code blocks, lists)
- Clear section headers

✅ **Agent Usability:**
- Quick-start sections for time-sensitive tasks
- Critical information highlighted or boxed
- Examples provided for complex concepts

---

## Why This Matters

### Impact of Poor Accessibility

**Critical Impact:**
- **Navigation Difficulty:** Hard to find specific sections in long files
- **Reduced Comprehension:** Poor formatting reduces understanding
- **Time Wasted:** Searching for information instead of executing tasks
- **Syntax Confusion:** Untagged code blocks lose context (bash vs markdown vs python)

**Example Failure (Hypothetical):**
```bash
File: stages/s5/s5_p1_planning_round1.md (800 lines, no TOC)

Agent task: "Find Gate 4a requirements"
Problem: No TOC, must scan 800 lines manually
Result: 5 minutes wasted searching, may miss information
```

**With TOC:**
```markdown
Agent clicks TOC link → ## Gate 4a (line 523) → Jumps directly
Result: 5 seconds, accurate
```

### User Directive on Usability

**From file_size_reduction_guide.md:**
> "The point of it is to ensure that agents are able to effectively read and process the guides as they are executing them. I want to ensure that agents have no barriers in their way toward completing their task, or anything that would cause them to incorrectly complete their task."

**Accessibility directly supports this goal:**
- TOCs = remove navigation barriers
- Language tags = remove comprehension barriers
- Clear formatting = remove execution barriers

---

## Pattern Types

### Type 0: Root-Level File Navigation

**Critical Files for Navigation:**
```text
README.md - Main entry point
EPIC_WORKFLOW_USAGE.md - Detailed reference
prompts_reference_v2.md - Prompt lookup
```

**Navigation Requirements:**
- **README.md:** Quick Start section at top (no scrolling needed)
- **EPIC_WORKFLOW_USAGE.md:** TOC with direct links to each stage
- **prompts_reference_v2.md:** Organized by stage with clear headers

**Automated:** ⚠️ Partial (TOC presence automated, navigation quality manual)

### Type 1: Table of Contents Requirement

**Rule:** Files >500 lines MUST have TOC

**Why 500 Lines:**
- Typical screen shows ~50 lines
- >500 lines = >10 screens of scrolling
- Without TOC, finding specific section requires extensive scrolling

**TOC Format:**
```markdown
## Table of Contents

1. [Section 1](#section-1)
2. [Section 2](#section-2)
   - [Subsection 2a](#subsection-2a)
   - [Subsection 2b](#subsection-2b)
3. [Section 3](#section-3)
```text

**Search Command:**
```bash
# Find files >500 lines without TOC
for file in $(find stages reference -name "*.md"); do
  lines=$(wc -l < "$file")
  if [ "$lines" -gt 500 ]; then
    if ! grep -qi "table of contents" "$file"; then
      echo "MISSING TOC: $file ($lines lines)"
    fi
  fi
done
```markdown

**Automated:** ✅ Yes (CHECK 5 in pre_audit_checks.sh)

### Type 2: Code Block Language Tags

**Rule:** All code blocks must have language identifier

**Format:**
```markdown
# WRONG (no language tag)
```text
command here
```text

# CORRECT (with language tag)
```bash
command here
```text

# Common Language Tags
```bash, ```markdown, ```python, ```json, ```yaml
```bash

**Why This Matters:**
- Syntax highlighting improves readability
- Distinguishes bash commands from markdown examples
- Clear visual differentiation between code types

**Search Command:**
```bash
# Find code blocks without language tags
grep -rn "^\`\`\`$" stages templates prompts reference

# Should have minimal results
```markdown

**Automated:** ✅ Yes (CHECK 7 in pre_audit_checks.sh)

### Type 3: Navigation Links

**Required Navigation Elements:**

**At Top (After Title):**
- Link to parent guide (if sub-guide)
- Breadcrumb trail (if deep hierarchy)

**At Bottom (Before end):**
- "Next Stage" or "Next" section (what to do after this)
- "See Also" section (related content)
- Links back to overview or index

**Examples:**

**Sub-Guide:**
```markdown
# S5.P1.I1: Requirements Analysis

**Parent:** [S5.P1: Planning Round 1](s5_p1_planning_round1.md)

[Content]

## Next

Continue to [S5.P1.I2: Algorithm Design](s5_p1_i2_algorithms.md)

## See Also

- [S5.P1: Round 1 Overview](s5_p1_planning_round1.md) - Router to all iterations
- [S4: Testing Strategy](../s4/s4_feature_testing_strategy.md) - Inputs to this iteration
```markdown

**Automated:** ⚠️ Partial (link presence automated, quality manual)

### Type 4: Readability Formatting

**What to Check:**
- Use of bold for emphasis
- Use of code blocks for commands/code
- Use of lists for sequences/options
- Use of tables for comparisons
- Use of callout boxes for warnings

**Good Example:**
```markdown
**CRITICAL:** Do not skip Gate 23a validation.

**Required Steps:**
1. Complete spec analysis
2. Verify checklist resolution
3. Pass 5-part audit

**Warning:** Skipping this gate leads to implementation failures (historical: 80% correlation).
```text

**Poor Example:**
```markdown
Make sure you don't skip Gate 23a validation. It's really important.
You need to complete spec analysis, verify checklist resolution, and
pass the 5-part audit. If you skip this, you'll probably have problems
during implementation.
```markdown

**Automated:** ❌ No (requires human judgment)

### Type 5: Examples and Quick Reference

**What to Check:**
- Complex concepts have examples
- Common tasks have quick reference boxes
- Commands show actual syntax (not pseudocode)

**Good Example:**
```markdown
## Creating Feature Spec

**Quick Reference:**
```bash
# 1. Copy template
cp templates/feature_spec_template.md feature_01_name/spec.md

# 2. Fill in sections (see example below)

# 3. Verify completeness
grep -n "TODO\|\[placeholder\]" spec.md  # Should return nothing
```text

**Example spec.md section:**
```markdown
## Purpose
Enable users to fetch player data from ESPN API with configurable
date ranges and data types (stats, projections, rankings).
```text
```markdown

**Automated:** ❌ No (requires content review)

---

## How Usability Issues Happen

### Root Cause 1: File Growth Without TOC Addition

**Scenario:** File starts small, grows over time, TOC never added

**Evolution:**
```text
Version 1 (2025-10): 250 lines, no TOC needed
Version 2 (2025-11): 400 lines, still manageable
Version 3 (2026-01): 650 lines, should have TOC but not added
Version 4 (2026-02): 850 lines, definitely needs TOC
```markdown

**Why It Happens:**
- No clear trigger for "add TOC now"
- Incremental growth doesn't feel like big change
- Effort to create TOC deferred

**Prevention:**
- Automated check flags >500 lines without TOC
- Add TOC preemptively at 400 lines

### Root Cause 2: Copy-Paste Code Without Language Tags

**Scenario:** Adding examples by copying code snippets

**What Happens:**
```markdown
User requests: "Add example command"

Agent copies from terminal:
```bash
grep -rn "pattern" files/
```

Result: No language tag (just ```)
```text

**Why It Happens:**
- Quick copy-paste doesn't include tag
- Agent doesn't realize tag is missing
- Not caught until audit

**Prevention:**
- Automated check for untagged code blocks
- Prompt agents to add language tags when showing commands

### Root Cause 3: Missing "Next" Navigation

**Scenario:** Guide created standalone, not integrated into workflow

**What Happens:**
```markdown
# Guide Content

[Extensive content about S5.P1.I1]

## See Also
- [Related guide 1]
- [Related guide 2]

# MISSING: What to do next after this iteration
```text

**Why It Happens:**
- Focus on content, not workflow integration
- "Next" step seems obvious so not documented
- Not validated during creation

**Prevention:**
- Template includes "Next" section
- Automated check for navigation sections

### Root Cause 4: Poor Formatting Reduces Scan-ability

**Scenario:** Content written as wall of text

**What Happens:**
```markdown
The implementation planning stage requires you to read the spec
carefully and then identify all the requirements and then check
the checklist and make sure everything is addressed and then create
the implementation plan and verify it covers everything and document
any assumptions and get user approval before proceeding to execution.
```text

**Better:**
```markdown
**Implementation Planning Requirements:**

1. **Read Spec:** Review spec.md thoroughly
2. **Identify Requirements:** Extract all requirements
3. **Check Checklist:** Verify checklist.md items addressed
4. **Create Plan:** Draft implementation_plan.md
5. **Verify Coverage:** Ensure plan covers all requirements
6. **Document Assumptions:** Note any decisions or assumptions
7. **User Approval:** Get Gate 5 approval before S6
```text

**Why Original is Poor:**
- Single long sentence hard to scan
- No visual breaks
- Hard to identify individual steps

---

## Automated Validation

### Script 1: TOC Requirement (IN pre_audit_checks.sh)

```bash
# CHECK 5: Accessibility - TOC for Long Files (D16)
# ============================================================================

echo "=== Accessibility - TOC Check (D16) ==="

MISSING_TOC=0

for file in $(find stages reference -name "*.md"); do
  lines=$(wc -l < "$file")

  if [ "$lines" -gt 500 ]; then
    if ! grep -qi "table of contents\|## contents\|## table of contents" "$file"; then
      echo "⚠️  MISSING TOC: $file ($lines lines)"
      ((MISSING_TOC++))
    fi
  fi
done

echo "Large files missing TOC: $MISSING_TOC"
```markdown

### Script 2: Code Block Language Tags (IN pre_audit_checks.sh)

```bash
# CHECK 7: Code Block Language Tags (D16)
# ============================================================================

echo "=== Code Block Language Tags (D16) ==="

UNTAGGED_BLOCKS=$(grep -rn "^\`\`\`$" stages templates prompts 2>/dev/null | wc -l)

if [ "$UNTAGGED_BLOCKS" -gt 0 ]; then
  echo "⚠️  Code blocks without language tags: $UNTAGGED_BLOCKS"
  echo "   (First 5 examples:)"
  grep -rn "^\`\`\`$" stages templates prompts 2>/dev/null | head -5
else
  echo "✅ All code blocks have language tags"
fi
```markdown

### Script 3: Navigation Links Check (SHOULD ADD)

```bash
# CHECK 5b: Navigation Links (D16)
# ============================================================================

echo "=== Navigation Links Validation ==="

# Check stage guides have "Next" or "See Also"
for file in $(find stages -name "s*_*.md" ! -name "*_template.md"); do
  has_next=$(grep -qi "^## Next\|Next Stage\|Next:" "$file" && echo "yes" || echo "no")
  has_see_also=$(grep -qi "^## See Also" "$file" && echo "yes" || echo "no")

  if [ "$has_next" = "no" ] && [ "$has_see_also" = "no" ]; then
    echo "⚠️  Missing navigation: $file (no Next or See Also)"
  fi
done
```markdown

---

## Manual Validation

### Manual Usability Review Process

**For each guide:**

```markdown
STEP 1: Quick Navigation Test
- Open file
- Can you find TOC within 5 seconds? (if file >500 lines)
- Can you identify next step without reading entire file?
- Are related guides clearly linked?

STEP 2: Readability Assessment
- Scan first screen (don't read in detail)
- Can you identify purpose within 10 seconds?
- Are key warnings/rules highlighted?
- Is formatting used effectively? (bold, lists, code blocks)

STEP 3: Code Example Validation
- Are all code blocks tagged? (```bash, ```python, etc.)
- Are examples concrete? (not pseudocode)
- Are commands copy-pasteable?

STEP 4: Agent Usability Test (Critical)
- If you were an agent starting this task, what would you need first?
- Is that information at the top? (or in TOC if long file)
- Are prerequisites clearly visible before main content?
- Can you execute without reading entire file?

STEP 5: Document Issues
- Missing TOC (if >500 lines)
- Untagged code blocks
- Poor navigation
- Wall-of-text sections needing formatting
```markdown

---

## Context-Sensitive Rules

### When TOCs Are Not Required

**1. Short Files (<500 lines):**
```markdown
File: stages/s8/s8_p1_cross_feature_alignment.md (300 lines)
Verdict: ✅ TOC Optional (file short enough to scan)
```text

**2. Single-Topic Files:**
```markdown
File: reference/naming_conventions.md (200 lines, one topic)
Verdict: ✅ TOC Optional (straightforward navigation)
```markdown

### When TOCs Are Required

**1. Long Files (>500 lines):**
```markdown
File: stages/s5/s5_p1_planning_round1.md (850 lines)
Verdict: ❌ TOC REQUIRED (too long to scan)
```text

**2. Multi-Section Guides:**
```markdown
File: EPIC_WORKFLOW_USAGE.md (600 lines, 10 stage sections)
Verdict: ❌ TOC REQUIRED (multiple distinct sections)
```markdown

### When Untagged Code Blocks Are Acceptable

**1. Intentional Generic Blocks:**
```markdown
```json
[Placeholder for user's custom content]
```
```text
**Verdict:** ✅ ACCEPTABLE (generic placeholder)

**2. Visual Diagrams:**
```markdown
```text
┌─────────┐
│  Box 1  │
└─────────┘
```
```bash
**Verdict:** ✅ ACCEPTABLE (ASCII art, not code)

### When Untagged Code Blocks Are Errors

**1. Bash Commands:**
```markdown
```bash
git commit -m "message"
```
```text
**Verdict:** ❌ ERROR (should be ```bash)

**2. Markdown Examples:**
```markdown
```markdown
## Example Header
```
```text
**Verdict:** ❌ ERROR (should be ```markdown)

---

## Real Examples

### Example 1: Long File Missing TOC

**Issue Found:**
```bash
$ wc -l stages/s5/s5_p1_planning_round1.md
685 stages/s5/s5_p1_planning_round1.md

$ grep -i "table of contents" stages/s5/s5_p1_planning_round1.md
[No results]
```text

**Analysis:**
- File 685 lines (>500 line threshold)
- Contains 3 iteration guides (I1, I2, I3)
- No TOC for navigation

**Impact:** ⚠️ MEDIUM - Time wasted finding specific sections

**Fix:**
```markdown
# S5.P1: Planning Round 1

**Router:** Navigate to iteration guides

## Table of Contents

1. [Overview](#overview)
2. [I1: Requirements Analysis](#i1-requirements-analysis)
3. [I2: Algorithm Design](#i2-algorithm-design)
4. [I3: Integration Planning](#i3-integration-planning)
5. [Validation Loop](#validation-loop)
6. [Next](#next)

[Rest of content]
```markdown

### Example 2: Untagged Code Blocks

**Issue Found:**
```bash
$ grep -n "^\`\`\`$" stages/s5/s5_p1_i1_requirements.md
234:```text
237:```
289:```text
292:```
```bash

**Analysis:**
- 4 code blocks without language tags
- Commands shown without syntax highlighting
- Unclear whether bash, markdown, or other language

**Impact:** ⚠️ LOW - Reduces readability

**Fix:**
```markdown
# Before
```bash
grep -rn "TODO" feature_*/spec.md
```

# After
```bash
grep -rn "TODO" feature_*/spec.md
```text
```markdown

### Example 3: Missing Next Navigation

**Issue Found:**
```markdown
File: stages/s5/s5_p1_i1_requirements.md

[Extensive content about iteration I1]

## See Also
- [S5.P1 Overview](s5_p1_planning_round1.md)
- [S4: Testing Strategy](../s4/s4_feature_testing_strategy.md)

# MISSING: What comes after I1?
```text

**Analysis:**
- Guide ends abruptly
- No indication of next step
- Agents may not know to proceed to I2

**Impact:** ⚠️ MEDIUM - Workflow clarity

**Fix:**
```markdown
## Next

**After completing I1:**
- Continue to [I2: Algorithm Design](s5_p1_i2_algorithms.md)
- If issues found, resolve before proceeding

## See Also
[existing links]
```markdown

### Example 4: Wall of Text Needs Formatting

**Issue Found:**
```markdown
## Critical Rules

You must complete all 22 iterations in S5 before proceeding to S6
and you cannot skip any iterations and you must get user approval
at Gate 5 before starting implementation and all tests must pass
100% before committing and you must run verification after each
round to ensure no new issues were introduced.
```text

**Analysis:**
- Single long sentence
- Multiple important rules buried in paragraph
- Hard to scan, easy to miss rules

**Impact:** ⚠️ MEDIUM - Important information not scannable

**Fix:**
```markdown
## Critical Rules

**🚨 MANDATORY Requirements:**

1. ✅ **Complete ALL 22 iterations** - No skipping allowed
2. ✅ **User approval at Gate 5** - Must pass before S6
3. ✅ **100% test pass rate** - Required before commits
4. ✅ **Verification after each round** - Ensure no new issues

**Historical failure rate when skipping:** 80%
```markdown

---

## Integration with Other Dimensions

**Works With:**
- **D10: File Size Assessment** - Large files especially need TOCs
- **D13: Documentation Quality** - Code tags improve quality

**Complementary:**
- **D5: Content Completeness** (not implemented) - Ensures examples present

---

## See Also

**Related Dimensions:**
- `d10_file_size_assessment.md` - File size directly impacts navigation needs
- `d13_documentation_quality.md` - Quality standards include formatting

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to discover usability issues
- `../stages/stage_4_verification.md` - Re-verify accessibility after fixes

**Reference:**
- `../reference/file_size_reduction_guide.md` - Why usability matters (user directive)

**Scripts:**
- `../scripts/pre_audit_checks.sh` - Automated accessibility validation (CHECK 5, CHECK 7)

---

**When to Use:** Run D16 validation during every audit. Accessibility issues (especially missing TOCs and untagged code blocks) should be fixed to improve agent effectiveness.
