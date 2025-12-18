# Accuracy Simulation

## Objective

Create a new simulation mode that evaluates the **accuracy** of scoring algorithm configurations by comparing calculated projected points to actual player performance. This complements the existing win-rate simulation by providing a different optimization target - prediction accuracy rather than competitive success.

---

## Critical Context: Simulation & Config File Relationships

### The Two Simulation Purposes

| Simulation | Purpose | Optimizes | Represents |
|------------|---------|-----------|------------|
| **Win Rate** | Find best draft *strategy* | `league_config.json` | How to pick players during draft |
| **Accuracy** | Find best player *prediction* | `draft_config.json` + weekly configs | How accurately we predict player performance |

**Key insight:** Win Rate = strategy, Accuracy = prediction ability

### Config File Architecture

```
data/configs/
├── league_config.json    # Draft STRATEGY (optimized by Win Rate sim)
├── draft_config.json     # Draft PREDICTION (optimized by Accuracy sim - ROS mode)
├── week1-5.json          # Weekly prediction (optimized by Accuracy sim - weekly mode)
├── week6-9.json          # Weekly prediction (optimized by Accuracy sim - weekly mode)
├── week10-13.json        # Weekly prediction (optimized by Accuracy sim - weekly mode)
└── week14-17.json        # Weekly prediction (optimized by Accuracy sim - weekly mode)
```

### How Each Config is Used

| Config | Used By | When | Optimized By |
|--------|---------|------|--------------|
| `league_config.json` | Win Rate Simulation | During simulated drafts | Win Rate Simulation |
| `draft_config.json` | Add to Roster Mode | During actual draft | Accuracy Simulation (ROS) |
| `week1-5.json` | Starter Helper, Trade Simulator | Weeks 1-5 of season | Accuracy Simulation (weekly) |
| `week6-9.json` | Starter Helper, Trade Simulator | Weeks 6-9 of season | Accuracy Simulation (weekly) |
| `week10-13.json` | Starter Helper, Trade Simulator | Weeks 10-13 of season | Accuracy Simulation (weekly) |
| `week14-17.json` | Starter Helper, Trade Simulator | Weeks 14-17 of season | Accuracy Simulation (weekly) |

### Accuracy Simulation Two-Mode Output

1. **ROS (Rest of Season) Accuracy** → Optimizes `draft_config.json`
   - Evaluates season-long projection accuracy
   - Used for Add to Roster Mode (draft decisions)

2. **Weekly Accuracy** → Optimizes `week1-5.json`, `week6-9.json`, etc.
   - Evaluates per-week projection accuracy
   - Used for Starter Helper and Trade Simulator (in-season decisions)

### New File: draft_config.json

- **Initial creation:** Copy of `week1-5.json`
- **Purpose:** Store optimal parameters for predicting player performance during draft
- **Used by:** Add to Roster Mode (alongside league_config.json)
- **Optimized by:** Accuracy Simulation ROS mode

### Config Parameter Split (RESOLVED via investigation)

**league_config.json** (Strategy - optimized by Win Rate):
- CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT
- SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT
- INJURY_PENALTIES
- DRAFT_ORDER_BONUSES (PRIMARY, SECONDARY)
- DRAFT_ORDER (position priority per round)
- MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS
- ADP_SCORING

**draft_config.json / week-specific configs** (Prediction - optimized by Accuracy):
- NORMALIZATION_MAX_SCALE
- PLAYER_RATING_SCORING (WEIGHT param)
- TEAM_QUALITY_SCORING (WEIGHT, MIN_WEEKS params)
- PERFORMANCE_SCORING (WEIGHT, STEPS, MIN_WEEKS params)
- MATCHUP_SCORING (IMPACT_SCALE, WEIGHT, MIN_WEEKS params)
- SCHEDULE_SCORING (synced with MATCHUP - not independently optimized)
- TEMPERATURE_SCORING (IMPACT_SCALE, WEIGHT params)
- WIND_SCORING (IMPACT_SCALE, WEIGHT params)
- LOCATION_MODIFIERS (HOME, AWAY, INTERNATIONAL params)

**Key insight:** These are COMPLEMENTARY, not duplicates. Add to Roster Mode needs BOTH files.

**Note:** See "Parameters to Optimize" section below for the specific 17 parameters that accuracy simulation will iterate through.

---

## High-Level Requirements

### 1. Simulation Modes

**Season-Long Accuracy Mode:**
- Loop through every player
- Calculate season-long projected points using Add to Roster Mode scoring
- Compare to actual total points scored by the player
- Aggregate accuracy metrics across all players

**Weekly Accuracy Mode:**
- Loop through every week in the season (weeks 1-17)
- For each week, calculate projected points for each player
- Compare to actual points scored that week
- Aggregate accuracy metrics across all weeks and players

### 2. Folder Restructuring

Current structure:
```
simulation/
├── SimulationManager.py
├── ParallelLeagueRunner.py
├── ConfigGenerator.py
├── ResultsManager.py
├── ConfigPerformance.py
├── SimulatedLeague.py
├── DraftHelperTeam.py
├── SimulatedOpponent.py
├── Week.py
└── sim_data/
```

Proposed structure:
```
simulation/
├── shared/                    # Shared between both modes
│   ├── ConfigGenerator.py
│   ├── ResultsManager.py      # May need modification
│   └── ConfigPerformance.py   # May need modification
├── win_rate/                  # Win-rate simulation specific
│   ├── SimulationManager.py
│   ├── ParallelLeagueRunner.py
│   ├── SimulatedLeague.py
│   ├── DraftHelperTeam.py
│   ├── SimulatedOpponent.py
│   └── Week.py
├── accuracy/                  # Accuracy simulation specific
│   ├── AccuracySimulationManager.py
│   └── (other accuracy-specific classes)
└── sim_data/
```

### 3. Runner Scripts

**Rename existing:**
- `run_simulation.py` → `run_win_rate_simulation.py`
- `run_simulation_loop.sh` → `run_win_rate_simulation_loop.sh`

**Create new:**
- `run_accuracy_simulation.py`
- `run_accuracy_simulation_loop.sh`

### 4. Output/Deliverables

- Best config identification per week range (same as win-rate)
- Accuracy metrics output (format TBD)
- Association with week-specific config files

---

## All Questions Resolved

All planning questions have been resolved. See detailed specifications below.

---

## Resolved Implementation Details

### Feature Scope

**FULL SCOPE - This feature includes:**
- New accuracy simulation mode
- Folder restructure (shared/, win_rate/, accuracy/)
- Win Rate simulation changes (pass different PARAMETER_ORDER to only test league_config.json params)
- Add to Roster Mode changes (load draft_config.json)
- ConfigManager updates (support draft_config.json)
- Script renames (run_simulation.py → run_win_rate_simulation.py)
- Disable auto-copy to data/configs/ in both simulations

---

### Accuracy Metric

**Decision:** MAE (Mean Absolute Error) as the single metric
- **Formula:** `MAE = mean(|actual - projected|)` across all players
- **Comparison logic:** Lower MAE is better (opposite of win-rate where higher is better)
- **Tie-breaking:** First config found with that MAE wins

**Implementation:**
```python
# For each player:
error = abs(actual_points - projected_points)

# Aggregate across all players:
mae = sum(errors) / len(errors)

# Best config = lowest MAE
```

---

### Player Filtering Rules

| Rule | Decision |
|------|----------|
| Players with 0 actual points | **Exclude** - didn't play, not a prediction failure |
| Minimum projection threshold | **None** - include all players regardless of projection |
| Minimum games played | **None** - include all players with any games |
| Traded/released players | **Include as-is** - measure player performance regardless of team |
| Missing data (incomplete weeks) | **Skip that player-week only** - include all weeks with valid data |
| Player weighting | **Equal weight** - every player's error counts the same |
| Position-specific accuracy | **Aggregate only** - single MAE across all players |
| Baseline comparison | **No** - just optimize MAE directly |

---

### ROS (Rest of Season) Mode

- **Evaluation timing:** Week 1 only - pre-season predictions vs actual season totals
- **Projection source:** Pre-season projections only (week_01 data)
- **Purpose:** Optimize `draft_config.json` for Add to Roster Mode (draft decisions)

---

### Weekly Mode

- **Week ranges:** Same as win-rate: 1-5, 6-9, 10-13, 14-17
- **Bye week handling:** Skip empty week_N_points values in CSVs
- **Data isolation:** Built into data structure - weekly CSVs are SNAPSHOTS at that week
- **Purpose:** Optimize `week1-5.json`, `week6-9.json`, etc. for Starter Helper/Trade Simulator

---

### Run Order & CLI

- **--mode options:** `ros`, `weekly`, `both`
- **Default:** `both` (runs ROS first, then Weekly)
- **CLI pattern:** Mirror run_simulation.py structure (--mode, --baseline, --output, --workers, --data, --test-values, --use-processes)
- **Note:** `--sims` is NOT applicable to accuracy simulation - MAE calculation is deterministic (no randomness like draft simulations)
- **Shell loop:** Mirror run_simulation_loop.sh (trap signals, restart on kill/error, exit on success)

---

### Parameters to Optimize (17 total)

**Accuracy simulation optimizes these prediction params:**
- NORMALIZATION_MAX_SCALE
- PLAYER_RATING_SCORING_WEIGHT
- TEAM_QUALITY_SCORING_WEIGHT, TEAM_QUALITY_MIN_WEEKS
- PERFORMANCE_SCORING_WEIGHT, PERFORMANCE_SCORING_STEPS, PERFORMANCE_MIN_WEEKS
- MATCHUP_IMPACT_SCALE, MATCHUP_SCORING_WEIGHT, MATCHUP_MIN_WEEKS
- TEMPERATURE_IMPACT_SCALE, TEMPERATURE_SCORING_WEIGHT
- WIND_IMPACT_SCALE, WIND_SCORING_WEIGHT
- LOCATION_HOME, LOCATION_AWAY, LOCATION_INTERNATIONAL

**SYNC REQUIREMENT:** SCHEDULE params (IMPACT_SCALE, WEIGHT, MIN_WEEKS) must mirror MATCHUP values - keep these 6 in sync when creating/updating JSON files.

---

### Results Storage

| Setting | Value |
|---------|-------|
| Results folder location | `simulation/simulation_configs/` (same as win-rate) |
| Optimal folder naming | `accuracy_optimal_TIMESTAMP/` |
| Intermediate folder naming | `accuracy_intermediate_{idx}_{param}/` |
| Output file format | Same 5-JSON structure (draft_config.json + 4 week-range files) |
| Auto-copy to data/configs/ | **No** - manual copy only (also disable in win-rate sim) |

**Output metrics in JSON performance_metrics:**
- `mae` - Mean Absolute Error (primary metric)
- `player_count` - Number of players evaluated
- `config_id` - Parameter combo hash
- `timestamp` - When config was tested

---

### Un-Normalization

**Decision:** Use existing `ScoredPlayer.projected_points` field
**Source:** `league_helper/util/player_scoring.py:455-466`

```python
# Already implemented in score_player():
normalization_scale = self.config.normalization_max_scale
chosen_max = self.max_weekly_projection if use_weekly_projection else self.max_projection
calculated_projection = (player_score / normalization_scale) * chosen_max
return ScoredPlayer(p, player_score, reasons, projected_points=calculated_projection)

# Usage for accuracy comparison:
scored_player = player_manager.score_player(player)
projected = scored_player.projected_points  # Un-normalized, comparable to actual
actual = player.actual_points  # From historical data
error = abs(actual - projected)
```

---

### Data Sources

**Data Structure:**
```
sim_data/
├── players_projected.csv       # Season-long projections (root level)
├── players_actual.csv          # Season-long actual results (root level)
└── {year}/                     # Per-year folders (2021, 2022, 2024, etc.)
    └── weeks/
        └── week_XX/
            ├── players.csv           # SNAPSHOT - contains week_1_points through week_17_points columns
            └── players_projected.csv # Projections for that week
```

**Critical finding:** Weekly CSVs are SNAPSHOTS at that point in time (different values in week_05 vs week_10 for same player's past weeks). The weekly `players.csv` files contain all 17 weeks of data as columns (week_1_points through week_17_points), with actual results for past weeks and projections/empty values for future weeks.

---

### Folder Restructuring

**Current → New structure:**
```
simulation/
├── shared/                    # Shared between both modes
│   ├── ConfigGenerator.py
│   ├── ResultsManager.py
│   └── ConfigPerformance.py
├── win_rate/                  # Win-rate simulation specific
│   ├── SimulationManager.py
│   ├── ParallelLeagueRunner.py
│   ├── SimulatedLeague.py
│   ├── DraftHelperTeam.py
│   ├── SimulatedOpponent.py
│   └── Week.py
├── accuracy/                  # Accuracy simulation specific
│   ├── AccuracySimulationManager.py
│   ├── AccuracyResultsManager.py
│   ├── AccuracyConfigPerformance.py
│   └── PlayerAccuracyCalculator.py
└── sim_data/
```

**Migration strategy:** All-at-once - single commit with folder restructure and import updates
**Import pattern:** Keep sys.path.append pattern, just adjust paths

---

### League Helper Integration

| Setting | Decision |
|---------|----------|
| ConfigManager changes | YES - add support for loading draft_config.json |
| Mode-specific config selection | Hardcoded: Add to Roster uses draft_config.json, others use weekX-Y.json |
| Missing draft_config.json | Error with helpful message (no silent fallback) |
| Config validation | Yes - validate all required configs exist on startup |

---

### Multi-Season Handling

- **Season aggregation:** Same as win-rate (aggregate across all 20XX folders in sim_data)
- **Season weighting:** Equal weight - all seasons count the same
- **Minimum seasons:** None - use whatever seasons are available

---

### Operational Details

| Setting | Decision |
|---------|----------|
| Signal handling | Same as win-rate (SIGINT/SIGTERM graceful shutdown) |
| Resume capability | Yes, via intermediate folders |
| Parallel execution | Same ThreadPoolExecutor/ProcessPoolExecutor pattern |
| Expected runtime | Faster than win-rate (no drafts/matches to simulate) |
| Logging pattern | Same LoggingManager pattern, DEBUG shows per-player errors |
| Progress display | Same pattern as win-rate (configs tested, current best, etc.) |

---

### Testing Strategy

- **Accuracy formula validation:** Unit tests with known inputs/outputs
- **Restructure validation:** Run existing tests - they should catch issues
- **Performance testing:** No specific requirements
- **Known scenario tests:** Create test fixtures with known MAE values
- **Test updates:** Update test imports to match new folder structure

---

### Relationship Between Modes

- **Combined optimization:** No - they optimize different config files
- **Shared results folder:** Yes - both in simulation/simulation_configs/
- **Config compatibility:** Yes - same JSON structure, just different optimal values
- **Workflow documentation:** Yes - add docs explaining when to run which simulation
- **Config file documentation:** No extra metadata - folder naming indicates source

---

### Runner Scripts

**Rename existing:**
- `run_simulation.py` → `run_win_rate_simulation.py` (no deprecation wrapper)
- `run_simulation_loop.sh` → `run_win_rate_simulation_loop.sh`

**Create new:**
- `run_accuracy_simulation.py`
- `run_accuracy_simulation_loop.sh`

---

## Status: READY FOR IMPLEMENTATION
