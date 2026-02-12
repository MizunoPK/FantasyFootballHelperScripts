#!/usr/bin/env python3
"""
Schedule Fetcher for Historical Data Compiler

Fetches NFL season schedule from ESPN Scoreboard API.
Adapted from schedule-data-fetcher/ScheduleFetcher.py.

Author: Kai Mizuno
"""

import csv
from pathlib import Path
from typing import Dict, List, Set

from .http_client import BaseHTTPClient
from .constants import (
    ESPN_SCOREBOARD_API_URL,
    ALL_NFL_TEAMS,
    REGULAR_SEASON_WEEKS,
    SEASON_SCHEDULE_FILE,
    normalize_team_abbrev,
)

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


class ScheduleFetcher:
    """
    Fetches NFL season schedule from ESPN Scoreboard API.

    Creates season_schedule.csv with format:
        week,team,opponent
        1,ARI,BUF
        1,ATL,PIT
        ...
        6,KC,       # bye week (empty opponent)
    """

    def __init__(self, http_client: BaseHTTPClient):
        """
        Initialize ScheduleFetcher.

        Args:
            http_client: Shared HTTP client instance
        """
        self.http_client = http_client
        self.logger = get_logger()

    async def fetch_schedule(self, year: int) -> Dict[int, Dict[str, str]]:
        """
        Fetch complete season schedule for all weeks.

        Args:
            year: NFL season year (e.g., 2024)

        Returns:
            Dict[week_number, Dict[team, opponent]]
            Example: {1: {'KC': 'BAL', 'BAL': 'KC', ...}, 2: {...}, ...}
            Teams on bye are not included in that week's dict
        """
        self.logger.info(f"Fetching schedule for {year} season (weeks 1-{REGULAR_SEASON_WEEKS})")

        full_schedule: Dict[int, Dict[str, str]] = {}

        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            self.logger.debug(f"Fetching schedule for week {week}/{REGULAR_SEASON_WEEKS}")

            params = {
                "seasontype": 2,  # Regular season
                "week": week,
                "dates": year
            }

            data = await self.http_client.get(ESPN_SCOREBOARD_API_URL, params=params)

            # Parse schedule for this week
            week_schedule = self._parse_week_schedule(data, week)
            full_schedule[week] = week_schedule

        self.logger.info(f"Fetched schedule for {len(full_schedule)} weeks")
        return full_schedule

    def _parse_week_schedule(self, data: dict, week: int) -> Dict[str, str]:
        """
        Parse schedule for a single week from ESPN API response.

        Args:
            data: ESPN API response
            week: Week number (for logging)

        Returns:
            Dict mapping team to opponent for this week
        """
        week_schedule: Dict[str, str] = {}
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
                team1 = competitors[0].get('team', {}).get('abbreviation', '')
                team2 = competitors[1].get('team', {}).get('abbreviation', '')

                # Normalize team names
                team1 = normalize_team_abbrev(team1)
                team2 = normalize_team_abbrev(team2)

                if team1 and team2:
                    week_schedule[team1] = team2
                    week_schedule[team2] = team1

            except Exception as e:
                self.logger.warning(f"Error parsing event in week {week}: {e}")
                continue

        return week_schedule

    def identify_bye_weeks(self, schedule: Dict[int, Dict[str, str]]) -> Dict[str, int]:
        """
        Identify bye week for each team.

        Args:
            schedule: Full season schedule from fetch_schedule()

        Returns:
            Dict mapping team abbreviation to bye week number
        """
        bye_weeks: Dict[str, int] = {}

        for team in ALL_NFL_TEAMS:
            for week in range(1, REGULAR_SEASON_WEEKS + 1):
                week_schedule = schedule.get(week, {})
                if team not in week_schedule:
                    bye_weeks[team] = week
                    break  # Found bye week, move to next team

        return bye_weeks

    def write_schedule_csv(
        self,
        schedule: Dict[int, Dict[str, str]],
        output_path: Path
    ) -> None:
        """
        Write season_schedule.csv.

        CSV format:
            week,team,opponent
            1,ARI,BUF
            ...
            6,KC,       # bye week (empty opponent)

        Args:
            schedule: Full season schedule from fetch_schedule()
            output_path: Path to output CSV file
        """
        self.logger.info(f"Writing schedule to {output_path}")

        # Get bye weeks for all teams
        bye_weeks = self.identify_bye_weeks(schedule)

        rows: List[List] = []

        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            week_schedule = schedule.get(week, {})

            for team in sorted(ALL_NFL_TEAMS):
                if bye_weeks.get(team) == week:
                    # Bye week - empty opponent
                    rows.append([week, team, ''])
                else:
                    # Regular game
                    opponent = week_schedule.get(team, '')
                    rows.append([week, team, opponent])

        # Write CSV
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['week', 'team', 'opponent'])
            writer.writerows(rows)

        self.logger.info(f"Wrote {len(rows)} rows to {output_path}")


async def fetch_and_write_schedule(
    year: int,
    output_dir: Path,
    http_client: BaseHTTPClient
) -> Dict[int, Dict[str, str]]:
    """
    Convenience function to fetch schedule and write CSV.

    Args:
        year: NFL season year
        output_dir: Output directory
        http_client: HTTP client instance

    Returns:
        Schedule dict for use by other modules
    """
    fetcher = ScheduleFetcher(http_client)
    schedule = await fetcher.fetch_schedule(year)

    output_path = output_dir / SEASON_SCHEDULE_FILE
    fetcher.write_schedule_csv(schedule, output_path)

    return schedule
