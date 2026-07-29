# Step 8: Draft Order Bonus

Draft Order Bonus adds position-specific points based on optimal draft strategy for the current round.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 8 |
| Type | Additive Bonus |
| Bonus Range | 0 to +88 points |
| Data Source | `league_config.json` → `DRAFT_ORDER` |

## Purpose

Different positions have different value at different draft rounds:
- **Round 1-2**: RB/WR typically best value
- **Round 3-4**: QB/TE often optimal
- **Round 8+**: K/DST become relevant

This guides optimal draft strategy by boosting positions appropriate for each round.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ✅ | Guides optimal draft picks by round |
| Starter Helper | ❌ | Already drafted, not applicable |
| Trade Simulator | ❌ | Already drafted, not applicable |

## Calculation

### Bonus Lookup

```python
def get_draft_order_bonus(position: str, draft_round: int) -> Tuple[float, str]:
    # Look up position in DRAFT_ORDER[round]
    bonus_type = DRAFT_ORDER[draft_round].get(position, "")

    if bonus_type == "P":
        return (PRIMARY_BONUS, "PRIMARY")
    elif bonus_type == "S":
        return (SECONDARY_BONUS, "SECONDARY")
    else:
        return (0, "")
```

### Bonus Types

| Type | Typical Value | Description |
|------|---------------|-------------|
| PRIMARY | 72.81 pts | Top priority position for round |
| SECONDARY | 80.47 pts | Secondary priority position |
| None | 0 pts | Position not prioritized this round |

### Example Draft Order Configuration

```json
{
  "DRAFT_ORDER": [
    {"FLEX": "P", "QB": "S"},    // Round 0 - FLEX primary
    {"FLEX": "P", "QB": "S"},    // Round 1
    {"FLEX": "P", "QB": "S"},    // Round 2
    {"FLEX": "P", "QB": "S"},    // Round 3
    {"QB": "P", "FLEX": "S"},    // Round 4 - QB becomes primary
    {"TE": "P", "FLEX": "S"},    // Round 5 - TE primary
    {"FLEX": "P"},               // Round 6
    {"QB": "P", "FLEX": "S"},    // Round 7
    {"TE": "P", "FLEX": "S"},    // Round 8
    {"FLEX": "P"},               // Round 9
    {"FLEX": "P"},               // Round 10
    {"K": "P", "FLEX": "S"},     // Round 11 - K primary
    {"DST": "P", "FLEX": "S"},   // Round 12 - DST primary
    {"FLEX": "P"},               // Round 13
    {"FLEX": "P"}                // Round 14
  ]
}
```

Note: a round's **natively named position wins**. A position is looked up under its own name first (so a round naming `RB` or `WR` awards that round's bonus directly), and only falls back to the `"FLEX"` key when the position is FLEX-eligible *and* the round names `FLEX`. The shipped `FLEX_ELIGIBLE_POSITIONS` is `["RB", "WR"]`. The actual configuration values may vary based on simulation optimization results.

### Example Calculation

**Round 3, QB** (using example config above):
- Lookup: DRAFT_ORDER[3]["QB"] = "S"
- Bonus type: SECONDARY
- Bonus: +80.47 pts
- If previous score = 166: Final = 166 + 80.47 = 246.47

**Round 4, QB**:
- Lookup: DRAFT_ORDER[4]["QB"] = "P"
- Bonus type: PRIMARY
- Bonus: +72.81 pts

Note: SECONDARY bonus (80.47) is intentionally higher than PRIMARY (72.81) in the optimized configuration to fine-tune draft strategy recommendations.

## Data Sources

### Configuration

**Source**: `data/league_config.json`

| Key | Description |
|-----|-------------|
| `DRAFT_ORDER_BONUSES.PRIMARY` | Primary position bonus value |
| `DRAFT_ORDER_BONUSES.SECONDARY` | Secondary position bonus value |
| `DRAFT_ORDER` | Array of round-specific position priorities |
| `FLEX_ELIGIBLE_POSITIONS` | Positions that map to FLEX slot |

### FLEX Handling

The native position name is matched **first**. A FLEX-eligible position falls back to the `"FLEX"` key only when the round does not name that position natively:

```python
# 1. Native name wins - a round naming "RB" awards the bonus to an RB directly.
if position in DRAFT_ORDER[round]:
    return get_bonus_for_type(DRAFT_ORDER[round][position])

# 2. FLEX fallback - only for FLEX-eligible positions, and only if the round names FLEX.
if position in FLEX_ELIGIBLE_POSITIONS and "FLEX" in DRAFT_ORDER[round]:
    return get_bonus_for_type(DRAFT_ORDER[round]["FLEX"])

# 3. Otherwise no bonus.
return 0, ""
```

A position that is **not** FLEX-eligible never matches a `"FLEX"` key. So in a round `{"WR": "P", "FLEX": "S"}`: a WR takes PRIMARY natively, an RB takes SECONDARY via FLEX, and a TE takes no bonus at all.

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_draft_order_bonus()` (lines 577-591)

```python
def _apply_draft_order_bonus(self, p: FantasyPlayer, draft_round: int, player_score: float) -> Tuple[float, str]:
    bonus, bonus_type = self.config.get_draft_order_bonus(p.position, draft_round)

    reason = ""
    if bonus_type != "":
        reason = f"Draft Order Bonus: {bonus_type} ({bonus:+.1f} pts)"

    return player_score + bonus, reason
```

### ConfigManager Method

**File**: `league_helper/util/ConfigManager.py`

**Method**: `get_draft_order_bonus()` (lines 364-411)

```python
def get_draft_order_bonus(self, position: str, draft_round: int) -> Tuple[float, str]:
    if draft_round >= len(self.draft_order):
        draft_round = len(self.draft_order) - 1  # Use last round config

    round_priorities = self.draft_order[draft_round]

    # Check direct position match
    if position in round_priorities:
        bonus_type = round_priorities[position]
        if bonus_type == "P":
            return (self.draft_order_bonuses['PRIMARY'], "PRIMARY")
        elif bonus_type == "S":
            return (self.draft_order_bonuses['SECONDARY'], "SECONDARY")

    # Check FLEX eligibility
    if position in self.flex_eligible_positions:
        if 'FLEX' in round_priorities:
            # ... similar logic for FLEX

    return (0, "")
```

## Configuration

**league_config.json**:
```json
{
  "DRAFT_ORDER_BONUSES": {
    "PRIMARY": 72.81,
    "SECONDARY": 80.47
  },
  "DRAFT_ORDER": [
    {"RB": "P", "WR": "P"},
    ...
  ],
  "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "TE"]
}
```

## Real Player Example

**Travis Kelce (TE, KC)** - Round 3:

| Metric | Value |
|--------|-------|
| Position | TE |
| Draft Round | 3 |
| Round 3 Config | {"QB": "P", "TE": "P", "WR": "S"} |
| TE Priority | "P" (PRIMARY) |
| Previous Score | 166.36 |
| Bonus | +72.81 pts |
| Adjusted Score | 239.17 |

**Reason String**: `"Draft Order Bonus: PRIMARY (+72.8 pts)"`

## Edge Cases

### Round Beyond Configuration

If draft_round > configured rounds:
- Uses last round's configuration
- Prevents index out of bounds

### Position Not Listed

If position not in round's priorities:
- Returns (0, "") - no bonus
- Common for K/DST in early rounds

### Round -1 (Disabled)

When `draft_round=-1`:
- Bonus step is skipped entirely
- Used by all non-draft modes

## Relationship to Other Steps

- **Input**: Schedule-adjusted score from Step 7
- **Output**: Draft bonus-adjusted score
- **Next Step**: Bye Week penalty applied (Step 9)

Draft Order Bonus is only applied during Add To Roster mode (draft_round >= 0).

## Strategic Impact

The bonus values are substantial (70-80 pts):
- Strongly guides optimal draft strategy
- Makes "wrong position" picks appear much less valuable
- Encourages positional diversity at appropriate times
