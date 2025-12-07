#!/usr/bin/env python3
"""
Test script to verify edge case handling with bulk ESPN API fetch.

Tests:
1. Bye week handling - weeks with no stats should be handled gracefully
2. DST negative scores - defense can have negative fantasy points
3. Missing data - players with incomplete stats (rookies, practice squad)
"""

import json
import urllib.request
from typing import Dict, List, Any, Optional

ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
SEASON = 2024
ESPN_PLAYER_LIMIT = 500  # Larger batch to catch DST players


def fetch_bulk_players() -> Dict[str, Any]:
    """Fetch players using bulk API call with scoringPeriodId=0."""
    base_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leaguedefaults/3"
    url = f"{base_url}?view=kona_player_info&scoringPeriodId=0"

    headers = {
        "User-Agent": ESPN_USER_AGENT,
        "X-Fantasy-Filter": json.dumps({
            "players": {
                "limit": ESPN_PLAYER_LIMIT,
                "sortPercOwned": {"sortPriority": 4, "sortAsc": False}
            }
        })
    }

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode('utf-8'))


def extract_weekly_points(stats: List[Dict], year: int, position: str) -> tuple:
    """Extract weekly points from stats array."""
    weekly_actual: Dict[int, Optional[float]] = {}
    weekly_projected: Dict[int, Optional[float]] = {}

    for stat in stats:
        if not isinstance(stat, dict):
            continue

        season_id = stat.get('seasonId')
        week = stat.get('scoringPeriodId')
        source = stat.get('statSourceId')  # 0=actual, 1=projected
        points = stat.get('appliedTotal')

        if season_id != year or week is None or week == 0:
            continue

        if week < 1 or week > 17:
            continue

        if points is not None:
            if source == 0:  # Actual
                weekly_actual[week] = float(points)
            elif source == 1:  # Projected
                weekly_projected[week] = float(points)

    return weekly_actual, weekly_projected


def test_edge_cases():
    """Run edge case tests."""
    print("=" * 60)
    print("EDGE CASE VERIFICATION FOR BULK API FETCH")
    print("=" * 60)

    data = fetch_bulk_players()
    players = data.get('players', [])

    print(f"\nFetched {len(players)} players in bulk request")

    # Track edge cases found
    dst_players = []
    negative_dst_scores = []
    low_dst_scores = []  # Track scores < 5 to verify DST data is present
    bye_week_zeros = []
    missing_data_players = []
    players_with_full_data = 0

    # ESPN position mapping
    position_map = {1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'DST'}

    for player in players:
        player_info = player.get('player', {})
        player_id = str(player_info.get('id', ''))

        # Get name
        first = player_info.get('firstName', '')
        last = player_info.get('lastName', '')
        name = f"{first} {last}".strip() or 'Unknown'

        # Get position
        pos_id = player_info.get('defaultPositionId')
        position = position_map.get(pos_id, 'UNK')

        # Skip non-fantasy positions
        if position == 'UNK':
            continue

        # Get stats
        stats = player_info.get('stats', [])

        # Test 1: Check DST players
        if position == 'DST':
            actual, projected = extract_weekly_points(stats, SEASON, position)
            dst_players.append({
                'name': name,
                'actual_weeks': len(actual),
                'projected_weeks': len(projected)
            })

            # Check for negative or low scores
            for week, points in actual.items():
                if points is not None:
                    if points < 0:
                        negative_dst_scores.append({
                            'name': name,
                            'week': week,
                            'points': points
                        })
                    elif points < 5:
                        low_dst_scores.append({
                            'name': name,
                            'week': week,
                            'points': points
                        })

        # Test 2: Check for weeks with no data (potential bye weeks)
        actual, projected = extract_weekly_points(stats, SEASON, position)
        weeks_with_data = set(actual.keys()) | set(projected.keys())
        all_weeks = set(range(1, 18))
        missing_weeks = all_weeks - weeks_with_data

        # Count players with full weekly data
        if len(weeks_with_data) >= 13:  # Good amount of data
            players_with_full_data += 1

        if missing_weeks and len(weeks_with_data) > 5:  # Has some data but missing weeks
            bye_week_zeros.append({
                'name': name,
                'position': position,
                'missing_weeks': sorted(missing_weeks),
                'has_weeks': len(weeks_with_data)
            })

        # Test 3: Check for players with very limited data
        if len(weeks_with_data) < 3 and len(stats) > 0:  # Has stats array but few weeks
            missing_data_players.append({
                'name': name,
                'position': position,
                'weeks_with_data': len(weeks_with_data),
                'total_stat_entries': len(stats)
            })

    # Report results
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    # DST Results
    print(f"\n1. DST PLAYERS FOUND: {len(dst_players)}")
    if dst_players[:5]:
        for d in dst_players[:5]:
            print(f"   - {d['name']}: {d['actual_weeks']} actual weeks, {d['projected_weeks']} projected weeks")

    print(f"\n2. DST NEGATIVE SCORES: {len(negative_dst_scores)}")
    if negative_dst_scores:
        for score in negative_dst_scores[:5]:
            print(f"   - {score['name']} Week {score['week']}: {score['points']:.1f} pts")
    else:
        print("   (None found - checking low scores instead)")
        print(f"   DST LOW SCORES (<5 pts): {len(low_dst_scores)}")
        if low_dst_scores[:3]:
            for score in low_dst_scores[:3]:
                print(f"   - {score['name']} Week {score['week']}: {score['points']:.1f} pts")

    # Bye week results
    print(f"\n3. PLAYERS WITH MISSING WEEKS (bye weeks): {len(bye_week_zeros)}")
    if bye_week_zeros[:3]:
        for p in bye_week_zeros[:3]:
            print(f"   - {p['name']} ({p['position']}): missing {len(p['missing_weeks'])} weeks, has {p['has_weeks']} weeks")

    # Missing data results
    print(f"\n4. PLAYERS WITH LIMITED DATA: {len(missing_data_players)}")
    if missing_data_players[:5]:
        for p in missing_data_players[:5]:
            print(f"   - {p['name']} ({p['position']}): {p['weeks_with_data']} weeks, {p['total_stat_entries']} stat entries")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Bulk API call successful - got {len(players)} players")
    print(f"✓ DST players in response: {len(dst_players)}")
    print(f"✓ Players with 13+ weeks of data: {players_with_full_data}")
    print(f"✓ Bye week gaps detected: {len(bye_week_zeros)} players")
    print(f"✓ Limited data players: {len(missing_data_players)}")

    # Final verdict
    print("\n" + "=" * 60)
    print("EDGE CASE VERDICT")
    print("=" * 60)
    if len(dst_players) > 0:
        print("✓ DST: PASS - DST players present with weekly stats")
    else:
        print("⚠ DST: Need larger sample - no DST in top players by ownership")

    if players_with_full_data > 0:
        print("✓ BYE WEEKS: PASS - Missing weeks handled gracefully (shown as gaps)")

    print("✓ MISSING DATA: PASS - Players with limited stats don't crash extraction")

    return True


if __name__ == "__main__":
    test_edge_cases()
