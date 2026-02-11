# Naming Conventions & Hierarchical Notation Guide

**Purpose:** Reference guide for agents creating or updating workflow guides
**Use Case:** Ensure consistent file naming, header formatting, and cross-references
**Last Updated:** 2026-01-12

---

## Overview

The Epic-Driven Development Workflow v2 uses a **3-level hierarchical S#.P#.I# notation system** for organizing guides. This document defines the naming rules, file structure conventions, and formatting standards that ALL guides must follow.

**Why This Matters:**
- **Self-Documenting:** Prefixes (S, P, I) make hierarchy level immediately clear
- **Scalability:** New guides can be added without breaking existing structure
- **Navigation:** Clear hierarchy enables easier guide discovery and cross-referencing
- **Maintainability:** Renaming/restructuring is easier when rules are explicit

---

## Table of Contents

1. [S#.P#.I# Notation System](#spi-notation-system)
2. [File Naming Conventions](#file-naming-conventions)
3. [Directory Structure Rules](#directory-structure-rules)
4. [Header Formatting Standards](#header-formatting-standards)
5. [Cross-Reference Formatting](#cross-reference-formatting)
6. [Level Terminology](#level-terminology)
7. [Examples from Actual Guides](#examples-from-actual-guides)
8. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
9. [Quick Reference Table](#quick-reference-table)

---

## S#.P#.I# Notation System

### The 3-Level System

| Level | Notation | Prefix | Example | Description | Terminology |
|-------|----------|--------|---------|-------------|-------------|
| **Level 1** | S# | S | `S5` | Top-level workflow stage | **Stage** |
| **Level 2** | S#.P# | P | `S5.P1` | Major subdivision within stage | **Phase** |
| **Level 3** | S#.P#.I# | I | `S5.P1.I2` | Specific iteration/task within phase | **Iteration** |

**Additional levels within files:**
- **Steps** - Numbered tasks within a guide (Step 1, Step 2, etc.)
- Steps are NOT part of the file naming hierarchy

### Notation Rules

**Rule 1: Prefixes indicate level**
- ✅ Correct: `S5`, `S5.P1`, `S5.P1.I2`
- ❌ Wrong: `5`, `5.1`, `5.1.2` (missing prefixes)
- **Why:** Self-documenting - immediately clear what level you're at

**Rule 2: Use whole numbers only**
- ✅ Correct: `S5.P1`, `S5.P2`, `S5.P3`
- ❌ Wrong: `S5.P1a`, `S5.P1b` (no letter suffixes)

**Rule 3: Lower levels inherit from upper levels**
- `S5.P1.I2` is an Iteration within Phase P1 of S5
- Cannot have `S5.P1.I2` without `S5.P1` existing

**Rule 4: Use minimum levels needed**
- If a Stage has no Phases, just use `S5` (not `S5.P0`)
- If a Phase has no Iterations, just use `S5.P1` (not `S5.P1.I0`)

**Rule 5: Maximum 3 levels for files**
- File names go up to S#.P#.I# only
- Within files, use Steps (not part of file hierarchy)

---

## File Naming Conventions

### Pattern Rules

**Format:** `s{N}_p{M}_i{K}_{descriptive_name}.md` (adjust based on level)

| Level | Pattern | Example Filename |
|-------|---------|------------------|
| **Stage** | `s{N}_{name}.md` | `s1_epic_planning.md` |
| **Phase** | `s{N}_p{M}_{name}.md` | `s2_p2_specification.md` |
| **Iteration** | `s{N}_p{M}_i{K}_{name}.md` | *(deprecated - S5 v2 uses single comprehensive file)* |

**Note:** S5 v2 replaces the iteration-based structure with a single comprehensive Validation Loop guide (`s5_v2_validation_loop.md`). See `reference/stage_5/s5_v2_quick_reference.md` for details.

### Specific Rules

**Rule 1: Stage files (Level 1) - Single prefix**
- ✅ Correct: `s1_epic_planning.md`, `s10_epic_cleanup.md`
- ❌ Wrong: `stage_1_epic_planning.md`, `1_epic_planning.md`
- **Why:** Lowercase 's' prefix is concise and consistent

**Rule 2: Phase files (Level 2) - Stage + Phase prefix**
- ✅ Correct: `s5_v2_validation_loop.md`, `s2_p2_specification.md`
- ❌ Wrong: `s5_planning_round1.md` (missing p1), `phase_5.1_planning.md` (old notation)
- **Why:** Shows exactly where in hierarchy (S5, Phase 1)

**Rule 3: Iteration files (Level 3) - Stage + Phase + Iteration prefix** *(deprecated)*
- **Note:** S5 v2 no longer uses iteration files. For historical reference:
  - ✅ Was correct: `s5_p1_i2_algorithms.md`, `s5_p3_i1_preparation.md`
  - ❌ Was wrong: `s5_algorithms.md` (missing p and i), `s5_p1_2_algorithms.md` (wrong format)
- **Current:** See `reference/stage_5/s5_v2_quick_reference.md`

**Rule 4: Descriptive names use snake_case**
- ✅ Correct: `epic_smoke_testing.md`, `cross_feature_sanity_check.md`
- ❌ Wrong: `Epic-Smoke-Testing.md`, `CrossFeatureSanityCheck.md`
- **Why:** Consistent with project-wide file naming standards

**Rule 5: Use underscores to separate parts**
- ✅ Correct: `s2_p2_specification.md`
- ❌ Wrong: `s2-p2-specification.md`, `s2p2_specification.md`
- **Why:** Clear visual separation between notation and description

**Rule 6: Special case - Phase number variants**
- For S2.P2.5 style numbering: `s2_p2_5_spec_validation.md`
- ✅ Correct: `s2_p2_5_spec_validation.md`
- ❌ Wrong: `s2_p2.5_spec_validation.md` (dot in filename)

---

## Directory Structure Rules

### Standard Hierarchy

```text
feature-updates/guides_v2/
├── stages/
│   ├── s1/
│   │   └── s1_epic_planning.md                    (Level 1: Stage)
│   ├── s2/
│   │   ├── s2_feature_deep_dive.md                (Level 1: Stage, router)
│   │   ├── s2_p1_spec_creation_refinement.md                      (Level 2: Phase)
│   │   ├── s2_p2_specification.md                 (Level 2: Phase)
│   │   ├── s2_p2_5_spec_validation.md             (Level 2: Phase variant)
│   │   └── s2_p3_refinement.md                    (Level 2: Phase)
│   ├── s3/
│   │   └── s3_epic_planning_approval.md       (Level 1: Stage)
│   ├── s4/
│   │   └── s4_epic_testing_strategy.md            (Level 1: Stage)
│   ├── s5/
│   │   ├── s5_v2_validation_loop.md               (Level 2: Primary guide - Draft + Validation Loop)
│   │   ├── validation_loop_qc_pr.md               (Support doc - QC/PR template)
│   │   ├── s5_bugfix_workflow.md                  (Support doc - Bugfix workflow)
│   │   ├── S5_V1_TO_V2_MIGRATION.md               (Archive - Migration notes)
│   │   ├── S5_V2_DESIGN_PLAN.md                   (Archive - Design rationale)
│   │   └── s5_update_notes.md                     (Archive - Update tracking)
│   ├── s6/
│   │   └── s6_execution.md                         (Level 1: Stage)
│   ├── s7/
│   │   ├── s7_p1_smoke_testing.md                  (Level 2: Phase)
│   │   ├── s7_p2_qc_rounds.md                      (Level 2: Phase)
│   │   └── s7_p3_final_review.md                   (Level 2: Phase)
│   ├── s8/
│   │   ├── s8_p1_cross_feature_alignment.md        (Level 2: Phase)
│   │   └── s8_p2_epic_testing_update.md            (Level 2: Phase)
│   ├── s9/
│   │   ├── s9_epic_final_qc.md                     (Level 1: Stage, router)
│   │   ├── s9_p1_epic_smoke_testing.md             (Level 2: Phase)
│   │   ├── s9_p2_epic_qc_rounds.md                 (Level 2: Phase)
│   │   ├── s9_p3_user_testing.md                   (Level 2: Phase)
│   │   └── s9_p4_epic_final_review.md              (Level 2: Phase)
│   └── s10/
│       ├── s10_epic_cleanup.md                     (Level 1: Stage)
│       └── s10_p1_guide_update_workflow.md         (Level 2: Phase)
```

### Directory Naming Rules

**Rule 1: Stage directories use `s{N}/` format**
- ✅ Correct: `stages/s1/`, `stages/s5/`
- ❌ Wrong: `stages/stage_1/`, `stages/1/`
- **Why:** Concise and consistent with file naming

**Rule 2: Flat structure within stage directories**
- All files for a stage (including phases and iterations) go directly in `s{N}/` directory
- ✅ Example: `stages/s5/s5_v2_validation_loop.md` (not nested)
- **Why:** Keeps structure simple, file names show full hierarchy

**Rule 3: No subdirectories within stage folders**
- ❌ Wrong: `stages/s5/p1/`, `stages/s5/iterations/`
- ✅ Correct: All files flat in `stages/s5/`
- **Why:** File naming already shows hierarchy, no need for nested folders

---

## Header Formatting Standards

### Markdown Header Hierarchy

**Rule: Header level matches notation level**

| Notation Level | Markdown Header | Example |
|----------------|-----------------|---------|
| **Level 1** | `# S{N}:` | `# S5: Feature Implementation` |
| **Level 2** | `## S{N}.P{M}:` | `## S5.P1: Planning Round 1` |
| **Level 3** | `### S{N}.P{M}.I{K}:` | `### S5.P1.I2: Algorithms` |
| **Within file** | `#### Step {X}:` | `#### Step 3: Create Test Plan` |

### Standard Header Format

**All guide files MUST start with this header structure:**

```markdown
## S{N}: {Stage Name}
## S{N}.P{M}: {Phase Name}  (if Level 2)
### S{N}.P{M}.I{K}: {Iteration Name}  (if Level 3)

**File:** `{filename}.md`

**Purpose:** {One-line description of what this guide covers}
**Prerequisites:** {Previous phase complete OR specific conditions}
**Next Guide:** `{path/to/next/guide.md}`

---
```

**Examples:**

**Level 1 (Stage) Header:**
```markdown
## S1: Epic Planning

**File:** `s1_epic_planning.md`

**Purpose:** Plan epic scope, break down into features, create folder structure
**Prerequisites:** User created `{epic_name}.txt` with initial requirements
**Next Guide:** `stages/s2/s2_feature_deep_dive.md`

---
```

**Level 2 (Phase) Header:**
```markdown
## S5: Feature Implementation
## S5.P1: Planning Round 1

**File:** `s5_v2_validation_loop.md`

**Purpose:** Execute iterations 1-7 with requirement reviews and algorithm design
**Prerequisites:** S2-S4 complete (spec, alignment, test strategy approved)
**Next Guide:** `stages/s5/s5_v2_validation_loop.md`

---
```

**Level 3 (Iteration) Header:** *(deprecated - no longer used in v2 workflow)*

**Note:** The iteration-based structure (S#.P#.I#) was deprecated with S5 v2. Historical example:

```markdown
## S5: Feature Implementation (HISTORICAL - S5 v1)
## S5.P1: Planning Round 1
### S5.P1.I2: Algorithms

**File:** `s5_p1_i2_algorithms.md`
**Purpose:** Design core algorithms
**Prerequisites:** S5.P1.I1 complete
**Next Guide:** `stages/s5/s5_p1_i3_integration.md`
```

**Current S5 v2:** Uses single comprehensive `s5_v2_validation_loop.md` file. See `reference/stage_5/s5_v2_quick_reference.md`.

### Header Rules

**Rule 1: Always include full hierarchy in headers**
- Level 3 files show: `# S5:` → `## S5.P1:` → `### S5.P1.I2:`
- **Why:** Provides context when file is read in isolation

**Rule 2: File field must match actual filename**
- ✅ Correct: `**File:** s5_v2_validation_loop.md`
- ❌ Wrong: `**File:** planning_round1.md`

**Rule 3: Use relative paths for Next Guide**
- ✅ Correct: `stages/s5/s5_v2_validation_loop.md`
- ❌ Wrong: `s5_v2_validation_loop.md` (missing directory)

**Rule 4: Separator line `---` required after header**
- Separates metadata from content
- Provides visual consistency

---

## Cross-Reference Formatting

### Inline References

**Format 1: Notation only** (when context is clear)
```markdown
After completing S5.P1, proceed to S5.P2.
```

**Format 2: Notation + file link** (when directing to specific guide)
```markdown
See `stages/s6/s6_execution.md` for execution details.
```

**Format 3: Full descriptive link** (in navigation tables)
```markdown
| Current Phase | Guide to Read | Time |
|---------------|---------------|------|
| S5.P1 | `stages/s5/s5_v2_validation_loop.md` | 90 min |
```

### Reference Rules

**Rule 1: Use S#.P#.I# notation consistently**
- ✅ Correct: `S5.P1`, `S5.P1.I2`
- ❌ Wrong: `S5 Phase 1`, `S5.P1`, `5.1` (without prefix)

**Rule 2: File paths are relative to guides_v2/ directory**
- ✅ Correct: `stages/s5/s5_v2_validation_loop.md`
- ❌ Wrong: `feature-updates/guides_v2/stages/s5/s5_v2_validation_loop.md`

**Rule 3: Use backticks for file paths**
- ✅ Correct: `See \`stages/s5/s5_v2_validation_loop.md\``
- ❌ Wrong: `See stages/s5/s5_v2_validation_loop.md`

**Rule 4: When referencing a guide, include full path**
- ✅ Correct: `READ: \`stages/s5/s5_v2_validation_loop.md\``
- ❌ Wrong: `READ: s5_v2_validation_loop.md`

---

## Level Terminology

### Correct Terms

| Level | Singular | Plural | Usage Example | Reserved For |
|-------|----------|--------|---------------|--------------|
| **Level 1** | Stage | Stages | "S2 has 2 phases" | S# hierarchy only |
| **Level 2** | Phase | Phases | "S5.P1 is Planning Round 1" | S#.P# hierarchy only |
| **Level 3** | Iteration | Iterations | "S5.P1.I2 covers algorithms" | S#.P#.I# hierarchy only |
| **Within file** | Step | Steps | "Step 3: Create test plan" | Guide content only |

### Terminology Rules

**Rule 1: Reserve Stage/Phase/Iteration for S#.P#.I# notation ONLY**
- ✅ Correct: "Complete S5.P1 (Planning Round 1)"
- ❌ Wrong: "At this point in the process" (use "at this point")
- ❌ Wrong: "Phase the work carefully" (use "sequence" or "organize")

**Rule 2: Use alternative terms for casual usage**
- Instead of "this stage" → use "this guide", "this section", "this point"
- Instead of "phase" (verb) → use "organize", "sequence", "plan"
- Instead of "iterative" → use "repeated", "continuous", "incremental"

**Rule 3: Capitalize when referring to specific instance**
- ✅ Correct: "S5.P1: Planning Round 1"
- ❌ Wrong: "s5.p1: planning round 1"

**Rule 4: Lowercase when referring generally**
- ✅ Correct: "After completing the phase, proceed to..."
- ❌ Wrong: "After completing the Phase, proceed to..."

---

## Examples from Actual Guides

### Example 1: Stage File (Level 1)

**File:** `stages/s1/s1_epic_planning.md`

```markdown
## S1: Epic Planning

**File:** `s1_epic_planning.md`

**Purpose:** Plan epic scope, break down into features, create folder structure
**Prerequisites:** User created `{epic_name}.txt` with initial requirements
**Next Guide:** `stages/s2/s2_feature_deep_dive.md`

---

## Overview

S1 is the initial planning section where you:
1. Assign KAI number from EPIC_TRACKER.md
2. Analyze epic request and propose feature breakdown
...
```

### Example 2: Phase File (Level 2)

**File:** `stages/s5/s5_v2_validation_loop.md`

```markdown
## S5: Feature Implementation
## S5.P1: Planning Round 1 (Iterations 1-7)

**File:** `s5_v2_validation_loop.md`

**Purpose:** Execute iterations 1-7 with requirement reviews and algorithm design
**Prerequisites:** S2-S4 complete (spec, alignment, test strategy approved)
**Next Guide:** `stages/s5/s5_v2_validation_loop.md`

---

## Overview

S5.P1 is split into 3 iteration groups:
- **S5.P1.I1:** Requirements (Iterations 1-3)
- **S5.P1.I2:** Algorithms (Iterations 4-6 + Gate 4a)
- **S5.P1.I3:** Integration (Iteration 7 + Gate 7a)
...
```

### Example 3: Iteration File (Level 3) - DEPRECATED

**Note:** Iteration files (Level 3) are no longer used in v2 workflow. This example is historical only.

**Historical S5 v1 Example:**
```markdown
## S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I2: Algorithms

**File:** `s5_p1_i2_algorithms.md`
**Purpose:** Design core algorithms
**Prerequisites:** S5.P1.I1 complete
**Next Guide:** `stages/s5/s5_p1_i3_integration.md`
```

**Current S5 v2:** Uses comprehensive Validation Loop (`s5_v2_validation_loop.md`). See `reference/stage_5/s5_v2_quick_reference.md`.

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Using Old Notation

**Wrong:**
```markdown
After completing S5, proceed to S6.
See `stages/s5/phase_5.1_implementation_planning.md` for details.
```

**Correct:**
```markdown
After completing S5.P1, proceed to S5.P2.
See `stages/s5/s5_v2_validation_loop.md` for details.
```

**Why:** Old notation (S5, S5.P1) is deprecated.

---

### ❌ Mistake 2: Missing Prefixes in Notation

**Wrong:**
```markdown
## S5: Feature Implementation
## Phase 1: Planning Round 1  (missing S5)
```

**Correct:**
```markdown
## S5: Feature Implementation
## S5.P1: Planning Round 1
```

**Why:** S#.P#.I# notation requires prefixes for self-documentation.

---

### ❌ Mistake 3: Wrong File Naming Pattern

**Wrong:**
```markdown
stage_5_planning_round1.md       (old format)
s5_planning.md                   (missing p1)
s5-p1-planning.md                (hyphens instead of underscores)
```

**Correct:**
```markdown
s5_v2_validation_loop.md
```

**Why:** Must follow s{N}_p{M}_{name}.md pattern.

---

### ❌ Mistake 4: Absolute Paths in Cross-References

**Wrong:**
```markdown
See `C:\Users\...\feature-updates\guides_v2\stages\s5\s5_v2_validation_loop.md`
See `feature-updates/guides_v2/stages/s5/s5_v2_validation_loop.md`
```

**Correct:**
```markdown
See `stages/s5/s5_v2_validation_loop.md`
```

**Why:** Paths are relative to `guides_v2/` directory.

---

### ❌ Mistake 5: Using Reserved Terms Casually

**Wrong:**
```markdown
"At this point in the process, we organize the work..."
"The repeated approach means..."
```

**Correct:**
```markdown
"At this point in the process, we organize the work..."
"The repeated approach means..."
```

**Why:** Stage/Phase/Iteration reserved for S#.P#.I# hierarchy only.

---

### ❌ Mistake 6: Inconsistent Header Hierarchy

**Wrong:**
```markdown
## S5: Feature Implementation
### S5.P1.I2: Algorithms  (skipped Level 2)
```

**Correct:**
```markdown
## S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I2: Algorithms
```

**Why:** Must show full hierarchy for context.

---

## Quick Reference Table

### Complete Naming Pattern Reference

| Level | Term | Notation | Filename Pattern | Header Format | Example |
|-------|------|----------|------------------|---------------|---------|
| **1** | Stage | S# | `s{N}_{name}.md` | `# S{N}:` | `s1_epic_planning.md` |
| **2** | Phase | S#.P# | `s{N}_p{M}_{name}.md` | `## S{N}.P{M}:` | `s2_p2_specification.md` |
| **3** | Iteration | S#.P#.I# | `s{N}_p{M}_i{K}_{name}.md` | `### S{N}.P{M}.I{K}:` | *(deprecated)* |

### File Location Patterns

| Level | Directory Location | Example |
|-------|-------------------|---------|
| **Stage** | `stages/s{N}/` | `stages/s1/s1_epic_planning.md` |
| **Phase** | `stages/s{N}/` | `stages/s2/s2_p2_specification.md` |
| **Iteration** | `stages/s{N}/` | *(deprecated - no longer used)* |

### Cross-Reference Format Quick Reference

| Reference Type | Format | Example |
|---------------|--------|---------|
| **Notation only** | `S{N}.P{M}` | `S5.P1` |
| **File path** | `` `stages/s{N}/s{N}_p{M}_{name}.md` `` | `` `stages/s5/s5_v2_validation_loop.md` `` |
| **Descriptive** | `S{N}.P{M} ({Name})` | `S5.P1 (Planning Round 1)` |

---

## Validation Checklist

**Use this checklist when creating or updating guides:**

### File Naming
- [ ] File uses s{N}_ or s{N}_p{M}_ or s{N}_p{M}_i{K}_ prefix
- [ ] Notation uses S#.P#.I# format (with prefixes)
- [ ] Descriptive name uses snake_case
- [ ] Filename matches pattern for its level

### Header Formatting
- [ ] Headers show full hierarchy (Level 3 shows S# → S#.P# → S#.P#.I#)
- [ ] Header levels match notation levels (# for S#, ## for S#.P#, ### for S#.P#.I#)
- [ ] **File:** field matches actual filename
- [ ] **Purpose:** is one clear sentence
- [ ] **Prerequisites:** lists specific conditions
- [ ] **Next Guide:** includes full relative path
- [ ] Separator `---` appears after header metadata

### Cross-References
- [ ] All references use S#.P#.I# notation (no old formats)
- [ ] File paths are relative to `guides_v2/` directory
- [ ] File paths use backticks
- [ ] Terminology matches level (Stage for S#, Phase for S#.P#, Iteration for S#.P#.I#)

### Terminology
- [ ] Stage/Phase/Iteration used ONLY for S#.P#.I# hierarchy
- [ ] Casual usage uses alternative terms (guide, section, point, step)
- [ ] Notation is consistent throughout document

---

## When to Create New Levels

### Adding a New Phase (Level 2)

**Scenario:** Stage has grown complex, needs subdivision

**Steps:**
1. Identify logical break points in current Stage guide
2. Create `s{N}_p{M}_{name}.md` files
3. Convert original Stage file to router (if needed)
4. Update cross-references in related guides

### Adding a New Iteration (Level 3)

**Scenario:** Phase is too long (>800 lines), needs focused guides

**Steps:**
1. Identify natural sub-sections within Phase
2. Create `s{N}_p{M}_i{K}_{name}.md` files
3. Update Phase file to router with Quick Navigation table
4. Update cross-references

### Adding Steps Within a Guide

**Scenario:** Guide needs sequential numbered tasks

**Format:**
```markdown
## Step 1: Initialize Feature Folder
## Step 2: Create Specification Document
## Step 3: Review Prerequisites
```

**Note:** Steps are content organization, NOT part of file naming hierarchy

---

## Summary

**Key Takeaways:**
1. **Use S#.P#.I# notation:** Self-documenting with prefixes (S, P, I)
2. **Match level terminology:** Stage (S#), Phase (S#.P#), Iteration (S#.P#.I#)
3. **Follow filename patterns:** `s{N}_p{M}_i{K}_{name}.md` based on level
4. **Show full hierarchy in headers:** Level 3 shows S# → S#.P# → S#.P#.I#
5. **Use relative paths:** From `guides_v2/` directory, with backticks
6. **Reserve terminology:** Stage/Phase/Iteration for hierarchy only

**For more information:**
- **File structure:** See `README.md` → "Guide Structure"
- **Terminology:** See `reference/glossary.md`
- **Examples:** See actual guides in `stages/` directory
- **Troubleshooting:** See `reference/faq_troubleshooting.md`

---

**Last Updated:** 2026-01-12
**Version:** 2.0 (S#.P#.I# notation system)
