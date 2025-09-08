#!/usr/bin/env python3
"""
FantasyPlayer Class Definition

This module defines the FantasyPlayer class for NFL fantasy football player data.
Designed to be used across multiple scripts for consistent player representation.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List
import pandas as pd

# Import will be done dynamically to avoid circular imports


@dataclass
class FantasyPlayer:
    """
    Represents a fantasy football player with all relevant data fields.
    
    This class maps to the CSV/Excel export structure from data_fetcher-players.py
    and provides a consistent interface for player data across multiple scripts.
    """
    
    # Core identification
    id: str
    name: str
    team: str
    position: str
    
    # Fantasy relevant data  
    bye_week: Optional[int] = None
    drafted: int = 0  # 0 = not drafted, 1 = drafted, 2 = on our team
    locked: int = 0  # 0 = not locked, 1 = locked (cannot be drafted or traded)
    fantasy_points: float = 0.0
    average_draft_position: Optional[float] = None  # ESPN's ADP data
    
    # Injury information
    injury_status: str = "UNKNOWN"  # ACTIVE, QUESTIONABLE, OUT, etc.

    # Draft helper specific fields (computed later)
    score: float = 0.0  # Overall score for draft ranking
    weighted_projection: float = 0.0  # Normalized projection score
    
    # Metadata
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
        """
        Create a FantasyPlayer instance from a dictionary (e.g., CSV row).
        
        Args:
            data: Dictionary with player data keys matching class fields
            
        Returns:
            FantasyPlayer instance
        """
        return cls(
            id=str(data.get('id', '')),
            name=str(data.get('name', '')),
            team=str(data.get('team', '')),
            position=str(data.get('position', '')),
            bye_week=int(float(data['bye_week'])) if data.get('bye_week') and str(data['bye_week']).replace('.','').isdigit() else None,
            drafted=int(data.get('drafted', 0)),
            locked=int(data.get('locked', 0)),
            fantasy_points=float(data.get('fantasy_points', 0.0)),
            average_draft_position=float(data.get('average_draft_position')) if data.get('average_draft_position') else None,
            injury_status=str(data.get('injury_status', 'UNKNOWN')),
            score=float(data.get('score', 0.0)),
            weighted_projection=float(data.get('weighted_projection', 0.0))
        )
    
    @classmethod
    def from_csv_file(cls, filepath: str) -> List['FantasyPlayer']:
        """
        Load all players from a CSV file.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            List of FantasyPlayer instances
        """
        df = pd.read_csv(filepath)
        players = []
        
        for _, row in df.iterrows():
            try:
                player = cls.from_dict(row.to_dict())
                players.append(player)
            except Exception as e:
                print(f"Warning: Failed to parse player row: {e}")
                continue
                
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
        """
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        players = []
        
        for _, row in df.iterrows():
            try:
                player = cls.from_dict(row.to_dict())
                players.append(player)
            except Exception as e:
                print(f"Warning: Failed to parse player row: {e}")
                continue
                
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
    
    def is_locked(self) -> bool:
        """
        Check if player is locked from being drafted or traded.
        
        Returns:
            True if player is locked, False otherwise
        """
        return self.locked == 1
    
    def is_seriously_injured(self) -> bool:
        """
        Check if player is seriously injured (OUT or on IR).
        
        Returns:
            True if player is OUT or on INJURY_RESERVE
        """
        return self.injury_status in ['OUT', 'INJURY_RESERVE']
    
    def is_healthy(self) -> bool:
        """
        Check if player is healthy (not injured and active status).
        
        Returns:
            True if player appears healthy for play
        """
        return self.injury_status in ['ACTIVE', 'UNKNOWN']
    
    def get_risk_level(self) -> str:
        """
        Assess injury risk level based on status.
        
        Returns:
            Risk level string: "LOW", "MEDIUM", "HIGH"
        """
        if self.injury_status == 'ACTIVE':
            return "LOW"
        elif self.injury_status in ['QUESTIONABLE', 'UNKNOWN']:
            return "MEDIUM"
        elif self.injury_status in ['OUT', 'DOUBTFUL', 'INJURY_RESERVE', 'SUSPENSION']:
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


# Utility functions for working with FantasyPlayer lists
def filter_by_position(players: List[FantasyPlayer], position: str) -> List[FantasyPlayer]:
    """Filter players by position."""
    return [p for p in players if p.position == position]


def filter_available_players(players: List[FantasyPlayer]) -> List[FantasyPlayer]:
    """Filter to only available (not drafted) players."""
    return [p for p in players if p.is_available()]


def filter_healthy_players(players: List[FantasyPlayer]) -> List[FantasyPlayer]:
    """Filter to only healthy players."""
    return [p for p in players if p.is_healthy()]


def sort_by_fantasy_points(players: List[FantasyPlayer], reverse: bool = True) -> List[FantasyPlayer]:
    """Sort players by fantasy points (highest first by default)."""
    return sorted(players, key=lambda p: p.fantasy_points, reverse=reverse)


def get_top_players_by_position(players: List[FantasyPlayer], position: str, count: int = 10) -> List[FantasyPlayer]:
    """Get top N players for a specific position by fantasy points."""
    position_players = filter_by_position(players, position)
    sorted_players = sort_by_fantasy_points(position_players)
    return sorted_players[:count]


def players_to_dataframe(players: List[FantasyPlayer]) -> pd.DataFrame:
    """Convert list of FantasyPlayer objects to pandas DataFrame."""
    return pd.DataFrame([player.to_dict() for player in players])


# Example usage
if __name__ == "__main__":
    # Example of loading from CSV
    try:
        players = FantasyPlayer.from_csv_file("data/nfl_projections/nfl_projections_latest_weekly.csv")
        print(f"Loaded {len(players)} players from CSV")
        
        # Show top 5 QBs
        top_qbs = get_top_players_by_position(players, 'QB', 5)
        print("\nTop 5 QBs:")
        for qb in top_qbs:
            print(f"  {qb}")
            
    except FileNotFoundError:
        print("CSV file not found. Run data_fetcher-players.py first to generate data.")
    except Exception as e:
        print(f"Error loading players: {e}")