"""
Unit tests for fantasy_points_calculator module

Tests fantasy points extraction, stat parsing, and fallback logic.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from fantasy_points_calculator import (
    FantasyPointsConfig,
    FantasyPointsExtractor,
    extract_week_fantasy_points,
    extract_stat_entry_fantasy_points
)


class TestFantasyPointsConfig:
    """Test FantasyPointsConfig dataclass"""

    def test_default_config(self):
        """Test default configuration values"""
        config = FantasyPointsConfig()

        assert config.prefer_actual_over_projected is True
        assert config.include_negative_dst_points is True

    def test_custom_config(self):
        """Test custom configuration values"""
        config = FantasyPointsConfig(
            prefer_actual_over_projected=False,
            include_negative_dst_points=False
        )

        assert config.prefer_actual_over_projected is False
        assert config.include_negative_dst_points is False


class TestFantasyPointsExtractorInitialization:
    """Test FantasyPointsExtractor initialization"""

    def test_init_with_default_config(self):
        """Test initialization with default config"""
        extractor = FantasyPointsExtractor()

        assert extractor.config.prefer_actual_over_projected is True
        assert extractor.config.include_negative_dst_points is True

    def test_init_with_custom_config(self):
        """Test initialization with custom config"""
        config = FantasyPointsConfig(prefer_actual_over_projected=False)
        extractor = FantasyPointsExtractor(config=config)

        assert extractor.config.prefer_actual_over_projected is False

    def test_init_with_custom_season(self):
        """Test initialization with custom season"""
        extractor = FantasyPointsExtractor(season=2023)

        assert extractor.season == 2023

    def test_init_stores_config(self):
        """Test initialization stores config reference"""
        config = FantasyPointsConfig()
        extractor = FantasyPointsExtractor(config=config)

        assert extractor.config is config


class TestExtractStatEntryPoints:
    """Test extract_stat_entry_points method"""

    def test_extract_applied_total(self):
        """Test extracting appliedTotal"""
        extractor = FantasyPointsExtractor()
        stat_entry = {'appliedTotal': 25.5}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 25.5

    def test_extract_projected_total_when_no_applied(self):
        """Test extracting projectedTotal as fallback"""
        extractor = FantasyPointsExtractor()
        stat_entry = {'projectedTotal': 20.3}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 20.3

    def test_extract_prefers_applied_over_projected(self):
        """Test appliedTotal takes priority over projectedTotal"""
        extractor = FantasyPointsExtractor()
        stat_entry = {
            'appliedTotal': 25.5,
            'projectedTotal': 20.3
        }

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 25.5

    def test_extract_returns_zero_when_no_data(self):
        """Test returns 0.0 when no fantasy points available"""
        extractor = FantasyPointsExtractor()
        stat_entry = {}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 0.0

    def test_extract_handles_none_stat_entry(self):
        """Test handles None stat entry gracefully"""
        extractor = FantasyPointsExtractor()

        result = extractor.extract_stat_entry_points(None)

        assert result == 0.0

    def test_extract_handles_null_applied_total(self):
        """Test handles null appliedTotal"""
        extractor = FantasyPointsExtractor()
        stat_entry = {'appliedTotal': None, 'projectedTotal': 15.0}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 15.0

    def test_extract_handles_null_both_values(self):
        """Test handles null values for both fields"""
        extractor = FantasyPointsExtractor()
        stat_entry = {'appliedTotal': None, 'projectedTotal': None}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 0.0

    def test_extract_handles_string_numbers(self):
        """Test converts string numbers to float"""
        extractor = FantasyPointsExtractor()
        stat_entry = {'appliedTotal': '25.5'}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 25.5

    def test_extract_handles_invalid_data_type(self):
        """Test handles invalid data types gracefully"""
        extractor = FantasyPointsExtractor()
        stat_entry = {'appliedTotal': 'invalid'}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 0.0


class TestExtractFromStatsArray:
    """Test _extract_from_stats_array method"""

    def test_extract_from_stats_array_applied_total(self):
        """Test extracting appliedTotal from stats array"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 25.5
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(player_data, 5, 'RB')

        assert result == 25.5

    def test_extract_from_stats_array_projected_total(self):
        """Test extracting projectedTotal from stats array"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'projectedTotal': 20.3
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(player_data, 5, 'WR')

        assert result == 20.3

    def test_extract_from_stats_array_filters_by_week(self):
        """Test filters stats by scoringPeriodId"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 4,
                        'appliedTotal': 15.0
                    },
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 25.5
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(player_data, 5, 'QB')

        assert result == 25.5

    def test_extract_from_stats_array_filters_by_season(self):
        """Test filters stats by seasonId"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2023,
                        'scoringPeriodId': 5,
                        'appliedTotal': 15.0
                    },
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 25.5
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(player_data, 5, 'TE')

        assert result == 25.5

    def test_extract_from_stats_array_returns_none_when_not_found(self):
        """Test returns None when week not found"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 4,
                        'appliedTotal': 15.0
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(player_data, 5, 'RB')

        assert result is None

    def test_extract_from_stats_array_handles_empty_stats(self):
        """Test handles empty stats array"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {'player': {'stats': []}}

        result = extractor._extract_from_stats_array(player_data, 5, 'WR')

        assert result is None

    def test_extract_from_stats_array_handles_missing_stats(self):
        """Test handles missing stats key"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {'player': {}}

        result = extractor._extract_from_stats_array(player_data, 5, 'QB')

        assert result is None

    def test_extract_from_stats_array_handles_negative_dst_points(self):
        """Test allows negative DST points by default"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': -5.0
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(player_data, 5, 'DST')

        assert result == -5.0

    def test_extract_from_stats_array_skips_negative_non_dst(self):
        """Test skips negative points for non-DST positions"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': -5.0
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(player_data, 5, 'QB')

        assert result is None

    def test_extract_from_stats_array_disables_negative_dst_when_configured(self):
        """Test can disable negative DST points via config"""
        config = FantasyPointsConfig(include_negative_dst_points=False)
        extractor = FantasyPointsExtractor(config=config, season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': -5.0
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(player_data, 5, 'DST')

        assert result is None

    def test_extract_from_stats_array_week_priority_past_week(self):
        """Test prioritizes appliedTotal for past weeks"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 3,
                        'appliedTotal': 25.5,
                        'projectedTotal': 20.0
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(
            player_data, 3, 'RB', current_nfl_week=5
        )

        assert result == 25.5

    def test_extract_from_stats_array_week_priority_future_week(self):
        """Test prioritizes projectedTotal for future weeks"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 8,
                        'appliedTotal': 25.5,
                        'projectedTotal': 20.0
                    }
                ]
            }
        }

        result = extractor._extract_from_stats_array(
            player_data, 8, 'RB', current_nfl_week=5
        )

        assert result == 20.0


class TestExtractWeekPoints:
    """Test extract_week_points method"""

    def test_extract_week_points_success(self):
        """Test successful extraction of week points"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 25.5
                    }
                ]
            }
        }

        result = extractor.extract_week_points(player_data, 5, 'RB', 'Test Player')

        assert result == 25.5

    def test_extract_week_points_returns_zero_when_no_data(self):
        """Test returns 0.0 when no ESPN data available"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {'player': {'stats': []}}

        result = extractor.extract_week_points(player_data, 5, 'WR', 'Test Player')

        assert result == 0.0

    def test_extract_week_points_handles_exception(self):
        """Test handles exceptions gracefully"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = None  # Will cause exception

        result = extractor.extract_week_points(player_data, 5, 'QB', 'Test Player')

        assert result == 0.0

    def test_extract_week_points_with_current_nfl_week(self):
        """Test extraction with current_nfl_week parameter"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 3,
                        'appliedTotal': 25.5,
                        'projectedTotal': 20.0
                    }
                ]
            }
        }

        result = extractor.extract_week_points(
            player_data, 3, 'RB', 'Test Player', current_nfl_week=5
        )

        assert result == 25.5


class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_extract_week_fantasy_points(self):
        """Test extract_week_fantasy_points convenience function"""
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 25.5
                    }
                ]
            }
        }

        result = extract_week_fantasy_points(
            player_data, 5, 'RB', 'Test Player', season=2024
        )

        assert result == 25.5

    def test_extract_week_fantasy_points_with_custom_config(self):
        """Test convenience function with custom config"""
        config = FantasyPointsConfig(include_negative_dst_points=False)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': -5.0
                    }
                ]
            }
        }

        result = extract_week_fantasy_points(
            player_data, 5, 'DST', 'Test DST', config=config, season=2024
        )

        assert result == 0.0

    def test_extract_stat_entry_fantasy_points(self):
        """Test extract_stat_entry_fantasy_points convenience function"""
        stat_entry = {'appliedTotal': 25.5}

        result = extract_stat_entry_fantasy_points(stat_entry)

        assert result == 25.5

    def test_extract_stat_entry_fantasy_points_none(self):
        """Test convenience function with None entry"""
        result = extract_stat_entry_fantasy_points(None)

        assert result == 0.0


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_extract_zero_points(self):
        """Test extraction of 0.0 points"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 0.0
                    }
                ]
            }
        }

        result = extractor.extract_week_points(player_data, 5, 'K', 'Kicker')

        assert result == 0.0

    def test_extract_very_large_points(self):
        """Test extraction of very large point values"""
        extractor = FantasyPointsExtractor(season=2024)
        stat_entry = {'appliedTotal': 500.0}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 500.0

    def test_extract_fractional_points(self):
        """Test extraction of fractional point values"""
        extractor = FantasyPointsExtractor(season=2024)
        stat_entry = {'appliedTotal': 25.567}

        result = extractor.extract_stat_entry_points(stat_entry)

        assert result == 25.567

    def test_extract_playoff_week(self):
        """Test extraction for playoff weeks (19-22)"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 19,
                        'appliedTotal': 30.0
                    }
                ]
            }
        }

        result = extractor.extract_week_points(player_data, 19, 'QB', 'Playoff QB')

        assert result == 30.0

    def test_extract_with_multiple_stat_entries(self):
        """Test extraction with multiple stat entries for same week"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 15.0
                    },
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 25.5
                    }
                ]
            }
        }

        # Should return first matching entry
        result = extractor.extract_week_points(player_data, 5, 'RB', 'Test Player')

        assert result == 15.0

    def test_extract_handles_invalid_stat_structure(self):
        """Test handles invalid stat entry structure"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    'invalid_stat',  # Not a dict
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 5,
                        'appliedTotal': 25.5
                    }
                ]
            }
        }

        result = extractor.extract_week_points(player_data, 5, 'WR', 'Test Player')

        assert result == 25.5


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_full_season_data_extraction(self):
        """Test extracting data for multiple weeks"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {'seasonId': 2024, 'scoringPeriodId': 1, 'appliedTotal': 20.0},
                    {'seasonId': 2024, 'scoringPeriodId': 2, 'appliedTotal': 25.0},
                    {'seasonId': 2024, 'scoringPeriodId': 3, 'appliedTotal': 30.0}
                ]
            }
        }

        week1 = extractor.extract_week_points(player_data, 1, 'RB', 'Player')
        week2 = extractor.extract_week_points(player_data, 2, 'RB', 'Player')
        week3 = extractor.extract_week_points(player_data, 3, 'RB', 'Player')

        assert week1 == 20.0
        assert week2 == 25.0
        assert week3 == 30.0

    def test_mixed_actual_and_projected_data(self):
        """Test handling mix of actual and projected data"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {'seasonId': 2024, 'scoringPeriodId': 1, 'appliedTotal': 20.0},
                    {'seasonId': 2024, 'scoringPeriodId': 2, 'projectedTotal': 22.0},
                    {'seasonId': 2024, 'scoringPeriodId': 3, 'appliedTotal': 25.0, 'projectedTotal': 23.0}
                ]
            }
        }

        week1 = extractor.extract_week_points(player_data, 1, 'WR', 'Player')
        week2 = extractor.extract_week_points(player_data, 2, 'WR', 'Player')
        week3 = extractor.extract_week_points(player_data, 3, 'WR', 'Player')

        assert week1 == 20.0  # appliedTotal
        assert week2 == 22.0  # projectedTotal
        assert week3 == 25.0  # appliedTotal (preferred)

    def test_dst_with_negative_and_positive_points(self):
        """Test DST with both negative and positive performances"""
        extractor = FantasyPointsExtractor(season=2024)
        player_data = {
            'player': {
                'stats': [
                    {'seasonId': 2024, 'scoringPeriodId': 1, 'appliedTotal': 15.0},
                    {'seasonId': 2024, 'scoringPeriodId': 2, 'appliedTotal': -5.0},
                    {'seasonId': 2024, 'scoringPeriodId': 3, 'appliedTotal': 8.0}
                ]
            }
        }

        week1 = extractor.extract_week_points(player_data, 1, 'DST', 'Defense')
        week2 = extractor.extract_week_points(player_data, 2, 'DST', 'Defense')
        week3 = extractor.extract_week_points(player_data, 3, 'DST', 'Defense')

        assert week1 == 15.0
        assert week2 == -5.0  # Negative allowed for DST
        assert week3 == 8.0
