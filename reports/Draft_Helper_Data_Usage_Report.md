# Draft Helper Data Usage Report

**Last Updated**: 2025-09-30
**Version**: 2.0+ (Post-Scoring Overhaul)

## Overview

This document details how the Draft Helper system processes and scores fantasy football players using a modular, multi-step scoring architecture. The system uses different scoring flows depending on the mode (Draft vs Trade/Waiver) to provide optimal recommendations.

---

## Data Sources

### Primary Data Inputs
1. **Player Database** (`shared_files/players.csv`)
   - Master database with seasonal fantasy point projections
   - Drafted status (0=available, 1=drafted by others, 2=on your roster)
   - Injury status and risk levels
   - Position, team, and identification data

2. **Bye Week Schedule** (`shared_files/bye_weeks.csv`)
   - NFL bye week schedule by team
   - Updated manually before each season

3. **ESPN Player Data** (via `player-data-fetcher`)
   - Weekly and seasonal projections
   - Average Draft Position (ADP)
   - Player rankings by position
   - Real-time injury updates

4. **Team Rankings** (via `enhanced_scoring`)
   - Offensive team strength ratings
   - Used to adjust player value based on team quality

---

## Scoring Architecture

### Add to Roster Mode (7-Step Scoring)

Used during initial draft to evaluate all available players.

#### Step 1: Normalization
**Purpose**: Scale seasonal fantasy points to consistent 0-N range (default: 0-100)

**Formula**:
```
normalized_score = (player_points / max_player_points) * NORMALIZATION_MAX_SCALE
```

**Implementation**: `NormalizationCalculator` class
- Finds max fantasy points among all available players (drafted=0)
- Caches max value for performance
- Cache invalidated after each draft pick
- Fallback to `fantasy_points` if `remaining_season_projection` unavailable

**Configuration**:
- `NORMALIZATION_MAX_SCALE = 100.0` (default, configurable 80-120 in simulation)

**Example**:
```
Player A: 250 points (seasonal projection)
Max available: 300 points
Normalized: (250 / 300) * 100 = 83.33
```

---

#### Step 2: ADP Multiplier
**Purpose**: Apply consensus value adjustment based on Average Draft Position

**Implementation**: `EnhancedScoring` class
- Earlier ADP = higher multiplier (reflects consensus value)
- ADP data from ESPN projections

**Formula**: Multiplier applied to normalized score based on ADP rank

**Example**:
```
Normalized score: 83.33
ADP multiplier: 1.15 (high consensus value)
After ADP: 83.33 * 1.15 = 95.83
```

---

#### Step 3: Player Ranking Multiplier
**Purpose**: Apply position-specific ranking bonus

**Implementation**: `PositionalRankingCalculator` via `EnhancedScoring`
- Higher-ranked players within their position receive bonus
- QB1, RB1, WR1 get highest multipliers

**Example**:
```
After ADP: 95.83
Position rank multiplier: 1.10 (RB3 in position)
After rank: 95.83 * 1.10 = 105.41
```

---

#### Step 4: Team Ranking Multiplier
**Purpose**: Adjust value based on offensive team strength

**Implementation**: `TeamDataLoader` via `EnhancedScoring`
- Players on stronger offensive teams receive bonus
- Reflects better scoring environment

**Example**:
```
After rank: 105.41
Team ranking multiplier: 1.05 (strong offense)
After team: 105.41 * 1.05 = 110.68
```

---

#### Step 5: Draft Order Bonus
**Purpose**: Add round-based position bonuses to prioritize positional needs

**Implementation**: `DraftOrderCalculator` class
- Current round = roster size (0-indexed for DRAFT_ORDER array access)
- Each round configured with ideal positions and static point bonuses
- FLEX eligibility: Only RB and WR positions

**Configuration**:
```python
DRAFT_ORDER = [
    {FLEX: 50, QB: 25},    # Round 1: FLEX players +50, QB +25
    {FLEX: 50, QB: 25},    # Round 2: Same priorities
    {FLEX: 50, QB: 30},    # Round 3: Increased QB bonus
    {FLEX: 50, QB: 30},    # Round 4: Same
    {QB: 50, FLEX: 25},    # Round 5: Prioritize QB
    {TE: 50, FLEX: 25},    # Round 6: TE priority
    {FLEX: 50},            # Round 7: FLEX only
    {FLEX: 50},            # Round 8: FLEX only
    {FLEX: 50},            # Round 9: FLEX only
    {FLEX: 50},            # Round 10: FLEX only
    {FLEX: 50},            # Round 11: FLEX only
    {FLEX: 50},            # Round 12: FLEX only
    {FLEX: 50},            # Round 13: FLEX only
    {K: 50},               # Round 14: Kicker
    {DST: 50}              # Round 15: Defense
]

DRAFT_ORDER_PRIMARY_BONUS = 50
DRAFT_ORDER_SECONDARY_BONUS = 25
```

**Bonus Logic**:
1. Check direct position match (e.g., QB in round with QB bonus)
2. Check FLEX eligibility (RB or WR in round with FLEX bonus)
3. Return 0 if no match

**Example**:
```
After team: 110.68
Current round: 0 (first pick)
Player position: RB (FLEX-eligible)
Round 1 config: {FLEX: 50, QB: 25}
Draft bonus: 50 points
After draft bonus: 110.68 + 50 = 160.68
```

---

#### Step 6: Bye Week Penalty
**Purpose**: Penalize players with upcoming bye weeks

**Implementation**: `ScoringEngine.compute_bye_penalty_for_player()`
- Compares player's bye week to current week
- Higher penalty for immediate byes
- Uses configurable penalty schedule

**Configuration**:
```python
BYE_PENALTY = 30  # Default penalty points
```

**Example**:
```
After draft bonus: 160.68
Bye week: Week 7
Current week: 1
Bye penalty: 5 points (far in future)
After bye: 160.68 - 5 = 155.68
```

---

#### Step 7: Injury Penalty
**Purpose**: Penalize players based on injury risk

**Implementation**: `ScoringEngine.compute_injury_penalty()`
- Three risk levels: LOW, MEDIUM, HIGH
- Configurable penalty values

**Configuration**:
```python
INJURY_PENALTIES = {
    "LOW": 0,      # Healthy players
    "MEDIUM": 25,  # Questionable, Day-to-Day
    "HIGH": 50     # Out, IR, Suspended
}
```

**Example**:
```
After bye: 155.68
Injury status: MEDIUM
Injury penalty: 25 points
Final score: 155.68 - 25 = 130.68
```

---

### Trade/Waiver Mode (6-Step Scoring)

Used for trade analysis and waiver wire pickups (no draft round context).

**Steps 1-4**: Identical to Add to Roster Mode
- Step 1: Normalization
- Step 2: ADP Multiplier
- Step 3: Player Ranking Multiplier
- Step 4: Team Ranking Multiplier

**Step 5 REMOVED**: No Draft Order Bonus
- Ensures fair comparison of all players regardless of roster construction
- Prevents bias toward current positional needs

**Steps 5-6 (renumbered from 6-7)**:
- Step 5: Bye Week Penalty (same as Add to Roster)
- Step 6: Injury Penalty (same as Add to Roster, with optional roster exclusion)

**Trade Mode Special Configuration**:
```python
APPLY_INJURY_PENALTY_TO_ROSTER = True   # Apply injury penalties to roster players
APPLY_INJURY_PENALTY_TO_ROSTER = False  # Ignore injury penalties for roster players
```

When `False`, roster players (drafted=2) are evaluated without injury penalties, providing an optimistic view of your current team while still penalizing trade candidates.

---

## Calculator Classes

### NormalizationCalculator
**File**: `draft_helper/core/normalization_calculator.py`

**Purpose**: Provides consistent 0-N scale normalization across all scoring modes

**Key Methods**:
- `normalize_player_score(player_points, max_player_points)` - Core formula
- `calculate_max_player_points(players)` - Finds max from available players
- `normalize_player(player, all_players)` - Convenience method
- `invalidate_cache()` - Called after each draft pick

**Test Coverage**: 22 comprehensive unit tests
- Formula validation across different scales (80, 100, 120)
- Edge cases (zero max, negative values, empty player pools)
- Cache behavior and invalidation
- Fallback logic

**Cache Management**:
- Caches max player points for performance
- Invalidated after draft picks (player pool changes)
- Fallback to 1.0 if no available players found

---

### DraftOrderCalculator
**File**: `draft_helper/core/draft_order_calculator.py`

**Purpose**: Calculates round-based position bonuses using DRAFT_ORDER configuration

**Key Methods**:
- `get_current_draft_round()` - Returns `len(roster)` (0-indexed)
- `calculate_bonus(player)` - Returns bonus points based on current round and position
- `assign_players_to_rounds()` - Maps roster players to rounds for display

**Test Coverage**: 23 comprehensive unit tests
- Round detection (empty roster, partial roster, full roster)
- Bonus calculations for all positions
- FLEX eligibility rules (RB/WR only)
- Roster composition validation

**Round Detection Algorithm**:
```python
current_round = len(roster)  # Simple and accurate
if current_round >= MAX_PLAYERS:
    return None  # Roster full
return current_round  # 0-indexed for DRAFT_ORDER array
```

**Position Matching Logic**:
1. Check direct position match (e.g., QB in round with QB: 50)
2. Check FLEX eligibility (RB or WR in round with FLEX: 50)
3. Return 0 if no match

---

### ScoringEngine
**File**: `draft_helper/core/scoring_engine.py`

**Purpose**: Orchestrates all scoring steps and integrates calculator classes

**Key Methods**:
- `score_player()` - 7-step Add to Roster scoring
- `score_player_for_trade()` - 6-step Trade/Waiver scoring
- `_apply_enhanced_scoring()` - Helper for steps 2-4 (ADP, Rank, Team)
- `compute_bye_penalty_for_player()` - Step 6 (or 5 in trade mode)
- `compute_injury_penalty()` - Step 7 (or 6 in trade mode)

**Integration**:
- Initializes `NormalizationCalculator` and `DraftOrderCalculator`
- Coordinates with `EnhancedScoring`, `TeamDataLoader`, `PositionalRankingCalculator`
- Manages cache invalidation after draft picks

---

## Data Flow Diagrams

### Add to Roster Flow
```
Player Database (CSV)
    ↓
[Load All Players]
    ↓
[Filter Available (drafted=0)]
    ↓
[STEP 1: Normalize (0-100 scale)]
    ↓
[STEP 2: Apply ADP Multiplier]
    ↓
[STEP 3: Apply Player Rank Multiplier]
    ↓
[STEP 4: Apply Team Rank Multiplier]
    ↓
[STEP 5: Add Draft Order Bonus] ← Current round from roster size
    ↓
[STEP 6: Subtract Bye Penalty]
    ↓
[STEP 7: Subtract Injury Penalty]
    ↓
[Sort by Final Score]
    ↓
[Display Top Recommendations]
```

### Trade/Waiver Flow
```
Player Database (CSV)
    ↓
[Load All Players]
    ↓
[Filter Available + Others' Rosters (drafted=0 or 1)]
    ↓
[STEP 1: Normalize (0-100 scale)]
    ↓
[STEP 2: Apply ADP Multiplier]
    ↓
[STEP 3: Apply Player Rank Multiplier]
    ↓
[STEP 4: Apply Team Rank Multiplier]
    ↓
[STEP 5: Subtract Bye Penalty] ← Exclude roster players from roster bye calc
    ↓
[STEP 6: Subtract Injury Penalty] ← Optional exclusion for roster players
    ↓
[Compare with Roster Players]
    ↓
[Identify Trade Improvements]
    ↓
[Sort by Net Gain]
    ↓
[Display Trade Recommendations]
```

---

## Configuration Parameters

### Normalization Settings
```python
NORMALIZATION_MAX_SCALE = 100.0  # Scale for normalized scores (80-120 in simulation)
```

### Draft Order Settings
```python
DRAFT_ORDER_PRIMARY_BONUS = 50    # Primary position bonus points
DRAFT_ORDER_SECONDARY_BONUS = 25  # Secondary position bonus points
DRAFT_ORDER = [...]               # 15 rounds of position priorities with static bonuses
```

### Penalty Settings
```python
INJURY_PENALTIES = {
    "LOW": 0,      # Healthy
    "MEDIUM": 25,  # Questionable
    "HIGH": 50     # Out/IR
}

BYE_WEEK_PENALTY = 30  # Base bye week penalty
```

### Trade Mode Settings
```python
APPLY_INJURY_PENALTY_TO_ROSTER = True   # Apply injury penalties to roster players
MIN_TRADE_IMPROVEMENT = 1               # Minimum points to suggest trade
NUM_TRADE_RUNNERS_UP = 5                # Number of alternative trades to show
```

---

## Key Design Principles

### 1. Modularity
- Separate calculator classes for each scoring component
- Clean separation of concerns
- Easy to test and modify independently

### 2. Mode-Specific Scoring
- Draft mode includes Draft Order Bonus (7 steps)
- Trade mode excludes Draft Order Bonus (6 steps)
- Ensures fair evaluation in each context

### 3. Position Awareness
- FLEX eligibility limited to RB and WR only
- Position-specific bonuses via DRAFT_ORDER
- Position limits enforced by FantasyTeam

### 4. Cache Management
- Normalization caches max player points for performance
- Cache invalidated after each draft pick
- Ensures accurate scoring as player pool changes

### 5. Configurable Strategy
- All parameters configurable via draft_helper_config.py
- Simulation config allows automated optimization
- Easy to adjust for different league rules or preferences

---

## Removed Systems

### Positional Need Scoring (REMOVED)
**Why Removed**: Replaced by DRAFT_ORDER static bonus system
- Old system used complex weight-based calculations
- New system uses simple static point bonuses by round
- More transparent and easier to configure

**Impact**: 33 lines deleted from scoring_engine.py

### Projection-Based Scoring (REMOVED)
**Why Removed**: Replaced by normalization + enhanced scoring
- Old system used raw fantasy points with complex adjustments
- New system normalizes first, then applies multipliers
- Provides consistent baseline across all positions

**Impact**: 64 lines deleted from scoring_engine.py

### Matchup in Draft Mode (REMOVED)
**Why Removed**: Matchup only relevant for weekly lineup decisions
- Matchup analysis moved exclusively to Starter Helper
- Draft decisions should focus on seasonal value
- Trade analysis uses seasonal projections, not weekly matchups

**Impact**: Matchup calculations removed from Add to Roster and Trade modes

### MIN/MAX_TOTAL_ADJUSTMENT (REMOVED)
**Why Removed**: Caps limited the impact of enhanced scoring multipliers
- Old system capped total multipliers to prevent extreme values
- New system applies full multipliers without artificial limits
- More accurate representation of player value differences

**Impact**: Commented out in simulation config

---

## Test Coverage

### Unit Tests
**Total**: 79 comprehensive tests for new scoring system

**NormalizationCalculator** (22 tests):
- Formula validation across scales (80, 100, 120)
- Edge cases (zero max, negative values, empty pools)
- Cache behavior and invalidation
- Fallback to fantasy_points

**DraftOrderCalculator** (23 tests):
- Round detection (empty, partial, full rosters)
- Bonus calculations for all positions
- FLEX eligibility rules
- Roster composition validation

**Updated test_draft_helper.py** (34 tests):
- New 7-step Add to Roster scoring
- New 6-step Trade/Waiver scoring
- DRAFT_ORDER integration
- All penalty systems
- Integration with calculator classes

### Legacy Tests Removed
**test_enhanced_scoring_integration.py** (17 tests removed):
- Tests were for old projection scoring method
- Replaced by 79 new comprehensive tests
- Old tests tested deleted code

### Test Results
**Status**: 582/582 tests passing (100%)

---

## Performance Characteristics

### Normalization Cache
- **Cache hit**: O(1) lookup
- **Cache miss**: O(n) scan of all available players
- **Invalidation**: After each draft pick (roster changes)

### Draft Order Lookup
- **Round detection**: O(1) (simple roster length check)
- **Bonus calculation**: O(1) dictionary lookup
- **Round assignment**: O(n) roster scan for display

### Overall Scoring
- **Add to Roster**: 7 sequential steps, O(n) for all players
- **Trade Analysis**: 6 sequential steps, O(n*m) for n roster × m available players
- **Typical Runtime**: < 5 seconds for full draft recommendation

---

## Future Enhancements

### Potential Additions
1. **Dynamic Bonus Adjustment**: Auto-adjust DRAFT_ORDER bonuses based on roster composition
2. **Positional Scarcity**: Factor remaining available players by position
3. **Schedule Strength**: Consider opponent schedules in normalization
4. **Custom Scoring Formats**: Support for non-PPR leagues with different normalization

### Backward Compatibility
- Legacy wrapper methods maintained in `draft_helper.py`
- `compute_positional_need_score()` now returns DRAFT_ORDER bonus
- `compute_projection_score()` now returns normalized + enhanced score
- Ensures old code continues to work with new system

---

## Conclusion

The scoring overhaul provides a modular, transparent, and highly configurable system for draft recommendations and trade analysis. The separation of concerns between normalization, draft bonuses, and penalties enables independent testing and easy modification of each component.

Key improvements:
- **79 comprehensive tests** (100% passing)
- **Modular calculator classes** (easy to test and modify)
- **Mode-specific scoring** (draft vs trade fairness)
- **Static bonus system** (transparent and configurable)
- **Normalization baseline** (consistent across all positions)

The system is ready for production use with comprehensive test coverage and clear documentation.