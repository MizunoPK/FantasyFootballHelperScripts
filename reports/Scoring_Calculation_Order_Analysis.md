# Scoring Calculation Order Analysis

**Date:** September 2025
**Question:** Are all static constants applied before multipliers?
**Answer:** ❌ **NO** - The order is complex and some static constants are applied AFTER multipliers.

---

## Complete Scoring Flow with Exact Order

### High-Level Formula

```python
total_score = pos_score + projection_score - bye_penalty - injury_penalty + matchup_adjustment
```

**Key Finding:** Static constants are used in DIFFERENT stages, some before multipliers, some after.

---

## Step-by-Step Execution Order

### STEP 1: Positional Need Score (Static Constants ONLY)

**Location:** `scoring_engine.py:83-115`

```python
def compute_positional_need_score(p):
    pos_score = (max_limit - current_count) * POS_NEEDED_SCORE  # Static: 65

    # FLEX bonus
    if pos in [RB, WR]:
        flex_need = (flex_limit - flex_count) * POS_NEEDED_SCORE * 0.5
        pos_score += flex_need

    return pos_score
```

**Constants Used:**
- `POS_NEEDED_SCORE = 65` (static constant)

**Example:**
```python
# Need 1 more QB (max: 2, current: 1)
pos_score = (2 - 1) * 65 = 65
```

**Applied:** ✅ Before any multipliers

---

### STEP 2: Projection Score (Multipliers Chain)

**Location:** `scoring_engine.py:117-191`

#### Sub-Step 2A: Get Base Score

```python
if hasattr(p, 'remaining_season_projection'):
    base_score = p.remaining_season_projection
elif hasattr(p, 'weighted_projection'):
    base_score = p.weighted_projection
else:
    base_score = p.fantasy_points
```

**Example:**
```python
base_score = 315.5  # Patrick Mahomes fantasy_points
```

**No constants applied yet** - just reading data from CSV.

---

#### Sub-Step 2B: Enhanced Scoring (First Set of Multipliers)

**Location:** `enhanced_scoring.py:76-155`

```python
def calculate_enhanced_score(base_fantasy_points, position, adp, player_rating,
                            team_offensive_rank, team_defensive_rank):

    total_multiplier = 1.0

    # Multiplier 1: ADP adjustment
    if adp <= 50:
        adp_mult = ADP_EXCELLENT_MULTIPLIER  # 1.15
    elif adp <= 100:
        adp_mult = ADP_GOOD_MULTIPLIER       # 1.08
    elif adp >= 200:
        adp_mult = ADP_POOR_MULTIPLIER       # 0.92
    else:
        adp_mult = 1.0

    total_multiplier *= adp_mult

    # Multiplier 2: Player rating adjustment
    if player_rating >= 80:
        rating_mult = PLAYER_RATING_EXCELLENT_MULTIPLIER  # 1.20
    elif player_rating >= 60:
        rating_mult = PLAYER_RATING_GOOD_MULTIPLIER       # 1.10
    elif player_rating <= 30:
        rating_mult = PLAYER_RATING_POOR_MULTIPLIER       # 0.90
    else:
        rating_mult = 1.0

    total_multiplier *= rating_mult

    # Multiplier 3: Team quality adjustment
    if team_offensive_rank <= 5:
        team_mult = TEAM_EXCELLENT_MULTIPLIER  # 1.12
    elif team_offensive_rank <= 12:
        team_mult = TEAM_GOOD_MULTIPLIER       # 1.06
    elif team_offensive_rank >= 25:
        team_mult = TEAM_POOR_MULTIPLIER       # 0.94
    else:
        team_mult = 1.0

    total_multiplier *= team_mult

    # Apply caps (multiplier constraints)
    total_multiplier = max(MIN_TOTAL_ADJUSTMENT,     # 0.70
                          min(MAX_TOTAL_ADJUSTMENT,  # 1.50
                              total_multiplier))

    enhanced_score = base_fantasy_points * total_multiplier

    return enhanced_score
```

**Example:**
```python
base_score = 315.5
adp_mult = 1.15  # ADP = 8
rating_mult = 1.20  # Rating = 92
team_mult = 1.12  # Team rank = 2

total_mult = 1.15 * 1.20 * 1.12 = 1.5456 → capped at 1.50

enhanced_score = 315.5 * 1.50 = 473.25
```

**Multipliers Used (config values):**
- `ADP_EXCELLENT_MULTIPLIER = 1.15`
- `ADP_GOOD_MULTIPLIER = 1.08`
- `ADP_POOR_MULTIPLIER = 0.92`
- `PLAYER_RATING_EXCELLENT_MULTIPLIER = 1.20`
- `PLAYER_RATING_GOOD_MULTIPLIER = 1.10`
- `PLAYER_RATING_POOR_MULTIPLIER = 0.90`
- `TEAM_EXCELLENT_MULTIPLIER = 1.12`
- `TEAM_GOOD_MULTIPLIER = 1.06`
- `TEAM_POOR_MULTIPLIER = 0.94`
- `MAX_TOTAL_ADJUSTMENT = 1.50` (cap)
- `MIN_TOTAL_ADJUSTMENT = 0.70` (floor)

**Result:** `projection_score = 473.25` after first multiplier chain

---

#### Sub-Step 2C: Positional Ranking Adjustment (Second Set of Multipliers)

**Location:** `positional_ranking_calculator.py:121-183`

```python
def calculate_positional_adjustment(player_team, position, base_points, current_week):

    # Get team rank
    our_rank = team_data.offensive_rank  # e.g., rank 2 for KC

    # Determine base multiplier from rank
    if our_rank <= 5:
        base_multiplier = EXCELLENT_MATCHUP  # 1.10
    elif our_rank <= 12:
        base_multiplier = GOOD_MATCHUP       # 1.05
    elif our_rank >= 25:
        base_multiplier = BAD_MATCHUP        # 0.95
    else:
        base_multiplier = NEUTRAL_MATCHUP    # 1.0

    # Apply weight factor
    adjustment_weight = ADJUSTMENT_WEIGHT  # 0.15
    final_multiplier = 1.0 + (base_multiplier - 1.0) * adjustment_weight

    adjusted_points = base_points * final_multiplier

    return adjusted_points
```

**Example (continuing from enhanced_score):**
```python
base_points = 473.25  # From enhanced scoring
our_rank = 2  # KC offensive rank

base_mult = 1.10  # Elite rank
weight = 0.15
final_mult = 1.0 + (1.10 - 1.0) * 0.15 = 1.015

adjusted_points = 473.25 * 1.015 = 480.35
```

**Multipliers Used (config values):**
- `EXCELLENT_MATCHUP = 1.10`
- `GOOD_MATCHUP = 1.05`
- `NEUTRAL_MATCHUP = 1.0`
- `BAD_MATCHUP = 0.95`
- `TERRIBLE_MATCHUP = 0.90`
- `ADJUSTMENT_WEIGHT = 0.15` (weight factor)

**Result:** `projection_score = 480.35` after second multiplier chain

---

### STEP 3: Bye Week Penalty (Static Constant - AFTER Multipliers)

**Location:** `scoring_engine.py:193-256`

```python
def compute_bye_penalty_for_player(player, exclude_self=False):

    if player_bye_week < CURRENT_NFL_WEEK:
        return 0  # Bye already passed

    # Count conflicts
    same_position_bye_count = count_roster_players_on_same_bye(position, bye_week)

    # Calculate penalty
    if position in [RB, WR]:  # FLEX eligible
        all_flex_bye_count = count_flex_players_on_same_bye(bye_week)

        if all_flex_bye_count >= 2:
            penalty = BASE_BYE_PENALTY * 1.5  # 15 * 1.5 = 22.5
        elif same_position_bye_count >= 1:
            penalty = BASE_BYE_PENALTY        # 15
        else:
            penalty = BASE_BYE_PENALTY * 0.5  # 7.5
    else:
        if same_position_bye_count >= 1:
            penalty = BASE_BYE_PENALTY * 1.5  # 22.5
        else:
            penalty = BASE_BYE_PENALTY        # 15

    return penalty
```

**Constants Used:**
- `BASE_BYE_PENALTY = 5` (static constant)
- Multipliers on penalty: 0.5, 1.0, 1.5 (context-dependent)

**Example:**
```python
# Mahomes bye week 6, no other QBs on bye week 6
bye_penalty = 5 * 1.0 = 5
```

**Applied:** ❌ AFTER all multipliers (subtracted from final score)

---

### STEP 4: Injury Penalty (Static Constant - AFTER Multipliers)

**Location:** `scoring_engine.py:257-287`

```python
def compute_injury_penalty(p, trade_mode=False):

    risk_level = p.get_risk_level()  # "LOW", "MEDIUM", "HIGH"

    # Check if we should skip injury penalties for roster players
    in_trade_mode = config.TRADE_HELPER_MODE or trade_mode
    if in_trade_mode and not config.APPLY_INJURY_PENALTY_TO_ROSTER and p.drafted == 2:
        return 0  # Skip penalty for roster players

    # Apply penalty from lookup table
    penalty = INJURY_PENALTIES[risk_level]

    return penalty
```

**Constants Used:**
```python
INJURY_PENALTIES = {
    "LOW": 0,      # Static constant
    "MEDIUM": 15,  # Static constant
    "HIGH": 35     # Static constant
}
```

**Example:**
```python
# Mahomes injury_status = "ACTIVE" → risk_level = "LOW"
injury_penalty = 0
```

**Applied:** ❌ AFTER all multipliers (subtracted from final score)

---

### STEP 5: Matchup Adjustment (Static Constant - AFTER Multipliers)

**Location:** `scoring_engine.py:68-72`

```python
matchup_adjustment = 0
if hasattr(p, 'matchup_adjustment') and p.matchup_adjustment is not None:
    matchup_adjustment = p.matchup_adjustment
```

**Constants Used:**
- `matchup_adjustment` (static value set by matchup analyzer, typically -2.0 to +2.0)

**Example:**
```python
matchup_adjustment = 0  # Not set for this example
```

**Applied:** ❌ AFTER all multipliers (added to final score)

---

### STEP 6: Final Score Calculation

**Location:** `scoring_engine.py:74-75`

```python
total_score = pos_score + projection_score - bye_penalty - injury_penalty + matchup_adjustment
```

**Example (Patrick Mahomes):**
```python
pos_score = 100           # Static constant math (STEP 1)
projection_score = 480.35 # After multipliers (STEP 2)
bye_penalty = 5          # Static constant (STEP 3)
injury_penalty = 0        # Static constant (STEP 4)
matchup_adjustment = 0    # Static constant (STEP 5)

total_score = 100 + 480.35 - 5 - 0 + 0 = 575.35
```

---

## Summary: When Each Type of Constant is Applied

### Static Constants BEFORE Multipliers

| Constant | Step | Value | Purpose |
|----------|------|-------|---------|
| `POS_NEEDED_SCORE` | 1 | 65 | Position need calculation |

**Applied to:** Base roster needs, BEFORE projection scoring

---

### Multipliers (Applied in Sequence)

| Multiplier Set | Step | Applied To | Config Values |
|---------------|------|------------|---------------|
| **Enhanced Scoring** | 2B | `base_score` | ADP, Rating, Team multipliers (1.0 - 1.5) |
| **Positional Ranking** | 2C | `enhanced_score` | Matchup multipliers (0.9 - 1.1) weighted at 15% |

**Applied to:** Fantasy point projections from CSV

---

### Static Constants AFTER Multipliers

| Constant | Step | Value | Purpose |
|----------|------|-------|---------|
| `BASE_BYE_PENALTY` | 3 | 5 | Bye week penalty |
| `INJURY_PENALTIES["LOW"]` | 4 | 0 | Healthy players |
| `INJURY_PENALTIES["MEDIUM"]` | 4 | 15 | Questionable players |
| `INJURY_PENALTIES["HIGH"]` | 4 | 35 | Injured players |
| `matchup_adjustment` | 5 | -2 to +2 | Matchup-specific bonus/penalty |

**Applied to:** Final score adjustments, AFTER all multiplier calculations

---

## Visual Flow Diagram

```
CSV Data (fantasy_points = 315.5)
    ↓
┌─────────────────────────────────┐
│ STEP 1: Position Need (Static) │
│ pos_score = 65 * 1 = 65        │
│ [Uses: POS_NEEDED_SCORE = 65]  │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ STEP 2A: Get Base Score         │
│ base_score = 315.5              │
│ [No constants yet]              │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ STEP 2B: Enhanced Scoring       │
│ 315.5 * 1.15 * 1.20 * 1.12     │
│ = 315.5 * 1.54 → cap at 1.50   │
│ = 473.25                        │
│ [Multipliers: ADP, Rating, Team]│
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ STEP 2C: Positional Ranking     │
│ 473.25 * 1.015 = 480.35        │
│ [Multiplier: Matchup (weighted)]│
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ STEP 3: Bye Week Penalty        │
│ penalty = 5 (static)            │
│ [Uses: BASE_BYE_PENALTY = 5]   │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ STEP 4: Injury Penalty          │
│ penalty = 0 (static lookup)     │
│ [Uses: INJURY_PENALTIES dict]  │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ STEP 5: Matchup Adjustment      │
│ adjustment = 0 (static)         │
│ [Uses: matchup_adjustment attr] │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ STEP 6: Final Score             │
│ 65 + 480.35 - 5 - 0 + 0        │
│ = 540.35                        │
└─────────────────────────────────┘
```

---

## Answer to Original Question

**Q: Are all static constants applied before multipliers?**

**A: NO** - The application order is:

1. **Position Need** (static) → Applied BEFORE multipliers
2. **Fantasy Points** → Base for multipliers
3. **Enhanced Scoring** (multipliers) → Applied to fantasy points
4. **Positional Ranking** (multipliers) → Applied to enhanced score
5. **Bye Penalty** (static) → Applied AFTER multipliers
6. **Injury Penalty** (static) → Applied AFTER multipliers
7. **Matchup Adjustment** (static) → Applied AFTER multipliers

---

## Why This Order Matters

### Example: Impact of Order

**Scenario: Player with 200 base points**

**Current Order (Correct):**
```python
# Multipliers first
enhanced = 200 * 1.50 = 300
positional = 300 * 1.015 = 304.5

# Static penalties after
final = 304.5 - 15 (bye) - 15 (injury) = 274.5
```

**If All Statics Were First (Hypothetical Wrong Order):**
```python
# Static penalties first
after_penalties = 200 - 15 - 15 = 170

# Multipliers after
enhanced = 170 * 1.50 = 255
positional = 255 * 1.015 = 258.8

# Final = 258.8 (much lower!)
```

**Difference:** 274.5 vs 258.8 = **15.7 points** difference

### Why Current Order is Correct

**Philosophy:**
1. **Multipliers represent comparative value** - "This player is X% better than average"
2. **Static penalties represent absolute costs** - "Losing a starter costs X points regardless of player quality"

**If penalties were applied first:**
- Elite injured players would be penalized LESS (because base is reduced before multiplication)
- Backup healthy players would look better relative to injured stars
- Doesn't match reality: losing Christian McCaffrey hurts more than losing a backup RB

**Current order (penalties after):**
- Elite players maintain elite scores, then pay penalty
- Properly models: "This is a great player (multipliers), BUT they're injured (penalty)"
- Matches fantasy manager thinking

---

## Configuration Summary

### Multiplier Config Locations

**Enhanced Scoring:**
```python
# File: shared_files/enhanced_scoring.py
DEFAULT_SCORING_CONFIG = {
    "adp_excellent_multiplier": 1.15,
    "adp_good_multiplier": 1.08,
    "adp_poor_multiplier": 0.92,
    "player_rating_excellent_multiplier": 1.20,
    "player_rating_good_multiplier": 1.10,
    "player_rating_poor_multiplier": 0.90,
    "team_excellent_multiplier": 1.12,
    "team_good_multiplier": 1.06,
    "team_poor_multiplier": 0.94,
    "max_total_adjustment": 1.50,
    "min_total_adjustment": 0.70,
}
```

**Positional Ranking:**
```python
# File: shared_files/positional_ranking_calculator.py
config = {
    "excellent_matchup": 1.1,
    "good_matchup": 1.05,
    "neutral_matchup": 1.0,
    "bad_matchup": 0.95,
    "terrible_matchup": 0.9,
    "adjustment_weight": 0.15,
}
```

### Static Constant Config Locations

**Positional Need:**
```python
# File: draft_helper/draft_helper_config.py
POS_NEEDED_SCORE = 65
```

**Penalties:**
```python
# File: draft_helper/draft_helper_config.py
BASE_BYE_PENALTY = 5

INJURY_PENALTIES = {
    "LOW": 0,
    "MEDIUM": 15,
    "HIGH": 35
}
```

---

## Implications for Tuning

### To Adjust Relative Player Values (Use Multipliers)

**Want to boost elite players more?**
```python
# Increase multipliers
ADP_EXCELLENT_MULTIPLIER = 1.20  # Was 1.15
PLAYER_RATING_EXCELLENT_MULTIPLIER = 1.25  # Was 1.20
```

**Impact:** Elite players get bigger boost, gap between elite and average widens.

---

### To Adjust Absolute Penalties (Use Static Constants)

**Want to care less about bye weeks?**
```python
# Decrease static penalty
BASE_BYE_PENALTY = 3  # Was 5
```

**Impact:** All bye week conflicts penalized less, regardless of player quality.

**Want to be more risk-averse about injuries?**
```python
# Increase static penalties
INJURY_PENALTIES["MEDIUM"] = 25  # Was 15
INJURY_PENALTIES["HIGH"] = 50    # Was 35
```

**Impact:** All injured players penalized more, regardless of talent level.

---

## Conclusion

**Static constants are NOT all applied before multipliers.**

**Actual Order:**
1. Position need (static) - BEFORE
2. Enhanced scoring (multipliers) - ON fantasy points
3. Positional ranking (multipliers) - ON enhanced score
4. Penalties (static) - AFTER all multipliers

**This order is intentional and correct** because:
- Multipliers model **relative value** (comparative)
- Static constants model **absolute costs** (fixed impact)
- Applying penalties after multipliers properly values elite injured players vs healthy backups

---

**End of Analysis**