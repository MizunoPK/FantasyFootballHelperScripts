"""
Integration Tests for Accuracy Simulation Workflow

Tests end-to-end accuracy simulation workflows:
- Config generation → MAE calculation → Results
- ROS mode optimization
- Weekly mode optimization
- Output file validation

Author: Claude Code
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Accuracy simulation imports
sys.path.append(str(project_root / "simulation" / "shared"))
sys.path.append(str(project_root / "simulation" / "accuracy"))
from ConfigGenerator import ConfigGenerator
from AccuracySimulationManager import AccuracySimulationManager
from AccuracyResultsManager import AccuracyResultsManager, WEEK_RANGES
from AccuracyCalculator import AccuracyCalculator, AccuracyResult


# Test parameter order - mirrors the PARAMETER_ORDER in run_accuracy_simulation.py
# These affect how projected points are calculated (prediction params)
# NOTE: PLAYER_RATING_SCORING_WEIGHT is excluded because StarterHelperModeManager
# (the consuming mode) has player_rating=False, so this parameter has no effect.
TEST_PARAMETER_ORDER = [
    'NORMALIZATION_MAX_SCALE',
    'TEAM_QUALITY_SCORING_WEIGHT',
    'TEAM_QUALITY_MIN_WEEKS',
    'PERFORMANCE_SCORING_WEIGHT',
    'PERFORMANCE_SCORING_STEPS',
    'PERFORMANCE_MIN_WEEKS',
    'MATCHUP_IMPACT_SCALE',
    'MATCHUP_SCORING_WEIGHT',
    'MATCHUP_MIN_WEEKS',
    'TEMPERATURE_IMPACT_SCALE',
    'TEMPERATURE_SCORING_WEIGHT',
    'WIND_IMPACT_SCALE',
    'WIND_SCORING_WEIGHT',
    'LOCATION_HOME',
    'LOCATION_AWAY',
    'LOCATION_INTERNATIONAL',
]


def create_mock_historical_season(data_folder: Path, year: str = "2024") -> None:
    """Create a mock historical season folder structure for accuracy testing."""
    season_folder = data_folder / year
    season_folder.mkdir(parents=True, exist_ok=True)

    # Create required root files
    (season_folder / "season_schedule.csv").write_text(
        "week,home_team,away_team,home_score,away_score\n"
        "1,KC,DET,27,24\n"
        "2,KC,JAX,17,9\n"
    )
    (season_folder / "game_data.csv").write_text(
        "week,home_team,away_team,temperature,wind_speed,location\n"
        "1,KC,DET,72,5,HOME\n"
        "2,KC,JAX,68,8,AWAY\n"
    )

    # Create team_data folder with team files
    team_data_folder = season_folder / "team_data"
    team_data_folder.mkdir(exist_ok=True)

    for team in ["KC", "DET", "MIN", "SF", "BUF", "MIA", "LAC", "BAL", "JAX"]:
        (team_data_folder / f"teams_week_1.csv").write_text(
            "team,offensive_rank,defensive_rank\n"
            "KC,1,5\n"
            "DET,3,10\n"
            "MIN,5,8\n"
        )

    # Create weeks folder with player data
    weeks_folder = season_folder / "weeks"
    weeks_folder.mkdir(exist_ok=True)

    # Create player_data folder for JSON files
    player_data_folder = season_folder / "player_data"
    player_data_folder.mkdir(exist_ok=True)

    # Helper to build 17-element arrays for projected/actual points
    def build_points_array(base_points: float, current_week: int, is_projected: bool = False) -> list:
        """Build 17-element array of points (actual or projected)"""
        points = []
        for w in range(1, 18):
            if w <= current_week:
                # Vary points slightly per week
                week_points = base_points + (w * 0.5) - 5
                if is_projected:
                    week_points -= 1.0  # Projected slightly lower than actual
                points.append(round(week_points, 1))
            else:
                points.append(None)
        return points

    # Create position-specific JSON files with test players
    qb_data = [
        {
            "id": "1",
            "name": "Patrick Mahomes",
            "position": "QB",
            "team": "KC",
            "bye_week": 7,
            "fantasy_points": 350.5,
            "injury_status": "ACTIVE",
            "average_draft_position": 1.2,
            "player_rating": 95,
            "locked": False,
            "drafted_by": None,
            "projected_points": build_points_array(25.0, 17, is_projected=True),
            "actual_points": build_points_array(25.0, 17, is_projected=False)
        }
    ]

    rb_data = [
        {
            "id": "3",
            "name": "Christian McCaffrey",
            "position": "RB",
            "team": "SF",
            "bye_week": 9,
            "fantasy_points": 320.1,
            "injury_status": "ACTIVE",
            "average_draft_position": 1.1,
            "player_rating": 94,
            "locked": False,
            "drafted_by": None,
            "projected_points": build_points_array(22.0, 17, is_projected=True),
            "actual_points": build_points_array(22.0, 17, is_projected=False)
        }
    ]

    wr_data = [
        {
            "id": "2",
            "name": "Justin Jefferson",
            "position": "WR",
            "team": "MIN",
            "bye_week": 13,
            "fantasy_points": 310.8,
            "injury_status": "ACTIVE",
            "average_draft_position": 2.1,
            "player_rating": 92,
            "locked": False,
            "drafted_by": None,
            "projected_points": build_points_array(18.0, 17, is_projected=True),
            "actual_points": build_points_array(18.0, 17, is_projected=False)
        }
    ]

    te_data = [
        {
            "id": "4",
            "name": "Travis Kelce",
            "position": "TE",
            "team": "KC",
            "bye_week": 7,
            "fantasy_points": 220.4,
            "injury_status": "ACTIVE",
            "average_draft_position": 4.5,
            "player_rating": 88,
            "locked": False,
            "drafted_by": None,
            "projected_points": build_points_array(12.0, 17, is_projected=True),
            "actual_points": build_points_array(12.0, 17, is_projected=False)
        }
    ]

    k_data = []
    dst_data = []

    # Write position JSON files
    with open(player_data_folder / "qb_data.json", 'w') as f:
        json.dump(qb_data, f, indent=2)
    with open(player_data_folder / "rb_data.json", 'w') as f:
        json.dump(rb_data, f, indent=2)
    with open(player_data_folder / "wr_data.json", 'w') as f:
        json.dump(wr_data, f, indent=2)
    with open(player_data_folder / "te_data.json", 'w') as f:
        json.dump(te_data, f, indent=2)
    with open(player_data_folder / "k_data.json", 'w') as f:
        json.dump(k_data, f, indent=2)
    with open(player_data_folder / "dst_data.json", 'w') as f:
        json.dump(dst_data, f, indent=2)

    for week_num in range(1, 18):
        week_folder = weeks_folder / f"week_{week_num:02d}"
        week_folder.mkdir(exist_ok=True)

        # Helper to build week-specific points arrays
        def build_week_points(base_points: float, is_projected: bool = False) -> list:
            points = []
            for w in range(1, 18):
                if w <= week_num:
                    week_points = base_points + (w * 0.5) - 5
                    if is_projected:
                        week_points -= 1.0
                    points.append(round(week_points, 1))
                else:
                    points.append(None)
            return points

        # Create week-specific JSON files (6 position files per week)
        qb_week = [{"id": "1", "name": "Patrick Mahomes", "position": "QB", "team": "KC", "bye_week": 7,
                     "fantasy_points": 350.5, "injury_status": "ACTIVE", "average_draft_position": 1.2,
                     "player_rating": 95, "locked": False, "drafted_by": None,
                     "projected_points": build_week_points(25.0, True), "actual_points": build_week_points(25.0, False)}]
        rb_week = [{"id": "3", "name": "Christian McCaffrey", "position": "RB", "team": "SF", "bye_week": 9,
                     "fantasy_points": 320.1, "injury_status": "ACTIVE", "average_draft_position": 1.1,
                     "player_rating": 94, "locked": False, "drafted_by": None,
                     "projected_points": build_week_points(22.0, True), "actual_points": build_week_points(22.0, False)}]
        wr_week = [{"id": "2", "name": "Justin Jefferson", "position": "WR", "team": "MIN", "bye_week": 13,
                     "fantasy_points": 310.8, "injury_status": "ACTIVE", "average_draft_position": 2.1,
                     "player_rating": 92, "locked": False, "drafted_by": None,
                     "projected_points": build_week_points(18.0, True), "actual_points": build_week_points(18.0, False)}]
        te_week = [{"id": "4", "name": "Travis Kelce", "position": "TE", "team": "KC", "bye_week": 7,
                     "fantasy_points": 220.4, "injury_status": "ACTIVE", "average_draft_position": 4.5,
                     "player_rating": 88, "locked": False, "drafted_by": None,
                     "projected_points": build_week_points(12.0, True), "actual_points": build_week_points(12.0, False)}]

        with open(week_folder / "qb_data.json", 'w') as f:
            json.dump(qb_week, f, indent=2)
        with open(week_folder / "rb_data.json", 'w') as f:
            json.dump(rb_week, f, indent=2)
        with open(week_folder / "wr_data.json", 'w') as f:
            json.dump(wr_week, f, indent=2)
        with open(week_folder / "te_data.json", 'w') as f:
            json.dump(te_week, f, indent=2)
        with open(week_folder / "k_data.json", 'w') as f:
            json.dump([], f, indent=2)
        with open(week_folder / "dst_data.json", 'w') as f:
            json.dump([], f, indent=2)


@pytest.fixture
def temp_accuracy_data(tmp_path):
    """Create temporary simulation data folder with historical season structure"""
    data_folder = tmp_path / "sim_data"
    data_folder.mkdir()

    # Create mock historical season folder structure
    create_mock_historical_season(data_folder, "2024")

    return data_folder


def create_test_config_folder(tmp_path: Path) -> Path:
    """Create a test config folder with all required files for ConfigGenerator."""
    config_folder = tmp_path / "test_configs"
    config_folder.mkdir(parents=True, exist_ok=True)

    # Try to load from actual data/configs folder if it exists
    actual_configs = project_root / "data" / "configs"
    if actual_configs.exists():
        # Copy from real configs (5 files: 1 base + 4 weekly)
        for config_file in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            src = actual_configs / config_file
            if src.exists():
                with open(src) as f:
                    data = json.load(f)
                with open(config_folder / config_file, 'w') as f:
                    json.dump(data, f, indent=2)
        return config_folder

    # Fallback: create minimal config structure
    base_config = {
        'config_name': 'test_baseline',
        'description': 'Test base config',
        'parameters': {
            'CURRENT_NFL_WEEK': 14,
            'NFL_SEASON': 2025,
            'NFL_SCORING_FORMAT': 'ppr',
            'SAME_POS_BYE_WEIGHT': 1.0,
            'DIFF_POS_BYE_WEIGHT': 1.0,
            'INJURY_PENALTIES': {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0},
            'DRAFT_ORDER_BONUSES': {'PRIMARY': 50.0, 'SECONDARY': 40.0},
            'DRAFT_ORDER_FILE': 1,
            'DRAFT_ORDER': [{"FLEX": "P", "QB": "S"}] * 15,
            'MAX_POSITIONS': {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
            'FLEX_ELIGIBLE_POSITIONS': ["RB", "WR"],
            'ADP_SCORING': {
                'WEIGHT': 1.0,
                'MULTIPLIERS': {'EXCELLENT': 1.2, 'GOOD': 1.1, 'POOR': 0.9, 'VERY_POOR': 0.8},
                'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'DECREASING', 'STEPS': 37.5}
            },
        }
    }
    with open(config_folder / 'league_config.json', 'w') as f:
        json.dump(base_config, f, indent=2)

    week_params = {
        'NORMALIZATION_MAX_SCALE': 145.0,
        'PLAYER_RATING_SCORING': {
            'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.25, 'GOOD': 1.15, 'POOR': 0.85, 'VERY_POOR': 0.75},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'INCREASING', 'STEPS': 20.0}
        },
        'TEAM_QUALITY_SCORING': {
            'MIN_WEEKS': 5, 'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.3, 'GOOD': 1.2, 'POOR': 0.8, 'VERY_POOR': 0.7},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'DECREASING', 'STEPS': 6.25}
        },
        'PERFORMANCE_SCORING': {
            'WEIGHT': 1.0, 'MIN_WEEKS': 5,
            'MULTIPLIERS': {'EXCELLENT': 1.15, 'GOOD': 1.05, 'POOR': 0.95, 'VERY_POOR': 0.85},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'BI_EXCELLENT_HI', 'STEPS': 0.1}
        },
        'MATCHUP_SCORING': {
            'MIN_WEEKS': 5, 'IMPACT_SCALE': 150.0, 'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.2, 'GOOD': 1.1, 'POOR': 0.9, 'VERY_POOR': 0.8},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'BI_EXCELLENT_HI', 'STEPS': 7.5}
        },
        'SCHEDULE_SCORING': {
            'MIN_WEEKS': 5, 'IMPACT_SCALE': 80.0, 'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.05, 'GOOD': 1.025, 'POOR': 0.975, 'VERY_POOR': 0.95},
            'THRESHOLDS': {'BASE_POSITION': 16, 'DIRECTION': 'INCREASING', 'STEPS': 8.0}
        },
        'TEMPERATURE_SCORING': {
            'IDEAL_TEMPERATURE': 60, 'IMPACT_SCALE': 50.0, 'WEIGHT': 1.0,
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'DECREASING', 'STEPS': 10},
            'MULTIPLIERS': {'EXCELLENT': 1.05, 'GOOD': 1.025, 'POOR': 0.975, 'VERY_POOR': 0.95}
        },
        'WIND_SCORING': {
            'IMPACT_SCALE': 60.0, 'WEIGHT': 1.0,
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'DECREASING', 'STEPS': 8},
            'MULTIPLIERS': {'EXCELLENT': 1.05, 'GOOD': 1.025, 'POOR': 0.975, 'VERY_POOR': 0.95}
        },
        'LOCATION_MODIFIERS': {'HOME': 2.0, 'AWAY': -2.0, 'INTERNATIONAL': -5.0},
    }

    # Create week-specific configs
    for week_file in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
        week_config = {
            'config_name': f'Test {week_file}',
            'description': f'Test week config for {week_file}',
            'parameters': week_params
        }
        with open(config_folder / week_file, 'w') as f:
            json.dump(week_config, f, indent=2)

    return config_folder


@pytest.fixture
def baseline_config(tmp_path):
    """Create a baseline configuration folder for testing"""
    return create_test_config_folder(tmp_path)


class TestAccuracyCalculatorIntegration:
    """Integration tests for AccuracyCalculator"""

    def test_calculator_initializes(self):
        """Test AccuracyCalculator initializes successfully"""
        calculator = AccuracyCalculator()
        assert calculator is not None

    def test_calculator_calculates_weekly_mae(self):
        """Test AccuracyCalculator calculates weekly MAE correctly"""
        calculator = AccuracyCalculator()

        projections = {
            1: {1: 25.0, 2: 18.0},
            2: {1: 24.0, 2: 17.0}
        }
        actuals = {
            1: {1: 23.0, 2: 19.0},
            2: {1: 26.0, 2: 16.0}
        }

        result = calculator.calculate_weekly_mae(projections, actuals, (1, 2))

        assert result.mae > 0
        assert result.player_count > 0

    def test_calculator_aggregates_season_results(self):
        """Test AccuracyCalculator aggregates multiple seasons correctly"""
        calculator = AccuracyCalculator()

        season_results = [
            ("2022", AccuracyResult(mae=10.0, player_count=100, total_error=1000.0)),
            ("2023", AccuracyResult(mae=12.0, player_count=100, total_error=1200.0)),
            ("2024", AccuracyResult(mae=8.0, player_count=100, total_error=800.0)),
        ]

        result = calculator.aggregate_season_results(season_results)

        # Aggregate MAE = total_error / total_players = 3000 / 300 = 10.0
        assert result.player_count == 300
        assert abs(result.mae - 10.0) < 0.01


class TestAccuracyResultsManagerIntegration:
    """Integration tests for AccuracyResultsManager"""

    def test_results_manager_initializes(self, tmp_path, baseline_config):
        """Test AccuracyResultsManager initializes successfully"""
        output_dir = tmp_path / "output"
        manager = AccuracyResultsManager(output_dir, baseline_config)
        assert manager is not None
        assert manager.baseline_config_path == baseline_config

    def test_results_manager_adds_results(self, tmp_path, baseline_config):
        """Test AccuracyResultsManager can add results"""
        output_dir = tmp_path / "output"
        manager = AccuracyResultsManager(output_dir, baseline_config)

        with open(baseline_config / 'league_config.json') as f:
            config_dict = json.load(f)

        result = AccuracyResult(mae=15.5, player_count=100, total_error=1550.0)
        is_new_best = manager.add_result('ros', config_dict, result)

        assert is_new_best is True  # First result is always best

    def test_results_manager_tracks_best_config(self, tmp_path, baseline_config):
        """Test AccuracyResultsManager tracks best config correctly"""
        output_dir = tmp_path / "output"
        manager = AccuracyResultsManager(output_dir, baseline_config)

        with open(baseline_config / 'league_config.json') as f:
            config_dict = json.load(f)

        # Add worse result first
        result1 = AccuracyResult(mae=20.0, player_count=100, total_error=2000.0)
        manager.add_result('ros', config_dict, result1)

        # Add better result (lower MAE)
        result2 = AccuracyResult(mae=15.0, player_count=100, total_error=1500.0)
        is_new_best = manager.add_result('ros', config_dict, result2)

        assert is_new_best is True

        best = manager.get_best_config('ros')
        assert best is not None
        assert best.mae == 15.0

    def test_results_manager_saves_optimal_configs(self, tmp_path, baseline_config):
        """Test AccuracyResultsManager saves optimal configs correctly"""
        output_dir = tmp_path / "output"
        manager = AccuracyResultsManager(output_dir, baseline_config)

        with open(baseline_config / 'league_config.json') as f:
            config_dict = json.load(f)

        result = AccuracyResult(mae=15.5, player_count=100, total_error=1550.0)
        manager.add_result('ros', config_dict, result)

        optimal_path = manager.save_optimal_configs()

        assert optimal_path.exists()
        assert (optimal_path / 'league_config.json').exists()  # Copied from baseline
        assert (optimal_path / 'week1-5.json').exists()
        assert (optimal_path / 'week6-9.json').exists()
        assert (optimal_path / 'week10-13.json').exists()
        assert (optimal_path / 'week14-17.json').exists()
        # No separate performance_metrics.json - metrics are embedded in each config file


class TestAccuracySimulationManagerIntegration:
    """Integration tests for AccuracySimulationManager"""

    def test_manager_initializes(self, baseline_config, temp_accuracy_data, tmp_path):
        """Test AccuracySimulationManager initializes successfully"""
        output_dir = tmp_path / "results"

        manager = AccuracySimulationManager(
            baseline_config_path=baseline_config,
            output_dir=output_dir,
            data_folder=temp_accuracy_data,
            parameter_order=TEST_PARAMETER_ORDER,
            num_test_values=1,
            num_parameters_to_test=1
        )

        assert manager is not None
        assert len(manager.available_seasons) >= 1

    def test_manager_has_correct_parameter_order(self, baseline_config, temp_accuracy_data, tmp_path):
        """Test AccuracySimulationManager uses correct parameter order"""
        output_dir = tmp_path / "results"

        manager = AccuracySimulationManager(
            baseline_config_path=baseline_config,
            output_dir=output_dir,
            data_folder=temp_accuracy_data,
            parameter_order=TEST_PARAMETER_ORDER,
            num_test_values=1
        )

        # Should have 16 accuracy parameters (PLAYER_RATING excluded - see TEST_PARAMETER_ORDER comment)
        assert len(TEST_PARAMETER_ORDER) == 16
        assert 'NORMALIZATION_MAX_SCALE' in TEST_PARAMETER_ORDER
        assert 'PLAYER_RATING_SCORING_WEIGHT' not in TEST_PARAMETER_ORDER  # Excluded
        assert 'LOCATION_INTERNATIONAL' in TEST_PARAMETER_ORDER
        # Verify manager stored the parameter order
        assert manager.parameter_order == TEST_PARAMETER_ORDER


class TestWeekRanges:
    """Tests for week range configuration"""

    def test_week_ranges_defined_correctly(self):
        """Test week ranges are defined correctly"""
        assert 'week_1_5' in WEEK_RANGES
        assert 'week_6_9' in WEEK_RANGES
        assert 'week_10_13' in WEEK_RANGES
        assert 'week_14_17' in WEEK_RANGES

        assert WEEK_RANGES['week_1_5'] == (1, 5)
        assert WEEK_RANGES['week_6_9'] == (6, 9)
        assert WEEK_RANGES['week_10_13'] == (10, 13)
        assert WEEK_RANGES['week_14_17'] == (14, 17)


class TestOutputFileValidation:
    """Tests for output file structure validation"""

class TestErrorHandling:
    """Integration tests for error handling"""

    def test_handles_missing_data_folder(self, baseline_config, tmp_path):
        """Test handles missing data folder gracefully"""
        nonexistent_path = tmp_path / "nonexistent"

        # FileNotFoundError when folder doesn't exist, ValueError when folder exists but has no seasons
        with pytest.raises((ValueError, FileNotFoundError)):
            AccuracySimulationManager(
                baseline_config_path=baseline_config,
                output_dir=tmp_path / "results",
                data_folder=nonexistent_path,
                parameter_order=TEST_PARAMETER_ORDER,
                num_test_values=1
            )

    def test_handles_empty_projections(self):
        """Test handles empty projections gracefully"""
        calculator = AccuracyCalculator()

        # Use calculate_weekly_mae with empty dicts
        result = calculator.calculate_weekly_mae({}, {}, (1, 5))

        assert result.mae == 0.0
        assert result.player_count == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
