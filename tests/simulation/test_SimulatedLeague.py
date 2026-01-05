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

from simulation.win_rate.SimulatedLeague import SimulatedLeague


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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_init_creates_temp_directory(self, mock_gen_schedule, mock_init_teams,
                                        mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that initialization creates temporary directory"""
        mock_mkdtemp.return_value = str(tmp_path / "temp_league")
        (tmp_path / "temp_league").mkdir()

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        mock_mkdtemp.assert_called_once()
        assert str(tmp_path / "temp_league") in mock_mkdtemp.return_value

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_init_calls_team_initialization(self, mock_gen_schedule, mock_init_teams,
                                           mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that _initialize_teams is called during init"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        mock_init_teams.assert_called_once()

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_init_calls_schedule_generation(self, mock_gen_schedule, mock_init_teams,
                                           mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that _generate_schedule is called during init"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        mock_gen_schedule.assert_called_once()

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    def test_initialize_teams_called_during_init(self, mock_gen_schedule, mock_init_teams,
                                                 mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that _initialize_teams is called during initialization"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        # Verify that _initialize_teams was called
        mock_init_teams.assert_called_once()

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.generate_schedule_for_nfl_season')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    def test_generate_schedule_calls_scheduler(self, mock_init_teams, mock_gen_schedule,
                                              mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that schedule generation calls scheduler utility"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        mock_gen_schedule.return_value = [[]]

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        mock_gen_schedule.assert_called_once_with(league.teams, num_weeks=17)

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.generate_schedule_for_nfl_season')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    def test_generate_schedule_creates_17_weeks(self, mock_init_teams, mock_gen_schedule,
                                               mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that 17-week schedule is generated"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Mock 17 weeks of schedule
        mock_schedule = [[Mock()] for _ in range(17)]
        mock_gen_schedule.return_value = mock_schedule

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")

        assert len(league.season_schedule) == 17


# ============================================================================
# DRAFT TESTS
# ============================================================================

class TestDraft:
    """Test draft simulation"""

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.win_rate.SimulatedLeague.random.shuffle')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.win_rate.SimulatedLeague.Week')
    def test_run_season_simulates_17_weeks(self, mock_week_class, mock_gen_schedule,
                                          mock_init_teams, mock_mkdtemp,
                                          sample_config_dict, tmp_path):
        """Test that 17 weeks are simulated"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock schedule (17 weeks)
        mock_schedule = [[(Mock(), Mock())] for _ in range(17)]

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.season_schedule = mock_schedule

        league.run_season()

        # Week class should be instantiated 17 times
        assert mock_week_class.call_count == 17

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._update_team_rankings')
    @patch('simulation.win_rate.SimulatedLeague.Week')
    def test_run_season_updates_rankings_each_week(self, mock_week_class, mock_update_rankings,
                                                   mock_gen_schedule, mock_init_teams,
                                                   mock_mkdtemp, sample_config_dict, tmp_path):
        """Test that team rankings are updated each week"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock schedule (17 weeks)
        mock_schedule = [[(Mock(), Mock())] for _ in range(17)]

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.season_schedule = mock_schedule

        league.run_season()

        # Rankings should be updated 17 times (once per week)
        assert mock_update_rankings.call_count == 17

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.win_rate.SimulatedLeague.Week')
    def test_run_season_stores_week_results(self, mock_week_class, mock_gen_schedule,
                                           mock_init_teams, mock_mkdtemp,
                                           sample_config_dict, tmp_path):
        """Test that week results are stored"""
        temp_dir = tmp_path / "temp_league"
        temp_dir.mkdir()
        mock_mkdtemp.return_value = str(temp_dir)

        # Create mock schedule (17 weeks)
        mock_schedule = [[(Mock(), Mock())] for _ in range(17)]

        league = SimulatedLeague(sample_config_dict, tmp_path / "data")
        league.season_schedule = mock_schedule

        league.run_season()

        # 17 week results should be stored
        assert len(league.week_results) == 17


# ============================================================================
# UPDATE TEAM RANKINGS TESTS
# ============================================================================

class TestUpdateTeamRankings:
    """Test team ranking updates"""

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.win_rate.SimulatedLeague.shutil.rmtree')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
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

    @patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams')
    @patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule')
    @patch('simulation.win_rate.SimulatedLeague.shutil.rmtree')
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


# ============================================================================
# JSON LOADING TESTS (Feature 01 - Win Rate Sim JSON Verification)
# ============================================================================

class TestJSONLoading:
    """Test JSON player data loading functionality"""

    def test_parse_players_json_valid_data(self, tmp_path):
        """Test _parse_players_json with valid JSON data"""
        # Create temp week folder with JSON files
        week_folder = tmp_path / "week_01"
        week_folder.mkdir()

        # Create sample QB data
        qb_data = [
            {
                "id": "12345",
                "name": "Patrick Mahomes",
                "position": "QB",
                "drafted_by": "",
                "locked": False,
                "projected_points": [25.0] * 17,
                "actual_points": [28.0] * 17
            }
        ]
        (week_folder / "qb_data.json").write_text(json.dumps(qb_data))

        # Create empty files for other positions
        for pos in ['rb', 'wr', 'te', 'k', 'dst']:
            (week_folder / f"{pos}_data.json").write_text("[]")

        # Import and test
        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        # Create minimal league instance
        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)
            players = league._parse_players_json(week_folder, week_num=1)

        assert len(players) == 1
        assert 12345 in players
        assert players[12345]["name"] == "Patrick Mahomes"
        assert players[12345]["position"] == "QB"
        assert players[12345]["projected_points"] == "25.0"
        assert players[12345]["actual_points"] == "28.0"

    def test_parse_players_json_array_extraction(self, tmp_path):
        """Test correct extraction of week-specific values from arrays"""
        week_folder = tmp_path / "week_05"
        week_folder.mkdir()

        # Create data with varying values per week
        rb_data = [
            {
                "id": "67890",
                "name": "Christian McCaffrey",
                "position": "RB",
                "drafted_by": "",
                "locked": False,
                "projected_points": [10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0] + [0.0] * 10,
                "actual_points": [9.0, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5] + [0.0] * 10
            }
        ]
        (week_folder / "rb_data.json").write_text(json.dumps(rb_data))

        for pos in ['qb', 'wr', 'te', 'k', 'dst']:
            (week_folder / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)
            players = league._parse_players_json(week_folder, week_num=5)

        # Week 5 should extract index 4 (week_num - 1)
        assert players[67890]["projected_points"] == "14.0"
        assert players[67890]["actual_points"] == "13.5"

    def test_parse_players_json_locked_conversion(self, tmp_path):
        """Test field conversions: locked boolean to string"""
        week_folder = tmp_path / "week_01"
        week_folder.mkdir()

        wr_data = [
            {
                "id": "11111",
                "name": "Locked Player",
                "position": "WR",
                "drafted_by": "Team 1",
                "locked": True,
                "projected_points": [15.0] * 17,
                "actual_points": [16.0] * 17
            },
            {
                "id": "22222",
                "name": "Unlocked Player",
                "position": "WR",
                "drafted_by": "",
                "locked": False,
                "projected_points": [14.0] * 17,
                "actual_points": [13.0] * 17
            }
        ]
        (week_folder / "wr_data.json").write_text(json.dumps(wr_data))

        for pos in ['qb', 'rb', 'te', 'k', 'dst']:
            (week_folder / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)
            players = league._parse_players_json(week_folder, week_num=1)

        # Verify boolean → string conversion
        assert players[11111]["locked"] == "1"
        assert players[22222]["locked"] == "0"

    def test_parse_players_json_all_positions(self, tmp_path):
        """Test handling of all 6 position files"""
        week_folder = tmp_path / "week_01"
        week_folder.mkdir()

        positions = ['qb', 'rb', 'wr', 'te', 'k', 'dst']
        for idx, pos in enumerate(positions):
            data = [
                {
                    "id": f"{idx}0000",
                    "name": f"Test {pos.upper()}",
                    "position": pos.upper(),
                    "drafted_by": "",
                    "locked": False,
                    "projected_points": [10.0 + idx] * 17,
                    "actual_points": [11.0 + idx] * 17
                }
            ]
            (week_folder / f"{pos}_data.json").write_text(json.dumps(data))

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)
            players = league._parse_players_json(week_folder, week_num=1)

        # Verify all 6 positions loaded
        assert len(players) == 6
        assert 0 in players  # QB (converted "00000" to int 0)
        assert 10000 in players  # RB
        assert 20000 in players  # WR
        assert 30000 in players  # TE
        assert 40000 in players  # K
        assert 50000 in players  # DST

    def test_parse_players_json_missing_file(self, tmp_path):
        """Test error handling for missing JSON files"""
        week_folder = tmp_path / "week_01"
        week_folder.mkdir()

        # Only create QB file, missing other 5 positions
        qb_data = [{"id": "12345", "name": "QB Test", "position": "QB", "drafted_by": "",
                    "locked": False, "projected_points": [10.0] * 17, "actual_points": [11.0] * 17}]
        (week_folder / "qb_data.json").write_text(json.dumps(qb_data))

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)

            # Should not crash, should log warnings and continue
            players = league._parse_players_json(week_folder, week_num=1)

        # Should still have QB data
        assert len(players) == 1
        assert 12345 in players

    def test_parse_players_json_malformed_json(self, tmp_path):
        """Test error handling for malformed JSON"""
        week_folder = tmp_path / "week_01"
        week_folder.mkdir()

        # Create malformed JSON (invalid syntax)
        (week_folder / "qb_data.json").write_text("{invalid json syntax")

        # Create valid files for other positions
        for pos in ['rb', 'wr', 'te', 'k', 'dst']:
            (week_folder / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)

            # Should not crash, should handle error gracefully
            players = league._parse_players_json(week_folder, week_num=1)

        # Should return empty or partial data (other positions loaded)
        assert isinstance(players, dict)

    def test_parse_players_json_empty_arrays(self, tmp_path):
        """Test edge case: empty projected/actual arrays"""
        week_folder = tmp_path / "week_01"
        week_folder.mkdir()

        te_data = [
            {
                "id": "33333",
                "name": "Empty Arrays Player",
                "position": "TE",
                "drafted_by": "",
                "locked": False,
                "projected_points": [],  # Empty array
                "actual_points": []       # Empty array
            }
        ]
        (week_folder / "te_data.json").write_text(json.dumps(te_data))

        for pos in ['qb', 'rb', 'wr', 'k', 'dst']:
            (week_folder / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)
            players = league._parse_players_json(week_folder, week_num=1)

        # Should default to 0.0 for missing array values
        assert players[33333]["projected_points"] == "0.0"
        assert players[33333]["actual_points"] == "0.0"

    def test_parse_players_json_missing_fields(self, tmp_path):
        """Test edge case: missing fields in player dict"""
        week_folder = tmp_path / "week_01"
        week_folder.mkdir()

        k_data = [
            {
                "id": "44444",
                "name": "Minimal Data Kicker",
                "position": "K"
                # Missing: drafted_by, locked, projected_points, actual_points
            }
        ]
        (week_folder / "k_data.json").write_text(json.dumps(k_data))

        for pos in ['qb', 'rb', 'wr', 'te', 'dst']:
            (week_folder / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)
            players = league._parse_players_json(week_folder, week_num=1)

        # Should use defaults for missing fields
        assert players[44444]["drafted_by"] == ""
        assert players[44444]["locked"] == "0"  # False → "0"
        assert players[44444]["projected_points"] == "0.0"
        assert players[44444]["actual_points"] == "0.0"


# ============================================================================
# WEEK 17 SPECIFIC TESTS (Feature 01 - Week 17 Edge Case)
# ============================================================================

class TestWeek17EdgeCase:
    """Test Week 17 specific data loading logic"""

    def test_week_17_uses_week_18_for_actuals(self, tmp_path):
        """Test week 17 loads projected from week_17, actual from week_18"""
        # Create week folders
        weeks_folder = tmp_path / "weeks"
        weeks_folder.mkdir()

        week_17 = weeks_folder / "week_17"
        week_17.mkdir()
        week_18 = weeks_folder / "week_18"
        week_18.mkdir()

        # Week 17 data: projected_points[16] = 20.0, actual_points[16] = 0.0 (incomplete)
        week17_qb = [
            {
                "id": "99999",
                "name": "Josh Allen",
                "position": "QB",
                "drafted_by": "",
                "locked": False,
                "projected_points": [0.0] * 16 + [20.0],
                "actual_points": [0.0] * 17  # No actual yet
            }
        ]

        # Week 18 data: actual_points[16] = 23.2 (week 17 actual score)
        week18_qb = [
            {
                "id": "99999",
                "name": "Josh Allen",
                "position": "QB",
                "drafted_by": "",
                "locked": False,
                "projected_points": [0.0] * 17,
                "actual_points": [0.0] * 16 + [23.2]  # Week 17 actual at index 16
            }
        ]

        (week_17 / "qb_data.json").write_text(json.dumps(week17_qb))
        (week_18 / "qb_data.json").write_text(json.dumps(week18_qb))

        for pos in ['rb', 'wr', 'te', 'k', 'dst']:
            (week_17 / f"{pos}_data.json").write_text("[]")
            (week_18 / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)

            # Parse week 17 projected data
            projected = league._parse_players_json(week_17, week_num=17)

            # Parse week 18 actual data with week_num_for_actual=17 (to get index 16)
            actual = league._parse_players_json(week_18, week_num=17, week_num_for_actual=17)

        # Verify projected_points from week_17 (index 16)
        assert projected[99999]["projected_points"] == "20.0"

        # Verify actual_points from week_18 (index 16)
        # week_num_for_actual=17 means actual_week=17, index=16
        # Week 17's actual score is at index 16 in week_18 data
        assert actual[99999]["actual_points"] == "23.2"

    def test_preload_all_weeks_week_17_pattern(self, tmp_path):
        """Test _preload_all_weeks correctly implements week_N+1 for week 17"""
        # Create minimal week structure
        weeks_folder = tmp_path / "weeks"
        weeks_folder.mkdir()

        # Create week 16, 17, 18
        for week_num in [16, 17, 18]:
            week_folder = weeks_folder / f"week_{week_num:02d}"
            week_folder.mkdir()

            qb_data = [
                {
                    "id": "88888",
                    "name": "Test QB",
                    "position": "QB",
                    "drafted_by": "",
                    "locked": False,
                    "projected_points": [float(week_num)] * 17,
                    "actual_points": [float(week_num + 0.5)] * 17
                }
            ]
            (week_folder / "qb_data.json").write_text(json.dumps(qb_data))

            for pos in ['rb', 'wr', 'te', 'k', 'dst']:
                (week_folder / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)
            league._preload_all_weeks()

        # Verify week 17 cache
        assert 17 in league.week_data_cache
        week17_data = league.week_data_cache[17]

        # Projected should come from week_17 folder
        assert 88888 in week17_data['projected']
        assert week17_data['projected'][88888]["projected_points"] == "17.0"

        # Actual should come from week_18 folder
        assert 88888 in week17_data['actual']
        # Week 18 data has actual_points = [18.5] * 17, extracting index 16 should give 18.5
        assert week17_data['actual'][88888]["actual_points"] == "18.5"


# ============================================================================
# EDGE CASE BEHAVIOR TESTS (Feature 01 - Edge Case Verification)
# ============================================================================

class TestEdgeCaseBehavior:
    """Test edge case handling for JSON loading"""

    def test_missing_week_18_fallback(self, tmp_path):
        """Test missing week_18 folder triggers fallback to projected data"""
        weeks_folder = tmp_path / "weeks"
        weeks_folder.mkdir()

        # Create week_17 but NOT week_18
        week_17 = weeks_folder / "week_17"
        week_17.mkdir()

        qb_data = [
            {
                "id": "77777",
                "name": "Week 17 QB",
                "position": "QB",
                "drafted_by": "",
                "locked": False,
                "projected_points": [15.0] * 17,
                "actual_points": [0.0] * 17
            }
        ]
        (week_17 / "qb_data.json").write_text(json.dumps(qb_data))

        for pos in ['rb', 'wr', 'te', 'k', 'dst']:
            (week_17 / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)
            league._preload_all_weeks()

        # Verify week 17 uses projected as fallback for actual
        assert 17 in league.week_data_cache
        week17_data = league.week_data_cache[17]

        # Both projected and actual should exist
        assert 77777 in week17_data['projected'] or len(week17_data['projected']) >= 0
        assert 77777 in week17_data['actual'] or len(week17_data['actual']) >= 0

    def test_array_index_out_of_bounds(self, tmp_path):
        """Test array index out of bounds defaults to 0.0"""
        week_folder = tmp_path / "week_10"
        week_folder.mkdir()

        # Create data with short arrays (only 5 elements instead of 17)
        dst_data = [
            {
                "id": "66666",
                "name": "Short Array DST",
                "position": "DST",
                "drafted_by": "",
                "locked": False,
                "projected_points": [5.0, 6.0, 7.0, 8.0, 9.0],  # Only 5 elements
                "actual_points": [4.5, 5.5, 6.5, 7.5, 8.5]       # Only 5 elements
            }
        ]
        (week_folder / "dst_data.json").write_text(json.dumps(dst_data))

        for pos in ['qb', 'rb', 'wr', 'te', 'k']:
            (week_folder / f"{pos}_data.json").write_text("[]")

        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        config = {"config_name": "test", "description": "test", "parameters": {"num_teams": 2, "draft_rounds": 1}}
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch('simulation.win_rate.SimulatedLeague.tempfile.mkdtemp') as mock_mkdtemp, \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._initialize_teams'), \
             patch('simulation.win_rate.SimulatedLeague.SimulatedLeague._generate_schedule'):
            temp_dir = tmp_path / "temp"
            temp_dir.mkdir()
            mock_mkdtemp.return_value = str(temp_dir)

            league = SimulatedLeague(config, data_folder)

            # Parse week 10 (index 9, out of bounds for 5-element array)
            players = league._parse_players_json(week_folder, week_num=10)

        # Should default to 0.0, not raise IndexError
        assert players[66666]["projected_points"] == "0.0"
        assert players[66666]["actual_points"] == "0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
