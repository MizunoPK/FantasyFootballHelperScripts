"""
Manual Simulation Script

Single league simulation for testing and validation of core components.
Runs a complete draft and 17-week season with one DraftHelperTeam and
9 SimulatedOpponents.

Usage:
    python simulation/manual_simulation.py

Output:
    - Draft results (which team got which players)
    - Weekly matchup results (scores and winners)
    - Final standings (wins/losses/points for all teams)

Author: Kai Mizuno
"""

import sys
import json
from pathlib import Path

# Add simulation to path
sys.path.append(str(Path(__file__).parent))
from SimulatedLeague import SimulatedLeague

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


def load_config(config_path: Path) -> dict:
    """
    Load configuration from JSON file.

    Args:
        config_path (Path): Path to config JSON file

    Returns:
        dict: Configuration dictionary (full config with config_name, description, parameters)
    """
    with open(config_path, 'r') as f:
        config_data = json.load(f)

    # Return full config (ConfigManager expects config_name, description, parameters)
    return config_data


def print_draft_results(league: SimulatedLeague) -> None:
    """
    Print draft results showing which team drafted which players.

    Args:
        league (SimulatedLeague): Completed league simulation
    """
    print("\n" + "="*80)
    print("DRAFT RESULTS (15 rounds, 150 picks)")
    print("="*80)

    for idx, team in enumerate(league.teams):
        team_type = "DraftHelperTeam" if team == league.draft_helper_team else f"SimulatedOpponent"

        if team != league.draft_helper_team:
            strategy = team.strategy
            print(f"\n{team_type} (Team {idx}, Strategy: {strategy}):")
        else:
            print(f"\n{team_type} (Team {idx}):")

        roster = team.get_roster_players()

        # Group by position
        by_position = {}
        for player in roster:
            pos = player.position
            if pos not in by_position:
                by_position[pos] = []
            by_position[pos].append(player)

        # Print by position
        for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
            if pos in by_position:
                print(f"  {pos}:")
                for player in by_position[pos]:
                    adp = f"ADP: {player.average_draft_position:.1f}" if player.average_draft_position else "ADP: N/A"
                    pts = f"Proj: {player.fantasy_points:.1f}" if player.fantasy_points else "Proj: N/A"
                    print(f"    - {player.name} ({adp}, {pts})")


def print_weekly_results(league: SimulatedLeague) -> None:
    """
    Print weekly matchup results.

    Args:
        league (SimulatedLeague): Completed league simulation
    """
    print("\n" + "="*80)
    print("SEASON RESULTS (17 weeks)")
    print("="*80)

    for week in league.week_results:
        print(f"\nWeek {week.week_number}:")
        print("-" * 60)

        results = week.get_all_results()
        matchups = week.get_matchups()

        for team1, team2 in matchups:
            result1 = results[team1]
            result2 = results[team2]

            # Determine team names
            team1_name = "DraftHelperTeam" if team1 == league.draft_helper_team else "SimulatedOpponent"
            team2_name = "DraftHelperTeam" if team2 == league.draft_helper_team else "SimulatedOpponent"

            # Add strategy info for opponents
            if team1 != league.draft_helper_team:
                team1_name += f" ({team1.strategy})"
            if team2 != league.draft_helper_team:
                team2_name += f" ({team2.strategy})"

            # Format scores with winner indicator
            if result1.won:
                print(f"  {team1_name:50s} {result1.points_scored:6.2f}  WIN")
                print(f"  {team2_name:50s} {result2.points_scored:6.2f}  LOSS")
            elif result2.won:
                print(f"  {team1_name:50s} {result1.points_scored:6.2f}  LOSS")
                print(f"  {team2_name:50s} {result2.points_scored:6.2f}  WIN")
            else:
                # Tie
                print(f"  {team1_name:50s} {result1.points_scored:6.2f}  TIE")
                print(f"  {team2_name:50s} {result2.points_scored:6.2f}  TIE")

            print()


def print_final_standings(league: SimulatedLeague) -> None:
    """
    Print final standings for all teams.

    Args:
        league (SimulatedLeague): Completed league simulation
    """
    print("\n" + "="*80)
    print("FINAL STANDINGS")
    print("="*80)

    all_results = league.get_all_team_results()

    # Sort by wins (descending), then by total points (descending)
    sorted_teams = sorted(
        all_results.items(),
        key=lambda x: (x[1][0], x[1][2]),  # (wins, total_points)
        reverse=True
    )

    print(f"\n{'Team':<50s} {'Record':^12s} {'Points':>10s}")
    print("-" * 72)

    for team_name, (wins, losses, total_points) in sorted_teams:
        record = f"{wins}W - {losses}L"
        print(f"{team_name:<50s} {record:^12s} {total_points:>10.2f}")

    # Highlight DraftHelperTeam result
    print("\n" + "="*80)
    draft_helper_result = None
    for team_name, result in all_results.items():
        if "DraftHelper" in team_name:
            draft_helper_result = result
            break

    if draft_helper_result:
        wins, losses, total_points = draft_helper_result
        print(f"DraftHelperTeam Performance: {wins}W-{losses}L, {total_points:.2f} total points")
        print("="*80)


def main() -> None:
    """Run single manual simulation for testing/validation."""
    logger = get_logger()
    logger.info("Starting manual simulation")

    # Load baseline config
    config_path = Path("simulation/optimal_configs/optimal_2025-10-02_15-29-14.json.json")
    data_folder = Path("simulation/sim_data")

    print("\n" + "="*80)
    print("FANTASY FOOTBALL LEAGUE SIMULATION")
    print("="*80)
    print(f"\nConfig: {config_path.name}")
    print(f"Data folder: {data_folder}")
    print(f"\nLeague structure:")
    print("  - 10 teams total")
    print("  - 1 DraftHelperTeam (system being tested)")
    print("  - 9 SimulatedOpponents (various strategies)")
    print(f"\nSimulation process:")
    print("  - Snake draft (15 rounds, 150 total picks)")
    print("  - 16-week regular season")
    print("  - Round-robin schedule (each team plays each other ~2x)")

    # Load config
    config_dict = load_config(config_path)
    logger.info(f"Loaded config from {config_path}")

    # Create league
    print(f"\n{'='*80}")
    print("INITIALIZING LEAGUE")
    print("="*80)
    league = SimulatedLeague(config_dict, data_folder)
    logger.info("SimulatedLeague created")

    # Run draft
    print(f"\n{'='*80}")
    print("RUNNING DRAFT")
    print("="*80)
    print("Running 15-round snake draft...")
    league.run_draft()
    logger.info("Draft complete")

    # Print draft results
    print_draft_results(league)

    # Run season
    print(f"\n{'='*80}")
    print("RUNNING SEASON")
    print("="*80)
    print("Simulating 17-week season...")
    league.run_season()
    logger.info("Season complete")

    # Print weekly results
    print_weekly_results(league)

    # Print final standings
    print_final_standings(league)

    # Cleanup
    league.cleanup()
    logger.info("Manual simulation complete")

    print("\n" + "="*80)
    print("SIMULATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
