#!/usr/bin/env python3
"""
Runner Script for League Helper

This script runs the league helper from the parent directory.

Usage:
    python run_league_helper.py [--enable-log-file]

Arguments:
    --enable-log-file    Enable file logging (logs written to logs/league_helper/)

Author: Kai Mizuno
"""

from league_helper.LeagueHelperManager import main


if __name__ == "__main__":
    main()


