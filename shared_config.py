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
# SHARED DATA PATHS
# =============================================================================

# Shared data file location - used by all scripts
PLAYERS_CSV = 'shared_files/players.csv'

# =============================================================================
# CONFIGURATION GUIDE
# =============================================================================
"""
🎯 CONFIG FILE ORGANIZATION:

SCRIPT-SPECIFIC SETTINGS (most frequently modified):
- player-data-fetcher/config.py: ESPN API settings, fallback scoring, output formats
- nfl-scores-fetcher/config.py: NFL API settings, current week, season type
- draft_helper/config.py: Draft strategy, roster limits, scoring weights

SHARED SETTINGS (this file):
- PLAYERS_CSV: Shared data file path used by all scripts

🔧 HOW TO MODIFY SETTINGS:

For Player Data Changes:
→ Edit player-data-fetcher/config.py

For NFL Scores Changes:
→ Edit nfl-scores-fetcher/config.py

For Draft Strategy Changes:
→ Edit draft_helper/config.py

⚠️ VALIDATION:
Each script-specific config file has its own validation. No validation needed here
since this file only contains shared file paths.

📁 MIGRATION COMPLETE:
All frequently modified constants have been moved to script-specific config files.
This centralized approach makes it easier to modify settings for each script independently.
"""
