#!/usr/bin/env python3
"""
Matchup Analysis Engine

Core logic for calculating 1-100 scale matchup ratings based on opponent defense,
recent trends, home/away advantage, and strength of schedule factors.

Author: Generated for Fantasy Football Helper Scripts
Last Updated: September 2025
"""

import logging
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from matchup_models import (
    TeamDefenseStats, WeeklyMatchup, PlayerMatchupContext, MatchupRating,
    WeeklyMatchupAnalysis, FantasyPosition, MatchupAnalysisConfig
)
from espn_matchup_client import ESPNMatchupClient
from starter_helper_config import (
    DEFENSE_STRENGTH_WEIGHT, RECENT_TREND_WEIGHT, HOME_FIELD_WEIGHT, SCHEDULE_STRENGTH_WEIGHT,
    HOME_FIELD_ADVANTAGE_BONUS, FAVORABLE_MATCHUP_THRESHOLD, RECENT_WEEKS_FOR_DEFENSE,
    NFL_SEASON
)


class MatchupAnalyzer:
    """Core matchup analysis engine for calculating player vs defense ratings"""

    def __init__(self, espn_client: Optional[ESPNMatchupClient] = None):
        self.logger = logging.getLogger(__name__)
        self.espn_client = espn_client or ESPNMatchupClient()

        # Analysis configuration
        self.config = MatchupAnalysisConfig(
            defense_strength_weight=DEFENSE_STRENGTH_WEIGHT,
            recent_trend_weight=RECENT_TREND_WEIGHT,
            home_field_weight=HOME_FIELD_WEIGHT,
            schedule_strength_weight=SCHEDULE_STRENGTH_WEIGHT,
            recent_weeks_for_defense=RECENT_WEEKS_FOR_DEFENSE,
            favorable_matchup_threshold=FAVORABLE_MATCHUP_THRESHOLD
        )

        # Validate configuration
        self.config.validate_weights_sum()

    async def analyze_player_matchup(self, player_context: PlayerMatchupContext,
                                   team_defenses: Dict[int, TeamDefenseStats],
                                   league_averages: Dict[FantasyPosition, float]) -> MatchupRating:
        """
        Analyze a single player's matchup and return comprehensive rating.

        Args:
            player_context: Player and opponent context information
            team_defenses: Dictionary of team defense statistics
            league_averages: League average points allowed by position

        Returns:
            MatchupRating with 1-100 scale overall rating and component breakdowns
        """
        self.logger.debug(f"Analyzing matchup for {player_context.player_name} vs {player_context.opponent_team_abbreviation}")

        try:
            # Get opponent defense stats
            opponent_defense = team_defenses.get(player_context.opponent_team_id)
            if not opponent_defense:
                self.logger.warning(f"No defense stats found for team {player_context.opponent_team_id}")
                return self._create_default_rating(player_context)

            # Calculate component ratings
            defense_rating = self._calculate_defense_strength_rating(
                player_context, opponent_defense, league_averages
            )

            trend_rating = self._calculate_recent_trend_rating(
                player_context, opponent_defense, league_averages
            )

            home_field_rating = self._calculate_home_field_rating(player_context)

            schedule_rating = self._calculate_schedule_strength_rating(
                player_context, opponent_defense, team_defenses
            )

            # Calculate overall weighted rating
            overall_rating = (
                defense_rating * self.config.defense_strength_weight +
                trend_rating * self.config.recent_trend_weight +
                home_field_rating * self.config.home_field_weight +
                schedule_rating * self.config.schedule_strength_weight
            )

            # Ensure rating is within 1-100 bounds
            overall_rating = max(1.0, min(100.0, overall_rating))

            # Get detailed metrics
            opponent_points_allowed = opponent_defense.get_points_allowed_by_position(player_context.player_position)
            league_average = league_averages.get(player_context.player_position, 12.0)
            points_above_average = opponent_points_allowed - league_average

            # Calculate trend information
            recent_opponent_average = opponent_defense.get_recent_trend_by_position(player_context.player_position)
            trend_direction, trend_magnitude = self._analyze_trend_direction(
                opponent_points_allowed, recent_opponent_average
            )

            # Calculate confidence score based on data quality
            confidence_score = self._calculate_confidence_score(opponent_defense)

            # Create comprehensive matchup rating
            rating = MatchupRating(
                player_context=player_context,
                overall_rating=overall_rating,
                defense_strength_rating=defense_rating,
                recent_trend_rating=trend_rating,
                home_field_rating=home_field_rating,
                schedule_strength_rating=schedule_rating,
                opponent_points_allowed=opponent_points_allowed,
                league_average_allowed=league_average,
                points_above_average=points_above_average,
                recent_opponent_average=recent_opponent_average,
                trend_direction=trend_direction,
                trend_magnitude=trend_magnitude,
                home_field_advantage=HOME_FIELD_ADVANTAGE_BONUS if player_context.is_home_game else 0.0,
                weather_impact=0.0,  # Future enhancement
                venue_impact=0.0,    # Future enhancement
                confidence_score=confidence_score,
                sample_size=opponent_defense.games_played
            )

            self.logger.debug(f"Matchup rating for {player_context.player_name}: {overall_rating:.1f}")
            return rating

        except Exception as e:
            self.logger.error(f"Error analyzing matchup for {player_context.player_name}: {e}")
            return self._create_default_rating(player_context)

    def _calculate_defense_strength_rating(self, player_context: PlayerMatchupContext,
                                         opponent_defense: TeamDefenseStats,
                                         league_averages: Dict[FantasyPosition, float]) -> float:
        """
        Calculate defense strength rating (1-100).
        Higher rating = worse defense (better matchup for player).
        """
        position = player_context.player_position
        opponent_points_allowed = opponent_defense.get_points_allowed_by_position(position)
        league_average = league_averages.get(position, 12.0)

        # Calculate how much more/less this defense allows compared to league average
        # Positive difference = defense allows more points = better matchup
        difference_from_average = opponent_points_allowed - league_average

        # Convert to 1-100 scale where higher = better matchup
        # Base rating of 50 for league average defense
        base_rating = 50.0

        # Each point above/below average adjusts rating by ~3 points
        rating_adjustment = difference_from_average * 3.0

        rating = base_rating + rating_adjustment

        # Ensure bounds and add some variance for realism
        rating = max(10.0, min(90.0, rating))

        return rating

    def _calculate_recent_trend_rating(self, player_context: PlayerMatchupContext,
                                     opponent_defense: TeamDefenseStats,
                                     league_averages: Dict[FantasyPosition, float]) -> float:
        """
        Calculate recent trend rating (1-100).
        Analyzes if defense is getting better or worse recently.
        """
        position = player_context.player_position
        recent_average = opponent_defense.get_recent_trend_by_position(position)
        season_average = opponent_defense.get_points_allowed_by_position(position)

        if recent_average == 0.0 or season_average == 0.0:
            return 50.0  # Default neutral rating

        # Compare recent trend to season average
        trend_difference = recent_average - season_average

        # Base rating of 50 for no trend
        base_rating = 50.0

        # Positive trend difference = defense allowing more recently = better matchup
        trend_adjustment = trend_difference * 4.0

        rating = base_rating + trend_adjustment

        # Weight by number of recent games analyzed
        games_analyzed = opponent_defense.recent_games_analyzed
        if games_analyzed < 3:
            # Less confident in trend with fewer games
            rating = (rating + 50.0) / 2.0

        rating = max(10.0, min(90.0, rating))
        return rating

    def _calculate_home_field_rating(self, player_context: PlayerMatchupContext) -> float:
        """
        Calculate home field advantage rating (1-100).
        Home games generally provide slight advantage.
        """
        base_rating = 50.0

        if player_context.is_home_game:
            # Home field advantage
            rating = base_rating + (HOME_FIELD_ADVANTAGE_BONUS * 2.0)
        else:
            # Away game slight disadvantage
            rating = base_rating - (HOME_FIELD_ADVANTAGE_BONUS * 1.0)

        # Home/away effect is generally modest in fantasy football
        rating = max(40.0, min(60.0, rating))
        return rating

    def _calculate_schedule_strength_rating(self, player_context: PlayerMatchupContext,
                                          opponent_defense: TeamDefenseStats,
                                          all_team_defenses: Dict[int, TeamDefenseStats]) -> float:
        """
        Calculate strength of schedule rating (1-100).
        Considers how this defense ranks relative to other defenses.
        """
        position = player_context.player_position

        if len(all_team_defenses) < 10:
            return 50.0  # Not enough data for meaningful comparison

        # Get all defenses' points allowed for this position
        defense_rankings = []
        for team_id, defense in all_team_defenses.items():
            points_allowed = defense.get_points_allowed_by_position(position)
            defense_rankings.append((team_id, points_allowed))

        # Sort by points allowed (ascending = better defense, worse matchup)
        defense_rankings.sort(key=lambda x: x[1])

        # Find opponent's rank (0-indexed)
        opponent_rank = None
        for i, (team_id, points) in enumerate(defense_rankings):
            if team_id == player_context.opponent_team_id:
                opponent_rank = i
                break

        if opponent_rank is None:
            return 50.0

        # Convert rank to 1-100 rating
        # Worst defense (highest rank) = best matchup = highest rating
        total_teams = len(defense_rankings)
        percentile = (total_teams - opponent_rank - 1) / max(1, total_teams - 1)

        # Scale percentile to rating range 20-80 (avoid extremes)
        rating = 20.0 + (percentile * 60.0)

        return rating

    def _analyze_trend_direction(self, season_average: float, recent_average: float) -> Tuple[str, float]:
        """Analyze trend direction and magnitude"""
        if recent_average == 0.0 or season_average == 0.0:
            return "stable", 0.0

        difference = recent_average - season_average
        magnitude = abs(difference)

        if magnitude < 1.0:
            return "stable", magnitude
        elif difference > 0:
            return "declining", magnitude  # Allowing more points recently
        else:
            return "improving", magnitude  # Allowing fewer points recently

    def _calculate_confidence_score(self, opponent_defense: TeamDefenseStats) -> float:
        """Calculate confidence score based on data quality"""
        base_confidence = 70.0

        # Adjust based on games played (more games = higher confidence)
        games_played = opponent_defense.games_played
        if games_played >= 8:
            games_adjustment = 20.0
        elif games_played >= 4:
            games_adjustment = 10.0
        elif games_played >= 2:
            games_adjustment = 0.0
        else:
            games_adjustment = -20.0

        # Adjust based on recent games analyzed
        recent_games = opponent_defense.recent_games_analyzed
        if recent_games >= 3:
            recent_adjustment = 10.0
        elif recent_games >= 1:
            recent_adjustment = 0.0
        else:
            recent_adjustment = -10.0

        confidence = base_confidence + games_adjustment + recent_adjustment
        return max(30.0, min(95.0, confidence))

    def _create_default_rating(self, player_context: PlayerMatchupContext) -> MatchupRating:
        """Create default neutral rating when data is unavailable"""
        return MatchupRating(
            player_context=player_context,
            overall_rating=50.0,
            defense_strength_rating=50.0,
            recent_trend_rating=50.0,
            home_field_rating=50.0,
            schedule_strength_rating=50.0,
            opponent_points_allowed=12.0,
            league_average_allowed=12.0,
            points_above_average=0.0,
            recent_opponent_average=12.0,
            trend_direction="stable",
            trend_magnitude=0.0,
            home_field_advantage=0.0,
            weather_impact=0.0,
            venue_impact=0.0,
            confidence_score=30.0,
            sample_size=0
        )

    async def analyze_weekly_matchups(self, roster_players: List[Dict[str, Any]],
                                    week: Optional[int] = None) -> WeeklyMatchupAnalysis:
        """
        Analyze matchups for all roster players for a specific week.

        Args:
            roster_players: List of player dictionaries with id, name, position, team_id
            week: NFL week number (defaults to current week)

        Returns:
            WeeklyMatchupAnalysis with all player ratings and analysis metadata
        """
        analysis_start = datetime.now()
        target_week = week or self.espn_client.CURRENT_NFL_WEEK

        self.logger.info(f"Starting weekly matchup analysis for {len(roster_players)} players, week {target_week}")

        try:
            # Fetch required data
            self.logger.info("Fetching team defense statistics...")
            team_defenses = await self.espn_client.fetch_team_defense_stats()

            self.logger.info("Fetching weekly schedule...")
            weekly_matchups = await self.espn_client.fetch_current_week_schedule(target_week)

            # Calculate league averages
            self.logger.info("Calculating league averages...")
            league_averages = await self._calculate_league_averages(team_defenses)

            # Analyze each player
            player_ratings = []
            for player_data in roster_players:
                try:
                    player_rating = await self._analyze_roster_player(
                        player_data, target_week, team_defenses, league_averages
                    )
                    if player_rating:
                        player_ratings.append(player_rating)
                except Exception as e:
                    self.logger.warning(f"Failed to analyze player {player_data.get('name', 'unknown')}: {e}")
                    continue

            # Calculate analysis metadata
            analysis_end = datetime.now()
            runtime_seconds = (analysis_end - analysis_start).total_seconds()

            confidence_scores = [r.confidence_score for r in player_ratings]
            average_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0

            # Create comprehensive analysis
            analysis = WeeklyMatchupAnalysis(
                week=target_week,
                season=NFL_SEASON,
                player_ratings=player_ratings,
                team_defenses=team_defenses,
                weekly_matchups=weekly_matchups,
                total_players_analyzed=len(player_ratings),
                average_confidence=average_confidence,
                analysis_runtime_seconds=runtime_seconds
            )

            self.logger.info(f"Completed weekly matchup analysis: {len(player_ratings)} players, "
                           f"{runtime_seconds:.1f}s, {average_confidence:.1f}% avg confidence")

            return analysis

        except Exception as e:
            self.logger.error(f"Failed to complete weekly matchup analysis: {e}")
            raise

    async def _analyze_roster_player(self, player_data: Dict[str, Any], week: int,
                                   team_defenses: Dict[int, TeamDefenseStats],
                                   league_averages: Dict[FantasyPosition, float]) -> Optional[MatchupRating]:
        """Analyze matchup for a single roster player"""
        try:
            # Extract player information
            player_id = str(player_data.get('id', ''))
            player_name = player_data.get('name', 'Unknown Player')
            player_position = FantasyPosition(player_data.get('position', 'FLEX'))
            player_team_id = int(player_data.get('team_id', 0))

            if not all([player_id, player_name, player_team_id]):
                self.logger.warning(f"Missing required player data: {player_data}")
                return None

            # Create player matchup context
            player_context = await self.espn_client.create_player_matchup_context(
                player_id=player_id,
                player_name=player_name,
                player_position=player_position,
                player_team_id=player_team_id,
                week=week
            )

            if not player_context:
                self.logger.warning(f"Could not create matchup context for {player_name}")
                return None

            # Update injury status if available
            injury_status = player_data.get('injury_status', 'ACTIVE')
            if injury_status in ['OUT', 'IR', 'SUSPENDED']:
                player_context.is_available = False

            # Analyze the matchup
            return await self.analyze_player_matchup(player_context, team_defenses, league_averages)

        except Exception as e:
            self.logger.error(f"Error analyzing roster player {player_data.get('name', 'unknown')}: {e}")
            return None

    async def _calculate_league_averages(self, team_defenses: Dict[int, TeamDefenseStats]) -> Dict[FantasyPosition, float]:
        """Calculate league average points allowed by position"""
        if not team_defenses:
            # Return default averages if no data
            return {
                FantasyPosition.QB: 18.0,
                FantasyPosition.RB: 14.0,
                FantasyPosition.WR: 13.5,
                FantasyPosition.TE: 9.0,
                FantasyPosition.K: 7.5,
                FantasyPosition.DST: 10.0,
                FantasyPosition.FLEX: 13.5
            }

        league_averages = {}
        positions = [FantasyPosition.QB, FantasyPosition.RB, FantasyPosition.WR,
                    FantasyPosition.TE, FantasyPosition.K, FantasyPosition.DST]

        for position in positions:
            position_values = []
            for defense in team_defenses.values():
                points_allowed = defense.get_points_allowed_by_position(position)
                position_values.append(points_allowed)

            if position_values:
                league_averages[position] = sum(position_values) / len(position_values)
            else:
                league_averages[position] = 12.0  # Default fallback

        # FLEX is average of RB/WR/TE
        flex_avg = (league_averages[FantasyPosition.RB] + league_averages[FantasyPosition.WR] +
                   league_averages[FantasyPosition.TE]) / 3.0
        league_averages[FantasyPosition.FLEX] = flex_avg

        return league_averages

    def get_matchup_display_indicator(self, rating: float) -> str:
        """Get simple display indicator for matchup rating"""
        if rating >= 75:
            return "**"   # Excellent matchup
        elif rating >= 65:
            return "*"    # Good matchup
        elif rating >= 50:
            return "o"    # Average matchup
        elif rating >= 35:
            return "-"    # Below average matchup
        else:
            return "x"    # Poor matchup

    def format_matchup_summary(self, rating: MatchupRating, show_detailed: bool = False) -> str:
        """Format matchup rating for display in starter helper output"""
        indicator = self.get_matchup_display_indicator(rating.overall_rating)

        basic_info = f"{indicator} {rating.overall_rating:.0f}"

        if not show_detailed:
            return basic_info

        # Detailed format
        return (f"{basic_info} vs {rating.player_context.opponent_team_abbreviation} "
                f"({'H' if rating.player_context.is_home_game else 'A'}) "
                f"[{rating.get_rating_description()}, {rating.trend_direction}]")

    async def close(self):
        """Close the ESPN client connection"""
        if self.espn_client:
            await self.espn_client.close()