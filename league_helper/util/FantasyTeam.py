"""
Fantasy Team Manager

Manages a fantasy football team roster with position limits and draft order.
Handles player drafting, roster operations, FLEX slot logic, and position limits.

Key responsibilities:
- Tracking drafted players and roster composition
- Enforcing position limits (QB: 2, RB: 4, WR: 4, TE: 2, K: 1, DST: 1, FLEX: 1)
- Managing FLEX eligibility (RB/WR/DST can fill FLEX when natural position full)
- Slot assignment tracking (natural position vs FLEX)
- Bye week tracking for roster optimization
- Player replacement for trades

Author: Kai Mizuno
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Callable

from util.ConfigManager import ConfigManager

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
import constants as Constants

parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer


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

    # ============================================================================
    # INITIALIZATION
    # ============================================================================

    def __init__(self, config : ConfigManager, players : List[FantasyPlayer] = []) -> None:
        """
        Initialize a FantasyTeam instance.

        Args:
            players: Optional list of FantasyPlayer instances to initialize roster with.
                    If None, starts with an empty roster.
        """
        self.config = config
        self.logger = get_logger()
        self.logger.debug(f"FantasyTeam.__init__ called with {len(players) if players else 0} players")
        # Roster holds Player instances drafted so far
        self.roster : List[FantasyPlayer] = []
        self.injury_reserve : List[FantasyPlayer] = []
        for player in players:
            if player.injury_status not in ["ACTIVE", "QUESTIONABLE"]:
                self.injury_reserve.append(player)
            else:
                self.roster.append(player)

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

        # Explicit slot tracking - Track actual slot assignments
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
            self.bye_week_counts[bye_week] = {pos: 0 for pos in self.config.max_positions.keys()}

        # Set up the draft order list
        self.draft_order = [None] * self.config.max_players

        # Initialize slot assignments for existing players
        for player in self.roster:
            self._assign_player_to_slot(player)

        # place in the draft order
        for player in self.roster:
            pos = player.position
            pos_with_flex = Constants.FLEX if pos in self.config.flex_eligible_positions else pos
            for i in range(self.config.max_players):
                if self.draft_order[i] is None and pos_with_flex == self.config.get_ideal_draft_position(i):
                    self.draft_order[i] = player
                    break

        self.logger.debug(f"position counts after labeling: {self.pos_counts}")
        self.logger.debug(f"slot assignments after initialization: {self.slot_assignments}")
        self.logger.debug(f"draft_order after assignment: {[p.id if p else None for p in self.draft_order]}")
        self.logger.debug(f"FantasyTeam initialized. Roster size: {len(self.roster)}")

    # ============================================================================
    # PUBLIC DRAFT OPERATIONS
    # ============================================================================

    # Method to check if a player can be drafted
    def can_draft(self, player : FantasyPlayer) -> bool:
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
        if len(self.roster) >= self.config.max_players:
            self.logger.debug("Roster full, cannot draft.")
            return False

        # Check if player position is valid
        pos = player.position
        if pos not in self.config.max_positions:
            self.logger.debug(f"Invalid position {pos}, cannot draft.")
            return False

        # Check if position limit is reached
        # Use slot occupancy for natural position, not pos_counts (which includes FLEX players)
        natural_slots_full = len(self.slot_assignments[pos]) >= self.config.max_positions[pos]
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
    def draft_player(self, player : FantasyPlayer) -> bool:
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
                self.logger.debug(f"DRAFT SUCCESS: {player.name} ({player.position}) → {assigned_slot} slot")
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
    def remove_player(self, player : FantasyPlayer) -> bool:
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
        for i in range(self.config.max_players):
            if self.draft_order[i] == player:
                self.draft_order[i] = None
                break

        self.logger.debug(f"Player {player.id} removed successfully. Roster size now {len(self.roster)}.")
        self.logger.debug(f"Current slot assignments: {self.slot_assignments}")
        return True

    # Method to replace a player atomically (for trade helper)
    def replace_player(self, old_player : FantasyPlayer, new_player : FantasyPlayer) -> bool:
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

    # ============================================================================
    # PUBLIC ROSTER QUERIES
    # ============================================================================

    # Method to get the next draft position weights based on the current roster
    def get_next_draft_position_weights(self) -> Optional[Dict[str, str]]:
        """
        Get the position weights for the next draft pick based on current roster needs.

        Returns:
            dict or None: Dictionary mapping positions to weight values for next pick,
                         or None if draft is complete
        """
        self.logger.debug("FantasyTeam.get_next_draft_position_weights called")
        # Find the next open draft position
        for i in range(self.config.max_players):
            if self.draft_order[i] is None:
                self.logger.debug(f"Next draft position weights: {self.config.draft_order[i]}")
                return self.config.draft_order[i]
        self.logger.debug("No draft position weights available (draft full)")
        return None

    # Method to get total team score for trade optimization
    def get_total_team_score(self, scoring_function: Callable[[FantasyPlayer], float]) -> float:
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

    def get_players_by_slot(self, slot : str) -> List[FantasyPlayer]:
        """
        Get all players assigned to a specific slot.

        Args:
            slot: Position slot ('QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX')

        Returns:
            List[FantasyPlayer]: Players assigned to the slot
        """
        player_ids = self.slot_assignments.get(slot, [])
        return [p for p in self.roster if p.id in player_ids]

    def get_weakest_player_by_position(self, position : str, scoring_function: Callable[[FantasyPlayer], float]) -> Optional[FantasyPlayer]:
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

    def get_optimal_slot_for_player(self, player: FantasyPlayer) -> Optional[str]:
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
        if pos not in self.config.flex_eligible_positions:
            if len(self.slot_assignments[pos]) < self.config.max_positions[pos]:
                return pos
            else:
                return None

        # For FLEX-eligible positions, prioritize natural position
        if len(self.slot_assignments[pos]) < self.config.max_positions[pos]:
            return pos
        elif len(self.slot_assignments[Constants.FLEX]) < self.config.max_positions[Constants.FLEX]:
            return Constants.FLEX
        else:
            return None

    def get_slot_assignment(self, player: FantasyPlayer) -> Optional[str]:
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

    def get_matching_byes_in_roster(self, bye_week : int, position : str, is_rostered : bool) -> int:
        """
        Count how many players at a given position share the same bye week.

        This is used for bye week penalty calculations when evaluating draft picks.
        The is_rostered parameter accounts for whether the player being evaluated
        is already on the roster (to avoid double-counting them).

        Args:
            bye_week: Bye week number to check (typically 4-14)
            position: Position to filter by (QB, RB, WR, TE, K, DST)
            is_rostered: Whether the player being evaluated is already rostered
                        (if True, subtract 1 to avoid counting them twice)

        Returns:
            int: Number of matching players (excluding the evaluated player if already rostered)
        """
        # Count roster players with matching bye week and position
        matches = 0

        for p in self.roster:
            # Check if player matches both bye week and position criteria
            if p.bye_week == bye_week and p.position == position:
                matches += 1

        # If the player being evaluated is already on roster, don't count them twice
        # This prevents inflating the penalty when re-evaluating an existing roster player
        if is_rostered:
            matches -= 1
        return matches

    # ============================================================================
    # PUBLIC VALIDATION METHODS
    # ============================================================================

    # Method to check if a player can be drafted as a FLEX position
    # A player is eligible to be labeled as the 'FLEX' position if:
    # 1. Their position is one of the FLEX eligible positions (RB or WR or DST)
    # 2. Their primary position is already at the max limit
    # 3. The FLEX position itself is not yet filled to its max limit
    # This allows drafting a player into the FLEX spot when their main position is full
    # but there is still room in the FLEX slot.
    def flex_eligible(self, pos : str) -> bool:
        """
        Check if a player of the given position can be drafted into the FLEX slot.

        A position is FLEX eligible when:
        1. The position is RB, WR, or DST (FLEX eligible positions)
        2. The primary position slots are full
        3. The FLEX slot is available

        Args:
            pos: Position string (e.g., 'RB', 'WR', 'QB')

        Returns:
            bool: True if the position can be drafted to FLEX, False otherwise
        """
        # First requirement: Position must be one of the FLEX-eligible types
        # Only RB and WR can fill the FLEX slot
        # QB, TE, K, and DST cannot be assigned to FLEX
        if pos not in self.config.flex_eligible_positions:
            self.logger.debug(f"Position {pos} not FLEX eligible")
            return False

        # Second requirement: Natural position slots must be full
        # IMPORTANT: We check slot_assignments[pos], NOT pos_counts
        # Why? pos_counts includes players in FLEX, which would give wrong results
        # Example: 4 RBs total with 1 in FLEX would show pos_counts[RB]=5 (4+1)
        #          but slot_assignments[RB]=4 (the actual RB slots)
        pos_slots_full = len(self.slot_assignments[pos]) >= self.config.max_positions[pos]

        # Third requirement: FLEX slot must have space available
        # The FLEX slot can only hold 1 player (MAX_POSITIONS[FLEX] = 1)
        flex_available = len(self.slot_assignments[Constants.FLEX]) < self.config.max_positions[Constants.FLEX]

        # Both conditions must be true: natural position full AND FLEX available
        result = pos_slots_full and flex_available

        self.logger.debug(f"FLEX eligibility for {pos}: pos_slots_full={pos_slots_full} ({len(self.slot_assignments[pos])}>={self.config.max_positions[pos]}), flex_available={flex_available} ({len(self.slot_assignments[Constants.FLEX])}<{self.config.max_positions[Constants.FLEX]}), result={result}")
        return result

    def validate_roster_integrity(self) -> bool:
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
            max_allowed = self.config.max_positions.get(pos, 0)
            if count > max_allowed:
                errors.append(f"Position {pos}: {count} players > {max_allowed} maximum allowed")

        # Check total roster size
        total_players = len(self.roster)
        if total_players > self.config.max_players:
            errors.append(f"Total roster: {total_players} players > {self.config.max_players} maximum")

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

    # ============================================================================
    # PUBLIC UTILITY METHODS
    # ============================================================================

    def set_score(self, id : int, score : float) -> None:
        """
        Set the score for a specific player on the roster.

        Args:
            id: Player ID to update
            score: New score value to assign
        """
        # Iterate through roster to find the matching player by ID
        for p in self.roster:
            if p.id == id:
                # Update the player's score and exit early
                p.score = score
                break

    def optimize_flex_assignments(self, scoring_function: Callable[[FantasyPlayer], float]) -> bool:
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
            if len(self.slot_assignments[natural_pos]) < self.config.max_positions[natural_pos]:
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

    def copy_team(self) -> 'FantasyTeam':
        """Create a deep copy of the team for simulation purposes"""
        import copy
        new_team = FantasyTeam(self.config, players=[])
        new_team.roster = copy.deepcopy(self.roster)
        new_team.injury_reserve = copy.deepcopy(self.injury_reserve)
        new_team.draft_order = copy.deepcopy(self.draft_order)
        new_team.pos_counts = copy.deepcopy(self.pos_counts)
        new_team.slot_assignments = copy.deepcopy(self.slot_assignments)
        new_team.bye_week_counts = copy.deepcopy(self.bye_week_counts)
        return new_team

    def display_roster(self) -> None:
        """Display current roster organized by position and calling out bye weeks"""
        print(f"\nCurrent Roster by Position:")
        print("-" * 40)

        # Define the order for displaying positions
        # This provides a logical flow: QB → RB → WR → TE → K → DST
        display_order = [Constants.QB, Constants.RB, Constants.WR, Constants.TE, Constants.K, Constants.DST]

        # Initialize bye week dictionary to track players by their bye week
        # This will be populated as we iterate through players
        byes = dict.fromkeys(Constants.POSSIBLE_BYE_WEEKS, [])

        # Display players grouped by position
        for pos in display_order:
            print(f"--- {pos} ---")

            # Get all players at this position
            pos_players = [p for p in self.roster if p.position == pos]

            # Sort players by score (highest first) for better readability
            pos_players.sort(key=lambda item: item.score, reverse=True)

            # Print each player and track their bye week
            for p in pos_players:
                byes[p.bye_week].append(p)
                print(p)

        # Display injury reserve players (players not in active roster)
        print ("-- Injury Reserve --")
        for ir in self.injury_reserve:
            print(ir)

        # Display bye week summary showing which players are off in upcoming weeks
        # Only show bye weeks that haven't passed yet
        print("-- Bye Weeks --")
        for bye, player_list in byes.items():
            # Only display future bye weeks (current week or later)
            if self.config.current_nfl_week <= bye:
                # Format player names with positions for clarity
                name_list = [f"{n.name} ({n.position})" for n in player_list if n.bye_week == bye]
                print(f"  Week {bye}: {name_list}")

        # Display roster size summary
        print("------")
        print(f"\nTotal roster: {len(self.roster)}/{self.config.max_players} players")

    # ============================================================================
    # PRIVATE SLOT MANAGEMENT
    # ============================================================================

    def _assign_player_to_slot(self, player : FantasyPlayer) -> str:
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

        # Slot assignment priority:
        # 1. Always try natural position first (e.g., RB goes to RB slot)
        # 2. If natural position is full and player is FLEX-eligible (RB/WR/DST),
        #    then assign to FLEX slot
        # 3. If both natural position and FLEX are full, raise error

        # Check if natural position has available slots
        if len(self.slot_assignments[pos]) < self.config.max_positions[pos]:
            # Natural position has space - assign here
            self.slot_assignments[pos].append(player.id)
            assigned_slot = pos
            self.logger.debug(f"SLOT ASSIGN: {player.name} ({pos}) → {pos} slot. Slot {pos} now has {len(self.slot_assignments[pos])} players")

        # Natural position is full - try FLEX if eligible
        elif (pos in self.config.flex_eligible_positions and
              len(self.slot_assignments[Constants.FLEX]) < self.config.max_positions[Constants.FLEX]):
            # Player is FLEX-eligible (RB/WR) and FLEX has space
            self.slot_assignments[Constants.FLEX].append(player.id)
            assigned_slot = Constants.FLEX
            self.logger.debug(f"SLOT ASSIGN: {player.name} ({pos}) → FLEX slot. FLEX now has {len(self.slot_assignments[Constants.FLEX])} players")

        # No available slots - cannot assign
        else:
            raise ValueError(f"Cannot assign {player.name} ({pos}) to any available slot. Slots full: {pos}={len(self.slot_assignments[pos])}/{self.config.max_positions[pos]}, FLEX={len(self.slot_assignments[Constants.FLEX])}/{self.config.max_positions[Constants.FLEX]}")

        # Update position counts for tracking
        # IMPORTANT: pos_counts tracks TWO things:
        # 1. Total count of each position type (e.g., how many RBs on team)
        # 2. Total count of players in FLEX slot specifically

        # Always increment the position count for the player's original position
        # This tracks total players by position regardless of slot assignment
        self.pos_counts[pos] += 1

        # Also increment FLEX count if assigned to FLEX slot
        # This means FLEX-eligible positions contribute to TWO counts:
        # - Their natural position count (for position limit enforcement)
        # - The FLEX count (for FLEX slot limit enforcement)
        if assigned_slot == Constants.FLEX:
            self.pos_counts[Constants.FLEX] += 1

        # Update bye week tracking for bye week penalty calculations
        # This helps identify roster construction issues where multiple
        # players at the same position share the same bye week
        if player.bye_week and player.bye_week in self.bye_week_counts:
            self.bye_week_counts[player.bye_week][pos] += 1

        return assigned_slot

    # ============================================================================
    # PRIVATE VALIDATION HELPERS
    # ============================================================================

    # Helper method to check if a player replacement is valid
    def _can_replace_player(self, old_player : FantasyPlayer, new_player : FantasyPlayer) -> bool:
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
        if (old_player.position in self.config.flex_eligible_positions and
            new_player.position in self.config.flex_eligible_positions):

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
            if len(temp_slot_assignments[new_pos]) < self.config.max_positions[new_pos]:
                self.logger.debug(f"Replace validation: {new_player.name} can fit in {new_pos} slot")
                return True

            # Try FLEX if eligible
            elif (new_pos in self.config.flex_eligible_positions and
                  len(temp_slot_assignments[Constants.FLEX]) < self.config.max_positions[Constants.FLEX]):
                self.logger.debug(f"Replace validation: {new_player.name} can fit in FLEX slot")
                return True

            else:
                self.logger.debug(f"Replace validation: No available slots for {new_player.name} ({new_pos})")
                return False

        # Different position types not in FLEX eligibles - not allowed for now
        self.logger.debug(f"Replace validation: Cannot replace {old_player.position} with {new_player.position} (not FLEX eligible)")
        return False

    def _recalculate_position_counts(self) -> None:
        """Recalculate position counts based on current roster and slot assignments"""
        # Reset counts
        for pos in self.pos_counts:
            self.pos_counts[pos] = 0

        # Count players by their original position
        for player in self.roster:
            self.pos_counts[player.position] += 1

        # Count players in FLEX slot
        self.pos_counts[Constants.FLEX] = len(self.slot_assignments[Constants.FLEX])
