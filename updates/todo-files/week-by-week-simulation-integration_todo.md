# Week-by-Week Simulation Integration TODO

## Source Documents
- **Original Specification**: `updates/done/week-by-week-config.txt` (partially implemented)
- **Integration Specification**: `updates/week-by-week-simulation-integration.txt` (this work)

## Context
The original `week-by-week-config.txt` specified that:
> "We are going to be updating the simulation such that when it is testing different config combinations, it determines which config produced the best win rate for each block of weeks."
> "When creating files based on simulation results, we'll make folders instead of single files..."

Infrastructure was built (ConfigManager, ConfigPerformance, ResultsManager methods) but NOT integrated into SimulationManager. This TODO completes that integration.

## Objective
Integrate the week-by-week config system with the simulation optimization system so that:
1. Simulations track per-week-range performance throughout optimization
2. Intermediate saves are folders with 4 config files
3. Final output is a folder with 4 config files
4. Iterative mode can resume from folder-based checkpoints
5. Different optimal values are tracked per week range for week-specific params

## Progress Tracking
**Status**: ✅ Planning Complete - Ready for Implementation
**Last Updated**: 2025-12-02
**Current Phase**: All 16 verification iterations complete

## User Answers (Integrated)
| # | Question | Answer | Impact |
|---|----------|--------|--------|
| Q1 | Full optimization mode? | **B) Only iterative** | Remove Task 3.7, no changes to run_full_optimization() |
| Q2 | Baseline loading compatibility? | **A) Folder only** | ConfigGenerator only accepts folder input |
| Q3 | Old intermediate files? | **C) Error and stop** | Add validation to raise error if .json files found |
| Q4 | Intermediate metrics? | **A) Full metrics** | Include per-range win rates in intermediate folders |
| Q5 | Auto-update target? | **A) Update folder** | Update data/configs/ folder, not legacy file |

## Already Implemented (Infrastructure)
The following was built in the previous update but NOT integrated:

| Component | File | Line | Status |
|-----------|------|------|--------|
| `BASE_CONFIG_PARAMS` | ResultsManager.py | 237 | Exists |
| `WEEK_SPECIFIC_PARAMS` | ResultsManager.py | 254 | Exists |
| `_extract_base_params()` | ResultsManager.py | 265 | Exists |
| `_extract_week_params()` | ResultsManager.py | 288 | Exists |
| `save_optimal_configs_folder()` | ResultsManager.py | 364 | Exists but NOT CALLED |
| `record_week_results()` | ResultsManager.py | 82 | Exists but NOT CALLED |
| `get_best_config_for_range()` | ResultsManager.py | 121 | Exists but NOT CALLED |
| `get_best_configs_per_range()` | ResultsManager.py | 159 | Exists but NOT CALLED |
| `run_simulations_for_config_with_weeks()` | ParallelLeagueRunner.py | 253 | Exists but NOT CALLED |
| Per-week tracking | ConfigPerformance.py | - | Exists |

## Still Missing (Not Implemented)
| Component | File | Purpose |
|-----------|------|---------|
| `is_base_param()` | ConfigGenerator.py | Classify params for optimization logic |
| `is_week_specific_param()` | ConfigGenerator.py | Classify params for optimization logic |
| `load_baseline_from_folder()` | ConfigGenerator.py | Load from folder structure |
| `save_intermediate_folder()` | ResultsManager.py | Save intermediate as folder |
| `load_configs_from_folder()` | ResultsManager.py | Load for resume |
| Per-week tracking in iterative mode | SimulationManager.py | Use existing infrastructure |
| Folder-based intermediate saves | SimulationManager.py | Use folders not files |
| Folder-based resume detection | SimulationManager.py | Detect folders not files |

---

## Phase 1: ConfigGenerator Updates
**File**: `simulation/ConfigGenerator.py`

### Task 1.1: Add Parameter Classification
- [ ] Import `BASE_CONFIG_PARAMS` and `WEEK_SPECIFIC_PARAMS` from ResultsManager
- [ ] Add `PARAM_TO_SECTION_MAP` constant mapping PARAMETER_ORDER names to config sections:
  ```python
  PARAM_TO_SECTION_MAP = {
      'NORMALIZATION_MAX_SCALE': 'NORMALIZATION_MAX_SCALE',  # Direct (BASE)
      'SAME_POS_BYE_WEIGHT': 'SAME_POS_BYE_WEIGHT',          # Direct (BASE)
      'DIFF_POS_BYE_WEIGHT': 'DIFF_POS_BYE_WEIGHT',          # Direct (BASE)
      'PRIMARY_BONUS': 'DRAFT_ORDER_BONUSES',                # Nested (BASE)
      'SECONDARY_BONUS': 'DRAFT_ORDER_BONUSES',              # Nested (BASE)
      'DRAFT_ORDER_FILE': 'DRAFT_ORDER_FILE',                # Direct (BASE)
      'ADP_SCORING_WEIGHT': 'ADP_SCORING',                   # Nested (BASE)
      'ADP_SCORING_STEPS': 'ADP_SCORING',                    # Nested (BASE)
      'PLAYER_RATING_SCORING_WEIGHT': 'PLAYER_RATING_SCORING',   # WEEK-SPECIFIC
      'TEAM_QUALITY_SCORING_WEIGHT': 'TEAM_QUALITY_SCORING',     # WEEK-SPECIFIC
      'TEAM_QUALITY_MIN_WEEKS': 'TEAM_QUALITY_SCORING',          # WEEK-SPECIFIC
      # ... etc for all PARAMETER_ORDER entries
  }
  ```
- [ ] Add method `is_base_param(param_name: str) -> bool`:
  - Maps param_name to section via PARAM_TO_SECTION_MAP
  - Returns True if section in BASE_CONFIG_PARAMS
- [ ] Add method `is_week_specific_param(param_name: str) -> bool`:
  - Maps param_name to section via PARAM_TO_SECTION_MAP
  - Returns True if section in WEEK_SPECIFIC_PARAMS
- [ ] Add unit tests for parameter classification

### Task 1.2: Add Folder Loading (Answer Q2: Folder Only)
- [ ] Add method `load_baseline_from_folder(folder_path: Path) -> dict`
  - Loads `league_config.json` from folder
  - Loads all week-specific files (`week1-5.json`, `week6-11.json`, `week12-17.json`)
  - Merges into unified config dict for optimization
  - Raises `ValueError` if folder doesn't exist or missing required files
- [ ] Add unit tests for folder loading

### Task 1.3: Update `__init__` to Require Folder (Answer Q2: No Backward Compatibility)
- [ ] Validate that `baseline_config_path` is a folder (not a file)
- [ ] Raise `ValueError` if a single .json file is passed instead of folder
- [ ] Call `load_baseline_from_folder()` for all cases
- [ ] **NO backward compatibility** with single-file baselines (per user answer)
- [ ] Add unit tests for folder requirement and error on file input

### Task 1.4: Run Tests and Validate Phase 1
- [ ] Run `python tests/run_all_tests.py`
- [ ] Verify all ConfigGenerator tests pass
- [ ] Manual test: Load from folder structure

---

## Phase 2: ResultsManager Updates
**File**: `simulation/ResultsManager.py`

### Task 2.1: Add `save_intermediate_folder()` Method (Answer Q4: Full Metrics)
- [ ] Create method similar to `save_optimal_configs_folder()` but with custom naming
- [ ] Accept `param_index`, `param_name`, `base_config`, and `week_configs` dict
- [ ] Return folder path
- [ ] Format: `intermediate_{index:02d}_{param_name}/`
- [ ] Include full `performance_metrics` in each file:
  - `config_id`, `overall_win_rate`, `total_wins`, `total_losses`
  - For week files: `win_rate_for_range`, `week_range`
  - Timestamp of intermediate save
- [ ] Add unit tests

### Task 2.2: Add `load_configs_from_folder()` Method
- [ ] Load all 4 files from a folder
- [ ] Return tuple: `(base_config: dict, week_configs: Dict[str, dict])`
- [ ] Handle missing files gracefully with error messages
- [ ] Add unit tests

### Task 2.3: Run Tests and Validate Phase 2
- [ ] Run `python tests/run_all_tests.py`
- [ ] Verify all ResultsManager tests pass

---

## Phase 3: SimulationManager Updates
**File**: `simulation/SimulationManager.py`

### Task 3.1: Update Simulation Execution
- [ ] Change from `run_simulations_for_config()` to `run_simulations_for_config_with_weeks()`
- [ ] Change from `record_result()` to `record_week_results()`
- [ ] Verify data flow from ParallelLeagueRunner → ResultsManager

### Task 3.2: Track Multiple Optimal Configs
- [ ] Replace single `current_optimal_config` with:
  - `current_base_config` (for BASE params)
  - `current_week_configs = {"1-5": {}, "6-11": {}, "12-17": {}}`
- [ ] Initialize from baseline (folder or single file)
- [ ] Update after each parameter optimization

### Task 3.3: Update Optimization Logic
- [ ] For BASE params:
  - Find overall best using `get_best_config()`
  - Update `current_base_config` with best value
- [ ] For WEEK-SPECIFIC params:
  - Find best per range using `get_best_config_for_range()`
  - Update `current_week_configs["1-5"]`, `["6-11"]`, `["12-17"]` independently
- [ ] Use ConfigGenerator's `is_base_param()` to determine which path

### Task 3.4: Update Intermediate Saves
- [ ] Replace single file saves with folder saves
- [ ] Use `ResultsManager.save_intermediate_folder()`
- [ ] Format: `intermediate_{index:02d}_{param_name}/`

### Task 3.5: Update Resume Detection (Answer Q3: Error on Old Files)
- [ ] Add check for old `intermediate_*.json` files at start of `_detect_resume_state()`
- [ ] If old .json files found: Raise `ValueError` with message to manually delete old files
- [ ] Look for `intermediate_*/` folders instead of `intermediate_*.json` files
- [ ] Find highest numbered folder
- [ ] Load from folder using `ResultsManager.load_configs_from_folder()`
- [ ] Reconstruct `current_base_config` and `current_week_configs`

### Task 3.6: Update Final Save and Auto-Update (Answer Q5: Update Folder)
- [ ] Use `save_optimal_configs_folder()` instead of `save_optimal_config()`
- [ ] Output format: `optimal_iterative_{timestamp}/`
- [ ] Update `auto_update_league_config` logic:
  - Target: `data/configs/` folder (NOT `data/league_config.json`)
  - Copy optimal league_config.json to `data/configs/league_config.json`
  - Copy optimal week1-5.json to `data/configs/week1-5.json`
  - Copy optimal week6-11.json to `data/configs/week6-11.json`
  - Copy optimal week12-17.json to `data/configs/week12-17.json`

### ~~Task 3.7: Update Full Optimization Mode~~ (REMOVED per Answer Q1)
**Note**: User confirmed full optimization mode will be removed in the future.
No changes needed to `run_full_optimization()`. Only iterative mode gets per-week tracking.

### Task 3.8: Run Tests and Validate Phase 3
- [ ] Run `python tests/run_all_tests.py`
- [ ] Verify all SimulationManager tests pass
- [ ] Manual test: Run iterative optimization with new tracking

---

## Phase 4: Testing
**Files**: `tests/simulation/test_*.py`

### Task 4.1: ConfigGenerator Tests
- [ ] `test_load_baseline_from_folder`
- [ ] `test_load_baseline_from_folder_missing_files`
- [ ] `test_is_base_param_returns_true_for_base_params`
- [ ] `test_is_base_param_returns_false_for_week_params`
- [ ] `test_is_week_specific_param_returns_true_for_week_params`
- [ ] `test_is_week_specific_param_returns_false_for_base_params`
- [ ] `test_init_with_folder_path`
- [ ] `test_init_with_file_path`

### Task 4.2: ResultsManager Tests
- [ ] `test_save_intermediate_folder_creates_correct_structure`
- [ ] `test_save_intermediate_folder_naming`
- [ ] `test_load_configs_from_folder`
- [ ] `test_load_configs_from_folder_missing_file_error`

### Task 4.3: SimulationManager Tests
- [ ] `test_iterative_with_per_week_tracking`
- [ ] `test_intermediate_folder_save`
- [ ] `test_resume_from_folder`
- [ ] `test_base_param_optimization_updates_base_config`
- [ ] `test_week_specific_param_optimization_updates_week_configs`
- [ ] `test_full_optimization_uses_per_week_tracking`

### Task 4.4: Integration Tests
- [ ] End-to-end test: Start iterative optimization → interrupt → resume → complete
- [ ] Verify folder output structure matches specification

### Task 4.5: Run All Tests
- [ ] Run `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Document any test failures and fixes

---

## Phase 5: Documentation and Cleanup
### Task 5.1: Update Documentation
- [ ] Update `simulation/README.md` with new folder output format
- [ ] Update `CLAUDE.md` if needed
- [ ] Add examples of new folder structure

### Task 5.2: Cleanup
- [ ] Remove any deprecated single-file save methods if no longer needed
- [ ] Move `updates/week-by-week-simulation-integration.txt` to `updates/done/`
- [ ] Delete questions file

---

## Integration Verification Checklist
**Completed during iterations 14-16. All line numbers verified 2025-12-02.**

### New Components and Their Callers (Verified ✓)

| New Component | File | Called By | Caller File:Line | TODO Task | Verified |
|---------------|------|-----------|------------------|-----------|----------|
| `is_base_param()` | ConfigGenerator.py | `run_iterative_optimization()` | SimulationManager.py:524 | Task 3.3 | ✓ |
| `is_week_specific_param()` | ConfigGenerator.py | `run_iterative_optimization()` | SimulationManager.py:524 | Task 3.3 | ✓ |
| `PARAM_TO_SECTION_MAP` | ConfigGenerator.py | `is_base_param()` | ConfigGenerator.py (internal) | Task 1.1 | ✓ |
| `load_baseline_from_folder()` | ConfigGenerator.py | `__init__()` | ConfigGenerator.py:~198 | Task 1.2, 1.3 | ✓ |
| `save_intermediate_folder()` | ResultsManager.py | `run_iterative_optimization()` | SimulationManager.py:538 | Task 2.1, 3.4 | ✓ |
| `load_configs_from_folder()` | ResultsManager.py | `_detect_resume_state()` | SimulationManager.py:456 | Task 2.2, 3.5 | ✓ |

### Existing Components Needing Integration (Orphan Code - Verified ✓)

| Existing Component | File:Line | Current Caller | Required Caller | TODO Task | Status |
|-------------------|-----------|----------------|-----------------|-----------|--------|
| `run_simulations_for_config_with_weeks()` | ParallelLeagueRunner.py:253 | NONE | SimulationManager:513 | Task 3.1 | ⏳ |
| `record_week_results()` | ResultsManager.py:82 | NONE | SimulationManager:520 | Task 3.1 | ⏳ |
| `get_best_config_for_range()` | ResultsManager.py:121 | NONE | SimulationManager:525 | Task 3.3 | ⏳ |
| `get_best_configs_per_range()` | ResultsManager.py:159 | NONE | SimulationManager:525 | Task 3.3 | ⏳ |
| `save_optimal_configs_folder()` | ResultsManager.py:364 | NONE | SimulationManager:565 | Task 3.6 | ⏳ |

### Caller Modifications Required in SimulationManager.py (Verified ✓)

| Current Code | Line | New Code | Task | Verified |
|--------------|------|----------|------|----------|
| `self.parallel_runner.run_simulations_for_config(...)` | 513 | `self.parallel_runner.run_simulations_for_config_with_weeks(...)` | 3.1 | ✓ |
| `self.results_manager.record_result(...)` | 520 | `self.results_manager.record_week_results(...)` | 3.1 | ✓ |
| `current_optimal_config = best_result.config_dict` | 535 | Split into base_config and week_configs per range | 3.2, 3.3 | ✓ |
| `intermediate_path = ... .json` | 538-543 | Use save_intermediate_folder() | 3.4 | ✓ |
| `self.output_dir.glob("intermediate_*.json")` | 311 | `self.output_dir.glob("intermediate_*/")` + error check | 3.5 | ✓ |
| `with open(last_config_path, 'r') as f: ...` | 456-457 | Use load_configs_from_folder() | 3.5 | ✓ |
| `optimal_config_path = ... .json` (lines 565-569) | 565-569 | Use save_optimal_configs_folder() | 3.6 | ✓ |
| `league_config_path = ... / "league_config.json"` | 578 | Copy to data/configs/ folder | 3.6 | ✓ |

### ~~Integration Verification for Full Optimization Mode~~ (REMOVED)
**Answer Q1**: User confirmed full optimization mode will be removed in the future.
No changes to `run_full_optimization()`. Only iterative mode gets per-week tracking.

### Additional Integration: Auto-Update to Folder (Answer Q5)
| Current Code | Line | Required Change | Task |
|--------------|------|-----------------|------|
| `league_config_path = ... / "data" / "league_config.json"` | 578 | Change to `data/configs/` folder | 3.6 |
| `self.results_manager.update_league_config(...)` | 580 | Copy all 4 files to data/configs/ | 3.6 |

### Data Flow Traces (Updated with User Answers)

#### Requirement 1: Simulations track per-week-range performance (Iterative Only - Q1)
```
Entry: run_simulation.py --mode iterative (line 351)
  → SimulationManager.__init__() (line 57)
    → ConfigGenerator.__init__()
      → NEW: Validate baseline_config_path is folder (Q2: folder only)
      → NEW: load_baseline_from_folder() ← CHANGE NEEDED
  → SimulationManager.run_iterative_optimization() (line 390)
    → CURRENT: self.parallel_runner.run_simulations_for_config() (line 513)
    → REQUIRED: self.parallel_runner.run_simulations_for_config_with_weeks() ← CHANGE
    → CURRENT: self.results_manager.record_result() (line 520)
    → REQUIRED: self.results_manager.record_week_results() ← CHANGE
  → Output: Per-week performance tracked in ConfigPerformance
```

#### Requirement 2: Intermediate saves are folders (with Full Metrics - Q4)
```
Entry: run_simulation.py --mode iterative
  → SimulationManager.run_iterative_optimization() (line 390)
    → CURRENT: Saves to intermediate_{idx}_{param}.json (line 538-543)
    → REQUIRED: Saves to intermediate_{idx}_{param}/ folder ← CHANGE
      → Uses ResultsManager.save_intermediate_folder() ← NEW METHOD
      → Includes performance_metrics with per-range win rates (Q4)
  → Output: Folder with 4 config files + metrics
```

#### Requirement 3: Final output is folder + Auto-Update to data/configs/ (Q5)
```
Entry: run_simulation.py --mode iterative
  → SimulationManager.run_iterative_optimization() (line 390)
    → CURRENT: Saves to optimal_iterative_{timestamp}.json (line 565-569)
    → REQUIRED: Saves to optimal_iterative_{timestamp}/ folder ← CHANGE
      → Uses ResultsManager.save_optimal_configs_folder() ← EXISTS
    → CURRENT: Updates data/league_config.json (line 578-580)
    → REQUIRED: Updates data/configs/ folder (Q5) ← CHANGE
      → Copies all 4 files to data/configs/
  → Output: Folder + data/configs/ updated
```

#### Requirement 4: Resume from folder + Error on Old Files (Q3)
```
Entry: run_simulation.py --mode iterative
  → SimulationManager.run_iterative_optimization() (line 390)
    → SimulationManager._detect_resume_state() (line 290)
      → NEW: Check for old intermediate_*.json files ← ADD
      → NEW: If found, raise ValueError (Q3: Error and stop) ← ADD
      → CURRENT: Looks for intermediate_*.json files (line 311)
      → REQUIRED: Looks for intermediate_*/ folders ← CHANGE
      → CURRENT: Loads single JSON file (line 456-457)
      → REQUIRED: Loads from folder ← CHANGE
        → Uses ResultsManager.load_configs_from_folder() ← NEW METHOD
  → Output: Resume from folder structure (or error if old files exist)
```

#### Requirement 5: Different optimal values per week range
```
Entry: run_simulation.py --mode iterative
  → SimulationManager.run_iterative_optimization() (line 390)
    → For each parameter in PARAMETER_ORDER:
      → NEW: Check if is_base_param(param_name) ← ADD
      → CURRENT: Tracks single current_optimal_config (line 535)
      → REQUIRED: ← CHANGE
        IF is_base_param(): update current_base_config (overall best)
        IF is_week_specific_param():
          → get_best_config_for_range("1-5") → update week_configs["1-5"]
          → get_best_config_for_range("6-11") → update week_configs["6-11"]
          → get_best_config_for_range("12-17") → update week_configs["12-17"]
  → Output: Different optimal values per week range
```

---

## Verification Summary
### First Verification Round (Complete)
- [x] Iteration 1: Initial verification - Identified already-implemented vs missing components
- [x] Iteration 2-4: Deep dive - Found PARAM_TO_SECTION_MAP needed for parameter classification
- [x] Iteration 5: Data flow - Traced 5 requirements from entry point to output
- [x] Iteration 6: Skeptical re-verification - Verified line numbers, found full optimization mode question
- [x] Iteration 7: Integration gap check - Created integration matrix with 6 new + 5 existing components

**Key Findings:**
1. 5 existing methods need to be CALLED (currently orphan code)
2. 6 new methods need to be CREATED and integrated
3. 7 lines in SimulationManager.py need modification
4. Full optimization mode may also need updates (OPEN QUESTION)

### Second Verification Round (Complete)
- [x] Iterations 8-11: Standard verification with answers (integrated user choices)
- [x] Iteration 12: End-to-end data flow verification (updated traces with answers)
- [x] Iteration 13: Skeptical re-verification (verified all line numbers in SimulationManager.py)
- [x] Iteration 14: Integration gap check (finalized integration matrix below)
- [x] Iterations 15-16: Final preparation (checklist complete, ready for implementation)

**Verified Line Numbers in SimulationManager.py (as of 2025-12-02):**
- Line 101: ConfigGenerator.__init__() call - needs folder path validation
- Line 311: `intermediate_*.json` glob in _detect_resume_state()
- Line 456-457: JSON load in _detect_resume_state()
- Line 513: `run_simulations_for_config()` call
- Line 520: `record_result()` call
- Line 535: `current_optimal_config = best_result.config_dict`
- Line 538-543: Intermediate JSON save block
- Line 565-569: Final optimal config JSON save block
- Line 577-583: Auto-update league_config.json block

---

## Notes
- Keep this file updated as work progresses
- Run tests after each phase completion
- Commit after each phase passes all tests
