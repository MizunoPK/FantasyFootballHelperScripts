# Feature Specification: unified_debug_runner

**Feature:** 03 - unified_debug_runner
**Epic:** KAI-7 - improve_debugging_runs
**Status:** DRAFT (pending S2 deep dive)
**Estimated Size:** MEDIUM

---

## Purpose

Create a single script that runs all debug tests sequentially and reports aggregated pass/fail results, enabling agents to smoke test the entire project with one command.

---

## Discovery Context

**Based on Discovery findings:**
- Simulations already have reduced-run modes: `single --sims 1`, `--test-values 1` (Iteration 1)
- Data fetchers support scope reduction: `--weeks 1` (Iteration 1)
- User wants all-in-one debug capability (Q1 answer: "all of the above")
- Debug runs must hit real APIs (Q3 answer)
- **Critical: Full debug run must complete in under 5 minutes total**

**Key design decisions from Discovery:**
- Create `run_debug_tests.py` at project root
- Call each component with appropriate debug flags
- Aggregate results and report summary
- Exit code 0 if all pass, non-zero if any fail

---

## Scope

### In Scope
- `run_debug_tests.py` script at project root
- `--debug` flags added to simulation scripts:
  - `run_win_rate_simulation.py --debug`
  - `run_accuracy_simulation.py --debug`
- `--debug` flags added to fetcher scripts:
  - `run_player_fetcher.py --debug`
  - `run_game_data_fetcher.py --debug`
  - `run_schedule_fetcher.py --debug`
- Sequential execution of all 6 components
- Summary report showing pass/fail per component
- Aggregated exit code (0 = all pass)
- Integration with debug_infrastructure (Feature 01)

### Out of Scope
- Parallel execution of debug runs
- Historical result storage
- Performance benchmarking beyond pass/fail
- Selective component execution (run all or nothing)

---

## Requirements

{To be refined during S2 deep dive}

### R1: Unified Runner Script
- Create `run_debug_tests.py` at project root
- Execute all 6 components in sequence
- Capture pass/fail status for each
- Generate summary report
- Return exit code 0 only if all pass

### R2: Win Rate Simulation Debug Flag
- Add `--debug` flag to `run_win_rate_simulation.py`
- When flag present: run single mode with minimal iterations
- Must complete in under 60 seconds

### R3: Accuracy Simulation Debug Flag
- Add `--debug` flag to `run_accuracy_simulation.py`
- When flag present: run with minimal test values
- Must complete in under 60 seconds

### R4: Player Fetcher Debug Flag
- Add `--debug` flag to `run_player_fetcher.py`
- When flag present: fetch limited data with verbose logging

### R5: Game Data Fetcher Debug Flag
- Add `--debug` flag to `run_game_data_fetcher.py`
- When flag present: fetch single week only

### R6: Schedule Fetcher Debug Flag
- Add `--debug` flag to `run_schedule_fetcher.py`
- When flag present: run with verbose logging

### R7: Performance Constraint
- Total unified debug run must complete in under 5 minutes
- Simulation debug flags must use minimal iterations to meet constraint

---

## Dependencies

- Feature 01 (debug_infrastructure) - for logging utilities and configuration
- Feature 02 (league_helper_debug) - unified runner will call league helper debug

---

## Acceptance Criteria

{To be refined during S2 deep dive}

- [ ] `python run_debug_tests.py` exists and runs
- [ ] All 6 components are executed
- [ ] Summary report shows pass/fail for each component
- [ ] Exit code 0 when all pass, non-zero when any fail
- [ ] Total execution time under 5 minutes
- [ ] Individual `--debug` flags work on each script independently
- [ ] Normal mode for each script still works as before

---

## Technical Notes

{To be populated during S5 implementation planning}

**Files to be created:**
- `run_debug_tests.py` - Unified runner

**Files to be modified:**
- `run_win_rate_simulation.py` - Add --debug flag
- `run_accuracy_simulation.py` - Add --debug flag
- `run_player_fetcher.py` - Add --debug flag
- `run_game_data_fetcher.py` - Add --debug flag
- `run_schedule_fetcher.py` - Add --debug flag

**Performance budget (5 min = 300 sec):**
- League Helper debug: ~60 sec
- Win Rate Sim debug: ~60 sec
- Accuracy Sim debug: ~60 sec
- Player Fetcher debug: ~30 sec
- Game Data Fetcher debug: ~30 sec
- Schedule Fetcher debug: ~30 sec
- Buffer: ~30 sec
