#!/usr/bin/env python3
"""
TeamData Class Definition

This module defines the TeamData class for NFL team-level data including
offensive/defensive rankings and position-specific defense rankings. Designed
to be used alongside FantasyPlayer data for better separation of concerns.

Author: Kai Mizuno
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import pandas as pd
from utils.csv_utils import read_csv_with_validation, write_csv_with_backup


@dataclass
class TeamData:
    """
    Represents NFL team data with offensive/defensive rankings and position-specific defense.

    This class separates team-level data from individual player data for better
    data organization and enables enhanced matchup analysis.
    """

    # Core team identification
    team: str  # Team abbreviation (e.g., 'PHI', 'KC', 'BUF')

    # Team quality rankings (lower rank = better team)
    offensive_rank: Optional[int] = None  # Team offensive quality ranking (1-32)
    defensive_rank: Optional[int] = None  # Team defensive quality ranking (1-32)

    # Position-specific defense rankings (lower rank = better defense vs that position)
    def_vs_qb_rank: Optional[int] = None  # Defense rank vs QB (1-32, 1=best)
    def_vs_rb_rank: Optional[int] = None  # Defense rank vs RB (1-32, 1=best)
    def_vs_wr_rank: Optional[int] = None  # Defense rank vs WR (1-32, 1=best)
    def_vs_te_rank: Optional[int] = None  # Defense rank vs TE (1-32, 1=best)
    def_vs_k_rank: Optional[int] = None   # Defense rank vs K (1-32, 1=best)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TeamData':
        """
        Create TeamData instance from dictionary data.

        Args:
            data: Dictionary containing team data fields

        Returns:
            TeamData instance with converted fields
        """
        return cls(
            team=data.get('team', ''),
            offensive_rank=_safe_int_conversion(data.get('offensive_rank'), None),
            defensive_rank=_safe_int_conversion(data.get('defensive_rank'), None),
            def_vs_qb_rank=_safe_int_conversion(data.get('def_vs_qb_rank'), None),
            def_vs_rb_rank=_safe_int_conversion(data.get('def_vs_rb_rank'), None),
            def_vs_wr_rank=_safe_int_conversion(data.get('def_vs_wr_rank'), None),
            def_vs_te_rank=_safe_int_conversion(data.get('def_vs_te_rank'), None),
            def_vs_k_rank=_safe_int_conversion(data.get('def_vs_k_rank'), None)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert TeamData instance to dictionary for CSV export."""
        return {
            'team': self.team,
            'offensive_rank': self.offensive_rank,
            'defensive_rank': self.defensive_rank,
            'def_vs_qb_rank': self.def_vs_qb_rank,
            'def_vs_rb_rank': self.def_vs_rb_rank,
            'def_vs_wr_rank': self.def_vs_wr_rank,
            'def_vs_te_rank': self.def_vs_te_rank,
            'def_vs_k_rank': self.def_vs_k_rank
        }


def _safe_int_conversion(value, default=None):
    """
    Safely convert a value to integer with fallback to default.

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        int or default value
    """
    if value is None or value == '' or (isinstance(value, str) and value.lower() in ['nan', 'none', 'null']):
        return default
    try:
        # Handle string representations of floats
        if isinstance(value, str):
            # Remove any non-numeric characters except decimal points and negative signs
            cleaned = ''.join(c for c in value if c.isdigit() or c in '.-')
            if not cleaned or cleaned in ['-', '.', '-.']:
                return default
            float_val = float(cleaned)
        else:
            float_val = float(value)

        # Check for infinity values
        if float_val == float('inf') or float_val == float('-inf') or float_val != float_val:  # NaN check
            return default

        return int(float_val)
    except (ValueError, TypeError, OverflowError):
        return default


def _safe_string_conversion(value):
    """
    Safely convert a value to string, handling NaN values.

    Args:
        value: Value to convert

    Returns:
        str or None
    """
    if value is None:
        return None

    # Handle pandas NaN values
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    # Convert to string and check for NaN-like strings
    str_val = str(value).strip()
    if str_val.lower() in ['nan', 'none', 'null', '']:
        return None

    return str_val


def load_teams_from_csv(file_path: str) -> List[TeamData]:
    """
    Load TeamData objects from CSV file.

    Args:
        file_path: Path to the teams.csv file

    Returns:
        List of TeamData objects

    Raises:
        FileNotFoundError: If teams.csv file doesn't exist
        Exception: If CSV format is invalid
    """
    try:
        # Use csv_utils for standardized reading with error handling
        df = read_csv_with_validation(file_path)
        teams = []

        for _, row in df.iterrows():
            team_data = TeamData.from_dict(row.to_dict())
            teams.append(team_data)

        return teams
    except FileNotFoundError:
        raise FileNotFoundError(f"teams.csv file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading teams from CSV: {str(e)}")


def extract_teams_from_players(players: List['FantasyPlayer']) -> List[TeamData]:
    """
    Extract unique team data from a list of FantasyPlayer objects.

    Args:
        players: List of FantasyPlayer objects containing team ranking data

    Returns:
        List of TeamData objects with unique teams and their rankings

    Note:
        This function is deprecated since team ranking data is no longer stored
        in FantasyPlayer objects. Use extract_teams_from_rankings() instead.
    """
    team_data_map = {}

    for player in players:
        team = player.team
        if not team or team in team_data_map:
            continue  # Skip empty teams or already processed teams

        # Create team data with no ranking info (rankings are handled separately now)
        team_data_map[team] = TeamData(
            team=team,
            offensive_rank=None,  # Rankings no longer available in player data
            defensive_rank=None   # Rankings no longer available in player data
        )

    # Return sorted list by team name for consistent ordering
    return sorted(team_data_map.values(), key=lambda x: x.team)


def extract_teams_from_rankings(
    players: List['FantasyPlayer'],
    team_rankings: dict,
    schedule_data: dict = None,
    position_defense_rankings: dict = None
) -> List[TeamData]:
    """
    Extract unique team data using team rankings from ESPN API.

    Args:
        players: List of FantasyPlayer objects to get team list from
        team_rankings: Dictionary with team rankings from ESPN API
            Format: {'KC': {'offensive_rank': 5, 'defensive_rank': 12}, ...}
        schedule_data: Optional dictionary (deprecated, kept for backward compatibility)
        position_defense_rankings: Optional dictionary with position-specific defense ranks
            Format: {'KC': {'def_vs_qb_rank': 5, 'def_vs_rb_rank': 12, ...}, ...}

    Returns:
        List of TeamData objects with teams and their rankings
    """
    team_data_map = {}

    # Get unique teams from players
    for player in players:
        team = player.team
        if not team or team in team_data_map:
            continue  # Skip empty teams or already processed teams

        # Get rankings from the ESPN client data
        team_ranking_data = team_rankings.get(team, {})

        # Get position-specific defense rankings if provided
        position_ranks = position_defense_rankings.get(team, {}) if position_defense_rankings else {}

        team_data_map[team] = TeamData(
            team=team,
            offensive_rank=team_ranking_data.get('offensive_rank', None),
            defensive_rank=team_ranking_data.get('defensive_rank', None),
            def_vs_qb_rank=position_ranks.get('def_vs_qb_rank', None),
            def_vs_rb_rank=position_ranks.get('def_vs_rb_rank', None),
            def_vs_wr_rank=position_ranks.get('def_vs_wr_rank', None),
            def_vs_te_rank=position_ranks.get('def_vs_te_rank', None),
            def_vs_k_rank=position_ranks.get('def_vs_k_rank', None)
        )

    # Return sorted list by team name for consistent ordering
    return sorted(team_data_map.values(), key=lambda x: x.team)


def save_teams_to_csv(teams: List[TeamData], file_path: str) -> None:
    """
    Save TeamData objects to CSV file.

    Args:
        teams: List of TeamData objects to save
        file_path: Output CSV file path
    """
    if not teams:
        # Create empty CSV with proper headers
        df = pd.DataFrame(columns=['team', 'offensive_rank', 'defensive_rank',
                                    'def_vs_qb_rank', 'def_vs_rb_rank', 'def_vs_wr_rank',
                                    'def_vs_te_rank', 'def_vs_k_rank'])
    else:
        # Convert teams to dictionaries for DataFrame creation
        team_dicts = [team.to_dict() for team in teams]
        df = pd.DataFrame(team_dicts)

    # Ensure consistent column order
    df = df[['team', 'offensive_rank', 'defensive_rank',
             'def_vs_qb_rank', 'def_vs_rb_rank', 'def_vs_wr_rank',
             'def_vs_te_rank', 'def_vs_k_rank']]

    # Save to CSV using standardized csv_utils (no backup needed)
    write_csv_with_backup(df, file_path, create_backup=False)