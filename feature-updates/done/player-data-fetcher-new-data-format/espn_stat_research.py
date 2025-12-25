#!/usr/bin/env python3
"""
ESPN Stat ID Research Script

This script queries the ESPN API to discover missing stat IDs needed for the
new JSON format player data files.

Missing stats we're looking for:
- Fumbles (misc)
- 2-point conversions (misc)
- Return yards (misc)
- Return TDs (misc)
- Sacks (on QB - when QB gets sacked)
- Safety (defense)
- Defensive TDs (defense)

Author: Claude AI Research Assistant
Date: 2024-12-24
"""

import asyncio
import json
from pathlib import Path
import httpx

# ESPN API Configuration
ESPN_BASE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/{scoring_type}"
ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ESPN_FANTASY_FILTER = '{"players":{"limit":2000,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'

# Season configuration
SEASON = 2024
SCORING_TYPE = 1  # 1 = PPR
CURRENT_WEEK = 16

# Test players (chosen for specific stat types)
TEST_PLAYERS = {
    "QB_WITH_FUMBLES": {
        "name": "Daniel Jones",
        "id": 3917315,  # Known for fumbles
        "week": 8,
        "looking_for": ["fumbles", "sacks_taken", "2pt"]
    },
    "RB_WITH_FUMBLES": {
        "name": "Christian McCaffrey",
        "id": 3116593,
        "week": 1,
        "looking_for": ["fumbles", "2pt"]
    },
    "RETURNER": {
        "name": "Deebo Samuel",  # Known returner
        "id": 3116389,
        "week": 8,
        "looking_for": ["return_yards", "return_tds"]
    },
    "DST_WITH_SAFETY": {
        "name": "49ers D/ST",
        "id": 25,  # Team ID, not player ID
        "week": 8,
        "looking_for": ["safety", "defensive_tds"]
    }
}


async def fetch_all_players_week(week: int) -> dict:
    """Fetch all player data for a specific week"""
    url = ESPN_BASE_URL.format(season=SEASON, scoring_type=SCORING_TYPE)

    headers = {
        'User-Agent': ESPN_USER_AGENT,
        'X-Fantasy-Filter': ESPN_FANTASY_FILTER
    }

    params = {
        'scoringPeriodId': week,
        'view': 'kona_player_info'
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        print(f"\n[*] Fetching all players for Week {week}...")
        response = await client.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            print(f"[+] Fetched {len(data.get('players', []))} players")
            return data
        else:
            print(f"[-] Error: HTTP {response.status_code}")
            return {}


def find_player_stats(player_name: str, player_id: int, week: int, all_data: dict) -> dict:
    """Find specific player's stats in the full dataset"""
    for player_entry in all_data.get('players', []):
        player_info = player_entry.get('player', {})

        # Match by ID if provided, otherwise by name
        if player_id and player_info.get('id') == player_id:
            return extract_week_stats(player_info, week)
        elif player_info.get('fullName', '').lower() == player_name.lower():
            return extract_week_stats(player_info, week)

    return {}


def extract_week_stats(player_info: dict, week: int) -> dict:
    """Extract stats for a specific week from player data"""
    for stat_obj in player_info.get('stats', []):
        if stat_obj.get('scoringPeriodId') == week and stat_obj.get('statSourceId') == 0:
            return {
                'name': player_info.get('fullName'),
                'id': player_info.get('id'),
                'position': player_info.get('defaultPositionId'),
                'stats': stat_obj.get('stats', {}),
                'appliedTotal': stat_obj.get('appliedTotal', 0)
            }
    return {}


def analyze_unknown_stats(stats: dict, known_stats: dict) -> list:
    """Identify stats that are not yet documented"""
    unknown = []

    for stat_id, value in stats.items():
        if stat_id not in known_stats:
            unknown.append({
                'stat_id': stat_id,
                'value': value
            })

    return unknown


async def main():
    """Main research workflow"""

    # Known stats from our documentation
    KNOWN_STATS = {
        # Passing
        '0': 'Passing Attempts',
        '1': 'Completions',
        '2': 'Incompletions',
        '3': 'Passing Yards',
        '4': 'Passing TDs',
        '14': 'Interceptions Thrown',
        '21': 'Completion %',
        '22': 'Passing Yards (dup)',

        # Rushing
        '23': 'Rushing Attempts',
        '24': 'Rushing Yards',
        '25': 'Rushing TDs',
        '39': 'Yards Per Carry',
        '40': 'Rushing Yards (dup)',

        # Receiving
        '41': 'Receptions (dup)',
        '42': 'Receiving Yards',
        '43': 'Receiving TDs',
        '53': 'Receptions',
        '58': 'Targets',
        '60': 'Yards Per Reception',
        '61': 'Receiving Yards (dup)',

        # Kicking
        '80': 'Extra Points Made',
        '81': 'Extra Points Attempted',
        '83': 'Field Goals Made',
        '84': 'Field Goals Attempted',

        # Defense
        '95': 'Interceptions',
        '99': 'Fumbles Recovered',
        '106': 'Forced Fumbles',
        '107': 'Assisted Tackles',
        '108': 'Solo Tackles',
        '109': 'Total Tackles',
        '112': 'Sacks',
        '113': 'Passes Defensed',
        '118': 'Punt Returns',
        '120': 'Points Allowed',
        '127': 'Total Yards Allowed',
        '187': 'Points Allowed (dup)',

        # Participation
        '155': 'Game Played Flag',
        '156': 'Game Played Flag (dup)',
        '210': 'Game Participation',
    }

    print("=" * 80)
    print("ESPN STAT ID RESEARCH - Missing Stats Discovery")
    print("=" * 80)

    # Research Daniel Jones (QB with fumbles)
    print("\n[RESEARCH TARGET 1: QB with Fumbles (Daniel Jones)]")
    print("-" * 80)

    week_8_data = await fetch_all_players_week(8)
    daniel_jones_stats = find_player_stats("Daniel Jones", 3917315, 8, week_8_data)

    if daniel_jones_stats:
        print(f"\n[+] Found: {daniel_jones_stats['name']} (ID: {daniel_jones_stats['id']})")
        print(f"Fantasy Points: {daniel_jones_stats['appliedTotal']}")
        print("\n[All Stats:]")
        for stat_id, value in sorted(daniel_jones_stats['stats'].items(), key=lambda x: int(x[0])):
            known_name = KNOWN_STATS.get(stat_id, "??? UNKNOWN")
            print(f"  stat_{stat_id}: {value:>8.1f}  ->  {known_name}")

        unknown = analyze_unknown_stats(daniel_jones_stats['stats'], KNOWN_STATS)
        if unknown:
            print(f"\n[*] Found {len(unknown)} unknown stats - potential fumbles/sacks candidates:")
            for u in unknown:
                print(f"  stat_{u['stat_id']}: {u['value']}")

    # Research Christian McCaffrey (RB with fumbles)
    print("\n\n[RESEARCH TARGET 2: RB with Fumbles (Christian McCaffrey)]")
    print("-" * 80)

    week_1_data = await fetch_all_players_week(1)
    cmc_stats = find_player_stats("Christian McCaffrey", 3116593, 1, week_1_data)

    if cmc_stats:
        print(f"\n[+] Found: {cmc_stats['name']} (ID: {cmc_stats['id']})")
        print(f"Fantasy Points: {cmc_stats['appliedTotal']}")
        print("\n[All Stats:]")
        for stat_id, value in sorted(cmc_stats['stats'].items(), key=lambda x: int(x[0])):
            known_name = KNOWN_STATS.get(stat_id, "??? UNKNOWN")
            print(f"  stat_{stat_id}: {value:>8.1f}  ->  {known_name}")

        unknown = analyze_unknown_stats(cmc_stats['stats'], KNOWN_STATS)
        if unknown:
            print(f"\n[*] Found {len(unknown)} unknown stats:")
            for u in unknown:
                print(f"  stat_{u['stat_id']}: {u['value']}")

    # Research Deebo Samuel (Returner)
    print("\n\n[RESEARCH TARGET 3: Player with Return Stats (Deebo Samuel)]")
    print("-" * 80)

    deebo_stats = find_player_stats("Deebo Samuel", 3116389, 8, week_8_data)

    if deebo_stats:
        print(f"\n[+] Found: {deebo_stats['name']} (ID: {deebo_stats['id']})")
        print(f"Fantasy Points: {deebo_stats['appliedTotal']}")
        print("\n[All Stats:]")
        for stat_id, value in sorted(deebo_stats['stats'].items(), key=lambda x: int(x[0])):
            known_name = KNOWN_STATS.get(stat_id, "??? UNKNOWN")
            print(f"  stat_{stat_id}: {value:>8.1f}  ->  {known_name}")

        unknown = analyze_unknown_stats(deebo_stats['stats'], KNOWN_STATS)
        if unknown:
            print(f"\n[*] Found {len(unknown)} unknown stats - potential return stats:")
            for u in unknown:
                print(f"  stat_{u['stat_id']}: {u['value']}")

    # Save raw data for manual analysis
    output_folder = Path(__file__).parent
    output_file = output_folder / "espn_stat_research_output.json"

    research_data = {
        "daniel_jones_week_8": daniel_jones_stats,
        "christian_mccaffrey_week_1": cmc_stats,
        "deebo_samuel_week_8": deebo_stats,
        "known_stats": KNOWN_STATS
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(research_data, f, indent=2, ensure_ascii=False)

    print(f"\n\n[*] Raw data saved to: {output_file}")
    print(f"[*] Review this file to identify patterns in unknown stat IDs")

    print("\n" + "=" * 80)
    print("RESEARCH COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review unknown stat IDs in the output file")
    print("2. Cross-reference with NFL.com box scores for these games")
    print("3. Identify which unknown stats match fumbles, sacks, returns, etc.")
    print("4. Update stat_ids.md documentation")


if __name__ == "__main__":
    asyncio.run(main())
