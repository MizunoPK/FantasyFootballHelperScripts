"""
Data management for simulation - handles copying and isolating data files.
"""

import os
import shutil
import pandas as pd
from typing import Optional
from .config import SOURCE_PLAYERS_CSV, PLAYERS_CSV_COPY, SIMULATION_DATA_DIR


class SimulationDataManager:
    """Manages data isolation for simulation runs"""

    def __init__(self):
        self.data_dir = SIMULATION_DATA_DIR
        self.players_csv_copy = PLAYERS_CSV_COPY
        self.source_players_csv = SOURCE_PLAYERS_CSV

    def setup_simulation_data(self) -> None:
        """Copy source data files to simulation directory"""
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)

        # Copy players.csv to simulation directory
        if os.path.exists(self.source_players_csv):
            shutil.copy2(self.source_players_csv, self.players_csv_copy)
            print(f"Copied {self.source_players_csv} to {self.players_csv_copy}")
        else:
            raise FileNotFoundError(f"Source players file not found: {self.source_players_csv}")

    def get_players_data(self) -> pd.DataFrame:
        """Load players data from simulation copy"""
        if not os.path.exists(self.players_csv_copy):
            self.setup_simulation_data()

        return pd.read_csv(self.players_csv_copy)

    def reset_players_data(self) -> None:
        """Reset players data to original state (clear drafted flags)"""
        players_df = self.get_players_data()

        # Reset drafted status for all players
        if 'drafted' in players_df.columns:
            players_df['drafted'] = 0

        # Save the reset data
        players_df.to_csv(self.players_csv_copy, index=False)

    def cleanup_simulation_data(self) -> None:
        """Clean up temporary simulation data files"""
        if os.path.exists(self.players_csv_copy):
            os.remove(self.players_csv_copy)
            print(f"Cleaned up simulation data: {self.players_csv_copy}")

    def verify_data_integrity(self) -> bool:
        """Verify that simulation data is properly isolated"""
        try:
            # Check that both files exist
            if not os.path.exists(self.source_players_csv):
                print(f"Warning: Source file missing: {self.source_players_csv}")
                return False

            if not os.path.exists(self.players_csv_copy):
                print(f"Warning: Simulation copy missing: {self.players_csv_copy}")
                return False

            # Load both files and compare basic structure
            source_df = pd.read_csv(self.source_players_csv)
            sim_df = pd.read_csv(self.players_csv_copy)

            # Check that they have the same columns and number of rows
            if list(source_df.columns) != list(sim_df.columns):
                print("Warning: Column mismatch between source and simulation data")
                return False

            if len(source_df) != len(sim_df):
                print("Warning: Row count mismatch between source and simulation data")
                return False

            return True

        except Exception as e:
            print(f"Error verifying data integrity: {e}")
            return False