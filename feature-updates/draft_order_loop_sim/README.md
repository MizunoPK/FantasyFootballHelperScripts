# Draft Order Loop Simulation - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** COMPLETE
**Current Step:** All QC rounds complete
**Next Action:** None - ready for merge

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create draft_order_loop_sim_specs.md
  - [x] Create draft_order_loop_sim_checklist.md
  - [x] Create draft_order_loop_sim_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] Analyze notes thoroughly
  - [x] Research codebase patterns
  - [x] Populate checklist with questions
  - [x] Update specs with context
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Wait for user direction
- [x] Phase 4: Resolve Questions
  - [x] Original checklist items (Q1-Q13) resolved
  - [x] Additional edge cases (Q14-Q21) resolved
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 1: Create TODO file
- [x] Step 2: First Verification Round (7 iterations)
- [x] Step 3: Create questions file (if needed) - SKIPPED (spec complete)
- [x] Step 4: Update TODO with answers - SKIPPED (no questions)
- [x] Step 5: Second Verification Round (9 iterations)
- [x] Step 6: Third Verification Round (8 iterations)
- [x] Implementation
- [x] Post-implementation QC rounds (3 rounds complete, all 2217 tests pass)

---

## What This Is

A new simulation runner script (`run_draft_order_loop.py`) that iterates through all draft order strategy files in `simulation/sim_data/draft_order_possibilities/`, running full iterative optimization for each one. Each draft strategy gets its own dedicated config folder, allowing parallel optimization of scoring parameters for different draft approaches.

## Why We Need This

1. **Strategy Comparison:** Determine optimal scoring parameters for each draft strategy separately
2. **Personalized Optimization:** Different draft strategies (zero-RB, hero-RB, balanced, etc.) may have different optimal parameter weights
3. **Continuous Optimization:** Run indefinitely, cycling through all strategies to continuously improve configs
4. **Fault Tolerance:** Auto-resume from crashes via `loop_progress.json` tracker and `intermediate_*` folder detection

## Scope

**IN SCOPE:**
- New `run_draft_order_loop.py` script
- New `run_draft_order_loop.sh` bash wrapper for auto-restart
- Per-strategy config folders (`simulation/simulation_configs/0_MINE/`, etc.)
- Resume detection: which JSON file and which parameter was left off
- Copy initial configs from root `simulation_configs/optimal_*` folders
- Use same optimizations as `run_simulation.py` (--use-processes, workers, etc.)
- Endless loop through all draft order files

**OUT OF SCOPE:**
- Modifying SimulationManager core logic
- Modifying ConfigGenerator core logic
- Changes to the draft_order_possibilities JSON format
- GUI or web interface

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `draft_order_loop_sim_notes.txt` | Original scratchwork notes from user |
| `draft_order_loop_sim_specs.md` | Main specification with detailed requirements |
| `draft_order_loop_sim_checklist.md` | Tracks open questions and decisions |
| `draft_order_loop_sim_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Existing Infrastructure

1. **run_simulation.py** - Main simulation script with:
   - Constants at top: `DEFAULT_WORKERS=8`, `DEFAULT_SIMS=5`, etc.
   - `--use-processes` flag for ProcessPoolExecutor
   - Auto-detects baseline from `optimal_*` or `intermediate_*` folders
   - Infinite loop in iterative mode

2. **run_simulation_loop.sh** - Bash wrapper that:
   - Traps SIGINT/SIGTERM for graceful shutdown
   - Restarts on exit codes 137 (SIGKILL) or 143 (SIGTERM)
   - Exits cleanly on exit code 0

3. **SimulationManager** - Orchestrates optimization with:
   - `run_iterative_optimization()` - coordinate descent optimization
   - Auto-resume from `intermediate_*` folders
   - Saves `optimal_*` folders with 4 config files
   - Updates `data/configs/` folder on completion

4. **draft_order_possibilities/** - Contains 18 active JSON files (plus archived ones):
   - Named `{N}_{description}.json` (e.g., `0_MINE.json`, `1_zero_rb.json`)
   - Each has `DRAFT_ORDER` array defining draft strategy
   - Files in `archive/` subfolder are inactive

### Output Structure

Current `simulation_configs/` structure:
```
simulation/simulation_configs/
├── optimal_iterative_20251209_153905/
│   ├── league_config.json
│   ├── week1-5.json
│   ├── week6-11.json
│   └── week12-17.json
└── intermediate_*/
```

**New per-strategy structure:**
```
simulation/simulation_configs/
├── strategies/
│   ├── 0_MINE/
│   │   ├── optimal_seed/           # Initial seeded configs
│   │   └── optimal_iterative_*/    # Optimization results
│   ├── 1_zero_rb/
│   │   └── ...
│   └── loop_progress.json          # Progress tracker
├── optimal_iterative_*/            # Root baseline
└── intermediate_*/
```

## What's Resolved (21/21 Questions)

**Original Questions (Q1-Q13):**
- Q1-Q3: Architecture (injection, progress tracking, DRAFT_ORDER_FILE)
- Q4-Q5: Output structure (folder naming, `strategies/` subfolder)
- Q6-Q8: Edge cases (corrupt folders, missing baseline, archive handling)
- Q9-Q11: Loop behavior (order, restart, completion)
- Q12-Q13: Integration (no data/configs update, no config sharing)

**Additional Edge Cases (Q14-Q21):**
- Q14-Q15: Seeding (`optimal_seed/` subfolder, inject DRAFT_ORDER on disk)
- Q16-Q18: Runtime (cleanup intermediate, let crash, no extra signals)
- Q19-Q21: Misc (name extraction, bounds check, file changes)

## What's Still Pending

All planning items resolved. Ready for implementation phase.

**Final Resolution Summary (Q14-Q21):**

| Question | Resolution |
|----------|------------|
| Q14: Seeding structure | `optimal_seed/` subfolder |
| Q15: DRAFT_ORDER injection | During seeding (write to disk) |
| Q16: intermediate_* cleanup | Clean up after completion |
| Q17: Error handling | Let crash (bash restarts) |
| Q18: Signal handling | No extra handlers needed |
| Q19: Strategy name extraction | Implementation detail |
| Q20: Progress bounds check | Reset with warning |
| Q21: File list changes | Documentation only |

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `draft_order_loop_sim_specs.md` for complete specifications
3. Read `draft_order_loop_sim_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
