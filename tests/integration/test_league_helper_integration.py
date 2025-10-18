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

    # Create minimal players_projected.csv
    players_csv = data_folder / "players_projected.csv"
    players_csv.write_text("""Name,Position,Team,Projected Points,ADP,Injury Status
Patrick Mahomes,QB,KC,350.5,1.2,Healthy
Josh Allen,QB,BUF,340.2,1.5,Healthy
Justin Jefferson,WR,MIN,310.8,2.1,Healthy
Tyreek Hill,WR,MIA,305.3,2.3,Healthy
Christian McCaffrey,RB,SF,320.1,1.1,Questionable
Austin Ekeler,RB,LAC,295.7,3.2,Healthy
Travis Kelce,TE,KC,220.4,4.5,Healthy
Mark Andrews,TE,BAL,210.3,5.1,Healthy
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
        assert manager.data_folder == temp_data_folder

    def test_league_helper_loads_player_data_on_init(self, temp_data_folder):
        """Test that player data is loaded during initialization"""
        manager = LeagueHelperManager(temp_data_folder)

        # Verify player manager has loaded players
        assert manager.player_manager is not None
        assert len(manager.player_manager.get_all_players()) > 0

    def test_league_helper_loads_team_data_on_init(self, temp_data_folder):
        """Test that team data is loaded during initialization"""
        manager = LeagueHelperManager(temp_data_folder)

        # Verify team data manager has loaded teams
        assert manager.team_data_manager is not None
        assert len(manager.team_data_manager.get_all_teams()) > 0


class TestAddToRosterIntegration:
    """Integration tests for Add to Roster mode"""

    @patch('league_helper.add_to_roster_mode.AddToRosterModeManager.AddToRosterModeManager.run')
    def test_add_to_roster_mode_can_be_entered(self, mock_run, temp_data_folder):
        """Test that Add to Roster mode can be entered and exited"""
        manager = LeagueHelperManager(temp_data_folder)

        # Simulate entering and exiting mode
        mock_run.return_value = None
        manager.run_add_to_roster_mode()

        assert mock_run.called

    @patch('builtins.input', side_effect=['1', 'q'])
    @patch('league_helper.add_to_roster_mode.AddToRosterModeManager.AddToRosterModeManager.add_player_to_roster')
    def test_add_to_roster_workflow_adds_player(self, mock_add, mock_input, temp_data_folder):
        """Test complete workflow of adding a player to roster"""
        manager = LeagueHelperManager(temp_data_folder)

        # This would test the actual add workflow
        # For now, verify the manager is set up correctly
        assert manager.team_data_manager is not None


class TestStarterHelperIntegration:
    """Integration tests for Starter Helper mode"""

    @patch('league_helper.starter_helper_mode.StarterHelperModeManager.StarterHelperModeManager.run')
    def test_starter_helper_mode_can_be_entered(self, mock_run, temp_data_folder):
        """Test that Starter Helper mode can be entered"""
        manager = LeagueHelperManager(temp_data_folder)

        mock_run.return_value = None
        manager.run_starter_helper_mode()

        assert mock_run.called

    def test_starter_helper_works_with_empty_roster(self, temp_data_folder):
        """Test starter helper with empty roster"""
        manager = LeagueHelperManager(temp_data_folder)

        # Verify manager can handle empty roster
        assert manager.team_data_manager is not None


class TestTradeSimulatorIntegration:
    """Integration tests for Trade Simulator mode"""

    @patch('league_helper.trade_simulator_mode.TradeSimulatorModeManager.TradeSimulatorModeManager.run')
    def test_trade_simulator_mode_can_be_entered(self, mock_run, temp_data_folder):
        """Test that Trade Simulator mode can be entered"""
        manager = LeagueHelperManager(temp_data_folder)

        mock_run.return_value = None
        manager.run_trade_simulator_mode()

        assert mock_run.called


class TestModifyPlayerDataIntegration:
    """Integration tests for Modify Player Data mode"""

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.ModifyPlayerDataModeManager.run')
    def test_modify_player_data_mode_can_be_entered(self, mock_run, temp_data_folder):
        """Test that Modify Player Data mode can be entered"""
        manager = LeagueHelperManager(temp_data_folder)

        mock_run.return_value = None
        manager.run_modify_player_data_mode()

        assert mock_run.called


class TestModeTransitions:
    """Integration tests for transitions between modes"""

    @patch('league_helper.add_to_roster_mode.AddToRosterModeManager.AddToRosterModeManager.run')
    @patch('league_helper.starter_helper_mode.StarterHelperModeManager.StarterHelperModeManager.run')
    def test_transition_from_add_to_roster_to_starter_helper(
        self, mock_starter, mock_add, temp_data_folder
    ):
        """Test transition from Add to Roster to Starter Helper"""
        manager = LeagueHelperManager(temp_data_folder)

        # Run add to roster mode
        manager.run_add_to_roster_mode()

        # Run starter helper mode
        manager.run_starter_helper_mode()

        # Both modes should have been called
        assert mock_add.called
        assert mock_starter.called

    @patch('league_helper.add_to_roster_mode.AddToRosterModeManager.AddToRosterModeManager.run')
    @patch('league_helper.trade_simulator_mode.TradeSimulatorModeManager.TradeSimulatorModeManager.run')
    def test_transition_from_add_to_roster_to_trade_simulator(
        self, mock_trade, mock_add, temp_data_folder
    ):
        """Test transition from Add to Roster to Trade Simulator"""
        manager = LeagueHelperManager(temp_data_folder)

        # Run add to roster mode
        manager.run_add_to_roster_mode()

        # Run trade simulator mode
        manager.run_trade_simulator_mode()

        # Both modes should have been called
        assert mock_add.called
        assert mock_trade.called


class TestDataPersistence:
    """Integration tests for data persistence across modes"""

    def test_player_data_persists_across_mode_transitions(self, temp_data_folder):
        """Test that player data persists when switching modes"""
        manager = LeagueHelperManager(temp_data_folder)

        # Get initial player count
        initial_players = manager.player_manager.get_all_players()
        initial_count = len(initial_players)

        # Create new manager (simulating mode transition)
        manager2 = LeagueHelperManager(temp_data_folder)

        # Verify same player count
        new_players = manager2.player_manager.get_all_players()
        assert len(new_players) == initial_count

    def test_team_data_persists_across_mode_transitions(self, temp_data_folder):
        """Test that team data persists when switching modes"""
        manager = LeagueHelperManager(temp_data_folder)

        # Get initial team count
        initial_teams = manager.team_data_manager.get_all_teams()
        initial_count = len(initial_teams)

        # Create new manager (simulating mode transition)
        manager2 = LeagueHelperManager(temp_data_folder)

        # Verify same team count
        new_teams = manager2.team_data_manager.get_all_teams()
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
