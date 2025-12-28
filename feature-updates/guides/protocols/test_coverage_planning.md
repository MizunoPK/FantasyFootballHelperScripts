# Test Coverage Planning Protocol

**Purpose:** Plan behavior tests that would fail if algorithm is wrong, and audit mocks to ensure they match real interfaces.

**Related:** [README.md](README.md) - Protocol index

---


**Execute during:** Iteration 21

**Steps:**

1. **For each algorithm in spec:**
   - Identify the calculation or logic
   - Define expected input → output pairs
   - Define what WRONG implementation would produce

2. **Design tests that catch wrong implementations:**
   ```
   GOOD: test_player_rating_week2_uses_cumulative_points()
         - Input: Week 2, player with 20pts week 1
         - Expected: Rating based on cumulative
         - Would catch: Code using single week points

   BAD: test_player_rating_exists()
         - Only checks field exists
         - Would NOT catch: Wrong calculation
   ```

3. **For each conditional in spec:**
   - Test both branches
   - Test boundary conditions
   - Test that wrong branch would fail

4. **Document test plan:**
   ```
   | Algorithm | Test Name | Input | Expected | Catches |
   |-----------|-----------|-------|----------|---------|
   | Week scoring | test_week_2_cumulative | W2, 20pts | cumulative | single-week bug |
   ```

5. **Mock Audit (CRITICAL):**
   For each mocked dependency in the test plan:

   a. **List all mocked classes/methods:**
      ```
      | Mock | Real Class | Real Method | Signature Verified? |
      |------|------------|-------------|---------------------|
      | mock_config_gen | ConfigGenerator | generate_iterative_combinations | [ ] |
      | mock_progress | ProgressTracker | update | [ ] |
      ```

   b. **Verify each mock matches real interface:**
      - Read the actual class definition
      - Compare mock method calls to real method signatures
      - Verify parameter names and types match
      - Flag any mismatches for correction

   c. **Check for over-mocking:**
      - If mock accepts ANY arguments, it won't catch interface mismatches
      - Consider using `spec=RealClass` in `@patch` decorators
      - Example: `@patch('module.ClassName', spec=ClassName)`

   d. **Plan at least one integration test:**
      - Identify which test can use REAL objects instead of mocks
      - This test should exercise the actual integration path
      - Document: "Integration test X uses real ConfigGenerator and ProgressTracker"

   **Mock Audit Checklist:**
   ```
   □ All mocked dependencies listed
   □ Each mock's interface verified against real class
   □ At least one integration test planned with real objects
   □ Tests using spec= where appropriate
   □ No tests that would pass with wrong interface
   ```

6. **Output Consumer Validation (MANDATORY for features producing output files):**

   a. **Identify all outputs and their consumers:**
      ```
      | Output | Consumer | Consumer Location | Roundtrip Test |
      |--------|----------|-------------------|----------------|
      | accuracy_optimal_*/ | find_baseline_config | run_accuracy_sim.py | test_output_as_baseline |
      | accuracy_optimal_*/ | ConfigGenerator | shared/ConfigGenerator.py | test_output_as_baseline |
      ```

   b. **Plan roundtrip test for each output/consumer pair:**
      - Test MUST save output using new code
      - Test MUST load output using REAL consumer (not mocked)
      - Test MUST verify loaded data is usable

   c. **Example roundtrip test:**
      ```python
      def test_optimal_folder_usable_as_baseline(self, manager):
          """Verify output folder can be loaded as baseline for next run."""
          # Save output
          output_path = manager.save_optimal_configs()

          # Verify all required files exist
          required = ['league_config.json', 'draft_config.json', 'week1-5.json', ...]
          for f in required:
              assert (output_path / f).exists()

          # Load using REAL consumer (not mocked)
          config_gen = ConfigGenerator(output_path, parameter_order=...)
          assert config_gen.baseline_config is not None
      ```

   **Output Consumer Checklist:**
   ```
   □ All output files/folders identified
   □ All consumers of each output identified
   □ Roundtrip test planned for each output
   □ Roundtrip test uses REAL consumers, not mocks
   □ Test verifies output is actually usable, not just exists
   ```

**Output:** Test plan with behavior tests for all algorithms AND verified mock interfaces AND output consumer validation.

### Test Naming Convention

Use descriptive test names that explain what is being tested, under what conditions, and what should happen.

**Format:** `test_{unit}_{scenario}_{expected_behavior}`

**Good Examples:**
```python
# Clear: explains what, when, and expected outcome
def test_mae_calculation_with_bye_week_players_excludes_zero_actual():
    """MAE should exclude players with 0 actual points (bye weeks)."""
    pass

def test_player_rating_week_one_uses_draft_rank():
    """Week 1 player rating should use draft rank, not points."""
    pass

def test_config_save_with_empty_config_raises_validation_error():
    """Saving empty config should raise ValidationError."""
    pass

def test_parallel_runner_with_single_thread_completes_successfully():
    """Runner should work correctly even with thread_count=1."""
    pass
```

**Bad Examples:**
```python
# Vague: doesn't explain scenario or expected behavior
def test_mae():  # What about MAE? What scenario?
    pass

def test_player_rating():  # Which aspect? Which week?
    pass

def test_save():  # Save what? What should happen?
    pass

def test_1():  # Completely meaningless
    pass
```

**Why good names matter:**
- Test failures are immediately understandable: "test_mae_calculation_with_bye_week_players_excludes_zero_actual FAILED" tells you exactly what broke
- Tests serve as documentation: reading test names explains feature behavior
- Encourages thinking about edge cases: naming forces you to articulate the scenario

**Naming Checklist:**
```
□ Test name includes the unit being tested (method/class)
□ Test name includes the scenario/condition
□ Test name includes expected behavior/outcome
□ Test name is readable as a sentence when prefixed with "Verify that..."
```

---

### Test-First Implementation Principle

When possible, write tests BEFORE implementation:

**The Test-First Workflow:**
1. **Write failing test** that describes expected behavior
2. **Run test** - confirm it fails (red)
3. **Implement code** to make test pass
4. **Run test** - confirm it passes (green)
5. **Refactor** if needed, keeping tests green

**Benefits:**
- Forces you to think about behavior before code structure
- Naturally creates behavior tests (not structure tests)
- Catches "tests pass but behavior wrong" issues
- Documents expected behavior before implementation

**When to Use Test-First:**
- New methods with calculcations or algorithms
- New classes with business logic
- Edge case handling
- Any code where "what should happen" is clearer than "how to implement"

**When Test-First May Not Apply:**
- Simple data classes with no logic
- Boilerplate code (imports, setup)
- Integration code where the test requires the implementation to exist

**Test-First Checklist:**
```
□ Expected behavior documented in test name
□ Test runs and FAILS before implementation
□ Implementation makes test pass
□ Additional edge case tests added
□ Refactoring doesn't break tests
```

**Example:**
```python
# STEP 1: Write failing test FIRST
def test_mae_calculation_excludes_zero_actual_points():
    """MAE should exclude players with 0 actual points (bye weeks)."""
    players = [
        Player(projected=10.0, actual=12.0),  # Include
        Player(projected=15.0, actual=0.0),   # Exclude (bye week)
        Player(projected=8.0, actual=10.0),   # Include
    ]
    calculator = AccuracyCalculator()
    mae = calculator.calculate_mae(players)
    # Expected: (|10-12| + |8-10|) / 2 = (2 + 2) / 2 = 2.0
    assert mae == 2.0  # NOT (2 + 15 + 2) / 3 = 6.33

# STEP 2: Run test - it fails (AccuracyCalculator doesn't exist yet)
# STEP 3: Implement AccuracyCalculator.calculate_mae()
# STEP 4: Run test - it passes
# STEP 5: Add more edge case tests
```

---

