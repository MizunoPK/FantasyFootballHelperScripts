import csv
import requests
from datetime import datetime
import pandas as pd

ADP_SOURCE = './data/adp.csv'
BYE_WEEK_SOURCE = './data/bye_weeks.csv'

# File to save data
CSV_FILE = "./data/players.csv"

# CSV Headers for our draft helper
HEADERS = [
    "name", "position", "team", "adp", "bye_week", "injury_status", "id"
]

# Sleeper API Endpoints
BASE_URL = "https://api.sleeper.app/v1"
CURRENT_YEAR = datetime.now().year

def get_players():
    """Fetch all NFL players from Sleeper."""
    url = f"{BASE_URL}/players/nfl"
    print(f"📡 Fetching player list from Sleeper...")
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_bye_week_data():
    bye_week_data = {}
    
    with open(BYE_WEEK_SOURCE, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            try:
                bye_week_data[row["Team"]] = row["ByeWeek"]
            except ValueError:
                continue  # Skip rows with invalid numeric values
    
    return bye_week_data

def get_adp():
    player_adp = {}
    
    with open(ADP_SOURCE, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Identify which columns contain ADP numbers
        adp_columns = [col for col in reader.fieldnames if "ADP" in col.upper()]
        
        for row in reader:
            try:
                adp_values = [
                    float(row[col]) 
                    for col in adp_columns 
                    if row[col] not in (None, "", "NA")
                ]
                
                if adp_values:
                    avg_adp = sum(adp_values) / len(adp_values)
                    player_adp[row["Player Id"]] = avg_adp
            except ValueError:
                continue  # Skip rows with invalid numeric values
    
    return player_adp

def create_csv(players_data, adp_data, bye_week_data):
    """Merge Sleeper data into a CSV."""
    print(f"🛠 Processing and creating CSV: {CSV_FILE}")

    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)

        for pid, pdata in players_data.items():
            if pid not in adp_data:
                continue  # Skip irrelevant positions

            team = pdata.get("team", "")

            writer.writerow([
                pdata.get("full_name", pdata.get("last_name", "Unknown")),
                pdata.get("position", ""),
                team,
                adp_data.get(pid, ""),
                bye_week_data.get(team, 0) or 0,
                pdata.get("injury_status", "Healthy") or "Healthy",
                pid
            ])

    print(f"✅ Created {CSV_FILE} with {sum(1 for _ in open(CSV_FILE)) - 1} players.")

if __name__ == "__main__":
    players = get_players()
    adp = get_adp()
    bye_week_data = get_bye_week_data()
    create_csv(players, adp, bye_week_data)
