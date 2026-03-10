
**File:** `s6_execution.md`

---

🚨 **MANDATORY READING PROTOCOL**

**Before starting this guide:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

# S6: Implementation Execution

## Table of Contents

1. [Overview](#overview)
2. [File Roles in S6](#file-roles-in-s6)
3. [Critical Rules](#critical-rules)
4. [Prerequisites Checklist](#prerequisites-checklist)
5. [Workflow Overview](#workflow-overview)
6. [Step 1: Interface Verification Protocol (MANDATORY FIRST STEP)](#step-1-interface-verification-protocol-mandatory-first-step)
7. [Step 2: Create Implementation Checklist](#step-2-create-implementation-checklist)
8. [Step 3: Phase-by-Phase Implementation](#step-3-phase-by-phase-implementation)
9. [Special Protocols](#special-protocols)
10. [Step 4: Final Verification](#step-4-final-verification)
11. [Exit Criteria](#exit-criteria)
12. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
13. [Real-World Example](#real-world-example)
14. [README Agent Status Update Requirements](#readme-agent-status-update-requirements)
15. [Prerequisites for S7 (Testing & Review)](#prerequisites-for-s7-testing--review)
16. [Next Stage](#next-stage)

---

## Overview

**What is this guide?**
Implementation Execution is where you write the feature code following the implementation_plan.md, keeping spec.md visible at all times, verifying interfaces before coding, and running tests after each step with mini-QC checkpoints.

**When do you use this guide?**
- S5 complete (Validation Loop passed - 3 consecutive clean rounds achieved)
- implementation_plan.md is validated and ready
- Ready to write feature code

**Key Outputs:**
- ✅ Feature code implemented phase by phase
- ✅ All unit tests passing after each step (100% pass required)
- ✅ implementation_checklist.md updated in real-time
- ✅ Mini-QC checkpoints passed after major components
- ✅ Ready for S7 (Testing & Review) (Post-Implementation)

**Time Estimate:**
Varies by feature complexity (1-4 hours typical)

**Exit Condition:**
S6 is complete when all implementation tasks from implementation_plan.md are implemented, 100% of tests pass, and spec requirements are verified complete via dual verification

---

## File Roles in S6

**Understanding which file serves which purpose:**

**implementation_plan.md = PRIMARY REFERENCE** (~400 lines)
- **What:** Detailed implementation build guide created and user-approved in S5
- **Contains:** Implementation tasks, acceptance criteria, test strategy, phasing plan, dependencies
- **Use during S6:** Follow this file task-by-task for WHAT to implement and HOW to implement it
- **Authority:** User-approved plan - this is your implementation roadmap

**spec.md = CONTEXT REFERENCE** (requirements specification)
- **What:** Feature requirements specification created and user-approved in S2
- **Contains:** Objectives, scope, algorithms, edge cases, acceptance criteria
- **Use during S6:** Keep visible for context, verify code matches requirements, understand WHY
- **Authority:** User-approved requirements - verify against this but implement from implementation_plan.md

**implementation_checklist.md = PROGRESS TRACKER** (~50 lines)
- **What:** Lightweight checklist extracted from implementation_plan.md tasks
- **Contains:** Checkbox list linking spec requirements → implementation tasks
- **Use during S6:** Check off items in real-time as you complete them
- **Authority:** Your progress tracker - update continuously

**Key Principle:** implementation_plan.md tells you HOW to build (primary reference), spec.md tells you WHAT to build (verification), implementation_checklist.md tracks progress.

---

## Critical Rules

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Keep spec.md VISIBLE at all times during implementation
   - Not "consult when needed" - LITERALLY OPEN
   - Check every 5-10 minutes: "Did I consult specs recently?"

2. ⚠️ Interface Verification Protocol FIRST (before writing ANY code)
   - Verify ALL method signatures from source code
   - Copy-paste exact signatures (don't rely on memory)

3. ⚠️ Dual verification for EVERY requirement
   - BEFORE implementing: Read requirement in spec
   - AFTER implementing: Verify code matches spec

4. ⚠️ Run unit tests after each step (100% pass required)
   - Do NOT proceed to next phase with failing tests
   - Fix failures immediately

5. ⚠️ Mini-QC checkpoints after each major component
   - Not same as final QC - lightweight validation
   - Verify: Tests pass, spec requirements met, no regressions

6. ⚠️ Update implementation_checklist.md in REAL-TIME
   - Check off requirements AS YOU IMPLEMENT (not batched)
   - Prevents "forgot to implement requirement X"

7. ⚠️ NO coding from memory
   - Always consult actual spec text before coding
   - Memory degrades in minutes

8. ⚠️ Configuration Change Checkpoint (if modifying config)
   - Verify backward compatibility
   - Check ALL consumers of config
   - Document migration path

9. ⚠️ If ANY test fails → STOP, fix, re-run before proceeding

10. ⚠️ Create implementation_checklist.md FIRST
   - Must be created BEFORE writing ANY code
   - Track progress in real-time as you implement
   - Historical case: Agent skipped checklist creation, caught in Validation Round 1
```

---

## Prerequisites Checklist

**Verify BEFORE starting S6:**

- [ ] S5 complete:
  - Validation Loop passed (3 consecutive clean rounds achieved)
  - implementation_plan.md validated and complete
  - Gate 5 approval obtained from user
- [ ] All unit test files created (from implementation_plan.md test tasks)
- [ ] spec.md is accessible and will be kept open
- [ ] implementation_checklist.md created from implementation_plan.md
- [ ] No blockers in feature README.md Agent Status

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S6
- Return to S5 to complete missing items
- Document blocker in Agent Status

---

## Workflow Overview

```text
┌──────────────────────────────────────────────────────────────┐
│            STAGE 6 WORKFLOW (Implementation Execution)       │
└──────────────────────────────────────────────────────────────┘

Step 1: Interface Verification Protocol (MANDATORY FIRST)
   ├─ Read ALL external dependency source code
   ├─ Copy-paste exact method signatures
   ├─ Document verified interfaces
   └─ Create interface contract table

Step 2: Create Implementation Checklist
   ├─ Extract all tasks from implementation_plan.md
   ├─ Create checklist in implementation_checklist.md
   ├─ Link each requirement to implementation task
   └─ ⚠️ DO NOT PROCEED TO STEP 3 WITHOUT THIS FILE CREATED

Step 3: Phase-by-Phase Implementation
   ├─ For EACH phase (from implementation_plan.md "Implementation Phasing"):
   │  ├─ Read spec requirements for this phase
   │  ├─ Keep spec VISIBLE while coding
   │  ├─ Implement tasks for this phase
   │  ├─ Update implementation_checklist.md (check off requirements)
   │  ├─ Run unit tests for this phase
   │  ├─ Mini-QC checkpoint
   │  └─ If tests pass: Proceed to next phase
   │     If tests fail: Fix and re-run
   └─ Repeat for all phases

Step 4: Final Verification
   ├─ All implementation tasks complete
   ├─ All unit tests passing (100%)
   ├─ All requirements checked off
   └─ Ready for S7 (Testing & Review)

Mark S6 Complete
   └─ Update feature README.md
```

---

## Step 1: Interface Verification Protocol (MANDATORY FIRST STEP)

**Purpose:** Verify ALL external interfaces BEFORE writing any code

**⚠️ CRITICAL:** "Never assume interface - always verify"

### Process:

1. **List all external dependencies from implementation_plan.md:**

From implementation_plan.md, extract all external methods/classes you'll call:

```markdown
External Dependencies to Verify:
1. ConfigManager.get_rank_multiplier(rank: int)
2. csv_utils.read_csv_with_validation(filepath, required_columns)
3. DataRecord class (will add fields)
4. RecordManager.load_records() (will modify)
```

2. **For EACH dependency, READ actual source code:**

**DO NOT ASSUME - OPEN THE FILE AND READ IT**

```bash
## Example: Verify ConfigManager.get_rank_multiplier
code [module]/util/ConfigManager.py:234
```

3. **Copy-paste EXACT signature:**

```python
## [module]/util/ConfigManager.py:234
def get_rank_multiplier(self, rank: int) -> Tuple[float, int]:
    """
    Calculate rank multiplier based on rank value.

    Args:
        rank (int): rank value (1-500)

    Returns:
        Tuple[float, int]: (multiplier, rating)
            multiplier: Score adjustment factor (0.8-1.2)
            rating: Confidence rating (0-100)
    """
    # ... implementation
    return (multiplier, rating)
```

4. **Document in interface contract table:**

Create `feature_{N}_{name}_interface_contracts.md`:

```markdown
## Feature {N}: {Name} - Verified Interface Contracts

**Purpose:** Document ALL external interfaces verified from source code

**Verification Date:** {YYYY-MM-DD}

---

## Interface 1: ConfigManager.get_rank_multiplier

**Source:** [module]/util/ConfigManager.py:234

**Signature:**
```
def get_rank_multiplier(self, rank: int) -> Tuple[float, int]
```markdown

**Parameters:**
- `rank` (int): rank value value
  - Valid range: 1-500
  - Type: int (NOT float, NOT str)

**Returns:**
- Tuple[float, int]
  - [0]: multiplier (float) - Score adjustment (0.8-1.2)
  - [1]: rating (int) - Confidence (0-100)

**Exceptions:**
- None documented (handles invalid input internally)

**Example Usage Found:**
```
## [module]/util/RecordManager.py:456
multiplier, rating = self.config.get_rank_multiplier(item_rank)
```markdown

**Verified:** ✅ Interface matches implementation_plan.md assumptions

---

## Interface 2: csv_utils.read_csv_with_validation

{Repeat for each interface}
```

5. **Verify assumptions match reality:**

Check implementation tasks:
- implementation_plan.md assumed: `get_rank_multiplier(rank: int) -> Tuple[float, int]`
- Actual interface: `get_rank_multiplier(self, rank: int) -> Tuple[float, int]`
- ✅ MATCH

**If mismatch found:**
- Update implementation_plan.md tasks to match reality
- Update spec.md if needed
- Document mismatch in interface contracts file

**Output:** Verified interface contracts document, confidence in interfaces

---

## Step 2: Create Implementation Checklist

**Purpose:** Track requirement completion during implementation

### Process:

1. **Extract all requirements from spec.md:**

Read spec.md sections:
- Objective
- Scope
- Components Affected
- Algorithms
- Edge Cases

2. **Create implementation_checklist.md:**

```markdown
## Feature {N}: {Name} - Implementation Checklist

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**Update this file IN REAL-TIME (not batched at end)**

---

## Requirements from spec.md

### Objective Requirements

- [ ] **REQ-1:** Load rank data from data/rankings/priority.csv
  - Implementation Task: Task 1
  - Implementation: RecordManager.load_rank_data()
  - Verified: {Check after implementing Task 1}

- [ ] **REQ-2:** Match items to rank values
  - Implementation Task: Task 2
  - Implementation: RecordManager._match_item_to_rank()
  - Verified: {Check after implementing Task 2}

---

### Algorithm Requirements

- [ ] **ALG-1:** Use default multiplier 1.0 if item not in rank data
  - Spec: Algorithms section, step 2c
  - Implementation Task: Task 2
  - Implementation: RecordManager._match_item_to_rank() returns None
  - Verified: {Check after implementing}

- [ ] **ALG-2:** Call ConfigManager.get_rank_multiplier for matched items
  - Spec: Algorithms section, step 3
  - Implementation Task: Task 3
  - Implementation: RecordManager._calculate_rank_multiplier()
  - Verified: {Check after implementing}

---

### Edge Case Requirements

- [ ] **EDGE-1:** Handle rank file not found gracefully
  - Spec: Edge Cases section, case 3
  - Implementation Task: Task 11
  - Implementation: RecordManager.load_rank_data() try/except
  - Verified: {Check after implementing}

- [ ] **EDGE-2:** Handle invalid rank value (<1 or >500)
  - Spec: Edge Cases section, case 2
  - Implementation Task: Task 3
  - Implementation: RecordManager._calculate_rank_multiplier() validation
  - Verified: {Check after implementing}

---

{Continue for ALL requirements from spec.md}

---

## Summary

**Total Requirements:** {N}
**Implemented:** {Count of [x] items}
**Remaining:** {Count of [ ] items}

**Last Updated:** {YYYY-MM-DD HH:MM}
```

**Output:** implementation_checklist.md created, ready for real-time updates

---

## Step 3: Phase-by-Phase Implementation

**Purpose:** Implement tasks from implementation_plan.md incrementally with continuous validation

### General Process (Repeat for EACH phase):

#### 3.1: Read Spec Requirements for This Phase

**Before implementing Phase N:**

1. **Open spec.md** (keep it VISIBLE throughout phase)
2. **Read requirements for this phase:**
   - From implementation_plan.md "Implementation Phasing" section
   - Example: Phase 1 = Core Data Loading (Tasks 1, 2)

3. **Read spec sections relevant to these tasks:**
   - Algorithms for these tasks
   - Edge cases for these tasks
   - Data structures for these tasks

#### 3.2: Implement Tasks (Keep Spec VISIBLE)

**Implementation Protocol:**

1. **For EACH task in phase:**

**BEFORE writing code:**
- Read spec requirement (exact text)
- Read implementation task acceptance criteria from implementation_plan.md
- Check interface contracts (verified signatures)

**WHILE writing code:**
- Keep spec.md VISIBLE (other window/split screen)
- Check spec every 5-10 minutes
- Question yourself: "Am I implementing what spec says?"

**AFTER writing code:**
- Re-read spec requirement
- Verify code matches spec EXACTLY
- Check implementation_checklist.md item

**⚠️ Special Case — Dependency Removal Tasks:** When a task removes an import or dependency (X):
1. Remove the import statement (obvious)
2. **ALSO remove ALL code that references X** — conditionals, comparisons, function calls (critical!)
3. Replacement code for X goes in the appropriate later phase/task
4. Phase checkpoint: `grep "X" {file}` to verify ALL references gone

> **Why this matters:** If only the import is removed but referencing code remains, the code fails at runtime with a `NameError` — not at import time. Phase checkpoints that only test `--help` or import will NOT catch this. The bug appears only when the affected code path runs.

2. **Example: Implementing Task 1 (Load Rank Data)**

**Read spec (Algorithms section):**
> "Load rank data from data/rankings/priority.csv"

**Read implementation_plan.md Task 1 acceptance criteria:**
```markdown
- [ ] Function load_rank_data() created in RecordManager
- [ ] Reads file from path: data/rankings/priority.csv
- [ ] Returns List[Tuple[str, str, int]]
- [ ] Handles FileNotFoundError gracefully
- [ ] Validates CSV has required columns: Name, Position, rank priority
- [ ] Logs number of rows loaded
```

**Implement:**

```python
## [module]/util/RecordManager.py

def load_rank_data(self) -> List[Tuple[str, str, int]]:
    """
    Load rank (external rank priority) data from CSV file.

    Returns:
        List[Tuple[str, str, int]]: List of (Name, Position, rank priority) tuples

    Example:
        >>> rank_data = pm.load_rank_data()
        >>> rank_data[0]
        ('Christian McCaffrey', 'RB', 1)
    """
    filepath = self.data_folder / "rankings" / "priority.csv"

    try:
        # Read CSV with validation (from csv_utils)
        df = read_csv_with_validation(
            filepath,
            required_columns=['Name', 'Position', 'Rank'],
            encoding='utf-8'
        )

        # Convert to list of tuples
        rank_data = [
            (row['Name'], row['Position'], int(row['Rank']))
            for _, row in df.iterrows()
        ]

        # Log success
        self.logger.info(f"Loaded {len(rank_data)} rank values from {filepath}")

        return rank_data

    except FileNotFoundError:
        # Graceful degradation (spec.md Edge Cases, case 3)
        self.logger.error(f"rank file not found: {filepath}")
        return []  # Return empty list (not None, not crash)

    except Exception as e:
        # Unexpected error
        self.logger.error(f"Error loading rank data: {e}", exc_info=True)
        return []
```

**Verify against spec:**
- ✅ Loads from data/rankings/priority.csv (spec requirement)
- ✅ Returns List[Tuple[str, str, int]] (implementation_plan.md acceptance criteria)
- ✅ Handles FileNotFoundError (spec Edge Cases, case 3)
- ✅ Validates columns (implementation_plan.md acceptance criteria)
- ✅ Logs row count (implementation_plan.md acceptance criteria)

**Check off in implementation_checklist.md:**

```markdown
- [x] **REQ-1:** Load rank data from data/rankings/priority.csv
  - Implemented: RecordManager.load_rank_data()
  - Verified: 2025-12-30 15:45 (matches spec exactly)
```

3. **Continue for all tasks in phase**

#### 3.3: Run Unit Tests for This Phase

**After implementing all tasks in phase:**

1. **Run tests for this phase:**

```bash
## Run tests for Phase 1 (Data Loading)
python -m pytest tests/[module]/util/test_RecordManager_rank.py::test_load_rank_data_success -v
python -m pytest tests/[module]/util/test_RecordManager_rank.py::test_load_rank_data_file_not_found -v
```

2. **Verify 100% pass rate:**

```bash
tests/[module]/util/test_RecordManager_rank.py::test_load_rank_data_success PASSED
tests/[module]/util/test_RecordManager_rank.py::test_load_rank_data_file_not_found PASSED

========================= 2 passed in 0.15s =========================
```

**✅ All tests passed - proceed to mini-QC**

**❌ If ANY test fails:**
- STOP - Do NOT proceed to next phase
- Fix failing test
- Re-run all phase tests
- Only proceed when 100% pass

3. **Document test results:**

Add to feature README.md:

```markdown
**Phase 1 Test Results:**
- Date: 2025-12-30 16:00
- Tests run: 2
- Tests passed: 2
- Pass rate: 100%
- Status: ✅ PASSED
```

#### 3.4: Mini-QC Checkpoint

**Purpose:** Lightweight validation before next phase (not full QC)

**Checklist:**

- [ ] All tests for this phase pass (100%)
- [ ] Spec requirements for this phase checked off in implementation_checklist.md
- [ ] No regressions (existing tests still pass)
- [ ] Code follows project conventions (imports, naming, docstrings)
- [ ] No obvious bugs (smoke test the functionality)

**Quick smoke test:**

```python
## Quick manual verification
from [module].util.RecordManager import RecordManager
pm = RecordManager(data_folder="data/")
rank_data = pm.load_rank_data()
print(f"Loaded {len(rank_data)} rank values")
print(f"First entry: {rank_data[0]}")
## Expected: Loaded 200+ rankings, First entry valid tuple
```

**If mini-QC passes:**
- ✅ Proceed to next phase
- Document in Agent Status: "Phase 1 complete, mini-QC passed"

**If mini-QC fails:**
- ❌ Fix issues
- Re-run tests
- Re-run mini-QC
- Only proceed when passed

#### 3.5: Repeat for All Phases

**Continue process for Phase 2, 3, 4, etc.:**

Each phase:
- Read spec requirements
- Keep spec VISIBLE
- Implement tasks
- Update implementation_checklist.md
- Run phase tests (100% pass)
- Mini-QC checkpoint
- Proceed to next phase

---

## Special Protocols

### Configuration Change Checkpoint

**If modifying league_config.json or config.py:**

1. **Verify backward compatibility:**

```markdown
## Config Change Impact Analysis

**Config Key Added:** "rank_multiplier_ranges"

**Backward Compatibility:**
- If key missing in old config: Use default value (empty dict)
- Code handles missing key: Yes (get with default)
  ```
  rank_ranges = config.get("rank_multiplier_ranges", {})
  ```markdown

**Migration Path:**
- No migration needed (new feature, not changing existing)
- User can optionally add key for customization

**Consumers:**
- ConfigManager.get_rank_multiplier() - only consumer
- Handles missing key gracefully

**Verification:**
- [x] Tested with old config (key missing) - works
- [x] Tested with new config (key present) - works
```

2. **Check ALL consumers of config:**

Search for all code that reads this config:

```bash
grep -r "rank_multiplier_ranges" --include="*.py"
```

Verify each consumer handles both old and new config.

### Interface Change Protocol

**If modifying existing class/method signatures:**

⚠️ **WARNING:** Interface changes can break existing code

1. **Identify all callers:**

```bash
## Find all callers of method you're modifying
grep -r "\.load_players()" --include="*.py"
```

2. **Verify change is backward compatible:**
   - Adding optional parameter? ✅ Safe
   - Changing parameter type? ❌ Breaking change
   - Changing return type? ❌ Breaking change

3. **If breaking change:**
   - Update ALL callers
   - Update ALL tests

### No Coding from Memory Protocol

**If you find yourself thinking:**
- "I remember what the spec said..."
- "This algorithm is obvious..."
- "I know what this interface returns..."

**STOP - Consult actual sources:**

1. **Re-read spec.md** (don't trust memory)
2. **Re-check interface contracts** (verify signatures)
3. **Re-read implementation task** (check acceptance criteria)

**Why:** Memory degrades in minutes. Historical evidence shows memory-based coding leads to spec violations.

---

## Step 4: Final Verification

**After ALL phases complete:**

### 4.1: Verify All Implementation Tasks Complete

Check implementation_plan.md:

```markdown
## Implementation Status

**Total Tasks:** 30
**Completed:** 30
**Remaining:** 0

✅ All tasks complete
```

### 4.2: Verify All Tests Passing

Run complete test suite for this feature:

```bash
## Run ALL tests for this feature
python -m pytest tests/[module]/util/test_RecordManager_rank.py -v
python -m pytest tests/integration/test_rank_integration.py -v
```

**Required:** 100% pass rate

```bash
========================= 25 passed in 2.15s =========================
```

### 4.3: Verify All Requirements Checked Off

Check implementation_checklist.md:

```markdown
## Summary

**Total Requirements:** 45
**Implemented:** 45
**Remaining:** 0

✅ All requirements implemented and verified
```

### 4.4: Final Smoke Test

Run feature end-to-end:

```bash
python run_[module].py --mode draft
## Verify: Loads rank data, calculates scores, generates recommendations
```

**Expected:** No errors, feature works end-to-end

---

## Exit Criteria

**S6 is complete when ALL of these are true:**

- [ ] Interface Verification Protocol complete (Step 1)
- [ ] implementation_checklist.md created (Step 2)
- [ ] All phases implemented (Step 3):
  - All implementation tasks complete
  - All spec requirements checked off in implementation_checklist.md
- [ ] All unit tests passing (100% pass rate)
- [ ] All mini-QC checkpoints passed
- [ ] Final verification complete (Step 4):
  - All tests passing
  - All requirements implemented
  - End-to-end smoke test passed
- [ ] Feature README.md updated:
  - Agent Status: Phase = POST_IMPLEMENTATION
  - Next Action = Read S7 (Testing & Review) guide
  - All phase test results documented

**If any item unchecked:**
- ❌ S6 is NOT complete
- ❌ Do NOT proceed to S7 (Testing & Review)
- Complete missing items first

---

## Common Mistakes to Avoid

```text
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll keep spec in mind while coding"
   ✅ STOP - Keep spec VISIBLE (literally open in another window)

❌ "I remember the algorithm from the spec"
   ✅ STOP - Re-read the actual spec text (memory degrades)

❌ "Tests are failing but I'll fix them later"
   ✅ STOP - Fix tests NOW before proceeding (100% pass required)

❌ "I'll update implementation_checklist.md when all coding is done"
   ✅ STOP - Update in REAL-TIME as you implement

❌ "ConfigManager.get_rank_multiplier probably returns float"
   ✅ STOP - Verify from interface contracts (it returns Tuple[float, int])

❌ "I'll skip mini-QC, the tests passed"
   ✅ STOP - Mini-QC is MANDATORY after each step

❌ "Implementation looks good, I'll skip final smoke test"
   ✅ STOP - Final smoke test is MANDATORY (tests != E2E workflow)

❌ "One test is failing but the others pass, good enough"
   ✅ STOP - 100% pass rate REQUIRED (not 90%, not 99%)

❌ "I'll verify code matches spec during S7 (Testing & Review)"
   ✅ STOP - Verify NOW as you implement (dual verification)
```

---

## Real-World Example

**Feature:** rank priority Integration

**Step 1: Core Data Loading**

1. Read spec requirement: "Load rank data from CSV"
2. Keep spec.md VISIBLE while coding
3. Implement load_rank_data() method
4. Check off REQ-1 in implementation_checklist.md
5. Run tests: test_load_rank_data_* (2 tests)
   - Result: 2/2 PASSED ✅
7. Mini-QC: Quick smoke test
   - Loaded 200 rankings ✅
8. Proceed to Phase 2

**Step 2: Matching Logic**

1. Read spec algorithm: "Match item to rank ranking"
2. Keep spec.md VISIBLE
3. Implement _match_item_to_rank() method
4. Check off REQ-2, ALG-1 in implementation_checklist.md
5. Run tests: test_match_item_* (3 tests)
   - Result: 3/3 PASSED ✅
7. Mini-QC: Verify matching works
   - Test item matched correctly ✅
8. Proceed to Phase 3

{Continue for all phases}

**Final Verification:**

- All 30 tasks complete ✅
- All 45 requirements checked off ✅
- All 25 tests passing ✅
- End-to-end smoke test passed ✅
- Ready for S7 (Testing & Review) ✅

---

## README Agent Status Update Requirements

**Update feature README.md Agent Status at these points:**

1. ⚡ After completing Step 1 (Interface Verification)
2. ⚡ After completing Step 2 (Implementation Checklist created)
3. ⚡ After completing EACH phase (Phase 1, 2, 3, etc.)
4. ⚡ After EACH mini-QC checkpoint
5. ⚡ After final verification complete (Step 4)
6. ⚡ When marking S6 complete
7. ⚡ After session compaction (re-read timestamp)

---

## Prerequisites for S7 (Testing & Review)

**Before transitioning to S7 (Testing & Review), verify:**

- [ ] S6 completion criteria ALL met
- [ ] All implementation tasks marked complete
- [ ] All tests passing (100%)
- [ ] implementation_checklist.md shows all requirements checked
- [ ] Feature README.md shows:
  - Agent Status: Phase = POST_IMPLEMENTATION
  - All phase test results documented
  - Next Action = Read S7 (Testing & Review) guide

**If any prerequisite fails:**
- ❌ Do NOT transition to S7 (Testing & Review)
- Complete S6 missing items

---

## Next Stage

**After completing S6:**

📖 **READ:** `stages/s7/s7_p1_smoke_testing.md`
🎯 **GOAL:** Validate implementation through smoke testing (3 parts - MANDATORY GATE)
⏱️ **ESTIMATE:** 30-45 minutes

**Then continue with:**
- `stages/s7/s7_p2_qc_rounds.md` - Feature QC Validation Loop (3 consecutive clean rounds)
- `stages/s7/s7_p3_final_review.md` - PR review and lessons learned

**S7 (Testing & Review) will:**
- Execute 3-part smoke testing protocol (MANDATORY)
- Run Feature QC Validation Loop (16 dimensions, 3 consecutive clean rounds)
- Follow PR Validation Loop (11 categories + 7 master dimensions)
- Verify 100% requirement completion
- Fix ALL issues immediately (no restart needed - validation loop approach)

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S7 (Testing & Review).

---

*End of stages/s6/s6_execution.md*
