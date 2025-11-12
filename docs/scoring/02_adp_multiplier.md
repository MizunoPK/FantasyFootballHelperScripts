# ADP Multiplier (Step 2)

## Overview

**Type**: Multiplicative (percentage adjustment)
**Effect**: ±9.9% (0.904x to 1.099x with default weight=1.94)
**Base Multipliers**: 0.95x to 1.05x (±5% before weight exponent)
**When Applied**: Step 2 of 10-step scoring algorithm
**Purpose**: Incorporate market wisdom from fantasy community's draft behavior

The ADP (Average Draft Position) Multiplier adjusts player scores based on consensus draft position from the fantasy community. ADP reflects the collective wisdom of thousands of fantasy managers and captures factors not fully represented in projections alone - such as perceived upside, consistency concerns, injury risk, and opportunity changes. Lower ADP (earlier picks) indicates higher community confidence and receives a positive multiplier.

**Key Characteristics**:
- **Market signal**: Captures community consensus beyond pure projections
- **Decreasing threshold logic**: Lower ADP values = better (rank 1 = 1st pick)
- **Inverse relationship**: Better ADP → higher multiplier
- **Weight dampening**: Exponent reduces multiplier impact for fine-tuning
- **Optional metric**: Can be disabled but enabled by default

**Formula**:
```
Multiplier = lookup ADP in thresholds → apply weight exponent
Adjusted Score = player_score * (base_multiplier ^ WEIGHT)
```

**Implementation**: `league_helper/util/player_scoring.py:485-493`

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: Yes (`adp=True`)
**Why**: ADP reflects real draft behavior and market consensus. Players drafted earlier than projections suggest often have hidden value (opportunity, coaching trust, breakout potential) that raw projections miss.

**Example**: Two WRs with similar projections
- WR1: 180 ROS pts, ADP 15 (EXCELLENT) → 1.05x multiplier
- WR2: 180 ROS pts, ADP 95 (POOR) → 0.975x multiplier
- ADP multiplier identifies WR1 as safer pick despite equal projections

### Starter Helper Mode (Roster Optimizer)
**Enabled**: No (`adp=False`)
**Why**: ADP reflects draft-time value, not weekly performance. Once drafted, weekly lineup decisions depend on recent form, matchups, and projections - not where the player was drafted months ago.

**Example**: Week 9 lineup decision
- ADP is static season-long metric
- Recent performance and matchups more relevant for weekly starts
- ADP disabled to focus on current-week factors

### Trade Simulator Mode
**Enabled**: No (`adp=False`)
**Why**: Trade evaluation focuses on current player value (player_rating, team_quality, performance) rather than draft-day expectations. Mid-season, ADP becomes less relevant as players establish actual production patterns. Performance multiplier and player rating provide better ROS assessment.

**Rationale**: ADP reflects pre-season expectations which can be outdated by mid-season. A player drafted early (ADP 15) who's underperforming shouldn't get bonus points in trade valuation - their actual production (performance multiplier) and current expert rankings (player_rating) are more accurate indicators of trade value.

---

## How League Helper Gets the Value/Multiplier

### Step 1: Get ADP Value from Player

**Data Source**: `FantasyPlayer.average_draft_position` field
**File**: `utils/FantasyPlayer.py:98`

```python
@dataclass
class FantasyPlayer:
    # ... other fields ...
    average_draft_position: Optional[float] = None  # ESPN's ADP data
```

**Value Interpretation**:
- **Lower = Better**: ADP of 1.0 means typically picked 1st overall
- **Range**: 1.0 (first pick) to 300+ (undrafted)
- **Null handling**: None/null treated as neutral in multiplier logic

### Step 2: Convert ADP to Multiplier

**Method**: `ConfigManager.get_adp_multiplier()`
**File**: `league_helper/util/ConfigManager.py:297-298`

```python
def get_adp_multiplier(self, adp_val) -> Tuple[float, str]:
    """
    Get ADP multiplier based on average draft position.

    Args:
        adp_val: Average draft position (lower is better)

    Returns:
        Tuple[float, str]: (multiplier, rating_label)
            - multiplier: Weight-adjusted multiplier value
            - rating_label: EXCELLENT, GOOD, NEUTRAL, POOR, or VERY_POOR
    """
    return self._get_multiplier(self.adp_scoring, adp_val, rising_thresholds=False)
```

**Key Parameter**: `rising_thresholds=False`
- Indicates **decreasing threshold logic** (lower values are better)
- Opposite of player_rating (where higher is better)

### Step 3: Apply Threshold Logic

**Method**: `ConfigManager._get_multiplier()`
**File**: `league_helper/util/ConfigManager.py:922-1008`

```python
def _get_multiplier(self, scoring_dict, val, rising_thresholds=False):
    """
    Generic threshold-based multiplier calculation.

    For ADP (rising_thresholds=False, lower is better):
    - val <= EXCELLENT threshold → EXCELLENT multiplier
    - val <= GOOD threshold → GOOD multiplier
    - GOOD < val < POOR → neutral (1.0)
    - val >= POOR threshold → POOR multiplier
    - val >= VERY_POOR threshold → VERY_POOR multiplier

    Then apply weight exponent: final_multiplier = base_multiplier ^ weight
    """
    # Handle None values - return neutral
    if val is None:
        multiplier, label = 1.0, 'NEUTRAL'

    # DECREASING THRESHOLDS: Lower values are better
    elif not rising_thresholds:
        if val <= scoring_dict['THRESHOLDS']['EXCELLENT']:
            multiplier, label = scoring_dict['MULTIPLIERS']['EXCELLENT'], 'EXCELLENT'
        elif val <= scoring_dict['THRESHOLDS']['GOOD']:
            multiplier, label = scoring_dict['MULTIPLIERS']['GOOD'], 'GOOD'
        elif val >= scoring_dict['THRESHOLDS']['VERY_POOR']:
            multiplier, label = scoring_dict['MULTIPLIERS']['VERY_POOR'], 'VERY_POOR'
        elif val >= scoring_dict['THRESHOLDS']['POOR']:
            multiplier, label = scoring_dict['MULTIPLIERS']['POOR'], 'POOR'
        else:
            multiplier, label = 1.0, 'NEUTRAL'

    # Apply weight exponent
    multiplier = multiplier ** scoring_dict['WEIGHT']
    return multiplier, label
```

### Step 4: Apply to Player Score

**Method**: `PlayerScoringCalculator._apply_adp_multiplier()`
**File**: `league_helper/util/player_scoring.py:485-493`

```python
def _apply_adp_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Calculate ADP-based market wisdom adjustment multiplier (Step 2).

    Args:
        p: Player to evaluate
        player_score: Current score after normalization (Step 1)

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    # Get ADP-based multiplier from config
    # ADP (Average Draft Position) reflects market consensus on player value
    # Lower ADP (earlier picks) = higher multiplier (e.g., 1.05x)
    # Higher ADP (later picks) = lower multiplier (e.g., 0.95x)
    multiplier, rating = self.config.get_adp_multiplier(p.average_draft_position)
    reason = f"ADP: {rating} ({multiplier:.2f}x)"
    return player_score * multiplier, reason
```

**Complete Flow**:
```
Player (average_draft_position=12.01)
    ↓
get_adp_multiplier(12.01) → check thresholds
    ↓
12.01 <= 26.94 (EXCELLENT threshold) → EXCELLENT
    ↓
base_multiplier = 1.05, apply weight: 1.05 ^ 1.94 = 1.0989
    ↓
player_score * 1.0989
```

---

## Calculations Involved

### Formula Breakdown

**Threshold Lookup** (decreasing logic):
```
If ADP <= EXCELLENT_threshold (26.94):
    rating = EXCELLENT, base_multiplier = 1.05
Elif ADP <= GOOD_threshold (53.88):
    rating = GOOD, base_multiplier = 1.025
Elif ADP >= VERY_POOR_threshold (107.76):
    rating = VERY_POOR, base_multiplier = 0.95
Elif ADP >= POOR_threshold (80.82):
    rating = POOR, base_multiplier = 0.975
Else:
    rating = NEUTRAL, base_multiplier = 1.0
```

**Weight Exponent Application**:
```
final_multiplier = base_multiplier ^ WEIGHT

Example (WEIGHT=1.94):
- EXCELLENT: 1.05^1.94 = 1.0989 (+9.89%)
- GOOD: 1.025^1.94 = 1.0490 (+4.90%)
- NEUTRAL: 1.0^1.94 = 1.0 (0%)
- POOR: 0.975^1.94 = 0.9519 (-4.81%)
- VERY_POOR: 0.95^1.94 = 0.9038 (-9.62%)
```

**Final Score Adjustment**:
```
adjusted_score = player_score * final_multiplier
```

### Example Calculation (EXCELLENT)

**Player**: Amon-Ra St. Brown (WR, DET)
**ADP**: 12.01
**Current Score** (after Step 1): 51.35 points
**Config**: WEIGHT=1.94, EXCELLENT threshold=26.94

**Step 1: Compare to thresholds**
```
ADP = 12.01
EXCELLENT threshold = 26.94

12.01 <= 26.94 → EXCELLENT rating
```

**Step 2: Get base multiplier**
```
EXCELLENT → base_multiplier = 1.05
```

**Step 3: Apply weight exponent**
```
final_multiplier = 1.05 ^ 1.94
final_multiplier = 1.0989
```

**Step 4: Apply to score**
```
adjusted_score = 51.35 * 1.0989
adjusted_score = 56.43 points
bonus = 56.43 - 51.35 = +5.08 points
reason = "ADP: EXCELLENT (1.10x)"
```

**Result**: Amon-Ra receives +5.08 point boost for elite ADP (12th overall)

### Example Calculation (GOOD)

**Player**: Saquon Barkley (RB, PHI)
**ADP**: 8.73
**Current Score**: 48.50 points

**Calculation**:
```
ADP = 8.73 <= 26.94 (EXCELLENT threshold)
→ EXCELLENT rating
→ base_multiplier = 1.05
→ final_multiplier = 1.05^1.94 = 1.0989
→ adjusted_score = 48.50 * 1.0989 = 53.30 (+4.80 pts)
```

**Result**: Saquon also receives EXCELLENT rating (top-10 pick)

### Example Calculation (NEUTRAL)

**Player**: Jake Ferguson (TE, DAL)
**ADP**: 96.89
**Current Score**: 35.20 points

**Calculation**:
```
ADP = 96.89
EXCELLENT threshold = 26.94 → No
GOOD threshold = 53.88 → No
VERY_POOR threshold = 107.76 → No (96.89 < 107.76)
POOR threshold = 80.82 → Yes (96.89 >= 80.82)

→ POOR rating
→ base_multiplier = 0.975
→ final_multiplier = 0.975^1.94 = 0.9519
→ adjusted_score = 35.20 * 0.9519 = 33.51 (-1.69 pts)
```

**Result**: Mid-round TE receives small penalty for lower community confidence

### Example Calculation (VERY_POOR)

**Player**: Cameron Dicker (K, LAC)
**ADP**: 108.58
**Current Score**: 19.90 points

**Calculation**:
```
ADP = 108.58
VERY_POOR threshold = 107.76

108.58 >= 107.76 → VERY_POOR rating
→ base_multiplier = 0.95
→ final_multiplier = 0.95^1.94 = 0.9038
→ adjusted_score = 19.90 * 0.9038 = 17.99 (-1.91 pts)
```

**Result**: Late-round kicker receives -1.91 point penalty for poor ADP

---

## Data Sources (players.csv Fields)

### Required Fields

| Field Name | Data Type | Description | Valid Range | Example Values |
|------------|-----------|-------------|-------------|----------------|
| `average_draft_position` | float (nullable) | ESPN community average draft position | 1.0 - 300.0 | 12.01, 8.73, 108.58 |

### Field Specifications

**`average_draft_position`**:
- **Type**: float (nullable)
- **Source**: ESPN API `player.ownership.averageDraftPosition`
- **Range**: 1.0 (first overall pick) to 300+ (undrafted)
- **Interpretation**: Lower values indicate earlier draft position (higher value)
- **Update frequency**: Updated periodically during draft season (pre-season)
- **Null handling**: Treated as NEUTRAL (1.0x multiplier) if missing
- **Position variance**: QBs typically lower ADP than projection suggests (drafted later)

**Special Cases**:
- **Rookies**: May have ADP before NFL draft, updated after landing spot known
- **Breakout players**: ADP set pre-season, doesn't update mid-season
- **Injured players**: ADP reflects pre-injury value, not current status
- **Undrafted players**: Typically no ADP data (null/None)

---

## How player-data-fetcher Populates Data

### Data Collection Process

**Main Script**: `player-data-fetcher/player_data_fetcher_main.py`
**ESPN Client**: `player-data-fetcher/espn_client.py`
**Exporter**: `player-data-fetcher/player_data_exporter.py`
**Frequency**: Pre-season and early season (ADP stabilizes after week 1)

### ADP Extraction

**Step 1: Extract ownership data from ESPN API response**

```python
# File: player-data-fetcher/espn_client.py:1470-1474

# Extract ADP data
average_draft_position = None
ownership_data = player_info.get('ownership', {})
if ownership_data and 'averageDraftPosition' in ownership_data:
    average_draft_position = float(ownership_data['averageDraftPosition'])
```

**Step 2: Write to players.csv**

```python
# File: player-data-fetcher/player_data_exporter.py:336-358

# Create FantasyPlayer object with all fields (including ADP)
fantasy_player = FantasyPlayer(
    id=player_data.id,
    name=player_data.name,
    team=player_data.team,
    position=player_data.position,
    bye_week=player_data.bye_week,
    drafted=drafted_value,
    locked=locked_value,
    fantasy_points=player_data.fantasy_points,
    average_draft_position=player_data.average_draft_position,  # ADP field
    player_rating=player_data.player_rating,
    injury_status=player_data.injury_status,
    # Weekly projections (weeks 1-17)
    week_1_points=player_data.week_1_points,
    # ... (weeks 2-16) ...
    week_17_points=player_data.week_17_points
)
```

---

## ESPN API JSON Analysis

### ADP Data Structure

**API Endpoint**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{leagueId}`

**View Parameters**: `kona_player_info`, `ownership`

**Relevant JSON Path**: `player.ownership.averageDraftPosition`

### JSON Structure

```json
{
  "id": 4374302,
  "fullName": "Amon-Ra St. Brown",
  "proTeamId": 8,
  "defaultPositionId": 4,
  "ownership": {
    "percentOwned": 99.8,
    "percentStarted": 87.3,
    "averageDraftPosition": 12.01,
    "auctionValueAverage": 45.2
  }
}
```

### Field Mapping

| JSON Field | Type | Description | Example Value |
|------------|------|-------------|---------------|
| `ownership.averageDraftPosition` | float | Community average draft position | 12.01, 8.73, 108.58 |
| `ownership.percentOwned` | float | Percentage of leagues where owned | 99.8, 67.4, 12.3 |
| `ownership.percentStarted` | float | Percentage of leagues where started | 87.3, 45.2, 5.1 |
| `ownership.auctionValueAverage` | float | Average auction draft price | 45.2, 38.5, 1.2 |

**Key Field**: `averageDraftPosition`
- Aggregated from ESPN public and private leagues
- Reflects consensus across thousands of drafts
- Updated throughout pre-season as draft behavior evolves

### Extraction Logic

```python
# File: player-data-fetcher/espn_client.py:1470-1474

# Extract ADP data
average_draft_position = None
ownership_data = player_info.get('ownership', {})
if ownership_data and 'averageDraftPosition' in ownership_data:
    average_draft_position = float(ownership_data['averageDraftPosition'])
```

**Full Context** (espn_client.py:1470-1485):
- ADP extracted from `player_info.get('ownership', {})` dictionary
- Field: `averageDraftPosition` (ESPN's community consensus)
- Validation: Checks if ownership_data exists and contains the field
- Conversion: Converts to float for consistency
- Null handling: Remains None if not present in ESPN data

**Sample Extraction** (Top Players):

```python
# Top-5 ADP Players (Week 9, 2025)
adp_data = [
    {"name": "Ja'Marr Chase", "adp": 3.25},
    {"name": "Bijan Robinson", "adp": 4.25},
    {"name": "Christian McCaffrey", "adp": 5.86},
    {"name": "Justin Jefferson", "adp": 6.89},
    {"name": "Jahmyr Gibbs", "adp": 7.56}
]

# Written to players.csv
"4362628,Ja'Marr Chase,CIN,WR,10,164.42,ACTIVE,1,0,3.25,93.42,..."
"4430807,Bijan Robinson,ATL,RB,5,167.67,ACTIVE,1,0,4.25,84.08,..."
```

---

## Examples with Walkthroughs

### Example 1: Elite Pick (Ja'Marr Chase) - EXCELLENT

**Scenario**: Week 9, evaluating WR Ja'Marr Chase
**Player Data**:
- Position: WR
- Team: CIN
- ADP: 3.25 (3rd overall pick)
- Current Score (after Step 1): 50.00 points

**Step 1: Compare to thresholds**
```
ADP = 3.25
EXCELLENT threshold = 26.94

3.25 <= 26.94 → EXCELLENT rating
```

**Step 2: Get base multiplier**
```
EXCELLENT → base_multiplier = 1.05
```

**Step 3: Apply weight exponent**
```
WEIGHT = 1.94
final_multiplier = 1.05 ^ 1.94 = 1.0989
```

**Step 4: Apply to score**
```
adjusted_score = 50.00 * 1.0989 = 54.95
bonus = 54.95 - 50.00 = +4.95 points
reason = "ADP: EXCELLENT (1.10x)"
```

**Result**: Top-5 pick receives +4.95 point boost for elite community consensus

---

### Example 2: First-Round Pick (Saquon Barkley) - EXCELLENT

**Scenario**: Week 9, evaluating RB Saquon Barkley
**Player Data**:
- Position: RB
- Team: PHI
- ADP: 8.73
- Current Score: 48.50 points

**Calculation**:
```
ADP = 8.73 <= 26.94 (EXCELLENT)
→ base_multiplier = 1.05
→ final_multiplier = 1.05^1.94 = 1.0989
→ adjusted_score = 48.50 * 1.0989 = 53.30 (+4.80 pts)
```

**Result**: Late first-round pick still receives EXCELLENT rating

---

### Example 3: Second-Round Pick (Amon-Ra St. Brown) - EXCELLENT

**Scenario**: Week 9, evaluating WR Amon-Ra St. Brown
**Player Data**:
- Position: WR
- Team: DET
- ADP: 12.01
- Current Score: 51.35 points

**Calculation**:
```
ADP = 12.01 <= 26.94 (EXCELLENT)
→ final_multiplier = 1.0989
→ adjusted_score = 51.35 * 1.0989 = 56.43 (+5.08 pts)
```

**Result**: Early second-round pick receives EXCELLENT rating

---

### Example 4: Fourth-Round Pick (Josh Allen) - GOOD

**Scenario**: Week 9, evaluating QB Josh Allen
**Player Data**:
- Position: QB
- Team: BUF
- ADP: 20.75
- Current Score: 52.00 points

**Calculation**:
```
ADP = 20.75
20.75 <= 26.94 (EXCELLENT threshold) → EXCELLENT rating
→ base_multiplier = 1.05
→ final_multiplier = 1.05^1.94 = 1.0989
→ adjusted_score = 52.00 * 1.0989 = 57.14 (+5.14 pts)
```

**Result**: Top QB drafted in 2nd/3rd round receives EXCELLENT rating

**Note**: QBs typically have lower ADP than projections suggest (positional scarcity vs replacement value)

---

### Example 5: Mid-Round Pick (Nico Collins) - GOOD

**Scenario**: Week 9, evaluating WR Nico Collins
**Player Data**:
- Position: WR
- Team: HOU
- ADP: 23.59
- Current Score: 45.00 points

**Calculation**:
```
ADP = 23.59 <= 26.94 (EXCELLENT)
→ final_multiplier = 1.0989
→ adjusted_score = 45.00 * 1.0989 = 49.45 (+4.45 pts)
```

**Result**: Early third-round pick just makes EXCELLENT cutoff

---

### Example 6: Late Pick (Ladd McConkey) - NEUTRAL

**Scenario**: Week 9, evaluating WR Ladd McConkey
**Player Data**:
- Position: WR
- Team: LAC
- ADP: 39.30
- Current Score: 38.00 points

**Calculation**:
```
ADP = 39.30
EXCELLENT = 26.94 → No (39.30 > 26.94)
GOOD = 53.88 → Yes (39.30 <= 53.88)

→ GOOD rating
→ base_multiplier = 1.025
→ final_multiplier = 1.025^1.94 = 1.0490
→ adjusted_score = 38.00 * 1.0490 = 39.86 (+1.86 pts)
```

**Result**: Mid-round pick receives +1.86 point boost (GOOD rating)

---

### Example 7: Very Late Pick (Jake Ferguson) - POOR

**Scenario**: Week 9, evaluating TE Jake Ferguson
**Player Data**:
- Position: TE
- Team: DAL
- ADP: 96.89
- Current Score: 35.20 points

**Calculation**:
```
ADP = 96.89
96.89 >= 80.82 (POOR threshold) → POOR rating
→ base_multiplier = 0.975
→ final_multiplier = 0.975^1.94 = 0.9519
→ adjusted_score = 35.20 * 0.9519 = 33.51 (-1.69 pts)
```

**Result**: Late-round TE receives -1.69 point penalty

---

### Example 8: Undrafted (Cameron Dicker) - VERY_POOR

**Scenario**: Week 9, evaluating K Cameron Dicker
**Player Data**:
- Position: K
- Team: LAC
- ADP: 108.58
- Current Score: 19.90 points

**Calculation**:
```
ADP = 108.58 >= 107.76 (VERY_POOR threshold)
→ VERY_POOR rating
→ base_multiplier = 0.95
→ final_multiplier = 0.95^1.94 = 0.9038
→ adjusted_score = 19.90 * 0.9038 = 17.99 (-1.91 pts)
```

**Result**: Kickers typically receive VERY_POOR or POOR ratings due to late-round ADP

---

### Example 9: No ADP Data (Null/None)

**Scenario**: Week 9, evaluating undrafted rookie
**Player Data**:
- Position: WR
- Team: Various
- ADP: None (not in ESPN ADP data)
- Current Score: 25.00 points

**Step 1: Handle None value**
```python
if val is None:
    multiplier, label = 1.0, 'NEUTRAL'
```

**Step 2: Apply neutral multiplier**
```
final_multiplier = 1.0
adjusted_score = 25.00 * 1.0 = 25.00 (no change)
reason = "ADP: NEUTRAL (1.00x)"
```

**Result**: Players without ADP data receive neutral treatment (no bonus/penalty)

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "ADP_SCORING": {
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "DECREASING",
      "STEPS": 26.940395226996877
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 1.9356728036133104
  }
}
```

### Configuration Fields

| Field | Type | Description | Current Value |
|-------|------|-------------|---------------|
| `THRESHOLDS.BASE_POSITION` | float | Starting point for threshold calculation | 0 |
| `THRESHOLDS.DIRECTION` | string | Threshold direction logic | "DECREASING" |
| `THRESHOLDS.STEPS` | float | Step size between threshold levels | 26.94 |
| `MULTIPLIERS.VERY_POOR` | float | Multiplier for very poor ADP | 0.95 |
| `MULTIPLIERS.POOR` | float | Multiplier for poor ADP | 0.975 |
| `MULTIPLIERS.GOOD` | float | Multiplier for good ADP | 1.025 |
| `MULTIPLIERS.EXCELLENT` | float | Multiplier for excellent ADP | 1.05 |
| `WEIGHT` | float | Exponent for multiplier adjustment | 1.94 |

### Threshold Calculation

**Direction**: `DECREASING` (lower values = better)

**Formula**:
```
BASE = 0
STEP = 26.94

EXCELLENT = BASE + (1 * STEP) = 0 + 26.94 = 26.94
GOOD = BASE + (2 * STEP) = 0 + 53.88 = 53.88
POOR = BASE + (3 * STEP) = 0 + 80.82 = 80.82
VERY_POOR = BASE + (4 * STEP) = 0 + 107.76 = 107.76
```

**Calculated Thresholds**:
- **EXCELLENT**: ADP 26.94 or lower (top ~2 rounds)
- **GOOD**: ADP 26.95-53.88 (rounds 3-5)
- **NEUTRAL**: ADP 53.89-80.81 (rounds 6-7)
- **POOR**: ADP 80.82-107.75 (rounds 8-9)
- **VERY_POOR**: ADP 107.76+ (round 10+)

### Weight Exponent Impact

**Current Weight**: 1.94

**Multiplier Transformations**:

| Rating | Base Multiplier | Weight Applied | Final Multiplier | Effect |
|--------|----------------|----------------|------------------|--------|
| EXCELLENT | 1.05 | 1.05^1.94 = 1.0989 | +9.89% | ~+5 pts on 50 pt player |
| GOOD | 1.025 | 1.025^1.94 = 1.0490 | +4.90% | ~+2.5 pts on 50 pt player |
| NEUTRAL | 1.0 | 1.0^1.94 = 1.0 | 0% | No change |
| POOR | 0.975 | 0.975^1.94 = 0.9519 | -4.81% | ~-2.4 pts on 50 pt player |
| VERY_POOR | 0.95 | 0.95^1.94 = 0.9038 | -9.62% | ~-4.8 pts on 50 pt player |

**Interpretation**: High weight (1.94) amplifies the multiplier effect significantly, making ADP a substantial factor in scoring.

### Configuration Tuning Guide

**Increasing ADP Importance**:
- Increase `WEIGHT` (e.g., 2.5, 3.0) → larger multiplier spread
- Increase `STEPS` (e.g., 40.0, 50.0) → more players reach EXCELLENT/GOOD tiers
- Increase base multipliers (e.g., EXCELLENT=1.10) → larger bonuses

**Decreasing ADP Importance**:
- Decrease `WEIGHT` (e.g., 1.0, 0.5) → dampens multiplier effect
- Decrease `STEPS` (e.g., 15.0, 10.0) → fewer players reach EXCELLENT/GOOD tiers
- Decrease base multipliers (e.g., EXCELLENT=1.02) → smaller bonuses

**Why Current Values?**:
- **STEPS=26.94**: Roughly 2-3 rounds per tier (12-team league)
- **WEIGHT=1.94**: Amplifies community consensus meaningfully (~±5-10%)
- **Optimized via simulation**: Maximizes draft helper win rate

---

## See Also

### Related Metrics
- **[01_normalization.md](01_normalization.md)** - Base score that ADP multiplier modifies
- **[03_player_rating_multiplier.md](03_player_rating_multiplier.md)** - Expert consensus (complements community ADP)
- **[05_performance_multiplier.md](05_performance_multiplier.md)** - Historical performance (validates/contradicts ADP)

### Implementation Files
- **`league_helper/util/player_scoring.py:485-493`** - ADP multiplier application
- **`league_helper/util/ConfigManager.py:297-298`** - ADP multiplier getter
- **`league_helper/util/ConfigManager.py:922-1008`** - Generic multiplier logic with decreasing thresholds
- **`utils/FantasyPlayer.py:98`** - average_draft_position field definition

### Configuration
- **`data/league_config.json`** - ADP_SCORING parameters
- **`data/players.csv`** - average_draft_position field

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - ADP multiplier application tests
- **`tests/league_helper/util/test_ConfigManager.py`** - ADP threshold and multiplier tests

### Documentation
- **[README.md](README.md)** - Scoring algorithm overview
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 9
**Documentation Version**: 1.0
**Code Version**: Week 9, 2025 NFL Season
