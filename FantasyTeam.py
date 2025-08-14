from collections import Counter
import Constants

# FantasyTeam class to manage a fantasy football team
# It holds drafted players, manages roster limits, and draft order
# It also provides methods to draft players and check roster status
class FantasyTeam:
    def __init__(self, players=None):
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
                self.starter_counts[pos] += 1


        # Determine the draft order - holds the Player instances in the order they were drafted
        self.draft_order = [None] * Constants.MAX_PLAYERS
        for player in self.roster:
            pos = player.get_position_including_flex()
            for i in range(Constants.MAX_PLAYERS):
                if self.draft_order[i] is None and pos == Constants.get_ideal_draft_position(i):
                    self.draft_order[i] = player
                    break

    # Method to get the next draft position weights based on the current roster
    def get_next_draft_position_weights(self):
        # Find the next open draft position
        for i in range(Constants.MAX_PLAYERS):
            if self.draft_order[i] is None:
                return Constants.DRAFT_ORDER[i]
        return None

    # Method to get a count of players drafted by position
    def get_position_counts(self):
        # Count how many players drafted per position
        counts = Counter()
        for p in self.roster:
            if p.position in Constants.FLEX_ELIGIBLE_POSITIONS and counts[p.position] >= Constants.MAX_POSITIONS[p.position]:
                counts[Constants.FLEX] += 1
            else:
                counts[p.position] += 1
        return counts

    # Method to check if a player is already drafted in this team
    def is_player_drafted(self, player):
        # Check if player already drafted in this team
        return any(p.name == player.name for p in self.roster)
    
    # Method to check if a player can be drafted as a FLEX position
    def is_draftable_flex(self, player):
        # Check if player can be drafted as a FLEX
        if player.position not in Constants.FLEX_ELIGIBLE_POSITIONS:
            return False
        
        counts = self.get_position_counts()
        # TODO: Refine this logic
        # If both RB and WR limits have not been reached, it's draftable
        # If either RB or WR limit is reached, it's draftable as long as the other position has space
        # If both RB and WR limits are reached, it's draftable only if FLEX limit is not reached
        # In any other case, it's not draftable
        



        # Check if we've exceeded the FLEX limit
        # total_flex = 0
        # max_flex = Constants.MAX_POSITIONS[Constants.FLEX]
        # for possible_flex in Constants.FLEX_ELIGIBLE_POSITIONS:
        #     total_flex += counts.get(possible_flex, 0)
        #     max_flex += Constants.MAX_POSITIONS[possible_flex]
        # if total_flex >= max_flex:
        #     return False
        
        return True

    # Method to check if a player can be drafted
    def can_draft(self, player):
        # Check total roster space
        if len(self.roster) >= Constants.MAX_PLAYERS:
            return False

        # Check if player position is valid
        pos = player.position
        if pos not in Constants.MAX_POSITIONS:
            return False

        # Check if position limit is reached
        counts = self.get_position_counts()
        # Treat FLEX cases a bit differently
        if pos in Constants.FLEX_ELIGIBLE_POSITIONS and not self.is_draftable_flex(player):
            return False
        
        # Check if position limit is reached for non-FLEX positions
        if pos not in Constants.FLEX_ELIGIBLE_POSITIONS and counts[pos] >= Constants.MAX_POSITIONS[pos]:
            return False

        # Check if player is already drafted
        if self.is_player_drafted(player):
            return False

        return True

    # Method to draft a player onto the team
    def draft_player(self, player):
        # Attempt to draft a player; returns success bool and message
        can_draft = self.can_draft(player)
        if can_draft:
            self.roster.append(player)
            return True
        else:
            return False
