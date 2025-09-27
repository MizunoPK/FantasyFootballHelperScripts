# Dual Export Configuration Guide: Projected vs Actual Data

**Generated:** September 26, 2025
**Purpose:** Generate two versions of players.csv and teams.csv - one with projected data, one with actual data
**Method:** Configuration changes only (no code modifications required)

## 🎯 Overview

This guide shows how to generate two distinct versions of your fantasy data files by modifying configuration variables and running the player-data-fetcher twice:

- **Version 1:** Projected players + Initial team rankings
- **Version 2:** Actual players + Final team rankings

## 📊 File Versions Explained

### Players.csv Versions:
| File | Data Source | Content |
|------|-------------|---------|
| `players_projected.csv` | ESPN pre-game projections (`statSourceId: 1`) | What ESPN predicted before games |
| `players_actual.csv` | ESPN post-game results (`statSourceId: 0`) | What actually happened in games |

### Teams.csv Versions:
| File | Data Source | Content |
|------|-------------|---------|
| `teams_initial.csv` | Previous season rankings (2024) | Pre-season expectations |
| `teams_final.csv` | Current season rankings (2025) | Actual performance after games |

---

## 🔧 Configuration Changes Required

### Version 1: Projected Data + Initial Rankings

#### Step 1.1: Configure for Projected Player Data
**File:** `shared_files/fantasy_points_calculator.py`
```python
# Line 36 - Change this setting:
prefer_actual_over_projected: bool = False  # Change from True to False
```

#### Step 1.2: Configure for Initial Team Rankings
**File:** `player-data-fetcher/player_data_fetcher_config.py`
```python
# Line 36-38 - Force use of previous season rankings:
MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 999  # Change from 3 to 999
# This forces the system to always use previous season data = "initial" rankings
```

#### Step 1.3: Run Player Data Fetcher
```bash
.venv\Scripts\python.exe run_player_data_fetcher.py
```

#### Step 1.4: Rename Output Files
```bash
# Windows Command Prompt
move shared_files\players.csv shared_files\players_projected.csv
move shared_files\teams.csv shared_files\teams_initial.csv

# Or PowerShell
Move-Item shared_files\players.csv shared_files\players_projected.csv
Move-Item shared_files\teams.csv shared_files\teams_initial.csv

# Or Git Bash
mv shared_files/players.csv shared_files/players_projected.csv
mv shared_files/teams.csv shared_files/teams_initial.csv
```

---

### Version 2: Actual Data + Final Rankings

#### Step 2.1: Configure for Actual Player Data
**File:** `shared_files/fantasy_points_calculator.py`
```python
# Line 36 - Change back to original setting:
prefer_actual_over_projected: bool = True  # Change back to True
```

#### Step 2.2: Configure for Final Team Rankings
**File:** `player-data-fetcher/player_data_fetcher_config.py`
```python
# Line 36-38 - Use current season rankings:
MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 1  # Change from 999 to 1
# This forces use of current season data = "final" rankings
```

#### Step 2.3: Run Player Data Fetcher Again
```bash
.venv\Scripts\python.exe run_player_data_fetcher.py
```

#### Step 2.4: Rename Output Files
```bash
# Windows Command Prompt
move shared_files\players.csv shared_files\players_actual.csv
move shared_files\teams.csv shared_files\teams_final.csv

# Or PowerShell
Move-Item shared_files\players.csv shared_files\players_actual.csv
Move-Item shared_files\teams.csv shared_files\teams_final.csv

# Or Git Bash
mv shared_files/players.csv shared_files/players_actual.csv
mv shared_files/teams.csv shared_files/teams_final.csv
```

---

## 🔄 Complete Step-by-Step Workflow

### Preparation: Backup Original Config Values
Before starting, note the original values to restore later:
- `prefer_actual_over_projected: bool = True` (original)
- `MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 3` (original)

### Generate Version 1: Projected + Initial
```bash
# 1. Edit shared_files/fantasy_points_calculator.py
#    Line 36: prefer_actual_over_projected: bool = False

# 2. Edit player-data-fetcher/player_data_fetcher_config.py
#    Line 36: MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 999

# 3. Run player data fetcher
.venv\Scripts\python.exe run_player_data_fetcher.py

# 4. Rename outputs
mv shared_files/players.csv shared_files/players_projected.csv
mv shared_files/teams.csv shared_files/teams_initial.csv
```

### Generate Version 2: Actual + Final
```bash
# 1. Edit shared_files/fantasy_points_calculator.py
#    Line 36: prefer_actual_over_projected: bool = True

# 2. Edit player-data-fetcher/player_data_fetcher_config.py
#    Line 36: MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 1

# 3. Run player data fetcher again
.venv\Scripts\python.exe run_player_data_fetcher.py

# 4. Rename outputs
mv shared_files/players.csv shared_files/players_actual.csv
mv shared_files/teams.csv shared_files/teams_final.csv
```

### Restore Original Configuration (Optional)
```bash
# Restore original settings after both exports:
# shared_files/fantasy_points_calculator.py line 36:
prefer_actual_over_projected: bool = True

# player-data-fetcher/player_data_fetcher_config.py line 36:
MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 3
```

---

## 📋 Expected Output Files

After completing both runs, you should have:

### Final File Structure:
```
shared_files/
├── players_projected.csv    # ESPN pre-game projections for all weeks
├── players_actual.csv       # ESPN post-game results for completed weeks
├── teams_initial.csv        # Previous season rankings (pre-season expectations)
├── teams_final.csv          # Current season rankings (actual performance)
└── (original files may be overwritten)
```

### Data Content Differences:

#### players_projected.csv:
- **Weekly Points:** ESPN's pre-game projections (`projectedTotal`)
- **Data Source:** `statSourceId: 1` (projected data)
- **Availability:** All weeks (1-17) have projected values
- **Use Case:** What ESPN expected players to score

#### players_actual.csv:
- **Weekly Points:** Actual game results (`appliedTotal`)
- **Data Source:** `statSourceId: 0` (actual data)
- **Availability:** Only completed weeks have actual values
- **Use Case:** What players actually scored

#### teams_initial.csv:
- **Rankings:** Based on previous season (2024) performance
- **Context:** Pre-season expectations and rankings
- **Use Case:** Initial draft strategy and team strength assessment

#### teams_final.csv:
- **Rankings:** Based on current season (2025) performance
- **Context:** Updated rankings after games played
- **Use Case:** Current team strength for trade/waiver decisions

---

## 🎯 Analysis Opportunities

### Player Performance Analysis:
- **Projection Accuracy:** Compare projected vs actual points for each player/week
- **Boom/Bust Identification:** Find players with high variance between projected and actual
- **Consistency Metrics:** Identify reliable players who meet projections regularly
- **Position Analysis:** Compare projection accuracy across QB/RB/WR/TE positions

### Team Strength Evolution:
- **Ranking Changes:** Track how team rankings evolved from initial to final
- **Surprise Teams:** Identify teams that significantly outperformed/underperformed expectations
- **Strength of Schedule:** Use ranking changes to assess schedule difficulty

### Fantasy Strategy Insights:
- **Undervalued Players:** Find players who consistently exceed projections
- **Overvalued Players:** Identify players who consistently underperform projections
- **Matchup Analysis:** Use team ranking evolution for future matchup predictions
- **Waiver Wire Targets:** Find consistently undervalued players for pickup

---

## ⚠️ Important Considerations

### Data Availability:
- **Current Season (2025):** Only completed weeks will have actual data
- **Historical Season (2024):** Complete projected vs actual data available
- **Team Rankings:** Previous season = complete, current season = in progress

### For Historical Analysis:
To generate 2024 data instead of 2025, also change:
**File:** `shared_config.py`
```python
NFL_SEASON = 2024  # Change from 2025 to 2024
```

### File Management:
- The process overwrites the original `players.csv` and `teams.csv` each time
- Always rename files immediately after each run
- Consider backing up original files before starting

### Performance:
- Each run takes 8-15 minutes for the full player data fetch
- Total time for both versions: ~16-30 minutes
- API calls remain optimized (646 calls per run)

---

## 🔧 Troubleshooting

### Common Issues:

#### No Actual Data for Future Weeks:
- **Problem:** Future weeks show 0.0 points in actual version
- **Solution:** This is expected - actual data only exists for completed games

#### Team Rankings Don't Change:
- **Problem:** Initial and final team rankings are identical
- **Solution:** Verify `MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS` was changed correctly

#### Files Not Generated:
- **Problem:** CSV files missing after run
- **Solution:** Check that player data fetcher completed successfully, check logs

#### Projected Data Looks Like Actual:
- **Problem:** Projected version has actual-looking data
- **Solution:** Verify `prefer_actual_over_projected: bool = False` was set correctly

### Validation Steps:
1. **Check projected data:** Should have decimal values that look like projections
2. **Check actual data:** Should have integer-like values for completed weeks
3. **Compare team rankings:** Initial and final should be different if season is in progress
4. **Verify file timestamps:** Ensure files were generated from recent runs

---

## 📊 Configuration Reference

### Key Configuration Files and Lines:

| File | Line | Setting | Projected Version | Actual Version |
|------|------|---------|------------------|----------------|
| `shared_files/fantasy_points_calculator.py` | 36 | `prefer_actual_over_projected` | `False` | `True` |
| `player-data-fetcher/player_data_fetcher_config.py` | 36 | `MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS` | `999` | `1` |

### Original Values (for restoration):
- `prefer_actual_over_projected: bool = True`
- `MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 3`

---

## 🚀 Conclusion

This configuration-based approach allows you to generate comprehensive projected vs actual analysis data without any code modifications. By simply changing two configuration variables and running the player data fetcher twice, you can create powerful datasets for:

- Player performance analysis
- Projection accuracy studies
- Team strength evolution tracking
- Fantasy strategy optimization

The resulting files provide a complete foundation for advanced fantasy football analytics and decision-making tools.

---

**Total Implementation Time:** ~30-45 minutes (including both data fetching runs)
**Code Changes Required:** 0 (configuration only)
**Analysis Value:** High (complete projected vs actual dataset)