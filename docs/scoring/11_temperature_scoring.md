# Step 11: Temperature Scoring

Temperature Scoring applies an additive bonus/penalty based on weather temperature conditions at game time.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 11 |
| Type | Additive Bonus/Penalty |
| Bonus Range | -2.5 to +2.5 points |
| Impact Scale | 50.0 |
| Data Source | `data/game_data.csv` |

## Purpose

Temperature affects player performance:
- **Ideal temperature (~60°F)**: Optimal playing conditions → No adjustment
- **Extreme cold (<30°F)**: Reduced performance → Penalty points
- **Extreme heat (>90°F)**: Reduced performance → Penalty points

This captures the environmental impact of weather on all positions.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ❌ | Season-long value, not weekly weather |
| Starter Helper | ✅ | Weekly weather affects game-day performance |
| Trade Simulator | ❌ | Current week weather not relevant to trade value |

## Calculation

### Temperature Distance Formula

```python
ideal_temp = 60  # Fahrenheit
temp_distance = abs(actual_temperature - ideal_temp)
```

The distance represents how far the actual temperature deviates from the ideal playing conditions.

### Bonus Formula

```python
multiplier, tier = config.get_temperature_multiplier(temp_distance)
bonus = ((IMPACT_SCALE * multiplier) - IMPACT_SCALE) * WEIGHT
adjusted_score = previous_score + bonus
```

### Threshold System

Temperature uses **DECREASING** direction (lower distance = better):

Calculated from BASE_POSITION=0, STEPS=10:

| Temp Distance | Actual Temp Range | Rating | Base Multiplier | Weighted (^1.0) | Bonus (scale=50.0) |
|---------------|-------------------|--------|-----------------|-----------------|---------------------|
| ≤10°F | 50-70°F | EXCELLENT | 1.05 | 1.05 | +2.5 pts |
| 11-20°F | 40-49°F or 71-80°F | GOOD | 1.025 | 1.025 | +1.25 pts |
| 21-30°F | 30-39°F or 81-90°F | AVERAGE | 1.0 | 1.0 | 0 pts |
| 31-40°F | 20-29°F or 91-100°F | POOR | 0.975 | 0.975 | -1.25 pts |
| >40°F | <20°F or >100°F | VERY_POOR | 0.95 | 0.95 | -2.5 pts |

Note: Distance is calculated as absolute value, so both cold and hot extremes receive the same penalty.

### Example Calculation

**Game at 58°F (EXCELLENT - near ideal)**:
- Ideal temp: 60°F
- Distance: |58 - 60| = 2°F
- Rating: EXCELLENT (distance ≤ 10)
- Base Multiplier: 1.05
- Weighted Multiplier: 1.05^1.0 = 1.05
- Bonus: (50.0 × 1.05) - 50.0 = +2.5
- If previous score = 165: Final = 165 + 2.5 = 167.5

**Game at 25°F (POOR - extreme cold)**:
- Ideal temp: 60°F
- Distance: |25 - 60| = 35°F
- Rating: POOR (distance 31-40)
- Base Multiplier: 0.975
- Weighted Multiplier: 0.975^1.0 = 0.975
- Bonus: (50.0 × 0.975) - 50.0 = -1.25
- If previous score = 165: Final = 165 - 1.25 = 163.75

## Data Sources

### Game Data File

**Source**: `data/game_data.csv`

| Column | Description | Example |
|--------|-------------|---------|
| `team` | NFL team abbreviation | KC |
| `week` | NFL week number | 12 |
| `temperature` | Game temperature in Fahrenheit | 45 |
| `indoor` | Boolean flag for dome/indoor | False |

### Game Conditions Manager

**File**: `league_helper/util/GameDataManager.py`

```python
def get_game(team: str, week: int) -> Optional[GameData]:
    # Returns game data including temperature
    # Returns None if bye week or no data
```

### Indoor Game Handling

Games played in domes or retractable roof stadiums (when closed) are marked as `indoor=True`:
- Temperature scoring is **skipped** for indoor games
- No bonus or penalty applied (indoor = controlled environment)

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_temperature_scoring()` (lines 717-770)

```python
def _apply_temperature_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    # Skip if no game data manager
    if not self.game_data_manager:
        return player_score, ""

    # Get game for player's team
    game = self.game_data_manager.get_game(p.team, self.config.current_nfl_week)

    # Skip if bye week (no game)
    if not game:
        return player_score, ""

    # Skip if indoor game (no weather effects)
    if game.indoor:
        return player_score, ""

    # Skip if no temperature data
    if game.temperature is None:
        return player_score, ""

    # Calculate temperature distance from ideal
    temp_distance = self.config.get_temperature_distance(game.temperature)

    # Get multiplier (lower distance = better = higher multiplier)
    multiplier, tier = self.config.get_temperature_multiplier(temp_distance)

    # Calculate additive bonus
    impact_scale = self.config.temperature_scoring.get('IMPACT_SCALE', 50.0)
    weight = self.config.temperature_scoring.get('WEIGHT', 1.0)
    bonus = ((impact_scale * multiplier) - impact_scale) * weight

    return player_score + bonus, reason
```

### ConfigManager Methods

**File**: `league_helper/util/ConfigManager.py`

**Method**: `get_temperature_distance()` (lines 399-416)

```python
def get_temperature_distance(self, temperature: int) -> float:
    """Calculate distance from ideal temperature."""
    ideal_temp = self.temperature_scoring.get('IDEAL_TEMPERATURE', 60)
    return abs(temperature - ideal_temp)
```

**Method**: `get_temperature_multiplier()` (lines 418-431)

```python
def get_temperature_multiplier(self, temp_distance: float) -> Tuple[float, str]:
    """Get temperature multiplier based on distance from ideal."""
    return self._get_multiplier(self.temperature_scoring, temp_distance, rising_thresholds=False)
```

## Configuration

**league_config.json**:
```json
{
  "TEMPERATURE_SCORING": {
    "IDEAL_TEMPERATURE": 60,
    "IMPACT_SCALE": 50.0,
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "DECREASING",
      "STEPS": 10
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
| `IDEAL_TEMPERATURE` | 60 | Optimal temperature in Fahrenheit |
| `IMPACT_SCALE` | 50.0 | Scaling factor for bonus/penalty magnitude |
| `WEIGHT` | 0.0 (disabled) | Multiplier for final bonus (0 = disabled by default) |
| `THRESHOLDS.STEPS` | 10 | Distance threshold step size (10°F per tier) |

**Note**: Default `WEIGHT` is 0.0 (disabled) for backward compatibility. Set to 1.0 to enable temperature scoring.

## Real Player Example

**Josh Allen (QB, BUF)** - Week 12 vs Kansas City:

| Metric | Value |
|--------|-------|
| Game Location | Buffalo (outdoor) |
| Game Temperature | 32°F |
| Ideal Temperature | 60°F |
| Temperature Distance | |32 - 60| = 28°F |
| Previous Score | 170.33 |
| Rating | AVERAGE (21-30°F distance) |
| Bonus | 0 pts |
| Adjusted Score | 170.33 |

**Reason String**: `"Temp: 32°F (AVERAGE, +0.0 pts)"`

**Example with extreme cold:**

**Tua Tagovailoa (QB, MIA)** - Hypothetical game at Green Bay:

| Metric | Value |
|--------|-------|
| Game Location | Green Bay (outdoor) |
| Game Temperature | 15°F |
| Ideal Temperature | 60°F |
| Temperature Distance | |15 - 60| = 45°F |
| Previous Score | 145.0 |
| Rating | VERY_POOR (>40°F distance) |
| Bonus | -2.5 pts |
| Adjusted Score | 142.5 |

**Reason String**: `"Temp: 15°F (VERY_POOR, -2.5 pts)"`

## Edge Cases

### Indoor Games

For games in domes or with closed roofs:
- `game.indoor = True`
- Temperature scoring is **completely skipped**
- No bonus or penalty applied
- Empty reason string returned

Examples: Atlanta (Mercedes-Benz Stadium), Las Vegas (Allegiant Stadium), Detroit (Ford Field)

### Bye Weeks

Players on bye have no game:
- `game = None`
- Temperature scoring skipped
- No bonus or penalty

### Missing Temperature Data

If temperature data is unavailable:
- `game.temperature = None`
- Temperature scoring skipped
- No bonus or penalty

### International Games

Games outside USA may have different temperature patterns:
- Temperature scoring still applies if outdoor
- Indoor international games (e.g., London indoor venues) skip temperature scoring

## Position Applicability

Temperature affects **all positions**:

| Position | Impact Reasoning |
|----------|------------------|
| QB | Cold affects grip, passing accuracy, decision-making |
| RB | Cold affects ball security, footing, stamina |
| WR | Cold affects hands, catching ability, route running |
| TE | Cold affects hands, catching ability, blocking |
| K | Cold affects kicking distance, accuracy (ball flight) |
| DST | Both offense and defense affected equally (neutral) |

**Note**: Unlike wind (Step 12) which only affects passing positions, temperature affects all players equally.

## Relationship to Other Steps

- **Input**: Injury penalty-adjusted score from Step 10
- **Output**: Temperature-adjusted score
- **Next Step**: Wind bonus applied (Step 12)

Temperature is the first of three game conditions scoring steps (11-13) that adjust for weekly environmental factors.

## Strategic Insights

### When Temperature Matters Most

**High Impact Games:**
- Late season (Dec-Jan) games in cold weather cities
- Early season (Sep) games in extreme heat locations
- Playoff games in outdoor northern stadiums

**Low Impact Games:**
- Any indoor game (dome/closed roof)
- Mid-season games in moderate climates
- Games around 60°F (ideal temperature)

### Position-Specific Considerations

While all positions are affected, some research suggests:
- **QBs**: Most affected by extreme cold (ball handling, passing accuracy)
- **Kickers**: Affected by cold (ball flight, distance on long FGs)
- **WRs/TEs**: Catching difficulty in extreme cold (ball hardness)
- **RBs**: Less affected than passing game players

However, the current implementation applies temperature equally to all positions for simplicity.

## Historical Context

Temperature scoring was added in **v2.1 (2025-11-26)** as part of the game conditions scoring enhancement. It addresses the gap identified in streaming research where weather conditions significantly impact weekly player performance.

## Related Documentation

- Step 12: Wind Scoring (affects QB/WR/K only)
- Step 13: Location Scoring (home/away/international)
- `GameDataManager` implementation
- `docs/research/scoring_gap_analysis.md` - Weather metrics identified as high priority
