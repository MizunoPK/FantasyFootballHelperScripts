# Stage 2: Fix Planning

**Purpose:** Organize discovered issues into executable fix groups with clear priorities
**Duration:** 15-30 minutes
**Input:** Discovery report from Stage 1
**Output:** Fix plan with grouped patterns and sed commands
**Reading Time:** 10-15 minutes

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Fix Planning Strategy](#fix-planning-strategy)
4. [Grouping Issues](#grouping-issues)
5. [Creating Fix Commands](#creating-fix-commands)
6. [Exit Criteria](#exit-criteria)

---

## Overview

### Purpose

**Stage 2: Fix Planning** transforms the discovery report into an actionable fix plan. The goals are:
- Group similar issues together for batch fixing
- Prioritize by severity (Critical → High → Medium → Low)
- Create sed commands for automated fixes
- Identify issues requiring manual review
- Minimize number of file edits

### Why Planning Matters

**Without planning:**
- Fix issues randomly → inefficient
- Touch same file multiple times → error-prone
- Miss pattern variations → incomplete fixes
- No prioritization → critical issues delayed

**With planning:**
- Fix by pattern group → efficient
- Touch each file once → clean commits
- Catch all variations → complete fixes
- Critical first → faster impact

---

## Prerequisites

### Before Starting Fix Planning

**Verify you have:**

- [ ] Completed Stage 1 (Discovery)
- [ ] Discovery report with ALL issues documented
- [ ] Issues categorized by dimension
- [ ] Severity assigned to each issue
- [ ] File paths and line numbers for each issue
- [ ] Pattern that found each issue documented

**If missing any:** Return to Stage 1 and complete discovery fully.

---

## Fix Planning Strategy

### The Grouping Process

```text
Step 1: Review All Issues
  ↓
Step 2: Group by Pattern Similarity (not by file)
  ↓
Step 3: Prioritize Groups by Severity
  ↓
Step 4: Create Sed Commands for Each Group
  ↓
Step 5: Identify Manual Review Cases
  ↓
Step 6: Document Fix Order
```

---

## Grouping Issues

### Group by Pattern, Not by File

**❌ WRONG: Group by File**
```markdown
Group 1: Fix s5_p1_planning_round1.md
  - Issue #5: "5a" → "S5.P1"
  - Issue #12: "stages/s5/round1/" → "stages/s5/s5_p1_"

Group 2: Fix s5_p2_planning_round2.md
  - Issue #6: "5a" → "S5.P1"
  - Issue #13: "stages/s5/round2/" → "stages/s5/s5_p2_"
```
**Problem:** Same pattern fixed multiple times, inefficient

**✅ CORRECT: Group by Pattern**
```markdown
Group 1: Old Notation "5a/5b/5c" → "S5.P1/P2/P3"
  - Issue #5: s5_p1_planning_round1.md:45
  - Issue #6: s5_p2_planning_round2.md:78
  - Issue #18: s5_bugfix_workflow.md:123
  [20 instances across 8 files]

Group 2: Old Paths "stages/s5/round1/" → "stages/s5/s5_p1_"
  - Issue #12: s5_p1_planning_round1.md:155
  - Issue #19: s5_p1_i1_requirements.md:67
  [15 instances across 6 files]
```
**Benefit:** Fix all instances of pattern at once with single sed command

### Grouping Criteria

**Group issues together if:**
1. Same OLD pattern (exact match)
2. Same NEW replacement (deterministic)
3. Same context (all errors, or all intentional exceptions)

**Separate into different groups if:**
1. Different OLD patterns
2. Different NEW replacements
3. Mixed context (some errors, some intentional)
4. Requires manual review

### Example Grouping

**From Discovery Report:**
```text
Total Issues: 45
- D1 (Cross-Reference): 20 issues
- D2 (Terminology): 18 issues
- D10 (File Size): 2 issues
- D13 (Documentation Quality): 5 issues
```

**Grouped by Pattern:**
```markdown
## Fix Groups

### Group 1: Old Stage Notation (D2)
**Pattern:** \bS[5-9]a\b → S[5-9].P1 (and b/c/d/e variations)
**Count:** 18 instances
**Files:** 12 files
**Severity:** High
**Automated:** Yes

### Group 2: Broken File References (D1)
**Pattern:** stages/s5/round1/file.md → stages/s5/s5_p1_file.md
**Count:** 12 instances
**Files:** 8 files
**Severity:** Critical
**Automated:** Yes

### Group 3: Missing Prerequisites Sections (D13)
**Pattern:** N/A (requires manual addition)
**Count:** 5 instances
**Files:** 5 files
**Severity:** Medium
**Automated:** No

### Group 4: Oversized Files (D10)
**Pattern:** N/A (requires file split)
**Count:** 2 instances
**Files:** 2 files
**Severity:** Medium
**Automated:** No
```

---

## Prioritizing Groups

### Priority Levels

**P0 - Critical (Fix Immediately):**
- Breaks workflow
- Wrong file paths
- Template errors
- CLAUDE.md sync issues

**P1 - High (Fix in Same Session):**
- Causes confusion
- Inconsistent terminology
- Missing required sections
- Wrong stage references

**P2 - Medium (Fix Soon):**
- Cosmetic but important
- Minor inconsistencies
- Non-critical counts

**P3 - Low (Fix When Time Allows):**
- Nice-to-have
- Minor formatting

### Fix Order

**Execute groups in this order:**

```text
1. P0 groups (all)
   ↓
2. P1 groups (all)
   ↓
3. P2 groups (all)
   ↓
4. P3 groups (if time)
```

**Within same priority:**
```text
1. Automated fixes first (faster)
   ↓
2. Manual fixes second (require thought)
```

---

## Creating Fix Commands

### Sed Command Template

**For automated fixes:**

```bash
# Group X: [Description]
# Pattern: [OLD] → [NEW]
# Count: N instances across M files
# Severity: [Critical/High/Medium/Low]

# Approach 1: Single file
sed -i 's|OLD_PATTERN|NEW_PATTERN|g' path/to/file.md

# Approach 2: Multiple files (same pattern)
sed -i 's|OLD_PATTERN|NEW_PATTERN|g' file1.md file2.md file3.md

# Approach 3: All files in folder
sed -i 's|OLD_PATTERN|NEW_PATTERN|g' stages/s5/*.md

# Approach 4: All markdown files
find . -name "*.md" -exec sed -i 's|OLD_PATTERN|NEW_PATTERN|g' {} +
```

### Pattern Escaping

**Special characters that need escaping:**

```bash
# In sed patterns, escape these: . * [ ] ^ $ / \

# Example: Replacing file paths
# Path: stages/s5/round1_todo.md
# Escaped: stages\/s5\/round1_todo\.md

sed -i 's|stages/s5/round1_todo\.md|stages/s5/s5_p1_planning.md|g' file.md

# Using | as delimiter (recommended for paths)
sed -i 's|stages/s5/round1_todo.md|stages/s5/s5_p1_planning.md|g' file.md
```

### Word Boundary Regex

**Prevent partial matches:**

```bash
# Wrong: Will match "5ab", "15a", etc.
sed -i 's/5a/S5.P1/g' file.md

# Correct: Only matches standalone "5a"
sed -i 's/\b5a\b/S5.P1/g' file.md
```

### Example Fix Plan

```markdown
# Fix Plan - Round N

## Execution Order

### Group 1: Critical File References (P0)
```
# Fix broken stages/s5/round1/ references
sed -i 's|stages/s5/round1/iterations_1_3\.md|stages/s5/s5_p1_i1_requirements.md|g; \
        s|stages/s5/round1/iteration_4\.md|stages/s5/s5_p1_i2_algorithms.md|g; \
        s|stages/s5/round1/iteration_7\.md|stages/s5/s5_p1_i3_integration.md|g' \
    stages/s5/s5_p1_*.md
```text

**Verification:**
```
# Should return 0
grep -rn "stages/s5/round1/" stages/s5/ --include="*.md" | wc -l
```markdown

### Group 2: Old Notation (P1)
```
# Fix S5a/5b/5c notation
sed -i 's/\bS5a\b/S5.P1/g; s/\bS5b\b/S5.P2/g; s/\bS5c\b/S5.P3/g' \
    stages/s5/*.md stages/s2/*.md stages/s10/*.md
```text

**Verification:**
```
# Should return 0 (or only intentional cases)
grep -rn "\bS5[a-e]\b" stages --include="*.md" | wc -l
```markdown

### Group 3: Missing Prerequisites (P2 - MANUAL)
**Files needing Prerequisites section:**
1. stages/s5/s5_bugfix_workflow.md (line 45 - add after Overview)
2. stages/s7/s7_p2_qc_rounds.md (line 67 - add after Overview)
3. stages/s9/s9_p3_user_testing.md (line 89 - add after Overview)

**Action:** Manually add using Edit tool, following template structure
```
```markdown

---

## Investigation and User Questions

**🚨 CRITICAL: DO NOT DEFER ISSUES - Investigate or Ask User**

**When you encounter complexity, you have TWO options:**

**OPTION 1: INVESTIGATE (Preferred)**
1. Read affected files thoroughly
2. Analyze context and determine correct fix
3. Apply fix with confidence
4. Document decision rationale

**OPTION 2: ASK USER (When Uncertain)**
1. Perform initial investigation first
2. Document what you found
3. Present options to user with analysis
4. Include your recommendation
5. Wait for user decision
6. Apply chosen fix immediately

**Decision Framework:**
```text
Issue requires investigation
  ↓
Read files, analyze context (15-30 min)
  ├─ NOW confident in correct fix?
  │   └─ YES → Apply fix immediately
  └─ Still uncertain?
      └─ ASK USER with analysis + options
```

**Examples of Investigation (DO THIS):**

**Context-Sensitive:**
- Pattern appears in both error and intentional contexts
- **ACTION:** Read surrounding lines, determine which instances are errors
- **EXAMPLE:** "5a" in historical example (keep) vs current workflow (fix)

**Complex Replacement:**
- No simple OLD→NEW mapping
- **ACTION:** Read file, understand purpose, determine correct structure
- **EXAMPLE:** Restructuring oversized file requires understanding content

**Adds New Content:**
- Missing sections need to be written
- **ACTION:** Read file, determine if section needed, write appropriate content
- **EXAMPLE:** Adding Prerequisites section - read file to understand dependencies

**User Question Template (When Investigation Insufficient):**

```markdown
## Issue #X - User Decision Needed

**Issue:** [Description]
**Files Affected:** [List]
**Investigation Summary:** [What I found after reading files]

**Context:**
[Explanation of issue after investigation]

**Options Identified:**

**Option 1:** [Description]
- Pros: [benefits]
- Cons: [drawbacks]
- Effort: [time estimate]

**Option 2:** [Description]
- Pros: [benefits]
- Cons: [drawbacks]
- Effort: [time estimate]

**My Recommendation:** [Which option and why]

**Question for User:**
[Specific question about how to proceed]
```

**❌ NEVER DO THIS:**
```text
"Issue X requires file reading → Defer to Round 3"
"Issue Y requires 12 hours → Defer to post-audit"
"Issue Z is complex → Mark for later"
```

**✅ ALWAYS DO THIS:**
```text
"Issue X requires file reading → [Reads files now] → Fixes immediately OR asks user"
"Issue Y requires 12 hours → Investigates scope → Asks user about priority/approach"
"Issue Z is complex → Investigates thoroughly → Presents options to user"
```

---

## File Size Reduction Planning

### Overview

**After planning content accuracy fixes**, you must plan file size reductions for any large files flagged in discovery.

**File size issues are first-class issues** - they get their own fix group with planning, execution, and verification.

### When to Plan File Size Reduction

**If discovery report flagged ANY of these:**
- CLAUDE.md exceeds 40,000 characters
- Any workflow guide >1250 lines

**Then you MUST include file size reduction in fix plan.**

### File Size Fix Group Template

**For EACH large file, create a dedicated fix group:**

```
## Group X: File Size Reduction - [file_name]

**File:** [file_path]
**Current Size:** [X lines / X chars]
**Threshold:** [40,000 chars for CLAUDE.md / 1250 lines for guides]
**Overage:** [amount over threshold]
**Severity:** P1 (if CLAUDE.md or >1250 lines)

**Strategy:** [One of: Extract to sub-guides / Extract to reference files / Consolidate redundant / Move examples to appendices]

**Evaluation Questions:**
- Purpose: [What is this file for?]
- Natural subdivisions: [Yes/No - if yes, what are they?]
- Usage pattern: [How do agents use this file?]
- Reduction potential: [Can split without harming usability?]

**Planned Reduction Approach:**
1. [Step 1: e.g., "Extract Round 2 content to s5_p2_planning_round2.md"]
2. [Step 2: e.g., "Extract Round 3 content to s5_p3_planning_round3.md"]
3. [Step 3: e.g., "Convert original to router file with TOC"]
4. [Step 4: e.g., "Update all cross-references"]

**Target Size After Reduction:** [X lines / X chars]

**Files to Create:**
- [list new files that will be created]

**Cross-References to Update:**
- CLAUDE.md (if file paths changed)
- README.md (if file paths changed)
- Templates (if file paths changed)
- [other files with references]

**Estimated Duration:** [X minutes]

**Verification:**
- [ ] File size ≤ threshold
- [ ] No information lost
- [ ] Cross-references valid
- [ ] Agent usability maintained
- [ ] Pre-audit script passes
```markdown

### Planning Process

**For each large file:**

1. **Read File Size Reduction Guide:**
   - Location: `reference/file_size_reduction_guide.md`
   - Read relevant protocol (CLAUDE.md or Workflow Guide)

2. **Evaluate File:**
   - Answer evaluation questions (purpose, subdivisions, usage, potential)
   - Determine if reduction beneficial or necessary

3. **Choose Strategy:**
   - Extract to sub-guides (preferred for >600 line guides)
   - Extract to reference files (preferred for CLAUDE.md)
   - Consolidate redundant content
   - Move examples to appendices

4. **Document Plan:**
   - Use template above
   - Be specific about extraction targets
   - List all files to create
   - List all cross-references to update

5. **Estimate Duration:**
   - Simple extraction: 15-20 min
   - CLAUDE.md reduction: 30-45 min
   - Complex restructuring: 45-60 min

### Priority Assignment

**File size reduction groups get priority:**
- **P1:** CLAUDE.md >40,000 chars (policy violation - CRITICAL)
- **P1:** Files >1250 lines (too large - CRITICAL)

**Updated Policy (Meta-Audit 2026-02-05):** Simplified from 3-tier to single 1250-line baseline.

**Fix order in Stage 3:**
1. Content accuracy P0-P1 groups (critical content fixes first)
2. File size P1 groups (CLAUDE.md, files >1250 lines)
3. Content accuracy P2-P3 groups

**Rationale:** Fix critical content issues first (so we're not reducing files that still need content updates), then address file size, then lower priority items.

### Example: CLAUDE.md Reduction Plan

```
## Group 5: File Size Reduction - CLAUDE.md

**File:** `../../CLAUDE.md`
**Current Size:** 45,786 characters (1,011 lines)
**Threshold:** 40,000 characters
**Overage:** 5,786 characters (14.5%)
**Severity:** P1 (policy violation)

**Strategy:** Extract to reference files

**Evaluation:**
- Purpose: Quick reference for agents at task start
- Natural subdivisions: Yes (Stage Workflows, Anti-Patterns, Parallel Work, etc.)
- Usage pattern: Read at start of every task
- Reduction potential: High - detailed content can be extracted

**Planned Reduction Approach:**
1. Extract detailed Stage Workflows section to EPIC_WORKFLOW_USAGE.md (keep 4,000 char summary in CLAUDE.md, extract 8,000 chars)
2. Extract S2 Parallel Work details to parallel_work/README.md (keep 1,000 char summary, extract 1,500 chars)
3. Extract detailed Anti-Pattern examples to reference/common_mistakes.md (keep 3 brief examples, extract detailed content ~3,000 chars)
4. Update CLAUDE.md with short summaries + clear links to extracted content

**Target Size After Reduction:** ~38,000 characters

**Files to Create:**
- None (all target files exist, just moving content)

**Cross-References to Update:**
- None (no file path changes, just content extraction)

**Estimated Duration:** 30-40 minutes

**Verification:**
- [ ] wc -c CLAUDE.md ≤ 40,000
- [ ] All critical content remains in CLAUDE.md
- [ ] Links to extracted content clear
- [ ] No information lost
- [ ] Pre-audit script passes

### Critical Rules

**🚨 NO DEFERRAL POLICY:**
**❌ DO NOT defer ANY issues** - Investigate and fix ALL issues immediately
**❌ DO NOT defer to "Round 3" or "post-audit"** - Complete work in current round
**❌ DO NOT say "requires file reading"** - READ the files and fix
**❌ DO NOT say "requires X hours"** - DO the work or ask user about approach

**FILE SIZE REDUCTION:**
**❌ DO NOT skip file size planning** - It's mandatory
**❌ DO NOT defer file size issues** - Address them immediately
**❌ DO NOT treat as "nice to have"** - Treat as first-class fixes
**✅ DO create dedicated fix groups** - Same rigor as content accuracy
**✅ DO consult file size reduction guide** - Use systematic approach
**✅ DO read files to understand structure** - Deep investigation required
**✅ DO ask user if uncertain about split approach** - Present options with analysis

---

## Exit Criteria

### Stage 2 Complete When ALL These Are True

**Content Accuracy Planning:**
- [ ] All content issues from discovery report reviewed
- [ ] Content issues grouped by pattern similarity
- [ ] Groups prioritized (P0 → P1 → P2 → P3)
- [ ] Sed commands created for automated fixes where applicable
- [ ] Word boundaries used where appropriate (\b)
- [ ] Verification commands written for each group
- [ ] Complex issues investigated (files read, context analyzed)
- [ ] User questions prepared for genuinely uncertain cases (with analysis + options)
- [ ] **NO ISSUES DEFERRED** - All issues have fix plan OR user question prepared

**File Size Reduction Planning (if applicable):**
- [ ] All large files from discovery report identified
- [ ] File size reduction guide consulted
- [ ] Evaluation completed for each large file
- [ ] Reduction strategy chosen for each large file
- [ ] Dedicated fix group created for each large file
- [ ] Target files documented (files to create)
- [ ] Cross-reference updates documented
- [ ] Priority assigned (P1/P2/P3)

**Fix Plan Document:**
- [ ] Fix plan document created with:
  - [ ] Group number and description (content + file size groups)
  - [ ] Old pattern → New pattern (or reduction approach for file size)
  - [ ] Count and file list
  - [ ] Sed command (content) or reduction steps (file size) or investigation results
  - [ ] Verification command
  - [ ] Estimated duration
  - [ ] User questions prepared (if needed) with analysis + recommendations
- [ ] **ZERO DEFERRALS** - Every issue has actionable fix plan
- [ ] Ready to proceed to Stage 3 (Apply Fixes) OR user decision (if questions prepared)

**If ANY criterion incomplete:** Continue planning until all complete.

---

## See Also

**Next Stage:**
- `stage_3_apply_fixes.md` - Execute the fix plan incrementally

**Reference:**
- `../reference/verification_commands.md` - More verification examples
- `../templates/fix_plan_template.md` - Use this template for fix plan output

**Dimensions:**
- Relevant dimension guides for context on each issue type

---

**After completing Stage 2:** Proceed to `stages/stage_3_apply_fixes.md`
