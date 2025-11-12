# Injury Penalty (Step 10)

## Overview

**Type**: Subtractive (flat point penalty)
**Effect**: 0 to -100 points (based on injury risk level)
**When Applied**: Step 10 of 10-step scoring algorithm (final step)
**Purpose**: Account for availability risk and reduce value of injured players

The Injury Penalty is the final adjustment in the scoring algorithm, applying a flat point reduction based on a player's injury status and associated risk level. This ensures that injured players are appropriately devalued to reflect their uncertain availability. The penalty system uses three risk levels (LOW, MEDIUM, HIGH) mapped from ESPN injury designations, with only HIGH-risk players currently penalized in the optimal configuration.

**Key Characteristics**:
- **Final step**: Applied after all multipliers and bonuses
- **Risk-based**: Uses injury status to determine risk level (LOW/MEDIUM/HIGH)
- **Subtractive**: Flat penalty deducted from score (not multiplicative)
- **Conservative approach**: Current config only penalizes HIGH-risk players (-100 pts)
- **Zero-tolerance for unavailable**: OUT/DOUBTFUL/IR players effectively removed from consideration

**Formula**:
```
risk_level = map injury_status to (LOW, MEDIUM, HIGH)
penalty = INJURY_PENALTIES[risk_level]
adjusted_score = player_score - penalty
```

**Implementation**: `league_helper/util/player_scoring.py:685-697`

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: Yes (`injury=True`)
**Why**: Drafting injured players carries substantial risk. Players who won't play early season or may miss games provide diminished value. The penalty helps avoid drafting players who are OUT, DOUBTFUL, or on IR.

**Example**: Two WRs with similar projections
- WR1: 150 ROS pts, ACTIVE → penalty = 0
- WR2: 150 ROS pts, DOUBTFUL → penalty = -100 pts
- Injury penalty makes WR1 clearly superior pick

### Starter Helper Mode (Roster Optimizer)
**Enabled**: No (`injury=False`)
**Why**: Weekly projections already account for injury status - OUT/DOUBTFUL players receive 0 or near-0 projections. Adding injury penalty would double-penalize. Disabled to avoid redundant scoring adjustments.

**Rationale**: Injury status is implicitly handled:
- OUT players: Already have 0 weekly projection (can't score if not playing)
- DOUBTFUL players: Projections already reduced to reflect low likelihood of playing
- QUESTIONABLE players: Projections already adjusted for snap count/usage uncertainty
- Injury penalty would stack on top of already-reduced projections

### Trade Simulator Mode
**Enabled**: No (`injury=False`)
**Why**: ROS projections already incorporate injury impact - injured players have reduced projections. Trade evaluation relies on current ROS value (projections + player_rating + performance), not additional injury penalties.

**Rationale**: Similar to Starter Helper, injury status is implicitly handled in projections. An OUT player's ROS projection is already lowered to reflect missed games. Adding -100 penalty would excessively penalize beyond the projection adjustment. Performance multiplier captures actual injury impact through recent underperformance.

---

## How League Helper Gets the Value/Multiplier

### Step 1: Get Injury Status from Player

**Data Source**: `FantasyPlayer.injury_status` field
**File**: `utils/FantasyPlayer.py:120`

```python
@dataclass
class FantasyPlayer:
    # ... other fields ...
    injury_status: str = "UNKNOWN"  # ACTIVE, QUESTIONABLE, OUT, etc.
```

**Valid Values** (ESPN API designations):
- `ACTIVE`: Player is healthy and available
- `QUESTIONABLE`: Player is game-time decision (50/50 chance)
- `DOUBTFUL`: Player unlikely to play (~25% chance)
- `OUT`: Player will not play this week
- `INJURY_RESERVE`: Player on season-long IR
- `UNKNOWN`: Status not available

### Step 2: Map Injury Status to Risk Level

**Method**: `FantasyPlayer.get_risk_level()`
**File**: `utils/FantasyPlayer.py:322-355`

```python
def get_risk_level(self) -> str:
    """
    Get injury risk level based on injury status.

    Returns:
        str: Risk level (LOW, MEDIUM, or HIGH)
            - LOW: ACTIVE (player is healthy)
            - MEDIUM: QUESTIONABLE (game-time decision)
            - HIGH: DOUBTFUL, OUT, IR (player unlikely to play or unavailable)
    """
    # Normalize status to uppercase for comparison
    status = self.injury_status.upper() if self.injury_status else "UNKNOWN"

    # HIGH risk: Player will not or very unlikely to play
    if status in ["OUT", "DOUBTFUL", "INJURY_RESERVE", "IR"]:
        return "HIGH"

    # MEDIUM risk: Player is uncertain (game-time decision)
    elif status in ["QUESTIONABLE", "Q"]:
        return "MEDIUM"

    # LOW risk: Player is active and healthy
    # Includes ACTIVE, PROBABLE, HEALTHY, UNKNOWN (benefit of doubt)
    else:
        return "LOW"
```

**Risk Level Mapping**:
- **LOW**: ACTIVE (and unknown statuses - benefit of doubt)
- **MEDIUM**: QUESTIONABLE
- **HIGH**: DOUBTFUL, OUT, INJURY_RESERVE

### Step 3: Get Penalty from Config

**Method**: `ConfigManager.get_injury_penalty()`
**File**: `league_helper/util/ConfigManager.py:464-484`

```python
def get_injury_penalty(self, risk_level: str) -> float:
    """
    Get injury penalty for a given risk level.

    Args:
        risk_level: Injury risk level (LOW, MEDIUM, or HIGH)

    Returns:
        float: Penalty points to subtract from player score

    Note:
        If an invalid risk level is provided, defaults to HIGH penalty
        for safety (conservative approach to injury risk)
    """
    # Look up penalty for the given risk level
    if risk_level in self.injury_penalties:
        return self.injury_penalties[risk_level]
    else:
        # Default to HIGH penalty if risk level is unrecognized
        # This is a conservative fallback to avoid drafting risky players
        return self.injury_penalties[self.keys.INJURY_HIGH]
```

### Step 4: Apply Penalty to Score

**Method**: `PlayerScoringCalculator._apply_injury_penalty()`
**File**: `league_helper/util/player_scoring.py:685-697`

```python
def _apply_injury_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply injury penalty (Step 10).

    Args:
        p: Player to evaluate
        player_score: Current score before penalty

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    # Get injury penalty based on player's risk level
    # Risk levels: ACTIVE (no penalty), QUESTIONABLE (small penalty),
    #              DOUBTFUL/OUT (large penalty), IR (very large penalty)
    penalty = self.config.get_injury_penalty(p.get_risk_level())

    # Only show injury reason if player is not fully active
    # This keeps the reason list clean for healthy players
    reason = "" if p.injury_status == "ACTIVE" else f"Injury: {p.injury_status} ({-penalty:.1f} pts)"

    # Subtract penalty from score (injury reduces player value)
    return player_score - penalty, reason
```

**Complete Flow**:
```
Player (injury_status="OUT")
    ↓
get_risk_level() → "OUT" maps to HIGH risk
    ↓
get_injury_penalty("HIGH") → 100.0
    ↓
player_score - 100.0
    ↓
reason = "Injury: OUT (-100.0 pts)"
```

---

## Calculations Involved

### Formula Breakdown

**Risk Level Determination**:
```
If injury_status in ["OUT", "DOUBTFUL", "INJURY_RESERVE", "IR"]:
    risk_level = "HIGH"
Elif injury_status in ["QUESTIONABLE", "Q"]:
    risk_level = "MEDIUM"
Else:
    risk_level = "LOW"
```

**Penalty Lookup**:
```
penalty = INJURY_PENALTIES[risk_level]

Current config:
- LOW: 0 points
- MEDIUM: 0 points
- HIGH: 100 points
```

**Score Adjustment**:
```
adjusted_score = player_score - penalty
```

### Example Calculation (ACTIVE Player)

**Player**: Amon-Ra St. Brown (WR, DET)
**Injury Status**: ACTIVE
**Current Score** (after Steps 1-9): 155.00 points
**Config**: LOW=0, MEDIUM=0, HIGH=100

**Step 1: Get risk level**
```
injury_status = "ACTIVE"
"ACTIVE" not in ["OUT", "DOUBTFUL", "IR"] → Not HIGH
"ACTIVE" not in ["QUESTIONABLE", "Q"] → Not MEDIUM
→ risk_level = "LOW"
```

**Step 2: Get penalty**
```
penalty = INJURY_PENALTIES["LOW"]
penalty = 0 points
```

**Step 3: Apply penalty**
```
adjusted_score = 155.00 - 0 = 155.00 (no change)
reason = "" (empty - player is ACTIVE)
```

**Result**: Healthy player receives no penalty

### Example Calculation (QUESTIONABLE Player)

**Player**: Saquon Barkley (RB, PHI)
**Injury Status**: QUESTIONABLE
**Current Score**: 148.50 points

**Calculation**:
```
injury_status = "QUESTIONABLE"
"QUESTIONABLE" in ["QUESTIONABLE", "Q"] → risk_level = "MEDIUM"

penalty = INJURY_PENALTIES["MEDIUM"]
penalty = 0 points (current config)

adjusted_score = 148.50 - 0 = 148.50 (no change with current config)
reason = "Injury: QUESTIONABLE (-0.0 pts)"
```

**Result**: QUESTIONABLE player receives no penalty with current config

**Note**: Config could be changed to penalize MEDIUM risk (e.g., -20 pts)

### Example Calculation (OUT Player)

**Player**: A.J. Brown (WR, PHI) - hypothetical
**Injury Status**: OUT
**Current Score**: 142.00 points

**Calculation**:
```
injury_status = "OUT"
"OUT" in ["OUT", "DOUBTFUL", "IR"] → risk_level = "HIGH"

penalty = INJURY_PENALTIES["HIGH"]
penalty = 100 points

adjusted_score = 142.00 - 100 = 42.00 points
reason = "Injury: OUT (-100.0 pts)"
```

**Result**: OUT player receives -100 point penalty, dropping from 142 to 42

**Analysis**: This effectively removes the player from top-tier consideration

### Example Calculation (INJURY_RESERVE Player)

**Player**: Hypothetical RB on IR
**Injury Status**: INJURY_RESERVE
**Current Score**: 160.00 points

**Calculation**:
```
injury_status = "INJURY_RESERVE"
"INJURY_RESERVE" in ["OUT", "DOUBTFUL", "IR"] → risk_level = "HIGH"

penalty = 100 points
adjusted_score = 160.00 - 100 = 60.00 points
reason = "Injury: INJURY_RESERVE (-100.0 pts)"
```

**Result**: IR player severely penalized, making them a poor draft choice despite high projections

---

## Data Sources (players.csv Fields)

### Required Fields

| Field Name | Data Type | Description | Valid Values | Example Values |
|------------|-----------|-------------|--------------|----------------|
| `injury_status` | string | ESPN injury designation | ACTIVE, QUESTIONABLE, DOUBTFUL, OUT, INJURY_RESERVE | ACTIVE, QUESTIONABLE, OUT |

### Field Specifications

**`injury_status`**:
- **Type**: string
- **Source**: ESPN API `player.injuryStatus`
- **Valid Values**:
  - `ACTIVE`: Healthy and available
  - `QUESTIONABLE`: Game-time decision
  - `DOUBTFUL`: Unlikely to play
  - `OUT`: Will not play this week
  - `INJURY_RESERVE`: Season-long injured reserve
  - `UNKNOWN`: Status not available (treated as LOW risk)
- **Update frequency**: Updated frequently (multiple times per week, especially near game time)
- **Null handling**: Defaults to "UNKNOWN", treated as LOW risk
- **Case sensitivity**: Normalized to uppercase in risk level determination

**Special Cases**:
- **Bye week players**: May show ACTIVE (healthy but not playing due to bye)
- **Suspended players**: May show as OUT
- **COVID-19 list**: Historically treated as OUT or QUESTIONABLE
- **Practice report**: ESPN may update status based on practice participation

---

## How player-data-fetcher Populates Data

### Data Collection Process

**Main Script**: `player-data-fetcher/player_data_fetcher_main.py`
**ESPN Client**: `player-data-fetcher/espn_client.py`
**Exporter**: `player-data-fetcher/player_data_exporter.py`
**Frequency**: Multiple times per week (especially Wednesday-Sunday during season)

### Injury Status Extraction

**Step 1: Extract injury status from ESPN API response**

```python
# File: player-data-fetcher/espn_client.py:1465-1468

# Extract injury status
injury_status = "ACTIVE"  # Default
injury_info = player_info.get('injuryStatus')
if injury_info:
    injury_status = injury_info.upper()
```

**Step 2: Write to players.csv**

```python
# File: player-data-fetcher/player_data_exporter.py:336-358

# Create FantasyPlayer object with all fields (including injury_status)
fantasy_player = FantasyPlayer(
    id=player_data.id,
    name=player_data.name,
    team=player_data.team,
    position=player_data.position,
    bye_week=player_data.bye_week,
    drafted=drafted_value,
    locked=locked_value,
    fantasy_points=player_data.fantasy_points,
    average_draft_position=player_data.average_draft_position,
    player_rating=player_data.player_rating,
    injury_status=player_data.injury_status,  # Injury status field
    # Weekly projections (weeks 1-17)
    week_1_points=player_data.week_1_points,
    # ... (weeks 2-16) ...
    week_17_points=player_data.week_17_points
)
```

---

## ESPN API JSON Analysis

### Injury Status Data Structure

**API Endpoint**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{leagueId}`

**View Parameters**: `kona_player_info`

**Relevant JSON Path**: `player.injuryStatus`

### JSON Structure

```json
{
  "id": 3929630,
  "fullName": "Saquon Barkley",
  "proTeamId": 21,
  "defaultPositionId": 2,
  "injuryStatus": "QUESTIONABLE",
  "injured": true,
  "injuredSlot": true
}
```

### Field Mapping

| JSON Field | Type | Description | Example Values |
|------------|------|-------------|----------------|
| `injuryStatus` | string | Injury designation | ACTIVE, QUESTIONABLE, OUT, DOUBTFUL, INJURY_RESERVE |
| `injured` | boolean | Whether player has injury designation | true, false |
| `injuredSlot` | boolean | Whether player is in IR slot | true, false |

**Key Field**: `injuryStatus`
- Reflects official NFL injury report designations
- Updated based on team practice reports
- Changes throughout the week as player status evolves

### Extraction Logic

```python
# File: player-data-fetcher/espn_client.py:1465-1468

# Extract injury status
injury_status = "ACTIVE"  # Default
injury_info = player_info.get('injuryStatus')
if injury_info:
    injury_status = injury_info.upper()
```

**Full Context** (espn_client.py:1464-1469):
- Injury status extracted from `player_info.get('injuryStatus')` field
- Default: "ACTIVE" if not present in ESPN data
- Normalization: Converts to uppercase for consistency
- Source: ESPN's injury report system (updated multiple times per week)

**Sample Extraction**:

```python
# Sample players with various statuses
injury_examples = [
    {"name": "Amon-Ra St. Brown", "injuryStatus": "ACTIVE"},
    {"name": "Saquon Barkley", "injuryStatus": "QUESTIONABLE"},
    {"name": "Puka Nacua", "injuryStatus": "QUESTIONABLE"},
    {"name": "A.J. Brown", "injuryStatus": "OUT"}
]

# Written to players.csv
"4374302,Amon-Ra St. Brown,DET,WR,8,167.32,ACTIVE,1,1,..."
"3929630,Saquon Barkley,PHI,RB,9,139.90,QUESTIONABLE,1,0,..."
"4426515,Puka Nacua,LAR,WR,8,175.11,QUESTIONABLE,1,0,..."
"4047646,A.J. Brown,PHI,WR,9,142.81,OUT,1,0,..."
```

---

## Examples with Walkthroughs

### Example 1: Healthy Player (Amon-Ra St. Brown) - No Penalty

**Scenario**: Week 9, evaluating WR Amon-Ra St. Brown for draft
**Player Data**:
- Position: WR
- Team: DET
- Injury Status: ACTIVE
- Current Score (after Steps 1-9): 155.00 points

**Step 1: Get risk level**
```
injury_status = "ACTIVE"
get_risk_level() → "LOW"
```

**Step 2: Get penalty**
```
INJURY_PENALTIES["LOW"] = 0
penalty = 0 points
```

**Step 3: Apply penalty**
```
adjusted_score = 155.00 - 0 = 155.00
reason = "" (empty string - player is ACTIVE)
```

**Result**: Healthy player's score unchanged (155.00)

---

### Example 2: Questionable Player (Saquon Barkley) - No Penalty

**Scenario**: Week 9, evaluating RB Saquon Barkley
**Player Data**:
- Position: RB
- Team: PHI
- Injury Status: QUESTIONABLE
- Current Score: 148.50 points

**Calculation**:
```
injury_status = "QUESTIONABLE"
get_risk_level() → "MEDIUM"

INJURY_PENALTIES["MEDIUM"] = 0 (current config)
penalty = 0 points

adjusted_score = 148.50 - 0 = 148.50
reason = "Injury: QUESTIONABLE (-0.0 pts)"
```

**Result**: QUESTIONABLE player receives no penalty with current configuration

**Note**: Reason string still shows status for user awareness, but penalty is 0

---

### Example 3: Questionable Player (Puka Nacua) - No Penalty

**Scenario**: Week 9, evaluating WR Puka Nacua
**Player Data**:
- Position: WR
- Team: LAR
- Injury Status: QUESTIONABLE
- Current Score: 162.00 points

**Calculation**:
```
risk_level = "MEDIUM"
penalty = 0 points
adjusted_score = 162.00 - 0 = 162.00
reason = "Injury: QUESTIONABLE (-0.0 pts)"
```

**Result**: No penalty applied, but status shown to user

---

### Example 4: OUT Player (A.J. Brown) - Large Penalty

**Scenario**: Week 9, evaluating WR A.J. Brown (hypothetically OUT)
**Player Data**:
- Position: WR
- Team: PHI
- Injury Status: OUT
- Current Score: 142.00 points

**Calculation**:
```
injury_status = "OUT"
get_risk_level() → "HIGH"

INJURY_PENALTIES["HIGH"] = 100
penalty = 100 points

adjusted_score = 142.00 - 100 = 42.00 points
reason = "Injury: OUT (-100.0 pts)"
```

**Result**: OUT player severely penalized, dropping from 142 to 42

**Analysis**: Score drops below most healthy players, effectively removing from draft consideration

---

### Example 5: DOUBTFUL Player - Large Penalty

**Scenario**: Week 9, evaluating RB with DOUBTFUL status
**Player Data**:
- Position: RB
- Injury Status: DOUBTFUL
- Current Score: 135.00 points

**Calculation**:
```
injury_status = "DOUBTFUL"
"DOUBTFUL" in ["OUT", "DOUBTFUL", "IR"] → risk_level = "HIGH"

penalty = 100 points
adjusted_score = 135.00 - 100 = 35.00 points
reason = "Injury: DOUBTFUL (-100.0 pts)"
```

**Result**: DOUBTFUL player receives same penalty as OUT player

**Analysis**: Appropriate since DOUBTFUL players are unlikely to play (similar risk to OUT)

---

### Example 6: INJURY_RESERVE Player - Large Penalty

**Scenario**: Draft evaluation, RB on season-long IR
**Player Data**:
- Position: RB
- Injury Status: INJURY_RESERVE
- Current Score: 180.00 points (high ROS projection assuming return)

**Calculation**:
```
injury_status = "INJURY_RESERVE"
risk_level = "HIGH"

penalty = 100 points
adjusted_score = 180.00 - 100 = 80.00 points
reason = "Injury: INJURY_RESERVE (-100.0 pts)"
```

**Result**: IR player dropped from 180 to 80

**Analysis**: Still might be draftable late-round if expected to return, but significantly devalued

---

### Example 7: UNKNOWN Status - No Penalty

**Scenario**: Player with missing injury data
**Player Data**:
- Injury Status: UNKNOWN (or null)
- Current Score: 120.00 points

**Calculation**:
```
injury_status = "UNKNOWN"
get_risk_level() → "LOW" (default to benefit of doubt)

penalty = 0 points
adjusted_score = 120.00 - 0 = 120.00
reason = "" (treated as ACTIVE)
```

**Result**: Unknown status treated as healthy (no penalty)

**Analysis**: Conservative approach benefits player when data unavailable

---

### Example 8: Comparison - Healthy vs OUT Players

**Scenario**: Week 9, comparing two WRs with similar base scores

**Player A: Healthy WR**
- Injury Status: ACTIVE
- Score before penalty: 145.00
- Risk level: LOW
- Penalty: 0
- **Final score: 145.00**

**Player B: OUT WR**
- Injury Status: OUT
- Score before penalty: 155.00 (slightly higher projection)
- Risk level: HIGH
- Penalty: 100
- **Final score: 55.00**

**Result**:
- Player A ranks 90.00 points higher despite lower base projection
- Injury penalty makes Player B undraftable
- Demonstrates importance of availability over projection

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "INJURY_PENALTIES": {
    "LOW": 0,
    "MEDIUM": 0,
    "HIGH": 100
  }
}
```

### Configuration Fields

| Field | Type | Description | Current Value | Risk Categories |
|-------|------|-------------|---------------|-----------------|
| `INJURY_PENALTIES.LOW` | float | Penalty for low-risk players | 0 | ACTIVE, UNKNOWN |
| `INJURY_PENALTIES.MEDIUM` | float | Penalty for medium-risk players | 0 | QUESTIONABLE |
| `INJURY_PENALTIES.HIGH` | float | Penalty for high-risk players | 100 | OUT, DOUBTFUL, IR |

### Penalty Interpretation

**Current Penalties**:
- LOW: 0 points (no penalty for healthy players)
- MEDIUM: 0 points (no penalty for questionable players)
- HIGH: -100 points (severe penalty for unavailable players)

**Impact on 0-150 Scale** (typical final scores after all steps):
- LOW penalty: No impact (score unchanged)
- MEDIUM penalty: No impact with current config
- HIGH penalty: Drops player ~100 points (e.g., 150 → 50)

**Effect**: Only OUT/DOUBTFUL/IR players penalized in current optimal configuration

### Risk Level Mapping Reference

| Injury Status | Risk Level | Current Penalty | Effect |
|--------------|-----------|----------------|--------|
| ACTIVE | LOW | 0 | No change |
| UNKNOWN | LOW | 0 | No change (benefit of doubt) |
| QUESTIONABLE | MEDIUM | 0 | No change (current config) |
| DOUBTFUL | HIGH | -100 | Severe penalty |
| OUT | HIGH | -100 | Severe penalty |
| INJURY_RESERVE | HIGH | -100 | Severe penalty |

### Configuration Tuning Guide

**Increasing Injury Risk Aversion**:
- Increase HIGH penalty (e.g., 150, 200) → even stronger avoidance
- Add MEDIUM penalty (e.g., 20, 30) → penalize QUESTIONABLE players
- Lower HIGH threshold → treat more statuses as HIGH risk

**Decreasing Injury Risk Aversion**:
- Decrease HIGH penalty (e.g., 50, 75) → accept more injury risk
- Keep MEDIUM at 0 → no penalty for QUESTIONABLE
- Narrow HIGH risk → only OUT and IR get penalty

**Alternative Configurations**:

**Aggressive (penalize all uncertainty)**:
```json
{
  "LOW": 0,
  "MEDIUM": 25,
  "HIGH": 150
}
```

**Moderate (small QUESTIONABLE penalty)**:
```json
{
  "LOW": 0,
  "MEDIUM": 15,
  "HIGH": 100
}
```

**Conservative (current optimal)**:
```json
{
  "LOW": 0,
  "MEDIUM": 0,
  "HIGH": 100
}
```

### Why Current Configuration?

**Optimization Results**:
- Simulation found MEDIUM=0 (no QUESTIONABLE penalty) maximizes win rate
- Suggests QUESTIONABLE players often play and provide value
- HIGH=100 appropriately removes unavailable players from consideration
- Balance between risk aversion and opportunity capture

**Rationale**:
- QUESTIONABLE designation is often precautionary
- Many QUESTIONABLE players end up playing
- Penalizing them reduces draft quality (missed opportunities)
- OUT/DOUBTFUL players very unlikely to contribute → strong penalty appropriate

---

## See Also

### Related Metrics
- **[01_normalization.md](01_normalization.md)** - Base score that injury penalty subtracts from
- **[09_bye_week_penalty.md](09_bye_week_penalty.md)** - Other subtractive penalty
- **[02_adp_multiplier.md](02_adp_multiplier.md)** - Market may already price in injury concerns

### Implementation Files
- **`league_helper/util/player_scoring.py:685-697`** - Injury penalty application
- **`league_helper/util/ConfigManager.py:464-484`** - Injury penalty getter
- **`utils/FantasyPlayer.py:120`** - injury_status field definition
- **`utils/FantasyPlayer.py:350-380`** - get_risk_level() method

### Configuration
- **`data/league_config.json`** - INJURY_PENALTIES parameters
- **`data/players.csv`** - injury_status field

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - Injury penalty tests
- **`tests/league_helper/util/test_ConfigManager.py`** - Injury penalty configuration tests
- **`tests/utils/test_FantasyPlayer.py`** - Risk level mapping tests

### Documentation
- **[README.md](README.md)** - Scoring algorithm overview
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 9
**Documentation Version**: 1.0
**Code Version**: Week 9, 2025 NFL Season
