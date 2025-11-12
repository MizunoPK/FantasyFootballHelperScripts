# Player Rating Multiplier (Step 3)

## Overview

**Type**: Multiplicative (percentage adjustment)
**Effect**: ±10.8% (0.898x to 1.108x with default weight=2.094)
**Base Multipliers**: 0.95x to 1.05x (±5% before weight exponent)
**When Applied**: Step 3 of 10-step scoring algorithm
**Purpose**: Adjust scores based on expert consensus position-specific rankings

The Player Rating Multiplier uses ESPN's weekly-updated expert consensus rankings to evaluate each player's perceived value within their position. Rankings reflect aggregated expert opinions on Rest of Season (ROS) performance expectations and are updated each week during the season. Higher-rated players (top-tier at position) receive a score boost, while lower-rated players receive a penalty.

**Key Characteristics**:
- **Position-specific normalization**: Each position (QB, RB, WR, TE, K, DST) normalized independently
- **Weekly updates**: Uses rankings from current NFL week
- **ROS projections**: Rankings represent expected future performance through end of season
- **Expert consensus**: Aggregates multiple expert opinions (ESPN's averageRank field)
- **Adaptive scaling**: Adjusts to actual number of ranked players each week
- **1-100 scale**: Normalized ratings where 100 = best player at position, 1 = worst player at position

---

## Algorithm Overview

The player rating calculation uses a **three-pass processing approach**:

```
Pass 1: Preprocessing  → Collect min/max positional ranks
Pass 2: Main Loop      → Extract player data and store ranks
Pass 3: Post-Processing → Normalize all ratings to 1-100 scale
```

This ensures all ratings are normalized relative to the actual distribution of players at each position.

---

## Normalization Formula

### Core Formula

```python
normalized_rating = 1 + ((rank - max_rank) / (min_rank - max_rank)) * 99
```

### Variables

| Variable | Description | Example (RB Position) |
|----------|-------------|----------------------|
| `rank` | Player's positional rank from ESPN | 5.0 (RB5) |
| `min_rank` | Best rank for position | 1.1 (RB1) |
| `max_rank` | Worst rank for position | 50.9 (RB50) |
| `normalized_rating` | Output rating (1-100 scale) | 92.1 |

### Scale Direction

- **100** = Best player at position (lowest rank number)
- **50** = Middle player at position
- **1** = Worst player at position (highest rank number)

### Mathematical Properties

1. **Linear transformation**: Preserves relative differences between players
2. **Position-independent**: Each position uses same 1-100 scale
3. **Automatic adjustment**: Adapts to varying numbers of ranked players
4. **No arbitrary breakpoints**: Unlike tier-based systems, every rank has a precise rating

---

## Calculation Examples

### Example 1: QB Position (Week 10, 2025)

**Position Data**:
- Ranked players: 42
- Best rank (QB1): 1.0
- Worst rank (QB42): 25.9

**Player Ratings**:

| Player | Rank | Formula | Rating | Interpretation |
|--------|------|---------|--------|----------------|
| QB1 | 1.0 | `1 + ((1.0 - 25.9) / (1.0 - 25.9)) * 99` | **100.0** | Elite (best QB) |
| QB5 | 5.0 | `1 + ((5.0 - 25.9) / (1.0 - 25.9)) * 99` | **84.1** | Top-tier starter |
| QB13 | 13.0 | `1 + ((13.0 - 25.9) / (1.0 - 25.9)) * 99` | **51.6** | Fringe starter |
| QB25 | 25.0 | `1 + ((25.0 - 25.9) / (1.0 - 25.9)) * 99` | **5.1** | Deep bench |
| QB42 | 25.9 | `1 + ((25.9 - 25.9) / (1.0 - 25.9)) * 99` | **1.0** | Worst ranked QB |

### Example 2: RB Position (Week 10, 2025)

**Position Data**:
- Ranked players: 75
- Best rank (RB1): 1.1
- Worst rank (RB75): 50.9

**Player Ratings**:

| Player | Rank | Formula | Rating | Interpretation |
|--------|------|---------|--------|----------------|
| RB1 | 1.1 | `1 + ((1.1 - 50.9) / (1.1 - 50.9)) * 99` | **100.0** | Elite (best RB) |
| RB10 | 10.0 | `1 + ((10.0 - 50.9) / (1.1 - 50.9)) * 99` | **82.8** | RB1 starter |
| RB25 | 25.0 | `1 + ((25.0 - 50.9) / (1.1 - 50.9)) * 99` | **52.6** | Flex/RB2 |
| RB50 | 50.0 | `1 + ((50.0 - 50.9) / (1.1 - 50.9)) * 99` | **3.0** | Deep bench |

### Example 3: WR Position (Week 10, 2025)

**Position Data**:
- Ranked players: 85
- Best rank (WR1): 1.5
- Worst rank (WR85): 60.9

**Player Ratings**:

| Player | Rank | Formula | Rating | Interpretation |
|--------|------|---------|--------|----------------|
| WR1 | 1.5 | `1 + ((1.5 - 60.9) / (1.5 - 60.9)) * 99` | **100.0** | Elite (best WR) |
| WR12 | 12.0 | `1 + ((12.0 - 60.9) / (1.5 - 60.9)) * 99` | **82.7** | WR1 starter |
| WR30 | 30.0 | `1 + ((30.0 - 60.9) / (1.5 - 60.9)) * 99` | **52.7** | Flex/WR2 |
| WR60 | 60.0 | `1 + ((60.0 - 60.9) / (1.5 - 60.9)) * 99` | **2.5** | Waiver wire |

---

## Implementation Details

### Data Collection (`player-data-fetcher/espn_client.py`)

#### Pass 1: Preprocessing (Lines 1290-1385)

**Purpose**: Collect min/max positional ranks across all players

**Process**:
1. Loop through all 1000+ players from ESPN API
2. Extract positional rank for each player (same logic as main loop)
3. Track min, max, and count for each position
4. Store in `position_rank_ranges` dictionary

**Data Structure**:
```python
position_rank_ranges = {
    'QB': {'min': 1.0, 'max': 25.9, 'count': 42},
    'RB': {'min': 1.1, 'max': 50.9, 'count': 75},
    'WR': {'min': 1.5, 'max': 60.9, 'count': 85},
    'TE': {'min': 1.1, 'max': 25.9, 'count': 37},
    'K': {'min': 1.0, 'max': 20.9, 'count': 32},
    'DST': {'min': 1.0, 'max': 20.6, 'count': 23}
}
```

**Logging Output**:
```
INFO - Collecting positional rank ranges for normalization (processing 1071 players)
INFO - Position rank ranges collected for 6 positions:
INFO -   DST: 1.0-20.6 (23 players with ranks)
INFO -   K: 1.0-20.9 (32 players with ranks)
INFO -   QB: 1.0-25.9 (42 players with ranks)
INFO -   RB: 1.1-50.9 (75 players with ranks)
INFO -   TE: 1.1-25.9 (37 players with ranks)
INFO -   WR: 1.5-60.9 (85 players with ranks)
```

#### Pass 2: Main Loop (Lines 1386-1645)

**Purpose**: Extract player data and store positional ranks

**Process**:
1. For each player, extract positional rank from ESPN API
2. Store rank in temporary dictionary: `player_positional_ranks[player_id] = rank`
3. Set `player_rating = None` temporarily (will be calculated in Pass 3)
4. Continue extracting other player data (projections, ADP, etc.)

**Rank Extraction Logic**:
- **Week 1**: Use draft rankings converted to positional rankings
- **Week 2+**: Use current week's ROS consensus rankings from `rankings[str(CURRENT_NFL_WEEK)]`
- **Fallback**: Use most recent available week if current week missing
- **Last resort**: Use pre-season rankings if no weekly data exists

#### Pass 3: Post-Processing (Lines 1646-1727)

**Purpose**: Normalize all player ratings to 1-100 scale

**Process**:
1. Loop through all parsed player projections
2. For each player with a stored positional rank:
   - Get min/max for their position from `position_rank_ranges`
   - Apply normalization formula
   - Set `player_rating` to normalized value
3. Validate all ratings are between 1-100
4. Log normalization summary

**Logging Output**:
```
INFO - Normalizing player ratings for 294 players with positional ranks
INFO - Player rating normalization complete: 294 normalized, 777 using fallback or None
```

### Multiplier Application (`league_helper/util/player_scoring.py`)

**Location**: Lines 495-503

**Process**:
1. Retrieve player's normalized rating (1-100 scale)
2. Determine which threshold range the rating falls into
3. Select base multiplier from configuration
4. Apply weight exponent to the base multiplier: `adjusted_multiplier = base_multiplier ** weight`
5. Multiply player's base score by adjusted multiplier

**Code Flow**:
```python
# Step 1: Get player rating multiplier
def _apply_player_rating_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    multiplier, rating = self.config.get_player_rating_multiplier(p.player_rating)
    reason = f"Player Rating: {rating} ({multiplier:.2f}x)"
    return player_score * multiplier, reason

# Step 2: ConfigManager determines multiplier based on thresholds
def get_player_rating_multiplier(self, player_rating: float) -> Tuple[float, str]:
    return self._get_multiplier(
        self.config[self.keys.PLAYER_RATING_SCORING],
        player_rating,
        rising_thresholds=True
    )

# Step 3: Dynamic threshold calculation
def _get_multiplier(self, scoring_dict: Dict[str, Any], val, rising_thresholds=True):
    # Calculate thresholds dynamically from STEPS parameter
    base = scoring_dict[self.keys.THRESHOLDS][self.keys.BASE_POSITION]
    steps = scoring_dict[self.keys.THRESHOLDS][self.keys.STEPS]

    excellent_threshold = base + (3 * steps)
    good_threshold = base + (2 * steps)
    poor_threshold = base + (1 * steps)

    # Select base multiplier based on rating
    if rising_thresholds:  # Higher values = better
        if val >= excellent_threshold:
            multiplier = scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT]
            label = self.keys.EXCELLENT
        elif val >= good_threshold:
            multiplier = scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD]
            label = self.keys.GOOD
        elif val >= poor_threshold:
            multiplier = scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR]
            label = self.keys.POOR
        else:
            multiplier = scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR]
            label = self.keys.VERY_POOR

    # Apply weight exponent
    weight = scoring_dict[self.keys.WEIGHT]
    adjusted_multiplier = multiplier ** weight

    return adjusted_multiplier, label
```

**Configuration Structure** (from `league_config.json`):
```json
"PLAYER_RATING_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 26.670328317807673
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 2.093715281560986
}
```

**Threshold Calculation** (with example config):
- `BASE_POSITION` = 0
- `STEPS` = 26.67
- **Excellent** threshold = 0 + (3 × 26.67) = **80.0**
- **Good** threshold = 0 + (2 × 26.67) = **53.3**
- **Poor** threshold = 0 + (1 × 26.67) = **26.7**

**Multiplier Selection** (rating scale 1-100, higher = better):
- Rating ≥ 80.0 → `EXCELLENT` multiplier (1.05)
- Rating ≥ 53.3 → `GOOD` multiplier (1.025)
- Rating ≥ 26.7 → `POOR` multiplier (0.975)
- Rating < 26.7 → `VERY_POOR` multiplier (0.95)

**Weight Exponent Application**:
With `WEIGHT = 2.094`:
- `EXCELLENT`: 1.05^2.094 = **1.108** (+10.8%)
- `GOOD`: 1.025^2.094 = **1.052** (+5.2%)
- `POOR`: 0.975^2.094 = **0.948** (-5.2%)
- `VERY_POOR`: 0.95^2.094 = **0.898** (-10.2%)

---

## Data Sources

### ESPN API Rankings Structure

The rankings data comes from ESPN's hidden API endpoint for player projections. Rankings are stored in a nested structure keyed by week:

```json
{
  "player": {
    "id": "4372016",
    "firstName": "Saquon",
    "lastName": "Barkley",
    "rankings": {
      "0": [...],    // Pre-season ROS projection (static)
      "1": [...],    // Week 1 ROS projection snapshot
      "2": [...],    // Week 2 ROS projection snapshot
      "9": [...],    // Week 9 ROS projection snapshot
      "10": [        // Week 10 ROS projection snapshot (current)
        {
          "rankType": "PPR",
          "slotId": 2,           // 2 = RB position
          "averageRank": 2.5     // RB2.5 in expert consensus
        }
      ]
    }
  }
}
```

### Ranking Key Selection

| Scenario | Key Used | Rationale |
|----------|----------|-----------|
| Week 1 | `"0"` (pre-season) | Week 1 expert rankings may be sparse |
| Week 2-18 | `str(CURRENT_NFL_WEEK)` | Most up-to-date expert consensus |
| Missing current week | Most recent prior week | Fallback to latest available data |
| No weekly data | `"0"` (pre-season) | Last resort fallback |

### averageRank Field

The `averageRank` value represents the **consensus expert ranking** for a player's Rest of Season performance:
- Aggregates rankings from multiple fantasy experts
- Updated weekly as expert opinions change
- Position-specific (RB1-RB50, WR1-WR60, etc.)
- Decimal values indicate ties or averaging (e.g., 2.5 = between RB2 and RB3)

### Verification: ROS vs Weekly Rankings

**Proof these are ROS (Rest of Season) rankings, not weekly matchup rankings**:

During Week 6 (bye weeks), multiple top players on bye were still ranked #1 at their position:
- **Puka Nacua** (WR, LAR): Ranked WR1 during his bye week
- **De'Von Achane** (RB, MIA): Ranked RB5 during his bye week

This is **impossible** for weekly matchup rankings (bye week = 0 projected points). This definitively proves these are ROS projections representing expected future performance through end of season.

---

## Edge Cases and Error Handling

### 1. Division by Zero (Single Player Position)

**Scenario**: Position has only one ranked player (min_rank == max_rank)

**Formula Issue**:
```python
normalized = 1 + ((rank - max_rank) / (min_rank - max_rank)) * 99
# Division by zero when min_rank == max_rank
```

**Solution**: Default to neutral rating
```python
if min_rank == max_rank:
    player_rating = 50.0  # Neutral rating
```

**Logging**:
```
DEBUG - Single rank for position K (rank=5.0), using neutral rating 50.0 for Player Name
```

### 2. Missing Positional Rank

**Scenario**: Player has no rank in ESPN API (new players, injuries, etc.)

**Solution**: Use fallback calculation based on overall draft rank
```python
if positional_rank is None:
    # Apply draft rank formula (preserved for backward compatibility)
    # Tiered formula based on overall draft position
    if draft_rank <= 50:
        player_rating = 100.0 - (draft_rank - 1) * 0.4
    # ... additional tiers ...
```

**Logging**:
```
WARNING - Rankings object missing for Player Name (ID: 12345), using draft rank fallback
```

### 3. Position Not in Ranges Dictionary

**Scenario**: Player's position wasn't found during preprocessing (shouldn't happen)

**Solution**: Log warning and leave rating as None
```python
if position not in position_rank_ranges:
    logger.warning(f"Position {position} not in rank ranges for {player.name}")
    player_rating = None  # Downstream code will handle missing rating
```

### 4. Rating Out of Range

**Scenario**: Floating point arithmetic produces value slightly outside 1-100

**Solution**: Validation with logging
```python
if not (1.0 <= normalized <= 100.0):
    logger.warning(
        f"Normalized rating out of range for {player.name}: {normalized:.2f}"
    )
```

**Note**: This should never occur with correct min/max ranges, but validation catches potential bugs.

### 5. Extreme Ratings (Edge of Scale)

**Scenario**: Player receives rating of exactly 1.0 or 100.0

**Logging**: Log for visibility
```python
if normalized >= 99.5 or normalized <= 1.5:
    logger.debug(
        f"Extreme rating for {player.name} ({position}): {normalized:.1f}"
    )
```

**Interpretation**: Normal for #1 and last-ranked players at each position

---

## Performance Characteristics

### Processing Overhead

**Preprocessing Pass**:
- Additional loop through ~1000 players
- Lightweight operations (rank extraction only)
- Overhead: ~5-10% of total processing time

**Post-Processing Pass**:
- Loop through parsed projections (~300-700 players)
- Simple arithmetic operations
- Overhead: ~2-3% of total processing time

**Total Impact**: ~10-15% increase in player data fetcher runtime (negligible, still completes in <15 minutes)

### Memory Usage

**Temporary Data Structures**:
```python
position_rank_ranges = {...}      # ~6 positions × 3 fields = negligible
player_positional_ranks = {...}   # ~300-700 entries × 8 bytes = ~5 KB
```

**Memory Impact**: Minimal (< 10 KB additional memory)

---

## Data Model

### ESPNPlayerData Model

**File**: `player-data-fetcher/player_data_models.py`

**Field Definition** (Line 45):
```python
player_rating: Optional[float] = None  # 0-100 scale normalized from ESPN position-specific rankings (100=best, 1=worst within position)
```

**Type**: `Optional[float]`
- `None` = No rating available (no rankings data, filtered player, etc.)
- `1.0 - 100.0` = Normalized position-specific rating

**CSV Output**:
- Column: `player_rating`
- Format: Decimal with 1-2 decimal places (e.g., `95.3`, `42.7`)
- Missing values: Empty string or `None`

---

## Configuration Parameters

### Full Configuration Structure

**File**: `data/league_config.json`

**Section**: `PLAYER_RATING_SCORING`

```json
"PLAYER_RATING_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 26.670328317807673
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 2.093715281560986
}
```

### Parameter Breakdown

#### THRESHOLDS

**Purpose**: Define dynamic threshold ranges for categorizing player ratings

| Parameter | Type | Description | Example Value |
|-----------|------|-------------|---------------|
| `BASE_POSITION` | float | Starting point for threshold calculations | 0 |
| `DIRECTION` | string | "INCREASING" (higher = better) or "DECREASING" | "INCREASING" |
| `STEPS` | float | Gap between threshold levels | 26.67 |

**Threshold Calculation**:
```python
poor_threshold = BASE_POSITION + (1 * STEPS)       # 0 + 26.67 = 26.67
good_threshold = BASE_POSITION + (2 * STEPS)       # 0 + 53.34 = 53.34
excellent_threshold = BASE_POSITION + (3 * STEPS)  # 0 + 80.01 = 80.01
```

**Effect**: With `STEPS = 26.67`:
- Rating < 26.67 → VERY_POOR
- Rating 26.67-53.33 → POOR
- Rating 53.34-79.99 → GOOD
- Rating ≥ 80.00 → EXCELLENT

**Customization**: Adjust `STEPS` to change threshold sensitivity:
- **Smaller STEPS** (e.g., 20): Tighter ranges, more players reach higher tiers
- **Larger STEPS** (e.g., 33): Wider ranges, fewer players reach higher tiers

#### MULTIPLIERS

**Purpose**: Define base multiplier values for each rating tier

| Tier | Default Value | Effect | Description |
|------|---------------|--------|-------------|
| `EXCELLENT` | 1.05 | +5% base | Elite players at position |
| `GOOD` | 1.025 | +2.5% base | Quality starters |
| `POOR` | 0.975 | -2.5% base | Below average |
| `VERY_POOR` | 0.95 | -5% base | Deep bench/waiver |

**Customization**: Adjust multipliers to change tier impact:
```json
"MULTIPLIERS": {
  "VERY_POOR": 0.90,   // Increase penalty to -10% base
  "POOR": 0.97,
  "GOOD": 1.03,
  "EXCELLENT": 1.10    // Increase bonus to +10% base
}
```

#### WEIGHT

**Purpose**: Controls how strongly multipliers affect final scores via exponentiation

**Formula**: `adjusted_multiplier = base_multiplier ** WEIGHT`

**Effect of Different Weights**:

| Weight | EXCELLENT (1.05) | GOOD (1.025) | POOR (0.975) | VERY_POOR (0.95) |
|--------|------------------|--------------|--------------|------------------|
| 0.5 | 1.025 (+2.5%) | 1.012 (+1.2%) | 0.987 (-1.3%) | 0.975 (-2.5%) |
| 1.0 | 1.050 (+5.0%) | 1.025 (+2.5%) | 0.975 (-2.5%) | 0.950 (-5.0%) |
| 2.0 | 1.103 (+10.3%) | 1.051 (+5.1%) | 0.951 (-4.9%) | 0.903 (-9.7%) |
| 2.094 | 1.108 (+10.8%) | 1.052 (+5.2%) | 0.948 (-5.2%) | 0.898 (-10.2%) |

**Current Value**: `2.094` (amplifies differences between tiers)

**Customization**:
- **Lower weight** (e.g., 0.5): Dampens multiplier effect, reduces impact of rankings
- **Higher weight** (e.g., 3.0): Amplifies multiplier effect, increases impact of rankings

### Example Customization Scenarios

#### Scenario 1: Reduce Impact of Player Ratings

```json
"PLAYER_RATING_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 33.33  // Wider ranges
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.97,   // Smaller penalties
    "POOR": 0.985,
    "GOOD": 1.015,
    "EXCELLENT": 1.03    // Smaller bonuses
  },
  "WEIGHT": 1.0  // No amplification
}
```

**Result**: ±3% max effect, wider threshold ranges

#### Scenario 2: Increase Impact of Player Ratings

```json
"PLAYER_RATING_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 20.0  // Tighter ranges
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.90,   // Larger penalties
    "POOR": 0.95,
    "GOOD": 1.05,
    "EXCELLENT": 1.10    // Larger bonuses
  },
  "WEIGHT": 2.5  // Strong amplification
}
```

**Result**: ±15-20% max effect, tighter threshold ranges

---

## Simulation Data

### Normalization Script

**File**: `simulation/normalize_player_ratings.py`

**Purpose**: One-time script to normalize historical simulation CSV files

**Process**:
1. Read `players_projected_backup.csv` and `players_actual_backup.csv`
2. Calculate position-specific min/max from backup data
3. Apply same normalization formula as ESPN client
4. Write `players_projected.csv` and `players_actual.csv`

**Usage**:
```bash
cd simulation
python normalize_player_ratings.py
```

**Output**:
```
INFO - Position rank ranges collected for 6 positions:
INFO -   WR: 15.0-100.0 (270 players)
INFO -   RB: 15.0-99.6 (163 players)
INFO -   QB: 15.0-90.4 (101 players)
INFO -   TE: 15.0-77.2 (150 players)
INFO -   K: 15.0-46.2 (40 players)
INFO -   DST: 23.1-49.2 (32 players)
INFO - Normalized 756 players, 20 using fallback/None
```

**Note**: Script only needs to run once to migrate from old tier-based ratings to normalized ratings.

---

## Validation and Quality Checks

### Automated Validation

1. **Range Check**: All ratings must be between 1.0 and 100.0
2. **Count Verification**: Normalized count + fallback count = total players
3. **Fallback Threshold**: Warning if >10% of players use fallback
4. **Extreme Value Logging**: Log players with ratings at edges (1.0 or 100.0)

### Manual Verification

**Recommended Checks After Data Fetch**:

1. **Position Distribution**:
   ```bash
   # Check player_rating distribution by position
   cat data/players.csv | grep "^[^,]*,[^,]*,[^,]*,QB," | cut -d',' -f11 | sort -n
   ```

2. **Top Players**:
   - Verify elite players (RB1, WR1, QB1) have ratings near 100
   - Check that ratings align with expert consensus (ESPN, FantasyPros, etc.)

3. **Position Counts**:
   - Verify reasonable numbers of ranked players per position
   - QB: ~30-50, RB: ~50-80, WR: ~60-100, TE: ~30-50, K: ~30-40, DST: ~20-30

### Logging Levels

**INFO**: Key milestones and summaries
```
INFO - Position rank ranges collected for 6 positions
INFO - Player rating normalization complete: 294 normalized, 777 using fallback
```

**WARNING**: Recoverable issues
```
WARNING - High fallback usage: 15.2% of players using fallback or have no rating
WARNING - Rankings object missing for Player Name, using draft rank fallback
```

**DEBUG**: Detailed progress
```
DEBUG - Normalized 100 player ratings...
DEBUG - Extreme rating for Player Name (QB): 100.0 (rank=1.0)
```

---

## Best Practices

### For League Administrators

1. **Run fetcher weekly**: Keep rankings current with latest expert consensus
2. **Monitor fallback percentage**: >15% may indicate ESPN API issues
3. **Verify top players**: Spot-check elite players have appropriate ratings
4. **Review position counts**: Ensure reasonable distribution across positions

### For Developers

1. **Never modify normalization formula**: Changes break historical comparisons
2. **Log extensively**: DEBUG logs help diagnose rating calculation issues
3. **Handle None gracefully**: Downstream code must handle missing ratings
4. **Test edge cases**: Single-player positions, division by zero, etc.
5. **Validate ranges**: Assert all normalized values are 1-100

### For Data Analysis

1. **Compare across positions**: Normalized scale allows cross-position comparison
2. **Track changes over time**: Player ratings evolve as expert consensus shifts
3. **Correlation with ADP**: Higher ratings should correlate with lower ADP
4. **Outlier identification**: Large rating-ADP divergences may indicate value

---

## Troubleshooting

### Issue: All Ratings Are None

**Cause**: ESPN API not returning rankings data

**Check**:
```bash
# Verify ESPN API response contains rankings
curl "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/..." | jq '.players[0].player.rankings'
```

**Solution**: ESPN API may be down or changed structure. Check API documentation.

### Issue: Ratings All Near 50

**Cause**: All players have similar ranks (min ≈ max)

**Check**: Review preprocessing logs for position ranges
```
INFO -   QB: 5.0-6.0 (42 players with ranks)  # Very narrow range!
```

**Solution**: ESPN rankings may be incomplete. Verify API is returning full data.

### Issue: High Fallback Percentage

**Cause**: Many players missing positional rankings

**Common Reasons**:
- Rookies/new players not yet ranked
- Injured players removed from rankings
- ESPN hasn't updated rankings this week

**Solution**: Normal if <15%. If >20%, investigate ESPN API data quality.

### Issue: Rating Calculation Errors

**Symptoms**: Errors during normalization, ratings outside 1-100

**Debug Steps**:
1. Check preprocessing logs for position ranges
2. Verify min < max for all positions
3. Review player's specific rank value
4. Check for NaN or infinity in calculations

**Logging**:
```python
logger.error(f"Error normalizing rating for {player.name}: {e}")
```

---

## Summary

The Player Rating Multiplier provides a **position-specific, dynamically-normalized score adjustment** based on expert consensus rankings. By normalizing each position independently to a 1-100 scale, the system:

✅ **Accounts for position depth**: More WRs ranked than QBs
✅ **Adapts weekly**: Rankings change as expert opinions evolve
✅ **Enables comparison**: Same scale across all positions
✅ **Handles edge cases**: Division by zero, missing data, etc.
✅ **Preserves accuracy**: Linear transformation maintains relative differences

The three-pass processing approach ensures all ratings are calculated relative to the actual distribution of ranked players each week, providing a robust and fair valuation system for fantasy football scoring.
