#!/usr/bin/env python3
"""
NFL Scores Fetcher Package

This package contains all modules for NFL game scores collection from ESPN API.

Author: Kai Mizuno
Last Updated: September 2025
"""

from nfl_scores_models import Team, GameScore, WeeklyScores, ScoreDataCollectionError, NFLAPIError
from nfl_api_client import NFLAPIClient
from nfl_scores_exporter import ScoresDataExporter

__version__ = "2.0.0"
__all__ = [
    "Team",
    "GameScore", 
    "WeeklyScores",
    "ScoreDataCollectionError",
    "NFLAPIError",
    "NFLAPIClient",
    "ScoresDataExporter"
]