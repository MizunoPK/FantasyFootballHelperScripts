# Simulation System Fixes - Summary

**Date**: 2025-10-16
**Purpose**: Fix two critical issues in the simulation system that prevented proper testing of scoring parameters

---

## Issue 1: Performance Scoring Not Enabled in Draft Mode

### Problem
The `AddToRosterModeManager.get_recommendations()` method was only calling `score_player()` with `adp=True`, which meant:
- ADP_SCORING_WEIGHT was the only multiplier being tested
- PERFORMANCE_SCORING_WEIGHT, PLAYER_RATING_SCORING_WEIGHT, TEAM_QUALITY_SCORING_WEIGHT, and MATCHUP_SCORING_WEIGHT had **no effect** on simulations
- The simulation was not properly testing the full scoring algorithm

### Root Cause
**File**: `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
**Line**: 225

**Original Code**:
```python
scored_player = self.player_manager.score_player(p, draft_round=current_round, adp=True)
```

### Fix Applied
**Updated Code**:
```python
scored_player = self.player_manager.score_player(
    p,
    draft_round=current_round,
    adp=True,
    player_rating=True,
    team_quality=True,
    performance=True,
    matchup=True
)
```

### Impact
Now all scoring multipliers are properly enabled during draft simulations:
1. **ADP_SCORING**: Market wisdom adjustment (was working)
2. **PLAYER_RATING_SCORING**: Expert consensus (now enabled)
3. **TEAM_QUALITY_SCORING**: Offensive/defensive strength (now enabled)
4. **PERFORMANCE_SCORING**: Actual vs projected deviation (now enabled)
5. **MATCHUP_SCORING**: Opponent strength (now enabled)

Each multiplier's WEIGHT parameter will now be properly tested:
- WEIGHT=0.0 → multiplier = 1.0 (no effect)
- WEIGHT=1.0 → multiplier = 1.025 (2.5% boost for GOOD rating)
- WEIGHT=2.0 → multiplier = 1.050625 (5.06% boost for GOOD rating)
- WEIGHT=5.0 → multiplier = 1.1314 (13.14% boost for GOOD rating)

The simulation generates 6 values per WEIGHT parameter (baseline + 5 random variations) and tests each across 100+ simulations.

---

## Issue 2: Draft Phase Using Wrong NFL Week

### Problem
The draft simulation was using `CURRENT_NFL_WEEK = 6` from the baseline config, which meant:
- Performance scoring during draft used weeks 1-5 historical data
- This is **incorrect** - the draft should occur at week 1 with NO performance history
- Players were being evaluated with 5 weeks of actual performance data during the draft
- This artificially biased draft decisions based on future information

### Root Cause
**File**: `simulation/SimulatedLeague.py`
**Method**: `run_draft()`
**Line**: 217

The method never updated `current_nfl_week` before starting the draft, so all teams used the baseline config value (week 6).

### Fix Applied
**Location**: `simulation/SimulatedLeague.py` line 221-224

**Added Code**:
```python
# Set all teams to week 1 for draft (no performance history yet)
for team in self.teams:
    team.config.current_nfl_week = 1
self.logger.debug("Set all teams to week 1 for draft (no performance history)")
```

### Impact
Now the simulation correctly handles NFL weeks:

**Draft Phase (Week 1)**:
- `current_nfl_week = 1`
- Performance scoring requires `MIN_WEEKS = 3`, so no performance data is available
- Draft decisions based purely on projections, ADP, player ratings, team quality, and matchups
- This is realistic - drafts happen before the season starts

**Match Simulations (Weeks 1-17)**:
- Each week, `DraftHelperTeam.set_weekly_lineup(week)` updates `config.current_nfl_week = week`
- Week 1: No performance data (< 3 weeks)
- Week 2: No performance data (< 3 weeks)
- Week 3: No performance data (< 3 weeks)
- Week 4+: Performance scoring uses weeks 1 through (current_week - 1)
- Week 17: Performance scoring uses weeks 1-16 (full season history)

### Verification
The simulation now properly isolates different phases:
1. **Draft**: Week 1, no performance history
2. **Early season (weeks 1-3)**: Cumulative weeks 1-2, still < 3 weeks (no performance scoring)
3. **Mid/late season (weeks 4-17)**: Full performance history up to previous week

---

## Testing Verification

### ConfigGenerator
✅ Properly includes all WEIGHT parameters:
- Line 46-50: Defines WEIGHT ranges for all 5 scoring sections
- Line 54-60: Lists all SCORING_SECTIONS including PERFORMANCE_SCORING
- Line 234: Generates PERFORMANCE_SCORING_WEIGHT variations
- Line 399-400: Applies WEIGHT to config multipliers

### ConfigManager
✅ Properly applies WEIGHT as exponent:
- Line 105: `multiplier = multiplier ** scoring_dict[self.keys.WEIGHT]`
- Line 120-121: `get_performance_multiplier()` calls `_get_multiplier()`
- This raises base multipliers (0.95, 0.975, 1.025, 1.05) to the WEIGHT power

### PlayerManager
✅ Properly calls performance scoring:
- Line 226: `score_player()` method signature includes `performance=False` parameter
- Line 285-288: Step 5 applies performance multiplier when enabled
- Line 353-387: `_apply_performance_multiplier()` calculates deviation and gets multiplier

### Simulation Flow
✅ Now correctly sequences:
1. Draft at week 1 (no performance data)
2. Season weeks 1-17 (cumulative performance data)
3. All 5 multiplier WEIGHTs properly tested

---

## Expected Results

After these fixes, the simulation will properly test all scoring parameters:

### Parameters Tested Per Configuration
- NORMALIZATION_MAX_SCALE
- BASE_BYE_PENALTY
- PRIMARY_BONUS
- SECONDARY_BONUS
- ADP_SCORING_WEIGHT
- PLAYER_RATING_SCORING_WEIGHT
- TEAM_QUALITY_SCORING_WEIGHT
- **PERFORMANCE_SCORING_WEIGHT** (now properly enabled)
- MATCHUP_SCORING_WEIGHT

### Simulation Coverage
- Full optimization: `(num_test_values + 1)^9` configurations
- Iterative optimization: `9 parameters × 6 values = 54 configurations`
- Each config tested across 100+ simulations
- Each simulation includes draft + 17-week season

### Validation
To verify the fixes are working:
1. Run simulation with `PERFORMANCE_SCORING_WEIGHT` variations
2. Check that different WEIGHT values produce different win rates
3. Verify draft decisions don't use future performance data
4. Confirm week 1-3 matches don't use performance scoring
5. Confirm week 4+ matches properly use performance scoring

---

## Files Modified

1. **league_helper/add_to_roster_mode/AddToRosterModeManager.py**
   - Line 225-233: Enable all scoring multipliers in draft recommendations

2. **simulation/SimulatedLeague.py**
   - Line 221-224: Set all teams to week 1 before draft

---

## Next Steps

1. ✅ Fixes applied and documented
2. ⏳ Run simulation to verify PERFORMANCE_SCORING_WEIGHT has impact
3. ⏳ Compare results before/after fixes to measure impact
4. ⏳ Potentially re-run parameter optimization with proper scoring enabled

---

**Status**: Fixes applied, ready for testing
