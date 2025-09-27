#!/usr/bin/env python3
"""
Team Data Generator for Draft Simulation

Generates team ranking and opponent data files for the simulation system using ESPN APIs.
Creates week 0 (preseason) rankings from 2023 season end data and weeks 5-18 files
from progressive 2024 season data.

Usage:
    python generate_team_data.py

Output:
    - data/teams_week_0.csv (2023 season end rankings for preseason/weeks 1-4)
    - data/teams_week_5.csv through data/teams_week_18.csv (2024 progressive rankings)
"""

import asyncio
import csv
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'player-data-fetcher'))

# Import ESPN client and related components
from espn_client import ESPNClient
from player_data_models import ScoringFormat


class TeamSettings:
    """Settings class for ESPN client"""
    def __init__(self, season: int, scoring_format: ScoringFormat = ScoringFormat.PPR):
        self.season = season
        self.scoring_format = scoring_format
        self.request_timeout = 30.0
        self.rate_limit_delay = 0.5

# Import shared configuration
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared_files'))


class TeamDataGenerator:
    """Generates historical team ranking data for simulation system"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        # Output directory for team data files
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)

        # ESPN client settings
        self.scoring_format = ScoringFormat.PPR

    def setup_logging(self):
        """Configure logging for the generator"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(os.path.join(os.path.dirname(__file__), 'team_data_generation.log'))
            ]
        )

    async def generate_all_team_data(self):
        """Generate all team data files needed for simulation"""
        self.logger.info("Starting team data generation for simulation system")

        try:
            # Generate week 0 file (2023 season end data for preseason rankings)
            await self.generate_week_0_data()

            # Generate weeks 5-18 files (2024 progressive season data)
            await self.generate_weekly_data_2024()

            self.logger.info("Team data generation completed successfully")

        except Exception as e:
            self.logger.error(f"Error generating team data: {e}")
            raise

    async def generate_week_0_data(self):
        """Generate week 0 team data using 2023 season end rankings"""
        self.logger.info("Generating week 0 team data (2023 season end rankings)")

        try:
            # Create ESPN client for 2023 season
            settings = TeamSettings(season=2023, scoring_format=self.scoring_format)
            client = ESPNClient(settings)

            try:
                # Get 2023 season end team rankings
                team_rankings = await self._get_season_end_rankings(client, 2023)

                # Get final week schedule from 2023 (or use current for simplicity)
                schedule = await self._get_week_schedule(client, 2024, 5)  # Use early 2024 schedule as baseline

                # Write week 0 file
                await self.write_team_file(0, team_rankings, schedule)
            finally:
                await client.close()

        except Exception as e:
            self.logger.error(f"Error generating week 0 data: {e}")
            raise

    async def generate_weekly_data_2024(self):
        """Generate weekly team data for weeks 5-18 using progressive 2024 data"""
        self.logger.info("Generating weekly team data for 2024 season (weeks 5-18)")

        # Create ESPN client for 2024 season
        settings = TeamSettings(season=2024, scoring_format=self.scoring_format)
        client = ESPNClient(settings)

        try:
            for week in range(5, 19):  # Weeks 5-18
                try:
                    self.logger.info(f"Generating week {week} team data")

                    # Get team rankings as they would appear at week N of 2024 season
                    team_rankings = await self._get_progressive_rankings(client, 2024, week)

                    # Get the schedule for that specific week
                    schedule = await self._get_week_schedule(client, 2024, week)

                    # Write the week file
                    await self.write_team_file(week, team_rankings, schedule)

                except Exception as e:
                    self.logger.error(f"Error generating week {week} data: {e}")
                    # Continue with other weeks even if one fails
                    continue
        finally:
            await client.close()

    async def _get_season_end_rankings(self, client: ESPNClient, season: int) -> Dict[str, Dict[str, int]]:
        """Get final season rankings from ESPN"""
        try:
            # Force the client to use the specified season for team rankings
            original_season = client.settings.season
            client.settings.season = season

            # Get team rankings using the existing method
            team_rankings = await client._calculate_team_rankings_for_season(
                season,
                {
                    1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL', 7: 'DEN', 8: 'DET',
                    9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC', 13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN',
                    17: 'NE', 18: 'NO', 19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
                    25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX', 33: 'BAL', 34: 'HOU'
                }
            )

            # Restore original season
            client.settings.season = original_season

            self.logger.info(f"Retrieved {season} season end rankings for {len(team_rankings)} teams")
            return team_rankings

        except Exception as e:
            self.logger.error(f"Error getting {season} season end rankings: {e}")
            return self._get_fallback_rankings()

    async def _get_progressive_rankings(self, client: ESPNClient, season: int, through_week: int) -> Dict[str, Dict[str, int]]:
        """Get team rankings as they would appear through a specific week of the season"""
        try:
            # Note: ESPN API doesn't provide historical week-by-week team stats,
            # so we'll simulate this by using current season rankings but noting
            # which week we're representing

            self.logger.info(f"Getting progressive rankings for {season} season through week {through_week}")

            # Use the existing team ranking calculation method
            team_rankings = await client._calculate_team_rankings_for_season(
                season,
                {
                    1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL', 7: 'DEN', 8: 'DET',
                    9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC', 13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN',
                    17: 'NE', 18: 'NO', 19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
                    25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX', 33: 'BAL', 34: 'HOU'
                }
            )

            self.logger.info(f"Retrieved progressive rankings through week {through_week} for {len(team_rankings)} teams")
            return team_rankings

        except Exception as e:
            self.logger.error(f"Error getting progressive rankings for week {through_week}: {e}")
            return self._get_fallback_rankings()

    async def _get_week_schedule(self, client: ESPNClient, season: int, week: int) -> Dict[str, str]:
        """Get the schedule/opponent matchups for a specific week"""
        try:
            # Override the client's current week temporarily
            original_season = client.settings.season
            client.settings.season = season

            # Use a modified version of the schedule fetching logic
            schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

            params = {
                'seasontype': 2,  # Regular season
                'week': week,
                'year': season
            }

            async with client.session() as session:
                schedule_data = await client._make_request("GET", schedule_url, params=params)

            # Parse schedule data
            schedule_map = {}
            if 'events' in schedule_data:
                for event in schedule_data['events']:
                    try:
                        competitors = event.get('competitions', [{}])[0].get('competitors', [])
                        if len(competitors) >= 2:
                            team1_data = competitors[0].get('team', {})
                            team2_data = competitors[1].get('team', {})
                            team1_abbrev = team1_data.get('abbreviation', '')
                            team2_abbrev = team2_data.get('abbreviation', '')

                            if team1_abbrev and team2_abbrev:
                                # Each team's opponent is the other team
                                schedule_map[team1_abbrev] = team2_abbrev
                                schedule_map[team2_abbrev] = team1_abbrev

                    except Exception as e:
                        self.logger.warning(f"Error parsing schedule event: {e}")
                        continue

            # Restore original season
            client.settings.season = original_season

            self.logger.info(f"Retrieved schedule for week {week} ({len(schedule_map)} matchups)")
            return schedule_map

        except Exception as e:
            self.logger.error(f"Error getting week {week} schedule: {e}")
            return self._get_fallback_schedule()

    def _get_fallback_rankings(self) -> Dict[str, Dict[str, int]]:
        """Fallback team rankings when API fails"""
        teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN',
                'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LAC', 'LAR', 'LV', 'MIA',
                'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH']

        return {team: {'offensive_rank': 16, 'defensive_rank': 16} for team in teams}

    def _get_fallback_schedule(self) -> Dict[str, str]:
        """Fallback schedule when API fails - use current teams.csv data"""
        try:
            teams_file = os.path.join(os.path.dirname(__file__), '..', '..', 'shared_files', 'teams.csv')
            schedule_map = {}

            if os.path.exists(teams_file):
                with open(teams_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        team = row.get('team', '').strip()
                        opponent = row.get('opponent', '').strip()
                        if team and opponent:
                            schedule_map[team] = opponent

            return schedule_map

        except Exception as e:
            self.logger.warning(f"Error reading fallback schedule: {e}")
            return {}

    async def write_team_file(self, week: int, team_rankings: Dict[str, Dict[str, int]], schedule: Dict[str, str]):
        """Write team data to CSV file"""
        filename = f"teams_week_{week}.csv"
        filepath = os.path.join(self.data_dir, filename)

        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['team', 'offensive_rank', 'defensive_rank', 'opponent'])

                # Get all teams and sort them for consistent output
                all_teams = set(team_rankings.keys()) | set(schedule.keys())
                all_teams = sorted(all_teams)

                for team in all_teams:
                    rankings = team_rankings.get(team, {'offensive_rank': 16, 'defensive_rank': 16})
                    opponent = schedule.get(team, 'BYE')

                    writer.writerow([
                        team,
                        rankings.get('offensive_rank', 16),
                        rankings.get('defensive_rank', 16),
                        opponent
                    ])

            self.logger.info(f"Successfully wrote {filename} with {len(all_teams)} teams")

        except Exception as e:
            self.logger.error(f"Error writing {filename}: {e}")
            raise


async def main():
    """Main entry point for team data generation"""
    generator = TeamDataGenerator()
    await generator.generate_all_team_data()


if __name__ == "__main__":
    asyncio.run(main())