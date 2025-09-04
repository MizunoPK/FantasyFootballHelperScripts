from draft_helper import DraftHelper
import os

BASE_DATA_FOLDER = './data/draft_simulation/'
PLAYERS_CSV = BASE_DATA_FOLDER + 'players.csv'
SIMULATION_PLAYERS = 8

# Copy ./data/players.csv to the simulation folder and overwrite if exists
if not os.path.exists(BASE_DATA_FOLDER):
    os.makedirs(BASE_DATA_FOLDER)
if os.path.exists(PLAYERS_CSV):
    os.remove(PLAYERS_CSV)  # Remove existing file if it exists
import shutil
shutil.copy('./data/players.csv', PLAYERS_CSV)

# Clear the last simulation team files if exists
for i in range(SIMULATION_PLAYERS):
    team_csv = BASE_DATA_FOLDER + f'team_{i+1}.csv'
    if os.path.exists(team_csv):
        os.remove(team_csv)
        print(f"Removed existing file: {team_csv}")

# Run simulations for multiple teams, each with its own team CSV
# Do 15 rounds of drafting
for round in range(15):
    print(f"\n=== Simulation Round {round + 1} ===")
    for i in range(SIMULATION_PLAYERS):
        team_csv = BASE_DATA_FOLDER + f'team_{i+1}.csv'
        print(f"\n--- Running simulation for team file: {team_csv} ---")
        simulator = DraftHelper(players_csv=PLAYERS_CSV, team_csv=team_csv)
        simulator.run_draft(simulation=True)