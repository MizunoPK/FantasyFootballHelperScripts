#!/usr/bin/env python3
"""
Data Models for NFL Fantasy Football Data Collection

This module contains all Pydantic data models used across the fantasy football
data collection scripts. Separated for better organization and reusability.

Author: Kai Mizuno  
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ScoringFormat(str, Enum):
    """Fantasy football scoring format options"""
    STANDARD = "std"
    PPR = "ppr" 
    HALF_PPR = "half"


class ESPNPlayerData(BaseModel):
    """
    ESPN player data model with fantasy projections.

    This model represents player data as received from ESPN's fantasy API,
    with proper field separation (no field reuse) and validation.
    """

    # Core player identification
    id: str
    name: str
    team: str
    position: str

    # Fantasy data
    bye_week: Optional[int] = None
    drafted: int = 0  # 0 = not drafted, 1 = drafted, 2 = roster player
    locked: int = 0   # 0 = not locked, 1 = locked
    fantasy_points: float = 0.0
    average_draft_position: Optional[float] = None  # ESPN's ADP data
    player_rating: Optional[float] = None  # 0-100 scale normalized from ESPN position-specific rankings (100=best, 1=worst within position)

    # Weekly projections (weeks 1-17 fantasy regular season only)
    week_1_points: Optional[float] = None
    week_2_points: Optional[float] = None
    week_3_points: Optional[float] = None
    week_4_points: Optional[float] = None
    week_5_points: Optional[float] = None
    week_6_points: Optional[float] = None
    week_7_points: Optional[float] = None
    week_8_points: Optional[float] = None
    week_9_points: Optional[float] = None
    week_10_points: Optional[float] = None
    week_11_points: Optional[float] = None
    week_12_points: Optional[float] = None
    week_13_points: Optional[float] = None
    week_14_points: Optional[float] = None
    week_15_points: Optional[float] = None
    week_16_points: Optional[float] = None
    week_17_points: Optional[float] = None

    # Injury information (proper field instead of reusing others)
    injury_status: str = "ACTIVE"  # ACTIVE, QUESTIONABLE, OUT, etc.

    # Metadata
    api_source: str = "ESPN"
    updated_at: datetime = Field(default_factory=datetime.now)

    def set_week_points(self, week: int, points: float):
        """Set points for a specific week (fantasy regular season weeks 1-17 only)"""
        if 1 <= week <= 17:
            setattr(self, f"week_{week}_points", points)

    def get_week_points(self, week: int) -> Optional[float]:
        """Get points for a specific week (fantasy regular season weeks 1-17 only)"""
        if 1 <= week <= 17:
            return getattr(self, f"week_{week}_points", None)
        return None

    def get_all_weekly_points(self) -> Dict[int, Optional[float]]:
        """Get all weekly points as a dictionary (weeks 1-17 only)"""
        return {
            week: self.get_week_points(week)
            for week in range(1, 18)
        }


class PlayerProjection(ESPNPlayerData):
    """Legacy model for backward compatibility - delegates to ESPNPlayerData"""
    pass


class ProjectionData(BaseModel):
    """
    Container for projection data with metadata.
    
    Holds a collection of player projections along with metadata about
    the data collection session (season, scoring format, etc.).
    """
    season: int
    scoring_format: str
    total_players: int
    players: List[ESPNPlayerData]
    generated_at: datetime = Field(default_factory=datetime.now)


# Custom Exceptions
class DataCollectionError(Exception):
    """Custom exception for data collection issues"""
    pass


class PlayerDataValidationError(Exception):
    """Custom exception for player data validation issues"""
    pass