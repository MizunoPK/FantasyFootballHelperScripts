#!/usr/bin/env python3
"""
Unit tests for NormalizationCalculator

Tests normalization of fantasy points to 0-N scale with various configurations.

Author: Kai Mizuno
Last Updated: September 2025
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from draft_helper.core.normalization_calculator import NormalizationCalculator
from shared_files.FantasyPlayer import FantasyPlayer


class TestNormalizationCalculator:
    """Test suite for NormalizationCalculator"""

    def create_test_player(self, name: str, points: float, drafted: int = 0):
        """Helper to create test players"""
        player = FantasyPlayer(
            id=hash(name) % 10000,
            name=name,
            position='RB',
            team='TEST',
            fantasy_points=points,
            drafted=drafted
        )
        # Set remaining_season_projection for tests
        player.remaining_season_projection = points
        return player

    # =============================================================================
    # Basic Normalization Tests
    # =============================================================================

    def test_normalize_basic_scale_100(self):
        """Test normalization with default scale of 100"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        # Max player: 350 points
        # Test player: 175 points (50%)
        normalized = calc.normalize_player_score(175.0, 350.0)

        assert normalized == 50.0, f"Expected 50.0, got {normalized}"

    def test_normalize_best_player_scale_100(self):
        """Test that best player normalizes to scale value"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        # Best player: 350 points (100%)
        normalized = calc.normalize_player_score(350.0, 350.0)

        assert normalized == 100.0, f"Expected 100.0, got {normalized}"

    def test_normalize_worst_player_scale_100(self):
        """Test that player with 0 points normalizes to 0"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        # Worst player: 0 points
        normalized = calc.normalize_player_score(0.0, 350.0)

        assert normalized == 0.0, f"Expected 0.0, got {normalized}"

    # =============================================================================
    # Different Scale Tests
    # =============================================================================

    def test_normalize_scale_80(self):
        """Test normalization with scale of 80"""
        calc = NormalizationCalculator(normalization_scale=80.0)

        # 50% of max
        normalized = calc.normalize_player_score(175.0, 350.0)

        assert normalized == 40.0, f"Expected 40.0 (50% of 80), got {normalized}"

    def test_normalize_scale_120(self):
        """Test normalization with scale of 120"""
        calc = NormalizationCalculator(normalization_scale=120.0)

        # 50% of max
        normalized = calc.normalize_player_score(175.0, 350.0)

        assert normalized == 60.0, f"Expected 60.0 (50% of 120), got {normalized}"

    def test_normalize_scale_variations(self):
        """Test multiple scale values with same input"""
        scales = [80, 100, 120]
        player_points = 175.0
        max_points = 350.0

        for scale in scales:
            calc = NormalizationCalculator(normalization_scale=scale)
            normalized = calc.normalize_player_score(player_points, max_points)
            expected = (player_points / max_points) * scale

            assert abs(normalized - expected) < 0.01, \
                f"Scale {scale}: Expected {expected}, got {normalized}"

    # =============================================================================
    # Edge Case Tests
    # =============================================================================

    def test_normalize_zero_max_points(self):
        """Test handling of zero max points (should return 0)"""
        calc = NormalizationCalculator()

        normalized = calc.normalize_player_score(100.0, 0.0)

        assert normalized == 0.0, f"Expected 0.0 for zero max, got {normalized}"

    def test_normalize_negative_max_points(self):
        """Test handling of negative max points (should return 0)"""
        calc = NormalizationCalculator()

        normalized = calc.normalize_player_score(100.0, -50.0)

        assert normalized == 0.0, f"Expected 0.0 for negative max, got {normalized}"

    def test_normalize_negative_player_points(self):
        """Test handling of negative player points (should treat as 0)"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        normalized = calc.normalize_player_score(-50.0, 350.0)

        assert normalized == 0.0, f"Expected 0.0 for negative points, got {normalized}"

    def test_normalize_player_exceeds_max(self):
        """Test that player can exceed 100% if their points exceed cached max"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        # Player has more points than the "max"
        normalized = calc.normalize_player_score(400.0, 350.0)

        assert normalized > 100.0, f"Expected >100.0 when exceeding max, got {normalized}"
        assert abs(normalized - 114.29) < 0.1, f"Expected ~114.29, got {normalized}"

    def test_calculate_max_no_available_players(self):
        """Test handling when no players available (all drafted)"""
        calc = NormalizationCalculator()

        players = [
            self.create_test_player("Player A", 100, drafted=2),
            self.create_test_player("Player B", 200, drafted=1),
        ]

        max_points = calc.calculate_max_player_points(players)

        assert max_points == 1.0, f"Expected fallback value 1.0, got {max_points}"

    def test_calculate_max_empty_player_list(self):
        """Test handling of empty player list"""
        calc = NormalizationCalculator()

        max_points = calc.calculate_max_player_points([])

        assert max_points == 1.0, f"Expected fallback value 1.0 for empty list, got {max_points}"

    # =============================================================================
    # Player Pool Integration Tests
    # =============================================================================

    def test_calculate_max_player_points_from_pool(self):
        """Test finding max from player pool"""
        calc = NormalizationCalculator()

        players = [
            self.create_test_player("Player A", 350, drafted=0),
            self.create_test_player("Player B", 175, drafted=0),
            self.create_test_player("Player C", 70, drafted=0),
        ]

        max_points = calc.calculate_max_player_points(players)

        assert max_points == 350.0, f"Expected 350.0, got {max_points}"

    def test_calculate_max_ignores_drafted_players(self):
        """Test that drafted players are excluded from max calculation"""
        calc = NormalizationCalculator()

        players = [
            self.create_test_player("Best Drafted", 500, drafted=2),  # Should be ignored
            self.create_test_player("Best Available", 300, drafted=0),  # Should be max
            self.create_test_player("Other Available", 200, drafted=0),
        ]

        max_points = calc.calculate_max_player_points(players)

        assert max_points == 300.0, \
            f"Expected 300.0 (ignoring drafted player), got {max_points}"

    def test_normalize_player_convenience_method(self):
        """Test normalize_player convenience method with player pool"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        players = [
            self.create_test_player("Player A", 350, drafted=0),
            self.create_test_player("Player B", 175, drafted=0),
            self.create_test_player("Player C", 70, drafted=0),
        ]

        # Normalize Player B (should be 50% of scale)
        normalized = calc.normalize_player(players[1], players)

        assert normalized == 50.0, f"Expected 50.0, got {normalized}"

    def test_normalize_multiple_players_from_pool(self):
        """Test normalizing all players in a pool"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        players = [
            self.create_test_player("Player A", 350, drafted=0),
            self.create_test_player("Player B", 175, drafted=0),
            self.create_test_player("Player C", 70, drafted=0),
        ]

        scores = [calc.normalize_player(p, players) for p in players]

        assert abs(scores[0] - 100.0) < 0.01, f"Player A: Expected 100.0, got {scores[0]}"
        assert abs(scores[1] - 50.0) < 0.01, f"Player B: Expected 50.0, got {scores[1]}"
        assert abs(scores[2] - 20.0) < 0.01, f"Player C: Expected 20.0, got {scores[2]}"

    # =============================================================================
    # Cache Behavior Tests
    # =============================================================================

    def test_cache_invalidation(self):
        """Test that cache invalidation works correctly"""
        calc = NormalizationCalculator()

        players = [self.create_test_player("Player A", 100, drafted=0)]

        # First call caches max
        calc.normalize_player(players[0], players)
        assert calc._max_player_points_cache == 100.0, "Cache should be set"

        # Invalidate cache
        calc.invalidate_cache()
        assert calc._max_player_points_cache is None, "Cache should be None after invalidation"

    def test_cache_reuses_max_value(self):
        """Test that cache avoids recalculating max"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        players = [
            self.create_test_player("Player A", 350, drafted=0),
            self.create_test_player("Player B", 175, drafted=0),
        ]

        # First call calculates and caches max
        calc.normalize_player(players[0], players)
        cached_max = calc._max_player_points_cache

        # Second call should reuse cached max
        calc.normalize_player(players[1], players)
        assert calc._max_player_points_cache == cached_max, "Cache should be reused"

    def test_cache_updates_after_invalidation(self):
        """Test that cache is recalculated after invalidation"""
        calc = NormalizationCalculator()

        players = [self.create_test_player("Player A", 100, drafted=0)]

        # Cache initial max
        calc.normalize_player(players[0], players)
        assert calc._max_player_points_cache == 100.0

        # Add better player and invalidate
        players.append(self.create_test_player("Player B", 200, drafted=0))
        calc.invalidate_cache()

        # Should recalculate with new max
        calc.normalize_player(players[1], players)
        assert calc._max_player_points_cache == 200.0, \
            "Cache should update to new max after invalidation"

    # =============================================================================
    # Fallback Behavior Tests
    # =============================================================================

    def test_fallback_to_fantasy_points(self):
        """Test fallback when remaining_season_projection not available"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        # Create player without remaining_season_projection
        player = FantasyPlayer(
            id=1,
            name="Test Player",
            position='QB',
            team='TEST',
            fantasy_points=250.0,
            drafted=0
        )
        # Don't set remaining_season_projection

        players = [
            player,
            self.create_test_player("Max Player", 500, drafted=0)
        ]

        # Should use fantasy_points as fallback
        normalized = calc.normalize_player(player, players)

        assert normalized == 50.0, \
            f"Expected 50.0 using fantasy_points fallback, got {normalized}"

    # =============================================================================
    # Info Method Tests
    # =============================================================================

    def test_get_normalization_info(self):
        """Test get_normalization_info returns correct details"""
        calc = NormalizationCalculator(normalization_scale=100.0)

        players = [
            self.create_test_player("Player A", 350, drafted=0),
            self.create_test_player("Player B", 175, drafted=0),
        ]

        info = calc.get_normalization_info(players[1], players)

        assert info['player_name'] == "Player B"
        assert info['raw_points'] == 175.0
        assert info['max_points'] == 350.0
        assert info['scale'] == 100.0
        assert info['normalized_score'] == 50.0
        assert info['percentage'] == 50.0

    # =============================================================================
    # Formula Verification Tests
    # =============================================================================

    def test_normalization_formula_exact(self):
        """Verify exact normalization formula: (player / max) * scale"""
        test_cases = [
            # (player_points, max_points, scale, expected)
            (350, 350, 100, 100.0),  # 100%
            (175, 350, 100, 50.0),   # 50%
            (70, 350, 100, 20.0),    # 20%
            (350, 350, 80, 80.0),    # 100% with scale 80
            (175, 350, 80, 40.0),    # 50% with scale 80
            (350, 350, 120, 120.0),  # 100% with scale 120
            (175, 350, 120, 60.0),   # 50% with scale 120
        ]

        for player_pts, max_pts, scale, expected in test_cases:
            calc = NormalizationCalculator(normalization_scale=scale)
            result = calc.normalize_player_score(player_pts, max_pts)
            assert abs(result - expected) < 0.01, \
                f"Formula test failed: ({player_pts}/{max_pts})*{scale} = {expected}, got {result}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])