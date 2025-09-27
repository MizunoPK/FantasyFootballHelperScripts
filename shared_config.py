#!/usr/bin/env python3
"""
Shared Configuration for Fantasy Football Helper Scripts

This file contains only the truly shared constants that are used across multiple scripts.
Script-specific constants have been moved to individual config.py files in each script folder.

Configuration Files:
- player-data-fetcher/config.py - Player data fetcher specific settings
- nfl-scores-fetcher/config.py - NFL scores fetcher specific settings  
- draft_helper/config.py - Draft helper specific settings
- config.py (this file) - Shared constants only

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

# =============================================================================
# SHARED NFL SEASON VARIABLES
# =============================================================================

# NFL Season and Week Configuration (CRITICAL - UPDATE WEEKLY)
CURRENT_NFL_WEEK = 4      # Current NFL week (1-18, update weekly)
NFL_SEASON = 2025        # Current NFL season year
NFL_SCORING_FORMAT = "ppr"  # Fantasy scoring format: "ppr", "std", or "half"

# =============================================================================
# SHARED DATA PATHS
# =============================================================================

# Shared data file location - used by all scripts
PLAYERS_CSV = 'shared_files/players.csv'

# =============================================================================
# DATA FILE MANAGEMENT
# =============================================================================

# Default file caps for each data folder (maximum number of files per type)
DEFAULT_FILE_CAPS = {
    'csv': 5,      # Maximum CSV files to keep
    'json': 5,     # Maximum JSON files to keep
    'xlsx': 5,     # Maximum Excel files to keep
    'txt': 5       # Maximum text files to keep
}

# Module-specific file caps (override DEFAULT_FILE_CAPS if needed)
MODULE_SPECIFIC_CAPS = {
    # Example: 'player-data-fetcher': {'csv': 10, 'json': 10, 'xlsx': 10}
    # Uncomment and modify if specific modules need different caps
}

# File cap enforcement settings
ENABLE_FILE_CAPS = True        # Set to False to disable file cap enforcement entirely
DRY_RUN_MODE = False          # Set to True to log what would be deleted without actual deletion

# =============================================================================
# CONFIGURATION GUIDE
# =============================================================================
"""
🎯 CONFIG FILE ORGANIZATION:

SHARED SETTINGS (this file - MOST CRITICAL):
- CURRENT_NFL_WEEK: Update every Tuesday for the upcoming week (1-18)
- NFL_SEASON: Current NFL season year (update annually)
- NFL_SCORING_FORMAT: Fantasy scoring format ("ppr", "std", or "half")
- PLAYERS_CSV: Shared data file path used by all scripts
- DEFAULT_FILE_CAPS: Maximum files to keep per type (default: 5 each)
- ENABLE_FILE_CAPS: Enable/disable automatic file cleanup (default: True)

SCRIPT-SPECIFIC SETTINGS:
- player-data-fetcher/config.py: ESPN API settings, projection settings, output formats
- nfl-scores-fetcher/config.py: NFL API settings, export options
- draft_helper/config.py: Draft strategy, roster limits, trade settings
- starter_helper/config.py: Lineup requirements, display options

🔧 HOW TO MODIFY SETTINGS:

For Weekly Updates (MOST IMPORTANT):
→ Edit CURRENT_NFL_WEEK in shared_config.py (this file)

For Season Updates:
→ Edit NFL_SEASON and NFL_SCORING_FORMAT in shared_config.py (this file)

For Player Data Changes:
→ Edit player-data-fetcher/player_data_fetcher_config.py

For NFL Scores Changes:
→ Edit nfl-scores-fetcher/nfl_scores_fetcher_config.py

For Draft Strategy Changes:
→ Edit draft_helper/draft_helper_config.py

For Lineup Settings:
→ Edit starter_helper/starter_helper_config.py

⚠️ VALIDATION:
The shared variables in this file are used by all scripts. Validation is performed
by each individual script that imports these values.

📁 CENTRALIZATION COMPLETE:
Core NFL season/week variables are now centralized for consistency across all scripts.
Weekly updates now require changing only ONE location instead of multiple files.
"""
