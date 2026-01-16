# S6: Implementation Execution

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

## Quick Start

**What is this guide?**
Implementation Execution is where you write the feature code following the implementation_plan.md, keeping spec.md visible at all times, verifying interfaces before coding, and running tests after each step with mini-QC checkpoints.

**When do you use this guide?**
- S5a complete (Round 3 Iteration 24 returned "GO")
- implementation_plan.md v3.0 is ready
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
- **What:** Detailed implementation build guide created and user-approved in S5a
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

```
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
```

---

## Prerequisites Checklist

**Verify BEFORE starting S6:**

□ S5a complete:
  - Iteration 24 shows: ✅ GO decision
  - implementation_plan.md v3.0 exists and complete
  - Iteration 23a: ALL 4 PARTS PASSED
□ All unit test files created (from implementation_plan.md test tasks)
□ spec.md is accessible and will be kept open
□ implementation_checklist.md created from implementation_plan.md
□ No blockers in feature README.md Agent Status

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S6
- Return to S5a to complete missing items
- Document blocker in Agent Status

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│            STAGE 5b WORKFLOW (Implementation)                │
└──────────────────────────────────────────────────────────────┘

Step 1: Interface Verification Protocol
   ├─ Read ALL external dependency source code
   ├─ Copy-paste exact method signatures
   ├─ Document verified interfaces
   └─ Create interface contract table

Step 2: Create Implementation Checklist
   ├─ Extract all tasks from implementation_plan.md
   ├─ Create checklist in implementation_checklist.md
   └─ Link each requirement to implementation task

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
1. ConfigManager.get_adp_multiplier(adp: int)
2. csv_utils.read_csv_with_validation(filepath, required_columns)
3. FantasyPlayer class (will add fields)
4. PlayerManager.load_players() (will modify)
```

2. **For EACH dependency, READ actual source code:**

**DO NOT ASSUME - OPEN THE FILE AND READ IT**

```bash
# Example: Verify ConfigManager.get_adp_multiplier
code league_helper/util/ConfigManager.py:234
```

3. **Copy-paste EXACT signature:**

```python
# league_helper/util/ConfigManager.py:234
def get_adp_multiplier(self, adp: int) -> Tuple[float, int]:
    """
    Calculate ADP multiplier based on ADP ranking.

    Args:
        adp (int): ADP ranking (1-500)

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
# Feature {N}: {Name} - Verified Interface Contracts

**Purpose:** Document ALL external interfaces verified from source code

**Verification Date:** {YYYY-MM-DD}

---

## Interface 1: ConfigManager.get_adp_multiplier

**Source:** league_helper/util/ConfigManager.py:234

**Signature:**
```python
def get_adp_multiplier(self, adp: int) -> Tuple[float, int]
```

**Parameters:**
- `adp` (int): ADP ranking value
  - Valid range: 1-500
  - Type: int (NOT float, NOT str)

**Returns:**
- Tuple[float, int]
  - [0]: multiplier (float) - Score adjustment (0.8-1.2)
  - [1]: rating (int) - Confidence (0-100)

**Exceptions:**
- None documented (handles invalid input internally)

**Example Usage Found:**
```python
# league_helper/util/PlayerManager.py:456
multiplier, rating = self.config.get_adp_multiplier(player_adp)
```

**Verified:** ✅ Interface matches implementation_plan.md assumptions

---

## Interface 2: csv_utils.read_csv_with_validation

{Repeat for each interface}
```

5. **Verify assumptions match reality:**

Check implementation tasks:
- implementation_plan.md assumed: `get_adp_multiplier(adp: int) -> Tuple[float, int]`
- Actual interface: `get_adp_multiplier(self, adp: int) -> Tuple[float, int]`
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
# Feature {N}: {Name} - Implementation Checklist

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**Update this file IN REAL-TIME (not batched at end)**

---

## Requirements from spec.md

### Objective Requirements

- [ ] **REQ-1:** Load ADP data from data/rankings/adp.csv
  - Implementation Task: Task 1
  - Implementation: PlayerManager.load_adp_data()
  - Verified: {Check after implementing Task 1}

- [ ] **REQ-2:** Match players to ADP rankings
  - Implementation Task: Task 2
  - Implementation: PlayerManager._match_player_to_adp()
  - Verified: {Check after implementing Task 2}

---

### Algorithm Requirements

- [ ] **ALG-1:** Use default multiplier 1.0 if player not in ADP data
  - Spec: Algorithms section, step 2c
  - Implementation Task: Task 2
  - Implementation: PlayerManager._match_player_to_adp() returns None
  - Verified: {Check after implementing}

- [ ] **ALG-2:** Call ConfigManager.get_adp_multiplier for matched players
  - Spec: Algorithms section, step 3
  - Implementation Task: Task 3
  - Implementation: PlayerManager._calculate_adp_multiplier()
  - Verified: {Check after implementing}

---

### Edge Case Requirements

- [ ] **EDGE-1:** Handle ADP file not found gracefully
  - Spec: Edge Cases section, case 3
  - Implementation Task: Task 11
  - Implementation: PlayerManager.load_adp_data() try/except
  - Verified: {Check after implementing}

- [ ] **EDGE-2:** Handle invalid ADP value (<1 or >500)
  - Spec: Edge Cases section, case 2
  - Implementation Task: Task 3
  - Implementation: PlayerManager._calculate_adp_multiplier() validation
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

2. **Example: Implementing Task 1 (Load ADP Data)**

**Read spec (Algorithms section):**
> "Load ADP data from data/rankings/adp.csv"

**Read implementation_plan.md Task 1 acceptance criteria:**
```
- [ ] Function load_adp_data() created in PlayerManager
- [ ] Reads file from path: data/rankings/adp.csv
- [ ] Returns List[Tuple[str, str, int]]
- [ ] Handles FileNotFoundError gracefully
- [ ] Validates CSV has required columns: Name, Position, ADP
- [ ] Logs number of rows loaded
```

**Implement:**

```python
# league_helper/util/PlayerManager.py

def load_adp_data(self) -> List[Tuple[str, str, int]]:
    """
    Load ADP (Average Draft Position) data from CSV file.

    Returns:
        List[Tuple[str, str, int]]: List of (Name, Position, ADP) tuples

    Example:
        >>> adp_data = pm.load_adp_data()
        >>> adp_data[0]
        ('Christian McCaffrey', 'RB', 1)
    """
    filepath = self.data_folder / "rankings" / "adp.csv"

    try:
        # Read CSV with validation (from csv_utils)
        df = read_csv_with_validation(
            filepath,
            required_columns=['Name', 'Position', 'ADP'],
            encoding='utf-8'
        )

        # Convert to list of tuples
        adp_data = [
            (row['Name'], row['Position'], int(row['ADP']))
            for _, row in df.iterrows()
        ]

        # Log success
        self.logger.info(f"Loaded {len(adp_data)} ADP rankings from {filepath}")

        return adp_data

    except FileNotFoundError:
        # Graceful degradation (spec.md Edge Cases, case 3)
        self.logger.error(f"ADP file not found: {filepath}")
        return []  # Return empty list (not None, not crash)

    except Exception as e:
        # Unexpected error
        self.logger.error(f"Error loading ADP data: {e}", exc_info=True)
        return []
```

**Verify against spec:**
- ✅ Loads from data/rankings/adp.csv (spec requirement)
- ✅ Returns List[Tuple[str, str, int]] (implementation_plan.md acceptance criteria)
- ✅ Handles FileNotFoundError (spec Edge Cases, case 3)
- ✅ Validates columns (implementation_plan.md acceptance criteria)
- ✅ Logs row count (implementation_plan.md acceptance criteria)

**Check off in implementation_checklist.md:**

```markdown
- [x] **REQ-1:** Load ADP data from data/rankings/adp.csv
  - Implemented: PlayerManager.load_adp_data()
  - Verified: 2025-12-30 15:45 (matches spec exactly)
```

3. **Continue for all tasks in phase**

#### 3.3: Run Unit Tests for This Phase

**After implementing all tasks in phase:**

1. **Run tests for this phase:**

```bash
# Run tests for Phase 1 (Data Loading)
python -m pytest tests/league_helper/util/test_PlayerManager_adp.py::test_load_adp_data_success -v
python -m pytest tests/league_helper/util/test_PlayerManager_adp.py::test_load_adp_data_file_not_found -v
```

2. **Verify 100% pass rate:**

```
tests/league_helper/util/test_PlayerManager_adp.py::test_load_adp_data_success PASSED
tests/league_helper/util/test_PlayerManager_adp.py::test_load_adp_data_file_not_found PASSED

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

□ All tests for this phase pass (100%)
□ Spec requirements for this phase checked off in implementation_checklist.md
□ No regressions (existing tests still pass)
□ Code follows project conventions (imports, naming, docstrings)
□ No obvious bugs (smoke test the functionality)

**Quick smoke test:**

```python
# Quick manual verification
from league_helper.util.PlayerManager import PlayerManager
pm = PlayerManager(data_folder="data/")
adp_data = pm.load_adp_data()
print(f"Loaded {len(adp_data)} ADP rankings")
print(f"First entry: {adp_data[0]}")
# Expected: Loaded 200+ rankings, First entry valid tuple
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

**Config Key Added:** "adp_multiplier_ranges"

**Backward Compatibility:**
- If key missing in old config: Use default value (empty dict)
- Code handles missing key: Yes (get with default)
  ```python
  adp_ranges = config.get("adp_multiplier_ranges", {})
  ```

**Migration Path:**
- No migration needed (new feature, not changing existing)
- User can optionally add key for customization

**Consumers:**
- ConfigManager.get_adp_multiplier() - only consumer
- Handles missing key gracefully

**Verification:**
- [x] Tested with old config (key missing) - works
- [x] Tested with new config (key present) - works
```

2. **Check ALL consumers of config:**

Search for all code that reads this config:

```bash
grep -r "adp_multiplier_ranges" --include="*.py"
```

Verify each consumer handles both old and new config.

### Interface Change Protocol

**If modifying existing class/method signatures:**

⚠️ **WARNING:** Interface changes can break existing code

1. **Identify all callers:**

```bash
# Find all callers of method you're modifying
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
# Run ALL tests for this feature
python -m pytest tests/league_helper/util/test_PlayerManager_adp.py -v
python -m pytest tests/integration/test_adp_integration.py -v
```

**Required:** 100% pass rate

```
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
python run_league_helper.py --mode draft
# Verify: Loads ADP data, calculates scores, generates recommendations
```

**Expected:** No errors, feature works end-to-end

---

## Completion Criteria

**S6 is complete when ALL of these are true:**

□ Interface Verification Protocol complete (Step 1)
□ implementation_checklist.md created (Step 2)
□ All phases implemented (Step 3):
  - All implementation tasks complete
  - All spec requirements checked off in implementation_checklist.md
□ All unit tests passing (100% pass rate)
□ All mini-QC checkpoints passed
□ Final verification complete (Step 4):
  - All tests passing
  - All requirements implemented
  - End-to-end smoke test passed
□ Feature README.md updated:
  - Agent Status: Phase = POST_IMPLEMENTATION
  - Next Action = Read S7 (Testing & Review) guide
  - All phase test results documented

**If any item unchecked:**
- ❌ S6 is NOT complete
- ❌ Do NOT proceed to S7 (Testing & Review)
- Complete missing items first

---

## Common Mistakes to Avoid

```
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

❌ "ConfigManager.get_adp_multiplier probably returns float"
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

**Feature:** ADP Integration

**Step 1: Core Data Loading**

1. Read spec requirement: "Load ADP data from CSV"
2. Keep spec.md VISIBLE while coding
3. Implement load_adp_data() method
4. Check off REQ-1 in implementation_checklist.md
5. Run tests: test_load_adp_data_* (2 tests)
   - Result: 2/2 PASSED ✅
7. Mini-QC: Quick smoke test
   - Loaded 200 rankings ✅
8. Proceed to Phase 2

**Step 2: Matching Logic**

1. Read spec algorithm: "Match player to ADP ranking"
2. Keep spec.md VISIBLE
3. Implement _match_player_to_adp() method
4. Check off REQ-2, ALG-1 in implementation_checklist.md
5. Run tests: test_match_player_* (3 tests)
   - Result: 3/3 PASSED ✅
7. Mini-QC: Verify matching works
   - Test player matched correctly ✅
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

□ S6 completion criteria ALL met
□ All implementation tasks marked complete
□ All tests passing (100%)
□ implementation_checklist.md shows all requirements checked
□ Feature README.md shows:
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
- `stages/s7/s7_p2_qc_rounds.md` - 3 QC rounds with restart protocol
- `stages/s7/s7_p3_final_review.md` - PR review and lessons learned

**S7 (Testing & Review) will:**
- Execute 3-part smoke testing protocol (MANDATORY)
- Complete 3 QC rounds (no exceptions)
- Follow PR review protocol (multi-round with fresh eyes)
- Verify 100% requirement completion
- If ANY issues found → COMPLETELY RESTART S7 (Testing & Review)

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S7 (Testing & Review).

---

*End of stages/s5/implementation_execution.md*
