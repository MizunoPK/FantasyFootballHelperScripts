
import csv
from pathlib import Path

import sys

from league_helper.util import FantasyTeam
sys.path.append(str(Path(__file__).parent))
import constants as Constants
from ConfigManager import ConfigManager

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class PlayerManager:

    def __init__(self, data_folder : Path, config : ConfigManager):
        self.logger = get_logger()
        self.config = config

        self.file_str = str(data_folder / 'players.csv')
        
        self.load_players_from_csv()
        self.load_team()


    def load_players_from_csv(self):
        """
        Load players from CSV file using the new FantasyPlayer class.
        
        This function now supports the new projection data format with fantasy_points
        and can fall back to the legacy format if needed.
        """
        players = []
        max_projection = 0.0
        required_columns = ['id', 'name', 'team', 'position']
        
        try:
            with open(self.file_str, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Validate required columns exist
                if not all(col in reader.fieldnames for col in required_columns):
                    missing_cols = [col for col in required_columns if col not in reader.fieldnames]
                    raise ValueError(f"Missing required columns in CSV: {missing_cols}")
                
                row_count = 0
                error_count = 0
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
                    row_count += 1
                    try:
                        # Use FantasyPlayer.from_dict for proper field handling including locked
                        player = FantasyPlayer.from_dict(row)
                        
                        # Validate player data
                        if not player.name:
                            self.logger.warning(f"Warning: Empty player name on row {row_num}, skipping")
                            error_count += 1
                            continue
                        
                        if player.position not in Constants.MAX_POSITIONS:
                            self.logger.warning(f"Warning: Invalid position '{player.position}' for player {player.name} on row {row_num}, skipping")
                            error_count += 1
                            continue
                        
                        players.append(player)
                        
                        # Track max projection for normalization
                        if player.fantasy_points and player.fantasy_points > max_projection:
                            max_projection = player.fantasy_points
                    
                    except Exception as e:
                        error_count += 1
                        self.logger.error(f"Error parsing row {row_num} for player {row.get('name', 'Unknown')}: {e}")
                        continue
                
                if error_count > 0:
                    self.logger.warning(f"Warning: {error_count} rows had errors and were skipped out of {row_count} total rows")
                        
        except FileNotFoundError:
            self.logger.error(f"Error: File {self.file_str} not found.")
            return []
        except PermissionError:
            self.logger.error(f"Error: Permission denied accessing file {self.file_str}")
            return []
        except csv.Error as e:
            self.logger.error(f"Error: Invalid CSV format in file {self.file_str}: {e}")
            return []
        except ValueError as e:
            self.logger.error(f"Error: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error loading CSV file {self.file_str}: {e}")
            return []
        
        # Add computed properties needed by draft helper
        for player in players:
            
            # Calculate weighted_projection (normalized between 0-100)
            # Note: This property is deprecated and not actively used - actual normalization
            # happens in NormalizationCalculator using param_manager values
            if player.fantasy_points and max_projection > 0:
                player.weighted_projection = (player.fantasy_points / max_projection) * 100.0  # Default scale
            else:
                player.weighted_projection = 0.0
                
            # Initialize draft helper specific properties if not already set
            if not hasattr(player, 'is_starter'):
                player.is_starter = False  # To be set when added to FantasyTeam
        
        self.logger.info(f"Loaded {len(players)} players from {self.file_str}.")

        self.players = players
    

    def load_team(self):
        """
        Load the current team from the player data
        it will be players marked as drafted=2
        """
        drafted_players = [p for p in self.players if p.drafted == 2]
        self.team = FantasyTeam(drafted_players)
    

    def reload_player_data(self):
        """
        Reload player data from CSV file and refresh team roster
        This is called before each main menu display to ensure data is up-to-date
        """
        try:
            self.logger.info("Reloading player data from CSV file")

            # Store current roster size for comparison
            old_roster_size = len(self.team.roster)

            # Reload players from CSV
            self.load_players_from_csv()

            # Reload team with updated data
            self.load_team()

            # Log changes if any
            new_roster_size = len(self.team.roster)
            if old_roster_size != new_roster_size:
                self.logger.info(f"Roster size changed: {old_roster_size} -> {new_roster_size}")
                print(f"Player data reloaded. Roster updated: {old_roster_size} -> {new_roster_size} players")
            else:
                self.logger.debug(f"Player data reloaded. Roster size unchanged: {new_roster_size} players")

        except Exception as e:
            self.logger.error(f"Error reloading player data: {e}")
            print(f"Warning: Could not reload player data from {self.players_csv}: {e}")


    def get_roster_len(self):
        return len(self.team.roster)
    

    def display_roster_by_draft_order(self):
        """Display current roster organized by assigned slots in draft order"""
        print(f"\nCurrent Roster by Position:")
        print("-" * 40)

        # Create a map from player ID to player object for quick lookup
        player_map = {player.id: player for player in self.team.roster}

        # Display each position based on slot assignments (not original position)
        for pos in Constants.MAX_POSITIONS.keys():
            max_count = Constants.MAX_POSITIONS[pos]

            # Get players assigned to this slot (using slot_assignments, not position filtering)
            assigned_player_ids = self.team.slot_assignments.get(pos, [])
            assigned_players = [player_map[pid] for pid in assigned_player_ids if pid in player_map]
            current_count = len(assigned_players)

            print(f"\n{pos} ({current_count}/{max_count}):")
            if assigned_players:
                # Sort by fantasy points (highest first) for display
                sorted_players = sorted(assigned_players, key=lambda p: p.fantasy_points, reverse=True)
                for i, player in enumerate(sorted_players, 1):
                    locked_indicator = " (LOCKED)" if getattr(player, 'locked', False) else ""
                    print(f"  {pos}{i}: {player.name} ({player.team}) - {player.fantasy_points:.1f} pts{locked_indicator}")
            else:
                print(f"  (No {pos} players)")

        print(f"\nTotal roster: {len(self.team.roster)}/{Constants.MAX_PLAYERS} players")


    def score_player(self, p, injury=True, bye=True, draft_order=False, adp=True, player_rating=True, team_quality=True, matchup=False, consistency=True):
        """
        Calculate score for a player (8-step calculation).

        New Scoring System:
        1. Get normalized seasonal fantasy points (0-N scale)
        2. Apply ADP multiplier
        3. Apply Player Ranking multiplier
        4. Apply Team ranking multiplier
        5. Apply Consistency multiplier (CV-based volatility scoring)
        6. Apply Matchup multiplier
        7. Add DRAFT_ORDER bonus (round-based position priority)
        8. Subtract Bye Week penalty
        9. Subtract Injury penalty

        Returns:
            float: Total score for the player
        """
        # STEP 1: Normalize seasonal fantasy points to 0-N scale
        player_score = self._get_normalized_fantasy_points(p)
        self.logger.debug(f"Step 1 - Normalized score for {p.name}: {player_score:.2f}")

        # STEP 2: Apply ADP multiplier
        if (adp):
            player_score = self._apply_adp_multiplier(p, player_score)
            self.logger.debug(f"Step 2 - ADP Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 3: Apply Player Rating multiplier
        if (player_rating):
            player_score = self._apply_player_rating_multiplier(p, player_score)
            self.logger.debug(f"Step 3 - Player Rating Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 4: Apply Team Quality multiplier
        if (team_quality):
            player_score = self._apply_team_quality_multiplier(p, player_score)
            self.logger.debug(f"Step 4 - Team Quality Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 5: Apply Consistency multiplier (CV-based volatility scoring)
        if (consistency):
            player_score = self._apply_consistency_scoring(p, player_score)

            self.logger.debug(f"Step 5 - After consistency for {p.name}: {player_score:.2f}")

        # STEP 6: Apply Matchup multiplier
        if (matchup):
            player_score = self._apply_matchup_multiplier(p, player_score)

            self.logger.debug(f"Step 6 - After matchup multiplier for {p.name}: {player_score:.2f}")

        # STEP 7: Add DRAFT_ORDER bonus (round-based position priority)
        if (draft_order):
            player_score = self._apply_draft_order_bonus(p, player_score)
            self.logger.debug(f"Step 7 - After DRAFT_ORDER bonus for {p.name}: {player_score:.2f}")

        # STEP 8: Subtract Bye Week penalty
        if (bye):
            player_score = self._apply_bye_penalty_for_player(p, player_score)
            self.logger.debug(f"Step 8 - After bye penalty for {p.name}: {player_score:.2f}")

        # STEP 9: Subtract Injury penalty
        if (injury):
            player_score = self.apply_injury_penalty(p, player_score)
            self.logger.debug(f"Step 9 - Final score for {p.name}: {player_score:.2f}")

        # Summary logging
        self.logger.info(
            f"Scoring for {p.name}: final_score={player_score:.1f}"
        )

        return player_score
    
    def _get_normalized_fantasy_points(self, p):
        pass
