"""
Season simulation for head-to-head matchups after draft completion.

Simulates 17-week fantasy football season with weekly matchups between teams.
"""

import random
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import sys
import os
import logging

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared_files.FantasyPlayer import FantasyPlayer
from draft_helper.FantasyTeam import FantasyTeam
from shared_files.configs.shared_config import CURRENT_NFL_WEEK

# Import starter_helper components for lineup optimization
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'starter_helper'))
from lineup_optimizer import LineupOptimizer, OptimalLineup, StartingRecommendation

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

    def __init__(self, teams: List[Any], players_projected_df: pd.DataFrame, players_actual_df: pd.DataFrame, current_nfl_week: int = None):
        self.teams = teams
        self.players_projected_df = players_projected_df
        self.players_actual_df = players_actual_df
        self.current_nfl_week = current_nfl_week or CURRENT_NFL_WEEK
        self.matchups: List[WeeklyMatchup] = []
        self.season_stats: Dict[int, TeamSeasonStats] = {}

        # Initialize data manager for weekly teams data access
        sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
        from data_manager import SimulationDataManager
        self.data_manager = SimulationDataManager()

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
            # Use actual data for final scoring to determine winners
            player_score = self._get_player_week_points_from_df(player, week, use_actual=True)

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
        """
        Get the optimal starting lineup for a team for a specific week using starter_helper logic.

        Uses projected data for current week projections, but actual data for consistency calculations.
        This ensures consistency scoring reflects real performance variance, not projected variance.
        """

        # Convert roster to DataFrame format expected by LineupOptimizer
        roster_data = []
        for player in roster.roster:
            player_dict = {
                'id': player.id,
                'name': player.name,
                'position': player.position,
                'team': player.team,
                'injury_status': getattr(player, 'injury_status', 'ACTIVE'),
                'bye_week': getattr(player, 'bye_week', 0)
            }

            # Add actual weekly points data for consistency calculation
            # Consistency should use ACTUAL performance data, not projections
            for hist_week in range(1, week):  # Only weeks that have occurred
                week_attr = f'week_{hist_week}_points'
                # Get actual points from actual dataframe
                actual_points = self._get_player_week_points_from_df(player, hist_week, use_actual=True)
                player_dict[week_attr] = actual_points

            roster_data.append(player_dict)

        roster_df = pd.DataFrame(roster_data)

        # Create projections dictionary for this week using projected data
        projections = {}
        for player in roster.roster:
            week_attr = f'week_{week}_points'
            # Use projected data for lineup decisions
            projected_points = self._get_player_week_points_from_df(player, week, use_actual=False)
            projections[str(player.id)] = projected_points

        # Create a lineup optimizer with the appropriate weekly teams data
        weekly_teams_csv = self.data_manager.teams_weekly_csvs[week]
        weekly_lineup_optimizer = self._create_weekly_lineup_optimizer(weekly_teams_csv)

        # Use lineup optimizer to get optimal lineup
        optimal_lineup = weekly_lineup_optimizer.optimize_lineup(roster_df, projections)

        # Convert back to list of FantasyPlayer objects
        starting_lineup = []
        starting_recommendations = optimal_lineup.get_all_starters()

        for recommendation in starting_recommendations:
            if recommendation:
                # Find the corresponding FantasyPlayer object
                player_id = recommendation.player_id
                matching_player = None
                for player in roster.roster:
                    if str(player.id) == player_id:
                        matching_player = player
                        break

                if matching_player:
                    starting_lineup.append(matching_player)

        return starting_lineup

    def _create_weekly_lineup_optimizer(self, weekly_teams_csv_path: str) -> LineupOptimizer:
        """Create a LineupOptimizer with weekly teams data for positional rankings"""
        # Create a temporary class to override the LineupOptimizer initialization
        class WeeklyLineupOptimizer(LineupOptimizer):
            def __init__(self, teams_csv_path: str):
                # Initialize logger first
                self.logger = logging.getLogger(__name__)

                # Initialize matchup calculator with weekly teams data
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'starter_helper'))
                from matchup_calculator import MatchupCalculator
                self.matchup_calculator = MatchupCalculator(teams_csv_path=teams_csv_path)

                if self.matchup_calculator.is_matchup_available():
                    self.logger.debug(f"Matchup calculator initialized with weekly teams data: {teams_csv_path}")

                # Initialize positional ranking calculator with weekly teams data
                try:
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
                    from shared_files.positional_ranking_calculator import PositionalRankingCalculator
                    self.positional_ranking_calculator = PositionalRankingCalculator(teams_file_path=teams_csv_path)
                    if self.positional_ranking_calculator.is_positional_ranking_available():
                        self.logger.debug(f"Positional ranking calculations enabled with weekly teams data: {teams_csv_path}")
                    else:
                        self.logger.debug(f"Positional ranking calculations disabled (weekly teams.csv not available): {teams_csv_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize positional ranking calculator with weekly teams data: {e}")
                    self.positional_ranking_calculator = None

        return WeeklyLineupOptimizer(weekly_teams_csv_path)

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
        """Get points for a player for a specific week from actual data (for final scoring)"""
        week_attr = f'week_{week}_points'
        return getattr(player, week_attr, 0.0) or 0.0

    def _get_player_week_points_from_df(self, player: FantasyPlayer, week: int, use_actual: bool = True) -> float:
        """Get points for a player from either projected or actual dataframe"""
        player_df = self.players_actual_df if use_actual else self.players_projected_df

        # Find player in dataframe
        player_row = player_df[player_df['id'] == player.id]
        if player_row.empty:
            return 0.0

        week_col = f'week_{week}_points'
        if week_col in player_row.columns:
            points = player_row[week_col].iloc[0]
            return float(points) if pd.notna(points) else 0.0

        return 0.0