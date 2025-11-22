#!/usr/bin/env python3
"""
Fix team assignments in simulation data files using Week 1 2024 historical data.

This script reads the Week 1 historical data to get correct team assignments
and updates players_actual.csv with those assignments.
"""

import csv
from pathlib import Path

# Paths
HISTORICAL_DATA_PATH = Path("/home/kai/code/NFL-Data/NFL-data-Players/2024/1")
SIM_DATA_PATH = Path(__file__).parent / "sim_data"

# Position files to read from historical data
POSITION_FILES = ["QB.csv", "RB.csv", "WR.csv", "TE.csv", "K.csv"]

# Team bye weeks for 2024 season
BYE_WEEKS_2024 = {
    "ARI": 11, "ATL": 12, "BAL": 14, "BUF": 12, "CAR": 11, "CHI": 7,
    "CIN": 12, "CLE": 10, "DAL": 7, "DEN": 14, "DET": 5, "GB": 10,
    "HOU": 14, "IND": 14, "JAX": 12, "KC": 6, "LAC": 5, "LAR": 6,
    "LV": 10, "MIA": 6, "MIN": 6, "NE": 14, "NO": 12, "NYG": 11,
    "NYJ": 12, "PHI": 5, "PIT": 9, "SEA": 10, "SF": 9, "TB": 11,
    "TEN": 5, "WSH": 14
}


def normalize_name(name):
    """Normalize player name for matching."""
    # Remove suffixes like Jr., Sr., III, etc.
    name = name.strip()
    for suffix in [' Jr.', ' Sr.', ' III', ' II', ' IV', ' V']:
        name = name.replace(suffix, '')
    # Handle special cases
    name = name.replace("'", "'")  # Normalize apostrophes
    return name.lower().strip()


def load_week1_team_mappings():
    """Load player name to team mappings from Week 1 historical data."""
    player_teams = {}

    for pos_file in POSITION_FILES:
        filepath = HISTORICAL_DATA_PATH / pos_file
        if not filepath.exists():
            print(f"Warning: {filepath} not found")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                player_name = row.get('PlayerName', '')
                team = row.get('Team', '')
                if player_name and team:
                    normalized = normalize_name(player_name)
                    player_teams[normalized] = team

    print(f"Loaded {len(player_teams)} player-team mappings from Week 1 data")
    return player_teams


def fix_players_file(filepath, player_teams):
    """Fix team assignments in a players CSV file."""
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return 0

    # Read all rows
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Track changes
    changes = []
    not_found = []

    for row in rows:
        player_id = row.get('id', '')
        old_team = row.get('team', '')
        player_name = row.get('name', '')
        normalized_name = normalize_name(player_name)

        if normalized_name in player_teams:
            new_team = player_teams[normalized_name]
            if old_team != new_team:
                changes.append({
                    'name': player_name,
                    'id': player_id,
                    'old_team': old_team,
                    'new_team': new_team
                })
                row['team'] = new_team
                # Also update bye week
                if new_team in BYE_WEEKS_2024:
                    row['bye_week'] = str(BYE_WEEKS_2024[new_team])
        else:
            # Player not found in Week 1 data (might be DST or not active Week 1)
            if not player_name.endswith('D/ST'):
                not_found.append(f"{player_name} ({player_id})")

    # Write updated file
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Report changes
    print(f"\nFixed {len(changes)} team assignments in {filepath.name}:")
    for change in changes:
        print(f"  {change['name']}: {change['old_team']} -> {change['new_team']}")

    if not_found and len(not_found) <= 20:
        print(f"\nPlayers not found in Week 1 data ({len(not_found)}):")
        for player in not_found[:20]:
            print(f"  {player}")
    elif not_found:
        print(f"\n{len(not_found)} players not found in Week 1 data (showing first 10):")
        for player in not_found[:10]:
            print(f"  {player}")

    return len(changes)


def main():
    print("=" * 60)
    print("Fixing Team Assignments Using Week 1 2024 Data")
    print("=" * 60)

    # Load Week 1 team mappings
    player_teams = load_week1_team_mappings()

    if not player_teams:
        print("Error: No player-team mappings loaded")
        return

    # Fix players_actual.csv
    actual_path = SIM_DATA_PATH / "players_actual.csv"
    actual_changes = fix_players_file(actual_path, player_teams)

    # Check if players_projected.csv exists
    projected_path = SIM_DATA_PATH / "players_projected.csv"
    if projected_path.exists():
        projected_changes = fix_players_file(projected_path, player_teams)
    else:
        projected_changes = 0
        print(f"\n{projected_path.name} not found, skipping")

    print("\n" + "=" * 60)
    print(f"Total changes: {actual_changes + projected_changes}")
    print("=" * 60)
    print("\nDon't forget to regenerate team_data by running:")
    print("  python simulation/generate_team_data.py")


if __name__ == "__main__":
    main()
