# Feature 02: simulation_data_flow_validation - Discovery Findings

**Research Date:** 2025-12-31
**Researcher:** Agent

---

## Components Identified

**Main Simulation Files:**
- `simulation/win_rate/SimulatedLeague.py`
  - Lines 266-294: `_preload_all_weeks()` - Pre-loads weeks 1-17 data
  - Lines 318-344: `_load_week_data()` - Loads week-specific data at start of each week
  - Lines 403-437: `run_season()` - Simulates 17-week season
  - Lines 131-209: `_initialize_teams()` - Creates projected_pm and actual_pm for each team

**Weekly Simulation:**
- `simulation/win_rate/Week.py`
  - Lines 89-129: `simulate_week()` - Simulates matchups for a week
  - Line 109-110: Calls `team.set_weekly_lineup()` to get actual points scored

---

## Current Data Flow

**Team Initialization (line 161-196):**
```python
# For historical structure, use week 1 data for initial setup
weeks_folder = self.data_folder / "weeks" / "week_01"
if weeks_folder.exists():
    players_projected_path = weeks_folder / "players_projected.csv"
    players_actual_path = weeks_folder / "players.csv"

# Each team gets two PlayerManager instances:
projected_pm = PlayerManager(shared_projected_dir, ...)  # For draft decisions
actual_pm = PlayerManager(shared_actual_dir, ...)        # For scoring actual points
```

**Pre-Loading Week Data (line 266-294):**
```python
def _preload_all_weeks(self):
    for week_num in range(1, 18):  # Weeks 1-17
        week_folder = weeks_folder / f"week_{week_num:02d}"
        players_file = week_folder / "players.csv"
        if players_file.exists():
            self.week_data_cache[week_num] = self._parse_players_csv(players_file)
```

**Loading Week Data During Season (line 318-344):**
```python
def _load_week_data(self, week_num: int):
    week_player_data = self.week_data_cache[week_num]

    # Update each team's PlayerManagers with week-specific data
    for team in self.teams:
        team.projected_pm.set_player_data(week_player_data)
        team.actual_pm.set_player_data(week_player_data)
```

**Season Simulation (line 403-437):**
```python
def run_season(self):
    for week_num in range(1, 18):  # Weeks 1-17
        # Load week-specific player data from cache
        self._load_week_data(week_num)

        # Update team rankings
        self._update_team_rankings(week_num)

        # Simulate week
        week = Week(week_num, matchups)
        week.simulate_week()
```

---

## The Problem (Data Flow Bug)

**Current behavior when simulating week N:**
1. Load week_N data from cache
2. Week_N/players.csv contains:
   - Actual points for weeks 1 to N-1
   - **Projected points for week N to 17**
3. Teams use `actual_pm` to score their week N lineup
4. But `actual_pm` has **projected** data for week N (not actuals!)

**Expected behavior:**
- Week_N simulation should use week_N for projections/decisions
- Week_N scoring should use week_N+1 for actual results

**The bug for week 17:**
- Week 17 simulation loads week_17 data
- week_17/players.csv has: actuals 1-16, **projections for week 17**
- Week 17 scoring uses projections instead of actuals
- **No week_18 data exists to provide week 17 actuals**

---

## Questions for User

**I need to understand the intended data flow:**

1. **Question: Is the current implementation correct?**
   - Does the simulation intentionally use week_N data for both projections AND actuals for week N?
   - Or is there a bug where it should be using week_N+1 for actuals?

2. **Question: What is the purpose of projected_pm vs actual_pm?**
   - Both seem to get loaded with the same week_N data
   - If actual_pm should have "actual" data, shouldn't it load from week_N+1?

3. **Question: How should week 17 be evaluated?**
   - Should week 17 simulation use week_18 data for actuals?
   - Or should it be evaluated differently?

---

## Hypothesis

Based on the epic description and Feature 01, I believe:

**HYPOTHESIS (needs user confirmation):**
- Current implementation is BUGGY
- Week N simulation should:
  - Use week_N for draft decisions/projections
  - Use week_N+1 for actual scoring/results
- Week 17 simulation should:
  - Use week_17 for draft decisions/projections
  - Use week_18 for actual scoring/results (currently missing!)

**If this hypothesis is correct, the fix would be:**
1. Modify `_preload_all_weeks()` to load weeks 1-18 (not 1-17)
2. Modify `_load_week_data()` to load week_N for projected_pm, week_N+1 for actual_pm
3. Handle week 17 special case (use week_18 for actuals)

**BUT I CANNOT ASSUME THIS - MUST ASK USER FIRST**

---

## Next Steps

1. Create checklist.md with questions for user
2. Ask user to clarify the intended data flow
3. Only after confirmation, update spec.md with the correct approach
4. DO NOT make assumptions about "correct" behavior
