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

from typing import List, Dict, Optional, Callable

from league_helper.util.ConfigManager import ConfigManager

import league_helper.constants as Constants
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
        self.roster : List[FantasyPlayer] = []
        self.injury_reserve : List[FantasyPlayer] = []
        for player in players:
            if player.get_risk_level() == "HIGH":
                self.injury_reserve.append(player)
            else:
                self.roster.append(player)

        self.pos_counts = {
            Constants.QB: 0,
            Constants.RB: 0,
            Constants.WR: 0,
            Constants.TE: 0,
            Constants.DST: 0,
            Constants.K: 0,
            Constants.FLEX: 0
        }

        self.slot_assignments = {
            Constants.QB: [],
            Constants.RB: [],
            Constants.WR: [],
            Constants.TE: [],
            Constants.FLEX: [],
            Constants.K: [],
            Constants.DST: []
        }

        self.bye_week_counts = {}
        for bye_week in Constants.POSSIBLE_BYE_WEEKS:
            self.bye_week_counts[bye_week] = {pos: 0 for pos in self.config.max_positions.keys()}

        self.draft_order = [None] * self.config.max_players

        for player in self.roster:
            self._assign_player_to_slot(player)

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
        if len(self.roster) >= self.config.max_players:
            return False

        pos = player.position
        if pos not in self.config.max_positions:
            return False

        natural_slots_full = len(self.slot_assignments[pos]) >= self.config.max_positions[pos]
        if natural_slots_full and not self.flex_eligible(pos):
            return False

        if not player.is_available():
            return False

        if player.bye_week is not None and player.bye_week not in Constants.POSSIBLE_BYE_WEEKS:
            return False

        return True

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
            player.drafted_by = Constants.FANTASY_TEAM_NAME
            self.roster.append(player)

            try:
                assigned_slot = self._assign_player_to_slot(player)
                self.logger.debug(f"DRAFT SUCCESS: {player.name} ({player.position}) → {assigned_slot} slot")
            except ValueError as e:
                self.logger.error(f"DRAFT FAILED: Could not assign slot for {player.name}: {e}")
                self.roster.remove(player)
                player.drafted_by = ""
                return False

            self.logger.debug(f"Player {player.id} drafted successfully. Roster size now {len(self.roster)}.")
            self.logger.debug(f"Current slot assignments: {self.slot_assignments}")
            return True
        else:
            self.logger.debug(f"Player {player.id} could not be drafted.")
            return False

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

        player_slot = None
        for slot, player_ids in self.slot_assignments.items():
            if player.id in player_ids:
                player_slot = slot
                player_ids.remove(player.id)
                break

        if player_slot is None:
            self.logger.error(f"REMOVAL ERROR: Player {player.name} ({player.id}) not found in any slot assignments")
            return False

        self.roster.remove(player)
        player.drafted_by = ""

        self.pos_counts[player.position] -= 1
        if player_slot == Constants.FLEX:
            self.pos_counts[Constants.FLEX] -= 1

        self.logger.info(f"REMOVAL SUCCESS: {player.name} ({player.position}) removed from {player_slot} slot. New {player.position} count: {self.pos_counts[player.position]}")

        if player.bye_week and player.bye_week in self.bye_week_counts:
            self.bye_week_counts[player.bye_week][player.position] -= 1

        for i in range(self.config.max_players):
            if self.draft_order[i] == player:
                self.draft_order[i] = None
                break

        self.logger.debug(f"Player {player.id} removed successfully. Roster size now {len(self.roster)}.")
        self.logger.debug(f"Current slot assignments: {self.slot_assignments}")
        return True

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

        if not self._can_replace_player(old_player, new_player):
            self.logger.debug(f"Cannot replace {old_player.id} with {new_player.id} due to position constraints.")
            return False

        old_player_slot = None
        for slot, player_ids in self.slot_assignments.items():
            if old_player.id in player_ids:
                old_player_slot = slot
                break

        if old_player_slot is None:
            self.logger.error(f"REPLACE ERROR: Old player {old_player.name} not found in slot assignments")
            return False

        if not self.remove_player(old_player):
            return False

        if not self.draft_player(new_player):
            self.logger.warning(f"REPLACE ROLLBACK: Failed to add {new_player.name}, restoring {old_player.name}")
            self.draft_player(old_player)
            return False

        self.logger.info(f"REPLACE SUCCESS: {old_player.name} ({old_player.position}) -> {new_player.name} ({new_player.position})")
        self.logger.debug(f"Current slot assignments after replacement: {self.slot_assignments}")
        return True


    def get_next_draft_position_weights(self) -> Optional[Dict[str, str]]:
        """
        Get the position weights for the next draft pick based on current roster needs.

        Returns:
            dict or None: Dictionary mapping positions to weight values for next pick,
                         or None if draft is complete
        """
        self.logger.debug("FantasyTeam.get_next_draft_position_weights called")
        for i in range(self.config.max_players):
            if self.draft_order[i] is None:
                self.logger.debug(f"Next draft position weights: {self.config.draft_order[i]}")
                return self.config.draft_order[i]
        self.logger.debug("No draft position weights available (draft full)")
        return None

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

        if pos not in self.config.flex_eligible_positions:
            if len(self.slot_assignments[pos]) < self.config.max_positions[pos]:
                return pos
            else:
                return None

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

        for slot, player_ids in self.slot_assignments.items():
            if player.id in player_ids:
                return slot

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
        matches = 0

        for p in self.roster:
            if p.bye_week == bye_week and p.position == position:
                matches += 1

        if is_rostered:
            matches -= 1
        return matches


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
        if pos not in self.config.flex_eligible_positions:
            self.logger.debug(f"Position {pos} not FLEX eligible")
            return False

        pos_slots_full = len(self.slot_assignments[pos]) >= self.config.max_positions[pos]

        flex_available = len(self.slot_assignments[Constants.FLEX]) < self.config.max_positions[Constants.FLEX]

        result = pos_slots_full and flex_available

        self.logger.debug(f"FLEX eligibility for {pos}: pos_slots_full={pos_slots_full} ({len(self.slot_assignments[pos])}>={self.config.max_positions[pos]}), flex_available={flex_available} ({len(self.slot_assignments[Constants.FLEX])}<{self.config.max_positions[Constants.FLEX]}), result={result}")
        return result

    def validate_roster_integrity(self) -> bool:
        """Validate that position counts match actual roster composition and slot assignments"""
        errors = []

        self._recalculate_position_counts()

        slot_based_counts = {pos: len(player_ids) for pos, player_ids in self.slot_assignments.items()}

        for pos, slot_count in slot_based_counts.items():
            tracked_count = self.pos_counts.get(pos, 0)
            if pos == Constants.FLEX:
                if slot_count != tracked_count:
                    errors.append(f"Position {pos}: {slot_count} in slots != {tracked_count} tracked count")
            else:
                if slot_count > tracked_count:
                    errors.append(f"Position {pos}: {slot_count} in slots > {tracked_count} tracked count")

        for pos, count in slot_based_counts.items():
            max_allowed = self.config.max_positions.get(pos, 0)
            if count > max_allowed:
                errors.append(f"Position {pos}: {count} players > {max_allowed} maximum allowed")

        total_players = len(self.roster)
        if total_players > self.config.max_players:
            errors.append(f"Total roster: {total_players} players > {self.config.max_players} maximum")

        player_ids = [p.id for p in self.roster]
        if len(player_ids) != len(set(player_ids)):
            duplicates = [pid for pid in player_ids if player_ids.count(pid) > 1]
            errors.append(f"Duplicate players found: {set(duplicates)}")

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


    def set_score(self, id : int, score : float) -> None:
        """
        Set the score for a specific player on the roster.

        Args:
            id: Player ID to update
            score: New score value to assign
        """
        for p in self.roster:
            if p.id == id:
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

        flex_players_sorted = sorted(flex_players, key=scoring_function, reverse=True)

        for flex_player in flex_players_sorted:
            natural_pos = flex_player.position

            if len(self.slot_assignments[natural_pos]) < self.config.max_positions[natural_pos]:
                natural_pos_players = self.get_players_by_slot(natural_pos)

                if natural_pos_players:
                    weakest_natural = min(natural_pos_players, key=scoring_function)

                    if scoring_function(flex_player) > scoring_function(weakest_natural):
                        self.logger.info(f"FLEX OPTIMIZATION: Swapping {flex_player.name} (FLEX) with {weakest_natural.name} ({natural_pos})")

                        self.slot_assignments[Constants.FLEX].remove(flex_player.id)
                        self.slot_assignments[natural_pos].remove(weakest_natural.id)

                        self.slot_assignments[natural_pos].append(flex_player.id)
                        self.slot_assignments[Constants.FLEX].append(weakest_natural.id)

                        optimized = True
                else:
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

        display_order = [Constants.QB, Constants.RB, Constants.WR, Constants.TE, Constants.K, Constants.DST]

        byes = dict.fromkeys(Constants.POSSIBLE_BYE_WEEKS, [])

        for pos in display_order:
            print(f"--- {pos} ---")

            pos_players = [p for p in self.roster if p.position == pos]

            pos_players.sort(key=lambda item: item.score, reverse=True)

            for p in pos_players:
                byes[p.bye_week].append(p)
                print(p)

        print ("-- Injury Reserve --")
        for ir in self.injury_reserve:
            print(ir)

        print("-- Bye Weeks --")
        for bye, player_list in byes.items():
            if self.config.current_nfl_week <= bye:
                name_list = [f"{n.name} ({n.position})" for n in player_list if n.bye_week == bye]
                print(f"  Week {bye}: {name_list}")

        print("------")
        print(f"\nTotal roster: {len(self.roster)}/{self.config.max_players} players")


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


        if len(self.slot_assignments[pos]) < self.config.max_positions[pos]:
            self.slot_assignments[pos].append(player.id)
            assigned_slot = pos
            self.logger.debug(f"SLOT ASSIGN: {player.name} ({pos}) → {pos} slot. Slot {pos} now has {len(self.slot_assignments[pos])} players")

        elif (pos in self.config.flex_eligible_positions and
              len(self.slot_assignments[Constants.FLEX]) < self.config.max_positions[Constants.FLEX]):
            self.slot_assignments[Constants.FLEX].append(player.id)
            assigned_slot = Constants.FLEX
            self.logger.debug(f"SLOT ASSIGN: {player.name} ({pos}) → FLEX slot. FLEX now has {len(self.slot_assignments[Constants.FLEX])} players")

        else:
            raise ValueError(f"Cannot assign {player.name} ({pos}) to any available slot. Slots full: {pos}={len(self.slot_assignments[pos])}/{self.config.max_positions[pos]}, FLEX={len(self.slot_assignments[Constants.FLEX])}/{self.config.max_positions[Constants.FLEX]}")


        self.pos_counts[pos] += 1

        if assigned_slot == Constants.FLEX:
            self.pos_counts[Constants.FLEX] += 1

        if player.bye_week and player.bye_week in self.bye_week_counts:
            self.bye_week_counts[player.bye_week][pos] += 1

        return assigned_slot


    def _can_replace_player(self, old_player : FantasyPlayer, new_player : FantasyPlayer) -> bool:
        """
        Check if a player replacement is valid using explicit slot tracking.

        Args:
            old_player: FantasyPlayer to be replaced
            new_player: FantasyPlayer to replace with

        Returns:
            bool: True if replacement is valid, False otherwise
        """
        if old_player.position == new_player.position:
            return True

        if (old_player.position in self.config.flex_eligible_positions and
            new_player.position in self.config.flex_eligible_positions):

            old_player_slot = None
            for slot, player_ids in self.slot_assignments.items():
                if old_player.id in player_ids:
                    old_player_slot = slot
                    break

            if old_player_slot is None:
                self.logger.warning(f"Cannot find slot assignment for {old_player.name}")
                return False

            temp_slot_assignments = {slot: player_ids.copy() for slot, player_ids in self.slot_assignments.items()}

            temp_slot_assignments[old_player_slot].remove(old_player.id)

            new_pos = new_player.position

            if len(temp_slot_assignments[new_pos]) < self.config.max_positions[new_pos]:
                self.logger.debug(f"Replace validation: {new_player.name} can fit in {new_pos} slot")
                return True

            elif (new_pos in self.config.flex_eligible_positions and
                  len(temp_slot_assignments[Constants.FLEX]) < self.config.max_positions[Constants.FLEX]):
                self.logger.debug(f"Replace validation: {new_player.name} can fit in FLEX slot")
                return True

            else:
                self.logger.debug(f"Replace validation: No available slots for {new_player.name} ({new_pos})")
                return False

        self.logger.debug(f"Replace validation: Cannot replace {old_player.position} with {new_player.position} (not FLEX eligible)")
        return False

    def _recalculate_position_counts(self) -> None:
        """Recalculate position counts based on current roster and slot assignments"""
        for pos in self.pos_counts:
            self.pos_counts[pos] = 0

        for player in self.roster:
            self.pos_counts[player.position] += 1

        self.pos_counts[Constants.FLEX] = len(self.slot_assignments[Constants.FLEX])


