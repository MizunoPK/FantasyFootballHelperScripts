#!/usr/bin/env python3
"""
Unit tests for ParameterJsonManager

Tests parameter loading, validation, error handling, and access patterns.

Author: Kai Mizuno
Last Updated: October 2025
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from shared_files.parameter_json_manager import ParameterJsonManager


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def valid_parameters_dict():
    """Valid parameter dictionary with nested INJURY_PENALTIES structure."""
    return {
        'ADP_EXCELLENT_MULTIPLIER': 1.18,
        'ADP_GOOD_MULTIPLIER': 1.08,
        'ADP_POOR_MULTIPLIER': 0.52,
        'BASE_BYE_PENALTY': 28.85,
        'DRAFT_ORDER_PRIMARY_BONUS': 74.76,
        'DRAFT_ORDER_SECONDARY_BONUS': 38.57,
        'INJURY_PENALTIES': {
            'LOW': 0,
            'MEDIUM': 4.68,
            'HIGH': 78.22
        },
        'MATCHUP_EXCELLENT_MULTIPLIER': 1.23,
        'MATCHUP_GOOD_MULTIPLIER': 1.03,
        'MATCHUP_NEUTRAL_MULTIPLIER': 1.0,
        'MATCHUP_POOR_MULTIPLIER': 0.92,
        'MATCHUP_VERY_POOR_MULTIPLIER': 0.5,
        'NORMALIZATION_MAX_SCALE': 102.42,
        'PLAYER_RATING_EXCELLENT_MULTIPLIER': 1.21,
        'PLAYER_RATING_GOOD_MULTIPLIER': 1.15,
        'PLAYER_RATING_POOR_MULTIPLIER': 0.94,
        'TEAM_EXCELLENT_MULTIPLIER': 1.12,
        'TEAM_GOOD_MULTIPLIER': 1.32,
        'TEAM_POOR_MULTIPLIER': 0.64,
        'CONSISTENCY_LOW_MULTIPLIER': 1.08,
        'CONSISTENCY_MEDIUM_MULTIPLIER': 1.00,
        'CONSISTENCY_HIGH_MULTIPLIER': 0.92
    }


@pytest.fixture
def valid_json_data(valid_parameters_dict):
    """Valid complete JSON structure."""
    return {
        'config_name': 'test_config',
        'description': 'Test configuration for unit tests',
        'parameters': valid_parameters_dict
    }


@pytest.fixture
def temp_json_file(valid_json_data):
    """Create a temporary JSON file with valid data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name
    yield temp_path
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


# ============================================================================
# Basic Loading Tests
# ============================================================================

def test_load_valid_json_file(temp_json_file):
    """Test loading a valid JSON file."""
    with patch('sys.exit'):  # Prevent actual exit in tests
        manager = ParameterJsonManager(temp_json_file)

    assert manager.config_name == 'test_config'
    assert manager.description == 'Test configuration for unit tests'
    assert len(manager.parameters) == 22  # 22 parameters (INJURY_PENALTIES counts as 1 nested dict)


def test_file_not_found():
    """Test error handling when JSON file doesn't exist."""
    with pytest.raises(SystemExit) as exc_info:
        ParameterJsonManager('/nonexistent/path/parameters.json')

    assert exc_info.value.code == 1


def test_invalid_json_format():
    """Test error handling for malformed JSON."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{ invalid json content }')
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_missing_parameters_section():
    """Test error when 'parameters' section is missing."""
    data = {
        'config_name': 'test',
        'description': 'Missing parameters section'
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


# ============================================================================
# Parameter Access Tests
# ============================================================================

def test_dict_style_access(temp_json_file):
    """Test accessing parameters using dict-style get()."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    assert manager.get('ADP_EXCELLENT_MULTIPLIER') == 1.18
    assert manager.get('NONEXISTENT_PARAM', 'default') == 'default'


def test_bracket_notation_access(temp_json_file):
    """Test accessing parameters using bracket notation."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    assert manager['BASE_BYE_PENALTY'] == 28.85
    assert manager['INJURY_PENALTIES']['LOW'] == 0
    assert manager['INJURY_PENALTIES']['MEDIUM'] == 4.68
    assert manager['INJURY_PENALTIES']['HIGH'] == 78.22


def test_bracket_notation_keyerror(temp_json_file):
    """Test KeyError when accessing non-existent parameter with bracket notation."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    with pytest.raises(KeyError):
        _ = manager['NONEXISTENT_PARAM']


def test_attribute_style_access(temp_json_file):
    """Test accessing parameters using attribute notation."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    assert manager.ADP_EXCELLENT_MULTIPLIER == 1.18
    assert manager.NORMALIZATION_MAX_SCALE == 102.42


def test_attribute_style_error(temp_json_file):
    """Test AttributeError when accessing non-existent parameter."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    with pytest.raises(AttributeError):
        _ = manager.NONEXISTENT_PARAM


def test_contains_operator(temp_json_file):
    """Test 'in' operator for checking parameter existence."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    assert 'ADP_EXCELLENT_MULTIPLIER' in manager
    assert 'INJURY_PENALTIES' in manager
    assert 'NONEXISTENT_PARAM' not in manager


def test_get_all_parameters(temp_json_file):
    """Test getting all parameters as dictionary."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    all_params = manager.get_all_parameters()
    assert len(all_params) == 22  # 22 parameters (INJURY_PENALTIES counts as 1 nested dict)
    assert 'ADP_EXCELLENT_MULTIPLIER' in all_params
    assert isinstance(all_params['INJURY_PENALTIES'], dict)


def test_get_metadata(temp_json_file):
    """Test getting configuration metadata."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    metadata = manager.get_metadata()
    assert metadata['config_name'] == 'test_config'
    assert metadata['description'] == 'Test configuration for unit tests'
    assert 'file_path' in metadata


# ============================================================================
# Validation Tests - Missing Parameters
# ============================================================================

def test_missing_required_parameter(valid_json_data):
    """Test error when required parameter is missing."""
    # Remove a required parameter
    del valid_json_data['parameters']['ADP_EXCELLENT_MULTIPLIER']

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_missing_multiple_parameters(valid_json_data):
    """Test error when multiple required parameters are missing."""
    # Remove multiple parameters
    del valid_json_data['parameters']['ADP_EXCELLENT_MULTIPLIER']
    del valid_json_data['parameters']['BASE_BYE_PENALTY']
    del valid_json_data['parameters']['NORMALIZATION_MAX_SCALE']

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


# ============================================================================
# Validation Tests - INJURY_PENALTIES Structure
# ============================================================================

def test_injury_penalties_not_nested(valid_json_data):
    """Test error when INJURY_PENALTIES is not a nested dict."""
    valid_json_data['parameters']['INJURY_PENALTIES'] = 50  # Wrong type

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_injury_penalties_missing_key(valid_json_data):
    """Test error when INJURY_PENALTIES is missing required key."""
    # Remove MEDIUM key
    del valid_json_data['parameters']['INJURY_PENALTIES']['MEDIUM']

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_injury_penalties_valid_structure(temp_json_file):
    """Test that nested INJURY_PENALTIES structure is loaded correctly."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    injury_penalties = manager.INJURY_PENALTIES
    assert isinstance(injury_penalties, dict)
    assert 'LOW' in injury_penalties
    assert 'MEDIUM' in injury_penalties
    assert 'HIGH' in injury_penalties
    assert injury_penalties['LOW'] == 0
    assert injury_penalties['MEDIUM'] == 4.68
    assert injury_penalties['HIGH'] == 78.22


# ============================================================================
# Validation Tests - Value Ranges
# ============================================================================

def test_multiplier_out_of_range_high(valid_json_data):
    """Test error when multiplier exceeds maximum value."""
    valid_json_data['parameters']['ADP_EXCELLENT_MULTIPLIER'] = 3.0  # Too high

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_multiplier_out_of_range_low(valid_json_data):
    """Test error when multiplier is below minimum value."""
    valid_json_data['parameters']['TEAM_POOR_MULTIPLIER'] = -0.5  # Too low

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_penalty_out_of_range(valid_json_data):
    """Test error when penalty exceeds maximum value."""
    valid_json_data['parameters']['BASE_BYE_PENALTY'] = 250  # Too high

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_bonus_out_of_range(valid_json_data):
    """Test error when bonus exceeds maximum value."""
    valid_json_data['parameters']['DRAFT_ORDER_PRIMARY_BONUS'] = 150  # Too high

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_normalization_out_of_range(valid_json_data):
    """Test error when normalization scale is out of range."""
    valid_json_data['parameters']['NORMALIZATION_MAX_SCALE'] = 300  # Too high

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_injury_penalty_out_of_range(valid_json_data):
    """Test error when injury penalty value is out of range."""
    valid_json_data['parameters']['INJURY_PENALTIES']['HIGH'] = 300  # Too high

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with pytest.raises(SystemExit) as exc_info:
            ParameterJsonManager(temp_path)

        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink(missing_ok=True)


# ============================================================================
# Edge Case Tests
# ============================================================================

def test_all_parameters_present(temp_json_file):
    """Test that all 22 required parameters are loaded."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    expected_params = [
        'ADP_EXCELLENT_MULTIPLIER', 'ADP_GOOD_MULTIPLIER', 'ADP_POOR_MULTIPLIER',
        'BASE_BYE_PENALTY', 'DRAFT_ORDER_PRIMARY_BONUS', 'DRAFT_ORDER_SECONDARY_BONUS',
        'INJURY_PENALTIES', 'MATCHUP_EXCELLENT_MULTIPLIER', 'MATCHUP_GOOD_MULTIPLIER',
        'MATCHUP_NEUTRAL_MULTIPLIER', 'MATCHUP_POOR_MULTIPLIER', 'MATCHUP_VERY_POOR_MULTIPLIER',
        'NORMALIZATION_MAX_SCALE', 'PLAYER_RATING_EXCELLENT_MULTIPLIER',
        'PLAYER_RATING_GOOD_MULTIPLIER', 'PLAYER_RATING_POOR_MULTIPLIER',
        'TEAM_EXCELLENT_MULTIPLIER', 'TEAM_GOOD_MULTIPLIER', 'TEAM_POOR_MULTIPLIER',
        'CONSISTENCY_LOW_MULTIPLIER', 'CONSISTENCY_MEDIUM_MULTIPLIER', 'CONSISTENCY_HIGH_MULTIPLIER'
    ]

    # Should have exactly 22 parameters
    assert len(expected_params) == 22
    for param in expected_params:
        assert param in manager.parameters


def test_edge_values_valid(valid_json_data):
    """Test that edge values (boundaries) are accepted."""
    # Set parameters to boundary values
    valid_json_data['parameters']['ADP_EXCELLENT_MULTIPLIER'] = 0.0  # Min
    valid_json_data['parameters']['TEAM_EXCELLENT_MULTIPLIER'] = 2.0  # Max
    valid_json_data['parameters']['BASE_BYE_PENALTY'] = 0  # Min penalty
    valid_json_data['parameters']['NORMALIZATION_MAX_SCALE'] = 50  # Min scale

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_json_data, f)
        temp_path = f.name

    try:
        with patch('sys.exit'):
            manager = ParameterJsonManager(temp_path)

        assert manager.ADP_EXCELLENT_MULTIPLIER == 0.0
        assert manager.TEAM_EXCELLENT_MULTIPLIER == 2.0
        assert manager.BASE_BYE_PENALTY == 0
        assert manager.NORMALIZATION_MAX_SCALE == 50
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_repr_and_str(temp_json_file):
    """Test string representations."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    repr_str = repr(manager)
    assert 'test_config' in repr_str
    assert 'ParameterJsonManager' in repr_str

    str_str = str(manager)
    assert 'test_config' in str_str
    assert '22 parameters' in str_str


def test_missing_metadata_fields(valid_parameters_dict):
    """Test handling when metadata fields are missing."""
    data = {
        'parameters': valid_parameters_dict
        # Missing config_name and description
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name

    try:
        with patch('sys.exit'):
            manager = ParameterJsonManager(temp_path)

        assert manager.config_name == 'unknown'
        assert manager.description == ''
    finally:
        Path(temp_path).unlink(missing_ok=True)


# ============================================================================
# Integration Tests
# ============================================================================

def test_load_actual_shared_parameters_file():
    """Test loading the actual shared_files/parameters.json file if it exists."""
    params_path = Path(__file__).parent.parent / 'parameters.json'

    if params_path.exists():
        with patch('sys.exit'):
            manager = ParameterJsonManager(str(params_path))

        # Verify it loaded successfully
        assert len(manager.parameters) >= 22  # At least 22 parameters
        assert 'INJURY_PENALTIES' in manager
        assert isinstance(manager.INJURY_PENALTIES, dict)
    else:
        pytest.skip("Shared parameters.json file not found")


def test_immutability_of_returned_dict(temp_json_file):
    """Test that modifying returned parameter dict doesn't affect original."""
    with patch('sys.exit'):
        manager = ParameterJsonManager(temp_json_file)

    # Get parameters and modify
    params = manager.get_all_parameters()
    original_value = params['ADP_EXCELLENT_MULTIPLIER']
    params['ADP_EXCELLENT_MULTIPLIER'] = 999

    # Verify original is unchanged
    assert manager.ADP_EXCELLENT_MULTIPLIER == original_value
    assert manager.ADP_EXCELLENT_MULTIPLIER != 999
