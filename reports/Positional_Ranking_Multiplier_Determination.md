# Positional Ranking Multiplier Determination

**Date:** September 2025
**Question:** How is the positional ranking multiplier determined in Starter Helper?
**Answer:** It's based on **team offensive/defensive rankings** from `teams.csv`, NOT on opponent matchups

---

## Quick Answer

The positional ranking multiplier is determined by:

1. **Player's team rank** (offensive or defensive) from `teams.csv`
2. **Position-specific logic** (QB/RB/WR/TE use offensive rank, DST uses defensive rank)
3. **Rank threshold tiers** (Elite/Good/Average/Poor)
4. **Base multiplier** (0.90 - 1.10 depending on tier)
5. **Weight factor** (15% - reduces impact to ±1.5% max)

**Key Insight:** It's based on **your player's team quality**, NOT the opponent they're facing this week.

---

## Complete Flow Diagram

```
Player: Patrick Mahomes (QB, KC)
    ↓
┌────────────────────────────────────────────┐
│ STEP 1: Determine Which Rank to Use       │
│ Position = QB (offensive position)         │
│ → Use team OFFENSIVE rank                  │
└────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────┐
│ STEP 2: Look Up Team Data                 │
│ Read teams.csv for KC:                     │
│ - offensive_rank = 14                      │
│ - defensive_rank = 16                      │
│ - opponent = BAL                           │
└────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────┐
│ STEP 3: Determine Rank Tier               │
│ offensive_rank = 14                        │
│ Check thresholds:                          │
│ - 14 > 5 (excellent_threshold)            │
│ - 14 > 12 (good_threshold)                │
│ - 14 < 25 (poor_threshold)                │
│ → Tier: AVERAGE                           │
└────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────┐
│ STEP 4: Get Base Multiplier               │
│ Tier = AVERAGE                             │
│ → base_multiplier = neutral_matchup = 1.0  │
└────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────┐
│ STEP 5: Apply Weight Factor               │
│ base_multiplier = 1.0                      │
│ adjustment_weight = 0.15                   │
│ final_mult = 1.0 + (1.0 - 1.0) * 0.15    │
│            = 1.0 + 0.0 = 1.0              │
└────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────┐
│ STEP 6: Apply to Player Score             │
│ base_points = 18.6                         │
│ adjusted_points = 18.6 * 1.0 = 18.6       │
│ adjustment = 0.0 (no change)               │
└────────────────────────────────────────────┘
```

---

## Detailed Step-by-Step

### STEP 1: Determine Which Rank to Use

**Location:** `positional_ranking_calculator.py:145-159`

```python
# Determine which ranking to use based on position
if position in ["QB", "RB", "WR", "TE"]:
    # Offensive players: use team offensive rank
    our_rank = team_data.offensive_rank
    context = "offensive"
elif position in ["DST"]:
    # Defensive players: use team defensive rank
    our_rank = team_data.defensive_rank
    context = "defensive"
elif position in ["K"]:
    # Kickers: use team offensive rank (field goal opportunities)
    our_rank = team_data.offensive_rank
    context = "offensive (kicking)"
else:
    return base_points, f"No adjustment (unknown position {position})"
```

**Position Mapping:**
| Position | Uses Which Rank | Logic |
|----------|----------------|-------|
| QB | Offensive | Good offense = more passing yards/TDs |
| RB | Offensive | Good offense = more rushing yards/TDs |
| WR | Offensive | Good offense = more receiving yards/TDs |
| TE | Offensive | Good offense = more receiving yards/TDs |
| K | Offensive | Good offense = more field goal opportunities |
| DST | Defensive | Good defense = more sacks/INTs/TDs |

**Example:**
```python
# Patrick Mahomes (QB)
position = "QB"
→ Use offensive_rank

# Pittsburgh Steelers DST
position = "DST"
→ Use defensive_rank
```

---

### STEP 2: Look Up Team Data

**Data Source:** `shared_files/teams.csv`

**CSV Structure:**
```csv
team,offensive_rank,defensive_rank,opponent
KC,14,16,BAL
DET,1,8,CLE
BUF,2,13,NO
PIT,16,2,MIN
```

**Loading Process:**
```python
# On initialization
teams = load_teams_from_csv('shared_files/teams.csv')
team_data_cache = {team.team: team for team in teams}

# During calculation
team_data = team_data_cache.get('KC')
# Returns: TeamData(team='KC', offensive_rank=14, defensive_rank=16, opponent='BAL')
```

**Example Lookups:**
```python
# KC Chiefs
team_data = team_data_cache['KC']
→ offensive_rank = 14, defensive_rank = 16, opponent = 'BAL'

# Detroit Lions
team_data = team_data_cache['DET']
→ offensive_rank = 1, defensive_rank = 8, opponent = 'CLE'

# Pittsburgh Steelers
team_data = team_data_cache['PIT']
→ offensive_rank = 16, defensive_rank = 2, opponent = 'MIN'
```

**Important:** The `opponent` field is stored but **NOT currently used** in the calculation. The adjustment is based solely on the team's own quality rank.

---

### STEP 3: Determine Rank Tier

**Location:** `positional_ranking_calculator.py:185-194`

```python
def _get_multiplier_from_rank(self, rank: int) -> float:
    """Convert team rank to adjustment multiplier."""
    if rank <= self.config["excellent_threshold"]:  # 5
        return self.config["excellent_matchup"]      # 1.10
    elif rank <= self.config["good_threshold"]:     # 12
        return self.config["good_matchup"]           # 1.05
    elif rank >= self.config["poor_threshold"]:     # 25
        return self.config["bad_matchup"]            # 0.95
    else:
        return self.config["neutral_matchup"]        # 1.0
```

**Threshold Configuration:**
```python
"excellent_threshold": 5,     # Rank 1-5 (top tier)
"good_threshold": 12,         # Rank 6-12 (above average)
"poor_threshold": 25,         # Rank 25-32 (bottom tier)
# Ranks 13-24 = neutral/average
```

**Tier Breakdown:**
| Rank Range | Tier | Base Multiplier | Description |
|------------|------|----------------|-------------|
| 1-5 | Elite | 1.10 | Top 5 teams (+10%) |
| 6-12 | Good | 1.05 | Above average (+5%) |
| 13-24 | Average | 1.0 | Middle tier (no adjustment) |
| 25-32 | Poor | 0.95 | Bottom tier (-5%) |

**Examples:**
```python
# Detroit Lions (rank 1 offense)
rank = 1
→ 1 <= 5 (excellent)
→ base_multiplier = 1.10 (Elite)

# Kansas City Chiefs (rank 14 offense)
rank = 14
→ 14 > 5, 14 > 12, 14 < 25
→ base_multiplier = 1.0 (Average)

# Tennessee Titans (rank 32 offense)
rank = 32
→ 32 >= 25 (poor)
→ base_multiplier = 0.95 (Poor)

# Pittsburgh Steelers (rank 2 defense)
rank = 2
→ 2 <= 5 (excellent)
→ base_multiplier = 1.10 (Elite)
```

---

### STEP 4: Get Base Multiplier

**Multiplier Config:**
```python
"excellent_matchup": 1.1,    # 10% boost for great teams
"good_matchup": 1.05,         # 5% boost for good teams
"neutral_matchup": 1.0,       # No adjustment for average teams
"bad_matchup": 0.95,          # 5% penalty for bad teams
"terrible_matchup": 0.9,     # 10% penalty for terrible teams (not used in tiers)
```

**Note:** `terrible_matchup` (0.9) is defined but **not currently used** by the tier system. The `bad_matchup` (0.95) is applied to ranks 25-32.

**Visual Scale:**
```
Rank:  1    5    12        24   25        32
Tier:  [Elite][Good][Average][Poor]
Mult:  1.10  1.05  1.0      0.95

       +10%  +5%   0%       -5%
```

---

### STEP 5: Apply Weight Factor

**Location:** `positional_ranking_calculator.py:167-169`

```python
weight = self.config["adjustment_weight"]  # 0.15
final_multiplier = 1.0 + (multiplier - 1.0) * weight
```

**Weight Factor:** `adjustment_weight = 0.15` (15% of the full effect)

**Formula:**
```python
final_multiplier = 1.0 + (base_multiplier - 1.0) * weight
```

**Why the weight factor?**
- Reduces the impact to a conservative level
- Prevents team quality from dominating weekly projections
- Makes adjustment more of a "tiebreaker" than primary factor

**Calculation Examples:**

**Elite Team (rank 1-5):**
```python
base_multiplier = 1.10
weight = 0.15
final_multiplier = 1.0 + (1.10 - 1.0) * 0.15
                 = 1.0 + 0.10 * 0.15
                 = 1.0 + 0.015
                 = 1.015

Impact: +1.5% boost
```

**Good Team (rank 6-12):**
```python
base_multiplier = 1.05
weight = 0.15
final_multiplier = 1.0 + (1.05 - 1.0) * 0.15
                 = 1.0 + 0.05 * 0.15
                 = 1.0 + 0.0075
                 = 1.0075

Impact: +0.75% boost
```

**Average Team (rank 13-24):**
```python
base_multiplier = 1.0
weight = 0.15
final_multiplier = 1.0 + (1.0 - 1.0) * 0.15
                 = 1.0 + 0.0
                 = 1.0

Impact: 0% (no change)
```

**Poor Team (rank 25-32):**
```python
base_multiplier = 0.95
weight = 0.15
final_multiplier = 1.0 + (0.95 - 1.0) * 0.15
                 = 1.0 + (-0.05) * 0.15
                 = 1.0 - 0.0075
                 = 0.9925

Impact: -0.75% penalty
```

**Actual Impact Summary:**
| Tier | Base Multiplier | Final Multiplier | Effective Impact |
|------|----------------|------------------|------------------|
| Elite (1-5) | 1.10 | 1.015 | +1.5% |
| Good (6-12) | 1.05 | 1.0075 | +0.75% |
| Average (13-24) | 1.0 | 1.0 | 0% |
| Poor (25-32) | 0.95 | 0.9925 | -0.75% |

---

### STEP 6: Apply to Player Score

**Location:** `positional_ranking_calculator.py:171`

```python
adjusted_points = base_points * final_multiplier
```

**Examples:**

**Example 1: Elite Team QB**
```python
# Jared Goff (DET, rank 1 offense)
base_points = 20.0
final_multiplier = 1.015
adjusted_points = 20.0 * 1.015 = 20.3

Gain: +0.3 points
```

**Example 2: Average Team QB**
```python
# Patrick Mahomes (KC, rank 14 offense)
base_points = 18.6
final_multiplier = 1.0
adjusted_points = 18.6 * 1.0 = 18.6

Gain: 0 points
```

**Example 3: Poor Team QB**
```python
# Will Levis (TEN, rank 32 offense)
base_points = 15.0
final_multiplier = 0.9925
adjusted_points = 15.0 * 0.9925 = 14.89

Loss: -0.11 points
```

**Example 4: Elite Team DST**
```python
# Pittsburgh Steelers DST (rank 2 defense)
base_points = 10.0
final_multiplier = 1.015
adjusted_points = 10.0 * 1.015 = 10.15

Gain: +0.15 points
```

---

## Important Notes

### What This Adjustment IS

✅ **Team Quality Indicator**
- Measures how good the player's team is overall
- Based on season-long offensive/defensive performance
- Elite teams get small boost, poor teams get small penalty

✅ **Conservative Adjustment**
- Maximum impact: ±1.5% (±0.3 points on 20-point projection)
- Designed as "tiebreaker" not primary factor
- Won't override obvious better projections

✅ **Position-Specific**
- Offensive positions use offensive rank
- Defensive positions use defensive rank
- Kickers use offensive rank (field goal opportunities)

---

### What This Adjustment IS NOT

❌ **NOT Opponent-Based**
- Does NOT look at opponent's defensive rank
- Does NOT consider this week's specific matchup
- The `opponent` field in teams.csv is stored but unused

❌ **NOT Weekly Matchup Analysis**
- Same adjustment every week (unless teams.csv updated)
- Doesn't account for "Lions vs weak defense this week"
- Doesn't change based on opponent's injuries/performance

❌ **NOT Dominant Factor**
- Only ±1.5% impact max
- Weekly projection variance (15-25 points) dwarfs this
- Injury/bye penalties (50-1000) completely override this

---

## Real-World Example Comparison

### Scenario: Week 5 QB Decision

**Option A: Jared Goff (DET, Elite Offense)**
```python
Position: QB
Team: DET
Offensive Rank: 1 (Elite)
Week 5 Projection: 20.0
Injury Status: ACTIVE
Bye Week: 9 (not this week)

Calculation:
- Start: 20.0
- Injury: 20.0 - 0 = 20.0
- Bye: 20.0 - 0 = 20.0
- Positional Ranking: 20.0 * 1.015 = 20.3

Final Score: 20.3 points
```

**Option B: Patrick Mahomes (KC, Average Offense)**
```python
Position: QB
Team: KC
Offensive Rank: 14 (Average)
Week 5 Projection: 18.6
Injury Status: ACTIVE
Bye Week: 6 (not this week)

Calculation:
- Start: 18.6
- Injury: 18.6 - 0 = 18.6
- Bye: 18.6 - 0 = 18.6
- Positional Ranking: 18.6 * 1.0 = 18.6

Final Score: 18.6 points
```

**Decision:**
- Goff: 20.3 points (20.0 + 1.5% boost)
- Mahomes: 18.6 points (no adjustment)
- Difference: 1.7 points

**Breakdown:**
- 1.4 points from better projection (20.0 vs 18.6)
- 0.3 points from positional ranking (1.5% boost vs 0%)

**Key Insight:** The projection difference (1.4) is much larger than the ranking adjustment (0.3). The adjustment acts as a tiebreaker, not a game-changer.

---

## Configuration and Tuning

### Where to Configure

**File:** `shared_files/positional_ranking_calculator.py`

**Default Config:**
```python
def _get_default_config(self) -> Dict:
    return {
        # Tier thresholds
        "excellent_threshold": 5,     # Rank 1-5
        "good_threshold": 12,         # Rank 6-12
        "poor_threshold": 25,         # Rank 25-32

        # Base multipliers
        "excellent_matchup": 1.1,     # +10% before weight
        "good_matchup": 1.05,          # +5% before weight
        "neutral_matchup": 1.0,
        "bad_matchup": 0.95,           # -5% before weight
        "terrible_matchup": 0.9,      # -10% (unused)

        # Weight factor
        "adjustment_weight": 0.15,     # 15% of base multiplier

        # Control
        "enable_adjustments": True,
        "log_adjustments": True
    }
```

---

### Tuning Options

#### Option 1: Increase Impact (More Weight)

**Current:**
```python
"adjustment_weight": 0.15  # ±1.5% max
```

**More Aggressive:**
```python
"adjustment_weight": 0.25  # ±2.5% max
# Elite: +2.5%, Poor: -1.25%
```

**More Conservative:**
```python
"adjustment_weight": 0.10  # ±1.0% max
# Elite: +1.0%, Poor: -0.5%
```

---

#### Option 2: Adjust Thresholds

**Current Tiers:**
```python
Elite:   1-5   (5 teams)
Good:    6-12  (7 teams)
Average: 13-24 (12 teams)
Poor:    25-32 (8 teams)
```

**More Exclusive Elite:**
```python
"excellent_threshold": 3,   # Only top 3
"good_threshold": 10,
"poor_threshold": 27,
# Elite: 1-3, Good: 4-10, Average: 11-26, Poor: 27-32
```

**More Forgiving:**
```python
"excellent_threshold": 8,   # Top 8 (top 25%)
"good_threshold": 16,       # Top half
"poor_threshold": 24,
# Elite: 1-8, Good: 9-16, Average: 17-23, Poor: 24-32
```

---

#### Option 3: Change Base Multipliers

**Current:**
```python
"excellent_matchup": 1.1,   # +10%
"good_matchup": 1.05,        # +5%
"bad_matchup": 0.95,         # -5%
```

**More Dramatic:**
```python
"excellent_matchup": 1.15,   # +15%
"good_matchup": 1.08,         # +8%
"bad_matchup": 0.92,          # -8%
# With 15% weight: Elite +2.25%, Poor -1.2%
```

**Flatter:**
```python
"excellent_matchup": 1.05,   # +5%
"good_matchup": 1.03,         # +3%
"bad_matchup": 0.97,          # -3%
# With 15% weight: Elite +0.75%, Poor -0.45%
```

---

#### Option 4: Disable Completely

**Turn Off:**
```python
"enable_adjustments": False
```

**Result:** No positional ranking adjustments applied at all.

---

## Data Management

### Updating teams.csv

**When to Update:**
- Weekly (if you want fresh team rankings)
- Mid-season (if team performance shifts dramatically)
- Never (if you want consistency throughout season)

**Where Rankings Come From:**
- **Manual:** You assign ranks based on your judgment
- **ESPN API:** Could fetch from ESPN's team rankings (not currently implemented)
- **Stats:** Could calculate from offensive/defensive yards/points (not currently implemented)

**Current State:**
The `teams.csv` file appears to be manually maintained with static rankings.

**Example Update:**
```csv
# Before Week 5
KC,14,16,BAL

# After Week 5 (KC offense looks better)
KC,10,16,BAL  # Moved from rank 14 → 10
```

---

### Opponent Field (Currently Unused)

**Current teams.csv includes opponent:**
```csv
team,offensive_rank,defensive_rank,opponent
KC,14,16,BAL
```

**The opponent field is:**
- ✅ Stored in the CSV
- ✅ Loaded into TeamData objects
- ❌ **NOT used in calculations**

**Future Enhancement Opportunity:**
Could implement true matchup analysis:
```python
# POTENTIAL FUTURE ENHANCEMENT (not currently implemented)
def calculate_matchup_adjustment(player_team, opponent_team, position):
    player_data = team_data_cache[player_team]
    opponent_data = team_data_cache[opponent_team]

    if position in offensive_positions:
        # Compare team's offensive rank vs opponent's defensive rank
        our_rank = player_data.offensive_rank
        their_rank = opponent_data.defensive_rank

        # Good offense vs bad defense = boost
        # Bad offense vs good defense = penalty
```

This would give true weekly matchup awareness.

---

## Summary

### How the Multiplier is Determined

1. **Position** → Determines offensive or defensive rank to use
2. **Team** → Look up rank in teams.csv
3. **Rank** → Map to tier (Elite/Good/Average/Poor)
4. **Tier** → Get base multiplier (0.95 - 1.10)
5. **Weight** → Apply 15% weight factor (final: 0.9925 - 1.015)
6. **Apply** → Multiply player's score by final multiplier

### Key Characteristics

- **Based on team quality**, not opponent matchup
- **Conservative impact** (±1.5% max)
- **Same every week** (unless teams.csv updated)
- **Position-aware** (offensive positions use offensive rank)
- **Tiebreaker role** (won't override projection differences)

### Configuration Summary

| Setting | Default | Range | Impact |
|---------|---------|-------|--------|
| `adjustment_weight` | 0.15 | 0.0 - 1.0 | Controls overall impact |
| `excellent_threshold` | 5 | 1 - 10 | Top tier cutoff |
| `good_threshold` | 12 | 6 - 16 | Above average cutoff |
| `poor_threshold` | 25 | 20 - 31 | Bottom tier cutoff |
| `excellent_matchup` | 1.10 | 1.0 - 1.3 | Elite team multiplier |
| `good_matchup` | 1.05 | 1.0 - 1.2 | Good team multiplier |
| `bad_matchup` | 0.95 | 0.7 - 1.0 | Poor team multiplier |

---

**End of Analysis**