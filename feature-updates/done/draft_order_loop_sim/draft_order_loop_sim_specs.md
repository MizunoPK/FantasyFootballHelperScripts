# Draft Order Loop Simulation

## Objective

Create a simulation runner script that loops through all draft order strategy files, running full iterative optimization for each strategy with dedicated output folders, supporting auto-resume and crash recovery.

---

## High-Level Requirements

### 1. New Script: `run_draft_order_loop.py`

- **Location:** Project root (alongside `run_simulation.py`)
- **Purpose:** Loop through draft_order_possibilities files, run iterative optimization for each
- **Constants at top:** Same pattern as `run_simulation.py`:
  - `DEFAULT_WORKERS`, `DEFAULT_SIMS`, `DEFAULT_TEST_VALUES`, etc.
  - Logging configuration

### 2. Draft Order File Discovery

- **Source folder:** `simulation/sim_data/draft_order_possibilities/`
- **Pattern:** `{N}_{description}.json` files (NOT files in `archive/` subfolder)
- **Ordering:** Process files in numeric order (0, 1, 2, ..., N)
- **Behavior:** Skip archived files (glob doesn't recurse into subdirs)
- **Reuse:** Can reuse `discover_draft_order_files()` from `run_draft_order_simulation.py`

### 3. Per-Strategy Output Folders

- **Structure:** `simulation/simulation_configs/strategies/{N}_{description}/`
  - Example: `simulation/simulation_configs/strategies/0_MINE/`
  - Example: `simulation/simulation_configs/strategies/1_zero_rb/`
- **Contents:**
  - `optimal_seed/` - Initial seeded configs (created when folder is first seeded)
  - `optimal_iterative_*/` - Results from optimization runs
  - `intermediate_*/` - Progress during optimization (cleaned up after completion)

**Full structure:**
```
simulation/simulation_configs/
├── strategies/
│   ├── 0_MINE/
│   │   ├── optimal_seed/
│   │   │   ├── league_config.json
│   │   │   ├── week1-5.json
│   │   │   ├── week6-11.json
│   │   │   └── week12-17.json
│   │   └── optimal_iterative_20251209_*/
│   ├── 1_zero_rb/
│   └── loop_progress.json
├── optimal_iterative_*/        # root baseline
└── intermediate_*/
```

### 4. Initial Config Seeding

When a strategy folder doesn't exist yet:
1. Create the strategy folder and `optimal_seed/` subfolder
2. Copy latest `optimal_*` configs from root `simulation/simulation_configs/` into `optimal_seed/`
3. Inject DRAFT_ORDER into `optimal_seed/league_config.json`:
   ```python
   config['parameters']['DRAFT_ORDER_FILE'] = file_num
   config['parameters']['DRAFT_ORDER'] = draft_order
   ```
4. Write the modified config back to disk (config files are self-contained)

### 5. Progress Tracking and Resume Detection

#### Progress Tracker File

`simulation/simulation_configs/strategies/loop_progress.json`:
```json
{
  "current_cycle": 3,
  "last_completed_strategy": 5,
  "last_updated": "2025-12-09 15:30:00"
}
```

- **current_cycle**: Which optimization cycle we're on (1, 2, 3, ...)
- **last_completed_strategy**: Index of last strategy that finished (0-based)
- **last_updated**: Timestamp for debugging/monitoring

#### Resume Logic

The script must detect:
1. **Which cycle** we're on - from `loop_progress.json`
2. **Which strategy** to process next - `last_completed_strategy + 1`
3. **Whether mid-optimization** - check for `intermediate_*` folders in strategy folder

```python
def find_resume_point(draft_files, config_dir):
    progress_file = config_dir / "loop_progress.json"

    # Load progress (or initialize if first run)
    if progress_file.exists():
        progress = load_json(progress_file)
        last_completed = progress["last_completed_strategy"]
        current_cycle = progress["current_cycle"]
    else:
        last_completed = -1  # None completed yet
        current_cycle = 1

    # Next strategy to process
    next_strategy_idx = last_completed + 1

    # Check if we've completed all strategies in this cycle
    if next_strategy_idx >= len(draft_files):
        # Start new cycle
        current_cycle += 1
        next_strategy_idx = 0

    next_file_num = draft_files[next_strategy_idx]
    strategy_folder = config_dir / get_strategy_name(next_file_num)

    # Check if mid-optimization (has intermediate_*)
    if strategy_folder.exists():
        intermediate_folders = list(strategy_folder.glob("intermediate_*"))
        if intermediate_folders:
            return next_file_num, "resume", current_cycle

    return next_file_num, "start", current_cycle
```

#### When to Update Progress File

- **After each strategy completes** - Update `last_completed_strategy` after `run_iterative_optimization()` finishes
- **NOT during intermediate saves** - If interrupted mid-optimization, we resume from `intermediate_*` folder
- **On cycle boundary** - When `last_completed_strategy` reaches max, increment `current_cycle` and reset to -1

#### Folder States and Actions

| Progress File Says | Folder State | Action |
|-------------------|--------------|--------|
| Doesn't exist | - | Start cycle 1, strategy 0 |
| `last_completed: 3` | Strategy 4 has `intermediate_*` | Resume strategy 4 mid-optimization |
| `last_completed: 3` | Strategy 4 has no `intermediate_*` | Start strategy 4 fresh (use its `optimal_*` as baseline) |
| `last_completed: 3` | Strategy 4 doesn't exist | Seed strategy 4 from root baseline, then start |
| `last_completed: N` (last) | - | Increment cycle, start strategy 0 |

### 6. Endless Loop Behavior

- Loop through all draft order files continuously
- After completing all strategies, start again from the first
- Continue until user interrupts (Ctrl+C)

### 7. Bash Wrapper: `run_draft_order_loop.sh`

- **Location:** Project root
- **Behavior:** Same as `run_simulation_loop.sh`:
  - Trap SIGINT/SIGTERM for graceful shutdown
  - Restart on exit codes 137/143
  - Exit cleanly on code 0

### 8. Command-Line Interface

Support same arguments as `run_simulation.py`:
- `--sims`: Number of simulations per config
- `--workers`: Number of parallel workers
- `--test-values`: Number of test values per parameter
- `--use-processes`: Use ProcessPoolExecutor
- `--data`: Path to simulation data folder

---

## Resolved Implementation Details

### DRAFT_ORDER Injection (Q1)

Modify config dict directly before passing to SimulationManager:
```python
# From run_draft_order_simulation.py:282-283
config['parameters']['DRAFT_ORDER_FILE'] = file_num
config['parameters']['DRAFT_ORDER'] = draft_order
```
No changes to SimulationManager needed.

### Progress Tracking (Q2)

Use explicit progress tracker file `loop_progress.json`:
- Tracks `current_cycle` and `last_completed_strategy`
- Updated after each strategy completes (not during intermediate saves)
- Combined with folder state (`intermediate_*` presence) for full resume detection

Folder state still used for mid-optimization detection:
- Has `intermediate_*` folder → Resume from that parameter
- Has `optimal_*` folder only → Start fresh optimization using `optimal_*` as baseline
- Doesn't exist → Seed from root baseline and start

### DRAFT_ORDER_FILE Parameter (Q3)

Keep disabled in `PARAMETER_ORDER` (already commented out in ConfigGenerator.py:193).
Each strategy uses its fixed DRAFT_ORDER; we optimize other params around it.

### Strategy Folder Naming (Q4)

Match JSON filename: `{N}_{description}/`
- `0_MINE/` (from `0_MINE.json`)
- `1_zero_rb/` (from `1_zero_rb.json`)

### Folder Location (Q5)

`simulation/simulation_configs/strategies/{N}_{description}/`

Progress tracker: `simulation/simulation_configs/strategies/loop_progress.json`

### Corrupt Folder Handling (Q6)

Delete and re-seed from root `optimal_*` if any required files are missing:
- `league_config.json`
- `week1-5.json`
- `week6-11.json`
- `week12-17.json`

### Missing Baseline (Q7)

Error out with clear message if no `optimal_*` folder exists in root `simulation_configs/`.
User must run base simulation first.

### Archive Handling (Q8)

Skip automatically - `glob("*.json")` doesn't recurse into `archive/` subfolder.

### Loop Order (Q9)

Numeric order (0, 1, 2, ...) using sorted file numbers.

### Restart Point (Q10)

Continue from interrupted strategy based on folder state.

### Completion Behavior (Q11)

Move immediately to next strategy after saving optimal config.

### Update data/configs (Q12)

NO - Each strategy has its own folder. Root `data/configs/` is not updated.

### Config Sharing (Q13)

NO - Each strategy is independently optimized. No sharing between strategies.

---

## Additional Edge Cases (All Resolved)

### Q14: Seeding Structure ✓

**Resolution:** Copy into `optimal_seed/` subfolder

When seeding a new strategy folder:
```
simulation/simulation_configs/strategies/0_MINE/
└── optimal_seed/
    ├── league_config.json      # Seeded from root optimal_*, DRAFT_ORDER injected
    ├── week1-5.json
    ├── week6-11.json
    └── week12-17.json
```

### Q15: DRAFT_ORDER Injection Timing ✓

**Resolution:** Inject during seeding (write to disk)

```python
def seed_strategy_folder(strategy_folder, root_baseline, file_num, data_folder):
    """Seed a new strategy folder from root baseline with DRAFT_ORDER injected."""
    # Create optimal_seed subfolder
    seed_folder = strategy_folder / "optimal_seed"
    seed_folder.mkdir(parents=True, exist_ok=True)

    # Copy 4 config files from root baseline into optimal_seed/
    for filename in ['league_config.json', 'week1-5.json', 'week6-11.json', 'week12-17.json']:
        src = root_baseline / filename
        dst = seed_folder / filename
        shutil.copy(src, dst)

    # Load and inject DRAFT_ORDER into league_config.json
    draft_order = load_draft_order_from_file(file_num, data_folder)
    league_config_path = seed_folder / 'league_config.json'

    with open(league_config_path, 'r') as f:
        config = json.load(f)

    config['parameters']['DRAFT_ORDER_FILE'] = file_num
    config['parameters']['DRAFT_ORDER'] = draft_order

    with open(league_config_path, 'w') as f:
        json.dump(config, f, indent=2)
```

**Rationale:** Config files are self-contained. SimulationManager preserves all parameters in outputs.

### Q16: intermediate_* Cleanup After Completion ✓

**Resolution:** Clean up after successful `optimal_*` save

```python
def cleanup_intermediate_folders(strategy_folder):
    """Remove intermediate_* folders after successful optimization."""
    for folder in strategy_folder.glob("intermediate_*"):
        if folder.is_dir():
            shutil.rmtree(folder)
```

**Rationale:** Saves disk space. Intermediate state only needed for resume.

### Q17: Error Handling During Optimization ✓

**Resolution:** Let it crash (bash script restarts and resumes)

- Transient errors (OOM, network) auto-recover on restart
- Persistent errors surface immediately for manual attention
- Simpler code, no try/except complexity

### Q18: Signal Handling at Loop Level ✓

**Resolution:** No additional handlers needed

- SimulationManager already handles SIGINT/SIGTERM gracefully
- Progress file only updated AFTER strategy completes (no mid-write corruption)
- Bash wrapper handles restart logic

### Q19: Strategy Name Extraction ✓

**Resolution:** Implementation detail

```python
def get_strategy_name(file_num: int, data_folder: Path) -> str:
    """Get strategy folder name from file number."""
    draft_order_dir = data_folder / "draft_order_possibilities"

    # Try pattern with suffix first (e.g., 1_zero_rb.json)
    matches = list(draft_order_dir.glob(f"{file_num}_*.json"))
    if matches:
        return matches[0].stem  # "1_zero_rb"

    # Try exact match (e.g., 1.json)
    matches = list(draft_order_dir.glob(f"{file_num}.json"))
    if matches:
        return matches[0].stem  # "1"

    raise FileNotFoundError(f"No draft order file found for number {file_num}")
```

### Q20: Progress File Bounds Checking ✓

**Resolution:** Reset to -1 (start new cycle) with warning log

```python
def find_resume_point(draft_files, strategies_dir):
    progress_file = strategies_dir / "loop_progress.json"

    if progress_file.exists():
        progress = load_json(progress_file)
        last_completed = progress["last_completed_strategy"]
        current_cycle = progress["current_cycle"]

        # Bounds check: if files were removed, reset
        if last_completed >= len(draft_files):
            logger.warning(
                f"Progress index {last_completed} exceeds file count {len(draft_files)}. "
                f"Resetting to start of new cycle."
            )
            last_completed = -1
            current_cycle += 1
    else:
        last_completed = -1
        current_cycle = 1

    # ... rest of logic
```

### Q21: Draft Order File List Changes ✓

**Resolution:** Documentation only, no special handling

| Change | Behavior |
|--------|----------|
| File added | Discovered on next cycle, sorted into position by number |
| File removed | Orphaned folder remains; progress bounds check handles index issues |
| File renamed | Old folder orphaned; new folder created when number is reached |

---

## Existing Patterns to Reuse

**From run_simulation.py:**
- Argument parsing structure
- Constants definition pattern
- Logging setup
- `find_config_folders()` helper function
- Baseline config resolution logic

**From run_draft_order_simulation.py:**
- `discover_draft_order_files()` - Find and sort draft order JSON files
- `load_draft_order_from_file()` - Load DRAFT_ORDER array from JSON
- DRAFT_ORDER injection pattern

**From run_simulation_loop.sh:**
- Signal trapping pattern (SIGINT/SIGTERM)
- Exit code handling (137, 143, 0)
- Restart loop structure

**From SimulationManager:**
- `_detect_resume_state()` logic for intermediate folder detection
- `run_iterative_optimization()` for the actual optimization
- Config folder structure with 4 JSON files

---

## Implementation Notes

### Files to Create
- `run_draft_order_loop.py` - New script
- `run_draft_order_loop.sh` - New bash wrapper

### Files to Potentially Modify
- None - this is additive functionality

### Dependencies
- `simulation/SimulationManager.py` - Used as-is
- `simulation/ConfigGenerator.py` - Used as-is
- `simulation/ResultsManager.py` - Used as-is

### Testing Strategy
- Unit tests for new helper functions (strategy folder management, seeding, resume detection)
- Integration test with mock draft order files
- Manual testing with real simulation data

---

## Pseudo-code Outline

```python
def main():
    # Parse args (same as run_simulation.py)
    config_dir = Path("simulation/simulation_configs")
    strategies_dir = config_dir / "strategies"
    strategies_dir.mkdir(exist_ok=True)
    progress_file = strategies_dir / "loop_progress.json"

    # Find root baseline (error if none)
    root_baseline = find_latest_optimal_folder(config_dir)
    if not root_baseline:
        logger.error("No optimal_* folders found in simulation_configs/")
        logger.error("Please run 'python run_simulation.py iterative' first.")
        sys.exit(1)

    # Discover draft order files
    draft_files = discover_draft_order_files(data_folder)  # [0, 1, 2, ..., N]

    # Find resume point
    start_idx, action, current_cycle = find_resume_point(draft_files, strategies_dir)
    logger.info(f"Resuming at cycle {current_cycle}, strategy index {start_idx} ({action})")

    # Endless loop
    while True:
        # Process strategies from resume point to end
        for idx in range(start_idx, len(draft_files)):
            file_num = draft_files[idx]
            strategy_name = get_strategy_name(file_num, data_folder)  # "0_MINE", "1_zero_rb"
            strategy_folder = strategies_dir / strategy_name

            # Ensure strategy folder exists and is valid (seed if needed)
            ensure_strategy_folder(strategy_folder, root_baseline, file_num, data_folder)

            # Determine baseline for this run (most recent optimal_* in strategy folder)
            baseline = get_strategy_baseline(strategy_folder)

            # Run iterative optimization for this strategy
            # (DRAFT_ORDER already in config files from seeding)
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

            # Clean up intermediate folders after successful completion
            cleanup_intermediate_folders(strategy_folder)

            # Update progress tracker
            update_progress(progress_file, last_completed=idx, cycle=current_cycle)
            logger.info(f"Completed optimization for {strategy_name}")

        # All strategies complete for this cycle
        logger.info(f"Cycle {current_cycle} complete. Starting cycle {current_cycle + 1}...")
        current_cycle += 1
        start_idx = 0  # Reset to first strategy for new cycle


def ensure_strategy_folder(strategy_folder, root_baseline, file_num, data_folder):
    """Ensure strategy folder exists with valid configs. Seed if needed."""
    seed_folder = strategy_folder / "optimal_seed"
    required_files = ['league_config.json', 'week1-5.json', 'week6-11.json', 'week12-17.json']

    # Check if we need to seed
    needs_seed = False
    if not strategy_folder.exists():
        needs_seed = True
    elif not seed_folder.exists():
        # Check for any optimal_* folder
        optimal_folders = list(strategy_folder.glob("optimal_*"))
        if not optimal_folders:
            needs_seed = True

    if needs_seed:
        seed_strategy_folder(strategy_folder, root_baseline, file_num, data_folder)
    else:
        # Validate existing folder has required files somewhere
        has_valid_baseline = False
        for opt_folder in strategy_folder.glob("optimal_*"):
            if all((opt_folder / f).exists() for f in required_files):
                has_valid_baseline = True
                break

        if not has_valid_baseline:
            logger.warning(f"Corrupt strategy folder {strategy_folder.name}, re-seeding")
            shutil.rmtree(strategy_folder)
            seed_strategy_folder(strategy_folder, root_baseline, file_num, data_folder)


def seed_strategy_folder(strategy_folder, root_baseline, file_num, data_folder):
    """Seed a new strategy folder from root baseline with DRAFT_ORDER injected."""
    seed_folder = strategy_folder / "optimal_seed"
    seed_folder.mkdir(parents=True, exist_ok=True)

    # Copy 4 config files from root baseline
    for filename in ['league_config.json', 'week1-5.json', 'week6-11.json', 'week12-17.json']:
        shutil.copy(root_baseline / filename, seed_folder / filename)

    # Inject DRAFT_ORDER into league_config.json
    draft_order = load_draft_order_from_file(file_num, data_folder)
    league_config_path = seed_folder / 'league_config.json'

    with open(league_config_path, 'r') as f:
        config = json.load(f)

    config['parameters']['DRAFT_ORDER_FILE'] = file_num
    config['parameters']['DRAFT_ORDER'] = draft_order

    with open(league_config_path, 'w') as f:
        json.dump(config, f, indent=2)

    logger.info(f"Seeded strategy folder: {strategy_folder.name}")


def get_strategy_baseline(strategy_folder):
    """Get the best baseline to use for this strategy's optimization."""
    # Prefer most recent optimal_iterative_* if exists (from previous optimization)
    optimal_folders = sorted(
        [f for f in strategy_folder.glob("optimal_*") if f.name != "optimal_seed"],
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if optimal_folders:
        return optimal_folders[0]

    # Fall back to optimal_seed
    seed_folder = strategy_folder / "optimal_seed"
    if seed_folder.exists():
        return seed_folder

    raise ValueError(f"No valid baseline found in {strategy_folder}")


def cleanup_intermediate_folders(strategy_folder):
    """Remove intermediate_* folders after successful optimization."""
    for folder in strategy_folder.glob("intermediate_*"):
        if folder.is_dir():
            shutil.rmtree(folder)
            logger.debug(f"Cleaned up: {folder.name}")


def update_progress(progress_file, last_completed, cycle):
    """Update progress tracker file after strategy completion."""
    progress = {
        "current_cycle": cycle,
        "last_completed_strategy": last_completed,
        "last_updated": datetime.now().isoformat()
    }
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)
```

---

## Status: READY FOR IMPLEMENTATION ✓

All 21 questions resolved. Planning phase complete.
