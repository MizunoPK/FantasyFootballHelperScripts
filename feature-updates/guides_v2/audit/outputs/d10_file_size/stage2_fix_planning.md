# D10: File Size Assessment - Stage 2 Fix Planning

**Dimension:** D10 - File Size Assessment
**Audit Round:** Round 1
**Stage:** Stage 2 - Fix Planning
**Date:** 2026-02-05
**Auditor:** Claude (Primary Agent)

---

## Executive Summary

**Planning Status:** IN PROGRESS

**Files Analyzed:** 2/11 CRITICAL files (2 quick wins complete)

**Reduction Plans Created:**
- ✅ **reference/stage_2/refinement_examples.md** - Split into 4 phase files + router
- ✅ **stages/s10/s10_epic_cleanup.md** - Extract duplicate S10.P1 content + condense STEP 5
- ⏳ **9 files remaining** - Require structure analysis

**Estimated Reduction Impact:**
- refinement_examples.md: 1396 → ~150 lines (89% reduction)
- s10_epic_cleanup.md: 1170 → ~850 lines (27% reduction)

**Next Actions:** Analyze remaining 9 CRITICAL files (in priority order)

---

## Fix Planning Methodology

### Evaluation Framework (from D10 dimension guide)

For each CRITICAL file, we perform:

**1. Purpose Analysis:**
- What is the primary purpose of this file?
- Does it serve multiple distinct purposes?
- Is it a router, guide, reference, or template?

**2. Content Analysis:**
- Does content have natural subdivisions? (phases, iterations, categories)
- Is there duplicate content across sections?
- Are there detailed examples that could be extracted?
- Are there reference materials that could live elsewhere?

**3. Usage Analysis:**
- How do agents use this file? (read once, reference repeatedly, etc.)
- Do agents need ALL content at once, or only portions?
- Is file referenced in contexts where only portion is relevant?

**4. Reduction Strategy Selection:**
- Strategy 1: Extract to Sub-Guides (for natural subdivisions)
- Strategy 2: Extract to Reference Files (for detailed examples/references)
- Strategy 3: Consolidate Redundant Content (remove duplication)
- Strategy 4: Condense Verbose Sections (tighten language)

---

## QUICK WIN 1: reference/stage_2/refinement_examples.md

### Current State

**File:** `feature-updates/guides_v2/reference/stage_2/refinement_examples.md`
**Size:** 1396 lines
**Over Threshold:** 396 lines (1000-line CRITICAL threshold)
**Category:** CRITICAL - MUST reduce

### Analysis

**Purpose Analysis:**
- **Primary Purpose:** Detailed examples for S2.P3 Refinement Phase execution
- **File Type:** Reference examples (not sequential workflow)
- **Usage Pattern:** Referenced from stages/s2/s2_p3_refinement.md when agents need examples

**Content Analysis:**
- **Natural Subdivisions:** ✅ YES - 4 distinct phases with examples:
  - Phase 3 Examples: Interactive Question Resolution (lines 23-415: 392 lines)
  - Phase 4 Examples: Dynamic Scope Adjustment (lines 415-610: 195 lines)
  - Phase 5 Examples: Cross-Feature Alignment (lines 610-947: 337 lines)
  - Phase 6 Examples: Acceptance Criteria & User Approval (lines 947-1396: 449 lines)
- **Duplicate Content:** No
- **Examples:** Entire file is examples (extraction already done)
- **Reference Material:** No separate reference material

**Usage Analysis:**
- **How Agents Use:** Reference when executing specific phases (not all at once)
- **Need All Content:** No - only need examples for current phase
- **Context:** Referenced with `See: reference/stage_2/refinement_examples.md` from phase guides

**Evaluation:**
- ❌ 1396 lines exceeds CRITICAL threshold by 396 lines
- ✅ Clear natural subdivisions (4 phases)
- ✅ Agents don't need all content simultaneously (phase-by-phase usage)
- ✅ Splitting improves usability (agents find relevant examples faster)
- ✅ No duplication or redundant content (just too much in one file)

### Reduction Strategy

**Selected Strategy:** Strategy 1 - Extract to Sub-Guides (phase-based split)

**Implementation Plan:**

**Step 1: Create 4 Phase-Specific Example Files**

1. **refinement_examples_phase3_questions.md** (~392 lines)
   - Extract lines 23-415 (Phase 3 Examples: Interactive Question Resolution)
   - Content: Complete question-answer cycles, agent behavior examples
   - Referenced from: s2_p3_refinement.md Phase 3 section

2. **refinement_examples_phase4_scope.md** (~195 lines)
   - Extract lines 415-610 (Phase 4 Examples: Dynamic Scope Adjustment)
   - Content: Feature splitting, new work discovery examples
   - Referenced from: s2_p3_refinement.md Phase 4 section

3. **refinement_examples_phase5_alignment.md** (~337 lines)
   - Extract lines 610-947 (Phase 5 Examples: Cross-Feature Alignment)
   - Content: Feature comparison, conflict resolution examples
   - Referenced from: s2_p3_refinement.md Phase 5 section

4. **refinement_examples_phase6_approval.md** (~449 lines)
   - Extract lines 947-1396 (Phase 6 Examples: Acceptance Criteria & User Approval)
   - Content: Acceptance criteria templates, approval workflows
   - Referenced from: s2_p3_refinement.md Phase 6 section

**Step 2: Create Router File**

**File:** `refinement_examples.md` (~100-150 lines)

**Content Structure:**
```markdown
# S2 Refinement Phase - Example Library

**Purpose:** Quick navigation to phase-specific refinement examples

**How to Use:**
- Identify which phase you're executing
- Click link to relevant example file
- Return to main guide after reviewing examples

---

## Phase 3: Interactive Question Resolution

**Examples:** [refinement_examples_phase3_questions.md](refinement_examples_phase3_questions.md)

**What's Covered:**
- Complete question-answer cycles (5+ examples)
- Agent behavior for different question types
- Immediate spec/checklist updates after answers
- Common question patterns and anti-patterns

**When to Use:** During S2.P3 Phase 3 when formulating questions or updating specs

---

## Phase 4: Dynamic Scope Adjustment

**Examples:** [refinement_examples_phase4_scope.md](refinement_examples_phase4_scope.md)

**What's Covered:**
- Feature too large - proposing splits (2 examples)
- New work discovered - creating separate features (2 examples)
- Scope reduction strategies

**When to Use:** During S2.P3 Phase 4 when evaluating feature scope

---

## Phase 5: Cross-Feature Alignment

**Examples:** [refinement_examples_phase5_alignment.md](refinement_examples_phase5_alignment.md)

**What's Covered:**
- Complete feature comparison workflows (2 examples)
- Pairwise comparison with conflict resolution
- Alignment without conflicts (clean comparison)

**When to Use:** During S2.P3 Phase 5 when comparing features

---

## Phase 6: Acceptance Criteria & User Approval

**Examples:** [refinement_examples_phase6_approval.md](refinement_examples_phase6_approval.md)

**What's Covered:**
- Acceptance criteria templates (5 feature types)
- User approval workflows
- Handling approval with modifications

**When to Use:** During S2.P3 Phase 6 when creating acceptance criteria or preparing for approval

---

[Navigation back to main guide]
```

**Step 3: Update Cross-References**

**Files to Update:**
- `stages/s2/s2_p3_refinement.md` - Update references to point to specific phase example files
- Any other guides that reference `refinement_examples.md`

**Search Command:**
```bash
cd feature-updates/guides_v2
grep -r "refinement_examples.md" stages/ reference/ templates/
```

**Update Pattern:**
- Old: `See: reference/stage_2/refinement_examples.md`
- New: `See: reference/stage_2/refinement_examples_phase3_questions.md` (phase-specific)

**Step 4: Validate Navigation**

- [ ] All phase example files <600 lines (comprehension threshold)
- [ ] Router file <200 lines (clear navigation)
- [ ] All cross-references updated
- [ ] No broken links
- [ ] Content flow intact (examples still make sense in split files)

### Projected Outcome

**Before:**
```
reference/stage_2/refinement_examples.md: 1396 lines (❌ CRITICAL)
```

**After:**
```
reference/stage_2/refinement_examples.md: ~150 lines (✅ OK - Router)
reference/stage_2/refinement_examples_phase3_questions.md: ~392 lines (✅ OK)
reference/stage_2/refinement_examples_phase4_scope.md: ~195 lines (✅ OK)
reference/stage_2/refinement_examples_phase5_alignment.md: ~337 lines (✅ OK)
reference/stage_2/refinement_examples_phase6_approval.md: ~449 lines (✅ OK)
```

**Total Reduction:** 1396 → 150 lines (main file: 89% reduction)
**All Files Compliant:** ✅ All <600 lines

### Estimated Effort

- **File Creation:** 1.5 hours (4 phase files + router)
- **Cross-Reference Updates:** 0.5 hours
- **Validation:** 0.5 hours
- **Total:** 2.5 hours

### Implementation Commands

```bash
cd feature-updates/guides_v2/reference/stage_2

# Step 1: Create phase-specific files
sed -n '1,22p;23,415p' refinement_examples.md > refinement_examples_phase3_questions.md
# Add header to phase3 file

sed -n '1,22p;415,610p' refinement_examples.md > refinement_examples_phase4_scope.md
# Add header to phase4 file

sed -n '1,22p;610,947p' refinement_examples.md > refinement_examples_phase5_alignment.md
# Add header to phase5 file

sed -n '1,22p;947,$p' refinement_examples.md > refinement_examples_phase6_approval.md
# Add header to phase6 file

# Step 2: Create router file
# Write new router content to refinement_examples.md

# Step 3: Update cross-references
grep -r "refinement_examples.md" ../../../stages/ ../../../reference/ | grep -v ".md:" | cut -d: -f1 | sort -u
# Review each file and update references

# Step 4: Validate
wc -l refinement_examples*.md
git diff --stat
```

---

## QUICK WIN 2: stages/s10/s10_epic_cleanup.md

### Current State

**File:** `feature-updates/guides_v2/stages/s10/s10_epic_cleanup.md`
**Size:** 1170 lines
**Over Threshold:** 170 lines (1000-line CRITICAL threshold)
**Category:** CRITICAL - MUST reduce

### Analysis

**Purpose Analysis:**
- **Primary Purpose:** Stage guide for S10 Epic Cleanup (final epic stage)
- **File Type:** Sequential workflow guide (agents read start-to-finish)
- **Usage Pattern:** Read once when executing S10

**Content Analysis:**
- **Natural Subdivisions:** ✅ YES - 7 STEPs:
  - STEP 1: Pre-Cleanup Verification (lines 271-308: 37 lines)
  - STEP 2: Run Unit Tests (lines 308-352: 44 lines)
  - STEP 2b: Investigate User-Reported Anomalies (lines 352-371: 19 lines)
  - STEP 3: Documentation Verification (lines 371-432: 61 lines)
  - **STEP 4: Guide Update from Lessons Learned (lines 432-505: 74 lines)** ← DUPLICATE CONTENT
  - **STEP 5: Final Commit (lines 505-822: 318 lines)** ← VERBOSE CONTENT
  - STEP 6: Move Epic to done/ (lines 822-971: 149 lines)
  - STEP 7: Final Verification (lines 971-1170: 199 lines)

- **Duplicate Content:** ✅ YES - STEP 4 duplicates s10_p1_guide_update_workflow.md
  - s10_p1_guide_update_workflow.md: 733 lines (dedicated guide)
  - STEP 4 in s10_epic_cleanup.md: 74 lines (overview + details)
  - Duplication: STEP 4 contains "Quick Overview of S10.P1" with priority system, user approval process, scope - all already in dedicated guide

- **Verbose Content:** ✅ YES - STEP 5 (Final Commit) is 318 lines
  - Contains extremely detailed git commit instructions
  - Full commit message templates and examples
  - Reference file exists: reference/stage_10/commit_message_examples.md
  - Much of this content could be condensed with reference to commit examples guide

**Usage Analysis:**
- **How Agents Use:** Read sequentially when executing S10
- **Need All Content:** No - STEP 4 details are in dedicated guide, STEP 5 examples are in reference guide
- **Context:** Final stage, agents follow step-by-step

**Evaluation:**
- ❌ 1170 lines exceeds CRITICAL threshold by 170 lines
- ✅ Clear duplicate content (STEP 4 ~ s10_p1_guide_update_workflow.md)
- ✅ Verbose content with existing reference (STEP 5 ~ commit_message_examples.md)
- ⚠️ Cannot split into sub-files (already a sequential stage guide)
- ✅ Can extract/condense duplicate and verbose content

### Reduction Strategy

**Selected Strategy:** Strategy 3 - Consolidate Redundant Content + Strategy 4 - Condense Verbose Sections

**Implementation Plan:**

**Reduction 1: Extract STEP 4 Duplicate Content**

**Current STEP 4 (74 lines):**
- Objective statement
- "Quick Overview of S10.P1" (7-step list)
- Priority system (P0-P3 definitions)
- User approval process
- Scope
- Time estimate
- Why this matters
- Transition prompt
- Exit conditions checklist

**Revised STEP 4 (~15 lines):**
```markdown
### STEP 4: Guide Update from Lessons Learned (🚨 MANDATORY - S10.P1)

**Objective:** Apply lessons learned from epic to improve guides for future agents using systematic user-approved workflow.

**⚠️ CRITICAL:** This is NOT optional. Every epic must run S10.P1 to continuously improve guides.

**READ THE FULL GUIDE:**
```text
stages/s10/s10_p1_guide_update_workflow.md
```

**Process Overview:**
1. Analyze all lessons_learned.md files (epic + features)
2. Create GUIDE_UPDATE_PROPOSAL.md with prioritized proposals
3. Present each proposal to user for individual approval
4. Apply only approved changes to guides
5. Create separate commit for guide updates

**Time Estimate:** 20-45 minutes

**Exit Condition:** S10.P1 complete (verify guide-updates.txt updated if applicable)

**NEXT:** Proceed to STEP 5 (Final Commit) for epic code

---
```

**Reduction:** 74 lines → 15 lines (59 lines saved)

**Reduction 2: Condense STEP 5 Verbose Content**

**Current STEP 5 (318 lines):**
- 5a. Review All Changes (verification checklist)
- 5b. Stage All Epic Changes (git add commands)
- 5c. Create Commit with Clear Message (DETAILED templates + examples)
- 5d. Verify Commit Successful (git log validation)
- 5e. Push Branch to Remote (push commands)

**Issue:** 5c (Create Commit) is ~200 lines with:
- Full commit message format specification
- Multi-paragraph example commit message
- HEREDOC syntax details
- Reference to commit_message_examples.md (but then duplicates examples anyway)

**Revised STEP 5 (~150 lines):**

Condense 5c by:
- Keep commit message format specification (concise version)
- Keep ONE short example
- Reference commit_message_examples.md for detailed examples and anti-patterns
- Remove redundant example variations
- Keep HEREDOC syntax (necessary)

**Reduction:** 318 lines → 150 lines (168 lines saved)

**Total Reduction:** 59 + 168 = 227 lines saved

### Projected Outcome

**Before:**
```
stages/s10/s10_epic_cleanup.md: 1170 lines (❌ CRITICAL)
```

**After:**
```
stages/s10/s10_epic_cleanup.md: ~943 lines (⚠️ LARGE, but below CRITICAL)
```

**Reduction:** 1170 → 943 lines (227 lines saved: 19% reduction)

**Note:** File still in LARGE category (800-1000 lines), but below CRITICAL threshold (1000 lines). Further reduction may require extracting STEPs to sub-guides, but that would require creating router pattern which might reduce usability for sequential workflow guide. 943 lines is acceptable for comprehensive stage guide per D10 evaluation framework.

### Estimated Effort

- **STEP 4 Extraction:** 0.5 hours (straightforward condensation)
- **STEP 5 Condensing:** 1.0 hours (careful editing to preserve clarity)
- **Validation:** 0.5 hours (verify no information loss)
- **Total:** 2.0 hours

### Implementation Commands

```bash
cd feature-updates/guides_v2/stages/s10

# Step 1: Backup original
cp s10_epic_cleanup.md s10_epic_cleanup.md.backup

# Step 2: Edit STEP 4 (lines 432-505)
# Use Edit tool to replace STEP 4 content with condensed version

# Step 3: Edit STEP 5 (lines 505-822)
# Use Edit tool to condense 5c subsection (commit message details)

# Step 4: Validate
wc -l s10_epic_cleanup.md  # Should be ~943 lines
git diff s10_epic_cleanup.md | head -100  # Review changes

# Step 5: Verify no information loss
# Read condensed STEP 4 - confirm reference to full guide clear
# Read condensed STEP 5 - confirm essential information retained
```

---

## REMAINING ANALYSIS: 9 CRITICAL Files

### Priority Order for Analysis

**Analysis Session 1 (3-4 hours):**
1. stages/s1/s1_epic_planning.md (1116 lines) - Verify extraction status
2. stages/s2/s2_p3_refinement.md (1106 lines) - Verify phase structure
3. stages/s4/s4_epic_testing_strategy.md (1060 lines) - Just over threshold

**Analysis Session 2 (3-4 hours):**
4. stages/s5/s5_p1_i3_integration.md (1239 lines) - Verify iteration scope
5. stages/s5/s5_p3_i1_preparation.md (1145 lines) - Multi-iteration split
6. stages/s5/s5_p3_i2_gates_part1.md (1155 lines) - Gate structure analysis

**Analysis Session 3 (3-4 hours):**
7. stages/s3/s3_cross_feature_sanity_check.md (1354 lines) - Structure analysis
8. stages/s8/s8_p2_epic_testing_update.md (1344 lines) - STEP grouping
9. reference/glossary.md (1446 lines) - Largest file, special handling

**Total Analysis Effort:** 9-12 hours across 3 sessions

### Analysis Template (for remaining files)

For each file, document:

1. **Current State**
   - File path, size, over-threshold amount

2. **Analysis** (4-part framework)
   - Purpose Analysis
   - Content Analysis
   - Usage Analysis
   - Evaluation

3. **Reduction Strategy**
   - Selected strategy (1-4)
   - Implementation plan (detailed steps)
   - Projected outcome (before/after sizes)
   - Estimated effort

4. **Implementation Commands**
   - Specific bash/edit commands for reduction
   - Validation steps

---

## Next Steps

### Immediate Actions

**Complete Quick Wins (Stage 3):**
1. Execute refinement_examples.md split (2.5 hours)
2. Execute s10_epic_cleanup.md condensing (2.0 hours)
3. **Total Quick Wins:** 4.5 hours

**After Quick Wins:**
- Update Stage 1 Discovery with completed reductions
- Verify 2 files now compliant (<1000 lines)
- Remaining CRITICAL files: 9 (down from 11)

### Analysis Schedule

**Session 1:** Files 1-3 (s1, s2, s4) - 3-4 hours analysis
**Session 2:** Files 4-6 (s5 iterations/gates) - 3-4 hours analysis
**Session 3:** Files 7-9 (s3, s8, glossary) - 3-4 hours analysis

**Total Analysis:** 9-12 hours

### Stage 3 Execution (After Analysis)

**After completing all analyses:**
- Execute reductions for 9 remaining files
- Estimated: 15-25 hours (varies by strategy complexity)

---

## Summary

**Stage 2 Fix Planning Status:**
- ✅ **2 quick wins planned** (refinement_examples.md, s10_epic_cleanup.md)
- ⏳ **9 files require analysis** (structured analysis sessions)

**Projected Impact (Quick Wins Only):**
- refinement_examples.md: 1396 → 150 lines (89% reduction)
- s10_epic_cleanup.md: 1170 → 943 lines (19% reduction)
- **Total CRITICAL files reduced:** 11 → 9 (18% progress)

**Next Action:** Proceed to Stage 3 (Apply Fixes) for 2 quick wins, OR continue Stage 2 analysis for remaining 9 files

**Recommendation:** Execute quick wins first (4.5 hours) to get immediate results and verify process, THEN continue analysis sessions for remaining files.

---

**Stage 2 Fix Planning: IN PROGRESS**
**Next Action:** Proceed to Stage 3 for quick wins OR continue analysis for remaining files
