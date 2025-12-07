# Simulation with Historical Data - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `simulation_with_historical_data_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Season discovery location:** Where in code to detect `20XX/` folders?
  - **RESOLVED:** SimulationManager - discover once at init, pass to runner
- [x] **Results aggregation method:** → **Option A: Total wins / Total games**
  - See Algorithm/Logic Questions section for details
  - **RESOLVED:** User selected Option A 2024-12-06
- [x] **Backwards compatibility:** → **No fallback - require historical data**
  - Fail loudly if no valid `20XX/` folders exist
  - Old flat structure (`sim_data/players.csv`) not supported
  - **RESOLVED:** User selected fail loudly 2024-12-06
- [x] **Deprecate unused simulation modes:**
  - `run_full_optimization()` → Mark as DEPRECATED (do not update)
  - `run_single_config_test()` → Mark as DEPRECATED (do not update)
  - **Only update `run_iterative_optimization()`** for historical data support
  - **RESOLVED:** User confirmed 2024-12-06
- [x] **Restore week 17 to simulation:**
  - Current: `run_season()` simulates weeks 1-16 (week 17 removed due to data corruption)
  - Change: Simulate weeks 1-17 (historical data fixes the corruption)
  - Files affected: `SimulatedLeague.run_season()`, schedule generation
  - **RESOLVED:** User confirmed 2024-12-06
- [x] **Auto-detect new seasons (no code changes required):**
  - `_discover_seasons()` uses glob pattern `20*/` to find all season folders
  - Adding `2025/` folder automatically includes it in simulation
  - No hardcoded year lists - fully dynamic discovery
  - Only validates folder structure, not specific years
  - **RESOLVED:** Already covered by design 2024-12-06

---

## Architecture Questions (Critical Design Decisions)

### Q1: Season Loop Location

- [x] **Where should the loop over seasons live?** → **Option A: SimulationManager**
  - Season discovery happens ONCE at init via `_discover_seasons()`
  - Season iteration added to `run_full_optimization()` and `run_iterative_optimization()`
  - Each season = separate call to ParallelLeagueRunner with season-specific data_folder
  - Fallback: If no `20XX/` folders found, use flat structure (backwards compatible)
  - **RESOLVED:** User selected Option A on 2024-12-06

### Q2: Week-Specific Data Loading

- [x] **How should SimulatedLeague load week-specific player data?** → **FULLY OPTIMIZED**
  - **Pre-load all 17 weeks** at SimulatedLeague init (`_preload_all_weeks()`)
  - **Share parsed data across all 10 teams** (no redundant parsing)
  - Add `set_player_data(dict)` method to PlayerManager
  - **Performance:** 17 CSV parses/sim (down from 340) = 20× improvement
  - Zero file copies, zero disk I/O during `run_season()`
  - **RESOLVED:** User selected fully optimized approach on 2024-12-06

### Q3: Draft Data Source

- [x] **What data to use for draft simulation?** → **`week_01/players.csv`**
  - Use `{YEAR}/weeks/week_01/players.csv` for draft (same as week 1 matchups)
  - Contains all required columns for draft decisions
  - `players_projected.csv` only used for starter helper/performance calculations
  - Draft calls `_load_week_data(1)` before draft logic
  - **RESOLVED:** User confirmed 2024-12-06

### Q4: ConfigManager Scope

- [x] **Does ConfigManager need to be instantiated per-season?** → **No changes needed**
  - ConfigManager loads TEST CONFIG from temp file (legacy mode)
  - Week-specific config loading (`configs/` subfolder) doesn't apply to simulation
  - `current_nfl_week` already updated per-week in existing code
  - Test config parameters stay constant across all weeks/seasons (correct behavior)
  - **RESOLVED:** Investigation confirmed no changes needed 2024-12-06

---

## Data File Mapping Questions

- [x] **Team data structure:** `team_data/{TEAM}.csv` (same in both structures) ✓
- [x] **Schedule file:** `season_schedule.csv` (same name, different location per year) ✓
- [x] **Game data:** `game_data.csv` (same name, different location per year) ✓
- [x] **Draft file:** → `{YEAR}/weeks/week_01/players.csv`
  - Contains all required columns for draft decisions
  - **RESOLVED:** See Q3 above
- [x] **Weekly scoring file:** → `{YEAR}/weeks/week_XX/players.csv`
  - **RESOLVED:** Confirmed during investigation

---

## Algorithm/Logic Questions

- [x] **Win rate calculation across seasons:** → **Option A: Total wins / Total games**
  - Formula: `(W₁+W₂+W₃+W₄) / (17 × num_seasons)`
  - Simple to implement and understand
  - With equal games per season, equivalent to average per-season
  - **RESOLVED:** User selected Option A 2024-12-06
- [x] **Tie-breaking for configs with same win rate:** → **Total points scored**
  - Higher total points = better ranking
  - Already tracked in simulation results
  - **RESOLVED:** User selected Option 1 2024-12-06

---

## Error Handling Questions

- [x] **Missing season folder structure:** → **Fail loudly**
  - Raise error if `20XX/` folder exists but missing required structure (`weeks/`, `season_schedule.csv`, etc.)
  - Ensures data integrity - don't silently skip corrupted data
  - **RESOLVED:** User selected fail loudly 2024-12-06
- [x] **Missing week folder (e.g., week_15 missing):** → **Fail loudly**
  - Raise error if any week 1-17 folder is missing
  - Ensures consistent 17-game seasons across all years
  - **RESOLVED:** User selected fail loudly 2024-12-06
- [x] **Missing required file in week folder:** → **Fail loudly**
  - Raise error if `players.csv` missing from any week folder
  - **RESOLVED:** User selected fail loudly 2024-12-06
- [x] **No historical seasons found:** → **Fail loudly**
  - Raise error if no valid `20XX/` folders exist
  - No fallback to flat structure - require historical data
  - **RESOLVED:** User selected fail loudly 2024-12-06

---

## Edge Cases

- [x] **No historical seasons found:** → **Fail loudly** (covered in Error Handling)
- [x] **Single season available:** → **Allow**
  - Run simulation with just one year if only one exists
  - Still validates config across 17 games
  - **RESOLVED:** User confirmed 2024-12-06
- [x] **Player roster changes between weeks:** → **No special handling needed**
  - Each week loads fresh data from that week's CSV
  - If player doesn't exist in week N, they're simply not available
  - Drafted players who disappear are treated as benched/injured
  - **RESOLVED:** User confirmed analysis 2024-12-06
- [x] **Different number of players per season:** → **No special handling needed**
  - Each season's player pool is independent
  - Draft uses whatever players exist in week_01/players.csv
  - **RESOLVED:** Follows from roster changes analysis 2024-12-06

---

## Validation Requirements

### Season Folder Validation

| Check | Required? | Notes |
|-------|-----------|-------|
| `weeks/` folder exists | [x] | Contains weekly snapshots |
| `week_01/` folder exists | [x] | Required for draft |
| `week_01/players.csv` exists | [x] | Draft data |
| All 17 weeks exist (week_01-week_17) | [x] | Required - fail loudly if missing |
| `season_schedule.csv` exists | [x] | Bye weeks |
| `team_data/` folder exists | [x] | Team rankings |

### Weekly Data Validation

| Check | Required? | Notes |
|-------|-----------|-------|
| `players.csv` exists | [x] | Smart values for scoring |
| `players_projected.csv` exists | [ ] | May not be needed after week 1 |

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Season folders | `sim_data/20*/` glob | ✓ Confirmed (2021-2024 exist) |
| Weekly player data | `{YEAR}/weeks/week_XX/players.csv` | ✓ Confirmed |
| Weekly projections | `{YEAR}/weeks/week_XX/players_projected.csv` | ✓ Confirmed |
| Team data | `{YEAR}/team_data/{TEAM}.csv` | ✓ Confirmed |
| Schedule/bye weeks | `{YEAR}/season_schedule.csv` | ✓ Confirmed |
| Game data (weather) | `{YEAR}/game_data.csv` | ✓ Confirmed |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Historical data structure | Confirmed 4 seasons (2021-2024) with weeks/week_XX structure | Investigation Phase |
| Data file locations | All files confirmed in expected locations | Investigation Phase |
| **Q1: Season Loop Location** | **Option A: SimulationManager** - discover once at init, iterate per config | 2024-12-06 |
| **Scope: Deprecate modes** | Only update `run_iterative_optimization()`, deprecate full/single modes | 2024-12-06 |
| **Restore week 17** | Change from 16 weeks to 17 weeks (historical data fixes corruption) | 2024-12-06 |
| **Q2: Week-Specific Loading** | **Fully optimized** - pre-load + shared data (20× fewer disk reads) | 2024-12-06 |
| **Optimization: Parallel seasons** | Run all 4 seasons in parallel per config (4× speedup potential) | 2024-12-06 |
| **Optimization: Shared week data** | Parse CSV once per week, share across all 10 teams | 2024-12-06 |
| **Q3: Draft Data Source** | Use `week_01/players.csv` (contains all required columns) | 2024-12-06 |
| **Q4: ConfigManager Scope** | No changes needed - loads test config, legacy mode, week updated per-week | 2024-12-06 |
| **Win rate aggregation** | Option A: Total wins / Total games across all seasons | 2024-12-06 |
| **Auto-detect new seasons** | Glob `20*/` pattern - no hardcoded years, fully dynamic | 2024-12-06 |
| **Tie-breaking** | Total points scored (higher = better) | 2024-12-06 |
| **Error handling** | Fail loudly for all missing data scenarios (no silent skips) | 2024-12-06 |
| **Single season** | Allow running with just one year | 2024-12-06 |
| **Player roster changes** | No special handling - use each week's CSV as-is | 2024-12-06 |
