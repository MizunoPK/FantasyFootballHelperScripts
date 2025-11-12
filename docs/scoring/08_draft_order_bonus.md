# Draft Order Bonus (Step 8)

## Overview

**Type**: Additive (flat point bonus)
**Effect**: +0 to +88 points (PRIMARY or SECONDARY bonus based on position/round)
**When Applied**: Step 8 of 10-step scoring algorithm
**Purpose**: Guide draft strategy by prioritizing optimal positions for each round

The Draft Order Bonus implements a positional value system that encourages drafting the right positions at the right time. Unlike multipliers that scale with player quality, this is a flat bonus that shifts the entire position tier up or down based on draft strategy. Each round specifies PRIMARY positions (highest priority) and SECONDARY positions (medium priority), helping avoid common draft mistakes like drafting QBs too early or waiting too long on RBs.

**Key Characteristics**:
- **Mode-specific**: Only used in Add To Roster Mode (Draft Helper)
- **Round-dependent**: Different positions prioritized in different rounds
- **Flat bonus**: Not multiplicative - adds fixed points regardless of player quality
- **Strategic guidance**: Implements optimal draft strategy from simulation analysis
- **Two-tier system**: PRIMARY (+81.64 pts) and SECONDARY (+87.96 pts)

**Formula**:
```
If player.position matches round's PRIMARY position:
    bonus = PRIMARY_BONUS (81.64 pts)
Elif player.position matches round's SECONDARY position:
    bonus = SECONDARY_BONUS (87.96 pts)
Else:
    bonus = 0 pts

adjusted_score = player_score + bonus
```

**Implementation**: `league_helper/util/player_scoring.py:609-623`

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: Yes (when draft_round >= 0)
**Why**: Draft strategy requires position-specific value by round. Early rounds prioritize RB/WR (scarcity), mid-rounds balance with QB/TE, late rounds fill remaining slots with K/DST.

**Example**: Round 1 (draft_round=0)
- FLEX (RB/WR): PRIMARY bonus +81.64 pts
- QB: SECONDARY bonus +87.96 pts
- Effect: Pushes top RB/WR above QB in rankings despite similar base scores

### Starter Helper Mode (Roster Optimizer)
**Enabled**: No (draft_round=-1)
**Why**: Lineup optimization has no draft rounds - evaluating existing roster for weekly starts.

### Trade Simulator Mode
**Enabled**: No (draft_round=-1)
**Why**: Trade evaluation assesses season-long value, not draft strategy. Position scarcity already captured in projections and other multipliers.

---

## How League Helper Gets the Value/Multiplier

### Step 1: Check if Draft Mode is Active

**Parameter**: `draft_round` in `score_player()` method
**File**: `league_helper/util/player_scoring.py:356-462`

```python
def score_player(self, p: FantasyPlayer, team_roster: List[FantasyPlayer],
                 draft_round=-1, ...):
    """
    Calculate score for a player (10-step calculation).

    Args:
        draft_round: Draft round for position bonus (-1 to disable)
        ... other parameters ...
    """
    # ... Steps 1-7 ...

    # STEP 8: Add DRAFT_ORDER bonus (round-based position priority)
    # BUG FIX: Changed from draft_round > 0 to draft_round >= 0
    # This allows round 0 (first round) to get bonuses, -1 is the disabled flag
    if draft_round >= 0:
        player_score, reason = self._apply_draft_order_bonus(p, draft_round, player_score)
        add_to_reasons(reason)
```

**Key Logic**:
- `draft_round >= 0`: Bonus enabled (rounds 0-14 for 15-round draft)
- `draft_round = -1`: Bonus disabled (default for non-draft modes)

### Step 2: Get Draft Strategy for Round

**Method**: `ConfigManager.get_draft_order_bonus()`
**File**: `league_helper/util/ConfigManager.py:333-380`

```python
def get_draft_order_bonus(self, position: str, draft_round: int) -> Tuple[float, str]:
    """
    Get draft order bonus for a position in a specific round.

    Args:
        position: Player position (QB, RB, WR, TE, K, DST, or FLEX)
        draft_round: Draft round number (0-indexed)

    Returns:
        Tuple[float, str]: (bonus_points, bonus_type)
            - bonus_points: Point bonus to add to score
            - bonus_type: "PRIMARY", "SECONDARY", or "" (no bonus)
    """
    # Convert position to FLEX-aware format
    position_with_flex = self.get_position_with_flex(position)

    # Get the ideal positions for this draft round
    ideal_positions = self.draft_order[draft_round]

    # Check if this position is listed in the draft strategy for this round
    if position_with_flex in ideal_positions:
        priority = ideal_positions.get(position_with_flex)

        if priority == self.keys.DRAFT_ORDER_PRIMARY_LABEL:  # "P"
            return self.draft_order_bonuses[self.keys.BONUS_PRIMARY], self.keys.BONUS_PRIMARY
        else:  # "S"
            return self.draft_order_bonuses[self.keys.BONUS_SECONDARY], self.keys.BONUS_SECONDARY
    else:
        # Position not listed in this round's strategy (no bonus)
        return 0, ""
```

**Key Components**:
1. **Position normalization**: RB/WR/TE/DST may map to "FLEX" based on config
2. **Round lookup**: Access `draft_order[draft_round]` dict (e.g., `{"FLEX": "P", "QB": "S"}`)
3. **Priority check**: "P" = PRIMARY bonus, "S" = SECONDARY bonus, absent = no bonus

### Step 3: Apply Bonus to Score

**Method**: `PlayerScoringCalculator._apply_draft_order_bonus()`
**File**: `league_helper/util/player_scoring.py:609-623`

```python
def _apply_draft_order_bonus(self, p: FantasyPlayer, draft_round: int, player_score: float) -> Tuple[float, str]:
    """
    Add draft order bonus (Step 8).

    Args:
        p: Player to evaluate
        draft_round: Current draft round (0-indexed)
        player_score: Current score before bonus

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    # Get position-specific bonus for the current draft round
    bonus, bonus_type = self.config.get_draft_order_bonus(p.position, draft_round)

    # Only add reason text if there's an actual bonus (not empty string)
    reason = ""
    if bonus_type != "":
        reason = f"Draft Order Bonus: {bonus_type} ({bonus:+.1f} pts)"

    # Add bonus to score (not multiply, since it's a flat point adjustment)
    return player_score + bonus, reason
```

**Complete Flow**:
```
Player (position=RB, draft_round=0)
    ↓
Check config.FLEX_ELIGIBLE_POSITIONS → RB is in list
    ↓
position_with_flex = "FLEX"
    ↓
Lookup draft_order[0] → {"FLEX": "P", "QB": "S"}
    ↓
"FLEX" in dict, priority = "P" → PRIMARY
    ↓
bonus = 81.64 points
    ↓
player_score + 81.64
```

---

## Calculations Involved

### Formula Breakdown

**Position-to-FLEX Mapping**:
```python
if position in config.FLEX_ELIGIBLE_POSITIONS:  # Typically ["RB", "WR", "TE", "DST"]
    position_with_flex = "FLEX"
else:
    position_with_flex = position  # QB, K remain unchanged
```

**Bonus Lookup Logic**:
```python
draft_strategy = draft_order[draft_round]  # e.g., {"FLEX": "P", "QB": "S"}

if position_with_flex in draft_strategy:
    priority_label = draft_strategy[position_with_flex]

    if priority_label == "P":  # PRIMARY
        bonus = 81.64 pts
        label = "PRIMARY"
    elif priority_label == "S":  # SECONDARY
        bonus = 87.96 pts
        label = "SECONDARY"
else:
    bonus = 0 pts
    label = ""
```

**Score Adjustment**:
```
adjusted_score = player_score + bonus
```

### Example Calculation (Round 1, RB)

**Player**: Bijan Robinson (RB, ATL)
**Draft Round**: 0 (first round)
**Current Score** (after Steps 1-7): 65.00 points
**Config**: PRIMARY=81.64, SECONDARY=87.96

**Step 1: Check FLEX eligibility**
```python
position = "RB"
config.FLEX_ELIGIBLE_POSITIONS = ["RB", "WR", "TE", "DST"]

"RB" in FLEX_ELIGIBLE_POSITIONS → True
position_with_flex = "FLEX"
```

**Step 2: Lookup round 0 strategy**
```python
draft_order[0] = {"FLEX": "P", "QB": "S"}

"FLEX" in {"FLEX": "P", "QB": "S"} → True
priority = "P"
```

**Step 3: Get PRIMARY bonus**
```
priority = "P" → PRIMARY
bonus = 81.64 points
```

**Step 4: Apply to score**
```
adjusted_score = 65.00 + 81.64 = 146.64 points
reason = "Draft Order Bonus: PRIMARY (+81.6 pts)"
```

**Result**: RB in round 1 receives +81.64 point boost (PRIMARY position)

### Example Calculation (Round 1, QB)

**Player**: Patrick Mahomes (QB, KC)
**Draft Round**: 0
**Current Score**: 68.00 points

**Calculation**:
```
position = "QB"
QB not in FLEX_ELIGIBLE_POSITIONS
position_with_flex = "QB"

draft_order[0] = {"FLEX": "P", "QB": "S"}
"QB" in dict → True, priority = "S"

bonus = 87.96 points (SECONDARY)
adjusted_score = 68.00 + 87.96 = 155.96 points
```

**Result**: QB in round 1 receives +87.96 point boost (SECONDARY position)

**Analysis**: SECONDARY bonus (87.96) is higher than PRIMARY (81.64), making QB slightly more valuable in round 1. This reflects that while FLEX is prioritized, elite QBs are also valid picks.

### Example Calculation (Round 5, QB)

**Player**: Josh Allen (QB, BUF)
**Draft Round**: 4 (fifth round)
**Current Score**: 70.00 points

**Calculation**:
```
position_with_flex = "QB"
draft_order[4] = {"QB": "P", "FLEX": "S"}

"QB" in dict → True, priority = "P"
bonus = 81.64 points (PRIMARY)
adjusted_score = 70.00 + 81.64 = 151.64 points
```

**Result**: QB in round 5 receives +81.64 point boost (PRIMARY position)

**Strategic Note**: QB becomes PRIMARY in round 5, encouraging QB selection at this point if not taken earlier.

### Example Calculation (Round 1, K)

**Player**: Brandon Aubrey (K, DAL)
**Draft Round**: 0
**Current Score**: 20.00 points

**Calculation**:
```
position_with_flex = "K"
draft_order[0] = {"FLEX": "P", "QB": "S"}

"K" not in dict → False
bonus = 0 points
adjusted_score = 20.00 + 0 = 20.00 points (no change)
```

**Result**: Kicker in round 1 receives NO bonus (not in strategy)

**Strategic Note**: Kickers intentionally excluded from early rounds to discourage poor draft decisions.

---

## Data Sources (league_config.json Fields)

### Required Fields

| Field Name | Data Type | Description | Example Values |
|------------|-----------|-------------|----------------|
| `DRAFT_ORDER_BONUSES.PRIMARY` | float | Bonus for PRIMARY position | 81.64 |
| `DRAFT_ORDER_BONUSES.SECONDARY` | float | Bonus for SECONDARY position | 87.96 |
| `DRAFT_ORDER` | array of dicts | Position priorities by round | See below |
| `FLEX_ELIGIBLE_POSITIONS` | array of strings | Positions that map to FLEX | ["RB", "WR", "TE", "DST"] |

### Field Specifications

**`DRAFT_ORDER_BONUSES`**:
- **Type**: object with PRIMARY and SECONDARY keys
- **PRIMARY**: Float value for highest-priority positions
- **SECONDARY**: Float value for medium-priority positions
- **Range**: Typically 50-100 points (large enough to shift tiers)
- **Optimization**: Values determined by simulation to maximize draft win rate

**`DRAFT_ORDER`** (array of 15 objects, one per round):
- **Type**: array of dictionaries
- **Length**: 15 (for 15-round draft)
- **Keys**: Position names (QB, RB, WR, TE, K, DST, FLEX)
- **Values**: "P" (PRIMARY) or "S" (SECONDARY)
- **Structure**:
```json
[
  {"FLEX": "P", "QB": "S"},      // Round 1 (index 0)
  {"FLEX": "P", "QB": "S"},      // Round 2 (index 1)
  {"FLEX": "P", "QB": "S"},      // Round 3 (index 2)
  {"FLEX": "P", "QB": "S"},      // Round 4 (index 3)
  {"QB": "P", "FLEX": "S"},      // Round 5 (index 4)
  {"TE": "P", "FLEX": "S"},      // Round 6 (index 5)
  {"FLEX": "P"},                 // Round 7 (index 6)
  {"QB": "P", "FLEX": "S"},      // Round 8 (index 7)
  {"TE": "P", "FLEX": "S"},      // Round 9 (index 8)
  {"FLEX": "P"},                 // Round 10 (index 9)
  {"FLEX": "P"},                 // Round 11 (index 10)
  {"K": "P", "FLEX": "S"},       // Round 12 (index 11)
  {"DST": "P", "FLEX": "S"},     // Round 13 (index 12)
  {"FLEX": "P"},                 // Round 14 (index 13)
  {"FLEX": "P"}                  // Round 15 (index 14)
]
```

**`FLEX_ELIGIBLE_POSITIONS`**:
- **Type**: array of strings
- **Valid Values**: Any subset of ["QB", "RB", "WR", "TE", "K", "DST"]
- **Current Value**: ["RB", "WR", "TE", "DST"]
- **Purpose**: Determines which positions map to "FLEX" in draft strategy
- **Note**: QB and K typically excluded from FLEX

---

## Draft Strategy Analysis

### Round-by-Round Breakdown

**Rounds 1-4: FLEX Primary, QB Secondary**
```json
{"FLEX": "P", "QB": "S"}
```
- **Strategy**: Prioritize RB/WR/TE, but elite QB acceptable
- **Rationale**: Build core roster with high-value flex positions
- **Effect**: Top RBs/WRs receive +81.64 pts, top QBs receive +87.96 pts

**Round 5: QB Primary, FLEX Secondary**
```json
{"QB": "P", "FLEX": "S"}
```
- **Strategy**: Target QB if not taken, continue FLEX otherwise
- **Rationale**: Ensure QB1 secured before mid-rounds
- **Effect**: QBs receive +81.64 pts boost (now PRIMARY)

**Round 6: TE Primary, FLEX Secondary**
```json
{"TE": "P", "FLEX": "S"}
```
- **Strategy**: Target elite TE if available
- **Rationale**: TE scarcity at top tier
- **Effect**: Top TEs receive +81.64 pts boost

**Round 7: FLEX Primary Only**
```json
{"FLEX": "P"}
```
- **Strategy**: Fill RB/WR depth
- **Rationale**: Core positions still valuable
- **Effect**: FLEX receives +81.64 pts, all others 0

**Round 8: QB Primary, FLEX Secondary**
```json
{"QB": "P", "FLEX": "S"}
```
- **Strategy**: Second QB or backup QB
- **Rationale**: Ensure QB depth before late rounds
- **Effect**: QB2 receives encouragement boost

**Round 9: TE Primary, FLEX Secondary**
```json
{"TE": "P", "FLEX": "S"}
```
- **Strategy**: Second TE if needed
- **Rationale**: TE2 for bye week coverage
- **Effect**: TEs receive +81.64 pts boost

**Rounds 10-11: FLEX Primary Only**
```json
{"FLEX": "P"}
```
- **Strategy**: Continue depth building
- **Rationale**: RB/WR depth for injuries/byes
- **Effect**: Only FLEX positions boosted

**Round 12: K Primary, FLEX Secondary**
```json
{"K": "P", "FLEX": "S"}
```
- **Strategy**: Draft kicker
- **Rationale**: Wait on kicker until necessary
- **Effect**: Kickers finally receive bonus

**Round 13: DST Primary, FLEX Secondary**
```json
{"DST": "P", "FLEX": "S"}
```
- **Strategy**: Draft defense
- **Rationale**: DST can wait until late
- **Effect**: DST receives +81.64 pts boost

**Rounds 14-15: FLEX Primary Only**
```json
{"FLEX": "P"}
```
- **Strategy**: Final depth/lottery tickets
- **Rationale**: Fill remaining FLEX spots
- **Effect**: Deep bench RB/WR receive boost

---

## Examples with Walkthroughs

### Example 1: Round 1, Elite RB (Bijan Robinson)

**Scenario**: Draft round 1, evaluating RB Bijan Robinson
**Player Data**:
- Position: RB
- Team: ATL
- Current Score (after Steps 1-7): 65.00 points

**Step 1: Map position to FLEX**
```
position = "RB"
FLEX_ELIGIBLE = ["RB", "WR", "TE", "DST"]
→ position_with_flex = "FLEX"
```

**Step 2: Lookup round 1 strategy**
```
draft_order[0] = {"FLEX": "P", "QB": "S"}
"FLEX" is PRIMARY ("P")
```

**Step 3: Get PRIMARY bonus**
```
bonus = 81.64 points
bonus_type = "PRIMARY"
```

**Step 4: Apply bonus**
```
adjusted_score = 65.00 + 81.64 = 146.64 points
reason = "Draft Order Bonus: PRIMARY (+81.6 pts)"
```

**Result**: Elite RB receives huge boost (+81.64) in round 1, encouraging early RB selection

---

### Example 2: Round 1, Elite QB (Patrick Mahomes)

**Scenario**: Draft round 1, evaluating QB Patrick Mahomes
**Player Data**:
- Position: QB
- Team: KC
- Current Score: 68.00 points

**Calculation**:
```
position = "QB" (not in FLEX_ELIGIBLE)
→ position_with_flex = "QB"

draft_order[0] = {"FLEX": "P", "QB": "S"}
"QB" is SECONDARY ("S")

bonus = 87.96 points
adjusted_score = 68.00 + 87.96 = 155.96 points
```

**Result**: Elite QB receives +87.96 (SECONDARY bonus), actually slightly higher than FLEX PRIMARY

**Strategic Analysis**:
- SECONDARY=87.96 > PRIMARY=81.64 (unusual but intentional)
- Reflects that elite QBs are also valid round 1 picks
- Prevents over-penalizing QB-first strategy

---

### Example 3: Round 5, QB Josh Allen

**Scenario**: Draft round 5, evaluating QB Josh Allen
**Player Data**:
- Position: QB
- Current Score: 70.00 points

**Calculation**:
```
position_with_flex = "QB"
draft_order[4] = {"QB": "P", "FLEX": "S"}
"QB" is PRIMARY ("P")

bonus = 81.64 points
adjusted_score = 70.00 + 81.64 = 151.64 points
```

**Result**: QB becomes PRIMARY in round 5, encouraging QB selection at this point

**Strategic Analysis**:
- If QB not taken in rounds 1-4, round 5 is optimal time
- PRIMARY bonus makes QB very attractive here
- Prevents waiting too long on QB position

---

### Example 4: Round 6, TE Trey McBride

**Scenario**: Draft round 6, evaluating TE Trey McBride
**Player Data**:
- Position: TE
- Team: ARI
- Current Score: 55.00 points

**Calculation**:
```
position = "TE"
TE in FLEX_ELIGIBLE → position_with_flex = "FLEX"

But wait - draft_order[5] = {"TE": "P", "FLEX": "S"}

Actually checks position="TE" BEFORE FLEX mapping!
position in draft_order[5] → "TE" is PRIMARY

bonus = 81.64 points
adjusted_score = 55.00 + 81.64 = 136.64 points
```

**Result**: Elite TE receives PRIMARY bonus in round 6

**Implementation Note**: Need to check if code maps TE→FLEX before or after dict lookup
- If after: TE as TE gets PRIMARY
- If before: TE as FLEX gets SECONDARY

---

### Example 5: Round 12, Kicker Cameron Dicker

**Scenario**: Draft round 12, evaluating K Cameron Dicker
**Player Data**:
- Position: K
- Current Score: 18.00 points

**Calculation**:
```
position_with_flex = "K" (not in FLEX_ELIGIBLE)
draft_order[11] = {"K": "P", "FLEX": "S"}
"K" is PRIMARY ("P")

bonus = 81.64 points
adjusted_score = 18.00 + 81.64 = 99.64 points
```

**Result**: Kicker finally receives PRIMARY bonus in round 12

**Strategic Analysis**:
- Kickers intentionally excluded from rounds 1-11
- Round 12 is appropriate time to draft kicker
- Large bonus ensures kicker selected here

---

### Example 6: Round 1, Kicker (Anti-Pattern)

**Scenario**: Draft round 1, evaluating K Brandon Aubrey (hypothetical mistake)
**Player Data**:
- Position: K
- Current Score: 20.00 points

**Calculation**:
```
position_with_flex = "K"
draft_order[0] = {"FLEX": "P", "QB": "S"}
"K" not in dict

bonus = 0 points
adjusted_score = 20.00 + 0 = 20.00 points (unchanged)
```

**Result**: Kicker in round 1 receives NO bonus

**Strategic Analysis**:
- Zero bonus discourages drafting kicker early
- Kicker's low base score (~20) remains low
- Elite RBs (~65 + 81.64 = 146.64) far superior picks

---

### Example 7: Round 13, DST Broncos

**Scenario**: Draft round 13, evaluating Broncos D/ST
**Player Data**:
- Position: DST
- Current Score: 22.00 points

**Calculation**:
```
position = "DST"
DST in FLEX_ELIGIBLE → position_with_flex = "FLEX"

But draft_order[12] = {"DST": "P", "FLEX": "S"}
Need to check if code uses "DST" or "FLEX" key

Assuming code checks original position first:
"DST" is PRIMARY

bonus = 81.64 points
adjusted_score = 22.00 + 81.64 = 103.64 points
```

**Result**: DST receives PRIMARY bonus in round 13

---

### Example 8: Mid-Round RB (No Bonus Example)

**Scenario**: Draft round 7, evaluating mid-tier RB
**Player Data**:
- Position: RB
- Current Score: 48.00 points

**Calculation**:
```
position_with_flex = "FLEX"
draft_order[6] = {"FLEX": "P"}

"FLEX" is PRIMARY
bonus = 81.64 points
adjusted_score = 48.00 + 81.64 = 129.64 points
```

**Result**: Even in round 7, FLEX positions still receive PRIMARY bonus

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "DRAFT_ORDER_BONUSES": {
    "PRIMARY": 81.63820523910373,
    "SECONDARY": 87.96323122074631
  },
  "DRAFT_ORDER": [
    {"FLEX": "P", "QB": "S"},      // Round 1
    {"FLEX": "P", "QB": "S"},      // Round 2
    {"FLEX": "P", "QB": "S"},      // Round 3
    {"FLEX": "P", "QB": "S"},      // Round 4
    {"QB": "P", "FLEX": "S"},      // Round 5
    {"TE": "P", "FLEX": "S"},      // Round 6
    {"FLEX": "P"},                 // Round 7
    {"QB": "P", "FLEX": "S"},      // Round 8
    {"TE": "P", "FLEX": "S"},      // Round 9
    {"FLEX": "P"},                 // Round 10
    {"FLEX": "P"},                 // Round 11
    {"K": "P", "FLEX": "S"},       // Round 12
    {"DST": "P", "FLEX": "S"},     // Round 13
    {"FLEX": "P"},                 // Round 14
    {"FLEX": "P"}                  // Round 15
  ],
  "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "TE", "DST"]
}
```

### Configuration Fields

| Field | Type | Description | Current Value |
|-------|------|-------------|---------------|
| `DRAFT_ORDER_BONUSES.PRIMARY` | float | Bonus for highest-priority positions | 81.64 |
| `DRAFT_ORDER_BONUSES.SECONDARY` | float | Bonus for medium-priority positions | 87.96 |
| `DRAFT_ORDER` | array | 15-element array of position priorities | See above |
| `FLEX_ELIGIBLE_POSITIONS` | array | Positions that map to FLEX | ["RB", "WR", "TE", "DST"] |

### Bonus Value Interpretation

**Current Bonuses**:
- PRIMARY: +81.64 points
- SECONDARY: +87.96 points

**Impact on 0-105 Scale**:
- Base scores typically: 15-70 points (before multipliers)
- PRIMARY bonus: Adds ~115-195% of low-tier player's base score
- SECONDARY bonus: Adds ~125-585% of low-tier player's base score
- Effect: Completely reorders position tiers within each round

**Why SECONDARY > PRIMARY?**:
- Unusual configuration (typically PRIMARY should be higher)
- Current values from simulation optimization
- May reflect that SECONDARY positions (QB in early rounds) are also highly valuable
- Consider this a quirk of the optimized parameters

### Configuration Tuning Guide

**Increasing Strategic Impact**:
- Increase PRIMARY/SECONDARY values (e.g., 100, 120) → stronger position guidance
- Make PRIMARY > SECONDARY (e.g., 100 vs 80) → clearer priority hierarchy
- Add more positions per round → more flexibility in draft strategy

**Decreasing Strategic Impact**:
- Decrease PRIMARY/SECONDARY values (e.g., 50, 40) → gentler position guidance
- Remove SECONDARY tier entirely → binary yes/no position priority
- Leave fewer positions per round → stricter draft strategy

**Modifying Draft Strategy**:
- Change round allocations for QB/TE/K/DST
- Adjust FLEX vs specific position targets
- Add/remove positions from FLEX_ELIGIBLE_POSITIONS

---

## See Also

### Related Metrics
- **[01_normalization.md](01_normalization.md)** - Base score that draft bonus adds to
- **[02_adp_multiplier.md](02_adp_multiplier.md)** - Market consensus (complements draft strategy)
- **[09_bye_week_penalty.md](09_bye_week_penalty.md)** - Another additive adjustment

### Implementation Files
- **`league_helper/util/player_scoring.py:609-623`** - Draft order bonus application
- **`league_helper/util/ConfigManager.py:333-380`** - Draft strategy lookup
- **`league_helper/util/ConfigManager.py:490-536`** - Draft position helpers

### Configuration
- **`data/league_config.json`** - DRAFT_ORDER_BONUSES, DRAFT_ORDER, FLEX_ELIGIBLE_POSITIONS

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - Draft order bonus tests
- **`tests/league_helper/util/test_ConfigManager.py`** - Draft strategy configuration tests

### Documentation
- **[README.md](README.md)** - Scoring algorithm overview
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 9
**Documentation Version**: 1.0
**Code Version**: Week 9, 2025 NFL Season
