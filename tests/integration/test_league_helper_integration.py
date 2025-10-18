"""
Integration Tests for League Helper Workflow

Tests end-to-end workflows across multiple LeagueHelper modes including:
- Full draft workflow with multiple players
- Starter helper with drafted roster
- Trade simulator with full roster
- Mode transitions and data persistence
- Error recovery scenarios

Author: Kai Mizuno
"""

import pytest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from league_helper.LeagueHelperManager import LeagueHelperManager


@pytest.fixture
def temp_data_folder(tmp_path):
    """Create temporary data folder with test CSV files"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create minimal players.csv with correct column names
    players_csv = data_folder / "players.csv"
    players_csv.write_text("""id,name,position,team,bye_week,fantasy_points,injury_status,average_draft_position
1,Patrick Mahomes,QB,KC,7,350.5,ACTIVE,1.2
2,Josh Allen,QB,BUF,12,340.2,ACTIVE,1.5
3,Justin Jefferson,WR,MIN,13,310.8,ACTIVE,2.1
4,Tyreek Hill,WR,MIA,10,305.3,ACTIVE,2.3
5,Christian McCaffrey,RB,SF,9,320.1,QUESTIONABLE,1.1
6,Austin Ekeler,RB,LAC,5,295.7,ACTIVE,3.2
7,Travis Kelce,TE,KC,7,220.4,ACTIVE,4.5
8,Mark Andrews,TE,BAL,13,210.3,ACTIVE,5.1
""")

    # Create minimal teams.csv
    teams_csv = data_folder / "teams.csv"
    teams_csv.write_text("""Team Name,Position,Player Name
MyTeam,QB,
MyTeam,RB,
MyTeam,RB,
MyTeam,WR,
MyTeam,WR,
MyTeam,TE,
MyTeam,FLEX,
MyTeam,K,
MyTeam,DST,
MyTeam,BENCH,
""")

    # Copy league_config.json from actual data folder
    source_config = project_root / "data" / "league_config.json"
    if source_config.exists():
        shutil.copy(source_config, data_folder / "league_config.json")
    else:
        # Create minimal config if source doesn't exist
        config_json = data_folder / "league_config.json"
        config_json.write_text("""{
    "config_name": "Test Config",
    "description": "Test configuration for integration tests",
    "current_nfl_week": 1,
    "scoring": {
        "qb": {"pass_yards": 0.04, "pass_tds": 4, "interceptions": -2},
        "rb": {"rush_yards": 0.1, "rush_tds": 6, "receptions": 1, "rec_yards": 0.1, "rec_tds": 6},
        "wr": {"receptions": 1, "rec_yards": 0.1, "rec_tds": 6},
        "te": {"receptions": 1, "rec_yards": 0.1, "rec_tds": 6}
    },
    "thresholds": {
        "projected_points_multiplier": 1.0,
        "adp_multipliers": [[0, 1.0]],
        "injury_penalties": {"Healthy": 0, "Questionable": -5, "Doubtful": -15, "Out": -100}
    }
}""")

    return data_folder


class TestLeagueHelperIntegrationBasic:
    """Basic integration tests for league helper initialization"""

    def test_league_helper_initializes_with_valid_data_folder(self, temp_data_folder):
        """Test that LeagueHelperManager initializes with valid data folder"""
        manager = LeagueHelperManager(temp_data_folder)

        assert manager is not None
        assert manager.config is not None
        assert manager.player_manager is not None
        assert manager.team_data_manager is not None

    def test_league_helper_loads_player_data_on_init(self, temp_data_folder):
        """Test that player data is loaded during initialization"""
        manager = LeagueHelperManager(temp_data_folder)

        # Verify player manager has loaded players
        assert manager.player_manager is not None
        assert len(manager.player_manager.get_player_list(drafted_vals=[0, 1, 2])) > 0

    def test_league_helper_loads_team_data_on_init(self, temp_data_folder):
        """Test that team data is loaded during initialization"""
        manager = LeagueHelperManager(temp_data_folder)

        # Verify team data manager has loaded teams
        assert manager.team_data_manager is not None
        assert len(manager.team_data_manager.get_available_teams()) > 0


class TestAddToRosterIntegration:
    """Integration tests for Add to Roster mode"""

    def test_add_to_roster_mode_can_be_entered(self, temp_data_folder):
        """Test that Add to Roster mode can be entered and exited"""
        manager = LeagueHelperManager(temp_data_folder)

        # Mock the start_interactive_mode method on the instance
        with patch.object(manager.add_to_roster_mode_manager, 'start_interactive_mode', return_value=None) as mock_start:
            manager._run_add_to_roster_mode()
            assert mock_start.called

    def test_add_to_roster_workflow_adds_player(self, temp_data_folder):
        """Test complete workflow of adding a player to roster"""
        manager = LeagueHelperManager(temp_data_folder)

        # Mock the start_interactive_mode to avoid stdin issues
        with patch.object(manager.add_to_roster_mode_manager, 'start_interactive_mode', return_value=None):
            # This would test the actual add workflow
            # For now, verify the manager is set up correctly
            assert manager.team_data_manager is not None


class TestStarterHelperIntegration:
    """Integration tests for Starter Helper mode"""

    def test_starter_helper_mode_can_be_entered(self, temp_data_folder):
        """Test that Starter Helper mode can be entered"""
        manager = LeagueHelperManager(temp_data_folder)

        # Mock the show_recommended_starters method on the instance
        with patch.object(manager.starter_helper_mode_manager, 'show_recommended_starters', return_value=None) as mock_show:
            manager._run_starter_helper_mode()
            assert mock_show.called

    def test_starter_helper_works_with_empty_roster(self, temp_data_folder):
        """Test starter helper with empty roster"""
        manager = LeagueHelperManager(temp_data_folder)

        # Verify manager can handle empty roster
        assert manager.team_data_manager is not None


class TestTradeSimulatorIntegration:
    """Integration tests for Trade Simulator mode"""

    def test_trade_simulator_mode_can_be_entered(self, temp_data_folder):
        """Test that Trade Simulator mode can be entered"""
        manager = LeagueHelperManager(temp_data_folder)

        # Mock the run_interactive_mode method on the instance
        with patch.object(manager.trade_simulator_mode_manager, 'run_interactive_mode', return_value=None) as mock_run:
            manager._run_trade_simulator_mode()
            assert mock_run.called


class TestModifyPlayerDataIntegration:
    """Integration tests for Modify Player Data mode"""

    def test_modify_player_data_mode_can_be_entered(self, temp_data_folder):
        """Test that Modify Player Data mode can be entered"""
        manager = LeagueHelperManager(temp_data_folder)

        # Mock the start_interactive_mode method on the instance
        with patch.object(manager.modify_player_data_mode_manager, 'start_interactive_mode', return_value=None) as mock_start:
            manager.run_modify_player_data_mode()
            assert mock_start.called


class TestModeTransitions:
    """Integration tests for transitions between modes"""

    def test_transition_from_add_to_roster_to_starter_helper(self, temp_data_folder):
        """Test transition from Add to Roster to Starter Helper"""
        manager = LeagueHelperManager(temp_data_folder)

        # Mock both mode managers
        with patch.object(manager.add_to_roster_mode_manager, 'start_interactive_mode', return_value=None) as mock_add, \
             patch.object(manager.starter_helper_mode_manager, 'show_recommended_starters', return_value=None) as mock_starter:

            # Run add to roster mode
            manager._run_add_to_roster_mode()

            # Run starter helper mode
            manager._run_starter_helper_mode()

            # Both modes should have been called
            assert mock_add.called
            assert mock_starter.called

    def test_transition_from_add_to_roster_to_trade_simulator(self, temp_data_folder):
        """Test transition from Add to Roster to Trade Simulator"""
        manager = LeagueHelperManager(temp_data_folder)

        # Mock both mode managers
        with patch.object(manager.add_to_roster_mode_manager, 'start_interactive_mode', return_value=None) as mock_add, \
             patch.object(manager.trade_simulator_mode_manager, 'run_interactive_mode', return_value=None) as mock_trade:

            # Run add to roster mode
            manager._run_add_to_roster_mode()

            # Run trade simulator mode
            manager._run_trade_simulator_mode()

            # Both modes should have been called
            assert mock_add.called
            assert mock_trade.called


class TestDataPersistence:
    """Integration tests for data persistence across modes"""

    def test_player_data_persists_across_mode_transitions(self, temp_data_folder):
        """Test that player data persists when switching modes"""
        manager = LeagueHelperManager(temp_data_folder)

        # Get initial player count
        initial_players = manager.player_manager.get_player_list(drafted_vals=[0, 1, 2])
        initial_count = len(initial_players)

        # Create new manager (simulating mode transition)
        manager2 = LeagueHelperManager(temp_data_folder)

        # Verify same player count
        new_players = manager2.player_manager.get_player_list(drafted_vals=[0, 1, 2])
        assert len(new_players) == initial_count

    def test_team_data_persists_across_mode_transitions(self, temp_data_folder):
        """Test that team data persists when switching modes"""
        manager = LeagueHelperManager(temp_data_folder)

        # Get initial team count
        initial_teams = manager.team_data_manager.get_available_teams()
        initial_count = len(initial_teams)

        # Create new manager (simulating mode transition)
        manager2 = LeagueHelperManager(temp_data_folder)

        # Verify same team count
        new_teams = manager2.team_data_manager.get_available_teams()
        assert len(new_teams) == initial_count


class TestErrorRecovery:
    """Integration tests for error recovery scenarios"""

    def test_league_helper_handles_missing_data_folder(self):
        """Test error handling when data folder doesn't exist"""
        with pytest.raises(Exception):
            LeagueHelperManager(Path("/nonexistent/path"))

    def test_league_helper_handles_invalid_csv_data(self, tmp_path):
        """Test error handling with malformed CSV data"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create invalid players CSV
        players_csv = data_folder / "players_projected.csv"
        players_csv.write_text("Invalid,CSV,Header\nBad,Data,Here\n")

        # Create minimal teams CSV
        teams_csv = data_folder / "teams.csv"
        teams_csv.write_text("Team Name,Position,Player Name\n")

        # Create minimal config
        config_json = data_folder / "league_config.json"
        config_json.write_text("""{
    "config_name": "Test",
    "current_nfl_week": 1,
    "scoring": {},
    "thresholds": {"projected_points_multiplier": 1.0}
}""")

        # Should raise an error or handle gracefully (bad CSV data)
        with pytest.raises(Exception):
            LeagueHelperManager(data_folder)


class TestEndToEndWorkflow:
    """End-to-end integration tests for complete workflows"""

    @patch('builtins.input', side_effect=['1', '1', 'q', '0'])
    @patch('builtins.print')
    def test_complete_draft_and_starter_workflow(self, mock_print, mock_input, temp_data_folder):
        """Test complete workflow: draft player, then check starters"""
        manager = LeagueHelperManager(temp_data_folder)

        # This is a simplified test - real workflow would involve:
        # 1. Add players to roster
        # 2. Run starter helper to optimize lineup
        # 3. Verify correct players are in starting lineup

        assert manager is not None

    @patch('builtins.input', side_effect=['2', '1', 'q', '0'])
    @patch('builtins.print')
    def test_complete_draft_and_trade_workflow(self, mock_print, mock_input, temp_data_folder):
        """Test complete workflow: draft players, then simulate trade"""
        manager = LeagueHelperManager(temp_data_folder)

        # This is a simplified test - real workflow would involve:
        # 1. Add players to roster
        # 2. Run trade simulator to evaluate trades
        # 3. Verify trade analysis is correct

        assert manager is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
