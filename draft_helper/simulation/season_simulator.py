"""
Season simulation for head-to-head matchups after draft completion.

Simulates 17-week fantasy football season with weekly matchups between teams.
"""

import random
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared_files.FantasyPlayer import FantasyPlayer
from draft_helper.FantasyTeam import FantasyTeam
from shared_config import CURRENT_NFL_WEEK

@dataclass
class WeeklyMatchup:
    """Represents a single weekly matchup between two teams"""
    week: int
    team1_index: int
    team2_index: int
    team1_score: float
    team2_score: float
    winner_index: int

@dataclass
class TeamSeasonStats:
    """Season statistics for a single team"""
    team_index: int
    wins: int
    losses: int
    total_points: float
    weekly_scores: List[float]
    win_percentage: float
    points_per_game: float
    score_consistency: float  # Standard deviation

class SeasonSimulator:
    """Simulates a full fantasy football season after draft completion"""

    def __init__(self, teams: List[Any], current_nfl_week: int = None):
        self.teams = teams
        self.current_nfl_week = current_nfl_week or CURRENT_NFL_WEEK
        self.matchups: List[WeeklyMatchup] = []
        self.season_stats: Dict[int, TeamSeasonStats] = {}

    def simulate_full_season(self) -> Dict[str, Any]:
        """Simulate complete 17-week fantasy season"""

        # Generate schedule for 17 weeks
        schedule = self._generate_season_schedule()

        # Simulate each week
        for week in range(1, 18):  # Weeks 1-17
            weekly_matchups = schedule.get(week, [])
            for matchup in weekly_matchups:
                self._simulate_weekly_matchup(week, matchup)

        # Calculate season statistics
        self._calculate_season_stats()

        return self._generate_season_results()

    def _generate_season_schedule(self) -> Dict[int, List[Tuple[int, int]]]:
        """Generate 17-week schedule ensuring each team plays enough games"""

        schedule = {}
        num_teams = len(self.teams)

        for week in range(1, 18):
            weekly_matchups = []

            # Create all possible pairings for this week
            available_teams = list(range(num_teams))
            random.shuffle(available_teams)

            # Pair teams for matchups
            while len(available_teams) >= 2:
                team1 = available_teams.pop()
                team2 = available_teams.pop()
                weekly_matchups.append((team1, team2))

            # If odd number of teams, one team gets a bye (plays against average)
            if available_teams:
                bye_team = available_teams[0]
                # Create a "bye week" matchup against league average
                weekly_matchups.append((bye_team, -1))  # -1 represents bye/average

            schedule[week] = weekly_matchups

        return schedule

    def _simulate_weekly_matchup(self, week: int, matchup: Tuple[int, int]) -> None:
        """Simulate a single weekly matchup"""

        team1_index, team2_index = matchup

        # Calculate team scores for the week
        team1_score = self._calculate_weekly_score(team1_index, week)

        if team2_index == -1:
            # Bye week - compare against league average
            team2_score = self._calculate_league_average_score(week)
            team2_index = -1  # Keep as bye indicator
        else:
            team2_score = self._calculate_weekly_score(team2_index, week)

        # Determine winner
        if team1_score > team2_score:
            winner_index = team1_index
        elif team2_score > team1_score:
            winner_index = team2_index
        else:
            # Tie - random winner
            winner_index = random.choice([team1_index, team2_index])

        # Record the matchup
        weekly_matchup = WeeklyMatchup(
            week=week,
            team1_index=team1_index,
            team2_index=team2_index,
            team1_score=team1_score,
            team2_score=team2_score,
            winner_index=winner_index
        )

        self.matchups.append(weekly_matchup)

    def _calculate_weekly_score(self, team_index: int, week: int) -> float:
        """Calculate a team's total score for a specific week"""

        if team_index < 0 or team_index >= len(self.teams):
            return 0.0

        team = self.teams[team_index]
        total_score = 0.0

        # Get the optimal starting lineup for this week
        starting_lineup = self._get_optimal_starting_lineup(team.roster, week)

        for player in starting_lineup:
            player_score = self._get_player_week_points(player, week)

            # Apply bye week penalty if player is on bye
            if hasattr(player, 'bye_week') and player.bye_week == week:
                player_score = 0.0

            # Apply injury penalty if player is injured
            if hasattr(player, 'injury_status') and player.injury_status in ['MEDIUM', 'HIGH']:
                if player.injury_status == 'MEDIUM':
                    player_score *= 0.85  # 15% reduction for questionable
                elif player.injury_status == 'HIGH':
                    player_score *= 0.5   # 50% reduction for out/IR

            total_score += player_score

        return total_score

    def _get_optimal_starting_lineup(self, roster: FantasyTeam, week: int) -> List[FantasyPlayer]:
        """Get the optimal starting lineup for a team for a specific week"""

        # This should use the starter helper logic to get the best lineup
        # For now, use a simplified version

        starting_lineup = []
        available_players = roster.roster.copy()

        # Required starting positions based on league rules
        required_positions = {
            'QB': 1,
            'RB': 2,
            'WR': 2,
            'TE': 1,
            'FLEX': 1,  # Can be RB or WR
            'K': 1,
            'DST': 1
        }

        # Fill required positions
        for position, count in required_positions.items():
            if position == 'FLEX':
                # FLEX can be RB or WR
                flex_candidates = [p for p in available_players if p.position in ['RB', 'WR']]
                flex_candidates.sort(key=lambda p: self._get_player_week_points(p, week), reverse=True)

                for i in range(min(count, len(flex_candidates))):
                    player = flex_candidates[i]
                    starting_lineup.append(player)
                    available_players.remove(player)
            else:
                position_players = [p for p in available_players if p.position == position]
                position_players.sort(key=lambda p: self._get_player_week_points(p, week), reverse=True)

                for i in range(min(count, len(position_players))):
                    player = position_players[i]
                    starting_lineup.append(player)
                    available_players.remove(player)

        return starting_lineup

    def _calculate_league_average_score(self, week: int) -> float:
        """Calculate league average score for bye week comparisons"""

        total_scores = []

        for team_index in range(len(self.teams)):
            team_score = self._calculate_weekly_score(team_index, week)
            total_scores.append(team_score)

        if total_scores:
            return sum(total_scores) / len(total_scores)
        else:
            return 100.0  # Default fallback score

    def _calculate_season_stats(self) -> None:
        """Calculate season-long statistics for each team"""

        # Initialize stats for each team
        for team_index in range(len(self.teams)):
            self.season_stats[team_index] = TeamSeasonStats(
                team_index=team_index,
                wins=0,
                losses=0,
                total_points=0.0,
                weekly_scores=[],
                win_percentage=0.0,
                points_per_game=0.0,
                score_consistency=0.0
            )

        # Aggregate matchup results
        for matchup in self.matchups:
            # Update wins/losses
            if matchup.winner_index == matchup.team1_index:
                self.season_stats[matchup.team1_index].wins += 1
                if matchup.team2_index >= 0:  # Not a bye week
                    self.season_stats[matchup.team2_index].losses += 1
            elif matchup.winner_index == matchup.team2_index and matchup.team2_index >= 0:
                self.season_stats[matchup.team2_index].wins += 1
                self.season_stats[matchup.team1_index].losses += 1

            # Update total points and weekly scores
            self.season_stats[matchup.team1_index].total_points += matchup.team1_score
            self.season_stats[matchup.team1_index].weekly_scores.append(matchup.team1_score)

            if matchup.team2_index >= 0:  # Not a bye week
                self.season_stats[matchup.team2_index].total_points += matchup.team2_score
                self.season_stats[matchup.team2_index].weekly_scores.append(matchup.team2_score)

        # Calculate derived statistics
        for team_index, stats in self.season_stats.items():
            total_games = stats.wins + stats.losses
            if total_games > 0:
                stats.win_percentage = stats.wins / total_games
                stats.points_per_game = stats.total_points / total_games
            else:
                stats.win_percentage = 0.0
                stats.points_per_game = 0.0

            # Calculate score consistency (standard deviation)
            if len(stats.weekly_scores) > 1:
                mean_score = sum(stats.weekly_scores) / len(stats.weekly_scores)
                variance = sum((score - mean_score) ** 2 for score in stats.weekly_scores) / len(stats.weekly_scores)
                stats.score_consistency = variance ** 0.5
            else:
                stats.score_consistency = 0.0

    def _generate_season_results(self) -> Dict[str, Any]:
        """Generate summary of season simulation results"""

        results = {
            'season_stats': self.season_stats,
            'total_matchups': len(self.matchups),
            'weeks_simulated': 17,
            'team_rankings': self._rank_teams(),
            'matchup_details': self.matchups
        }

        return results

    def _rank_teams(self) -> List[Dict[str, Any]]:
        """Rank teams by performance"""

        rankings = []

        for team_index, stats in self.season_stats.items():
            team_info = {
                'team_index': team_index,
                'wins': stats.wins,
                'losses': stats.losses,
                'win_percentage': stats.win_percentage,
                'total_points': stats.total_points,
                'points_per_game': stats.points_per_game,
                'score_consistency': stats.score_consistency,
                'strategy': self.teams[team_index].strategy if hasattr(self.teams[team_index], 'strategy') else 'unknown'
            }
            rankings.append(team_info)

        # Sort by win percentage, then by total points
        rankings.sort(key=lambda x: (x['win_percentage'], x['total_points']), reverse=True)

        # Add ranking position
        for i, team in enumerate(rankings):
            team['rank'] = i + 1

        return rankings

    def _get_player_week_points(self, player: FantasyPlayer, week: int) -> float:
        """Get points for a player for a specific week"""
        week_attr = f'week_{week}_points'
        return getattr(player, week_attr, 0.0) or 0.0