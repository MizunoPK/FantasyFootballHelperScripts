#!/usr/bin/env python3
"""
Generate players_week1.csv from players.csv and players_projected.csv

This script creates a combined CSV file that:
- Takes id, name, team, position, bye_week, average_draft_position from players.csv
- Takes week_1_points through week_17_points from players_projected.csv
- Sets default values: drafted=0, locked=0, injury_status='ACTIVE'
- Calculates fantasy_points as sum of all week columns
- Calculates player_rating based on ADP normalization per position (0-100 scale)

Usage:
    python generate_players_week1.py

Output:
    data/players_week1.csv

Author: Kai Mizuno
"""

import sys
from pathlib import Path

import pandas as pd

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from utils.LoggingManager import setup_logger, get_logger


def calculate_position_rating(adp_series: pd.Series) -> pd.Series:
    """
    Calculate player_rating based on ADP within a position group.

    Formula: rating = 100 * (max_adp - player_adp) / (max_adp - min_adp)
    - Lowest ADP (best player) = 100
    - Highest ADP (worst player) = 0

    Args:
        adp_series: Series of average_draft_position values for a position group

    Returns:
        Series of player_rating values (0-100 scale)
    """
    min_adp = adp_series.min()
    max_adp = adp_series.max()

    # Handle edge case: all players have same ADP
    if min_adp == max_adp:
        return pd.Series([50.0] * len(adp_series), index=adp_series.index)

    return 100 * (max_adp - adp_series) / (max_adp - min_adp)


def generate_players_week1(
    players_path: Path,
    projected_path: Path,
    output_path: Path
) -> pd.DataFrame:
    """
    Generate players_week1.csv combining data from players.csv and players_projected.csv.

    Args:
        players_path: Path to players.csv
        projected_path: Path to players_projected.csv
        output_path: Path to write output CSV

    Returns:
        DataFrame containing the generated data
    """
    logger = get_logger()

    # Week column names
    week_cols = [f'week_{i}_points' for i in range(1, 18)]

    # Step 1: Load source files
    logger.info(f"Loading {players_path.name}...")
    players_df = pd.read_csv(players_path)
    logger.info(f"  Loaded {len(players_df)} players")

    logger.info(f"Loading {projected_path.name}...")
    projected_df = pd.read_csv(projected_path)
    logger.info(f"  Loaded {len(projected_df)} projections")

    # Step 2: Merge on 'id' - select only required columns from each
    logger.info("Merging data...")
    players_cols = ['id', 'name', 'team', 'position', 'bye_week', 'average_draft_position']
    projected_cols = ['id'] + week_cols

    merged = players_df[players_cols].merge(
        projected_df[projected_cols],
        on='id',
        how='inner'
    )
    logger.info(f"  Merged {len(merged)} rows")

    # Step 3: Calculate fantasy_points (sum of weeks from projected data)
    logger.info("Calculating fantasy_points...")
    merged['fantasy_points'] = merged[week_cols].sum(axis=1)

    # Step 4: Set default values
    logger.info("Setting default values...")
    merged['injury_status'] = 'ACTIVE'
    merged['drafted'] = 0
    merged['locked'] = 0

    # Step 5: Calculate player_rating per position
    logger.info("Calculating player_rating per position...")
    merged['player_rating'] = merged.groupby('position')['average_draft_position'].transform(
        calculate_position_rating
    )

    # Log rating ranges per position
    for position in merged['position'].unique():
        pos_df = merged[merged['position'] == position]
        min_r = pos_df['player_rating'].min()
        max_r = pos_df['player_rating'].max()
        logger.info(f"  {position}: rating range {min_r:.2f} - {max_r:.2f}")

    # Step 6: Select columns in exact order (matching players.csv)
    output_cols = [
        'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
        'injury_status', 'drafted', 'locked', 'average_draft_position', 'player_rating'
    ] + week_cols

    output_df = merged[output_cols]

    # Step 7: Write to CSV
    logger.info(f"Writing {output_path.name}...")
    output_df.to_csv(output_path, index=False)
    logger.info(f"  Wrote {len(output_df)} rows to {output_path}")

    return output_df


def main():
    """Main execution function."""
    # Setup logging
    logger = setup_logger(name="generate_players_week1", level="INFO")
    logger.info("=" * 60)
    logger.info("Generate players_week1.csv")
    logger.info("=" * 60)

    # Define paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    players_path = data_dir / "players.csv"
    projected_path = data_dir / "players_projected.csv"
    output_path = data_dir / "players_week1.csv"

    # Validate input files exist
    if not players_path.exists():
        logger.error(f"File not found: {players_path}")
        return 1

    if not projected_path.exists():
        logger.error(f"File not found: {projected_path}")
        return 1

    # Generate the file
    try:
        output_df = generate_players_week1(players_path, projected_path, output_path)

        # Summary
        logger.info("=" * 60)
        logger.info("GENERATION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Output file: {output_path}")
        logger.info(f"Total players: {len(output_df)}")
        logger.info(f"Fantasy points range: {output_df['fantasy_points'].min():.2f} - {output_df['fantasy_points'].max():.2f}")
        logger.info(f"Player rating range: {output_df['player_rating'].min():.2f} - {output_df['player_rating'].max():.2f}")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"Error generating file: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
