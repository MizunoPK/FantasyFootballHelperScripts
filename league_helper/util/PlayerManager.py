"""
Player Manager

Manages all player data, scoring calculations, and roster operations.
This is the core module responsible for loading player data from CSV,
calculating player scores using the 9-step scoring algorithm, and
managing draft operations.

Key responsibilities:
- Loading and parsing player data from players.csv
- Calculating consistency scores from weekly projections
- Computing the 9-step scoring algorithm for player evaluation
- Managing the team roster through FantasyTeam
- Updating the CSV file with roster changes
- Displaying roster information

The 9-step scoring algorithm:
1. Normalization (based on fantasy_points projection)
2. ADP Multiplier (market wisdom adjustment)
3. Player Rating Multiplier (expert consensus)
4. Team Quality Multiplier (offensive/defensive strength)
5. Consistency Multiplier (CV-based volatility)
6. Matchup Multiplier (opponent strength)
7. Draft Order Bonus (positional value by round)
8. Bye Week Penalty (same-position and different-position roster conflicts)
   - BASE_BYE_PENALTY applied per same-position overlap
   - DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY applied per different-position overlap
9. Injury Penalty (risk assessment)

Author: Kai Mizuno
"""

import csv
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import statistics

import sys
import logging
from util.TeamDataManager import TeamDataManager
from util.SeasonScheduleManager import SeasonScheduleManager
from util.FantasyTeam import FantasyTeam
from util.ProjectedPointsManager import ProjectedPointsManager

sys.path.append(str(Path(__file__).parent))
import constants as Constants
from ConfigManager import ConfigManager
from ScoredPlayer import ScoredPlayer
from player_scoring import PlayerScoringCalculator

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class PlayerManager:
    """
    Manages player data, scoring, and roster operations.

    This class is responsible for all player-related functionality including
    loading player data from CSV, calculating scores using the 9-step algorithm,
    managing the team roster, and persisting changes back to the CSV file.

    Attributes:
        logger: Logger instance for tracking operations
        config (ConfigManager): Configuration manager for scoring parameters
        team_data_manager (TeamDataManager): Manager for team rankings and matchups
        season_schedule_manager (SeasonScheduleManager): Manager for season schedule data
        file_str (str): Path to players.csv file
        team (FantasyTeam): Current fantasy team roster
        players (List[FantasyPlayer]): All available players
        max_projection (int): Maximum fantasy points projection (for normalization)

    Example:
        >>> player_manager = PlayerManager(data_folder, config, team_data_manager, season_schedule_manager)
        >>> score = player_manager.score_player(player, draft_round=0)
        >>> can_add = player_manager.can_draft(player)
        >>> if can_add:
        ...     player_manager.draft_player(player)
        ...     player_manager.update_players_file()
    """

    def __init__(
        self,
        data_folder: Path,
        config: ConfigManager,
        team_data_manager: TeamDataManager,
        season_schedule_manager: SeasonScheduleManager
    ) -> None:
        """
        Initialize the Player Manager.

        Args:
            data_folder (Path): Path to data directory containing players.csv
            config (ConfigManager): Configuration manager with scoring parameters
            team_data_manager (TeamDataManager): Manager for team rankings and matchups
            season_schedule_manager (SeasonScheduleManager): Manager for season schedule data

        Side Effects:
            - Loads all players from players.csv
            - Calculates consistency scores for each player
            - Initializes the team roster with drafted players
            - Logs player loading statistics
        """
        self.logger = get_logger()
        self.logger.debug("Initializing Player Manager")

        self.config = config
        self.team_data_manager = team_data_manager
        self.season_schedule_manager = season_schedule_manager
        self.projected_points_manager = ProjectedPointsManager(config, data_folder)

        # Initialize scoring calculator (max_projection will be updated in load_players_from_csv)
        self.scoring_calculator = PlayerScoringCalculator(
            config,
            self.projected_points_manager,
            0.0,
            team_data_manager,
            season_schedule_manager,
            config.current_nfl_week
        )

        self.file_str = str(data_folder / 'players.csv')
        self.logger.debug(f"Players CSV path: {self.file_str}")

        self.team: FantasyTeam
        self.players: List[FantasyPlayer] = []
        self.max_projection : int = 0

        self.load_players_from_csv()
        self.load_team()
        self.logger.debug(f"Player Manager initialized with {len(self.players)} players, {len(self.team.roster)} on roster")


    def load_players_from_csv(self) -> None:
        """
        Load players from CSV file using the new FantasyPlayer class.

        This function now supports the new projection data format with fantasy_points
        and can fall back to the legacy format if needed.
        """
        players: list[FantasyPlayer] = []
        self.max_projection = 0.0

        # Define required columns for basic player data
        # These are the minimum fields needed to create a valid FantasyPlayer
        required_columns = ['id', 'name', 'team', 'position']

        # Track consistency data statistics for logging purposes
        # This helps monitor data quality and identify players with insufficient historical data
        consistency_stats = {
            'sufficient_data': 0,      # Players with MIN_WEEKS or more of data
            'insufficient_data': 0,    # Players defaulted to MEDIUM consistency
            'by_weeks': {0: 0, 1: 0, 2: 0}  # Breakdown of players by weeks of data
        }

        try:
            with open(self.file_str, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # Validate that all required columns are present in the CSV
                # This catches corrupted or incomplete data files early
                if not all(col in reader.fieldnames for col in required_columns):
                    missing_cols = [col for col in required_columns if col not in reader.fieldnames]
                    raise ValueError(f"Missing required columns in CSV: {missing_cols}")

                # Track rows processed and errors encountered
                row_count = 0
                error_count = 0

                # Process each row in the CSV file
                # Start at row 2 to account for header row in error messages
                for row_num, row in enumerate(reader, start=2):
                    row_count += 1
                    try:
                        # Convert CSV row dictionary into FantasyPlayer object
                        # This handles type conversion and sets default values for missing fields
                        player = FantasyPlayer.from_dict(row)

                        # Validate player data before adding to roster
                        # Empty names indicate corrupt data rows
                        if not player.name:
                            self.logger.warning(f"Warning: Empty player name on row {row_num}, skipping")
                            error_count += 1
                            continue

                        # Validate position is one of the allowed values (QB, RB, WR, TE, K, DST)
                        # Invalid positions would break roster management logic
                        if player.position not in self.config.max_positions:
                            self.logger.warning(f"Warning: Invalid position '{player.position}' for player {player.name} on row {row_num}, skipping")
                            error_count += 1
                            continue

                        # Calculate rest-of-season projection by summing weeks from current week onwards
                        # This adjusts for the current point in the season (early vs late season)
                        player.fantasy_points = player.get_rest_of_season_projection(self.config.current_nfl_week)

                        # Calculate consistency score (coefficient of variation) from historical weekly data
                        # Returns (consistency_value, weeks_with_data) tuple
                        consistency_val, weeks_count = self.scoring_calculator.calculate_consistency(player)
                        player.consistency = consistency_val

                        # Update consistency statistics for logging
                        # Track how many players have sufficient data vs. defaults
                        min_weeks = self.config.consistency_scoring[self.config.keys.MIN_WEEKS]
                        if weeks_count >= min_weeks:
                            consistency_stats['sufficient_data'] += 1
                        else:
                            # Players with insufficient data get default consistency rating (MEDIUM)
                            consistency_stats['insufficient_data'] += 1
                            if weeks_count in consistency_stats['by_weeks']:
                                consistency_stats['by_weeks'][weeks_count] += 1

                        # Load team quality rankings for scoring calculations
                        # Offensive rank used for offensive players, defensive rank used for DST
                        player.team_offensive_rank = self.team_data_manager.get_team_offensive_rank(player.team)
                        player.team_defensive_rank = self.team_data_manager.get_team_defensive_rank(player.team)

                        # Calculate matchup score (favorable/unfavorable matchup this week)
                        # Uses position-specific defense rankings for more accurate matchup analysis
                        matchup_score = self.team_data_manager.get_rank_difference(player.team, player.position)
                        player.matchup_score = matchup_score

                        # Add validated player to the list
                        players.append(player)

                        # Track maximum projection across all players for normalization
                        # This is used as the denominator when calculating weighted projections
                        if player.fantasy_points and player.fantasy_points > self.max_projection:
                            self.max_projection = player.fantasy_points

                    except Exception as e:
                        error_count += 1
                        self.logger.error(f"Error parsing row {row_num} for player {row.get('name', 'Unknown')}: {e}")
                        continue

                # Log if any rows had parsing errors
                if error_count > 0:
                    self.logger.warning(f"Warning: {error_count} rows had errors and were skipped out of {row_count} total rows")

                # Update the scoring calculator with the final maximum projection
                # This is needed for normalization calculations in score_player()
                self.scoring_calculator.max_projection = self.max_projection

                # Log summary of consistency data quality
                # Helps identify if most players have sufficient historical data
                self.logger.debug(
                    f"Consistency calculation: {consistency_stats['sufficient_data']} players with sufficient data, "
                    f"{consistency_stats['insufficient_data']} players defaulted to MEDIUM "
                    f"({consistency_stats['by_weeks'][0]} with 0 weeks, "
                    f"{consistency_stats['by_weeks'][1]} with 1 week, "
                    f"{consistency_stats['by_weeks'][2]} with 2 weeks)"
                )
                        
        except FileNotFoundError:
            self.logger.error(f"Error: File {self.file_str} not found.")
            return []
        except PermissionError:
            self.logger.error(f"Error: Permission denied accessing file {self.file_str}")
            return []
        except csv.Error as e:
            self.logger.error(f"Error: Invalid CSV format in file {self.file_str}: {e}")
            return []
        except ValueError as e:
            self.logger.error(f"Error: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error loading CSV file {self.file_str}: {e}")
            return []
        
        # Add computed properties needed by scoring calculations
        for player in players:

            # Calculate weighted_projection (normalized between 0-N scale)
            # This creates a comparable metric across all players by normalizing to max_projection
            # Note: Actual scoring happens in PlayerScoringCalculator.score_player()
            if player.fantasy_points and self.max_projection > 0:
                player.weighted_projection = self.scoring_calculator.weight_projection(player.fantasy_points)
            else:
                # Handle edge case where player has no projection or max is zero
                player.weighted_projection = 0.0

            # Initialize draft helper specific properties if not already set
            # The is_starter flag is used by simulation to track starting lineup
            if not hasattr(player, 'is_starter'):
                player.is_starter = False  # Will be set to True when added to starting lineup

        # Calculate baseline scores for all players (now that max_projection is set)
        for player in players:
            player.score = self.score_player(player, 
                                             adp=False,
                                             player_rating=True,
                                             team_quality=True,
                                             performance=False,
                                             matchup=False,
                                             schedule=False,
                                             bye=False,
                                             injury=True
                                             ).score

        self.logger.debug(f"Loaded {len(players)} players from {self.file_str}.")

        self.players = players
    

    def load_team(self) -> None:
        """
        Load the current team roster from player data.

        Filters players where drafted=2 (drafted by user) and initializes
        the FantasyTeam with these rostered players. Players with drafted=1
        are drafted by opponents, drafted=0 are available.

        Side Effects:
            - Creates new FantasyTeam instance
            - Assigns players to roster slots based on position priority
        """
        drafted_players = [p for p in self.players if p.drafted == 2]
        self.logger.debug(f"Loading team roster with {len(drafted_players)} drafted players")
        self.team = FantasyTeam(self.config, drafted_players)
        # Go ahead and score the team
        for p in drafted_players:
            result = self.score_player(p, 
                                        adp=False,
                                        player_rating=True,
                                        team_quality=True,
                                        performance=True,
                                        matchup=False,
                                        schedule=True,
                                        bye=True,
                                        injury=True
                                        )
            self.team.set_score(p.id, result.score)
        # self.team.display_roster()

        self.logger.debug(f"Team loaded: {len(self.team.roster)} players on roster")

    def update_players_file(self) -> str:
        """
        Save current player data back to CSV file.

        Sorts players by drafted status (available → opponents → us) and writes
        all player data including weekly projections back to players.csv.

        Returns:
            str: Success message

        Side Effects:
            - Overwrites players.csv with current state
            - Preserves all columns including weekly projections
            - Sorts by drafted status for easier reading
        """
        self.logger.debug("Updating players CSV file")

        # Sort players by drafted value (ascending: 0=available, 1=drafted by others, 2=drafted by us)
        sorted_players = sorted(self.players, key=lambda p: p.drafted)

        # Use complete field list from player data fetcher to preserve all enhanced scoring columns
        fieldnames = [
            'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
            'injury_status', 'drafted', 'locked', 'average_draft_position',
            'player_rating',
            # Weekly projections (weeks 1-17 fantasy regular season only)
            'week_1_points', 'week_2_points', 'week_3_points', 'week_4_points',
            'week_5_points', 'week_6_points', 'week_7_points', 'week_8_points',
            'week_9_points', 'week_10_points', 'week_11_points', 'week_12_points',
            'week_13_points', 'week_14_points', 'week_15_points', 'week_16_points',
            'week_17_points'
        ]

        # Save sorted players to CSV
        with open(self.file_str, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in sorted_players:
                # Only include fields that are in fieldnames to avoid DictWriter errors
                player_dict = p.to_dict()
                filtered_dict = {key: player_dict.get(key, None) for key in fieldnames}
                writer.writerow(filtered_dict)
        self.logger.info(f"Available players saved with {len(self.players)} players (sorted by drafted status, all enhanced columns preserved)")
    

    def reload_player_data(self) -> None:
        """
        Reload player data from CSV file and refresh team roster
        This is called before each main menu display to ensure data is up-to-date
        """
        try:
            self.logger.info("Reloading player data from CSV file")

            # Store current roster size for comparison
            old_roster_size = len(self.team.roster)

            # Reload players from CSV
            self.load_players_from_csv()

            # Reload team with updated data
            self.load_team()

            # Log changes if any
            new_roster_size = len(self.team.roster)
            if old_roster_size != new_roster_size:
                self.logger.info(f"Roster size changed: {old_roster_size} -> {new_roster_size}")
                print(f"Player data reloaded. Roster updated: {old_roster_size} -> {new_roster_size} players")
            else:
                self.logger.debug(f"Player data reloaded. Roster size unchanged: {new_roster_size} players")

        except Exception as e:
            self.logger.error(f"Error reloading player data: {e}")
            print(f"Warning: Could not reload player data from {self.players_csv}: {e}")


    def get_roster_len(self) -> int:
        return len(self.team.roster)
    
    def can_draft(self, player: FantasyPlayer) -> bool:
        return self.team.can_draft(player)
    
    def draft_player(self, player_to_draft : FantasyPlayer) -> bool:
        return self.team.draft_player(player_to_draft)
    
    def get_player_list(self, drafted_vals : List[int] = [], can_draft : bool = False, min_scores : Dict[str,float] = {}, unlocked_only=False) -> List[FantasyPlayer]:
        """
        Get a filtered list of players based on multiple criteria.

        Args:
            drafted_vals: List of draft status values to include (0=available, 1=drafted by others, 2=on roster)
            can_draft: If True, only return players that can currently be drafted
            min_scores: Dictionary of minimum scores by position (e.g., {'QB': 50.0, 'RB': 45.0})
            unlocked_only: If True, only return players with locked=0 (not locked from being dropped)

        Returns:
            List[FantasyPlayer]: Filtered list of players meeting all criteria
        """
        # Define helper function to check locked status
        def is_unlocked(val: int) -> bool:
            if unlocked_only:
                return val == 0  # Only unlocked players (locked=0)
            return True  # All players if unlocked_only=False

        # Ensure all positions have a minimum score threshold (default to 0.0)
        for pos in Constants.ALL_POSITIONS:
            if pos not in min_scores:
                min_scores[pos] = 0.0

        # Filter players by drafted status, score threshold, and locked status
        player_list = [
            p for p in self.players
            if p.drafted in drafted_vals and p.score >= min_scores[p.position] and is_unlocked(p.locked)
        ]

        # Apply additional roster/position limit filtering if can_draft is True
        if can_draft:
            player_list = [
                p for p in player_list
                if self.can_draft(p)  # Check if player can fit on current roster
            ]

        return player_list
    

    def display_roster_by_draft_order(self) -> None:
        """Display current roster organized by assigned slots in draft order"""
        print(f"\nCurrent Roster by Position:")
        print("-" * 40)

        # Create a map from player ID to player object for quick lookup
        player_map = {player.id: player for player in self.team.roster}

        # Display each position based on slot assignments (not original position)
        for pos in self.config.max_positions.keys():
            max_count = self.config.max_positions[pos]

            # Get players assigned to this slot (using slot_assignments, not position filtering)
            assigned_player_ids = self.team.slot_assignments.get(pos, [])
            assigned_players = [player_map[pid] for pid in assigned_player_ids if pid in player_map]
            current_count = len(assigned_players)

            print(f"\n{pos} ({current_count}/{max_count}):")
            if assigned_players:
                # Sort by fantasy points (highest first) for display
                sorted_players = sorted(assigned_players, key=lambda p: p.fantasy_points, reverse=True)
                for i, player in enumerate(sorted_players, 1):
                    locked_indicator = " (LOCKED)" if getattr(player, 'locked', False) else ""
                    print(f"  {pos}{i}: {player.name} ({player.team}) - {player.fantasy_points:.1f} pts{locked_indicator}")
            else:
                print(f"  (No {pos} players)")

        print(f"\nTotal roster: {len(self.team.roster)}/{self.config.max_players} players")

    def display_roster(self) -> None:
        self.team.display_roster()

    def display_scored_roster(self) -> None:
        """
        Display scored roster players with their scoring details.

        Shows each rostered player with their score and the reasons
        contributing to that score. Recalculates scores with bye penalties
        enabled to show how roster conflicts affect each player's value.
        """
        if not self.team.roster:
            print("\nNo players on roster yet.")
            return

        print("\n" + "="*80)
        print("SCORED ROSTER PLAYERS")
        print("="*80)

        # Recalculate scores with bye penalties enabled for display
        scored_players = []
        for player in self.team.roster:
            scored_player = self.score_player(player, adp=False,
                                             player_rating=True,
                                             team_quality=True,
                                             performance=True,
                                             matchup=False,
                                             schedule=True,
                                             bye=True,
                                             injury=True)
            scored_players.append(scored_player)

        # Sort by score (highest first) for better readability
        scored_players.sort(key=lambda sp: sp.score, reverse=True)

        for scored_player in scored_players:
            print(str(scored_player))
            print()  # Add blank line between players

    def get_lowest_scores_on_roster(self) -> Dict[str, float]:
        lowest_scores = {
            Constants.QB: 9999,
            Constants.RB: 9999,
            Constants.WR: 9999,
            Constants.TE: 9999,
            Constants.K: 9999,
            Constants.DST: 9999,
        }
        for p in self.team.roster:
            if p.score < lowest_scores[p.position] and p.locked == 0:
                lowest_scores[p.position] = p.score
        return lowest_scores

    def get_weekly_projection(self, player: FantasyPlayer, week=0) -> Tuple[float, float]:
        """
        Get weekly projection for a specific player and week.

        Delegates to PlayerScoringCalculator.

        Args:
            player (FantasyPlayer): Player to get projection for
            week (int): NFL week number (1-17). If 0 or outside valid range, uses current_nfl_week

        Returns:
            Tuple[float, float]: (original_points, weighted_points)
        """
        return self.scoring_calculator.get_weekly_projection(player, week)

    def score_player(self, p: FantasyPlayer, use_weekly_projection=False, adp=False, player_rating=True, team_quality=True, performance=False, matchup=False, schedule=False, draft_round=-1, bye=True, injury=True, roster: Optional[List[FantasyPlayer]] = None) -> ScoredPlayer:
        """
        Calculate score for a player (10-step calculation).

        Delegates to PlayerScoringCalculator for all scoring logic.

        New Scoring System:
        1. Get normalized seasonal fantasy points (0-N scale)
        2. Apply ADP multiplier
        3. Apply Player Ranking multiplier
        4. Apply Team ranking multiplier
        5. Apply Performance multiplier (actual vs projected deviation)
        6. Apply Matchup multiplier (current week opponent)
        7. Apply Schedule multiplier (future opponents strength)
        8. Add DRAFT_ORDER bonus (round-based position priority)
        9. Subtract Bye Week penalty
        10. Subtract Injury penalty

        Args:
            p: FantasyPlayer to score
            use_weekly_projection: Use weekly projection instead of rest-of-season
            adp: Apply ADP multiplier
            player_rating: Apply player rating multiplier
            team_quality: Apply team quality multiplier
            performance: Apply performance multiplier (actual vs projected deviation)
            matchup: Apply matchup multiplier (current week opponent)
            schedule: Apply schedule strength multiplier (future opponents) - DEFAULT TRUE
            draft_round: Draft round for position bonus (-1 to disable)
            bye: Apply bye week penalty
            injury: Apply injury penalty
            roster: Optional custom roster to use for bye week calculations (defaults to self.team.roster)

        Returns:
            ScoredPlayer: Scored player object with final score and reasons
        """
        # Use empty roster if team hasn't been initialized yet (during load_players_from_csv)
        team_roster = self.team.roster if hasattr(self, 'team') and self.team else []
        return self.scoring_calculator.score_player(
            p, team_roster, use_weekly_projection, adp, player_rating,
            team_quality, performance, matchup, schedule, draft_round, bye, injury, roster
        )
