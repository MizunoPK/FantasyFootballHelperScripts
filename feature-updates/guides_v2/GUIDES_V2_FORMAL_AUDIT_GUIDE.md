# guides_v2 Formal Audit Guide

**Version:** 2.0
**Created:** 2026-01-14
**Updated:** 2026-01-14 (Major revision after critical review)
**Purpose:** Generic, reusable audit methodology for ensuring complete consistency and identifying gaps across all guides_v2 files
**Audience:** Future agents conducting quality audits after guide updates

**⚠️ CRITICAL READING REQUIREMENT:**
- This guide was created based on ACTUAL audit experience (Sessions 2-3, 221+ fixes across 110 files)
- Every recommendation addresses a REAL mistake that occurred during those audits
- The iterative loop is NOT optional - premature completion happened 3 times
- User challenges are EXPECTED - treat "are you sure?" as a red flag

---

## Table of Contents

1. [Overview](#overview)
2. [When to Run This Audit](#when-to-run-this-audit)
3. [Audit Dimensions](#audit-dimensions)
4. [The Iterative Audit Loop](#the-iterative-audit-loop)
5. [How to Handle User Challenges](#how-to-handle-user-challenges)
6. [Context-Sensitive Analysis Guide](#context-sensitive-analysis-guide)
7. [Discovery Phase Checklist](#discovery-phase-checklist)
8. [Pattern Evolution Strategy](#pattern-evolution-strategy)
9. [Verification Commands Library](#verification-commands-library)
10. [Confidence Calibration](#confidence-calibration)
11. [Issue Classification System](#issue-classification-system)
12. [Reporting Template](#reporting-template)
13. [Common Pitfalls](#common-pitfalls)
14. [Real Examples from Audits](#real-examples-from-audits)
15. [Automated Pre-Checks](#automated-pre-checks)
16. [Appendix: Quick Reference](#appendix-quick-reference)

---

## Overview

### What This Audit Covers

This audit ensures **consistency, accuracy, and completeness** across all guides_v2 files:

- ✅ **Cross-Reference Accuracy:** All file paths, stage references, and cross-links are valid
- ✅ **Terminology Consistency:** Notation, naming conventions, and terminology are uniform
- ✅ **Workflow Integration:** Guides correctly reference each other and form cohesive workflows
- ✅ **Content Accuracy:** Instructions are technically correct and up-to-date
- ✅ **Completeness:** No missing sections, gaps in coverage, or orphaned references
- ✅ **Template Currency:** Templates reflect current workflow structure and terminology
- ✅ **Context-Sensitive Validation:** Same pattern validated differently based on file context

### What This Audit Does NOT Cover

- ❌ Content quality evaluation (writing style, clarity, examples)
- ❌ Workflow design decisions (whether stages are correct)
- ❌ Code implementation (actual Python scripts)

### Audit Philosophy

**Fresh Eyes, Zero Assumptions, User Skepticism is Healthy:**
- Approach each round as if you've never seen the codebase
- Question everything, verify everything, assume you missed something
- Use iterative loops until zero new issues found (minimum 3 rounds)
- Provide evidence, not just claims
- When user challenges you, THEY ARE USUALLY RIGHT - re-verify immediately

**Historical Evidence:**
- Session 2-3 audits: 221+ fixes across 110 files
- Premature completion claims: 3 times (each time, 50+ more issues found)
- User challenges: 3 ("are you sure?", "did you actually make fixes?", "assume everything is wrong")
- Rounds required: 3+ to reach zero new issues

---

## When to Run This Audit

**MANDATORY Triggers:**

1. **After Major Restructuring**
   - Stage renumbering, folder reorganization, file splits/merges
   - Example: Splitting S5 into S5-S8, renumbering S6→S9, S7→S10

2. **After Terminology Changes**
   - Notation updates (e.g., "Stage 5a" → "S5.P1")
   - Naming convention changes
   - Reserved term definitions

3. **After Workflow Updates**
   - Adding/removing stages, phases, or iterations
   - Changing gate requirements or checkpoints
   - Modifying file structures

4. **After S10.P1 Guide Updates**
   - After completing lessons learned integration
   - Ensure guide changes don't introduce inconsistencies
   - Validate all cross-references still accurate

5. **User Reports Inconsistency**
   - User finds error or reports confusion
   - Immediate spot-audit of related files
   - Full audit if issue is widespread

**OPTIONAL Triggers:**

- Quarterly maintenance (even without changes)
- After adding new templates
- After significant content updates to core guides
- Before major epic release

---

## Audit Dimensions

Evaluate guides across **seven critical dimensions:**

### 1. Cross-Reference Accuracy

**What to Check:**
- File paths point to existing files
- Stage/phase/iteration references are correct
- External links are valid
- No references to deleted files

**Pattern Types to Find:**
- Direct file paths: `stages/sN/file.md`
- Stage references: `S#`, `S#.P#`, `S#.P#.I#`
- Relative paths: `../folder/file.md`
- Links: `[text](path.md)`

**How Errors Happen:**
- After folder reorganization, paths not updated
- After stage renumbering, old numbers remain
- After file deletion, references orphaned

**Generic Test:** After ANY change, grep for the old pattern to find stragglers

### 2. Terminology Consistency

**What to Check:**
- Notation follows naming_conventions.md (S#.P#.I# hierarchy)
- Reserved terms used correctly (Stage, Phase, Iteration)
- Casual usage doesn't conflict with reserved terms
- Acronyms and abbreviations are consistent

**Pattern Types to Find:**
- Old notation if recently changed
- Casual misuse of reserved terms
- Inconsistent abbreviations

**How Errors Happen:**
- Content-heavy files missed during bulk updates
- Templates not updated with terminology changes
- New files created with old patterns

**Generic Test:** Define "old patterns" based on what changed, grep for ALL variations

### 3. Workflow Integration

**What to Check:**
- Guides reference correct predecessor/successor stages
- Prerequisites are accurate
- Exit criteria match next stage's entry criteria
- Router files correctly link to sub-guides

**Pattern Types to Find:**
- Prerequisites mentioning wrong stages
- "Next: S#" pointing to wrong stage
- Router → sub-guide link mismatches

**How Errors Happen:**
- Stage reordering not reflected in prerequisites
- Router files not updated when sub-guides renamed
- Workflow sequence changes not propagated

**Generic Test:** Trace workflow path S1→S2→...→S10, verify each transition

### 4. Count Accuracy

**What to Check:**
- Guide counts match actual files
- Stage counts are correct
- Iteration counts are accurate
- File structure lists are current

**Pattern Types to Find:**
- Statements like "N files", "N guides", "N stages"
- Documentation saying different count than reality
- Templates showing old file structure

**How Errors Happen:**
- Documentation updated manually, counts not recalculated
- Stage splits/merges change count, docs not updated
- New files added, index not updated

**Generic Test:** Count actual files, compare to documented counts

### 5. Content Completeness

**What to Check:**
- All stages have corresponding guides
- All templates exist and are complete
- No orphaned sections or TODO placeholders
- Cross-stage patterns are documented

**Pattern Types to Find:**
- Missing guides (S# mentioned but no file exists)
- TODO or placeholder comments
- Incomplete templates
- Orphaned references

**How Errors Happen:**
- Stage added but guide not created yet
- Template partially updated
- TODO left from development

**Generic Test:** List all mentioned stages/files, verify each exists

### 6. Template Currency

**What to Check:**
- Templates use current stage names
- Templates reflect current workflow structure
- Template examples use correct notation
- Template file structures match current standards

**Pattern Types to Find:**
- Old stage names in templates
- Old notation in examples
- Outdated file structure sections
- Missing stages in progress tracking

**How Errors Happen:**
- Templates updated less frequently than guides
- New stages added, templates not updated
- Notation changed, template examples not updated

**Generic Test:** Check templates FIRST after any change - they propagate errors to new epics

### 7. Context-Sensitive Validation

**What to Check:**
- Same pattern validated differently based on context
- Intentional exceptions documented
- File-specific rules applied correctly
- Context analysis performed for ambiguous cases

**Pattern Types to Find:**
- Patterns that are errors in some files, correct in others
- Examples: "S10.P1" could mean feature testing (wrong) or guide updates (correct)
- Examples: "5a" in text (wrong) vs "STAGE 5a" as reference card label (intentional)

**How Errors Happen:**
- Bulk find/replace without context review
- Assuming all matches are errors
- Not understanding file-specific purposes

**Generic Test:** For ambiguous patterns, manually review EVERY match in context

---

## The Iterative Audit Loop

### Overview

```
┌─────────────────────────────────────────────────────────────────┐
│         AUDIT LOOP (Repeat until ZERO new issues found)         │
│                    MINIMUM 3 ROUNDS REQUIRED                     │
└─────────────────────────────────────────────────────────────────┘

Round 1: Initial Discovery
  ↓
Stage 1: Discovery → Stage 2: Fix Planning → Stage 3: Apply Fixes
  ↓                                                           ↓
Stage 4: Verification ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
  ↓
Stage 5: User Presentation & Loop Decision
  ↓                     ↓
  ├─> EXIT (ONLY if ALL exit criteria met + user approves)
  └─> LOOP BACK to Round 2 Discovery (new issues found OR user challenges)

Round 2: Fresh Eyes Discovery
  ↓
[Repeat Stages 1-5 with DIFFERENT patterns, DIFFERENT order, FRESH perspective]
  ↓
Continue until EXIT criteria met (typically 3-5 rounds)
```

### MANDATORY Loop Exit Criteria

**ALL must be true (failing ANY ONE means continue looping):**

1. ✅ **Minimum Rounds:** Completed at least 3 rounds with fresh eyes
2. ✅ **Zero New Discoveries:** Round N Discovery finds ZERO new issues (tried 5+ different pattern types)
3. ✅ **Zero Verification Findings:** Round N Verification finds ZERO new issues (spot-checked 10+ random files)
4. ✅ **All Remaining Documented:** All remaining instances documented as intentional with clear reasoning
5. ✅ **User Verification Passed:** User has NOT challenged findings (no "are you sure?" questions)
6. ✅ **Confidence Calibrated:** Confidence score ≥ 80% (see Confidence Calibration section)
7. ✅ **Pattern Diversity:** Used at least 5 different pattern types across all rounds
8. ✅ **Spot-Check Clean:** Random sample of 10+ files shows zero issues

**IF USER CHALLENGES YOU:**
- **IMMEDIATELY** set loop counter back to Round 1
- User challenge = evidence you missed something
- Re-verify EVERYTHING with fresh patterns
- Do NOT defend - user is usually right

### Round Structure

**Each round consists of 5 stages:**

#### Stage 1: Discovery (FRESH EYES)

**Duration:** 30-60 minutes per round

**Mindset:** Assume you know NOTHING about the codebase

**Activities:**
1. **Clear Assumptions:** Physically clear mental model from previous rounds
   - Take 5-minute break if continuing immediately
   - Don't look at previous round notes until AFTER discovery
   - Approach folders in DIFFERENT order than last round

2. **Choose NEW Patterns:** Use completely different search patterns
   - Round 1: Basic patterns (e.g., " 5a\| 5b\| 5c")
   - Round 2: Variations (e.g., "5a →\|→ 5a\|5a→")
   - Round 3: Context patterns (e.g., "back to 5a\|Proceed to 5b\|restart 5a")
   - Round 4+: Spot-checks, random sampling, manual reading

3. **Explore Unexplored Areas:**
   - "What folders did I skip last round?"
   - "What file types did I not check?"
   - "What edge cases did I not consider?"

4. **Document ALL Findings:**
   - File path
   - Line number
   - Issue description
   - Pattern that found it
   - Severity (Critical/High/Medium/Low)

5. **Count Issues:** N_found = total issues found this round

**Output:** Discovery checklist with N_found issues categorized by severity

**RED FLAGS (indicating you need to loop back):**
- Found > 10 issues in Round 3+
- User asks "are you sure?"
- You feel uncertain about completeness
- Spot-checks reveal issues you missed

#### Stage 2: Fix Planning

**Duration:** 15-30 minutes

**Activities:**
1. Group issues by pattern type
2. Prioritize by severity: Critical → High → Medium → Low
3. Plan sed/grep commands for each group
4. Identify edge cases requiring manual review
5. Create fix checklist with verification steps

**Output:** Fix plan with grouped patterns and priority order

#### Stage 3: Apply Fixes (INCREMENTAL VERIFICATION)

**Duration:** 30-90 minutes

**Activities:**
1. **Fix ONE group at a time** (never batch all fixes)
2. **IMMEDIATELY verify EACH fix:**
   ```bash
   # Apply fix
   sed -i 's/OLD/NEW/g' file.md

   # Verify NEW pattern exists
   grep -n "NEW" file.md

   # Verify OLD pattern gone
   grep -n "OLD" file.md  # Should return nothing

   # Spot-read actual lines
   sed -n 'LINEp' file.md  # Replace LINE with actual line number
   ```
3. **Re-run grep to confirm reduction:**
   ```bash
   grep -rn "OLD" --include="*.md" | wc -l  # Count should decrease
   ```
4. **Document before/after:**
   - File: `path/to/file.md`
   - Line: 123
   - Before: `old content here`
   - After: `new content here`
   - Verified: `grep -n "new content" file.md` shows line 123

5. **Repeat for next group**

**CRITICAL:** Never trust sed - always verify by reading actual files

**Output:** Fixed files with before/after documentation for each change

#### Stage 4: Comprehensive Verification

**Duration:** 30-45 minutes

**Activities:**
1. **Re-run ALL patterns from Stage 1:**
   ```bash
   # For each pattern used in Discovery:
   grep -rn "PATTERN" --include="*.md" | wc -l
   # Count should match N_remaining (intentional cases only)
   ```

2. **Try NEW patterns** (variations you just thought of):
   ```bash
   # Brainstorm: "What variations did I not try?"
   # Example: If you tried " 5a", try "5a:", "5a-", "(5a)"
   ```

3. **Spot-check random files** (read actual content, don't just grep):
   ```bash
   find . -name "*.md" -type f | shuf -n 10  # Pick 10 random files
   # Manually open and read portions of each
   ```

4. **Calculate counts:**
   - N_remaining = issues still found (should be only intentional)
   - N_new = issues found in verification NOT in original Stage 1 list
   - N_fixed = N_found - N_remaining

5. **Categorize remaining:**
   - Intentional: Document why it's acceptable
   - Missed: Add to fix list, loop back

**Output:** Verification report with N_remaining, N_new, N_fixed

**CRITICAL:** If N_new > 0, you MUST loop back - you missed something

#### Stage 5: User Presentation & Loop Decision

**Duration:** 15-30 minutes

**Activities:**
1. **Summarize round results:**
   - Round number
   - Patterns used
   - Issues found/fixed/remaining
   - New discoveries

2. **Provide evidence** (MANDATORY):
   - Show before/after file content (not just grep output)
   - List grep commands used
   - Show verification commands and outputs
   - Spot-check results

3. **List intentional cases:**
   - File path + line number
   - Pattern matched
   - Why it's intentional
   - Why it's acceptable

4. **Report new discoveries:**
   - N_new issues found during verification
   - Patterns that found them
   - Why they were missed in Discovery

5. **Invite user challenge:**
   - "Please verify these findings"
   - "Challenge me if anything seems incomplete"
   - "Ask 'are you sure?' if you have doubts"

6. **Make loop decision:**

```
DECISION LOGIC:

IF ALL of the following are true:
  - N_new = 0 (verification found no new issues)
  - N_remaining documented as intentional
  - User has NOT challenged findings
  - Minimum 3 rounds completed
  - Confidence score ≥ 80%
  - Spot-checks clean (10+ files)
  - Pattern diversity ≥ 5 types
THEN:
  └─> ✅ EXIT LOOP - Audit complete
ELSE:
  └─> 🔄 LOOP BACK to Stage 1 Round N+1
      Requirements for next round:
      - Clear all assumptions (fresh eyes)
      - Use DIFFERENT patterns than any previous round
      - Explore folders in DIFFERENT order
      - Question ALL previous findings
      - Incorporate lessons from this round

SPECIAL CASE - User Challenge:
IF user asks "are you sure?" OR "did you make fixes?" OR similar:
  └─> 🚨 IMMEDIATE LOOP BACK to Round 1
      - User challenge = evidence you missed something
      - Do NOT defend or justify - re-verify EVERYTHING
      - Assume you were wrong, prove yourself right
      - Use completely fresh patterns and approach
```

**Output:** Loop decision + preparation for next round (if needed)

---

## How to Handle User Challenges

**CRITICAL PRINCIPLE:** User skepticism is HEALTHY. When challenged, assume user is RIGHT.

### Types of User Challenges

#### Challenge 1: "Are you sure there are no remaining issues?"

**What This Means:**
- User doubts your thoroughness
- Likely you missed pattern variations
- You may have claimed completion prematurely

**Historical Evidence:**
- Session 2-3: After claiming completion, this challenge found 50+ more issues

**How to Respond:**

```
STEP 1: Acknowledge (do NOT defend)
  "You're right to challenge - let me re-verify with fresh patterns"

STEP 2: Immediate Re-Verification
  - Run completely NEW grep patterns (variations you didn't try)
  - Spot-check random files by reading actual content
  - Try patterns suggested by the challenge (infer what user suspects)

STEP 3: Report Findings Honestly
  IF new issues found:
    "You were right - I found N more issues using patterns X, Y, Z"
  IF no new issues:
    "I've re-verified with patterns X, Y, Z and spot-checked 10 files -
     found zero new issues. Here's the evidence: [show grep outputs]"

STEP 4: Loop Back
  - Even if zero found, consider this a new round
  - User challenge = failed confidence test
  - Complete at least one more round before claiming done
```

#### Challenge 2: "I only saw you use grep commands. Did you actually make the fixes?"

**What This Means:**
- User doubts fixes were applied (not just discovered)
- You may have shown grep output without verification
- You need to provide proof, not claims

**Historical Evidence:**
- Session 2-3: Had to prove fixes by reading actual file contents

**How to Respond:**

```
STEP 1: Acknowledge
  "Valid concern - let me show proof the fixes were applied"

STEP 2: Provide Evidence (show actual file contents)
  For 3-5 example fixes:
    File: path/to/file.md
    Line: 123
    Before: [show OLD content via grep or sed]
    After: [show NEW content via grep or sed]
    Proof:
      $ grep -n "NEW content" file.md
      123: NEW content here

      $ grep -n "OLD content" file.md
      [no results - confirms removed]

STEP 3: Spot-Check Verification
  "Let me spot-check 5 random files to confirm all fixes applied:"
  [Read actual file contents via cat/sed, show relevant sections]

STEP 4: Re-Grep Verification
  "Confirming OLD patterns are gone:"
  $ grep -rn "OLD pattern" --include="*.md" | wc -l
  47  [These are all documented intentional cases]
```

#### Challenge 3: "Assume everything in the guide is wrong, misleading, or incomplete"

**What This Means:**
- User wants comprehensive critical review
- Look for gaps, inaccuracies, missing sections
- Verify claims, test commands, question assumptions

**How to Respond:**

```
STEP 1: Fresh Critical Review
  - Read guide assuming it's WRONG
  - Question every claim: "Is this actually true?"
  - Test every command: "Does this actually work?"
  - Check for gaps: "What's missing?"

STEP 2: Verification Checks
  - Untested commands: Flag which commands were NOT tested
  - Incomplete sections: Identify missing information
  - Misleading statements: Find confusing or wrong info
  - Real-world applicability: Does this work for ANY audit or only one specific case?

STEP 3: Document Findings
  Create list:
    VERIFIED: [commands/claims that were tested and work]
    UNTESTED: [commands/claims with no evidence]
    INCORRECT: [statements that are wrong]
    INCOMPLETE: [missing sections or details]
    MISLEADING: [confusing or unclear statements]

STEP 4: Comprehensive Updates
  - Fix all incorrect statements
  - Add all missing sections
  - Clarify all misleading statements
  - Label untested commands
  - Add real examples to verify claims
```

### General Response Protocol

**When user challenges you:**

1. **NEVER defend or justify** - assume user is right
2. **ALWAYS re-verify** - don't trust previous work
3. **PROVIDE EVIDENCE** - show actual file contents, not just grep
4. **LOOP BACK** - treat challenge as new round
5. **THANK USER** - challenges improve quality

**Red Flags You Missed:**
- You claimed completion without 3+ rounds
- You didn't provide before/after file content
- You didn't spot-check random files
- You used same patterns each round
- Your confidence wasn't calibrated (see Confidence Calibration section)

---

## Context-Sensitive Analysis Guide

**CRITICAL PRINCIPLE:** Not all pattern matches are errors. Context determines correctness.

### When Same Pattern is Both Error and Correct

**Example 1: "S10.P1" Reference**

Context determines if this is wrong:

```
FILE: debugging/discovery.md
LINE 88: "Feature testing occurs in S10.P1 (smoke testing)"
CONTEXT: Describing when debugging happens (feature testing phase)
ANALYSIS: S10.P1 is Epic Guide Updates, NOT feature testing
VERDICT: ❌ WRONG - Should be "S7.P1"

FILE: debugging/root_cause_analysis.md
LINE 156: "S10.P1 Guide Update Workflow"
CONTEXT: Describing where lessons integrate (guide updates phase)
ANALYSIS: S10.P1 IS Guide Update Workflow
VERDICT: ✅ CORRECT - Keep as-is
```

**How to Analyze:**
1. Read surrounding 5-10 lines for context
2. Identify what the reference is describing
3. Verify against workflow: Does S10.P1 mean feature testing or guide updates?
4. Check file purpose: Is this file about feature testing or epic cleanup?

**Example 2: "5a" Notation**

Context determines if this is intentional:

```
FILE: EPIC_WORKFLOW_USAGE.md
LINE 75: "The workflow goes 5a → 5b → 5c → 5d → 5e"
CONTEXT: Describing old workflow in content paragraph
ANALYSIS: Old notation in current documentation
VERDICT: ❌ WRONG - Should be "S5 → S6 → S7 → S8"

FILE: reference/stage_5/stage_5_reference_card.md
LINE 12: "## STAGE 5a: Planning Round 1"
CONTEXT: Reference card section header (document-specific label)
ANALYSIS: Reference card uses "STAGE 5a" as section label for readability
PURPOSE: Quick reference format, not workflow documentation
VERDICT: ✅ INTENTIONAL - Keep as-is (document as intentional case)

FILE: reference/stage_5/stage_5_reference_card.md
LINE 176: "5a: 2 hours | 5b: 1 hour | 5c: 30 min"
CONTEXT: Time estimates table with shorthand
ANALYSIS: Compact table format using shorthand notation
PURPOSE: Quick reference, space-constrained format
VERDICT: ✅ INTENTIONAL - Keep as-is (shorthand acceptable in tables)
```

### Context Analysis Workflow

**For EVERY ambiguous match:**

```
STEP 1: Read Context
  - Read 10 lines before and after
  - Understand what section this is in
  - Identify the purpose of this statement

STEP 2: Determine Intent
  Questions to ask:
    - Is this describing the workflow? (should use current notation)
    - Is this a document-specific label? (may use old notation for continuity)
    - Is this a table/list with space constraints? (shorthand may be acceptable)
    - Is this an example or quote? (may preserve old notation intentionally)

STEP 3: Verify Against Workflow
  - Check actual workflow structure
  - Confirm what the reference SHOULD be
  - Determine if current reference is correct

STEP 4: Make Decision
  IF describing current workflow AND using old notation:
    → ❌ ERROR - Fix it
  IF document-specific label OR space-constrained format OR quote:
    → ⚠️ POSSIBLE INTENTIONAL - Check file purpose
  IF file purpose justifies old notation:
    → ✅ INTENTIONAL - Document it
  ELSE:
    → ❌ ERROR - Fix it

STEP 5: Document Decision
  For intentional cases:
    File: path/to/file.md
    Lines: X, Y, Z
    Pattern: "old notation"
    Reason: Reference card section labels
    Acceptable: Yes
    Verified: [Your name/ID]
```

### File-Specific Exception Rules

Some files have special rules:

**Reference Cards:**
- May use old notation as section headers
- May use shorthand in tables
- Purpose: Quick reference, not definitive documentation
- Acceptable if documented as intentional

**Time Estimate Tables:**
- Shorthand notation acceptable: "5a: 2h, 5b: 1h"
- Space-constrained format justifies brevity
- Acceptable if consistent within table

**Historical Examples:**
- May preserve old notation to show "before/after"
- Quotes from old guides may use old notation
- Context must make clear this is historical
- Must be labeled as "old notation" or "before change"

**ASCII Art Headers:**
- May use old notation for visual formatting
- "STAGE 5b WORKFLOW" as ASCII art banner
- Acceptable if purely decorative

**NOT Acceptable:**
- Current workflow descriptions using old notation
- Prerequisites using old stage numbers
- "Next stage" references using old notation
- File paths to non-existent locations

### When in Doubt

**If you cannot determine intentionality:**

1. **Flag for User Review:**
   ```
   File: path/to/file.md
   Line: 123
   Pattern: "ambiguous notation"
   Context: [paste 10 lines]
   Question: Is this intentional?
   Recommendation: [Fix/Keep] based on X reasoning
   ```

2. **Default to Fix Unless Certain:**
   - If uncertain, treat as error
   - Better to over-fix than under-fix
   - User can confirm intentional cases

3. **Document All Ambiguous Cases:**
   - Create "AMBIGUOUS_CASES.md"
   - List each case with context
   - Present to user for final decision

---

## Discovery Phase Checklist

### Philosophy: Principles Over Prescriptions

**This checklist teaches HOW to create patterns, not just which patterns to run.**

Why? Because:
- Future guide updates will create NEW error patterns
- Prescriptive checklists only catch known issues
- Principle-based approach adapts to any changes

**Core Principle:** Ask "What changed?" → Infer patterns → Search for stragglers

### Pre-Discovery Preparation

**Before starting Discovery, ensure:**

- [ ] Fresh terminal session (clear history/bias)
- [ ] Current working directory: `guides_v2/`
- [ ] All previous round assumptions cleared (take 5-min break)
- [ ] New notepad/file for THIS round's findings (don't look at previous rounds yet)
- [ ] Round counter incremented
- [ ] Identified what changed since last guide update (if any)

### Discovery Strategy: Pattern Generation

**STEP 1: Understand What Changed**

If audit triggered by specific change:
- Stage renumbering? → Search for old stage numbers
- File moved? → Search for old file paths
- Terminology changed? → Search for old terminology

If periodic maintenance (no specific trigger):
- Review git log for recent changes
- Check GUIDE_UPDATE_PROPOSAL.md for known areas of change
- Ask: "What areas are most likely to have drift?"

**STEP 2: Generate Base Patterns**

Based on what changed, create patterns:

```
CHANGE TYPE: Stage renumbering (e.g., S6 → S9, S7 → S10)

BASE PATTERNS:
  - References to old stage numbers: "Stage 6", "S6", "stage_6"
  - File paths with old numbers: "stages/s6/", "stage_6/"
  - Casual mentions: "stage 6", "Stage Six"

VARIATIONS TO CONSIDER:
  - With context: "back to S6", "proceed to S6"
  - In sequences: "S5 → S6 → S7"
  - In file names: "stage_6_prompts.md"
  - In folder names: "reference/stage_6/"
```

**STEP 3: Brainstorm Variations**

For each base pattern, ask:
- Where else might this appear?
- What forms could this take?
- What edge cases exist?

```
EXAMPLE: Old notation "5a" changed to "S5.P1"

BASE: " 5a" (space before to avoid false positives)

VARIATIONS:
  - With punctuation: "5a:", "5a-", "5a)", "(5a)"
  - With arrows: "5a →", "→ 5a", "5a→", "→5a"
  - With actions: "back to 5a", "restart 5a", "Proceed to 5a"
  - With stage: "Stage 5a", "STAGE 5a"
  - In sequences: "5a → 5b → 5c"
  - Headers: "## 5a:", "### Stage 5a"
  - Files: "5a_planning.md", "stage_5a_"
```

**STEP 4: Create Search Commands**

For each variation, create grep command:

```bash
# Base pattern
grep -rn " 5a\| 5b\| 5c" --include="*.md"

# Punctuation variations
grep -rn "5a:\|5b:\|5c:" --include="*.md"

# Arrow variations
grep -rn "5a →\|→ 5a\|5a→\|→5a" --include="*.md"

# Action variations
grep -rn "back to 5[a-e]\|restart 5[a-e]\|Proceed to 5[a-e]" --include="*.md"

# Header variations
grep -rn "^## 5[a-e]\|^### Stage 5[a-e]" --include="*.md"
```

### Discovery Execution: Systematic Search

**Run searches in priority order:**

#### Priority 1: Critical Files

Files that propagate errors to new epics:
```bash
# Templates (highest priority - errors propagate)
grep -rn "PATTERN" templates/*.md

# Core documentation (README, EPIC_WORKFLOW_USAGE)
grep -rn "PATTERN" README.md EPIC_WORKFLOW_USAGE.md prompts_reference_v2.md

# Prompts (affect all phase transitions)
grep -rn "PATTERN" prompts/*.md
```

#### Priority 2: Systematic Folder Search

```bash
# For each folder, search with all patterns
for folder in debugging missed_requirement reference stages templates prompts; do
  echo "=== Checking $folder/ ==="
  grep -rn "PATTERN" $folder/*.md
done
```

#### Priority 3: Cross-Cutting Searches

```bash
# Search ALL .md files for each pattern variation
grep -rn "PATTERN_1" --include="*.md"
grep -rn "PATTERN_2" --include="*.md"
grep -rn "PATTERN_3" --include="*.md"
# ... for each pattern generated in Step 4
```

#### Priority 4: Spot Checks

```bash
# Random file sampling
find . -name "*.md" -type f | shuf -n 10

# For each random file, manually read portions
sed -n '1,50p; 100,150p; 200,250p' "RANDOM_FILE"

# Look for issues grep might miss:
# - Concepts correct but outdated
# - Missing sections
# - Incorrect examples
# - Broken formatting
```

### Discovery Documentation

**For EACH issue found, document:**

```markdown
## Issue #N

**File:** path/to/file.md
**Line:** 123
**Severity:** Critical/High/Medium/Low
**Pattern:** `grep pattern that found it`
**Context:** [Paste 3-5 lines around the issue]

**Current State:**
`old incorrect content`

**Should Be:**
`new correct content`

**Why This is Wrong:**
[Explanation of why current state is incorrect]

**Fix Command:**
`sed -i 's/old/new/g' file.md`
```

### Discovery Output Template

```markdown
## Round N Discovery Results

**Date:** YYYY-MM-DD HH:MM
**Time Spent:** XX minutes
**Round Type:** [Initial/Follow-up/User Challenge Response]

### Patterns Used This Round

1. `grep -rn "PATTERN_1"` → Found X issues
2. `grep -rn "PATTERN_2"` → Found Y issues
3. Spot-checks of Z files → Found W issues

**Total Patterns Tried:** N
**Total Issues Found:** X+Y+W

### Issues by Severity

**Critical (Blocking):** N issues
- [List with file:line references]

**High Priority:** M issues
- [List with file:line references]

**Medium Priority:** K issues
- [List with file:line references]

**Low Priority:** L issues
- [List with file:line references]

### Files Affected

**Total:** X files
**By Folder:**
- templates/: N files
- prompts/: M files
- stages/: K files
- [etc.]

### New Insights for Next Round

**Patterns to Try:**
- [Variations not yet tried]
- [Edge cases not considered]

**Areas to Explore:**
- [Folders not fully checked]
- [File types not reviewed]

**Questions:**
- [Ambiguous cases needing user input]
```

---

## Pattern Evolution Strategy

**CRITICAL PRINCIPLE:** Each round discovers what previous rounds MISSED.

### Round-by-Round Pattern Strategy

**Round 1: Base Patterns**

Focus: Find obvious instances
```bash
# If change was "5a" → "S5.P1", search for:
grep -rn " 5a\| 5b\| 5c\| 5d\| 5e" --include="*.md"

# Result Example: Found 123 instances
```

After Round 1, analyze what you FOUND:
- Where did most issues occur? (templates, specific guides)
- What forms did they take? (in text, in headers, in file paths)

After Round 1, analyze what you MISSED:
- Did you search for punctuation variations? (5a:, 5a-, 5a))
- Did you search for arrow variations? (5a →, → 5a)
- Did you search for action verbs? (back to 5a, restart 5a)

**Round 2: Variations of Found Patterns**

Focus: Find forms Round 1 missed
```bash
# Based on Round 1 findings, search for variations:
grep -rn "5a →\|5a→\|→ 5a\|→5a" --include="*.md"  # Arrows
grep -rn "5a:\|5b:\|5c:" --include="*.md"         # Punctuation

# Result Example: Found 68 more instances
```

After Round 2, analyze:
- What new forms did you find?
- Are there still variations not covered?

**Round 3: Context and Edge Cases**

Focus: Find instances in specific contexts
```bash
# Search for action verbs with old notation
grep -rn "back to 5[a-e]\|restart 5[a-e]\|Proceed to 5[a-e]" --include="*.md"

# Search in specific file types
grep -rn "5a\|5b" templates/*.md  # Templates
grep -rn "5a\|5b" prompts/*.md    # Prompts

# Result Example: Found 15 more instances
```

After Round 3, analyze:
- Are you finding fewer issues each round? (Good - converging)
- Are remaining instances intentional? (Document them)

**Round 4+: Verification and Spot-Checks**

Focus: Manual review for issues grep can't find
```bash
# Random file sampling
find . -name "*.md" -type f | shuf -n 10

# Manual reading of files
# Look for:
# - Conceptual errors (correct notation but wrong stage number)
# - Missing sections
# - Outdated examples
# - Broken workflow references

# Result Example: Found 0-3 issues
```

**Exit when:** Round N finds 0 new issues AND Round N+1 also finds 0

### Pattern Learning: What to Try Next

**After each round, ask:**

1. **What did I find?**
   - List all patterns that had matches
   - Categorize by type (notation, paths, references)

2. **What did I miss?**
   - Variations I didn't search for
   - Contexts I didn't consider
   - Files I didn't check

3. **What should I try next round?**
   - Variations: punctuation, spacing, case
   - Contexts: action verbs, sequences, headers
   - Locations: specific folders, file types

**Example Learning Progression:**

```
ROUND 1: Found " 5a" (123 instances)
LEARNED: Only searched for space-prefixed, missed other forms
NEXT: Try punctuation and arrows

ROUND 2: Found "5a →" (68 instances)
LEARNED: Only searched for arrows, missed action verbs
NEXT: Try "back to", "Proceed to", "restart"

ROUND 3: Found "back to 5a" (15 instances)
LEARNED: Mostly found all pattern variations
NEXT: Manual spot-checks for conceptual errors

ROUND 4: Spot-checked 10 files (0 new issues)
LEARNED: Pattern coverage appears complete
NEXT: One more round to confirm
```

### When to Stop Adding Patterns

**Stop adding new patterns when:**

1. **Diminishing Returns:** Round N finds < 5 issues AND Round N-1 found < 10
2. **Pattern Exhaustion:** You've tried 5+ different pattern types
3. **Clean Spot-Checks:** Random sampling of 10+ files finds 0 issues
4. **User Approval:** User has not challenged findings

**Don't stop if:**
- Only completed 1-2 rounds (minimum 3 required)
- User challenged you ("are you sure?")
- Spot-checks reveal issues
- Confidence score < 80%

---

## Verification Commands Library

**⚠️ IMPORTANT:** This section contains BOTH tested and untested commands. Tested commands are marked ✅. Untested commands are marked ⚠️ and should be validated before relying on them.

### Tested Commands (from actual Session 2-3 audits)

These commands were actually used and confirmed working:

#### ✅ Basic Pattern Search

```bash
# Find old stage notation (Session 2-3: Found 123 instances)
grep -rn " 5a\| 5b\| 5c\| 5d\| 5e" --include="*.md"

# Find specific file path errors (Session 2-3: Found 15 instances)
grep -rn "stages/s9/s6_\|stages/s10/s7_" --include="*.md"

# Find stage count errors (Session 2-3: Found 3 instances)
grep -rn "[0-9]-stage\|[0-9] stage" --include="*.md"

# Count total matches
grep -rn "PATTERN" --include="*.md" | wc -l

# Exclude audit files from results
grep -rn "PATTERN" --include="*.md" --exclude="*AUDIT*.md"
```

#### ✅ File Counting

```bash
# Count .md files in folder (Session 2-3: Used to verify file counts)
find . -name "*.md" -type f | wc -l
find stages/ -name "*.md" -type f | wc -l
find templates/ -name "*.md" -type f | wc -l

# List all folders
ls -d */
```

#### ✅ Context Search

```bash
# Find pattern with surrounding context (Session 2-3: Used for S10.P1 analysis)
grep -rn -B 5 -A 5 "PATTERN" --include="*.md"

# Case-insensitive search
grep -rin "PATTERN" --include="*.md"
```

#### ✅ Verification After Fixes

```bash
# Verify fix applied (Session 2-3: Used to confirm sed commands worked)
# 1. Apply fix
sed -i 's/OLD/NEW/g' file.md

# 2. Verify NEW exists
grep -n "NEW" file.md

# 3. Verify OLD gone
grep -n "OLD" file.md  # Should return nothing

# 4. Count reduction
grep -rn "OLD" --include="*.md" | wc -l  # Should decrease
```

### Untested Commands (use with caution)

These commands are theoretically useful but were NOT tested during Session 2-3:

#### ⚠️ File Path Validation (UNTESTED)

```bash
# Extract all .md references (MAY NOT WORK - regex untested)
grep -ro "[a-z_/]*\.md" --include="*.md" | sort -u > /tmp/refs.txt

# Then manually check each exists (TEDIOUS - may not be practical)
# This approach was NOT used in actual audits

# Alternative (UNTESTED):
# Find all markdown links
grep -rn "\[.*\](.*\.md)" --include="*.md"
```

**⚠️ Warning:** The regex `[a-z_/]*\.md` may not match all path formats (uppercase, numbers, etc.). Test before relying on this.

#### ⚠️ Random Sampling (PLATFORM-DEPENDENT)

```bash
# Random file sampling (REQUIRES 'shuf' - not available on all systems)
find . -name "*.md" -type f | shuf -n 5

# macOS alternative (use 'gshuf' if installed via brew):
find . -name "*.md" -type f | gshuf -n 5

# Portable alternative (UNTESTED):
find . -name "*.md" -type f | sort -R | head -n 5
```

**⚠️ Warning:** `shuf` not available on macOS by default. `sort -R` is less random but portable.

#### ⚠️ Bash-Specific Scripts (SHELL-DEPENDENT)

```bash
# Random file selection and reading (REQUIRES BASH - won't work in sh)
RANDOM_FILE=$(find . -name "*.md" -type f | shuf -n 1)
echo "Checking: $RANDOM_FILE"
sed -n '1,50p; 100,150p; 200,250p' "$RANDOM_FILE"
```

**⚠️ Warning:** This uses bash-specific syntax. Use `/bin/bash` explicitly if needed.

### Recommended Workflow

**ALWAYS:**
1. Use ✅ tested commands first
2. Validate ⚠️ untested commands on small dataset before bulk use
3. Provide alternative if command fails

**Example:**
```bash
# Try shuf first
if command -v shuf &> /dev/null; then
  find . -name "*.md" -type f | shuf -n 5
else
  echo "shuf not available, using sort -R"
  find . -name "*.md" -type f | sort -R | head -n 5
fi
```

### Pattern Library (from actual audits)

**✅ These patterns were ACTUALLY USED and WORKED in Session 2-3:**

```bash
# Old stage notation (found 123 instances)
" 5a\| 5b\| 5c\| 5d\| 5e\| 6a\| 6b\| 6c"

# Arrow variations (found 68 instances)
"5a →\|5a→\|→ 5a\|→5a"

# Action verbs with stages (found 15 instances)
"back to\|Proceed to\|restart"

# Stage headers (found 8 instances)
"Stage 5[a-e]:\|STAGE 5[a-e]:"

# File path errors (found 15 instances)
"stages/s9/s6_\|stages/s10/s7_"

# Stage count errors (found 3 instances)
"[0-9]-stage workflow\|[0-9] stage workflow"

# Old stage references (found 47 intentional instances)
"(1-7)\|(7 stages)\|7-stage"
```

---

## Confidence Calibration

**CRITICAL:** Confidence is NOT a feeling - it's a calculated score based on objective metrics.

### Confidence Formula

```
Confidence Score = (Rounds × 10) + (Pattern Types × 5) + (Spot Checks × 2) - (User Challenges × 20)

WHERE:
  Rounds = Number of complete audit rounds (minimum 3)
  Pattern Types = Number of DIFFERENT pattern types tried (minimum 5)
  Spot Checks = Number of random files manually read (minimum 10)
  User Challenges = Number of times user questioned findings (0 = best)

SCORE INTERPRETATION:
  80-100: HIGH confidence - likely safe to exit
  60-79:  MEDIUM confidence - do another round
  40-59:  LOW confidence - need more verification
  0-39:   VERY LOW confidence - missing critical checks

EXIT THRESHOLD: ≥ 80
```

### Confidence Calculation Examples

**Example 1: Strong Confidence**

```
Rounds: 4
Pattern Types: 6 (base, arrows, actions, headers, spot-checks, manual)
Spot Checks: 12 files
User Challenges: 0

Score = (4 × 10) + (6 × 5) + (12 × 2) - (0 × 20)
      = 40 + 30 + 24 - 0
      = 94

VERDICT: ✅ HIGH confidence - safe to exit if all other criteria met
```

**Example 2: False Confidence**

```
Rounds: 2
Pattern Types: 3 (base, arrows, spot-checks)
Spot Checks: 5 files
User Challenges: 1 ("are you sure?")

Score = (2 × 10) + (3 × 5) + (5 × 2) - (1 × 20)
      = 20 + 15 + 10 - 20
      = 25

VERDICT: ❌ VERY LOW confidence - need 2+ more rounds, more patterns, more spot-checks
```

**Example 3: After User Challenge**

```
Initial:
  Rounds: 3, Pattern Types: 4, Spot Checks: 10, User Challenges: 0
  Score = 30 + 20 + 20 - 0 = 70 (MEDIUM)

User Challenge: "are you sure?"

Updated:
  Rounds: 3, Pattern Types: 4, Spot Checks: 10, User Challenges: 1
  Score = 30 + 20 + 20 - 20 = 50 (LOW)

After Re-Verification (Round 4):
  Rounds: 4, Pattern Types: 5, Spot Checks: 15, User Challenges: 1
  Score = 40 + 25 + 30 - 20 = 75 (MEDIUM)

After Round 5:
  Rounds: 5, Pattern Types: 6, Spot Checks: 20, User Challenges: 1
  Score = 50 + 30 + 40 - 20 = 100 (HIGH)

VERDICT: ✅ Recovered confidence through additional rounds
```

### Component Metrics

**Rounds (Weight: 10 points each)**

Minimum: 3
Recommended: 4-5
Reasoning: Each round catches what previous missed

**Pattern Types (Weight: 5 points each)**

Minimum: 5
Recommended: 6-8
Types:
1. Base patterns (e.g., " 5a\| 5b")
2. Punctuation variations (e.g., "5a:\|5b:")
3. Arrow variations (e.g., "5a →\|→ 5a")
4. Action variations (e.g., "back to\|Proceed to")
5. Header variations (e.g., "Stage 5a:\|STAGE 5a:")
6. Spot-checks (manual file reading)
7. Context searches (grep -B/-A)
8. File-specific searches (templates, prompts)

**Spot Checks (Weight: 2 points each)**

Minimum: 10 files
Recommended: 15-20 files
Method: Random selection, read actual content (not just grep)

**User Challenges (Weight: -20 points EACH)**

Penalty: SEVERE (-20 points per challenge)
Reasoning: User challenge = evidence you missed something significant
Impact: One challenge requires 2 extra rounds to recover confidence

### When to Admit Uncertainty

**Say "I don't know if I'm done" when:**

- Confidence score < 80
- Only completed 1-2 rounds
- User challenged you
- Spot-checks revealed issues
- You feel uncertain (trust your instinct)

**Don't claim completion if:**
- You haven't tried 5+ pattern types
- You haven't spot-checked 10+ files
- Any exit criteria not met
- User has questioned findings

**Admitting uncertainty is GOOD:**
- Shows self-awareness
- Prevents premature completion
- Invites user guidance
- Builds trust through honesty

---

## Issue Classification System

### Severity Definitions (Context-Dependent)

#### CRITICAL (Blocking)

**Definition:** Prevents users from following workflow or creates cascading errors

**Characteristics:**
- References non-existent files (agent tries to read, fails)
- Contradictory information (says both 7-stage and 10-stage)
- Template errors (propagate to all new epics)
- Incorrect stage sequences (S5 → S4 instead of S5 → S6)

**Impact:** Users cannot complete task, workflow breaks

**Fix Timeline:** Immediate (within 1 hour of discovery)

**Examples:**
```
CRITICAL: README.md line 105 references deleted file `diagrams/workflow_diagrams.md`
  WHY: Agent tries to read this file, gets error, cannot proceed

CRITICAL: stages/s5/s5_p1_planning_round1.md line 50 says "proceed to S4"
  WHY: Should be S6 - creates infinite loop in workflow

CRITICAL: templates/feature_readme_template.md line 63 says "S5 - TODO Creation"
  WHY: Propagates wrong stage name to all new features
```

**Context Factor:** Critical in frequently-used files, High in rarely-used files

#### HIGH

**Definition:** Causes confusion or requires mental translation but doesn't block

**Characteristics:**
- Incorrect file paths (user can figure out correct path but wastes time)
- Wrong stage numbers in prerequisites (user can infer but confusing)
- Outdated terminology in core guides (requires translation)
- Missing sections in templates (user has to add manually)

**Impact:** Slows down users, causes frustration, increases errors

**Fix Timeline:** Same day (within 4 hours)

**Examples:**
```
HIGH: prompts/s5_s8_prompts.md line 304 references `stages/s9/s6_execution.md`
  WHY: Should be `stages/s6/s6_execution.md` - user wastes time finding correct file

HIGH: EPIC_WORKFLOW_USAGE.md line 75 uses "5a → 5b → 5c"
  WHY: Should be "S5 → S6 → S7" - user has to mentally translate

HIGH: templates/feature_readme_template.md missing S9 and S10 sections
  WHY: User has to add manually when creating epic
```

**Context Factor:** High in templates/prompts/core guides, Medium in reference materials

#### MEDIUM

**Definition:** Minor confusion, doesn't affect workflow

**Characteristics:**
- Notation inconsistencies (mixed old/new but not confusing)
- Incorrect counts (guide count, stage count)
- Cross-reference to deprecated but existing files
- Missing cross-references (would be helpful but not required)

**Impact:** Slight confusion, no workflow impact

**Fix Timeline:** Within 1-2 days

**Examples:**
```
MEDIUM: README.md line 874 says "12 stage guides" (should be "35")
  WHY: Misleading but doesn't prevent use

MEDIUM: EPIC_WORKFLOW_USAGE.md line 86 says "(1-7)" (should be "(S1-S10)")
  WHY: Inconsistent with rest of document but understandable

MEDIUM: glossary.md missing cross-reference to new S8 stage
  WHY: Would be helpful but not required for workflow
```

**Context Factor:** Medium in documentation, Low in examples

#### LOW

**Definition:** Cosmetic, intentional, or negligible impact

**Characteristics:**
- Notation in intentional contexts (labels, time estimates)
- Stylistic inconsistencies
- Redundant information
- Unclear wording (but correct information)

**Impact:** Negligible

**Fix Timeline:** Next audit cycle or batch with other fixes

**Examples:**
```
LOW: reference/stage_5/stage_5_reference_card.md line 12 says "STAGE 5a"
  WHY: Intentional section label for reference card (document-specific)

LOW: reference/stage_5/stage_5_reference_card.md line 176 says "5a: 2h"
  WHY: Intentional shorthand in time estimate table (space-constrained)

LOW: faq_troubleshooting.md uses both "folder" and "directory"
  WHY: Stylistic inconsistency but meaning clear
```

**Context Factor:** Low everywhere unless documented as intentional (then OK)

### Context-Based Classification

**Same error, different severity based on context:**

**Example: "S10.P1" Reference**

```
FILE: prompts/s5_s8_prompts.md
CONTEXT: "Feature smoke testing is in S10.P1"
ANALYSIS: S10.P1 is Guide Updates, NOT feature smoke testing (which is S7.P1)
SEVERITY: ❌ CRITICAL (prompts used for every feature - high frequency error)

FILE: debugging/discovery.md
CONTEXT: "Feature testing occurs in S10.P1"
ANALYSIS: Same error (feature testing is S7.P1, not S10.P1)
SEVERITY: ❌ HIGH (debugging used frequently, but less than prompts)

FILE: reference/hands_on_data_inspection.md
CONTEXT: "See S10.P1 for feature testing"
ANALYSIS: Same error
SEVERITY: ⚠️ MEDIUM (reference material used less frequently)

FILE: debugging/root_cause_analysis.md
CONTEXT: "S10.P1 Guide Update Workflow"
ANALYSIS: CORRECT - S10.P1 IS Guide Updates in this context
SEVERITY: ✅ INTENTIONAL (keep as-is)
```

**Classification Decision Tree:**

```
STEP 1: Is this error or intentional?
  → Use Context-Sensitive Analysis Guide
  → If INTENTIONAL: Severity = LOW (document as intentional)
  → If ERROR: Proceed to Step 2

STEP 2: Does this prevent workflow execution?
  → YES: Severity = CRITICAL
  → NO: Proceed to Step 3

STEP 3: How frequently is this file used?
  → Templates/Prompts/Core guides: Severity = HIGH
  → Stage guides: Severity = HIGH
  → Reference materials: Severity = MEDIUM
  → Examples/FAQs: Severity = LOW

STEP 4: Does this cause confusion?
  → Requires mental translation: Severity = HIGH
  → Minor inconsistency: Severity = MEDIUM
  → Cosmetic only: Severity = LOW
```

---

## Reporting Template

### Audit Report Structure

```markdown
# guides_v2 Audit Report - [Date]

**Auditor:** [Agent ID/Name]
**Audit Type:** [Post-Restructuring / Periodic Maintenance / User-Requested]
**Trigger:** [What prompted this audit]
**Duration:** X hours Y minutes
**Status:** [IN PROGRESS / COMPLETE / BLOCKED]

---

## Executive Summary

**Scope:** [Number] files across [N] folders
**Rounds Completed:** N
**Issues Found:** X critical, Y high, Z medium, W low
**Issues Fixed:** X critical, Y high, Z medium, W low
**Remaining:** W low (all documented as intentional)
**Confidence Score:** XX/100 ([HIGH/MEDIUM/LOW])

**Overall Assessment:** [PASS / NEEDS WORK / BLOCKED]

**Key Findings:**
- [Most significant finding 1]
- [Most significant finding 2]
- [Most significant finding 3]

---

## User Challenges Received

**Total Challenges:** N

### Challenge 1: [Date/Time]
**User Question:** "Are you sure there are no remaining issues?"
**Context:** After Round 2, claimed completion with 68 remaining instances

**Response:**
- Acknowledged concern
- Re-verified with fresh patterns
- Found 47 additional instances (arrow variations)

**Outcome:**
- Looped back to Round 3
- Applied 47 fixes
- Confidence decreased from 70 → 50

### Challenge 2: [Date/Time]
**User Question:** "Did you actually make the fixes?"
**Context:** Showed grep output but no verification

**Response:**
- Provided before/after file content for 5 examples
- Spot-checked 5 random files with actual content
- Confirmed all sed commands applied correctly

**Outcome:**
- Proved fixes were applied
- Added verification step to workflow
- Confidence increased to 75

**Lessons:**
- User challenges indicate missed verification steps
- Always provide file content, not just grep output
- Challenges are HELPFUL - they improve audit quality

---

## False Completion Claims

**Times Claimed Complete Prematurely:** 2

### Claim 1: After Round 2
**Claim:** "Audit complete - all issues fixed"
**Reality:** 47 issues remained (arrow variations not searched)
**Why Wrong:** Only tried 3 pattern types, didn't spot-check
**Impact:** User challenged, found issues immediately

### Claim 2: After Round 3
**Claim:** "All fixes verified and applied"
**Reality:** Didn't actually verify sed commands applied
**Why Wrong:** Showed grep output, didn't read actual files
**Impact:** User questioned verification, had to prove fixes

**Lessons:**
- Don't claim complete without minimum 3 rounds
- Don't claim complete without spot-checks
- Don't claim verification without file content proof

---

## Round-by-Round Summary

### Round 1: Initial Discovery

**Date:** YYYY-MM-DD
**Duration:** 45 minutes
**Patterns Used:**
1. `grep -rn " 5a\| 5b\| 5c"` → Found 123 issues
2. `grep -rn "stages/s9/s6_\|stages/s10/s7_"` → Found 15 issues
3. `grep -rn "[0-9]-stage"` → Found 3 issues

**Found:** 141 issues total
  - Critical: 8
  - High: 35
  - Medium: 72
  - Low: 26

**Fixed:** 114 issues
**Remaining:** 27 (further analysis needed)
**New Discovery:** Missed arrow variations (5a →, → 5a)
**Decision:** Loop back to Round 2

### Round 2: Arrow and Variation Search

**Date:** YYYY-MM-DD
**Duration:** 50 minutes
**Patterns Used:**
1. `grep -rn "5a →\|→ 5a\|5a→"` → Found 68 issues
2. `grep -rn "back to\|Proceed to\|restart"` → Found 15 issues

**Found:** 83 issues total
  - Critical: 2
  - High: 28
  - Medium: 48
  - Low: 5

**Fixed:** 78 issues
**Remaining:** 5 (appears intentional)
**New Discovery:** Action verb variations
**Decision:** Loop back to Round 3

### Round 3: Spot-Checks and Verification

**Date:** YYYY-MM-DD
**Duration:** 40 minutes
**Patterns Used:**
1. Re-ran all Round 1-2 patterns
2. Spot-checked 12 random files
3. Manual reading of templates and prompts

**Found:** 5 issues (all confirmed intentional)
**Fixed:** 0 (all documented as intentional)
**Remaining:** 5 (documented below)
**New Discovery:** None
**Decision:** Present to user for approval

**Spot-Check Results:**
- templates/feature_readme_template.md: ✅ Clean
- stages/s7/s7_p1_smoke_testing.md: ✅ Clean
- prompts/s5_s8_prompts.md: ✅ Clean
- reference/implementation_orchestration.md: ✅ Clean
- [8 more files - all clean]

---

## Issues by Severity

### Critical Issues (10 total, 10 fixed)

#### Issue C1
**File:** README.md
**Line:** 105
**Pattern:** `grep -rn "diagrams/workflow_diagrams.md"`
**Before:** `See [workflow diagram](diagrams/workflow_diagrams.md)`
**After:** `[Removed - file deleted in restructuring]`
**Verified:** ✅ `grep -n "diagrams/workflow" README.md` → No results
**Fix Date:** YYYY-MM-DD

#### Issue C2
**File:** templates/feature_readme_template.md
**Line:** 63
**Pattern:** Manual review
**Before:** `S5 - TODO Creation`
**After:** `S5 - Implementation Planning`
**Verified:** ✅ Read actual file line 63
**Fix Date:** YYYY-MM-DD

[Continue for all critical issues...]

### High Priority Issues (63 total, 63 fixed)

[Same format as critical...]

### Medium Priority Issues (120 total, 120 fixed)

[Same format as critical...]

### Low Priority Issues (31 total, 26 fixed, 5 documented as intentional)

[List fixed, then intentional below...]

---

## Intentional Remaining Instances

**Total:** 5 instances documented as intentional

### Case 1: Reference Card Section Labels
**Files:** reference/stage_5/stage_5_reference_card.md
**Lines:** 12, 46, 54, 71, 75
**Pattern:** "STAGE 5a", "STAGE 5b", "STAGE 5c"
**Context:**
```markdown
12: ## STAGE 5a: Planning Round 1
46: ## STAGE 5b: Planning Round 2
54: ## STAGE 5c: Planning Round 3
```
**Reason:** Reference card uses old notation as section labels for clarity
**Why Intentional:** Document-specific formatting, not workflow documentation
**Acceptable:** ✅ Yes - quick reference format
**Documented By:** [Agent ID]

### Case 2: Time Estimate Shorthand
**File:** reference/stage_5/stage_5_reference_card.md
**Lines:** 176-193 (table)
**Pattern:** "5a: 2h", "5b: 1h", "5c: 30m"
**Context:**
```markdown
| Phase | Duration |
|-------|----------|
| 5a    | 2 hours  |
| 5b    | 1 hour   |
```
**Reason:** Table format with space constraints uses shorthand
**Why Intentional:** Compact reference format
**Acceptable:** ✅ Yes - shorthand in tables acceptable
**Documented By:** [Agent ID]

[Continue for all intentional cases...]

---

## Verification Evidence

### Pattern Verification

**Verification Date:** YYYY-MM-DD

**Old patterns remaining:**
```bash
$ grep -rn " 5a\| 5b\| 5c" --include="*.md" --exclude="*AUDIT*.md" | wc -l
5

# All 5 verified as intentional cases documented above
```

**New patterns confirmed:**
```bash
$ grep -rn "S5 → S6 → S7" --include="*.md" | wc -l
15

# Sample matches:
EPIC_WORKFLOW_USAGE.md:75:The feature loop goes S5 → S6 → S7 → S8
README.md:234:Feature stages: S5 → S6 → S7 → S8
```

### Spot-Check Results

**Total Files Checked:** 12
**Method:** Random selection, manual reading
**Issues Found:** 0

**Files Checked:**
1. ✅ templates/feature_readme_template.md - Clean
2. ✅ stages/s7/s7_p1_smoke_testing.md - Clean
3. ✅ prompts/s5_s8_prompts.md - Clean
4. ✅ reference/implementation_orchestration.md - Clean
5. ✅ stages/s2/s2_p1_research.md - Clean
6. ✅ templates/epic_smoke_test_plan_template.md - Clean
7. ✅ debugging/loop_back.md - Clean
8. ✅ stages/s9/s9_p2_epic_qc_rounds.md - Clean
9. ✅ reference/glossary.md - Clean
10. ✅ prompts/s2_prompts.md - Clean
11. ✅ stages/s5/s5_p3_planning_round3.md - Clean
12. ✅ missed_requirement/realignment.md - Clean

### Before/After Examples

#### Example 1: File Path Fix

**File:** prompts/s5_s8_prompts.md
**Line:** 304

**Before:**
```markdown
I'm reading `stages/s9/s6_execution.md` to ensure I follow...
```

**After:**
```markdown
I'm reading `stages/s6/s6_execution.md` to ensure I follow...
```

**Verification:**
```bash
$ grep -n "stages/s6/s6_execution" prompts/s5_s8_prompts.md
304:I'm reading `stages/s6/s6_execution.md` to ensure I follow...

$ grep -n "stages/s9/s6_execution" prompts/s5_s8_prompts.md
[no results - confirms old path removed]
```

#### Example 2: Notation Fix

**File:** EPIC_WORKFLOW_USAGE.md
**Line:** 75

**Before:**
```markdown
The feature loop goes 5a → 5b → 5c → 5d → 5e
```

**After:**
```markdown
The feature loop goes S5 → S6 → S7 → S8
```

**Verification:**
```bash
$ sed -n '75p' EPIC_WORKFLOW_USAGE.md
The feature loop goes S5 → S6 → S7 → S8

$ grep -n "5a → 5b → 5c" EPIC_WORKFLOW_USAGE.md
[no results - confirms old notation removed]
```

[3 more examples...]

---

## Confidence Calibration

**Calculation:**

```
Rounds: 3
Pattern Types: 6 (base, arrows, actions, headers, spot-checks, manual)
Spot Checks: 12 files
User Challenges: 2 ("are you sure?", "did you make fixes?")

Score = (3 × 10) + (6 × 5) + (12 × 2) - (2 × 20)
      = 30 + 30 + 24 - 40
      = 44

Initial Confidence: 44/100 (LOW)
```

**After Round 4 (response to challenges):**

```
Rounds: 4
Pattern Types: 7 (added context searches)
Spot Checks: 15 files
User Challenges: 2 (no new challenges)

Score = (4 × 10) + (7 × 5) + (15 × 2) - (2 × 20)
      = 40 + 35 + 30 - 40
      = 65

Updated Confidence: 65/100 (MEDIUM)
```

**After Round 5 (additional verification):**

```
Rounds: 5
Pattern Types: 8 (added manual template review)
Spot Checks: 20 files
User Challenges: 2 (no new challenges)

Score = (5 × 10) + (8 × 5) + (20 × 2) - (2 × 20)
      = 50 + 40 + 40 - 40
      = 90

Final Confidence: 90/100 (HIGH)
```

**Confidence Assessment:** ✅ HIGH (≥ 80) - Safe to exit loop

---

## Blockers Discovered

**Total Blockers:** 2

### Blocker 1: Template Errors Propagating
**Issue:** feature_readme_template.md had 5 errors with old stage names
**Impact:** All NEW features created from this template would have wrong names
**Severity:** CRITICAL
**Status:** ✅ RESOLVED
**Resolution:** Fixed template, documented need to check templates FIRST in future audits

### Blocker 2: Prompt File Paths Incorrect
**Issue:** s5_s8_prompts.md referenced non-existent file paths
**Impact:** Agents following prompts would fail to read guides
**Severity:** CRITICAL
**Status:** ✅ RESOLVED
**Resolution:** Fixed 15 file path references, added verification step

**Lessons:**
- Check templates and prompts FIRST (they have highest impact)
- Verify file paths point to existing files
- Test critical workflows after fixes

---

## Automated vs Manual Findings

### Automated Findings (Grep-Based)

**Total:** 219 issues found via grep patterns
**Efficiency:** High (found bulk of issues quickly)
**Accuracy:** Medium (required context analysis for many)

**Breakdown:**
- Base patterns: 123 issues
- Arrow variations: 68 issues
- Action verbs: 15 issues
- Headers: 8 issues
- File paths: 15 issues

### Manual Findings (Spot-Checks)

**Total:** 2 issues found via manual reading
**Efficiency:** Low (time-consuming)
**Accuracy:** High (context automatically considered)

**Findings:**
- README.md: Incorrect guide count (missed by grep because no pattern)
- EPIC_WORKFLOW_USAGE.md: Conceptual error in workflow description (correct notation but wrong sequence)

**Lessons:**
- Grep finds 99% of pattern-based issues
- Manual checks catch conceptual errors
- Both are necessary for complete audit

---

## Lessons Learned

### What Worked Well

1. **Iterative Loop Approach**
   - Each round caught what previous missed
   - Fresh eyes prevented confirmation bias
   - Converged to zero issues by Round 3

2. **Context-Sensitive Analysis**
   - Prevented false positives in reference cards
   - Documented intentional cases clearly
   - User understood why some instances kept

3. **Incremental Verification**
   - Fixed one group at a time
   - Verified each fix immediately
   - Caught sed errors early

4. **User Challenges**
   - Improved thoroughness
   - Caught premature completion
   - Built trust through honesty

### What Could Improve

1. **Initial Pattern Coverage**
   - Round 1 should try more variations
   - Consider arrows, actions, punctuation upfront
   - Reduce number of rounds needed

2. **Template Priority**
   - Should check templates FIRST (highest impact)
   - Templates propagate errors to new epics
   - Critical to fix early

3. **Verification Documentation**
   - Should provide file content examples earlier
   - Don't wait for user to ask for proof
   - Include before/after in first report

4. **Confidence Calibration**
   - Should calculate score explicitly
   - Don't rely on subjective feeling
   - Share score with user for transparency

### Recommendations for Next Audit

1. **Start with Critical Files**
   - Templates first (propagate to new epics)
   - Prompts second (affect all transitions)
   - Core documentation third (README, EPIC_WORKFLOW_USAGE)

2. **Broader Pattern Coverage in Round 1**
   - Don't just search " 5a" - also search "5a:", "5a →", "back to 5a"
   - Try 5+ pattern types in Round 1
   - Reduce rounds needed to converge

3. **Automated Pre-Checks**
   - Script to validate file paths exist
   - Script to count files vs documented counts
   - Run before manual audit begins

4. **Explicit Confidence Tracking**
   - Calculate score after each round
   - Share with user for transparency
   - Use as objective exit criterion

---

## Audit Completion Checklist

- [x] Minimum 3 rounds completed (completed 5)
- [x] Zero new issues in final round (Round 5 found 0)
- [x] Verified all fixes applied (spot-checked 20 files)
- [x] Documented all intentional cases (5 cases documented)
- [x] User challenges addressed (2 challenges, re-verified after each)
- [x] Confidence score ≥ 80 (score: 90/100)
- [x] Pattern diversity ≥ 5 types (used 8 types)
- [x] Spot-checks ≥ 10 files (checked 20 files)

**Exit Criteria Met:** ✅ ALL

**Audit Status:** ✅ COMPLETE

**User Approval:** [Pending/Approved]

**Sign-off:** [Agent ID] - YYYY-MM-DD HH:MM

---

**END OF AUDIT REPORT**
```

---

## Common Pitfalls

**Ranked by frequency and severity from actual audit experience:**

### 🚨 Pitfall 1: Premature Completion (MOST COMMON, MOST DANGEROUS)

**Frequency:** Occurred 3 times in Session 2-3 audit
**Severity:** CRITICAL
**Impact:** Missed 100+ issues, required user challenges to detect

**Symptom:** Claiming audit complete after 1-2 rounds without verification

**Why it happens:**
- Trust grep patterns too much
- Assume coverage is complete after first round
- Want to finish quickly
- Overconfidence in initial findings

**How to Detect:**
```
RED FLAGS:
- ❌ Only completed 1-2 rounds
- ❌ Didn't spot-check random files
- ❌ Didn't try pattern variations
- ❌ User asks "are you sure?"
- ❌ Confidence score < 60
```

**Prevention:**
```
MANDATORY RULES:
✅ MINIMUM 3 rounds (non-negotiable)
✅ Each round uses DIFFERENT patterns
✅ Spot-check 10+ random files
✅ Calculate confidence score (must be ≥ 80)
✅ Only exit when Round N finds ZERO new issues
✅ If user challenges, loop back immediately

ENFORCEMENT:
- Set calendar reminder to do Round 3 even if "done"
- Calculate confidence score explicitly, don't rely on feeling
- Ask yourself: "What patterns did I NOT try yet?"
```

**Historical Evidence:**
```
Round 1: Claimed complete after finding 123 instances
Reality: User asked "are you sure?" → Found 68 MORE instances

Round 2: Claimed complete after fixing 68 more
Reality: User asked "did you make fixes?" → Had to prove verification

Round 3: Provided verification, claimed complete
Reality: User asked "assume guide is wrong" → Found guide issues
```

---

### 🚨 Pitfall 2: Not Verifying Fixes (SECOND MOST COMMON)

**Frequency:** Occurred 1 time (but caught by user)
**Severity:** HIGH
**Impact:** Could report "complete" with NO fixes actually applied

**Symptom:** Using sed to fix but not verifying changes applied

**Why it happens:**
- Assume sed worked correctly
- Trust automation without verification
- Don't read actual file contents
- Show grep output but not actual files

**How to Detect:**
```
RED FLAGS:
- ❌ Report only shows grep commands
- ❌ No before/after file content examples
- ❌ Didn't re-read fixed files
- ❌ User asks "did you actually make the fixes?"
```

**Prevention:**
```
MANDATORY VERIFICATION PROTOCOL:

After EVERY sed command:

1. Run sed
   sed -i 's/OLD/NEW/g' file.md

2. Verify NEW exists (IMMEDIATELY)
   grep -n "NEW" file.md

3. Verify OLD gone (IMMEDIATELY)
   grep -n "OLD" file.md  # Should return nothing

4. Read actual file lines
   sed -n 'LINEp' file.md  # Replace LINE with line number

5. Document before/after
   File: path/to/file.md
   Before: [actual old content]
   After: [actual new content]
   Verified: [show grep output]
```

**Example Verification:**
```bash
# Fix applied
$ sed -i 's/5a → 5b/S5 → S6/g' EPIC_WORKFLOW_USAGE.md

# Verify new pattern exists
$ grep -n "S5 → S6" EPIC_WORKFLOW_USAGE.md
75:The workflow goes S5 → S6 → S7

# Verify old pattern gone
$ grep -n "5a → 5b" EPIC_WORKFLOW_USAGE.md
[no results - GOOD]

# Read actual line
$ sed -n '75p' EPIC_WORKFLOW_USAGE.md
The workflow goes S5 → S6 → S7

✅ VERIFIED - Fix actually applied
```

---

### ⚠️ Pitfall 3: Insufficient Pattern Coverage (COMMON)

**Frequency:** Occurred every round until patterns exhausted
**Severity:** MEDIUM
**Impact:** Each round found 50-100 more issues

**Symptom:** Missing pattern variations, same patterns each round

**Why it happens:**
- Only search for common patterns
- Don't consider edge cases (arrows, punctuation, actions)
- Use same patterns every round
- Don't brainstorm variations

**How to Detect:**
```
RED FLAGS:
- ❌ Round 2 finds 50+ issues Round 1 missed
- ❌ Using same grep patterns each round
- ❌ Didn't try: punctuation, arrows, actions, context
- ❌ User finds issues you missed
```

**Prevention:**
```
PATTERN BRAINSTORMING CHECKLIST:

For each base pattern, try:
✅ Punctuation: "5a:", "5a-", "5a)", "(5a)"
✅ Arrows: "5a →", "→ 5a", "5a→", "→5a"
✅ Actions: "back to 5a", "restart 5a", "Proceed to 5a"
✅ Headers: "## 5a:", "### Stage 5a"
✅ Sequences: "5a → 5b → 5c"
✅ Context: grep -B 5 -A 5 "5a"
✅ Case: "Stage 5a", "STAGE 5a", "stage 5a"
✅ Files: "5a_planning.md", "stage_5a"
```

**Example Progression:**
```
Round 1: " 5a\| 5b" → Found 123
MISSED: Arrows, actions, punctuation

Round 2: "5a →\|→ 5a" → Found 68
MISSED: Actions, headers

Round 3: "back to 5a\|Proceed to 5b" → Found 15
MISSED: Spot-checks, manual review

Round 4: Spot-checks → Found 0
✅ COMPLETE
```

---

### ⚠️ Pitfall 4: Ignoring Intentional Cases (MODERATE)

**Frequency:** Would occur without context analysis
**Severity:** MEDIUM
**Impact:** Breaks document structure, removes meaningful labels

**Symptom:** "Fixing" intentional labels, shorthand, or quotes

**Why it happens:**
- Pattern matching without reading context
- Not understanding document purpose
- Bulk find/replace without review
- Treating ALL matches as errors

**How to Detect:**
```
RED FLAGS:
- ❌ Fixing reference card section labels
- ❌ Fixing time estimate shorthand in tables
- ❌ Fixing ASCII art headers
- ❌ Removing old notation from historical examples
```

**Prevention:**
```
CONTEXT ANALYSIS FOR AMBIGUOUS MATCHES:

1. Read 10 lines before and after
2. Identify document purpose
3. Ask: "Is this intentional for THIS document?"
4. Check file type:
   - Reference card? May use old notation as labels
   - Table? May use shorthand for space
   - Quote/example? May preserve old notation
   - Current workflow doc? Should use new notation

IF INTENTIONAL:
  - Document why it's acceptable
  - Add to intentional cases list
  - Don't fix

IF ERROR:
  - Fix and verify
```

**Intentional Examples:**
```
✅ KEEP: reference/stage_5_reference_card.md line 12: "STAGE 5a"
WHY: Section label for reference card

✅ KEEP: stage_5_reference_card.md line 176: "5a: 2h"
WHY: Shorthand in time estimate table

❌ FIX: EPIC_WORKFLOW_USAGE.md line 75: "5a → 5b"
WHY: Current workflow documentation (not reference card)
```

---

### ⚠️ Pitfall 5: Single-Pass Mentality (MODERATE)

**Frequency:** Tendency to think "one round is enough"
**Severity:** MEDIUM
**Impact:** Missed issues, premature completion

**Symptom:** Linear workflow instead of iterative loop

**Why it happens:**
- Want to avoid repetition
- Think one comprehensive pass is enough
- Don't embrace fresh eyes principle
- Efficiency mindset over thoroughness

**How to Detect:**
```
RED FLAGS:
- ❌ Only 1-2 rounds completed
- ❌ Didn't loop back when issues found
- ❌ Assumed first pass covered everything
- ❌ Didn't question previous findings
```

**Prevention:**
```
ITERATIVE LOOP MINDSET:

PLAN for 3-5 rounds from the start
  - Round 1: Base patterns
  - Round 2: Variations
  - Round 3: Context
  - Round 4: Spot-checks
  - Round 5: Verification

EACH ROUND:
  - Forget previous assumptions
  - Try DIFFERENT patterns
  - Explore DIFFERENT folders
  - Question EVERYTHING

ONLY EXIT WHEN:
  - Round N finds ZERO new issues
  - Round N+1 ALSO finds zero
  - All exit criteria met
```

**Round Tracking:**
```
Track what each round contributed:

Round 1: 123 issues (base patterns)
  → Learned: missed variations

Round 2: 68 issues (arrows)
  → Learned: missed actions

Round 3: 15 issues (actions)
  → Learned: mostly complete

Round 4: 0 issues (spot-checks)
  → Learned: verification clean

✅ EXIT: Two consecutive zero-issue rounds
```

---

### ⚠️ Pitfall 6: Confirmation Bias (MODERATE)

**Frequency:** Natural tendency, must actively fight
**Severity:** MEDIUM
**Impact:** Missed issues in previously "cleared" areas

**Symptom:** Assuming previous rounds covered everything, not re-checking

**Why it happens:**
- Trust previous work too much
- Don't want to admit gaps in earlier rounds
- Avoid re-checking same areas
- Carry forward assumptions

**How to Detect:**
```
RED FLAGS:
- ❌ "I already checked folder X"
- ❌ Not trying new patterns in Round 2+
- ❌ Skipping folders checked in Round 1
- ❌ No new discoveries in later rounds (but still < 3 rounds)
```

**Prevention:**
```
FRESH EYES TECHNIQUES:

Physical Reset:
  - Take 5-minute break between rounds
  - Don't look at Round 1 notes before Round 2 Discovery
  - Start in DIFFERENT folder each round

Mental Reset:
  - Ask: "What if I missed X?"
  - Question: "What variations didn't I consider?"
  - Challenge: "What would I try if starting fresh?"

Pattern Reset:
  - Use COMPLETELY different patterns each round
  - Re-check folders with new patterns
  - Spot-check even "cleared" files

Document What NOT Checked:
  - After each round: "I didn't check: X, Y, Z"
  - Next round: Start with what was skipped
```

**Example:**
```
Round 1: Checked templates/ with " 5a" pattern
  Found: 15 issues
  Mindset: "Templates done ✓"

Round 2: FRESH EYES - Re-check templates/ with "5a →" pattern
  Found: 8 MORE issues in SAME folder
  Lesson: Folder not "done" until all patterns tried

Round 3: FRESH EYES - Re-check templates/ with manual reading
  Found: 1 MORE conceptual error
  Lesson: Grep doesn't catch everything
```

---

### ⚠️ Pitfall 7: No Evidence Provided (LOW FREQUENCY, HIGH IMPACT)

**Frequency:** Happened once (Round 2)
**Severity:** HIGH when it happens
**Impact:** User can't verify claims, loses trust

**Symptom:** Claims without proof, grep output instead of file content

**Why it happens:**
- Assume user trusts you
- Don't want to clutter report
- Think grep output is sufficient
- Forget user can't see your terminal

**How to Detect:**
```
RED FLAGS:
- ❌ Report has no file content examples
- ❌ Only grep commands shown, no output
- ❌ Claims "fixed 100 issues" with no examples
- ❌ User asks "did you actually make fixes?"
```

**Prevention:**
```
EVIDENCE REQUIREMENTS FOR EVERY REPORT:

1. Before/After Examples (MINIMUM 3):
   File: path/to/file.md
   Line: 123
   Before: `old content`
   After: `new content`
   Verification: [show grep output]

2. Grep Command Outputs:
   $ grep -rn "PATTERN" --include="*.md"
   [show actual results, not just command]

3. Spot-Check Results:
   File: path/to/file.md
   Status: Clean/Issues Found
   [Paste relevant sections if issues]

4. Verification Commands:
   $ grep -n "OLD pattern" file.md
   [no results - confirms removal]

   $ grep -n "NEW pattern" file.md
   123: NEW pattern here

5. Counts:
   Before: 123 instances
   After: 5 instances (all intentional)
   Reduction: 118 fixes
```

**Example Report Section:**
```
## Evidence: File Path Fixes

**Issue:** stages/s9/s6_execution.md → stages/s6/s6_execution.md

**Files Fixed:** 15

**Example 1:** prompts/s5_s8_prompts.md line 304
Before:
```markdown
I'm reading `stages/s9/s6_execution.md` to ensure...
```
After:
```markdown
I'm reading `stages/s6/s6_execution.md` to ensure...
```
Verification:
```bash
$ grep -n "stages/s6/s6_execution" prompts/s5_s8_prompts.md
304:I'm reading `stages/s6/s6_execution.md` to ensure...

$ grep -n "stages/s9/s6_execution" prompts/s5_s8_prompts.md
[no results]
```

[2 more examples...]

**Bulk Verification:**
```bash
$ grep -rn "stages/s9/s6_" --include="*.md" | wc -l
0  # All instances fixed
```
```

---

### ⚠️ Pitfall 8: Skipping Fresh Eyes (LOW FREQUENCY)

**Frequency:** Natural tendency without discipline
**Severity:** MEDIUM
**Impact:** Missed pattern variations, confirmation bias

**Symptom:** Using same assumptions each round, not clearing mental model

**Why it happens:**
- Efficiency mindset (reuse previous knowledge)
- Don't want to "waste time" relearning
- Carry forward biases from Round 1
- Don't take breaks between rounds

**How to Detect:**
```
RED FLAGS:
- ❌ Round 2 uses same patterns as Round 1
- ❌ Check same folders in same order
- ❌ No breaks between rounds
- ❌ Each round finds similar patterns (not expanding)
```

**Prevention:**
```
FRESH EYES PROTOCOL:

BEFORE EACH ROUND:

1. Physical Break (MANDATORY):
   - Take 5-10 minute break
   - Walk away from computer
   - Clear your mind

2. Mental Reset:
   - Start new notepad/file
   - Don't look at previous round notes YET
   - Approach as if you've never seen the codebase

3. Different Approach:
   - Start with different folder than last round
   - Use different search patterns
   - Try opposite order (last round: templates first, this round: templates last)

4. Question Everything:
   "What if previous rounds missed X?"
   "What variations didn't I consider?"
   "What assumptions am I making?"

5. After Discovery, THEN review:
   - Compare findings to previous rounds
   - Identify what was new
   - Learn from differences
```

**Example Fresh Eyes in Action:**
```
Round 1 Approach:
  - Started with templates/
  - Used pattern: " 5a\| 5b"
  - Found: 123 issues

Round 2 Fresh Eyes:
  - Started with prompts/ (DIFFERENT folder)
  - Used pattern: "5a →\|→ 5a" (DIFFERENT pattern)
  - Found: 68 issues (many in folders "cleared" in Round 1)

Round 3 Fresh Eyes:
  - Started with stages/ (DIFFERENT folder again)
  - Used manual reading (DIFFERENT method)
  - Found: 2 conceptual errors grep missed

Lesson: Fresh eyes catch what routine checking misses
```

---

## Real Examples from Audits

**These are ACTUAL examples from Session 2-3 audits (221+ fixes across 110 files):**

### Example 1: grep Command Finding Old Notation

**Scenario:** After stage split (S5 → S5-S8), needed to find old notation

**Command:**
```bash
$ grep -rn " 5a\| 5b\| 5c\| 5d\| 5e" --include="*.md" --exclude="*AUDIT*.md"
```

**Actual Output (first 10 matches):**
```
EPIC_WORKFLOW_USAGE.md:75:The feature loop goes 5a → 5b → 5c → 5d → 5e
EPIC_WORKFLOW_USAGE.md:373:**Stages:** 5a → 5b → 5c → 5d → 5e (for EACH feature)
EPIC_WORKFLOW_USAGE.md:541:After 5e, proceed to S9
EPIC_WORKFLOW_USAGE.md:958:"5e" references in cross-feature alignment
README.md:641:Old S5 phases: 5a, 5b, 5c, 5d, 5e
templates/epic_readme_template.md:63:S5 - TODO Creation (5a)
templates/epic_lessons_learned_template.md:27:5a through 5e phases
reference/implementation_orchestration.md:42:Document title: "5b → 5e Workflow"
reference/stage_5/stage_5_reference_card.md:12:## STAGE 5a: Planning Round 1
reference/stage_5/stage_5_reference_card.md:176:| 5a | 2 hours |
...
[113 more matches]
```

**Total Found:** 123 instances

**Analysis:**
- Lines 1-8: Errors (should use S5→S6→S7→S8)
- Line 9: Intentional (reference card section header)
- Line 10: Intentional (time estimate shorthand)

**Action:** Fixed 113, documented 10 as intentional

### Example 2: sed Command Applying Fix

**Before Fix (EPIC_WORKFLOW_USAGE.md line 75):**
```markdown
The feature loop goes 5a → 5b → 5c → 5d → 5e for each feature.
```

**sed Command:**
```bash
$ sed -i 's/5a → 5b → 5c → 5d → 5e/S5 → S6 → S7 → S8/g' EPIC_WORKFLOW_USAGE.md
```

**Verification:**
```bash
# Verify new pattern exists
$ grep -n "S5 → S6 → S7 → S8" EPIC_WORKFLOW_USAGE.md
75:The feature loop goes S5 → S6 → S7 → S8 for each feature.

# Verify old pattern gone
$ grep -n "5a → 5b → 5c → 5d → 5e" EPIC_WORKFLOW_USAGE.md
[no results]

# Read actual line
$ sed -n '75p' EPIC_WORKFLOW_USAGE.md
The feature loop goes S5 → S6 → S7 → S8 for each feature.
```

**After Fix (EPIC_WORKFLOW_USAGE.md line 75):**
```markdown
The feature loop goes S5 → S6 → S7 → S8 for each feature.
```

**✅ VERIFIED - Fix actually applied**

### Example 3: Context-Sensitive Analysis

**File:** debugging/discovery.md
**Line:** 88

**grep Output:**
```
debugging/discovery.md:88:Feature testing occurs in S10.P1 (smoke testing)
```

**Context Analysis:**
```markdown
# Read 5 lines before and after
$ grep -rn -B 5 -A 5 "S10.P1" debugging/discovery.md

83:During debugging, you may need to restart testing:
84:
85:## When to Loop Back
86:
87:**Feature Testing:**
88:Feature testing occurs in S10.P1 (smoke testing), S10.P2 (QC rounds).
89:If issues are found, you must loop back to the START of feature testing.
90:
91:**Epic Testing:**
92:Epic testing occurs in S9.P1 (epic smoke testing), S9.P2 (epic QC rounds).
93:If issues are found, you must loop back to the START of epic testing.
```

**Analysis:**
- Line 87: "Feature Testing" context
- Line 88: References S10.P1 for feature smoke testing
- Line 92: Correctly references S9.P1 for EPIC testing

**Workflow Check:**
- S10.P1 = Guide Update Workflow (Epic Cleanup)
- S7.P1 = Feature Smoke Testing
- Line 88 is WRONG

**Decision:** ❌ ERROR - Fix to S7.P1

**Fix:**
```bash
$ sed -i 's/S10\.P1 (smoke testing), S10\.P2/S7.P1 (smoke testing), S7.P2/g' debugging/discovery.md
```

**Verification:**
```bash
$ grep -n "S7.P1" debugging/discovery.md
88:Feature testing occurs in S7.P1 (smoke testing), S7.P2 (QC rounds).
```

### Example 4: Intentional Case Documentation

**File:** reference/stage_5/stage_5_reference_card.md
**Lines:** 12, 46, 54, 71, 75

**grep Output:**
```
reference/stage_5/stage_5_reference_card.md:12:## STAGE 5a: Planning Round 1
reference/stage_5/stage_5_reference_card.md:46:## STAGE 5b: Planning Round 2
reference/stage_5/stage_5_reference_card.md:54:## STAGE 5c: Planning Round 3
reference/stage_5/stage_5_reference_card.md:71:## STAGE 5d: Implementation Execution
reference/stage_5/stage_5_reference_card.md:75:## STAGE 5e: Post-Implementation
```

**Context Analysis:**
```markdown
# Read file header
$ sed -n '1,20p' reference/stage_5/stage_5_reference_card.md

1:# Stage 5 Quick Reference Card
2:
3:**Purpose:** Quick reference for Stage 5 Implementation Planning
4:**Format:** Condensed guide with section labels for easy navigation
5:**Note:** This reference card uses "STAGE 5a", "STAGE 5b" notation as section headers
6:          for clarity and continuity. This is document-specific formatting.
...
12:## STAGE 5a: Planning Round 1
```

**Analysis:**
- File is reference card (quick reference format)
- Line 5: Explicitly states old notation used as section headers
- Purpose: Quick navigation, not workflow documentation
- Headers use old notation intentionally for clarity

**Decision:** ✅ INTENTIONAL - Document and keep

**Documentation:**
```markdown
## Intentional Case #1

**File:** reference/stage_5/stage_5_reference_card.md
**Lines:** 12, 46, 54, 71, 75
**Pattern:** "STAGE 5a", "STAGE 5b", "STAGE 5c", etc.
**Context:** Reference card section headers
**Reason:** Document-specific formatting for quick navigation
**Why Acceptable:**
  - Reference card, not workflow documentation
  - Explicitly noted in file header (line 5)
  - Old notation aids continuity for users familiar with structure
**Verified By:** Session 2-3 Audit
**Documented:** YYYY-MM-DD
```

### Example 5: User Challenge Response

**Round 2 Claim:**
> "Audit complete - found and fixed 123 instances of old notation"

**User Challenge:**
> "Are you sure there are no remaining issues?"

**Response Actions:**
```bash
# Step 1: Acknowledge and re-verify
# Tried new pattern: arrows

$ grep -rn "5a →\|→ 5a\|5a→\|→5a" --include="*.md"

EPIC_WORKFLOW_USAGE.md:75:The workflow goes 5a → 5b → 5c
EPIC_WORKFLOW_USAGE.md:373:**Stages:** 5a → 5b → 5c → 5d → 5e
templates/epic_readme_template.md:63:S5 - TODO Creation (5a →)
...
[65 more matches]

# Found 68 MORE instances!
```

**Honest Report:**
```
User was RIGHT to challenge.

Round 2 Re-Verification Results:
- New Pattern: "5a →\|→ 5a\|5a→\|→5a"
- Issues Found: 68
- Why Missed: Round 1 only searched for " 5a" (space-prefixed)
- Action: Fixing 68 additional instances, looping to Round 3

Lesson: Don't claim complete without trying pattern variations
```

**Outcome:**
- Fixed 68 more issues
- Tried action verb patterns in Round 3 (found 15 more)
- Didn't claim complete until Round 4 found ZERO

### Example 6: Spot-Check Finding Conceptual Error

**Round 3 Random File Selection:**
```bash
$ find . -name "*.md" -type f | shuf -n 10

./README.md
./EPIC_WORKFLOW_USAGE.md
./templates/feature_readme_template.md
./stages/s7/s7_p1_smoke_testing.md
./prompts/s5_s8_prompts.md
./reference/implementation_orchestration.md
./debugging/loop_back.md
./stages/s2/s2_p1_research.md
./templates/epic_smoke_test_plan_template.md
./reference/glossary.md
```

**Spot-Check README.md:**
```bash
$ sed -n '870,880p' README.md

870:## Guide Organization
871:
872:### Stage Guides
873:
874:The guides_v2 folder contains 12 comprehensive stage guides:
875:
876:1. Epic Planning (S1)
877:2. Feature Deep Dive (S2)
...
```

**Issue Found:**
- Line 874: Says "12 comprehensive stage guides"
- Reality: 35+ guide files across S1-S10 folders
- grep didn't find because no old notation pattern

**Fix:**
```bash
# Count actual files
$ find stages/ -name "*.md" -type f | wc -l
35

# Fix count
$ sed -i 's/12 comprehensive stage guides/35 stage guides/' README.md

# Verify
$ grep -n "35 stage guides" README.md
874:The guides_v2 folder contains 35 stage guides:
```

**Lesson:** Spot-checks catch conceptual errors grep can't find

### Example 7: Pattern Evolution Across Rounds

**Round 1: Base Pattern**
```bash
$ grep -rn " 5a\| 5b\| 5c\| 5d\| 5e" --include="*.md" | wc -l
123

# Found 123 instances of space-prefixed notation
```

**Analysis After Round 1:**
- What was found: Space-prefixed instances
- What was missed: Arrows, punctuation, actions
- Next round: Try arrow variations

**Round 2: Arrow Variations**
```bash
$ grep -rn "5a →\|→ 5a\|5a→\|→5a" --include="*.md" | wc -l
68

# Found 68 MORE instances with arrows
```

**Analysis After Round 2:**
- What was found: Arrow variations
- What was missed: Action verbs ("back to", "Proceed to")
- Next round: Try action variations

**Round 3: Action Variations**
```bash
$ grep -rn "back to 5[a-e]\|Proceed to 5[a-e]\|restart 5[a-e]" --include="*.md" | wc -l
15

# Found 15 MORE instances with action verbs
```

**Analysis After Round 3:**
- What was found: Action verb variations
- What was missed: Possibly nothing (low count)
- Next round: Spot-checks to confirm

**Round 4: Spot-Checks**
```bash
# Random file sampling
$ find . -name "*.md" -type f | shuf -n 10
[Selected 10 files]

# Manual reading of each
# Found: 0 new pattern-based issues
# Found: 1 conceptual error (README.md guide count)
```

**Total Across 4 Rounds:**
- Round 1: 123 issues (base)
- Round 2: 68 issues (arrows)
- Round 3: 15 issues (actions)
- Round 4: 1 issue (spot-check)
- **Total: 207 issues**

**Lesson:** Each round caught what previous missed - iterative approach essential

---

## Automated Pre-Checks

**Purpose:** Run quick automated checks BEFORE starting manual audit

**When to Use:** At the very beginning of audit, before Stage 1 Discovery

**Benefits:**
- Catch obvious errors quickly
- Validate basic assumptions
- Provide baseline metrics
- Focus manual effort on complex issues

### Pre-Check 1: File Path Validation

**Purpose:** Verify all referenced file paths actually exist

**⚠️ Status:** PARTIALLY TESTED (concept validated, script not fully tested)

**Approach:**
```bash
#!/bin/bash
# validate_file_paths.sh

echo "Extracting all .md file references..."

# Find all markdown file references (adjust regex as needed)
# This finds patterns like: stages/sN/filename.md
grep -roh '[a-zA-Z0-9_/-]*\.md' --include="*.md" | sort -u > /tmp/referenced_files.txt

echo "Total unique .md references found: $(wc -l < /tmp/referenced_files.txt)"

# Check which ones don't exist
echo ""
echo "Checking for non-existent files..."
not_found=0

while IFS= read -r filepath; do
  # Skip if contains wildcards or placeholders
  if [[ "$filepath" == *"*"* ]] || [[ "$filepath" == *"{}"* ]]; then
    continue
  fi

  # Check if file exists
  if [ ! -f "$filepath" ]; then
    echo "❌ NOT FOUND: $filepath"
    ((not_found++))
  fi
done < /tmp/referenced_files.txt

echo ""
if [ $not_found -eq 0 ]; then
  echo "✅ All referenced files exist"
else
  echo "❌ Found $not_found non-existent file references"
fi
```

**Usage:**
```bash
$ cd guides_v2/
$ bash validate_file_paths.sh
```

**Example Output:**
```
Extracting all .md file references...
Total unique .md references found: 156

Checking for non-existent files...
❌ NOT FOUND: diagrams/workflow_diagrams.md
❌ NOT FOUND: stages/s9/s6_execution.md
❌ NOT FOUND: stages/s10/s7_p1_smoke_testing.md

❌ Found 3 non-existent file references
```

**Limitations:**
- May not catch all path reference formats
- Regex may need adjustment for specific patterns
- Won't catch incorrect paths that point to wrong existing files

### Pre-Check 2: File Count Comparison

**Purpose:** Compare documented counts to actual file counts

**✅ Status:** TESTED (commands work)

**Script:**
```bash
#!/bin/bash
# compare_counts.sh

echo "=== File Count Validation ==="
echo ""

# Count actual files
actual_total=$(find . -name "*.md" -type f | wc -l)
actual_stages=$(find stages/ -name "*.md" -type f 2>/dev/null | wc -l)
actual_prompts=$(find prompts/ -name "*.md" -type f 2>/dev/null | wc -l)
actual_templates=$(find templates/ -name "*.md" -type f 2>/dev/null | wc -l)
actual_reference=$(find reference/ -name "*.md" -type f 2>/dev/null | wc -l)

echo "Actual Counts:"
echo "  Total .md files: $actual_total"
echo "  stages/ folder: $actual_stages"
echo "  prompts/ folder: $actual_prompts"
echo "  templates/ folder: $actual_templates"
echo "  reference/ folder: $actual_reference"
echo ""

# Extract documented counts (adjust grep patterns for your docs)
echo "Documented Counts (from README.md):"
grep -n "[0-9]\+ stage guides\|[0-9]\+ comprehensive" README.md | head -5
echo ""

# Extract stage count claims
echo "Stage Count Claims:"
grep -n "[0-9]-stage\|[0-9] stage" --include="*.md" -r . | head -10
echo ""

echo "⚠️ Manually compare actual vs documented counts above"
```

**Usage:**
```bash
$ cd guides_v2/
$ bash compare_counts.sh
```

**Example Output:**
```
=== File Count Validation ===

Actual Counts:
  Total .md files: 110
  stages/ folder: 35
  prompts/ folder: 11
  templates/ folder: 16
  reference/ folder: 31

Documented Counts (from README.md):
874:The guides_v2 folder contains 12 comprehensive stage guides:

Stage Count Claims:
EPIC_WORKFLOW_USAGE.md:47:This is a 10-stage workflow
EPIC_WORKFLOW_USAGE.md:86:covering all stages (1-7)
README.md:234:The 10-stage workflow consists of:

⚠️ Manually compare actual vs documented counts above
```

**Analysis:**
- Actual: 35 stage guides
- Documented (README line 874): "12 comprehensive stage guides"
- **MISMATCH - needs fix**

### Pre-Check 3: Basic Pattern Check

**Purpose:** Quick count of known problem patterns

**✅ Status:** TESTED (based on actual audit experience)

**Script:**
```bash
#!/bin/bash
# pattern_check.sh

echo "=== Basic Pattern Check ==="
echo ""

# Adjust patterns based on your recent changes
echo "Checking for old stage notation..."
count_old_notation=$(grep -rn " 5a\| 5b\| 5c\| 5d\| 5e\| 6a\| 6b" --include="*.md" --exclude="*AUDIT*.md" | wc -l)
echo "  Old notation ( 5a, 5b, etc.): $count_old_notation instances"

echo ""
echo "Checking for old file paths..."
count_old_paths=$(grep -rn "stages/s9/s6_\|stages/s10/s7_" --include="*.md" | wc -l)
echo "  Old paths (s9/s6_, s10/s7_): $count_old_paths instances"

echo ""
echo "Checking stage count references..."
count_stage_counts=$(grep -rn "[0-9]-stage\|[0-9] stage" --include="*.md" | wc -l)
echo "  Stage count mentions: $count_stage_counts instances"

echo ""
echo "Checking for deleted file references..."
count_deleted=$(grep -rn "diagrams/workflow_diagrams.md\|deprecated/" --include="*.md" | wc -l)
echo "  Deleted file references: $count_deleted instances"

echo ""
if [ $count_old_notation -eq 0 ] && [ $count_old_paths -eq 0 ] && [ $count_deleted -eq 0 ]; then
  echo "✅ No obvious issues found - proceed to manual audit"
else
  echo "⚠️ Found potential issues - prioritize these in manual audit"
fi
```

**Usage:**
```bash
$ cd guides_v2/
$ bash pattern_check.sh
```

**Example Output:**
```
=== Basic Pattern Check ===

Checking for old stage notation...
  Old notation ( 5a, 5b, etc.): 123 instances

Checking for old file paths...
  Old paths (s9/s6_, s10/s7_): 15 instances

Checking stage count references...
  Stage count mentions: 18 instances

Checking for deleted file references...
  Deleted file references: 3 instances

⚠️ Found potential issues - prioritize these in manual audit
```

### Pre-Check Workflow

**Recommended sequence:**

```
BEFORE STARTING MANUAL AUDIT:

1. Run File Path Validation
   → Identifies broken references immediately
   → High priority issues

2. Run File Count Comparison
   → Identifies documentation drift
   → Medium priority issues

3. Run Basic Pattern Check
   → Estimates scope of known issues
   → Helps prioritize manual effort

4. Create Pre-Check Report
   → Document all findings
   → Use as baseline for Round 1 Discovery

5. Begin Manual Audit
   → Focus on areas flagged by pre-checks
   → Don't skip manual audit - pre-checks catch basics only
```

### Pre-Check Limitations

**What Pre-Checks DON'T Catch:**

- ❌ Context-sensitive errors (S10.P1 correct in some files, wrong in others)
- ❌ Conceptual errors (correct notation but wrong stage number)
- ❌ Intentional cases (need manual review to determine)
- ❌ Pattern variations (pre-checks use fixed patterns)
- ❌ Subtle inconsistencies (wording, terminology drift)

**Pre-checks are a STARTING POINT, not a replacement for manual audit**

---

## Appendix: Quick Reference

### Essential Commands (All Tested ✅)

```bash
# File counting
find . -name "*.md" -type f | wc -l

# Pattern searching
grep -rn "PATTERN" --include="*.md"

# Exclude audit files from search
grep -rn "PATTERN" --include="*.md" --exclude="*AUDIT*.md"

# Case-insensitive search
grep -rin "PATTERN" --include="*.md"

# Count matches
grep -rn "PATTERN" --include="*.md" | wc -l

# Context search
grep -rn -B 5 -A 5 "PATTERN" --include="*.md"

# Apply fix and verify (MANDATORY VERIFICATION)
sed -i 's/OLD/NEW/g' file.md
grep -n "NEW" file.md      # Verify new exists
grep -n "OLD" file.md      # Verify old gone (should be empty)
sed -n 'LINEp' file.md     # Read actual line
```

### Pattern Library (From Actual Audits ✅)

```bash
# Old stage notation (Session 2-3: Found 123)
" 5a\| 5b\| 5c\| 5d\| 5e\| 6a\| 6b\| 6c"

# Arrow variations (Session 2-3: Found 68)
"5a →\|5a→\|→ 5a\|→5a"

# Action verbs with stages (Session 2-3: Found 15)
"back to\|Proceed to\|restart"

# Stage headers (Session 2-3: Found 8)
"Stage 5[a-e]:\|STAGE 5[a-e]:"

# File path errors (Session 2-3: Found 15)
"stages/s9/s6_\|stages/s10/s7_"

# Stage count errors (Session 2-3: Found 3)
"[0-9]-stage workflow\|[0-9] stage workflow"

# Old stage references (Session 2-3: Found 47 intentional)
"(1-7)\|(7 stages)\|7-stage"
```

### Confidence Score Quick Calculator

```
Score = (Rounds × 10) + (Pattern Types × 5) + (Spot Checks × 2) - (User Challenges × 20)

Minimum for HIGH confidence (≥ 80):
  - 3 rounds, 6 pattern types, 10 spot-checks, 0 challenges = 80
  - 4 rounds, 5 pattern types, 10 spot-checks, 0 challenges = 85
  - 5 rounds, 6 pattern types, 10 spot-checks, 0 challenges = 100

After 1 user challenge (-20 points):
  - Need 2 extra rounds to recover (2 × 10 = 20)
  OR 4 extra pattern types (4 × 5 = 20)
  OR 10 extra spot-checks (10 × 2 = 20)
```

### Exit Criteria Checklist

```
Can only exit when ALL are true:

✅ Minimum 3 rounds completed
✅ Round N found ZERO new issues
✅ Round N used 5+ different pattern types
✅ Spot-checked 10+ random files (all clean)
✅ All remaining instances documented as intentional
✅ User has NOT challenged findings
✅ Confidence score ≥ 80
✅ Provided evidence (before/after examples)
```

### Common Mistakes Severity

```
Severity Ranking (by frequency and impact):

1. 🚨 CRITICAL: Premature Completion
   - Occurred 3 times in Session 2-3
   - Missed 100+ issues
   - Prevention: MINIMUM 3 rounds

2. 🚨 HIGH: Not Verifying Fixes
   - Occurred 1 time
   - Could report "done" with no fixes applied
   - Prevention: Read actual files after sed

3. ⚠️ MEDIUM: Insufficient Pattern Coverage
   - Occurred every round until exhausted
   - Each round found 50+ more
   - Prevention: Brainstorm variations upfront

4-8. ⚠️ MEDIUM: All other pitfalls
```

---

**END OF FORMAL AUDIT GUIDE v2.0**

**Version History:**
- v1.0 (2026-01-14): Initial creation based on Session 2-3 audit learnings
- v2.0 (2026-01-14): Major revision after critical review
  - Added "How to Handle User Challenges" section
  - Added "Context-Sensitive Analysis Guide" section
  - Added "Pattern Evolution Strategy" section
  - Added "Confidence Calibration" section
  - Added "Real Examples from Audits" section
  - Added "Automated Pre-Checks" section
  - Updated "Verification Commands Library" with tested vs untested labels
  - Updated "Discovery Checklist" to be more principle-based
  - Updated "Exit Criteria" with objective metrics
  - Updated "Common Pitfalls" with severity rankings and detection triggers
  - Updated "Reporting Template" with missing sections
  - Expanded all sections with actual audit examples
  - Total: ~2000 lines (94% increase from v1.0)

**Changelog Summary:**
- Added 6 new major sections (1000+ lines)
- Rewrote 5 existing sections for clarity and completeness
- Added 50+ real examples from actual audits
- Labeled all commands as tested ✅ or untested ⚠️
- Made all principles actionable with concrete techniques
- Increased from 1033 lines to ~2000 lines
- Transformed from theoretical guide to evidence-based playbook
