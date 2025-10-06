#!/usr/bin/env python3
"""
Unit tests for DraftOrderCalculator

Tests round-based bonus calculations using DRAFT_ORDER configuration.

Author: Kai Mizuno
Last Updated: September 2025
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from draft_helper.core.draft_order_calculator import DraftOrderCalculator
from draft_helper.FantasyTeam import FantasyTeam
from shared_files.FantasyPlayer import FantasyPlayer
from shared_files.parameter_json_manager import ParameterJsonManager
import draft_helper.draft_helper_constants as Constants


class TestDraftOrderCalculator:
    """Test suite for DraftOrderCalculator"""

    @pytest.fixture
    def param_manager(self):
        """Create ParameterJsonManager for testing"""
        param_json_path = str(Path(__file__).parent.parent.parent / 'shared_files' / 'parameters.json')
        return ParameterJsonManager(param_json_path)

    def create_test_player(self, name: str, position: str, drafted: int = 0):
        """Helper to create test players (default drafted=0 for drafting)"""
        return FantasyPlayer(
            id=hash(name) % 10000,
            name=name,
            position=position,
            team='TEST',
            fantasy_points=100.0,
            drafted=drafted
        )

    # =============================================================================
    # Current Round Detection Tests
    # =============================================================================

    def test_current_round_empty_roster(self, param_manager):
        """Test round detection with empty roster (should be Round 1)"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        current_round = calc.get_current_draft_round()

        assert current_round == 0, f"Expected round 0 (Round 1), got {current_round}"

    def test_current_round_partial_roster(self, param_manager):
        """Test round detection with partial roster"""
        team = FantasyTeam()

        # Draft 4 players
        for i in range(4):
            player = self.create_test_player(f"Player {i}", 'RB')
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)
        current_round = calc.get_current_draft_round()

        assert current_round == 4, f"Expected round 4 (Round 5), got {current_round}"

    def test_current_round_full_roster(self, param_manager):
        """Test round detection with full roster (should be None)"""
        team = FantasyTeam()

        # Draft max players with valid position distribution
        # MAX_POSITIONS: QB:2, RB:4, WR:4, FLEX:1, TE:2, K:1, DST:1 = 15 total
        players = [
            self.create_test_player("RB1", 'RB'),
            self.create_test_player("RB2", 'RB'),
            self.create_test_player("RB3", 'RB'),
            self.create_test_player("RB4", 'RB'),
            self.create_test_player("WR1", 'WR'),
            self.create_test_player("WR2", 'WR'),
            self.create_test_player("WR3", 'WR'),
            self.create_test_player("WR4", 'WR'),
            self.create_test_player("QB1", 'QB'),
            self.create_test_player("QB2", 'QB'),
            self.create_test_player("TE1", 'TE'),
            self.create_test_player("TE2", 'TE'),
            self.create_test_player("K1", 'K'),
            self.create_test_player("DST1", 'DST'),
            self.create_test_player("WR5", 'WR'),  # FLEX slot
        ]
        for player in players:
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)
        current_round = calc.get_current_draft_round()

        assert current_round is None, f"Expected None for full roster, got {current_round}"

    # =============================================================================
    # Round Priorities Tests
    # =============================================================================

    def test_get_round_priorities_round_1(self, param_manager):
        """Test getting priorities for Round 1"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        # DRAFT_ORDER[0] should be {FLEX: PRIMARY, QB: SECONDARY}
        priorities = calc.get_round_priorities(0)

        assert 'FLEX' in priorities, "Round 1 should have FLEX priority"
        assert 'QB' in priorities, "Round 1 should have QB priority"
        assert priorities['FLEX'] == param_manager.DRAFT_ORDER_PRIMARY_BONUS, f"FLEX bonus should be PRIMARY, got {priorities['FLEX']}"
        assert priorities['QB'] == param_manager.DRAFT_ORDER_SECONDARY_BONUS, f"QB bonus should be SECONDARY, got {priorities['QB']}"

    def test_get_round_priorities_round_5(self, param_manager):
        """Test getting priorities for Round 5"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        # DRAFT_ORDER[4] should be {QB: PRIMARY, FLEX: SECONDARY}
        priorities = calc.get_round_priorities(4)

        assert 'QB' in priorities, "Round 5 should have QB priority"
        assert 'FLEX' in priorities, "Round 5 should have FLEX priority"
        assert priorities['QB'] == param_manager.DRAFT_ORDER_PRIMARY_BONUS, f"QB bonus should be PRIMARY, got {priorities['QB']}"
        assert priorities['FLEX'] == param_manager.DRAFT_ORDER_SECONDARY_BONUS, f"FLEX bonus should be SECONDARY, got {priorities['FLEX']}"

    def test_get_round_priorities_invalid_round(self, param_manager):
        """Test getting priorities for invalid round returns empty dict"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        priorities = calc.get_round_priorities(999)

        assert priorities == {}, f"Expected empty dict for invalid round, got {priorities}"

    # =============================================================================
    # Bonus Calculation Tests - Round 1 (FLEX Priority)
    # =============================================================================

    def test_bonus_round_1_rb_player(self, param_manager):
        """Test DRAFT_ORDER bonus for RB in Round 1 (FLEX priority)"""
        team = FantasyTeam()  # Empty roster = Round 1
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        rb = self.create_test_player("Test RB", 'RB', drafted=0)

        bonus = calc.calculate_bonus(rb)

        # RB is FLEX-eligible, should get PRIMARY bonus
        assert bonus == param_manager.DRAFT_ORDER_PRIMARY_BONUS, f"Expected PRIMARY bonus, got {bonus}"

    def test_bonus_round_1_wr_player(self, param_manager):
        """Test DRAFT_ORDER bonus for WR in Round 1 (FLEX priority)"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        wr = self.create_test_player("Test WR", 'WR', drafted=0)

        bonus = calc.calculate_bonus(wr)

        # WR is FLEX-eligible, should get PRIMARY bonus
        assert bonus == param_manager.DRAFT_ORDER_PRIMARY_BONUS, f"Expected PRIMARY bonus, got {bonus}"

    def test_bonus_round_1_qb_player(self, param_manager):
        """Test DRAFT_ORDER bonus for QB in Round 1 (secondary priority)"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        qb = self.create_test_player("Test QB", 'QB', drafted=0)

        bonus = calc.calculate_bonus(qb)

        # QB has secondary priority
        assert bonus == param_manager.DRAFT_ORDER_SECONDARY_BONUS, f"Expected SECONDARY bonus, got {bonus}"

    def test_bonus_round_1_te_player(self, param_manager):
        """Test DRAFT_ORDER bonus for TE in Round 1 (no priority)"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        te = self.create_test_player("Test TE", 'TE', drafted=0)

        bonus = calc.calculate_bonus(te)

        # TE not in Round 1 priorities
        assert bonus == 0.0, f"Expected 0.0 (no priority), got {bonus}"

    # =============================================================================
    # Bonus Calculation Tests - Round 5 (QB Priority)
    # =============================================================================

    def test_bonus_round_5_qb_player(self, param_manager):
        """Test DRAFT_ORDER bonus for QB in Round 5 (QB primary)"""
        team = FantasyTeam()

        # Draft 4 players to reach Round 5
        for i in range(4):
            player = self.create_test_player(f"Player {i}", 'RB')
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)

        qb = self.create_test_player("Test QB", 'QB', drafted=0)

        bonus = calc.calculate_bonus(qb)

        # QB is primary in Round 5
        assert bonus == param_manager.DRAFT_ORDER_PRIMARY_BONUS, f"Expected PRIMARY bonus, got {bonus}"

    def test_bonus_round_5_rb_player(self, param_manager):
        """Test DRAFT_ORDER bonus for RB in Round 5 (FLEX secondary)"""
        team = FantasyTeam()

        # Draft 4 players to reach Round 5
        for i in range(4):
            player = self.create_test_player(f"Player {i}", 'WR')
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)

        rb = self.create_test_player("Test RB", 'RB', drafted=0)

        bonus = calc.calculate_bonus(rb)

        # RB is FLEX-eligible, gets secondary bonus
        assert bonus == param_manager.DRAFT_ORDER_SECONDARY_BONUS, f"Expected SECONDARY bonus, got {bonus}"

    def test_bonus_round_5_te_player(self, param_manager):
        """Test DRAFT_ORDER bonus for TE in Round 5 (no priority)"""
        team = FantasyTeam()

        # Draft 4 players to reach Round 5
        for i in range(4):
            player = self.create_test_player(f"Player {i}", 'RB')
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)

        te = self.create_test_player("Test TE", 'TE', drafted=0)

        bonus = calc.calculate_bonus(te)

        # TE not in Round 5 priorities
        assert bonus == 0.0, f"Expected 0.0 (no priority), got {bonus}"

    # =============================================================================
    # Bonus Calculation Tests - Draft Complete
    # =============================================================================

    def test_bonus_draft_complete(self, param_manager):
        """Test that bonus is 0 when draft is complete"""
        team = FantasyTeam()

        # Draft max players with valid distribution
        players = [
            self.create_test_player("RB1", 'RB'),
            self.create_test_player("RB2", 'RB'),
            self.create_test_player("RB3", 'RB'),
            self.create_test_player("RB4", 'RB'),
            self.create_test_player("WR1", 'WR'),
            self.create_test_player("WR2", 'WR'),
            self.create_test_player("WR3", 'WR'),
            self.create_test_player("WR4", 'WR'),
            self.create_test_player("QB1", 'QB'),
            self.create_test_player("QB2", 'QB'),
            self.create_test_player("TE1", 'TE'),
            self.create_test_player("TE2", 'TE'),
            self.create_test_player("K1", 'K'),
            self.create_test_player("DST1", 'DST'),
            self.create_test_player("WR5", 'WR'),
        ]
        for player in players:
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)

        rb = self.create_test_player("Extra RB", 'RB', drafted=0)

        bonus = calc.calculate_bonus(rb)

        assert bonus == 0.0, f"Expected 0.0 for completed draft, got {bonus}"

    # =============================================================================
    # Round Assignment Tests
    # =============================================================================

    def test_assign_players_to_rounds_basic(self, param_manager):
        """Test basic player assignment to rounds"""
        team = FantasyTeam()

        # Create roster matching DRAFT_ORDER expectations
        players = [
            self.create_test_player("RB1", 'RB'),   # Round 1: FLEX
            self.create_test_player("WR1", 'WR'),   # Round 2: FLEX
            self.create_test_player("RB2", 'RB'),   # Round 3: FLEX
            self.create_test_player("WR2", 'WR'),   # Round 4: FLEX
            self.create_test_player("QB1", 'QB'),   # Round 5: QB
        ]

        for player in players:
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)
        assignments = calc.assign_players_to_rounds()

        assert len(assignments) == 5, f"Expected 5 assignments, got {len(assignments)}"
        assert 1 in assignments, "Round 1 should have assignment"
        assert 5 in assignments, "Round 5 should have assignment"
        assert assignments[5].position == 'QB', "Round 5 should have QB"

    def test_assign_players_handles_all_positions(self, param_manager):
        """Test assignment with diverse position roster"""
        team = FantasyTeam()

        # Create a full, valid roster
        players = [
            self.create_test_player("RB1", 'RB'),
            self.create_test_player("RB2", 'RB'),
            self.create_test_player("RB3", 'RB'),
            self.create_test_player("RB4", 'RB'),
            self.create_test_player("WR1", 'WR'),
            self.create_test_player("WR2", 'WR'),
            self.create_test_player("WR3", 'WR'),
            self.create_test_player("WR4", 'WR'),
            self.create_test_player("QB1", 'QB'),
            self.create_test_player("QB2", 'QB'),
            self.create_test_player("TE1", 'TE'),
            self.create_test_player("TE2", 'TE'),
            self.create_test_player("K1", 'K'),
            self.create_test_player("DST1", 'DST'),
            self.create_test_player("WR5", 'WR'),  # Extra FLEX
        ]

        for player in players:
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)
        assignments = calc.assign_players_to_rounds()

        # Should assign all 15 players
        assert len(assignments) == 15, f"Expected 15 assignments, got {len(assignments)}"

    # =============================================================================
    # Validation Tests
    # =============================================================================

    def test_validate_roster_composition_valid(self, param_manager):
        """Test validation passes for valid roster"""
        team = FantasyTeam()

        # Create a roster matching DRAFT_ORDER
        players = [
            self.create_test_player("RB1", 'RB'),
            self.create_test_player("RB2", 'RB'),
            self.create_test_player("WR1", 'WR'),
            self.create_test_player("WR2", 'WR'),
            self.create_test_player("QB1", 'QB'),
        ]

        for player in players:
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)
        is_valid = calc.validate_roster_composition()

        assert is_valid, "Valid roster should pass validation"

    # =============================================================================
    # Info Method Tests
    # =============================================================================

    def test_get_bonus_info_with_bonus(self, param_manager):
        """Test get_bonus_info returns correct details"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        rb = self.create_test_player("Test RB", 'RB', drafted=0)

        info = calc.get_bonus_info(rb)

        assert info['player_name'] == "Test RB"
        assert info['position'] == 'RB'
        assert info['current_round'] == 1  # 1-indexed for display
        assert info['match_type'] == 'flex'
        assert info['bonus'] == param_manager.DRAFT_ORDER_PRIMARY_BONUS
        assert info['draft_complete'] is False

    def test_get_bonus_info_draft_complete(self, param_manager):
        """Test get_bonus_info when draft is complete"""
        team = FantasyTeam()

        # Fill roster with valid distribution
        players = [
            self.create_test_player("RB1", 'RB'),
            self.create_test_player("RB2", 'RB'),
            self.create_test_player("RB3", 'RB'),
            self.create_test_player("RB4", 'RB'),
            self.create_test_player("WR1", 'WR'),
            self.create_test_player("WR2", 'WR'),
            self.create_test_player("WR3", 'WR'),
            self.create_test_player("WR4", 'WR'),
            self.create_test_player("QB1", 'QB'),
            self.create_test_player("QB2", 'QB'),
            self.create_test_player("TE1", 'TE'),
            self.create_test_player("TE2", 'TE'),
            self.create_test_player("K1", 'K'),
            self.create_test_player("DST1", 'DST'),
            self.create_test_player("WR5", 'WR'),
        ]
        for player in players:
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)

        rb = self.create_test_player("Extra RB", 'RB', drafted=0)

        info = calc.get_bonus_info(rb)

        assert info['current_round'] is None
        assert info['draft_complete'] is True
        assert info['bonus'] == 0.0

    # =============================================================================
    # FLEX Eligibility Tests
    # =============================================================================

    def test_flex_eligibility_rb(self, param_manager):
        """Test that RB is FLEX-eligible"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        rb = self.create_test_player("Test RB", 'RB', drafted=0)

        # Round 1 has FLEX priority
        bonus = calc.calculate_bonus(rb)

        assert bonus == param_manager.DRAFT_ORDER_PRIMARY_BONUS, "RB should get FLEX bonus"

    def test_flex_eligibility_wr(self, param_manager):
        """Test that WR is FLEX-eligible"""
        team = FantasyTeam()
        calc = DraftOrderCalculator(team, param_manager=param_manager)

        wr = self.create_test_player("Test WR", 'WR', drafted=0)

        # Round 1 has FLEX priority
        bonus = calc.calculate_bonus(wr)

        assert bonus == param_manager.DRAFT_ORDER_PRIMARY_BONUS, "WR should get FLEX bonus"

    def test_flex_not_eligible_qb(self, param_manager):
        """Test that QB is not FLEX-eligible"""
        team = FantasyTeam()

        # Draft mixed positions to reach Round 7 (FLEX-only)
        # Need 6 players: 2RB + 2WR + 1QB + 1TE = Round 7
        players = [
            self.create_test_player("RB1", 'RB'),
            self.create_test_player("RB2", 'RB'),
            self.create_test_player("WR1", 'WR'),
            self.create_test_player("WR2", 'WR'),
            self.create_test_player("QB1", 'QB'),
            self.create_test_player("TE1", 'TE'),
        ]
        for player in players:
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)

        qb = self.create_test_player("Test QB2", 'QB', drafted=0)

        bonus = calc.calculate_bonus(qb)

        # QB should not get FLEX bonus in Round 7
        assert bonus == 0.0, "QB should not be FLEX-eligible"

    def test_flex_not_eligible_te(self, param_manager):
        """Test that TE is not FLEX-eligible"""
        team = FantasyTeam()

        # Draft mixed positions to reach Round 7 (FLEX-only)
        players = [
            self.create_test_player("RB1", 'RB'),
            self.create_test_player("RB2", 'RB'),
            self.create_test_player("WR1", 'WR'),
            self.create_test_player("WR2", 'WR'),
            self.create_test_player("QB1", 'QB'),
            self.create_test_player("TE1", 'TE'),
        ]
        for player in players:
            team.draft_player(player)

        calc = DraftOrderCalculator(team, param_manager=param_manager)

        te = self.create_test_player("Test TE2", 'TE', drafted=0)

        bonus = calc.calculate_bonus(te)

        # TE should not get FLEX bonus in Round 7
        assert bonus == 0.0, "TE should not be FLEX-eligible"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])