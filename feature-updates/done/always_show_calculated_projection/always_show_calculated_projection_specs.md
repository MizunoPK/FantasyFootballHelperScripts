# Always Show Calculated Projection - Specification

## Objective

Enable all player display methods (`__str__`, print statements) to show the **raw/un-normalized projected fantasy points** so users can see actual expected points rather than just weighted ranking scores.

---

## High-Level Requirements

### 1. Player String Representations

Update `__str__` methods to display raw projected points:

**Current Format (FantasyPlayer):**
```
Patrick Mahomes (KC QB) - 15.3 pts [Bye=7] [ROSTERED]
```

**Proposed Format:**
```
Patrick Mahomes (KC QB) - Proj: 320.5 pts, Score: 15.3 [Bye=7] [ROSTERED]
```

### 2. ScoredPlayer Display

Update `ScoredPlayer.__str__()` to show projection:

**Current Format:**
```
[QB] [KC] Patrick Mahomes - 123.45 pts (Bye=7)
```

**Proposed Format:**
```
[QB] [KC] Patrick Mahomes - Proj: 320.5 pts, Score: 123.45 (Bye=7)
```

### 3. Scoring Method Returns

(Pending) - Determine if `score_player()` should return additional values.

---

## Current Architecture

### String Representation Methods

**1. FantasyPlayer.__str__()** - `utils/FantasyPlayer.py:380-400`
```python
def __str__(self) -> str:
    # ...
    return f"{self.name} ({self.team} {self.position}) - {self.score:.1f} pts {status} [Bye={self.bye_week}] [{drafted}]{locked_indicator}"
```

**2. ScoredPlayer.__str__()** - `league_helper/util/ScoredPlayer.py:64-89`
```python
def __str__(self) -> str:
    header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.score:.2f} pts (Bye={self.player.bye_week})"
    lines = [header]
    for reason in self.reason:
        lines.append(f"            - {reason}")
    return "\n".join(lines)
```

### Where Projections Are Available

**FantasyPlayer fields:**
- `fantasy_points` (float) - Total season projected points (sum of weeks 1-17)
- `week_N_points` (Optional[float]) - Individual week projections (weeks 1-17)
- `score` (float) - Weighted/normalized ranking score
- `weighted_projection` (float) - Normalized projection value

**Methods:**
- `get_weekly_projections()` - Returns list of all 17 weekly values
- `get_single_weekly_projection(week_num)` - Returns specific week's projection
- `get_total_projection()` - Returns sum of non-None weekly values

### Where Raw Projection IS Currently Shown

**1. player_scoring.py:474** - First scoring reason:
```python
reason = f"Projected: {orig_pts:.2f} pts, Weighted: {weighted_pts:.2f} pts"
```

**2. StarterHelperModeManager.py:349** - Lineup total:
```python
total_raw_projected = lineup.get_total_raw_projected_points(self.config.current_nfl_week)
print(f"COMBINED PROJECTED POINTS: {total_raw_projected:.1f} pts")
```

### Files That Print Players

| File | Lines | What's Printed |
|------|-------|----------------|
| `AddToRosterModeManager.py` | 357 | `{player.fantasy_points:.1f} pts` |
| `StarterHelperModeManager.py` | 524 | `{recommendation}` (ScoredPlayer.__str__) |
| `TradeSimulatorModeManager.py` | 378, 545-574 | `{player}` (ScoredPlayer.__str__) |
| `PlayerManager.py` | 491, 533 | Various player displays |
| `trade_display_helper.py` | 241-274 | `{player}` (ScoredPlayer.__str__) |
| `player_search.py` | 181 | `{player}` (FantasyPlayer.__str__) |
| `ModifyPlayerDataModeManager.py` | 362 | `{player.name}` only |

---

## Resolved Implementation Details

### Q1: Which Projection Value to Show?
**Decision:** Context-dependent - use whatever projection the scoring method used (ROS or single-week). Return the calculated fantasy points as part of the ScoredPlayer object.

### Q2: Display Format
**Decision:** Projection primary with score secondary.
```
[QB] [KC] Patrick Mahomes - 18.5 pts (Score: 123.45) (Bye=7)
```

### Q3: Which __str__ Methods Need Updating?
**Decision:** ScoredPlayer only (`league_helper/util/ScoredPlayer.py`). FantasyPlayer.__str__() unchanged since it doesn't have scored context.

### Q4: Scoring Method Return Values
**Decision:** Add `projected_points` field to ScoredPlayer to hold the calculated projection value used in scoring.

### Q5: AddToRosterMode Display
**Decision:** Leave as-is. Already shows raw projection (`fantasy_points`) and serves a different purpose than scored recommendations.

### Q6: Starter Helper Mode
**Decision:** No additional changes. ScoredPlayer.__str__() update applies automatically to individual player displays.

---

## Implementation Notes

### Files to Modify

1. **`utils/FantasyPlayer.py`**
   - Update `__str__()` method to include projection

2. **`league_helper/util/ScoredPlayer.py`**
   - Update `__str__()` method to include projection
   - Possibly add `projected_points` field

3. **`league_helper/util/player_scoring.py`**
   - Possibly update to populate projection field in ScoredPlayer

### Dependencies

- No new external dependencies
- Internal changes only

### Testing Strategy

- Verify string output format in existing tests
- Add tests for new projection display
- Run all 2200+ tests to ensure no regressions

---

## Status: READY FOR IMPLEMENTATION
