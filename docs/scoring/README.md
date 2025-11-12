# Fantasy Football Scoring Algorithm Documentation

## Overview

This directory contains comprehensive documentation for the 10-step scoring algorithm used in the Fantasy Football Helper application. The scoring system evaluates players through multiple metrics to produce a final composite score used for draft recommendations, roster optimization, and trade analysis.

**Implementation File**: `league_helper/util/player_scoring.py` (PlayerScoringCalculator class)

**Last Updated**: November 5, 2025 (Week 10, 2025 NFL Season)

---

## Table of Contents

- [Scoring Algorithm Flow](#scoring-algorithm-flow)
- [10-Step Process](#10-step-process)
- [Metric Categories](#metric-categories)
- [Mode Usage](#mode-usage)
- [Configuration](#configuration)
- [Recent Updates](#recent-updates)
- [Quick Reference](#quick-reference)
- [Metric Dependencies](#metric-dependencies)
- [See Also](#see-also)

---

## Scoring Algorithm Flow

```
Input: FantasyPlayer object + team_roster + mode parameters
  ↓
┌─────────────────────────────────────────────────────────────┐
│                    SCORING ALGORITHM                         │
│                                                              │
│  Step 1: Normalization                                      │
│          fantasy_points → weighted_score (0-105 scale)      │
│          Base Score: 0-105 points                           │
│  ↓                                                           │
│  Step 2: ADP Multiplier (×0.90 - ×1.10)                    │
│          Market wisdom adjustment (±9.9% with weight)       │
│  ↓                                                           │
│  Step 3: Player Rating Multiplier (×0.90 - ×1.11)          │
│          Expert consensus adjustment (±10.8% with weight)   │
│  ↓                                                           │
│  Step 4: Team Quality Multiplier (×0.98 - ×1.02)           │
│          Team strength adjustment (±1.8% with weight)       │
│  ↓                                                           │
│  Step 5: Performance Multiplier (×0.99 - ×1.01)            │
│          Actual vs projected deviation (±1.0% with weight)  │
│  ↓                                                           │
│  Step 6: Matchup Bonus/Penalty (±3.6 pts)                  │
│          Current opponent strength (additive)               │
│  ↓                                                           │
│  Step 7: Schedule Bonus/Penalty (0 pts, disabled)          │
│          Future opponents strength (weight=0)               │
│  ↓                                                           │
│  Step 8: Draft Order Bonus (+0-88 pts)                     │
│          Position-specific value by round (additive)        │
│  ↓                                                           │
│  Step 9: Bye Week Penalty (-0-50 pts)                      │
│          Roster conflict penalty (additive)                 │
│  ↓                                                           │
│  Step 10: Injury Penalty (-0-100 pts)                      │
│           Risk assessment penalty (additive)                │
│  ↓                                                           │
└─────────────────────────────────────────────────────────────┘
  ↓
Output: ScoredPlayer(player, final_score, reasons[])
```

---

## 10-Step Process

### Core Value Metrics (Steps 1-5)

Establish base player value using projections, market data, and performance:

| Step | Metric | Type | Effect | Documentation |
|------|--------|------|--------|---------------|
| 1 | **Normalization** | Multiplicative | Establishes 0-105 base score | [01_normalization.md](01_normalization.md) |
| 2 | **ADP Multiplier** | Multiplicative | ±9.9% (0.95-1.05 base, weight=1.94) | [02_adp_multiplier.md](02_adp_multiplier.md) |
| 3 | **Player Rating** | Multiplicative | ±10.8% (0.95-1.05 base, weight=2.09) | [03_player_rating_multiplier.md](03_player_rating_multiplier.md) |
| 4 | **Team Quality** | Multiplicative | ±1.8% (0.95-1.05 base, weight=0.36) | [04_team_quality_multiplier.md](04_team_quality_multiplier.md) |
| 5 | **Performance** | Multiplicative | ±1.0% (0.95-1.05 base, weight=0.20) | [05_performance_multiplier.md](05_performance_multiplier.md) |

### Environmental Metrics (Steps 6-7)

Evaluate external factors affecting player opportunity:

| Step | Metric | Type | Effect | Documentation |
|------|--------|------|--------|---------------|
| 6 | **Matchup Bonus/Penalty** | Additive | ±3.6 pts (scale=108.4, weight=0.68) | [06_matchup_multiplier.md](06_matchup_multiplier.md) |
| 7 | **Schedule Bonus/Penalty** | Additive | 0 pts (disabled, weight=0.0) | [07_schedule_multiplier.md](07_schedule_multiplier.md) |

### Strategic Adjustments (Steps 8-10)

Apply strategic considerations and risk factors:

| Step | Metric | Type | Effect | Documentation |
|------|--------|------|--------|---------------|
| 8 | **Draft Order Bonus** | Additive | +0-88 pts by position/round | [08_draft_order_bonus.md](08_draft_order_bonus.md) |
| 9 | **Bye Week Penalty** | Additive | -0-50 pts for roster conflicts | [09_bye_week_penalty.md](09_bye_week_penalty.md) |
| 10 | **Injury Penalty** | Additive | -0-100 pts for injury risk | [10_injury_penalty.md](10_injury_penalty.md) |

---

## Metric Categories

### Multiplicative vs Additive Metrics

**Multiplicative Metrics (Steps 1-5)**:
- Applied as percentage adjustments to the score
- Chain together: `score = base * mult1 * mult2 * mult3 ...`
- Base range: ×0.95 to ×1.05 (±5% before weight exponent)
- **Weight exponent applied**: `actual_multiplier = base_multiplier ^ weight`
- Actual effects vary by weight: ±1% (performance) to ±11% (player rating)
- **Purpose**: Adjust player's intrinsic value based on quality indicators

**Additive Metrics (Steps 6-10)**:
- Applied as flat point bonuses or penalties
- Added/subtracted: `score = base + bonus1 - penalty1 + bonus2 ...`
- Range varies by metric (matchup ±3.6, draft order +0-88, etc.)
- Weight exponent also applied to additive metrics before bonus calculation
- **Purpose**: Account for environmental factors and strategic considerations

**Why the distinction?**
- **Multiplicative**: Quality metrics that scale with player value (better players benefit more from good teams, ratings, etc.)
- **Additive**: Opportunity metrics that affect all players equally (favorable matchup gives same points regardless of player quality)

---

## Mode Usage

The scoring algorithm is used by three primary modes with different parameter configurations:

### Add To Roster Mode (Draft Helper)

**File**: `league_helper/add_to_roster_mode/AddToRosterModeManager.py:281-290`

**Purpose**: Evaluate available players for draft selection

**Parameters**:
```python
score_player(
    use_weekly_projection=False,  # ROS value for long-term assessment
    adp=True,                      # Market wisdom important for drafting
    player_rating=True,            # Expert consensus valuable
    team_quality=True,             # Team context matters
    performance=False,             # Disabled for draft (already in projections)
    matchup=False,                 # Current week not relevant for draft
    schedule=False,                # Disabled (future already in ROS projections)
    draft_round=current_round,     # Apply position-specific bonuses
    bye=True,                      # Enabled but ineffective (weights=0 in config)
    injury=True                    # Enabled but only HIGH risk penalized (-100 pts)
)
```

**Why these settings?**
- **ROS projections**: Draft decisions require season-long value, not single-week
- **ADP + Player Rating + Team Quality**: Market consensus and expert rankings guide decisions
- **Performance disabled**: Historical performance already incorporated into updated projections
- **Schedule disabled**: Future matchups already incorporated into ROS projections
- **Draft bonuses**: Encourages drafting right positions at right time
- **Bye/Injury enabled**: But current config makes bye ineffective (weights=0) and only HIGH-risk injuries penalized

### Starter Helper Mode (Roster Optimizer)

**File**: `league_helper/starter_helper_mode/StarterHelperModeManager.py:365-376`

**Purpose**: Optimize weekly lineup from existing roster

**Parameters**:
```python
score_player(
    use_weekly_projection=True,   # Only current week matters
    adp=False,                     # Market value irrelevant for owned players
    player_rating=False,           # Expert rankings not used for weekly lineups
    team_quality=True,             # Team offensive/defensive strength affects weekly scoring
    performance=True,              # Recent performance indicator
    matchup=True,                  # Current opponent very important
    schedule=False,                # Future games irrelevant for this week
    draft_round=-1,                # No draft bonuses (already drafted)
    bye=False,                     # Bye handled by roster constraints
    injury=False                   # Injury risk not penalized for weekly lineups
)
```

**Why these settings?**
- **Weekly projections**: Only this week's performance matters
- **Performance + Matchup + Team Quality**: Recent trends, current opponent, and team strength context
- **No ADP/Rating**: Weekly decisions focus on immediate performance, not long-term market value
- **No schedule**: Future opponents irrelevant for lineup decisions
- **No draft bonuses**: Players already owned
- **No bye/injury**: Roster constraints and availability already filter out unavailable players

### Trade Simulator Mode

**File**: `league_helper/trade_simulator_mode/TradeSimTeam.py:86-89`

**Purpose**: Evaluate roster before/after trade

**Parameters** (user team):
```python
score_player(
    use_weekly_projection=False,  # ROS value for trade evaluation
    adp=False,                     # Draft position not relevant for trades
    player_rating=True,            # Expert consensus valuable
    team_quality=True,             # Team context matters
    performance=True,              # Performance trends important
    matchup=False,                 # Current week not relevant
    schedule=True,                 # Future value important for trades
    draft_round=-1,                # No draft bonuses (already drafted)
    bye=True,                      # Post-trade roster conflicts matter
    injury=False                   # Injury risk not penalized for trades
)
```

**Note**: Opponent teams use `schedule=False, bye=False` for faster computation.

**Why these settings?**
- **ROS projections**: Trades evaluated on season-long impact
- **Player Rating + Team Quality + Performance**: Current player value indicators
- **Schedule enabled**: Future strength of schedule matters for user team
- **Bye penalties**: Ensure post-trade roster doesn't have conflicts (but weights=0)
- **No ADP**: Draft position irrelevant mid-season
- **No injury penalties**: Injury status doesn't reduce score (but affects availability)

---

## Configuration

All scoring parameters are defined in `data/league_config.json`:

### Configuration Structure

```json
{
  "config_name": "simulation/optimal_config.json",
  "description": "Optimized scoring parameters",
  "parameters": {
    "CURRENT_NFL_WEEK": 10,
    "NFL_SEASON": 2025,
    "NFL_SCORING_FORMAT": "ppr",
    "NORMALIZATION_MAX_SCALE": 105.01,

    "ADP_SCORING": {
      "THRESHOLDS": { /* parameterized */ },
      "MULTIPLIERS": {
        "VERY_POOR": 0.95,
        "POOR": 0.975,
        "GOOD": 1.025,
        "EXCELLENT": 1.05
      },
      "WEIGHT": 1.94
    },

    /* Similar structure for:
       PLAYER_RATING_SCORING
       TEAM_QUALITY_SCORING
       PERFORMANCE_SCORING
       MATCHUP_SCORING
       SCHEDULE_SCORING
    */

    "DRAFT_ORDER_BONUSES": {
      "PRIMARY": 81.64,
      "SECONDARY": 87.96
    },

    "DRAFT_ORDER": [ /* position priorities by round */ ],

    "INJURY_PENALTIES": {
      "LOW": 0,
      "MEDIUM": 0,
      "HIGH": 100
    },

    "SAME_POS_BYE_WEIGHT": 0,
    "DIFF_POS_BYE_WEIGHT": 0
  }
}
```

### Key Configuration Components

**Thresholds**: Define rating boundaries (EXCELLENT, GOOD, POOR, VERY_POOR)
- Can be explicit values or parameterized (BASE_POSITION, DIRECTION, STEPS)
- Calculated at config load time for efficiency

**Multipliers**: Define adjustment factors for each rating level
- Standard range: 0.95 to 1.05 (±5%)
- Neutral zone gets 1.0x (no adjustment)

**Weights**: Define relative importance via exponentiation
- `actual_mult = base_mult ^ weight`
- Weight > 1: Amplifies effect (e.g., 1.05² = 1.1025)
- Weight < 1: Dampens effect (e.g., 1.05^0.5 = 1.0247)
- Weight = 0: Disables metric entirely

**Impact Scales**: Define additive bonus/penalty ranges
- Used for matchup, schedule bonuses
- Formula: `bonus = (impact_scale * multiplier) - impact_scale`

---

## Recent Updates

### Player Rating Normalization System (November 5, 2025)

**Change**: Replaced tier-based player rating calculation with position-specific normalized rankings (1-100 scale)

**Implementation**:
- **ESPN Client**: Three-pass processing (preprocessing, main loop, post-processing normalization)
- **Formula**: `normalized = 1 + ((rank - max_rank) / (min_rank - max_rank)) * 99`
- **Position-specific**: Each position (QB, RB, WR, TE, K, DST) normalized independently
- **Scale**: 100 = best player at position, 1 = worst player at position

**Impact**:
- More accurate position-specific rankings
- Dynamic adjustment to actual player distribution each week
- Linear transformation preserves relative differences between players
- Weekly updates reflect current expert consensus

**Documentation**:
- [03_player_rating_multiplier.md](03_player_rating_multiplier.md) - Comprehensive system documentation
- `simulation/normalize_player_ratings.py` - Historical data normalization script

**Code Changes**:
- `player-data-fetcher/espn_client.py:1321-1757` - Three-pass normalization
- `player-data-fetcher/player_data_models.py:45` - Updated field comment
- `docs/scoring/03_player_rating_multiplier.md` - Complete documentation

---

## Quick Reference

### Metric Impact Summary

| Metric | Type | Base Range | Weight | Actual Range | Max Impact on 100pt Player |
|--------|------|------------|--------|--------------|----------------------------|
| Normalization | Multiplicative | 0-105 pts | N/A | 0-105 pts | Establishes base score |
| ADP | Multiplicative | ×0.95-1.05 | 1.94 | ×0.90-1.10 | ±10 pts |
| Player Rating | Multiplicative | ×0.95-1.05 | 2.09 | ×0.90-1.11 | ±11 pts |
| Team Quality | Multiplicative | ×0.95-1.05 | 0.36 | ×0.98-1.02 | ±2 pts |
| Performance | Multiplicative | ×0.95-1.05 | 0.20 | ×0.99-1.01 | ±1 pt |
| Matchup | Additive | ±5.4 pts | 0.68 | ±3.6 pts | ±3.6 pts (equal for all) |
| Schedule | Additive | ±4.0 pts | 0.0 | 0 pts | 0 pts (disabled) |
| Draft Order | Additive | +0-88 pts | N/A | +0-88 pts | +0-88 pts (position/round specific) |
| Bye Week | Additive | -0-50 pts | N/A | -0-50 pts | -0-50 pts (roster dependent) |
| Injury | Additive | -0-100 pts | N/A | -0-100 pts | -0-100 pts (status dependent) |

**Combined Multiplicative Effect** (Steps 2-5 with current weights):
- All EXCELLENT: 1.099 × 1.108 × 1.017 × 1.010 = ×1.252 (+25.2%)
- All GOOD: 1.049 × 1.052 × 1.009 × 1.005 = ×1.118 (+11.8%)
- All POOR: 0.952 × 0.948 × 0.991 × 0.995 = ×0.889 (-11.1%)
- All VERY_POOR: 0.904 × 0.898 × 0.982 × 0.990 = ×0.784 (-21.6%)

**Calculation**: Each base multiplier raised to its weight, then multiplied together:
- EXCELLENT: (1.05^1.94) × (1.05^2.09) × (1.05^0.36) × (1.05^0.20)
- Breakdown: ADP^weight × Rating^weight × Quality^weight × Perf^weight

### Data Sources Quick Reference

| Data Field | Source File | ESPN API Path | Update Frequency |
|------------|-------------|---------------|------------------|
| fantasy_points | players.csv | stats[*].projectedTotal | Daily |
| week_N_points | players.csv | stats[*].projectedTotal/appliedTotal | Daily |
| average_draft_position | players.csv | ownership.averageDraftPosition | Daily |
| player_rating | players.csv | rankings[N][*].averageRank | Daily |
| team_offensive_rank | teams.csv | Calculated from team stats | Weekly |
| team_defensive_rank | teams.csv | Calculated from team stats | Weekly |
| matchup_score | Calculated | Current week opponent rank | Real-time |
| bye_week | players.csv | proTeam.byeWeek | Season start |
| injury_status | players.csv | injuryStatus | Daily |

---

## Metric Dependencies

### Dependency Diagram

```
ESPN API
    ↓
player-data-fetcher/espn_client.py
    ↓
┌───────────────────────────────────────────────────┐
│           data/players.csv                        │
│  (fantasy_points, week_N_points, adp,             │
│   player_rating, bye_week, injury_status)         │
└───────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────┐
│      utils/FantasyPlayer (dataclass)              │
│  - get_rest_of_season_projection()                │
│  - get_single_weekly_projection()                 │
│  - get_risk_level()                               │
└───────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────┐
│  league_helper/util/PlayerScoringCalculator       │
│                                                   │
│  Dependencies:                                    │
│  • ConfigManager (thresholds, multipliers)        │
│  • ProjectedPointsManager (weekly projections)    │
│  • TeamDataManager (matchup scores)               │
│  • SeasonScheduleManager (future opponents)       │
└───────────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────────┐
│         Mode-Specific Scoring                     │
│  • AddToRosterModeManager (draft scoring)         │
│  • StarterHelperModeManager (lineup scoring)      │
│  • TradeSimulatorModeManager (trade scoring)      │
└───────────────────────────────────────────────────┘
```

### Inter-Metric Dependencies

**Normalization** (Step 1):
- **Depends on**: `max_projection` (calculated from all players' ROS projections)
- **Used by**: All subsequent metrics (establishes base score)

**Performance** (Step 5):
- **Depends on**: ProjectedPointsManager (historical weekly projections)
- **Depends on**: FantasyPlayer (actual weekly points: week_1_points, week_2_points, etc.)
- **Calculation**: Compare actual vs projected for past weeks

**Matchup** (Step 6):
- **Depends on**: TeamDataManager (opponent defense rank)
- **Depends on**: FantasyPlayer.team (player's team)
- **Calculation**: Opponent strength vs player's position

**Schedule** (Step 7):
- **Depends on**: SeasonScheduleManager (future opponents)
- **Depends on**: TeamDataManager (opponent defense ranks)
- **Calculation**: Average future opponent defense rank

**Bye Week** (Step 9):
- **Depends on**: team_roster (all players on team)
- **Depends on**: FantasyPlayer.bye_week (all roster players)
- **Calculation**: Count same-bye and different-position conflicts

---

## See Also

### Primary Documentation
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - Overall system architecture
- **[README.md](../../README.md)** - Project overview and usage
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines

### Implementation Files
- **`league_helper/util/player_scoring.py`** - Main scoring implementation
- **`league_helper/util/ConfigManager.py`** - Configuration management
- **`league_helper/util/ProjectedPointsManager.py`** - Weekly projection data
- **`league_helper/util/TeamDataManager.py`** - Team rankings and matchups
- **`league_helper/util/SeasonScheduleManager.py`** - Season schedule data
- **`player-data-fetcher/espn_client.py`** - ESPN API data extraction
- **`data/league_config.json`** - Scoring configuration parameters

### Testing
- **`tests/league_helper/util/test_PlayerManager.py`** - Scoring tests
- **`tests/league_helper/util/test_ConfigManager.py`** - Configuration tests
- **`tests/run_all_tests.py`** - Full test suite (1,811 tests, 100% pass rate required)

### Recent Updates
- **`RANKING_FIX_SUMMARY.md`** - Player rating fix summary
- **`updates/ranking_fix_code_changes.md`** - Player rating fix details
- **`updates/scoring_report_todo.md`** - This documentation project tracking

---

## Contributing

When modifying the scoring algorithm:

1. **Update code**: Make changes to `player_scoring.py` or related files
2. **Update tests**: Ensure 100% test pass rate (`python tests/run_all_tests.py`)
3. **Update config**: Modify `data/league_config.json` if thresholds/multipliers change
4. **Update docs**: Update relevant metric documentation in this directory
5. **Update README**: Update this file if algorithm flow or structure changes
6. **Document changes**: Create summary in `updates/` folder

---

**Last Updated**: November 5, 2025
**Documentation Version**: 1.0
**Code Version**: Week 10, 2025 NFL Season
