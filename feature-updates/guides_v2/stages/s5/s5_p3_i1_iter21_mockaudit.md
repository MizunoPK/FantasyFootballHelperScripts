# S5: Feature Implementation
## S5.P3: Planning Round 3
### S5.P3.I1: Mock Audit & Integration Test Plan

**Purpose:** Mock Audit & Integration Test Plan
**Prerequisites:** Previous iterations complete
**Main Guide:** `stages/s5/s5_p3_planning_round3.md`
**Router:** `stages/s5/s5_p3_i1_preparation.md`

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
```
# In test file
mock_config.get_adp_multiplier.return_value = (1.2, 95)
```markdown

**Real interface verification:**

Step 1: Read actual source code
```
# Read real implementation
Read league_helper/util/ConfigManager.py
# Found at line 234
```text

Step 2: Verify real signature
```
# Real interface from ConfigManager.py:234
def get_adp_multiplier(self, adp: int) -> Tuple[float, int]:
    """Returns (multiplier, rank) based on ADP value.

    Args:
        adp (int): ADP ranking value

    Returns:
        Tuple[float, int]: (multiplier, rank)
    """
    # implementation...
```markdown

Step 3: Compare mock to real
- **Mock accepts:** ANY arguments (over-mocking) ⚠️
- **Real accepts:** adp (int)
- **⚠️ PARAMETER MISMATCH:** Mock too permissive, doesn't validate type

- **Mock returns:** (1.2, 95) - Tuple[float, int] ✅
- **Real returns:** Tuple[float, int] ✅
- **✅ RETURN TYPE MATCH**

**Issue Found:** Mock doesn't validate parameter type

**Fix:** Update mock to validate parameters
```
def mock_get_adp_multiplier(adp: int):
    assert isinstance(adp, int), "adp must be int"
    assert adp > 0, "adp must be positive"
    return (1.2, 95)

mock_config.get_adp_multiplier = mock_get_adp_multiplier
```markdown

**Verification:** ✅ FIXED - Mock now matches real interface

**Action:** Update test file with fixed mock

---

### Mock 2: csv_utils.read_csv_with_validation

**Used in tests:** test_load_adp_data_success()

**Mock definition:**
```
mock_read_csv.return_value = pd.DataFrame([...])
```markdown

**Real interface verification:**

Step 1: Read actual source
```
Read utils/csv_utils.py
# Found at line 45
```text

Step 2: Verify real signature
```
# Real interface from csv_utils.py:45
def read_csv_with_validation(
    filepath: Union[str, Path],
    required_columns: List[str],
    encoding: str = 'utf-8'
) -> pd.DataFrame:
    """Reads CSV and validates required columns exist."""
```markdown

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
Progress: Iteration 21/24 (Planning Round 3 Part 1) complete
Mock Audit: 5 mocks audited, 1 issue fixed
Integration Tests: 3 real-object tests planned
Next Action: Iteration 22 - Output Consumer Validation
```

---

