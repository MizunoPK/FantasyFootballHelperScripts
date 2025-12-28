# Step 12: Wind Scoring

Wind Scoring applies an additive bonus/penalty based on wind gust conditions, affecting only passing game and kicking positions.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 12 |
| Type | Additive Bonus/Penalty |
| Bonus Range | -3.0 to +3.0 points |
| Impact Scale | 60.0 |
| Data Source | `data/game_data.csv` |

## Purpose

Wind disrupts passing and kicking:
- **Calm conditions (<5 mph)**: Optimal for passing/kicking → Bonus points
- **Moderate wind (8-15 mph)**: Slightly affected → Small penalty
- **High wind (15-20 mph)**: Significantly affected → Moderate penalty
- **Extreme wind (>20 mph)**: Severely affected → Large penalty

This captures the selective impact of wind on aerial game positions only.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ❌ | Season-long value, not weekly weather |
| Starter Helper | ✅ | Weekly wind affects game-day passing/kicking |
| Trade Simulator | ❌ | Current week weather not relevant to trade value |

## Calculation

### Wind Gust Value

Wind is measured by maximum gust speed (not sustained wind):
- Gust speed in miles per hour (mph)
- Lower wind = better conditions

### Bonus Formula

```python
multiplier, tier = config.get_wind_multiplier(wind_gust)
bonus = ((IMPACT_SCALE * multiplier) - IMPACT_SCALE) * WEIGHT
adjusted_score = previous_score + bonus
```

### Threshold System

Wind uses **DECREASING** direction (lower wind = better):

Calculated from BASE_POSITION=0, STEPS=8:

| Wind Gust Range | Rating | Base Multiplier | Weighted (^1.0) | Bonus (scale=60.0) |
|-----------------|--------|-----------------|-----------------|---------------------|
| ≤8 mph | EXCELLENT | 1.05 | 1.05 | +3.0 pts |
| 9-16 mph | GOOD | 1.025 | 1.025 | +1.5 pts |
| 17-24 mph | AVERAGE | 1.0 | 1.0 | 0 pts |
| 25-32 mph | POOR | 0.975 | 0.975 | -1.5 pts |
| >32 mph | VERY_POOR | 0.95 | 0.95 | -3.0 pts |

### Example Calculation

**Game with 5 mph wind (EXCELLENT - calm)**:
- Wind gust: 5 mph
- Rating: EXCELLENT (≤8 mph)
- Base Multiplier: 1.05
- Weighted Multiplier: 1.05^1.0 = 1.05
- Bonus: (60.0 × 1.05) - 60.0 = +3.0
- If previous score = 167.5: Final = 167.5 + 3.0 = 170.5

**Game with 22 mph wind (AVERAGE - moderate wind)**:
- Wind gust: 22 mph
- Rating: AVERAGE (17-24 mph)
- Base Multiplier: 1.0
- Weighted Multiplier: 1.0^1.0 = 1.0
- Bonus: (60.0 × 1.0) - 60.0 = 0
- If previous score = 167.5: Final = 167.5 + 0 = 167.5

**Game with 28 mph wind (POOR - high wind)**:
- Wind gust: 28 mph
- Rating: POOR (25-32 mph)
- Base Multiplier: 0.975
- Weighted Multiplier: 0.975^1.0 = 0.975
- Bonus: (60.0 × 0.975) - 60.0 = -1.5
- If previous score = 167.5: Final = 167.5 - 1.5 = 166.0

## Data Sources

### Game Data File

**Source**: `data/game_data.csv`

| Column | Description | Example |
|--------|-------------|---------|
| `team` | NFL team abbreviation | BUF |
| `week` | NFL week number | 12 |
| `wind_gust` | Maximum wind gust in mph | 18 |
| `indoor` | Boolean flag for dome/indoor | False |

### Game Conditions Manager

**File**: `league_helper/util/GameDataManager.py`

```python
def get_game(team: str, week: int) -> Optional[GameData]:
    # Returns game data including wind_gust
    # Returns None if bye week or no data
```

### Indoor Game Handling

Games played in domes or retractable roof stadiums (when closed) are marked as `indoor=True`:
- Wind scoring is **skipped** for indoor games
- No bonus or penalty applied (indoor = no wind)

## Position Applicability

Wind **only affects** these positions:

| Position | Affected? | Reasoning |
|----------|-----------|-----------|
| **QB** | ✅ YES | Passing accuracy, deep ball trajectory |
| **WR** | ✅ YES | Route timing, catching passes in wind |
| **K** | ✅ YES | Field goal accuracy, kickoff distance |
| RB | ❌ NO | Rushing game not affected by wind |
| TE | ❌ NO | Mostly short/intermediate routes, blocking role |
| DST | ❌ NO | Defensive performance not directly affected |

**Constant**: `Constants.WIND_AFFECTED_POSITIONS = ['QB', 'WR', 'K']`

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_wind_scoring()` (lines 772-825)

```python
def _apply_wind_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    # Skip if position not affected by wind
    if p.position not in Constants.WIND_AFFECTED_POSITIONS:
        return player_score, ""

    # Skip if no game data manager
    if not self.game_data_manager:
        return player_score, ""

    # Get game for player's team
    game = self.game_data_manager.get_game(p.team, self.config.current_nfl_week)

    # Skip if bye week (no game)
    if not game:
        return player_score, ""

    # Skip if indoor game (no wind effects)
    if game.indoor:
        return player_score, ""

    # Skip if no wind data
    if game.wind_gust is None:
        return player_score, ""

    # Get multiplier (lower wind = better = higher multiplier)
    multiplier, tier = self.config.get_wind_multiplier(game.wind_gust)

    # Calculate additive bonus
    impact_scale = self.config.wind_scoring.get('IMPACT_SCALE', 60.0)
    weight = self.config.wind_scoring.get('WEIGHT', 1.0)
    bonus = ((impact_scale * multiplier) - impact_scale) * weight

    return player_score + bonus, reason
```

### Position Filter (Early Exit)

**Important**: Wind scoring checks position **first** before any other logic:

```python
if p.position not in Constants.WIND_AFFECTED_POSITIONS:
    return player_score, ""  # Skip immediately for RB, TE, DST
```

This ensures RB, TE, and DST players never receive wind adjustments, even in extreme conditions.

### ConfigManager Method

**File**: `league_helper/util/ConfigManager.py`

**Method**: `get_wind_multiplier()` (lines 433-446)

```python
def get_wind_multiplier(self, wind_gust: float) -> Tuple[float, str]:
    """Get wind multiplier based on gust speed."""
    return self._get_multiplier(self.wind_scoring, wind_gust, rising_thresholds=False)
```

## Configuration

**league_config.json**:
```json
{
  "WIND_SCORING": {
    "IMPACT_SCALE": 60.0,
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "DECREASING",
      "STEPS": 8
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 1.0
  }
}
```

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `IMPACT_SCALE` | 60.0 | Scaling factor for bonus/penalty magnitude |
| `WEIGHT` | 0.0 (disabled) | Multiplier for final bonus (0 = disabled by default) |
| `THRESHOLDS.STEPS` | 8 | Wind threshold step size (8 mph per tier) |

**Note**: Default `WEIGHT` is 0.0 (disabled) for backward compatibility. Set to 1.0 to enable wind scoring.

## Real Player Example

### Example 1: QB in Calm Conditions

**Josh Allen (QB, BUF)** - Week 12 at home:

| Metric | Value |
|--------|-------|
| Game Location | Buffalo (outdoor) |
| Wind Gust | 6 mph |
| Previous Score | 170.33 |
| Position | QB (affected ✅) |
| Rating | EXCELLENT (≤8 mph) |
| Bonus | +3.0 pts |
| Adjusted Score | 173.33 |

**Reason String**: `"Wind: 6mph (EXCELLENT, +3.0 pts)"`

### Example 2: QB in High Wind

**Patrick Mahomes (QB, KC)** - Hypothetical game in Chicago:

| Metric | Value |
|--------|-------|
| Game Location | Chicago (outdoor) |
| Wind Gust | 26 mph |
| Previous Score | 165.0 |
| Position | QB (affected ✅) |
| Rating | POOR (25-32 mph) |
| Bonus | -1.5 pts |
| Adjusted Score | 163.5 |

**Reason String**: `"Wind: 26mph (POOR, -1.5 pts)"`

### Example 3: RB (Not Affected)

**Derrick Henry (RB, BAL)** - Same game as Example 2:

| Metric | Value |
|--------|-------|
| Game Location | Chicago (outdoor) |
| Wind Gust | 26 mph |
| Previous Score | 155.0 |
| Position | RB (not affected ❌) |
| Bonus | Skipped |
| Adjusted Score | 155.0 (unchanged) |

**Reason String**: `""` (empty - not affected)

### Example 4: Kicker in Extreme Wind

**Justin Tucker (K, BAL)** - Hypothetical extreme weather:

| Metric | Value |
|--------|-------|
| Game Location | Outdoor stadium |
| Wind Gust | 35 mph |
| Previous Score | 120.0 |
| Position | K (affected ✅) |
| Rating | VERY_POOR (>32 mph) |
| Bonus | -3.0 pts |
| Adjusted Score | 117.0 |

**Reason String**: `"Wind: 35mph (VERY_POOR, -3.0 pts)"`

## Edge Cases

### Indoor Games

For games in domes or with closed roofs:
- `game.indoor = True`
- Wind scoring is **completely skipped** (even for QB/WR/K)
- No bonus or penalty applied
- Empty reason string returned

### Bye Weeks

Players on bye have no game:
- `game = None`
- Wind scoring skipped
- No bonus or penalty

### Missing Wind Data

If wind data is unavailable:
- `game.wind_gust = None`
- Wind scoring skipped
- No bonus or penalty

### Unaffected Positions

For RB, TE, DST positions:
- Position check **fails immediately** (line 788)
- All other logic skipped
- No bonus or penalty
- Empty reason string

## Why Only QB, WR, K?

### Positions Excluded (RB, TE, DST)

**Running Backs (RB):**
- Rushing game is ground-based
- Wind doesn't affect running lanes or ball carriers
- Receiving work is typically short-range (less wind impact)

**Tight Ends (TE):**
- Routes are mostly short/intermediate (5-15 yards)
- Strong blocking role (unaffected by wind)
- Not primary deep threat targets
- Design decision: TE more similar to RB than WR in wind impact

**Defense/Special Teams (DST):**
- Both offense and defense affected equally by wind (neutral)
- Kicking plays (punts, FG attempts) are opponent's, not DST's
- Wind doesn't systematically favor defense

### Positions Included (QB, WR, K)

**Quarterbacks (QB):**
- Passing accuracy severely affected by wind
- Deep ball trajectory significantly altered
- Ball flight time increases (more wind exposure)

**Wide Receivers (WR):**
- Route timing disrupted by wind resistance
- Catching difficulty increases (ball movement)
- Deep routes most affected

**Kickers (K):**
- Field goal accuracy heavily affected
- Distance reduced on long attempts (40+ yards)
- Trajectory changes affect success rate

## Relationship to Other Steps

- **Input**: Temperature-adjusted score from Step 11
- **Output**: Wind-adjusted score
- **Next Step**: Location modifier applied (Step 13)

Wind is the second of three game conditions scoring steps (11-13) and the most position-selective of all scoring steps.

## Strategic Insights

### When Wind Matters Most

**High Impact Games:**
- Coastal cities (e.g., Buffalo, Chicago, Cleveland) in fall/winter
- Open-air stadiums with swirling winds
- Games with 20+ mph gusts (avoid WR/QB)
- Kickers facing long FG attempts in high wind

**Low Impact Games:**
- Any indoor game (dome/closed roof)
- Calm weather days (<10 mph)
- Games in wind-protected stadiums

### Position-Specific Strategy

**For QBs:**
- Avoid starting QBs in 20+ mph winds (especially if outdoor)
- Prioritize QBs in domes during windy weather weeks
- Check weekly weather forecasts for Sunday game conditions

**For WRs:**
- Deep threat WRs (high aDOT) most affected by wind
- Slot WRs (short routes) less affected
- Consider TEs as safer alternatives in high wind

**For Kickers:**
- Avoid kickers in 20+ mph winds entirely
- Prioritize dome kickers during windy weather weeks
- FG attempts 40+ yards become very risky

**For RBs:**
- Wind is an **advantage** for RBs (teams run more in wind)
- Consider RB volume increases in high-wind games
- This is NOT captured by current scoring (RBs not adjusted)

## Historical Context

Wind scoring was added in **v2.1 (2025-11-26)** as part of the game conditions scoring enhancement. It addresses the gap identified in streaming research where wind conditions significantly impact QB, WR, and K performance.

## Related Documentation

- Step 11: Temperature Scoring (affects all positions)
- Step 13: Location Scoring (home/away/international)
- `GameDataManager` implementation
- `docs/research/scoring_gap_analysis.md` - Weather metrics identified as high priority
- `Constants.WIND_AFFECTED_POSITIONS` definition

## Comparison to Temperature (Step 11)

| Factor | Temperature (Step 11) | Wind (Step 12) |
|--------|----------------------|----------------|
| **Positions Affected** | All positions | QB, WR, K only |
| **Impact Scale** | 50.0 | 60.0 |
| **Bonus Range** | ±2.5 pts | ±3.0 pts |
| **Measurement** | Distance from 60°F | Wind gust mph |
| **Indoor Games** | Skipped | Skipped |
| **Strategic Value** | Moderate (universal) | High (position-specific) |
