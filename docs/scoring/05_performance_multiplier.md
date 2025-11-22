# Performance Multiplier (Step 5)

## Overview

**Type**: Multiplicative (percentage adjustment)
**Effect**: ±1.0% (0.990x to 1.010x with default weight=0.20)
**Base Multipliers**: 0.95x to 1.05x (±5% before weight exponent)
**When Applied**: Step 5 of 10-step scoring algorithm
**Purpose**: Reward players who consistently outperform projections, penalize underperformers

The Performance Multiplier evaluates how a player's actual fantasy points compare to their weekly projections over the season. Players who consistently exceed projections receive a boost (up to 1.05x), while those who underperform receive a penalty (down to 0.95x). This metric captures execution quality and reliability beyond raw statistical projections.

**Key Characteristics**:
- **Rolling window**: Uses only the last MIN_WEEKS weeks (not entire season) for recent performance trends
- **Minimum data requirement**: MIN_WEEKS serves as both window size AND minimum required weeks (default: 3)
- **Position exclusions**: DST players excluded (insufficient projection data)
- **Week filtering**: Only analyzes the rolling window of recent completed weeks
- **Smart skipping**: Ignores weeks where player didn't play (actual=0) or projections missing

**Formula**:
```
Average Deviation = mean((actual_points - projected_points) / projected_points) for all valid weeks
Multiplier = lookup deviation in thresholds → apply weight exponent
```

**Implementation**: `league_helper/util/player_scoring.py:206-301, 521-555`

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: No (`performance=False`)
**Why**: Draft decisions rely on ROS projections and expert consensus (player_rating), not historical actual vs projected trends. Early in the season, performance data is limited. Mid-season, performance trends are already incorporated into updated projections.

**Rationale**: Performance deviation measures "has this player beaten projections in past weeks?" This is most useful for weekly lineup decisions (hot/cold streaks). For draft strategy, ADP and player_rating already capture market consensus about which players outperform expectations.

### Starter Helper Mode (Roster Optimizer)
**Enabled**: Yes (`performance=True`)
**Why**: Recent performance trends inform weekly lineup decisions. A player trending hot (beating projections) may be a better start than a cold player even with similar projections.

**Example**: Choosing between two WRs for FLEX spot:
- WR1: Projected 15.0 pts, averaging +20% above projections last 4 weeks
- WR2: Projected 16.0 pts, averaging -15% below projections last 4 weeks
- Performance multiplier may favor WR1 despite lower projection

### Trade Simulator Mode
**Enabled**: Yes (`performance=True`)
**Why**: Performance trends affect player valuation in trades. Acquiring a player who consistently beats projections provides better ROS value than projections alone suggest.

**Example**: Evaluating trade offer:
- Receiving: WR projected 150 ROS pts, +25% performance deviation (EXCELLENT)
- Giving: WR projected 160 ROS pts, -20% performance deviation (VERY_POOR)
- Performance multiplier helps recognize the trade value despite lower projection

---

## How League Helper Gets the Value/Multiplier

### Step 1: Calculate Performance Deviation

**Method**: `PlayerScoringCalculator.calculate_performance_deviation()`
**File**: `league_helper/util/player_scoring.py:167-262`

```python
def calculate_performance_deviation(self, player: FantasyPlayer) -> Optional[float]:
    """
    Calculate performance deviation for a player based on actual vs projected points.

    Formula: average((actual - projected) / projected) for valid weeks in rolling window

    Uses MIN_WEEKS as both the rolling window size AND minimum data requirement.

    Returns:
        Optional[float]: Average performance deviation as percentage (e.g., 0.15 = +15%)
                        Returns None if insufficient data or DST position
    """
    # Skip DST teams - insufficient historical projection data
    if player.position == 'DST':
        return None

    # Get MIN_WEEKS for rolling window size
    min_weeks = self.config.performance_scoring['MIN_WEEKS']  # Default: 3

    # Calculate rolling window start (use last MIN_WEEKS completed weeks)
    # Example: current_week=10, min_weeks=4 -> analyze weeks 6,7,8,9
    start_week = max(1, self.config.current_nfl_week - min_weeks)

    deviations = []

    # Analyze only the rolling window (recent MIN_WEEKS weeks)
    for week in range(start_week, self.config.current_nfl_week):
        # Get actual points from player object
        actual_points = getattr(player, f'week_{week}_points')
        if actual_points is None or actual_points == 0:
            continue  # Skip weeks where player didn't play

        # Get projected points from ProjectedPointsManager
        projected_points = self.projected_points_manager.get_projected_points(player, week)
        if projected_points is None or projected_points == 0.0:
            continue  # Skip weeks with missing or zero projections

        # Calculate deviation: (actual - projected) / projected
        deviation = (actual_points - projected_points) / projected_points
        deviations.append(deviation)

    # Require minimum weeks of data (MIN_WEEKS is both window size and minimum)
    if len(deviations) < min_weeks:
        return None

    # Return average deviation
    return statistics.mean(deviations)
```

**Key Logic**:
1. **Position check**: Immediately return None for DST players
2. **Rolling window**: Only analyze the last MIN_WEEKS completed weeks (not entire season)
3. **Data validation**: Skip weeks with missing or zero actual/projected points
4. **Deviation calculation**: `(actual - projected) / projected` for each valid week
5. **Minimum requirement**: Need at least MIN_WEEKS (3) valid weeks
6. **Average**: Return mean of all week-by-week deviations

### Step 2: Convert Deviation to Multiplier

**Method**: `ConfigManager.get_performance_multiplier()`
**File**: `league_helper/util/ConfigManager.py:326-327, 922-1008`

```python
def get_performance_multiplier(self, deviation: float) -> Tuple[float, str]:
    """
    Convert performance deviation to multiplier and rating.

    Args:
        deviation: Average performance deviation (e.g., 0.15 = +15%)

    Returns:
        Tuple[float, str]: (multiplier, rating_label)
    """
    return self._get_multiplier(self.performance_scoring, deviation)

def _get_multiplier(self, scoring_dict, val, rising_thresholds=True):
    """
    Generic threshold-based multiplier calculation.

    For PERFORMANCE (rising_thresholds=True, higher deviation = better):
    - val >= EXCELLENT threshold → EXCELLENT multiplier
    - val >= GOOD threshold → GOOD multiplier
    - GOOD > val > POOR → neutral (1.0)
    - val <= POOR threshold → POOR multiplier
    - val <= VERY_POOR threshold → VERY_POOR multiplier

    Then apply weight exponent: final_multiplier = base_multiplier ^ weight
    """
    thresholds = scoring_dict['THRESHOLDS']
    multipliers = scoring_dict['MULTIPLIERS']
    weight = scoring_dict['WEIGHT']

    # Determine rating level based on thresholds
    if val >= thresholds['EXCELLENT']:
        multiplier, label = multipliers['EXCELLENT'], 'EXCELLENT'
    elif val >= thresholds['GOOD']:
        multiplier, label = multipliers['GOOD'], 'GOOD'
    elif val <= thresholds['VERY_POOR']:
        multiplier, label = multipliers['VERY_POOR'], 'VERY_POOR'
    elif val <= thresholds['POOR']:
        multiplier, label = multipliers['POOR'], 'POOR'
    else:
        multiplier, label = 1.0, 'NEUTRAL'

    # Apply weight exponent
    multiplier = multiplier ** weight
    return multiplier, label
```

### Step 3: Apply to Player Score

**Method**: `PlayerScoringCalculator._apply_performance_multiplier()`
**File**: `league_helper/util/player_scoring.py:521-555`

```python
def _apply_performance_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply performance-based multiplier to player score (Step 5).

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    # Calculate performance deviation
    deviation = self.calculate_performance_deviation(p)

    # If insufficient data or DST, return neutral (no change)
    if deviation is None:
        return player_score, ""

    # Get multiplier and rating from ConfigManager
    multiplier, rating = self.config.get_performance_multiplier(deviation)

    reason = f"Performance: {rating} ({deviation*100:+.1f}%, {multiplier:.2f}x)"
    return player_score * multiplier, reason
```

**Complete Flow**:
```
Player (week_1_points, week_2_points, ..., week_9_points)
    ↓
calculate_performance_deviation() → deviation (e.g., +0.15 = +15%)
    ↓
get_performance_multiplier(0.15) → (1.05, "EXCELLENT")
    ↓
Apply weight exponent: 1.05 ^ 0.2 = 1.0098
    ↓
player_score * 1.0098
```

---

## Calculations Involved

### Formula Breakdown

**Performance Deviation**:
```
For each week W in [1, CURRENT_NFL_WEEK):
    If actual_W > 0 AND projected_W > 0:
        deviation_W = (actual_W - projected_W) / projected_W

avg_deviation = mean(all deviation_W values)
```

**Threshold Comparison** (rising thresholds logic):
```
If avg_deviation >= EXCELLENT_threshold:
    base_multiplier = EXCELLENT (1.05)
Elif avg_deviation >= GOOD_threshold:
    base_multiplier = GOOD (1.025)
Elif avg_deviation <= VERY_POOR_threshold:
    base_multiplier = VERY_POOR (0.95)
Elif avg_deviation <= POOR_threshold:
    base_multiplier = POOR (0.975)
Else:
    base_multiplier = NEUTRAL (1.0)
```

**Weight Exponent Application**:
```
final_multiplier = base_multiplier ^ WEIGHT

Example (WEIGHT=0.2):
- EXCELLENT: 1.05^0.2 = 1.0098 (+0.98%)
- GOOD: 1.025^0.2 = 1.0049 (+0.49%)
- NEUTRAL: 1.0^0.2 = 1.0 (0%)
- POOR: 0.975^0.2 = 0.9950 (-0.50%)
- VERY_POOR: 0.95^0.2 = 0.9898 (-1.02%)
```

**Final Score Adjustment**:
```
adjusted_score = player_score * final_multiplier
```

### Example Calculation

**Player**: Saquon Barkley (RB, PHI)
**Current Week**: 9
**Config**: WEIGHT=0.2, MIN_WEEKS=3

**Step 1: Gather weekly data** (weeks 1-8, actual vs projected)

| Week | Actual Points | Projected Points | Deviation | Calculation |
|------|--------------|------------------|-----------|-------------|
| 1 | 18.4 | 18.4 | 0.0% | (18.4 - 18.4) / 18.4 = 0.000 |
| 2 | 17.4 | 18.03 | -3.5% | (17.4 - 18.03) / 18.03 = -0.035 |
| 3 | 9.5 | 19.26 | -50.7% | (9.5 - 19.26) / 19.26 = -0.507 |
| 4 | 17.4 | 18.23 | -4.6% | (17.4 - 18.23) / 18.23 = -0.046 |
| 5 | 17.8 | 17.95 | -0.8% | (17.8 - 17.95) / 17.95 = -0.008 |
| 6 | 8.7 | 17.66 | -50.7% | (8.7 - 17.66) / 17.66 = -0.507 |
| 7 | 5.2 | 16.07 | -67.6% | (5.2 - 16.07) / 16.07 = -0.676 |
| 8 | 33.4 | 16.93 | +97.3% | (33.4 - 16.93) / 16.93 = +0.973 |

**Step 2: Calculate average deviation**
```
avg_deviation = (-0.035 - 0.507 - 0.046 - 0.008 - 0.507 - 0.676 + 0.973) / 8
avg_deviation = -0.806 / 8 = -0.101 = -10.1%
```

**Step 3: Determine rating** (assuming typical thresholds)
```
EXCELLENT: +0.23 (+23%)
GOOD: +0.12 (+12%)
POOR: -0.12 (-12%)
VERY_POOR: -0.23 (-23%)

-10.1% is between POOR (-12%) and NEUTRAL (0%)
Therefore: NEUTRAL zone → base_multiplier = 1.0
```

**Step 4: Apply weight exponent**
```
final_multiplier = 1.0 ^ 0.2 = 1.0
```

**Step 5: Apply to score**
```
If player_score = 80.0 (after steps 1-4):
adjusted_score = 80.0 * 1.0 = 80.0 (no change, neutral performance)
```

### High Performer Example

**Player**: Christian McCaffrey (RB, SF)
**Weeks 1-8 Average Deviation**: +8.5% (hypothetical)

**Calculation**:
1. avg_deviation = +0.085 (+8.5%)
2. Threshold check: Between NEUTRAL (0%) and GOOD (+12%)
3. Rating: NEUTRAL → base_multiplier = 1.0
4. Weight application: 1.0^0.2 = 1.0
5. Score adjustment: 100.0 * 1.0 = 100.0

**Note**: To reach GOOD (+1.025x), player needs +12% or higher average deviation

### Excellent Performer Example

**Player**: Josh Allen (QB, BUF)
**Hypothetical Deviation**: +25.0% (consistently beats projections)

**Calculation**:
1. avg_deviation = +0.25 (+25.0%)
2. Threshold check: +25% >= EXCELLENT (+23%)
3. Rating: EXCELLENT → base_multiplier = 1.05
4. Weight application: 1.05^0.2 = 1.0098
5. Score adjustment: 100.0 * 1.0098 = 100.98 (+0.98 pts)

---

## Data Sources (players.csv Fields)

### Required Fields

| Field Name | Data Type | Description | Valid Range | Example Values |
|------------|-----------|-------------|-------------|----------------|
| `week_1_points` | float | Actual fantasy points scored in Week 1 | 0.0 - 60.0 | 18.4, 23.2, 0.0 |
| `week_2_points` | float | Actual fantasy points scored in Week 2 | 0.0 - 60.0 | 17.4, 22.7, 39.2 |
| `week_3_points` | float | Actual fantasy points scored in Week 3 | 0.0 - 60.0 | 9.5, 24.0, 20.7 |
| ... | ... | ... | ... | ... |
| `week_N_points` | float | Actual fantasy points for Week N | 0.0 - 60.0 | 33.4, 34.3, 28.82 |

**Note**: Week fields exist for weeks 1-17 (full NFL season)

### Field Specifications

**`week_N_points`**:
- **Type**: float (nullable)
- **Source**: ESPN API `player.stats[week].appliedTotal` (actual points after game completion)
- **Range**: 0.0 to ~60.0 (typical max, QBs can occasionally exceed)
- **Null handling**: Skipped in deviation calculation
- **Zero handling**: Skipped in deviation calculation (indicates player didn't play)
- **Update frequency**: Updated after each game completion (typically Monday-Tuesday)

**Special Cases**:
- **Week N = 0.0**: Player played but scored zero (rare, included in calculation)
- **Week N = None/null**: Data not available (week hasn't occurred or data missing)
- **Bye weeks**: Typically show as 0.0, correctly skipped by logic
- **Injured weeks**: May show 0.0 or None depending on listing status

### Position Field

| Field Name | Data Type | Description | Valid Values |
|------------|-----------|-------------|--------------|
| `position` | string | Player's primary position | QB, RB, WR, TE, K, DST |

**DST Exclusion**: Players with position='DST' are automatically excluded from performance calculations due to insufficient historical projection data quality.

---

## How player-data-fetcher Populates Data

### Data Collection Process

**Script**: `player-data-fetcher/espn_client.py`
**Method**: `ESPNClient.fetch_players()`
**Frequency**: Daily (typically run before draft or weekly updates)

### Weekly Points Extraction

**Data Source**: `data/players.csv` (fields: `week_1_points` through `week_17_points`)

**Population**: Weekly points are populated by `player-data-fetcher` during data collection

**Implementation Details**: See [01_normalization.md - How player-data-fetcher Populates Data](01_normalization.md#how-player-data-fetcher-populates-data) for complete documentation of:
- ESPN API weekly projections/actuals extraction (`espn_client.py:533-572`)
- Fantasy points calculation (`fantasy_points_calculator.py:103-194`)
- CSV export (`player_data_exporter.py:336-358`)

**Key Points**:
- Past weeks (week < CURRENT_NFL_WEEK): Contains actual points (appliedTotal from ESPN)
- Future weeks (week >= CURRENT_NFL_WEEK): Contains projected points (projectedTotal from ESPN)
- The performance multiplier only uses actual points from completed weeks

### Projected Points (Separate File)

**File**: `data/players_projected.csv`
**Purpose**: Historical projections made at start of each week

**Manager**: `league_helper/util/ProjectedPointsManager.py`

```python
class ProjectedPointsManager:
    """Manages access to historical projected points for performance calculations."""

    def get_projected_points(self, player, week_num):
        """
        Get projected points for a specific player and week.

        Returns the projection that was made at the START of that week,
        allowing fair comparison with actual results.

        Args:
            player: FantasyPlayer object
            week_num: Week number (1-17)

        Returns:
            float: Projected points, or None if not available
        """
        # Load from players_projected.csv
        projected_data = pd.read_csv('data/players_projected.csv')

        # Find player by name
        player_row = projected_data[projected_data['name'].str.lower() == player.name.lower()]

        if player_row.empty:
            return None

        # Get week_N_points column
        week_col = f'week_{week_num}_points'
        if week_col not in projected_data.columns:
            return None

        return player_row[week_col].values[0]
```

**Why Separate Files?**
- `players.csv` contains CURRENT/LATEST projections (updated frequently)
- `players_projected.csv` contains HISTORICAL projections (snapshot from each week start)
- Performance calculation requires HISTORICAL projections to avoid hindsight bias

---

## ESPN API JSON Analysis

### Actual Points Data Structure

**API Endpoint**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{leagueId}`

**View Parameters**: `kona_player_info`, `players_wl`

**Relevant JSON Path**: `player.stats[]`

### JSON Structure

```json
{
  "id": 3929630,
  "fullName": "Saquon Barkley",
  "proTeamId": 21,
  "defaultPositionId": 2,
  "eligibleSlots": [2, 23, 16, 17],
  "stats": [
    {
      "id": "013929630",
      "seasonId": 2025,
      "scoringPeriodId": 1,
      "statSourceId": 1,
      "statSplitTypeId": 1,
      "appliedTotal": 18.4,
      "appliedStats": {
        "3": 74.0,
        "24": 1.0,
        "25": 4.0,
        "26": 2.0,
        "42": 10.4,
        "43": 8.0
      }
    },
    {
      "id": "003929630",
      "seasonId": 2025,
      "scoringPeriodId": 1,
      "statSourceId": 0,
      "statSplitTypeId": 1,
      "appliedTotal": 18.4,
      "appliedStats": {
        "3": 75.0,
        "24": 1.0,
        "25": 4.0,
        "26": 2.0,
        "42": 10.5,
        "43": 8.1
      }
    },
    {
      "id": "023929630",
      "seasonId": 2025,
      "scoringPeriodId": 2,
      "statSourceId": 1,
      "appliedTotal": 17.4,
      "appliedStats": { /* Week 2 actual stats */ }
    },
    {
      "id": "003929630",
      "seasonId": 2025,
      "scoringPeriodId": 2,
      "statSourceId": 0,
      "appliedTotal": 18.03,
      "appliedStats": { /* Week 2 projected stats */ }
    }
    // ... more weeks ...
  ]
}
```

### Field Mapping

| JSON Field | Type | Description | Example Value |
|------------|------|-------------|---------------|
| `stats[].scoringPeriodId` | int | Week number (1-17) | 1, 2, 3, ... 17 |
| `stats[].statSourceId` | int | 0=projected, 1=actual | 0 or 1 |
| `stats[].appliedTotal` | float | Total fantasy points (scoring format applied) | 18.4, 17.4, 9.5 |
| `stats[].appliedStats` | object | Individual stat categories with points | {"3": 74.0, "24": 1.0} |

**Key Distinction**: `statSourceId`
- **0**: Projected stats (made before game)
- **1**: Actual stats (recorded after game completion)

### Extraction Logic

```python
# Conceptual example - see 01_normalization.md for actual implementation

def extract_weekly_points(player_info: dict) -> dict:
    """
    Extract weekly actual points from ESPN API response.

    Returns:
        dict: {week_1_points: float, week_2_points: float, ...}
    """
    weekly_points = {}
    stats = player_info.get('stats', [])

    for stat_entry in stats:
        scoring_period = stat_entry.get('scoringPeriodId')
        stat_source = stat_entry.get('statSourceId')

        # Only process actual stats (statSourceId=1)
        if stat_source != 1:
            continue

        # Extract applied total (fantasy points with scoring format)
        actual_points = stat_entry.get('appliedTotal', 0.0)

        # Map to week_N_points field
        week_key = f'week_{scoring_period}_points'
        weekly_points[week_key] = actual_points

    return weekly_points
```

**Sample Extraction** (Saquon Barkley, Week 1-3):

```python
# Input JSON (filtered for statSourceId=1)
stats_actual = [
    {"scoringPeriodId": 1, "statSourceId": 1, "appliedTotal": 18.4},
    {"scoringPeriodId": 2, "statSourceId": 1, "appliedTotal": 17.4},
    {"scoringPeriodId": 3, "statSourceId": 1, "appliedTotal": 9.5}
]

# Output mapping
weekly_points = {
    "week_1_points": 18.4,
    "week_2_points": 17.4,
    "week_3_points": 9.5
}

# Written to players.csv row
"3929630,Saquon Barkley,PHI,RB,9,139.90,QUESTIONABLE,1,0,8.73,72.03,18.4,17.4,9.5,..."
```

### Projected Points Extraction (Historical)

For `players_projected.csv`, the fetcher must store a snapshot at each week start:

```python
def extract_weekly_projections(player_info: dict, target_week: int) -> dict:
    """
    Extract projected points for all future weeks at a specific point in time.

    Args:
        player_info: ESPN player JSON
        target_week: Week when projections are being saved

    Returns:
        dict: {week_N_points: projected_value for N >= target_week}
    """
    projections = {}
    stats = player_info.get('stats', [])

    for stat_entry in stats:
        scoring_period = stat_entry.get('scoringPeriodId')
        stat_source = stat_entry.get('statSourceId')

        # Only process projected stats (statSourceId=0)
        # And only for current/future weeks
        if stat_source != 0 or scoring_period < target_week:
            continue

        projected_points = stat_entry.get('appliedTotal', 0.0)
        week_key = f'week_{scoring_period}_points'
        projections[week_key] = projected_points

    return projections
```

**Important**: `players_projected.csv` should be updated weekly to capture projections as they were made, not overwritten with current projections.

---

## Examples with Walkthroughs

### Example 1: Excellent Performer (Josh Allen)

**Scenario**: Week 9, evaluating QB Josh Allen for draft
**Player Data**:
- Position: QB
- Team: BUF
- Current Score (after Steps 1-4): 95.0 points

**Weekly Performance** (hypothetical consistent overperformer):

| Week | Actual | Projected | Deviation | Calculation |
|------|--------|-----------|-----------|-------------|
| 1 | 38.76 | 38.76 | 0.0% | (38.76 - 38.76) / 38.76 = 0.000 |
| 2 | 11.82 | 20.92 | -43.5% | (11.82 - 20.92) / 20.92 = -0.435 |
| 3 | 23.02 | 21.70 | +6.1% | (23.02 - 21.70) / 21.70 = +0.061 |
| 4 | 24.86 | 20.56 | +20.9% | (24.86 - 20.56) / 20.56 = +0.209 |
| 5 | 19.42 | 22.28 | -12.8% | (19.42 - 22.28) / 22.28 = -0.128 |
| 7 | 23.22 | 21.39 | +8.6% | (23.22 - 21.39) / 21.39 = +0.086 |
| 8 | 28.82 | 21.71 | +32.7% | (28.82 - 21.71) / 21.71 = +0.327 |

**Step 1: Calculate average deviation**
```
avg_deviation = (0.000 - 0.435 + 0.061 + 0.209 - 0.128 + 0.086 + 0.327) / 7
avg_deviation = 0.120 / 7 = 0.0171 = +1.71%
```

**Step 2: Determine rating** (typical thresholds)
```
EXCELLENT: +23.0%
GOOD: +12.0%
NEUTRAL: -12.0% to +12.0%
POOR: -23.0%
VERY_POOR: < -23.0%

+1.71% falls in NEUTRAL zone → base_multiplier = 1.0
```

**Step 3: Apply weight exponent**
```
Config: WEIGHT = 0.2
final_multiplier = 1.0 ^ 0.2 = 1.0
```

**Step 4: Apply to score**
```
adjusted_score = 95.0 * 1.0 = 95.0
reason = "Performance: NEUTRAL (+1.7%, 1.00x)"
```

**Result**: Josh Allen receives neutral performance multiplier despite some strong weeks because average deviation is only +1.71% (within neutral zone).

---

### Example 2: Good Performer (Christian McCaffrey)

**Scenario**: Week 9, evaluating RB Christian McCaffrey
**Player Data**:
- Position: RB
- Team: SF
- Current Score (after Steps 1-4): 105.0 points

**Weekly Performance**:

| Week | Actual | Projected | Deviation | Calculation |
|------|--------|-----------|-----------|-------------|
| 1 | 23.2 | 23.2 | 0.0% | (23.2 - 23.2) / 23.2 = 0.000 |
| 2 | 22.7 | 17.02 | +33.4% | (22.7 - 17.02) / 17.02 = +0.334 |
| 3 | 24.0 | 19.88 | +20.7% | (24.0 - 19.88) / 19.88 = +0.207 |
| 4 | 26.1 | 17.83 | +46.4% | (26.1 - 17.83) / 17.83 = +0.464 |
| 5 | 27.9 | 21.91 | +27.3% | (27.9 - 21.91) / 21.91 = +0.273 |
| 6 | 24.1 | 24.12 | -0.1% | (24.1 - 24.12) / 24.12 = -0.001 |
| 7 | 39.1 | 22.59 | +73.1% | (39.1 - 22.59) / 22.59 = +0.731 |
| 8 | 9.8 | 21.00 | -53.3% | (9.8 - 21.00) / 21.00 = -0.533 |

**Step 1: Calculate average deviation**
```
avg_deviation = (0.000 + 0.334 + 0.207 + 0.464 + 0.273 - 0.001 + 0.731 - 0.533) / 8
avg_deviation = 1.475 / 8 = 0.184 = +18.4%
```

**Step 2: Determine rating**
```
EXCELLENT: +23.0%
GOOD: +12.0%

+18.4% >= +12.0% but < +23.0% → GOOD
base_multiplier = 1.025
```

**Step 3: Apply weight exponent**
```
Config: WEIGHT = 0.2
final_multiplier = 1.025 ^ 0.2 = 1.0049
```

**Step 4: Apply to score**
```
adjusted_score = 105.0 * 1.0049 = 105.51
bonus = 105.51 - 105.0 = +0.51 points
reason = "Performance: GOOD (+18.4%, 1.00x)"
```

**Result**: CMC receives +0.51 point boost for consistently beating projections by 18.4% on average.

---

### Example 3: Poor Performer (Saquon Barkley)

**Scenario**: Week 9, evaluating RB Saquon Barkley
**Player Data**:
- Position: RB
- Team: PHI
- Current Score (after Steps 1-4): 78.0 points

**Weekly Performance** (actual data from players.csv):

| Week | Actual | Projected | Deviation | Calculation |
|------|--------|-----------|-----------|-------------|
| 1 | 18.4 | 18.4 | 0.0% | (18.4 - 18.4) / 18.4 = 0.000 |
| 2 | 17.4 | 18.03 | -3.5% | (17.4 - 18.03) / 18.03 = -0.035 |
| 3 | 9.5 | 19.26 | -50.7% | (9.5 - 19.26) / 19.26 = -0.507 |
| 4 | 17.4 | 18.23 | -4.6% | (17.4 - 18.23) / 18.23 = -0.046 |
| 5 | 17.8 | 17.95 | -0.8% | (17.8 - 17.95) / 17.95 = -0.008 |
| 6 | 8.7 | 17.66 | -50.7% | (8.7 - 17.66) / 17.66 = -0.507 |
| 7 | 5.2 | 16.07 | -67.6% | (5.2 - 16.07) / 16.07 = -0.676 |
| 8 | 33.4 | 16.93 | +97.3% | (33.4 - 16.93) / 16.93 = +0.973 |

**Step 1: Calculate average deviation**
```
avg_deviation = (0.000 - 0.035 - 0.507 - 0.046 - 0.008 - 0.507 - 0.676 + 0.973) / 8
avg_deviation = -0.806 / 8 = -0.101 = -10.1%
```

**Step 2: Determine rating**
```
EXCELLENT: +23.0%
GOOD: +12.0%
NEUTRAL: -12.0% to +12.0%
POOR: -23.0%

-10.1% falls in NEUTRAL zone (-12.0% < -10.1% < +12.0%)
base_multiplier = 1.0
```

**Step 3: Apply weight exponent**
```
Config: WEIGHT = 0.2
final_multiplier = 1.0 ^ 0.2 = 1.0
```

**Step 4: Apply to score**
```
adjusted_score = 78.0 * 1.0 = 78.0
reason = "Performance: NEUTRAL (-10.1%, 1.00x)"
```

**Result**: Despite multiple very poor weeks (weeks 3, 6, 7) and one huge week (week 8), Saquon's average deviation of -10.1% barely keeps him in the neutral zone, avoiding a penalty.

**Analysis**:
- His week 8 explosion (+97.3%) significantly helped his average
- Without week 8, his average would be -23.1% (POOR rating)
- This demonstrates how outlier performances impact the metric

---

### Example 4: Very Poor Performer (Hypothetical)

**Scenario**: Week 9, evaluating WR with consistent underperformance
**Player Data**:
- Position: WR
- Current Score (after Steps 1-4): 72.0 points

**Weekly Performance** (hypothetical chronic underperformer):

| Week | Actual | Projected | Deviation | Calculation |
|------|--------|-----------|-----------|-------------|
| 1 | 10.0 | 14.5 | -31.0% | (10.0 - 14.5) / 14.5 = -0.310 |
| 2 | 9.2 | 13.8 | -33.3% | (9.2 - 13.8) / 13.8 = -0.333 |
| 3 | 11.5 | 15.2 | -24.3% | (11.5 - 15.2) / 15.2 = -0.243 |
| 4 | 8.3 | 14.0 | -40.7% | (8.3 - 14.0) / 14.0 = -0.407 |
| 5 | 12.8 | 16.1 | -20.5% | (12.8 - 16.1) / 16.1 = -0.205 |
| 6 | 9.9 | 14.8 | -33.1% | (9.9 - 14.8) / 14.8 = -0.331 |
| 7 | 10.4 | 15.5 | -32.9% | (10.4 - 15.5) / 15.5 = -0.329 |
| 8 | 11.2 | 14.2 | -21.1% | (11.2 - 14.2) / 14.2 = -0.211 |

**Step 1: Calculate average deviation**
```
avg_deviation = (-0.310 - 0.333 - 0.243 - 0.407 - 0.205 - 0.331 - 0.329 - 0.211) / 8
avg_deviation = -2.369 / 8 = -0.296 = -29.6%
```

**Step 2: Determine rating**
```
EXCELLENT: +23.0%
GOOD: +12.0%
POOR: -23.0%
VERY_POOR: < -23.0%

-29.6% < -23.0% → VERY_POOR
base_multiplier = 0.95
```

**Step 3: Apply weight exponent**
```
Config: WEIGHT = 0.2
final_multiplier = 0.95 ^ 0.2 = 0.9898
```

**Step 4: Apply to score**
```
adjusted_score = 72.0 * 0.9898 = 71.27
penalty = 72.0 - 71.27 = -0.73 points
reason = "Performance: VERY_POOR (-29.6%, 0.99x)"
```

**Result**: This WR receives -0.73 point penalty for chronic underperformance, consistently scoring 30% below projections.

---

### Example 5: Insufficient Data (Rookie Player)

**Scenario**: Week 3, evaluating rookie RB
**Player Data**:
- Position: RB
- Current Score (after Steps 1-4): 65.0 points
- Weeks played: 2 (less than MIN_WEEKS=3)

**Weekly Performance**:

| Week | Actual | Projected | Deviation |
|------|--------|-----------|-----------|
| 1 | 12.5 | 10.2 | +22.5% |
| 2 | 8.3 | 9.8 | -15.3% |

**Step 1: Count valid weeks**
```
valid_weeks = 2
MIN_WEEKS = 3 (from config)
2 < 3 → insufficient data
```

**Step 2: Return None**
```
calculate_performance_deviation() returns None
```

**Step 3: Apply neutral multiplier**
```
_apply_performance_multiplier() receives None
Returns (player_score, "") with no adjustment
```

**Step 4: No change to score**
```
adjusted_score = 65.0 (unchanged)
reason = "" (empty, no performance metric applied)
```

**Result**: Rookie player's score unchanged. Performance multiplier not applied until 3+ weeks of data available.

---

### Example 6: DST Player (Excluded)

**Scenario**: Week 9, evaluating Broncos D/ST
**Player Data**:
- Position: DST
- Current Score (after Steps 1-4): 48.0 points

**Step 1: Check position**
```python
if player.position == 'DST':
    return None
```

**Step 2: Immediate exclusion**
```
calculate_performance_deviation() returns None immediately
No deviation calculation performed
```

**Step 3: Apply neutral**
```
_apply_performance_multiplier() receives None
Returns (player_score, "") with no adjustment
```

**Step 4: No change to score**
```
adjusted_score = 48.0 (unchanged)
reason = "" (DST excluded from performance evaluation)
```

**Result**: DST players never receive performance multiplier due to insufficient projection data quality.

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "PERFORMANCE_SCORING": {
    "MIN_WEEKS": 3,
    "THRESHOLDS": {
      "BASE_POSITION": 0.0,
      "DIRECTION": "BI_EXCELLENT_HI",
      "STEPS": 0.2295799423833918
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 0.19998697166494606
  }
}
```

### Configuration Fields

| Field | Type | Description | Current Value |
|-------|------|-------------|---------------|
| `MIN_WEEKS` | int | Minimum weeks required for calculation | 3 |
| `THRESHOLDS.BASE_POSITION` | float | Center point for threshold calculation | 0.0 |
| `THRESHOLDS.DIRECTION` | string | Threshold direction logic | "BI_EXCELLENT_HI" |
| `THRESHOLDS.STEPS` | float | Step size for threshold boundaries | 0.2296 |
| `MULTIPLIERS.VERY_POOR` | float | Multiplier for very poor performance | 0.95 |
| `MULTIPLIERS.POOR` | float | Multiplier for poor performance | 0.975 |
| `MULTIPLIERS.GOOD` | float | Multiplier for good performance | 1.025 |
| `MULTIPLIERS.EXCELLENT` | float | Multiplier for excellent performance | 1.05 |
| `WEIGHT` | float | Exponent for multiplier adjustment | 0.2000 |

### Threshold Calculation

**Direction**: `BI_EXCELLENT_HI` (bi-directional with excellent high)

**Formula**:
```
BASE = 0.0 (neutral performance = 0% deviation)
STEP = 0.2296 (~23%)

EXCELLENT = BASE + STEP = 0.0 + 0.2296 = +0.2296 (+23.0%)
GOOD = BASE + (STEP / 2) = 0.0 + 0.1148 = +0.1148 (+11.5%)
POOR = BASE - (STEP / 2) = 0.0 - 0.1148 = -0.1148 (-11.5%)
VERY_POOR = BASE - STEP = 0.0 - 0.2296 = -0.2296 (-23.0%)
```

**Calculated Thresholds**:
- EXCELLENT: +23.0% or higher
- GOOD: +11.5% to +23.0%
- NEUTRAL: -11.5% to +11.5%
- POOR: -23.0% to -11.5%
- VERY_POOR: -23.0% or lower

### Weight Exponent Impact

**Current Weight**: 0.2000

**Multiplier Transformations**:

| Rating | Base Multiplier | Weight Applied | Final Multiplier | Effect |
|--------|----------------|----------------|------------------|--------|
| EXCELLENT | 1.05 | 1.05^0.2 = 1.0098 | +0.98% | ~+1.0 pts on 100 pt player |
| GOOD | 1.025 | 1.025^0.2 = 1.0049 | +0.49% | ~+0.5 pts on 100 pt player |
| NEUTRAL | 1.0 | 1.0^0.2 = 1.0 | 0% | No change |
| POOR | 0.975 | 0.975^0.2 = 0.9950 | -0.50% | ~-0.5 pts on 100 pt player |
| VERY_POOR | 0.95 | 0.95^0.2 = 0.9898 | -1.02% | ~-1.0 pts on 100 pt player |

**Interpretation**: Low weight (0.2) significantly dampens the multiplier effect, making performance a subtle adjustment rather than major factor.

### Configuration Tuning Guide

**Increasing Effect**:
- Increase `WEIGHT` (e.g., 0.5, 1.0, 2.0) → amplifies multiplier impact
- Increase `STEPS` (e.g., 0.15, 0.10) → makes thresholds easier to reach
- Increase base multipliers (e.g., EXCELLENT=1.10) → larger adjustments

**Decreasing Effect**:
- Decrease `WEIGHT` (e.g., 0.1, 0.05) → dampens multiplier impact
- Decrease `STEPS` (e.g., 0.30, 0.40) → makes thresholds harder to reach
- Decrease base multipliers (e.g., EXCELLENT=1.02) → smaller adjustments

**Changing Sensitivity**:
- Lower `MIN_WEEKS` (e.g., 2) → more players eligible, less reliable data
- Higher `MIN_WEEKS` (e.g., 5) → fewer players eligible, more reliable data

---

## See Also

### Related Metrics
- **[01_normalization.md](01_normalization.md)** - Base score calculation (uses same weekly points data)
- **[03_player_rating_multiplier.md](03_player_rating_multiplier.md)** - Expert consensus multiplier (complements performance)
- **[06_matchup_multiplier.md](06_matchup_multiplier.md)** - Current week opponent strength (short-term factor)

### Implementation Files
- **`league_helper/util/player_scoring.py:206-301`** - Performance deviation calculation
- **`league_helper/util/player_scoring.py:521-555`** - Performance multiplier application
- **`league_helper/util/ConfigManager.py:326-327, 922-1008`** - Multiplier threshold logic
- **`league_helper/util/ProjectedPointsManager.py`** - Historical projected points access
- **`player-data-fetcher/espn_client.py:1200-1500`** - Weekly points extraction from ESPN API

### Configuration
- **`data/league_config.json`** - Performance scoring parameters (PERFORMANCE_SCORING section)
- **`data/players.csv`** - Actual weekly points (week_1_points through week_17_points)
- **`data/players_projected.csv`** - Historical weekly projections (for deviation calculation)

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - Performance deviation and multiplier tests
- **`tests/league_helper/util/test_ConfigManager.py`** - Threshold and multiplier configuration tests
- **`tests/league_helper/util/test_ProjectedPointsManager.py`** - Projected points loading tests

### Documentation
- **[README.md](README.md)** - Scoring algorithm overview and metric summary
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture and data flow
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines and coding standards

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 9
**Documentation Version**: 1.0
**Code Version**: Week 9, 2025 NFL Season
