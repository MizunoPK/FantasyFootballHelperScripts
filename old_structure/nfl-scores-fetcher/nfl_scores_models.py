#!/usr/bin/env python3
"""
Data Models for NFL Scores Collection

This module contains all Pydantic data models used for NFL game score collection
and analysis. Separated for better organization and reusability.

Author: Kai Mizuno
Last Updated: September 2025
"""

from datetime import datetime, timezone
from typing import List, Optional, Any

from pydantic import BaseModel, Field


class Team(BaseModel):
    """Represents an NFL team with all relevant metadata.
    
    ESPN provides extensive team information that we capture here.
    Optional fields handle cases where ESPN doesn't provide all data.
    """
    id: str  # ESPN's unique team identifier
    name: str  # Team name (e.g., "Cowboys")
    display_name: str  # Full display name (e.g., "Dallas Cowboys")
    abbreviation: str  # 3-letter code (e.g., "DAL")
    location: str  # City/location (e.g., "Dallas")
    color: Optional[str] = None  # Primary team color (hex code)
    alternate_color: Optional[str] = None  # Secondary team color
    logo_url: Optional[str] = None  # URL to team logo image
    record: Optional[str] = None  # Season record in "W-L" format
    score: Optional[int] = None  # Game score (set when used in GameScore context)


class GameScore(BaseModel):
    """Comprehensive NFL game data model.
    
    Captures everything we might want to know about an NFL game,
    from basic scores to detailed venue and weather information.
    The model automatically calculates derived fields after initialization.
    """
    
    # Core Game Identification
    # ========================
    game_id: str  # ESPN's unique game identifier
    date: datetime  # Game date and time (timezone-aware)
    week: int  # NFL week number (1-18 for regular season)
    season: int  # Season year
    season_type: int  # Season type (preseason, regular, postseason)
    
    # Team Information
    # ================
    home_team: Team  # Complete home team data
    away_team: Team  # Complete away team data
    
    # Final Scores
    # ============
    home_score: int  # Home team final score
    away_score: int  # Away team final score
    
    # Game Status Information
    # ======================
    status: str  # ESPN status code ("STATUS_FINAL", "STATUS_IN_PROGRESS", etc.)
    status_detail: str  # Human-readable status description
    is_completed: bool  # Whether the game is finished
    is_in_progress: bool = Field(default=False)  # Whether the game is currently being played
    
    # Venue and Location Details
    # ==========================
    venue_name: Optional[str] = None  # Stadium name (e.g., "AT&T Stadium")
    venue_city: Optional[str] = None  # Stadium city
    venue_state: Optional[str] = None  # Stadium state
    venue_capacity: Optional[int] = None  # Stadium seating capacity
    attendance: Optional[int] = None  # Actual game attendance
    
    # Weather Conditions (if available)
    # ================================
    temperature: Optional[int] = None  # Game temperature in Fahrenheit
    weather_description: Optional[str] = None  # Weather condition description
    wind_speed: Optional[int] = None  # Wind speed in MPH
    
    # Broadcast Information
    # ====================
    tv_network: Optional[str] = None  # TV network broadcasting the game
    
    # Betting Information (if available)
    # =================================
    home_team_odds: Optional[float] = None  # Home team betting odds
    away_team_odds: Optional[float] = None  # Away team betting odds
    over_under: Optional[float] = None  # Total points over/under line
    
    # Basic Game Statistics
    # ====================
    # ESPN sometimes provides summary stats, we capture the most important ones
    home_total_yards: Optional[int] = None  # Home team total offensive yards
    away_total_yards: Optional[int] = None  # Away team total offensive yards
    home_turnovers: Optional[int] = None  # Home team turnovers
    away_turnovers: Optional[int] = None  # Away team turnovers
    
    # Quarter-by-Quarter Scoring
    # =========================
    # Detailed scoring breakdown by quarter (and overtime if applicable)
    home_score_q1: Optional[int] = None  # Home team Q1 score
    home_score_q2: Optional[int] = None  # Home team Q2 score
    home_score_q3: Optional[int] = None  # Home team Q3 score
    home_score_q4: Optional[int] = None  # Home team Q4 score
    home_score_ot: Optional[int] = None  # Home team overtime score
    away_score_q1: Optional[int] = None  # Away team Q1 score
    away_score_q2: Optional[int] = None  # Away team Q2 score
    away_score_q3: Optional[int] = None  # Away team Q3 score
    away_score_q4: Optional[int] = None  # Away team Q4 score
    away_score_ot: Optional[int] = None  # Away team overtime score
    
    # Calculated/Derived Fields
    # ========================
    # These fields are automatically calculated after the model is created
    total_points: int = Field(default=0)  # Combined score of both teams
    point_difference: int = Field(default=0)  # Absolute difference between scores
    winning_team: str = Field(default="")  # Abbreviation of winning team
    is_overtime: bool = Field(default=False)  # Whether game went to overtime
    
    # Record Keeping
    # =============
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # When this data was collected
    
    def model_post_init(self, __context: Any) -> None:
        """Automatically calculate derived fields after model initialization.
        
        This Pydantic v2 hook runs after all fields are set, allowing us to
        compute additional fields based on the provided data. This ensures
        consistency and reduces the chance of calculation errors.
        """
        # Calculate total points scored in the game
        self.total_points = self.home_score + self.away_score
        
        # Calculate point difference (always positive)
        self.point_difference = abs(self.home_score - self.away_score)
        
        # Determine the winning team
        if self.home_score > self.away_score:
            self.winning_team = self.home_team.abbreviation
        elif self.away_score > self.home_score:
            self.winning_team = self.away_team.abbreviation
        else:
            self.winning_team = "TIE"  # Rare in NFL, but possible in regular season
        
        # Check if the game went to overtime
        # Any non-zero overtime score indicates an overtime game
        self.is_overtime = any([
            self.home_score_ot and self.home_score_ot > 0,
            self.away_score_ot and self.away_score_ot > 0
        ])


class WeeklyScores(BaseModel):
    """Container for a collection of NFL games from a specific time period.
    
    This model groups multiple GameScore objects together with metadata
    about the collection, making it easy to export and analyze.
    """
    week: int  # Week number (0 for multi-week collections)
    season: int  # Season year
    season_type: int  # Season type
    total_games: int  # Total number of games found
    completed_games: int  # Number of finished games
    games: List[GameScore]  # List of all game data
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Collection timestamp


# Custom Exceptions
class ScoreDataCollectionError(Exception):
    """Custom exception for score data collection issues"""
    pass


class GameDataValidationError(Exception):
    """Custom exception for game data validation issues"""
    pass


class NFLAPIError(Exception):
    """Custom exception for NFL API errors"""
    pass