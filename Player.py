import csv
import Constants

# FantasyTeam class to manage a fantasy football team
# It holds drafted players, manages roster limits, and draft order
# It also provides methods to draft players and check roster status
class Player:
    def __init__(self, name, position, team, original_adp, bye_week, injury_status):
        self.name = name
        self.position = position.upper()
        self.team = team
        self.original_adp = float(original_adp) if original_adp else None
        self.weighted_adp = 0.0
        self.bye_week = int(bye_week) if bye_week else None
        self.injury_status = injury_status.lower()
        self.score = 0  # Initialize score for ranking
        self.is_starter = False  # To be set when added to a FantasyTeam

    def __repr__(self):
        return f"{self.name} ({self.position} - {self.team}) ADP: {self.original_adp} Bye: {self.bye_week} Injury: {self.injury_status} [Score: {self.score}]"
    
    # Method to get the position including FLEX eligibility
    def get_position_including_flex(self):
        return Constants.FLEX if self.position in Constants.FLEX_ELIGIBLE_POSITIONS else self.position

# Method to load players from a CSV file
# Returns a list of Player instances with their ADP normalized to a base score
def load_players_from_csv(filename):
    players = []
    max_adp = 0.0
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                player = Player(
                    name=row['name'],
                    position=row['position'],
                    team=row['team'],
                    original_adp=float(row['adp']),
                    bye_week=row['bye_week'],
                    injury_status=row['injury_status']
                )
                players.append(player)
                if player.original_adp and player.original_adp > max_adp:
                    max_adp = player.original_adp
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

    # Change ADP values to be between 0 and 100
    for player in players:
        if player.original_adp:
            player.weighted_adp = (player.original_adp / max_adp) * Constants.ADP_BASE_SCORE if max_adp > 0 else 0
        else:
            player.weighted_adp = 0

    print(f"Loaded {len(players)} players from {filename}.")

    return players