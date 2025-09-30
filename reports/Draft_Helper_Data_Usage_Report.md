# Draft Helper - Data Usage and Scoring Calculation Report

**Generated:** September 2025
**Author:** Analysis of Draft Helper System
**Purpose:** Comprehensive documentation of how each Draft Helper mode uses `players.csv` data and calculates scores

---

## Table of Contents

1. [Overview](#overview)
2. [Players.csv Data Structure](#playerscsv-data-structure)
3. [Mode-by-Mode Analysis](#mode-by-mode-analysis)
4. [Core Scoring Calculations](#core-scoring-calculations)
5. [Team Scoring Methods](#team-scoring-methods)
6. [Data Flow Summary](#data-flow-summary)

---

## Overview

The Draft Helper system operates in **7 distinct modes** (8 with Starter Helper enabled), each using data from `shared_files/players.csv` in different ways. This report documents:

- **What data fields** each mode reads from `players.csv`
- **How scores are calculated** for players and teams
- **Which scoring functions** are used in each mode
- **Data flow** from CSV through the system

---

## Players.csv Data Structure

### Core Fields Used Across All Modes

```csv
id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,
average_draft_position,player_rating,week_1_points,...,week_17_points
```

### Field Definitions

| Field | Type | Purpose | Used By |
|-------|------|---------|---------|
| `id` | str | Unique player identifier | All modes |
| `name` | str | Player name | All modes |
| `team` | str | Team abbreviation (e.g., 'KC', 'PHI') | All modes |
| `position` | str | Position (QB, RB, WR, TE, K, DST) | All modes |
| `bye_week` | int | Bye week number (1-18) | Draft, Trade, Waiver modes |
| `fantasy_points` | float | Season-total projected points | All scoring modes |
| `injury_status` | str | Injury status (ACTIVE, QUESTIONABLE, OUT, etc.) | All scoring modes |
| `drafted` | int | Draft status: 0=available, 1=drafted by others, 2=on our team | All modes |
| `locked` | int | Lock status: 0=unlocked, 1=locked (protected from trades) | Trade, Waiver modes |
| `average_draft_position` | float | ESPN ADP (lower is better) | Enhanced scoring |
| `player_rating` | float | ESPN player rating (higher is better) | Enhanced scoring |
| `week_1_points` through `week_17_points` | float | Weekly point projections | Starter Helper mode |

### Computed Fields (Added at Runtime)

| Field | Calculation | Used By |
|-------|-------------|---------|
| `weighted_projection` | `(fantasy_points / max_projection) * 100` | Draft mode scoring |
| `score` | Complex multi-factor calculation | Draft recommendations |
| `remaining_season_projection` | Sum of future weeks only | Trade/Waiver modes |

---

## Mode-by-Mode Analysis

### Mode 1: Add to Roster (Draft Mode)

**Purpose:** Recommend and draft players to your team (drafted=2)

#### Data Fields Read:
- **Core:** `id`, `name`, `team`, `position`, `fantasy_points`
- **Availability:** `drafted` (filters for drafted=0 only)
- **Penalties:** `bye_week`, `injury_status`
- **Enhanced Scoring:** `average_draft_position`, `player_rating`

#### Player Selection Logic:
```python
# Filter available players
available_players = [p for p in players if p.drafted == 0]

# Can only draft if:
# 1. Position has open slots (or FLEX eligible)
# 2. Player not drafted (drafted == 0)
# 3. Total roster < MAX_PLAYERS (15)
```

#### Scoring Calculation:
**Function:** `DraftHelper.score_player()` → `ScoringEngine.score_player()`

**Formula:**
```
total_score = positional_need_score
            + projection_score
            - bye_penalty
            - injury_penalty
            + matchup_adjustment
```

**Component Breakdown:**

1. **Positional Need Score** (`compute_positional_need_score`)
   - **Input:** Player position, current roster counts
   - **Calculation:**
     ```python
     if current_count < max_limit:
         need_score = (max_limit - current_count) * POS_NEEDED_SCORE  # POS_NEEDED_SCORE = 50
     else:
         need_score = 0

     # FLEX bonus for RB/WR
     if position in ['RB', 'WR']:
         if flex_count < flex_limit:
             need_score += (flex_limit - flex_count) * POS_NEEDED_SCORE * 0.5
     ```
   - **Example:** If team has 1/2 RBs, need_score = (2-1) * 50 = 50 points

2. **Projection Score** (`compute_projection_score`)
   - **Base Input:** `fantasy_points` or `weighted_projection`
   - **Enhanced Scoring Applied:**
     - **ADP Adjustment:**
       - ADP ≤ 50: +15% boost
       - ADP ≤ 100: +8% boost
       - ADP ≥ 200: -8% penalty
     - **Player Rating Adjustment:**
       - Rating ≥ 80: +20% boost
       - Rating ≥ 60: +10% boost
       - Rating ≤ 30: -10% penalty
     - **Team Quality Adjustment:**
       - Offensive players use team offensive rank
       - Top 5 team: +12% boost
       - Top 12 team: +6% boost
       - Bottom 8 teams: -6% penalty
   - **Positional Ranking Adjustment:**
     - Elite offense (rank 1-5): +1.5% additional
     - Good offense (rank 6-12): +0.75% additional
     - Poor offense (rank 25-32): -0.75% penalty
   - **Total Caps:** Min 70% to Max 150% of base score

3. **Bye Week Penalty** (`compute_bye_penalty_for_player`)
   - **Input:** Player bye_week, roster bye_week distribution
   - **Calculation:**
     ```python
     if player_bye_week < CURRENT_NFL_WEEK:
         penalty = 0  # Bye already passed
     else:
         same_position_on_bye = count_roster_players_with_same_bye(position, bye_week)

         if position in ['RB', 'WR']:  # FLEX eligible
             all_flex_on_bye = count_flex_players_with_same_bye(bye_week)
             if all_flex_on_bye >= 2:
                 penalty = BASE_BYE_PENALTY * 1.5  # 15 * 1.5 = 22.5
             elif same_position_on_bye >= 1:
                 penalty = BASE_BYE_PENALTY  # 15
             else:
                 penalty = BASE_BYE_PENALTY * 0.5  # 7.5
         else:
             if same_position_on_bye >= 1:
                 penalty = BASE_BYE_PENALTY * 1.5  # 22.5
             else:
                 penalty = BASE_BYE_PENALTY  # 15
     ```
   - **Constant:** `BASE_BYE_PENALTY = 15`

4. **Injury Penalty** (`compute_injury_penalty`)
   - **Input:** `injury_status`
   - **Calculation:**
     ```python
     risk_level = get_risk_level(injury_status)
     # ACTIVE → "LOW" → 0
     # QUESTIONABLE/UNKNOWN → "MEDIUM" → 25
     # OUT/INJURY_RESERVE → "HIGH" → 50

     penalty = INJURY_PENALTIES[risk_level]
     ```
   - **Constants:**
     ```python
     INJURY_PENALTIES = {
         "LOW": 0,
         "MEDIUM": 25,
         "HIGH": 50
     }
     ```

5. **Matchup Adjustment** (if available)
   - **Input:** `matchup_adjustment` attribute (set by matchup analyzer)
   - **Range:** Typically -2.0 to +2.0 points

#### Roster Display Logic:
After drafting, players are assigned to draft rounds based on:
```python
# Match players to rounds based on:
# 1. Position fit with DRAFT_ORDER[round_num]
# 2. Fantasy points (higher is better)
# 3. Round assignment optimization

for round_num in range(MAX_PLAYERS):
    ideal_positions = DRAFT_ORDER[round_num]  # e.g., {FLEX: 1.0, QB: 0.7}
    # Assign best available player matching ideal position
```

#### CSV Updates:
- Sets `drafted = 2` for selected player
- Saves entire players list to `players.csv`
- Preserves all other fields (locked, weekly points, etc.)

---

### Mode 2: Mark Drafted Player

**Purpose:** Mark players drafted by others (drafted=1) to remove from available pool

#### Data Fields Read:
- **Search:** `name`, `position`, `team`
- **Update:** `drafted`

#### Search Logic:
```python
# Fuzzy name matching (case-insensitive)
search_results = []
for player in players:
    if search_term.lower() in player.name.lower():
        search_results.append(player)

# Can search by:
# - Full name: "Patrick Mahomes"
# - Last name: "Mahomes"
# - First name: "Patrick"
# - Partial: "Patt"
```

#### CSV Updates:
- Sets `drafted = 1` for selected player
- Saves entire players list to `players.csv`
- No scoring calculations performed

#### No Scoring Used:
This mode only updates the `drafted` field and does not calculate any scores.

---

### Mode 3: Waiver Optimizer (Trade Analysis)

**Purpose:** Analyze roster and recommend beneficial waiver wire pickups (trading roster players for available players)

#### Data Fields Read:
- **Core:** All fields from Mode 1 (Draft)
- **Trade-Specific:** `locked` (locked=1 players excluded from trades)
- **Roster:** Only players with `drafted == 2`
- **Available:** Only players with `drafted == 0`

#### Player Selection Logic:
```python
# Roster players (can be traded away)
roster_players = [p for p in players if p.drafted == 2 and p.locked == 0]

# Available players (can be acquired)
available_players = [p for p in players if p.drafted == 0 and p.locked == 0]
```

#### Scoring Calculation:
**Function:** `DraftHelper.score_player_for_trade()` → `ScoringEngine.score_player_for_trade()`

**Formula:**
```
trade_score = 0  # No positional need
            + projection_score  # Same as draft mode
            - bye_penalty  # Exclude self from roster
            - injury_penalty  # Conditional based on config
            + matchup_adjustment
```

**Key Difference from Draft Mode:**
- **Positional need score = 0** (no position shortage bias)
- **Bye penalty excludes self** if player is on roster (exclude_self=True)
- **Injury penalty conditional:**
  ```python
  if TRADE_HELPER_MODE and not APPLY_INJURY_PENALTY_TO_ROSTER and player.drafted == 2:
      injury_penalty = 0  # Optimistic view of your players
  else:
      injury_penalty = INJURY_PENALTIES[risk_level]
  ```

#### Trade Optimization Algorithm:
**Pure Greedy Approach** (`TradeAnalyzer.optimize_roster_iteratively`)

```python
def optimize_roster_iteratively(available_players):
    trades_made = []
    iteration = 0
    recent_trades = set()  # Prevent oscillation

    while iteration < 100:
        # Find best trade across all roster positions
        best_trade = find_best_trade_with_runners_up(available_players, recent_trades)

        if best_trade is None:
            break  # No beneficial trades found

        improvement = best_trade['improvement']
        if improvement < MIN_TRADE_IMPROVEMENT:  # Default: 1.0 points
            break

        # Execute trade
        team.replace_player(best_trade['out'], best_trade['in'])

        # Track to prevent reversal
        recent_trades.add((best_trade['out'].id, best_trade['in'].id))
        recent_trades.add((best_trade['in'].id, best_trade['out'].id))

        trades_made.append(best_trade)
        iteration += 1

    return trades_made
```

#### Trade Evaluation:
```python
def find_best_trade_with_runners_up(available_players, recent_trades):
    best_trade = None
    best_improvement = 0

    for roster_player in team.roster:
        if roster_player.locked == 1:
            continue

        current_score = score_player_for_trade(roster_player)

        # Find replacements (same position or FLEX-eligible)
        candidates = get_position_candidates(roster_player, available_players)

        for candidate in candidates:
            candidate_score = score_player_for_trade(candidate)
            improvement = candidate_score - current_score

            if improvement >= MIN_TRADE_IMPROVEMENT:
                if improvement > best_improvement:
                    best_trade = {
                        'out': roster_player,
                        'in': candidate,
                        'improvement': improvement
                    }
                    best_improvement = improvement

    return best_trade
```

#### Team Score Calculation:
**Function:** `FantasyTeam.get_total_team_score(scoring_function)`

```python
def get_total_team_score(scoring_function):
    total_score = 0
    for player in roster:
        total_score += scoring_function(player)  # Uses score_player_for_trade
    return total_score
```

#### Roster Comparison Display:
```python
initial_score = team.get_total_team_score(score_player_for_trade)
# Execute trades...
final_score = team.get_total_team_score(score_player_for_trade)
total_improvement = final_score - initial_score

# Show by position:
for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']:
    position_players = team.get_players_by_slot(position)
    position_score = sum(score_player_for_trade(p) for p in position_players)
    print(f"{position}: {position_score:.2f} points")
```

#### CSV Updates:
- **Important:** Changes are **NOT saved** to CSV
- After analysis, original player states are restored:
  ```python
  finally:
      # Restore original player states
      for player_id, original_state in original_player_states.items():
          player.drafted = original_state

      # Restore original roster
      team.roster = original_roster
  ```
- This mode is **simulation-only** - no persistent changes

---

### Mode 4: Drop Player

**Purpose:** Remove players from roster (set drafted=0) or from other teams' rosters

#### Data Fields Read:
- **Search:** `name`, `position`, `team`
- **Filter:** `drafted` (only shows drafted != 0)
- **Update:** `drafted`

#### Player Selection Logic:
```python
# Show all drafted players (both roster and others)
drafted_players = [p for p in players if p.drafted != 0]

# Fuzzy search within drafted players
search_results = [p for p in drafted_players if search_term.lower() in p.name.lower()]
```

#### CSV Updates:
- Sets `drafted = 0` for selected player
- Removes player from `team.roster` if drafted==2
- Saves entire players list to `players.csv`

#### No Scoring Used:
This mode only updates the `drafted` field and does not calculate any scores.

---

### Mode 5: Lock/Unlock Player

**Purpose:** Toggle lock status for roster players (prevent trade suggestions)

#### Data Fields Read:
- **Core:** `name`, `position`, `team`, `fantasy_points`
- **Filter:** `drafted` (only shows drafted == 2)
- **Display:** `locked` (0=unlocked, 1=locked)
- **Update:** `locked`

#### Player Selection Logic:
```python
# Only roster players
roster_players = [p for p in players if p.drafted == 2]

# Group by lock status
unlocked_players = [p for p in roster_players if p.locked == 0]
locked_players = [p for p in roster_players if p.locked == 1]

# Display both groups with fantasy_points
```

#### CSV Updates:
- Toggles `locked` between 0 and 1 for selected player
- Saves entire players list to `players.csv`

#### No Scoring Used:
This mode displays `fantasy_points` but does not calculate any scores.

---

### Mode 6: Starter Helper (Integrated)

**Purpose:** Generate optimal starting lineup for current week

#### Data Fields Read:
- **Core:** `id`, `name`, `team`, `position`
- **Roster:** `drafted` (only drafted == 2)
- **Projections:** `fantasy_points` and `week_N_points` columns
- **Penalties:** `bye_week`, `injury_status`

#### Player Selection Logic:
```python
# Get roster players only
roster_players = [p for p in players if p.drafted == 2]

# Convert to DataFrame for LineupOptimizer
roster_df = pd.DataFrame([p.to_dict() for p in roster_players])
```

#### Projection Calculation:
```python
def get_weekly_projection(player, current_week):
    # Try to get week-specific projection
    week_column = f'week_{current_week}_points'
    if hasattr(player, week_column) and getattr(player, week_column) is not None:
        return getattr(player, week_column)

    # Fallback: use season average
    return player.fantasy_points / 17.0  # 17 weeks in fantasy regular season
```

#### Lineup Optimization:
**Function:** `LineupOptimizer.optimize_lineup(roster_df, projections)`

**Lineup Constraints:**
```python
LINEUP_REQUIREMENTS = {
    'QB': 1,    # Must start 1 QB
    'RB': 2,    # Must start 2 RBs
    'WR': 2,    # Must start 2 WRs
    'TE': 1,    # Must start 1 TE
    'FLEX': 1,  # Must start 1 RB or WR
    'K': 1,     # Must start 1 Kicker
    'DST': 1    # Must start 1 Defense
}
```

**Optimization Algorithm:**
```python
def optimize_lineup(roster_df, projections):
    # 1. Sort players by position and projected points (high to low)
    # 2. Fill required positions first (QB, TE, K, DST)
    # 3. Fill RB/WR slots with top 2 of each
    # 4. Fill FLEX with best remaining RB or WR

    optimal_lineup = OptimalLineup()
    used_players = set()

    # Apply penalties
    for player in roster:
        adjusted_projection = projections[player.id]

        # Bye week penalty
        if player.bye_week == current_week:
            adjusted_projection = 0  # Cannot start

        # Injury penalty
        if player.injury_status == 'OUT':
            adjusted_projection = 0
        elif player.injury_status == 'QUESTIONABLE':
            adjusted_projection *= 0.9  # 10% reduction

    # Select best players for each slot
    # ... (greedy selection by adjusted projection)

    return optimal_lineup
```

#### Total Score Calculation:
```python
total_projected_points = sum([
    starter.projected_points
    for starter in optimal_lineup.get_all_starters()
])
```

#### CSV Updates:
- **No changes to players.csv**
- Outputs results to `draft_helper/data/starter_helper/` directory
- Creates timestamped and "latest" result files

---

### Mode 7: Trade Simulator

**Purpose:** Simulate trades without affecting actual roster data

#### Data Fields Read:
- **Core:** `id`, `name`, `team`, `position`, `fantasy_points`
- **Roster:** `drafted` (shows drafted == 2 for current roster)
- **Available:** `drafted` (can search drafted == 0 or drafted == 1)

#### Display Logic:
```python
def display_current_roster_with_scores(team, scoring_function):
    print("\nCURRENT ROSTER:")
    print("="*60)

    # Calculate position totals
    position_totals = {}
    for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']:
        players = team.get_players_by_slot(position)
        position_score = sum(scoring_function(p) for p in players)
        position_totals[position] = position_score

    # Display numbered list (1-15)
    for i, player in enumerate(team.roster, 1):
        score = scoring_function(player)
        slot = team.get_slot_assignment(player)
        print(f"{i:2d}. {player.name:25s} ({player.position:3s}, {player.team:3s}) "
              f"- {score:.1f} pts [Slot: {slot}]")

    total_score = sum(position_totals.values())
    print(f"\nTOTAL TEAM SCORE: {total_score:.2f}")
    print(f"By Position: {position_totals}")
```

#### Scoring Calculation:
Uses same `score_player_for_trade()` function as Waiver Optimizer mode.

#### Trade Simulation:
```python
class TradeSimulator:
    def __init__(self, team, all_players, scoring_function):
        self.team = team.copy_team()  # Deep copy for simulation
        self.all_players = all_players
        self.original_team = team
        self.scoring_function = scoring_function
        self.trade_history = []

    def simulate_trade(self, roster_player_num, new_player_name):
        # 1. Get roster player by number (1-15)
        old_player = self.team.roster[roster_player_num - 1]

        # 2. Search for new player by name (fuzzy matching)
        new_player = self.search_available_player(new_player_name)

        # 3. Calculate score comparison
        old_score = self.scoring_function(old_player)
        new_score = self.scoring_function(new_player)
        improvement = new_score - old_score

        # 4. Execute trade
        success = self.team.replace_player(old_player, new_player)

        if success:
            self.trade_history.append({
                'out': old_player,
                'in': new_player,
                'improvement': improvement
            })

            # Display updated scores
            self.display_score_comparison()
```

#### Score Comparison Display:
```python
def display_score_comparison():
    original_score = original_team.get_total_team_score(scoring_function)
    current_score = simulated_team.get_total_team_score(scoring_function)

    print("\nSCORE COMPARISON:")
    print(f"Original Roster: {original_score:.2f}")
    print(f"Current Simulation: {current_score:.2f}")
    print(f"Net Change: {current_score - original_score:+.2f}")

    # By position breakdown
    for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']:
        original_pos_score = get_position_score(original_team, position)
        current_pos_score = get_position_score(simulated_team, position)
        change = current_pos_score - original_pos_score
        print(f"  {position}: {original_pos_score:.1f} -> {current_pos_score:.1f} ({change:+.1f})")
```

#### CSV Updates:
- **No changes to players.csv**
- All simulations use temporary team copy
- Original roster restored on exit

---

## Core Scoring Calculations

### Enhanced Scoring System

The system uses a sophisticated multi-factor scoring approach combining:

#### 1. Base Projection Score
```python
# Priority chain:
if hasattr(player, 'remaining_season_projection'):
    base_score = player.remaining_season_projection
elif hasattr(player, 'weighted_projection'):
    base_score = player.weighted_projection
else:
    base_score = player.fantasy_points
```

#### 2. Enhanced Scoring Multipliers
**Source:** `EnhancedScoringCalculator.calculate_enhanced_score()`

```python
enhanced_score = base_score * total_multiplier

where:
    total_multiplier = adp_multiplier * rating_multiplier * team_multiplier

Constraints:
    0.70 ≤ total_multiplier ≤ 1.50  (capped at ±50%)
```

**ADP Multiplier:**
```python
if adp ≤ 50:
    multiplier = 1.15  # +15% for elite ADP
elif adp ≤ 100:
    multiplier = 1.08  # +8% for good ADP
elif adp ≥ 200:
    multiplier = 0.92  # -8% for poor ADP
else:
    multiplier = 1.0   # Neutral
```

**Player Rating Multiplier:**
```python
if player_rating ≥ 80:
    multiplier = 1.20  # +20% for excellent rating
elif player_rating ≥ 60:
    multiplier = 1.10  # +10% for good rating
elif player_rating ≤ 30:
    multiplier = 0.90  # -10% for poor rating
else:
    multiplier = 1.0   # Neutral (with linear interpolation)

Max cap: 1.25  # Cannot exceed +25% from rating alone
```

**Team Quality Multiplier:**
```python
# Use offensive rank for QB/RB/WR/TE/K, defensive rank for DST
if team_rank ≤ 5:
    multiplier = 1.12  # +12% for elite team
elif team_rank ≤ 12:
    multiplier = 1.06  # +6% for good team
elif team_rank ≥ 25:
    multiplier = 0.94  # -6% for poor team
else:
    multiplier = 1.0   # Neutral
```

#### 3. Positional Ranking Adjustment
**Source:** `PositionalRankingCalculator.calculate_positional_adjustment()`

```python
# Applied AFTER enhanced scoring
base_multiplier = get_multiplier_from_rank(team_rank)

# Examples:
if rank ≤ 5:   # Elite
    base_multiplier = 1.10  # +10%
elif rank ≤ 12:  # Good
    base_multiplier = 1.05  # +5%
elif rank ≥ 25:  # Poor
    base_multiplier = 0.95  # -5%
else:
    base_multiplier = 1.0   # Neutral

# Apply weight factor (default: 15%)
final_multiplier = 1.0 + (base_multiplier - 1.0) * 0.15

adjusted_points = enhanced_score * final_multiplier
```

**Example Full Calculation:**

```python
# Patrick Mahomes (QB, KC)
base_points = 315.5
adp = 8.0  # Elite ADP
player_rating = 92.0  # Excellent rating
team_offensive_rank = 2  # Elite offense

# Step 1: Enhanced Scoring
adp_mult = 1.15  # ADP ≤ 50
rating_mult = 1.20  # Rating ≥ 80
team_mult = 1.12  # Rank ≤ 5
total_mult = 1.15 * 1.20 * 1.12 = 1.54 → capped at 1.50

enhanced_score = 315.5 * 1.50 = 473.25

# Step 2: Positional Ranking
rank_mult_base = 1.10  # Elite offense
rank_mult_weighted = 1.0 + (1.10 - 1.0) * 0.15 = 1.015

final_score = 473.25 * 1.015 = 480.35

# Step 3: Penalties
bye_penalty = 15  # Standard penalty (no conflicts)
injury_penalty = 0  # ACTIVE status

# Final Score
total_score = 480.35 - 15 - 0 = 465.35
```

---

## Team Scoring Methods

### Method 1: Total Roster Score
**Function:** `FantasyTeam.get_total_team_score(scoring_function)`

```python
def get_total_team_score(scoring_function):
    """Calculate total fantasy points for entire roster."""
    total = 0.0
    for player in roster:
        total += scoring_function(player)
    return total
```

**Used By:**
- Waiver Optimizer (Mode 3)
- Trade Simulator (Mode 7)

### Method 2: Position-Based Score
**Custom Implementation:** Used in roster comparison displays

```python
def get_position_scores(team, scoring_function):
    """Calculate scores by position slot."""
    position_scores = {}

    for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']:
        players_in_slot = team.get_players_by_slot(position)
        position_score = sum(scoring_function(p) for p in players_in_slot)
        position_scores[position] = position_score

    return position_scores
```

**Used By:**
- Roster comparison displays (Waiver Optimizer, Trade Simulator)

### Method 3: Starter-Only Score
**Function:** `LineupOptimizer.optimize_lineup()` (Starter Helper)

```python
def get_starter_total_score(optimal_lineup):
    """Calculate total for starting lineup only (9 players)."""
    starters = optimal_lineup.get_all_starters()
    total = sum(starter.projected_points for starter in starters if starter)
    return total
```

**Used By:**
- Starter Helper (Mode 6)
- Only counts the 9 starting positions (ignores bench)

---

## Data Flow Summary

### Read Operations (All Modes)

```
players.csv
    ↓
FantasyPlayer.from_dict() for each row
    ↓
List[FantasyPlayer] stored in DraftHelper.players
    ↓
Mode-specific filtering and processing
```

### Write Operations (Modes 1, 2, 4, 5)

```
User action modifies player.drafted or player.locked
    ↓
DraftHelper.save_players()
    ↓
Converts players to dict: player.to_dict()
    ↓
Writes to CSV with DictWriter
    ↓
players.csv updated
```

### Score Calculation Flow

```
Player Data (CSV)
    ↓
┌─────────────────────────────────────┐
│ Base Data Extraction                │
│ - fantasy_points                    │
│ - average_draft_position            │
│ - player_rating                     │
│ - team, position                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Enhanced Scoring Calculator         │
│ - ADP adjustment                    │
│ - Player rating adjustment          │
│ - Team quality adjustment           │
│ Result: enhanced_score              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Positional Ranking Calculator       │
│ - Team rank lookup                  │
│ - Matchup quality assessment        │
│ Result: ranking_adjusted_score      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Scoring Engine                      │
│ - Positional need score             │
│ - Bye week penalty                  │
│ - Injury penalty                    │
│ - Matchup adjustment                │
│ Result: final_player_score          │
└─────────────────────────────────────┘
    ↓
Mode-Specific Usage:
- Draft Mode: score_player()
- Trade/Waiver: score_player_for_trade()
- Starter Helper: weekly projections only
```

### FLEX Position Handling

**Critical Logic:** RB and WR players can occupy FLEX slot

```python
# Slot assignment priority:
if position_slot_available(player.position):
    assign_to_natural_slot(player)
elif position in ['RB', 'WR'] and flex_slot_available():
    assign_to_flex_slot(player)
else:
    raise ValueError("No slots available")

# Tracking:
team.slot_assignments = {
    'QB': [player_ids],
    'RB': [player_ids],
    'WR': [player_ids],
    'TE': [player_ids],
    'FLEX': [player_ids],  # Can contain RB or WR IDs
    'K': [player_ids],
    'DST': [player_ids]
}
```

**Impact on Scoring:**
- FLEX eligibility adds +25 points to positional need score for RB/WR
- Trade algorithm checks both natural position and FLEX for valid swaps

---

## Configuration Constants

### Key Constants from `draft_helper_constants.py`

```python
# Roster limits
MAX_PLAYERS = 15
MAX_POSITIONS = {
    'QB': 2,
    'RB': 4,
    'WR': 4,
    'FLEX': 1,
    'TE': 2,
    'K': 1,
    'DST': 1
}

# Scoring weights
POS_NEEDED_SCORE = 50
PROJECTION_BASE_SCORE = 100
BASE_BYE_PENALTY = 15
INJURY_PENALTIES = {
    "LOW": 0,
    "MEDIUM": 25,
    "HIGH": 50
}

# Trade optimization
MIN_TRADE_IMPROVEMENT = 1.0
```

### Configuration Files

| File | Purpose |
|------|---------|
| `draft_helper_constants.py` | Core roster and scoring constants |
| `draft_helper_config.py` | Mode toggles, file paths, injury settings |
| `shared_config.py` | Current NFL week (CRITICAL weekly update) |
| `enhanced_scoring.py` | ADP, rating, team quality multipliers |
| `positional_ranking_calculator.py` | Matchup adjustment factors |

---

## Summary Table: Data Usage by Mode

| Mode | Reads `drafted` | Writes `drafted` | Reads `locked` | Writes `locked` | Reads Weekly Points | Calculates Scores |
|------|----------------|------------------|----------------|-----------------|---------------------|-------------------|
| 1. Add to Roster | ✓ (filter) | ✓ (sets to 2) | ✗ | ✗ | ✗ | ✓ (full scoring) |
| 2. Mark Drafted | ✓ (filter) | ✓ (sets to 1) | ✗ | ✗ | ✗ | ✗ |
| 3. Waiver Optimizer | ✓ (filter) | ✗ (simulation) | ✓ (filter) | ✗ | ✗ | ✓ (trade scoring) |
| 4. Drop Player | ✓ (filter) | ✓ (sets to 0) | ✗ | ✗ | ✗ | ✗ |
| 5. Lock/Unlock | ✓ (filter) | ✗ | ✓ (display) | ✓ (toggle) | ✗ | ✗ (displays only) |
| 6. Starter Helper | ✓ (filter) | ✗ | ✗ | ✗ | ✓ | ✓ (lineup optimization) |
| 7. Trade Simulator | ✓ (filter) | ✗ (simulation) | ✗ | ✗ | ✗ | ✓ (trade scoring) |

---

## Appendix: Example Score Calculations

### Example 1: QB with Excellent Profile

**Player:** Patrick Mahomes (QB, KC)

**Data from players.csv:**
```csv
id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,average_draft_position,player_rating
4046,Patrick Mahomes,KC,QB,6,315.5,ACTIVE,0,0,8.0,92.0
```

**Calculation (Draft Mode):**
```
1. Positional Need Score:
   - Current QBs on roster: 0
   - Max QBs allowed: 2
   - need_score = (2 - 0) * 50 = 100

2. Projection Score:
   a) Enhanced Scoring:
      base = 315.5
      adp_mult = 1.15 (ADP ≤ 50)
      rating_mult = 1.20 (rating ≥ 80)
      team_mult = 1.12 (offensive rank #2)
      total_mult = 1.54 → capped at 1.50
      enhanced = 315.5 * 1.50 = 473.25

   b) Positional Ranking:
      rank_mult = 1.0 + (1.10 - 1.0) * 0.15 = 1.015
      adjusted = 473.25 * 1.015 = 480.35

3. Bye Week Penalty:
   - Bye week 6, no other QBs on bye
   - penalty = 15

4. Injury Penalty:
   - Status: ACTIVE
   - penalty = 0

5. Matchup Adjustment:
   - (none for draft mode)
   - adjustment = 0

TOTAL SCORE = 100 + 480.35 - 15 - 0 + 0 = 565.35
```

### Example 2: RB with Average Profile

**Player:** Kareem Hunt (RB, CLE)

**Data from players.csv:**
```csv
id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,average_draft_position,player_rating
4098,Kareem Hunt,CLE,RB,10,135.54,ACTIVE,0,0,120.0,45.0
```

**Calculation (Draft Mode):**
```
1. Positional Need Score:
   - Current RBs on roster: 2
   - Max RBs allowed: 4
   - FLEX count: 0, max: 1
   - need_score = (4 - 2) * 50 + (1 - 0) * 50 * 0.5 = 100 + 25 = 125

2. Projection Score:
   a) Enhanced Scoring:
      base = 135.54
      adp_mult = 1.08 (ADP ≤ 100)
      rating_mult = 1.0 (neutral range)
      team_mult = 1.06 (offensive rank #8)
      total_mult = 1.08 * 1.0 * 1.06 = 1.1448
      enhanced = 135.54 * 1.1448 = 155.17

   b) Positional Ranking:
      rank_mult = 1.0 + (1.05 - 1.0) * 0.15 = 1.0075
      adjusted = 155.17 * 1.0075 = 156.33

3. Bye Week Penalty:
   - Bye week 10, 1 other RB on bye (week 10)
   - penalty = 15 (standard for FLEX-eligible with conflict)

4. Injury Penalty:
   - Status: ACTIVE
   - penalty = 0

5. Matchup Adjustment:
   - adjustment = 0

TOTAL SCORE = 125 + 156.33 - 15 - 0 + 0 = 266.33
```

### Example 3: Trade Score Comparison

**Scenario:** Trading out Kareem Hunt for TreVeyon Henderson

**Hunt (on roster):**
```csv
4098,Kareem Hunt,CLE,RB,10,135.54,ACTIVE,2,0,120.0,45.0
```

**Henderson (available):**
```csv
4242,TreVeyon Henderson,JAX,RB,12,121.97,ACTIVE,0,0,85.0,65.0
```

**Hunt Trade Score:**
```
1. Positional Need = 0 (trade mode)

2. Projection Score:
   enhanced = 155.17 (same as above)
   ranking_adjusted = 156.33

3. Bye Week Penalty:
   - Exclude self from roster for calculation
   - No other RBs on week 10 after removing Hunt
   - penalty = 7.5 (reduced for FLEX coverage)

4. Injury Penalty = 0

HUNT SCORE = 0 + 156.33 - 7.5 - 0 = 148.83
```

**Henderson Trade Score:**
```
1. Positional Need = 0

2. Projection Score:
   a) Enhanced:
      base = 121.97
      adp_mult = 1.08 (ADP ≤ 100)
      rating_mult = 1.10 (rating ≥ 60)
      team_mult = 1.0 (neutral rank #18)
      total_mult = 1.08 * 1.10 * 1.0 = 1.188
      enhanced = 121.97 * 1.188 = 144.90

   b) Ranking:
      rank_mult = 1.0 (neutral)
      adjusted = 144.90

3. Bye Week Penalty:
   - Week 12, no conflicts
   - penalty = 7.5

4. Injury Penalty = 0

HENDERSON SCORE = 0 + 144.90 - 7.5 - 0 = 137.40
```

**Trade Evaluation:**
```
improvement = Henderson_score - Hunt_score
           = 137.40 - 148.83
           = -11.43

Result: TRADE NOT RECOMMENDED (negative improvement)
```

**Note:** In the actual system with current team rankings and full context, Henderson might score higher due to upside factors not captured in this example.

---

## Conclusion

The Draft Helper system uses `players.csv` data in sophisticated ways across 7 distinct modes:

1. **Persistent Modes** (1, 2, 4, 5) modify and save changes to `players.csv`
2. **Simulation Modes** (3, 7) use data for analysis but restore original states
3. **Read-Only Mode** (6) uses data for lineup optimization without modifications

**Scoring is calculated** in 4 modes (1, 3, 6, 7) using multi-factor algorithms:
- Enhanced scoring (ADP, rating, team quality)
- Positional ranking adjustments
- Penalty systems (bye weeks, injuries)
- Position-specific logic (FLEX eligibility)

**Team scores** are calculated as:
- Sum of all roster player scores (Modes 3, 7)
- Sum of starting lineup only (Mode 6)
- Position-grouped totals for display purposes

This comprehensive system ensures accurate player valuation while maintaining data integrity across all operational modes.

---

**End of Report**