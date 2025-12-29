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

## Verification Findings (From Deep Dive)

### Current Usage Locations

**PlayerManager.__init__() (line 113):**
```python
self.projected_points_manager = ProjectedPointsManager(config, data_folder)
```
**Action:** Remove this instantiation and import (line 43)

**player_scoring.py usage:**
- **Line 53, 65, 77, 86:** Type hints and docstrings reference ProjectedPointsManager
- **Line 235:** `projected_points = self.projected_points_manager.get_projected_points(player, week)`

**Update required:**
- Remove ProjectedPointsManager references from type hints/docstrings
- Change line 235 to use `self.player_manager.get_projected_points(player, week)`

### Rationale for Consolidation

**PlayerManager already has the data:**
- Sub-feature 1 loads projected_points arrays from JSON into FantasyPlayer objects
- PlayerManager.players contains all players with projected_points
- No need for separate class to reload same data

**Complexity reduction:**
- ProjectedPointsManager: ~200 lines with CSV loading logic
- New approach: ~25 lines in PlayerManager (simple array access)
- **Savings:** ~175 lines of obsolete code eliminated

**Single caller:**
- Only player_scoring.py uses ProjectedPointsManager
- Simple update: change self.projected_points_manager → self.player_manager

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
