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


def recommend_next_picks(players, team):
    """
    Recommend top players to draft next based on:
    - Team position needs vs roster max and starters requirements
    - Player ADP (lower better)
    - Injury status (only healthy)
    - Avoid players already drafted
    - Avoid bye week stacking (warn or deprioritize)
    """

    # Count how many players are currently drafted at each position
    counts = team.get_position_counts()
    total_drafted = len(team.roster)

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
    for p in team.roster:
        players_by_pos[p.position].append(p)

    # Sort each group by ADP (lower ADP = better player)
    # This helps us pick the best available players for each position
    for pos in players_by_pos:
        players_by_pos[pos].sort(key=lambda x: x.adp if x.adp else 999)

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
    flex_candidates.sort(key=lambda x: x.adp if x.adp else 999)
    if flex_candidates and starters_needed[Constants.FLEX] > 0:
        starters_list.append(flex_candidates[0])

    # Calculate available bench spots (excluding DEF)
    # This is used to determine if we should recommend bench depth
    bench_spots = max(14 - (total_drafted - counts.get(Constants.DEF, 0)), 0)

    def compute_bye_penalty_for_player(p, starters_bye_counts_by_pos, bench_bye_counts_by_pos):
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
            if pos == p.position:
                pos_weight = Constants.STARTER_BYE_WEIGHTS[Constants.MATCH]
            penalty += pos_weight * count

        # Add a smaller penalty for bench conflicts (less important than starters)
        bench_counts = bench_bye_counts_by_pos.get(bw, {})
        for pos, count in bench_counts.items():
            pos_weight = Constants.STARTER_BYE_WEIGHTS.get(pos, 10)
            if pos == p.position:
                pos_weight = Constants.STARTER_BYE_WEIGHTS[Constants.MATCH]
            penalty += (pos_weight * Constants.BENCH_WEIGHT_FACTOR) * count

        return penalty

    def score_player(p):
        pos = p.position
        # Calculate ADP score: lower ADP means higher value, so we invert it
        adp_score = Constants.ADP_BASE_SCORE - (p.adp if p.adp else Constants.ADP_BASE_SCORE)

        # Calculate bye week penalty based on overlap with current starters/bench
        # This discourages drafting too many players with the same bye week
        starters_bye_counts_by_pos = defaultdict(Counter)
        for p in starters_list:
            if p.bye_week:
                starters_bye_counts_by_pos[p.bye_week][p.position] += 1
        bench_players = [p for p in team.roster if p not in starters_list]
        bench_bye_counts_by_pos = defaultdict(Counter)
        for p in bench_players:
            if p.bye_week:
                bench_bye_counts_by_pos[p.bye_week][p.position] += 1
        bye_penalty = compute_bye_penalty_for_player(p, starters_bye_counts_by_pos, bench_bye_counts_by_pos)

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
        counts = team.get_position_counts()
        if counts.get(pos, 0) >= Constants.MAX_POSITIONS[pos]:
            pos_need = 0

        # Assign a weight based on whether the player fills a starter or bench spot
        if pos_need > 0:
            # Strongly prioritize filling starting lineup
            need_weight = Constants.STARTER_POS_NEEDED_SCORE * pos_need
        elif bench_spots > 0:
            # Lower weight for bench depth
            need_weight = Constants.BENCH_POS_NEEDED_SCORE * pos_need
        else:
            need_weight = 0

        # Final score combines all factors
        total_score = need_weight + adp_score - bye_penalty - injury_penalty
        return total_score

    # Sort available players by score descending
    available_players = [
        p for p in players
        if not team.is_player_drafted(p)
        and p.bye_week in Constants.POSSIBLE_BYE_WEEKS
        and p.position in Constants.MAX_POSITIONS
    ]

    ranked_players = sorted(available_players, key=score_player, reverse=True)
    return ranked_players[:5]


def save_team(filename, team):
    # Save drafted team to CSV
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'position', 'team', 'adp', 'bye_week', 'injury_status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in team.roster:
            writer.writerow({
                'name': p.name,
                'position': p.position,
                'team': p.team,
                'adp': p.adp,
                'bye_week': p.bye_week,
                'injury_status': p.injury_status
            })

def main():
    # Load players from players.csv
    players = load_players_from_csv(Constants.PLAYERS_CSV)
    # Load current drafted team from team.csv, or start empty
    drafted_players = load_players_from_csv(Constants.TEAM_CSV)
    team = FantasyTeam(drafted_players)

    print("Welcome to the Start 7 Fantasy League Draft Helper!")
    print(f"Currently drafted players: {len(team.roster)} / {Constants.MAX_PLAYERS} max")
    print("Your current roster by position:")
    for pos, count in team.get_position_counts().items():
        print(f"  {pos}: {count}")

    looping = 0
    while looping  == 0:
        looping += 1
        print("\nTop draft recommendations based on your current roster:")
        # Get the top 5 recommended players based on current team needs
        recommendations = recommend_next_picks(players, team)
        for i, p in enumerate(recommendations, start=1):
            print(f"{i}. {p}")

        # Prompt user to draft a player or quit
        choice = input("\nEnter the number of the player to draft, or 'quit' to exit: ").strip()
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
        success, msg = team.draft_player(player_to_draft)
        print(msg)
        if not success:
            continue

        # Save updated team to team.csv after each draft
        save_team('./data/team.csv', team)

    # Print final roster after drafting is complete or user exits
    print("\nDrafting complete or exited. Final team roster:")
    for p in team.roster:
        print(f" - {p}")

if __name__ == "__main__":
    main()
