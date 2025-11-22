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

import sys
sys.path.append(str(Path(__file__).parent.parent))
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent.parent))
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

    # Top Level Keys
    CONFIG_NAME = "config_name"
    DESCRIPTION = "description"
    PARAMETERS = "parameters"

    # Parameter Keys
    CURRENT_NFL_WEEK = "CURRENT_NFL_WEEK"
    NFL_SEASON = "NFL_SEASON"
    NFL_SCORING_FORMAT = "NFL_SCORING_FORMAT"
    NORMALIZATION_MAX_SCALE = "NORMALIZATION_MAX_SCALE"
    SAME_POS_BYE_WEIGHT = "SAME_POS_BYE_WEIGHT"
    DIFF_POS_BYE_WEIGHT = "DIFF_POS_BYE_WEIGHT"
    INJURY_PENALTIES = "INJURY_PENALTIES"
    ADP_SCORING = "ADP_SCORING"
    PLAYER_RATING_SCORING = "PLAYER_RATING_SCORING"
    TEAM_QUALITY_SCORING = "TEAM_QUALITY_SCORING"
    CONSISTENCY_SCORING = "CONSISTENCY_SCORING"  # Deprecated - kept for backwards compatibility
    PERFORMANCE_SCORING = "PERFORMANCE_SCORING"
    MATCHUP_SCORING = "MATCHUP_SCORING"
    SCHEDULE_SCORING = "SCHEDULE_SCORING"
    DRAFT_ORDER_BONUSES = "DRAFT_ORDER_BONUSES"
    DRAFT_ORDER = "DRAFT_ORDER"
    MAX_POSITIONS = "MAX_POSITIONS"
    FLEX_ELIGIBLE_POSITIONS = "FLEX_ELIGIBLE_POSITIONS"

    # Draft Order scoring
    DRAFT_ORDER_PRIMARY_LABEL = "P"
    DRAFT_ORDER_SECONDARY_LABEL = "S"

    # Nested Structure Keys
    MULTIPLIERS = "MULTIPLIERS"
    THRESHOLDS = "THRESHOLDS"
    MIN_WEEKS = "MIN_WEEKS"
    WEIGHT = "WEIGHT"

    # Injury Level Keys
    INJURY_LOW = "LOW"
    INJURY_MEDIUM = "MEDIUM"
    INJURY_HIGH = "HIGH"

    # Bonus Type Keys
    BONUS_PRIMARY = "PRIMARY"
    BONUS_SECONDARY = "SECONDARY"

    # Threshold/Multiplier Level Keys
    VERY_POOR = "VERY_POOR"
    POOR = "POOR"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"
    NEUTRAL = "NEUTRAL"

    # Parameterized Threshold Keys (new system)
    BASE_POSITION = "BASE_POSITION"
    DIRECTION = "DIRECTION"
    STEPS = "STEPS"

    # Direction Values
    DIRECTION_INCREASING = "INCREASING"
    DIRECTION_DECREASING = "DECREASING"
    DIRECTION_BI_EXCELLENT_HI = "BI_EXCELLENT_HI"
    DIRECTION_BI_EXCELLENT_LOW = "BI_EXCELLENT_LOW"

    # Optional calculated field (for transparency in config files)
    CALCULATED = "_calculated"


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
        >>> draft_bonus = config.get_draft_order_bonus("RB", 1)  # RB in round 1 → returns bonus
    """

    # ============================================================================
    # INITIALIZATION
    # ============================================================================

    def __init__(self, data_folder: Path) -> None:
        """
        Initialize the config manager and load configuration.

        Args:
            data_folder (Path): Path to the data directory containing league_config.json

        Raises:
            FileNotFoundError: If league_config.json is not found
            ValueError: If configuration structure is invalid or missing required fields
        """
        self.keys = ConfigKeys()
        self.config_name: str = ""
        self.description: str = ""
        self.parameters: Dict[str, Any] = {}
        self.logger = get_logger()

        # Set config path to data/league_config.json
        self.config_path = data_folder / 'league_config.json'

        # League settings
        self.current_nfl_week: int = 0
        self.nfl_season: int = 0
        self.nfl_scoring_format: str = ""

        # Scoring parameters
        self.normalization_max_scale: float = 0.0
        self.same_pos_bye_weight: float = 0.0
        self.diff_pos_bye_weight: float = 0.0
        self.injury_penalties: Dict[str, float] = {}
        self.adp_scoring: Dict[str, Any] = {}
        self.player_rating_scoring: Dict[str, Any] = {}
        self.team_quality_scoring: Dict[str, Any] = {}
        self.consistency_scoring: Dict[str, Any] = {}  # Deprecated - kept for backwards compatibility
        self.performance_scoring: Dict[str, Any] = {}
        self.matchup_scoring: Dict[str, Any] = {}

        # Add to Roster mode settings
        self.draft_order_bonuses: Dict[str, float] = {}
        self.draft_order: List[Dict[str, str]] = []

        # Roster construction limits
        self.max_positions: Dict[str, int] = {}
        self.flex_eligible_positions: List[str] = []

        # Threshold calculation cache
        self._threshold_cache: Dict[Tuple[str, float, str, float], Dict[str, float]] = {}

        self._load_config()

    # ============================================================================
    # PUBLIC CONFIGURATION ACCESS
    # ============================================================================

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

    # ============================================================================
    # PUBLIC MULTIPLIER GETTERS
    # ============================================================================

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
            rising_thresholds=True  # Higher rank = better schedule
        )

    def get_performance_multiplier(self, deviation: float) -> Tuple[float, str]:
        return self._get_multiplier(self.performance_scoring, deviation)

    # ============================================================================
    # PUBLIC MIN_WEEKS GETTERS
    # ============================================================================

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

    # ============================================================================
    # PUBLIC BONUS/PENALTY GETTERS
    # ============================================================================

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
            Round 1 strategy: {"RB": "P", "WR": "S"}
            - get_draft_order_bonus("RB", 1) → (10.0, "PRIMARY")
            - get_draft_order_bonus("WR", 1) → (5.0, "SECONDARY")
            - get_draft_order_bonus("QB", 1) → (0, "")
        """
        # Convert position to FLEX-aware format
        # For example, RB/WR might be labeled as FLEX in later rounds
        position_with_flex = self.get_position_with_flex(position)

        # Get the ideal positions for this draft round
        # This is a dictionary like {"RB": "P", "WR": "S", "FLEX": "P"}
        ideal_positions = self.draft_order[draft_round]

        # Check if this position is listed in the draft strategy for this round
        if position_with_flex in ideal_positions:
            # Get the priority label: "P" (PRIMARY) or "S" (SECONDARY)
            priority = ideal_positions.get(position_with_flex)

            if priority == self.keys.DRAFT_ORDER_PRIMARY_LABEL:
                # This is a PRIMARY position for this round (highest bonus)
                # Example: RB in round 1-2, QB in round 3
                return self.draft_order_bonuses[self.keys.BONUS_PRIMARY], self.keys.BONUS_PRIMARY
            else:
                # This is a SECONDARY position for this round (smaller bonus)
                # Example: WR in round 1 when RB is PRIMARY
                return self.draft_order_bonuses[self.keys.BONUS_SECONDARY], self.keys.BONUS_SECONDARY
        else:
            # Position is not listed in this round's strategy (no bonus)
            # Example: K or DST in early rounds
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
                # Collect valid weekly points (skip None and zeros)
                valid_weeks = [
                    points for week in range(1, 18)
                    if (points := getattr(player, f'week_{week}_points')) is not None
                    and points > 0
                ]

                if not valid_weeks:
                    self.logger.warning(f"No valid weekly data for {player.name}, using 0.0 median")
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

        # Calculate median totals for each list
        same_pos_median_total = sum(calculate_player_median(p) for p in same_pos_players)
        diff_pos_median_total = sum(calculate_player_median(p) for p in diff_pos_players)

        # Apply scaling
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
        # Look up penalty for the given risk level
        if risk_level in self.injury_penalties:
            return self.injury_penalties[risk_level]
        else:
            # Default to HIGH penalty if risk level is unrecognized
            # This is a conservative fallback to avoid drafting risky players
            return self.injury_penalties[self.keys.INJURY_HIGH]

    # ============================================================================
    # PUBLIC DRAFT POSITION GETTERS
    # ============================================================================

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
        # Check if round number is within the draft order list
        if round_num < len(self.draft_order):
            # Get the position with PRIMARY priority ("P") for this round
            # IMPORTANT: Use min() not max() because in ASCII/Unicode:
            # - 'P' (PRIMARY) = 80
            # - 'S' (SECONDARY) = 83
            # So 'P' < 'S', meaning min() returns the PRIMARY position
            best_position = min(self.draft_order[round_num], key=self.draft_order[round_num].get)
            return best_position

        # If round number is out of range (beyond defined strategy), default to FLEX
        # This allows flexible drafting in late rounds
        return 'FLEX'

    # ============================================================================
    # PUBLIC THRESHOLD UTILITIES
    # ============================================================================

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

        # STEPS must be positive
        if steps <= 0:
            self.logger.error(f"STEPS must be positive, got {steps}")
            raise ValueError(f"STEPS must be positive, got {steps}")

        # Must be finite
        if not math.isfinite(base_pos) or not math.isfinite(steps):
            self.logger.error("BASE_POSITION and STEPS must be finite")
            raise ValueError("BASE_POSITION and STEPS must be finite")

        # DIRECTION must be valid
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
        # Check cache first
        cache_key = (scoring_type, base_pos, direction, steps)
        if cache_key in self._threshold_cache:
            return self._threshold_cache[cache_key]

        # Validate parameters
        self.validate_threshold_params(base_pos, direction, steps)

        # Calculate thresholds based on direction
        if direction == self.keys.DIRECTION_INCREASING:
            # Higher values = better (e.g., player rating)
            # Formula: VP=base+1s, P=base+2s, G=base+3s, E=base+4s
            thresholds = {
                self.keys.VERY_POOR: base_pos + steps,
                self.keys.POOR: base_pos + (2 * steps),
                self.keys.GOOD: base_pos + (3 * steps),
                self.keys.EXCELLENT: base_pos + (4 * steps)
            }

        elif direction == self.keys.DIRECTION_DECREASING:
            # Lower values = better (e.g., ADP rank)
            # Formula: E=base+1s, G=base+2s, P=base+3s, VP=base+4s
            thresholds = {
                self.keys.EXCELLENT: base_pos + steps,
                self.keys.GOOD: base_pos + (2 * steps),
                self.keys.POOR: base_pos + (3 * steps),
                self.keys.VERY_POOR: base_pos + (4 * steps)
            }

        elif direction == self.keys.DIRECTION_BI_EXCELLENT_HI:
            # Bidirectional: positive deviation = excellent
            # Formula: VP=base-2s, P=base-1s, G=base+1s, E=base+2s (1x/2x multipliers per user Q4)
            thresholds = {
                self.keys.VERY_POOR: base_pos - (steps * 2),
                self.keys.POOR: base_pos - steps,
                self.keys.GOOD: base_pos + steps,
                self.keys.EXCELLENT: base_pos + (steps * 2)
            }

        elif direction == self.keys.DIRECTION_BI_EXCELLENT_LOW:
            # Bidirectional: negative deviation = excellent (rare case)
            # Formula: E=base-2s, G=base-1s, P=base+1s, VP=base+2s (1x/2x multipliers)
            thresholds = {
                self.keys.EXCELLENT: base_pos - (steps * 2),
                self.keys.GOOD: base_pos - steps,
                self.keys.POOR: base_pos + steps,
                self.keys.VERY_POOR: base_pos + (steps * 2)
            }

        else:
            # This should never happen due to validation, but included for safety
            raise ValueError(f"Invalid direction: {direction}")

        # Store in cache
        self._threshold_cache[cache_key] = thresholds
        return thresholds

    # ============================================================================
    # PRIVATE LOADING AND VALIDATION
    # ============================================================================

    def _load_config(self) -> None:
        """
        Load and validate configuration from JSON file.

        Reads league_config.json, validates its structure, extracts all parameters,
        and stores them in instance variables for type-safe access.

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
            self.logger.debug("Successfully loaded JSON configuration")
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            raise

        # Validate required fields
        self._validate_config_structure(data)

        # Store configuration data
        self.config_name = data.get(self.keys.CONFIG_NAME, "")
        self.description = data.get(self.keys.DESCRIPTION, "")
        self.parameters = data.get(self.keys.PARAMETERS, {})

        self.logger.debug(f"Loaded configuration: '{self.config_name}'")
        self.logger.debug(f"Description: {self.description}")
        self.logger.debug(f"Parameters count: {len(self.parameters)}")

        # Extract and validate all parameters
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

        self.logger.debug("Configuration structure validation passed")

    def _extract_parameters(self) -> None:
        """Extract and validate all parameters from the config."""
        # Required parameters
        required_params = [
            self.keys.CURRENT_NFL_WEEK,
            self.keys.NFL_SEASON,
            self.keys.NFL_SCORING_FORMAT,
            self.keys.NORMALIZATION_MAX_SCALE,
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

        # Extract league-wide parameters
        self.current_nfl_week = self.parameters[self.keys.CURRENT_NFL_WEEK]
        self.nfl_season = self.parameters[self.keys.NFL_SEASON]
        self.nfl_scoring_format = self.parameters[self.keys.NFL_SCORING_FORMAT]
        self.normalization_max_scale = self.parameters[self.keys.NORMALIZATION_MAX_SCALE]
        self.same_pos_bye_weight = self.parameters[self.keys.SAME_POS_BYE_WEIGHT]
        self.diff_pos_bye_weight = self.parameters[self.keys.DIFF_POS_BYE_WEIGHT]
        self.injury_penalties = self.parameters[self.keys.INJURY_PENALTIES]
        self.adp_scoring = self.parameters[self.keys.ADP_SCORING]
        self.player_rating_scoring = self.parameters[self.keys.PLAYER_RATING_SCORING]
        self.team_quality_scoring = self.parameters[self.keys.TEAM_QUALITY_SCORING]
        self.performance_scoring = self.parameters[self.keys.PERFORMANCE_SCORING]
        # Keep consistency_scoring as fallback for backwards compatibility
        self.consistency_scoring = self.parameters.get(self.keys.CONSISTENCY_SCORING, self.performance_scoring)
        self.matchup_scoring = self.parameters[self.keys.MATCHUP_SCORING]

        # Schedule scoring is optional (for backward compatibility)
        # Default to matchup_scoring structure if not present
        self.schedule_scoring = self.parameters.get(self.keys.SCHEDULE_SCORING, {
            "THRESHOLDS": {"VERY_POOR": 8, "POOR": 12, "GOOD": 20, "EXCELLENT": 24},
            "MULTIPLIERS": {"EXCELLENT": 1.0, "GOOD": 1.0, "POOR": 1.0, "VERY_POOR": 1.0},
            "WEIGHT": 0.0  # Weight 0 = disabled by default
        })

        # Validate IMPACT_SCALE is present (required as of additive scoring)
        if 'IMPACT_SCALE' not in self.matchup_scoring:
            raise ValueError("MATCHUP_SCORING missing required parameter: IMPACT_SCALE")
        if 'IMPACT_SCALE' not in self.schedule_scoring:
            raise ValueError("SCHEDULE_SCORING missing required parameter: IMPACT_SCALE")

        # Extract Add to Roster mode parameters
        self.draft_order_bonuses = self.parameters[self.keys.DRAFT_ORDER_BONUSES]
        self.draft_order = self.parameters[self.keys.DRAFT_ORDER]

        # Extract roster construction limits
        self.max_positions = self.parameters[self.keys.MAX_POSITIONS]
        self.flex_eligible_positions = self.parameters[self.keys.FLEX_ELIGIBLE_POSITIONS]

        # Extract Starter Helper mode parameters (optional - not in current config)
        # Note: matchup_multipliers are accessed directly from matchup_scoring[self.keys.MULTIPLIERS]

        # Validate injury penalties structure
        required_injury_levels = [self.keys.INJURY_LOW, self.keys.INJURY_MEDIUM, self.keys.INJURY_HIGH]
        missing_levels = [
            level for level in required_injury_levels
            if level not in self.injury_penalties
        ]
        if missing_levels:
            raise ValueError(
                f"INJURY_PENALTIES missing levels: {', '.join(missing_levels)}"
            )

        # Validate draft order bonuses structure
        required_bonus_types = [self.keys.BONUS_PRIMARY, self.keys.BONUS_SECONDARY]
        missing_bonus_types = [
            bonus_type for bonus_type in required_bonus_types
            if bonus_type not in self.draft_order_bonuses
        ]
        if missing_bonus_types:
            raise ValueError(
                f"DRAFT_ORDER_BONUSES missing types: {', '.join(missing_bonus_types)}"
            )

        # Validate draft order is a list
        if not isinstance(self.draft_order, list):
            raise ValueError("DRAFT_ORDER must be a list")

        # Validate MAX_POSITIONS structure (strict validation)
        required_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']
        missing_positions = [pos for pos in required_positions if pos not in self.max_positions]
        if missing_positions:
            error_msg = f"MAX_POSITIONS missing required positions: {', '.join(missing_positions)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # Validate all values are positive integers
        for pos, limit in self.max_positions.items():
            if not isinstance(limit, int) or limit <= 0:
                error_msg = f"MAX_POSITIONS[{pos}] must be a positive integer, got: {limit} (type: {type(limit).__name__})"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

        # Log successful validation
        self.logger.debug(f"MAX_POSITIONS validated: {sum(self.max_positions.values())} total roster spots")

        # Validate FLEX_ELIGIBLE_POSITIONS structure
        if not isinstance(self.flex_eligible_positions, list):
            error_msg = f"FLEX_ELIGIBLE_POSITIONS must be a list, got: {type(self.flex_eligible_positions).__name__}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        if len(self.flex_eligible_positions) == 0:
            error_msg = "FLEX_ELIGIBLE_POSITIONS must contain at least one position"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # Validate no circular reference (FLEX can't be in FLEX_ELIGIBLE_POSITIONS)
        if 'FLEX' in self.flex_eligible_positions:
            error_msg = "FLEX_ELIGIBLE_POSITIONS cannot contain 'FLEX' (circular reference)"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # Validate all positions are valid
        valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        invalid_positions = [pos for pos in self.flex_eligible_positions if pos not in valid_positions]
        if invalid_positions:
            error_msg = f"FLEX_ELIGIBLE_POSITIONS contains invalid positions: {', '.join(invalid_positions)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # Log successful validation
        self.logger.debug(f"FLEX_ELIGIBLE_POSITIONS validated: {', '.join(self.flex_eligible_positions)}")

        # Pre-calculate parameterized thresholds if needed (backward compatible)
        # Skip CONSISTENCY_SCORING as it's deprecated
        for scoring_type in [self.keys.ADP_SCORING, self.keys.PLAYER_RATING_SCORING,
                             self.keys.TEAM_QUALITY_SCORING, self.keys.PERFORMANCE_SCORING,
                             self.keys.MATCHUP_SCORING, self.keys.SCHEDULE_SCORING]:
            # Skip if scoring type not in config (e.g., SCHEDULE_SCORING is optional)
            if scoring_type not in self.parameters:
                continue

            scoring_dict = self.parameters[scoring_type]
            thresholds_config = scoring_dict[self.keys.THRESHOLDS]

            # Check if parameterized (new format with BASE_POSITION, DIRECTION, STEPS)
            if self.keys.BASE_POSITION in thresholds_config:
                # Calculate thresholds from parameters
                calculated = self.calculate_thresholds(
                    thresholds_config[self.keys.BASE_POSITION],
                    thresholds_config[self.keys.DIRECTION],
                    thresholds_config[self.keys.STEPS],
                    scoring_type
                )

                # Add calculated values to thresholds dict for direct access
                # This maintains backward compatibility - existing code can continue
                # to access thresholds_config[VERY_POOR], etc.
                thresholds_config[self.keys.VERY_POOR] = calculated[self.keys.VERY_POOR]
                thresholds_config[self.keys.POOR] = calculated[self.keys.POOR]
                thresholds_config[self.keys.GOOD] = calculated[self.keys.GOOD]
                thresholds_config[self.keys.EXCELLENT] = calculated[self.keys.EXCELLENT]

                self.logger.debug(f"{scoring_type} thresholds calculated: E={calculated[self.keys.EXCELLENT]}, "
                                 f"G={calculated[self.keys.GOOD]}, P={calculated[self.keys.POOR]}, "
                                 f"VP={calculated[self.keys.VERY_POOR]}")

    # ============================================================================
    # PRIVATE MULTIPLIER CALCULATION
    # ============================================================================

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
        # Handle None values - return neutral multiplier (1.0) when data is unavailable
        # This prevents crashes when player data is incomplete
        if val == None:
            self.logger.debug(f"Multiplier calculation received None value, returning NEUTRAL (1.0)")
            multiplier, label = 1.0, self.keys.NEUTRAL

        elif rising_thresholds:
            # RISING THRESHOLDS: Higher values are better
            # Examples: player rating (80+ = excellent), performance deviation (+20% = excellent)

            # Check thresholds from best to worst to find the appropriate multiplier
            # The order is important: EXCELLENT → GOOD → (neutral) → POOR → VERY_POOR

            if val >= scoring_dict[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
                # Value exceeds EXCELLENT threshold (e.g., player rating >= 80)
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT], self.keys.EXCELLENT
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.GOOD]:
                # Value exceeds GOOD threshold but not EXCELLENT (e.g., 60 <= rating < 80)
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD], self.keys.GOOD
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
                # Value is below VERY_POOR threshold (e.g., rating <= 20)
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR], self.keys.VERY_POOR
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.POOR]:
                # Value is below POOR threshold but above VERY_POOR (e.g., 20 < rating <= 40)
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR], self.keys.POOR
            else:
                # Value is in the neutral zone between POOR and GOOD thresholds
                # No adjustment applied (1.0x multiplier)
                multiplier, label = 1.0, self.keys.NEUTRAL
        else:
            # DECREASING THRESHOLDS: Lower values are better
            # Examples: ADP (20 or less = excellent), team rank (1-10 = excellent)

            # Check thresholds from best to worst
            # The comparison operators are reversed compared to rising_thresholds

            if val <= scoring_dict[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
                # Value is below EXCELLENT threshold (e.g., ADP <= 20, rank <= 10)
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT], self.keys.EXCELLENT
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.GOOD]:
                # Value is below GOOD threshold but above EXCELLENT (e.g., 20 < ADP <= 50)
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD], self.keys.GOOD
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
                # Value exceeds VERY_POOR threshold (e.g., ADP >= 150, rank >= 25)
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR], self.keys.VERY_POOR
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.POOR]:
                # Value exceeds POOR threshold but below VERY_POOR (e.g., 100 <= ADP < 150)
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR], self.keys.POOR
            else:
                # Value is in the neutral zone between GOOD and POOR thresholds
                # No adjustment applied (1.0x multiplier)
                multiplier, label = 1.0, self.keys.NEUTRAL

        # Apply weight exponent to the multiplier
        # Weight > 1 amplifies the multiplier effect (e.g., 1.05^2 = 1.1025)
        # Weight < 1 dampens the multiplier effect (e.g., 1.05^0.5 = 1.0247)
        # This allows fine-tuning of how much each factor influences the final score
        multiplier = multiplier ** scoring_dict[self.keys.WEIGHT]
        return multiplier, label

    # ============================================================================
    # STRING REPRESENTATION
    # ============================================================================

    def __repr__(self) -> str:
        """String representation of the config manager."""
        return (
            f"ConfigManager("
            f"week={self.current_nfl_week}, "
            f"season={self.nfl_season}, "
            f"format='{self.nfl_scoring_format}')"
        )
