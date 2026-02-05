# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I3: Error Handling Scenarios

**Purpose:** Error Handling Scenarios
**Prerequisites:** Previous iterations complete
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`
**Router:** `stages/s5/s5_p1_i3_integration.md`

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

