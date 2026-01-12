# Guide Structure Refactoring Plan - 2026-01-11

## Problem Statement

Current guides use X.Y.Z.W notation that is:
- **Not intuitive**: Have to count dots to know hierarchy level
- **Abstract**: Numbers don't communicate meaning
- **Inconsistent**: Mix of old notation (STAGE_5aa) and new notation (5.1.3)
- **Too deep**: 4 levels of hierarchy creates complexity

**User feedback:** "I don't really grasp where we are in the process"

## Solution: S#.P#.I# Notation System

**New 3-level self-documenting notation:**
- **S#** = Stage (Level 1) - Top-level workflow phase
- **S#.P#** = Phase (Level 2) - Major subdivision within stage
- **S#.P#.I#** = Iteration (Level 3) - Specific task/step

**Example:** `S5.P2.I8` immediately communicates:
- Stage 5 (Feature Implementation)
- Phase 2 (Planning Round 2)
- Iteration 8 (specific task)

**Key Design Decisions:**
1. **Max 3 levels for files** - No file deeper than S#.P#.I#
2. **Steps within files** - Additional steps are sections/headers, not separate files
3. **Flatten 4th level** - Current Level 4 items promoted or merged
4. **Self-documenting prefixes** - S/P/I make hierarchy immediately clear

---

## Complete Mapping: Current → New

### Stage 1: Epic Planning

**Current:**
```
Stage 1: Epic Planning (single file)
  - stages/stage_1/epic_planning.md
```

**New:**
```
S1: Epic Planning (single file)
  - stages/s1/s1_epic_planning.md
```

**Changes:**
- Rename directory: `stage_1/` → `s1/`
- Rename file: `epic_planning.md` → `s1_epic_planning.md`
- Update header: `# STAGE 1:` → `# S1:`
- No phases needed (single guide)

---

### Stage 2: Feature Deep Dive

**Current:**
```
Stage 2: Feature Deep Dive
  - Phase 2.1: Research
  - Phase 2.2: Specification
  - Phase 2.3: Refinement
```

**New:**
```
S2: Feature Deep Dive
  - S2.P1: Research
  - S2.P2: Specification
  - S2.P3: Refinement
```

**Files:**
- `stages/s2/s2_feature_deep_dive.md` (router/overview)
- `stages/s2/s2_p1_research.md`
- `stages/s2/s2_p2_specification.md`
- `stages/s2/s2_p3_refinement.md`

**Changes:**
- Rename directory: `stage_2/` → `s2/`
- Rename: `phase_2.1_research.md` → `s2_p1_research.md`
- Rename: `phase_2.2_specification.md` → `s2_p2_specification.md`
- Rename: `phase_2.3_refinement.md` → `s2_p3_refinement.md`
- Update all headers and cross-references

---

### Stage 3: Cross-Feature Sanity Check

**Current:**
```
Stage 3: Cross-Feature Sanity Check (single file)
```

**New:**
```
S3: Cross-Feature Sanity Check (single file)
  - stages/s3/s3_cross_feature_sanity_check.md
```

**Changes:**
- Rename directory: `stage_3/` → `s3/`
- Rename file: `cross_feature_sanity_check.md` → `s3_cross_feature_sanity_check.md`
- Update headers
- No phases needed

---

### Stage 4: Epic Testing Strategy

**Current:**
```
Stage 4: Epic Testing Strategy (single file)
```

**New:**
```
S4: Epic Testing Strategy (single file)
  - stages/s4/s4_epic_testing_strategy.md
```

**Changes:**
- Rename directory: `stage_4/` → `s4/`
- Rename file: `epic_testing_strategy.md` → `s4_epic_testing_strategy.md`
- Update headers
- No phases needed

---

### Stage 5: Feature Implementation (MAJOR RESTRUCTURING)

**Current (4 levels - very complex):**
```
Stage 5: Feature Implementation
  Phase 5.1: Implementation Planning
    Part 5.1.1: Round 1 (iterations 1-7 + Gate 4a)
    Part 5.1.2: Round 2 (iterations 8-16)
    Part 5.1.3: Round 3 (iterations 17-28)
      Step 5.1.3.1: Preparation (iterations 17-22)
      Step 5.1.3.2: Gates 1-2 (iterations 23, 23a)
      Step 5.1.3.3: Gate 3 (iterations 24, 25)
  Phase 5.2: Implementation Execution
  Phase 5.3: Post-Implementation
    Part 5.3.1: Smoke Testing
    Part 5.3.2: QC Rounds
    Part 5.3.3: Final Review
  Phase 5.4: Cross-Feature Alignment
  Phase 5.5: Epic Testing Update
```

**New (3 levels with I# file splits):**
```
S5: Feature Implementation
  S5.P1: Planning Round 1 (router)
    → S5.P1.I1: Requirements Analysis (iterations 1-3)
    → S5.P1.I2: Algorithms & Dependencies (iterations 4-6 + Gate 4a)
    → S5.P1.I3: Integration Check (iteration 7)
  S5.P2: Planning Round 2 (router)
    → S5.P2.I1: Test Strategy (iterations 8-10)
    → S5.P2.I2: Re-verification (iterations 11-12)
    → S5.P2.I3: Final Checks (iterations 13-16)
  S5.P3: Planning Round 3 (router)
    → S5.P3.I1: Preparation (iterations 17-22)
    → S5.P3.I2: Gates Part 1 (iterations 23, 23a)
    → S5.P3.I3: Gates Part 2 (iterations 24, 25)
  S9: Execution
  S10.P1: Smoke Testing
  S10.P2: QC Rounds
  S10.P3: Final Review
  S8.P1: Cross-Feature Alignment
  S8.P2: Epic Testing Update
```

**Key Changes:**
1. **Promote Parts to Phases:**
   - Part 5.1.1 → S5.P1
   - Part 5.1.2 → S5.P2
   - Part 5.1.3 → S5.P3
   - Part 5.3.1 → S10.P1
   - Part 5.3.2 → S10.P2
   - Part 5.3.3 → S10.P3

2. **Eliminate 4th level (Steps become I# files):**
   - Step 5.1.3.1 (Preparation) → S5.P3.I1 file
   - Step 5.1.3.2 (Gates 1-2) → S5.P3.I2 file
   - Step 5.1.3.3 (Gate 3) → S5.P3.I3 file

3. **Use I# for file splits within phases:**
   - S5.P1 → Split into 3 I# files (I1: iterations 1-3, I2: iterations 4-6, I3: iteration 7)
   - S5.P2 → Split into 3 I# files (I1: iterations 8-10, I2: iterations 11-12, I3: iterations 13-16)
   - S5.P3 → Split into 3 I# files (I1: iterations 17-22, I2: iterations 23/23a, I3: iterations 24/25)
   - Phase files become routers pointing to I# files

**Files:**
```
stages/s5/
  s5_feature_implementation.md          (main router)

  # Planning Round 1
  s5_p1_planning_round1.md              (phase router)
  s5_p1_i1_requirements.md              (iterations 1-3)
  s5_p1_i2_algorithms.md                (iterations 4-6 + Gate 4a)
  s5_p1_i3_integration.md               (iteration 7)

  # Planning Round 2
  s5_p2_planning_round2.md              (phase router)
  s5_p2_i1_test_strategy.md             (iterations 8-10)
  s5_p2_i2_reverification.md            (iterations 11-12)
  s5_p2_i3_final_checks.md              (iterations 13-16)

  # Planning Round 3
  s5_p3_planning_round3.md              (phase router)
  s5_p3_i1_preparation.md               (iterations 17-22)
  s5_p3_i2_gates_part1.md               (iterations 23, 23a)
  s5_p3_i3_gates_part2.md               (iterations 24, 25)

  # Other phases (single files, no I# splitting needed)
  s5_p4_execution.md
  s5_p5_smoke_testing.md
  s5_p6_qc_rounds.md
  s5_p7_final_review.md
  s5_p8_cross_feature_alignment.md
  s5_p9_epic_testing_update.md
```

**Total: 22 files in s5/ directory**

**Current files to TRANSFORM:**
- `part_5.1.1_round1.md` → `s5_p1_planning_round1.md` (router)
- `5.1.1_iterations_1_3_requirements.md` → `s5_p1_i1_requirements.md`
- `5.1.1_iteration_4_algorithms.md` → `s5_p1_i2_algorithms.md`
- `5.1.1_iterations_5_6_dependencies.md` + `5.1.1_iteration_7_integration.md` → `s5_p1_i3_integration.md`

- `part_5.1.2_round2.md` → `s5_p2_planning_round2.md` (router)
- `5.1.2_iterations_8_10_test_strategy.md` → `s5_p2_i1_test_strategy.md`
- `5.1.2_iterations_11_12_reverification.md` → `s5_p2_i2_reverification.md`
- `5.1.2_iterations_13_16_final_checks.md` → `s5_p2_i3_final_checks.md`

- `part_5.1.3_round3.md` → `s5_p3_planning_round3.md` (router)
- `5.1.3.1_iterations_17_18_phasing.md` + `5.1.3.1_iterations_19_20_algorithms.md` + `5.1.3.1_iterations_21_22_testing.md` → `s5_p3_i1_preparation.md`
- `5.1.3.2_iteration_23_integration.md` + `5.1.3.2_gate_23a_spec_audit.md` → `s5_p3_i2_gates_part1.md`
- `5.1.3.3_iterations_24_25_final.md` → `s5_p3_i3_gates_part2.md`

- `phase_5.2_implementation_execution.md` → `s5_p4_execution.md`
- `part_5.3.1_smoke_testing.md` → `s5_p5_smoke_testing.md`
- `part_5.3.2_qc_rounds.md` → `s5_p6_qc_rounds.md`
- `part_5.3.3_final_review.md` → `s5_p7_final_review.md`
- `phase_5.4_post_feature_alignment.md` → `s5_p8_cross_feature_alignment.md`
- `phase_5.5_post_feature_testing_update.md` → `s5_p9_epic_testing_update.md`

**Files to DELETE:**
- `phase_5.1_implementation_planning.md` (old router - replaced by s5_p1)
- `phase_5.3_post_implementation.md` (old router - replaced by s5_p5/p6/p7)
- `support/bugfix_workflow.md` → Move to `stages/s5/s5_bugfix_workflow.md`

---

### Stage 9: Epic Final QC

**Current:**
```
Stage 9: Epic Final QC
  Phase 6.1: Epic Smoke Testing
  Phase 6.2: Epic QC Rounds
  Phase 6.3: User Testing
  Phase 6.4: Epic Final Review
```

**New:**
```
S9: Epic Final QC
  S9.P1: Epic Smoke Testing
  S9.P2: Epic QC Rounds
  S9.P3: User Testing
  S9.P4: Epic Final Review
```

**Files:**
```
stages/s9/
  s6_epic_final_qc.md (router/overview)
  s6_p1_epic_smoke_testing.md
  s6_p2_epic_qc_rounds.md
  s6_p3_user_testing.md
  s6_p4_epic_final_review.md
```

**Changes:**
- Rename: `phase_6.1_epic_smoke_testing.md` → `s6_p1_epic_smoke_testing.md`
- Rename: `phase_6.2_epic_qc_rounds.md` → `s6_p2_epic_qc_rounds.md`
- Rename: `phase_6.3_user_testing.md` → `s6_p3_user_testing.md`
- Rename: `phase_6.4_epic_final_review.md` → `s6_p4_epic_final_review.md`

---

### Stage 10: Epic Cleanup

**Current:**
```
Stage 10: Epic Cleanup
  Phase 7.1: Guide Update Workflow
```

**New:**
```
S10: Epic Cleanup
  S10.P1: Guide Update Workflow
```

**Files:**
```
stages/s10/
  s7_epic_cleanup.md (main file)
  s7_p1_guide_update_workflow.md
```

**Changes:**
- Rename directory: `stage_7/` → `s7/`
- Rename: `epic_cleanup.md` → `s7_epic_cleanup.md`
- Rename: `phase_7.1_guide_update_workflow.md` → `s7_p1_guide_update_workflow.md`

---

## Complete File Structure: New

```
feature-updates/guides_v2/
├── README.md (update all references)
├── EPIC_WORKFLOW_USAGE.md (update all references)
├── naming_conventions.md (REWRITE for S#.P#.I# system)
├── prompts_reference_v2.md (update all references)
│
├── stages/
│   ├── s1/
│   │   └── s1_epic_planning.md
│   │
│   ├── s2/
│   │   ├── s2_feature_deep_dive.md (router)
│   │   ├── s2_p1_research.md
│   │   ├── s2_p2_specification.md
│   │   └── s2_p3_refinement.md
│   │
│   ├── s3/
│   │   └── s3_cross_feature_sanity_check.md
│   │
│   ├── s4/
│   │   └── s4_epic_testing_strategy.md
│   │
│   ├── s5/
│   │   ├── s5_feature_implementation.md (router)
│   │   ├── s5_p1_planning_round1.md (phase router)
│   │   ├── s5_p1_i1_requirements.md
│   │   ├── s5_p1_i2_algorithms.md
│   │   ├── s5_p1_i3_integration.md
│   │   ├── s5_p2_planning_round2.md (phase router)
│   │   ├── s5_p2_i1_test_strategy.md
│   │   ├── s5_p2_i2_reverification.md
│   │   ├── s5_p2_i3_final_checks.md
│   │   ├── s5_p3_planning_round3.md (phase router)
│   │   ├── s5_p3_i1_preparation.md
│   │   ├── s5_p3_i2_gates_part1.md
│   │   ├── s5_p3_i3_gates_part2.md
│   │   ├── s5_p4_execution.md
│   │   ├── s5_p5_smoke_testing.md
│   │   ├── s5_p6_qc_rounds.md
│   │   ├── s5_p7_final_review.md
│   │   ├── s5_p8_cross_feature_alignment.md
│   │   ├── s5_p9_epic_testing_update.md
│   │   └── s5_bugfix_workflow.md
│   │
│   ├── s6/
│   │   ├── s6_epic_final_qc.md (router)
│   │   ├── s6_p1_epic_smoke_testing.md
│   │   ├── s6_p2_epic_qc_rounds.md
│   │   ├── s6_p3_user_testing.md
│   │   └── s6_p4_epic_final_review.md
│   │
│   └── s7/
│       ├── s7_epic_cleanup.md
│       └── s7_p1_guide_update_workflow.md
│
├── prompts/ (update all file references)
├── reference/ (update all cross-references)
├── templates/ (update all examples)
├── debugging/ (update all cross-references)
└── missed_requirement/ (update all cross-references)
```

**DELETED directories:**
- `stages/stage_5/iterations/` → Content merged into phase files
- `stages/stage_5/support/` → Content merged or moved

**RENAMED directories:**
- `stages/stage_1/` → `stages/s1/`
- `stages/stage_2/` → `stages/s2/`
- `stages/stage_3/` → `stages/s3/`
- `stages/stage_4/` → `stages/s4/`
- `stages/stage_5/` → `stages/s5/`
- `stages/stage_6/` → `stages/s9/`
- `stages/stage_7/` → `stages/s10/`

---

## Directory Structure Changes

**Current:**
```
stages/
  stage_1/
    epic_planning.md
  stage_2/
    feature_deep_dive.md
    phase_2.1_research.md
    phase_2.2_specification.md
    phase_2.3_refinement.md
  stage_5/
    part_5.1.1_round1.md
    part_5.1.2_round2.md
    iterations/
      5.1.1_iteration_4_algorithms.md
      5.1.3.1_iterations_17_18_phasing.md
      ...
```

**New (STAGE SUBDIRECTORIES, FLAT WITHIN):**
```
stages/
  s1/
    s1_epic_planning.md
  s2/
    s2_feature_deep_dive.md
    s2_p1_research.md
    s2_p2_specification.md
    s2_p3_refinement.md
  s5/
    s5_feature_implementation.md          (main router)
    s5_p1_planning_round1.md              (phase router)
    s5_p1_i1_requirements.md              (iterations 1-3)
    s5_p1_i2_algorithms.md                (iterations 4-6 + Gate 4a)
    s5_p1_i3_integration.md               (iteration 7)
    s5_p2_planning_round2.md              (phase router)
    s5_p2_i1_test_strategy.md             (iterations 8-10)
    s5_p2_i2_reverification.md            (iterations 11-12)
    s5_p2_i3_final_checks.md              (iterations 13-16)
    s5_p3_planning_round3.md              (phase router)
    s5_p3_i1_preparation.md               (iterations 17-22)
    s5_p3_i2_gates_part1.md               (iterations 23, 23a)
    s5_p3_i3_gates_part2.md               (iterations 24, 25)
    s5_p4_execution.md
    s5_p5_smoke_testing.md
    s5_p6_qc_rounds.md
    s5_p7_final_review.md
    s5_p8_cross_feature_alignment.md
    s5_p9_epic_testing_update.md
    s5_bugfix_workflow.md
  ...
```

**Benefits:**
- **Natural grouping** - All S5 phases together in `s5/` directory
- **Manageable file sizes** - I# splits keep files 200-400 lines (not 800-1000)
- **Flat within each stage** - No deeper nesting (no `s5/iterations/`)
- **Self-documenting** - `s5_p1_i2_algorithms.md` = S5.P1.I2
- **Matches notation** - File names directly map to S#.P#.I# notation
- **Easy to see scope** - Opening `s5/` shows all 9 phases + I# sub-files

---

## Header Format Changes

**Current:**
```markdown
# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning
### Part 5.1.3: Round 3
```

**New:**
```markdown
# S5: Feature Implementation
## S5.P3: Planning Round 3
### S5.P3.I1: Preparation (Iterations 17-22)

# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I2: Algorithms & Dependencies (Iterations 4-6)
```

**Rules:**
1. Always include full hierarchy in header (S5.P3.I1, not just I1)
2. Use self-documenting prefixes (S/P/I)
3. Keep descriptive names after colon
4. I# files contain multiple workflow iterations grouped logically

---

## Cross-Reference Changes

**Current (confusing):**
```markdown
After completing Phase 5.1, proceed to Phase 5.2.
See `stages/stage_5/part_5.1.3_round3.md` for details.
Complete Part 5.3.1 before moving to Part 5.3.2.
```

**New (clear):**
```markdown
After completing S5.P1, proceed to S5.P2.
See `stages/s5/s5_p3_i1_preparation.md` for iterations 17-22.
Complete S7.P1 before moving to S7.P2.
Start with S5.P1.I1 (Requirements Analysis) for iterations 1-3.
```

**Benefits:**
- Notation matches file names and paths exactly
- Hierarchy is obvious from prefixes (S/P/I)
- Stage grouping visible in path (`stages/s5/`)
- I# level provides granular file references
- Can include descriptive names for clarity

---

## Terminology Changes

**Old Terms → New Terms:**

| Old Term | New Term | Example |
|----------|----------|---------|
| Stage 1 | S1 | S1: Epic Planning |
| Phase 5.1 | S5.P1 | S5.P1: Planning Round 1 |
| Part 5.1.3 | S5.P3 | S5.P3: Planning Round 3 |
| Step 5.1.3.1 | S5.P3.I1 | S5.P3.I1: Preparation |
| Iteration file (1-3) | S5.P1.I1 | S5.P1.I1: Requirements |
| Iteration file (4-6) | S5.P1.I2 | S5.P1.I2: Algorithms |
| STAGE_5aa | S5.P1 | (old notation eliminated) |
| STAGE_5ab | S5.P2 | (old notation eliminated) |
| STAGE_5ac | S5.P3 | (old notation eliminated) |

---

## Implementation Steps

### Phase 1: Create New Files (No Deletion Yet)
1. Create all new files with S#.P#.I# notation
2. Update headers within files
3. Merge content from Level 4 files into Level 3 files
4. Update internal cross-references

### Phase 2: Update Supporting Files
1. Update `naming_conventions.md` with new system
2. Update `README.md` with new file locations
3. Update `EPIC_WORKFLOW_USAGE.md` with new notation
4. Update `prompts_reference_v2.md` with new notation
5. Update all templates with new notation
6. Update CLAUDE.md with new notation

### Phase 3: Update Cross-References
1. Update all guides in `debugging/`
2. Update all guides in `missed_requirement/`
3. Update all guides in `reference/`
4. Update all prompts in `prompts/`
5. Search for all old notation and replace

### Phase 4: Delete Old Files
1. Delete all old `stage_X/` subdirectories
2. Delete all old iteration files
3. Delete router files that are no longer needed
4. Clean up any remaining old notation

### Phase 5: Validation
1. Check all file references are valid
2. Verify no broken cross-references
3. Test navigation through guides
4. Confirm all old notation eliminated

---

## Benefits of New System

### 1. Immediate Clarity
- `S5.P2.I8` → Stage 5, Phase 2, Iteration 8 (no counting dots)
- Self-documenting prefixes (S/P/I)

### 2. Easier Navigation
- Stage files grouped by stage directory
- File names match notation exactly: `s5/s5_p1_i2_algorithms.md` ↔ S5.P1.I2
- Natural grouping (all S5 work in `s5/` directory)
- I# splits create manageable file sizes (200-400 lines)
- Clear file organization with routers guiding navigation

### 3. Simplified Structure
- 3 levels instead of 4
- No deeply nested subdirectories
- Fewer router files

### 4. Better Scanability
- Prefixes jump out when reading: **S5.P2**
- Easy to spot hierarchy level
- Notation consistent with file names

### 5. Eliminates Confusion
- No more counting dots to determine level
- No more "is this a Phase or Part?"
- No more mixing STAGE_5aa with 5.1.3

---

## Migration Strategy for In-Progress Epics

**For any in-progress epics using old notation:**

1. **EPIC_README.md updates:**
   - Update Agent Status notation
   - Update Progress Tracker notation
   - Add migration note at top

2. **Feature README.md updates:**
   - Update Agent Status notation
   - Update current guide references

3. **No file structure changes in epic folders** (only guides change)

4. **User communication:**
   - Explain notation change in next session
   - Reference old → new mapping
   - Confirm they understand new notation

---

## Testing Plan

### Test 1: Navigation Test
- Start at S1
- Follow cross-references through all stages
- Verify no broken links

### Test 2: Comprehension Test
- Read random guide (e.g., S5.P3)
- Verify hierarchy clear from notation
- Verify can understand position in workflow

### Test 3: Resumption Test
- Simulate session compaction at S5.P2.I12
- Verify Agent Status clear
- Verify can resume from notation

### Test 4: Search Test
- Search for old notation patterns
- Verify all eliminated
- Verify new notation consistent

---

## Estimated Effort

**Files to create/update:**
- ~45 guide files (stages/ - includes I# splits)
- ~10 prompt files
- ~15 reference files
- ~10 template files
- ~10 supporting files

**Total:** ~90 files

**Time estimate:** 5-7 hours (with careful validation and I# file creation)

---

## Risks & Mitigation

### Risk 1: Breaking In-Progress Epics
**Mitigation:** Only guides change, epic folders unchanged. Add migration notes.

### Risk 2: Missing Cross-References
**Mitigation:** Use search to find all old notation. Create exhaustive replacement list.

### Risk 3: User Confusion During Transition
**Mitigation:** Create "Old → New" quick reference card. Include in next session.

### Risk 4: Incomplete Flattening
**Mitigation:** Review all Level 4 items manually. Ensure all accounted for.

---

## Decision Points for User

### Decision 1: Directory Structure
**Option A:** Completely flat (all files in `stages/`)
**Option B (CHOSEN):** Stage subdirectories, flat within (`stages/s5/s5_p1_planning_round1.md`)

**Decision:** Option B chosen for natural grouping and reduced clutter per directory

### Decision 2: Router Files
**Option A (Proposed):** Keep minimal router files (s2, s5, s6)
**Option B:** Eliminate all routers, make each file standalone

**Recommendation:** Option A (minimal routers for multi-phase stages)

### Decision 3: I# File Splitting
**Option A (CHOSEN):** Use I# for file splits (S5.P1.I1, S5.P1.I2, S5.P1.I3)
**Option B:** Keep phases as single large files (S5.P1 = 600-800 lines)

**Decision:** Option A chosen to keep files manageable (200-400 lines each) and match existing iteration file structure

### Decision 4: File Name Casing
**Option A (Proposed):** Lowercase with underscores (s5_p1_planning_round1.md)
**Option B:** Mixed case (S5_P1_Planning_Round1.md)

**Recommendation:** Option A (consistent with project standards)

---

## Next Steps

1. **User reviews this plan**
2. **User approves or requests modifications**
3. **Begin Phase 1: Create new files**
4. **Validate each phase before proceeding**
5. **Complete migration within one session** (avoid partial state)

---

## Questions for User

1. Do you approve the S#.P#.I# notation system?
2. Do you approve flattening to 3 levels max?
3. Do you prefer flat directory structure (Option A)?
4. Any concerns about breaking existing references?
5. Should we proceed with implementation?

---

**Created:** 2026-01-11
**Status:** AWAITING USER APPROVAL
**Estimated Completion:** 4-6 hours after approval
