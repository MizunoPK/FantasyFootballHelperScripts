import json
from pathlib import Path
from typing import Dict, Optional, Any

from simulation.win_rate.SimulatedLeague import SimulatedLeague, DRAFT_ROUNDS
from utils.LoggingManager import get_logger

MIN_VALID_PLAYERS = sum(SimulatedLeague.SELF_PLAY_TEAM_STRATEGIES.values()) * DRAFT_ROUNDS


class SimDataLoader:
    """
    Pre-loads all week player data for a single season folder once at startup.

    Extracts _preload_all_weeks() and _parse_players_json() from SimulatedLeague
    and _validate_season_data() from DraftStrategyOrchestrator, providing a
    single load point that eliminates per-simulation file reads.

    Attributes:
        season_folder (Path): Path to the season directory (e.g. simulation/sim_data/2023/)
        week_data_cache (Dict[int, Dict]): Pre-loaded week data keyed by week number.
            Structure: {week_num: {'projected': {player_id: dict}, 'actual': {player_id: dict}}}
        is_valid (bool): True if season data passed validation (MIN_VALID_PLAYERS check).
        logger: Logger instance
    """

    def __init__(self, season_folder: Path) -> None:
        """
        Initialize SimDataLoader for a single season folder.

        Validates season data first; if valid, pre-loads all weeks of player data
        into week_data_cache. Caller checks is_valid before using week_data_cache.

        Args:
            season_folder (Path): Path to the season directory (e.g. simulation/sim_data/2023/)
        """
        self.season_folder = season_folder
        self.week_data_cache: Dict[int, Dict] = {}
        self.is_valid: bool = False
        self.logger = get_logger()
        self._validate_season_data()
        if self.is_valid:
            self._preload_all_weeks()

    def _validate_season_data(self) -> None:
        """
        Validate that season_folder contains sufficient player data.

        Sets is_valid to True if week_01 contains at least MIN_VALID_PLAYERS
        undrafted players with positive projected_points across all position
        files combined. Malformed individual position files are skipped with a
        warning; validation succeeds based on the total count across valid files.
        Sets is_valid to False and logs a warning if the total falls below
        MIN_VALID_PLAYERS or if the week_01 folder is unreadable.
        """
        week_01_folder = self.season_folder / "weeks" / "week_01"
        if not week_01_folder.is_dir():
            self.logger.warning(f"Season {self.season_folder.name}: week_01 folder missing — skipping")
            return

        position_files = [
            "qb_data.json",
            "rb_data.json",
            "wr_data.json",
            "te_data.json",
            "k_data.json",
            "dst_data.json",
        ]

        try:
            valid_count = 0
            for position_file in position_files:
                json_file = week_01_folder / position_file
                if not json_file.exists():
                    self.logger.warning(
                        f"Season {self.season_folder.name}: Missing {position_file} in week_01"
                    )
                    continue

                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        position_key = position_file.removesuffix(".json")
                        players_array = data.get(position_key, [])
                        for player_dict in players_array:
                            drafted_by = player_dict.get("drafted_by", "")
                            projected_points = player_dict.get("projected_points", [])
                            fp_val = projected_points[0] if len(projected_points) > 0 else 0

                            if drafted_by == "" and fp_val > 0:
                                valid_count += 1
                except (json.JSONDecodeError, ValueError) as e:
                    self.logger.warning(
                        f"Season {self.season_folder.name}: Malformed JSON in {position_file}: {e}"
                    )
                    continue

            if valid_count < MIN_VALID_PLAYERS:
                self.logger.warning(
                    f"Season {self.season_folder.name}: only {valid_count} valid players "
                    f"(need {MIN_VALID_PLAYERS}+) — skipping"
                )
                return

            self.logger.debug(f"Season {self.season_folder.name}: {valid_count} valid players - OK")
            self.is_valid = True

        except Exception as e:
            self.logger.warning(
                f"Season {self.season_folder.name}: Error reading player data: {e}"
            )

    def _preload_all_weeks(self) -> None:
        """
        Pre-load all 17 weeks of player data into week_data_cache.

        Cache structure: {week_num: {'projected': {players}, 'actual': {players}}}

        Only loads data if historical structure (weeks/week_XX/) exists.
        Falls back gracefully if using legacy flat structure.
        """
        weeks_folder = self.season_folder / "weeks"

        if not weeks_folder.exists():
            self.logger.debug("No weeks/ folder found - using legacy flat structure")
            return

        self.logger.debug("Pre-loading all 17 weeks of player data (projected + actual)")

        for week_num in range(1, 18):
            projected_folder = weeks_folder / f"week_{week_num:02d}"

            actual_week_num = week_num + 1
            actual_folder = weeks_folder / f"week_{actual_week_num:02d}"

            if not projected_folder.exists():
                self.logger.warning(f"Week {week_num} projected folder not found at {projected_folder}")
                continue

            projected_data = self._parse_players_json(projected_folder, week_num)

            if actual_folder.exists():
                actual_data = self._parse_players_json(actual_folder, week_num, week_num_for_actual=week_num)
            else:
                self.logger.warning(
                    f"Week {actual_week_num} actual folder not found (needed for week {week_num} actuals). "
                    f"Using projected data as fallback."
                )
                actual_data = projected_data

            self.week_data_cache[week_num] = {
                'projected': projected_data,
                'actual': actual_data
            }

        self.logger.debug(f"Pre-loaded {len(self.week_data_cache)} weeks of player data")

    def _parse_players_json(
        self,
        week_folder: Path,
        week_num: int,
        week_num_for_actual: Optional[int] = None
    ) -> Dict[int, Dict[str, Any]]:
        """
        Parse 6 position JSON files and extract week-specific values from arrays.

        Args:
            week_folder (Path): Path to week_NN folder containing 6 JSON files
            week_num (int): Week number for projected_points indexing (1-17)
            week_num_for_actual (Optional[int]): Week number for actual_points indexing.
                                                  If None, uses week_num (backward compatible)

        Returns:
            Dict[int, Dict[str, Any]]: Player data keyed by player ID
        """
        actual_week = week_num_for_actual if week_num_for_actual is not None else week_num

        players = {}
        position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                         'te_data.json', 'k_data.json', 'dst_data.json']

        for position_file in position_files:
            json_file = week_folder / position_file
            if not json_file.exists():
                self.logger.warning(f"Missing {position_file} in {week_folder}")
                continue

            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, ValueError) as e:
                self.logger.error(f"Malformed JSON in {position_file}: {e}")
                continue

            position_key = position_file.removesuffix(".json")
            players_array = data.get(position_key, [])
            for player_dict in players_array:
                try:
                    player_id = int(player_dict['id'])

                    projected_array = player_dict.get('projected_points', [])
                    actual_array = player_dict.get('actual_points', [])

                    if len(projected_array) > week_num - 1:
                        projected = projected_array[week_num - 1]
                    else:
                        projected = 0.0

                    if len(actual_array) > actual_week - 1:
                        actual = actual_array[actual_week - 1]
                    else:
                        actual = 0.0

                    players[player_id] = {
                        'id': str(player_id),
                        'name': player_dict.get('name', ''),
                        'position': player_dict.get('position', ''),
                        'drafted_by': player_dict.get('drafted_by', ''),
                        'locked': str(int(player_dict.get('locked', False))),
                        'projected_points': str(projected),
                        'actual_points': str(actual)
                    }
                except (ValueError, KeyError, TypeError) as e:
                    self.logger.warning(f"Error parsing player in {position_file}: {e}")
                    continue

        return players
