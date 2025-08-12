PLAYERS_CSV = './data/players.csv'
TEAM_CSV = './data/team.csv'

RB, WR, QB, TE, K, DEF, FLEX, MATCH = 'RB', 'WR', 'QB', 'TE', 'K', 'DEF', 'FLEX', 'MATCH'

# Define max roster slots by position (draft limits)
MAX_POSITIONS = {
    QB: 2,
    RB: 5,
    WR: 5,
    TE: 2,
    K: 1,
    DEF: 1,
}
MAX_PLAYERS = 15  # Total roster size

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

# Weights for bye week penalties by position
STARTER_BYE_WEIGHTS = {
    RB: 100,
    WR: 100,
    FLEX: 60,
    QB: 40,
    TE: 60,
    K: 20,
    DEF: 20,
    MATCH: 500
}

# Bench weights as a fraction of starter weights
BENCH_WEIGHT_FACTOR = 0.5

# SCORE WEIGHTS
STARTER_POS_NEEDED_SCORE = 1000  # Weight for positional need in starters
BENCH_POS_NEEDED_SCORE = 100  # Weight for positional need in bench
ADP_BASE_SCORE = 100  # Base score for ADP, higher is better
PENALTY_INJURED = 50  # Penalty for injured players
PENALTY_BYE = 100  # Penalty for bye week conflicts

# The possible bye weeks for players
POSSIBLE_BYE_WEEKS = [5,6,7,8,9,10,11,12]

# Labels from data
HEALTHY = 'healthy'

