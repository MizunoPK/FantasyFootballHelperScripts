# League Configuration File Documentation

## Overview

The `league_config.json` file is the central configuration for the Fantasy Football Helper application. It contains all parameters that control the 10-step scoring algorithm, including normalization scales, multipliers, thresholds, bonuses, and penalties.

**Location**: `data/league_config.json`
**Managed By**: `league_helper/util/ConfigManager.py`
**Validated At**: Application startup and configuration loading

**Last Updated**: November 17, 2025 (Week 11, 2025 NFL Season)

---

## Table of Contents

- [File Structure](#file-structure)
- [Top-Level Fields](#top-level-fields)
- [Basic Parameters](#basic-parameters)
- [Scoring Section Structure](#scoring-section-structure)
- [Threshold System](#threshold-system)
- [Multiplier System](#multiplier-system)
- [Weight System](#weight-system)
- [Scoring Sections](#scoring-sections)
  - [ADP Scoring](#adp-scoring)
  - [Player Rating Scoring](#player-rating-scoring)
  - [Team Quality Scoring](#team-quality-scoring)
  - [Performance Scoring](#performance-scoring)
  - [Matchup Scoring](#matchup-scoring)
  - [Schedule Scoring](#schedule-scoring)
- [Draft Configuration](#draft-configuration)
- [Roster Configuration](#roster-configuration)
- [Penalty Configuration](#penalty-configuration)
- [Parameter Optimization](#parameter-optimization)
- [Interpreting Parameter Values](#interpreting-parameter-values)
- [Configuration Validation](#configuration-validation)

---

## File Structure

```json
{
  "config_name": "simulation/simulation_configs/optimal_iterative_20251107_194637.json",
  "description": "Win Rate: 0.74",
  "parameters": {
    // All configuration parameters
  }
}
```

### Top-Level Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `config_name` | string | Identifier for this configuration (often points to source simulation config) | Yes |
| `description` | string | Human-readable description (often includes win rate from simulation) | Yes |
| `parameters` | object | All configuration parameters (see below) | Yes |

---

## Basic Parameters

These parameters control fundamental aspects of the league and scoring system:

```json
"parameters": {
  "CURRENT_NFL_WEEK": 11,
  "NFL_SEASON": 2025,
  "NFL_SCORING_FORMAT": "ppr",
  "NORMALIZATION_MAX_SCALE": 129.3980536042144,
  "SAME_POS_BYE_WEIGHT": 0.4224105904019155,
  "DIFF_POS_BYE_WEIGHT": 0.16312046041817152
}
```

### Parameter Details

| Parameter | Type | Description | Range | Interpretation |
|-----------|------|-------------|-------|----------------|
| `CURRENT_NFL_WEEK` | int | Current NFL week number | 1-18 | Used to filter historical data, determine ROS projections |
| `NFL_SEASON` | int | Current NFL season year | 2000+ | Season identifier for data files |
| `NFL_SCORING_FORMAT` | string | League scoring format | "ppr", "std", "half" | Determines how player projections are calculated |
| `NORMALIZATION_MAX_SCALE` | float | Maximum normalized score scale | 100-150 | **Higher = larger point differences between players** |
| `SAME_POS_BYE_WEIGHT` | float | Weight for same-position bye week conflicts | 0.0-0.6 | **Higher = stronger penalty for bye conflicts at same position** |
| `DIFF_POS_BYE_WEIGHT` | float | Weight for different-position bye week conflicts | 0.0-0.3 | **Higher = stronger penalty for bye conflicts at different positions** |

**Good vs Bad Values**:
- **NORMALIZATION_MAX_SCALE**:
  - **Good**: 120-140 (creates meaningful score differences)
  - **Bad**: <100 (compresses scores too much), >150 (exaggerates differences)
- **SAME_POS_BYE_WEIGHT**:
  - **Good**: 0.3-0.5 (penalizes same-position conflicts appropriately)
  - **Bad**: 0.0 (ignores bye weeks), >0.6 (over-penalizes)
- **DIFF_POS_BYE_WEIGHT**:
  - **Good**: 0.1-0.2 (small penalty for cross-position conflicts)
  - **Bad**: 0.0 (ignores cross-position conflicts), >0.3 (too harsh)

---

## Scoring Section Structure

All scoring metrics (ADP, Player Rating, Team Quality, Performance, Matchup, Schedule) follow this structure:

```json
"ADP_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "DECREASING",
    "STEPS": 32.268618801448
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 2.808290873461697
}
```

Optional fields (only for additive metrics like Matchup/Schedule):
```json
"MATCHUP_SCORING": {
  "IMPACT_SCALE": 185.1525173185212,  // Additive bonus scale
  // ... THRESHOLDS, MULTIPLIERS, WEIGHT
}
```

Optional fields (only for Performance):
```json
"PERFORMANCE_SCORING": {
  "MIN_WEEKS": 3,  // Minimum weeks of data required
  // ... THRESHOLDS, MULTIPLIERS, WEIGHT
}
```

---

## Threshold System

Thresholds define when a player's metric value transitions from one rating tier to another (VERY_POOR → POOR → NEUTRAL → GOOD → EXCELLENT).

### Parameterized Threshold Format

Modern configs use a **parameterized system** that calculates thresholds from three values:

```json
"THRESHOLDS": {
  "BASE_POSITION": 0,
  "DIRECTION": "INCREASING",
  "STEPS": 20
}
```

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `BASE_POSITION` | float | Starting point for threshold calculation | Typically 0 or 0.0 |
| `DIRECTION` | string | How thresholds are arranged | "INCREASING", "DECREASING", "BI_EXCELLENT_HI", "BI_EXCELLENT_LOW" |
| `STEPS` | float | Spacing between threshold levels | Must be positive, non-zero |

### Direction Types

#### 1. INCREASING (Higher is Better)

Used for metrics where **higher values = better performance** (e.g., player rating, matchup rank).

**Formula**:
- VERY_POOR = BASE + (1 × STEPS)
- POOR = BASE + (2 × STEPS)
- GOOD = BASE + (3 × STEPS)
- EXCELLENT = BASE + (4 × STEPS)

**Example** (Player Rating: BASE=0, STEPS=20):
```
VERY_POOR = 0 + 20 = 20
POOR = 0 + 40 = 40
GOOD = 0 + 60 = 60
EXCELLENT = 0 + 80 = 80
```

**Interpretation**:
- Rating ≥ 80: EXCELLENT multiplier (×1.05)
- Rating ≥ 60: GOOD multiplier (×1.025)
- 40 < Rating < 60: NEUTRAL (×1.0)
- Rating ≤ 40: POOR multiplier (×0.975)
- Rating ≤ 20: VERY_POOR multiplier (×0.95)

#### 2. DECREASING (Lower is Better)

Used for metrics where **lower values = better performance** (e.g., ADP rank, team offensive rank).

**Formula**:
- EXCELLENT = BASE + (1 × STEPS)
- GOOD = BASE + (2 × STEPS)
- POOR = BASE + (3 × STEPS)
- VERY_POOR = BASE + (4 × STEPS)

**Example** (ADP: BASE=0, STEPS=32.27):
```
EXCELLENT = 0 + 32.27 = 32.27
GOOD = 0 + 64.54 = 64.54
POOR = 0 + 96.81 = 96.81
VERY_POOR = 0 + 129.08 = 129.08
```

**Interpretation**:
- ADP ≤ 32: EXCELLENT multiplier (×1.05) - Top 3 rounds
- ADP ≤ 65: GOOD multiplier (×1.025) - Rounds 4-5
- 65 < ADP < 97: NEUTRAL (×1.0) - Rounds 6-8
- ADP ≥ 97: POOR multiplier (×0.975) - Rounds 9-10
- ADP ≥ 129: VERY_POOR multiplier (×0.95) - Rounds 11+

#### 3. BI_EXCELLENT_HI (Bidirectional, Positive is Excellent)

Used for metrics where **deviation from zero matters**, and **positive deviation = excellent** (e.g., performance: outperforming projections).

**Formula**:
- VERY_POOR = BASE - (2 × STEPS)
- POOR = BASE - (1 × STEPS)
- GOOD = BASE + (1 × STEPS)
- EXCELLENT = BASE + (2 × STEPS)

**Example** (Performance: BASE=0.0, STEPS=0.31):
```
VERY_POOR = 0.0 - 0.62 = -0.62 (underperforming by 62%)
POOR = 0.0 - 0.31 = -0.31 (underperforming by 31%)
GOOD = 0.0 + 0.31 = +0.31 (overperforming by 31%)
EXCELLENT = 0.0 + 0.62 = +0.62 (overperforming by 62%)
```

**Interpretation**:
- Deviation ≥ +0.62: EXCELLENT (×1.05) - Significantly outperforming
- Deviation ≥ +0.31: GOOD (×1.025) - Moderately outperforming
- -0.31 < Deviation < +0.31: NEUTRAL (×1.0) - Performing as expected
- Deviation ≤ -0.31: POOR (×0.975) - Moderately underperforming
- Deviation ≤ -0.62: VERY_POOR (×0.95) - Significantly underperforming

#### 4. BI_EXCELLENT_LOW (Bidirectional, Negative is Excellent)

Used for metrics where **negative deviation = excellent** (rare, reserved for future metrics).

**Formula**:
- EXCELLENT = BASE - (2 × STEPS)
- GOOD = BASE - (1 × STEPS)
- POOR = BASE + (1 × STEPS)
- VERY_POOR = BASE + (2 × STEPS)

**Currently Unused** in production configs.

---

## Multiplier System

Multipliers adjust a player's score based on their threshold tier. All metrics use the same base multiplier structure:

```json
"MULTIPLIERS": {
  "VERY_POOR": 0.95,
  "POOR": 0.975,
  "GOOD": 1.025,
  "EXCELLENT": 1.05
}
```

### Base Multiplier Ranges

| Tier | Multiplier | Effect | Meaning |
|------|------------|--------|---------|
| EXCELLENT | 1.05 | +5% | Exceptional quality/opportunity |
| GOOD | 1.025 | +2.5% | Above average quality/opportunity |
| NEUTRAL | 1.0 | 0% | Average quality/opportunity (implicit tier) |
| POOR | 0.975 | -2.5% | Below average quality/opportunity |
| VERY_POOR | 0.95 | -5% | Very poor quality/opportunity |

**Note**: These are **base multipliers** before weight is applied. The actual effect is `base_multiplier ^ WEIGHT`.

### Neutral Tier (Implicit)

The **NEUTRAL** tier (×1.0) is **not explicitly defined** in the config but exists as the default when a value falls between POOR and GOOD thresholds. This represents average performance with no adjustment.

---

## Weight System

The `WEIGHT` parameter controls **how strongly a metric influences the final score** by applying an exponent to the base multiplier:

```
actual_multiplier = base_multiplier ^ WEIGHT
```

### Weight Effects

| Weight Range | Effect | Interpretation |
|--------------|--------|----------------|
| 0.0 | No effect | Multiplier becomes 1.0 (disabled metric) |
| 0.1 - 0.5 | Minimal | Dampens the multiplier effect (e.g., 1.05^0.2 = 1.0098 → ~1% effect) |
| 0.5 - 1.5 | Moderate | Moderate multiplier effect (e.g., 1.05^1.0 = 1.05 → 5% effect) |
| 1.5 - 3.0 | Strong | Amplifies the multiplier effect (e.g., 1.05^2.0 = 1.1025 → 10.25% effect) |
| 3.0+ | Very Strong | Heavily amplifies effect (e.g., 1.05^3.0 = 1.1576 → 15.76% effect) |

### Example Calculations

**ADP Multiplier** (BASE=1.05, WEIGHT=2.81):
```
EXCELLENT: 1.05 ^ 2.81 = 1.1485 → +14.85% boost
GOOD:      1.025 ^ 2.81 = 1.0724 → +7.24% boost
NEUTRAL:   1.0 ^ 2.81 = 1.0000 → 0% change
POOR:      0.975 ^ 2.81 = 0.9305 → -6.95% penalty
VERY_POOR: 0.95 ^ 2.81 = 0.8676 → -13.24% penalty
```

**Performance Multiplier** (BASE=1.05, WEIGHT=0.58):
```
EXCELLENT: 1.05 ^ 0.58 = 1.0284 → +2.84% boost
GOOD:      1.025 ^ 0.58 = 1.0143 → +1.43% boost
NEUTRAL:   1.0 ^ 0.58 = 1.0000 → 0% change
POOR:      0.975 ^ 0.58 = 0.9857 → -1.43% penalty
VERY_POOR: 0.95 ^ 0.58 = 0.9719 → -2.81% penalty
```

### Good vs Bad Weight Values

**By Metric Category**:

| Metric | Good Range | Bad Range | Rationale |
|--------|------------|-----------|-----------|
| **ADP** | 2.0 - 3.0 | <1.0, >5.0 | High weight emphasizes market consensus |
| **Player Rating** | 0.5 - 1.5 | <0.3, >2.0 | Moderate weight for expert rankings |
| **Team Quality** | 0.5 - 1.0 | <0.3, >1.5 | Team context matters but isn't dominant |
| **Performance** | 0.5 - 1.0 | <0.3, >2.0 | Recent trends inform but don't override |
| **Matchup** | 0.5 - 1.0 | <0.3, >1.5 | Weekly opponent affects but isn't decisive |

**General Guidelines**:
- **Weight=0.0**: Disables the metric entirely
- **Weight < 0.5**: Too weak, metric barely affects final score
- **Weight > 3.0**: Too strong, metric dominates final score
- **Optimal**: Balance weights so no single metric overwhelms others

---

## Scoring Sections

### ADP Scoring

**Purpose**: Adjusts score based on Average Draft Position (market consensus).

**Type**: Multiplicative (affects percentage of score)

**Direction**: DECREASING (lower ADP = earlier draft pick = better player)

```json
"ADP_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "DECREASING",
    "STEPS": 32.268618801448
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 2.808290873461697
}
```

**Current Effect**: ±14% (1.05^2.81 = 1.1485, 0.95^2.81 = 0.8676)

**How It Works**:
1. Player's ADP is compared to thresholds
2. Lower ADP (earlier pick) gets higher multiplier
3. Weight amplifies the effect (2.81 is high → strong influence)

**Interpreting Values**:
- **STEPS** (32.27):
  - **Good**: 30-40 (groups draft rounds logically)
  - **Bad**: <20 (too granular), >50 (too coarse)
- **WEIGHT** (2.81):
  - **Good**: 2.0-3.0 (market wisdom is important)
  - **Bad**: <1.5 (ignores market), >4.0 (over-relies on ADP)

**Example** (STEPS=32.27):
- ADP 15 (Round 2): EXCELLENT (×1.1485) → +14.85% boost
- ADP 50 (Round 5): GOOD (×1.0724) → +7.24% boost
- ADP 80 (Round 7): NEUTRAL (×1.0000) → No change
- ADP 110 (Round 9): POOR (×0.9305) → -6.95% penalty

---

### Player Rating Scoring

**Purpose**: Adjusts score based on expert consensus rankings.

**Type**: Multiplicative

**Direction**: INCREASING (higher rating = better player)

```json
"PLAYER_RATING_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 20
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 0.7931596191637781
}
```

**Current Effect**: ±4% (1.05^0.79 = 1.0394, 0.95^0.79 = 0.9611)

**How It Works**:
1. Player's rating (0-100 scale) is compared to thresholds
2. Higher rating gets higher multiplier
3. Weight moderates the effect (0.79 is moderate)

**Interpreting Values**:
- **STEPS** (20):
  - **Good**: 15-25 (creates 4-5 rating tiers across 0-100 scale)
  - **Bad**: <10 (too many tiers), >30 (too few tiers)
- **WEIGHT** (0.79):
  - **Good**: 0.5-1.5 (expert rankings matter but aren't dominant)
  - **Bad**: <0.3 (ignores experts), >2.0 (over-relies on rankings)

**Example** (STEPS=20):
- Rating 85: EXCELLENT (×1.0394) → +3.94% boost
- Rating 65: GOOD (×1.0195) → +1.95% boost
- Rating 50: NEUTRAL (×1.0000) → No change
- Rating 35: POOR (×0.9806) → -1.94% penalty

---

### Team Quality Scoring

**Purpose**: Adjusts score based on player's team offensive/defensive rank.

**Type**: Multiplicative

**Direction**: DECREASING (lower rank = better team = rank 1 is best)

```json
"TEAM_QUALITY_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "DECREASING",
    "STEPS": 6
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 0.7863701095223943
}
```

**Current Effect**: ±4% (1.05^0.79 = 1.0393, 0.95^0.79 = 0.9611)

**How It Works**:
1. Team's offensive rank (1-32) is compared to thresholds
2. Better (lower) rank gets higher multiplier
3. For DST position, defensive rank is used instead

**Interpreting Values**:
- **STEPS** (6):
  - **Good**: 5-8 (groups teams into 4-5 tiers)
  - **Bad**: <4 (too granular for 32 teams), >10 (too coarse)
- **WEIGHT** (0.79):
  - **Good**: 0.5-1.0 (team matters but player talent matters more)
  - **Bad**: <0.3 (ignores team context), >1.5 (team overrides player)

**Example** (STEPS=6):
- Team Rank 5 (Top Offense): EXCELLENT (×1.0393) → +3.93% boost
- Team Rank 12 (Good Offense): GOOD (×1.0195) → +1.95% boost
- Team Rank 18 (Average): NEUTRAL (×1.0000) → No change
- Team Rank 26 (Weak Offense): POOR (×0.9806) → -1.94% penalty

---

### Performance Scoring

**Purpose**: Adjusts score based on actual vs projected point deviation.

**Type**: Multiplicative

**Direction**: BI_EXCELLENT_HI (positive deviation = outperforming = excellent)

**Special Field**: `MIN_WEEKS` (minimum weeks of data required for calculation)

```json
"PERFORMANCE_SCORING": {
  "MIN_WEEKS": 3,
  "THRESHOLDS": {
    "BASE_POSITION": 0.0,
    "DIRECTION": "BI_EXCELLENT_HI",
    "STEPS": 0.3112580181091078
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 0.5770528501106625
}
```

**Current Effect**: ±3% (1.05^0.58 = 1.0284, 0.95^0.58 = 0.9719)

**How It Works**:
1. For each past week, calculate: (actual_points - projected_points) / projected_points
2. Average all weekly deviations to get overall deviation
3. Requires MIN_WEEKS (3) weeks of data; otherwise returns None
4. Deviation compared to BI_EXCELLENT_HI thresholds
5. Positive deviation (outperforming) gets higher multiplier

**Interpreting Values**:
- **MIN_WEEKS** (3):
  - **Good**: 3-5 (enough data without being too restrictive)
  - **Bad**: <2 (insufficient data), >6 (too restrictive, excludes many players)
- **STEPS** (0.31):
  - **Good**: 0.15-0.35 (captures meaningful over/underperformance)
  - **Bad**: <0.10 (too sensitive), >0.50 (not sensitive enough)
- **WEIGHT** (0.58):
  - **Good**: 0.5-1.0 (trends matter but projections already capture much)
  - **Bad**: <0.3 (ignores recent trends), >1.5 (overweights volatility)

**Example** (STEPS=0.31):
- Deviation +0.70 (+70%): EXCELLENT (×1.0284) → +2.84% boost (consistently outperforming)
- Deviation +0.40 (+40%): GOOD (×1.0142) → +1.42% boost (moderately outperforming)
- Deviation 0.00 (0%): NEUTRAL (×1.0000) → No change (performing as expected)
- Deviation -0.40 (-40%): POOR (×0.9858) → -1.42% penalty (moderately underperforming)
- Deviation -0.70 (-70%): VERY_POOR (×0.9719) → -2.81% penalty (significantly underperforming)

**Note**: DST position players are skipped (insufficient historical projection data).

---

### Matchup Scoring

**Purpose**: Adds bonus/penalty based on current week's opponent defensive strength.

**Type**: Additive (adds/subtracts flat points)

**Direction**: INCREASING (higher rank = weaker defense = easier matchup = more points)

**Special Field**: `IMPACT_SCALE` (scaling factor for additive bonus calculation)

```json
"MATCHUP_SCORING": {
  "IMPACT_SCALE": 185.1525173185212,
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 6
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 0.5147172590226383
}
```

**Current Effect**: ±4.6 pts (see formula below)

**How It Works**:
1. Get opponent's defense rank vs player's position (1-32)
2. Higher rank = weaker defense = better matchup
3. Compare rank to INCREASING thresholds
4. Calculate additive bonus: `bonus = (IMPACT_SCALE × weighted_multiplier) - IMPACT_SCALE`
5. Add bonus to score (not multiply)

**Additive Bonus Formula**:
```
weighted_multiplier = base_multiplier ^ WEIGHT
bonus = (IMPACT_SCALE × weighted_multiplier) - IMPACT_SCALE
```

**Example** (IMPACT_SCALE=185.15, WEIGHT=0.51):
- **EXCELLENT** (defense rank ≥ 24):
  - weighted_mult = 1.05^0.51 = 1.0252
  - bonus = (185.15 × 1.0252) - 185.15 = +4.67 pts
- **GOOD** (defense rank ≥ 18):
  - weighted_mult = 1.025^0.51 = 1.0126
  - bonus = (185.15 × 1.0126) - 185.15 = +2.33 pts
- **NEUTRAL** (12 < defense rank < 18):
  - bonus = 0.0 pts
- **POOR** (defense rank ≤ 12):
  - weighted_mult = 0.975^0.51 = 0.9874
  - bonus = (185.15 × 0.9874) - 185.15 = -2.33 pts
- **VERY_POOR** (defense rank ≤ 6):
  - weighted_mult = 0.95^0.51 = 0.9749
  - bonus = (185.15 × 0.9749) - 185.15 = -4.65 pts

**Interpreting Values**:
- **IMPACT_SCALE** (185.15):
  - **Good**: 150-200 (meaningful but not overwhelming bonuses)
  - **Bad**: <100 (too small, matchup doesn't matter), >300 (too large, dominates score)
- **STEPS** (6):
  - **Good**: 5-8 (divides 32 defenses into 4-5 tiers)
  - **Bad**: <4 (too granular), >10 (too coarse)
- **WEIGHT** (0.51):
  - **Good**: 0.5-1.0 (matchup matters for weekly decisions)
  - **Bad**: <0.3 (ignores matchup), >1.5 (over-emphasizes single week)

---

### Schedule Scoring

**Purpose**: Adds bonus/penalty based on average future opponent defensive strength.

**Type**: Additive (adds/subtracts flat points)

**Direction**: BI_EXCELLENT_HI (deviation from league average = rank 16)

**Special Field**: `IMPACT_SCALE` (scaling factor for additive bonus calculation)

```json
"SCHEDULE_SCORING": {
  "IMPACT_SCALE": 185.1525173185212,
  "THRESHOLDS": {
    "BASE_POSITION": 16,
    "DIRECTION": "BI_EXCELLENT_HI",
    "STEPS": 2.5
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,
    "POOR": 0.975,
    "GOOD": 1.025,
    "EXCELLENT": 1.05
  },
  "WEIGHT": 0.5147172590226383
}
```

**Current Effect**: ±4.6 pts (same as Matchup)

**How It Works**:
1. Get all future opponents from current week to end of season
2. Calculate average defense rank vs player's position (1-32)
3. Compare average to BASE_POSITION (16 = league average)
4. Deviation from 16 determines rating:
   - **Positive deviation** (avg rank > 16): Easier schedule (facing worse defenses)
   - **Negative deviation** (avg rank < 16): Harder schedule (facing better defenses)
5. Apply additive bonus formula: `bonus = (IMPACT_SCALE × weighted_multiplier) - IMPACT_SCALE`

**Threshold Calculation** (BASE=16, STEPS=2.5, DIRECTION=BI_EXCELLENT_HI):
```
EXCELLENT = 16 + (2 × 2.5) = 21.0   (facing bad defenses, ranks 21-32)
GOOD      = 16 + (1 × 2.5) = 18.5   (facing below-avg defenses, ranks 19-20)
NEUTRAL   = 13.5 to 18.5            (average schedule)
POOR      = 16 - (1 × 2.5) = 13.5   (facing above-avg defenses, ranks 12-13)
VERY_POOR = 16 - (2 × 2.5) = 11.0   (facing elite defenses, ranks 1-11)
```

**Example** (IMPACT_SCALE=185.15, WEIGHT=0.51):
- **Avg rank 24** (easier schedule):
  - EXCELLENT tier
  - weighted_mult = 1.05^0.51 = 1.0252
  - bonus = (185.15 × 1.0252) - 185.15 = **+4.67 pts**
- **Avg rank 19** (slightly easier):
  - GOOD tier
  - weighted_mult = 1.025^0.51 = 1.0126
  - bonus = (185.15 × 1.0126) - 185.15 = **+2.33 pts**
- **Avg rank 16** (league average):
  - NEUTRAL tier
  - bonus = **0.0 pts**
- **Avg rank 12** (slightly harder):
  - POOR tier
  - weighted_mult = 0.975^0.51 = 0.9874
  - bonus = (185.15 × 0.9874) - 185.15 = **-2.33 pts**
- **Avg rank 8** (elite defenses):
  - VERY_POOR tier
  - weighted_mult = 0.95^0.51 = 0.9749
  - bonus = (185.15 × 0.9749) - 185.15 = **-4.65 pts**

**Interpreting Values**:
- **BASE_POSITION** (16):
  - **Good**: 16 (midpoint of 1-32 range, league average)
  - **Bad**: 0 (would treat all defenses as above average), >20 (skewed baseline)
- **STEPS** (2.5):
  - **Good**: 2-4 (creates fine-grained tiers across defense ranks)
  - **Bad**: <1.5 (too sensitive), >6 (too coarse, similar to old INCREASING)
- **WEIGHT** (0.51):
  - **Good**: 0.4-0.6 (schedule matters but isn't decisive)
  - **Bad**: <0.3 (ignores schedule), >1.0 (overweights uncertain future)
- **IMPACT_SCALE** (185.15):
  - **Current**: Same as MATCHUP (both ±4.6 pts)
  - **Alternative**: 80-120 (lower impact than current matchup, since future is uncertain)

**Why BI_EXCELLENT_HI Direction**:
- **Bidirectional**: Both easier (rank > 16) and harder (rank < 16) schedules matter
- **Centered on average**: Rank 16 represents league-average defense
- **Finer granularity**: STEPS=2.5 creates more nuanced tiers than old INCREASING/STEPS=6
- **Intuitive**: Positive deviation from 16 = easier opponents = bonus points

**Schedule vs Matchup Comparison**:

| Aspect | Matchup | Schedule |
|--------|---------|----------|
| **Timeframe** | Current week only | Rest of season |
| **Direction** | INCREASING (raw rank) | BI_EXCELLENT_HI (deviation from avg) |
| **BASE_POSITION** | 0 (rank 1-32) | 16 (league average) |
| **STEPS** | 6 (coarse tiers) | 2.5 (fine tiers) |
| **IMPACT_SCALE** | 185.15 | 185.15 (same) |
| **WEIGHT** | 0.51 | 0.51 (same) |
| **Effect** | ±4.6 pts | ±4.6 pts (same) |

**Recommendation**: Consider reducing SCHEDULE_IMPACT_SCALE to 100-120 (vs MATCHUP's 185) to give less weight to uncertain future matchups compared to immediate opponent

---

## Draft Configuration

### Draft Order Bonuses

Flat point bonuses awarded based on position and draft round to encourage positional value strategies.

```json
"DRAFT_ORDER_BONUSES": {
  "PRIMARY": 85.7408381861009,
  "SECONDARY": 94.62036179378356
}
```

| Field | Type | Description | Range |
|-------|------|-------------|-------|
| `PRIMARY` | float | Bonus for PRIMARY position in a round | 70-100 |
| `SECONDARY` | float | Bonus for SECONDARY position in a round | 75-100 |

**Good vs Bad Values**:
- **PRIMARY** (85.74):
  - **Good**: 80-95 (encourages drafting high-value positions)
  - **Bad**: <70 (too weak to influence decisions), >100 (overwhelms player value)
- **SECONDARY** (94.62):
  - **Good**: 85-100 (smaller than PRIMARY but still meaningful)
  - **Bad**: <80 (too weak), >110 (too strong, overrides player value)

**Typical Relationship**: SECONDARY ≈ PRIMARY + 5-15 pts (or sometimes PRIMARY > SECONDARY)

### Draft Order Strategy

Defines which positions to prioritize in each draft round.

```json
"DRAFT_ORDER": [
  {
    "FLEX": "P",
    "QB": "S"
  },
  {
    "FLEX": "P",
    "QB": "S"
  },
  // ... 15 rounds total
]
```

**Structure**: Array of objects, one per draft round (typically 15 rounds)

**Labels**:
- `"P"` = PRIMARY position (gets PRIMARY bonus)
- `"S"` = SECONDARY position (gets SECONDARY bonus)
- Unlisted positions get no bonus

**Common Strategies**:
- **Early Rounds (1-4)**: FLEX="P" (RB/WR), QB="S" (high-value skill positions)
- **Mid Rounds (5-10)**: QB="P", TE="P", FLEX="S" (fill key positions)
- **Late Rounds (11-15)**: K="P", DST="P", FLEX="S" (round out roster)

**Example Round 1**:
```json
{
  "FLEX": "P",  // RB/WR get +85.74 pts
  "QB": "S"     // QB gets +94.62 pts
}
```

**Interpretation**: In Round 1, prioritize FLEX-eligible positions (RB/WR) as PRIMARY, with QB as SECONDARY option.

---

## Roster Configuration

### Max Positions

Defines maximum players allowed per position on the roster.

```json
"MAX_POSITIONS": {
  "QB": 2,
  "RB": 3,
  "WR": 3,
  "FLEX": 3,
  "TE": 2,
  "K": 1,
  "DST": 1
}
```

**Total Roster Size**: Sum of all MAX_POSITIONS values (2+3+3+3+2+1+1 = 15 players)

**Required Positions**: All 7 positions must be defined (QB, RB, WR, FLEX, TE, K, DST)

**Validation**:
- Each value must be a positive integer
- FLEX represents additional flex slots beyond natural position slots
- Common roster sizes: 12-16 players

### Flex Eligible Positions

Defines which positions can fill FLEX slots.

```json
"FLEX_ELIGIBLE_POSITIONS": [
  "RB",
  "WR"
]
```

**Common Configurations**:
- `["RB", "WR"]` - Most common, allows RB/WR in FLEX
- `["RB", "WR", "TE"]` - Some leagues allow TE in FLEX
- `["WR"]` - WR-only FLEX (rare)

**Validation**:
- Cannot include "FLEX" (circular reference)
- Must contain at least one position
- Only valid positions: QB, RB, WR, TE, K, DST

---

## Penalty Configuration

### Injury Penalties

Flat point penalties applied based on injury risk level.

```json
"INJURY_PENALTIES": {
  "LOW": 0,
  "MEDIUM": 0,
  "HIGH": 100
}
```

| Risk Level | Current Penalty | Interpretation |
|------------|-----------------|----------------|
| `LOW` | 0 pts | No injury concern (healthy players) |
| `MEDIUM` | 0 pts | Minor injury concern (Questionable tag) |
| `HIGH` | -100 pts | Major injury concern (Out, IR, Doubtful) |

**Good vs Bad Values**:
- **LOW**: Should always be 0 (no penalty for healthy players)
- **MEDIUM**:
  - **Good**: 0-20 (small penalty for minor concerns)
  - **Bad**: >30 (too harsh for Questionable tag)
- **HIGH**:
  - **Good**: 80-120 (prevents drafting injured players)
  - **Bad**: <50 (insufficient deterrent), >150 (excessive)

**Current Strategy**: Binary approach (only HIGH-risk players penalized heavily)

**Alternative Strategy**: Graduated penalties (LOW=0, MEDIUM=20, HIGH=100)

### Bye Week Penalties

Calculated dynamically based on roster conflicts (not a fixed config value).

**Formula**:
```
penalty = (same_pos_median_total × SAME_POS_BYE_WEIGHT) +
          (diff_pos_median_total × DIFF_POS_BYE_WEIGHT)
```

**Where**:
- `same_pos_median_total` = sum of median weekly points for same-position players with same bye
- `diff_pos_median_total` = sum of median weekly points for different-position players with same bye

**Controlled By**: `SAME_POS_BYE_WEIGHT` and `DIFF_POS_BYE_WEIGHT` (see [Basic Parameters](#basic-parameters))

---

## Parameter Optimization

The configuration values are typically derived from simulation-based optimization using `SimulationManager.py`.

### Optimization Process

1. **Baseline Config**: Start with a known-good configuration
2. **Parameter Variation**: Generate combinations of 13+ parameters
3. **Simulation**: Run full league simulations (15 rounds × 100+ iterations)
4. **Evaluation**: Track win rate for each configuration
5. **Selection**: Choose config with highest win rate

### Optimized Parameters

The following parameters are actively optimized via simulation (as of Nov 2025):

| Parameter | Optimization Range | Current Optimal |
|-----------|-------------------|-----------------|
| NORMALIZATION_MAX_SCALE | 110-140 | 129.40 |
| SAME_POS_BYE_WEIGHT | 0.2-0.5 | 0.42 |
| DIFF_POS_BYE_WEIGHT | 0.0-0.2 | 0.16 |
| PRIMARY_BONUS | 70-90 | 85.74 |
| SECONDARY_BONUS | 75-95 | 94.62 |
| ADP_SCORING_WEIGHT | 2.0-3.0 | 2.81 |
| ADP_SCORING_STEPS | 25-40 | 32.27 |
| PLAYER_RATING_SCORING_WEIGHT | 0.5-1.5 | 0.79 |
| TEAM_QUALITY_SCORING_WEIGHT | 1.5-3.0 | 0.79 |
| PERFORMANCE_SCORING_WEIGHT | 1.5-3.0 | 0.58 |
| PERFORMANCE_SCORING_STEPS | 0.15-0.3 | 0.31 |
| MATCHUP_IMPACT_SCALE | 100-150 | 185.15 |
| MATCHUP_SCORING_WEIGHT | 0.5-1.0 | 0.51 |

**Fixed Parameters** (not optimized):
- PLAYER_RATING_SCORING_STEPS = 20
- TEAM_QUALITY_SCORING_STEPS = 6
- MATCHUP_SCORING_STEPS = 6
- All SCHEDULE_SCORING parameters (disabled)
- All MULTIPLIERS (always 0.95, 0.975, 1.025, 1.05)
- All DIRECTION values (determined by metric type)
- All BASE_POSITION values (always 0 or 0.0)

### Win Rate Interpretation

The `description` field often includes the win rate from simulation:

```json
"description": "Win Rate: 0.74"
```

| Win Rate | Interpretation |
|----------|----------------|
| 0.70-0.80 | Excellent configuration, well-optimized |
| 0.60-0.70 | Good configuration, competitive |
| 0.50-0.60 | Average configuration, room for improvement |
| <0.50 | Poor configuration, needs significant tuning |

**Note**: Win rate represents performance in simulated drafts against AI opponents using various strategies.

---

## Interpreting Parameter Values

### General Principles

1. **Balance is Key**: No single parameter should dominate scoring
2. **Weight Distribution**: Total "weight budget" should be spread across multiple factors
3. **Additive vs Multiplicative**: Understand when to use bonuses (additive) vs adjustments (multiplicative)
4. **Context Matters**: Draft mode prioritizes different factors than weekly lineup decisions

### Quick Health Checks

**Red Flags** (indicates poor configuration):
- Any WEIGHT > 5.0 (metric dominates score)
- NORMALIZATION_MAX_SCALE < 80 or > 180 (scoring too compressed or spread)
- PRIMARY_BONUS > 150 (draft bonuses overwhelm player value)
- MATCHUP_IMPACT_SCALE > 300 (single matchup overwhelms season value)
- All INJURY_PENALTIES = 0 (ignores injury risk completely)

**Good Signs** (indicates balanced configuration):
- All WEIGHT values between 0.3-3.0
- NORMALIZATION_MAX_SCALE near 120-140
- PRIMARY_BONUS < 100, SECONDARY_BONUS ≈ PRIMARY ± 15
- MATCHUP_IMPACT_SCALE between 100-200
- HIGH injury penalty >> MEDIUM penalty >> LOW penalty

### Parameter Interactions

Some parameters interact with each other:

1. **NORMALIZATION_MAX_SCALE × Multiplier Weights**:
   - Higher normalization = larger base scores
   - Higher weights = stronger multiplier effects
   - Together: can cause score inflation/deflation

2. **MATCHUP_IMPACT_SCALE × MATCHUP_SCORING_WEIGHT**:
   - Both control matchup influence
   - IMPACT_SCALE = absolute bonus size
   - WEIGHT = how much the rating tier matters
   - Balance both for appropriate matchup effect

3. **SAME_POS_BYE_WEIGHT vs DIFF_POS_BYE_WEIGHT**:
   - SAME_POS should be **higher** (more impactful)
   - Typical ratio: SAME_POS = 2-3× DIFF_POS
   - Example: SAME=0.4, DIFF=0.15 (ratio 2.67)

4. **PRIMARY_BONUS vs SECONDARY_BONUS**:
   - Can be PRIMARY > SECONDARY (traditional)
   - Or PRIMARY < SECONDARY (flexible drafting)
   - Gap should be 5-20 pts for meaningful difference

---

## Configuration Validation

The `ConfigManager.py` validates configurations on load.

### Required Fields

**Top Level**:
- `config_name` (string)
- `description` (string)
- `parameters` (object)

**Parameters** (all required):
- CURRENT_NFL_WEEK (int)
- NFL_SEASON (int)
- NFL_SCORING_FORMAT (string)
- NORMALIZATION_MAX_SCALE (float)
- SAME_POS_BYE_WEIGHT (float)
- DIFF_POS_BYE_WEIGHT (float)
- INJURY_PENALTIES (object with LOW, MEDIUM, HIGH)
- ADP_SCORING (object)
- PLAYER_RATING_SCORING (object)
- TEAM_QUALITY_SCORING (object)
- PERFORMANCE_SCORING (object)
- MATCHUP_SCORING (object)
- DRAFT_ORDER_BONUSES (object with PRIMARY, SECONDARY)
- DRAFT_ORDER (array)
- MAX_POSITIONS (object)
- FLEX_ELIGIBLE_POSITIONS (array)

**Each Scoring Section**:
- THRESHOLDS (object with BASE_POSITION, DIRECTION, STEPS)
- MULTIPLIERS (object with VERY_POOR, POOR, GOOD, EXCELLENT)
- WEIGHT (float)

**Optional Fields**:
- SCHEDULE_SCORING (object, defaults to disabled)
- IMPACT_SCALE (float, required for MATCHUP_SCORING and SCHEDULE_SCORING)
- MIN_WEEKS (int, required for PERFORMANCE_SCORING)

### Validation Rules

1. **STEPS must be positive**: `STEPS > 0`
2. **DIRECTION must be valid**: One of "INCREASING", "DECREASING", "BI_EXCELLENT_HI", "BI_EXCELLENT_LOW"
3. **BASE_POSITION must be finite**: Not NaN or Infinity
4. **MAX_POSITIONS must include all positions**: QB, RB, WR, TE, K, DST, FLEX
5. **MAX_POSITIONS values must be positive integers**: `value > 0`
6. **FLEX_ELIGIBLE_POSITIONS cannot include FLEX**: Prevents circular reference
7. **FLEX_ELIGIBLE_POSITIONS must be valid**: Only QB, RB, WR, TE, K, DST
8. **INJURY_PENALTIES must have all levels**: LOW, MEDIUM, HIGH
9. **DRAFT_ORDER_BONUSES must have both types**: PRIMARY, SECONDARY
10. **DRAFT_ORDER must be a list**: Typically 15 rounds

### Error Messages

Common validation errors:

```
"Configuration missing required fields: parameters"
"Config missing required parameters: ADP_SCORING, MATCHUP_SCORING"
"STEPS must be positive, got -5.0"
"DIRECTION must be one of ['INCREASING', 'DECREASING', ...], got 'INVALID'"
"MAX_POSITIONS[QB] must be a positive integer, got: 0"
"FLEX_ELIGIBLE_POSITIONS cannot contain 'FLEX' (circular reference)"
"INJURY_PENALTIES missing levels: MEDIUM, HIGH"
"MATCHUP_SCORING missing required parameter: IMPACT_SCALE"
```

---

## See Also

- **Scoring Algorithm Documentation**: `docs/scoring/README.md` (10-step algorithm overview)
- **ConfigManager Implementation**: `league_helper/util/ConfigManager.py` (config loading and validation)
- **Parameter Optimization**: `simulation/ConfigGenerator.py` (parameter range definitions)
- **Simulation System**: `simulation/SimulationManager.py` (optimization process)
- **Architecture Guide**: `ARCHITECTURE.md` (system design and data flow)

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-17 | 1.0 | Initial documentation created |

---

**End of Documentation**
