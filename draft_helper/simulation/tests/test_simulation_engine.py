"""
Unit tests for simulation engine.
"""

import unittest
import pandas as pd
import sys
import os
from unittest.mock import Mock, patch

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from draft_helper.simulation.simulation_engine import DraftSimulationEngine, DraftPick, SimulationTeam
from shared_files.FantasyPlayer import FantasyPlayer


class TestDraftSimulationEngine(unittest.TestCase):
    """Test cases for DraftSimulationEngine"""

    def setUp(self):
        """Set up test data"""
        # Create sample player data
        self.sample_players_df = pd.DataFrame({
            'name': ['Player A', 'Player B', 'Player C', 'Player D', 'Player E'],
            'position': ['QB', 'RB', 'WR', 'TE', 'K'],
            'team': ['Team1', 'Team2', 'Team3', 'Team4', 'Team5'],
            'injury_status': ['LOW', 'LOW', 'MEDIUM', 'LOW', 'LOW'],
            'bye_week': [6, 7, 8, 9, 10],
            'drafted': [0, 0, 0, 0, 0],
            'week_1_points': [25.0, 15.0, 12.0, 8.0, 5.0],
            'week_2_points': [23.0, 18.0, 14.0, 6.0, 4.0]
        })

        self.config_params = {
            'INJURY_PENALTIES_MEDIUM': 25,
            'INJURY_PENALTIES_HIGH': 50,
            'POS_NEEDED_SCORE': 50,
            'PROJECTION_BASE_SCORE': 100,
            'BASE_BYE_PENALTY': 20
        }

    def test_engine_initialization(self):
        """Test engine initializes correctly"""
        engine = DraftSimulationEngine(self.sample_players_df, self.config_params)

        self.assertEqual(len(engine.teams), 10)  # Should create 10 teams
        self.assertEqual(len(engine.available_players), 5)  # 5 available players
        self.assertEqual(engine.current_round, 1)
        self.assertEqual(engine.current_pick, 1)

    def test_team_initialization(self):
        """Test teams are initialized with correct strategies"""
        engine = DraftSimulationEngine(self.sample_players_df, self.config_params)

        # Check that we have the right number of each strategy
        strategy_counts = {}
        for team in engine.teams:
            strategy = team.strategy
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

        # Should match TEAM_STRATEGIES from config
        expected_strategies = {
            'conservative': 2,
            'aggressive': 2,
            'positional': 2,
            'value': 3,
            'draft_helper': 1
        }

        self.assertEqual(strategy_counts, expected_strategies)

    def test_available_players_initialization(self):
        """Test available players are correctly initialized"""
        engine = DraftSimulationEngine(self.sample_players_df, self.config_params)

        self.assertEqual(len(engine.available_players), 5)

        # Check that players have correct data
        player_names = [p.name for p in engine.available_players]
        self.assertIn('Player A', player_names)
        self.assertIn('Player B', player_names)

        # Check week points are loaded
        for player in engine.available_players:
            # Check that player has weekly points
            self.assertIsNotNone(getattr(player, 'week_1_points', None))

    def test_draft_order_snake_format(self):
        """Test snake draft order is correct"""
        engine = DraftSimulationEngine(self.sample_players_df, self.config_params)

        # Round 1: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
        round1_order = engine.get_draft_order(1)
        expected_round1 = list(range(10))
        self.assertEqual(round1_order, expected_round1)

        # Round 2: 9, 8, 7, 6, 5, 4, 3, 2, 1, 0
        round2_order = engine.get_draft_order(2)
        expected_round2 = list(range(9, -1, -1))
        self.assertEqual(round2_order, expected_round2)

    @patch('draft_helper.simulation.team_strategies.TeamStrategyManager')
    def test_make_team_pick(self, mock_strategy_manager_class):
        """Test making a team pick"""
        # Setup mock
        mock_strategy_manager = Mock()
        mock_strategy_manager_class.return_value = mock_strategy_manager

        # Mock strategy manager to return first available player
        engine = DraftSimulationEngine(self.sample_players_df, self.config_params)
        mock_strategy_manager.get_team_picks.return_value = engine.available_players[:3]

        team = engine.teams[0]
        picked_player = engine._make_team_pick(team, 1)

        self.assertIsNotNone(picked_player)
        self.assertIn(picked_player, engine.available_players)

    def test_draft_pick_dataclass(self):
        """Test DraftPick dataclass"""
        player = FantasyPlayer(id="test1", name="Test Player", team="Team1", position="QB")
        pick = DraftPick(
            round_num=1,
            pick_num=1,
            team_index=0,
            player=player,
            strategy_used="conservative"
        )

        self.assertEqual(pick.round_num, 1)
        self.assertEqual(pick.pick_num, 1)
        self.assertEqual(pick.team_index, 0)
        self.assertEqual(pick.player, player)
        self.assertEqual(pick.strategy_used, "conservative")

    def test_simulation_team_dataclass(self):
        """Test SimulationTeam dataclass"""
        from draft_helper.FantasyTeam import FantasyTeam

        roster = FantasyTeam()
        team = SimulationTeam(
            team_index=0,
            strategy="conservative",
            roster=roster,
            draft_picks=[]
        )

        self.assertEqual(team.team_index, 0)
        self.assertEqual(team.strategy, "conservative")
        self.assertEqual(team.roster, roster)
        self.assertEqual(len(team.draft_picks), 0)

    def test_get_team_by_index(self):
        """Test getting team by index"""
        engine = DraftSimulationEngine(self.sample_players_df, self.config_params)

        # Valid index - after shuffle, team at list index 0 might have any team_index
        team = engine.get_team_by_index(0)
        self.assertIsNotNone(team)
        self.assertIsInstance(team.team_index, int)
        self.assertGreaterEqual(team.team_index, 0)
        self.assertLess(team.team_index, 10)

        # Invalid index
        team = engine.get_team_by_index(15)
        self.assertIsNone(team)

        team = engine.get_team_by_index(-1)
        self.assertIsNone(team)


class TestDraftPickAndTeamDataClasses(unittest.TestCase):
    """Test the dataclasses used in simulation"""

    def test_draft_pick_creation(self):
        """Test creating DraftPick objects"""
        player = FantasyPlayer(id="test2", name="Test Player", team="Team1", position="RB")
        pick = DraftPick(1, 5, 2, player, "aggressive")

        self.assertEqual(pick.round_num, 1)
        self.assertEqual(pick.pick_num, 5)
        self.assertEqual(pick.team_index, 2)
        self.assertEqual(pick.player.name, "Test Player")
        self.assertEqual(pick.strategy_used, "aggressive")

    def test_simulation_team_creation(self):
        """Test creating SimulationTeam objects"""
        from draft_helper.FantasyTeam import FantasyTeam

        roster = FantasyTeam()
        team = SimulationTeam(3, "value", roster, [])

        self.assertEqual(team.team_index, 3)
        self.assertEqual(team.strategy, "value")
        self.assertIsInstance(team.roster, FantasyTeam)
        self.assertEqual(len(team.draft_picks), 0)


if __name__ == '__main__':
    unittest.main()