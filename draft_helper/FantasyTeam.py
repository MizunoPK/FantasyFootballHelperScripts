from collections import Counter
import logging
import draft_helper_constants as Constants

# FantasyTeam class to manage a fantasy football team
# It holds drafted players, manages roster limits, and draft order
# It also provides methods to draft players and check roster status
class FantasyTeam:
    def __init__(self, players=None):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"FantasyTeam.__init__ called with {len(players) if players else 0} players")
        # Roster holds Player instances drafted so far
        self.roster = players if players else []

        # Count positions
        self.pos_counts = {
            Constants.QB: 0,
            Constants.RB: 0,
            Constants.WR: 0,
            Constants.TE: 0,
            Constants.DST: 0,
            Constants.K: 0, 
            Constants.FLEX: 0
        }
        
        # Pre-compute bye week counts by position for efficient penalty calculation
        # Structure: {bye_week: {position: count}}
        self.bye_week_counts = {}
        for bye_week in Constants.POSSIBLE_BYE_WEEKS:
            self.bye_week_counts[bye_week] = {pos: 0 for pos in Constants.MAX_POSITIONS.keys()}
        
        # Set up the draft order list
        self.draft_order = [None] * Constants.MAX_PLAYERS

        # Count current positions in roster and organize them
        for player in self.roster:
            pos = player.position

            # add to counts
            if self.flex_eligible(pos):
                self.pos_counts[Constants.FLEX] += 1
            else:
                self.pos_counts[pos] += 1

            # Update bye week counts
            if player.bye_week and player.bye_week in self.bye_week_counts:
                self.bye_week_counts[player.bye_week][pos] += 1

            # place in the draft order
            pos_with_flex = Constants.FLEX if pos in Constants.FLEX_ELIGIBLE_POSITIONS else pos
            for i in range(Constants.MAX_PLAYERS):
                if self.draft_order[i] is None and pos_with_flex == Constants.get_ideal_draft_position(i):
                    self.draft_order[i] = player
                    break

        self.logger.debug(f"position counts after labeling: {self.pos_counts}")
        self.logger.debug(f"draft_order after assignment: {[p.id if p else None for p in self.draft_order]}")
        self.logger.info(f"FantasyTeam initialized. Roster size: {len(self.roster)}")

    # Method to get the next draft position weights based on the current roster
    def get_next_draft_position_weights(self):
        self.logger.debug("FantasyTeam.get_next_draft_position_weights called")
        # Find the next open draft position
        for i in range(Constants.MAX_PLAYERS):
            if self.draft_order[i] is None:
                self.logger.debug(f"Next draft position weights: {Constants.DRAFT_ORDER[i]}")
                return Constants.DRAFT_ORDER[i]
        self.logger.debug("No draft position weights available (draft full)")
        return None

    
    # Method to check if a player can be drafted as a FLEX position
    # A player is eligible to be labeled as the 'FLEX' position if:
    # 1. Their position is one of the FLEX eligible positions (RB or WR)
    # 2. Their primary position is already at the max limit
    # 3. The FLEX position itself is not yet filled to its max limit
    # This allows drafting a player into the FLEX spot when their main position is full
    # but there is still room in the FLEX slot.
    def flex_eligible(self, pos):
        # Check if player can be drafted as a FLEX
        if pos not in Constants.FLEX_ELIGIBLE_POSITIONS:
            return False
        
        # Return whether the player's position is at the limit and the FLEX slot is available
        result = self.pos_counts[pos] >= Constants.MAX_POSITIONS[pos] and self.pos_counts[Constants.FLEX] < Constants.MAX_POSITIONS[Constants.FLEX]
        return result

    # Method to check if a player can be drafted
    def can_draft(self, player):
        self.logger.debug(f"FantasyTeam.can_draft called for player ID: {player.id}")
        # Check total roster space
        if len(self.roster) >= Constants.MAX_PLAYERS:
            self.logger.debug("Roster full, cannot draft.")
            return False

        # Check if player position is valid
        pos = player.position
        if pos not in Constants.MAX_POSITIONS:
            self.logger.debug(f"Invalid position {pos}, cannot draft.")
            return False
        
        # Check if position limit is reached
        if self.pos_counts[pos] >= Constants.MAX_POSITIONS[pos] and not self.flex_eligible(pos):
            self.logger.debug(f"Cannot draft player {player.id}, position {pos} limit reached.")
            return False

        # Check if player is already drafted
        if not player.is_available():
            self.logger.debug(f"Player {player.id} already drafted.")
            return False
        
        # Check player's bye week (allow None for players without assigned bye weeks)
        if player.bye_week is not None and player.bye_week not in Constants.POSSIBLE_BYE_WEEKS:
            self.logger.debug(f"Player {player.id} has an invalid bye week: {player.bye_week}.")
            return False

        self.logger.debug(f"Player {player.id} can be drafted.")
        return True

    # Method to draft a player onto the team
    def draft_player(self, player):
        self.logger.debug(f"FantasyTeam.draft_player called for player ID: {player.id}")
        can_draft = self.can_draft(player)
        if can_draft:
            player.drafted = 2
            self.roster.append(player)
            
            # Update position counts
            pos = player.position
            if self.flex_eligible(pos):
                self.pos_counts[Constants.FLEX] += 1
            else:
                self.pos_counts[pos] += 1
            
            # Update bye week counts
            if player.bye_week and player.bye_week in self.bye_week_counts:
                self.bye_week_counts[player.bye_week][pos] += 1
            
            self.logger.debug(f"Player {player.id} drafted successfully. Roster size now {len(self.roster)}.")
            return True
        else:
            self.logger.debug(f"Player {player.id} could not be drafted.")
            return False

    # Method to remove a player from the team (for trade helper)
    def remove_player(self, player):
        self.logger.debug(f"FantasyTeam.remove_player called for player ID: {player.id}")
        if player not in self.roster:
            self.logger.debug(f"Player {player.id} not in roster, cannot remove.")
            return False
        
        # Remove from roster
        self.roster.remove(player)
        player.drafted = 0  # Mark as available again
        
        # Update position counts
        pos = player.position
        if pos in Constants.FLEX_ELIGIBLE_POSITIONS and self.pos_counts[Constants.FLEX] > 0:
            # Check if this was a FLEX player or regular position player
            # We need to determine which count to decrement
            if self.pos_counts[pos] < Constants.MAX_POSITIONS[pos]:
                self.pos_counts[pos] -= 1
            else:
                self.pos_counts[Constants.FLEX] -= 1
        else:
            self.pos_counts[pos] -= 1
        
        # Update bye week counts
        if player.bye_week and player.bye_week in self.bye_week_counts:
            self.bye_week_counts[player.bye_week][pos] -= 1
        
        # Remove from draft order
        for i in range(Constants.MAX_PLAYERS):
            if self.draft_order[i] == player:
                self.draft_order[i] = None
                break
        
        self.logger.debug(f"Player {player.id} removed successfully. Roster size now {len(self.roster)}.")
        return True

    # Method to replace a player atomically (for trade helper)
    def replace_player(self, old_player, new_player):
        self.logger.debug(f"FantasyTeam.replace_player called: {old_player.id} -> {new_player.id}")
        
        # Check if we can make this swap while maintaining position constraints
        if not self._can_replace_player(old_player, new_player):
            self.logger.debug(f"Cannot replace {old_player.id} with {new_player.id} due to position constraints.")
            return False
        
        # Remove old player
        if not self.remove_player(old_player):
            return False
        
        # Add new player
        if not self.draft_player(new_player):
            # If adding new player fails, add the old player back
            self.draft_player(old_player)
            return False
        
        self.logger.debug(f"Player replacement successful: {old_player.id} -> {new_player.id}")
        return True
    
    # Helper method to check if a player replacement is valid
    def _can_replace_player(self, old_player, new_player):
        # For same position, always allowed
        if old_player.position == new_player.position:
            return True
        
        # For FLEX eligible positions, check if we maintain minimums
        if (old_player.position in Constants.FLEX_ELIGIBLE_POSITIONS and 
            new_player.position in Constants.FLEX_ELIGIBLE_POSITIONS):
            
            # Count current RB and WR (excluding FLEX)
            rb_count = self.pos_counts[Constants.RB]
            wr_count = self.pos_counts[Constants.WR]
            
            # Check if old player is in FLEX slot or regular slot
            old_in_flex = (self.pos_counts[old_player.position] >= Constants.MAX_POSITIONS[old_player.position])
            
            if not old_in_flex:
                # Removing from regular position
                if old_player.position == Constants.RB:
                    rb_count -= 1
                else:  # WR
                    wr_count -= 1
            
            # Adding new player - will it go to regular or FLEX?
            new_in_flex = (self.pos_counts[new_player.position] >= Constants.MAX_POSITIONS[new_player.position])
            
            if not new_in_flex:
                # Adding to regular position
                if new_player.position == Constants.RB:
                    rb_count += 1
                else:  # WR
                    wr_count += 1
            
            # Check if we still have at least 4 in each position (including potential FLEX)
            total_rb = rb_count + (1 if self.pos_counts[Constants.FLEX] > 0 else 0)
            total_wr = wr_count + (1 if self.pos_counts[Constants.FLEX] > 0 else 0)
            
            return total_rb >= 4 and total_wr >= 4
        
        # Different position types not in FLEX eligibles - not allowed for now
        return False

    # Method to get total team score for trade optimization
    def get_total_team_score(self, scoring_function):
        self.logger.debug("FantasyTeam.get_total_team_score called")
        total_score = 0
        for player in self.roster:
            total_score += scoring_function(player)
        return total_score

    # print the ideal draft order, and what the actual draft order is
    def print_draft_order(self):
        self.logger.debug("FantasyTeam.print_draft_order called")
        for i, pos in enumerate(Constants.DRAFT_ORDER):
            print(f"Round {i + 1}: {', '.join(pos.keys())} -- Drafted: {self.draft_order[i].name if self.draft_order[i] else 'None'} ({self.draft_order[i].position if self.draft_order[i] else 'None'})")
