# STAGE 5aa: TODO Creation - Round 1 (Iterations 1-7 + 4a)

🚨 **MANDATORY READING PROTOCOL**

**Before starting this round:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current iteration
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**Overview:**
- **Round 1 of 3** in the 24-iteration TODO creation process
- **Iterations 1-7 + 4a** (Initial Analysis & Planning)
- **Focus:** Requirements coverage, dependency mapping, algorithm tracing

**Estimated Time:** 45-60 minutes
**Prerequisites:** Stage 4 complete, feature spec.md complete
**Outputs:** Initial TODO file with tasks, dependencies verified, algorithms traced

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 8 iterations in Round 1 are MANDATORY (no skipping)
   - Iterations 1-7 + Iteration 4a
   - Each iteration catches specific bug categories

2. ⚠️ Execute iterations IN ORDER (not parallel, not random)
   - Later iterations depend on earlier findings

3. ⚠️ Iteration 4a (TODO Specification Audit) is a MANDATORY GATE
   - CANNOT proceed to Round 2 without PASSING iteration 4a
   - Every TODO task MUST have acceptance criteria

4. ⚠️ NEVER ASSUME - TODO TASKS MUST TRACE TO SPEC REQUIREMENTS
   - Every TODO task must map to explicit spec.md requirement
   - Do NOT add tasks based on "best practices" or assumptions
   - Do NOT add tasks the user didn't ask for
   - If uncertain about a task → create question in questions.md
   - Only create TODO tasks for confirmed, documented requirements

5. ⚠️ Interface Verification Protocol: READ actual source code
   - Never assume interface - always verify (Iteration 2)
   - Copy-paste exact method signatures

6. ⚠️ Algorithm Traceability Matrix (Iteration 4)
   - Map EVERY algorithm in spec to exact code location
   - Typical matrix has 40+ mappings

7. ⚠️ Integration Gap Check (Iteration 7)
   - For EVERY new method: identify caller
   - No orphan code allowed

8. ⚠️ STOP if confidence < Medium at Round 1 checkpoint
   - Create questions file
   - Wait for user answers
   - Do NOT proceed to Round 2

9. ⚠️ Update feature README.md Agent Status after Round 1 complete
   - Document confidence level
   - Document next action
```

---

## Prerequisites Checklist

**Verify BEFORE starting Round 1:**

□ Stage 4 (Epic Testing Strategy) complete
□ This feature's spec.md is complete:
  - All sections filled (Components, Data Structures, Algorithms, Dependencies)
  - No "TBD" or placeholder content
  - All algorithms documented with pseudocode
□ This feature's checklist.md shows all items resolved
□ epic_smoke_test_plan.md updated (Stage 4 version)
□ No blockers in feature README.md Agent Status

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with Round 1
- Return to previous stage to complete prerequisites
- Document blocker in Agent Status

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│          ROUND 1: Initial Analysis & Planning                │
│                    (8 Iterations)                             │
└──────────────────────────────────────────────────────────────┘

Iteration 1: Requirements Coverage Check
   ↓
Iteration 2: Component Dependency Mapping
   ↓
Iteration 3: Data Structure Verification
   ↓
Iteration 4: Algorithm Traceability Matrix (CRITICAL)
   ↓
Iteration 4a: TODO Specification Audit (MANDATORY GATE)
   ↓
Iteration 5: End-to-End Data Flow
   ↓
Iteration 6: Error Handling Scenarios
   ↓
Iteration 7: Integration Gap Check (CRITICAL)
   ↓
ROUND 1 CHECKPOINT
   ↓
If confidence >= MEDIUM: Proceed to Round 2 (STAGE_5ab)
If confidence < MEDIUM: Create questions file, wait for user
```

---

## ROUND 1: Initial Analysis & Planning

### Iteration 1: Requirements Coverage Check

**Purpose:** Verify every requirement in spec.md has corresponding TODO task(s)

**🚨 CRITICAL: TODO TASKS MUST TRACE TO SPEC REQUIREMENTS**

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

1. **Read spec.md completely**
2. **Extract all requirements:**
   - From "Objective" section
   - From "Scope" section
   - From "Components Affected" section
   - From "Algorithms" section
   - From "Edge Cases" section

3. **Create initial TODO list:**

For EACH requirement, create TODO task(s) - and ONLY for confirmed requirements.

**Example:**

**Requirement from spec:** "Load ADP data from data/rankings/adp.csv"

**TODO tasks:**
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
   - Check: Every requirement has at least one TODO task
   - Check: No orphan TODO tasks (not tied to requirement)

**Output:** Initial TODO file with tasks for all requirements

**Update Agent Status:**
```
Progress: Iteration 1/8 (Round 1) complete
Next Action: Iteration 2 - Component Dependency Mapping
```

---

### Iteration 2: Component Dependency Mapping

**Purpose:** Map all components this feature depends on and verify interfaces

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

**TODO tasks using this:**
- Task 3: Calculate ADP multiplier (calls this method)
```

4. **Repeat for ALL dependencies**

5. **Update TODO tasks with verified interfaces**

**Output:** Dependency map with verified interfaces, TODO tasks updated

**Update Agent Status:**
```
Progress: Iteration 2/8 (Round 1) complete
Next Action: Iteration 3 - Data Structure Verification
```

---

### Iteration 3: Data Structure Verification

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

**TODO tasks affected:**
- Task 2: Add ADP fields to FantasyPlayer __init__
```

5. **Repeat for all data structures**

**Output:** Data structure verification report, confidence in design

**Update Agent Status:**
```
Progress: Iteration 3/8 (Round 1) complete
Next Action: Iteration 4 - Algorithm Traceability Matrix
```

---

### Iteration 4: Algorithm Traceability Matrix (CRITICAL)

**Purpose:** Map EVERY algorithm in spec.md to exact implementation location

**⚠️ CRITICAL:** This iteration prevents "implemented wrong algorithm" bugs

**Process:**

1. **Extract ALL algorithms from spec.md:**
   - Main algorithms
   - Helper algorithms
   - Edge case handling logic

2. **Create traceability matrix:**

| Algorithm (from spec.md) | Spec Section | Implementation Location | TODO Task | Verified |
|--------------------------|--------------|------------------------|-----------|----------|
| Load ADP data from CSV | Algorithms, step 1 | PlayerManager.load_adp_data() | Task 1 | ✅ |
| Match player to ADP ranking | Algorithms, step 2 | PlayerManager._match_player_to_adp() | Task 2 | ✅ |
| Calculate ADP multiplier | Algorithms, step 3 | PlayerManager._calculate_adp_multiplier() | Task 3 | ✅ |
| Apply multiplier to score | Algorithms, step 4 | FantasyPlayer.calculate_total_score() | Task 4 | ✅ |
| Handle player not in ADP data | Edge Cases, case 1 | PlayerManager._match_player_to_adp() | Task 2 | ✅ |
| Handle invalid ADP value | Edge Cases, case 2 | PlayerManager._calculate_adp_multiplier() | Task 3 | ✅ |
| Handle ADP file missing | Edge Cases, case 3 | PlayerManager.load_adp_data() | Task 1 | ✅ |

3. **For EACH algorithm, verify:**
   - Algorithm from spec has TODO task
   - TODO task specifies WHERE to implement
   - Implementation location is specific (file, method, approximate line)

4. **Quote exact spec text in TODO:**

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

5. **Verify matrix is complete:**
   - Count algorithms in spec: {N}
   - Count rows in matrix: {N}
   - ✅ All algorithms traced

**Output:** Algorithm Traceability Matrix (40+ mappings typical)

**Update Agent Status:**
```
Progress: Iteration 4/8 (Round 1) complete
Next Action: Iteration 4a - TODO Specification Audit (MANDATORY)
```

---

### Iteration 4a: TODO Specification Audit (MANDATORY GATE)

**Purpose:** Verify EVERY TODO task has acceptance criteria (no vague tasks)

**⚠️ MANDATORY:** Cannot proceed to Round 2 without passing this audit

**Process:**

1. **Review EVERY TODO task**

2. **For EACH task, verify it has:**

   □ **Requirement reference** (which spec section it implements)
   □ **Acceptance criteria** (checklist of what defines "done")
   □ **Implementation location** (file, method, line number)
   □ **Dependencies** (what this task needs, what depends on it)
   □ **Tests** (specific test names that verify this task)

3. **Examples:**

**❌ BAD TODO task (vague):**
```markdown
## Task 5: Implement ADP feature

Do the ADP stuff.
```

**✅ GOOD TODO task (specific):**
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

4. **Audit results:**

Count tasks:
- Total tasks: {N}
- Tasks with complete acceptance criteria: {M}
- ✅ PASS if M == N
- ❌ FAIL if M < N (fix vague tasks)

**If FAIL:**
- STOP - Do NOT proceed
- Fix vague tasks (add acceptance criteria)
- Re-run iteration 4a
- Document in Agent Status: "Iteration 4a FAILED - fixing vague tasks"

**If PASS:**
- Document in TODO file:

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

**Output:** Verified TODO file with acceptance criteria for EVERY task

**Update Agent Status:**
```
Progress: Iteration 4a PASSED (critical gate)
Next Action: Iteration 5 - End-to-End Data Flow
```

---

### Iteration 5: End-to-End Data Flow

**Purpose:** Trace data from entry point through all transformations to output

**Process:**

1. **Identify entry point:**
   - Where does data enter this feature?
   - Example: load_adp_data() reads CSV file

2. **Trace data flow step-by-step:**

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

3. **Verify no gaps:**
   - Data created in Step 1 → used in Step 2 ✅
   - Data created in Step 2 → used in Step 3 ✅
   - Data created in Step 3 → used in Step 4 ✅
   - Output from Step 4 → consumed by downstream system ✅

4. **Identify data transformations:**
   - CSV text → Python objects (Step 1)
   - Player object → ADP value lookup (Step 2)
   - ADP value → multiplier (Step 3)
   - Multiplier → final score (Step 4)

5. **Add data flow tests to TODO:**

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

**Output:** Data flow diagram, E2E test task added to TODO

**Update Agent Status:**
```
Progress: Iteration 5/8 (Round 1) complete
Next Action: Iteration 6 - Error Handling Scenarios
```

---

### Iteration 6: Error Handling Scenarios

**Purpose:** Enumerate all error scenarios and ensure they're handled

**Process:**

1. **List all error scenarios from spec.md Edge Cases:**
   - File not found
   - Invalid data format
   - Missing data
   - Null/None values
   - **Data format differences** (e.g., name formats between sources)
   - etc.

2. **Verify name formats between data sources match or have handling:**
   - If matching data from multiple sources (CSV vs JSON, API vs file, etc.)
   - Document any format differences in spec.md
   - Ensure matching logic handles format variations
   - Example: CSV "Baltimore Ravens" vs JSON "Ravens D/ST"

3. **For EACH error scenario, define handling:**

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

3. **Verify every error scenario has:**
   - Detection logic (how we know error occurred)
   - Handling logic (what we do about it)
   - Recovery strategy (graceful degradation or crash?)
   - Logging (what message to log)
   - Test coverage (test name)

4. **Add error handling tasks to TODO:**

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

**Output:** Error handling catalog, error handling tasks added to TODO

**Update Agent Status:**
```
Progress: Iteration 6/8 (Round 1) complete
Next Action: Iteration 7 - Integration Gap Check
```

---

### Iteration 7: Integration Gap Check (CRITICAL)

**Purpose:** Verify EVERY new method has an identified caller (no orphan code)

**⚠️ CRITICAL:** "If nothing calls it, it's not integrated"

**Process:**

1. **List all NEW methods/functions this feature creates:**
   - From TODO tasks
   - Example: load_adp_data(), _match_player_to_adp(), _calculate_adp_multiplier()

2. **For EACH new method, identify caller:**

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

3. **Verify integration for ALL new code:**

Count:
- New methods created: {N}
- Methods with identified caller: {M}
- ❌ FAIL if M < N (orphan methods exist)
- ✅ PASS if M == N (all integrated)

**If orphan methods found:**
- STOP - Fix integration
- Options:
  - Add caller (integrate the method)
  - Remove method (not needed)
- Document decision in TODO

4. **Create integration matrix:**

| New Method | Caller | Call Location | Verified |
|------------|--------|---------------|----------|
| load_adp_data() | PlayerManager.load_players() | PlayerManager.py:180 | ✅ |
| _match_player_to_adp() | PlayerManager.load_players() | PlayerManager.py:210 | ✅ |
| _calculate_adp_multiplier() | PlayerManager.load_players() | PlayerManager.py:215 | ✅ |

**Output:** Integration matrix, no orphan code

**Update Agent Status:**
```
Progress: Round 1 complete (7/8 iterations + iteration 4a)
Next Action: Round 1 checkpoint - evaluate confidence
```

---

## ROUND 1 CHECKPOINT

**After completing Iteration 7:**

1. **Update Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** TODO_CREATION
**Current Step:** Round 1 complete (8/8 iterations), evaluating confidence
**Current Guide:** STAGE_5aa_round1_guide.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- 8 iterations mandatory (Round 1)
- STOP if confidence < Medium
- Iteration 4a PASSED (mandatory gate)

**Progress:** Round 1 complete (8/8 iterations)
**Confidence Level:** {HIGH / MEDIUM / LOW}
**Next Action:** {Create questions file / Proceed to Round 2}
**Blockers:** {List any uncertainties or "None"}
```

2. **Evaluate Confidence:**

**Ask yourself:**
- Do I understand the feature requirements? (HIGH/MEDIUM/LOW)
- Are all algorithms clear? (HIGH/MEDIUM/LOW)
- Are interfaces verified? (HIGH/MEDIUM/LOW)
- Overall confidence: {HIGH/MEDIUM/LOW}

3. **If confidence < MEDIUM:**

**STOP - Create questions file:**

`feature_{N}_{name}_questions.md`:

```markdown
# Feature {N}: {Name} - Questions for User

**Created After:** Round 1 (Iteration 7)
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
```
Blockers: Waiting for user answers to questions file
Next Action: Wait for user responses, then update TODO based on answers
```

**WAIT for user answers. Do NOT proceed to Round 2.**

4. **If confidence >= MEDIUM:**

**Proceed to Round 2:**

```markdown
✅ Round 1 complete (8/8 iterations)

**Confidence Level:** HIGH / MEDIUM
**Questions:** None (or documented in questions file)

**Proceeding to Round 2 (Iterations 8-16).**

**Next Guide:** STAGE_5ab_round2_guide.md
```

---

## Completion Criteria

**Round 1 is complete when ALL of these are true:**

□ All 8 iterations executed (1-7 + 4a) in order
□ Iteration 4a PASSED (TODO Specification Audit)
□ TODO file created with:
  - All requirements covered by tasks
  - All tasks have acceptance criteria
  - Dependencies verified from source code
  - Algorithm Traceability Matrix created
  - Integration Gap Check complete
  - E2E data flow documented
□ Feature README.md updated:
  - Agent Status: "Round 1 complete"
  - Confidence level documented
  - Next action documented

**If any item unchecked:**
- ❌ Round 1 is NOT complete
- Complete missing items before proceeding

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll skip iteration 3, seems simple"
   ✅ STOP - ALL 8 iterations MANDATORY, no exceptions

❌ "I'll assume ConfigManager.get_adp_multiplier interface"
   ✅ STOP - READ actual source code, verify interface (Iteration 2)

❌ "My confidence is low but I'll proceed to Round 2"
   ✅ STOP - Create questions file, wait for answers

❌ "TODO tasks can be vague, I'll figure it out later"
   ✅ STOP - Iteration 4a requires acceptance criteria for EVERY task

❌ "I mapped most algorithms, that's good enough"
   ✅ STOP - Algorithm Traceability Matrix must map ALL algorithms

❌ "This new method seems obvious, don't need caller"
   ✅ STOP - Integration Gap Check requires caller for EVERY new method

❌ "Iteration 4a failed but I'll proceed anyway"
   ✅ STOP - Iteration 4a is MANDATORY GATE, must PASS

❌ "Let me skip to Round 2 now"
   ✅ STOP - Evaluate confidence at checkpoint first
```

---

## Prerequisites for Round 2 (STAGE_5ab)

**Before transitioning to Round 2, verify:**

□ Round 1 completion criteria ALL met
□ Iteration 4a shows: ✅ PASS
□ Confidence level: >= MEDIUM
□ Feature README.md shows:
  - Round 1 complete (8/8)
  - Iteration 4a: PASSED
  - Confidence: HIGH or MEDIUM
  - Next Action: Read STAGE_5ab guide

**If any prerequisite fails:**
- ❌ Do NOT transition to Round 2
- Complete Round 1 missing items

---

## Next Round

**After completing Round 1:**

📖 **READ:** `STAGE_5ab_round2_guide.md`
🎯 **GOAL:** Deep verification - test strategy, edge cases, re-verification
⏱️ **ESTIMATE:** 45-60 minutes

**Round 2 will:**
- Develop comprehensive test strategy (Iteration 8)
- Enumerate all edge cases (Iteration 9)
- Re-verify algorithms, data flow, integration (Iterations 11, 12, 14)
- Check test coverage depth (Iteration 15)
- Plan documentation (Iteration 16)

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Round 2.

---

*End of STAGE_5aa_round1_guide.md*
