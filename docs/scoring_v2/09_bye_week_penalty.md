# Step 9: Bye Week Penalty

Bye Week Penalty reduces score based on roster conflicts during a player's bye week.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 9 |
| Type | Additive Penalty |
| Penalty Range | 0 to -50+ points |
| Scaling | Linear (median-based) |
| Data Source | `players.csv` → `bye_week`, `week_N_points` |

## Purpose

Roster bye week conflicts create gaps in weekly scoring:
- **Same-position overlap**: 2 RBs on same bye = no backup → Severe penalty
- **Different-position overlap**: RB + WR on same bye = weaker roster → Moderate penalty

Penalty discourages stacking bye weeks during draft.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ✅ | Evaluate roster fit during draft |
| Starter Helper | ❌ | Handled by roster constraints |
| Trade Simulator (User) | ✅ | Post-trade roster conflicts matter |
| Trade Simulator (Opponent) | ❌ | Don't penalize opponent comparison |

## Calculation

### Penalty Formula

```python
# Collect bye week conflicts
same_pos_players = [p for p in roster if p.position == player.position and p.bye == player.bye]
diff_pos_players = [p for p in roster if p.position != player.position and p.bye == player.bye]

# Calculate median weekly scores for each player
same_total = sum(median(p.week_1..week_17) for p in same_pos_players)
diff_total = sum(median(p.week_1..week_17) for p in diff_pos_players)

# Apply linear scaling
penalty = (same_total * SAME_POS_BYE_WEIGHT) + (diff_total * DIFF_POS_BYE_WEIGHT)
```

### Weight Parameters

| Weight | Typical Value | Purpose |
|--------|---------------|---------|
| `SAME_POS_BYE_WEIGHT` | 0.403 | Linear scale for same-position conflicts |
| `DIFF_POS_BYE_WEIGHT` | 0.176 | Linear scale for different-position conflicts |

### Why These Weights?

The weights control penalty severity:
- **Same-position weight (0.403)**: Higher because losing same-position depth is more critical
- **Different-position weight (0.176)**: Lower because roster depth is less affected
- **Linear scaling**: Penalty grows proportionally with player quality (median points)

### Example Calculation

**WR added to roster with existing bye week 10 conflicts**:

**Same position (1 WR on roster with bye 10)**:
- WR1 median weekly: 12.5 pts
- Same total: 12.5
- Same penalty: 12.5 × 0.403 = 5.04

**Different position (2 other players with bye 10)**:
- RB median: 11.0 pts
- TE median: 8.5 pts
- Diff total: 19.5
- Diff penalty: 19.5 × 0.176 = 3.43

**Total penalty**: 5.04 + 3.43 = 8.47 pts

## Data Sources

### Player Bye Week

**Source**: `players.csv` → `bye_week` column

| Column | Description | Example |
|--------|-------------|---------|
| `bye_week` | NFL bye week number | 10 |

### Weekly Projections for Median

**Source**: `players.csv` → `week_1_points` through `week_17_points`

Used to calculate median weekly value for each conflicting player.

### ESPN API Source

Bye week is determined from team schedule data:

```python
# In espn_client.py
bye_weeks = {}
for team in teams:
    bye_week = team_schedule.find_bye_week(team)
    bye_weeks[team] = bye_week

player.bye_week = bye_weeks[player.team]
```

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_bye_week_penalty()` (lines 593-651)

```python
def _apply_bye_week_penalty(self, p: FantasyPlayer, player_score: float, roster: List[FantasyPlayer]) -> Tuple[float, str]:
    # Skip if bye week is None or already passed
    if p.bye_week is None or p.bye_week < self.config.current_nfl_week:
        return player_score, "Bye week has passed"

    same_pos_players = []
    diff_pos_players = []

    for roster_player in roster:
        if roster_player.id == p.id:
            continue
        if roster_player.bye_week == p.bye_week:
            if roster_player.position == p.position:
                same_pos_players.append(roster_player)
            else:
                diff_pos_players.append(roster_player)

    penalty = self.config.get_bye_week_penalty(same_pos_players, diff_pos_players)

    if len(same_pos_players) == 0 and len(diff_pos_players) == 0:
        reason = ""
    else:
        reason = f"Bye Overlaps: {len(same_pos_players)} same-position, {len(diff_pos_players)} different-position ({-penalty:.1f} pts)"

    return player_score - penalty, reason
```

### ConfigManager Method

**File**: `league_helper/util/ConfigManager.py`

**Method**: `get_bye_week_penalty()` (lines 413-493)

```python
def get_bye_week_penalty(self, same_pos_players: List, diff_pos_players: List) -> float:
    # Calculate median for each player
    def get_median_weekly(player):
        weekly_pts = [getattr(player, f'week_{w}_points', 0) or 0 for w in range(1, 18)]
        weekly_pts = [p for p in weekly_pts if p > 0]
        return statistics.median(weekly_pts) if weekly_pts else 0

    same_total = sum(get_median_weekly(p) for p in same_pos_players)
    diff_total = sum(get_median_weekly(p) for p in diff_pos_players)

    # Apply linear scaling (multiplication, not exponentiation)
    same_penalty = same_total * self.same_pos_bye_weight
    diff_penalty = diff_total * self.diff_pos_bye_weight

    return same_penalty + diff_penalty
```

## Configuration

**league_config.json**:
```json
{
  "SAME_POS_BYE_WEIGHT": 0.403,
  "DIFF_POS_BYE_WEIGHT": 0.176
}
```

## Real Player Example

**Adding DeVonta Smith (WR, PHI)** - Bye week 5:

Existing roster bye week 5 conflicts:
- A.J. Brown (WR, PHI) - median 15.2 pts
- Dallas Goedert (TE, PHI) - median 9.8 pts

| Metric | Value |
|--------|-------|
| Same-position conflicts | 1 (A.J. Brown) |
| Different-position conflicts | 1 (Goedert) |
| Same total | 15.2 |
| Same penalty | 15.2 × 0.403 = 6.13 |
| Diff total | 9.8 |
| Diff penalty | 9.8 × 0.176 = 1.72 |
| Total Penalty | 7.85 pts |
| Previous Score | 239.17 |
| Adjusted Score | 231.32 |

**Reason String**: `"Bye Overlaps: 1 same-position, 1 different-position (-7.9 pts)"`

## Edge Cases

### No Conflicts

If no roster players share bye week:
- Penalty = 0
- Empty reason string returned

### Bye Week Already Passed

If `bye_week < current_nfl_week`:
- Returns "Bye week has passed"
- No penalty applied

### None Bye Week

Some players may have `None` bye week:
- Returns "No bye week information"
- No penalty applied

### Custom Roster

Trade Simulator passes `roster` parameter to evaluate post-trade conflicts:
```python
scored_player = player_manager.score_player(p, ..., roster=post_trade_roster)
```

## Relationship to Other Steps

- **Input**: Draft bonus-adjusted score from Step 8
- **Output**: Bye penalty-adjusted score
- **Next Step**: Injury penalty applied (Step 10)

Bye Week Penalty helps diversify roster bye weeks during draft and trade evaluation.

## Penalty Magnitude

With typical weights (0.403, 0.176) and median-based linear scaling:
- **1 same-position conflict** (median 12 pts): 12 × 0.403 = ~4.8 pts penalty
- **2 same-position conflicts** (total median 24 pts): 24 × 0.403 = ~9.7 pts penalty
- **3 different-position conflicts** (total median 30 pts): 30 × 0.176 = ~5.3 pts penalty

The penalties scale linearly with player quality - losing high-value players hurts more.
