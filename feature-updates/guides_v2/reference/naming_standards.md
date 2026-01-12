# Naming Standards - Epic Development Workflow v2

## Overview

This document defines the **hierarchical structure** and **naming conventions** for all epic development guides. Understanding this system is critical for navigating guides and maintaining consistency.

---

## Core Principle: Separation of Structure and Content

The workflow uses two independent concepts:

1. **Hierarchical Structure (Levels)** - The positional organization (4 levels max)
2. **Content Naming (Descriptive)** - What we call things at each level (varies by context)

**Example:**
- **Structure:** "6.1.2" is a **Level 3 item** (X.Y.Z format)
- **Content:** "6.1.2" is called "Epic Smoke Testing Execution Task"
- **Key Point:** Level number defines position, name describes content

---

## Hierarchical Structure

### Level Definitions

The workflow supports **4 hierarchical levels** using decimal notation:

| Level | Notation | Format | Example | Depth |
|-------|----------|--------|---------|-------|
| **Level 1** | X | Single number | `5` | Shallowest |
| **Level 2** | X.Y | Two numbers | `5.1` | |
| **Level 3** | X.Y.Z | Three numbers | `5.1.3` | |
| **Level 4** | X.Y.Z.W | Four numbers | `5.1.3.2` | Deepest |

### Critical Rules

1. **Maximum 4 levels** - No item can be deeper than X.Y.Z.W
2. **Use only what you need** - Not all stages require all 4 levels
3. **No skipping levels** - Can't go from Level 1 to Level 3 (must have Level 2)
4. **Whole numbers only** - Each position uses integers (1, 2, 3, ...), no decimals within positions

### Examples of Level Usage

**Shallow hierarchy (2 levels):**
```
2 - Feature Deep Dives (Level 1)
  2.1 - Research Phase (Level 2)
  2.2 - Specification Phase (Level 2)
  2.3 - Refinement Phase (Level 2)
```

**Medium hierarchy (3 levels):**
```
5 - Feature Implementation (Level 1)
  5.3 - Post-Implementation (Level 2)
    5.3.1 - Smoke Testing (Level 3)
    5.3.2 - QC Rounds (Level 3)
    5.3.3 - Final Review (Level 3)
```

**Deep hierarchy (4 levels):**
```
5 - Feature Implementation (Level 1)
  5.1 - Implementation Planning (Level 2)
    5.1.3 - Round 3 (Level 3)
      5.1.3.1 - Part 1: Preparation (Level 4)
      5.1.3.2 - Part 2a: Gates 1-2 (Level 4)
      5.1.3.3 - Part 2b: Gate 3 (Level 4)
```

---

## Content Naming

### Principle: Descriptive Names Based on Context

Content names vary by what the item actually is, not by its hierarchical level.

**Common content terms used:**
- **Stage** - Always used for Level 1 (1-7)
- **Phase** - Major functional subdivision (often Level 2)
- **Round** - Iterative cycles (Stage 5.1 uses for Level 3)
- **Part** - Smaller divisions within phases or rounds
- **Task** - Specific work items (Stage 6 uses for Level 3)
- **Step** - Sequential actions (can be various levels)
- **Iteration** - Verification cycles (NOT part of hierarchy - see below)
- **Gate** - Quality checkpoints (NOT part of hierarchy - see below)

### Level 1 Content Naming

**Always called "Stage X":**
```
1 - Epic Planning
2 - Feature Deep Dives
3 - Cross-Feature Sanity Check
4 - Epic Testing Strategy
5 - Feature Implementation
6 - Epic-Level Final QC
7 - Epic Cleanup
```

### Level 2-4 Content Naming (Contextual)

Content names at deeper levels are **contextual** - chosen based on what makes sense:

| Stage | L2 Name | L3 Name | L4 Name | Notes |
|-------|---------|---------|---------|-------|
| 2 | Phase | - | - | Only uses 2 levels |
| 3 | - | - | - | Only uses 1 level |
| 4 | - | - | - | Only uses 1 level |
| 5.1 | Phase | Part (Round) | Part subdivision | Uses all 4 levels for Round 3 |
| 5.2 | Phase | - | - | Only uses 2 levels |
| 5.3 | Phase | Part | - | Uses 3 levels |
| 5.4 | Phase | - | - | Only uses 2 levels |
| 5.5 | Phase | - | - | Only uses 2 levels |
| 6.1-6.4 | Phase | Task/Checkpoint | - | Uses 3 levels |
| 7 | - | - | - | Only uses 1 level |
| 7.1 | Phase | - | - | Uses 2 levels |

**Key Insight:** The same Level 3 position might be called:
- "Part 5.1.1" (in Stage 5.1)
- "Part 5.3.1" (in Stage 5.3)
- "Task 6.1.1" (in Stage 6)

All are **Level 3 items**, just named differently based on context.

---

## Special Cases: Non-Hierarchical Elements

### Iterations (Stage 5.1)

**What they are:** Sequential verification tasks within Implementation Planning (28 total)

**NOT part of hierarchy:** Iterations are documented task lists within Level 3/4 items

**Example:**
```
5.1.1 - Round 1 (Level 3 item)
  Contains: Iterations 1, 2, 3, 4, 5, 5a, 6, 7 (plus Gates 4a, 7a)

5.1.3 - Round 3 (Level 3 item)
  5.1.3.1 - Part 1: Preparation (Level 4 item)
    Contains: Iterations 17, 18, 19, 20, 21, 22
```

**Why not hierarchical:** Would create 5-level depth (5.1.1.1 through 5.1.3.3.6), violating 4-level maximum

**How to reference:** "Complete Iteration 23a within Part 5.1.4"

### Gates

**What they are:** Quality checkpoints requiring approval or validation

**NOT part of hierarchy:** Gates occur within hierarchical items

**Two types:**

**Type 1: Stage-Level Gates (User Approval)**
- Gate 3 - After Stage 2 (User approves checklist)
- Gate 4.5 - After Stage 4 (User approves epic test plan)
- Gate 5 - After Stage 5a (User approves implementation plan)

**Type 2: Iteration-Level Gates (Agent Validation)**
- Gate 4a - Within Iteration 4 (Round 1)
- Gate 7a - Within Iteration 7 (Round 1)
- Gate 23a - Within Iteration 23a (Round 3 Part 2a)
- Gate 24 - Within Iteration 24 (Round 3 Part 2b)
- Gate 25 - Within Iteration 25 (Round 3 Part 2b)

**How to reference:** "Gate 23a occurs in Part 5.1.4, Iteration 23a"

---

## Complete Workflow Structure Mapping

### Stage 1: Epic Planning
```
1 (L1)
```
**Levels used:** 1

---

### Stage 2: Feature Deep Dives
```
2 (L1) - Feature Deep Dives
  2.1 (L2) - Phase 2.1: Research
  2.2 (L2) - Phase 2.2: Specification
    (Special: 2.2.5 - Specification Validation checkpoint)
  2.3 (L2) - Phase 2.3: Refinement
```
**Levels used:** 2 (3 for special checkpoint 2.2.5)

---

### Stage 3: Cross-Feature Sanity Check
```
3 (L1)
```
**Levels used:** 1

---

### Stage 4: Epic Testing Strategy
```
4 (L1)
```
**Levels used:** 1

---

### Stage 5: Feature Implementation
```
5 (L1) - Feature Implementation

  5.1 (L2) - Phase 5.1: Implementation Planning
    5.1.1 (L3) - Part 5.1.1: Round 1
      [Contains Iterations 1-9, Gates 4a, 7a]
    5.1.2 (L3) - Part 5.1.2: Round 2
      [Contains Iterations 8-16]
    5.1.3 (L3) - Part 5.1.3: Round 3
      5.1.3.1 (L4) - Part 1: Preparation
        [Contains Iterations 17-22]
      5.1.3.2 (L4) - Part 2a: Gates 1-2
        [Contains Iterations 23, 23a, Gate 23a]
      5.1.3.3 (L4) - Part 2b: Gate 3
        [Contains Iterations 25, 24, Gates 25, 24]

  5.2 (L2) - Phase 5.2: Implementation Execution

  5.3 (L2) - Phase 5.3: Post-Implementation
    5.3.1 (L3) - Part 5.3.1: Smoke Testing
    5.3.2 (L3) - Part 5.3.2: QC Rounds
    5.3.3 (L3) - Part 5.3.3: Final Review

  5.4 (L2) - Phase 5.4: Post-Feature Alignment

  5.5 (L2) - Phase 5.5: Post-Feature Testing Update
```
**Levels used:** 4 (Stage 5.1 Round 3), 3 (Stage 5.3), 2 (others)

---

### Stage 6: Epic-Level Final QC
```
6 (L1) - Epic-Level Final QC

  6.1 (L2) - Phase 6.1: Epic Smoke Testing
    6.1.1 (L3) - Pre-QC Verification
    6.1.2 (L3) - Epic Smoke Testing Execution

  6.2 (L2) - Phase 6.2: Epic QC Rounds
    6.2.1 (L3) - QC Round 1
    6.2.2 (L3) - QC Round 2
    6.2.3 (L3) - QC Round 3

  6.3 (L2) - Phase 6.3: User Testing
    6.3.1 (L3) - User Testing & Bug Fixes

  6.4 (L2) - Phase 6.4: Epic Final Review
    6.4.1 (L3) - Epic PR Review
    6.4.2 (L3) - Validate Against Epic Request
    6.4.3 (L3) - Final Verification
```
**Levels used:** 3

**Note:** Previously called "Steps 1-9", these are Level 3 tasks/checkpoints.

---

### Stage 7: Epic Cleanup
```
7 (L1) - Epic Cleanup
  7.1 (L2) - Phase 7.1: Guide Update Workflow
```
**Levels used:** 2

---

## File Naming Conventions

### General Pattern

Files use hierarchical notation in their names to indicate position:

```
{type}_{notation}_{descriptive_name}.md
```

**Components:**
- **type** - `stage`, `phase`, `part`, `step` (lowercase)
- **notation** - The decimal number (X, X.Y, X.Y.Z, or X.Y.Z.W)
- **descriptive_name** - Snake_case description

### Examples by Level

**Level 1 (Stages):**
```
stages/s1/s1_epic_planning.md
stages/s3/s3_cross_feature_sanity_check.md
```
Format: `{stage_name}.md` (no notation needed, implied by directory)

**Level 2 (Phases):**
```
stages/s2/s2_p1_research.md
stages/s5/s5_p4_execution.md
stages/s7/s7_p1_guide_update_workflow.md
```
Format: `phase_{X.Y}_{name}.md`

**Level 3 (Parts/Tasks):**
```
stages/s5/s5_p1_planning_round1.md
stages/s5/s5_p5_smoke_testing.md
stages/s6/s6_p1_epic_smoke_testing.md
```
Format: `part_{X.Y.Z}_{name}.md` or `phase_{X.Y}_{name}.md` (depending on context)

**Level 4 (Detailed subdivisions):**
```
stages/s5/part_5.1.3.1_round3_part1.md
stages/s5/5.1.3.2_round3_part2a.md
```
Format: `part_{X.Y.Z.W}_{name}.md`

### Router Files

**Router files** point to multiple sub-guides:

```
stages/s2/s2_feature_deep_dive.md (routes to phase_2.1, phase_2.2, phase_2.3)
stages/s5/phase_5.1_implementation_planning.md (routes to parts 5.1.1-5.1.3)
stages/s6/s6_epic_final_qc.md (routes to phases 6.1-6.4)
```

Format: Use the parent item's name (without subdivisions listed)

### Support/Reference Files

Files that aren't part of the main workflow hierarchy use **descriptive names only** (no notation):

```
stages/s5/s5_bugfix_workflow.md
stages/s5/s5_pr_review_protocol.md
reference/common_mistakes.md
reference/glossary.md
debugging/debugging_protocol.md
```

---

## Header Format in Files

### Markdown Headers

Use hierarchy levels to structure headers within guide files:

```markdown
# Stage {X}: {Name}              ← Level 1 (H1)
## Phase {X.Y}: {Name}           ← Level 2 (H2)
### Part {X.Y.Z}: {Name}         ← Level 3 (H3)
#### Item {X.Y.Z.W}: {Name}      ← Level 4 (H4)
```

### Examples

```markdown
# Stage 2: Feature Deep Dives
## Phase 2.1: Research Phase
### Step 1: Epic Intent Extraction
```

```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning
### Part 5.1.3: Round 3
#### Part 5.1.3.1: Preparation (Iterations 17-22)
```

```markdown
# Stage 6: Epic-Level Final QC
## Phase 6.2: Epic QC Rounds
### 6.2.1: QC Round 1 (Cross-Feature Integration)
```

---

## Cross-Reference Format

### In Documentation

**Format:** Use notation with descriptive name for clarity

```
"See Phase 2.1 (Research Phase)"
"Complete Part 5.1.3 before proceeding to Part 5.1.3.1"
"Gate 23a occurs in Part 5.1.3.2, Iteration 23a"
"Execute task 6.1.1 (Pre-QC verification)"
```

**When brevity needed:**
```
"After completing 5.1.2, proceed to 5.1.3"
"Phases 6.1-6.4 comprise the epic QC workflow"
```

### In Agent Status Sections

```markdown
**Current Position:** Phase 5.1.2 (Implementation Planning - Round 2)
**Current Iteration:** Iteration 12 (within Part 5.1.2)
**Next Action:** Complete Iteration 12, proceed to Iteration 13

**Current Position:** Part 5.3.1 (Smoke Testing)
**Current Test:** Part 3 - E2E Execution
**Next Action:** Fix identified issues, restart from Part 1
```

### In Prompts

```markdown
"I'm starting Phase 2.1 (Research Phase) for feature_01_player_manager.
I've read the complete guide at stages/s2/s2_p1_research.md."

"I've completed Part 5.1.3.2 (Round 3 Part 2a) including Gate 23a.
All 5 parts of the spec audit passed. Proceeding to Part 5.1.3.3."
```

---

## Navigation Aids

### Quick Level Identification

**By notation format:**
- `X` = Level 1 (e.g., `5`)
- `X.Y` = Level 2 (e.g., `5.1`)
- `X.Y.Z` = Level 3 (e.g., `5.1.3`)
- `X.Y.Z.W` = Level 4 (e.g., `5.1.3.2`)

**Count the dots:** Number of dots + 1 = Level number

### Finding Files

**Pattern:** File name contains the notation

```
Looking for Phase 2.1? → Search for "phase_2.1"
Looking for Part 5.1.3? → Search for "part_5.1.3"
Looking for Part 5.1.3.2? → Search for "part_5.1.3.2"
```

### Determining Hierarchy

**From notation alone:**
```
5.1.3.2 is nested under:
  5.1.3 (parent - Level 3)
    5.1 (grandparent - Level 2)
      5 (great-grandparent - Level 1)
```

---

## Common Patterns

### Sibling Items (Same Level)

Items at the same level with same parent:

```
5.1.1, 5.1.2, 5.1.3 are siblings (all Level 3 under 5.1)
6.1, 6.2, 6.3, 6.4 are siblings (all Level 2 under 6)
```

### Parent-Child Relationships

```
5.1 (parent - Level 2)
├── 5.1.1 (child - Level 3)
├── 5.1.2 (child - Level 3)
└── 5.1.3 (child - Level 3)
    ├── 5.1.3.1 (grandchild - Level 4)
    ├── 5.1.3.2 (grandchild - Level 4)
    └── 5.1.3.3 (grandchild - Level 4)
```

### Sequential Workflow

Within a level, items typically execute in numerical order:

```
Phase 2.1 → Phase 2.2 → Phase 2.3
Part 5.1.1 → Part 5.1.2 → Part 5.1.3
Task 6.1.1 → Task 6.1.2 (then move to Phase 6.2)
```

---

## Benefits of This System

### 1. Clear Hierarchy
- Decimal notation immediately shows nesting depth
- 5.1.3.2 is clearly nested 4 levels deep

### 2. Flexible Content Naming
- Level 3 can be a "Part", "Task", "Round" - whatever fits
- Structure (Level) is independent from semantics (name)

### 3. Scalability
- Can add 2.4 (new phase) without renumbering
- Can insert 5.1.6 if needed later

### 4. Self-Documenting
- "5.1.3.2" tells you exactly where it fits in the hierarchy
- File names match notation for easy searching

### 5. Consistent Sorting
- File explorers naturally sort correctly
- 5.1.1, 5.1.2, 5.1.3, 5.1.3.1, 5.1.3.2

### 6. Maximum Depth Control
- 4-level maximum prevents over-fragmentation
- Forces appropriate granularity

### 7. Easy Navigation
- Count dots to know depth
- Parent is always notation with last number removed

---

## Quick Reference Card

### Notation Format
```
Level 1: X           (e.g., 5)
Level 2: X.Y         (e.g., 5.1)
Level 3: X.Y.Z       (e.g., 5.1.3)
Level 4: X.Y.Z.W     (e.g., 5.1.3.2)
```

### File Naming
```
Level 1: {stage_name}.md
Level 2: phase_{X.Y}_{name}.md
Level 3: part_{X.Y.Z}_{name}.md
Level 4: part_{X.Y.Z.W}_{name}.md
```

### Deepest Items by Stage
```
Stage 1: Level 1 (1)
Stage 2: Level 2 (2.3) [plus special 2.2.5]
Stage 3: Level 1 (3)
Stage 4: Level 1 (4)
Stage 5: Level 4 (5.1.3.3)
Stage 6: Level 3 (6.4.3)
Stage 7: Level 2 (7.1)
```

### Content Terms (Contextual)
```
Stage - Always Level 1
Phase - Usually Level 2 (sometimes Level 3 in Stage 6)
Part - Usually Level 3 or Level 4
Round - Level 3 in Stage 5.1
Task/Checkpoint - Level 3 in Stage 6
Iteration - NOT hierarchical (content within Parts)
Gate - NOT hierarchical (checkpoints within items)
```

---

## Migration Notes

### Old Naming → New Naming

**Stage 2:**
```
s2_p1_research.md → s2_p1_research.md
s2_p2_specification.md → s2_p2_specification.md
s2_p3_refinement.md → s2_p3_refinement.md
```

**Stage 5:**
```
s5_p1_planning_round1.md → s5_p1_planning_round1.md
s5_p2_planning_round2.md → s5_p2_planning_round2.md
s5_p3_planning_round3.md → s5_p3_planning_round3.md (router)
5.1.3.2_round3_part2a.md → 5.1.3.2_round3_part2a.md
5.1.3.3_round3_part2b.md → 5.1.3.3_round3_part2b.md

implementation_execution.md → s5_p4_execution.md
smoke_testing.md → s5_p5_smoke_testing.md
qc_rounds.md → s5_p6_qc_rounds.md
final_review.md → s5_p7_final_review.md
post_feature_alignment.md → s5_p8_cross_feature_alignment.md
post_feature_testing_update.md → s5_p9_epic_testing_update.md
```

**Stage 6:**
```
epic_smoke_testing.md → s6_p1_epic_smoke_testing.md
epic_qc_rounds.md → s6_p2_epic_qc_rounds.md
user_testing.md → s6_p3_user_testing.md
epic_final_review.md → s6_p4_epic_final_review.md
```

**Stage 7:**
```
guide_update_workflow.md → s7_p1_guide_update_workflow.md
```

### References to Update

All cross-references in:
- CLAUDE.md
- README.md
- All prompt files
- All guide files
- All reference files
- Templates
- Debugging and missed requirement protocols

---

## Glossary Integration

See `reference/glossary.md` for alphabetical definitions of all content terms (Phase, Round, Part, Iteration, Gate, etc.) and how they map to hierarchical levels in different contexts.

---

**Document Version:** 1.0
**Last Updated:** 2026-01-11
**Status:** ✅ APPROVED - Official naming standard for Epic Development Workflow v2
