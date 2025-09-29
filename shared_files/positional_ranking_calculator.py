#!/usr/bin/env python3
"""
Positional Ranking Calculator for Fantasy Football Helper Scripts

This module calculates position-specific score adjustments based on team offensive/defensive
rankings and opponent matchups. Integrates with the fantasy football system to provide
enhanced matchup-based scoring across all modules.

Author: Kai Mizuno
Last Updated: September 2025
"""

from pathlib import Path
from typing import Dict, Optional, Tuple, List
import pandas as pd
from shared_files.logging_utils import setup_module_logging

from shared_files.TeamData import TeamData, load_teams_from_csv


class PositionalRankingCalculator:
    """Calculates position-specific score adjustments based on team rankings and matchups."""

    def __init__(self, teams_file_path: Optional[str] = None, teams_dataframe: Optional[pd.DataFrame] = None, config: Optional[Dict] = None):
        """
        Initialize PositionalRankingCalculator.

        Args:
            teams_file_path: Path to teams.csv file. If None, uses shared_files/teams.csv
            teams_dataframe: Teams data as pandas DataFrame. If provided, takes precedence over teams_file_path
            config: Configuration dictionary for adjustment factors
        """
        self.logger = setup_module_logging(__name__)

        # Store teams data source
        self.teams_dataframe = teams_dataframe
        if teams_file_path:
            self.teams_file = Path(teams_file_path)
        else:
            # When in shared_files, teams.csv is in the same directory
            shared_files_dir = Path(__file__).parent
            self.teams_file = shared_files_dir / "teams.csv"

        self.team_data_cache: Dict[str, TeamData] = {}
        self._load_team_data()

        # Configuration for adjustment factors (multipliers applied to base scores)
        self.config = self._get_default_config()
        if config:
            # Merge custom config with defaults
            self.config.update(config)

    def _get_default_config(self) -> Dict:
        """Get default configuration for positional ranking adjustments."""
        return {
            # Position groups for ranking application
            "offensive_positions": ["QB", "RB", "WR", "TE"],  # Use team offensive rank vs opponent defense
            "defensive_positions": ["DST"],                   # Use team defensive rank vs opponent offense
            "kicker_positions": ["K"],                       # Use team offensive rank (field goal opportunities)

            # Ranking tiers and multipliers (applied to projected fantasy points)
            "excellent_threshold": 5,     # Rank 1-5 (top tier)
            "good_threshold": 12,         # Rank 6-12 (above average)
            "poor_threshold": 25,         # Rank 25-32 (bottom tier)

            # Multipliers for matchup quality (conservative adjustments)
            "excellent_matchup": 1.1,    # 10% boost for great matchups
            "good_matchup": 1.05,         # 5% boost for good matchups
            "neutral_matchup": 1.0,       # No adjustment
            "bad_matchup": 0.95,          # 5% penalty for bad matchups
            "terrible_matchup": 0.9,     # 10% penalty for terrible matchups

            # Enable/disable adjustments
            "enable_adjustments": True,
            "adjustment_weight": 0.15,    # How much impact rankings have (15% max adjustment)

            # Logging
            "log_adjustments": True       # Log significant adjustments for transparency
        }

    def _load_team_data(self) -> None:
        """Load team data from DataFrame or CSV file."""
        try:
            teams = []

            if self.teams_dataframe is not None:
                # Load from provided DataFrame (preferred for simulation)
                teams = self._load_teams_from_dataframe(self.teams_dataframe)
                self.logger.debug(f"Loaded team data from DataFrame: {len(teams)} teams")
            else:
                # Load from file (default behavior)
                if not self.teams_file.exists():
                    self.logger.warning(f"Teams file not found: {self.teams_file}. Positional rankings disabled.")
                    return

                teams = load_teams_from_csv(str(self.teams_file))
                self.logger.debug(f"Loaded team data from file: {len(teams)} teams")

            # Build team lookup cache
            self.team_data_cache = {team.team: team for team in teams}

            self.logger.info(f"Loaded team data for positional ranking calculations: {len(self.team_data_cache)} teams")

        except Exception as e:
            self.logger.warning(f"Error loading team data: {e}. Positional rankings disabled.")
            self.team_data_cache = {}

    def _load_teams_from_dataframe(self, teams_df: pd.DataFrame) -> List[TeamData]:
        """Convert pandas DataFrame to list of TeamData objects."""
        teams = []
        for _, row in teams_df.iterrows():
            team_data = TeamData(
                team=row.get('team', ''),
                offensive_rank=int(row.get('offensive_rank', 16)),  # Default to middle rank
                defensive_rank=int(row.get('defensive_rank', 16)),  # Default to middle rank
                opponent=row.get('opponent', '')
            )
            teams.append(team_data)
        return teams

    def calculate_positional_adjustment(self,
                                      player_team: str,
                                      position: str,
                                      base_points: float,
                                      current_week: Optional[int] = None) -> Tuple[float, str]:
        """
        Calculate positional adjustment factor based on team rankings and opponent matchup.

        Args:
            player_team: Player's team abbreviation (e.g., 'PHI', 'KC')
            position: Player position (e.g., 'QB', 'RB', 'WR', 'TE', 'K', 'DST')
            base_points: Base projected fantasy points
            current_week: Current NFL week (for future opponent lookup - not implemented yet)

        Returns:
            Tuple of (adjusted_points, explanation_string)
        """
        if not self.config["enable_adjustments"] or not self.team_data_cache:
            return base_points, "No adjustment (rankings unavailable)"

        team_data = self.team_data_cache.get(player_team)
        if not team_data:
            return base_points, f"No adjustment (team {player_team} not found)"

        # Determine which ranking to use and matchup context
        if position in self.config["offensive_positions"]:
            # Offensive players: use team offensive rank (how good is player's team offense)
            our_rank = team_data.offensive_rank
            context = "offensive"
        elif position in self.config["defensive_positions"]:
            # Defensive players: use team defensive rank (how good is player's team defense)
            our_rank = team_data.defensive_rank
            context = "defensive"
        elif position in self.config["kicker_positions"]:
            # Kickers: use team offensive rank (field goal opportunities from red zone stalls)
            our_rank = team_data.offensive_rank
            context = "offensive (kicking)"
        else:
            return base_points, f"No adjustment (unknown position {position})"

        if our_rank is None:
            return base_points, f"No adjustment ({context} rank unavailable)"

        # Calculate adjustment multiplier based on ranking
        multiplier = self._get_multiplier_from_rank(our_rank)

        # Apply weight factor to limit impact
        weight = self.config["adjustment_weight"]
        final_multiplier = 1.0 + (multiplier - 1.0) * weight

        adjusted_points = base_points * final_multiplier

        # Create explanation
        rank_tier = self._get_rank_tier_description(our_rank)
        adjustment_pct = (final_multiplier - 1.0) * 100

        explanation = f"{rank_tier} {context} (rank {our_rank}): {adjustment_pct:+.1f}%"

        # Log significant adjustments
        if self.config["log_adjustments"] and abs(adjustment_pct) >= 5.0:
            self.logger.info(f"{player_team} {position}: {base_points:.1f} -> {adjusted_points:.1f} pts ({explanation})")

        return adjusted_points, explanation

    def _get_multiplier_from_rank(self, rank: int) -> float:
        """Convert team rank to adjustment multiplier."""
        if rank <= self.config["excellent_threshold"]:
            return self.config["excellent_matchup"]
        elif rank <= self.config["good_threshold"]:
            return self.config["good_matchup"]
        elif rank >= self.config["poor_threshold"]:
            return self.config["bad_matchup"]
        else:
            return self.config["neutral_matchup"]

    def _get_rank_tier_description(self, rank: int) -> str:
        """Get human-readable description of rank tier."""
        if rank <= self.config["excellent_threshold"]:
            return "Elite"
        elif rank <= self.config["good_threshold"]:
            return "Good"
        elif rank >= self.config["poor_threshold"]:
            return "Poor"
        else:
            return "Average"

    def is_positional_ranking_available(self) -> bool:
        """Check if team data is loaded and positional ranking is available."""
        return bool(self.team_data_cache) and self.config["enable_adjustments"]

    def get_available_teams(self) -> list[str]:
        """Get list of teams for which ranking data is available."""
        return list(self.team_data_cache.keys())

    def get_team_summary(self, team: str) -> Optional[str]:
        """Get summary string for team rankings."""
        team_data = self.team_data_cache.get(team)
        if not team_data:
            return None

        off_desc = self._get_rank_tier_description(team_data.offensive_rank or 16)
        def_desc = self._get_rank_tier_description(team_data.defensive_rank or 16)

        return f"{team}: {off_desc} offense (#{team_data.offensive_rank}), {def_desc} defense (#{team_data.defensive_rank})"

    def reload_team_data(self) -> None:
        """Reload team data from teams.csv file."""
        self.team_data_cache = {}
        self._load_team_data()