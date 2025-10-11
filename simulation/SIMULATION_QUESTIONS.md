# Simulation Implementation Questions

## Overview
Based on the code comments in SimulationManager.py, the existing groundwork, and the real 2024 season data files, I need clarification on several aspects of the simulation system before implementing it.

---

## 1. Data Files & Player Pools (Understanding Confirmed)

### Confirmed Understanding:
✅ **Real 2024 Data Available**: All data files populated with actual NFL 2024 season data

✅ **players_projected.csv**: Contains projected fantasy points (what teams see during draft/season)
- Structure: id, name, team, position, bye_week, fantasy_points, injury_status, drafted, locked, average_draft_position, player_rating, week_1_points through week_17_points
- Example: Amon-Ra St. Brown - 219.69 projected points total, bye week 8 shows 0.0 points

✅ **players_actual.csv**: Contains actual weekly performance (ground truth for scoring)
- Same structure as projected, but with real performance data
- Significant variance from projections (e.g., Lamar Jackson: 325.92 projected vs 404.47 actual)
- Realistic week-to-week volatility

✅ **teams_week_1.csv & teams_week_17.csv**: Team rankings and matchups
- Structure: team, offensive_rank (1-32), defensive_rank (1-32), opponent
- Rankings change over season (e.g., DET offense: #3 week 1 → #1 week 17)
- Used for matchup scoring multipliers

✅ **bye_weeks.csv**: Does not exist - bye week info is in player data (bye_week column)

### Remaining Questions:

**Q1.1:** Team ranking files - only week 1 and 17 provided:
- Should I interpolate rankings for weeks 2-16?
- Or should team rankings remain static throughout the season?
- Do we need to create files for all 17 weeks?
Answer: weeks 1 through 17 have been provided now in the folder.
---

## 2. Draft Simulation

**Q2.1:** Snake draft mechanics:
- Standard snake draft order (1→10, then 10→1, repeat)?
- How should we handle the "HUMAN_ERROR_RATE" of 0.2?
  - Does this mean 20% of the time, opponents pick from top 5 instead of #1?
  - Does this apply to DraftHelperTeam or only to SimulatedOpponent teams?

Answer: Yes use standard snake draft order. Yes the human error rate means that 20% of the time they will select from their top 5 options instead of their top option. This error rate will only apply to the SimulatedOpponent teams - have the DraftHelperTeam always pick the #1 option.

**Q2.2:** Team strategies (from TEAM_STRATEGIES config):
- `'adp_aggressive'`: Pick based on lowest ADP available?
- `'projected_points_aggressive'`: Pick highest projected points?
- `'adp_with_draft_order'`: Use ADP but respect round position priorities?
- `'projected_points_with_draft_order'`: Use points but respect position priorities?
- `'draft_helper'`: This is our system being tested (1 team per league)?
  - Should there always be exactly 1 DraftHelperTeam and 9 SimulatedOpponents?
  - Or can we test with multiple DraftHelperTeam instances?
Answer: Yes all your assumptions here are correct. The draft order used should be the same one used by the AddToRosterMode and PlayerManager. Only use 1 draft helper team per league.

**Q2.3:** Draft process flow:
- Should each team draft until rosters are full (15 players each)?
- After draft completes, do we immediately start week 1 of the season?
Answer: Yes and yes

---

## 3. Season Simulation

**Q3.1:** Weekly matchups:
- How are matchups determined each week? (Random pairing? Round-robin schedule?)
- Does each team play 1 opponent per week?
- Are playoffs included (weeks 15-17 typically)?
Answer: Use a round-robin schedule. Each team faces 1 opponent per week. Yes do all 17 weeks.

**Q3.2:** Weekly scoring:
- Each team uses StarterHelperModeManager to set their optimal lineup?
- Do we compare lineup points using `players_actual` data?
- Winner is whoever has more total points from their starting lineup?
Answer: Use the StarterHelperModeManager to set up only the DraftHelperTeam's starting line up. For the SimulatedOpponents, have their starting line up be the same amount of each position that the starter helper sets up, except it just goes off of the players' weekly projected points from players_projected.csv. After determining each lineup, add up the team's actual points earned based on what is in the players_actual.csv file and compare each team's total points.

**Q3.3:** Opponent lineup decisions:
- Do SimulatedOpponent teams also use StarterHelperModeManager for weekly lineup decisions?
- Or do they use simpler strategies (e.g., always start highest projected players)?
- Should opponent strategies affect both drafting AND weekly lineup decisions?
Answer: See Q3.2 answer. Only use projected points for the week for SimulatedOpponent teams

---

## 4. Configuration Testing

**Q4.1:** Parameter generation:
- The PARAMETER_RANGES use tuples like `(range, min, max)`.
- For example: `NORMALIZATION_MAX_SCALE = (20, 60, 140)`
  - Does this mean: generate random values within ±20 of the optimal value, but never below 60 or above 140?
  - What's the "optimal value" for the first iteration? (The values in the optimal_2025-10-02 config?)
Answer: Yes, all your assumptions here are correct

**Q4.2:** Config generation strategy:
- Generate `NUMBER_OF_TEST_VALUES` (5) random configs per parameter?
- Test all combinations (5^N configs where N = number of parameters)?
- Or use a smarter approach (genetic algorithm, grid search, random search)?
Answer: Yes, we'll be generating 5 random values for each parameter and testing them along with the value set in the json file. Test all combinations for now

**Q4.3:** The `NUMBER_OF_RUNS` = 100 vs `SIMULATIONS_PER_CONFIG` = 100:
- Does `NUMBER_OF_RUNS` mean 100 different parameter configurations tested?
- Does `SIMULATIONS_PER_CONFIG` mean each configuration runs 100 full draft+season simulations?
- Total simulations = 100 configs × 100 sims = 10,000 complete league simulations?
Answer: NUMBER_OF_RUNS is the number of times we will go through the entire end to end flow. The flow starts by reading in a json file, and ends with creating a new json file based on the most optimal combination of parameter values that were found. The SIMULATIONS_PER_CONFIG is the number of simulated leagues to run for each combination of parameters. The win rate of the combination will be determined by the number of week to week wins the DraftHelperTeam earns throughout all the simulations

**Q4.4:** Which parameters should be randomly varied?
- All the multipliers and thresholds in the scoring sections?
- NORMALIZATION_MAX_SCALE, BASE_BYE_PENALTY, DRAFT_ORDER_BONUSES?
- The DRAFT_ORDER array itself (different draft strategies)?
- Injury penalties?

NORMALIZATION_MAX_SCALE, BASE_BYE_PENALTY, DRAFT_ORDER_BONUSES, and the MULTIPLIER parameters for the ADP, Player Rating, Team Quality, Consistency, and Matchup scoring. The POSITIVE_MULTIPLIER gives the range, min, and max for all the GOOD and EXCELLENT multipliers, and the NEGATIVE_MULTIPLIER gives the range, min, and max for all the POOR and VERY_POOR multipliers.

---

## 5. Performance Metrics

**Q5.1:** Win rate calculation:
- Track DraftHelperTeam's wins/losses across all 17 weeks?
- Win rate = (wins / total_games)?
- Should we also track:
  - Points scored per week?
  - Playoff performance separately?
  - Consistency of performance (variance in weekly scores)?
Just track the win rate and total points scored, and it's going to be based on all the wins the configuration combination earns across all simulations it runs.

**Q5.2:** Optimal config determination:
- Highest win rate = best config?
- Any tiebreakers if multiple configs have same win rate?
- Should we weight playoff weeks differently than regular season?
Yes. Use total points scored as the tie breaker if that happens. No don't weigh playoff weeks differently.

**Q5.3:** Output format:
- Save top N configs or just the absolute best?
- Include statistics like average win rate, confidence intervals?
- Track historical progression (configs tested over time)?
Just save the absolute best. Just show the win rate of the winner and average points earned per league it performed in. No historical progression needed.

---

## 6. Implementation Details

**Q6.1:** PlayerManager instances:
- `DraftHelperTeam` gets 2 PlayerManager instances (projected + actual).
- `SimulatedOpponent` also gets 2 PlayerManager instances.
- Should each team get their own independent PlayerManager instances?
- Or share the same underlying player pool?
- How do we handle player availability (only 1 instance of each player can be drafted)?
Each team gets their own independant instances, and each gets one for projected and one for actual. After a player is picked by a team, all other teams will be told about that player getting drafted by another team and will thus label the player as drafted=1 in their player data for both instances.

**Q6.2:** ConfigManager handling:
- Each simulation iteration tests a different league_config.json?
- Should we create a new ConfigManager for each test?
- How do we inject the config into AddToRosterModeManager and StarterHelperModeManager?
Yes create a new ConfigManager for every new config being tested. There will only be one json used per end-to-end run of the simulation, though mock json objects should be made and provided to config managers for the generated combinations that are tested. The config manager will then be provided to the Managers through the constructors.

**Q6.3:** Progress tracking:
- Console output showing progress (config X of Y, sim X of Y)?
- Save intermediate results to avoid losing progress?
- Resume capability if interrupted?
Show console output of amount of leagues completed out of how many total will be run, and report how much time has passed and an estimated amount of time remaining.

**Q6.4:** Parallel execution:
- `MAX_PARALLEL_THREADS = 7` means running 7 simulations concurrently?
- Are individual league simulations parallelized, or just running multiple leagues in parallel?
- Thread safety concerns with shared data structures?
Parrallelize the individual league simulations if possible. Make an assessment on if there would be thread safety concerns and find ways to make it work.

---

## 7. Clarifications Needed

**Q7.1:** File structure:
- Should there be a `SimulatedLeague` class to manage the 10 teams + season?
- Do we need a `Week` class to manage matchups and scoring?
- Should results be stored in a database or JSON files?
Yes you can make both those classes, and store the final most optimal configuration found in a json file in simulated_configs

**Q7.2:** Testing approach:
- Should I implement and test with a single manual simulation first?
- Or build the full automated config-testing system from the start?
Test a single manual simulation first then move on to the fully automated system.

**Q7.3:** Validation:
- How do we validate that simulations are realistic?
- Should we compare win rates to expected distributions?
- Any sanity checks on draft results (e.g., top players going in early rounds)?
Set up unit tests to ensure that the draft simulation functions behave as expected and the expected players get taken. Be thourough about setting up unit tests to sanity check logic and ensure nothing breaks over the course of the implementation. Do not worry about the simulations being realistic for now.

**Q7.4:** Edge cases:
- What happens if all "good" players are drafted before DraftHelperTeam's turn?
- How to handle ties in weekly matchups?
- What if a team has insufficient players due to byes/injuries?
There will always be at least 1 player recommended to the DraftHelperTeam through the use of the AddToRosterModeManager and PlayerManager's scoring system. Ties will count as a loss. If there are byes or injuries but the Starter Helper still assigns them to the main starter lineup, then they will just end up contributing 0 points to the week's total. Just trust the Starter Helper's logic there.

---

---

## Notes
- The `optimal_2025-10-02_15-29-14.json.json` file appears to be the baseline config for first iteration
- Real 2024 season data now available in sim_data/ folder
- DraftHelperTeam and SimulatedOpponent classes are just stubs
- No existing code for league simulation, season play, or matchup resolution
- Data files confirm projected vs actual split for realistic simulation
