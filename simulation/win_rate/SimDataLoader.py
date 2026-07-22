import json
from pathlib import Path
from typing import Dict, Optional, Any

from simulation.win_rate.SimulatedLeague import SimulatedLeague, DRAFT_ROUNDS, load_week_player_data
from utils.LoggingManager import get_logger

MIN_VALID_PLAYERS = sum(SimulatedLeague.SELF_PLAY_TEAM_STRATEGIES.values()) * DRAFT_ROUNDS

# T73/R2: the complete season shape SimDataLoader requires — weeks 1..17 are simulated
# (WEEKS_PER_SEASON) and week_18 supplies week 17's actuals, so 18 folders are needed.
WEEKS_REQUIRED = 18


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

        T73/D2: additionally requires the COMPLETE weeks/week_01..week_18 tree. A season
        missing any week folder is refused (ERROR, is_valid stays False) rather than
        simulated with fabricated actuals; CombinationEvaluator then drops it from
        _season_cache, so season_count and games_per_evaluation stay exact.
        """
        week_01_folder = self.season_folder / "weeks" / "week_01"
        if not week_01_folder.is_dir():
            self.logger.warning(f"Season {self.season_folder.name}: week_01 folder missing — skipping")
            return

        # T73/D2: a season must carry the FULL week_01..week_18 tree. Weeks 1-17 supply the
        # projections and week_N+1 supplies week N's actuals, so a truncated tree (e.g. from
        # compile_historical_data.py --weeks N / --keep-partial) has no valid actuals for its
        # last simulated week. Refuse the whole season here rather than fabricating actuals;
        # CombinationEvaluator drops it from _season_cache and season_count stays exact.
        weeks_folder = self.season_folder / "weeks"
        missing_weeks = [
            f"week_{week_num:02d}"
            for week_num in range(1, WEEKS_REQUIRED + 1)
            if not (weeks_folder / f"week_{week_num:02d}").is_dir()
        ]
        if missing_weeks:
            self.logger.error(
                f"Season {self.season_folder.name}: incomplete week data — missing "
                f"{', '.join(missing_weeks)} under {weeks_folder}. "
                f"All {WEEKS_REQUIRED} week folders (week_01-week_{WEEKS_REQUIRED:02d}) are "
                f"required; week_N+1 supplies week N's actuals. Season skipped."
            )
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
            week_data = load_week_player_data(
                weeks_folder, week_num, self._parse_players_json, self.logger
            )
            if week_data is None:
                continue
            self.week_data_cache[week_num] = week_data

        self.logger.debug(f"Pre-loaded {len(self.week_data_cache)} weeks of player data")

    def _parse_players_json(
        self,
        week_folder: Path,
        week_num: int,
        week_num_for_actual: Optional[int] = None
    ) -> Dict[int, Dict[str, Any]]:
        """
        Parse the 6 position JSON files in a week folder into per-player datasets.

        Emits, per player id, the FULL 17-element ``projected_points`` and
        ``actual_points`` arrays from this folder (padded/truncated to 17), for direct
        in-place replacement by ``PlayerManager.set_player_data``. The per-folder week
        choice — week_N for projections, week_{N+1} for actuals — is made by the caller
        (``_preload_all_weeks``); the whole array passes through here, so ``week_num`` and
        ``week_num_for_actual`` are retained only for call-site/signature stability and are
        not used for indexing under this array-passthrough shape.

        NOTE: This method is kept BYTE-FOR-BYTE IDENTICAL between
        simulation/win_rate/SimulatedLeague.py and simulation/win_rate/SimDataLoader.py
        (guarded by test_parse_players_json_copies_byte_for_byte_identical). Any change
        here must be mirrored verbatim in the other copy.

        Args:
            week_folder (Path): Path to the week_NN folder containing the 6 JSON files.
            week_num (int): Retained for signature compatibility with the unchanged
                _preload_all_weeks call site; not used under the array-passthrough shape.
            week_num_for_actual (Optional[int]): Retained for signature compatibility;
                not used under the array-passthrough shape.

        Returns:
            Dict[int, Dict[str, Any]]: Player data keyed by player ID; each value carries
                full 17-element ``projected_points`` / ``actual_points`` lists plus
                id/name/position/drafted_by/locked metadata.
        """
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

                    projected_points = (list(projected_array) + [0.0] * 17)[:17]
                    actual_points = (list(actual_array) + [0.0] * 17)[:17]

                    players[player_id] = {
                        'id': str(player_id),
                        'name': player_dict.get('name', ''),
                        'position': player_dict.get('position', ''),
                        'drafted_by': player_dict.get('drafted_by', ''),
                        'locked': str(int(player_dict.get('locked', False))),
                        'projected_points': projected_points,
                        'actual_points': actual_points
                    }
                except (ValueError, KeyError, TypeError) as e:
                    self.logger.warning(f"Error parsing player in {position_file}: {e}")
                    continue

        return players
