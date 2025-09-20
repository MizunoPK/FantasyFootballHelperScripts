import csv
import sys
import logging
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from FantasyTeam import FantasyTeam
import draft_helper_constants as Constants
from shared_files.FantasyPlayer import FantasyPlayer


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
        if player.fantasy_points and max_projection > 0:
            player.weighted_projection = (player.fantasy_points / max_projection) * Constants.PROJECTION_BASE_SCORE
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

    def __init__(self, players_csv=Constants.PLAYERS_CSV):
        """
        Initialize the DraftHelper with players and team data.
        Loads players from the specified CSV files.
        """
        self.logger = logging.getLogger(__name__)
        self.players_csv = players_csv
        self.players = load_players_from_csv(players_csv)
        self.team = self.load_team()
        
        self.logger.info(f"DraftHelper initialized with {len(self.players)} players and team of {len(self.team.roster)} drafted players")
        print(f"DraftHelper initialized with {len(self.players)} players and team of {len(self.team.roster)} drafted players.")

    def load_team(self):
        """
        Load the current team from the player data
        it will be players marked as drafted=2
        """
        drafted_players = [p for p in self.players if p.drafted == 2]
        return FantasyTeam(drafted_players)
        
        
    """        
    Function to score a player based on various factors:
    - Team position needs vs roster max and starters requirements
    - Projected Points
    - Bye week conflicts with current starters and bench
    - Injury status
    - Returns a score that can be used to rank players for drafting.
    """
    def score_player(self, p):
        self.logger.debug(f"Scoring player {p.name} (ID: {p.id}, Position: {p.position}, Bye: {p.bye_week}, Injury: {p.injury_status})")
        # Calculate Position score based on where we are in the draft, and what positions are needed
        pos_score = self.compute_positional_need_score(p)
        self.logger.debug(f"Positional need score for {p.name}: {pos_score}")

        # Calculate projection score
        projection_score = self.compute_projection_score(p)
        self.logger.debug(f"Projection score for {p.name}: {projection_score}")

        # Calculate bye week penalty based on overlap with current starters/bench
        # This discourages drafting too many players with the same bye week
        bye_penalty = self.compute_bye_penalty_for_player(p)
        self.logger.debug(f"Bye week penalty for {p.name}: {bye_penalty}")

        # Apply a penalty if the player is not healthy
        # This deprioritizes injured players in recommendations
        injury_penalty = self.compute_injury_penalty(p)
        self.logger.debug(f"Injury penalty for {p.name}: {injury_penalty}")

        # Final score combines all factors
        total_score = pos_score + projection_score - bye_penalty - injury_penalty
        self.logger.debug(f"Total score for {p.name}: {total_score}")
        return total_score
    
    # Function to compute the positional need score for a player
    # This considers how many players are already drafted at that position
    # And the pre-defined ideal draft order
    def compute_positional_need_score(self, p):
        self.logger.debug(f"compute_positional_need_score called for {p.name} (ID: {p.id})")
        score = 0
        pos = p.get_position_including_flex()
        
        # calculate score based on draft order
        draft_weights = self.team.get_next_draft_position_weights()
        if draft_weights is None:
            # Draft is full, no positional need scoring
            multiplier = 0.0
            self.logger.debug(f"Draft is full, no positional need score for {p.name}")
        else:
            multiplier = draft_weights.get(pos, 0.0)
            self.logger.debug(f"Computing positional need score for {p.name}: position={pos}, multiplier={multiplier}")
        score += Constants.POS_NEEDED_SCORE * multiplier

        return score

    # Function to compute the ADP score for a player
    # This is a simple inversion of the ADP value, where lower ADP means higher score
    def compute_projection_score(self, p):
        self.logger.debug(f"compute_projection_score called for {p.name} (ID: {p.id})")
        projection_score = p.weighted_projection if p.weighted_projection else 0.0
        self.logger.debug(f"Computing projection score for {p.name}: weighted_projection={projection_score}")
        return projection_score

    # Function to compute the bye week penalty for a player
    # This checks how many players are already drafted with the same bye week
    # and applies a penalty based on the number of conflicts
    def compute_bye_penalty_for_player(self, player, exclude_self=False):
        self.logger.debug(f"compute_bye_penalty_for_player called for {player.name} (ID: {player.id}), exclude_self={exclude_self}")
        # If player has no bye week, no penalty is applied
        if not player.bye_week:
            return 0

        pos = player.position
        bw = player.bye_week
        penalty = 0

        # Get the max number of players allowed at this position
        max_pos = Constants.MAX_POSITIONS.get(pos, 0)
        if max_pos == 0:  # Avoid division by zero
            return 0
        
        # Use pre-computed bye week counts for efficiency
        bye_week_count = 0
        if bw in self.team.bye_week_counts:
            bye_week_count = self.team.bye_week_counts[bw].get(pos, 0)
            
        # If excluding self and this player is on the roster, subtract 1 from count
        if exclude_self and player.drafted == 2 and bye_week_count > 0:
            bye_week_count -= 1
            self.logger.debug(f"Excluding self from bye week count for {player.name}: reduced count to {bye_week_count}")
        
        if bye_week_count > 0:
            penalty += Constants.BASE_BYE_PENALTY * bye_week_count / max_pos

        self.logger.debug(f"Bye penalty for {player.name}: {penalty} (bye week: {bw}, count: {bye_week_count})")
        return penalty

    # Function to compute the injury penalty for a player
    # This checks if the player is injured and applies a penalty
    # In trade mode, can optionally ignore injury penalties for roster players (drafted=2)
    def compute_injury_penalty(self, p):
        self.logger.debug(f"compute_injury_penalty called for {p.name} (ID: {p.id})")

        # Import current config values to get real-time settings
        import draft_helper_config as config

        # Check if we should skip injury penalties for roster players in trade mode
        if (config.TRADE_HELPER_MODE and
            not config.APPLY_INJURY_PENALTY_TO_ROSTER and
            p.drafted == 2):
            self.logger.debug(f"Skipping injury penalty for roster player {p.name} (APPLY_INJURY_PENALTY_TO_ROSTER=False)")
            return 0

        penalty = Constants.INJURY_PENALTIES.get(p.get_risk_level(), 0)
        self.logger.debug(f"Injury penalty for {p.name}: {penalty} (risk level: {p.get_risk_level()})")
        return penalty

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
        
        # Save sorted players to CSV
        with open(self.players_csv, 'w', newline='') as csvfile:
            fieldnames = [
                'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
                'injury_status', 'drafted'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in sorted_players:
                # Only include fields that are in fieldnames to avoid DictWriter errors
                player_dict = p.to_dict()
                filtered_dict = {key: player_dict[key] for key in fieldnames if key in player_dict}
                writer.writerow(filtered_dict)
        self.logger.info(f"Available players saved with {len(self.players)} players (sorted by drafted status)")

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
        print("Welcome to the Start 7 Fantasy League Trade Helper!")
        print(f"Current roster: {len(self.team.roster)} / {Constants.MAX_PLAYERS} players")
        print("Your current roster by position:")
        for pos, count in self.team.pos_counts.items():
            print(f"  {pos}: {count}")

        # Get available players for trades (drafted=0)
        available_players = [p for p in self.players if p.drafted == 0 and p.locked == 0]
        print(f"\nAnalyzing {len(available_players)} available players for potential trades...")

        # Calculate initial team score
        initial_score = self.team.get_total_team_score(self.score_player_for_trade)
        print(f"Initial team score: {initial_score:.2f}")

        # Perform iterative improvement
        trades_made, all_player_trades = self.optimize_roster_iteratively(available_players)

        # Final results
        final_score = self.team.get_total_team_score(self.score_player_for_trade)
        total_improvement = final_score - initial_score

        print(f"\n{'='*60}")
        print("TRADE OPTIMIZATION COMPLETE")
        print(f"{'='*60}")
        print(f"Initial team score: {initial_score:.2f}")
        print(f"Final team score: {final_score:.2f}")
        print(f"Total improvement: {total_improvement:+.2f}")
        print(f"Number of trades recommended: {len(trades_made)}")

        # Show final roster comparison with runner-ups
        self.show_roster_comparison(trades_made, all_player_trades)

        self.logger.info(f"Trade optimization complete. {len(trades_made)} trades recommended, "
                        f"total improvement: {total_improvement:+.2f}")

    def optimize_roster_iteratively(self, available_players):
        """
        Perform iterative improvement on the roster by finding the best possible trades
        """
        trades_made = []
        iteration = 0
        recent_trades = set()  # Track recent trades to prevent oscillation
        max_iterations = 100  # Safety limit to prevent infinite loops
        all_player_trades = None  # Store runner-up data from last iteration

        while iteration < max_iterations:
            iteration += 1
            self.logger.info(f"Trade optimization iteration {iteration}")

            # Find the best possible trade that hasn't been recently reversed, including runner-ups
            best_trade, current_all_player_trades = self.find_best_trade_with_runners_up(available_players, recent_trades)

            if best_trade is None:
                self.logger.info(f"No beneficial trades found in iteration {iteration}. Optimization complete.")
                break

            # Store the runner-up data for this trade before executing it
            if best_trade['out'].id in current_all_player_trades:
                best_trade['runners_up'] = current_all_player_trades[best_trade['out'].id]

            # Execute the trade
            old_player = best_trade['out']
            new_player = best_trade['in']
            improvement = best_trade['improvement']

            self.logger.info(f"Executing trade: {old_player.name} -> {new_player.name} (+{improvement:.2f})")

            if self.team.replace_player(old_player, new_player):
                # Move players between available/roster lists
                available_players.append(old_player)
                available_players.remove(new_player)

                trades_made.append(best_trade)

                # Update all_player_trades with the latest data
                all_player_trades = current_all_player_trades

                # Track this trade to prevent immediate reversal
                trade_key = (old_player.id, new_player.id)
                reverse_key = (new_player.id, old_player.id)
                recent_trades.add(trade_key)

                # Also add the reverse to prevent oscillation
                recent_trades.add(reverse_key)

                # Keep only the last 20 trades in memory to prevent cycles
                if len(recent_trades) > 20:
                    recent_trades = set(list(recent_trades)[-20:])

                print(f"Trade {len(trades_made)}: {old_player.name} ({old_player.position}) -> "
                      f"{new_player.name} ({new_player.position}) (+{improvement:.2f} points)")
            else:
                self.logger.error(f"Failed to execute trade: {old_player.name} -> {new_player.name}")
                break

        if iteration >= max_iterations:
            print(f"Warning: Reached maximum iterations ({max_iterations}). Optimization stopped.")
            self.logger.warning(f"Trade optimization reached maximum iterations ({max_iterations})")

        return trades_made, all_player_trades

    def find_best_trade_with_runners_up(self, available_players, recent_trades=None):
        """
        Find the best possible trade from the current roster along with runner-up trades for each player
        """
        if recent_trades is None:
            recent_trades = set()

        best_trade = None
        best_improvement = 0
        all_player_trades = {}  # Dictionary to store all potential trades by player being traded out

        # For each player on the roster (excluding locked players)
        for current_player in self.team.roster:
            if current_player.locked == 1:
                continue
            current_score = self.score_player_for_trade(current_player)

            # Find the best available replacement for this position
            same_position_players = [p for p in available_players
                                   if p.position == current_player.position]

            # Also consider FLEX-eligible swaps
            if current_player.position in Constants.FLEX_ELIGIBLE_POSITIONS:
                for other_pos in Constants.FLEX_ELIGIBLE_POSITIONS:
                    if other_pos != current_player.position:
                        flex_candidates = [p for p in available_players if p.position == other_pos]
                        same_position_players.extend(flex_candidates)

            # Collect all valid trades for this player
            player_trades = []

            # Evaluate each potential replacement
            for candidate in same_position_players:
                # Check if this trade was recently made (prevent oscillation)
                trade_key = (current_player.id, candidate.id)
                if trade_key in recent_trades:
                    continue

                # Check if this trade is valid
                if not self.team._can_replace_player(current_player, candidate):
                    continue

                candidate_score = self.score_player_for_trade(candidate)
                improvement = candidate_score - current_score

                # Only consider trades that meet the minimum improvement threshold
                if improvement >= Constants.MIN_TRADE_IMPROVEMENT:
                    trade = {
                        'out': current_player,
                        'in': candidate,
                        'improvement': improvement
                    }
                    player_trades.append(trade)

                    # Check if this is the best overall trade
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_trade = trade

            # Sort trades for this player by improvement (best first)
            player_trades.sort(key=lambda x: x['improvement'], reverse=True)
            all_player_trades[current_player.id] = player_trades

        return best_trade, all_player_trades

    def score_player_for_trade(self, player):
        """
        Modified scoring function for trade evaluation
        Sets positional need weight to 0 and focuses on projections, injuries, and bye weeks
        For roster players (drafted=2), excludes self from bye week penalty calculation
        """
        self.logger.debug(f"Scoring player for trade: {player.name} (ID: {player.id})")
        
        # Use 0 weight for positional need as specified
        pos_score = 0
        
        # Calculate projection score
        projection_score = self.compute_projection_score(player)
        self.logger.debug(f"Projection score for {player.name}: {projection_score}")
        
        # Calculate bye week penalty - exclude self if this is a roster player
        exclude_self = (player.drafted == 2)
        bye_penalty = self.compute_bye_penalty_for_player(player, exclude_self=exclude_self)
        self.logger.debug(f"Bye week penalty for {player.name}: {bye_penalty}")
        
        # Calculate injury penalty
        injury_penalty = self.compute_injury_penalty(player)
        self.logger.debug(f"Injury penalty for {player.name}: {injury_penalty}")
        
        # Calculate final score (higher is better)
        total_score = pos_score + projection_score - bye_penalty - injury_penalty
        
        self.logger.debug(f"Total score for {player.name}: {total_score:.2f} "
                         f"(pos: {pos_score}, proj: {projection_score:.2f}, "
                         f"bye: -{bye_penalty:.2f}, injury: -{injury_penalty})")
        
        return total_score

    def show_roster_comparison(self, trades_made, all_player_trades=None):
        """
        Display a clear comparison between original and final roster, including runner-up trades
        """
        if not trades_made:
            print("\nNo beneficial trades found. Your roster is already optimized!")

            # Still show runner-up trades if available for current players
            if all_player_trades:
                self.show_current_roster_with_alternatives(all_player_trades)
            else:
                print(f"\nCurrent roster:")
                for p in sorted(self.team.roster, key=lambda x: x.position):
                    score = self.score_player_for_trade(p)
                    print(f"  {p.name} ({p.position}) - {score:.2f} pts")
            return

        # Get original roster by reversing all trades (using player IDs for comparison)
        original_roster_ids = set(p.id for p in self.team.roster)
        players_out = []
        players_in = []

        # Reverse the trades to find original roster
        for trade in reversed(trades_made):
            # Remove players that were traded in
            if trade['in'].id in original_roster_ids:
                original_roster_ids.remove(trade['in'].id)
                players_in.append(trade['in'])

            # Add back players that were traded out
            original_roster_ids.add(trade['out'].id)
            players_out.append(trade['out'])

        # Remove duplicates while preserving order (last occurrence wins)
        seen_out = set()
        players_out_unique = []
        for p in reversed(players_out):
            if p.id not in seen_out:
                seen_out.add(p.id)
                players_out_unique.append(p)
        players_out_unique.reverse()

        seen_in = set()
        players_in_unique = []
        for p in reversed(players_in):
            if p.id not in seen_in:
                seen_in.add(p.id)
                players_in_unique.append(p)
        players_in_unique.reverse()

        # Current final roster
        final_roster_ids = set(p.id for p in self.team.roster)

        # Players that stayed (in both original and final)
        players_kept_ids = original_roster_ids.intersection(final_roster_ids)
        players_kept = [p for p in self.team.roster if p.id in players_kept_ids]

        print(f"\nROSTER ANALYSIS:")
        print(f"Players kept: {len(players_kept)}")
        print(f"Players traded out: {len(players_out_unique)}")
        print(f"Players traded in: {len(players_in_unique)}")

        # Show kept players first
        if players_kept:
            print(f"\n[KEPT] PLAYERS REMAINING ON ROSTER:")
            for p in sorted(players_kept, key=lambda x: x.position):
                score = self.score_player_for_trade(p)
                print(f"  {p.name} ({p.position}) - {score:.2f} pts")

        print(f"\n[TRADES] RECOMMENDED CHANGES ({len(trades_made)} trades):")
        for i, trade in enumerate(trades_made, 1):
            out_score = self.score_player_for_trade(trade['out'])
            in_score = self.score_player_for_trade(trade['in'])

            print(f"  {i}. OUT: {trade['out'].name} ({trade['out'].position}) - {out_score:.2f} pts")
            print(f"     IN:  {trade['in'].name} ({trade['in'].position}) - {in_score:.2f} pts")
            print(f"     Net Improvement: +{trade['improvement']:.2f} pts")

            # Show runner-ups for this trade (use stored data from when trade was made)
            if 'runners_up' in trade:
                player_trades = trade['runners_up']
                # Find runner-ups (skip the main trade we just showed)
                runners_up = []
                for pt in player_trades:
                    if pt['in'].id != trade['in'].id:  # Skip the main trade
                        runners_up.append(pt)
                    if len(runners_up) >= Constants.NUM_TRADE_RUNNERS_UP:
                        break

                if runners_up:
                    for j, runner_up in enumerate(runners_up, 1):
                        ru_score = self.score_player_for_trade(runner_up['in'])
                        print(f"        Runner-up {j}: {runner_up['in'].name} - {ru_score:.2f} pts ({runner_up['improvement']:+.2f})")
            print()

    def show_current_roster_with_alternatives(self, all_player_trades):
        """
        Show current roster with alternative trade options when no beneficial trades exist
        """
        print(f"\nCurrent roster with potential alternatives:")

        for p in sorted(self.team.roster, key=lambda x: x.position):
            if p.locked == 1:
                continue

            score = self.score_player_for_trade(p)
            print(f"  {p.name} ({p.position}) - {score:.2f} pts")

            # Show alternatives that don't meet the threshold
            if p.id in all_player_trades:
                player_trades = all_player_trades[p.id]
                alternatives = player_trades[:Constants.NUM_TRADE_RUNNERS_UP]

                if alternatives:
                    for j, alt in enumerate(alternatives, 1):
                        alt_score = self.score_player_for_trade(alt['in'])
                        print(f"        Alternative {j}: {alt['in'].name} - {alt_score:.2f} pts ({alt['improvement']:+.2f})")
            print()
    
    def consolidate_trades(self, trades_made):
        """
        Consolidate trades to show only the net result (remove back-and-forth swaps)
        """
        if len(trades_made) <= 10:  # If few trades, show all
            return trades_made
        
        # For many trades, show only the first meaningful ones before oscillation starts
        consolidated = []
        seen_positions = set()
        
        for trade in trades_made:
            position_pair = (trade['out'].position, trade['in'].position)
            reverse_pair = (trade['in'].position, trade['out'].position)
            
            # Add trade if we haven't seen this position pair before
            if position_pair not in seen_positions and reverse_pair not in seen_positions:
                consolidated.append(trade)
                seen_positions.add(position_pair)
                
                # Stop after we have good trades from each position
                if len(consolidated) >= 8:  # Reasonable limit for meaningful trades
                    break
        
        return consolidated

if __name__ == "__main__":
    # Setup logging
    logger = setup_logging()
    
    try:
        draft_helper = DraftHelper(Constants.PLAYERS_CSV)
        
        if Constants.TRADE_HELPER_MODE:
            logger.info("Starting Fantasy Trade Helper")
            draft_helper.run_trade_helper()
        else:
            logger.info("Starting Fantasy Draft Helper")
            draft_helper.run_draft()
        
    except Exception as e:
        logger.error(f"Error in helper: {e}")
        raise
