"""
Main simulation orchestrator that coordinates all simulation components.

Entry point for running complete draft simulation analysis.
"""

import sys
import os
import pandas as pd
from typing import Dict, Any, List

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add current directory to path for local imports
sys.path.append(os.path.dirname(__file__))

from data_manager import SimulationDataManager
from config_optimizer import ConfigurationOptimizer
from parallel_runner import ParallelSimulationRunner
from results_analyzer import ResultsAnalyzer
from simulation_engine import DraftSimulationEngine
from season_simulator import SeasonSimulator
from config import get_timestamped_results_file, RESULTS_DIR
from parameter_loader import load_and_expand_config

class MainSimulator:
    """Main orchestrator for draft simulation analysis"""

    def __init__(self, parameter_config_path: str = None, parameter_config: Dict[str, List] = None):
        """
        Initialize the main simulator.

        Args:
            parameter_config_path: Path to JSON parameter configuration file
            parameter_config: Direct parameter configuration dict (alternative to path)

        Note: Must provide either parameter_config_path OR parameter_config
        """
        if parameter_config_path is None and parameter_config is None:
            raise ValueError("Must provide either parameter_config_path or parameter_config")

        # Load configuration if path provided
        if parameter_config_path:
            config_data, _ = load_and_expand_config(parameter_config_path)
            self.config_name = config_data['config_name']
            self.config_description = config_data['description']
            parameter_config = config_data['parameters']
        else:
            self.config_name = "custom"
            self.config_description = "Custom configuration"

        self.data_manager = SimulationDataManager()
        self.config_optimizer = ConfigurationOptimizer(parameter_config)
        self.parallel_runner = ParallelSimulationRunner()
        self.results_analyzer = ResultsAnalyzer()
        self.parameter_config = parameter_config

    def run_complete_analysis(self) -> str:
        """Run complete simulation analysis from start to finish"""

        print(">> Starting Draft Simulation Analysis")
        print(f">> Configuration: {self.config_name}")
        print(f">> Description: {self.config_description}")
        print("=" * 50)

        try:
            # Step 1: Verify static simulation data files exist
            print(">> Verifying simulation data files...")
            self.data_manager.setup_simulation_data()

            # Step 2: Load player data
            print(">> Loading player data...")
            players_projected_df = self.data_manager.get_players_projected_data()
            players_actual_df = self.data_manager.get_players_actual_data()
            print(f"Loaded {len(players_projected_df)} projected players and {len(players_actual_df)} actual players")

            # Step 3: Generate preliminary configurations
            print(">> Generating preliminary configurations...")
            preliminary_configs = self.config_optimizer.generate_preliminary_configs()
            print(f"Generated {len(preliminary_configs)} preliminary configurations")

            # Step 4: Run preliminary simulations
            print(">> Running preliminary simulations...")
            preliminary_results = self.parallel_runner.run_preliminary_simulations(
                preliminary_configs,
                lambda config: self._run_single_complete_simulation(config, players_projected_df, players_actual_df)
            )

            # Step 5: Analyze preliminary results
            print(">> Analyzing preliminary results...")
            preliminary_config_results = []
            for config_key, result_data in preliminary_results.items():
                config_result = self.config_optimizer.analyze_config_performance(
                    result_data['config'],
                    result_data['results']
                )
                preliminary_config_results.append(config_result)

            self.config_optimizer.preliminary_results = preliminary_config_results

            # Step 6: Identify top configurations
            top_configs = self.config_optimizer.identify_top_configs(preliminary_config_results)
            print(f">> Identified {len(top_configs)} top configurations for full testing")

            # Step 7: Generate full configurations
            print(">> Generating full configurations...")
            full_configs = self.config_optimizer.generate_full_configs(top_configs)
            print(f"Generated {len(full_configs)} full configurations")

            # Step 8: Run full simulations
            print(">> Running full simulations...")
            full_results = self.parallel_runner.run_full_simulations(
                full_configs,
                lambda config: self._run_single_complete_simulation(config, players_projected_df, players_actual_df)
            )

            # Step 9: Analyze full results
            print(">> Analyzing full results...")
            full_config_results = []
            for config_key, result_data in full_results.items():
                config_result = self.config_optimizer.analyze_config_performance(
                    result_data['config'],
                    result_data['results']
                )
                full_config_results.append(config_result)

            self.config_optimizer.full_results = full_config_results

            # Step 10: Generate comprehensive analysis
            print(">> Generating comprehensive analysis...")
            analysis = self.results_analyzer.analyze_all_results(full_config_results)

            # Step 11: Save results
            print(">> Saving results...")

            # Ensure results directory exists
            os.makedirs(RESULTS_DIR, exist_ok=True)

            # Get timestamped results file path
            results_file_path = get_timestamped_results_file()
            self.results_analyzer.save_results_to_file(analysis, results_file_path)

            # Step 12: Cleanup
            print(">> Cleaning up...")
            # Note: Keep simulation data for potential future analysis
            # self.data_manager.cleanup_simulation_data()

            print(">> Simulation analysis completed successfully!")
            print(f">> Results saved to: {results_file_path}")

            return results_file_path

        except Exception as e:
            print(f">> Simulation failed: {e}")
            # Cleanup on failure
            try:
                self.data_manager.cleanup_simulation_data()
            except:
                pass
            raise

    def _run_single_complete_simulation(self, config_params: Dict[str, Any], players_projected_df: pd.DataFrame, players_actual_df: pd.DataFrame) -> Dict[str, Any]:
        """Run a single complete simulation (draft + season)"""

        try:
            # Create clean copies of both projected and actual data for this simulation
            simulation_players_projected_df = players_projected_df.copy()
            simulation_players_actual_df = players_actual_df.copy()

            # Reset drafted status for all players in both copies
            if 'drafted' in simulation_players_projected_df.columns:
                simulation_players_projected_df['drafted'] = 0
            if 'drafted' in simulation_players_actual_df.columns:
                simulation_players_actual_df['drafted'] = 0

            # Run draft simulation using projected data
            draft_engine = DraftSimulationEngine(simulation_players_projected_df, config_params)
            draft_results = draft_engine.run_complete_draft()

            # Extract teams from draft results
            simulation_teams = draft_engine.teams

            # Run season simulation with both projected and actual data
            season_simulator = SeasonSimulator(simulation_teams, simulation_players_projected_df, simulation_players_actual_df)
            season_results = season_simulator.simulate_full_season()

            # Combine results
            combined_results = {
                'user_team_index': draft_results['user_team_index'],
                'draft_results': draft_results,
                'season_stats': season_results['season_stats'],
                'team_rankings': season_results['team_rankings'],
                'total_matchups': season_results['total_matchups']
            }

            return combined_results

        except Exception as e:
            print(f"Error in single simulation: {e}")
            # Return default results to prevent total failure
            return {
                'user_team_index': 0,
                'draft_results': {},
                'season_stats': {},
                'team_rankings': [],
                'total_matchups': 0
            }

def run_simulation(parameter_config_path: str = None, parameter_config: Dict[str, List] = None) -> str:
    """
    Main entry point for running simulation.

    Args:
        parameter_config_path: Path to JSON parameter configuration file
        parameter_config: Direct parameter configuration dict (alternative to path)

    Returns:
        Path to the results file

    Note: Must provide either parameter_config_path OR parameter_config
    """
    simulator = MainSimulator(parameter_config_path=parameter_config_path, parameter_config=parameter_config)
    return simulator.run_complete_analysis()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # If config path provided as argument, use it
        config_path = sys.argv[1]
        print(f"Loading configuration from: {config_path}")
        run_simulation(parameter_config_path=config_path)
    else:
        print("Error: Must provide path to parameter configuration JSON file")
        print("Usage: python main_simulator.py <path_to_config.json>")
        sys.exit(1)