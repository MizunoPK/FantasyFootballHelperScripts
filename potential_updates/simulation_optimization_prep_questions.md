# Clarifying Questions: Simulation Optimization Prep

**Date**: 2025-09-30
**Related File**: `simulation_optimization_prep.txt`
**Status**: Awaiting User Response

---

## Questions for User

### 1. **JSON Parameter Files Structure**
You want to pass parameter configs via JSON files (e.g., `iteration_1.json`). Should these JSON files:

- **Option A**: Contain ALL 20 parameters with specific single values (not ranges)?
  ```json
  {
    "NORMALIZATION_MAX_SCALE": 100,
    "DRAFT_ORDER_PRIMARY_BONUS": 50,
    "DRAFT_ORDER_SECONDARY_BONUS": 25,
    ...all 20 parameters...
  }
  ```

- **Option B**: Only specify the parameters being tested for that iteration, with defaults for the rest?
  ```json
  {
    "NORMALIZATION_MAX_SCALE": 100,
    "DRAFT_ORDER_PRIMARY_BONUS": 50,
    "DRAFT_ORDER_SECONDARY_BONUS": 25
    // Other parameters use baseline defaults
  }
  ```

**Your Answer**:
It should contain all 20 parameters in the same format as the existing PARAMETER_RANGES variable, where each parameter is a list of values that will be tested in combinations and the final report should say what combination of values had the highest win rate.

---

### 2. **Command Line Interface**
You mentioned: `python run_draft_helper.py --simulate iteration_1.json`

Should I:
- **Option A**: Create a new `run_simulation.py` script (since `run_draft_helper.py` is for the interactive draft tool)?
- **Option B**: Add `--simulate` flag to existing `run_draft_helper.py`?
- **Option C**: Use a different command structure entirely?

**Your Answer**:
Option A - make a new script. The --simulate flag already exists in the run_draft_helper.py run but let's remove that in leu of the dedicated run script

---

### 3. **Test Scripts to Delete**
Which test scripts should be removed? I found:
- `test_simulation_config.py` in the simulation folder
- Are there other test/experimental files in `draft_helper/simulation/` that should be deleted?

Should I keep the pytest tests in `draft_helper/tests/` that test the simulation components?

**Your Answer**:
Keep unit tests - remove any one off files that are not connected to the main flow of the script.

---

### 4. **Results File Format**
After simulation completes, what should the results file be named/formatted?

Current system uses timestamped markdown files: `result_2025-09-26_14-22-43.md`

Should results be:
- **Option A**: `iteration_1_results.csv` (CSV format with iteration name)
- **Option B**: `iteration_1_results.json` (JSON format with iteration name)
- **Option C**: Stay as timestamped markdown files
- **Option D**: Both JSON/CSV data files AND a markdown summary

**Your Answer**:
Option C

---

### 5. **Execution Tracker Auto-Update**
You mentioned Claude should update the execution tracker after each run. Should I:

- **Option A**: Create a Python script that auto-updates the tracker markdown file with results when simulation completes?
- **Option B**: You'll manually tell me the results filename and I'll read it and update the tracker?

**Your Answer**:
Option B

---

### 6. **Next Parameter JSON Generation**
After analyzing results, should the system:

- **Option A**: Automatically analyze results and generate the next parameter JSON file based on winners?
- **Option B**: I provide recommendations and you decide what parameters to test next?
- **Option C**: Fully automated optimization that runs all phases without user intervention?

**Your Answer**:
The simulation script's duties should end at creating the results file. After the results are made, I will open claude and say something along the lines of 'a new simulation result file is ready', then claude should 1. re-read the simulation_execution_tracker.md and simulation_optimization_strategy.md files, 2. read the latest results file, 3. Update the tracker to include the important findings from the result file, 4. Create a new json file with the next set of parameters that should be tested based on the results and optimization strategy.

---

### 7. **Backward Compatibility**
Should the simulation still support the old `PARAMETER_RANGES` dict approach for testing, or completely replace it with JSON-based configs?

- **Option A**: Remove `PARAMETER_RANGES` entirely, only support JSON configs
- **Option B**: Keep both approaches (JSON for optimization, ranges for other testing)

**Your Answer**:
Remove the existing PARAMETER_RANGES entirely - we will work exclusively with the json files from here on.

---

### 8. **Parameters Folder Location**
You mentioned storing JSON parameter files in a `parameters/` folder. Should this be:

- **Option A**: `draft_helper/simulation/parameters/`
- **Option B**: `potential_updates/simulation_parameters/`
- **Option C**: Other location?

**Your Answer**:
Option A

---

## Instructions for User

Please answer each question above by filling in the "Your Answer" sections. You can be brief - just indicate which option (A/B/C) or provide a short answer.

Once you've answered these questions, I'll create the comprehensive TODO file and begin implementation.

---

**Note**: This questions file will be deleted once answers are incorporated into the TODO file.
