# Iteration 19: Integration Gap Check

**Part of:** S5.P3 Part 2b - Round 3 Gate 3
**Purpose:** Verify ALL implementation tasks have integration points (no orphan code)
**Prerequisites:** Round 3 Part 2a started, iterations 14-19 complete
**Time Estimate:** 15-20 minutes

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Overview](#overview)
3. [Purpose](#purpose)
4. [Process](#process)
5. [Integration Verification](#integration-verification)
6. [End-to-End Integration Flow](#end-to-end-integration-flow)
7. [Integration Flow: {Feature Name}](#integration-flow-feature-name)
8. [Integration Verification (Iteration 23)](#integration-verification-iteration-23)
9. [Completion Criteria](#completion-criteria)
10. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
11. [Next Step](#next-step)
12. [🚨 MANDATORY GATE](#-mandatory-gate)
13. [Purpose](#purpose-1)
14. [PART 1: Completeness Verification](#part-1-completeness-verification)
15. [Spec Requirements Inventory](#spec-requirements-inventory)
16. [Requirement → Task Mapping](#requirement--task-mapping)
17. [⚠️ PART 1 FAILED - Missing Implementation Tasks](#️-part-1-failed---missing-implementation-tasks)
18. [PART 2: Specificity Verification](#part-2-specificity-verification)
19. [Task Specificity Audit](#task-specificity-audit)
20. [⚠️ PART 2 FAILED - Vague Tasks Found](#️-part-2-failed---vague-tasks-found)

---


## Prerequisites

**Before starting Iteration 20 (Gate 23a - Part 1):**

- [ ] S5.P3 Round 3 Part 2a started
- [ ] Iterations 14-19 complete (preparation iterations)
- [ ] implementation_plan.md exists with implementation tasks section
- [ ] Working directory: Feature folder

**If any prerequisite fails:**
- Complete missing iterations before starting Gate 23a

---

## Overview

**What is this iteration?**
Iteration 20 is Part 1 of Gate 23a (Pre-Implementation Spec Audit). This iteration performs Integration Gap Check to prevent "orphan code" - code that gets implemented but never called/used.

**Time Estimate:** 15-20 minutes

---

## Purpose

**Integration Gap Check** prevents "orphan code" - code that gets implemented but never called/used.

**Historical Context:**
- Feature 01 implemented `_load_json_player_data()` but no caller existed
- Code written, tested, but never executed in actual feature flow
- Discovered during S7 smoke testing
- Required emergency implementation of caller + integration tests

**This iteration prevents implementing code that won't be used.**

---

## Process

### STEP 1: List all implementation methods/functions from implementation_plan.md

### STEP 1-2: List Methods and Verify Callers

**Create integration verification table:**

```markdown
## Integration Verification

| Method | Caller | Call Site | Status |
|--------|--------|-----------|--------|
| `_load_json_player_data()` | `run_simulation()` | Phase 1 - Data Loading | ✅ HAS CALLER |
| `_build_week_folder_path()` | `_load_json_player_data()` | Inside data loading loop | ✅ HAS CALLER |
| `_parse_player_json()` | `_load_json_player_data()` | After reading JSON | ✅ HAS CALLER |
| `_calculate_win_rate()` | `run_simulation()` | Phase 3 - Calculation | ✅ HAS CALLER |
| ... (continue for all methods) | ... | ... | ... |

**Summary:**
- Total methods: {N}
- Methods with callers: {N}
- Orphan methods: 0 ✅
```

---

### STEP 3: Handle Orphan Code

**If ANY method has NO CALLER:**

1. Verify method is actually needed (check spec.md)
2. Options:
   - Add caller if method needed
   - Remove method from plan if not needed
   - Document as intentionally unused (rare)

3. Update implementation_plan.md with decision

**If NO orphan code:** Proceed to next section

---

## End-to-End Integration Flow

**Document complete integration path:**

```markdown
## Integration Flow: {Feature Name}

**Entry Point:** {main_method()}
   ↓
**Step 1:** {method_1()} loads data
   ↓
**Step 2:** {method_2()} processes data
   ↓
**Step 3:** {method_3()} generates output
   ↓
**Output:** {final_result}
```

**Verify:**
- Each step calls the next
- No gaps in flow
- Output consumed by downstream system

---

## Integration Verification (Iteration 23)

**Date:** {YYYY-MM-DD}
**Status:** ✅ PASSED

**Methods verified:** 12/12
**Methods with callers:** 12
**Orphan methods:** 0

**Integration Flow:**
- Entry point: `run_simulation()` (external)
- Exit point: Return summary report
- Flow completeness: 100%

**Gaps found:** 0

**RESULT:** ✅ All implementation tasks are integrated, no orphan code

---
```

---

## Completion Criteria

**Iteration 23 is COMPLETE when ALL of these are true:**

- [ ] All methods/functions listed from implementation_plan.md
- [ ] Every method has identified caller
- [ ] Orphan code identified (if any)
- [ ] End-to-end flow traced
- [ ] Gaps documented (if any)
- [ ] implementation_plan.md updated with verification results
- [ ] If gaps found → User decision obtained before proceeding

---

## Common Mistakes to Avoid

### ❌ MISTAKE: "I'll assume all methods are called"

**Why this is wrong:**
- Assumptions miss orphan code
- Orphan code discovered during smoke testing = emergency fixes

**What to do instead:**
- ✅ Explicitly verify EACH method has caller
- ✅ Trace caller references from implementation_plan.md
- ✅ Document evidence for each caller

---

### ❌ MISTAKE: "Method is in plan, so it must be needed"

**Why this is wrong:**
- Methods can be planned but not integrated
- "Planned" ≠ "Called"

**What to do instead:**
- ✅ Verify caller exists in implementation tasks
- ✅ If no caller found, recommend removal or add caller

---

## Next Step

**After Iteration 23 completes:**

Proceed to **Iteration 20 (Pre-Implementation Spec Audit - Gate 2)** in gate_23a_spec_audit.md

**📖 READ:** `stages/s5/s5_p3_i2_gates_part1.md`

---

**END OF ITERATION 23 GUIDE**
# 🚨 Gate 2 (Iteration 20): Pre-Implementation Spec Audit

**Part of:** S5.P3 Part 2b - Round 3 Gate 3
**Gate Type:** MANDATORY (cannot skip)
**Purpose:** Final verification that implementation_plan.md correctly implements spec.md before coding
**Prerequisites:** Iteration 23 complete (Integration Gap Check passed)
**Time Estimate:** 25-35 minutes

---

## 🚨 MANDATORY GATE

**This is Gate 2 - Pre-Implementation Spec Audit**

**CRITICAL:** This iteration has 4 PARTS, ALL 4 must PASS to proceed.

**Failure mode:** If ANY part fails, CANNOT proceed to Iteration 21 until fixed.

---

## Purpose

**Pre-Implementation Spec Audit** is the FINAL verification before implementation that:
1. Every spec requirement has implementation tasks
2. Every implementation task is specific (not vague)
3. Every interface contract is verified from actual source code
4. Integration evidence exists for all cross-module dependencies

**This gate prevents:**
- Missing requirements (incomplete implementation)
- Vague tasks (implementation confusion)
- Wrong interface assumptions (integration failures)
- Broken integrations (runtime errors)

**Historical Context (Feature 01):**
- Iteration 4a caught missing requirements early (Day 2 of planning)
- Iteration 20 is FINAL check (Day 4-5 of planning)
- Catches issues missed in earlier iterations
- Last chance before implementation starts

---

## PART 1: Completeness Verification

**Verify ALL spec requirements have implementation tasks**

### STEP 1: List all requirements from spec.md

**Read spec.md and extract ALL requirements:**

```markdown
## Spec Requirements Inventory

**From spec.md:**

### Requirements (by section):

**Section: Data Loading (spec.md lines 45-89)**
1. R1: Load JSON files from sim_data/YYYY/weeks/week_NN/ folders
2. R2: Support years 2018-2024
3. R3: Support weeks 1-18
4. R4: Parse JSON structure: {player_id, name, projected_points[], actual_points[]}
5. R5: Handle missing week folders gracefully

**Section: Week Offset Logic**
6. R6-R9: Week offset logic, data merging, edge cases

**Section: Win Rate Calculation**
10. R10-R13: Win rate calculation, simulation runs, aggregation

**Section: Error Handling**
14. R14-R16: Schema validation, error logging, graceful failures

**Section: Reporting**
17. R17-R19: Report generation, metrics, CSV export

**Total Requirements:** 19

---
```

---

### STEP 2: Map each requirement to implementation tasks

**Create requirement mapping table:**

```markdown
## Requirement → Task Mapping

| Requirement | Implementation Tasks | Status |
|-------------|---------------------|--------|
| R1: Load JSON files | Task 1.1: `_build_week_folder_path()`<br>Task 1.2: `_load_json_player_data()` | ✅ MAPPED |
| R2: Support years 2018-2024 | Task 1.1: Year parameter in path builder<br>Task 1.2: Year loop in loader | ✅ MAPPED |
| R3: Support weeks 1-18 | Task 1.1: Week parameter in path builder<br>Task 1.2: Week loop in loader | ✅ MAPPED |
| R4: Parse JSON structure | Task 1.3: `_parse_player_json()`<br>Task 1.4: `_validate_json_schema()` | ✅ MAPPED |
| ... (continue for all 19) | ... | ... |

**Mapping Summary:**
- Total requirements: 19
- Requirements mapped: 19 ✅
- Requirements NOT mapped: 0 ✅

**If ANY requirement not mapped:**

```markdown
## ⚠️ PART 1 FAILED - Missing Implementation Tasks

### Requirement R{X}: {Description}
**Status:** ❌ NOT MAPPED
**Problem:** No implementation tasks found for this requirement
**Impact:** Requirement will not be implemented
**Fix Required:** Add implementation tasks to implementation_plan.md

**STOP - Cannot proceed to Part 2 until all requirements mapped**

---
```

---

## PART 2: Specificity Verification

**Verify ALL implementation tasks are specific (not vague)**

### Process

**Read EACH task in implementation_plan.md and check:**
- [ ] Does task specify WHAT to implement?
- [ ] Does task specify WHERE to implement (file, method)?
- [ ] Does task specify HOW (algorithm, logic)?
- [ ] Does task avoid vague terms (e.g., "handle", "process", "update")?

**Examples:**

**❌ VAGUE TASK:**
```text
Task 1.1: Handle JSON loading
```
**Problem:** "Handle" is vague, no details on what/where/how

**✅ SPECIFIC TASK:**
```bash
Task 1.1: Implement `_load_json_player_data(week: int, year: int)` in simulation/WinRateSimulator.py
- Construct path: f"simulation/sim_data/{year}/weeks/week_{week:02d}/players.json"
- Open file with json.load()
- Return parsed dictionary
- Raise FileNotFoundError if file missing
```
**Why specific:** Method name, parameters, file location, logic steps, error handling

---

### Verification

### Verification

**Create task specificity table:**

```markdown
## Task Specificity Audit

| Task | WHAT | WHERE | HOW | Vague Terms? | Status |
|------|------|-------|-----|--------------|--------|
| Task 1.1: `_build_week_folder_path()` | Build week folder path | simulation/WinRateSimulator.py | Construct f"sim_data/{year}/weeks/week_{week:02d}/" | No | ✅ SPECIFIC |
| Task 1.2: `_load_json_player_data()` | Load JSON player data | simulation/WinRateSimulator.py | Call path builder, open JSON, parse with json.load() | No | ✅ SPECIFIC |
| Task 1.3: `_parse_player_json()` | Parse player JSON structure | simulation/WinRateSimulator.py | Extract player_id, name, projected_points[], actual_points[] | No | ✅ SPECIFIC |
| ... (continue for all tasks) | ... | ... | ... | ... | ... |

**Specificity Summary:**
- Total tasks: {N}
- Specific tasks: {N} ✅
- Vague tasks: 0 ✅
**If ANY task is vague:**

```markdown
## ⚠️ PART 2 FAILED - Vague Tasks Found

### Task {X.Y}: {Description}
**Status:** ❌ VAGUE
**Problem:** Task uses vague term "{term}" without specifics
**Missing:** {WHAT / WHERE / HOW}
**Fix Required:** Rewrite task with specific details

**Example fix:**
Before: "Handle JSON loading"
After: "Implement `_load_json_player_data(week: int, year: int)` in simulation/WinRateSimulator.py to load JSON from sim_data/{year}/weeks/week_{week:02d}/players.json using json.load()"

**STOP - Cannot proceed to Part 3 until all tasks are specific**

---
```

---

## PART 3: Interface Contract Verification

**Verify ALL interface assumptions are verified from actual source code**

**Purpose:** Prevent wrong interface assumptions (parameters, return types, behavior)

### Process

**For EACH external dependency (method calls to other modules):**
1. Identify dependency in implementation_plan.md
2. Find source file for dependency
3. Read actual source code
4. Verify parameters, return type, behavior match plan
5. Document verification

**Example:**

```markdown
```markdown
## Interface Contract Verification

**Create interface verification table:**

| Dependency | Used In | Source File | Signature | Verified? |
|------------|---------|-------------|-----------|----------|
| LoggingManager.get_logger() | Task 3.1 | utils/LoggingManager.py:45-67 | `def get_logger(name: Optional[str] = None) -> logging.Logger:` | ✅ |
| csv_utils.write_csv_with_backup() | Task 4.6 | utils/csv_utils.py:89-123 | `def write_csv_with_backup(df: pd.DataFrame, filepath: Union[str, Path], create_backup: bool = True) -> None:` | ✅ |
| ... (continue for all dependencies) | ... | ... | ... | ... |

**Example Detailed Verification:**

### Dependency 1: LoggingManager.get_logger()
**Used in:** Task 3.1
**Source:** utils/LoggingManager.py lines 45-67
**Signature:** `def get_logger(name: Optional[str] = None) -> logging.Logger:`
**Verification:**
- ✅ Parameters: Optional[str] name
- ✅ Return type: logging.Logger
- ✅ Import path: utils.LoggingManager
**Status:** ✅ VERIFIED

---

**[Continue this pattern for ALL external dependencies...]**

**Verification Summary:**
- Total dependencies: {N}
- Dependencies verified: {N} ✅
- Dependencies NOT verified: 0 ✅

**If ANY dependency not verified:**

```markdown
## ⚠️ PART 3 FAILED - Unverified Interfaces

### Dependency {X}: {method_name}

**Used in:** Task {X.Y}

**Implementation plan assumes:**
```
{Assumed interface}
```markdown

**Status:** ❌ NOT VERIFIED
**Problem:** Did not verify interface from actual source code
**Risk:** Interface may be wrong (parameters, return type, behavior)
**Fix Required:** Read actual source code and verify interface

**STOP - Cannot proceed to Part 4 until all interfaces verified**

---
```

---

## PART 4: Integration Evidence

**Verify implementation_plan.md shows evidence of integration planning**

### Verification Checklist

```markdown
## Integration Evidence Checklist

**From implementation_plan.md:**

### Algorithm Traceability Matrix
- [ ] Section exists in implementation_plan.md
- [ ] Contains N mappings (spec algorithm → implementation tasks)
- [ ] Every spec algorithm has implementation tasks
**Status:** ✅ PRESENT

---

### Component Dependencies Matrix
- [ ] Section exists in implementation_plan.md
- [ ] Shows cross-module dependencies
- [ ] Lists all external method calls
**Status:** ✅ PRESENT

---

### Integration Gap Check (Iteration 23)
- [ ] Results documented in implementation_plan.md
- [ ] Shows all methods have callers
- [ ] No orphan code identified
**Status:** ✅ PRESENT

---

### Mock Audit (Iteration 22)
- [ ] Results documented in implementation_plan.md
- [ ] All mocks verified against real interfaces
- [ ] Integration test plan defined
**Status:** ✅ PRESENT

---

## Integration Evidence Summary

**Required sections:** 4
**Sections present:** 4 ✅

**Status:** ✅ PART 4 PASSED - Integration evidence documented

---
```

**If ANY section missing:**

```markdown
## ⚠️ PART 4 FAILED - Missing Integration Evidence

### Missing Section: {Section Name}

**Status:** ❌ NOT FOUND
**Problem:** integration_plan.md missing {section name} section
**Impact:** Cannot verify integration planning was done
**Fix Required:** Add {section name} section to implementation_plan.md

**STOP - Cannot proceed to Iteration 21 until all integration evidence documented**

---
```

---

## Final Gate Decision

**ALL 4 PARTS must PASS to proceed:**

```markdown
---

## ✅ Iteration 20: Pre-Implementation Spec Audit - ALL 4 PARTS PASSED

**Audit Date:** {YYYY-MM-DD}

**PART 1: Completeness - ✅ PASSED**
- All 19 requirements mapped to implementation tasks
- 0 requirements missing tasks

**PART 2: Specificity - ✅ PASSED**
- All {N} tasks are specific (what/where/how defined)
- 0 vague tasks

**PART 3: Interface Contracts - ✅ PASSED**
- All {N} external dependencies verified from source code
- 0 unverified interfaces

**PART 4: Integration Evidence - ✅ PASSED**
- All 4 required sections present in implementation_plan.md
- Algorithm Traceability Matrix: ✅
- Component Dependencies Matrix: ✅
- Integration Gap Check: ✅
- Mock Audit: ✅

**GATE 2 STATUS: ✅ PASSED**

**Confidence:** HIGH
**Ready for:** Iteration 21 (Spec Validation)

**Next Action:** Read `stages/s5/s5_p3_i3_gates_part2.md`

---
```

**If ANY part failed:**

```markdown
---

## ❌ Iteration 20: Pre-Implementation Spec Audit - FAILED

**Audit Date:** {YYYY-MM-DD}

**PART 1: Completeness - {✅ PASSED / ❌ FAILED}**
- {Details}

**PART 2: Specificity - {✅ PASSED / ❌ FAILED}**
- {Details}

**PART 3: Interface Contracts - {✅ PASSED / ❌ FAILED}**
- {Details}

**PART 4: Integration Evidence - {✅ PASSED / ❌ FAILED}**
- {Details}

**GATE 2 STATUS: ❌ FAILED**

**Blockers:** {List which parts failed}

**Required Fixes:**
1. {Fix for Part 1 if failed}
2. {Fix for Part 2 if failed}
3. {Fix for Part 3 if failed}
4. {Fix for Part 4 if failed}

**Next Action:** Fix ALL failed parts, re-run Iteration 20

**CANNOT proceed to Iteration 21 until ALL 4 PARTS PASS**

---
```

---

## Update Agent Status

**If all parts passed:**
```markdown
Progress: Iteration 20 PASSED - ALL 4 PARTS
Gate Status: ✅ GATE 2 PASSED
Next Action: Read stages/s5/s5_p3_i3_gates_part2.md
```

**If any parts failed:**
```markdown
Progress: Iteration 20 FAILED - {X} parts failed
Gate Status: ❌ BLOCKED
Blockers: {List failed parts}
Next Action: Fix failed parts, re-run Iteration 20
```

---

## Common Mistakes to Avoid

### ❌ MISTAKE: "I'll skip Part 3, interfaces look right"

**Why this is wrong:**
- Assumptions about interfaces cause integration failures
- Must verify from actual source code

**What to do instead:**
- ✅ Read actual source files
- ✅ Verify parameters, return types, behavior
- ✅ Document verification with line numbers

---

### ❌ MISTAKE: "Task says 'handle X', that's specific enough"

**Why this is wrong:**
- "Handle" is vague - doesn't specify what/where/how
- Vague tasks cause implementation confusion

**What to do instead:**
- ✅ Rewrite task with method name, file location, algorithm steps
- ✅ Every task must answer: what + where + how

---

## Exit Criteria

**Iteration 20 (Gate 23a Part 1) is complete when ALL of these are true:**

- [ ] ALL implementation methods/functions listed from implementation_plan.md
- [ ] EACH method has at least one verified caller
- [ ] ALL orphan code identified and either:
  - Added callers to implementation_plan.md, OR
  - Removed from implementation_plan.md (with justification)
- [ ] Integration verification complete with source file evidence (line numbers)
- [ ] No vague tasks remaining (all tasks specify method name, file, algorithm)
- [ ] Ready to proceed to Part 2 of Gate 23a

**If any criterion unchecked:** Continue iteration until complete

---

## Next Step

**After Iteration 20 passes (ALL 4 PARTS):**

Proceed to **Iterations 25 and 24 (Final Gates)** in s5_p3_i3_gates_part2.md

**📖 READ:** `stages/s5/s5_p3_i3_gates_part2.md`

---

**END OF GATE 23a GUIDE**
