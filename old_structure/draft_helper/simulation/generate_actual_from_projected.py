#!/usr/bin/env python3
"""
Generate Realistic Actual Player Data from Projected Data

This script creates a realistic "actual" performance dataset by applying
statistical variation to projected data. This simulates real-world variance
where actual performance differs from projections.

Usage:
    python generate_actual_from_projected.py

Input:
    - data/players_projected.csv (ESPN projections)

Output:
    - data/players_actual.csv (Simulated actual performance with variance)

Variance Model:
    - Player quality affects variance (elite players more consistent)
    - Position affects variance (RB/WR more volatile than QB)
    - Injury status affects availability
    - Bye weeks are respected
    - Total points adjusted by ±15-30% based on player tier
"""

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def apply_actual_variance(projected_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply realistic variance to projected data to simulate actual performance.

    Strategy:
    - Elite players (rating >= 90): ±10-20% variance, high consistency
    - Good players (rating 70-89): ±15-25% variance, moderate consistency
    - Average players (rating 50-69): ±20-35% variance, lower consistency
    - Low players (rating < 50): ±25-50% variance, very inconsistent

    Position variance:
    - QB: Lower variance (more predictable)
    - RB: Higher variance (injury prone, usage dependent)
    - WR: Moderate-high variance (target dependent)
    - TE: Moderate variance (fewer targets but more consistent)
    - K: Low variance (relatively consistent)
    - DST: High variance (matchup dependent)
    """

    actual_df = projected_df.copy()

    # Seed for reproducibility
    np.random.seed(42)

    # Week columns
    week_cols = [f'week_{i}_points' for i in range(1, 18)]

    for idx, row in actual_df.iterrows():
        position = row['position']
        rating = row.get('player_rating', 50.0)
        injury_status = row.get('injury_status', 'ACTIVE')

        # Determine variance range based on player quality
        if rating >= 90:
            base_variance = 0.15  # ±15%
            consistency_factor = 0.85  # More consistent
        elif rating >= 70:
            base_variance = 0.20  # ±20%
            consistency_factor = 0.75
        elif rating >= 50:
            base_variance = 0.275  # ±27.5%
            consistency_factor = 0.65
        else:
            base_variance = 0.375  # ±37.5%
            consistency_factor = 0.50  # Very inconsistent

        # Position-specific variance multipliers
        position_multipliers = {
            'QB': 0.8,   # More consistent
            'RB': 1.2,   # More volatile
            'WR': 1.1,   # Moderately volatile
            'TE': 0.9,   # Moderately consistent
            'K': 0.7,    # Quite consistent
            'DST': 1.3   # Very volatile
        }

        position_mult = position_multipliers.get(position, 1.0)
        final_variance = base_variance * position_mult

        # Apply weekly variance
        weekly_actuals = []
        for week_col in week_cols:
            projected_points = row[week_col]

            if pd.isna(projected_points) or projected_points == 0:
                actual_points = 0.0
            else:
                # Generate variance: some weeks over, some under projection
                # Use beta distribution for realistic skew
                variance_pct = np.random.beta(2, 2) * 2 - 1  # Range: -1 to +1
                variance_pct *= final_variance

                actual_points = projected_points * (1 + variance_pct)

                # Add injury volatility
                if injury_status == 'OUT':
                    # OUT players: 80% chance of 0 points
                    if np.random.random() < 0.8:
                        actual_points = 0.0
                elif injury_status == 'DOUBTFUL':
                    # DOUBTFUL: 60% chance of 0, 40% chance of reduced points
                    if np.random.random() < 0.6:
                        actual_points = 0.0
                    else:
                        actual_points *= 0.5  # Half points if they play
                elif injury_status == 'QUESTIONABLE':
                    # QUESTIONABLE: 20% chance of missing, otherwise slight reduction
                    if np.random.random() < 0.2:
                        actual_points = 0.0
                    else:
                        actual_points *= 0.9  # 90% of expected

                # Ensure non-negative
                actual_points = max(0.0, actual_points)

            weekly_actuals.append(actual_points)

        # Update actual weekly points
        for week_col, actual_val in zip(week_cols, weekly_actuals):
            actual_df.at[idx, week_col] = actual_val

        # Calculate new total fantasy points
        actual_df.at[idx, 'fantasy_points'] = sum(weekly_actuals)

    return actual_df


def main():
    """Generate actual data from projected data"""

    script_dir = Path(__file__).parent
    data_dir = script_dir / 'data'

    projected_file = data_dir / 'players_projected.csv'
    actual_file = data_dir / 'players_actual.csv'

    # Check if projected file exists
    if not projected_file.exists():
        print(f"ERROR: Projected file not found: {projected_file}")
        print("Please run the player data fetcher first to generate projected data.")
        sys.exit(1)

    print(f"Loading projected data from: {projected_file}")
    projected_df = pd.read_csv(projected_file)
    print(f"Loaded {len(projected_df)} players")

    print("\nApplying realistic variance to generate actual performance data...")
    actual_df = apply_actual_variance(projected_df)

    # Calculate statistics
    projected_total = projected_df['fantasy_points'].sum()
    actual_total = actual_df['fantasy_points'].sum()
    variance_pct = ((actual_total - projected_total) / projected_total) * 100

    print(f"\nGenerated actual data statistics:")
    print(f"  Projected total points: {projected_total:,.2f}")
    print(f"  Actual total points: {actual_total:,.2f}")
    print(f"  Overall variance: {variance_pct:+.2f}%")

    # Sample comparison
    print("\nSample player comparison (top 5 by projected points):")
    top_5_idx = projected_df.nlargest(5, 'fantasy_points').index
    for idx in top_5_idx:
        name = projected_df.loc[idx, 'name']
        proj_pts = projected_df.loc[idx, 'fantasy_points']
        actual_pts = actual_df.loc[idx, 'fantasy_points']
        diff_pct = ((actual_pts - proj_pts) / proj_pts) * 100
        print(f"  {name}: {proj_pts:.1f} → {actual_pts:.1f} ({diff_pct:+.1f}%)")

    # Save actual data
    print(f"\nSaving actual data to: {actual_file}")
    actual_df.to_csv(actual_file, index=False)

    print("\nDone! Actual data file generated successfully.")
    print("\nNOTE: This is simulated actual data with realistic variance.")
    print("For production use, you would need true historical performance data.")


if __name__ == "__main__":
    main()
