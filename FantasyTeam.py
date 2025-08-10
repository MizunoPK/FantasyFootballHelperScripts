from collections import Counter
import Constants

class FantasyTeam:
    def __init__(self, players=None):
        # Roster holds Player instances drafted so far
        self.roster = players if players else []

    def get_position_counts(self):
        # Count how many players drafted per position
        counts = Counter()
        for p in self.roster:
            counts[p.position] += 1
        return counts

    def is_player_drafted(self, player):
        # Check if player already drafted in this team
        return any(p.name == player.name for p in self.roster)

    def can_draft(self, player):
        # Check total roster space
        if len(self.roster) >= Constants.MAX_PLAYERS:
            return False, "Roster full."

        pos = player.position
        if pos not in Constants.MAX_POSITIONS:
            return False, f"Position {pos} not recognized."

        counts = self.get_position_counts()
        if counts[pos] >= Constants.MAX_POSITIONS[pos]:
            return False, f"Max players for position {pos} reached."

        if self.is_player_drafted(player):
            return False, f"{player.name} is already drafted."

        return True, ""

    def draft_player(self, player):
        # Attempt to draft a player; returns success bool and message
        can_draft, msg = self.can_draft(player)
        if can_draft:
            self.roster.append(player)
            return True, f"Drafted {player.name} ({player.position})"
        else:
            return False, msg
