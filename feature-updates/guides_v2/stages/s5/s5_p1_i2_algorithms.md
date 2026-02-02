# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I2: Algorithms (Iterations 4-6 + Gate 4a)

**Purpose:** Map every algorithm in spec.md to exact implementation location, then audit all tasks
**Prerequisites:** Iterations 1-3 complete (iterations_1_3_requirements.md)
**Next:** iterations_5_6_dependencies.md (Data Flow and Consumption)
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`

---

## Overview

Iteration 4 creates the Algorithm Traceability Matrix - a comprehensive mapping of every algorithm in spec.md to its implementation location. This is followed by **Gate 4a**, a mandatory audit ensuring every task has specific acceptance criteria.

**Why This Matters:**
- Prevents "implemented wrong algorithm" bugs
- Ensures spec algorithms aren't forgotten
- Catches vague implementation tasks before implementation begins

**Two Parts:**
1. **Iteration 4:** Create Algorithm Traceability Matrix
2. **Gate 4a:** Mandatory TODO Specification Audit (CANNOT proceed without passing)

---

## Iteration 4: Algorithm Traceability Matrix (CRITICAL)

**Purpose:** Map EVERY algorithm in spec.md to exact implementation location, add "Algorithm Traceability Matrix" section to implementation_plan.md

**⚠️ CRITICAL:** This iteration prevents "implemented wrong algorithm" bugs

**Process:**

### Step 1: Extract ALL Algorithms from spec.md

Extract algorithms from:
- Main algorithms section
- Helper algorithms
- Edge case handling logic
- Error handling procedures

### Step 2: Create Traceability Matrix

**Format:**

| Algorithm (from spec.md) | Spec Section | Implementation Location | Implementation Task | Verified |
|--------------------------|--------------|------------------------|-----------|----------|
| Load ADP data from CSV | Algorithms, step 1 | PlayerManager.load_adp_data() | Task 1 | ✅ |
| Match player to ADP ranking | Algorithms, step 2 | PlayerManager._match_player_to_adp() | Task 2 | ✅ |
| Calculate ADP multiplier | Algorithms, step 3 | PlayerManager._calculate_adp_multiplier() | Task 3 | ✅ |
| Apply multiplier to score | Algorithms, step 4 | FantasyPlayer.calculate_total_score() | Task 4 | ✅ |
| Handle player not in ADP data | Edge Cases, case 1 | PlayerManager._match_player_to_adp() | Task 2 | ✅ |
| Handle invalid ADP value | Edge Cases, case 2 | PlayerManager._calculate_adp_multiplier() | Task 3 | ✅ |
| Handle ADP file missing | Edge Cases, case 3 | PlayerManager.load_adp_data() | Task 1 | ✅ |

**Typical matrix size:** 40+ mappings

### Step 3: Verify Each Algorithm

For EACH algorithm, verify:
- ✅ Algorithm from spec has implementation task
- ✅ Implementation task specifies WHERE to implement
- ✅ Implementation location is specific (file, method, approximate line)

### Step 4: Quote Exact Spec Text in Tasks

**Example:**

```markdown
## Task 3: Calculate ADP Multiplier

**Algorithm from spec.md (Algorithms section, step 3):**

> "For each player:
>    If match found:
>       - Get ADP value (1-500)
>       - Call ConfigManager.get_adp_multiplier(adp_value)
>       - Store multiplier in player.adp_multiplier
>    If NO match found:
>       - Use default multiplier (1.0 = neutral)"

**Implementation:**
- Method: PlayerManager._calculate_adp_multiplier(player: FantasyPlayer) -> float
- Logic:
  1. Get player's adp_value
  2. If adp_value is None: return 1.0
  3. If adp_value < 1 or > 500: log warning, return 1.0
  4. Call self.config.get_adp_multiplier(adp_value)
  5. Extract multiplier from tuple
  6. Return multiplier

**Traceability:** Algorithm #3 in spec.md → Task 3 → PlayerManager._calculate_adp_multiplier()
```

### Step 5: Verify Matrix is Complete

**Verification:**
- Count algorithms in spec: {N}
- Count rows in matrix: {N}
- ✅ All algorithms traced

**Output:** Algorithm Traceability Matrix section added to implementation_plan.md (40+ mappings typical)

**🔄 After Iteration Checkpoint - questions.md Review:**

After completing this iteration, check if you have questions or found answers:

1. **If you discovered NEW uncertainties during this iteration:**
   - Add them to `questions.md` with context
   - Format: Question, context, impact on implementation

2. **If you found ANSWERS to existing questions in questions.md:**
   - Update questions.md to mark question as answered
   - Document the answer and source

3. **If no new questions and no answers found:**
   - No action needed, proceed to next iteration

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

**Update Agent Status:**
```
Progress: Iteration 4/9 (Planning Round 1) complete
Next Action: Iteration 4a - TODO Specification Audit (MANDATORY GATE)
```

---

## 🛑 GATE 4a: TODO Specification Audit (MANDATORY)

**Purpose:** Verify EVERY implementation task has acceptance criteria (no vague tasks)

**⚠️ MANDATORY:** Cannot proceed to Planning Round 2 without passing this audit

### Audit Process

**Step 1: Review EVERY Implementation Task**

Go through implementation_plan.md and check each task.

**Step 2: For EACH Task, Verify It Has:**

Required elements:
- □ **Requirement reference** (which spec section it implements)
- □ **Acceptance criteria** (checklist of what defines "done")
- □ **Implementation location** (file, method, line number)
- □ **Dependencies** (what this task needs, what depends on it)
- □ **Tests** (specific test names that verify this task)

### Examples: Good vs Bad Tasks

**❌ BAD implementation task (vague):**
```markdown
## Task 5: Implement ADP feature

Do the ADP stuff.
```

**Why BAD:**
- No requirement reference
- No acceptance criteria
- No implementation location
- No dependencies
- No tests

**✅ GOOD implementation task (specific):**
```markdown
## Task 5: Integrate ADP multiplier into scoring

**Requirement:** Apply ADP multiplier to total score calculation (spec.md Algorithms section, step 4)

**Acceptance Criteria:**
- [ ] Modified: FantasyPlayer.calculate_total_score() method
- [ ] Multiplies score by self.adp_multiplier
- [ ] Order: base_score * adp_multiplier * injury_multiplier * [other multipliers]
- [ ] If adp_multiplier is None: treat as 1.0 (neutral)
- [ ] Verified: total_score includes ADP contribution

**Implementation Location:**
- File: league_helper/util/FantasyPlayer.py
- Method: calculate_total_score()
- Line: ~230

**Dependencies:**
- Requires: Task 2 complete (adp_multiplier field added)
- Requires: Task 3 complete (_calculate_adp_multiplier implemented)

**Tests:**
- Unit test: test_calculate_total_score_with_adp()
- Unit test: test_calculate_total_score_adp_none()
- Integration test: test_scoring_includes_all_multipliers()
```

**Why GOOD:**
- ✅ Clear requirement reference
- ✅ Specific acceptance criteria (5 items)
- ✅ Exact implementation location
- ✅ Dependencies documented
- ✅ Tests specified

### Step 3: Audit Results

**Count tasks:**
- Total tasks: {N}
- Tasks with complete acceptance criteria: {M}

**Passing Criteria:**
- ✅ **PASS** if M == N (all tasks have criteria)
- ❌ **FAIL** if M < N (some tasks vague)

### If Audit FAILS

**Action Required:**
1. STOP - Do NOT proceed to next iteration
2. Fix vague tasks (add missing acceptance criteria)
3. Re-run Iteration 4a audit
4. Document in Agent Status: "Iteration 4a FAILED - fixing vague tasks"

**Continue fixing until PASS**

### If Audit PASSES

**Document in implementation_plan.md:**

```markdown
---

## ✅ Iteration 4a: TODO Specification Audit - PASSED

**Audit Date:** {YYYY-MM-DD}
**Total Tasks:** {N}
**Tasks with Acceptance Criteria:** {N}
**Result:** ✅ PASS - All tasks have specific acceptance criteria

**No vague tasks found. Ready to proceed.**

---
```

**Output:** Verified implementation_plan.md with acceptance criteria for EVERY task

**🔄 After Iteration Checkpoint - questions.md Review:**

After completing this iteration, check if you have questions or found answers:

1. **If you discovered NEW uncertainties during this iteration:**
   - Add them to `questions.md` with context
   - Format: Question, context, impact on implementation

2. **If you found ANSWERS to existing questions in questions.md:**
   - Update questions.md to mark question as answered
   - Document the answer and source

3. **If no new questions and no answers found:**
   - No action needed, proceed to next iteration

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

**Update Agent Status:**
```
Progress: Iteration 4a PASSED (critical gate)
Next Action: Read stages/s5/s5_p1_i2_algorithms.md
```

---

## Checkpoint: After Iteration 4 + Gate 4a

**Before proceeding to Iteration 5:**

**Verify:**
- [ ] Algorithm Traceability Matrix created with 40+ mappings
- [ ] ALL algorithms from spec.md traced to implementation tasks
- [ ] ALL implementation tasks quote exact spec text
- [ ] Gate 4a audit PASSED
- [ ] ALL tasks have requirement references
- [ ] ALL tasks have acceptance criteria checklists
- [ ] ALL tasks have implementation locations
- [ ] ALL tasks have dependencies documented
- [ ] ALL tasks have tests specified

**Files Updated:**
- ✅ implementation_plan.md - Algorithm Traceability Matrix section added
- ✅ implementation_plan.md - All tasks verified with acceptance criteria
- ✅ implementation_plan.md - Gate 4a PASSED documentation added
- ✅ questions.md - Updated with new questions/answers (if any)
- ✅ feature README.md Agent Status - Progress: Iteration 4a PASSED

**Critical Gate:**
- ✅ **Gate 4a PASSED** - Cannot proceed without this

**Next:** Read `stages/s5/s5_p1_i2_algorithms.md` for End-to-End Data Flow and Downstream Consumption

---

**END OF ITERATION 4 + GATE 4a**
