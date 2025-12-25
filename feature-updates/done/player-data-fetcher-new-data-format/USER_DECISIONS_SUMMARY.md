# Player Data Fetcher - New Data Format - User Decisions Summary

**Date:** December 24, 2024
**Status:** ALL 11 DECISIONS COMPLETE ✅

---

## Decision Summary

### 1. Config Toggle Default Value
**Decision:** `CREATE_POSITION_JSON = True` (enabled by default)

**Rationale:** Feature is needed immediately, consistent with `CREATE_CSV = True` pattern, minimal performance impact due to async execution.

---

### 2. Array Length (17 vs 18 elements)
**Decision:** **17 elements** (weeks 1-17, fantasy regular season only)

**Rationale:** Matches user notes ("17 elements, weeks 1-17"), matches existing `ESPNPlayerData` model (week_1_points through week_17_points), fantasy leagues exclude Week 18. The 18 elements in example's `actual_points` was a typo.

**Implementation:**
- All arrays (projected_points, actual_points, and all stat arrays) have exactly 17 elements
- Array index 0 = Week 1, index 16 = Week 17

---

### 3. Typo Fix - "recieving" vs "receiving"
**Decision:** Use **"receiving"** (correct spelling)

**Rationale:** Correct English spelling, professional code quality, easier maintenance. Example files were templates with a typo.

**Impact:**
- `"recieving"` → `"receiving"`
- `"recieving_yds"` → `"receiving_yds"`
- `"recieving_tds"` → `"receiving_tds"`

---

### 4. JSON Key "2_pt" Naming
**Decision:** Use **"two_pt"** (conventional naming)

**Rationale:** Consistent with other keys (all start with letters), follows snake_case convention, prevents potential issues in downstream languages.

**Impact:**
- `"2_pt"` → `"two_pt"`

---

### 5. Empty vs Zero-Filled Arrays
**Decision:** **Actual data for past weeks (weeks 1-CURRENT_NFL_WEEK), zeros for future weeks**

**Rationale:** Matches user notes ("use 0 for unplayed weeks"), consistent structure (all arrays always 17 elements), clear semantics.

**Implementation:**
```python
for week in range(1, 18):
    if week <= CURRENT_NFL_WEEK:
        stat_value = extract_actual_stat(player, week, stat_id)  # statSourceId=0
    else:
        stat_value = 0.0  # Future week not yet played
```

**Missing stat handling:** If stat data is missing for a past week, use 0.

---

### 6. Return Yards Source (ret_yds, ret_tds)
**Decision:** **Remove `ret_yds` and `ret_tds` fields entirely from non-DST positions**

**Rationale:** ESPN only provides return stats for D/ST players. Rather than having misleading zeros for all non-DST positions, remove the fields entirely.

**Implementation:**

**Non-DST positions (QB, RB, WR, TE, K):**
```json
"misc": {
    "fumbles": [],
    "two_pt": []
    // ret_yds and ret_tds removed
}
```

**DST position only:**
```json
"defense": {
    "yds_g": [],
    "pts_g": [],
    "def_td": [],
    "sacks": [],
    "safety": [],
    "interceptions": [],
    "forced_fumble": [],
    "fumbles_recovered": [],
    "ret_yds": [],     // stat_114 + stat_115 (kickoff + punt return yards)
    "ret_tds": []      // stat_101 + stat_102 (kickoff + punt return TDs)
}
```

---

### 7. Field Goal Distance Granularity
**Decision:** **Simplify to just made/missed totals (no distance breakdown)**

**Rationale:** ESPN provides 3 distance ranges (0-39, 40-49, 50+) but example had 5 ranges. Rather than deal with the mismatch, simplify to just totals which are clearer and universally available.

**Implementation:**
```json
"field_goals": {
    "made": [],      // stat_83 (total FG made)
    "missed": []     // stat_85 (total FG missed)
}
```

**Removed:** All distance-based fields (under_19, under_29, under_39, under_49, over_50)

---

### 8. Stat Arrays for Historical Weeks
**Decision:** Use **actual stats (statSourceId=0)** for weeks already played

**Rationale:** Parallel to `actual_points` array logic, more valuable data (actual performance vs old projections), historical accuracy.

**Implementation:**
```python
if week <= CURRENT_NFL_WEEK:
    stat_value = get_stat(player, week, stat_id, statSourceId=0)  # Actual game stats
```

---

### 9. Stat Arrays for Future Weeks
**Decision:** Use **zeros** for weeks not yet played

**Rationale:** Clear semantic meaning (zero = game not played), consistent with "use 0 for unplayed weeks", separates concerns (projected_points has projections, stat arrays have actuals only).

**Implementation:**
```python
else:  # week > CURRENT_NFL_WEEK
    stat_value = 0.0  # Future week, use zero
```

**Note:** The `projected_points` array still contains projections for all 17 weeks (including future weeks) - this decision only affects position-specific stat arrays.

---

### 10. Team Name Reverse Lookup Implementation
**Decision:** **Add `get_team_name_for_player()` method to DraftedRosterManager**

**Rationale:** Clean API, keeps DraftedRosterManager as single source of truth, encapsulated logic, simple implementation.

**Implementation:**

**Add to `utils/DraftedRosterManager.py`:**
```python
def get_team_name_for_player(self, player: FantasyPlayer) -> str:
    """
    Get fantasy team name for a player.

    Args:
        player: FantasyPlayer object

    Returns:
        Team name string if player is drafted, empty string otherwise
    """
    # Build normalized player key
    player_info = f"{player.name} {player.position} - {player.team}"
    player_key = self._normalize_player_info(player_info)

    # Look up in drafted_players dict
    return self.drafted_players.get(player_key, "")
```

**Usage in `DataExporter`:**
```python
# Build drafted_by field for JSON:
if player.drafted == 0:
    drafted_by = ""  # Free agent
elif player.drafted == 2:
    drafted_by = MY_TEAM_NAME  # User's team
else:  # drafted == 1
    drafted_by = self.drafted_roster_manager.get_team_name_for_player(player)
```

---

### 11. Missing Stat Handling
**Decision:** **Always use 0** (never null/None)

**Rationale:** Matches user notes ("use 0 NOT null"), simplest implementation, correct semantics (missing = didn't occur = 0).

**Implementation:**
```python
# When extracting stats from ESPN API:
stat_value = player_stats.get(stat_id, 0.0)  # Default to 0 if missing
```

**Applies to:**
- Future weeks: 0
- Missing stat data from API: 0
- Stat legitimately didn't occur: 0
- Bye weeks: 0

**Never use:** null, None, or empty values in arrays

---

## Updated JSON Structure Examples

### QB/RB/WR/TE Structure (with all decisions applied):

```json
{
    "qb_data": [
        {
            "id": 123,
            "name": "Trevor Lawrence",
            "team": "JAX",
            "position": "QB",
            "injury_status": "ACTIVE",
            "drafted_by": "Sea Sharp",
            "locked": true,
            "average_draft_position": 170,
            "player_rating": 97,
            "projected_points": [18.4, 18.1, ..., 22.6],  // 17 elements
            "actual_points": [97.5, 15.0, ..., 9.8, 0],   // 17 elements (Week 17 = 0, not yet played)

            "passing": {
                "completions": [25, 18, ..., 0],           // 17 elements
                "attempts": [39, 30, ..., 0],
                "pass_yds": [315, 280, ..., 0],
                "pass_tds": [2, 1, ..., 0],
                "interceptions": [1, 0, ..., 0],
                "sacks": [2, 3, ..., 0]
            },
            "rushing": {
                "attempts": [3, 2, ..., 0],
                "rush_yds": [15, 8, ..., 0],
                "rush_tds": [0, 0, ..., 0]
            },
            "receiving": {                                  // ← Fixed spelling
                "targets": [0, 0, ..., 0],
                "receiving_yds": [0, 0, ..., 0],           // ← Fixed spelling
                "receiving_tds": [0, 0, ..., 0],           // ← Fixed spelling
                "receptions": [0, 0, ..., 0]
            },
            "misc": {
                "fumbles": [0, 1, ..., 0],
                "two_pt": [0, 0, ..., 0]                   // ← Fixed key name
                // ret_yds and ret_tds removed for non-DST
            }
        }
    ]
}
```

### K (Kicker) Structure:

```json
{
    "k_data": [
        {
            "id": 456,
            "name": "Brandon Aubrey",
            "team": "DAL",
            "position": "K",
            "injury_status": "ACTIVE",
            "drafted_by": "",
            "locked": false,
            "average_draft_position": 200,
            "player_rating": 85,
            "projected_points": [8.5, 9.2, ..., 8.8],
            "actual_points": [12.0, 6.0, ..., 0],

            "extra_points": {
                "made": [3, 2, ..., 0],
                "missed": [0, 0, ..., 0]
            },
            "field_goals": {                               // ← Simplified structure
                "made": [2, 1, ..., 0],
                "missed": [0, 1, ..., 0]
                // All distance breakdowns removed
            }
        }
    ]
}
```

### DST Structure:

```json
{
    "dst_data": [
        {
            "id": 789,
            "name": "Eagles D/ST",
            "team": "PHI",
            "position": "DST",
            "injury_status": "ACTIVE",
            "drafted_by": "Pidgin",
            "locked": false,
            "average_draft_position": 150,
            "player_rating": 92,
            "projected_points": [10.5, 11.2, ..., 10.8],
            "actual_points": [15.0, 8.0, ..., 0],

            "defense": {
                "yds_g": [320, 280, ..., 0],
                "pts_g": [17, 21, ..., 0],
                "def_td": [1, 0, ..., 0],
                "sacks": [4, 3, ..., 0],
                "safety": [0, 1, ..., 0],
                "interceptions": [2, 1, ..., 0],
                "forced_fumble": [1, 2, ..., 0],
                "fumbles_recovered": [1, 1, ..., 0],
                "ret_yds": [29, 15, ..., 0],               // ← Only in DST
                "ret_tds": [0, 0, ..., 0]                  // ← Only in DST
            }
        }
    ]
}
```

---

## Configuration Updates

**Add to `player-data-fetcher/config.py`:**
```python
# Output Settings (FREQUENTLY MODIFIED)
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = False
CREATE_CONDENSED_EXCEL = False
CREATE_POSITION_JSON = True  # ← NEW: Generate position-based JSON files
DEFAULT_FILE_CAPS = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}

# Position JSON Output Settings
POSITION_JSON_OUTPUT = "../data/player_data"  # ← NEW: Output folder for position JSON files
```

---

## Implementation Checklist

- [ ] Update config.py with new settings
- [ ] Add `get_team_name_for_player()` to DraftedRosterManager
- [ ] Create `export_position_json_files()` in DataExporter
- [ ] Implement stat extraction logic (statSourceId=0 for past weeks, 0 for future)
- [ ] Apply all structural decisions (17 elements, correct spellings, simplified field goals)
- [ ] Remove ret_yds/ret_tds from non-DST position JSON generation
- [ ] Add position JSON export to main workflow
- [ ] Create unit tests for new functionality
- [ ] Validate output against decisions (QC protocol)

---

## Status

**Planning Phase:** COMPLETE ✅
**All User Decisions:** RESOLVED ✅
**Next Phase:** DEVELOPMENT (Implementation)
