#!/usr/bin/env python3
"""
Runner Script for League Helper

This script runs the league helper from the parent directory.

Usage:
    python run_league_helper.py [--enable-log-file] [--week N]

Arguments:
    --enable-log-file    Enable file logging (logs written to logs/league_helper/)
    --week N             Override current NFL week for this session (in-memory only)

Author: Kai Mizuno
"""

from league_helper.LeagueHelperManager import main


if __name__ == "__main__":
    main()


