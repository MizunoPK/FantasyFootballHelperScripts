# Stage 1: Discovery

**Purpose:** Find issues using systematic search patterns with fresh eyes
**Duration:** 30-60 minutes per sub-round
**Input:** Pre-audit check results (from `scripts/pre_audit_checks.sh`) OR lessons learned from previous sub-rounds
**Output:** Discovery report with categorized issues
**Reading Time:** 15-20 minutes

---

## Table of Contents

1. [Overview](#overview)
2. [Sub-Round Focus](#sub-round-focus)
3. [Prerequisites](#prerequisites)
4. [Discovery Philosophy](#discovery-philosophy)
5. [Discovery Strategy](#discovery-strategy)
6. [Discovery Execution](#discovery-execution)
7. [Documentation Format](#documentation-format)
8. [Exit Criteria](#exit-criteria)
9. [Common Pitfalls](#common-pitfalls)

---

## Overview

### Purpose

**Stage 1: Discovery** is where you find issues that need fixing. The goal is to:
- Search systematically using multiple pattern types
- Focus on specific dimensions based on current sub-round
- Document every issue found with evidence
- Categorize issues by audit dimension
- Prepare for Stage 2 (Fix Planning)

---

## Sub-Round Focus

### Dimension Focus by Sub-Round

**🚨 CRITICAL:** Only check dimensions assigned to your current sub-round. Do NOT check all 22 dimensions in one discovery phase.

#### Sub-Round N.1: Core Dimensions
**Focus on:** D1, D2, D3, D4 (4 dimensions)
**Duration:** 60-90 minutes (full cycle)
**Why First:** Broken references and inconsistent notation affect all other checks

**Dimensions:**
- **D1: Cross-Reference Accuracy** - File paths, links, stage references
- **D2: Terminology Consistency** - Notation (S#.P#.I#), naming conventions
- **D3: Workflow Integration** - Prerequisites, stage transitions, workflow continuity
- **D4: CLAUDE.md Sync** - Root file content matches guide content

**Priority Order:**
1. D1 first (broken references block other work)
2. D2 second (notation consistency needed for D3)
3. D3 third (workflow integration depends on correct references)
4. D4 last (root file sync validates D1-D3)

#### Sub-Round N.2: Content Quality Dimensions
**Focus on:** D5, D6, D7, D8, D9 (5 dimensions)
**Duration:** 75-120 minutes (full cycle)
**Why Second:** Content fixes may reveal structural issues

**Dimensions:**
- **D5: Count Accuracy** - File counts, iteration counts, stage counts
- **D6: Content Completeness** - Missing sections, gaps, orphaned references
- **D7: Template Currency** - Templates reflect current workflow and terminology
- **D8: Documentation Quality** - Required sections present, no TODOs/placeholders
- **D9: Content Accuracy** - Claims match reality (step counts, durations, etc.); for `export_workflow.md` and `import_workflow.md`, cross-reference each prose description of script behavior against the actual script to verify accuracy

**Priority Order:**
1. D6 first (find missing sections)
2. D8 second (validate required sections present)
3. D5 third (verify counts accurate)
4. D9 fourth (validate claims vs reality)
5. D7 last (templates match current state)

#### Sub-Round N.3: Structural Dimensions
**Focus on:** D10, D11, D12, D13, D14 (5 dimensions)
**Duration:** 60-90 minutes (full cycle)
**Why Third:** Structure depends on correct content and references

**Dimensions:**
- **D10: Intra-File Consistency** - Within-file quality (formatting, headers, etc.)
- **D11: File Size Assessment** - Files within readable limits (CLAUDE.md <40K, guides <1250 lines)
- **D12: Structural Patterns** - Guides follow expected template structures
- **D13: Cross-File Dependencies** - Stage prerequisites match outputs, workflow continuity
- **D14: Character and Format Compliance** - No Unicode checkboxes, curly quotes, or other banned non-ASCII chars

**Priority Order:**
1. D11 first (file size issues may require splitting)
2. D14 second (character compliance — 100% automated, run pre-audit script)
3. D12 third (structural patterns)
4. D10 fourth (intra-file consistency)
5. D13 last (cross-file dependencies require D10-D12 clean)

#### Sub-Round N.4: Advanced Dimensions
**Focus on:** D15, D16, D17, D18, D19, D20, D21 (7 dimensions)
**Duration:** 60-90 minutes (full cycle)
**Why Last:** Advanced checks require all other dimensions to be clean

**Dimensions:**
- **D15: Context-Sensitive Validation** - Distinguish errors from intentional exceptions
- **D16: Duplication Detection** - No duplicate content or contradictory instructions
- **D17: Accessibility** - Navigation aids, TOCs, scannable structure; for guides with platform-specific commands (bash/PowerShell), verify each platform has a corresponding equivalent
- **D18: Stage Flow Consistency** - Stage transitions, handoffs, next-guide references
- **D19: Rules File Template Alignment** - Child rules file retains Shamt structural sections (**child context only** — skip in master context)
- **D20: Script Integrity** - Sync scripts are functionally correct, parity between bash/PowerShell, output matches guide instructions (**all contexts** — see D20 checklist in Priority 5 below)
- **D21: Agent Comprehension Risk** - Each stage guide prominently states its scope; no migration notes in the agent instruction path; structurally similar sibling guides have explicit scope differentiation callouts (see `dimensions/d21_agent_comprehension_risk.md`)

**Priority Order:**
1. D17 first (accessibility - missing TOCs and platform parity)
2. D16 second (duplication detection)
3. D18 third (stage flow and handoff accuracy)
4. D21 fourth (agent comprehension risk — per-guide scope clarity; run after D18)
5. D15 fifth (context-sensitive validation requires understanding all content)
6. D19 sixth (child context only; skip entirely if master context)
7. D20 last (script integrity — manual review of sync scripts)

### How to Use This Section

**Before starting discovery:**
1. Identify your current sub-round (N.1, N.2, N.3, or N.4)
2. Read the dimension focus for that sub-round
3. Read the dimension guides for those specific dimensions ONLY
4. Use search patterns relevant to those dimensions
5. Document issues under those dimension categories ONLY

**Example:**
```text
Current: Sub-Round N.1 (Core Dimensions)
Focus: D1, D2, D3, D4
Read: d1_cross_reference_accuracy.md, d2_terminology_consistency.md, d3_workflow_integration.md, d4_claude_md_sync.md
Search: File paths, old notation, prerequisite chains, CLAUDE.md vs guides
Output: Discovery report with D1, D2, D3, D4 issues ONLY
```diff

**Do NOT:**
- ❌ Check all 22 dimensions in Sub-Round N.1
- ❌ Check D11 (file size) during Sub-Round N.1 (save for N.3)
- ❌ Mix dimensions from different sub-rounds
- ❌ Skip dimensions assigned to current sub-round

### Mindset

**CRITICAL:** Approach this with "fresh eyes" - assume you know NOTHING about the codebase.

```text
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

- [ ] **Clean up previous output files** (if starting NEW audit, not new round)
- [ ] Fresh terminal session (cleared history, no bias from previous work)
- [ ] Current working directory: `.shamt/guides/`
- [ ] All previous round assumptions cleared (took 5-minute break if continuing)
- [ ] New notepad/file ready for THIS round's findings
- [ ] Do NOT look at previous round notes until AFTER discovery complete
- [ ] Round counter incremented (Round 1, Round 2, etc.)
- [ ] Identified what changed since last guide update (if triggered by specific change)

### 🚨 Clean Up Previous Output Files (New Audit Only)

**If starting a BRAND NEW audit** (not continuing existing audit):

```bash
# Remove all previous audit output files
rm -rf audit/outputs/*

# Verify cleanup
ls -la audit/outputs/
# Should show empty directory or only .gitkeep
```diff

**When to clean up:**
- ✅ Starting NEW audit after guide changes
- ✅ Starting NEW dimension audit
- ✅ User requested fresh audit start

**When NOT to clean up:**
- ❌ Continuing existing audit (Round N+1 of same audit)
- ❌ Mid-audit (between stages of same round)
- ❌ Resuming after interruption

**Why clean up:**
- Output files are temporary working documents
- Old output files from previous audits cause confusion
- Fresh start ensures no stale references

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

```text
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
```text
Changes:
- Stage 5a → S5.P1
- Stage 5b → S5.P2
- Stage 6 → S9
- Stage 7 → S10
- File: stage_5a_planning.md → s5_v2_validation_loop.md
```diff

**If general maintenance audit:**

Focus on common issue types:
- Cross-references (D1)
- Terminology (D2)
- File sizes (D11)
- Missing sections (D8)
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
```markdown

### STEP 3: Brainstorm Pattern Variations

**For each old pattern, think about ALL ways it might appear:**

**Punctuation Variations:**
```text
Base: "5a"
- "5a:", "5a-", "5a.", "5a)", "(5a", "5a,"
- " 5a ", "5a\n", "\n5a"
```

**Context Variations:**
```text
- Action verbs: "back to 5a", "restart 5a", "proceed to 5a", "complete 5a"
- Descriptive: "in 5a", "during 5a", "from 5a", "after 5a"
- Comparisons: "5a vs 5b", "5a or 5b", "5a and 5b"
```diff

**Header Variations:**
```markdown
- "## 5a:", "### Stage 5a", "#### 5a -"
- "# Part 5a", "## Section 5a"
```

**File Name Variations:**
```text
- "5a_planning.md"
- "stage_5a_"
- "part_5a"
- "round_5a"
```diff

**Case Variations:**
```text
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
```bash

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

### Audit Context: Master vs Child

**Before starting discovery, identify your audit context:**

Check whether `.shamt/shamt_master_path.conf` exists in the project root:
- **File absent** → you are auditing the **master Shamt repo** (master context)
- **File present** → you are auditing a **child project** (child context)

Context determines which files are in scope for full dimension coverage (see Priority 1 below).

---

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
```bash

**Why templates first?** Template errors multiply - every new epic created gets the error.

**Also check guides/sync/ (all contexts):**
The sync guides (`README.md`, `separation_rule.md`, `export_workflow.md`, `import_workflow.md`) are `.md` guide files subject to the same audit dimensions as all other guides. Include `guides/sync/` in every audit run.

```bash
echo "=== Checking guides/sync/ ==="
grep -rn "PATTERN" sync/ --include="*.md"
```

**Also check RULES_FILE.template.md (all contexts):**
`scripts/initialization/RULES_FILE.template.md` is copied to every new child project at init time as the agent's rules file. Quality issues in this file propagate to all new projects. Include it in every audit run.

```bash
echo "=== Checking RULES_FILE.template.md ==="
grep -rn "PATTERN" ../../scripts/initialization/RULES_FILE.template.md
```

**Also check sync scripts for D20 (all contexts):**
The four sync scripts (`export.sh`, `export.ps1`, `import.sh`, `import.ps1`) are in scope for D20 (Script Integrity) in Sub-Round N.4. They are not markdown files; the check is a manual code review using the D20 checklist below.

**Master context — additional files (full dimension coverage):**
When auditing the master repo (`.shamt/shamt_master_path.conf` absent), these master-only files are also in scope for all applicable audit dimensions:
- `CLAUDE.md` (root) — already in Priority 1 above
- Root `README.md` — also already in Priority 1 above
- `scripts/initialization/RULES_FILE.template.md` — already added above

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
```bash

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
```bash

**Example: D11 File Size Assessment**
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

**D20: Script Integrity Checklist (Sub-Round N.4)**

Read each of the four sync scripts manually and verify:

```text
scripts/export/export.sh
scripts/export/export.ps1
scripts/import/import.sh
scripts/import/import.ps1
```

Checklist for each script pair (bash + PowerShell):

- [ ] All function calls in `.ps1` files resolve to functions defined in the script or PowerShell built-ins — no undefined function calls
- [ ] Bash and PowerShell scripts are functionally equivalent — same logic, same behavior, same edge case handling
- [ ] Script next-steps output (what the script prints to the user) matches the corresponding guide's step-by-step instructions
- [ ] Transient output files written by the script (e.g. `import_diff*.md`) and all `.conf` files (via `.shamt/*.conf`) are listed in `.gitignore`
- [ ] State writes (e.g. `write_last_sync`) happen before output generation and agent prompt — not at the very end where an interruption would skip them

---

## Documentation Format

### Issue Documentation Template

**For EACH issue found, document in discovery report:**

```markdown
## Issue #N

**Dimension:** [D1-D21]
**File:** path/to/file.md
**Line:** 123
**Severity:** Critical/High/Medium/Low

**Pattern That Found It:**
`grep -rn "pattern" --include="*.md"`

**Context (5 lines):**
```markdown
[Line before]
[Line before]
→ [Issue line - mark with arrow]
[Line after]
[Line after]
```text

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
| D11: File Size | 2 | 2 Medium |
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

### Stage 1 Complete When ALL These Are True (Sub-Round Specific)

**Sub-Round Focus:**
- [ ] Identified current sub-round (N.1, N.2, N.3, or N.4)
- [ ] Read dimension guides for current sub-round ONLY
- [ ] Focused search on assigned dimensions ONLY

**Discovery Execution:**
- [ ] Ran automated pre-checks (`scripts/pre_audit_checks.sh`) if Sub-Round 1.1
- [ ] Checked all Priority 1 files (templates, CLAUDE.md, prompts, core docs)
- [ ] Searched all folders systematically (at least 6 folders)
- [ ] Ran all pattern variations from Step 4 (minimum 5 patterns per dimension)
- [ ] Performed spot-checks on 10+ random files

**Documentation:**
- [ ] Documented ALL issues found using template above
- [ ] Categorized issues by dimension (ONLY dimensions in current sub-round)
- [ ] Assigned severity to each issue
- [ ] Created discovery report for current sub-round
- [ ] Issues ONLY include dimensions assigned to current sub-round

**Verification:**
- [ ] Did NOT check dimensions outside current sub-round
- [ ] Discovery report dimension categories match sub-round focus
- [ ] Ready to proceed to Stage 2 (Fix Planning) for current sub-round

**If ANY criterion incomplete:** Continue discovery until all complete.

**Sub-Round Dimension Checklist:**
- Sub-Round N.1: D1 ✓, D2 ✓, D3 ✓, D4 ✓ (Core)
- Sub-Round N.2: D5 ✓, D6 ✓, D7 ✓, D8 ✓, D9 ✓ (Content)
- Sub-Round N.3: D10 ✓, D11 ✓, D12 ✓, D13 ✓, D14 ✓ (Structural)
- Sub-Round N.4: D15 ✓, D16 ✓, D17 ✓, D18 ✓, D19 ✓, D20 ✓, D21 ✓ (Advanced; D19 child context only; D20 manual script review)

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
- `dimensions/d11_file_size_assessment.md` - Automated size checks

**Reference Materials:**
- `reference/pattern_library.md` - Pre-built search patterns
- `reference/verification_commands.md` - Command examples

**Templates:**
- `templates/discovery_report_template.md` - Use this for output

**Next Stage:**
- `stage_2_fix_planning.md` - Plan how to fix discovered issues

---

**After completing Stage 1:** Proceed to `stages/stage_2_fix_planning.md`
