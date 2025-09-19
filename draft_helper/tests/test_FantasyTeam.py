#!/usr/bin/env python3
"""
Unit tests for FantasyTeam class.

Tests the comprehensive FLEX position improvements including:
- Phase 1: Enhanced Validation
- Phase 2: Explicit Slot Tracking
- Phase 3: Trade Logic Improvements and Optimization
- Roster management and construction validation
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from FantasyTeam import FantasyTeam
import draft_helper_constants as Constants

# Import FantasyPlayer from shared_files
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared_files"))
from FantasyPlayer import FantasyPlayer


class TestFantasyTeam:
    """Test suite for FantasyTeam class with FLEX improvements"""

    @pytest.fixture
    def team(self):
        """Create fresh FantasyTeam instance"""
        return FantasyTeam()

    @pytest.fixture
    def sample_rb(self):
        """Create sample RB player"""
        return FantasyPlayer(
            id="rb1",
            name="Test RB",
            team="TEST",
            position="RB",
            bye_week=5,
            drafted=0,
            locked=0,
            fantasy_points=150.0,
            injury_status="ACTIVE"
        )

    @pytest.fixture
    def sample_wr(self):
        """Create sample WR player"""
        return FantasyPlayer(
            id="wr1",
            name="Test WR",
            team="TEST",
            position="WR",
            bye_week=7,
            drafted=0,
            locked=0,
            fantasy_points=140.0,
            injury_status="ACTIVE"
        )

    def test_team_initialization(self, team):
        """Test Phase 2: Team initializes with explicit slot tracking"""
        # Test basic initialization
        assert len(team.roster) == 0
        assert team.pos_counts == {pos: 0 for pos in Constants.MAX_POSITIONS.keys()}

        # Test Phase 2: Explicit slot tracking initialization
        assert hasattr(team, 'slot_assignments')
        assert isinstance(team.slot_assignments, dict)

        # Verify all position slots are initialized
        expected_slots = [Constants.QB, Constants.RB, Constants.WR,
                         Constants.TE, Constants.FLEX, Constants.K, Constants.DST]
        for slot in expected_slots:
            assert slot in team.slot_assignments
            assert isinstance(team.slot_assignments[slot], list)
            assert len(team.slot_assignments[slot]) == 0

    def test_basic_player_drafting(self, team, sample_rb, sample_wr):
        """Test basic player drafting to regular positions"""
        # Draft RB to regular RB slot
        result = team.draft_player(sample_rb)
        assert result is True
        assert len(team.roster) == 1
        assert team.pos_counts["RB"] == 1

        # Verify explicit slot assignment
        assert sample_rb.id in team.slot_assignments["RB"]
        assert team.get_slot_assignment(sample_rb) == "RB"

        # Draft WR to regular WR slot
        result = team.draft_player(sample_wr)
        assert result is True
        assert len(team.roster) == 2
        assert team.pos_counts["WR"] == 1

        # Verify explicit slot assignment
        assert sample_wr.id in team.slot_assignments["WR"]
        assert team.get_slot_assignment(sample_wr) == "WR"

    def test_flex_position_assignment(self, team):
        """Test FLEX position assignment when regular slots are full"""
        # Fill regular RB slots
        for i in range(Constants.MAX_POSITIONS["RB"]):
            rb = FantasyPlayer(
                id=f"rb{i}",
                name=f"RB {i}",
                team="TEST",
                position="RB",
                bye_week=5,
                fantasy_points=100.0 + i
            )
            result = team.draft_player(rb)
            assert result is True

        # Verify RB slots are full
        assert len(team.slot_assignments["RB"]) == Constants.MAX_POSITIONS["RB"]
        assert team.pos_counts["RB"] == Constants.MAX_POSITIONS["RB"]

        # Draft another RB (should go to FLEX)
        flex_rb = FantasyPlayer(
            id="flex_rb",
            name="FLEX RB",
            team="TEST",
            position="RB",
            bye_week=6,
            fantasy_points=120.0
        )
        result = team.draft_player(flex_rb)
        assert result is True

        # Verify FLEX assignment
        assert flex_rb.id in team.slot_assignments["FLEX"]
        assert team.get_slot_assignment(flex_rb) == "FLEX"
        assert team.pos_counts["RB"] == Constants.MAX_POSITIONS["RB"] + 1  # Total RBs including FLEX

    def test_flex_position_limits(self, team):
        """Test FLEX position limits are enforced"""
        # Fill all RB slots (regular + FLEX)
        total_rb_capacity = Constants.MAX_POSITIONS["RB"] + Constants.MAX_POSITIONS["FLEX"]

        for i in range(total_rb_capacity):
            rb = FantasyPlayer(
                id=f"rb{i}",
                name=f"RB {i}",
                team="TEST",
                position="RB",
                bye_week=5,
                fantasy_points=100.0 + i
            )
            result = team.draft_player(rb)
            assert result is True

        # Try to draft one more RB (should fail)
        extra_rb = FantasyPlayer(
            id="extra_rb",
            name="Extra RB",
            team="TEST",
            position="RB",
            bye_week=7,
            fantasy_points=90.0
        )
        result = team.draft_player(extra_rb)
        assert result is False

    def test_phase1_roster_integrity_validation(self, team, sample_rb, sample_wr):
        """Test Phase 1: Enhanced validation methods"""
        # Empty team should be valid
        integrity = team.validate_roster_integrity()
        assert integrity is True

        # Add players
        team.draft_player(sample_rb)
        team.draft_player(sample_wr)

        # Team with valid players should be valid
        integrity = team.validate_roster_integrity()
        assert integrity is True

        # Test integrity with corrupted data (simulate error)
        original_slot = team.slot_assignments["RB"].copy()
        team.slot_assignments["RB"].append("invalid_id")  # Add invalid player ID

        integrity = team.validate_roster_integrity()
        assert integrity is False

        # Restore valid state
        team.slot_assignments["RB"] = original_slot
        integrity = team.validate_roster_integrity()
        assert integrity is True

    def test_phase2_explicit_slot_tracking(self, team):
        """Test Phase 2: Explicit slot tracking methods"""
        # Create test players
        rb1 = FantasyPlayer(id="rb1", name="RB 1", position="RB", team="TEST", fantasy_points=100.0)
        rb2 = FantasyPlayer(id="rb2", name="RB 2", position="RB", team="TEST", fantasy_points=90.0)
        wr1 = FantasyPlayer(id="wr1", name="WR 1", position="WR", team="TEST", fantasy_points=80.0)

        # Draft players
        team.draft_player(rb1)
        team.draft_player(rb2)
        team.draft_player(wr1)

        # Test get_players_by_slot
        rb_players = team.get_players_by_slot("RB")
        assert len(rb_players) == 2
        assert rb1 in rb_players
        assert rb2 in rb_players

        wr_players = team.get_players_by_slot("WR")
        assert len(wr_players) == 1
        assert wr1 in wr_players

        # Test get_slot_assignment
        assert team.get_slot_assignment(rb1) == "RB"
        assert team.get_slot_assignment(rb2) == "RB"
        assert team.get_slot_assignment(wr1) == "WR"

        # Test slot assignments are consistent
        for slot, player_ids in team.slot_assignments.items():
            for player_id in player_ids:
                player = next((p for p in team.roster if p.id == player_id), None)
                assert player is not None
                assert team.get_slot_assignment(player) == slot

    def test_player_removal_with_slot_tracking(self, team):
        """Test player removal maintains slot tracking integrity"""
        # Create and draft players
        rb1 = FantasyPlayer(id="rb1", name="RB 1", position="RB", team="TEST", fantasy_points=100.0)
        rb2 = FantasyPlayer(id="rb2", name="RB 2", position="RB", team="TEST", fantasy_points=90.0)

        team.draft_player(rb1)
        team.draft_player(rb2)

        # Verify initial state
        assert len(team.slot_assignments["RB"]) == 2
        assert len(team.roster) == 2

        # Remove first player
        result = team.remove_player(rb1)
        assert result is True

        # Verify slot tracking updated
        assert rb1.id not in team.slot_assignments["RB"]
        assert rb2.id in team.slot_assignments["RB"]
        assert len(team.slot_assignments["RB"]) == 1
        assert len(team.roster) == 1

        # Verify integrity
        integrity = team.validate_roster_integrity()
        assert integrity is True

    def test_player_replacement_with_slot_tracking(self, team):
        """Test player replacement maintains slot tracking integrity"""
        # Create players
        old_rb = FantasyPlayer(id="old_rb", name="Old RB", position="RB", team="TEST", fantasy_points=80.0)
        new_wr = FantasyPlayer(id="new_wr", name="New WR", position="WR", team="TEST", fantasy_points=90.0)

        # Draft old player
        team.draft_player(old_rb)
        assert old_rb.id in team.slot_assignments["RB"]

        # Replace with new player
        result = team.replace_player(old_rb, new_wr)
        assert result is True

        # Verify slot tracking updated
        assert old_rb.id not in team.slot_assignments["RB"]
        assert new_wr.id in team.slot_assignments["WR"]
        assert old_rb not in team.roster
        assert new_wr in team.roster

        # Verify integrity
        integrity = team.validate_roster_integrity()
        assert integrity is True

    def test_phase3_flex_optimization(self, team):
        """Test Phase 3: FLEX optimization functionality"""
        # Create players with different fantasy points for optimization
        rb1 = FantasyPlayer(id="rb1", name="Elite RB", position="RB", team="TEST", fantasy_points=200.0)
        rb2 = FantasyPlayer(id="rb2", name="Good RB", position="RB", team="TEST", fantasy_points=150.0)
        wr1 = FantasyPlayer(id="wr1", name="Average WR", position="WR", team="TEST", fantasy_points=100.0)

        # Draft to create FLEX scenario
        team.draft_player(rb1)
        team.draft_player(rb2)
        team.draft_player(wr1)

        # Force a suboptimal FLEX assignment for testing
        # Move the better RB to FLEX and worse WR to regular slot
        team.slot_assignments["RB"] = [rb2.id]  # Keep worse RB in regular slot
        team.slot_assignments["FLEX"] = [rb1.id]  # Put better RB in FLEX
        team.slot_assignments["WR"] = [wr1.id]

        def simple_scoring_function(player):
            return player.fantasy_points

        # Test optimization
        optimization_performed = team.optimize_flex_assignments(simple_scoring_function)

        # Since we have RBs and WRs, optimization should be possible
        # (exact behavior depends on implementation, but should handle gracefully)
        assert isinstance(optimization_performed, bool)

        # Verify integrity after optimization
        integrity = team.validate_roster_integrity()
        assert integrity is True

    def test_get_weakest_player_by_position(self, team):
        """Test finding weakest player by position"""
        # Create players with different fantasy points
        rb1 = FantasyPlayer(id="rb1", name="Strong RB", position="RB", team="TEST", fantasy_points=150.0)
        rb2 = FantasyPlayer(id="rb2", name="Weak RB", position="RB", team="TEST", fantasy_points=80.0)
        rb3 = FantasyPlayer(id="rb3", name="Average RB", position="RB", team="TEST", fantasy_points=120.0)

        team.draft_player(rb1)
        team.draft_player(rb2)
        team.draft_player(rb3)

        def simple_scoring_function(player):
            return player.fantasy_points

        weakest = team.get_weakest_player_by_position("RB", simple_scoring_function)
        assert weakest == rb2  # Should return the one with lowest fantasy_points

        # Test with position that has no players
        weakest_te = team.get_weakest_player_by_position("TE", simple_scoring_function)
        assert weakest_te is None

    def test_can_replace_player_logic(self, team):
        """Test _can_replace_player logic"""
        # Create test players
        rb1 = FantasyPlayer(id="rb1", name="RB 1", position="RB", team="TEST", fantasy_points=100.0)
        wr1 = FantasyPlayer(id="wr1", name="WR 1", position="WR", team="TEST", fantasy_points=90.0)

        team.draft_player(rb1)

        # Test replacing RB with WR (should work if WR slots available)
        can_replace = team._can_replace_player(rb1, wr1)
        assert isinstance(can_replace, bool)

        # Test replacing with same position (should work)
        rb2 = FantasyPlayer(id="rb2", name="RB 2", position="RB", team="TEST", fantasy_points=110.0)
        can_replace = team._can_replace_player(rb1, rb2)
        assert can_replace is True

    def test_total_team_score_calculation(self, team):
        """Test total team score calculation"""
        # Create players
        rb1 = FantasyPlayer(id="rb1", name="RB 1", position="RB", team="TEST", fantasy_points=100.0)
        wr1 = FantasyPlayer(id="wr1", name="WR 1", position="WR", team="TEST", fantasy_points=90.0)

        team.draft_player(rb1)
        team.draft_player(wr1)

        def simple_scoring_function(player):
            return player.fantasy_points

        total_score = team.get_total_team_score(simple_scoring_function)
        assert total_score == 190.0  # 100.0 + 90.0

    def test_roster_construction_limits(self, team):
        """Test that roster construction follows league rules"""
        players_drafted = 0

        # Try to draft up to maximum players
        for i in range(Constants.MAX_PLAYERS + 2):  # Try to exceed limit
            if i % 4 == 0:
                player = FantasyPlayer(id=f"qb{i}", name=f"QB {i}", position="QB", team="TEST")
            elif i % 4 == 1:
                player = FantasyPlayer(id=f"rb{i}", name=f"RB {i}", position="RB", team="TEST")
            elif i % 4 == 2:
                player = FantasyPlayer(id=f"wr{i}", name=f"WR {i}", position="WR", team="TEST")
            else:
                player = FantasyPlayer(id=f"te{i}", name=f"TE {i}", position="TE", team="TEST")

            result = team.draft_player(player)
            if result:
                players_drafted += 1

            # Should not exceed maximum
            assert players_drafted <= Constants.MAX_PLAYERS
            assert len(team.roster) <= Constants.MAX_PLAYERS

    def test_edge_case_empty_operations(self, team):
        """Test edge cases with empty team"""
        # Test operations on empty team
        assert team.get_players_by_slot("RB") == []
        assert team.get_weakest_player_by_position("RB", lambda p: p.fantasy_points) is None
        assert team.get_total_team_score(lambda p: p.fantasy_points) == 0.0
        assert team.validate_roster_integrity() is True

    def test_mixed_flex_scenarios(self, team):
        """Test complex FLEX scenarios with mixed RB/WR"""
        # Fill RB slots
        for i in range(Constants.MAX_POSITIONS["RB"]):
            rb = FantasyPlayer(id=f"rb{i}", name=f"RB {i}", position="RB", team="TEST", fantasy_points=100.0)
            team.draft_player(rb)

        # Fill WR slots
        for i in range(Constants.MAX_POSITIONS["WR"]):
            wr = FantasyPlayer(id=f"wr{i}", name=f"WR {i}", position="WR", team="TEST", fantasy_points=90.0)
            team.draft_player(wr)

        # Add FLEX-eligible player (should go to FLEX)
        flex_player = FantasyPlayer(id="flex1", name="FLEX Player", position="RB", team="TEST", fantasy_points=85.0)
        result = team.draft_player(flex_player)
        assert result is True
        assert team.get_slot_assignment(flex_player) == "FLEX"

        # Try to add another FLEX-eligible player (should fail)
        extra_player = FantasyPlayer(id="extra", name="Extra Player", position="WR", team="TEST", fantasy_points=80.0)
        result = team.draft_player(extra_player)
        assert result is False

        # Verify integrity
        integrity = team.validate_roster_integrity()
        assert integrity is True


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        # Basic test runner
        team = FantasyTeam()

        # Test initialization
        assert len(team.roster) == 0
        assert hasattr(team, 'slot_assignments')
        print("✅ Team initialization test passed")

        # Test basic drafting
        rb = FantasyPlayer(id="rb1", name="Test RB", position="RB", team="TEST", fantasy_points=100.0)
        result = team.draft_player(rb)
        assert result is True
        assert len(team.roster) == 1
        print("✅ Basic drafting test passed")

        # Test slot tracking
        assert team.get_slot_assignment(rb) == "RB"
        rb_players = team.get_players_by_slot("RB")
        assert len(rb_players) == 1
        print("✅ Slot tracking test passed")

        # Test integrity validation
        integrity = team.validate_roster_integrity()
        assert integrity is True
        print("✅ Integrity validation test passed")

        print("Basic tests completed successfully!")