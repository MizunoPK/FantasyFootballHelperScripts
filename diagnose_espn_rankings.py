#!/usr/bin/env python3
"""
Diagnostic script to inspect ESPN API rankings data structure.
This will help identify if ESPN changed their API format.
"""

import asyncio
import httpx
import json
import sys
from pathlib import Path

# Add player-data-fetcher to path
sys.path.append(str(Path(__file__).parent / "player-data-fetcher"))

from config import ESPN_USER_AGENT, CURRENT_NFL_WEEK, NFL_SEASON

async def fetch_player_data(player_id: str, player_name: str):
    """Fetch and inspect ESPN data for a specific player"""

    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{NFL_SEASON}/segments/0/leaguedefaults/3"

    params = {
        'view': 'kona_player_info',
        'scoringPeriodId': 0  # Get all data
    }

    headers = {
        'User-Agent': ESPN_USER_AGENT,
        'X-Fantasy-Filter': f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
    }

    print(f"\n{'='*80}")
    print(f"Fetching data for {player_name} (ID: {player_id})")
    print(f"Current Week: {CURRENT_NFL_WEEK}, Season: {NFL_SEASON}")
    print(f"{'='*80}\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        players = data.get('players', [])
        if not players:
            print(f"❌ No player data found for ID {player_id}")
            return

        player_info = players[0].get('player', {})

        # Extract key fields
        print(f"Player Name: {player_info.get('firstName', '')} {player_info.get('lastName', '')}")
        print(f"Position ID: {player_info.get('defaultPositionId')}")
        print(f"Team ID: {player_info.get('proTeamId')}")

        # Check draft rankings
        print(f"\n📊 DRAFT RANKINGS:")
        draft_ranks = player_info.get('draftRanksByRankType', {})
        if draft_ranks:
            for rank_type, rank_data in draft_ranks.items():
                print(f"  {rank_type}: {rank_data}")
        else:
            print("  ❌ No draft rankings found")

        # Check ROS rankings (this is what's likely broken)
        print(f"\n📈 ROS RANKINGS (player_info['rankings']):")
        rankings = player_info.get('rankings', {})

        if rankings:
            print(f"  Available weeks: {list(rankings.keys())}")

            # Show current week rankings
            current_week_key = str(CURRENT_NFL_WEEK)
            print(f"\n  Week {CURRENT_NFL_WEEK} rankings (key='{current_week_key}'):")
            current_week_rankings = rankings.get(current_week_key, [])

            if current_week_rankings:
                for i, ranking in enumerate(current_week_rankings, 1):
                    print(f"    Entry {i}:")
                    print(f"      rankType: {ranking.get('rankType')}")
                    print(f"      slotId: {ranking.get('slotId')}")
                    print(f"      averageRank: {ranking.get('averageRank')}")
                    print(f"      rank: {ranking.get('rank')}")
                    print(f"      All keys: {list(ranking.keys())}")
            else:
                print(f"    ❌ No rankings found for week {CURRENT_NFL_WEEK}")

                # Try fallback weeks
                print(f"\n  Trying fallback weeks (working backwards from {CURRENT_NFL_WEEK}):")
                for fallback_week in range(CURRENT_NFL_WEEK - 1, 0, -1):
                    fallback_key = str(fallback_week)
                    fallback_rankings = rankings.get(fallback_key, [])
                    if fallback_rankings:
                        print(f"    ✅ Found rankings for week {fallback_week}")
                        for ranking in fallback_rankings[:1]:  # Show first entry only
                            print(f"       rankType: {ranking.get('rankType')}, averageRank: {ranking.get('averageRank')}")
                        break

                # Try week 0 (pre-season)
                preseason_rankings = rankings.get('0', [])
                if preseason_rankings:
                    print(f"\n    ✅ Found pre-season rankings (key='0'):")
                    for ranking in preseason_rankings[:1]:  # Show first entry only
                        print(f"       rankType: {ranking.get('rankType')}, averageRank: {ranking.get('averageRank')}")
        else:
            print("  ❌ No rankings object found at all")

        # Show full JSON structure for debugging
        print(f"\n🔍 FULL RANKINGS STRUCTURE (JSON):")
        print(json.dumps(rankings, indent=2))

async def main():
    """Test with multiple players to see the pattern"""

    # Test players (ID, Name)
    test_players = [
        ("4431459", "Tyler Warren"),  # TE - reported as having missing rankings
        ("4361741", "Patrick Mahomes"),  # QB - established player
        ("4241479", "Christian McCaffrey"),  # RB - established player
    ]

    for player_id, player_name in test_players:
        try:
            await fetch_player_data(player_id, player_name)
        except Exception as e:
            print(f"\n❌ Error fetching {player_name}: {e}")

        print("\n")  # Separator between players

if __name__ == "__main__":
    asyncio.run(main())
