# Planning Round 2 - Iterations 8-10: Test Strategy & Configuration

**Purpose:** Develop comprehensive test strategy, enumerate edge cases, and assess configuration impact

**Prerequisites:**
- Planning Round 1 (S5.P1) complete
- implementation_plan.md v1.0 created
- Confidence level >= MEDIUM

**Main Guide:** `stages/s5/s5_p2_planning_round2.md`

---
---

## Prerequisites

**Before starting Iteration 8-10:**

- [ ] Previous iterations complete (as specified in guide header)
- [ ] implementation_plan.md exists and is up to date
- [ ] Working directory: Feature folder
- [ ] S5.P2 Round 2 in progress

**If any prerequisite fails:**
- Complete missing iterations before starting this iteration

---

## Overview

**What is this iteration?**
Iteration 8-10: Test Strategy Development, Edge Cases, Config Tests

**Time Estimate:** As specified in guide header

---


## Iteration 8: Test Strategy Development

**Purpose:** Define comprehensive test strategy for this feature

**Process:**

1. **Categorize tests needed:**
   - Unit tests (test individual methods)
   - Integration tests (test feature as whole)
   - Edge case tests (test error scenarios)
   - Regression tests (ensure no breakage)

2. **Add "Test Strategy" section to implementation_plan.md:**

```markdown
## Test Strategy

### Unit Tests (per-method testing)

**Test File:** tests/league_helper/util/test_PlayerManager_adp.py

1. test_load_adp_data_success()
   - Given: Valid ADP CSV exists
   - When: load_adp_data() called
   - Then: Returns list of tuples with correct data

2. test_load_adp_data_file_not_found()
   - Given: ADP CSV does not exist
   - When: load_adp_data() called
   - Then: Returns empty list, logs error

3. test_match_player_to_adp_found()
   - Given: Player exists in ADP data
   - When: _match_player_to_adp(player) called
   - Then: player.adp_value set correctly

4. test_match_player_to_adp_not_found()
   - Given: Player NOT in ADP data
   - When: _match_player_to_adp(player) called
   - Then: player.adp_value = None

5. test_calculate_adp_multiplier_valid()
   - Given: player.adp_value = 5
   - When: _calculate_adp_multiplier(player) called
   - Then: Returns multiplier from ConfigManager

6. test_calculate_adp_multiplier_none()
   - Given: player.adp_value = None
   - When: _calculate_adp_multiplier(player) called
   - Then: Returns 1.0 (neutral)

7. test_calculate_adp_multiplier_invalid()
   - Given: player.adp_value = -1
   - When: _calculate_adp_multiplier(player) called
   - Then: Returns 1.0, logs warning

---

### Integration Tests (feature-level testing)

**Test File:** tests/integration/test_adp_integration.py

1. test_adp_integration_end_to_end()
   - Given: Valid ADP CSV, player data
   - When: Load players, calculate scores
   - Then: All players have adp_multiplier, scores reflect ADP

2. test_adp_integration_with_other_features()
   - Given: ADP + Injury + Schedule features active
   - When: Calculate scores
   - Then: All multipliers applied, correct final score

---

### Edge Case Tests

1. test_empty_adp_file()
2. test_malformed_adp_csv()
3. test_duplicate_players_in_adp()
4. test_player_name_with_special_characters()

---

### Regression Tests

1. test_existing_scoring_still_works()
   - Ensure existing multipliers still applied
2. test_backward_compatibility()
   - Ensure old code still runs
```markdown

3. **Add test tasks to implementation_plan.md "Implementation Tasks" section:**

```markdown
## Task 15: Unit Tests - ADP Data Loading

**Tests to Create:**
- test_load_adp_data_success()
- test_load_adp_data_file_not_found()
- test_load_adp_data_malformed_csv()

**Acceptance Criteria:**
- [ ] All 3 tests written
- [ ] All 3 tests pass
- [ ] Tests cover success and error paths
- [ ] Tests use fixtures for test data
```markdown

**Output:** "Test Strategy" section added to implementation_plan.md, test tasks added to "Implementation Tasks" section

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
Progress: Iteration 8/16 (Planning Round 2) complete
Next Action: Iteration 9 - Edge Case Enumeration
```markdown

---

## Iteration 9: Edge Case Enumeration

**Purpose:** List ALL edge cases and add "Edge Cases" section to implementation_plan.md

**Process:**

1. **Enumerate edge cases systematically:**

**Data Quality Edge Cases:**
- Empty file
- Malformed CSV (wrong columns, wrong format)
- Duplicate entries
- Missing values (null, empty string)
- Invalid data types

**Boundary Cases:**
- ADP = 0, 1, 500, 501 (boundary values)
- Player name = empty string, very long string
- File size = 0 bytes, very large file

**State Edge Cases:**
- File missing
- File unreadable (permissions)
- Config missing ADP multiplier ranges

**Concurrency Edge Cases:**
- Multiple threads accessing data

2. **For EACH edge case:**
   - Check if spec.md mentions it
   - Check if implementation_plan.md has task for it
   - Check if test strategy covers it

3. **Add "Edge Cases" section to implementation_plan.md:**

**Example:**

```markdown
## Task 18: Edge Case - Duplicate Players in ADP Data

**Edge Case:** ADP CSV contains duplicate player entries

**Handling:**
- load_adp_data() should:
  - Detect duplicates during loading
  - Log warning: "Duplicate player in ADP data: {name}, keeping first occurrence"
  - Keep first occurrence, skip subsequent

**Acceptance Criteria:**
- [ ] Duplicate detection implemented
- [ ] Warning logged for duplicates
- [ ] First occurrence retained
- [ ] No crash on duplicates

**Test:** test_load_adp_data_duplicates()
```markdown

**Output:** "Edge Cases" section added to implementation_plan.md with complete edge case catalog

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
Progress: Iteration 9/16 (Planning Round 2) complete
Next Action: Iteration 10 - Configuration Change Impact
```markdown

---

## Iteration 10: Configuration Change Impact

**Purpose:** Assess impact on league_config.json and ensure backward compatibility

**Process:**

1. **Identify config changes:**
   - New keys added?
   - Existing keys modified?
   - Example: Adding "adp_multiplier_ranges" section

2. **Verify backward compatibility:**
   - What happens if new keys missing?
   - Do we have defaults?

**Example:**

```markdown
## Configuration Impact Assessment

**New Config Keys:**
- `adp_multiplier_ranges`: Dict mapping ADP ranges to multipliers

**Backward Compatibility:**
- **If key missing:** Use default multiplier (1.0 for all players)
- **Migration needed:** No (graceful degradation)
- **User action required:** Optional (feature disabled if not configured)

**Default Values:**
```python
DEFAULT_ADP_MULTIPLIER_RANGES = {
    "1-10": 1.2,
    "11-50": 1.1,
    "51-150": 1.0,
    "151-300": 0.95,
    "301-500": 0.9
}
```markdown

**Config Validation:**
- Task: Add config validation in ConfigManager
- Check: "adp_multiplier_ranges" is dict
- Check: All values are floats
- Fallback: Use defaults if invalid
```markdown

3. **Add config migration tasks to implementation_plan.md "Implementation Tasks" section if needed:**

```markdown
## Task 20: Config Validation - ADP Multiplier Ranges

**Requirement:** Validate ADP config or use defaults

**Implementation:**
- Add: ConfigManager._validate_adp_config()
- Check: "adp_multiplier_ranges" exists and is valid
- Fallback: Use DEFAULT_ADP_MULTIPLIER_RANGES if invalid/missing

**Acceptance Criteria:**
- [ ] Validation method created
- [ ] Invalid config detected and logged
- [ ] Defaults used as fallback
- [ ] No crash on missing config
```markdown

**Output:** Config impact assessment, migration tasks if needed

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
Progress: Iteration 10/16 (Planning Round 2) complete
Next Action: Iteration 11 - Algorithm Traceability Matrix (Re-verify)
```


## Exit Criteria

**Iterations 8-10 complete when ALL of these are true:**

- [ ] All iteration tasks complete as specified in guide
- [ ] implementation_plan.md updated with any discoveries
- [ ] questions.md updated if new questions arose
- [ ] Agent Status updated with progress and next action
- [ ] Ready to proceed to next iteration

**If any criterion unchecked:** Continue iterations until complete

---
---

*End of iterations_8_10_test_strategy.md*
