# Fantasy Football Helper Scripts - Claude Code Guidelines

## Quick Start for New Agents

**FIRST**: Read `ARCHITECTURE.md` for complete architectural overview, system design, and implementation details.

**SECOND**: Read `README.md` for project overview, installation instructions, and usage guide.

**THIS FILE**: Contains workflow rules, coding standards, and commit protocols.

---

## Project-Specific Rules

### Feature Development Workflow Overview

The feature development process has two phases:

1. **Planning Phase** - User says "Help me develop the {feature-name} feature"
2. **Implementation Phase** - User says "Prepare for updates based on {feature-name}"

---

### 🚨 MANDATORY: Phase Transition Protocol

**When transitioning between ANY phase, you MUST:**

1. **READ the guide FIRST** - Open and read the complete guide for that phase
2. **ACKNOWLEDGE what you read** - Use the phase transition prompt from `feature-updates/guides/prompts_reference.md`
3. **THEN proceed** - Follow the guide step-by-step

**Phase transition prompts are MANDATORY for:**
- Starting Feature Creation → Use "Starting Feature Creation" prompt
- Starting Deep Dive (per sub-feature) → Use "Starting Deep Dive" prompt
- Starting TODO Creation (Phase 2a) → Use "Starting TODO Creation" prompt
- Starting Implementation (Phase 2b) → Use "Starting Implementation" prompt
- Starting Post-Implementation QC (Phase 2c) → Use "Starting Post-Implementation QC" prompt
- Resuming In-Progress Feature → Use "Resuming In-Progress Feature" prompt

**See:** `feature-updates/guides/prompts_reference.md` → "Phase Transition Prompts" section

**Why this matters:** Reading the guide first ensures you don't miss mandatory steps. The prompt acknowledgment confirms you understand the requirements before starting work.

**Example - Starting TODO Creation:**
```
I'm reading `todo_creation_guide.md` to ensure I follow all 24 verification iterations...

The guide requires:
- 24 mandatory iterations across 3 rounds
- Algorithm Traceability Matrix (iterations 4, 11, 19)
- TODO Specification Audit (iteration 4a)
- NO SKIPPING ITERATIONS - complexity hides, shortcuts cause 40% QC failure

I'll now proceed with Round 1 (iterations 1-7)...
```

---

### Phase 1: When User Says "Help Me Develop {feature-name}"

**Trigger phrases:** "Help me develop...", "I want to plan...", "Let's work on the specification for..."

**Prerequisites:** User has created `feature-updates/{feature-name}.txt` with initial scratchwork notes.

**🚨 FIRST ACTION:** Use the "Starting Feature Creation" prompt from `feature-updates/guides/prompts_reference.md` - READ the creation guide, ACKNOWLEDGE requirements, THEN proceed.

**Workflow (Two-Guide Approach):**

**Step 1: Initial Planning & Sub-Feature Breakdown**
1. **Follow `feature-updates/guides/feature_creation_guide.md`**
2. **Create the feature folder** `feature-updates/{feature-name}/`
3. **Move original notes** into folder as `{feature_name}_notes.txt`
4. **Broad reconnaissance** - Understand scope, identify major components
5. **Critical decision: Sub-feature breakdown**
   - Evaluate if feature should be broken into sub-features
   - **Triggers:** 3+ components, 30+ items, multiple subsystems, different risk levels
   - If YES: Create `SUB_FEATURES_README.md` + per-sub-feature specs/checklists
   - If NO: Create single `{feature_name}_specs.md` + `{feature_name}_checklist.md`
6. **Create `research/` folder** - All research documents go here from the start
7. **Create** `{feature_name}_lessons_learned.md` (shared across all sub-features)
8. **Create** `README.md` - Context and status for future agents

**Step 2: Deep Dive Planning (Per Sub-Feature or Once for Single Feature)**
9. **Follow `feature-updates/guides/feature_deep_dive_guide.md`**
10. **Execute ONCE per sub-feature** (or once if single feature)
11. **Targeted research** - Deep dive into THIS sub-feature's scope only
12. **Interactive question resolution** - ONE question at a time, update after each
13. **Dynamic scope adjustment** - Propose new sub-features if scope grows
14. **Repeat for all sub-features**
15. **Cross-sub-feature alignment review** (MANDATORY if using sub-features)
16. **Complete planning** - All checklist items should be `[x]`

**Key Differences from Old Workflow:**
- Early sub-feature breakdown (Phase 3 of creation guide)
- No global spec/checklist when using sub-features
- All research in `research/` folder from start
- Cross-sub-feature alignment review before implementation

**🚨 IMPORTANT:** Do NOT skip any steps in the guides. Thorough planning prevents rework.

---

### Phase 2: When User Says "Prepare for Updates Based on {feature-name}"

**Trigger phrases:** "Prepare for updates...", "Implement the...", "Start development on..."

**Prerequisites:** Planning phase complete. Feature folder should contain:
- `{feature_name}_notes.txt` - Original scratchwork (reference only)
- `{feature_name}_specs.md` - **Primary specification** (USE THIS for implementation)
- `{feature_name}_checklist.md` - All items marked `[x]`
- `README.md` - Status shows "Ready for Implementation"

**Workflow (3 sequential guides - ALL MANDATORY):**

**Phase 2a: TODO Creation (Verification)**

**🚨 FIRST ACTION:** Use the "Starting TODO Creation" prompt from `feature-updates/guides/prompts_reference.md` - READ the TODO guide, ACKNOWLEDGE the 24 iterations, THEN proceed.

1. **Follow `feature-updates/guides/todo_creation_guide.md`**
2. **Complete ALL 24 verification iterations** (3 rounds: 7+9+8)
   - Round 1: Iterations 1-7 (+ iteration 4a)
   - Round 2: Iterations 8-16
   - Round 3: Iterations 17-24 (+ iteration 23a)
3. **Create `{name}_todo.md`** with complete implementation plan
4. **Create `{name}_questions.md`** if needed (or document "no questions")
5. **Verify interfaces** against actual source code
6. **🛑 STOP:** Do not proceed to coding until Iteration 24 passes

**Phase 2b: Implementation (Coding)**

**🚨 FIRST ACTION:** Use the "Starting Implementation" prompt from `feature-updates/guides/prompts_reference.md` - READ the implementation guide, ACKNOWLEDGE Interface Verification requirement, THEN proceed.

7. **Follow `feature-updates/guides/implementation_execution_guide.md`**
8. **Create `{name}_implementation_checklist.md`** for continuous spec verification
9. **Execute TODO tasks** with specs.md VISIBLE at all times
10. **Run unit tests** after EVERY phase (100% pass required)
11. **Mini-QC checkpoints** after each major component
12. **Create `{name}_code_changes.md`** documenting all changes
13. **🛑 STOP:** Do not proceed to QC until ALL TODO tasks complete

**Phase 2c: Post-Implementation (QC & Validation)**

**🚨 FIRST ACTION:** Use the "Starting Post-Implementation QC" prompt from `feature-updates/guides/prompts_reference.md` - READ the post-implementation guide, ACKNOWLEDGE the 3 QC rounds and smoke testing, THEN proceed.

14. **Follow `feature-updates/guides/post_implementation_guide.md`**
15. **Execute smoke testing protocol** (MANDATORY - 3 parts)
16. **Complete ALL 3 QC rounds** (no exceptions)
17. **Review lessons learned** and identify guide updates
18. **Move entire folder** to `feature-updates/done/{feature-name}/`
19. **Commit changes** with descriptive message

**🚨 CRITICAL:** Each phase has MANDATORY steps. Do NOT skip to the next phase until current phase is 100% complete. Shortcuts cause 40% QC failure rate.

---

### Key Principles

- **Keep files together**: All working files stay in `feature-updates/{feature-name}/`
- **Specs vs Notes**: Use `_specs.md` for implementation, `_notes.txt` is just reference
- **No skipping steps**: Both guides have mandatory steps that must be followed
- **Validate constantly**: Run unit tests after each major step (100% pass required)
- **Document everything**: Keep `_code_changes.md` updated incrementally
- **Quality control**: Complete 3 QC review rounds before completion
- **Clean completion**: Move entire folder to `feature-updates/done/` when finished

See the individual guides for complete protocols and templates.

---

### Resuming In-Progress Feature Work

**BEFORE starting any feature-related work**, check for in-progress features:

1. **Check for active feature folders:** Look in `feature-updates/` for any folders (excluding `done/` and `guides/`)

2. **If found, use the "Resuming In-Progress Feature" prompt** from `feature-updates/guides/prompts_reference.md` - Acknowledge the feature status before continuing

3. **READ THE README.md FIRST:** The README contains an "Agent Status" section at the top with:
   - Current phase and step
   - Next action to take
   - Full workflow checklist showing what's done vs remaining

4. **Continue from where the previous agent left off** - Don't restart the workflow

**Why this matters:** Session compaction can interrupt agents mid-workflow. The README.md serves as the persistent state file that survives context window limits.

---

### Commit Standards
- Brief, descriptive messages (50 chars or less)
- No emojis or subjective prefixes
- Do NOT include "Generated with Claude Code" and co-author tag
- List major changes in body

### Pre-Commit Protocol
**MANDATORY BEFORE EVERY COMMIT**

When the user requests to commit changes (e.g., "commit changes", "verify and commit", "commit this"):

**STEP 1: Run Unit Tests (REQUIRED)**
```bash
python tests/run_all_tests.py
```

**Test Requirements**:
- All unit tests must pass (100% pass rate)
- Tests located in `tests/` directory
- Exit code 0 = safe to commit, 1 = DO NOT COMMIT

**Only proceed to commit if all tests pass.**

**STEP 2: If Tests Pass, Commit Changes**
1. Analyze all changes with `git status` and `git diff`
2. Update documentation (README.md, CLAUDE.md) if functionality changed
3. Stage and commit with clear, concise message
4. Follow commit standards (see above)

**STEP 3: If Tests Fail**
- **STOP** - Do NOT commit
- Fix failing tests
- Re-run `python tests/run_all_tests.py`
- Only commit when all tests pass (exit code 0)

**Test Structure**:
- All tests in `tests/` directory (mirror source structure)
- See `tests/README.md` for test standards and guidelines
- Run with `--verbose` or `--detailed` flags for more output

**Do NOT skip validation**: 100% test pass rate is mandatory

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
- `feature-updates/` - Root folder for feature development
  - `{feature-name}.txt` - Initial scratchwork from user (before planning)
  - `{feature-name}/` - Feature folder (created during planning phase)
    - `{name}_notes.txt` - Original scratchwork (moved from root)
    - `{name}_specs.md` - **Primary specification** (detailed requirements)
    - `{name}_checklist.md` - Tracks resolved vs pending decisions
    - `{name}_questions.md` - Questions for user (created during development)
    - `{name}_todo.md` - Implementation tracking
    - `{name}_code_changes.md` - Documentation of all changes
    - `README.md` - Context for agents
- `feature-updates/done/` - Completed feature folders (moved here after completion)
- `feature-updates/guides/` - Workflow guides for feature development
  - `feature_planning_guide.md` - Guide for Phase 1 (planning)
  - `feature_development_guide.md` - Guide for Phase 2 (implementation)
  - `README.md` - Guide overview and quick reference
- `CLAUDE.md` - This file (coding standards and workflow guidelines)
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
