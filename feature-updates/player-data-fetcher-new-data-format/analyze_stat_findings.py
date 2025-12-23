#!/usr/bin/env python3
"""
Analyze ESPN Stat Research Results

Cross-reference findings with known stat IDs and identify missing stats.
"""

import json


def analyze_research_results():
    """Analyze the research results JSON file"""

    with open('espn_stat_research_results.json', 'r') as f:
        results = json.load(f)

    stat_ids = results['stat_ids']

    print("="*70)
    print("ANALYSIS: Missing Stat ID Identification")
    print("="*70)

    # Known stat IDs from documentation
    known_stats = {
        # Passing
        '0': 'passing_attempts', '1': 'completions', '2': 'incompletions',
        '3': 'passing_yards', '4': 'passing_tds', '14': 'interceptions',
        '21': 'completion_pct', '22': 'passing_yards_dup',
        # Rushing
        '23': 'rushing_attempts', '24': 'rushing_yards', '25': 'rushing_tds',
        '39': 'yards_per_carry', '40': 'rushing_yards_dup',
        # Receiving
        '41': 'receptions_dup', '42': 'receiving_yards', '43': 'receiving_tds',
        '53': 'receptions', '58': 'targets', '60': 'yards_per_reception',
        '61': 'receiving_yards_dup',
        # Kicking
        '80': 'xp_made', '81': 'xp_attempted', '83': 'fg_made', '84': 'fg_attempted',
        # Defense
        '95': 'interceptions', '99': 'fumbles_recovered', '106': 'forced_fumbles',
        '107': 'assisted_tackles', '108': 'solo_tackles', '109': 'total_tackles',
        '112': 'sacks', '113': 'passes_defensed', '118': 'punts_returned',
        '120': 'points_allowed', '127': 'yards_allowed', '187': 'points_allowed_dup',
        # Game participation
        '155': 'game_played', '156': 'game_played_dup', '210': 'games_played',
    }

    print("\n1. QB SACKS TAKEN")
    print("-" * 70)
    # stat_158 appears in QBs with reasonable values (12 for Mahomes)
    if '158' in stat_ids:
        print(f"✅ FOUND: stat_158 (appears in {stat_ids['158']['count']} players)")
        print(f"   Examples: {stat_ids['158']['examples'][:3]}")
        print("   HYPOTHESIS: This is likely sacks taken (appears mainly in QBs)")

    print("\n2. FUMBLES")
    print("-" * 70)
    # stat_72 appears in many players
    candidates = ['72', '73', '68']
    for stat_id in candidates:
        if stat_id in stat_ids:
            print(f"   stat_{stat_id}: {stat_ids[stat_id]['count']} players")
            print(f"      Examples: {stat_ids[stat_id]['examples'][:2]}")

    # stat_72 is a good candidate (appears in 409 players, consistent with fumble frequency)
    print("\n   ✅ LIKELY: stat_72 (fumbles) - appears in 409 players across positions")

    print("\n3. TWO-POINT CONVERSIONS")
    print("-" * 70)
    # Need a stat that appears rarely and with value 1
    candidates_2pt = ['64', '65', '68', '73', '175', '176']
    for stat_id in candidates_2pt:
        if stat_id in stat_ids:
            count = stat_ids[stat_id]['count']
            examples = stat_ids[stat_id]['examples'][:3]
            print(f"   stat_{stat_id}: {count} players | Examples: {examples}")

    print("\n   ✅ LIKELY: stat_68 or stat_73 (2-pt conversions) - appear frequently with value 1")

    print("\n4. RETURN YARDS AND TDs")
    print("-" * 70)
    # From KaVontae Turpin (known returner):
    # stat_114: 115, stat_115: 13, stat_116: 11, stat_117: 4, stat_118: 1
    return_candidates = ['114', '115', '116', '117', '118']
    for stat_id in return_candidates:
        if stat_id in stat_ids:
            count = stat_ids[stat_id]['count']
            examples = stat_ids[stat_id]['examples'][:3]
            print(f"   stat_{stat_id}: {count} players | Examples: {examples}")

    print("\n   ✅ LIKELY:")
    print("      stat_114: Return yards (high values like 115)")
    print("      stat_118: Return TDs (low values like 1)")
    print("      Note: stat_118 documented as 'punts returned' - may be punt return TDs")

    print("\n5. DEFENSIVE TDs")
    print("-" * 70)
    # Look for rare defensive stats
    rare_defense_stats = []
    for stat_id, data in stat_ids.items():
        try:
            stat_num = int(stat_id)
            if 89 <= stat_num <= 136 and data['count'] < 100:
                # Check if examples are defenses
                examples = data['examples']
                if any('D/ST' in ex.get('player', '') for ex in examples):
                    rare_defense_stats.append((stat_id, data))
        except:
            pass

    print("   Rare defense stats (potential TDs/safeties):")
    for stat_id, data in sorted(rare_defense_stats, key=lambda x: x[1]['count']):
        count = data['count']
        examples = [ex for ex in data['examples'] if 'D/ST' in ex.get('player', '')][:2]
        print(f"      stat_{stat_id}: {count} players | {examples}")

    print("\n   ✅ LIKELY:")
    print("      stat_93: Defensive/Special Teams TD (14 players - very rare)")
    print("      stat_94: Possible safety or blocked kicks (69 players)")
    print("      stat_119: Another rare defense stat (312 players)")

    print("\n6. SAFETIES")
    print("-" * 70)
    print("   ✅ LIKELY:")
    print("      stat_93 or stat_94 (both rare defensive stats)")
    print("      Safeties are extremely rare, so very low count makes sense")

    print("\n" + "="*70)
    print("SUMMARY OF FINDINGS")
    print("="*70)

    findings = {
        'sacks_taken': 'stat_158',
        'fumbles': 'stat_72',
        'two_point_conversions': 'stat_68 or stat_73',
        'return_yards': 'stat_114',
        'return_tds': 'stat_118 (may be punt return TDs)',
        'defensive_tds': 'stat_93 (strongest candidate)',
        'safeties': 'stat_94 (possible) or stat_93'
    }

    for missing_stat, stat_id in findings.items():
        print(f"✅ {missing_stat}: {stat_id}")

    print("\n" + "="*70)
    print("VERIFICATION NEEDED")
    print("="*70)
    print("""
These identifications are based on statistical analysis and need verification:

1. Cross-reference with NFL.com box scores for specific games
2. Check GitHub community repositories (cwendt94/espn-api)
3. Test with known examples (e.g., QB with X sacks, player with Y fumbles)
4. Verify with multiple weeks of data

NEXT STEPS:
1. Create targeted tests for each stat ID
2. Verify against actual game data
3. Update stat_ids.md documentation
4. Update feature specifications
""")


if __name__ == "__main__":
    analyze_research_results()
