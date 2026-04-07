"""
Player Manager

Manages all player data, scoring calculations, and roster operations.
This is the core module responsible for loading player data from CSV,
calculating player scores using the 10-step scoring algorithm, and
managing draft operations.

Key responsibilities:
- Loading and parsing player data from players.csv
- Computing the 10-step scoring algorithm for player evaluation
- Managing the team roster through FantasyTeam
- Updating the CSV file with roster changes
- Displaying roster information

The 10-step scoring algorithm:
1. Normalization (based on fantasy_points projection)
2. ADP Multiplier (market wisdom adjustment)
3. Player Rating Multiplier (expert consensus)
4. Team Quality Multiplier (offensive/defensive strength)
5. Performance Multiplier (actual vs projected deviation)
6. Matchup Multiplier (opponent strength)
7. Schedule Multiplier (future opponent strength)
8. Draft Order Bonus (positional value by round)
9. Bye Week Penalty (same-position and different-position roster conflicts)
   - BASE_BYE_PENALTY applied per same-position overlap
   - DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY applied per different-position overlap
10. Injury Penalty (risk assessment)

Author: Kai Mizuno
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import statistics
import warnings

from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
from league_helper.util.FantasyTeam import FantasyTeam
from league_helper.util.GameDataManager import GameDataManager
import league_helper.constants as Constants
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from league_helper.util.player_scoring import PlayerScoringCalculator
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class PlayerManager:
    """
    Manages player data, scoring, and roster operations.

    This class is responsible for all player-related functionality including
    loading player data from CSV, calculating scores using the 10-step algorithm,
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
            - Initializes team rankings and matchup data for each player
            - Initializes the team roster with drafted players
            - Logs player loading statistics
        """
        self.logger = get_logger()

        self.config = config
        self.data_folder = data_folder
        self.team_data_manager = team_data_manager
        self.season_schedule_manager = season_schedule_manager

        self.game_data_manager = GameDataManager(data_folder, config.current_nfl_week)

        self.scoring_calculator = PlayerScoringCalculator(
            config,
            self,
            0.0,
            team_data_manager,
            season_schedule_manager,
            config.current_nfl_week,
            self.game_data_manager
        )

        self.file_str = str(data_folder / 'players.csv')
        self.logger.debug(f"Players CSV path: {self.file_str}")

        self.team: FantasyTeam
        self.players: List[FantasyPlayer] = []
        self.max_projection : int = 0
        self.max_weekly_projections: Dict[int, float] = {}

        self.load_players_from_json()
        self.load_team()
        self.logger.debug(f"Player Manager initialized with {len(self.players)} players, {len(self.team.roster)} on roster")


    def load_players_from_csv(self) -> None:
        """
        DEPRECATED: Use load_players_from_json() instead.

        This method loads player data from the old players.csv format.
        It is maintained for backward compatibility only.

        Deprecated: 2025-12-30
        Remove in: Next major version

        Legacy documentation:
        Load players from CSV file using the new FantasyPlayer class.
        This function supports the projection data format with fantasy_points
        and can fall back to the legacy format if needed.
        """
        warnings.warn(
            "load_players_from_csv() is deprecated. "
            "Use load_players_from_json() instead. "
            "CSV support will be removed in future version.",
            DeprecationWarning,
            stacklevel=2
        )

        players: list[FantasyPlayer] = []
        self.max_projection = 0.0
        self.max_weekly_projections = {}

        required_columns = ['id', 'name', 'team', 'position']


        try:
            with open(self.file_str, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                if not all(col in reader.fieldnames for col in required_columns):
                    missing_cols = [col for col in required_columns if col not in reader.fieldnames]
                    raise ValueError(f"Missing required columns in CSV: {missing_cols}")

                row_count = 0
                error_count = 0

                for row_num, row in enumerate(reader, start=2):
                    row_count += 1
                    try:
                        player = FantasyPlayer.from_dict(row)

                        if not player.name:
                            self.logger.warning(f"Warning: Empty player name on row {row_num}, skipping")
                            error_count += 1
                            continue

                        if player.position not in self.config.max_positions:
                            self.logger.warning(f"Warning: Invalid position '{player.position}' for player {player.name} on row {row_num}, skipping")
                            error_count += 1
                            continue

                        player.fantasy_points = player.get_rest_of_season_projection(self.config)

                        player.team_offensive_rank = self.team_data_manager.get_team_offensive_rank(player.team)

                        if player.position in Constants.DEFENSE_POSITIONS:
                            player.team_defensive_rank = self.team_data_manager.get_team_dst_fantasy_rank(player.team)
                        else:
                            player.team_defensive_rank = self.team_data_manager.get_team_defensive_rank(player.team)

                        matchup_score = self.team_data_manager.get_rank_difference(player.team, player.position)
                        player.matchup_score = matchup_score

                        players.append(player)

                        if player.fantasy_points and player.fantasy_points > self.max_projection:
                            self.max_projection = player.fantasy_points

                    except Exception as e:
                        error_count += 1
                        self.logger.error(f"Error parsing row {row_num} for player {row.get('name', 'Unknown')}: {e}")
                        continue

                if error_count > 0:
                    self.logger.warning(f"Warning: {error_count} rows had errors and were skipped out of {row_count} total rows")

                self.scoring_calculator.max_projection = self.max_projection

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
        
        for player in players:

            if player.fantasy_points and self.max_projection > 0:
                player.weighted_projection = self.scoring_calculator.weight_projection(player.fantasy_points)
            else:
                player.weighted_projection = 0.0

            if not hasattr(player, 'is_starter'):
                player.is_starter = False

        for player in players:
            player.score = self.score_player(player, 
                                             adp=False,
                                             player_rating=True,
                                             team_quality=True,
                                             performance=True,
                                             matchup=False,
                                             schedule=True,
                                             bye=False,
                                             injury=True
                                             ).score

        self.logger.debug(f"Loaded {len(players)} players from {self.file_str}.")

        self.players = players

    def load_players_from_json(self) -> bool:
        """
        Load all players from position-specific JSON files.

        Replaces load_players_from_csv() for JSON-based data loading.
        Loads players from player_data/ directory with 6 position files:
        qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json

        Returns:
            True if successful, False otherwise

        Raises:
            FileNotFoundError: If player_data directory doesn't exist
            json.JSONDecodeError: If JSON file is malformed

        Side Effects:
            - Sets self.players to combined list from all position files
            - Calculates self.max_projection from all players
            - Calls self.load_team() to initialize team roster

        Spec Reference: sub_feature_01_core_data_loading_spec.md lines 242-319
        """
        player_data_dir = self.data_folder / 'player_data'
        if not player_data_dir.exists():
            raise FileNotFoundError(
                f"Player data directory not found: {player_data_dir}\n"
                "Run run_player_fetcher.py to generate JSON files."
            )

        all_players = []
        position_files = [
            'qb_data.json', 'rb_data.json', 'wr_data.json',
            'te_data.json', 'k_data.json', 'dst_data.json'
        ]

        for position_file in position_files:
            filepath = player_data_dir / position_file

            if not filepath.exists():
                self.logger.warning(f"Position file not found: {position_file}")
                continue

            try:
                with open(filepath, 'r') as f:
                    json_data = json.load(f)

                position_key = position_file.replace('.json', '')
                players_array = json_data if isinstance(json_data, list) else json_data.get(position_key, [])

                for player_data in players_array:
                    try:
                        player = FantasyPlayer.from_json(player_data)
                        all_players.append(player)
                    except ValueError as e:
                        self.logger.warning(f"Skipping invalid player: {e}")
                        continue

                self.logger.debug(f"Loaded {len(players_array)} players from {position_file}")

            except json.JSONDecodeError as e:
                self.logger.error(f"Malformed JSON in {position_file}: {e}")
                raise

        self.players = all_players
        self.logger.debug(f"All position files loaded: {len(self.players)} total players across all positions")

        if self.players:
            self.max_projection = max(p.fantasy_points for p in self.players)

            if hasattr(self, 'scoring_calculator'):
                self.scoring_calculator.max_projection = self.max_projection

        self.load_team()

        return True

    def calculate_max_weekly_projection(self, week_num: int) -> float:
        """
        Calculate the maximum weekly projection for a given week across all players.

        Uses caching to avoid recalculating the same week multiple times.
        This is used for normalizing weekly projections in Starter Helper mode.

        Args:
            week_num (int): NFL week number (1-17)

        Returns:
            float: Maximum weekly projection for the given week (0.0 if no valid projections)
        """
        if week_num in self.max_weekly_projections:
            self.logger.debug(f"Week {week_num} max projection (cached): {self.max_weekly_projections[week_num]:.2f} pts")
            return self.max_weekly_projections[week_num]

        max_weekly = 0.0
        for player in self.players:
            weekly_points = player.get_single_weekly_projection(week_num, self.config)
            if weekly_points is not None and weekly_points > max_weekly:
                max_weekly = float(weekly_points)

        self.max_weekly_projections[week_num] = max_weekly

        self.logger.debug(f"Week {week_num} max projection (calculated): {max_weekly:.2f} pts")
        return max_weekly

    def load_team(self) -> None:
        """
        Load the current team roster from player data.

        Filters players on our roster (is_rostered()) and initializes
        the FantasyTeam with these rostered players. Players drafted by
        opponents and free agents are not included.

        Side Effects:
            - Creates new FantasyTeam instance
            - Assigns players to roster slots based on position priority
        """
        drafted_players = [p for p in self.players if p.is_rostered()]
        self.logger.debug(f"Loading team roster with {len(drafted_players)} drafted players")
        self.team = FantasyTeam(self.config, drafted_players)
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

        self.logger.debug(f"Team loaded: {len(self.team.roster)} players on roster")

    def update_players_file(self) -> str:
        """
        Update player JSON files with current drafted_by and locked status.

        This method selectively updates ONLY the drafted_by and locked fields
        in position-specific JSON files (qb_data.json, rb_data.json, etc.),
        preserving all other player data (projections, stats, etc.) from
        the player_data_fetcher.

        Uses atomic write pattern (temp file + rename).

        Returns:
            str: Success message

        Side Effects:
            - Updates 6 JSON files in player_data/ directory
            - Only modifies drafted_by and locked fields
            - Preserves all other fields (projections, stats)

        Raises:
            FileNotFoundError: If position JSON file missing (run run_player_fetcher.py)
            PermissionError: If cannot write to files
            json.JSONDecodeError: If JSON file corrupted

        Spec Reference: sub_feature_04_file_update_strategy_spec.md lines 154-178
        """
        self.logger.debug(f"Updating player JSON files: {len(self.players)} players across 6 position files")

        players_by_position = {}
        for player in self.players:
            if player.position is None or player.position not in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
                self.logger.warning(f"Skipping player {player.id} with invalid position: {player.position}")
                continue

            position_key = player.position
            if position_key not in players_by_position:
                players_by_position[position_key] = []
            players_by_position[position_key].append(player)

        player_data_dir = self.data_folder / 'player_data'
        positions = ['qb', 'rb', 'wr', 'te', 'k', 'dst']

        for position in positions:
            position_upper = position.upper()
            json_path = player_data_dir / f'{position}_data.json'

            if not json_path.exists():
                error_msg = (
                    f"{position}_data.json not found in player_data/ directory. "
                    f"Please run run_player_fetcher.py to create missing position files."
                )
                self.logger.error(error_msg)
                raise FileNotFoundError(error_msg)

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                position_key = f"{position}_data"
                players_array = json_data.get(position_key, [])

                position_players = players_by_position.get(position_upper, [])
                player_updates = {p.id: p for p in position_players}

                for player_dict in players_array:
                    player_id = player_dict.get('id')

                    if isinstance(player_id, str):
                        player_id = int(player_id)

                    if player_id in player_updates:
                        updated_player = player_updates[player_id]

                        if updated_player.drafted_by:
                            player_dict['drafted_by'] = updated_player.drafted_by
                        else:
                            if updated_player.is_free_agent():
                                player_dict['drafted_by'] = ""
                            elif updated_player.is_rostered():
                                player_dict['drafted_by'] = Constants.FANTASY_TEAM_NAME

                        player_dict['locked'] = updated_player.locked


                json_data_to_write = {position_key: players_array}
                tmp_path = json_path.with_suffix('.tmp')
                with open(tmp_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data_to_write, f, indent=2)

                tmp_path.replace(json_path)

                self.logger.debug(f"Updated {position}_data.json ({len(position_players)} players in memory)")

            except json.JSONDecodeError as e:
                error_msg = f"Malformed JSON in {json_path}: {e}"
                self.logger.error(error_msg)
                raise
            except PermissionError as e:
                error_msg = f"Permission denied writing to {json_path}: {e}"
                self.logger.error(error_msg)
                raise

        success_msg = f"Player data updated successfully (6 JSON files updated)"
        self.logger.info(success_msg)
        return success_msg
    

    def reload_player_data(self) -> None:
        """
        Reload player data from JSON files and refresh team roster
        This is called before each main menu display to ensure data is up-to-date
        """
        try:
            self.logger.info("Reloading player data from JSON files")

            old_roster_size = len(self.team.roster)

            self.load_players_from_json()

            self.load_team()

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

        Note: Maintains backward compatibility with int API.
        Internally uses helper methods (is_free_agent(), is_drafted_by_opponent(), is_rostered()).
        """
        def is_unlocked(val: int) -> bool:
            if unlocked_only:
                return val == 0
            return True

        def matches_drafted_status(player: FantasyPlayer, drafted_vals: List[int]) -> bool:
            if not drafted_vals:
                return True
            for val in drafted_vals:
                if val == 0 and player.is_free_agent():
                    return True
                elif val == 1 and player.is_drafted_by_opponent():
                    return True
                elif val == 2 and player.is_rostered():
                    return True
            return False

        for pos in Constants.ALL_POSITIONS:
            if pos not in min_scores:
                min_scores[pos] = 0.0

        player_list = [
            p for p in self.players
            if matches_drafted_status(p, drafted_vals) and p.score >= min_scores[p.position] and is_unlocked(p.locked)
        ]

        if can_draft:
            player_list = [
                p for p in player_list
                if self.can_draft(p)
                and p.fantasy_points and p.fantasy_points > 0
            ]

        return player_list
    

    def display_roster_by_draft_order(self) -> None:
        """Display current roster organized by assigned slots in draft order"""
        print(f"\nCurrent Roster by Position:")
        print("-" * 40)

        player_map = {player.id: player for player in self.team.roster}

        for pos in self.config.max_positions.keys():
            max_count = self.config.max_positions[pos]

            assigned_player_ids = self.team.slot_assignments.get(pos, [])
            assigned_players = [player_map[pid] for pid in assigned_player_ids if pid in player_map]
            current_count = len(assigned_players)

            print(f"\n{pos} ({current_count}/{max_count}):")
            if assigned_players:
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

        scored_players.sort(key=lambda sp: sp.score, reverse=True)

        for scored_player in scored_players:
            print(str(scored_player))
            print()

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
            if p.score < lowest_scores[p.position] and not p.is_locked():
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

    def get_projected_points(self, player: FantasyPlayer, week: int) -> Optional[float]:
        """
        Get original projected points for a specific player and week.

        This method accesses the pre-season projected points that were loaded
        from JSON player data files. These represent the original fantasy point
        projections before any actual games were played.

        Spec: sub_feature_05_projected_points_manager_consolidation_spec.md
              NEW-100, lines 61-71

        Args:
            player (FantasyPlayer): Player to get projected points for
            week (int): NFL week number (1-17)

        Returns:
            Optional[float]: Projected points for the week, or None if:
                - Week is a bye week (projection is 0.0)
                - Player's projected_points array is missing/empty
                - Projected points data is not available

        Raises:
            ValueError: If week is outside valid range (< 1 or > 17)

        Example:
            >>> projected = pm.get_projected_points(player, 5)
            >>> if projected is not None:
            ...     print(f"Week 5 projection: {projected} points")
        """
        if week < 1 or week > 17:
            raise ValueError(f"Week must be between 1-17, got {week}")

        if not player.projected_points or len(player.projected_points) < week:
            return None

        projected_value = player.projected_points[week - 1]

        if projected_value == 0.0:
            return None

        return float(projected_value)

    def get_projected_points_array(self, player: FantasyPlayer, start_week: int, end_week: int) -> List[Optional[float]]:
        """
        Get projected points for a range of weeks.

        Returns a list of projected points for weeks in the specified range (inclusive).
        Delegates to get_projected_points() for each week, so validation and error
        handling follow the same rules.

        Spec: sub_feature_05_projected_points_manager_consolidation_spec.md
              NEW-101, lines 49-53

        Args:
            player (FantasyPlayer): Player to get projected points for
            start_week (int): Starting week number (1-17, inclusive)
            end_week (int): Ending week number (1-17, inclusive)

        Returns:
            List[Optional[float]]: List of projected points for each week in range.
                Empty list if start_week > end_week or if range is invalid.
                Each element follows get_projected_points() behavior:
                - None for bye weeks (0.0 projections)
                - None for missing data
                - float value for valid projections

        Raises:
            ValueError: If any week in range is outside 1-17 (raised by get_projected_points())

        Example:
            >>> projections = pm.get_projected_points_array(player, 1, 4)
            >>> # Returns [25.5, None, 27.0, 24.3] for weeks 1-4
            >>> # (week 2 is bye week with 0.0 projection → None)
        """
        if start_week > end_week:
            return []

        result = []
        for week in range(start_week, end_week + 1):
            projected = self.get_projected_points(player, week)
            result.append(projected)

        return result

    def get_historical_projected_points(self, player: FantasyPlayer) -> List[Optional[float]]:
        """
        Get historical projected points (weeks 1 to current week - 1).

        Returns projected points for all weeks from the start of the season up to
        (but not including) the current NFL week. Used for calculating performance
        deviation based on historical data.

        Spec: sub_feature_05_projected_points_manager_consolidation_spec.md
              NEW-102, lines 54-60

        Args:
            player (FantasyPlayer): Player to get historical projections for

        Returns:
            List[Optional[float]]: List of projected points for weeks 1 to current_week-1.
                Empty list if current_nfl_week <= 1 (no historical weeks yet).
                Each element follows get_projected_points() behavior:
                - None for bye weeks
                - None for missing data
                - float value for valid projections

        Raises:
            ValueError: If any week is invalid (raised by get_projected_points())

        Example:
            >>> # If current_nfl_week is 5
            >>> historical = pm.get_historical_projected_points(player)
            >>> # Returns projections for weeks 1, 2, 3, 4
            >>> # (week 5 excluded since it's the current week)
        """
        current_week = self.config.current_nfl_week

        if current_week <= 1:
            return []

        return self.get_projected_points_array(player, 1, current_week - 1)

    def score_player(self, p: FantasyPlayer, use_weekly_projection=False, adp=False, player_rating=True, team_quality=True, performance=False, matchup=False, schedule=False, draft_round=-1, bye=True, injury=True, roster: Optional[List[FantasyPlayer]] = None, temperature=False, wind=False, location=False, *, is_draft_mode: bool = False, nfl_team_penalty=False) -> ScoredPlayer:
        """
        Calculate score for a player (14-step calculation).

        Delegates to PlayerScoringCalculator for all scoring logic.

        Scoring System:
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
        11. Apply Temperature bonus/penalty (game conditions)
        12. Apply Wind bonus/penalty (game conditions, QB/WR/K only)
        13. Apply Location bonus/penalty (home/away/international)
        14. Apply NFL Team Penalty (multiply score by penalty weight for specified teams)

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
            temperature: Apply temperature bonus/penalty (game conditions)
            wind: Apply wind bonus/penalty (game conditions, QB/WR/K only)
            location: Apply location bonus/penalty (home/away/international)
            is_draft_mode: Use draft normalization scale (163) instead of weekly scale.
                Set to True for Add to Roster Mode (draft decisions). Default False.
            nfl_team_penalty: Apply NFL team penalty multiplier (Add to Roster mode only).
                Default False.

        Returns:
            ScoredPlayer: Scored player object with final score and reasons
        """
        team_roster = self.team.roster if hasattr(self, 'team') and self.team else []
        return self.scoring_calculator.score_player(
            p, team_roster, use_weekly_projection, adp, player_rating,
            team_quality, performance, matchup, schedule, draft_round, bye, injury, roster,
            temperature, wind, location, is_draft_mode, nfl_team_penalty
        )

    def set_player_data(self, player_data: Dict[int, Dict[str, Any]]) -> None:
        """
        Update player data from pre-loaded week-specific cache.

        This method is used by simulation to load week-specific player data
        without re-reading CSV files. Updates player attributes from the provided
        data dictionary and recalculates derived values (max_projection, weighted_projection).

        Args:
            player_data (Dict[int, Dict[str, Any]]): Player data keyed by player ID.
                Each dict should match the CSV format with keys like 'fantasy_points',
                'projected_points', 'actual_points', etc.

        Side Effects:
            - Updates self.players with new data
            - Recalculates self.max_projection
            - Updates weighted_projection for each player
            - Updates scoring_calculator.max_projection
        """
        if not player_data:
            return

        self.logger.debug(f"Updating player data from cache ({len(player_data)} players)")

        new_max_projection = 0.0

        for player in self.players:
            if player.id in player_data:
                data = player_data[player.id]

                for week in range(1, 18):
                    week_key = f'week_{week}_points'
                    if week_key in data:
                        try:
                            value = float(data[week_key]) if data[week_key] else None
                            setattr(player, week_key, value)
                        except (ValueError, TypeError):
                            pass

                if 'fantasy_points' in data:
                    try:
                        player.fantasy_points = float(data['fantasy_points']) if data['fantasy_points'] else 0.0
                    except (ValueError, TypeError):
                        pass

                if 'injury_status' in data:
                    player.injury_status = str(data['injury_status'])

            if player.fantasy_points and player.fantasy_points > new_max_projection:
                new_max_projection = player.fantasy_points

        if new_max_projection > 0:
            self.max_projection = new_max_projection
            self.scoring_calculator.max_projection = new_max_projection

            for player in self.players:
                if player.fantasy_points and self.max_projection > 0:
                    player.weighted_projection = self.scoring_calculator.weight_projection(player.fantasy_points)

        self.logger.debug(f"Player data updated, max_projection={self.max_projection:.2f}")

    def get_players_by_team(self) -> Dict[str, List[FantasyPlayer]]:
        """
        Organize players by their fantasy team.

        Returns dict of {team_name: [player1, player2, ...]} for all drafted players.
        Players with empty drafted_by field are excluded (not drafted).

        Returns:
            Dict[str, List[FantasyPlayer]]: Dictionary mapping team names to player lists

        Example:
            >>> teams = player_manager.get_players_by_team()
            >>> teams
            {
                "Sea Sharp": [<FantasyPlayer: Mahomes>, <FantasyPlayer: Kelce>],
                "Team Alpha": [<FantasyPlayer: Allen>, <FantasyPlayer: Hill>]
            }

            >>> # Access specific team
            >>> my_roster = teams.get("Sea Sharp", [])
            >>>
            >>> # Iterate all teams
            >>> for team_name, roster in teams.items():
            >>>     print(f"{team_name}: {len(roster)} players")
        """
        if not self.players:
            self.logger.warning("No players loaded - cannot organize by team")
            return {}

        teams = {}
        for player in self.players:
            if player.drafted_by:
                if player.drafted_by not in teams:
                    teams[player.drafted_by] = []
                teams[player.drafted_by].append(player)
        return teams


