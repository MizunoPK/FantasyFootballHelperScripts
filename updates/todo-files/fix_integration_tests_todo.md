# TODO: Fix Integration Tests

**Objective**: Fix 13 failing integration tests that are out of sync with refactored codebase

**Status**: Phase 1 - Verification Complete (3 iterations done)

**Created**: 2025-10-18

---

## Verification Summary

✅ **3 verification iterations completed**
✅ **API research complete** - All current APIs documented
✅ **Codebase patterns identified** - Async testing pattern found
✅ **Test dependencies analyzed** - No circular dependencies
✅ **Risk assessment complete** - Low risk (unit tests passing)

**Key Findings from Research**:
- PlayerManager uses `get_player_list()` NOT `get_all_players()`
- TeamDataManager uses `get_available_teams()` NOT `get_all_teams()`
- ConfigPerformance uses `add_league_result()` NOT `add_result()`
- Config format is FLAT (no nested 'parameters' section)
- pytest-asyncio already available (in requirements.txt)
- Async test pattern already used in test_csv_utils.py and test_data_file_manager.py

---

## Phase 1: API Research & Verification ✅ COMPLETE

### 1.1 Research PlayerManager API ✅ COMPLETE
- **File**: `league_helper/util/PlayerManager.py`
- **Actual Method**: `get_player_list(drafted_vals, can_draft, min_scores, unlocked_only)`
- **Old Method (tests expect)**: `get_all_players()` ❌ DOESN'T EXIST

### 1.2 Research TeamDataManager API ✅ COMPLETE
- **File**: `league_helper/util/TeamDataManager.py`
- **Actual Method**: `get_available_teams() -> list[str]`
- **Old Method (tests expect)**: `get_all_teams()` ❌ DOESN'T EXIST

### 1.3 Research LeagueHelperManager API ✅ COMPLETE
- **File**: `league_helper/LeagueHelperManager.py`
- **Actual Attributes**: `config`, `team_data_manager`, `player_manager`, mode managers
- **Old Attribute (tests expect)**: `data_folder` ❌ NOT PUBLIC

### 1.4 Research NFLProjectionsCollector API ✅ COMPLETE
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Actual Class**: `NFLProjectionsCollector(settings: Settings)`
- **Old Class (tests expect)**: `PlayerDataFetcher(output_dir)` ❌ DOESN'T EXIST
- **Key Change**: Now async, requires Settings object with scoring_format, season, output_directory

### 1.5 Research Config Format ✅ COMPLETE
- **File**: `data/league_config.json`
- **Actual Format**: Flat JSON with "parameters" at top level
  ```json
  {
    "config_name": "...",
    "description": "...",
    "parameters": {
      "CURRENT_NFL_WEEK": 7,
      "NORMALIZATION_MAX_SCALE": 148.37,
      ... (all params here, flat structure)
    }
  }
  ```
- **Old Format (tests expect)**: Nested "parameters" section ❌ DOESN'T MATCH

### 1.6 Research ConfigPerformance API ✅ COMPLETE
- **File**: `simulation/ConfigPerformance.py`
- **Actual Method**: `add_league_result(wins, losses, points)`
- **Old Method (tests expect)**: `add_result(wins, losses, points)` ❌ WRONG NAME

### 1.7 Verify Async Test Patterns ✅ COMPLETE
- **pytest-asyncio**: Already in requirements.txt ✅
- **Pattern Example**: `tests/utils/test_csv_utils.py:214` uses `@pytest.mark.asyncio`
- **Pattern Example**: `tests/utils/test_data_file_manager.py:428` uses `@pytest.mark.asyncio`

---

## Phase 2: Fix test_data_fetcher_integration.py

**Status**: PENDING
**File**: `tests/integration/test_data_fetcher_integration.py` (260 lines, 9 test methods)
**Issue**: Import error - `PlayerDataFetcher` class doesn't exist

### 2.1 Update Imports
**Lines to modify**: 24-27
**Current**:
```python
from player_data_fetcher_main import PlayerDataFetcher
from player_data_models import PlayerProjection, PlayerWeeklyStats
from config import Config as PlayerConfig
```
**Change to**:
```python
from player_data_fetcher_main import NFLProjectionsCollector, Settings
from player_data_models import PlayerProjection, ScoringFormat, ProjectionData
from config import Config as PlayerConfig
```

### 2.2 Create Settings Fixture
**Add after line 35**:
```python
@pytest.fixture
def fetcher_settings(tmp_path):
    """Create Settings object for NFLProjectionsCollector"""
    return Settings(
        scoring_format=ScoringFormat.PPR,
        season=2024,
        output_directory=str(tmp_path),
        create_csv=True,
        create_json=False,
        create_excel=False
    )
```

### 2.3 Convert test_player_fetcher_initialization to Async
**Lines**: 46-56
**Current** (sync test):
```python
def test_player_fetcher_initialization(self, mock_espn_client, tmp_path):
    fetcher = PlayerDataFetcher(output_dir=tmp_path)
    assert fetcher is not None
    assert fetcher.output_dir == tmp_path
```
**Change to** (async test):
```python
@pytest.mark.asyncio
async def test_player_fetcher_initialization(self, mock_espn_client, fetcher_settings):
    collector = NFLProjectionsCollector(fetcher_settings)
    assert collector is not None
    assert collector.settings.output_directory == str(fetcher_settings.output_directory)
```

### 2.4 Convert test_fetch_and_export_workflow to Async
**Lines**: 58-78
**Pattern**: Same as 2.3 - add `@pytest.mark.asyncio`, make `async def`, update API calls

### 2.5 Convert test_player_data_can_be_exported_and_loaded to Async
**Lines**: 166-193
**Pattern**: Same as 2.3 - add `@pytest.mark.asyncio`, make `async def`, update API calls

### 2.6 Convert test_player_fetcher_handles_api_errors to Async
**Lines**: 200-211
**Pattern**: Same as 2.3 - add `@pytest.mark.asyncio`, make `async def`, update API calls

### 2.7 Update Mock Patches
**All `@patch` decorators throughout file**:
```python
# OLD:
@patch('player_data_fetcher_main.ESPNClient')

# NEW (if needed - may not need to change):
@patch('player_data_fetcher_main.ESPNClient')
```

### 2.8 Validation
**Command**: `python -m pytest tests/integration/test_data_fetcher_integration.py -v`
**Expected**: All tests pass

---

## Phase 3: Fix test_league_helper_integration.py

**Status**: PENDING
**File**: `tests/integration/test_league_helper_integration.py` (270 lines, 17 test methods)
**Issues**: 12 failures due to API mismatches

### 3.1 Fix test_league_helper_initializes_with_valid_data_folder
**Line**: 98
**Current**:
```python
assert manager.data_folder == temp_data_folder
```
**Change to**:
```python
assert manager.config is not None
assert manager.player_manager is not None
# data_folder is not a public attribute - remove this assertion
```

### 3.2 Fix test_league_helper_loads_player_data_on_init
**Line**: 105
**Current**:
```python
players = manager.player_manager.get_all_players()
```
**Change to**:
```python
players = manager.player_manager.get_player_list(drafted_vals=[0, 1, 2])  # All players
```

### 3.3 Fix test_league_helper_loads_team_data_on_init
**Line**: 115
**Current**:
```python
teams = manager.team_data_manager.get_all_teams()
```
**Change to**:
```python
teams = manager.team_data_manager.get_available_teams()
```

### 3.4 Fix test_add_to_roster_mode_can_be_entered
**Line**: 128
**Pattern**: Check that `manager.add_to_roster_mode_manager` exists (not null)

### 3.5 Fix test_add_to_roster_workflow_adds_player
**Line**: 141
**Update**: Replace `get_all_players()` → `get_player_list(drafted_vals=[0, 1, 2])`

### 3.6 Fix test_starter_helper_mode_can_be_entered
**Line**: 158
**Pattern**: Check that `manager.starter_helper_mode_manager` exists

### 3.7 Fix test_trade_simulator_mode_can_be_entered
**Line**: 177
**Pattern**: Check that `manager.trade_simulator_mode_manager` exists

### 3.8 Fix test_modify_player_data_mode_can_be_entered
**Line**: 193
**Pattern**: Check that `manager.modify_player_data_mode_manager` exists

### 3.9 Fix test_transition_from_add_to_roster_to_starter_helper
**Line**: 212
**Update**: Replace any `get_all_players()` → `get_player_list(drafted_vals=[0, 1, 2])`

### 3.10 Fix test_transition_from_add_to_roster_to_trade_simulator
**Line**: 225
**Update**: Replace any `get_all_players()` → `get_player_list(drafted_vals=[0, 1, 2])`

### 3.11 Fix test_player_data_persists_across_mode_transitions
**Line**: 239
**Update**: Replace `get_all_players()` → `get_player_list(drafted_vals=[0, 1, 2])`

### 3.12 Fix test_team_data_persists_across_mode_transitions
**Line**: 254
**Update**: Replace `get_all_teams()` → `get_available_teams()`

### 3.13 Validation
**Command**: `python -m pytest tests/integration/test_league_helper_integration.py -v`
**Expected**: All 17 tests pass

---

## Phase 4: Fix test_simulation_integration.py

**Status**: PENDING
**File**: `tests/integration/test_simulation_integration.py` (300 lines, 16 test methods)
**Issue**: Config format mismatch - tests expect old nested format

### 4.1 Fix baseline_config Fixture
**Lines**: ~60-75
**Current** (creates WRONG format):
```python
@pytest.fixture
def baseline_config(tmp_path):
    config = {
        "config_name": "Test Config",
        "parameters": {  # WRONG - this nesting doesn't exist
            "projected_points_multiplier": 1.0
        }
    }
    ...
```
**Change to** (create CORRECT format):
```python
@pytest.fixture
def baseline_config(tmp_path):
    config = {
        "config_name": "Test Config",
        "description": "Test configuration",
        "parameters": {
            "CURRENT_NFL_WEEK": 1,
            "NFL_SEASON": 2024,
            "NFL_SCORING_FORMAT": "ppr",
            "NORMALIZATION_MAX_SCALE": 150.0,
            "BASE_BYE_PENALTY": 50.0,
            "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 0.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 100},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 60.0, "SECONDARY": 70.0},
            "DRAFT_ORDER": [],  # Simplified for testing
            "ADP_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 40.0},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": 1.0
            },
            # Add other required sections...
        }
    }
    config_path = tmp_path / "baseline_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f)
    return config_path
```

### 4.2 Fix test_config_generator_loads_baseline
**Line**: 87
**Update**: Test should now pass with correct config format from 4.1

### 4.3 Fix test_config_generator_creates_combinations
**Line**: 93
**Update**: Test should now pass with correct config format from 4.1

### 4.4 Fix test_config_dict_has_required_fields
**Line**: 102
**Update**: Verify against CORRECT fields (CURRENT_NFL_WEEK, NORMALIZATION_MAX_SCALE, etc.)

### 4.5 Fix test_simulation_manager_initializes
**Line**: 117
**Update**: Test should now pass with correct config format from 4.1

### 4.6 Fix test_simulation_manager_single_config_test
**Line**: 130
**Update**: Test should now pass with correct config format from 4.1

### 4.7 Fix test_parallel_runner_can_run_simulations
**Line**: 164
**Update**: Test should now pass with correct config format from 4.1

### 4.8 Fix test_config_performance_adds_results
**Line**: 248
**Current**:
```python
perf.add_result(wins=10, losses=4, points=1500.0)
```
**Change to**:
```python
perf.add_league_result(wins=10, losses=4, points=1500.0)
```

### 4.9 Fix test_config_performance_calculates_win_rate
**Line**: 264
**Current**:
```python
perf.add_result(wins=10, losses=4, points=1500.0)
```
**Change to**:
```python
perf.add_league_result(wins=10, losses=4, points=1500.0)
```

### 4.10 Fix test_complete_single_simulation_workflow
**Line**: 281
**Update**: Test should now pass with correct config format from 4.1

### 4.11 Validation
**Command**: `python -m pytest tests/integration/test_simulation_integration.py -v`
**Expected**: All 16 tests pass

---

## Phase 5: Final Validation & Cleanup

### 5.1 Run All Integration Tests
**Command**: `python -m pytest tests/integration/ -v`
**Expected**: All 34 tests pass (100%)

### 5.2 Run Full Test Suite
**Command**: `python tests/run_all_tests.py`
**Expected**: 1,820/1,820 tests pass (100%)

### 5.3 Update Code Changes Documentation
**File**: `updates/fix_integration_tests_code_changes.md`
**Action**: Document all changes made with file paths, line numbers, before/after

### 5.4 Update Specification Status
**File**: `updates/fix_integration_tests.txt`
**Action**: Update STATUS to COMPLETE

### 5.5 Move Files to Done
**Actions**:
- Move `updates/fix_integration_tests.txt` → `updates/done/`
- Move `updates/fix_integration_tests_code_changes.md` → `updates/done/`
- Delete `updates/fix_integration_tests_questions.md` (no longer needed)

---

## Success Criteria

✅ All 34 integration tests passing (100%)
✅ All 1,786 unit tests still passing (100%)
✅ Total: 1,820/1,820 tests passing
✅ No new warnings or errors
✅ Code changes documentation complete
✅ Files moved to updates/done/

---

## Progress Tracking

**Keep this section updated as you work through each phase!**

- [✅] Phase 1: API Research & Verification (COMPLETE)
- [ ] Phase 2: Fix test_data_fetcher_integration.py (0/8 tasks)
- [ ] Phase 3: Fix test_league_helper_integration.py (0/13 tasks)
- [ ] Phase 4: Fix test_simulation_integration.py (0/11 tasks)
- [ ] Phase 5: Final Validation & Cleanup (0/5 tasks)

**Current Phase**: Phase 2
**Last Updated**: 2025-10-18

---

## Notes

- All API research complete - actual methods documented
- pytest-asyncio already available (in requirements.txt)
- Async test pattern found in test_csv_utils.py
- Config format is flat (no nested structure)
- Unit tests prove implementation is correct (100% passing)
