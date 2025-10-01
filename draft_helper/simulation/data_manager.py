"""
Data management for simulation - handles verification and loading of static data files.
"""

import os
import pandas as pd
from typing import Optional, Tuple

# Add parent directory to path for imports
import sys
from pathlib import Path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config import SIMULATION_DATA_DIR


class SimulationDataManager:
    """Manages data isolation for simulation runs"""

    def __init__(self):
        self.data_dir = SIMULATION_DATA_DIR

        # Source file paths
        self.source_players_csv = os.path.join(os.path.dirname(__file__), '..', '..', 'shared_files', 'players.csv')
        self.source_teams_csv = os.path.join(os.path.dirname(__file__), '..', '..', 'shared_files', 'teams.csv')

        # Projected data file paths (for draft decisions and lineup optimization)
        self.players_projected_csv = os.path.join(self.data_dir, 'players_projected.csv')

        # Actual data file paths (for final scoring)
        self.players_actual_csv = os.path.join(self.data_dir, 'players_actual.csv')

        # Weekly teams data file paths (for positional rankings)
        # Week 0: Draft phase (preseason rankings baseline)
        # Weeks 1-4: Early season with regression adjustments
        # Weeks 5-18: Season phase with actual team performance data
        self.teams_weekly_csvs = {}
        self.teams_weekly_csvs[0] = os.path.join(self.data_dir, 'teams_week_0.csv')  # Draft phase
        for week in range(1, 19):  # Weeks 1-18 now have separate files
            self.teams_weekly_csvs[week] = os.path.join(self.data_dir, f'teams_week_{week}.csv')

    def setup_simulation_data(self, force_refresh: bool = False) -> None:
        """Verify that static simulation data files exist in the data directory

        Args:
            force_refresh: Unused parameter kept for backward compatibility
        """
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)

        # Verify required player files exist
        missing_files = []
        if not os.path.exists(self.players_projected_csv):
            missing_files.append(self.players_projected_csv)
        if not os.path.exists(self.players_actual_csv):
            missing_files.append(self.players_actual_csv)

        # Verify all weekly teams files exist
        for week, weekly_teams_path in self.teams_weekly_csvs.items():
            if not os.path.exists(weekly_teams_path):
                missing_files.append(weekly_teams_path)

        # Raise error if any files are missing
        if missing_files:
            error_msg = "Required simulation data files are missing:\n"
            for file in missing_files:
                error_msg += f"  - {file}\n"
            error_msg += "\nPlease ensure all static simulation data files are present in the data directory."
            raise FileNotFoundError(error_msg)

        print(f"Verified all simulation data files exist: {len(self.teams_weekly_csvs) + 2} files total")

    def get_players_projected_data(self) -> pd.DataFrame:
        """Load projected players data for draft decisions and lineup optimization"""
        if not os.path.exists(self.players_projected_csv):
            raise FileNotFoundError(f"Projected players file not found: {self.players_projected_csv}. Please ensure simulation data is properly initialized.")
        return pd.read_csv(self.players_projected_csv)

    def get_players_actual_data(self) -> pd.DataFrame:
        """Load actual players data for final scoring"""
        if not os.path.exists(self.players_actual_csv):
            raise FileNotFoundError(f"Actual players file not found: {self.players_actual_csv}. Please ensure simulation data is properly initialized.")
        return pd.read_csv(self.players_actual_csv)

    def get_teams_weekly_data(self, week: int) -> pd.DataFrame:
        """Load teams data for a specific week (0-18)

        Args:
            week: Week number (0 for draft phase, 1-18 for season phase)

        Returns:
            DataFrame with teams data for the specified week

        Note:
            Week 0: Draft phase (preseason rankings baseline)
            Weeks 1-4: Early season with regression adjustments from preseason
            Weeks 5-18: Full season data with actual team performance
        """
        if week not in range(0, 19):
            raise ValueError(f"Week must be between 0 and 18, got {week}")

        # All weeks now have their own data files
        weekly_teams_path = self.teams_weekly_csvs[week]
        if not os.path.exists(weekly_teams_path):
            raise FileNotFoundError(f"Weekly teams file not found: {weekly_teams_path}. Please ensure simulation data is properly initialized.")
        return pd.read_csv(weekly_teams_path)

    def get_draft_teams_data(self) -> pd.DataFrame:
        """Load teams data for draft phase (week 0)"""
        return self.get_teams_weekly_data(0)

    def get_players_data(self) -> pd.DataFrame:
        """Load projected players data (legacy compatibility)"""
        return self.get_players_projected_data()

    def reset_players_data(self) -> None:
        """Reset players data to original state (clear drafted flags) for both projected and actual"""
        # Reset projected data
        players_projected_df = self.get_players_projected_data()
        if 'drafted' in players_projected_df.columns:
            players_projected_df['drafted'] = 0
        players_projected_df.to_csv(self.players_projected_csv, index=False)

        # Reset actual data
        players_actual_df = self.get_players_actual_data()
        if 'drafted' in players_actual_df.columns:
            players_actual_df['drafted'] = 0
        players_actual_df.to_csv(self.players_actual_csv, index=False)

    def cleanup_simulation_data(self) -> None:
        """Clean up temporary simulation data files"""
        files_to_remove = [
            self.players_projected_csv,
            self.players_actual_csv
        ]

        # Add all weekly teams files
        files_to_remove.extend(self.teams_weekly_csvs.values())

        for file_path in files_to_remove:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleaned up simulation data: {file_path}")

    def verify_data_integrity(self) -> bool:
        """Verify that all required static simulation data files exist"""
        try:
            # Check that all simulation files exist
            simulation_files = [
                self.players_projected_csv,
                self.players_actual_csv
            ]

            # Add all weekly teams files
            simulation_files.extend(self.teams_weekly_csvs.values())

            for sim_file in simulation_files:
                if not os.path.exists(sim_file):
                    print(f"Warning: Simulation file missing: {sim_file}")
                    return False

            # Verify players files have consistent structure
            projected_df = pd.read_csv(self.players_projected_csv)
            actual_df = pd.read_csv(self.players_actual_csv)

            if list(projected_df.columns) != list(actual_df.columns):
                print("Warning: Column mismatch between projected and actual player files")
                return False

            if len(projected_df) != len(actual_df):
                print("Warning: Row count mismatch between projected and actual player files")
                return False

            # Verify all weekly teams files have consistent structure
            expected_columns = None
            for week, teams_file in self.teams_weekly_csvs.items():
                teams_df = pd.read_csv(teams_file)
                if expected_columns is None:
                    expected_columns = list(teams_df.columns)
                elif list(teams_df.columns) != expected_columns:
                    print(f"Warning: Column mismatch in {teams_file}")
                    return False

            return True

        except Exception as e:
            print(f"Error verifying data integrity: {e}")
            return False