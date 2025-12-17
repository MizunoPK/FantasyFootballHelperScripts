# Fix ConfigGenerator Horizon Behavior

## Objective

Refactor ConfigGenerator to support horizon-based configuration management with proper 6-file structure (league_config.json + draft_config.json + 4 week configs). Enable win-rate simulation to optimize shared parameters while accuracy simulation performs tournament optimization across all 5 horizons with independent horizon-specific parameters.

---

## High-Level Requirements

### 1. File Structure (6 Files)

**Complete Config Folder Structure:**
- `league_config.json` - Base parameters shared by all horizons (non-week-specific)
- `draft_config.json` - Week-specific parameters for draft/season-long (ROS horizon) **[NEW]**
- `week1-5.json` - Week-specific parameters for weeks 1-5
- `week6-9.json` - Week-specific parameters for weeks 6-9
- `week10-13.json` - Week-specific parameters for weeks 10-13
- `week14-17.json` - Week-specific parameters for weeks 14-17

**Horizon Composition:**
Each horizon = league_config.json (base) + horizon-specific file (week params)
- ROS: league_config.json + draft_config.json
- 1-5: league_config.json + week1-5.json
- 6-9: league_config.json + week6-9.json
- 10-13: league_config.json + week10-13.json
- 14-17: league_config.json + week14-17.json

### 2. Core Behavior Change

**Current (Incorrect):**
- ConfigGenerator.load_baseline_from_folder() merges all files into single unified config
- Uses week1-5.json values for week-specific parameters arbitrarily
- All test configs start from this same merged baseline
- Only 5 files supported (no draft_config.json)

**New (Correct):**
- Load league_config.json + 5 horizon files separately
- Merge each horizon's files (league + specific) into 5 separate baseline configs
- When generating test values for a parameter, create 5 arrays (one per horizon)
- Each array: [baseline_value, random_1, random_2, ..., random_N]
- Provide configs on demand: "Give me config for horizon X, test index Y, parameter Z"

### 3. Simulation Responsibilities

**Win-Rate Simulation:**
- Optimizes ONLY league_config.json parameters (shared/base params)
- Does NOT optimize horizon-specific parameters (draft_config.json, week*.json stay fixed)
- PARAMETER_ORDER contains only league_config.json params
- Loads all 6 files, but only varies shared parameters during optimization
- Uses draft_config.json when simulating drafts (not for optimization)
- Performance: Still tests ~20 configs per parameter (not 5x increase)

**Accuracy Simulation:**
- Optimizes ALL parameters (league_config.json AND horizon-specific params)
- PARAMETER_ORDER contains both base and week-specific params
- Tests configs across all 5 horizons (tournament optimization)
- Performance: 5 horizons × 20 test values = 100 configs per parameter (5x increase)
- Each config evaluated across all 5 horizons for MAE calculation

### 4. Deprecate NUM_PARAMETERS_TO_TEST

- Remove support for testing multiple parameters simultaneously
- ConfigGenerator will only handle ONE parameter at a time
- Simpler implementation and clearer semantics
- Affects both win-rate and accuracy simulations

---

## Resolved Implementation Details

> **Status:** All 40 checklist questions resolved (100%) on 2025-12-16

### File Loading & Structure (Q1-Q4)

**Q1: How to load 6-file structure?**
- Load league_config.json once at init
- Merge with each of 5 horizon files separately
- Store as 5 separate baseline configs in memory
- Performance: Avoids repeated file reads, faster access

**Q2: How to merge configs?**
- Simple dict merge: `{**league_config['parameters'], **horizon_config['parameters']}`
- Precedence: Horizon file wins if same param in both (allows override)
- Nested structures (INJURY_PENALTIES, DRAFT_ORDER_BONUSES) stay in league_config.json only

**Q3: File validation?**
- Fail immediately with clear error if ANY of 6 files missing
- Required files: league_config.json, draft_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json
- No backward compatibility - clean break from 5-file structure

**Q4: Metadata handling?**
- Preserve metadata from horizon-specific file (config_name, description)
- Reasoning: Horizon file defines purpose, so its metadata is more relevant

### ConfigGenerator Interface Design (Q5-Q13, Q22-Q23, Q40)

**Q5: Data storage approach?**
- Store 6 loaded files + 5 merged horizon configs in memory (Option A)
- Faster access, no repeated file I/O

**Q6-Q8: Method signatures?**
```python
def generate_horizon_test_values(param_name: str) -> Dict[str, List[float]]:
    """
    Generate test values for parameter optimization.

    Returns different structures based on parameter type:
    - Shared params (BASE_CONFIG_PARAMS): {'shared': [N values]}
      → N configs tested across all 5 horizons
    - Horizon params (WEEK_SPECIFIC_PARAMS): {'ros': [N], '1-5': [N], ...}
      → 5×N configs tested (tournament model)
    """

def get_config_for_horizon(horizon: str, param_name: str, test_index: int) -> dict:
    """Get complete config with test value applied at test_index"""

def update_baseline_for_horizon(horizon: str, new_config: dict):
    """Update baseline config for horizon after finding optimal value"""
```

**Q7: Parameter type detection?**
- Use existing `is_base_config_param()` and `is_week_specific_param()` methods
- Auto-detect internally - simulations don't specify mode

**Q9: Update methods?**
- Unified `update_baseline_for_horizon(horizon, new_config)` for both types
- For shared params: Update league_config portion in all 5 horizon baselines
- For horizon params: Update only specified horizon's baseline

**Q10-Q11: Horizon naming & file mapping?**
```python
# In ConfigPerformance.py
HORIZONS = ['ros', '1-5', '6-9', '10-13', '14-17']

HORIZON_FILES = {
    'ros': 'draft_config.json',
    '1-5': 'week1-5.json',
    '6-9': 'week6-9.json',
    '10-13': 'week10-13.json',
    '14-17': 'week14-17.json'
}
```

**Q12-Q13: Data structures?**
```python
# Baseline configs (5 merged horizons)
baseline_configs = {
    'ros': {'config_name': '...', 'description': '...', 'parameters': {...}},
    '1-5': {'config_name': '...', 'description': '...', 'parameters': {...}},
    # ... etc
}

# Test values (unified structure)
# For shared params:
test_values = {'shared': [baseline, test1, test2, ...]}

# For horizon params:
test_values = {
    'ros': [baseline_ros, test1, ...],
    '1-5': [baseline_1_5, test1, ...],
    # ... etc
}
```

**Q22-Q23, Q40: Unified interface?**
- **YES** - Both simulations use exactly the same interface
- Auto-detection based on param type (no mode parameter)
- ConfigGenerator handles complexity internally

### Win-Rate Simulation Integration (Q14-Q17)

**Q14: Parameter selection?**
- PARAMETER_ORDER in SimulationManager pre-filtered to BASE_CONFIG_PARAMS only
- Clearer intent, simpler (no filtering logic)

**Q15: Shared param optimization?**
- Generate: 1 set of test values with 'shared' key
- Test: N configs total (NOT 5×N)
- Update: Only league_config.json updated with optimal value

**Q16: draft_config.json usage?**
- ConfigManager initialized with draft_config.json params for draft phase
- Flow: ConfigManager → DraftHelperTeam → AddToRosterModeManager → PlayerManager.score_player()
- No changes needed to AddToRosterModeManager/DraftHelperTeam (already receive ConfigManager)

**Q17: Save all 6 files?**
- Yes - save NEW files (not copy) for all 6 configs
- Optimized league_config.json + unchanged (but freshly saved) horizon files
- Maintains consistent 6-file structure

### Accuracy Simulation Integration (Q18-Q21)

**Q18: Parameter selection?**
- PARAMETER_ORDER in run_accuracy_simulation.py = WEEK_SPECIFIC_PARAMS only
- Top-level runner script (not AccuracySimulationManager)

**Q19: Shared param handling?**
- N/A - Accuracy does NOT optimize shared params
- Win-rate handles all BASE_CONFIG_PARAMS optimization

**Q20: Horizon param optimization?**
- Tournament model - 5 independent optimizations
- Generate: 5 independent test value sets (one per horizon)
- Test: 5 horizons × N test values = 5×N configs total
- Each horizon finds its own optimal value independently

**Q21: Save all 6 files?**
- Yes - league_config.json (copied from input) + 5 optimized horizon files
- Shared save logic for both simulations

### ResultsManager Updates (Q24-Q26)

**Q24: Changes needed?**
1. Update `required_files` list: add 'draft_config.json'
2. Update `save_optimal_configs_folder()` to save all 6 files
3. Update `load_from_folder()` to load all 6 files
4. Extend `week_range_files` mapping to include `'ros': 'draft_config.json'`

**Q25: Results tracking?**
- Track by horizon for both shared and horizon params (existing approach)
- Even with same shared param value, each horizon performs differently
- No changes needed - current tracking works for both param types

**Q26: Intermediate folders?**
- Same 6-file structure as optimal folders
- ConfigGenerator can load from intermediate folders to resume optimization

### Error Handling (Q27-Q29, Q32)

**Q27-Q28: Missing files/params?**
- Fail immediately with clear error (fail fast approach)
- No defaults - configs should be complete and explicit
- Error messages indicate which file/param is missing

**Q29: Merge conflicts?**
- Horizon file wins on conflicts (from Q2 resolution)
- Provides flexibility for edge cases

**Q32: Backward compatibility?**
- Clean break - no backward compatibility testing
- Old 5-file folders will fail with clear error directing to 6-file structure
- Correctness fix justifies breaking change

### Testing Approach (Q30-Q31)

**Q30: File loading tests?**
- Use pytest tmp_path fixture to create temporary test folders
- Test scenarios:
  1. Happy path: All 6 files present and valid
  2. Missing file: Verify error raised
  3. Merge behavior: Verify horizon file overrides league_config
  4. Parameter extraction: Verify correct params loaded per horizon

**Q31: Interface behavior tests?**
- Test shared param (e.g., ADP_SCORING): Verify returns `{'shared': [...]}`
- Test horizon param (e.g., NORMALIZATION_MAX_SCALE): Verify returns `{'ros': [...], '1-5': [...], ...}`
- Verify 5 independent arrays with different baseline values

### Performance & Optimization (Q33-Q35)

**Q33: Deep copy vs reference?**
- Return deep copies when providing configs to simulation
- Prevents accidental baseline mutation
- Trade-off: Slight performance overhead for safety

**Q34: Pre-generate vs on-demand?**
- Pre-generate test values when `generate_horizon_test_values()` called
- Store in memory for determinism and performance
- Can inspect/log test values before simulation

**Q35: Expected config counts?**
- **Win-rate (shared params):** N configs (example: `--test-values 20` → 20 configs)
- **Accuracy (horizon params):** 5×N configs (example: `--test-values 20` → 100 configs)
- Document in code comments and ResultsManager logging

### Deprecation & Migration (Q36-Q38)

**Q36: num_parameters_to_test parameter?**
- Remove entirely (clean break)
- Signature: `__init__(baseline_folder: str, num_test_values: int)`
- Migration: Update both SimulationManager and AccuracySimulationManager

**Q37: generate_iterative_combinations() method?**
- Remove entirely (dead code with single-parameter optimization)
- Only keep new `generate_horizon_test_values()` interface

**Q38: Migration from 5-file to 6-file?**
- Require re-run (no migration script)
- Old configs generated with incorrect algorithm (not trustworthy)
- Document why re-run is necessary (bug fix, correctness)
- Provide migration guidance in specs and README

### Implementation Strategy (Q39)

**Q39: Incremental vs atomic?**
- Atomic change - all files in one commit
- Update 4 core files simultaneously:
  1. simulation/shared/ConfigGenerator.py
  2. simulation/shared/ResultsManager.py
  3. simulation/win_rate/SimulationManager.py
  4. simulation/accuracy/AccuracySimulationManager.py
- Commit only when ALL tests pass (100% pass rate required)

---

## Dependency Map

### Module Dependencies

```
┌──────────────────────────────────────────────────────────────────────┐
│ SIMULATION ENTRY POINTS                                              │
├──────────────────────────────────────────────────────────────────────┤
│ run_win_rate_simulation.py          run_accuracy_simulation.py       │
│          │                                    │                       │
│          ▼                                    ▼                       │
│   SimulationManager                  AccuracySimulationManager        │
│          │                                    │                       │
│          └────────────────┬───────────────────┘                       │
│                           ▼                                           │
│                   ConfigGenerator (SHARED - needs refactor)           │
│                           │                                           │
│                           ├──► BASE_CONFIG_PARAMS (ResultsManager)   │
│                           ├──► WEEK_SPECIFIC_PARAMS (ResultsManager) │
│                           └──► PARAM_DEFINITIONS (internal)           │
│                                                                       │
│                   ResultsManager (SHARED - needs 6-file support)      │
│                           │                                           │
│                           ├──► ConfigPerformance                      │
│                           └──► WEEK_RANGES constant                   │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Flow (6-File Structure)

```
INPUT: Config Folder
├── league_config.json (shared params: ADP, DRAFT, INJURY, etc.)
├── draft_config.json (week params for ROS/draft)
├── week1-5.json (week params for early season)
├── week6-9.json (week params for mid-early season)
├── week10-13.json (week params for mid-late season)
└── week14-17.json (week params for late season)
   ▼
ConfigGenerator.__init__(folder_path)
   │
   ├──► Load league_config.json
   ├──► Load draft_config.json
   ├──► Load week1-5.json
   ├──► Load week6-9.json
   ├──► Load week10-13.json
   └──► Load week14-17.json
   ▼
Merge into 5 horizon configs:
   │
   ├──► baseline_configs['ros'] = league + draft
   ├──► baseline_configs['1-5'] = league + week1-5
   ├──► baseline_configs['6-9'] = league + week6-9
   ├──► baseline_configs['10-13'] = league + week10-13
   └──► baseline_configs['14-17'] = league + week14-17
   ▼
Simulation calls:
   ├──► generate_horizon_test_values(param_name)
   │      └──► Creates test_values dict (shared: 1 array, horizon: 5 arrays)
   │
   ├──► get_config_for_horizon(horizon, param_name, test_idx)
   │      └──► Returns complete config with test value applied
   │
   └──► update_baseline_for_horizon(horizon, new_config)
          └──► Updates baseline for next parameter
   ▼
OUTPUT: Optimal/Intermediate Folder
├── league_config.json (optimized shared params)
├── draft_config.json (optimized ROS week params)
├── week1-5.json (optimized early season params)
├── week6-9.json (optimized mid-early params)
├── week10-13.json (optimized mid-late params)
└── week14-17.json (optimized late season params)
```

### Key Integration Points

1. **ConfigGenerator ← ResultsManager**: Uses BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS constants
2. **SimulationManager → ConfigGenerator**: Calls new horizon-based interface
3. **AccuracySimulationManager → ConfigGenerator**: Same interface, different parameter list
4. **ResultsManager**: Needs to save/load 6 files instead of 5
5. **ConfigPerformance**: WEEK_RANGES constant used for horizon naming

---

## Vagueness Audit

**Audit Result:** Notes are clear and specific. No vague phrases requiring clarification.

- ✓ File structure explicitly defined (6 files with names)
- ✓ Horizon composition clearly specified (league + horizon-specific)
- ✓ Simulation responsibilities explicitly separated (win-rate vs accuracy)
- ✓ Expected behavior documented with concrete examples

## Assumptions

| Assumption | Basis | Risk if Wrong | Mitigation |
|------------|-------|---------------|------------|
| league_config.json + horizon file merge is simple dict merge | Current load_baseline_from_folder() uses simple merge | Complex nested structures might conflict | Document merge precedence rules (horizon file wins for week params) |
| draft_config.json has same structure as week files | User confirmed this | If structure differs, loading will fail | Validate structure on load, clear error message |
| Win-rate only needs to optimize shared params | User specification | If horizon params also need optimization, performance impact | Document this decision, can extend later if needed |
| Accuracy needs to optimize all params (shared + horizon) | User specification | If shared params should have single optimal value across all horizons, tournament model doesn't apply | Q19/Q22 address this - needs user decision |
| Existing BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS constants are complete | Verified in ResultsManager.py | If new params don't fit either category, classification breaks | Add validation in ConfigGenerator to check param is in one of the lists |
| ResultsManager can be updated to support 6 files | Currently supports 5 files with hard-coded list | If deeply coupled to 5-file assumption, refactor harder | Check all file count assumptions in ResultsManager |
| WEEK_RANGES constant can be reused for horizon naming | Exists in ConfigPerformance.py | If format incompatible ('1-5' vs 'week_1_5'), string manipulation needed | Use existing format to avoid changes |
| Simulations don't need both shared and horizon optimization simultaneously | User specification | If future needs this, interface design changes | Design flexible interface now (Q22, Q23) |
