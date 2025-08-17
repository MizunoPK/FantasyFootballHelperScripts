import csv
from collections import Counter, defaultdict

from Player import load_players_from_csv
from FantasyTeam import FantasyTeam
import Constants                # Centralized constants for configuration
from logger import log

class DraftHelper:
    """
    DraftHelper class to manage the drafting process, including player recommendations
    based on team needs, player ADP, and bye week considerations.
    """

    def __init__(self, players_csv=Constants.PLAYERS_CSV, team_csv=Constants.TEAM_CSV):
        """
        Initialize the DraftHelper with players and team data.
        Loads players from the specified CSV files.
        """
        self.players_csv = players_csv
        self.team_csv = team_csv
        self.players = load_players_from_csv(players_csv)
        self.team = FantasyTeam(load_players_from_csv(team_csv))
        print(f"DraftHelper initialized with {len(self.players)} players and team of {len(self.team.roster)} drafted players.")

        
        
    """        
    Function to score a player based on various factors:
    - Team position needs vs roster max and starters requirements
    - ADP (Average Draft Position)
    - Bye week conflicts with current starters and bench
    - Injury status
    - Returns a score that can be used to rank players for drafting.
    """
    def score_player(self, p):
        log(f"Scoring player {p.name} (ID: {p.id}, Position: {p.position}, ADP: {p.weighted_adp}, Bye: {p.bye_week}, Injury: {p.injury_status})")
        # Calculate Position score based on where we are in the draft, and what positions are needed
        pos_score = self.compute_positional_need_score(p)
        log(f"Positional need score for {p.name}: {pos_score}")

        # Calculate ADP score: lower ADP means higher value, so we invert it
        adp_score = self.compute_adp_score(p)
        log(f"ADP score for {p.name}: {adp_score}")

        # Calculate bye week penalty based on overlap with current starters/bench
        # This discourages drafting too many players with the same bye week
        bye_penalty = self.compute_bye_penalty_for_player(p)
        log(f"Bye week penalty for {p.name}: {bye_penalty}")

        # Apply a penalty if the player is not healthy
        # This deprioritizes injured players in recommendations
        injury_penalty = self.compute_injury_penalty(p)
        log(f"Injury penalty for {p.name}: {injury_penalty}")

        # Final score combines all factors
        total_score = pos_score + adp_score - bye_penalty - injury_penalty
        log(f"Total score for {p.name}: {total_score}")
        return total_score
    
    # Function to compute the positional need score for a player
    # This considers how many players are already drafted at that position
    # And the pre-defined ideal draft order
    def compute_positional_need_score(self, p):
        log(f"compute_positional_need_score called for {p.name} (ID: {p.id})")
        score = 0
        pos = p.get_position_including_flex()
        
        # calculate score based on draft order
        draft_weights = self.team.get_next_draft_position_weights()
        multiplier = draft_weights.get(pos, 0.0)
        log(f"Computing positional need score for {p.name}: position={pos}, multiplier={multiplier}")
        score += Constants.POS_NEEDED_SCORE * multiplier

        return score

    # Function to compute the ADP score for a player
    # This is a simple inversion of the ADP value, where lower ADP means higher score
    def compute_adp_score(self, p):
        log(f"compute_adp_score called for {p.name} (ID: {p.id})")
        adp_val = p.weighted_adp if p.weighted_adp else Constants.ADP_BASE_SCORE
        log(f"Computing ADP score for {p.name}: weighted_adp={adp_val}")
        return Constants.ADP_BASE_SCORE - adp_val

    # Function to compute the bye week penalty for a player
    # This checks how many players are already drafted with the same bye week
    # and applies a penalty based on the number of conflicts
    def compute_bye_penalty_for_player(self, player):
        log(f"compute_bye_penalty_for_player called for {player.name} (ID: {player.id})")
        # If player has no bye week, no penalty is applied
        if not player.bye_week:
            return 0

        bw = player.bye_week
        
        # Get counts of starters and bench players by bye week and position
        starters_bye_counts_by_pos = defaultdict(Counter)
        bench_bye_counts_by_pos = defaultdict(Counter)
        for p in self.team.roster:
            if bw and p.is_starter:
                starters_bye_counts_by_pos[p.bye_week][p.position] += 1
            elif bw and not p.is_starter:
                bench_bye_counts_by_pos[p.bye_week][p.position] += 1

        penalty = 0

        # Add penalty for bye week conflicts with current starters
        # The penalty is higher if the candidate's position matches a starter's position
        starters_counts = starters_bye_counts_by_pos.get(bw, {})
        for pos, count in starters_counts.items():
            pos_weight = Constants.STARTER_BYE_WEIGHTS.get(pos, 10)

            # If position matches the candidate's position, use MATCH weight
            if pos == player.position:
                pos_weight = Constants.STARTER_BYE_WEIGHTS[Constants.MATCH]
            penalty += Constants.BASE_BYE_PENALTY * pos_weight * count

        # Add a smaller penalty for bench conflicts (less important than starters)
        bench_counts = bench_bye_counts_by_pos.get(bw, {})
        for pos, count in bench_counts.items():
            pos_weight = Constants.STARTER_BYE_WEIGHTS.get(pos, 10)
            if pos == player.position:
                pos_weight = Constants.STARTER_BYE_WEIGHTS[Constants.MATCH]
            penalty += Constants.BASE_BYE_PENALTY * pos_weight * Constants.BENCH_WEIGHT_FACTOR * count

        log(f"Bye penalty for {player.name}: {penalty} (bye week: {bw})")
        return penalty

    # Function to compute the injury penalty for a player
    # This checks if the player is injured and applies a penalty
    def compute_injury_penalty(self, p):
        log(f"compute_injury_penalty called for {p.name} (ID: {p.id})")
        if p.injury_status != Constants.HEALTHY:
            log(f"Injury penalty applied for {p.name}: status={p.injury_status}")
            return Constants.PENALTY_INJURED
        return 0

    # Function to recommend the next players to draft based on team needs
    # This considers:
    # - Team position needs vs roster max and starters requirements
    # - Player ADP (lower better)
    # - Injury status (only healthy)
    # - Avoid players already drafted
    # - Avoid bye week stacking (warn or deprioritize)
    # - Returns a list of recommended players sorted by score
    def recommend_next_picks(self):
        log("recommend_next_picks called")
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
        log(f"Recommended next picks: {[p.name for p in ranked_players[:Constants.RECOMMENDATION_COUNT]]}")
        return ranked_players[:Constants.RECOMMENDATION_COUNT]

    # Function to save the drafted team to a CSV file
    # This allows the user to keep track of their drafted players
    def save_team(self):
        log("save_team called")
        # Save drafted team to CSV
        with open(self.team_csv, 'w', newline='') as csvfile:
            fieldnames = ['name', 'position', 'team', 'adp', 'bye_week', 'injury_status', 'id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in self.team.roster:
                writer.writerow({
                    'name': p.name,
                    'position': p.position,
                    'team': p.team,
                    'adp': p.original_adp,
                    'bye_week': p.bye_week,
                    'injury_status': p.injury_status,
                    'id': p.id
                })
        log(f"Team saved to {self.team_csv} with {len(self.team.roster)} players.")

    # Function to save the available players to a CSV file
    # This allows the user to keep track of the available players after drafting
    def save_players(self):
        log("save_players called")
        # Save drafted team to CSV
        with open(self.players_csv, 'w', newline='') as csvfile:
            fieldnames = ['name', 'position', 'team', 'adp', 'bye_week', 'injury_status', 'id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in self.players:
                writer.writerow({
                    'name': p.name,
                    'position': p.position,
                    'team': p.team,
                    'adp': p.original_adp,
                    'bye_week': p.bye_week,
                    'injury_status': p.injury_status,
                    'id': p.id
                })
        log(f"Available players saved to {self.players_csv} with {len(self.players)} players.")

    # Function to get the user's choice of player to draft
    # This displays the top recommended players and prompts the user to select one
    def get_user_player_choice(self, simulation=False):
        log(f"get_user_player_choice called (simulation={simulation})")
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
            log("User chose to quit drafting.")
            return None
        if not choice.isdigit():
            print("Invalid input. Please enter a number or 'quit'.")
            log(f"Invalid input received: {choice}")
            return None

        index = int(choice) - 1
        if index < 0 or index >= len(recommendations):
            print("Number out of range.")
            log(f"User input out of range: {choice}")
            return None

        # Draft the selected player and update the team
        player_to_draft = recommendations[index]
        success = self.team.draft_player(player_to_draft)
        if not success:
            print(f"Failed to draft {player_to_draft.name}.")
            log(f"Failed to draft player: {player_to_draft.name}")
            return None
        log(f"Player drafted: {player_to_draft.name} (ID: {player_to_draft.id})")
        return player_to_draft


    # Main function to run the draft helper
    # This will prompt the user to draft players based on recommendations
    def run_draft(self, simulation=False):
        print("Welcome to the Start 7 Fantasy League Draft Helper!")
        print(f"Currently drafted players: {len(self.team.roster)} / {Constants.MAX_PLAYERS} max")
        print("Your current roster by position:")
        for pos, count in self.team.get_position_counts().items():
            print(f"  {pos}: {count}")
        print("\nDraft order:")
        self.team.print_draft_order()
        log(f"Draft started. Current roster size: {len(self.team.roster)}")

        # Get the user's draft choice
        player_to_draft = self.get_user_player_choice(simulation=simulation)

        # If a player was successfully drafted, save the updated team
        # and remove the drafted player from available players if in simulation mode
        if player_to_draft is not None:
            # Save updated team to team.csv after each draft
            self.save_team()

            # If running in simulation mode, delete the drafted player from available players
            if simulation:
                self.players = [p for p in self.players if p.id != player_to_draft.id]
                self.save_players()
            log(f"Draft round complete. Player {player_to_draft.name} drafted. Team and players updated.")

        # Print final roster after drafting is complete or user exits
        print("\nDrafting complete or exited. Final team roster:")
        for p in self.team.roster:
            print(f" - {p}")
        print(f"Total players drafted: {len(self.team.roster)} / {Constants.MAX_PLAYERS}")
        print(f"Average ADP of drafted players: {sum(p.original_adp for p in self.team.roster) / len(self.team.roster) if self.team.roster else 0:.2f}")
        log(f"Drafting session ended. Final team roster size: {len(self.team.roster)}")

if __name__ == "__main__":
    # clear the log file
    from logger import clear_log
    clear_log()

    DraftHelper(Constants.PLAYERS_CSV, Constants.TEAM_CSV).run_draft()
