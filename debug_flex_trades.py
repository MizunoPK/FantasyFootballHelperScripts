#!/usr/bin/env python3
"""
Debug why FLEX trades aren't being selected
"""

import pandas as pd
import sys
import os

# Add the draft_helper directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared_files'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'draft_helper'))

from FantasyPlayer import FantasyPlayer
from FantasyTeam import FantasyTeam
import draft_helper_constants as Constants

def debug_flex_trades():
    # Load player data
    players_file = "shared_files/players.csv"
    df = pd.read_csv(players_file)

    # Create FantasyPlayer objects
    all_players = []
    for _, row in df.iterrows():
        try:
            if row['position'] == 'UNKNOWN':  # Skip invalid positions
                continue
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

    # Separate into roster and available players
    roster_players = [p for p in all_players if p.drafted == 2]
    available_players = [p for p in all_players if p.drafted == 0]

    # Create team
    team = FantasyTeam(roster_players)

    print("=== CURRENT ROSTER COMPOSITION ===")
    print(f"Current position counts: {team.pos_counts}")
    print(f"Max positions allowed: {Constants.MAX_POSITIONS}")

    # Find the specific players we want to test
    brian_robinson = next((p for p in roster_players if p.name == "Brian Robinson Jr."), None)
    keenan_allen = next((p for p in available_players if p.name == "Keenan Allen"), None)
    michael_pittman = next((p for p in roster_players if p.name == "Michael Pittman Jr."), None)
    rhamondre_stevenson = next((p for p in available_players if p.name == "Rhamondre Stevenson"), None)

    print("\n=== TESTING SPECIFIC TRADES ===")

    if brian_robinson and keenan_allen:
        print(f"\n1. Testing Brian Robinson Jr. (RB, {brian_robinson.fantasy_points:.1f} pts) -> Keenan Allen (WR, {keenan_allen.fantasy_points:.1f} pts)")
        can_trade = team._can_replace_player(brian_robinson, keenan_allen)
        print(f"   Can replace? {can_trade}")
        if can_trade:
            improvement = keenan_allen.fantasy_points - brian_robinson.fantasy_points
            print(f"   Improvement: {improvement:.1f} pts")
            print(f"   Meets min threshold ({Constants.MIN_TRADE_IMPROVEMENT})? {improvement >= Constants.MIN_TRADE_IMPROVEMENT}")
        else:
            print("   BLOCKED by _can_replace_player logic!")

    if brian_robinson and rhamondre_stevenson:
        print(f"\n2. Testing Brian Robinson Jr. (RB, {brian_robinson.fantasy_points:.1f} pts) -> Rhamondre Stevenson (RB, {rhamondre_stevenson.fantasy_points:.1f} pts)")
        can_trade = team._can_replace_player(brian_robinson, rhamondre_stevenson)
        print(f"   Can replace? {can_trade}")
        if can_trade:
            improvement = rhamondre_stevenson.fantasy_points - brian_robinson.fantasy_points
            print(f"   Improvement: {improvement:.1f} pts")
            print(f"   Meets min threshold ({Constants.MIN_TRADE_IMPROVEMENT})? {improvement >= Constants.MIN_TRADE_IMPROVEMENT}")

    if michael_pittman and rhamondre_stevenson:
        print(f"\n3. Testing Michael Pittman Jr. (WR, {michael_pittman.fantasy_points:.1f} pts) -> Rhamondre Stevenson (RB, {rhamondre_stevenson.fantasy_points:.1f} pts)")
        can_trade = team._can_replace_player(michael_pittman, rhamondre_stevenson)
        print(f"   Can replace? {can_trade}")
        if can_trade:
            improvement = rhamondre_stevenson.fantasy_points - michael_pittman.fantasy_points
            print(f"   Improvement: {improvement:.1f} pts")
            print(f"   Meets min threshold ({Constants.MIN_TRADE_IMPROVEMENT})? {improvement >= Constants.MIN_TRADE_IMPROVEMENT}")

    if michael_pittman and keenan_allen:
        print(f"\n4. Testing Michael Pittman Jr. (WR, {michael_pittman.fantasy_points:.1f} pts) -> Keenan Allen (WR, {keenan_allen.fantasy_points:.1f} pts)")
        can_trade = team._can_replace_player(michael_pittman, keenan_allen)
        print(f"   Can replace? {can_trade}")
        if can_trade:
            improvement = keenan_allen.fantasy_points - michael_pittman.fantasy_points
            print(f"   Improvement: {improvement:.1f} pts")
            print(f"   Meets min threshold ({Constants.MIN_TRADE_IMPROVEMENT})? {improvement >= Constants.MIN_TRADE_IMPROVEMENT}")

    # Analyze which players are counted as FLEX vs regular position
    print("\n=== FLEX POSITION ANALYSIS ===")
    rb_count = 0
    wr_count = 0
    flex_count = 0

    for player in roster_players:
        if player.position == 'RB':
            if rb_count < Constants.MAX_POSITIONS['RB']:
                rb_count += 1
                print(f"  {player.name} (RB): Regular RB slot")
            else:
                flex_count += 1
                print(f"  {player.name} (RB): FLEX slot")
        elif player.position == 'WR':
            if wr_count < Constants.MAX_POSITIONS['WR']:
                wr_count += 1
                print(f"  {player.name} (WR): Regular WR slot")
            else:
                flex_count += 1
                print(f"  {player.name} (WR): FLEX slot")

    print(f"\nCalculated counts: RB={rb_count}, WR={wr_count}, FLEX={flex_count}")
    print(f"Team counts: {team.pos_counts}")

if __name__ == "__main__":
    debug_flex_trades()