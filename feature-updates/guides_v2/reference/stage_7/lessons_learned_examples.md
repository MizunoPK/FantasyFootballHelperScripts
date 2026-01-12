# Lessons Learned Examples - Stage 7.5

**Purpose:** Examples and guidance for reading and applying lessons learned
**When to use:** Stage 7.5 (Guide Update from Lessons Learned)
**Main Guide:** `stages/stage_7/phase_7.1_guide_update_workflow.md`

---

## Overview

Stage 7.5 (Guide Update from Lessons Learned) requires finding ALL lessons learned files and creating user-approved guide update proposals. This reference provides:
- Examples of what lessons learned files look like
- How to extract guide improvements from lessons
- How lessons map to priority levels (P0-P3)
- How to apply lessons systematically

---

## Example 1: epic_lessons_learned.md Structure

**File:** `feature-updates/done/{epic_name}/epic_lessons_learned.md`

```markdown
# Epic Lessons Learned: improve_draft_helper

**Epic Overview:** Enhanced draft helper with ADP integration, matchup analysis, and performance tracking
**Date Range:** 2025-12-15 - 2025-12-30
**Total Features:** 3

---

## Stage 1 Lessons Learned

**What Went Well:**
- Epic planning with 3 features was appropriate scope
- Feature breakdown was clear and logical
- Git branch creation worked smoothly

**What Could Be Improved:**
- Initial time estimates were too optimistic (15 days actual vs 10 days estimated)
- Should have identified ADP data source earlier

**Guide Improvements Needed:**
- stages/stage_1/epic_planning.md: Add reminder to verify data sources during planning
- Section: "Step 3: Create Epic Folder Structure"
- Update: Add step "Verify all external data sources are accessible"

---

## Stage 2 Lessons Learned (Per Feature)

### Feature 01: ADP Integration

**What Went Well:**
- Deep dive identified CSV format mismatch early
- Consumption tracing revealed all PlayerManager dependencies
- Interface verification caught ESPN API changes

**What Could Be Improved:**
- Could have created more edge case tests (only identified 8, needed 12)

**Guide Improvements Needed:**
- stages/stage_2/feature_deep_dive.md: Add example of CSV format verification
- Section: "Phase 1: Targeted Research"
- Update: Add step "Verify file format matches expectations (headers, encoding, delimiters)"

### Feature 02: Matchup System

**What Went Well:**
- Algorithm definition was clear and implementable
- Edge case analysis caught division-by-zero scenario

**What Could Be Improved:**
- None - Stage 2 worked well for this feature

**Guide Improvements Needed:**
- None identified

---

## Stage 5a Lessons Learned

**What Went Well:**
- 28 verification iterations caught interface mismatches before implementation
- Iteration 4a audit revealed ambiguous spec sections
- Iteration 23a spec audit prevented wrong implementation approach

**What Could Be Improved:**
- Round 2 test coverage iterations could include integration test examples

**Guide Improvements Needed:**
- stages/stage_5/part_5.1.1_round1.md: Add example for nested algorithm traceability
- Section: "Iteration 4: Algorithm Traceability Matrix"
- Update: Add example showing how to trace nested algorithms (algorithm calling other algorithms)

---

## Cross-Epic Insights

**Patterns Observed Across Features:**
1. CSV format verification saves debugging time later
2. Algorithm traceability matrix prevents implementation confusion
3. User approval on acceptance criteria prevents scope drift

**Systemic Improvements:**
- All future epics should verify data sources in Stage 1
- Stage 2 should always include file format verification
- Stage 5a algorithm traceability should show nested algorithm examples

---

## Recommendations for Future Epics

1. **Plan for 1.5x estimated time:** Actual duration often exceeds estimates
2. **Verify data sources early:** Don't wait until Stage 5b to discover format issues
3. **Create 12-15 edge cases:** 8 edge cases is often insufficient
4. **Use acceptance criteria:** Prevents entire features from targeting wrong scope

---
```

**Key Sections to Look For:**
- "Guide Improvements Needed" appears in EVERY stage section
- Each improvement specifies: Guide name, Section, and Update needed
- Cross-Epic Insights identify patterns across multiple features

---

## Example 2: feature lessons_learned.md Structure

**File:** `feature-updates/done/{epic_name}/feature_01_adp_integration/lessons_learned.md`

```markdown
# Feature Lessons Learned: ADP Integration

**Feature:** feature_01_adp_integration
**Epic:** improve_draft_helper
**Date Range:** 2025-12-16 - 2025-12-22

---

## Stage 2: Deep Dive

**What Went Well:**
- Found CSV loader utility quickly using grep
- Interface verification caught ESPN API version change

**What Could Be Improved:**
- Could have documented CSV format earlier

**Guide Improvements Needed:**
- stages/stage_2/feature_deep_dive.md: Add CSV format documentation step
- Section: "Phase 1: Targeted Research"
- Update: "When feature uses CSV data, document expected format (headers, types, encoding) in spec.md"

---

## Stage 5a: TODO Creation

**What Went Well:**
- Algorithm traceability matrix revealed missing validation step
- Iteration 23a caught spec ambiguity about ADP missing data

**What Could Be Improved:**
- None - Stage 5a worked well

**Guide Improvements Needed:**
- None from this stage

---

## Stage 5b: Implementation

**What Went Well:**
- Implementation followed spec exactly
- Test coverage was thorough (98%)

**What Could Be Improved:**
- Should have added integration test during implementation

**Guide Improvements Needed:**
- stages/stage_5/phase_5.2_implementation_execution.md: Add checkpoint for integration tests
- Section: "Phase 3: Implementation Verification"
- Update: "After unit tests pass, create at least 1 integration test for cross-module workflows"

---

## Stage 5c: Post-Implementation

**What Went Well:**
- Smoke testing caught CSV encoding issue
- QC Round 2 found unused import statement

**What Could Be Improved:**
- None - Stage 5c worked well

**Guide Improvements Needed:**
- None from this stage

---
```

**Key Differences from Epic Lessons:**
- Feature lessons are specific to one feature's implementation
- May have guide improvements that epic lessons missed
- Often more technical/detailed than epic-level insights

---

## Example 3: bugfix lessons_learned.md Structure

**File:** `feature-updates/done/{epic_name}/bugfix_high_point_calculation/lessons_learned.md`

```markdown
# Bug Fix Lessons Learned: Point Calculation Error

**Bug Fix:** bugfix_high_point_calculation
**Epic:** improve_draft_helper
**Priority:** high
**Date Range:** 2025-12-28 - 2025-12-29

---

## Stage 2: Deep Dive (Bug Investigation)

**What Went Well:**
- Root cause analysis identified integer division issue quickly
- Test case reproduction was straightforward

**What Could Be Improved:**
- None - bug investigation was efficient

**Guide Improvements Needed:**
- stages/stage_5/bugfix_workflow.md: Add example of integer division bugs
- Section: "Stage 2: Root Cause Analysis"
- Update: "Common bug patterns: integer division (use float division if fractional results needed)"

---

## Stage 5a: TODO Creation

**What Went Well:**
- 28 iterations ensured fix didn't introduce new bugs
- Test coverage included edge cases (zero denominator)

**What Could Be Improved:**
- None - Stage 5a worked well for bug fix

**Guide Improvements Needed:**
- None from this stage

---

## Stage 5c: Post-Implementation

**What Went Well:**
- Smoke testing verified bug fix didn't break other features
- QC rounds confirmed no regression

**What Could Be Improved:**
- None - Stage 5c worked well

**Guide Improvements Needed:**
- None from this stage

---
```

**Key Differences from Feature Lessons:**
- Bug fix lessons focus on investigation and verification
- Often identify common bug patterns for future reference
- May suggest preventive measures for Stage 5a

---

## How to Extract Guide Improvements from Lessons

### Step 1: Find ALL lessons_learned.md Files

Use bash to systematically find all files:

```bash
find feature-updates/done/{epic_name} -name "lessons_learned.md" -type f
```

**Expected Results:**
```
feature-updates/done/improve_draft_helper/epic_lessons_learned.md
feature-updates/done/improve_draft_helper/feature_01_adp_integration/lessons_learned.md
feature-updates/done/improve_draft_helper/feature_02_matchup_system/lessons_learned.md
feature-updates/done/improve_draft_helper/feature_03_performance_tracker/lessons_learned.md
feature-updates/done/improve_draft_helper/bugfix_high_point_calculation/lessons_learned.md
```

**Total: 5 files** (1 epic + 3 features + 1 bugfix)

---

### Step 2: Read EACH File Systematically

For EACH file found, read it completely and extract "Guide Improvements Needed" sections.

**Example extraction from epic_lessons_learned.md:**

```markdown
**Reading:** feature-updates/done/improve_draft_helper/epic_lessons_learned.md

**Lessons Found:**
1. Stage 1 Lesson: Verify data sources during planning
   - Guide: stages/stage_1/epic_planning.md
   - Section: Step 3: Create Epic Folder Structure
   - Update: Add step to verify external data sources accessible

2. Stage 2 Lesson: Add CSV format verification example
   - Guide: stages/stage_2/feature_deep_dive.md
   - Section: Phase 1: Targeted Research
   - Update: Add step for CSV format verification

3. Stage 5a Lesson: Add nested algorithm traceability example
   - Guide: stages/stage_5/part_5.1.1_round1.md
   - Section: Iteration 4: Algorithm Traceability Matrix
   - Update: Show example of tracing nested algorithms

**Total Lessons from This File:** 3
```

---

### Step 3: Create Master Checklist

Combine ALL lessons from ALL files:

```markdown
## Master Checklist: Guide Updates from Epic improve_draft_helper

**Total Files Checked:** 5
**Total Lessons Found:** 6

**Source: epic_lessons_learned.md (3 lessons)**
□ Lesson 1: Verify data sources in Stage 1
  - Guide: stages/stage_1/epic_planning.md
  - Section: Step 3
  - Update: Add data source verification step

□ Lesson 2: CSV format verification in Stage 2
  - Guide: stages/stage_2/feature_deep_dive.md
  - Section: Phase 1
  - Update: Add CSV format check step

□ Lesson 3: Nested algorithm example in Stage 5a
  - Guide: stages/stage_5/part_5.1.1_round1.md
  - Section: Iteration 4
  - Update: Add nested algorithm traceability example

**Source: feature_01_adp_integration/lessons_learned.md (2 lessons)**
□ Lesson 4: Document CSV format early
  - Guide: stages/stage_2/feature_deep_dive.md
  - Section: Phase 1
  - Update: Add CSV documentation requirement

□ Lesson 5: Integration test checkpoint
  - Guide: stages/stage_5/phase_5.2_implementation_execution.md
  - Section: Phase 3
  - Update: Add integration test checkpoint

**Source: bugfix_high_point_calculation/lessons_learned.md (1 lesson)**
□ Lesson 6: Integer division bug pattern
  - Guide: stages/stage_5/bugfix_workflow.md
  - Section: Stage 2
  - Update: Add common bug pattern example
```

---

### Step 4: Apply Each Lesson

For each lesson in master checklist:

**Example: Applying Lesson 3 (Nested algorithm example)**

1. **Read current guide:**
   ```bash
   Read feature-updates/guides_v2/stages/stage_5/part_5.1.1_round1.md
   ```

2. **Locate section:**
   - Find "Iteration 4: Algorithm Traceability Matrix"
   - Look for examples section

3. **Add improvement:**
   - Add new example showing nested algorithm tracing
   - Example: "calculate_adp_score() calls get_adp_rank() and apply_multiplier()"

4. **Update guide using Edit tool:**
   ```
   Old: [Current examples section]
   New: [Current examples + nested algorithm example]
   ```

5. **Mark as applied:**
   ```markdown
   [x] Lesson 3: Nested algorithm example in Stage 5a
   ```

---

## Verification: All Lessons Applied

**Before proceeding from Step 4, verify:**

```markdown
## Verification Checklist

□ Found ALL lessons_learned.md files using find command
□ Read EVERY file found (epic + features + bugfixes)
□ Created master checklist with ALL lessons from ALL sources
□ Applied EVERY lesson (none skipped)
□ Each lesson marked [x] APPLIED in checklist
□ Can cite which guide section was updated for each lesson

**Totals:**
- Files checked: {N} (epic: 1, features: {F}, bugfixes: {B})
- Lessons identified: {L}
- Lessons applied: {L}
- Lessons skipped: 0 ✅
- Application rate: 100% ✅
```

**If application rate < 100%:**
- ❌ STOP - Apply remaining lessons
- ❌ Do NOT proceed until ALL lessons integrated

---

## Common Mistakes

### ❌ Mistake 1: Only checking epic_lessons_learned.md

**Wrong approach:**
```
Read epic_lessons_learned.md only
Apply 3 lessons
Mark Step 4 complete
```

**Why wrong:** Feature and bugfix lessons are missed

**Right approach:**
```
Find ALL lessons_learned.md files using find command
Read epic + all features + all bugfixes
Apply ALL lessons (epic: 3, features: 3, bugfixes: 1 = 7 total)
Verify 100% application rate
```

---

### ❌ Mistake 2: Skipping lessons that seem minor

**Wrong reasoning:**
```
Lesson 4 is just about CSV documentation... seems minor, skip it
```

**Why wrong:** Small improvements accumulate, minor issues become major over time

**Right approach:**
```
ALL lessons are valuable
Apply EVERY lesson regardless of perceived importance
100% application rate required
```

---

### ❌ Mistake 3: Not verifying all sources

**Wrong approach:**
```
Read epic lessons: 3 found
Apply 3 lessons
Done!
```

**Missing:** Feature lessons (2) and bugfix lessons (1) = 3 lessons missed!

**Right approach:**
```
Find all files: 5 total (epic: 1, features: 3, bugfixes: 1)
Read all 5 files: 6 lessons total
Apply all 6 lessons
Verify: 5 files checked, 6 lessons applied, 0 skipped
```

---

## Summary

**Key Principles:**
1. **Systematic search:** Use find command to locate ALL lessons_learned.md files
2. **Complete reading:** Read EVERY file found (epic + features + bugfixes)
3. **Master checklist:** Combine ALL lessons into one list
4. **100% application:** Apply EVERY lesson (no skipping)
5. **Verification:** Confirm application rate = 100%

**Sources to Check:**
- Epic: `epic_lessons_learned.md` (1 file)
- Features: `feature_XX_{name}/lessons_learned.md` (N files)
- Bugfixes: `bugfix_{priority}_{name}/lessons_learned.md` (M files)

**Total Files:** 1 + N + M

**Goal:** Extract and apply ALL lessons to improve guides for future epics.

---

**END OF LESSONS LEARNED EXAMPLES**
