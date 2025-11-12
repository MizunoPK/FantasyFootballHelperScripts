# Bye Week Penalty (Step 9)

## Overview

**Type**: Additive penalty (point subtraction)
**Effect**: 0 pts (disabled, SAME_POS_BYE_WEIGHT=0, DIFF_POS_BYE_WEIGHT=0)
**Theoretical Effect**: Variable penalty based on median roster conflict values if enabled
**When Applied**: Step 9 of 10-step scoring algorithm
**Purpose**: Discourage drafting players who share bye weeks with existing roster, preventing depth issues

The Bye Week Penalty evaluates roster construction by identifying players who share the same bye week as players already on the team. When multiple players have overlapping bye weeks, the team faces depth challenges during that week. The penalty is calculated using the median weekly scores of conflicting players, with exponential scaling to reflect severity.

**Key Characteristics**:
- **Position-aware**: Same-position conflicts penalized more heavily than cross-position conflicts
- **Roster-dependent**: Penalty depends on existing roster composition
- **Median-based**: Uses median weekly performance of conflicting players (weeks 1-17)
- **Exponential scaling**: Configurable weight allows non-linear penalty growth
- **Future-looking**: Only considers bye weeks that haven't occurred yet
- **Currently disabled**: Weights set to 0 in config, but logic fully documented

**Formula**:
```
Same-position median total = sum(median(week_1_points ... week_17_points) for each same-pos conflict)
Different-position median total = sum(median(week_1_points ... week_17_points) for each diff-pos conflict)
Penalty = (same_median_total * SAME_POS_BYE_WEIGHT) + (diff_median_total * DIFF_POS_BYE_WEIGHT)
```

**Implementation**: `league_helper/util/player_scoring.py:625-683`

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: Yes (`bye=True`)
**Why**: Prevents drafting players who create bye week depth issues. Encourages balanced roster construction where bye weeks are distributed across multiple weeks rather than clustered.

**Example**: Drafting your 3rd RB:
- RB1 (on roster): Bye week 7, 15.0 median pts
- RB2 (on roster): Bye week 7, 12.0 median pts
- Candidate A: Bye week 7, 14.0 median pts → Large penalty (3 RBs on bye week 7)
- Candidate B: Bye week 10, 14.0 median pts → No penalty (unique bye week)
- Bye week penalty helps system favor Candidate B despite similar projections

### Starter Helper Mode (Roster Optimizer)
**Enabled**: No (`bye=False`)
**Why**: Weekly lineup decisions can't change roster composition - bye weeks are fixed. Players on bye already receive 0 weekly projection, making bye penalty redundant. Disabled to simplify weekly scoring calculations.

**Rationale**: Bye week penalty is for ROSTER CONSTRUCTION (draft/trade decisions). Lineup optimizer works with existing roster, so bye conflicts are irrelevant - you simply can't start players on bye (they have 0 pts projected).

### Trade Simulator Mode
**Enabled**: Varies by configuration
- **Manual Visualizer** (line 86): No (`bye=False`)
- **Full Simulation** (line 89): Yes (`bye=True`)

**Why Full Simulation enables it**: Comprehensive trade analysis benefits from bye week distribution assessment. Acquiring players who cluster bye weeks reduces roster depth quality - Full Simulation mode captures this nuance.

**Why Manual Visualizer disables it**: Quick trade comparisons prioritize ROS value (player_rating, team_quality, performance) over bye week logistics. Manual mode is faster without bye penalty calculations.

**Example** (Full Simulation): Evaluating trade:
- Current roster: 2 WRs on bye week 9
- Trade offer receives: WR with bye week 9 → Penalty increases (3 WRs on bye 9)
- Trade offer receives: WR with bye week 12 → No penalty increase (new bye week)
- Helps identify trades that create roster construction problems

---

## How League Helper Gets the Value/Penalty

### Step 1: Identify Bye Week Conflicts

**Method**: `PlayerScoringCalculator._apply_bye_week_penalty()`
**File**: `league_helper/util/player_scoring.py:625-683`

```python
def _apply_bye_week_penalty(self, p: FantasyPlayer, player_score: float, roster: List[FantasyPlayer]) -> Tuple[float, str]:
    """
    Apply bye week penalty based on roster conflicts (Step 9).

    Collects players with same-position and different-position bye week overlaps,
    then calculates penalty based on median weekly scores using exponential scaling.
    Penalty calculation: (same_median_total ** SAME_POS_BYE_WEIGHT) + (diff_median_total ** DIFF_POS_BYE_WEIGHT)
    """
    # Collect bye week conflicts separately by position relationship
    same_pos_players = []
    diff_pos_players = []

    # Return if the player's bye week is None or has already passed
    if p.bye_week is None:
        return player_score, "No bye week information available"

    if p.bye_week < self.config.current_nfl_week:
        return player_score, "The player's bye week has already passed."

    # Iterate through roster to find bye week overlaps
    for roster_player in roster:
        # Skip the player being scored (avoid counting them against themselves)
        # Also skip roster players with None bye_week or bye week already passed
        if roster_player.id == p.id:
            continue
        if roster_player.bye_week is None or roster_player.bye_week < self.config.current_nfl_week:
            continue

        # Check if this roster player has the same bye week
        if roster_player.bye_week == p.bye_week:
            # Compare positions (use actual position, not FLEX assignment)
            # Same position overlap is worse since it weakens a specific position
            if roster_player.position == p.position:
                same_pos_players.append(roster_player)
            else:
                # Different position overlap is less critical
                diff_pos_players.append(roster_player)

    # Calculate total penalty using median-based exponential scaling
    penalty = self.config.get_bye_week_penalty(same_pos_players, diff_pos_players)

    # Build reason string (only show if there are actual conflicts)
    if len(same_pos_players) == 0 and len(diff_pos_players) == 0:
        reason = ""  # No conflicts = no reason string
    else:
        reason = f"Bye Overlaps: {len(same_pos_players)} same-position, {len(diff_pos_players)} different-position ({-penalty:.1f} pts)"

    # Subtract penalty from score (penalty reduces player value)
    return player_score - penalty, reason
```

**Key Logic**:
1. **Skip invalid bye weeks**: Return immediately if bye_week is None or already passed
2. **Iterate roster**: Check each roster player for bye week overlap
3. **Skip self-comparison**: Don't count player against themselves
4. **Categorize conflicts**: Separate same-position vs different-position overlaps
5. **Calculate penalty**: Use ConfigManager to compute median-based penalty
6. **Subtract from score**: Return adjusted score with penalty applied

### Step 2: Calculate Median-Based Penalty

**Method**: `ConfigManager.get_bye_week_penalty()`
**File**: `league_helper/util/ConfigManager.py:382-462`

```python
def get_bye_week_penalty(self, same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float:
    """
    Calculate bye week penalty based on median weekly scores of conflicting players.

    Algorithm:
    1. For each player in same_pos_players: calculate median from weeks 1-17
    2. For each player in diff_pos_players: calculate median from weeks 1-17
    3. Sum all medians for each list
    4. Apply exponential scaling: same_total * SAME_POS_BYE_WEIGHT + diff_total * DIFF_POS_BYE_WEIGHT
    """
    def calculate_player_median(player: FantasyPlayer) -> float:
        """
        Calculate median weekly points for a player from weeks 1-17.

        Filters out None and zero values, returns 0.0 if no valid data.
        """
        try:
            # Collect valid weekly points (skip None and zeros)
            valid_weeks = [
                points for week in range(1, 18)
                if (points := getattr(player, f'week_{week}_points')) is not None
                and points > 0
            ]

            if not valid_weeks:
                self.logger.warning(f"No valid weekly data for {player.name}, using 0.0 median")
                return 0.0

            median = statistics.median(valid_weeks)
            self.logger.debug(f"Median for {player.name}: {median:.2f} from {len(valid_weeks)} valid weeks")
            return median

        except statistics.StatisticsError as e:
            self.logger.error(f"Failed to calculate median for {player.name}: {e}")
            return 0.0
        except Exception as e:
            self.logger.error(f"Unexpected error calculating median for {player.name}: {e}")
            return 0.0

    # Calculate median totals for each list
    same_pos_median_total = sum(calculate_player_median(p) for p in same_pos_players)
    diff_pos_median_total = sum(calculate_player_median(p) for p in diff_pos_players)

    # Apply scaling
    same_penalty = same_pos_median_total * self.same_pos_bye_weight
    diff_penalty = diff_pos_median_total * self.diff_pos_bye_weight

    total_penalty = same_penalty + diff_penalty

    self.logger.debug(
        f"Bye penalty calculation: "
        f"same_pos_median={same_pos_median_total:.2f}*{self.same_pos_bye_weight}={same_penalty:.2f}, "
        f"diff_pos_median={diff_pos_median_total:.2f}*{self.diff_pos_bye_weight}={diff_penalty:.2f}, "
        f"total={total_penalty:.2f}"
    )

    return total_penalty
```

**Complete Flow**:
```
Player being evaluated: RB, bye_week=7
Roster: [RB1 (bye=7, median=15.0), RB2 (bye=7, median=12.0), WR1 (bye=7, median=18.0)]
    ↓
_apply_bye_week_penalty() → identifies conflicts
    ↓
same_pos_players = [RB1, RB2]  (same position as candidate)
diff_pos_players = [WR1]  (different position)
    ↓
get_bye_week_penalty() → calculates medians
    ↓
same_median_total = 15.0 + 12.0 = 27.0
diff_median_total = 18.0
    ↓
Apply weights (currently 0, but if enabled):
penalty = (27.0 * SAME_POS_BYE_WEIGHT) + (18.0 * DIFF_POS_BYE_WEIGHT)
    ↓
player_score - penalty
```

---

## Calculations Involved

### Formula Breakdown

**Median Calculation** (per player):
```
For player P:
    valid_weeks = [week_N_points for N in 1..17 if week_N_points is not None and week_N_points > 0]
    median_P = median(valid_weeks)
```

**Conflict Totals**:
```
same_median_total = sum(median_P for P in same_pos_players)
diff_median_total = sum(median_P for P in diff_pos_players)
```

**Weight Application**:
```
same_penalty = same_median_total * SAME_POS_BYE_WEIGHT
diff_penalty = diff_median_total * DIFF_POS_BYE_WEIGHT
total_penalty = same_penalty + diff_penalty
```

**Final Score Adjustment**:
```
adjusted_score = player_score - total_penalty
```

### Example Calculation

**Player**: Derrick Henry (RB, BAL)
**Bye Week**: 14
**Current Week**: 9
**Current Score**: 85.0 points (after steps 1-8)

**Roster Analysis**:
- RB1 (Jahmyr Gibbs): Bye week 14, median 16.5 pts
- RB2 (Chase Brown): Bye week 14, median 11.2 pts
- WR1 (Christian Kirk): Bye week 14, median 14.8 pts
- WR2 (Michael Pittman): Bye week 5 (already passed, ignored)
- QB1 (Josh Allen): Bye week 12 (different week, no conflict)

**Step 1: Identify conflicts**
```
Same-position conflicts (RB): [Jahmyr Gibbs, Chase Brown]
Different-position conflicts: [Christian Kirk]
```

**Step 2: Calculate median totals**
```
same_median_total = 16.5 + 11.2 = 27.7
diff_median_total = 14.8
```

**Step 3: Apply weights** (current config: both = 0)
```
SAME_POS_BYE_WEIGHT = 0
DIFF_POS_BYE_WEIGHT = 0

same_penalty = 27.7 * 0 = 0.0
diff_penalty = 14.8 * 0 = 0.0
total_penalty = 0.0 + 0.0 = 0.0
```

**Step 4: Apply to score**
```
adjusted_score = 85.0 - 0.0 = 85.0 (no change due to weights = 0)
reason = "Bye Overlaps: 2 same-position, 1 different-position (0.0 pts)"
```

**Result**: Derrick Henry's score unchanged because bye week weights are disabled (0). If weights were enabled (e.g., SAME=1.0, DIFF=0.5), penalty would be 27.7 + 7.4 = 35.1 pts.

### Example with Enabled Weights (Hypothetical)

**Configuration** (if bye week penalty were enabled):
```json
{
  "SAME_POS_BYE_WEIGHT": 1.5,
  "DIFF_POS_BYE_WEIGHT": 1.0
}
```

**Same scenario as above**:
```
same_median_total = 27.7
diff_median_total = 14.8

same_penalty = 27.7 * 1.5 = 41.55
diff_penalty = 14.8 * 1.0 = 14.8
total_penalty = 41.55 + 14.8 = 56.35
```

**Score adjustment**:
```
adjusted_score = 85.0 - 56.35 = 28.65
penalty_string = "Bye Overlaps: 2 same-position, 1 different-position (-56.4 pts)"
```

**Interpretation**: With weights enabled, creating a 3-RB bye week cluster on week 14 would severely penalize Derrick Henry's draft value, encouraging selection of an RB with a different bye week.

### No Conflict Example

**Player**: Josh Jacobs (RB, GB)
**Bye Week**: 10
**Current Score**: 82.0 points

**Roster Analysis**:
- No players on roster with bye_week = 10

**Calculation**:
```
same_pos_players = []
diff_pos_players = []

same_median_total = 0.0
diff_median_total = 0.0

penalty = 0.0 * SAME_POS_BYE_WEIGHT + 0.0 * DIFF_POS_BYE_WEIGHT = 0.0
adjusted_score = 82.0 - 0.0 = 82.0
reason = "" (empty, no conflicts)
```

**Result**: No penalty applied because Josh Jacobs' bye week doesn't conflict with any roster players.

---

## Data Sources (players.csv Fields)

### Required Fields

| Field Name | Data Type | Description | Valid Range | Example Values |
|------------|-----------|-------------|-------------|----------------|
| `bye_week` | int (nullable) | Week when player's team has bye | 1 - 17 | 7, 10, 14 |
| `week_1_points` | float | Actual points scored in Week 1 | 0.0 - 60.0 | 18.4, 0.0, 23.2 |
| `week_2_points` | float | Actual points scored in Week 2 | 0.0 - 60.0 | 17.4, 22.7, 19.5 |
| ... | ... | ... | ... | ... |
| `week_17_points` | float | Actual points scored in Week 17 | 0.0 - 60.0 | 21.3, 15.8, 28.2 |

**Note**: All weekly point fields (week_1_points through week_17_points) are used to calculate median weekly performance for penalty calculation.

### Field Specifications

**`bye_week`**:
- **Type**: int (nullable)
- **Source**: `data/bye_weeks.csv` (loaded by player-data-fetcher)
- **Range**: 1 to 17 (week number during NFL season)
- **Null handling**: Player excluded from bye week penalty calculation (returned as "No bye week information available")
- **Update frequency**: Static per season (set at beginning of NFL season, does not change)
- **Special cases**:
  - None/null: Player skipped (no penalty applied)
  - < CURRENT_NFL_WEEK: Bye already passed, treated as no conflict

**`week_N_points`** (used for median calculation):
- **Type**: float (nullable)
- **Source**: ESPN API `player.stats[week].appliedTotal` (statSourceId=1, actual points)
- **Range**: 0.0 to ~60.0 (typical max)
- **Null handling**: Excluded from median calculation
- **Zero handling**: Excluded from median calculation (player didn't play)
- **Update frequency**: Updated after each week's games complete

**Why Median Instead of Mean?**
- **Robustness**: Median is less affected by outlier performances (one huge game doesn't skew penalty)
- **Represents typical value**: Better reflects player's usual impact on bye week depth
- **Fair to boom/bust players**: High-variance players not disproportionately penalized

---

## How player-data-fetcher Populates Data

### Data Collection Process

**Script**: `player-data-fetcher/player_data_fetcher_main.py`
**Frequency**: Daily (typically run before draft or weekly updates)

### Bye Week Data Loading

**Step 1: Load bye weeks from CSV**

**File**: `player-data-fetcher/player_data_fetcher_main.py:141-199`

```python
def _load_bye_weeks(self) -> Dict[str, int]:
    """
    Load bye week data from bye_weeks.csv.

    File format (data/bye_weeks.csv):
    Team,ByeWeek
    KC,10
    PHI,5
    ...

    Returns:
        Dict mapping team abbreviation to bye week number
    """
    bye_weeks = {}

    # Look for bye_weeks.csv in parent directory's data folder
    # Path: player-data-fetcher/../data/bye_weeks.csv = project_root/data/bye_weeks.csv
    bye_weeks_file = self.script_dir.parent / "data" / "bye_weeks.csv"

    if not bye_weeks_file.exists():
        # Bye weeks file doesn't exist, log warning and return empty dict
        # Players will have bye_week=None (no penalty applied)
        self.logger.warning(f"Bye weeks file not found: {bye_weeks_file}")
        return bye_weeks

    try:
        # Load CSV with validation (requires 'Team' and 'ByeWeek' columns)
        required_columns = ['Team', 'ByeWeek']
        df = read_csv_with_validation(bye_weeks_file, required_columns)

        # Filter out invalid bye weeks (must be 1-17)
        valid_df = df[(df['ByeWeek'] >= 1) & (df['ByeWeek'] <= 17)]

        # Create mapping: team abbreviation -> bye week number
        bye_weeks = dict(zip(valid_df['Team'], valid_df['ByeWeek']))

        self.logger.info(f"Loaded bye weeks for {len(bye_weeks)} teams")
        self.logger.debug(f"Bye weeks data: {bye_weeks}")

    except Exception as e:
        self.logger.error(f"Failed to load bye weeks from {bye_weeks_file}: {e}")
        # Return empty dict on error (no bye week data available)

    return bye_weeks
```

**Step 2: Assign bye weeks to players**

**File**: `player-data-fetcher/espn_client.py:1394-1396`

```python
# During player data extraction
async def fetch_players(self):
    """Fetch player data from ESPN API including bye weeks."""

    # ... (earlier code extracts team from ESPN API)

    # Extract team
    pro_team_id = player_info.get('proTeamId')
    team = ESPN_TEAM_MAPPINGS.get(pro_team_id, 'UNK')

    # Get bye week from loaded bye_weeks dict
    bye_week = self.bye_weeks.get(team)

    # ... (create ESPNPlayerData object with bye_week field)
```

**Step 3: Write to players.csv**

**File**: `player-data-fetcher/player_data_exporter.py:333`

```python
def export_to_csv(players: List[ESPNPlayerData], filepath: Path):
    """Export player data to CSV including bye weeks."""

    fieldnames = [
        'id', 'name', 'team', 'position', 'bye_week',
        'fantasy_points', 'injury_status', 'drafted', 'locked',
        'average_draft_position', 'player_rating',
        'week_1_points', 'week_2_points', ..., 'week_17_points'
    ]

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player in players:
            row = {
                'id': player.id,
                'name': player.name,
                'team': player.team,
                'position': player.position,
                'bye_week': player.bye_week,
                # ... other fields including week_1_points through week_17_points
            }
            writer.writerow(row)
```

### Weekly Points Extraction

Weekly points data (week_1_points through week_17_points) is extracted from ESPN API as documented in **[05_performance_multiplier.md](05_performance_multiplier.md)** section "How player-data-fetcher Populates Data". The same weekly points used for performance multiplier are used for bye week penalty median calculations.

---

## ESPN API JSON Analysis

### Bye Week Data Structure

Bye weeks are **NOT** provided directly by the ESPN Fantasy API. They must be maintained separately in `data/bye_weeks.csv`.

**Why separate file?**
- ESPN API does not expose bye week information in player data endpoints
- Bye weeks are team-level data (all players on a team share the same bye)
- Bye weeks are static for the season (set by NFL schedule at season start)
- Manually maintained CSV is most reliable source

### bye_weeks.csv Structure

**File**: `data/bye_weeks.csv`

```csv
Team,ByeWeek
ARI,11
ATL,12
BAL,14
BUF,12
CAR,11
CHI,7
CIN,12
CLE,10
DAL,7
DEN,14
DET,5
GB,10
HOU,14
IND,14
JAX,12
KC,6
LAC,5
LAR,6
LV,10
MIA,6
MIN,6
NE,14
NO,12
NYG,11
NYJ,12
PHI,5
PIT,9
SEA,10
SF,9
TB,11
TEN,5
WSH,14
```

**Field Specifications**:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Team` | string | NFL team abbreviation (3 letters) | KC, PHI, BAL |
| `ByeWeek` | int | Week number when team has bye | 5, 10, 14 |

**Mapping to Players**:

**Step 1: Extract team from ESPN API**

```json
{
  "id": 3929630,
  "fullName": "Saquon Barkley",
  "proTeamId": 21,
  "defaultPositionId": 2
}
```

**Step 2: Map proTeamId to team abbreviation**

```python
# ESPN_TEAM_MAPPINGS (in espn_client.py)
ESPN_TEAM_MAPPINGS = {
    21: "PHI",
    22: "PIT",
    # ... all 32 teams
}

team = ESPN_TEAM_MAPPINGS.get(21)  # Returns "PHI"
```

**Step 3: Lookup bye week from bye_weeks.csv**

```python
# Loaded bye_weeks dict: {"PHI": 5, "KC": 6, ...}
bye_week = bye_weeks.get("PHI")  # Returns 5
```

**Step 4: Assign to player**

```python
player_data = ESPNPlayerData(
    id=3929630,
    name="Saquon Barkley",
    team="PHI",
    position="RB",
    bye_week=5,  # Assigned from bye_weeks.csv lookup
    # ... other fields
)
```

### Weekly Points JSON Structure

Weekly points (week_1_points through week_17_points) come from ESPN API and are documented in **[05_performance_multiplier.md](05_performance_multiplier.md)** section "ESPN API JSON Analysis".

**Key JSON Path**: `player.stats[]` where `statSourceId=1` (actual points)

**Sample Extraction**:
```json
{
  "stats": [
    {
      "scoringPeriodId": 1,
      "statSourceId": 1,
      "appliedTotal": 18.4
    },
    {
      "scoringPeriodId": 2,
      "statSourceId": 1,
      "appliedTotal": 17.4
    }
  ]
}
```

Maps to:
```csv
week_1_points,week_2_points,...
18.4,17.4,...
```

These weekly points are used to calculate median performance for bye week penalty.

---

## Examples with Walkthroughs

### Example 1: Severe Same-Position Conflict (Weights Enabled Scenario)

**Scenario**: Week 9, drafting 3rd RB, weights hypothetically enabled
**Config**: SAME_POS_BYE_WEIGHT=1.5, DIFF_POS_BYE_WEIGHT=1.0

**Current Roster**:
- RB1 (Jahmyr Gibbs): Bye week 8 (passed), median 16.5 pts
- RB2 (David Montgomery): Bye week 8 (passed), median 13.8 pts
- WR1 (Amon-Ra St. Brown): Bye week 8 (passed), median 19.2 pts
- QB1 (Jared Goff): Bye week 8 (passed), median 20.5 pts

**Candidate**: James Conner (RB, ARI)
- Team: ARI
- Bye week: 11
- Current Score: 78.0 points (after steps 1-8)

**Step 1: Check roster for week 11 conflicts**
```
Scan roster for bye_week = 11:
- Jahmyr Gibbs: bye=8 (not 11, no conflict)
- David Montgomery: bye=8 (not 11, no conflict)
- Amon-Ra St. Brown: bye=8 (not 11, no conflict)
- Jared Goff: bye=8 (not 11, no conflict)

Result: No conflicts found
```

**Step 2: Calculate penalty**
```
same_pos_players = []
diff_pos_players = []

same_median_total = 0.0
diff_median_total = 0.0

same_penalty = 0.0 * 1.5 = 0.0
diff_penalty = 0.0 * 1.0 = 0.0
total_penalty = 0.0
```

**Step 3: Apply to score**
```
adjusted_score = 78.0 - 0.0 = 78.0
reason = "" (no conflicts)
```

**Result**: James Conner receives no bye week penalty because bye week 11 is unique on roster. Score remains 78.0 points.

---

### Example 2: Heavy Conflict Scenario (Weights Enabled)

**Scenario**: Week 9, drafting 4th RB, bye week cluster already exists
**Config**: SAME_POS_BYE_WEIGHT=1.5, DIFF_POS_BYE_WEIGHT=1.0

**Current Roster**:
- RB1 (Derrick Henry): Bye week 14, median 18.2 pts
- RB2 (Chase Brown): Bye week 14, median 11.5 pts
- RB3 (Devin Singletary): Bye week 14, median 9.3 pts
- WR1 (Davante Adams): Bye week 10, median 16.8 pts
- TE1 (Trey McBride): Bye week 11, median 12.1 pts

**Candidate**: Jonathan Taylor (RB, IND)
- Team: IND
- Bye week: 14
- Current Score: 92.0 points (after steps 1-8)

**Step 1: Calculate weekly medians** (for week 14 conflicts)

```python
# Derrick Henry (RB, bye=14)
henry_weeks = [18.4, 19.2, 15.6, 20.8, 17.5, 21.3, 16.9, 18.8]
henry_median = median([18.4, 19.2, 15.6, 20.8, 17.5, 21.3, 16.9, 18.8]) = 18.2

# Chase Brown (RB, bye=14)
brown_weeks = [8.2, 12.5, 10.8, 13.1, 11.2, 9.9, 14.3, 10.5]
brown_median = median([8.2, 12.5, 10.8, 13.1, 11.2, 9.9, 14.3, 10.5]) = 11.5

# Devin Singletary (RB, bye=14)
singletary_weeks = [6.3, 11.2, 8.5, 10.7, 9.1, 8.9, 12.4, 7.8]
singletary_median = median([6.3, 11.2, 8.5, 10.7, 9.1, 8.9, 12.4, 7.8]) = 9.3
```

**Step 2: Identify conflicts**
```
Scan roster for bye_week = 14:
- Derrick Henry: bye=14, position=RB → SAME-POSITION conflict
- Chase Brown: bye=14, position=RB → SAME-POSITION conflict
- Devin Singletary: bye=14, position=RB → SAME-POSITION conflict
- Davante Adams: bye=10 (no conflict)
- Trey McBride: bye=11 (no conflict)

same_pos_players = [Derrick Henry, Chase Brown, Devin Singletary]
diff_pos_players = []
```

**Step 3: Calculate median totals**
```
same_median_total = 18.2 + 11.5 + 9.3 = 39.0
diff_median_total = 0.0
```

**Step 4: Apply weights**
```
SAME_POS_BYE_WEIGHT = 1.5
DIFF_POS_BYE_WEIGHT = 1.0

same_penalty = 39.0 * 1.5 = 58.5
diff_penalty = 0.0 * 1.0 = 0.0
total_penalty = 58.5 + 0.0 = 58.5
```

**Step 5: Apply to score**
```
adjusted_score = 92.0 - 58.5 = 33.5
reason = "Bye Overlaps: 3 same-position, 0 different-position (-58.5 pts)"
```

**Result**: Jonathan Taylor receives massive -58.5 point penalty for creating 4-RB bye week cluster on week 14. His value drops from 92.0 to 33.5 points, heavily discouraging this pick.

**Alternative**: If Taylor had bye week 10 (different from week 14):
```
same_pos_players = []
diff_pos_players = []
penalty = 0.0
adjusted_score = 92.0 (no penalty)
```

---

### Example 3: Mixed Position Conflicts (Weights Enabled)

**Scenario**: Week 9, drafting WR, some roster players share bye week
**Config**: SAME_POS_BYE_WEIGHT=1.5, DIFF_POS_BYE_WEIGHT=1.0

**Current Roster**:
- RB1 (Bijan Robinson): Bye week 12, median 17.3 pts
- WR1 (Drake London): Bye week 12, median 15.8 pts
- WR2 (DJ Moore): Bye week 7 (passed), median 14.2 pts
- TE1 (Kyle Pitts): Bye week 12, median 9.5 pts

**Candidate**: Calvin Ridley (WR, TEN)
- Team: TEN
- Bye week: 5 (already passed)
- Current Score: 73.0 points

**Step 1: Check bye week status**
```python
if p.bye_week < self.config.current_nfl_week:
    return player_score, "The player's bye week has already passed."
```

**Calculation**:
```
calvin_ridley.bye_week = 5
current_nfl_week = 9
5 < 9 → True (bye already passed)

Return immediately: (73.0, "The player's bye week has already passed.")
```

**Result**: Calvin Ridley receives no bye week penalty because his bye week (5) has already occurred. Score remains 73.0 points.

---

### Example 4: Current Configuration (Weights = 0)

**Scenario**: Week 9, any draft pick with current production config
**Config**: SAME_POS_BYE_WEIGHT=0, DIFF_POS_BYE_WEIGHT=0

**Current Roster**:
- RB1: Bye week 10, median 15.0 pts
- RB2: Bye week 10, median 12.0 pts
- WR1: Bye week 10, median 18.0 pts

**Candidate**: Kenneth Walker III (RB, SEA)
- Bye week: 10
- Current Score: 80.0 points

**Step 1: Identify conflicts**
```
same_pos_players = [RB1, RB2]  (2 RBs on bye week 10)
diff_pos_players = [WR1]  (1 WR on bye week 10)
```

**Step 2: Calculate medians**
```
same_median_total = 15.0 + 12.0 = 27.0
diff_median_total = 18.0
```

**Step 3: Apply weights**
```
SAME_POS_BYE_WEIGHT = 0
DIFF_POS_BYE_WEIGHT = 0

same_penalty = 27.0 * 0 = 0.0
diff_penalty = 18.0 * 0 = 0.0
total_penalty = 0.0
```

**Step 4: Apply to score**
```
adjusted_score = 80.0 - 0.0 = 80.0
reason = "Bye Overlaps: 2 same-position, 1 different-position (0.0 pts)"
```

**Result**: Kenneth Walker III receives no actual penalty (0.0 pts) because weights are disabled. Reason string still shows conflicts for informational purposes, but score is unchanged.

**Why Disabled?**
- Current optimal configuration (from simulation optimization) found that bye week penalties don't improve draft performance
- Weights set to 0 effectively disables penalty while keeping logic intact
- System can be re-enabled by adjusting weights in configuration
- Logic fully documented for potential future activation

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "SAME_POS_BYE_WEIGHT": 0,
  "DIFF_POS_BYE_WEIGHT": 0
}
```

### Configuration Fields

| Field | Type | Description | Current Value | Effect When Enabled |
|-------|------|-------------|---------------|---------------------|
| `SAME_POS_BYE_WEIGHT` | float | Multiplier for same-position conflict penalty | 0 | Linear scaling: 1.0 = sum of medians, 1.5 = 1.5x sum, 0.5 = 0.5x sum |
| `DIFF_POS_BYE_WEIGHT` | float | Multiplier for different-position conflict penalty | 0 | Linear scaling: 1.0 = sum of medians, 1.5 = 1.5x sum, 0.5 = 0.5x sum |

### Weight Scaling Interpretation

**Linear Multipliers** (not exponential like other metrics):

```
Weight = 0.0 → Disabled (no penalty)
Weight = 0.5 → Penalty = 50% of median sum
Weight = 1.0 → Penalty = 100% of median sum (full median total)
Weight = 1.5 → Penalty = 150% of median sum (emphasizes conflicts)
Weight = 2.0 → Penalty = 200% of median sum (severe penalty)
```

**Example Comparison**:

Scenario: same_median_total = 30.0, diff_median_total = 15.0

| SAME Weight | DIFF Weight | Same Penalty | Diff Penalty | Total |
|-------------|-------------|--------------|--------------|-------|
| 0.0 | 0.0 | 0.0 | 0.0 | 0.0 (disabled) |
| 0.5 | 0.5 | 15.0 | 7.5 | 22.5 |
| 1.0 | 1.0 | 30.0 | 15.0 | 45.0 |
| 1.5 | 1.0 | 45.0 | 15.0 | 60.0 |
| 2.0 | 1.5 | 60.0 | 22.5 | 82.5 |

### Configuration Tuning Guide

**When to Enable**:
- League values roster construction and depth management
- Want to discourage bye week clustering
- Prefer balanced bye week distribution across season

**When to Keep Disabled**:
- Focus purely on projected points (current approach)
- Bye week management handled manually by user
- System optimization found no performance benefit (current status)

**Recommended Starting Values** (if enabling):
```json
{
  "SAME_POS_BYE_WEIGHT": 1.0,
  "DIFF_POS_BYE_WEIGHT": 0.5
}
```

Rationale:
- Same-position conflicts penalized at full median value (severe depth issue)
- Different-position conflicts penalized at half value (less critical)
- Can adjust based on league preferences

---

## See Also

### Related Metrics
- **[01_normalization.md](01_normalization.md)** - Base score calculation (uses same weekly points for median)
- **[05_performance_multiplier.md](05_performance_multiplier.md)** - Performance deviation (uses same weekly points)
- **[08_draft_order_bonus.md](08_draft_order_bonus.md)** - Draft round bonuses (applied just before bye penalty)

### Implementation Files
- **`league_helper/util/player_scoring.py:625-683`** - Bye week penalty application
- **`league_helper/util/ConfigManager.py:382-462`** - Median-based penalty calculation
- **`player-data-fetcher/player_data_fetcher_main.py:141-199`** - Bye week data loading

### Data Files
- **`data/league_config.json`** - Bye week weight configuration (SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT)
- **`data/bye_weeks.csv`** - Team bye week mappings (source: NFL schedule)
- **`data/players.csv`** - Player bye weeks and weekly points (bye_week, week_N_points)

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - Bye week penalty logic tests
- **`tests/league_helper/util/test_ConfigManager.py`** - Median calculation and weight application tests

### Documentation
- **[README.md](../../README.md)** - Scoring algorithm overview
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture and data flow
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 9
**Documentation Version**: 1.0
**Bye Week Penalty Status**: Disabled (weights = 0)
