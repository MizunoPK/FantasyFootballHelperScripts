# Add Bye Week to Player Data - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `add_bye_week_to_player_data_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [ ] **Field name:** Confirm `bye_week` is the correct field name (vs `byeWeek` or `bye`)
- [ ] **Field placement:** Determine where in JSON object bye_week should appear
- [ ] **Consistency check:** Verify same field name and format used across both systems

---

## API/Data Source Questions

- [x] **Player-data-fetcher data source:** Where does bye_week come from in player-data-fetcher?
  - ✅ RESOLVED: Derives from `data/season_schedule.csv` via `_derive_bye_weeks_from_schedule()` method
  - Identifies bye week by finding which week team is missing from schedule
  - Returns `Dict[str, int]` mapping team abbreviation to bye week number (1-17)
- [x] **Historical compiler data source:** Where does bye_week come from in historical_data_compiler?
  - ✅ RESOLVED: Similar logic via `identify_bye_weeks()` method
  - Both systems use schedule data, NOT ESPN API
- [x] **Data validation:** Is bye_week data correctly populated before JSON export?
  - ✅ RESOLVED: YES - Both systems populate bye_week correctly from schedule data
  - Historical compiler already uses it internally (lines 327-331 in json_exporter.py)
- [x] **Null handling:** What should bye_week be if missing?
  - ✅ RESOLVED: Use `None` (JSON null) - matches CSV pattern and Optional[int] type
  - CSV export uses `""` for missing values, but JSON should use `null`
  - Code uses `dict.get(team)` which returns `None` if team not found

---

## Output Files / Data Structures

### Player-Data-Fetcher JSON Output

**File-level decisions:**
- [ ] Location: `data/player_data/{position}_data.json`
- [ ] Method to modify: `_prepare_position_json_data()`

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `bye_week` | [ ] | From `player.bye_week` (FantasyPlayer) |

**Questions:**
- [x] Data type in JSON: integer, string, or null?
  - ✅ RESOLVED: Integer (or null if missing) - matches `Optional[int]` type
- [x] Should bye_week be rounded/formatted?
  - ✅ RESOLVED: NO - bye_week is already an integer (1-17), no rounding needed
- [x] CSV uses empty string for null - what about JSON?
  - ✅ RESOLVED: JSON uses `null` (standard JSON practice for None values)

**Implementation Note:** Add to `json_data` dictionary in `player-data-fetcher/player_data_exporter.py:494-510`

### Historical Data Compiler JSON Output

**File-level decisions:**
- [ ] Location: `simulation/sim_data/{year}/weeks/week_{NN}/{position}_data.json`
- [ ] Method to modify: `_build_player_json_object()`

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `bye_week` | [x] | From `player_data.bye_week` (PlayerData) - line 327 shows it's already used for logic |

**Questions:**
- [x] Data type in JSON: integer, string, or null?
  - ✅ RESOLVED: Integer (or null if missing) - matches `Optional[int]` type
- [x] Should bye_week be rounded/formatted?
  - ✅ RESOLVED: NO - bye_week is already an integer (1-17), no rounding needed
- [x] Current code uses bye_week for array logic (lines 327-331) but doesn't export it
  - ✅ CONFIRMED: Code already uses bye_week internally to zero out bye week indices
  - Just needs to be added to the player_obj dictionary

**Implementation Note:** Add to `player_obj` dictionary in `historical_data_compiler/json_exporter.py:337-349`

---

## Algorithm/Logic Questions

- [x] **Bye week logic verification:** Both systems already use bye_week internally - verify this logic is correct
  - ✅ VERIFIED: Both systems handle bye weeks correctly (points = 0.0 during bye)
  - Historical compiler: Sets bye week indices to 0.0 in arrays during JSON export (lines 327-331)
  - Player-data-fetcher: Points already 0.0 for bye weeks from ESPN data (no additional logic needed)
  - Confirmed via CSV data: Christian McCaffrey (bye=14, week_14_points=0.0), Jahmyr Gibbs (bye=8, week_8_points=0.0)
- [x] **Consistency:** Should JSON bye_week match CSV bye_week exactly?
  - ✅ RESOLVED: YES - JSON bye_week should exactly match CSV bye_week value
  - Both use same data source (season_schedule.csv) and same Optional[int] type
  - CSV shows bye_week is already correctly populated (e.g., "8", "14")

---

## Architecture Questions

- [x] **Code reuse:** Can we reference CSV export implementation for consistency?
  - ✅ RESOLVED: YES - CSV export pattern shows null handling: `self.bye_week if self.bye_week is not None else ""`
  - JSON should use `None` (outputs as `null`) instead of empty string
- [x] **Field ordering:** Should bye_week appear in specific position in JSON object?
  - ✅ RESOLVED: Place after "position" field, before "injury_status"
  - Current JSON: id, name, team, position, injury_status, ...
  - New JSON: id, name, team, position, **bye_week**, injury_status, ...
  - Rationale: Matches CSV column order, groups player identity fields together

---

## Error Handling Questions

- [x] **Missing bye_week:** What if bye_week is None?
  - ✅ RESOLVED: JSON exports None as `null` - matches Optional[int] type
  - CSV uses empty string `""` but JSON uses `null`
- [x] **Invalid bye_week:** What if bye_week is outside 1-17 range?
  - ✅ RESOLVED: Trust the data source - no validation needed during JSON export
  - NFL season structure can vary (some seasons have 17 weeks, some 18)
  - If schedule data is wrong, that's a data quality issue, not a code issue
  - JSON export should faithfully represent the data without filtering
- [x] **Schedule data dependency:** What if `season_schedule.csv` is missing or malformed?
  - ✅ RESOLVED: Already handled - player_data_fetcher_main.py raises FileNotFoundError (lines 122-129)
  - User sees clear error message directing them to create the file
  - No additional handling needed in JSON export (bye_week will be None if not populated)
- [x] **Team abbreviation mismatch:** What if team abbreviation in player data doesn't match season_schedule.csv?
  - ✅ RESOLVED: Handled gracefully - `dict.get(team)` returns `None` if team not found
  - player_data_fetcher_main.py logs warnings for teams without bye weeks (lines 196-197)
  - JSON export will show `"bye_week": null` for these players
  - No additional logging needed in JSON export layer

---

## Edge Cases

- [x] **Players without teams:** Do free agents have bye weeks?
  - ✅ RESOLVED: If player has no team or team not in schedule, `dict.get(team)` returns `None`
  - JSON will show `"bye_week": null` which is correct behavior for free agents
- [x] **DST positions:** Do defenses have bye weeks?
  - ✅ RESOLVED: YES - DST positions have teams and therefore have bye weeks
  - Defenses are tied to NFL teams which all have bye weeks
- [x] **Future weeks:** Does bye_week get populated for future seasons?
  - ✅ RESOLVED: YES - as long as season_schedule.csv exists for that season
  - season_schedule.csv is season-specific (user must provide it for each season)
- [x] **Historical data:** Is bye_week available for past seasons?
  - ✅ RESOLVED: YES - historical_data_compiler already uses bye_week field
  - Historical data can be compiled for any season with a season_schedule.csv file

---

## Testing & Validation

- [x] **Output verification:** How to verify bye_week appears in JSON?
  - ✅ METHOD: Read generated JSON file, parse it, verify "bye_week" field exists
  - Check multiple positions (QB, RB, WR, TE, K, DST)
  - Verify field appears in correct position (after "position", before "injury_status")
- [x] **Data accuracy:** How to verify bye_week values are correct?
  - ✅ METHOD: Compare JSON bye_week to CSV bye_week (should match exactly)
  - Both use same data source (season_schedule.csv) so values must be identical
  - Spot-check against known bye weeks (e.g., DET=8, SF=14 per CSV data)
  - No need to compare to ESPN - ESPN doesn't provide bye_week data
- [x] **Test cases needed:**
  - ✅ IDENTIFIED:
    - Player with bye week set (e.g., Christian McCaffrey, bye_week=14)
    - Player with bye_week = None (free agent or team not in schedule)
    - All positions (QB, RB, WR, TE, K, DST) - verify field exists for each
    - Data type verification (integer or null, not string)
    - Field ordering verification (after position, before injury_status)

---

## Integration Questions

- [x] **Consumers:** Who/what reads these JSON files?
  - ✅ IDENTIFIED: Simulation system uses JSON files (found json.load in simulation/*.py)
  - League helper uses `players.csv`, NOT JSON files (loads via PlayerManager)
  - JSON files are primarily for simulation/analysis purposes
- [x] **Backwards compatibility:** Will adding bye_week break existing consumers?
  - ✅ RESOLVED: NO - Adding a new field is backwards compatible
  - Additive changes don't break existing consumers (they ignore unknown fields)
  - Most JSON parsers ignore extra fields by default
  - Consumers can choose to use bye_week or ignore it
- [x] **Schema validation:** Do consumers validate JSON schema?
  - ✅ RESOLVED: Not a concern - Python JSON parsing is permissive
  - Simulation system uses json.load() which doesn't enforce schema
  - No strict schema validation found in consumer code
  - Extra fields are safely ignored

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| bye_week (player-data-fetcher) | ESPN API or FantasyPlayer model | Needs verification |
| bye_week (historical compiler) | PlayerData.bye_week | Known - already used in code |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Bye week data source (both systems) | Derives from `data/season_schedule.csv`, NOT ESPN API. Uses `_derive_bye_weeks_from_schedule()` method to identify which week team is missing from schedule. Returns `Dict[str, int]`. | 2025-12-26 |
| Data validation | Confirmed bye_week is correctly populated before JSON export in both systems. Historical compiler already uses it internally (lines 327-331). | 2025-12-26 |
| Null handling for bye_week | Use `None` (JSON null) when team not found. Matches Optional[int] type and CSV pattern (CSV uses empty string, JSON uses null). | 2025-12-26 |
| Field ordering in JSON | Place bye_week after "position" field, before "injury_status". Matches CSV column order and groups player identity fields together. | 2025-12-26 |
| Data type in JSON | Export as integer (or null if missing). No rounding/formatting needed - bye_week is already an integer (1-17). | 2025-12-26 |
| Code reuse from CSV export | Can reference CSV null handling pattern: `self.bye_week if self.bye_week is not None else ""`. JSON uses None instead of empty string. | 2025-12-26 |
| Bye week logic verification | Both systems handle bye weeks correctly. Historical compiler sets bye week indices to 0.0 during export. Player-data-fetcher gets 0.0 points from ESPN data. Verified via CSV data. | 2025-12-26 |
| JSON/CSV consistency | JSON bye_week should exactly match CSV bye_week value. Both use same data source (season_schedule.csv) and same Optional[int] type. | 2025-12-26 |
| Edge cases (all positions) | All positions (including DST) have bye weeks. Free agents/missing teams get null. Works for past/future seasons with season_schedule.csv. | 2025-12-26 |
| Error handling | Invalid bye_week: trust data source. Schedule dependency: already raises FileNotFoundError. Team mismatch: dict.get() returns None gracefully. | 2025-12-26 |
| Integration | Simulation system uses JSON files. League helper uses CSV only. Adding bye_week is backwards compatible - consumers ignore unknown fields. | 2025-12-26 |
| Testing strategy | Verify field exists in JSON, compare to CSV for accuracy, test all positions, verify data types and field ordering. | 2025-12-26 |
