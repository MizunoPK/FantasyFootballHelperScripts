#!/usr/bin/env python3
"""
Simulation Player Rating Normalization Script

One-time script to normalize player_rating values in simulation CSV files.
Replaces tier-based ratings with position-specific normalized ratings (1-100 scale).

This script:
1. Reads players_projected_backup.csv and players_actual_backup.csv
2. Calculates min/max player_rating for each position
3. Normalizes ratings to 1-100 scale (100=best, 1=worst within position)
4. Writes new players_projected.csv and players_actual.csv files

Author: Kai Mizuno
Date: 2025-11-05
"""

import sys
from pathlib import Path
import pandas as pd
from typing import Dict, Tuple

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import setup_logger, get_logger
from utils.error_handler import error_context, DataProcessingError, FileOperationError


def calculate_position_ranges(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate min/max player_rating for each position.

    Args:
        df: DataFrame with 'position' and 'player_rating' columns

    Returns:
        Dict mapping position to {'min': float, 'max': float, 'count': int}

    Example:
        {'QB': {'min': 65.5, 'max': 97.3, 'count': 25}, ...}
    """
    logger = get_logger()
    position_ranges = {}

    # Group by position and calculate ranges
    for position in df['position'].unique():
        position_df = df[df['position'] == position]

        # Filter out NaN/None player_rating values
        valid_ratings = position_df['player_rating'].dropna()

        if len(valid_ratings) == 0:
            logger.warning(f"Position {position} has no valid player_rating values, skipping")
            continue

        min_rating = float(valid_ratings.min())
        max_rating = float(valid_ratings.max())
        count = len(valid_ratings)

        position_ranges[position] = {
            'min': min_rating,
            'max': max_rating,
            'count': count
        }

        logger.info(f"  {position}: {min_rating:.1f}-{max_rating:.1f} ({count} players)")

        # Validation: min should be <= max
        if min_rating > max_rating:
            raise DataProcessingError(
                f"Invalid range for {position}: min ({min_rating}) > max ({max_rating})"
            )

    return position_ranges


def normalize_rating(rating: float, min_val: float, max_val: float) -> float:
    """
    Normalize a rating to 1-100 scale.

    Formula: normalized = 1 + ((rating - max_val) / (min_val - max_val)) * 99
    This gives: min_val (best) → 100, max_val (worst) → 1

    Args:
        rating: Original rating value
        min_val: Minimum rating for position (best player)
        max_val: Maximum rating for position (worst player)

    Returns:
        Normalized rating (1-100 scale)

    Raises:
        DataProcessingError: If rating is outside valid range
    """
    # Handle division by zero (all players have same rating)
    if min_val == max_val:
        return 50.0  # Neutral rating

    # Apply normalization formula
    normalized = 1 + ((rating - max_val) / (min_val - max_val)) * 99

    # Validation: ensure result is within expected range
    if not (0.5 <= normalized <= 100.5):  # Allow 0.5 tolerance for floating point
        raise DataProcessingError(
            f"Normalized rating out of range: {normalized:.2f} "
            f"(original={rating}, min={min_val}, max={max_val})"
        )

    # Clamp to exact range
    return max(1.0, min(100.0, normalized))


def normalize_csv_file(
    input_path: Path,
    output_path: Path,
    position_ranges: Dict[str, Dict[str, float]]
) -> Tuple[int, int]:
    """
    Normalize player_rating values in a CSV file.

    Args:
        input_path: Path to input CSV (backup file)
        output_path: Path to output CSV (normalized file)
        position_ranges: Position min/max ranges from calculate_position_ranges()

    Returns:
        Tuple of (normalized_count, fallback_count)
    """
    logger = get_logger()

    logger.info(f"Reading {input_path.name}...")
    df = pd.read_csv(input_path)

    logger.info(f"  Total rows: {len(df)}")

    normalized_count = 0
    fallback_count = 0

    # Normalize each player's rating
    for idx, row in df.iterrows():
        position = row['position']
        original_rating = row['player_rating']

        # Skip players with no rating
        if pd.isna(original_rating):
            fallback_count += 1
            continue

        # Get min/max for this position
        if position not in position_ranges:
            logger.warning(
                f"Position {position} not in ranges for player {row.get('name', 'unknown')}, "
                f"preserving original rating"
            )
            fallback_count += 1
            continue

        min_val = position_ranges[position]['min']
        max_val = position_ranges[position]['max']

        # Normalize the rating
        try:
            normalized = normalize_rating(original_rating, min_val, max_val)
            df.at[idx, 'player_rating'] = normalized
            normalized_count += 1

            # Log extreme ratings for visibility
            if normalized >= 99.5 or normalized <= 1.5:
                logger.debug(
                    f"Extreme rating for {row.get('name', 'unknown')} ({position}): "
                    f"{normalized:.1f} (original={original_rating:.1f})"
                )
        except DataProcessingError as e:
            logger.error(f"Error normalizing rating for {row.get('name', 'unknown')}: {e}")
            fallback_count += 1
            continue

    # Write output CSV
    logger.info(f"Writing {output_path.name}...")
    df.to_csv(output_path, index=False)
    logger.info(f"  Wrote {len(df)} rows to {output_path}")

    return normalized_count, fallback_count


def main():
    """Main execution function."""
    # Setup logging
    logger = setup_logger(name="normalize_player_ratings", level="INFO")
    logger.info("=" * 60)
    logger.info("Simulation Player Rating Normalization Script")
    logger.info("=" * 60)

    # Define paths
    script_dir = Path(__file__).parent
    sim_data_dir = script_dir / "sim_data"

    projected_backup = sim_data_dir / "players_projected_backup.csv"
    actual_backup = sim_data_dir / "players_actual_backup.csv"
    projected_output = sim_data_dir / "players_projected.csv"
    actual_output = sim_data_dir / "players_actual.csv"

    logger.info(f"Data directory: {sim_data_dir}")

    # Validate input files exist
    with error_context("validate_input_files", component="normalize_player_ratings"):
        if not projected_backup.exists():
            raise FileOperationError(f"Backup file not found: {projected_backup}")
        if not actual_backup.exists():
            raise FileOperationError(f"Backup file not found: {actual_backup}")

        logger.info("✓ Input files found")

    # Step 1: Read backup files and calculate position ranges
    logger.info("\nStep 1: Calculating position ranges from backup files")
    logger.info("-" * 60)

    with error_context("calculate_ranges", component="normalize_player_ratings"):
        # Read both backup files
        df_projected = pd.read_csv(projected_backup)
        df_actual = pd.read_csv(actual_backup)

        logger.info(f"Projected backup: {len(df_projected)} rows")
        logger.info(f"Actual backup: {len(df_actual)} rows")

        # Validate required columns
        required_cols = ['id', 'position', 'player_rating']
        for col in required_cols:
            if col not in df_projected.columns:
                raise DataProcessingError(f"Missing column '{col}' in {projected_backup.name}")
            if col not in df_actual.columns:
                raise DataProcessingError(f"Missing column '{col}' in {actual_backup.name}")

        logger.info("✓ Required columns validated")

        # Calculate position ranges from projected data (use as source of truth)
        logger.info("\nPosition ranges (from projected backup):")
        position_ranges = calculate_position_ranges(df_projected)

        if len(position_ranges) == 0:
            raise DataProcessingError("No position ranges calculated (no valid data?)")

        logger.info(f"✓ Calculated ranges for {len(position_ranges)} positions")

    # Step 2: Normalize projected CSV
    logger.info("\nStep 2: Normalizing players_projected.csv")
    logger.info("-" * 60)

    with error_context("normalize_projected", component="normalize_player_ratings"):
        proj_norm_count, proj_fallback_count = normalize_csv_file(
            projected_backup,
            projected_output,
            position_ranges
        )

        logger.info(f"✓ Normalized {proj_norm_count} players, {proj_fallback_count} using fallback/None")

    # Step 3: Normalize actual CSV
    logger.info("\nStep 3: Normalizing players_actual.csv")
    logger.info("-" * 60)

    with error_context("normalize_actual", component="normalize_player_ratings"):
        actual_norm_count, actual_fallback_count = normalize_csv_file(
            actual_backup,
            actual_output,
            position_ranges
        )

        logger.info(f"✓ Normalized {actual_norm_count} players, {actual_fallback_count} using fallback/None")

    # Step 4: Validation
    logger.info("\nStep 4: Validating output files")
    logger.info("-" * 60)

    with error_context("validate_output", component="normalize_player_ratings"):
        # Read output files
        df_proj_out = pd.read_csv(projected_output)
        df_actual_out = pd.read_csv(actual_output)

        # Check all normalized ratings are within 1-100
        proj_ratings = df_proj_out['player_rating'].dropna()
        actual_ratings = df_actual_out['player_rating'].dropna()

        proj_out_of_range = ((proj_ratings < 1) | (proj_ratings > 100)).sum()
        actual_out_of_range = ((actual_ratings < 1) | (actual_ratings > 100)).sum()

        if proj_out_of_range > 0:
            logger.warning(f"Projected: {proj_out_of_range} ratings outside 1-100 range")
        if actual_out_of_range > 0:
            logger.warning(f"Actual: {actual_out_of_range} ratings outside 1-100 range")

        # Log summary stats
        logger.info(f"Projected ratings: min={proj_ratings.min():.1f}, max={proj_ratings.max():.1f}, mean={proj_ratings.mean():.1f}")
        logger.info(f"Actual ratings: min={actual_ratings.min():.1f}, max={actual_ratings.max():.1f}, mean={actual_ratings.mean():.1f}")

        logger.info("✓ Validation complete")

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("NORMALIZATION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Output files created:")
    logger.info(f"  - {projected_output}")
    logger.info(f"  - {actual_output}")
    logger.info(f"\nStatistics:")
    logger.info(f"  Projected: {proj_norm_count} normalized, {proj_fallback_count} fallback/None")
    logger.info(f"  Actual: {actual_norm_count} normalized, {actual_fallback_count} fallback/None")
    logger.info("=" * 60)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger = get_logger()
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
