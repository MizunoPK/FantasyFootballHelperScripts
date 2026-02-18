#!/usr/bin/env python3
"""
Tests for TeamData module.

Comprehensive tests for TeamData class, conversion helpers, and
team data extraction functions.

Author: Kai Mizuno
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from utils.TeamData import (
    TeamData,
    _safe_int_conversion,
    _safe_string_conversion,
    load_team_weekly_data,
    save_team_weekly_data,
    load_single_team_data,
    save_single_team_data,
    NFL_TEAMS
)

class TestTeamDataInit:
    """Test suite for TeamData initialization."""

    def test_team_data_initialization_minimal(self):
        """Test TeamData initializes with just team name."""
        team = TeamData(team='KC')

        assert team.team == 'KC'
        assert team.offensive_rank is None
        assert team.defensive_rank is None

    def test_team_data_initialization_complete(self):
        """Test TeamData initializes with all fields."""
        team = TeamData(
            team='PHI',
            offensive_rank=5,
            defensive_rank=12
        )

        assert team.team == 'PHI'
        assert team.offensive_rank == 5
        assert team.defensive_rank == 12


class TestTeamDataFromDict:
    """Test suite for TeamData.from_dict() method."""

    def test_from_dict_complete_data(self):
        """Test from_dict() with all fields present."""
        data = {
            'team': 'BUF',
            'offensive_rank': 3,
            'defensive_rank': 8
        }

        team = TeamData.from_dict(data)

        assert team.team == 'BUF'
        assert team.offensive_rank == 3
        assert team.defensive_rank == 8

    def test_from_dict_missing_optional_fields(self):
        """Test from_dict() with only team field."""
        data = {'team': 'KC'}

        team = TeamData.from_dict(data)

        assert team.team == 'KC'
        assert team.offensive_rank is None
        assert team.defensive_rank is None

    def test_from_dict_handles_string_ranks(self):
        """Test from_dict() converts string ranks to int."""
        data = {
            'team': 'SF',
            'offensive_rank': '10',
            'defensive_rank': '15'
        }

        team = TeamData.from_dict(data)

        assert team.offensive_rank == 10
        assert team.defensive_rank == 15

    def test_from_dict_handles_nan_values(self):
        """Test from_dict() converts NaN to None."""
        data = {
            'team': 'NE',
            'offensive_rank': 'nan',
            'defensive_rank': float('nan')
        }

        team = TeamData.from_dict(data)

        assert team.offensive_rank is None
        assert team.defensive_rank is None

    def test_from_dict_empty_team(self):
        """Test from_dict() with empty team field."""
        data = {}

        team = TeamData.from_dict(data)

        assert team.team == ''


class TestTeamDataToDict:
    """Test suite for TeamData.to_dict() method."""

    def test_to_dict_complete_data(self):
        """Test to_dict() with all fields populated."""
        team = TeamData(
            team='DAL',
            offensive_rank=7,
            defensive_rank=20,
            def_vs_qb_rank=5,
            def_vs_rb_rank=12,
            def_vs_wr_rank=8,
            def_vs_te_rank=15,
            def_vs_k_rank=20
        )

        result = team.to_dict()

        assert result == {
            'team': 'DAL',
            'offensive_rank': 7,
            'defensive_rank': 20,
            'def_vs_qb_rank': 5,
            'def_vs_rb_rank': 12,
            'def_vs_wr_rank': 8,
            'def_vs_te_rank': 15,
            'def_vs_k_rank': 20
        }

    def test_to_dict_partial_data(self):
        """Test to_dict() with some None fields."""
        team = TeamData(team='GB', offensive_rank=4)

        result = team.to_dict()

        assert result['team'] == 'GB'
        assert result['offensive_rank'] == 4
        assert result['defensive_rank'] is None


class TestSafeIntConversion:
    """Test suite for _safe_int_conversion() helper."""

    def test_safe_int_conversion_valid_int(self):
        """Test converts valid integer."""
        assert _safe_int_conversion(5) == 5
        assert _safe_int_conversion(0) == 0
        assert _safe_int_conversion(-10) == -10

    def test_safe_int_conversion_valid_string(self):
        """Test converts valid string to int."""
        assert _safe_int_conversion('15') == 15
        assert _safe_int_conversion('0') == 0

    def test_safe_int_conversion_float(self):
        """Test converts float to int."""
        assert _safe_int_conversion(12.7) == 12
        assert _safe_int_conversion(9.1) == 9

    def test_safe_int_conversion_float_string(self):
        """Test converts string representation of float."""
        assert _safe_int_conversion('12.7') == 12
        assert _safe_int_conversion('9.1') == 9

    def test_safe_int_conversion_none(self):
        """Test returns default for None."""
        assert _safe_int_conversion(None) is None
        assert _safe_int_conversion(None, default=0) == 0

    def test_safe_int_conversion_empty_string(self):
        """Test returns default for empty string."""
        assert _safe_int_conversion('') is None
        assert _safe_int_conversion('', default=-1) == -1

    def test_safe_int_conversion_nan_string(self):
        """Test returns default for 'nan' string."""
        assert _safe_int_conversion('nan') is None
        assert _safe_int_conversion('NaN', default=0) == 0
        assert _safe_int_conversion('none') is None
        assert _safe_int_conversion('null') is None

    def test_safe_int_conversion_infinity(self):
        """Test returns default for infinity values."""
        assert _safe_int_conversion(float('inf')) is None
        assert _safe_int_conversion(float('-inf')) is None

    def test_safe_int_conversion_actual_nan(self):
        """Test returns default for actual NaN."""
        assert _safe_int_conversion(float('nan')) is None

    def test_safe_int_conversion_invalid_string(self):
        """Test returns default for non-numeric string."""
        assert _safe_int_conversion('abc') is None
        # Note: '12abc' extracts the '12' digits, so it returns 12 not default
        assert _safe_int_conversion('12abc', default=0) == 12

    def test_safe_int_conversion_string_with_extras(self):
        """Test handles string with non-numeric characters."""
        assert _safe_int_conversion('$15') == 15
        assert _safe_int_conversion('rank: 10') == 10


class TestSafeStringConversion:
    """Test suite for _safe_string_conversion() helper."""

    def test_safe_string_conversion_valid_string(self):
        """Test returns valid string unchanged."""
        assert _safe_string_conversion('KC') == 'KC'
        assert _safe_string_conversion('BUF') == 'BUF'

    def test_safe_string_conversion_none(self):
        """Test returns None for None."""
        assert _safe_string_conversion(None) is None

    def test_safe_string_conversion_nan_string(self):
        """Test returns None for 'nan' strings."""
        assert _safe_string_conversion('nan') is None
        assert _safe_string_conversion('NaN') is None
        assert _safe_string_conversion('none') is None
        assert _safe_string_conversion('null') is None

    def test_safe_string_conversion_empty_string(self):
        """Test returns None for empty string."""
        assert _safe_string_conversion('') is None
        assert _safe_string_conversion('   ') is None

    def test_safe_string_conversion_pandas_nan(self):
        """Test handles pandas NaN values."""
        assert _safe_string_conversion(pd.NA) is None
        assert _safe_string_conversion(float('nan')) is None

    def test_safe_string_conversion_numeric(self):
        """Test converts numeric values to string."""
        assert _safe_string_conversion(123) == '123'
        assert _safe_string_conversion(12.5) == '12.5'

    def test_safe_string_conversion_strips_whitespace(self):
        """Test strips leading/trailing whitespace."""
        assert _safe_string_conversion('  PHI  ') == 'PHI'


