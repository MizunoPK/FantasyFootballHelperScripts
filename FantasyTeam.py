from collections import Counter
import Constants
from logger import log

# FantasyTeam class to manage a fantasy football team
# It holds drafted players, manages roster limits, and draft order
# It also provides methods to draft players and check roster status
class FantasyTeam:
    def __init__(self, players=None):
        log(f"FantasyTeam.__init__ called with {len(players) if players else 0} players.")
        # Roster holds Player instances drafted so far
        self.roster = players if players else []

        # Label starters
        self.roster.sort(key=lambda x: x.original_adp)
        self.starter_counts = {
            Constants.QB: 0,
            Constants.RB: 0,
            Constants.WR: 0,
            Constants.TE: 0,
            Constants.DEF: 0,
            Constants.K: 0, 
            Constants.FLEX: 0
        }
        self.bench_counts = {
            Constants.QB: 0,
            Constants.RB: 0,
            Constants.WR: 0,
            Constants.TE: 0,
            Constants.DEF: 0,
            Constants.K: 0, 
            Constants.FLEX: 0
        }
        for player in self.roster:
            pos = player.position
            if self.starter_counts.get(pos, 0) < Constants.STARTERS_REQ.get(pos, 0):
                player.is_starter = True
                self.starter_counts[pos] += 1
            elif pos in Constants.FLEX_ELIGIBLE_POSITIONS and self.starter_counts[Constants.FLEX] < Constants.STARTERS_REQ[Constants.FLEX]:
                player.is_starter = True
                self.starter_counts[Constants.FLEX] += 1
            else:
                player.is_starter = False
                self.bench_counts[pos] += 1
        log(f"starter_counts after labeling: {self.starter_counts}")
        log(f"bench_counts after labeling: {self.bench_counts}")

        # Determine the draft order - holds the Player instances in the order they were drafted
        self.draft_order = [None] * Constants.MAX_PLAYERS
        for player in self.roster:
            pos = player.get_position_including_flex()
            for i in range(Constants.MAX_PLAYERS):
                if self.draft_order[i] is None and pos == Constants.get_ideal_draft_position(i):
                    self.draft_order[i] = player
                    break
        log(f"draft_order after assignment: {[p.id if p else None for p in self.draft_order]}")
        log(f"FantasyTeam initialized. Roster size: {len(self.roster)}")

    # Method to get the next draft position weights based on the current roster
    def get_next_draft_position_weights(self):
        log("FantasyTeam.get_next_draft_position_weights called")
        # Find the next open draft position
        for i in range(Constants.MAX_PLAYERS):
            if self.draft_order[i] is None:
                log(f"Next draft position weights: {Constants.DRAFT_ORDER[i]}")
                return Constants.DRAFT_ORDER[i]
        log("No draft position weights available (draft full)")
        return None

    # Method to get a count of players drafted by position
    def get_position_counts(self):
        log("FantasyTeam.get_position_counts called")
        # Count how many players drafted per position
        counts = Counter()
        for p in self.roster:
            if p.position in Constants.FLEX_ELIGIBLE_POSITIONS and counts[p.position] >= Constants.MAX_POSITIONS[p.position]:
                counts[Constants.FLEX] += 1
            else:
                counts[p.position] += 1
        log(f"Position counts: {dict(counts)}")
        return counts

    # Method to check if a player is already drafted in this team
    def is_player_drafted(self, player):
        log(f"FantasyTeam.is_player_drafted called for player ID: {player.id}")
        drafted = any(p.id == player.id for p in self.roster)
        log(f"Player {player.id} drafted: {drafted}")
        return drafted
    
    # Method to check if a player can be drafted as a FLEX position
    def is_draftable_flex(self, player):
        log(f"FantasyTeam.is_draftable_flex called for player ID: {player.id}")
        # Check if player can be drafted as a FLEX
        if player.position not in Constants.FLEX_ELIGIBLE_POSITIONS:
            log(f"Player {player.id} not FLEX eligible.")
            return False
        
        counts = self.get_position_counts()
        
        # Return whether the player's position is under the limit or if FLEX slot is available
        result = counts[player.position] < Constants.MAX_POSITIONS[player.position] or counts[Constants.FLEX] < Constants.MAX_POSITIONS[Constants.FLEX]
        log(f"Player {player.id} draftable as FLEX: {result}")
        return result

    # Method to check if a player can be drafted
    def can_draft(self, player):
        log(f"FantasyTeam.can_draft called for player ID: {player.id}")
        # Check total roster space
        if len(self.roster) >= Constants.MAX_PLAYERS:
            log("Roster full, cannot draft.")
            return False

        # Check if player position is valid
        pos = player.position
        if pos not in Constants.MAX_POSITIONS:
            log(f"Invalid position {pos}, cannot draft.")
            return False

        # Check if position limit is reached
        counts = self.get_position_counts()
        # Treat FLEX cases a bit differently
        if pos in Constants.FLEX_ELIGIBLE_POSITIONS and not self.is_draftable_flex(player):
            log(f"Cannot draft player {player.id} as FLEX, limits reached.")
            return False
        
        # Check if position limit is reached for non-FLEX positions
        if pos not in Constants.FLEX_ELIGIBLE_POSITIONS and counts[pos] >= Constants.MAX_POSITIONS[pos]:
            log(f"Cannot draft player {player.id}, position {pos} limit reached.")
            return False

        # Check if player is already drafted
        if self.is_player_drafted(player):
            log(f"Player {player.id} already drafted.")
            return False
        
        # Check player's bye week
        if player.bye_week not in Constants.POSSIBLE_BYE_WEEKS:
            log(f"Player {player.id} has an invalid bye week: {player.bye_week}.")
            return False

        log(f"Player {player.id} can be drafted.")
        return True

    # Method to draft a player onto the team
    def draft_player(self, player):
        log(f"FantasyTeam.draft_player called for player ID: {player.id}")
        can_draft = self.can_draft(player)
        if can_draft:
            self.roster.append(player)
            log(f"Player {player.id} drafted successfully. Roster size now {len(self.roster)}.")
            return True
        else:
            log(f"Player {player.id} could not be drafted.")
            return False
        

    # print the ideal draft order, and what the actual draft order is
    def print_draft_order(self):
        log("FantasyTeam.print_draft_order called")
        for i, pos in enumerate(Constants.DRAFT_ORDER):
            print(f"Round {i + 1}: {', '.join(pos.keys())} -- Drafted: {self.draft_order[i].name if self.draft_order[i] else 'None'} ({self.draft_order[i].position if self.draft_order[i] else 'None'})")
