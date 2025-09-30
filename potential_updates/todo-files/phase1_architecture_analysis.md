# Phase 1: Architecture Analysis - Scoring System Overhaul

**Date:** 2025-09-29
**Status:** ✅ COMPLETE
**Objective:** Deep analysis of current scoring system to inform refactoring strategy

---

## Executive Summary

The current scoring system has **four distinct scoring contexts** but uses **overlapping logic** that must be separated:

1. **Add to Roster Mode** (Draft Mode) - draft_helper.py
2. **Waiver Optimizer** - draft_helper.py
3. **Trade Simulator** - draft_helper.py
4. **Starter Helper** - starter_helper/starter_helper.py

### Key Findings

| Component | Current State | Required Changes |
|-----------|--------------|------------------|
| **Positional Need** | Position count-based scoring | ❌ **REMOVE ENTIRELY** |
| **DRAFT_ORDER** | Display-only, not connected to scoring | ✅ **IMPLEMENT** as round-based bonus system |
| **Normalization** | None | ✅ **ADD** 0-N scale for seasonal points |
| **Matchup System** | Used in Add to Roster | ❌ **REMOVE** from Add to Roster, ✅ **ADD** to Starter Helper |
| **Injury Penalties** | Same across all modes | ✅ **MODIFY** Starter Helper to zero out non-ACTIVE/QUESTIONABLE |
| **Multiplier Caps** | MIN/MAX_TOTAL_ADJUSTMENT applied | ❌ **REMOVE** all caps |

---

## Current Architecture Deep Dive

### 1. Scoring Engine (draft_helper/core/scoring_engine.py)

**Primary Methods:**
- `score_player()` - Used for Add to Roster and Waiver Optimizer
- `score_player_for_trade()` - Used for Trade Simulator
- `compute_positional_need_score()` - **TO BE REMOVED**
- `compute_projection_score()` - **TO BE REFACTORED**
- `compute_bye_penalty_for_player()` - **KEEP AS-IS**
- `compute_injury_penalty()` - **KEEP AS-IS** (modify for Starter Helper separately)

**Current Calculation Flow (Add to Roster):**
```python
total_score = pos_score + projection_score - bye_penalty - injury_penalty + matchup_adjustment
```

**Key Issues:**
1. ❌ Positional need uses simple position counts, not DRAFT_ORDER
2. ❌ Matchup adjustment applied (should only be in Starter Helper)
3. ❌ No normalization of fantasy points
4. ❌ DRAFT_ORDER infrastructure exists but is NEVER CALLED in scoring

---

### 2. DRAFT_ORDER Configuration (draft_helper/draft_helper_config.py)

**Current Configuration (Lines 48-64):**
```python
DRAFT_ORDER = [
    {FLEX: 1.0, QB: 0.7},    # Round 1
    {FLEX: 1.0, QB: 0.7},    # Round 2
    {FLEX: 1.0, QB: 0.8},    # Round 3
    # ... continues for 15 rounds
]
```

**Critical Issues:**
1. ❌ **SYNTAX ERROR on Line 49**: Missing comma between `FLEX: 1.0` and `QB: 0.7`
2. ❌ Uses weight/multiplier pattern (0.0-2.0 range) instead of static point values
3. ✅ Has infrastructure method `get_next_draft_position_weights()` in FantasyTeam.py
4. ❌ Method is NEVER CALLED in scoring pipeline

**Current Usage:**
- ✅ Display purposes only (roster_manager.py shows "OK" or "!!" indicators)
- ❌ NOT used for scoring decisions
- ❌ Simulation config has `DRAFT_ORDER_WEIGHTS` parameter that doesn't connect to anything

---

### 3. Enhanced Scoring System Integration

**Location:** draft_helper/enhanced_scoring/enhanced_scoring_calculator.py

**Current Integration Points:**
- ADP multipliers (EXCELLENT/GOOD/POOR ranges)
- Player ranking multipliers (EXCELLENT/GOOD/POOR ranges)
- Team ranking multipliers (EXCELLENT/GOOD/POOR ranges)
- **Multiplier caps**: MIN_TOTAL_ADJUSTMENT, MAX_TOTAL_ADJUSTMENT

**Required Changes:**
- ✅ Keep ADP, Player Ranking, Team Ranking multipliers AS-IS
- ❌ Remove MIN/MAX_TOTAL_ADJUSTMENT caps from ALL systems
- ✅ Integrate with new normalization system

---

### 4. Simulation Configuration

**Location:** draft_helper/simulation/config.py

**Current Parameters:**
```python
PARAMETER_RANGES = {
    'DRAFT_ORDER_WEIGHTS': [1.0, 1.2],  # ❌ NOT CONNECTED
    'MAX_TOTAL_ADJUSTMENT': [1.45, 1.50, 1.55],  # ❌ TO BE REMOVED
    'MIN_TOTAL_ADJUSTMENT': [0.65, 0.70, 0.75],  # ❌ TO BE REMOVED
    # ... other parameters
}
```

**Required New Parameters:**
```python
PARAMETER_RANGES = {
    'NORMALIZATION_MAX_SCALE': [80, 100, 120],  # ✅ NEW
    'DRAFT_ORDER_PRIMARY_BONUS': [40, 50, 60],  # ✅ NEW
    'DRAFT_ORDER_SECONDARY_BONUS': [20, 25, 30],  # ✅ NEW
    'MATCHUP_EXCELLENT_MULTIPLIER': [1.15, 1.2, 1.25],  # ✅ NEW
    'MATCHUP_GOOD_MULTIPLIER': [1.05, 1.1, 1.15],  # ✅ NEW
    'MATCHUP_POOR_MULTIPLIER': [0.8, 0.85, 0.9],  # ✅ NEW
}
```

---

### 5. Starter Helper Architecture

**Location:** starter_helper/starter_helper.py

**Current Scoring Method:**
- Uses `LineupOptimizer` class
- Reads weekly projections from CSV `week_N_points` columns
- Applies injury and bye week penalties
- **NO matchup analysis currently** (optional ESPN matchup analysis exists but not integrated into scoring)

**Required Changes:**
1. ✅ Keep current week projection reading (no normalization)
2. ✅ Add matchup multiplier system
3. ✅ Modify injury filtering to zero out non-ACTIVE/QUESTIONABLE players
4. ✅ Apply matchup multipliers ONLY to QB/WR/RB/TE (skip K/DEF)

---

## File Modification Map

### Files Requiring Major Changes

| File | Lines to Modify | Change Type |
|------|----------------|-------------|
| `draft_helper/core/scoring_engine.py` | 39-340 (entire class) | **MAJOR OVERHAUL** |
| `draft_helper/draft_helper_config.py` | 48-64 (DRAFT_ORDER) | **SYNTAX FIX + VALUE UPDATE** |
| `draft_helper/simulation/config.py` | 13-37 (PARAMETER_RANGES) | **ADD NEW PARAMETERS** |
| `starter_helper/starter_helper.py` | TBD (scoring method) | **ADD MATCHUP SYSTEM** |
| `starter_helper/lineup_optimizer.py` | TBD (penalty method) | **MODIFY INJURY FILTERING** |

### Files Requiring Minor Changes

| File | Change Type |
|------|------------|
| `draft_helper/FantasyTeam.py` | Add round tracking system |
| `draft_helper/enhanced_scoring/enhanced_scoring_calculator.py` | Remove multiplier caps |
| All test files | Update assertions to match new behavior |

### Files Requiring New Creation

| File | Purpose |
|------|---------|
| `draft_helper/core/normalization_calculator.py` | Normalize fantasy points 0-N scale |
| `draft_helper/core/draft_order_calculator.py` | Calculate DRAFT_ORDER bonuses |
| `starter_helper/matchup_calculator.py` | Calculate matchup multipliers |
| `tests/test_normalization_calculator.py` | Unit tests for normalization |
| `tests/test_draft_order_calculator.py` | Unit tests for DRAFT_ORDER |
| `tests/test_matchup_calculator.py` | Unit tests for matchup system |

---

## Target Scoring Formulas

### Add to Roster Mode (7 Steps)
```python
1. normalized_score = (player_points / max_player_points) * NORMALIZATION_MAX_SCALE
2. adp_multiplied_score = normalized_score * adp_multiplier
3. player_rank_multiplied_score = adp_multiplied_score * player_rank_multiplier
4. team_rank_multiplied_score = player_rank_multiplied_score * team_rank_multiplier
5. draft_bonus_score = team_rank_multiplied_score + draft_order_bonus
6. bye_adjusted_score = draft_bonus_score - bye_week_penalty
7. final_score = bye_adjusted_score - injury_penalty
```

### Waiver Optimizer (6 Steps)
```python
# Same as Add to Roster but skip step 5 (no DRAFT_ORDER bonus)
1-4: Same as Add to Roster
5: bye_adjusted_score = team_rank_multiplied_score - bye_week_penalty
6: final_score = bye_adjusted_score - injury_penalty
```

### Trade Simulator (6 Steps)
```python
# Same as Waiver Optimizer (no DRAFT_ORDER bonus)
```

### Starter Helper (3 Steps)
```python
1. base_score = week_N_projected_points  # No normalization
2. matchup_adjusted_score = base_score * matchup_multiplier  # Only for QB/WR/RB/TE
3. final_score = 0 if injury_status not in [ACTIVE, QUESTIONABLE] else matchup_adjusted_score
```

---

## Critical Implementation Details

### 1. Normalization System

**Formula:**
```python
normalized_score = (player_points / max_player_points) * normalization_scale

# Example with scale=100:
# Player A: 350 points (max) → 100
# Player B: 175 points (half) → 50
# Player C: 70 points (20%) → 20
```

**Configuration:**
- Default scale: 100
- Configurable via simulation: [80, 100, 120]
- Uses seasonal total projected fantasy points as base

---

### 2. DRAFT_ORDER Round-Based Bonus

**New Structure:**
```python
DRAFT_ORDER = [
    {FLEX: 50, QB: 25},  # Round 1: FLEX gets 50 bonus pts, QB gets 25
    {FLEX: 50, QB: 25},  # Round 2: Same priorities
    {FLEX: 50, QB: 30},  # Round 3: QB priority increasing
    {FLEX: 50, QB: 30},  # Round 4
    {QB: 50, FLEX: 25},  # Round 5: QB now primary
    {TE: 50, FLEX: 25},  # Round 6: TE primary
    {FLEX: 50},          # Round 7: FLEX only
    {QB: 50, FLEX: 25},  # Round 8: QB primary
    {TE: 50, FLEX: 25},  # Round 9: TE primary
    {FLEX: 50},          # Round 10-11: FLEX only
    {FLEX: 50},
    {K: 50},             # Round 12: K
    {DST: 50},           # Round 13: DST
    {FLEX: 50},          # Round 14-15: FLEX
    {FLEX: 50}
]
```

**Bonus Calculation:**
```python
# Get current draft round (first unfilled slot)
current_round = count of roster players

# Get DRAFT_ORDER dictionary for that round
round_priorities = DRAFT_ORDER[current_round]

# Check if player's position is in priorities
if player.position in round_priorities:
    bonus = round_priorities[player.position]
elif player.position in FLEX_ELIGIBLE and FLEX in round_priorities:
    bonus = round_priorities[FLEX]
else:
    bonus = 0
```

---

### 3. Round Tracking System

**Algorithm (from clarification questions):**
```python
# Assign roster players to rounds
for player in roster:
    for round_num in range(1, MAX_PLAYERS + 1):
        if round_assignments[round_num] is None:  # Round not assigned
            round_priorities = DRAFT_ORDER[round_num - 1]
            highest_priority_position = max(round_priorities, key=round_priorities.get)

            if player.position == highest_priority_position or \
               (player.position in FLEX_ELIGIBLE and highest_priority_position == FLEX):
                # Assign player to this round
                round_assignments[round_num] = player
                break

# Current round = first unassigned round
current_round = next unassigned round number
```

**Important Notes:**
- Assignment order doesn't matter (just fill slots)
- Roster composition MUST align with DRAFT_ORDER position expectations
- Unit tests should verify this alignment

---

### 4. Matchup Multiplier System (Starter Helper Only)

**Formula:**
```python
rank_diff = opponent_defense_rank - player_team_offense_rank

# Positive diff = favorable matchup (weak defense vs strong offense)
# Negative diff = unfavorable matchup (strong defense vs weak offense)

# Multiplier ranges:
if rank_diff < -15:
    multiplier = 0.8x  # Very unfavorable
elif -15 <= rank_diff < -6:
    multiplier = 0.9x  # Unfavorable
elif -5 <= rank_diff <= 5:
    multiplier = 1.0x  # Neutral
elif 6 <= rank_diff <= 15:
    multiplier = 1.1x  # Favorable
else:  # rank_diff > 15
    multiplier = 1.2x  # Very favorable
```

**Application:**
- ✅ Apply to: QB, WR, RB, TE
- ❌ Skip: K, DEF

---

## Dependencies and Integration Points

### Enhanced Scoring System (Existing - Keep Integration)
- **Location:** `draft_helper/enhanced_scoring/`
- **Components:**
  - `enhanced_scoring_calculator.py` - Main calculator
  - `team_data_loader.py` - Team rankings
  - `positional_ranking_calculator.py` - Position-specific adjustments
- **Integration:** All three scoring modes use enhanced scoring AFTER normalization

### Week-by-Week Projection System (Existing - Keep Integration)
- **Location:** Shared files, fantasy_points_calculator.py
- **Usage:**
  - Draft modes use seasonal total
  - Starter Helper uses week-specific columns
- **No changes required**

### Bye Week System (Existing - Keep As-Is)
- **Location:** `shared_files/bye_weeks.csv`
- **Usage:** All modes apply bye week penalties
- **No changes required**

### Injury Status System (Existing - Modify for Starter Helper)
- **Current:** Penalty-based (LOW=0, MEDIUM=15, HIGH=35)
- **New (Starter Helper only):** Binary (ACTIVE/QUESTIONABLE=keep score, else=0)

---

## Risk Assessment

### High Risk Areas

1. **Breaking Changes to Scoring Logic**
   - **Risk:** Existing drafts/trades may score differently
   - **Mitigation:** Comprehensive unit tests, step-by-step validation

2. **DRAFT_ORDER Syntax Error**
   - **Risk:** Config currently has syntax error (line 49)
   - **Mitigation:** Fix immediately in Phase 2

3. **Round Tracking Algorithm Complexity**
   - **Risk:** Complex assignment logic may have edge cases
   - **Mitigation:** Liberal unit testing as requested

4. **Starter Helper Integration**
   - **Risk:** Separate codebase, may have different patterns
   - **Mitigation:** Create standalone matchup calculator module

### Medium Risk Areas

1. **Simulation Parameter Changes**
   - **Risk:** Removing old parameters may break simulation runs
   - **Mitigation:** Update simulation config before removing from main config

2. **Test Suite Updates**
   - **Risk:** 241 existing tests may fail with new behavior
   - **Mitigation:** Update tests incrementally as we modify each component

### Low Risk Areas

1. **Enhanced Scoring Integration**
   - Already well-tested and modular
   - Just need to apply after normalization instead of before

2. **Bye Week/Injury Penalties**
   - Keep existing logic mostly as-is
   - Only modify injury filtering for Starter Helper

---

## Next Steps (Phase 2)

1. ✅ Create backup branch
2. ✅ Fix DRAFT_ORDER syntax error (line 49)
3. ✅ Update DRAFT_ORDER to static point values
4. ✅ Add new simulation config parameters
5. ✅ Add round tracking mechanism
6. ✅ Validate all configuration changes

---

## Clarification Notes

All clarification questions have been answered. Key decisions:

- **Normalization:** Both scale and max value configurable (formula confirmed)
- **DRAFT_ORDER values:** Start at 50 for #1 positions, configurable via simulation
- **Round assignment:** Order doesn't matter, just fill slots by position
- **Matchup formula:** `(opponent_def_rank - team_off_rank)` for positive=favorable
- **Injury filtering:** Zero out non-ACTIVE/QUESTIONABLE in Starter Helper only
- **Backwards compatibility:** Clean break acceptable, no migration needed
- **Testing approach:** Liberal unit tests with extensive logging (as requested)

---

**Analysis Complete:** Ready to proceed to Phase 2 (Configuration System Updates)

**Session Notes:** All major architectural decisions mapped. No blockers identified. Syntax error in config file is critical but easily fixed. Round tracking algorithm is most complex new feature but well-defined by user clarifications.