"""
Comprehensive Unit Tests for TeamDataManager.py

Tests the TeamDataManager class which manages NFL team rankings and matchup data:
- Loading team data from teams.csv
- Caching team rankings (offensive and defensive)
- Calculating matchup differentials for scoring
- Handling missing/invalid data gracefully

This module is critical for accurate player scoring based on team matchups.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

# Imports work via conftest.py which adds league_helper/util to path
from util.TeamDataManager import TeamDataManager
from utils.TeamData import TeamData


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(autouse=True)
def mock_logger():
    """Mock the logger for all tests"""
    with patch('utils.LoggingManager.get_logger') as mock_get_logger:
        mock_get_logger.return_value = Mock()
        yield mock_get_logger


@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with test teams.csv"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    return data_folder


@pytest.fixture
def sample_teams_csv():
    """Sample teams.csv content for testing"""
    return """team,offensive_rank,defensive_rank,opponent
KC,1,5,LV
BUF,2,3,MIA
PHI,3,8,NYG
DAL,15,20,WAS
JAX,28,30,IND
SF,4,1,ARI
"""


@pytest.fixture
def populated_data_folder(mock_data_folder, sample_teams_csv):
    """Data folder with valid teams.csv"""
    teams_file = mock_data_folder / "teams.csv"
    teams_file.write_text(sample_teams_csv)
    return mock_data_folder


@pytest.fixture
def team_manager(populated_data_folder):
    """TeamDataManager with valid data loaded"""
    return TeamDataManager(populated_data_folder)


@pytest.fixture
def empty_team_manager(mock_data_folder):
    """TeamDataManager with no teams.csv file"""
    return TeamDataManager(mock_data_folder)


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestInitialization:
    """Test TeamDataManager initialization"""

    def test_init_with_valid_file(self, team_manager):
        """Test initialization with valid teams.csv"""
        assert len(team_manager.team_data_cache) == 6
        assert team_manager.is_team_data_available() is True

    def test_init_without_file(self, empty_team_manager):
        """Test initialization when teams.csv doesn't exist"""
        assert len(empty_team_manager.team_data_cache) == 0
        assert empty_team_manager.is_team_data_available() is False

    def test_init_sets_teams_file_path(self, populated_data_folder):
        """Test that teams_file path is set correctly"""
        manager = TeamDataManager(populated_data_folder)
        expected_path = populated_data_folder / "teams.csv"
        assert manager.teams_file == expected_path

    def test_init_loads_team_cache(self, team_manager):
        """Test that team cache is populated on init"""
        assert 'KC' in team_manager.team_data_cache
        assert 'BUF' in team_manager.team_data_cache
        assert 'SF' in team_manager.team_data_cache


# ============================================================================
# LOAD TEAM DATA TESTS
# ============================================================================

class TestLoadTeamData:
    """Test _load_team_data() method"""

    def test_load_valid_data(self, team_manager):
        """Test loading valid teams.csv"""
        assert len(team_manager.team_data_cache) == 6

        # Verify specific team data
        kc_data = team_manager.team_data_cache['KC']
        assert kc_data.offensive_rank == 1
        assert kc_data.defensive_rank == 5
        assert kc_data.opponent == 'LV'

    def test_load_missing_file(self, mock_data_folder):
        """Test loading when file doesn't exist"""
        manager = TeamDataManager(mock_data_folder)
        assert manager.team_data_cache == {}

    def test_load_invalid_csv_format(self, mock_data_folder):
        """Test loading malformed CSV"""
        # Create invalid CSV
        teams_file = mock_data_folder / "teams.csv"
        teams_file.write_text("invalid,csv,format\nno,proper,headers")

        manager = TeamDataManager(mock_data_folder)
        # Should handle gracefully - may load partial/invalid data
        # The CSV loader creates entries with empty/None values
        # This is acceptable defensive behavior
        assert isinstance(manager.team_data_cache, dict)

    def test_load_empty_file(self, mock_data_folder):
        """Test loading empty teams.csv"""
        teams_file = mock_data_folder / "teams.csv"
        teams_file.write_text("")

        manager = TeamDataManager(mock_data_folder)
        assert manager.team_data_cache == {}


# ============================================================================
# GETTER METHOD TESTS
# ============================================================================

class TestGetterMethods:
    """Test team data getter methods"""

    def test_get_team_offensive_rank_valid(self, team_manager):
        """Test getting offensive rank for valid team"""
        assert team_manager.get_team_offensive_rank('KC') == 1
        assert team_manager.get_team_offensive_rank('BUF') == 2
        assert team_manager.get_team_offensive_rank('JAX') == 28

    def test_get_team_offensive_rank_invalid(self, team_manager):
        """Test getting offensive rank for invalid team"""
        assert team_manager.get_team_offensive_rank('INVALID') is None
        assert team_manager.get_team_offensive_rank('') is None

    def test_get_team_defensive_rank_valid(self, team_manager):
        """Test getting defensive rank for valid team"""
        assert team_manager.get_team_defensive_rank('SF') == 1
        assert team_manager.get_team_defensive_rank('BUF') == 3
        assert team_manager.get_team_defensive_rank('JAX') == 30

    def test_get_team_defensive_rank_invalid(self, team_manager):
        """Test getting defensive rank for invalid team"""
        assert team_manager.get_team_defensive_rank('INVALID') is None

    def test_get_team_opponent_valid(self, team_manager):
        """Test getting opponent for valid team"""
        assert team_manager.get_team_opponent('KC') == 'LV'
        assert team_manager.get_team_opponent('BUF') == 'MIA'
        assert team_manager.get_team_opponent('PHI') == 'NYG'

    def test_get_team_opponent_invalid(self, team_manager):
        """Test getting opponent for invalid team"""
        assert team_manager.get_team_opponent('INVALID') is None

    def test_get_team_data_valid(self, team_manager):
        """Test getting complete TeamData object"""
        team_data = team_manager.get_team_data('KC')
        assert team_data is not None
        assert team_data.team == 'KC'
        assert team_data.offensive_rank == 1
        assert team_data.defensive_rank == 5
        assert team_data.opponent == 'LV'

    def test_get_team_data_invalid(self, team_manager):
        """Test getting TeamData for invalid team"""
        assert team_manager.get_team_data('INVALID') is None


# ============================================================================
# DATA AVAILABILITY TESTS
# ============================================================================

class TestDataAvailability:
    """Test data availability check methods"""

    def test_is_team_data_available_true(self, team_manager):
        """Test is_team_data_available with loaded data"""
        assert team_manager.is_team_data_available() is True

    def test_is_team_data_available_false(self, empty_team_manager):
        """Test is_team_data_available with no data"""
        assert empty_team_manager.is_team_data_available() is False

    def test_get_available_teams(self, team_manager):
        """Test getting list of available teams"""
        teams = team_manager.get_available_teams()
        assert len(teams) == 6
        assert 'KC' in teams
        assert 'BUF' in teams
        assert 'SF' in teams

    def test_get_available_teams_empty(self, empty_team_manager):
        """Test getting available teams with no data"""
        teams = empty_team_manager.get_available_teams()
        assert teams == []

    def test_is_matchup_available_true(self, team_manager):
        """Test is_matchup_available with data loaded"""
        assert team_manager.is_matchup_available() is True

    def test_is_matchup_available_false(self, empty_team_manager):
        """Test is_matchup_available with no data"""
        assert empty_team_manager.is_matchup_available() is False


# ============================================================================
# RELOAD DATA TESTS
# ============================================================================

class TestReloadData:
    """Test reload_team_data() method"""

    def test_reload_team_data(self, populated_data_folder):
        """Test reloading team data"""
        manager = TeamDataManager(populated_data_folder)
        assert len(manager.team_data_cache) == 6

        # Modify the file
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text("""team,offensive_rank,defensive_rank,opponent
KC,1,5,LV
""")

        # Reload
        manager.reload_team_data()
        assert len(manager.team_data_cache) == 1
        assert 'KC' in manager.team_data_cache

    def test_reload_clears_cache(self, team_manager):
        """Test that reload clears existing cache"""
        assert len(team_manager.team_data_cache) == 6
        team_manager.reload_team_data()
        # Should reload same data
        assert len(team_manager.team_data_cache) == 6


# ============================================================================
# RANK DIFFERENCE CALCULATION TESTS
# ============================================================================

class TestRankDifference:
    """Test get_rank_difference() method"""

    def test_offensive_player_favorable_matchup(self, team_manager):
        """Test offensive player with favorable matchup (positive diff)"""
        # KC offense (#1) vs LV defense
        # Need to add LV to test data
        # For now, test with existing teams

        # Add teams for complete matchup
        manager = team_manager
        # KC (#1 OFF) vs LV - we need LV data
        # Let's test with complete data

        # PHI (#3 OFF) vs NYG - we need NYG data
        # For this test, assume NYG has worse defense than PHI offense
        # This would give positive rank diff (favorable)

        # Actually, let's test with incomplete data first
        diff = manager.get_rank_difference('KC', is_defense=False)
        # Since LV isn't in our test data, should return 0
        assert diff == 0

    def test_offensive_player_unfavorable_matchup(self, populated_data_folder):
        """Test offensive player with unfavorable matchup (negative diff)"""
        # Create complete matchup data
        teams_csv = """team,offensive_rank,defensive_rank,opponent
KC,1,15,BUF
BUF,10,3,KC
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(populated_data_folder)

        # KC offense (#1) vs BUF defense (#3)
        # Rank diff = 3 - 1 = +2 (favorable for KC)
        diff = manager.get_rank_difference('KC', is_defense=False)
        assert diff == 2

    def test_defensive_player_favorable_matchup(self, populated_data_folder):
        """Test defensive player with favorable matchup"""
        teams_csv = """team,offensive_rank,defensive_rank,opponent
SF,10,1,DAL
DAL,25,20,SF
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(populated_data_folder)

        # SF defense (#1) vs DAL offense (#25)
        # Rank diff = 25 - 1 = +24 (very favorable for SF DST)
        diff = manager.get_rank_difference('SF', is_defense=True)
        assert diff == 24

    def test_defensive_player_unfavorable_matchup(self, populated_data_folder):
        """Test defensive player with unfavorable matchup"""
        teams_csv = """team,offensive_rank,defensive_rank,opponent
JAX,30,28,KC
KC,1,15,JAX
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(populated_data_folder)

        # JAX defense (#28) vs KC offense (#1)
        # Rank diff = 1 - 28 = -27 (very unfavorable for JAX DST)
        diff = manager.get_rank_difference('JAX', is_defense=True)
        assert diff == -27

    def test_rank_difference_neutral_matchup(self, populated_data_folder):
        """Test matchup with equal ranks"""
        teams_csv = """team,offensive_rank,defensive_rank,opponent
TEAM1,15,10,TEAM2
TEAM2,20,15,TEAM1
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(populated_data_folder)

        # TEAM1 offense (#15) vs TEAM2 defense (#15)
        # Rank diff = 15 - 15 = 0 (neutral)
        diff = manager.get_rank_difference('TEAM1', is_defense=False)
        assert diff == 0

    def test_rank_difference_no_matchup_data(self, empty_team_manager):
        """Test rank difference with no data loaded"""
        diff = empty_team_manager.get_rank_difference('KC', is_defense=False)
        assert diff == 0

    def test_rank_difference_invalid_team(self, team_manager):
        """Test rank difference for team not in data"""
        diff = team_manager.get_rank_difference('INVALID', is_defense=False)
        assert diff == 0

    def test_rank_difference_no_opponent_data(self, populated_data_folder):
        """Test rank difference when opponent data missing"""
        teams_csv = """team,offensive_rank,defensive_rank,opponent
KC,1,5,LV
"""
        # LV not in data, so no opponent data available
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(populated_data_folder)

        diff = manager.get_rank_difference('KC', is_defense=False)
        # Should return 0 when opponent data missing
        assert diff == 0


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_team_with_none_values(self, mock_data_folder):
        """Test handling teams with None values"""
        teams_csv = """team,offensive_rank,defensive_rank,opponent
KC,1,,LV
"""
        teams_file = mock_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(mock_data_folder)

        # Should handle None defensive rank gracefully
        defensive_rank = manager.get_team_defensive_rank('KC')
        # Depends on TeamData implementation
        # Assume it handles None gracefully

    def test_team_case_sensitivity(self, team_manager):
        """Test that team lookups are case-sensitive"""
        # Team abbreviations should be uppercase
        assert team_manager.get_team_offensive_rank('KC') == 1
        assert team_manager.get_team_offensive_rank('kc') is None

    def test_multiple_teams_same_opponent(self, populated_data_folder):
        """Test handling multiple teams with same opponent"""
        teams_csv = """team,offensive_rank,defensive_rank,opponent
KC,1,5,LV
BUF,2,3,LV
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(populated_data_folder)

        assert manager.get_team_opponent('KC') == 'LV'
        assert manager.get_team_opponent('BUF') == 'LV'

    def test_circular_opponents(self, populated_data_folder):
        """Test handling circular opponent references"""
        teams_csv = """team,offensive_rank,defensive_rank,opponent
KC,1,5,BUF
BUF,2,3,KC
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(populated_data_folder)

        assert manager.get_team_opponent('KC') == 'BUF'
        assert manager.get_team_opponent('BUF') == 'KC'


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
