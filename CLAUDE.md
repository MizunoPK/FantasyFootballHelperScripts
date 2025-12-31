# Fantasy Football Helper Scripts - Claude Code Guidelines

## Quick Start for New Agents

**FIRST**: Read `ARCHITECTURE.md` for complete architectural overview, system design, and implementation details.

**SECOND**: Read `README.md` for project overview, installation instructions, and usage guide.

**THIS FILE**: Contains workflow rules, coding standards, and commit protocols.

---

## Project-Specific Rules

### Epic-Driven Development Workflow (v2)

The v2 workflow is a **7-stage epic-driven development process** for managing large projects:

**Workflow Overview:**
```
Stage 1: Epic Planning → Stage 2: Feature Deep Dives → Stage 3: Cross-Feature Sanity Check →
Stage 4: Epic Testing Strategy → Stage 5: Feature Implementation (5a→5b→5c→5d→5e per feature) →
Stage 6: Epic-Level Final QC → Stage 7: Epic Cleanup
```

**Terminology:**
- **Epic** = Top-level work unit (collection of related features)
- **Feature** = Individual component within an epic
- User creates `{epic_name}.txt` → Agent creates `{epic_name}/` folder with multiple `feature_XX_{name}/` folders

---

### 🚨 MANDATORY: Phase Transition Protocol

**When transitioning between ANY stage, you MUST:**

1. **READ the guide FIRST** - Use Read tool to load the ENTIRE guide for that stage
2. **ACKNOWLEDGE what you read** - Use the phase transition prompt from `feature-updates/guides_v2/prompts_reference_v2.md`
3. **VERIFY prerequisites** - Check prerequisites checklist in guide
4. **UPDATE Agent Status** - Update EPIC_README.md or feature README.md with current guide + timestamp
5. **THEN proceed** - Follow the guide step-by-step

**Phase transition prompts are MANDATORY for:**
- Starting any of the 7 stages (1, 2, 3, 4, 5a, 5b, 5c, 5d, 5e, 6, 7)
- Starting Stage 5a rounds (Round 1, 2, 3)
- Starting Stage 5c phases (Smoke Testing, QC Rounds, Final Review)
- Creating a bug fix
- Resuming after session compaction

**See:** `feature-updates/guides_v2/prompts_reference_v2.md` → Complete prompt library

**Why this matters:** Reading the guide first ensures you don't miss mandatory steps. The prompt acknowledgment confirms you understand requirements. Historical evidence: 40% guide abandonment rate without mandatory prompts.

**Example - Starting Stage 5a Round 1:**
```
I'm reading `STAGE_5aa_round1_guide.md` to ensure I follow all 8 iterations in Round 1...

The guide requires:
- Round 1: 8 MANDATORY iterations (iterations 1-7 + 4a)
- Iteration 4a is a MANDATORY GATE (TODO Specification Audit)
- Algorithm Traceability Matrix (iteration 4)
- Integration Gap Check (iteration 7)
- STOP if confidence < Medium at Round 1 checkpoint

Prerequisites I'm verifying:
✅ spec.md exists and is complete
✅ checklist.md all items resolved
✅ Stage 4 (Epic Testing Strategy) complete

I'll now proceed with Round 1 (iterations 1-7 + 4a)...
```

---

### Stage 1: When User Says "Help Me Develop {epic-name}"

**Trigger phrases:** "Help me develop...", "I want to plan...", "Let's work on..."

**Prerequisites:** User has created `feature-updates/{epic_name}.txt` with initial scratchwork notes.

**🚨 FIRST ACTION:** Use the "Starting Stage 1" prompt from `feature-updates/guides_v2/prompts_reference_v2.md`

**Workflow:**
1. **READ:** `feature-updates/guides_v2/STAGE_1_epic_planning_guide.md`
2. **Analyze epic request** and perform codebase reconnaissance
3. **Propose feature breakdown** (agent → user confirms/modifies)
4. **Create epic folder:** `feature-updates/{epic_name}/`
5. **Create feature folders:** `feature_01_{name}/`, `feature_02_{name}/`, etc.
6. **Create epic-level files:**
   - `EPIC_README.md` (with Quick Reference Card, Agent Status, Epic Progress Tracker)
   - `epic_smoke_test_plan.md` (initial version, updated in Stages 4 and 5e)
   - `epic_lessons_learned.md` (cross-feature insights)
7. **Create feature-level files** for each feature:
   - `README.md`, `spec.md`, `checklist.md`, `lessons_learned.md`

**Next:** Stage 2 (Feature Deep Dives)

---

### Stage 2-4: Planning & Testing Strategy

**Stage 2: Feature Deep Dives** (Loop through ALL features)
- **READ:** `STAGE_2_feature_deep_dive_guide.md`
- Flesh out `spec.md` for each feature with detailed requirements
- Interactive question resolution (ONE question at a time)
- Compare to already-completed features for alignment
- Dynamic scope adjustment (if scope >35 items, propose split)

**Stage 3: Cross-Feature Sanity Check** (After ALL features planned)
- **READ:** `STAGE_3_cross_feature_sanity_check_guide.md`
- Systematic pairwise comparison of all feature specs
- Resolve conflicts and inconsistencies
- Get user sign-off on complete plan

**Stage 4: Epic Testing Strategy** (Update test plan)
- **READ:** `STAGE_4_epic_testing_strategy_guide.md`
- Update `epic_smoke_test_plan.md` based on deep dive findings
- Identify integration points between features
- Define epic success criteria

**Next:** Stage 5 (Feature Implementation - first feature)

---

### Stage 5: Feature Implementation (Loop per feature: 5a→5b→5c→5d→5e)

**Stage 5a: TODO Creation** (24 verification iterations across 3 rounds)

**🚨 FIRST ACTION:** Use the "Starting Stage 5a Round 1" prompt from `prompts_reference_v2.md`

- **Round 1:** READ `STAGE_5aa_round1_guide.md` - Iterations 1-7 + 4a
  - Iteration 4: Algorithm Traceability Matrix
  - Iteration 4a: TODO Specification Audit (MANDATORY GATE)
  - Iteration 7: Integration Gap Check
- **Round 2:** READ `STAGE_5ab_round2_guide.md` - Iterations 8-16
  - Iteration 11: Algorithm Traceability Matrix (re-verify)
  - Iteration 14: Integration Gap Check (re-verify)
  - Iteration 15: Test Coverage Depth Check (>90% required)
- **Round 3:** READ `STAGE_5ac_round3_guide.md` - Iterations 17-24 + 23a
  - Iteration 19: Algorithm Traceability Matrix (final verify)
  - Iteration 21: Mock Audit & Integration Test Plan
  - Iteration 23: Integration Gap Check (final verify)
  - Iteration 23a: Pre-Implementation Spec Audit (4 MANDATORY PARTS - ALL must PASS)
  - Iteration 24: Implementation Readiness Protocol (GO/NO-GO decision)
- Create `todo.md` and `questions.md`

**Stage 5b: Implementation Execution**

**🚨 FIRST ACTION:** Use the "Starting Stage 5b" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_5b_implementation_execution_guide.md`
- Keep `spec.md` VISIBLE at all times (not just "consult when needed")
- Continuous spec verification via `implementation_checklist.md`
- Mini-QC checkpoints after each major component
- Create `code_changes.md` documenting all changes
- Run unit tests after EVERY phase (100% pass required)

**Stage 5c: Post-Implementation** (3 phases - smoke testing, QC rounds, final review)

**🚨 FIRST ACTION:** Use the "Starting Stage 5c Smoke Testing" prompt from `prompts_reference_v2.md`

- **Phase 1 (Smoke Testing):** READ `STAGE_5ca_smoke_testing_guide.md`
  - Part 1: Import Test (module loads without errors)
  - Part 2: Entry Point Test (script starts correctly)
  - Part 3: E2E Execution Test (verify OUTPUT DATA VALUES, not just file structure)
  - MANDATORY GATE before QC rounds

- **Phase 2 (QC Rounds):** READ `STAGE_5cb_qc_rounds_guide.md`
  - QC Round 1: Basic validation (<3 critical issues, >80% requirements)
  - QC Round 2: Deep verification (all Round 1 resolved + zero new critical)
  - QC Round 3: Final skeptical review (ZERO tolerance)
  - **QC Restart Protocol:** If ANY issues → COMPLETELY RESTART from smoke testing

- **Phase 3 (Final Review):** READ `STAGE_5cc_final_review_guide.md`
  - PR Review Checklist (11 categories - all mandatory)
  - Lessons learned capture with IMMEDIATE guide updates
  - Final verification (100% completion required)

**Stage 5d: Cross-Feature Spec Alignment** (After feature completes)

**🚨 FIRST ACTION:** Use the "Starting Stage 5d" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_5d_post_feature_alignment_guide.md`
- Review ALL remaining (unimplemented) feature specs
- Compare specs to ACTUAL implementation (not just plan)
- Update specs based on real insights from completed feature
- Prevents spec drift as implementation reveals reality

**Stage 5e: Epic Testing Plan Reassessment** (After Stage 5d)

**🚨 FIRST ACTION:** Use the "Starting Stage 5e" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_5e_post_feature_testing_update_guide.md`
- Reassess `epic_smoke_test_plan.md` after EACH feature
- Update test scenarios based on actual implementation
- Add newly discovered integration points
- Keep testing plan current throughout implementation

**Repeat Stage 5 (5a→5b→5c→5d→5e) for EACH feature**

---

### Stage 6-7: Epic Finalization

**Stage 6: Epic-Level Final QC** (After ALL features complete)

**🚨 FIRST ACTION:** Use the "Starting Stage 6" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_6_epic_final_qc_guide.md`
- Execute evolved `epic_smoke_test_plan.md` (reflects all Stage 5e updates)
- Run epic-level smoke testing (tests ALL features integrated together)
- Complete 3 epic-level QC rounds
- Epic-level PR review (11 categories)
- Validate against original epic request
- Create bug fixes for any issues, RESTART Stage 6 after fixes

**Stage 7: Epic Cleanup** (After Stage 6 passes)

**🚨 FIRST ACTION:** Use the "Starting Stage 7" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_7_epic_cleanup_guide.md`
- Run unit tests (100% pass MANDATORY)
- Capture guide improvements
- **User testing (MANDATORY GATE):**
  - Ask user to test complete system themselves
  - If bugs found → Follow bug fix protocol
  - After bug fixes → RESTART Stage 6 (Epic Final QC)
  - Repeat until user testing passes with ZERO bugs
- Commit changes (only after user testing passes)
- Move entire epic folder to `feature-updates/done/{epic_name}/`

---

### Bug Fix Workflow

If bugs are discovered during ANY stage:

**🚨 FIRST ACTION:** Use the "Creating a Bug Fix" prompt from `prompts_reference_v2.md`

- **READ:** `STAGE_5_bug_fix_workflow_guide.md`
- Create `bugfix_{priority}_{name}/` folder inside epic
- Priority levels: high, medium, low
- Bug fixes go through: Stage 2 → 5a → 5b → 5c (SKIP Stages 1, 3, 4, 5d, 5e, 6, 7)
- After bug fix complete, return to paused work

---

### Key Principles

- **Epic-first thinking**: Top-level work unit is an epic (collection of features)
- **Mandatory reading protocol**: ALWAYS read guide before starting stage
- **Phase transition prompts**: MANDATORY acknowledgment (proves guide was read)
- **Continuous alignment**: Stage 5d updates specs after each feature
- **Iterative testing**: Test plan evolves (Stage 1 → 4 → 5e → 6)
- **Epic vs feature distinction**: Feature testing (5c) vs epic testing (6) are different
- **24 verification iterations**: All mandatory (across 3 rounds in Stage 5a)
- **QC restart protocol**: If ANY issues → restart completely
- **No skipping stages**: All stages have dependencies, must complete in order
- **100% test pass**: Required before commits and stage transitions

See `feature-updates/guides_v2/README.md` for complete workflow overview and guide index.

---

### Resuming In-Progress Epic Work

**BEFORE starting any epic-related work**, check for in-progress epics:

1. **Check for active epic folders:** Look in `feature-updates/` for any folders (excluding `done/` and `guides_v2/`)

2. **If found, use the "Resuming In-Progress Epic" prompt** from `feature-updates/guides_v2/prompts_reference_v2.md`

3. **READ THE EPIC_README.md FIRST:** Check the "Agent Status" section at the top with:
   - Current stage and guide
   - Current step/iteration
   - Next action to take
   - Critical rules from current guide

4. **READ THE CURRENT GUIDE:** Use Read tool to load the guide listed in Agent Status

5. **Continue from where previous agent left off** - Don't restart the workflow

**Why this matters:** Session compaction can interrupt agents mid-workflow. EPIC_README.md Agent Status survives context window limits and provides exact resumption point.

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
  - **Supporting Files (4 files):**
    - `templates_v2.md` - File templates (epic, feature, bug fix)
    - `prompts_reference_v2.md` - MANDATORY phase transition prompts
    - `README.md` - Workflow overview and guide index
    - `PLAN.md` - Complete v2 workflow specification
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
