#!/usr/bin/env python3
"""
Fantasy Football Starter Helper

This script analyzes your current roster and recommends optimal starting lineups
based on current week projections from players.csv weekly columns.

Features:
- Identifies current roster players (drafted=2)
- Reads current week projections from CSV weekly columns (no API requests)
- Recommends optimal starting lineup: QB, RB, RB, WR, WR, TE, FLEX, K, DEF
- Handles FLEX position (best available RB or WR)
- Applies injury and bye week penalties
- Shows bench alternatives

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025

Dependencies:
    pip install pandas
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
from datetime import datetime
from io import StringIO
from contextlib import redirect_stdout

import pandas as pd

# Add parent directory to path for shared imports
sys.path.append(str(Path(__file__).parent.parent))

from starter_helper_config import (
    CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT,
    PLAYERS_CSV, LOGGING_ENABLED, LOGGING_LEVEL,
    SHOW_PROJECTION_DETAILS, SHOW_INJURY_STATUS,
    RECOMMENDATION_COUNT, STARTING_LINEUP_REQUIREMENTS,
    SAVE_OUTPUT_TO_FILE, DATA_DIR, get_timestamped_filepath, get_latest_filepath,
    ENABLE_MATCHUP_ANALYSIS, SHOW_MATCHUP_SIMPLE, SHOW_MATCHUP_DETAILED
)
# from espn_current_week_client import ESPNCurrentWeekClient  # No longer needed - using CSV weekly columns
from lineup_optimizer import LineupOptimizer, OptimalLineup, StartingRecommendation


class StarterHelper:
    """Main class for generating starting lineup recommendations"""

    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.optimizer = LineupOptimizer()
        self.output_buffer = StringIO()
        self.matchup_analysis = None

        # Initialize matchup analysis if enabled
        if ENABLE_MATCHUP_ANALYSIS:
            try:
                from matchup_analyzer import MatchupAnalyzer
                self.matchup_analyzer = MatchupAnalyzer()
                self.logger.info("Matchup analysis initialized")
            except ImportError as e:
                self.logger.warning(f"Matchup analysis disabled due to import error: {e}")
                self.matchup_analyzer = None
        else:
            self.matchup_analyzer = None

    def setup_logging(self):
        """Configure logging based on config settings"""
        if not LOGGING_ENABLED:
            logging.disable(logging.CRITICAL)
            return

        level = getattr(logging, LOGGING_LEVEL.upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

    def save_output_to_files(self, output_content: str):
        """
        Save output to both timestamped and latest files

        Args:
            output_content: The content to save to files
        """
        if not SAVE_OUTPUT_TO_FILE:
            return

        try:
            # Ensure data directory exists
            os.makedirs(DATA_DIR, exist_ok=True)

            # Save to timestamped file
            timestamped_file = get_timestamped_filepath()
            with open(timestamped_file, 'w', encoding='utf-8') as f:
                f.write(output_content)
            self.logger.info(f"Results saved to: {timestamped_file}")

            # Save to latest file
            latest_file = get_latest_filepath()
            with open(latest_file, 'w', encoding='utf-8') as f:
                f.write(output_content)
            self.logger.info(f"Latest results updated: {latest_file}")

        except Exception as e:
            self.logger.error(f"Error saving output to files: {str(e)}")
            print(f"Warning: Could not save results to file: {str(e)}")

    def print_and_capture(self, message: str):
        """
        Print message to console and capture for file output

        Args:
            message: The message to print and capture
        """
        print(message)
        self.output_buffer.write(message + '\n')

    def load_roster_players(self) -> pd.DataFrame:
        """
        Load current roster players from players.csv

        Returns:
            DataFrame containing only roster players (drafted=2)
        """
        try:
            # Load all players
            players_df = pd.read_csv(PLAYERS_CSV)

            # Filter for roster players (drafted=2)
            roster_players = players_df[players_df['drafted'] == 2].copy()

            self.logger.info(f"Loaded {len(roster_players)} roster players from {PLAYERS_CSV}")

            # Log roster composition
            position_counts = roster_players['position'].value_counts()
            self.logger.info(f"Roster composition: {dict(position_counts)}")

            return roster_players

        except FileNotFoundError:
            self.logger.error(f"Players CSV file not found: {PLAYERS_CSV}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading roster players: {str(e)}")
            raise

    def get_current_week_projections(self, roster_players: pd.DataFrame) -> dict:
        """
        Get current week projections for all roster players from CSV weekly columns

        Args:
            roster_players: DataFrame of roster players

        Returns:
            Dictionary mapping player_id to current week projected points
        """
        self.logger.info(f"Reading Week {CURRENT_NFL_WEEK} projections from players.csv weekly columns")

        projections = {}
        week_column = f"week_{CURRENT_NFL_WEEK}_points"

        # Check if the weekly column exists in the DataFrame
        if week_column not in roster_players.columns:
            self.logger.warning(f"Column '{week_column}' not found in players.csv. Available columns: {roster_players.columns.tolist()}")
            # Fallback to fantasy_points column if weekly column doesn't exist
            if 'fantasy_points' in roster_players.columns:
                self.logger.info(f"Using 'fantasy_points' as fallback for weekly projections")
                return {str(player['id']): float(player.get('fantasy_points', 0.0)) / 17.0
                       for _, player in roster_players.iterrows()}
            else:
                # Return empty projections if no fallback available
                return {str(player_id): 0.0 for player_id in roster_players['id'].tolist()}

        # Extract projections from the weekly column
        for _, player in roster_players.iterrows():
            player_id = str(player['id'])
            week_points = player.get(week_column, 0.0)

            # Handle NaN, None, or invalid values
            try:
                projections[player_id] = float(week_points) if pd.notna(week_points) else 0.0
            except (ValueError, TypeError):
                projections[player_id] = 0.0
                self.logger.warning(f"Invalid weekly points for player {player.get('name', 'Unknown')} (ID: {player_id}): {week_points}")

        # Log summary
        successful_projections = sum(1 for p in projections.values() if p > 0)
        total_players = len(projections)
        self.logger.info(f"Retrieved {successful_projections}/{total_players} projections from CSV weekly columns")

        # Log some example projections for verification
        if projections:
            top_projections = sorted(projections.items(), key=lambda x: x[1], reverse=True)[:3]
            for player_id, points in top_projections:
                player_name = roster_players[roster_players['id'] == int(player_id)]['name'].iloc[0] if len(roster_players[roster_players['id'] == int(player_id)]) > 0 else "Unknown"
                self.logger.info(f"Sample projection: {player_name} (ID: {player_id}) = {points:.1f} points")

        return projections

    def display_optimal_lineup(self, lineup: OptimalLineup):
        """Display the optimal starting lineup"""
        self.print_and_capture(f"\n{'='*80}")
        self.print_and_capture(f"OPTIMAL STARTING LINEUP - WEEK {CURRENT_NFL_WEEK} ({NFL_SCORING_FORMAT.upper()} SCORING)")
        self.print_and_capture(f"{'='*80}")

        # Define the order to display starters (as requested)
        starter_positions = [
            ("QB", lineup.qb),
            ("RB", lineup.rb1),
            ("RB", lineup.rb2),
            ("WR", lineup.wr1),
            ("WR", lineup.wr2),
            ("TE", lineup.te),
            ("FLEX", lineup.flex),
            ("K", lineup.k),
            ("DEF", lineup.dst)
        ]

        total_projected = 0.0

        for i, (pos_label, recommendation) in enumerate(starter_positions, 1):
            if recommendation:
                total_projected += recommendation.projected_points

                # Format player info
                name_team = f"{recommendation.name} ({recommendation.team})"
                points_info = f"{recommendation.projected_points:.1f} pts"

                # Add injury status if enabled
                status_info = ""
                if SHOW_INJURY_STATUS and recommendation.injury_status != "ACTIVE":
                    status_info = f" [{recommendation.injury_status}]"

                # Add matchup info if enabled and available
                matchup_info = ""
                if ENABLE_MATCHUP_ANALYSIS and recommendation.matchup_indicator:
                    if SHOW_MATCHUP_SIMPLE:
                        matchup_info = f" {recommendation.matchup_indicator}"
                    if SHOW_MATCHUP_DETAILED and recommendation.opponent_team:
                        home_away = "H" if recommendation.is_home_game else "A"
                        matchup_info += f" vs {recommendation.opponent_team} ({home_away})"

                # Add penalty info if there are penalties
                penalty_info = ""
                if SHOW_PROJECTION_DETAILS and recommendation.reason != "No penalties":
                    penalty_info = f" ({recommendation.reason})"

                self.print_and_capture(f"{i:2d}. {pos_label:4s}: {name_team:25s} - {points_info}{status_info}{matchup_info}{penalty_info}")

            else:
                self.print_and_capture(f"{i:2d}. {pos_label:4s}: No available player")

        self.print_and_capture(f"{'-'*80}")
        self.print_and_capture(f"TOTAL PROJECTED POINTS: {total_projected:.1f}")
        self.print_and_capture(f"{'-'*80}")

    def display_bench_recommendations(self,
                                    bench_recommendations: list,
                                    used_player_ids: set):
        """Display top bench players that could be considered"""
        if not bench_recommendations:
            return

        self.print_and_capture(f"\nTOP BENCH ALTERNATIVES:")
        self.print_and_capture(f"{'-'*60}")

        for i, rec in enumerate(bench_recommendations, 1):
            name_team = f"{rec.name} ({rec.team}) - {rec.position}"
            points_info = f"{rec.projected_points:.1f} pts"

            # Add injury status
            status_info = ""
            if SHOW_INJURY_STATUS and rec.injury_status != "ACTIVE":
                status_info = f" [{rec.injury_status}]"

            self.print_and_capture(f"{i:2d}. {name_team:35s} - {points_info}{status_info}")

    def display_roster_summary(self, roster_players: pd.DataFrame, projections: dict):
        """Display summary of all roster players with projections"""
        if not SHOW_PROJECTION_DETAILS:
            return

        self.print_and_capture(f"\nFULL ROSTER - WEEK {CURRENT_NFL_WEEK} PROJECTIONS:")
        self.print_and_capture(f"{'-'*80}")

        # Sort by projected points (descending)
        roster_with_projections = []
        for _, player in roster_players.iterrows():
            player_id = str(player['id'])
            projected = projections.get(player_id, 0.0)
            roster_with_projections.append({
                'name': player['name'],
                'team': player['team'],
                'position': player['position'],
                'projected': projected,
                'injury_status': player.get('injury_status', 'ACTIVE'),
                'bye_week': player.get('bye_week', 0)
            })

        # Sort by projected points
        roster_with_projections.sort(key=lambda x: x['projected'], reverse=True)

        for i, player in enumerate(roster_with_projections[:RECOMMENDATION_COUNT], 1):
            name_pos = f"{player['name']} ({player['team']}) - {player['position']}"
            points_info = f"{player['projected']:.1f} pts"

            status_info = ""
            if player['injury_status'] != "ACTIVE":
                status_info = f" [{player['injury_status']}]"

            bye_info = ""
            if player['bye_week'] == CURRENT_NFL_WEEK:
                bye_info = " [BYE]"

            self.print_and_capture(f"{i:2d}. {name_pos:40s} - {points_info}{status_info}{bye_info}")

    async def perform_matchup_analysis(self, roster_players: pd.DataFrame):
        """
        Perform matchup analysis for all roster players.

        Args:
            roster_players: DataFrame of roster players (drafted=2)

        Returns:
            WeeklyMatchupAnalysis object or None if analysis fails
        """
        try:
            # Convert roster players to list format expected by matchup analyzer
            roster_player_list = []
            for _, player in roster_players.iterrows():
                player_dict = {
                    'id': str(player['id']),
                    'name': player['name'],
                    'position': player['position'],
                    'team_id': self._get_team_id_from_abbreviation(player['team']),
                    'injury_status': player.get('injury_status', 'ACTIVE')
                }
                roster_player_list.append(player_dict)

            # Perform weekly matchup analysis
            matchup_analysis = await self.matchup_analyzer.analyze_weekly_matchups(
                roster_player_list, week=CURRENT_NFL_WEEK
            )

            return matchup_analysis

        except Exception as e:
            self.logger.error(f"Failed to perform matchup analysis: {e}")
            return None

    def _get_team_id_from_abbreviation(self, team_abbr: str) -> int:
        """Convert team abbreviation to ESPN team ID"""
        # ESPN team abbreviation to ID mapping
        team_mapping = {
            'ATL': 1, 'BUF': 2, 'CHI': 3, 'CIN': 4, 'CLE': 5, 'DAL': 6,
            'DEN': 7, 'DET': 8, 'GB': 9, 'TEN': 10, 'IND': 11, 'KC': 12,
            'LV': 13, 'LAR': 14, 'MIA': 15, 'MIN': 16, 'NE': 17, 'NO': 18,
            'NYG': 19, 'NYJ': 20, 'PHI': 21, 'ARI': 22, 'PIT': 23, 'LAC': 24,
            'SF': 25, 'SEA': 26, 'TB': 27, 'WSH': 28, 'CAR': 29, 'JAX': 30,
            'BAL': 33, 'HOU': 34
        }
        return team_mapping.get(team_abbr, 1)  # Default to ATL if not found

    async def run(self):
        """Main execution method"""
        try:
            self.print_and_capture(f"Fantasy Football Starter Helper")
            self.print_and_capture(f"Week {CURRENT_NFL_WEEK} of {NFL_SEASON} NFL Season")
            self.print_and_capture(f"Scoring Format: {NFL_SCORING_FORMAT.upper()}")
            self.print_and_capture("="*60)

            # Load roster players
            roster_players = self.load_roster_players()

            if roster_players.empty:
                error_msg = "ERROR: No roster players found! Make sure players have drafted=2 in players.csv"
                self.print_and_capture(error_msg)
                return

            # Get current week projections
            projections = self.get_current_week_projections(roster_players)

            # Perform matchup analysis if enabled
            if ENABLE_MATCHUP_ANALYSIS and self.matchup_analyzer:
                self.print_and_capture("Performing matchup analysis...")
                self.matchup_analysis = await self.perform_matchup_analysis(roster_players)
                if self.matchup_analysis:
                    self.print_and_capture(f"Matchup analysis complete for {self.matchup_analysis.total_players_analyzed} players")
                else:
                    self.print_and_capture("Matchup analysis failed, proceeding without matchup data")

            # Optimize lineup
            optimal_lineup = self.optimizer.optimize_lineup(roster_players, projections, self.matchup_analysis)

            # Display optimal lineup
            self.display_optimal_lineup(optimal_lineup)

            # Get used player IDs for bench recommendations
            used_player_ids = set()
            for starter in optimal_lineup.get_all_starters():
                if starter:
                    used_player_ids.add(starter.player_id)

            # Display bench recommendations
            bench_recs = self.optimizer.get_bench_recommendations(
                roster_players, projections, used_player_ids, count=5, matchup_analysis=self.matchup_analysis
            )
            self.display_bench_recommendations(bench_recs, used_player_ids)

            # Display full roster if detailed view is enabled
            self.display_roster_summary(roster_players, projections)

            self.print_and_capture(f"\nStarter recommendations complete for Week {CURRENT_NFL_WEEK}")
            self.print_and_capture(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Save output to files
            if SAVE_OUTPUT_TO_FILE:
                output_content = self.output_buffer.getvalue()
                self.save_output_to_files(output_content)

        except Exception as e:
            self.logger.error(f"Error in starter helper execution: {str(e)}")
            error_msg = f"Error: {str(e)}"
            self.print_and_capture(error_msg)

            # Save output even if there was an error
            if SAVE_OUTPUT_TO_FILE:
                output_content = self.output_buffer.getvalue()
                self.save_output_to_files(output_content)
            raise

        finally:
            # Cleanup matchup analyzer resources
            if self.matchup_analyzer:
                await self.matchup_analyzer.close()


async def main():
    """Main entry point"""
    helper = StarterHelper()
    await helper.run()


if __name__ == "__main__":
    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)