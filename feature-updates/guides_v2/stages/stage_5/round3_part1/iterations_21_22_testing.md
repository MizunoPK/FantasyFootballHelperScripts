# STAGE 5ac Part 1: Iterations 21-22 - Mock Audit & Output Validation

**Part of:** Epic-Driven Development Workflow v2
**Stage:** 5ac - Implementation Planning Round 3 Part 1
**Iterations:** 21-22
**Purpose:** Verify mocks match real interfaces and outputs are consumable
**Prerequisites:** Iterations 19-20 complete
**Main Guide:** stages/stage_5/round3_part1_preparation.md

---

## Overview

Iterations 21-22 validate testing approach and output compatibility:
- **Iteration 21:** Mock audit and integration test planning (CRITICAL - prevents interface mismatch bugs)
- **Iteration 22:** Output consumer validation (ensures downstream compatibility)

**Time estimate:** 15-25 minutes (both iterations)

---

## Iteration 21: Mock Audit & Integration Test Plan (CRITICAL)

**Purpose:** Verify mocks match real interfaces, plan integration tests with real objects

**⚠️ CRITICAL:** Unit tests with wrong mocks can pass while hiding interface mismatch bugs

**Why this matters:**
- Mocks that don't match real interfaces → Tests pass but feature fails
- Integration tests with real objects → Prove feature works in real environment

### Process

**1. List ALL mocked dependencies in unit tests:**

Review test files and identify every mocked class/function.

**2. For EACH mock, verify against real interface:**

```markdown
## Mock Audit (Iteration 21)

### Mock 1: ConfigManager.get_adp_multiplier

**Used in tests:** test_calculate_adp_multiplier_valid()

**Mock definition:**
```python
# In test file
mock_config.get_adp_multiplier.return_value = (1.2, 95)
```

**Real interface verification:**

Step 1: Read actual source code
```bash
# Read real implementation
Read league_helper/util/ConfigManager.py
# Found at line 234
```

Step 2: Verify real signature
```python
# Real interface from ConfigManager.py:234
def get_adp_multiplier(self, adp: int) -> Tuple[float, int]:
    """Returns (multiplier, rank) based on ADP value.

    Args:
        adp (int): ADP ranking value

    Returns:
        Tuple[float, int]: (multiplier, rank)
    """
    # implementation...
```

Step 3: Compare mock to real
- **Mock accepts:** ANY arguments (over-mocking) ⚠️
- **Real accepts:** adp (int)
- **⚠️ PARAMETER MISMATCH:** Mock too permissive, doesn't validate type

- **Mock returns:** (1.2, 95) - Tuple[float, int] ✅
- **Real returns:** Tuple[float, int] ✅
- **✅ RETURN TYPE MATCH**

**Issue Found:** Mock doesn't validate parameter type

**Fix:** Update mock to validate parameters
```python
def mock_get_adp_multiplier(adp: int):
    assert isinstance(adp, int), "adp must be int"
    assert adp > 0, "adp must be positive"
    return (1.2, 95)

mock_config.get_adp_multiplier = mock_get_adp_multiplier
```

**Verification:** ✅ FIXED - Mock now matches real interface

**Action:** Update test file with fixed mock

---

### Mock 2: csv_utils.read_csv_with_validation

**Used in tests:** test_load_adp_data_success()

**Mock definition:**
```python
mock_read_csv.return_value = pd.DataFrame([...])
```

**Real interface verification:**

Step 1: Read actual source
```bash
Read utils/csv_utils.py
# Found at line 45
```

Step 2: Verify real signature
```python
# Real interface from csv_utils.py:45
def read_csv_with_validation(
    filepath: Union[str, Path],
    required_columns: List[str],
    encoding: str = 'utf-8'
) -> pd.DataFrame:
    """Reads CSV and validates required columns exist."""
```

Step 3: Compare mock to real
- **Mock accepts:** ANY (uses MagicMock default) ✅
- **Real accepts:** filepath, required_columns, encoding (optional)
- **✅ ACCEPTABLE:** Test only uses (filepath, required_columns)

- **Mock returns:** pd.DataFrame ✅
- **Real returns:** pd.DataFrame ✅
- **✅ RETURN TYPE MATCH**

**Verification:** ✅ PASSED - Mock matches real interface

---

### Mock 3: [Continue for ALL mocks in test suite]

[Repeat mock audit for each dependency]

---

## Mock Audit Summary

**Total Mocks Audited:** 5
**Mocks with Issues:** 1 (ConfigManager.get_adp_multiplier)
**Fixes Required:** 1 (update mock to validate parameters)

**✅ All mock issues fixed, audit PASSED**

---
```

**3. Plan integration tests with REAL objects (no mocks):**

```markdown
## Integration Test Plan (No Mocks)

**Purpose:** Prove feature works with REAL objects (not mocks)

**Why no mocks:** Catch interface mismatches that mocks hide

---

### Integration Test 1: test_adp_integration_with_real_config()

**Purpose:** Verify ADP integration works with REAL ConfigManager

**Setup:**
- Use REAL ConfigManager (not mock)
- Use REAL league_config.json
- Use test ADP CSV file in tmp_path

**Steps:**
1. Create test config file: `tmp_path / "league_config.json"`
2. Initialize REAL ConfigManager(data_folder=tmp_path)
3. Load ADP data from test CSV
4. Match player "Patrick Mahomes, QB"
5. Call REAL ConfigManager.get_adp_multiplier(adp=5)
6. Verify result matches expected (multiplier, rank) from config

**Acceptance Criteria:**
- [ ] Uses REAL ConfigManager (no mocks)
- [ ] Uses REAL league_config.json
- [ ] No mocks used anywhere
- [ ] Test passes (proves real integration works)

**Expected Duration:** ~100ms (acceptable for integration test)

---

### Integration Test 2: test_adp_integration_with_real_csv_utils()

**Purpose:** Verify ADP loading works with REAL csv_utils

**Setup:**
- Use REAL csv_utils.read_csv_with_validation
- Create test CSV file in tmp_path

**Steps:**
1. Create test CSV: `tmp_path / "adp_test.csv"`
2. Write test data: "Name,Position,ADP\nPatrick Mahomes,QB,5\n"
3. Call REAL csv_utils.read_csv_with_validation(filepath, required_columns)
4. Verify DataFrame loaded correctly
5. Verify columns exist: Name, Position, ADP

**Acceptance Criteria:**
- [ ] Uses REAL csv_utils (no mocks)
- [ ] Creates real CSV file
- [ ] No mocks used
- [ ] Test proves CSV parsing works

**Expected Duration:** ~50ms

---

### Integration Test 3: test_adp_end_to_end_real_objects()

**Purpose:** Full E2E test with ALL real objects (comprehensive)

**Setup:**
- REAL ConfigManager
- REAL csv_utils
- REAL PlayerManager
- REAL FantasyPlayer
- NO MOCKS ANYWHERE

**Steps:**
1. Initialize PlayerManager with test data folder
2. Load ADP data (uses REAL csv_utils)
3. Load players (uses REAL PlayerManager)
4. Calculate scores (uses REAL ConfigManager.get_adp_multiplier())
5. Verify: All players have adp_value set
6. Verify: All players have adp_rank set
7. Verify: Scores reflect ADP contribution
8. Verify: Top-ranked player (ADP=1) has highest multiplier

**Acceptance Criteria:**
- [ ] NO MOCKS used anywhere in test
- [ ] All objects are real implementations
- [ ] All steps execute successfully
- [ ] Test proves entire feature works end-to-end

**Expected Duration:** ~500ms (acceptable for E2E test)

---
```

**4. Add integration test tasks to implementation_plan.md "Implementation Tasks" section:**

```markdown
## Task 35: Integration Test - Real ConfigManager

**Requirement:** Test ADP integration with REAL ConfigManager (no mocks)

**Test:** test_adp_integration_with_real_config()

**Acceptance Criteria:**
- [ ] Uses REAL ConfigManager
- [ ] Uses REAL league_config.json
- [ ] No mocks used
- [ ] Test passes (proves real integration works)

---

## Task 36: Integration Test - Real CSV Utils

**Requirement:** Test ADP loading with REAL csv_utils (no mocks)

**Test:** test_adp_integration_with_real_csv_utils()

**Acceptance Criteria:**
- [ ] Uses REAL csv_utils.read_csv_with_validation
- [ ] Creates test CSV file
- [ ] No mocks used
- [ ] Test passes

---

## Task 37: Integration Test - End-to-End (No Mocks)

**Requirement:** Full E2E test with ALL real objects

**Test:** test_adp_end_to_end_real_objects()

**Acceptance Criteria:**
- [ ] Uses REAL ConfigManager, csv_utils, PlayerManager
- [ ] NO mocks used anywhere
- [ ] All steps execute successfully
- [ ] Test proves feature works in real environment

---
```

### Iteration 21 Output

**Output:**
- Mock audit report (all mocks verified)
- Integration test plan (at least 3 real-object tests)
- Tasks added for integration tests

### After Iteration Checkpoint - questions.md Review

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

### Update Agent Status

```markdown
Progress: Iteration 21/24 (Round 3 Part 1) complete
Mock Audit: 5 mocks audited, 1 issue fixed
Integration Tests: 3 real-object tests planned
Next Action: Iteration 22 - Output Consumer Validation
```

---

## Iteration 22: Output Consumer Validation

**Purpose:** Verify feature outputs are consumable by downstream code

**Why this matters:** Feature can work in isolation but fail when consumed by other modules → Integration failures

### Process

**1. Identify output consumers:**

```markdown
## Output Consumer Analysis

**Feature Output:** Updated FantasyPlayer objects with:
- player.adp_value (int): ADP ranking
- player.adp_rank (int): Rank in ADP list
- player.adp_multiplier (float): Score multiplier from ADP

**Downstream Consumers:**

1. **AddToRosterModeManager.get_recommendations()**
   - Consumes: FantasyPlayer objects with adp_multiplier
   - Usage: Generates draft recommendations sorted by score
   - Impact: Must handle players with adp_multiplier applied

2. **StarterHelperModeManager.get_optimal_lineup()**
   - Consumes: Roster FantasyPlayer objects with adp_multiplier
   - Usage: Selects optimal lineup based on scores
   - Impact: Must use ADP-adjusted scores for lineup decisions

3. **TradeAnalyzerModeManager.analyze_trade()**
   - Consumes: FantasyPlayer objects for trade analysis
   - Usage: Compares player values
   - Impact: Should use ADP-adjusted scores for trade value

---
```

**2. Plan roundtrip validation tests:**

```markdown
## Output Consumer Validation Tests

### Consumer 1: AddToRosterModeManager (Draft Mode)

**Roundtrip Test:** test_adp_output_consumed_by_draft_mode()

**Steps:**
1. Load players with ADP integration (REAL PlayerManager)
2. Verify: Players have adp_value, adp_rank, adp_multiplier set
3. Call: AddToRosterModeManager.get_recommendations() with ADP-enabled players
4. Verify: Recommendations generated successfully (no errors)
5. Verify: Recommendations use ADP-adjusted scores
6. Verify: Top recommendations include high-ADP players (logic check)
7. Verify: Low-ADP players ranked lower

**Expected Behavior:** Draft recommendations prioritize high-ADP players

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Recommendations use adp_multiplier in scoring
- [ ] Top 10 recommendations include players with ADP <20
- [ ] No AttributeError or KeyError

---

### Consumer 2: StarterHelperModeManager (Starter Mode)

**Roundtrip Test:** test_adp_output_consumed_by_starter_mode()

**Steps:**
1. Load roster players with ADP integration
2. Verify: Roster players have adp_multiplier set
3. Call: StarterHelperModeManager.get_optimal_lineup()
4. Verify: Lineup selection successful (no errors)
5. Verify: Lineup scores include ADP contribution
6. Verify: Optimal lineup selects high-ADP players when scores close

**Expected Behavior:** Lineup optimizer uses ADP-adjusted scores

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Lineup scores reflect adp_multiplier
- [ ] No AttributeError or KeyError

---

### Consumer 3: TradeAnalyzerModeManager (Trade Mode)

**Roundtrip Test:** test_adp_output_consumed_by_trade_analyzer()

**Steps:**
1. Load players with ADP integration
2. Create mock trade: Give player A, Receive player B
3. Call: TradeAnalyzerModeManager.analyze_trade()
4. Verify: Trade analysis successful (no errors)
5. Verify: Trade value uses ADP-adjusted scores
6. Verify: Analysis shows "fair" when ADP values similar

**Expected Behavior:** Trade analysis uses ADP-adjusted values

**Acceptance Criteria:**
- [ ] Consumer code runs without errors
- [ ] Trade values reflect adp_multiplier
- [ ] No AttributeError or KeyError

---
```

**3. Add consumer validation tasks to implementation_plan.md "Implementation Tasks" section:**

```markdown
## Task 40: Consumer Validation - Draft Mode

**Requirement:** Verify AddToRosterModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_draft_mode()

**Acceptance Criteria:**
- [ ] Load players with ADP integration
- [ ] Call AddToRosterModeManager.get_recommendations()
- [ ] Verify recommendations use ADP-adjusted scores
- [ ] Verify top recommendations include high-ADP players
- [ ] No errors in consumer code

---

## Task 41: Consumer Validation - Starter Mode

**Requirement:** Verify StarterHelperModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_starter_mode()

**Acceptance Criteria:**
- [ ] Load roster with ADP integration
- [ ] Call StarterHelperModeManager.get_optimal_lineup()
- [ ] Verify lineup selection works
- [ ] Verify lineup scores include ADP contribution
- [ ] No errors in consumer code

---

## Task 42: Consumer Validation - Trade Analyzer

**Requirement:** Verify TradeAnalyzerModeManager consumes ADP-adjusted scores

**Test:** test_adp_output_consumed_by_trade_analyzer()

**Acceptance Criteria:**
- [ ] Load players with ADP integration
- [ ] Call TradeAnalyzerModeManager.analyze_trade()
- [ ] Verify trade analysis works
- [ ] Verify trade values use ADP-adjusted scores
- [ ] No errors in consumer code

---
```

### Iteration 22 Output

**Output:** Output consumer validation plan with roundtrip tests

### After Iteration Checkpoint - questions.md Review

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

### Update Agent Status

```markdown
Progress: Iteration 22/24 (Round 3 Part 1) complete
Consumer Validation: 3 consumers identified, roundtrip tests planned
Part 1 COMPLETE - Ready for Part 2
Next Action: Read stages/stage_5/round3_part2_final_gates.md
```

---

## Summary - Iterations 21-22

**Completed:**
- [ ] Iteration 21: Mock audit (5 mocks verified, 1 fixed) + integration tests (3 planned)
- [ ] Iteration 22: Output consumer validation (3 consumers, roundtrip tests)

**Key Outputs:**
- Mock audit prevents interface mismatch bugs
- Integration tests prove feature works with real objects
- Consumer validation ensures downstream compatibility
- All added to implementation_plan.md

**Part 1 COMPLETE - Next:** Read `stages/stage_5/round3_part2_final_gates.md` for Part 2

---

**END OF ITERATIONS 21-22 GUIDE**
