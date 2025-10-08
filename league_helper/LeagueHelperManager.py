#!/usr/bin/env python3
"""
League Helper Manager

Main entry point for the League Helper application.

Author: Kai Mizuno
"""

from pathlib import Path
from util.LeagueConfigManager import LeagueConfigManager
from util.PlayerManager import PlayerManager
from add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager
from drop_player_mode.DropPlayerModeManager import DropPlayerModeManager
from lock_player_mode.LockPlayerModeManager import LockPlayerModeManager
from mark_drafted_player_mode.MarkDraftedPlayerModeManager import MarkDraftedPlayerModeManager
from starter_helper_mode.StarterHelperModeManager import StarterHelperModeManager
from trade_simulator_mode.TradeSimulatorModeManager import TradeSimulatorModeManager
from waiver_optimizer_mode.WaiverOptimizerModeManager import WaiverOptimizerModeManager

class LeagueHelperManager:

    def __init__(self, data_folder : Path, config_folder : Path):
        self.league_config_manager = LeagueConfigManager(config_folder)

        self.player_manager = PlayerManager(data_folder)

        self.add_to_roster_mode_manager = AddToRosterModeManager(config_folder)
        self.drop_player_mode_manager = DropPlayerModeManager()
        self.lock_player_mode_manager = LockPlayerModeManager()
        self.mark_drafted_player_mode_manager = MarkDraftedPlayerModeManager()
        self.starter_helper_mode_manager = StarterHelperModeManager(config_folder)
        self.trade_simulator_mode_manager = TradeSimulatorModeManager()
        self.waiver_optimizer_mode_manager = WaiverOptimizerModeManager(config_folder)


    def start_interactive_mode(self):
        pass




def main():
    
    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"
    config_path = base_path / "config"

    leagueHelper = LeagueHelperManager(data_path, config_path)
    leagueHelper.start_interactive_mode()


if __name__ == "__main__":
    main()
