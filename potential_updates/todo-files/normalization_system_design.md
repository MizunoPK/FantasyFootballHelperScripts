# Normalization System Design

**Purpose:** Scale seasonal fantasy points to 0-N range for consistent scoring across all draft modes

**Date:** 2025-09-29
**Status:** DESIGN PHASE

---

## Overview

The normalization system converts raw seasonal fantasy points into a consistent 0-N scale where N is configurable. This provides:

1. **Consistent baseline** across all draft modes (Add to Roster, Waiver, Trade)
2. **Configurable scale** for simulation optimization
3. **Fair comparison** between players regardless of absolute point values
4. **Integration point** for enhanced scoring multipliers

---

## Formula

```python
normalized_score = (player_points / max_player_points) * normalization_scale
```

**Where:**
- `player_points` = Seasonal total projected fantasy points for the player
- `max_player_points` = Highest seasonal total among all available players
- `normalization_scale` = Configurable max value (default: 100)

---

## Examples

### Example 1: Default Scale (100)

```python
normalization_scale = 100
max_player_points = 350  # Best player in pool

# Player A (best player):
normalized_score = (350 / 350) * 100 = 100.0

# Player B (half as good):
normalized_score = (175 / 350) * 100 = 50.0

# Player C (20% as good):
normalized_score = (70 / 350) * 100 = 20.0
```

### Example 2: Scale = 80

```python
normalization_scale = 80
max_player_points = 350

# Player A (best player):
normalized_score = (350 / 350) * 80 = 80.0

# Player B (half as good):
normalized_score = (175 / 350) * 80 = 40.0

# Player C (20% as good):
normalized_score = (70 / 350) * 80 = 16.0
```

### Example 3: Scale = 120

```python
normalization_scale = 120
max_player_points = 350

# Player A (best player):
normalized_score = (350 / 350) * 120 = 120.0

# Player B (half as good):
normalized_score = (175 / 350) * 120 = 60.0

# Player C (20% as good):
normalized_score = (70 / 350) * 120 = 24.0
```

---

## Implementation Design

### Class Structure

```python
class NormalizationCalculator:
    """
    Calculates normalized fantasy points for players on 0-N scale.

    The normalization scale is configurable for simulation optimization.
    """

    def __init__(self, normalization_scale: float = 100.0, logger=None):
        """
        Initialize the normalization calculator.

        Args:
            normalization_scale: Maximum value for normalized scores (default: 100.0)
            logger: Logger instance for debugging
        """
        self.normalization_scale = normalization_scale
        self.logger = logger or logging.getLogger(__name__)
        self._max_player_points_cache = None

    def calculate_max_player_points(self, players: List[FantasyPlayer]) -> float:
        """
        Find the maximum seasonal fantasy points among all players.

        Args:
            players: List of all players to consider

        Returns:
            float: Maximum seasonal fantasy points value
        """
        # Filter to available players only (drafted=0)
        available_players = [p for p in players if p.drafted == 0]

        if not available_players:
            self.logger.warning("No available players found for normalization")
            return 1.0  # Avoid division by zero

        # Find max using remaining_season_projection if available, else fantasy_points
        max_points = max(
            getattr(p, 'remaining_season_projection', None) or p.fantasy_points
            for p in available_players
        )

        self.logger.debug(f"Maximum player points for normalization: {max_points:.1f}")
        return max_points

    def normalize_player_score(
        self,
        player_points: float,
        max_player_points: float
    ) -> float:
        """
        Normalize a player's fantasy points to 0-N scale.

        Args:
            player_points: Player's seasonal fantasy points
            max_player_points: Maximum points among all players

        Returns:
            float: Normalized score on 0-N scale
        """
        if max_player_points <= 0:
            self.logger.warning("Invalid max_player_points, returning 0")
            return 0.0

        normalized = (player_points / max_player_points) * self.normalization_scale

        self.logger.debug(
            f"Normalized: {player_points:.1f} / {max_player_points:.1f} * {self.normalization_scale} = {normalized:.2f}"
        )

        return normalized

    def normalize_player(
        self,
        player: FantasyPlayer,
        all_players: List[FantasyPlayer]
    ) -> float:
        """
        Convenience method to normalize a player using the full player pool.

        Args:
            player: Player to normalize
            all_players: All players for finding max

        Returns:
            float: Normalized score on 0-N scale
        """
        # Get player's points (prefer remaining_season_projection)
        player_points = (
            getattr(player, 'remaining_season_projection', None) or
            player.fantasy_points
        )

        # Calculate or use cached max
        if self._max_player_points_cache is None:
            self._max_player_points_cache = self.calculate_max_player_points(all_players)

        max_points = self._max_player_points_cache

        return self.normalize_player_score(player_points, max_points)

    def invalidate_cache(self):
        """
        Invalidate the cached max player points.

        Call this when the player pool changes (e.g., after a draft pick).
        """
        self._max_player_points_cache = None
        self.logger.debug("Max player points cache invalidated")
```

---

## Integration Points

### 1. Add to Roster Mode

```python
# Step 1 of 7-step calculation
normalized_score = normalization_calculator.normalize_player(player, all_players)

# Continue with steps 2-7 (ADP, Player Rank, Team Rank, Draft Order, Bye, Injury)
```

### 2. Waiver Optimizer

```python
# Step 1 of 6-step calculation (same as Add to Roster)
normalized_score = normalization_calculator.normalize_player(player, all_players)

# Continue with steps 2-6 (no Draft Order bonus)
```

### 3. Trade Simulator

```python
# Step 1 of 6-step calculation (same as Waiver Optimizer)
normalized_score = normalization_calculator.normalize_player(player, all_players)

# Continue with steps 2-6 (no Draft Order bonus)
```

### 4. Starter Helper

```python
# NO NORMALIZATION - uses raw week-specific points
base_score = player.week_N_points  # No normalization
```

---

## Configuration

### Main Config (draft_helper/draft_helper_config.py)

**NEW CONSTANT:**
```python
# Normalization scale for fantasy points (default: 100)
NORMALIZATION_MAX_SCALE = 100.0
```

### Simulation Config (draft_helper/simulation/config.py)

**NEW PARAMETER RANGE:**
```python
PARAMETER_RANGES = {
    'NORMALIZATION_MAX_SCALE': [80, 100, 120],  # Test different scale values
    # ... existing parameters
}
```

---

## Edge Cases and Error Handling

### Edge Case 1: No Available Players

```python
if not available_players:
    return 1.0  # Avoid division by zero
```

**Scenario:** All players drafted (edge of draft)
**Handling:** Return 1.0 to prevent division by zero
**Result:** Normalized score will equal player_points

### Edge Case 2: Zero Max Points

```python
if max_player_points <= 0:
    return 0.0
```

**Scenario:** All players have 0 or negative points (data error)
**Handling:** Return 0.0
**Result:** All players score 0

### Edge Case 3: Player Points Exceed Max

```python
# No special handling needed - can exceed 100% if player improves
normalized = (player_points / max_player_points) * scale
```

**Scenario:** Player's projection updated after max calculated
**Handling:** Allow values > scale
**Result:** Player can score > 100 if they become the new best

### Edge Case 4: Cache Invalidation

```python
# After each draft pick:
normalization_calculator.invalidate_cache()
```

**Scenario:** Max player drafted, new max needed
**Handling:** Cache invalidation forces recalculation
**Result:** Normalized scores update with new pool

---

## Performance Considerations

### Optimization 1: Caching Max Value

```python
self._max_player_points_cache = None  # Cache the max
```

**Benefit:** Avoid recalculating max for every player in recommendation loop
**Invalidation:** Call `invalidate_cache()` after draft picks

### Optimization 2: Single Pass for Max

```python
max_points = max(p.fantasy_points for p in available_players)
```

**Benefit:** O(n) single pass through players
**Complexity:** Linear time with player count

---

## Logging Strategy

### Debug Logging (Detailed)

```python
self.logger.debug(f"Maximum player points for normalization: {max_points:.1f}")
self.logger.debug(f"Normalized: {player_points:.1f} / {max_points:.1f} * {scale} = {normalized:.2f}")
```

### Info Logging (Key Operations)

```python
self.logger.info(f"Normalization scale set to: {self.normalization_scale}")
self.logger.info(f"Cache invalidated after draft pick")
```

### Warning Logging (Issues)

```python
self.logger.warning("No available players found for normalization")
self.logger.warning("Invalid max_player_points, returning 0")
```

---

## Testing Strategy

### Unit Test 1: Basic Normalization

```python
def test_normalize_basic_scale_100():
    """Test normalization with default scale of 100"""
    calc = NormalizationCalculator(normalization_scale=100.0)

    # Max player: 350 points
    # Test player: 175 points (50%)
    normalized = calc.normalize_player_score(175.0, 350.0)

    assert normalized == 50.0  # 50% of scale
```

### Unit Test 2: Different Scales

```python
def test_normalize_scale_80():
    """Test normalization with scale of 80"""
    calc = NormalizationCalculator(normalization_scale=80.0)

    normalized = calc.normalize_player_score(175.0, 350.0)
    assert normalized == 40.0  # 50% of 80

def test_normalize_scale_120():
    """Test normalization with scale of 120"""
    calc = NormalizationCalculator(normalization_scale=120.0)

    normalized = calc.normalize_player_score(175.0, 350.0)
    assert normalized == 60.0  # 50% of 120
```

### Unit Test 3: Edge Cases

```python
def test_normalize_zero_max_points():
    """Test handling of zero max points"""
    calc = NormalizationCalculator()
    normalized = calc.normalize_player_score(100.0, 0.0)
    assert normalized == 0.0

def test_normalize_no_available_players():
    """Test handling when no players available"""
    calc = NormalizationCalculator()
    players = [FantasyPlayer(drafted=2), FantasyPlayer(drafted=1)]  # All drafted
    max_points = calc.calculate_max_player_points(players)
    assert max_points == 1.0  # Fallback value
```

### Unit Test 4: Cache Behavior

```python
def test_cache_invalidation():
    """Test that cache invalidation works correctly"""
    calc = NormalizationCalculator()
    players = [FantasyPlayer(fantasy_points=100, drafted=0)]

    # First call caches max
    calc.normalize_player(players[0], players)
    assert calc._max_player_points_cache == 100.0

    # Invalidate cache
    calc.invalidate_cache()
    assert calc._max_player_points_cache is None
```

### Integration Test: Full Scoring Pipeline

```python
def test_normalization_in_scoring_pipeline():
    """Test normalization as first step in scoring"""
    players = [
        FantasyPlayer(name="Player A", fantasy_points=350, drafted=0),
        FantasyPlayer(name="Player B", fantasy_points=175, drafted=0),
        FantasyPlayer(name="Player C", fantasy_points=70, drafted=0),
    ]

    calc = NormalizationCalculator(normalization_scale=100.0)

    scores = [calc.normalize_player(p, players) for p in players]

    assert scores[0] == 100.0  # Best player
    assert scores[1] == 50.0   # Half as good
    assert scores[2] == 20.0   # 20% as good
```

---

## File Structure

**Location:** `draft_helper/core/normalization_calculator.py`

**Dependencies:**
- `shared_files/FantasyPlayer.py` - Player data model
- `logging` - Standard library
- `typing` - Type hints

**Imported By:**
- `draft_helper/core/scoring_engine.py` - Main scoring calculations
- Test files

---

## Migration Notes

### Before Normalization

```python
# Old scoring (Add to Roster):
base_score = player.remaining_season_projection  # Raw points (0-400 range)
```

### After Normalization

```python
# New scoring (Add to Roster):
normalized_score = normalization_calculator.normalize_player(player, all_players)  # 0-100 range
```

### Impact on Scores

**Example:**
- **Before:** Player with 300 pts gets 300 base score → ~600 after multipliers
- **After:** Player with 300 pts gets ~86 normalized → ~172 after multipliers (if max=350)

**Mitigation:** All scores scale proportionally, so rankings remain consistent

---

## Design Complete

**Next Steps:**
1. Implement `NormalizationCalculator` class
2. Write comprehensive unit tests
3. Integrate into `ScoringEngine`
4. Update simulation config
5. Validate with integration tests

**Design Approved:** Ready for implementation in Phase 3