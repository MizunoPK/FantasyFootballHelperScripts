# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I1: Requirements (Iterations 1-3)

**Purpose:** Break down spec.md requirements into implementation tasks
**Prerequisites:** Planning Round 1 overview read from round1_todo_creation.md
**Next:** iteration_4_algorithms.md (Algorithm Traceability Matrix)
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`

---

## Prerequisites

**Before starting Iteration 1-3:**

- [ ] Previous iterations complete
- [ ] implementation_plan.md exists
- [ ] Working directory: Feature folder

**If any prerequisite fails:** Complete missing iterations first

---

## Overview

**What is this iteration?**
Iteration 1-3: Requirements Validation

---

## Overview

Iterations 1-3 focus on translating spec.md into concrete implementation tasks, verifying component dependencies, and validating data structures.

**Key Activities:**
- **Iteration 1:** Requirements coverage check - create implementation_plan.md with tasks
- **Iteration 2:** Component dependency mapping - verify interfaces exist
- **Iteration 3:** Data structure verification - ensure modifications are feasible

**Output:** implementation_plan.md v1.0 with verified requirements and dependencies

---

## Iteration 1: Requirements Coverage Check

**Purpose:** Verify every requirement in spec.md has corresponding implementation task(s) and create implementation_plan.md

**🚨 CRITICAL: IMPLEMENTATION TASKS MUST TRACE TO SPEC REQUIREMENTS**

**DO NOT:**
- ❌ Add tasks based on "what makes sense"
- ❌ Add tasks based on "best practices"
- ❌ Add tasks the user didn't ask for
- ❌ Add "improvements" or "nice to haves"
- ❌ Assume anything beyond what's in spec.md

**DO:**
- ✅ Create tasks ONLY for requirements explicitly in spec.md
- ✅ If uncertain about a task → create question in questions.md
- ✅ Every task must cite which spec section it implements

**Process:**

1. **Create implementation_plan.md** using template from `templates/implementation_plan_template.md`
2. **Read spec.md completely**
3. **Extract all requirements:**
   - From "Objective" section
   - From "Scope" section
   - From "Components Affected" section
   - From "Algorithms" section
   - From "Edge Cases" section

4. **Add "Implementation Tasks" section to implementation_plan.md:**

For EACH requirement, create implementation task - and ONLY for confirmed requirements.

**Example:**

**Requirement from spec:** "Load ADP data from data/rankings/adp.csv"

**implementation tasks:**
```markdown
## Task 1: Implement ADP Data Loading

**Requirement:** Load ADP data from CSV file (spec.md Objective section)

**Acceptance Criteria:**
- [ ] Function `load_adp_data()` created in PlayerManager
- [ ] Reads file from path: data/rankings/adp.csv
- [ ] Returns List[Tuple[str, str, int]] (Name, Position, ADP)
- [ ] Handles FileNotFoundError gracefully (logs error, returns empty list)
- [ ] Validates CSV has required columns: Name, Position, ADP
- [ ] Logs number of rows loaded: "Loaded {N} ADP rankings"

**Implementation Location:**
- File: league_helper/util/PlayerManager.py
- Method: load_adp_data() (NEW method)
- Line: ~450 (after existing load methods)

**Dependencies:**
- Requires: csv_utils.read_csv_with_validation()
- Called by: _calculate_adp_multiplier() (Task 3)

**Tests:**
- Unit test: test_load_adp_data_success()
- Unit test: test_load_adp_data_file_not_found()
- Unit test: test_load_adp_data_invalid_columns()
```

4. **Continue for ALL requirements**

5. **Verify coverage:**
   - Check: Every requirement has at least one implementation task
   - Check: No orphan implementation tasks (not tied to requirement)

**Output:** Initial implementation_plan.md with tasks for all requirements

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
Progress: Iteration 1/9 (Planning Round 1) complete
Next Action: Iteration 2 - Component Dependency Mapping
```

---

## Iteration 2: Component Dependency Mapping

**Purpose:** Map all components this feature depends on, verify interfaces, and add "Component Dependencies" section to implementation_plan.md

**Process:**

1. **List all external components this feature will call:**
   - From spec.md "Dependencies" section
   - From spec.md "Components Affected" section

**Example:**
```
External Dependencies:
- ConfigManager.get_adp_multiplier(adp: int)
- csv_utils.read_csv_with_validation(filepath, required_columns)
- FantasyPlayer class (will add fields)
```

2. **For EACH dependency, verify it exists:**

**DO NOT ASSUME - VERIFY BY READING SOURCE CODE**

```bash
# Find ConfigManager.get_adp_multiplier
grep -n "def get_adp_multiplier" league_helper/util/ConfigManager.py
```

**Read the actual method:**
```python
# league_helper/util/ConfigManager.py:234
def get_adp_multiplier(self, adp: int) -> Tuple[float, int]:
    """Calculate ADP multiplier based on ADP ranking."""
    # ... implementation
    return (multiplier, rating)
```

3. **Document verified interface:**

```markdown
## Dependency 1: ConfigManager.get_adp_multiplier

**Interface Verified:**
- Source: league_helper/util/ConfigManager.py:234
- Signature: `def get_adp_multiplier(self, adp: int) -> Tuple[float, int]`
- Parameters:
  - adp (int): ADP ranking (1-500)
- Returns:
  - Tuple[float, int]: (multiplier, rating)
    - multiplier: Score adjustment (0.8-1.2)
    - rating: Confidence rating (0-100)
- Exceptions: None documented
- Example usage found in: PlayerManager.calculate_injury_penalty (line 456)

**implementation tasks using this:**
- Task 3: Calculate ADP multiplier (calls this method)
```

4. **Repeat for ALL dependencies**

5. **Update implementation tasks with verified interfaces**

**Output:** Dependency map with verified interfaces, implementation tasks updated

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
Progress: Iteration 2/9 (Planning Round 1) complete
Next Action: Iteration 3 - Data Structure Verification
```

---

## Iteration 3: Data Structure Verification

**Purpose:** Verify all data structures can be created/modified as planned

**Process:**

1. **List all data structures from spec.md:**
   - Classes to modify (e.g., FantasyPlayer)
   - New classes to create
   - Data file formats

2. **For EACH data structure, verify feasibility:**

**Example: FantasyPlayer modifications**

**Read current FantasyPlayer class:**
```bash
# Find FantasyPlayer class definition
grep -n "class FantasyPlayer" league_helper/util/FantasyPlayer.py
```

**Verify we can add fields:**
```python
# league_helper/util/FantasyPlayer.py:15
class FantasyPlayer:
    def __init__(self, ...):
        self.name = name
        self.position = position
        # ... existing fields
        # ✅ CAN ADD: self.adp_value = None
        # ✅ CAN ADD: self.adp_multiplier = 1.0
```

3. **Check for conflicts:**
   - Field name already used?
   - Type conflicts with existing patterns?

4. **Document verification:**

```markdown
## Data Structure 1: FantasyPlayer modifications

**Verified Feasible:**
- Source: league_helper/util/FantasyPlayer.py:15
- Current fields: name, position, team, projected_points, ...
- ✅ Can add: adp_value (Optional[int])
- ✅ Can add: adp_multiplier (float)
- ✅ No naming conflicts found
- ✅ Types consistent with existing patterns

**implementation tasks affected:**
- Task 2: Add ADP fields to FantasyPlayer __init__
```

5. **Repeat for all data structures**

**Output:** Data structure verification report, confidence in design

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
Progress: Iteration 3/9 (Planning Round 1) complete
Next Action: Read stages/s5/s5_p1_i2_algorithms.md
```

---

## Checkpoint: After Iterations 1-3

**Before proceeding to Iteration 4:**

**Verify:**
- [ ] implementation_plan.md created using template
- [ ] ALL requirements from spec.md have implementation tasks
- [ ] NO orphan tasks (all tasks trace to requirements)
- [ ] ALL component dependencies verified with source code
- [ ] NO assumed interfaces (all interfaces copy-pasted from actual code)
- [ ] ALL data structure modifications verified as feasible
- [ ] NO naming conflicts found

**Files Updated:**
- ✅ implementation_plan.md - v1.0 created with initial tasks
- ✅ questions.md - Updated with new questions/answers (if any)
- ✅ feature README.md Agent Status - Progress: Iteration 3/9 complete

**Next:** Read `stages/s5/s5_p1_i2_algorithms.md` for Algorithm Traceability Matrix


## Exit Criteria

**Iteration 1-3 complete when ALL of these are true:**

- [ ] All tasks in this iteration complete
- [ ] implementation_plan.md updated
- [ ] Agent Status updated
- [ ] Ready for next iteration

**If any criterion unchecked:** Complete missing items first

---
---

**END OF ITERATIONS 1-3**
