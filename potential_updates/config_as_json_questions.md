# Questions for JSON Parameter Configuration Update

## Scope and Parameter Clarification

1. **Parameter Count Discrepancy**: The config_as_json.txt mentions "23 parameters" but the existing parameters.json only contains 23 parameters in the "parameters" section. The draft_helper_config.py and starter_helper_config.py contain many MORE configuration values beyond these 23. Should we:
   - Only move the 23 parameters that are already in parameters.json?
   - Move ALL scoring-related parameters from both config files?
   - Keep some parameters in the config files (like MAX_POSITIONS, DRAFT_ORDER structure, etc.)?
Answer: For now, only move over the 23 parameters that the json file mentions. We may move more over at a later time, but we will start with those 23


2. **Which parameters should remain in config files?** For example:
   - `MAX_POSITIONS` (roster construction limits)
   - `DRAFT_ORDER` (round-by-round draft strategy)
   - `FLEX_ELIGIBLE_POSITIONS`
   - `STARTING_LINEUP_REQUIREMENTS`
   - `POSSIBLE_BYE_WEEKS`
   - Display settings (SHOW_PROJECTION_DETAILS, RECOMMENDATION_COUNT)
   - Logging settings
   - File path settings
   - Should these stay in config files or move to JSON?
Answer: Keep all of these in the config files for now. Start with moving over the 23 mentioned parameters then we will move over more later as a future improvement.

3. **Consistency Scoring Parameters**: The parameters.json includes consistency multipliers (CONSISTENCY_LOW_MULTIPLIER, etc.) but draft_helper_config.py also has:
   - `ENABLE_CONSISTENCY_SCORING` (boolean toggle)
   - `CONSISTENCY_CV_LOW_THRESHOLD`
   - `CONSISTENCY_CV_HIGH_THRESHOLD`
   - `MINIMUM_WEEKS_FOR_CONSISTENCY`
   - `CONSISTENCY_WEIGHT`

   Should these additional consistency parameters also move to JSON?
Answer: Keep all of these in the config files for now. Start with moving over the 23 mentioned parameters then we will move over more later as a future improvement.


4. **Injury Penalty Structure**: Currently `INJURY_PENALTIES` is a dictionary with LOW/MEDIUM/HIGH keys. The JSON has separate keys like `INJURY_PENALTIES_HIGH`, `INJURY_PENALTIES_MEDIUM`. Should we:
   - Keep the flattened JSON structure (3 separate keys)?
   - Convert to nested structure in JSON (single "INJURY_PENALTIES" object)?
Answer: Convert to the nested structure

## Simulation-Specific Questions

5. **Parameter Sets vs Parameter Runs**: The update mentions:
   - `parameter_sets/` folder: Contains files with arrays of values to test
   - `parameter_runs/` folder: Contains individual JSON configs for each combination

   Should the simulation:
   - Generate ALL combinations upfront and save them as files in parameter_runs/?
   - Generate combinations on-the-fly and save them as they're tested?
   - How should we name these generated files?
Answer: Generate the combinations upfront. Name them after the file from the parameter_sets folder that was used to create the run file then tag on an index value like {parameter_set_name}_0.json, {parameter_set_name}_1.json...

6. **Simulation Injection Removal**: Currently the simulation uses a ParameterInjector class. Should we:
   - Completely remove the ParameterInjector class and its tests?
   - Keep it for backward compatibility but mark as deprecated?
   - Replace it with a simpler parameter combination generator?
Answer: Completely remove the ParameterInjector class. Replace it with whatever new classes would be best for code quality to meet the new objectives


7. **Existing Parameter Files**: There are existing parameter JSON files:
   - `draft_helper/simulation/parameters/old/` folder with old files
   - Should we preserve these or clean them up?
   - What should the new file structure look like?
Answer: Ignore that directory for now, just perserve them and do not bother updating or cleaning them up.

## Implementation Questions

8. **ParameterJsonManager Location**: Where should this new class live?
   - `shared_files/` (since it's used by both draft_helper and starter_helper)?
   - `shared_files/configs/` (alongside other config-related code)?
   - Each module has its own copy?
Answer: Place in shared_files

9. **Default Parameter File**: The update mentions `shared_files/parameters.json` as the default. Should we:
   - Keep the existing optimal_2025-10-05_19-46-54.json as the default?
   - Create a new "baseline_parameters.json" with conservative defaults?
   - Support multiple default profiles (aggressive, conservative, balanced)?
Answer: The shared_files/parameters.json file should be the default for when launching from the run_draft_helper.py file. The default for the simulation should be the existing optimal file for now.

10. **Validation**: The config files have extensive validation. Should ParameterJsonManager:
    - Validate all parameters on load using the existing validation utilities?
    - Only validate types (not ranges)?
    - Skip validation and trust the JSON files?
Answer: Validate all parameters

11. **Config File Cleanup**: After moving parameters to JSON, should we:
    - Remove the parameter constants from config files entirely?
    - Leave them as commented-out documentation?
    - Keep them with default values that get overridden by JSON?
Answer: Remove the parameter constants entirely

## Testing Questions

12. **Test Coverage**: Should we:
    - Create new unit tests specifically for ParameterJsonManager?
    - Update existing tests that mock config parameters to use JSON instead?
    - Test all parameter combinations to ensure none are missed?
Answer: Yes create brand new unit tests for any new files or functions you make. Be as thourough as possible

13. **Integration Testing**: The interactive integration tests currently don't test parameter variations. Should we:
    - Add tests that load different parameter files?
    - Keep the existing tests as-is since they test functionality, not parameters?
Answer: Yes add tests to test different files. Set up dummy files that are unlikely to be changed for those tests.

## Backward Compatibility

14. **Optional JSON Parameter**: Should the system:
    - Require a JSON file path (fail if not provided)?
    - Fall back to config file values if no JSON provided?
    - Support a hybrid mode (some from JSON, some from config)?
   Answer: Require a JSON file path, no fallbacks

15. **Simulation Results**: Existing simulation results reference parameter values. Should we:
    - Update result files to include the parameter JSON filename?
    - Keep the existing result format?
    - Add a migration script for old results?
Answer: Update the results to include the parameter json filename. No need for a migration script.

## User Experience

16. **Error Handling**: If the JSON file is missing or malformed, should we:
    - Display a clear error message and exit?
    - Fall back to default values?
    - Prompt the user to create/fix the JSON file?
Answer: Display an error message and exit

17. **Parameter Documentation**: Should we:
    - Create a README in the parameters folder explaining each parameter?
    - Include parameter descriptions in the JSON files themselves?
    - Keep documentation only in CLAUDE.md?
Answer: Create a README in the parameters folder

## Answer Format
Please answer each question with the number and your response. If any questions need further discussion, let me know!
