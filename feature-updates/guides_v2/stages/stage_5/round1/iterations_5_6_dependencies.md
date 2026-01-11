# Round 1: Iterations 5-6 - Data Flow & Dependencies

**Purpose:** Trace data flow, verify downstream consumption, and ensure error handling
**Prerequisites:** Iteration 4 + Gate 4a complete (iteration_4_algorithms.md)
**Next:** iteration_7_integration.md (Integration Gap Check)
**Main Guide:** `stages/stage_5/round1_todo_creation.md`

---

## Overview

Iterations 5-6 focus on three critical verification steps:
- **Iteration 5:** End-to-End Data Flow - Trace data from entry to output
- **Iteration 5a:** Downstream Consumption Tracing - Verify how loaded data is CONSUMED (NEW - prevents catastrophic bugs)
- **Iteration 6:** Error Handling Scenarios - Enumerate and handle all error cases

**Why These Matter:**
- Iteration 5 ensures data flows correctly through transformations
- **Iteration 5a prevents "data loads successfully but calculation fails" bugs**
- Iteration 6 ensures graceful degradation instead of crashes

---

## Iteration 5: End-to-End Data Flow

**Purpose:** Trace data from entry point through all transformations to output

**Process:**

### Step 1: Identify Entry Point

Where does data enter this feature?

**Example:** load_adp_data() reads CSV file

### Step 2: Trace Data Flow Step-by-Step

Document the complete data flow:

```markdown
## End-to-End Data Flow: ADP Integration

**Entry Point:**
data/rankings/adp.csv (CSV file)
   ↓
**Step 1: Load (Task 1)**
PlayerManager.load_adp_data() reads CSV
Returns: List[Tuple[str, str, int]] (Name, Position, ADP)
   ↓
**Step 2: Match (Task 2)**
PlayerManager._match_player_to_adp(player) matches player to ADP data
Sets: player.adp_value (int or None)
   ↓
**Step 3: Calculate (Task 3)**
PlayerManager._calculate_adp_multiplier(player) calculates multiplier
Sets: player.adp_multiplier (float)
   ↓
**Step 4: Apply (Task 4)**
FantasyPlayer.calculate_total_score() multiplies score
Returns: total_score (float) with ADP contribution
   ↓
**Output:**
Updated player score used in draft recommendations
```

### Step 3: Verify No Gaps

Check data flows continuously:
- ✅ Data created in Step 1 → used in Step 2
- ✅ Data created in Step 2 → used in Step 3
- ✅ Data created in Step 3 → used in Step 4
- ✅ Output from Step 4 → consumed by downstream system

### Step 4: Identify Data Transformations

Document how data changes:
- CSV text → Python objects (Step 1)
- Player object → ADP value lookup (Step 2)
- ADP value → multiplier (Step 3)
- Multiplier → final score (Step 4)

### Step 5: Add Data Flow Tests to implementation_plan.md

```markdown
## Task 10: End-to-End Data Flow Test

**Requirement:** Verify data flows correctly from CSV to final score

**Test Steps:**
1. Create test CSV: data/test/adp_test.csv
2. Add player "Patrick Mahomes,QB,5"
3. Load ADP data
4. Create FantasyPlayer("Patrick Mahomes", "QB", ...)
5. Match to ADP (should get adp_value=5)
6. Calculate multiplier (should get adp_multiplier from config)
7. Calculate score (should include adp_multiplier)
8. Verify: final score != base score (multiplier applied)

**Acceptance Criteria:**
- [ ] Test data file created
- [ ] All steps execute without error
- [ ] Data flows through all 4 steps
- [ ] Output score reflects ADP contribution
```

**Output:** Data flow diagram, E2E test task added to implementation_plan.md

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
Progress: Iteration 5/9 (Round 1) complete
Next Action: Iteration 5a - Downstream Consumption Tracing (CRITICAL)
```

---

## Iteration 5a: Downstream Data Consumption Tracing (CRITICAL)

**Purpose:** Verify how loaded data is CONSUMED after loading completes

**Historical Context:** Feature 02 catastrophic bug - changed how data was LOADED (CSV → JSON) but missed how data was CONSUMED (week_N_points attributes → actual_points[N] arrays). This resulted in a fully non-functional feature that survived 7 stages because all verification checked data loading, not data consumption.

**This iteration prevents the "data loads successfully but calculation fails" bug.**

---

### Process Overview

**Six-Step Process:**
1. Identify all downstream consumption locations (grep for usage patterns)
2. List OLD access patterns (before this feature)
3. List NEW access patterns (after this feature)
4. Compare OLD vs NEW - identify breaking changes
5. Determine if consumption code needs updates
6. Add consumption update tasks to implementation_plan.md

---

### Step 1: Identify All Downstream Consumption Locations

Use Grep to find WHERE loaded data is accessed:

```bash
# Find attribute access patterns
grep -r "player\.week_\|player\.points\|player\.score" --include="*.py"

# Find getattr/hasattr usage (dynamic attribute access)
grep -r "getattr.*player\|hasattr.*player" --include="*.py"

# Find array/list access patterns
grep -r "player\.\w+\[" --include="*.py"

# Find method calls on loaded objects
grep -r "player\.\w+(" simulation/ --include="*.py"
```

**Document findings:**
```markdown
## Downstream Consumption Locations

**Location 1:** AccuracySimulationManager.py lines 452-456
- Method: _evaluate_config_weekly()
- Access pattern: `getattr(player, f'week_{week_num}_points', None)`
- Purpose: Get actual points for accuracy calculation

**Location 2:** ParallelAccuracyRunner.py lines 180-185
- Function: worker()
- Access pattern: `player.week_17_points`
- Purpose: Get week 17 actual points for parallel MAE calculation

[Document ALL consumption locations]
```

---

### Step 2: List OLD Access Patterns (Before This Feature)

Document how data is currently accessed:

```markdown
## OLD Data Access Patterns (CSV-based)

**Pattern 1: Week-specific attributes**
- Code: `player.week_1_points`, `player.week_2_points`, ..., `player.week_17_points`
- Type: Scalar float attributes
- Access: Direct attribute access

**Pattern 2: Dynamic attribute lookup**
- Code: `getattr(player, f'week_{N}_points', None)`
- Type: Scalar float (or None if missing)
- Access: Dynamic attribute name

**Pattern 3: Projected points**
- Code: `player.projected_points`
- Type: Scalar float
- Access: Direct attribute access
```

---

### Step 3: List NEW Access Patterns (After This Feature)

Document how data will be accessed after changes:

```markdown
## NEW Data Access Patterns (JSON-based)

**Pattern 1: Array-based week data**
- Code: `player.actual_points[week_num - 1]`
- Type: Array element (float)
- Access: Array indexing (0-based, so week 1 = index 0)

**Pattern 2: Projected points array**
- Code: `player.projected_points[week_num - 1]`
- Type: Array element (float)
- Access: Array indexing

**Pattern 3: Array bounds checking**
- Code: `if len(player.actual_points) > week_num - 1: actual = player.actual_points[week_num - 1]`
- Type: Safe array access
- Access: Bounds check before indexing
```

---

### Step 4: Compare OLD vs NEW - Identify Breaking Changes

**Critical Analysis:**

```markdown
## API Breaking Changes Analysis

### Change 1: week_N_points attributes → actual_points[] array

**OLD API:**
- `player.week_1_points` (attribute)
- `player.week_2_points` (attribute)
- ...
- `player.week_17_points` (attribute)

**NEW API:**
- `player.actual_points[0]` (array element for week 1)
- `player.actual_points[1]` (array element for week 2)
- ...
- `player.actual_points[16]` (array element for week 17)

**Breaking Change?** ✅ YES - Attributes no longer exist
**Impact:** Code using `getattr(player, 'week_17_points')` will return None (attribute missing)
**Consequence:** Calculation skips ALL players → MAE = NaN/empty

---

### Change 2: projected_points scalar → projected_points[] array

**OLD API:**
- `player.projected_points` (single float value)

**NEW API:**
- `player.projected_points[week_num - 1]` (array of 17 floats)

**Breaking Change?** ✅ YES - Type changed from scalar to array
**Impact:** Code expecting float will get array
**Consequence:** Type error or incorrect calculation

---

### Change 3: Index offset (1-based weeks → 0-based arrays)

**OLD API:**
- Week 1 = `player.week_1_points`
- Week 17 = `player.week_17_points`

**NEW API:**
- Week 1 = `player.actual_points[0]`
- Week 17 = `player.actual_points[16]`

**Breaking Change?** ⚠️ LOGIC CHANGE - Off-by-one errors possible
**Impact:** Using `actual_points[week_num]` instead of `actual_points[week_num - 1]`
**Consequence:** Wrong week data, array index out of bounds
```

---

### Step 5: Determine If Consumption Code Needs Updates

**Decision criteria:**

- [ ] Are there API breaking changes? (YES from Step 4)
- [ ] Are there downstream consumption locations? (YES from Step 1)
- [ ] Does spec.md include consumption updates? (Check spec)

**If ALL YES:**
- ✅ Consumption code updates ARE REQUIRED
- Add tasks to implementation_plan.md

**If ANY NO:**
- ❌ Missing scope - STOP and report to user
- Epic may need scope clarification

---

### Step 6: Add Consumption Update Tasks to implementation_plan.md

**If consumption changes needed, add tasks:**

```markdown
## Task X: Update Consumption Code - AccuracySimulationManager

**Requirement:** Update _evaluate_config_weekly() to use array-based access

**Current Code (OLD):**
```python
actual = getattr(player, f'week_{week_num}_points', None)
```

**Updated Code (NEW):**
```python
if len(player.actual_points) > week_num - 1:
    actual = player.actual_points[week_num - 1]
else:
    actual = None
```

**Changes:**
- Replace getattr() with array indexing
- Add bounds checking (array might have <17 elements)
- Use week_num - 1 (0-based indexing)

**Files Modified:**
- simulation/accuracy/AccuracySimulationManager.py lines 452-456

**Tests Required:**
- Unit test: Test array access with various week numbers
- Edge case test: Test with short arrays (< 17 elements)
- Integration test: Verify MAE calculation uses correct week data

**Acceptance Criteria:**
- [ ] Code updated to use array indexing
- [ ] Bounds checking added
- [ ] All tests pass
- [ ] MAE calculation produces non-zero results (not all None)
```

---

### Critical Questions Checklist

Before marking Iteration 5a complete, answer these questions:

**Consumption Location Discovery:**
- [ ] Did I grep for ALL attribute access patterns (not just one)?
- [ ] Did I search for getattr/hasattr (dynamic attribute access)?
- [ ] Did I search for array/list indexing patterns?
- [ ] Did I search for method calls on loaded objects?
- [ ] Did I document EVERY consumption location found?

**API Change Analysis:**
- [ ] Did I list OLD access patterns (before this feature)?
- [ ] Did I list NEW access patterns (after this feature)?
- [ ] Did I compare OLD vs NEW for EVERY data field?
- [ ] Did I identify ALL breaking changes (not just some)?
- [ ] Did I assess impact of EACH breaking change?

**Breaking Change Detection:**
- [ ] Attribute removal (OLD has attributes, NEW uses arrays)?
- [ ] Type change (OLD scalar, NEW array)?
- [ ] Index offset change (1-based weeks → 0-based arrays)?
- [ ] Bounds checking needed (arrays may have variable length)?
- [ ] Method signature changes (parameters or return types)?

**Feature 02 Prevention:**
- [ ] If loading changes from CSV → JSON, did I check consumption code?
- [ ] If OLD uses `week_N_points` attributes, does NEW break this?
- [ ] If NEW uses arrays, does consumption code still use getattr()?
- [ ] Would consumption code get None when accessing new API?
- [ ] Would calculation fail silently (skip all players)?

**Spec Scope Verification:**
- [ ] Does spec.md mention consumption code updates?
- [ ] If API breaks, does spec include consumption tasks?
- [ ] If spec says "no consumption changes", did I verify with grep?
- [ ] If consumption changes needed but not in spec → STOP and report to user?

**Implementation Task Creation:**
- [ ] Did I add tasks for EVERY consumption location that needs updates?
- [ ] Does each task specify OLD code vs NEW code?
- [ ] Does each task include bounds checking (if arrays)?
- [ ] Does each task include tests for consumption code?
- [ ] Did I add integration tests (not just unit tests)?

**Decision Confidence:**
- [ ] Can I confidently say ALL consumption locations are identified?
- [ ] Can I confidently say ALL breaking changes are documented?
- [ ] If I skip consumption updates, would feature be non-functional?
- [ ] Would I bet feature success on this consumption analysis?

---

### Automatic Stop Conditions

If you encounter ANY of these, IMMEDIATELY stop and report to user:

❌ **API has breaking changes BUT spec doesn't mention consumption updates** - Spec scope incomplete
❌ **Found consumption locations using OLD API BUT no tasks in implementation_plan.md** - Missing implementation tasks
❌ **Feature changes data structure BUT spec says "no consumption changes"** - Spec likely wrong
❌ **Cannot confidently answer "All consumption locations identified?"** - Need more grepping
❌ **Consumption code uses getattr() for attributes that will be removed** - Breaking change

---

### Decision Framework

```
Are there API breaking changes? (from Step 4)
└─ YES → Are there downstream consumption locations? (from Step 1)
    └─ YES → Does spec.md include consumption updates?
        ├─ YES → ✅ Add consumption tasks to implementation_plan.md, proceed to Iteration 6
        └─ NO → ❌ STOP - Report to user (scope clarification needed)
    └─ NO → ✅ No consumption code to update, proceed to Iteration 6
└─ NO → ✅ No breaking changes, proceed to Iteration 6
```

---

**Output:**
- List of consumption locations
- OLD vs NEW API comparison table
- Breaking changes analysis
- NEW implementation tasks for consumption updates (if needed)

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
Progress: Iteration 5a/9 (Round 1) complete - Downstream consumption traced
Next Action: Iteration 6 - Error Handling Scenarios
Critical Finding: [X consumption locations found, Y breaking changes, Z tasks added]
```

---

### Why This Iteration Matters

**Feature 02 Example:**
- Iteration 5 verified data flow (loading works) ✅
- **Iteration 5a WOULD HAVE caught:** Consumption code still uses OLD API ❌
- Without 5a: Bug survived to user final review
- With 5a: Bug caught during TODO creation (before implementation)

**30 seconds of grepping saves days of debugging wrong implementation.**

---

## Iteration 6: Error Handling Scenarios

**Purpose:** Enumerate all error scenarios and ensure they're handled

**Process:**

### Step 1: List All Error Scenarios from spec.md Edge Cases

Common error scenarios:
- File not found
- Invalid data format
- Missing data
- Null/None values
- **Data format differences** (e.g., name formats between sources)

### Step 2: Verify Name Formats Between Data Sources

If matching data from multiple sources (CSV vs JSON, API vs file, etc.):
- Document any format differences in spec.md
- Ensure matching logic handles format variations
- Example: CSV "Baltimore Ravens" vs JSON "Ravens D/ST"

### Step 3: For EACH Error Scenario, Define Handling

**Example error scenarios:**

```markdown
## Error Scenario 1: ADP File Not Found

**Condition:** data/rankings/adp.csv does not exist

**Handling:**
- Task 1: load_adp_data() should:
  - Log error: "ADP file not found: {path}"
  - Return empty list (not crash)
  - Continue execution (graceful degradation)

**Result:** All players get adp_multiplier = 1.0 (neutral)

**Test:** test_load_adp_data_file_not_found()

---

## Error Scenario 2: Player Not in ADP Data

**Condition:** Player exists in system but not in ADP CSV

**Handling:**
- Task 2: _match_player_to_adp() should:
  - Set player.adp_value = None
  - Log info: "Player not in ADP data: {name}"
  - Continue (not an error)

**Result:** Player gets adp_multiplier = 1.0 (neutral, no penalty)

**Test:** test_match_player_not_in_adp()

---

## Error Scenario 3: Invalid ADP Value

**Condition:** ADP value < 1 or > 500

**Handling:**
- Task 3: _calculate_adp_multiplier() should:
  - Log warning: "Invalid ADP value: {value} for {name}"
  - Return 1.0 (neutral)
  - Continue (not crash)

**Result:** Player not penalized for bad data

**Test:** test_calculate_adp_multiplier_invalid_value()
```

### Step 4: Verify Every Error Scenario Has

Required elements:
- ✅ Detection logic (how we know error occurred)
- ✅ Handling logic (what we do about it)
- ✅ Recovery strategy (graceful degradation or crash?)
- ✅ Logging (what message to log)
- ✅ Test coverage (test name)

### Step 5: Add Error Handling Tasks to implementation_plan.md

```markdown
## Task 11: Error Handling - File Not Found

**Requirement:** Gracefully handle missing ADP file (spec.md Edge Cases, case 3)

**Implementation:**
- Modify: PlayerManager.load_adp_data()
- Add: try/except FileNotFoundError
- Log: "ADP file not found: {path}"
- Return: empty list []

**Acceptance Criteria:**
- [ ] FileNotFoundError caught
- [ ] Error logged (not printed)
- [ ] Function returns empty list (not None, not crash)
- [ ] Downstream code handles empty list correctly

**Test:** test_load_adp_data_file_not_found()
```

**Output:** Error handling catalog, error handling tasks added to implementation_plan.md

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
Progress: Iteration 6/9 (Round 1) complete
Next Action: Read stages/stage_5/round1/iteration_7_integration.md
```

---

## Checkpoint: After Iterations 5-6

**Before proceeding to Iteration 7:**

**Verify:**
- [ ] End-to-end data flow documented
- [ ] Data flow tests added to implementation_plan.md
- [ ] ALL downstream consumption locations identified (grepped comprehensively)
- [ ] OLD vs NEW API comparison completed
- [ ] ALL breaking changes documented
- [ ] Consumption update tasks added (if needed)
- [ ] ALL error scenarios from spec.md documented
- [ ] Error handling logic defined for each scenario
- [ ] Error handling tasks added to implementation_plan.md

**Files Updated:**
- ✅ implementation_plan.md - Data flow diagram added
- ✅ implementation_plan.md - E2E test task added
- ✅ implementation_plan.md - Consumption update tasks added (if breaking changes)
- ✅ implementation_plan.md - Error handling tasks added
- ✅ questions.md - Updated with new questions/answers (if any)
- ✅ feature README.md Agent Status - Progress: Iteration 6/9 complete

**Critical Verification:**
- ✅ **Iteration 5a prevents catastrophic bugs** - Consumption code verified

**Next:** Read `stages/stage_5/round1/iteration_7_integration.md` for Integration Gap Check

---

**END OF ITERATIONS 5-6**
