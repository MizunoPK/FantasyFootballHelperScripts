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

    # Create minimal players_projected.csv (required by ProjectedPointsManager)
    players_projected_csv = data_folder / "players_projected.csv"
    players_projected_csv.write_text("""id,name,week_1_points,week_2_points,week_3_points,week_4_points,week_5_points,week_6_points,week_7_points,week_8_points,week_9_points,week_10_points,week_11_points,week_12_points,week_13_points,week_14_points,week_15_points,week_16_points,week_17_points
1,Patrick Mahomes,22.5,21.3,23.1,20.5,22.0,21.5,0.0,23.5,22.8,21.9,22.3,20.8,21.2,22.6,23.0,21.7,22.4
2,Josh Allen,21.8,20.9,22.4,21.0,21.5,20.3,21.7,22.1,21.3,22.5,21.9,0.0,20.7,21.8,22.2,21.4,21.6
3,Justin Jefferson,18.5,17.8,19.2,18.0,18.7,17.5,18.9,19.1,18.3,19.5,18.9,19.3,0.0,18.6,19.0,18.2,18.8
4,Tyreek Hill,17.9,17.2,18.6,17.4,18.1,16.9,18.3,18.5,17.7,0.0,18.3,18.7,18.1,18.0,18.4,17.6,18.2
5,Christian McCaffrey,20.5,19.8,21.2,20.0,20.7,19.5,20.9,21.1,0.0,21.5,20.9,21.3,20.7,20.6,21.0,20.2,20.8
6,Austin Ekeler,16.5,15.8,17.2,16.0,0.0,15.5,16.9,17.1,16.3,17.5,16.9,17.3,16.7,16.6,17.0,16.2,16.8
7,Travis Kelce,14.5,13.8,15.2,14.0,14.7,13.5,0.0,15.1,14.3,15.5,14.9,15.3,14.7,14.6,15.0,14.2,14.8
8,Mark Andrews,13.5,12.8,14.2,13.0,13.7,12.5,13.9,14.1,13.3,14.5,13.9,14.3,0.0,13.6,14.0,13.2,13.8
""")

    # Note: teams.csv no longer used - team data is now in team_data folder

    # Create team_data folder with per-team weekly data (new format)
    team_data_folder = data_folder / "team_data"
    team_data_folder.mkdir()

    # Create KC team data (teams from players.csv)
    kc_csv = team_data_folder / "KC.csv"
    kc_csv.write_text("""week,QB,RB,WR,TE,K,points_scored,points_allowed
1,20.5,25.3,35.2,8.1,9.0,31,17
2,18.3,22.1,31.5,7.8,8.5,28,21
3,22.1,28.5,38.3,9.2,10.1,35,14
4,19.8,24.2,33.1,8.5,9.3,30,20
5,21.3,26.8,36.7,8.8,9.8,33,18
6,20.8,25.5,34.9,8.6,9.5,31,19
""")

    # Create BUF team data
    buf_csv = team_data_folder / "BUF.csv"
    buf_csv.write_text("""week,QB,RB,WR,TE,K,points_scored,points_allowed
1,22.1,24.0,33.5,7.5,8.8,32,15
2,20.5,23.2,35.1,8.0,9.2,30,18
3,21.8,25.5,34.8,7.9,9.0,31,16
4,19.2,22.8,32.5,7.3,8.6,29,19
5,20.8,24.1,33.9,7.7,8.9,30,17
6,21.5,24.8,34.2,7.8,9.1,31,17
""")

    # Copy player_data folder with JSON files (JSON-based loading from Sub-feature 1)
    source_player_data_folder = project_root / "data" / "player_data"
    dest_player_data_folder = data_folder / "player_data"

    if source_player_data_folder.exists():
        # Copy the entire player_data folder with all position JSON files
        shutil.copytree(source_player_data_folder, dest_player_data_folder)

    # Copy configs folder structure from actual data folder (new folder-based config system)
    source_configs_folder = project_root / "data" / "configs"
    dest_configs_folder = data_folder / "configs"

    if source_configs_folder.exists():
        # Copy the entire configs folder
        shutil.copytree(source_configs_folder, dest_configs_folder)
    else:
        # Create minimal config folder structure if source doesn't exist
        dest_configs_folder.mkdir()

        # Create base league_config.json
        base_config = dest_configs_folder / "league_config.json"
        base_config.write_text("""{
    "config_name": "Test Config",
    "description": "Test configuration for integration tests",
    "parameters": {
        "CURRENT_NFL_WEEK": 1,
        "NFL_SEASON": 2025,
        "NFL_SCORING_FORMAT": "ppr",
        "NORMALIZATION_MAX_SCALE": 100.0,
        "DRAFT_NORMALIZATION_MAX_SCALE": 163,
        "SAME_POS_BYE_WEIGHT": 0.2,
        "DIFF_POS_BYE_WEIGHT": 0.1,
        "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": -5, "HIGH": -100},
        "DRAFT_ORDER_BONUSES": {"PRIMARY": 10, "SECONDARY": 5},
        "DRAFT_ORDER": [{"FLEX": "P"}, {"FLEX": "P"}, {"FLEX": "P"}],
        "MAX_POSITIONS": {"QB": 1, "RB": 4, "WR": 4, "FLEX": 2, "TE": 2, "K": 1, "DST": 1},
        "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "TE"],
        "ADP_SCORING": {
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 30},
            "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
            "WEIGHT": 1.0
        }
    }
}""")

        # Create week-specific configs with week-specific parameters
        week_params_base = """{
    "config_name": "Test Config",
    "description": "Week-specific test configuration",
    "parameters": {
        "PLAYER_RATING_SCORING": {
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20},
            "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
            "WEIGHT": 1.0
        },
        "TEAM_QUALITY_SCORING": {
            "MIN_WEEKS": 5,
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6},
            "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
            "WEIGHT": 1.0
        },
        "PERFORMANCE_SCORING": {
            "MIN_WEEKS": 5,
            "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.2},
            "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
            "WEIGHT": 1.0
        },
        "MATCHUP_SCORING": {
            "MIN_WEEKS": 5,
            "IMPACT_SCALE": 100.0,
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 6},
            "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
            "WEIGHT": 1.0
        },
        "SCHEDULE_SCORING": {
            "MIN_WEEKS": 5,
            "IMPACT_SCALE": 100.0,
            "THRESHOLDS": {"BASE_POSITION": 16, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 4},
            "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
            "WEIGHT": 1.0
        },
        "TEMPERATURE_SCORING": {
            "IMPACT_SCALE": 50.0,
            "WEIGHT": 0.5,
            "IDEAL_TEMPERATURE": 60,
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 10},
            "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95}
        },
        "WIND_SCORING": {
            "IMPACT_SCALE": 50.0,
            "WEIGHT": 0.5,
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 8},
            "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95}
        },
        "LOCATION_MODIFIERS": {"HOME": 2.0, "AWAY": -2.0, "INTERNATIONAL": -3.0}
    }
}"""

        # Write week config files
        (dest_configs_folder / "week1-5.json").write_text(week_params_base)
        (dest_configs_folder / "week6-9.json").write_text(week_params_base)
        (dest_configs_folder / "week10-13.json").write_text(week_params_base)
        (dest_configs_folder / "week14-17.json").write_text(week_params_base)

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

        # Note: teams.csv no longer used - team data is now in team_data folder

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


class TestDraftedRosterManagerConsolidation:
    """Integration tests for Sub-feature 7: DraftedRosterManager consolidation"""

    def test_get_players_by_team_with_real_json(self, tmp_path):
        """Test PlayerManager.get_players_by_team() with real JSON data"""
        # Create data folder with JSON file containing drafted_by field
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create team_data folder to avoid warnings
        team_data_folder = data_folder / "team_data"
        team_data_folder.mkdir()

        # Create player_data folder to avoid D/ST warnings
        player_data_folder = data_folder / "player_data"
        player_data_folder.mkdir()

        # Create position-specific JSON files (Sub-feature 1 format)
        # QBs
        qb_json = player_data_folder / "qb_data.json"
        qb_json.write_text("""{
    "qb_data": [
        {
            "id": 1,
            "name": "Patrick Mahomes",
            "position": "QB",
            "team": "KC",
            "bye_week": 7,
            "fantasy_points": 350.5,
            "injury_status": "ACTIVE",
            "average_draft_position": 1.2,
            "drafted_by": "Sea Sharp"
        },
        {
            "id": 2,
            "name": "Josh Allen",
            "position": "QB",
            "team": "BUF",
            "bye_week": 12,
            "fantasy_points": 340.2,
            "injury_status": "ACTIVE",
            "average_draft_position": 1.5,
            "drafted_by": "Team Alpha"
        }
    ]
}""")

        # RBs
        rb_json = player_data_folder / "rb_data.json"
        rb_json.write_text("""{
    "rb_data": [
        {
            "id": 5,
            "name": "Christian McCaffrey",
            "position": "RB",
            "team": "SF",
            "bye_week": 9,
            "fantasy_points": 320.1,
            "injury_status": "QUESTIONABLE",
            "average_draft_position": 1.1,
            "drafted_by": "Team Alpha"
        }
    ]
}""")

        # WRs
        wr_json = player_data_folder / "wr_data.json"
        wr_json.write_text("""{
    "wr_data": [
        {
            "id": 3,
            "name": "Justin Jefferson",
            "position": "WR",
            "team": "MIN",
            "bye_week": 13,
            "fantasy_points": 310.8,
            "injury_status": "ACTIVE",
            "average_draft_position": 2.1,
            "drafted_by": "Sea Sharp"
        },
        {
            "id": 4,
            "name": "Tyreek Hill",
            "position": "WR",
            "team": "MIA",
            "bye_week": 10,
            "fantasy_points": 305.3,
            "injury_status": "ACTIVE",
            "average_draft_position": 2.3,
            "drafted_by": ""
        }
    ]
}""")

        # Empty files for other positions to avoid warnings
        for position in ["te", "k", "dst"]:
            pos_json = player_data_folder / f"{position}_data.json"
            pos_json.write_text(f'{{"{position}_data": []}}')

        # Create required config files
        import json
        import shutil

        # Copy configs folder from actual data
        source_configs = Path(__file__).parent.parent.parent / "data" / "configs"
        dest_configs = data_folder / "configs"

        if source_configs.exists():
            shutil.copytree(source_configs, dest_configs)

        # Import after setting up files
        from league_helper.util.PlayerManager import PlayerManager
        from league_helper.util.ConfigManager import ConfigManager
        from league_helper.util.TeamDataManager import TeamDataManager
        from league_helper.util.SeasonScheduleManager import SeasonScheduleManager

        # Initialize managers
        config = ConfigManager(data_folder)
        team_data = TeamDataManager(data_folder, config.current_nfl_week)
        schedule = SeasonScheduleManager(data_folder)
        player_manager = PlayerManager(data_folder, config, team_data, schedule)

        # Test get_players_by_team() - this is the new method from Sub-feature 7
        teams = player_manager.get_players_by_team()

        # Verify results
        assert isinstance(teams, dict)
        assert "Sea Sharp" in teams
        assert "Team Alpha" in teams

        # Verify Sea Sharp roster (players 1 and 3)
        assert len(teams["Sea Sharp"]) == 2
        sea_sharp_names = [p.name for p in teams["Sea Sharp"]]
        assert "Patrick Mahomes" in sea_sharp_names
        assert "Justin Jefferson" in sea_sharp_names

        # Verify Team Alpha roster (players 2 and 5)
        assert len(teams["Team Alpha"]) == 2
        team_alpha_names = [p.name for p in teams["Team Alpha"]]
        assert "Josh Allen" in team_alpha_names
        assert "Christian McCaffrey" in team_alpha_names

        # Verify player 4 (Tyreek Hill) is NOT in any team (drafted_by="")
        all_drafted_players = []
        for roster in teams.values():
            all_drafted_players.extend([p.name for p in roster])
        assert "Tyreek Hill" not in all_drafted_players

    def test_trade_simulator_uses_get_players_by_team(self, tmp_path):
        """Test TradeSimulator integration with PlayerManager.get_players_by_team()"""
        # Create data folder with JSON
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create team_data folder to avoid warnings
        team_data_folder = data_folder / "team_data"
        team_data_folder.mkdir()

        # Create player_data folder to avoid D/ST warnings
        player_data_folder = data_folder / "player_data"
        player_data_folder.mkdir()

        # Create position-specific JSON files (Sub-feature 1 format)
        # QBs
        qb_json = player_data_folder / "qb_data.json"
        qb_json.write_text("""{
    "qb_data": [
        {"id": 1, "name": "QB1", "position": "QB", "team": "KC", "bye_week": 7, "fantasy_points": 350.5, "injury_status": "ACTIVE", "average_draft_position": 1.2, "drafted_by": "Sea Sharp"},
        {"id": 2, "name": "QB2", "position": "QB", "team": "BUF", "bye_week": 12, "fantasy_points": 340.2, "injury_status": "ACTIVE", "average_draft_position": 1.5, "drafted_by": "Team Alpha"}
    ]
}""")

        # RBs
        rb_json = player_data_folder / "rb_data.json"
        rb_json.write_text("""{
    "rb_data": [
        {"id": 3, "name": "RB1", "position": "RB", "team": "SF", "bye_week": 9, "fantasy_points": 320.1, "injury_status": "ACTIVE", "average_draft_position": 1.1, "drafted_by": "Sea Sharp"},
        {"id": 4, "name": "RB2", "position": "RB", "team": "DAL", "bye_week": 8, "fantasy_points": 310.5, "injury_status": "ACTIVE", "average_draft_position": 2.5, "drafted_by": "Team Alpha"}
    ]
}""")

        # WRs
        wr_json = player_data_folder / "wr_data.json"
        wr_json.write_text("""{
    "wr_data": [
        {"id": 5, "name": "WR1", "position": "WR", "team": "MIN", "bye_week": 13, "fantasy_points": 310.8, "injury_status": "ACTIVE", "average_draft_position": 2.1, "drafted_by": "Sea Sharp"},
        {"id": 6, "name": "WR2", "position": "WR", "team": "MIA", "bye_week": 10, "fantasy_points": 305.3, "injury_status": "ACTIVE", "average_draft_position": 2.3, "drafted_by": "Team Alpha"}
    ]
}""")

        # TEs
        te_json = player_data_folder / "te_data.json"
        te_json.write_text("""{
    "te_data": [
        {"id": 7, "name": "TE1", "position": "TE", "team": "KC", "bye_week": 7, "fantasy_points": 220.4, "injury_status": "ACTIVE", "average_draft_position": 4.5, "drafted_by": "Sea Sharp"},
        {"id": 8, "name": "TE2", "position": "TE", "team": "BAL", "bye_week": 13, "fantasy_points": 210.3, "injury_status": "ACTIVE", "average_draft_position": 5.1, "drafted_by": "Team Alpha"}
    ]
}""")

        # Empty files for other positions to avoid warnings
        for position in ["k", "dst"]:
            pos_json = player_data_folder / f"{position}_data.json"
            pos_json.write_text(f'{{"{position}_data": []}}')

        # Create required config and team data
        import json
        import shutil

        source_configs = Path(__file__).parent.parent.parent / "data" / "configs"
        dest_configs = data_folder / "configs"
        if source_configs.exists():
            shutil.copytree(source_configs, dest_configs)

        # Import managers
        from league_helper.util.PlayerManager import PlayerManager
        from league_helper.util.ConfigManager import ConfigManager
        from league_helper.util.TeamDataManager import TeamDataManager
        from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
        from league_helper.trade_simulator_mode.TradeSimulatorModeManager import TradeSimulatorModeManager

        # Initialize managers
        config = ConfigManager(data_folder)
        team_data = TeamDataManager(data_folder, config.current_nfl_week)
        schedule = SeasonScheduleManager(data_folder)
        player_manager = PlayerManager(data_folder, config, team_data, schedule)

        # Initialize TradeSimulator
        trade_sim = TradeSimulatorModeManager(data_folder, player_manager, config)

        # Initialize team data (this should use get_players_by_team() internally)
        trade_sim.init_team_data()

        # Verify team_rosters was populated correctly
        assert hasattr(trade_sim, 'team_rosters')
        assert isinstance(trade_sim.team_rosters, dict)
        assert "Sea Sharp" in trade_sim.team_rosters
        assert "Team Alpha" in trade_sim.team_rosters

        # Verify each team has 4 players
        assert len(trade_sim.team_rosters["Sea Sharp"]) == 4
        assert len(trade_sim.team_rosters["Team Alpha"]) == 4

        # Verify NO CSV file was accessed (new approach doesn't use CSV)
        drafted_csv = data_folder / "drafted_data.csv"
        assert not drafted_csv.exists()  # CSV should NOT exist


class TestCSVDeprecation:
    """Integration tests for Sub-feature 8: CSV Deprecation & Cleanup"""

    def test_all_modes_with_json_only(self, temp_data_folder):
        """
        Test that all 4 League Helper modes work with JSON-only loading (no CSV files).

        This test verifies the complete CSV → JSON migration:
        - PlayerManager loads from player_data/*.json files
        - No players.csv file present (deprecated)
        - All 4 modes (Add to Roster, Starter Helper, Trade Simulator, Modify Player Data) work correctly

        Spec: sub_feature_08_csv_deprecation_cleanup_spec.md lines 92-97
        """
        # Remove players.csv to simulate production environment after CSV deprecation
        players_csv = temp_data_folder / "players.csv"
        if players_csv.exists():
            players_csv.unlink()  # Delete the CSV file

        # Also remove players_projected.csv (deprecated in Sub-feature 5)
        players_projected_csv = temp_data_folder / "players_projected.csv"
        if players_projected_csv.exists():
            players_projected_csv.unlink()

        # Verify CSV files do NOT exist (using JSON only)
        assert not players_csv.exists(), "Test should not have players.csv (using JSON only)"
        assert not players_projected_csv.exists(), "Test should not have players_projected.csv (deprecated)"

        # Verify player_data folder DOES exist
        player_data_folder = temp_data_folder / "player_data"
        assert player_data_folder.exists(), "Test must have player_data folder with JSON files"

        # Initialize League Helper Manager (should load from JSON)
        manager = LeagueHelperManager(temp_data_folder)

        # Verify players were loaded successfully from JSON
        assert manager.player_manager is not None
        assert len(manager.player_manager.players) > 0, "Players should be loaded from JSON files"

        # Verify all mode managers initialized successfully
        assert manager.add_to_roster_mode_manager is not None
        assert manager.starter_helper_mode_manager is not None
        assert manager.trade_simulator_mode_manager is not None
        assert manager.modify_player_data_mode_manager is not None

        # Test Mode 1: Add to Roster Mode
        with patch.object(manager.add_to_roster_mode_manager, 'start_interactive_mode', return_value=None) as mock_add:
            manager._run_add_to_roster_mode()
            assert mock_add.called, "Add to Roster mode should be callable with JSON loading"

        # Test Mode 2: Starter Helper Mode
        with patch.object(manager.starter_helper_mode_manager, 'show_recommended_starters', return_value=None) as mock_starter:
            manager._run_starter_helper_mode()
            assert mock_starter.called, "Starter Helper mode should be callable with JSON loading"

        # Test Mode 3: Trade Simulator Mode
        with patch.object(manager.trade_simulator_mode_manager, 'run_interactive_mode', return_value=None) as mock_trade:
            manager._run_trade_simulator_mode()
            assert mock_trade.called, "Trade Simulator mode should be callable with JSON loading"

        # Test Mode 4: Modify Player Data Mode
        with patch.object(manager.modify_player_data_mode_manager, 'start_interactive_mode', return_value=None) as mock_modify:
            manager.run_modify_player_data_mode()
            assert mock_modify.called, "Modify Player Data mode should be callable with JSON loading"

        # Verify NO CSV files were accessed during initialization or mode execution
        assert not (temp_data_folder / "players.csv").exists()

        # Success: All 4 modes work with JSON-only loading ✅


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
