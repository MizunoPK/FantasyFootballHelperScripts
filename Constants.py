# Constants for Fantasy Football Helper Scripts
# This file contains constants used across the application

LOGGING_FILE = './data/log.txt'  # Log file path
LOGGING_ENABLED = False  # Enable or disable logging

# Constants for file paths
PLAYERS_CSV = './data/players.csv'
TEAM_CSV = './data/team.csv'

# Number of players to recommend
RECOMMENDATION_COUNT = 10

# Constants for player positions and their roles
RB, WR, QB, TE, K, DEF, FLEX, MATCH = 'RB', 'WR', 'QB', 'TE', 'K', 'DEF', 'FLEX', 'MATCH'

# Define max roster slots by position (draft limits)
MAX_POSITIONS = {
    QB: 2,
    RB: 3,
    WR: 3,
    FLEX: 1,  # FLEX can be RB or WR
    TE: 2,
    K: 2,
    DEF: 2,
}
MAX_PLAYERS = 15  # Total roster size

FLEX_ELIGIBLE_POSITIONS = [RB, WR]  # Positions eligible for FLEX spot

# Starting lineup requirements
STARTERS_REQ = {
    QB: 1,
    RB: 2,
    WR: 2,
    TE: 1,
    FLEX: 1,  # RB or WR
    K: 1,
    DEF: 1
}


# Ideal position drafting order
# Each dict represents a round, with position weights for that round
# Higher weight means higher priority to draft that position
# Example: In round 1, FLEX has weight 1.2, so it's prioritized
# In round 5, TE has weight 1.4 and FLEX 1.1
DRAFT_ORDER = [
    {FLEX: 1.0},
    {FLEX: 1.0},
    {FLEX: 1.0},
    {FLEX: 1.0},
    {TE: 1.0, FLEX: 0.6},
    {QB: 1.0, FLEX: 0.6},
    {FLEX: 1.0},
    {TE: 1.0, FLEX: 0.6},
    {QB: 1.0, FLEX: 0.6},
    {DEF: 1.0},
    {DEF: 1.0},
    {K: 1.0},
    {K: 1.0},
    {FLEX: 1.0},
    {FLEX: 1.0}
]
def get_ideal_draft_position(round):
    if round < len(DRAFT_ORDER):
        best_position = max(DRAFT_ORDER[round], key=DRAFT_ORDER[round].get)
        return best_position
    return FLEX


# SCORE WEIGHTS
POS_NEEDED_SCORE = 60  # Weight for positional need
ADP_BASE_SCORE = 100  # Base score for ADP, higher is better
PENALTY_INJURED = 50  # Penalty for injured players
# Weights for bye week penalties by position
BASE_BYE_PENALTY = 50  # Base penalty for any bye week conflict
STARTER_BYE_WEIGHTS = {
    RB: 2.0,
    WR: 2.0,
    QB: 1.5,
    TE: 1.3,
    K: 0.5,
    DEF: 0.5,
    MATCH: 6.0
}
BENCH_WEIGHT_FACTOR = 0.9

# The possible bye weeks for players
POSSIBLE_BYE_WEEKS = [5,6,7,8,9,10,11,12]

# Labels from data
HEALTHY = 'healthy'

