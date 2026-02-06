# Issue Classification

**Purpose:** Severity levels and prioritization criteria for audit issues
**Audience:** Agents organizing discovery reports and fix plans (Stages 1-2)
**Last Updated:** 2026-02-05

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Severity Levels](#severity-levels)
3. [Dimension-Specific Classifications](#dimension-specific-classifications)
4. [Prioritization Rules](#prioritization-rules)
5. [Fix Order Guidelines](#fix-order-guidelines)
6. [Classification Examples](#classification-examples)

---

## Quick Reference

### The 4 Severity Levels

| Level | Symbol | Impact | Fix Timing | Examples |
|-------|--------|--------|------------|----------|
| **Critical** | 🔴 | Blocks workflow | Fix FIRST | Broken file paths, CLAUDE.md >40K chars |
| **High** | 🟠 | Causes confusion | Fix SECOND | Old notation, broken templates |
| **Medium** | 🟡 | Cosmetic but important | Fix THIRD | File sizes >1250 lines, missing TOCs |
| **Low** | 🟢 | Nice-to-have | Fix LAST | Minor formatting, spacing |

### Priority Matrix

```text
           High Impact
               │
      Critical │ High
        🔴     │  🟠
        ───────┼───────
      Medium   │ Low
        🟡     │  🟢
               │
           Low Impact
```

---

## Severity Levels

### 🔴 CRITICAL: Blocks Workflow

**Definition:** Issues that prevent agents or users from completing tasks

**Characteristics:**
- **Breaks functionality** - File paths that don't exist, broken links agents must follow
- **Policy violations** - CLAUDE.md exceeds 40,000 character hard limit
- **Template errors** - Errors in templates propagate to ALL new epics
- **Safety issues** - Instructions that could destroy work (incorrect git commands)

**Impact:**
- Agent gets stuck (can't find file to read)
- User can't proceed (workflow instructions broken)
- Cascading failures (one error causes multiple downstream errors)

**Fix Timing:** IMMEDIATELY, before any other issues

**Examples:**
- ❌ `stages/s6/file.md` referenced but file is at `stages/s9/file.md`
- ❌ CLAUDE.md is 45,000 characters (exceeds 40K policy limit)
- ❌ Template has broken file path → All new epics will have broken path
- ❌ Git command says `git reset --hard` without safety check

**How to Identify:**
```text
Ask: "If this isn't fixed, can workflow complete?"
If answer is NO → CRITICAL
```

---

### 🟠 HIGH: Causes Confusion

**Definition:** Issues that don't block workflow but cause significant confusion

**Characteristics:**
- **Inconsistent notation** - Mixed "S5a" and "S5.P1" terminology
- **Outdated references** - Guide references stage that was renumbered
- **Missing required sections** - No Prerequisites section in stage guide
- **Contradictory info** - One guide says X, another says Y

**Impact:**
- Agent unclear which notation to use
- User loses confidence in guides (sees inconsistency)
- Time wasted clarifying ambiguity
- Wrong decisions made based on unclear info

**Fix Timing:** AFTER Critical, BEFORE Medium

**Examples:**
- ⚠️ File uses both "S5a" and "S5.P1" for same concept
- ⚠️ Guide says "Next: S6" but S6 was renumbered to S9
- ⚠️ Stage guide missing "Exit Criteria" section
- ⚠️ One guide says "3 rounds minimum", another says "5 rounds"

**How to Identify:**
```text
Ask: "Will this cause agent or user to be confused?"
If answer is YES + doesn't block → HIGH
```

---

### 🟡 MEDIUM: Cosmetic but Important

**Definition:** Issues that don't cause confusion but reduce guide quality/usability

**Characteristics:**
- **File size issues** - Files >1250 lines (hard to read but not broken)
- **Missing navigation** - No Table of Contents in long file
- **Count inaccuracies** - Says "15 files" but actually 16
- **Formatting inconsistencies** - Headers not following pattern
- **Accessibility issues** - Missing section anchors for links

**Impact:**
- Harder to use guides (navigation difficulty)
- Reduced readability (file too long)
- Minor inaccuracies (counts slightly off)
- Appears unprofessional (formatting inconsistent)

**Fix Timing:** AFTER High, BEFORE Low

**Examples:**
- ⚠️ File is 1,500 lines (exceeds 1250 readability limit)
- ⚠️ File >500 lines has no Table of Contents
- ⚠️ Says "16 dimensions" but actually 17 listed
- ⚠️ Some headers use "##" others use "###" inconsistently

**How to Identify:**
```text
Ask: "Does this reduce quality/usability?"
If answer is YES + no confusion → MEDIUM
```

---

### 🟢 LOW: Nice-to-Have

**Definition:** Minor improvements that don't affect functionality or clarity

**Characteristics:**
- **Minor formatting** - Extra blank lines, trailing spaces
- **Style preferences** - "OK" vs "Okay"
- **Trivial typos** - Misspelled word that's still clear
- **Optional enhancements** - Could add example but not required

**Impact:**
- Minimal to none
- Purely cosmetic
- User unlikely to notice

**Fix Timing:** AFTER all other issues, or defer

**Examples:**
- Minor: Extra blank line between sections
- Minor: "filesystem" vs "file system" (both acceptable)
- Minor: Trailing whitespace at end of line
- Minor: Could add 5th example but 4 is sufficient

**How to Identify:**
```text
Ask: "If this isn't fixed, does anything matter?"
If answer is NO → LOW
```

---

## Dimension-Specific Classifications

### D1: Cross-Reference Accuracy

| Issue Type | Severity | Reason |
|------------|----------|--------|
| Broken file path (workflow guide) | 🔴 CRITICAL | Blocks agent from proceeding |
| Broken file path (example) | 🟠 HIGH | Confusing but doesn't block |
| Broken internal anchor | 🟡 MEDIUM | Navigation impaired |
| Outdated link to renamed file | 🟠 HIGH | Causes confusion |

### D2: Terminology Consistency

| Issue Type | Severity | Reason |
|------------|----------|--------|
| Mixed notation in same file | 🟠 HIGH | Causes confusion |
| Old notation in current content | 🟠 HIGH | Misleading |
| Old notation in historical section (unmarked) | 🟡 MEDIUM | Should be marked historical |
| Inconsistent capitalization | 🟢 LOW | Cosmetic |

### D4: Count Accuracy

| Issue Type | Severity | Reason |
|------------|----------|--------|
| Claims "10 stages" but workflow has 11 | 🟠 HIGH | Misleading count |
| Off-by-one error (says 15, actually 16) | 🟡 MEDIUM | Minor inaccuracy |
| Count in old historical section | 🟢 LOW | Historical reference |

### D5: Content Completeness

| Issue Type | Severity | Reason |
|------------|----------|--------|
| Missing required section (Prerequisites) | 🟠 HIGH | Reduces usability |
| Missing optional section (Examples) | 🟡 MEDIUM | Reduces clarity |
| TODO marker in main content | 🟠 HIGH | Incomplete content |
| TODO marker in template | 🟢 LOW | Placeholder (acceptable) |

### D6: Template Currency

| Issue Type | Severity | Reason |
|------------|----------|--------|
| Template has broken file path | 🔴 CRITICAL | Propagates to all new epics |
| Template has old notation | 🔴 CRITICAL | Propagates to all new epics |
| Template missing new section | 🟠 HIGH | New epics missing content |
| Template formatting outdated | 🟡 MEDIUM | Cosmetic issue |

### D8: CLAUDE.md Sync

| Issue Type | Severity | Reason |
|------------|----------|--------|
| CLAUDE.md >40,000 characters | 🔴 CRITICAL | Policy violation |
| Step numbers don't match guide | 🔴 CRITICAL | Blocks workflow |
| Quick reference outdated | 🟠 HIGH | Causes confusion |
| Minor terminology difference | 🟡 MEDIUM | Slightly inconsistent |

### D10: File Size Assessment

| Issue Type | Severity | Reason |
|------------|----------|--------|
| CLAUDE.md >40K chars | 🔴 CRITICAL | Hard policy limit |
| File >2000 lines | 🟠 HIGH | Severely impacts readability |
| File 1251-1500 lines | 🟡 MEDIUM | Exceeds guideline |
| File 1000-1250 lines | 🟢 LOW | Within acceptable range |

### D13: Documentation Quality

| Issue Type | Severity | Reason |
|------------|----------|--------|
| No TOC in file >1000 lines | 🟠 HIGH | Navigation impaired |
| No TOC in file 500-1000 lines | 🟡 MEDIUM | Should have TOC |
| TODO in main content | 🟠 HIGH | Incomplete |
| TODO in future work section | 🟢 LOW | Planned enhancement |

---

## Prioritization Rules

### Rule 1: Fix by Severity

**Order:**
1. 🔴 All Critical issues
2. 🟠 All High issues
3. 🟡 All Medium issues
4. 🟢 All Low issues (or defer)

**Rationale:** Don't fix cosmetic issues while workflow is broken

---

### Rule 2: Fix by Dependency

**Within same severity, fix in dependency order:**

```text
Example: All 🟠 HIGH issues:

Issue A: Broken file reference in Stage 2 guide
Issue B: Stage 3 guide references Stage 2 content
Issue C: Notation inconsistency in Stage 5

Fix Order:
1. A first (Stage 2 fix enables B verification)
2. B second (depends on A being fixed)
3. C third (independent)
```

**Rule:**
- If Issue B depends on Issue A → Fix A first
- If independent → Fix in any order

---

### Rule 3: Fix by Blast Radius

**Within same severity, fix high-impact first:**

```text
Example: All 🔴 CRITICAL issues:

Issue X: Template has broken path (affects all new epics)
Issue Y: One guide has broken path (affects that guide only)

Fix Order:
1. X first (blast radius: ALL new epics)
2. Y second (blast radius: single guide)
```

**Blast Radius Ranking:**
1. **Templates** - Affects ALL future epics
2. **Root files** (CLAUDE.md, README.md) - Affects ALL users
3. **Core guides** (stages/) - Affects most workflows
4. **Reference files** - Affects specific lookups
5. **Individual guides** - Affects single topic

---

### Rule 4: Fix by Frequency of Access

**Within same severity and blast radius, fix frequently-accessed first:**

**Access Frequency Ranking:**
1. CLAUDE.md (read at start of EVERY task)
2. README.md (entry point)
3. Stage guides (read during workflow)
4. Templates (used when creating new epics)
5. Reference guides (used as needed)
6. Dimension guides (used during audits only)

---

## Fix Order Guidelines

### Example Priority List

**Given these issues discovered:**

| ID | Issue | Dimension | Severity | Blast Radius | Dependency |
|----|-------|-----------|----------|--------------|------------|
| 1 | CLAUDE.md 45K chars | D8, D10 | 🔴 CRITICAL | Root file | None |
| 2 | Template broken path | D6 | 🔴 CRITICAL | All epics | None |
| 3 | Stage 2 broken path | D1 | 🔴 CRITICAL | Single guide | None |
| 4 | Mixed notation S5 guide | D2 | 🟠 HIGH | Single guide | None |
| 5 | File >1500 lines | D10 | 🟡 MEDIUM | Single file | None |
| 6 | Extra blank line | None | 🟢 LOW | Cosmetic | None |

**Fix Order:**
```text
Round 1 (CRITICAL):
1. Issue #1 (CLAUDE.md) - Root file, highest access
2. Issue #2 (Template) - Highest blast radius
3. Issue #3 (Stage 2 path) - Lower blast radius

Round 2 (HIGH):
4. Issue #4 (Mixed notation) - Causes confusion

Round 3 (MEDIUM):
5. Issue #5 (File size) - Reduces readability

Round 4 (LOW) - Optional:
6. Issue #6 (Formatting) - Defer or fix if time permits
```

---

## Classification Examples

### Example 1: File Path Reference

**Discovery:**
```markdown
Guide says: "Read stages/s6/s6_execution.md"
Reality: File is at stages/s9/s9_execution.md
```

**Classification:**
- **Dimension:** D1 (Cross-Reference Accuracy)
- **Severity:** 🔴 CRITICAL (if in workflow guide) OR 🟠 HIGH (if in example)
- **Reason:** Blocks workflow (critical) or confuses user (high)
- **Priority:** Fix in Round 1 (if critical) or Round 2 (if high)

---

### Example 2: Old Notation

**Discovery:**
```markdown
Guide says: "Complete S5a iterations"
Should say: "Complete S5.P1 iterations"
```

**Classification:**
- **Dimension:** D2 (Terminology Consistency)
- **Severity:** 🟠 HIGH
- **Reason:** Causes confusion (what is S5a?)
- **Priority:** Fix in Round 2 (after Critical issues)

**BUT if in historical section:**
```markdown
Historical Note: The old workflow used S5a notation...
```
- **Severity:** 🟢 LOW or INTENTIONAL
- **Reason:** Historical reference (acceptable with marker)

---

### Example 3: File Size

**Discovery:**
```text
File: stages/s5/s5_p1_planning.md
Lines: 1,600 lines
Limit: 1,250 lines
```

**Classification:**
- **Dimension:** D10 (File Size Assessment)
- **Severity:** 🟡 MEDIUM
- **Reason:** Reduces readability, not blocking
- **Priority:** Fix in Round 3 (after High issues)

**Special case - CLAUDE.md:**
```text
File: CLAUDE.md
Characters: 45,000
Limit: 40,000 (HARD POLICY)
```
- **Severity:** 🔴 CRITICAL
- **Reason:** Policy violation
- **Priority:** Fix in Round 1 FIRST

---

### Example 4: Missing TOC

**Discovery:**
```text
File: stages/s5/s5_p1_planning.md
Lines: 800 lines
TOC: Not present
```

**Classification:**
- **Dimension:** D13 (Documentation Quality)
- **Severity:** 🟡 MEDIUM
- **Reason:** Reduces navigation, not confusing
- **Priority:** Fix in Round 3

**But if file is <500 lines:**
- **Severity:** 🟢 LOW
- **Reason:** Optional for shorter files

---

## Decision Tree

```text
Issue Discovered
       ↓
   ┌───┴───┐
   │       │
Blocks?  Confuses?
   │       │
   YES     YES
   ↓       ↓
🔴 CRITICAL 🟠 HIGH
   │       │
   └───┬───┘
       ↓
   Both NO
       ↓
   Reduces Quality?
       │
   ┌───┴───┐
   YES     NO
   ↓       ↓
🟡 MEDIUM 🟢 LOW
```

---

## See Also

- **Stage 1 Discovery:** `stages/stage_1_discovery.md` - When to classify issues
- **Stage 2 Fix Planning:** `stages/stage_2_fix_planning.md` - How to organize by priority
- **Dimension Guides:** `dimensions/d*.md` - Dimension-specific issue types
