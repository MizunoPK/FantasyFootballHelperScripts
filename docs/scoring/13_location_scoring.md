# Step 13: Location Scoring

Location Scoring applies fixed bonus/penalty points based on game location (home, away, or international).

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 13 |
| Type | Additive Bonus/Penalty (Fixed) |
| Bonus Range | -5.0 to +2.0 points |
| Data Source | `data/game_data.csv` |

## Purpose

Game location affects player performance:
- **Home games**: Familiar environment, crowd support → Bonus points
- **Away games**: Travel fatigue, hostile crowd → Penalty points
- **International games**: Jet lag, unfamiliar environment, long travel → Larger penalty

This captures the well-documented home-field advantage and international game challenges.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ❌ | Season-long value, home/away split evenly |
| Starter Helper | ✅ | Weekly location affects game-day performance |
| Trade Simulator | ❌ | Current week location not relevant to trade value |

## Calculation

### Location Determination

```python
# Determine location type
is_home = game.is_home_game(player.team)
is_international = game.is_international()

# Priority order: International > Home > Away
if is_international:
    modifier = INTERNATIONAL  # -5.0 pts
elif is_home:
    modifier = HOME           # +2.0 pts
else:
    modifier = AWAY           # -2.0 pts
```

### Fixed Modifiers

**Unlike Steps 11-12**, location uses **fixed point values** (not multiplier-based):

| Location Type | Modifier | Description |
|---------------|----------|-------------|
| **HOME** | +2.0 pts | Playing at team's home stadium |
| **AWAY** | -2.0 pts | Playing at opponent's stadium |
| **INTERNATIONAL** | -5.0 pts | Playing outside USA (London, Germany, Mexico) |

### Priority Logic

**International takes precedence over home/away**:
- If game is international, always use INTERNATIONAL modifier (-5.0)
- Even if technically a "home" team, international travel penalty applies
- Domestic games use HOME (+2.0) or AWAY (-2.0) based on opponent

### Example Calculation

**Home Game**:
- Location: Home
- Modifier: +2.0
- If previous score = 170.5: Final = 170.5 + 2.0 = 172.5

**Away Game**:
- Location: Away
- Modifier: -2.0
- If previous score = 170.5: Final = 170.5 - 2.0 = 168.5

**International Game (London)**:
- Location: International (England)
- Modifier: -5.0
- If previous score = 170.5: Final = 170.5 - 5.0 = 165.5

## Data Sources

### Game Data File

**Source**: `data/game_data.csv`

| Column | Description | Example |
|--------|-------------|---------|
| `team` | NFL team abbreviation | KC |
| `week` | NFL week number | 12 |
| `opponent` | Opponent team abbreviation | LV |
| `home_team` | Which team is home | KC |
| `country` | Country where game is played | USA |

### Game Location Logic

**File**: `league_helper/util/GameData.py`

```python
def is_home_game(self, team: str) -> bool:
    """Check if team is playing at home."""
    return self.home_team == team

def is_international(self) -> bool:
    """Check if game is outside USA."""
    return self.country and self.country.upper() != 'USA'
```

### International Game Detection

Games are marked as international when `country != 'USA'`:
- **London games**: `country = 'England'` or `'UK'`
- **Germany games**: `country = 'Germany'`
- **Mexico games**: `country = 'Mexico'`

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_location_modifier()` (lines 827-875)

```python
def _apply_location_modifier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    # Skip if no game data manager
    if not self.game_data_manager:
        return player_score, ""

    # Get game for player's team
    game = self.game_data_manager.get_game(p.team, self.config.current_nfl_week)

    # Skip if bye week (no game)
    if not game:
        return player_score, ""

    # Determine location type
    is_home = game.is_home_game(p.team)
    is_international = game.is_international()

    # Get location modifier (priority: international > home/away)
    modifier = self.config.get_location_modifier(is_home, is_international)

    # Build reason string
    if is_international:
        location_type = f"International ({game.country})"
    elif is_home:
        location_type = "Home"
    else:
        location_type = "Away"

    return player_score + modifier, reason
```

### ConfigManager Method

**File**: `league_helper/util/ConfigManager.py`

**Method**: `get_location_modifier()` (lines 448-469)

```python
def get_location_modifier(self, is_home: bool, is_international: bool) -> float:
    """
    Get location modifier based on game location.

    Priority:
        1. International games always use INTERNATIONAL modifier (regardless of home/away)
        2. Domestic home games use HOME modifier
        3. Domestic away games use AWAY modifier
    """
    if is_international:
        return self.location_modifiers.get('INTERNATIONAL', 0.0)
    elif is_home:
        return self.location_modifiers.get('HOME', 0.0)
    else:
        return self.location_modifiers.get('AWAY', 0.0)
```

## Configuration

**league_config.json**:
```json
{
  "LOCATION_MODIFIERS": {
    "HOME": 2.0,
    "AWAY": -2.0,
    "INTERNATIONAL": -5.0
  }
}
```

### Configuration Parameters

| Parameter | Default | Typical Value | Description |
|-----------|---------|---------------|-------------|
| `HOME` | 0.0 (disabled) | 2.0 | Bonus for home games |
| `AWAY` | 0.0 (disabled) | -2.0 | Penalty for away games |
| `INTERNATIONAL` | 0.0 (disabled) | -5.0 | Penalty for international games |

**Note**: Default values are 0.0 (disabled) for backward compatibility. Set to typical values (2.0, -2.0, -5.0) to enable location scoring.

## Real Player Examples

### Example 1: Home Game

**Patrick Mahomes (QB, KC)** - Week 12 at Arrowhead:

| Metric | Value |
|--------|-------|
| Game Location | Kansas City (home) |
| Opponent | Las Vegas Raiders |
| Previous Score | 173.33 |
| Location Type | Home |
| Modifier | +2.0 pts |
| Adjusted Score | 175.33 |

**Reason String**: `"Location: Home (+2.0 pts)"`

### Example 2: Away Game

**Josh Allen (QB, BUF)** - Week 13 at San Francisco:

| Metric | Value |
|--------|-------|
| Game Location | San Francisco (away) |
| Opponent | San Francisco 49ers |
| Previous Score | 168.5 |
| Location Type | Away |
| Modifier | -2.0 pts |
| Adjusted Score | 166.5 |

**Reason String**: `"Location: Away (-2.0 pts)"`

### Example 3: International Game (London)

**Trevor Lawrence (QB, JAX)** - Hypothetical London game:

| Metric | Value |
|--------|-------|
| Game Location | London, England |
| Country | England |
| Previous Score | 155.0 |
| Location Type | International |
| Modifier | -5.0 pts |
| Adjusted Score | 150.0 |

**Reason String**: `"Location: International (England) (-5.0 pts)"`

**Note**: Even if Jacksonville is designated as "home team" for the London game, the international penalty applies.

### Example 4: International Game (Germany)

**Kansas City Chiefs** player - Germany game:

| Metric | Value |
|--------|-------|
| Game Location | Munich, Germany |
| Country | Germany |
| Previous Score | 165.0 |
| Location Type | International |
| Modifier | -5.0 pts |
| Adjusted Score | 160.0 |

**Reason String**: `"Location: International (Germany) (-5.0 pts)"`

## Edge Cases

### Bye Weeks

Players on bye have no game:
- `game = None`
- Location scoring skipped
- No bonus or penalty

### Neutral Site Domestic Games

Some games are played at neutral sites within USA (e.g., Super Bowl):
- Currently treated as home/away based on official designation
- Not marked as international (country = 'USA')

### International "Home" Team

For international games:
- One team is designated as "home" for scheduling purposes
- **Location scoring ignores home/away for international games**
- Both teams receive INTERNATIONAL penalty (-5.0)
- This reflects equal travel burden for both teams

### Missing Country Data

If country data is missing:
- Defaults to assuming USA (not international)
- Falls back to home/away logic

## Position Applicability

Location affects **all positions** equally:

| Position | Impact Reasoning |
|----------|------------------|
| QB | Home crowd familiarity, signal calling ease |
| RB | Home field surface knowledge, crowd energy |
| WR | Route timing, communication with QB |
| TE | Blocking assignments, crowd noise |
| K | Familiarity with kicking surface, wind patterns |
| DST | Crowd noise disrupts opponent offense, home momentum |

**Note**: Unlike wind (Step 12) which is position-selective, location affects all players uniformly.

## Relationship to Other Steps

- **Input**: Wind-adjusted score from Step 12
- **Output**: Final player score (this is the last step)
- **Next Step**: None - this is Step 13 (final scoring step)

Location is the third and final game conditions scoring step (11-13).

## Strategic Insights

### Home/Away Advantage

**Research-backed home field advantage:**
- NFL home teams win ~57% of games historically
- Home teams score ~2-3 more points per game on average
- Crowd noise, familiarity, no travel fatigue contribute

**Modifier calibration:**
- Home: +2.0 pts reflects ~1-2% score boost
- Away: -2.0 pts reflects ~1-2% score reduction
- Net difference: 4 points between home and away

### International Game Penalty

**Why -5.0 pts for international games?**

1. **Extreme travel**: 5,000+ miles for most teams
2. **Jet lag**: 5-8 hour time zone differences (London)
3. **Unfamiliar environment**: Different field, stadium, routine
4. **Shortened week**: Teams often travel Thursday/Friday
5. **Both teams affected**: Neither team has "true" home advantage

**Historical data supports penalty:**
- International games often lower-scoring
- Player performance more variable
- Both teams underperform typical averages

### Position-Specific Considerations

While location modifier is uniform, strategic impact varies:

**High Impact Positions:**
- **QBs**: Communication, crowd noise during away games
- **Kickers**: Field familiarity, wind pattern knowledge
- **DST**: Crowd noise helps defense at home

**Lower Impact Positions:**
- **RBs**: Less affected by crowd noise
- **TEs**: Moderate impact

However, the current implementation applies location equally for simplicity.

## When Location Matters Most

**High Impact Games:**
- Playoff games (home field advantage critical)
- Division rivalry games (intense home crowd)
- International games (major travel disruption)
- Primetime home games (crowd energy peaks)

**Low Impact Games:**
- Neutral matchups
- Short travel distances (division games)
- Preseason/week 1 (less crowd energy)

## Historical Context

Location scoring was added in **v2.1 (2025-11-26)** as part of the game conditions scoring enhancement. It addresses the well-documented home field advantage and the unique challenges of international games.

## Comparison to Other Game Conditions

| Factor | Temperature (11) | Wind (12) | Location (13) |
|--------|-----------------|-----------|---------------|
| **Type** | Additive (multiplier-based) | Additive (multiplier-based) | Additive (fixed) |
| **Positions** | All | QB, WR, K only | All |
| **Range** | ±2.5 pts | ±3.0 pts | -5.0 to +2.0 pts |
| **Measurement** | Distance from 60°F | Wind gust mph | Home/Away/International |
| **Calculation** | Dynamic (weather) | Dynamic (weather) | Static (location) |
| **Variability** | High (0-100°F range) | High (0-40+ mph) | Low (3 fixed values) |

**Key Differences:**
- **Location is the only fixed modifier** (no multiplier calculation)
- **Location has asymmetric range** (-5.0 to +2.0, not ±X)
- **Location is most predictable** (known days in advance)

## Related Documentation

- Step 11: Temperature Scoring (dynamic weather)
- Step 12: Wind Scoring (dynamic weather, position-selective)
- `GameDataManager` implementation
- `GameData.is_home_game()` and `GameData.is_international()` methods
- `docs/research/scoring_gap_analysis.md` - Location identified as medium priority

## Future Enhancements

Potential refinements identified in gap analysis:

1. **Primetime game adjustment** (MNF/SNF/TNF)
   - Some players perform differently in primetime
   - Would require player-specific historical analysis
   - Currently not implemented

2. **Travel distance** consideration
   - East coast to west coast = 3 hour time zone shift
   - Could adjust AWAY penalty based on distance
   - Currently all away games treated equally

3. **Division game adjustment**
   - More familiarity reduces home/away gap
   - Could reduce modifiers for division matchups
   - Currently not implemented

4. **Retractable roof games**
   - Some stadiums have roofs that open/close
   - Currently treated as indoor (no temp/wind) when closed
   - Could distinguish from true domes

## Final Score Summary

After Step 13 (location), the **final player score** reflects:

**Pre-Game Conditions (Steps 1-10):**
1. Projection normalization
2. Market consensus (ADP)
3. Expert consensus (rating)
4. Team quality
5. Performance trends
6. Matchup strength
7. Schedule strength
8. Draft strategy fit
9. Roster bye conflicts
10. Injury risk

**Game Conditions (Steps 11-13):**
11. Temperature impact (all positions)
12. Wind impact (QB/WR/K only)
13. Location advantage (all positions)

This comprehensive 13-step scoring system enables informed weekly lineup decisions in Starter Helper mode.
