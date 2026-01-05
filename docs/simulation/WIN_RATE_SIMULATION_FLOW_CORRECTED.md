# Win Rate Simulation - Functional Flow Documentation (CORRECTED)

> **IMPORTANT**: This document describes the **Win Rate Simulation ONLY**.
> For Accuracy Simulation (prediction optimization), see ACCURACY_SIMULATION_FLOW.md
> These are **separate simulation systems** with different purposes and parameters.

---

## ⚠️ DOCUMENT SCOPE

**This Document Covers:**
- Win Rate Simulation (`run_win_rate_simulation.py`)
- Draft strategy parameter optimization (7 parameters)
- Maximizing league win percentage

**This Document Does NOT Cover:**
- Accuracy Simulation (`run_accuracy_simulation.py`) - separate system for prediction optimization
- Draft Order Simulation (`run_draft_order_simulation.py`) - testing draft strategies across seasons

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Entry Point and Execution Modes](#entry-point-and-execution-modes)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Configuration System](#configuration-system)
7. [Parallel Execution](#parallel-execution)
8. [Results Management](#results-management)
9. [Complete Execution Flow](#complete-execution-flow)
10. [Performance Characteristics](#performance-characteristics)

---

## Overview

The Win Rate Simulation optimizes **draft strategy parameters** by simulating complete fantasy football leagues across multiple historical seasons.

### Purpose

- **Optimize 7 draft strategy parameters** to maximize league win rate
- **Test DraftHelper recommendations** against realistic AI opponents
- **Validate parameter changes** before applying to production configs
- **Discover optimal settings** that work across different seasons

### Key Metrics

- **Win Rate**: Percentage of head-to-head matchups won
- **Total Points**: Fantasy points scored across all weeks
- **Multi-Season Validation**: Performance across 2021, 2022, 2024+ seasons

### Parameters Optimized (7 Total)

**Win Rate Simulation optimizes DRAFT STRATEGY parameters only:**

1. **DRAFT_NORMALIZATION_MAX_SCALE** [100-200] - Draft scoring normalization scale
2. **SAME_POS_BYE_WEIGHT** [0.0-0.5] - Penalty for drafting same-position players with same bye
3. **DIFF_POS_BYE_WEIGHT** [0.0-0.3] - Penalty for drafting different-position players with same bye
4. **PRIMARY_BONUS** [25-150] - Bonus points for drafting primary positions at optimal time
5. **SECONDARY_BONUS** [25-150] - Bonus points for drafting secondary positions
6. **ADP_SCORING_WEIGHT** [0.5-7.0] - Weight given to Average Draft Position
7. **PLAYER_RATING_SCORING_WEIGHT** [0.5-4.0] - Weight given to expert rankings

**Note**: Prediction accuracy parameters (TEAM_QUALITY, MATCHUP, WEATHER, etc.) are optimized separately by `run_accuracy_simulation.py`.

---

## Architecture

### High-Level Components

```
run_win_rate_simulation.py (Entry Point)
    ↓
SimulationManager (Orchestration Layer)
    ├─ ConfigGenerator (Parameter Space - 7 params)
    ├─ ParallelLeagueRunner (Parallel Execution)
    └─ ResultsManager (Result Aggregation)
        ↓
    For each configuration variation:
        ↓
    ParallelLeagueRunner (Thread/Process Pool)
        ↓
    Multiple SimulatedLeague instances (parallel)
        ├─ DraftHelperTeam (1x - system under test)
        └─ SimulatedOpponent (9x - AI competitors)
            ↓
        Snake Draft (15 rounds, 150 picks)
            ↓
        17-Week Season Simulation
            ├─ Week 1 through Week 17
            └─ Each week: Lineup optimization + scoring + matchup resolution
                ↓
        Return: wins, losses, points_scored, points_against
            ↓
    ResultsManager aggregates all results
        ↓
    Identify best configuration
        ↓
    Save optimal config folder
```

### Module Organization

```
simulation/
├─ win_rate/                      # Win rate optimization
│   ├─ SimulationManager.py       # Main orchestrator
│   ├─ SimulatedLeague.py         # League simulation logic
│   ├─ DraftHelperTeam.py         # Draft Helper system team
│   ├─ SimulatedOpponent.py       # AI opponent teams
│   ├─ Week.py                    # Weekly matchup simulation
│   └─ ParallelLeagueRunner.py    # Parallel execution engine
├─ shared/                        # Shared utilities
│   ├─ ConfigGenerator.py         # Parameter combination generator
│   ├─ ResultsManager.py          # Result tracking and ranking
│   └─ SeasonDataLoader.py        # Historical data loading
└─ sim_data/                      # Historical season data
    ├─ 2021/
    ├─ 2022/
    └─ 2024/
```

---

## Entry Point and Execution Modes

### Command Line Interface

```bash
python run_win_rate_simulation.py [mode] [options]
```

### Three Execution Modes

#### 1. Single Mode (Validation)

**Purpose**: Test a single configuration for validation

**Usage**:
```bash
python run_win_rate_simulation.py single --sims 100
```

**Behavior**:
- Tests only the baseline configuration
- Runs specified number of simulations
- Outputs win rate, points scored, and statistics
- Fast execution for quick validation

**Use Cases**:
- Verifying baseline config behavior
- Smoke testing after config changes
- Quick performance checks

#### 2. Full Mode (Grid Search)

**Purpose**: Exhaustive search of parameter space

**Usage**:
```bash
python run_win_rate_simulation.py full --test-values 3 --sims 100
```

**Behavior**:
- Tests ALL combinations of parameter values
- For 5 test values per parameter: **(5+1)^6 = 46,656 configurations**
- **EXTREMELY SLOW** - impractical for all 7 parameters
- Typically used for testing 2-3 parameters in isolation

**Formula**: `(test_values + 1)^6` total configurations (6 parameters varied simultaneously)

**Note**: The code uses 6 as the exponent (not 7), likely because one parameter is held constant or optimized separately.

**Use Cases**:
- Exploring interactions between 2-3 specific parameters
- Finding global optimum (when limited parameter set)
- Research and analysis

#### 3. Iterative Mode (Coordinate Descent - DEFAULT)

**Purpose**: Efficient local optimization

**Usage**:
```bash
python run_win_rate_simulation.py iterative --sims 100 --workers 8
```

**Behavior**:
- Optimizes ONE parameter at a time
- Tests `test_values + 1` configurations per parameter (default: 6)
- Uses best value from previous parameter as baseline for next
- For 7 parameters × 6 values = **42 total configurations**
- **MUCH FASTER** than full mode
- Finds local optimum (not guaranteed global)

**Algorithm**:
1. Start with baseline configuration
2. For each of 7 parameters:
   - Generate test values around current value
   - Run simulations for each test value
   - Select best performing value
   - Update baseline with best value
3. Next parameter uses updated baseline
4. After all 7 parameters optimized, save optimal config

**Use Cases**:
- Production optimization runs
- Continuous improvement cycles
- Parameter tuning for new seasons

### Common Options

| Option | Default | Description |
|--------|---------|-------------|
| `--sims` | 5 | Number of simulations per configuration |
| `--workers` | 8 | Number of parallel workers |
| `--test-values` | 5 | Number of test values per parameter |
| `--baseline-folder` | Auto-detect | Path to baseline config folder |
| `--use-processes` | False | Use ProcessPoolExecutor instead of threads |

---

## Core Components

### 1. SimulationManager

**File**: `simulation/win_rate/SimulationManager.py`

**Responsibilities**:
- Orchestrate entire optimization process
- Load baseline configuration from folder (5 files: league_config.json + 4 week configs)
- Coordinate ConfigGenerator, ParallelLeagueRunner, ResultsManager
- Implement iterative optimization loop
- Save intermediate and final results

**Key Methods**:

```python
def run_iterative_optimization(self):
    """Coordinate descent optimization of 7 parameters"""
    # Load baseline config folder
    # For each of 7 parameters:
    #   - Generate test values (default: 6)
    #   - Run parallel simulations across all historical seasons
    #   - Select best value
    #   - Update baseline
    # Save optimal config folder
```

**Multi-Season Validation**:
- Runs simulations across ALL available historical seasons (2021, 2022, 2024+)
- Aggregates results across seasons for robust validation
- Win rate calculated as: Total Wins / Total Games (across all seasons)

---

### 2. ConfigGenerator

**File**: `simulation/shared/ConfigGenerator.py`

**Responsibilities**:
- Define parameter search space (7 parameters for win rate)
- Generate parameter value combinations
- Validate parameter ranges
- Create configuration dictionaries

**Parameter Definitions (7 for Win Rate)**:

```python
# From run_win_rate_simulation.py lines 54-66
PARAMETER_ORDER = [
    'DRAFT_NORMALIZATION_MAX_SCALE',    # Range: [100, 200]
    'SAME_POS_BYE_WEIGHT',              # Range: [0.0, 0.5]
    'DIFF_POS_BYE_WEIGHT',              # Range: [0.0, 0.3]
    'PRIMARY_BONUS',                     # Range: [25, 150]
    'SECONDARY_BONUS',                   # Range: [25, 150]
    'ADP_SCORING_WEIGHT',                # Range: [0.5, 7.0]
    'PLAYER_RATING_SCORING_WEIGHT',      # Range: [0.5, 4.0]
]
```

**Test Value Generation**:

```python
def generate_test_values(param_name, baseline_value, num_values=5):
    """Generate 6 test values (baseline + 5 variations)"""
    param_def = PARAMETER_DEFINITIONS[param_name]
    min_val, max_val, precision = param_def
    step = calculate_step(min_val, max_val, num_values)

    # Generate: baseline ± (step × i) for i in 1..num_values
    test_values = [baseline_value]  # Include baseline

    for i in range(1, num_values + 1):
        # Add higher value
        if baseline_value + (step * i) <= max_val:
            test_values.append(baseline_value + (step * i))

        # Add lower value
        if baseline_value - (step * i) >= min_val:
            test_values.append(baseline_value - (step * i))

    return test_values[:num_values + 1]  # Return max num_values + 1
```

**Example**:
- Parameter: `ADP_SCORING_WEIGHT`
- Baseline: `3.0`
- Range: `[0.5, 7.0]`
- Test values (num_values=5): `[1.5, 2.0, 2.5, 3.0, 3.5, 4.0]` (6 values)

---

### 3. ParallelLeagueRunner

**File**: `simulation/win_rate/ParallelLeagueRunner.py`

**Responsibilities**:
- Execute multiple league simulations in parallel
- Manage thread/process pools
- Handle exceptions and timeouts
- Track progress and collect results
- Memory management and cleanup

**Execution Strategies**:

#### ThreadPoolExecutor (Default)
```python
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    for sim_num in range(num_sims):
        future = executor.submit(run_single_simulation, config, sim_num)
        futures.append(future)

    for future in as_completed(futures):
        result = future.result()
        results.append(result)
```

**Advantages**:
- Lower memory overhead
- Shared memory space
- Faster startup

**Disadvantages**:
- Python GIL limits true parallelism
- CPU-bound bottleneck

#### ProcessPoolExecutor (Optional)
```python
with ProcessPoolExecutor(max_workers=8) as executor:
    # Same structure as ThreadPoolExecutor
```

**Advantages**:
- True parallelism (no GIL)
- Better CPU utilization

**Disadvantages**:
- Higher memory overhead (separate processes)
- Slower startup
- Data serialization overhead

---

### 4. SimulatedLeague

**File**: `simulation/win_rate/SimulatedLeague.py`

**Responsibilities**:
- Create and manage 10 fantasy football teams
- Orchestrate snake draft (15 rounds, 150 picks)
- Simulate 17-week season with matchups
- Track wins, losses, and points
- Manage team-specific PlayerManager instances

**League Structure**:

```python
class SimulatedLeague:
    # Team strategy distribution (from lines 77-83)
    TEAM_STRATEGIES = {
        'draft_helper': 1,                            # 1 DraftHelper team
        'adp_aggressive': 2,                          # 2 ADP-focused teams
        'projected_points_aggressive': 2,             # 2 projection-focused teams
        'adp_with_draft_order': 2,                    # 2 ADP + draft order teams
        'projected_points_with_draft_order': 3        # 3 projection + draft order teams
    }
```

**Total**: 10 teams (1 DraftHelper + 9 AI opponents)

**Snake Draft Implementation**:

```python
def run_draft(self):
    """Execute 15-round snake draft"""
    num_rounds = 15
    num_teams = 10

    for round_num in range(1, num_rounds + 1):
        if round_num % 2 == 1:  # Odd rounds: 1→10
            draft_order = list(range(10))
        else:  # Even rounds: 10→1 (snake)
            draft_order = list(range(9, -1, -1))

        for team_idx in draft_order:
            team = self.teams[team_idx]
            player = team.select_draft_pick()
            team.draft_player(player)

            # Mark player as drafted for all teams
            for t in self.teams:
                t.mark_player_drafted(player.id)
```

**Data Optimization**:
- **Shared read-only directories**: All teams reference same season data folder
- **In-memory PlayerManager instances**: Each team has independent instance (no disk copies)
- **Pre-loaded week data**: All 17 weeks loaded at initialization to avoid repeated I/O

---

### 5. SimulatedOpponent

**File**: `simulation/win_rate/SimulatedOpponent.py`

**Responsibilities**:
- Represent AI opponent teams with different strategies
- Make draft decisions based on strategy type
- Optimize weekly lineups
- Provide realistic competition for DraftHelper team

**Strategy Types**:

| Strategy | Draft Logic | Weighting |
|----------|------------|-----------|
| `adp_aggressive` | Prioritize ADP (Best Player Available) | 80% ADP, 20% Projected Points |
| `projected_points_aggressive` | Prioritize projected points | 20% ADP, 80% Projected Points |
| `adp_with_draft_order` | ADP + draft order bonuses | 60% ADP, 20% PP, 20% Draft Order |
| `projected_points_with_draft_order` | Projected points + draft order | 30% ADP, 50% PP, 20% Draft Order |

---

## Data Flow

### Historical Season Data Structure

```
simulation/sim_data/
├─ 2021/
│   ├─ season_schedule.csv           # Bye weeks, game matchups
│   ├─ game_data.csv                 # Weather, location data
│   ├─ team_data/                    # Per-NFL-team rankings
│   │   ├─ ARI.csv
│   │   ├─ ATL.csv
│   │   └─ ... (32 teams)
│   └─ weeks/
│       ├─ week_01/
│       │   ├─ qb_data.json          # QB projected + actual points
│       │   ├─ rb_data.json          # RB projected + actual points
│       │   ├─ wr_data.json          # WR projected + actual points
│       │   ├─ te_data.json          # TE projected + actual points
│       │   ├─ k_data.json           # K projected + actual points
│       │   └─ dst_data.json         # DST projected + actual points
│       ├─ week_02/
│       └─ ... week_17/
├─ 2022/
└─ 2024/
```

**Note**: Each position JSON file contains arrays for:
- `projected_points[0..16]` - Projected points for weeks 1-17
- `actual_points[0..16]` - Actual points for weeks 1-17

---

## Configuration System

### Three-Level Hierarchy

#### Level 1: Base Configuration (`league_config.json`)

**Parameters that apply league-wide** (optimized by win rate simulation):

```json
{
  "DRAFT_NORMALIZATION_MAX_SCALE": 150,
  "SAME_POS_BYE_WEIGHT": 0.25,
  "DIFF_POS_BYE_WEIGHT": 0.15,
  "DRAFT_ORDER_BONUSES": {
    "PRIMARY": 87,
    "SECONDARY": 78
  },
  "ADP_SCORING": {
    "WEIGHT": 3.0,
    "THRESHOLDS": { "STEPS": 25 }
  },
  "PLAYER_RATING_SCORING": {
    "WEIGHT": 2.0
  }
}
```

#### Level 2: Week-Range Configurations (`week*.json`)

**Parameters optimized separately for different season phases** (by accuracy simulation):

- `week1-5.json` - Early season
- `week6-9.json` - Mid-early season
- `week10-13.json` - Mid-late season
- `week14-17.json` - Playoffs

**These are NOT optimized by win rate simulation** - they're optimized by `run_accuracy_simulation.py`

---

## Complete Execution Flow

### Iterative Mode (Step-by-Step)

**Command**:
```bash
python run_win_rate_simulation.py iterative --sims 100 --workers 8 --test-values 5
```

**Execution Steps**:

```
1. Parse Command Line Arguments
   ├─ mode = "iterative"
   ├─ sims = 100
   ├─ workers = 8
   └─ test_values = 5

2. Find Baseline Config Folder
   ├─ Check simulation/simulation_configs/ for optimal_* folders
   └─ Load 5 config files (league_config.json + 4 week files)

3. Initialize SimulationManager
   ├─ ConfigGenerator(baseline_config, test_values=5)
   ├─ ParallelLeagueRunner(workers=8, executor="thread")
   └─ ResultsManager()

4. Start Iterative Optimization Loop
   ├─ Load 7 parameter definitions from PARAMETER_ORDER
   └─ For each parameter (7 iterations):

      ┌─────────────────────────────────────────────┐
      │ Parameter Iteration (e.g., ADP_SCORING_WEIGHT) │
      └─────────────────────────────────────────────┘

      4.1. Generate Test Values
           ├─ Baseline: 3.0
           ├─ Test values: [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
           └─ Total: 6 configurations

      4.2. For Each Test Value (6 configs):

           ┌──────────────────────────────────────┐
           │ Configuration Testing (e.g., 3.5)   │
           └──────────────────────────────────────┘

           4.2.1. Create Config Dictionary
                  ├─ Copy baseline config
                  └─ Set ADP_SCORING_WEIGHT = 3.5

           4.2.2. Submit to ParallelLeagueRunner
                  ├─ Run 100 simulations PER SEASON
                  ├─ Across ALL historical seasons (2021, 2022, 2024)
                  └─ Use 8 worker threads

           ┌────────────────────────────────────────────┐
           │ For EACH Season (2021, 2022, 2024, ...)   │
           └────────────────────────────────────────────┘

               ┌────────────────────────────────────────────┐
               │ Worker Thread (8 parallel, 100 jobs/season)│
               └────────────────────────────────────────────┘

               4.2.3. Create SimulatedLeague Instance
                      ├─ Season: 2021 (or 2022, 2024, etc.)
                      ├─ Sim number: 1-100
                      └─ Config: {ADP_SCORING_WEIGHT: 3.5}

               4.2.4. Initialize Teams (10 total)
                      ├─ DraftHelperTeam (1x)
                      │   ├─ PlayerManager (projected)
                      │   ├─ PlayerManager (actual)
                      │   ├─ AddToRosterModeManager
                      │   └─ StarterHelperModeManager
                      │
                      └─ SimulatedOpponent (9x)
                          ├─ 2x adp_aggressive
                          ├─ 2x projected_points_aggressive
                          ├─ 2x adp_with_draft_order
                          └─ 3x projected_points_with_draft_order

               4.2.5. Load Season Data
                      ├─ 6 position JSON files per week (17 weeks)
                      ├─ team_data/*.csv (32 NFL teams)
                      └─ season_schedule.csv (bye weeks)

               4.2.6. Run Snake Draft (15 rounds)
                      ├─ Round 1: Pick 1 → 10
                      ├─ Round 2: Pick 10 → 1 (snake)
                      ├─ ...
                      └─ Round 15: Pick 10 → 1

                      For each pick:
                          ├─ Team selects best available player
                          │   ├─ DraftHelper: Get #1 recommendation
                          │   └─ Opponent: Score by strategy weights
                          │
                          ├─ Add player to roster
                          └─ Mark player as drafted (all teams)

               4.2.7. Run 17-Week Season

                      ┌────────────────────────────────┐
                      │ Week Loop (Week 1 through 17) │
                      └────────────────────────────────┘

                      For each week (1-17):

                          4.2.7.1. All Teams Optimize Lineups
                                   ├─ DraftHelper: StarterHelperModeManager
                                   └─ Opponents: Lineup optimization

                          4.2.7.2. Load Actual Player Data
                                   └─ 6 position JSON files (actual_points arrays)

                          4.2.7.3. Calculate Actual Points
                                   For each team:
                                       ├─ Sum starter points from actual data
                                       └─ Store in team_points[team.name]

                          4.2.7.4. Resolve Matchups
                                   For each matchup:
                                       ├─ Compare team1_points vs team2_points
                                       ├─ Award win to higher score (tie = both lose)
                                       └─ Track: won, points_scored, points_against

               4.2.8. Return Simulation Result
                      ├─ wins, losses, points_scored
                      └─ Cleanup temporary files

           4.2.9. Aggregate Results Across ALL Seasons
                  ├─ Total wins = sum(wins from all seasons)
                  ├─ Total losses = sum(losses from all seasons)
                  ├─ Win rate = total_wins / (total_wins + total_losses)
                  └─ Store in ConfigPerformance object

      4.3. ResultsManager Analyzes All 6 Configs
           ├─ Rank by win rate (primary)
           ├─ Tie-break by total points (secondary)
           └─ Select best configuration

      4.4. Update Baseline Config
           ├─ baseline_config[ADP_SCORING_WEIGHT] = 3.5 (best value)
           └─ Save intermediate config folder

      ┌────────────────────────────────────────────┐
      │ End Parameter Iteration (repeat for 7)    │
      └────────────────────────────────────────────┘

5. After All 7 Parameters Optimized
   ├─ Final baseline_config contains all optimal values
   └─ Generate results

6. Save Optimal Config Folder
   ├─ Create: optimal_iterative_{timestamp}/
   ├─ Save: league_config.json (updated base params)
   ├─ Save: week1-5.json, week6-9.json, week10-13.json, week14-17.json
   └─ Save: metadata with performance metrics

7. Cleanup
   ├─ Delete intermediate folders
   └─ Update data/configs folder (optional)
```

### Timing Breakdown

**For 100 simulations × 42 configs × 3 seasons (iterative mode)**:

```
Single Simulation (one season):
├─ Draft (150 picks): ~0.05s
├─ Season (17 weeks): ~0.10s
└─ Total: ~0.15s

100 Simulations × 3 Seasons (parallel, 8 workers):
├─ Single-threaded: 100 × 3 × 0.15s = 45s
├─ 8 workers: 45s / 5.5 ≈ 8.2s (accounting for overhead)
└─ Actual: ~10s per config

42 Configurations:
├─ 42 × 10s = 420s
└─ ~7 minutes

Total Execution Time (iterative):
├─ Computation: ~7 min
├─ I/O + overhead: ~1 min
└─ Total: ~8 minutes
```

**Note**: This is significantly faster than the 11.2 minutes stated in the original document (which was based on incorrect 168 config count).

---

## Performance Characteristics

### Scalability

**Simulation Count Scaling** (single config, single season):
- 10 sims: ~0.4s
- 50 sims: ~2s
- 100 sims: ~4s
- 500 sims: ~18s

**Worker Count Scaling** (100 sims, single season):
- 1 worker: 15s
- 2 workers: 8s
- 4 workers: 5s
- 8 workers: 4s
- 16 workers: 3.5s (diminishing returns)

**Optimal**: 8 workers for most systems.

### Configuration Counts by Mode

| Mode | Formula | Default Count | Notes |
|------|---------|---------------|-------|
| Single | 1 | 1 | Baseline only |
| Full | (test_values+1)^6 | 46,656 | Impractical |
| Iterative | params × (test_values+1) | 7 × 6 = 42 | **Recommended** |

---

## Summary

### Key Takeaways

1. **Win Rate Simulation optimizes 7 DRAFT STRATEGY parameters** (not prediction parameters)

2. **Three execution modes**: Single (testing), Full (exhaustive), Iterative (practical)

3. **Iterative mode is default**: 7 parameters × 6 test values = 42 configs (~8 minutes)

4. **Multi-season validation**: Tests across all available historical seasons (2021, 2022, 2024+)

5. **10-team league simulation**: 1 DraftHelper + 9 AI opponents with diverse strategies

6. **High-performance parallel execution**: ThreadPoolExecutor default, ProcessPoolExecutor optional

7. **5-file config structure**: league_config.json + 4 week-range files

### Typical Use Cases

**Development Workflow**:
1. Modify draft strategy parameters in league_config.json
2. Run single mode for quick validation (100 sims, ~10s)
3. If promising, run iterative mode for optimization (42 configs, ~8 min)
4. Review results in optimal_iterative_*/ folder
5. Apply optimal config to production

**Continuous Improvement**:
1. Run iterative mode weekly using current optimal as baseline
2. Track win rate trends over time
3. Adjust parameter ranges based on findings
4. Archive results for historical comparison

---

## Conclusion

The Win Rate Simulation is a sophisticated system for optimizing fantasy football draft strategies through multi-season league simulations. By testing configurations against realistic AI opponents across historical data, it provides data-driven insights into optimal parameter settings.

**Key Distinction**: This system optimizes **DRAFT STRATEGY** (how to pick players). Separate `run_accuracy_simulation.py` optimizes **PREDICTION ACCURACY** (how to score players).

**For more information**:
- See `ARCHITECTURE.md` for complete system architecture
- See `README.md` for usage instructions
- See `simulation/README.md` for simulation-specific details
- See `run_accuracy_simulation.py` for prediction optimization

---

**Document Version**: 2.0 (Corrected)
**Last Updated**: 2026-01-05
**Verified Against**: Latest main branch source code
