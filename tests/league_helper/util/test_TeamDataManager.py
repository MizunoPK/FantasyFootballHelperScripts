"""
Comprehensive Unit Tests for TeamDataManager.py

Tests the TeamDataManager class which manages NFL team rankings and matchup data:
- Loading team data from team_data folder (per-team CSV files)
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
from util.ConfigManager import ConfigManager
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
    """Create temporary data folder with test configuration"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create league_config.json for ConfigManager
    config_content = '''{
      "config_name": "Test Config",
      "description": "Test configuration",
      "parameters": {
        "CURRENT_NFL_WEEK": 6,
        "NFL_SEASON": 2024,
        "NFL_SCORING_FORMAT": "ppr",
        "NORMALIZATION_MAX_SCALE": 125,
        "SAME_POS_BYE_WEIGHT": 0.3,
        "DIFF_POS_BYE_WEIGHT": 0.1,
        "INJURY_PENALTIES": {"LOW": -2, "MEDIUM": -5, "HIGH": -10},
        "ADP_SCORING": {"THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 30}, "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05}, "WEIGHT": 2.5},
        "PLAYER_RATING_SCORING": {"THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20}, "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05}, "WEIGHT": 1.0},
        "TEAM_QUALITY_SCORING": {"MIN_WEEKS": 5, "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6}, "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05}, "WEIGHT": 2.0},
        "PERFORMANCE_SCORING": {"MIN_WEEKS": 3, "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.2}, "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05}, "WEIGHT": 2.5},
        "MATCHUP_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 115, "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 6}, "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05}, "WEIGHT": 1.0},
        "SCHEDULE_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 100, "THRESHOLDS": {"BASE_POSITION": 16, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 2}, "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05}, "WEIGHT": 1.0},
        "DRAFT_ORDER_BONUSES": {"PRIMARY": 85, "SECONDARY": 90},
        "DRAFT_ORDER": [{"RB": "P", "WR": "S"}, {"RB": "P", "FLEX": "S"}, {"QB": "P", "WR": "S"}],
        "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "TE": 2, "K": 2, "DST": 1, "FLEX": 2},
        "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"]
      }
    }'''
    (data_folder / "league_config.json").write_text(config_content)

    return data_folder


@pytest.fixture
def config_manager(mock_data_folder):
    """Create ConfigManager with test configuration"""
    return ConfigManager(mock_data_folder)


@pytest.fixture
def populated_data_folder(mock_data_folder):
    """Data folder with valid team_data folder"""
    team_data_folder = mock_data_folder / "team_data"
    team_data_folder.mkdir()

    # Create team CSV files with 6 weeks of data
    teams_data = {
        'KC': """week,QB,RB,WR,TE,K,points_scored,points_allowed
1,20.5,25.3,35.2,8.1,9.0,31,17
2,18.3,22.1,31.5,7.8,8.5,28,21
3,22.1,28.5,38.3,9.2,10.1,35,14
4,19.8,24.2,33.1,8.5,9.3,30,20
5,21.3,26.8,36.7,8.8,9.8,33,18""",
        'BUF': """week,QB,RB,WR,TE,K,points_scored,points_allowed
1,22.1,24.0,33.5,7.5,8.8,32,15
2,20.5,23.2,35.1,8.0,9.2,30,18
3,21.8,25.5,34.8,7.9,9.0,31,16
4,19.2,22.8,32.5,7.3,8.6,29,19
5,20.8,24.1,33.9,7.7,8.9,30,17""",
        'PHI': """week,QB,RB,WR,TE,K,points_scored,points_allowed
1,19.5,26.3,34.2,8.8,9.5,29,20
2,18.8,25.1,33.5,8.3,9.1,27,22
3,20.2,27.5,35.3,8.9,9.6,30,19
4,19.1,26.0,34.1,8.6,9.3,28,21
5,19.8,26.8,34.7,8.7,9.4,29,20""",
        'DAL': """week,QB,RB,WR,TE,K,points_scored,points_allowed
1,17.5,21.3,29.2,6.8,8.0,23,26
2,16.8,20.1,28.5,6.3,7.6,21,28
3,18.2,22.5,30.3,7.2,8.3,24,25
4,17.1,21.0,29.1,6.6,7.9,22,27
5,17.8,21.8,29.7,6.9,8.1,23,26""",
        'JAX': """week,QB,RB,WR,TE,K,points_scored,points_allowed
1,15.5,18.3,25.2,5.8,7.0,19,30
2,14.8,17.1,24.5,5.3,6.6,17,32
3,16.2,19.5,26.3,6.2,7.3,20,29
4,15.1,18.0,25.1,5.6,6.9,18,31
5,15.8,18.8,25.7,5.9,7.1,19,30""",
        'SF': """week,QB,RB,WR,TE,K,points_scored,points_allowed
1,21.5,27.3,37.2,9.1,10.0,34,13
2,20.3,26.1,36.5,8.8,9.5,32,15
3,22.1,28.5,38.3,9.5,10.2,35,12
4,20.8,27.2,37.1,9.2,9.8,33,14
5,21.3,27.8,37.7,9.3,10.0,34,13"""
    }

    for team, content in teams_data.items():
        (team_data_folder / f"{team}.csv").write_text(content)

    return mock_data_folder


@pytest.fixture
def mock_season_schedule_manager():
    """Mock SeasonScheduleManager for testing"""
    mock_manager = Mock()
    # Default behavior: return None (no opponent)
    mock_manager.get_opponent.return_value = None
    return mock_manager


@pytest.fixture
def team_manager(populated_data_folder, config_manager, mock_season_schedule_manager):
    """TeamDataManager with valid data loaded"""
    return TeamDataManager(populated_data_folder, config_manager, mock_season_schedule_manager, 6)


@pytest.fixture
def empty_team_manager(mock_data_folder, config_manager):
    """TeamDataManager with no team_data folder"""
    return TeamDataManager(mock_data_folder, config_manager, None, 1)


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

    def test_init_sets_team_data_folder_path(self, populated_data_folder, config_manager):
        """Test that team_data_folder path is set correctly"""
        manager = TeamDataManager(populated_data_folder, config_manager, None, 1)
        expected_path = populated_data_folder / "team_data"
        assert manager.team_data_folder == expected_path

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
        """Test loading valid team_data folder"""
        assert len(team_manager.team_data_cache) == 6

        # Verify specific team data - rankings are calculated from weekly data
        kc_data = team_manager.team_data_cache['KC']
        # KC is ranked #2 offensively (SF is #1 with higher avg points_scored)
        assert kc_data.offensive_rank == 2
        assert kc_data.defensive_rank == 3

    def test_load_missing_file(self, mock_data_folder, config_manager):
        """Test loading when team_data folder doesn't exist"""
        manager = TeamDataManager(mock_data_folder, config_manager, None, 1)
        assert manager.team_weekly_data == {}

    def test_load_invalid_csv_format(self, mock_data_folder, config_manager):
        """Test loading malformed CSV in team_data folder"""
        # Create team_data folder with invalid CSV
        team_data_folder = mock_data_folder / "team_data"
        team_data_folder.mkdir()
        (team_data_folder / "KC.csv").write_text("invalid,csv,format\nno,proper,headers")

        manager = TeamDataManager(mock_data_folder, config_manager, None, 1)
        # Should handle gracefully - may load partial/invalid data
        assert isinstance(manager.team_weekly_data, dict)

    def test_load_empty_file(self, mock_data_folder, config_manager):
        """Test loading empty team CSV file"""
        team_data_folder = mock_data_folder / "team_data"
        team_data_folder.mkdir()
        (team_data_folder / "KC.csv").write_text("")

        manager = TeamDataManager(mock_data_folder, config_manager, None, 1)
        # Empty file results in no data for that team
        assert manager.team_weekly_data.get('KC', []) == []


# ============================================================================
# GETTER METHOD TESTS
# ============================================================================

class TestGetterMethods:
    """Test team data getter methods"""

    def test_get_team_offensive_rank_valid(self, team_manager):
        """Test getting offensive rank for valid team"""
        # Rankings calculated from avg points_scored in test data
        # SF: ~33.6, KC: ~31.4, BUF: ~30.4, PHI: ~28.6, DAL: ~22.6, JAX: ~18.6
        assert team_manager.get_team_offensive_rank('SF') == 1
        assert team_manager.get_team_offensive_rank('KC') == 2
        assert team_manager.get_team_offensive_rank('JAX') == 6

    def test_get_team_offensive_rank_invalid(self, team_manager):
        """Test getting offensive rank for invalid team"""
        assert team_manager.get_team_offensive_rank('INVALID') is None
        assert team_manager.get_team_offensive_rank('') is None

    def test_get_team_defensive_rank_valid(self, team_manager):
        """Test getting defensive rank for valid team"""
        # Rankings calculated from avg points_allowed in test data (lower is better)
        # SF: ~13.4, BUF: ~17.0, KC: ~18.0, PHI: ~20.4, DAL: ~26.4, JAX: ~30.4
        assert team_manager.get_team_defensive_rank('SF') == 1
        assert team_manager.get_team_defensive_rank('BUF') == 2
        assert team_manager.get_team_defensive_rank('JAX') == 6

    def test_get_team_defensive_rank_invalid(self, team_manager):
        """Test getting defensive rank for invalid team"""
        assert team_manager.get_team_defensive_rank('INVALID') is None

    def test_get_team_opponent_valid(self, populated_data_folder, config_manager):
        """Test getting opponent for valid team"""
        mock_schedule = Mock()
        mock_schedule.get_opponent.side_effect = lambda team, week: {
            ('KC', 6): 'LV',
            ('BUF', 6): 'MIA',
            ('PHI', 6): 'NYG'
        }.get((team, week))

        manager = TeamDataManager(populated_data_folder, config_manager, mock_schedule, 6)
        assert manager.get_team_opponent('KC') == 'LV'
        assert manager.get_team_opponent('BUF') == 'MIA'
        assert manager.get_team_opponent('PHI') == 'NYG'

    def test_get_team_opponent_invalid(self, populated_data_folder, config_manager):
        """Test getting opponent for invalid team"""
        mock_schedule = Mock()
        mock_schedule.get_opponent.return_value = None

        manager = TeamDataManager(populated_data_folder, config_manager, mock_schedule, 6)
        assert manager.get_team_opponent('INVALID') is None

    def test_get_team_data_valid(self, team_manager):
        """Test getting complete TeamData object"""
        team_data = team_manager.get_team_data('KC')
        assert team_data is not None
        assert team_data.team == 'KC'
        # KC is #2 offense (SF #1), #3 defense (SF #1, BUF #2)
        assert team_data.offensive_rank == 2
        assert team_data.defensive_rank == 3

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

    def test_reload_team_data(self, populated_data_folder, config_manager):
        """Test reloading team data"""
        manager = TeamDataManager(populated_data_folder, config_manager, None, 6)
        assert len(manager.team_weekly_data) == 6

        # Remove some team files
        (populated_data_folder / "team_data" / "KC.csv").unlink()
        (populated_data_folder / "team_data" / "BUF.csv").unlink()

        # Reload
        manager.reload_team_data()
        assert len(manager.team_weekly_data) == 4
        assert 'KC' not in manager.team_weekly_data

    def test_reload_clears_cache(self, team_manager):
        """Test that reload clears existing cache"""
        assert len(team_manager.team_weekly_data) == 6
        team_manager.reload_team_data()
        # Should reload same data
        assert len(team_manager.team_weekly_data) == 6


# ============================================================================
# RANK DIFFERENCE CALCULATION TESTS
# ============================================================================

@pytest.mark.skip(reason="Tests use old teams.csv format - needs rewrite for team_data folder format")
class TestRankDifference:
    """Test get_rank_difference() method"""

    def test_offensive_player_favorable_matchup(self, team_manager):
        """Test offensive player with favorable matchup (positive diff)"""
        # KC offense (#1) vs opponent - testing with incomplete data

        manager = team_manager
        # Test with QB position (uses position-specific defense rank)
        diff = manager.get_rank_difference('KC', 'QB')
        # Since LV isn't in our test data, should return 0
        assert diff == 0

    def test_offensive_player_unfavorable_matchup(self, populated_data_folder):
        """Test offensive player with tough matchup (strong defense)"""
        # Create complete matchup data with position-specific defense ranks
        teams_csv = """team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
KC,1,15,,,,,
BUF,10,3,3,5,4,6,8
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        # Mock schedule manager to return BUF as KC's opponent
        mock_schedule = Mock()
        mock_schedule.get_opponent.return_value = 'BUF'

        manager = TeamDataManager(populated_data_folder, mock_schedule, 1)

        # KC QB vs BUF defense vs QB (#3)
        # matchup_score = 3 (tough - low rank = strong defense)
        diff = manager.get_rank_difference('KC', 'QB')
        assert diff == 3

    def test_defensive_player_favorable_matchup(self, populated_data_folder):
        """Test defensive player with favorable matchup"""
        teams_csv = """team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
SF,10,1,,,,,
DAL,25,20,,,,,
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        # Mock schedule manager to return DAL as SF's opponent
        mock_schedule = Mock()
        mock_schedule.get_opponent.return_value = 'DAL'

        manager = TeamDataManager(populated_data_folder, mock_schedule, 1)

        # SF DST vs DAL offense (#25)
        # matchup_score = 25 (favorable - high rank = weak offense)
        diff = manager.get_rank_difference('SF', 'DST')
        assert diff == 25

    def test_defensive_player_unfavorable_matchup(self, populated_data_folder):
        """Test defensive player with unfavorable matchup"""
        teams_csv = """team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
JAX,30,28,,,,,
KC,1,15,,,,,
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        # Mock schedule manager to return KC as JAX's opponent
        mock_schedule = Mock()
        mock_schedule.get_opponent.return_value = 'KC'

        manager = TeamDataManager(populated_data_folder, mock_schedule, 1)

        # JAX DST vs KC offense (#1)
        # matchup_score = 1 (tough - low rank = strong offense)
        diff = manager.get_rank_difference('JAX', 'DST')
        assert diff == 1

    def test_rank_difference_neutral_matchup(self, populated_data_folder):
        """Test matchup with mid-tier defense"""
        teams_csv = """team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
TEAM1,15,10,,15,,,
TEAM2,20,15,,15,,,
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        # Mock schedule manager to return TEAM2 as TEAM1's opponent
        mock_schedule = Mock()
        mock_schedule.get_opponent.return_value = 'TEAM2'

        manager = TeamDataManager(populated_data_folder, mock_schedule, 1)

        # TEAM1 RB vs TEAM2 defense vs RB (#15)
        # matchup_score = 15 (mid-tier defense)
        diff = manager.get_rank_difference('TEAM1', 'RB')
        assert diff == 15

    def test_rank_difference_no_matchup_data(self, empty_team_manager):
        """Test rank difference with no data loaded"""
        diff = empty_team_manager.get_rank_difference('KC', 'QB')
        assert diff == 0

    def test_rank_difference_invalid_team(self, team_manager):
        """Test rank difference for team not in data"""
        diff = team_manager.get_rank_difference('INVALID', 'QB')
        assert diff == 0

    def test_rank_difference_no_opponent_data(self, populated_data_folder):
        """Test rank difference when opponent data missing"""
        teams_csv = """team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
KC,1,5,,,,,
"""
        # LV not in data, so no opponent data available
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        # Mock schedule manager to return LV (which is not in the data)
        mock_schedule = Mock()
        mock_schedule.get_opponent.return_value = 'LV'

        manager = TeamDataManager(populated_data_folder, mock_schedule, 1)

        diff = manager.get_rank_difference('KC', 'QB')
        # Should return 0 when opponent data missing
        assert diff == 0


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

@pytest.mark.skip(reason="Tests use old teams.csv format - needs rewrite for team_data folder format")
class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_team_with_none_values(self, mock_data_folder):
        """Test handling teams with None values"""
        teams_csv = """team,offensive_rank,defensive_rank
KC,1,
"""
        teams_file = mock_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        manager = TeamDataManager(mock_data_folder, None, 1)

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
        teams_csv = """team,offensive_rank,defensive_rank
KC,1,5
BUF,2,3
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        # Mock schedule manager to return LV for both teams
        mock_schedule = Mock()
        mock_schedule.get_opponent.return_value = 'LV'

        manager = TeamDataManager(populated_data_folder, mock_schedule, 1)

        assert manager.get_team_opponent('KC') == 'LV'
        assert manager.get_team_opponent('BUF') == 'LV'

    def test_circular_opponents(self, populated_data_folder):
        """Test handling circular opponent references"""
        teams_csv = """team,offensive_rank,defensive_rank
KC,1,5
BUF,2,3
"""
        teams_file = populated_data_folder / "teams.csv"
        teams_file.write_text(teams_csv)

        # Mock schedule manager to return opposite teams
        mock_schedule = Mock()
        mock_schedule.get_opponent.side_effect = lambda team, week: {
            ('KC', 1): 'BUF',
            ('BUF', 1): 'KC'
        }.get((team, week))

        manager = TeamDataManager(populated_data_folder, mock_schedule, 1)

        assert manager.get_team_opponent('KC') == 'BUF'
        assert manager.get_team_opponent('BUF') == 'KC'


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
