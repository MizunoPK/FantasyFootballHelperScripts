# D14: Character and Format Compliance

**Dimension Number:** 14
**Category:** Structural Dimensions
**Automation Level:** 95% automated
**Priority:** HIGH
**Last Updated:** 2026-02-19

**Focus:** Ensure guide files use only agent-readable characters and standard markdown formatting, with no Unicode characters that can cause parsing confusion or readability issues.
**Typical Issues Found:** 0-20 per audit (spikes after manual edits or content pasted from external sources)

---

## Table of Contents

1. [What This Checks](#what-this-checks)
2. [Why This Matters](#why-this-matters)
3. [Pattern Types](#pattern-types)
4. [Banned Characters](#banned-characters)
5. [Allowed Exceptions](#allowed-exceptions)
6. [Automated Validation](#automated-validation)
7. [Manual Validation](#manual-validation)
8. [Fix Patterns](#fix-patterns)
9. [Real Examples](#real-examples)
10. [Integration with Other Dimensions](#integration-with-other-dimensions)

---

## What This Checks

**D14: Character and Format Compliance** ensures that every character in guide files can be reliably read, rendered, and acted upon by AI agents:

1. **Banned Unicode Characters** - Characters that should use standard ASCII/markdown alternatives (box chars used as checkboxes, etc.)
2. **Standard Checkbox Format** - All task/checklist items use `- [ ]` or `- [x]` (not Unicode box characters)
3. **Code Block Completeness** - All code blocks have a closing triple-backtick (no unclosed blocks)

**Coverage:**
- All `.md` files in .shamt/guides (stages/, reference/, templates/, prompts/, parallel_work/, debugging/)
- Excludes: audit/outputs/ and audit/round_*.md (temporary audit logs)

**Key Distinction from D10 (Intra-File Consistency):**
- **D10:** Validates consistency of notation and terminology within files
- **D14:** Validates the character-level encoding and format primitives that agents rely on to parse content

---

## Why This Matters

**Agents read guide files as plain text or markdown. Non-standard characters cause:**

### Impact 1: Silent Rendering Failures
Unicode box characters (`□`, `☐`, `☑`) render correctly in most text editors, but may display as `?`, `□`, or garbage in some terminal environments. Agents reading files via tool calls receive raw bytes — if they're not expecting UTF-8 multi-byte sequences for what "should be" a simple checkbox, the content is harder to reliably parse.

### Impact 2: Incorrect Checkbox Handling
An agent looking for task completion status may search for `- [ ]` (standard markdown) but miss `☐` (U+2610) even though both look like empty checkboxes to a human reader. This creates invisible task tracking errors.

### Impact 3: Copy-Paste Contamination
Content pasted from Google Docs, Word, or other tools frequently introduces Unicode box characters, curly quotes, em-dashes, and other non-ASCII characters that "look fine" but differ from expected ASCII patterns.

### Impact 4: Inconsistency Across Files
If some files use `- [ ]` and others use `□`, agents face inconsistent checklist formats — reducing confidence in parsing and potentially causing them to miss checklist items.

**Historical Evidence:**
- Round 1.3 audit found 85 Unicode checkbox characters across 8 files, introduced via content pasting from external documents
- Characters found: □ (U+25A1), ☐ (U+2610), ☑ (U+2611) — all "looked correct" in editor previews

---

## Pattern Types

D14 violations fall into four categories based on character type and impact:

### Type A: Unicode Checkbox Characters (CRITICAL)

**What:** Unicode box characters used as checklist items instead of standard markdown checkboxes
**Examples:** `□` (U+25A1), `☐` (U+2610), `☑` (U+2611), `☒` (U+2612)
**Impact:** Agents searching for `- [ ]` miss these items; invisible task tracking failures
**Fix:** Replace with `- [ ]` or `- [x]`
**Automated:** ✅ Yes (exact byte match)

### Type B: Unicode Quotation Marks (HIGH)

**What:** Curly/smart quotes from word processors or external content
**Examples:** `"` (U+201C), `"` (U+201D), `'` (U+2018), `'` (U+2019)
**Impact:** Agents grepping for quoted strings or code examples fail to match
**Fix:** Replace with straight ASCII quotes `"` and `'`
**Automated:** ✅ Yes (exact byte match)

### Type C: Unicode Dashes Used as Hyphens (MEDIUM)

**What:** Em-dash or en-dash used in place of ASCII hyphen/dash
**Examples:** `–` (U+2013 EN DASH), `—` (U+2014 EM DASH)
**Impact:** Code examples and structured lists break when dashes are non-ASCII
**Fix:** Replace with `--` or `-` in code/lists; acceptable in prose (human review required)
**Automated:** ⚠️ Partial (detection automated; context judgment manual)

### Type D: Box-Drawing Characters in Prose (LOW)

**What:** Box-drawing chars used as prose list-item prefixes instead of inside diagrams
**Examples:** `│` used as bullet prefix in prose (not in a diagram block)
**Impact:** Inconsistent visual parsing; agents expecting `-` bullets miss `│` items
**Fix:** Replace prose-context box chars with standard markdown list markers
**Automated:** ⚠️ Partial (context-sensitive; diagram use is allowed)

---

## Banned Characters

### Category A: Unicode Checkboxes (Replace with Standard Markdown)

| Character | Unicode | Name | Replace With |
|-----------|---------|------|-------------|
| `□` | U+25A1 | WHITE SQUARE | `- [ ]` |
| `☐` | U+2610 | BALLOT BOX | `- [ ]` |
| `☑` | U+2611 | BALLOT BOX WITH CHECK | `- [x]` |
| `☒` | U+2612 | BALLOT BOX WITH X | `- [x]` |

**Rule for numbered lists:** If the Unicode checkbox follows a number+dot (e.g., `1. ☐ item`), replace with `1. [ ] item` (keep the numbered list structure, remove the `- ` prefix).

### Category B: Unicode Quotation Marks (Replace with ASCII Quotes)

| Character | Unicode | Name | Replace With |
|-----------|---------|------|-------------|
| `"` | U+201C | LEFT DOUBLE QUOTATION MARK | `"` |
| `"` | U+201D | RIGHT DOUBLE QUOTATION MARK | `"` |
| `'` | U+2018 | LEFT SINGLE QUOTATION MARK | `'` |
| `'` | U+2019 | RIGHT SINGLE QUOTATION MARK | `'` |

**Exception:** Category B violations in quoted user content (showing an example of what a user might say) are acceptable if clearly demarcated as external content. Use judgment.

### Category C: Unicode Dashes Used as Hyphens (Replace with ASCII)

| Character | Unicode | Name | Replace With |
|-----------|---------|------|-------------|
| `–` | U+2013 | EN DASH | `--` or `-` |
| `—` | U+2014 | EM DASH | `--` or `-` |

**Exception:** Em-dashes used intentionally in prose for stylistic effect (not as list-item markers or code) are acceptable. Flag for human review.

### Category D: Box-Drawing Characters Used in Prose Checkpoints (NOT diagrams)

Box-drawing characters (`│`, `┌`, `└`, `├`, `─`, `━`) are **acceptable in ASCII art diagrams and flowcharts**. They become problematic only when used in contexts where simpler markdown would work (e.g., as bullet point prefixes in prose).

**Acceptable (ASCII art diagram):**
```text
┌────────────────────┐
│ CRITICAL RULES     │
└────────────────────┘
```

**Not acceptable (as prose list items):**
```text
│ - Complete step 1
│ - Complete step 2
```

**Search pattern:** Box chars used as list-item prefixes in prose sections (not inside a clearly-delineated diagram block).

---

## Allowed Exceptions

The following Unicode characters are **explicitly allowed** throughout guides:

### Emojis Used as Semantic Markers

These serve specific semantic purposes and are intentional:

| Character | Unicode | Purpose | Used In |
|-----------|---------|---------|---------|
| `✅` | U+2705 | Pass / correct / complete | Checklists, verification |
| `❌` | U+274C | Fail / wrong / blocked | Anti-patterns, failures |
| `🚨` | U+1F6A8 | Critical warning | MANDATORY sections |
| `⚠️` | U+26A0 | Caution / warning | Important notes |
| `🛑` | U+1F6D1 | Stop / checkpoint | Mandatory stops |
| `→` | U+2192 | Rightwards arrow | Flow transitions |
| `⏱` | U+23F1 | Time estimate | Duration markers |
| `⏳` | U+23F3 | Pending / in progress | Status markers |
| `🔀` | U+1F500 | Shuffle / parallel | Parallel work sections |
| `📖` | U+1F4D6 | Read instruction | READ callouts |
| `🎯` | U+1F3AF | Goal | Goal markers |
| `🚀` | U+1F680 | Launch / opportunity | Parallel work triggers |

### Box-Drawing Characters in Diagrams

`│`, `┌`, `└`, `├`, `─`, `━`, `╔`, `╗`, `╚`, `╝`, `║` are allowed when clearly used in ASCII art diagrams and flowcharts.

### Arrows in Flow Diagrams

`→`, `←`, `↑`, `↓`, `↔`, `⟶` are allowed as flow indicators in diagrams and transitions.

### Detection and Validation Scripts

Banned characters present in audit detection scripts (e.g., `audit/scripts/pre_audit_checks.sh`) as detection targets or lookup table values are explicitly allowed. The script must reference the characters it detects. These occurrences are never in guide content and are never rendered as documentation.

**Example:** `BANNED = {'\u25a1': ('□', ...), '\u2610': ('☐', ...)}` — the `□` and `☐` characters appear as dictionary values to show what the banned character looks like, not as content.

---

## Automated Validation

### Pre-Audit Script Detection

**Search patterns for each banned category:**

```python
# Python validation script
import glob, os

BASE = '.shamt/guides'
EXCLUDE = ['/audit/round_', '/audit/outputs/']

# Category A: Unicode checkboxes
BANNED_CHARS = {
    '\u25a1': ('□', 'U+25A1 WHITE SQUARE', '- [ ]'),
    '\u2610': ('☐', 'U+2610 BALLOT BOX', '- [ ]'),
    '\u2611': ('☑', 'U+2611 BALLOT BOX WITH CHECK', '- [x]'),
    '\u2612': ('☒', 'U+2612 BALLOT BOX WITH X', '- [x]'),
    '\u201c': ('"', 'U+201C LEFT DOUBLE QUOTE', '"'),
    '\u201d': ('"', 'U+201D RIGHT DOUBLE QUOTE', '"'),
    '\u2018': (''', 'U+2018 LEFT SINGLE QUOTE', "'"),
    '\u2019': (''', 'U+2019 RIGHT SINGLE QUOTE', "'"),
    '\u2013': ('–', 'U+2013 EN DASH', '--'),
    '\u2014': ('—', 'U+2014 EM DASH', '--'),
}

files = [f for f in glob.glob(BASE + '/**/*.md', recursive=True)
         if not any(ex in f for ex in EXCLUDE)]

total = 0
for fpath in files:
    with open(fpath, encoding='utf-8') as f:
        content = f.read()
    for char, (display, name, replacement) in BANNED_CHARS.items():
        count = content.count(char)
        if count > 0:
            rel = os.path.relpath(fpath, BASE)
            print(f'BANNED {name}: {count} in {rel} → replace with {repr(replacement)}')
            total += count

print(f'Total banned characters: {total}')
```

**Grep-based quick check:**

```bash
# Check for Unicode checkboxes (most common issue)
python3 -c "
import glob, sys
files = glob.glob('**/*.md', recursive=True)
files = [f for f in files if 'audit/round_' not in f]
found = []
for f in files:
    content = open(f, encoding='utf-8').read()
    for char in ['\u25a1', '\u2610', '\u2611', '\u2612']:
        if char in content:
            found.append((f, char, content.count(char)))
if found:
    for f, c, n in found:
        print(f'FOUND {repr(c)} x{n} in {f}')
    sys.exit(1)
else:
    print('CLEAN: No Unicode checkboxes found')
"
```

**Automation Coverage: 95%**
- ✅ All banned character categories (exact byte-level detection)
- ✅ Count and location reporting
- ❌ Context-sensitive exceptions (em-dash in prose vs code — requires human review)

---

## Manual Validation

### Manual Process (Character Compliance Audit)

**Duration:** 10-15 minutes
**When:** After any manual editing session or content paste from external sources

**Step 1: Run automated detection (2 min)**
```bash
cd .shamt/guides
python3 -c "
import glob
files = [f for f in glob.glob('**/*.md', recursive=True) if 'audit/round_' not in f]
banned = ['\u25a1', '\u2610', '\u2611', '\u2612', '\u201c', '\u201d', '\u2018', '\u2019', '\u2013', '\u2014']
for f in files:
    content = open(f, encoding='utf-8').read()
    for char in banned:
        if char in content:
            print(f'{repr(char)} x{content.count(char)} in {f}')
"
```

**Step 2: Spot-check recently edited files (5 min)**
- Open each file modified in recent session
- Search (Ctrl+F) for: `□` `☐` `☑` `"` `"` `'` `'` `–` `—`
- Flag any occurrences

**Step 3: Review em-dash findings (5 min)**
- Em-dash `—` may be intentional in flowing prose
- Flag occurrences in code blocks or as list markers (not acceptable)
- Accept occurrences in narrative prose sentences (acceptable)

---

## Fix Patterns

### Pattern 1: Bulk Replace Unicode Checkboxes

```python
# Fix all Unicode checkboxes in all guide files
import glob, re, os

BASE = '/home/kai/code/[project name]Refactored/.shamt/guides'
EXCLUDE = ['audit/round_']

REPLACEMENTS = [
    ('\u2611', 'checked_box'),  # ☑ → - [x]  (check first - most specific)
    ('\u2612', 'checked_box'),  # ☒ → - [x]
    ('\u2610', 'empty_box'),    # ☐ → - [ ]
    ('\u25a1', 'empty_box'),    # □ → - [ ]
]

def replace_in_file(fpath):
    with open(fpath, encoding='utf-8') as f:
        content = f.read()

    original = content
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        # Process each replacement
        for char, box_type in REPLACEMENTS:
            if char not in line:
                continue

            stripped = line.lstrip()
            indent = line[:len(line) - len(stripped)]

            if box_type == 'checked_box':
                replacement = '- [x] '
            else:
                replacement = '- [ ] '

            # Numbered list: "1. □ item" → "1. [ ] item"
            if re.match(r'^\s*\d+\.\s+' + re.escape(char) + r' ', line):
                line = re.sub(re.escape(char) + r' ', '[ ] ', line)
            else:
                # Standard replacement
                line = line.replace(char + ' ', replacement)
                line = line.replace(char, replacement.rstrip())

        new_lines.append(line)

    new_content = '\n'.join(new_lines)
    if new_content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

files = [f for f in glob.glob(BASE + '/**/*.md', recursive=True)
         if not any(ex in f for ex in EXCLUDE)]
changed = sum(1 for f in files if replace_in_file(f))
print(f'Fixed {changed} files')
```

### Pattern 2: Replace Unicode Quotes

```bash
# Replace curly/smart quotes with ASCII equivalents
# Use Python (sed struggles with multi-byte UTF-8)
python3 -c "
import glob
files = [f for f in glob.glob('**/*.md', recursive=True) if 'audit/round_' not in f]
for f in files:
    content = open(f, encoding='utf-8').read()
    new = (content
        .replace('\u201c', '\"').replace('\u201d', '\"')
        .replace('\u2018', \"'\").replace('\u2019', \"'\"))
    if new != content:
        open(f, 'w', encoding='utf-8').write(new)
        print(f'Fixed quotes in {f}')
"
```

### Pattern 3: Replace Em/En Dashes in Code/Lists

```bash
# Find em/en dashes and replace in non-prose contexts
# REQUIRES MANUAL REVIEW for prose context
python3 -c "
import glob, re
files = [f for f in glob.glob('**/*.md', recursive=True) if 'audit/round_' not in f]
for f in files:
    content = open(f, encoding='utf-8').read()
    if '\u2013' in content or '\u2014' in content:
        print(f'Review needed: {f}')
        for i, line in enumerate(content.split('\n'), 1):
            if '\u2013' in line or '\u2014' in line:
                print(f'  Line {i}: {repr(line)}')
"
```

---

## Real Examples

### Example 1: Checkbox Characters from External Paste (Round 1 Audit)

**Issue Found:** Round 1.3 audit discovered 85 Unicode checkbox characters across 8 files

**Root Cause:** Content was copied from a word processor or Google Doc that automatically converts `[]` to `☐` and `[x]` to `☑`

**Files Affected:**
- `reference/stage_2/research_examples.md` (24 occurrences)
- `parallel_work/parallel_work_prompts.md` (25 occurrences)
- `reference/stage_10/lessons_learned_examples.md` (12 occurrences)
- + 5 other files

**Impact:** Agents searching for `- [ ]` patterns would miss these checklist items

**Fix Applied:** Python bulk replacement (see Pattern 1 above)

**Prevention:** Run D14 check after every content paste from external source

---

### Example 2: Smart Quotes in Error Messages

**Issue:** File contains `"Use the correct format"` (curly quotes) instead of `"Use the correct format"` (straight quotes)

**Why it matters:** When agents try to grep for the string or match it in code examples, curly quotes won't match straight-quote patterns

**Fix:** Run Pattern 2 bulk replacement

---

## Integration with Other Dimensions

| Dimension | Relationship |
|-----------|-------------|
| **D10: Intra-File Consistency** | D10 catches mixed notation/terminology; D14 catches character-level encoding issues. Both are structural. |
| **D8: Documentation Quality** | D8 checks for incomplete/placeholder content; D14 checks for unparseable character formats. |
| **D12: Structural Patterns** | D12 verifies high-level structure; D14 verifies lowest-level character compliance. |

**Recommended execution order in Sub-Round N.3:** D11 → D14 → D12 → D10 → D13

---

## Pre-Audit Script Integration

**Add to `scripts/pre_audit_checks.sh`:**

```bash
# === D14: Character and Format Compliance ===
echo ""
echo "=== Character and Format Compliance (D14) ==="

python3 -c "
import glob, sys, os

base = '.'
exclude = ['audit/round_', 'audit/outputs/']
banned = {
    '\u25a1': ('□', 'U+25A1 WHITE SQUARE'),
    '\u2610': ('☐', 'U+2610 BALLOT BOX'),
    '\u2611': ('☑', 'U+2611 BALLOT BOX WITH CHECK'),
    '\u2612': ('☒', 'U+2612 BALLOT BOX WITH X'),
    '\u201c': ('\u201c', 'U+201C LEFT DOUBLE QUOTE'),
    '\u201d': ('\u201d', 'U+201D RIGHT DOUBLE QUOTE'),
    '\u2018': ('\u2018', 'U+2018 LEFT SINGLE QUOTE'),
    '\u2019': ('\u2019', 'U+2019 RIGHT SINGLE QUOTE'),
}

files = [f for f in glob.glob('**/*.md', recursive=True)
         if not any(ex in f for ex in exclude)]

total = 0
for fpath in sorted(files):
    with open(fpath, encoding='utf-8') as f:
        content = f.read()
    for char, (display, name) in banned.items():
        count = content.count(char)
        if count > 0:
            print(f'❌ BANNED CHAR {name}: {count} occurrence(s) in {fpath}')
            total += count

if total == 0:
    print('✅ PASS: No banned characters found')
else:
    print(f'Found {total} banned character(s) - run fix from d14_character_format_compliance.md')
    sys.exit(1)
" 2>/dev/null || true
```

---

## Summary

**D14: Character and Format Compliance ensures agents can reliably read and parse guide content.**

**Key Validations:**
1. ✅ No Unicode checkbox chars (□ ☐ ☑ ☒) — use `- [ ]` / `- [x]` instead
2. ✅ No Unicode quote chars (" " ' ') — use straight ASCII quotes instead
3. ⚠️ Review em/en dashes (– —) — acceptable in prose, not in code/lists
4. ✅ Box-drawing chars allowed only in diagrams, not as prose list markers

**Automation: 95%**
- Highly automated for character detection and replacement
- Manual review needed for em-dash context (prose vs non-prose)

**Critical for:**
- Ensuring agents can parse checklist items with standard patterns
- Preventing invisible task tracking failures from Unicode vs ASCII checkboxes
- Catching copy-paste contamination from external documents early

**Sub-Round:** N.3 (Structural Dimensions) alongside D10, D11, D12, D13

---

**Last Updated:** 2026-02-19
**Version:** 1.0
**Status:** ✅ Fully Implemented
