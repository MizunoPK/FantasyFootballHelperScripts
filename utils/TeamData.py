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


def load_team_weekly_data(team_data_folder: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Load all team weekly data from team_data folder.

    Args:
        team_data_folder: Path to folder containing team CSV files (e.g., KC.csv, MIN.csv)

    Returns:
        Dict mapping team abbreviation to list of weekly data dicts
        Format: {'KC': [{'week': 1, 'pts_allowed_to_QB': 18.5, ...}, ...], ...}

    Raises:
        FileNotFoundError: If team_data folder doesn't exist
    """
    from pathlib import Path

    folder_path = Path(team_data_folder)
    if not folder_path.exists():
        raise FileNotFoundError(f"Team data folder not found: {team_data_folder}")

    team_weekly_data = {}

    # Load each team's CSV file
    for csv_file in folder_path.glob("*.csv"):
        team_abbr = csv_file.stem  # e.g., 'KC' from 'KC.csv'
        weekly_data = load_single_team_data(str(csv_file))
        team_weekly_data[team_abbr] = weekly_data

    return team_weekly_data


def load_single_team_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load weekly data for a single team from CSV file.

    Args:
        file_path: Path to team CSV file (e.g., KC.csv)

    Returns:
        List of weekly data dicts, one per week
        Format: [{'week': 1, 'pts_allowed_to_QB': 18.5, 'pts_allowed_to_RB': 22.3,
                  'pts_allowed_to_WR': 31.2, 'pts_allowed_to_TE': 8.4, 'pts_allowed_to_K': 9.0,
                  'points_scored': 28, 'points_allowed': 17}, ...]

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    try:
        df = read_csv_with_validation(file_path)
        weekly_data = []

        for _, row in df.iterrows():
            week_data = {
                'week': _safe_int_conversion(row.get('week'), 0),
                'pts_allowed_to_QB': float(row.get('pts_allowed_to_QB', 0) or 0),
                'pts_allowed_to_RB': float(row.get('pts_allowed_to_RB', 0) or 0),
                'pts_allowed_to_WR': float(row.get('pts_allowed_to_WR', 0) or 0),
                'pts_allowed_to_TE': float(row.get('pts_allowed_to_TE', 0) or 0),
                'pts_allowed_to_K': float(row.get('pts_allowed_to_K', 0) or 0),
                'points_scored': float(row.get('points_scored', 0) or 0),
                'points_allowed': float(row.get('points_allowed', 0) or 0)
            }
            weekly_data.append(week_data)

        return weekly_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Team data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading team data from {file_path}: {str(e)}")


def save_team_weekly_data(team_data_folder: str, team_weekly_data: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Save all team weekly data to team_data folder.

    Args:
        team_data_folder: Path to folder for team CSV files
        team_weekly_data: Dict mapping team abbreviation to list of weekly data
            Format: {'KC': [{'week': 1, 'pts_allowed_to_QB': 18.5, ...}, ...], ...}
    """
    from pathlib import Path

    folder_path = Path(team_data_folder)
    folder_path.mkdir(parents=True, exist_ok=True)

    for team_abbr, weekly_data in team_weekly_data.items():
        file_path = folder_path / f"{team_abbr}.csv"
        save_single_team_data(str(file_path), weekly_data)


def save_single_team_data(file_path: str, weekly_data: List[Dict[str, Any]]) -> None:
    """
    Save weekly data for a single team to CSV file.

    Args:
        file_path: Output CSV file path (e.g., KC.csv)
        weekly_data: List of weekly data dicts
            Format: [{'week': 1, 'pts_allowed_to_QB': 18.5, 'pts_allowed_to_RB': 22.3, ...}, ...]
    """
    if not weekly_data:
        # Create empty CSV with proper headers
        df = pd.DataFrame(columns=['week', 'pts_allowed_to_QB', 'pts_allowed_to_RB',
                                   'pts_allowed_to_WR', 'pts_allowed_to_TE', 'pts_allowed_to_K',
                                   'points_scored', 'points_allowed'])
    else:
        df = pd.DataFrame(weekly_data)

    # Ensure consistent column order
    columns = ['week', 'pts_allowed_to_QB', 'pts_allowed_to_RB', 'pts_allowed_to_WR',
               'pts_allowed_to_TE', 'pts_allowed_to_K', 'points_scored', 'points_allowed']
    df = df[columns]

    # Save to CSV
    write_csv_with_backup(df, file_path, create_backup=False)


# NFL team abbreviations (all 32 teams)
NFL_TEAMS = [
    'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
    'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
    'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
    'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
]