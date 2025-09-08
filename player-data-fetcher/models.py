#!/usr/bin/env python3
"""
Data Models for NFL Fantasy Football Data Collection

This module contains all Pydantic data models used across the fantasy football
data collection scripts. Separated for better organization and reusability.

Author: Generated for NFL Fantasy Data Collection  
Last Updated: September 2025
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

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
    drafted: int = 0  # 0 = not drafted, 1 = drafted
    fantasy_points: float = 0.0
    average_draft_position: Optional[float] = None  # ESPN's ADP data
    
    # Injury information (proper field instead of reusing others)
    injury_status: str = "ACTIVE"  # ACTIVE, QUESTIONABLE, OUT, etc.
    
    # Metadata
    api_source: str = "ESPN"
    updated_at: datetime = Field(default_factory=datetime.now)


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