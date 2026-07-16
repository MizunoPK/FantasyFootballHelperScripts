#!/usr/bin/env python3
"""
FantasyPlayer Class Definition

This module defines the FantasyPlayer class for NFL fantasy football player data.
Designed to be used across multiple scripts for consistent player representation.

Author: Kai Mizuno
"""

from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List
import pandas as pd
from utils.csv_utils import read_csv_with_validation, write_csv_with_backup
from utils.LoggingManager import get_logger
from league_helper.constants import FANTASY_TEAM_NAME

logger = get_logger()

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
        if isinstance(value, str):
            cleaned = ''.join(c for c in value if c.isdigit() or c in '.-')
            if not cleaned or cleaned in ['-', '.', '-.']:
                return default
            float_val = float(cleaned)
        else:
            float_val = float(value)

        if float_val == float('inf') or float_val == float('-inf') or float_val != float_val:
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
        if float_val == float('inf') or float_val == float('-inf') or float_val != float_val:
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
    
    id: int
    name: str
    team: str
    position: str
    
    bye_week: Optional[int] = None
    drafted_by: str = ""
    locked: bool = False
    fantasy_points: float = 0.0
    average_draft_position: Optional[float] = None
    player_rating: Optional[float] = None

    projected_points: List[float] = field(default_factory=lambda: [0.0] * 17)
    actual_points: List[float] = field(default_factory=lambda: [0.0] * 17)

    passing: Optional[Dict[str, List[float]]] = None
    rushing: Optional[Dict[str, List[float]]] = None
    receiving: Optional[Dict[str, List[float]]] = None
    misc: Optional[Dict[str, List[float]]] = None
    extra_points: Optional[Dict[str, List[float]]] = None
    field_goals: Optional[Dict[str, List[float]]] = None
    defense: Optional[Dict[str, List[float]]] = None


    injury_status: str = "UNKNOWN"

    score: float = 0.0
    weighted_projection: float = 0.0
    consistency: float = 0.0
    matchup_score: Optional[int] = None

    team_offensive_rank: Optional[int] = None
    team_defensive_rank: Optional[int] = None


    def __post_init__(self):
        """Post-initialization setup."""
        if isinstance(self.locked, int):
            object.__setattr__(self, 'locked', bool(self.locked))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
        """
        Create a FantasyPlayer instance from a dictionary (e.g., CSV row).

        Args:
            data: Dictionary with player data keys matching class fields

        Returns:
            FantasyPlayer instance
        """
        adp_value = data.get('average_draft_position') or data.get('adp')
        processed_adp = safe_float_conversion(adp_value, None) if adp_value is not None else None

        return cls(
            id=safe_int_conversion(data.get('id'), 0),
            name=str(data.get('name', '')),
            team=str(data.get('team', '')),
            position=str(data.get('position', '')),
            bye_week=safe_int_conversion(data.get('bye_week'), 0),
            drafted_by=str(data.get('drafted_by', '')),
            locked=safe_int_conversion(data.get('locked'), 0),
            fantasy_points=safe_float_conversion(data.get('fantasy_points'), 0.0),
            average_draft_position=processed_adp,
            player_rating=safe_float_conversion(data.get('player_rating'), None) if data.get('player_rating') is not None else None,
            injury_status=str(data.get('injury_status', 'UNKNOWN')),
            score=safe_float_conversion(data.get('score'), 0.0),
            weighted_projection=safe_float_conversion(data.get('weighted_projection'), 0.0),
            consistency=safe_float_conversion(data.get('consistency'), 0.0),
            matchup_score=safe_int_conversion(data.get('matchup_score'), 0),
            team_offensive_rank=safe_int_conversion(data.get('team_offensive_rank'), None),
            team_defensive_rank=safe_int_conversion(data.get('team_defensive_rank'), None)
        )

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
        """
        Create FantasyPlayer instance from JSON dictionary.

        This method loads player data from JSON files in the player_data/ directory,
        handling all required type conversions and data transformations.

        Args:
            data: Dictionary from JSON player data with keys matching JSON structure

        Returns:
            FantasyPlayer instance with all fields populated

        Raises:
            ValueError: If required field missing (id, name, or position)

        Field Conversions:
            - id: string → int (using safe_int_conversion)
            - drafted_by: stored as string (team name) AND converted to drafted int (0/1/2) for backward compatibility
            - locked: boolean → loaded directly as is
            - projected_points/actual_points: arrays padded/truncated to exactly 17 elements
            - fantasy_points: calculated as sum of projected_points
            - position-specific stats: loaded as-is (Optional[Dict[str, List[float]]])

        Example:
            >>> json_data = {
            ...     "id": "12345",
            ...     "name": "Patrick Mahomes",
            ...     "team": "KC",
            ...     "position": "QB",
            ...     "drafted_by": "",
            ...     "locked": false,
            ...     "projected_points": [25.3, 28.1, ...],
            ...     "actual_points": [0.0, 0.0, ...],
            ...     "passing": {"completions": [22.5, ...], ...}
            ... }
            >>> player = FantasyPlayer.from_json(json_data)
            >>> print(player.name)
            'Patrick Mahomes'

        Spec Reference: sub_feature_01_core_data_loading_spec.md lines 161-240
        """
        if 'id' not in data or 'name' not in data or 'position' not in data:
            raise ValueError(f"Missing required field in player data: {data}")

        player_id = safe_int_conversion(data.get('id'), 0)

        projected_points = data.get('projected_points', [0.0] * 17)
        actual_points = data.get('actual_points', [0.0] * 17)

        projected_points = (projected_points + [0.0] * 17)[:17]
        actual_points = (actual_points + [0.0] * 17)[:17]

        drafted_by = data.get('drafted_by', '')


        locked = data.get('locked', False)

        fantasy_points = sum(projected_points)

        passing = data.get('passing')
        rushing = data.get('rushing')
        receiving = data.get('receiving')
        misc = data.get('misc')
        extra_points = data.get('extra_points')
        field_goals = data.get('field_goals')
        defense = data.get('defense')

        return cls(
            id=player_id,
            name=data.get('name'),
            team=data.get('team'),
            position=data.get('position'),
            bye_week=data.get('bye_week'),
            fantasy_points=fantasy_points,
            drafted_by=drafted_by,
            locked=locked,
            average_draft_position=data.get('average_draft_position'),
            player_rating=data.get('player_rating'),
            injury_status=data.get('injury_status', 'UNKNOWN'),
            projected_points=projected_points,
            actual_points=actual_points,
            passing=passing,
            rushing=rushing,
            receiving=receiving,
            misc=misc,
            extra_points=extra_points,
            field_goals=field_goals,
            defense=defense
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
            df = read_csv_with_validation(filepath)
        except Exception as e:
            logger.error(f"Error reading CSV file at {filepath}: {e}")
            raise

        players = []
        failed_rows = 0

        for row_idx, row in df.iterrows():
            try:
                player = cls.from_dict(row.to_dict())
                players.append(player)
            except Exception as e:
                failed_rows += 1
                logger.warning(f"Failed to parse player row {row_idx + 1}: {e}")
                continue

        if failed_rows > 0:
            logger.warning(f"Failed to parse {failed_rows} out of {len(df)} rows")

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
            logger.error(f"Excel file not found at {filepath}")
            raise
        except ValueError as e:
            if "Worksheet" in str(e) and "does not exist" in str(e):
                logger.error(f"Sheet '{sheet_name}' not found in Excel file {filepath}")
            else:
                logger.error(f"Invalid Excel file format at {filepath}: {e}")
            raise
        except PermissionError:
            logger.error(f"Permission denied reading Excel file at {filepath}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error reading Excel file at {filepath}: {e}")
            raise

        if df.empty:
            logger.warning(f"Excel sheet '{sheet_name}' is empty in {filepath}")
            return []

        players = []
        failed_rows = 0

        for row_idx, row in df.iterrows():
            try:
                player = cls.from_dict(row.to_dict())
                players.append(player)
            except Exception as e:
                failed_rows += 1
                logger.warning(f"Failed to parse player row {row_idx + 1} from sheet '{sheet_name}': {e}")
                continue

        if failed_rows > 0:
            logger.warning(f"Failed to parse {failed_rows} out of {len(df)} rows from sheet '{sheet_name}'")

        return players
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert FantasyPlayer to dictionary.

        Returns:
            Dictionary representation of the player
        """
        result = asdict(self)
        return result
    
    def is_available(self) -> bool:
        """
        Check if player is available for drafting.

        Returns:
            True if player is not drafted and not locked, False otherwise
        """
        return self.is_free_agent() and not self.locked
    
    def is_rostered(self) -> bool:
        """
        Check if player is on our team's roster.

        Returns:
            True if player is drafted by our team
        """
        return self.drafted_by == FANTASY_TEAM_NAME

    def is_free_agent(self) -> bool:
        """
        Check if player is a free agent (not drafted by any team).

        Returns:
            True if player is not drafted (drafted_by is empty string)
        """
        return self.drafted_by == ""

    def is_drafted_by_opponent(self) -> bool:
        """
        Check if player is drafted by an opponent team.

        Returns:
            True if player is drafted by a team other than ours
        """
        return self.drafted_by != "" and self.drafted_by != FANTASY_TEAM_NAME

    def is_locked(self) -> bool:
        """
        Check if player is locked from being drafted or traded.
        
        Returns:
            True if player is locked, False otherwise
        """
        return self.locked
    
    def get_risk_level(self) -> str:
        """
        Assess injury risk level based on status.

        Returns:
            Risk level string: "LOW", "MEDIUM", "HIGH"
        """
        if self.injury_status == 'ACTIVE':
            return "LOW"
        elif self.injury_status in ['QUESTIONABLE', 'OUT', 'DOUBTFUL']:
            return "MEDIUM"
        elif self.injury_status in ['INJURY_RESERVE', 'SUSPENSION', 'UNKNOWN']:
            return "HIGH"
        else:
            return "MEDIUM"
        
    def get_weekly_projections(self, config) -> List[float]:
        """
        Return hybrid weekly points: actual results for past weeks,
        projected points for current/future weeks.

        This maintains backward compatibility with the old week_N_points
        behavior where player-data-fetcher updated past weeks with actual
        results after games were played.

        Args:
            config: ConfigManager instance (for current_nfl_week)

        Returns:
            List of 17 weekly points (actual for past, projected for future)

        Note:
            This replaces the old pattern:
            [self.week_1_points, ..., self.week_17_points]
        """
        current_week = config.current_nfl_week
        result = []

        for i in range(17):
            week_num = i + 1
            if week_num < current_week:
                result.append(self.actual_points[i])
            else:
                result.append(self.projected_points[i])

        return result
    
    def get_single_weekly_projection(self, week_num: int, config) -> float:
        """
        Get weekly points for a specific week.

        Returns actual result for past weeks, projected points for future weeks.
        Delegates to get_weekly_projections() for consistency.

        Args:
            week_num: Week number (1-17)
            config: ConfigManager instance

        Returns:
            Weekly points (actual for past, projected for future)

        Raises:
            ValueError: If week_num is not in range 1-17
        """
        if not (1 <= week_num <= 17):
            raise ValueError(f"week_num must be between 1 and 17, got {week_num}")

        return self.get_weekly_projections(config)[week_num - 1]
    
    def get_rest_of_season_projection(self, config) -> float:
        """
        Calculate total projected points from current week through week 17.

        Uses hybrid weekly points from get_weekly_projections(), so if
        current_week has already been played, it includes the actual result.

        Args:
            config: ConfigManager instance

        Returns:
            Sum of projected points for remaining weeks
        """
        current_week = config.current_nfl_week
        weekly_projections = self.get_weekly_projections(config)

        total = 0.0
        for i in range(current_week, 18):
            week_projection = weekly_projections[i - 1]
            if week_projection is not None:
                total += week_projection

        return total
    
    def __str__(self) -> str:
        """String representation of the player for display."""
        status = f" ({self.injury_status})" if self.injury_status != 'ACTIVE' else ""

        if self.is_drafted_by_opponent():
            drafted = "DRAFTED"
        elif self.is_rostered():
            drafted = "ROSTERED"
        else:
            drafted = "AVAILABLE"

        locked_indicator = " [LOCKED]" if self.is_locked() else ""

        return f"{self.name} ({self.team} {self.position}) - {self.score:.1f} pts {status} [Bye={self.bye_week}] [{drafted}]{locked_indicator}"
    
    def __repr__(self) -> str:
        """Developer representation of the player."""
        return f"FantasyPlayer(id='{self.id}', name='{self.name}', team='{self.team}', position='{self.position}', fantasy_points={self.fantasy_points})"
    
    def get_position_including_flex(self):
        """
        Get player's position with FLEX eligibility if applicable.

        In fantasy football, FLEX positions can be filled by RB or WR.
        This helps determine roster slot compatibility.

        Returns:
            'FLEX' for RB/WR players, original position otherwise (QB, TE, K, DEF)
        """
        FLEX_ELIGIBLE_POSITIONS = ['RB', 'WR']
        return 'FLEX' if self.position in FLEX_ELIGIBLE_POSITIONS else self.position

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
        """
        Check equality based on player ID.

        This allows player comparisons and use in sets/dicts.
        Two players are equal if they have the same ID.
        """
        if not isinstance(other, FantasyPlayer):
            return False
        return self.id == other.id

    def __hash__(self):
        """
        Make FantasyPlayer hashable based on ID.

        This allows players to be used in sets and as dictionary keys.
        Hash must be consistent with __eq__ (same ID → same hash).
        """
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