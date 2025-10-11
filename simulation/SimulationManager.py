
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
HUMAN_ERROR_RATE = 0.2              # chance of suboptimal pick
SUBOPTIMAL_CHOICE_POOL = 5          # Pick from top 5 instead of #1
TEAM_STRATEGIES = {         # Team strategy distribution
    'adp_aggressive': 2,
    'projected_points_agressive': 2,
    'adp_with_draft_order': 2,
    'projected_points_with_draft_order': 3,
    'draft_helper': 1 
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



    # Init the AddToDraftModeManager, StarterHelperModeManager, and all the simulated teams
    # Generate the config set and pick one to run with
    # Randomly determine draft order then run the draft in a snake draft order
    # Run through the 17 weeks of the fantasy league, compiling the win rate of the DraftHelper team
    # Compare the win rate to the previously completed sims then start another one
    # After all configs run through all their sims, output the most optimal config to the simulated_configs folder
    # Restart with the optimal config