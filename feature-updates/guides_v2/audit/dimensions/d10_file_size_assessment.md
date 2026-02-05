# D10: File Size Assessment

**Dimension Number:** 10
**Category:** Structural Dimensions
**Automation Level:** 100% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-04

**Focus:** Ensure files are appropriately sized for agent comprehension and usability
**Typical Issues Found:** 2-5 large files per audit

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [How Large Files Happen](#how-large-files-happen)
5. [Automated Validation](#automated-validation)
6. [Manual Validation](#manual-validation)
7. [Context-Sensitive Rules](#context-sensitive-rules)
8. [Real Examples](#real-examples)

---

## What This Checks

**File Size Assessment** validates that files don't exceed usability thresholds:

✅ **CLAUDE.md Character Limit:**
- HARD LIMIT: 40,000 characters
- Policy violation if exceeded
- Must reduce before audit completion

✅ **Workflow Guide Line Limits:**
- CRITICAL: >1000 lines (must reduce or justify)
- LARGE: 800-1000 lines (strongly consider split)
- WARNING: 600-800 lines (evaluate for split)
- OK: <600 lines (no action needed)

✅ **Root-Level File Sizes:**
- README.md, EPIC_WORKFLOW_USAGE.md, prompts_reference_v2.md
- No hard limits, but large sizes indicate potential issues

✅ **Template Sizes:**
- Templates should be concise (typical: 100-300 lines)
- Large templates (>500 lines) may indicate over-specification

---

## Why This Matters

### Impact of Large Files

**Critical Impact:**
- **Agent Comprehension Barriers:** Large files overwhelm agent processing
- **Navigation Difficulty:** Hard to find relevant sections quickly
- **Information Overload:** May skip critical instructions
- **Execution Errors:** Incorrect task completion due to missed details

**User Directive:**
> "The point of it is to ensure that agents are able to effectively read and process the guides as they are executing them. I want to ensure that agents have no barriers in their way toward completing their task, or anything that would cause them to incorrectly complete their task."

**Example Impact (Real):**
```text
CLAUDE.md: 45,786 characters (5,786 over limit)
Problem: Agents read CLAUDE.md at start of EVERY task
Result: Information overload, reduced effectiveness, slower task start
Solution: Reduced to 27,395 chars (40% reduction) by extracting to EPIC_WORKFLOW_USAGE.md
```

### When Files Grow

**Common Trigger Events:**

**After Feature Additions:**
- S5 gains more iterations → planning guide grows from 400→800 lines
- New protocol added → guide gains 200 lines of detailed instructions
- Examples added for clarity → guide doubles in size

**After Multiple Refinements:**
- Each iteration adds clarifications → file grows incrementally
- No single change is large, but cumulative effect significant
- Historical: guides grow 10-20% per epic cycle

**After Content Consolidation:**
- Merge 3 small guides into 1 → creates 1200-line file
- Centralize scattered content → concentration effect

---

## Pattern Types

### Type 0: Root-Level Critical Files

**Files with HARD LIMITS:**

```text
CLAUDE.md: 40,000 characters (POLICY VIOLATION if exceeded)
```

**Why This Matters:**
- CLAUDE.md read at start of EVERY task by EVERY agent
- Direct correlation between file size and agent effectiveness
- User-mandated policy limit

**Search Command:**
```bash
# Check CLAUDE.md character count
wc -c CLAUDE.md

# Compare to limit
CHARS=$(wc -c < CLAUDE.md)
if [ $CHARS -gt 40000 ]; then
  echo "POLICY VIOLATION: CLAUDE.md ($CHARS chars) exceeds 40,000 limit"
  echo "Overage: $((CHARS - 40000)) characters"
fi
```

**Automated:** ✅ Yes (CHECK 1b in pre_audit_checks.sh)

### Type 1: Critical Size Files (>1000 lines)

**What to Check:**
- Any workflow guide >1000 lines
- Indicates substantial content that likely has natural subdivisions
- MUST reduce or provide strong justification

**Search Command:**
```bash
# Find files >1000 lines
find stages reference templates -name "*.md" -exec wc -l {} \; | \
  awk '$1 > 1000 {print $1, $2}' | \
  sort -rn
```

**Automated:** ✅ Yes (CHECK 1 in pre_audit_checks.sh)

### Type 2: Large Files (800-1000 lines)

**What to Check:**
- Files approaching critical threshold
- Should strongly consider splitting
- Evaluate natural subdivisions

**Search Command:**
```bash
# Find files 800-1000 lines
find stages reference templates -name "*.md" -exec wc -l {} \; | \
  awk '$1 > 800 && $1 <= 1000 {print $1, $2}' | \
  sort -rn
```

**Automated:** ⚠️ Partial (detection automated, evaluation manual)

### Type 3: Warning Size Files (600-800 lines)

**What to Check:**
- Files in warning range
- May benefit from splitting
- Evaluate if file serves multiple purposes

**Search Command:**
```bash
# Find files 600-800 lines
find stages reference templates -name "*.md" -exec wc -l {} \; | \
  awk '$1 > 600 && $1 <= 800 {print $1, $2}' | \
  sort -rn
```

**Automated:** ✅ Yes (CHECK 1 in pre_audit_checks.sh)

### Type 4: Template Size Assessment

**What to Check:**
- Templates should be concise (100-300 lines typical)
- Large templates (>500 lines) may over-specify
- Check if template is actually a guide (misnamed)

**Search Command:**
```bash
# Find large templates
find templates -name "*.md" -exec wc -l {} \; | \
  awk '$1 > 500 {print $1, $2}' | \
  sort -rn
```

**Automated:** ⚠️ Partial (no specific check, but caught by general file size check)

---

## How Large Files Happen

### Root Cause 1: Incremental Growth (Silent Creep)

**Scenario:** File starts at 400 lines, grows 50 lines per epic

**What Happens:**
```text
Epic 1: 400 lines (OK)
Epic 2: 450 lines (OK) - Added examples
Epic 3: 520 lines (OK) - Added edge cases
Epic 4: 580 lines (WARNING) - Added debugging section
Epic 5: 650 lines (LARGE) - Added more iterations
Epic 6: 720 lines (LARGE) - Added validation loop details
```

**Why It Happens:**
- Each addition seems small (5-10% growth)
- No single change triggers review
- Cumulative effect not noticed until file is 80% larger

**Prevention:**
- Regular file size audits (every 2-3 epics)
- "Last Updated" date monitoring (D14)
- Pre-audit script catches threshold crossings

### Root Cause 2: Content Consolidation Without Refactoring

**Scenario:** Merge 3 guides into 1 for better organization

**Before:**
```text
s5_round1.md (400 lines)
s5_round2.md (350 lines)
s5_round3.md (450 lines)
```

**After (WRONG):**
```text
s5_planning.md (1200 lines) ← Direct concatenation
```

**Better Approach:**
```text
s5_planning.md (200 lines) ← Router to sub-guides
s5_p1_planning_round1.md (400 lines)
s5_p2_planning_round2.md (350 lines)
s5_p3_planning_round3.md (450 lines)
```

### Root Cause 3: Detailed Examples Added Inline

**Scenario:** Users request more examples for clarity

**Before:**
```markdown
## Step 3: Create Spec
Create spec.md using template.
```

**After:**
```markdown
## Step 3: Create Spec
Create spec.md using template.

### Example 1: Simple Feature
[50 lines of example]

### Example 2: Complex Feature
[75 lines of example]

### Example 3: Integration Feature
[60 lines of example]

### Common Mistakes
[40 lines of anti-patterns]
```

**Result:** Section grows from 3 lines → 225 lines

**Better Approach:**
```markdown
## Step 3: Create Spec
Create spec.md using template.

**See:** `reference/stage_2/specification_examples.md` for detailed examples
```

---

## Automated Validation

### Script 1: File Size Assessment (IN pre_audit_checks.sh)

```bash
# CHECK 1: File Size Assessment (D10)
# ============================================================================

echo "=== File Size Assessment (D10) ==="

TOO_LARGE=0
LARGE=0

for file in $(find stages -name "*.md"); do
  lines=$(wc -l < "$file")

  if [ "$lines" -gt 1000 ]; then
    echo "❌ TOO LARGE: $file ($lines lines)"
    ((TOO_LARGE++))
  elif [ "$lines" -gt 600 ]; then
    echo "⚠️  LARGE: $file ($lines lines) - consider split"
    ((LARGE++))
  fi
done

echo "Files >1000 lines: $TOO_LARGE"
echo "Files 600-1000 lines: $LARGE"
```

### Script 2: CLAUDE.md Character Limit (IN pre_audit_checks.sh)

```bash
# CHECK 1b: Policy Compliance - CLAUDE.md Character Limit (D10)
# ============================================================================

claude_md="../../CLAUDE.md"
if [ -f "$claude_md" ]; then
    claude_size=$(wc -c < "$claude_md")
    if [ $claude_size -gt 40000 ]; then
        echo "❌ POLICY VIOLATION: CLAUDE.md ($claude_size chars) exceeds 40,000 limit"
        echo "   Overage: $((claude_size - 40000)) characters"
        echo "   Action: Extract ~$((claude_size - 40000)) characters to separate files"
    else
        echo "✅ PASS: CLAUDE.md ($claude_size chars) within 40,000 limit"
    fi
fi
```

### Script 3: Size Trend Analysis (SHOULD ADD)

```bash
# CHECK 1c: File Size Trend Analysis (D10)
# ============================================================================

echo "=== File Size Trend Analysis ==="

# Check for files that grew significantly since last audit
# (Requires git history)

for file in $(find stages -name "*.md"); do
  # Get current size
  current_size=$(wc -l < "$file" 2>/dev/null || echo "0")

  # Get size from 1 month ago
  old_size=$(git show HEAD~30:"$file" 2>/dev/null | wc -l || echo "0")

  if [ "$old_size" -gt 0 ] && [ "$current_size" -gt 0 ]; then
    growth=$(( (current_size - old_size) * 100 / old_size ))

    if [ "$growth" -gt 50 ]; then
      echo "⚠️  RAPID GROWTH: $file (+$growth% in last month)"
      echo "   Was: $old_size lines → Now: $current_size lines"
    fi
  fi
done
```

---

## Manual Validation

### ⚠️ CRITICAL: Evaluation Framework for Large Files

**When pre-audit script flags large files, use this framework:**

```markdown
For EACH file flagged as LARGE or TOO LARGE:

STEP 1: Purpose Analysis
- What is the primary purpose of this file?
- Does it serve multiple distinct purposes?
- Is it a router, guide, reference, or template?

STEP 2: Content Analysis
- Does content have natural subdivisions? (phases, iterations, categories)
- Is there duplicate content across sections?
- Are there detailed examples that could be extracted?
- Are there reference materials that could live elsewhere?

STEP 3: Usage Analysis
- How do agents use this file? (read once, reference repeatedly, router)
- Would splitting improve or hinder usability?

STEP 4: Decision
- [ ] KEEP: File should remain as-is (provide justification)
- [ ] SPLIT: Extract to sub-guides (create file structure)
- [ ] EXTRACT: Move examples/reference to separate files
- [ ] CONSOLIDATE: Remove duplicate content
```

**See:** `../reference/file_size_reduction_guide.md` for complete reduction protocols

### Manual Validation Process

**For CLAUDE.md over limit:**

```markdown
STEP 1: Run character count
$ wc -c CLAUDE.md

STEP 2: If over 40,000, calculate overage
$ CHARS=$(wc -c < CLAUDE.md)
$ echo "Overage: $((CHARS - 40000)) characters"

STEP 3: Use CLAUDE.md Reduction Protocol
→ See file_size_reduction_guide.md Section 5

STEP 4: Identify extraction candidates
- Detailed workflow descriptions → EPIC_WORKFLOW_USAGE.md
- Parallel work details → parallel_work/README.md
- Anti-patterns examples → reference/common_mistakes.md

STEP 5: Execute reduction
- Extract content to target files
- Replace with condensed version + reference link
- Verify all information still accessible

STEP 6: Validate reduction
$ wc -c CLAUDE.md  # Should be ≤40,000
```

**For workflow guides >1000 lines:**

```markdown
STEP 1: Analyze file structure
- Read table of contents
- Identify natural subdivisions
- Check if router pattern appropriate

STEP 2: Determine reduction strategy
→ See file_size_reduction_guide.md Section 4 (4 strategies)

STEP 3: Create reduction plan
- List files to create
- List content to extract
- List cross-references to update

STEP 4: Execute reduction
- Create new files
- Move content
- Update cross-references
- Verify navigation intact

STEP 5: Validate reduction
$ wc -l new_files.md  # All should be <600 lines
$ grep -r "old_file_path" .  # No broken references
```

---

## Context-Sensitive Rules

### When Large Files Are Acceptable

**1. Reference Files (Lists):**
```markdown
File: reference/glossary.md (700 lines)
Content: Alphabetical term definitions
Verdict: ✅ ACCEPTABLE (reference material, not sequential reading)
```

**2. Pattern Libraries:**
```markdown
File: reference/pattern_library.md (650 lines)
Content: Search patterns organized by category
Verdict: ✅ ACCEPTABLE (lookup reference, not read start-to-finish)
```

**3. Comprehensive Templates:**
```markdown
File: templates/epic_readme_template.md (400 lines)
Content: Complete template with all sections
Verdict: ✅ ACCEPTABLE (copied then edited, not read repeatedly)
```

### When Large Files Are Errors

**1. Sequential Workflow Guides:**
```markdown
File: stages/s5/s5_implementation_planning.md (1200 lines)
Content: Step-by-step instructions for S5
Verdict: ❌ ERROR (agents must read sequentially, too long)
Fix: Split into s5_p1, s5_p2, s5_p3 (400 lines each)
```

**2. Root Entry Point Files:**
```markdown
File: CLAUDE.md (45,786 characters)
Content: Project instructions
Verdict: ❌ POLICY VIOLATION (exceeds 40,000 char limit)
Fix: Extract to EPIC_WORKFLOW_USAGE.md, keep quick reference
```

**3. Guides with Multiple Purposes:**
```markdown
File: stages/s2/s2_feature_deep_dive.md (950 lines)
Content: Research + Specification + Refinement (3 phases)
Verdict: ⚠️ LARGE (should split into phase files)
Fix: Create s2_p1_research.md, s2_p2_specification.md, s2_p3_refinement.md
```

---

## Real Examples

### Example 1: CLAUDE.md Policy Violation (Critical)

**Issue Found:**
```bash
$ wc -c CLAUDE.md
45786 CLAUDE.md

POLICY VIOLATION: 5,786 characters over 40,000 limit
```

**Analysis:**
- CLAUDE.md read at start of every task
- 45,786 chars = information overload
- Contains detailed workflows better suited for reference docs

**Reduction Strategy:**
- Extract detailed stage workflows to EPIC_WORKFLOW_USAGE.md
- Extract S2 parallel work details to parallel_work/ guides
- Extract anti-patterns to reference/common_mistakes.md
- Keep concise quick reference in CLAUDE.md

**Result:**
```bash
$ wc -c CLAUDE.md
27395 CLAUDE.md

✅ PASS: 40% reduction, 32.5% under limit
```

**Impact:**
- Faster agent task startup
- Clearer navigation (table format)
- All details still accessible via links

### Example 2: Workflow Guide Over Threshold

**Issue Found:**
```bash
$ wc -l stages/s1/s1_epic_planning.md
1089 stages/s1/s1_epic_planning.md

❌ TOO LARGE: Must reduce or justify
```

**Analysis:**
- File structure: 6 phases (P1-P6) with detailed steps
- Each phase 150-200 lines
- Natural subdivision exists

**Reduction Strategy:**
- Keep s1_epic_planning.md as router (150 lines)
- Extract S1.P3 to s1_p3_discovery_phase.md (400 lines)
- Other phases remain inline (simpler)

**Result:**
```bash
$ wc -l stages/s1/s1_epic_planning.md
650 stages/s1/s1_epic_planning.md

$ wc -l stages/s1/s1_p3_discovery_phase.md
400 stages/s1/s1_p3_discovery_phase.md

✅ PASS: Both files <1000 lines, improved navigation
```

### Example 3: Incremental Growth Not Noticed

**Issue Found:**
```bash
# Git history analysis
$ git log --oneline --all -- stages/s5/s5_p1_planning_round1.md | wc -l
47  # 47 commits to this file

$ git show HEAD~40:stages/s5/s5_p1_planning_round1.md | wc -l
420 lines (6 months ago)

$ wc -l stages/s5/s5_p1_planning_round1.md
685 lines (current)

Growth: +265 lines (+63%) over 6 months
```

**Analysis:**
- No single commit added >50 lines
- Cumulative growth 5-10 lines per commit
- Silent creep: 420 → 685 lines

**Reduction Strategy:**
- Extract detailed iteration instructions to separate i1, i2, i3 files
- Keep router with iteration overview

**Result:**
```bash
$ wc -l stages/s5/s5_p1_planning_round1.md
180 stages/s5/s5_p1_planning_round1.md (router)

$ wc -l stages/s5/s5_p1_i*.md
220 stages/s5/s5_p1_i1_requirements.md
195 stages/s5/s5_p1_i2_algorithms.md
160 stages/s5/s5_p1_i3_integration.md

✅ PASS: All files <600 lines
```

### Example 4: Template Appropriately Large

**Issue Found:**
```bash
$ wc -l templates/epic_readme_template.md
420 templates/epic_readme_template.md

⚠️  LARGE: Consider split?
```

**Analysis:**
- File is a template (copied once, then edited)
- Contains all sections agents need for epic tracking
- Not read repeatedly (used once per epic creation)
- Splitting would make template harder to use

**Decision:**
```text
✅ ACCEPTABLE: Template nature justifies size
- Usage: Copy-once, not repeated reading
- Splitting would reduce usability
- Size appropriate for comprehensive template
```

**No Action Required**

---

## Integration with File Size Reduction Guide

This dimension guide focuses on **detection and evaluation**. For **reduction execution**, see:

**`../reference/file_size_reduction_guide.md`** provides:
- Detailed reduction strategies (4 methods)
- CLAUDE.md reduction protocol (step-by-step)
- Workflow guide reduction protocol
- Validation checklist
- Before/after examples

**Division of Responsibility:**
- **D10 (this guide):** WHAT to check, WHEN files are too large, WHETHER to reduce
- **file_size_reduction_guide.md:** HOW to reduce, step-by-step protocols

---

## See Also

**Related Dimensions:**
- **D1: Cross-Reference Accuracy** - Verify links after splitting files
- **D16: Accessibility & Usability** - Navigation quality (complements file size)

**Audit Stages:**
- `../stages/stage_1_discovery.md` - How to discover large files
- `../stages/stage_2_fix_planning.md` - Planning file size reductions
- `../stages/stage_3_apply_fixes.md` - Executing reductions (MANDATORY step)
- `../stages/stage_4_verification.md` - Verifying size compliance

**Reference:**
- `../reference/file_size_reduction_guide.md` - Complete reduction protocols

**Scripts:**
- `../scripts/pre_audit_checks.sh` - Automated size validation (CHECK 1, CHECK 1b)

---

**When to Use:** Run D10 validation during every audit. File size issues are first-class fixes (not deferred) and must be addressed in Stage 3.
