# Simulation System - Quick Start Guide

## TL;DR

```bash
# Test it works (3 seconds)
python run_simulation.py single --sims 5

# Validate full pipeline (1-2 minutes)
python run_simulation.py subset --configs 10 --sims 10 --workers 4

# Run full optimization (8-12 hours)
python run_simulation.py full --sims 100 --workers 8
```

**Note**: Run from project root directory. The script is at `run_simulation.py` in the root.

## What This Does

Tests 46,656 different parameter combinations to find the optimal DraftHelper configuration that maximizes win rate in fantasy football leagues.

## Three Modes

| Mode | Purpose | Speed | Sims | Output |
|------|---------|-------|------|--------|
| **single** | Quick test/debug | ~3 sec | 5 | Console only |
| **subset** | Validation | ~1-2 min | 100-1000 | Config + results |
| **full** | Real optimization | ~8-12 hrs | 4.6M | Config + results |

## Common Commands

### Development/Testing
```bash
# Quick sanity check
python simulation/run_simulation.py single --sims 3

# Test with custom config
python simulation/run_simulation.py single --baseline my_config.json --sims 5

# Validate subset with more parallelism
python simulation/run_simulation.py subset --configs 20 --sims 50 --workers 12
```

### Production
```bash
# Full optimization (recommended settings)
python simulation/run_simulation.py full --sims 100 --workers 8

# Full optimization with custom output
python simulation/run_simulation.py full --sims 100 --workers 8 --output results/2025_01_run
```

## Options

```bash
--sims N         # Simulations per config (single: 5, subset: 10, full: 100)
--configs N      # Number of configs (subset mode only, default: 10)
--workers N      # Parallel threads (default: 4, recommend: CPU cores - 1)
--baseline PATH  # Baseline config (default: simulation/simulated_configs/optimal_*.json)
--output PATH    # Output directory (default: simulation/results)
--data PATH      # Data folder (default: simulation/sim_data)
```

## Output Files

After running subset or full mode:

```
simulation/results/
├── optimal_2025-10-11_14-30-45.json  # Best config with metrics
└── all_results.json                   # All configs tested
```

## Worker Thread Tuning

| CPUs | Recommended Workers | Expected Speed |
|------|---------------------|----------------|
| 4 | 3 | Slow |
| 8 | 6-7 | Medium |
| 12 | 10-11 | Fast |
| 16+ | 14-15 | Very Fast |

**Rule of thumb**: workers = CPU_count - 1

## Time Estimates

Full optimization (46,656 configs × 100 sims = 4.6M total):

| Workers | Estimated Time |
|---------|---------------|
| 4 | ~18-24 hours |
| 8 | ~8-12 hours |
| 12 | ~6-8 hours |
| 16 | ~4-6 hours |

## Troubleshooting

### "No such file: players_projected.csv"
```bash
ls simulation/sim_data/
# Should show: players_projected.csv, players_actual.csv, teams_week_*.csv
```

### "Baseline config not found"
```bash
ls simulation/simulated_configs/
# Pick one and use: --baseline simulation/simulated_configs/optimal_*.json
```

### Slow/Out of Memory
- Reduce workers: `--workers 2`
- Reduce simulations for testing: `--sims 50`
- Close other applications

### Check Progress
Progress bars show:
- Current config being tested
- Simulations completed for current config
- Overall progress
- Elapsed time and ETA

## Running Tests

Validate the system works:

```bash
# Test all components (~30 seconds)
python simulation/test_config_generator.py
python simulation/test_performance_tracking.py
python simulation/test_parallel_runner.py
python simulation/test_simulation_manager.py

# Test original manual simulation (~1 second)
python simulation/manual_simulation.py
```

## Reading Results

### Console Output
```
Best Configuration:
  ID: config_12345
  Win Rate: 62.34%
  Record: 1063W-642L
  Avg Points/League: 1456.32
  Simulations: 100
```

### Optimal Config File
```json
{
  "parameters": {
    "NORMALIZATION_MAX_SCALE": 105.3,
    "BASE_BYE_PENALTY": 28.7,
    ...
  },
  "performance_metrics": {
    "win_rate": 0.6234,
    "avg_points_per_league": 1456.32,
    ...
  }
}
```

## What Gets Optimized

6 parameters tested (6 values each = 46,656 combinations):

1. **NORMALIZATION_MAX_SCALE** (60-140)
2. **BASE_BYE_PENALTY** (0-40)
3. **DRAFT_ORDER_BONUSES.PRIMARY** (25-100)
4. **DRAFT_ORDER_BONUSES.SECONDARY** (25-75)
5. **POSITIVE_MULTIPLIER** (1.0-1.3) - GOOD/EXCELLENT ratings
6. **NEGATIVE_MULTIPLIER** (0.7-1.0) - POOR/VERY_POOR ratings

## Next Steps

1. **Test**: Run `single` mode to verify it works
2. **Validate**: Run `subset` mode to test full pipeline
3. **Optimize**: Run `full` mode (let it run overnight)
4. **Use Results**: Copy optimal config to main DraftHelper config

## Help

```bash
# General help
python simulation/run_simulation.py --help

# Mode-specific help
python simulation/run_simulation.py single --help
python simulation/run_simulation.py subset --help
python simulation/run_simulation.py full --help
```

## More Documentation

- **README.md** - Full documentation
- **IMPLEMENTATION_SUMMARY.md** - Implementation details
- **SIMULATION_TODO.md** - Original design document
