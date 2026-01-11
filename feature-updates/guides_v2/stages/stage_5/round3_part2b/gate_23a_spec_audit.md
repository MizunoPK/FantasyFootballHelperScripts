# 🚨 Gate 2 (Iteration 23a): Pre-Implementation Spec Audit

**Part of:** STAGE 5ac Part 2b - Round 3 Gate 3
**Gate Type:** MANDATORY (cannot skip)
**Purpose:** Final verification that implementation_plan.md correctly implements spec.md before coding
**Prerequisites:** Iteration 23 complete (Integration Gap Check passed)
**Time Estimate:** 25-35 minutes

---

## 🚨 MANDATORY GATE

**This is Gate 2 - Pre-Implementation Spec Audit**

**CRITICAL:** This iteration has 4 PARTS, ALL 4 must PASS to proceed.

**Failure mode:** If ANY part fails, CANNOT proceed to Iteration 25 until fixed.

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
- Iteration 23a is FINAL check (Day 4-5 of planning)
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

**Section: Week Offset Logic (spec.md lines 90-134)**
6. R6: Load projected points from week_N folder
7. R7: Load actual points from week_N+1 folder
8. R8: Merge projected and actual data by player_id
9. R9: Handle week 18 edge case (no week 19)

**Section: Win Rate Calculation (spec.md lines 135-178)**
10. R10: Compare projected vs actual for each player
11. R11: Calculate win rate as (correct_predictions / total_predictions)
12. R12: Support multiple simulation runs
13. R13: Aggregate results across weeks

**Section: Error Handling (spec.md lines 179-210)**
14. R14: Validate JSON schema before parsing
15. R15: Log errors for debugging
16. R16: Continue processing if single week fails

**Section: Reporting (spec.md lines 211-245)**
17. R17: Generate summary report with win rate
18. R18: Include player-level accuracy metrics
19. R19: Export results to CSV

**Total Requirements:** 19

---
```

---

### STEP 2: Map each requirement to implementation tasks

**For EACH requirement, find corresponding tasks in implementation_plan.md:**

```markdown
## Requirement → Task Mapping

### R1: Load JSON files from sim_data/YYYY/weeks/week_NN/ folders
**Implementation tasks:**
- Task 1.1: Implement `_build_week_folder_path()` to construct folder paths
- Task 1.2: Implement `_load_json_player_data()` to read JSON files
**Status:** ✅ MAPPED

---

### R2: Support years 2018-2024
**Implementation tasks:**
- Task 1.1: Include year parameter in `_build_week_folder_path()`
- Task 1.2: Loop through years 2018-2024 in `_load_json_player_data()`
**Status:** ✅ MAPPED

---

### R3: Support weeks 1-18
**Implementation tasks:**
- Task 1.1: Include week parameter in `_build_week_folder_path()`
- Task 1.2: Loop through weeks 1-18 in `_load_json_player_data()`
**Status:** ✅ MAPPED

---

### R4: Parse JSON structure: {player_id, name, projected_points[], actual_points[]}
**Implementation tasks:**
- Task 1.3: Implement `_parse_player_json()` to extract fields
- Task 1.4: Validate JSON schema with `_validate_json_schema()`
**Status:** ✅ MAPPED

---

### R5: Handle missing week folders gracefully
**Implementation tasks:**
- Task 1.5: Implement `_handle_missing_weeks()` for error handling
- Task 1.6: Add try/except in `_load_json_player_data()`
**Status:** ✅ MAPPED

---

### R6: Load projected points from week_N folder
**Implementation tasks:**
- Task 1.7: Implement `_load_projected_points()` to read week_N
- Task 1.8: Extract projected_points[] array
**Status:** ✅ MAPPED

---

### R7: Load actual points from week_N+1 folder
**Implementation tasks:**
- Task 1.9: Implement `_load_actual_points()` to read week_N+1
- Task 1.10: Extract actual_points[] array
**Status:** ✅ MAPPED

---

### R8: Merge projected and actual data by player_id
**Implementation tasks:**
- Task 1.11: Implement `_merge_projected_actual()` to merge by player_id
- Task 1.12: Handle cases where player_id missing in one dataset
**Status:** ✅ MAPPED

---

### R9: Handle week 18 edge case (no week 19)
**Implementation tasks:**
- Task 1.13: Add special case in `_load_actual_points()` for week 18
- Task 1.14: Use week 18 actual for week 18 (no offset)
**Status:** ✅ MAPPED

---

### R10: Compare projected vs actual for each player
**Implementation tasks:**
- Task 2.1: Implement `_calculate_win_rate()` with comparison logic
- Task 2.2: Loop through players and compare values
**Status:** ✅ MAPPED

---

### R11: Calculate win rate as (correct_predictions / total_predictions)
**Implementation tasks:**
- Task 2.3: Implement win rate formula in `_calculate_win_rate()`
- Task 2.4: Track correct_predictions counter
- Task 2.5: Track total_predictions counter
**Status:** ✅ MAPPED

---

### R12: Support multiple simulation runs
**Implementation tasks:**
- Task 2.6: Add run_count parameter to `run_simulation()`
- Task 2.7: Loop through simulation runs
**Status:** ✅ MAPPED

---

### R13: Aggregate results across weeks
**Implementation tasks:**
- Task 2.8: Implement `_aggregate_weekly_scores()` to combine weeks
- Task 2.9: Calculate overall metrics from weekly data
**Status:** ✅ MAPPED

---

### R14: Validate JSON schema before parsing
**Implementation tasks:**
- Task 1.4: Implement `_validate_json_schema()` with schema checks
- Task 1.15: Call validator before `_parse_player_json()`
**Status:** ✅ MAPPED

---

### R15: Log errors for debugging
**Implementation tasks:**
- Task 3.1: Add logging statements in error handlers
- Task 3.2: Use LoggingManager from utils
**Status:** ✅ MAPPED

---

### R16: Continue processing if single week fails
**Implementation tasks:**
- Task 3.3: Add try/except around week processing loop
- Task 3.4: Log error and continue to next week
**Status:** ✅ MAPPED

---

### R17: Generate summary report with win rate
**Implementation tasks:**
- Task 4.1: Implement `_generate_summary_report()` to create report
- Task 4.2: Include win rate in report output
**Status:** ✅ MAPPED

---

### R18: Include player-level accuracy metrics
**Implementation tasks:**
- Task 4.3: Add player-level accuracy to report
- Task 4.4: Calculate per-player metrics
**Status:** ✅ MAPPED

---

### R19: Export results to CSV
**Implementation tasks:**
- Task 4.5: Implement CSV export in `_generate_summary_report()`
- Task 4.6: Use csv_utils from utils module
**Status:** ✅ MAPPED

---

## Completeness Summary

**Total requirements:** 19
**Requirements mapped to tasks:** 19 ✅
**Requirements NOT mapped:** 0 ✅

**Status:** ✅ PART 1 PASSED - All requirements have implementation tasks

---
```

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
```
Task 1.1: Handle JSON loading
```
**Problem:** "Handle" is vague, no details on what/where/how

**✅ SPECIFIC TASK:**
```
Task 1.1: Implement `_load_json_player_data(week: int, year: int)` in simulation/WinRateSimulator.py
- Construct path: f"simulation/sim_data/{year}/weeks/week_{week:02d}/players.json"
- Open file with json.load()
- Return parsed dictionary
- Raise FileNotFoundError if file missing
```
**Why specific:** Method name, parameters, file location, logic steps, error handling

---

### Verification

```markdown
## Task Specificity Audit

**From implementation_plan.md Implementation Tasks section:**

### Task 1.1: Implement `_build_week_folder_path()`
**Specificity check:**
- ✅ WHAT: Build week folder path
- ✅ WHERE: simulation/WinRateSimulator.py
- ✅ HOW: Construct f"simulation/sim_data/{year}/weeks/week_{week:02d}/"
- ✅ No vague terms
**Status:** ✅ SPECIFIC

---

### Task 1.2: Implement `_load_json_player_data()`
**Specificity check:**
- ✅ WHAT: Load JSON player data
- ✅ WHERE: simulation/WinRateSimulator.py
- ✅ HOW: Call `_build_week_folder_path()`, open JSON file, parse with json.load()
- ✅ No vague terms
**Status:** ✅ SPECIFIC

---

### Task 1.3: Implement `_parse_player_json()`
**Specificity check:**
- ✅ WHAT: Parse player JSON structure
- ✅ WHERE: simulation/WinRateSimulator.py
- ✅ HOW: Extract player_id, name, projected_points[], actual_points[] from dict
- ✅ No vague terms
**Status:** ✅ SPECIFIC

---

[Continue for ALL tasks...]

---

## Specificity Summary

**Total tasks:** {N}
**Specific tasks:** {N} ✅
**Vague tasks:** 0 ✅

**Status:** ✅ PART 2 PASSED - All tasks are specific

---
```

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
## Interface Contract Verification

### Dependency 1: LoggingManager.get_logger()

**Used in:** Task 3.1 (Error logging)

**Implementation plan assumes:**
```python
from utils.LoggingManager import get_logger
logger = get_logger()
logger.error("Error message")
```

**Actual source:** `utils/LoggingManager.py` lines 45-67

**Verified:**
```python
# Actual source code from LoggingManager.py
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get or create a logger instance.

    Args:
        name (Optional[str]): Logger name. If None, returns root logger.

    Returns:
        logging.Logger: Logger instance
    """
    if name is None:
        return logging.getLogger()
    return logging.getLogger(name)
```

**Contract verification:**
- ✅ Parameters: Optional[str] name (plan matches)
- ✅ Return type: logging.Logger (plan matches)
- ✅ Behavior: Returns logger instance (plan matches)
- ✅ Import path: utils.LoggingManager (plan matches)

**Status:** ✅ VERIFIED FROM SOURCE

---

### Dependency 2: csv_utils.write_csv_with_backup()

**Used in:** Task 4.6 (CSV export)

**Implementation plan assumes:**
```python
from utils.csv_utils import write_csv_with_backup
write_csv_with_backup(df, filepath, create_backup=True)
```

**Actual source:** `utils/csv_utils.py` lines 89-123

**Verified:**
```python
# Actual source code from csv_utils.py
def write_csv_with_backup(df: pd.DataFrame,
                          filepath: Union[str, Path],
                          create_backup: bool = True) -> None:
    """Write DataFrame to CSV with optional backup.

    Args:
        df (pd.DataFrame): DataFrame to write
        filepath (Union[str, Path]): Output file path
        create_backup (bool): Create .bak file if file exists

    Returns:
        None
    """
    # Implementation...
```

**Contract verification:**
- ✅ Parameters: df, filepath, create_backup (plan matches)
- ✅ Return type: None (plan matches)
- ✅ Behavior: Writes CSV with backup (plan matches)
- ✅ Import path: utils.csv_utils (plan matches)

**Status:** ✅ VERIFIED FROM SOURCE

---

[Continue for ALL external dependencies...]

---

## Interface Verification Summary

**Total external dependencies:** {N}
**Dependencies verified from source:** {N} ✅
**Dependencies NOT verified:** 0 ✅

**Status:** ✅ PART 3 PASSED - All interfaces verified

---
```

**If ANY dependency not verified:**

```markdown
## ⚠️ PART 3 FAILED - Unverified Interfaces

### Dependency {X}: {method_name}

**Used in:** Task {X.Y}

**Implementation plan assumes:**
```python
{Assumed interface}
```

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

**STOP - Cannot proceed to Iteration 25 until all integration evidence documented**

---
```

---

## Final Gate Decision

**ALL 4 PARTS must PASS to proceed:**

```markdown
---

## ✅ Iteration 23a: Pre-Implementation Spec Audit - ALL 4 PARTS PASSED

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
**Ready for:** Iteration 25 (Spec Validation)

**Next Action:** Read `stages/stage_5/round3_part2b/iterations_24_25_final.md`

---
```

**If ANY part failed:**

```markdown
---

## ❌ Iteration 23a: Pre-Implementation Spec Audit - FAILED

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

**Next Action:** Fix ALL failed parts, re-run Iteration 23a

**CANNOT proceed to Iteration 25 until ALL 4 PARTS PASS**

---
```

---

## Update Agent Status

**If all parts passed:**
```markdown
Progress: Iteration 23a PASSED - ALL 4 PARTS
Gate Status: ✅ GATE 2 PASSED
Next Action: Read stages/stage_5/round3_part2b/iterations_24_25_final.md
```

**If any parts failed:**
```markdown
Progress: Iteration 23a FAILED - {X} parts failed
Gate Status: ❌ BLOCKED
Blockers: {List failed parts}
Next Action: Fix failed parts, re-run Iteration 23a
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

## Next Step

**After Iteration 23a passes (ALL 4 PARTS):**

Proceed to **Iterations 25 and 24 (Final Gates)** in iterations_24_25_final.md

**📖 READ:** `stages/stage_5/round3_part2b/iterations_24_25_final.md`

---

**END OF GATE 23a GUIDE**
