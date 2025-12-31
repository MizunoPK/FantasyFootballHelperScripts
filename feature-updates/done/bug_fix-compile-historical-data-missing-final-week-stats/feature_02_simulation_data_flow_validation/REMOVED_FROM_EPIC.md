# Feature 02: simulation_data_flow_validation - REMOVED FROM EPIC

**Date Removed:** 2025-12-31
**Stage When Removed:** Stage 2 (Feature Deep Dive)
**Removed By:** User decision

---

## Reason for Removal

During Stage 2 deep dive research, I discovered that the simulation's data loading logic has significant bugs that are more complex than initially anticipated.

**User's decision:** "The simulation is very broken currently. Let's scrap this feature and just focus on having the historical data compiler get the data we want. We will make another epic for updating the simulation."

---

## What Was Discovered

**The simulation currently:**
1. Loads week_N data for both `projected_pm` and `actual_pm`
2. Uses the SAME data for both projections AND actuals
3. week_N data contains: actuals 1 to N-1, **projections** N to 17
4. When scoring week N, uses **projected** data instead of actuals
5. For week 17: No week_18 data, so week 17 scores using projections

**This affects:**
- All 17 weeks of simulation (not just week 17)
- The entire simulation validation system
- Multiple simulation modules (SimulatedLeague, Week, teams)

---

## Research Preserved for Future Epic

**All research is preserved in:**
- `research/FEATURE_02_DISCOVERY.md` - Complete analysis of simulation data flow bugs
- `spec.md` - Initial spec with problem analysis
- `checklist.md` - Critical questions about intended behavior

**This research will be valuable when creating the simulation fix epic.**

---

## Impact on Current Epic

**Epic scope changed to:**
- Feature 01 ONLY: Create week_18 data folder with compile historical data script
- Simulation validation: OUT OF SCOPE (future epic)

**Epic remains valid:**
- Creating week_18 data is still useful (even though simulation doesn't use it yet)
- When simulation is fixed in future epic, week_18 data will be ready
- Historical data will be complete for all 17 weeks

---

## Future Epic Recommendation

**For the simulation fix epic, consider:**

1. **Scope:** Fix simulation data loading to use week_N+1 for actuals
2. **Files affected:**
   - `simulation/win_rate/SimulatedLeague.py` (_load_week_data, _preload_all_weeks)
   - Potentially other simulation modules
3. **Dependencies:** This epic (week_18 data must exist first)
4. **Research:** Start with `research/FEATURE_02_DISCOVERY.md` from this epic

---

**This folder preserved for future reference.**
**Do not delete** - contains valuable research for simulation epic.
