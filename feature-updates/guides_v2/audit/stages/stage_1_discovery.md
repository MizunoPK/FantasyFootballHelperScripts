# Stage 1: Discovery

**Purpose:** Find issues using systematic search patterns with fresh eyes
**Duration:** 30-60 minutes per round
**Output:** Discovery report with categorized issues
**Reading Time:** 15-20 minutes

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Discovery Philosophy](#discovery-philosophy)
4. [Discovery Strategy](#discovery-strategy)
5. [Discovery Execution](#discovery-execution)
6. [Documentation Format](#documentation-format)
7. [Exit Criteria](#exit-criteria)
8. [Common Pitfalls](#common-pitfalls)

---

## Overview

### Purpose

**Stage 1: Discovery** is where you find issues that need fixing. The goal is to:
- Search systematically using multiple pattern types
- Document every issue found with evidence
- Categorize issues by audit dimension
- Prepare for Stage 2 (Fix Planning)

### Mindset

**CRITICAL:** Approach this with "fresh eyes" - assume you know NOTHING about the codebase.

```
❌ WRONG: "I already know where the issues are from last round"
✅ CORRECT: "I'll search systematically as if I've never seen this before"

❌ WRONG: "This folder probably doesn't have issues"
✅ CORRECT: "I'll check EVERY folder, regardless of assumptions"

❌ WRONG: "Grep returned zero, I'm done"
✅ CORRECT: "Grep returned zero, let me try 4 more pattern variations"
```

### Duration Expectations

- **Round 1:** 45-60 minutes (broad initial search)
- **Round 2:** 30-45 minutes (focused pattern variations)
- **Round 3+:** 30-60 minutes (context-sensitive, manual reading)

---

## Prerequisites

### Before Starting Discovery

**Verify ALL of these are complete:**

- [ ] Fresh terminal session (cleared history, no bias from previous work)
- [ ] Current working directory: `feature-updates/guides_v2/`
- [ ] All previous round assumptions cleared (took 5-minute break if continuing)
- [ ] New notepad/file ready for THIS round's findings
- [ ] Do NOT look at previous round notes until AFTER discovery complete
- [ ] Round counter incremented (Round 1, Round 2, etc.)
- [ ] Identified what changed since last guide update (if triggered by specific change)

### Mental Model Reset

**If this is Round 2+:**

Take a genuine 5-minute break before starting. Do NOT:
- Look at previous discovery reports
- Review previous patterns
- Assume you remember what you found

Instead:
- Clear mental model
- Approach with skepticism
- Question everything fresh

---

## Discovery Philosophy

### Principles Over Prescriptions

**This guide teaches HOW to create patterns, not just which patterns to run.**

**Why?**
- Future guide updates will create NEW error patterns
- Prescriptive checklists only catch known issues
- Principle-based approach adapts to any changes

**Core Principle:** Ask "What changed?" → Infer patterns → Search for stragglers

### The Pattern Generation Process

```
Step 1: Understand What Changed
  ↓
Step 2: List All Old Patterns (what should no longer exist)
  ↓
Step 3: Brainstorm Pattern Variations (how might it appear?)
  ↓
Step 4: Create Search Commands (grep, find, sed)
  ↓
Step 5: Execute Systematically (priority order)
  ↓
Step 6: Document ALL Findings (even if unsure)
```

---

## Discovery Strategy

### STEP 1: Understand What Changed

**If audit triggered by specific change:**

Ask yourself:
- What file names changed?
- What notation changed?
- What stage numbers changed?
- What folder structure changed?
- What terminology changed?

**Example: After S5 split into S5-S8**
```
Changes:
- Stage 5a → S5.P1
- Stage 5b → S5.P2
- Stage 6 → S9
- Stage 7 → S10
- File: stage_5a_planning.md → s5_p1_planning_round1.md
```

**If general maintenance audit:**

Focus on common issue types:
- Cross-references (D1)
- Terminology (D2)
- File sizes (D10)
- Missing sections (D13)
- Run automated pre-checks first

### STEP 2: List All Old Patterns

**Based on what changed, list what should NO LONGER exist:**

**Example: After notation change**
```markdown
Old Patterns (should be gone):
- " 5a" (space before)
- "5a:" (colon after)
- "Stage 5a"
- "S5a"
- "Proceed to 5a"
- "Restart 5b"
- "Complete 5c"
```

**Template:**
```markdown
Old Patterns for [CHANGE TYPE]:
1. [exact old string]
2. [old string with punctuation]
3. [old string in sentence context]
4. [old string in file names]
5. [old string in headers]
```

### STEP 3: Brainstorm Pattern Variations

**For each old pattern, think about ALL ways it might appear:**

**Punctuation Variations:**
```
Base: "5a"
- "5a:", "5a-", "5a.", "5a)", "(5a", "5a,"
- " 5a ", "5a\n", "\n5a"
```

**Context Variations:**
```
- Action verbs: "back to 5a", "restart 5a", "proceed to 5a", "complete 5a"
- Descriptive: "in 5a", "during 5a", "from 5a", "after 5a"
- Comparisons: "5a vs 5b", "5a or 5b", "5a and 5b"
```

**Header Variations:**
```
- "## 5a:", "### Stage 5a", "#### 5a -"
- "# Part 5a", "## Section 5a"
```

**File Name Variations:**
```
- "5a_planning.md"
- "stage_5a_"
- "part_5a"
- "round_5a"
```

**Case Variations:**
```
- "Stage 5A" (uppercase)
- "STAGE 5a" (mixed)
```

### STEP 4: Create Search Commands

**For each variation, create grep command:**

```bash
# Base pattern (exact match with word boundaries)
grep -rn "\b5a\b" --include="*.md"

# Punctuation variations
grep -rn "5a:\|5a-\|5a\.\|5a)" --include="*.md"

# Arrow/sequence variations
grep -rn "5a →\|→ 5a\|5a→\|→5a" --include="*.md"

# Action variations
grep -rn "back to 5[a-e]\|restart 5[a-e]\|proceed to 5[a-e]" --include="*.md" -i

# Header variations (line start)
grep -rn "^## 5[a-e]\|^### Stage 5[a-e]" --include="*.md"

# In file paths/names
find . -name "*5a*" -o -name "*5b*" -o -name "*5c*"
```

**Command Template:**
```bash
# Pattern: [DESCRIPTION]
grep -rn "[PATTERN]" [LOCATION] --include="*.md" [OPTIONS]

# Options to consider:
# -i = case insensitive
# -w = whole word match
# -E = extended regex
# -A 2 = show 2 lines after
# -B 2 = show 2 lines before
```

---

## Discovery Execution

### Priority 1: Critical Files (Highest Impact)

**Files that propagate errors to new epics:**

```bash
# TEMPLATES (errors propagate to all new epics)
echo "=== Checking templates/ ==="
for pattern in "PATTERN1" "PATTERN2" "PATTERN3"; do
  echo "Pattern: $pattern"
  grep -rn "$pattern" templates/ --include="*.md"
done

# CLAUDE.md (root file - agents read first)
echo "=== Checking CLAUDE.md ==="
grep -rn "PATTERN" ../../CLAUDE.md

# PROMPTS (affect all phase transitions)
echo "=== Checking prompts/ ==="
grep -rn "PATTERN" prompts/ --include="*.md"

# README and EPIC_WORKFLOW_USAGE (entry points)
echo "=== Checking core docs ==="
grep -rn "PATTERN" README.md EPIC_WORKFLOW_USAGE.md
```

**Why templates first?** Template errors multiply - every new epic created gets the error.

### Priority 2: Systematic Folder Search

**Search each folder sequentially:**

```bash
# Define folder order (vary this in each round!)
folders=("debugging" "missed_requirement" "reference" "stages" "templates" "prompts")

# For Round 1: alphabetical order
# For Round 2: reverse order
# For Round 3: random order

for folder in "${folders[@]}"; do
  echo "=== Checking $folder/ ==="

  # Run ALL pattern variations on this folder
  for pattern in "PATTERN1" "PATTERN2" "PATTERN3"; do
    echo "  Pattern: $pattern"
    grep -rn "$pattern" "$folder/" --include="*.md"
  done

  echo ""
done
```

**Folder Descriptions:**
- `debugging/` - Debugging protocol guides
- `missed_requirement/` - Missed requirement protocol
- `reference/` - Reference cards and supporting materials
- `stages/` - Core workflow guides (S1-S10 with sub-guides)
- `templates/` - File templates for epics/features
- `prompts/` - Phase transition prompts
- `audit/` - Audit guides (if checking for self-references)

### Priority 3: Cross-Cutting Searches

**Search ALL markdown files for each pattern variation:**

```bash
# Pattern 1: Basic exact match
grep -rn " 5a\| 5b\| 5c" --include="*.md"

# Pattern 2: Punctuation
grep -rn "5a:\|5b:\|5c:" --include="*.md"

# Pattern 3: Arrows
grep -rn "5a →\|→ 5a\|5a→" --include="*.md"

# Pattern 4: Action verbs
grep -rn "back to 5[a-e]\|restart 5[a-e]\|proceed to 5[a-e]" --include="*.md" -i

# Pattern 5: Headers
grep -rn "^## 5[a-e]\|^### Stage 5[a-e]" --include="*.md"

# Continue with ALL pattern variations from Step 4
```

**Document Results:**
- Pattern used
- Number of matches
- File paths with matches
- Line numbers

### Priority 4: Spot Checks

**Manual reading to catch issues grep misses:**

```bash
# Random file sampling (different files each round)
echo "=== Random Spot Checks ==="
find . -name "*.md" -type f | shuf -n 10 | while read file; do
  echo "Checking: $file"

  # Read different sections of file
  # Beginning
  sed -n '1,50p' "$file"

  # Middle
  sed -n '100,150p' "$file"

  # End
  tail -n 50 "$file"

  # Look for:
  # - Concepts correct but outdated
  # - Missing sections
  # - Incorrect examples
  # - Broken formatting
  # - Issues grep wouldn't catch
done
```

**What to look for in spot-checks:**
- File size issues (very long files)
- Missing expected sections (no Prerequisites, no Exit Criteria)
- Inconsistent formatting within file
- Broken internal cross-references
- Outdated examples or screenshots

### Priority 5: Dimension-Specific Checks

**If focusing on specific dimensions, read those dimension guides:**

**Example: D1 Cross-Reference Accuracy**
```bash
# Extract all file paths
grep -rh "stages/s[0-9].*\.md" --include="*.md" | \
  grep -o "stages/s[0-9][^)]*\.md" | \
  sort -u > /tmp/all_refs.txt

# Verify each exists
while read path; do
  [ ! -f "$path" ] && echo "BROKEN: $path"
done < /tmp/all_refs.txt
```

**Example: D10 File Size Assessment**
```bash
# Check for oversized files
for file in $(find stages -name "*.md"); do
  lines=$(wc -l < "$file")
  if [ $lines -gt 1000 ]; then
    echo "TOO LARGE: $file ($lines lines)"
  elif [ $lines -gt 600 ]; then
    echo "LARGE: $file ($lines lines)"
  fi
done
```

---

## Documentation Format

### Issue Documentation Template

**For EACH issue found, document in discovery report:**

```markdown
## Issue #N

**Dimension:** [D1-D16]
**File:** path/to/file.md
**Line:** 123
**Severity:** Critical/High/Medium/Low

**Pattern That Found It:**
`grep -rn "pattern" --include="*.md"`

**Context (5 lines):**
```
[Line before]
[Line before]
→ [Issue line - mark with arrow]
[Line after]
[Line after]
```

**Current State:**
`old incorrect content`

**Should Be:**
`new correct content`

**Why This Is Wrong:**
[Explanation of the error]

**Fix Strategy:**
- [ ] Automated sed replacement
- [ ] Manual edit required (context-sensitive)
- [ ] Requires user decision

---
```

### Categorization by Dimension

**Group issues by audit dimension:**

```markdown
# Discovery Report - Round N

**Date:** YYYY-MM-DD
**Round:** N
**Duration:** XX minutes
**Total Issues Found:** N

## Summary by Dimension

| Dimension | Issues Found | Severity Breakdown |
|-----------|--------------|-------------------|
| D1: Cross-Reference | 15 | 10 Critical, 5 High |
| D2: Terminology | 8 | 3 High, 5 Medium |
| D10: File Size | 2 | 2 Medium |
| **TOTAL** | **25** | **13 C, 8 H, 6 M** |

## Issues by Dimension

### D1: Cross-Reference Accuracy (15 issues)

[Issue #1, #2, #3... documented as above]

### D2: Terminology Consistency (8 issues)

[Issue #14, #15... documented as above]

...
```

### Severity Classification

**Use this rubric:**

**Critical:**
- Breaks workflow (agent cannot proceed)
- Wrong file path (link to non-existent file)
- Wrong stage reference in critical path
- Template error (propagates to all epics)

**High:**
- Causes confusion (agent uncertain how to proceed)
- Inconsistent terminology (same concept, different names)
- Missing required section
- Outdated decision criteria

**Medium:**
- Cosmetic but important
- Inconsistent formatting
- Minor terminology drift
- Count inaccuracy (non-critical)

**Low:**
- Nice-to-have
- Minor formatting issues
- Stylistic inconsistency

---

## Exit Criteria

### Stage 1 Complete When ALL These Are True

- [ ] Ran automated pre-checks (`scripts/pre_audit_checks.sh`)
- [ ] Checked all Priority 1 files (templates, CLAUDE.md, prompts, core docs)
- [ ] Searched all folders systematically (at least 6 folders)
- [ ] Ran all pattern variations from Step 4 (minimum 5 patterns)
- [ ] Performed spot-checks on 10+ random files
- [ ] Documented ALL issues found using template above
- [ ] Categorized issues by dimension
- [ ] Assigned severity to each issue
- [ ] Created discovery report
- [ ] Ready to proceed to Stage 2 (Fix Planning)

**If ANY criterion incomplete:** Continue discovery until all complete.

---

## Common Pitfalls

### Pitfall 1: Stopping Too Early

**Symptom:** "Grep returned zero results, I'm done"

**Problem:** Only tried one pattern, missed variations

**Solution:** ALWAYS try at least 5 pattern variations:
1. Exact match
2. Punctuation variations
3. Context variations
4. Case variations
5. Header/file name variations

### Pitfall 2: Trusting Grep Without Verification

**Symptom:** "Grep says 50 matches, all are errors"

**Problem:** Didn't manually review context - some may be intentional

**Solution:** Spot-check at least 10 matches manually before assuming all are errors

### Pitfall 3: Assuming Folders Are Clean

**Symptom:** "I checked stages/, the other folders probably don't have issues"

**Problem:** Assumptions lead to blind spots

**Solution:** Check EVERY folder systematically, regardless of assumptions

### Pitfall 4: Not Documenting "Uncertain" Issues

**Symptom:** "I'm not sure if this is an error, so I'll skip it"

**Problem:** Uncertain issues get lost, never resolved

**Solution:** Document EVERYTHING, mark as "needs context analysis" or "needs user decision"

### Pitfall 5: Looking at Previous Round Notes

**Symptom:** "Let me check what I found last round to guide my search"

**Problem:** Biases current round, prevents fresh eyes

**Solution:** Do NOT look at previous notes until AFTER discovery complete

---

## See Also

**Dimension Guides:**
- Read relevant dimension guides for deep-dive checks
- `dimensions/d1_cross_reference_accuracy.md` - File path validation
- `dimensions/d2_terminology_consistency.md` - Notation patterns
- `dimensions/d10_file_size_assessment.md` - Automated size checks

**Reference Materials:**
- `reference/pattern_library.md` - Pre-built search patterns
- `reference/verification_commands.md` - Command examples

**Templates:**
- `templates/discovery_report_template.md` - Use this for output

**Next Stage:**
- `stage_2_fix_planning.md` - Plan how to fix discovered issues

---

**After completing Stage 1:** Proceed to `stages/stage_2_fix_planning.md`
