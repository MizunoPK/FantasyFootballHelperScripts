# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I3: Downstream Data Consumption Tracing

**Purpose:** Downstream Data Consumption Tracing
**Prerequisites:** Previous iterations complete
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`
**Router:** `stages/s5/s5_p1_i3_integration.md`

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

