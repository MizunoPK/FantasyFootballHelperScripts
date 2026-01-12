# Implementation Strategy - Dual Refactoring
## 2026-01-11

## Overview

We need to implement TWO major changes:
1. **Notation Refactoring** - S#.P#.I# notation + file restructuring (~90 files, 5-7 hours)
2. **Terminology Standardization** - Reserve Stage/Phase/Iteration (~70 files, 3-4 hours)

**Total Effort:** 8-11 hours
**Total Files:** ~90 files (many overlap between plans)

---

## Strategy: Sequential Phased Approach

**Why Sequential?**
- Refactoring changes FILE NAMES and PATHS
- Terminology changes CONTENT within files
- If we fix terminology in old files, that work is lost when we delete/merge them
- Cleaner to establish new structure FIRST, then clean up content

**Approach: Do refactoring first, then terminology on the new structure**

---

## Phase 1: File Structure Refactoring (5-7 hours)

### Part 1A: Stage Directories (30 min)

**Create new directory structure:**
```bash
cd feature-updates/guides_v2/stages

# Create stage subdirectories
mkdir s1 s2 s3 s4 s5 s6 s7
```

**Checkpoint:** Verify 7 directories created

---

### Part 1B: Simple Renames (1 hour)

**Stages 1, 3, 4 (single files):**
```bash
# Stage 1
mv stage_1/epic_planning.md s1/s1_epic_planning.md

# Stage 3
mv stage_3/cross_feature_sanity_check.md s3/s3_cross_feature_sanity_check.md

# Stage 4
mv stage_4/epic_testing_strategy.md s4/s4_epic_testing_strategy.md
```

**For each file:**
1. Rename file
2. Update header: `# STAGE 1:` → `# S1:`
3. Update all internal references to S# notation
4. Update cross-references to new file paths

**Checkpoint:** 3 stages complete (S1, S3, S4)

---

### Part 1C: Stage 2 - Simple Phase Renames (45 min)

**Stage 2 has 4 files (router + 3 phases):**
```bash
cd stages
mv stage_2/feature_deep_dive.md s2/s2_feature_deep_dive.md
mv stage_2/phase_2.1_research.md s2/s2_p1_research.md
mv stage_2/phase_2.2_specification.md s2/s2_p2_specification.md
mv stage_2/phase_2.3_refinement.md s2/s2_p3_refinement.md
mv stage_2/phase_2.2.5_spec_validation.md s2/s2_p2_5_spec_validation.md
```

**For each file:**
1. Rename file
2. Update headers to S2.P# notation
3. Update cross-references

**Checkpoint:** Stage 2 complete

---

### Part 1D: Stage 9 - Simple Phase Renames (45 min)

**Stage 9 has 5 files (router + 4 phases):**
```bash
mv stage_6/epic_final_qc.md s6/s6_epic_final_qc.md
mv stage_6/phase_6.1_epic_smoke_testing.md s6/s6_p1_epic_smoke_testing.md
mv stage_6/phase_6.2_epic_qc_rounds.md s6/s6_p2_epic_qc_rounds.md
mv stage_6/phase_6.3_user_testing.md s6/s6_p3_user_testing.md
mv stage_6/phase_6.4_epic_final_review.md s6/s6_p4_epic_final_review.md
```

**For each file:**
1. Rename file
2. Update headers to S9.P# notation
3. Update cross-references

**Checkpoint:** Stage 9 complete

---

### Part 1E: Stage 10 - Simple Phase Renames (30 min)

**Stage 10 has 2 files:**
```bash
mv stage_7/epic_cleanup.md s7/s7_epic_cleanup.md
mv stage_7/phase_7.1_guide_update_workflow.md s7/s7_p1_guide_update_workflow.md
```

**Checkpoint:** Stage 10 complete

---

### Part 1F: Stage 5 - Complex Restructuring (2.5-3 hours)

**This is the big one: 22 files total**

#### Step 1: Create Phase 1 (Round 1) files (30 min)
```bash
# Create router
cp stage_5/part_5.1.1_round1.md s5/s5_p1_planning_round1.md
# Edit to make it a router

# Create I# files
cp stage_5/iterations/5.1.1_iterations_1_3_requirements.md s5/s5_p1_i1_requirements.md
cp stage_5/iterations/5.1.1_iteration_4_algorithms.md s5/s5_p1_i2_algorithms.md
# Merge 5.1.1_iterations_5_6 + iteration_7 → s5/s5_p1_i3_integration.md
```

**For each file:**
- Update headers to S5.P1.I# notation
- Update cross-references
- Convert P1 file to router pointing to I# files

#### Step 2: Create Phase 2 (Round 2) files (30 min)
```bash
# Create router
cp stage_5/part_5.1.2_round2.md s5/s5_p2_planning_round2.md

# Create I# files
cp stage_5/iterations/5.1.2_iterations_8_10_test_strategy.md s5/s5_p2_i1_test_strategy.md
cp stage_5/iterations/5.1.2_iterations_11_12_reverification.md s5/s5_p2_i2_reverification.md
cp stage_5/iterations/5.1.2_iterations_13_16_final_checks.md s5/s5_p2_i3_final_checks.md
```

#### Step 3: Create Phase 3 (Round 3) files (45 min)
```bash
# Create router
cp stage_5/part_5.1.3_round3.md s5/s5_p3_planning_round3.md

# Create I# files - these require MERGING multiple files
# Merge 5.1.3.1_iterations_17_18 + 19_20 + 21_22 → s5/s5_p3_i1_preparation.md
# Merge 5.1.3.2_iteration_23 + gate_23a → s5/s5_p3_i2_gates_part1.md
# Use 5.1.3.3_iterations_24_25 → s5/s5_p3_i3_gates_part2.md
```

#### Step 4: Create remaining phases (45 min)
```bash
# Phases 4-9 (no I# splits, direct renames)
cp stage_5/phase_5.2_implementation_execution.md s5/s5_p4_execution.md
cp stage_5/part_5.3.1_smoke_testing.md s5/s5_p5_smoke_testing.md
cp stage_5/part_5.3.2_qc_rounds.md s5/s5_p6_qc_rounds.md
cp stage_5/part_5.3.3_final_review.md s5/s5_p7_final_review.md
cp stage_5/phase_5.4_post_feature_alignment.md s5/s5_p8_cross_feature_alignment.md
cp stage_5/phase_5.5_post_feature_testing_update.md s5/s5_p9_epic_testing_update.md

# Bugfix workflow
cp stage_5/support/bugfix_workflow.md s5/s5_bugfix_workflow.md
```

#### Step 5: Update all S5 files (30 min)
- Update headers in all 22 files
- Update cross-references throughout
- Test navigation between files

**Checkpoint:** Stage 5 complete (22 files)

---

### Part 1G: Update Supporting Files (1 hour)

**Update cross-references in:**
- `README.md` - Update all stage/phase references to S#.P#
- `EPIC_WORKFLOW_USAGE.md` - Update all references
- `naming_conventions.md` - Complete rewrite for S#.P#.I#
- `prompts_reference_v2.md` - Update all file paths
- All `prompts/*.md` files - Update file paths
- All `reference/*.md` files - Update file paths
- All `templates/*.md` files - Update example paths
- `debugging/*.md` files - Update cross-references
- `missed_requirement/*.md` files - Update cross-references

**Strategy for this part:**
1. Create search/replace list of all old → new paths
2. Run batch find/replace
3. Manual verification of key files

---

### Part 1H: Delete Old Files (15 min)

**Delete old directories:**
```bash
rm -rf stage_1/ stage_2/ stage_3/ stage_4/ stage_5/ stage_6/ stage_7/
```

**Verify:**
- All content moved to new structure
- No broken references
- Navigation works

**Checkpoint:** Phase 1 complete - ALL files in new S#.P#.I# structure

---

### Part 1I: Validation (30 min)

**Tests:**
1. Check all file references valid (no 404s)
2. Verify S#.P#.I# notation consistent
3. Test navigation through workflow
4. Spot-check 10 random files for correctness

**Commit Point:** Git commit after Phase 1 complete

---

## Phase 2: Terminology Standardization (3-4 hours)

**Now that file structure is stable, clean up terminology**

### Part 2A: High-Priority Batch Updates (1 hour)

**Category 1: Implementation Steps (Phase # → Step #)**

Run find/replace:
```
Pattern: ### Phase ([0-9]+):
Replace: ### Step \1:
Context: NOT in stage guide headers (those are S#.P#)
```

**Files to update:**
- REFACTORING_PLAN (this file)
- EPIC_WORKFLOW_USAGE.md
- prompts/*.md (all files)
- debugging/*.md (all files)
- missed_requirement/*.md (all files)
- reference/common_mistakes.md
- reference/stage_1/stage_1_reference_card.md

**Manual verification after batch:** Check 5-10 files

---

### Part 2B: Casual Stage References (1 hour)

**Find/replace patterns:**
```
"What is this stage?" → "What is this guide?"
"Before starting this stage:" → "Before starting this guide:"
"at this stage" → "at this point"
"in this stage" → "in this guide"
"during this stage" → "during this process"
"from this stage" → "from this section"
"Could this stage" → "Could this guide"
```

**Files affected:** All `stages/s*/*.md` files

**Approach:** Run batch find/replace, then manually check stage guides

---

### Part 2C: Generic Iteration Usage (30 min)

**Find/replace patterns:**
```
"ITERATIVE" → "REPEATING"
"iterative refinement" → "continuous refinement"
"Iterative Comprehensive Reviews" → "Repeated Comprehensive Reviews"
"iterative cycles" → "repeated cycles"
```

**Files affected:**
- debugging/investigation.md
- EPIC_WORKFLOW_USAGE.md
- README.md
- reference/faq_troubleshooting.md
- stages/s5/*.md

---

### Part 2D: Manual Cleanup (1 hour)

**Files needing manual review:**
- stages/s2/s2_feature_deep_dive.md - Remove "Phase" suffix
- stages/s5/phase_5.3_post_implementation.md - Update Part 1/2/3
- reference/stage_2/*.md - Check Phase vs Step usage
- reference/hands_on_data_inspection.md - "this stage" → "this guide"
- reference/spec_validation.md - "this stage" → "this guide"

**Approach:** Go through file-by-file, use checklist from TERMINOLOGY_STANDARDIZATION_PLAN.md

---

### Part 2E: Validation (30 min)

**Tests:**
1. Search for remaining "Phase #:" (not S#.P#) - should be ZERO
2. Search for "this stage" - should be minimal/contextual only
3. Search for "ITERATIVE" - should be ZERO in casual usage
4. Verify S#.P#.I# notation still intact
5. Spot-check 10 files for natural language flow

**Commit Point:** Git commit after Phase 2 complete

---

## Phase 3: Final Validation & Documentation (30 min)

### Part 3A: Complete Validation
1. Run all validation tests from both plans
2. Check navigation through complete workflow
3. Verify no broken references
4. Test with real epic (if possible - or plan to)

### Part 3B: Update CLAUDE.md
1. Update root CLAUDE.md with new notation
2. Update workflow instructions
3. Add reference to both completed plans

### Part 3C: Final Commit
1. Git commit all changes
2. Create summary of changes
3. Archive both refactoring plans to `_internal/`

---

## Implementation Schedule

**Option A: Single Long Session (8-11 hours)**
- Pros: Everything done at once, no partial state
- Cons: Very long, risk of fatigue/errors

**Option B: Two Sessions (Recommended)**
- Session 1: Phase 1 (File Structure) - 5-7 hours
- Session 2: Phase 2 & 3 (Terminology + Validation) - 3-4 hours
- Pros: Natural break point, can commit after Phase 1
- Cons: Two sessions required

**Option C: Three Sessions**
- Session 1: Phase 1A-1E (Simple files) - 3 hours
- Session 2: Phase 1F-1I (Stage 5 + validation) - 3-4 hours
- Session 3: Phase 2 & 3 (Terminology + final) - 3-4 hours
- Pros: Manageable chunks, multiple commit points
- Cons: Three sessions required

---

## Risk Mitigation

### Risk 1: Breaking In-Progress Epic
**Mitigation:**
- Only guide files change, epic folders unchanged
- Update KAI-6 EPIC_README.md Agent Status if notation referenced
- Add migration note at top of current epic

### Risk 2: Missed References
**Mitigation:**
- Create comprehensive search list BEFORE starting
- Use script to find all references to old paths
- Validate with grep searches after completion

### Risk 3: Terminology Regression
**Mitigation:**
- Add pre-commit hook to catch "Phase #:" patterns
- Document reserved terms clearly in CLAUDE.md
- Update glossary with standardized terminology

### Risk 4: Fatigue/Errors in Long Session
**Mitigation:**
- Take breaks every 90 minutes
- Use checklists for validation
- Commit after each major part
- Option B (two sessions) reduces this risk

---

## My Recommendation

**Use Option B (Two Sessions):**

**Session 1 (5-7 hours): File Structure Refactoring**
- Complete Phase 1A through 1I
- Results in clean S#.P#.I# structure
- Commit point: "refactor: Migrate to S#.P#.I# notation system"
- Can test navigation and structure

**Session 2 (3-4 hours): Terminology + Final**
- Complete Phase 2A through 2E
- Complete Phase 3 validation
- Commit point: "refactor: Standardize Stage/Phase/Iteration terminology"
- Everything complete and validated

**Why this is best:**
- Natural break after file structure complete
- Can validate structure before terminology
- Two shorter sessions less error-prone than one long
- Clear commit points for rollback if needed

---

## Execution Checklist

### Before Starting
- [ ] User confirms approval of both plans
- [ ] User confirms Option B (two sessions) or prefers different schedule
- [ ] Git status clean (no uncommitted changes)
- [ ] Create backup branch: `git checkout -b backup-pre-refactor`
- [ ] Return to epic branch: `git checkout epic/KAI-6`

### During Session 1 (Phase 1)
- [ ] Part 1A: Stage directories created
- [ ] Part 1B: Stages 1, 3, 4 renamed
- [ ] Part 1C: Stage 2 renamed
- [ ] Part 1D: Stage 9 renamed
- [ ] Part 1E: Stage 10 renamed
- [ ] Part 1F: Stage 5 restructured (22 files)
- [ ] Part 1G: Supporting files updated
- [ ] Part 1H: Old files deleted
- [ ] Part 1I: Validation complete
- [ ] Git commit: "refactor: Migrate to S#.P#.I# notation system"

### During Session 2 (Phase 2 & 3)
- [ ] Part 2A: Implementation steps updated
- [ ] Part 2B: Casual stage references updated
- [ ] Part 2C: Generic iteration usage updated
- [ ] Part 2D: Manual cleanup complete
- [ ] Part 2E: Terminology validation complete
- [ ] Part 3A: Complete validation passed
- [ ] Part 3B: CLAUDE.md updated
- [ ] Part 3C: Final commit
- [ ] Archive plans to `_internal/`

### After Completion
- [ ] Test navigation through all 7 stages
- [ ] Update any in-progress epic READMEs
- [ ] Delete backup branch (optional)
- [ ] Celebrate! 🎉

---

**Ready to proceed?**

---

**Created:** 2026-01-11
**Status:** AWAITING USER CONFIRMATION ON SCHEDULE
