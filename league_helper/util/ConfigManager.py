"""
Configuration Manager

Centralized configuration management for Fantasy Football League Helper.
Loads and validates all league settings from league_config.json, providing
type-safe access to scoring parameters, thresholds, multipliers, and
mode-specific configurations.

This module handles:
- Loading and validating JSON configuration
- Extracting NFL settings (season, week, scoring format)
- Managing scoring thresholds and multipliers for all 9 scoring steps
- Providing draft order bonuses and strategy
- Calculating penalties for injuries and bye weeks

Author: Kai Mizuno
"""

import json
import statistics
from pathlib import Path
from typing import Any, Dict, List, Tuple

import league_helper.constants as Constants
from historical_data_compiler.constants import ALL_NFL_TEAMS
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer


class ConfigKeys:
    """
    Constants for JSON configuration keys.

    This class defines all valid keys used in league_config.json, providing
    a centralized reference for configuration structure. Using constants
    prevents typos and makes refactoring easier.

    The configuration follows a hierarchical structure:
    - Top level: config_name, description, parameters
    - Parameters: NFL settings, scoring configs, mode-specific settings
    - Nested: thresholds, multipliers, bonuses for each scoring category
    """

    CONFIG_NAME = "config_name"
    DESCRIPTION = "description"
    PARAMETERS = "parameters"

    CURRENT_NFL_WEEK = "CURRENT_NFL_WEEK"
    NFL_SEASON = "NFL_SEASON"
    NFL_SCORING_FORMAT = "NFL_SCORING_FORMAT"
    NORMALIZATION_MAX_SCALE = "NORMALIZATION_MAX_SCALE"
    DRAFT_NORMALIZATION_MAX_SCALE = "DRAFT_NORMALIZATION_MAX_SCALE"
    SAME_POS_BYE_WEIGHT = "SAME_POS_BYE_WEIGHT"
    DIFF_POS_BYE_WEIGHT = "DIFF_POS_BYE_WEIGHT"
    INJURY_PENALTIES = "INJURY_PENALTIES"
    ADP_SCORING = "ADP_SCORING"
    PLAYER_RATING_SCORING = "PLAYER_RATING_SCORING"
    TEAM_QUALITY_SCORING = "TEAM_QUALITY_SCORING"
    CONSISTENCY_SCORING = "CONSISTENCY_SCORING"
    PERFORMANCE_SCORING = "PERFORMANCE_SCORING"
    MATCHUP_SCORING = "MATCHUP_SCORING"
    SCHEDULE_SCORING = "SCHEDULE_SCORING"
    TEMPERATURE_SCORING = "TEMPERATURE_SCORING"
    WIND_SCORING = "WIND_SCORING"
    LOCATION_MODIFIERS = "LOCATION_MODIFIERS"
    DRAFT_ORDER_BONUSES = "DRAFT_ORDER_BONUSES"
    DRAFT_ORDER = "DRAFT_ORDER"
    MAX_POSITIONS = "MAX_POSITIONS"
    FLEX_ELIGIBLE_POSITIONS = "FLEX_ELIGIBLE_POSITIONS"
    NFL_TEAM_PENALTY = "NFL_TEAM_PENALTY"
    NFL_TEAM_PENALTY_WEIGHT = "NFL_TEAM_PENALTY_WEIGHT"

    TRADE_SIMULATOR = "TRADE_SIMULATOR"

    TRADE_WAIVERS_TWO_FOR_TWO = "WAIVERS_TWO_FOR_TWO"
    TRADE_WAIVERS_THREE_FOR_THREE = "WAIVERS_THREE_FOR_THREE"
    TRADE_ENABLE_ONE_FOR_ONE = "ENABLE_ONE_FOR_ONE"
    TRADE_ENABLE_TWO_FOR_TWO = "ENABLE_TWO_FOR_TWO"
    TRADE_ENABLE_THREE_FOR_THREE = "ENABLE_THREE_FOR_THREE"
    TRADE_ENABLE_TWO_FOR_ONE = "ENABLE_TWO_FOR_ONE"
    TRADE_ENABLE_ONE_FOR_TWO = "ENABLE_ONE_FOR_TWO"
    TRADE_ENABLE_THREE_FOR_ONE = "ENABLE_THREE_FOR_ONE"
    TRADE_ENABLE_ONE_FOR_THREE = "ENABLE_ONE_FOR_THREE"
    TRADE_ENABLE_THREE_FOR_TWO = "ENABLE_THREE_FOR_TWO"
    TRADE_ENABLE_TWO_FOR_THREE = "ENABLE_TWO_FOR_THREE"
    TRADE_MAX_COMBINATIONS = "MAX_COMBINATIONS"

    DRAFT_ORDER_PRIMARY_LABEL = "P"
    DRAFT_ORDER_SECONDARY_LABEL = "S"

    MULTIPLIERS = "MULTIPLIERS"
    THRESHOLDS = "THRESHOLDS"
    MIN_WEEKS = "MIN_WEEKS"
    WEIGHT = "WEIGHT"
    IDEAL_TEMPERATURE = "IDEAL_TEMPERATURE"
    IMPACT_SCALE = "IMPACT_SCALE"

    LOCATION_HOME = "HOME"
    LOCATION_AWAY = "AWAY"
    LOCATION_INTERNATIONAL = "INTERNATIONAL"

    INJURY_LOW = "LOW"
    INJURY_MEDIUM = "MEDIUM"
    INJURY_HIGH = "HIGH"

    BONUS_PRIMARY = "PRIMARY"
    BONUS_SECONDARY = "SECONDARY"

    VERY_POOR = "VERY_POOR"
    POOR = "POOR"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"
    NEUTRAL = "NEUTRAL"

    BASE_POSITION = "BASE_POSITION"
    DIRECTION = "DIRECTION"
    STEPS = "STEPS"

    DIRECTION_INCREASING = "INCREASING"
    DIRECTION_DECREASING = "DECREASING"
    DIRECTION_BI_EXCELLENT_HI = "BI_EXCELLENT_HI"
    DIRECTION_BI_EXCELLENT_LOW = "BI_EXCELLENT_LOW"

    CALCULATED = "_calculated"
    MAX_SEARCH_RESULTS = "MAX_SEARCH_RESULTS"


class ConfigManager:
    """
    Manages all configuration settings from league_config.json.

    This class is the single source of truth for all league configuration,
    including scoring parameters, thresholds, multipliers, and mode-specific
    settings. It validates the JSON structure and provides type-safe access
    to all configuration values.

    Attributes:
        config_name (str): Name of the configuration (e.g., "Default", "Test High Normalization")
        description (str): Description of this configuration's purpose
        current_nfl_week (int): Current NFL week number
        nfl_season (int): Current NFL season year
        nfl_scoring_format (str): Scoring format ("ppr", "std", "half")
        normalization_max_scale (float): Maximum scale for normalized scores
        base_bye_penalty (float): Base penalty per bye week conflict
        injury_penalties (Dict[str, float]): Penalties by injury risk level (LOW/MEDIUM/HIGH)
        adp_scoring (Dict): ADP thresholds and multipliers
        player_rating_scoring (Dict): Player rating thresholds and multipliers
        team_quality_scoring (Dict): Team quality thresholds and multipliers
        performance_scoring (Dict): Performance deviation thresholds and multipliers
        matchup_scoring (Dict): Matchup thresholds and multipliers
        draft_order_bonuses (Dict): PRIMARY and SECONDARY draft bonuses
        draft_order (List[Dict]): Draft strategy by round

    Example:
        >>> config = ConfigManager(Path("./data"))
        >>> adp_mult = config.get_adp_multiplier(15)  # ADP of 15 → returns multiplier
        >>> draft_bonus = config.get_draft_order_bonus("RB", 0)  # RB in first round (0-indexed) → returns bonus
    """


    def __init__(self, data_folder: Path) -> None:
        """
        Initialize the config manager and load configuration.

        Supports two folder structures:
        1. New structure: data/configs/league_config.json + week{N}-{M}.json files
        2. Legacy structure: data/league_config.json (for tests and backward compatibility)

        Args:
            data_folder (Path): Path to the data directory containing config files

        Raises:
            FileNotFoundError: If league_config.json is not found
            ValueError: If configuration structure is invalid or missing required fields
        """
        self.keys = ConfigKeys()
        self.config_name: str = ""
        self.description: str = ""
        self.parameters: Dict[str, Any] = {}
        self.logger = get_logger()

        configs_folder = data_folder / 'configs'
        if configs_folder.exists() and (configs_folder / 'league_config.json').exists():
            self.config_path = configs_folder / 'league_config.json'
            self.configs_folder = configs_folder
            self.logger.debug(f"Using new config structure: {configs_folder}")
        else:
            self.config_path = data_folder / 'league_config.json'
            self.configs_folder = None
            self.logger.debug(f"Using legacy config structure: {self.config_path}")

        self.current_nfl_week: int = 0
        self.nfl_season: int = 0
        self.nfl_scoring_format: str = ""

        self.normalization_max_scale: float = 0.0
        self.same_pos_bye_weight: float = 0.0
        self.diff_pos_bye_weight: float = 0.0
        self.injury_penalties: Dict[str, float] = {}
        self.adp_scoring: Dict[str, Any] = {}
        self.player_rating_scoring: Dict[str, Any] = {}
        self.team_quality_scoring: Dict[str, Any] = {}
        self.consistency_scoring: Dict[str, Any] = {}
        self.performance_scoring: Dict[str, Any] = {}
        self.matchup_scoring: Dict[str, Any] = {}
        self.schedule_scoring: Dict[str, Any] = {}
        self.temperature_scoring: Dict[str, Any] = {}
        self.wind_scoring: Dict[str, Any] = {}
        self.location_modifiers: Dict[str, float] = {}

        self.draft_order_bonuses: Dict[str, float] = {}
        self.draft_order: List[Dict[str, str]] = []

        self.max_positions: Dict[str, int] = {}
        self.flex_eligible_positions: List[str] = []

        self.nfl_team_penalty: List[str] = []
        self.nfl_team_penalty_weight: float = 1.0

        self.trade_waivers_two_for_two: bool = False
        self.trade_waivers_three_for_three: bool = False
        self.trade_enable_one_for_one: bool = False
        self.trade_enable_two_for_two: bool = True
        self.trade_enable_three_for_three: bool = True
        self.trade_enable_two_for_one: bool = True
        self.trade_enable_one_for_two: bool = True
        self.trade_enable_three_for_one: bool = False
        self.trade_enable_one_for_three: bool = False
        self.trade_enable_three_for_two: bool = True
        self.trade_enable_two_for_three: bool = True
        self.trade_max_combinations: int = 50000

        self._threshold_cache: Dict[Tuple[str, float, str, float], Dict[str, float]] = {}
        self.max_search_results: int = 15

        self._load_config()


    def _get_week_config_filename(self, week: int) -> str:
        """
        Get the week-specific config filename for a given week number.

        Week ranges:
        - Weeks 1-5: week1-5.json
        - Weeks 6-9: week6-9.json
        - Weeks 10-13: week10-13.json
        - Weeks 14-17: week14-17.json

        Args:
            week (int): NFL week number (1-17)

        Returns:
            str: Filename for the week-specific config

        Raises:
            ValueError: If week is outside valid range (1-17)
        """
        if 1 <= week <= 5:
            return "week1-5.json"
        elif 6 <= week <= 9:
            return "week6-9.json"
        elif 10 <= week <= 13:
            return "week10-13.json"
        elif 14 <= week <= 17:
            return "week14-17.json"
        else:
            raise ValueError(f"Invalid week number: {week}. Must be between 1 and 17.")

    def _load_week_config(self, week: int) -> Dict[str, Any]:
        """
        Load week-specific config parameters and return them for merging.

        Only loads if configs_folder is set (new folder structure).
        Returns empty dict if using legacy structure or if week config not found.

        Args:
            week (int): NFL week number to load config for

        Returns:
            Dict[str, Any]: Week-specific parameters to merge, or empty dict
        """
        if self.configs_folder is None:
            self.logger.debug("Legacy config mode, skipping week-specific config")
            return {}

        week_filename = self._get_week_config_filename(week)
        week_config_path = self.configs_folder / week_filename

        if not week_config_path.exists():
            self.logger.warning(f"Week config not found: {week_config_path}")
            return {}

        try:
            with open(week_config_path, 'r') as f:
                week_data = json.load(f)
            self.logger.debug(f"Loaded week config: {week_filename}")

            return week_data.get(self.keys.PARAMETERS, {})

        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in week config {week_filename}: {e}")
            raise


    @property
    def max_players(self) -> int:
        """
        Calculate total roster size as sum of MAX_POSITIONS.

        Returns:
            int: Total maximum players allowed (sum of all position limits)
        """
        return sum(self.max_positions.values())

    def get_position_with_flex(self, position: str) -> str:
        """
        Determine if a position should be considered for FLEX assignment.

        In fantasy football, certain positions (typically RB/WR) can fill FLEX slots.
        This method checks if a given position is FLEX-eligible according to the
        league configuration.

        Args:
            position: Player's natural position (QB, RB, WR, TE, K, DST)

        Returns:
            'FLEX' if position is in flex_eligible_positions, otherwise the original position

        Example:
            >>> config.get_position_with_flex('RB')
            'FLEX'
            >>> config.get_position_with_flex('QB')
            'QB'
        """
        if position in self.flex_eligible_positions:
            return 'FLEX'
        else:
            return position

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """
        Get a parameter value by key.

        Args:
            key: The parameter key
            default: Default value if key not found

        Returns:
            The parameter value or default
        """
        return self.parameters.get(key, default)

    def has_parameter(self, key: str) -> bool:
        """
        Check if a parameter exists.

        Args:
            key: The parameter key

        Returns:
            True if parameter exists, False otherwise
        """
        return key in self.parameters


    def get_adp_multiplier(self, adp_val) -> Tuple[float, str]:
        return self._get_multiplier(self.adp_scoring, adp_val, rising_thresholds=False)

    def get_player_rating_multiplier(self, rating) -> Tuple[float, str]:
        return self._get_multiplier(self.player_rating_scoring, rating)

    def get_team_quality_multiplier(self, quality_rank : int) -> Tuple[float, str]:
        return self._get_multiplier(self.team_quality_scoring, quality_rank, rising_thresholds=False)

    def get_matchup_multiplier(self, value) -> Tuple[float, str]:
        return self._get_multiplier(self.matchup_scoring, value)

    def get_schedule_multiplier(self, schedule_value) -> Tuple[float, str]:
        """
        Get schedule multiplier based on average future opponent defense rank.

        Args:
            schedule_value: Average defense rank of future opponents (1-32)
                           Higher rank = worse defenses = easier schedule = higher multiplier

        Returns:
            Tuple (multiplier, rating_label)
        """
        return self._get_multiplier(
            self.schedule_scoring,
            schedule_value,
            rising_thresholds=True
        )

    def get_performance_multiplier(self, deviation: float) -> Tuple[float, str]:
        return self._get_multiplier(self.performance_scoring, deviation)

    def get_temperature_distance(self, temperature: int) -> float:
        """
        Calculate distance from ideal temperature.

        Args:
            temperature (int): Actual game temperature in Fahrenheit

        Returns:
            float: Absolute distance from ideal temperature (0 = ideal, higher = worse)

        Example:
            >>> config.get_temperature_distance(75)  # If ideal is 60
            15.0
            >>> config.get_temperature_distance(45)  # If ideal is 60
            15.0
        """
        ideal_temp = self.temperature_scoring.get(self.keys.IDEAL_TEMPERATURE, 60)
        return abs(temperature - ideal_temp)

    def get_temperature_multiplier(self, temp_distance: float) -> Tuple[float, str]:
        """
        Get temperature multiplier based on distance from ideal.

        Lower distance = better (closer to ideal temperature).
        Uses DECREASING direction: E=base+1s, G=base+2s, P=base+3s, VP=base+4s

        Args:
            temp_distance (float): Distance from ideal temperature (from get_temperature_distance)

        Returns:
            Tuple[float, str]: (multiplier, tier_name)
        """
        return self._get_multiplier(self.temperature_scoring, temp_distance, rising_thresholds=False)

    def get_wind_multiplier(self, wind_gust: float) -> Tuple[float, str]:
        """
        Get wind multiplier based on gust speed.

        Lower wind = better (calmer conditions).
        Uses DECREASING direction: E=base+1s, G=base+2s, P=base+3s, VP=base+4s

        Args:
            wind_gust (float): Wind gust speed in mph

        Returns:
            Tuple[float, str]: (multiplier, tier_name)
        """
        return self._get_multiplier(self.wind_scoring, wind_gust, rising_thresholds=False)

    def get_location_modifier(self, is_home: bool, is_international: bool) -> float:
        """
        Get location modifier based on game location.

        Args:
            is_home (bool): True if team is playing at home
            is_international (bool): True if game is outside USA

        Returns:
            float: Location modifier (positive = bonus, negative = penalty)

        Priority:
            1. International games always use INTERNATIONAL modifier (regardless of home/away)
            2. Domestic home games use HOME modifier
            3. Domestic away games use AWAY modifier
        """
        if is_international:
            return self.location_modifiers.get(self.keys.LOCATION_INTERNATIONAL, 0.0)
        elif is_home:
            return self.location_modifiers.get(self.keys.LOCATION_HOME, 0.0)
        else:
            return self.location_modifiers.get(self.keys.LOCATION_AWAY, 0.0)


    def get_team_quality_min_weeks(self) -> int:
        """
        Get MIN_WEEKS for team quality scoring calculations.

        Returns:
            int: Number of weeks for rolling window (default 5)
        """
        return self.team_quality_scoring.get(self.keys.MIN_WEEKS, 5)

    def get_matchup_min_weeks(self) -> int:
        """
        Get MIN_WEEKS for matchup scoring calculations.

        Returns:
            int: Number of weeks for rolling window (default 5)
        """
        return self.matchup_scoring.get(self.keys.MIN_WEEKS, 5)

    def get_schedule_min_weeks(self) -> int:
        """
        Get MIN_WEEKS for schedule scoring calculations.

        Returns:
            int: Number of weeks for rolling window (default 5)
        """
        return self.schedule_scoring.get(self.keys.MIN_WEEKS, 5)


    def get_draft_order_bonus(self, position : str, draft_round : int) -> Tuple[float, str]:
        """
        Get draft order bonus for a position in a specific round.

        The draft strategy defines which positions to prioritize in each round.
        PRIMARY positions get the highest bonus, SECONDARY positions get a smaller bonus,
        and non-listed positions get no bonus.

        Args:
            position: Player position (QB, RB, WR, TE, K, DST, or FLEX)
            draft_round: Draft round number (0-indexed)

        Returns:
            Tuple[float, str]: (bonus_points, bonus_type)
                - bonus_points: Point bonus to add to score
                - bonus_type: "PRIMARY", "SECONDARY", or "" (no bonus)

        Example:
            First round strategy (draft_round=0): {"RB": "P", "WR": "S"}
            - get_draft_order_bonus("RB", 0) → (10.0, "PRIMARY")
            - get_draft_order_bonus("WR", 0) → (5.0, "SECONDARY")
            - get_draft_order_bonus("QB", 0) → (0, "")
        """
        position_with_flex = self.get_position_with_flex(position)

        ideal_positions = self.draft_order[draft_round]

        if position_with_flex in ideal_positions:
            priority = ideal_positions.get(position_with_flex)

            if priority == self.keys.DRAFT_ORDER_PRIMARY_LABEL:
                return self.draft_order_bonuses[self.keys.BONUS_PRIMARY], self.keys.BONUS_PRIMARY
            else:
                return self.draft_order_bonuses[self.keys.BONUS_SECONDARY], self.keys.BONUS_SECONDARY
        else:
            return 0, ""

    def get_bye_week_penalty(self, same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float:
        """
        Calculate bye week penalty based on median weekly scores of conflicting players.

        Bye week conflicts reduce a player's value when rostering them would create
        depth issues on a specific week. The penalty is calculated using the median
        weekly points of players who share the same bye week, then applying linear
        scaling based on position overlap.

        Algorithm:
        1. For each player in same_pos_players: calculate median from weeks 1-17
        2. For each player in diff_pos_players: calculate median from weeks 1-17
        3. Sum all medians for each list
        4. Apply linear scaling: same_total * SAME_POS_BYE_WEIGHT + diff_total * DIFF_POS_BYE_WEIGHT

        The linear scaling allows the penalty to grow proportionally with player quality.
        Weight values typically range 0.0-1.0:
        - Higher weight = larger penalty per point of median value
        - Same-position weight is higher than different-position (more impactful)

        Args:
            same_pos_players: List of players on roster with same position and same bye week
            diff_pos_players: List of players on roster with different position and same bye week

        Returns:
            float: Total bye week penalty (linearly scaled sum)

        Example:
            Config has SAME_POS_BYE_WEIGHT=0.403, DIFF_POS_BYE_WEIGHT=0.176
            same_pos_players = [RB with median 15.0, RB with median 12.0] → total 27.0
            diff_pos_players = [WR with median 18.0] → total 18.0
            penalty = 27.0 * 0.403 + 18.0 * 0.176 = 10.88 + 3.17 = 14.05 points
        """
        def calculate_player_median(player: FantasyPlayer) -> float:
            """
            Calculate median weekly points for a player from weeks 1-17.

            Filters out None and zero values, returns 0.0 if no valid data.
            """
            try:
                valid_weeks = [
                    points for week in range(1, 18)
                    if (points := player.get_single_weekly_projection(week, self)) is not None
                    and points > 0
                ]

                if not valid_weeks:
                    self.logger.debug(f"No valid weekly data for {player.name}, using 0.0 median")
                    return 0.0

                median = statistics.median(valid_weeks)
                self.logger.debug(f"Median for {player.name}: {median:.2f} from {len(valid_weeks)} valid weeks")
                return median

            except statistics.StatisticsError as e:
                self.logger.error(f"Failed to calculate median for {player.name}: {e}")
                return 0.0
            except Exception as e:
                self.logger.error(f"Unexpected error calculating median for {player.name}: {e}")
                return 0.0

        same_pos_median_total = sum(calculate_player_median(p) for p in same_pos_players)
        diff_pos_median_total = sum(calculate_player_median(p) for p in diff_pos_players)

        same_penalty = same_pos_median_total * self.same_pos_bye_weight
        diff_penalty = diff_pos_median_total * self.diff_pos_bye_weight

        total_penalty = same_penalty + diff_penalty

        self.logger.debug(
            f"Bye penalty calculation: "
            f"same_pos_median={same_pos_median_total:.2f}*{self.same_pos_bye_weight}={same_penalty:.2f}, "
            f"diff_pos_median={diff_pos_median_total:.2f}*{self.diff_pos_bye_weight}={diff_penalty:.2f}, "
            f"total={total_penalty:.2f}"
        )

        return total_penalty

    def get_injury_penalty(self, risk_level : str) -> float:
        """
        Get injury penalty for a given risk level.

        Args:
            risk_level: Injury risk level (LOW, MEDIUM, or HIGH)

        Returns:
            float: Penalty points to subtract from player score

        Note:
            If an invalid risk level is provided, defaults to HIGH penalty
            for safety (conservative approach to injury risk)
        """
        if risk_level in self.injury_penalties:
            return self.injury_penalties[risk_level]
        else:
            return self.injury_penalties[self.keys.INJURY_HIGH]


    def get_draft_position_for_round(self, round_number: int) -> Dict[str, str]:
        """
        Get the draft order entry for a specific round.

        Args:
            round_number: The draft round (1-indexed)

        Returns:
            Dictionary mapping positions to priority ('P' or 'S')

        Raises:
            IndexError: If round_number is out of range
        """
        if round_number < 1 or round_number > len(self.draft_order):
            raise IndexError(
                f"Round number {round_number} out of range (1-{len(self.draft_order)})"
            )

        return self.draft_order[round_number - 1]

    def get_ideal_draft_position(self, round_num: int) -> str:
        """
        Get the ideal position to draft in a given round (returns PRIMARY='P' position).

        Args:
            round_num: Draft round number (0-indexed)

        Returns:
            str: The PRIMARY position for this round, or 'FLEX' if round is out of range

        Example:
            Round 1 strategy: {"RB": "P", "WR": "S"}
            → Returns "RB" (PRIMARY position)
        """
        if round_num < len(self.draft_order):
            best_position = min(self.draft_order[round_num], key=self.draft_order[round_num].get)
            return best_position

        return 'FLEX'


    def validate_threshold_params(self, base_pos: float, direction: str, steps: float) -> bool:
        """
        Validate threshold parameters.

        Args:
            base_pos: Base position value (typically 0)
            direction: Direction type (INCREASING, DECREASING, BI_EXCELLENT_HI, BI_EXCELLENT_LOW)
            steps: Step size between thresholds (must be positive)

        Returns:
            True if parameters are valid

        Raises:
            ValueError: If parameters are invalid
        """
        import math

        if steps <= 0:
            self.logger.error(f"STEPS must be positive, got {steps}")
            raise ValueError(f"STEPS must be positive, got {steps}")

        if not math.isfinite(base_pos) or not math.isfinite(steps):
            self.logger.error("BASE_POSITION and STEPS must be finite")
            raise ValueError("BASE_POSITION and STEPS must be finite")

        valid_dirs = [
            self.keys.DIRECTION_INCREASING,
            self.keys.DIRECTION_DECREASING,
            self.keys.DIRECTION_BI_EXCELLENT_HI,
            self.keys.DIRECTION_BI_EXCELLENT_LOW
        ]
        if direction not in valid_dirs:
            self.logger.error(f"DIRECTION must be one of {valid_dirs}, got '{direction}'")
            raise ValueError(f"DIRECTION must be one of {valid_dirs}, got '{direction}'")

        return True

    def calculate_thresholds(self, base_pos: float, direction: str, steps: float,
                            scoring_type: str = "") -> Dict[str, float]:
        """
        Calculate threshold values from parameters.

        This method implements the parameterized threshold system, replacing
        hardcoded threshold values with calculated ones based on:
        - BASE_POSITION: Starting point (typically 0)
        - DIRECTION: How thresholds are arranged
        - STEPS: Spacing between threshold levels

        Args:
            base_pos: Base position (typically 0)
            direction: INCREASING, DECREASING, BI_EXCELLENT_HI, or BI_EXCELLENT_LOW
            steps: Step size between thresholds
            scoring_type: Optional scoring type for caching (e.g., "ADP_SCORING")

        Returns:
            Dict with VERY_POOR, POOR, GOOD, EXCELLENT threshold values

        Examples:
            >>> # INCREASING (player rating): VP=20, P=40, G=60, E=80
            >>> config.calculate_thresholds(0, "INCREASING", 20)
            {'VERY_POOR': 20, 'POOR': 40, 'GOOD': 60, 'EXCELLENT': 80}

            >>> # DECREASING (ADP): E=37.5, G=75, P=112.5, VP=150
            >>> config.calculate_thresholds(0, "DECREASING", 37.5)
            {'EXCELLENT': 37.5, 'GOOD': 75, 'POOR': 112.5, 'VERY_POOR': 150}

            >>> # BI_EXCELLENT_HI (performance): VP=-0.2, P=-0.1, G=0.1, E=0.2
            >>> config.calculate_thresholds(0, "BI_EXCELLENT_HI", 0.1)
            {'VERY_POOR': -0.2, 'POOR': -0.1, 'GOOD': 0.1, 'EXCELLENT': 0.2}
        """
        cache_key = (scoring_type, base_pos, direction, steps)
        if cache_key in self._threshold_cache:
            return self._threshold_cache[cache_key]

        self.validate_threshold_params(base_pos, direction, steps)

        if direction == self.keys.DIRECTION_INCREASING:
            thresholds = {
                self.keys.VERY_POOR: base_pos + steps,
                self.keys.POOR: base_pos + (2 * steps),
                self.keys.GOOD: base_pos + (3 * steps),
                self.keys.EXCELLENT: base_pos + (4 * steps)
            }

        elif direction == self.keys.DIRECTION_DECREASING:
            thresholds = {
                self.keys.EXCELLENT: base_pos + steps,
                self.keys.GOOD: base_pos + (2 * steps),
                self.keys.POOR: base_pos + (3 * steps),
                self.keys.VERY_POOR: base_pos + (4 * steps)
            }

        elif direction == self.keys.DIRECTION_BI_EXCELLENT_HI:
            thresholds = {
                self.keys.VERY_POOR: base_pos - (steps * 2),
                self.keys.POOR: base_pos - steps,
                self.keys.GOOD: base_pos + steps,
                self.keys.EXCELLENT: base_pos + (steps * 2)
            }

        elif direction == self.keys.DIRECTION_BI_EXCELLENT_LOW:
            thresholds = {
                self.keys.EXCELLENT: base_pos - (steps * 2),
                self.keys.GOOD: base_pos - steps,
                self.keys.POOR: base_pos + steps,
                self.keys.VERY_POOR: base_pos + (steps * 2)
            }

        else:
            raise ValueError(f"Invalid direction: {direction}")

        self._threshold_cache[cache_key] = thresholds
        return thresholds


    def _load_config(self) -> None:
        """
        Load and validate configuration from JSON file(s).

        For new folder structure (data/configs/):
        1. Load base config (league_config.json)
        2. Extract CURRENT_NFL_WEEK to determine which week config to load
        3. Load week-specific config (week{N}-{M}.json)
        4. Merge week-specific parameters over base parameters
        5. Validate and extract all parameters

        For legacy structure (data/league_config.json):
        - Load single config file as before

        Raises:
            FileNotFoundError: If league_config.json does not exist
            json.JSONDecodeError: If the JSON is malformed
            ValueError: If required fields are missing or invalid
        """
        self.logger.debug(f"Loading configuration from: {self.config_path}")

        if not self.config_path.exists():
            self.logger.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            raise

        self._validate_config_structure(data)

        self.config_name = data.get(self.keys.CONFIG_NAME, "")
        self.description = data.get(self.keys.DESCRIPTION, "")
        self.parameters = data.get(self.keys.PARAMETERS, {})

        self.logger.debug(f"Loaded configuration: '{self.config_name}'")
        self.logger.debug(f"Description: {self.description}")
        self.logger.debug(f"Parameters count: {len(self.parameters)}")

        if self.configs_folder is not None:
            if self.keys.CURRENT_NFL_WEEK not in self.parameters:
                raise ValueError("Base config missing required parameter: CURRENT_NFL_WEEK")

            current_week = self.parameters[self.keys.CURRENT_NFL_WEEK]
            self.logger.debug(f"Current NFL week: {current_week}")

            prediction_params = self._load_week_config(current_week)
            config_source = self._get_week_config_filename(current_week)

            if prediction_params:
                self.parameters.update(prediction_params)
                self.logger.info(
                    f"Merged prediction config ({config_source}): "
                    f"{len(prediction_params)} parameters"
                )

        self._extract_parameters()
        self.logger.debug("Configuration loaded and validated successfully")

    def _validate_config_structure(self, data: Dict[str, Any]) -> None:
        """
        Validate that the configuration has the required structure.

        Args:
            data: The loaded JSON data

        Raises:
            ValueError: If required fields are missing or have invalid types
        """
        required_fields = [self.keys.CONFIG_NAME, self.keys.DESCRIPTION, self.keys.PARAMETERS]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            error_msg = f"Configuration missing required fields: {', '.join(missing_fields)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        if not isinstance(data[self.keys.PARAMETERS], dict):
            error_msg = "'parameters' field must be a dictionary"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

    def _extract_parameters(self) -> None:
        """Extract and validate all parameters from the config."""
        required_params = [
            self.keys.CURRENT_NFL_WEEK,
            self.keys.NFL_SEASON,
            self.keys.NFL_SCORING_FORMAT,
            self.keys.NORMALIZATION_MAX_SCALE,
            self.keys.DRAFT_NORMALIZATION_MAX_SCALE,
            self.keys.SAME_POS_BYE_WEIGHT,
            self.keys.DIFF_POS_BYE_WEIGHT,
            self.keys.INJURY_PENALTIES,
            self.keys.ADP_SCORING,
            self.keys.PLAYER_RATING_SCORING,
            self.keys.TEAM_QUALITY_SCORING,
            self.keys.PERFORMANCE_SCORING,
            self.keys.MATCHUP_SCORING,
            self.keys.DRAFT_ORDER_BONUSES,
            self.keys.DRAFT_ORDER,
            self.keys.MAX_POSITIONS,
            self.keys.FLEX_ELIGIBLE_POSITIONS,
        ]

        missing_params = [p for p in required_params if p not in self.parameters]
        if missing_params:
            raise ValueError(
                f"Config missing required parameters: {', '.join(missing_params)}"
            )

        self.current_nfl_week = self.parameters[self.keys.CURRENT_NFL_WEEK]
        self.nfl_season = self.parameters[self.keys.NFL_SEASON]
        self.nfl_scoring_format = self.parameters[self.keys.NFL_SCORING_FORMAT]
        self.normalization_max_scale = self.parameters[self.keys.NORMALIZATION_MAX_SCALE]
        self.draft_normalization_max_scale = self.parameters[self.keys.DRAFT_NORMALIZATION_MAX_SCALE]
        self.logger.debug(f"Loaded DRAFT_NORMALIZATION_MAX_SCALE: {self.draft_normalization_max_scale}")
        self.same_pos_bye_weight = self.parameters[self.keys.SAME_POS_BYE_WEIGHT]
        self.diff_pos_bye_weight = self.parameters[self.keys.DIFF_POS_BYE_WEIGHT]
        self.injury_penalties = self.parameters[self.keys.INJURY_PENALTIES]
        self.adp_scoring = self.parameters[self.keys.ADP_SCORING]
        self.player_rating_scoring = self.parameters[self.keys.PLAYER_RATING_SCORING]
        self.team_quality_scoring = self.parameters[self.keys.TEAM_QUALITY_SCORING]
        self.performance_scoring = self.parameters[self.keys.PERFORMANCE_SCORING]
        self.consistency_scoring = self.parameters.get(self.keys.CONSISTENCY_SCORING, self.performance_scoring)
        self.matchup_scoring = self.parameters[self.keys.MATCHUP_SCORING]

        self.schedule_scoring = self.parameters.get(self.keys.SCHEDULE_SCORING, {
            "THRESHOLDS": {"VERY_POOR": 8, "POOR": 12, "GOOD": 20, "EXCELLENT": 24},
            "MULTIPLIERS": {"EXCELLENT": 1.0, "GOOD": 1.0, "POOR": 1.0, "VERY_POOR": 1.0},
            "WEIGHT": 0.0
        })

        if 'IMPACT_SCALE' not in self.matchup_scoring:
            raise ValueError("MATCHUP_SCORING missing required parameter: IMPACT_SCALE")
        if 'IMPACT_SCALE' not in self.schedule_scoring:
            raise ValueError("SCHEDULE_SCORING missing required parameter: IMPACT_SCALE")

        self.temperature_scoring = self.parameters.get(self.keys.TEMPERATURE_SCORING, {
            "IDEAL_TEMPERATURE": 60,
            "IMPACT_SCALE": 50.0,
            "THRESHOLDS": {
                "BASE_POSITION": 0,
                "DIRECTION": "DECREASING",
                "STEPS": 10
            },
            "MULTIPLIERS": {
                "VERY_POOR": 0.95,
                "POOR": 0.975,
                "GOOD": 1.025,
                "EXCELLENT": 1.05
            },
            "WEIGHT": 0.0
        })

        self.wind_scoring = self.parameters.get(self.keys.WIND_SCORING, {
            "IMPACT_SCALE": 60.0,
            "THRESHOLDS": {
                "BASE_POSITION": 0,
                "DIRECTION": "DECREASING",
                "STEPS": 8
            },
            "MULTIPLIERS": {
                "VERY_POOR": 0.95,
                "POOR": 0.975,
                "GOOD": 1.025,
                "EXCELLENT": 1.05
            },
            "WEIGHT": 0.0
        })

        self.location_modifiers = self.parameters.get(self.keys.LOCATION_MODIFIERS, {
            "HOME": 0.0,
            "AWAY": 0.0,
            "INTERNATIONAL": 0.0
        })

        self.draft_order_bonuses = self.parameters[self.keys.DRAFT_ORDER_BONUSES]
        self.draft_order = self.parameters[self.keys.DRAFT_ORDER]

        self.max_positions = self.parameters[self.keys.MAX_POSITIONS]
        self.flex_eligible_positions = self.parameters[self.keys.FLEX_ELIGIBLE_POSITIONS]

        self.nfl_team_penalty = self.parameters.get(
            self.keys.NFL_TEAM_PENALTY, []
        )
        self.nfl_team_penalty_weight = self.parameters.get(
            self.keys.NFL_TEAM_PENALTY_WEIGHT, 1.0
        )

        trade_sim_section = self.parameters.get(self.keys.TRADE_SIMULATOR, {}) or {}

        self.trade_waivers_two_for_two = trade_sim_section.get(self.keys.TRADE_WAIVERS_TWO_FOR_TWO, False)
        self.trade_waivers_three_for_three = trade_sim_section.get(self.keys.TRADE_WAIVERS_THREE_FOR_THREE, False)
        self.trade_enable_one_for_one = trade_sim_section.get(self.keys.TRADE_ENABLE_ONE_FOR_ONE, False)
        self.trade_enable_two_for_two = trade_sim_section.get(self.keys.TRADE_ENABLE_TWO_FOR_TWO, True)
        self.trade_enable_three_for_three = trade_sim_section.get(self.keys.TRADE_ENABLE_THREE_FOR_THREE, True)
        self.trade_enable_two_for_one = trade_sim_section.get(self.keys.TRADE_ENABLE_TWO_FOR_ONE, True)
        self.trade_enable_one_for_two = trade_sim_section.get(self.keys.TRADE_ENABLE_ONE_FOR_TWO, True)
        self.trade_enable_three_for_one = trade_sim_section.get(self.keys.TRADE_ENABLE_THREE_FOR_ONE, False)
        self.trade_enable_one_for_three = trade_sim_section.get(self.keys.TRADE_ENABLE_ONE_FOR_THREE, False)
        self.trade_enable_three_for_two = trade_sim_section.get(self.keys.TRADE_ENABLE_THREE_FOR_TWO, True)
        self.trade_enable_two_for_three = trade_sim_section.get(self.keys.TRADE_ENABLE_TWO_FOR_THREE, True)
        self.trade_max_combinations = trade_sim_section.get(self.keys.TRADE_MAX_COMBINATIONS, 50000)

        trade_flag_attrs = [
            "trade_waivers_two_for_two", "trade_waivers_three_for_three",
            "trade_enable_one_for_one", "trade_enable_two_for_two", "trade_enable_three_for_three",
            "trade_enable_two_for_one", "trade_enable_one_for_two",
            "trade_enable_three_for_one", "trade_enable_one_for_three",
            "trade_enable_three_for_two", "trade_enable_two_for_three",
        ]
        for attr in trade_flag_attrs:
            if not isinstance(getattr(self, attr), bool):
                raise ValueError(
                    f"TRADE_SIMULATOR.{attr.replace('trade_', '').upper()} must be a boolean, "
                    f"got {getattr(self, attr)!r}"
                )

        if (
            not isinstance(self.trade_max_combinations, int)
            or isinstance(self.trade_max_combinations, bool)
            or self.trade_max_combinations <= 0
        ):
            raise ValueError(
                f"TRADE_SIMULATOR.MAX_COMBINATIONS must be a positive integer, "
                f"got {self.trade_max_combinations!r}"
            )

        if not isinstance(self.nfl_team_penalty, list):
            raise ValueError(
                f"NFL_TEAM_PENALTY must be a list, got {type(self.nfl_team_penalty).__name__}"
            )

        invalid_teams = [
            team for team in self.nfl_team_penalty
            if team not in ALL_NFL_TEAMS
        ]
        if invalid_teams:
            raise ValueError(
                f"NFL_TEAM_PENALTY contains invalid team abbreviations: {', '.join(invalid_teams)}. "
                f"Valid teams: {', '.join(ALL_NFL_TEAMS)}"
            )

        if not isinstance(self.nfl_team_penalty_weight, (int, float)):
            raise ValueError(
                f"NFL_TEAM_PENALTY_WEIGHT must be a number (int or float), "
                f"got {type(self.nfl_team_penalty_weight).__name__}"
            )

        if not (0.0 <= self.nfl_team_penalty_weight <= 1.0):
            raise ValueError(
                f"NFL_TEAM_PENALTY_WEIGHT must be between 0.0 and 1.0 (inclusive), "
                f"got {self.nfl_team_penalty_weight}"
            )

        self.max_search_results = self.parameters.get(self.keys.MAX_SEARCH_RESULTS, 15)

        if (
            not isinstance(self.max_search_results, int)
            or isinstance(self.max_search_results, bool)
            or self.max_search_results <= 0
        ):
            raise ValueError(
                f"MAX_SEARCH_RESULTS must be a positive integer, "
                f"got {self.max_search_results!r}"
            )

        required_injury_levels = [self.keys.INJURY_LOW, self.keys.INJURY_MEDIUM, self.keys.INJURY_HIGH]
        missing_levels = [
            level for level in required_injury_levels
            if level not in self.injury_penalties
        ]
        if missing_levels:
            raise ValueError(
                f"INJURY_PENALTIES missing levels: {', '.join(missing_levels)}"
            )

        required_bonus_types = [self.keys.BONUS_PRIMARY, self.keys.BONUS_SECONDARY]
        missing_bonus_types = [
            bonus_type for bonus_type in required_bonus_types
            if bonus_type not in self.draft_order_bonuses
        ]
        if missing_bonus_types:
            raise ValueError(
                f"DRAFT_ORDER_BONUSES missing types: {', '.join(missing_bonus_types)}"
            )

        if not isinstance(self.draft_order, list):
            raise ValueError("DRAFT_ORDER must be a list")

        required_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']
        missing_positions = [pos for pos in required_positions if pos not in self.max_positions]
        if missing_positions:
            error_msg = f"MAX_POSITIONS missing required positions: {', '.join(missing_positions)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        for pos, limit in self.max_positions.items():
            if not isinstance(limit, int) or limit <= 0:
                error_msg = f"MAX_POSITIONS[{pos}] must be a positive integer, got: {limit} (type: {type(limit).__name__})"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

        self.logger.debug(f"MAX_POSITIONS validated: {sum(self.max_positions.values())} total roster spots")

        if not isinstance(self.flex_eligible_positions, list):
            error_msg = f"FLEX_ELIGIBLE_POSITIONS must be a list, got: {type(self.flex_eligible_positions).__name__}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        if len(self.flex_eligible_positions) == 0:
            error_msg = "FLEX_ELIGIBLE_POSITIONS must contain at least one position"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        if 'FLEX' in self.flex_eligible_positions:
            error_msg = "FLEX_ELIGIBLE_POSITIONS cannot contain 'FLEX' (circular reference)"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        invalid_positions = [pos for pos in self.flex_eligible_positions if pos not in valid_positions]
        if invalid_positions:
            error_msg = f"FLEX_ELIGIBLE_POSITIONS contains invalid positions: {', '.join(invalid_positions)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.logger.debug(f"FLEX_ELIGIBLE_POSITIONS validated: {', '.join(self.flex_eligible_positions)}")

        for scoring_type in [self.keys.ADP_SCORING, self.keys.PLAYER_RATING_SCORING,
                             self.keys.TEAM_QUALITY_SCORING, self.keys.PERFORMANCE_SCORING,
                             self.keys.MATCHUP_SCORING, self.keys.SCHEDULE_SCORING,
                             self.keys.TEMPERATURE_SCORING, self.keys.WIND_SCORING]:
            if scoring_type not in self.parameters:
                continue

            scoring_dict = self.parameters[scoring_type]
            thresholds_config = scoring_dict[self.keys.THRESHOLDS]

            if self.keys.BASE_POSITION in thresholds_config:
                calculated = self.calculate_thresholds(
                    thresholds_config[self.keys.BASE_POSITION],
                    thresholds_config[self.keys.DIRECTION],
                    thresholds_config[self.keys.STEPS],
                    scoring_type
                )

                thresholds_config[self.keys.VERY_POOR] = calculated[self.keys.VERY_POOR]
                thresholds_config[self.keys.POOR] = calculated[self.keys.POOR]
                thresholds_config[self.keys.GOOD] = calculated[self.keys.GOOD]
                thresholds_config[self.keys.EXCELLENT] = calculated[self.keys.EXCELLENT]

                self.logger.debug(f"{scoring_type} thresholds calculated: E={calculated[self.keys.EXCELLENT]}, "
                                 f"G={calculated[self.keys.GOOD]}, P={calculated[self.keys.POOR]}, "
                                 f"VP={calculated[self.keys.VERY_POOR]}")


    def _get_multiplier(self, scoring_dict : Dict[str, Any], val, rising_thresholds=True) -> Tuple[float, str]:
        """
        Get multiplier based on threshold logic.

        Args:
            scoring_dict: Dictionary with THRESHOLDS and MULTIPLIERS
            val: Value to evaluate
            rising_thresholds: True if higher values are better (e.g., player rating)
                              False if lower values are better (e.g., ADP, team rank)

        Returns:
            float: Multiplier value

        Logic:
            rising_thresholds=True (higher is better):
                - val >= EXCELLENT threshold → EXCELLENT multiplier
                - val >= GOOD threshold → GOOD multiplier
                - GOOD > val > POOR → neutral (1.0)
                - val <= POOR threshold → POOR multiplier
                - val <= VERY_POOR threshold → VERY_POOR multiplier

            rising_thresholds=False (lower is better):
                - val <= EXCELLENT threshold → EXCELLENT multiplier
                - val <= GOOD threshold → GOOD multiplier
                - GOOD < val < POOR → neutral (1.0)
                - val >= POOR threshold → POOR multiplier
                - val >= VERY_POOR threshold → VERY_POOR multiplier
        """
        if val == None:
            self.logger.debug(f"Multiplier calculation received None value, returning NEUTRAL (1.0)")
            multiplier, label = 1.0, self.keys.NEUTRAL

        elif rising_thresholds:


            if val >= scoring_dict[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT], self.keys.EXCELLENT
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.GOOD]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD], self.keys.GOOD
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR], self.keys.VERY_POOR
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.POOR]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR], self.keys.POOR
            else:
                multiplier, label = 1.0, self.keys.NEUTRAL
        else:


            if val <= scoring_dict[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT], self.keys.EXCELLENT
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.GOOD]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD], self.keys.GOOD
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR], self.keys.VERY_POOR
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.POOR]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR], self.keys.POOR
            else:
                multiplier, label = 1.0, self.keys.NEUTRAL

        multiplier = multiplier ** scoring_dict[self.keys.WEIGHT]
        return multiplier, label


    def __repr__(self) -> str:
        """String representation of the config manager."""
        return (
            f"ConfigManager("
            f"week={self.current_nfl_week}, "
            f"season={self.nfl_season}, "
            f"format='{self.nfl_scoring_format}')"
        )


