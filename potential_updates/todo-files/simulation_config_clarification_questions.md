# Simulation Config Updates - Clarification Questions

**Objective**: Update Draft Helper simulation to properly handle configurations from recent scoring overhaul

**Date**: 2025-09-30

---

## Questions Requiring Clarification

### 1. **Simulation Parameter Reduction**
The simulation_config_updates.txt requests capping test values at 2 per variable, but the current `PARAMETER_RANGES` has 3 values for many parameters (e.g., `NORMALIZATION_MAX_SCALE: [80, 100, 120]`).

**Should I:**
- **Option A**: Reduce all existing 3-value parameters to 2 values (removing middle value)?
- **Option B**: Keep existing parameters as-is and only apply the 2-value cap to new parameters?
- **Option C**: Reduce to 2 values only for the variables explicitly listed in the requirements?

**Your Answer:**
Option A

---

### 2. **Enhanced Scoring Parameter Names**
The requirement lists several parameters with slightly different naming than what's in the current config:
- Requirement: `"adp_excellent_multiplier"` vs Current: `'ADP_EXCELLENT_MULTIPLIER'`
- Requirement: `"player_rating_good_multiplier"` vs Current: `'PLAYER_RATING_GOOD_MULTIPLIER'`

**Should I:**
- **Option A**: Keep current uppercase naming convention (consistent with Python config constants)?
- **Option B**: Change to lowercase to match the requirement exactly?

**Your Answer:**
Keep the names consistent with their real config constants

---

### 3. **Player Rating Max Boost**
The requirement includes `"player_rating_max_boost"` which doesn't exist in the current config.

**What should the test range be for this parameter?**
- Conservative: `[15, 20]` (points)
- Moderate: `[20, 30]` (points)
- Aggressive: `[30, 40]` (points)
- Your suggested range: `[___, ___]`

**Your Answer:**
This was a mistake, do not include the player_rating_max_boost in the simulation config

---

### 4. **Starter Helper vs Draft Helper Parameters**
The matchup multipliers (lines 23-27 in current config) are marked as "for Starter Helper".

**Should these parameters:**
- **Option A**: Only affect Starter Helper scoring (menu option 6 in draft_helper)?
- **Option B**: Also affect Trade Helper and other draft_helper modes?
- **Option C**: Be tested in both contexts separately?

**Your Answer:**
The Simulation should only be making use of the Starter Helper and Add to Roster modes. Thus, the matchup multipliers should only be applicable for the starter helper in the simulation runs

---

### 5. **Simulation Scope**
**Should the simulation system test:**
- **Option A**: Only draft mode (initial roster construction)?
- **Option B**: Only trade mode (weekly roster optimization)?
- **Option C**: Both draft and trade modes with separate configuration sets?

**Your Answer:**
The simulation flow should already be set up as expected, we are just ensuring the correct parameters from config files are being tested. The simulation should start by using the draft mode to get the initial teams set up, then it should be simulating the week-by-week matchups using the starter helper. Read through the simulation code to understand this further, and look for the simulation_improvements.txt and simulation_improvements.md files for more context on this, and ask me any questions you need.

---

### 6. **BASE_BYE_PENALTY Removal**
Based on the scoring overhaul, bye week penalties were removed from Starter Helper.

**Should `BASE_BYE_PENALTY`:**
- **Option A**: Be removed from simulation parameters entirely?
- **Option B**: Be kept for draft_helper modes (since starter_helper doesn't use it)?
- **Option C**: Be deprecated but kept for backward compatibility?

**Your Answer:**
Option B

---

## Additional Notes or Questions from User

[Space for any additional clarifications or requirements]

---

**Instructions**: Please fill in your answers for each question above. Once complete, let me know and I'll proceed with creating the comprehensive TODO file and implementation plan.
