# Fantasy Football Simulation Documentation

This directory contains comprehensive technical documentation for the Fantasy Football Helper Scripts simulation systems.

---

## Available Documentation

### 1. [Win Rate Simulation Flow](WIN_RATE_SIMULATION_FLOW.md)
**Focus**: Draft strategy parameter optimization

- **Purpose**: Maximize league win rate by optimizing draft decisions
- **Parameters**: 7 draft strategy parameters
- **Method**: Simulates complete 10-team leagues with snake draft + 17-week season
- **Metric**: Win percentage against AI opponents
- **Execution**: Multi-season validation (2021, 2022, 2024+)
- **Modes**: Single, Full, Iterative (default)
- **Typical Runtime**: ~8 minutes (iterative mode, 42 configs)

**Key Components**:
- SimulatedLeague - Complete league simulation
- DraftHelperTeam - System under test
- SimulatedOpponent - AI opponents (9 teams)
- Week - Matchup resolution and scoring
- ParallelLeagueRunner - Parallel execution

### 2. [Accuracy Simulation Flow](ACCURACY_SIMULATION_FLOW.md)
**Focus**: Prediction accuracy parameter optimization

- **Purpose**: Maximize ranking accuracy (pairwise accuracy primary, MAE fallback)
- **Parameters**: 16 prediction accuracy parameters
- **Method**: Calculates projected vs actual points across historical data
- **Metric**: Pairwise Accuracy (primary), MAE (fallback) - higher/lower is better
- **Execution**: Tournament optimization across 4 weekly horizons
- **Mode**: Tournament (default and only mode)
- **Typical Runtime**: ~6-7 minutes per iteration (infinite loop, 384 configs per iteration)
- **⚠️ Infinite Loop**: Runs continuously until manually stopped (Ctrl+C)

**Key Components**:
- AccuracyCalculator - MAE calculation
- ParallelAccuracyRunner - Parallel config evaluation
- AccuracyResultsManager - Per-horizon tracking
- Tournament optimization - Cross-validation across horizons

---

## Quick Comparison

| Aspect | Win Rate Simulation | Accuracy Simulation |
|--------|---------------------|---------------------|
| **Entry Point** | `run_win_rate_simulation.py` | `run_accuracy_simulation.py` |
| **Parameters** | 7 (draft strategy) | 16 (prediction accuracy) |
| **Metric** | Win Rate (higher better) | Pairwise Accuracy (higher) / MAE (lower) |
| **Optimization** | Iterative (1 param at a time) | Tournament (all horizons) |
| **Configs Tested** | 42 (default) | 384 per iteration (default) |
| **Execution Time** | ~8 minutes | ~6-7 min/iteration (infinite loop) |
| **Parallelization** | ThreadPoolExecutor | ProcessPoolExecutor |
| **Randomness** | Yes (draft + matchups) | No (deterministic MAE) |
| **Output** | 5 files (base + 4 week) | 5 files (base + 4 week) |

---

## Parameters Optimized

### Win Rate Simulation (7 Parameters)
**Location**: `league_config.json` (base config)

1. DRAFT_NORMALIZATION_MAX_SCALE
2. SAME_POS_BYE_WEIGHT
3. DIFF_POS_BYE_WEIGHT
4. PRIMARY_BONUS
5. SECONDARY_BONUS
6. ADP_SCORING_WEIGHT
7. PLAYER_RATING_SCORING_WEIGHT

### Accuracy Simulation (16 Parameters)
**Location**: `week*.json` (week-specific configs)

1. NORMALIZATION_MAX_SCALE
2. TEAM_QUALITY_SCORING_WEIGHT
3. TEAM_QUALITY_MIN_WEEKS
4. PERFORMANCE_SCORING_WEIGHT
5. PERFORMANCE_SCORING_STEPS
6. PERFORMANCE_MIN_WEEKS
7. MATCHUP_IMPACT_SCALE
8. MATCHUP_SCORING_WEIGHT
9. MATCHUP_MIN_WEEKS
10. TEMPERATURE_IMPACT_SCALE
11. TEMPERATURE_SCORING_WEIGHT
12. WIND_IMPACT_SCALE
13. WIND_SCORING_WEIGHT
14. LOCATION_HOME
15. LOCATION_AWAY
16. LOCATION_INTERNATIONAL

---

## Common Workflows

### Initial Setup
```bash
# Run both simulations to establish optimal baselines
python run_win_rate_simulation.py iterative --sims 100
python run_accuracy_simulation.py --test-values 5
```

### After Data Updates
```bash
# Re-optimize accuracy with new historical data
# Note: Runs in infinite loop - stop with Ctrl+C when satisfied
python run_accuracy_simulation.py --test-values 5
```

### Before Draft Season
```bash
# Validate draft strategy for new season
python run_win_rate_simulation.py single --sims 100

# If needed, optimize for new ADP data
python run_win_rate_simulation.py iterative --sims 50
```

### Continuous Improvement
```bash
# Monthly accuracy optimization (runs indefinitely, stop with Ctrl+C)
# Each iteration ~6-7 minutes, let run until MAE stops decreasing
python run_accuracy_simulation.py --test-values 3

# Quarterly win rate optimization
python run_win_rate_simulation.py iterative --sims 100
```

---

## Historical Season Data

Both simulations use shared historical data:

```
simulation/sim_data/
├─ 2021/
│   ├─ season_schedule.csv
│   ├─ game_data.csv
│   ├─ team_data/*.csv (32 NFL teams)
│   └─ weeks/
│       ├─ week_01/
│       │   ├─ qb_data.json
│       │   ├─ rb_data.json
│       │   ├─ wr_data.json
│       │   ├─ te_data.json
│       │   ├─ k_data.json
│       │   └─ dst_data.json
│       └─ ... week_18/
├─ 2022/
└─ 2024/
```

---

## Output Structure

### Win Rate Optimal Config
```
simulation/simulation_configs/optimal_iterative_{timestamp}/
├─ league_config.json    # Updated draft strategy params
├─ week1-5.json
├─ week6-9.json
├─ week10-13.json
└─ week14-17.json
```

### Accuracy Optimal Config
```
simulation/simulation_configs/accuracy_optimal_{timestamp}/
├─ league_config.json    # Shared base params
├─ week1-5.json          # Optimal for weeks 1-5
├─ week6-9.json          # Optimal for weeks 6-9
├─ week10-13.json        # Optimal for weeks 10-13
└─ week14-17.json        # Optimal for weeks 14-17
```

---

## Performance Tips

### Win Rate Simulation
- Use `--sims 100` for production runs (more stable results)
- Use `--sims 20-50` for quick testing
- ThreadPoolExecutor is default (sufficient for most cases)
- Use `--use-processes` only if CPU-bound

### Accuracy Simulation
- Always use `--use-processes` (default, significantly faster)
- Use `--test-values 5` for production (6 values per param)
- Use `--test-values 3` for quick testing (4 values per param)
- ProcessPoolExecutor bypasses Python GIL for true parallelism

---

## Troubleshooting

### Win Rate Simulation Issues

**Problem**: Low win rate (<50%)
- Check if baseline config is recent
- Verify ADP data is current
- Run accuracy simulation first to ensure good projections

**Problem**: Slow execution (>15 minutes)
- Reduce `--sims` count
- Check for memory leaks (restart if needed)
- Ensure historical data is cached

### Accuracy Simulation Issues

**Problem**: Low pairwise accuracy (<65%) or high MAE (>4.0)
- Check if historical data is complete
- Verify week offset (projections from week_N, actuals from week_N+1)
- Ensure all position JSON files exist
- Review ranking metrics in console output

**Problem**: Simulation won't stop
- This is expected behavior (infinite loop)
- Press Ctrl+C to stop gracefully
- Results are saved after each parameter (auto-resume support)

**Problem**: Process crashes
- Reduce `--max-workers` (try 4 instead of 8)
- Check available RAM (~2GB needed)
- Verify temp directory space

---

## See Also

- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - Complete system architecture
- **[README.md](../../README.md)** - Project overview and installation
- **[CORRECTIONS_NEEDED.md](CORRECTIONS_NEEDED.md)** - Verification history for Win Rate docs

---

**Last Updated**: 2026-01-05
**Maintained By**: Kai Mizuno
