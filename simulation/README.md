# Fantasy Football Simulation System

A comprehensive parameter optimization system for the DraftHelper fantasy football tool. Uses simulation-based testing to identify optimal configuration parameters by running thousands of league simulations.

## Overview

This system tests parameter combinations to find the configuration that maximizes win rate and points scored. Each configuration is tested across multiple simulated leagues with different opponents using various draft strategies.

**Default configuration**: ~13.1 billion combinations (13 parameters with 6 values each = 6^13)

### What Gets Optimized

The system optimizes these 13 key parameters:

1. **NORMALIZATION_MAX_SCALE** (50-500): Score normalization ceiling
2. **SAME_POS_BYE_WEIGHT** (0-3): Weight for same-position bye week conflicts
3. **DIFF_POS_BYE_WEIGHT** (0-3): Weight for different-position bye week conflicts
4. **DRAFT_ORDER_BONUSES.PRIMARY** (0-200): Bonus for primary draft position
5. **DRAFT_ORDER_BONUSES.SECONDARY** (0-200): Bonus for secondary draft position
6. **ADP_SCORING_WEIGHT** (0-5): Weight for ADP multiplier
7. **ADP_SCORING_STEPS** (1-60): Threshold step size for ADP tiers
8. **PLAYER_RATING_SCORING_WEIGHT** (0-5): Weight for player rating multiplier
9. **TEAM_QUALITY_SCORING_WEIGHT** (0-5): Weight for team quality multiplier
10. **PERFORMANCE_SCORING_WEIGHT** (0-5): Weight for performance multiplier
11. **PERFORMANCE_SCORING_STEPS** (0.05-0.5): Threshold step size for performance tiers
12. **MATCHUP_IMPACT_SCALE** (0-300): Scaling factor for matchup bonus/penalty
13. **MATCHUP_SCORING_WEIGHT** (0-5): Weight for matchup bonus

Each parameter gets 6 test values by default: the baseline optimal value + 5 random variations within bounds.

**Note**: Due to the extremely large number of combinations (13.1B+), iterative optimization is strongly recommended over full cartesian product testing.

## Architecture

```
simulation/
├── run_simulation.py           # CLI entry point
├── SimulationManager.py         # Orchestrates full optimization process
├── ConfigGenerator.py           # Generates parameter combinations (13.1B possible)
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

Tests all generated configurations with 100 simulations each. This is the real optimization run.

**Estimated time**: Due to the large number of configurations (10M+ with 9 parameters), full cartesian product optimization is impractical. Consider using iterative optimization or subset testing instead.

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
