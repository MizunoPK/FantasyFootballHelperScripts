# Game Conditions Scoring Implementation Spec

This document specifies the implementation of new scoring parameters based on game condition data from `game_data.csv`.

## Overview

| Parameter | Type | Data Range | Applied When |
|-----------|------|------------|--------------|
| `TEMPERATURE_SCORING` | Additive Bonus/Penalty | 10°F - 103°F (2024 data) | Outdoor games |
| `WIND_SCORING` | Additive Bonus/Penalty | 3 - 41 mph (2024 data) | Outdoor games |
| `LOCATION_MODIFIERS` | Fixed Bonus/Penalty | HOME/AWAY/INTERNATIONAL | All games |

## Special Conditions

1. **Indoor games**: `TEMPERATURE_SCORING` and `WIND_SCORING` return neutral (0 pts)
2. **International games**: Only `INTERNATIONAL` modifier applies (no HOME/AWAY)
3. **Neutral site (USA)**: No location modifier applies - **Note: No neutral site games in USA in 2024 data**

---

## Bonus/Penalty Formula

Temperature and Wind use the same formula as MATCHUP_SCORING and SCHEDULE_SCORING:

```python
weighted_multiplier = base_multiplier ** WEIGHT
bonus = (IMPACT_SCALE * weighted_multiplier) - IMPACT_SCALE
adjusted_score = previous_score + bonus
```

Where:
- `base_multiplier` is 0.95 (VERY_POOR) to 1.05 (EXCELLENT) based on rating
- `WEIGHT` controls the strength of the effect
- `IMPACT_SCALE` controls the magnitude of the bonus/penalty

---

## 1. TEMPERATURE_SCORING

### Purpose
Adjust player scores based on game temperature. Extreme cold and heat historically reduce scoring.

### Configuration

```json
{
  "TEMPERATURE_SCORING": {
    "IMPACT_SCALE": 50.0,
    "IDEAL_TEMPERATURE": 60,
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

### Threshold System

**Important**: The input value is the **distance from ideal temperature (60°F)**, not the raw temperature. Direction is `DECREASING` because smaller distance = better.

Using BASE_POSITION=0, STEPS=10, DIRECTION=DECREASING:

**Calculated thresholds**: EXCELLENT=10, GOOD=20, POOR=30, VERY_POOR=40

| Temperature | Distance from 60°F | Rating | Multiplier | Bonus (scale=50) |
|-------------|-------------------|--------|------------|------------------|
| 50-70°F | ≤10 | EXCELLENT | 1.05 | +2.5 pts |
| 40-49°F or 71-80°F | >10 and ≤20 | GOOD | 1.025 | +1.25 pts |
| 31-39°F or 81-89°F | >20 and <30 | NEUTRAL | 1.0 | 0 pts |
| 21-30°F or 90-99°F | ≥30 and <40 | POOR | 0.975 | -1.25 pts |
| ≤20°F or ≥100°F | ≥40 | VERY_POOR | 0.95 | -2.5 pts |

### Implementation

```python
def get_temperature_score(self, temperature: int) -> float:
    """
    Calculate temperature score (distance from ideal temperature).

    Args:
        temperature: Game temperature in Fahrenheit

    Returns:
        Temperature distance for threshold lookup
    """
    ideal_temp = self.temperature_scoring.get('IDEAL_TEMPERATURE', 60)
    return abs(temperature - ideal_temp)
```

### Multiplier Method (ConfigManager)

```python
def get_temperature_multiplier(self, temp_distance: float) -> Tuple[float, str]:
    """
    Get temperature multiplier based on distance from ideal temperature.

    IMPORTANT: Uses rising_thresholds=False because lower distance = better.
    """
    return self._get_multiplier(self.temperature_scoring, temp_distance, rising_thresholds=False)
```

### Scoring Method

```python
def _apply_temperature_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply temperature bonus/penalty (Step 11)."""
    # Get game data from GameDataManager
    game = self.game_data_manager.get_game(p.team)

    # Skip if team is on bye or no game data
    if game is None:
        return player_score, ""

    # Skip for indoor games
    if game.indoor:
        return player_score, ""

    # Skip if no temperature data
    if game.temperature is None:
        return player_score, ""

    # Calculate distance from ideal temperature
    temp_distance = self.config.get_temperature_score(game.temperature)
    multiplier, rating = self.config.get_temperature_multiplier(temp_distance)

    impact_scale = self.config.temperature_scoring['IMPACT_SCALE']
    bonus = (impact_scale * multiplier) - impact_scale

    if rating == "NEUTRAL":
        return player_score, ""

    reason = f"Temperature: {game.temperature}°F - {rating} ({bonus:+.1f} pts)"
    return player_score + bonus, reason
```

---

## 2. WIND_SCORING

### Purpose
Adjust player scores based on wind conditions. High winds affect passing and kicking accuracy.

### Configuration

```json
{
  "WIND_SCORING": {
    "IMPACT_SCALE": 60.0,
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

### Threshold System

Using BASE_POSITION=0, STEPS=10, DIRECTION=DECREASING (lower wind = better):

**Calculated thresholds**: EXCELLENT=10, GOOD=20, POOR=30, VERY_POOR=40

| Wind Gusts | Rating | Multiplier | Bonus (scale=60) |
|------------|--------|------------|------------------|
| ≤10 mph | EXCELLENT | 1.05 | +3.0 pts |
| >10 and ≤20 mph | GOOD | 1.025 | +1.5 pts |
| >20 and <30 mph | NEUTRAL | 1.0 | 0 pts |
| ≥30 and <40 mph | POOR | 0.975 | -1.5 pts |
| ≥40 mph | VERY_POOR | 0.95 | -3.0 pts |

### Implementation

Wind scoring doesn't need a separate `get_wind_score()` method - the wind gust value is used directly for threshold lookup.

### Multiplier Method (ConfigManager)

```python
def get_wind_multiplier(self, wind_gust: float) -> Tuple[float, str]:
    """
    Get wind multiplier based on wind gust speed.

    IMPORTANT: Uses rising_thresholds=False because lower wind = better.
    """
    return self._get_multiplier(self.wind_scoring, wind_gust, rising_thresholds=False)
```

### Scoring Method

```python
def _apply_wind_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply wind bonus/penalty (Step 12)."""
    # Get game data from GameDataManager
    game = self.game_data_manager.get_game(p.team)

    # Skip if team is on bye or no game data
    if game is None:
        return player_score, ""

    # Skip for indoor games
    if game.indoor:
        return player_score, ""

    # Skip if no wind data
    if game.wind_gust is None:
        return player_score, ""

    multiplier, rating = self.config.get_wind_multiplier(game.wind_gust)

    impact_scale = self.config.wind_scoring['IMPACT_SCALE']
    bonus = (impact_scale * multiplier) - impact_scale

    if rating == "NEUTRAL":
        return player_score, ""

    reason = f"Wind: {game.wind_gust} mph - {rating} ({bonus:+.1f} pts)"
    return player_score + bonus, reason
```

---

## 3. LOCATION_MODIFIERS

### Purpose
Apply fixed point adjustments based on game location:
- **Home games**: Bonus for home field advantage (53.3% win rate, +1.87 avg point differential in 2024)
- **Away games**: Penalty for travel and hostile environment
- **International games**: Penalty for travel fatigue, timezone disruption, unfamiliar conditions

### Configuration

```json
{
  "LOCATION_MODIFIERS": {
    "HOME": 2,
    "AWAY": -2,
    "INTERNATIONAL": -5
  }
}
```

### Modifier Values

| Situation | Modifier | Effect |
|-----------|----------|--------|
| Home game (USA, non-neutral) | +2 | +2 pts bonus |
| Away game (USA, non-neutral) | -2 | -2 pts penalty |
| International game | -5 | -5 pts penalty |
| Neutral site (USA) | 0 | No modifier |

**Note**: All international games in 2024 data are neutral site. International games receive ONLY the international penalty, not home/away modifiers.

**Important**: Both teams' players receive the -5 international penalty. In a London game between JAX and NE, all JAX players AND all NE players get -5 pts.

### Implementation

```python
def get_location_modifier(self, game: UpcomingGame, team: str) -> float:
    """
    Get location modifier based on game situation.

    Args:
        game: UpcomingGame data
        team: Player's team abbreviation

    Returns:
        Point modifier (positive = bonus, negative = penalty)
    """
    # International games get international penalty only
    if game.is_international():
        return self.location_modifiers.get('INTERNATIONAL', -5)

    # Neutral site (USA) - no modifier
    if game.neutral_site:
        return 0

    # Home or away game
    if game.is_home_game(team):
        return self.location_modifiers.get('HOME', 2)
    else:
        return self.location_modifiers.get('AWAY', -2)
```

### Scoring Method

```python
def _apply_location_modifier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply location modifier (Step 13)."""
    # Get game data from GameDataManager
    game = self.game_data_manager.get_game(p.team)

    # Skip if team is on bye or no game data
    if game is None:
        return player_score, ""

    modifier = self.config.get_location_modifier(game, p.team)

    # Skip if no modifier (neutral site USA)
    if modifier == 0:
        return player_score, ""

    # Determine reason string
    if game.is_international():
        reason = f"International: {game.country} ({modifier:+.1f} pts)"
    elif modifier > 0:
        reason = f"Home Game ({modifier:+.1f} pts)"
    else:
        reason = f"Away Game ({modifier:+.1f} pts)"

    return player_score + modifier, reason
```

---

## Game Data Architecture

### Design Decision: No Player Attributes

Game condition data is **NOT** stored on `FantasyPlayer` objects. Instead:
- `GameDataManager` loads current week's game data on startup
- Scoring methods query `GameDataManager` by player's team when needed
- This keeps `FantasyPlayer` clean and avoids stale data issues

### UpcomingGame Data Class

```python
@dataclass
class UpcomingGame:
    """Game condition data for a single upcoming game."""
    home_team: str
    away_team: str
    temperature: Optional[int]      # °F, None for indoor
    wind_gust: Optional[int]        # mph, None for indoor
    indoor: bool
    neutral_site: bool
    country: str                    # "USA", "England", "Germany", "Brazil"

    def is_home_game(self, team: str) -> bool:
        """Check if the given team is the home team."""
        return team == self.home_team

    def is_international(self) -> bool:
        """Check if this is an international game."""
        return self.country != "USA"
```

### GameDataManager Class

```python
class GameDataManager:
    """
    Manages game condition data for the current NFL week.

    Loads game_data.csv and provides lookup by team name.
    Only stores games for the current week (not historical data).
    """

    def __init__(self, data_folder: Path, current_week: int):
        """
        Initialize GameDataManager for the current week.

        Args:
            data_folder: Path to data folder containing game_data.csv
            current_week: Current NFL week number (1-18)
        """
        self.current_week = current_week
        self.games_by_team: Dict[str, UpcomingGame] = {}
        self._load_current_week_games(data_folder)

    def _load_current_week_games(self, data_folder: Path) -> None:
        """Load only current week's games into team-indexed dictionary."""
        game_data_path = data_folder / "game_data.csv"

        if not game_data_path.exists():
            # No game data available - all lookups will return None
            return

        with open(game_data_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['week']) != self.current_week:
                    continue

                game = UpcomingGame(
                    home_team=row['home_team'],
                    away_team=row['away_team'],
                    temperature=int(row['temperature']) if row.get('temperature') else None,
                    wind_gust=int(float(row['gust'])) if row.get('gust') else None,
                    indoor=row.get('indoor', '').lower() == 'true',
                    neutral_site=row.get('neutral_site', '').lower() == 'true',
                    country=row.get('country', 'USA')
                )

                # Index by both teams for O(1) lookup
                self.games_by_team[game.home_team] = game
                self.games_by_team[game.away_team] = game

    def get_game(self, team: str) -> Optional[UpcomingGame]:
        """
        Get upcoming game for a team.

        Args:
            team: Team abbreviation (e.g., "BUF", "KC")

        Returns:
            UpcomingGame if team is playing this week, None if on bye
        """
        return self.games_by_team.get(team)
```

### Data File Locations
- **League Helper**: `data/game_data.csv` (current season data)
- **Simulation**: `simulation/sim_data/game_data.csv` (historical data for backtesting)

These are separate data pipelines - simulation uses its own data folder.

### Initialization

GameDataManager is initialized when LeagueHelperManager starts:

```python
# In LeagueHelperManager.__init__ or _initialize_data()
self.game_data_manager = GameDataManager(
    data_folder=self.data_folder,
    current_week=self.config.current_nfl_week
)
```

### Bye Week Handling

When `get_game(team)` returns `None`:
- Team is on bye week
- Weather scoring methods return early (no adjustment)
- Location modifier returns early (no adjustment)
- Existing bye week penalty (Step 9) still applies separately

---

## Mode Usage

| Parameter | Add To Roster | Starter Helper | Trade Simulator |
|-----------|---------------|----------------|-----------------|
| Temperature | ❌ | ✅ | ❌ |
| Wind | ❌ | ✅ | ❌ |
| Location | ❌ | ✅ | ❌ |

**Rationale**: These are all weekly game-specific conditions, so they only apply to Starter Helper mode (weekly lineup decisions).

---

## Scoring Step Order

Current steps 1-10, plus new steps 11-13:

| Step | Name | Type |
|------|------|------|
| 1 | Normalization | Transform |
| 2 | ADP Multiplier | Multiplicative |
| 3 | Player Rating | Multiplicative |
| 4 | Team Quality | Multiplicative |
| 5 | Performance | Multiplicative |
| 6 | Matchup | Additive |
| 7 | Schedule | Additive |
| 8 | Draft Order Bonus | Additive |
| 9 | Bye Week Penalty | Additive |
| 10 | Injury Penalty | Additive |
| **11** | **Temperature** | **Additive** |
| **12** | **Wind** | **Additive** |
| **13** | **Location** | **Additive** |

---

## Complete Configuration Example

**Note**: These go inside the `"parameters": {}` object in `league_config.json`.

```json
{
  "parameters": {
    "TEMPERATURE_SCORING": {
      "IMPACT_SCALE": 50.0,
      "IDEAL_TEMPERATURE": 60,
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
    },
    "WIND_SCORING": {
      "IMPACT_SCALE": 60.0,
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
    },
    "LOCATION_MODIFIERS": {
      "HOME": 2,
      "AWAY": -2,
      "INTERNATIONAL": -5
    }
  }
}
```

### Configuration Notes

1. **No MIN_WEEKS**: Unlike MATCHUP_SCORING and SCHEDULE_SCORING, weather parameters don't use MIN_WEEKS because they're game-specific (not seasonal averages).

2. **IDEAL_TEMPERATURE is a new key type**: Existing configs don't have custom keys like this. ConfigManager will need special handling.

3. **LOCATION_MODIFIERS breaks the _SCORING pattern**: This uses simple fixed values instead of THRESHOLDS/MULTIPLIERS/WEIGHT. This is intentional for simplicity.

4. **WEIGHT=1.0 are starting values**: Existing weights are optimized floats (e.g., 0.8029). These values should be tuned via simulation.

5. **IMPACT_SCALE magnitude**:
   - MATCHUP_SCORING uses ~115 (gives ±5.77 pts at extremes)
   - TEMPERATURE uses 50 (gives ±2.5 pts)
   - WIND uses 60 (gives ±3.0 pts)
   - Combined weather max: ±5.5 pts (comparable to matchup)

---

## Example Calculations

### Example 1: Cold Windy Outdoor Away Game

**Player**: Josh Allen (QB, BUF) @ NE, Week 18 (2024 data)
- Temperature: 31°F → distance from 60 = 29 → NEUTRAL
- Wind: 38 mph → POOR
- Country: USA
- Away game: Yes

| Step | Value | Rating | Adjustment |
|------|-------|--------|------------|
| Temperature | 29°F distance | NEUTRAL | 0 pts |
| Wind | 38 mph | POOR | (60 × 0.975) - 60 = -1.5 pts |
| Location | Away | - | -2 pts |
| **Total** | | | **-3.5 pts** |

### Example 2: Indoor Home Game

**Player**: CeeDee Lamb (WR, DAL) vs PHI, Week 10
- Temperature: N/A (indoor) → skipped
- Wind: N/A (indoor) → skipped
- Country: USA
- Home game: Yes

| Step | Value | Rating | Adjustment |
|------|-------|--------|------------|
| Temperature | - | - | 0 pts (indoor) |
| Wind | - | - | 0 pts (indoor) |
| Location | Home | - | +2 pts |
| **Total** | | | **+2 pts** |

### Example 3: London Game (Actual 2024 Data)

**Player**: Trevor Lawrence (QB, JAX) vs NE, Week 7 (London)
- Temperature: 63°F → distance from 60 = 3 → EXCELLENT
- Wind: 37 mph → POOR
- Country: England (International)
- Neutral Site: True

| Step | Value | Rating | Adjustment |
|------|-------|--------|------------|
| Temperature | 3°F distance | EXCELLENT | (50 × 1.05) - 50 = +2.5 pts |
| Wind | 37 mph | POOR | (60 × 0.975) - 60 = -1.5 pts |
| Location | International | - | -5 pts |
| **Total** | | | **-4.0 pts** |

*Note: London had excellent temperature but high winds on game day.*

### Example 4: Neutral Site Game (USA) - Hypothetical

**Note**: No neutral site USA games existed in 2024 regular season data. This example is hypothetical for Super Bowl or future neutral site games.

**Player**: Any player in Super Bowl or neutral site game
- Temperature: 72°F → distance from 60 = 12 → GOOD
- Wind: 8 mph → EXCELLENT
- Country: USA
- Neutral Site: True

| Step | Value | Rating | Adjustment |
|------|-------|--------|------------|
| Temperature | 12°F distance | GOOD | (50 × 1.025) - 50 = +1.25 pts |
| Wind | 8 mph | EXCELLENT | (60 × 1.05) - 60 = +3.0 pts |
| Location | Neutral | - | 0 pts |
| **Total** | | | **+4.25 pts** |

---

## Data Verification Notes

### Verified from 2024 game_data.csv:
- **Total games**: 272
- **Indoor games**: 94 (weather data is NULL)
- **Outdoor games**: 178 (all have temperature, gust, precipitation)
- **Temperature range**: 10°F - 103°F
- **Wind gust range**: 3 - 41 mph
- **International games**: 5 (all are neutral site: London x3, Munich x1, Sao Paulo x1)
- **Neutral site USA games**: 0 (all neutral sites are international)
- **Home win rate**: 53.3% (145/272)
- **Avg home point differential**: +1.87 pts

### Data Quality Notes:
- 94 games have NULL weather data (all indoor stadiums)
- 5 games have NULL state (all international)
- Precipitation data exists but only 14 games had any (max 0.27 inches)

---

## Open Questions / Future Considerations

### 1. Position-Specific Weather Effects
Research suggests weather affects positions differently:
- **Wind**: Most affects QB, WR, K; may benefit RB, DST
- **Cold**: Most affects K (kick distance), QB (ball grip)
- **Heat**: Affects all positions through fatigue

**Decision needed**: Should weather modifiers be position-specific?

### 2. Precipitation
The game_data.csv includes precipitation but only 14/272 games (5%) had any precipitation in 2024. May not be worth implementing due to rarity.

### 3. Altitude (Denver)
Denver's mile-high altitude affects kicking and player fatigue. Not currently captured in game_data.csv.

### 4. Time of Day / Night Games
Late games may have different conditions. Date/time is available in game_data.csv but not currently used.

### 5. Travel Distance
Could calculate actual travel distance from team home to game venue using coordinates.json. May provide more nuanced penalty than simple home/away.

---

## Verification Summary

This document has been verified against the actual codebase and data through multiple verification rounds.

### Round 1-2: ConfigManager Threshold Logic Verified
- DECREASING direction formula: `E=base+1s, G=base+2s, P=base+3s, VP=base+4s`
- Comparison operators: `val <= threshold` for EXCELLENT/GOOD, `val >= threshold` for POOR/VERY_POOR
- Weight exponent is applied inside `_get_multiplier()`, so returned multiplier is already weighted
- Boundary tables corrected to use precise notation (≤, >, ≥, <)

### Round 3: Example Calculations Verified Against Actual 2024 Data
- **Example 1**: Corrected from fabricated values to actual BUF @ NE Week 18 data (temp=31°F, wind=38 mph)
- **Example 2**: Verified DAL vs PHI Week 10 is indoor (correct)
- **Example 3**: Corrected from fabricated values to actual JAX vs NE London data (temp=63°F, wind=37 mph)
- **Example 4**: Marked as hypothetical since no neutral site USA games exist in 2024 data

### Round 3: Default Value Safety
- Changed `is_home_game` default from `True` to `None` to prevent silent bugs
- Updated `get_location_modifier()` to handle `None` (unknown) is_home status

### Round 4: Configuration Structure Verified Against league_config.json
- Added `"parameters": {}` wrapper to config example (actual structure)
- Documented differences from existing _SCORING pattern:
  - No MIN_WEEKS (weather is game-specific, not seasonal)
  - IDEAL_TEMPERATURE is a new custom key type
  - LOCATION_MODIFIERS uses simple values (not THRESHOLDS/MULTIPLIERS/WEIGHT)
- Noted WEIGHT=1.0 are starting values to be tuned via simulation
- Documented IMPACT_SCALE rationale (weather ±5.5 pts comparable to matchup ±5.77 pts)
- Expanded implementation checklist with all ConfigKeys and ConfigManager changes needed
- Added Game Data Loading section with:
  - GameDataManager requirements
  - Player-to-game matching logic
  - Bye week handling (weather scoring skipped, existing bye penalty still applies)
- Verified each team has exactly 1 game per week (no duplicates)
- Documented that `is_home_game` can be derived from team + game data

### Round 5: Implementation Details Verified
- **CRITICAL**: Added missing `get_temperature_multiplier()` and `get_wind_multiplier()` implementations
  - Both MUST use `rising_thresholds=False` because lower values = better
- Added `score_player()` integration pattern (boolean flags like existing steps)
- Clarified that BOTH teams get international penalty in London games
- Added CSV column mapping note (`gust` → `wind_gust` in UpcomingGame)
- Added data file location documentation (sim_data for simulation, data/ for league helper)
- Verified FantasyPlayer class has `team` attribute for game matching
- Verified FantasyPlayer is at `utils/FantasyPlayer.py` (single location)

### Architecture Revision: GameDataManager Pattern
- **NO player attributes for game data** - cleaner design, avoids stale data
- Created `UpcomingGame` dataclass to hold game condition data
- Created `GameDataManager` class:
  - Loads only current week's games (not all historical data)
  - Indexes by team for O(1) lookup
  - Returns `None` for bye weeks
- Scoring methods query `GameDataManager.get_game(player.team)` when needed
- `GameDataManager` initialized in `LeagueHelperManager` and passed to `PlayerScoring`

### Data Statistics Verified (2024 sim_data/game_data.csv)
- Total games: 272
- Indoor/Outdoor: 94 indoor (null weather), 178 outdoor (complete weather data)
- Temperature range: 10°F - 103°F (outdoor only)
- Wind gust range: 3 - 41 mph (outdoor only)
- International games: 5 (all neutral site: 3 England, 1 Germany, 1 Brazil)
- Neutral site USA: 0 games
- Home win rate: 53.3% (145/272)
- Avg home point differential: +1.87 pts
- Games with precipitation: 14 (max 0.27 inches)

### Rating Distributions (2024 outdoor games)
| Rating | Temperature | Wind |
|--------|-------------|------|
| EXCELLENT | 46.1% | 19.7% |
| GOOD | 28.1% | 51.1% |
| NEUTRAL | 18.5% | 21.9% |
| POOR | 4.5% | 6.7% |
| VERY_POOR | 2.8% | 0.6% |

*Note: 60°F ideal temperature validated - average outdoor temp is 59.3°F, median is 60°F.*

---

## Implementation Checklist

### ConfigKeys Class Updates
- [ ] Add `TEMPERATURE_SCORING = "TEMPERATURE_SCORING"` to ConfigKeys
- [ ] Add `WIND_SCORING = "WIND_SCORING"` to ConfigKeys
- [ ] Add `LOCATION_MODIFIERS = "LOCATION_MODIFIERS"` to ConfigKeys
- [ ] Add `IDEAL_TEMPERATURE = "IDEAL_TEMPERATURE"` to ConfigKeys

### ConfigManager Updates
- [ ] Add `temperature_scoring`, `wind_scoring`, `location_modifiers` attributes
- [ ] Update `_extract_parameters()` to load new keys (make optional for backwards compatibility)
- [ ] Add `get_temperature_score(temperature: int)` method (returns distance from ideal)
- [ ] Add `get_temperature_multiplier()` method (**must use `rising_thresholds=False`**)
- [ ] Add `get_wind_multiplier()` method (**must use `rising_thresholds=False`**)
- [ ] Add `get_location_modifier(game: UpcomingGame, team: str)` method

### New Classes (league_helper/util/)
- [ ] Create `UpcomingGame` dataclass with: home_team, away_team, temperature, wind_gust, indoor, neutral_site, country
- [ ] Add `is_home_game(team)` method to UpcomingGame
- [ ] Add `is_international()` method to UpcomingGame
- [ ] Create `GameDataManager` class
- [ ] Implement `__init__(data_folder, current_week)` to load current week's games
- [ ] Implement `get_game(team) -> Optional[UpcomingGame]` for O(1) lookup
- [ ] Index games by both home_team and away_team for fast lookup

### FantasyPlayer Updates
- [ ] **NO CHANGES NEEDED** - game data accessed via GameDataManager, not stored on player

### PlayerScoring Updates
- [ ] Add `game_data_manager` attribute (injected via constructor or setter)
- [ ] Add `_apply_temperature_scoring()` method (Step 11) - queries GameDataManager
- [ ] Add `_apply_wind_scoring()` method (Step 12) - queries GameDataManager
- [ ] Add `_apply_location_modifier()` method (Step 13) - queries GameDataManager
- [ ] Update `score_player()` signature to add `temperature=False`, `wind=False`, `location=False` parameters
- [ ] Call new methods when respective flags are True

### LeagueHelperManager Updates
- [ ] Initialize `GameDataManager` in `__init__` or `_initialize_data()`
- [ ] Pass `GameDataManager` to PlayerScoring
- [ ] StarterHelperModeManager should call `score_player(..., temperature=True, wind=True, location=True)`

### Configuration
- [ ] Add new keys to `league_config.json` (in parameters section)
- [ ] Ensure existing configs without new keys still work (backwards compatibility)

### Testing
- [ ] Add unit tests for `UpcomingGame` dataclass methods
- [ ] Add unit tests for `GameDataManager` (loading, lookup, bye weeks)
- [ ] Add unit tests for `get_temperature_score()`
- [ ] Add unit tests for `get_temperature_multiplier()`
- [ ] Add unit tests for `get_wind_multiplier()`
- [ ] Add unit tests for `get_location_modifier()`
- [ ] Add unit tests for `_apply_temperature_scoring()`
- [ ] Add unit tests for `_apply_wind_scoring()`
- [ ] Add unit tests for `_apply_location_modifier()`
- [ ] Add integration tests for full scoring flow with GameDataManager

### Documentation
- [ ] Add `docs/scoring/11_temperature_scoring.md`
- [ ] Add `docs/scoring/12_wind_scoring.md`
- [ ] Add `docs/scoring/13_location_modifier.md`
- [ ] Update `docs/scoring/README.md` with new steps (currently has steps 1-10)
