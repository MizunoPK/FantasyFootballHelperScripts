# Random Parameter Simulation - TODO

**Objective**: Update the iterative simulation to test random parameter combinations using the scaffolded `NUM_PARAMETERS_TO_TEST` variable and `generate_iterative_combinations` function in ConfigGenerator.

**Status**: Draft - Pre-verification

---

## Overview

Modify the `generate_iterative_combinations` function to:
1. Generate configs for the base parameter (as currently done)
2. Randomly select `NUM_PARAMETERS_TO_TEST - 1` additional parameters
3. Generate individual configs for each random parameter (as if it were the only one being tested)
4. Generate combination configs that test multiple parameter values together
5. Merge all configs into a single list

**Example**: If base parameter has values [1,2] and random parameter has values [3,4], generate configs for: [[1], [2], [3], [4], [1,3], [2,4]]

---

## Phase 1: Research and Understanding

### Task 1.1: Examine Current Implementation ✅ COMPLETED
- [x] Read `simulation/ConfigGenerator.py` - `generate_iterative_combinations` at line 339-340 (incomplete)
- [x] `NUM_PARAMETERS_TO_TEST` defined at line 143 as `self.num_parameters_to_test`
- [x] Current implementation calls `generate_single_parameter_configs` but doesn't return
- [x] Helper method `generate_single_parameter_configs` exists (lines 342-428)

**Key Code References:**
- `simulation/ConfigGenerator.py:339-340` - Target function to implement
- `simulation/ConfigGenerator.py:342-428` - Reusable helper for single parameter
- `simulation/ConfigGenerator.py:143` - NUM_PARAMETERS_TO_TEST storage

### Task 1.2: Identify Parameter List ✅ COMPLETED
- [x] 14 parameters total in `PARAMETER_ORDER` (lines 104-121)
- [x] Parameters: 5 scalar + 4 weights + 5 threshold STEPS
- [x] Value generation via `generate_parameter_values()` returns N+1 values per parameter

**Available Parameters:**
1. NORMALIZATION_MAX_SCALE
2. BASE_BYE_PENALTY
3. DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY
4. PRIMARY_BONUS
5. SECONDARY_BONUS
6. ADP_SCORING_WEIGHT
7. PLAYER_RATING_SCORING_WEIGHT
8. PERFORMANCE_SCORING_WEIGHT
9. MATCHUP_SCORING_WEIGHT
10. ADP_SCORING_STEPS
11. PLAYER_RATING_SCORING_STEPS
12. TEAM_QUALITY_SCORING_STEPS
13. PERFORMANCE_SCORING_STEPS
14. MATCHUP_SCORING_STEPS

### Task 1.3: Review SimulationManager Integration ✅ COMPLETED
- [x] Called at `simulation/SimulationManager.py:270`
- [x] Signature: `generate_iterative_combinations(param_name, current_optimal_config)`
- [x] Expected return: `List[dict]` of complete config dictionaries
- [x] Configs are directly used for simulation runs

---

## Phase 2: Implementation

**File**: `simulation/ConfigGenerator.py`
**Function**: `generate_iterative_combinations` (lines 339-340)

### Task 2.0: Input Validation and Error Handling
- [ ] Validate `param_name` is in `self.PARAMETER_ORDER`
- [ ] If not found, raise `ValueError(f"Unknown parameter: {param_name}")`
- [ ] Validate `self.num_parameters_to_test >= 1`
- [ ] If < 1, log warning and default to 1 (base parameter only)
- [ ] Cap `num_parameters_to_test` at `len(self.PARAMETER_ORDER)` (14)
- [ ] If capped, log info about the cap
- [ ] Calculate expected combination count: `(N+1)^num_parameters_to_test`
- [ ] If combination count > 1000, log warning about performance impact
- [ ] Log info about exponential growth (similar to line 525 note about "impractical for full cartesian product")

**Error Handling Pattern**: Follow existing pattern at line 403 - `raise ValueError` with descriptive message
**Performance Note**: Cartesian product grows exponentially. With N=5:
- 2 params: 36 combinations (acceptable)
- 3 params: 216 combinations (acceptable)
- 4 params: 1,296 combinations (getting large, warn user)
- 5 params: 7,776 combinations (very large, warn user)

### Task 2.1: Implement Random Parameter Selection
- [ ] Calculate number of random parameters: `num_random = self.num_parameters_to_test - 1`
- [ ] Create selection pool: `[p for p in self.PARAMETER_ORDER if p != param_name]`
- [ ] Use `random.sample(pool, num_random)` for guaranteed uniqueness
- [ ] Log selected parameters: `self.logger.info(f"Selected {num_random} random parameters: {selected}")`
- [ ] Handle edge cases (covered in Task 2.0):
  - If `num_random == 0`: Empty list, only base parameter
  - If `num_random > available`: Already capped in Task 2.0

**Randomness Decision**: Do NOT seed random - allows different exploration on each run
**Pattern**: Similar to `random.choice()` usage at SimulatedOpponent.py:235

### Task 2.2: Generate Individual Parameter Configs
- [ ] Call `self.generate_single_parameter_configs(param_name, base_config)` for base parameter
- [ ] Store result in `base_configs` list
- [ ] For each random parameter, call `self.generate_single_parameter_configs(random_param, base_config)`
- [ ] Store all parameter config lists in a dictionary: `{param_name: [configs]}`
- [ ] Each config list has N+1 configs (where N = `self.num_test_values`)

**Key Insight**: Reuse existing `generate_single_parameter_configs` method - no need to duplicate logic

**Data Structure Flow** (from iteration 2 research):
- `generate_single_parameter_configs()` returns `List[dict]` (lines 342-428)
- Each dict is a complete config ready for simulation
- Internally uses `_extract_combination_from_config()` (line 430) to get `Dict[str, float]`
- Combination dict has simplified keys: 'NORMALIZATION_MAX_SCALE', 'ADP_SCORING_WEIGHT', etc.
- Then uses `create_config_dict()` (line 472) to rebuild full config structure

**Error Recovery**:
- `generate_single_parameter_configs()` may raise `ValueError(f"Unknown parameter: {param_name}")` (line 403)
- Do NOT catch this error - let it propagate (fail fast)
- If a random parameter is somehow invalid, entire operation should fail
- This prevents silent failures and partial results

### Task 2.3: Generate Combination Configs (CARTESIAN PRODUCT Strategy) ⚠️ USER DECISION
- [ ] Extract parameter values from generated configs:
  ```python
  # For each parameter's config list, extract the values
  param_values = {}
  for param_name in all_params:
      param_values[param_name] = []
      for config in param_configs[param_name]:
          combination = self._extract_combination_from_config(config)
          param_values[param_name].append(combination[param_name])
  ```
- [ ] Use `itertools.product()` to generate ALL combinations (cartesian product):
  ```python
  from itertools import product

  # Get all parameter names and their value lists
  param_names = list(param_values.keys())
  value_lists = [param_values[p] for p in param_names]

  # Generate cartesian product
  combination_configs = []
  for value_tuple in product(*value_lists):
      # Create combination dict with all params from base_config
      combination = self._extract_combination_from_config(base_config)
      # Update with values from this tuple
      for param_name, value in zip(param_names, value_tuple):
          combination[param_name] = value
      # Create full config
      config = self.create_config_dict(combination)
      combination_configs.append(config)
  ```
- [ ] Log number of combination configs generated

**CRITICAL - USER DECISION**: Use FULL CARTESIAN PRODUCT, not ZIP
- Example: param1=[1,2], param2=[3,4] → generates ALL 4 combinations: [1,3], [1,4], [2,3], [2,4]
- Individual configs: [1], [2], [3], [4]
- Cartesian combinations: [1,3], [1,4], [2,3], [2,4] (4 configs)
- Total: 4 individual + 4 cartesian = 8 configs

**Reused Methods**:
- `self._extract_combination_from_config()` - Extract parameter dict from config (line 430)
- `self.create_config_dict()` - Build complete config from parameter dict (line 472)
- `itertools.product()` - Already imported at line 34 for cartesian products

### Task 2.4: Merge All Configs
- [ ] Create master list: `all_configs = []`
- [ ] Add all individual parameter configs (base + random parameters)
- [ ] Add all combination configs
- [ ] Return merged list
- [ ] Log detailed breakdown (per user answer #4):
  ```python
  self.logger.info(
      f"Generated {len(all_configs)} total configs:\n"
      f"  - Base parameter ({param_name}): {len(base_configs)} configs\n"
      f"  - Random parameters ({', '.join(random_params)}): {len(random_configs)} configs\n"
      f"  - Combination configs: {len(combination_configs)} configs"
  )
  ```

**Logging Strategy** (from iteration 2 research):
- Use `self.logger.info()` for major steps (pattern from lines 365, 427)
- Use `self.logger.debug()` for detailed iteration info (if needed)
- No `logger.warning()` exists in ConfigGenerator - add only for performance concerns (> 1000 combinations)

**Expected Output Size** (⚠️ UPDATED for CARTESIAN PRODUCT):
- Individual configs: `NUM_PARAMETERS_TO_TEST * (N+1)` (base + all random parameters)
- Cartesian combinations: `(N+1)^NUM_PARAMETERS_TO_TEST` (all possible value combinations)
- Total: `NUM_PARAMETERS_TO_TEST * (N+1) + (N+1)^NUM_PARAMETERS_TO_TEST` configs

**Example** (NUM_PARAMETERS_TO_TEST=2, N=5):
- Base param: 6 configs
- 1 random param: 6 configs
- Individual total: 12 configs
- Cartesian combinations: 6^2 = 36 configs
- **Total: 48 configs** (not 18 with ZIP!)

**Performance Note**: Cartesian product grows exponentially - with 3 params and N=5, that's 18 individual + 216 combinations = 234 total configs

---

## Phase 3: Testing

**Test File**: `tests/simulation/test_config_generator.py` (already exists with fixtures)

### Task 3.1: Create Unit Tests for `generate_iterative_combinations`
- [ ] Add test class: `TestGenerateIterativeCombinations`
- [ ] Test with `NUM_PARAMETERS_TO_TEST = 1` (base parameter only):
  - Verify returns N+1 configs
  - Verify no random parameters selected
  - Verify no combination configs generated
- [ ] Test with `NUM_PARAMETERS_TO_TEST = 2` (base + 1 random):
  - Verify selects 1 random parameter
  - Verify returns `2*(N+1) + (N+1)^2` configs (with N=5: 12 individual + 36 cartesian = 48 total)
  - Verify combination configs have both parameters varied (all possible combinations)
- [ ] Test with `NUM_PARAMETERS_TO_TEST = 3` (base + 2 random):
  - Verify selects 2 random parameters
  - Verify returns `3*(N+1) + (N+1)^3` configs (with N=5: 18 individual + 216 cartesian = 234 total)
- [ ] Test edge case: `NUM_PARAMETERS_TO_TEST > 14`:
  - Should cap at 14 and log warning
- [ ] Test edge case: Invalid `param_name`:
  - Should raise `ValueError`
- [ ] Test randomness: Run twice, verify different random parameters selected
- [ ] Test config structure: Verify all returned configs have valid structure

**Test Pattern**: Use `@pytest.fixture` for baseline config (existing pattern at line 30)
**Mock Strategy**: No mocking needed - test actual implementation
**Randomness**: Test structure, not specific values (acceptable variance)

### Task 3.2: Integration Testing
- [ ] Manual test: Run `python run_simulation.py` in iterative mode
- [ ] Verify configs are generated without errors
- [ ] Verify simulation completes successfully
- [ ] Check logs show random parameter selection
- [ ] Verify combination configs are being used

**Integration Points**: Only called from SimulationManager.py:270 (verified via Grep)

### Task 3.3: Run Full Test Suite
- [ ] Run `python tests/run_all_tests.py`
- [ ] Fix any failing tests (including existing tests for `generate_single_parameter_configs`)
- [ ] Ensure 100% pass rate (1,837/1,837 tests)

**Potential Impact**: Existing tests may need updates if they mock `generate_iterative_combinations`

---

## Phase 4: Documentation and Cleanup

### Task 4.1: Update Code Comments
- [ ] Add detailed docstrings to modified functions
- [ ] Document the algorithm for config generation
- [ ] Add inline comments for complex logic

### Task 4.2: Update README/Documentation
- [ ] Update `README.md` if iterative simulation usage changed
- [ ] Update `ARCHITECTURE.md` if design changed
- [ ] Document `NUM_PARAMETERS_TO_TEST` configuration

### Task 4.3: Create Code Changes Documentation
- [ ] Create `updates/random_parameter_simulation_code_changes.md`
- [ ] Document all file modifications with line numbers
- [ ] Include before/after code snippets
- [ ] Explain rationale for each change

---

## Phase 5: Final Validation

### Task 5.1: Requirement Verification
- [ ] Re-read original `updates/random_parameter_simulation.txt`
- [ ] Verify all 6 requirements implemented
- [ ] Check example scenario works correctly
- [ ] Confirm changes only in `generate_iterative_combinations`

### Task 5.2: Pre-Commit Validation
- [ ] Run `python tests/run_all_tests.py` - 100% pass required
- [ ] Manual test: Run simulation in iterative mode
- [ ] Verify output configs match expected format
- [ ] Check git diff for unintended changes

### Task 5.3: Cleanup and Move Files
- [ ] Finalize code changes documentation
- [ ] Move `updates/random_parameter_simulation.txt` to `updates/done/`
- [ ] Move `updates/random_parameter_simulation_code_changes.md` to `updates/done/`
- [ ] Delete `updates/random_parameter_simulation_questions.md`

---

## Notes

- **Keep this TODO file updated** as you progress through tasks
- **Run tests after each phase** to catch issues early
- **Changes should be isolated** to `generate_iterative_combinations` function only
- **New session agents**: Read this file to understand current progress and continue work

---

## Verification Summary

**Status**: First verification round COMPLETE ✅

**Iterations Completed**: 3/6
- First round (draft): 3/3 ✅✅✅
- Second round (with answers): 0/3

### Iteration 1 Findings:
- ✅ All 7 requirements from original file covered in TODO
- ✅ Identified target function: `generate_iterative_combinations` at ConfigGenerator.py:339-340
- ✅ Found reusable helper: `generate_single_parameter_configs` (lines 342-428)
- ✅ Clarified combination strategy: ZIP (UPDATED TO CARTESIAN PRODUCT per user answer)
- ✅ Identified 14 available parameters in PARAMETER_ORDER
- ✅ Determined expected output size formula

### Iteration 2 Findings:
- ✅ Added Task 2.0: Input validation and error handling
- ✅ Decided: Do NOT seed random (allows exploration variety)
- ✅ Pattern: Use `random.sample()` for guaranteed uniqueness (vs `random.choice`)
- ✅ Logging pattern: `.info()` for major steps, `.debug()` for details
- ✅ Error handling: `raise ValueError(f"...")` for invalid inputs
- ✅ Added pseudo-code for value extraction and zipping
- ✅ Identified reusable methods for config manipulation

### Iteration 3 Findings:
- ✅ Verified integration points: Only called from SimulationManager.py:270
- ✅ Added comprehensive unit test plan with 7+ test cases
- ✅ Identified test patterns: `@pytest.fixture` for baseline configs
- ✅ No mocking needed - test actual implementation
- ✅ Randomness testing strategy: Test structure, not specific values
- ✅ Added integration test checklist
- ✅ Identified edge cases: cap at 14 params, invalid param_name raises ValueError

**Key Codebase Patterns Identified**:
1. Error handling: `raise ValueError` with descriptive message (line 403)
2. Logging: `self.logger.info()` for counts and major steps (lines 137-138)
3. Random selection: `random.choice()` used elsewhere without seeding (SimulatedOpponent.py:235)
4. Config manipulation:
   - `generate_single_parameter_configs()` - Generate configs for one parameter
   - `_extract_combination_from_config()` - Extract param dict from config (line 430)
   - `create_config_dict()` - Build complete config from param dict (line 472)
5. Test patterns: `@pytest.fixture` for reusable test data (test_config_generator.py:30)

**Critical Dependencies**: None identified
**Risk Areas**: Randomness may select same parameters twice in a row (acceptable variance)
**Total Requirements Added**: 3 new tasks (2.0, detailed test cases, integration points)

**First Round Summary**:
- ✅ 3 complete verification iterations performed
- ✅ All requirements from original file mapped to tasks
- ✅ Specific file paths and line numbers documented
- ✅ Existing code patterns researched and documented
- ✅ Test requirements specified with 7+ test cases
- ✅ Task dependencies verified (no circular dependencies)
- ✅ Edge cases addressed (validation, capping, invalid inputs)
- ✅ Documentation tasks included (code comments, README updates)
- ✅ Pre-commit validation checkpoints added

---

### User Answers Integration (STEP 4 Complete ✅)

**Questions File Created**: `updates/random_parameter_simulation_questions.md`
**User Answers Received**: All 6 questions answered

**Answer 1 - Combination Strategy (CRITICAL)**:
- ✅ Decision: Use FULL CARTESIAN PRODUCT (not ZIP)
- ✅ Impact: Task 2.3 completely rewritten to use `itertools.product()`
- ✅ Impact: Expected output size changed from `(NUM_PARAMETERS_TO_TEST + 1) * (N+1)` to `NUM_PARAMETERS_TO_TEST * (N+1) + (N+1)^NUM_PARAMETERS_TO_TEST`
- ✅ Impact: Test expectations updated (2 params: 48 configs instead of 18)
- ✅ Impact: Added performance note about exponential growth
- Example: param1=[1,2], param2=[3,4] → generates [1,3], [1,4], [2,3], [2,4] (all 4 combinations)

**Answer 2 - Random Selection**:
- ✅ Decision: Non-deterministic (do not seed random)
- ✅ Rationale: Allows exploration variety on each run
- ✅ Pattern: Matches existing `random.choice()` usage in SimulatedOpponent.py:235

**Answer 3 - Edge Case Handling**:
- ✅ Decision: Approved proposed handling
- ✅ NUM_PARAMETERS_TO_TEST = 1: Only base parameter, no combinations
- ✅ NUM_PARAMETERS_TO_TEST ≤ 0: Log warning, default to 1
- ✅ NUM_PARAMETERS_TO_TEST > 14: Cap at 14, log info

**Answer 4 - Logging**:
- ✅ Decision: Add detailed breakdown logging
- ✅ Format: "Generated 48 total configs: Base (X): 6 configs, Random (Y): 6 configs, Combinations: 36 configs"

**Answer 5 - Error Handling**:
- ✅ Decision: Raise ValueError for invalid param_name
- ✅ Pattern: `raise ValueError(f"Unknown parameter: {param_name}")`
- ✅ Rationale: Fail fast to catch configuration errors early

**Answer 6 - Documentation**:
- ✅ Decision: Update README.md and add code comments
- ✅ Task 4.1: Add comprehensive docstring explaining algorithm
- ✅ Task 4.2: Document NUM_PARAMETERS_TO_TEST in README.md

**All Answers Integrated**: ✅ Complete
**TODO File Updated**: ✅ All tasks reflect user decisions
**Ready for Second Verification Round**: ✅ Yes

---

### Second Verification Round (STEP 5 Complete ✅)

**Iterations Completed**: 6/6 total (3 first round + 3 second round)
- Second round: 3/3 ✅✅✅

**📋 ITERATION 4 Findings (Re-read with answers)**:
- ✅ All original requirements still covered with cartesian product approach
- ✅ User answer #1 (cartesian product) impacts: Task 2.3, Task 2.4 formulas, Task 3.1 test expectations
- ✅ User answer #4 (logging) impacts: Task 2.4 logging format
- ✅ No requirements missed after answer integration
- ✅ All 6 user answers fully reflected in implementation tasks

**📋 ITERATION 5 Findings (Deep dive)**:
- ✅ Data structure flow documented: `List[dict]` → `Dict[str, float]` → `List[dict]`
- ✅ Performance considerations added:
  - Cartesian product grows exponentially: (N+1)^num_parameters_to_test
  - 4+ params with N=5 generates 1,000+ configs
  - Added warning logging for > 1000 combinations (Task 2.0)
- ✅ Error recovery strategy: Fail fast - do NOT catch ValueError from `generate_single_parameter_configs()`
- ✅ Logging strategy clarified:
  - `self.logger.info()` for major steps (pattern from lines 365, 427)
  - `self.logger.warning()` for performance concerns only (new addition)
- ✅ Added Task 2.0 sub-tasks: Calculate and warn about combination count

**📋 ITERATION 6 Findings (Final integration)**:
- ✅ Integration point verified: Only called from SimulationManager.py:270
- ✅ No error handling at call site - exceptions propagate (correct behavior)
- ✅ Caller expects `List[dict]` return type (line 275, 281)
- ✅ No existing tests mock this function - no test breakage risk
- ✅ Circular dependency check: None identified
  - `random` already imported at line 30
  - `itertools.product` already imported at line 34
  - No new imports needed
- ✅ No cleanup operations needed on failure (stateless function)
- ✅ Thread safety: Not applicable (simulation runs are separate processes)

**Key Integration Dependencies**:
1. `generate_single_parameter_configs()` (lines 342-428) - Must return List[dict]
2. `_extract_combination_from_config()` (line 430) - Must return Dict[str, float]
3. `create_config_dict()` (line 472) - Must accept Dict[str, float] and return dict
4. `self.PARAMETER_ORDER` (lines 104-121) - Must contain valid parameter names
5. `self.num_parameters_to_test` (line 143) - Must be set by __init__
6. `self.num_test_values` (line 142) - Used to calculate expected config count

**No Risks Identified**:
- ✅ No circular imports
- ✅ No shared state modifications
- ✅ No backward compatibility issues (function currently incomplete)
- ✅ No database/file system dependencies
- ✅ No external API calls

**Second Round Summary**:
- ✅ 3 complete verification iterations performed (total: 6/6)
- ✅ Performance considerations added (exponential growth warnings)
- ✅ Data structure flow fully documented
- ✅ Error recovery strategy defined (fail fast)
- ✅ Integration point verified (SimulationManager.py:270)
- ✅ Dependencies verified (all imports already present)
- ✅ No circular dependency risks
- ✅ Mock requirements: None (test actual implementation)
- ✅ Thread safety: Not applicable

---

**VERIFICATION COMPLETE** ✅

All 6 iterations complete (3 + 3). TODO file is comprehensive and ready for implementation.

**Next Step**: Begin implementation (Phase 2)
