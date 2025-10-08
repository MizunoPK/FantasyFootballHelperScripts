# Simulation Optimization Prep - TODO

**Objective**: Clean up and refactor the simulation folder to prepare for parameter optimization using JSON-based configurations.

**Date Created**: 2025-09-30
**Status**: In Progress
**Related Files**:
- `potential_updates/simulation_optimization_prep.txt`
- `potential_updates/simulation_optimization_strategy.md`
- `potential_updates/simulation_execution_tracker.md`

**IMPORTANT**: Keep this file updated with progress after completing each task to maintain continuity across sessions.

---

## Summary of Changes

Based on user requirements:
1. **JSON-based parameter configs** - Replace `PARAMETER_RANGES` dict with JSON files containing parameter combinations to test
2. **New run script** - Create `run_simulation.py` for running simulations with JSON configs
3. **Remove old --simulate flag** - Clean up existing `run_draft_helper.py`
4. **Parameter storage** - Store JSON configs in `draft_helper/simulation/parameters/`
5. **Cleanup** - Remove unnecessary test scripts and dead code
6. **Comprehensive unit tests** - Ensure all functionality is thoroughly tested
7. **Results workflow** - User runs simulation → tells Claude results are ready → Claude analyzes and creates next iteration JSON

---

## Phase 1: Analysis & Cleanup (Preparation)

**Goal**: Understand current code, identify what to keep/remove, and clean up the simulation folder.

### 1.1 Code Analysis
- [x] Read and understand current simulation structure
- [x] Identify all files in `draft_helper/simulation/` directory
- [x] Identify test scripts vs core functionality files
- [ ] Document current simulation flow and data structures
- [ ] Identify files to delete (one-off test scripts not part of main flow)

### 1.2 Identify Files to Delete
Files to review for deletion (keep unit tests, remove one-off experimental files):
- [ ] Review `test_simulation_config.py` - likely delete
- [ ] Review `comprehensive_parameter_test.py` - likely delete
- [ ] Review `test_basic_simulation.py` - check if it's a unit test or one-off
- [ ] Review `test_simulation_run.py` - check if it's a unit test or one-off
- [ ] Check for any other experimental/temporary files

### 1.3 Document Current PARAMETER_RANGES Structure
- [ ] Document all 20 parameters in current `PARAMETER_RANGES`
- [ ] Create template JSON file showing expected format
- [ ] Verify all parameters are used in the simulation

### 1.4 Pre-Cleanup Validation
- [ ] Run all existing unit tests to establish baseline (must be 100% passing)
- [ ] Document current test count and passing status
- [ ] Ensure all imports work correctly before changes

**Completion Criteria**:
- Clear list of files to delete
- Documented understanding of current system
- All tests passing before any changes

---

## Phase 2: Remove Old --simulate Flag from run_draft_helper.py

**Goal**: Clean up the existing draft helper script by removing the --simulate functionality.

### 2.1 Analyze Current --simulate Implementation
- [ ] Read `run_draft_helper.py` to find --simulate flag implementation
- [ ] Document what the current --simulate flag does
- [ ] Identify all code related to simulation mode in draft helper

### 2.2 Remove --simulate Code
- [ ] Remove argparse --simulate flag from `run_draft_helper.py`
- [ ] Remove any conditional logic that checks for simulate mode
- [ ] Remove any imports only used for simulation mode
- [ ] Ensure draft helper remains fully functional for its core purpose

### 2.3 Validation
- [ ] Run draft helper startup validation: `timeout 10 python run_draft_helper.py`
- [ ] Run integration tests for draft helper (all 23 validation steps)
- [ ] Verify no simulation-related code remains in draft helper

**Completion Criteria**:
- run_draft_helper.py has no --simulate functionality
- Draft helper works perfectly for interactive draft/trade use
- All integration tests pass

**Pre-Commit Validation**: Execute full validation protocol before proceeding to Phase 3

---

## Phase 3: Create JSON Parameter Configuration System

**Goal**: Replace PARAMETER_RANGES dict with JSON-based configuration files.

### 3.1 Create Parameters Directory
- [ ] Create `draft_helper/simulation/parameters/` directory
- [ ] Add `.gitignore` if needed (or ensure parameters are tracked)
- [ ] Create README.md in parameters folder explaining format

### 3.2 Create JSON Schema/Template
- [ ] Create `parameter_template.json` showing expected format
- [ ] Create `baseline_parameters.json` with all current baseline values (first value from each range)
- [ ] Document JSON structure with comments/examples
- [ ] Validate JSON format is correct

Example structure:
```json
{
  "config_name": "baseline",
  "description": "Baseline configuration with all conservative values",
  "parameters": {
    "NORMALIZATION_MAX_SCALE": [100, 120],
    "DRAFT_ORDER_PRIMARY_BONUS": [50, 60],
    ...all 20 parameters...
  }
}
```

### 3.3 Update config.py
- [ ] Remove `PARAMETER_RANGES` dict from `config.py`
- [ ] Add configuration to point to parameters directory
- [ ] Add validation functions for JSON parameter files
- [ ] Keep all other simulation settings (LEAGUE_SIZE, etc.)
- [ ] Update config validation function

### 3.4 Create Parameter Loading Module
- [ ] Create `parameter_loader.py` (or add to existing module)
- [ ] Implement `load_parameter_config(json_path)` function
- [ ] Implement JSON validation (ensure all 20 params present)
- [ ] Implement parameter range expansion (for combination testing)
- [ ] Add error handling for malformed JSON files

### 3.5 Unit Tests for Parameter System
- [ ] Test loading valid JSON parameter files
- [ ] Test error handling for invalid JSON
- [ ] Test error handling for missing parameters
- [ ] Test parameter range expansion logic
- [ ] Test validation functions

**Completion Criteria**:
- Parameters directory created with template files
- PARAMETER_RANGES removed from config.py
- Parameter loading system works correctly
- All unit tests pass

**Pre-Commit Validation**: Execute full validation protocol before proceeding to Phase 4

---

## Phase 4: Update Simulation Engine for JSON Configs

**Goal**: Modify the simulation engine to work with JSON parameter configs instead of PARAMETER_RANGES.

### 4.1 Analyze Current Simulation Flow
- [ ] Review `main_simulator.py` to understand current parameter usage
- [ ] Review `simulation_engine.py` for PARAMETER_RANGES references
- [ ] Review `config_optimizer.py` for parameter combination logic
- [ ] Document how parameters currently flow through the system

### 4.2 Update Simulation Engine
- [ ] Modify simulation engine to accept loaded parameter config
- [ ] Update parameter combination generation logic
- [ ] Ensure all 20 parameters are properly used
- [ ] Update any hardcoded PARAMETER_RANGES references

### 4.3 Update Config Optimizer
- [ ] Update `config_optimizer.py` to work with JSON configs
- [ ] Ensure combination generation works correctly
- [ ] Update any reporting logic to reference JSON config name

### 4.4 Update Results Generation
- [ ] Ensure results file includes which JSON config was used
- [ ] Add config metadata to results file (config name, description)
- [ ] Verify results format matches existing markdown format
- [ ] Add winning parameter combination to results

### 4.5 Unit Tests for Updated Engine
- [ ] Test simulation runs with JSON config
- [ ] Test parameter combination generation
- [ ] Test results include config metadata
- [ ] Test all 20 parameters are applied correctly
- [ ] Test error handling for invalid configs

**Completion Criteria**:
- Simulation engine works with JSON configs
- Results properly document which config was used
- All unit tests pass
- No references to old PARAMETER_RANGES remain

**Pre-Commit Validation**: Execute full validation protocol before proceeding to Phase 5

---

## Phase 5: Create run_simulation.py Script

**Goal**: Create new dedicated script for running simulations with JSON configs.

### 5.1 Design CLI Interface
- [ ] Design argparse interface for `run_simulation.py`
- [ ] Required argument: path to JSON parameter file
- [ ] Optional arguments: number of simulations, output directory, etc.
- [ ] Design help text and usage examples

Expected usage:
```bash
python run_simulation.py parameters/iteration_1.json
python run_simulation.py parameters/baseline.json --sims 20
```

### 5.2 Implement run_simulation.py
- [ ] Create `run_simulation.py` in repository root
- [ ] Implement argument parsing
- [ ] Load JSON parameter config
- [ ] Validate parameter config
- [ ] Run simulation with loaded config
- [ ] Generate results file with timestamped name
- [ ] Print results summary to console
- [ ] Handle errors gracefully

### 5.3 Add User Feedback
- [ ] Progress indicators during simulation
- [ ] Estimated time remaining
- [ ] Clear success/failure messages
- [ ] Path to results file when complete

### 5.4 Integration Testing
- [ ] Test with baseline_parameters.json
- [ ] Test with invalid JSON (should fail gracefully)
- [ ] Test with missing parameters (should fail gracefully)
- [ ] Verify results file is created correctly
- [ ] Verify console output is clear and helpful

**Completion Criteria**:
- run_simulation.py works correctly
- Clear error messages for all failure modes
- Results file generated with correct format
- User experience is smooth

**Pre-Commit Validation**: Execute full validation protocol before proceeding to Phase 6

---

## Phase 6: Delete Obsolete Files

**Goal**: Remove one-off test scripts and dead code identified in Phase 1.

### 6.1 Review Files for Deletion
- [ ] Final review of each file marked for deletion
- [ ] Ensure no other code depends on these files
- [ ] Document reason for deletion of each file

### 6.2 Delete Files
- [ ] Delete identified test/experimental files
- [ ] Remove any obsolete imports from other files
- [ ] Clean up any references in documentation

### 6.3 Verify System Still Works
- [ ] Run all unit tests (must be 100% passing)
- [ ] Test simulation with run_simulation.py
- [ ] Verify no broken imports or missing dependencies

**Completion Criteria**:
- Obsolete files removed
- No broken dependencies
- All tests still pass

**Pre-Commit Validation**: Execute full validation protocol before proceeding to Phase 7

---

## Phase 7: Comprehensive Unit Tests

**Goal**: Ensure comprehensive test coverage for all new functionality.

### 7.1 Identify Test Gaps
- [ ] Review current test coverage
- [ ] Identify untested functionality in new system
- [ ] Create list of tests needed

### 7.2 Create New Unit Tests
- [ ] Test parameter JSON loading (various scenarios)
- [ ] Test parameter validation (missing params, invalid values)
- [ ] Test simulation runs with different configs
- [ ] Test results file generation
- [ ] Test run_simulation.py CLI arguments
- [ ] Test error handling throughout system
- [ ] Test backward compatibility (if any remains)

### 7.3 Update Existing Tests
- [ ] Update any tests that referenced PARAMETER_RANGES
- [ ] Ensure all simulation tests use JSON configs
- [ ] Update test data files if needed

### 7.4 Run All Tests
- [ ] Run entire test suite: `python -m pytest --tb=short`
- [ ] Verify 100% pass rate (577 tests or updated count)
- [ ] Fix any failures
- [ ] Document final test count

**Completion Criteria**:
- Comprehensive test coverage for new JSON system
- All 577+ tests passing
- No test gaps identified

**Pre-Commit Validation**: Execute full validation protocol before proceeding to Phase 8

---

## Phase 8: Documentation Updates

**Goal**: Update all documentation to reflect new JSON-based simulation system.

### 8.1 Update CLAUDE.md
- [ ] Update simulation section with JSON config approach
- [ ] Document new run_simulation.py usage
- [ ] Update parameter configuration instructions
- [ ] Remove references to PARAMETER_RANGES
- [ ] Add examples of creating custom parameter JSONs
- [ ] Document the workflow: run sim → tell Claude → Claude analyzes → Claude creates next JSON

### 8.2 Update README.md (if needed)
- [ ] Update simulation documentation in main README
- [ ] Update quick start guide if affected

### 8.3 Create Simulation Documentation
- [ ] Create or update `draft_helper/simulation/README.md`
- [ ] Document JSON parameter format in detail
- [ ] Provide examples of different parameter configs
- [ ] Document simulation workflow
- [ ] Explain results interpretation

### 8.4 Create Parameter Templates
- [ ] Create example JSONs for different scenarios:
  - `baseline_parameters.json` - all conservative values
  - `aggressive_parameters.json` - all aggressive values
  - `phase1_example.json` - example Phase 1 test config
- [ ] Document each example file

### 8.5 Update Execution Tracker
- [ ] Update tracker to reference new JSON-based system
- [ ] Update instructions for running iterations
- [ ] Update section on Claude's analysis workflow

**Completion Criteria**:
- CLAUDE.md fully updated
- Simulation README comprehensive
- Example parameter JSONs created
- All documentation consistent

**Pre-Commit Validation**: Execute full validation protocol before proceeding to Phase 9

---

## Phase 9: End-to-End Testing & Validation

**Goal**: Perform complete system validation before marking as complete.

### 9.1 Full Repository Test Suite
- [ ] Run `python -m pytest --tb=short` (must be 100% passing)
- [ ] Run `python -m pytest tests/ shared_files/tests/ draft_helper/tests/ starter_helper/tests/ -v`
- [ ] Document final test count and pass rate

### 9.2 Startup Validation
- [ ] Test player data fetcher: `timeout 10 python run_player_data_fetcher.py`
- [ ] Test NFL scores fetcher: `timeout 10 python run_nfl_scores_fetcher.py`
- [ ] Test draft helper: `timeout 10 python run_draft_helper.py`
- [ ] Verify no import or config errors

### 9.3 Draft Helper Integration Testing
- [ ] Copy `tests/draft_helper_validation_checklist.md` to temp
- [ ] Run all 23 validation steps
- [ ] Verify FLEX system, CSV persistence, point calculations
- [ ] All 7 menu options functional

### 9.4 Simulation End-to-End Test
- [ ] Run simulation with baseline config: `python run_simulation.py draft_helper/simulation/parameters/baseline_parameters.json`
- [ ] Verify simulation completes successfully
- [ ] Verify results file created with correct format
- [ ] Verify winning combination identified in results
- [ ] Test with at least 2-3 different parameter configs

### 9.5 Performance Validation
- [ ] Time a single simulation run
- [ ] Verify performance is acceptable (document timing)
- [ ] Check for memory leaks or issues

**Completion Criteria**:
- All 577+ tests passing (100% pass rate)
- All startup validations pass
- Draft helper integration tests pass
- Simulation runs successfully end-to-end
- Performance acceptable

---

## Phase 10: Final Cleanup & Completion

**Goal**: Final checks and move files to completion.

### 10.1 Final Code Review
- [ ] Review all changed files for code quality
- [ ] Remove any debug print statements
- [ ] Ensure consistent code style
- [ ] Check for any TODO comments left in code

### 10.2 Final Documentation Review
- [ ] Verify all documentation is accurate
- [ ] Check for broken links or references
- [ ] Ensure examples work correctly

### 10.3 Git Status Check
- [ ] Review `git status` for any untracked files
- [ ] Ensure no sensitive data in commits
- [ ] Verify all intended files are committed

### 10.4 Final Commit
- [ ] Create final commit with summary of all changes
- [ ] Use proper commit format (no emojis)
- [ ] Include comprehensive summary in commit body

### 10.5 Move Completion Files
- [ ] Move `potential_updates/simulation_optimization_prep.txt` to `potential_updates/done/`
- [ ] Delete `potential_updates/simulation_optimization_prep_questions.md`
- [ ] Move this TODO file to `potential_updates/todo-files/done/`

**Completion Criteria**:
- All code review complete
- Final commit made
- Files moved to done folders
- Objective 100% complete

---

## Pre-Commit Validation Checklist

**EXECUTE AFTER EACH PHASE COMPLETION**

Refer to `potential_updates/rules.txt` for full pre-commit validation protocol. Summary:

1. **Copy Checklist**: `cp tests/pre_commit_validation_checklist.md tests/temp_commit_checklist.md`
2. **Analyze Changes**: `git status` and `git diff`
3. **Unit Tests**: `python -m pytest --tb=short` (100% pass required)
4. **Integration Tests**: Run all 23 draft helper validation steps
5. **Startup Tests**: Validate player data fetcher and NFL scores fetcher start
6. **Documentation**: Update CLAUDE.md, README.md as needed
7. **Commit**: Proper format, no emojis, descriptive message
8. **Cleanup**: Remove temp checklist files

---

## Notes & Observations

### Key Design Decisions
- JSON files contain same format as PARAMETER_RANGES (lists of values to test in combinations)
- Results stay in timestamped markdown format for consistency
- User triggers Claude analysis after simulation completes
- Complete removal of PARAMETER_RANGES for clean architecture

### Files to Create
- `run_simulation.py` - New simulation runner script
- `draft_helper/simulation/parameters/` - Parameter storage directory
- `draft_helper/simulation/parameter_loader.py` - JSON loading module
- `draft_helper/simulation/parameters/baseline_parameters.json` - Example config
- `draft_helper/simulation/parameters/README.md` - Parameter documentation

### Files to Delete (Identified in Phase 1)
- TBD after analysis phase

### Claude's Post-Simulation Workflow
When user says "new simulation result file is ready":
1. Re-read `simulation_execution_tracker.md`
2. Re-read `simulation_optimization_strategy.md`
3. Read latest results file
4. Update tracker with important findings
5. Create next iteration JSON based on results and strategy

---

## Progress Log

**2025-09-30 - Session 1**:
- ✅ Phase 1: Analysis complete - no obsolete files found
- ✅ Phase 2: Removed --simulate flag from run_draft_helper.py
- ✅ Phase 3: Created complete JSON parameter system (34 tests passing)
  - Created parameter_loader.py with validation
  - Created parameters/ directory with baseline and template JSONs
  - Created comprehensive README for parameter system
- ✅ Phase 4: Updated simulation engine for JSON configs
  - Updated config_optimizer.py to use parameter_loader
  - Updated main_simulator.py to accept JSON config paths
  - Removed PARAMETER_RANGES from config.py
- ✅ Phase 5: Created run_simulation.py script with full CLI
- ✅ Phase 8: Updated CLAUDE.md documentation
  - Added simulation workflow section
  - Updated recent changes

**Status**: Core implementation complete. Ready for testing phase.

---

**END OF TODO FILE**

**Remember**: Update this file after completing each task to maintain continuity!
