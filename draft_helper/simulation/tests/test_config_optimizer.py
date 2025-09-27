"""
Unit tests for configuration optimizer.
"""

import unittest
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from draft_helper.simulation.config_optimizer import ConfigurationOptimizer, ConfigResult


class TestConfigurationOptimizer(unittest.TestCase):
    """Test cases for ConfigurationOptimizer"""

    def setUp(self):
        """Set up test data"""
        self.optimizer = ConfigurationOptimizer()

        # Create sample config results
        self.sample_results = [
            ConfigResult(
                config_params={'INJURY_PENALTIES_MEDIUM': 25, 'POS_NEEDED_SCORE': 50},
                avg_win_percentage=0.65,
                avg_total_points=1500.0,
                avg_points_per_game=88.2,
                avg_consistency=15.5,
                simulations_run=50,
                user_team_rankings=[1, 2, 1, 3, 1]
            ),
            ConfigResult(
                config_params={'INJURY_PENALTIES_MEDIUM': 35, 'POS_NEEDED_SCORE': 60},
                avg_win_percentage=0.72,
                avg_total_points=1550.0,
                avg_points_per_game=91.2,
                avg_consistency=12.3,
                simulations_run=50,
                user_team_rankings=[1, 1, 2, 1, 1]
            ),
            ConfigResult(
                config_params={'INJURY_PENALTIES_MEDIUM': 15, 'POS_NEEDED_SCORE': 40},
                avg_win_percentage=0.58,
                avg_total_points=1480.0,
                avg_points_per_game=87.1,
                avg_consistency=18.7,
                simulations_run=50,
                user_team_rankings=[2, 3, 2, 2, 3]
            )
        ]

    def test_generate_preliminary_configs(self):
        """Test preliminary configuration generation"""
        configs = self.optimizer.generate_preliminary_configs()

        self.assertIsInstance(configs, list)
        self.assertGreater(len(configs), 0)

        # Check that each config has required parameters
        for config in configs:
            self.assertIn('INJURY_PENALTIES_MEDIUM', config)
            self.assertIn('INJURY_PENALTIES_HIGH', config)
            self.assertIn('POS_NEEDED_SCORE', config)
            self.assertIn('PROJECTION_BASE_SCORE', config)
            self.assertIn('BASE_BYE_PENALTY', config)

    def test_identify_top_configs(self):
        """Test identifying top configurations"""
        top_configs = self.optimizer.identify_top_configs(self.sample_results)

        self.assertIsInstance(top_configs, list)

        # Should return configs in order of performance
        if len(top_configs) >= 2:
            # Check that configs are returned in order of win percentage
            first_config = None
            second_config = None

            for result in self.sample_results:
                if result.config_params == top_configs[0]:
                    first_config = result
                elif result.config_params == top_configs[1]:
                    second_config = result

            if first_config and second_config:
                self.assertGreaterEqual(first_config.avg_win_percentage,
                                       second_config.avg_win_percentage)

    def test_analyze_config_performance_empty_results(self):
        """Test analyzing performance with empty results"""
        config_params = {'INJURY_PENALTIES_MEDIUM': 25}
        result = self.optimizer.analyze_config_performance(config_params, [])

        self.assertEqual(result.avg_win_percentage, 0.0)
        self.assertEqual(result.avg_total_points, 0.0)
        self.assertEqual(result.simulations_run, 0)
        self.assertEqual(len(result.user_team_rankings), 0)

    def test_analyze_config_performance_with_data(self):
        """Test analyzing performance with actual data"""
        config_params = {'INJURY_PENALTIES_MEDIUM': 25}

        # Sample simulation results
        simulation_results = [
            {
                'user_team_index': 0,
                'season_stats': {
                    0: type('Stats', (), {
                        'win_percentage': 0.7,
                        'total_points': 1600.0,
                        'points_per_game': 94.1,
                        'score_consistency': 12.5
                    })()
                },
                'team_rankings': [
                    {'team_index': 0, 'rank': 1}
                ]
            },
            {
                'user_team_index': 0,
                'season_stats': {
                    0: type('Stats', (), {
                        'win_percentage': 0.6,
                        'total_points': 1550.0,
                        'points_per_game': 91.2,
                        'score_consistency': 15.0
                    })()
                },
                'team_rankings': [
                    {'team_index': 0, 'rank': 2}
                ]
            }
        ]

        result = self.optimizer.analyze_config_performance(config_params, simulation_results)

        self.assertEqual(result.config_params, config_params)
        self.assertEqual(result.simulations_run, 2)
        self.assertAlmostEqual(result.avg_win_percentage, 0.65, places=2)  # (0.7 + 0.6) / 2
        self.assertEqual(result.avg_total_points, 1575.0)  # (1600 + 1550) / 2
        self.assertEqual(result.user_team_rankings, [1, 2])

    def test_get_optimal_config_empty_results(self):
        """Test getting optimal config with no results"""
        result = self.optimizer.get_optimal_config()
        self.assertIsNone(result)

    def test_get_optimal_config_with_results(self):
        """Test getting optimal config with results"""
        self.optimizer.full_results = self.sample_results

        optimal = self.optimizer.get_optimal_config()

        self.assertIsNotNone(optimal)
        # Should return the config with highest win percentage (0.72)
        self.assertEqual(optimal.avg_win_percentage, 0.72)
        self.assertEqual(optimal.config_params['INJURY_PENALTIES_MEDIUM'], 35)

    def test_apply_draft_order_weights(self):
        """Test applying draft order weights"""
        config = {
            'INJURY_PENALTIES_MEDIUM': 25,
            'DRAFT_ORDER_WEIGHTS': 1.2
        }

        modified_config = self.optimizer._apply_draft_order_weights(config)

        self.assertIn('DRAFT_ORDER', modified_config)
        self.assertEqual(modified_config['DRAFT_ORDER_WEIGHTS'], 1.2)

    def test_generate_config_variations(self):
        """Test generating configuration variations"""
        base_config = {
            'INJURY_PENALTIES_MEDIUM': 25,
            'INJURY_PENALTIES_HIGH': 50,
            'POS_NEEDED_SCORE': 50
        }

        variations = self.optimizer._generate_config_variations(base_config)

        self.assertIsInstance(variations, list)
        self.assertGreater(len(variations), 1)  # Should include base + variations

        # Base config should be included
        self.assertIn(base_config, variations)

        # Should have variations with different values
        has_different_values = False
        for variation in variations:
            if variation != base_config:
                has_different_values = True
                break

        self.assertTrue(has_different_values)


class TestConfigResult(unittest.TestCase):
    """Test ConfigResult dataclass"""

    def test_config_result_creation(self):
        """Test creating ConfigResult objects"""
        config_params = {'INJURY_PENALTIES_MEDIUM': 30}
        result = ConfigResult(
            config_params=config_params,
            avg_win_percentage=0.68,
            avg_total_points=1520.0,
            avg_points_per_game=89.4,
            avg_consistency=14.2,
            simulations_run=25,
            user_team_rankings=[1, 2, 1, 1, 3]
        )

        self.assertEqual(result.config_params, config_params)
        self.assertEqual(result.avg_win_percentage, 0.68)
        self.assertEqual(result.avg_total_points, 1520.0)
        self.assertEqual(result.simulations_run, 25)
        self.assertEqual(len(result.user_team_rankings), 5)


if __name__ == '__main__':
    unittest.main()