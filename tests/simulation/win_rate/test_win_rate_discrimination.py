"""
Controlled-landscape tests for win-rate discrimination (measured-vs-incumbent).

Tests AC1 and AC2: proves that the sweep now measures discrimination (measured team's
performance relative to the incumbent), not just self-play symmetry, and that trial
configs stronger than the incumbent beat it while weaker ones lose.

Author: Kai Mizuno
"""

# Standard library
from unittest.mock import Mock, patch
from pathlib import Path

# Third-party
import pytest

# Local
from simulation.win_rate.CombinationEvaluator import CombinationEvaluator
from simulation.win_rate.param_value_generation import DRAFT_SWEEP_PARAMS
from simulation.shared.ConfigGenerator import ConfigGenerator


def _fake_params():
    """A league_config-like parameters dict (the 6 params nested + other keys)."""
    return {
        "CURRENT_NFL_WEEK": 17,
        "NFL_SEASON": 2025,
        "SAME_POS_BYE_WEIGHT": 0.07,
        "DIFF_POS_BYE_WEIGHT": 0.01,
        "DRAFT_ORDER_BONUSES": {"PRIMARY": 67, "SECONDARY": 69},
        "DRAFT_ORDER": [{"QB": "P"}],
        "MAX_POSITIONS": {"QB": 2},
        "ADP_SCORING": {"THRESHOLDS": {"STEPS": 25}, "WEIGHT": 4.76},
        "PLAYER_RATING_SCORING": {"THRESHOLDS": {"STEPS": 20}, "WEIGHT": 3.52},
        "DRAFT_NORMALIZATION_MAX_SCALE": 150,
    }


class FakeRunner:
    """
    A controlled-scoring runner for discrimination tests.

    Computes a deterministic "strength" scalar from a config's 6 draft-side params
    as the sum of normalized progress (v - min)/(max - min) toward each param's max.
    Returns simulations where the measured team's win fraction is deterministic based
    on strength(measured) - strength(incumbent).
    """

    def __init__(self):
        self.last_dropped_count = 0
        self.last_requested_count = 0

    def set_data_folder(self, data_folder):
        """Stub method for compatibility with ParallelLeagueRunner interface."""
        pass

    def run_simulations_for_config(self, config_dict, num_simulations, preloaded_week_data=None, measured_config_dict=None):
        """
        Return deterministic (wins, losses, points) tuples based on config strength.

        When measured_config_dict is None, treat it as equal to config_dict (symmetric).
        """
        # Update counters (KDD-1 compatibility)
        self.last_requested_count = num_simulations
        self.last_dropped_count = 0

        # Extract the 6 draft-side params from each config dict's parameters section
        measured_params = self._extract_params(measured_config_dict) if measured_config_dict is not None else self._extract_params(config_dict)
        incumbent_params = self._extract_params(config_dict)

        # Compute strength for each config (normalized progress toward max endpoint)
        measured_strength = self._compute_strength(measured_params)
        incumbent_strength = self._compute_strength(incumbent_params)

        # Determine win fraction: >0.5 if measured stronger, <0.5 if weaker, 0.5 if equal
        strength_diff = measured_strength - incumbent_strength
        if strength_diff > 0.001:  # Measured is materially stronger
            win_fraction = 0.75
        elif strength_diff < -0.001:  # Measured is materially weaker
            win_fraction = 0.25
        else:  # Measured equals incumbent (symmetric)
            win_fraction = 0.5

        # Distribute wins across simulations deterministically
        results = []
        for sim_id in range(num_simulations):
            if sim_id < num_simulations * win_fraction:
                wins, losses = 1, 0
            else:
                wins, losses = 0, 1
            points = 1500.0 + sim_id * 10  # Dummy points value
            results.append((wins, losses, points))

        return results

    def _extract_params(self, config_dict):
        """Extract the 6 draft-side params from a config dict."""
        if config_dict is None:
            return {}
        params = config_dict.get("parameters", {})
        # Extract only draft-side params (the 6 we're sweeping)
        return {k: v for k, v in params.items() if k in DRAFT_SWEEP_PARAMS}

    def _compute_strength(self, params):
        """
        Compute deterministic strength as sum of normalized progress toward max.

        Progress = (value - min) / (max - min) for each param.
        """
        if not params:
            return 0.5  # Default for empty params

        total_progress = 0.0
        param_defs = ConfigGenerator.PARAM_DEFINITIONS
        for param_name, value in params.items():
            if param_name in param_defs:
                min_val, max_val, _ = param_defs[param_name]
                if max_val > min_val:
                    progress = (value - min_val) / (max_val - min_val)
                    total_progress += progress

        # Return average progress (0–1 range for typical in-bounds params)
        return total_progress / len(params) if params else 0.5


class TestWinRateDiscrimination:
    """Test discrimination effect: swept params now affect the objective."""

    def test_param_change_moves_measured_win_rate(self, tmp_path):
        """
        AC1: Evaluate a trial whose params differ from the incumbent; assert
        the returned win_rate differs materially from symmetric ~0.50.
        """
        # Patch the expensive dependencies
        with patch('simulation.win_rate.CombinationEvaluator.ConfigManager') as mock_cm, \
             patch('simulation.win_rate.CombinationEvaluator.SimDataLoader') as mock_sdl, \
             patch('simulation.win_rate.CombinationEvaluator.ParallelLeagueRunner') as mock_plr_class:

            # Setup mocks
            mock_cm.return_value.config_name = "test_config"
            mock_cm.return_value.description = "Test"
            mock_cm.return_value.parameters = _fake_params()

            mock_sdl.return_value.is_valid = True
            mock_sdl.return_value.week_data_cache = {}

            # Inject FakeRunner
            mock_runner = FakeRunner()
            mock_plr_class.return_value = mock_runner

            # Create evaluator with a season folder
            season_folder = tmp_path / "2023"
            season_folder.mkdir()
            config_path = tmp_path / "configs" / "league_config.json"
            config_path.parent.mkdir(parents=True)

            evaluator = CombinationEvaluator(
                data_folder=tmp_path,
                num_simulations=10,
                config_path=config_path
            )

            draft_order = [1, 2, 3]

            # Trial params: weak set (all at min)
            weak_params = {
                param: ConfigGenerator.PARAM_DEFINITIONS[param][0]
                for param in DRAFT_SWEEP_PARAMS
            }

            # Incumbent params: strong set (all at max)
            strong_params = {
                param: ConfigGenerator.PARAM_DEFINITIONS[param][1]
                for param in DRAFT_SWEEP_PARAMS
            }

            # Evaluate weak trial against strong incumbent
            wins_weak, games_weak, wr_weak = evaluator.evaluate(
                draft_order, weak_params, incumbent_param_values=strong_params
            )

            # Evaluate strong trial against weak incumbent (should be higher)
            wins_strong, games_strong, wr_strong = evaluator.evaluate(
                draft_order, strong_params, incumbent_param_values=weak_params
            )

            # Both should differ materially from 0.5 (symmetric)
            assert abs(wr_weak - 0.5) > 0.05, f"Weak trial should have win_rate << 0.5, got {wr_weak}"
            assert abs(wr_strong - 0.5) > 0.05, f"Strong trial should have win_rate >> 0.5, got {wr_strong}"

            # Symmetric (incumbent omitted) should return ~0.5
            wins_sym, games_sym, wr_sym = evaluator.evaluate(draft_order, weak_params)
            assert abs(wr_sym - 0.5) < 0.1, f"Symmetric evaluation should have win_rate ~= 0.5, got {wr_sym}"

    def test_stronger_trial_beats_incumbent(self, tmp_path):
        """AC2: Materially stronger trial beats a weaker incumbent."""
        with patch('simulation.win_rate.CombinationEvaluator.ConfigManager') as mock_cm, \
             patch('simulation.win_rate.CombinationEvaluator.SimDataLoader') as mock_sdl, \
             patch('simulation.win_rate.CombinationEvaluator.ParallelLeagueRunner') as mock_plr_class:

            mock_cm.return_value.config_name = "test_config"
            mock_cm.return_value.description = "Test"
            mock_cm.return_value.parameters = _fake_params()

            mock_sdl.return_value.is_valid = True
            mock_sdl.return_value.week_data_cache = {}

            mock_runner = FakeRunner()
            mock_plr_class.return_value = mock_runner

            season_folder = tmp_path / "2023"
            season_folder.mkdir()
            config_path = tmp_path / "configs" / "league_config.json"
            config_path.parent.mkdir(parents=True)

            evaluator = CombinationEvaluator(
                data_folder=tmp_path,
                num_simulations=10,
                config_path=config_path
            )

            draft_order = [1, 2, 3]

            strong_trial = {
                param: ConfigGenerator.PARAM_DEFINITIONS[param][1]
                for param in DRAFT_SWEEP_PARAMS
            }
            weak_incumbent = {
                param: ConfigGenerator.PARAM_DEFINITIONS[param][0]
                for param in DRAFT_SWEEP_PARAMS
            }

            wins, games, win_rate = evaluator.evaluate(
                draft_order, strong_trial, incumbent_param_values=weak_incumbent
            )

            assert win_rate > 0.5, f"Stronger trial should beat weak incumbent, got win_rate {win_rate}"

    def test_weaker_trial_loses_to_incumbent(self, tmp_path):
        """AC2: Materially weaker trial loses to a stronger incumbent."""
        with patch('simulation.win_rate.CombinationEvaluator.ConfigManager') as mock_cm, \
             patch('simulation.win_rate.CombinationEvaluator.SimDataLoader') as mock_sdl, \
             patch('simulation.win_rate.CombinationEvaluator.ParallelLeagueRunner') as mock_plr_class:

            mock_cm.return_value.config_name = "test_config"
            mock_cm.return_value.description = "Test"
            mock_cm.return_value.parameters = _fake_params()

            mock_sdl.return_value.is_valid = True
            mock_sdl.return_value.week_data_cache = {}

            mock_runner = FakeRunner()
            mock_plr_class.return_value = mock_runner

            season_folder = tmp_path / "2023"
            season_folder.mkdir()
            config_path = tmp_path / "configs" / "league_config.json"
            config_path.parent.mkdir(parents=True)

            evaluator = CombinationEvaluator(
                data_folder=tmp_path,
                num_simulations=10,
                config_path=config_path
            )

            draft_order = [1, 2, 3]

            weak_trial = {
                param: ConfigGenerator.PARAM_DEFINITIONS[param][0]
                for param in DRAFT_SWEEP_PARAMS
            }
            strong_incumbent = {
                param: ConfigGenerator.PARAM_DEFINITIONS[param][1]
                for param in DRAFT_SWEEP_PARAMS
            }

            wins, games, win_rate = evaluator.evaluate(
                draft_order, weak_trial, incumbent_param_values=strong_incumbent
            )

            assert win_rate < 0.5, f"Weaker trial should lose to strong incumbent, got win_rate {win_rate}"

    def test_symmetric_when_incumbent_omitted(self, tmp_path):
        """AC1/AC4: With incumbent_param_values omitted, measured-against-itself returns ~0.50."""
        with patch('simulation.win_rate.CombinationEvaluator.ConfigManager') as mock_cm, \
             patch('simulation.win_rate.CombinationEvaluator.SimDataLoader') as mock_sdl, \
             patch('simulation.win_rate.CombinationEvaluator.ParallelLeagueRunner') as mock_plr_class:

            mock_cm.return_value.config_name = "test_config"
            mock_cm.return_value.description = "Test"
            mock_cm.return_value.parameters = _fake_params()

            mock_sdl.return_value.is_valid = True
            mock_sdl.return_value.week_data_cache = {}

            mock_runner = FakeRunner()
            mock_plr_class.return_value = mock_runner

            season_folder = tmp_path / "2023"
            season_folder.mkdir()
            config_path = tmp_path / "configs" / "league_config.json"
            config_path.parent.mkdir(parents=True)

            evaluator = CombinationEvaluator(
                data_folder=tmp_path,
                num_simulations=10,
                config_path=config_path
            )

            draft_order = [1, 2, 3]
            params = {
                param: (ConfigGenerator.PARAM_DEFINITIONS[param][1] + ConfigGenerator.PARAM_DEFINITIONS[param][0]) / 2
                for param in DRAFT_SWEEP_PARAMS
            }

            wins, games, win_rate = evaluator.evaluate(draft_order, params)

            # Symmetric self-play should be ~0.5
            assert abs(win_rate - 0.5) < 0.15, f"Symmetric evaluation should have win_rate ~= 0.5, got {win_rate}"


class TestDiscriminationWiring:
    """Test that the discrimination split is correctly threaded through the evaluator."""

    def test_evaluate_passes_distinct_measured_config(self, tmp_path):
        """AC1 wiring: assert distinct measured_config_dict reaches the runner."""
        with patch('simulation.win_rate.CombinationEvaluator.ConfigManager') as mock_cm, \
             patch('simulation.win_rate.CombinationEvaluator.SimDataLoader') as mock_sdl, \
             patch('simulation.win_rate.CombinationEvaluator.ParallelLeagueRunner') as mock_plr_class:

            mock_cm.return_value.config_name = "test_config"
            mock_cm.return_value.description = "Test"
            mock_cm.return_value.parameters = _fake_params()

            mock_sdl.return_value.is_valid = True
            mock_sdl.return_value.week_data_cache = {}

            # Create a mock runner that captures the call
            mock_runner = Mock()
            mock_runner.run_simulations_for_config.return_value = [(1, 0, 1500.0)] * 10
            mock_runner.last_dropped_count = 0
            mock_runner.last_requested_count = 10
            mock_plr_class.return_value = mock_runner

            season_folder = tmp_path / "2023"
            season_folder.mkdir()
            config_path = tmp_path / "configs" / "league_config.json"
            config_path.parent.mkdir(parents=True)

            evaluator = CombinationEvaluator(
                data_folder=tmp_path,
                num_simulations=10,
                config_path=config_path
            )

            draft_order = [1, 2, 3]
            trial_params = {
                param: ConfigGenerator.PARAM_DEFINITIONS[param][1]
                for param in DRAFT_SWEEP_PARAMS
            }
            incumbent_params = {
                param: ConfigGenerator.PARAM_DEFINITIONS[param][0]
                for param in DRAFT_SWEEP_PARAMS
            }

            evaluator.evaluate(draft_order, trial_params, incumbent_param_values=incumbent_params)

            # Assert the runner was called with measured_config_dict kwarg
            assert mock_runner.run_simulations_for_config.called
            call_args = mock_runner.run_simulations_for_config.call_args
            # The call should have measured_config_dict as a kwarg
            assert "measured_config_dict" in call_args.kwargs
            # The measured_config_dict should NOT be equal to the positional arg (incumbent_config)
            # (they would be equal only if both trial and incumbent params are identical)
            measured = call_args.kwargs["measured_config_dict"]
            incumbent = call_args.args[0]  # First positional arg is incumbent_config
            # For our test case, they should be different
            assert measured != incumbent, "Measured and incumbent configs should differ"
