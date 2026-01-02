"""
Update Player ADP Values Script

Updates all player ADP values across all simulation weeks (108 files total).
Loads FantasyPros 2025 ADP data and updates simulation player data files.

Usage:
    python update_adp_values.py

Author: Epic fix_2025_adp
Created: 2026-01-01
"""

from pathlib import Path
from utils.adp_csv_loader import load_adp_from_csv
from utils.adp_updater import update_player_adp_values


def main():
    """Main function to update all player ADP values."""

    # Paths
    csv_path = Path("feature-updates/FantasyPros_2025_Overall_ADP_Rankings.csv")
    sim_data_folder = Path("simulation/sim_data/2025/weeks")

    # Verify CSV exists
    if not csv_path.exists():
        print(f"ERROR: CSV file not found at {csv_path}")
        print("Please ensure FantasyPros_2025_Overall_ADP_Rankings.csv exists")
        return 1

    # Verify simulation folder exists
    if not sim_data_folder.exists():
        print(f"ERROR: Simulation data folder not found at {sim_data_folder}")
        return 1

    print("="*80)
    print("ADP VALUE UPDATE - ALL WEEKS")
    print("="*80)

    # Load CSV data
    print(f"\nLoading ADP data from CSV: {csv_path}")
    try:
        adp_df = load_adp_from_csv(csv_path)
        print(f"✓ Loaded {len(adp_df)} players from CSV")
    except Exception as e:
        print(f"ERROR loading CSV: {e}")
        return 1

    # Update all player files across all 18 weeks
    print(f"\nUpdating player ADP values...")
    print(f"Target: {sim_data_folder}")
    print(f"Files to update: 108 (18 weeks × 6 positions)")
    print()

    try:
        report = update_player_adp_values(adp_df, sim_data_folder)
    except Exception as e:
        print(f"ERROR during update: {e}")
        return 1

    # Print comprehensive summary
    print("\n" + "="*80)
    print("UPDATE COMPLETE")
    print("="*80)

    summary = report['summary']
    print(f"\nTotal JSON players processed: {summary['total_json_players']}")
    print(f"Matched players: {summary['matched']}")
    print(f"Unmatched JSON players: {summary['unmatched_json']}")
    print(f"Unmatched CSV players: {summary['unmatched_csv']}")

    match_rate = (summary['matched'] / summary['total_json_players'] * 100) if summary['total_json_players'] > 0 else 0
    print(f"Match rate: {match_rate:.1f}%")

    print("\nConfidence Distribution:")
    for conf_range, count in report['confidence_distribution'].items():
        print(f"  {conf_range}: {count}")

    # Show unmatched players if any
    if report['unmatched_json_players']:
        print(f"\nUnmatched JSON Players ({len(report['unmatched_json_players'])}):")
        for player in report['unmatched_json_players'][:10]:  # Show first 10
            print(f"  - {player['name']} ({player['position']}) - ADP: {player['adp']}")
        if len(report['unmatched_json_players']) > 10:
            print(f"  ... and {len(report['unmatched_json_players']) - 10} more")

    if report['unmatched_csv_players']:
        print(f"\nUnmatched CSV Players ({len(report['unmatched_csv_players'])}):")
        for player in report['unmatched_csv_players'][:10]:  # Show first 10
            print(f"  - {player['name']} ({player['position']}) - ADP: {player['adp']}")
        if len(report['unmatched_csv_players']) > 10:
            print(f"  ... and {len(report['unmatched_csv_players']) - 10} more")

    print("\n" + "="*80)
    print("All player files have been updated successfully!")
    print("="*80)

    return 0


if __name__ == '__main__':
    exit(main())
