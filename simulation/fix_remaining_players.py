#!/usr/bin/env python3
"""
Find team assignments for players not found in Week 1 by searching other weeks.
"""

import csv
from pathlib import Path

# Paths
HISTORICAL_DATA_PATH = Path("/home/kai/code/NFL-Data/NFL-data-Players/2024")
SIM_DATA_PATH = Path(__file__).parent / "sim_data"

# Position files to read
POSITION_FILES = ["QB.csv", "RB.csv", "WR.csv", "TE.csv", "K.csv"]

# Team bye weeks for 2024 season
BYE_WEEKS_2024 = {
    "ARI": 11, "ATL": 12, "BAL": 14, "BUF": 12, "CAR": 11, "CHI": 7,
    "CIN": 12, "CLE": 10, "DAL": 7, "DEN": 14, "DET": 5, "GB": 10,
    "HOU": 14, "IND": 14, "JAX": 12, "KC": 6, "LAC": 5, "LAR": 6,
    "LV": 10, "MIA": 6, "MIN": 6, "NE": 14, "NO": 12, "NYG": 11,
    "NYJ": 12, "PHI": 5, "PIT": 9, "SEA": 10, "SF": 9, "TB": 11,
    "TEN": 5, "WSH": 14, "WAS": 14, "FA": 0
}


def normalize_name(name):
    """Normalize player name for matching."""
    name = name.strip()
    for suffix in [' Jr.', ' Sr.', ' III', ' II', ' IV', ' V']:
        name = name.replace(suffix, '')
    name = name.replace("'", "'")
    return name.lower().strip()


def load_week1_players():
    """Load player names from Week 1 data."""
    week1_players = set()
    week1_path = HISTORICAL_DATA_PATH / "1"

    for pos_file in POSITION_FILES:
        filepath = week1_path / pos_file
        if not filepath.exists():
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('PlayerName', '')
                if name:
                    week1_players.add(normalize_name(name))

    return week1_players


def find_player_in_other_weeks(player_name):
    """Search weeks 2-17 for a player's team."""
    normalized = normalize_name(player_name)

    for week in range(2, 18):
        week_path = HISTORICAL_DATA_PATH / str(week)
        if not week_path.exists():
            continue

        for pos_file in POSITION_FILES:
            filepath = week_path / pos_file
            if not filepath.exists():
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get('PlayerName', '')
                    if normalize_name(name) == normalized:
                        team = row.get('Team', '')
                        return team, week

    return None, None


def main():
    print("=" * 60)
    print("Finding Team Assignments for Remaining Players")
    print("=" * 60)

    # Load Week 1 players
    week1_players = load_week1_players()
    print(f"Loaded {len(week1_players)} players from Week 1\n")

    # Load players_actual.csv
    actual_path = SIM_DATA_PATH / "players_actual.csv"
    with open(actual_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Find players not in Week 1
    not_found = []
    for row in rows:
        player_name = row.get('name', '')
        if player_name.endswith('D/ST'):
            continue
        normalized = normalize_name(player_name)
        if normalized not in week1_players:
            not_found.append(row)

    print(f"Found {len(not_found)} players not in Week 1 data\n")

    # Search other weeks for each player
    changes = []
    still_not_found = []

    for row in not_found:
        player_name = row.get('name', '')
        old_team = row.get('team', '')

        new_team, week_found = find_player_in_other_weeks(player_name)

        if new_team:
            if old_team != new_team:
                changes.append({
                    'name': player_name,
                    'old_team': old_team,
                    'new_team': new_team,
                    'week_found': week_found
                })
                row['team'] = new_team
                if new_team in BYE_WEEKS_2024:
                    row['bye_week'] = str(BYE_WEEKS_2024[new_team])
            else:
                print(f"  {player_name}: Already correct ({old_team}, found in week {week_found})")
        else:
            still_not_found.append(player_name)

    # Write updated file
    with open(actual_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Report
    print(f"\nFixed {len(changes)} team assignments:")
    for change in changes:
        print(f"  {change['name']}: {change['old_team']} -> {change['new_team']} (found in week {change['week_found']})")

    if still_not_found:
        print(f"\n{len(still_not_found)} players still not found in any week:")
        for name in still_not_found:
            print(f"  {name}")

    # Also update players_projected.csv
    projected_path = SIM_DATA_PATH / "players_projected.csv"
    if projected_path.exists():
        with open(projected_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            proj_fieldnames = reader.fieldnames
            proj_rows = list(reader)

        proj_changes = 0
        for row in proj_rows:
            player_name = row.get('name', '')
            normalized = normalize_name(player_name)

            # Check if this player was updated
            for change in changes:
                if normalize_name(change['name']) == normalized:
                    if row['team'] != change['new_team']:
                        row['team'] = change['new_team']
                        if change['new_team'] in BYE_WEEKS_2024:
                            row['bye_week'] = str(BYE_WEEKS_2024[change['new_team']])
                        proj_changes += 1
                    break

        with open(projected_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=proj_fieldnames)
            writer.writeheader()
            writer.writerows(proj_rows)

        print(f"\nAlso fixed {proj_changes} assignments in players_projected.csv")

    print("\n" + "=" * 60)
    print("Don't forget to regenerate team_data:")
    print("  python simulation/generate_team_data.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
