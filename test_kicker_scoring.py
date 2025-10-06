#!/usr/bin/env python3
"""
Test script to compare scoring for Brandon McManus vs Chase McLaughlin
"""
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(name)s - %(message)s'
)

from draft_helper.draft_helper import DraftHelper
from shared_files.FantasyPlayer import FantasyPlayer

def main():
    print("="*80)
    print("KICKER SCORING COMPARISON - WAIVER OPTIMIZER MODE")
    print("="*80)

    # Initialize draft helper with correct path
    draft_helper = DraftHelper("shared_files/players.csv")

    # Find the two kickers
    mcmanus = None
    mclaughlin = None

    for player in draft_helper.players:
        if player.name == "Brandon McManus":
            mcmanus = player
        elif player.name == "Chase McLaughlin":
            mclaughlin = player

    if not mcmanus:
        print("ERROR: Could not find Brandon McManus")
        return

    if not mclaughlin:
        print("ERROR: Could not find Chase McLaughlin")
        return

    print(f"\nFound players:")
    print(f"1. {mcmanus.name} ({mcmanus.team}) - Fantasy Points: {mcmanus.fantasy_points:.2f}")
    print(f"   ADP: {mcmanus.average_draft_position}, Player Rating: {mcmanus.player_rating}")
    print(f"   Bye Week: {mcmanus.bye_week}, Injury: {mcmanus.injury_status}")
    print(f"   Drafted Status: {mcmanus.drafted}, Locked: {mcmanus.locked}")

    print(f"\n2. {mclaughlin.name} ({mclaughlin.team}) - Fantasy Points: {mclaughlin.fantasy_points:.2f}")
    print(f"   ADP: {mclaughlin.average_draft_position}, Player Rating: {mclaughlin.player_rating}")
    print(f"   Bye Week: {mclaughlin.bye_week}, Injury: {mclaughlin.injury_status}")
    print(f"   Drafted Status: {mclaughlin.drafted}, Locked: {mclaughlin.locked}")

    print("\n" + "="*80)
    print("SCORING BREAKDOWN - WAIVER OPTIMIZER MODE (score_player_for_trade)")
    print("="*80)

    # Score both players using the trade/waiver scoring function
    print(f"\n{'Brandon McManus':=^80}")
    mcmanus_score = draft_helper.score_player_for_trade(mcmanus)

    print(f"\n{'Chase McLaughlin':=^80}")
    mclaughlin_score = draft_helper.score_player_for_trade(mclaughlin)

    # Summary
    print("\n" + "="*80)
    print("FINAL SCORES SUMMARY")
    print("="*80)
    print(f"Brandon McManus:   {mcmanus_score:.2f} pts")
    print(f"Chase McLaughlin:  {mclaughlin_score:.2f} pts")
    print(f"Difference:        {abs(mcmanus_score - mclaughlin_score):.2f} pts")

    if mcmanus_score > mclaughlin_score:
        print(f"\nWinner: Brandon McManus (+{mcmanus_score - mclaughlin_score:.2f} pts)")
    else:
        print(f"\nWinner: Chase McLaughlin (+{mclaughlin_score - mcmanus_score:.2f} pts)")

    # Show consistency categories
    print(f"\nConsistency Categories:")
    print(f"Brandon McManus:   {getattr(mcmanus, 'consistency_category', 'N/A')}")
    print(f"Chase McLaughlin:  {getattr(mclaughlin, 'consistency_category', 'N/A')}")

if __name__ == "__main__":
    main()
