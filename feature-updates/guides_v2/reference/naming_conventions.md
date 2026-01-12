# Naming Conventions & Hierarchical Notation Guide

**Purpose:** Reference guide for agents creating or updating workflow guides
**Use Case:** Ensure consistent file naming, header formatting, and cross-references
**Last Updated:** 2026-01-11

---

## Overview

The Epic-Driven Development Workflow v2 uses a **4-level hierarchical notation system** for organizing guides. This document defines the naming rules, file structure conventions, and formatting standards that ALL guides must follow.

**Why This Matters:**
- **Consistency:** Users and agents can predict file locations and naming patterns
- **Scalability:** New guides can be added without breaking existing structure
- **Navigation:** Clear hierarchy enables easier guide discovery and cross-referencing
- **Maintainability:** Renaming/restructuring is easier when rules are explicit

---

## Table of Contents

1. [Hierarchical Notation System](#hierarchical-notation-system)
2. [File Naming Conventions](#file-naming-conventions)
3. [Directory Structure Rules](#directory-structure-rules)
4. [Header Formatting Standards](#header-formatting-standards)
5. [Cross-Reference Formatting](#cross-reference-formatting)
6. [Level Terminology](#level-terminology)
7. [Examples from Actual Guides](#examples-from-actual-guides)
8. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
9. [Quick Reference Table](#quick-reference-table)

---

## Hierarchical Notation System

### The 4-Level System

| Level | Notation | Format | Example | Description | Terminology |
|-------|----------|--------|---------|-------------|-------------|
| **Level 1** | X | Single number | `5` | Top-level workflow stage | **Stage** |
| **Level 2** | X.Y | Two numbers | `5.1` | Major subdivision within stage | **Phase** |
| **Level 3** | X.Y.Z | Three numbers | `5.1.3` | Focused guide within phase | **Part** |
| **Level 4** | X.Y.Z.W | Four numbers | `5.1.3.2` | Detailed task/iteration | **Step** |

### Notation Rules

**Rule 1: Levels are dot-separated decimals**
- ✅ Correct: `5.1`, `5.1.3`, `5.1.3.2`
- ❌ Wrong: `5a`, `5-1`, `5_1`, `STAGE_5a`

**Rule 2: Each level increases by whole numbers**
- ✅ Correct: `5.1`, `5.2`, `5.3`
- ❌ Wrong: `5.1`, `5.1a`, `5.1b`

**Rule 3: Lower levels inherit from upper levels**
- `5.1.1` is a Part within Phase `5.1`
- `5.1.3.2` is a Step within Part `5.1.3`
- Cannot have `5.1.3.2` without `5.1.3` existing

**Rule 4: Use minimum levels needed**
- If a Stage has no Phases, just use `Stage 5` (not `Stage 5.0`)
- If a Phase has no Parts, just use `Phase 5.1` (not `Phase 5.1.0`)

---

## File Naming Conventions

### Pattern Rules

**Format:** `{level_prefix}_{notation}_{descriptive_name}.md`

| Level | Prefix | Example Filename | Pattern |
|-------|--------|------------------|---------|
| **Stage** | `stage` | `epic_planning.md` | `{descriptive_name}.md` (no notation) |
| **Phase** | `phase` | `phase_5.1_implementation_planning.md` | `phase_{X.Y}_{name}.md` |
| **Part** | `part` | `part_5.1.3_round3.md` | `part_{X.Y.Z}_{name}.md` |
| **Step** | `5.{Y}.{Z}.{W}` | `5.1.3.2_gates_1_2.md` | `{X.Y.Z.W}_{name}.md` |

### Specific Rules

**Rule 1: Stage files (Level 1) - No notation prefix**
- ✅ Correct: `epic_planning.md`, `epic_cleanup.md`
- ❌ Wrong: `stage_1_epic_planning.md`, `1_epic_planning.md`
- **Why:** Stage files are top-level, notation is implicit from directory location (`stages/stage_1/`)

**Rule 2: Phase files (Level 2) - Include notation**
- ✅ Correct: `phase_5.1_implementation_planning.md`
- ❌ Wrong: `implementation_planning.md`, `phase_5a_implementation.md`
- **Why:** Phases need explicit notation to show position within Stage

**Rule 3: Part files (Level 3) - Include notation**
- ✅ Correct: `part_5.1.3_round3.md`
- ❌ Wrong: `round3.md`, `part_5ac_round3.md`
- **Why:** Parts need notation to show position within Phase

**Rule 4: Step files (Level 4) - Full notation, no prefix**
- ✅ Correct: `5.1.3.2_gates_1_2.md`
- ❌ Wrong: `step_5.1.3.2_gates.md`, `gates_1_2.md`
- **Why:** Full notation at this level is already self-documenting

**Rule 5: Descriptive names use snake_case**
- ✅ Correct: `epic_smoke_testing.md`, `cross_feature_sanity_check.md`
- ❌ Wrong: `Epic-Smoke-Testing.md`, `CrossFeatureSanityCheck.md`, `epic smoke testing.md`
- **Why:** Consistent with project-wide file naming standards

**Rule 6: Use underscores to separate notation from name**
- ✅ Correct: `phase_5.1_implementation_planning.md`
- ❌ Wrong: `phase_5.1-implementation-planning.md`, `phase5.1_implementation.md`
- **Why:** Clear visual separation between notation and description

---

## Directory Structure Rules

### Standard Hierarchy

```
feature-updates/guides_v2/
├── stages/
│   ├── stage_1/
│   │   └── epic_planning.md                    (Level 1: Stage)
│   ├── stage_2/
│   │   ├── feature_deep_dive.md                (Level 1: Stage, router)
│   │   ├── phase_2.1_research.md               (Level 2: Phase)
│   │   ├── phase_2.2_specification.md          (Level 2: Phase)
│   │   └── phase_2.3_refinement.md             (Level 2: Phase)
│   ├── stage_5/
│   │   ├── feature_implementation.md           (Level 1: Stage, router)
│   │   ├── phase_5.1_implementation_planning.md (Level 2: Phase, router)
│   │   ├── phase_5.3_post_implementation.md    (Level 2: Phase, router)
│   │   ├── part_5.1.1_round1.md                (Level 3: Part)
│   │   ├── part_5.1.3_round3.md                (Level 3: Part, router)
│   │   ├── iterations/
│   │   │   ├── 5.1.3.1_preparation.md          (Level 4: Step)
│   │   │   └── 5.1.3.2_gates_1_2.md            (Level 4: Step)
│   │   └── ...
│   ├── stage_6/
│   │   ├── epic_final_qc.md                    (Level 1: Stage, router)
│   │   ├── phase_6.1_epic_smoke_testing.md     (Level 2: Phase)
│   │   └── ...
│   └── stage_7/
│       └── epic_cleanup.md                      (Level 1: Stage)
```

### Directory Naming Rules

**Rule 1: Stage directories use `stage_{N}` format**
- ✅ Correct: `stages/stage_1/`, `stages/stage_5/`
- ❌ Wrong: `stages/1/`, `stages/stage_one/`

**Rule 2: Subdirectories for Level 4 files (optional)**
- Create `iterations/` or `steps/` subdirectory when Level 4 files exceed 3-4 files
- ✅ Example: `stages/stage_5/iterations/` contains all `5.1.3.{W}_*.md` files
- **Why:** Keeps parent directory clean, groups related iteration files

**Rule 3: No nested stage directories**
- ❌ Wrong: `stages/stage_5/stage_5a/`
- ✅ Correct: `stages/stage_5/phase_5.1_implementation_planning.md`

---

## Header Formatting Standards

### Markdown Header Hierarchy

**Rule: Header level matches notation level**

| Notation Level | Markdown Header | Example |
|----------------|-----------------|---------|
| **Level 1** | `# Stage {X}:` | `# Stage 5: Feature Implementation` |
| **Level 2** | `## Phase {X.Y}:` | `## Phase 5.1: Implementation Planning` |
| **Level 3** | `### Part {X.Y.Z}:` | `### Part 5.1.3: Round 3` |
| **Level 4** | `#### Step {X.Y.Z.W}:` | `#### Step 5.1.3.2: Gates 1-2` |

### Standard Header Format

**All guide files MUST start with this header structure:**

```markdown
# Stage {X}: {Stage Name}
## Phase {X.Y}: {Phase Name}
### Part {X.Y.Z}: {Part Name}  (if Level 3)

**File:** `{filename}.md`

**Purpose:** {One-line description of what this guide covers}
**Prerequisites:** {Previous phase complete OR specific conditions}
**Next Phase:** `{path/to/next/guide.md}`

---
```

**Examples:**

**Level 1 (Stage) Header:**
```markdown
# Stage 1: Epic Planning

**File:** `epic_planning.md`

**Purpose:** Plan epic scope, break down into features, create folder structure
**Prerequisites:** User created `{epic_name}.txt` with initial requirements
**Next Phase:** `stages/stage_2/feature_deep_dive.md`

---
```

**Level 2 (Phase) Header:**
```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning

**File:** `phase_5.1_implementation_planning.md`

**Purpose:** Create comprehensive implementation plan through 3 rounds (28 iterations)
**Prerequisites:** Stage 2-4 complete (spec, alignment, test strategy approved)
**Next Phase:** `stages/stage_5/phase_5.2_implementation_execution.md`

---
```

**Level 3 (Part) Header:**
```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning
### Part 5.1.3: Round 3 (Iterations 17-25)

**File:** `part_5.1.3_round3.md`

**Purpose:** Router file for Round 3 (Preparation, Gates, GO/NO-GO decision)
**Prerequisites:** Part 5.1.2 complete (Round 2 iterations 8-16)
**Next Phase:** See Quick Navigation table below

---
```

**Level 4 (Step) Header:**
```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning
### Part 5.1.3: Round 3
#### Step 5.1.3.2: Gates 1-2 (Iterations 23, 23a)

**File:** `5.1.3.2_gates_1_2.md`

**Purpose:** Execute Gate 23a (Pre-Implementation Spec Audit - 5 parts)
**Prerequisites:** Step 5.1.3.1 complete (Preparation iterations 17-22)
**Next Step:** `stages/stage_5/iterations/5.1.3.3_gate_3.md`

---
```

### Header Rules

**Rule 1: Always include full hierarchy in headers**
- Level 3 files show: `# Stage 5:` → `## Phase 5.1:` → `### Part 5.1.3:`
- **Why:** Provides context when file is read in isolation

**Rule 2: File field must match actual filename**
- ✅ Correct: `**File:** phase_5.1_implementation_planning.md`
- ❌ Wrong: `**File:** implementation_planning.md`

**Rule 3: Use relative paths for Next Phase/Step**
- ✅ Correct: `stages/stage_5/phase_5.2_implementation_execution.md`
- ❌ Wrong: `phase_5.2_implementation_execution.md` (missing directory)

**Rule 4: Separator line `---` required after header**
- Separates metadata from content
- Provides visual consistency

---

## Cross-Reference Formatting

### Inline References

**Format 1: Notation only** (when context is clear)
```markdown
After completing Phase 5.1, proceed to Phase 5.2.
```

**Format 2: Notation + file link** (when directing to specific guide)
```markdown
See `stages/stage_5/phase_5.2_implementation_execution.md` for execution details.
```

**Format 3: Full descriptive link** (in navigation tables)
```markdown
| Current Phase | Guide to Read | Time |
|---------------|---------------|------|
| Phase 5.1 | `stages/stage_5/phase_5.1_implementation_planning.md` | 3-4 hrs |
```

### Reference Rules

**Rule 1: Use hierarchical notation, not old STAGE_x format**
- ✅ Correct: `Phase 5.1`, `Part 5.1.3`
- ❌ Wrong: `STAGE_5a`, `STAGE_5ac`, `Stage 5a`

**Rule 2: File paths are relative to guides_v2/ directory**
- ✅ Correct: `stages/stage_5/phase_5.1_implementation_planning.md`
- ❌ Wrong: `feature-updates/guides_v2/stages/stage_5/phase_5.1_implementation_planning.md`

**Rule 3: Use backticks for file paths**
- ✅ Correct: `See \`stages/stage_5/part_5.1.3_round3.md\``
- ❌ Wrong: `See stages/stage_5/part_5.1.3_round3.md`

**Rule 4: When referencing a guide, include full path**
- ✅ Correct: `READ: \`stages/stage_5/phase_5.1_implementation_planning.md\``
- ❌ Wrong: `READ: phase_5.1_implementation_planning.md`

---

## Level Terminology

### Correct Terms

| Level | Singular | Plural | Usage Example |
|-------|----------|--------|---------------|
| **Level 1** | Stage | Stages | "Stage 5 has 5 phases" |
| **Level 2** | Phase | Phases | "Phase 5.1 is Implementation Planning" |
| **Level 3** | Part | Parts | "Part 5.1.3 covers Round 3" |
| **Level 4** | Step | Steps | "Step 5.1.3.2 contains Gates 1-2" |

### Terminology Rules

**Rule 1: Use correct level term**
- ✅ Correct: "Phase 5.1", "Part 5.1.3"
- ❌ Wrong: "Stage 5.1", "Phase 5.1.3"

**Rule 2: Capitalize when referring to specific instance**
- ✅ Correct: "Phase 5.1: Implementation Planning"
- ❌ Wrong: "phase 5.1: implementation planning"

**Rule 3: Lowercase when referring generally**
- ✅ Correct: "After completing the phase, proceed to..."
- ❌ Wrong: "After completing the Phase, proceed to..."

**Rule 4: Include name after notation for clarity**
- ✅ Correct: "Phase 5.1 (Implementation Planning)"
- ❌ Wrong: "Phase 5.1" (without name in first mention)

---

## Examples from Actual Guides

### Example 1: Stage File (Level 1)

**File:** `stages/stage_1/epic_planning.md`

```markdown
# Stage 1: Epic Planning

**File:** `epic_planning.md`

**Purpose:** Plan epic scope, break down into features, create folder structure
**Prerequisites:** User created `{epic_name}.txt` with initial requirements
**Next Phase:** `stages/stage_2/feature_deep_dive.md`

---

## Overview

Stage 1 is the initial planning phase where you:
1. Assign KAI number from EPIC_TRACKER.md
2. Analyze epic request and propose feature breakdown
...
```

### Example 2: Phase File (Level 2)

**File:** `stages/stage_5/phase_5.1_implementation_planning.md`

```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning

**File:** `phase_5.1_implementation_planning.md`

**Purpose:** Create comprehensive implementation plan through 3 rounds (28 iterations)
**Prerequisites:** Stage 2-4 complete (spec, alignment, test strategy approved)
**Next Phase:** `stages/stage_5/phase_5.2_implementation_execution.md`

---

## Overview

Phase 5.1 is split into 3 rounds:
- **Part 5.1.1:** Round 1 (Iterations 1-7 + Gates 4a, 7a)
- **Part 5.1.2:** Round 2 (Iterations 8-16)
- **Part 5.1.3:** Round 3 (Iterations 17-25 + Gates 23a, 24, 25)
...
```

### Example 3: Part File (Level 3)

**File:** `stages/stage_5/part_5.1.3_round3.md`

```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning
### Part 5.1.3: Round 3 (Iterations 17-25)

**File:** `part_5.1.3_round3.md`

**Purpose:** Router file for Round 3 (Preparation, Gates, GO/NO-GO decision)
**Prerequisites:** Part 5.1.2 complete (Round 2 iterations 8-16)
**Next Phase:** See Quick Navigation table below

---

## Quick Navigation

**Round 3 is split into 3 parts:**

| Part | Guide to Read | Iterations | Time Estimate |
|------|---------------|------------|---------------|
| Step 5.1.3.1: Preparation | `stages/stage_5/iterations/5.1.3.1_preparation.md` | 17-22 | 45-60 min |
| Step 5.1.3.2: Gates 1-2 | `stages/stage_5/iterations/5.1.3.2_gates_1_2.md` | 23, 23a | 30-45 min |
| Step 5.1.3.3: Gate 3 | `stages/stage_5/iterations/5.1.3.3_gate_3.md` | 24, 25 | 15-30 min |
...
```

### Example 4: Step File (Level 4)

**File:** `stages/stage_5/iterations/5.1.3.2_gates_1_2.md`

```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning
### Part 5.1.3: Round 3
#### Step 5.1.3.2: Gates 1-2 (Iterations 23, 23a)

**File:** `5.1.3.2_gates_1_2.md`

**Purpose:** Execute Gate 23a (Pre-Implementation Spec Audit - 5 parts)
**Prerequisites:** Step 5.1.3.1 complete (Preparation iterations 17-22)
**Next Step:** `stages/stage_5/iterations/5.1.3.3_gate_3.md`

---

## Iteration 23: Integration & Spec Audit Preparation

**Purpose:** Prepare for Gate 23a by reviewing implementation plan and spec...
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Using Old STAGE_x Notation

**Wrong:**
```markdown
After completing STAGE_5a, proceed to STAGE_5b.
See `stages/stage_5/STAGE_5ac_round3.md` for details.
```

**Correct:**
```markdown
After completing Phase 5.1, proceed to Phase 5.2.
See `stages/stage_5/part_5.1.3_round3.md` for details.
```

**Why:** Old notation is deprecated as of 2026-01-10 restructuring.

---

### ❌ Mistake 2: Inconsistent Header Levels

**Wrong:**
```markdown
# Stage 5: Feature Implementation
### Part 5.1.3: Round 3  (skipped Level 2)
```

**Correct:**
```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning
### Part 5.1.3: Round 3
```

**Why:** Must show full hierarchy for context.

---

### ❌ Mistake 3: Wrong File Prefix

**Wrong:**
```markdown
stage_5.1_implementation_planning.md    (using "stage" for Level 2)
5.1_implementation_planning.md          (missing prefix)
implementation_planning.md              (missing notation)
```

**Correct:**
```markdown
phase_5.1_implementation_planning.md
```

**Why:** Level 2 files use `phase_` prefix with full notation.

---

### ❌ Mistake 4: Absolute Paths in Cross-References

**Wrong:**
```markdown
See `C:\Users\...\feature-updates\guides_v2\stages\stage_5\phase_5.1_implementation_planning.md`
See `feature-updates/guides_v2/stages/stage_5/phase_5.1_implementation_planning.md`
```

**Correct:**
```markdown
See `stages/stage_5/phase_5.1_implementation_planning.md`
```

**Why:** Paths are relative to `guides_v2/` directory.

---

### ❌ Mistake 5: Missing Separator After Header

**Wrong:**
```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning

**File:** `phase_5.1_implementation_planning.md`
**Purpose:** Create implementation plan...

## Overview
(no separator line before content)
```

**Correct:**
```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning

**File:** `phase_5.1_implementation_planning.md`
**Purpose:** Create implementation plan...

---

## Overview
```

**Why:** `---` separator provides visual consistency and separates metadata from content.

---

### ❌ Mistake 6: Inconsistent Terminology

**Wrong:**
```markdown
"After completing stage 5.1..." (lowercase when specific)
"Phase 5.1.3" (wrong level term - should be Part)
"Step 5.1" (wrong level term - should be Phase)
```

**Correct:**
```markdown
"After completing Phase 5.1..." (capitalized when specific)
"Part 5.1.3" (correct level term)
"Phase 5.1" (correct level term)
```

**Why:** Consistent terminology prevents confusion about which level is referenced.

---

## Quick Reference Table

### Complete Naming Pattern Reference

| Level | Term | Notation | Prefix | Filename Pattern | Header Format | Example |
|-------|------|----------|--------|------------------|---------------|---------|
| **1** | Stage | X | (none) | `{name}.md` | `# Stage X:` | `epic_planning.md` |
| **2** | Phase | X.Y | `phase_` | `phase_{X.Y}_{name}.md` | `## Phase X.Y:` | `phase_5.1_implementation_planning.md` |
| **3** | Part | X.Y.Z | `part_` | `part_{X.Y.Z}_{name}.md` | `### Part X.Y.Z:` | `part_5.1.3_round3.md` |
| **4** | Step | X.Y.Z.W | (none) | `{X.Y.Z.W}_{name}.md` | `#### Step X.Y.Z.W:` | `5.1.3.2_gates_1_2.md` |

### File Location Patterns

| Level | Directory Location | Example |
|-------|-------------------|---------|
| **Stage** | `stages/stage_{X}/` | `stages/stage_1/epic_planning.md` |
| **Phase** | `stages/stage_{X}/` | `stages/stage_5/phase_5.1_implementation_planning.md` |
| **Part** | `stages/stage_{X}/` | `stages/stage_5/part_5.1.3_round3.md` |
| **Step** | `stages/stage_{X}/iterations/` | `stages/stage_5/iterations/5.1.3.2_gates_1_2.md` |

### Cross-Reference Format Quick Reference

| Reference Type | Format | Example |
|---------------|--------|---------|
| **Notation only** | `{Term} {X.Y}` | `Phase 5.1` |
| **File path** | `` `{relative/path/to/file.md}` `` | `` `stages/stage_5/phase_5.1_implementation_planning.md` `` |
| **Descriptive** | `{Term} {X.Y} ({Name})` | `Phase 5.1 (Implementation Planning)` |
| **Navigation link** | `[{Name}]({path})` | `[Implementation Planning](stages/stage_5/phase_5.1_implementation_planning.md)` |

---

## Validation Checklist

**Use this checklist when creating or updating guides:**

### File Naming
- [ ] File uses correct prefix for level (`phase_`, `part_`, or none)
- [ ] Notation uses dots, not letters (`5.1` not `5a`)
- [ ] Descriptive name uses snake_case
- [ ] Filename matches pattern: `{prefix}_{notation}_{name}.md`

### Header Formatting
- [ ] Headers show full hierarchy (Level 3 shows Stage → Phase → Part)
- [ ] Header levels match notation levels (## for Phase, ### for Part)
- [ ] **File:** field matches actual filename
- [ ] **Purpose:** is one clear sentence
- [ ] **Prerequisites:** lists specific conditions
- [ ] **Next Phase/Step:** includes full relative path
- [ ] Separator `---` appears after header metadata

### Cross-References
- [ ] All references use new notation (no STAGE_x patterns)
- [ ] File paths are relative to `guides_v2/` directory
- [ ] File paths use backticks
- [ ] Terminology matches level (Phase for X.Y, Part for X.Y.Z)

### Content
- [ ] Level terminology is consistent (Stage/Phase/Part/Step)
- [ ] Notation is consistent throughout document
- [ ] Navigation tables (if router file) include file paths and time estimates
- [ ] Examples reference actual workflow patterns

---

## Migration from Old Notation

**If you encounter old notation (STAGE_x format), use these mappings:**

See `reference/glossary.md` → "Deprecated Terms" section for complete mapping table.

**Common migrations:**
- `STAGE_2a` → `Phase 2.1`
- `STAGE_5aa` → `Part 5.1.1`
- `STAGE_5ac` → `Part 5.1.3`
- `Stage 6a` → `Phase 6.1`
- `Stage 7a` → `Phase 7.1`

**File path migrations:**
- `stages/stage_2/phase_0_research.md` → `stages/stage_2/phase_2.1_research.md`
- `stages/stage_5/part_5aa_round1.md` → `stages/stage_5/part_5.1.1_round1.md`

---

## When to Create New Levels

### Adding a New Phase (Level 2)

**Scenario:** Stage has grown complex, needs subdivision

**Steps:**
1. Identify logical break points in current Stage guide
2. Create `phase_{X.Y}_{name}.md` files (e.g., `phase_3.1_initial_alignment.md`, `phase_3.2_conflict_resolution.md`)
3. Convert original Stage file to router (if needed)
4. Update cross-references in related guides
5. Update glossary with new Phase definitions

### Adding a New Part (Level 3)

**Scenario:** Phase is too long (>1000 lines), needs focused guides

**Steps:**
1. Identify natural sub-sections within Phase (e.g., rounds, checkpoints)
2. Create `part_{X.Y.Z}_{name}.md` files
3. Update Phase file to router with Quick Navigation table
4. Update cross-references
5. Consider creating `iterations/` subdirectory if many Part files

### Adding a New Step (Level 4)

**Scenario:** Part needs detailed iteration-by-iteration guides

**Steps:**
1. Create `iterations/` subdirectory under `stages/stage_{X}/`
2. Create `{X.Y.Z.W}_{name}.md` files for each iteration
3. Update Part file (Level 3) to router with iteration breakdown
4. Link iterations in sequence (Next Step fields)

---

## Summary

**Key Takeaways:**
1. **Use hierarchical notation:** X, X.Y, X.Y.Z, X.Y.Z.W (no letters)
2. **Match level terminology:** Stage (1), Phase (2), Part (3), Step (4)
3. **Follow filename patterns:** Correct prefix + notation + snake_case name
4. **Show full hierarchy in headers:** Level 3 shows Stage → Phase → Part
5. **Use relative paths:** From `guides_v2/` directory, with backticks
6. **No old STAGE_x notation:** All references use new hierarchical notation

**For more information:**
- **File structure:** See `README.md` → "Guide Structure"
- **Deprecated terms:** See `reference/glossary.md` → "Deprecated Terms"
- **Examples:** See actual guides in `stages/` directory
- **Troubleshooting:** See `reference/faq_troubleshooting.md`

---

**Last Updated:** 2026-01-11
**Version:** 1.0 (initial creation after 2026-01-10 restructuring)
