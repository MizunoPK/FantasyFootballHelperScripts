# Context Analysis Guide

**Purpose:** Decision trees for determining if pattern matches are errors or intentional cases
**Audience:** Agents conducting Stage 2 Fix Planning
**Last Updated:** 2026-02-05

---

## Table of Contents

1. [Quick Decision Tree](#quick-decision-tree)
2. [Context Markers](#context-markers)
3. [Common Scenarios](#common-scenarios)
4. [File-Specific Exception Rules](#file-specific-exception-rules)
5. [Analysis Workflow](#analysis-workflow)
6. [Documentation Template](#documentation-template)

---

## Quick Decision Tree

```text
┌─────────────────────────────────────────────┐
│  Pattern Match Found (e.g., "S5a")          │
└─────────────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          │                   │
    Check Context         Is there a
    (5 lines before      context marker?
     5 lines after)           │
          │            ┌──────┴──────┐
          ↓            │             │
    ┌─────────┐      YES           NO
    │ Markers │       │             │
    │ Present?│       ↓             ↓
    └─────────┘   ┌────────┐   ┌────────┐
          │       │Analyze │   │Likely  │
     ┌────┴────┐  │Context │   │ERROR   │
     │         │  │Type    │   └────────┘
    YES       NO  └────────┘        │
     │         │       │            ↓
     ↓         ↓       ↓       Fix immediately
┌─────────┬─────────┬─────────┐
│Historical│Example│Template │
│Reference│Content│Placeholder│
└─────────┴────────┴─────────┘
     │         │         │
     ↓         ↓         ↓
INTENTIONAL INTENTIONAL IF VALID
  Document   Document   OTHERWISE
                        FIX IT
```

---

## Context Markers

### Category 1: Historical Reference Markers

**Presence of these = Likely intentional reference to old patterns:**

```text
✅ Valid Historical Markers:
- "Historical Note:"
- "Previously,"
- "Before 2025,"
- "Old workflow:"
- "Deprecated:"
- "Legacy notation:"
- "(now S#.P#)"
- "was changed to"
- "prior to"
```

**Example - INTENTIONAL:**
```markdown
## Historical Note

Before 2025, the workflow used S5a notation. This was changed to S5.P1 for clarity.
```

**Action:** Document as intentional, do NOT fix

---

### Category 2: Anti-Pattern Example Markers

**Presence of these = Showing wrong code intentionally:**

```text
✅ Valid Example Markers:
- "❌ WRONG:"
- "❌ BAD:"
- "Anti-pattern:"
- "Incorrect example:"
- "Don't do this:"
- "Example of mistake:"
- "Before fix:"
```

**Example - INTENTIONAL:**
```markdown
## Common Mistakes

❌ WRONG:
```bash
git reset --hard  # Destroys uncommitted work
```

✅ CORRECT:
```bash
git stash  # Saves uncommitted work
```text
```

**Action:** Document as intentional, do NOT fix

**Red Flag:** If example has no marker, verify it's actually showing wrong code vs being a mistake itself

---

### Category 3: Quoted Error/Output Markers

**Presence of these = Showing system output, not documentation content:**

```text
✅ Valid Quote Markers:
- In code blocks (```)
- "Error message:"
- "Output:"
- "Agent said:"
- "User saw:"
```

**Example - INTENTIONAL:**
```markdown
The agent encountered this error:
```yaml
Error: File stages/s6/file.md not found
```text
```

**Action:** Document as intentional, do NOT fix

---

### Category 4: Template Placeholder Markers

**Presence of these = Template file with placeholder text:**

```text
✅ Valid Placeholder Markers:
- [PLACEHOLDER]
- [Your text here]
- [N]
- [description]
- [file_path]
- YYYY-MM-DD (dates)
```

**Example - INTENTIONAL:**
```markdown
# Feature [NN]_[name]

**Description:** [Your feature description here]
**Files Modified:** [N] files
```

**Action:** IF file is in `templates/` directory → Document as intentional
**Action:** IF file is NOT in `templates/` → Likely error, needs actual content

---

### Category 5: Explanatory Content Markers

**Presence of these = Explaining old patterns, not using them:**

```text
✅ Valid Explanatory Markers:
- "explained why"
- "refers to"
- "in the old system"
- "For example, the old"
- "This replaced"
```

**Example - INTENTIONAL:**
```markdown
The old notation "S5a" referred to Round 1 of Stage 5, which is now called S5.P1.
```

**Action:** Document as intentional, do NOT fix

---

## Common Scenarios

### Scenario 1: Old Notation Found

**Pattern Match:** `S5a` found in file

**Decision Process:**

1. **Read 5 lines before and after the match**
2. **Check for historical markers:**
   - "Historical", "Old", "Previously", "Before", etc.
3. **Check for example markers:**
   - "❌ WRONG", "Example of", "Don't use", etc.
4. **Check file type:**
   - Is it in `templates/` directory?
   - Is it in a TEMPLATE file? (filename contains "template")

**Outcomes:**

| Context Found | Action | Reason |
|---------------|--------|--------|
| "Historical Note: S5a was..." | **INTENTIONAL** | Historical reference |
| "❌ WRONG: S5a..." | **INTENTIONAL** | Anti-pattern example |
| "Complete S5a iterations" (no markers) | **ERROR** | Current content using old notation |
| In `templates/feature_XX_template.md` | **EVALUATE** | Could be placeholder or error |

---

### Scenario 2: File Path Reference Not Found

**Pattern Match:** `stages/s6/file.md` referenced but file doesn't exist

**Decision Process:**

1. **Check if in error/output example:**
   - Is it in code block showing error message?
   - Is it labeled "Error:" or "Output:"?
2. **Check if file was moved:**
   - Does `stages/s9/file.md` exist? (renumbering)
   - Is path in historical section?
3. **Check if intentional broken link example:**
   - Is it in section about validating links?
   - Is it in audit guide showing what to check?

**Outcomes:**

| Context Found | Action | Reason |
|---------------|--------|--------|
| In code block: "Error: stages/s6/ not found" | **INTENTIONAL** | Showing error message |
| In audit guide: "Check for stages/s6/ refs" | **INTENTIONAL** | Explaining what to audit |
| In workflow guide: "Read stages/s6/file.md" | **ERROR** | Broken reference needs fixing |

---

### Scenario 3: TODO/TBD Marker Found

**Pattern Match:** `TODO` or `TBD` found in file

**Decision Process:**

1. **Check file type:**
   - Is it in `templates/` directory?
   - Is filename `*_template.md`?
2. **Check context:**
   - Is it in placeholder position: "**Description:** TODO"?
   - Is it in reference section showing what to complete?
3. **Check section header:**
   - Is it under "Future Work" or "Planned Features"?

**Outcomes:**

| Context Found | Action | Reason |
|---------------|--------|--------|
| In `templates/spec_template.md` | **INTENTIONAL** | Template placeholder |
| In "Future Work" section | **EVALUATE** | Planned work (may be acceptable) |
| In main content (no marker) | **ERROR** | Incomplete content |

---

### Scenario 4: Wrong File Reference in Code Example

**Pattern Match:** Reference to non-existent file in code block

**Example:**
```markdown
```bash
# Read the discovery file
Read stages/nonexistent_file.md
```text
```

**Decision Process:**

1. **Is it in example/demonstration section?**
2. **Does surrounding text explain it's a generic example?**
3. **Is actual filename clearly a placeholder?** ("your_file.md", "example.md")

**Outcomes:**

| Context Found | Action | Reason |
|---------------|--------|--------|
| "Example command (replace with actual file):" | **INTENTIONAL** | Generic example |
| "Run this command:" (no disclaimer) | **ERROR** | Broken instruction |

---

## File-Specific Exception Rules

### CLAUDE.md Exceptions

**Location:** Project root `CLAUDE.md`

**Known Intentional Cases:**

1. **Historical workflow references** in "Workflow Evolution" sections
2. **Anti-pattern examples** in "Common Mistakes" sections
3. **Old stage numbers** in "Historical Evidence" sections

**Validation:**
```bash
# Check CLAUDE.md for old notation
grep -n "S[0-9][a-z]" CLAUDE.md

# For each match, check if in historical context
grep -B 5 -A 5 "S[0-9][a-z]" CLAUDE.md | grep -q "Historical\|Before"
```

---

### Template Files Exceptions

**Location:** `templates/` directory or `*_template.md` files

**Known Intentional Cases:**

1. **Placeholder text:** `[description]`, `[N]`, `[name]`
2. **Example dates:** `YYYY-MM-DD`, `2026-XX-XX`
3. **Variable markers:** `{epic_name}`, `{feature_name}`

**Validation:**
```bash
# Check if file is template
if [[ "$file" == *"template"* ]] || [[ "$file" == templates/* ]]; then
  echo "Template file - placeholders expected"
fi
```

---

### Audit Guide Exceptions

**Location:** `feature-updates/guides_v2/audit/` directory

**Known Intentional Cases:**

1. **Examples of errors to find:** "Search for S5a notation"
2. **Pattern demonstrations:** "grep for 'old_pattern'"
3. **Before/after examples:** Showing incorrect code then correct code

**Validation:**
- Check if in "Pattern Types" or "Search Commands" sections
- Check if labeled as "What to Search For"
- Check if in "Common Issues" section (describing errors, not making them)

---

### Example Files

**Location:** `examples/` directory

**Known Intentional Cases:**

1. **Historical audit rounds** - May reference old notation that existed at time
2. **Error demonstrations** - Showing mistakes that were found
3. **Before-state snapshots** - Capturing state before fixes

**Validation:**
- All content in `examples/` is historical/demonstrative
- Check if labeled "Before Fix:" or "Error Found:"

---

## Analysis Workflow

### Step 1: Capture Match with Context

```bash
# Find match with 5 lines of context
PATTERN="your_pattern"
FILE="path/to/file.md"
LINE_NUM=$(grep -n "$PATTERN" "$FILE" | cut -d: -f1 | head -1)

# Show context
sed -n "$((LINE_NUM - 5)),$((LINE_NUM + 5))p" "$FILE"
```

### Step 2: Check for Context Markers

```bash
# Check if any markers present in context
CONTEXT=$(sed -n "$((LINE_NUM - 5)),$((LINE_NUM + 5))p" "$FILE")

# Check for each marker category
echo "$CONTEXT" | grep -q "Historical\|Old\|Previously" && echo "MARKER: Historical"
echo "$CONTEXT" | grep -q "❌ WRONG\|❌ BAD\|Anti-pattern" && echo "MARKER: Example"
echo "$CONTEXT" | grep -q "Error:\|Output:\|Agent said:" && echo "MARKER: Quote"
echo "$CONTEXT" | grep -q "\[.*\]\|YYYY-MM-DD\|{.*}" && echo "MARKER: Placeholder"
```

### Step 3: Apply Decision Rules

```text
IF marker found THEN
  Check if marker validates exception
  IF yes THEN
    DOCUMENT as intentional
  ELSE
    FLAG for user review
  END IF
ELSE
  MARK as error
  ADD to fix plan
END IF
```

### Step 4: Document Decision

**Use this template:**
```markdown
## Context Analysis - [Pattern]

**File:** path/to/file.md:LINE
**Pattern Found:** [pattern text]
**Context (±5 lines):**
```text
[context text]
```text

**Markers Found:**
- [Historical / Example / Quote / Placeholder / None]

**Decision:** INTENTIONAL / ERROR / USER_REVIEW_NEEDED

**Reason:**
[Explanation of why this is intentional or error]

**Action:**
[Document and skip / Fix immediately / Ask user]
```

---

## Documentation Template

When documenting intentional exceptions for verification report:

```markdown
### Remaining Instances (Intentional)

| File | Line | Pattern | Context | Reason |
|------|------|---------|---------|--------|
| audit_overview.md | 240 | "S5a" | Example pattern in Round 1 | Historical reference showing old audit pattern |
| s5_p1_planning.md | 45 | "TODO" | Template section | Placeholder in template for user to fill |
| CLAUDE.md | 123 | "9 stages" | Historical Note section | Refers to old workflow structure |

**Total Intentional:** 3 instances
**Action:** Documented, no fixes needed
```

---

## When in Doubt

### Escalation to User

**If uncertain after analysis:**

```markdown
## USER REVIEW NEEDED

**File:** path/to/file.md:LINE
**Pattern:** [pattern]
**Context:**
```text
[5 lines before]
>>> [MATCH LINE] <<<
[5 lines after]
```text

**Question:** Is this intentional or error?

**My Analysis:**
- No clear context markers found
- Could be [possibility 1] OR [possibility 2]
- Need clarification on intent

**Options:**
1. INTENTIONAL - Document and skip
2. ERROR - Fix to [suggested replacement]
3. CLARIFY - Needs more context

Please advise.
```

---

## Red Flags Requiring Extra Scrutiny

### High-Risk False Negatives

**These scenarios often LOOK intentional but may be errors:**

1. **Undocumented examples** - Example code with no "❌ WRONG" marker
2. **Ambiguous historical refs** - Old notation without "Historical Note:" label
3. **Template errors** - Actual mistakes in template files (not placeholders)
4. **Copy-paste errors** - Intentional content copied to wrong location

**Always verify:**
- Example code is properly labeled
- Historical sections have clear markers
- Templates have only valid placeholders
- Context makes logical sense

---

## See Also

- **D7: Context-Sensitive Validation:** `dimensions/d7_context_sensitive_validation.md` - Complete dimension guide
- **Known Exceptions:** `reference/known_exceptions.md` - Pre-documented exception cases
- **Stage 2 Fix Planning:** `stages/stage_2_fix_planning.md` - When to use context analysis
