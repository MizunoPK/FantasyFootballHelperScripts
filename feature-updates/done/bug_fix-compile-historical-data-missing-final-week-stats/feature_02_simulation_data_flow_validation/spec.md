# Feature 02: simulation_data_flow_validation

**Part of Epic:** bug_fix-compile-historical-data-missing-final-week-stats
**Feature Number:** 2 of 2
**Created:** 2025-12-31
**Last Updated:** 2025-12-31 12:12

---

## Objective

Verify and validate that the simulation system correctly uses week_N data for player projections when simulating week N, and week_N+1 data for actual results when evaluating week N performance. Ensure the new week_18 data is properly consumed for week 17 evaluation.

---

## Current System Analysis

### Files Identified

**Main Simulation:**
- `simulation/win_rate/SimulatedLeague.py`
  - Line 266-294: `_preload_all_weeks()` - Pre-loads weeks 1-17 data into cache
  - Line 318-344: `_load_week_data()` - Loads week-specific data at start of each week
  - Line 403-437: `run_season()` - Simulates 17-week season
  - Line 131-209: `_initialize_teams()` - Creates projected_pm and actual_pm for each team

**Weekly Simulation:**
- `simulation/win_rate/Week.py`
  - Line 89-129: `simulate_week()` - Simulates matchups for a week
  - Line 109-110: Calls `team.set_weekly_lineup()` to get actual points scored

### Current Data Flow

**Team Initialization (uses week 1 for initial setup):**
```python
# Line 161-166
weeks_folder = self.data_folder / "weeks" / "week_01"
if weeks_folder.exists():
    players_projected_path = weeks_folder / "players_projected.csv"
    players_actual_path = weeks_folder / "players.csv"

# Line 195-196
projected_pm = PlayerManager(shared_projected_dir, ...)  # For draft decisions
actual_pm = PlayerManager(shared_actual_dir, ...)        # For scoring actual points
```

**Pre-Loading Weeks (currently loads 1-17):**
```python
# Line 284
for week_num in range(1, 18):  # Weeks 1-17 ONLY
    week_folder = weeks_folder / f"week_{week_num:02d}"
    self.week_data_cache[week_num] = self._parse_players_csv(week_folder / "players.csv")
```

**Loading Week Data During Season:**
```python
# Line 335-342
week_player_data = self.week_data_cache[week_num]

for team in self.teams:
    team.projected_pm.set_player_data(week_player_data)  # SAME DATA
    team.actual_pm.set_player_data(week_player_data)     # SAME DATA
```

**The Problem:**
- Both projected_pm and actual_pm get loaded with THE SAME week_N data
- week_N/players.csv contains: actuals 1 to N-1, **projections** N to 17
- When scoring week N, actual_pm uses **projected** data for week N (not actuals!)
- For week 17: No week_18 data loaded, so week 17 scoring uses projections

---

## Scope

**What's included in THIS feature:**
- **CRITICAL:** Clarify intended data flow with user (don't assume!)
- Analyze and document current simulation data loading behavior
- Determine if current behavior is correct or buggy
- If buggy: Fix data loading to use week_N+1 for week_N actuals
- Ensure week_18 data is loaded and used for week 17 actuals
- Create comprehensive tests validating data flow
- Document the correct data flow pattern

**What's NOT included:**
- Changes to compile historical data script (that's Feature 01)
- Performance optimizations (out of scope)
- UI/reporting changes (out of scope)

---

## Open Questions

**🚨 CRITICAL: I discovered potential bugs in current implementation**

**I CANNOT ASSUME the current implementation is wrong - must clarify with user first!**

See `checklist.md` for detailed questions about intended data flow.

Key questions:
1. Is the current data flow correct (week_N for both projections AND actuals)?
2. What is the intended purpose of projected_pm vs actual_pm?
3. How should week 17 be evaluated with week_18 data?

---

## Dependencies

**Prerequisites:** Feature 01 (requires week_18 folder to exist)
**Blocks:** None (final feature in epic)

**External Dependencies:**
- Week 18 data created by Feature 01
- Simulation system's PlayerManager.set_player_data() method

---

## Estimates

- Implementation items: ~20-25 (will refine after questions resolved)
- Risk level: HIGH (may require significant simulation changes if data flow is buggy)
- Priority: HIGH (validates entire bug fix)

---

## Testing Strategy

**Will define after questions resolved - test strategy depends on intended behavior**

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2025-12-31 | Agent | Initial spec created | Stage 1 (Epic Planning) |
| 2025-12-31 | Agent | Added technical details from research | Stage 2 Phase 1 (Targeted Research) |

---

**Status:** Stage 2 Phase 1 complete (Targeted Research)
**Next:** Phase 2 - Create checklist.md with CRITICAL questions about data flow intent
