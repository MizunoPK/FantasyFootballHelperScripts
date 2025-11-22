"""
Unit Tests for Simulated League

Tests complete fantasy football league simulation including team initialization,
draft execution, season simulation, and results tracking.

Author: Kai Mizuno
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open, call
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from simulation.SimulatedLeague import SimulatedLeague


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_config_dict():
    """Sample configuration dictionary"""
    return {
        "config_name": "test_config",
        "description": "Test configuration",
        "parameters": {
            "num_teams": 10,
            "draft_rounds": 15
        }
    }


@pytest.fixture
def mock_data_folder(tmp_path):
    """Create mock data folder with required files"""
    data_folder = tmp_path / "sim_data"
    data_folder.mkdir()

    # Create required CSV files
    (data_folder / "players_projected.csv").write_text("id,name,position\n1,Player1,QB\n")
    (data_folder / "players_actual.csv").write_text("id,name,position\n1,Player1,QB\n")

    # Create team ranking files for weeks 1-16
    for week in range(1, 17):
        (data_folder / f"teams_week_{week}.csv").write_text("team,rank\nNE,1\n")

    return data_folder


@pytest.fixture
def mock_player():
    """Create a mock FantasyPlayer"""
    player = Mock()
    player.id = 101
    player.name = "Patrick Mahomes"
    player.position = "QB"
    player.fantasy_points = 385.6
    return player


@pytest.fixture
def mock_week_result():
    """Create a mock weekly result"""
    result = Mock()
    result.points_scored = 125.5
    result.won = True
    return result


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestSimulatedLeagueInitialization:
    """Test SimulatedLeague initialization"""

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_init_creates_temp_directory(self, mock_gen_schedule, mock_init_teams,
                                        mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that initialization creates temporary directory"""
        mock_mkdtemp.return_value = str(tmp_path / "temp_league")
        (tmp_path / "temp_league").mkdir()

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        mock_mkdtemp.assert_called_once()
        assert str(tmp_path / "temp_league") in mock_mkdtemp.return_value

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_init_saves_config_to_file(self, mock_gen_schedule, mock_init_teams,
                                      mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that config is saved to JSON file"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        config_file = temp_dir / "league_config.json"
        assert config_file.exists()

        with open(config_file, 'r') as f:
            saved_config = json.load(f)
        assert saved_config == sample_config_dict

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_init_calls_team_initialization(self, mock_gen_schedule, mock_init_teams,
                                           mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that _initialize_teams is called during init"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        mock_init_teams.assert_called_once()

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_init_calls_schedule_generation(self, mock_gen_schedule, mock_init_teams,
                                           mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that _generate_schedule is called during init"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        mock_gen_schedule.assert_called_once()

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_init_sets_attributes(self, mock_gen_schedule, mock_init_teams,
                                 mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that initialization sets all required attributes"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        assert league.config_dict == sample_config_dict
        assert isinstance(league.teams, list)
        assert isinstance(league.draft_order, list)
        assert isinstance(league.season_schedule, list)
        assert isinstance(league.week_results, list)


# ============================================================================
# TEAM INITIALIZATION TESTS
# ============================================================================

class TestTeamInitialization:
    """Test team initialization logic"""

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_team_strategy_distribution(self, mock_gen_schedule, mock_init_teams,
                                        mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that team strategy distribution is correct"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        # Verify strategy distribution constants
        assert SimulatedLeague.TEAM_STRATEGIES['draft_helper'] == 1
        assert SimulatedLeague.TEAM_STRATEGIES['adp_aggressive'] == 2
        assert SimulatedLeague.TEAM_STRATEGIES['projected_points_aggressive'] == 2
        assert SimulatedLeague.TEAM_STRATEGIES['adp_with_draft_order'] == 2
        assert SimulatedLeague.TEAM_STRATEGIES['projected_points_with_draft_order'] == 3

        # Total should be 10 teams
        assert sum(SimulatedLeague.TEAM_STRATEGIES.values()) == 10

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_initialize_teams_called_during_init(self, mock_gen_schedule, mock_init_teams,
                                                 mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that _initialize_teams is called during initialization"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        # Verify that _initialize_teams was called
        mock_init_teams.assert_called_once()

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_teams_list_initialized(self, mock_gen_schedule, mock_init_teams,
                                    mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that teams list is initialized"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        # Verify teams list exists
        assert hasattr(league, 'teams')
        assert isinstance(league.teams, list)


# ============================================================================
# SCHEDULE GENERATION TESTS
# ============================================================================

class TestScheduleGeneration:
    """Test schedule generation"""

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.generate_schedule_for_nfl_season')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    def test_generate_schedule_calls_scheduler(self, mock_init_teams, mock_gen_schedule,
                                              mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that schedule generation calls scheduler utility"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        mock_gen_schedule.return_value = [[]]

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        mock_gen_schedule.assert_called_once_with(league.teams, num_weeks=16)

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.generate_schedule_for_nfl_season')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    def test_generate_schedule_creates_16_weeks(self, mock_init_teams, mock_gen_schedule,
                                               mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that 16-week schedule is generated"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Mock 16 weeks of schedule
        mock_schedule = [[Mock()] for _ in range(16)]
        mock_gen_schedule.return_value = mock_schedule

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        assert len(league.season_schedule) == 16


# ============================================================================
# DRAFT TESTS
# ============================================================================

class TestDraft:
    """Test draft simulation"""

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.SimulatedLeague.random.shuffle')
    def test_run_draft_randomizes_order(self, mock_shuffle, mock_gen_schedule,
                                       mock_init_teams, mock_mkdtemp,
                                       sample_config_dict, tmp_path):
        """Test that draft order is randomized"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock teams
        mock_teams = [Mock() for _ in range(10)]
        for team in mock_teams:
            team.config = Mock()
            team.get_draft_recommendation.return_value = Mock(id=1, name="Test", position="QB")

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.teams = mock_teams

        league.run_draft()

        # shuffle should be called once to randomize draft order
        assert mock_shuffle.call_count >= 1

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_run_draft_sets_week_to_1(self, mock_gen_schedule, mock_init_teams,
                                     mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that all teams are set to week 1 during draft"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock teams
        mock_teams = [Mock() for _ in range(10)]
        for team in mock_teams:
            team.config = Mock()
            team.config.current_nfl_week = 0
            team.get_draft_recommendation.return_value = Mock(id=1, name="Test", position="QB")

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.teams = mock_teams

        league.run_draft()

        # All teams should have week set to 1
        for team in mock_teams:
            assert team.config.current_nfl_week == 1

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_run_draft_executes_15_rounds(self, mock_gen_schedule, mock_init_teams,
                                         mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that 15 rounds of draft are executed"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock teams
        mock_teams = [Mock() for _ in range(10)]
        player_counter = [0]  # Mutable counter

        def get_draft_rec():
            player_counter[0] += 1
            player = Mock()
            player.id = player_counter[0]
            player.name = f"Player_{player_counter[0]}"
            player.position = "QB"
            return player

        for team in mock_teams:
            team.config = Mock()
            team.get_draft_recommendation = get_draft_rec

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.teams = mock_teams

        league.run_draft()

        # Each team should draft 15 players (150 total picks)
        for team in mock_teams:
            assert team.draft_player.call_count == 15

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_run_draft_broadcasts_picks(self, mock_gen_schedule, mock_init_teams,
                                       mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that drafted players are broadcast to all teams"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock teams
        mock_teams = [Mock() for _ in range(2)]  # Use 2 teams for simplicity
        for team in mock_teams:
            team.config = Mock()
            team.get_draft_recommendation.return_value = Mock(id=1, name="Test", position="QB")

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.teams = mock_teams

        league.run_draft()

        # Each team should mark other team's picks as drafted
        for team in mock_teams:
            assert team.mark_player_drafted.call_count > 0


# ============================================================================
# SEASON SIMULATION TESTS
# ============================================================================

class TestSeasonSimulation:
    """Test season simulation"""

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.SimulatedLeague.Week')
    def test_run_season_simulates_16_weeks(self, mock_week_class, mock_gen_schedule,
                                          mock_init_teams, mock_mkdtemp,
                                          sample_config_dict, tmp_path):
        """Test that 16 weeks are simulated"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock schedule (16 weeks)
        mock_schedule = [[(Mock(), Mock())] for _ in range(16)]

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.season_schedule = mock_schedule

        league.run_season()

        # Week class should be instantiated 16 times
        assert mock_week_class.call_count == 16

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.SimulatedLeague.SimulatedLeague._update_team_rankings')
    @patch('simulation.SimulatedLeague.Week')
    def test_run_season_updates_rankings_each_week(self, mock_week_class, mock_update_rankings,
                                                   mock_gen_schedule, mock_init_teams,
                                                   mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that team rankings are updated each week"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock schedule
        mock_schedule = [[(Mock(), Mock())] for _ in range(16)]

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.season_schedule = mock_schedule

        league.run_season()

        # Rankings should be updated 16 times (once per week)
        assert mock_update_rankings.call_count == 16

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.SimulatedLeague.Week')
    def test_run_season_stores_week_results(self, mock_week_class, mock_gen_schedule,
                                           mock_init_teams, mock_mkdtemp,
                                           sample_config_dict, tmp_path):
        """Test that week results are stored"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock schedule
        mock_schedule = [[(Mock(), Mock())] for _ in range(16)]

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.season_schedule = mock_schedule

        league.run_season()

        # 16 week results should be stored
        assert len(league.week_results) == 16


# ============================================================================
# UPDATE TEAM RANKINGS TESTS
# ============================================================================

class TestUpdateTeamRankings:
    """Test team ranking updates"""

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_update_team_rankings_uses_correct_data_folder(self, mock_gen_schedule,
                                                           mock_init_teams, mock_mkdtemp,
                                                           sample_config_dict, mock_data_folder):
        """Test that update_team_rankings uses the data folder"""
        temp_dir = mock_data_folder / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create team directories
        for i in range(10):
            (temp_dir / f"team_{i}").mkdir()

        league = SimulatedLeague(sample_config_dict, mock_data_folder)

        # Verify league has correct data folder
        assert league.data_folder == mock_data_folder

        # Verify week file exists for the test
        assert (mock_data_folder / "teams_week_5.csv").exists()

        # Should not raise an exception
        league._update_team_rankings(5)

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_update_team_rankings_handles_missing_file(self, mock_gen_schedule,
                                                       mock_init_teams, mock_mkdtemp,
                                                       sample_config_dict, tmp_path):
        """Test fallback to week 1 when week file missing"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        data_folder = tmp_path / "data"
        data_folder.mkdir()
        # Only create week 1 file
        (data_folder / "teams_week_1.csv").write_text("team,rank\n")

        # Create team directories
        for i in range(10):
            (temp_dir / f"team_{i}").mkdir()

        league = SimulatedLeague(sample_config_dict, data_folder)

        # Try to update to week 99 (doesn't exist) - should fall back to week 1
        # Should not raise exception
        league._update_team_rankings(99)


# ============================================================================
# RESULTS TESTS
# ============================================================================

class TestResults:
    """Test result retrieval"""

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_get_draft_helper_results_returns_tuple(self, mock_gen_schedule, mock_init_teams,
                                                    mock_mkdtemp, sample_config_dict,
                                                    tmp_path, mock_week_result):
        """Test that get_draft_helper_results returns (wins, losses, points)"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        # Create mock draft helper team
        draft_helper = Mock()
        league.draft_helper_team = draft_helper

        # Create mock week results
        mock_week = Mock()
        mock_week.get_result.return_value = mock_week_result

        league.week_results = [mock_week] * 3  # 3 weeks

        wins, losses, points = league.get_draft_helper_results()

        assert isinstance(wins, int)
        assert isinstance(losses, int)
        assert isinstance(points, float)

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_get_draft_helper_results_raises_without_draft_helper(self, mock_gen_schedule,
                                                                  mock_init_teams, mock_mkdtemp,
                                                                  sample_config_dict, tmp_path):
        """Test that error is raised if no DraftHelperTeam"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.draft_helper_team = None

        with pytest.raises(ValueError) as exc_info:
            league.get_draft_helper_results()

        assert "DraftHelperTeam not found" in str(exc_info.value)

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_get_all_team_results_returns_dict(self, mock_gen_schedule, mock_init_teams,
                                               mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that get_all_team_results returns dictionary"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        # Create mock teams
        league.teams = [Mock() for _ in range(3)]
        league.draft_helper_team = league.teams[0]

        # Create mock week results
        result_win = Mock()
        result_win.won = True
        result_win.points_scored = 120.0

        mock_week = Mock()
        mock_week.get_result.return_value = result_win

        league.week_results = [mock_week] * 2

        results = league.get_all_team_results()

        assert isinstance(results, dict)
        assert len(results) == 3  # 3 teams


# ============================================================================
# CLEANUP TESTS
# ============================================================================

class TestCleanup:
    """Test cleanup functionality"""

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.SimulatedLeague.shutil.rmtree')
    def test_cleanup_removes_temp_directory(self, mock_rmtree, mock_gen_schedule,
                                           mock_init_teams, mock_mkdtemp,
                                           sample_config_dict, tmp_path):
        """Test that cleanup removes temporary directory"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        league.cleanup()

        # Check that rmtree was called with the temp_dir
        mock_rmtree.assert_any_call(league.temp_dir)

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_cleanup_handles_missing_directory(self, mock_gen_schedule, mock_init_teams,
                                              mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that cleanup handles missing temp directory gracefully"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()  # Create it for init
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        # Now set to nonexistent path and cleanup
        nonexistent = tmp_path / "nonexistent_temp"
        league.temp_dir = nonexistent

        # Should not raise exception
        league.cleanup()

    @patch('simulation.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.SimulatedLeague.shutil.rmtree')
    def test_destructor_calls_cleanup(self, mock_rmtree, mock_gen_schedule,
                                     mock_init_teams, mock_mkdtemp,
                                     sample_config_dict, tmp_path):
        """Test that __del__ calls cleanup"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        # Call destructor
        league.__del__()

        # cleanup should have been called (which calls rmtree)
        assert mock_rmtree.call_count >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
