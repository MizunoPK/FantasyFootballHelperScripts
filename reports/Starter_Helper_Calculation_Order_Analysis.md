# Starter Helper - Calculation Order Analysis

**Date:** September 2025
**Purpose:** Document the exact order of scoring calculations in Starter Helper mode
**Key Difference:** Much simpler than Draft Helper - uses penalties only, NO multipliers for player value

---

## Executive Summary

### Calculation Formula

```python
adjusted_score = projected_points - injury_penalty - bye_week_penalty + positional_ranking_adjustment
```

**Key Differences from Draft Helper:**
1. ❌ **No positional need score** - filling fixed lineup slots, not building roster
2. ❌ **No enhanced scoring multipliers** - no ADP, player rating, or team quality multipliers
3. ✅ **Uses weekly projections** - `week_N_points` columns, not season totals
4. ✅ **Absolute penalties** - injured/bye players should NOT start (0 points)
5. ✅ **Positional ranking multipliers** - only multipliers used (same as Draft Helper)

---

## Complete Scoring Flow

### STEP 0: Get Weekly Projection (Pre-Calculation)

**Location:** `starter_helper.py` (main script)

```python
def get_weekly_projection(player, current_week):
    """Get projection for specific week from players.csv"""

    # Try to get week-specific projection
    week_column = f'week_{current_week}_points'
    if hasattr(player, week_column):
        weekly_points = getattr(player, week_column)
        if weekly_points is not None and weekly_points > 0:
            return weekly_points

    # Fallback: use season average
    if player.fantasy_points > 0:
        return player.fantasy_points / 17.0  # 17-week fantasy regular season

    return 0.0
```

**Example:**
```python
# Week 5 for Patrick Mahomes
# CSV has: week_5_points = 18.6
projected_points = 18.6

# If week_5_points missing, fallback:
projected_points = 315.5 / 17 = 18.6  # Season average per week
```

**Data Source:**
- Primary: `week_N_points` columns in `players.csv`
- Fallback: `fantasy_points / 17`

**No calculations yet** - just reading data.

---

### STEP 1: Start with Weekly Projection

**Location:** `lineup_optimizer.py:88-144`

```python
def calculate_adjusted_score(projected_points, injury_status, bye_week,
                            player_team=None, player_position=None):

    adjusted_score = projected_points  # Start with weekly projection
    reasons = []

    # ... penalties applied next
```

**Example:**
```python
adjusted_score = 18.6  # Patrick Mahomes week 5 projection
```

**Type:** Base value (no constants or multipliers)

---

### STEP 2: Apply Injury Penalty (Static Constant)

**Location:** `lineup_optimizer.py:110-115`

```python
# Apply injury penalty
if injury_status in INJURY_PENALTIES:
    penalty = INJURY_PENALTIES[injury_status]
    adjusted_score -= penalty
    if penalty > 0:
        reasons.append(f"-{penalty} injury penalty ({injury_status})")
```

**Constants Used:**
```python
INJURY_PENALTIES = {
    "ACTIVE": 0,           # No penalty
    "LOW": 0,              # Healthy
    "MEDIUM": 0,           # Questionable (configured to ignore)
    "HIGH": 50,            # Doubtful (major penalty)
    "OUT": 100,            # Cannot start
    "INJURY_RESERVE": 100, # Cannot start
    "SUSPENSION": 100,     # Cannot start
    "DOUBTFUL": 50,
    "QUESTIONABLE": 0,
}
```

**Example:**
```python
# Mahomes injury_status = "ACTIVE"
penalty = 0
adjusted_score = 18.6 - 0 = 18.6
```

**Type:** Static constant (subtraction)

**Design Philosophy:**
- **OUT/IR = 100 points penalty** → Makes score deeply negative, ensuring they're never selected
- **HIGH = 50 points penalty** → Severe penalty, usually drops below bench alternatives
- **MEDIUM/QUESTIONABLE = 0** → Configured to start questionable players (user preference)

---

### STEP 3: Apply Bye Week Penalty (Static Constant)

**Location:** `lineup_optimizer.py:117-120`

```python
# Apply bye week penalty
if bye_week == CURRENT_NFL_WEEK:
    adjusted_score -= BYE_WEEK_PENALTY
    reasons.append(f"-{BYE_WEEK_PENALTY} bye week penalty")
```

**Constant Used:**
```python
BYE_WEEK_PENALTY = 1000  # Massive penalty - should NEVER start
```

**Example:**
```python
# Mahomes bye_week = 6, CURRENT_NFL_WEEK = 5
# Not on bye this week
penalty = 0
adjusted_score = 18.6 - 0 = 18.6
```

**Type:** Static constant (subtraction)

**Design Philosophy:**
- **1000 points penalty** → Absolutely ensures players on bye are NEVER selected
- Doesn't matter if they're the best player - bye week = cannot play = 0 contribution

---

### STEP 4: Apply Positional Ranking Adjustment (Multiplier)

**Location:** `lineup_optimizer.py:122-141`

```python
# Apply positional ranking adjustment if available
if (self.positional_ranking_calculator and
    self.positional_ranking_calculator.is_positional_ranking_available() and
    player_team and player_position):

    ranking_adjusted_points, ranking_explanation = self.positional_ranking_calculator.calculate_positional_adjustment(
        player_team=player_team,
        position=player_position,
        base_points=adjusted_score,
        current_week=CURRENT_NFL_WEEK
    )

    # Apply the adjustment
    ranking_adjustment = ranking_adjusted_points - adjusted_score
    adjusted_score = ranking_adjusted_points

    # Add explanation if significant adjustment
    if abs(ranking_adjustment) >= 0.5:
        sign = "+" if ranking_adjustment > 0 else ""
        reasons.append(f"{sign}{ranking_adjustment:.1f} rank adj ({ranking_explanation})")
```

**Multiplier Calculation (from `positional_ranking_calculator.py`):**
```python
# Get team rank
our_rank = team_data.offensive_rank  # e.g., 2 for KC

# Determine base multiplier
if our_rank <= 5:
    base_multiplier = 1.10  # Elite
elif our_rank <= 12:
    base_multiplier = 1.05  # Good
elif our_rank >= 25:
    base_multiplier = 0.95  # Poor
else:
    base_multiplier = 1.0   # Neutral

# Apply weight factor
weight = 0.15  # 15% impact
final_multiplier = 1.0 + (base_multiplier - 1.0) * weight

adjusted_points = base_points * final_multiplier
```

**Example:**
```python
base_points = 18.6  # After injury/bye penalties
our_rank = 2  # KC offensive rank

base_mult = 1.10  # Elite
weight = 0.15
final_mult = 1.0 + (1.10 - 1.0) * 0.15 = 1.015

adjusted_points = 18.6 * 1.015 = 18.88
ranking_adjustment = +0.28
```

**Type:** Multiplier (same as Draft Helper positional ranking)

**Config Values:**
```python
EXCELLENT_MATCHUP = 1.10
GOOD_MATCHUP = 1.05
NEUTRAL_MATCHUP = 1.0
BAD_MATCHUP = 0.95
TERRIBLE_MATCHUP = 0.90
ADJUSTMENT_WEIGHT = 0.15  # 15% impact
```

---

### STEP 5: Floor at Zero

**Location:** `lineup_optimizer.py:144`

```python
return max(0.0, adjusted_score), reason
```

**Example:**
```python
# Normal case
adjusted_score = 18.88
final_score = max(0.0, 18.88) = 18.88

# Player on bye
adjusted_score = 18.6 - 1000 = -981.4
final_score = max(0.0, -981.4) = 0.0  # Cannot be negative
```

**Type:** Floor constraint

**Purpose:** Prevents negative scores from skewing total lineup calculations.

---

## Complete Example Calculation

### Example 1: Healthy Elite QB (Patrick Mahomes)

**Input Data:**
```python
name = "Patrick Mahomes"
position = "QB"
team = "KC"
week_5_points = 18.6
injury_status = "ACTIVE"
bye_week = 6
CURRENT_NFL_WEEK = 5
team_offensive_rank = 2  # Elite
```

**Calculation:**
```python
# STEP 1: Start with weekly projection
adjusted_score = 18.6

# STEP 2: Injury penalty
penalty = INJURY_PENALTIES["ACTIVE"] = 0
adjusted_score = 18.6 - 0 = 18.6

# STEP 3: Bye week penalty
# bye_week (6) != CURRENT_NFL_WEEK (5)
penalty = 0
adjusted_score = 18.6 - 0 = 18.6

# STEP 4: Positional ranking adjustment
base_mult = 1.10 (Elite offense, rank 2)
final_mult = 1.0 + (1.10 - 1.0) * 0.15 = 1.015
adjusted_score = 18.6 * 1.015 = 18.88

# STEP 5: Floor at zero
final_score = max(0.0, 18.88) = 18.88
```

**Result:** `18.88 points` with reason `+0.3 rank adj (Elite offensive (rank 2): +1.5%)`

---

### Example 2: Injured RB (Christian McCaffrey)

**Input Data:**
```python
name = "Christian McCaffrey"
position = "RB"
team = "SF"
week_5_points = 22.4
injury_status = "DOUBTFUL"
bye_week = 9
CURRENT_NFL_WEEK = 5
team_offensive_rank = 4  # Elite
```

**Calculation:**
```python
# STEP 1: Start with weekly projection
adjusted_score = 22.4

# STEP 2: Injury penalty
penalty = INJURY_PENALTIES["DOUBTFUL"] = 50
adjusted_score = 22.4 - 50 = -27.6

# STEP 3: Bye week penalty
# bye_week (9) != CURRENT_NFL_WEEK (5)
penalty = 0
adjusted_score = -27.6 - 0 = -27.6

# STEP 4: Positional ranking adjustment
base_mult = 1.10 (Elite offense, rank 4)
final_mult = 1.015
adjusted_score = -27.6 * 1.015 = -28.01

# STEP 5: Floor at zero
final_score = max(0.0, -28.01) = 0.0
```

**Result:** `0.0 points` with reason `-50 injury penalty (DOUBTFUL); -0.4 rank adj`

**Impact:** Will NOT be selected for starting lineup (backup RB with 5 points would be better).

---

### Example 3: Player on Bye Week

**Input Data:**
```python
name = "Tyreek Hill"
position = "WR"
team = "MIA"
week_6_points = 19.2
injury_status = "ACTIVE"
bye_week = 6
CURRENT_NFL_WEEK = 6
team_offensive_rank = 7  # Good
```

**Calculation:**
```python
# STEP 1: Start with weekly projection
adjusted_score = 19.2

# STEP 2: Injury penalty
penalty = 0
adjusted_score = 19.2 - 0 = 19.2

# STEP 3: Bye week penalty
# bye_week (6) == CURRENT_NFL_WEEK (6) ← ON BYE!
penalty = 1000
adjusted_score = 19.2 - 1000 = -980.8

# STEP 4: Positional ranking adjustment
base_mult = 1.05 (Good offense, rank 7)
final_mult = 1.0 + (1.05 - 1.0) * 0.15 = 1.0075
adjusted_score = -980.8 * 1.0075 = -988.15

# STEP 5: Floor at zero
final_score = max(0.0, -988.15) = 0.0
```

**Result:** `0.0 points` with reason `-1000 bye week penalty; -7.4 rank adj`

**Impact:** Absolutely will NOT be selected (even though he's elite - he can't play this week).

---

## Order Comparison: Starter Helper vs Draft Helper

### Starter Helper Order (Current)

```
1. Weekly Projection (from CSV)
    ↓
2. Injury Penalty (static: 0-100)
    ↓
3. Bye Week Penalty (static: 1000)
    ↓
4. Positional Ranking Adjustment (multiplier: ~1.5%)
    ↓
5. Floor at 0
```

### Draft Helper Order (For Comparison)

```
1. Position Need Score (static: 65)
    ↓
2. Base Fantasy Points (from CSV)
    ↓
3. Enhanced Scoring (multipliers: ADP, rating, team)
    ↓
4. Positional Ranking (multiplier: ~1.5%)
    ↓
5. Bye Week Penalty (static: 5)
    ↓
6. Injury Penalty (static: 0-35)
    ↓
7. Matchup Adjustment (static: ±2)
```

---

## Key Design Differences

### 1. Philosophy

**Starter Helper:**
- **Binary decisions**: Can this player start THIS WEEK?
- **Absolute penalties**: OUT/BYE = cannot play = massive penalty
- **Weekly focus**: Only cares about current week performance
- **No comparison needed**: Not comparing players to each other for value

**Draft Helper:**
- **Relative value**: How does this player compare to alternatives?
- **Proportional adjustments**: Elite players still valuable even if injured
- **Season focus**: Building a roster for entire season
- **Comparison critical**: Must rank all players for draft order

---

### 2. Penalty Magnitudes

| Penalty Type | Starter Helper | Draft Helper | Ratio |
|--------------|---------------|--------------|-------|
| **Bye Week** | 1000 | 5 | 200x |
| **OUT** | 100 | 35 | 3x |
| **DOUBTFUL** | 50 | 35 | 1.4x |
| **QUESTIONABLE** | 0 | 15 | 0x |

**Why so different?**

**Starter Helper:**
- Bye week = player CANNOT play → Must ensure score = 0
- OUT = player CANNOT play → Must ensure they're never selected
- Questionable = might play → User decision (configured to allow)

**Draft Helper:**
- Bye week = minor scheduling concern → Small penalty (you have 17 weeks)
- OUT = injury risk → Moderate penalty (might heal, has trade value)
- Questionable = probable starter → Small penalty (most play)

---

### 3. Multipliers

| Multiplier Type | Starter Helper | Draft Helper |
|-----------------|---------------|--------------|
| **ADP** | ❌ None | ✅ ±15% |
| **Player Rating** | ❌ None | ✅ ±20% |
| **Team Quality** | ❌ None | ✅ ±12% |
| **Positional Ranking** | ✅ ±1.5% | ✅ ±1.5% |

**Why no ADP/Rating/Team in Starter Helper?**

**Not Relevant for Weekly Decisions:**
- ADP = draft value (doesn't matter once drafted)
- Player Rating = season-long skill (already baked into weekly projections)
- Team Quality = season-long context (already baked into weekly projections)

**Only Positional Ranking Used:**
- Matchup quality changes week-to-week
- Elite offense vs bad defense THIS WEEK matters
- Weekly projections don't capture opponent matchup

---

### 4. Score Magnitude

**Starter Helper:**
```python
# Typical score range
Healthy QB: 15-25 points
Healthy RB: 10-20 points
Injured player: 0 points (penalty > projection)
Bye week: 0 points (massive penalty)
```

**Draft Helper:**
```python
# Typical score range
Elite QB: 400-600 points
Good RB: 250-400 points
Injured player: Still 200-300 points (elite talent - injury penalty)
Position need: +50-100 points (roster construction bonus)
```

**Result:** Starter Helper scores are ~20x smaller (weekly vs seasonal).

---

## Configuration Constants

### Injury Penalties

```python
# File: starter_helper/starter_helper_config.py
INJURY_PENALTIES = {
    "ACTIVE": 0,           # Healthy
    "LOW": 0,              # Healthy
    "MEDIUM": 0,           # Questionable (user choice: allow)
    "HIGH": 50,            # Doubtful (major penalty)
    "OUT": 100,            # Cannot start
    "INJURY_RESERVE": 100, # Cannot start
    "SUSPENSION": 100,     # Cannot start
    "DOUBTFUL": 50,
    "QUESTIONABLE": 0,
}
```

**Tuning Guide:**
- Increase `MEDIUM` penalty to be more conservative about questionable players
- Decrease `HIGH` penalty if you're willing to gamble on doubtful players
- `OUT`/`IR`/`SUSPENSION` should stay at 100 (they literally cannot play)

---

### Bye Week Penalty

```python
# File: starter_helper/starter_helper_config.py
BYE_WEEK_PENALTY = 1000  # Massive penalty
```

**Why 1000?**
- Ensures bye week players score negative (even elite projections ~25)
- Floor at 0 means they score 0, guaranteeing they're never selected
- Any value >50 would work, but 1000 makes intent crystal clear

**Should NOT be tuned** - players on bye cannot play.

---

### Positional Ranking Adjustments

```python
# File: shared_files/positional_ranking_calculator.py
config = {
    "excellent_matchup": 1.10,    # ±10% before weighting
    "good_matchup": 1.05,          # ±5% before weighting
    "neutral_matchup": 1.0,
    "bad_matchup": 0.95,
    "terrible_matchup": 0.90,
    "adjustment_weight": 0.15,     # 15% impact
}
```

**Actual Impact:**
- Elite matchup: +1.5% points (10% * 15% weight)
- Good matchup: +0.75% points (5% * 15% weight)
- Bad matchup: -0.75% points
- Terrible matchup: -1.5% points

**Tuning Guide:**
- Increase `adjustment_weight` to 0.20-0.30 for more matchup emphasis
- Decrease to 0.10 to reduce matchup impact
- Change multiplier thresholds to adjust tier definitions

---

## Visual Flow Diagram

```
players.csv (week_5_points = 18.6)
    ↓
┌─────────────────────────────────────┐
│ STEP 0: Get Weekly Projection       │
│ projected_points = 18.6             │
│ [Source: week_5_points column]     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 1: Start with Projection       │
│ adjusted_score = 18.6               │
│ [No constants yet]                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 2: Injury Penalty (Static)     │
│ adjusted_score = 18.6 - 0 = 18.6   │
│ [INJURY_PENALTIES["ACTIVE"] = 0]   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 3: Bye Week Penalty (Static)   │
│ adjusted_score = 18.6 - 0 = 18.6   │
│ [BYE_WEEK_PENALTY = 1000, not on bye]│
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 4: Positional Ranking (Mult)   │
│ adjusted_score = 18.6 * 1.015      │
│                = 18.88              │
│ [Multiplier: 1.0 + 0.10 * 0.15]   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 5: Floor at Zero               │
│ final_score = max(0.0, 18.88)      │
│             = 18.88                 │
└─────────────────────────────────────┘
```

---

## Summary

### Order Answer

**All static constants applied before multipliers?**
- ✅ **YES** - Injury penalty (static) applied first
- ✅ **YES** - Bye week penalty (static) applied second
- ❌ **THEN** - Positional ranking (multiplier) applied last

**But it doesn't matter much because:**
- Penalties so large they dominate calculation
- Multiplier impact tiny (~1.5%) compared to penalties (50-1000)
- Order mostly irrelevant when penalty = 1000 (result is 0 either way)

---

### Key Takeaways

1. **Much simpler than Draft Helper** - Only 4 calculation steps vs 7
2. **No value multipliers** - No ADP, rating, or team quality adjustments
3. **Absolute penalties** - Designed to force score to 0 for unplayable players
4. **Weekly focus** - Uses `week_N_points`, not season totals
5. **Only one multiplier** - Positional ranking (~1.5% impact)

---

### Configuration Files

**Main Config:**
```python
# starter_helper/starter_helper_config.py
INJURY_PENALTIES = {...}      # Adjust injury risk tolerance
BYE_WEEK_PENALTY = 1000       # Should not change
```

**Positional Ranking:**
```python
# shared_files/positional_ranking_calculator.py
config = {
    "adjustment_weight": 0.15,  # Tune matchup impact
    ...
}
```

---

**End of Analysis**