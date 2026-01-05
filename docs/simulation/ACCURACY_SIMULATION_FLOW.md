# Accuracy Simulation - Functional Flow Documentation (CORRECTED)

> **IMPORTANT**: This document describes the **Accuracy Simulation ONLY**.
> For Win Rate Simulation (draft strategy optimization), see WIN_RATE_SIMULATION_FLOW.md
> These are **separate simulation systems** with different purposes and parameters.

---

## ⚠️ DOCUMENT SCOPE

**This Document Covers:**
- Accuracy Simulation (`run_accuracy_simulation.py`)
- Prediction accuracy parameter optimization (16 parameters)
- Maximizing ranking accuracy (pairwise accuracy primary, MAE fallback)
- **Infinite loop execution** - runs continuously until manually stopped

**This Document Does NOT Cover:**
- Win Rate Simulation (`run_win_rate_simulation.py`) - separate system for draft strategy optimization
- Draft Order Simulation (`run_draft_order_simulation.py`) - testing draft strategies across seasons

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Entry Point and Tournament Optimization](#entry-point-and-tournament-optimization)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Tournament Optimization](#tournament-optimization)
7. [Parallel Execution](#parallel-execution)
8. [Results Management](#results-management)
9. [Complete Execution Flow](#complete-execution-flow)
10. [Performance Characteristics](#performance-characteristics)

---

## Overview

The Accuracy Simulation optimizes **prediction accuracy parameters** by calculating Mean Absolute Error (MAE) between projected points (from scoring algorithm) and actual points (from historical data).

### Purpose

- **Optimize 16 prediction parameters** to minimize projection error
- **Tournament optimization** across 4 weekly horizons simultaneously
- **Evaluate scoring algorithm** accuracy for Starter Helper and Trade Simulator modes
- **Find optimal settings** for different season phases

### Key Metrics

- **Pairwise Accuracy**: **Primary metric** - % of player pairs correctly ranked (higher is better)
- **MAE (Mean Absolute Error)**: Fallback metric when ranking unavailable - lower is better
- **Additional Ranking Metrics**: Spearman correlation, top-5/10/20 accuracy
- **Per-Position Metrics**: Separate evaluation for QB, RB, WR, TE
- **Multi-Season Validation**: Aggregated across all historical seasons (2021, 2022, 2024+)

**Metric Hierarchy** (from `AccuracyResultsManager.py`):
1. **Primary**: Pairwise Accuracy (% of player pairs with correct relative ranking)
2. **Fallback**: MAE (used for backward compatibility when ranking metrics unavailable)

### Parameters Optimized (16 Total)

**Accuracy Simulation optimizes PREDICTION ACCURACY parameters only:**

1. **NORMALIZATION_MAX_SCALE** [50-200] - Point spread normalization scale
2. **TEAM_QUALITY_SCORING_WEIGHT** [0.0-4.0] - Weight for NFL team strength
3. **TEAM_QUALITY_MIN_WEEKS** [1-12] - Minimum weeks of team data required
4. **PERFORMANCE_SCORING_WEIGHT** [0.0-8.0] - Weight for recent player performance
5. **PERFORMANCE_SCORING_STEPS** [0.01-0.30] - Performance deviation % per tier
6. **PERFORMANCE_MIN_WEEKS** [1-14] - Minimum weeks of performance data
7. **MATCHUP_IMPACT_SCALE** [25-250] - Maximum additive matchup impact
8. **MATCHUP_SCORING_WEIGHT** [0.0-4.0] - Weight for opponent strength
9. **MATCHUP_MIN_WEEKS** [1-14] - Minimum weeks of matchup data
10. **TEMPERATURE_IMPACT_SCALE** [0-200] - Maximum temperature impact
11. **TEMPERATURE_SCORING_WEIGHT** [0.0-3.0] - Weight for temperature adjustment
12. **WIND_IMPACT_SCALE** [0-150] - Maximum wind impact
13. **WIND_SCORING_WEIGHT** [0.0-4.0] - Weight for wind adjustment
14. **LOCATION_HOME** [-5 to 15] - Home field advantage modifier
15. **LOCATION_AWAY** [-15 to 5] - Away game penalty modifier
16. **LOCATION_INTERNATIONAL** [-25 to 5] - International game modifier

**Note**: Draft strategy parameters (ADP_SCORING_WEIGHT, PLAYER_RATING, etc.) are optimized separately by `run_win_rate_simulation.py`.

---

## Ranking Metrics Explained

The simulation calculates multiple ranking-based metrics to evaluate configuration quality. **Pairwise Accuracy** is the primary comparison metric.

### Metric Definitions

From `AccuracyResultsManager.py` lines 38-54:

```python
@dataclass
class RankingMetrics:
    pairwise_accuracy: float      # % of pairwise comparisons correct (0.0-1.0)
    top_5_accuracy: float          # % overlap in top-5 predictions (0.0-1.0)
    top_10_accuracy: float         # % overlap in top-10 predictions (0.0-1.0)
    top_20_accuracy: float         # % overlap in top-20 predictions (0.0-1.0)
    spearman_correlation: float    # Rank correlation coefficient (-1.0 to +1.0)
```

**1. Pairwise Accuracy** (PRIMARY):
- % of player pairs with correct relative ranking
- For every pair (player_A, player_B):
  - Projected: player_A > player_B
  - Actual: player_A > player_B
  - **Correct**: Both agree on ranking
- Higher is better (100% = perfect ranking)
- **Why primary**: Most important for draft/trade decisions (relative value matters)

**2. Top-N Accuracy**:
- % overlap between top-N projected and top-N actual
- Measures: "Did we identify the best players?"
- Example top-5: [Player1, Player2, Player3, Player4, Player5]
  - If 4 out of 5 appear in actual top-5 → 80% accuracy

**3. Spearman Correlation**:
- Rank correlation coefficient (-1 to +1)
- Measures: How well projected ranking matches actual ranking
- +1 = perfect correlation, 0 = no correlation, -1 = perfect inverse

**4. MAE (Fallback Only)**:
- Mean Absolute Error: `mean(|actual - projected|)`
- Only used when ranking metrics unavailable
- Lower is better

### Configuration Comparison Logic

From `AccuracyResultsManager.py` lines 115-146:

```python
def is_better_than(self, other: 'AccuracyConfigPerformance') -> bool:
    # Reject invalid configs (player_count == 0)
    if self.player_count == 0:
        return False

    # Use ranking metrics if available (Q12: pairwise_accuracy is primary)
    if self.overall_metrics and other.overall_metrics:
        return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy

    # Fallback to MAE for backward compatibility (Q25)
    return self.mae < other.mae
```

**Selection Priority**:
1. Reject configs with 0 players
2. **Compare pairwise accuracy** (if metrics available) - higher wins
3. Fallback to MAE comparison (if no ranking metrics) - lower wins

### Threshold Warnings

The simulation logs warnings when ranking metrics fall below acceptable thresholds:

- **Pairwise Accuracy < 65%**: Warning - poor relative ranking
- **Top-10 Accuracy < 70%**: Warning - missing top talent

---

## Architecture

### High-Level Components

```
run_accuracy_simulation.py (Entry Point)
    ↓
AccuracySimulationManager (Orchestration Layer)
    ├─ ConfigGenerator (Parameter Space - 16 params × 4 horizons)
    ├─ ParallelAccuracyRunner (Parallel Evaluation)
    ├─ AccuracyCalculator (MAE Calculation)
    └─ AccuracyResultsManager (Result Tracking)
        ↓
    Tournament Optimization Loop:
        For each parameter (16 iterations):
            ↓
        Generate configs from 4 baseline horizons
            ↓
        Evaluate each config across ALL 4 horizons
            ↓
        ParallelAccuracyRunner (Process Pool)
            ↓
        For each config × horizon combination:
            ↓
        AccuracyCalculator
            ├─ Load historical player data (weeks 1-17)
            ├─ Calculate projections using config parameters
            ├─ Compare to actual points
            └─ Return MAE + ranking metrics
                ↓
        AccuracyResultsManager
            ├─ Track best config per horizon
            ├─ Save intermediate results
            └─ Update baselines for next parameter
                ↓
        Save optimal config folder (4 week files)
```

### Module Organization

```
simulation/
├─ accuracy/                      # Accuracy optimization
│   ├─ AccuracySimulationManager.py   # Main orchestrator
│   ├─ AccuracyCalculator.py          # MAE calculation
│   ├─ ParallelAccuracyRunner.py      # Parallel evaluation
│   └─ AccuracyResultsManager.py      # Result tracking per horizon
├─ shared/                        # Shared utilities
│   ├─ ConfigGenerator.py         # Parameter combination generator
│   ├─ ProgressTracker.py         # Progress tracking
│   └─ config_cleanup.py          # Folder cleanup utilities
└─ sim_data/                      # Historical season data
    ├─ 2021/
    ├─ 2022/
    └─ 2024/
```

---

## Entry Point and Tournament Optimization

### Command Line Interface

```bash
python run_accuracy_simulation.py [options]
```

### ⚠️ CRITICAL: Infinite Loop Behavior

**The simulation runs in an INFINITE LOOP** (`run_accuracy_simulation.py` lines 316-318):
```python
if __name__ == "__main__":
    while True:
        main()
```

**What This Means**:
- The simulation **NEVER STOPS** automatically
- Runs continuously, improving with each iteration
- Each iteration:
  1. Completes full tournament optimization (all 16 parameters)
  2. Saves optimal config to `accuracy_optimal_{timestamp}/`
  3. **Uses that optimal as baseline for next iteration**
  4. Repeats from parameter 1
- **To stop**: Press Ctrl+C (graceful shutdown with signal handler)
- **Intermediate results**: Saved after each parameter (auto-resume on restart)

**Use Cases**:
- **Continuous improvement**: Let run overnight/weekend for iterative refinement
- **Convergence testing**: See when improvements plateau
- **Production tuning**: Run until MAE stops decreasing

**To Run Single Iteration**: Modify code to remove `while True` loop

---

### Tournament Optimization Algorithm

**Purpose**: Optimize all 16 parameters across 4 weekly horizons simultaneously

**Usage**:
```bash
python run_accuracy_simulation.py --test-values 5 --max-workers 8 --use-processes
```

**Behavior**:
- **Tournament optimization** - each parameter tested across ALL 4 horizons
- Tests `test_values + 1` configurations per parameter per horizon (default: 6)
- For 16 parameters × 4 horizons × 6 values = **384 total configurations**
- Each config evaluated across all 4 horizons = 384 × 4 = **1,536 total evaluations**
- **Parallel processing** enabled by default (ProcessPoolExecutor)
- **Auto-resume support** - resumes from last completed parameter if interrupted

**⚠️ Known CLI Bug**:
The command-line output displays: `Configs per parameter: 46,656`

This is **INCORRECT** - it uses the win-rate simulation formula `(test_values+1)^6`.

**Actual behavior**: 24 configs per parameter (4 horizons × 6 test values)

The simulation correctly runs 24 configs per parameter, but the CLI display is misleading.

Source: `run_accuracy_simulation.py` line 268 (bug) vs `AccuracySimulationManager.py` line 762 (correct)

**What is Tournament Optimization?**
- Each parameter generates 4 baseline configs (one per horizon: weeks 1-5, 6-9, 10-13, 14-17)
- Each baseline config is tested with variations of the parameter
- Each variation is evaluated on ALL 4 horizons (cross-validation)
- Best config is selected independently for each horizon
- Next parameter uses updated baselines

**Example**:
```
Parameter: TEAM_QUALITY_SCORING_WEIGHT
- Generate from horizon "1-5" baseline: configs with values [0.0, 0.8, 1.6, 2.4, 3.2, 4.0]
- Generate from horizon "6-9" baseline: configs with values [0.0, 0.8, 1.6, 2.4, 3.2, 4.0]
- Generate from horizon "10-13" baseline: configs with values [0.0, 0.8, 1.6, 2.4, 3.2, 4.0]
- Generate from horizon "14-17" baseline: configs with values [0.0, 0.8, 1.6, 2.4, 3.2, 4.0]
→ Total: 24 configs
→ Each config evaluated on all 4 horizons = 24 × 4 = 96 evaluations
```

### Common Options

| Option | Default | Description |
|--------|---------|-------------|
| `--test-values` | 5 | Number of test values per parameter (total values = test_values + 1) |
| `--max-workers` | 8 | Number of parallel workers |
| `--use-processes` | True | Use ProcessPoolExecutor (recommended for CPU-intensive MAE) |
| `--num-params` | 1 | Number of parameters to vary simultaneously (1 = iterative) |
| `--baseline-folder` | Auto-detect | Path to baseline config folder |

### Auto-Resume Feature

The simulation supports automatic resumption if interrupted (Ctrl+C, crash, etc.).

**How It Works** (`AccuracySimulationManager.py` lines 187-291):

1. **Detection**: On startup, scans for `accuracy_intermediate_*` folders
   ```
   simulation/simulation_configs/
   ├─ accuracy_intermediate_00_NORMALIZATION_MAX_SCALE/
   ├─ accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT/
   ├─ accuracy_intermediate_02_TEAM_QUALITY_MIN_WEEKS/
   └─ ... (folders for completed parameters)
   ```

2. **Parse Folder Names**: Extract parameter index from folder name pattern
   - Pattern: `accuracy_intermediate_{idx}_{param_name}/`
   - Example: `accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/` → index 5

3. **Find Highest Completed**: Determine last completed parameter
   - If parameter 0-5 complete → Resume from parameter 6
   - If all 16 complete → Clean up intermediates, start fresh iteration

4. **Load Intermediate Results**: Load 4 week files from highest intermediate folder
   - Use as baselines for next parameter
   - Preserves optimization progress

5. **Resume Optimization**: Continue from next parameter in sequence

**Folder Lifecycle**:
- **During optimization**: Intermediate folders created after each parameter
- **On completion**: All intermediates deleted, optimal folder created
- **On interrupt**: Intermediates preserved for resume

**Force Fresh Start**: Delete all `accuracy_intermediate_*` folders before running

---

## Core Components

### 1. AccuracySimulationManager

**File**: `simulation/accuracy/AccuracySimulationManager.py`

**Responsibilities**:
- Orchestrate tournament optimization process
- Load baseline configuration folder (5 files: league_config.json + 4 week files)
- Coordinate ConfigGenerator, AccuracyCalculator, ParallelAccuracyRunner, AccuracyResultsManager
- Implement parameter-by-parameter tournament optimization
- Auto-resume from interrupted runs
- Save intermediate and final results

**Key Methods**:

```python
def run_both(self) -> Path:
    """Tournament optimization across all 4 horizons"""
    # Auto-resume detection
    # For each of 16 parameters:
    #   - Generate test values from 4 baselines (24 configs)
    #   - Evaluate each config on all 4 horizons (96 evaluations)
    #   - Track best config per horizon
    #   - Update baselines for next parameter
    # Save optimal config folder
```

**Multi-Season Validation**:
- Evaluates across ALL available historical seasons (2021, 2022, 2024+)
- Aggregates MAE using weighted average (equal weight per player)
- Ensures robust parameter selection

**Auto-Resume Feature**:
- Scans for `accuracy_intermediate_*` folders
- Resumes from last completed parameter
- Prevents data loss from interruptions

---

### 2. AccuracyCalculator

**File**: `simulation/accuracy/AccuracyCalculator.py`

**Responsibilities**:
- Calculate Mean Absolute Error (MAE) between projected and actual points
- Apply player filtering rules
- Calculate ranking metrics (Spearman correlation, pairwise accuracy, top-N)
- Aggregate results across seasons

**MAE Calculation**:

```python
def calculate_mae(self, player_data) -> AccuracyResult:
    """
    Calculate MAE for player projections

    Formula: mean(|actual - projected|) for all eligible players

    Filtering Rules:
    - Exclude players with actual <= 0 (didn't play)
    - Include all players regardless of projection value
    - Equal weight for all players
    """
    errors = []
    for player in player_data:
        projected = player['projected']
        actual = player['actual']

        if actual <= 0:  # Skip players who didn't play
            continue

        error = abs(actual - projected)
        errors.append(error)

    mae = sum(errors) / len(errors)
    return AccuracyResult(mae=mae, player_count=len(errors))
```

**Ranking Metrics**:

```python
def calculate_ranking_metrics(self, player_data) -> RankingMetrics:
    """
    Calculate ranking accuracy metrics:
    - Spearman correlation (rank correlation)
    - Pairwise accuracy (% correctly ordered pairs)
    - Top-5, Top-10, Top-20 accuracy (overlap in top-N)
    """
    # Sort by projected vs actual and compare rankings
```

**Aggregation Across Seasons**:

```python
def aggregate_season_results(self, season_results) -> AccuracyResult:
    """
    Aggregate MAE using weighted average

    Weight = player count (equal weight per player)
    Aggregated MAE = sum(total_error) / sum(player_count)
    """
    total_error = sum(result.total_error for _, result in season_results)
    total_players = sum(result.player_count for _, result in season_results)
    return AccuracyResult(mae=total_error / total_players)
```

---

### 3. ParallelAccuracyRunner

**File**: `simulation/accuracy/ParallelAccuracyRunner.py`

**Responsibilities**:
- Execute parallel config evaluations using ProcessPoolExecutor
- Evaluate each config across all 4 horizons simultaneously
- Manage worker processes
- Track progress and handle exceptions

**Parallel Evaluation**:

```python
def evaluate_configs_parallel(self, configs) -> List[Tuple[dict, Dict[str, AccuracyResult]]]:
    """
    Evaluate configs in parallel across all 4 horizons

    Args:
        configs: List of config dicts to evaluate

    Returns:
        List of (config, results_dict) where results_dict = {
            'week_1_5': AccuracyResult,
            'week_6_9': AccuracyResult,
            'week_10_13': AccuracyResult,
            'week_14_17': AccuracyResult
        }
    """
    with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
        futures = [
            executor.submit(
                _evaluate_config_tournament_process,
                config,
                self.data_folder,
                self.available_seasons
            )
            for config in configs
        ]

        results = []
        for future in as_completed(futures):
            config, horizon_results = future.result()
            results.append((config, horizon_results))

        return results
```

**Why ProcessPoolExecutor?**
- **True parallelism** - bypasses Python GIL
- **CPU-intensive workload** - MAE calculation across thousands of players
- **Independent evaluations** - no shared state between processes
- **~7-8x speedup** on 8-core systems

---

### 4. AccuracyResultsManager

**File**: `simulation/accuracy/AccuracyResultsManager.py`

**Responsibilities**:
- Track best configuration for each horizon independently
- Save intermediate results (4 week files)
- Load results from previous runs for auto-resume
- Generate summary reports

**Per-Horizon Tracking**:

```python
class AccuracyResultsManager:
    """
    Track best config for each of 4 weekly horizons

    Data Structure:
    {
        'week_1_5': ConfigPerformance(config, mae=3.45, ...),
        'week_6_9': ConfigPerformance(config, mae=3.12, ...),
        'week_10_13': ConfigPerformance(config, mae=2.98, ...),
        'week_14_17': ConfigPerformance(config, mae=2.87, ...)
    }
    """
    def __init__(self):
        self.best_configs = {
            'week_1_5': None,
            'week_6_9': None,
            'week_10_13': None,
            'week_14_17': None
        }
```

**Adding Results**:

```python
def add_result(self, horizon: str, config: dict, result: AccuracyResult) -> bool:
    """
    Add result and check if new best

    Args:
        horizon: 'week_1_5', 'week_6_9', 'week_10_13', or 'week_14_17'
        config: Configuration dictionary
        result: AccuracyResult with MAE

    Returns:
        True if new best (lower MAE), False otherwise
    """
    if not self.best_configs[horizon] or result.mae < self.best_configs[horizon].mae:
        self.best_configs[horizon] = ConfigPerformance(config, result)
        return True
    return False
```

**Saving Optimal Configs**:

```python
def save_optimal_configs(self) -> Path:
    """
    Save 4 optimal week configs to accuracy_optimal_* folder

    Output Structure:
    accuracy_optimal_{timestamp}/
    ├─ league_config.json    # Base config (shared)
    ├─ week1-5.json          # Optimal for weeks 1-5
    ├─ week6-9.json          # Optimal for weeks 6-9
    ├─ week10-13.json        # Optimal for weeks 10-13
    └─ week14-17.json        # Optimal for weeks 14-17
    """
```

---

### 5. ConfigGenerator

**File**: `simulation/shared/ConfigGenerator.py`

**Responsibilities**:
- Define parameter search space (16 parameters for accuracy)
- Generate test values for each parameter
- Manage 4 independent baseline configs (one per horizon)
- Create configuration dictionaries with parameter variations

**Horizon-Specific Baselines**:

```python
class ConfigGenerator:
    def load_baseline_from_folder(folder_path) -> Dict[str, dict]:
        """
        Load 4 independent baseline configs

        Returns:
        {
            '1-5': {full config for weeks 1-5},
            '6-9': {full config for weeks 6-9},
            '10-13': {full config for weeks 10-13},
            '14-17': {full config for weeks 14-17}
        }
        """
        # Load league_config.json (shared base)
        # Merge with week1-5.json → baseline['1-5']
        # Merge with week6-9.json → baseline['6-9']
        # Merge with week10-13.json → baseline['10-13']
        # Merge with week14-17.json → baseline['14-17']
```

**Test Value Generation (Per Horizon)**:

```python
def generate_horizon_test_values(self, param_name) -> Dict[str, List]:
    """
    Generate test values for a parameter across all 4 horizons

    Args:
        param_name: e.g., 'TEAM_QUALITY_SCORING_WEIGHT'

    Returns:
        {
            '1-5': [0.0, 0.8, 1.6, 2.4, 3.2, 4.0],     # 6 values
            '6-9': [0.5, 1.3, 2.1, 2.9, 3.7, 4.0],     # 6 values
            '10-13': [1.0, 1.8, 2.6, 3.4, 4.0, 4.0],   # 6 values
            '14-17': [1.5, 2.3, 3.1, 3.9, 4.0, 4.0]    # 6 values
        }
    """
    # Get current value from each horizon's baseline
    # Generate num_test_values + 1 values around each baseline
```

**Example**: TEAM_QUALITY_SCORING_WEIGHT optimization
- Horizon "1-5" baseline: 1.5 → Test values: [0.0, 0.8, 1.6, 2.4, 3.2, 4.0]
- Horizon "6-9" baseline: 2.0 → Test values: [0.5, 1.3, 2.1, 2.9, 3.7, 4.0]
- Horizon "10-13" baseline: 2.5 → Test values: [1.0, 1.8, 2.6, 3.4, 4.0, 4.0]
- Horizon "14-17" baseline: 3.0 → Test values: [1.5, 2.3, 3.1, 3.9, 4.0, 4.0]

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
│       └─ ... week_18/              # Week 18 has week 17 actuals
├─ 2022/
└─ 2024/
```

**Note**: Each position JSON file contains arrays:
- `projected_points[0..16]` - Projected points for weeks 1-17
- `actual_points[0..16]` - Actual points for weeks 1-17

### Week Offset Explained (Critical Detail)

Each week folder contains **two sets of data** in the position JSON files:
- `projected_points[0..16]` - Projections for weeks 1-17
- `actual_points[0..16]` - Actual results for weeks 1-17

**Week Offset Logic** (from `AccuracySimulationManager.py` lines 293-338):
- **For projections**: Use `week_N` folder → `projected_points[week_N - 1]`
- **For actuals**: Use `week_N+1` folder → `actual_points[week_N - 1]`

**Why the offset?**
- Week N folder created at **START** of week N (before games)
  - Contains: `projected_points[N-1]` = week N projections ✓
  - Does NOT contain: `actual_points[N-1]` = week N actuals (games not played yet) ✗
- Week N+1 folder created **AFTER** week N games complete
  - Contains: `actual_points[N-1]` = week N actuals (games finished) ✓

**Example**: Evaluating Week 5 performance
- **Projections**: Load `week_05/qb_data.json` → Read `projected_points[4]` (index 4 = week 5)
- **Actuals**: Load `week_06/qb_data.json` → Read `actual_points[4]` (index 4 = week 5, available after week 5 completes)

**Array Indexing**: Weeks 1-17 stored at indices 0-16 (zero-based)

---

## Tournament Optimization

### What is Tournament Optimization?

Tournament optimization evaluates each parameter's variations **across ALL 4 weekly horizons simultaneously**, allowing:
1. Cross-validation between horizons
2. Independent optimal selection per horizon
3. Ensures each horizon gets best parameter value for its specific needs

### Tournament Flow (Per Parameter)

```
1. Start with 4 baseline configs (one per horizon)
   ├─ Baseline_1-5   (week1-5.json)
   ├─ Baseline_6-9   (week6-9.json)
   ├─ Baseline_10-13 (week10-13.json)
   └─ Baseline_14-17 (week14-17.json)

2. Generate test values for current parameter
   ├─ From Baseline_1-5: [val1, val2, val3, val4, val5, val6]
   ├─ From Baseline_6-9: [val1, val2, val3, val4, val5, val6]
   ├─ From Baseline_10-13: [val1, val2, val3, val4, val5, val6]
   └─ From Baseline_14-17: [val1, val2, val3, val4, val5, val6]
   → Total: 24 configurations

3. Evaluate EACH config on ALL 4 horizons (cross-evaluation)
   For each of 24 configs:
       ├─ Evaluate on horizon 1-5   (weeks 1-5 MAE)
       ├─ Evaluate on horizon 6-9   (weeks 6-9 MAE)
       ├─ Evaluate on horizon 10-13 (weeks 10-13 MAE)
       └─ Evaluate on horizon 14-17 (weeks 14-17 MAE)
   → Total: 24 × 4 = 96 evaluations

4. Select best config for EACH horizon independently
   ├─ Best for 1-5: Config with lowest MAE on weeks 1-5
   ├─ Best for 6-9: Config with lowest MAE on weeks 6-9
   ├─ Best for 10-13: Config with lowest MAE on weeks 10-13
   └─ Best for 14-17: Config with lowest MAE on weeks 14-17

5. Update baselines for next parameter
   ├─ Baseline_1-5 ← Best config for 1-5
   ├─ Baseline_6-9 ← Best config for 6-9
   ├─ Baseline_10-13 ← Best config for 10-13
   └─ Baseline_14-17 ← Best config for 14-17
```

### Why Tournament Instead of Per-Horizon?

**Alternative approach (per-horizon optimization)**:
- Optimize horizon 1-5 completely, then 6-9, then 10-13, then 14-17
- **Problem**: Later horizons don't benefit from early horizon discoveries
- **Problem**: No cross-validation between horizons

**Tournament approach (current)**:
- Each parameter tested across all horizons simultaneously
- **Benefit**: Cross-validation ensures robust parameter selection
- **Benefit**: All horizons improve together
- **Benefit**: Discovers parameter interactions between horizons

---

## Complete Execution Flow

### Tournament Mode (Step-by-Step)

**Command**:
```bash
python run_accuracy_simulation.py --test-values 5 --max-workers 8 --use-processes
```

**Execution Steps**:

```
1. Parse Command Line Arguments
   ├─ test_values = 5 (6 values including baseline)
   ├─ max_workers = 8
   └─ use_processes = True

2. Find Baseline Config Folder
   ├─ Check simulation/simulation_configs/ for accuracy_optimal_* folders
   ├─ If found: Use latest as baseline
   └─ Else: Use data/ folder configs

3. Load 4 Baseline Configs
   ├─ Load league_config.json (shared base)
   ├─ Merge with week1-5.json → baseline['1-5']
   ├─ Merge with week6-9.json → baseline['6-9']
   ├─ Merge with week10-13.json → baseline['10-13']
   └─ Merge with week14-17.json → baseline['14-17']

4. Initialize AccuracySimulationManager
   ├─ ConfigGenerator(4 baselines, test_values=5)
   ├─ AccuracyCalculator()
   ├─ ParallelAccuracyRunner(max_workers=8, use_processes=True)
   └─ AccuracyResultsManager()

5. Discover Historical Seasons
   ├─ Scan simulation/sim_data/ for year folders (2021, 2022, 2024, ...)
   └─ Validate each has weeks/ subfolder

6. Auto-Resume Detection
   ├─ Check for accuracy_intermediate_* folders
   ├─ If found: Determine last completed parameter
   │   └─ Resume from next parameter
   └─ Else: Start from parameter 0

7. Start Tournament Optimization Loop
   └─ For each of 16 parameters:

      ┌──────────────────────────────────────────────────┐
      │ Parameter Iteration (e.g., TEAM_QUALITY_WEIGHT)  │
      └──────────────────────────────────────────────────┘

      7.1. Generate Test Values for All 4 Horizons
           ├─ Horizon '1-5': Generate 6 values around baseline
           ├─ Horizon '6-9': Generate 6 values around baseline
           ├─ Horizon '10-13': Generate 6 values around baseline
           └─ Horizon '14-17': Generate 6 values around baseline
           → Total: 24 configurations

      7.2. Create Config Dictionaries
           For each of 24 configs:
               ├─ Copy baseline for source horizon
               ├─ Set parameter to test value
               └─ Add metadata (param name, value, horizon)

      7.3. Submit to ParallelAccuracyRunner
           ├─ 24 configs submitted to process pool
           └─ Each config evaluated on ALL 4 horizons

      ┌────────────────────────────────────────────┐
      │ Worker Process (8 parallel, 24 jobs)      │
      └────────────────────────────────────────────┘

      7.4. For EACH Config:

           ┌────────────────────────────────────────┐
           │ Evaluate on ALL 4 Horizons            │
           └────────────────────────────────────────┘

           7.4.1. For Each Horizon (week_1_5, week_6_9, week_10_13, week_14_17):

                  For Each Season (2021, 2022, 2024, ...):

                      For Each Week in Horizon Range:

                          7.4.1.1. Load Data for Week N
                                   ├─ Projected: week_N folder (6 position JSONs)
                                   └─ Actual: week_N+1 folder (6 position JSONs)

                          7.4.1.2. Create 2 PlayerManagers
                                   ├─ projected_mgr (from week_N folder)
                                   └─ actual_mgr (from week_N+1 folder)

                          7.4.1.3. Calculate Max Weekly Projection
                                   └─ For normalization scaling

                          7.4.1.4. Calculate Projected Points
                                   For each player:
                                       ├─ Score with config parameters:
                                       │   ├─ team_quality=True
                                       │   ├─ performance=True
                                       │   ├─ matchup=True
                                       │   ├─ temperature=True
                                       │   ├─ wind=True
                                       │   └─ location=True
                                       └─ Store: projections[player.id] = scored.projected_points

                          7.4.1.5. Extract Actual Points
                                   For each player:
                                       └─ Get: actual_points[week_num - 1]

                          7.4.1.6. Cleanup PlayerManagers
                                   └─ Delete temporary directories

                  7.4.1.7. Calculate MAE for Season
                           └─ AccuracyCalculator.calculate_weekly_mae(...)

                  7.4.1.8. Calculate Ranking Metrics for Season
                           ├─ Spearman correlation
                           ├─ Pairwise accuracy
                           └─ Top-N accuracy (5, 10, 20)

           7.4.2. Aggregate MAE Across All Seasons
                  ├─ Total error = sum(season.total_error)
                  ├─ Total players = sum(season.player_count)
                  └─ Aggregated MAE = total_error / total_players

           7.4.3. Return Results for All 4 Horizons
                  {
                      'week_1_5': AccuracyResult(mae=3.45, ...),
                      'week_6_9': AccuracyResult(mae=3.12, ...),
                      'week_10_13': AccuracyResult(mae=2.98, ...),
                      'week_14_17': AccuracyResult(mae=2.87, ...)
                  }

      ┌──────────────────────────────────────────────┐
      │ End Worker Process (repeat for 24 configs)  │
      └──────────────────────────────────────────────┘

      7.5. Collect Results from All Workers
           └─ 24 configs × 4 horizons = 96 results

      7.6. Update Best Configs for Each Horizon
           For each horizon:
               ├─ Compare all 24 configs' MAE for this horizon
               ├─ Select config with lowest MAE
               └─ Update best_configs[horizon]

      7.7. Save Intermediate Results
           accuracy_intermediate_{idx}_{param_name}/
           ├─ league_config.json
           ├─ week1-5.json   (best config for 1-5)
           ├─ week6-9.json   (best config for 6-9)
           ├─ week10-13.json (best config for 10-13)
           └─ week14-17.json (best config for 14-17)

      7.8. Update Baselines for Next Parameter
           ├─ baseline['1-5'] ← best_configs['week_1_5']
           ├─ baseline['6-9'] ← best_configs['week_6_9']
           ├─ baseline['10-13'] ← best_configs['week_10_13']
           └─ baseline['14-17'] ← best_configs['week_14_17']

      ┌──────────────────────────────────────────────┐
      │ End Parameter Iteration (repeat for 16)     │
      └──────────────────────────────────────────────┘

8. After All 16 Parameters Optimized
   └─ All 4 baselines contain optimal parameter values

9. Save Optimal Config Folder
   accuracy_optimal_{timestamp}/
   ├─ league_config.json    (shared base parameters)
   ├─ week1-5.json          (optimal for weeks 1-5)
   ├─ week6-9.json          (optimal for weeks 6-9)
   ├─ week10-13.json        (optimal for weeks 10-13)
   └─ week14-17.json        (optimal for weeks 14-17)

10. Cleanup
    ├─ Delete all accuracy_intermediate_* folders
    └─ Delete old accuracy_optimal_* folders (keep only latest)
```

### Timing Breakdown

**For 16 parameters × 24 configs × 4 horizons × 3 seasons (tournament mode)**:

```
Single Config Evaluation (one horizon, one week):
├─ Load data (6 position JSONs): ~0.3s
├─ Score all players (~500 players): ~1.5s
├─ Calculate MAE + ranking metrics: ~0.2s
└─ Total: ~2.0s per horizon per week

Single Config (one horizon, all weeks in range, all seasons):
├─ Average weeks per horizon: ~4 weeks
├─ 4 weeks × 3 seasons × 2.0s = ~24s per horizon
├─ All 4 horizons: 24s × 4 = ~96s per config
└─ With 8 workers (parallel execution): 96s / 7 ≈ ~14s per config

24 Configs per Parameter:
├─ 24 configs in parallel (8 workers)
├─ 3 batches of 8 configs
├─ 3 batches × 14s ≈ 42s per parameter
└─ Actual with overhead: ~24s per parameter

16 Parameters:
├─ 16 × 24s = 384s
└─ ~6.4 minutes

Total Execution Time (tournament, single iteration):
├─ Computation: ~6.4 min
├─ I/O + overhead: ~0.6 min
└─ Total: ~6-7 minutes
```

**Note**: Faster than win rate simulation due to:
- Deterministic calculation (no random draft/season simulation)
- Pure MAE computation (no game logic)
- Efficient parallel processing with ProcessPoolExecutor

**Infinite Loop Impact**: Since the simulation runs in an infinite loop, actual runtime is unlimited until manually stopped (Ctrl+C). Each iteration takes ~6-7 minutes.

---

## Performance Characteristics

### Scalability

**Config Count Scaling** (parallel, 8 workers):
- 6 configs: ~8s
- 24 configs (1 param): ~24s
- 96 configs (4 params): ~90s
- 384 configs (16 params): ~6-7 min

**Worker Count Scaling** (24 configs):
- 1 worker: ~5 min
- 2 workers: ~2.5 min
- 4 workers: ~1.3 min
- 8 workers: ~24s
- 16 workers: ~18s (diminishing returns)

**Optimal**: 8 workers for most systems (matches CPU cores).

**Default Values Verified** (`run_accuracy_simulation.py` lines 53-68):
- `DEFAULT_TEST_VALUES = 5` (6 values including baseline) ✓
- `DEFAULT_MAX_WORKERS = 8` ✓
- `DEFAULT_USE_PROCESSES = True` ✓

### Configuration Counts

| Mode | Formula | Default Count | Notes |
|------|---------|---------------|-------|
| Tournament (Default) | params × horizons × (test_values+1) | 16 × 4 × 6 = 384 | **Recommended** |
| Per-Horizon (Legacy) | params × (test_values+1) × horizons | 16 × 6 × 4 = 384 | Sequential optimization |

**Note**: Both modes evaluate same total configs, but tournament provides cross-validation.

### Bottlenecks

**Identified Bottlenecks**:

1. **Player Scoring** (CPU-intensive):
   - Calculating projections for ~500 players per week
   - Mitigation: ProcessPoolExecutor for true parallelism

2. **Data Loading** (I/O-intensive):
   - Loading 6 position JSON files per week
   - Mitigation: Pre-load common data, cache when possible

3. **Temporary Directory Creation**:
   - Creating temp dirs for each PlayerManager
   - Mitigation: Cleanup immediately after use

---

## Summary

### Key Takeaways

1. **Accuracy Simulation optimizes 16 PREDICTION ACCURACY parameters** (not draft strategy)

2. **Tournament optimization**: Each parameter tested across all 4 horizons simultaneously

3. **384 total configurations**: 16 params × 4 horizons × 6 test values

4. **~6-7 minutes per iteration**: Faster than win rate simulation (deterministic MAE)

5. **Infinite loop execution**: Runs continuously, each iteration refines from previous optimal

6. **4 independent optimal configs**: One per weekly horizon (1-5, 6-9, 10-13, 14-17)

7. **Multi-season validation**: Aggregated MAE across all historical seasons

8. **ProcessPoolExecutor default**: True parallelism for CPU-intensive MAE calculation

9. **Auto-resume support**: Resumes from last parameter if interrupted

### Typical Use Cases

**Development Workflow**:
1. Modify prediction parameters in week*.json files
2. Run tournament optimization (384 configs, ~6-7 min per iteration)
3. Monitor console output for improvements
4. Stop (Ctrl+C) when MAE stops decreasing
5. Review optimal config folder
6. Apply to production (copy to data/ folder)

**Continuous Improvement** (Infinite Loop):
1. Start simulation and let run overnight/weekend
2. Simulation continuously refines parameters
3. Each iteration uses previous optimal as baseline
4. Stop when improvements plateau
5. Track MAE trends over multiple iterations
6. Adjust parameter ranges based on convergence patterns

**Single Iteration** (Modified Code):
1. Remove `while True` loop from `run_accuracy_simulation.py`
2. Run once (384 configs, ~6-7 min)
3. Get single optimal config

---

## Conclusion

The Accuracy Simulation is a sophisticated system for optimizing fantasy football prediction accuracy through tournament optimization across multiple weekly horizons. By testing configurations against historical data and calculating MAE, it provides data-driven insights into optimal parameter settings.

**Key Distinction**: This system optimizes **PREDICTION ACCURACY** (how to score players). Separate `run_win_rate_simulation.py` optimizes **DRAFT STRATEGY** (how to pick players).

**For more information**:
- See `ARCHITECTURE.md` for complete system architecture
- See `README.md` for usage instructions
- See `simulation/README.md` for simulation-specific details
- See `run_win_rate_simulation.py` for draft strategy optimization

---

**Document Version**: 1.0
**Last Updated**: 2026-01-05
**Verified Against**: Latest main branch source code
