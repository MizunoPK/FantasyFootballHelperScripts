import csv
import sys
import logging
import asyncio
import os
from pathlib import Path
from datetime import datetime
from io import StringIO

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from .FantasyTeam import FantasyTeam
    from . import draft_helper_constants as Constants
    from .team_data_loader import TeamDataLoader
    from .core.menu_system import MenuSystem
    from .core.player_search import PlayerSearch
    from .core.roster_manager import RosterManager
    from .core.trade_analyzer import TradeAnalyzer
    from .core.scoring_engine import ScoringEngine
    from .core.trade_simulator import TradeSimulator
except ImportError:
    # Fallback to absolute imports when run directly
    from FantasyTeam import FantasyTeam
    import draft_helper_constants as Constants
    from team_data_loader import TeamDataLoader
    from core.menu_system import MenuSystem
    from core.player_search import PlayerSearch
    from core.roster_manager import RosterManager
    from core.trade_analyzer import TradeAnalyzer
    from core.scoring_engine import ScoringEngine
    from core.trade_simulator import TradeSimulator

from shared_files.FantasyPlayer import FantasyPlayer
from shared_files.enhanced_scoring import EnhancedScoringCalculator
from shared_files.positional_ranking_calculator import PositionalRankingCalculator
from shared_files.parameter_json_manager import ParameterJsonManager

# Import starter helper components
sys.path.append(str(parent_dir / 'starter_helper'))
try:
    import pandas as pd
    from shared_files.configs.starter_helper_config import (
        CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT,
        SHOW_PROJECTION_DETAILS, SHOW_INJURY_STATUS,
        SAVE_OUTPUT_TO_FILE, get_timestamped_filepath, get_latest_filepath
    )
    from lineup_optimizer import LineupOptimizer, OptimalLineup, StartingRecommendation
    from starter_helper import StarterHelper
    STARTER_HELPER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Starter Helper functionality not available: {e}")
    STARTER_HELPER_AVAILABLE = False


def setup_logging():
    """Setup logging configuration based on constants"""
    if not Constants.LOGGING_ENABLED:
        # Disable logging completely by setting to CRITICAL+1 (higher than any standard level)
        logging.basicConfig(level=logging.CRITICAL + 1)
        return logging.getLogger(__name__)
    
    # Map string levels to logging constants
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    log_level = level_map.get(Constants.LOGGING_LEVEL.upper(), logging.INFO)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if Constants.LOGGING_TO_FILE:
        # Log to file
        logging.basicConfig(
            level=log_level,
            format=log_format,
            filename=Constants.LOGGING_FILE,
            filemode='a'
        )
    else:
        # Log to console
        logging.basicConfig(
            level=log_level,
            format=log_format
        )
    
    return logging.getLogger(__name__)


def load_players_from_csv(filename):
    """
    Load players from CSV file using the new FantasyPlayer class.
    
    This function now supports the new projection data format with fantasy_points
    and can fall back to the legacy format if needed.
    """
    players = []
    max_projection = 0.0
    required_columns = ['id', 'name', 'team', 'position']
    
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
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
                        print(f"Warning: Empty player name on row {row_num}, skipping")
                        error_count += 1
                        continue
                    
                    if player.position not in Constants.MAX_POSITIONS:
                        print(f"Warning: Invalid position '{player.position}' for player {player.name} on row {row_num}, skipping")
                        error_count += 1
                        continue
                    
                    players.append(player)
                    
                    # Track max projection for normalization
                    if player.fantasy_points and player.fantasy_points > max_projection:
                        max_projection = player.fantasy_points
                
                except Exception as e:
                    error_count += 1
                    print(f"Error parsing row {row_num} for player {row.get('name', 'Unknown')}: {e}")
                    continue
            
            if error_count > 0:
                print(f"Warning: {error_count} rows had errors and were skipped out of {row_count} total rows")
                    
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied accessing file {filename}")
        return []
    except csv.Error as e:
        print(f"Error: Invalid CSV format in file {filename}: {e}")
        return []
    except ValueError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error loading CSV file {filename}: {e}")
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
    
    print(f"Loaded {len(players)} players from {filename}.")
    return players


class DraftHelper:
    """
    DraftHelper class to manage the drafting process, including player recommendations
    based on team needs, player ADP, and bye week considerations.
    """

    def __init__(self, players_csv=Constants.PLAYERS_CSV, parameter_json_path=None):
        """
        Initialize the DraftHelper with players and team data.
        Loads players from the specified CSV files.

        Args:
            players_csv: Path to players CSV file
            parameter_json_path: Path to parameter JSON file (required)
        """
        self.logger = logging.getLogger(__name__)
        self.players_csv = players_csv

        # Initialize parameter manager (required)
        if parameter_json_path is None:
            raise ValueError("parameter_json_path is required")
        self.param_manager = ParameterJsonManager(parameter_json_path)
        self.logger.info(f"Loaded parameters: {self.param_manager.config_name}")

        self.players = load_players_from_csv(players_csv)
        self.team = self.load_team()

        # Initialize enhanced scoring calculator
        self.enhanced_scorer = EnhancedScoringCalculator()

        # Initialize team data loader for offensive/defensive rankings
        self.team_data_loader = TeamDataLoader()

        # Initialize positional ranking calculator for matchup analysis
        self.positional_ranking_calculator = None
        try:
            # Try to initialize with current week team data
            from shared_files.configs.shared_config import CURRENT_NFL_WEEK
            current_week = CURRENT_NFL_WEEK

            # Try current week first
            teams_file_path = f"data/teams_week_{current_week}.csv"
            full_teams_path = Path(__file__).parent / "simulation" / teams_file_path

            # If current week doesn't exist, try to find the nearest available week
            if not full_teams_path.exists():
                # Try weeks from current to 18
                for week in range(current_week, 19):
                    teams_file_path = f"data/teams_week_{week}.csv"
                    full_teams_path = Path(__file__).parent / "simulation" / teams_file_path
                    if full_teams_path.exists():
                        self.logger.info(f"Using week {week} team data (current week {current_week} not available)")
                        break
                else:
                    # Try week 0 as fallback
                    teams_file_path = f"data/teams_week_0.csv"
                    full_teams_path = Path(__file__).parent / "simulation" / teams_file_path
                    if full_teams_path.exists():
                        week = 0
                        self.logger.info(f"Using week 0 team data as fallback")
                    else:
                        full_teams_path = None

            if full_teams_path and full_teams_path.exists():
                self.positional_ranking_calculator = PositionalRankingCalculator(teams_file_path=str(full_teams_path))
                self.logger.info(f"Positional ranking calculator initialized with week {week if 'week' in locals() else current_week} data")
                print(f"Positional ranking calculator loaded for week {week if 'week' in locals() else current_week}.")
            else:
                self.logger.warning(f"No team data files found in simulation/data/")
                print("Warning: Positional ranking data not available.")
        except Exception as e:
            self.logger.error(f"Failed to initialize positional ranking calculator: {e}")
            print(f"Warning: Could not load positional ranking calculator: {e}")

        # Initialize menu system
        self.menu_system = MenuSystem(self.team, STARTER_HELPER_AVAILABLE, self)

        # Initialize player search system
        self.player_search = PlayerSearch(self.players, self.logger)

        # Initialize roster manager
        self.roster_manager = RosterManager(self.team, self.logger)

        # Initialize trade analyzer
        self.trade_analyzer = TradeAnalyzer(self.team, self.logger)

        # Initialize scoring engine with parameter manager
        self.scoring_engine = ScoringEngine(self.team, self.players, self.logger, self.param_manager)

        self.logger.info(f"DraftHelper initialized with {len(self.players)} players and team of {len(self.team.roster)} drafted players")
        if self.team_data_loader.is_team_data_available():
            self.logger.info(f"Team rankings loaded for {len(self.team_data_loader.get_available_teams())} teams")
            print(f"Team rankings loaded for {len(self.team_data_loader.get_available_teams())} teams.")
        else:
            self.logger.warning("Team rankings not available - enhanced scoring will use default values")
            print("Warning: Team rankings not available - enhanced scoring will use default values.")

        print(f"DraftHelper initialized with {len(self.players)} players and team of {len(self.team.roster)} drafted players.")

    def _match_players_to_rounds(self):
        """Legacy method for compatibility - delegates to RosterManager"""
        return self.roster_manager._match_players_to_rounds()

    def _calculate_round_fit_score(self, player, round_num, ideal_position):
        """Legacy method for compatibility - delegates to RosterManager"""
        return self.roster_manager._calculate_round_fit_score(player, round_num, ideal_position)

    def load_team(self):
        """
        Load the current team from the player data
        it will be players marked as drafted=2
        """
        drafted_players = [p for p in self.players if p.drafted == 2]
        return FantasyTeam(drafted_players)

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
            self.players = load_players_from_csv(self.players_csv)

            # Reload team with updated data
            self.team = self.load_team()

            # Update player search with new players list
            self.player_search.players = self.players

            # Update roster manager with new team data
            self.roster_manager.team = self.team

            # Update trade analyzer with new team data
            self.trade_analyzer.team = self.team

            # Update scoring engine with new team and players data
            self.scoring_engine.team = self.team
            self.scoring_engine.players = self.players

            # Update menu system with new team data
            self.menu_system.team = self.team

            new_roster_size = len(self.team.roster)

            # Log changes if any
            if old_roster_size != new_roster_size:
                self.logger.info(f"Roster size changed: {old_roster_size} -> {new_roster_size}")
                print(f"Player data reloaded. Roster updated: {old_roster_size} -> {new_roster_size} players")
            else:
                self.logger.debug(f"Player data reloaded. Roster size unchanged: {new_roster_size} players")

        except Exception as e:
            self.logger.error(f"Error reloading player data: {e}")
            print(f"Warning: Could not reload player data from {self.players_csv}: {e}")


    """        
    Function to score a player based on various factors:
    - Team position needs vs roster max and starters requirements
    - Projected Points
    - Bye week conflicts with current starters and bench
    - Injury status
    - Returns a score that can be used to rank players for drafting.
    """
    def score_player(self, p):
        """
        Calculate the total score for a player based on positional need, projections, penalties, and bonuses
        """
        return self.scoring_engine.score_player(
            p,
            enhanced_scorer=self.enhanced_scorer,
            team_data_loader=self.team_data_loader,
            positional_ranking_calculator=self.positional_ranking_calculator
        )
    

    # Function to recommend the next players to draft based on team needs
    # This considers:
    # - Team position needs vs roster max and starters requirements
    # - Player ADP (lower better)
    # - Injury status (only healthy)
    # - Avoid players already drafted
    # - Avoid bye week stacking (warn or deprioritize)
    # - Returns a list of recommended players sorted by score
    def recommend_next_picks(self):
        self.logger.debug("recommend_next_picks called")
        # get a list of available players that can be drafted
        available_players = [
            p for p in self.players
            if self.team.can_draft(p)
        ]

        # Score each player based on team needs and bye week conflicts
        for p in available_players:
            p.score = self.score_player(p)

        # Sort available players by score descending
        ranked_players = sorted(available_players, key=lambda x: x.score, reverse=True)

        # Return top recommended players
        self.logger.info(f"Recommended next picks: {[p.name for p in ranked_players[:Constants.RECOMMENDATION_COUNT]]}")
        return ranked_players[:Constants.RECOMMENDATION_COUNT]

    # Function to save the drafted team to the players CSV file by marking drafted=2
    # This eliminates the need for a separate team.csv file
    def save_team(self):
        self.logger.debug("save_team called")
        # Team is already saved by updating drafted status in players data
        # No separate team file needed - drafted players are marked with drafted=2
        self.logger.info(f"Team updated with {len(self.team.roster)} players marked as drafted")

    # Function to save the available players to a CSV file
    # This allows the user to keep track of the available players after drafting
    def save_players(self):
        self.logger.debug("save_players called")
        # Sort players by drafted value (ascending: 0=available, 1=drafted by others, 2=drafted by us)
        sorted_players = sorted(self.players, key=lambda p: p.drafted)

        # Use complete field list from player data fetcher to preserve all enhanced scoring columns
        fieldnames = [
            'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
            'injury_status', 'drafted', 'locked', 'average_draft_position',
            'player_rating',
            # Weekly projections (weeks 1-17 fantasy regular season only)
            'week_1_points', 'week_2_points', 'week_3_points', 'week_4_points',
            'week_5_points', 'week_6_points', 'week_7_points', 'week_8_points',
            'week_9_points', 'week_10_points', 'week_11_points', 'week_12_points',
            'week_13_points', 'week_14_points', 'week_15_points', 'week_16_points',
            'week_17_points'
        ]

        # Save sorted players to CSV
        with open(self.players_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in sorted_players:
                # Only include fields that are in fieldnames to avoid DictWriter errors
                player_dict = p.to_dict()
                filtered_dict = {key: player_dict.get(key, None) for key in fieldnames}
                writer.writerow(filtered_dict)
        self.logger.info(f"Available players saved with {len(self.players)} players (sorted by drafted status, all enhanced columns preserved)")

    # Function to get the user's choice of player to draft
    # This displays the top recommended players and prompts the user to select one
    def get_user_player_choice(self, simulation=False):
        self.logger.debug(f"get_user_player_choice called (simulation={simulation})")
        print("\nTop draft recommendations based on your current roster:")
        # Get the top 5 recommended players based on current team needs
        recommendations = self.recommend_next_picks()
        for i, p in enumerate(recommendations, start=1):
            print(f"{i}. {p}")

        # Prompt user to draft a player or quit
        if not simulation:
            choice = input("\nEnter the number of the player to draft, or 'quit' to exit: ").strip()
        else:
            choice = '1'
        if choice.lower() == 'quit':
            self.logger.info("User chose to quit drafting")
            return None
        if not choice.isdigit():
            print("Invalid input. Please enter a number or 'quit'.")
            self.logger.warning(f"Invalid input received: {choice}")
            return None

        index = int(choice) - 1
        if index < 0 or index >= len(recommendations):
            print("Number out of range.")
            self.logger.warning(f"User input out of range: {choice}")
            return None

        # Draft the selected player and update the team
        player_to_draft = recommendations[index]
        success = self.team.draft_player(player_to_draft)
        if not success:
            print(f"Failed to draft {player_to_draft.name}.")
            self.logger.error(f"Failed to draft player: {player_to_draft.name}")
            return None
        self.logger.info(f"Player drafted: {player_to_draft.name} (ID: {player_to_draft.id})")
        return player_to_draft


    # Interactive Menu System Methods
    async def run_interactive_draft(self):
        """Run the interactive draft helper with main menu"""
        print("Welcome to the Start 7 Fantasy League Draft Helper!")
        print(f"Currently drafted players: {len(self.team.roster)} / {Constants.MAX_PLAYERS} max")

        # Show initial roster status
        self.display_roster_by_draft_order()

        self.logger.info(f"Interactive draft started. Current roster size: {len(self.team.roster)}")

        while True:
            # Reload player data from CSV before showing menu to ensure latest changes
            self.reload_player_data()

            choice = self.show_main_menu()
            if choice == 1:
                self.run_add_to_roster_mode()
            elif choice == 2:
                self.run_mark_drafted_player_mode()
            elif choice == 3:
                self.run_trade_analysis_mode()
            elif choice == 4:
                self.run_drop_player_mode()
            elif choice == 5:
                self.run_lock_unlock_player_mode()
            elif choice == 6:
                if STARTER_HELPER_AVAILABLE:
                    await self.run_starter_helper_mode()
                else:
                    self.run_trade_simulator_mode()
            elif choice == 7:
                if STARTER_HELPER_AVAILABLE:
                    self.run_trade_simulator_mode()
                else:
                    print("Goodbye!")
                    self.logger.info("User exited interactive draft")
                    break
            elif choice == 8:
                if STARTER_HELPER_AVAILABLE:
                    print("Goodbye!")
                    self.logger.info("User exited interactive draft")
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("Invalid choice. Please try again.")

    def show_main_menu(self):
        """Display main menu and get user choice"""
        return self.menu_system.show_main_menu()

    def display_roster_by_draft_order(self):
        """Display current roster organized by assigned slots in draft order"""
        return self.roster_manager.display_roster_by_draft_order()

    def display_roster_by_draft_rounds(self):
        """Display current roster organized by draft round order based on DRAFT_ORDER config"""
        return self.roster_manager.display_roster_by_draft_rounds()


    def run_add_to_roster_mode(self):
        """Add to Roster Mode - shows recommendations and allows drafting to our team"""
        return self.roster_manager.run_add_to_roster_mode(
            recommend_next_picks_func=self.recommend_next_picks,
            save_players_func=self.save_players
        )

    def run_mark_drafted_player_mode(self):
        """Mark Drafted Player Mode - allows marking other players as drafted=1"""
        print("\n" + "="*50)
        print("MARK DRAFTED PLAYER MODE")
        print("="*50)
        print("Type 'exit' to return to Main Menu")

        try:
            self.search_and_mark_player()
        except Exception as e:
            print(f"Error: {e}")
            print("Returning to Main Menu...")
            self.logger.error(f"Error in mark drafted player mode: {e}")

    def search_and_mark_player(self):
        """Search for player by name and mark as drafted"""
        return self.player_search.search_and_mark_player_interactive(self.save_players)

    def run_trade_analysis_mode(self):
        """Waiver Optimizer Mode - run waiver optimizer to optimize current roster"""
        return self.trade_analyzer.run_trade_analysis_mode(
            add_basic_matchup_indicators_func=self.add_basic_matchup_indicators,
            run_trade_helper_func=self.run_trade_helper,
            save_players_func=self.save_players
        )

    def run_trade_simulator_mode(self):
        """Trade Simulator Mode - simulate trades without affecting actual roster data"""
        try:
            # Create trade simulator instance
            trade_simulator = TradeSimulator(
                team=self.team,
                all_players=self.players,
                scoring_function=self.score_player_for_trade,
                logger=self.logger
            )

            # Run the trade simulator
            trade_simulator.run_trade_simulator()

        except Exception as e:
            print(f"Error in trade simulator: {e}")
            self.logger.error(f"Error in trade simulator mode: {e}")
            input("\nPress Enter to return to Main Menu...")

    def run_drop_player_mode(self):
        """Drop Player Mode - allows removing players from roster (set drafted=0)"""
        print("\n" + "="*50)
        print("DROP PLAYER MODE")
        print("="*50)
        print("Type 'exit' to return to Main Menu")

        try:
            self.search_and_drop_player()
        except Exception as e:
            print(f"Error: {e}")
            print("Returning to Main Menu...")
            self.logger.error(f"Error in drop player mode: {e}")

    def search_and_drop_player(self):
        """Search for player by name and drop from roster (set drafted=0)"""
        def save_with_roster_update():
            """Custom save callback that handles team roster updates"""
            # The player_search module will have already set drafted=0
            # We need to find any players that were dropped and update team roster
            current_roster_players = [p for p in self.players if p.drafted == 2]

            # Rebuild team roster from current drafted=2 players
            self.team.roster = current_roster_players

            # Recalculate position counts
            self.team.pos_counts = {}
            for player in current_roster_players:
                if player.position in self.team.pos_counts:
                    self.team.pos_counts[player.position] += 1
                else:
                    self.team.pos_counts[player.position] = 1

            # Save to file
            self.save_players()

            # Show updated roster
            print(f"✓ Player has been dropped and is now available for draft.")
            self.display_roster_by_draft_order()

        return self.player_search.search_and_drop_player_interactive(save_with_roster_update)

    def run_lock_unlock_player_mode(self):
        """Lock/Unlock Player Mode - toggle lock status for roster players"""
        print("\n" + "="*50)
        print("LOCK/UNLOCK PLAYER MODE")
        print("="*50)

        while True:
            # Get roster players only (drafted=2)
            roster_players = [p for p in self.players if p.drafted == 2]

            if not roster_players:
                print("No players in your roster to lock/unlock.")
                input("\nPress Enter to return to Main Menu...")
                break

            # Group players by lock status
            unlocked_players = [p for p in roster_players if p.locked == 0]
            locked_players = [p for p in roster_players if p.locked == 1]

            print(f"\nYour Roster - Lock/Unlock Status:")
            print("-" * 40)

            # Display unlocked players
            print(f"\nUNLOCKED PLAYERS ({len(unlocked_players)}):")
            if unlocked_players:
                for i, player in enumerate(unlocked_players, 1):
                    print(f"  {i}. {player.name} ({player.position}, {player.team}) - {player.fantasy_points:.1f} pts")
            else:
                print("  (No unlocked players)")

            # Display locked players
            print(f"\nLOCKED PLAYERS ({len(locked_players)}):")
            if locked_players:
                for i, player in enumerate(locked_players, len(unlocked_players) + 1):
                    print(f"  {i}. {player.name} ({player.position}, {player.team}) - {player.fantasy_points:.1f} pts")
            else:
                print("  (No locked players)")

            total_players = len(roster_players)
            print(f"\n{total_players + 1}. Back to Main Menu")

            try:
                choice = int(input(f"\nSelect a player to toggle lock status (1-{total_players + 1}): ").strip())

                if 1 <= choice <= total_players:
                    # Player selected - toggle lock status
                    if choice <= len(unlocked_players):
                        selected_player = unlocked_players[choice - 1]
                        new_status = 1
                    else:
                        selected_player = locked_players[choice - len(unlocked_players) - 1]
                        new_status = 0

                    # Toggle lock status immediately (no confirmation)
                    selected_player.locked = new_status

                    # Save changes to CSV
                    self.save_players()

                    status_text = "🔒 LOCKED" if new_status == 1 else "🔓 UNLOCKED"
                    print(f"✓ {selected_player.name} is now {status_text}")

                    self.logger.info(f"Player lock status changed: {selected_player.name} (locked={new_status})")
                    # Continue the loop to show updated list

                elif choice == total_players + 1:
                    # Back to Main Menu
                    print("Returning to Main Menu...")
                    break
                else:
                    print("Invalid choice. Please try again.")

            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")
                print("Returning to Main Menu...")
                self.logger.error(f"Error in lock/unlock mode: {e}")
                break

    async def run_starter_helper_mode(self):
        """Starter Helper Mode - generate optimal starting lineup recommendations"""
        if not STARTER_HELPER_AVAILABLE:
            print("Error: Starter Helper functionality is not available")
            input("\nPress Enter to return to Main Menu...")
            return

        print("\n" + "="*60)
        print("STARTER HELPER MODE")
        print("="*60)

        try:
            # Convert roster to pandas DataFrame
            roster_data = []
            for player in self.players:
                if player.drafted == 2:  # Only roster players
                    # Include all weekly projection columns from FantasyPlayer
                    player_dict = {
                        'id': player.id,
                        'name': player.name,
                        'team': player.team,
                        'position': player.position,
                        'bye_week': player.bye_week,
                        'fantasy_points': player.fantasy_points,
                        'injury_status': player.injury_status,
                        'drafted': player.drafted,
                        'locked': player.locked
                    }

                    # Add weekly projection columns if available
                    for week in range(1, 18):
                        week_attr = f'week_{week}_points'
                        if hasattr(player, week_attr):
                            player_dict[week_attr] = getattr(player, week_attr)

                    roster_data.append(player_dict)

            if not roster_data:
                print("ERROR: No roster players found! Add players to your roster first.")
                input("\nPress Enter to return to Main Menu...")
                return

            roster_df = pd.DataFrame(roster_data)

            # Use StarterHelper's projection logic for consistency
            starter_helper = StarterHelper()
            projections = starter_helper.get_current_week_projections(roster_df)

            print(f"Fantasy Football Starter Helper")
            print(f"Week {CURRENT_NFL_WEEK} of {NFL_SEASON} NFL Season")
            print(f"Scoring Format: {NFL_SCORING_FORMAT.upper()}")
            print("="*60)
            print(f"Loaded {len(roster_df)} roster players")

            # Initialize lineup optimizer
            optimizer = LineupOptimizer()

            # Optimize lineup using projections
            optimal_lineup = optimizer.optimize_lineup(roster_df, projections)

            # Display optimal lineup
            self.display_starter_lineup(optimal_lineup)

            # Get used player IDs for bench recommendations
            used_player_ids = set()
            for starter in optimal_lineup.get_all_starters():
                if starter:
                    used_player_ids.add(starter.player_id)

            # Display bench recommendations
            bench_recs = optimizer.get_bench_recommendations(
                roster_df, projections, used_player_ids, count=5
            )
            self.display_bench_alternatives(bench_recs)

            # Save output to files
            if SAVE_OUTPUT_TO_FILE:
                output_content = self.generate_starter_output(optimal_lineup, bench_recs, roster_df, projections)
                self.save_starter_output_to_files(output_content)

            print(f"\nStarter recommendations complete for Week {CURRENT_NFL_WEEK}")
            print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"Error in starter helper: {str(e)}")
            self.logger.error(f"Error in starter helper mode: {str(e)}")

        # Wait for user acknowledgment before returning to menu
        input("\nPress Enter to return to Main Menu...")


    async def apply_matchup_analysis_to_all_players(self, matchup_analyzer):
        """Apply matchup analysis to all available players for trade analysis"""
        try:
            # Create player contexts for all players
            player_contexts = []
            for player in self.players:
                if player.drafted != 1:  # Include undrafted players and roster players
                    player_context = {
                        'id': str(player.id),
                        'name': player.name,
                        'position': player.position,
                        'team': player.team,
                        'team_id': self.get_team_id_for_analysis(player.team),
                        'injury_status': player.injury_status
                    }
                    player_contexts.append(player_context)

            # Perform analysis for all players
            analysis = await matchup_analyzer.analyze_weekly_matchups(player_contexts, CURRENT_NFL_WEEK)

            if analysis and hasattr(analysis, 'player_ratings'):
                # Apply matchup data back to player objects
                for player_rating in analysis.player_ratings:
                    player_name = player_rating.player_context.player_name

                    # Find matching player object
                    for player in self.players:
                        if player.name == player_name and player.drafted != 1:
                            # Set matchup indicator
                            from matchup_analyzer import MatchupAnalyzer
                            analyzer = MatchupAnalyzer()
                            player.matchup_indicator = analyzer.get_matchup_display_indicator(player_rating.rating)

                            # Set matchup adjustment
                            base_points = player.fantasy_points
                            adjusted_points = player_rating.adjusted_points or base_points
                            player.matchup_adjustment = adjusted_points - base_points
                            break

            return analysis
        except Exception as e:
            self.logger.error(f"Error applying matchup analysis to all players: {e}")
            return None

    def add_basic_matchup_indicators(self):
        """Add basic matchup indicators to players for trade analysis"""
        try:
            print("Adding matchup indicators for trade analysis...")

            # Simple heuristic: use fantasy points to determine matchup quality
            # This is a simplified approach until full matchup analysis can be integrated
            for player in self.players:
                if player.drafted != 1:  # Include undrafted and roster players
                    # Simple heuristic based on fantasy points relative to position average
                    position_players = [p for p in self.players if p.position == player.position and p.drafted != 1]

                    if position_players:
                        avg_points = sum(p.fantasy_points for p in position_players) / len(position_players)

                        # Set basic matchup indicators based on points relative to position average
                        points_ratio = player.fantasy_points / avg_points if avg_points > 0 else 1.0

                        if points_ratio >= 1.3:
                            player.matchup_indicator = "^"  # Great (was ★)
                            player.matchup_adjustment = 2.0
                        elif points_ratio >= 1.1:
                            player.matchup_indicator = "o"  # Good (was ○)
                            player.matchup_adjustment = 1.0
                        elif points_ratio >= 0.9:
                            player.matchup_indicator = ""   # Average
                            player.matchup_adjustment = 0.0
                        else:
                            player.matchup_indicator = "v"  # Poor (was ●)
                            player.matchup_adjustment = -1.0
                    else:
                        # Fallback if no position players found
                        player.matchup_indicator = ""
                        player.matchup_adjustment = 0.0

        except Exception as e:
            print(f"Warning: Could not add matchup indicators: {e}")
            self.logger.error(f"Error adding basic matchup indicators: {e}")

    def get_team_id_for_analysis(self, team_abbr):
        """Convert team abbreviation to team ID for matchup analysis"""
        # Same mapping as in starter_helper
        team_mapping = {
            'ATL': 1, 'BUF': 2, 'CHI': 3, 'CIN': 4, 'CLE': 5, 'DAL': 6, 'DEN': 7,
            'DET': 8, 'GB': 9, 'TEN': 10, 'IND': 11, 'KC': 12, 'LV': 13, 'LAC': 14,
            'LAR': 15, 'MIA': 16, 'MIN': 17, 'NE': 18, 'NO': 19, 'NYG': 20, 'NYJ': 21,
            'PHI': 22, 'ARI': 23, 'PIT': 24, 'SF': 25, 'SEA': 26, 'TB': 27, 'WSH': 28,
            'CAR': 29, 'JAX': 30, 'BAL': 33, 'HOU': 34
        }
        return team_mapping.get(team_abbr, 1)  # Default to ATL if not found

    def display_starter_lineup(self, optimal_lineup):
        """Display optimal starting lineup in starter_helper format"""
        return self.menu_system.display_starter_lineup(optimal_lineup)

    def display_bench_alternatives(self, bench_recommendations):
        """Display bench alternatives in starter_helper format"""
        return self.menu_system.display_bench_alternatives(bench_recommendations)

    def generate_starter_output(self, optimal_lineup, bench_recs, roster_df, projections):
        """Generate output content for file saving"""
        output_buffer = StringIO()

        # Helper function to write to buffer
        def write_line(message=""):
            output_buffer.write(message + '\n')

        write_line(f"Fantasy Football Starter Helper")
        write_line(f"Week {CURRENT_NFL_WEEK} of {NFL_SEASON} NFL Season")
        write_line(f"Scoring Format: {NFL_SCORING_FORMAT.upper()}")
        write_line("="*60)
        write_line()

        # Optimal lineup
        write_line("="*80)
        write_line(f"OPTIMAL STARTING LINEUP - WEEK {CURRENT_NFL_WEEK} ({NFL_SCORING_FORMAT.upper()} SCORING)")
        write_line("="*80)

        starters = [
            (optimal_lineup.qb, "QB"),
            (optimal_lineup.rb1, "RB"),
            (optimal_lineup.rb2, "RB"),
            (optimal_lineup.wr1, "WR"),
            (optimal_lineup.wr2, "WR"),
            (optimal_lineup.te, "TE"),
            (optimal_lineup.flex, "FLEX"),
            (optimal_lineup.k, "K"),
            (optimal_lineup.dst, "DEF")
        ]

        for i, (recommendation, pos_label) in enumerate(starters, 1):
            if recommendation:
                name_team = f"{recommendation.name} ({recommendation.team})"
                points_info = f"{recommendation.projected_points:.1f} pts"

                status_info = ""
                if recommendation.injury_status != "ACTIVE":
                    status_info = f" [{recommendation.injury_status}]"

                matchup_info = ""
                if recommendation.matchup_indicator:
                    matchup_info = f" {recommendation.matchup_indicator}"

                penalty_info = ""
                if recommendation.reason != "No penalties":
                    penalty_info = f" ({recommendation.reason})"

                write_line(f"{i:2d}. {pos_label:4s}: {name_team:25s} - {points_info}{status_info}{matchup_info}{penalty_info}")
            else:
                write_line(f"{i:2d}. {pos_label:4s}: No available player")

        write_line("-"*80)
        write_line(f"TOTAL PROJECTED POINTS: {optimal_lineup.total_projected_points:.1f}")
        write_line("-"*80)

        # Bench alternatives
        if bench_recs:
            write_line()
            write_line("TOP BENCH ALTERNATIVES:")
            write_line("-"*60)

            for i, rec in enumerate(bench_recs, 1):
                name_team = f"{rec.name} ({rec.team}) - {rec.position}"
                points_info = f"{rec.projected_points:.1f} pts"

                status_info = ""
                if rec.injury_status != "ACTIVE":
                    status_info = f" [{rec.injury_status}]"

                write_line(f"{i:2d}. {name_team:35s} - {points_info}{status_info}")

        write_line()
        write_line(f"Starter recommendations complete for Week {CURRENT_NFL_WEEK}")
        write_line(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return output_buffer.getvalue()

    def save_starter_output_to_files(self, output_content):
        """Save starter helper output to files in original starter_helper/data directory"""
        try:
            # Use original starter_helper/data directory to maintain consistency
            starter_data_dir = Path("../starter_helper/data")
            starter_data_dir.mkdir(parents=True, exist_ok=True)

            # Generate file names manually to use correct directory
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            timestamped_filename = f"starter_results_{timestamp}.txt"
            latest_filename = "starter_results_latest.txt"

            timestamped_filepath = starter_data_dir / timestamped_filename
            latest_filepath = starter_data_dir / latest_filename

            # Save to timestamped file
            with open(timestamped_filepath, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"Results saved to: {timestamped_filepath}")

            # Save to latest file
            with open(latest_filepath, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"Latest results updated: {latest_filepath}")

        except Exception as e:
            print(f"Warning: Could not save results to file: {str(e)}")
            self.logger.error(f"Error saving starter output: {str(e)}")

    # Main function to run the draft helper
    # This will prompt the user to draft players based on recommendations
    def run_draft(self, simulation=False):
        print("Welcome to the Start 7 Fantasy League Draft Helper!")
        print(f"Currently drafted players: {len(self.team.roster)} / {Constants.MAX_PLAYERS} max")
        print("Your current roster by position:")
        for pos, count in self.team.pos_counts.items():
            print(f"  {pos}: {count}")
        print("\nDraft order:")
        self.team.print_draft_order()
        self.logger.info(f"Draft started. Current roster size: {len(self.team.roster)}")

        # Get the user's draft choice
        player_to_draft = self.get_user_player_choice(simulation=simulation)

        # If a player was successfully drafted, save the updated player data
        if player_to_draft is not None:
            # Update the player data to reflect the drafted player
            self.save_players()
            self.logger.info(f"Draft round complete. Player {player_to_draft.name} drafted. Players data updated")

        # Print final roster after drafting is complete or user exits
        print("\nDrafting complete or exited. Final team roster:")
        for p in self.team.roster:
            print(f" - {p}")
        print(f"Total players drafted: {len(self.team.roster)} / {Constants.MAX_PLAYERS}")
        self.logger.info(f"Drafting session ended. Final team roster size: {len(self.team.roster)}")

    # Trade helper methods
    def run_trade_helper(self):
        """
        Run the trade helper to optimize the current roster by finding beneficial trades
        """
        # Get available players for trades (drafted=0)
        available_players = [p for p in self.players if p.drafted == 0 and p.locked == 0]

        # Run trade helper analysis
        trades_made, all_player_trades = self.trade_analyzer.run_trade_helper(available_players, self.score_player_for_trade)

        # Show final roster comparison with runner-ups
        self.show_roster_comparison(trades_made, all_player_trades)

    def optimize_roster_iteratively(self, available_players):
        """Legacy method for compatibility - delegates to TradeAnalyzer"""
        return self.trade_analyzer.optimize_roster_iteratively(available_players, self.score_player_for_trade)

    def find_best_trade_with_runners_up(self, available_players, recent_trades=None):
        """Legacy method for compatibility - delegates to TradeAnalyzer"""
        return self.trade_analyzer.find_best_trade_with_runners_up(available_players, recent_trades or set(), self.score_player_for_trade)

    def consolidate_trades(self, trades_made):
        """Legacy method for compatibility - delegates to TradeAnalyzer"""
        return self.trade_analyzer.consolidate_trades(trades_made)


    def score_player_for_trade(self, player):
        """
        Modified scoring function for trade evaluation
        Sets positional need weight to 0 and focuses on projections, injuries, bye weeks, and matchups
        Uses enhanced scoring for accurate player valuations
        """
        return self.scoring_engine.score_player_for_trade(
            player,
            positional_ranking_calculator=self.positional_ranking_calculator,
            enhanced_scorer=self.enhanced_scorer,
            team_data_loader=self.team_data_loader
        )

    def compute_positional_need_score(self, p):
        """
        Legacy method for compatibility - now uses DRAFT_ORDER bonus system.

        The old positional need scoring has been replaced with DRAFT_ORDER bonuses.
        This method now returns the DRAFT_ORDER bonus for the current round.
        """
        return self.scoring_engine.draft_order_calculator.calculate_bonus(p)

    def compute_projection_score(self, p):
        """
        Legacy method for compatibility - now uses new normalization + enhanced scoring system.

        Returns normalized + enhanced score (steps 1-4 of new scoring system).
        This is equivalent to the old projection score but uses the new modular approach.
        """
        # STEP 1: Normalize seasonal fantasy points
        normalized_score = self.scoring_engine.normalization_calculator.normalize_player(p, self.players)

        # STEPS 2-4: Apply enhanced scoring (ADP, Player Ranking, Team Ranking multipliers)
        enhanced_score = self.scoring_engine._apply_enhanced_scoring(
            normalized_score,
            p,
            enhanced_scorer=self.enhanced_scorer,
            team_data_loader=self.team_data_loader,
            positional_ranking_calculator=self.positional_ranking_calculator
        )

        return enhanced_score

    def compute_bye_penalty_for_player(self, player, exclude_self=False):
        """Legacy method for compatibility - delegates to ScoringEngine"""
        return self.scoring_engine.compute_bye_penalty_for_player(player, exclude_self)

    def compute_injury_penalty(self, p, trade_mode=False):
        """Legacy method for compatibility - delegates to ScoringEngine"""
        return self.scoring_engine.compute_injury_penalty(p, trade_mode)

    def show_roster_comparison(self, trades_made, all_player_trades=None):
        """
        Display a clear comparison between original and final roster, including runner-up trades
        """
        return self.roster_manager.show_roster_comparison(
            trades_made=trades_made,
            all_player_trades=all_player_trades,
            score_player_for_trade_func=self.score_player_for_trade
        )
    

async def main():
    """Main async entry point for the draft helper"""
    # Setup logging
    logger = setup_logging()

    try:
        # Default parameter JSON path
        param_json_path = str(Path(__file__).parent.parent / 'shared_files' / 'parameters.json')

        draft_helper = DraftHelper(
            players_csv=Constants.PLAYERS_CSV,
            parameter_json_path=param_json_path
        )

        # Always run interactive mode - waiver optimizer now available via menu
        logger.info("Starting Interactive Fantasy Helper (Draft & Waiver Optimizer)")
        await draft_helper.run_interactive_draft()

    except Exception as e:
        logger.error(f"Error in helper: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
