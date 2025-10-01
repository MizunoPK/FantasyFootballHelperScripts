# Draft Helper Simulation Flow Analysis

**Generated**: 2025-09-30
**Purpose**: Comprehensive documentation of simulation system architecture and execution flow

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Execution Flow](#execution-flow)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Parameter Optimization Strategy](#parameter-optimization-strategy)
7. [Performance Characteristics](#performance-characteristics)
8. [Key Design Patterns](#key-design-patterns)

---

## Overview

The Draft Helper Simulation System is a sophisticated parameter optimization engine that tests different draft strategy configurations to identify optimal settings for fantasy football draft success. The system simulates complete draft-to-season cycles, evaluating how different parameter combinations affect final season outcomes.

**Primary Goal**: Find the optimal combination of 20 draft parameters that maximize win percentage and total points across a simulated fantasy football season.

**Simulation Scope**:
- 10-team fantasy league (1 user team + 9 AI teams with varying strategies)
- Snake draft format (15 rounds)
- 17-week regular season
- Head-to-head matchups
- Optimal lineup selection per week using starter_helper logic

---

## System Architecture

### Component Hierarchy

```
run_simulation.py (Entry Point)
    └── main_simulator.py (MainSimulator)
        ├── parameter_loader.py (Configuration Loading)
        ├── data_manager.py (Data Verification)
        ├── config_optimizer.py (ConfigurationOptimizer)
        │   └── Generates parameter combinations
        ├── parallel_runner.py (ParallelSimulationRunner)
        │   └── Manages concurrent execution
        ├── simulation_engine.py (DraftSimulationEngine)
        │   └── Executes individual drafts
        ├── season_simulator.py (SeasonSimulator)
        │   └── Simulates 17-week seasons
        └── results_analyzer.py (ResultsAnalyzer)
            └── Generates comprehensive analysis
```

### File Structure

```
draft_helper/simulation/
├── run_simulation.py              # CLI entry point
├── main_simulator.py              # Orchestrator
├── parameter_loader.py            # JSON config handling
├── data_manager.py                # Static data verification
├── config_optimizer.py            # Parameter combination generator
├── parallel_runner.py             # Concurrent execution manager
├── simulation_engine.py           # Draft execution engine
├── season_simulator.py            # Season simulation logic
├── results_analyzer.py            # Results analysis & reporting
├── config.py                      # Simulation settings
├── data/                          # Static simulation data
│   ├── players_projected.csv      # Draft decisions data
│   ├── players_actual.csv         # Season scoring data
│   └── teams_week_*.csv           # Weekly team rankings (0-18)
├── parameters/                    # Parameter configurations
│   ├── baseline_parameters.json   # Conservative defaults
│   └── parameter_template.json    # 2-value ranges template
└── results/                       # Timestamped result files
    └── simulation_results_*.json
```

---

## Execution Flow

### High-Level Process

```
1. User runs: python run_simulation.py parameters/config.json
2. MainSimulator loads and validates configuration
3. Data verification (21 static files)
4. Preliminary phase (quick evaluation)
5. Identification of top configurations
6. Full testing phase (comprehensive evaluation)
7. Results analysis and reporting
8. Save timestamped JSON results
```

### Detailed Step-by-Step Flow

#### Phase 1: Initialization (Steps 1-2)

**Step 1: Verify Static Simulation Data**
- Location: `main_simulator.py:68-70`
- Function: `data_manager.setup_simulation_data()`
- Action: Verifies existence of 21 static data files:
  - `players_projected.csv` (667 players for draft decisions)
  - `players_actual.csv` (667 players for season scoring)
  - `teams_week_0.csv` through `teams_week_18.csv` (weekly team rankings)
- **Critical**: Does NOT copy files, only validates they exist
- Error Handling: Raises `FileNotFoundError` with list of missing files

**Step 2: Load Player Data**
- Location: `main_simulator.py:72-76`
- Functions:
  - `data_manager.get_players_projected_data()` → DataFrame (667 players)
  - `data_manager.get_players_actual_data()` → DataFrame (667 players)
- Result: Two separate DataFrames for dual-purpose data usage:
  - Projected: Used for draft decisions and lineup optimization
  - Actual: Used for final weekly scoring

#### Phase 2: Preliminary Testing (Steps 3-5)

**Step 3: Generate Preliminary Configurations**
- Location: `main_simulator.py:78-81`
- Function: `config_optimizer.generate_preliminary_configs()`
- Process:
  1. Load parameter configuration from JSON file
  2. Expand all parameter combinations (Cartesian product)
  3. Example: 2 values per param × 20 params = 2^20 = 1,048,576 combinations
  4. Apply DRAFT_ORDER_WEIGHTS transformations if present
- Output: List of configuration dictionaries

**Step 4: Run Preliminary Simulations**
- Location: `main_simulator.py:83-88`
- Function: `parallel_runner.run_preliminary_simulations()`
- Configuration: `PRELIMINARY_SIMULATIONS_PER_CONFIG` from config.py
- Process:
  1. Create simulation tasks (configs × simulations per config)
  2. Use ThreadPoolExecutor with `MAX_PARALLEL_THREADS` workers
  3. For each task, execute `_run_single_complete_simulation()`
  4. Collect results as futures complete
  5. Track progress with real-time updates
- Parallelization: Up to 6 concurrent threads by default
- Output: Dictionary mapping config_key → list of simulation results

**Step 5: Analyze Preliminary Results**
- Location: `main_simulator.py:90-100`
- Function: `config_optimizer.analyze_config_performance()`
- Metrics Calculated:
  - Average win percentage (primary metric)
  - Average total points (secondary metric)
  - Average points per game
  - Score consistency (standard deviation)
  - User team rankings distribution
- Output: List of `ConfigResult` objects

#### Phase 3: Top Configuration Identification (Step 6)

**Step 6: Identify Top Configurations**
- Location: `main_simulator.py:102-104`
- Function: `config_optimizer.identify_top_configs()`
- Process:
  1. Sort all preliminary results by win percentage (descending)
  2. Take top N% (defined by `TOP_CONFIGS_PERCENTAGE` in config.py)
  3. Minimum 1 configuration selected
- Output: List of top-performing parameter dictionaries

#### Phase 4: Full Testing (Steps 7-9)

**Step 7: Generate Full Configurations**
- Location: `main_simulator.py:106-109`
- Function: `config_optimizer.generate_full_configs()`
- Process:
  1. For each top config, generate fine-grained variations
  2. Add offsets to key parameters (±5, ±10, ±15, etc.)
  3. Apply parameter bounds checking
  4. Remove duplicate configurations
- Purpose: Explore parameter space around successful configurations
- Output: Expanded list of configuration variations

**Step 8: Run Full Simulations**
- Location: `main_simulator.py:111-116`
- Function: `parallel_runner.run_full_simulations()`
- Configuration: `SIMULATIONS_PER_CONFIG` from config.py (typically higher than preliminary)
- Process: Same as Step 4, but with more simulations per config
- Output: Dictionary mapping config_key → list of simulation results

**Step 9: Analyze Full Results**
- Location: `main_simulator.py:118-128`
- Function: Same as Step 5, but for full testing results
- Output: List of `ConfigResult` objects with more simulation data

#### Phase 5: Final Analysis (Steps 10-12)

**Step 10: Generate Comprehensive Analysis**
- Location: `main_simulator.py:130-132`
- Function: `results_analyzer.analyze_all_results()`
- Components:
  - Optimal configuration identification
  - Top 10 configurations ranking
  - Parameter effect analysis (how each param affects performance)
  - Strategy effectiveness comparison (conservative vs aggressive, etc.)
  - Performance distribution statistics
  - Statistical summary across all runs
  - Analysis metadata (timestamp, configuration info)
- Output: Comprehensive dictionary with all analysis results

**Step 11: Save Results**
- Location: `main_simulator.py:134-142`
- Function: `results_analyzer.save_results_to_file()`
- Format: Timestamped JSON file
- Path: `draft_helper/simulation/results/simulation_results_YYYYMMDD_HHMMSS.json`
- Content: Complete analysis including all metrics and configurations

**Step 12: Cleanup**
- Location: `main_simulator.py:144-147`
- Action: Keep simulation data for future analysis (commented out cleanup)
- Note: Static data files are never modified during simulation

---

## Core Components

### 1. MainSimulator (`main_simulator.py`)

**Purpose**: Top-level orchestrator coordinating all simulation phases

**Key Methods**:
- `__init__(parameter_config_path)`: Load configuration and initialize components
- `run_complete_analysis()`: Execute full 12-step simulation pipeline
- `_run_single_complete_simulation(config, projected_df, actual_df)`: Execute one draft+season cycle

**Responsibilities**:
- Coordinate phase execution order
- Manage data flow between components
- Handle errors and cleanup
- Generate final output path

### 2. ConfigurationOptimizer (`config_optimizer.py`)

**Purpose**: Generate and evaluate parameter combinations

**Key Methods**:
- `generate_preliminary_configs()`: Create all parameter combinations
- `identify_top_configs(results)`: Select best performers
- `generate_full_configs(top_configs)`: Create fine-grained variations
- `analyze_config_performance(config, results)`: Calculate performance metrics

**Algorithm**:
```python
# Preliminary: Full Cartesian product
configs = itertools.product(*parameter_values)

# Full: Local variations around top configs
for top_config in top_configs:
    for param in key_params:
        for offset in [-15, -10, -5, 0, 5, 10, 15]:
            new_config = apply_offset(top_config, param, offset)
            validate_bounds(new_config)
```

### 3. ParallelSimulationRunner (`parallel_runner.py`)

**Purpose**: Manage concurrent simulation execution

**Key Methods**:
- `run_preliminary_simulations(configs, sim_function)`: Parallel preliminary testing
- `run_full_simulations(configs, sim_function)`: Parallel full testing
- `_run_single_simulation(task, sim_function)`: Execute one simulation task
- `_update_progress()`: Track and report completion status

**Parallelization Strategy**:
```python
with ThreadPoolExecutor(max_workers=6) as executor:
    futures = {
        executor.submit(sim_function, config): config
        for config in all_configs
    }

    for future in as_completed(futures):
        result = future.result()
        collect_and_aggregate(result)
```

**Performance**: Can run 6 simulations concurrently on typical systems

### 4. DraftSimulationEngine (`simulation_engine.py`)

**Purpose**: Execute individual draft simulations

**Key Methods**:
- `__init__(players_df, config_params)`: Initialize draft state
- `run_complete_draft(user_team_index)`: Execute full 15-round draft
- `_make_team_pick(team, round_num)`: AI logic for one draft pick
- `_calculate_pick_score(player, team, round_num)`: Score players for selection

**Draft Mechanics**:
- **Format**: Snake draft (1-10, 10-1, 1-10, ...)
- **Rounds**: 15 (per `MAX_PLAYERS` in config)
- **Teams**: 10 (1 user + 9 AI with different strategies)
- **Strategy Types**: Conservative, Aggressive, Positional, Value-based, Draft Helper

**Scoring Integration**:
Uses the same 7-step draft scoring system as production Draft Helper:
1. Normalize fantasy points (0-100 scale)
2. Apply ADP multiplier (1.15x excellent → 0.92x poor)
3. Apply player rating multiplier (1.20x excellent → 0.90x poor)
4. Apply team quality multiplier (1.12x excellent → 0.94x poor)
5. Add draft order bonus (position-specific by round)
6. Apply bye week penalty (10-20 points)
7. Apply injury penalty (0/25/50 points by risk level)

**AI Strategy Differentiation**:
Each AI team uses different parameter values for the 7-step scoring, creating diverse draft behaviors.

### 5. SeasonSimulator (`season_simulator.py`)

**Purpose**: Simulate 17-week fantasy season with optimal lineups

**Key Methods**:
- `simulate_full_season()`: Run complete 17-week season
- `_generate_season_schedule()`: Create weekly matchups
- `_simulate_weekly_matchup(week, matchup)`: Execute one game
- `_calculate_weekly_score(team_index, week)`: Determine team's weekly points
- `_optimize_lineup(team, week)`: Use starter_helper to set optimal lineup

**Season Mechanics**:
- **Weeks**: 17 (standard NFL regular season)
- **Matchups**: Head-to-head, randomized schedule
- **Scoring**: Weekly optimal lineup selection
- **Bye Weeks**: One random team per week (plays against league average)

**Lineup Optimization**:
```python
# For each team, each week:
roster_players = get_team_roster(team)
teams_data = load_teams_weekly_data(week)  # Week-specific rankings

lineup_optimizer = LineupOptimizer()
optimal_lineup = lineup_optimizer.optimize_lineup(
    roster_players,
    teams_data,
    week
)

weekly_score = sum(player.week_N_points for player in optimal_lineup.starters)
```

**Data Usage**:
- **Projected Data**: Used for lineup optimization decisions (mirror user experience)
- **Actual Data**: Used for final weekly scoring (mirror real-world outcomes)
- **Teams Data**: Week-specific files (`teams_week_1.csv` through `teams_week_17.csv`)

### 6. ResultsAnalyzer (`results_analyzer.py`)

**Purpose**: Generate comprehensive performance analysis

**Key Methods**:
- `analyze_all_results(config_results)`: Create full analysis report
- `_find_optimal_config()`: Identify single best configuration
- `_get_top_configs(count)`: Rank top N configurations
- `_analyze_parameter_effects()`: Measure impact of each parameter
- `_analyze_strategy_effectiveness()`: Compare strategy performance
- `save_results_to_file(analysis, filepath)`: Write JSON output

**Analysis Metrics**:
- Win percentage (primary)
- Total points (secondary)
- Points per game
- Score consistency (standard deviation)
- Average ranking (1-10)
- Strategy head-to-head records

**Output Format**:
```json
{
  "optimal_config": {
    "config_params": { ... },
    "performance": {
      "win_percentage": 0.65,
      "total_points": 1850.5,
      "points_per_game": 108.85,
      "consistency": 12.3,
      "avg_ranking": 2.8
    }
  },
  "top_10_configs": [ ... ],
  "parameter_analysis": { ... },
  "analysis_metadata": { ... }
}
```

### 7. DataManager (`data_manager.py`)

**Purpose**: Manage static simulation data access

**Key Methods**:
- `setup_simulation_data()`: Verify all files exist
- `verify_data_integrity()`: Check file consistency
- `get_players_projected_data()`: Load draft/lineup data
- `get_players_actual_data()`: Load scoring data
- `get_teams_weekly_data(week)`: Load week-specific team rankings

**Data Files** (21 total):
```
data/
├── players_projected.csv      # 667 players, used for decisions
├── players_actual.csv         # 667 players, used for scoring
└── teams_week_*.csv           # 19 files (weeks 0-18)
    ├── teams_week_0.csv       # Draft phase (preseason rankings)
    ├── teams_week_1.csv       # Early season with regression
    ├── teams_week_2.csv       # Early season with regression
    ├── teams_week_3.csv       # Early season with regression
    ├── teams_week_4.csv       # Early season with regression
    └── teams_week_5-18.csv    # Full season data (2024 actual)
```

**Data Characteristics**:
- **Static**: Never modified during simulation
- **Baseline**: Represents specific season snapshot (2024)
- **Dual-purpose**: Projected vs Actual separation mimics real-world uncertainty
- **Historical**: Week-by-week team rankings track season progression

---

## Data Flow

### Single Simulation Execution (`_run_single_complete_simulation`)

```
INPUT: config_params, players_projected_df, players_actual_df

STEP 1: Create isolated copies
├── simulation_players_projected_df = players_projected_df.copy()
└── simulation_players_actual_df = players_actual_df.copy()

STEP 2: Reset drafted status
├── projected_df['drafted'] = 0
└── actual_df['drafted'] = 0

STEP 3: Run draft simulation
├── draft_engine = DraftSimulationEngine(projected_df, config_params)
├── draft_results = draft_engine.run_complete_draft()
└── OUTPUT: 10 teams with 15-player rosters, draft picks tracked

STEP 4: Run season simulation
├── season_simulator = SeasonSimulator(teams, projected_df, actual_df)
├── For each week 1-17:
│   ├── Load teams_week_N.csv for matchup data
│   ├── For each team:
│   │   ├── Optimize lineup using projected_df + teams data
│   │   └── Score lineup using actual_df weekly points
│   └── Determine matchup winners
└── OUTPUT: Season statistics, team rankings, win/loss records

STEP 5: Combine results
└── Return {draft_results, season_stats, team_rankings, total_matchups}
```

### Parameter Configuration Flow

```
1. User provides JSON configuration
   └── parameters/iteration_1.json

2. parameter_loader.py loads and validates
   ├── Check all 20 required parameters present
   ├── Validate value types and ranges
   └── Generate metadata (config_name, description)

3. config_optimizer.py expands combinations
   ├── Cartesian product of all value lists
   ├── Example: [10, 20] × [5, 10] = [(10,5), (10,10), (20,5), (20,10)]
   └── Apply DRAFT_ORDER_WEIGHTS transformations

4. Each combination becomes config_params dict
   └── Passed to simulation engine for testing
```

### Results Aggregation Flow

```
PRELIMINARY PHASE:
├── N configs × M sims each = N×M simulation executions
├── Group results by config_key
├── Calculate average metrics per config
├── Sort by win_percentage
└── Select top X% configurations

FULL PHASE:
├── Generate variations of top configs
├── N_top configs × M_full sims each = N_top×M_full executions
├── Group results by config_key
├── Calculate comprehensive metrics
└── Identify global optimal configuration

FINAL ANALYSIS:
├── Cross-reference all configurations
├── Analyze parameter effect correlations
├── Generate strategy comparison matrix
└── Save complete report to JSON
```

---

## Parameter Optimization Strategy

### 20 Optimizable Parameters

#### Normalization Parameters (1)
- `NORMALIZATION_MAX_SCALE`: Fantasy points scaling target (0-200)

#### Enhanced Scoring Multipliers (9)
- `ADP_MULTIPLIER_EXCELLENT`: Multiplier for excellent ADP (0.8-1.5)
- `ADP_MULTIPLIER_GOOD`: Multiplier for good ADP (0.8-1.5)
- `ADP_MULTIPLIER_POOR`: Multiplier for poor ADP (0.5-1.2)
- `PLAYER_RATING_MULTIPLIER_EXCELLENT`: Player quality bonus (0.8-1.5)
- `PLAYER_RATING_MULTIPLIER_GOOD`: Player quality bonus (0.8-1.5)
- `PLAYER_RATING_MULTIPLIER_POOR`: Player quality penalty (0.5-1.2)
- `TEAM_QUALITY_MULTIPLIER_EXCELLENT`: Team quality bonus (0.8-1.5)
- `TEAM_QUALITY_MULTIPLIER_GOOD`: Team quality bonus (0.8-1.5)
- `TEAM_QUALITY_MULTIPLIER_POOR`: Team quality penalty (0.5-1.2)

#### Draft Order Bonuses (2)
- `DRAFT_ORDER_PRIMARY_BONUS`: Primary position bonus (0-100)
- `DRAFT_ORDER_SECONDARY_BONUS`: Secondary position bonus (0-100)

#### Bye Week Penalties (5)
- `BASE_BYE_PENALTY`: Base penalty for bye week (0-50)
- `POSITIONAL_BYE_PENALTIES_QB`: QB-specific penalty (0-50)
- `POSITIONAL_BYE_PENALTIES_RB`: RB-specific penalty (0-50)
- `POSITIONAL_BYE_PENALTIES_WR`: WR-specific penalty (0-50)
- `POSITIONAL_BYE_PENALTIES_TE`: TE-specific penalty (0-50)

#### Injury Penalties (3)
- `INJURY_PENALTIES_LOW`: Low injury risk penalty (0-50)
- `INJURY_PENALTIES_MEDIUM`: Medium injury risk penalty (0-50)
- `INJURY_PENALTIES_HIGH`: High injury risk penalty (0-100)

### Optimization Approach

**Two-Phase Strategy**:

1. **Preliminary Phase**: Broad exploration
   - Test all parameter combinations
   - Run fewer simulations per config (e.g., 3-5)
   - Identify promising regions of parameter space
   - Computational cost: O(combinations × sims_per_config)

2. **Full Phase**: Focused refinement
   - Test variations around top performers
   - Run more simulations per config (e.g., 10-20)
   - Fine-tune parameter values
   - Computational cost: O(top_configs × variations × sims_per_config)

**Success Metrics**:
- **Primary**: Win percentage (% of matchups won)
- **Secondary**: Total points (cumulative season scoring)
- **Tertiary**: Consistency (low standard deviation in weekly scores)

### Configuration File Format

**JSON Structure**:
```json
{
  "config_name": "iteration_1",
  "description": "Testing baseline vs increased multipliers",
  "parameters": {
    "NORMALIZATION_MAX_SCALE": [100.0, 120.0],
    "ADP_MULTIPLIER_EXCELLENT": [1.10, 1.20],
    "ADP_MULTIPLIER_GOOD": [1.05, 1.10],
    ...
  }
}
```

**Expansion Logic**:
- Each parameter: List of values to test
- Total combinations: Product of list lengths
- Example: 20 params × 2 values each = 2^20 = 1,048,576 combinations
- **Best Practice**: Use 2-3 values per parameter maximum

---

## Performance Characteristics

### Computational Complexity

**Per Simulation**:
- Draft: O(teams × rounds × available_players × scoring_calculations)
  - 10 teams × 15 rounds × ~600 players × 7 scoring steps ≈ 630,000 operations
- Season: O(weeks × teams × roster_size × lineup_optimization)
  - 17 weeks × 10 teams × 15 players × optimization ≈ 2,550 operations
- **Total per simulation**: ~1-2 seconds on typical hardware

**Full Simulation Run**:
- Preliminary: N configs × M sims ≈ N×M × 2 seconds
- Full: Top configs × variations × M_full sims ≈ Top×Var×M_full × 2 seconds
- **Example**: 100 configs × 5 sims + 10 tops × 10 vars × 10 sims = 1,500 sims ≈ 50 minutes

### Parallelization Gains

**Sequential**: 1,500 sims × 2 sec = 3,000 seconds (50 minutes)
**6 Threads**: 3,000 / 6 = 500 seconds (8.3 minutes)
**Speedup**: ~6x improvement

### Memory Usage

**Per Simulation**:
- Players data: 667 players × 2 copies (projected + actual) × ~2KB ≈ 2.7 MB
- Teams data: 19 weeks × 32 teams × ~0.5KB ≈ 0.3 MB
- **Total**: ~3 MB per concurrent simulation

**Peak Memory** (6 concurrent):
- Active simulations: 6 × 3 MB = 18 MB
- Shared data: Players + teams (loaded once) = 3 MB
- Results accumulation: ~10 MB
- **Total**: ~30-50 MB (very lightweight)

### Disk I/O

**Read Operations**:
- One-time: Load all 21 static data files at startup (~4 MB total)
- Per simulation: Zero (data cached in memory)

**Write Operations**:
- One-time: Write final results JSON at completion (~1-5 MB)

**I/O Efficiency**: Minimal disk access, primarily CPU-bound

---

## Key Design Patterns

### 1. Data Isolation Pattern

**Problem**: Simulations must not interfere with each other or modify source data
**Solution**: Copy-on-entry, static source files

```python
# Each simulation gets independent copies
simulation_projected_df = players_projected_df.copy()
simulation_actual_df = players_actual_df.copy()

# Reset state for clean start
simulation_projected_df['drafted'] = 0
simulation_actual_df['drafted'] = 0
```

**Benefits**:
- Thread-safe parallel execution
- No cross-contamination between simulations
- Source data remains pristine

### 2. Dual-Purpose Data Pattern

**Problem**: Need to simulate both projected uncertainty and actual outcomes
**Solution**: Separate projected vs actual DataFrames

```python
# Draft decisions use projected data (what you think will happen)
draft_engine = DraftSimulationEngine(projected_df, config)

# Season scoring uses actual data (what actually happened)
season_simulator = SeasonSimulator(teams, projected_df, actual_df)

# Lineup optimization uses projected (decision-making)
optimal_lineup = optimize_lineup(roster, projected_df, week)

# Weekly scoring uses actual (real results)
weekly_score = sum(player.actual_week_N_points for player in lineup)
```

**Benefits**:
- Realistic simulation of real-world uncertainty
- Mirrors actual user experience (draft on projections, score on actuals)
- Tests parameter robustness to projection errors

### 3. Two-Phase Optimization Pattern

**Problem**: Full grid search is computationally prohibitive
**Solution**: Preliminary screening + focused refinement

```python
# Phase 1: Broad exploration (low resolution)
preliminary_configs = generate_all_combinations(params)
preliminary_results = run_simulations(configs, sims=5)

# Phase 2: Focused search (high resolution)
top_configs = identify_top_performers(preliminary_results, top_pct=0.1)
full_configs = generate_fine_variations(top_configs)
full_results = run_simulations(full_configs, sims=20)
```

**Benefits**:
- Reduced computational cost (prune poor performers early)
- Higher confidence in final results (more sims on promising configs)
- Adaptive search strategy

### 4. Strategy-Based AI Pattern

**Problem**: Need diverse draft behaviors to test against
**Solution**: Multiple AI strategies with different parameter profiles

```python
TEAM_STRATEGIES = {
    'conservative': 2,      # Lower multipliers, higher penalties
    'aggressive': 2,        # Higher multipliers, lower penalties
    'positional': 2,        # Position-specific bonuses
    'value': 2,             # ADP-focused
    'draft_helper': 1       # Baseline production settings
}
```

**Benefits**:
- Realistic competitive environment
- Tests configuration against varying opponents
- Identifies robust vs situational parameter settings

### 5. Progress Tracking Pattern

**Problem**: Long-running simulations need visibility
**Solution**: Concurrent progress updates with thread-safe counters

```python
class SimulationProgress:
    total_simulations: int
    completed_simulations: int
    start_time: float
    estimated_completion_time: float

# Thread-safe updates
with self.progress_lock:
    self.progress.completed_simulations += 1
    self._print_progress_update()
```

**Benefits**:
- User feedback during long runs
- Early detection of performance issues
- Accurate time estimates

### 6. Timestamped Results Pattern

**Problem**: Multiple simulation runs need unique output files
**Solution**: Timestamp-based file naming

```python
def get_timestamped_results_file():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"simulation_results_{timestamp}.json"
```

**Benefits**:
- No file collisions
- Chronological result tracking
- Easy comparison between iterations

---

## Workflow Integration

### Complete Optimization Cycle

```
ITERATION 1: Baseline
├── User creates: parameters/iteration_1.json (2 values per param)
├── Run: python run_simulation.py parameters/iteration_1.json
├── Output: results/simulation_results_20250930_143022.json
└── Analyze: Identify optimal config and parameter trends

ITERATION 2: Refinement
├── User creates: parameters/iteration_2.json (focused on promising ranges)
├── Run: python run_simulation.py parameters/iteration_2.json
├── Output: results/simulation_results_20250930_152145.json
└── Analyze: Validate improvements, identify new optima

ITERATION 3: Validation
├── User creates: parameters/iteration_3.json (narrow ranges around best)
├── Run: python run_simulation.py parameters/iteration_3.json
├── Output: results/simulation_results_20250930_161308.json
└── Finalize: Apply optimal parameters to production config
```

### Claude-Assisted Workflow

```
1. User runs simulation
2. User tells Claude: "new simulation result file is ready"
3. Claude reads latest results JSON
4. Claude analyzes:
   ├── Optimal configuration performance
   ├── Parameter effect trends
   ├── Areas for further exploration
   └── Convergence indicators
5. Claude generates next parameter configuration JSON
6. Repeat until convergence or diminishing returns
```

---

## Summary

The Draft Helper Simulation System is a sophisticated, multi-phase parameter optimization engine that:

1. **Validates** 21 static data files containing player and team information
2. **Generates** all combinations of 20 tunable draft parameters
3. **Executes** thousands of complete draft-to-season simulations in parallel
4. **Identifies** top-performing configurations through two-phase testing
5. **Analyzes** results comprehensively with multiple performance metrics
6. **Outputs** timestamped JSON reports for iterative optimization

**Key Strengths**:
- Realistic simulation (mirrors actual draft and season mechanics)
- Efficient parallelization (6x speedup on typical hardware)
- Comprehensive analysis (win %, points, consistency, strategy comparison)
- Iterative refinement (two-phase optimization reduces computational cost)
- Production integration (optimal configs directly applicable to real drafts)

**Typical Use Cases**:
- Finding optimal draft parameter values for specific league settings
- Testing robustness of draft strategies across different scenarios
- Validating scoring system changes before production deployment
- Comparing effectiveness of different AI strategies
- Identifying parameter interactions and correlations

---

**Document Version**: 1.0
**Last Updated**: 2025-09-30
**Maintainer**: Draft Helper Development Team
