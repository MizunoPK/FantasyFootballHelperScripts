"""
Simulated League

Orchestrates a complete fantasy football league simulation including draft
and 17-week season. Manages 10 teams (1 DraftHelperTeam + 9 SimulatedOpponents)
through the entire process.

The simulation process:
1. Initialize teams with separate PlayerManager instances
2. Run snake draft (15 rounds, 150 total picks)
3. Run 17-week regular season with round-robin matchups
4. Track results and determine final standings

Author: Kai Mizuno
"""

import sys
import random
import shutil
import tempfile
import json
import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any

# Add league_helper to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "league_helper"))
sys.path.append(str(project_root / "league_helper" / "util"))
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager

# Import simulation classes
sys.path.append(str(Path(__file__).parent))
from DraftHelperTeam import DraftHelperTeam
from SimulatedOpponent import SimulatedOpponent
from Week import Week

# Import scheduler
sys.path.append(str(Path(__file__).parent / "utils"))
from utils.scheduler import generate_schedule_for_nfl_season

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


class SimulatedLeague:
    """
    Complete fantasy football league simulation.

    Manages 10 teams through draft and 17-week season, tracking results
    and determining final standings.

    Team Distribution (from TODO):
    - 1 DraftHelperTeam (our system being tested)
    - 2 adp_aggressive opponents
    - 2 projected_points_aggressive opponents
    - 2 adp_with_draft_order opponents
    - 3 projected_points_with_draft_order opponents

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

    # Team strategy distribution
    TEAM_STRATEGIES = {
        'draft_helper': 1,
        'adp_aggressive': 2,
        'projected_points_aggressive': 2,
        'adp_with_draft_order': 2,
        'projected_points_with_draft_order': 3
    }

    def __init__(self, config_dict: dict, data_folder: Path = Path("./simulation/sim_data")) -> None:
        """
        Initialize SimulatedLeague with configuration.

        Args:
            config_dict (dict): Configuration dictionary (will be saved as temp JSON)
            data_folder (Path): Path to folder containing players_projected.csv,
                               players_actual.csv, and teams_week_N.csv files

        Raises:
            FileNotFoundError: If data files are missing
        """
        self.logger = get_logger()
        self.logger.debug("Initializing SimulatedLeague")

        self.config_dict = config_dict
        self.data_folder = data_folder

        # Create temporary directory for this league's data
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sim_league_"))
        self.logger.debug(f"Created temporary directory: {self.temp_dir}")

        # Save config to temp file
        self.config_path = self.temp_dir / "league_config.json"
        with open(self.config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)

        # Initialize teams (will create separate PlayerManager instances for each)
        self.teams: List = []
        self.draft_helper_team: Optional[DraftHelperTeam] = None
        self.draft_order: List = []
        self.season_schedule: List[List[Tuple]] = []
        self.week_results: List[Week] = []

        # Cache for pre-loaded week data (historical data optimization)
        self.week_data_cache: Dict[int, Dict] = {}

        # Pre-load all 17 weeks of player data if historical structure exists
        self._preload_all_weeks()

        # Initialize all teams
        self._initialize_teams()

        # Generate schedule
        self._generate_schedule()

    def _initialize_teams(self) -> None:
        """
        Initialize all 10 teams with separate PlayerManager instances.

        Creates:
        - 1 DraftHelperTeam
        - 9 SimulatedOpponents with strategy distribution

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

        # Create strategy list based on distribution
        strategies = []
        for strategy, count in self.TEAM_STRATEGIES.items():
            strategies.extend([strategy] * count)

        # Shuffle to randomize which teams get which strategies
        random.shuffle(strategies)

        # Determine player data source paths
        # For historical data structure, use week 1 data for initial setup
        weeks_folder = self.data_folder / "weeks" / "week_01"
        if weeks_folder.exists():
            # Historical structure: use week 1 data
            players_projected_path = weeks_folder / "players_projected.csv"
            players_actual_path = weeks_folder / "players.csv"
            self.logger.debug("Using historical week 1 data for initial team setup")
        else:
            # Legacy flat structure
            players_projected_path = self.data_folder / "players_projected.csv"
            players_actual_path = self.data_folder / "players_actual.csv"

        # OPTIMIZATION: Create shared directories ONCE instead of per-team
        shared_projected_dir = self._create_shared_data_dir(
            "shared_projected", players_projected_path, players_projected_path
        )
        shared_actual_dir = self._create_shared_data_dir(
            "shared_actual", players_actual_path, players_projected_path
        )

        # Create shared ConfigManager (all teams use same config)
        shared_config = ConfigManager(shared_projected_dir)

        # Create shared SeasonScheduleManager
        shared_schedule_mgr = SeasonScheduleManager(shared_projected_dir)

        # Create shared TeamDataManager
        shared_team_data_mgr = TeamDataManager(
            shared_projected_dir, shared_config, shared_schedule_mgr, shared_config.current_nfl_week
        )

        # Create each team using shared directories
        for idx, strategy in enumerate(strategies):
            # Each team gets independent PlayerManager instances
            # PlayerManager loads data into memory, so each team has its own in-memory state
            projected_pm = PlayerManager(shared_projected_dir, shared_config, shared_team_data_mgr, shared_schedule_mgr)
            actual_pm = PlayerManager(shared_actual_dir, shared_config, shared_team_data_mgr, shared_schedule_mgr)

            # Create team based on strategy
            if strategy == 'draft_helper':
                team = DraftHelperTeam(projected_pm, actual_pm, shared_config, shared_team_data_mgr)
                self.draft_helper_team = team
                self.logger.debug(f"Created DraftHelperTeam (team {idx})")
            else:
                team = SimulatedOpponent(projected_pm, actual_pm, shared_config, shared_team_data_mgr, strategy)
                self.logger.debug(f"Created SimulatedOpponent (team {idx}, strategy: {strategy})")

            self.teams.append(team)

        self.logger.debug(f"Initialized {len(self.teams)} teams (using shared data directories)")

    def _create_shared_data_dir(self, dir_name: str, players_csv_path: Path, players_projected_path: Path) -> Path:
        """
        Create a shared data directory with all required files.

        This is called ONCE per simulation to create shared directories that all teams
        can read from. This optimization reduces file I/O from ~60 copies per simulation
        to just 2 directories.

        Args:
            dir_name (str): Name for the shared directory (e.g., "shared_projected")
            players_csv_path (Path): Source path for players.csv
            players_projected_path (Path): Source path for players_projected.csv

        Returns:
            Path: Path to the created shared directory
        """
        shared_dir = self.temp_dir / dir_name
        shared_dir.mkdir()

        # Copy player data files
        shutil.copy(players_csv_path, shared_dir / "players.csv")
        shutil.copy(players_projected_path, shared_dir / "players_projected.csv")

        # Copy config
        shutil.copy(self.config_path, shared_dir / "league_config.json")

        # Copy season schedule if exists
        if (self.data_folder / "season_schedule.csv").exists():
            shutil.copy(self.data_folder / "season_schedule.csv", shared_dir / "season_schedule.csv")

        # Copy game_data.csv if exists
        if (self.data_folder / "game_data.csv").exists():
            shutil.copy(self.data_folder / "game_data.csv", shared_dir / "game_data.csv")

        # Copy team_data folder (contains NFL team historical data)
        team_data_source = self.data_folder / "team_data"
        if team_data_source.exists():
            shutil.copytree(team_data_source, shared_dir / "team_data")
        else:
            self.logger.warning(f"team_data folder not found: {team_data_source}")

        self.logger.debug(f"Created shared data directory: {shared_dir}")
        return shared_dir

    def _generate_schedule(self) -> None:
        """
        Generate 17-week round-robin schedule.

        Uses generate_schedule_for_nfl_season to create matchups where each
        team plays each other team twice (as close as possible in 17 weeks).
        """
        self.logger.debug("Generating 17-week round-robin schedule")
        self.season_schedule = generate_schedule_for_nfl_season(self.teams, num_weeks=17)
        self.logger.debug(f"Generated schedule: {len(self.season_schedule)} weeks")

    def _preload_all_weeks(self) -> None:
        """
        Pre-load all 17 weeks of player data into memory cache.

        This optimization reduces disk I/O from 340 reads (17 weeks × 10 teams × 2 files)
        to just 17 reads per simulation. Data is parsed once and shared across all teams.

        Only loads data if historical structure (weeks/week_XX/) exists.
        Falls back gracefully if using legacy flat structure.
        """
        weeks_folder = self.data_folder / "weeks"

        if not weeks_folder.exists():
            self.logger.debug("No weeks/ folder found - using legacy flat structure")
            return

        self.logger.debug("Pre-loading all 17 weeks of player data")

        for week_num in range(1, 18):
            week_folder = weeks_folder / f"week_{week_num:02d}"
            players_file = week_folder / "players.csv"

            if players_file.exists():
                self.week_data_cache[week_num] = self._parse_players_csv(players_file)
                self.logger.debug(f"Cached week {week_num}: {len(self.week_data_cache[week_num])} players")
            else:
                self.logger.warning(f"Week {week_num} players.csv not found at {players_file}")

        self.logger.debug(f"Pre-loaded {len(self.week_data_cache)} weeks of player data")

    def _parse_players_csv(self, filepath: Path) -> Dict[int, Dict[str, Any]]:
        """
        Parse players.csv into dictionary format keyed by player ID.

        Args:
            filepath (Path): Path to players.csv file

        Returns:
            Dict[int, Dict[str, Any]]: Player data keyed by player ID
        """
        players = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    player_id = int(row.get('id', 0))
                    if player_id > 0:
                        players[player_id] = dict(row)
                except (ValueError, KeyError):
                    continue
        return players

    def _load_week_data(self, week_num: int) -> None:
        """
        Load week-specific player data from pre-loaded cache.

        Updates all teams' PlayerManagers with the week's data.
        This is called at the start of each week during run_season().

        Args:
            week_num (int): Week number (1-17)

        Note:
            Does nothing if week data was not pre-loaded (legacy mode).
        """
        if week_num not in self.week_data_cache:
            # Legacy mode - no week-specific data available
            return

        week_player_data = self.week_data_cache[week_num]

        # Update each team's PlayerManagers with week-specific data
        for team in self.teams:
            if hasattr(team, 'projected_pm') and hasattr(team.projected_pm, 'set_player_data'):
                team.projected_pm.set_player_data(week_player_data)
            if hasattr(team, 'actual_pm') and hasattr(team.actual_pm, 'set_player_data'):
                team.actual_pm.set_player_data(week_player_data)

        self.logger.debug(f"Loaded week {week_num} data for all teams")

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

        # Set all teams to week 1 for draft (no performance history yet)
        for team in self.teams:
            team.config.current_nfl_week = 1
        self.logger.debug("Set all teams to week 1 for draft (no performance history)")

        # Randomize initial draft order
        self.draft_order = self.teams.copy()
        random.shuffle(self.draft_order)
        self.logger.debug(f"Draft order randomized: {len(self.draft_order)} teams")

        # Run 15 rounds
        for round_num in range(15):
            # Determine pick order for this round (snake)
            if round_num % 2 == 0:
                # Even rounds: normal order (1→10)
                pick_order = self.draft_order
            else:
                # Odd rounds: reverse order (10→1)
                pick_order = list(reversed(self.draft_order))

            self.logger.debug(f"Draft Round {round_num + 1}/15")

            # Each team picks
            for team in pick_order:
                # Get recommendation
                player = team.get_draft_recommendation()

                # Team drafts the player
                team.draft_player(player)

                # Broadcast to all other teams
                for other_team in self.teams:
                    if other_team != team:
                        other_team.mark_player_drafted(player.id)

                self.logger.debug(f"Round {round_num + 1}: {player.name} ({player.position}) drafted")

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

        for week_num in range(1, 18):  # Weeks 1-17
            self.logger.debug(f"Simulating Week {week_num}/17")

            # Load week-specific player data from pre-loaded cache (if available)
            self._load_week_data(week_num)

            # Update team rankings for this week
            self._update_team_rankings(week_num)

            # Get matchups for this week
            matchups = self.season_schedule[week_num - 1]  # 0-indexed

            # Create and simulate week
            week = Week(week_num, matchups)
            week.simulate_week()

            # Store results
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
        # Update each team's TeamDataManager to recalculate rankings for this week
        for team in self.teams:
            if hasattr(team, 'team_data_mgr') and team.team_data_mgr:
                team.team_data_mgr.set_current_week(week_num)

        self.logger.debug(f"Updated team rankings for week {week_num}")

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

        self.logger.info(f"DraftHelperTeam final results: {wins}W-{losses}L, {total_points:.2f} total points")

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
        # Clean up temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self.logger.debug(f"Cleaned up temporary directory: {self.temp_dir}")

        # Clear large internal objects to free memory immediately
        # This prevents memory accumulation when GC is delayed
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
            pass  # Ignore errors during cleanup
