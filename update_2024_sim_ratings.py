#!/usr/bin/env python3
"""
Update 2024 Simulation Data with Position-Specific Player Ratings

This script recalculates the player_rating column in the 2024 simulation data
using position-specific rankings instead of overall draft rankings.

Author: Claude Code
Date: 2025-11-03
"""

import pandas as pd
import sys
from pathlib import Path
from typing import Dict


def convert_positional_rank_to_rating(positional_rank: float) -> float:
    """
    Convert position-specific rank to 0-100 rating scale.

    Uses same 6-tier formula as espn_client.py implementation.

    Args:
        positional_rank: Rank within position (1.0 = best)

    Returns:
        Rating on 0-100 scale
    """
    # Tier 1: Elite (Rank 1-2)
    if positional_rank <= 2.0:
        # 100 for rank 1, 97.5 for rank 2
        return 100.0 - (positional_rank - 1.0) * 2.5

    # Tier 2: Top-5 (Rank 2-5)
    elif positional_rank <= 5.0:
        # 94.0 to 80.0
        return 94.0 - (positional_rank - 2.0) * 4.67

    # Tier 3: Quality starters (Rank 6-12)
    elif positional_rank <= 12.0:
        # 80.0 to 66.0
        return 80.0 - (positional_rank - 5.0) * 2.0

    # Tier 4: Flex/Bye-week (Rank 13-24)
    elif positional_rank <= 24.0:
        # 66.0 to 50.0
        return 66.0 - (positional_rank - 12.0) * 1.33

    # Tier 5: Deep bench (Rank 25-50)
    elif positional_rank <= 50.0:
        # 50.0 to 30.0
        return 50.0 - (positional_rank - 24.0) * 0.77

    # Tier 6: Waiver wire (Rank 51+)
    else:
        # 30.0 down to floor of 10.0
        rating = 30.0 - (positional_rank - 50.0) * 0.2
        return max(10.0, rating)


def calculate_positional_ranks(df: pd.DataFrame) -> Dict[str, Dict[int, float]]:
    """
    Calculate position-specific ranks based on ADP.

    Args:
        df: DataFrame with player data

    Returns:
        Dict mapping position -> player_index -> positional_rank
    """
    positional_ranks = {}

    # Standard fantasy positions
    positions = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST', 'DST']

    for position in positions:
        # Filter players at this position with valid ADP
        pos_players = df[
            (df['position'] == position) &
            (df['average_draft_position'].notna())
        ].copy()

        if len(pos_players) == 0:
            continue

        # Sort by ADP (lower ADP = better = lower rank)
        pos_players = pos_players.sort_values('average_draft_position')

        # Assign positional ranks (1-indexed)
        position_dict = {}
        for rank, (idx, _) in enumerate(pos_players.iterrows(), start=1):
            position_dict[idx] = float(rank)

        positional_ranks[position] = position_dict

    return positional_ranks


def update_player_ratings(input_file: Path, output_file: Path, backup: bool = True):
    """
    Update player ratings in simulation data using position-specific rankings.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        backup: Whether to create backup of original file
    """
    print("=" * 70)
    print("Update 2024 Simulation Data - Position-Specific Player Ratings")
    print("=" * 70)
    print()

    # Validate input file exists
    if not input_file.exists():
        print(f"❌ Error: Input file not found: {input_file}")
        sys.exit(1)

    # Create backup if requested
    if backup:
        backup_file = input_file.parent / f"{input_file.stem}_backup{input_file.suffix}"
        print(f"📦 Creating backup: {backup_file}")
        import shutil
        shutil.copy2(input_file, backup_file)
        print(f"   ✓ Backup created")
        print()

    # Read CSV
    print(f"📖 Reading file: {input_file}")
    df = pd.read_csv(input_file)
    print(f"   ✓ Loaded {len(df)} players")
    print()

    # Calculate position-specific ranks
    print("🔢 Calculating position-specific ranks...")
    positional_ranks = calculate_positional_ranks(df)

    total_ranked = sum(len(ranks) for ranks in positional_ranks.values())
    print(f"   ✓ Calculated ranks for {total_ranked} players across {len(positional_ranks)} positions")

    # Show position breakdown
    for position in ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST', 'DST']:
        if position in positional_ranks:
            count = len(positional_ranks[position])
            print(f"      • {position}: {count} players")
    print()

    # Update player ratings
    print("✏️  Updating player_rating values...")
    old_ratings = df['player_rating'].copy()
    updates_count = 0

    for position, ranks in positional_ranks.items():
        for idx, positional_rank in ranks.items():
            new_rating = convert_positional_rank_to_rating(positional_rank)
            df.at[idx, 'player_rating'] = new_rating
            updates_count += 1

    print(f"   ✓ Updated {updates_count} player ratings")
    print()

    # Show sample comparisons
    print("📊 Sample Rating Changes:")
    print("-" * 70)
    print(f"{'Player':<25} {'Pos':<5} {'ADP':>7} {'Old':>7} {'New':>7} {'Change':>8}")
    print("-" * 70)

    # Show top 3 players from each major position
    for position in ['QB', 'RB', 'WR', 'TE']:
        pos_players = df[df['position'] == position].nlargest(3, 'player_rating')
        for _, player in pos_players.iterrows():
            idx = player.name
            old_val = old_ratings[idx] if pd.notna(old_ratings[idx]) else 0.0
            new_val = player['player_rating'] if pd.notna(player['player_rating']) else 0.0
            change = new_val - old_val

            print(f"{player['name']:<25} {player['position']:<5} "
                  f"{player['average_draft_position']:>7.1f} "
                  f"{old_val:>7.2f} {new_val:>7.2f} "
                  f"{change:>+8.2f}")
    print()

    # Calculate statistics
    valid_old = old_ratings[old_ratings.notna()]
    valid_new = df['player_rating'][df['player_rating'].notna()]

    print("📈 Rating Statistics:")
    print(f"   Before: Mean={valid_old.mean():.2f}, Min={valid_old.min():.2f}, Max={valid_old.max():.2f}")
    print(f"   After:  Mean={valid_new.mean():.2f}, Min={valid_new.min():.2f}, Max={valid_new.max():.2f}")
    print()

    # Write output
    print(f"💾 Writing updated data to: {output_file}")
    df.to_csv(output_file, index=False)
    print(f"   ✓ File written successfully")
    print()

    print("=" * 70)
    print("✅ Update Complete!")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("1. Verify the output file looks correct")
    print("2. Run a test simulation to ensure compatibility")
    print("3. If satisfied, the updated data is ready to use")
    print()
    if backup:
        print(f"Note: Original file backed up to {backup_file.name}")


def main():
    """Main entry point."""
    # Default paths
    input_file = Path("simulation/sim_data/players_projected.csv")
    output_file = input_file  # Overwrite by default

    # Check if custom path provided
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])

    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])

    # Run update
    update_player_ratings(input_file, output_file, backup=True)


if __name__ == "__main__":
    main()
