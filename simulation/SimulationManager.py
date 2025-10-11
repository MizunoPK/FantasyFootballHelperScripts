
# ------ SIMULATION CONFIG ------
NUMBER_OF_TEST_VALUES = 5  # Number of test values per parameter
NUMBER_OF_RUNS = 100
SIMULATIONS_PER_CONFIG = 100        # Number of drafts to run per configuration
MAX_PARALLEL_THREADS = 7            # Max concurrent threads for simulation
                                       # None = auto-detect: min(6, CPU_COUNT)
                                       # Integer = explicit thread count
                                       # Examples: 1, 4, 8, 12, None
DATA_FOLDER = "./sim_data"
CONFIGS_FOLDER = "./simulated_configs"


# ------ League settings ------
NFL_SEASON= 2024
LEAGUE_SIZE = 10                      # Number of teams in the draft
NFL_SEASON_WEEKS = 17                 # Full season simulation
HUMAN_ERROR_RATE = 0.5              # 50% chance of suboptimal pick
SUBOPTIMAL_CHOICE_POOL = 5          # Pick from top 5 instead of #1
TEAM_STRATEGIES = {         # Team strategy distribution
    'conservative': 2,      # 2 teams use conservative strategy
    'aggressive': 2,        # 2 teams use aggressive strategy
    'positional': 2,        # 2 teams use positional strategy
    'value': 3,             # 3 teams use value strategy
    'draft_helper': 1       # 1 team uses draft_helper logic
}

# ------ RANDOM GENERATION CONFIG -------
# First value in tuple is PARAMETER_RANGES - it specifies the range from the optimal value that the random values will be generated.
# The second and third values of the tuple are Absolute min/max bounds for each parameter (enforced regardless of PARAMETER_RANGES)
# These bounds ensure generated values stay within valid ranges.
# For example, POSITIVE_MULTIPLIER: (0.1, 1.0, 1.5) means generated values will never be < 1.0 or > 1.5, and the values will be within 0.1 of the most recently found optimal value
NORMALIZATION_MAX_SCALE =  (20, 60, 140)

BASE_BYE_PENALTY =  (10, 0, 40)

DRAFT_ORDER_PRIMARY_BONUS =  (20, 25, 100)
DRAFT_ORDER_SECONDARY_BONUS =  (20, 25, 75)

POSITIVE_MULTIPLIER =  (0.1, 1.0, 1.3)
NEGATIVE_MULTIPLIER =  (0.1, 0.7, 1.0)



class SimulationManager:

    def __init__(self):
        pass