import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
import constants as Constants

parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))
from utils.LoggingManager import get_logger

# FantasyTeam class to manage a fantasy football team
# It holds drafted players, manages roster limits, and draft order
# It also provides methods to draft players and check roster status
class FantasyTeam:
    """
    Manages a fantasy football team roster with position limits and draft order.

    This class handles all aspects of team management including:
    - Tracking drafted players and roster composition
    - Enforcing position limits and FLEX eligibility rules
    - Managing draft order and slot assignments
    - Calculating team scores and bye week impacts

    Attributes:
        roster: List of FantasyPlayer instances on the team
        pos_counts: Dictionary tracking count of players by position
        slot_assignments: Dictionary tracking which players are in which slots
        bye_week_counts: Dictionary tracking bye week distribution by position
        draft_order: List representing draft order with player assignments
    """
    def __init__(self, players=None):
        """
        Initialize a FantasyTeam instance.

        Args:
            players: Optional list of FantasyPlayer instances to initialize roster with.
                    If None, starts with an empty roster.
        """
        self.logger = get_logger()
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

        # NEW: Explicit slot tracking - Track actual slot assignments
        self.slot_assignments = {
            Constants.QB: [],     # List of player IDs in QB slots
            Constants.RB: [],     # List of player IDs in RB slots
            Constants.WR: [],     # List of player IDs in WR slots
            Constants.TE: [],     # List of player IDs in TE slots
            Constants.FLEX: [],   # List of player IDs in FLEX slot
            Constants.K: [],      # List of player IDs in K slots
            Constants.DST: []     # List of player IDs in DST slots
        }
        
        # Pre-compute bye week counts by position for efficient penalty calculation
        # Structure: {bye_week: {position: count}}
        self.bye_week_counts = {}
        for bye_week in Constants.POSSIBLE_BYE_WEEKS:
            self.bye_week_counts[bye_week] = {pos: 0 for pos in Constants.MAX_POSITIONS.keys()}
        
        # Set up the draft order list
        self.draft_order = [None] * Constants.MAX_PLAYERS

        # Initialize slot assignments for existing players
        for player in self.roster:
            self._assign_player_to_slot(player)

        # place in the draft order
        for player in self.roster:
            pos = player.position
            pos_with_flex = Constants.FLEX if pos in Constants.FLEX_ELIGIBLE_POSITIONS else pos
            for i in range(Constants.MAX_PLAYERS):
                if self.draft_order[i] is None and pos_with_flex == Constants.get_ideal_draft_position(i):
                    self.draft_order[i] = player
                    break

        self.logger.debug(f"position counts after labeling: {self.pos_counts}")
        self.logger.debug(f"slot assignments after initialization: {self.slot_assignments}")
        self.logger.debug(f"draft_order after assignment: {[p.id if p else None for p in self.draft_order]}")
        self.logger.info(f"FantasyTeam initialized. Roster size: {len(self.roster)}")

    def _assign_player_to_slot(self, player):
        """
        Assign a player to the appropriate slot and update counts.

        Args:
            player: FantasyPlayer instance

        Returns:
            str: The slot the player was assigned to

        Raises:
            ValueError: If the player cannot be assigned to any available slot
        """
        pos = player.position

        # Try natural position first
        if len(self.slot_assignments[pos]) < Constants.MAX_POSITIONS[pos]:
            self.slot_assignments[pos].append(player.id)
            assigned_slot = pos
            self.logger.debug(f"SLOT ASSIGN: {player.name} ({pos}) → {pos} slot. Slot {pos} now has {len(self.slot_assignments[pos])} players")
        # Try FLEX if eligible
        elif (pos in Constants.FLEX_ELIGIBLE_POSITIONS and
              len(self.slot_assignments[Constants.FLEX]) < Constants.MAX_POSITIONS[Constants.FLEX]):
            self.slot_assignments[Constants.FLEX].append(player.id)
            assigned_slot = Constants.FLEX
            self.logger.debug(f"SLOT ASSIGN: {player.name} ({pos}) → FLEX slot. FLEX now has {len(self.slot_assignments[Constants.FLEX])} players")
        else:
            raise ValueError(f"Cannot assign {player.name} ({pos}) to any available slot. Slots full: {pos}={len(self.slot_assignments[pos])}/{Constants.MAX_POSITIONS[pos]}, FLEX={len(self.slot_assignments[Constants.FLEX])}/{Constants.MAX_POSITIONS[Constants.FLEX]}")

        # Always increment the position count for the player's original position
        # This tracks total players by position regardless of slot assignment
        self.pos_counts[pos] += 1
        # Also increment FLEX count if assigned to FLEX slot
        if assigned_slot == Constants.FLEX:
            self.pos_counts[Constants.FLEX] += 1

        # Update bye week counts
        if player.bye_week and player.bye_week in self.bye_week_counts:
            self.bye_week_counts[player.bye_week][pos] += 1

        return assigned_slot

    # Method to get the next draft position weights based on the current roster
    def get_next_draft_position_weights(self):
        """
        Get the position weights for the next draft pick based on current roster needs.

        Returns:
            dict or None: Dictionary mapping positions to weight values for next pick,
                         or None if draft is complete
        """
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
        """
        Check if a player of the given position can be drafted into the FLEX slot.

        A position is FLEX eligible when:
        1. The position is RB or WR (FLEX eligible positions)
        2. The primary position slots are full
        3. The FLEX slot is available

        Args:
            pos: Position string (e.g., 'RB', 'WR', 'QB')

        Returns:
            bool: True if the position can be drafted to FLEX, False otherwise
        """
        # Check if player can be drafted as a FLEX
        if pos not in Constants.FLEX_ELIGIBLE_POSITIONS:
            self.logger.debug(f"Position {pos} not FLEX eligible")
            return False

        # Check actual slot occupancy, not position counts
        # pos_counts includes players in FLEX slots, but we need to check natural position slots only
        pos_slots_full = len(self.slot_assignments[pos]) >= Constants.MAX_POSITIONS[pos]
        flex_available = len(self.slot_assignments[Constants.FLEX]) < Constants.MAX_POSITIONS[Constants.FLEX]
        result = pos_slots_full and flex_available

        self.logger.debug(f"FLEX eligibility for {pos}: pos_slots_full={pos_slots_full} ({len(self.slot_assignments[pos])}>={Constants.MAX_POSITIONS[pos]}), flex_available={flex_available} ({len(self.slot_assignments[Constants.FLEX])}<{Constants.MAX_POSITIONS[Constants.FLEX]}), result={result}")
        return result

    # Method to check if a player can be drafted
    def can_draft(self, player):
        """
        Check if a player can be drafted to the team.

        Validates:
        - Roster has space available
        - Player's position is valid
        - Position limit not exceeded (including FLEX eligibility)
        - Player is available (not already drafted)
        - Player has valid bye week

        Args:
            player: FantasyPlayer instance to check

        Returns:
            bool: True if player can be drafted, False otherwise
        """
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
        # Use slot occupancy for natural position, not pos_counts (which includes FLEX players)
        natural_slots_full = len(self.slot_assignments[pos]) >= Constants.MAX_POSITIONS[pos]
        if natural_slots_full and not self.flex_eligible(pos):
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
        """
        Draft a player onto the team.

        Updates the player's drafted status, adds them to the roster,
        assigns them to an appropriate slot, and updates all tracking data.

        Args:
            player: FantasyPlayer instance to draft

        Returns:
            bool: True if draft was successful, False if it failed
        """
        self.logger.debug(f"FantasyTeam.draft_player called for player ID: {player.id}")
        can_draft = self.can_draft(player)
        if can_draft:
            player.drafted = 2
            self.roster.append(player)

            # Use explicit slot assignment
            try:
                assigned_slot = self._assign_player_to_slot(player)
                self.logger.info(f"DRAFT SUCCESS: {player.name} ({player.position}) → {assigned_slot} slot")
            except ValueError as e:
                # This should not happen if can_draft is working correctly
                self.logger.error(f"DRAFT FAILED: Could not assign slot for {player.name}: {e}")
                # Rollback the draft
                self.roster.remove(player)
                player.drafted = 0
                return False

            self.logger.debug(f"Player {player.id} drafted successfully. Roster size now {len(self.roster)}.")
            self.logger.debug(f"Current slot assignments: {self.slot_assignments}")
            return True
        else:
            self.logger.debug(f"Player {player.id} could not be drafted.")
            return False

    # Method to remove a player from the team (for trade helper)
    def remove_player(self, player):
        """
        Remove a player from the team roster.

        Removes the player from roster, clears their slot assignment,
        updates all tracking data, and resets their drafted status.

        Args:
            player: FantasyPlayer instance to remove

        Returns:
            bool: True if removal was successful, False if player not found
        """
        self.logger.debug(f"FantasyTeam.remove_player called for player ID: {player.id}")
        if player not in self.roster:
            self.logger.debug(f"Player {player.id} not in roster, cannot remove.")
            return False

        # Find which slot the player is actually in using explicit tracking
        player_slot = None
        for slot, player_ids in self.slot_assignments.items():
            if player.id in player_ids:
                player_slot = slot
                player_ids.remove(player.id)
                break

        if player_slot is None:
            self.logger.error(f"REMOVAL ERROR: Player {player.name} ({player.id}) not found in any slot assignments")
            return False

        # Remove from roster and update counts
        self.roster.remove(player)
        player.drafted = 0  # Mark as available again

        # Decrement position count for player's original position
        self.pos_counts[player.position] -= 1
        # Also decrement slot count if it was in FLEX
        if player_slot == Constants.FLEX:
            self.pos_counts[Constants.FLEX] -= 1

        self.logger.info(f"REMOVAL SUCCESS: {player.name} ({player.position}) removed from {player_slot} slot. New {player.position} count: {self.pos_counts[player.position]}")

        # Update bye week counts
        if player.bye_week and player.bye_week in self.bye_week_counts:
            self.bye_week_counts[player.bye_week][player.position] -= 1

        # Remove from draft order
        for i in range(Constants.MAX_PLAYERS):
            if self.draft_order[i] == player:
                self.draft_order[i] = None
                break

        self.logger.debug(f"Player {player.id} removed successfully. Roster size now {len(self.roster)}.")
        self.logger.debug(f"Current slot assignments: {self.slot_assignments}")
        return True

    # Method to replace a player atomically (for trade helper)
    def replace_player(self, old_player, new_player):
        """
        Replace one player on the roster with another player.

        This is used for trades and waiver moves. Validates that the new player
        can fill the slot being vacated by the old player.

        Args:
            old_player: FantasyPlayer instance currently on roster
            new_player: FantasyPlayer instance to add to roster

        Returns:
            bool: True if replacement was successful, False otherwise
        """
        self.logger.debug(f"FantasyTeam.replace_player called: {old_player.id} -> {new_player.id}")

        # Check if we can make this swap while maintaining position constraints
        if not self._can_replace_player(old_player, new_player):
            self.logger.debug(f"Cannot replace {old_player.id} with {new_player.id} due to position constraints.")
            return False

        # Store the old player's slot for optimal replacement
        old_player_slot = None
        for slot, player_ids in self.slot_assignments.items():
            if old_player.id in player_ids:
                old_player_slot = slot
                break

        if old_player_slot is None:
            self.logger.error(f"REPLACE ERROR: Old player {old_player.name} not found in slot assignments")
            return False

        # Remove old player
        if not self.remove_player(old_player):
            return False

        # Add new player (it will automatically find the best available slot)
        if not self.draft_player(new_player):
            # If adding new player fails, add the old player back
            self.logger.warning(f"REPLACE ROLLBACK: Failed to add {new_player.name}, restoring {old_player.name}")
            self.draft_player(old_player)
            return False

        self.logger.info(f"REPLACE SUCCESS: {old_player.name} ({old_player.position}) -> {new_player.name} ({new_player.position})")
        self.logger.debug(f"Current slot assignments after replacement: {self.slot_assignments}")
        return True
    
    # Helper method to check if a player replacement is valid
    def _can_replace_player(self, old_player, new_player):
        """
        Check if a player replacement is valid using explicit slot tracking.

        Args:
            old_player: FantasyPlayer to be replaced
            new_player: FantasyPlayer to replace with

        Returns:
            bool: True if replacement is valid, False otherwise
        """
        # For same position, always allowed
        if old_player.position == new_player.position:
            return True

        # For FLEX eligible positions (RB <-> WR trades), check using explicit slot tracking
        if (old_player.position in Constants.FLEX_ELIGIBLE_POSITIONS and
            new_player.position in Constants.FLEX_ELIGIBLE_POSITIONS):

            # Find which slot the old player currently occupies
            old_player_slot = None
            for slot, player_ids in self.slot_assignments.items():
                if old_player.id in player_ids:
                    old_player_slot = slot
                    break

            if old_player_slot is None:
                self.logger.warning(f"Cannot find slot assignment for {old_player.name}")
                return False

            # Simulate the replacement: temporarily remove old player and see if new player can fit
            temp_slot_assignments = {slot: player_ids.copy() for slot, player_ids in self.slot_assignments.items()}

            # Remove old player from temp assignments
            temp_slot_assignments[old_player_slot].remove(old_player.id)

            # Check if new player can be assigned to any available slot
            new_pos = new_player.position

            # Try natural position first
            if len(temp_slot_assignments[new_pos]) < Constants.MAX_POSITIONS[new_pos]:
                self.logger.debug(f"Replace validation: {new_player.name} can fit in {new_pos} slot")
                return True

            # Try FLEX if eligible
            elif (new_pos in Constants.FLEX_ELIGIBLE_POSITIONS and
                  len(temp_slot_assignments[Constants.FLEX]) < Constants.MAX_POSITIONS[Constants.FLEX]):
                self.logger.debug(f"Replace validation: {new_player.name} can fit in FLEX slot")
                return True

            else:
                self.logger.debug(f"Replace validation: No available slots for {new_player.name} ({new_pos})")
                return False

        # Different position types not in FLEX eligibles - not allowed for now
        self.logger.debug(f"Replace validation: Cannot replace {old_player.position} with {new_player.position} (not FLEX eligible)")
        return False

    # Method to get total team score for trade optimization
    def get_total_team_score(self, scoring_function):
        """
        Calculate the total fantasy points for all players on the roster using a scoring function.

        Args:
            scoring_function: Function that takes a player and returns their score

        Returns:
            float: Sum of scores for all players on the team
        """
        self.logger.debug("FantasyTeam.get_total_team_score called")
        total_score = 0
        for player in self.roster:
            total_score += scoring_function(player)
        return total_score

    def get_players_by_slot(self, slot):
        """
        Get all players assigned to a specific slot.

        Args:
            slot: Position slot ('QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX')

        Returns:
            List[FantasyPlayer]: Players assigned to the slot
        """
        player_ids = self.slot_assignments.get(slot, [])
        return [p for p in self.roster if p.id in player_ids]

    def get_weakest_player_by_position(self, position, scoring_function):
        """
        Get the weakest player of a given position for trade optimization.

        Args:
            position: Player position ('QB', 'RB', 'WR', 'TE', 'K', 'DST')
            scoring_function: Function to score players

        Returns:
            FantasyPlayer or None: Weakest player of that position
        """
        position_players = [p for p in self.roster if p.position == position]
        if not position_players:
            return None

        # Find the player with the lowest score
        weakest = min(position_players, key=scoring_function)
        return weakest

    def get_optimal_slot_for_player(self, player):
        """
        Determine the optimal slot assignment for a FLEX-eligible player.

        For FLEX-eligible positions, prioritize:
        1. Natural position slot if available
        2. FLEX slot if natural position is full

        Args:
            player: FantasyPlayer instance

        Returns:
            str: Optimal slot ('RB', 'WR', 'FLEX', etc.) or None if no slots available
        """
        pos = player.position

        # For non-FLEX eligible positions, only one option
        if pos not in Constants.FLEX_ELIGIBLE_POSITIONS:
            if len(self.slot_assignments[pos]) < Constants.MAX_POSITIONS[pos]:
                return pos
            else:
                return None

        # For FLEX-eligible positions, prioritize natural position
        if len(self.slot_assignments[pos]) < Constants.MAX_POSITIONS[pos]:
            return pos
        elif len(self.slot_assignments[Constants.FLEX]) < Constants.MAX_POSITIONS[Constants.FLEX]:
            return Constants.FLEX
        else:
            return None

    def optimize_flex_assignments(self, scoring_function):
        """
        Optimize FLEX assignments by moving the highest-scoring FLEX player
        to their natural position if possible.

        Args:
            scoring_function: Function to score players

        Returns:
            bool: True if any optimization was performed
        """
        flex_players = self.get_players_by_slot(Constants.FLEX)
        if not flex_players:
            return False

        optimized = False

        # Sort FLEX players by score (highest first)
        flex_players_sorted = sorted(flex_players, key=scoring_function, reverse=True)

        for flex_player in flex_players_sorted:
            natural_pos = flex_player.position

            # Check if natural position has available space
            if len(self.slot_assignments[natural_pos]) < Constants.MAX_POSITIONS[natural_pos]:
                # Check if there's a weaker player in natural position to potentially move to FLEX
                natural_pos_players = self.get_players_by_slot(natural_pos)

                if natural_pos_players:
                    weakest_natural = min(natural_pos_players, key=scoring_function)

                    # If FLEX player scores higher than weakest in natural position, swap them
                    if scoring_function(flex_player) > scoring_function(weakest_natural):
                        self.logger.info(f"FLEX OPTIMIZATION: Swapping {flex_player.name} (FLEX) with {weakest_natural.name} ({natural_pos})")

                        # Remove both players from their slots
                        self.slot_assignments[Constants.FLEX].remove(flex_player.id)
                        self.slot_assignments[natural_pos].remove(weakest_natural.id)

                        # Reassign them optimally
                        self.slot_assignments[natural_pos].append(flex_player.id)
                        self.slot_assignments[Constants.FLEX].append(weakest_natural.id)

                        optimized = True
                else:
                    # Natural position is empty, move FLEX player there
                    self.logger.info(f"FLEX OPTIMIZATION: Moving {flex_player.name} from FLEX to {natural_pos}")

                    self.slot_assignments[Constants.FLEX].remove(flex_player.id)
                    self.slot_assignments[natural_pos].append(flex_player.id)
                    self.pos_counts[Constants.FLEX] -= 1
                    self.pos_counts[natural_pos] += 1

                    optimized = True

        return optimized

    def copy_team(self):
        """Create a deep copy of the team for simulation purposes"""
        import copy
        new_team = FantasyTeam()
        new_team.roster = copy.deepcopy(self.roster)
        new_team.draft_order = copy.deepcopy(self.draft_order)
        new_team.pos_counts = copy.deepcopy(self.pos_counts)
        new_team.slot_assignments = copy.deepcopy(self.slot_assignments)
        new_team.bye_week_counts = copy.deepcopy(self.bye_week_counts)
        return new_team

    def _recalculate_position_counts(self):
        """Recalculate position counts based on current roster and slot assignments"""
        # Reset counts
        for pos in self.pos_counts:
            self.pos_counts[pos] = 0

        # Count players by their original position
        for player in self.roster:
            self.pos_counts[player.position] += 1

        # Count players in FLEX slot
        self.pos_counts[Constants.FLEX] = len(self.slot_assignments[Constants.FLEX])

    def validate_roster_integrity(self):
        """Validate that position counts match actual roster composition and slot assignments"""
        errors = []

        # Recalculate position counts to ensure they're accurate
        self._recalculate_position_counts()

        # Use slot assignments as the source of truth for slot validation
        slot_based_counts = {pos: len(player_ids) for pos, player_ids in self.slot_assignments.items()}

        # For slot-based validation, only validate slots that aren't position-based
        # FLEX is special because it can contain players of different positions
        for pos, slot_count in slot_based_counts.items():
            tracked_count = self.pos_counts.get(pos, 0)
            if pos == Constants.FLEX:
                # FLEX count should match slot assignment
                if slot_count != tracked_count:
                    errors.append(f"Position {pos}: {slot_count} in slots != {tracked_count} tracked count")
            else:
                # For position-based slots, the slot count should not exceed the tracked count
                # (because some players of this position might be in FLEX)
                if slot_count > tracked_count:
                    errors.append(f"Position {pos}: {slot_count} in slots > {tracked_count} tracked count")

        # Check that no position exceeds maximum
        for pos, count in slot_based_counts.items():
            max_allowed = Constants.MAX_POSITIONS.get(pos, 0)
            if count > max_allowed:
                errors.append(f"Position {pos}: {count} players > {max_allowed} maximum allowed")

        # Check total roster size
        total_players = len(self.roster)
        if total_players > Constants.MAX_PLAYERS:
            errors.append(f"Total roster: {total_players} players > {Constants.MAX_PLAYERS} maximum")

        # Check for duplicate players
        player_ids = [p.id for p in self.roster]
        if len(player_ids) != len(set(player_ids)):
            duplicates = [pid for pid in player_ids if player_ids.count(pid) > 1]
            errors.append(f"Duplicate players found: {set(duplicates)}")

        # Check that all roster players are assigned to slots
        assigned_player_ids = set()
        for slot, player_ids_in_slot in self.slot_assignments.items():
            assigned_player_ids.update(player_ids_in_slot)

        roster_player_ids = {p.id for p in self.roster}

        if assigned_player_ids != roster_player_ids:
            missing = roster_player_ids - assigned_player_ids
            extra = assigned_player_ids - roster_player_ids
            if missing:
                errors.append(f"Players in roster but not assigned to slots: {missing}")
            if extra:
                errors.append(f"Players assigned to slots but not in roster: {extra}")

        # Log results
        if errors:
            error_msg = f"Roster integrity validation failed: {'; '.join(errors)}"
            self.logger.error(error_msg)
            self.logger.debug(f"Slot-based counts: {slot_based_counts}")
            self.logger.debug(f"Tracked counts: {self.pos_counts}")
            self.logger.debug(f"Slot assignments: {self.slot_assignments}")
            return False
        else:
            self.logger.debug("Roster integrity validation passed")
            return True

    def get_slot_assignment(self, player):
        """
        Determine which slot a player is currently assigned to using explicit slot tracking.

        Args:
            player: FantasyPlayer instance

        Returns:
            str: Position slot ('QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX') or None if not found
        """
        if player not in self.roster:
            return None

        # Use explicit slot tracking for accurate assignment
        for slot, player_ids in self.slot_assignments.items():
            if player.id in player_ids:
                return slot

        # Player is in roster but not in slot assignments - this is an error
        self.logger.warning(f"Player {player.name} ({player.id}) is in roster but not assigned to any slot")
        return None

    # print the ideal draft order, and what the actual draft order is
    def print_draft_order(self):
        """
        Print the current draft order showing round-by-round roster composition.

        Displays each round with the ideal position, actual player assigned,
        and whether the assignment matches the ideal position.
        """
        self.logger.debug("FantasyTeam.print_draft_order called")
        for i, pos in enumerate(Constants.DRAFT_ORDER):
            print(f"Round {i + 1}: {', '.join(pos.keys())} -- Drafted: {self.draft_order[i].name if self.draft_order[i] else 'None'} ({self.draft_order[i].position if self.draft_order[i] else 'None'})")
