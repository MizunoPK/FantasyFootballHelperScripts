# Add Bye Week to Player Data

## Objective

Add the `bye_week` field to the position-specific JSON files exported by both the player-data-fetcher and historical_data_compiler systems. The field already exists in the internal data models but is not currently included in the JSON output.

---

## High-Level Requirements

### 1. Player-Data-Fetcher JSON Export
- **Location:** `player-data-fetcher/player_data_exporter.py`
- **Method:** `_prepare_position_json_data()` (lines 479-535)
- **Change:** Add `"bye_week": player.bye_week` to the `json_data` dictionary

### 2. Historical Data Compiler JSON Export
- **Location:** `historical_data_compiler/json_exporter.py`
- **Method:** `_build_player_json_object()` (lines 286-349)
- **Change:** Add `"bye_week": player_data.bye_week` to the `player_obj` dictionary

### 3. Output Format
```json
{
  "id": "3918298",
  "name": "Josh Allen",
  "team": "BUF",
  "position": "QB",
  "bye_week": 6,
  "injury_status": "ACTIVE",
  "drafted_by": "",
  "locked": false,
  ...
}
```

---

## Resolved Implementation Details

### Data Models (Already Exist)

**player-data-fetcher/player_data_models.py (line 40):**
```python
class ESPNPlayerData(BaseModel):
    ...
    bye_week: Optional[int] = None
    ...
```

**historical_data_compiler/player_data_fetcher.py (line 76):**
```python
@dataclass
class PlayerData:
    ...
    bye_week: Optional[int] = None
    ...
```

### Bye Week Data Source (Resolved)

**Player-Data-Fetcher Source:**
- **File:** `player-data-fetcher/player_data_fetcher_main.py` (lines 125-174)
- **Method:** `_derive_bye_weeks_from_schedule()`
- **Data Source:** Reads `data/season_schedule.csv`
- **Logic:** Identifies bye week by finding which week (1-17) a team is missing from the schedule
- **Format:** Returns `Dict[str, int]` mapping team abbreviation to bye week number
- **Usage:** `bye_week = self.bye_weeks.get(team)` in espn_client.py (line 1674)
- **Null Handling:** `dict.get(team)` returns `None` if team not found

**Historical Data Compiler Source:**
- **Logic:** Similar approach - derives from schedule data via `identify_bye_weeks()`
- **Data Flow:** Schedule dict → bye_weeks dict → PlayerData.bye_week
- **Already Used Internally:** json_exporter.py lines 327-331 uses bye_week to set array indices to 0.0

**Key Finding:** Both systems derive bye weeks from NFL schedule data, NOT from ESPN API. The data is already correctly populated before JSON export.

### Field Ordering and Data Type (Resolved)

**Field Placement:**
- **Location:** After "position" field, before "injury_status" field
- **Rationale:**
  - Matches CSV column order where bye_week appears right after position
  - Groups player identity fields (id, name, team, position, bye_week) before status fields
- **Field Order:** id → name → team → position → **bye_week** → injury_status → drafted_by → locked → ...

**Data Type:**
- **Format:** Integer (or null if missing)
- **Example:** `"bye_week": 6` or `"bye_week": null`
- **Type:** Matches `Optional[int]` from data models
- **No Rounding:** bye_week is already an integer (1-17), no formatting needed
- **Null Handling:** JSON exports None as `null` (standard practice), CSV uses empty string `""`

### CSV Exports (Already Include Bye Week)

**historical_data_compiler/player_data_fetcher.py (lines 42-50):**
```python
PLAYERS_CSV_COLUMNS = [
    "id", "name", "team", "position", "bye_week", "drafted", "locked",
    ...
]
```

**PlayerData.to_csv_row() (line 94):**
```python
"bye_week": self.bye_week if self.bye_week is not None else "",
```

### Current JSON Export (Missing Bye Week)

**player-data-fetcher/player_data_exporter.py (lines 494-510):**
```python
json_data = {
    "id": player.id,
    "name": player.name,
    "team": player.team,
    "position": player.position,
    "injury_status": player.injury_status,
    "drafted_by": self._get_drafted_by(player),
    "locked": bool(player.locked),
    "average_draft_position": player.average_draft_position,
    "player_rating": player.player_rating,
    "projected_points": self._get_projected_points_array(espn_data),
    "actual_points": self._get_actual_points_array(espn_data)
}
# bye_week NOT included!
```

**historical_data_compiler/json_exporter.py (lines 337-349):**
```python
player_obj = {
    "id": player_data.id,
    "name": player_data.name,
    "team": player_data.team,
    "position": player_data.position,
    "injury_status": player_data.injury_status if player_data.injury_status else "ACTIVE",
    "drafted_by": "",
    "locked": False,
    "average_draft_position": player_data.average_draft_position,
    "player_rating": round(player_rating, 1),
    "projected_points": [round(p, 1) for p in projected_points],
    "actual_points": [round(p, 1) for p in actual_points],
}
# bye_week NOT included!
```

---

## Implementation Notes

### Files to Modify
- `player-data-fetcher/player_data_exporter.py` - Add bye_week to JSON export
- `historical_data_compiler/json_exporter.py` - Add bye_week to JSON export

### Dependencies
- No new dependencies required
- Uses existing `bye_week` field from data models

### Reusable Code
- Both CSV exports already handle bye_week correctly
- Can reference CSV export logic for null handling

### Testing & Validation Strategy

**Output Verification:**
- Read generated JSON files for all positions (QB, RB, WR, TE, K, DST)
- Parse JSON and verify "bye_week" field exists in each player object
- Verify field appears in correct position: after "position", before "injury_status"
- Verify data type: integer for populated values, null for missing values

**Data Accuracy:**
- Compare JSON bye_week values to CSV bye_week values (should match exactly)
- Both use same data source (season_schedule.csv), so values must be identical
- Spot-check against known values from CSV (e.g., Christian McCaffrey: bye_week=14)
- No need to verify against ESPN - ESPN API doesn't provide bye week data

**Test Cases:**
1. Player with bye week set (e.g., Christian McCaffrey, bye_week=14)
2. Player with bye_week = None (free agent or team not in schedule)
3. All positions (QB, RB, WR, TE, K, DST) - verify field exists for each
4. Data type verification (integer or null, not string)
5. Field ordering verification (correct position in JSON object)
6. Backwards compatibility (existing consumers still work)

### Integration & Consumers

**JSON File Consumers:**
- **Simulation System:** Uses position-specific JSON files for win rate analysis (simulation/*.py)
- **League Helper System:** Does NOT use JSON files - reads from players.csv only
- JSON files are primarily for simulation and analysis purposes

**Backwards Compatibility:**
- Adding bye_week field is backwards compatible (additive change)
- Existing consumers ignore unknown fields by default (Python json.load() behavior)
- Simulation system can choose to use bye_week or ignore it
- No breaking changes to existing functionality

**Error Handling:**
- Invalid bye_week values: Trust the data source - faithfully export what's in the data model
- Missing schedule data: Already handled by player_data_fetcher_main.py (raises FileNotFoundError)
- Team abbreviation mismatch: Handled gracefully - dict.get() returns None, exports as null
- No additional error handling needed in JSON export layer

---

## Status: PLANNING COMPLETE - READY FOR IMPLEMENTATION
