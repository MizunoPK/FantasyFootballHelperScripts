"""
Integration Tests for Simulation Workflow

Tests end-to-end simulation workflows:
- Config generation → Simulation → Results
- Multi-config simulation runs
- Parallel execution
- Error scenarios

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

project_root = Path(__file__).parent.parent.parent

from simulation.shared.ConfigGenerator import ConfigGenerator
from simulation.win_rate.DraftStrategyOrchestrator import DraftStrategyOrchestrator
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager
from simulation.win_rate.ParallelLeagueRunner import ParallelLeagueRunner
from simulation.shared.ResultsManager import ResultsManager
from simulation.shared.ConfigPerformance import ConfigPerformance

TEST_PARAMETER_ORDER = [
    'NORMALIZATION_MAX_SCALE',
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    'PRIMARY_BONUS',
    'SECONDARY_BONUS',
    'ADP_SCORING_WEIGHT',
    'PLAYER_RATING_SCORING_WEIGHT',
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

VALID_DRAFT_ORDER = [
    {"WR": "P", "RB": "S"},
    {"WR": "P", "RB": "S"},
    {"TE": "P", "WR": "S"},
    {"WR": "P", "RB": "S"},
    {"QB": "P", "FLEX": "S"},
    {"TE": "P", "WR": "S"},
    {"RB": "P", "WR": "S"},
    {"QB": "P", "FLEX": "S"},
    {"RB": "P", "WR": "S"},
    {"RB": "P", "WR": "S"},
    {"WR": "P", "RB": "S"},
    {"RB": "P", "WR": "S"},
    {"K": "P", "FLEX": "S"},
    {"DST": "P", "FLEX": "S"},
    {"FLEX": "P"},
]


def create_mock_historical_season(data_folder: Path, year: str = "2024") -> None:
    """Create a mock historical season folder structure for testing."""
    season_folder = data_folder / year
    season_folder.mkdir(parents=True, exist_ok=True)

    (season_folder / "season_schedule.csv").write_text("week,home,away\n1,KC,DET\n")
    (season_folder / "game_data.csv").write_text("week,home,away\n1,KC,DET\n")

    (season_folder / "team_data").mkdir(exist_ok=True)
    (season_folder / "team_data" / "KC.csv").write_text("week,points\n1,30\n")

    weeks_folder = season_folder / "weeks"
    weeks_folder.mkdir(exist_ok=True)
    for week_num in range(1, 18):
        week_folder = weeks_folder / f"week_{week_num:02d}"
        week_folder.mkdir(exist_ok=True)

        position_files = {
            'qb_data.json': [{"id": 1, "name": "Test QB", "position": "QB", "team": "KC", "drafted_by": "", "locked": False,
                              "projected_points": [20.0]*17, "actual_points": [18.0]*17}],
            'rb_data.json': [{"id": 2, "name": "Test RB", "position": "RB", "team": "KC", "drafted_by": "", "locked": False,
                              "projected_points": [15.0]*17, "actual_points": [14.0]*17}],
            'wr_data.json': [{"id": 3, "name": "Test WR", "position": "WR", "team": "KC", "drafted_by": "", "locked": False,
                              "projected_points": [12.0]*17, "actual_points": [11.0]*17}],
            'te_data.json': [{"id": 4, "name": "Test TE", "position": "TE", "team": "KC", "drafted_by": "", "locked": False,
                              "projected_points": [10.0]*17, "actual_points": [9.0]*17}],
            'k_data.json': [{"id": 5, "name": "Test K", "position": "K", "team": "KC", "drafted_by": "", "locked": False,
                             "projected_points": [8.0]*17, "actual_points": [7.0]*17}],
            'dst_data.json': [{"id": 6, "name": "Test DST", "position": "DST", "team": "KC", "drafted_by": "", "locked": False,
                               "projected_points": [10.0]*17, "actual_points": [9.0]*17}]
        }

        for filename, data in position_files.items():
            (week_folder / filename).write_text(json.dumps(data, indent=2))


@pytest.fixture
def temp_simulation_data(tmp_path):
    """Create temporary simulation data folder with historical season structure"""
    data_folder = tmp_path / "sim_data"
    data_folder.mkdir()

    create_mock_historical_season(data_folder)

    players_csv = data_folder / "players_projected.csv"
    players_csv.write_text("""id,name,position,team,bye_week,fantasy_points,injury_status,average_draft_position
1,Patrick Mahomes,QB,KC,7,350.5,ACTIVE,1.2
2,Justin Jefferson,WR,MIN,13,310.8,ACTIVE,2.1
3,Christian McCaffrey,RB,SF,9,320.1,ACTIVE,1.1
4,Travis Kelce,TE,KC,7,220.4,ACTIVE,4.5
5,Josh Allen,QB,BUF,12,340.2,ACTIVE,1.5
6,Tyreek Hill,WR,MIA,10,305.3,ACTIVE,2.3
7,Austin Ekeler,RB,LAC,5,295.7,ACTIVE,3.2
8,Mark Andrews,TE,BAL,13,210.3,ACTIVE,5.1
""")

    players_actual_csv = data_folder / "players_actual.csv"
    players_actual_csv.write_text("""Name,Position,Team,Week 1,Week 2,Week 3
Patrick Mahomes,QB,KC,25.5,22.3,28.1
Justin Jefferson,WR,MIN,18.2,15.4,22.3
Christian McCaffrey,RB,SF,22.1,19.5,25.2
Travis Kelce,TE,KC,12.3,10.2,15.1
""")

    teams_week_1_csv = data_folder / "teams_week_1.csv"
    teams_week_1_csv.write_text("""Team Name,Position,Player Name
TestTeam,QB,
TestTeam,RB,
TestTeam,RB,
TestTeam,WR,
TestTeam,WR,
TestTeam,TE,
TestTeam,FLEX,
TestTeam,K,
TestTeam,DST,
TestTeam,BENCH,
""")

    return data_folder


def create_test_config_folder(tmp_path: Path) -> Path:
    """Create a test config folder with all required files for ConfigGenerator."""
    config_folder = tmp_path / "test_configs"
    config_folder.mkdir(parents=True, exist_ok=True)

    actual_configs = project_root / "data" / "configs"
    if actual_configs.exists():
        for config_file in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            src = actual_configs / config_file
            if src.exists():
                with open(src) as f:
                    data = json.load(f)
                with open(config_folder / config_file, 'w') as f:
                    json.dump(data, f, indent=2)
        return config_folder

    base_config = {
        'config_name': 'test_baseline',
        'description': 'Test base config',
        'parameters': {
            'SAME_POS_BYE_WEIGHT': 1.0,
            'DIFF_POS_BYE_WEIGHT': 1.0,
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
            'IMPACT_SCALE': 80.0, 'WEIGHT': 1.0,
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


class TestConfigGeneratorIntegration:
    """Integration tests for config generator"""

    def test_config_generator_loads_baseline(self, baseline_config):
        """Test config generator loads baseline config"""
        generator = ConfigGenerator(baseline_config, num_test_values=3)

        assert generator is not None
        assert hasattr(generator, 'baseline_configs')
        assert len(generator.baseline_configs) == 4

    def test_config_generator_creates_combinations(self, baseline_config):
        """Test config generator creates horizon test values"""
        generator = ConfigGenerator(baseline_config, num_test_values=1)

        test_values_shared = generator.generate_horizon_test_values('SAME_POS_BYE_WEIGHT')
        assert 'shared' in test_values_shared
        assert len(test_values_shared['shared']) >= 1

        test_values_horizon = generator.generate_horizon_test_values('NORMALIZATION_MAX_SCALE')
        assert '1-5' in test_values_horizon
        assert '6-9' in test_values_horizon
        assert len(test_values_horizon['1-5']) >= 1

    def test_config_dict_has_required_fields(self, baseline_config):
        """Test generated config dicts have all required fields"""
        generator = ConfigGenerator(baseline_config, num_test_values=1)

        config_dict = generator.get_config_for_horizon('1-5', 'NORMALIZATION_MAX_SCALE', 0)

        assert "parameters" in config_dict
        assert "NORMALIZATION_MAX_SCALE" in config_dict["parameters"]
        assert "SAME_POS_BYE_WEIGHT" in config_dict["parameters"]
        assert "DIFF_POS_BYE_WEIGHT" in config_dict["parameters"]


class TestDraftStrategyOrchestratorIntegration:
    """Integration tests for DraftStrategyOrchestrator"""

    def test_orchestrator_initializes(self, temp_simulation_data, tmp_path):
        """Test DraftStrategyOrchestrator initializes successfully"""
        strategy_dir = temp_simulation_data / "draft_order_possibilities"
        strategy_dir.mkdir()
        (strategy_dir / "1_test.json").write_text(
            '{"name": "Test", "DRAFT_ORDER": []}'
        )

        meta_data_manager = WinRateMetaDataManager(tmp_path / "meta.json")
        orchestrator = DraftStrategyOrchestrator(
            data_folder=temp_simulation_data,
            num_simulations=2,
            max_workers=2,
            meta_data_manager=meta_data_manager
        )

        assert len(orchestrator._seasons) == 1
        assert orchestrator._num_simulations == 2


class TestDraftStrategyOrchestratorRun:
    """Integration tests for DraftStrategyOrchestrator.run()"""

    def _make_orchestrator(self, tmp_path, strategy_files):
        """Helper: create orchestrator with given strategy JSON files."""
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir(exist_ok=True)
        create_mock_historical_season(data_folder)

        strategy_dir = data_folder / "draft_order_possibilities"
        strategy_dir.mkdir()
        for filename, content in strategy_files.items():
            (strategy_dir / filename).write_text(json.dumps(content))

        meta_path = tmp_path / "meta.json"
        meta_data_manager = WinRateMetaDataManager(meta_path)
        orchestrator = DraftStrategyOrchestrator(
            data_folder=data_folder,
            num_simulations=1,
            max_workers=1,
            meta_data_manager=meta_data_manager,
        )
        return orchestrator, meta_data_manager

    def test_run_processes_strategies_in_numeric_order(self, tmp_path):
        """Test run() enumerates strategy files sorted by numeric prefix (AC4)."""
        strategy_files = {
            "3_c.json": {"name": "C", "DRAFT_ORDER": VALID_DRAFT_ORDER},
            "1_a.json": {"name": "A", "DRAFT_ORDER": VALID_DRAFT_ORDER},
            "2_b.json": {"name": "B", "DRAFT_ORDER": VALID_DRAFT_ORDER},
        }
        orchestrator, meta_data_manager = self._make_orchestrator(tmp_path, strategy_files)

        processed_order = []
        original_update = meta_data_manager.update

        def tracking_update(filename, name, win_rate, wins, games):
            processed_order.append(filename)
            original_update(filename, name, win_rate, wins, games)

        with patch("simulation.win_rate.DraftStrategyOrchestrator.SimDataLoader") as mock_loader_class, \
             patch.object(orchestrator._runner, "run_simulations_for_config", return_value=[(1, 0, 100.0)]), \
             patch.object(meta_data_manager, "update", side_effect=tracking_update):
            mock_loader = Mock()
            mock_loader.is_valid = True
            mock_loader.week_data_cache = {}
            mock_loader_class.return_value = mock_loader
            orchestrator.run()

        assert processed_order == ["1_a.json", "2_b.json", "3_c.json"]

    def test_run_calls_update_for_valid_strategies(self, tmp_path):
        """Test run() calls meta_data_manager.update() for each valid strategy (AC5/AC6)."""
        strategy_files = {
            "1_valid.json": {"name": "Valid", "DRAFT_ORDER": VALID_DRAFT_ORDER},
            "2_no_draft_order.json": {"name": "Bad", "other_key": "value"},
        }
        orchestrator, meta_data_manager = self._make_orchestrator(tmp_path, strategy_files)

        with patch("simulation.win_rate.DraftStrategyOrchestrator.SimDataLoader") as mock_loader_class, \
             patch.object(orchestrator._runner, "run_simulations_for_config", return_value=[(1, 0, 100.0)]), \
             patch.object(meta_data_manager, "update") as mock_update:
            mock_loader = Mock()
            mock_loader.is_valid = True
            mock_loader.week_data_cache = {}
            mock_loader_class.return_value = mock_loader
            orchestrator.run()

        mock_update.assert_called_once_with("1_valid.json", "Valid", 1.0, 1, 1)

    def test_run_does_not_mutate_base_config(self, tmp_path):
        """Test run() deep-copies config before injecting DRAFT_ORDER (AC8)."""
        import copy as _copy
        draft_order = VALID_DRAFT_ORDER
        strategy_files = {
            "1_strat.json": {"name": "Strat", "DRAFT_ORDER": draft_order},
        }
        orchestrator, meta_data_manager = self._make_orchestrator(tmp_path, strategy_files)

        base_config_snapshot = _copy.deepcopy(orchestrator._base_config)

        captured_configs = []

        def capture_config(config, n, preloaded_week_data=None):
            captured_configs.append(_copy.deepcopy(config))
            return [(1, 0, 100.0)]

        with patch("simulation.win_rate.DraftStrategyOrchestrator.SimDataLoader") as mock_loader_class, \
             patch.object(orchestrator._runner, "run_simulations_for_config", side_effect=capture_config):
            mock_loader = Mock()
            mock_loader.is_valid = True
            mock_loader.week_data_cache = {}
            mock_loader_class.return_value = mock_loader
            orchestrator.run()

        assert orchestrator._base_config == base_config_snapshot
        assert len(captured_configs) == 1
        assert captured_configs[0]["parameters"]["DRAFT_ORDER"] == draft_order


class TestParallelLeagueRunnerIntegration:
    """Integration tests for parallel league runner"""

    def test_parallel_runner_initializes(self, temp_simulation_data):
        """Test parallel runner initializes successfully"""
        runner = ParallelLeagueRunner(
            max_workers=2,
            data_folder=temp_simulation_data
        )

        assert runner is not None
        assert runner.max_workers == 2


class TestResultsManagerIntegration:
    """Integration tests for results manager"""

    def test_results_manager_initializes(self):
        """Test results manager initializes"""
        manager = ResultsManager()

        assert manager is not None

    def test_results_manager_registers_config(self, baseline_config):
        """Test results manager can register configs"""
        manager = ResultsManager()

        with open(baseline_config / 'league_config.json') as f:
            config_dict = json.load(f)

        manager.register_config("test_config_1", config_dict)

        assert manager is not None

    def test_results_manager_records_results(self, baseline_config):
        """Test results manager can record simulation results"""
        manager = ResultsManager()

        with open(baseline_config / 'league_config.json') as f:
            config_dict = json.load(f)

        manager.register_config("test_config_1", config_dict)

        manager.record_result("test_config_1", wins=10, losses=4, points=1500.5)
        manager.record_result("test_config_1", wins=9, losses=5, points=1480.2)

        best = manager.get_best_config()

        assert best is not None
        assert best.config_id == "test_config_1"
        assert best.num_simulations == 2


class TestConfigPerformanceIntegration:
    """Integration tests for config performance tracking"""

    def test_config_performance_initialization(self, baseline_config):
        """Test ConfigPerformance initializes correctly"""
        with open(baseline_config / 'league_config.json') as f:
            config_dict = json.load(f)

        perf = ConfigPerformance("test_config", config_dict)

        assert perf.config_id == "test_config"
        assert perf.config_dict == config_dict

    def test_config_performance_adds_results(self, baseline_config):
        """Test ConfigPerformance can add simulation results"""
        with open(baseline_config / 'league_config.json') as f:
            config_dict = json.load(f)

        perf = ConfigPerformance("test_config", config_dict)

        perf.add_league_result(wins=10, losses=4, points=1500.0)
        perf.add_league_result(wins=9, losses=5, points=1480.0)

        assert perf.num_simulations == 2
        assert perf.total_wins == 19
        assert perf.total_losses == 9

    def test_config_performance_calculates_win_rate(self, baseline_config):
        """Test ConfigPerformance calculates win rate correctly"""
        with open(baseline_config / 'league_config.json') as f:
            config_dict = json.load(f)

        perf = ConfigPerformance("test_config", config_dict)

        perf.add_league_result(wins=10, losses=4, points=1500.0)

        win_rate = perf.get_win_rate()

        expected_rate = 10 / (10 + 4)
        assert abs(win_rate - expected_rate) < 0.001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


