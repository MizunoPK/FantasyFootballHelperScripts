# Stage 5 Split Implementation Strategy

**Goal:** Split current Stage 5 into 4 separate stages (S5-S8) and renumber current S6→S9, S7→S10

**Estimated time:** 4-6 hours

**Backup branch:** `refactor/stage-5-split`

---

## Current vs. New Structure

### Current (10 stages, S5 has 20 files)
- S1: Epic Planning (1 file)
- S2: Feature Deep Dives (5 files)
- S3: Cross-Feature Sanity Check (1 file)
- S4: Epic Testing Strategy (1 file)
- **S5: Feature Implementation (20 files)** ← TOO BIG
  - S5.P1-P3: Planning (12 files)
  - S5.P4: Execution (1 file)
  - S5.P5-P7: Testing (3 files)
  - S5.P8: Alignment (1 file)
  - S5.P9: Epic Update (1 file)
  - Support: 2 files
- S6: Epic-Level Final QC (4 files)
- S7: Epic Cleanup (2 files)

### New (10 stages, balanced distribution)
- S1: Epic Planning (1 file)
- S2: Feature Deep Dives (5 files)
- S3: Cross-Feature Sanity Check (1 file)
- S4: Epic Testing Strategy (1 file)
- **S5: Implementation Planning (12 files)** ← Former S5.P1-P3
- **S6: Implementation Execution (1 file)** ← Former S5.P4
- **S7: Implementation Testing & Review (3 files)** ← Former S5.P5-P7
- **S8: Post-Feature Alignment (2 files)** ← Former S5.P8-P9
- **S9: Epic-Level Final QC (4 files)** ← Former S6
- **S10: Epic Cleanup (2 files)** ← Former S7

---

## Stage Mapping Reference

| Old Stage | Old Notation | New Stage | New Notation | Description |
|-----------|--------------|-----------|--------------|-------------|
| S5.P1-P3 | S5.P1-P3 | **S5** | S5.P1-P3 | Implementation Planning (28 iterations) |
| S5.P4 | S5.P4 | **S6** | S6 | Implementation Execution |
| S5.P5-P7 | S5.P5-P7 | **S7** | S7.P1-P3 | Implementation Testing & Review |
| S5.P8 | S5.P8 | **S8** | S8.P1 | Cross-Feature Spec Alignment |
| S5.P9 | S5.P9 | **S8** | S8.P2 | Epic Testing Plan Reassessment |
| S6 | S6 | **S9** | S9 | Epic-Level Final QC |
| S7 | S7 | **S10** | S10 | Epic Cleanup |

---

## Implementation Plan

### Part 1: Create Backup Branch
```bash
git checkout -b refactor/stage-5-split
```

### Part 2: Create New Stage Directories
```bash
cd feature-updates/guides_v2/stages
mkdir s6 s7 s8 s9 s10
```

### Part 3: Move Files to New Structure

#### Part 3A: S5 → S5 (Keep Planning Files)
**Files stay in s5/:**
- s5_p1_planning_round1.md (router)
- s5_p1_i1_requirements.md
- s5_p1_i2_algorithms.md
- s5_p1_i3_integration.md
- s5_p2_planning_round2.md (router)
- s5_p2_i1_test_strategy.md
- s5_p2_i2_reverification.md
- s5_p2_i3_final_checks.md
- s5_p3_planning_round3.md (router)
- s5_p3_i1_preparation.md
- s5_p3_i2_gates_part1.md
- s5_p3_i3_gates_part2.md

**12 files remain in s5/**

#### Part 3B: S5.P4 → S6 (Execution)
**Move and rename:**
```bash
mv s5/s5_p4_execution.md s6/s6_execution.md
```

**Update header:**
- `# S5: Feature Implementation` → `# S6: Implementation Execution`
- `## S5.P4: Implementation Execution` → `## S6: Implementation Execution`

**1 file in s6/**

#### Part 3C: S5.P5-P7 → S7 (Testing & Review)
**Move and rename:**
```bash
mv s5/s5_p5_smoke_testing.md s7/s7_p1_smoke_testing.md
mv s5/s5_p6_qc_rounds.md s7/s7_p2_qc_rounds.md
mv s5/s5_p7_final_review.md s7/s7_p3_final_review.md
```

**Update headers:**
- S5.P5 → S7.P1 (Smoke Testing)
- S5.P6 → S7.P2 (QC Rounds)
- S5.P7 → S7.P3 (Final Review)

**3 files in s7/**

#### Part 3D: S5.P8-P9 → S8 (Post-Feature Alignment)
**Move and rename:**
```bash
mv s5/s5_p8_cross_feature_alignment.md s8/s8_p1_cross_feature_alignment.md
mv s5/s5_p9_epic_testing_update.md s8/s8_p2_epic_testing_update.md
```

**Update headers:**
- S5.P8 → S8.P1 (Cross-Feature Spec Alignment)
- S5.P9 → S8.P2 (Epic Testing Plan Reassessment)

**2 files in s8/**

#### Part 3E: S6 → S9 (Epic QC)
**Move and rename:**
```bash
mv s6/s6_epic_final_qc.md s9/s9_epic_final_qc.md
mv s6/s6_p1_epic_smoke_testing.md s9/s9_p1_epic_smoke_testing.md
mv s6/s6_p2_epic_qc_rounds.md s9/s9_p2_epic_qc_rounds.md
mv s6/s6_p3_user_testing.md s9/s9_p3_user_testing.md
mv s6/s6_p4_epic_final_review.md s9/s9_p4_epic_final_review.md
```

**Update headers:**
- All S6 → S9 throughout files

**Delete old s6/ directory after move**

**5 files in s9/** (includes router)

#### Part 3F: S7 → S10 (Epic Cleanup)
**Move and rename:**
```bash
mv s7/s7_epic_cleanup.md s10/s10_epic_cleanup.md
mv s7/s7_p1_guide_updates.md s10/s10_p1_guide_updates.md
```

**Update headers:**
- All S7 → S10 throughout files

**Delete old s7/ directory after move**

**2 files in s10/**

#### Part 3G: S5 Support Files (Keep in S5 with new context)
**Files stay in s5/:**
- s5_bugfix_workflow.md (applies to S5-S8 loop)
- s5_pr_review_protocol.md (used in S7.P3)

**Update context notes:**
- Bugfix: "Applies to any issues during S5-S8 feature loop"
- PR Review: "Used in S7.P3 Final Review"

---

### Part 4: Batch Update Cross-References

#### Part 4A: Update Stage Numbers in All Files
```bash
# Create sed script for stage number updates
cat > /tmp/stage_updates.sed << 'EOF'
# S5.P4 → S6
s/S5\.P4/S6/g
s/Starting S5\.P4/Starting S6/g

# S5.P5 → S7.P1
s/S5\.P5/S7.P1/g
s/Starting S5\.P5/Starting S7.P1/g

# S5.P6 → S7.P2
s/S5\.P6/S7.P2/g

# S5.P7 → S7.P3
s/S5\.P7/S7.P3/g

# S5.P8 → S8.P1
s/S5\.P8/S8.P1/g
s/Starting S5\.P8/Starting S8.P1/g

# S5.P9 → S8.P2
s/S5\.P9/S8.P2/g
s/Starting S5\.P9/Starting S8.P2/g

# S6 → S9
s/\bS6\b/S9/g
s/S6\./S9./g
s/Starting S6/Starting S9/g
s/Stage 6/Stage 9/g

# S7 → S10
s/\bS7\b/S10/g
s/S7\./S10./g
s/Starting S7/Starting S10/g
s/Stage 7/Stage 10/g
s/Stage 7\.5/Stage 10.1/g
s/S7\.P1/S10.P1/g
EOF

# Apply to all guide files
find . -name "*.md" -type f -exec sed -i -f /tmp/stage_updates.sed {} +
```

#### Part 4B: Update File Paths
```bash
cat > /tmp/path_updates.sed << 'EOF'
# S5 paths (execution and testing moved)
s|stages/s5/s5_p4_execution\.md|stages/s6/s6_execution.md|g
s|stages/s5/s5_p5_smoke_testing\.md|stages/s7/s7_p1_smoke_testing.md|g
s|stages/s5/s5_p6_qc_rounds\.md|stages/s7/s7_p2_qc_rounds.md|g
s|stages/s5/s5_p7_final_review\.md|stages/s7/s7_p3_final_review.md|g
s|stages/s5/s5_p8_cross_feature_alignment\.md|stages/s8/s8_p1_cross_feature_alignment.md|g
s|stages/s5/s5_p9_epic_testing_update\.md|stages/s8/s8_p2_epic_testing_update.md|g

# S6 → S9 paths
s|stages/s6/s6_epic_final_qc\.md|stages/s9/s9_epic_final_qc.md|g
s|stages/s6/s6_p1_epic_smoke_testing\.md|stages/s9/s9_p1_epic_smoke_testing.md|g
s|stages/s6/s6_p2_epic_qc_rounds\.md|stages/s9/s9_p2_epic_qc_rounds.md|g
s|stages/s6/s6_p3_user_testing\.md|stages/s9/s9_p3_user_testing.md|g
s|stages/s6/s6_p4_epic_final_review\.md|stages/s9/s9_p4_epic_final_review.md|g

# S7 → S10 paths
s|stages/s7/s7_epic_cleanup\.md|stages/s10/s10_epic_cleanup.md|g
s|stages/s7/s7_p1_guide_updates\.md|stages/s10/s10_p1_guide_updates.md|g

# Directory references
s|stages/s6/|stages/s9/|g
s|stages/s7/|stages/s10/|g
EOF

find . -name "*.md" -type f -exec sed -i -f /tmp/path_updates.sed {} +
```

---

### Part 5: Update Key Documentation Files

#### Part 5A: Root CLAUDE.md
- Update workflow overview diagram (S5→S6→S7→S8→S9→S10)
- Update Stage Workflows section with new structure
- Update gate table (locations moved)
- Update all cross-references

#### Part 5B: naming_conventions.md
- Update directory structure table
- Update all stage examples
- Update file count per stage

#### Part 5C: prompts_reference_v2.md
- Add prompts for new stages (S6, S7, S8)
- Update S9, S10 prompts (formerly S6, S7)
- Update "Resuming" prompt stage references

#### Part 5D: EPIC_WORKFLOW_USAGE.md
- Update workflow overview
- Update stage descriptions
- Update FAQ references

#### Part 5E: README.md
- Update guide index table
- Update stage descriptions
- Update quick reference

---

### Part 6: Update Reference Files

**Files to update:**
- reference/common_mistakes.md (stage references)
- reference/glossary.md (stage definitions)
- reference/mandatory_gates.md (gate locations)
- reference/PROTOCOL_DECISION_TREE.md (stage references)
- reference/GIT_WORKFLOW.md (commit stage references)

---

### Part 7: Update Template Files

**Files to update:**
- templates/epic_readme_template.md (stage workflow)
- templates/feature_readme_template.md (stage references)
- All other templates with stage references

---

### Part 8: Update Prompt Files

**Files to update:**
- All prompts/*.md files with stage transitions
- Update stage names and numbers consistently

---

### Part 9: Validation

#### Validation Checklist
```bash
# Check for orphaned old references
grep -r "S5\.P4" . --include="*.md" | grep -v "STAGE_SPLIT_STRATEGY.md"
grep -r "S5\.P5" . --include="*.md" | grep -v "STAGE_SPLIT_STRATEGY.md"
grep -r "S5\.P6" . --include="*.md" | grep -v "STAGE_SPLIT_STRATEGY.md"
grep -r "S5\.P7" . --include="*.md" | grep -v "STAGE_SPLIT_STRATEGY.md"
grep -r "S5\.P8" . --include="*.md" | grep -v "STAGE_SPLIT_STRATEGY.md"
grep -r "S5\.P9" . --include="*.md" | grep -v "STAGE_SPLIT_STRATEGY.md"

# Check stage 6 wasn't left behind (should be S9 now)
grep -r "\bS6\b" . --include="*.md" | grep -v "STAGE_SPLIT_STRATEGY.md" | grep -v "KAI-6"

# Check stage 7 wasn't left behind (should be S10 now)
grep -r "\bS7\b" . --include="*.md" | grep -v "STAGE_SPLIT_STRATEGY.md" | grep -v "KAI-7"

# Verify new stages exist
grep -r "S6:" . --include="*.md" | head -5
grep -r "S7:" . --include="*.md" | head -5
grep -r "S8:" . --include="*.md" | head -5
grep -r "S9:" . --include="*.md" | head -5
grep -r "S10:" . --include="*.md" | head -5

# Count files per stage
ls -1 stages/s5/*.md | wc -l  # Should be 14 (12 planning + 2 support)
ls -1 stages/s6/*.md | wc -l  # Should be 1
ls -1 stages/s7/*.md | wc -l  # Should be 3
ls -1 stages/s8/*.md | wc -l  # Should be 2
ls -1 stages/s9/*.md | wc -l  # Should be 5
ls -1 stages/s10/*.md | wc -l # Should be 2
```

---

### Part 10: Commit
```bash
git add .
git commit -m "refactor/KAI-6: Split Stage 5 into S5-S8, renumber S6→S9, S7→S10

- Split Feature Implementation into 4 logical stages
- S5: Implementation Planning (former S5.P1-P3, 12 files)
- S6: Implementation Execution (former S5.P4, 1 file)
- S7: Implementation Testing & Review (former S5.P5-P7, 3 files)
- S8: Post-Feature Alignment (former S5.P8-P9, 2 files)
- Renumbered Epic QC: S6 → S9 (4 files)
- Renumbered Epic Cleanup: S7 → S10 (2 files)
- Updated 180+ cross-references across all guides
- Better stage balance and conceptual clarity

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Execution Order

1. ✅ Create strategy document (this file)
2. Create backup branch
3. Create new directories (s6-s10)
4. Move and rename files (Parts 3A-3G)
5. Batch update cross-references (Part 4)
6. Update key documentation (Part 5)
7. Update reference files (Part 6)
8. Update templates (Part 7)
9. Update prompts (Part 8)
10. Validate changes (Part 9)
11. Commit (Part 10)

---

## Risk Mitigation

- Work on backup branch
- Test after each major part
- Keep this strategy file for rollback reference
- Validate comprehensively before commit

---

## Expected Outcomes

✅ Balanced stage distribution (1-5 files per stage)
✅ Clear conceptual separation (each stage = one major activity)
✅ Logical workflow progression (S1→S10)
✅ Easier to understand and navigate
✅ Better reflects actual workflow complexity
