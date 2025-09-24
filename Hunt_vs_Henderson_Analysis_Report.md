# Kareem Hunt vs TreVeyon Henderson Fantasy Scoring Analysis

## Executive Summary

Our fantasy football scoring algorithm currently projects **Kareem Hunt** (135.54 points) higher than **TreVeyon Henderson** (121.97 points), yet Henderson has significantly higher roster rates in the fantasy community. This analysis investigates what ESPN API data could improve our scoring accuracy to better reflect market sentiment.

## Current Data Analysis

### Player Comparison - Current System
```
Kareem Hunt (KC RB):
- ID: 3059915
- Projected Points: 135.54
- Team: Kansas City Chiefs (Bye Week 10)
- Status: ACTIVE
- Age: ~29 years old (veteran)

TreVeyon Henderson (NE RB):
- ID: 4432710
- Projected Points: 121.97
- Team: New England Patriots (Bye Week 14)
- Status: ACTIVE
- Age: ~22 years old (younger player)
```

**Gap**: Hunt projected 13.57 points higher, but Henderson rostered more frequently.

## Key Factors Missing from Current Algorithm

### 1. **Player Context & Opportunity**

**Kareem Hunt (KC)**:
- **Role**: Backup/Change-of-pace behind Isiah Pacheco
- **Team Context**: High-powered KC offense, but limited touches
- **Career Stage**: Veteran player, established ceiling
- **Opportunity**: Dependent on Pacheco injury/rest

**TreVeyon Henderson (NE)**:
- **Role**: Higher potential for increased workload
- **Team Context**: NE rebuilding, more opportunity for young players
- **Career Stage**: Young player with upside potential
- **Opportunity**: More pathway to starter role

### 2. **Age & Development Curve**

- **Hunt**: 29+ years old, declining phase of career
- **Henderson**: ~22 years old, ascending phase with growth potential
- **Fantasy Impact**: Younger players often have more season-long upside

### 3. **Team Offensive Context**

**Kansas City Chiefs**:
- Elite offense BUT Hunt competes with Pacheco for touches
- Passing-heavy approach limits RB opportunities
- Hunt's role is situational/injury-dependent

**New England Patriots**:
- Developing offense with more ground-game dependency
- Less competition for backfield touches
- More opportunity for Henderson to establish himself

## ESPN API Data Points That Could Improve Scoring

### Recommended Data Integration

#### 1. **Average Draft Position (ADP)**
```python
# ESPN API Field: ownership.averageDraftPosition
def incorporate_adp_factor(base_score, adp):
    """Market wisdom adjustment"""
    if adp < 100:  # Higher draft capital
        return base_score * 1.1  # 10% boost
    elif adp > 150:  # Lower draft capital
        return base_score * 0.95  # 5% penalty
    return base_score
```

#### 2. **Player Rating & Ranking**
```python
# ESPN API Fields: playerPoolEntry.playerRating, playerPoolEntry.positionRank
def incorporate_espn_rating(base_score, player_rating, position_rank):
    """ESPN internal rating adjustment"""
    rating_multiplier = min(player_rating / 50.0, 1.2)  # Cap at 20% boost
    rank_adjustment = max(0.9, 1.0 - (position_rank / 100))
    return base_score * rating_multiplier * rank_adjustment
```

#### 3. **Ownership Trends**
```python
# ESPN API Fields: ownership.percentChange, ownership.percentOwned
def incorporate_ownership_trends(base_score, percent_change, percent_owned):
    """Rising/falling player adjustment"""
    if percent_change > 5:  # Rising ownership
        trend_boost = min(percent_change / 100, 0.15)  # Cap at 15%
        return base_score * (1 + trend_boost)
    elif percent_change < -5:  # Falling ownership
        trend_penalty = max(percent_change / 100, -0.10)  # Cap penalty at 10%
        return base_score * (1 + trend_penalty)
    return base_score
```

#### 4. **Recent Performance Momentum**
```python
# ESPN API Field: stats (recent weeks vs season average)
def incorporate_momentum(base_score, recent_avg, season_avg):
    """Hot/cold streak adjustment"""
    if recent_avg > season_avg * 1.2:  # Hot streak
        return base_score * 1.1
    elif recent_avg < season_avg * 0.8:  # Cold streak
        return base_score * 0.95
    return base_score
```

#### 5. **Age-Based Upside Factor**
```python
def incorporate_age_factor(base_score, age, position):
    """Age-based upside/downside for RBs"""
    if position == 'RB':
        if age < 25:  # Prime upside years
            return base_score * 1.05
        elif age > 28:  # Decline years
            return base_score * 0.97
    return base_score
```

#### 6. **Team Offensive Quality**
```python
# Could use team stats from ESPN API
def incorporate_team_context(base_score, team_off_rank, team_pace):
    """Team offensive environment adjustment"""
    # Better offenses = more scoring opportunities
    if team_off_rank <= 10:  # Top 10 offense
        return base_score * 1.08
    elif team_off_rank >= 25:  # Bottom 8 offense
        return base_score * 0.94
    return base_score
```

## Implementation Strategy

### Phase 1: Core Market Data
1. **ADP Integration**: Use `ownership.averageDraftPosition` as market wisdom
2. **ESPN Player Rating**: Use `playerPoolEntry.playerRating` for expert evaluation
3. **Ownership Trends**: Use `ownership.percentChange` for momentum

### Phase 2: Advanced Context
1. **Age Factor**: Calculate age from player data and apply position-specific curves
2. **Team Context**: Incorporate team offensive rankings and pace
3. **Role/Opportunity**: Use depth chart data if available

### Phase 3: Dynamic Adjustments
1. **Recent Performance**: Weight recent weeks more heavily
2. **News/Injury Impact**: Factor in recent news sentiment
3. **Matchup Context**: Consider weekly opponent strength

## Expected Impact

### For Hunt vs Henderson Case:
- **Henderson** would gain points from:
  - Better ADP (younger player premium)
  - Age upside factor (+5%)
  - Potentially higher ESPN rating
  - Positive ownership trends

- **Hunt** would lose some points from:
  - Age decline factor (-3%)
  - Lower ESPN rating for backups
  - Situational role penalty

**Projected Result**: Henderson score would increase to ~128-132 points, making the comparison much closer to market reality.

## Data Collection Requirements

### Essential ESPN API Fields:
```json
{
  "ownership": {
    "averageDraftPosition": float,
    "percentOwned": float,
    "percentChange": float,
    "percentStarted": float
  },
  "playerPoolEntry": {
    "playerRating": float,
    "positionRank": int,
    "ratingChange": float
  },
  "stats": [
    {
      "scoringPeriodId": int,
      "appliedTotal": float,
      "stats": {...}
    }
  ],
  "age": int,
  "experience": int,
  "proTeamId": int
}
```

## Conclusion

The discrepancy between Hunt's higher projection and Henderson's higher roster rate can be addressed by incorporating:

1. **Market Wisdom** (ADP, ownership trends)
2. **Player Context** (age, role, team situation)
3. **Expert Ratings** (ESPN's internal player ratings)
4. **Dynamic Factors** (momentum, news, opportunity)

These additions would make our algorithm more aligned with how fantasy managers actually evaluate players, accounting for both statistical projections AND contextual factors that drive real-world roster decisions.

## Next Steps

1. Modify ESPN API client to capture additional fields
2. Implement scoring adjustments in draft helper algorithm
3. Test with other similar player comparisons
4. Monitor correlation between adjusted scores and actual roster rates
5. Iterate based on performance data

---

*Analysis Date: September 2025*
*Data Sources: ESPN Fantasy API, Players CSV*