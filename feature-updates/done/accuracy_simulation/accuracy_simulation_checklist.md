# Accuracy Simulation - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `accuracy_simulation_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Accuracy metric:** MAE (Mean Absolute Error) - single metric, no secondary
- [x] **Player weighting:** Equal weight - every player's error counts the same
- [x] **Week ranges:** Same as win-rate: 1-5, 6-9, 10-13, 14-17 (from WEEK_RANGES in ConfigPerformance.py)
- [x] **Season-long vs Weekly modes:** Both required - ROS optimizes draft_config.json, Weekly optimizes week-specific configs
- [x] **Position-specific accuracy:** Aggregate only - single MAE across all players
- [x] **Baseline comparison:** No - just optimize MAE directly without baseline comparison
- [x] **ROS evaluation timing:** Week 1 only - test pre-season predictions vs actual season totals (matches draft use case)
- [x] **ROS vs Weekly run order:** Configurable via --mode (ros/weekly/both). Default=both, runs ROS first then Weekly

---

## New Config File: draft_config.json

- [x] **Initial creation:** Create as copy of week1-5.json
- [x] **File location:** Same folder as other configs (data/configs/)
- [x] **Add to Roster Mode update:** Modify to use draft_config.json for prediction params
- [x] **Win Rate Simulation scope:** Will only optimize league_config.json (draft strategy)
- [x] **Parameter overlap:** NO overlap - league_config.json has strategy params (DRAFT_ORDER, BYE weights, ADP), draft_config.json has prediction params (NORMALIZATION, PLAYER_RATING, MATCHUP, etc.)
- [x] **Config loading in league_helper:** Add to Roster Mode needs BOTH: league_config.json (strategy) + draft_config.json (prediction)
- [x] **Missing file handling:** Error with helpful message telling user to run accuracy simulation first (or copy week1-5.json manually)

---

## API/Data Source Questions

- [x] **Actual points source:** `sim_data/{year}/weeks/week_XX/players.csv` (weekly), `players_actual.csv` (season)
- [x] **Historical data format:** CSV files per week with actual and projected points
- [x] **Bye week handling:** Skip - bye weeks are empty values in week_N_points columns (verified in sim_data CSVs)
- [x] **Data isolation for fair testing:** YES - Weekly CSVs are SNAPSHOTS! Verified: week_05/players.csv has different week_5-9 values than week_10/players.csv. Data isolation is built into the data structure.
- [x] **ROS evaluation point:** Week 1 only - pre-season predictions vs full season actuals
- [x] **Projection source for ROS:** Pre-season projections only (week_01 data)

---

## Output Files / Data Structures

### Accuracy Results Output

**File-level decisions:**
- [x] Output format: JSON files like win-rate (verified: ResultsManager uses JSON for all output)
- [x] Output location: Same folder structure as win-rate results (simulation/simulation_configs/)

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `config_id` | [x] | Same pattern as win-rate (parameter combo hash) |
| `week_range` | [x] | Same ranges: 1-5, 6-9, 10-13, 14-17 |
| `accuracy_metric` | [x] | MAE (Mean Absolute Error) - lower is better |
| `player_count` | [x] | Count of players evaluated |

**Questions:**
- [x] Should individual player accuracies be stored or just aggregates? Aggregates only

---

## Algorithm/Logic Questions

- [x] **Point normalization:** `ScoredPlayer.projected_points` already contains un-normalized value
- [x] **Season vs Weekly scoring:** Different flags (ADP/rating for ROS, performance/matchup for weekly)
- [x] **Calculated projection:** `(score / normalization_scale) * max_projection` - already in ScoredPlayer

---

## Architecture Questions

- [x] **Shared classes identification:** ConfigGenerator, PARAM_DEFINITIONS, data loading (shared); SimulatedLeague, Week, DraftHelperTeam (win-rate only)
- [x] **Folder structure:** Use shared/ subfolder (specs are correct; "root" in notes was ambiguous)
- [x] **__init__.py files:** Currently not used (sys.path.append pattern), but SHOULD add for cleaner imports
- [x] **Import path changes:** Keep sys.path.append pattern, just adjust paths for new folder structure
- [x] **Results comparison:** No - separate simulations with separate outputs
- [x] **Migration strategy:** All-at-once - single commit with folder restructure and import updates

---

## Runner Scripts Setup

- [x] **run_accuracy_simulation.py structure:** Mirror run_simulation.py pattern (--mode, --baseline, --output, --workers, --data, --test-values, --use-processes). Note: --sims NOT applicable (MAE is deterministic)
- [x] **run_accuracy_simulation_loop.sh structure:** Mirror run_simulation_loop.sh (trap signals, restart on kill/error, exit on success)
- [x] **Shared CLI arguments:** All args shared except --mode options and --sims (accuracy modes vs win-rate modes)
- [x] **Entry point pattern:** Independent scripts (matches existing pattern, no shared base)

---

## Results Storage

- [x] **Results folder location:** Same parent folder (simulation/simulation_configs/) - matches win-rate pattern
- [x] **Results folder naming:** `accuracy_optimal_TIMESTAMP/` (matches optimal_TIMESTAMP pattern)
- [x] **Output file format:** Same 5-JSON structure (draft_config.json + 4 week-range files for accuracy)
- [x] **Intermediate results:** Yes, `accuracy_intermediate_{idx}_{param}/` (matches win-rate pattern)
- [x] **Best config selection:** Lowest MAE wins (opposite of win-rate where highest wins)
- [x] **Metrics in output:** mae, player_count, config_id, timestamp (4 metrics - matches win-rate pattern)

---

## Error Handling Questions

- [x] **Zero actual points:** MAE handles zeros naturally (no division), but players with zero actual should likely be excluded (they didn't play)
- [x] **Missing data:** Skip that player-week only, include all weeks with valid data
- [x] **Negative projections:** No - projections are always positive (score normalized then multiplied by max_projection)

---

## Edge Cases

- [x] **Injured players:** Exclude - zero points due to injury is missing data, not prediction failure
- [x] **Players who didn't play:** Exclude from accuracy calculation (0 actual points = skip)
- [x] **Trades/releases:** Include as-is - measure player performance prediction regardless of team changes
- [x] **Minimum projection threshold:** No threshold - include all players regardless of projection level
- [x] **Minimum games played:** No minimum - include all players with any games played

---

## Testing & Validation

- [x] **Accuracy formula validation:** Unit tests with known inputs/outputs
- [x] **Restructure validation:** Run existing tests - they should catch issues
- [x] **Performance testing:** No specific requirements - just needs to complete reasonably
- [x] **Known scenario tests:** Yes - create test fixtures with known MAE values

---

## Scoring Mode Configuration

- [x] **Season-long scoring flags:** N/A - accuracy sim optimizes prediction params, not mode flags
- [x] **Weekly scoring flags:** N/A - accuracy sim optimizes prediction params, not mode flags
- [x] **Custom flag configuration:** No - use existing mode flags, optimize prediction params only
- [x] **Parameter scope:** 17 prediction params:
  - NORMALIZATION_MAX_SCALE
  - PLAYER_RATING_SCORING_WEIGHT
  - TEAM_QUALITY_SCORING_WEIGHT, TEAM_QUALITY_MIN_WEEKS
  - PERFORMANCE_SCORING_WEIGHT, PERFORMANCE_SCORING_STEPS, PERFORMANCE_MIN_WEEKS
  - MATCHUP_IMPACT_SCALE, MATCHUP_SCORING_WEIGHT, MATCHUP_MIN_WEEKS
  - TEMPERATURE_IMPACT_SCALE, TEMPERATURE_SCORING_WEIGHT
  - WIND_IMPACT_SCALE, WIND_SCORING_WEIGHT
  - LOCATION_HOME, LOCATION_AWAY, LOCATION_INTERNATIONAL
  - **SYNC REQUIREMENT:** SCHEDULE params (IMPACT_SCALE, WEIGHT, MIN_WEEKS) must mirror MATCHUP values - keep these 6 in sync

---

## Multi-Season Handling

- [x] **Season aggregation:** Yes, same approach as win-rate (aggregate across all 20XX folders in sim_data)
- [x] **Season weighting:** Equal weight - all seasons count the same
- [x] **Minimum seasons:** No minimum - use whatever seasons are available

---

## Parallelization & Performance

- [x] **Parallel execution:** Yes, same thread pool pattern as ParallelLeagueRunner (verified: uses ThreadPoolExecutor/ProcessPoolExecutor)
- [x] **Expected runtime:** FASTER than win-rate - no drafts/matches to simulate, just player scoring and MAE calculation
- [x] **Memory considerations:** No concerns - player data loaded same way as win-rate, already proven to work

---

## Operational Concerns

- [x] **Signal handling:** Yes, same pattern as win-rate (SIGINT/SIGTERM graceful shutdown, update configs before exit)
- [x] **Resume capability:** Yes, via intermediate folders (same pattern as win-rate)
- [x] **Backwards compatibility:** Current code uses sys.path.append (no __init__.py), restructure needs care
- [x] **Test updates:** Yes - update test imports to match new folder structure
- [x] **Deprecation warnings:** No - clean rename, old name just doesn't exist

---

## Integration & Workflow

- [x] **Copy to data/configs:** No auto-copy - manual only. Also disable auto-copy in win-rate simulation
- [x] **Comparison workflow:** No built-in comparison - user can manually compare JSON files
- [x] **Tie-breaking:** First one wins - keep first config found with that MAE

---

## Logging & Debugging

- [x] **Logging level:** Yes, same logging pattern as win-rate (uses LoggingManager, configurable levels)
- [x] **Per-player debug output:** Yes - use logging levels (DEBUG shows per-player, INFO shows aggregate)
- [x] **Progress display:** Yes, same progress tracker pattern (configs tested, current best, etc.)

---

## Relationship Between Modes

- [x] **Combined optimization:** No - they optimize different config files, keep them separate
- [x] **Shared results folder:** Yes - both in simulation/simulation_configs/ (accuracy_optimal_*, optimal_*)
- [x] **Config compatibility:** Yes - configs work in both modes (same JSON structure, just different optimal values)
- [x] **Workflow documentation:** Yes - add docs explaining when to run which simulation (Win-rate = strategy, Accuracy = prediction)
- [x] **Config file documentation:** No extra metadata - folder naming (accuracy_optimal_* vs optimal_*) indicates source

---

## League Helper Integration

- [x] **ConfigManager changes:** YES - ConfigManager currently only loads league_config.json + weekX-Y.json. Needs update to also load draft_config.json for Add to Roster Mode.
- [x] **Mode-specific config selection:** Hardcoded by mode - Add to Roster uses draft_config.json, others use weekX-Y.json
- [x] **Fallback behavior:** Error - no silent fallback, require draft_config.json to exist
- [x] **Config validation:** Yes - validate all required configs exist on startup, fail early with helpful message

---

## Scope Clarification

- [x] **Win Rate simulation changes:** YES - but minimal: just pass different PARAMETER_ORDER array to only test league_config.json params (no code changes to prevent other file modifications)
- [x] **Add to Roster Mode changes:** YES - part of this feature (update to load draft_config.json)
- [x] **Feature boundaries:** FULL SCOPE - includes: new accuracy sim, folder restructure, Win Rate changes, Add to Roster changes, ConfigManager updates, script renames

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player projected points | `ScoredPlayer.projected_points` from `score_player()` | Verified |
| Player actual points | `sim_data/{year}/weeks/week_XX/players.csv` | Verified |
| Config parameters | ConfigGenerator (fully reusable) | Verified |
| Week-specific configs | 5 JSON files (league_config + 4 week-range files) | Verified |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Actual points source | sim_data/{year}/weeks/week_XX/players.csv | 2025-12-13 |
| Un-normalization method | Use ScoredPlayer.projected_points (already calculated) | 2025-12-13 |
| Shared classes | ConfigGenerator, PARAM_DEFINITIONS fully reusable | 2025-12-13 |
| Season vs Weekly scoring | Different flags - see specs for details | 2025-12-13 |
| Accuracy metric | MAE (Mean Absolute Error) - single metric, lower is better | 2025-12-14 |
| draft_config.json creation | Copy of week1-5.json, in data/configs/ | 2025-12-14 |
| Add to Roster Mode config | Uses BOTH league_config.json (strategy) + draft_config.json (prediction) | 2025-12-14 |
| Win Rate sim scope | Only optimizes league_config.json (strategy params) | 2025-12-14 |
| Accuracy sim output | ROS→draft_config.json, Weekly→week-specific configs | 2025-12-14 |
| Config parameter split | league_config.json has strategy (DRAFT_ORDER, BYE, ADP), week configs have prediction (NORMALIZATION, PLAYER_RATING, MATCHUP, etc.) | 2025-12-14 |
| Week ranges | Same as win-rate: 1-5, 6-9, 10-13, 14-17 (WEEK_RANGES in ConfigPerformance.py) | 2025-12-14 |
| Bye week handling | Skip empty week_N_points values in CSVs | 2025-12-14 |
| Runner script CLI | Mirror run_simulation.py args pattern | 2025-12-14 |
| Shell loop pattern | Mirror run_simulation_loop.sh (trap, restart, exit) | 2025-12-14 |
| Results folder | Same parent (simulation/simulation_configs/), accuracy_optimal_TIMESTAMP/ naming | 2025-12-14 |
| Intermediate saves | Yes, accuracy_intermediate_{idx}_{param}/ pattern | 2025-12-14 |
| Best config selection | Lowest MAE wins | 2025-12-14 |
| Signal handling | Same as win-rate (SIGINT/SIGTERM graceful shutdown) | 2025-12-14 |
| Resume capability | Yes, via intermediate folders | 2025-12-14 |
| Season aggregation | Aggregate across all 20XX folders like win-rate | 2025-12-14 |
| Folder structure | Use shared/ subfolder (specs are correct) | 2025-12-14 |
| __init__.py | Not currently used, should add for cleaner imports | 2025-12-14 |
| Data isolation | Built into data structure - weekly CSVs are SNAPSHOTS at that week | 2025-12-14 |
| Output format | JSON files same as win-rate (ResultsManager pattern) | 2025-12-14 |
| Output location | simulation/simulation_configs/ (same as win-rate) | 2025-12-14 |
| Zero actual points | MAE handles naturally; exclude players who didn't play | 2025-12-14 |
| Negative projections | Not possible - always positive after normalization | 2025-12-14 |
| Parallel execution | Same ThreadPoolExecutor/ProcessPoolExecutor pattern | 2025-12-14 |
| Expected runtime | Faster than win-rate (no drafts/matches) | 2025-12-14 |
| Logging pattern | Same LoggingManager pattern as win-rate | 2025-12-14 |
| Progress display | Same pattern as win-rate | 2025-12-14 |
| ConfigManager changes | YES - needs update to load draft_config.json | 2025-12-14 |
| Parameter split verified | Confirmed: league_config has ADP_SCORING + strategy; week configs have prediction params | 2025-12-14 |
