#!/usr/bin/env python3
"""
ESPN API Stat Research Script

This script fetches real ESPN data to identify missing stat IDs:
- QB sacks taken
- Fumbles
- 2-point conversions
- Return yards/TDs
- Defensive TDs
- Safeties

Usage:
    python espn_stat_research.py

Author: Research for player-data-fetcher-new-data-format feature
"""

import json
import requests
from typing import Dict, List, Any, Optional
from collections import defaultdict


class ESPNStatResearcher:
    """Research ESPN API to find undocumented stat IDs"""

    BASE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/1"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Fantasy-Filter': '{"players":{"limit":2000,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'
    }

    def __init__(self, season: int = 2024):
        self.season = season
        self.players_data = None

    def fetch_players(self, scoring_period: int = 8) -> List[Dict]:
        """Fetch player data from ESPN API for a specific week"""
        url = self.BASE_URL.format(season=self.season)
        params = {
            'scoringPeriodId': scoring_period,
            'view': 'kona_player_info'
        }

        print(f"Fetching ESPN data for {self.season} season, week {scoring_period}...")
        response = requests.get(url, headers=self.HEADERS, params=params, timeout=30)

        if response.status_code != 200:
            raise Exception(f"ESPN API error: {response.status_code}")

        data = response.json()
        self.players_data = data.get('players', [])
        print(f"Fetched {len(self.players_data)} players")
        return self.players_data

    def find_player_by_name(self, name: str) -> Optional[Dict]:
        """Find a player by name (partial match)"""
        if not self.players_data:
            return None

        name_lower = name.lower()
        for player_entry in self.players_data:
            player = player_entry.get('player', {})
            full_name = player.get('fullName', '').lower()
            if name_lower in full_name:
                return player_entry
        return None

    def get_player_stats(self, player_entry: Dict, scoring_period: int) -> Optional[Dict]:
        """Extract stats for a specific week from player data"""
        player = player_entry.get('player', {})
        stats_array = player.get('stats', [])

        # Find stats for the specific week with statSourceId=0 (actual stats)
        for stat_entry in stats_array:
            if (stat_entry.get('scoringPeriodId') == scoring_period and
                stat_entry.get('statSourceId') == 0):
                return stat_entry.get('stats', {})
        return None

    def analyze_stat_ids(self, stats: Dict) -> None:
        """Analyze and display all stat IDs present"""
        print("\nStat IDs found:")
        for stat_id, value in sorted(stats.items(), key=lambda x: int(x[0])):
            print(f"  stat_{stat_id}: {value}")

    def research_sacks_taken(self) -> None:
        """Research QB sacks taken stat ID"""
        print("\n" + "="*70)
        print("RESEARCH: QB Sacks Taken")
        print("="*70)

        # Patrick Mahomes is frequently sacked
        player = self.find_player_by_name("Patrick Mahomes")
        if not player:
            print("Player not found")
            return

        player_info = player.get('player', {})
        print(f"Player: {player_info.get('fullName')}")
        print(f"Position: {player_info.get('defaultPositionId')}")

        stats = self.get_player_stats(player, 8)
        if stats:
            self.analyze_stat_ids(stats)

            # Known stat IDs
            print("\nKnown passing stats:")
            print(f"  Attempts: {stats.get('0', 'N/A')}")
            print(f"  Completions: {stats.get('1', 'N/A')}")
            print(f"  Yards: {stats.get('3', 'N/A')}")
            print(f"  TDs: {stats.get('4', 'N/A')}")
            print(f"  INTs: {stats.get('14', 'N/A')}")

            # Look for unknown stats that might be sacks
            unknown_stats = {k: v for k, v in stats.items()
                           if k not in ['0', '1', '2', '3', '4', '14', '21', '22']}
            print(f"\nUnknown stat IDs (potential sacks): {len(unknown_stats)}")
            for stat_id, value in sorted(unknown_stats.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
                print(f"  stat_{stat_id}: {value}")

    def research_fumbles(self) -> None:
        """Research fumbles stat ID"""
        print("\n" + "="*70)
        print("RESEARCH: Fumbles")
        print("="*70)

        # Look for a RB known to fumble
        player = self.find_player_by_name("Rhamondre Stevenson")  # Had fumbles in 2024
        if not player:
            print("Player not found, trying another...")
            player = self.find_player_by_name("Tony Pollard")

        if not player:
            print("No suitable player found")
            return

        player_info = player.get('player', {})
        print(f"Player: {player_info.get('fullName')}")

        stats = self.get_player_stats(player, 8)
        if stats:
            self.analyze_stat_ids(stats)

            print("\nKnown rushing stats:")
            print(f"  Attempts: {stats.get('23', 'N/A')}")
            print(f"  Yards: {stats.get('24', 'N/A')}")
            print(f"  TDs: {stats.get('25', 'N/A')}")

            # Look for fumbles in unknown stats
            print("\nLooking for fumbles in unknown stats...")

    def research_two_point_conversions(self) -> None:
        """Research 2-point conversion stat ID"""
        print("\n" + "="*70)
        print("RESEARCH: 2-Point Conversions")
        print("="*70)

        # Need to find a week where teams went for 2-pt conversions
        # Check multiple players
        test_players = ["Lamar Jackson", "Jalen Hurts", "Josh Allen"]

        for name in test_players:
            player = self.find_player_by_name(name)
            if player:
                player_info = player.get('player', {})
                print(f"\nPlayer: {player_info.get('fullName')}")
                stats = self.get_player_stats(player, 8)
                if stats:
                    # Look for stat IDs with value of 1 or 2 (successful 2-pt conversions)
                    small_value_stats = {k: v for k, v in stats.items()
                                        if isinstance(v, (int, float)) and 0 < v <= 3}
                    print(f"Stats with values 1-3 (potential 2-pt): {small_value_stats}")

    def research_return_stats(self) -> None:
        """Research kick/punt return stats"""
        print("\n" + "="*70)
        print("RESEARCH: Return Yards and TDs")
        print("="*70)

        # Look for known returners
        returners = ["Devin Duvernay", "Brandon Aubrey", "KaVontae Turpin"]

        for name in returners:
            player = self.find_player_by_name(name)
            if player:
                player_info = player.get('player', {})
                print(f"\nPlayer: {player_info.get('fullName')}")
                print(f"Position: {player_info.get('defaultPositionId')}")

                stats = self.get_player_stats(player, 8)
                if stats:
                    self.analyze_stat_ids(stats)

    def research_defensive_stats(self) -> None:
        """Research defensive TD and safety stats"""
        print("\n" + "="*70)
        print("RESEARCH: Defensive TDs and Safeties")
        print("="*70)

        # Look for top defenses
        defenses = ["Ravens", "49ers", "Cowboys", "Bills"]

        for name in defenses:
            player = self.find_player_by_name(name)
            if player:
                player_info = player.get('player', {})
                print(f"\nDefense: {player_info.get('fullName')}")

                stats = self.get_player_stats(player, 8)
                if stats:
                    print("\nKnown defense stats:")
                    print(f"  Interceptions (stat_95): {stats.get('95', 'N/A')}")
                    print(f"  Fumbles Recovered (stat_99): {stats.get('99', 'N/A')}")
                    print(f"  Forced Fumbles (stat_106): {stats.get('106', 'N/A')}")
                    print(f"  Sacks (stat_112): {stats.get('112', 'N/A')}")
                    print(f"  Points Allowed (stat_120): {stats.get('120', 'N/A')}")
                    print(f"  Yards Allowed (stat_127): {stats.get('127', 'N/A')}")

                    # Look for unknown stats
                    known_def_stats = ['95', '99', '106', '107', '108', '109',
                                      '112', '113', '118', '120', '127', '187']
                    unknown = {k: v for k, v in stats.items() if k not in known_def_stats}

                    print(f"\nUnknown defense stats (potential TD/safety):")
                    for stat_id, value in sorted(unknown.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
                        print(f"  stat_{stat_id}: {value}")

    def find_all_stat_ids(self) -> Dict[str, int]:
        """Find all stat IDs across all players"""
        print("\n" + "="*70)
        print("COMPREHENSIVE STAT ID ANALYSIS")
        print("="*70)

        if not self.players_data:
            return {}

        stat_id_counts = defaultdict(int)
        stat_id_examples = {}

        for player_entry in self.players_data:
            player = player_entry.get('player', {})
            stats_array = player.get('stats', [])

            for stat_entry in stats_array:
                if stat_entry.get('statSourceId') == 0:  # Actual stats only
                    stats = stat_entry.get('stats', {})
                    for stat_id, value in stats.items():
                        stat_id_counts[stat_id] += 1
                        if stat_id not in stat_id_examples and value != 0:
                            stat_id_examples[stat_id] = {
                                'player': player.get('fullName'),
                                'value': value,
                                'position': player.get('defaultPositionId')
                            }

        print(f"\nTotal unique stat IDs found: {len(stat_id_counts)}")
        print("\nStat ID frequency (showing all):")

        for stat_id, count in sorted(stat_id_counts.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
            example = stat_id_examples.get(stat_id, {})
            print(f"  stat_{stat_id}: {count} players | Example: {example.get('player', 'N/A')} = {example.get('value', 'N/A')}")

        return dict(stat_id_counts)

    def save_research_results(self, filename: str = "espn_stat_research_results.json"):
        """Save research results to JSON file"""
        if not self.players_data:
            return

        stat_id_counts = defaultdict(int)
        stat_id_details = defaultdict(list)

        for player_entry in self.players_data:
            player = player_entry.get('player', {})
            stats_array = player.get('stats', [])

            for stat_entry in stats_array:
                if stat_entry.get('statSourceId') == 0:
                    stats = stat_entry.get('stats', {})
                    week = stat_entry.get('scoringPeriodId')

                    for stat_id, value in stats.items():
                        stat_id_counts[stat_id] += 1
                        if value != 0 and len(stat_id_details[stat_id]) < 5:  # Keep 5 examples
                            stat_id_details[stat_id].append({
                                'player': player.get('fullName'),
                                'position': player.get('defaultPositionId'),
                                'week': week,
                                'value': value
                            })

        results = {
            'season': self.season,
            'total_players': len(self.players_data),
            'stat_ids': {
                stat_id: {
                    'count': count,
                    'examples': stat_id_details[stat_id]
                }
                for stat_id, count in sorted(stat_id_counts.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999)
            }
        }

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n✅ Research results saved to: {filename}")


def main():
    """Run comprehensive ESPN stat research"""
    researcher = ESPNStatResearcher(season=2024)

    # Fetch data for Week 8 (good sample week with varied stats)
    researcher.fetch_players(scoring_period=8)

    # Research specific missing stats
    researcher.research_sacks_taken()
    researcher.research_fumbles()
    researcher.research_two_point_conversions()
    researcher.research_return_stats()
    researcher.research_defensive_stats()

    # Comprehensive analysis
    researcher.find_all_stat_ids()

    # Save results
    researcher.save_research_results()

    print("\n" + "="*70)
    print("RESEARCH COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Review espn_stat_research_results.json")
    print("2. Cross-reference findings with /docs/espn/reference/stat_ids.md")
    print("3. Update documentation with newly discovered stat IDs")


if __name__ == "__main__":
    main()
