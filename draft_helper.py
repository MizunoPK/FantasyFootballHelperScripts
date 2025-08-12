import csv
from collections import Counter, defaultdict

from Player import load_players_from_csv
from FantasyTeam import FantasyTeam
import Constants

# Standard library imports
import csv
from collections import Counter, defaultdict

# Local module imports
from Player import load_players_from_csv  # Function to load players from a CSV file
from FantasyTeam import FantasyTeam       # FantasyTeam class for managing team state
import Constants                         # Centralized constants for configuration

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
    - ADP (Average Draft Position)
    - Bye week conflicts with current starters and bench
    - Injury status
    - Starting lineup requirements
    - Bench depth needs
    - Returns a score that can be used to rank players for drafting.
    """
    def score_player(self, p, starters_needed, open_bench_spots, starters_list):
            pos = p.position
            # Calculate ADP score: lower ADP means higher value, so we invert it
            adp_score = Constants.ADP_BASE_SCORE - (p.weighted_adp if p.weighted_adp else Constants.ADP_BASE_SCORE)

            # Calculate bye week penalty based on overlap with current starters/bench
            # This discourages drafting too many players with the same bye week
            starters_bye_counts_by_pos = defaultdict(Counter)
            for p in starters_list:
                if p.bye_week:
                    starters_bye_counts_by_pos[p.bye_week][p.position] += 1
            bench_players = [p for p in self.team.roster if p not in starters_list]
            bench_bye_counts_by_pos = defaultdict(Counter)
            for p in bench_players:
                if p.bye_week:
                    bench_bye_counts_by_pos[p.bye_week][p.position] += 1
            bye_penalty = self.compute_bye_penalty_for_player(p, starters_bye_counts_by_pos, bench_bye_counts_by_pos)

            # Apply a penalty if the player is not healthy
            # This deprioritizes injured players in recommendations
            injury_penalty = 0
            if p.injury_status != Constants.HEALTHY:
                injury_penalty = Constants.PENALTY_INJURED

            # Calculate positional need: prioritize positions where starters are still needed
            pos_need = 0
            if pos in [Constants.RB, Constants.WR]:
                # For RB/WR, also consider FLEX needs
                pos_need = starters_needed[pos] + (starters_needed[Constants.FLEX] if starters_needed[Constants.FLEX] > 0 else 0)
            else:
                pos_need = starters_needed.get(pos, 0)

            # If we've already filled the max allowed for this position, don't recommend more
            counts = self.team.get_position_counts()
            if counts.get(pos, 0) >= Constants.MAX_POSITIONS[pos]:
                pos_need = 0

            # Assign a weight based on whether the player fills a starter or bench spot
            if pos_need > 0:
                # Strongly prioritize filling starting lineup
                need_weight = Constants.STARTER_POS_NEEDED_SCORE * pos_need
            elif open_bench_spots > 0:
                # Lower weight for bench depth
                need_weight = Constants.BENCH_POS_NEEDED_SCORE * pos_need
            else:
                need_weight = 0

            # Final score combines all factors
            total_score = need_weight + adp_score - bye_penalty - injury_penalty
            return total_score
    
    
    def compute_bye_penalty_for_player(self, p, starters_bye_counts_by_pos, bench_bye_counts_by_pos):
        """
        p: candidate Player
        starters_bye_counts_by_pos: dict mapping (bye_week -> Counter of positions among starters)
        bench_bye_counts_by_pos: dict mapping (bye_week -> Counter of positions among bench players)
        Returns total bye penalty (positive number to subtract from score).
        """
        # If player has no bye week, no penalty is applied
        if not p.bye_week:
            return 0

        bw = p.bye_week
        penalty = 0

        # Add penalty for bye week conflicts with current starters
        # The penalty is higher if the candidate's position matches a starter's position
        starters_counts = starters_bye_counts_by_pos.get(bw, {})
        for pos, count in starters_counts.items():
            pos_weight = Constants.STARTER_BYE_WEIGHTS.get(pos, 10)

            if pos in [Constants.RB, Constants.WR] and count >= Constants.STARTERS_REQ[pos]:
                pos_weight = Constants.STARTER_BYE_WEIGHTS.get(Constants.FLEX, 10)
            # if pos == p.position:
            #     pos_weight = Constants.STARTER_BYE_WEIGHTS[Constants.MATCH]
            penalty += pos_weight * count

        # Add a smaller penalty for bench conflicts (less important than starters)
        bench_counts = bench_bye_counts_by_pos.get(bw, {})
        for pos, count in bench_counts.items():
            pos_weight = Constants.STARTER_BYE_WEIGHTS.get(pos, 10)
            # if pos == p.position:
            #     pos_weight = Constants.STARTER_BYE_WEIGHTS[Constants.MATCH]
            penalty += (pos_weight * Constants.BENCH_WEIGHT_FACTOR) * count

        return penalty


    def recommend_next_picks(self):
        """
        Recommend top players to draft next based on:
        - Team position needs vs roster max and starters requirements
        - Player ADP (lower better)
        - Injury status (only healthy)
        - Avoid players already drafted
        - Avoid bye week stacking (warn or deprioritize)
        """

        # Count how many players are currently drafted at each position
        counts = self.team.get_position_counts()
        total_drafted = len(self.team.roster)

        # Calculate how many starters are still needed at each position
        # This helps prioritize which positions to recommend next
        starters_needed = {
            Constants.QB: max(Constants.STARTERS_REQ[Constants.QB] - counts.get(Constants.QB, 0), 0),
            Constants.RB: max(Constants.STARTERS_REQ[Constants.RB] - counts.get(Constants.RB, 0), 0),
            Constants.WR: max(Constants.STARTERS_REQ[Constants.WR] - counts.get(Constants.WR, 0), 0),
            Constants.TE: max(Constants.STARTERS_REQ[Constants.TE] - counts.get(Constants.TE, 0), 0),
            Constants.K: max(Constants.STARTERS_REQ[Constants.K] - counts.get(Constants.K, 0), 0),
            Constants.DEF: max(Constants.STARTERS_REQ[Constants.DEF] - counts.get(Constants.DEF, 0), 0)
        }

        # Calculate how many FLEX starters are needed (FLEX can be RB or WR)
        # FLEX is filled after RB/WR starters are filled, so we subtract those from the total
        rb_wr_total = counts.get(Constants.RB, 0) + counts.get(Constants.WR, 0)
        flex_needed = max(Constants.STARTERS_REQ[Constants.FLEX] - max(rb_wr_total - (Constants.STARTERS_REQ[Constants.RB] + Constants.STARTERS_REQ[Constants.WR]), 0), 0)
        starters_needed[Constants.FLEX] = flex_needed

        # Group drafted players by position for easier starter assignment
        players_by_pos = defaultdict(list)
        for p in self.team.roster:
            players_by_pos[p.position].append(p)

        # Sort each group by ADP (lower ADP = better player)
        # This helps us pick the best available players for each position
        for pos in players_by_pos:
            players_by_pos[pos].sort(key=lambda x: x.weighted_adp if x.weighted_adp else 999)

        starters_list = []  # List of players who are considered starters

        # Assign starters for each position (except FLEX)
        # We fill each position up to the required number of starters
        for pos, needed in Constants.STARTERS_REQ.items():
            if pos == Constants.FLEX:
                continue
            count = 0
            for p in players_by_pos.get(pos, []):
                if count < needed:
                    starters_list.append(p)
                    count += 1

        # Assign FLEX starter: best available RB or WR not already a starter
        # Only one FLEX starter is allowed, and we pick the best available
        flex_candidates = []
        for p in players_by_pos.get(Constants.RB, []) + players_by_pos.get(Constants.WR, []):
            if p not in starters_list:
                flex_candidates.append(p)
        flex_candidates.sort(key=lambda x: x.weighted_adp if x.weighted_adp else 999)
        if flex_candidates and starters_needed[Constants.FLEX] > 0:
            starters_list.append(flex_candidates[0])

        # Calculate available bench spots (excluding DEF)
        # This is used to determine if we should recommend bench depth
        bench_spots = max(14 - (total_drafted - counts.get(Constants.DEF, 0)), 0)

        # Sort available players by score descending
        available_players = [
            p for p in self.players
            if not self.team.is_player_drafted(p)
            and p.bye_week in Constants.POSSIBLE_BYE_WEEKS
            and p.position in Constants.MAX_POSITIONS
        ]

        # Score each player based on team needs and bye week conflicts
        for p in available_players:
            p.score = self.score_player(p, starters_needed, bench_spots, starters_list)

        # Sort available players by score descending
        ranked_players = sorted(available_players, key=lambda x: x.score, reverse=True)

        # Return top 5 recommended players
        return ranked_players[:5]


    def save_team(self):
        # Save drafted team to CSV
        with open(self.team_csv, 'w', newline='') as csvfile:
            fieldnames = ['name', 'position', 'team', 'adp', 'bye_week', 'injury_status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in self.team.roster:
                writer.writerow({
                    'name': p.name,
                    'position': p.position,
                    'team': p.team,
                    'adp': p.original_adp,
                    'bye_week': p.bye_week,
                    'injury_status': p.injury_status
                })

    def save_players(self):
        # Save drafted team to CSV
        with open(self.players_csv, 'w', newline='') as csvfile:
            fieldnames = ['name', 'position', 'team', 'adp', 'bye_week', 'injury_status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in self.players:
                writer.writerow({
                    'name': p.name,
                    'position': p.position,
                    'team': p.team,
                    'adp': p.original_adp,
                    'bye_week': p.bye_week,
                    'injury_status': p.injury_status
                })

    def run_draft(self, simulation=False):
        print("Welcome to the Start 7 Fantasy League Draft Helper!")
        print(f"Currently drafted players: {len(self.team.roster)} / {Constants.MAX_PLAYERS} max")
        print("Your current roster by position:")
        for pos, count in self.team.get_position_counts().items():
            print(f"  {pos}: {count}")

        looping = 0
        while looping  == 0:
            looping += 1
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
                break
            if not choice.isdigit():
                print("Invalid input. Please enter a number or 'quit'.")
                continue

            index = int(choice) - 1
            if index < 0 or index >= len(recommendations):
                print("Number out of range.")
                continue

            # Draft the selected player and update the team
            player_to_draft = recommendations[index]
            success, msg = self.team.draft_player(player_to_draft)
            print(msg)
            if not success:
                continue

            # Save updated team to team.csv after each draft
            self.save_team()

            # If running in simulation mode, delete the drafted player from available players
            if simulation:
                self.players = [p for p in self.players if p.name != player_to_draft.name]
                self.save_players()

        # Print final roster after drafting is complete or user exits
        print("\nDrafting complete or exited. Final team roster:")
        for p in self.team.roster:
            print(f" - {p}")
        print(f"Total players drafted: {len(self.team.roster)} / {Constants.MAX_PLAYERS}")
        print(f"Average ADP of drafted players: {sum(p.original_adp for p in self.team.roster) / len(self.team.roster) if self.team.roster else 0:.2f}")

if __name__ == "__main__":
    DraftHelper(Constants.PLAYERS_CSV, Constants.TEAM_CSV).run_draft()
