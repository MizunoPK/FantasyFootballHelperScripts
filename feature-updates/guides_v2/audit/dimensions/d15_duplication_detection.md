# D15: Duplication Detection

**Dimension Number:** 15
**Category:** Advanced Dimensions
**Automation Level:** 50% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-04

**Focus:** Identify duplicate content across guides and enforce DRY principle through consolidation
**Typical Issues Found:** 10-25 duplicate sections per audit

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
9. [Integration with Other Dimensions](#integration-with-other-dimensions)

---

## What This Checks

**D15: Duplication Detection** validates the DRY principle (Don't Repeat Yourself) across guides:

1. **Exact Duplicates** - Same content appears in multiple files verbatim
2. **Near Duplicates** - Very similar content with minor variations (90%+ similarity)
3. **Redundant Instructions** - Same instructions repeated in multiple contexts
4. **Duplicate Examples** - Same examples used in multiple guides
5. **Copied Sections** - Entire sections duplicated across files
6. **Maintenance Burden** - Content that must be updated in multiple places
7. **Consolidation Opportunities** - Content that should be in one place with references

**Coverage:**
- All workflow guides in stages/
- Reference materials in reference/
- Templates in templates/
- Root-level documentation

**Key Distinction:**
- **Acceptable:** Reference or link to canonical source ("See X.md for details")
- **Problematic:** Copy-paste same content into multiple files

---

## Why This Matters

**Duplication = Maintenance burden and inconsistency over time**

### Impact of Duplication:

**Update Overhead:**
- Same content exists in 5 files
- Content needs updating
- Must remember to update all 5 locations
- Easy to miss one location
- Result: Inconsistent information across guides

**Inconsistency Over Time:**
- Content duplicated across files
- One copy updated, others not
- Users see conflicting information
- Don't know which version is correct

**Increased File Size:**
- Duplicated content increases file size unnecessarily
- Files exceed readability thresholds
- Should extract to shared reference instead

**Search Confusion:**
- User searches for topic
- Finds same content in 5 different files
- Doesn't know which is authoritative
- May read outdated version

**Version Drift:**
- File A and File B start with same content
- Over time, A gets updated, B doesn't
- A and B now have conflicting information
- Users confused about which is correct

### Historical Evidence:

**KAI-7 Issues:**
- "Critical Rules" section duplicated in 8 different stage guides
- Gate definitions copy-pasted into multiple files instead of referencing mandatory_gates.md
- Same debugging protocol instructions in multiple stage guides

**Why 50% Automation:**
- Automated: Exact duplicate detection, near-duplicate fuzzy matching
- Manual Required: Semantic duplication (same meaning, different words), determining if duplication is intentional

---

## Pattern Types

### Type 0: Root-Level File Duplication (CRITICAL - Often Missed)

**Files to Always Check:**
```text
C:\Users\kmgam\code\FantasyFootballHelperScripts\CLAUDE.md
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
```

**What to Validate:**

**Common Duplication: Stage Workflow Descriptions**

CLAUDE.md has workflow overview.
README.md has workflow overview.
EPIC_WORKFLOW_USAGE.md has detailed workflow.

**Problem:** If all three describe workflow, updates must happen in 3 places.

**Validation:**
```bash
# Extract workflow section from each root file
grep -A 50 "Stage Workflows\|Workflow Overview" CLAUDE.md > /tmp/claude_workflow.txt
grep -A 50 "10 Stages\|Workflow Overview" feature-updates/guides_v2/README.md > /tmp/readme_workflow.txt
grep -A 50 "Stage-by-Stage" feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md > /tmp/usage_workflow.txt

# Compare for similarity
diff /tmp/claude_workflow.txt /tmp/readme_workflow.txt
diff /tmp/readme_workflow.txt /tmp/usage_workflow.txt
```

**Recommendation:**
- CLAUDE.md: High-level overview (3-5 sentences per stage)
- README.md: Router to guides (just links)
- EPIC_WORKFLOW_USAGE.md: Detailed workflow (comprehensive)

**Red Flags:**
- Same paragraph appears in all 3 files
- Stage descriptions duplicated across files
- Gate lists copy-pasted instead of referenced

**Automated:** ✅ Yes (can detect exact duplicates, near-duplicates)

---

### Type 1: Exact Duplicate Content

**What to Check:**
Same content appears verbatim in multiple files.

**Common Pattern:**

**File A (stages/s5/s5_p1_planning_round1.md):**
```markdown
## Critical Rules

1. Never skip iterations
2. Always run tests before committing
3. Update Agent Status after each phase
4. Zero tech debt tolerance
5. Fix all issues immediately
```

**File B (stages/s6/s6_execution.md):**
```markdown
## Critical Rules

1. Never skip iterations
2. Always run tests before committing
3. Update Agent Status after each phase
4. Zero tech debt tolerance
5. Fix all issues immediately
```

**Problem:** Exact duplicate - if rules change, must update both files.

**Search Commands:**
```bash
# Find exact duplicate sections (>5 lines)
# This requires specialized tooling or manual comparison

# Simple approach: Extract common section headers, compare content
for header in "Critical Rules" "Common Mistakes" "Exit Criteria"; do
  echo "=== Checking duplication of: $header ==="

  # Find all files with this header
  files=$(grep -rl "^## $header" feature-updates/guides_v2/stages/)

  # For each pair, compare content
  # (Manual comparison needed for semantic understanding)
done
```

**Validation Process:**

1. **Identify common sections** across files (Critical Rules, Prerequisites, Exit Criteria)
2. **Extract section content** from each file
3. **Compare line-by-line** for exact matches
4. **Flag duplicates** for consolidation or referencing

**Red Flags:**
- Same multi-line content in 3+ files
- Content is general (applies to all stages), not stage-specific
- Content likely to change over time

**Automated:** ✅ Yes (can detect exact text matches across files)

---

### Type 2: Near-Duplicate Content (90%+ Similarity)

**What to Check:**
Content is nearly identical with minor wording variations.

**Common Pattern:**

**File A:**
```markdown
## Testing Requirements

All code must be tested before committing. Run the full test suite and ensure 100% pass rate. Never commit failing tests.
```

**File B:**
```markdown
## Testing Requirements

All code should be tested before committing. Run the complete test suite and verify 100% pass rate. Do not commit failing tests.
```

**Similarity:** ~90% (must→should, full→complete, ensure→verify, Never→Do not)

**Problem:** Essentially duplicate content with slight variations. Should be consolidated.

**Detection Approach:**

**Using similarity tools:**
```bash
# Install similarity detection tool (if available)
# Example with Python difflib or fuzzywuzzy

# For each pair of files
for file1 in stages/s*/*.md; do
  for file2 in stages/s*/*.md; do
    if [ "$file1" != "$file2" ]; then
      # Compare similarity (requires tool)
      # Flag if >90% similar
    fi
  done
done
```

**Manual Detection:**
```bash
# Extract common section types
grep -rh "^## Testing Requirements\|^## Quality Standards" stages/ > /tmp/testing_sections.txt

# Manually review for near-duplicates
```

**Red Flags:**
- Same meaning expressed with different words
- Same structure, minor wording changes
- Copy-paste then slight editing

**Automated:** ⚠️ Partial (requires fuzzy matching tools like fuzzywuzzy, diff ratio)

---

### Type 3: Redundant Instructions Across Guides

**What to Check:**
Same instructions repeated in context where reference would suffice.

**Common Pattern:**

**Multiple guides explain how to create git branch:**

**S1 Guide:**
```markdown
## Step 1.1: Create Git Branch

Create branch: `git checkout -b epic/KAI-{number}`

Branch naming format: {work_type}/KAI-{number}
Where work_type is: epic, feat, or fix
```

**S10 Guide:**
```markdown
## Create Pull Request

First, ensure you're on correct branch: `git checkout -b epic/KAI-{number}`

Branch naming format: {work_type}/KAI-{number}
Where work_type is: epic, feat, or fix
```

**Problem:** Branch naming rules duplicated. Should reference GIT_WORKFLOW.md instead.

**Recommendation:**

**S1 Guide:**
```markdown
## Step 1.1: Create Git Branch

Create branch following git workflow conventions.
See `reference/GIT_WORKFLOW.md` for branch naming format.

Command: `git checkout -b epic/KAI-{number}`
```

**S10 Guide:**
```markdown
## Create Pull Request

Follow git workflow for PR creation.
See `reference/GIT_WORKFLOW.md` for complete process.
```

**Detection:**
```bash
# Find instructions that appear in multiple guides
common_instructions=(
  "git checkout"
  "Branch naming"
  "Commit message format"
  "Test command"
  "File structure"
)

for instruction in "${common_instructions[@]}"; do
  echo "=== $instruction ==="
  grep -rn "$instruction" stages/ | wc -l
  # If count > 3, may be redundant duplication
done
```

**Red Flags:**
- Same how-to instructions in 5+ files
- Instructions are reference material (should be in reference/)
- Instructions likely to change (maintenance burden)

**Automated:** ✅ Yes (can count occurrences of instruction patterns)

---

### Type 4: Duplicate Examples Across Guides

**What to Check:**
Same examples used in multiple guides instead of referencing common examples.

**Common Pattern:**

**S5 Guide:**
```markdown
### Example: Missing Import Error

**Problem:** Code fails with "ModuleNotFoundError"
**Cause:** Missing import statement
**Solution:** Add `import pandas as pd`
**Result:** Code executes successfully
```

**S7 Guide:**
```markdown
### Example: Import Error During Testing

**Problem:** Test fails with "ModuleNotFoundError"
**Cause:** Missing import statement
**Solution:** Add `import pandas as pd`
**Result:** Tests pass
```

**Problem:** Same example duplicated with slight context changes.

**Recommendation:**

**Create shared examples file:**
```text
reference/common_examples.md
```

**S5 and S7 both reference:**
```markdown
See `reference/common_examples.md` → "Missing Import Error" for debugging approach.
```

**Detection:**
```bash
# Find example sections
grep -rn "^### Example\|^## Example" stages/ > /tmp/all_examples.txt

# Manually review for duplicates
# Look for same scenario, problem, solution patterns
```

**Red Flags:**
- Same scenario described in multiple examples
- Same code snippets in multiple examples
- Same problem-solution pairs

**Automated:** ❌ No (requires semantic understanding of example content)

---

### Type 5: Entire Section Duplication

**What to Check:**
Large sections (50+ lines) duplicated across files.

**Common Pattern:**

**Prerequisites Section Duplication:**

Many stage guides have identical "Prerequisites" boilerplate:
```markdown
## Prerequisites

Before starting this stage:

- [ ] Read the complete guide using Read tool
- [ ] Use mandatory phase transition prompt
- [ ] Verify prerequisites checklist
- [ ] Update Agent Status in README
- [ ] THEN proceed with work
```

**If this appears in 10 stage guides identically, it's duplication.**

**Recommendation:**

**Create shared prerequisite template:**
```text
reference/standard_prerequisites.md
```

**Stage guides reference:**
```markdown
## Prerequisites

**Standard Prerequisites:**
See `reference/standard_prerequisites.md` for standard workflow prerequisites.

**Stage-Specific Prerequisites:**
- [ ] Completed S4
- [ ] test_strategy.md exists
- [ ] User approved epic plan (Gate 4.5)
```

**Detection:**
```bash
# Find large sections (>50 lines)
for file in stages/**/*.md; do
  # Extract major sections
  csplit -s -f /tmp/section_ "$file" '/^## /' '{*}' 2>/dev/null

  # For each section, compare to sections in other files
  # (Requires tooling or manual review)
done
```

**Red Flags:**
- Same 50+ line section in 5+ files
- Section is general, not file-specific
- Section changes occasionally (maintenance burden)

**Automated:** ⚠️ Partial (can detect exact matches, requires fuzzy matching for near-duplicates)

---

### Type 6: Duplicate Reference Lists

**What to Check:**
Same reference lists (See Also, Additional Resources) duplicated across files.

**Common Pattern:**

**Multiple guides have same "See Also" section:**

**S2, S3, S4, S5 all have:**
```markdown
## See Also

- `reference/mandatory_gates.md` - Complete gate reference
- `reference/common_mistakes.md` - Anti-pattern reference
- `reference/GIT_WORKFLOW.md` - Git branching workflow
- `CODING_STANDARDS.md` - Coding standards
```

**Problem:** Duplicated reference lists. If new reference added, must update all files.

**Recommendation:**

**Create master reference index:**
```text
reference/REFERENCE_INDEX.md
```

**Guides reference index:**
```markdown
## See Also

See `reference/REFERENCE_INDEX.md` for complete reference list.

**Stage-Specific:**
- `stages/s6/s6_execution.md` - Implementation guide
- `stages/s7/s7_testing.md` - Testing guide
```

**Detection:**
```bash
# Extract all "See Also" sections
grep -A 10 "^## See Also" stages/**/*.md > /tmp/see_also_sections.txt

# Compare for duplication
# Count unique vs total
```

**Red Flags:**
- Same reference list in 5+ files
- References are general (not file-specific)
- List grows over time (maintenance burden)

**Automated:** ✅ Yes (can detect exact duplicate lists)

---

### Type 7: Template Content Propagation

**What to Check:**
Templates create duplicates by design - content appears in all instances.

**Pattern:**

**Template creates boilerplate:**
```markdown
# templates/feature_spec_template.md

## Common Pitfalls

1. Forgetting to run tests
2. Skipping user approval
3. Not updating Agent Status
```

**Every feature spec has this section.**

**Evaluation:**

**ACCEPTABLE if:**
- Content is placeholder to be filled in with feature-specific pitfalls
- Each instance customized for that feature

**PROBLEMATIC if:**
- Content is generic, never customized
- Same text appears in 20 feature specs
- Should be in reference material instead

**Detection:**
```bash
# Find content that appears in many instances
# Compare all feature_XX/spec.md files

common_sections=$(grep -rh "^## Common Pitfalls" feature-updates/KAI-*/feature_*/spec.md | sort | uniq)

# If all identical, template content not being customized
```

**Recommendation:**

**If generic content:**
```markdown
# template: Don't include generic content

## Common Pitfalls

[List feature-specific pitfalls here]

**See:** `reference/common_pitfalls.md` for general pitfalls
```

**Red Flags:**
- Template creates non-customizable boilerplate
- All instances have identical content
- Content is reference material, not feature-specific

**Automated:** ⚠️ Partial (can detect identical content across instances, requires judgment on acceptability)

---

## How Errors Happen

### Root Cause 1: Copy-Paste for Consistency

**Scenario:**
- Need to add "Critical Rules" to S5 guide
- S2 guide has good "Critical Rules" section
- Copy entire section from S2 to S5
- **RESULT:** Same content in both files

**Better Approach:**
- Create `reference/critical_rules.md`
- Both S2 and S5 reference: "See reference/critical_rules.md"

---

### Root Cause 2: Template Boilerplate Not Customized

**Scenario:**
- Feature template includes generic "Prerequisites" section
- User creates 20 features from template
- Never customizes Prerequisites (leaves template text)
- **RESULT:** Same Prerequisites in 20 feature specs

**Better Approach:**
- Template includes: "[Customize this - list feature-specific prerequisites]"
- Forces user to replace with feature-specific content

---

### Root Cause 3: Reference Material in Multiple Places

**Scenario:**
- Git workflow instructions needed in S1 and S10
- Instead of creating reference/GIT_WORKFLOW.md once
- Same instructions copy-pasted into both guides
- **RESULT:** Must update 2 places when git workflow changes

---

### Root Cause 4: Examples Not Extracted to Shared Library

**Scenario:**
- Multiple guides need same example (e.g., "Missing Import Error")
- Each guide includes full example
- Example appears in 5 guides
- **RESULT:** Example fix requires updating 5 files

**Better Approach:**
- Create `reference/common_examples.md`
- Guides reference: "See common_examples.md → Missing Import Error"

---

### Root Cause 5: Consolidation Effort Not Prioritized

**Scenario:**
- Duplication identified during audit
- "We'll fix it later" decision
- Later never comes
- **RESULT:** Duplication persists, creates maintenance burden

---

## Automated Validation

### Pre-Audit Script Coverage

**From `scripts/pre_audit_checks.sh`:**

**CHECK 19: Exact Duplicate Detection** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Checking for exact duplicate sections..."

# Find common section headers
headers=$(grep -rh "^## " stages/ | sort | uniq -c | sort -rn | head -20 | awk '{$1=""; print $0}')

for header in $headers; do
  # Extract content for this header from all files
  files=$(grep -rl "^## $header" stages/)

  # Compare content across files
  temp_files=()
  for file in $files; do
    # Extract section content (from header to next header)
    awk "/^## $header/,/^## /" "$file" > /tmp/"$(basename $file)_$header.txt"
    temp_files+=("/tmp/$(basename $file)_$header.txt")
  done

  # Find duplicates
  for ((i=0; i<${#temp_files[@]}; i++)); do
    for ((j=i+1; j<${#temp_files[@]}; j++)); do
      if diff -q "${temp_files[$i]}" "${temp_files[$j]}" > /dev/null; then
        echo "DUPLICATE: $header section identical in ${temp_files[$i]} and ${temp_files[$j]}"
      fi
    done
  done
done
```

**CHECK 20: Instruction Duplication Count** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Checking for redundant instructions..."

# Common instruction patterns
patterns=(
  "git checkout -b"
  "Branch naming format"
  "Commit message format"
  "run tests"
  "Agent Status"
)

for pattern in "${patterns[@]}"; do
  count=$(grep -rc "$pattern" stages/ | awk -F: '{sum+=$2} END {print sum}')
  files=$(grep -rl "$pattern" stages/ | wc -l)

  if [ "$files" -gt 5 ]; then
    echo "WARNING: '$pattern' appears in $files files ($count total occurrences)"
    echo "  Consider creating reference file"
  fi
done
```

**Automation Coverage: ~50%**
- ✅ Exact duplicate detection
- ✅ Instruction duplication counting
- ⚠️ Near-duplicate detection (requires fuzzy matching)
- ❌ Semantic duplication (same meaning, different words)
- ❌ Determining if duplication is intentional/acceptable

---

## Manual Validation

### Manual Process (Duplication Audit)

**Duration:** 60-90 minutes
**Frequency:** Quarterly, after major guide additions

**Step 1: Identify Common Sections (15 min)**

```bash
# Find most common section headers
grep -rh "^## " stages/ reference/ | sort | uniq -c | sort -rn | head -30

# Common sections typically:
# - Critical Rules
# - Prerequisites
# - Exit Criteria
# - Common Mistakes
# - Examples
# - See Also
```

**For each common section:**
1. Note how many files contain it
2. If >5 files, investigate for duplication

**Step 2: Compare Content of Common Sections (20 min)**

```bash
# For each common section (e.g., "Critical Rules")
header="Critical Rules"

# Extract from all files
for file in $(grep -rl "^## $header" stages/); do
  echo "=== $file ==="
  awk "/^## $header/,/^## /" "$file"
  echo ""
done > /tmp/critical_rules_comparison.txt

# Manually review for duplicates
cat /tmp/critical_rules_comparison.txt
```

**Questions to ask:**
- Is content identical across files?
- Is content nearly identical (>90% similar)?
- Is content generic (applies to all stages) or stage-specific?
- If duplicated, should it be consolidated?

**Step 3: Search for Duplicate Instructions (15 min)**

```bash
# Common instructions likely to be duplicated
instructions=(
  "Create git branch"
  "Commit format"
  "Run tests"
  "Update Agent Status"
  "User approval"
)

for instr in "${instructions[@]}"; do
  echo "=== $instr ==="
  grep -rn "$instr" stages/ | head -10
  count=$(grep -rc "$instr" stages/ | awk -F: '{sum+=$2} END {print sum}')
  echo "Total occurrences: $count"
  echo ""
done
```

**For high-count instructions:**
- Check if same text appears in multiple places
- Determine if should be in reference file instead

**Step 4: Review Examples for Duplication (20 min)**

```bash
# Extract all examples
grep -B 2 -A 10 "^### Example" stages/**/*.md > /tmp/all_examples.txt

# Manually review for:
# - Same scenario in multiple examples
# - Same code snippets
# - Same problem-solution pairs
```

**Create spreadsheet:**

| Example Topic | Files | Similarity | Action Needed |
|---------------|-------|------------|---------------|
| Missing Import | S5, S7, S9 | High | Consolidate to common_examples.md |
| Logic Error | S6, S7 | Medium | Keep separate (context-specific) |
| ... | ... | ... | ... |

**Step 5: Evaluate Consolidation Opportunities (20 min)**

For each duplicate found:

**Decision Matrix:**

| Duplication Type | Action |
|------------------|--------|
| Exact duplicate, generic content | **CONSOLIDATE** - Create reference file |
| Near-duplicate, minor variations | **STANDARDIZE** - Consolidate to one version |
| Similar, different context | **KEEP** - Duplication acceptable |
| Template boilerplate | **EVALUATE** - Should it be customized or referenced? |

**Consolidation Process:**
1. Create reference file with canonical content
2. Update all guides to reference (not duplicate)
3. Delete duplicated content from guides

---

## Context-Sensitive Rules

### Rule 1: Intentional Duplication for Critical Rules

**Context:** Some rules are SO critical they're intentionally duplicated for visibility.

**Example:**
```markdown
# S5, S6, S7 all have:

## Critical Rule

NEVER commit without running tests first. 100% test pass rate required.
```

**Evaluation:**
- Is rule truly critical? (commits without tests = high risk)
- Is duplication intentional for emphasis?
- Is content stable (rarely changes)?

**Validation:** If rule is critical, stable, and intentionally duplicated for emphasis → ACCEPTABLE

**Recommendation:** Add comment in guides:
```markdown
## Critical Rule

[NOTE: Intentionally duplicated across S5-S7 for emphasis]

NEVER commit without running tests first. 100% test pass rate required.
```

---

### Rule 2: Template Boilerplate Intended for Customization

**Context:** Templates create instances with same initial content, intended to be customized.

**Example:**
```markdown
# template creates:

## Prerequisites

- [ ] Previous stage complete
- [ ] Required files exist
- [ ] User approval received
```

**Evaluation:**
- Is template content placeholder?
- Is customization expected?
- Do instances actually customize it?

**Validation:** If template creates customizable placeholders AND instances customize them → ACCEPTABLE

**Problematic:** If all instances have identical template content (not customized) → DUPLICATION ISSUE

---

### Rule 3: Examples Demonstrating Same Pattern in Different Contexts

**Context:** Same pattern shown in different stage contexts may be intentional.

**Example:**

**S5 Example:** Missing import during planning
**S7 Example:** Missing import discovered during testing

**Same problem, different discovery context.**

**Evaluation:**
- Does context matter?
- Do examples emphasize different aspects?
- Would consolidation lose context-specific value?

**Validation:** If context adds value → ACCEPTABLE

---

### Rule 4: High-Level vs Detailed Duplication

**Context:** Root files may duplicate detailed guides at high level.

**Example:**

**CLAUDE.md:** 2-sentence stage summary
**stages/sN/guide.md:** 500-line detailed guide

**Overlap:** Both describe stage, but different levels of detail.

**Validation:** High-level summary + link to detailed guide → ACCEPTABLE (not duplication)

**Problematic:** Both have 50-line detailed descriptions → DUPLICATION

---

## Real Examples

### Example 1: Critical Rules Duplicated Across 8 Guides

**Issue Found During KAI-7 Audit:**

**Duplication:**
```markdown
# S2, S3, S4, S5, S6, S7, S8, S9 all had identical section:

## Critical Rules

1. Always read guide before starting
2. Use mandatory phase transition prompts
3. Update Agent Status after each phase
4. Zero tech debt tolerance
5. Fix all issues immediately
```

**Problem:**
- 8 files with same content
- If rules change, must update 8 files
- High maintenance burden

**Solution:**

**Created:** `reference/critical_workflow_rules.md`

**All guides updated to:**
```markdown
## Critical Rules

See `reference/critical_workflow_rules.md` for universal workflow rules.

**Stage-Specific Rules:**
- [Stage-specific rules here]
```

**Result:**
- Single source of truth
- Updates in one place
- Guides focus on stage-specific rules

**Root Cause:** Copy-paste for consistency without consolidation

**How D15 Detects:**
- Type 1: Exact Duplicate Content
- Type 5: Entire Section Duplication
- Automated: CHECK 19 detects identical sections

---

### Example 2: Git Instructions Duplicated in S1 and S10

**Issue Found During Documentation Review:**

**S1 Guide:**
```markdown
## Step 1.1: Create Git Branch

Create branch using format: {work_type}/KAI-{number}

Where work_type is:
- epic: For epic-level work
- feat: For feature additions
- fix: For bug fixes

Command: `git checkout -b epic/KAI-{number}`
```

**S10 Guide:**
```markdown
## Create Pull Request

Ensure you're on correct branch format: {work_type}/KAI-{number}

Where work_type is:
- epic: For epic-level work
- feat: For feature additions
- fix: For bug fixes

Use: `git checkout -b epic/KAI-{number}` if needed
```

**Problem:**
- Branch naming rules duplicated
- Git commands duplicated
- Should reference GIT_WORKFLOW.md

**Solution:**

**Both guides updated to:**
```markdown
See `reference/GIT_WORKFLOW.md` for branch naming and git commands.
```

**Result:**
- Git workflow in one canonical location
- Guides reference, don't duplicate

**Root Cause:** Reference material embedded in guides instead of extracted

**How D15 Detects:**
- Type 3: Redundant Instructions Across Guides
- Automated: CHECK 20 counts instruction occurrences

---

### Example 3: Missing Import Example in 5 Guides

**Issue Found During Example Review:**

**S5, S6, S7, S9, Debugging Protocol all had:**
```markdown
### Example: Missing Import Error

**Problem:** Code fails with "ModuleNotFoundError: No module named 'pandas'"
**Cause:** Missing import statement
**Solution:** Add `import pandas as pd` at top of file
**Result:** Code executes successfully
```

**Problem:**
- Same example in 5 places
- If example needs updating (e.g., better debugging tip), must update 5 files

**Solution:**

**Created:** `reference/common_examples.md`

**Included:**
- Missing Import Error
- Logic Error Examples
- Configuration Error Examples
- Common Debugging Patterns

**Guides updated to:**
```markdown
### Example: Missing Import

See `reference/common_examples.md` → "Missing Import Error" for debugging approach.
```

**Result:**
- Examples in one location
- Guides reference by name
- Easy to maintain and expand

**Root Cause:** Examples not extracted to shared library

**How D15 Detects:**
- Type 4: Duplicate Examples Across Guides
- Manual validation: Compare example content

---

### Example 4: Template Boilerplate Never Customized

**Issue Found During Feature Spec Review:**

**Template:** `templates/feature_spec_template.md`
```markdown
## Common Pitfalls

1. Forgetting to run tests before committing
2. Skipping user approval gates
3. Not updating Agent Status regularly
4. Deferring issues for later
5. Skipping validation loops
```

**All 12 features in KAI-7 had identical "Common Pitfalls" section.**

**Problem:**
- Generic pitfalls, not feature-specific
- Template content never customized
- Should be reference material

**Solution:**

**Template updated to:**
```markdown
## Common Pitfalls

[List feature-specific pitfalls discovered during implementation]

**See:** `reference/common_pitfalls.md` for general workflow pitfalls
```

**Existing features:**
- Generic content removed
- Feature-specific pitfalls added

**Result:**
- Feature specs have feature-specific content
- Generic content in reference file

**Root Cause:** Template created generic content without customization prompt

**How D15 Detects:**
- Type 7: Template Content Propagation
- Manual validation: Check if template instances identical

---

### Example 5: Prerequisites Boilerplate in All Stage Guides

**Issue Found During Stage Guide Review:**

**All 10 stage guides started with:**
```markdown
## Prerequisites

Before starting this stage:

- [ ] Read the complete guide using Read tool
- [ ] Use mandatory phase transition prompt from prompts_reference_v2.md
- [ ] Verify prerequisites checklist
- [ ] Update Agent Status in README with current guide path
- [ ] THEN proceed with work
```

**Problem:**
- Same 5 items in all guides
- If standard prerequisite process changes, must update 10 files

**Solution:**

**Created:** `reference/standard_prerequisites.md`

**Stage guides updated to:**
```markdown
## Prerequisites

**Standard Prerequisites:**
See `reference/standard_prerequisites.md`

**Stage-Specific Prerequisites:**
- [ ] Completed [Previous Stage]
- [ ] [Stage-specific file] exists
- [ ] [Stage-specific approval] received
```

**Result:**
- Standard prerequisites in one place
- Guides focus on stage-specific prerequisites
- Clear separation

**Root Cause:** Standard boilerplate not extracted to shared reference

**How D15 Detects:**
- Type 5: Entire Section Duplication
- Automated: CHECK 19 detects identical Prerequisites sections

---

## Integration with Other Dimensions

### D5: Content Completeness

**Overlap:**
- D5 validates required content exists
- D15 validates content doesn't exist redundantly
- **Division:** D5 = presence, D15 = non-duplication

**Example:**
- D5 checks: Guide has "Examples" section ✅
- D15 checks: Examples aren't duplicated across guides ✅

---

### D11: Structural Patterns

**Overlap:**
- D11 validates structural consistency
- D15 validates structure isn't duplicated unnecessarily
- **Division:** D11 = consistency, D15 = consolidation

**Example:**
- D11 checks: All guides have Prerequisites section (consistent) ✅
- D15 checks: Prerequisites content isn't duplicated (consolidated) ✅

---

### D12: Cross-File Dependencies

**Overlap:**
- D12 validates file references are correct
- D15 validates content is referenced, not duplicated
- **Division:** D12 = references work, D15 = prefer references over duplication

**Example:**
- D12 checks: Reference to common_examples.md exists and valid ✅
- D15 checks: Examples are referenced, not copy-pasted ✅

---

### D14: Content Accuracy

**Overlap:**
- D14 validates claims are correct
- D15 validates claims aren't duplicated
- **Division:** D14 = correctness, D15 = efficiency

**Example:**
- D14 checks: Gate count "10 gates" is accurate ✅
- D15 checks: Gate list isn't duplicated, references mandatory_gates.md ✅

---

## Summary

**D15: Duplication Detection validates the DRY principle across guides.**

**Key Validations:**
1. ✅ Exact duplicate detection
2. ⚠️ Near-duplicate detection (fuzzy matching)
3. ✅ Redundant instruction counting
4. ❌ Duplicate example detection (manual)
5. ⚠️ Section duplication detection
6. ✅ Reference list duplication
7. ⚠️ Template propagation evaluation

**Automation: ~50%**
- Automated for exact duplicates, instruction counts
- Manual for semantic duplication, consolidation decisions

**Critical for:**
- Reducing maintenance burden (single source of truth)
- Preventing inconsistency over time (one update point)
- Improving file readability (extract to references)
- DRY principle adherence

**Next Dimension:** D7: Context-Sensitive Validation (distinguishing intentional exceptions from errors)

---

**Last Updated:** 2026-02-04
**Version:** 1.0
**Status:** ✅ Fully Implemented
