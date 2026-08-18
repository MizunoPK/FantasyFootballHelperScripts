"""
Unit Tests for the Shared Base Config Parameter Filter

Covers simulation/shared/config_filters.extract_base_params - the single
"filter a config dict to BASE_CONFIG_PARAMS" body in the repo (T90 D3), shared by
the win-rate path (ResultsManager._extract_base_params) and both accuracy promote
call sites (save_optimal_configs, propagate_to_configs).

Author: Kai Mizuno
"""

# Standard library
import copy

# Local
from simulation.shared.config_constants import BASE_CONFIG_PARAMS, WEEK_SPECIFIC_PARAMS
from simulation.shared.config_filters import extract_base_params


_BASE_DESCRIPTION = 'Base configuration (non-week-specific parameters)'


class TestD178EspnKeysAreBaseParams:
    """D17.8 G1, second half: BASE_CONFIG_PARAMS membership needs its own guard.

    Review CONCERN-2: the unit mutation-verified only the PRESERVE_KEYS half.
    Removing the ESPN keys from BASE_CONFIG_PARAMS turned NO green test red --
    that half of the fix had no regression guard at all, and the only signal was
    an already-red shape assertion widening by two entries, which is exactly the
    kind of change seven prior units read past.

    This asserts the BEHAVIOUR (extract_base_params emits the keys), not the
    membership, so it fails for the reason that matters rather than restating the
    list back to itself.
    """

    def test_extract_base_params_emits_the_espn_league_identity(self):
        from simulation.shared.config_filters import extract_base_params
        out = extract_base_params({'parameters': {
            'ESPN_LEAGUE_ID': '138260302',
            'ESPN_TEAM_ID': 1,
            'CURRENT_NFL_WEEK': 3,
        }})
        params = out['parameters']
        assert params.get('ESPN_LEAGUE_ID') == '138260302', (
            "ESPN_LEAGUE_ID must survive base-param extraction; dropping it here is "
            "what let an accuracy promote delete the user's league identity"
        )
        assert params.get('ESPN_TEAM_ID') == 1


class TestExtractBaseParams:
    """Unit coverage of the shared BASE_CONFIG_PARAMS filter (T90 D3)."""

    def test_week_owned_keys_are_dropped(self):
        """Every WEEK_SPECIFIC_PARAMS member is filtered out of the result."""
        # Arrange
        params = {'ADP_SCORING': {'WEIGHT': 1.5}}
        params.update({key: {'WEIGHT': 1.0} for key in WEEK_SPECIFIC_PARAMS})

        # Act
        result = extract_base_params({'parameters': params})['parameters']

        # Assert
        assert set(result) & set(WEEK_SPECIFIC_PARAMS) == set(), (
            f"week-owned keys survived the filter: "
            f"{sorted(set(result) & set(WEEK_SPECIFIC_PARAMS))}"
        )

    def test_keys_in_neither_ownership_list_are_dropped(self):
        """An unrecognized key is not base-owned, so it is filtered out."""
        # Arrange
        params = {'ADP_SCORING': 1, 'NOT_A_REAL_PARAM': 2, 'SCORING_WEIGHT': 3}

        # Act
        result = extract_base_params({'parameters': params})['parameters']

        # Assert
        assert set(result) <= set(BASE_CONFIG_PARAMS), (
            f"non-base keys survived the filter: "
            f"{sorted(set(result) - set(BASE_CONFIG_PARAMS))}"
        )
        assert set(result) == {'ADP_SCORING'}

    def test_every_base_key_present_is_retained_with_its_value_unchanged(self):
        """No base-owned key is dropped, and no retained value is altered."""
        # Arrange
        params = {key: {'marker': index} for index, key in enumerate(BASE_CONFIG_PARAMS)}

        # Act
        result = extract_base_params({'parameters': params})['parameters']

        # Assert
        assert set(result) == set(BASE_CONFIG_PARAMS), (
            f"base-owned keys were dropped: {sorted(set(BASE_CONFIG_PARAMS) - set(result))}"
        )
        assert result == params, "retained parameter values must be unchanged"

    def test_retained_keys_follow_base_config_params_order(self):
        """The result's key order is BASE_CONFIG_PARAMS order, as the docstring promises."""
        # Arrange
        params = {'PLAYER_RATING_SCORING': 1, 'ADP_SCORING': 2, 'NFL_SEASON': 3}

        # Act
        result = extract_base_params({'parameters': params})['parameters']

        # Assert
        assert list(result) == [key for key in BASE_CONFIG_PARAMS if key in params]

    def test_missing_parameters_block_yields_an_empty_parameter_set(self):
        """A config dict with no 'parameters' key is treated as an empty parameter block."""
        # Arrange
        config = {'config_name': 'No Params'}

        # Act
        result = extract_base_params(config)

        # Assert
        assert result['parameters'] == {}

    def test_config_name_is_preserved_when_present(self):
        """The source's config_name rides through unchanged."""
        # Arrange
        config = {'config_name': 'Inflated Baseline', 'parameters': {'ADP_SCORING': 1}}

        # Act
        result = extract_base_params(config)

        # Assert
        assert result['config_name'] == 'Inflated Baseline'

    def test_config_name_falls_back_to_the_default_when_absent(self):
        """A source with no config_name gets the documented default label."""
        # Arrange
        config = {'parameters': {'ADP_SCORING': 1}}

        # Act
        result = extract_base_params(config)

        # Assert
        assert result['config_name'] == 'Optimal Base Config'

    def test_return_shape_is_exactly_the_three_documented_keys(self):
        """The result carries config_name, description and parameters - nothing else."""
        # Arrange
        config = {
            'config_name': 'X',
            'description': 'the source description',
            'performance_metrics': {'mae': 1.23},
            'parameters': {'ADP_SCORING': 1},
        }

        # Act
        result = extract_base_params(config)

        # Assert
        assert set(result) == {'config_name', 'description', 'parameters'}
        assert result['description'] == _BASE_DESCRIPTION, (
            "the helper always emits the base-config description label"
        )

    def test_the_input_config_dict_is_not_mutated(self):
        """The caller's dict survives the call untouched.

        propagate_to_configs spreads the helper's 'parameters' over the SOURCE dict,
        so a helper that mutated its input would corrupt that spread.
        """
        # Arrange
        config = {
            'config_name': 'X',
            'parameters': {'ADP_SCORING': 1, 'WIND_SCORING': 2, 'NOT_A_REAL_PARAM': 3},
        }
        before = copy.deepcopy(config)

        # Act
        extract_base_params(config)

        # Assert
        assert config == before, "extract_base_params must not mutate its argument"
