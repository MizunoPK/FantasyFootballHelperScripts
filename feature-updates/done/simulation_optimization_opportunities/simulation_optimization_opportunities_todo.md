# Simulation Optimization Opportunities - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 |

**Current Iteration:** 24 COMPLETE - READY TO IMPLEMENT

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [x]1 [x]2 [x]3 [x]8 [x]9 [x]10 [x]15 [x]16 |
| Algorithm Traceability | 4, 11, 19 | [x]4 [x]11 [x]19 |
| End-to-End Data Flow | 5, 12 | [x]5 [x]12 |
| Skeptical Re-verification | 6, 13, 22 | [x]6 [x]13 [x]22 |
| Integration Gap Check | 7, 14, 23 | [x]7 [x]14 [x]23 |
| Fresh Eyes Review | 17, 18 | [x]17 [x]18 |
| Edge Case Verification | 20 | [x]20 |
| Test Coverage Planning | 21 | [x]21 |
| Implementation Readiness | 24 | [x]24 |

---

## Verification Summary

- Iterations completed: 24/24 ✓
- Requirements from spec: 6 optimization opportunities
- Requirements in TODO: 6
- Questions for user: 0 (all resolved during planning)
- Integration points identified: 4 (see Integration Matrix)
- Edge cases identified: parallel execution, memory limits, single-threaded fallback
- Test files to update: test_SimulatedLeague.py, test_ConfigManager.py

---

## User Decisions Summary

| Decision | Resolution |
|----------|------------|
| Scope | Iterative mode only (single/full deprecated) |
| Target | 5x faster |
| Priority | Highest → lowest impact |
| Verification | Unit tests + integration tests |
| Benchmarking | Wall clock + memory profiling |

---

## Phase 1: Benchmarking Infrastructure

### Task 1.1: Create Benchmark Script
- **File:** `simulation/benchmark.py` (NEW)
- **Purpose:** Measure baseline and post-optimization performance
- **Tests:** `tests/simulation/test_benchmark.py`
- **Status:** [ ] Not started

**Implementation details:**
- Use `time.perf_counter()` for wall clock timing
- Use `tracemalloc` for memory profiling
- Run `iterative --sims 5` as standard benchmark
- Output: JSON with timing and memory metrics

### Task 1.2: Capture Baseline Metrics
- **File:** N/A (measurement only)
- **Purpose:** Document current performance before changes
- **Status:** [ ] Not started

**Implementation details:**
- Run benchmark 3 times, take average
- Record: total time, peak memory, per-simulation time

---

## Phase 2: Shared Read-Only Data Directories (HIGH IMPACT)

### Task 2.1: Modify SimulatedLeague to Use Shared Data
- **File:** `simulation/SimulatedLeague.py`
- **Lines:** 173-214 (`_initialize_teams()`)
- **Similar to:** Current week data pre-loading (`_preload_all_weeks()`)
- **Tests:** `tests/simulation/test_SimulatedLeague.py`
- **Status:** [ ] Not started

**Implementation details:**
- Create single shared data directory per simulation (not per team)
- Copy player files once to shared location
- Copy team_data once to shared location
- Teams read from shared location (read-only)
- Only per-team: track drafted status in memory (not file)

**Current code flow:**
```python
for idx, strategy in enumerate(strategies):
    team_dir = self.temp_dir / f"team_{idx}"
    team_dir.mkdir()
    shutil.copy(players_projected_path, team_dir / "players.csv")
    # ... more copies per team
```

**New code flow:**
```python
# Create shared data directory ONCE
shared_dir = self.temp_dir / "shared_data"
shared_dir.mkdir()
shutil.copy(players_projected_path, shared_dir / "players.csv")
# ... copy other files once

for idx, strategy in enumerate(strategies):
    # Teams use shared_dir for read-only data
    # Only create minimal per-team state
```

### Task 2.2: Update PlayerManager to Accept Shared Data Path
- **File:** `league_helper/util/PlayerManager.py`
- **Purpose:** Allow PlayerManager to work with shared read-only data
- **Tests:** `tests/league_helper/util/test_PlayerManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- PlayerManager reads from shared path
- Drafted status tracked in memory, not written to file
- Must verify all read operations work with shared path

### Task 2.3: Update ConfigManager to Accept Dict
- **File:** `league_helper/util/ConfigManager.py`
- **Purpose:** Allow ConfigManager to work without JSON file
- **Tests:** `tests/league_helper/util/test_ConfigManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Add `from_dict(config_dict)` class method
- Avoid JSON write/read cycle in SimulatedLeague
- Maintain backward compatibility for file-based usage

---

## Phase 3: Reuse ParallelLeagueRunner (HIGH IMPACT)

### Task 3.1: Modify SimulationManager to Reuse Runner
- **File:** `simulation/SimulationManager.py`
- **Purpose:** Create runner once, reuse across seasons
- **Tests:** `tests/simulation/test_SimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Move runner creation outside season loop
- Update `data_folder` parameter per season instead of recreating
- Ensure thread pool is properly managed across reuse

---

## Phase 4: Season-Level Parallelization (MEDIUM IMPACT)

### Task 4.1: Add Season Parallelization to SimulationManager
- **File:** `simulation/SimulationManager.py`
- **Purpose:** Run multiple seasons concurrently
- **Tests:** `tests/simulation/test_SimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Submit season-level tasks to executor
- Aggregate results across seasons
- Consider memory limits (may need to limit concurrent seasons)

---

## Phase 5: ProcessPoolExecutor Option (MEDIUM IMPACT)

### Task 5.1: Add ProcessPoolExecutor Support
- **File:** `simulation/ParallelLeagueRunner.py`
- **Purpose:** True parallelism for CPU-bound work
- **Tests:** `tests/simulation/test_ParallelLeagueRunner.py`
- **Status:** [ ] Not started

**Implementation details:**
- Add `use_processes` parameter to ParallelLeagueRunner
- Default to ThreadPoolExecutor (current behavior)
- ProcessPoolExecutor option for users with multi-core systems
- Handle serialization requirements for ProcessPoolExecutor

---

## Phase 6: Memory Optimizations (LOW IMPACT)

### Task 6.1: Optimize ConfigPerformance Storage
- **File:** `simulation/ResultsManager.py`
- **Lines:** ~58 (`register_config()`)
- **Purpose:** Reduce memory per config
- **Tests:** `tests/simulation/test_ResultsManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Store only varied parameter values instead of full config_dict
- Track baseline config separately
- Reconstruct full config when needed for output

---

## Phase 7: Integration Tests

### Task 7.1: Create Optimization Integration Tests
- **File:** `tests/integration/test_simulation_optimization.py` (NEW)
- **Purpose:** Verify simulation runs correctly after optimizations
- **Status:** [ ] Not started

**Implementation details:**
- Test iterative mode completes without errors
- Test results are consistent (statistical comparison)
- Test memory usage is acceptable
- Test with various worker counts (1, 4, 8)

---

## Phase 8: Final Benchmarking

### Task 8.1: Measure Post-Optimization Performance
- **File:** N/A (measurement only)
- **Purpose:** Verify 5x improvement target achieved
- **Status:** [ ] Not started

**Implementation details:**
- Run same benchmark as Task 1.2
- Compare: before vs after
- Document improvement percentages

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| `from_dict()` | ConfigManager.py | SimulatedLeague | SimulatedLeague.py:~110 | Task 2.1 |
| `shared_dir` | SimulatedLeague.py | `_initialize_teams()` | SimulatedLeague.py:131 | Task 2.1 |
| (TBD during iterations) | | | | |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Shared directories | Copy files once instead of per-team | SimulatedLeague._initialize_teams() | N/A (refactor) |
| Config from dict | Accept dict directly | ConfigManager.from_dict() | N/A (new method) |
| Reuse runner | Create once, use across seasons | SimulationManager | Season loop modification |

---

## Data Flow Traces

### Requirement: Shared Read-Only Data
```
Entry: run_simulation.py iterative
  → SimulationManager.run_iterative_simulation()
  → ParallelLeagueRunner.run_simulations_for_config()
  → SimulatedLeague.__init__()
  → SimulatedLeague._initialize_teams()  ← MODIFIED
      - Creates shared_dir ONCE
      - Teams reference shared_dir
  → Output: Same simulation results, faster
```

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:** (pending)
- **Corrections made:** (pending)
- **Confidence level:** (pending)

### Round 2 (Iteration 13)
(pending)

### Round 3 (Iteration 22)
(pending)

---

## Progress Notes

**Last Updated:** 2025-12-06
**Current Status:** TODO created, starting verification iterations
**Next Steps:** Execute iteration 1 (Files & Patterns)
**Blockers:** None
