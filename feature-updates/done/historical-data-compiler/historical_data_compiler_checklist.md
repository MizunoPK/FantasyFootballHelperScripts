# Historical Data Compiler - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `historical_data_compiler.txt` with full implementation details (data sources, field mappings, calculation logic, etc.). The checklist tracks status; the txt file is the implementation spec.

---

## General Decisions

- [x] **Week range:** 1-17 (full regular season)
- [x] **Year support:** 2021+ only (weekly data required; 2015-2020 not supported)
- [x] **Position filtering:** QB, RB, WR, TE, K, DST (6 fantasy-relevant positions)
- [x] **Scoring system:** Use ESPN fantasy points directly (`appliedTotal` field)
- [x] **Dependencies:** httpx + standard library (same as player-data-fetcher)

---

## Output Files Checklist

### 1. `simulation/sim_data/{YEAR}/season_schedule.csv`

**File-level decisions:**
- [x] Data source for schedule → **ESPN scoreboard API** (reuse `ScheduleFetcher.py` logic)
- [x] Include all 17 weeks → **Yes, weeks 1-17**

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `week` | [x] | Week number (1-17) - from API week parameter |
| `team` | [x] | Team abbreviation - from API, normalized (WAS→WSH) |
| `opponent` | [x] | Opponent abbreviation - from API matchup data |

**Questions:**
- [x] Do we include bye weeks in schedule? → **Yes, with empty opponent**
- [x] How do we handle teams with same opponent (home vs away distinction)? → **game_data.csv has home/away; schedule just shows matchups**

**Implementation Note:** Borrow logic from `schedule-data-fetcher/ScheduleFetcher.py` which already fetches from ESPN API and handles bye week detection.

---

### 2. `simulation/sim_data/{YEAR}/game_data.csv`

**File-level decisions:**
- [x] Data source for game results → **ESPN Scoreboard API** (reuse `game_data_fetcher.py` logic)
- [x] Data source for weather data → **Open-Meteo Archive API** (historical) / **Forecast API** (recent)
- [x] Data source for venue/location data → **ESPN Scoreboard API** (venue object in competition)

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `week` | [x] | ESPN API - week parameter |
| `home_team` | [x] | ESPN API - `competitors[].team.abbreviation` where `homeAway=home` |
| `away_team` | [x] | ESPN API - `competitors[].team.abbreviation` where `homeAway=away` |
| `temperature` | [x] | Open-Meteo API - `temperature_2m` at game hour (None for indoor) |
| `gust` | [x] | Open-Meteo API - `wind_gusts_10m` at game hour (None for indoor) |
| `precipitation` | [x] | Open-Meteo API - `precipitation` at game hour (None for indoor) |
| `home_team_score` | [x] | ESPN API - `competitors[].score` where `homeAway=home` |
| `away_team_score` | [x] | ESPN API - `competitors[].score` where `homeAway=away` |
| `indoor` | [x] | ESPN API - `venue.indoor` boolean |
| `neutral_site` | [x] | ESPN API - `competition.neutralSite` boolean |
| `country` | [x] | ESPN API - `venue.address.country` (default: "USA") |
| `city` | [x] | ESPN API - `venue.address.city` |
| `state` | [x] | ESPN API - `venue.address.state` (None for international) |
| `date` | [x] | ESPN API - `event.date` (ISO 8601 format) |

**Questions:**
- [x] Is weather data available historically? → **Yes, Open-Meteo Archive API provides historical weather**
- [x] If weather unavailable, use defaults or leave empty? → **Empty/None for indoor games**
- [x] Where do we get stadium indoor/outdoor info? → **ESPN API `venue.indoor` flag**
- [x] How do we identify neutral site games? → **ESPN API `competition.neutralSite` flag**

**Implementation Note:** Reuse logic from `player-data-fetcher/game_data_fetcher.py` which already implements all of this. Uses `coordinates.json` for stadium lat/lon lookup for weather API calls.

---

### 3. `simulation/sim_data/{YEAR}/team_data/{TEAM}.csv` (32 files)

**File-level decisions:**
- [x] How to calculate defensive stats → **Aggregate from player fantasy points vs opponent**
- [x] Cumulative through week N or just week N stats? → **Single-week values (not cumulative)**
- [x] Data source for team scores → **Calculated from player fantasy points**

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `week` | [x] | Week number (1-17) |
| `pts_allowed_to_QB` | [x] | Sum of QB fantasy points scored AGAINST this team |
| `pts_allowed_to_RB` | [x] | Sum of RB fantasy points scored AGAINST this team |
| `pts_allowed_to_WR` | [x] | Sum of WR fantasy points scored AGAINST this team |
| `pts_allowed_to_TE` | [x] | Sum of TE fantasy points scored AGAINST this team |
| `pts_allowed_to_K` | [x] | Sum of K fantasy points scored AGAINST this team |
| `points_scored` | [x] | Sum of fantasy points by players ON this team |
| `points_allowed` | [x] | Sum of fantasy points by players AGAINST this team |

**Questions:**
- [x] Calculate pts_allowed from ESPN API player stats vs opponent? → **Yes, aggregate player points by opponent**
- [x] How to handle bye weeks in team files (skip row or 0s)? → **Include row with 0s for all fields**
- [x] Rolling average or single-week values? → **Single-week values**

**Implementation Note:** Reuse algorithm from `player-data-fetcher/espn_client.py:_collect_team_weekly_data()` which already implements this exact logic.

---

### 4. `simulation/sim_data/{YEAR}/weeks/week_NN/players.csv`

**File-level decisions:**
- [x] Cumulative stats through week N or just week N? → **See week column logic below (actuals for past, projected for future)**
- [x] Which positions to include? → **QB, RB, WR, TE, K, DST (6 positions)**
- [x] Minimum games/stats threshold to include player? → **Filter by activity (at least 1 game or projected points)**

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `id` | [x] | ESPN API player ID |
| `name` | [x] | ESPN API `fullName` |
| `team` | [x] | ESPN API team (normalized) |
| `position` | [x] | ESPN API `defaultPositionId` mapped to string |
| `bye_week` | [x] | **From schedule file** - lookup team's bye week |
| `fantasy_points` | [x] | **Sum of week_1_points through week_17_points** |
| `injury_status` | [x] | **Default: "ACTIVE"** |
| `drafted` | [x] | **Default: 0** |
| `locked` | [x] | **Default: 0** |
| `average_draft_position` | [x] | **ESPN API** - `ownership.averageDraftPosition` field |
| `player_rating` | [x] | **ESPN API** - Week 1: draft rank normalized; Week 2+: fantasy_points ranking |
| `week_1_points` | [x] | ESPN API `statSourceId=0` (actual) or `1` (projected) |
| `week_2_points` | [x] | ESPN API - see week column logic below |
| `week_3_points` | [x] | ESPN API - see week column logic below |
| `week_4_points` | [x] | ESPN API - see week column logic below |
| `week_5_points` | [x] | ESPN API - see week column logic below |
| `week_6_points` | [x] | ESPN API - see week column logic below |
| `week_7_points` | [x] | ESPN API - see week column logic below |
| `week_8_points` | [x] | ESPN API - see week column logic below |
| `week_9_points` | [x] | ESPN API - see week column logic below |
| `week_10_points` | [x] | ESPN API - see week column logic below |
| `week_11_points` | [x] | ESPN API - see week column logic below |
| `week_12_points` | [x] | ESPN API - see week column logic below |
| `week_13_points` | [x] | ESPN API - see week column logic below |
| `week_14_points` | [x] | ESPN API - see week column logic below |
| `week_15_points` | [x] | ESPN API - see week column logic below |
| `week_16_points` | [x] | ESPN API - see week column logic below |
| `week_17_points` | [x] | ESPN API - see week column logic below |

**Week Column Logic (RESOLVED):**
For `week_XX/players.csv` (file created at Week X):
- **Bye week:** Always `0`
- **Week < X:** Actual points from ESPN API (`statSourceId=0, appliedTotal`)
- **Week >= X:** Projected points from ESPN API (`statSourceId=1, appliedTotal`)

**Questions:**
- [x] For week N folder, should weeks N+1 through 17 be 0 or empty? → **Use projected points from ESPN API**
- [x] How do we distinguish bye week (0 points) from "future week" (no data yet)? → **Bye = 0, future = projected**
- [x] Source for injury_status historically? → **Default to "ACTIVE"**
- [x] ADP source? → **ESPN API `ownership.averageDraftPosition`**
- [x] player_rating calculation? → **Week 1: draft rank; Week 2+: fantasy_points ranking**

---

### 5. `simulation/sim_data/{YEAR}/weeks/week_NN/players_projected.csv`

**File-level decisions:**
- [x] Source: ESPN API (`statSourceId=1` for projections)
- [x] How to handle weeks where projections aren't available? → **Skip player entirely**

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `id` | [x] | ESPN API player ID |
| `name` | [x] | ESPN API `fullName` |
| `team` | [x] | ESPN API team (normalized) |
| `position` | [x] | ESPN API `defaultPositionId` mapped to string |
| `bye_week` | [x] | **From schedule file** - lookup team's bye week |
| `fantasy_points` | [x] | **Sum of week_1_points through week_17_points** |
| `injury_status` | [x] | **Default: "ACTIVE"** |
| `drafted` | [x] | **Default: 0** |
| `locked` | [x] | **Default: 0** |
| `average_draft_position` | [x] | **ESPN API** - `ownership.averageDraftPosition` field |
| `player_rating` | [x] | **ESPN API** - Week 1: draft rank normalized; Week 2+: fantasy_points ranking |
| `week_1_points` | [x] | See logic below |
| `week_2_points` | [x] | See logic below |
| `week_3_points` | [x] | See logic below |
| `week_4_points` | [x] | See logic below |
| `week_5_points` | [x] | See logic below |
| `week_6_points` | [x] | See logic below |
| `week_7_points` | [x] | See logic below |
| `week_8_points` | [x] | See logic below |
| `week_9_points` | [x] | See logic below |
| `week_10_points` | [x] | See logic below |
| `week_11_points` | [x] | See logic below |
| `week_12_points` | [x] | See logic below |
| `week_13_points` | [x] | See logic below |
| `week_14_points` | [x] | See logic below |
| `week_15_points` | [x] | See logic below |
| `week_16_points` | [x] | See logic below |
| `week_17_points` | [x] | See logic below |

**Week Column Logic (RESOLVED):**
For `week_XX/players_projected.csv` (file created at Week X):
- **Bye week:** Always `0`
- **Week < X:** Historical projection from ESPN API for that week (`statSourceId=1`)
- **Week >= X:** Current projection from ESPN API for Week X (`statSourceId=1`)

**Questions:**
- [x] For week N, use actual for weeks 1 to N-1, projected for N to 17? → **Use projections for all weeks (not actuals)**
- [x] Or just use projected values as they were at that point in time? → **Yes, historical projections for past, current projection for future**
- [x] ESPN API provides per-week projections? → **Yes, via `scoringPeriodId` parameter**
- [x] How to handle players with no projections? → **Skip player entirely**

---

## Data Source Summary

### Standardized: ESPN API Only

**Decision:** Use ESPN API as single data source for all player data.

| Data | ESPN API Field | Status |
|------|---------------|--------|
| Player names, IDs, teams, positions | Player info | ✓ Verified |
| Weekly actual fantasy points | `statSourceId=0, appliedTotal` | ✓ Verified |
| Weekly projected fantasy points | `statSourceId=1, appliedTotal` | ✓ Verified |
| ADP | `ownership.averageDraftPosition` | ✓ Verified |
| Draft rank (for Week 1 player_rating) | `draftRanksByRankType.PPR.rank` | ✓ Verified |
| Season schedule | ESPN scoreboard API | ✓ Verified |
| Bye weeks | Derived from schedule | ✓ Verified |

### Game Data (RESOLVED)
| Data | Source | Status |
|------|--------|--------|
| Game scores | ESPN Scoreboard API | ✓ Verified |
| Weather data | Open-Meteo Archive/Forecast API | ✓ Verified |
| Venue data | ESPN Scoreboard API | ✓ Verified |
| Game dates | ESPN Scoreboard API | ✓ Verified |

### Team Data (RESOLVED)
| Data | Source | Status |
|------|--------|--------|
| pts_allowed_to_* | Calculated from player fantasy points | ✓ Algorithm verified |
| points_scored | Sum of team's player fantasy points | ✓ Algorithm verified |
| points_allowed | Sum of opponent player fantasy points | ✓ Algorithm verified |

**All data sources resolved!**

---

## Calculation Logic Needed

- [x] **Bye week detection:** Teams missing from week's schedule = bye week (from ESPN API)
- [x] **Team defense stats:** Aggregate player fantasy points by opponent (reuse `espn_client.py` algorithm)
- [x] **Player rating:** Week 1 = draft rank normalized; Week 2+ = fantasy_points ranking (position-specific 1-100)
- [x] **Fantasy points total:** Sum of week_1_points through week_17_points
- [x] **Cumulative stats:** Sum actual points for weeks < X, use projections for weeks >= X

**All calculation logic resolved!**

---

## Team Abbreviation Handling (VERIFIED)

**Canonical 32-team abbreviation list:**
```
ARI, ATL, BAL, BUF, CAR, CHI, CIN, CLE, DAL, DEN, DET, GB,
HOU, IND, JAX, KC, LAC, LAR, LV, MIA, MIN, NE, NO, NYG,
NYJ, PHI, PIT, SEA, SF, TB, TEN, WSH
```

**API Consistency (Tested Dec 2024):**
- [x] ESPN Scoreboard API returns WSH for Washington (all years 2021+)
- [x] ESPN Fantasy API returns numeric `proTeamId` → mapped via `ESPN_TEAM_MAPPINGS`
- [x] All 32 teams have identical abbreviations across 2021-2024
- [x] No year-specific variations found

**Normalization (if needed):**
```python
def normalize_team(abbrev: str) -> str:
    return 'WSH' if abbrev == 'WAS' else abbrev
```

**Key Mappings:**
| Team | proTeamId | Abbreviation |
|------|-----------|--------------|
| Washington | 28 | WSH |
| LA Chargers | 24 | LAC |
| LA Rams | 14 | LAR |
| Las Vegas | 13 | LV |

---

## Testing & Validation

- [ ] Compare output format with existing sim_data structure
- [ ] Validate player counts per position
- [ ] Validate week counts (16 or 17)
- [ ] Spot-check specific player stats against source
- [ ] Verify bye weeks are correctly identified
- [ ] Verify team abbreviations match (WSH vs WAS, LAR vs LA, etc.)
