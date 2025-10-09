#!/usr/bin/env python3
"""
FantasyPlayer Class Definition

This module defines the FantasyPlayer class for NFL fantasy football player data.
Designed to be used across multiple scripts for consistent player representation.

Author: Kai Mizuno
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List
import pandas as pd
from utils.csv_utils import read_csv_with_validation, write_csv_with_backup

# Import will be done dynamically to avoid circular imports

def safe_int_conversion(value, default=None):
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

def safe_float_conversion(value, default=0.0):
    """
    Safely convert a value to float with fallback to default.

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        float or default value
    """
    if value is None or value == '' or (isinstance(value, str) and value.lower() in ['nan', 'none', 'null']):
        return default
    try:
        float_val = float(value)
        # Check for infinity values
        if float_val == float('inf') or float_val == float('-inf') or float_val != float_val:  # NaN check
            return default
        return float_val
    except (ValueError, TypeError, OverflowError):
        return default


@dataclass
class FantasyPlayer:
    """
    Represents a fantasy football player with all relevant data fields.
    
    This class maps to the CSV/Excel export structure from data_fetcher-players.py
    and provides a consistent interface for player data across multiple scripts.
    """
    
    # Core identification
    id: int  # Player ID (int to match CSV/dataframe format)
    name: str
    team: str
    position: str
    
    # Fantasy relevant data
    bye_week: Optional[int] = None
    drafted: int = 0  # 0 = not drafted, 1 = drafted, 2 = on our team
    locked: int = 0  # 0 = not locked, 1 = locked (cannot be drafted or traded)
    fantasy_points: float = 0.0
    average_draft_position: Optional[float] = None  # ESPN's ADP data
    player_rating: Optional[float] = None  # ESPN's internal player rating system

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

    # Injury information
    injury_status: str = "UNKNOWN"  # ACTIVE, QUESTIONABLE, OUT, etc.

    # League helper specific fields (computed later)
    score: float = 0.0  # Overall score for draft ranking
    weighted_projection: float = 0.0  # Normalized projection score
    consistency: float = 0.0
    matchup_score: int = 0

    # Enhanced scoring fields for team context
    team_offensive_rank: Optional[int] = None  # Team offensive quality rank (lower is better)
    team_defensive_rank: Optional[int] = None  # Team defensive quality rank (lower is better)

    # Metadata

    def __post_init__(self):
        """Post-initialization setup."""
        # No special initialization needed since adp is now a property
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
        """
        Create a FantasyPlayer instance from a dictionary (e.g., CSV row).

        Args:
            data: Dictionary with player data keys matching class fields

        Returns:
            FantasyPlayer instance
        """
        # Handle both 'adp' and 'average_draft_position' for backward compatibility
        adp_value = data.get('average_draft_position') or data.get('adp')
        processed_adp = safe_float_conversion(adp_value, 0.0) if adp_value is not None else None

        return cls(
            id=safe_int_conversion(data.get('id'), 0),  # Keep ID as int to match dataframe
            name=str(data.get('name', '')),
            team=str(data.get('team', '')),
            position=str(data.get('position', '')),
            bye_week=safe_int_conversion(data.get('bye_week'), 0),
            drafted=safe_int_conversion(data.get('drafted'), 0),
            locked=safe_int_conversion(data.get('locked'), 0),
            fantasy_points=safe_float_conversion(data.get('fantasy_points'), 0.0),
            average_draft_position=processed_adp,
            player_rating=safe_float_conversion(data.get('player_rating'), None) if data.get('player_rating') is not None else None,
            # Weekly projections (weeks 1-17)
            week_1_points=safe_float_conversion(data.get('week_1_points'), None),
            week_2_points=safe_float_conversion(data.get('week_2_points'), None),
            week_3_points=safe_float_conversion(data.get('week_3_points'), None),
            week_4_points=safe_float_conversion(data.get('week_4_points'), None),
            week_5_points=safe_float_conversion(data.get('week_5_points'), None),
            week_6_points=safe_float_conversion(data.get('week_6_points'), None),
            week_7_points=safe_float_conversion(data.get('week_7_points'), None),
            week_8_points=safe_float_conversion(data.get('week_8_points'), None),
            week_9_points=safe_float_conversion(data.get('week_9_points'), None),
            week_10_points=safe_float_conversion(data.get('week_10_points'), None),
            week_11_points=safe_float_conversion(data.get('week_11_points'), None),
            week_12_points=safe_float_conversion(data.get('week_12_points'), None),
            week_13_points=safe_float_conversion(data.get('week_13_points'), None),
            week_14_points=safe_float_conversion(data.get('week_14_points'), None),
            week_15_points=safe_float_conversion(data.get('week_15_points'), None),
            week_16_points=safe_float_conversion(data.get('week_16_points'), None),
            week_17_points=safe_float_conversion(data.get('week_17_points'), None),
            injury_status=str(data.get('injury_status', 'UNKNOWN')),
            score=safe_float_conversion(data.get('score'), 0.0),
            weighted_projection=safe_float_conversion(data.get('weighted_projection'), 0.0),
            consistency=safe_float_conversion(data.get('consistency'), 0.0),
            matchup_score=safe_int_conversion(data.get('matchup_score'), 0),
            team_offensive_rank=safe_int_conversion(data.get('team_offensive_rank'), None),
            team_defensive_rank=safe_int_conversion(data.get('team_defensive_rank'), None)
        )
    
    @classmethod
    def from_csv_file(cls, filepath: str) -> List['FantasyPlayer']:
        """
        Load all players from a CSV file.

        Args:
            filepath: Path to the CSV file

        Returns:
            List of FantasyPlayer instances

        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            pd.errors.EmptyDataError: If the CSV file is empty
            pd.errors.ParserError: If the CSV file is malformed
        """
        try:
            # Use csv_utils for standardized reading with error handling
            df = read_csv_with_validation(filepath)
        except Exception as e:
            print(f"Error reading CSV file at {filepath}: {e}")
            raise

        players = []
        failed_rows = 0

        for row_idx, row in df.iterrows():
            try:
                player = cls.from_dict(row.to_dict())
                players.append(player)
            except Exception as e:
                failed_rows += 1
                print(f"Warning: Failed to parse player row {row_idx + 1}: {e}")
                continue

        if failed_rows > 0:
            print(f"Warning: Failed to parse {failed_rows} out of {len(df)} rows")

        return players
    
    @classmethod
    def from_excel_file(cls, filepath: str, sheet_name: str = 'All Players') -> List['FantasyPlayer']:
        """
        Load all players from an Excel file.

        Args:
            filepath: Path to the Excel file
            sheet_name: Name of the sheet to read (default: 'All Players')

        Returns:
            List of FantasyPlayer instances

        Raises:
            FileNotFoundError: If the Excel file doesn't exist
            ValueError: If the sheet name doesn't exist
            pd.errors.EmptyDataError: If the Excel file/sheet is empty
        """
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
        except FileNotFoundError:
            print(f"Error: Excel file not found at {filepath}")
            raise
        except ValueError as e:
            if "Worksheet" in str(e) and "does not exist" in str(e):
                print(f"Error: Sheet '{sheet_name}' not found in Excel file {filepath}")
            else:
                print(f"Error: Invalid Excel file format at {filepath}: {e}")
            raise
        except PermissionError:
            print(f"Error: Permission denied reading Excel file at {filepath}")
            raise
        except Exception as e:
            print(f"Error: Unexpected error reading Excel file at {filepath}: {e}")
            raise

        if df.empty:
            print(f"Warning: Excel sheet '{sheet_name}' is empty in {filepath}")
            return []

        players = []
        failed_rows = 0

        for row_idx, row in df.iterrows():
            try:
                player = cls.from_dict(row.to_dict())
                players.append(player)
            except Exception as e:
                failed_rows += 1
                print(f"Warning: Failed to parse player row {row_idx + 1} from sheet '{sheet_name}': {e}")
                continue

        if failed_rows > 0:
            print(f"Warning: Failed to parse {failed_rows} out of {len(df)} rows from sheet '{sheet_name}'")

        return players
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert FantasyPlayer to dictionary.
        
        Returns:
            Dictionary representation of the player
        """
        return asdict(self)
    
    def is_available(self) -> bool:
        """
        Check if player is available for drafting.
        
        Returns:
            True if player is not drafted and not locked, False otherwise
        """
        return self.drafted == 0 and self.locked == 0
    
    def is_rostered(self) -> bool:
        return self.drafted == 2
    
    def is_locked(self) -> bool:
        """
        Check if player is locked from being drafted or traded.
        
        Returns:
            True if player is locked, False otherwise
        """
        return self.locked == 1
    
    def get_risk_level(self) -> str:
        """
        Assess injury risk level based on status.
        
        Returns:
            Risk level string: "LOW", "MEDIUM", "HIGH"
        """
        if self.injury_status == 'ACTIVE':
            return "LOW"
        elif self.injury_status in ['QUESTIONABLE']:
            return "MEDIUM"
        elif self.injury_status in ['OUT', 'DOUBTFUL', 'INJURY_RESERVE', 'SUSPENSION', 'UNKNOWN']:
            return "HIGH"
        else:
            return "MEDIUM"
    
    def __str__(self) -> str:
        """String representation of the player."""
        status = f" ({self.injury_status})" if self.injury_status != 'ACTIVE' else ""
        drafted_status = " [DRAFTED]" if self.drafted == 1 else ""
        return f"{self.name} ({self.team} {self.position}) - {self.fantasy_points:.1f} pts{status}{drafted_status}"
    
    def __repr__(self) -> str:
        """Developer representation of the player."""
        return f"FantasyPlayer(id='{self.id}', name='{self.name}', team='{self.team}', position='{self.position}', fantasy_points={self.fantasy_points})"
    
    # Method to get the position including FLEX eligibility
    def get_position_including_flex(self):
        # FLEX eligible positions: RB and WR
        FLEX_ELIGIBLE_POSITIONS = ['RB', 'WR']
        return 'FLEX' if self.position in FLEX_ELIGIBLE_POSITIONS else self.position

    # Aliases for test compatibility
    @classmethod
    def load_from_csv(cls, filepath: str) -> List['FantasyPlayer']:
        """Alias for from_csv_file for test compatibility."""
        return cls.from_csv_file(filepath)

    @classmethod
    def load_from_excel(cls, filepath: str, sheet_name: str = 'All Players') -> List['FantasyPlayer']:
        """Alias for from_excel_file for test compatibility."""
        return cls.from_excel_file(filepath, sheet_name)

    @classmethod
    def save_to_csv(cls, players: List['FantasyPlayer'], filepath: str) -> None:
        """Save players to CSV file using standardized csv_utils."""
        df = players_to_dataframe(players)
        write_csv_with_backup(df, filepath, create_backup=False)

    def __eq__(self, other):
        """Check equality based on player ID."""
        if not isinstance(other, FantasyPlayer):
            return False
        return self.id == other.id

    def __hash__(self):
        """Make FantasyPlayer hashable based on ID."""
        return hash(self.id)

    @property
    def adp(self):
        """Alias for average_draft_position for backward compatibility."""
        return self.average_draft_position

    @adp.setter
    def adp(self, value):
        """Setter for adp alias."""
        self.average_draft_position = value

def players_to_dataframe(players: List[FantasyPlayer]) -> pd.DataFrame:
    """Convert list of FantasyPlayer objects to pandas DataFrame."""
    return pd.DataFrame([player.to_dict() for player in players])