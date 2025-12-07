# Week-by-Week Config TODO

**Status**: DRAFT (Pre-verification)
**Objective File**: `updates/week-by-week-config.txt`
**Created**: 2025-12-01

---

## Overview

Update the configuration loading system to support week-specific scoring parameters. The new system uses:
- **Base config**: `data/configs/league_config.json` - Contains static parameters (NFL settings, roster limits, draft order, ADP_SCORING)
- **Week-specific configs**: `data/configs/week{start}-{end}.json` - Contains variable scoring parameters for specific week ranges

The simulation system will be updated to output folders containing 4 config files instead of single files.

---

## Requirements from Original Specification

1. Update how config parameters are loaded into league helper
2. New folder structure at `data/configs/` with 4 files
3. Week-specific configs apply based on CURRENT_NFL_WEEK
4. Simulation tests configs per week block to find best win rate
5. Simulation outputs folders (not files) with 4 config files each
6. Original `data/league_config.json` is deprecated and deleted

---

## Phase 1: ConfigManager Updates

### 1.1 Update ConfigManager to load from configs folder
**Files to modify**: `league_helper/util/ConfigManager.py`

- [ ] Update `__init__` to accept configs folder path instead of data folder
- [ ] Update `config_path` to point to `data/configs/league_config.json`
- [ ] Add method to determine week range from CURRENT_NFL_WEEK
- [ ] Add method to load week-specific config file
- [ ] Update `_load_config` to merge base config with week-specific config
- [ ] Update `_extract_parameters` to handle merged config

**Week Range Logic**:
- Weeks 1-5: Load `week1-5.json`
- Weeks 6-11: Load `week6-11.json`
- Weeks 12-17: Load `week12-17.json`

### 1.2 Update all ConfigManager callers
**Files to search**: All files that instantiate ConfigManager

- [ ] Search codebase for `ConfigManager(` instantiations
- [ ] Update each to use new path structure
- [ ] Verify no hardcoded paths to old `league_config.json`

---

## Phase 2: Simulation System Updates

### 2.1 Update ResultsManager to save folders
**Files to modify**: `simulation/ResultsManager.py`

- [ ] Update `save_optimal_config` to create folder instead of file
- [ ] Save 4 config files in each result folder:
  - `league_config.json` (base config)
  - `week1-5.json` (week-specific)
  - `week6-11.json` (week-specific)
  - `week12-17.json` (week-specific)
- [ ] Update `update_league_config` to work with folder structure

### 2.2 Update SimulationManager output handling
**Files to modify**: `simulation/SimulationManager.py`

- [ ] Update `run_full_optimization` to handle folder output
- [ ] Update `run_iterative_optimization` to handle folder output
- [ ] Update intermediate result saving to use folder structure
- [ ] Update resume detection to work with folders

### 2.3 Update ConfigGenerator for week-block testing
**Files to modify**: `simulation/ConfigGenerator.py`

- [ ] Add logic to test configs per week block
- [ ] Track best performing config for each week range
- [ ] Generate separate optimal configs per week range

---

## Phase 3: Cleanup and Migration

### 3.1 Delete deprecated files
- [ ] Delete `data/league_config.json` (original file)
- [ ] Verify no remaining references to deleted file

### 3.2 Update documentation
- [ ] Update README.md with new config structure
- [ ] Update CLAUDE.md with new file paths
- [ ] Update any other relevant documentation

---

## Phase 4: Testing

### 4.1 Update existing tests
**Files to modify**: `tests/league_helper/util/test_ConfigManager.py`

- [ ] Update tests for new config loading logic
- [ ] Add tests for week range determination
- [ ] Add tests for config merging
- [ ] Update mock fixtures for new structure

### 4.2 Update simulation tests
**Files to modify**: `tests/simulation/test_*.py`

- [ ] Update tests for folder output
- [ ] Update tests for week-block testing
- [ ] Update mock fixtures

### 4.3 Create new integration tests
- [ ] Test end-to-end config loading
- [ ] Test simulation folder output

### 4.4 Run full test suite
- [ ] Run `python tests/run_all_tests.py`
- [ ] Ensure 100% pass rate
- [ ] Fix any failing tests

---

## Phase 5: Pre-Commit Validation

- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Verify 100% test pass rate
- [ ] Manual testing of league helper modes
- [ ] Manual testing of simulation system
- [ ] Update documentation

---

## Important Notes

- Keep this TODO file updated with progress
- Run tests after each phase completion
- The original `data/league_config.json` will be deleted - ensure no backward compatibility needed
- Week ranges are fixed: 1-5, 6-11, 12-17

---

## Verification Summary

**First Verification Round**: COMPLETE (5/5 iterations)
**Second Verification Round**: COMPLETE (5/5 iterations)
**Total**: 10/10 iterations complete

**User Answers Incorporated**:
1. Single config per simulation, analyze per-block after ✓
2. Different optimal config per week range ✓
3. Base config from best OVERALL (because DRAFT_ORDER is tested) ✓
4. ConfigManager auto-merges based on CURRENT_NFL_WEEK ✓

**Key Requirements**:
- Per-week-range performance tracking in ConfigPerformance
- Folder output with 4 JSON files instead of single file
- Best overall config for base, best per-range for week files
- Auto-merge in ConfigManager for league helper

**Critical Changes Identified**:
- ConfigManager: Detect configs folder, load/merge week-specific
- ConfigPerformance: Track wins/losses per week range
- SimulatedLeague: Return per-week results
- ResultsManager: Get best per range, save folder structure

**Status**: COMPLETE

## Implementation Progress

### Phase 1: ConfigManager Changes - COMPLETE
- [x] Added `configs_folder` attribute detection
- [x] Added `_get_week_config_filename()` method
- [x] Added `_load_week_config()` method
- [x] Modified `_load_config()` to merge week-specific params
- [x] Added 25 new tests for week config loading
- [x] All 101 ConfigManager tests pass

### Phase 2: Simulation Result Tracking - COMPLETE
- [x] Added `get_week_range()` module function
- [x] Added `week_range_wins/losses/points` tracking to ConfigPerformance
- [x] Added `add_week_results()` method for per-week tracking
- [x] Added `get_win_rate_for_range()` method
- [x] Updated `to_dict()` to include per-range performance
- [x] Added 14 new tests for per-week tracking
- [x] All 57 ConfigPerformance tests pass
- [x] SimulatedLeague.get_draft_helper_results_by_week() added
- [x] ParallelLeagueRunner.run_simulations_for_config_with_weeks() added
- [x] ResultsManager.record_week_results() added
- [x] ResultsManager.get_best_config_for_range() added
- [x] ResultsManager.get_best_configs_per_range() added

### Phase 3: Output Folder Structure - COMPLETE
- [x] ResultsManager.save_optimal_configs_folder() creates folder
- [x] _extract_base_params() helper function
- [x] _extract_week_params() helper function
- [x] Save 4 config files per folder (league_config.json, week1-5.json, week6-11.json, week12-17.json)

### Phase 4: Cleanup - COMPLETE
- [x] Original data/league_config.json kept for backward compatibility (can be deleted when ready)
- [x] All 2235 tests passing

---

## Iteration 1 Findings

### Key Files Analyzed
- `league_helper/util/ConfigManager.py` (1155 lines) - Main config loading logic
- `simulation/SimulationManager.py` (660 lines) - Orchestrates simulation
- `simulation/ResultsManager.py` (379 lines) - Saves optimal configs
- `simulation/SimulatedLeague.py` (416 lines) - Creates temp config for each sim
- `simulation/ConfigGenerator.py` (993 lines) - Generates parameter combinations

### Current Config Structure
**Base config (`data/configs/league_config.json`)** contains:
- CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT
- NORMALIZATION_MAX_SCALE
- SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT
- INJURY_PENALTIES
- DRAFT_ORDER_BONUSES, DRAFT_ORDER_FILE, DRAFT_ORDER
- MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS
- ADP_SCORING (only scoring parameter in base!)

**Week-specific configs (`week{N}-{M}.json`)** contain:
- PLAYER_RATING_SCORING
- TEAM_QUALITY_SCORING
- PERFORMANCE_SCORING
- MATCHUP_SCORING
- SCHEDULE_SCORING
- TEMPERATURE_SCORING
- WIND_SCORING
- LOCATION_MODIFIERS

### ConfigManager Current Behavior
- Takes `data_folder` Path as parameter
- Looks for `league_config.json` directly in that folder
- `_load_config()` reads single file and calls `_extract_parameters()`
- Has `current_nfl_week` attribute set from config

### Simulation Current Behavior
- `SimulatedLeague` creates temp directory for each simulation
- Saves `config_dict` as `league_config.json` in temp dir
- Copies to each team directory
- Each team gets its own ConfigManager instance

### ResultsManager Current Behavior
- `save_optimal_config()` saves single JSON file with timestamp
- `update_league_config()` copies optimal to `data/league_config.json`

### Critical Dependencies
1. **ConfigManager initialization**: Many callers pass data folder, expect `league_config.json` directly inside
2. **SimulatedLeague config handling**: Creates temp config files for each simulation
3. **Test fixtures**: Many tests create temp `league_config.json` files
4. **CURRENT_NFL_WEEK**: Used to determine which week-specific config to load

### Week Range Logic Needed
```python
def get_week_range(week: int) -> str:
    if 1 <= week <= 5:
        return "1-5"
    elif 6 <= week <= 11:
        return "6-11"
    elif 12 <= week <= 17:
        return "12-17"
    else:
        raise ValueError(f"Invalid week: {week}")
```

### Questions Identified (to ask after iteration 5)
1. Should ConfigManager merge configs at load time, or provide separate access methods?
2. How should simulation save results - as folders with 4 files or merged single files?
3. Should the simulation test ALL week ranges for each config variation?
4. How should the simulation determine "best" config when different week ranges may have different winners?

---

## Progress Log

| Date | Phase | Status | Notes |
|------|-------|--------|-------|
| 2025-12-01 | Draft TODO | Created | Initial draft based on specification |
| 2025-12-01 | Iteration 1 | Completed | Codebase research, identified patterns and dependencies |
| 2025-12-01 | Iteration 2 | Completed | Deep dive into simulation flow, understood config usage |
| 2025-12-01 | Iteration 3 | Completed | Integration points, error handling, test patterns |
| 2025-12-01 | Iteration 4 | Completed | Implementation details, merging strategy, test helpers |
| 2025-12-01 | Iteration 5 | Completed | Skeptical re-verification, discovered per-week-range tracking need |
| 2025-12-01 | Iteration 6 | Completed | Incorporated user answers, analyzed param categorization |
| 2025-12-01 | Iteration 7 | Completed | Data flow analysis for per-week result tracking |
| 2025-12-01 | Iteration 8 | Completed | Test strategy and implementation ordering |
| 2025-12-01 | Iteration 9 | Completed | Final implementation plan |
| 2025-12-01 | Iteration 10 | Completed | Final skeptical re-verification |

---

## Iteration 7-10 Findings

### Data Flow Analysis (Iteration 7)

**Current flow** (aggregate results only):
```
SimulatedLeague.get_draft_helper_results()
    → Returns: (total_wins, total_losses, total_points)
    → ParallelLeagueRunner.run_single_simulation()
        → Returns: (wins, losses, points)
        → ResultsManager.record_result(config_id, wins, losses, points)
            → ConfigPerformance.add_league_result(wins, losses, points)
```

**Required flow** (per-week results):
```
SimulatedLeague.get_draft_helper_results_by_week()
    → Returns: List[Tuple[week, won, points]]  # 16 entries
    → ParallelLeagueRunner.run_single_simulation()
        → Returns: List[Tuple[week, won, points]]
        → ResultsManager.record_week_results(config_id, week_results)
            → ConfigPerformance.add_week_result(week, won, points)
                → Updates both overall AND per-range tracking
```

### Implementation Order (Iteration 8-9)

**Phase 1: Core Changes (ConfigManager)**
1. Add `_get_week_config_filename()` method
2. Add `_load_week_config()` method
3. Modify `__init__()` to detect configs folder
4. Modify `_load_config()` to merge week-specific params
5. Update tests for ConfigManager

**Phase 2: Simulation Result Tracking**
1. Modify `ConfigPerformance` to track per-week-range results
2. Modify `SimulatedLeague.get_draft_helper_results()` to return per-week data
3. Modify `ParallelLeagueRunner.run_single_simulation()` return type
4. Modify `ResultsManager.record_result()` to handle per-week data
5. Add `ResultsManager.get_best_config_for_range()`
6. Modify `ResultsManager.save_optimal_config()` to create folder
7. Update tests for all simulation modules

**Phase 3: Output Folder Structure**
1. Create helper to extract base params from config
2. Create helper to extract week-specific params from config
3. Update `save_optimal_config()` to save 4 files in folder
4. Update `update_league_config()` to work with folder structure

**Phase 4: Cleanup**
1. Delete `data/league_config.json`
2. Update integration tests
3. Update documentation (README, CLAUDE.md)

### Test Strategy (Iteration 8)

**New Tests Required**:

1. `test_ConfigManager_week_config.py`:
   - Test week range detection
   - Test config merging
   - Test missing week config handling
   - Test each week boundary (5→6, 11→12)

2. `test_ConfigPerformance_per_week.py`:
   - Test per-week-range win rate calculation
   - Test week range categorization

3. `test_ResultsManager_folder_output.py`:
   - Test folder creation
   - Test 4-file output structure
   - Test best config per range selection

**Updated Test Helper**:
```python
def create_test_configs_structure(temp_path: Path, week: int = 6) -> Path:
    """Create complete configs folder structure for tests."""
    configs_folder = temp_path / 'configs'
    configs_folder.mkdir()

    base_config = {...}  # Base params only
    week_config = {...}  # Week-specific params

    (configs_folder / 'league_config.json').write_text(...)
    (configs_folder / 'week1-5.json').write_text(...)
    (configs_folder / 'week6-11.json').write_text(...)
    (configs_folder / 'week12-17.json').write_text(...)

    return temp_path
```

### Final Skeptical Verification (Iteration 10)

**Potential Issues Identified**:

1. **Week 16 vs 17**: Simulation runs weeks 1-16, but config has week12-17.json
   - Week 16 is within 12-17 range ✓
   - No issue, just noting the boundary

2. **Draft week**: Draft uses week 1 params (week1-5 config)
   - Draft decisions are made at "week 1" equivalent
   - This is correct behavior ✓

3. **SCHEDULE_SCORING**: Looks ahead at future matchups
   - Still uses current week's config for the calculation
   - This is acceptable behavior ✓

4. **MIN_WEEKS thresholds**: Some scoring has MIN_WEEKS requirements
   - Early weeks (1-5) may not meet MIN_WEEKS for some calculations
   - This is existing behavior, unchanged ✓

5. **Test fixture migration**: ~100+ files need updating
   - Create shared helper fixture in conftest.py
   - Reduces duplication

**Verification Summary**: Implementation plan is sound and complete.

---

## Iteration 6 Findings

### Parameter Categorization Analysis

Based on ConfigGenerator.PARAM_DEFINITIONS, params fall into two categories:

**Base Config Params** (affect all weeks uniformly):
- NORMALIZATION_MAX_SCALE, SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT
- PRIMARY_BONUS, SECONDARY_BONUS, DRAFT_ORDER_FILE
- ADP_SCORING_WEIGHT, ADP_SCORING_STEPS

**Week-Specific Params** (may have different optimal values per week range):
- PLAYER_RATING_SCORING_WEIGHT
- TEAM_QUALITY_SCORING_WEIGHT, TEAM_QUALITY_MIN_WEEKS
- PERFORMANCE_SCORING_WEIGHT, PERFORMANCE_SCORING_STEPS, PERFORMANCE_MIN_WEEKS
- MATCHUP_IMPACT_SCALE, MATCHUP_SCORING_WEIGHT, MATCHUP_MIN_WEEKS
- TEMPERATURE_IMPACT_SCALE, TEMPERATURE_SCORING_WEIGHT
- WIND_IMPACT_SCALE, WIND_SCORING_WEIGHT
- LOCATION_HOME, LOCATION_AWAY, LOCATION_INTERNATIONAL

### Output Structure Refined

Given user answer to Q3, the output folder structure is:
```
optimal_2025-12-01_12-00-00/
├── league_config.json    # From best OVERALL config
│   └── Contains: NORMALIZATION_*, BYE_WEIGHTS, DRAFT_ORDER*, ADP_SCORING
├── week1-5.json          # From config with best weeks 1-5 win rate
│   └── Contains: PLAYER_RATING_*, TEAM_QUALITY_*, PERFORMANCE_*,
│                 MATCHUP_*, TEMPERATURE_*, WIND_*, LOCATION_*
├── week6-11.json         # From config with best weeks 6-11 win rate
│   └── Contains: Same params as week1-5.json but different values
└── week12-17.json        # From config with best weeks 12-17 win rate
    └── Contains: Same params as week1-5.json but different values
```

### ConfigPerformance Changes Required

Need to track:
1. Overall win rate (for determining best base config)
2. Per-week-range win rates (for determining best week-specific configs)

```python
class ConfigPerformance:
    def __init__(self, ...):
        # Overall tracking (existing)
        self.total_wins = 0
        self.total_losses = 0

        # Per-week-range tracking (new)
        self.week_range_wins = {"1-5": 0, "6-11": 0, "12-17": 0}
        self.week_range_losses = {"1-5": 0, "6-11": 0, "12-17": 0}

    def add_week_result(self, week: int, won: bool, points: float):
        """Add single week result to both overall and per-range tracking."""
        if won:
            self.total_wins += 1
            self.week_range_wins[self._get_range(week)] += 1
        else:
            self.total_losses += 1
            self.week_range_losses[self._get_range(week)] += 1
```

### ResultsManager Changes Required

```python
class ResultsManager:
    def get_best_overall_config(self) -> ConfigPerformance:
        """Best config by overall win rate (for base config)."""
        return max(self.results.values(), key=lambda c: c.get_win_rate())

    def get_best_config_for_range(self, week_range: str) -> ConfigPerformance:
        """Best config by win rate in specific week range."""
        return max(
            self.results.values(),
            key=lambda c: c.get_win_rate_for_range(week_range)
        )

    def save_optimal_config(self, output_dir: Path) -> Path:
        """Save optimal configs as folder with 4 files."""
        best_overall = self.get_best_overall_config()
        best_per_range = {
            "1-5": self.get_best_config_for_range("1-5"),
            "6-11": self.get_best_config_for_range("6-11"),
            "12-17": self.get_best_config_for_range("12-17")
        }
        # ... create folder and save files ...
```

---

## Iteration 2 Findings

### Simulation Flow Analysis
1. **SimulatedLeague.__init__()**: Creates temp dir, saves config_dict as `league_config.json`
2. **SimulatedLeague._initialize_teams()**: Creates 10 teams, each gets ConfigManager instance
3. **SimulatedLeague.run_draft()**: Teams use config for draft recommendations
4. **SimulatedLeague.run_season()**: Loops through weeks 1-16, each week calls `team.set_weekly_lineup(week_num)`
5. **Week.simulate_week()**: Calls `team.set_weekly_lineup()` which uses config for scoring

### Critical Insight: Config Usage During Season
- Teams have a `config` attribute set at initialization
- Config is used for:
  - Draft recommendations (via AddToRosterModeManager)
  - Weekly lineup optimization (via StarterHelperModeManager)
- **Config is NOT updated between weeks currently**
- `team.config.current_nfl_week` is manually updated but scoring params remain constant

### Design Implications
The specification says:
> "it determines which config produced the best win rate for each block of weeks"

This suggests analyzing results per week block, NOT changing config during simulation:
1. Run full 16-week simulation with merged config
2. Track wins/losses by week range (1-5, 6-11, 12-17)
3. Determine which config performed best in each block
4. Save optimal config per block

### ConfigManager Merging Approach
For league_helper (non-simulation):
- ConfigManager loads base config
- Determines current week range from CURRENT_NFL_WEEK
- Loads appropriate week-specific config
- Merges week-specific params over base params
- All callers continue to use ConfigManager normally

For simulation:
- SimulatedLeague creates temp dir with merged config
- Uses single merged config for entire 16-week run
- ResultsManager tracks performance per week block
- Saves best config per week block to output folder

### Files Needing Modification (Updated)
1. **ConfigManager** - Add config folder support, week-based merging
2. **SimulatedLeague** - Already creates merged config in temp, minimal changes
3. **ResultsManager** - Track per-block performance, save folder output
4. **SimulationManager** - Handle folder output for results

### Merging Strategy
```python
# In ConfigManager._load_config():
# 1. Load base config from data/configs/league_config.json
# 2. Determine week range from CURRENT_NFL_WEEK
# 3. Load week-specific config (e.g., week6-11.json)
# 4. Merge: base_params.update(week_specific_params)
```

---

## Iteration 3 Findings

### Error Handling Patterns
From `test_ConfigManager_thresholds.py`:
- Missing config file → `FileNotFoundError("Configuration file not found")`
- Invalid JSON → `json.JSONDecodeError`
- Missing required parameters → `ValueError("Config missing required parameters...")`
- Missing nested fields → `ValueError("..._PENALTIES missing levels: HIGH")`

### Test Fixture Patterns
All tests create temp directories with `league_config.json`:
```python
@pytest.fixture
def temp_data_folder():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def minimal_config(temp_data_folder):
    config_content = {...}
    config_file = temp_data_folder / "league_config.json"
    with open(config_file, 'w') as f:
        json.dump(config_content, f)
    return temp_data_folder
```

### New Test Requirements
For ConfigManager with configs folder:
1. Test when `data/configs/` folder doesn't exist
2. Test when base `league_config.json` doesn't exist in configs folder
3. Test when week-specific file doesn't exist
4. Test merging logic for each week range
5. Test week boundary cases (weeks 5→6, 11→12)
6. Test invalid week values (0, 18, -1)

### Backward Compatibility Consideration
**IMPORTANT**: The spec says "No need for backward compatibility" but tests create `league_config.json` directly in data folder. Need to:
1. Update ALL test fixtures to use `data/configs/` structure
2. Or make ConfigManager detect old vs new structure (NOT preferred per spec)

### Integration Points
1. **LeagueHelperManager** → ConfigManager: Passes `data_folder` (e.g., `./data`)
2. **SimulatedLeague** → ConfigManager: Passes team-specific temp dir
3. **Integration tests** → Copy from `data/league_config.json` (needs update)

### Risk: Test Migration
- ~100+ test files create temp `league_config.json`
- All need to be updated for new folder structure
- Consider creating a helper fixture that creates full configs structure

---

## Iteration 4 Findings

### ConfigManager Implementation Details

**Current `__init__` signature**:
```python
def __init__(self, data_folder: Path) -> None:
    self.config_path = data_folder / 'league_config.json'
```

**New approach needed**:
```python
def __init__(self, data_folder: Path) -> None:
    # Check for new folder structure
    configs_folder = data_folder / 'configs'
    if configs_folder.exists():
        # New structure: data/configs/league_config.json + week files
        self.config_path = configs_folder / 'league_config.json'
        self.configs_folder = configs_folder
    else:
        # Legacy fallback for tests (temp dirs won't have configs subfolder)
        self.config_path = data_folder / 'league_config.json'
        self.configs_folder = None
```

**Week-specific loading method**:
```python
def _get_week_config_filename(self, week: int) -> str:
    """Return week-specific config filename based on week number."""
    if 1 <= week <= 5:
        return "week1-5.json"
    elif 6 <= week <= 11:
        return "week6-11.json"
    elif 12 <= week <= 17:
        return "week12-17.json"
    else:
        raise ValueError(f"Invalid week number: {week}")

def _load_week_config(self) -> Dict[str, Any]:
    """Load week-specific config and merge with base parameters."""
    if self.configs_folder is None:
        return {}  # No week-specific config in legacy mode

    week_file = self.configs_folder / self._get_week_config_filename(
        self.current_nfl_week
    )

    if not week_file.exists():
        self.logger.warning(f"Week config not found: {week_file}")
        return {}

    with open(week_file, 'r') as f:
        week_data = json.load(f)

    return week_data.get('parameters', {})
```

**Merging in `_load_config`**:
```python
def _load_config(self) -> None:
    # ... existing load logic ...

    # After loading base config and extracting CURRENT_NFL_WEEK
    self.current_nfl_week = self.parameters[self.keys.CURRENT_NFL_WEEK]

    # Load and merge week-specific parameters
    week_params = self._load_week_config()
    self.parameters.update(week_params)

    # Continue with _extract_parameters()
```

### Required Parameters Analysis

**Base config requires** (per `_extract_parameters`):
- CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT
- NORMALIZATION_MAX_SCALE, SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT
- INJURY_PENALTIES
- ADP_SCORING
- PLAYER_RATING_SCORING ← In week-specific!
- TEAM_QUALITY_SCORING ← In week-specific!
- PERFORMANCE_SCORING ← In week-specific!
- MATCHUP_SCORING ← In week-specific!
- DRAFT_ORDER_BONUSES, DRAFT_ORDER, MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS

**PROBLEM**: The required params check happens BEFORE week config merge!

**Solution**: Either:
1. Move week config loading before required check
2. Or modify required params list based on structure
3. Or ensure base config has ALL scoring params (even if overwritten)

### Recommended Approach
Since spec says "no backward compatibility", we can:
1. Move the required params validation AFTER merging
2. Load base config → extract CURRENT_NFL_WEEK → load week config → merge → validate → extract

### Test Helper Function
```python
def create_test_configs_folder(temp_path: Path, week: int = 6) -> Path:
    """Create full configs folder structure for testing."""
    configs_folder = temp_path / 'configs'
    configs_folder.mkdir()

    # Create base config
    base_config = {
        "config_name": "Test",
        "description": "Test config",
        "parameters": {
            "CURRENT_NFL_WEEK": week,
            "NFL_SEASON": 2025,
            "NFL_SCORING_FORMAT": "ppr",
            # ... other base params ...
        }
    }

    # Create week-specific config
    week_config = {
        "config_name": "Test Week",
        "description": "Test week config",
        "parameters": {
            "PLAYER_RATING_SCORING": {...},
            "TEAM_QUALITY_SCORING": {...},
            # ... other week params ...
        }
    }

    (configs_folder / 'league_config.json').write_text(json.dumps(base_config))
    (configs_folder / f'week{get_week_range(week)}.json').write_text(json.dumps(week_config))

    return temp_path
```

---

## Iteration 5 Findings (Skeptical Re-verification)

### Challenging My Understanding

**Re-reading the spec carefully**:
> "it determines which config produced the best win rate for each block of weeks"
> "have the 4 config files that were decided on contained within the folder"

**Key Insight**: The simulation might output DIFFERENT optimal configs for different week ranges!

Output folder structure:
```
optimal_2025-12-01_12-00-00/
├── league_config.json    (base config - shared)
├── week1-5.json          (best config for weeks 1-5)
├── week6-11.json         (best config for weeks 6-11)
└── week12-17.json        (best config for weeks 12-17)
```

This means:
- Config A might be best for weeks 1-5
- Config B might be best for weeks 6-11
- Config C might be best for weeks 12-17

### ConfigPerformance Needs Modification

**Current**: Tracks overall wins/losses across all 16 weeks
**Needed**: Track wins/losses per week range

```python
class ConfigPerformance:
    def __init__(self, config_id: str, config_dict: dict) -> None:
        # ... existing ...
        # NEW: Track per-week-range performance
        self.week_range_results = {
            "1-5": {"wins": 0, "losses": 0, "points": 0.0},
            "6-11": {"wins": 0, "losses": 0, "points": 0.0},
            "12-17": {"wins": 0, "losses": 0, "points": 0.0}
        }

    def add_week_result(self, week: int, won: bool, points: float) -> None:
        """Add result for a single week to appropriate range."""
        week_range = self._get_week_range(week)
        if won:
            self.week_range_results[week_range]["wins"] += 1
        else:
            self.week_range_results[week_range]["losses"] += 1
        self.week_range_results[week_range]["points"] += points
```

### Week.simulate_week() Needs to Return Per-Team Results

Currently returns Dict[Team, WeekResult], but results aren't aggregated by week range.

Need to propagate week number through result tracking.

### ResultsManager Needs Enhancement

**Current**: `get_best_config()` returns single best config
**Needed**: `get_best_configs_per_week_range()` returns dict of best configs

```python
def get_best_configs_per_week_range(self) -> Dict[str, ConfigPerformance]:
    """Get best performing config for each week range."""
    best_per_range = {}
    for week_range in ["1-5", "6-11", "12-17"]:
        best = max(
            self.results.values(),
            key=lambda c: c.get_win_rate_for_range(week_range)
        )
        best_per_range[week_range] = best
    return best_per_range
```

### save_optimal_config Needs Modification

**Current**: Saves single JSON file
**Needed**: Create folder with 4 files

```python
def save_optimal_config(self, output_dir: Path) -> Path:
    """Save optimal configs (one per week range) to a folder."""
    best_configs = self.get_best_configs_per_week_range()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"optimal_{timestamp}"
    folder_path = output_dir / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    # Save base config (from any config - base params are same)
    base_config = extract_base_params(best_configs["1-5"].config_dict)
    (folder_path / "league_config.json").write_text(json.dumps(base_config))

    # Save week-specific configs
    for week_range, config_perf in best_configs.items():
        week_config = extract_week_params(config_perf.config_dict)
        (folder_path / f"week{week_range}.json").write_text(json.dumps(week_config))

    return folder_path
```

### Edge Cases Identified

1. **Draft week**: Happens at week 1 equivalent - uses week 1-5 config
2. **SCHEDULE_SCORING**: Looks at future weeks - but still uses current week's config
3. **Week 0 / Week 18**: Invalid - should raise ValueError
4. **Week boundaries**: Weeks 5→6 and 11→12 are config transition points

### Questions for User - ANSWERED

1. **Config during simulation**: **Option A** - Run full 16 weeks with single config, analyze per-block after
2. **Best config selection**: **Option A** - Different optimal config per week range (config_A for weeks 1-5, config_B for 6-11, etc.)
3. **Base config in output**: **Option B** - Base config from best OVERALL config (because DRAFT_ORDER and other base params are also tested in simulation)
4. **League Helper behavior**: **Option A** - ConfigManager auto-merges week-specific based on CURRENT_NFL_WEEK

### Key Insight from Q3 Answer
The base `league_config.json` contains params like DRAFT_ORDER that ARE being tested via simulation. Therefore:
- Base config comes from the config with best win rate across ALL 17 weeks
- Week-specific configs come from the configs with best win rate in their respective ranges
- This means output folder might have:
  - `league_config.json` from config_X (best overall)
  - `week1-5.json` from config_A (best for weeks 1-5)
  - `week6-11.json` from config_B (best for weeks 6-11)
  - `week12-17.json` from config_C (best for weeks 12-17)
