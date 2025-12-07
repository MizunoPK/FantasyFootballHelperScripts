# Simulation Optimization Opportunities

## Objective

Analyze the iterative simulation system and implement optimizations to improve time efficiency (execution speed) and space efficiency (memory usage), with effective use of parallel threads while maintaining single-threaded compatibility.

---

## High-Level Requirements

### 1. Performance Analysis
- **Scope:** Analyze the iterative simulation mode (`run_simulation.py iterative`)
- **Focus Areas:** Time complexity, space complexity, I/O operations, parallelization

### 2. Optimization Priorities
- **Primary:** Execution speed improvements
- **Secondary:** Memory usage reduction
- **Constraint:** Must work in both parallel and single-threaded modes

### 3. Trade-offs Accepted
- Increased code complexity is acceptable for performance gains
- Reduced maintainability is acceptable if efficiency improves significantly

---

## Codebase Analysis Results

### Architecture Overview

The simulation system consists of 6 core components:

| Component | File | Responsibility |
|-----------|------|----------------|
| SimulationManager | `simulation/SimulationManager.py` | Main controller, runs iterative optimization |
| ParallelLeagueRunner | `simulation/ParallelLeagueRunner.py` | ThreadPoolExecutor-based parallel execution |
| ConfigGenerator | `simulation/ConfigGenerator.py` | Generates parameter combinations |
| ResultsManager | `simulation/ResultsManager.py` | Aggregates results, identifies best configs |
| SimulatedLeague | `simulation/SimulatedLeague.py` | Single league simulation (draft + season) |
| Week | `simulation/Week.py` | Single week matchup simulation |

### Current Execution Flow (Iterative Mode)

```
SimulationManager.run_iterative_simulation()
├── For each parameter (24 total):
│   ├── Create ResultsManager (cleared per param)
│   ├── For each historical season (2021-2024):
│   │   ├── Create new ParallelLeagueRunner  <-- OPPORTUNITY: reuse
│   │   ├── For each config variation:
│   │   │   └── Submit to thread pool:
│   │   │       └── SimulatedLeague (10 teams)
│   │   │           ├── Create temp directories  <-- BOTTLENECK
│   │   │           ├── Copy files (20+ per sim)  <-- BOTTLENECK
│   │   │           ├── Run draft (15 rounds)
│   │   │           └── Run season (17 weeks)
│   │   └── Collect results
│   └── Update optimal config
└── Save final results
```

### Current Parallelization Implementation

- **ThreadPoolExecutor** with configurable `max_workers` (default: 4)
- **Thread-safe** progress tracking via `threading.Lock`
- **Periodic GC** every 5 simulations (`GC_FREQUENCY = 5`)
- **Independent work units** - simulations don't share mutable state

### Existing Optimizations (Already Implemented)

1. **Week data pre-loading** (`SimulatedLeague._preload_all_weeks()`)
   - Pre-loads all 17 weeks into `week_data_cache`
   - Reduces disk I/O from 340 reads to 17 per simulation

2. **Explicit cleanup** (`SimulatedLeague.cleanup()`, `ParallelLeagueRunner`)
   - Clears large objects after simulation
   - Periodic `gc.collect()` to prevent memory accumulation

---

## Identified Optimization Opportunities

### HIGH IMPACT: File I/O Reduction

#### 1. Shared Read-Only Data Directories
**Current:** Each of 10 teams gets its own copy of files:
- `players.csv`, `players_projected.csv` (2 files × 10 teams = 20 copies)
- `team_data/` folder copied via `shutil.copytree` (10 copies)
- `league_config.json` (10 copies)

**Location:** `SimulatedLeague._initialize_teams()` lines 173-214

**Proposed:** Use shared read-only directories or symlinks:
- Create single shared data directory per simulation
- Teams read from shared location
- Only write team-specific `drafted` status elsewhere

**Estimated Impact:** ~80% reduction in per-simulation file I/O

#### 2. Pass Config Dict Directly
**Current:** Config saved to temp JSON, then loaded by ConfigManager
```python
# SimulatedLeague.__init__
with open(self.config_path, 'w') as f:
    json.dump(config_dict, f, indent=2)
```

**Location:** `SimulatedLeague.__init__()` lines 108-110

**Proposed:** Modify ConfigManager to accept dict directly:
- Add `ConfigManager.from_dict(config_dict)` method
- Avoid JSON write/read cycle

**Estimated Impact:** ~10% reduction in per-simulation overhead

#### 3. Reuse ParallelLeagueRunner
**Current:** New `ParallelLeagueRunner` created for each historical season
```python
# SimulationManager (in season loop)
runner = ParallelLeagueRunner(max_workers=self.workers)
```

**Location:** `SimulationManager._run_historical_simulation()` (approximate)

**Proposed:** Create runner once, reuse across seasons:
- Move runner creation outside season loop
- Update `data_folder` per season instead of recreating

**Estimated Impact:** Minor (~5%), but reduces object churn

---

### MEDIUM IMPACT: Parallelization Improvements

#### 4. Season-Level Parallelization
**Current:** Historical seasons run sequentially
```python
for season_year in historical_seasons:
    runner = ParallelLeagueRunner(...)
    results = runner.run_simulations_for_config(...)
```

**Proposed:** Run seasons in parallel:
- Submit season-level tasks to executor
- Requires careful result aggregation

**Estimated Impact:** Up to 4x speedup (with 4 seasons)
**Risk:** Increases memory usage, may hit resource limits

#### 5. ProcessPoolExecutor Option
**Current:** ThreadPoolExecutor (limited by Python GIL for CPU-bound work)

**Proposed:** Add ProcessPoolExecutor as alternative:
- True parallelism for CPU-bound simulation
- Requires serializable inputs/outputs

**Estimated Impact:** Variable, depends on CPU-bound ratio
**Risk:** Higher memory overhead, serialization costs

---

### LOW IMPACT: Memory Optimizations

#### 6. Store Only Param Values in ConfigPerformance
**Current:** Full `config_dict` stored per `ConfigPerformance`
```python
self.results[config_id] = ConfigPerformance(config_id, config_dict)
```

**Location:** `ResultsManager.register_config()` line 58

**Proposed:** Store only the varied parameter values:
- Reconstruct full config when needed
- Reduces memory per config by ~90%

**Estimated Impact:** Reduces memory for large parameter sweeps
**Risk:** Need to track baseline config separately

#### 7. ResultsManager Already Cleared Per Param
**Current:** Already done - `self.results_manager = ResultsManager()`
**Impact:** Already optimized, no change needed

---

## User Decisions (RESOLVED)

### 1. Optimization Scope
**Decision:** Iterative mode only. Single and full modes are deprecated.

### 2. Performance Target
**Decision:** 5x faster

### 3. Benchmarking Approach
**Decision:** Wall clock time + memory profiling (tracemalloc)

### 4. Implementation Priority
**Decision:** Highest impact to lowest impact, thorough implementation of each:
1. Shared read-only data directories (~80% I/O reduction)
2. Pass config dict directly (~10% overhead reduction)
3. Reuse ParallelLeagueRunner (minor, reduces object churn)
4. Season-level parallelization (up to 4x speedup)
5. ProcessPoolExecutor option (variable)
6. Store only param values in ConfigPerformance (memory reduction)

### 5. Correctness Verification
**Decision:** Unit tests + integration tests to ensure simulation runs end-to-end without errors

---

## Implementation Notes

### Core Simulation Files
| File | Lines | Key Classes/Functions |
|------|-------|----------------------|
| `SimulationManager.py` | ~800 | `run_iterative_simulation()` |
| `ParallelLeagueRunner.py` | ~380 | `run_simulations_for_config()` |
| `ConfigGenerator.py` | ~1200 | `generate_iterative_combinations()` |
| `ResultsManager.py` | ~930 | `register_config()`, `record_result()` |
| `SimulatedLeague.py` | ~550 | `_initialize_teams()`, `run_draft()`, `run_season()` |
| `Week.py` | ~160 | `simulate_week()` |

### Dependencies
- `concurrent.futures.ThreadPoolExecutor`
- `threading.Lock`
- `shutil.copy`, `shutil.copytree`
- `tempfile.mkdtemp`
- `csv.DictReader`
- `gc.collect()`

### Testing Strategy
- Performance benchmarks before/after
- Memory profiling with `tracemalloc`
- Regression tests for correctness
- Unit tests for new methods

---

## Status: PLANNING COMPLETE - READY FOR IMPLEMENTATION

All user decisions resolved. Ready to proceed with development phase.
