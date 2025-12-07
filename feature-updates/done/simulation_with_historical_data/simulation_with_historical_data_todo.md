# Simulation with Historical Data - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 ✓ |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 ✓ |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 ✓ |

**Current Iteration:** 24/24 COMPLETE - READY FOR IMPLEMENTATION

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [x]1 [x]2 [x]3 [x]8 [x]9 [x]10 [x]15 [x]16 ✓ |
| Algorithm Traceability | 4, 11, 19 | [x]4 [x]11 [x]19 ✓ |
| End-to-End Data Flow | 5, 12 | [x]5 [x]12 ✓ |
| Skeptical Re-verification | 6, 13, 22 | [x]6 [x]13 [x]22 ✓ |
| Integration Gap Check | 7, 14, 23 | [x]7 [x]14 [x]23 ✓ |
| Fresh Eyes Review | 17, 18 | [x]17 [x]18 ✓ |
| Edge Case Verification | 20 | [x]20 ✓ |
| Test Coverage Planning | 21 | [x]21 ✓ |
| Implementation Readiness | 24 | [x]24 ✓ |

---

## Verification Summary

- Iterations completed: 24/24 ✓ ALL COMPLETE
- Requirements from spec: 18
- Requirements in TODO: 17 (added Task 2.6, removed Task 3.2)
- Questions for user: 0
- Integration points identified: 7
- Tasks added: 1 (Task 2.6 for Week.py)
- Tasks removed: 1 (Task 3.2 - reuse FantasyPlayer.from_dict)

---

## Iteration Findings

### Iteration 1: Files & Patterns (Standard Verification)

**Files Read:**
- `simulation/SimulationManager.py` (895 lines)
- `simulation/SimulatedLeague.py` (451 lines)
- `simulation/ParallelLeagueRunner.py` (382 lines)
- `league_helper/util/PlayerManager.py` (612 lines)

**Key Findings:**

1. **Week Count Bug in SimulatedLeague.py**:
   - Line 298: `range(1, 17)` = weeks 1-16 (NOT 1-17)
   - Line 223: `num_weeks=16` in schedule generation
   - Line 314: Comment says "17 weeks simulated" but code does 16 - **BUG**
   - Class docstring (line 55) says "17-week season"

2. **Existing Pattern - FantasyPlayer.from_dict()**:
   - PlayerManager.py line 179: `player = FantasyPlayer.from_dict(row)` already exists
   - Can reuse this pattern for Task 3.2 instead of creating new method

3. **Current Data Loading** (SimulatedLeague._initialize_teams() lines 124-213):
   - Copies files ONCE at init using shutil.copy()
   - No week-specific loading - same data used for all 16 weeks
   - Lines 159-167: Copies players_projected.csv and players_actual.csv

4. **Integration Points Verified**:
   - SimulationManager.__init__: lines 59-114
   - ParallelLeagueRunner created at lines 104-107
   - run_iterative_optimization(): lines 404-706
   - Already uses `run_simulations_for_config_with_weeks()` (line 519)

**Updates Made:**
- None yet - findings documented for implementation phase

### Iteration 2: Error Handling (Standard Verification)

**Files Examined:**
- Grep patterns for `raise.*Error|except.*:|try:` in simulation/
- Logging patterns in SimulationManager.py

**Key Findings:**

1. **Week.py has hardcoded week 1-16 validation**:
   - Line 73: Docstring says `(1-16)`
   - Line 79: `if not (1 <= week_number <= 16)`
   - Line 80: Error message says "must be between 1 and 16"
   - **NEW TASK REQUIRED**: Update Week.py to allow week 17

2. **ConfigPerformance.py already supports week 17**:
   - Line 46: Already validates "Must be between 1 and 17"

3. **Error handling patterns to follow**:
   - `raise FileNotFoundError` for missing files (matches spec's "fail loudly")
   - `raise ValueError` for invalid inputs
   - try/except with logging for operation failures
   - Pattern: `self.logger.error(f"[Sim {simulation_id}] Failed: {e}", exc_info=True)`

4. **Logging patterns to follow**:
   - `self.logger.info()` for progress messages
   - `self.logger.debug()` for detailed tracing
   - `self.logger.warning()` for non-fatal issues

**New Task Identified:**
- Task 2.6: Update Week.py to allow week 17

### Iteration 3: Integration Points (Standard Verification)

**Test Patterns Found:**
- Use `unittest.mock` (Mock, MagicMock, patch)
- Use `tempfile` for temporary directories
- Use `pytest` fixtures for reusable test data
- Existing test files: `test_simulation_manager.py`, `test_SimulatedLeague.py`, `test_Week.py`

**Mocking Strategy for New Methods:**
1. `_discover_seasons()` - Mock `Path.glob()` to return fake season folders
2. `_validate_season_strict()` - Mock `Path.exists()` for file checks
3. `_preload_all_weeks()` - Mock file reads, return dict data
4. `set_player_data()` - No mocking needed, pure data manipulation

### Iteration 4: Algorithm Traceability (Special Protocol)

**Algorithm Mapping Complete** (see Algorithm Traceability Matrix section below):
- All spec algorithms mapped to code locations
- Conditional logic documented
- No missing algorithms identified

### Iteration 5: End-to-End Data Flow (Special Protocol)

**Data Flow Traces Verified** (see Data Flow Traces section):
1. Season Discovery: run_simulation.py → SimulationManager.__init__ → _discover_seasons → available_seasons
2. Multi-Season Loop: run_iterative_optimization → ThreadPoolExecutor → _run_season_simulations → ParallelLeagueRunner
3. Week-Specific Loading: SimulatedLeague.__init__ → _preload_all_weeks → run_season → _load_week_data → set_player_data

**Critical Path Verified:**
- Entry point: `run_simulation.py --mode iterative`
- No orphan code identified in proposed design

### Iteration 6: Skeptical Re-verification (Special Protocol)

**Assumptions Challenged:**
1. ✓ `FantasyPlayer.from_dict()` exists (verified at PlayerManager.py:179)
2. ✓ Historical data folders use `weeks/week_XX/` format (verified in compile_historical_data.py)
3. ✓ Current week loop is `range(1, 17)` = weeks 1-16 (verified at SimulatedLeague.py:298)
4. ✓ Week.py validates week 1-16 (verified at Week.py:79)

**Corrections Made:**
- Added Task 2.6 for Week.py validation update (found in iteration 2)

**Confidence Level:** HIGH - All assumptions verified against source code

### Iteration 7: Integration Gap Check (Special Protocol)

**Every New Method Has a Caller:**
| New Method | Caller | Task |
|------------|--------|------|
| `_discover_seasons()` | `SimulationManager.__init__()` | Task 1.3 |
| `_validate_season_strict()` | `_discover_seasons()` | Task 1.1 |
| `_run_season_simulations()` | `run_iterative_optimization()` | Task 1.4 |
| `_preload_all_weeks()` | `SimulatedLeague.__init__()` | Task 2.1 |
| `_parse_players_csv()` | `_preload_all_weeks()` | Task 2.1 |
| `_load_week_data()` | `run_season()` | Task 2.4 |
| `set_player_data()` | `_load_week_data()` | Task 2.3 |

**No Orphan Code Identified** - All methods have callers and caller modification tasks

---

## Round 2 Findings (Iterations 8-16)

### Iteration 8: Standard Verification - Code Reuse

**Key Finding:**
- `FantasyPlayer.from_dict()` exists at `utils/FantasyPlayer.py:141`
- Handles all 17 weekly projections and player fields
- **Task 3.2 REMOVED** - no new method needed

**Simplification:**
- Task 3.1 updated to use `FantasyPlayer.from_dict()` directly
- Reduced complexity, better code reuse

### Iteration 9-10: Standard Verification - Integration Points

**Verified Integration Points:**
- `SimulationManager.parallel_runner` created at line 104
- `run_simulations_for_config_with_weeks()` called at line 519
- This is THE integration point for multi-season support

**Modification Strategy Confirmed:**
- Wrap line 519 call in season loop
- Aggregate results across seasons before comparison

### Iteration 11: Algorithm Traceability (Repeat)

**Verified:**
- All algorithms from spec have code locations identified
- Season discovery → `_discover_seasons()`
- Week loading → `_preload_all_weeks()` + `_load_week_data()`
- Parallel seasons → `ThreadPoolExecutor` in `run_iterative_optimization()`

### Iteration 12: End-to-End Data Flow (Repeat)

**Full Data Flow Verified:**
```
run_simulation.py --mode iterative
  → SimulationManager.__init__()
    → _discover_seasons() [NEW]
    → available_seasons = [2021, 2022, 2023, 2024]
  → run_iterative_optimization()
    → For each config:
      → For each season (parallel):
        → ParallelLeagueRunner(data_folder=season_folder)
        → SimulatedLeague.__init__()
          → _preload_all_weeks() [NEW]
        → SimulatedLeague.run_draft()
        → SimulatedLeague.run_season()
          → _load_week_data() [NEW]
          → PlayerManager.set_player_data() [NEW]
      → Aggregate results across all seasons
    → Compare configs, select best
```

### Iteration 13-14: Skeptical Re-verification & Integration Gap

**All Verified:**
- No orphan methods
- No missing callers
- All error handling uses "fail loudly" pattern per spec

### Iterations 15-16: Standard Verification (Final)

**Data File Mapping Verified:**
- Current: `players_projected.csv` → decisions, `players_actual.csv` → scoring
- Historical: `weeks/week_XX/players.csv` → "smart values" (actuals for past, projected for future)
- Design uses `players.csv` for both (contains correct data per week)

---

## Round 3 Findings (Iterations 17-24)

### Iteration 17-18: Fresh Eyes Review

**Critical Review - No Issues Found:**
1. ✓ Season discovery at init - correct (fail early if no data)
2. ✓ Parallel season execution - correct (maximizes throughput)
3. ✓ Pre-load weeks at SimulatedLeague init - correct (17 parses vs 340)
4. ✓ Share data across teams - correct (no redundant parsing)
5. ✓ Week.py validation update - correct (17 weeks now)

**Possible Future Improvement (NOT IN SCOPE):**
- Could add progress tracking per season (currently only per config)

### Iteration 19: Algorithm Traceability (Final)

**Complete Algorithm Map:**
| Spec Requirement | Method | File:Line |
|------------------|--------|-----------|
| Discover seasons | `_discover_seasons()` | SimulationManager.py:NEW |
| Validate structure | `_validate_season_strict()` | SimulationManager.py:NEW |
| Parallel seasons | `ThreadPoolExecutor` | SimulationManager.py:519 area |
| Pre-load weeks | `_preload_all_weeks()` | SimulatedLeague.py:NEW |
| Parse CSV | `_parse_players_csv()` | SimulatedLeague.py:NEW |
| Load week data | `_load_week_data()` | SimulatedLeague.py:NEW |
| Set player data | `set_player_data()` | PlayerManager.py:NEW |
| 17-week season | `run_season()` | SimulatedLeague.py:298 |
| Week validation | `__init__()` | Week.py:79 |

### Iteration 20: Edge Case Verification

**Edge Cases Handled:**
1. ✓ No seasons found → FileNotFoundError (fail loudly)
2. ✓ Single season only → Works (run with just one year)
3. ✓ Missing week folder → FileNotFoundError (fail loudly)
4. ✓ Missing players.csv → FileNotFoundError (fail loudly)
5. ✓ Player roster changes between weeks → No issue (each week loads fresh)
6. ✓ New season added (2025/) → Auto-discovered via glob

### Iteration 21: Test Coverage Planning

**Tests Required:**
| Task | Test Type | Priority |
|------|-----------|----------|
| `_discover_seasons()` | Unit | HIGH |
| `_validate_season_strict()` | Unit | HIGH |
| `_preload_all_weeks()` | Unit | MEDIUM |
| `_load_week_data()` | Unit | MEDIUM |
| `set_player_data()` | Unit | MEDIUM |
| Week.py validation | Unit | LOW (simple change) |
| Multi-season simulation | Integration | HIGH |

### Iteration 22: Skeptical Re-verification (Final)

**Final Verification:**
- ✓ All code paths have error handling
- ✓ All new methods have callers
- ✓ All callers are modified appropriately
- ✓ No hardcoded values (uses glob pattern, range(1, 18))

### Iteration 23: Integration Gap Check (Final)

**Final Integration Verification:**
- ✓ SimulationManager → ParallelLeagueRunner (passes season folder)
- ✓ ParallelLeagueRunner → SimulatedLeague (passes data_folder)
- ✓ SimulatedLeague → PlayerManager (calls set_player_data)
- ✓ All connections verified

### Iteration 24: Implementation Readiness

**READY FOR IMPLEMENTATION ✓**

**Final Task Count:** 17 tasks (reduced from 19)
- Task 3.2 removed (reuse FantasyPlayer.from_dict)
- All other tasks verified and ready

**Implementation Order:**
1. Task 2.6: Week.py validation (simple, no dependencies)
2. Task 2.5: Schedule generation (simple, no dependencies)
3. Tasks 1.1-1.3: Season discovery (SimulationManager)
4. Tasks 2.1-2.4: Week loading (SimulatedLeague)
5. Task 3.1: set_player_data (PlayerManager)
6. Tasks 1.4-1.6: Parallel execution + deprecation
7. Tasks 4.1-4.4: Tests

---

## Phase 1: SimulationManager Changes

### Task 1.1: Add Season Discovery Method

- **File:** `simulation/SimulationManager.py`
- **Method:** `_discover_seasons() -> List[Path]`
- **Tests:** `tests/simulation/test_SimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def _discover_seasons(self) -> List[Path]:
    """Find all valid 20XX/ season folders in data_folder."""
    season_folders = sorted(self.data_folder.glob("20*/"))

    if not season_folders:
        raise FileNotFoundError(
            f"No historical season folders (20XX/) found in {self.data_folder}. "
            "Run compile_historical_data.py first."
        )

    valid = []
    for folder in season_folders:
        self._validate_season_strict(folder)  # Raises on invalid
        valid.append(folder)

    return valid
```

### Task 1.2: Add Strict Season Validation Method

- **File:** `simulation/SimulationManager.py`
- **Method:** `_validate_season_strict(folder: Path) -> None`
- **Tests:** `tests/simulation/test_SimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def _validate_season_strict(self, folder: Path) -> None:
    """Validate season folder structure. Raises FileNotFoundError on invalid."""
    year = folder.name

    # Check required files
    required_files = [folder / "season_schedule.csv", folder / "game_data.csv"]
    for req_file in required_files:
        if not req_file.exists():
            raise FileNotFoundError(f"Season {year} missing: {req_file.name}")

    # Check team_data and weeks folders
    if not (folder / "team_data").exists():
        raise FileNotFoundError(f"Season {year} missing team_data/")

    weeks_folder = folder / "weeks"
    if not weeks_folder.exists():
        raise FileNotFoundError(f"Season {year} missing weeks/")

    # Check all 17 weeks
    for week_num in range(1, 18):
        week_folder = weeks_folder / f"week_{week_num:02d}"
        if not week_folder.exists():
            raise FileNotFoundError(f"Season {year} missing week_{week_num:02d}/")
        if not (week_folder / "players.csv").exists():
            raise FileNotFoundError(f"Season {year} week_{week_num:02d}/ missing players.csv")
```

### Task 1.3: Update SimulationManager __init__

- **File:** `simulation/SimulationManager.py`
- **Method:** `__init__()`
- **Tests:** `tests/simulation/test_SimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Add `self.available_seasons = self._discover_seasons()` after existing init
- Log discovered seasons: `self.logger.info(f"Discovered {len(self.available_seasons)} seasons")`

### Task 1.4: Update run_iterative_optimization for Parallel Seasons

- **File:** `simulation/SimulationManager.py`
- **Method:** `run_iterative_optimization()`
- **Tests:** `tests/simulation/test_SimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# For each config, run all seasons in PARALLEL
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=len(self.available_seasons)) as season_executor:
    future_to_season = {
        season_executor.submit(
            self._run_season_simulations, config, season_folder
        ): season_folder
        for season_folder in self.available_seasons
    }

    for future in as_completed(future_to_season):
        season_results = future.result()
        all_season_results.extend(season_results)
```

### Task 1.5: Add Season Simulation Helper Method

- **File:** `simulation/SimulationManager.py`
- **Method:** `_run_season_simulations(config: dict, season_folder: Path) -> List`
- **Tests:** `tests/simulation/test_SimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def _run_season_simulations(self, config: dict, season_folder: Path) -> List:
    """Run simulations for a single season (called in parallel)."""
    runner = ParallelLeagueRunner(
        max_workers=self.max_workers,
        data_folder=season_folder
    )
    return runner.run_simulations_for_config_with_weeks(
        config, self.num_simulations_per_config
    )
```

### Task 1.6: Deprecate Unused Simulation Modes

- **File:** `simulation/SimulationManager.py`
- **Methods:** `run_full_optimization()`, `run_single_config_test()`
- **Tests:** `tests/simulation/test_SimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
import warnings

def run_full_optimization(self) -> Path:
    """
    DEPRECATED: Use run_iterative_optimization() instead.
    Does not support historical multi-season simulation.
    """
    warnings.warn(
        "run_full_optimization is deprecated. Use run_iterative_optimization().",
        DeprecationWarning
    )
    # ... existing code unchanged ...
```

---

## Phase 2: SimulatedLeague Changes

### Task 2.1: Add Week Data Cache and Pre-loading

- **File:** `simulation/SimulatedLeague.py`
- **Attribute:** `self.week_data_cache: Dict[int, Dict]`
- **Method:** `_preload_all_weeks() -> None`
- **Tests:** `tests/simulation/test_SimulatedLeague.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def __init__(self, config_dict: dict, data_folder: Path) -> None:
    # ... existing init ...
    self.week_data_cache: Dict[int, Dict] = {}
    self._preload_all_weeks()

def _preload_all_weeks(self) -> None:
    """Pre-load all 17 weeks of player data into memory."""
    for week_num in range(1, 18):
        week_folder = self.data_folder / "weeks" / f"week_{week_num:02d}"
        players_file = week_folder / "players.csv"
        if players_file.exists():
            self.week_data_cache[week_num] = self._parse_players_csv(players_file)
```

### Task 2.2: Add CSV Parsing Method

- **File:** `simulation/SimulatedLeague.py`
- **Method:** `_parse_players_csv(filepath: Path) -> Dict[int, Dict]`
- **Tests:** `tests/simulation/test_SimulatedLeague.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def _parse_players_csv(self, filepath: Path) -> Dict[int, Dict]:
    """Parse players.csv into dictionary format."""
    players = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            player_id = int(row['id'])
            players[player_id] = row
    return players
```

### Task 2.3: Add/Update Load Week Data Method

- **File:** `simulation/SimulatedLeague.py`
- **Method:** `_load_week_data(week_num: int) -> None`
- **Tests:** `tests/simulation/test_SimulatedLeague.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def _load_week_data(self, week_num: int) -> None:
    """Load week data from pre-loaded cache (NO disk I/O)."""
    if week_num not in self.week_data_cache:
        raise ValueError(f"Week {week_num} not in cache")

    week_player_data = self.week_data_cache[week_num]

    # Share with all teams - no copying, no disk reads
    for team in self.teams:
        team.projected_pm.set_player_data(week_player_data)
        team.actual_pm.set_player_data(week_player_data)
```

### Task 2.4: Update run_season for 17 Weeks with Cached Data

- **File:** `simulation/SimulatedLeague.py`
- **Method:** `run_season()`
- **Tests:** `tests/simulation/test_SimulatedLeague.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def run_season(self) -> None:
    """Simulate 17-week regular season with pre-loaded week-specific data."""
    for week_num in range(1, 18):  # Changed from range(1, 17)
        self._load_week_data(week_num)  # Load from cache
        self._update_team_rankings(week_num)
        matchups = self.season_schedule[week_num - 1]
        week = Week(week_num, matchups)
        week.simulate_week()
        self.week_results.append(week)
```

### Task 2.5: Update Schedule Generation for 17 Weeks

- **File:** `simulation/SimulatedLeague.py`
- **Method:** `_generate_schedule()`
- **Tests:** `tests/simulation/test_SimulatedLeague.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# BEFORE:
self.season_schedule = generate_schedule_for_nfl_season(self.teams, num_weeks=16)

# AFTER:
self.season_schedule = generate_schedule_for_nfl_season(self.teams, num_weeks=17)
```

### Task 2.6: Update Week.py Validation for 17 Weeks

- **File:** `simulation/Week.py`
- **Method:** `__init__()`
- **Lines:** 73, 79-80
- **Tests:** `tests/simulation/test_Week.py`
- **Status:** [ ] Not started
- **Found in:** Iteration 2 (Error Handling)

**Implementation details:**
```python
# BEFORE (line 73 docstring):
week_number (int): Week number (1-16)

# AFTER:
week_number (int): Week number (1-17)

# BEFORE (line 79):
if not (1 <= week_number <= 16):

# AFTER:
if not (1 <= week_number <= 17):

# BEFORE (line 80):
raise ValueError(f"Week number must be between 1 and 16, got {week_number}")

# AFTER:
raise ValueError(f"Week number must be between 1 and 17, got {week_number}")
```

---

## Phase 3: PlayerManager Changes

### Task 3.1: Add set_player_data Method

- **File:** `league_helper/util/PlayerManager.py`
- **Method:** `set_player_data(player_data: Dict[int, Dict]) -> None`
- **Tests:** `tests/league_helper/util/test_PlayerManager.py`
- **Status:** [ ] Not started
- **Simplified:** Uses existing `FantasyPlayer.from_dict()` (found at utils/FantasyPlayer.py:141)

**Implementation details:**
```python
def set_player_data(self, player_data: Dict[int, Dict]) -> None:
    """Set player data from pre-parsed dictionary (no disk I/O).

    Uses existing FantasyPlayer.from_dict() pattern for consistency.
    """
    self.players = []
    for player_id, data in player_data.items():
        player = FantasyPlayer.from_dict(data)  # Reuse existing classmethod
        self.players.append(player)

    # Recalculate max_projection for normalization
    self.max_projection = max((p.fantasy_points for p in self.players), default=0.0)
    self.scoring_calculator.max_projection = self.max_projection

    # Reload team with new player data
    self.load_team()
```

### Task 3.2: REMOVED - Use Existing FantasyPlayer.from_dict()

- **Status:** [x] Not needed - `FantasyPlayer.from_dict()` already exists at `utils/FantasyPlayer.py:141`
- **Found in:** Iteration 8 (Round 2 verification)
- **Original task removed:** No new method needed, reuse existing classmethod

---

## Phase 4: Testing

### Task 4.1: Unit Tests for Season Discovery

- **File:** `tests/simulation/test_SimulationManager.py`
- **New Tests:**
  - `test_discover_seasons_finds_valid_folders`
  - `test_discover_seasons_raises_when_none_exist`
  - `test_validate_season_strict_missing_files`
  - `test_validate_season_strict_missing_weeks`
- **Status:** [ ] Not started

### Task 4.2: Unit Tests for Week Data Loading

- **File:** `tests/simulation/test_SimulatedLeague.py`
- **New Tests:**
  - `test_preload_all_weeks_caches_17_weeks`
  - `test_parse_players_csv_returns_dict`
  - `test_load_week_data_from_cache`
  - `test_load_week_data_raises_for_missing_week`
- **Status:** [ ] Not started

### Task 4.3: Unit Tests for PlayerManager New Methods

- **File:** `tests/league_helper/util/test_PlayerManager.py`
- **New Tests:**
  - `test_set_player_data_updates_players`
  - `test_set_player_data_recalculates_scores`
  - `test_create_player_from_dict`
- **Status:** [ ] Not started

### Task 4.4: Integration Tests for Multi-Season Simulation

- **File:** `tests/integration/test_simulation_integration.py`
- **New Tests:**
  - `test_iterative_optimization_runs_all_seasons`
  - `test_results_aggregated_across_seasons`
  - `test_17_week_season_simulation`
- **Status:** [ ] Not started

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| `_discover_seasons()` | SimulationManager.py | `__init__()` | SimulationManager.py:91 (after data_folder) | Task 1.3 |
| `_validate_season_strict()` | SimulationManager.py | `_discover_seasons()` | SimulationManager.py:NEW | Task 1.1 |
| `_run_season_simulations()` | SimulationManager.py | `run_iterative_optimization()` | SimulationManager.py:519 area | Task 1.4 |
| `_preload_all_weeks()` | SimulatedLeague.py | `__init__()` | SimulatedLeague.py:119 area | Task 2.1 |
| `_load_week_data()` | SimulatedLeague.py | `run_season()` | SimulatedLeague.py:298 | Task 2.4 |
| `set_player_data()` | PlayerManager.py | `_load_week_data()` | SimulatedLeague.py:NEW | Task 2.3 |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Q1: Season Loop | Discover seasons with glob `20*/` | SimulationManager._discover_seasons() | Fail if no folders |
| Q1: Validation | Validate all 17 weeks exist | SimulationManager._validate_season_strict() | Fail loudly on missing |
| Q1: Parallel | Run all seasons in parallel per config | SimulationManager.run_iterative_optimization() | ThreadPoolExecutor |
| Q2: Pre-load | Cache all 17 weeks at init | SimulatedLeague._preload_all_weeks() | Parse each week CSV |
| Q2: Shared data | Share parsed data across teams | SimulatedLeague._load_week_data() | Reference same dict |
| Week 17 | Simulate 17 weeks | SimulatedLeague.run_season() | range(1, 18) |

---

## Data Flow Traces

### Requirement: Season Discovery
```
Entry: run_simulation.py
  → SimulationManager.__init__()
  → SimulationManager._discover_seasons()  ← NEW
  → SimulationManager._validate_season_strict()  ← NEW
  → Output: self.available_seasons = [2021, 2022, 2023, 2024]
```

### Requirement: Multi-Season Iteration
```
Entry: run_simulation.py
  → SimulationManager.run_iterative_optimization()
  → ThreadPoolExecutor (parallel)  ← NEW
  → SimulationManager._run_season_simulations()  ← NEW
  → ParallelLeagueRunner.run_simulations_for_config_with_weeks()
  → Output: Aggregated results across all seasons
```

### Requirement: Week-Specific Data Loading
```
Entry: SimulatedLeague.__init__()
  → SimulatedLeague._preload_all_weeks()  ← NEW
  → SimulatedLeague._parse_players_csv()  ← NEW
  → (17 weeks cached in self.week_data_cache)

Entry: SimulatedLeague.run_season()
  → SimulatedLeague._load_week_data(week_num)  ← NEW
  → PlayerManager.set_player_data()  ← NEW
  → Output: Teams updated with week-specific player data
```

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:** {to be filled during iteration 6}
- **Corrections made:** {to be filled during iteration 6}
- **Confidence level:** {to be filled}

### Round 2 (Iteration 13)
- **Verified correct:** {to be filled during iteration 13}
- **Corrections made:** {to be filled during iteration 13}
- **Confidence level:** {to be filled}

### Round 3 (Iteration 22)
- **Verified correct:** {to be filled during iteration 22}
- **Corrections made:** {to be filled during iteration 22}
- **Confidence level:** {to be filled}

---

## Progress Notes

**Last Updated:** 2024-12-06
**Current Status:** TODO file created from specs, ready for verification iterations
**Next Steps:** Complete first verification round (7 iterations)
**Blockers:** None
