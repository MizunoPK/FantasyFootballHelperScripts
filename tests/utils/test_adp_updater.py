"""
Unit tests for utils.adp_updater module

Tests the player matching and ADP update functionality with various scenarios
including normal operation, edge cases, and error conditions.

Author: Claude Code (Epic: fix_2025_adp, Feature 2)
Created: 2025-12-31
"""

import pytest
import json
from pathlib import Path
import pandas as pd

from utils.adp_updater import (
    normalize_name,
    calculate_similarity,
    extract_dst_team_name,
    find_best_match,
    update_player_adp_values
)


class TestNormalizeName:
    """Test the normalize_name() function"""

    def test_lowercase_conversion(self):
        """Test that names are converted to lowercase"""
        assert normalize_name("Patrick Mahomes") == "patrick mahomes"

    def test_removes_punctuation(self):
        """Test that punctuation is removed"""
        assert normalize_name("Ja'Marr Chase") == "jamarr chase"
        assert normalize_name("Amon-Ra St. Brown") == "amon ra st brown"  # Hyphen becomes space

    def test_removes_suffixes(self):
        """Test that name suffixes are removed"""
        assert normalize_name("Kenneth Walker III") == "kenneth walker"
        assert normalize_name("Patrick Mahomes Jr.") == "patrick mahomes"
        assert normalize_name("Player Name II") == "player name"

    def test_collapses_whitespace(self):
        """Test that extra whitespace is collapsed"""
        assert normalize_name("Patrick   Mahomes") == "patrick mahomes"
        assert normalize_name("  Name  Player  ") == "name player"


class TestCalculateSimilarity:
    """Test the calculate_similarity() function"""

    def test_identical_names(self):
        """Test that identical names have score of 1.0"""
        score = calculate_similarity("patrick mahomes", "patrick mahomes")
        assert score == 1.0

    def test_similar_names(self):
        """Test that similar names have high scores"""
        score = calculate_similarity("patrick mahomes", "patrick mahomes ii")
        assert score > 0.85

    def test_different_names(self):
        """Test that different names have low scores"""
        score = calculate_similarity("patrick mahomes", "tom brady")
        assert score < 0.5


class TestExtractDstTeamName:
    """Test the extract_dst_team_name() function"""

    def test_json_format(self):
        """Test extraction from JSON format (Team D/ST)"""
        assert extract_dst_team_name("Ravens D/ST") == "ravens"
        assert extract_dst_team_name("49ers D/ST") == "49ers"
        assert extract_dst_team_name("Patriots D/ST") == "patriots"

    def test_csv_format(self):
        """Test extraction from CSV format (City Team)"""
        assert extract_dst_team_name("Baltimore Ravens") == "ravens"
        assert extract_dst_team_name("San Francisco 49ers") == "49ers"
        assert extract_dst_team_name("New England Patriots") == "patriots"

    def test_case_insensitive(self):
        """Test that extraction is case-insensitive"""
        assert extract_dst_team_name("RAVENS D/ST") == "ravens"
        assert extract_dst_team_name("ravens d/st") == "ravens"

    def test_whitespace_handling(self):
        """Test that extra whitespace is handled"""
        assert extract_dst_team_name("Ravens  D/ST  ") == "ravens"
        assert extract_dst_team_name("  Baltimore Ravens  ") == "ravens"


class TestFindBestMatch:
    """Test the find_best_match() function"""

    @pytest.fixture
    def sample_csv_df(self):
        """Create sample CSV DataFrame for testing"""
        return pd.DataFrame({
            'player_name': ['Patrick Mahomes', 'Josh Allen', 'Lamar Jackson'],
            'adp': [15.5, 18.2, 22.1],
            'position': ['QB', 'QB', 'QB']
        })

    def test_finds_exact_match(self, sample_csv_df):
        """Test finding exact name match"""
        result = find_best_match("Patrick Mahomes", sample_csv_df, "QB")

        assert result is not None
        csv_name, adp, confidence = result
        assert csv_name == "Patrick Mahomes"
        assert adp == 15.5
        assert confidence == 1.0

    def test_finds_fuzzy_match(self, sample_csv_df):
        """Test finding fuzzy match with suffix"""
        result = find_best_match("Patrick Mahomes II", sample_csv_df, "QB")

        assert result is not None
        csv_name, adp, confidence = result
        assert csv_name == "Patrick Mahomes"
        assert confidence > 0.75

    def test_filters_by_position(self, sample_csv_df):
        """Test that position filtering works"""
        # Add RB player
        df = pd.concat([sample_csv_df, pd.DataFrame({
            'player_name': ['Christian McCaffrey'],
            'adp': [2.0],
            'position': ['RB']
        })], ignore_index=True)

        # Should not match QB to RB
        result = find_best_match("Christian McCaffrey", df, "QB")
        assert result is None  # No QB with that name

        # Should match RB to RB
        result = find_best_match("Christian McCaffrey", df, "RB")
        assert result is not None
        assert result[0] == "Christian McCaffrey"

    def test_returns_none_below_threshold(self, sample_csv_df):
        """Test that no match returned if confidence < 0.75"""
        result = find_best_match("Completely Different Name", sample_csv_df, "QB")
        assert result is None

    def test_matches_dst_with_different_formats(self):
        """Test DST matching with JSON (Ravens D/ST) and CSV (Baltimore Ravens) formats"""
        dst_df = pd.DataFrame({
            'player_name': ['Baltimore Ravens', 'San Francisco 49ers', 'Dallas Cowboys'],
            'adp': [120.7, 105.2, 110.5],
            'position': ['DST', 'DST', 'DST']
        })

        # JSON format should match CSV format
        result = find_best_match("Ravens D/ST", dst_df, "DST")
        assert result is not None
        csv_name, adp, confidence = result
        assert csv_name == "Baltimore Ravens"
        assert adp == 120.7
        assert confidence == 1.0  # Exact team name match

    def test_matches_dst_all_teams(self):
        """Test DST matching for multiple teams"""
        dst_df = pd.DataFrame({
            'player_name': ['Baltimore Ravens', 'San Francisco 49ers', 'New England Patriots'],
            'adp': [120.7, 105.2, 115.3],
            'position': ['DST', 'DST', 'DST']
        })

        # Test multiple DST teams
        test_cases = [
            ("Ravens D/ST", "Baltimore Ravens", 120.7),
            ("49ers D/ST", "San Francisco 49ers", 105.2),
            ("Patriots D/ST", "New England Patriots", 115.3)
        ]

        for json_name, expected_csv_name, expected_adp in test_cases:
            result = find_best_match(json_name, dst_df, "DST")
            assert result is not None, f"No match for {json_name}"
            csv_name, adp, confidence = result
            assert csv_name == expected_csv_name
            assert adp == expected_adp
            assert confidence == 1.0

    def test_dst_no_match_different_team(self):
        """Test that DST matching returns None for non-existent team"""
        dst_df = pd.DataFrame({
            'player_name': ['Baltimore Ravens'],
            'adp': [120.7],
            'position': ['DST']
        })

        result = find_best_match("Cowboys D/ST", dst_df, "DST")
        assert result is None


class TestUpdatePlayerAdpValues:
    """Test the update_player_adp_values() function"""

    @pytest.fixture
    def sample_adp_df(self):
        """Create sample ADP DataFrame"""
        return pd.DataFrame({
            'player_name': ['Patrick Mahomes', 'Josh Allen'],
            'adp': [15.5, 18.2],
            'position': ['QB', 'QB']
        })

    @pytest.fixture
    def test_sim_data_folder(self, tmp_path):
        """Create test simulation data folder with multi-week structure (direct arrays)"""
        sim_data_folder = tmp_path / 'simulation' / 'sim_data' / '2025' / 'weeks'

        # Create 3 test weeks (week_01, week_02, week_03)
        for week_num in range(1, 4):
            week_folder = sim_data_folder / f'week_{week_num:02d}'
            week_folder.mkdir(parents=True)

            # Create QB JSON file with direct array structure (no wrapper dict)
            qb_data = [
                {
                    'name': 'Patrick Mahomes II',
                    'position': 'QB',
                    'average_draft_position': 170.0,
                    'projected_points': 300.0
                },
                {
                    'name': 'Unmatched QB',
                    'position': 'QB',
                    'average_draft_position': 170.0,
                    'projected_points': 250.0
                }
            ]

            qb_path = week_folder / 'qb_data.json'
            with open(qb_path, 'w', encoding='utf-8') as f:
                json.dump(qb_data, f, indent=2)  # Direct array, no wrapper

            # Create empty files for other positions
            for pos_file in ['rb_data.json', 'wr_data.json', 'te_data.json', 'k_data.json', 'dst_data.json']:
                pos_path = week_folder / pos_file
                with open(pos_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)  # Direct empty array, no wrapper

        return sim_data_folder

    def test_matches_and_updates_players(self, sample_adp_df, test_sim_data_folder):
        """Test that players are matched and ADP values updated across all weeks"""
        # Act
        report = update_player_adp_values(sample_adp_df, test_sim_data_folder)

        # Assert - 3 weeks × 2 players per week = 6 total
        assert report['summary']['total_json_players'] == 6
        assert report['summary']['matched'] >= 3  # Patrick Mahomes in each week

        # Verify JSON file updated in first week (direct array structure)
        qb_path = test_sim_data_folder / 'week_01' / 'qb_data.json'
        with open(qb_path, 'r', encoding='utf-8') as f:
            qb_data = json.load(f)  # Direct array, not wrapped dict

        # Verify it's a direct array
        assert isinstance(qb_data, list)

        # Patrick Mahomes II should be matched and updated
        mahomes = [p for p in qb_data if 'Mahomes' in p['name']][0]
        assert mahomes['average_draft_position'] == 15.5  # Updated from 170.0

    def test_unmatched_players_keep_170(self, sample_adp_df, test_sim_data_folder):
        """Test that unmatched players keep 170.0 ADP value"""
        # Act
        report = update_player_adp_values(sample_adp_df, test_sim_data_folder)

        # Assert - "Unmatched QB" in each of 3 weeks
        assert len(report['unmatched_json_players']) >= 3

        # Verify JSON file - unmatched player keeps 170.0 (check week_01)
        qb_path = test_sim_data_folder / 'week_01' / 'qb_data.json'
        with open(qb_path, 'r', encoding='utf-8') as f:
            qb_data = json.load(f)  # Direct array

        unmatched = [p for p in qb_data if p['name'] == 'Unmatched QB'][0]
        assert unmatched['average_draft_position'] == 170.0  # Unchanged

    def test_returns_comprehensive_report(self, sample_adp_df, test_sim_data_folder):
        """Test that comprehensive match report is returned (aggregated across weeks)"""
        # Act
        report = update_player_adp_values(sample_adp_df, test_sim_data_folder)

        # Assert
        assert 'summary' in report
        assert 'unmatched_json_players' in report
        assert 'unmatched_csv_players' in report
        assert 'confidence_distribution' in report
        assert 'individual_matches' in report

        # Verify summary structure
        assert 'total_json_players' in report['summary']
        assert 'matched' in report['summary']
        assert 'unmatched_json' in report['summary']
        assert 'unmatched_csv' in report['summary']

    def test_raises_error_empty_dataframe(self, test_sim_data_folder):
        """Test that ValueError raised for empty DataFrame"""
        empty_df = pd.DataFrame()

        with pytest.raises(ValueError, match="ADP DataFrame is empty"):
            update_player_adp_values(empty_df, test_sim_data_folder)

    def test_raises_error_missing_columns(self, test_sim_data_folder):
        """Test that ValueError raised for missing columns"""
        bad_df = pd.DataFrame({'wrong_column': [1, 2, 3]})

        with pytest.raises(ValueError, match="DataFrame missing required columns"):
            update_player_adp_values(bad_df, test_sim_data_folder)

    def test_raises_error_missing_folder(self, sample_adp_df, tmp_path):
        """Test that FileNotFoundError raised for missing simulation folder"""
        nonexistent_folder = tmp_path / 'nonexistent'

        with pytest.raises(FileNotFoundError, match="Simulation data folder not found"):
            update_player_adp_values(sample_adp_df, nonexistent_folder)

    def test_atomic_write_creates_tmp_file(self, sample_adp_df, test_sim_data_folder):
        """Test that atomic write pattern is used across all weeks"""
        # Act
        report = update_player_adp_values(sample_adp_df, test_sim_data_folder)

        # Assert - after atomic write, tmp files should be cleaned up in all weeks
        for week_folder in test_sim_data_folder.glob('week_*'):
            tmp_files = list(week_folder.glob('*.tmp'))
            assert len(tmp_files) == 0  # Tmp files replaced

            # JSON files should exist and be valid (direct arrays)
            qb_path = week_folder / 'qb_data.json'
            assert qb_path.exists()

            # Should be able to load JSON as direct array (not corrupted)
            with open(qb_path, 'r', encoding='utf-8') as f:
                qb_data = json.load(f)
            assert isinstance(qb_data, list)  # Direct array, not wrapped dict

    def test_updates_all_week_folders(self, sample_adp_df, test_sim_data_folder):
        """Test that all week folders are processed and updated (Task 12)"""
        # Act
        report = update_player_adp_values(sample_adp_df, test_sim_data_folder)

        # Assert - verify all 3 weeks were processed
        for week_num in range(1, 4):
            week_folder = test_sim_data_folder / f'week_{week_num:02d}'
            qb_path = week_folder / 'qb_data.json'

            assert qb_path.exists()

            with open(qb_path, 'r', encoding='utf-8') as f:
                qb_data = json.load(f)

            # Verify direct array structure
            assert isinstance(qb_data, list)

            # Verify Patrick Mahomes was updated in this week
            mahomes = [p for p in qb_data if 'Mahomes' in p['name']][0]
            assert mahomes['average_draft_position'] == 15.5

    def test_consistent_updates_across_weeks(self, sample_adp_df, test_sim_data_folder):
        """Test that same player gets same ADP value in all weeks (Task 13)"""
        # Act
        report = update_player_adp_values(sample_adp_df, test_sim_data_folder)

        # Collect Patrick Mahomes ADP from all weeks
        mahomes_adp_values = []
        for week_num in range(1, 4):
            week_folder = test_sim_data_folder / f'week_{week_num:02d}'
            qb_path = week_folder / 'qb_data.json'

            with open(qb_path, 'r', encoding='utf-8') as f:
                qb_data = json.load(f)

            mahomes = [p for p in qb_data if 'Mahomes' in p['name']][0]
            mahomes_adp_values.append(mahomes['average_draft_position'])

        # Assert - all weeks should have same ADP value
        assert len(set(mahomes_adp_values)) == 1  # All values are identical
        assert mahomes_adp_values[0] == 15.5  # Correct value
