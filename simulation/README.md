# Fantasy Football Simulation System

A comprehensive parameter optimization system for the DraftHelper fantasy football tool. Uses simulation-based testing to identify optimal configuration parameters by running thousands of league simulations.

## Overview

This system tests 46,656 different parameter combinations (6 parameters with 6 values each) to find the configuration that maximizes win rate and points scored. Each configuration is tested across multiple simulated leagues with different opponents using various draft strategies.

### What Gets Optimized

The system optimizes these 6 key parameters:

1. **NORMALIZATION_MAX_SCALE** (60-140): Score normalization ceiling
2. **BASE_BYE_PENALTY** (0-40): Penalty for bye week conflicts
3. **DRAFT_ORDER_BONUSES.PRIMARY** (25-100): Bonus for primary draft position
4. **DRAFT_ORDER_BONUSES.SECONDARY** (25-75): Bonus for secondary draft position
5. **POSITIVE_MULTIPLIER** (1.0-1.3): Multiplier for GOOD/EXCELLENT ratings
6. **NEGATIVE_MULTIPLIER** (0.7-1.0): Multiplier for POOR/VERY_POOR ratings

Each parameter gets 6 test values: the baseline optimal value + 5 random variations within bounds.

## Architecture

```
simulation/
├── run_simulation.py           # CLI entry point
├── SimulationManager.py         # Orchestrates full optimization process
├── ConfigGenerator.py           # Generates 46,656 parameter combinations
├── ParallelLeagueRunner.py      # Multi-threaded simulation executor
├── ResultsManager.py            # Aggregates and compares results
├── ConfigPerformance.py         # Tracks individual config performance
├── ProgressTracker.py           # Real-time progress display
│
├── SimulatedLeague.py           # 10-team league simulator
├── DraftHelperTeam.py           # Team using DraftHelper (being tested)
├── SimulatedOpponent.py         # Opponent teams with strategies
├── Week.py                      # Weekly matchup simulator
│
├── utils/
│   └── scheduler.py             # Round-robin schedule generator
│
├── sim_data/                    # Required data files
│   ├── players_projected.csv   # Projected player stats
│   ├── players_actual.csv      # Actual player stats
│   └── teams_week_N.csv        # Team rankings by week
│
└── results/                     # Output directory
    ├── optimal_YYYY-MM-DD_HH-MM-SS.json
    └── all_results.json
```

## Quick Start

**Important**: Run all commands from the project root directory.

### 1. Test Single Configuration (Fast - ~3 seconds)

```bash
python run_simulation.py single --sims 5
```

Runs 5 simulations with the baseline configuration. Good for:
- Verifying the system works
- Debugging changes
- Quick sanity checks

### 2. Test Subset (Moderate - ~1-2 minutes)

```bash
python run_simulation.py subset --configs 10 --sims 10 --workers 4
```

Tests 10 configurations with 10 simulations each (100 total simulations). Good for:
- Validating the full pipeline
- Testing before running full optimization
- Quick parameter exploration

### 3. Full Optimization (Slow - hours/days)

```bash
python run_simulation.py full --sims 100 --workers 8
```

Tests all 46,656 configurations with 100 simulations each (4.6 million total simulations). This is the real optimization run.

**Estimated time**: With 8 workers, expect ~8-12 hours depending on hardware.

## Command-Line Options

### Common Options (all modes)

```bash
--baseline PATH      # Path to baseline config (default: simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json)
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
   - Generates 46,656 parameter combinations
   - Each combination varies 6 parameters

2. **League Simulation** (SimulatedLeague)
   - Creates 10-team league:
     - 1 DraftHelperTeam (system being tested)
     - 9 SimulatedOpponents with different strategies
   - Runs snake draft (15 rounds, 150 picks)
   - Simulates 17-week regular season
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
  "total_configs": 46656,
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
| Full | 46,656 | 100 | 4.6M | 8 | ~8-12 hours |

**Note**: Times vary based on CPU speed and system load. Single simulation takes ~0.7 seconds on average.

## Troubleshooting

### "No such file or directory: players_projected.csv"

Ensure data files exist in `simulation/sim_data/`:
```bash
ls simulation/sim_data/
# Should show: players_projected.csv, players_actual.csv, teams_week_*.csv
```

### "Baseline config not found"

Check the baseline path:
```bash
ls simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json
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
