# Technical Analysis: players_projected.csv Creation and Modification Flow

## 1. File Purpose & Intent

**Purpose**: `players_projected.csv` is designed to store week-by-week fantasy football projections for all NFL players. It serves as a performance tracking file used by the league helper system to compare actual scoring against projected scoring for analysis and recommendations.

**Intended Content**:
- Column structure: `id, name, week_1_points, week_2_points, ..., week_17_points`
- Each `week_X_points` column should contain **projected fantasy points** for that specific week
- Historical weeks (weeks that have already been played) should be preserved and not updated
- Current and future weeks should be updated with fresh projection data

**Documented Requirement** (from `player_data_fetcher_main.py`, lines 349-352):
```
Per requirement #6 from update_consistency.txt: "Update the player_data_fetcher such that
every time the player_data_fetcher is run, the info for the current week and everything
upcoming is updated in that players_projected.csv file."
```

---

## 2. File Locations

**Primary File**:
- `/data/players_projected.csv` - The main active file used by league helper

**Historical Archives** (weekly snapshots saved for analysis):
- `/data/historical_data/{SEASON}/{WEEK}/players_projected.csv` (e.g., `/data/historical_data/2025/12/players_projected.csv`)
- These are created by automatic historical data backup feature (when `ENABLE_HISTORICAL_DATA_SAVE=True`)

**Simulation File**:
- `/simulation/sim_data/players_projected.csv` - Copy for simulation system

---

## 3. Creation Flow: Initial Creation

### Entry Point
**File**: `/run_player_fetcher.py` (lines 18-39)
- Simple wrapper that changes to `player-data-fetcher/` directory and runs the main script
- Ensures relative paths in the fetcher work correctly

### Main Script Execution
**File**: `player-data-fetcher/player_data_fetcher_main.py`

**Step 1: Initialize Collector** (`NFLProjectionsCollector.__init__`, lines 113-142)
- Creates instance with configuration settings
- Loads bye weeks data
- Initializes data exporter

**Step 2: Collect Data** (`main()` → `collect_all_projections()`, lines 208-283)
- Creates `ESPNClient` with settings
- Calls `ESPNClient.get_season_projections()` to fetch player data from ESPN API
- Each player receives week-by-week projections (weeks 1-17)

**Step 3: Export Data** (`main()` → `export_data()`, lines 293-370)
```python
# Line 354-357 in player_data_fetcher_main.py
projected_file = await self.exporter.export_projected_points_data(
    data,
    self.settings.current_nfl_week  # Only update this week and beyond
)
```

**Step 4: Create File** (`DataExporter.export_projected_points_data()`, lines 521-632)

If file doesn't exist (first run):
1. Creates new `players_projected.csv` with just `id, name` columns (line 600-608)
2. Adds all 17 week columns with fresh projection data for new players
3. Writes to `/data/players_projected.csv`

If file already exists (subsequent runs):
1. Loads existing CSV (line 555)
2. Updates only current week and future weeks (lines 567-587)
3. Preserves historical weeks (1 through current_week-1)
4. Adds any completely new players not in existing file (lines 594-615)

---

## 4. Data Source & Processing Flow

### ESPN API Data Collection

**File**: `player-data-fetcher/espn_client.py`

#### Phase 1: Fetch Raw Player Data
- `ESPNClient.get_season_projections()` (lines 696-726)
  - Calls ESPN Fantasy API endpoint
  - Returns raw ESPN player data objects
  - Each contains player ID, name, team, position, injury status, ADP

#### Phase 2: Extract Week-by-Week Projections
- `ESPNClient._parse_espn_data()` (lines 1602-2138)
  - Processes each player from ESPN response
  - For each player: calls `_populate_weekly_projections()`

- `ESPNClient._populate_weekly_projections()` (lines 533-571)
  - Gets all weekly data for player in single API call via `_get_all_weeks_data()`
  - Calls `_extract_raw_espn_week_points()` for each week 1-17
  - Stores result in `ESPNPlayerData.week_X_points` fields

#### Phase 3: Extract Individual Week Points
**Critical Function**: `ESPNClient._extract_raw_espn_week_points()` (lines 573-690)

This is where the bug originates. ESPN returns complex data structure:

```
For each week, ESPN provides multiple stat entries:
[
  {"scoringPeriodId": 7, "statSourceId": 0, "appliedTotal": 18.2, ...},  # ACTUAL RESULTS
  {"scoringPeriodId": 7, "statSourceId": 1, "projectedTotal": 15.8, ...}  # PROJECTIONS
]
```

**Data Source Priority (Lines 588-593 - Documented Intent)**:
1. `statSourceId=0` + `appliedTotal` - Actual game results (HIGHEST PRIORITY)
2. `statSourceId=0` + `projectedTotal` - Official ESPN projection
3. `statSourceId=1` + `appliedTotal` - Projected actuals for future weeks
4. `statSourceId=1` + `projectedTotal` - Projected estimate (LOWEST PRIORITY)

**Actual Implementation (Lines 614-681)** - THE BUG:
```python
# Lines 636-653: Extract points (both appliedTotal and projectedTotal)
if 'appliedTotal' in stat and stat['appliedTotal'] is not None:
    points = float(stat['appliedTotal'])  # Gets ACTUAL scores
elif 'projectedTotal' in stat and stat['projectedTotal'] is not None:
    points = float(stat['projectedTotal'])  # Gets projected

# Lines 657-664: Separate by source
if stat_source_id == 0:
    actual_entries.append(points)  # Both actual AND projections from statSourceId=0
elif stat_source_id == 1:
    projected_entries.append(points)  # Both projections and actuals from statSourceId=1

# Lines 668-673: SELECT ACTUAL RESULTS (BUG HERE)
if actual_entries:
    valid_actuals = [p for p in actual_entries if position == 'DST' or p > 0]
    if valid_actuals:
        return valid_actuals[0]  # RETURNS ACTUAL SCORES, NOT PROJECTIONS!
```

**The Bug**:
- For past weeks that have been played, `statSourceId=0` contains both `appliedTotal` (actual score) and `projectedTotal` (what was projected)
- The code prefers `appliedTotal` (line 636) when available
- This means **actual game results are stored in the "projected" file** for completed weeks
- The file name and purpose say "projections" but it's storing actual scores

---

## 5. Alternative Data Path: FantasyPointsExtractor

**File**: `player-data-fetcher/fantasy_points_calculator.py`

This class has configurable logic but is **NOT used** for weekly projections in the fetcher.

**FantasyPointsConfig** (lines 32-40):
- `prefer_actual_over_projected=True` - Always prefer `appliedTotal` over `projectedTotal`
- But this class is **only instantiated for season-level calculations**, not weekly

The weekly extraction uses `_extract_raw_espn_week_points()` directly (line 557 in espn_client.py), not the extractor.

---

## 6. Key Functions Involved

### ESPNClient Methods

| Function | File | Lines | Purpose |
|----------|------|-------|---------|
| `get_season_projections()` | espn_client.py | 696-726 | Fetch all player data from ESPN API |
| `_parse_espn_data()` | espn_client.py | 1602-2138 | Convert ESPN response to ESPNPlayerData objects |
| `_populate_weekly_projections()` | espn_client.py | 533-571 | Populate week_1_points through week_17_points |
| `_get_all_weeks_data()` | espn_client.py | 436-506 | Fetch all weekly data for one player in single API call |
| `_extract_raw_espn_week_points()` | espn_client.py | 573-690 | **THE BUG**: Extract points for specific week |

### DataExporter Methods

| Function | File | Lines | Purpose |
|----------|------|-------|---------|
| `export_all_formats_with_teams()` | player_data_exporter.py | 634-676 | Orchestrate all export operations |
| `export_projected_points_data()` | player_data_exporter.py | 521-632 | **Update players_projected.csv** |
| `_prepare_export_dataframe()` | player_data_exporter.py | 189-207 | Prepare DataFrame for export |
| `get_fantasy_players()` | player_data_exporter.py | 367-378 | Convert ESPNPlayerData to FantasyPlayer objects |

### Supporting Classes

| Class | File | Purpose |
|-------|------|---------|
| `ESPNPlayerData` | player_data_models.py | Data model with week_1_points through week_17_points fields |
| `ProjectionData` | player_data_models.py | Container with season metadata and player list |
| `Settings` | player_data_fetcher_main.py | Configuration from environment/config.py |

---

## 7. Data Flow Diagram

```
ESPN API
    ↓
ESPNClient.get_season_projections()
    ↓
ESPNClient._parse_espn_data()
    ├─→ For each player:
    │   └─→ _populate_weekly_projections()
    │       ├─→ _get_all_weeks_data() [single optimized API call]
    │       └─→ For weeks 1-17:
    │           └─→ _extract_raw_espn_week_points() [THE BUG LOCATION]
    │               ├─ Extracts both appliedTotal and projectedTotal
    │               ├─ Prioritizes appliedTotal (actual scores)
    │               └─ Returns actual game results for past weeks
    └─→ Creates ProjectionData with all players
        └─→ Each player has week_1_points through week_17_points populated
            with ACTUAL SCORES (not projections) for completed weeks

DataExporter.export_data()
    ├─→ export_to_data() [exports to data/players.csv - full player data]
    ├─→ export_teams_to_data() [exports team quality rankings]
    └─→ export_projected_points_data() [THE FILE CREATION]
        ├─ If file doesn't exist: CREATE with fresh weekly data
        ├─ If file exists: UPDATE only current week + future
        └─ RESULT: players_projected.csv contains actual scores for past weeks

save_to_historical_data()
    └─→ Copies players_projected.csv to data/historical_data/{SEASON}/{WEEK}/
```

---

## 8. The Bug: Exact Location & Root Cause

### Bug Location
**File**: `player-data-fetcher/espn_client.py`
**Method**: `_extract_raw_espn_week_points()`
**Lines**: 636-673

### Root Cause

ESPN API returns data structure with week-specific `statSourceId` values:
- `statSourceId=0` (official ESPN stats): Contains BOTH actual scores and projections
- `statSourceId=1` (projected): Contains future week projections

**Current Implementation Problem** (Lines 614-673):

```python
# STEP 1: Extract points from both appliedTotal and projectedTotal
if 'appliedTotal' in stat:           # Line 636
    points = float(stat['appliedTotal'])  # Gets ACTUAL game score
elif 'projectedTotal' in stat:       # Line 645
    points = float(stat['projectedTotal']) # Gets projection

# STEP 2: Categorize by statSourceId (not by point type!)
if stat_source_id == 0:              # Line 657
    actual_entries.append(points)    # Line 660 - BOTH actual AND projected go here!
elif stat_source_id == 1:            # Line 661
    projected_entries.append(points) # Line 664

# STEP 3: Return actual (which are game scores, not projections!)
if actual_entries:                   # Line 668
    return actual_entries[0]         # Line 673 - RETURNS ACTUAL SCORES!
```

### Why This Happens

For a completed week (Week 7):
```
ESPN returns:
[
  {"scoringPeriodId": 7, "statSourceId": 0, "appliedTotal": 18.2},  # Actual result
  {"scoringPeriodId": 7, "statSourceId": 0, "projectedTotal": 15.8} # Projection made before game
  {"scoringPeriodId": 7, "statSourceId": 1, "projectedTotal": 16.1}  # Other projection model
]
```

Code behavior:
1. Processes first entry: `appliedTotal=18.2`, `statSourceId=0` → adds 18.2 to `actual_entries`
2. Returns 18.2 from `actual_entries` (actual game result)
3. Never checks if these are really "projections" vs "actuals"

**Confusion of terminology**:
- `statSourceId=0` = "official stats" (includes both actual results and official projections)
- `statSourceId=1` = "alternate models" (for future weeks)
- **NOT**: 0 = actual, 1 = projected

---

## 9. Configuration Settings Affecting Behavior

**File**: `player-data-fetcher/config.py`

| Setting | Value | Effect |
|---------|-------|--------|
| `CURRENT_NFL_WEEK` | 12 | Controls which weeks are "past" vs "future" |
| `NFL_SEASON` | 2025 | Current season year |
| `ENABLE_HISTORICAL_DATA_SAVE` | True | Auto-save weekly snapshots |
| `SKIP_DRAFTED_PLAYER_UPDATES` | False | Skip API calls for drafted players |
| `USE_SCORE_THRESHOLD` | False | Skip API for low-scoring players |
| `PRESERVE_DRAFTED_VALUES` | False | Keep draft status between updates |
| `LOAD_DRAFTED_DATA_FROM_FILE` | True | Load drafted state from external file |

None of these settings can prevent the bug - they only control optimization behavior and data preservation.

---

## 10. Update & Preservation Behavior

**When fetcher runs** (`export_projected_points_data()`, lines 567-589):

```python
weeks_to_update = [f'week_{week}_points' for week in range(current_nfl_week, 18)]
# If CURRENT_NFL_WEEK=12, this becomes: [week_12_points, week_13_points, ..., week_17_points]

# Update existing players
for week_col in weeks_to_update:
    week_num = int(week_col.split('_')[1])
    new_value = getattr(new_player, week_col, 0.0)
    existing_df.at[idx, week_col] = new_value
```

**What this means**:
- Historical weeks (1-11) are NEVER touched - they remain as actual scores
- Current and future weeks (12-17) get updated with new data
- But new data is ALSO actual scores for completed weeks

**Result**: Week-by-week data gets progressively "contaminated" with actual scores as weeks complete

---

## 11. Summary Table: Data Type by Week

As of Week 12 (CURRENT_NFL_WEEK=12):

| Week | What Should Be There | What Actually Gets Stored |
|------|---------------------|--------------------------|
| 1-11 | Projections made pre-season | **ACTUAL GAME RESULTS** |
| 12 | Current week projections | **ACTUAL GAME RESULTS** (if game played) |
| 13-17 | Future projections | Future projections (correct) |

---

## 12. Actual vs Intended Behavior

### Intended Behavior
```
players_projected.csv should track what was PREDICTED for each week:
Week 1 projections (made before season started)
Week 2 projections (made before week 1 ended)
Week 3 projections (made before week 2 ended)
...
Week 12 projections (made before week 11 ended)
Week 13-17 projections (updated each run)
```

### Actual Behavior
```
players_projected.csv contains:
Week 1-11: ACTUAL game results (not projections)
Week 12: ACTUAL game result (if game played)
Week 13-17: Future projections (correct, until they're played)
```

---

## 13. Why This Matters

This bug affects:

1. **Performance Tracking**: League helper reads this file to compare projected vs actual, but it's comparing actual vs actual for past weeks (no variation to analyze)

2. **Projection Quality Assessment**: Can't determine if projections were good or bad because actual results are stored instead

3. **Seasonal Analysis**: Historical snapshots (in `data/historical_data/`) contain the same contaminated data

4. **ADP/Ranking Evaluation**: Can't assess if early-week projections were accurate

---

## 14. Corrections From Re-Verification (November 24, 2025)

### Original Analysis Corrections

| Original Statement | Correction |
|-------------------|------------|
| File contains actual scores for all past weeks | **PARTIALLY CORRECT** - Week 1 matches actual scores, but Weeks 2+ appear to contain projection data |
| The `projectedTotal` field exists in ESPN API | **INCORRECT** - This field does not exist; code comments are outdated |
| Line numbers 521-632 for export function | ✓ CONFIRMED accurate |
| Bug at lines 636-673 | ✓ CONFIRMED accurate |

### Key New Finding

The `players_projected.csv` file contains a **MIX of data**:
- **Week 1**: Matches actual game scores exactly (38.76 for Josh Allen)
- **Weeks 2-12**: Values are close to (but not exactly matching) current ESPN projections

This suggests the file was created after Week 1 games were played, causing Week 1 to be captured as actuals while later weeks got projection data. ESPN has since slightly updated their projection model, causing small discrepancies.

### Git History Evidence

The file was created on October 15, 2025 (commit `ab9db90`) with the message "Create players_projected.csv with historical week 1-6 projections" - but Week 1 already contained actual scores at creation time.

---

---

## 15. Final Verification (November 25, 2025)

### Code Bug Verification

The code at `espn_client.py:668-673` prioritizes actual scores over projections:

```python
# Lines 668-673: Code returns actuals first
if actual_entries:  # statSourceId=0 entries
    valid_actuals = [p for p in actual_entries if position == 'DST' or p > 0]
    if valid_actuals:
        return valid_actuals[0]  # Returns ACTUAL score when available
```

**Intended vs Actual Behavior**: For a "projected" file, the code SHOULD return `statSourceId=1` (projections), but it currently returns `statSourceId=0` (actuals) when available.

### CRITICAL CORRECTION: File Has MIXED Data

**Previous analysis was incomplete.** Re-verification revealed the file has a MIX of actual scores and projections:

| Player | Week 1 CSV | Week 1 Actual | Week 1 Projection | CSV Contains |
|--------|------------|---------------|-------------------|--------------|
| Josh Allen | 38.76 | 38.76 | 20.83 | ACTUAL |
| Saquon Barkley | 18.40 | 18.40 | 20.92 | ACTUAL |
| Amon-Ra St. Brown | 17.20 | 8.50 | 17.20 | **PROJECTION** |
| Jahmyr Gibbs | 18.42 | 15.00 | 18.42 | **PROJECTION** |

**Statistical Breakdown (100 players tested):**
- 46 players: CSV = ACTUAL score
- 42 players: CSV = PROJECTION (despite actual existing)
- 12 players: CSV = Unknown/unmatched value

### Code vs File Discrepancy

**Key Finding**: The current code would return ACTUAL scores for ALL players with actual > 0. But the file has projections for ~42% of players.

This indicates:
1. The file was NOT created by the current code
2. OR the code was different when the file was created
3. OR there was post-processing/manual editing

Git commit `ab9db90` (Oct 15, 2025) shows the file was created with this mixed pattern from the beginning.

### API Field Verification

| Field | Exists in API? | Notes |
|-------|---------------|-------|
| `appliedTotal` | ✅ YES | Contains fantasy points |
| `projectedTotal` | ❌ NO | Does NOT exist (code comments outdated) |
| `statSourceId` | ✅ YES | 0=actuals, 1=projections |

---

*Document created: November 24, 2025*
*Document updated: November 25, 2025 (re-verification with corrections)*
*Author: Claude Code Analysis*
