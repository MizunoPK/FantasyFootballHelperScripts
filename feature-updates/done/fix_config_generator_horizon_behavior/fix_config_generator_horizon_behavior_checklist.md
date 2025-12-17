# Fix ConfigGenerator Horizon Behavior - Requirements Checklist

> **Note:** Items marked [x] are resolved. Items marked [ ] need investigation or user decision.

---

## ITERATION 1: Core Questions (File Structure, Architecture, Interface)

### File Structure & Loading Questions

- [x] **Q1**: How should ConfigGenerator load the 6-file structure?
  - **RESOLVED:** Load league_config.json once at init, then merge with each of 5 horizon files
  - **Performance:** Avoids repeated file reads, faster access
  - **Date:** 2025-12-16

- [x] **Q2**: How to merge league_config.json + horizon-specific file?
  - **RESOLVED:** Simple dict merge: `{**league_config['parameters'], **horizon_config['parameters']}`
  - **Precedence:** Horizon file wins if same param exists in both (allows override)
  - **Nested structures:** INJURY_PENALTIES, DRAFT_ORDER_BONUSES stay in league_config.json only
  - **Date:** 2025-12-16

- [x] **Q3**: Should ConfigGenerator validate that all 6 files exist?
  - **RESOLVED:** Fail immediately with clear error if ANY of 6 files missing
  - **Required files:** league_config.json, draft_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json
  - **No backward compatibility:** Clean break
  - **Date:** 2025-12-16

- [x] **Q4**: What metadata should merged horizon configs have?
  - **RESOLVED:** Preserve metadata from horizon-specific file (config_name, description)
  - **Reasoning:** Horizon file defines purpose, so its metadata is more relevant
  - **Date:** 2025-12-16

### ConfigGenerator Interface Questions

- [x] **Q5**: Should ConfigGenerator store baseline configs or baseline folder path?
  - Option A: Store 6 loaded files + 5 merged horizon configs in memory
  - Option B: Store folder path, reload and merge on demand
  - **Recommendation:** Option A (load once, faster access)

- [x] **Q6**: What should be the method signature for generating test values?
  - `generate_horizon_test_values(param_name: str) -> Dict[str, List[float]]`?
  - Returns: `{'ros': [baseline, rand1, ...], '1-5': [...], ...}`
  - Should it skip horizons that don't have this parameter?

- [x] **Q7**: How does ConfigGenerator know which parameters are horizon-specific vs shared?
  - Use existing BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS constants?
  - When param is in BASE_CONFIG_PARAMS, only generate 1 set of test values (not 5)?
  - When param is in WEEK_SPECIFIC_PARAMS, generate 5 independent sets?

- [x] **Q8**: What should be the signature for getting a specific config?
  - `get_config_for_horizon(horizon: str, param_name: str, test_index: int) -> dict`?
  - For shared params: All horizons get same test value at given index?
  - For horizon params: Each horizon gets independent test value at given index?

- [x] **Q9**: How should ConfigGenerator be updated after parameter optimization?
  - For shared params: `update_shared_baseline(new_league_config: dict)`?
  - For horizon params: `update_baseline_for_horizon(horizon: str, new_horizon_config: dict)`?
  - Two different update methods based on parameter type?

### Horizon Naming & Constants

- [x] **Q10**: What horizon names should we use?
  - **RESOLVED:** Use WEEK_RANGES format with 'ros' added: `['ros', '1-5', '6-9', '10-13', '14-17']`
  - **Constant:** Create `HORIZONS = ['ros', '1-5', '6-9', '10-13', '14-17']`
  - **Location:** Add to ConfigPerformance.py (where WEEK_RANGES lives)
  - **Note:** Unify naming - accuracy sim uses 'week_1_5' (underscores), we'll use hyphens
  - **Code reference:** simulation/shared/ConfigPerformance.py:23
  - **Date:** 2025-12-16

- [x] **Q11**: How to map horizon names to filenames?
  - **RESOLVED:** Explicit constant (not programmatic):
    ```python
    HORIZON_FILES = {
        'ros': 'draft_config.json',
        '1-5': 'week1-5.json',
        '6-9': 'week6-9.json',
        '10-13': 'week10-13.json',
        '14-17': 'week14-17.json'
    }
    ```
  - **Location:** ConfigPerformance.py alongside HORIZONS
  - **Reasoning:** Clearer than derivation, matches existing week_range_files pattern
  - **Code reference:** simulation/shared/ResultsManager.py:426-431 (existing pattern)
  - **Date:** 2025-12-16

### Data Structures

- [x] **Q12**: What should horizon baseline configs structure be?
  - **RESOLVED:** Store 5 merged configs with full structure:
    ```python
    {
        'ros': {'config_name': '...', 'description': '...', 'parameters': {...}},
        '1-5': {'config_name': '...', 'description': '...', 'parameters': {...}},
        # ... etc
    }
    ```
  - **Include:** Full metadata (config_name, description, parameters) to match existing format
  - **Date:** 2025-12-16

- [x] **Q13**: What should horizon test values structure be?
  - **RESOLVED:** Unified dict structure for consistency:
  - **Shared params:** `{'shared': [baseline, test1, test2, ...]}`
  - **Horizon params:** `{'ros': [...], '1-5': [...], '6-9': [...], '10-13': [...], '14-17': [...]}`
  - **Benefit:** Consistent structure, check key to determine param type
  - **Date:** 2025-12-16

## ITERATION 2: Simulation Integration (Win-Rate vs Accuracy)

### Win-Rate Simulation Questions

- [x] **Q14**: How does win-rate sim identify which params to optimize?
  - **RESOLVED:** Option A - PARAMETER_ORDER in SimulationManager pre-filtered to only BASE_CONFIG_PARAMS
  - **Reasoning:** Clearer intent, simpler (no filtering logic), matches pattern (accuracy has different list)
  - **Implementation:** Win-rate PARAMETER_ORDER = list of BASE_CONFIG_PARAMS only
  - **Date:** 2025-12-16

- [x] **Q15**: When win-rate optimizes a shared param, what happens?
  - **RESOLVED:**
    - **Generate:** 1 set of test values with 'shared' key: `{'shared': [baseline, test1, ...]}`
    - **Test:** N configs total (NOT 5×N) - each tested across all 5 horizons
    - **Update:** Only league_config.json updated with optimal value (horizon files unchanged)
  - **Example:** 20 test values = 20 configs tested (not 100)
  - **Date:** 2025-12-16

- [x] **Q16**: How does win-rate use draft_config.json during simulation?
  - **RESOLVED:** ConfigManager initialized with draft_config.json params for draft phase
  - **Flow:** ConfigManager → DraftHelperTeam → AddToRosterModeManager → PlayerManager.score_player()
  - **Implementation:**
    - ConfigManager loads horizon-specific config (league + draft for draft phase)
    - SimulatedLeague uses ConfigManager with draft_config.json during run_draft()
    - No changes needed to AddToRosterModeManager/DraftHelperTeam (already receive ConfigManager)
  - **Code references:**
    - DraftHelperTeam.py:140-144 (creates AddToRosterModeManager with config)
    - PlayerManager.py:565 (score_player uses config params)
  - **Date:** 2025-12-16

- [x] **Q17**: Should win-rate save draft_config.json in optimal/intermediate folders?
  - **RESOLVED:** Yes - save NEW files (not copy) for all 6 configs to maintain structure
  - **Approach:**
    - Save optimized league_config.json with new optimal shared params
    - Save draft_config.json with current params (unchanged but written fresh)
    - Save week*.json files with current params (unchanged but written fresh)
  - **Benefits:**
    - Consistent 6-file structure (matches accuracy sim)
    - Shared save logic for both win-rate and accuracy sims
    - Output folders usable as input for future simulations
    - No special "copy vs save" logic - always save
  - **Date:** 2025-12-16

### Accuracy Simulation Questions

- [x] **Q18**: How does accuracy sim know to optimize all params?
  - **RESOLVED:** PARAMETER_ORDER in run_accuracy_simulation.py contains ONLY WEEK_SPECIFIC_PARAMS
  - **Location:** Top-level runner script (not AccuracySimulationManager)
  - **Reasoning:**
    - Accuracy optimizes horizon-specific params only (not shared params)
    - Shared params (BASE_CONFIG_PARAMS) are optimized by win-rate sim
    - Clear separation of responsibilities
  - **Implementation:** PARAMETER_ORDER = WEEK_SPECIFIC_PARAMS in run_accuracy_simulation.py
  - **Date:** 2025-12-16

- [x] **Q19**: When accuracy optimizes a shared param, what happens?
  - **RESOLVED:** N/A - Accuracy does NOT optimize shared params
  - **Reasoning:**
    - Accuracy PARAMETER_ORDER = WEEK_SPECIFIC_PARAMS only (Q18)
    - Win-rate handles all BASE_CONFIG_PARAMS optimization
    - Accuracy never encounters shared params during optimization
  - **Impact:** Simplifies ConfigGenerator interface - only needs to handle one param type per simulation
  - **Date:** 2025-12-16

- [x] **Q20**: When accuracy optimizes a horizon param, what happens?
  - **RESOLVED:** Tournament model - 5 independent optimizations
  - **Generate:** 5 independent test value sets (one per horizon)
    - `{'ros': [baseline_ros, test1, ...], '1-5': [baseline_1_5, test1, ...], ...}`
  - **Test:** 5 horizons × N test values = 5×N configs total
    - Example: 20 test values per horizon = 100 configs evaluated
  - **Optimize:** Each horizon finds its own optimal value independently
    - ROS optimal might be 150, Week 1-5 optimal might be 180, etc.
  - **This is the core "tournament" optimization model**
  - **Date:** 2025-12-16

- [x] **Q21**: Should accuracy save all 6 files (including draft_config.json)?
  - **RESOLVED:** Yes - save all 6 files with optimized horizon-specific params
  - **Files saved:**
    - league_config.json - Copy from input (unchanged, shared params from win-rate)
    - draft_config.json - OPTIMIZED week-specific params for ROS horizon
    - week1-5.json - OPTIMIZED week-specific params for weeks 1-5
    - week6-9.json - OPTIMIZED week-specific params for weeks 6-9
    - week10-13.json - OPTIMIZED week-specific params for weeks 10-13
    - week14-17.json - OPTIMIZED week-specific params for weeks 14-17
  - **Consistency:** Matches Q17 - shared save logic for both simulations
  - **Date:** 2025-12-16

### Unified vs Split Interface

- [x] **Q22**: Should ConfigGenerator have ONE interface for both sims?
  - **RESOLVED:** ONE unified interface with auto-detection of param type
  - **Methods:** Same for both sims - `generate_horizon_test_values()`, `get_config_for_horizon()`, `update_baseline_for_horizon()`
  - **Auto-detection:** ConfigGenerator uses `is_base_config_param()` and `is_week_specific_param()` to determine behavior
  - **Behavior adapts:**
    - BASE_CONFIG_PARAMS → return `{'shared': [values]}`
    - WEEK_SPECIFIC_PARAMS → return `{'ros': [...], '1-5': [...], ...}`
  - **Benefits:** Simpler, ConfigGenerator handles complexity, same signatures for both sims
  - **Date:** 2025-12-16

- [x] **Q23**: How do simulations specify which mode to use?
  - **RESOLVED:** Auto-detection based on param type (no mode parameter)
  - **Implementation:**
    - ConfigGenerator internally calls `is_base_config_param(param_name)` or `is_week_specific_param(param_name)`
    - Simulations just call `generate_horizon_test_values(param_name)` - no mode parameter needed
    - ConfigGenerator determines behavior automatically
  - **Consistency:** Matches Q22's unified interface approach
  - **Date:** 2025-12-16

## ITERATION 3: ResultsManager, Error Handling, Testing

### ResultsManager Integration

- [x] **Q24**: Does ResultsManager need changes for 6-file structure?
  - **RESOLVED:** Yes - ResultsManager needs updates for 6-file structure
  - **Changes needed:**
    1. Update `required_files` list: add `'draft_config.json'` (currently 5 files at line 593)
    2. Update `save_optimal_configs_folder()` to save all 6 files
    3. Update `load_from_folder()` to load all 6 files
    4. Extend `week_range_files` mapping to include `'ros': 'draft_config.json'`
  - **Code reference:** ResultsManager.py:593 (required_files), 426-431 (week_range_files)
  - **Date:** 2025-12-16

- [x] **Q25**: How does ResultsManager track results for shared vs horizon params?
  - **RESOLVED:** Track by horizon for both shared and horizon params (existing approach)
  - **Reasoning:**
    - Even with same shared param value, each horizon performs differently
    - Allows selecting config with best **overall** performance across all horizons
    - Existing ResultsManager logic already handles this
  - **Example (shared param ADP_SCORING = 1.5):**
    - Week 1-5: 55% win rate
    - Week 6-9: 60% win rate
    - Overall: Aggregate across horizons for best overall
  - **No changes needed** - current tracking approach works for both param types
  - **Date:** 2025-12-16

- [x] **Q26**: What about intermediate folders?
  - **RESOLVED:** Same 6-file structure as optimal folders
  - **Structure:** Identical to optimal folders (just different optimization stage)
    - league_config.json (current best shared params)
    - draft_config.json (current best ROS horizon params)
    - week1-5.json, week6-9.json, week10-13.json, week14-17.json (current best per horizon)
  - **ConfigGenerator can load from intermediate folders** to resume optimization
  - **Enables resume capability** if simulation interrupted
  - **Date:** 2025-12-16

### Error Handling

- [x] **Q27**: What if draft_config.json is missing from baseline folder?
  - **RESOLVED:** Fail immediately with clear error (consistent with Q3)
  - **No backward compatibility** - clean break
  - **Error message:** "Missing required config files in {folder_path}: draft_config.json"
  - **Reasoning:**
    - 6-file structure mandatory for correct behavior
    - Creating default could hide configuration issues
    - Clean error helps users understand requirement
  - **Date:** 2025-12-16

- [x] **Q28**: What if parameter doesn't exist in expected file?
  - **RESOLVED:** Raise clear error (fail fast approach)
  - **Missing shared param from league_config.json:**
    - Error: "Parameter '{param_name}' not found in league_config.json"
  - **Missing horizon param from horizon file:**
    - Error: "Parameter '{param_name}' not found in {horizon_file}"
  - **No defaults** - configs should be complete and explicit
  - **Reasoning:**
    - Missing params indicate configuration issue
    - Defaults could hide problems
    - Fail fast and fix the config
  - **Date:** 2025-12-16

- [x] **Q29**: What if merge conflicts occur?
  - **RESOLVED:** Already resolved by Q2 - horizon file wins on conflicts
  - **Merge precedence:** `{**league_config['parameters'], **horizon_config['parameters']}`
  - **Horizon file overrides** - allows horizon-specific customization even for shared params if needed
  - **Intentional behavior** - provides flexibility for edge cases
  - **Reference:** Q2 resolution
  - **Date:** 2025-12-16

### Testing & Validation

- [x] **Q30**: How to test 6-file loading?
  - **RESOLVED:** Use pytest tmp_path fixture to create temporary test folders
  - **Create all 6 config files** with known test values
  - **Test scenarios:**
    1. Happy path: All 6 files present and valid
    2. Missing file: Verify error raised when any file missing
    3. Merge behavior: Verify horizon file overrides league_config
    4. Parameter extraction: Verify correct params loaded per horizon
  - **Example:**
    ```python
    @pytest.fixture
    def test_config_folder(tmp_path):
        folder = tmp_path / "test_configs"
        folder.mkdir()
        # Create all 6 files with test data
        return folder
    ```
  - **Date:** 2025-12-16

- [x] **Q31**: How to verify shared vs horizon param behavior?
  - **RESOLVED:** Test both param types with different expected outputs
  - **Test shared param (e.g., ADP_SCORING from BASE_CONFIG_PARAMS):**
    - Call `generate_horizon_test_values('ADP_SCORING')`
    - Verify returns `{'shared': [baseline, test1, test2, ...]}`
    - Verify single array, not 5 horizon arrays
  - **Test horizon param (e.g., NORMALIZATION_MAX_SCALE from WEEK_SPECIFIC_PARAMS):**
    - Call `generate_horizon_test_values('NORMALIZATION_MAX_SCALE')`
    - Verify returns `{'ros': [...], '1-5': [...], '6-9': [...], '10-13': [...], '14-17': [...]}`
    - Verify 5 independent arrays
    - Verify each starts with different baseline value (from respective horizon file)
  - **Date:** 2025-12-16

- [x] **Q32**: Should we test backward compatibility?
  - **RESOLVED:** Clean break - no backward compatibility testing
  - **Reasoning:**
    - Q3 and Q27 already resolved: Fail immediately if any files missing
    - User notes explicitly state "breaking change is acceptable"
    - Current behavior is INCORRECT (bug fix, not feature change)
    - Correctness fix justifies breaking change
  - **Implementation:**
    - Old 5-file folders (without draft_config.json) will fail with clear error
    - Error message should direct users to update to 6-file structure
    - No fallback logic or compatibility mode
    - Users must re-run simulations with new structure
  - **Error message example:**
    ```
    ConfigGeneratorError: Missing required file 'draft_config.json' in folder '/path/to/configs'
    Required files: league_config.json, draft_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json
    This is a breaking change from 5-file structure. Please update your configuration folders to include draft_config.json.
    ```
  - **Benefits:** Simpler implementation, clearer semantics, consistent with "fail fast" approach
  - **Date:** 2025-12-16

### Performance & Optimization

- [x] **Q33**: Should baseline configs be deep-copied when providing to simulation?
  - **RESOLVED:** Return deep copies (Option A - safety over performance)
  - **Reasoning:**
    - ConfigGenerator owns baseline state - simulations shouldn't mutate it
    - Prevents bugs from accidental modifications corrupting baseline
    - Each call already creates new config (applying test values), so copying anyway
    - Modest performance cost (only on config request, not test value generation)
    - Standard practice for state-owning libraries
  - **Implementation:**
    ```python
    import copy

    def get_config_for_horizon(self, horizon: str, param_name: str, test_index: int) -> dict:
        baseline = copy.deepcopy(self.baseline_configs[horizon])
        baseline['parameters'][param_name] = self.test_values[...][test_index]
        return baseline  # Already a deep copy, safe from mutation
    ```
  - **Trade-off accepted:** Slight performance overhead for safety and correctness
  - **Date:** 2025-12-16

- [x] **Q34**: Should test values be pre-generated or on-demand?
  - **RESOLVED:** Pre-generate when `generate_horizon_test_values()` called (Option A)
  - **Reasoning:**
    - Determinism: Same test values for fair comparison across horizons
    - Interface semantics: Method name "generate" implies immediate generation and storage
    - Performance: Simulations may request same config multiple times (pre-gen faster)
    - Debugging: Can log/inspect test values before simulation runs
    - Memory not a concern: ~100 values × 5 horizons = minimal overhead
    - Simplicity: No seed management needed for determinism
  - **Implementation pattern:**
    ```python
    def generate_horizon_test_values(self, param_name: str) -> Dict[str, List[float]]:
        """Generate and STORE test values for parameter"""
        if self.is_base_config_param(param_name):
            baseline = self.baseline_configs['ros']['parameters'][param_name]
            test_values = self._generate_test_values(param_name, baseline, self.num_test_values)
            self.test_values = {'shared': test_values}
        else:
            self.test_values = {}
            for horizon in HORIZONS:
                baseline = self.baseline_configs[horizon]['parameters'][param_name]
                test_values = self._generate_test_values(param_name, baseline, self.num_test_values)
                self.test_values[horizon] = test_values
        return self.test_values  # Return what we stored

    def get_config_for_horizon(self, horizon: str, param_name: str, test_index: int) -> dict:
        """Use pre-generated self.test_values"""
        # Access self.test_values that was pre-generated
    ```
  - **Trade-off accepted:** Slight memory overhead for determinism and performance
  - **Date:** 2025-12-16

- [x] **Q35**: What's the expected config count per parameter?
  - **RESOLVED:** Document both patterns clearly in specs and code
  - **Win-Rate Simulation (Shared Parameters):**
    - Optimizes: BASE_CONFIG_PARAMS (league_config.json)
    - Configs tested: N (where N = num_test_values)
    - Example: `--test-values 20` → 20 configs
    - Each config tested across all 5 horizons to find best overall shared value
  - **Accuracy Simulation (Horizon Parameters):**
    - Optimizes: WEEK_SPECIFIC_PARAMS (draft_config.json, week*.json)
    - Configs tested: 5 × N (where N = num_test_values per horizon)
    - Example: `--test-values 20` → 5 × 20 = 100 configs
    - Tournament optimization: each horizon finds its own optimal value independently
  - **Documentation locations:**
    - Add to specs.md under "Core Behavior Change" section
    - Add code comment in `generate_horizon_test_values()` method
    - Include in ResultsManager logging (config count per parameter)
  - **Code comment example:**
    ```python
    def generate_horizon_test_values(self, param_name: str) -> Dict[str, List[float]]:
        """
        Generate test values for parameter optimization.

        Returns different structures based on parameter type:
        - Shared params (BASE_CONFIG_PARAMS): {'shared': [N values]}
          → N configs tested across all 5 horizons
        - Horizon params (WEEK_SPECIFIC_PARAMS): {'ros': [N], '1-5': [N], ...}
          → 5×N configs tested (tournament model)
        """
    ```
  - **Date:** 2025-12-16

### Deprecation & Migration

- [x] **Q36**: What happens to `num_parameters_to_test` init parameter?
  - **RESOLVED:** Remove entirely (Option A - clean break)
  - **Reasoning:**
    - Already a breaking change: Both sims need updates for 6-file structure
    - Notes explicitly say "deprecate NUM_PARAMETERS_TO_TEST"
    - Simpler code: No parameter validation or error handling needed
    - Clearer API: Single parameter optimization is now the only mode
    - Both sims being updated anyway: No legacy callers to worry about
    - Consistent with Q32: Clean break, no backward compatibility
  - **Implementation:**
    ```python
    # OLD (remove):
    def __init__(self, baseline_folder: str, num_parameters_to_test: int, num_test_values: int):
        self.num_parameters_to_test = num_parameters_to_test

    # NEW (simpler):
    def __init__(self, baseline_folder: str, num_test_values: int):
        # Only num_test_values needed - always optimize one parameter at a time
        self.num_test_values = num_test_values
    ```
  - **Migration required:** Update SimulationManager and AccuracySimulationManager to remove `num_parameters_to_test` from ConfigGenerator initialization
  - **Date:** 2025-12-16

- [x] **Q37**: Should we remove `generate_iterative_combinations()` entirely?
  - **RESOLVED:** Remove entirely (Option A - consistent with Q36)
  - **Reasoning:**
    - Consistent with Q36: Removed num_parameters_to_test which drives this method
    - Dead code: Method has no valid use case with single-parameter optimization
    - Clean break accepted: Q32 and Q36 established clean break pattern
    - Simpler codebase: Less code to maintain and test
    - Both sims being updated: No risk of breaking existing callers
    - Interface clarity: New `generate_horizon_test_values()` is the only way
  - **Implementation:**
    ```python
    # REMOVE this entire method:
    def generate_iterative_combinations(self, ...):
        """OLD METHOD - supported testing multiple parameters simultaneously"""
        ...

    # ONLY keep new interface:
    def generate_horizon_test_values(self, param_name: str) -> Dict[str, List[float]]:
        """NEW METHOD - optimizes one parameter at a time"""
        ...
    ```
  - **Migration**: Both simulations use new `generate_horizon_test_values()` method (planned in Q6-Q9)
  - **Date:** 2025-12-16

- [x] **Q38**: How to handle migration from 5-file to 6-file structure?
  - **RESOLVED:** Require re-run (Option B) + Document why (Option C)
  - **Reasoning:**
    - Correctness: Old optimal configs generated with bug - not trustworthy
    - Tournament model is different: Old merged baselines, new optimizes independently
    - draft_config.json has no prior values: Can't migrate what doesn't exist
    - Clean break accepted: Consistent with Q32 decision
    - Simpler implementation: No migration script to maintain
    - Better results: Re-running finds better optimal parameters (correct algorithm)
  - **Documentation locations:**
    - Add "Migration from 5-File to 6-File Structure" section to specs.md
    - Update README.md with migration notice
    - Include in breaking changes documentation
  - **Migration guidance:**
    ```markdown
    ## Migration from 5-File to 6-File Structure

    **IMPORTANT**: This is a breaking change that fixes incorrect optimization behavior.

    ### Why Re-Run is Required
    1. Bug fix: Old optimal configs used incorrect merge behavior
    2. New file: draft_config.json didn't exist in 5-file structure
    3. Tournament model: New approach optimizes horizons independently
    4. Better results: Re-running finds more optimal parameter values

    ### Migration Steps
    1. Backup old configs (optional - reference only)
    2. Create draft_config.json from seed or template
    3. Re-run simulations with updated code
    4. Old 5-file configs will fail with clear error message
    ```
  - **No migration script**: Would perpetuate incorrect optimization results
  - **Date:** 2025-12-16

### Implementation Strategy

- [x] **Q39**: Should we update ConfigGenerator first, then simulations?
  - **RESOLVED:** Atomic change - all in one commit (Option B)
  - **Reasoning:**
    - Tests must pass: Pre-commit protocol requires 100% test pass (CLAUDE.md)
    - Breaking change: Any partial update leaves system in broken state
    - Tightly coupled: ConfigGenerator, ResultsManager, and both SimulationManagers are interdependent
    - Not that large: Only 4 core files to update
    - Clear scope: All changes serve single purpose (6-file horizon-based optimization)
    - Easier rollback: Single commit to revert if issues found
  - **Implementation plan:**
    ```
    Single commit updating:
    1. simulation/shared/ConfigGenerator.py - New 6-file horizon interface
    2. simulation/shared/ResultsManager.py - 6-file support
    3. simulation/win_rate/SimulationManager.py - Use new ConfigGenerator interface
    4. simulation/accuracy/AccuracySimulationManager.py - Use new ConfigGenerator interface
    5. All related tests updated to pass
    6. Commit only when ALL tests pass
    ```
  - **Commit message example:**
    ```
    Fix ConfigGenerator horizon behavior for 6-file structure

    - Add support for league_config.json + draft_config.json + 4 week configs
    - Implement horizon-based optimization (tournament model)
    - Remove num_parameters_to_test (one parameter at a time)
    - Update both win-rate and accuracy simulations
    - Breaking change: requires re-run of all simulations
    ```
  - **Date:** 2025-12-16

- [x] **Q40**: Should win-rate and accuracy use exactly same ConfigGenerator interface?
  - **RESOLVED:** Yes - DUPLICATE of Q22-Q23 (already resolved)
  - **Answer:** Both simulations use **exactly the same interface**
  - **Interface methods (identical for both):**
    - `generate_horizon_test_values(param_name)` - Generate test values
    - `get_config_for_horizon(horizon, param_name, test_index)` - Get specific config
    - `update_baseline_for_horizon(horizon, new_config)` - Update after optimization
  - **Auto-detection:** ConfigGenerator internally calls `is_base_config_param()` or `is_week_specific_param()` to determine behavior
  - **Return structure adapts:**
    - BASE_CONFIG_PARAMS → `{'shared': [values]}`
    - WEEK_SPECIFIC_PARAMS → `{'ros': [...], '1-5': [...], ...}`
  - **Simulations don't know the difference:** Same method calls, ConfigGenerator handles complexity
  - **Reference:** See Q22 and Q23 resolutions for full details
  - **Date:** 2025-12-16

---

## Codebase Verification Findings (Round 2 - Skeptical Re-check)

**Date:** 2025-12-16

### Finding 1: Confirmed - 5-file structure currently required
- **Files checked:** `simulation/shared/ResultsManager.py:593`, `simulation/shared/ConfigGenerator.py:317`
- **Status:** ✓ VERIFIED - Both require exactly 5 files (no draft_config.json)
- **Impact:** Requires update to 6-file structure for Q24, Q27

### Finding 2: Confirmed - Accuracy sim ALREADY saves draft_config.json
- **File:** `simulation/accuracy/AccuracyResultsManager.py:237-336`
- **Status:** ✓ VERIFIED - Accuracy has full 6-file support including draft_config.json
- **Code evidence:**
```python
file_mapping = {
    'ros': ('draft_config.json', 'ROS (Rest of Season) prediction parameters'),
    'week_1_5': ('week1-5.json', 'Weeks 1-5 prediction parameters'),
    ...
}
```
- **Impact:** Accuracy sim is AHEAD of win-rate sim on this feature! Win-rate needs to catch up.

### Finding 3: Confirmed - Win-rate sim does NOT use draft_config.json yet
- **File:** `simulation/win_rate/SimulationManager.py`
- **Status:** ✓ VERIFIED - No references to draft_config.json found
- **Impact:** Confirms user's statement that draft_config.json is "new file that had yet to be integrated into the win rate simulation"

### Finding 4: Confirmed - WEEK_RANGES constant exists
- **File:** `simulation/shared/ConfigPerformance.py:23`
- **Value:** `["1-5", "6-9", "10-13", "14-17"]`
- **Status:** ✓ VERIFIED - Can be reused for horizon naming (Q10)
- **Implication:** ROS horizon name needs to be added separately (not in WEEK_RANGES)

### Finding 5: Confirmed - Accuracy uses different WEEK_RANGES format
- **File:** `simulation/accuracy/AccuracyResultsManager.py:32-37`
- **Format:** Dict with 'week_1_5' keys (underscores, not hyphens)
```python
WEEK_RANGES = {
    'week_1_5': (1, 5),
    'week_6_9': (6, 9),
    ...
}
```
- **Status:** ✓ VERIFIED - Accuracy uses different naming convention
- **Impact:** Need to decide unified horizon naming for ConfigGenerator (Q10, Q11)

### Finding 6: Confirmed - BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS exist
- **File:** `simulation/shared/ResultsManager.py:239-265`
- **Status:** ✓ VERIFIED - Both constants exist and are imported by ConfigGenerator
- **Methods exist:** `is_base_config_param()` and `is_week_specific_param()` in ConfigGenerator
- **Impact:** Can use these for Q7 (detecting parameter type)

### Finding 7: New Discovery - ResultsManager has week_range_files mapping
- **File:** `simulation/shared/ResultsManager.py:426-431`
```python
week_range_files = {
    '1-5': 'week1-5.json',
    '6-9': 'week6-9.json',
    '10-13': 'week10-13.json',
    '14-17': 'week14-17.json'
}
```
- **Status:** ✓ USEFUL - Existing mapping for horizon files (but missing ROS/draft_config)
- **Impact:** Can extend this for Q11 (horizon to filename mapping)

### Key Insights from Round 2:

1. **Accuracy simulation is AHEAD** - Already has 6-file support with draft_config.json
2. **Win-rate simulation is BEHIND** - Still uses 5-file structure, needs draft_config.json integration
3. **Two different WEEK_RANGES formats exist** - Need to unify (hyphens vs underscores)
4. **ConfigGenerator has param detection methods** - Can use for shared vs horizon param distinction
5. **ResultsManager has file mapping** - Can extend for full horizon support

### Questions Resolvable from Codebase:

**Q10 (Horizon naming):** Use existing WEEK_RANGES format from ConfigPerformance (`'1-5'`, etc.) + add `'ros'` for draft
**Q11 (File mapping):** Extend existing week_range_files dict in ResultsManager with `'ros': 'draft_config.json'`
**Q7 (Param type detection):** Use existing `is_base_config_param()` and `is_week_specific_param()` methods
**Q24 (ResultsManager changes):** Yes - update required_files from 5 to 6, add draft_config.json

---

## Resolution Log

**Progress: 40/40 questions resolved (100%)**

🎉 **ALL QUESTIONS RESOLVED** - Ready for Phase 3 (Present findings to user)

### Session 2025-12-16 - Questions 1-13 Resolved

**Q1-Q4: File Structure & Loading**
- Q1: Load league_config once, merge with 5 horizons (performance)
- Q2: Simple dict merge, horizon file wins on conflicts
- Q3: Require all 6 files, fail immediately if missing
- Q4: Preserve horizon file metadata (more relevant)

**Q5-Q9: ConfigGenerator Interface**
- Q5: Store configs in memory (Option A) - faster access
- Q6: `generate_horizon_test_values()` returns dict with 'shared' or horizon keys
- Q7: Use existing BASE_CONFIG_PARAMS/WEEK_SPECIFIC_PARAMS constants
- Q8: `get_config_for_horizon()` returns complete config with test value applied
- Q9: Two update methods - `update_shared_baseline()` and `update_baseline_for_horizon()`

**Q10-Q11: Horizon Naming**
- Q10: HORIZONS = ['ros', '1-5', '6-9', '10-13', '14-17'] in ConfigPerformance.py
- Q11: HORIZON_FILES dict with explicit mapping in ConfigPerformance.py

**Q12-Q13: Data Structures**
- Q12: Store full config structure (config_name, description, parameters)
- Q13: Unified dict structure - 'shared' key for shared params, horizon keys for horizon params

**Q14-Q17: Win-Rate Simulation Integration**
- Q14: PARAMETER_ORDER pre-filtered to BASE_CONFIG_PARAMS only (Option A)
- Q15: Generate 1 set (shared key), test N configs (not 5×N), update league_config.json only
- Q16: ConfigManager initialized with draft_config.json params, passed through call chain to PlayerManager
- Q17: Save all 6 files (not copy) - shared save logic for both sims

**Q18-Q21: Accuracy Simulation Integration**
- Q18: PARAMETER_ORDER = WEEK_SPECIFIC_PARAMS only (in run_accuracy_simulation.py)
- Q19: N/A - Accuracy does NOT optimize shared params (win-rate handles those)
- Q20: Tournament model - generate 5 sets, test 5×N configs, each horizon finds own optimal
- Q21: Save all 6 files (league_config copied, 5 horizon files optimized)

**Q22-Q23: Unified Interface Design**
- Q22: ONE unified interface with auto-detection (simpler, same methods for both sims)
- Q23: Auto-detection based on param type (no mode parameter needed)

**Q24-Q26: ResultsManager Updates**
- Q24: Yes - update required_files to 6, save/load 6 files, extend week_range_files mapping
- Q25: Track by horizon for both param types (existing approach works, no changes needed)
- Q26: Intermediate folders same 6-file structure, ConfigGenerator can load to resume

**Q27-Q29: Error Handling**
- Q27: Missing files - fail immediately with clear error (no backward compatibility)
- Q28: Missing parameters - raise clear error (fail fast, no defaults)
- Q29: Merge conflicts - horizon file wins (resolved by Q2)

**Q30-Q31: Testing Approach**
- Q30: Use pytest tmp_path fixture, create 6 files, test happy path + error cases
- Q31: Test both shared and horizon params verify correct output structure

**Q32-Q35: Testing, Performance & Optimization**
- Q32: Clean break - no backward compatibility testing (fail on 5-file folders)
- Q33: Return deep copies for safety (prevent baseline mutation)
- Q34: Pre-generate test values (determinism, performance, debugging)
- Q35: Document config counts (win-rate: N configs, accuracy: 5×N configs)

**Q36-Q38: Deprecation & Migration**
- Q36: Remove num_parameters_to_test entirely (clean break)
- Q37: Remove generate_iterative_combinations() entirely (dead code)
- Q38: Require re-run (no migration script) + document why (bug fix correctness)

**Q39-Q40: Implementation Strategy**
- Q39: Atomic change - all 4 files in one commit (tests must pass)
- Q40: Unified interface (duplicate of Q22-Q23 - already resolved)

**ALL 40 QUESTIONS RESOLVED** ✓

---

## Resolution Log (Detailed)

*(Resolved items will be logged here with date, decision, rationale, and source)*
