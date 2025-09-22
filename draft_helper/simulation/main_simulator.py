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

from .data_manager import SimulationDataManager
from .config_optimizer import ConfigurationOptimizer
from .parallel_runner import ParallelSimulationRunner
from .results_analyzer import ResultsAnalyzer
from .simulation_engine import DraftSimulationEngine
from .season_simulator import SeasonSimulator
from .config import RESULTS_FILE

class MainSimulator:
    """Main orchestrator for draft simulation analysis"""

    def __init__(self):
        self.data_manager = SimulationDataManager()
        self.config_optimizer = ConfigurationOptimizer()
        self.parallel_runner = ParallelSimulationRunner()
        self.results_analyzer = ResultsAnalyzer()

    def run_complete_analysis(self) -> str:
        """Run complete simulation analysis from start to finish"""

        print("🚀 Starting Draft Simulation Analysis")
        print("=" * 50)

        try:
            # Step 1: Setup data
            print("📁 Setting up simulation data...")
            self.data_manager.setup_simulation_data()

            if not self.data_manager.verify_data_integrity():
                raise Exception("Data integrity check failed")

            # Step 2: Load player data
            print("📊 Loading player data...")
            players_df = self.data_manager.get_players_data()
            print(f"Loaded {len(players_df)} players")

            # Step 3: Generate preliminary configurations
            print("⚙️ Generating preliminary configurations...")
            preliminary_configs = self.config_optimizer.generate_preliminary_configs()
            print(f"Generated {len(preliminary_configs)} preliminary configurations")

            # Step 4: Run preliminary simulations
            print("🏃 Running preliminary simulations...")
            preliminary_results = self.parallel_runner.run_preliminary_simulations(
                preliminary_configs,
                lambda config: self._run_single_complete_simulation(config, players_df)
            )

            # Step 5: Analyze preliminary results
            print("📈 Analyzing preliminary results...")
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
            print(f"🎯 Identified {len(top_configs)} top configurations for full testing")

            # Step 7: Generate full configurations
            print("⚙️ Generating full configurations...")
            full_configs = self.config_optimizer.generate_full_configs(top_configs)
            print(f"Generated {len(full_configs)} full configurations")

            # Step 8: Run full simulations
            print("🏃‍♂️ Running full simulations...")
            full_results = self.parallel_runner.run_full_simulations(
                full_configs,
                lambda config: self._run_single_complete_simulation(config, players_df)
            )

            # Step 9: Analyze full results
            print("📊 Analyzing full results...")
            full_config_results = []
            for config_key, result_data in full_results.items():
                config_result = self.config_optimizer.analyze_config_performance(
                    result_data['config'],
                    result_data['results']
                )
                full_config_results.append(config_result)

            self.config_optimizer.full_results = full_config_results

            # Step 10: Generate comprehensive analysis
            print("🔍 Generating comprehensive analysis...")
            analysis = self.results_analyzer.analyze_all_results(full_config_results)

            # Step 11: Save results
            print("💾 Saving results...")
            self.results_analyzer.save_results_to_file(analysis, RESULTS_FILE)

            # Step 12: Cleanup
            print("🧹 Cleaning up...")
            # Note: Keep simulation data for potential future analysis
            # self.data_manager.cleanup_simulation_data()

            print("✅ Simulation analysis completed successfully!")
            print(f"📄 Results saved to: {RESULTS_FILE}")

            return RESULTS_FILE

        except Exception as e:
            print(f"❌ Simulation failed: {e}")
            # Cleanup on failure
            try:
                self.data_manager.cleanup_simulation_data()
            except:
                pass
            raise

    def _run_single_complete_simulation(self, config_params: Dict[str, Any], players_df: pd.DataFrame) -> Dict[str, Any]:
        """Run a single complete simulation (draft + season)"""

        try:
            # Reset players data for this simulation
            self.data_manager.reset_players_data()

            # Run draft simulation
            draft_engine = DraftSimulationEngine(players_df, config_params)
            draft_results = draft_engine.run_complete_draft()

            # Extract teams from draft results
            simulation_teams = draft_engine.teams

            # Run season simulation
            season_simulator = SeasonSimulator(simulation_teams)
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

def run_simulation() -> str:
    """Main entry point for running simulation"""

    simulator = MainSimulator()
    return simulator.run_complete_analysis()

if __name__ == "__main__":
    run_simulation()