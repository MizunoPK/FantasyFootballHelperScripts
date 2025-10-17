# Refactoring Investigation Summary

**Created**: 2025-10-17
**Purpose**: Critical findings for implementation reference

---

## Data Structures

### CSV Files

**players.csv** (27 columns):
```
id, name, team, position, bye_week, fantasy_points, injury_status, drafted, locked,
average_draft_position, player_rating,
week_1_points, week_2_points, ..., week_17_points
```

**teams.csv** (4 columns):
```
team, offensive_rank, defensive_rank, opponent
```

### Configuration Structure

**league_config.json** (complex nested JSON):
- `config_name`: String identifier
- `description`: Config description
- `parameters`: Object with:
  - `CURRENT_NFL_WEEK`: Integer (current week)
  - `NFL_SEASON`: Integer (year)
  - `NORMALIZATION_MAX_SCALE`: Float
  - `BASE_BYE_PENALTY`: Float
  - `DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY`: Float
  - `INJURY_PENALTIES`: {LOW, MEDIUM, HIGH}
  - `DRAFT_ORDER_BONUSES`: {PRIMARY, SECONDARY}
  - `DRAFT_ORDER`: Array of position priority objects
  - `ADP_SCORING`: {THRESHOLDS, MULTIPLIERS, WEIGHT}
  - `PLAYER_RATING_SCORING`: {THRESHOLDS, MULTIPLIERS, WEIGHT}
  - `TEAM_QUALITY_SCORING`: {THRESHOLDS, MULTIPLIERS, WEIGHT}
  - `PERFORMANCE_SCORING`: {MIN_WEEKS, THRESHOLDS, MULTIPLIERS, WEIGHT}
  - `CONSISTENCY_SCORING`: {MIN_WEEKS, THRESHOLDS, MULTIPLIERS, WEIGHT}
  - `MATCHUP_SCORING`: {THRESHOLDS, MULTIPLIERS, WEIGHT}

---

## Constants (from league_helper/constants.py)

### Position Limits
```python
MAX_POSITIONS = {
    QB: 2,
    RB: 4,
    WR: 4,
    FLEX: 1,
    TE: 2,
    K: 1,
    DST: 1
}
MAX_PLAYERS = 15
FLEX_ELIGIBLE_POSITIONS = [RB, WR, DST]
```

### Bye Weeks
```python
POSSIBLE_BYE_WEEKS = [5, 6, 7, 8, 9, 10, 11, 12, 14]
```

### Logging
```python
LOGGING_LEVEL = 'INFO'
LOGGING_TO_FILE = False
LOG_NAME = "league_helper"
RECOMMENDATION_COUNT = 10
```

---

## Dependency Graph

```
FantasyTeam
├── ConfigManager
├── LoggingManager
└── FantasyPlayer

PlayerManager
├── FantasyTeam (composition)
├── ConfigManager
├── TeamDataManager
├── ProjectedPointsManager
├── LoggingManager
└── FantasyPlayer

AddToRosterModeManager
├── ConfigManager
├── PlayerManager
├── TeamDataManager
├── ScoredPlayer
├── LoggingManager
└── FantasyPlayer

TeamDataManager
├── TeamData
└── LoggingManager
```

**Insight**: PlayerManager is central - depends on many modules and is depended upon by all mode managers.

---

## Test Fixture Patterns

### Common Fixtures (from test_PlayerManager_scoring.py)

```python
@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with test config and data files"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create league_config.json
    config_file = data_folder / "league_config.json"
    config_file.write_text(config_content)

    # Create teams.csv
    teams_file = data_folder / "teams.csv"
    teams_file.write_text(teams_content)

    # Create players.csv
    players_file = data_folder / "players.csv"
    players_file.write_text(players_content)

    return data_folder

@pytest.fixture
def config_manager(mock_data_folder):
    """Create ConfigManager with test configuration"""
    return ConfigManager(mock_data_folder)

@pytest.fixture
def mock_fantasy_team(config_manager):
    """Create mock FantasyTeam for testing"""
    team = Mock(spec=FantasyTeam)
    team.roster = []
    team.get_matching_byes_in_roster = Mock(return_value=0)
    return team
```

**Pattern**: Use tmp_path for file-based tests, Mock(spec=Class) for type-safe mocks

---

## Test Patterns & Best Practices

### Mock Patterns
```python
from unittest.mock import Mock, MagicMock, patch

# Type-safe mocking
team = Mock(spec=FantasyTeam)

# Method mocking
team.get_matching_byes_in_roster = Mock(return_value=0)

# Patching
@patch('league_helper.util.ProjectedPointsManager.Path')
def test_something(self, mock_path):
    pass
```

### Test Organization
```python
class TestFeatureName:
    """Test Feature Name functionality"""

    @pytest.fixture
    def local_fixture(self):
        """Fixture scoped to this test class"""
        return setup_object()

    def test_specific_behavior(self, local_fixture):
        """Test specific behavior with clear description"""
        result = local_fixture.method()
        assert result == expected
```

### Test Data Creation
```python
def test_player():
    """Create a test player with all attributes set"""
    player = FantasyPlayer(
        id=12345,
        name="Test Player",
        team="KC",
        position="RB",
        bye_week=7,
        fantasy_points=200.0,
        # ... all required fields
    )

    # Set weekly points for consistency calculation
    player.week_1_points = 18.5
    player.week_2_points = 22.0
    # ... etc

    return player
```

---

## Existing Test Coverage by File

| File | Test File | Test Count | Coverage Quality |
|------|-----------|------------|------------------|
| PlayerManager | test_PlayerManager_scoring.py | 62 | Excellent - comprehensive |
| ConfigManager | test_ConfigManager_thresholds.py | 26 | Good - thresholds covered |
| DraftedDataWriter | test_DraftedDataWriter.py | 24 | Good |
| ProjectedPointsManager | test_ProjectedPointsManager.py | 13 | Adequate |
| ScoredPlayer | test_ScoredPlayer.py | 17 | Good |
| player_search | test_player_search.py | 33 | Good |
| StarterHelperModeManager | test_StarterHelperModeManager.py | 24 | Good |
| TradeSimulator | test_trade_simulator.py | 41 | Good |
| TradeSimulator (manual) | test_manual_trade_visualizer.py | 39 | Good |
| ModifyPlayerData | test_modify_player_data_mode.py | 20 | Good |
| ConfigGenerator | test_config_generator.py | 23 | Good |
| SimulationManager | test_simulation_manager.py | 18 | Adequate |
| FantasyPlayer | test_FantasyPlayer.py | 4 | Minimal |
| **MISSING** | test_FantasyTeam.py | 0 | **NONE** |
| **MISSING** | test_TeamDataManager.py | 0 | **NONE** |
| **MISSING** | test_AddToRosterModeManager.py | 0 | **NONE** |

---

## Python Dependencies (requirements.txt)

```
# HTTP clients
httpx>=0.24.0                       # Modern async HTTP (primary)

# Data validation
pydantic>=2.0.0                     # Type checking and validation
pydantic-settings>=2.0.0            # Configuration management

# Async operations
tenacity>=8.2.0                     # Retry logic
aiofiles>=23.0.0                    # Async file I/O

# Configuration
python-dotenv>=1.0.0                # Environment variables

# Data processing
pandas>=2.0.0                       # Data manipulation and CSV/Excel

# Testing (implied)
pytest                              # Test framework
```

**Note**: Python 3.13.6+ compatible

---

## Code Quality Observations

### Well-Implemented Patterns ✅
1. **Error handling**: error_handler.py provides decorators and context managers
2. **CSV operations**: csv_utils.py consolidates all CSV operations
3. **Logging**: LoggingManager.py centralizes logging configuration
4. **Type hints**: Extensive use throughout (Good, Optional, Union, etc.)
5. **Docstrings**: ConfigManager shows excellent Google-style docstrings
6. **Test fixtures**: Comprehensive fixture library in test_PlayerManager_scoring.py

### Areas Needing Improvement ⚠️
1. **Print statements**: 177 found (should use logging)
2. **Error handling**: PlayerManager has only 3 try blocks (needs more)
3. **Docstring consistency**: Missing Raises sections in some files
4. **Import organization**: AddToRosterModeManager needs cleanup
5. **Missing tests**: FantasyTeam (748 lines!), TeamDataManager, AddToRosterModeManager

---

## Key Implementation Insights

### For FantasyTeam Tests
- Mock ConfigManager with roster limits
- Create test players with all 27 CSV fields
- Test FLEX assignment logic thoroughly (complex)
- Test slot_assignments dict tracking
- Test bye_week_counts dict tracking
- Mock logger to avoid actual logging during tests

### For TeamDataManager Tests
- Use tmp_path to create test teams.csv
- Mock teams.csv with various team rankings
- Test matchup calculations (rank differences)
- Test missing data scenarios

### For AddToRosterModeManager Tests
- Mock PlayerManager, ConfigManager, TeamDataManager
- Mock user input for interactive testing
- Test draft recommendation logic
- Test round matching algorithm
- Test roster display formatting

### For Integration Tests
- Test full workflow: draft → starter helper → trade simulator
- Test data persistence between mode switches
- Test CSV updates propagating correctly
- Test error recovery scenarios

---

## Common Test Data Templates

### Minimal Config Template
```python
config_content = """{
  "config_name": "Test Config",
  "parameters": {
    "CURRENT_NFL_WEEK": 6,
    "NORMALIZATION_MAX_SCALE": 100.0,
    "BASE_BYE_PENALTY": 25.0,
    "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 75},
    "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
    "DRAFT_ORDER": [{"FLEX": "P", "QB": "S"}],
    "ADP_SCORING": {"THRESHOLDS": {...}, "MULTIPLIERS": {...}, "WEIGHT": 1.0}
  }
}"""
```

### Minimal Teams Data
```python
teams_content = """team,offensive_rank,defensive_rank,opponent
KC,1,5,LV
BUF,2,3,MIA
PHI,3,8,NYG"""
```

### Minimal Players Data
```python
players_content = """id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,average_draft_position,player_rating,week_1_points,...
12345,Test Player,KC,RB,7,200.0,ACTIVE,0,0,15.0,85.0,18.5,..."""
```

---

## Testing Anti-Patterns to Avoid

❌ **Don't**:
- Use actual CSV files (use tmp_path)
- Hard-code file paths
- Test multiple concerns in one test
- Use print() for debugging (use logger or pytest -s)
- Create tests without clear descriptions

✅ **Do**:
- Use fixtures for reusable test data
- Mock external dependencies
- Test one concern per test method
- Use descriptive test names
- Group related tests in classes

---

## Reference: 9-Step Scoring System

From PlayerManager (for understanding tests):

1. **Normalization**: weighted_projection (fantasy_points / max_projection * 100)
2. **ADP Multiplier**: Based on average draft position thresholds
3. **Player Rating Multiplier**: Based on player rating thresholds
4. **Team Quality Multiplier**: Based on team offensive/defensive rank
5. **Performance Multiplier**: (Not consistency) - actual vs projected
6. **Matchup Multiplier**: Based on opponent matchup differential
7. **Draft Order Bonus**: PRIMARY/SECONDARY bonuses for current round
8. **Bye Week Penalty**: Same-position and different-position overlaps
9. **Injury Penalty**: LOW/MEDIUM/HIGH based on injury status

**Flags**: adp, player_rating, team_quality, performance, matchup, draft_round, bye, injury

---

## Questions Answered ✅

1. **CSV structure?** → 27 columns for players, 4 for teams
2. **Test fixture patterns?** → tmp_path + Mock(spec=Class) + comprehensive fixtures
3. **Configuration complexity?** → Highly nested JSON with ~10 scoring sections
4. **Constants?** → Well-organized in constants.py
5. **Dependencies?** → Clear graph, PlayerManager is central
6. **Mock patterns?** → unittest.mock with Mock/MagicMock/patch
7. **Data flow?** → CSV → Manager → Mode Manager → User
8. **Existing test quality?** → Generally excellent (62 tests just for PlayerManager!)

---

## Ready for Implementation

All critical information gathered. Key takeaways:

1. **Follow existing patterns** - test_PlayerManager_scoring.py is the gold standard
2. **Use tmp_path for all file tests** - never use real data files
3. **Mock extensively** - all managers can be mocked with Mock(spec=Class)
4. **Comprehensive fixtures** - create reusable fixtures for common test data
5. **Test one thing at a time** - clear test names, focused assertions
6. **Edge cases matter** - None values, zero values, boundary conditions

**No further investigation needed - ready to begin Phase 1 implementation!**
