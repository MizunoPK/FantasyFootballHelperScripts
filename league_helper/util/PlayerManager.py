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
8. Bye Week Penalty (roster conflicts)
9. Injury Penalty (risk assessment)

Author: Kai Mizuno
"""

import csv
from pathlib import Path
from typing import List, Tuple
import statistics

import sys
import logging
from util.TeamDataManager import TeamDataManager
from util.FantasyTeam import FantasyTeam

sys.path.append(str(Path(__file__).parent))
import constants as Constants
from ConfigManager import ConfigManager
from ScoredPlayer import ScoredPlayer

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
        file_str (str): Path to players.csv file
        team (FantasyTeam): Current fantasy team roster
        players (List[FantasyPlayer]): All available players
        max_projection (int): Maximum fantasy points projection (for normalization)

    Example:
        >>> player_manager = PlayerManager(data_folder, config, team_data_manager)
        >>> score = player_manager.score_player(player, draft_round=0)
        >>> can_add = player_manager.can_draft(player)
        >>> if can_add:
        ...     player_manager.draft_player(player)
        ...     player_manager.update_players_file()
    """

    def __init__(self, data_folder : Path, config : ConfigManager, team_data_manager : TeamDataManager):
        """
        Initialize the Player Manager.

        Args:
            data_folder (Path): Path to data directory containing players.csv
            config (ConfigManager): Configuration manager with scoring parameters
            team_data_manager (TeamDataManager): Manager for team rankings and matchups

        Side Effects:
            - Loads all players from players.csv
            - Calculates consistency scores for each player
            - Initializes the team roster with drafted players
            - Logs player loading statistics
        """
        self.logger = get_logger()
        self.logger.info("Initializing Player Manager")

        self.config = config
        self.team_data_manager = team_data_manager

        self.file_str = str(data_folder / 'players.csv')
        self.logger.debug(f"Players CSV path: {self.file_str}")

        self.team: FantasyTeam
        self.players: List[FantasyPlayer] = []
        self.max_projection : int = 0

        self.load_players_from_csv()
        self.load_team()
        self.logger.info(f"Player Manager initialized with {len(self.players)} players, {len(self.team.roster)} on roster")


    def load_players_from_csv(self):
        """
        Load players from CSV file using the new FantasyPlayer class.

        This function now supports the new projection data format with fantasy_points
        and can fall back to the legacy format if needed.
        """
        players: list[FantasyPlayer] = []
        self.max_projection = 0.0
        required_columns = ['id', 'name', 'team', 'position']

        # Track consistency data statistics
        consistency_stats = {
            'sufficient_data': 0,
            'insufficient_data': 0,
            'by_weeks': {0: 0, 1: 0, 2: 0}
        }

        try:
            with open(self.file_str, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # Validate required columns exist
                if not all(col in reader.fieldnames for col in required_columns):
                    missing_cols = [col for col in required_columns if col not in reader.fieldnames]
                    raise ValueError(f"Missing required columns in CSV: {missing_cols}")

                row_count = 0
                error_count = 0

                for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
                    row_count += 1
                    try:
                        # Use FantasyPlayer.from_dict for proper field handling including locked
                        player = FantasyPlayer.from_dict(row)

                        # Validate player data
                        if not player.name:
                            self.logger.warning(f"Warning: Empty player name on row {row_num}, skipping")
                            error_count += 1
                            continue

                        if player.position not in Constants.MAX_POSITIONS:
                            self.logger.warning(f"Warning: Invalid position '{player.position}' for player {player.name} on row {row_num}, skipping")
                            error_count += 1
                            continue

                        # Get the rest of season projected points
                        player.fantasy_points = player.get_rest_of_season_projection(self.config.current_nfl_week)

                        # Calculate the consistency value and track statistics
                        consistency_val, weeks_count = self._calculate_consistency(player)
                        player.consistency = consistency_val

                        # Update consistency statistics
                        min_weeks = self.config.consistency_scoring[self.config.keys.MIN_WEEKS]
                        if weeks_count >= min_weeks:
                            consistency_stats['sufficient_data'] += 1
                        else:
                            consistency_stats['insufficient_data'] += 1
                            if weeks_count in consistency_stats['by_weeks']:
                                consistency_stats['by_weeks'][weeks_count] += 1

                        # Set team quality ranks
                        player.team_offensive_rank = self.team_data_manager.get_team_offensive_rank(player.team)
                        player.team_defensive_rank = self.team_data_manager.get_team_defensive_rank(player.team)

                        # Calculate the matchup score
                        is_def = player.position in Constants.DEFENSE_POSITIONS
                        matchup_score = self.team_data_manager.get_rank_difference(player.team, is_def)
                        player.matchup_score = matchup_score

                        players.append(player)

                        # Track max projection for normalization
                        if player.fantasy_points and player.fantasy_points > self.max_projection:
                            self.max_projection = player.fantasy_points

                    except Exception as e:
                        error_count += 1
                        self.logger.error(f"Error parsing row {row_num} for player {row.get('name', 'Unknown')}: {e}")
                        continue

                if error_count > 0:
                    self.logger.warning(f"Warning: {error_count} rows had errors and were skipped out of {row_count} total rows")

                # Log consistency data summary
                self.logger.info(
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

            # Calculate weighted_projection (normalized between 0-100)
            # Note: This property is deprecated and not actively used - actual normalization
            # happens in NormalizationCalculator using param_manager values
            if player.fantasy_points and self.max_projection > 0:
                player.weighted_projection = self.weight_projection(player.fantasy_points)
            else:
                player.weighted_projection = 0.0

            # Initialize draft helper specific properties if not already set
            if not hasattr(player, 'is_starter'):
                player.is_starter = False  # To be set when added to FantasyTeam

        # Calculate baseline scores for all players (now that max_projection is set)
        for player in players:
            player.score = self.score_player(player, bye=False).score

        self.logger.info(f"Loaded {len(players)} players from {self.file_str}.")

        self.players = players
    

    def load_team(self):
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
            result = self.score_player(p)
            print(result)
            self.team.set_score(p.id, result.score)

        self.logger.info(f"Team loaded: {len(self.team.roster)} players on roster")

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
    

    def reload_player_data(self):
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
    
    def get_player_list(self, drafted_vals : List[int] = [], can_draft : bool = False, min_score : float = 0.0) -> List[FantasyPlayer]:
        player_list = [
            p for p in self.players
            if p.drafted in drafted_vals and p.score >= min_score
        ]
        if can_draft:
            drafted_players = [
                p for p in player_list
                if self.can_draft(p)
            ]
        return player_list
    

    def display_roster_by_draft_order(self):
        """Display current roster organized by assigned slots in draft order"""
        print(f"\nCurrent Roster by Position:")
        print("-" * 40)

        # Create a map from player ID to player object for quick lookup
        player_map = {player.id: player for player in self.team.roster}

        # Display each position based on slot assignments (not original position)
        for pos in Constants.MAX_POSITIONS.keys():
            max_count = Constants.MAX_POSITIONS[pos]

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

        print(f"\nTotal roster: {len(self.team.roster)}/{Constants.MAX_PLAYERS} players")

    def display_roster(self):
        self.team.display_roster()

    def get_lowest_score_on_roster(self):
        lowest_score = 0
        for p in self.team.roster:
            if p.score < lowest_score:
                lowest_score = p.score
        return lowest_score


    def get_weekly_projection(self, player : FantasyPlayer, week=0) -> Tuple[float, float]:
        """
        Get weekly projection for a specific player and week.

        This method retrieves the projected fantasy points for a player in a specific week
        and calculates the normalized/weighted projection using the same scale as seasonal
        projections (0-N scale based on normalization_max_scale).

        Args:
            player (FantasyPlayer): Player to get projection for
            week (int): NFL week number (1-17). If 0 or outside valid range, uses current_nfl_week

        Returns:
            Tuple[float, float]: (original_points, weighted_points)
                - original_points: Raw fantasy points projection for the week
                - weighted_points: Normalized projection (0-N scale) calculated as
                  (weekly_points / max_projection) * normalization_max_scale
                - Returns (0.0, 0.0) if no valid projection data exists

        Example:
            >>> orig_pts, weighted_pts = player_manager.get_weekly_projection(player, week=5)
            >>> print(f"Week 5 projection: {orig_pts:.1f} pts (normalized: {weighted_pts:.1f})")
        """
        # If week isn't in the valid range (1-17), use current week from config
        if week not in range(1, 18):
            week = self.config.current_nfl_week

        weekly_points = player.get_single_weekly_projection(week)
        if weekly_points is not None and float(weekly_points) > 0:
            weekly_points = float(weekly_points)
            # Calculate normalized/weighted projection using same scale as seasonal projections
            # This ensures weekly and seasonal scores are comparable
            if self.max_projection > 0:
                weighted_projection = self.weight_projection(weekly_points)
            else:
                weighted_projection = 0.0
            self.logger.debug(
                f"Week {week} projection for {player.name}: {weekly_points:.2f} pts "
                f"(weighted: {weighted_projection:.2f})"
            )
            return weekly_points, weighted_projection

        # Return zeros if no valid projection found
        self.logger.debug(
            f"No valid projection data for {player.name} in week {week}"
        )
        return 0.0, 0.0

    def weight_projection(self, pts) -> float:
        return (pts / self.max_projection) * self.config.normalization_max_scale

    def _calculate_consistency(self, player : FantasyPlayer) -> tuple[float, int]:
        """
        Calculate consistency score for a player based on weekly projections.
        Value equals the coefficient of variation

        Only uses weeks < CURRENT_NFL_WEEK (weeks that have already occurred).
        Requires minimum MIN_WEEKS weeks of data for reliable calculation.

        Args:
            player: FantasyPlayer object with weekly projection data

        Returns:
            tuple: (consistency_score, weeks_count)
                - consistency_score: the calculated values between 0 and 1 associated with how consistent a player's scores have been
                - weeks_count: number of weeks with data used in calculation
        """
        # Extract weekly scores for weeks that have occurred
        weekly_points = []

        # Only analyze weeks that have occurred (weeks < CURRENT_NFL_WEEK)
        for week in range(1, self.config.current_nfl_week):
            week_attr = f'week_{week}_points'
            if hasattr(player, week_attr):
                points = getattr(player, week_attr)
                # Filter out None values (missing data) and zeros
                # Zeros could be bye weeks, benched players, or data issues
                if points is not None and float(points) > 0:
                    weekly_points.append(float(points))

        weeks_count = len(weekly_points)

        # Handle insufficient data
        min_weeks = self.config.consistency_scoring[self.config.keys.MIN_WEEKS]
        if weeks_count < min_weeks:
            # Return default consistency score without logging individual warnings
            return 0.5, weeks_count

        # Calculate statistics
        mean_points = statistics.mean(weekly_points)

        # Handle zero mean (avoid division by zero)
        if mean_points == 0:
            return 0.5, weeks_count

        # Calculate standard deviation
        if len(weekly_points) == 1:
            std_dev = 0.0
        else:
            std_dev = statistics.stdev(weekly_points)

        # Calculate coefficient of variation
        cv = std_dev / mean_points if mean_points > 0 else 0.0

        self.logger.debug(
                f"Consistency for {player.name}: mean={mean_points:.2f}, "
                f"std_dev={std_dev:.2f}, CV={cv:.3f}"
            )

        return cv, weeks_count


    def score_player(self, p : FantasyPlayer, use_weekly_projection=False, adp=False, player_rating=True, team_quality=True, consistency=True, matchup=False, draft_round=-1, bye=True, injury=True) -> ScoredPlayer:
        """
        Calculate score for a player (8-step calculation).

        New Scoring System:
        1. Get normalized seasonal fantasy points (0-N scale)
        2. Apply ADP multiplier
        3. Apply Player Ranking multiplier
        4. Apply Team ranking multiplier
        5. Apply Consistency multiplier (CV-based volatility scoring)
        6. Apply Matchup multiplier
        7. Add DRAFT_ORDER bonus (round-based position priority)
        8. Subtract Bye Week penalty
        9. Subtract Injury penalty

        Returns:
            float: Total score for the player
        """
        reasons = []
        def add_to_reasons(r : str):
            if r is not None and r != "":
                reasons.append(r)

        # STEP 1: Normalize seasonal fantasy points to 0-N scale
        player_score, reason = self._get_normalized_fantasy_points(p, use_weekly_projection)
        add_to_reasons(reason)
        self.logger.debug(f"Step 1 - Normalized score for {p.name}: {player_score:.2f}")

        # STEP 2: Apply ADP multiplier
        if (adp):
            player_score, reason = self._apply_adp_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 2 - ADP Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 3: Apply Player Rating multiplier
        if (player_rating):
            player_score, reason = self._apply_player_rating_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 3 - Player Rating Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 4: Apply Team Quality multiplier
        if (team_quality):
            player_score, reason = self._apply_team_quality_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 4 - Team Quality Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 5: Apply Consistency multiplier (CV-based volatility scoring)
        if (consistency):
            player_score, reason = self._apply_consistency_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 5 - After consistency for {p.name}: {player_score:.2f}")

        # STEP 6: Apply Matchup multiplier
        if (matchup):
            player_score, reason = self._apply_matchup_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 6 - After matchup multiplier for {p.name}: {player_score:.2f}")

        # STEP 7: Add DRAFT_ORDER bonus (round-based position priority)
        # BUG FIX: Changed from draft_round > 0 to draft_round >= 0
        # This allows round 0 (first round) to get bonuses, -1 is the disabled flag
        if (draft_round >= 0):
            player_score, reason = self._apply_draft_order_bonus(p, draft_round, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 7 - After DRAFT_ORDER bonus for {p.name}: {player_score:.2f}")

        # STEP 8: Subtract Bye Week penalty
        if (bye):
            player_score, reason = self._apply_bye_week_penalty(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 8 - After bye penalty for {p.name}: {player_score:.2f}")

        # STEP 9: Subtract Injury penalty
        if (injury):
            player_score, reason = self._apply_injury_penalty(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 9 - Final score for {p.name}: {player_score:.2f}")

        # Summary logging
        self.logger.info(
            f"Scoring for {p.name}: final_score={player_score:.1f}"
        )

        p.score = player_score
        return ScoredPlayer(p, player_score, reasons)
    
    def _get_normalized_fantasy_points(self, p : FantasyPlayer, use_weekly_projection : bool) -> Tuple[float, str]:
        if use_weekly_projection:
            orig_pts, weighted_pts = self.get_weekly_projection(p)
        else:
            orig_pts = p.get_rest_of_season_projection(self.config.current_nfl_week)
            weighted_pts = self.weight_projection(orig_pts)

        reason = f"Projected: {orig_pts:.2f} pts, Weighted: {weighted_pts:.2f} pts"
        return weighted_pts, reason
    
    def _apply_adp_multiplier(self, p : FantasyPlayer, player_score : float) -> Tuple[float, str]:
        """Calculate ADP-based market wisdom adjustment multiplier."""
        multiplier, rating = self.config.get_adp_multiplier(p.adp)
        reason = f"ADP: {rating}"
        return player_score * multiplier, reason
    
    def _apply_player_rating_multiplier(self, p : FantasyPlayer, player_score : float) -> Tuple[float, str]:
        multiplier, rating = self.config.get_player_rating_multiplier(p.player_rating)
        reason = f"Player Rating: {rating}"
        return player_score * multiplier, reason
    
    def _apply_team_quality_multiplier(self, p : FantasyPlayer, player_score : float) -> Tuple[float, str]:
        quality_val = p.team_offensive_rank
        if p.position in Constants.DEFENSE_POSITIONS:
            quality_val = p.team_defensive_rank
        multiplier, rating = self.config.get_team_quality_multiplier(quality_val)
        reason = f"Team Quality: {rating}"
        return player_score * multiplier, reason
    
    def _apply_consistency_multiplier(self, p : FantasyPlayer, player_score : float) -> Tuple[float, str]:
        multiplier, rating = self.config.get_consistency_multiplier(p.consistency)
        reason = f"Consistency: {rating}"
        return player_score * multiplier, reason
    
    def _apply_matchup_multiplier(self, p : FantasyPlayer, player_score : float) -> Tuple[float, str]:
        multiplier = 1.0
        rating = "NEUTRAL"
        if p.position in Constants.MATCHUP_ENABLED_POSITIONS:
            multiplier, rating = self.config.get_matchup_multiplier(p.matchup_score)
        reason = f"Matchup: {rating}"
        return player_score * multiplier, reason
    
    def _apply_draft_order_bonus(self, p : FantasyPlayer, draft_round : int, player_score : float) -> Tuple[float, str]:
        bonus, bonus_type = self.config.get_draft_order_bonus(p.position, draft_round)
        reason = ""
        if bonus_type != "":
            reason = f"Draft Order Bonus: {bonus_type}"
        return player_score + bonus, reason
    
    def _apply_bye_week_penalty(self, p : FantasyPlayer, player_score : float) -> Tuple[float, str]:
        num_matching_byes = self.team.get_matching_byes_in_roster(p.bye_week, p.position, p.is_rostered())
        penalty = self.config.get_bye_week_penalty(num_matching_byes)
        reason = "" if num_matching_byes == 0 else f"Number of Matching Bye Weeks: {num_matching_byes}"
        return player_score - penalty, reason

    def _apply_injury_penalty(self, p : FantasyPlayer, player_score : float) -> Tuple[float, str]:
        penalty = self.config.get_injury_penalty(p.get_risk_level())
        reason = "" if p.injury_status == "ACTIVE" else f"Injury: {p.injury_status}"
        return player_score - penalty, reason
