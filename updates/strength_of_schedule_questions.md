# Strength of Schedule Implementation - Questions

This file contains clarifying questions about the implementation based on my research of the codebase and the requirements in `strength_of_schedule.txt`.

---

## Phase 1: ESPN API & Data Sources

### Q1: ESPN API - Position-Specific Defense Data
**Question**: Can the ESPN API provide position-specific defensive rankings (def_vs_qb_rank, def_vs_rb_rank, etc.), or will we need to calculate these ourselves from other metrics?

**Context**: The requirement mentions "Investigate the ESPN API for the positional defense data." I need to know if:
- ESPN provides this data directly
- We need to calculate it from other stats (e.g., points allowed to each position)
- We should use a different data source

**Options**:
1. ESPN API provides position-specific defense rankings directly
2. ESPN provides raw stats, we calculate rankings
3. Use alternative data source (which one?)

**Recommendation**: _(Pending your investigation or knowledge of ESPN API)_
You should go ahead and investigate this yourself. Add a TODO item to investigate the ESPN API and update the TODO with your findings. Perform 5 iterations of verification where you go back and re-examine the ESPN API and your findings to ensure the most accurate and best solution is found and documented.

---

### Q2: ESPN API - Full Season Schedule
**Question**: Can the ESPN API provide the complete season schedule (all teams, all weeks), or should we use a different source?

**Context**: Need to populate season_schedule.csv with week-by-week matchups.

**Options**:
1. ESPN API provides full schedule
2. Use NFL.com or another source
3. Manual data entry / static file

**Recommendation**: _(Pending your knowledge)_
Same as Q1

---

## Phase 3: season_schedule.csv Schema

### Q3: season_schedule.csv Column Design
**Question**: What columns should season_schedule.csv contain?

**Current thinking**:
```csv
week,team,opponent
1,KC,BAL
1,BAL,KC
2,KC,CIN
```

**Should we also include**:
- `home_away` (H/A indicator)?
- `date` (game date)?
- `game_id` (for tracking)?

**Options**:
1. Minimal: `week, team, opponent` only
2. Standard: `week, team, opponent, home_away`
3. Extended: `week, team, opponent, home_away, date`

**Recommendation**: Start with **Option 1 (Minimal)** for simplicity. Can add columns later if needed.
Option A

---

### Q4: Bye Week Representation
**Question**: How should bye weeks be represented in season_schedule.csv?

**Options**:
1. Empty opponent field: `5,KC,` (empty string)
2. Special value: `5,KC,BYE`
3. Omit the row entirely (no entry for team during bye week)

**Recommendation**: **Option 1 (Empty opponent)** - Consistent with current teams.csv pattern and easier to parse.
Option 1

---

## Phase 7: SCHEDULE_SCORING Configuration

### Q5: SCHEDULE_SCORING Initial Values
**Question**: What should the initial values be for the SCHEDULE_SCORING configuration?

**Current thinking** based on existing patterns:
```json
"SCHEDULE_SCORING": {
  "THRESHOLDS": {
    "BASE_POSITION": 16,        // Middle of 32 teams
    "DIRECTION": "INCREASING",  // Higher avg rank = easier schedule = better
    "STEPS": 8                  // Roughly quarters of the rankings (32/4=8)
  },
  "MULTIPLIERS": {
    "VERY_POOR": 0.95,   // Facing top defenses (avg rank ~0-8)
    "POOR": 0.975,       // Facing good defenses (avg rank ~8-16)
    "GOOD": 1.025,       // Facing weak defenses (avg rank ~24-32)
    "EXCELLENT": 1.05    // Facing worst defenses (avg rank ~32+)
  },
  "WEIGHT": 1.0          // Start at 1.0, will be optimized by simulation
}
```

**Do you want different values?** These will be optimized by the simulation system anyway.

**Recommendation**: Use the values above as starting point, let simulation optimize them.
Yes start with these for now

---

## Phase 8: Schedule Scoring Implementation

### Q6: Minimum Future Games for Schedule Calculation
**Question**: What is the minimum number of future games with valid data required to calculate a meaningful schedule value?

**Context**: Near end of season or when most future opponents are missing data, we may not have enough games to calculate an average.

**Options**:
1. Require at least 1 future game
2. Require at least 2 future games (more stable average)
3. Require at least 3 future games
4. Scale confidence based on number of games (fewer games = less weight)

**Recommendation**: **Option 2 (Require 2+ games)** - Balances having data with statistical stability. Return `None` if fewer than 2 valid future games.
Option 2


---

### Q7: End of Season Handling
**Question**: How should schedule scoring behave in the final weeks when there are few/no future games?

**Options**:
1. Return `None` (no schedule multiplier applied)
2. Use last N weeks of schedule in reverse (historical difficulty)
3. Apply neutral multiplier (1.0)

**Recommendation**: **Option 1 (Return None)** - Consistent with how performance multiplier handles insufficient data. Schedule becomes irrelevant at season end anyway.
Option 1

---

## Phase 9-10: Mode Integration

### Q8: StarterHelperMode Schedule Scoring
**Question**: Should the StarterHelperMode (weekly lineup optimizer) use schedule scoring?

**Context**: StarterHelperMode focuses on weekly projections and short-term performance. Schedule scoring looks at rest-of-season difficulty.

**Arguments for YES**:
- Helps decide who to keep on bench vs start based on future value
- Useful for season-long lineup planning

**Arguments for NO**:
- StarterHelperMode uses weekly projections, not rest-of-season
- Schedule doesn't matter for "who do I start this week?"
- Keeps the mode focused on immediate performance

**Recommendation**: **NO (keep schedule=False)** - StarterHelperMode should focus on immediate week performance only. Schedule scoring is for rest-of-season decisions (draft, trades).

NO, do not enable for the Starter Mode. Use it for Add to Roster mode and all of the Trade Simulator modes

---

### Q9: Default Schedule Scoring Behavior
**Question**: Should schedule scoring be enabled by default in PlayerManager initialization, or only when explicitly requested?

**Current implementation**: All multipliers have default values in score_player signature. Examples:
- `adp=False` (disabled by default)
- `player_rating=True` (enabled by default)
- `matchup=False` (disabled by default)

**What should `schedule` default be?**

**Options**:
1. `schedule=False` (disabled by default, explicit opt-in)
2. `schedule=True` (enabled by default, explicit opt-out)

**Recommendation**: **Option 1 (schedule=False)** - Consistent with `adp` and `matchup` patterns. Modes that need it will explicitly enable it.

Enable it by default

---

## Phase 11: Simulation System

### Q10: Schedule Simulation Parameter Ranges
**Question**: What ranges should the simulation system test for SCHEDULE_SCORING parameters?

**Current patterns** (from ConfigGenerator):
- ADP: STEPS=[20-50], WEIGHT=[0.5-3.0]
- PLAYER_RATING: STEPS=[10-40], WEIGHT=[0.5-3.0]

**Proposed for SCHEDULE_SCORING**:
- `BASE_POSITION`: Fixed at 16 (middle of rankings)
- `DIRECTION`: Fixed at "INCREASING" (higher rank = easier)
- `STEPS`: Test range [4, 6, 8, 10, 12] (different granularities)
- `WEIGHT`: Test range [0.5, 1.0, 1.5, 2.0, 2.5, 3.0] (same as others)

**Do these ranges make sense?**

**Recommendation**: Start with these ranges. They provide good coverage without excessive combinations.
Yes keep it aligned with other patterns for now

---

## Additional Questions

### Q11: Position-Specific Defense Rankings Calculation
**Question**: If we need to calculate position-specific defense rankings ourselves (not provided by ESPN API), what stats should we use?

**Options**:
1. Fantasy points allowed to each position (direct measure)
2. Yards allowed + TDs allowed to each position
3. Opponent position performance vs their season average
4. Composite score combining multiple stats

**Recommendation**: **Option 1 (Fantasy points allowed)** - Most directly relevant to fantasy football. Need to verify if ESPN provides this data.
This should - in theory be provided by the ESPN API. If not, then bring it up to me again and we will figure out a solution

---

### Q12: Week-Specific Team Rankings
**Question**: The current system has weekly team ranking files (`teams_week_N.csv`). Should position-specific defense rankings also be week-specific?

**Context**: Current system has:
- `data/teams_week_1.csv`
- `data/teams_week_2.csv`
- etc.

**Options**:
1. Position-specific rankings are week-specific (teams_week_N.csv includes def_vs_qb_rank, etc.)
2. Position-specific rankings are season-long (single teams.csv file)

**Recommendation**: **Option 1 (Week-specific)** - Maintains consistency with existing architecture. Defense performance changes weekly.
Yes maintain the week-specific versions. The rankings will change over the course of the season. Each file will have the same rankings for now and we will update them with real data later, but keep the system of using multiple files


---

## Summary

**Critical decisions needed**:
1. ✅ Q3: season_schedule.csv schema → **Minimal (week, team, opponent)**
2. ✅ Q4: Bye week representation → **Empty opponent field**
3. ✅ Q5: Initial SCHEDULE_SCORING values → **Use proposed values**
4. ✅ Q6: Minimum future games → **Require 2+ games**
5. ✅ Q7: End of season → **Return None**
6. ✅ Q8: StarterHelperMode → **NO schedule scoring**
7. ✅ Q9: Default behavior → **schedule=TRUE (enable by default)**
8. ✅ Q10: Simulation ranges → **Use proposed ranges**

**API Investigation needed** (must be done first):
1. ❓ Q1: Can ESPN provide position-specific defense rankings?
2. ❓ Q2: Can ESPN provide full season schedule?
3. ❓ Q11: How to calculate position-specific rankings if needed?
4. ❓ Q12: Should rankings be week-specific?

**Recommendation**: Start with Phase 1 (API investigation) to answer Q1, Q2, Q11, Q12. This will inform the implementation approach for all subsequent phases.
