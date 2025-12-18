# Fantasy Football Simulation System

A comprehensive parameter optimization system for the DraftHelper fantasy football tool. Uses simulation-based testing to identify optimal configuration parameters.

## Overview

This system provides **two complementary simulation modes**:

| Simulation | Purpose | Optimizes | Metric |
|------------|---------|-----------|--------|
| **Win Rate** | Find best draft *strategy* | `league_config.json` | Win Rate (higher = better) |
| **Accuracy** | Find best player *prediction* | `draft_config.json` + weekly configs | MAE (lower = better) |

**Key insight:** Win Rate = strategy optimization, Accuracy = prediction optimization

### When to Use Each Mode

- **Win Rate Simulation**: Before the season, optimize draft strategy parameters (bye week weights, draft order bonuses, ADP scoring)
- **Accuracy Simulation**: Throughout the season, optimize prediction parameters (scoring weights, matchup impacts, weather factors)

### What Gets Optimized

**Win Rate Simulation** optimizes 5 strategy parameters:
1. SAME_POS_BYE_WEIGHT - Same-position bye week conflicts
2. DIFF_POS_BYE_WEIGHT - Different-position bye week conflicts
3. PRIMARY_BONUS - Draft order primary bonus
4. SECONDARY_BONUS - Draft order secondary bonus
5. ADP_SCORING_WEIGHT - ADP scoring weight

**Accuracy Simulation** optimizes 17 prediction parameters:
1. NORMALIZATION_MAX_SCALE
2. PLAYER_RATING_SCORING_WEIGHT
3. TEAM_QUALITY_SCORING_WEIGHT, TEAM_QUALITY_MIN_WEEKS
4. PERFORMANCE_SCORING_WEIGHT, PERFORMANCE_SCORING_STEPS, PERFORMANCE_MIN_WEEKS
5. MATCHUP_IMPACT_SCALE, MATCHUP_SCORING_WEIGHT, MATCHUP_MIN_WEEKS
6. TEMPERATURE_IMPACT_SCALE, TEMPERATURE_SCORING_WEIGHT
7. WIND_IMPACT_SCALE, WIND_SCORING_WEIGHT
8. LOCATION_HOME, LOCATION_AWAY, LOCATION_INTERNATIONAL

Each parameter gets test values based on the baseline optimal value + variations within bounds.

## Architecture

```
simulation/
├── shared/                      # Shared between both modes
│   ├── ConfigGenerator.py       # Generates parameter combinations
│   ├── ResultsManager.py        # Aggregates and compares results
│   ├── ConfigPerformance.py     # Tracks individual config performance
│   ├── ProgressTracker.py       # Real-time progress display
│   └── config_cleanup.py        # Cleans up old optimal folders
│
├── win_rate/                    # Win-rate simulation (strategy)
│   ├── SimulationManager.py     # Orchestrates win-rate optimization
│   ├── ParallelLeagueRunner.py  # Multi-threaded simulation executor
│   ├── SimulatedLeague.py       # 10-team league simulator
│   ├── DraftHelperTeam.py       # Team using DraftHelper (being tested)
│   ├── SimulatedOpponent.py     # Opponent teams with strategies
│   ├── Week.py                  # Weekly matchup simulator
│   └── manual_simulation.py     # Manual test runs
│
├── accuracy/                    # Accuracy simulation (prediction)
│   ├── AccuracySimulationManager.py  # Orchestrates accuracy optimization
│   ├── AccuracyResultsManager.py     # Tracks MAE results
│   └── AccuracyCalculator.py         # MAE calculation logic
│
├── sim_data/                    # Historical data
│   ├── 2021/, 2022/, 2024/      # Season folders with weeks/week_NN/ data
│   ├── players_projected.csv   # Season-long projections
│   ├── players_actual.csv      # Season-long actuals
│   └── team_data/              # Team rankings
│
└── simulation_configs/          # Output directory
    ├── optimal_iterative_*/     # Win-rate optimal configs
    └── accuracy_optimal_*/      # Accuracy optimal configs
```

## Quick Start

**Important**: Run all commands from the project root directory.

### Win Rate Simulation

```bash
# Single config test (fast)
python run_win_rate_simulation.py single --sims 5

# Iterative optimization (recommended)
python run_win_rate_simulation.py iterative --sims 100 --workers 8
```

### Accuracy Simulation

```bash
# ROS mode - optimizes draft_config.json
python run_accuracy_simulation.py ros --test-values 5

# Weekly mode - optimizes week1-5.json, week6-9.json, etc.
python run_accuracy_simulation.py weekly --test-values 5

# Both modes (default)
python run_accuracy_simulation.py both --test-values 5
```

### Quick Tests

```bash
# Win rate: single config test (~3 seconds)
python run_win_rate_simulation.py single --sims 5

# Accuracy: quick test with minimal values (~1 minute)
python run_accuracy_simulation.py ros --test-values 2 --num-params 1
```

## Command-Line Options

### Common Options (all modes)

```bash
--baseline PATH      # Path to baseline config (default: simulation/optimal_configs/optimal_2025-10-02_15-29-14.json.json)
--output PATH        # Output directory (default: simulation/results)
--workers N          # Number of parallel threads (default: 4)
--data PATH          # Data folder (default: simulation/sim_data)
```

### Mode-Specific Options

**Single mode:**
- `--sims N`: Number of simulations (default: 5)

**Subset mode:**
- `--configs N`: Number of configs to test (default: 10)
- `--sims N`: Simulations per config (default: 10)

**Full mode:**
- `--sims N`: Simulations per config (default: 100)

### Examples

```bash
# Quick test with custom baseline
python simulation/run_simulation.py single --baseline my_config.json --sims 3

# Subset test with more parallelism
python simulation/run_simulation.py subset --configs 20 --sims 50 --workers 12

# Full optimization with custom output
python simulation/run_simulation.py full --sims 100 --workers 8 --output results/run_2025_01
```

## How It Works

### Simulation Process

1. **Configuration Generation** (ConfigGenerator)
   - Loads baseline configuration
   - Generates parameter combinations (default: 13.1 billion for 13 parameters)
   - Each combination varies all optimizable parameters

2. **League Simulation** (SimulatedLeague)
   - Creates 10-team league:
     - 1 DraftHelperTeam (system being tested)
     - 9 SimulatedOpponents with different strategies
   - Runs snake draft (15 rounds, 150 picks)
   - Simulates 16-week regular season
   - Tracks wins, losses, and points

3. **Parallel Execution** (ParallelLeagueRunner)
   - Runs multiple simulations concurrently
   - Uses ThreadPoolExecutor for parallelization
   - Configurable worker thread count

4. **Performance Tracking** (ResultsManager)
   - Aggregates results across all simulations
   - Calculates win rates and average points
   - Identifies best performing configuration

5. **Result Output**
   - Saves optimal configuration with timestamp
   - Includes performance metrics
   - Saves all results for analysis

### Opponent Strategies

The 9 simulated opponents use 4 different draft strategies:

1. **adp_aggressive** (2 teams): Pick best available by ADP
2. **projected_points_aggressive** (2 teams): Pick highest projected points
3. **adp_with_draft_order** (2 teams): ADP with draft position consideration
4. **projected_points_with_draft_order** (3 teams): Projected points with draft position

All opponents have a 20% "human error" rate where they pick from top 5 instead of #1.

### Performance Metrics

Configurations are ranked by:
1. **Win Rate** (primary): Total wins / total games
2. **Average Points** (tiebreaker): Total points / number of leagues

## Output Files

### Optimal Configuration

`simulation/results/optimal_YYYY-MM-DD_HH-MM-SS.json`

Contains the best performing configuration plus metadata:

```json
{
  "config_name": "Optimal Configuration",
  "parameters": {
    "NORMALIZATION_MAX_SCALE": 105.3,
    "BASE_BYE_PENALTY": 28.7,
    ...
  },
  "performance_metrics": {
    "config_id": "config_12345",
    "win_rate": 0.6234,
    "total_wins": 1063,
    "total_losses": 642,
    "avg_points_per_league": 1456.32,
    "num_simulations": 100,
    "timestamp": "2025-10-11_14-30-45"
  }
}
```

### All Results

`simulation/results/all_results.json`

Complete results for all tested configurations:

```json
{
  "total_configs": 13123110400,
  "configs": {
    "config_00000": {
      "config_id": "config_00000",
      "total_wins": 1050,
      "total_losses": 650,
      "win_rate": 0.6176,
      "avg_points_per_league": 1442.18,
      "num_simulations": 100
    },
    ...
  }
}
```

**Note**: With 13 parameters generating 13.1B+ combinations, the all_results.json file would be prohibitively large. Iterative optimization or database storage is required for full-scale runs.

## Testing

Run the test suites to validate components:

```bash
# Test ConfigGenerator
python simulation/test_config_generator.py

# Test performance tracking
python simulation/test_performance_tracking.py

# Test parallel execution
python simulation/test_parallel_runner.py

# Test SimulationManager integration
python simulation/test_simulation_manager.py

# Test original manual simulation
python simulation/manual_simulation.py
```

## Memory Management

The simulation system implements automatic memory management to prevent Out-Of-Memory (OOM) issues during long-running optimization:

**Explicit Cleanup**: Each simulation immediately cleans up temporary directories and resources after completion (success or failure) using try/finally blocks. This prevents memory accumulation from delayed Python garbage collection.

**Periodic GC**: Garbage collection is forced every 10 simulations to ensure timely release of memory. This adds ~1 second overhead over a complete iterative optimization run (negligible).

**No User Action Required**: These optimizations run automatically. Memory usage stays controlled throughout multi-hour optimization runs without manual intervention.

---

## Performance Tuning

### Worker Thread Count

The `--workers` parameter controls parallelization:

- **Low (1-2)**: Sequential execution, slow but low resource usage
- **Medium (4-8)**: Good balance for most systems
- **High (12+)**: Maximum speed if you have many CPU cores

**Rule of thumb**: Set workers = CPU core count - 1 (leave 1 core for system)

### Simulations Per Config

The `--sims` parameter affects accuracy vs speed:

- **Low (10-50)**: Fast but less reliable results
- **Medium (100)**: Good balance (recommended)
- **High (200+)**: More accurate but slower

100 simulations per config provides good statistical confidence.

### Memory Usage

Each simulation creates temporary files (~2MB per league). With 8 workers running concurrently, expect:
- Memory: ~2GB peak usage
- Disk: ~100MB temporary files (auto-cleaned)

## Estimated Runtimes

Based on average hardware (modern laptop/desktop):

| Mode | Configs | Sims/Config | Total Sims | Workers | Time |
|------|---------|-------------|------------|---------|------|
| Single | 1 | 5 | 5 | 2 | ~3 sec |
| Subset | 10 | 10 | 100 | 4 | ~1-2 min |
| Subset | 20 | 50 | 1,000 | 8 | ~10-15 min |
| Subset | 100 | 100 | 10,000 | 8 | ~2-3 hours |
| Full | 13.1B | 100 | 1.3T+ | 8 | Impossible* |

**Note**: Times vary based on CPU speed and system load. Single simulation takes ~0.7 seconds on average.

\*Full cartesian product with 13 parameters (13.1B configs) is impossible. Use iterative optimization instead.

## Troubleshooting

### "Killed" or OOM Issues

If the simulation process is killed with just "Killed" message and no Python traceback:

**Cause**: Linux OOM killer terminated the process due to memory exhaustion.

**Solution**: This issue has been fixed with automatic memory management (explicit cleanup + periodic GC). If you still experience this:
1. Reduce `--workers` to decrease concurrent memory usage
2. Reduce `--sims` to lower per-config memory requirements
3. Close other applications to free system RAM
4. Check system logs: `sudo grep -i "out of memory" /var/log/kern.log`

**Note**: Current implementation prevents OOM by cleaning up after each simulation and forcing GC every 10 simulations.

---

### "No such file or directory: players_projected.csv"

Ensure data files exist in `simulation/sim_data/`:
```bash
ls simulation/sim_data/
# Should show: players_projected.csv, players_actual.csv, teams_week_*.csv
```

### "Baseline config not found"

Check the baseline path:
```bash
ls simulation/optimal_configs/optimal_2025-10-02_15-29-14.json.json
```

Or specify a custom baseline:
```bash
python simulation/run_simulation.py single --baseline path/to/your/config.json
```

### Slow Performance

1. Increase workers: `--workers 8` (or higher if you have more cores)
2. Reduce simulations for testing: `--sims 50`
3. Close other applications to free resources

### Out of Memory

1. Reduce workers: `--workers 2`
2. Close other applications
3. Run on a machine with more RAM

## Development

### Adding New Parameters

To add a new parameter to optimize:

1. Add to `ConfigGenerator.PARAM_DEFINITIONS`:
```python
PARAM_DEFINITIONS = {
    ...
    'MY_NEW_PARAM': (range_val, min_val, max_val)
}
```

2. Add value generation in `generate_all_parameter_value_sets()`
3. Update `create_config_dict()` to apply the parameter
4. Update `SIMULATION_TODO.md` documentation

### Modifying Opponent Strategies

Edit `SimulatedLeague.TEAM_STRATEGIES` to change distribution:

```python
TEAM_STRATEGIES = {
    'draft_helper': 1,
    'adp_aggressive': 3,  # Changed from 2
    'projected_points_aggressive': 3,  # Changed from 2
    'adp_with_draft_order': 1,  # Changed from 2
    'projected_points_with_draft_order': 2  # Changed from 3
}
```

## Credits

Author: Kai Mizuno
Date: 2024

Built for optimizing the DraftHelper fantasy football assistant.
