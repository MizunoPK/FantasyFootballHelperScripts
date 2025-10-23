#!/usr/bin/env python3
"""
Schedule Data Fetcher

Fetches complete NFL season schedule from ESPN API and exports to season_schedule.csv.
Uses same async HTTP patterns as PlayerDataFetcher for consistency.

Author: Kai Mizuno
"""

import asyncio
import csv
from pathlib import Path
from typing import Dict, Optional, Set
from utils.LoggingManager import setup_logger
import httpx


class ScheduleFetcher:
    """
    Fetches and exports NFL season schedule data.

    This class fetches the complete NFL season schedule from ESPN's API
    and exports it to a CSV file for use by the league helper system.
    """

    def __init__(self, output_path: Path):
        """
        Initialize the ScheduleFetcher.

        Args:
            output_path: Path where season_schedule.csv will be written
        """
        self.output_path = output_path
        self.logger = setup_logger(name="ScheduleFetcher", level="INFO")
        self.client: Optional[httpx.AsyncClient] = None

    async def _create_client(self):
        """Create httpx async client if not already created."""
        if self.client is None:
            self.client = httpx.AsyncClient(timeout=30.0)

    async def _close_client(self):
        """Close httpx async client if open."""
        if self.client:
            await self.client.aclose()
            self.client = None

    async def _make_request(self, url: str, params: dict) -> dict:
        """
        Make an HTTP GET request to ESPN API.

        Args:
            url: API endpoint URL
            params: Query parameters

        Returns:
            JSON response as dictionary

        Raises:
            Exception: If request fails
        """
        await self._create_client()

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            self.logger.error(f"HTTP request failed: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to parse response: {e}")
            raise

    async def fetch_full_schedule(self, season: int) -> Dict[int, Dict[str, str]]:
        """
        Fetch complete season schedule for all weeks.

        Args:
            season: NFL season year (e.g., 2024)

        Returns:
            Dict[week_number, Dict[team, opponent]]
            Example: {1: {'KC': 'BAL', 'BAL': 'KC', ...}, 2: {...}, ...}
            Bye weeks are represented by missing team entries in that week
        """
        try:
            full_schedule = {}

            self.logger.info("Fetching full season schedule (weeks 1-18)")

            for week in range(1, 19):  # Weeks 1-18
                self.logger.debug(f"Fetching schedule for week {week}/18")

                # ESPN scoreboard API endpoint
                url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
                params = {
                    "seasontype": 2,  # Regular season
                    "week": week,
                    "dates": season
                }

                data = await self._make_request(url, params)

                # Parse schedule for this week
                week_schedule = {}
                events = data.get('events', [])

                for event in events:
                    try:
                        competitions = event.get('competitions', [])
                        if not competitions:
                            continue

                        competition = competitions[0]
                        competitors = competition.get('competitors', [])

                        if len(competitors) != 2:
                            continue

                        # Get team abbreviations
                        team1_data = competitors[0].get('team', {})
                        team2_data = competitors[1].get('team', {})

                        team1 = team1_data.get('abbreviation', '')
                        team2 = team2_data.get('abbreviation', '')

                        # Normalize team names (ESPN uses WAS, we use WSH)
                        team1 = 'WSH' if team1 == 'WAS' else team1
                        team2 = 'WSH' if team2 == 'WAS' else team2

                        if team1 and team2:
                            week_schedule[team1] = team2
                            week_schedule[team2] = team1

                    except Exception as e:
                        self.logger.debug(f"Error parsing event in week {week}: {e}")
                        continue

                full_schedule[week] = week_schedule

                # Rate limiting between requests
                await asyncio.sleep(0.2)

            self.logger.info(f"Successfully fetched schedule for {len(full_schedule)} weeks")

            # Close client after all requests complete
            await self._close_client()

            return full_schedule

        except Exception as e:
            self.logger.error(f"Failed to fetch full season schedule: {e}")
            await self._close_client()
            return {}

    def _identify_bye_weeks(self, schedule: Dict[int, Dict[str, str]]) -> Dict[str, Set[int]]:
        """
        Identify bye weeks for each team.

        Args:
            schedule: Full season schedule

        Returns:
            Dict mapping team abbreviation to set of bye week numbers
        """
        # All 32 NFL teams
        all_teams = {
            'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
            'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
            'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
            'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
        }

        bye_weeks: Dict[str, Set[int]] = {team: set() for team in all_teams}

        # For each week, check which teams don't have games
        for week in range(1, 18):  # Weeks 1-17 (18 is typically playoffs)
            week_schedule = schedule.get(week, {})
            teams_playing = set(week_schedule.keys())

            # Teams not in this week's schedule have a bye
            for team in all_teams:
                if team not in teams_playing:
                    bye_weeks[team].add(week)

        return bye_weeks

    def export_to_csv(self, schedule: Dict[int, Dict[str, str]]):
        """
        Export season_schedule.csv with complete schedule including bye weeks.

        CSV Schema:
            week,team,opponent
            1,KC,BAL
            1,BAL,KC
            5,KC,        # Bye week (empty opponent)

        Args:
            schedule: Full season schedule from fetch_full_schedule()
        """
        try:
            # Identify bye weeks
            bye_weeks = self._identify_bye_weeks(schedule)

            # Ensure output directory exists
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['week', 'team', 'opponent'])

                # Write schedule entries for weeks 1-17
                for week in range(1, 18):
                    week_schedule = schedule.get(week, {})

                    # Get all teams (including those on bye)
                    all_teams = {
                        'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
                        'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
                        'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
                        'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
                    }

                    # Write entries for all teams (sorted for consistency)
                    for team in sorted(all_teams):
                        if week in bye_weeks.get(team, set()):
                            # Bye week - empty opponent
                            writer.writerow([week, team, ''])
                        else:
                            # Regular game
                            opponent = week_schedule.get(team, '')
                            writer.writerow([week, team, opponent])

            self.logger.info(f"Schedule exported to {self.output_path}")

        except Exception as e:
            self.logger.error(f"Failed to export schedule to CSV: {e}")
            raise
