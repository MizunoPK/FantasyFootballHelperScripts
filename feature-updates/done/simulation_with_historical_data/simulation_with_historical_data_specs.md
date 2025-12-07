# Simulation with Historical Data

## Objective

Update the simulation system to test configurations across ALL available historical NFL seasons (stored in `sim_data/20XX/` folders), aggregating win rates across seasons to produce more robust and validated results.

---

## High-Level Requirements

### 1. Season Discovery

- **Detection:** Find all `20XX/` folders in `simulation/sim_data/` directory
- **Validation:** Verify each folder contains required structure
- **Minimum:** At least one valid season required to run simulation

### 2. Multi-Season Simulation Loop

- **Per Config:** Each configuration tested must run through ALL discovered seasons
- **Aggregation:** Win rates reflect total wins and losses across ALL seasons
- **Independence:** Each season simulation is independent (fresh draft, fresh matchups)

### 3. Draft Simulation (Per Season)

- **Data Source:** Load from `{YEAR}/weeks/week_01/` folder
- **Player File:** `players.csv` - Contains draft-relevant player data
- **Projection File:** `players_projected.csv` - Contains projected points for drafting

### 4. Weekly Match Simulation (Per Season)

- **Data Source:** Load from `{YEAR}/weeks/week_XX/` for each week 1-17
- **Player File:** `players.csv` - Contains "smart values" (actuals for past weeks from that point-in-time, projections for future)
- **Use:** Determine starters, calculate scores, determine winners

### 5. Output/Deliverables

- Optimal configs should reflect performance across all tested seasons
- Results aggregated across seasons (total wins, total losses, combined win rate)
- Output format remains compatible with existing consumers

---

## Open Questions (To Be Resolved)

### Data Loading Questions

1. **Week-specific data loading:** How should the simulation load week-specific files?
   - Currently loads single `players.csv` from `sim_data/`
   - Need to load `{YEAR}/weeks/week_XX/players.csv` per week

2. **Team data loading:** How should team rankings/matchup data be loaded?
   - Historical compiler creates `team_data/{TEAM}.csv` per season
   - Current system uses `teams_week_X.csv` files

3. **Schedule data:** How do we get bye weeks and schedule for each season?
   - Historical compiler creates `season_schedule.csv` per year

### Architecture Questions

4. **Where to add season loop?** Which class/method should iterate over seasons?
   - SimulationManager? ParallelLeagueRunner? ConfigGenerator?

5. **How to pass season context?** How does week-specific data path flow through the system?
   - Constructor? Method parameters? Global state?

6. **ConfigManager changes?** Does ConfigManager need to handle season-specific config?

### Algorithm Questions

7. **Win rate aggregation:** How to aggregate across seasons?
   - Total wins / total games across all seasons?
   - Average win rate per season?

8. **Handling variable season count:** What if one config fails on a specific season?
   - Skip that config entirely?
   - Mark as incomplete?

### Error Handling Questions

9. **Incomplete season data:** What if a season folder is missing weeks?
   - Skip that season? Fail loudly? Warn and continue?

10. **Missing files in week folder:** What if `players.csv` or `players_projected.csv` is missing?
    - Skip that week? Fail the season?

---

## Resolved Implementation Details

### Q1: Season Loop Location → SimulationManager

**Decision:** Add season iteration at the SimulationManager level.

**Implementation:**

```python
# SimulationManager.__init__()
def __init__(self, ...):
    # ... existing init ...
    self.available_seasons = self._discover_seasons()
    self.logger.info(f"Discovered {len(self.available_seasons)} historical seasons")

def _discover_seasons(self) -> List[Path]:
    """
    Find all valid 20XX/ season folders in data_folder.

    Returns:
        List[Path]: Valid season folders

    Raises:
        FileNotFoundError: If no valid season folders found
        ValueError: If any season folder has invalid structure
    """
    season_folders = sorted(self.data_folder.glob("20*/"))

    if not season_folders:
        raise FileNotFoundError(
            f"No historical season folders (20XX/) found in {self.data_folder}. "
            "Run compile_historical_data.py first."
        )

    # Validate each season folder - fail loudly if any are invalid
    valid = []
    for folder in season_folders:
        self._validate_season_strict(folder)  # Raises on invalid
        valid.append(folder)

    self.logger.info(f"Discovered {len(valid)} valid seasons: {[f.name for f in valid]}")
    return valid

def _validate_season_strict(self, folder: Path) -> None:
    """
    Strictly validate season folder structure. Raises on any missing data.

    Args:
        folder: Path to season folder (e.g., sim_data/2024/)

    Raises:
        FileNotFoundError: If required files/folders are missing
    """
    year = folder.name

    # Check required top-level files
    required_files = [
        folder / "season_schedule.csv",
        folder / "game_data.csv",
    ]
    for req_file in required_files:
        if not req_file.exists():
            raise FileNotFoundError(f"Season {year} missing required file: {req_file.name}")

    # Check team_data folder
    team_data = folder / "team_data"
    if not team_data.exists():
        raise FileNotFoundError(f"Season {year} missing team_data/ folder")

    # Check weeks folder
    weeks_folder = folder / "weeks"
    if not weeks_folder.exists():
        raise FileNotFoundError(f"Season {year} missing weeks/ folder")

    # Check all 17 weeks exist with required files
    for week_num in range(1, 18):
        week_folder = weeks_folder / f"week_{week_num:02d}"
        if not week_folder.exists():
            raise FileNotFoundError(f"Season {year} missing week folder: week_{week_num:02d}/")

        players_file = week_folder / "players.csv"
        if not players_file.exists():
            raise FileNotFoundError(f"Season {year} week_{week_num:02d}/ missing players.csv")
```

**Changes to run_iterative_optimization() - OPTIMIZED:**

```python
def run_iterative_optimization(self):
    # ... existing setup ...

    for param_idx, param_name in enumerate(param_order):
        for config in configs:
            # OPTIMIZED: Run all seasons in PARALLEL
            all_season_results = []

            with ThreadPoolExecutor(max_workers=len(self.available_seasons)) as season_executor:
                # Submit all seasons simultaneously
                future_to_season = {
                    season_executor.submit(
                        self._run_season_simulations,
                        config,
                        season_folder
                    ): season_folder
                    for season_folder in self.available_seasons
                }

                # Collect results as they complete
                for future in as_completed(future_to_season):
                    season_results = future.result()
                    all_season_results.extend(season_results)

            # Record aggregated results across all seasons
            for week_results in all_season_results:
                self.results_manager.record_week_results(config_id, week_results)

def _run_season_simulations(
    self,
    config: dict,
    season_folder: Path
) -> List[List[Tuple[int, bool, float]]]:
    """
    Run simulations for a single season (called in parallel).

    Args:
        config: Configuration dictionary
        season_folder: Path to season data (e.g., sim_data/2024/)

    Returns:
        List of per-simulation week results
    """
    # Reuse single runner instance per season (not per call)
    runner = ParallelLeagueRunner(
        max_workers=self.max_workers,
        data_folder=season_folder
    )
    return runner.run_simulations_for_config_with_weeks(
        config,
        self.num_simulations_per_config
    )
```

**Optimization: Parallel Season Execution**
- All 4 seasons run simultaneously (4× speedup potential)
- Each season gets its own thread with dedicated ParallelLeagueRunner
- Results aggregated as seasons complete

**Key Points:**
- Season discovery happens ONCE at `__init__`
- Each config is tested against ALL discovered seasons IN PARALLEL
- Results are aggregated across seasons before recording
- Backwards compatible: Falls back to flat structure if no `20XX/` folders exist

---

### Scope Limitation: Deprecate Unused Simulation Modes

**Decision:** Only update `run_iterative_optimization()` for historical data support.

**Deprecated Methods (do not update):**
- `run_full_optimization()` - Mark with `@deprecated` or docstring warning
- `run_single_config_test()` - Mark with `@deprecated` or docstring warning

**Rationale:** These modes are not used in practice. Focusing on iterative mode reduces implementation scope and testing burden.

**Implementation:**
```python
def run_full_optimization(self) -> Path:
    """
    DEPRECATED: Use run_iterative_optimization() instead.

    This method does not support historical multi-season simulation.
    It remains for backwards compatibility but will be removed in a future version.
    """
    warnings.warn(
        "run_full_optimization is deprecated. Use run_iterative_optimization() instead.",
        DeprecationWarning
    )
    # ... existing code unchanged ...
```

---

### Restore Week 17 to Simulation

**Decision:** Change simulation from 16 weeks to 17 weeks.

**Background:** Week 17 was previously removed due to data corruption in the old data format. The new historical data compiler produces clean week 17 data.

**Changes Required:**

```python
# SimulatedLeague.py - run_season()
# BEFORE:
for week_num in range(1, 17):  # Weeks 1-16

# AFTER:
for week_num in range(1, 18):  # Weeks 1-17
```

```python
# SimulatedLeague.py - _generate_schedule()
# BEFORE:
self.season_schedule = generate_schedule_for_nfl_season(self.teams, num_weeks=16)

# AFTER:
self.season_schedule = generate_schedule_for_nfl_season(self.teams, num_weeks=17)
```

**Impact:**
- Each simulation now has 17 matchups instead of 16
- Win rates based on 17 games per season
- Historical data has all 17 weeks available

---

### Q2: Week-Specific Data Loading → FULLY OPTIMIZED

**Decision:** Pre-load all weeks + share data across teams for maximum performance.

**Optimizations Applied:**
1. **Pre-load all 17 weeks at simulation init** - moves disk I/O out of hot path
2. **Share parsed data across all 10 teams** - eliminates redundant CSV parsing
3. **No file copying** - direct memory references

**Performance Comparison:**

| Approach | CSV Parses/Sim | Disk Reads/Sim | Memory |
|----------|----------------|----------------|--------|
| Original (copy files) | 340 | 340 | High (copies) |
| Direct folder ref | 340 | 340 | Low |
| **Shared + Pre-load** | **17** | **17** | Medium (cache) |

**Implementation - SimulatedLeague.py:**

```python
class SimulatedLeague:
    def __init__(self, config_dict: dict, data_folder: Path) -> None:
        # ... existing init ...

        # OPTIMIZATION: Pre-load all 17 weeks into memory at init
        self.week_data_cache: Dict[int, Dict] = {}
        self._preload_all_weeks()

        # Initialize teams
        self._initialize_teams()
        self._generate_schedule()

    def _preload_all_weeks(self) -> None:
        """
        Pre-load all 17 weeks of player data into memory.

        Moves all disk I/O to initialization phase for faster run_season().
        Each week's data is parsed ONCE and shared across all teams.
        """
        self.logger.debug("Pre-loading all 17 weeks of player data")

        for week_num in range(1, 18):
            week_folder = self.data_folder / "weeks" / f"week_{week_num:02d}"
            players_file = week_folder / "players.csv"

            if players_file.exists():
                # Parse CSV once, store in cache
                self.week_data_cache[week_num] = self._parse_players_csv(players_file)
            else:
                self.logger.warning(f"Missing players.csv for week {week_num}")

        self.logger.debug(f"Pre-loaded {len(self.week_data_cache)} weeks into cache")

    def _parse_players_csv(self, filepath: Path) -> Dict[int, Dict]:
        """
        Parse players.csv into dictionary format.

        Returns:
            Dict mapping player_id -> player_data dict
        """
        players = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                player_id = int(row['id'])
                players[player_id] = row
        return players

    def _load_week_data(self, week_num: int) -> None:
        """
        Load week data from pre-loaded cache (NO disk I/O).

        OPTIMIZATION: Data is shared read-only across all teams.
        """
        if week_num not in self.week_data_cache:
            raise ValueError(f"Week {week_num} not in cache - was it pre-loaded?")

        # Get cached data (single reference, shared across teams)
        week_player_data = self.week_data_cache[week_num]

        # Share with all teams - no copying, no disk reads
        for team in self.teams:
            team.projected_pm.set_player_data(week_player_data)
            team.actual_pm.set_player_data(week_player_data)

    def run_season(self) -> None:
        """Simulate 17-week regular season with pre-loaded week-specific data."""
        self.logger.debug("Starting 17-week season simulation")

        for week_num in range(1, 18):  # Weeks 1-17
            # Load from cache - instant, no disk I/O
            self._load_week_data(week_num)

            # Update team rankings for this week
            self._update_team_rankings(week_num)

            # Get matchups and simulate
            matchups = self.season_schedule[week_num - 1]
            week = Week(week_num, matchups)
            week.simulate_week()
            self.week_results.append(week)

        self.logger.debug("Season complete: 17 weeks simulated")
```

**Implementation - PlayerManager.py:**

```python
def set_player_data(self, player_data: Dict[int, Dict]) -> None:
    """
    Set player data from pre-parsed dictionary (no disk I/O).

    Used for sharing week data across teams in simulation.
    Data is treated as read-only - no modifications.

    Args:
        player_data: Dict mapping player_id -> player attributes
    """
    self.players = {}
    for player_id, data in player_data.items():
        # Create FantasyPlayer from dict data
        self.players[player_id] = self._create_player_from_dict(data)

    # Recalculate scores with new player data
    self._calculate_scores()

def _create_player_from_dict(self, data: Dict) -> FantasyPlayer:
    """Create FantasyPlayer instance from dictionary data."""
    return FantasyPlayer(
        id=int(data['id']),
        name=data['name'],
        position=data['position'],
        team=data['team'],
        fantasy_points=float(data.get('fantasy_points', 0)),
        projected_points=float(data.get('projected_points', 0)),
        player_rating=float(data.get('player_rating', 50)),
        bye_week=int(data.get('bye_week', 0)),
        # ... other fields as needed
    )
```

**Performance Summary:**
- **17 CSV parses per simulation** (down from 340) - 20× improvement
- **17 disk reads per simulation** (down from 340) - 20× improvement
- **Zero file copies** - eliminated entirely
- **Shared memory** - all teams reference same parsed data

---

## Codebase Investigation Findings

### Current Data Flow

```
run_simulation.py (entry point)
  └── SimulationManager.__init__(data_folder=sim_data/)
        └── ParallelLeagueRunner.__init__(data_folder)
              └── run_single_simulation()
                    └── SimulatedLeague.__init__(config_dict, data_folder)
                          └── _initialize_teams()
                                - Copies players_projected.csv → team temp dir
                                - Copies players_actual.csv → team temp dir
                                - Copies season_schedule.csv, game_data.csv
                                - Copies team_data/ folder
                          └── run_draft()
                                - Uses copied players_projected.csv
                          └── run_season()
                                - Runs weeks 1-16
                                - Uses SAME player data for all weeks
```

### Key Files and Their Roles

| File | Current Role | Location |
|------|--------------|----------|
| `SimulationManager.py` | Orchestrates configs, creates ParallelLeagueRunner | Lines 59-114: receives data_folder, passes to runner |
| `ParallelLeagueRunner.py` | Runs simulations in parallel | Lines 76-129: creates SimulatedLeague per simulation |
| `SimulatedLeague.py` | Single season simulation | Lines 124-212: copies data files to temp dirs, runs draft + 16 weeks |
| `Week.py` | Single week matchup | Simulates matchups, calculates scores |

### Current Data Structure (Flat)

```
sim_data/
├── players_projected.csv   # Used for draft decisions (ALL weeks)
├── players_actual.csv      # Used for scoring (ALL weeks)
├── season_schedule.csv     # Bye weeks, schedule
├── game_data.csv           # Weather, location
└── team_data/              # Per-team ranking data
    ├── KC.csv
    └── ...
```

### Historical Data Structure (Confirmed - 4 seasons exist)

```
sim_data/
├── 2021/
├── 2022/
├── 2023/
└── 2024/
    ├── season_schedule.csv
    ├── game_data.csv
    ├── team_data/
    │   ├── KC.csv
    │   └── ...
    └── weeks/
        ├── week_01/
        │   ├── players.csv           # "Smart values" snapshot at week 1
        │   └── players_projected.csv # Projections at week 1
        ├── week_02/
        │   ├── players.csv
        │   └── players_projected.csv
        └── ... (through week_17)
```

### Critical Changes Required

1. **SimulatedLeague._initialize_teams()** (lines 124-212)
   - Currently copies SINGLE player files once at init
   - Need to change to load WEEK-SPECIFIC files dynamically

2. **SimulatedLeague.run_season()** (lines 283-314)
   - Currently uses same data for all 16 weeks
   - Need to reload player data for EACH week from `weeks/week_XX/`

3. **Season Loop Location**
   - Most likely: Add loop in ParallelLeagueRunner or SimulationManager
   - Each season = independent SimulatedLeague instance with different data_folder

### Data File Mapping

| Current File | Historical Equivalent | Usage |
|--------------|----------------------|-------|
| `players_projected.csv` | `{YEAR}/weeks/week_01/players.csv` | Draft decisions |
| `players_actual.csv` | `{YEAR}/weeks/week_XX/players.csv` | Weekly scoring (per week) |
| `season_schedule.csv` | `{YEAR}/season_schedule.csv` | Bye weeks |
| `game_data.csv` | `{YEAR}/game_data.csv` | Weather/location |
| `team_data/{TEAM}.csv` | `{YEAR}/team_data/{TEAM}.csv` | Team rankings |

---

## Implementation Notes

### Files to Modify

| File | Changes | Complexity |
|------|---------|------------|
| `simulation/SimulationManager.py` | Add season discovery, loop over seasons | Medium |
| `simulation/ParallelLeagueRunner.py` | Pass season year to SimulatedLeague | Low |
| `simulation/SimulatedLeague.py` | Major refactor for week-specific loading | High |
| `simulation/ResultsManager.py` | Aggregate results across seasons | Medium |

### Dependencies

- Historical data must be compiled first (`compile_historical_data.py --year XXXX`)
- At least one valid `20XX/` folder must exist in `sim_data/`
- All 4 seasons currently available: 2021, 2022, 2023, 2024

### Reusable Code

- `historical_data_compiler/` modules for understanding data format
- Existing simulation infrastructure (just needs data source updates)
- `SimulatedLeague._update_team_rankings()` pattern for weekly updates

### Testing Strategy

- Unit tests for season discovery (glob `20*/` folders)
- Unit tests for week-specific data loading
- Integration tests verifying multi-season simulation produces aggregated results
- Verify results are consistent when run multiple times
- Compare single-season vs multi-season results

---

## Status: PLANNING
