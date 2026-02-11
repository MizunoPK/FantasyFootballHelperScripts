# D10: File Size Assessment

**Dimension Number:** 10
**Category:** Structural Dimensions
**Automation Level:** 100% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-05

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
- CRITICAL: >1250 lines (exceeds baseline - must reduce or justify)
- ACCEPTABLE: ≤1250 lines (within baseline - OK if content non-duplicated)

**Updated Policy:**
- **2026-02-05:** Simplified from 3-tier threshold (600/800/1000) to single 1000-line baseline
- **2026-02-05 (Meta-Audit):** Increased baseline from 1000 → 1250 lines to accommodate comprehensive reference guides while maintaining agent usability

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
```markdown

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
```markdown

**Automated:** ✅ Yes (CHECK 1b in pre_audit_checks.sh)

### Type 1: Critical Size Files (>1250 lines)

**What to Check:**
- Any workflow guide >1250 lines
- Indicates substantial content that likely has natural subdivisions
- MUST reduce or provide strong justification

**Search Command:**
```bash
# Find files >1250 lines
find stages reference templates -name "*.md" -exec wc -l {} \; | \
  awk '$1 > 1250 {print $1, $2}' | \
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
```markdown

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
```markdown

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
```markdown

**After (WRONG):**
```text
s5_planning.md (1200 lines) ← Direct concatenation
```

**Better Approach:**
```text
s5_planning.md (200 lines) ← Router to sub-guides
s5_v2_validation_loop.md (400 lines)
s5_v2_validation_loop.md (350 lines)
s5_v2_validation_loop.md (450 lines)
```markdown

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
```markdown

**Result:** Section grows from 3 lines → 225 lines

**Better Approach:**
```markdown
## Step 3: Create Spec
Create spec.md using template.
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

  if [ "$lines" -gt 1250 ]; then
    echo "❌ TOO LARGE: $file ($lines lines)"
    ((TOO_LARGE++))
  fi
done

echo "Files >1250 lines: $TOO_LARGE"
```bash

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
```diff

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

**See:** `reference/file_size_reduction_guide.md` for complete reduction protocols

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
```diff

**For workflow guides >1250 lines:**

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
$ wc -l new_files.md  # All should be <1000 lines ideally
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
```yaml

**2. Pattern Libraries:**
```markdown
File: audit/reference/pattern_library.md (650 lines)
Content: Search patterns organized by category
Verdict: ✅ ACCEPTABLE (lookup reference, not read start-to-finish)
```

**3. Comprehensive Templates:**
```markdown
File: templates/epic_readme_template.md (400 lines)
Content: Complete template with all sections
Verdict: ✅ ACCEPTABLE (copied then edited, not read repeatedly)
```yaml

### When Large Files Are Errors

**1. Sequential Workflow Guides:**
```markdown
File: stages/s5/s5_v2_validation_loop.md (1400 lines)
Content: Step-by-step instructions for S5
Verdict: ❌ ERROR (agents must read sequentially, too long)
Fix: Split into s5_p1, s5_p2, s5_p3 (400-500 lines each)
```

**2. Root Entry Point Files:**
```markdown
File: CLAUDE.md (45,786 characters)
Content: Project instructions
Verdict: ❌ POLICY VIOLATION (exceeds 40,000 char limit)
Fix: Extract to EPIC_WORKFLOW_USAGE.md, keep quick reference
```yaml

**3. Guides with Multiple Purposes:**
```markdown
File: stages/s2/s2_feature_deep_dive.md (950 lines)
Content: Research + Specification + Refinement (3 phases)
Verdict: ⚠️ LARGE (should split into phase files)
Fix: Create s2_p1_spec_creation_refinement.md, s2_p2_specification.md, s2_p3_refinement.md
```

---

## Real Examples

### Example 1: CLAUDE.md Policy Violation (Critical)

**Issue Found:**
```bash
$ wc -c CLAUDE.md
45786 CLAUDE.md

POLICY VIOLATION: 5,786 characters over 40,000 limit
```diff

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
1289 stages/s1/s1_epic_planning.md

❌ TOO LARGE: Must reduce or justify
```diff

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
850 stages/s1/s1_epic_planning.md

$ wc -l stages/s1/s1_p3_discovery_phase.md
400 stages/s1/s1_p3_discovery_phase.md

✅ PASS: Both files <1250 lines, improved navigation
```

### Example 3: Incremental Growth Not Noticed

**Issue Found:**
```bash
# Git history analysis
$ git log --oneline --all -- stages/s5/s5_v2_validation_loop.md | wc -l
47  # 47 commits to this file

$ git show HEAD~40:stages/s5/s5_v2_validation_loop.md | wc -l
420 lines (6 months ago)

$ wc -l stages/s5/s5_v2_validation_loop.md
685 lines (current)

Growth: +265 lines (+63%) over 6 months
```diff

**Analysis:**
- No single commit added >50 lines
- Cumulative growth 5-10 lines per commit
- Silent creep: 420 → 685 lines

**Reduction Strategy:**
- Extract detailed iteration instructions to separate i1, i2, i3 files
- Keep router with iteration overview

**Result:**
```bash
$ wc -l stages/s5/s5_v2_validation_loop.md
180 stages/s5/s5_v2_validation_loop.md (router)

$ wc -l stages/s5/s5_p1_i*.md
220 stages/s5/s5_p1_i1_requirements.md
195 stages/s5/s5_p1_i2_algorithms.md
160 stages/s5/s5_p1_i3_integration.md

✅ PASS: All files well under 1250-line baseline
```

### Example 4: Template Appropriately Large

**Issue Found:**
```bash
$ wc -l templates/epic_readme_template.md
420 templates/epic_readme_template.md

⚠️  LARGE: Consider split?
```diff

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

**`reference/file_size_reduction_guide.md`** provides:
- Detailed reduction strategies (4 methods)
- CLAUDE.md reduction protocol (step-by-step)
- Workflow guide reduction protocol
- Validation checklist
- Before/after examples

**Division of Responsibility:**
- **D10 (this guide):** WHAT to check, WHEN files are too large, WHETHER to reduce
- **file_size_reduction_guide.md:** HOW to reduce, step-by-step protocols

---

## Acceptance Criteria for Files Near Threshold

**Updated:** 2026-02-05 (Meta-Audit - baseline increased to 1250 lines)

### Files 1250-1300 Lines: Case-by-Case Evaluation

**Philosophy:** Not all files >1250 lines are violations. Comprehensive guides may legitimately need ~1250 lines if content is non-duplicated and serves the guide's purpose.

**Acceptance Criteria:**

✅ **ACCEPT as legitimate complexity when:**
1. **Content is non-duplicated** (no sections copying from other guides)
2. **File serves single cohesive purpose** (not multiple unrelated workflows)
3. **Only slightly over threshold** (1250-1300 lines, not 1500+)
4. **Whitespace is reasonable** (<30% blank lines + separators)
5. **Content cannot be reasonably reduced** without harming usability
6. **Critical workflows require inline context** (extracting would cause navigation barriers)

❌ **REDUCE when:**
1. **Content duplicates other guides** (apply Strategy 0: Reduce Duplication)
2. **Embedded templates** can be extracted (apply Strategy 2: Extract to Templates)
3. **Excessive whitespace** (>35% blank lines, can be tightened)
4. **Multiple unrelated workflows** (apply Strategy 1: Break into Sequential Phases)
5. **Verbose examples** that could be condensed or moved to appendices

### Current Accepted Files (Under New 1250 Baseline)

**As of Meta-Audit (2026-02-05), all previously borderline files now well under threshold:**

**Former borderline files (now under 1250):**

**1. stages/s1/s1_p3_discovery_phase.md (1006 lines)**
- **Status:** ✅ Well under 1250 baseline (244 lines of headroom)
- **No action needed**

**2. stages/s8/s8_p2_epic_testing_update.md (1010 lines)**
- **Status:** ✅ Well under 1250 baseline (240 lines of headroom)
- **No action needed**

### Monitoring for New Files Near Threshold

**Watch for files approaching new baseline:**
- **1250-1300 lines:** Acceptable with justification (case-by-case evaluation)
- **1300-1350 lines:** Should investigate reduction opportunities
- **>1350 lines:** Must reduce (clear violation)

### Historical Context

**Before Round 3 (Round 1-2):**
- Used 3-tier threshold: 600 (WARNING), 800 (LARGE), 1000 (CRITICAL)
- Created 32 violations (18 WARNING + 10 LARGE + 4 CRITICAL)
- 75% of flagged files were false positives

**After Round 3:**
- Simplified to single 1000-line baseline
- Reduced violations from 32 → 4 (75% reduction)
- Applied Strategy 0 to reduce: s1 (1017→978), s3 (1019→948)
- Accepted 2 files as legitimate complexity (s1_p3: 1006, s8_p2: 1010)
- Net result: 0 files requiring action

**After Meta-Audit (2026-02-05):**
- Increased baseline from 1000 → 1250 lines
- Rationale: Dimension reference guides (d1-d16) legitimately need 1000-1200 lines for comprehensive coverage
- Agent usability maintained (comprehensive guides acceptable if well-structured)
- 6 dimension files were 1104-1324 lines → 3 now under threshold, 3 still require reduction

**Philosophy Evolution:**
- Round 1-2: "All files >600 lines should be smaller"
- Round 3: "Files ≤1000 lines OK if content justified"
- Meta-Audit: "Files ≤1250 lines OK if comprehensive reference content justified"

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
- `reference/file_size_reduction_guide.md` - Complete reduction protocols

**Scripts:**
- `../scripts/pre_audit_checks.sh` - Automated size validation (CHECK 1, CHECK 1b)

---

**When to Use:** Run D10 validation during every audit. File size issues are first-class fixes (not deferred) and must be addressed in Stage 3.
