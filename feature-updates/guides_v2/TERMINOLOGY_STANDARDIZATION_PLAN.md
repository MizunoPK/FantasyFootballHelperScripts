# Terminology Standardization Plan - 2026-01-11

## Problem Statement

The terms **"Stage"**, **"Phase"**, and **"Iteration"** are used inconsistently throughout the guides:
- **Reserved for S#.P#.I# notation** (hierarchical workflow structure)
- **Also used casually** for implementation steps, process descriptions, and generic references

This creates confusion about whether "Phase 1" means "S#.P1" (hierarchical) or "Step 1" (sequential).

---

## Goal

**Standardize terminology so that Stage/Phase/Iteration are ONLY used for S#.P#.I# notation.**

**For everything else, use:**
- **Step** - Sequential actions within a guide
- **Part** - Subdivisions within a step
- **Round** - Repetitive cycles (QC rounds, investigation rounds)
- **Section** - Document sections
- **Process** - Generic workflows
- **Cycle** - Repeated activities

---

## Categories of Misuse

### Category 1: Implementation Steps (Using "Phase #:")

**Current (INCORRECT):**
```markdown
### Phase 1: Create New Files
### Phase 2: Update Supporting Files
### Phase 3: Update Cross-References
```

**Should be:**
```markdown
### Step 1: Create New Files
### Step 2: Update Supporting Files
### Step 3: Update Cross-References
```

**Files affected:** 40+ instances

**Files to update:**
- `REFACTORING_PLAN_2026_01_11.md` - Implementation Steps section
- `stages/stage_1/epic_planning.md` - Phase 1/2/3/4/5/6 → Step 1/2/3/4/5/6
- `stages/stage_6/phase_6.3_user_testing.md` - Phase 1/2/3/4 → Step 1/2/3/4
- `EPIC_WORKFLOW_USAGE.md` - Phase 1/2/3/4 (bug fix workflow)
- `debugging/*` - Phase 1/2/3/4/4b/5 → Step 1/2/3/4/4b/5
- `missed_requirement/*` - Phase 1/2/3/4 → Step 1/2/3/4
- `prompts/stage_1_prompts.md` - Phase 1-6 → Step 1-6
- `prompts/stage_2_prompts.md` - Phase 1-5 → Step 1-5
- `prompts/special_workflows_prompts.md` - Phase 1-5 → Step 1-5
- `reference/common_mistakes.md` - Phase 1-5 → Step 1-5
- `reference/stage_1/stage_1_reference_card.md` - Phase 1-5 → Step 1-5
- `README.md` - Phase 1-5 → Step 1-5

---

### Category 2: Descriptive "Phase" (Generic Use)

**Current (INCORRECT):**
```markdown
"planning phase"
"execution phase"
"testing phase"
"this phase is complete"
```

**Should be:**
```markdown
"planning step"
"execution step"
"testing step"
"this step is complete"
```

**Files affected:** 10+ instances

**Files to update:**
- `stages/stage_1/epic_planning.md` - "PLANNING phase" → "planning section"
- `stages/stage_2/feature_deep_dive.md` - "Research Phase", "Specification Phase", "Refinement Phase" → keep as-is (these ARE S2.P1, S2.P2, S2.P3)
- `reference/faq_troubleshooting.md` - "Phase 0", "Phase 1", "Phase 2" → "Step 0", "Step 1", "Step 2"
- `reference/stage_2/*` - "Phase 3", "Phase 4", "Phase 5" → "Step 3", "Step 4", "Step 5"

---

### Category 3: Casual "Stage" References

**Current (INCORRECT):**
```markdown
"What is this stage?"
"Before starting this stage:"
"at this stage"
"in this stage"
"during this stage"
"Could this stage have caught"
"None from this stage"
```

**Should be:**
```markdown
"What is this guide?"
"Before starting this guide:"
"at this point"
"in this guide"
"during this process"
"Could this guide have caught"
"None from this section"
```

**Files affected:** 30+ instances

**Files to update:**
- All `stages/*/` files with "What is this stage?" → "What is this guide?"
- All `stages/*/` files with "Before starting this stage:" → "Before starting this guide:"
- `reference/hands_on_data_inspection.md` - "this stage" → "this guide"
- `reference/spec_validation.md` - "this stage" → "this guide"
- `debugging/root_cause_analysis.md` - "Could this stage have caught" → "Could this guide have prevented"
- `reference/stage_7/lessons_learned_examples.md` - "from this stage" → "from this section"

---

### Category 4: Generic "Iteration" Use

**Current (INCORRECT):**
```markdown
"This phase is ITERATIVE"
"iterative refinement"
"iterative cycles"
"Iterative Comprehensive Reviews"
```

**Should be:**
```markdown
"This step repeats"
"repeated refinement"
"repeated cycles"
"Repeated Comprehensive Reviews"
```

**Files affected:** 10+ instances

**Files to update:**
- `debugging/investigation.md` - "ITERATIVE" → "REPEATING"
- `EPIC_WORKFLOW_USAGE.md` - "Iterative Refinement" → "Continuous Refinement"
- `README.md` - "Iterative testing" → "Evolving test planning"
- `reference/faq_troubleshooting.md` - "iterative refinement" → "continuous refinement"
- `stages/stage_5/part_5.3.3_final_review.md` - "Iterative" → "Repeated"
- `stages/s5/s5_pr_review_protocol.md` - "Iterative" → "Repeated"
- `stages/stage_6/phase_6.4_epic_final_review.md` - "Iterative" → "Repeated"

---

### Category 5: Router File Headers (Using "Phase")

**Current (INCORRECT):**
```markdown
### Phase 2.1: Research Phase (Phases 0, 1, 1.5)
### Phase 2.2: Specification Phase (Phases 2, 2.5)
```

**Should be:**
```markdown
### Phase 2.1: Research (Steps 0, 1, 1.5)
### Phase 2.2: Specification (Steps 2, 2.5)
```

**Files affected:**
- `stages/stage_2/feature_deep_dive.md` - Remove "Phase" suffix from "Research Phase"
- `stages/stage_5/phase_5.3_post_implementation.md` - "Phase 1/2/3" → "Part 1/2/3"

---

### Category 6: Debugging Protocol Terminology

**Current (uses "Phase" for steps):**
```markdown
Phase 1: Issue Discovery
Phase 2: Investigation
Phase 3: Solution Design
Phase 4: User Verification
Phase 4b: Root Cause Analysis
Phase 5: Loop Back
```

**Should be:**
```markdown
Step 1: Issue Discovery
Step 2: Investigation
Step 3: Solution Design
Step 4: User Verification
Step 4b: Root Cause Analysis
Step 5: Loop Back
```

**Files affected:**
- `debugging/DEBUGGING_LESSONS_INTEGRATION.md`
- `debugging/root_cause_analysis.md`
- `prompts/special_workflows_prompts.md`
- `README.md`
- `reference/common_mistakes.md`

---

### Category 7: Missed Requirement Protocol Terminology

**Current (uses "Phase" for steps):**
```markdown
Phase 1: Discovery & User Decision
Phase 2: Pause Current Work
Phase 3: Return to Planning Stages
Phase 4: Resume Previous Work
```

**Should be:**
```markdown
Step 1: Discovery & User Decision
Step 2: Pause Current Work
Step 3: Return to Planning Stages
Step 4: Resume Previous Work
```

**Files affected:**
- `missed_requirement/missed_requirement_protocol.md`
- `missed_requirement/discovery.md`
- `missed_requirement/planning.md`
- `missed_requirement/realignment.md`
- `prompts/special_workflows_prompts.md`
- `README.md`

---

## Replacement Strategy

### Global Find/Replace Patterns

**Pattern 1: "Phase #:" in headers**
```
Find:    ### Phase ([0-9]+):
Replace: ### Step \1:
```

**Pattern 2: "Phase #" in text (when NOT S#.P# notation)**
```
Find:    Phase ([0-9]+)([^.])
Replace: Step \1\2
```
*(Only when NOT followed by a period - avoids S#.P# notation)*

**Pattern 3: Descriptive phase references**
```
Find:    "planning phase", "execution phase", "testing phase"
Replace: "planning step", "execution step", "testing step"
```

**Pattern 4: Casual stage references**
```
Find:    "What is this stage?"
Replace: "What is this guide?"

Find:    "Before starting this stage:"
Replace: "Before starting this guide:"

Find:    "at this stage"
Replace: "at this point"

Find:    "in this stage"
Replace: "in this guide"

Find:    "during this stage"
Replace: "during this process"
```

**Pattern 5: Iterative/iteration (generic use)**
```
Find:    "ITERATIVE"
Replace: "REPEATING"

Find:    "iterative refinement"
Replace: "continuous refinement"

Find:    "Iterative Comprehensive Reviews"
Replace: "Repeated Comprehensive Reviews"
```

---

## Reserved Usage (DO NOT CHANGE)

### ✅ Keep "Stage" when referring to S# hierarchy
```markdown
S1: Epic Planning
S5: Feature Implementation
S1, S2, S3, S4, S5, S9, S10
```

### ✅ Keep "Phase" when referring to S#.P# hierarchy
```markdown
Phase 5.1: Implementation Planning
S5.P1, S5.P2, S5.P3
Phase 2.1: Research
S2.P1, S2.P2, S2.P3
```

### ✅ Keep "Iteration" when referring to S#.P#.I# hierarchy
```markdown
S5.P1.I1, S5.P1.I2
Iteration 4 (within S5.P1)
Iterations 1-7 (referring to I#)
```

### ✅ Keep stage/phase in workflow descriptions
```markdown
"After completing S5..."
"Move to Phase 5.2..."
"Complete all 7 stages..."
"S5 has 9 phases..."
```

---

## File-by-File Update List

### High Priority (Most instances)

| File | Instances | Changes |
|------|-----------|---------|
| `REFACTORING_PLAN_2026_01_11.md` | 5 | Phase 1-5 → Step 1-5 (Implementation Steps) |
| `EPIC_WORKFLOW_USAGE.md` | 15+ | Phase 1-4 → Step 1-4 (bug fix), "iterative" → "continuous" |
| `stages/stage_1/epic_planning.md` | 8 | Phase 1-6 → Step 1-6, "planning phase" → "planning section" |
| `stages/stage_6/phase_6.3_user_testing.md` | 6 | Phase 1-4 → Step 1-4 |
| `debugging/DEBUGGING_LESSONS_INTEGRATION.md` | 10+ | Phase 1-5 → Step 1-5 |
| `debugging/investigation.md` | 3 | "ITERATIVE" → "REPEATING" |
| `debugging/root_cause_analysis.md` | 5 | "Phase 4b" → "Step 4b", "this stage" → "this guide" |
| `prompts/special_workflows_prompts.md` | 15+ | Phase 1-5 → Step 1-5 (both protocols) |
| `prompts/stage_1_prompts.md` | 6 | Phase 1-6 → Step 1-6 |
| `prompts/stage_2_prompts.md` | 6 | Phase 1-5 → Step 1-5 |
| `README.md` | 20+ | Phase 1-5 → Step 1-5, "Iterative" → "Evolving" |
| `reference/common_mistakes.md` | 8 | Phase 1-5 → Step 1-5 |
| `reference/stage_1/stage_1_reference_card.md` | 10+ | Phase 1-5 → Step 1-5 |

### Medium Priority

| File | Instances | Changes |
|------|-----------|---------|
| `missed_requirement/missed_requirement_protocol.md` | 8 | Phase 1-4 → Step 1-4 |
| `missed_requirement/discovery.md` | 3 | Phase 1 → Step 1 |
| `missed_requirement/planning.md` | 5 | Phase 2-2.5 → Step 2-2.5 |
| `missed_requirement/realignment.md` | 5 | Phase 3-4 → Step 3-4 |
| `reference/hands_on_data_inspection.md` | 8 | "this stage" → "this guide" |
| `reference/spec_validation.md` | 6 | "this stage" → "this guide" |
| `reference/faq_troubleshooting.md` | 5 | Phase 0-2 → Step 0-2, "iterative" → "continuous" |
| `reference/stage_2/*` | 10+ | Phase 3-6 → Step 3-6 |
| `stages/stage_5/part_5.3.3_final_review.md` | 3 | "Iterative" → "Repeated" |
| `stages/s5/s5_pr_review_protocol.md` | 3 | "Iterative" → "Repeated" |
| `stages/stage_6/phase_6.4_epic_final_review.md` | 2 | "Iterative" → "Repeated" |

### Low Priority (Descriptions)

| File | Instances | Changes |
|------|-----------|---------|
| All `stages/*/` files | 30+ | "What is this stage?" → "What is this guide?" |
| All `stages/*/` files | 30+ | "Before starting this stage:" → "Before starting this guide:" |
| `reference/stage_7/lessons_learned_examples.md` | 4 | "from this stage" → "from this section" |

---

## Special Cases

### S5.3 Post-Implementation

**Current:**
```markdown
Phase 5.3: Post-Implementation
  Phase 1: Smoke Testing
  Phase 2: QC Rounds
  Phase 3: Final Review
```

**Should be:**
```markdown
S10.P1, S10.P2, S10.P3: Post-Implementation
  Part 1: Smoke Testing (S10.P1)
  Part 2: QC Rounds (S10.P2)
  Part 3: Final Review (S10.P3)
```

**Reasoning:** These ARE phases (S10.P1, S10.P2, S10.P3), not generic "phases"

---

### S2 Sub-Phases

**Current:**
```markdown
Phase 2.1: Research Phase (Phases 0, 1, 1.5)
```

**Should be:**
```markdown
S2.P1: Research (Steps 0, 1, 1.5)
```

**Reasoning:** "Phase 2.1" is S2.P1 (hierarchical), but internal "Phases 0, 1, 1.5" are steps

---

### Debugging "Phases"

**Current:**
```markdown
Phase 1: Issue Discovery
Phase 4b: Root Cause Analysis
```

**Should be:**
```markdown
Step 1: Issue Discovery
Step 4b: Root Cause Analysis
```

**Reasoning:** These are sequential steps within the debugging protocol, NOT S#.P# phases

---

## Implementation Order

### Phase 1: High-Priority Files (Core Workflows)
1. Update `REFACTORING_PLAN_2026_01_11.md`
2. Update `EPIC_WORKFLOW_USAGE.md`
3. Update all `prompts/*.md` files
4. Update `README.md`
5. Update `debugging/*` files
6. Update `missed_requirement/*` files

### Phase 2: Stage Guides
1. Update all `stages/stage_*/` files ("What is this stage" → "What is this guide")
2. Update `stages/stage_1/epic_planning.md` (Phase 1-6 → Step 1-6)
3. Update `stages/stage_6/phase_6.3_user_testing.md` (Phase 1-4 → Step 1-4)

### Phase 3: Reference Materials
1. Update all `reference/*` files
2. Update `reference/common_mistakes.md`
3. Update `reference/stage_1/stage_1_reference_card.md`

### Phase 4: Validation
1. Search for remaining "Phase #:" patterns (not S#.P#)
2. Search for casual "stage" usage
3. Search for generic "iteration" usage
4. Verify S#.P#.I# notation unchanged

---

## Testing Plan

### Test 1: Reserved Terms Unchanged
- ✅ "S1", "S5", "S1", "S5" still present
- ✅ "Phase 5.1", "S5.P1", "Phase 2.1" still present
- ✅ "Iteration 4", "S5.P1.I2" still present

### Test 2: Sequential Steps Updated
- ✅ No "Phase 1:", "Phase 2:" (except in S#.P# context)
- ✅ All debugging "Phase" → "Step"
- ✅ All missed requirement "Phase" → "Step"

### Test 3: Casual References Updated
- ✅ "What is this guide?" (not "stage")
- ✅ "Before starting this guide:" (not "stage")
- ✅ No "at this stage", "in this stage"

### Test 4: Generic Iteration Removed
- ✅ No "ITERATIVE" (except in S#.P#.I# context)
- ✅ "Continuous refinement" (not "iterative")
- ✅ "Repeated reviews" (not "iterative")

---

## Estimated Effort

**Files to update:** ~60-70 files

**Replacements:**
- ~150 instances of "Phase #:" → "Step #:"
- ~40 instances of "this stage" → "this guide/point"
- ~15 instances of "iterative" → "continuous/repeated"

**Time estimate:** 3-4 hours (with careful find/replace and validation)

---

## Questions for User

1. **Approve "Step" as replacement for sequential actions?**
2. **Any other terms we should standardize?** (Round, Part, Section?)
3. **Should we do this in same session as S#.P#.I# refactoring or separately?**

---

**Created:** 2026-01-11
**Status:** AWAITING USER APPROVAL
**Estimated Completion:** 3-4 hours after approval
