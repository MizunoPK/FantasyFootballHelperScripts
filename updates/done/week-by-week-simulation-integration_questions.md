# Week-by-Week Simulation Integration - Questions

These questions were identified during the first verification round (7 iterations) of TODO preparation.

---

## Q1: Should full optimization mode also use per-week tracking?

**Context:**
The original spec says "updating the simulation" which is general and could apply to all modes:
- `run_full_optimization()` - tests all parameter combinations
- `run_iterative_optimization()` - tests one parameter at a time
- `run_single_config_test()` - tests a single config

Currently, the TODO focuses on iterative mode. Full optimization mode also:
- Uses `run_simulations_for_config()` (line 225)
- Uses `record_result()` (line 232)
- Saves to single file via `save_optimal_config()` (line 261)

**Options:**
- **A) Yes, update both modes**: Both iterative and full optimization should use per-week tracking and folder output for consistency
- **B) No, only update iterative mode**: Full optimization is rarely used and can remain unchanged
- **C) Update full mode output only**: Use folder output for full mode but keep simple tracking (no per-week)

**Recommendation:** Option A for consistency, but this increases scope.

Answer: Option B. We are going to remove the full optimization in the future

---

## Q2: How to handle backward compatibility for baseline loading?

**Context:**
The original spec (line 7) says: "No need for backward compatibility"

However, the current ConfigManager implementation maintains backward compatibility:
- Can load from `data/configs/` folder (new format)
- Can also load from `data/league_config.json` (old format)

For ConfigGenerator baseline loading:
- Should it ONLY accept folder input?
- Or should it also accept single file for backward compatibility?

**Options:**
- **A) Folder only**: ConfigGenerator.load_baseline_from_folder() is the only path; single files rejected
- **B) Both formats**: ConfigGenerator can accept folder OR single file (auto-detect)
- **C) Config determines format**: If loading from folder, output folder; if loading from file, output file

**Recommendation:** Option B for flexibility during transition period.

Answer: Option A

---

## Q3: What should happen when old intermediate_*.json files are detected?

**Context:**
If a user starts iterative optimization with the new system but has old `intermediate_*.json` files from a previous run:
- These files won't work with the new folder-based system
- The resume detection would fail or produce incorrect results

**Options:**
- **A) Auto-migrate**: Convert old .json files to folder structure automatically
- **B) Warn and skip**: Log warning, ignore old files, start fresh
- **C) Error and stop**: Raise error requiring manual cleanup
- **D) Delete old files**: Automatically clean up old .json files and start fresh

**Recommendation:** Option B or D - warn/cleanup and start fresh is simpler than migration.

Answer: Option C

---

## Q4: Should intermediate folders include performance metrics?

**Context:**
The current intermediate saves include config_name and description with win rate.
The new `save_optimal_configs_folder()` includes `performance_metrics` in each file.

For intermediate folders:
- Should they include performance metrics?
- Should metrics be per-range (showing why each week file was chosen)?

**Options:**
- **A) Full metrics**: Include performance_metrics with per-range win rates in each file
- **B) Simple metrics**: Just include overall win rate in description
- **C) No metrics**: Intermediate files are just configs, no performance data

**Recommendation:** Option A for debugging and transparency.

Answer: Option A

---

## Q5: Should auto_update_league_config update the folder structure?

**Context:**
Currently, `auto_update_league_config=True` updates `data/league_config.json` with optimal parameters.

With the new folder structure:
- Should it update `data/configs/` folder instead?
- Should it update all 4 files (league_config.json + 3 week files)?
- Or should it only update the single legacy file?

**Options:**
- **A) Update folder**: Update all 4 files in `data/configs/` folder
- **B) Update legacy file**: Keep updating `data/league_config.json` (for backward compatibility)
- **C) Update both**: Update both folder and legacy file
- **D) Remove feature**: Don't auto-update; user manually copies optimal config

**Recommendation:** Option A if legacy file is truly deprecated; Option C during transition.

Answer: Option A

---

## Summary of Questions

| # | Question | Options | Recommendation |
|---|----------|---------|----------------|
| Q1 | Full optimization mode per-week tracking? | A/B/C | A (both modes) |
| Q2 | Backward compatibility for baseline loading? | A/B/C | B (both formats) |
| Q3 | Old intermediate_*.json files handling? | A/B/C/D | B or D (warn/cleanup) |
| Q4 | Intermediate folders include metrics? | A/B/C | A (full metrics) |
| Q5 | Auto-update target (folder vs file)? | A/B/C/D | A or C (folder) |

---

Please provide your answers to these questions so I can proceed with the second verification round (iterations 8-16) and finalize the implementation plan.
