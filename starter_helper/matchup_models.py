#!/usr/bin/env python3
"""
Matchup Analysis Data Models

Pydantic models for ESPN matchup data, defense statistics, and matchup ratings.
These models provide type safety and validation for the matchup analysis engine.

Author: Generated for Fantasy Football Helper Scripts
Last Updated: September 2025
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class InjuryStatus(str, Enum):
    """Player injury status enumeration"""
    ACTIVE = "ACTIVE"
    QUESTIONABLE = "QUESTIONABLE"
    DOUBTFUL = "DOUBTFUL"
    OUT = "OUT"
    IR = "IR"
    SUSPENDED = "SUSPENDED"
    PUP = "PUP"


class FantasyPosition(str, Enum):
    """Fantasy football positions"""
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"
    K = "K"
    DST = "DST"
    FLEX = "FLEX"


class HomeAwayStatus(str, Enum):
    """Home/Away game status"""
    HOME = "home"
    AWAY = "away"


class GameStatus(str, Enum):
    """NFL game status"""
    SCHEDULED = "STATUS_SCHEDULED"
    IN_PROGRESS = "STATUS_IN_PROGRESS"
    FINAL = "STATUS_FINAL"
    POSTPONED = "STATUS_POSTPONED"
    CANCELED = "STATUS_CANCELED"


class TeamDefenseStats(BaseModel):
    """Team defense statistics for fantasy points allowed by position"""
    team_id: int = Field(..., description="ESPN team ID")
    team_name: str = Field(..., description="Team name (e.g., 'Chiefs')")
    team_abbreviation: str = Field(..., description="Team abbreviation (e.g., 'KC')")

    # Fantasy points allowed by position (per game averages)
    qb_points_allowed: float = Field(0.0, description="Fantasy points allowed to QBs per game")
    rb_points_allowed: float = Field(0.0, description="Fantasy points allowed to RBs per game")
    wr_points_allowed: float = Field(0.0, description="Fantasy points allowed to WRs per game")
    te_points_allowed: float = Field(0.0, description="Fantasy points allowed to TEs per game")
    k_points_allowed: float = Field(0.0, description="Fantasy points allowed to Ks per game")
    dst_points_allowed: float = Field(0.0, description="Fantasy points allowed to DSTs per game")

    # Recent performance trends (last 4 weeks)
    recent_qb_trend: float = Field(0.0, description="Recent QB points allowed trend")
    recent_rb_trend: float = Field(0.0, description="Recent RB points allowed trend")
    recent_wr_trend: float = Field(0.0, description="Recent WR points allowed trend")
    recent_te_trend: float = Field(0.0, description="Recent TE points allowed trend")
    recent_k_trend: float = Field(0.0, description="Recent K points allowed trend")
    recent_dst_trend: float = Field(0.0, description="Recent DST points allowed trend")

    # Additional context
    games_played: int = Field(0, description="Number of games played this season")
    recent_games_analyzed: int = Field(0, description="Number of recent games in trend analysis")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    @validator('team_id')
    def validate_team_id(cls, v):
        if v < 1 or v > 34:
            raise ValueError(f'Invalid ESPN team ID: {v}')
        return v

    def get_points_allowed_by_position(self, position: FantasyPosition) -> float:
        """Get fantasy points allowed for a specific position"""
        position_mapping = {
            FantasyPosition.QB: self.qb_points_allowed,
            FantasyPosition.RB: self.rb_points_allowed,
            FantasyPosition.WR: self.wr_points_allowed,
            FantasyPosition.TE: self.te_points_allowed,
            FantasyPosition.K: self.k_points_allowed,
            FantasyPosition.DST: self.dst_points_allowed,
            FantasyPosition.FLEX: max(self.rb_points_allowed, self.wr_points_allowed, self.te_points_allowed)
        }
        return position_mapping.get(position, 0.0)

    def get_recent_trend_by_position(self, position: FantasyPosition) -> float:
        """Get recent trend for a specific position"""
        trend_mapping = {
            FantasyPosition.QB: self.recent_qb_trend,
            FantasyPosition.RB: self.recent_rb_trend,
            FantasyPosition.WR: self.recent_wr_trend,
            FantasyPosition.TE: self.recent_te_trend,
            FantasyPosition.K: self.recent_k_trend,
            FantasyPosition.DST: self.recent_dst_trend,
            FantasyPosition.FLEX: max(self.recent_rb_trend, self.recent_wr_trend, self.recent_te_trend)
        }
        return trend_mapping.get(position, 0.0)


class WeeklyMatchup(BaseModel):
    """NFL team matchup information for a specific week"""
    week: int = Field(..., description="NFL week number")
    season: int = Field(..., description="NFL season year")

    home_team_id: int = Field(..., description="Home team ESPN ID")
    home_team_name: str = Field(..., description="Home team name")
    home_team_abbreviation: str = Field(..., description="Home team abbreviation")

    away_team_id: int = Field(..., description="Away team ESPN ID")
    away_team_name: str = Field(..., description="Away team name")
    away_team_abbreviation: str = Field(..., description="Away team abbreviation")

    game_date: datetime = Field(..., description="Game date and time")
    game_status: GameStatus = Field(GameStatus.SCHEDULED, description="Current game status")

    # Venue information
    venue_name: Optional[str] = Field(None, description="Stadium name")
    venue_city: Optional[str] = Field(None, description="Stadium city")
    is_indoor: Optional[bool] = Field(None, description="Whether stadium is indoor")

    # Weather information (if available)
    temperature: Optional[int] = Field(None, description="Temperature in Fahrenheit")
    weather_condition: Optional[str] = Field(None, description="Weather description")

    @validator('week')
    def validate_week(cls, v):
        if v < 1 or v > 22:
            raise ValueError(f'Invalid NFL week: {v}')
        return v

    def get_opponent_for_team(self, team_id: int) -> Optional[Dict[str, Any]]:
        """Get opponent information for a given team ID"""
        if team_id == self.home_team_id:
            return {
                'team_id': self.away_team_id,
                'team_name': self.away_team_name,
                'team_abbreviation': self.away_team_abbreviation,
                'home_away': HomeAwayStatus.AWAY
            }
        elif team_id == self.away_team_id:
            return {
                'team_id': self.home_team_id,
                'team_name': self.home_team_name,
                'team_abbreviation': self.home_team_abbreviation,
                'home_away': HomeAwayStatus.HOME
            }
        return None

    def is_home_team(self, team_id: int) -> bool:
        """Check if the given team is playing at home"""
        return team_id == self.home_team_id


class PlayerMatchupContext(BaseModel):
    """Context information for a player's matchup"""
    player_id: str = Field(..., description="ESPN player ID")
    player_name: str = Field(..., description="Player full name")
    player_position: FantasyPosition = Field(..., description="Player's fantasy position")
    player_team_id: int = Field(..., description="Player's team ESPN ID")
    player_team_abbreviation: str = Field(..., description="Player's team abbreviation")

    # Opponent information
    opponent_team_id: int = Field(..., description="Opponent team ESPN ID")
    opponent_team_name: str = Field(..., description="Opponent team name")
    opponent_team_abbreviation: str = Field(..., description="Opponent team abbreviation")

    # Game context
    is_home_game: bool = Field(..., description="Whether player is playing at home")
    week: int = Field(..., description="NFL week number")
    game_date: datetime = Field(..., description="Game date and time")

    # Optional player status
    injury_status: Optional[InjuryStatus] = Field(InjuryStatus.ACTIVE, description="Player injury status")
    is_available: bool = Field(True, description="Whether player is available to play")


class MatchupRating(BaseModel):
    """Comprehensive matchup rating for a player"""
    player_context: PlayerMatchupContext = Field(..., description="Player and matchup context")

    # Core rating (1-100 scale)
    overall_rating: float = Field(..., description="Overall matchup rating (1-100, higher is better)")

    # Component ratings (1-100 scale each)
    defense_strength_rating: float = Field(..., description="Opponent defense strength vs position")
    recent_trend_rating: float = Field(..., description="Recent defensive performance trend")
    home_field_rating: float = Field(..., description="Home/away advantage factor")
    schedule_strength_rating: float = Field(..., description="Strength of schedule adjustment")

    # Detailed breakdown
    opponent_points_allowed: float = Field(..., description="Fantasy points allowed by opponent to this position")
    league_average_allowed: float = Field(..., description="League average points allowed to this position")
    points_above_average: float = Field(..., description="How many points above/below average opponent allows")

    # Trend analysis
    recent_opponent_average: float = Field(..., description="Opponent's recent average points allowed")
    trend_direction: str = Field(..., description="Trend direction: 'improving', 'declining', 'stable'")
    trend_magnitude: float = Field(..., description="Magnitude of trend change")

    # Context factors
    home_field_advantage: float = Field(0.0, description="Home field advantage bonus/penalty")
    weather_impact: float = Field(0.0, description="Weather impact factor")
    venue_impact: float = Field(0.0, description="Venue-specific impact factor")

    # Confidence metrics
    confidence_score: float = Field(..., description="Confidence in this rating (0-100)")
    sample_size: int = Field(..., description="Number of games in analysis")
    last_updated: datetime = Field(default_factory=datetime.now, description="Rating calculation timestamp")

    @validator('overall_rating', 'defense_strength_rating', 'recent_trend_rating',
              'home_field_rating', 'schedule_strength_rating', 'confidence_score')
    def validate_rating_range(cls, v):
        if v < 1 or v > 100:
            raise ValueError(f'Rating must be between 1 and 100, got {v}')
        return v

    def get_rating_description(self) -> str:
        """Get human-readable description of the matchup rating"""
        if self.overall_rating >= 80:
            return "Excellent"
        elif self.overall_rating >= 65:
            return "Good"
        elif self.overall_rating >= 50:
            return "Average"
        elif self.overall_rating >= 35:
            return "Below Average"
        else:
            return "Poor"

    def is_favorable_matchup(self, threshold: float = 65.0) -> bool:
        """Check if this is considered a favorable matchup"""
        return self.overall_rating >= threshold

    def get_matchup_summary(self) -> Dict[str, Any]:
        """Get a summary of key matchup information"""
        return {
            'player': f"{self.player_context.player_name} ({self.player_context.player_position})",
            'opponent': self.player_context.opponent_team_abbreviation,
            'rating': self.overall_rating,
            'description': self.get_rating_description(),
            'is_favorable': self.is_favorable_matchup(),
            'home_away': 'Home' if self.player_context.is_home_game else 'Away',
            'trend': self.trend_direction,
            'confidence': self.confidence_score
        }


class WeeklyMatchupAnalysis(BaseModel):
    """Complete matchup analysis for a week"""
    week: int = Field(..., description="NFL week number")
    season: int = Field(..., description="NFL season year")
    analysis_date: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")

    # All player matchup ratings for the week
    player_ratings: List[MatchupRating] = Field(default_factory=list, description="Individual player ratings")

    # Team defense statistics used in analysis
    team_defenses: Dict[int, TeamDefenseStats] = Field(default_factory=dict, description="Team defense stats by team ID")

    # Weekly matchups (games)
    weekly_matchups: List[WeeklyMatchup] = Field(default_factory=list, description="All games for the week")

    # Analysis metadata
    total_players_analyzed: int = Field(0, description="Number of players analyzed")
    average_confidence: float = Field(0.0, description="Average confidence across all ratings")
    analysis_runtime_seconds: float = Field(0.0, description="Time taken to complete analysis")

    def get_player_rating(self, player_id: str) -> Optional[MatchupRating]:
        """Get matchup rating for a specific player"""
        for rating in self.player_ratings:
            if rating.player_context.player_id == player_id:
                return rating
        return None

    def get_top_matchups(self, position: Optional[FantasyPosition] = None, limit: int = 10) -> List[MatchupRating]:
        """Get top matchups for a position or all positions"""
        filtered_ratings = self.player_ratings

        if position:
            filtered_ratings = [r for r in self.player_ratings
                              if r.player_context.player_position == position]

        return sorted(filtered_ratings, key=lambda x: x.overall_rating, reverse=True)[:limit]

    def get_worst_matchups(self, position: Optional[FantasyPosition] = None, limit: int = 10) -> List[MatchupRating]:
        """Get worst matchups for a position or all positions"""
        filtered_ratings = self.player_ratings

        if position:
            filtered_ratings = [r for r in self.player_ratings
                              if r.player_context.player_position == position]

        return sorted(filtered_ratings, key=lambda x: x.overall_rating)[:limit]

    def get_team_defense_ranking(self, position: FantasyPosition) -> List[tuple]:
        """Get team defense rankings for a specific position (best to worst)"""
        rankings = []
        for team_id, defense in self.team_defenses.items():
            points_allowed = defense.get_points_allowed_by_position(position)
            rankings.append((team_id, defense.team_abbreviation, points_allowed))

        # Sort by points allowed (ascending = better defense)
        return sorted(rankings, key=lambda x: x[2])


class MatchupAnalysisConfig(BaseModel):
    """Configuration settings for matchup analysis"""

    # Feature toggles
    enable_matchup_analysis: bool = Field(True, description="Enable/disable matchup analysis")
    show_matchup_simple: bool = Field(True, description="Show simple matchup indicators")
    show_matchup_detailed: bool = Field(False, description="Show detailed matchup analysis")

    # Rating calculation weights (must sum to 1.0)
    defense_strength_weight: float = Field(0.40, description="Weight for opponent defense strength")
    recent_trend_weight: float = Field(0.30, description="Weight for recent defensive trends")
    home_field_weight: float = Field(0.15, description="Weight for home/away advantage")
    schedule_strength_weight: float = Field(0.15, description="Weight for strength of schedule")

    # Analysis parameters
    matchup_weight_factor: float = Field(0.15, description="Impact of matchup on lineup recommendations")
    recent_weeks_for_defense: int = Field(4, description="Number of recent weeks for trend analysis")
    favorable_matchup_threshold: float = Field(65.0, description="Threshold for favorable matchup (1-100)")

    # Performance settings
    max_concurrent_requests: int = Field(5, description="Maximum concurrent ESPN API requests")
    request_timeout_seconds: int = Field(30, description="Timeout for ESPN API requests")
    rate_limit_delay_ms: int = Field(300, description="Delay between API requests in milliseconds")

    @validator('defense_strength_weight', 'recent_trend_weight', 'home_field_weight', 'schedule_strength_weight')
    def validate_weights(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Weight must be between 0 and 1')
        return v

    @validator('matchup_weight_factor')
    def validate_matchup_weight(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Matchup weight factor must be between 0 and 1')
        return v

    @validator('favorable_matchup_threshold')
    def validate_threshold(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Threshold must be between 1 and 100')
        return v

    def validate_weights_sum(self):
        """Validate that rating weights sum to approximately 1.0"""
        total_weight = (self.defense_strength_weight + self.recent_trend_weight +
                       self.home_field_weight + self.schedule_strength_weight)
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f'Rating weights must sum to 1.0, got {total_weight}')