"""
Unit Tests for Manual Simulation Script

Tests configuration loading, result printing, and simulation orchestration
for single league manual simulations.

Author: Kai Mizuno
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from io import StringIO
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from simulation.manual_simulation import (
    load_config,
    print_draft_results,
    print_weekly_results,
    print_final_standings,
    main
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_config_dict():
    """Sample configuration dictionary"""
    return {
        "config_name": "test_config",
        "description": "Test configuration for simulation",
        "parameters": {
            "num_teams": 10,
            "draft_rounds": 15,
            "season_weeks": 17
        }
    }


@pytest.fixture
def sample_config_file(tmp_path, sample_config_dict):
    """Create a temporary config JSON file"""
    config_file = tmp_path / "test_config.json"
    with open(config_file, 'w') as f:
        json.dump(sample_config_dict, f)
    return config_file


@pytest.fixture
def mock_player():
    """Create a mock FantasyPlayer"""
    player = Mock()
    player.name = "Patrick Mahomes"
    player.position = "QB"
    player.average_draft_position = 12.5
    player.fantasy_points = 385.6
    return player


@pytest.fixture
def mock_team(mock_player):
    """Create a mock team with roster"""
    team = Mock()
    team.strategy = "balanced"

    # Create mock roster
    qb = Mock()
    qb.name = "Josh Allen"
    qb.position = "QB"
    qb.average_draft_position = 8.3
    qb.fantasy_points = 402.1

    rb = Mock()
    rb.name = "Christian McCaffrey"
    rb.position = "RB"
    rb.average_draft_position = 1.2
    rb.fantasy_points = 345.7

    wr = Mock()
    wr.name = "Tyreek Hill"
    wr.position = "WR"
    wr.average_draft_position = 15.6
    wr.fantasy_points = 287.3

    team.get_roster_players.return_value = [qb, rb, wr]
    return team


@pytest.fixture
def mock_draft_helper_team():
    """Create a mock DraftHelperTeam"""
    team = Mock()

    # Create roster
    qb = Mock()
    qb.name = "Patrick Mahomes"
    qb.position = "QB"
    qb.average_draft_position = 12.5
    qb.fantasy_points = 385.6

    team.get_roster_players.return_value = [qb]
    return team


@pytest.fixture
def mock_week_result():
    """Create a mock weekly result"""
    week_result = Mock()
    week_result.week_number = 1

    # Create mock team results
    team1_result = Mock()
    team1_result.points_scored = 125.5
    team1_result.won = True

    team2_result = Mock()
    team2_result.points_scored = 98.3
    team2_result.won = False

    # Create mock teams
    team1 = Mock()
    team1.strategy = "aggressive"

    team2 = Mock()
    team2.strategy = "conservative"

    week_result.get_all_results.return_value = {team1: team1_result, team2: team2_result}
    week_result.get_matchups.return_value = [(team1, team2)]

    return week_result, team1, team2


@pytest.fixture
def mock_league(mock_draft_helper_team, mock_team, mock_week_result):
    """Create a mock SimulatedLeague"""
    league = Mock()
    league.draft_helper_team = mock_draft_helper_team
    league.teams = [mock_draft_helper_team, mock_team]

    week_result, team1, team2 = mock_week_result
    league.week_results = [week_result]

    # Mock get_all_team_results
    league.get_all_team_results.return_value = {
        "DraftHelperTeam": (10, 7, 1875.5),
        "SimulatedOpponent (balanced)": (8, 9, 1654.3)
    }

    return league


# ============================================================================
# LOAD CONFIG TESTS
# ============================================================================

class TestLoadConfig:
    """Test configuration loading functionality"""

    def test_load_valid_config(self, sample_config_file, sample_config_dict):
        """Test loading valid configuration file"""
        config = load_config(sample_config_file)

        assert config == sample_config_dict
        assert config["config_name"] == "test_config"
        assert config["description"] == "Test configuration for simulation"
        assert "parameters" in config

    def test_load_config_with_parameters(self, sample_config_file):
        """Test that parameters are loaded correctly"""
        config = load_config(sample_config_file)

        params = config["parameters"]
        assert params["num_teams"] == 10
        assert params["draft_rounds"] == 15
        assert params["season_weeks"] == 17

    def test_load_config_nonexistent_file(self, tmp_path):
        """Test loading nonexistent file raises error"""
        nonexistent = tmp_path / "nonexistent.json"

        with pytest.raises(FileNotFoundError):
            load_config(nonexistent)

    def test_load_config_invalid_json(self, tmp_path):
        """Test loading invalid JSON raises error"""
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("not valid json{")

        with pytest.raises(json.JSONDecodeError):
            load_config(invalid_file)

    def test_load_config_returns_full_structure(self, tmp_path):
        """Test that full config structure is returned"""
        full_config = {
            "config_name": "optimal_config",
            "description": "Optimal configuration",
            "parameters": {
                "qb_weight": 1.0,
                "rb_weight": 1.2
            }
        }

        config_file = tmp_path / "full_config.json"
        with open(config_file, 'w') as f:
            json.dump(full_config, f)

        result = load_config(config_file)
        assert result == full_config
        assert "config_name" in result
        assert "description" in result
        assert "parameters" in result


# ============================================================================
# PRINT DRAFT RESULTS TESTS
# ============================================================================

class TestPrintDraftResults:
    """Test draft results printing functionality"""

    def test_print_draft_results_basic(self, mock_league, capsys):
        """Test basic draft results printing"""
        print_draft_results(mock_league)

        captured = capsys.readouterr()
        assert "DRAFT RESULTS" in captured.out
        assert "DraftHelperTeam" in captured.out

    def test_print_draft_results_shows_positions(self, mock_league, capsys):
        """Test that positions are displayed correctly"""
        print_draft_results(mock_league)

        captured = capsys.readouterr()
        assert "QB:" in captured.out
        assert "RB:" in captured.out
        assert "WR:" in captured.out

    def test_print_draft_results_shows_player_names(self, mock_league, capsys):
        """Test that player names are displayed"""
        print_draft_results(mock_league)

        captured = capsys.readouterr()
        assert "Patrick Mahomes" in captured.out
        assert "Josh Allen" in captured.out
        assert "Christian McCaffrey" in captured.out

    def test_print_draft_results_shows_adp(self, mock_league, capsys):
        """Test that ADP values are displayed"""
        print_draft_results(mock_league)

        captured = capsys.readouterr()
        assert "ADP:" in captured.out

    def test_print_draft_results_shows_projections(self, mock_league, capsys):
        """Test that projected points are displayed"""
        print_draft_results(mock_league)

        captured = capsys.readouterr()
        assert "Proj:" in captured.out

    def test_print_draft_results_shows_strategy(self, mock_league, capsys):
        """Test that opponent strategies are displayed"""
        print_draft_results(mock_league)

        captured = capsys.readouterr()
        assert "Strategy: balanced" in captured.out

    def test_print_draft_results_handles_missing_stats(self, mock_league, capsys):
        """Test handling of players with missing stats"""
        # Create player with None values
        player_no_stats = Mock()
        player_no_stats.name = "Unknown Player"
        player_no_stats.position = "RB"
        player_no_stats.average_draft_position = None
        player_no_stats.fantasy_points = None

        mock_league.teams[0].get_roster_players.return_value = [player_no_stats]

        print_draft_results(mock_league)

        captured = capsys.readouterr()
        assert "Unknown Player" in captured.out
        assert "ADP: N/A" in captured.out
        assert "Proj: N/A" in captured.out


# ============================================================================
# PRINT WEEKLY RESULTS TESTS
# ============================================================================

class TestPrintWeeklyResults:
    """Test weekly results printing functionality"""

    def test_print_weekly_results_basic(self, mock_league, capsys):
        """Test basic weekly results printing"""
        print_weekly_results(mock_league)

        captured = capsys.readouterr()
        assert "SEASON RESULTS" in captured.out
        assert "Week 1:" in captured.out

    def test_print_weekly_results_shows_scores(self, mock_league, capsys):
        """Test that scores are displayed"""
        print_weekly_results(mock_league)

        captured = capsys.readouterr()
        assert "125.5" in captured.out or "125.50" in captured.out
        assert "98.3" in captured.out or "98.30" in captured.out

    def test_print_weekly_results_shows_winners(self, mock_league, capsys):
        """Test that winners are indicated"""
        print_weekly_results(mock_league)

        captured = capsys.readouterr()
        assert "WIN" in captured.out
        assert "LOSS" in captured.out

    def test_print_weekly_results_shows_strategies(self, mock_league, capsys):
        """Test that opponent strategies are shown"""
        print_weekly_results(mock_league)

        captured = capsys.readouterr()
        assert "aggressive" in captured.out or "conservative" in captured.out

    def test_print_weekly_results_handles_tie(self, mock_league, capsys):
        """Test handling of tied games"""
        # Modify mock to create a tie
        team1_result = Mock()
        team1_result.points_scored = 100.0
        team1_result.won = False

        team2_result = Mock()
        team2_result.points_scored = 100.0
        team2_result.won = False

        team1 = Mock()
        team1.strategy = "balanced"
        team2 = Mock()
        team2.strategy = "conservative"

        week_result = Mock()
        week_result.week_number = 1
        week_result.get_all_results.return_value = {team1: team1_result, team2: team2_result}
        week_result.get_matchups.return_value = [(team1, team2)]

        mock_league.week_results = [week_result]
        mock_league.draft_helper_team = Mock()  # Neither team is draft helper

        print_weekly_results(mock_league)

        captured = capsys.readouterr()
        assert "TIE" in captured.out

    def test_print_weekly_results_multiple_weeks(self, mock_league, capsys):
        """Test printing multiple weeks of results"""
        # Create multiple week results
        week1 = Mock()
        week1.week_number = 1
        week1.get_all_results.return_value = {}
        week1.get_matchups.return_value = []

        week2 = Mock()
        week2.week_number = 2
        week2.get_all_results.return_value = {}
        week2.get_matchups.return_value = []

        mock_league.week_results = [week1, week2]

        print_weekly_results(mock_league)

        captured = capsys.readouterr()
        assert "Week 1:" in captured.out
        assert "Week 2:" in captured.out


# ============================================================================
# PRINT FINAL STANDINGS TESTS
# ============================================================================

class TestPrintFinalStandings:
    """Test final standings printing functionality"""

    def test_print_final_standings_basic(self, mock_league, capsys):
        """Test basic standings printing"""
        print_final_standings(mock_league)

        captured = capsys.readouterr()
        assert "FINAL STANDINGS" in captured.out

    def test_print_final_standings_shows_records(self, mock_league, capsys):
        """Test that win-loss records are displayed"""
        print_final_standings(mock_league)

        captured = capsys.readouterr()
        assert "10W - 7L" in captured.out
        assert "8W - 9L" in captured.out

    def test_print_final_standings_shows_points(self, mock_league, capsys):
        """Test that total points are displayed"""
        print_final_standings(mock_league)

        captured = capsys.readouterr()
        assert "1875.5" in captured.out or "1875.50" in captured.out
        assert "1654.3" in captured.out or "1654.30" in captured.out

    def test_print_final_standings_sorted_by_wins(self, mock_league, capsys):
        """Test that standings are sorted by wins"""
        # Modify mock to have different win totals
        mock_league.get_all_team_results.return_value = {
            "Team A": (12, 5, 2000.0),
            "Team B": (10, 7, 1900.0),
            "Team C": (8, 9, 1800.0)
        }

        print_final_standings(mock_league)

        captured = capsys.readouterr()
        # Team A should appear before Team B
        team_a_pos = captured.out.find("Team A")
        team_b_pos = captured.out.find("Team B")
        team_c_pos = captured.out.find("Team C")

        assert team_a_pos < team_b_pos < team_c_pos

    def test_print_final_standings_highlights_draft_helper(self, mock_league, capsys):
        """Test that DraftHelperTeam is highlighted"""
        print_final_standings(mock_league)

        captured = capsys.readouterr()
        assert "DraftHelperTeam Performance:" in captured.out

    def test_print_final_standings_handles_no_draft_helper(self, mock_league, capsys):
        """Test standings when no DraftHelperTeam exists"""
        # Remove DraftHelperTeam from results
        mock_league.get_all_team_results.return_value = {
            "SimulatedOpponent 1": (10, 7, 1800.0),
            "SimulatedOpponent 2": (9, 8, 1750.0)
        }

        print_final_standings(mock_league)

        captured = capsys.readouterr()
        assert "FINAL STANDINGS" in captured.out
        # Should not crash even without DraftHelperTeam


# ============================================================================
# MAIN FUNCTION TESTS
# ============================================================================

class TestMain:
    """Test main simulation orchestration"""

    @patch('simulation.manual_simulation.SimulatedLeague')
    @patch('simulation.manual_simulation.load_config')
    @patch('simulation.manual_simulation.get_logger')
    @patch('simulation.manual_simulation.print_draft_results')
    @patch('simulation.manual_simulation.print_weekly_results')
    @patch('simulation.manual_simulation.print_final_standings')
    def test_main_full_workflow(self, mock_print_standings, mock_print_weekly,
                                mock_print_draft, mock_get_logger, mock_load_config,
                                mock_league_class, sample_config_dict, capsys):
        """Test full main workflow execution"""
        # Setup mocks
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_load_config.return_value = sample_config_dict

        mock_league = Mock()
        mock_league_class.return_value = mock_league

        # Run main
        main()

        # Verify workflow
        mock_load_config.assert_called_once()
        mock_league_class.assert_called_once()
        mock_league.run_draft.assert_called_once()
        mock_league.run_season.assert_called_once()
        mock_league.cleanup.assert_called_once()

        # Verify printing functions called
        mock_print_draft.assert_called_once_with(mock_league)
        mock_print_weekly.assert_called_once_with(mock_league)
        mock_print_standings.assert_called_once_with(mock_league)

    @patch('simulation.manual_simulation.SimulatedLeague')
    @patch('simulation.manual_simulation.load_config')
    @patch('simulation.manual_simulation.get_logger')
    def test_main_creates_league_with_config(self, mock_get_logger, mock_load_config,
                                            mock_league_class, sample_config_dict):
        """Test that league is created with loaded config"""
        mock_load_config.return_value = sample_config_dict
        mock_league = Mock()
        # Add required attributes for print functions
        mock_league.teams = []
        mock_league.draft_helper_team = Mock()
        mock_league.week_results = []
        mock_league.get_all_team_results.return_value = {}
        mock_league_class.return_value = mock_league

        main()

        # Verify league created with config dict
        assert mock_league_class.call_count == 1
        args = mock_league_class.call_args[0]
        assert args[0] == sample_config_dict

    @patch('simulation.manual_simulation.SimulatedLeague')
    @patch('simulation.manual_simulation.load_config')
    @patch('simulation.manual_simulation.get_logger')
    def test_main_logs_progress(self, mock_get_logger, mock_load_config, mock_league_class):
        """Test that main logs progress messages"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_load_config.return_value = {}

        mock_league = Mock()
        # Add required attributes for print functions
        mock_league.teams = []
        mock_league.draft_helper_team = Mock()
        mock_league.week_results = []
        mock_league.get_all_team_results.return_value = {}
        mock_league_class.return_value = mock_league

        main()

        # Verify logging calls
        assert mock_logger.info.call_count >= 4
        log_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("Starting manual simulation" in msg for msg in log_messages)
        assert any("Draft complete" in msg for msg in log_messages)
        assert any("Season complete" in msg for msg in log_messages)

    @patch('simulation.manual_simulation.SimulatedLeague')
    @patch('simulation.manual_simulation.load_config')
    @patch('simulation.manual_simulation.get_logger')
    def test_main_prints_configuration_info(self, mock_get_logger, mock_load_config,
                                           mock_league_class, capsys):
        """Test that configuration info is printed"""
        mock_load_config.return_value = {}
        mock_league = Mock()
        # Add required attributes for print functions
        mock_league.teams = []
        mock_league.draft_helper_team = Mock()
        mock_league.week_results = []
        mock_league.get_all_team_results.return_value = {}
        mock_league_class.return_value = mock_league

        main()

        captured = capsys.readouterr()
        assert "FANTASY FOOTBALL LEAGUE SIMULATION" in captured.out
        assert "10 teams total" in captured.out
        assert "Snake draft" in captured.out
        assert "17-week regular season" in captured.out

    @patch('simulation.manual_simulation.SimulatedLeague')
    @patch('simulation.manual_simulation.load_config')
    @patch('simulation.manual_simulation.get_logger')
    def test_main_cleanup_called(self, mock_get_logger, mock_load_config, mock_league_class):
        """Test that cleanup is called after simulation"""
        mock_load_config.return_value = {}
        mock_league = Mock()
        # Add required attributes for print functions
        mock_league.teams = []
        mock_league.draft_helper_team = Mock()
        mock_league.week_results = []
        mock_league.get_all_team_results.return_value = {}
        mock_league_class.return_value = mock_league

        main()

        mock_league.cleanup.assert_called_once()

    @patch('simulation.manual_simulation.SimulatedLeague')
    @patch('simulation.manual_simulation.load_config')
    @patch('simulation.manual_simulation.get_logger')
    def test_main_prints_completion_message(self, mock_get_logger, mock_load_config,
                                           mock_league_class, capsys):
        """Test that completion message is printed"""
        mock_load_config.return_value = {}
        mock_league = Mock()
        # Add required attributes for print functions
        mock_league.teams = []
        mock_league.draft_helper_team = Mock()
        mock_league.week_results = []
        mock_league.get_all_team_results.return_value = {}
        mock_league_class.return_value = mock_league

        main()

        captured = capsys.readouterr()
        assert "SIMULATION COMPLETE" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
