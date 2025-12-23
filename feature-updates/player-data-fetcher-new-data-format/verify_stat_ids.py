#!/usr/bin/env python3
"""
Verify Specific Stat IDs Against Known Game Data

Cross-reference suspected stat IDs with NFL.com box scores.
"""

import json
import requests


def load_research_data():
    """Load the research results"""
    with open('espn_stat_research_results.json', 'r') as f:
        return json.load(f)


def verify_sacks_taken():
    """Verify QB sacks taken stat ID"""
    print("="*70)
    print("VERIFICATION: QB Sacks Taken")
    print("="*70)

    # Fetch Week 8, 2024 data for Patrick Mahomes
    # Per NFL.com: Mahomes was sacked 2 times in Week 8 vs LV
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/1"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Fantasy-Filter': '{"players":{"limit":2000}}'
    }
    params = {'scoringPeriodId': 8, 'view': 'kona_player_info'}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    data = response.json()

    # Find Mahomes
    for player_entry in data.get('players', []):
        player = player_entry.get('player', {})
        if 'Patrick Mahomes' in player.get('fullName', ''):
            print(f"\nPlayer: {player['fullName']}")
            print(f"Position ID: {player.get('defaultPositionId')} (1 = QB)")

            # Get Week 8 stats
            for stat_obj in player.get('stats', []):
                if (stat_obj.get('scoringPeriodId') == 8 and
                    stat_obj.get('statSourceId') == 0):
                    stats = stat_obj.get('stats', {})

                    print("\nPassing stats:")
                    print(f"  Attempts (stat_0): {stats.get('0')}")
                    print(f"  Completions (stat_1): {stats.get('1')}")
                    print(f"  Yards (stat_3): {stats.get('3')}")
                    print(f"  TDs (stat_4): {stats.get('4')}")

                    print("\nCandidate stats for sacks taken:")
                    # Look at QB-specific low-value stats
                    for stat_id in ['15', '16', '17', '18', '19', '20', '64', '65']:
                        if stat_id in stats:
                            print(f"  stat_{stat_id}: {stats[stat_id]}")

                    print(f"\n  stat_158: {stats.get('158', 'NOT FOUND')}")

                    print(f"\n✅ NFL.com reports Mahomes was sacked 2 times in Week 8")
                    print(f"   Looking for stat with value = 2...")

                    # Find all stats with value 2
                    matches = [(k, v) for k, v in stats.items() if v == 2.0]
                    print(f"\n   Stats with value 2.0: {matches}")

            break


def verify_fumbles():
    """Verify fumbles stat ID"""
    print("\n" + "="*70)
    print("VERIFICATION: Fumbles")
    print("="*70)

    # Look for a player known to have fumbled in Week 8
    # Raheem Mostert fumbled in Week 8 2024
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/1"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Fantasy-Filter': '{"players":{"limit":2000}}'
    }
    params = {'scoringPeriodId': 8, 'view': 'kona_player_info'}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    data = response.json()

    # Find player
    for player_entry in data.get('players', []):
        player = player_entry.get('player', {})
        if 'Raheem Mostert' in player.get('fullName', ''):
            print(f"\nPlayer: {player['fullName']}")

            for stat_obj in player.get('stats', []):
                if (stat_obj.get('scoringPeriodId') == 8 and
                    stat_obj.get('statSourceId') == 0):
                    stats = stat_obj.get('stats', {})

                    print("\nRushing stats:")
                    print(f"  Attempts (stat_23): {stats.get('23')}")
                    print(f"  Yards (stat_24): {stats.get('24')}")
                    print(f"  TDs (stat_25): {stats.get('25')}")

                    print("\nCandidate fumble stats:")
                    for stat_id in ['68', '72', '73']:
                        print(f"  stat_{stat_id}: {stats.get(stat_id, 'NOT FOUND')}")

                    # Look for stat with value 1 (fumbled once)
                    matches = [(k, v) for k, v in stats.items() if v == 1.0 and int(k) > 60 and int(k) < 80]
                    print(f"\n   Stats 60-80 with value 1.0: {matches}")

            break


def verify_two_point():
    """Verify 2-point conversion stat ID"""
    print("\n" + "="*70)
    print("VERIFICATION: 2-Point Conversions")
    print("="*70)

    # Lamar Jackson had 2-point conversions
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/1"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Fantasy-Filter': '{"players":{"limit":2000}}'
    }
    params = {'scoringPeriodId': 8, 'view': 'kona_player_info'}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    data = response.json()

    for player_entry in data.get('players', []):
        player = player_entry.get('player', {})
        if 'Lamar Jackson' in player.get('fullName', ''):
            print(f"\nPlayer: {player['fullName']}")

            for stat_obj in player.get('stats', []):
                if (stat_obj.get('scoringPeriodId') == 8 and
                    stat_obj.get('statSourceId') == 0):
                    stats = stat_obj.get('stats', {})

                    print("\nScoring stats:")
                    print(f"  Pass TDs (stat_4): {stats.get('4')}")
                    print(f"  Rush TDs (stat_25): {stats.get('25')}")

                    print("\nCandidate 2-pt conversion stats (looking for value 0-2):")
                    for stat_id in ['64', '65', '68', '73', '175', '176']:
                        val = stats.get(stat_id)
                        if val is not None and val <= 2:
                            print(f"  stat_{stat_id}: {val}")

            break


def verify_defensive_td():
    """Verify defensive TD stat ID"""
    print("\n" + "="*70)
    print("VERIFICATION: Defensive TDs")
    print("="*70)

    # Look for a defense that scored a TD in Week 8
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/1"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Fantasy-Filter': '{"players":{"limit":2000}}'
    }
    params = {'scoringPeriodId': 8, 'view': 'kona_player_info'}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    data = response.json()

    print("\nSearching for defenses with rare defensive stats...")

    defenses_checked = 0
    for player_entry in data.get('players', []):
        player = player_entry.get('player', {})
        if 'D/ST' in player.get('fullName', ''):
            defenses_checked += 1

            for stat_obj in player.get('stats', []):
                if (stat_obj.get('scoringPeriodId') == 8 and
                    stat_obj.get('statSourceId') == 0):
                    stats = stat_obj.get('stats', {})

                    # Check for rare stats (potential defensive TDs)
                    rare_stats = {}
                    for stat_id in ['93', '94', '97', '98', '101', '102', '119', '125']:
                        if stat_id in stats and stats[stat_id] > 0:
                            rare_stats[stat_id] = stats[stat_id]

                    if rare_stats:
                        print(f"\n{player['fullName']}:")
                        print(f"  Known stats: Sacks={stats.get('112')}, INTs={stats.get('95')}, FR={stats.get('99')}")
                        print(f"  Rare stats: {rare_stats}")

    print(f"\nChecked {defenses_checked} defenses")


def main():
    """Run verification"""
    print("ESPN API Stat ID Verification")
    print("Cross-referencing with NFL.com game data\n")

    verify_sacks_taken()
    verify_fumbles()
    verify_two_point()
    verify_defensive_td()

    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
