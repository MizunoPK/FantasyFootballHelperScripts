# Feature 02: simulation_data_flow_validation - Planning Checklist

**Part of Epic:** bug_fix-compile-historical-data-missing-final-week-stats
**Last Updated:** 2025-12-31 12:13

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## 🚨 CRITICAL DISCOVERY

During research, I found what **appears** to be a bug in the simulation's data loading logic.

**However, I CANNOT ASSUME this is incorrect without user confirmation!**

The questions below are CRITICAL to understanding the intended behavior.

---

## Open Questions

### Question 1: Intended Data Flow for Week N Simulation

**Status:** [ ] OPEN - Needs user clarification (BLOCKING)

**What I discovered:**

Currently, when simulating week N, the code does this:
```python
# Load week_N data
self._load_week_data(week_num)  # week_num = N

# This loads the SAME data into both PlayerManagers:
team.projected_pm.set_player_data(week_player_data)  # week_N data
team.actual_pm.set_player_data(week_player_data)     # week_N data (SAME!)
```

**What week_N data contains (from Feature 01):**
- Actual points for weeks 1 to N-1
- **Projected points for weeks N to 17**

**The issue:**
- When scoring week N, teams use `actual_pm` to get "actual" points
- But `actual_pm` has **projected** data for week N (not actuals!)
- This means week N is scored using projections, not actuals

**My Question:**

**Is this the INTENDED behavior?**

**Option A: Current behavior is CORRECT**
- Week N simulation should use week_N data for BOTH projections and actuals
- The simulation intentionally scores using projections for current week
- No changes needed (just validate week_18 gets loaded)

**Option B: Current behavior is BUGGY**
- Week N simulation should:
  - Use week_N data for projected_pm (draft decisions, projections)
  - Use week_N+1 data for actual_pm (actual scoring)
- For week 17 specifically:
  - Use week_17 for projected_pm
  - Use week_18 for actual_pm (currently missing!)
- This requires code changes to load different data into each PlayerManager

**Which is correct?** (A or B)

**Impact on Implementation:**
- **Option A:** Small scope - just extend pre-loading to include week_18
- **Option B:** Large scope - refactor data loading to use week_N+1 for actuals

---

### Question 2: Purpose of projected_pm vs actual_pm

**Status:** [ ] OPEN - Needs user clarification

**Context:**
Teams have TWO PlayerManager instances:
- `projected_pm` - Used for draft decisions and recommendations
- `actual_pm` - Used for scoring weekly lineups

**Currently both get loaded with the SAME data** (week_N).

**My Question:**

**What is the INTENDED difference between projected_pm and actual_pm?**

**Option A: They should always have the same data**
- Both should use week_N data
- The separation is just for code organization
- No changes needed

**Option B: They should have different data**
- projected_pm should use week_N data (projections for decision-making)
- actual_pm should use week_N+1 data (actuals for scoring)
- This requires code changes

**Which is correct?** (A or B)

---

### Question 3: Week 17 Evaluation with Week 18 Data

**Status:** [ ] OPEN - Needs user clarification

**Context:**
Feature 01 will create week_18 folder with week 17 actual results.

**My Question:**

**How should week 17 be evaluated in the simulation?**

**Option A: Same as current (if Q1 answer is A)**
- Load week_17 data for both projected_pm and actual_pm
- Score week 17 using projections (as current behavior)
- Week_18 data NOT used by simulation

**Option B: Use week_18 for actuals (if Q1 answer is B)**
- Load week_17 for projected_pm
- Load week_18 for actual_pm
- Score week 17 using actuals from week_18

**Which is correct?** (A or B)

**Depends on:** Answer to Question 1

---

## Resolved Questions

{Will populate as questions are answered by user}

---

## Checklist Status

**Open Questions:** 3
**Resolved Questions:** 0
**Blocking Questions:** Question 1 (determines entire feature scope)

**Next Action:** Ask user Question 1 (data flow intent) - THIS IS CRITICAL

---

## Notes

- Question 1 is BLOCKING - answer determines if this is a validation feature or a bug fix feature
- If Answer is A: Small scope, just validate/test
- If Answer is B: Large scope, refactor data loading logic
- Questions 2 and 3 depend on Question 1 answer
- Will update spec.md immediately after each question is answered
