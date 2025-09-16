#!/usr/bin/env python3
"""
Simple analysis to understand why FLEX trades aren't showing up
"""

import pandas as pd
import sys
import os

# Add the draft_helper directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared_files'))

from FantasyPlayer import FantasyPlayer

def analyze_flex_opportunities():
    # Load player data
    players_file = "shared_files/players.csv"
    df = pd.read_csv(players_file)

    # Create FantasyPlayer objects
    all_players = []
    for _, row in df.iterrows():
        try:
            player = FantasyPlayer(
                id=str(row['id']),
                name=row['name'],
                team=row['team'],
                position=row['position'],
                bye_week=row['bye_week'],
                fantasy_points=float(row['fantasy_points']),
                injury_status=row['injury_status'],
                drafted=row['drafted']
            )
            all_players.append(player)
        except Exception as e:
            print(f"Error processing player {row.get('name', 'Unknown')}: {e}")
            continue

    # Separate into roster (drafted=2) and available (drafted=0) players
    roster_players = [p for p in all_players if p.drafted == 2]
    available_players = [p for p in all_players if p.drafted == 0]

    print("=== CURRENT ROSTER ANALYSIS ===")
    roster_rb = [p for p in roster_players if p.position == 'RB']
    roster_wr = [p for p in roster_players if p.position == 'WR']

    print(f"\nCurrent Roster RBs ({len(roster_rb)}):")
    for rb in sorted(roster_rb, key=lambda x: x.fantasy_points, reverse=True):
        print(f"  {rb.name}: {rb.fantasy_points:.1f} pts")

    print(f"\nCurrent Roster WRs ({len(roster_wr)}):")
    for wr in sorted(roster_wr, key=lambda x: x.fantasy_points, reverse=True):
        print(f"  {wr.name}: {wr.fantasy_points:.1f} pts")

    print("\n=== TOP AVAILABLE PLAYERS ===")
    available_rb = [p for p in available_players if p.position == 'RB']
    available_wr = [p for p in available_players if p.position == 'WR']

    print(f"\nTop 10 Available RBs:")
    top_rb = sorted(available_rb, key=lambda x: x.fantasy_points, reverse=True)[:10]
    for rb in top_rb:
        print(f"  {rb.name}: {rb.fantasy_points:.1f} pts")

    print(f"\nTop 10 Available WRs:")
    top_wr = sorted(available_wr, key=lambda x: x.fantasy_points, reverse=True)[:10]
    for wr in top_wr:
        print(f"  {wr.name}: {wr.fantasy_points:.1f} pts")

    print("\n=== FLEX TRADE ANALYSIS ===")
    # Find the weakest RB and WR on roster
    weakest_rb = min(roster_rb, key=lambda x: x.fantasy_points) if roster_rb else None
    weakest_wr = min(roster_wr, key=lambda x: x.fantasy_points) if roster_wr else None

    if weakest_rb and available_wr:
        best_available_wr = max(available_wr, key=lambda x: x.fantasy_points)
        print(f"\nBest FLEX swap opportunity (RB -> WR):")
        print(f"  OUT: {weakest_rb.name} ({weakest_rb.fantasy_points:.1f} pts)")
        print(f"  IN:  {best_available_wr.name} ({best_available_wr.fantasy_points:.1f} pts)")
        print(f"  Net improvement: {best_available_wr.fantasy_points - weakest_rb.fantasy_points:.1f} pts")

    if weakest_wr and available_rb:
        best_available_rb = max(available_rb, key=lambda x: x.fantasy_points)
        print(f"\nBest FLEX swap opportunity (WR -> RB):")
        print(f"  OUT: {weakest_wr.name} ({weakest_wr.fantasy_points:.1f} pts)")
        print(f"  IN:  {best_available_rb.name} ({best_available_rb.fantasy_points:.1f} pts)")
        print(f"  Net improvement: {best_available_rb.fantasy_points - weakest_wr.fantasy_points:.1f} pts")

if __name__ == "__main__":
    analyze_flex_opportunities()