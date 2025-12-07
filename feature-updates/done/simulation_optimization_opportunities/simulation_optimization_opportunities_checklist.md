# Simulation Optimization Opportunities - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `simulation_optimization_opportunities_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Optimization scope:** Which simulation modes to optimize (iterative only, or all modes)?
  - RESOLVED: Iterative mode only. Single and full modes are deprecated.

- [x] **Performance targets:** What improvement percentages are we aiming for?
  - RESOLVED: 5x faster target

- [x] **Benchmarking approach:** How will we measure before/after performance?
  - RESOLVED: Wall clock time + memory profiling (tracemalloc)

- [x] **Implementation priority:** What order to implement optimizations?
  - RESOLVED: Highest impact to lowest impact, thorough implementation of each

- [x] **Correctness verification:** How to verify optimizations don't break results?
  - RESOLVED: Unit tests + integration tests to ensure simulation runs end-to-end without errors

---

## Codebase Analysis Questions (INVESTIGATED)

- [x] **SimulationManager structure:** What is the main execution flow?
  - FINDING: Iterative mode loops through 24 parameters, running N configs × M simulations per param
  - Creates new `ParallelLeagueRunner` for EACH historical season (reuse opportunity)
  - `ResultsManager` cleared for each parameter (minor overhead)

- [x] **ParallelLeagueRunner implementation:** How is parallelization currently done?
  - FINDING: Uses `ThreadPoolExecutor` with configurable `max_workers`
  - Simulations submitted to thread pool, collected via `as_completed()`
  - Thread-safe progress with `threading.Lock`
  - Periodic GC with `GC_FREQUENCY = 5` (every 5 simulations)

- [x] **Data loading patterns:** How often is data loaded from disk?
  - FINDING: Per-simulation file copies via `shutil.copy` and `shutil.copytree`
  - Week data is pre-loaded (already optimized: `_preload_all_weeks`)
  - Config saved to temp JSON, then loaded by ConfigManager

- [x] **Object creation patterns:** Are objects being created/destroyed unnecessarily?
  - FINDING: Each `SimulatedLeague` creates temp directories and copies files
  - Explicit cleanup exists (`league.cleanup()`) - good
  - `ConfigPerformance` stores full `config_dict` per config (could store less)

---

## Time Efficiency Opportunities (IDENTIFIED)

- [x] **Hot path identification:** Where is most time spent?
  - FINDING: Per-simulation overhead from temp dir creation and file copies
  - `SimulatedLeague.__init__`: Creates 10 team dirs, copies config/player/team files
  - `shutil.copytree(team_data_source, team_data_dest)` for each of 10 teams

- [ ] **Algorithm complexity:** Any O(n²) that could be O(n)?
  - FINDING: No obvious O(n²) algorithms found
  - Draft broadcast is O(teams²) but N=10 is small

- [x] **Caching opportunities:** What repeated calculations could be cached?
  - FINDING: Week data already cached (good)
  - `copy.deepcopy(self.baseline_config)` called per config generation
  - `TeamDataManager.set_current_week()` called 10 teams × 17 weeks = 170 times

- [ ] **Parallel bottlenecks:** What serialization points slow things down?
  - FINDING: Season-level runs sequentially (could parallelize)
  - GIL limits true parallelism - I/O bound helps

---

## Space Efficiency Opportunities (IDENTIFIED)

- [x] **Large data structures:** What are the biggest memory consumers?
  - FINDING: `ConfigPerformance` stores full config_dict per config
  - Pre-loaded week data in `week_data_cache` (acceptable - prevents disk I/O)
  - `ResultsManager.results` dict holds all config performance objects

- [x] **Data duplication:** Is data being copied unnecessarily?
  - FINDING: YES - each of 10 teams gets its own copy of:
    - players.csv, players_projected.csv (2 files × 10 teams = 20 copies)
    - team_data folder (copied via `shutil.copytree`)
    - league_config.json

- [ ] **Object pooling:** Could object reuse reduce allocations?
  - POTENTIAL: Reuse temp directories across simulations?
  - POTENTIAL: Shared read-only data directories?

- [x] **Lazy loading:** Can data be loaded on-demand instead of upfront?
  - FINDING: Pre-loading is good for I/O efficiency
  - `_preload_all_weeks()` trades memory for disk I/O

---

## Parallelization Improvements (IDENTIFIED)

- [x] **Thread pool sizing:** Is the thread count optimal?
  - FINDING: Configurable `max_workers`, default=4
  - Should scale with CPU cores

- [x] **Work distribution:** Is work evenly distributed across threads?
  - FINDING: Yes - simulations are independent work units
  - `as_completed()` ensures efficient collection

- [x] **Shared state:** What state is shared and could cause contention?
  - FINDING: Thread-safe `threading.Lock` for progress updates
  - No shared mutable state between simulations (good)

- [x] **Single-threaded path:** Is there an efficient fallback?
  - FINDING: Yes - `max_workers=1` works with ThreadPoolExecutor
  - No separate single-threaded code path needed

---

## I/O Optimizations (IDENTIFIED)

- [x] **File read frequency:** How often are files read during simulation?
  - FINDING: Per simulation:
    - 10 temp directories created
    - ~20 file copies (players.csv × 2 × 10 teams)
    - 10 copytree operations for team_data
    - Config JSON written/read

- [ ] **Batching potential:** Can multiple reads/writes be combined?
  - POTENTIAL: Share read-only data across teams
  - POTENTIAL: Pass config dict directly instead of file I/O

- [ ] **Memory-mapped files:** Would mmap be beneficial?
  - POTENTIAL: For large CSV files, mmap could help
  - Risk: Adds complexity

- [ ] **Serialization format:** Is CSV the most efficient format?
  - Current: CSV with `csv.DictReader`
  - POTENTIAL: Pickle or parquet for faster deserialization
  - Risk: Changes data format

---

## Edge Cases

- [ ] **Single simulation:** Does optimization help for sims=1?
- [ ] **Large parameter space:** Performance with many configs?
- [ ] **Memory constraints:** Behavior under low memory?
- [ ] **Thread starvation:** Behavior with limited threads?

---

## Testing & Validation

- [ ] **Correctness verification:** How to ensure optimizations don't change results?
- [ ] **Benchmark suite:** What tests will measure performance?
- [ ] **Regression detection:** How to detect performance regressions?

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Simulation execution flow | SimulationManager.py | ANALYZED |
| Parallelization impl | ParallelLeagueRunner.py | ANALYZED |
| Config generation | ConfigGenerator.py | ANALYZED |
| Results handling | ResultsManager.py | ANALYZED |
| Single league simulation | SimulatedLeague.py | ANALYZED |
| Week simulation | Week.py | ANALYZED |

---

## Prioritized Optimization Opportunities

### HIGH IMPACT (File I/O reduction)
1. **Shared read-only data directories** - Eliminate per-team file copies
2. **Pass config dict directly** - Avoid config JSON write/read cycle
3. **Reuse ParallelLeagueRunner** - Create once, use across seasons

### MEDIUM IMPACT (Parallelization)
4. **Season-level parallelization** - Run multiple seasons concurrently
5. **ProcessPoolExecutor option** - True parallelism for CPU-bound work

### LOW IMPACT (Memory)
6. **Store only param values in ConfigPerformance** - Reduce memory per config
7. **Clear ResultsManager between params** - Already done, minimal impact

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Codebase analysis | Analyzed all 6 core simulation files | 2025-12-06 |
| Identified optimization opportunities | 7 opportunities identified and prioritized | 2025-12-06 |
| Optimization scope | Iterative mode only (single/full deprecated) | 2025-12-06 |
| Performance targets | 5x faster | 2025-12-06 |
| Benchmarking approach | Wall clock time + memory profiling (tracemalloc) | 2025-12-06 |
| Implementation priority | Highest to lowest impact, thorough implementation | 2025-12-06 |
| Correctness verification | Unit tests + integration tests for end-to-end | 2025-12-06 |
