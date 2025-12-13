# Draft Order Loop Simulation - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `draft_order_loop_sim_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Script naming:** Confirm `run_draft_order_loop.py` is acceptable ✓
- [x] **Bash script naming:** Confirm `run_draft_order_loop.sh` is acceptable ✓

---

## Architecture Questions

- [x] **Q1: DRAFT_ORDER injection method:** How should the DRAFT_ORDER from each strategy file be injected into the simulation config?
  - **RESOLVED: Option A** - Modify config dict before running SimulationManager
  - **Evidence:** `run_draft_order_simulation.py:282-283` shows the pattern:
    ```python
    config['parameters']['DRAFT_ORDER_FILE'] = file_num
    config['parameters']['DRAFT_ORDER'] = draft_order
    ```
  - No SimulationManager changes needed

- [x] **Q2: Progress tracking method:** How should we track which strategy/parameter is being optimized?
  - **RESOLVED: Hybrid approach** - Explicit progress file + folder state
  - **Progress file:** `simulation/simulation_configs/strategies/loop_progress.json` tracks:
    - `current_cycle`: Which optimization cycle (1, 2, 3, ...)
    - `last_completed_strategy`: Index of last completed strategy (0-based)
    - `last_updated`: Timestamp
  - **Folder state:** Still used for mid-optimization detection (`intermediate_*` folders)
  - **Rationale:** Progress file needed because `optimal_*` doesn't mean "skip" - we re-optimize each strategy every cycle

- [x] **Q3: DRAFT_ORDER_FILE parameter handling:** Should this parameter be optimized during the loop?
  - **RESOLVED: Option A** - Keep disabled (already commented out in `PARAMETER_ORDER`)
  - **Evidence:** `ConfigGenerator.py:193` - `# 'DRAFT_ORDER_FILE',` is commented out
  - Each strategy uses its fixed DRAFT_ORDER; we optimize other params around it

---

## Output Structure Questions

- [x] **Q4: Strategy folder naming:** What naming pattern for per-strategy folders?
  - **RESOLVED: Option A** - `{N}_{description}/` matching JSON filename
  - **Evidence:** Consistent with `draft_order_possibilities/{N}_{description}.json` naming
  - Examples: `0_MINE/`, `1_zero_rb/`, `2_hero_rb/`

- [x] **Q5: Where should strategy folders live?**
  - **RESOLVED: Option B** - `simulation/simulation_configs/strategies/{N}_{description}/`
  - Cleaner separation between root configs and per-strategy configs
  - `loop_progress.json` also lives in `strategies/` folder

---

## Edge Case Questions

- [x] **Q6: Corrupt/incomplete strategy folder handling:** What if a folder has missing or corrupt config files?
  - **RESOLVED: Option A** - Delete folder and re-seed from root optimal_*
  - **Evidence:** `run_simulation.py` auto-detects baseline when not found; same self-healing pattern
  - Required files: `league_config.json`, `week1-5.json`, `week6-11.json`, `week12-17.json`

- [x] **Q7: Missing root optimal_* folder:** What if no baseline exists?
  - **RESOLVED: Option A** - Error out with clear message
  - **Evidence:** `run_simulation.py:273-281` errors out if no baseline found
  - User must run base simulation first to establish a baseline

- [x] **Q8: Archive folder handling:** Should files in `archive/` subfolder be skipped?
  - **RESOLVED: Option A** - Skip archived files entirely
  - **Evidence:** `discover_draft_order_files()` uses `draft_order_dir.glob("*.json")` which doesn't recurse into subdirs
  - Files in `archive/` subfolder won't be discovered

---

## Loop Behavior Questions

- [x] **Q9: Loop order:** In what order should strategies be processed?
  - **RESOLVED: Option A** - Numeric order (0, 1, 2, ...)
  - **Evidence:** `run_draft_order_simulation.py:86` - `file_numbers.sort()`
  - Predictable, easy to track progress

- [x] **Q10: Starting point on restart:** When script restarts, where should it begin?
  - **RESOLVED: Option A** - Continue from the interrupted strategy
  - **Evidence:** `SimulationManager._detect_resume_state()` logic resumes from last `intermediate_*` folder
  - Efficient use of compute, no wasted work

- [x] **Q11: Completion behavior per strategy:** What happens after one strategy completes a full optimization pass?
  - **RESOLVED: Option A** - Move immediately to next strategy
  - **Evidence:** `run_iterative_optimization()` just saves and continues
  - Continuous optimization, no artificial delays

---

## Integration Questions

- [x] **Q12: Update data/configs after each strategy?** Should the root `data/configs/` folder be updated after each strategy completes?
  - **RESOLVED: Option B** - No, only the strategy-specific folder is updated
  - **Reasoning:** Each strategy has its own optimized config. The root `data/configs/` is the user's main config and shouldn't be overwritten by strategy-specific optimization.

- [x] **Q13: Inter-strategy config sharing:** Should a strategy that finishes benefit the next strategy?
  - **RESOLVED: Option A** - No, each starts fresh from its own folder or root optimal_*
  - **Reasoning:** Each strategy should be independently optimized. The whole point is to find the best params FOR THAT SPECIFIC draft strategy.

---

## Additional Edge Cases (Identified in Review)

- [x] **Q14: Seeding structure:** Where do the 4 config files go when seeding a new strategy folder?
  - **RESOLVED: Option B** - Copy into `optimal_seed/` subfolder
  - Structure: `strategies/0_MINE/optimal_seed/league_config.json`
  - Consistent with SimulationManager expecting `optimal_*` folders

- [x] **Q15: DRAFT_ORDER injection timing:** When should DRAFT_ORDER be injected into configs?
  - **RESOLVED: Option B** - During seeding (write to disk)
  - Config files become self-contained with correct DRAFT_ORDER
  - SimulationManager preserves all parameters in outputs

- [x] **Q16: intermediate_* cleanup after completion:** Should intermediate folders be cleaned up after saving optimal_*?
  - **RESOLVED: Option B** - Clean up after successful `optimal_*` save
  - Saves disk space; intermediate state only needed for resume
  - ~20 folders per strategy per cycle would accumulate otherwise

- [x] **Q17: Error handling during optimization:** What if `run_iterative_optimization()` raises an exception?
  - **RESOLVED: Option B** - Let it crash, bash script restarts
  - Transient errors auto-recover on restart
  - Persistent errors surface immediately for manual attention

- [x] **Q18: Signal handling at loop level:** Should the loop script have its own signal handlers?
  - **RESOLVED: Option A** - No extra handlers needed
  - SimulationManager handles graceful shutdown
  - Progress file only updated after completion (no corruption risk)

- [x] **Q19: Strategy name extraction:** How to get full filename stem for folder naming?
  - **RESOLVED:** Implementation detail
  - Function `get_strategy_name(file_num)` globs for matching JSON file, returns stem

- [x] **Q20: Progress file bounds checking:** What if `last_completed_strategy` exceeds current file list length?
  - **RESOLVED: Option A** - Reset to -1 (new cycle) with warning log
  - Self-healing behavior; file list changes don't require manual intervention

- [x] **Q21: Draft order file list changes:** What happens if files are added/removed/renamed between cycles?
  - **RESOLVED:** Documentation only, no special handling
  - Added: Discovered next cycle, sorted by number
  - Removed: Orphaned folder remains; bounds check handles index issues
  - Renamed: Old folder orphaned; new folder created when reached

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Draft order strategies | `simulation/sim_data/draft_order_possibilities/*.json` | Verified |
| Baseline configs | `simulation/simulation_configs/optimal_*/` | Verified |
| Historical seasons | `simulation/sim_data/20*/` | Verified |
| Config structure | 4-file folder (league_config.json + week*.json) | Verified |
| Strategy folders | `simulation/simulation_configs/strategies/{N}_{name}/` | **NEW - to be created** |
| Progress tracker | `simulation/simulation_configs/strategies/loop_progress.json` | **NEW - to be created** |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Q1: DRAFT_ORDER injection | Option A - Modify config dict | 2025-12-09 |
| Q2: Progress tracking | Hybrid - progress file + folder state | 2025-12-09 |
| Q3: DRAFT_ORDER_FILE param | Option A - Keep disabled | 2025-12-09 |
| Q4: Strategy folder naming | Option A - Match JSON filename | 2025-12-09 |
| Q5: Folder location | Option B - strategies/ subfolder | 2025-12-09 |
| Q6: Corrupt folder handling | Option A - Re-seed from root | 2025-12-09 |
| Q7: Missing baseline | Option A - Error out | 2025-12-09 |
| Q8: Archive handling | Option A - Skip archived files | 2025-12-09 |
| Q9: Loop order | Option A - Numeric order | 2025-12-09 |
| Q10: Restart point | Option A - Continue interrupted | 2025-12-09 |
| Q11: Completion behavior | Option A - Move immediately | 2025-12-09 |
| Q12: Update data/configs | Option B - No, strategy-only | 2025-12-09 |
| Q13: Config sharing | Option A - Independent per strategy | 2025-12-09 |
| Q14: Seeding structure | Option B - optimal_seed/ subfolder | 2025-12-09 |
| Q15: DRAFT_ORDER timing | Option B - Inject during seeding | 2025-12-09 |
| Q16: intermediate_* cleanup | Option B - Clean up after completion | 2025-12-09 |
| Q17: Error handling | Option B - Let it crash | 2025-12-09 |
| Q18: Signal handling | Option A - No extra handlers | 2025-12-09 |
| Q19: Strategy name extraction | Implementation detail | 2025-12-09 |
| Q20: Progress bounds check | Option A - Reset with warning | 2025-12-09 |
| Q21: File list changes | Documentation only | 2025-12-09 |
