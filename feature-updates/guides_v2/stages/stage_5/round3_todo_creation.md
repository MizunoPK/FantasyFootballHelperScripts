# STAGE 5ac: TODO Creation - Round 3 Guide (ROUTER)

🚨 **IMPORTANT: This guide has been split into focused sub-stages**

**This is a routing guide.** The complete Round 3 workflow is now split across two focused guides:

- **STAGE_5ac Part 1**: Preparation (Iterations 17-22)
- **STAGE_5ac Part 2**: Final Gates (Iterations 23, 23a, 25, 24)

**📖 Read the appropriate sub-stage guide based on your current iteration.**

---

## Quick Navigation

**Use this table to find the right guide:**

| Current Iteration | Guide to Read | Time Estimate |
|-------------------|---------------|---------------|
| Starting Round 3 | stages/stage_5/round3_part1_preparation.md | 60-90 min |
| Iteration 17: Implementation Phasing | stages/stage_5/round3_part1_preparation.md | 10-15 min |
| Iteration 18: Rollback Strategy | stages/stage_5/round3_part1_preparation.md | 10-15 min |
| Iteration 19: Algorithm Traceability (Final) | stages/stage_5/round3_part1_preparation.md | 15-20 min |
| Iteration 20: Performance Considerations | stages/stage_5/round3_part1_preparation.md | 10-15 min |
| Iteration 21: Mock Audit & Integration Test Plan | stages/stage_5/round3_part1_preparation.md | 15-20 min |
| Iteration 22: Output Consumer Validation | stages/stage_5/round3_part1_preparation.md | 10-15 min |
| Iteration 23: Integration Gap Check (Final) | stages/stage_5/round3_part2_final_gates.md | 15-20 min |
| Iteration 23a: Pre-Implementation Spec Audit | stages/stage_5/round3_part2_final_gates.md | 30-45 min |
| Iteration 25: Spec Validation Against Validated Docs | stages/stage_5/round3_part2_final_gates.md | 30-60 min |
| Iteration 24: Implementation Readiness Protocol | stages/stage_5/round3_part2_final_gates.md | 20-30 min |

---

## Round 3 Overview

**What is Round 3?**
Round 3 is the final TODO verification round focused on preparation iterations (phasing, rollback, algorithm traceability, performance, mock audit, output validation) followed by three mandatory gates (Pre-Implementation Spec Audit, Spec Validation Against Validated Documents, and Implementation Readiness Protocol) that determine GO/NO-GO for implementation.

**Total Time Estimate:** 2.5-4 hours (10 iterations across 2 guides, 3 mandatory gates)

**Exit Condition:** Round 3 is complete when ALL preparation iterations (17-22) are done, ALL 3 mandatory gates PASSED (Iterations 23a, 25, 24), and GO decision is made for Stage 5b implementation

---

## Sub-Stage Breakdown

### STAGE_5ac Part 1: Preparation (Iterations 17-22)

**Read:** `stages/stage_5/round3_part1_preparation.md`

**What it covers:**
- **Iteration 17:** Implementation Phasing (break implementation into incremental phases)
- **Iteration 18:** Rollback Strategy (plan for reverting if implementation fails)
- **Iteration 19:** Algorithm Traceability Matrix (Final) (verify ALL algorithms mapped to TODO tasks)
- **Iteration 20:** Performance Considerations (identify O(n²) algorithms, optimize to O(n))
- **Iteration 21:** Mock Audit & Integration Test Plan (verify mocks match real interfaces, plan integration tests)
- **Iteration 22:** Output Consumer Validation (verify outputs match what consumers expect)

**Key Outputs:**
- Implementation phasing plan (5-6 phases for incremental validation)
- Rollback strategy documented
- Algorithm traceability matrix complete (100% coverage)
- Performance optimization plan (identify bottlenecks, optimization strategies)
- Mock audit results (ALL mocks verified against real interfaces)
- Integration test plan (at least 3 tests with REAL objects)
- Output consumer validation results (outputs match consumer expectations)

**Time Estimate:** 60-90 minutes

**When complete:** Transition to STAGE_5ac Part 2

**Why this sub-stage exists:**
- Preparation iterations ensure implementation is well-planned
- Final algorithm traceability prevents missing requirements
- Mock audit prevents interface mismatch bugs
- Performance optimization prevents O(n²) algorithms in production
- Integration test planning ensures tests with real objects (not just mocks)

---

### STAGE_5ac Part 2: Final Gates (Iterations 23, 23a, 25, 24)

**Read:** `stages/stage_5/round3_part2_final_gates.md`

**What it covers:**
- **Iteration 23:** Integration Gap Check (Final) (verify all new methods have callers)
- **Iteration 23a:** Pre-Implementation Spec Audit (MANDATORY GATE - 4 PARTS: Completeness, Specificity, Interface Contracts, Integration Evidence)
- **Iteration 25:** Spec Validation Against Validated Documents (CRITICAL GATE - prevent Feature 02 catastrophic bug)
- **Iteration 24:** Implementation Readiness Protocol (FINAL GATE - GO/NO-GO decision)

**Key Outputs:**
- Integration gap check results (ALL methods have callers, no orphan code)
- Pre-Implementation Spec Audit results (ALL 4 PARTS PASSED):
  - Completeness Audit: Coverage = 100% (all requirements have TODO tasks)
  - Specificity Audit: Specificity = 100% (all tasks have acceptance criteria, implementation location, test coverage)
  - Interface Contracts Audit: Verification = 100% (all dependencies verified against actual source code)
  - Integration Evidence Audit: Integration = 100% (all methods have identified callers)
- Spec validation results (spec.md matches ALL three validated sources):
  - Epic notes (user's original request)
  - Epic ticket (user-validated outcomes from Stage 1)
  - Spec summary (user-validated feature outcomes from Stage 2)
- Implementation readiness decision: ✅ GO or ❌ NO-GO

**Time Estimate:** 1.5-2.5 hours

**When complete:** If GO decision → Transition to Stage 5b (Implementation Execution)

**Why this sub-stage exists:**
- **Contains ALL 3 mandatory gates** that cannot be skipped
- **Iteration 23a**: Evidence-based verification (cite specific numbers, provide proof)
- **Iteration 25**: Three-way validation prevents catastrophic bugs (Feature 02 bug: spec.md misinterpreted epic notes)
- **Iteration 24**: GO/NO-GO framework prevents implementing with incomplete planning
- **User decision required** if any discrepancies found in Iteration 25
- **Cannot proceed to Stage 5b** without GO decision

---

## Why Was Round 3 Split?

**Problem:** Original STAGE_5ac guide was 1,957 lines, making it difficult for agents to navigate efficiently.

**Solution:** Split into two focused sub-stages:
- **Part 1:** Preparation iterations (17-22) - 1,277 lines
- **Part 2:** Final gates (23, 23a, 25, 24) - comprehensive coverage of all mandatory gates

**Benefits:**
- **~50% token reduction per guide** - enables better agent navigation
- **Clear phase focus** - preparation vs validation/decision
- **Easier resumption** - after session compaction, agent can resume at correct part
- **Mandatory gates grouped** - all 3 gates in Part 2 for clear emphasis
- **Better context management** - agents only load relevant content

---

## Mandatory Gates in Round 3

Round 3 contains **3 MANDATORY GATES** that CANNOT be skipped:

### Gate 1: Iteration 23a - Pre-Implementation Spec Audit (4 PARTS)
**Location:** STAGE_5ac Part 2
**Purpose:** Evidence-based verification of TODO quality before implementation
**Requirements:**
- PART 1: Completeness Audit (Coverage = 100%)
- PART 2: Specificity Audit (Specificity = 100%)
- PART 3: Interface Contracts Audit (Verification = 100%)
- PART 4: Integration Evidence Audit (Integration = 100%)
**Pass Criteria:** ALL 4 PARTS must show 100% metrics with evidence (cite specific numbers)

### Gate 2: Iteration 25 - Spec Validation Against Validated Documents
**Location:** STAGE_5ac Part 2
**Purpose:** Prevent catastrophic bugs by validating spec.md against ALL user-validated sources
**Requirements:**
- Close spec.md first (avoid confirmation bias)
- Re-read validated documents independently: epic notes, epic ticket, spec summary
- Ask critical questions (example vs special case, literal vs interpreted)
- Three-way comparison: spec.md vs all three validated sources
- IF ANY DISCREPANCIES → STOP and report to user with 3 options
**Historical Context:** Feature 02 catastrophic bug - spec.md misinterpreted epic notes, implemented wrong solution
**Pass Criteria:** Zero discrepancies with ALL three validated sources

### Gate 3: Iteration 24 - Implementation Readiness Protocol (GO/NO-GO)
**Location:** STAGE_5ac Part 2
**Purpose:** Final decision on whether to proceed to Stage 5b implementation
**Requirements:**
- ALL checklist items checked (spec verification, TODO verification, iterations complete, gates passed)
- Confidence >= MEDIUM
- ALL mandatory gates PASSED (Iterations 4a, 23a all 4 parts, 25)
- Integration verification complete
- Quality gates met (test coverage >90%, performance acceptable)
**Decision:** ✅ GO if all criteria met, ❌ NO-GO if any criteria failed
**Pass Criteria:** GO decision made (cannot proceed to Stage 5b without GO)

---

## Workflow Progression

```
Round 2 (STAGE_5ab) Complete
         ↓
STAGE_5ac Part 1: Preparation
    Iterations 17-22
    (60-90 minutes)
         ↓
STAGE_5ac Part 2: Final Gates
    Iterations 23, 23a, 25, 24
    (1.5-2.5 hours)
         ↓
    3 Mandatory Gates
         ↓
  GO/NO-GO Decision
         ↓
   ✅ GO → Stage 5b (Implementation Execution)
   ❌ NO-GO → Fix issues, return to appropriate iteration
```

---

## Critical Rules

### Always Required

✅ **Read the appropriate sub-stage guide** based on current iteration (use Read tool for ENTIRE guide)
✅ **Complete ALL iterations in sequence** (17 → 18 → 19 → 20 → 21 → 22 → 23 → 23a → 25 → 24)
✅ **Pass ALL 3 mandatory gates** (Iterations 23a all 4 parts, 25, 24)
✅ **Provide evidence-based verification** (cite specific numbers: N requirements, M tasks, coverage %)
✅ **Close spec.md before Iteration 25** (avoid confirmation bias)
✅ **Three-way validation in Iteration 25** (spec.md vs epic notes + epic ticket + spec summary)
✅ **User decision required if discrepancies** (present 3 options in Iteration 25)
✅ **GO decision required to proceed** (cannot start Stage 5b without GO from Iteration 24)

### Never Allowed

❌ **Skip any iteration** (all 10 iterations are mandatory)
❌ **Skip any mandatory gate** (all 3 gates MUST pass)
❌ **Just check boxes without evidence** (must cite specific numbers and provide proof)
❌ **Assume interfaces match mocks** (must READ actual source code in Iteration 21 and 23a Part 3)
❌ **Proceed to Stage 5b with NO-GO** (must fix issues first)
❌ **Make autonomous decisions on discrepancies** (must present 3 options to user in Iteration 25)

---

## Deprecation Notice

**⚠️ ORIGINAL GUIDE DEPRECATED**

The original comprehensive stages/stage_5/round3_todo_creation.md has been renamed to `STAGE_5ac_round3_guide_ORIGINAL_BACKUP.md` and should NOT be used for new work.

**Use the new split guides instead:**
- stages/stage_5/round3_part1_preparation.md
- stages/stage_5/round3_part2_final_gates.md

The split guides provide the same comprehensive coverage with better navigation, token efficiency, and clearer phase focus.

---

## Next Stage

**After Round 3 completes with GO decision:**

**Stage 5b: Implementation Execution**

**Read:** `stages/stage_5/implementation_execution.md`

**What happens in Stage 5b:**
- Execute TODO.md task-by-task
- Keep spec.md visible, continuous verification
- Mini-QC checkpoints every 5-7 TODO items
- 100% test pass required before completing

**Prerequisites for Stage 5b:**
- Round 3 complete (ALL 10 iterations done)
- ALL 3 mandatory gates PASSED (23a all 4 parts, 25, 24)
- GO decision made (Iteration 24)
- todo.md finalized with all 25 iterations incorporated

---

## Additional Resources

**Phase Transition Prompts:**
- See `prompts_reference_v2.md` for mandatory prompts:
  - "Starting Stage 5ac Round 3" (when beginning Round 3)
  - "Starting Stage 5ac Part 1" (when beginning preparation iterations)
  - "Starting Stage 5ac Part 2" (when beginning final gates)

**Templates:**
- See `templates_v2.md` for TODO.md structure

**Workflow Overview:**
- See `EPIC_WORKFLOW_USAGE.md` for complete Stage 5 context

**Guide Index:**
- See `README.md` for all guide locations and quick reference

---

**Remember:** Round 3 is the FINAL verification before implementation. The 3 mandatory gates exist to prevent catastrophic bugs like the Feature 02 bug where spec.md misinterpreted epic notes. Take time to do thorough evidence-based verification - it's faster to catch issues in Round 3 than to fix them in Stage 5c QC rounds.
