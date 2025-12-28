# Sub-Feature 5: ProjectedPointsManager Consolidation

## Objective
Consolidate ProjectedPointsManager functionality into PlayerManager (eliminates ~200 lines of code).

## Dependencies
**Prerequisites:** Sub-feature 2 (Weekly Data Migration)
**Blocks:** None

## Scope (10 items)
- NEW-100 to NEW-109: ProjectedPointsManager consolidation

**From checklist:**
- NEW-100: Add get_projected_points() method to PlayerManager
- NEW-101: Add get_projected_points_array() method to PlayerManager
- NEW-102: Add get_historical_projected_points() method to PlayerManager
- NEW-103: Remove ProjectedPointsManager from PlayerManager.__init__()
- NEW-104: Update player_scoring.py to use PlayerManager methods
- NEW-105: Mark ProjectedPointsManager as deprecated
- NEW-106 to NEW-108: Testing
- NEW-109: Mark players_projected.csv as deprecated

## Key Implementation

**Add to PlayerManager:**
```python
def get_projected_points(self, player: FantasyPlayer, week_num: int) -> Optional[float]:
    """Get original projected points for specific player and week."""
    if week_num < 1 or week_num > 17:
        return None
    if not player.projected_points or len(player.projected_points) < week_num:
        return None
    projected_value = player.projected_points[week_num - 1]
    if projected_value == 0.0:
        return None
    return float(projected_value)
```

**Update caller (player_scoring.py:235):**
```python
# OLD: self.projected_points_manager.get_projected_points(player, week)
# NEW: self.player_manager.get_projected_points(player, week)
```

## Success Criteria
- [ ] 3 methods added to PlayerManager
- [ ] player_scoring.py updated
- [ ] ProjectedPointsManager marked deprecated
- [ ] Performance deviation calculations verified working

See `research/PROJECTED_POINTS_MANAGER_ANALYSIS.md` for complete details.
