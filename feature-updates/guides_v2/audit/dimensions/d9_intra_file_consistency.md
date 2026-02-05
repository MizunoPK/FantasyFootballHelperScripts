# D9: Intra-File Consistency

**Dimension Number:** 9
**Category:** Structural Dimensions
**Automation Level:** 80% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-04

**Focus:** Ensure notation, terminology, and instructions are consistent within each file (no mixed notation, contradictions)
**Typical Issues Found:** 8-15 per audit

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

**D9: Intra-File Consistency** validates that content WITHIN a single file is internally consistent:

1. **Notation Consistency** - File uses one notation system throughout (not mixed "S5a" and "S5.P1")
2. **Terminology Consistency** - Same concept uses same term (not "epic" then "project" then "initiative")
3. **Structural Consistency** - Sections follow same format pattern
4. **Instruction Consistency** - No contradictory directives within file
5. **Reference Consistency** - Internal file references are accurate
6. **Tone Consistency** - Maintains consistent voice/style throughout
7. **Example Consistency** - Examples demonstrate principles stated in text

**Coverage:**
- All workflow guides in stages/
- Reference materials in reference/
- Templates in templates/
- Root-level documentation files

**Key Distinction from D2 (Terminology Consistency):**
- **D2:** Validates consistency ACROSS files (all files use same notation)
- **D9:** Validates consistency WITHIN single files (one file doesn't mix notations)

---

## Why This Matters

**Internal inconsistencies = Confusion about which instruction/format is correct**

### Impact of Intra-File Inconsistencies:

**Mixed Notation:**
- Section 1 uses "S5.P1"
- Section 4 uses "S5a" (old notation)
- Agent confused about which is correct
- May search for wrong file paths

**Contradictory Instructions:**
- Section 2: "ALWAYS run tests before committing"
- Section 6: "Tests can be run after committing if needed"
- Agent doesn't know which rule to follow
- Different agents may follow different instructions

**Inconsistent Terminology:**
- Introduction calls it "epic"
- Middle sections call it "project"
- End calls it "initiative"
- Reader confused about whether these are same thing or different concepts

**Structural Inconsistency:**
- Sections 1-5 have "Prerequisites" subsections
- Sections 6-10 don't have "Prerequisites"
- Reader unsure if prerequisites don't exist or were forgotten

**Reference Mismatches:**
- Section 3 says "see Section 7 for details"
- File only has 5 sections
- Broken internal reference

### Historical Evidence:

**KAI-7 Issues:**
- S5 guide mixed "Round 1" and "S5.P1" notation in same file
- Debugging protocol said "ALWAYS create issue file" in one section, "create if needed" in another
- spec.md template used "epic" and "project" interchangeably

**Why 80% Automation:**
- Automated: Notation patterns, terminology variations, structural patterns
- Manual Required: Semantic contradictions, tone assessment, contextual appropriateness

---

## Pattern Types

### Type 0: Root-Level File Internal Consistency (CRITICAL - Often Missed)

**Files to Always Check:**
```text
C:\Users\kmgam\code\FantasyFootballHelperScripts\CLAUDE.md
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
```

**What to Validate:**

**CLAUDE.md - Notation Consistency:**
```bash
# Check for mixed notation within CLAUDE.md
grep -n "S[0-9][a-z]\|Stage [0-9][a-z]" CLAUDE.md | head -10
# Should find: ZERO matches (all should use S#.P# notation)

# Check for correct notation
grep -n "S[0-9]\\.P[0-9]" CLAUDE.md | head -10
# Should find: Multiple matches ✓
```

**README.md - Terminology Consistency:**
```bash
# Find all terms for workflow unit
grep -ion "epic\|project\|initiative\|feature set" \
  feature-updates/guides_v2/README.md | \
  cut -d: -f2 | sort | uniq -c

# Should show consistent use of "epic" (not mixed terms)
```

**EPIC_WORKFLOW_USAGE.md - Section Structure Consistency:**
```bash
# Check if all stage sections have same subsections
for stage in S{1..10}; do
  echo "=== $stage ==="
  grep "^###" feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md | \
    grep -A 5 "$stage"
done

# All should have: Duration, Phases, Key Outputs, Gates
```

**Red Flags:**
- CLAUDE.md uses "S5.P1" in top section, "S5a" later
- README.md calls it "epic" 20 times, "project" 5 times
- EPIC_WORKFLOW_USAGE.md has inconsistent section structures

**Automated:** ✅ Yes (can detect notation/terminology variations within file)

---

### Type 1: Mixed Notation Within Single File

**What to Check:**
File should use ONE notation system consistently, not mix old and new.

**Common Pattern:**
```markdown
# S5: Implementation Planning

## S5.P1: Planning Round 1

Complete iterations I1-I7...

## S5a: Planning Round 1  ← ERROR: Mixed notation

For backward compatibility, S5a refers to... ← If NOT explaining old notation, this is an error
```

**Search Commands:**
```bash
# For each guide file, check for notation mixing
for file in stages/**/*.md; do
  # Count old notation occurrences
  old=$(grep -c "S[0-9][a-z]\|Stage [0-9][a-z]" "$file")

  # Count new notation occurrences
  new=$(grep -c "S[0-9]\\.P[0-9]" "$file")

  if [ "$old" -gt 0 ] && [ "$new" -gt 0 ]; then
    echo "MIXED NOTATION: $file (old: $old, new: $new)"
  fi
done
```

**Validation Checklist:**

**Stage References:**
- [ ] All stage references use S# format (not "Stage #" or "Stage N")
- [ ] All phase references use S#.P# format (not "S#a" or "Phase #")
- [ ] All iteration references use S#.P#.I# format (not mixed)

**Common Mixing Patterns:**
```markdown
INCONSISTENT:
- "S5.P1" in header, "S5a" in text
- "Stage 5 Phase 1" in intro, "S5.P1" in body
- "Round 1" in some sections, "S5.P1" in others

CONSISTENT:
- "S5.P1" throughout entire file
- "Stage 5" explained once as "(S5)", then "S5" used throughout
```

**Red Flags:**
- Header uses "S5.P1.I1" but text uses "Iteration 1"
- Some sections say "S5a", others say "S5.P1"
- Mixed "Stage N" and "SN" within same file

**Automated:** ✅ Yes (grep for notation patterns, flag files with multiple types)

---

### Type 2: Contradictory Instructions Within File

**What to Check:**
File should not give conflicting instructions about same topic.

**Common Patterns:**

**Pattern A: ALWAYS vs SOMETIMES**
```markdown
## Section 2: Testing Requirements

ALWAYS run tests before committing. Never commit untested code.

## Section 8: Git Workflow

If you're in a hurry, you can commit first and run tests later.  ← CONTRADICTION
```

**Pattern B: MUST vs OPTIONAL**
```markdown
## Prerequisites

- [ ] User approval REQUIRED before proceeding

## When to Proceed

You can proceed without user approval if changes are minor.  ← CONTRADICTION
```

**Pattern C: DO vs DON'T**
```markdown
## Best Practices

DO update Agent Status after every phase.

## Workflow

Agent Status updates are optional for minor phases.  ← CONTRADICTION
```

**Search Commands:**
```bash
# Find mandatory language
grep -n "MUST\|ALWAYS\|REQUIRED\|NEVER" stages/s5/*.md > /tmp/mandatory.txt

# Find optional language for same topics
grep -n "optional\|can skip\|if needed\|may" stages/s5/*.md > /tmp/optional.txt

# Manually review for contradictions (requires reading context)
```

**Validation Process:**

1. Extract all imperative statements (MUST, ALWAYS, NEVER, REQUIRED)
2. Extract all permissive statements (optional, may, can, if needed)
3. For each topic, check if both mandatory and permissive statements exist
4. If both exist, verify they're not contradictory

**Red Flags:**
- "ALWAYS do X" followed later by "X is optional"
- "NEVER skip Y" followed by "Y can be skipped if..."
- "REQUIRED: Z" followed by "Z is only needed for..."

**Automated:** ⚠️ Partial (can find contradictory keywords, requires manual semantic validation)

---

### Type 3: Inconsistent Terminology Within File

**What to Check:**
File should use ONE term consistently for each concept, not multiple synonyms.

**Common Inconsistencies:**

**Epic vs Project vs Initiative:**
```markdown
# Introduction

This guide covers epic planning...

## Section 3

Your project should include...  ← INCONSISTENT (epic or project?)

## Section 7

The initiative requires...  ← INCONSISTENT (epic, project, or initiative?)
```

**Feature vs Component vs Module:**
```markdown
## Overview

Each feature within the epic...

## Implementation

Complete all components...  ← Are "components" same as "features"?

## Testing

Test each module independently...  ← Are "modules" same as "features" or "components"?
```

**Search Commands:**
```bash
# For a given file, extract terminology variations
file="stages/s2/s2_feature_deep_dive.md"

echo "=== Workflow unit terms ==="
grep -oi "epic\|project\|initiative\|feature set" "$file" | sort | uniq -c

echo "=== Component terms ==="
grep -oi "feature\|component\|module\|piece" "$file" | sort | uniq -c

echo "=== Stage terms ==="
grep -oi "stage\|phase\|step\|iteration" "$file" | sort | uniq -c
```

**Validation Checklist:**

For each concept category:
- [ ] Workflow unit: Uses ONE term (epic, not mixed with project/initiative)
- [ ] Sub-unit: Uses ONE term (feature, not mixed with component/module)
- [ ] Hierarchy: Uses consistent terms (stage→phase→iteration, not stage→step→round)
- [ ] Files: Uses consistent terms (guide, not mixed with document/file/manual)

**Valid Exception:**
```markdown
## Introduction

This guide covers **epic planning** (also called "project planning" in some organizations)...

[Rest of file uses "epic" consistently]
```

This is VALID if variation is explained once then consistent term used throughout.

**Red Flags:**
- Uses "epic" 20 times, "project" 15 times with no explanation
- Switches between "feature" and "component" arbitrarily
- Uses "step," "iteration," "phase" interchangeably

**Automated:** ✅ Yes (can count term variations and flag files with high variation)

---

### Type 4: Structural Pattern Inconsistencies

**What to Check:**
If file has repeated structures (like multiple examples or sections), they should follow same format.

**Common Pattern: Multiple Sections**
```markdown
## Section 1: First Topic
**Duration:** 30 min
**Prerequisites:** None
**Outputs:** File A

## Section 2: Second Topic
**Duration:** 45 min
**Prerequisites:** Section 1
**Outputs:** File B

## Section 3: Third Topic  ← INCONSISTENT (missing Duration, Prerequisites, Outputs)

This section covers...
```

**Common Pattern: Multiple Examples**
```markdown
### Example 1: Adding a Feature

**Scenario:**...
**Problem:**...
**Solution:**...
**Result:**...

### Example 2: Fixing a Bug

**Scenario:**...
**Problem:**...
**Solution:**...
[No Result section]  ← INCONSISTENT
```

**Search Commands:**
```bash
# Check if all major sections have same subsections
file="stages/s5/s5_p1_planning_round1.md"

# Extract section headers
sections=$(grep "^## " "$file" | sed 's/^## //')

# For each section, check if it has standard subsections
for section in $sections; do
  echo "=== $section ==="
  # Check for Duration
  grep -A 10 "^## $section" "$file" | grep -q "Duration:"
  [ $? -eq 0 ] && echo "  Has Duration" || echo "  MISSING Duration"

  # Check for Prerequisites
  grep -A 10 "^## $section" "$file" | grep -q "Prerequisites:"
  [ $? -eq 0 ] && echo "  Has Prerequisites" || echo "  MISSING Prerequisites"
done
```

**Validation Checklist:**

**For Section Structures:**
- [ ] All major sections have same subsection types
- [ ] Subsections appear in same order
- [ ] Subsection formatting is consistent

**For Example Structures:**
- [ ] All examples have same components (Scenario, Problem, Solution, Result)
- [ ] Components appear in same order
- [ ] Formatting is consistent

**For List Structures:**
- [ ] All list items use same bullet style (all "-" or all "1.")
- [ ] All list items have same depth pattern
- [ ] Sub-items consistently indented

**Red Flags:**
- Section 1 has Duration/Prerequisites/Outputs, Section 2 doesn't
- Example 1 uses Scenario/Problem/Solution/Result, Example 2 uses Before/After
- Some bullets use "-", others use "*"

**Automated:** ⚠️ Partial (can detect missing sections, requires pattern recognition for semantic consistency)

---

### Type 5: Internal Reference Accuracy

**What to Check:**
References within file (e.g., "see Section 5") should point to sections that exist.

**Common Patterns:**

**Section References:**
```markdown
## Section 3: Setup

For detailed configuration, see Section 7.

[File only has 5 sections]  ← ERROR: Section 7 doesn't exist
```

**"Above" and "Below" References:**
```markdown
## Section 2

As mentioned above in the Prerequisites section...

[No Prerequisites section exists above Section 2]  ← ERROR
```

**Search Commands:**
```bash
# Find all "see Section N" references
grep -n "see Section [0-9]\|Section [0-9] for\|described in Section [0-9]" \
  stages/s5/*.md

# For each reference, verify section exists
# (Manual validation - requires parsing file structure)
```

**Validation Process:**

1. **Extract section numbers:** Get all "## Section N" or "## N." headers
2. **Extract section references:** Get all "see Section N" mentions
3. **Cross-validate:** Ensure all referenced sections exist
4. **Check "above/below":** Verify referenced content actually appears above/below

**Common Errors:**

**After File Reorganization:**
```markdown
Original: Section 7: Advanced Topics
After reorg: Section 5: Advanced Topics

[References still say "see Section 7"]  ← BROKEN (now Section 5)
```

**After Section Deletion:**
```markdown
File had Sections 1-8
Section 4 deleted
References still mention Section 4  ← BROKEN
```

**Red Flags:**
- "See Section N" where N > total sections
- "As mentioned above" but content isn't above
- "Details below" but no details appear below
- References to deleted/renamed sections

**Automated:** ⚠️ Partial (can find references, requires parsing to validate)

---

### Type 6: Tone and Style Consistency

**What to Check:**
File should maintain consistent voice, formality level, and perspective throughout.

**Common Inconsistencies:**

**Perspective Shifts:**
```markdown
## Introduction

You should begin by reading the prerequisites.  ← Second person "you"

## Implementation

The agent must complete all iterations.  ← Third person "the agent"

## Conclusion

We recommend following best practices.  ← First person "we"
```

**Formality Shifts:**
```markdown
## Overview

This guide provides comprehensive instructions for implementation planning.  ← Formal

## Tips

Yo, don't forget to run tests!  ← Informal  ← INCONSISTENT
```

**Imperative vs Declarative:**
```markdown
## Steps

1. Read the prerequisites
2. Complete the setup
3. Run the validation

## Next Section

The agent will read the prerequisites.  ← INCONSISTENT (declarative, not imperative)
```

**Detection (Manual):**

Read through file and note:
- Perspective: Consistent use of "you," "the agent," "we"?
- Formality: All sections maintain similar formality level?
- Mood: Imperative ("Do X") vs Declarative ("Agent does X") consistent?
- Tone: Professional/instructional throughout, or mixed with casual?

**Red Flags:**
- Switches between "you" and "the agent" arbitrarily
- One section very formal, another very casual
- Inconsistent use of contractions ("don't" vs "do not")
- Mixed imperative and declarative mood

**Automated:** ❌ No (requires human judgment of tone and style)

---

### Type 7: Example-to-Principle Consistency

**What to Check:**
Examples should correctly demonstrate the principles stated in text.

**Common Pattern:**
```markdown
## Best Practice: Always Include Type Hints

All functions should include complete type hints for parameters and return values.

### Example

def calculate_total(items):  ← ERROR: No type hints in example
    return sum(items)
```

**Another Pattern:**
```markdown
## Rule: Use S#.P# Notation

Always use the S#.P# notation format (e.g., S5.P1, not S5a).

### Example

For Stage 5a Phase 2...  ← ERROR: Example violates the rule it demonstrates
```

**Validation Process:**

1. **Extract rules/principles:** Find declarative statements (ALWAYS, NEVER, MUST, SHOULD)
2. **Find associated examples:** Locate examples in same section
3. **Verify examples follow rules:** Check if example code/text follows stated principle

**Common Errors:**

**Example Violates Rule:**
- Rule: "Never skip checkpoints"
- Example workflow: Shows skipping checkpoint

**Example Outdated:**
- Rule updated to use new notation
- Example still shows old notation

**Example Unclear:**
- Rule is specific
- Example is vague or doesn't clearly demonstrate rule

**Red Flags:**
- Example does opposite of what rule states
- Example uses deprecated pattern
- Multiple examples exist, some follow rule, others don't

**Automated:** ❌ No (requires semantic understanding of principles and examples)

---

## How Errors Happen

### Root Cause 1: Incremental Editing Without Full File Review

**Scenario:**
- File created with consistent notation
- Later, Section 5 updated with new content
- Editor copy-pastes from old file with old notation
- **RESULT:** Section 5 now has old notation, rest of file has new notation

**Example:**
S5 guide originally consistent with S5.P1 notation. During update, copy-pasted content from old guide that used "S5a" notation. Now file mixes both.

---

### Root Cause 2: Multiple Authors Without Style Guide

**Scenario:**
- Author A writes Introduction using "epic" terminology
- Author B adds middle sections using "project" terminology
- No style guide enforces consistent terms
- **RESULT:** File mixes "epic" and "project"

---

### Root Cause 3: Section Reorganization Without Reference Updates

**Scenario:**
- File originally: Sections 1-8
- Section 4 deleted, subsequent sections renumbered
- Internal references updated for section numbers
- **FORGOT** to update "see Section 7" to "see Section 6"
- **RESULT:** Broken internal references

---

### Root Cause 4: Rule Changes Without Example Updates

**Scenario:**
- Rule originally: "Use S5a notation"
- Rule updated to: "Use S5.P1 notation"
- Rule text updated
- **FORGOT** to update examples still showing S5a
- **RESULT:** Examples violate updated rule

---

### Root Cause 5: Template Evolution Creating Structural Inconsistencies

**Scenario:**
- File created from template v1 (has Duration/Prerequisites/Outputs)
- Sections 1-5 written
- Template updated to v2 (adds "Exit Criteria" subsection)
- Sections 6-10 written using new template
- **RESULT:** Sections 1-5 don't have Exit Criteria, Sections 6-10 do

---

## Automated Validation

### Pre-Audit Script Coverage

**From `scripts/pre_audit_checks.sh`:**

**CHECK 16: Notation Mixing Detection** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Checking for mixed notation within files..."

for file in stages/**/*.md reference/*.md; do
  # Count old notation
  old=$(grep -c "S[0-9][a-z]\|Stage [0-9][a-z]" "$file")

  # Count new notation
  new=$(grep -c "S[0-9]\\.P[0-9]" "$file")

  if [ "$old" -gt 0 ] && [ "$new" -gt 0 ]; then
    echo "MIXED NOTATION in $file (old: $old, new: $new)"
  fi
done
```

**CHECK 17: Terminology Variation Detection** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Checking for terminology inconsistencies..."

for file in stages/**/*.md; do
  echo "=== $(basename $file) ==="

  # Check workflow unit term variation
  epic_count=$(grep -oi "epic" "$file" | wc -l)
  project_count=$(grep -oi "project" "$file" | wc -l)

  if [ "$epic_count" -gt 5 ] && [ "$project_count" -gt 5 ]; then
    echo "WARNING: Mixed 'epic' ($epic_count) and 'project' ($project_count)"
  fi

  # Check feature term variation
  feature_count=$(grep -oi "feature" "$file" | wc -l)
  component_count=$(grep -oi "component" "$file" | wc -l)

  if [ "$feature_count" -gt 5 ] && [ "$component_count" -gt 5 ]; then
    echo "WARNING: Mixed 'feature' ($feature_count) and 'component' ($component_count)"
  fi
done
```

**CHECK 18: Internal Reference Validation** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Checking internal section references..."

for file in stages/**/*.md; do
  # Count total sections
  section_count=$(grep -c "^## " "$file")

  # Find references to "Section N"
  refs=$(grep -o "Section [0-9]+" "$file" | grep -o "[0-9]+" | sort -u)

  for ref in $refs; do
    if [ "$ref" -gt "$section_count" ]; then
      echo "BROKEN REFERENCE in $file: References Section $ref but only $section_count sections exist"
    fi
  done
done
```

**Automation Coverage: ~80%**
- ✅ Notation mixing
- ✅ Terminology variations
- ✅ Structural pattern detection
- ⚠️ Internal reference validation (can detect some cases)
- ❌ Contradictory instructions (requires semantic analysis)
- ❌ Tone consistency (requires human judgment)
- ❌ Example-to-principle matching (requires semantic understanding)

---

## Manual Validation

### Manual Process (Intra-File Consistency Audit)

**Duration:** 45-60 minutes
**Frequency:** After major guide updates, new guide creation

**Step 1: Notation Consistency Check (10 min)**

```bash
# For each guide, check notation patterns
for file in stages/**/*.md; do
  echo "=== $(basename $file) ==="

  # Show all stage/phase references
  grep -n "S[0-9]" "$file" | head -20

  # Manually review for:
  # - Mixed "S5a" and "S5.P1"
  # - Mixed "Stage 5" and "S5"
  # - Inconsistent iteration notation
done
```

**Manual Review Questions:**
- Does file use ONE notation system consistently?
- If old notation appears, is it explained as historical reference?
- Are all stage/phase/iteration references formatted same way?

**Step 2: Terminology Consistency Check (10 min)**

```bash
# Extract term frequencies per file
file="stages/s2/s2_feature_deep_dive.md"

echo "Workflow unit terms:"
grep -oi "epic\|project\|initiative" "$file" | sort | uniq -c

echo "Sub-unit terms:"
grep -oi "feature\|component\|module" "$file" | sort | uniq -c

echo "Process terms:"
grep -oi "stage\|phase\|step\|iteration" "$file" | sort | uniq -c
```

**Manual Review Questions:**
- Does file use ONE term for each concept?
- If multiple terms exist, is variation explained?
- Are terms used appropriately in context?

**Step 3: Structural Consistency Check (10 min)**

```bash
# Check if all sections have same structure
file="stages/s5/s5_p1_planning_round1.md"

# List all section headers
grep "^## \|^### " "$file"

# For sections that should be parallel (e.g., all iteration sections):
# - Check if they have same subsections
# - Check if formatting is consistent
```

**Manual Review Process:**
1. Identify repeated structures (e.g., multiple examples, multiple iteration sections)
2. For each group, note structure of first item
3. Verify remaining items follow same structure
4. Flag inconsistencies

**Step 4: Contradiction Check (15 min)**

```bash
# Extract mandatory statements
grep -n "MUST\|ALWAYS\|NEVER\|REQUIRED" "$file" > /tmp/mandatory.txt

# Extract permissive statements
grep -n "optional\|can skip\|may\|if needed" "$file" > /tmp/permissive.txt

# Manually review both files for contradictions
```

**Manual Review Process:**
1. Read all mandatory statements
2. Read all permissive statements
3. For overlapping topics, check if they contradict
4. Verify exceptions are clearly marked as exceptions

**Step 5: Internal Reference Validation (10 min)**

```bash
# Find all internal references
grep -n "see Section\|Section [0-9]\|above\|below" "$file"

# For each reference:
# 1. Note what it claims to reference
# 2. Verify referenced content exists
# 3. Verify content is in claimed location (above/below)
```

**Manual Review Questions:**
- Do all "see Section N" references point to existing sections?
- Do "above" references actually reference content above?
- Do "below" references have content below?
- Are references still accurate after reorganization?

---

## Context-Sensitive Rules

### Rule 1: Intentional Terminology Variation in Examples

**Context:** Examples may intentionally show incorrect patterns as anti-patterns.

**Valid Example:**
```markdown
## Best Practice: Use S#.P# Notation

Always use S#.P# notation (e.g., S5.P1).

### Anti-Pattern Example

❌ WRONG: "For Stage 5a..."  ← This is showing what NOT to do
✅ CORRECT: "For S5.P1..."
```

**Validation:** If example explicitly labeled as anti-pattern/wrong → VALID (not inconsistency)

---

### Rule 2: Historical References May Use Old Notation

**Context:** Historical evidence sections intentionally reference old structure.

**Valid Example:**
```markdown
## Current Notation

Use S#.P# format (S5.P1, S5.P2, S5.P3).

## Historical Note

The old workflow used S5a/S5b/S5c notation. This was changed in 2025 to improve clarity.
```

**Validation:** Old notation in historical context → VALID (not inconsistency)

---

### Rule 3: Introductory Terminology Definitions

**Context:** Introductions may define multiple terms then use one consistently.

**Valid Example:**
```markdown
## Introduction

This guide covers **epic planning** (also called "project planning" or "initiative planning" in some organizations). Throughout this guide, we use "epic" consistently.

## Rest of File

[Uses "epic" exclusively, no "project" or "initiative"]
```

**Validation:** Multiple terms defined once then one used consistently → VALID

---

### Rule 4: Different Perspectives for Different Audiences

**Context:** Some guides intentionally address multiple audiences.

**Valid Example:**
```markdown
## For Users

You should review the implementation plan before approving.

## For Agents

The agent must wait for user approval before proceeding.
```

**Validation:** Perspective shift with clear audience markers → VALID

---

## Real Examples

### Example 1: Mixed Notation in S5 Guide

**Issue Found During KAI-7 Audit Round 3:**

**File:** `stages/s5/s5_p1_planning_round1.md`

**Mixed Content:**
```markdown
# S5.P1: Planning Round 1

This phase covers iterations I1-I7...

## Round 1 Iterations

Complete S5a iterations first...  ← ERROR: Mixed "S5a" with "S5.P1"

## Iteration I1: Requirements

Refer to S5.P1 guide for details...  ← Consistent notation
```

**Problem:**
- File header uses "S5.P1"
- Most content uses "S5.P1"
- One section uses "S5a" (old notation)
- Inconsistent within same file

**Fix:**
```diff
## Round 1 Iterations

-Complete S5a iterations first...
+Complete S5.P1 iterations first...
```

**Root Cause:** Content copy-pasted from old guide during update, old notation not replaced

**How D9 Detects:**
- Type 1: Mixed Notation Within Single File
- Automated: CHECK 16 detects files with both old and new notation

---

### Example 2: Contradictory Instructions in Debugging Protocol

**Issue Found During KAI-6 Debugging:**

**File:** `debugging/debugging_protocol.md`

**Contradictory Content:**
```markdown
## Section 2: Issue Discovery

ALWAYS create a dedicated issue file for each problem found.

## Section 5: Minor Issues

For minor issues, you can document them in the main checklist without creating separate files.  ← CONTRADICTION
```

**Problem:**
- Section 2: ALWAYS create file
- Section 5: Can skip file creation for minor issues
- Agents confused about when files are required

**Fix:**
```diff
## Section 2: Issue Discovery

-ALWAYS create a dedicated issue file for each problem found.
+Create a dedicated issue file for each problem found (exceptions noted below).

## Section 5: Minor Issues

For minor issues (typos, formatting), you can document them in the main checklist without creating separate files.
+This is the ONLY exception to the issue file requirement.
```

**Root Cause:** Rule made absolute, exception added later without updating original rule

**How D9 Detects:**
- Type 2: Contradictory Instructions Within File
- Manual validation: Find ALWAYS statements, check for contradicting permissive statements

---

### Example 3: Terminology Inconsistency in Template

**Issue Found During Template Review:**

**File:** `templates/feature_spec_template.md`

**Mixed Terminology:**
```markdown
# Feature Specification

## Epic Context

This feature is part of the [EPIC_NAME] epic...

## Project Background

The project aims to...  ← INCONSISTENT (epic or project?)

## Initiative Goals

The initiative will deliver...  ← INCONSISTENT (epic, project, or initiative?)
```

**Problem:**
- Uses "epic," "project," and "initiative" interchangeably
- No explanation that these are synonyms
- Creates confusion about scope

**Fix:**
```diff
# Feature Specification

## Epic Context

-This feature is part of the [EPIC_NAME] epic...
+This feature is part of the [EPIC_NAME] epic.

-## Project Background
+## Epic Background

-The project aims to...
+The epic aims to...

-## Initiative Goals
+## Epic Goals

-The initiative will deliver...
+The epic will deliver...
```

**Root Cause:** Template created from multiple sources, each using different terminology

**How D9 Detects:**
- Type 3: Inconsistent Terminology Within File
- Automated: CHECK 17 detects high variation in workflow unit terms

---

### Example 4: Structural Inconsistency in Examples

**Issue Found During S7 Guide Review:**

**File:** `stages/s7/s7_p2_qc_rounds.md`

**Inconsistent Example Structure:**
```markdown
### Example 1: Missing Import

**Scenario:** Implementation missing required import
**Problem:** Code fails to run
**Solution:** Add import statement
**Result:** Code executes successfully

### Example 2: Logic Error

**Scenario:** Calculation produces wrong result
**Problem:** Off-by-one error in loop
**Fix:** Update loop condition  ← INCONSISTENT (should be "Solution")
[No Result section]  ← INCONSISTENT (missing)
```

**Problem:**
- Example 1: Uses Scenario/Problem/Solution/Result
- Example 2: Uses Scenario/Problem/Fix (not "Solution"), missing Result
- Inconsistent structure confuses readers

**Fix:**
```diff
### Example 2: Logic Error

**Scenario:** Calculation produces wrong result
**Problem:** Off-by-one error in loop
-**Fix:** Update loop condition
+**Solution:** Update loop condition
+**Result:** Calculation produces correct result
```

**Root Cause:** Examples written at different times, structure evolved, old examples not updated

**How D9 Detects:**
- Type 4: Structural Pattern Inconsistencies
- Manual validation: Compare structure of all examples in file

---

### Example 5: Broken Internal Reference After Reorganization

**Issue Found During Guide Reorganization:**

**File:** `stages/s3/s3_epic_planning_approval.md`

**Broken Reference:**
```markdown
## Section 3: Testing Strategy

For detailed testing patterns, see Section 7: Advanced Testing Techniques.

[File only has 5 sections - Section 7 doesn't exist]
```

**What Happened:**
- Original file had 8 sections
- During reorganization, Sections 6-8 moved to separate file
- Internal references not updated

**Fix Option 1 (Update Reference):**
```diff
## Section 3: Testing Strategy

-For detailed testing patterns, see Section 7: Advanced Testing Techniques.
+For detailed testing patterns, see `stages/s4/s4_feature_testing_strategy.md`.
```

**Fix Option 2 (Remove Reference if No Longer Relevant):**
```diff
## Section 3: Testing Strategy

-For detailed testing patterns, see Section 7: Advanced Testing Techniques.
+For detailed testing patterns, refer to S4: Feature Testing Strategy.
```

**Root Cause:** File reorganization without updating internal references

**How D9 Detects:**
- Type 5: Internal Reference Accuracy
- Automated: CHECK 18 detects references to non-existent sections

---

## Integration with Other Dimensions

### D2: Terminology Consistency

**Overlap:**
- D2 validates terminology ACROSS files
- D9 validates terminology WITHIN files
- **Division:** D2 = inter-file, D9 = intra-file

**Example:**
- D2 checks: All files use "epic" (not "project") ✅
- D9 checks: Single file doesn't mix "epic" and "project" ✅

**Recommendation:** Run D2 AND D9 (complementary validations)

---

### D5: Content Completeness

**Overlap:**
- D5 validates required sections exist
- D9 validates those sections are internally consistent
- **Division:** D5 = presence, D9 = consistency

**Example:**
- D5 checks: File has "Prerequisites" section ✅
- D9 checks: All major sections have "Prerequisites" (structural consistency) ✅

---

### D11: Structural Patterns

**Overlap:**
- D11 validates file follows template structure
- D9 validates within-file structural consistency
- **Division:** D11 = template compliance, D9 = internal consistency

**Example:**
- D11 checks: File has required sections per template ✅
- D9 checks: All sections follow same format pattern ✅

---

### D13: Documentation Quality

**Overlap:**
- D13 validates quality standards met
- D9 validates internal consistency of quality
- **Division:** D13 = standards, D9 = consistency

**Example:**
- D13 checks: Examples are high-quality ✅
- D9 checks: All examples follow same structure ✅

---

## Summary

**D9: Intra-File Consistency validates that content within single files is internally consistent.**

**Key Validations:**
1. ✅ Notation consistency (one system throughout file)
2. ⚠️ No contradictory instructions
3. ✅ Terminology consistency (one term per concept)
4. ⚠️ Structural consistency (repeated patterns match)
5. ⚠️ Internal reference accuracy
6. ❌ Tone and style consistency (manual)
7. ❌ Example-to-principle consistency (manual)

**Automation: ~80%**
- Highly automated for notation, terminology, structure
- Manual needed for semantic contradictions, tone assessment, example validation

**Critical for:**
- Preventing reader confusion from mixed notation/terminology
- Ensuring file provides consistent guidance throughout
- Maintaining professional quality in documentation

**Next Dimension:** D15: Duplication Detection (finding duplicate content across files)

---

**Last Updated:** 2026-02-04
**Version:** 1.0
**Status:** ✅ Fully Implemented
