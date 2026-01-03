# Feature 01: Win Rate Simulation JSON Integration - Technical Specification

**Version:** 2.0 (Stage 2 Deep Dive)
**Last Updated:** 2026-01-01
**Status:** Deep Dive in progress

---

## Objective

Update the Win Rate Simulation subsystem to load player data from position-specific JSON files instead of the legacy CSV format. This restores Win Rate Sim functionality that was broken when the league helper module transitioned to JSON-based player data.

---

## Scope

**What's included in THIS feature:**
- Update `SimulationManager.py` season discovery and validation to expect JSON files
- Update `SimulatedLeague.py` to load 6 position-specific JSON files per week
- Parse JSON structure with projected_points/actual_points arrays
- Handle new field names (drafted_by as string, locked as boolean)
- Update week data caching to use JSON format instead of CSV format
- Verify `DraftHelperTeam.py` and `SimulatedOpponent.py` compatibility with PlayerManager JSON loading
- Maintain all existing simulation logic and algorithms (no functional changes)

**What's NOT included:**
- Changes to simulation algorithms or scoring logic
- Changes to configuration optimization parameters
- Updates to Accuracy Sim (that's Feature 2)
- Adding new simulation features

**Dependencies:**
- **Prerequisites:** None (foundation feature)
- **Blocks:** None (Feature 2 runs in parallel)

---

## Current Implementation (CSV-Based)

### Data Loading Flow

**See:** `research/WIN_RATE_SIM_DISCOVERY.md` for complete discovery findings

**Current flow:**
1. **SimulatedLeague._create_shared_data_dir()** - Creates shared directories, copies CSV files
2. **PlayerManager** instantiation - Loads data from CSV files
3. **_preload_week_data()** - Pre-loads all 17 weeks into cache using _parse_players_csv()
4. **_load_week_data()** - Updates PlayerManager with week-specific data during simulation

**Current file paths:**
- Historical structure: `data_folder/weeks/week_NN/players.csv` and `players_projected.csv`
- Legacy structure: `data_folder/players.csv` and `players_projected.csv`

---

## Data Structure Changes

### CSV Format (Current)

**Two files per week:**
- `players.csv` (actual points)
- `players_projected.csv` (projected points)

**Field types:**
- `drafted_by`: Integer or empty string
- `locked`: "0" or "1" (string)
- `projected_points`: Single float value
- `actual_points`: Single float value

### JSON Format (New)

**Six files per week:**
- `qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`

**JSON structure per file:**
```json
{
  "qb_data": [
    {
      "id": "3918298",
      "name": "Josh Allen",
      "position": "QB",
      "drafted_by": "",
      "locked": false,
      "projected_points": [20.8, 20.8, ...],  // 18 values
      "actual_points": [0, 0, ...]             // 18 values
    }
  ]
}
```

**Field type changes:**
- `drafted_by`: String (empty string = not drafted)
- `locked`: Boolean (true/false)
- `projected_points`: Array of 18 floats
- `actual_points`: Array of 18 floats

---

## Components Affected

### 1. SimulationManager.py

**Method:** `_validate_season_structure(folder)` (lines 166-211)
- **Current behavior:** Validates `players.csv` exists in each week folder (lines 210-211)
- **Change needed:** Validate 6 JSON files exist instead

**Method:** `_validate_season_data(season_folder)` (lines 213-252)
- **Current behavior:** Checks `players_projected.csv` or `players.csv` in week_01 (lines 228-231)
- **Change needed:** Check for JSON files instead

### 2. SimulatedLeague.py

**Method:** `__init__()` - Data path determination (lines 159-170)
- **Current behavior:** Determines paths to `players.csv` and `players_projected.csv`
- **Change needed:** Determine path to week folder containing JSON files

**Method:** `_create_shared_data_dir()` (lines 211-236)
- **Current behavior:** Copies 2 CSV files to shared directory (lines 231-232)
- **Change needed:** Copy 6 JSON files to shared directory
- **Signature change:** TBD (depends on approach - see checklist)

**Method:** `_preload_week_data()` (lines 269-294)
- **Current behavior:** Calls `_parse_players_csv()` for each week (line 289)
- **Change needed:** Call new JSON parsing method instead

**Method:** `_parse_players_csv()` (lines 296-316)
- **Current behavior:** Parses single CSV file into Dict[player_id, player_data]
- **Change needed:** Replace or supplement with `_parse_players_json()` that loads 6 JSON files

**New method needed:** `_parse_players_json(week_folder_path)` (TBD - details in checklist)

**Method:** `_load_week_data()` (lines 318-344)
- **Current behavior:** Passes cached week data to PlayerManager.set_player_data()
- **Verification needed:** Confirm compatibility with new field types

### 3. DraftHelperTeam.py

**No code changes expected:**
- Uses PlayerManager API (instantiation + method calls)
- PlayerManager already has `load_players_from_json()` method (verified in league_helper/util/PlayerManager.py:304)
- **Verification needed:** Confirm PlayerManager works with simulation folder structure

### 4. SimulatedOpponent.py

**No code changes expected:**
- Uses PlayerManager API like DraftHelperTeam
- **Verification needed:** Same as DraftHelperTeam

---

## Implementation Details

**Status:** ✅ ALL QUESTIONS RESOLVED via codebase investigation

**See:** `research/CODEBASE_INVESTIGATION_FINDINGS.md` for complete analysis

---

### Week-Specific Array Indexing

**JSON arrays use 0-based indexing:**
- Index 0 = Week 1
- Index 1 = Week 2
- ...
- Index 16 = Week 17

**Total elements:** 17 (REGULAR_SEASON_WEEKS from constants.py)

**Extraction formula:** `week_value = array[week_num - 1]`

**Evidence:** `historical_data_compiler/json_exporter.py:328` - `bye_idx = player_data.bye_week - 1`

---

### Data Extraction Strategy

**Approach:** Extract week-specific values DURING parsing (not during loading)

**Rationale:**
- Maintains consistent interface with `_parse_players_csv()`
- Keeps `_load_week_data()` unchanged
- JSON arrays already contain week-specific logic

**Method signature:**
```python
def _parse_players_json(week_folder: Path, week_num: int) -> Dict[int, Dict[str, Any]]:
    """
    Parse 6 JSON files and extract week-specific values from arrays.

    Args:
        week_folder: Path to week_NN folder containing 6 JSON files
        week_num: Current week number (1-17)

    Returns:
        Dict mapping player_id to player data (with single-value fields)
    """
```

**Extraction logic:**
```python
# For each player in JSON
projected = player_data['projected_points'][week_num - 1]
actual = player_data['actual_points'][week_num - 1]

# Return dict with single values (matching CSV format)
return {
    player_id: {
        'projected_points': projected,  # Single value
        'actual_points': actual,         # Single value
        ... # other fields
    }
}
```

---

### Shared Directory Structure

**Required structure:** `shared_dir/player_data/{position}_data.json`

**Why:** PlayerManager hardcodes `player_data/` subfolder (PlayerManager.py:327)

**Implementation in `_create_shared_data_dir()`:**
```python
def _create_shared_data_dir(dir_name: str, week_folder: Path) -> Path:
    """Create shared directory with player_data/ subfolder and 6 JSON files."""
    shared_dir = Path(tempfile.mkdtemp(prefix=dir_name))

    # Create player_data/ subfolder (REQUIRED by PlayerManager)
    player_data_dir = shared_dir / 'player_data'
    player_data_dir.mkdir()

    # Copy 6 JSON files from week folder to player_data/
    position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                      'te_data.json', 'k_data.json', 'dst_data.json']
    for position_file in position_files:
        src = week_folder / position_file
        dst = player_data_dir / position_file
        if src.exists():
            shutil.copy(src, dst)
        else:
            self.logger.warning(f"Missing {position_file} in {week_folder}")

    # Copy config and other required files
    shutil.copy(self.config_path, shared_dir / "league_config.json")
    # ... copy team_data, season_schedule, game_data

    return shared_dir
```

**Signature change:** Remove `players_csv_path` and `players_projected_path` parameters, replace with `week_folder` parameter

---

### Error Handling Strategy

**Two-tiered approach:**

**1. Validation (fail loud):**
```python
# In _validate_season_structure()
position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                  'te_data.json', 'k_data.json', 'dst_data.json']

for week in range(1, 18):
    week_folder = weeks_folder / f"week_{week:02d}"
    for position_file in position_files:
        json_file = week_folder / position_file
        if not json_file.exists():
            raise FileNotFoundError(
                f"Season {year} week_{week:02d}/ missing {position_file}"
            )
```

**2. Runtime (log warning, skip):**
```python
# In _preload_week_data()
for week_num in range(1, 18):
    week_folder = weeks_folder / f"week_{week_num:02d}"
    try:
        self.week_data_cache[week_num] = self._parse_players_json(week_folder, week_num)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        self.logger.warning(f"Week {week_num} data unavailable: {e}")
        # Skip this week (cache remains empty for this week)
```

---

### Field Type Handling

**No conversion needed** - FantasyPlayer.from_json() handles types correctly

**Evidence:**
- `locked`: FantasyPlayer.py:250 loads boolean directly
- `drafted_by`: FantasyPlayer.py:240 loads string directly

**Verification:**
```python
# FantasyPlayer.from_json() (utils/FantasyPlayer.py:248-274)
locked = data.get('locked', False)  # Boolean loaded as-is
drafted_by = data.get('drafted_by', '')  # String loaded as-is
```

**Result:** No type conversion logic needed in simulation code

---

### Array Length Validation

**Handled by FantasyPlayer.from_json():**
```python
# FantasyPlayer.py:235-237
projected_points = (projected_points + [0.0] * 17)[:17]  # Pad/truncate to 17
actual_points = (actual_points + [0.0] * 17)[:17]  # Pad/truncate to 17
```

**Result:** No additional validation needed in simulation code

---

## Implementation Estimate

**Based on codebase investigation:**
- **Files with code changes:** 2 (SimulationManager.py, SimulatedLeague.py)
- **Files needing verification only:** 2 (DraftHelperTeam.py, SimulatedOpponent.py) - NO CHANGES
- **New methods needed:** 1 (`_parse_players_json()`)
- **Modified methods:** 5 methods across 2 files
- **Lines of code (estimated):** ~150 LOC
- **Risk level:** MEDIUM (core data loading, but well-isolated changes)

**No PlayerManager modifications required** - it already handles JSON correctly

---

**Status:** Ready for Stage 5a (TODO Creation)
