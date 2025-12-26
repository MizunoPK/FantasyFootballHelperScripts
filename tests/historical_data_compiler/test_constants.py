#!/usr/bin/env python3
"""
Tests for historical_data_compiler/constants.py

Tests constant values and mappings used for ESPN API interactions.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.constants import (
    ESPN_TEAM_MAPPINGS,
    ESPN_POSITION_MAPPINGS,
    ALL_NFL_TEAMS,
    FANTASY_POSITIONS,
    REGULAR_SEASON_WEEKS,
    MIN_SUPPORTED_YEAR,
    POSITION_JSON_FILES,
    QB_DATA_FILE,
    RB_DATA_FILE,
    WR_DATA_FILE,
    TE_DATA_FILE,
    K_DATA_FILE,
    DST_DATA_FILE,
    normalize_team_abbrev,
)


class TestESPNTeamMappings:
    """Tests for ESPN team ID to abbreviation mappings"""

    def test_all_32_teams_mapped(self):
        """All 32 NFL teams should be mapped"""
        assert len(ESPN_TEAM_MAPPINGS) == 32

    def test_known_team_mappings(self):
        """Verify specific known team mappings"""
        assert ESPN_TEAM_MAPPINGS[12] == 'KC'  # Kansas City Chiefs
        assert ESPN_TEAM_MAPPINGS[33] == 'BAL'  # Baltimore Ravens
        assert ESPN_TEAM_MAPPINGS[1] == 'ATL'  # Atlanta Falcons
        assert ESPN_TEAM_MAPPINGS[28] == 'WSH'  # Washington Commanders

    def test_all_values_are_three_letter_codes(self):
        """All team abbreviations should be 2-3 characters"""
        for team in ESPN_TEAM_MAPPINGS.values():
            assert 2 <= len(team) <= 3


class TestESPNPositionMappings:
    """Tests for ESPN position ID to name mappings"""

    def test_six_fantasy_positions_mapped(self):
        """Six fantasy-relevant positions should be mapped"""
        assert len(ESPN_POSITION_MAPPINGS) == 6

    def test_known_position_mappings(self):
        """Verify specific known position mappings"""
        assert ESPN_POSITION_MAPPINGS[1] == 'QB'
        assert ESPN_POSITION_MAPPINGS[2] == 'RB'
        assert ESPN_POSITION_MAPPINGS[3] == 'WR'
        assert ESPN_POSITION_MAPPINGS[4] == 'TE'
        assert ESPN_POSITION_MAPPINGS[5] == 'K'
        assert ESPN_POSITION_MAPPINGS[16] == 'DST'


class TestAllNFLTeams:
    """Tests for ALL_NFL_TEAMS list"""

    def test_all_32_teams_listed(self):
        """Should contain all 32 NFL teams"""
        assert len(ALL_NFL_TEAMS) == 32

    def test_teams_are_sorted(self):
        """Teams should be in alphabetical order"""
        assert ALL_NFL_TEAMS == sorted(ALL_NFL_TEAMS)

    def test_specific_teams_present(self):
        """Known teams should be present"""
        assert 'KC' in ALL_NFL_TEAMS
        assert 'WSH' in ALL_NFL_TEAMS
        assert 'SF' in ALL_NFL_TEAMS

    def test_no_duplicates(self):
        """No duplicate team entries"""
        assert len(ALL_NFL_TEAMS) == len(set(ALL_NFL_TEAMS))


class TestFantasyPositions:
    """Tests for FANTASY_POSITIONS list"""

    def test_six_positions(self):
        """Should have 6 fantasy positions"""
        assert len(FANTASY_POSITIONS) == 6

    def test_all_positions_present(self):
        """All standard fantasy positions should be present"""
        expected = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        for pos in expected:
            assert pos in FANTASY_POSITIONS


class TestSeasonConfiguration:
    """Tests for season configuration constants"""

    def test_regular_season_weeks(self):
        """Regular season should be 17 weeks"""
        assert REGULAR_SEASON_WEEKS == 17

    def test_min_supported_year(self):
        """Minimum supported year should be 2021"""
        assert MIN_SUPPORTED_YEAR == 2021


class TestNormalizeTeamAbbrev:
    """Tests for normalize_team_abbrev function"""

    def test_washington_normalization(self):
        """WAS should normalize to WSH"""
        assert normalize_team_abbrev('WAS') == 'WSH'

    def test_other_teams_unchanged(self):
        """Other team abbreviations should remain unchanged"""
        assert normalize_team_abbrev('KC') == 'KC'
        assert normalize_team_abbrev('SF') == 'SF'
        assert normalize_team_abbrev('WSH') == 'WSH'

    def test_empty_string(self):
        """Empty string should remain empty"""
        assert normalize_team_abbrev('') == ''


class TestJSONFileConstants:
    """Tests for JSON file name constants"""

    def test_individual_json_file_constants(self):
        """Individual JSON file constants should have correct values"""
        assert QB_DATA_FILE == 'qb_data.json'
        assert RB_DATA_FILE == 'rb_data.json'
        assert WR_DATA_FILE == 'wr_data.json'
        assert TE_DATA_FILE == 'te_data.json'
        assert K_DATA_FILE == 'k_data.json'
        assert DST_DATA_FILE == 'dst_data.json'

    def test_position_json_files_has_six_positions(self):
        """POSITION_JSON_FILES should have all 6 fantasy positions"""
        assert len(POSITION_JSON_FILES) == 6

    def test_position_json_files_keys(self):
        """POSITION_JSON_FILES should have correct position keys"""
        expected_positions = {'QB', 'RB', 'WR', 'TE', 'K', 'DST'}
        assert set(POSITION_JSON_FILES.keys()) == expected_positions

    def test_position_json_files_values(self):
        """POSITION_JSON_FILES should map to correct filenames"""
        assert POSITION_JSON_FILES['QB'] == 'qb_data.json'
        assert POSITION_JSON_FILES['RB'] == 'rb_data.json'
        assert POSITION_JSON_FILES['WR'] == 'wr_data.json'
        assert POSITION_JSON_FILES['TE'] == 'te_data.json'
        assert POSITION_JSON_FILES['K'] == 'k_data.json'
        assert POSITION_JSON_FILES['DST'] == 'dst_data.json'

    def test_all_json_files_have_json_extension(self):
        """All JSON file constants should end with .json"""
        for filename in POSITION_JSON_FILES.values():
            assert filename.endswith('.json')

    def test_json_filenames_lowercase(self):
        """JSON filenames should be lowercase"""
        for filename in POSITION_JSON_FILES.values():
            assert filename == filename.lower()

    def test_position_json_files_matches_fantasy_positions(self):
        """POSITION_JSON_FILES keys should match FANTASY_POSITIONS"""
        assert set(POSITION_JSON_FILES.keys()) == set(FANTASY_POSITIONS)
