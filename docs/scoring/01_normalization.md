# Normalization (Step 1)

## Overview

**Type**: Base Score Calculation (0-N scale)
**Effect**: Establishes base score from raw fantasy point projections
**When Applied**: Step 1 of 10-step scoring algorithm
**Purpose**: Convert raw fantasy points to normalized comparable scale across all players

Normalization is the foundational step that converts raw fantasy point projections into a standardized 0-N scale. This allows fair comparison between players regardless of absolute projection values. A player with 300 projected points and a player with 50 projected points are normalized relative to the maximum projection in the player pool (typically 400+), creating a level playing field for subsequent multipliers and bonuses.

**Key Characteristics**:
- **First step**: All other scoring steps build on this normalized base
- **Flexible projection source**: Uses either weekly projection OR rest-of-season projection
- **Max-based scaling**: Normalizes relative to highest projection in player pool
- **Position-agnostic**: All positions normalized using same max projection value
- **Configurable scale**: NORMALIZATION_MAX_SCALE parameter controls output range

**Formula**:
```
normalized_score = (raw_projection / max_projection) * NORMALIZATION_MAX_SCALE
```

**Implementation**: `league_helper/util/player_scoring.py:464-483, 134-144`

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: Yes (always, Step 1)
**Projection Type**: Rest-of-Season (ROS)
**Why**: Draft decisions require season-long value assessment. ROS projections capture total remaining value from current week through week 17.

**Example**: Week 9 draft evaluation
- Player A: 180 ROS points (weeks 9-17) → normalized to 47.3 pts
- Player B: 80 ROS points (weeks 9-17) → normalized to 21.0 pts
- Normalization provides comparable base scores for subsequent multipliers

### Starter Helper Mode (Roster Optimizer)
**Enabled**: Yes (always, Step 1)
**Projection Type**: Weekly (single week)
**Why**: Lineup decisions focus on immediate performance. Weekly projections capture expected points for upcoming matchup only.

**Example**: Week 9 lineup decision
- QB1: 22.5 weekly projection → normalized to 5.9 pts
- QB2: 18.0 weekly projection → normalized to 4.7 pts
- Normalized scores used to compare this week's expected value

### Trade Simulator Mode
**Enabled**: Yes (always, Step 1)
**Projection Type**: Rest-of-Season (ROS)
**Why**: Trade decisions evaluate season-long value exchange. ROS projections show remaining value for trade comparison.

**Example**: Week 9 trade evaluation
- Receiving: WR with 150 ROS pts → normalized to 39.4 pts
- Giving: RB with 140 ROS pts → normalized to 36.8 pts
- Normalized values form basis for roster value comparison

---

## How League Helper Gets the Value/Multiplier

### Step 1: Determine Projection Type

**Method**: `PlayerScoringCalculator._get_normalized_fantasy_points()`
**File**: `league_helper/util/player_scoring.py:464-483`

```python
def _get_normalized_fantasy_points(self, p: FantasyPlayer, use_weekly_projection: bool) -> Tuple[float, str]:
    """
    Get normalized fantasy points (Step 1).

    Args:
        p: Player to score
        use_weekly_projection: If True, use weekly projection; if False, use ROS

    Returns:
        Tuple[float, str]: (normalized_score, reason_string)
    """
    # Determine which projection type to use
    if use_weekly_projection:
        # Use projection for current week only (for weekly recommendations)
        orig_pts, weighted_pts = self.get_weekly_projection(p)
    else:
        # Use rest-of-season projection (for season-long evaluation)
        # This sums all remaining weeks from current week through week 17
        orig_pts = p.get_rest_of_season_projection(self.config.current_nfl_week)
        # Normalize to 0-N scale for comparability across all players
        if self.max_projection > 0:
            weighted_pts = self.weight_projection(orig_pts)
        else:
            weighted_pts = 0.0

    # Format reason string showing both raw and normalized values
    reason = f"Projected: {orig_pts:.2f} pts, Weighted: {weighted_pts:.2f} pts"
    return weighted_pts, reason
```

**Key Logic**:
1. **Mode check**: `use_weekly_projection` flag determines projection type
2. **Weekly path**: Calls `get_weekly_projection()` which handles weekly normalization internally
3. **ROS path**: Gets ROS projection from player, normalizes using `weight_projection()`
4. **Safety**: Checks for zero max_projection to avoid division by zero
5. **Reason string**: Returns both raw and normalized values for transparency

### Step 2: Get Weekly Projection (if weekly mode)

**Method**: `PlayerScoringCalculator.get_weekly_projection()`
**File**: `league_helper/util/player_scoring.py:86-132`

```python
def get_weekly_projection(self, player: FantasyPlayer, week=0) -> Tuple[float, float]:
    """
    Get weekly projection for a specific player and week.

    Args:
        player: Player to get projection for
        week: NFL week number (1-17). If 0, uses current_nfl_week

    Returns:
        Tuple[float, float]: (original_points, weighted_points)
            - original_points: Raw fantasy points projection for the week
            - weighted_points: Normalized projection (0-N scale)
            - Returns (0.0, 0.0) if no valid projection data exists
    """
    # If week isn't in the valid range (1-17), use current week from config
    if week not in range(1, 18):
        week = self.config.current_nfl_week

    weekly_points = player.get_single_weekly_projection(week)
    if weekly_points is not None and float(weekly_points) > 0:
        weekly_points = float(weekly_points)
        # Calculate normalized/weighted projection using same scale as seasonal projections
        if self.max_projection > 0:
            weighted_projection = self.weight_projection(weekly_points)
        else:
            weighted_projection = 0.0
        return weekly_points, weighted_projection

    # Return zeros if no valid projection found
    return 0.0, 0.0
```

### Step 3: Calculate Normalized Score

**Method**: `PlayerScoringCalculator.weight_projection()`
**File**: `league_helper/util/player_scoring.py:136-168`

```python
def weight_projection(self, pts: float, use_weekly_max: bool = False) -> float:
    """
    Calculate weighted projection using normalization scale.

    Args:
        pts (float): Raw fantasy points
        use_weekly_max (bool): If True, use max_weekly_projection for normalization.
                               If False, use max_projection (ROS). Default: False.

    Returns:
        float: Weighted projection (0-N scale)
    """
    chosen_max = self.max_weekly_projection if use_weekly_max else self.max_projection

    if chosen_max == 0:
        # Safety check for data quality issues
        return 0.0

    return (pts / chosen_max) * self.config.normalization_max_scale
```

The `max_weekly_projection` is calculated on-demand and cached in `PlayerManager.max_weekly_projections` dict. Starter Helper mode sets this before scoring players each week.

**Complete Flow**:
```
Player (fantasy_points=180.0 or week_9_points=22.5)
    ↓
Determine projection type (ROS vs Weekly)
    ↓
Get raw projection value
    ↓
weight_projection(180.0) → (180.0 / 380.0) * 105.01 = 49.74
    ↓
Return (raw=180.0, normalized=49.74)
```

---

## Single-Week vs ROS Normalization

League Helper uses different normalization denominators depending on the scoring mode. **Starter Helper mode** (weekly lineup optimization) normalizes against the maximum single-week projection for that specific week, ensuring weekly scores use the full 0-N scale. **Draft Helper and Trade Simulator modes** normalize against the maximum rest-of-season (ROS) projection across all players.

**Example**: If the top weekly projection for Week 10 is 30 points and the top ROS projection is 400 points, a player with 25 weekly points would score `(25/30) * 100 = 83.3` in Starter Helper mode vs `(25/400) * 100 = 6.25` in Draft Helper mode. This allows weekly scores to be more differentiated and comparable within the week while preserving season-long value assessment for draft/trade decisions.

---

## Calculations Involved

### Formula Breakdown

**Normalization Formula**:
```
normalized_score = (raw_projection / max_projection) * NORMALIZATION_MAX_SCALE

Where:
- raw_projection: Player's fantasy points (ROS or weekly)
- max_projection: Highest fantasy points among all players
- NORMALIZATION_MAX_SCALE: Configuration parameter (typically ~105)
```

**Rest-of-Season (ROS) Projection**:
```
ros_projection = sum(week_N_points for N in [CURRENT_NFL_WEEK, 17])

Example (current week 9):
ros_projection = week_9_points + week_10_points + ... + week_17_points
```

**Weekly Projection**:
```
weekly_projection = week_N_points

Example (current week 9):
weekly_projection = week_9_points
```

### Example Calculation (ROS Mode)

**Player**: Amon-Ra St. Brown (WR, DET)
**Current Week**: 9
**Config**: NORMALIZATION_MAX_SCALE=105.01, max_projection=380.45

**Step 1: Calculate ROS projection**
```
ROS = week_9 + week_10 + week_11 + week_12 + week_13 + week_14 + week_15 + week_16 + week_17
ROS = 18.7 + 22.34 + 20.82 + 20.90 + 20.14 + 21.98 + 19.78 + 20.27 + 21.09
ROS = 186.02 points
```

**Step 2: Calculate normalized score**
```
normalized = (186.02 / 380.45) * 105.01
normalized = 0.4890 * 105.01
normalized = 51.35 points
```

**Result**: Amon-Ra St. Brown's base score is 51.35 (before any multipliers/bonuses)

### Example Calculation (Weekly Mode)

**Player**: Josh Allen (QB, BUF)
**Week**: 9
**Config**: NORMALIZATION_MAX_SCALE=105.01, max_projection=380.45

**Step 1: Get weekly projection**
```
weekly = week_9_points
weekly = 28.82 points
```

**Step 2: Calculate normalized score**
```
normalized = (28.82 / 380.45) * 105.01
normalized = 0.0758 * 105.01
normalized = 7.96 points
```

**Result**: Josh Allen's base score for week 9 is 7.96 (before any multipliers/bonuses)

### Top-Tier Player Example

**Player**: Christian McCaffrey (RB, SF)
**Current Week**: 9
**ROS Projection**: 189.46 points (weeks 9-17)

**Calculation**:
```
normalized = (189.46 / 380.45) * 105.01
normalized = 0.4980 * 105.01
normalized = 52.30 points
```

**Analysis**: CMC receives highest base score due to highest ROS projection

### Mid-Tier Player Example

**Player**: Josh Jacobs (RB, GB)
**Current Week**: 9
**ROS Projection**: 152.66 points (weeks 9-17)

**Calculation**:
```
normalized = (152.66 / 380.45) * 105.01
normalized = 0.4013 * 105.01
normalized = 42.14 points
```

**Analysis**: Mid-tier RB receives proportionally lower base score

### Low-Tier Player Example

**Player**: Cameron Dicker (K, LAC)
**Current Week**: 9
**ROS Projection**: 61.13 points (weeks 9-17)

**Calculation**:
```
normalized = (61.13 / 380.45) * 105.01
normalized = 0.1607 * 105.01
normalized = 16.87 points
```

**Analysis**: Kickers typically have much lower base scores due to lower raw projections

---

## Data Sources (players.csv Fields)

### Required Fields

| Field Name | Data Type | Description | Valid Range | Example Values |
|------------|-----------|-------------|-------------|----------------|
| `fantasy_points` | float | Total rest-of-season projected fantasy points | 0.0 - 500.0 | 167.32, 189.46, 61.13 |
| `week_1_points` | float | Projected fantasy points for Week 1 | 0.0 - 60.0 | 8.5, 23.2, 9.0 |
| `week_2_points` | float | Projected fantasy points for Week 2 | 0.0 - 60.0 | 39.2, 22.7, 8.0 |
| ... | ... | ... | ... | ... |
| `week_17_points` | float | Projected fantasy points for Week 17 | 0.0 - 60.0 | 21.09, 29.67, 8.33 |

**Note**: Week fields exist for weeks 1-17 (full NFL regular season)

### Field Specifications

**`fantasy_points`**:
- **Type**: float
- **Source**: ESPN API `player.stats[0].appliedTotal` (season-long projection)
- **Range**: 0.0 to ~500.0 (elite QBs can reach 400+)
- **Calculation**: Sum of all weekly projections OR season-total projection from ESPN
- **Update frequency**: Updated daily with latest ESPN projections
- **Null handling**: Defaults to 0.0 if missing

**`week_N_points`** (N = 1 to 17):
- **Type**: float (nullable)
- **Source**: ESPN API `player.stats[week].projectedTotal` OR `appliedTotal`
- **Range**: 0.0 to ~60.0 (typical max, QBs can occasionally exceed)
- **Update frequency**: Updated weekly before games
- **Null handling**: Treated as 0.0 in ROS calculations
- **Bye weeks**: Typically show as 0.0 or None

**Special Cases**:
- **Past weeks**: May contain actual points instead of projections (statSourceId=1)
- **Future weeks**: Contain projected points (statSourceId=0)
- **Current week**: Updates from projection to actual after games complete
- **Injured players**: May have 0.0 projections for affected weeks

---

## How player-data-fetcher Populates Data

### Data Collection Process

**Main Script**: `player-data-fetcher/player_data_fetcher_main.py`
**ESPN Client**: `player-data-fetcher/espn_client.py`
**Points Calculator**: `player-data-fetcher/fantasy_points_calculator.py`
**Exporter**: `player-data-fetcher/player_data_exporter.py`
**Frequency**: Daily (typically run before draft or weekly updates)

### Fantasy Points Extraction

**Step 1: Fetch player projections from ESPN API**

```python
# File: player-data-fetcher/espn_client.py:696-726

async def get_season_projections(self, season: Optional[int] = None) -> List[ESPNPlayerData]:
    """
    Get season projections from ESPN.

    Args:
        season: Optional season year (defaults to settings.season if not provided).
               Use season=2024 to fetch historical data for simulation validation.

    Returns:
        List of player data with projections
    """
    ppr_id = self._get_ppr_id()
    use_season = season if season is not None else self.settings.season

    self.logger.info(f"Fetching season projections for {use_season}")

    # ESPN's main fantasy API endpoint for player projections
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{use_season}/segments/0/leaguedefaults/{ppr_id}"

    params = {
        "view": "kona_player_info",
        "scoringPeriodId": 0  # 0 = season projections
    }

    headers = {
        'User-Agent': ESPN_USER_AGENT,
        'X-Fantasy-Filter': f'{{"players":{{"limit":{ESPN_PLAYER_LIMIT},"sortPercOwned":{{"sortPriority":4,"sortAsc":false}}}}}}'
    }

    data = await self._make_request("GET", url, params=params, headers=headers)
    return await self._parse_espn_data(data)
```

**Step 2: Calculate ROS projection from weekly data**

```python
# File: player-data-fetcher/espn_client.py:394-434

async def _calculate_week_by_week_projection(self, player_id: str, name: str, position: str) -> float:
    """Calculate remaining season projection by summing current + future week projections"""

    try:
        # Get all weekly data for this player in a single optimized call
        all_weeks_data = await self._get_all_weeks_data(player_id, position)
        if not all_weeks_data:
            return 0.0

        # Only calculate for remaining season (current week + future weeks)
        end_week = 17
        start_week = CURRENT_NFL_WEEK

        total_projection = 0.0
        weeks_processed = 0

        for week in range(start_week, end_week + 1):
            week_points = None

            # Extract week points using standardized logic (always prefers actual over projected)
            week_points = self._extract_week_points(all_weeks_data, week, position=position, player_name=name)

            # Determine data type for logging (current week = current, future weeks = projected)
            if week == CURRENT_NFL_WEEK:
                data_type = 'current'
            else:
                data_type = 'projected'

            if week_points > 0:
                total_projection += week_points
                weeks_processed += 1
                self.logger.debug(f"{name} Week {week}: {week_points:.1f} points ({data_type})")

        if weeks_processed > 0:
            self.logger.debug(f"Remaining season projection for {name}: {total_projection:.1f} points ({weeks_processed} weeks)")
            return total_projection

    except Exception as e:
        self.logger.warning(f"Week-by-week calculation failed for {name}: {e}")

    return 0.0
```

**Step 3: Populate weekly projections**

```python
# File: player-data-fetcher/espn_client.py:533-572

async def _populate_weekly_projections(self, player_data: ESPNPlayerData, player_id: str, name: str, position: str):
    """
    Populate weekly projections for a player if week-by-week projections are enabled

    Args:
        player_data: The ESPNPlayerData object to populate
        player_id: ESPN player ID
        name: Player name for logging
        position: Player position
    """
    # Week-by-week projections are always enabled

    try:
        # Get all weekly data for this player
        all_weeks_data = await self._get_all_weeks_data(player_id, position)
        if not all_weeks_data:
            return

        # Determine week range (limit to 17 for fantasy regular season)
        end_week = 17

        # Collect weekly projections for all weeks
        for week in range(1, end_week + 1):
            # Get raw points from ESPN data without fallbacks
            espn_points = self._extract_raw_espn_week_points(all_weeks_data, week, position)

            if espn_points is not None and (espn_points > 0 or position == 'DST'):
                player_data.set_week_points(week, espn_points)
                self.logger.debug(f"{name} Week {week}: {espn_points:.1f} points (ESPN data)")
            else:
                # Set to 0.0 when no ESPN data available (likely bye week for DST teams)
                player_data.set_week_points(week, 0.0)
                if position == 'DST':
                    self.logger.debug(f"{name} Week {week}: 0.0 points (likely bye week)")
                else:
                    self.logger.debug(f"{name} Week {week}: 0.0 points (no data)")

    except Exception as e:
        self.logger.warning(f"Failed to populate weekly projections for {name}: {str(e)}")
```

**Step 4: Write to players.csv**

```python
# File: player-data-fetcher/player_data_exporter.py:336-358

# Create FantasyPlayer object with all fields
fantasy_player = FantasyPlayer(
    id=player_data.id,
    name=player_data.name,
    team=player_data.team,
    position=player_data.position,
    bye_week=player_data.bye_week,
    drafted=drafted_value,
    locked=locked_value,
    fantasy_points=player_data.fantasy_points,
    average_draft_position=player_data.average_draft_position,
    # Enhanced scoring fields
    player_rating=player_data.player_rating,
    injury_status=player_data.injury_status,
    # Weekly projections (weeks 1-17 fantasy regular season only)
    week_1_points=player_data.week_1_points,
    week_2_points=player_data.week_2_points,
    week_3_points=player_data.week_3_points,
    week_4_points=player_data.week_4_points,
    week_5_points=player_data.week_5_points,
    week_6_points=player_data.week_6_points,
    week_7_points=player_data.week_7_points,
    week_8_points=player_data.week_8_points,
    week_9_points=player_data.week_9_points,
    week_10_points=player_data.week_10_points,
    week_11_points=player_data.week_11_points,
    week_12_points=player_data.week_12_points,
    week_13_points=player_data.week_13_points,
    week_14_points=player_data.week_14_points,
    week_15_points=player_data.week_15_points,
    week_16_points=player_data.week_16_points,
    week_17_points=player_data.week_17_points
)
```

### Max Projection Calculation

**Method**: `PlayerManager.load_players_from_csv()`
**File**: `league_helper/util/PlayerManager.py:135-243`

```python
def load_players_from_csv(self) -> None:
    """
    Load players from CSV file using the new FantasyPlayer class.

    This function now supports the new projection data format with fantasy_points
    and can fall back to the legacy format if needed.
    """
    players: list[FantasyPlayer] = []
    self.max_projection = 0.0

    # Define required columns for basic player data
    required_columns = ['id', 'name', 'team', 'position']

    # ... (CSV loading and validation code) ...

    # Track maximum projection across all players for normalization
    # This is used as the denominator when calculating weighted projections
    if player.fantasy_points and player.fantasy_points > self.max_projection:
        self.max_projection = player.fantasy_points

    # ... (continue loading players) ...

    # Update the scoring calculator with the final maximum projection
    # This is needed for normalization calculations in score_player()
    self.scoring_calculator.max_projection = self.max_projection

    self.logger.info(f"Loaded {len(players)} players from CSV, max projection: {self.max_projection:.2f}")
```

---

## ESPN API JSON Analysis

### Season-Long Projection Data Structure

**API Endpoint**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{leagueId}`

**View Parameters**: `kona_player_info`, `players_wl`

**Relevant JSON Path**: `player.stats[]`

### JSON Structure (Season-Long)

```json
{
  "id": 4374302,
  "fullName": "Amon-Ra St. Brown",
  "proTeamId": 8,
  "defaultPositionId": 4,
  "stats": [
    {
      "id": "004374302",
      "seasonId": 2025,
      "scoringPeriodId": 0,
      "statSourceId": 0,
      "statSplitTypeId": 0,
      "appliedTotal": 167.32,
      "appliedStats": {
        "53": 100.0,
        "42": 67.32
      }
    }
  ]
}
```

### JSON Structure (Weekly Projections)

```json
{
  "id": 4374302,
  "fullName": "Amon-Ra St. Brown",
  "stats": [
    {
      "id": "004374302",
      "seasonId": 2025,
      "scoringPeriodId": 9,
      "statSourceId": 0,
      "statSplitTypeId": 1,
      "appliedTotal": 18.7,
      "appliedStats": {
        "53": 6.5,
        "42": 12.2
      }
    },
    {
      "id": "004374302",
      "scoringPeriodId": 10,
      "statSourceId": 0,
      "appliedTotal": 22.34,
      "appliedStats": { /* Week 10 projection */ }
    }
    // ... more weeks ...
  ]
}
```

### Field Mapping

| JSON Field | Type | Description | Example Value |
|------------|------|-------------|---------------|
| `stats[].scoringPeriodId` | int | Week number (0=season, 1-17=weeks) | 0, 9, 10, 17 |
| `stats[].statSourceId` | int | 0=projected, 1=actual | 0 |
| `stats[].appliedTotal` | float | Total fantasy points (scoring format applied) | 167.32, 18.7, 22.34 |
| `stats[].appliedStats` | object | Individual stat categories with points | {"53": 100.0, "42": 67.32} |

**Key Distinction**: `scoringPeriodId`
- **0**: Season-long projection (total for all weeks)
- **1-17**: Individual week projections

### Extraction Logic

```python
# File: player-data-fetcher/fantasy_points_calculator.py:103-194

def _extract_from_stats_array(
    self,
    player_data: Dict[str, Any],
    week: int,
    position: str,
    current_nfl_week: Optional[int] = None
) -> Optional[float]:
    """
    Extract fantasy points from ESPN stats array

    Standardized logic: appliedTotal (actual) → projectedTotal (projected) → None

    Args:
        player_data: ESPN player data dictionary
        week: Target week number
        position: Player position for validation
        current_nfl_week: Current NFL week for prioritizing actual vs projected data

    Returns:
        Fantasy points if found, None if not available
    """
    try:
        stats = player_data.get('player', {}).get('stats', [])

        if not stats:
            self.logger.debug("No stats array found in player data")
            return None

        for stat in stats:
            # Validate stat entry structure
            if not isinstance(stat, dict):
                continue

            season_id = stat.get('seasonId')
            scoring_period = stat.get('scoringPeriodId')
            stat_entry = stat  # ESPN data has appliedTotal/projectedTotal directly in stat, not nested

            # Only use current season data - no historical fallback
            if scoring_period == week and season_id == self.season:
                points = None

                # WEEK-BASED PRIORITY LOGIC:
                # Past weeks (week < current): appliedTotal → projectedTotal
                # Current/Future weeks (week >= current): projectedTotal → appliedTotal
                # Legacy behavior (when current_nfl_week is None): appliedTotal → projectedTotal

                if current_nfl_week is not None:
                    if week < current_nfl_week:
                        # Past weeks: prefer appliedTotal (actual scores)
                        if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                            points = float(stat_entry['appliedTotal'])
                            self.logger.debug(f"Found appliedTotal for past week {week}: {points}")
                        elif 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                            points = float(stat_entry['projectedTotal'])
                            self.logger.debug(f"Found projectedTotal fallback for past week {week}: {points}")
                    else:
                        # Current/Future weeks: prefer projectedTotal (projected scores)
                        if 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                            points = float(stat_entry['projectedTotal'])
                            self.logger.debug(f"Found projectedTotal for current/future week {week}: {points}")
                        elif 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                            points = float(stat_entry['appliedTotal'])
                            self.logger.debug(f"Found appliedTotal fallback for current/future week {week}: {points}")
                else:
                    # Legacy behavior: prefer appliedTotal (for backward compatibility)
                    if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                        points = float(stat_entry['appliedTotal'])
                        self.logger.debug(f"Found appliedTotal (legacy mode): {points}")
                    elif 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                        points = float(stat_entry['projectedTotal'])
                        self.logger.debug(f"Found projectedTotal fallback (legacy mode): {points}")

                # Validate points (handle negative points based on position and config)
                if points is not None:
                    if points < 0:
                        # Handle negative points
                        if position == 'DST' and self.config.include_negative_dst_points:
                            # Allow negative DST points if configured
                            return points
                        else:
                            # Skip negative points for non-DST or when DST negatives disabled
                            self.logger.debug(f"Skipping negative points {points} for {position} position")
                            continue
                    else:
                        # Non-negative points are always allowed
                        return points

        # No current season data found
        return None

    except (ValueError, TypeError, KeyError) as e:
        self.logger.warning(f"Error parsing stats array: {str(e)}")
        return None
```

**Sample Extraction** (Amon-Ra St. Brown):

```python
# Input JSON (filtered for statSourceId=0)
stats_projected = [
    {"scoringPeriodId": 0, "statSourceId": 0, "appliedTotal": 167.32},
    {"scoringPeriodId": 9, "statSourceId": 0, "appliedTotal": 18.7},
    {"scoringPeriodId": 10, "statSourceId": 0, "appliedTotal": 22.34},
    {"scoringPeriodId": 11, "statSourceId": 0, "appliedTotal": 20.82}
]

# Output mapping
projections = {
    "fantasy_points": 167.32,
    "week_9_points": 18.7,
    "week_10_points": 22.34,
    "week_11_points": 20.82
}

# Written to players.csv row
"4374302,Amon-Ra St. Brown,DET,WR,8,167.32,ACTIVE,1,1,12.01,89.33,8.5,39.2,20.7,..."
```

---

## Examples with Walkthroughs

### Example 1: Elite RB (Christian McCaffrey) - ROS Mode

**Scenario**: Week 9, evaluating RB Christian McCaffrey for draft
**Player Data**:
- Position: RB
- Team: SF
- Bye Week: 14 (already occurred in previous weeks data)

**Step 1: Get ROS projection** (weeks 9-17)
```
ROS = sum(week_9 through week_17 projections)
ROS = 34.3 + 24.41 + 26.35 + 27.00 + 26.19 + 0.0 + 30.09 + 25.75 + 29.67
ROS = 223.76 points (note: week 14 is 0.0 for bye)
```

**Step 2: Calculate normalized score**
```
Config: NORMALIZATION_MAX_SCALE = 105.01
Config: max_projection = 380.45 (highest among all players)

normalized = (223.76 / 380.45) * 105.01
normalized = 0.5882 * 105.01
normalized = 61.76 points
```

**Step 3: Format reason string**
```
reason = "Projected: 223.76 pts, Weighted: 61.76 pts"
```

**Result**: CMC receives highest base score of 61.76, reflecting elite ROS value

---

### Example 2: Top WR (Amon-Ra St. Brown) - ROS Mode

**Scenario**: Week 9, evaluating WR Amon-Ra St. Brown
**Player Data**:
- Position: WR
- Team: DET
- Bye Week: 8 (already occurred)

**Step 1: Get ROS projection** (weeks 9-17)
```
ROS = 18.7 + 22.34 + 20.82 + 20.90 + 20.14 + 21.98 + 19.78 + 20.27 + 21.09
ROS = 186.02 points
```

**Step 2: Calculate normalized score**
```
normalized = (186.02 / 380.45) * 105.01
normalized = 0.4890 * 105.01
normalized = 51.35 points
```

**Result**: Top-tier WR receives 51.35 base score, ~17% lower than elite RB

---

### Example 3: Kicker (Cameron Dicker) - ROS Mode

**Scenario**: Week 9, evaluating K Cameron Dicker
**Player Data**:
- Position: K
- Team: LAC

**Step 1: Get ROS projection** (weeks 9-17)
```
ROS = 11.0 + 8.76 + 8.79 + 0.0 + 9.04 + 8.63 + 8.41 + 9.17 + 8.33
ROS = 72.13 points (note: week 12 is 0.0 for bye)
```

**Step 2: Calculate normalized score**
```
normalized = (72.13 / 380.45) * 105.01
normalized = 0.1896 * 105.01
normalized = 19.90 points
```

**Result**: Kicker receives much lower base score (19.90) due to inherently lower scoring potential

---

### Example 4: Elite QB (Josh Allen) - Weekly Mode

**Scenario**: Week 9, optimizing lineup for current week
**Player Data**:
- Position: QB
- Team: BUF
- Week 9 Projection: 28.82 points

**Step 1: Get weekly projection**
```
weekly = week_9_points
weekly = 28.82 points
```

**Step 2: Calculate normalized score**
```
normalized = (28.82 / 380.45) * 105.01
normalized = 0.0758 * 105.01
normalized = 7.96 points
```

**Result**: Weekly normalized score of 7.96 for this week's lineup decision

---

### Example 5: Mid-Tier RB (Josh Jacobs) - ROS Mode

**Scenario**: Week 9, evaluating RB Josh Jacobs
**Player Data**:
- Position: RB
- Team: GB
- Bye Week: 5 (already occurred)

**Step 1: Get ROS projection** (weeks 9-17)
```
ROS = 20.0 + 18.10 + 21.11 + 19.37 + 17.77 + 20.83 + 15.75 + 20.34 + 19.38
ROS = 172.65 points
```

**Step 2: Calculate normalized score**
```
normalized = (172.65 / 380.45) * 105.01
normalized = 0.4538 * 105.01
normalized = 47.65 points
```

**Result**: Solid RB2 receives 47.65 base score, between elite (61+) and low-tier (20-30)

---

### Example 6: Zero Projection Handling

**Scenario**: Week 9, injured player with no projections
**Player Data**:
- Position: WR
- Injury Status: OUT
- All weekly projections: 0.0 or None

**Step 1: Get ROS projection**
```
ROS = 0.0 + 0.0 + ... + 0.0
ROS = 0.0 points
```

**Step 2: Calculate normalized score**
```
normalized = (0.0 / 380.45) * 105.01
normalized = 0.0 * 105.01
normalized = 0.0 points
```

**Result**: Injured player with no projections receives 0.0 base score, effectively removing them from consideration (before injury penalty applied in Step 10)

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "NORMALIZATION_MAX_SCALE": 105.01467963908847
}
```

### Configuration Fields

| Field | Type | Description | Current Value |
|-------|------|-------------|---------------|
| `NORMALIZATION_MAX_SCALE` | float | Maximum value on normalized scale | 105.01 |

**Note**: No thresholds or multipliers for normalization - it's a direct linear scaling calculation.

### Scale Interpretation

**Current Scale**: 0 to 105.01

**Typical Score Ranges** (ROS mode, week 9):
- **Elite players (Top 5)**: 55-65 points
- **Tier 1 starters (Top 25)**: 45-55 points
- **Tier 2 starters (Top 50)**: 35-45 points
- **Flex/Bench players**: 25-35 points
- **Deep bench/streamers**: 15-25 points
- **Low-value players**: 5-15 points
- **No-value players**: 0-5 points

### Max Projection Calculation

**Determination**: Calculated at runtime from player pool

**Method**:
```python
max_projection = max(player.fantasy_points for player in all_players)
```

**Typical Values**:
- **Early season (Week 1)**: ~400 points (elite QB full season)
- **Mid season (Week 9)**: ~220-240 points (9 weeks remaining)
- **Late season (Week 15)**: ~60-80 points (3 weeks remaining)

**Impact**: Max projection decreases as season progresses, keeping normalized scores comparable week-to-week.

### Configuration Tuning Guide

**Increasing Scale**:
- Increase `NORMALIZATION_MAX_SCALE` (e.g., 150.0, 200.0)
- Effect: Higher base scores, multipliers have larger absolute impact
- Use case: When multiplier/bonus effects seem too small

**Decreasing Scale**:
- Decrease `NORMALIZATION_MAX_SCALE` (e.g., 75.0, 50.0)
- Effect: Lower base scores, multipliers have smaller absolute impact
- Use case: When multiplier/bonus effects seem too large

**Why Current Value (105.01)?**:
- Optimized through simulation to balance base scores with multiplier effects
- Creates intuitive score ranges (0-100+ scale)
- Allows meaningful point differences between tiers

---

## See Also

### Related Metrics
- **[02_adp_multiplier.md](02_adp_multiplier.md)** - First multiplier applied to normalized base
- **[03_player_rating_multiplier.md](03_player_rating_multiplier.md)** - Expert consensus adjustment
- **[05_performance_multiplier.md](05_performance_multiplier.md)** - Historical performance adjustment

### Implementation Files
- **`league_helper/util/player_scoring.py:464-483`** - Normalization calculation
- **`league_helper/util/player_scoring.py:86-132`** - Weekly projection retrieval
- **`league_helper/util/player_scoring.py:134-144`** - Weight projection helper
- **`league_helper/util/PlayerManager.py:150-200`** - Max projection calculation
- **`utils/FantasyPlayer.py:96`** - fantasy_points field definition

### Configuration
- **`data/league_config.json`** - NORMALIZATION_MAX_SCALE parameter
- **`data/players.csv`** - fantasy_points and week_N_points fields

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - Normalization tests
- **`tests/league_helper/util/test_PlayerManager.py`** - Max projection calculation tests

### Documentation
- **[README.md](README.md)** - Scoring algorithm overview
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 9
**Documentation Version**: 1.0
**Code Version**: Week 9, 2025 NFL Season
