# Codebase Research Findings

## Round 1: Initial Codebase Research

### 1. Runner Scripts Pattern (from run_simulation.py)

**CLI Arguments:**
```
--mode (single/full/iterative)  # Default: iterative
--sims (int)                    # Simulations per config, default 5
--baseline (str)                # Path to baseline config folder
--output (str)                  # Output directory, default: simulation/simulation_configs
--workers (int)                 # Parallel workers, default 8
--data (str)                    # Data folder, default: simulation/sim_data
--test-values (int)             # Test values per param, default 99
--use-processes                 # Use ProcessPoolExecutor vs ThreadPoolExecutor
```

**Baseline Resolution Priority:**
1. User-specified --baseline path
2. Most recent intermediate_*/ folder (for iterative mode resumption)
3. Most recent optimal_*/ folder in output directory
4. Fallback to simulation/simulation_configs

**Validation:** Requires 5 JSON files in config folder: league_config.json + 4 week files

### 2. Shell Loop Pattern (from run_simulation_loop.sh)

```bash
trap "echo 'Stopping...'; exit 0" SIGINT SIGTERM
while true; do
    python run_simulation.py --use-processes
    # exit 137/143 (killed) → restart after 2s
    # exit 0 (success) → break
    # other exit codes → restart after 2s
done
```

### 3. Signal Handling (from SimulationManager.py)

**Implemented:**
- SIGINT (Ctrl+C) and SIGTERM handlers
- Graceful shutdown: updates league_config.json before exit
- Tracks `_current_optimal_config_path` for shutdown
- Restores original handlers after completion

**Code location:** SimulationManager.py lines 261-303

### 4. Intermediate Results (from SimulationManager.py, ResultsManager.py)

**Folder naming:** `intermediate_{param_index:02d}_{param_name}/`
**Contains:** Full 5-JSON structure (league_config.json + 4 week files)
**Resume logic:** Scans for intermediate folders, finds most recent, resumes from next parameter

**Code location:** SimulationManager.py lines 515-620, ResultsManager.py lines 456-559

### 5. Results Storage Pattern

**Location:** `simulation/simulation_configs/` (default)
**Optimal folders:** `optimal_TIMESTAMP/`
**Intermediate folders:** `intermediate_{idx}_{param}/`

**JSON structure:**
```json
{
  "config_name": "...",
  "description": "...",
  "parameters": {...},
  "performance_metrics": {
    "overall_win_rate": 0.732,
    "total_wins": 112,
    "total_losses": 41,
    "config_id": "...",
    "timestamp": "20251210_024739"
  }
}
```

### 6. Week Ranges (from ConfigPerformance.py)

```python
WEEK_RANGES = ["1-5", "6-9", "10-13", "14-17"]
```

Used throughout for per-range tracking and best config selection.

### 7. Config Loading (from ConfigManager.py)

**New structure check:** `data/configs/` folder
**Week config selection:** Based on CURRENT_NFL_WEEK
**Fallback:** Legacy `data/league_config.json`

**No draft_config.json handling exists** - would need to be added

### 8. sim_data Structure

```
sim_data/{year}/
├── game_data.csv
├── season_schedule.csv
├── team_data/
└── weeks/
    └── week_XX/
        ├── players.csv           # Contains ALL 17 weeks of data
        └── players_projected.csv # Contains ALL 17 weeks of data
```

**Key insight:** Weekly CSVs contain full season data with week_N_points columns.
Bye weeks are represented as empty values in those columns.

### 9. No __init__.py Files

Simulation folder uses `sys.path.append()` pattern, no __init__.py files.

### 10. Multi-Season Handling (from SimulationManager.py)

**Discovery:** `_discover_seasons()` finds all `20XX/` folders in sim_data
**Validation:** Each season must have 150+ valid players
**Aggregation:** Results aggregated across all historical seasons

---

## Checklist Items Resolved by Research

### Runner Scripts Setup
- [x] **CLI args:** Should mirror run_simulation.py pattern (--mode, --sims, --baseline, --output, --workers, --data, --test-values, --use-processes)
- [x] **Shell loop:** Should mirror run_simulation_loop.sh pattern (trap signals, restart on kill/error, exit on success)
- [x] **Entry point:** Independent scripts (not shared base) - matches existing pattern

### Results Storage
- [x] **Location:** Same parent folder (simulation/simulation_configs/)
- [x] **Naming:** `accuracy_optimal_TIMESTAMP/` (matches optimal_TIMESTAMP pattern)
- [x] **Format:** Same 5-JSON structure
- [x] **Intermediate:** Yes, `accuracy_intermediate_{idx}_{param}/`

### Operational Concerns
- [x] **Signal handling:** Yes, same pattern as win-rate (SIGINT/SIGTERM graceful shutdown)
- [x] **Resume capability:** Yes, via intermediate folders
- [x] **Backwards compatibility:** No __init__.py files currently, uses sys.path.append

### Architecture
- [x] **Folder structure:** Specs show shared/ subfolder - this is the INTENDED structure (notes say "root" but that's ambiguous)
- [x] **__init__.py:** Not currently used, but should be added for cleaner imports

### Week Ranges
- [x] **Confirmed:** Same ranges as win-rate (1-5, 6-9, 10-13, 14-17)

### Data Sources
- [x] **Bye week handling:** Empty values in week_N_points columns - skip those weeks in accuracy calculation
- [x] **Data format:** Weekly CSVs have all 17 weeks, actual vs projected available

### Multi-Season
- [x] **Aggregation:** Same approach as win-rate (aggregate across all historical seasons)

---

## Round 2: Skeptical Re-verification

### 1. Weekly CSV Snapshots (CRITICAL FINDING)

**Verified:** Weekly CSVs are **SNAPSHOTS** at that point in time, not cumulative.

**Evidence:**
```
# Week 5 CSV - Josh Allen (weeks 5-9):
week_5=20.4, week_6=18.1, week_7=19.1, week_8=23.7, week_9=22.4

# Week 10 CSV - Josh Allen (same weeks):
week_5=14.6, week_6=24.4, week_7=21.0, week_8=19.8, week_9=22.1
```

**Implication:** Data isolation is **built into the data structure**. When evaluating week 5 accuracy, use week_05/players.csv which contains projections as of week 5. This is ideal for fair testing.

### 2. No __init__.py Files

**Verified:** Zero __init__.py files exist in simulation folder.
**Verified:** All 10 Python files in simulation/ use `sys.path.append()` pattern.

### 3. ConfigManager draft_config.json Status

**Verified:** ConfigManager at `league_helper/util/ConfigManager.py` does NOT currently support draft_config.json.

**Current behavior:**
1. Loads `data/configs/league_config.json` as base
2. Merges `data/configs/weekX-Y.json` over base based on CURRENT_NFL_WEEK
3. No awareness of draft_config.json

**Needed:** Add support for loading draft_config.json for Add to Roster Mode.

### 4. Parameter Split Verification

**league_config.json contains:**
- NFL settings (CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT)
- SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT
- INJURY_PENALTIES
- DRAFT_ORDER_BONUSES, DRAFT_ORDER, DRAFT_ORDER_FILE
- MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS
- ADP_SCORING (confirmed - strategy param)

**week1-5.json contains:**
- NORMALIZATION_MAX_SCALE
- PLAYER_RATING_SCORING
- TEAM_QUALITY_SCORING
- PERFORMANCE_SCORING
- MATCHUP_SCORING
- SCHEDULE_SCORING
- TEMPERATURE_SCORING
- WIND_SCORING
- LOCATION_MODIFIERS

**Confirmed:** NO overlap between league_config.json and week configs.

### 5. sim_data Structure Verification

**Available seasons:** 2021, 2022, 2024 (no 2023 folder found)
**Weekly structure:** Each year has weeks/week_01 through week_17
**Files per week:** players.csv (actuals) and players_projected.csv (projections)
**Columns:** Include week_1_points through week_17_points for each player

---

## Items Requiring User Decision

### ROS Evaluation
- **Question:** At what week evaluate ROS accuracy?
- **Options:**
  1. Week 1 only (pre-draft snapshot)
  2. Multiple starting points (week 1, 5, 10)
  3. Each week's ROS vs remaining season actual
- **Recommendation:** Week 1 only (simplest, matches draft use case)

### Data Isolation
- **Question:** Use only data available at evaluation time?
- **Finding:** Weekly CSVs already have the "as of that week" snapshots
- **Options:**
  1. Yes - strict data isolation (use week X data for week X evaluation)
  2. No - use final actual data throughout
- **Recommendation:** Yes, strict isolation for fair testing

### Player Filtering
- **Question:** Minimum thresholds for inclusion?
- **Options:**
  1. No filtering
  2. Projection threshold (e.g., >5 pts/week)
  3. Games played threshold
- **Recommendation:** Filter bye weeks (empty values), include all others

### Best Config Selection
- **Question:** Lower MAE = better (opposite of win-rate)
- **Recommendation:** Confirmed - lowest MAE wins

### Parameter Scope
- **Question:** Which parameters to optimize?
- **Finding:** ConfigGenerator has all 23 parameters defined
- **Options:**
  1. All 23 (same as win-rate)
  2. Subset relevant to prediction (exclude DRAFT_ORDER bonuses?)
- **Recommendation:** Start with all 23, can narrow later
