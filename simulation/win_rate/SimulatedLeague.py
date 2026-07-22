"""
Simulated League

Orchestrates a complete fantasy football league simulation including draft
and 17-week season. Manages 10 teams through the entire process — by default a
self-play field of 10 DraftHelperTeams, or (naive_opponents=True) the legacy field
of 1 DraftHelperTeam + 9 SimulatedOpponents.

The simulation process:
1. Initialize teams with separate PlayerManager instances
2. Run snake draft (15 rounds, 150 total picks)
3. Run 17-week regular season with round-robin matchups
4. Track results and determine final standings

Author: Kai Mizuno
"""

import random
import shutil
import tempfile
import json
from pathlib import Path
from typing import Callable, List, Dict, Tuple, Optional, Any

from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
from simulation.win_rate.DraftHelperTeam import DraftHelperTeam
from simulation.win_rate.SimulatedOpponent import SimulatedOpponent
from simulation.win_rate.Week import Week
from simulation.utils.scheduler import generate_schedule_for_nfl_season
from utils.LoggingManager import get_logger

DRAFT_ROUNDS = 15

# T61/D7: the fixed regular-season length every SimulatedLeague plays, defined once here (next
# to DRAFT_ROUNDS, the module's existing exported constant) rather than as a magic literal.
# _generate_schedule below passes it to generate_schedule_for_nfl_season, and the win-rate sweep
# driver's games-per-evaluation pre-flight (WEEKS_PER_SEASON x --sims x valid seasons) reads the
# SAME number, so the two can never silently diverge.
WEEKS_PER_SEASON = 17


def load_week_player_data(
    weeks_folder: Path,
    week_num: int,
    parse_players_json: Callable[..., Dict[int, Dict[str, Any]]],
    logger: Any,
) -> Optional[Dict[str, Dict[int, Dict[str, Any]]]]:
    """
    Resolve and parse one simulated week's projected + actual player datasets.

    T73/D4: this is the SINGLE implementation of the per-week resolve-and-parse block.
    Both SimDataLoader._preload_all_weeks and SimulatedLeague._preload_all_weeks call it,
    so the two loaders cannot drift on the week_N -> week_N+1 offset or on the
    missing-actuals disposition (guarded by
    TestPreloadCopiesShareOneImplementation in tests/simulation/test_SimulatedLeague_pointintime.py).

    Week N's projections live in the week_N folder; week N's RESULTS are only known in
    the week_N+1 snapshot, hence the offset.

    Args:
        weeks_folder (Path): The season's weeks/ directory.
        week_num (int): The simulated week (1..17).
        parse_players_json (Callable): The caller's _parse_players_json bound method.
        logger: Logger instance used for the missing-projected-folder warning.

    Returns:
        Optional[Dict]: {'projected': {...}, 'actual': {...}} for this week, or None when
            the week_N projected folder is absent (the caller skips the week).

    Raises:
        FileNotFoundError: If the week_N+1 folder needed for week N's actuals is absent.
            T73/D3: this path previously substituted the projected dataset for the missing
            actuals, which yields all-zero actual_points and charges every team a loss.
            The NET effect on a measured win rate is UNMEASURED — do not infer a direction
            from the per-week loss. A T73 Phase-4 run with the fallback firing came out
            HIGHER (0.529) than the same run on complete data (0.500), which is why the
            story treats the corruption as direction-unknown. What is established is that
            the reported number moves; the sign is an open question.
    """
    projected_folder = weeks_folder / f"week_{week_num:02d}"

    actual_week_num = week_num + 1
    actual_folder = weeks_folder / f"week_{actual_week_num:02d}"

    if not projected_folder.exists():
        logger.warning(f"Week {week_num} projected folder not found at {projected_folder}")
        return None

    projected_data = parse_players_json(projected_folder, week_num)

    if not actual_folder.exists():
        raise FileNotFoundError(
            f"Week {actual_week_num} actual folder not found at {actual_folder} "
            f"(needed for week {week_num} actuals). Recompile this season with all 18 "
            f"week folders; projected data is NOT a valid substitute for actuals."
        )

    actual_data = parse_players_json(actual_folder, week_num, week_num_for_actual=week_num)

    return {
        'projected': projected_data,
        'actual': actual_data
    }


class SimulatedLeague:
    """
    Complete fantasy football league simulation.

    Manages 10 teams through draft and 17-week season, tracking results
    and determining final standings.

    Team Distribution:
    - Self-play (default): 10 DraftHelperTeams sharing the reference config; one is
      designated the measured/reported team, the rest are self-play opponents.
    - Naive (naive_opponents=True): 1 DraftHelperTeam + 9 SimulatedOpponents
      (2 adp_aggressive, 2 projected_points_aggressive, 2 adp_with_draft_order,
      3 projected_points_with_draft_order).

    Attributes:
        config_dict (dict): League configuration dictionary
        data_folder (Path): Path to sim_data folder
        teams (List): All 10 teams in the league
        draft_helper_team (DraftHelperTeam): The DraftHelperTeam being tested
        draft_order (List): Randomized draft order for snake draft
        season_schedule (List[List[Tuple]]): Week-by-week matchups
        week_results (List[Week]): Results for each simulated week
        logger: Logger instance
    """

    SELF_PLAY_TEAM_STRATEGIES = {
        'draft_helper': 10
    }
    """Self-play composition (the DEFAULT): 10 DraftHelperTeams sharing the reference config, no SimulatedOpponents. dict values sum to 10 total teams per league. With identical configs the only asymmetry between teams is the randomized snake-draft order, so the measured team's baseline win rate sits near ~0.50 — giving config differences headroom to register. _initialize_teams designates one DraftHelperTeam as the measured (reported) team; the rest are self-play opponents."""

    NAIVE_TEAM_STRATEGIES = {
        'draft_helper': 1,
        'adp_aggressive': 2,
        'projected_points_aggressive': 2,
        'adp_with_draft_order': 2,
        'projected_points_with_draft_order': 3
    }
    """Legacy naive-opponent composition (selected when naive_opponents=True): 1 DraftHelperTeam + 9 SimulatedOpponents. dict values sum to 9 opponents + 1 DraftHelperTeam = 10 total teams per league. The 1/2/2/2/3 distribution reflects the relative prevalence of each strategy among typical human fantasy drafters. Retained verbatim so the prior ~0.84 baseline regime stays reproducible (T24)."""

    def __init__(self, config_dict: dict, data_folder: Path = Path("./simulation/sim_data"), preloaded_week_data: Optional[Dict[int, Dict]] = None, measured_config_dict: Optional[dict] = None, naive_opponents: bool = False, seed: Optional[int] = None) -> None:
        """
        Initialize SimulatedLeague with configuration.

        Args:
            config_dict (dict): Configuration dictionary (will be saved as temp JSON)
            data_folder (Path): Path to folder containing weeks/ subfolder with
                               week-specific JSON player data and teams_week_N.csv files
            preloaded_week_data (Optional[Dict[int, Dict]]): Pre-loaded week data from SimDataLoader. If provided, skips internal _preload_all_weeks() file reads.
            measured_config_dict (Optional[dict]): When provided, the single measured
                DraftHelperTeam (the one reported by get_draft_helper_results) is built with
                THIS config while every other team — including any additional self-play
                DraftHelperTeam opponents — uses config_dict. Because draft scoring runs through
                each team's own PlayerManager (AddToRosterModeManager -> player_manager.score_player),
                the measured team's PlayerManagers are built with this config too, so its draft-side
                params differ from the opponents'. Default None preserves the legacy single-config
                behavior (the last draft_helper team is the measured one and shares config_dict).
            naive_opponents (bool): When False (default) the opponent composition is self-play
                (SELF_PLAY_TEAM_STRATEGIES — 10 DraftHelperTeams, no SimulatedOpponents). When True
                the legacy naive composition (NAIVE_TEAM_STRATEGIES — 1 DraftHelperTeam + 9
                SimulatedOpponents) is used, reproducing the prior ~0.84 baseline regime (T24).
            seed (Optional[int]): Base seed for this league's private RNG (random.Random). When
                provided, every random draw in this league (team-slot shuffle, draft-order shuffle,
                opponent human-error picks) is deterministic and isolated from other leagues and
                from the process-global random module. Default None seeds from OS entropy,
                preserving today's stochastic behavior (D3/T29).

        Raises:
            FileNotFoundError: If data files are missing.
            ValueError: If measured_config_dict is provided but the team composition
                contains no 'draft_helper' team to apply it to (D2), or if the measured
                config is malformed/invalid (D3, re-raised from ConfigManager; a malformed
                measured config may alternatively surface as FileNotFoundError).
        """
        self.logger = get_logger()

        self.config_dict = config_dict
        self.measured_config_dict = measured_config_dict
        self.naive_opponents = naive_opponents
        self.data_folder = data_folder
        # Per-league private RNG (D1/T29): seeded deterministically when seed is provided so
        # every draw is isolated from the process-global random module and from other leagues.
        # seed=None falls back to OS entropy, preserving the original stochastic behavior (D3).
        self._rng = random.Random(seed)

        self.temp_dir = Path(tempfile.mkdtemp(prefix="sim_league_"))

        self.config_path = self.temp_dir / "league_config.json"
        with open(self.config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)

        self.teams: List = []
        self.draft_helper_team: Optional[DraftHelperTeam] = None
        self.draft_order: List = []
        self.season_schedule: List[List[Tuple]] = []
        self.week_results: List[Week] = []

        self.week_data_cache: Dict[int, Dict] = {}

        if preloaded_week_data is not None:
            self.week_data_cache = preloaded_week_data

        self._preload_all_weeks()

        self._initialize_teams()

        self._generate_schedule()

    def _initialize_teams(self) -> None:
        """
        Initialize all 10 teams with separate PlayerManager instances.

        Creates either:
        - self-play (default): 10 DraftHelperTeams (one designated the measured/reported team), or
        - naive (naive_opponents=True): 1 DraftHelperTeam + 9 SimulatedOpponents with strategy distribution

        OPTIMIZATION: Uses shared read-only directories instead of per-team copies.
        Each team gets its own PlayerManager instance (with independent in-memory state)
        but all teams share the same underlying data files.

        Note:
            Each team needs independent PlayerManager instances to track
            their own roster (drafted=2) vs opponents' rosters (drafted=1).
            This works because PlayerManager loads data into memory and modifications
            are made to in-memory objects, not written back to files during simulation.
        """
        self.logger.debug("Initializing 10 teams with shared data directories (optimized)")

        composition = self.NAIVE_TEAM_STRATEGIES if self.naive_opponents else self.SELF_PLAY_TEAM_STRATEGIES
        strategies = []
        for strategy, count in composition.items():
            strategies.extend([strategy] * count)

        self._rng.shuffle(strategies)  # site #1 (T29): team-slot assignment via per-league RNG

        weeks_folder = self.data_folder / "weeks"
        available_weeks = sorted([f for f in weeks_folder.iterdir() if f.is_dir() and f.name.startswith("week_")])
        if not available_weeks:
            raise FileNotFoundError(f"No week folders found in: {weeks_folder}")

        week_folder = available_weeks[-1]
        self.logger.debug(f"Using {week_folder.name} JSON files for team setup (has complete actual_points data)")

        shared_dir = self._create_shared_data_dir("shared_data", week_folder)

        shared_config = ConfigManager(shared_dir)

        shared_schedule_mgr = SeasonScheduleManager(shared_dir)

        shared_team_data_mgr = TeamDataManager(
            shared_dir, shared_config, shared_schedule_mgr, shared_config.current_nfl_week
        )

        measured_config = None
        if self.measured_config_dict is not None:
            if strategies.count('draft_helper') == 0:
                raise ValueError(
                    "SimulatedLeague._initialize_teams: measured_config_dict was provided but the "
                    "team composition contains no 'draft_helper' team to apply it to. This indicates "
                    "a wiring bug in the league composition (NAIVE_TEAM_STRATEGIES / SELF_PLAY_TEAM_STRATEGIES)."
                )
            try:
                measured_config = self._build_measured_config(self.measured_config_dict)
            except (ValueError, FileNotFoundError) as e:
                self.logger.error(
                    f"SimulatedLeague._initialize_teams: failed to build the measured team's "
                    f"ConfigManager from measured_config_dict: {e}",
                    exc_info=True,
                )
                raise

        measured_assigned = False
        for idx, strategy in enumerate(strategies):
            if strategy == 'draft_helper' and measured_config is not None and not measured_assigned:
                # The single measured DraftHelperTeam scores with its own config: its
                # PlayerManagers (whose scoring_calculator carries the draft-side params) are
                # built from measured_config, not shared_config.
                projected_pm = PlayerManager(shared_dir, measured_config, shared_team_data_mgr, shared_schedule_mgr)
                actual_pm = PlayerManager(shared_dir, measured_config, shared_team_data_mgr, shared_schedule_mgr)
                team = DraftHelperTeam(projected_pm, actual_pm, measured_config, shared_team_data_mgr)
                self.draft_helper_team = team
                measured_assigned = True
            elif strategy == 'draft_helper':
                projected_pm = PlayerManager(shared_dir, shared_config, shared_team_data_mgr, shared_schedule_mgr)
                actual_pm = PlayerManager(shared_dir, shared_config, shared_team_data_mgr, shared_schedule_mgr)
                team = DraftHelperTeam(projected_pm, actual_pm, shared_config, shared_team_data_mgr)
                if measured_config is None:
                    # Legacy single-config path: the last draft_helper is the measured team.
                    self.draft_helper_team = team
            else:
                projected_pm = PlayerManager(shared_dir, shared_config, shared_team_data_mgr, shared_schedule_mgr)
                actual_pm = PlayerManager(shared_dir, shared_config, shared_team_data_mgr, shared_schedule_mgr)
                team = SimulatedOpponent(projected_pm, actual_pm, shared_config, shared_team_data_mgr, strategy, rng=self._rng)

            self.teams.append(team)

        self.logger.debug(f"Initialized {len(self.teams)} teams (using shared data directory)")

    def _build_measured_config(self, config_dict: dict) -> ConfigManager:
        """
        Build a standalone ConfigManager for the measured team from config_dict.

        Writes config_dict as league_config.json into a dedicated temp subdir and loads it via
        ConfigManager (legacy single-file layout, same as the shared config). Only the config is
        needed here — player data, schedule, and team data are shared with the rest of the league.

        Args:
            config_dict (dict): The measured team's configuration dictionary.

        Returns:
            ConfigManager: Config manager scoped to the measured team.
        """
        measured_dir = self.temp_dir / "measured_config_data"
        measured_dir.mkdir(exist_ok=True)
        with open(measured_dir / "league_config.json", 'w') as f:
            json.dump(config_dict, f, indent=2)
        return ConfigManager(measured_dir)

    def _create_shared_data_dir(self, dir_name: str, week_folder: Path) -> Path:
        """
        Create a shared data directory with all required files (JSON format).

        This is called ONCE per simulation to create a shared directory that all teams
        can read from. This optimization reduces file I/O from ~60 copies per simulation
        to just 1 directory.

        Args:
            dir_name (str): Name for the shared directory (e.g., "shared_data")
            week_folder (Path): Path to week folder containing 6 JSON files

        Returns:
            Path: Path to the created shared directory
        """
        shared_dir = self.temp_dir / dir_name
        shared_dir.mkdir()

        player_data_dir = shared_dir / 'player_data'
        player_data_dir.mkdir()

        position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                         'te_data.json', 'k_data.json', 'dst_data.json']
        for position_file in position_files:
            src = week_folder / position_file
            dst = player_data_dir / position_file
            if src.exists():
                shutil.copy(src, dst)
            else:
                self.logger.warning(f"Missing {position_file} in {week_folder}")

        shutil.copy(self.config_path, shared_dir / "league_config.json")

        if (self.data_folder / "season_schedule.csv").exists():
            shutil.copy(self.data_folder / "season_schedule.csv", shared_dir / "season_schedule.csv")

        if (self.data_folder / "game_data.csv").exists():
            shutil.copy(self.data_folder / "game_data.csv", shared_dir / "game_data.csv")

        team_data_source = self.data_folder / "team_data"
        if team_data_source.exists():
            shutil.copytree(team_data_source, shared_dir / "team_data")
        else:
            self.logger.warning(f"team_data folder not found: {team_data_source}")

        return shared_dir

    def _generate_schedule(self) -> None:
        """
        Generate 17-week round-robin schedule.

        Uses generate_schedule_for_nfl_season to create matchups where each
        team plays each other team twice (as close as possible in 17 weeks).
        """
        self.logger.debug("Generating 17-week round-robin schedule")
        self.season_schedule = generate_schedule_for_nfl_season(self.teams, num_weeks=WEEKS_PER_SEASON)
        self.logger.debug(f"Generated schedule: {len(self.season_schedule)} weeks")

    def _preload_all_weeks(self) -> None:
        """
        Pre-load all 17 weeks of player data into memory cache.

        For Win Rate simulation accuracy, we need TWO datasets per week:
        - week_N folder: Contains projected_points for week N
        - week_N+1 folder: Contains actual_points for week N

        This is because week_N folder represents data "as of" week N's start,
        so week N's actual results aren't known until week_N+1.

        This optimization reduces disk I/O from 340 reads (17 weeks × 10 teams × 2 files)
        to just 34 reads per simulation (2 per week except week 17).

        Cache structure: {week_num: {'projected': {players}, 'actual': {players}}}

        Only loads data if historical structure (weeks/week_XX/) exists.
        Falls back gracefully if using legacy flat structure.
        """
        if self.week_data_cache:
            return

        weeks_folder = self.data_folder / "weeks"

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

    def _load_week_data(self, week_num: int) -> None:
        """
        Load week-specific player data from pre-loaded cache.

        Updates all teams' PlayerManagers with the week's data. For accuracy,
        we load DIFFERENT data for projected_pm vs actual_pm:
        - projected_pm: Gets data from week_N folder (projections for week N)
        - actual_pm: Gets data from week_N+1 folder (actuals for week N)

        This is because week_N folder has actual_points[N-1] = 0.0 (week not complete),
        but week_N+1 folder has actual_points[N-1] = real value (week now complete).

        This is called at the start of each week during run_season().

        Args:
            week_num (int): Week number (1-17)

        Note:
            Does nothing if week data was not pre-loaded (legacy mode).
        """
        if week_num not in self.week_data_cache:
            return

        week_data = self.week_data_cache[week_num]

        if isinstance(week_data, dict) and 'projected' in week_data and 'actual' in week_data:
            projected_data = week_data['projected']
            actual_data = week_data['actual']
        else:
            projected_data = week_data
            actual_data = week_data

        for team in self.teams:
            if hasattr(team, 'projected_pm') and hasattr(team.projected_pm, 'set_player_data'):
                team.projected_pm.set_player_data(projected_data)
            if hasattr(team, 'actual_pm') and hasattr(team.actual_pm, 'set_player_data'):
                team.actual_pm.set_player_data(actual_data)


    def run_draft(self) -> None:
        """
        Run snake draft for all 10 teams.

        Draft process:
        1. Set all teams to week 1 (draft occurs before season, no performance history)
        2. Randomize initial draft order
        3. Run 15 rounds (150 total picks)
        4. Snake order: Round 1 (1→10), Round 2 (10→1), Round 3 (1→10), etc.
        5. After each pick, broadcast to all teams to mark player as drafted

        Side Effects:
            - Each team ends up with 15 players
            - All teams' PlayerManagers have consistent drafted status
            - All teams' configs set to week 1 during draft (reset to proper week during season)
        """
        self.logger.debug("Starting draft simulation")

        for team in self.teams:
            team.config.current_nfl_week = 1

        # D3: draft on week-1 point-in-time projections. No-op in legacy no-cache mode
        # (empty week_data_cache -> _load_week_data early-returns), so unseeded/legacy
        # runs still draft on the init snapshot exactly as before.
        self._load_week_data(1)

        self.draft_order = self.teams.copy()
        self._rng.shuffle(self.draft_order)  # site #2 (T29): snake-draft order via per-league RNG

        for round_num in range(15):
            if round_num % 2 == 0:
                pick_order = self.draft_order
            else:
                pick_order = list(reversed(self.draft_order))

            for team in pick_order:
                player = team.get_draft_recommendation()

                team.draft_player(player)

                for other_team in self.teams:
                    if other_team != team:
                        other_team.mark_player_drafted(player.id)

        self.logger.debug("Draft complete: All teams have 15 players")

    def run_season(self) -> None:
        """
        Simulate 17-week regular season.

        For each week:
        1. Update team rankings (load teams_week_N.csv)
        2. Simulate all matchups
        3. Track results

        Side Effects:
            - Updates self.week_results with Week objects
            - Each team accumulates wins/losses
        """
        self.logger.debug("Starting 17-week season simulation")

        for week_num in range(1, 18):

            self._load_week_data(week_num)

            self._update_team_rankings(week_num)

            self._refresh_matchup_scores()

            matchups = self.season_schedule[week_num - 1]

            week = Week(week_num, matchups)
            week.simulate_week()

            self.week_results.append(week)

        self.logger.debug("Season complete: 17 weeks simulated")

    def _update_team_rankings(self, week_num: int) -> None:
        """
        Update team rankings for all teams for the given week.

        Uses TeamDataManager's set_current_week method to recalculate rankings
        based on the rolling window of historical data up to this week.

        Args:
            week_num (int): Week number (1-17)
        """
        for team in self.teams:
            if hasattr(team, 'team_data_mgr') and team.team_data_mgr:
                team.team_data_mgr.set_current_week(week_num)


    def _refresh_matchup_scores(self) -> None:
        """Recompute per-player matchup scores for each team's projected PlayerManager.

        The win-rate season advances weeks in place without rebuilding PlayerManagers, so a
        load-time populate alone would freeze matchup_score at the construction week. Called
        each week in run_season AFTER _update_team_rankings (which advances the shared
        TeamDataManager via set_current_week), this recomputes matchup_score from the now-current
        week so the win-rate sim's matchup factor matches the scored week. All PlayerManagers and
        the team share one TeamDataManager instance, so the refresh reads the advanced week.
        Only projected_pm is refreshed — it is the matchup-scored PlayerManager (Starter Helper
        reads it in DraftHelperTeam.set_weekly_lineup); actual_pm is not matchup-scored.
        """
        for team in self.teams:
            if hasattr(team, 'projected_pm') and team.projected_pm:
                team.projected_pm.refresh_matchup_scores()

    def get_draft_helper_results(self) -> Tuple[int, int, float]:
        """
        Get final results for the DraftHelperTeam.

        Returns:
            Tuple[int, int, float]: (wins, losses, total_points_scored)

        Note:
            This is the primary metric for evaluating configuration performance.
        """
        if not self.draft_helper_team:
            raise ValueError("DraftHelperTeam not found in league")

        wins = 0
        losses = 0
        total_points = 0.0

        for week in self.week_results:
            result = week.get_result(self.draft_helper_team)
            if result.won:
                wins += 1
            else:
                losses += 1
            total_points += result.points_scored

        self.logger.debug(f"DraftHelperTeam final results: {wins}W-{losses}L, {total_points:.2f} total points")

        return wins, losses, total_points

    def get_draft_helper_results_by_week(self) -> List[Tuple[int, bool, float]]:
        """
        Get per-week results for the DraftHelperTeam.

        Returns a list of tuples, one for each week played:
        - week_number (int): The week number (1-16)
        - won (bool): True if DraftHelperTeam won that week
        - points (float): Points scored that week

        This is used for per-week-range performance tracking to determine
        which configs perform best in different parts of the season.

        Returns:
            List[Tuple[int, bool, float]]: Per-week results

        Example:
            >>> results = league.get_draft_helper_results_by_week()
            >>> results[0]
            (1, True, 125.5)  # Week 1: Won with 125.5 points
        """
        if not self.draft_helper_team:
            raise ValueError("DraftHelperTeam not found in league")

        week_results = []

        for week in self.week_results:
            result = week.get_result(self.draft_helper_team)
            week_results.append((
                week.week_number,
                result.won,
                result.points_scored
            ))

        return week_results

    def get_all_team_results(self) -> Dict[str, Tuple[int, int, float]]:
        """
        Get results for all teams (for analysis/debugging).

        Returns:
            Dict[str, Tuple[int, int, float]]: {team_identifier: (wins, losses, points)}
        """
        results = {}

        for idx, team in enumerate(self.teams):
            wins = 0
            losses = 0
            total_points = 0.0

            for week in self.week_results:
                result = week.get_result(team)
                if result.won:
                    wins += 1
                else:
                    losses += 1
                total_points += result.points_scored

            team_type = "DraftHelper" if team == self.draft_helper_team else f"Opponent_{type(team).__name__}"
            results[f"Team_{idx}_{team_type}"] = (wins, losses, total_points)

        return results

    def cleanup(self) -> None:
        """
        Clean up temporary files and internal state after simulation.

        Should be called after simulation is complete to free disk space
        and memory. Clears all large objects to help garbage collector.
        """
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

        self.teams = None
        self.draft_helper_team = None
        self.week_results = None
        self.season_schedule = None
        self.draft_order = None
        self.config_dict = None

    def __del__(self) -> None:
        """Destructor to ensure cleanup happens."""
        try:
            self.cleanup()
        except:
            pass


