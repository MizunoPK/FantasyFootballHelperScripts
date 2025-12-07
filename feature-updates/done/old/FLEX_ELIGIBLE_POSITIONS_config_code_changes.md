# FLEX_ELIGIBLE_POSITIONS Config Migration - Code Changes Tracker

**Objective**: Move FLEX_ELIGIBLE_POSITIONS constant from constants.py to league_config.json

**Status**: Ready for implementation

**Reference Files**:
- Update request: `updates/FLEX_ELIGIBLE_POSITIONS_config.txt`
- Questions: `updates/FLEX_ELIGIBLE_POSITIONS_config_questions.md`
- TODO: `updates/todo-files/flex_eligible_positions_config_todo.md`

---

## ⚠️ IMPORTANT BEHAVIOR CHANGE

**Old value** (constants.py): `['RB', 'WR', 'TE', 'DST']`
**New value** (config): `['RB', 'WR']`

**Impact**:
- TE will NO LONGER be FLEX-eligible
- DST will NO LONGER be FLEX-eligible
- This fixes a bug where constants.py had the wrong value
- FantasyPlayer.py already had the correct value

---

## Phase 1: Configuration System Changes

### File 1: data/league_config.json
**Action**: Add FLEX_ELIGIBLE_POSITIONS parameter

**Change**:
```json
{
  "parameters": {
    ...
    "MAX_POSITIONS": {
      "QB": 2,
      "RB": 4,
      "WR": 4,
      "FLEX": 2,
      "TE": 1,
      "K": 1,
      "DST": 1
    },
    "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],  // ← ADD THIS
    ...
  }
}
```

**Line**: After MAX_POSITIONS (estimate ~line 70)
**Status**: [ ] Not started

---

### File 2: league_helper/util/ConfigManager.py

#### Change 2.1: Add ConfigKeys constant
**Location**: ConfigKeys class (~line 50-65)

**Change**:
```python
class ConfigKeys:
    ...
    FLEX_ELIGIBLE_POSITIONS = "FLEX_ELIGIBLE_POSITIONS"  // ← ADD THIS
    ...
```

**Status**: [ ] Not started

---

#### Change 2.2: Add instance attribute
**Location**: __init__ method (~line 185)

**Change**:
```python
def __init__(self, data_folder: Union[str, Path]) -> None:
    ...
    self.max_positions: Dict[str, int] = {}
    self.flex_eligible_positions: List[str] = []  // ← ADD THIS
    ...
```

**Status**: [ ] Not started

---

#### Change 2.3: Add to required parameters
**Location**: _extract_parameters method (~line 685)

**Change**:
```python
def _extract_parameters(self) -> None:
    ...
    required_params = [
        ...
        self.keys.MAX_POSITIONS,
        self.keys.FLEX_ELIGIBLE_POSITIONS,  // ← ADD THIS
        ...
    ]
```

**Status**: [ ] Not started

---

#### Change 2.4: Extract parameter value
**Location**: _extract_parameters method (~line 729)

**Change**:
```python
def _extract_parameters(self) -> None:
    ...
    self.max_positions = self.parameters[self.keys.MAX_POSITIONS]
    self.flex_eligible_positions = self.parameters[self.keys.FLEX_ELIGIBLE_POSITIONS]  // ← ADD THIS
    ...
```

**Status**: [ ] Not started

---

#### Change 2.5: Add validation
**Location**: _extract_parameters method (~line 776, after max_positions validation)

**Change**:
```python
# Validate FLEX_ELIGIBLE_POSITIONS structure
if not isinstance(self.flex_eligible_positions, list):
    error_msg = f"FLEX_ELIGIBLE_POSITIONS must be a list, got: {type(self.flex_eligible_positions).__name__}"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

if len(self.flex_eligible_positions) == 0:
    error_msg = "FLEX_ELIGIBLE_POSITIONS must contain at least one position"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

# Validate no circular reference (FLEX can't be in FLEX_ELIGIBLE_POSITIONS)
if 'FLEX' in self.flex_eligible_positions:
    error_msg = "FLEX_ELIGIBLE_POSITIONS cannot contain 'FLEX' (circular reference)"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

# Validate all positions are valid
valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
invalid_positions = [pos for pos in self.flex_eligible_positions if pos not in valid_positions]
if invalid_positions:
    error_msg = f"FLEX_ELIGIBLE_POSITIONS contains invalid positions: {', '.join(invalid_positions)}"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

# Log successful validation
self.logger.debug(f"FLEX_ELIGIBLE_POSITIONS validated: {', '.join(self.flex_eligible_positions)}")
```

**Status**: [ ] Not started

---

#### Change 2.6: Add get_position_with_flex method
**Location**: ConfigManager class (after max_players property ~line 205)

**Change**:
```python
def get_position_with_flex(self, position: str) -> str:
    """
    Determine if a position should be considered for FLEX assignment.

    In fantasy football, certain positions (typically RB/WR) can fill FLEX slots.
    This method checks if a given position is FLEX-eligible according to the
    league configuration.

    Args:
        position: Player's natural position (QB, RB, WR, TE, K, DST)

    Returns:
        'FLEX' if position is in flex_eligible_positions, otherwise the original position

    Example:
        >>> config.get_position_with_flex('RB')
        'FLEX'
        >>> config.get_position_with_flex('QB')
        'QB'
    """
    if position in self.flex_eligible_positions:
        return 'FLEX'
    else:
        return position
```

**Status**: [ ] Not started

---

## Phase 2: Production Code Updates

### File 3: league_helper/util/FantasyTeam.py

**Total Changes**: 7 lines

#### Change 3.1: Line 114
**From**: `pos_with_flex = Constants.FLEX if pos in Constants.FLEX_ELIGIBLE_POSITIONS else pos`
**To**: `pos_with_flex = Constants.FLEX if pos in self.config.flex_eligible_positions else pos`
**Status**: [ ] Not started

#### Change 3.2: Line 411
**From**: `if pos not in Constants.FLEX_ELIGIBLE_POSITIONS:`
**To**: `if pos not in self.config.flex_eligible_positions:`
**Status**: [ ] Not started

#### Change 3.3: Line 507
**From**: `if pos not in Constants.FLEX_ELIGIBLE_POSITIONS:`
**To**: `if pos not in self.config.flex_eligible_positions:`
**Status**: [ ] Not started

#### Change 3.4: Line 764
**From**: `elif (pos in Constants.FLEX_ELIGIBLE_POSITIONS and`
**To**: `elif (pos in self.config.flex_eligible_positions and`
**Status**: [ ] Not started

#### Change 3.5: Line 820
**From**: `if (old_player.position in Constants.FLEX_ELIGIBLE_POSITIONS and`
**To**: `if (old_player.position in self.config.flex_eligible_positions and`
**Status**: [ ] Not started

#### Change 3.6: Line 821
**From**: `new_player.position in Constants.FLEX_ELIGIBLE_POSITIONS):`
**To**: `new_player.position in self.config.flex_eligible_positions):`
**Status**: [ ] Not started

#### Change 3.7: Line 849
**From**: `elif (new_pos in Constants.FLEX_ELIGIBLE_POSITIONS and`
**To**: `elif (new_pos in self.config.flex_eligible_positions and`
**Status**: [ ] Not started

---

### File 4: league_helper/constants.py

#### Change 4.1: Remove FLEX_ELIGIBLE_POSITIONS constant
**Location**: Line 64
**Action**: DELETE entire line and comment above it

**From**:
```python
# Positions eligible for FLEX spot (RB or WR only)
FLEX_ELIGIBLE_POSITIONS = [RB, WR, TE, DST]
```

**To**: (removed)

**Status**: [ ] Not started

---

#### Change 4.2: Remove get_position_with_flex function
**Location**: Lines 66-85
**Action**: DELETE entire function (moving to ConfigManager)

**From**:
```python
def get_position_with_flex(position):
    """
    Determine if a position should be considered for FLEX assignment.
    ...
    """
    if position in FLEX_ELIGIBLE_POSITIONS:
        return FLEX
    else:
        return position
```

**To**: (removed - moved to ConfigManager)

**Status**: [ ] Not started

---

#### Change 4.3: Update module docstring
**Location**: Lines 7-9
**Action**: Remove mention of FLEX_ELIGIBLE_POSITIONS

**From**:
```python
"""
...
- MAX_POSITIONS: Position limits (moved to config) - DEPRECATED
- FLEX_ELIGIBLE_POSITIONS: Positions eligible for FLEX slots
...
"""
```

**To**:
```python
"""
...
- MAX_POSITIONS: Position limits (moved to config) - DEPRECATED
- FLEX_ELIGIBLE_POSITIONS: FLEX-eligible positions (moved to config) - DEPRECATED
...
"""
```

**Status**: [ ] Not started

---

### File 5: utils/FantasyPlayer.py

#### Change 5.1: Update local definition comment
**Location**: Line 418
**Action**: Update comment to clarify this matches config

**From**:
```python
# FLEX eligible positions: RB and WR only
# QB, TE, K, DEF are NOT FLEX eligible
FLEX_ELIGIBLE_POSITIONS = ['RB', 'WR']
```

**To**:
```python
# FLEX eligible positions: RB and WR only
# This hardcoded value matches FLEX_ELIGIBLE_POSITIONS in league_config.json
# Kept hardcoded to avoid adding config dependency to FantasyPlayer data class
# QB, TE, K, DEF are NOT FLEX eligible
FLEX_ELIGIBLE_POSITIONS = ['RB', 'WR']
```

**Status**: [ ] Not started

---

## Phase 3: Test Updates

### File 6: tests/league_helper/util/test_ConfigManager_flex_eligible_positions.py

**Action**: CREATE new test file

**Content**: See full test file below

**Status**: [ ] Not started

<details>
<summary>Full Test File Content (Click to expand)</summary>

```python
"""
Unit Tests for ConfigManager FLEX_ELIGIBLE_POSITIONS Configuration

Tests the loading, validation, and usage of FLEX_ELIGIBLE_POSITIONS parameter.

Author: Kai Mizuno
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock

import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from league_helper.util.ConfigManager import ConfigManager


@pytest.fixture
def temp_data_folder(tmp_path):
    """Create temporary data folder for testing."""
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    return data_folder


@pytest.fixture
def minimal_config():
    """Minimal valid configuration for testing."""
    return {
        "config_name": "test",
        "description": "test config",
        "parameters": {
            "CURRENT_NFL_WEEK": 1,
            "NFL_SEASON": 2025,
            "NFL_SCORING_FORMAT": "ppr",
            "NORMALIZATION_MAX_SCALE": 100.0,
            "BASE_BYE_PENALTY": 25.0,
            "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 5.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 75},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
            "DRAFT_ORDER": [{"FLEX": "P"}],
            "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
            "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
            "ADP_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 35},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "TEAM_QUALITY_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "PERFORMANCE_SCORING": {
                "MIN_WEEKS": 3,
                "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.15},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "MATCHUP_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 6},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            }
        }
    }


class TestFlexEligiblePositionsLoading:
    """Test loading FLEX_ELIGIBLE_POSITIONS from config."""

    def test_flex_eligible_positions_loads_from_config(self, temp_data_folder, minimal_config):
        """Test that flex_eligible_positions attribute is populated from config."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert hasattr(config, 'flex_eligible_positions')
        assert config.flex_eligible_positions == ["RB", "WR"]

    def test_flex_eligible_positions_is_list(self, temp_data_folder, minimal_config):
        """Test that flex_eligible_positions is a list type."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert isinstance(config.flex_eligible_positions, list)


class TestFlexEligiblePositionsValidation:
    """Test validation of FLEX_ELIGIBLE_POSITIONS parameter."""

    def test_flex_eligible_positions_missing_raises_error(self, temp_data_folder, minimal_config):
        """Test that missing FLEX_ELIGIBLE_POSITIONS raises ValueError."""
        del minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="FLEX_ELIGIBLE_POSITIONS"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_empty_list_raises_error(self, temp_data_folder, minimal_config):
        """Test that empty FLEX_ELIGIBLE_POSITIONS list raises ValueError."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = []
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="must contain at least one position"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_not_list_raises_error(self, temp_data_folder, minimal_config):
        """Test that non-list FLEX_ELIGIBLE_POSITIONS raises ValueError."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = "RB,WR"  # string instead of list
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="must be a list"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_contains_flex_raises_error(self, temp_data_folder, minimal_config):
        """Test that FLEX in FLEX_ELIGIBLE_POSITIONS raises ValueError (circular reference)."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["RB", "WR", "FLEX"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="cannot contain 'FLEX'"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_invalid_position_raises_error(self, temp_data_folder, minimal_config):
        """Test that invalid position in FLEX_ELIGIBLE_POSITIONS raises ValueError."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["RB", "INVALID"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="invalid positions"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_all_valid_positions_allowed(self, temp_data_folder, minimal_config):
        """Test that all valid positions are accepted."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["QB", "RB", "WR", "TE", "K", "DST"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert len(config.flex_eligible_positions) == 6


class TestGetPositionWithFlexMethod:
    """Test the get_position_with_flex() method."""

    def test_rb_returns_flex(self, temp_data_folder, minimal_config):
        """Test that RB position returns FLEX when RB is flex-eligible."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('RB') == 'FLEX'

    def test_wr_returns_flex(self, temp_data_folder, minimal_config):
        """Test that WR position returns FLEX when WR is flex-eligible."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('WR') == 'FLEX'

    def test_qb_returns_qb(self, temp_data_folder, minimal_config):
        """Test that QB position returns QB when QB is not flex-eligible."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('QB') == 'QB'

    def test_te_returns_te(self, temp_data_folder, minimal_config):
        """Test that TE position returns TE when TE is not flex-eligible."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('TE') == 'TE'

    def test_te_returns_flex_when_configured(self, temp_data_folder, minimal_config):
        """Test that TE returns FLEX when TE is added to flex_eligible_positions."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["RB", "WR", "TE"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('TE') == 'FLEX'


class TestFlexEligiblePositionsEdgeCases:
    """Test edge cases for FLEX_ELIGIBLE_POSITIONS."""

    def test_single_position_allowed(self, temp_data_folder, minimal_config):
        """Test that a single position in list is valid."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["RB"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.flex_eligible_positions == ["RB"]

    def test_all_positions_except_flex_allowed(self, temp_data_folder, minimal_config):
        """Test that all positions except FLEX can be flex-eligible."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["QB", "RB", "WR", "TE", "K", "DST"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert len(config.flex_eligible_positions) == 6
        assert "FLEX" not in config.flex_eligible_positions


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

</details>

---

### File 7: tests/league_helper/test_constants.py

#### Change 7.1: Update test_flex_eligible_positions_are_correct
**Location**: Lines 118-121
**Action**: Update to reference config instead of constant (or remove if no longer applicable)

**Current**:
```python
def test_flex_eligible_positions_are_correct(self):
    """Test that FLEX_ELIGIBLE_POSITIONS contains RB, WR, DST."""
    assert constants.RB in constants.FLEX_ELIGIBLE_POSITIONS
    assert constants.WR in constants.FLEX_ELIGIBLE_POSITIONS
    assert constants.DST in constants.FLEX_ELIGIBLE_POSITIONS
```

**Options**:
- **A**: Remove test entirely (constant no longer exists)
- **B**: Update to verify config loading (but that's covered in new test file)

**Recommended**: Remove test (covered by new ConfigManager test file)

**Status**: [ ] Not started

---

#### Change 7.2: Update test_flex_eligible_does_not_contain_flex_itself
**Location**: Lines 124-125
**Action**: Remove (covered by ConfigManager validation test)

**Status**: [ ] Not started

---

#### Change 7.3: Update test_flex_eligible_contains_only_valid_positions
**Location**: Lines 128-130
**Action**: Remove (covered by ConfigManager validation test)

**Status**: [ ] Not started

---

#### Change 7.4: Update test_get_position_with_flex tests
**Location**: Lines 192-211
**Action**: Update to call config.get_position_with_flex() instead of constants.get_position_with_flex()

**Current**:
```python
def test_tight_end_returns_correct_value(self):
    """Test that TE position returns FLEX if flex-eligible, otherwise TE."""
    result = constants.get_position_with_flex('TE')
    if constants.TE in constants.FLEX_ELIGIBLE_POSITIONS:
        assert result == constants.FLEX
    else:
        assert result == 'TE'
```

**Updated**:
```python
def test_tight_end_returns_te(self, mock_config):
    """Test that TE position returns TE when not flex-eligible."""
    mock_config.flex_eligible_positions = ['RB', 'WR']
    result = mock_config.get_position_with_flex('TE')
    assert result == 'TE'
```

**Status**: [ ] Not started

---

### File 8: Update test mocks (PROACTIVE)

**Files to update**: ~13 test files that mock ConfigManager

**Change**: Add `flex_eligible_positions` attribute to all config mocks

**Standard addition**:
```python
mock_config.flex_eligible_positions = ['RB', 'WR']
```

**Files identified** (from MAX_POSITIONS migration):
1. tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py
2. tests/league_helper/util/test_PlayerManager_scoring.py
3. tests/league_helper/trade_simulator_mode/test_trade_analyzer.py
4. tests/league_helper/trade_simulator_mode/test_trade_simulator.py
5. tests/simulation/test_SimulatedLeague.py
6. tests/simulation/test_manual_simulation.py
7. tests/league_helper/test_LeagueHelperManager.py
8. tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py
9. tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py
10. tests/league_helper/util/test_ProjectedPointsManager.py
11. tests/simulation/test_DraftHelperTeam.py
12. tests/simulation/test_ParallelLeagueRunner.py
13. tests/simulation/test_simulation_manager.py

**Status**: [ ] Not started (will be done in batch)

---

## Summary Statistics

**Total Files Modified**: 8+ files (5 production + 3+ test files + ~13 test mock updates)
**Total Code Changes**: ~30 changes
**Lines Added**: ~120 lines (validation + new method + tests)
**Lines Removed**: ~20 lines (removed constant + function)
**Net Change**: ~+100 lines

**Breakdown by Phase**:
- Phase 1 (Config System): 6 changes across 2 files
- Phase 2 (Production Code): 11 changes across 3 files
- Phase 3 (Tests): 13+ changes across 3+ files + 1 new file

**Risk Level**: 🟡 MEDIUM
- Behavior change (TE/DST no longer FLEX-eligible)
- 22 total references to update
- Function migration to ConfigManager
- Extensive test updates required

**Similar to**: MAX_POSITIONS migration (completed successfully)

---

## Implementation Checklist

### Pre-Implementation
- [x] User decisions confirmed
- [x] Questions answered
- [x] TODO file created
- [x] Code changes documented
- [ ] All existing tests passing (baseline: 1851/1851)

### Phase 1: Configuration
- [ ] Task 1.1: Add to league_config.json
- [ ] Task 1.2: Add ConfigKeys constant
- [ ] Task 1.3: Add instance attribute
- [ ] Task 1.4: Add to required parameters
- [ ] Task 1.5: Extract parameter value
- [ ] Task 1.6: Add validation
- [ ] Task 1.6b: Add get_position_with_flex method
- [ ] Verify config loads without errors

### Phase 2: Production Code
- [ ] Task 2.1: Update FantasyTeam.py (7 changes)
- [ ] Task 2.2: Move get_position_with_flex to ConfigManager
- [ ] Task 2.3: Update FantasyPlayer.py comment
- [ ] Task 2.4: Remove from constants.py
- [ ] Verify no Constants.FLEX_ELIGIBLE_POSITIONS references remain

### Phase 3: Tests
- [ ] Task 3.1: Create test_ConfigManager_flex_eligible_positions.py
- [ ] Task 3.2: Update test_constants.py
- [ ] Task 3.3: Update all config mocks (~13 files)
- [ ] Verify all tests pass (target: 1851/1851)

### Phase 4: Validation
- [ ] Run all unit tests (must be 100%)
- [ ] Manual testing of FLEX slot assignment
- [ ] Verify TE/DST no longer FLEX-eligible
- [ ] Test with different FLEX_ELIGIBLE_POSITIONS values

### Post-Implementation
- [ ] Update CLAUDE.md if needed
- [ ] Update README.md if needed
- [ ] Commit changes
- [ ] Move update file to updates/done/

---

## Notes

- Following same pattern as successful MAX_POSITIONS migration
- FantasyPlayer.py hardcoded value is intentional (avoids config dependency)
- get_position_with_flex() moved to ConfigManager for consistency
- Behavior change is intentional (bug fix)
