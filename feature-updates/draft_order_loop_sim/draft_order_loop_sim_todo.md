# Draft Order Loop Simulation - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 |

**Current Iteration:** 24 (COMPLETE - Ready to Implement)

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

- Iterations completed: 24/24 ✓ READY TO IMPLEMENT
- Requirements from spec: 21 (all questions resolved)
- Requirements in TODO: 21 tasks across 6 phases
- Questions for user: 0 (none needed - spec is complete)
- Integration points identified: 12 (all in Integration Matrix)

---

## Phase 1: Core Script Infrastructure

### Task 1.1: Create run_draft_order_loop.py with constants and CLI
- **File:** `run_draft_order_loop.py` (NEW)
- **Similar to:** `run_simulation.py:1-50` (constants pattern)
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
- Define constants at top: `DEFAULT_WORKERS`, `DEFAULT_SIMS`, `DEFAULT_TEST_VALUES`
- Match pattern from `run_simulation.py` exactly
- Set up logging configuration

### Task 1.2: Add CLI argument parsing
- **File:** `run_draft_order_loop.py`
- **Similar to:** `run_simulation.py:240-270` (argparse setup)
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
- `--sims`: Number of simulations per config
- `--workers`: Number of parallel workers
- `--test-values`: Number of test values per parameter
- `--use-processes`: Use ProcessPoolExecutor
- `--data`: Path to simulation data folder

### Task 1.3: Create main() entry point structure
- **File:** `run_draft_order_loop.py`
- **Similar to:** `run_simulation.py:273-310` (main flow)
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
- Parse arguments
- Set up strategies directory: `simulation/simulation_configs/strategies/`
- Find root baseline (error if none)
- Discover draft order files
- Find resume point
- Execute main loop (see Phase 4)

---

## Phase 2: Discovery and Progress Functions

### Task 2.1: Import/adapt discover_draft_order_files()
- **File:** `run_draft_order_loop.py`
- **Similar to:** `run_draft_order_simulation.py:71-90` (discover_draft_order_files)
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
- Reuse or adapt existing function
- Returns sorted list of file numbers: [0, 1, 2, ..., N]
- Skips files in archive/ subfolder (glob doesn't recurse)

### Task 2.2: Import/adapt load_draft_order_from_file()
- **File:** `run_draft_order_loop.py`
- **Similar to:** `run_draft_order_simulation.py:92-110` (load_draft_order_from_file)
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
- Load DRAFT_ORDER array from JSON file by file number

### Task 2.3: Implement find_resume_point()
- **File:** `run_draft_order_loop.py`
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
```python
def find_resume_point(draft_files, strategies_dir):
    """Find where to resume loop from.

    Returns: (start_idx, action, current_cycle)
    - start_idx: Index into draft_files to start from
    - action: "start" or "resume" (has intermediate_*)
    - current_cycle: Which optimization cycle
    """
```
- Load `strategies/loop_progress.json` if exists
- Bounds check: if `last_completed_strategy >= len(draft_files)`, reset with warning
- Check for `intermediate_*` folders in strategy folder for mid-optimization resume

### Task 2.4: Implement get_strategy_name()
- **File:** `run_draft_order_loop.py`
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
```python
def get_strategy_name(file_num: int, data_folder: Path) -> str:
    """Get strategy folder name from file number.

    Returns: e.g., "0_MINE", "1_zero_rb"
    """
```
- Glob for `{file_num}_*.json` or `{file_num}.json`
- Return stem (filename without extension)

### Task 2.5: Implement update_progress()
- **File:** `run_draft_order_loop.py`
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
```python
def update_progress(progress_file, last_completed, cycle):
    """Update progress tracker file after strategy completion."""
```
- Write JSON with `current_cycle`, `last_completed_strategy`, `last_updated`
- Only called AFTER successful optimization completion

---

## Phase 3: Folder Management Functions

### Task 3.1: Implement ensure_strategy_folder()
- **File:** `run_draft_order_loop.py`
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
```python
def ensure_strategy_folder(strategy_folder, root_baseline, file_num, data_folder):
    """Ensure strategy folder exists with valid configs. Seed if needed."""
```
- Check if folder exists and has valid `optimal_*` subfolder
- If not, call `seed_strategy_folder()`
- If corrupt (missing required files), delete and re-seed
- Required files: `league_config.json`, `week1-5.json`, `week6-11.json`, `week12-17.json`

### Task 3.2: Implement seed_strategy_folder()
- **File:** `run_draft_order_loop.py`
- **Similar to:** `run_draft_order_simulation.py:282-283` (DRAFT_ORDER injection pattern)
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
```python
def seed_strategy_folder(strategy_folder, root_baseline, file_num, data_folder):
    """Seed a new strategy folder from root baseline with DRAFT_ORDER injected."""
```
- Create `strategy_folder/optimal_seed/`
- Copy 4 config files from root baseline
- Inject DRAFT_ORDER into `league_config.json`:
  - `config['parameters']['DRAFT_ORDER_FILE'] = file_num`
  - `config['parameters']['DRAFT_ORDER'] = draft_order`

### Task 3.3: Implement get_strategy_baseline()
- **File:** `run_draft_order_loop.py`
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
```python
def get_strategy_baseline(strategy_folder):
    """Get the best baseline to use for this strategy's optimization."""
```
- Return most recent `optimal_iterative_*` if exists (skip `optimal_seed`)
- Fall back to `optimal_seed/` if no iterative results yet
- Raise error if no valid baseline found

### Task 3.4: Implement cleanup_intermediate_folders()
- **File:** `run_draft_order_loop.py`
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
```python
def cleanup_intermediate_folders(strategy_folder):
    """Remove intermediate_* folders after successful optimization."""
```
- Glob for `intermediate_*` in strategy folder
- Delete each one with `shutil.rmtree()`

### Task 3.5: Implement find_latest_optimal_folder()
- **File:** `run_draft_order_loop.py`
- **Similar to:** `run_simulation.py` (find_config_folders pattern)
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
- Find latest `optimal_*` folder in root `simulation_configs/`
- Used to seed new strategy folders
- Return None if none found (caller will error out)

---

## Phase 4: Main Loop Integration

### Task 4.1: Implement main optimization loop
- **File:** `run_draft_order_loop.py`
- **Similar to:** `run_simulation.py:290-310` (run_iterative_optimization call)
- **Tests:** `tests/root_scripts/test_root_scripts.py::TestRunDraftOrderLoop`
- **Status:** [ ] Not started

**Implementation details:**
```python
while True:
    for idx in range(start_idx, len(draft_files)):
        file_num = draft_files[idx]
        strategy_name = get_strategy_name(file_num, data_folder)
        strategy_folder = strategies_dir / strategy_name

        ensure_strategy_folder(strategy_folder, root_baseline, file_num, data_folder)
        baseline = get_strategy_baseline(strategy_folder)

        manager = SimulationManager(
            baseline_path=baseline,
            output_dir=strategy_folder,
            num_simulations_per_config=args.sims,
            num_test_values=args.test_values,
            max_workers=args.workers,
            use_processes=args.use_processes,
            auto_update_league_config=False  # Don't update root data/configs
        )
        manager.run_iterative_optimization()

        cleanup_intermediate_folders(strategy_folder)
        update_progress(progress_file, last_completed=idx, cycle=current_cycle)

    # Cycle complete, start next
    current_cycle += 1
    start_idx = 0
```

### Task 4.2: Add logging throughout main loop
- **File:** `run_draft_order_loop.py`
- **Similar to:** `run_simulation.py` (logging patterns)
- **Tests:** N/A (logging behavior)
- **Status:** [ ] Not started

**Implementation details:**
- Log resume point on startup
- Log when starting each strategy
- Log when completing each strategy
- Log cycle completion

---

## Phase 5: Bash Wrapper Script

### Task 5.1: Create run_draft_order_loop.sh
- **File:** `run_draft_order_loop.sh` (NEW)
- **Similar to:** `run_simulation_loop.sh` (exact pattern)
- **Tests:** Manual testing
- **Status:** [ ] Not started

**Implementation details:**
- Trap SIGINT/SIGTERM for graceful shutdown
- Restart on exit codes 137 (SIGKILL) or 143 (SIGTERM)
- Exit cleanly on exit code 0
- Pass through all arguments to Python script

---

## Phase 6: Unit Tests

### Task 6.1: Add test class to existing test file
- **File:** `tests/root_scripts/test_root_scripts.py` (ADD class TestRunDraftOrderLoop)
- **Similar to:** `tests/root_scripts/test_root_scripts.py:211` (TestRunSimulation class)
- **Tests:** N/A
- **Status:** [ ] Not started

**Implementation details:**
- Add `class TestRunDraftOrderLoop` following TestRunSimulation pattern
- Test fixtures for temp directories
- Test fixtures for mock draft order files
- Test fixtures for mock config folders

### Task 6.2: Tests for discovery functions
- **File:** `tests/root_scripts/test_root_scripts.py` (within TestRunDraftOrderLoop)
- **Status:** [ ] Not started

**Implementation details:**
- Test `discover_draft_order_files()` finds correct files
- Test `discover_draft_order_files()` skips archive folder
- Test `load_draft_order_from_file()` loads correct data
- Test `get_strategy_name()` returns correct name

### Task 6.3: Tests for progress tracking
- **File:** `tests/root_scripts/test_root_scripts.py` (within TestRunDraftOrderLoop)
- **Status:** [ ] Not started

**Implementation details:**
- Test `find_resume_point()` with no progress file (starts at 0)
- Test `find_resume_point()` with existing progress file
- Test `find_resume_point()` with `intermediate_*` folder (resume)
- Test `find_resume_point()` bounds check reset
- Test `update_progress()` creates correct JSON

### Task 6.4: Tests for folder management
- **File:** `tests/root_scripts/test_root_scripts.py` (within TestRunDraftOrderLoop)
- **Status:** [ ] Not started

**Implementation details:**
- Test `ensure_strategy_folder()` creates new folder
- Test `ensure_strategy_folder()` with existing valid folder (no-op)
- Test `ensure_strategy_folder()` with corrupt folder (re-seed)
- Test `seed_strategy_folder()` copies files correctly
- Test `seed_strategy_folder()` injects DRAFT_ORDER
- Test `get_strategy_baseline()` returns most recent optimal
- Test `get_strategy_baseline()` falls back to optimal_seed
- Test `cleanup_intermediate_folders()` removes folders
- Test `find_latest_optimal_folder()` finds correct folder

### Task 6.5: Tests for main loop edge cases
- **File:** `tests/root_scripts/test_root_scripts.py` (within TestRunDraftOrderLoop)
- **Status:** [ ] Not started

**Implementation details:**
- Test missing root baseline errors out
- Test empty draft_order_possibilities directory
- Test CLI argument parsing

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| `main()` | run_draft_order_loop.py | CLI entry point | __main__ | Task 1.3 |
| `discover_draft_order_files()` | run_draft_order_loop.py | `main()` | run_draft_order_loop.py | Task 1.3 |
| `load_draft_order_from_file()` | run_draft_order_loop.py | `seed_strategy_folder()` | run_draft_order_loop.py | Task 3.2 |
| `find_resume_point()` | run_draft_order_loop.py | `main()` | run_draft_order_loop.py | Task 1.3 |
| `get_strategy_name()` | run_draft_order_loop.py | `main()` | run_draft_order_loop.py | Task 4.1 |
| `update_progress()` | run_draft_order_loop.py | main loop | run_draft_order_loop.py | Task 4.1 |
| `ensure_strategy_folder()` | run_draft_order_loop.py | main loop | run_draft_order_loop.py | Task 4.1 |
| `seed_strategy_folder()` | run_draft_order_loop.py | `ensure_strategy_folder()` | run_draft_order_loop.py | Task 3.1 |
| `get_strategy_baseline()` | run_draft_order_loop.py | main loop | run_draft_order_loop.py | Task 4.1 |
| `cleanup_intermediate_folders()` | run_draft_order_loop.py | main loop | run_draft_order_loop.py | Task 4.1 |
| `find_latest_optimal_folder()` | run_draft_order_loop.py | `main()` | run_draft_order_loop.py | Task 1.3 |
| `SimulationManager` | simulation/SimulationManager.py | main loop | run_draft_order_loop.py | Task 4.1 (existing) |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Q2: Progress Tracking | Load progress, find next strategy | `find_resume_point()` | if progress_file.exists() else start fresh |
| Q6: Corrupt Folder | Check required files, re-seed if missing | `ensure_strategy_folder()` | if not has_valid_baseline: re-seed |
| Q7: Missing Baseline | Error if no root optimal_* | `main()` | if not root_baseline: sys.exit(1) |
| Q14: Seeding Structure | Copy to optimal_seed/ | `seed_strategy_folder()` | Creates optimal_seed/ subfolder |
| Q15: DRAFT_ORDER Injection | Inject during seeding | `seed_strategy_folder()` | Writes to league_config.json on disk |
| Q16: Cleanup | Remove intermediate_* after completion | `cleanup_intermediate_folders()` | After run_iterative_optimization() |
| Q20: Bounds Check | Reset if index exceeds file count | `find_resume_point()` | if last_completed >= len: reset with warning |

---

## Data Flow Traces

### Requirement: Run optimization for each strategy

```
Entry: run_draft_order_loop.py (CLI)
  → main()
    → find_latest_optimal_folder(config_dir)  ← Root baseline
    → discover_draft_order_files(data_folder)  ← [0, 1, 2, ...]
    → find_resume_point(draft_files, strategies_dir)  ← (idx, action, cycle)
    → LOOP: for idx in range(start_idx, len(draft_files))
      → get_strategy_name(file_num, data_folder)  ← "0_MINE"
      → ensure_strategy_folder()  ← Seeds if needed
        → seed_strategy_folder()  ← NEW (copies + injects DRAFT_ORDER)
      → get_strategy_baseline(strategy_folder)  ← optimal_seed or optimal_iterative_*
      → SimulationManager.run_iterative_optimization()  ← EXISTING
      → cleanup_intermediate_folders()  ← NEW
      → update_progress()  ← NEW
  → Output: optimal_iterative_* folders per strategy
```

### Requirement: Resume from crash

```
Entry: run_draft_order_loop.py (CLI)
  → main()
    → find_resume_point()
      → Load loop_progress.json
      → Check for intermediate_* in strategy folder
      → Return: (next_idx, "resume" if has intermediate, cycle)
    → LOOP: starts at next_idx
      → SimulationManager auto-resumes from intermediate_*
```

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:**
  - SimulationManager auto-resumes from `intermediate_*` folders (confirmed in code)
  - `output_dir` parameter allows per-strategy folders (confirmed in __init__)
  - `auto_update_league_config=False` prevents root data/configs updates (confirmed)
  - DRAFT_ORDER preserved through optimization (DRAFT_ORDER_FILE not in PARAMETER_ORDER)
- **Corrections made:** None needed
- **Confidence level:** High

### Round 2 (Iteration 13)
- **Verified correct:**
  - Test file structure corrected to use existing `test_root_scripts.py`
  - All task file references updated for consistency
  - SimulationManager interface fully understood
- **Corrections made:** Updated Phase 6 test file references from `test_run_draft_order_loop.py` to `test_root_scripts.py::TestRunDraftOrderLoop`
- **Confidence level:** High

### Round 3 (Iteration 22)
- **Verified correct:**
  - All edge cases have corresponding tasks and tests
  - Test coverage plan covers discovery, progress, folder management, edge cases
  - Integration Matrix complete - no orphan code
  - Pseudo-code in specs matches TODO tasks exactly
- **Corrections made:** None needed
- **Confidence level:** High - Ready to implement

---

## Progress Notes

**Last Updated:** 2025-12-09
**Current Status:** All 24 verification iterations complete. READY TO IMPLEMENT.
**Next Steps:** Begin implementation - execute Phase 1 tasks
**Blockers:** None

### Verification Round 1 Summary (7/7)
- Iterations 1-3: Researched existing code patterns in run_simulation.py, run_draft_order_simulation.py, run_simulation_loop.sh
- Iteration 4: Verified Algorithm Traceability Matrix covers all spec algorithms
- Iteration 5: Verified Data Flow Traces cover entry-to-output paths
- Iteration 6: Skeptical verification confirmed SimulationManager interface, DRAFT_ORDER preservation
- Iteration 7: Integration Gap Check confirmed all new methods have callers in Integration Matrix
- **Questions file:** Not needed - spec is clear and complete

### Verification Round 2 Summary (9/9)
- Iterations 8-10: Re-verified specs and TODO consistency
- Iteration 11: Algorithm Traceability re-verified
- Iteration 12: Data Flow re-verified
- Iteration 13: Skeptical check - corrected test file references
- Iteration 14: Integration Gap Check confirmed
- Iterations 15-16: Finalized TODO with corrected test file paths

### Verification Round 3 Summary (8/8)
- Iterations 17-18: Fresh Eyes Review of specs and pseudo-code
- Iteration 19: Algorithm Deep Dive confirmed spec-to-code mapping
- Iteration 20: Edge Case Verification - all have tasks + tests
- Iteration 21: Test Coverage Planning complete
- Iteration 22: Final Skeptical Re-verification passed
- Iteration 23: Final Integration Gap Check passed
- Iteration 24: Implementation Readiness confirmed
