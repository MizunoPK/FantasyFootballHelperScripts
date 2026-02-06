# D7: Context-Sensitive Validation

**Dimension Number:** 7
**Category:** Advanced Dimensions
**Automation Level:** 20% automated
**Priority:** MEDIUM
**Last Updated:** 2026-02-04

**Focus:** Distinguish intentional exceptions from actual errors using context markers and historical references
**Typical Issues Found:** 20-40 false positives reduced per audit

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

**D7: Context-Sensitive Validation** distinguishes intentional exceptions from actual errors:

1. **Historical References** - Old notation in historical context vs current errors
2. **Anti-Pattern Examples** - Wrong code shown intentionally vs actual mistakes
3. **Quoted Errors** - Error messages as examples vs documentation errors
4. **Intentional Variations** - Valid workflow variations vs violations
5. **Template Placeholders** - Placeholder text vs incomplete content
6. **Explanatory Content** - Explaining deprecated patterns vs using them
7. **Context Markers** - Presence of "[OLD]", "[DEPRECATED]", "[EXAMPLE]" markers

**Coverage:**
- All audit dimension findings
- Pattern matches that may be false positives
- Automated check results requiring human judgment

**Key Purpose:**
This dimension provides **context analysis** to interpret findings from other dimensions correctly.

**Key Distinction:**
- **Other Dimensions:** Find patterns (e.g., "S5a" notation found)
- **D7:** Determine if pattern match is error or intentional (e.g., "S5a" in historical section = intentional)

---

## Why This Matters

**Without context validation = False positives waste time, false negatives miss real errors**

### Impact of Missing Context Validation:

**False Positives (Wasted Effort):**
- Automated check finds "S5a" notation
- Flags as error (old notation)
- Actually in historical section explaining old workflow
- Auditor wastes time "fixing" intentional reference
- Worse: "fix" removes valuable historical context

**False Negatives (Missed Errors):**
- Example shows incorrect code with no marker
- Auditor assumes it's intentional anti-pattern
- Actually it's a mistake in the example
- Error persists, misleads users

**Lost Valuable Content:**
- Historical sections removed thinking they're errors
- Anti-pattern examples deleted thinking they're mistakes
- Valuable educational content lost

**Inconsistent Audit Results:**
- Different auditors interpret same findings differently
- Some mark historical references as errors, others don't
- Audit results depend on auditor judgment
- Need systematic context analysis

### Historical Evidence:

**KAI-7 Issues:**
- Automated checks flagged 50+ "S5a" references
- Manual review found 30 were in historical/explanatory contexts
- 20 were actual errors
- Without context validation, would have flagged all 50

**Why 20% Automation:**
- Automated: Detect context markers ([OLD], Historical section headers)
- Manual Required: Semantic understanding of whether exception is valid

---

## Pattern Types

### Type 0: Root-Level File Context (CRITICAL - Often Missed)

**Files to Always Check:**
```text
C:\Users\kmgam\code\FantasyFootballHelperScripts\CLAUDE.md
feature-updates/guides_v2/README.md
feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md
```markdown

**What to Validate:**

**CLAUDE.md - Historical Evidence Sections:**
```markdown
## Stage Workflows Quick Reference

**Current Workflow:** S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9 → S10

**Historical Note:** The old workflow (pre-2025) had 9 stages (S1-S9). S4 was added in January 2025, requiring renumbering of subsequent stages.
```

**Validation:**
- "9 stages" would normally be flagged as count error
- BUT it's in "Historical Note" section
- → INTENTIONAL reference to old structure

**Search Commands:**
```bash
# Find potential historical references
grep -B 3 -A 3 "Historical\|Old workflow\|Previously\|Before 2025" CLAUDE.md

# Check if "errors" appear in these contexts
grep -n "S[0-9][a-z]\|9 stages\|old notation" CLAUDE.md

# For each match, check if within historical context
```markdown

**Red Flags:**
- "Old notation" appears outside historical context
- No marker indicating it's intentional reference
- Pattern appears in current workflow section (not historical)

**Automated:** ⚠️ Partial (can detect "Historical" markers, requires judgment on validity)

---

### Type 1: Historical Reference Context

**What to Check:**
Content describing old/deprecated patterns should be clearly marked as historical.

**Common Patterns:**

**Valid Historical Reference:**
```markdown
## Notation System Evolution

**Current Notation:** S#.P#.I# (e.g., S5.P1.I1)

**Historical Note:** Prior to 2025, the workflow used S#a/b/c notation (e.g., S5a, S5b, S5c). This was changed to improve clarity.

**Example of Old Notation:**
- S5a = First phase of Stage 5 (now S5.P1)
- S5b = Second phase (now S5.P2)
```

**Validation:**
- ✅ Clearly labeled as "Historical Note"
- ✅ Explains old vs new
- ✅ Uses "Prior to," "was changed" (past tense)
- ✅ Provides mapping to current notation

**Invalid Historical Reference:**
```markdown
## Workflow

Complete S5a Phase 1 iterations...

[No marker indicating this is historical reference]
```bash

**Detection:**
```bash
# Find old notation patterns
grep -n "S[0-9][a-z]\|Stage [0-9][a-z]" feature-updates/guides_v2/stages/**/*.md

# For each match, check surrounding context
for match in $(grep -l "S[0-9][a-z]" stages/**/*.md); do
  echo "=== $match ==="
  # Check if in historical context
  grep -B 5 -A 5 "S[0-9][a-z]" "$match" | \
    grep -q "Historical\|Old\|Previous\|Before"

  if [ $? -eq 0 ]; then
    echo "  CONTEXT: Historical reference (likely intentional)"
  else
    echo "  CONTEXT: Current content (likely ERROR)"
  fi
done
```

**Context Markers Indicating Valid Historical Reference:**
- "Historical Note:"
- "Old workflow:"
- "Previously:"
- "Before [year]:"
- "Deprecated:"
- "Was changed to:"
- Past tense verbs ("used," "was," "had")

**Red Flags (Likely Errors):**
- Old notation with no context markers
- Present tense usage ("S5a is...")
- Appears in current workflow instructions

**Automated:** ⚠️ Partial (can detect markers, requires judgment on sufficiency)

---

### Type 2: Anti-Pattern Example Context

**What to Check:**
Examples showing incorrect patterns should be clearly marked as "wrong."

**Common Patterns:**

**Valid Anti-Pattern Example:**
```markdown
## Best Practice: Use S#.P# Notation

Always use S#.P# notation for clarity.

### Example: Correct Notation

✅ **CORRECT:**
```markdown
See S5.P1 for implementation planning.
```markdown

### Example: Incorrect Notation

❌ **WRONG:**
```
See S5a for implementation planning.
```text

**DO NOT use S5a notation. Use S5.P1 instead.**
```markdown

**Validation:**
- ✅ Clearly marked with ❌ or "WRONG" or "Incorrect"
- ✅ Followed by correct version
- ✅ Explicit instruction not to use pattern

**Invalid Example (Ambiguous):**
```markdown
## Examples

### Example 1

```
See S5a for implementation planning.
```json
[No indication if this is right or wrong]
```bash

**Detection:**
```bash
# Find examples that might show wrong patterns
grep -B 5 -A 5 "Example" stages/**/*.md | grep "S[0-9][a-z]"

# For each match, check for markers
markers="❌\|WRONG\|Incorrect\|Don't\|Avoid\|Anti-pattern"

# If markers present, likely intentional anti-pattern
# If no markers, likely error
```

**Context Markers Indicating Valid Anti-Pattern:**
- ❌ symbol
- ✅ symbol (for correct version)
- "WRONG:"
- "INCORRECT:"
- "DON'T DO THIS:"
- "Anti-pattern:"
- "Common Mistake:"
- Followed by "CORRECT:" version

**Red Flags (Likely Errors):**
- Example shows wrong pattern with no markers
- No correct version provided
- Unclear if pattern is endorsed or cautioned against

**Automated:** ✅ Yes (can detect ❌/✅ markers, "WRONG", "CORRECT")

---

### Type 3: Quoted Error Message Context

**What to Check:**
Error messages shown as examples should be clearly quoted/formatted as examples.

**Common Patterns:**

**Valid Quoted Error:**
```markdown
## Debugging Common Errors

### Missing Import Error

If you see this error:
```yaml
ModuleNotFoundError: No module named 'pandas'
```python

The solution is to add: `import pandas as pd`
```

**Validation:**
- ✅ Error in code block (```...```)
- ✅ Prefaced with "If you see this error:"
- ✅ Context makes clear it's example of error message

**Invalid (Ambiguous):**
```markdown
## Implementation

ModuleNotFoundError: No module named 'pandas'

[Unclear if this is error in documentation or example]
```bash

**Detection:**
```bash
# Find error-like content
grep -n "Error\|Exception\|Failed\|Warning" stages/**/*.md

# Check if in code blocks or quoted
# Code blocks: ``` ... ```bash
# Quotes: "...", '...'

# If in code block or quote, likely example
# If in prose, may be documentation error
```

**Context Markers Indicating Valid Error Example:**
- Code block formatting (```...```)
- "If you see this error:"
- "Example error:"
- "Common error message:"
- "You may encounter:"
- Quotation marks around error

**Red Flags (Likely Actual Errors):**
- Error message in prose, not code block
- No context indicating it's example
- Present tense ("this error occurs")

**Automated:** ✅ Yes (can detect code blocks, quotes, context phrases)

---

### Type 4: Intentional Workflow Variation Context

**What to Check:**
Valid workflow variations should be documented as intentional exceptions.

**Common Patterns:**

**Valid Workflow Variation:**
```markdown
## Standard Workflow

S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9 → S10

## Workflow Variations

### Bug Fix Workflow (Exception)

For urgent hotfixes, you may proceed directly:
S1 → Debugging Protocol → S10

**This is the ONLY approved variation from standard workflow.**
```markdown

**Validation:**
- ✅ Labeled as "Exception" or "Variation"
- ✅ Explicitly approved
- ✅ Clear conditions when variation applies

**Invalid Variation (Likely Error):**
```markdown
## Workflow

For this feature, we skipped S4 and went to S5.

[No indication if this is approved or mistake]
```

**Detection:**
```bash
# Find potential workflow variations
grep -n "skip\|omit\|bypass\|directly to" stages/**/*.md

# Check for approval markers
grep -B 3 -A 3 "skip\|omit" stages/**/*.md | \
  grep -q "Exception\|Variation\|Approved\|ONLY"

# If markers present, likely intentional
# If no markers, likely error
```markdown

**Context Markers Indicating Valid Variation:**
- "Exception:"
- "Variation:"
- "Approved workflow:"
- "ONLY approved..."
- "Special case:"
- "For [specific condition]:"
- Explicit permission language

**Red Flags (Likely Errors):**
- Deviation with no justification
- No explicit approval
- Unclear if exception or mistake

**Automated:** ⚠️ Partial (can detect variation keywords, requires judgment on validity)

---

### Type 5: Template Placeholder Context

**What to Check:**
Placeholder text in templates should be clearly marked for replacement.

**Common Patterns:**

**Valid Template Placeholder:**
```markdown
# Feature Specification Template

## Feature Name

**[USER: Replace with actual feature name]**

## Background

[USER: Provide context from DISCOVERY.md Section 2]

## Requirements

**[AGENT: List requirements based on spec.md]**
```

**Validation:**
- ✅ Square brackets with markers: [USER:], [AGENT:]
- ✅ Clear instruction to replace
- ✅ Distinguishable from actual content

**Invalid Placeholder (Ambiguous):**
```markdown
## Feature Name

Replace with actual feature name

[Unclear if this is instruction or incomplete content]
```bash

**Detection:**
```bash
# Find template placeholders
grep -n "\[USER:\|\[AGENT:\|\[TODO:\|\[REPLACE:" templates/**/*.md

# Valid placeholders have clear markers
# Invalid: Plain text that looks like instruction
```

**Context Markers Indicating Valid Placeholder:**
- [USER: ...]
- [AGENT: ...]
- [TODO: ...]
- [REPLACE: ...]
- **[Placeholder]**
- ALL CAPS: FEATURE_NAME (convention)

**Red Flags (Likely Incomplete Content):**
- Instruction-like text without markers
- Vague content with no clear directive
- Looks like actual content but generic

**Automated:** ✅ Yes (can detect [USER:], [AGENT:] markers)

---

### Type 6: Explanatory Deprecated Pattern Context

**What to Check:**
Content explaining deprecated patterns should frame them as "no longer used."

**Common Patterns:**

**Valid Explanation of Deprecated Pattern:**
```markdown
## Debugging Protocol Evolution

### Old Approach (Deprecated - No Longer Used)

Previously, debugging issues were logged in a single ISSUES.md file. This caused confusion when multiple issues were investigated simultaneously.

### Current Approach

Each issue now gets a dedicated file: `issue_01_description.md`. This provides clear separation and tracking.
```diff

**Validation:**
- ✅ Labeled "Deprecated" or "No Longer Used"
- ✅ Past tense ("Previously," "were logged")
- ✅ Explains why changed
- ✅ Shows current approach

**Invalid (Ambiguous):**
```markdown
## Debugging

Issues are logged in ISSUES.md.

[Unclear if current or deprecated]
```

**Detection:**
```bash
# Find deprecated content
grep -n "Deprecated\|No longer\|Obsolete\|Legacy" stages/**/*.md

# Check if explanation includes:
# - Why deprecated
# - What replaced it
# - Past tense usage
```diff

**Context Markers Indicating Valid Deprecation Explanation:**
- "Deprecated:"
- "No longer used:"
- "Obsolete:"
- "Legacy approach:"
- "Previously, ... Now, ..."
- "Old approach" vs "Current approach" sections
- Past tense throughout

**Red Flags (Likely Using Deprecated Pattern):**
- Present tense ("Issues are logged...")
- No indication pattern is deprecated
- No current alternative provided

**Automated:** ✅ Yes (can detect "Deprecated", "No longer used" markers)

---

### Type 7: Explicit Context Marker Detection

**What to Check:**
Files should use explicit markers to indicate intentional exceptions.

**Recommended Markers:**

**For Historical References:**
```markdown
[HISTORICAL] Old workflow used S#a notation
```

**For Examples of Wrong Patterns:**
```markdown
❌ **WRONG EXAMPLE:** Don't do this...
✅ **CORRECT EXAMPLE:** Do this instead...
```markdown

**For Deprecated Content:**
```markdown
[DEPRECATED 2025-01-15] This approach no longer recommended.
```

**For Intentional Variations:**
```markdown
[APPROVED EXCEPTION] Bug fix workflow may skip S4.
```markdown

**For Placeholders:**
```markdown
[USER: Replace this with actual content]
```

**Detection:**
```bash
# Count explicit markers in guides
grep -rc "\[HISTORICAL\]\|\[DEPRECATED\]\|\[APPROVED\]\|❌\|✅" \
  stages/**/*.md

# Files with high marker counts: Good explicit context
# Files with low/zero markers: May have ambiguous content
```diff

**Benefits:**
- Unambiguous intent
- Machine-readable (automation can filter)
- Consistent across all guides

**Recommendation:** Add explicit markers during guide creation/updates.

---

## How Errors Happen

### Root Cause 1: Historical Content Added Without Markers

**Scenario:**
- Guide updated to explain why notation changed
- Adds section: "Old workflow used S5a notation"
- **FORGOT** to add "Historical:" marker
- Automated check flags "S5a" as error

**Better Approach:**
- Add marker: "[HISTORICAL] Old workflow used S5a notation"
- OR: Header: "## Historical Note: Notation Evolution"

---

### Root Cause 2: Example Shows Wrong Pattern Without Clear Marking

**Scenario:**
- Guide includes example of common mistake
- Shows incorrect code
- **FORGOT** to add ❌ marker or "WRONG:" label
- Auditor thinks example has error

**Better Approach:**
- Mark clearly: "❌ **WRONG EXAMPLE:**"
- Follow with: "✅ **CORRECT EXAMPLE:**"

---

### Root Cause 3: Deprecated Pattern Explained in Present Tense

**Scenario:**
- Content explains old approach
- Uses present tense: "Issues are logged in ISSUES.md"
- **Unclear** if this is current or deprecated
- Auditor doesn't know if it needs updating

**Better Approach:**
- Use past tense: "Issues WERE logged in ISSUES.md"
- Add marker: "[DEPRECATED] Issues were logged..."

---

### Root Cause 4: Workflow Variation Not Explicitly Approved

**Scenario:**
- Feature required skipping S4
- Guide mentions skipping without justification
- **UNCLEAR** if approved exception or error
- Auditor flags as workflow violation

**Better Approach:**
- Document: "[APPROVED EXCEPTION] S4 skipped for reason X"
- OR: Add to workflow_variations.md reference

---

### Root Cause 5: Template Placeholder Looks Like Content

**Scenario:**
- Template says: "Provide feature background here"
- Looks like instruction or incomplete content
- **UNCLEAR** if placeholder or actual incomplete guide
- Auditor flags as completeness issue

**Better Approach:**
- Use marker: "[USER: Provide feature background here]"
- OR: ALL CAPS: FEATURE_BACKGROUND

---

## Automated Validation

### Pre-Audit Script Coverage

**From `scripts/pre_audit_checks.sh`:**

**CHECK 21: Context Marker Detection** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Checking for context markers on potential errors..."

# Find old notation
old_notation_files=$(grep -rl "S[0-9][a-z]" stages/ reference/)

for file in $old_notation_files; do
  # Check for historical markers
  if grep -q "Historical\|Old workflow\|Previously\|Deprecated" "$file"; then
    echo "✓ $file: Has context markers for old notation"
  else
    echo "⚠ $file: Old notation found without historical context"
  fi
done
```

**CHECK 22: Anti-Pattern Example Validation** *(planned, not yet implemented)*
```bash
#!/bin/bash
echo "Validating anti-pattern examples have clear markers..."

# Find examples with potentially wrong patterns
grep -B 2 -A 5 "Example" stages/**/*.md | grep "S[0-9][a-z]" > /tmp/examples_with_old.txt

# Check each has markers
while read -r line; do
  # Extract filename
  file=$(echo "$line" | cut -d: -f1)

  # Check for ❌ or "WRONG" markers within 5 lines
  context=$(grep -B 2 -A 5 "Example" "$file" | head -10)

  if echo "$context" | grep -q "❌\|WRONG\|Incorrect"; then
    echo "✓ $file: Example has error markers"
  else
    echo "⚠ $file: Example may be ambiguous"
  fi
done < /tmp/examples_with_old.txt
```markdown

**Automation Coverage: ~20%**
- ✅ Detect presence of context markers
- ✅ Flag content without markers
- ❌ Determine if context is sufficient (requires human judgment)
- ❌ Evaluate semantic validity of exception
- ❌ Balance false positives vs false negatives

---

## Manual Validation

### Manual Process (Context Validation)

**Duration:** 30-45 minutes per audit dimension
**Frequency:** During audit, for each dimension's findings

**Process Overview:**

For each finding from other dimensions (D1-D6, D8-D16), apply context validation.

**Step 1: Categorize Finding (5 min per dimension)**

For each pattern match:

1. **Note the finding:** "File X contains 'S5a' notation (old notation)"
2. **Read surrounding context:** 5 lines before and after
3. **Categorize:**
   - Historical reference
   - Anti-pattern example
   - Quoted error
   - Intentional variation
   - Template placeholder
   - Deprecated pattern explanation
   - Actual error (no valid context)

**Step 2: Validate Historical References (Per Finding)**

**Questions to ask:**
- [ ] Is it in section titled "Historical" or "Old" or "Previous"?
- [ ] Does it use past tense ("was," "used to," "previously")?
- [ ] Does it explain evolution to current approach?
- [ ] Is mapping to current notation provided?

**If YES to 3+:** Likely valid historical reference (not error)
**If NO to all:** Likely actual error

**Step 3: Validate Anti-Pattern Examples (Per Finding)**

**Questions to ask:**
- [ ] Is example marked with ❌ or "WRONG" or "Incorrect"?
- [ ] Is correct version (✅) provided?
- [ ] Is explicit instruction not to use pattern?
- [ ] Is pattern clearly in example context?

**If YES to 3+:** Likely valid anti-pattern example (not error)
**If NO to all:** Likely actual error

**Step 4: Validate Quoted Errors (Per Finding)**

**Questions to ask:**
- [ ] Is error message in code block (```...```)?
- [ ] Is it prefaced with "If you see this error"?
- [ ] Is solution/explanation provided?
- [ ] Is clearly example of error, not error in documentation?

**If YES to 3+:** Likely valid error example (not documentation error)
**If NO to all:** Likely documentation error

**Step 5: Validate Workflow Variations (Per Finding)**

**Questions to ask:**
- [ ] Is variation labeled "Exception" or "Approved"?
- [ ] Are conditions for variation clear?
- [ ] Is variation intentional (not accidental)?
- [ ] Is variation documented in workflow_variations.md?

**If YES to 3+:** Likely valid variation (not error)
**If NO to all:** Likely error

**Step 6: Document Context Decisions**

Create table:

| Finding | File | Context Type | Valid Exception? | Rationale |
|---------|------|--------------|------------------|-----------|
| "S5a" notation | s5_guide.md:45 | Historical | YES | In "Historical Note" section, past tense |
| "S5a" notation | s6_guide.md:120 | None | NO | Current instructions, no context |
| Missing import | s7_guide.md:200 | Error example | YES | In code block, "If you see..." |
| ... | ... | ... | ... | ... |

**Step 7: Apply Filters to Findings**

**Original findings:** 50 instances of "S5a"

**After context validation:**
- 30 instances: Valid historical references
- 5 instances: Valid anti-pattern examples
- 15 instances: Actual errors requiring fixes

**Only fix the 15 actual errors.**

---

## Context-Sensitive Rules

### Rule 1: Historical Sections May Use Any Notation

**Context:** Historical evidence sections intentionally reference old structures.

**Valid:**
```markdown
## Historical Evidence

The old workflow (2024) used S5a/S5b/S5c notation. This caused confusion, leading to the current S5.P1/P2/P3 system.
```

**Validation:** In historical section → Use of old notation VALID

---

### Rule 2: Anti-Pattern Examples Should Show Wrong Approach

**Context:** Educational examples intentionally show mistakes.

**Valid:**
```markdown
❌ **WRONG:**
```text
def calculate(items):  # No type hints
    return sum(items)
```text

✅ **CORRECT:**
```
def calculate(items: list[int]) -> int:
    return sum(items)
```text
```markdown

**Validation:** Marked as wrong, followed by correct version → VALID

---

### Rule 3: Templates May Reference Non-Existent Files as Placeholders

**Context:** Templates are meta-documents showing structure.

**Valid:**
```markdown
# Template: feature_spec_template.md

See DISCOVERY.md Section [X] for background.
See RESEARCH_NOTES.md for technical analysis.

[USER: Replace [X] with actual section number]
```

**Validation:** Template with placeholder markers → VALID

---

### Rule 4: Examples May Show Incomplete Code for Brevity

**Context:** Examples often omit boilerplate for clarity.

**Valid:**
```markdown
### Example

```text
def process_data(df):
    return df.groupby('category').sum()
```python

(Assumes `import pandas as pd` already present)
```

**Validation:** Example with explicit assumption statement → VALID

---

## Real Examples

### Example 1: False Positive - Historical Reference Flagged as Error

**Audit Finding:**
```text
D2: Terminology Consistency
FOUND: "S5a" notation in stages/s5/s5_implementation_planning.md:15
ERROR: Old notation, should be S5.P1
```markdown

**Context Review:**
```markdown
## Line 10-20 of s5_implementation_planning.md:

## Notation Evolution

**Historical Note:** Prior to January 2025, this stage used S5a/S5b/S5c notation for phases. This was changed to S5.P1/P2/P3 to align with standard notation system.

**Current Notation:** Always use S5.P1, S5.P2, S5.P3.
```

**Context Validation:**
- ✅ Labeled "Historical Note"
- ✅ Past tense ("used," "was changed")
- ✅ Explains current notation
- ✅ Clear evolution context

**Decision:** VALID historical reference, NOT an error. Do not fix.

**Action:** Update audit finding:
```text
D2: Terminology Consistency
FOUND: "S5a" notation in stages/s5/s5_implementation_planning.md:15
STATUS: Valid historical reference (intentional)
ACTION: No fix needed
```yaml

---

### Example 2: True Positive - Actual Error Despite Example Context

**Audit Finding:**
```text
D1: Cross-Reference Accuracy
FOUND: Reference to "stages/s4/s4_testing.md" in stages/s3/guide.md:45
ERROR: File does not exist (should be s4_feature_testing_strategy.md)
```

**Context Review:**
```markdown
## Line 40-50 of stages/s3/guide.md:

### Example: Cross-Stage References

When referencing other stages, use correct file paths.

**Example:**
See `stages/s4/s4_testing.md` for testing approach.
```diff

**Context Validation:**
- ❌ No "WRONG" or ❌ marker
- ❌ Not in anti-pattern section
- ❌ Appears to be recommended approach
- ❌ File path is actually wrong

**Decision:** This is an ACTUAL ERROR in the example. Fix required.

**Action:**
```diff
**Example:**
-See `stages/s4/s4_testing.md` for testing approach.
+See `stages/s4/s4_feature_testing_strategy.md` for testing approach.
```

---

### Example 3: Valid Exception - Bug Fix Workflow Variation

**Audit Finding:**
```text
D3: Workflow Integration
FOUND: Workflow skips S4 in debugging/debugging_protocol.md:120
ERROR: All stages required, S4 cannot be skipped
```markdown

**Context Review:**
```markdown
## Line 115-125 of debugging/debugging_protocol.md:

## Bug Fix Workflow Exception

**[APPROVED EXCEPTION]**

For urgent production hotfixes, the workflow may skip S4 (Feature Testing Strategy) and proceed directly from S3 to S5.

**Conditions:**
- Critical production bug requiring immediate fix
- User explicitly approves S4 skip
- Fix is simple, low-risk change

This is the ONLY approved deviation from standard workflow.
```

**Context Validation:**
- ✅ Marked "[APPROVED EXCEPTION]"
- ✅ Clear conditions specified
- ✅ Limited scope ("ONLY approved deviation")
- ✅ User approval required

**Decision:** VALID workflow variation, NOT an error.

**Action:** Document in audit findings:
```text
D3: Workflow Integration
FOUND: Workflow skips S4 in debugging/debugging_protocol.md:120
STATUS: Approved exception (bug fix workflow)
ACTION: No fix needed - variation is documented and approved
```yaml

---

### Example 4: Ambiguous - Needs Clarification Marker

**Audit Finding:**
```text
D4: Count Accuracy
FOUND: "S5 has 20 iterations" in stages/s5/guide.md:10
ERROR: Actual iteration count is 22
```

**Context Review:**
```markdown
## Line 10-15 of stages/s5/guide.md:

## S5: Implementation Planning

S5 has 20 iterations across 3 rounds. The final 2 iterations (I21-I22) were added in version 2.0 for enhanced gate validation.
```diff

**Context Validation:**
- ⚠️ Mentions "20 iterations" AND "final 2 iterations"
- ⚠️ Unclear if "20" is current or historical
- ⚠️ Could mean "20 originally, now 22" OR "20 main + 2 extra"
- ⚠️ Ambiguous statement

**Decision:** UNCLEAR context. Needs clarification.

**Action:** Improve clarity:
```diff
## S5: Implementation Planning

-S5 has 20 iterations across 3 rounds. The final 2 iterations (I21-I22) were added in version 2.0 for enhanced gate validation.
+S5 has 22 iterations across 3 rounds.
+
+**Historical Note:** Originally had 20 iterations. I21-I22 added in version 2.0 for enhanced gate validation.
```

---

### Example 5: Template Placeholder vs Incomplete Content

**Audit Finding:**
```text
D5: Content Completeness
FOUND: Generic placeholder text in feature_01/spec.md:20
ERROR: Content incomplete, needs feature-specific information
```markdown

**Context Review:**
```markdown
## Line 20-25 of feature_01/spec.md:

## Background

Provide feature background here based on DISCOVERY.md findings.
```

**Initial Assessment:** Looks incomplete.

**BUT - Check if this is template vs actual feature spec:**
```bash
# Check file header
head -5 feature_01/spec.md
```markdown

**If header shows:**
```markdown
# Feature Specification Template
```

**Then:** This is TEMPLATE (valid placeholder)

**If header shows:**
```markdown
# Feature 01: User Authentication - Specification
```

**Then:** This is ACTUAL FEATURE SPEC (incomplete, needs fixing)

**Context Validation:**
- Decision depends on whether file is template or instance
- Template: Placeholder VALID
- Instance: Incomplete, ERROR

**Action:** Check file type, then decide.

---

## Integration with Other Dimensions

### ALL Other Dimensions

**D7 provides context validation for ALL other dimensions:**

**D1: Cross-Reference Accuracy**
- Finding: Broken link
- D7: Is it example of broken link (intentional) or actual broken link?

**D2: Terminology Consistency**
- Finding: Old notation
- D7: Historical reference (valid) or current usage (error)?

**D3: Workflow Integration**
- Finding: Stage skipped
- D7: Approved variation (valid) or workflow violation (error)?

**D4: Count Accuracy**
- Finding: Count mismatch
- D7: Historical count (valid) or current error?

**D5: Content Completeness**
- Finding: Missing section
- D7: Template placeholder (valid) or incomplete (error)?

**And so on for all dimensions...**

**D7's Role:** Meta-dimension providing context analysis for interpreting all other dimension findings.

---

## Summary

**D7: Context-Sensitive Validation distinguishes intentional exceptions from actual errors.**

**Key Validations:**
1. ✅ Historical references (markers detectable)
2. ✅ Anti-pattern examples (❌/✅ markers)
3. ✅ Quoted errors (code block detection)
4. ⚠️ Intentional variations (requires judgment)
5. ✅ Template placeholders ([USER:] markers)
6. ✅ Deprecated explanations (past tense, markers)
7. ✅ Explicit context markers

**Automation: ~20%**
- Can detect presence of context markers
- Cannot determine sufficiency of context (requires human judgment)

**Critical for:**
- Reducing false positives (don't "fix" intentional references)
- Focusing audit effort on actual errors
- Preserving valuable historical/educational content
- Systematic context interpretation

**Usage:** Apply D7 analysis to findings from ALL other dimensions before creating fix plans.

---

**Last Updated:** 2026-02-04
**Version:** 1.0
**Status:** ✅ Fully Implemented
