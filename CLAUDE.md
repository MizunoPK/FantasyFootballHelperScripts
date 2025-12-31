# Fantasy Football Helper Scripts - Claude Code Guidelines

## Quick Start for New Agents

**FIRST**: Read `ARCHITECTURE.md` for complete architectural overview, system design, and implementation details.

**SECOND**: Read `README.md` for project overview, installation instructions, and usage guide.

**THIS FILE**: Contains workflow rules, coding standards, and commit protocols.

---

## Project-Specific Rules

### Epic-Driven Development Workflow (v2)

**Complete workflow instructions:** See `CLAUDE_EPICS.md` for all Epic-Driven Development Workflow instructions.

**Quick reference:**
- Complete usage guide: `feature-updates/guides_v2/EPIC_WORKFLOW_USAGE.md`
- Stage guides: `feature-updates/guides_v2/STAGE_*_guide.md`
- Phase transition prompts: `feature-updates/guides_v2/prompts_reference_v2.md`

**For new epics:** User creates `{epic_name}.txt` → Agent starts Stage 1

**For resuming work:** Check `feature-updates/` for in-progress epics → Read `EPIC_README.md` Agent Status

**See CLAUDE_EPICS.md for:**
- Complete 7-stage workflow
- Mandatory phase transition protocol
- Stage-by-stage instructions
- Bug fix workflow
- Key principles and critical rules
- Folder structure
- Pre-commit protocol

---

**All detailed workflow instructions have been moved to `CLAUDE_EPICS.md` for better organization and portability.**

---

### Commit Standards & Pre-Commit Protocol

**See `CLAUDE_EPICS.md` for complete pre-commit protocol and git branching workflow.**

**Quick reference:**

**Git branching workflow:**
- All epic work done on feature branches (not main)
- Branch naming: `{work_type}/KAI-{number}` (e.g., `epic/KAI-1`)
- Work types: `epic` (multi-feature), `feat` (single feature), `fix` (bug fix)
- KAI numbers tracked in `feature-updates/EPIC_TRACKER.md`
- See `CLAUDE_EPICS.md` "Git Branching Workflow" section for complete instructions

**Commit message standards:**
- Format: `{commit_type}/KAI-{number}: {message}`
- commit_type: `feat` or `fix`
- Brief, descriptive messages (100 chars or less for first line)
- No emojis or subjective prefixes
- Do NOT include "Generated with Claude Code" and co-author tag
- List major changes in body
- Example: `feat/KAI-1: Add ADP integration to PlayerManager`

**Pre-commit checklist:**
1. ✅ Verify on correct branch: `git branch` (should show epic/KAI-X)
2. ✅ Run unit tests: `python tests/run_all_tests.py`
3. ✅ Verify 100% pass rate (exit code 0)
4. ✅ Review changes: `git status` and `git diff`
5. ✅ Update documentation if functionality changed
6. ✅ Commit with new format: `{commit_type}/KAI-{number}: {message}`

**Critical rule:** Do NOT commit if any tests fail. Fix tests first, then retry.

## Current Project Structure

### Main Scripts (Root Level)
- `run_league_helper.py` - Main league helper application entry point
- `run_player_fetcher.py` - Fetch player projection data from APIs
- `run_scores_fetcher.py` - Fetch NFL scores and update team rankings
- `run_simulation.py` - Run simulation system (single/full/iterative modes)
- `run_pre_commit_validation.py` - Pre-commit test validation runner

### League Helper Module (`league_helper/`)
Main application with 4 interactive modes:

- `LeagueHelperManager.py` - Main controller, mode selection, data initialization
- **Mode Modules**:
  - `add_to_roster_mode/` - Draft helper mode
    - `AddToRosterModeManager.py` - Draft recommendation engine
    - `DraftRecommendation.py` - Recommendation data structure
  - `starter_helper_mode/` - Roster optimizer mode
    - `StarterHelperModeManager.py` - Lineup optimization engine
  - `trade_simulator_mode/` - Trade evaluation mode
    - `TradeSimulatorModeManager.py` - Trade analysis controller
    - `TradeSimTeam.py` - Team representation for trades
    - `TradeSnapshot.py` - Before/after trade comparison
    - `TradeFileWriter.py` - File export (txt and Excel) for trade analysis
  - `modify_player_data_mode/` - Player data editor mode
    - `ModifyPlayerDataModeManager.py` - Data modification interface
- **Utilities**:
  - `util/PlayerManager.py` - Player data management and scoring
  - `util/ConfigManager.py` - Configuration loading and access
  - `util/FantasyTeam.py` - Roster management and validation
  - `util/FantasyPlayer.py` - Player model with scoring logic
  - `util/TeamDataManager.py` - NFL team rankings and matchup data

### Simulation System (`simulation/`)
Parameter optimization through league simulation:

- `SimulationManager.py` - Main simulation controller (3 optimization modes)
- `ParallelLeagueRunner.py` - Multi-threaded league execution
- `ConfigGenerator.py` - Parameter combination generator
- `ResultsManager.py` - Results aggregation and best config tracking
- `ConfigPerformance.py` - Performance metrics for configurations
- `SimulatedLeague.py` - Single league simulation logic
- `DraftHelperTeam.py` - Team using DraftHelper system
- `SimulatedOpponent.py` - AI opponent team implementations
- `Week.py` - Weekly matchup simulation
- `sim_data/` - Simulation data files (separate from main data/)

### Data Fetchers
- `player-data-fetcher/` - Player projection data collection
  - `PlayerFetcher.py` - Main fetcher with async HTTP
  - `data_sources/` - API integrations (ESPN, etc.)
- `nfl-scores-fetcher/` - NFL game scores collection
  - `NFLScoresFetcher.py` - Scores fetcher and team ranking updates

### Shared Utilities (`utils/`)
- `LoggingManager.py` - Centralized logging configuration
- `error_handler.py` - Error handling utilities and context managers
- `csv_utils.py` - CSV I/O helpers with validation
- `FantasyPlayer.py` - Shared player model

### Tests (`tests/`) - 2,200+ Total Tests
Mirrors source structure with 100% unit test pass rate required:

- `run_all_tests.py` - Master test runner (REQUIRED before commits)
- `integration/` - 25 integration tests
  - `test_league_helper_integration.py` - League helper workflows
  - `test_data_fetcher_integration.py` - Data fetcher workflows
  - `test_simulation_integration.py` - Simulation workflows
- `league_helper/` - 1,000+ unit tests
  - `add_to_roster_mode/` - Draft mode tests
  - `starter_helper_mode/` - Optimizer tests
  - `trade_simulator_mode/` - Trade simulator tests
  - `modify_player_data_mode/` - Data editor tests
  - `util/` - Utility tests (PlayerManager, ConfigManager, etc.)
- `simulation/` - 500+ simulation system tests
- `player-data-fetcher/` - Player fetcher tests
- `nfl-scores-fetcher/` - Scores fetcher tests
- `utils/` - Shared utility tests
- `root_scripts/` - Root script wrapper tests (23 tests)
- `README.md` - Testing guidelines and standards

### Data Files (`data/`)
- `league_config.json` - League configuration (scoring, penalties, weights)
- `players.csv` - Player statistics and projections
- `teams_week_N.csv` - Weekly NFL team rankings (weeks 1-17)
- `drafted_players.csv` - Tracking drafted players during season

### Documentation (`docs/`)
- `docs/scoring/` - **Comprehensive scoring algorithm documentation** (10,469 lines, 328KB)
  - `README.md` - Scoring algorithm overview, flow diagram, mode usage, dependencies
  - `01_normalization.md` - Fantasy points normalization (Step 1)
  - `02_adp_multiplier.md` - Average Draft Position market wisdom (Step 2)
  - `03_player_rating_multiplier.md` - Expert consensus rankings (Step 3) **[RECENTLY UPDATED]**
  - `04_team_quality_multiplier.md` - Team offensive/defensive strength (Step 4)
  - `05_performance_multiplier.md` - Actual vs projected deviation (Step 5)
  - `06_matchup_multiplier.md` - Current opponent strength (Step 6)
  - `07_schedule_multiplier.md` - Future opponent strength (Step 7)
  - `08_draft_order_bonus.md` - Position-specific draft value (Step 8)
  - `09_bye_week_penalty.md` - Roster conflict penalty (Step 9)
  - `10_injury_penalty.md` - Injury risk assessment (Step 10)

### Configuration & Updates
- `feature-updates/` - Root folder for epic-driven development
  - `{epic_name}.txt` - Initial scratchwork from user (before Stage 1)
  - `{epic_name}/` - Epic folder (created during Stage 1)
    - **Epic-Level Files:**
      - `EPIC_README.md` - Master tracking with Quick Reference Card, Agent Status, Epic Progress Tracker
      - `epic_smoke_test_plan.md` - How to test complete epic (evolves: Stage 1 → 4 → 5e → 6)
      - `epic_lessons_learned.md` - Cross-feature patterns and systemic insights
    - **Feature Folders:**
      - `feature_01_{name}/` - Feature 1
        - `README.md` - Feature context and Agent Status
        - `spec.md` - **Primary specification** (detailed requirements)
        - `checklist.md` - Tracks resolved vs pending decisions
        - `todo.md` - Implementation tracking (created during Stage 5a)
        - `questions.md` - Questions for user (created during Stage 5a if needed)
        - `implementation_checklist.md` - Continuous spec verification (Stage 5b)
        - `code_changes.md` - Documentation of all changes (Stage 5b)
        - `lessons_learned.md` - Feature-specific insights
        - `research/` - Research documents (if needed)
      - `feature_02_{name}/` - Feature 2 (same structure)
      - `feature_03_{name}/` - Feature 3 (same structure)
    - **Bug Fix Folders (if any):**
      - `bugfix_{priority}_{name}/` - Bug fix folder
        - `notes.txt` - Issue description (user-verified)
        - `spec.md` - Fix requirements
        - `checklist.md` - Same as features
        - `todo.md` - Same as features
        - `implementation_checklist.md` - Same as features
        - `code_changes.md` - Same as features
        - `lessons_learned.md` - Same as features
- `feature-updates/done/` - Completed epic folders (moved here after Stage 7)
- `feature-updates/guides_v2/` - **v2 Workflow guides** (epic-driven development)
  - **Stage Guides (16 guides):**
    - `STAGE_1_epic_planning_guide.md` - Stage 1: Epic Planning
    - `STAGE_2_feature_deep_dive_guide.md` - Stage 2: Feature Deep Dives
    - `STAGE_3_cross_feature_sanity_check_guide.md` - Stage 3: Cross-Feature Sanity Check
    - `STAGE_4_epic_testing_strategy_guide.md` - Stage 4: Epic Testing Strategy
    - `STAGE_5aa_round1_guide.md` - Stage 5a Round 1: Iterations 1-7 + 4a
    - `STAGE_5ab_round2_guide.md` - Stage 5a Round 2: Iterations 8-16
    - `STAGE_5ac_round3_guide.md` - Stage 5a Round 3: Iterations 17-24 + 23a
    - `STAGE_5b_implementation_execution_guide.md` - Stage 5b: Implementation
    - `STAGE_5ca_smoke_testing_guide.md` - Stage 5c Phase 1: Smoke Testing
    - `STAGE_5cb_qc_rounds_guide.md` - Stage 5c Phase 2: QC Rounds
    - `STAGE_5cc_final_review_guide.md` - Stage 5c Phase 3: Final Review
    - `STAGE_5d_post_feature_alignment_guide.md` - Stage 5d: Cross-Feature Alignment
    - `STAGE_5e_post_feature_testing_update_guide.md` - Stage 5e: Testing Plan Update
    - `STAGE_5_bug_fix_workflow_guide.md` - Bug Fix Workflow
    - `STAGE_6_epic_final_qc_guide.md` - Stage 6: Epic-Level Final QC
    - `STAGE_7_epic_cleanup_guide.md` - Stage 7: Epic Cleanup
  - **Supporting Files (5 files):**
    - `EPIC_WORKFLOW_USAGE.md` - Complete usage guide (setup, patterns, FAQs)
    - `prompts_reference_v2.md` - MANDATORY phase transition prompts
    - `templates_v2.md` - File templates (epic, feature, bug fix)
    - `README.md` - Workflow overview and guide index
    - `PLAN.md` - Complete v2 workflow specification
- `CLAUDE.md` - This file (coding standards and workflow guidelines)
- `CLAUDE_EPICS.md` - Epic-Driven Development Workflow instructions (portable)
- `README.md` - Project documentation, installation, and usage guide
- `ARCHITECTURE.md` - Complete architectural and implementation guide

---

## Coding Standards & Conventions

### Import Organization
```python
# Standard library (alphabetical)
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party (alphabetical)
import pandas as pd
import pytest

# Local with sys.path manipulation
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer
```

**Rules**:
- Always use `Path` for file operations, not string concatenation
- Use `sys.path.append()` for relative imports between modules
- Type hints required for all public methods

### Error Handling
```python
from utils.error_handler import (
    FantasyFootballError,
    DataProcessingError,
    create_component_error_handler,
    error_context
)

# Use context managers for error tracking
with error_context("operation_name", component="module_name") as ctx:
    # Operations that might fail
    if error_condition:
        raise DataProcessingError("Error message", context=ctx)

# Always log errors before raising
try:
    risky_operation()
except SpecificError as e:
    self.logger.error(f"Operation failed: {e}")
    raise
```

### Logging Standards
```python
from utils.LoggingManager import setup_logger, get_logger

# Setup once (in main or __init__)
logger = setup_logger(name="module", level="INFO")

# Use in modules
logger = get_logger()

# Logging levels:
logger.debug(f"Detailed info: {value}")      # Diagnostic details
logger.info(f"Operation complete: {count}")  # Progress updates
logger.warning(f"Unexpected: {issue}")       # Recoverable issues
logger.error(f"Failed: {e}", exc_info=True)  # Serious problems
```

### Docstring Format (Google Style)
```python
def method_name(self, param1: Type, param2: Optional[Type] = None) -> ReturnType:
    """
    Brief one-line description.

    Longer description explaining behavior, edge cases, and important details.

    Args:
        param1 (Type): Description of parameter
        param2 (Optional[Type]): Description with default behavior

    Returns:
        ReturnType: Description of return value
            - Special case 1
            - Special case 2

    Raises:
        ErrorType: When this occurs

    Example:
        >>> result = obj.method_name(value)
        >>> print(result)
    """
```

### Type Hinting
```python
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path

# All public methods must have type hints
def process_data(
    filepath: Union[str, Path],
    options: Optional[Dict[str, Any]] = None
) -> Tuple[bool, str]:
    pass

# Use Optional for nullable values
def get_player(self, player_id: int) -> Optional[FantasyPlayer]:
    pass
```

### CSV Operations
```python
from utils.csv_utils import (
    read_csv_with_validation,
    write_csv_with_backup,
    safe_csv_read
)

# Always validate required columns
df = read_csv_with_validation(
    filepath,
    required_columns=['id', 'name', 'position'],
    encoding='utf-8'
)

# Use backup when writing critical data
write_csv_with_backup(df, filepath, create_backup=True)
```

### Configuration Access
```python
from util.ConfigManager import ConfigManager

# Single source of truth
config = ConfigManager(data_folder)

# Use helper methods for calculations
multiplier, rating = config.get_adp_multiplier(adp_val)
penalty = config.get_injury_penalty(risk_level)
```

### Naming Conventions
- **Classes**: `PascalCase` (PlayerManager, ConfigManager)
- **Functions/Methods**: `snake_case` (load_players, get_score)
- **Constants**: `UPPER_SNAKE_CASE` (RECOMMENDATION_COUNT, LOGGING_LEVEL)
- **Private**: `_leading_underscore` (_validate_config)
- **Modules**: `snake_case` (error_handler.py, csv_utils.py)

### Path Handling
```python
from pathlib import Path

# Always use Path objects
base_path = Path(__file__).parent
data_path = base_path / "data"
config_file = data_path / "league_config.json"

# Convert to string only when required
with open(str(config_file), 'r') as f:
    pass
```

### Testing Patterns
```python
# tests/module_path/test_FileName.py
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def test_object(tmp_path):
    """Create test instance with temp data"""
    return ClassUnderTest(tmp_path)

class TestFeatureName:
    """Test Feature Name functionality"""

    def test_feature_normal_case(self, test_object):
        """Test feature with normal inputs"""
        result = test_object.method()
        assert result == expected
```

**Testing Rules**:
- Test file structure mirrors source code structure
- Use fixtures for reusable test data
- Mock external dependencies (APIs, file systems)
- 100% pass rate required before commits
- See `tests/README.md` for complete guidelines

### Comprehensive Testing Standards

**Test Suite Overview** (2,200+ total tests):
- **Unit Tests**: 2,200+ tests (100% pass rate required)
- **Integration Tests**: 25 tests (cross-module workflow validation)
- **Test Coverage**: All major modules and functions

**Test Organization**:
```
tests/
├── integration/               # End-to-end workflow tests
│   ├── test_league_helper_integration.py
│   ├── test_data_fetcher_integration.py
│   └── test_simulation_integration.py
├── league_helper/            # League helper unit tests
│   ├── add_to_roster_mode/
│   ├── starter_helper_mode/
│   ├── trade_simulator_mode/
│   ├── modify_player_data_mode/
│   └── util/
├── simulation/               # Simulation system tests
├── player-data-fetcher/      # Player fetcher tests
├── nfl-scores-fetcher/       # Scores fetcher tests
├── utils/                    # Utility tests
└── root_scripts/             # Root script tests
```

**Test Types**:

1. **Unit Tests** (testing individual functions/classes):
   - Test one function or class in isolation
   - Mock all external dependencies
   - Fast execution (milliseconds per test)
   - Example: `test_PlayerManager_scoring.py`

2. **Integration Tests** (testing module interactions):
   - Test workflows spanning multiple classes
   - Use real objects where possible, mock only I/O
   - May take longer (seconds per test)
   - Example: `test_league_helper_integration.py`

**Writing Effective Tests**:

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Use descriptive test class names
class TestPlayerScoringCalculations:
    """Test player scoring algorithm with various scenarios"""

    @pytest.fixture
    def sample_player(self):
        """Create a test player with known stats"""
        return FantasyPlayer(
            name="Test Player",
            position="QB",
            projected_points=300.0
        )

    def test_scoring_with_normal_stats(self, sample_player):
        """Test scoring calculation with typical player stats"""
        # Arrange
        expected_score = 315.5

        # Act
        actual_score = sample_player.calculate_total_score()

        # Assert
        assert abs(actual_score - expected_score) < 0.1

    def test_scoring_handles_injury_penalty(self, sample_player):
        """Test that injury status reduces player score"""
        # Arrange
        sample_player.injury_status = "Questionable"
        expected_penalty = -5.0

        # Act
        score_healthy = sample_player.calculate_total_score()
        sample_player.injury_status = "Healthy"
        score_injured = sample_player.calculate_total_score()

        # Assert
        assert score_injured == score_healthy + expected_penalty
```

**Mocking Best Practices**:

```python
# Mock file I/O
@patch('pathlib.Path.open')
def test_loads_data_from_csv(self, mock_open):
    mock_open.return_value.__enter__.return_value = StringIO("header\ndata")
    result = load_csv_data(Path("test.csv"))
    assert len(result) == 1

# Mock external API calls
@patch('requests.get')
def test_fetches_player_data(self, mock_get):
    mock_get.return_value.json.return_value = {"players": []}
    result = fetch_players()
    assert result is not None

# Mock datetime for consistent tests
@patch('datetime.datetime')
def test_current_week_calculation(self, mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 9, 15)
    assert get_current_nfl_week() == 2
```

**Test Fixtures**:

```python
@pytest.fixture
def temp_data_folder(tmp_path):
    """Create temporary data folder with test files"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create test CSV
    players_csv = data_folder / "players.csv"
    players_csv.write_text("Name,Position,Team\nPlayer1,QB,KC\n")

    return data_folder

@pytest.fixture
def mock_config():
    """Create mock configuration for testing"""
    config = Mock()
    config.get_adp_multiplier.return_value = (1.5, 95)
    config.get_injury_penalty.return_value = -5.0
    return config
```

**Test Execution**:

```bash
# Run all tests (required before commits)
python tests/run_all_tests.py

# Run specific test file
python -m pytest tests/league_helper/util/test_PlayerManager.py -v

# Run specific test class
python -m pytest tests/simulation/test_Week.py::TestWeekSimulation -v

# Run tests with coverage report
python -m pytest --cov=league_helper --cov-report=html

# Run tests in parallel (faster)
python -m pytest -n 8
```

**Test Requirements**:
- ✅ All unit tests must pass (100% pass rate)
- ✅ Test names must be descriptive (not `test_1`, `test_2`)
- ✅ Each test should test ONE thing
- ✅ Use AAA pattern (Arrange, Act, Assert)
- ✅ Mock external dependencies (files, APIs, datetime)
- ✅ Use fixtures for reusable test data
- ✅ Clean up resources in test teardown
- ✅ Tests should be independent (no shared state)
