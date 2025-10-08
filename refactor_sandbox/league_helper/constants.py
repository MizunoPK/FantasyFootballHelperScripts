
LOGGING_LEVEL = 'INFO'      # ← DEBUG, INFO, WARNING, ERROR, CRITICAL (WARNING+ to reduce spam)
LOGGING_TO_FILE = False        # ← Console vs file logging
LOG_NAME = "league_helper"
LOGGING_FILE = './data/log.txt'
LOGGING_FORMAT = 'standard'     # detailed / standard / simple

# Position Constants
RB, WR, QB, TE, K, DST, FLEX = 'RB', 'WR', 'QB', 'TE', 'K', 'DST', 'FLEX'

# Roster Construction
MAX_POSITIONS = {
    QB: 2,      
    RB: 4,      
    WR: 4,     
    FLEX: 1,   
    TE: 2,     
    K: 1,  
    DST: 1,
}

# Total roster size
MAX_PLAYERS = 15  

# Positions eligible for FLEX spot
FLEX_ELIGIBLE_POSITIONS = [RB, WR]  

# Bye weeks for NFL season
POSSIBLE_BYE_WEEKS = [5, 6, 7, 8, 9, 10, 11, 12, 14]

# Starting Lineup Requirements (Start 7 Fantasy League)
STARTING_LINEUP_REQUIREMENTS = {
    QB: 1,      # 1 Quarterback
    RB: 2,      # 2 Running Backs
    WR: 2,      # 2 Wide Receivers
    TE: 1,      # 1 Tight End
    FLEX: 1,    # 1 FLEX (Wide Receiver OR Running Back)
    K: 1,       # 1 Kicker
    DST: 1,     # 1 Defense/Special Teams
}

# Positions eligible for matchup multipliers
MATCHUP_ENABLED_POSITIONS = [QB, RB, WR, TE]