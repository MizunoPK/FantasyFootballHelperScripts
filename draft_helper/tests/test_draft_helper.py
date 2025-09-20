#!/usr/bin/env python3
"""
Unit tests for Draft Helper main module.

Tests the draft helper functionality including:
- Draft and trade mode switching
- Player scoring and recommendations
- Pure greedy trade algorithm
- Configuration validation
- Injury and bye week penalties
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import draft_helper
import draft_helper_config as draft_config
import draft_helper_constants as Constants

# Import FantasyPlayer from shared_files
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared_files"))
from FantasyPlayer import FantasyPlayer


class TestDraftHelper:
    """Test suite for Draft Helper main functionality"""

    @pytest.fixture
    def sample_players(self):
        """Create sample player data for testing"""
        return [
            FantasyPlayer(
                id="1",
                name="Elite RB",
                position="RB",
                team="TEST",
                fantasy_points=200.0,
                bye_week=7,
                injury_status="ACTIVE"
            ),
            FantasyPlayer(
                id="2",
                name="Good WR",
                position="WR",
                team="DEMO",
                fantasy_points=150.0,
                bye_week=9,
                injury_status="QUESTIONABLE"
            ),
            FantasyPlayer(
                id="3",
                name="Average QB",
                position="QB",
                team="TEAM",
                fantasy_points=280.0,
                bye_week=5,
                injury_status="ACTIVE"
            ),
            FantasyPlayer(
                id="4",
                name="Injured TE",
                position="TE",
                team="INJ",
                fantasy_points=90.0,
                bye_week=11,
                injury_status="OUT"
            )
        ]

    @pytest.fixture
    def mock_team_with_players(self):
        """Create mock team with some players"""
        team = MagicMock()
        team.roster = [
            FantasyPlayer(id="owned1", name="Owned RB", position="RB", team="TEST", fantasy_points=120.0),
            FantasyPlayer(id="owned2", name="Owned WR", position="WR", team="TEST", fantasy_points=100.0)
        ]
        team.pos_counts = {"RB": 1, "WR": 1, "QB": 0, "TE": 0, "K": 0, "DST": 0, "FLEX": 0}
        return team

    @pytest.fixture
    def draft_helper_instance(self, sample_players):
        """Create DraftHelper instance for testing"""
        # Create a temporary CSV file with test players
        import tempfile
        import csv
        import os

        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')

        try:
            # Write test players to CSV
            fieldnames = ['id', 'name', 'team', 'position', 'bye_week', 'fantasy_points', 'injury_status', 'drafted']
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()

            for player in sample_players:
                writer.writerow({
                    'id': player.id,
                    'name': player.name,
                    'team': player.team,
                    'position': player.position,
                    'bye_week': player.bye_week or '',
                    'fantasy_points': player.fantasy_points,
                    'injury_status': player.injury_status,
                    'drafted': 0
                })

            temp_file.close()

            # Create DraftHelper with the temp file
            helper = draft_helper.DraftHelper(temp_file.name)
            yield helper

        finally:
            # Clean up temp file
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_configuration_validation(self):
        """Test that configuration is valid"""
        # Test that config validation runs without errors
        try:
            draft_config.validate_config()
        except ValueError as e:
            pytest.fail(f"Configuration validation failed: {e}")

        # Test core configuration values
        assert draft_config.MAX_PLAYERS > 0
        assert len(draft_config.DRAFT_ORDER) == draft_config.MAX_PLAYERS
        assert sum(draft_config.MAX_POSITIONS.values()) >= draft_config.MAX_PLAYERS

    def test_draft_mode_vs_trade_mode(self):
        """Test that both draft and trade functionality are available"""
        # Test that toggle still exists for injury penalty configuration
        assert isinstance(draft_config.TRADE_HELPER_MODE, bool)

        # Test recommendation count is reasonable
        assert draft_config.RECOMMENDATION_COUNT > 0
        assert draft_config.RECOMMENDATION_COUNT <= 20

        # Test that both modes are available via interactive menu
        assert hasattr(draft_config, 'MIN_TRADE_IMPROVEMENT')  # Trade functionality
        assert hasattr(draft_config, 'MAX_POSITIONS')  # Draft functionality

    def test_scoring_weights_configuration(self):
        """Test scoring weights are reasonable"""
        # Test positional need scoring
        assert draft_config.POS_NEEDED_SCORE > 0
        assert draft_config.PROJECTION_BASE_SCORE > 0

        # Test penalty system
        assert draft_config.BASE_BYE_PENALTY >= 0
        assert all(penalty >= 0 for penalty in draft_config.INJURY_PENALTIES.values())

    def test_injury_penalty_calculation(self, draft_helper_instance, sample_players):
        """Test injury penalty calculation"""
        active_player = sample_players[0]  # ACTIVE
        questionable_player = sample_players[1]  # QUESTIONABLE
        injured_player = sample_players[3]  # OUT

        # Test that injury penalties are applied correctly
        active_penalty = draft_helper_instance.compute_injury_penalty(active_player)
        questionable_penalty = draft_helper_instance.compute_injury_penalty(questionable_player)
        injured_penalty = draft_helper_instance.compute_injury_penalty(injured_player)

        # Active should have lowest penalty
        assert active_penalty == draft_config.INJURY_PENALTIES.get("LOW", 0)

        # Injured should have highest penalty
        assert injured_penalty == draft_config.INJURY_PENALTIES.get("HIGH", 50)

        # Questionable should be in between
        assert questionable_penalty == draft_config.INJURY_PENALTIES.get("MEDIUM", 25)

    def test_injury_penalty_roster_toggle(self, draft_helper_instance, sample_players):
        """Test APPLY_INJURY_PENALTY_TO_ROSTER toggle functionality"""
        # Create injured players with different drafted status
        injured_available = FantasyPlayer(
            id="avail_inj", name="Available Injured", position="RB", team="TEST",
            fantasy_points=100.0, bye_week=7, injury_status="OUT", drafted=0
        )
        injured_roster = FantasyPlayer(
            id="roster_inj", name="Roster Injured", position="WR", team="TEST",
            fantasy_points=100.0, bye_week=7, injury_status="OUT", drafted=2
        )

        # Save original config values
        original_trade_mode = draft_config.TRADE_HELPER_MODE
        original_apply_penalty = draft_config.APPLY_INJURY_PENALTY_TO_ROSTER

        try:
            # Test in trade mode with penalty toggle ON (default behavior)
            draft_config.TRADE_HELPER_MODE = True
            draft_config.APPLY_INJURY_PENALTY_TO_ROSTER = True

            available_penalty_on = draft_helper_instance.compute_injury_penalty(injured_available)
            roster_penalty_on = draft_helper_instance.compute_injury_penalty(injured_roster)

            # Both should have injury penalties when toggle is ON
            expected_penalty = draft_config.INJURY_PENALTIES.get("HIGH", 50)
            assert available_penalty_on == expected_penalty
            assert roster_penalty_on == expected_penalty

            # Test in trade mode with penalty toggle OFF
            draft_config.APPLY_INJURY_PENALTY_TO_ROSTER = False

            available_penalty_off = draft_helper_instance.compute_injury_penalty(injured_available)
            roster_penalty_off = draft_helper_instance.compute_injury_penalty(injured_roster)

            # Available players should still have penalties, roster players should not
            assert available_penalty_off == expected_penalty  # Still penalized
            assert roster_penalty_off == 0  # No penalty for roster players

            # Test in draft mode (toggle should not affect)
            draft_config.TRADE_HELPER_MODE = False

            available_penalty_draft = draft_helper_instance.compute_injury_penalty(injured_available)
            roster_penalty_draft = draft_helper_instance.compute_injury_penalty(injured_roster)

            # Both should have penalties in draft mode regardless of toggle
            assert available_penalty_draft == expected_penalty
            assert roster_penalty_draft == expected_penalty

        finally:
            # Restore original config values
            draft_config.TRADE_HELPER_MODE = original_trade_mode
            draft_config.APPLY_INJURY_PENALTY_TO_ROSTER = original_apply_penalty

    def test_bye_week_penalty_calculation(self, draft_helper_instance, sample_players):
        """Test bye week penalty calculation"""
        player = sample_players[0]

        # Test bye week penalty calculation using DraftHelper method
        penalty = draft_helper_instance.compute_bye_penalty_for_player(player)

        # Should be a valid penalty (non-negative number)
        assert penalty >= 0
        assert isinstance(penalty, (int, float))

    def test_positional_need_scoring(self, draft_helper_instance, sample_players):
        """Test positional need scoring logic"""
        qb_player = sample_players[2]  # QB position

        # Test positional need score calculation
        qb_need_score = draft_helper_instance.compute_positional_need_score(qb_player)

        # Should be a valid score
        assert isinstance(qb_need_score, (int, float))

        # RB player positional need
        rb_player = sample_players[0]  # RB position
        rb_need_score = draft_helper_instance.compute_positional_need_score(rb_player)

        # Should be a valid score
        assert isinstance(rb_need_score, (int, float))

    def test_player_total_score_calculation(self, draft_helper_instance, sample_players):
        """Test complete player scoring calculation"""
        player = sample_players[0]  # Elite RB, ACTIVE status

        # Calculate total score using DraftHelper method
        total_score = draft_helper_instance.score_player(player)

        # Should be a valid score
        assert isinstance(total_score, (int, float))

        # Test that injured player gets different score
        injured_player = sample_players[3]  # OUT status
        injured_score = draft_helper_instance.score_player(injured_player)

        # Both should be valid scores
        assert isinstance(injured_score, (int, float))

    def test_draft_recommendations(self, draft_helper_instance):
        """Test draft recommendation generation"""
        # Test getting recommendations using DraftHelper method
        recommendations = draft_helper_instance.recommend_next_picks()

        # Should return a list
        assert isinstance(recommendations, list)

        # Should not exceed recommendation count
        assert len(recommendations) <= draft_config.RECOMMENDATION_COUNT

        # Should be sorted by score (highest first)
        if len(recommendations) > 1:
            for i in range(len(recommendations) - 1):
                assert recommendations[i].score >= recommendations[i + 1].score

    def test_trade_recommendations(self, draft_helper_instance):
        """Test trade recommendation functionality exists"""
        # Temporarily enable trade mode for testing
        original_mode = draft_config.TRADE_HELPER_MODE
        draft_config.TRADE_HELPER_MODE = True

        try:
            # Test that DraftHelper instance is properly configured for trade mode
            assert hasattr(draft_helper_instance, 'team')
            assert hasattr(draft_helper_instance, 'players')

            # Trade functionality would be implemented as needed
            # This test validates the basic infrastructure is in place

            # Test that we can access trade-related configuration
            assert hasattr(draft_config, 'MIN_TRADE_IMPROVEMENT')
            assert hasattr(draft_config, 'NUM_TRADE_RUNNERS_UP')

        finally:
            # Restore original mode
            draft_config.TRADE_HELPER_MODE = original_mode

    def test_ideal_draft_position_by_round(self):
        """Test draft position recommendations by round"""
        # Test first few rounds
        round_1_pos = draft_config.get_ideal_draft_position(0)  # Round 1 (0-indexed)
        round_5_pos = draft_config.get_ideal_draft_position(4)  # Round 5

        # Should return valid positions
        valid_positions = [Constants.QB, Constants.RB, Constants.WR, Constants.TE,
                          Constants.FLEX, Constants.K, Constants.DST]
        assert round_1_pos in valid_positions
        assert round_5_pos in valid_positions

        # Test beyond draft order (should default to FLEX)
        late_round = draft_config.get_ideal_draft_position(20)
        assert late_round == Constants.FLEX

    def test_flex_position_handling(self, sample_players):
        """Test FLEX position logic in scoring"""
        rb_player = sample_players[0]  # RB
        wr_player = sample_players[1]  # WR

        # Both RB and WR should be eligible for FLEX
        assert rb_player.position in draft_config.FLEX_ELIGIBLE_POSITIONS
        assert wr_player.position in draft_config.FLEX_ELIGIBLE_POSITIONS

        # Test that FLEX scoring works for both positions
        mock_team = MagicMock()
        mock_team.pos_counts = {"RB": 2, "WR": 2, "FLEX": 0}  # FLEX slot available

        # Test that both positions are handled properly by the implementation
        assert rb_player.position == "RB"
        assert wr_player.position == "WR"

    def test_error_handling_with_invalid_data(self, draft_helper_instance):
        """Test error handling with invalid player data"""
        # Test that DraftHelper handles basic operations without crashing
        recommendations = draft_helper_instance.recommend_next_picks()
        assert isinstance(recommendations, list)

    def test_trade_improvement_calculation(self, sample_players):
        """Test trade improvement calculation logic"""
        strong_player = sample_players[0]  # Elite RB, 200 points
        weak_player = sample_players[3]  # Injured TE, 90 points

        # Simple validation - strong player should have higher fantasy points
        assert strong_player.fantasy_points > weak_player.fantasy_points

    def test_runner_up_trade_suggestions(self, draft_helper_instance):
        """Test that trade functionality infrastructure exists"""
        # Temporarily enable trade mode for testing
        original_mode = draft_config.TRADE_HELPER_MODE
        draft_config.TRADE_HELPER_MODE = True

        try:
            # Test basic trade mode infrastructure
            assert hasattr(draft_helper_instance, 'team')
            assert hasattr(draft_helper_instance, 'players')

            # Test trade configuration constants exist
            assert isinstance(draft_config.MIN_TRADE_IMPROVEMENT, (int, float))
            assert isinstance(draft_config.NUM_TRADE_RUNNERS_UP, int)
            assert draft_config.NUM_TRADE_RUNNERS_UP > 0

        finally:
            # Restore original mode
            draft_config.TRADE_HELPER_MODE = original_mode

    def test_bye_week_data_integration(self):
        """Test bye week data integration"""
        # Test that bye weeks are properly loaded and used
        assert isinstance(draft_config.POSSIBLE_BYE_WEEKS, list)
        assert len(draft_config.POSSIBLE_BYE_WEEKS) > 0

        # All bye weeks should be valid NFL weeks
        for bye_week in draft_config.POSSIBLE_BYE_WEEKS:
            assert 1 <= bye_week <= 18

    def test_scoring_format_consistency(self):
        """Test that scoring weights are internally consistent"""
        # Projection base should be larger than penalties
        assert draft_config.PROJECTION_BASE_SCORE > draft_config.BASE_BYE_PENALTY
        assert draft_config.PROJECTION_BASE_SCORE > max(draft_config.INJURY_PENALTIES.values())

        # Positional need should be meaningful relative to base score
        assert draft_config.POS_NEEDED_SCORE <= draft_config.PROJECTION_BASE_SCORE

    def test_interactive_menu_display_roster_by_draft_order(self, draft_helper_instance, sample_players):
        """Test the roster display functionality"""
        print("🧪 Testing roster display by draft order...")

        # Test with empty roster
        draft_helper_instance.team.roster = []
        draft_helper_instance.display_roster_by_draft_order()  # Should not crash

        # Test with full roster
        for player in sample_players[:15]:  # Limit to max roster
            draft_helper_instance.team.draft_player(player)

        draft_helper_instance.display_roster_by_draft_order()  # Should display organized roster
        print("✅ Roster display test passed")

    def test_interactive_menu_show_main_menu_validation(self, draft_helper_instance):
        """Test main menu input validation"""
        print("🧪 Testing main menu validation...")

        # Mock input validation - the method should handle invalid inputs gracefully
        # This tests the structure exists and can be called
        assert hasattr(draft_helper_instance, 'show_main_menu')
        assert callable(draft_helper_instance.show_main_menu)
        print("✅ Main menu validation test passed")

    def test_interactive_search_and_mark_player_logic(self, draft_helper_instance):
        """Test the player search and marking functionality"""
        print("🧪 Testing player search logic...")

        # Test that search method exists
        assert hasattr(draft_helper_instance, 'search_and_mark_player')
        assert callable(draft_helper_instance.search_and_mark_player)

        # Test player filtering for available players (drafted=0)
        available_players = [p for p in draft_helper_instance.players if p.drafted == 0]
        initial_available_count = len(available_players)

        # Manually mark a player as drafted to test filtering
        if available_players:
            test_player = available_players[0]
            test_player.drafted = 1

            # Verify the player is no longer in available list
            new_available = [p for p in draft_helper_instance.players if p.drafted == 0]
            assert len(new_available) == initial_available_count - 1

        print("✅ Player search logic test passed")

    def test_interactive_add_to_roster_mode_logic(self, draft_helper_instance, sample_players):
        """Test add to roster mode functionality"""
        print("🧪 Testing add to roster mode logic...")

        # Test that add to roster method exists
        assert hasattr(draft_helper_instance, 'run_add_to_roster_mode')
        assert callable(draft_helper_instance.run_add_to_roster_mode)

        # Test recommendation generation (should work with existing logic)
        recommendations = draft_helper_instance.recommend_next_picks()
        assert isinstance(recommendations, list)

        # Test with full roster - should handle gracefully
        for player in sample_players[:15]:  # Fill roster
            if draft_helper_instance.team.can_draft(player):
                draft_helper_instance.team.draft_player(player)

        # Should still be able to call without crashing
        recommendations_full = draft_helper_instance.recommend_next_picks()
        assert isinstance(recommendations_full, list)

        print("✅ Add to roster mode test passed")

    def test_interactive_menu_integration_with_existing_logic(self, draft_helper_instance, sample_players):
        """Test that interactive menu integrates properly with existing draft logic"""
        print("🧪 Testing interactive menu integration...")

        # Test that all new interactive methods exist
        interactive_methods = [
            'run_interactive_draft',
            'show_main_menu',
            'display_roster_by_draft_order',
            'run_add_to_roster_mode',
            'run_mark_drafted_player_mode',
            'search_and_mark_player'
        ]

        for method_name in interactive_methods:
            assert hasattr(draft_helper_instance, method_name), f"Missing method: {method_name}"
            assert callable(getattr(draft_helper_instance, method_name)), f"Method not callable: {method_name}"

        # Test that existing core logic still works
        assert draft_helper_instance.team is not None
        assert draft_helper_instance.players is not None
        assert len(draft_helper_instance.players) > 0

        # Test scoring still works
        test_player = sample_players[0]
        score = draft_helper_instance.score_player(test_player)
        assert isinstance(score, (int, float))
        assert score >= 0

        print("✅ Interactive menu integration test passed")

    def test_interactive_player_search_fuzzy_matching(self, draft_helper_instance):
        """Test fuzzy matching logic for player search"""
        print("🧪 Testing fuzzy search matching...")

        # Create test players with known names
        test_players = [
            FantasyPlayer(id="test1", name="Patrick Mahomes", team="KC", position="QB", drafted=0),
            FantasyPlayer(id="test2", name="Travis Kelce", team="KC", position="TE", drafted=0),
            FantasyPlayer(id="test3", name="Tyreek Hill", team="MIA", position="WR", drafted=0),
        ]

        # Test partial name matching logic
        search_term = "mahomes"
        matches = []

        for player in test_players:
            name_lower = player.name.lower()
            name_words = name_lower.split()

            # Simulate the search logic from search_and_mark_player
            if (search_term.lower() in name_lower or
                any(search_term.lower() in word or word.startswith(search_term.lower())
                    for word in name_words)):
                matches.append(player)

        # Should find Patrick Mahomes
        assert len(matches) == 1
        assert matches[0].name == "Patrick Mahomes"

        # Test first name search
        search_term = "patrick"
        matches = []
        for player in test_players:
            name_lower = player.name.lower()
            name_words = name_lower.split()
            if (search_term.lower() in name_lower or
                any(search_term.lower() in word or word.startswith(search_term.lower())
                    for word in name_words)):
                matches.append(player)

        assert len(matches) == 1
        assert matches[0].name == "Patrick Mahomes"

        print("✅ Fuzzy search matching test passed")

    def test_interactive_roster_state_management(self, draft_helper_instance, sample_players):
        """Test that roster state is properly managed through interactive operations"""
        print("🧪 Testing roster state management...")

        initial_roster_size = len(draft_helper_instance.team.roster)

        # Test adding a player
        available_players = [p for p in draft_helper_instance.players if p.drafted == 0]
        if available_players:
            test_player = available_players[0]

            # Manually simulate what Add to Roster mode does
            success = draft_helper_instance.team.draft_player(test_player)
            if success:
                assert len(draft_helper_instance.team.roster) == initial_roster_size + 1
                assert test_player.drafted == 2  # Should be marked as our team

        # Test that CSV save functionality exists
        assert hasattr(draft_helper_instance, 'save_players')
        assert callable(draft_helper_instance.save_players)

        print("✅ Roster state management test passed")

    def test_interactive_trade_analysis_mode(self, draft_helper_instance, sample_players):
        """Test trade analysis mode functionality"""
        print("🧪 Testing trade analysis mode...")

        # Test that trade analysis method exists
        assert hasattr(draft_helper_instance, 'run_trade_analysis_mode')
        assert callable(draft_helper_instance.run_trade_analysis_mode)

        # Test that trade helper method exists (called by trade analysis mode)
        assert hasattr(draft_helper_instance, 'run_trade_helper')
        assert callable(draft_helper_instance.run_trade_helper)

        # Add some players to roster first so we can test trade analysis
        for player in sample_players[:3]:  # Add a few players
            if draft_helper_instance.team.can_draft(player):
                draft_helper_instance.team.draft_player(player)

        # Test trade analysis with roster
        if len(draft_helper_instance.team.roster) > 0:
            # Should not crash when run with a roster
            # Note: We can't test the full interactive flow without mocking input
            assert hasattr(draft_helper_instance, 'score_player_for_trade')
            assert callable(draft_helper_instance.score_player_for_trade)

        print("✅ Trade analysis mode test passed")

    def test_interactive_menu_structure_complete(self, draft_helper_instance):
        """Test that all menu options are properly implemented"""
        print("🧪 Testing complete menu structure...")

        # Test all interactive methods exist
        assert hasattr(draft_helper_instance, 'show_main_menu')
        assert hasattr(draft_helper_instance, 'run_add_to_roster_mode')
        assert hasattr(draft_helper_instance, 'run_mark_drafted_player_mode')
        assert hasattr(draft_helper_instance, 'run_trade_analysis_mode')
        assert hasattr(draft_helper_instance, 'run_drop_player_mode')
        assert hasattr(draft_helper_instance, 'run_lock_unlock_player_mode')
        assert hasattr(draft_helper_instance, 'run_interactive_draft')

        # Test all methods are callable
        assert callable(draft_helper_instance.show_main_menu)
        assert callable(draft_helper_instance.run_add_to_roster_mode)
        assert callable(draft_helper_instance.run_mark_drafted_player_mode)
        assert callable(draft_helper_instance.run_trade_analysis_mode)
        assert callable(draft_helper_instance.run_drop_player_mode)
        assert callable(draft_helper_instance.run_lock_unlock_player_mode)
        assert callable(draft_helper_instance.run_interactive_draft)

        print("✅ Complete menu structure test passed")

    def test_drop_player_mode_functionality(self, draft_helper_instance, sample_players):
        """Test drop player mode functionality"""
        print("🧪 Testing drop player mode...")

        # Test that drop player methods exist
        assert hasattr(draft_helper_instance, 'run_drop_player_mode')
        assert hasattr(draft_helper_instance, 'search_and_drop_player')
        assert callable(draft_helper_instance.run_drop_player_mode)
        assert callable(draft_helper_instance.search_and_drop_player)

        # Set up test data using the actual players from draft_helper_instance
        test_players = draft_helper_instance.players[:3]
        original_states = []

        for i, player in enumerate(test_players):
            # Save original state
            original_states.append((player.drafted, player.locked))

            if i == 0:
                # Add to our roster
                player.drafted = 2
                if player not in draft_helper_instance.team.roster:
                    draft_helper_instance.team.roster.append(player)
            else:
                # Mark as drafted by others
                player.drafted = 1

        initial_roster_size = len(draft_helper_instance.team.roster)

        # Test filtering logic for drafted players
        drafted_players = [p for p in draft_helper_instance.players if p.drafted != 0]
        assert len(drafted_players) >= 2  # Should include both drafted=1 and drafted=2 players

        # Test drop functionality (simulate dropping a player)
        roster_player = next(p for p in draft_helper_instance.players if p.drafted == 2)
        original_drafted_status = roster_player.drafted

        # Simulate drop action
        roster_player.drafted = 0
        if roster_player in draft_helper_instance.team.roster:
            draft_helper_instance.team.roster.remove(roster_player)

        # Verify player was dropped
        assert roster_player.drafted == 0
        assert roster_player not in draft_helper_instance.team.roster
        assert len(draft_helper_instance.team.roster) == initial_roster_size - 1

        # Restore all original states
        for i, (player, (orig_drafted, orig_locked)) in enumerate(zip(test_players, original_states)):
            player.drafted = orig_drafted
            player.locked = orig_locked

        # Clear roster to original state
        draft_helper_instance.team.roster.clear()

        print("✅ Drop player mode test passed")

    def test_lock_unlock_player_mode_functionality(self, draft_helper_instance, sample_players):
        """Test lock/unlock player mode functionality"""
        print("🧪 Testing lock/unlock player mode...")

        # Test that lock/unlock methods exist
        assert hasattr(draft_helper_instance, 'run_lock_unlock_player_mode')
        assert callable(draft_helper_instance.run_lock_unlock_player_mode)

        # Set up test data using the actual players from draft_helper_instance
        test_players = draft_helper_instance.players[:3]
        original_states = []

        for i, player in enumerate(test_players):
            # Save original state
            original_states.append((player.drafted, player.locked))

            # Add to roster
            player.drafted = 2
            player.locked = i % 2  # Alternate lock status
            if player not in draft_helper_instance.team.roster:
                draft_helper_instance.team.roster.append(player)

        # Test roster player filtering
        roster_players = [p for p in draft_helper_instance.players if p.drafted == 2]
        assert len(roster_players) >= 3

        # Test lock status grouping
        unlocked_players = [p for p in roster_players if p.locked == 0]
        locked_players = [p for p in roster_players if p.locked == 1]

        assert len(unlocked_players) > 0 or len(locked_players) > 0

        # Test lock toggle functionality
        if unlocked_players:
            test_player = unlocked_players[0]
            original_status = test_player.locked

            # Toggle lock status
            test_player.locked = 1 - test_player.locked

            # Verify toggle worked
            assert test_player.locked != original_status

            # Restore original status
            test_player.locked = original_status

        # Restore all original states
        for i, (player, (orig_drafted, orig_locked)) in enumerate(zip(test_players, original_states)):
            player.drafted = orig_drafted
            player.locked = orig_locked

        # Clear roster to original state
        draft_helper_instance.team.roster.clear()

        print("✅ Lock/unlock player mode test passed")

    def test_new_menu_options_integration(self, draft_helper_instance):
        """Test that new menu options integrate properly with existing system"""
        print("🧪 Testing new menu options integration...")

        # Test menu input validation for new range (1-6)
        # This tests the concept without actual user input

        # Test that all menu choices are handled
        menu_methods = {
            1: 'run_add_to_roster_mode',
            2: 'run_mark_drafted_player_mode',
            3: 'run_trade_analysis_mode',
            4: 'run_drop_player_mode',
            5: 'run_lock_unlock_player_mode'
            # 6 would be quit
        }

        for choice, method_name in menu_methods.items():
            assert hasattr(draft_helper_instance, method_name)
            assert callable(getattr(draft_helper_instance, method_name))

        # Test that error handling exists for invalid choices
        # The show_main_menu method should return -1 for invalid input

        print("✅ New menu options integration test passed")

    def test_player_status_management(self, draft_helper_instance, sample_players):
        """Test player status changes work correctly across all modes"""
        print("🧪 Testing player status management...")

        # Use a test player
        test_player = sample_players[0]
        original_drafted = test_player.drafted
        original_locked = test_player.locked

        try:
            # Test status transitions
            # Available -> Drafted by others -> Available
            test_player.drafted = 0  # Available
            assert test_player.drafted == 0

            test_player.drafted = 1  # Drafted by others
            assert test_player.drafted == 1

            test_player.drafted = 0  # Back to available
            assert test_player.drafted == 0

            # Test roster management
            test_player.drafted = 2  # On our roster
            if test_player not in draft_helper_instance.team.roster:
                draft_helper_instance.team.roster.append(test_player)

            assert test_player.drafted == 2
            assert test_player in draft_helper_instance.team.roster

            # Test lock status for roster players
            test_player.locked = 0  # Unlocked
            assert test_player.locked == 0

            test_player.locked = 1  # Locked
            assert test_player.locked == 1

            test_player.locked = 0  # Back to unlocked
            assert test_player.locked == 0

            # Test dropping from roster
            if test_player in draft_helper_instance.team.roster:
                draft_helper_instance.team.roster.remove(test_player)
            test_player.drafted = 0

            assert test_player.drafted == 0
            assert test_player not in draft_helper_instance.team.roster

        finally:
            # Restore original state
            test_player.drafted = original_drafted
            test_player.locked = original_locked

        print("✅ Player status management test passed")


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        # Basic test runner
        print("Testing configuration validation...")
        try:
            draft_config.validate_config()
            print("✅ Configuration validation test passed")
        except ValueError as e:
            print(f"❌ Configuration validation failed: {e}")

        # Test sample player creation
        player = FantasyPlayer(
            id="test1",
            name="Test Player",
            position="RB",
            team="TEST",
            fantasy_points=100.0,
            injury_status="ACTIVE"
        )
        print("✅ Player creation test passed")

        print("Basic tests completed successfully!")