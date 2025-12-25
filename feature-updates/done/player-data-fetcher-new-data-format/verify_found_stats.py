#!/usr/bin/env python3
"""
Verify the newly discovered stat IDs with real player data

FOUND STATS:
- stat_20: passingInterceptions (NOT stat_14!)
- stat_114: kickoffReturnYards
- stat_115: puntReturnYards
- stat_98: defensiveSafeties
- stat_74-82: Distance-based field goals (weekly!)
- stat_86-88: Extra points (NOT 80-81!)

Author: Claude AI
Date: 2024-12-24
"""

import asyncio
import httpx

ESPN_BASE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/1"
ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ESPN_FANTASY_FILTER = '{"players":{"limit":2000,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'


async def fetch_week(week: int) -> dict:
    """Fetch player data for a week"""
    headers = {'User-Agent': ESPN_USER_AGENT, 'X-Fantasy-Filter': ESPN_FANTASY_FILTER}
    params = {'scoringPeriodId': week, 'view': 'kona_player_info'}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(ESPN_BASE_URL, headers=headers, params=params)
        return response.json() if response.status_code == 200 else {}


def find_player(player_id: int, week: int, data: dict):
    """Find player stats for a specific week"""
    for p in data.get('players', []):
        if p.get('player', {}).get('id') == player_id:
            for stat in p['player'].get('stats', []):
                if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
                    return {
                        'name': p['player'].get('fullName'),
                        'stats': stat.get('stats', {})
                    }
    return None


async def main():
    print("="*80)
    print("VERIFICATION: Newly Discovered Stat IDs")
    print("="*80)

    # TEST 1: Interceptions (stat_20)
    print("\n[TEST 1: Interceptions - stat_20]")
    print("Testing: Sam Darnold Week 15 (3 INTs known)")
    week15 = await fetch_week(15)
    # Search for Sam Darnold
    for p in week15.get('players', [])[:100]:
        player = p.get('player', {})
        if 'Darnold' in player.get('fullName', ''):
            for stat in player.get('stats', []):
                if stat.get('scoringPeriodId') == 15 and stat.get('statSourceId') == 0:
                    stats = stat.get('stats', {})
                    print(f"  Found: {player.get('fullName')}")
                    print(f"  stat_14: {stats.get('14', 'NOT FOUND')}")
                    print(f"  stat_20: {stats.get('20', 'NOT FOUND')}  <-- Should be 3")
                    break
            break

    # TEST 2: Return Yards (stat_114, stat_115)
    print("\n[TEST 2: Return Yards - stat_114 (KR), stat_115 (PR)]")
    print("Searching for players with return stats in Week 14...")
    week14 = await fetch_week(14)
    found_returns = []
    for p in week14.get('players', [])[:300]:
        player = p.get('player', {})
        for stat in player.get('stats', []):
            if stat.get('scoringPeriodId') == 14 and stat.get('statSourceId') == 0:
                stats = stat.get('stats', {})
                kr_yds = stats.get('114', 0)
                pr_yds = stats.get('115', 0)
                if kr_yds > 0 or pr_yds > 0:
                    found_returns.append({
                        'name': player.get('fullName'),
                        'kr_yds': kr_yds,
                        'pr_yds': pr_yds
                    })
                if len(found_returns) >= 5:
                    break
        if len(found_returns) >= 5:
            break

    for r in found_returns:
        print(f"  {r['name']}: KR={r['kr_yds']:.0f} yds, PR={r['pr_yds']:.0f} yds")

    # TEST 3: Safety (stat_98)
    print("\n[TEST 3: Safety - stat_98]")
    print("Searching for D/ST with safeties in 2024...")
    # Check multiple weeks
    for week in [5, 8, 12]:
        week_data = await fetch_week(week)
        for p in week_data.get('players', []):
            player = p.get('player', {})
            if player.get('defaultPositionId') == 16:  # DST
                for stat in player.get('stats', []):
                    if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
                        stats = stat.get('stats', {})
                        safeties = stats.get('98', 0)
                        if safeties > 0:
                            print(f"  Week {week}: {player.get('fullName')} - {safeties:.0f} safety(ies)")

    # TEST 4: Distance FG Stats (stat_74-82)
    print("\n[TEST 4: Distance-Based Field Goals]")
    print("Testing: Brandon Aubrey Week 14")
    # Find Brandon Aubrey
    for p in week14.get('players', []):
        player = p.get('player', {})
        if 'Aubrey' in player.get('fullName', ''):
            for stat in player.get('stats', []):
                if stat.get('scoringPeriodId') == 14 and stat.get('statSourceId') == 0:
                    stats = stat.get('stats', {})
                    print(f"  Found: {player.get('fullName')}")
                    print(f"  stat_74 (50+ made): {stats.get('74', 'NOT FOUND')}")
                    print(f"  stat_75 (50+ att): {stats.get('75', 'NOT FOUND')}")
                    print(f"  stat_77 (40-49 made): {stats.get('77', 'NOT FOUND')}")
                    print(f"  stat_80 (U40 made): {stats.get('80', 'NOT FOUND')}")
                    print(f"  stat_83 (Total FG made): {stats.get('83', 'NOT FOUND')}")
                    print(f"  stat_86 (XP made): {stats.get('86', 'NOT FOUND')}")
                    break
            break

    print("\n" + "="*80)
    print("VERIFICATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
