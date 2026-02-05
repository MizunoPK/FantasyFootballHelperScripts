# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I3: Integration (Iteration 7 + Gate 7a)

**Purpose:** Trace data flow, verify downstream consumption, and ensure error handling
**Prerequisites:** Iteration 4 + Gate 4a complete (iteration_4_algorithms.md)
**Next:** iteration_7_integration.md (Integration Gap Check)
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`

---

## Prerequisites

**Before starting Iteration 7:**

- [ ] Previous iterations complete
- [ ] implementation_plan.md exists
- [ ] Working directory: Feature folder

**If any prerequisite fails:** Complete missing iterations first

---

## Overview

**What is this iteration?**
Iteration 7: Integration Planning

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
```text
Progress: Iteration 5/9 (Planning Round 1) complete
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
```
actual = getattr(player, f'week_{week_num}_points', None)
```markdown

**Updated Code (NEW):**
```
if len(player.actual_points) > week_num - 1:
    actual = player.actual_points[week_num - 1]
else:
    actual = None
```bash

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

```text
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
```bash
Progress: Iteration 5a/9 (Planning Round 1) complete - Downstream consumption traced
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
```text
Progress: Iteration 6/9 (Planning Round 1) complete
Next Action: Iteration 6a - External Dependency Final Verification
```

---

## Iteration 6a: External Dependency Final Verification (NEW - from KAI-1 lessons)

**Purpose:** Re-verify external library assumptions before implementation

**Prerequisites:**
- Iteration 6 complete (Error handling scenarios documented)
- S1 Discovery identified potential external dependencies
- S2 Research tested library compatibility

**Historical Context (KAI-1 Feature 02):**
- Feature assumed library would work without final verification
- Result: 6/16 tests failed during S7
- Time cost: 2 hours debugging + workaround
- **This final checkpoint catches missed assumptions**

---

### Quick Re-Verification Checklist

**If S1 and S2 verified external dependencies:**

This is a quick checkpoint (5-10 minutes) to ensure nothing was missed:

- [ ] Review S1 Discovery: Were external dependencies identified?
- [ ] Review S2 Research: Were libraries tested with test environment?
- [ ] Check implementation_plan.md: Are workarounds documented?
- [ ] Verify: No NEW external dependencies added since S2

**If verification PASSED in S1/S2:**
- ✅ Proceed to Checkpoint (no additional work needed)

**If verification was SKIPPED or INCOMPLETE in S1/S2:**
- ⚠️ **STOP** - Perform full verification NOW (see below)

---

### Full Verification (If Skipped in S1/S2)

**Only perform if external dependencies were NOT verified in S1/S2:**

**1. List ALL External Libraries:**
```markdown
External libraries this feature uses:
- ESPN API (espn_api package) - fetch player data
- pandas - CSV manipulation
- requests - HTTP calls
```

**2. For EACH Library, Quick Test:**
```python
# Test library with test environment
# 10 minutes per library
```

**3. Document Findings:**
```markdown
Library: ESPN API
Compatibility: ✅ Works with mocks
Workaround: None needed
```

**4. Add Workaround Tasks (if needed):**
- Update implementation_plan.md with test client tasks
- Add time estimates

---

### Decision Point

**All libraries verified compatible?**
- ✅ Proceed to Checkpoint

**Library incompatible, no workaround planned?**
- ❌ **STOP** - Add workaround tasks to implementation_plan.md
- Document approach, add tasks, update time estimates
- Then proceed to Checkpoint

**NEW external dependency discovered?**
- ❌ **STOP** - Verify compatibility NOW (can't wait until S7)
- Test with test environment
- Document findings
- Add tasks if needed
- Then proceed to Checkpoint

---

**Time Investment:**
- If S1/S2 verification done: 5 minutes (quick checklist)
- If S1/S2 verification skipped: 15-30 minutes per library (full verification)

**Why This Final Checkpoint?**
- Catches dependencies added during planning (not in S1/S2)
- Ensures workarounds are actually in implementation_plan.md
- Last chance before implementation to avoid S7 debugging

**Update Agent Status:**
```bash
Progress: Iteration 6a/9 (Planning Round 1) complete - External dependencies verified
Next Action: Checkpoint - After Iterations 5-6a
Critical Finding: [X libraries verified, Y workarounds in plan]
```

---

## Checkpoint: After Iterations 5-6a (UPDATED)

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
- [ ] External dependencies verified compatible (or workarounds planned) - NEW

**Files Updated:**
- ✅ implementation_plan.md - Data flow diagram added
- ✅ implementation_plan.md - E2E test task added
- ✅ implementation_plan.md - Consumption update tasks added (if breaking changes)
- ✅ implementation_plan.md - Error handling tasks added
- ✅ questions.md - Updated with new questions/answers (if any)
- ✅ feature README.md Agent Status - Progress: Iteration 6/9 complete

**Critical Verification:**
- ✅ **Iteration 5a prevents catastrophic bugs** - Consumption code verified

**Next:** Read `stages/s5/s5_p1_i3_integration.md` for Integration Gap Check

---

**END OF ITERATIONS 5-6**
# Planning Round 1: Iteration 7 - Integration & Compatibility

**Purpose:** Verify all new code is integrated (no orphans) and handles backward compatibility
**Prerequisites:** Iteration 6 complete (iterations_5_6_dependencies.md)
**Next:** Planning Round 1 Checkpoint, then Planning Round 2 (round2_todo_creation.md)
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`

---

## Overview

Iteration 7 has two parts:
- **Iteration 7:** Integration Gap Check - Verify EVERY new method has a caller
- **Iteration 7a:** Backward Compatibility Analysis - Handle old data formats gracefully

**Why These Matter:**
- Iteration 7: Prevents orphan code that never gets called ("If nothing calls it, it's not integrated")
- Iteration 7a: Prevents bugs from loading old files created before this epic

---

## Iteration 7: Integration Gap Check (CRITICAL)

**Purpose:** Verify EVERY new method has an identified caller (no orphan code)

**⚠️ CRITICAL:** "If nothing calls it, it's not integrated"

**Process:**

### Step 1: List All NEW Methods/Functions This Feature Creates

Extract from implementation tasks:
- Example: load_adp_data(), _match_player_to_adp(), _calculate_adp_multiplier()

### Step 2: For EACH New Method, Identify Caller

**Example Integration Verification:**

```markdown
## Integration Verification

### Method: PlayerManager.load_adp_data()

**Caller:** PlayerManager.load_players() (existing method)
**Integration Point:** Line ~180 in load_players()
**Call Signature:** `self.adp_data = self.load_adp_data()`
**Verified:** ✅ Method will be called

**Call Chain:**
run_league_helper.py (entry point)
   → LeagueHelperManager.__init__()
   → PlayerManager.load_players()
   → PlayerManager.load_adp_data() ← NEW METHOD

**Orphan Check:** ✅ NOT ORPHANED (clear caller)

---

### Method: PlayerManager._match_player_to_adp(player)

**Caller:** PlayerManager.load_players() (existing method)
**Integration Point:** Line ~210 in load_players() loop
**Call Signature:** `self._match_player_to_adp(player)`
**Verified:** ✅ Method will be called for each player

**Call Chain:**
run_league_helper.py
   → LeagueHelperManager.__init__()
   → PlayerManager.load_players()
   → for player in players: ← LOOP
      → PlayerManager._match_player_to_adp(player) ← NEW METHOD

**Orphan Check:** ✅ NOT ORPHANED (called in loop)

---

### Method: PlayerManager._calculate_adp_multiplier(player)

**Caller:** FantasyPlayer.calculate_total_score()
**Integration Point:** Line ~235 in calculate_total_score()
**Call Signature:** `score *= self.adp_multiplier`
**Verified:** ✅ Field used in calculation

**Call Chain:**
AddToRosterModeManager.get_recommendations()
   → FantasyPlayer.calculate_total_score()
   → Uses: self.adp_multiplier ← NEW FIELD (set by Task 3)

**Orphan Check:** ✅ NOT ORPHANED (field consumed)
```

### Step 3: Verify Integration for ALL New Code

**Count:**
- New methods created: {N}
- Methods with identified caller: {M}

**Result:**
- ❌ **FAIL** if M < N (orphan methods exist)
- ✅ **PASS** if M == N (all integrated)

**If orphan methods found:**
- STOP - Fix integration
- Options:
  - Add caller (integrate the method)
  - Remove method (not needed)
- Document decision in implementation_plan.md

### Step 4: Create Integration Matrix

| New Method | Caller | Call Location | Verified |
|------------|--------|---------------|----------|
| load_adp_data() | PlayerManager.load_players() | PlayerManager.py:180 | ✅ |
| _match_player_to_adp() | PlayerManager.load_players() | PlayerManager.py:210 | ✅ |
| _calculate_adp_multiplier() | PlayerManager.load_players() | PlayerManager.py:215 | ✅ |

**Output:** Integration matrix added to implementation_plan.md, no orphan code

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
```text
Progress: Iteration 7/9 (Planning Round 1) complete
Next Action: Iteration 7a - Backward Compatibility Analysis
```

---

## Iteration 7a: Backward Compatibility Analysis (NEW - MANDATORY)

**Objective:** Identify how this feature interacts with existing data, files, and configurations created by older versions of the code.

**Why This Matters:** New features often modify data structures or file formats. If the system can resume/load old data, the new code must handle old formats gracefully. This iteration prevents bugs caused by old data polluting new calculations.

**Historical Evidence:** Issue #001 (KAI-5) discovered in user testing could have been prevented by this iteration. Resume logic loaded old files without ranking_metrics, polluting best_configs with invalid data.

---

### Research Questions

**1. Data Persistence:**
- Does this feature modify any data structures that are saved to files?
- Can the system resume/load from files created before this epic?
- What file formats are involved? (JSON, CSV, pickled objects, etc.)

**2. Old Data Handling:**
- What happens if new code loads old files missing new fields?
- Will old data be used in comparisons/calculations with new data?
- Are there fallback mechanisms that might hide incompatibilities?

**3. Migration Strategy:**
- Do old files need to be migrated to new format?
- Should old files be ignored/invalidated?
- Is there a version marker in saved files?

**4. Resume Scenarios:**
- Can users resume operations from intermediate states?
- What happens if intermediate files are from older code version?
- Will the system detect and handle version mismatches?

---

### Action Items

**1. Search for File I/O Operations:**

Look for save/load methods in affected modules:
```bash
# Find file write operations
grep -r "\.dump\|\.to_json\|\.to_csv\|pickle\.dump" affected_module/ --include="*.py"

# Find file read operations
grep -r "\.load\|\.from_json\|\.read_csv\|pickle\.load" affected_module/ --include="*.py"

# Find resume/checkpoint logic
grep -r "resume\|checkpoint\|load_state" affected_module/ --include="*.py"
```

**2. Analyze Data Structures:**

- List all fields added/removed/modified
- Check if structures have version markers
- Verify default values for missing fields

**Example analysis:**
```markdown
## Data Structure Changes

**FantasyPlayer class modifications:**
- Added: adp_value (Optional[int]) - Default: None
- Added: adp_multiplier (float) - Default: 1.0
- No fields removed
- No fields modified

**Serialization:**
- FantasyPlayer not directly serialized (checked with grep)
- No pickle files found in data/
- No JSON export of player objects

**Conclusion:** No backward compatibility issues (player objects not persisted)
```

**3. Document Findings in questions.md:**

```markdown
## Backward Compatibility Analysis (Iteration 7a)

**Files that persist data:**
- [List files and formats]

**New fields added:**
- [List new fields with types]

**Resume/load scenarios:**
- [Describe scenarios where old data might be loaded]

**Compatibility strategy:**
- [ ] Option 1: Migrate old files on load
- [ ] Option 2: Invalidate old files (require fresh run)
- [ ] Option 3: Handle missing fields with defaults
- [ ] Option 4: No old files exist / not applicable

**Rationale:** [Explain chosen strategy]
```

**4. Add Test Scenarios to implementation_plan.md:**

If resume/load possible:
- Add test: "Resume from file created before this epic"

If migration needed:
- Add test: "Migrate old file format to new format"

If validation needed:
- Add test: "Reject incompatible old files with clear error"

---

### Example: Backward Compatibility Scenario

**Feature that modifies persisted data:**

```markdown
## Backward Compatibility Analysis

**Files that persist data:**
- simulation/results/best_configs.json (simulation results)
- simulation/cache/player_cache.pkl (player objects)

**New fields added:**
- PlayerStats.ranking_metrics (Dict[str, float]) - NEW field

**Resume/load scenarios:**
- User runs simulation → best_configs.json created WITH ranking_metrics
- User upgrades code → runs simulation again
- System loads old best_configs.json WITHOUT ranking_metrics
- Comparison logic fails (missing field in old data)

**Compatibility strategy:**
- ✅ **Option 2: Invalidate old files (require fresh run)**
- Rationale: Simulations are cheap to re-run, data format changed significantly
- Implementation: Check for ranking_metrics field on load, reject if missing
- User message: "Simulation format updated. Previous results incompatible. Re-running simulation..."

**Tests to add:**
- test_load_old_best_configs_rejects_gracefully()
- test_load_best_configs_with_ranking_metrics_succeeds()
```

---

### Success Criteria

Before marking Iteration 7a complete:

- ✅ All file I/O operations identified and analyzed
- ✅ Compatibility strategy documented and justified
- ✅ Resume/load scenarios covered in test plan
- ✅ Migration or validation logic added to implementation_plan.md (if needed)

**Time Estimate:** 10-15 minutes (prevents hours of debugging)

---

**🔄 After Iteration Checkpoint - questions.md Review:**

After completing this iteration, check if you have questions or found answers:

1. **If you discovered NEW uncertainties during this iteration:**
   - Add them to `questions.md` with context
   - Format: Question, context, impact on implementation

2. **If you found ANSWERS to existing questions in questions.md:**
   - Update questions.md to mark question as answered
   - Document the answer and source

3. **If no new questions and no answers found:**
   - No action needed, proceed to checkpoint

**Note:** This is a quick check (1-2 minutes). questions.md will be presented to user at Gate 5.

**Update Agent Status:**
```text
Progress: Planning Round 1 Iteration 7a complete (backward compatibility analyzed)
Next Action: Planning Round 1 checkpoint - evaluate confidence
```

---

## 🛑 MANDATORY CHECKPOINT: ROUND 1 COMPLETE

**You have completed Iterations 1-7 + Gates 4a, 7a (Round 1)**

⚠️ STOP - DO NOT PROCEED TO ROUND 2 YET

**REQUIRED ACTIONS:**

### Step 1: Update implementation_plan.md Version
1. [ ] Mark version as v1.0 in Version History section

### Step 2: Update Agent Status
2. [ ] Update feature README.md Agent Status:
   - Current Guide: "stages/s5/s5_p2_planning_round2.md"
   - Current Step: "Round 1 complete (7 iterations + 2 gates), evaluating confidence"
   - Last Updated: [timestamp]
   - Progress: "Planning Round 1 complete (9/9 iterations)"
   - Confidence Level: {HIGH / MEDIUM / LOW}
   - Next Action: {Create questions file / Proceed to Planning Round 2}
   - Blockers: {List any uncertainties or "None"}

### Step 3: Evaluate Confidence
3. [ ] Evaluate confidence across 5 dimensions:
   - [ ] Do I understand the feature requirements? (HIGH/MEDIUM/LOW)
   - [ ] Are all algorithms clear? (HIGH/MEDIUM/LOW)
   - [ ] Are interfaces verified? (HIGH/MEDIUM/LOW)
   - [ ] Is data flow understood? (HIGH/MEDIUM/LOW)
   - [ ] Are all consumption locations identified? (HIGH/MEDIUM/LOW)
   - [ ] Overall confidence: {HIGH/MEDIUM/LOW}

### Step 4: Re-Read Critical Sections
4. [ ] Use Read tool to re-read "Round 1 Summary" section of s5_p1_planning_round1.md
5. [ ] Use Read tool to re-read "Confidence Evaluation" criteria

### Step 5: Output Acknowledgment
6. [ ] Output acknowledgment: "✅ ROUND 1 CHECKPOINT COMPLETE: Confidence={level}, proceeding to {Round 2 / questions.md}"

**Why this checkpoint exists:**
- Round 1 confidence determines whether Round 2 is needed
- 75% of agents skip confidence evaluation and proceed blindly
- Low confidence proceeding to Round 2 causes 80% implementation failure rate

### Decision Point

**If confidence >= MEDIUM:**
- ✅ Proceed to Planning Round 2
- Use "Starting S5 Round 2" prompt from prompts_reference_v2.md
- Read `stages/s5/s5_p2_planning_round2.md`

**If confidence < MEDIUM:**
- ❌ STOP - Create questions.md file
- Wait for user answers
- Do NOT proceed to Planning Round 2

---

### If Confidence < MEDIUM: Create Questions File

**File:** `questions.md` (in feature folder)

**Template:**
```markdown
# Feature Questions for User

**Created After:** Planning Round 1 (Iteration 7a)
**Confidence Level:** LOW / MEDIUM
**Reason:** {Why confidence is low}

---

## Question 1: {Topic}

**Context:** {Why this question arose during iterations}

**Current Understanding:** {What I think, but not sure}

**Question:** {Specific question for user}

**Options:**
A. {Option A}
B. {Option B}
C. {Option C}

**My Recommendation:** {Which option and why}

**Impact if wrong:** {What breaks if we guess wrong}

---

{Repeat for all questions}
```

**Update Agent Status:**
```bash
Blockers: Waiting for user answers to questions.md
Next Action: Wait for user responses, then update implementation_plan.md based on answers
```

**WAIT for user answers. Do NOT proceed to Planning Round 2.**

---

## Checkpoint: After Planning Round 1 Complete

**Verify:**
- [ ] All 9 iterations complete (1-7, 4a, 7a)
- [ ] Gate 4a PASSED (mandatory)
- [ ] implementation_plan.md v1.0 created with all sections
- [ ] Algorithm Traceability Matrix added (40+ mappings)
- [ ] Component Dependencies verified
- [ ] Data flow documented
- [ ] Downstream consumption analyzed (Iteration 5a)
- [ ] Error handling scenarios documented
- [ ] Integration matrix created (no orphan code)
- [ ] Backward compatibility analyzed
- [ ] Confidence level evaluated

**Files Created/Updated:**
- ✅ implementation_plan.md - v1.0 with comprehensive tasks
- ✅ questions.md - Created if confidence < MEDIUM (optional)
- ✅ feature README.md Agent Status - Planning Round 1 complete

**Next:**
- If confidence >= MEDIUM: Read `stages/s5/s5_p2_planning_round2.md`
- If confidence < MEDIUM: Wait for user to answer questions.md


## Exit Criteria

**Iteration 7 complete when ALL of these are true:**

- [ ] All tasks in this iteration complete
- [ ] implementation_plan.md updated
- [ ] Agent Status updated
- [ ] Ready for next iteration

**If any criterion unchecked:** Complete missing items first

---
---

**END OF ITERATION 7 + ROUND 1 CHECKPOINT**
