import csv
import Constants

class Player:
    def __init__(self, name, position, team, adp, bye_week, injury_status):
        self.name = name
        self.position = position.upper()
        self.team = team
        self.adp = float(adp) if adp else None
        self.bye_week = int(bye_week) if bye_week else None
        self.injury_status = injury_status.lower()

    def __repr__(self):
        return f"{self.name} ({self.position} - {self.team}) ADP: {self.adp} Bye: {self.bye_week} Injury: {self.injury_status}"


def load_players_from_csv(filename):
    players = []
    max_adp = 0.0
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player = Player(
                name=row['name'],
                position=row['position'],
                team=row['team'],
                adp=float(row['adp']),
                bye_week=row['bye_week'],
                injury_status=row['injury_status']
            )
            players.append(player)
            if player.adp and player.adp > max_adp:
                max_adp = player.adp

    # Change ADP values to be between 0 and 100
    for player in players:
        if player.adp:
            player.adp = (player.adp / max_adp) * Constants.ADP_BASE_SCORE if max_adp > 0 else 0
        else:
            player.adp = 0

    print(f"Loaded {len(players)} players from {filename}.")

    return players