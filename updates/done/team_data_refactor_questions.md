# Team Data Refactor - Clarification Questions

These questions arose during codebase research and verification of the implementation plan. Please answer each question to help finalize the TODO file before implementation begins.

---

## Question 1: MIN_WEEKS Configuration Strategy

**Context**: The spec adds MIN_WEEKS to TEAM_QUALITY_SCORING, MATCHUP_SCORING, and SCHEDULE_SCORING. Currently PERFORMANCE_SCORING already has MIN_WEEKS: 3.

**Question**: Should MIN_WEEKS be:

A) **Same value across all three** - One MIN_WEEKS value shared by TEAM_QUALITY, MATCHUP, and SCHEDULE (simpler, current behavior)

B) **Separate values for each** - Independent MIN_WEEKS for each scoring section (more flexible, allows simulation to optimize each independently)

**Recommendation**: Option B (separate values) since simulation can test different rolling windows for each scoring type, which may reveal that team quality benefits from longer windows while matchup benefits from shorter recency.

**Your Answer**: Option B

---

## Question 2: Simulation Data Generation Script

**Context**: The spec requires generating sim_data/team_data/*.csv files from players_actual.csv using season_schedule.csv for opponent lookups. This is complex logic involving:
- Parsing players_actual.csv for weekly fantasy points
- Looking up opponents for each team/week
- Aggregating points by position against each defense
- Writing 32 team CSV files

**Question**: Where should this data generation logic live?

A) **Standalone script** - New file `simulation/generate_team_data.py` (run manually when sim data needs regeneration)

B) **Integrated into SimulationManager** - Method in SimulationManager.py that generates data if missing

C) **Separate utility module** - New `simulation/sim_data_generator.py` that can be imported by SimulationManager

**Recommendation**: Option C - Separate utility module allows both manual execution and programmatic use by SimulationManager.

**Your Answer**: Option A

---

## Question 3: TeamDataManager Signature Change

**Context**: TeamDataManager needs ConfigManager to access MIN_WEEKS values. Current signature:
```python
def __init__(self, data_folder: Path, season_schedule_manager: Optional['SeasonScheduleManager'] = None, current_nfl_week: int = 1)
```

New signature needs ConfigManager. This affects:
- LeagueHelperManager.py (line 83)
- SimulatedLeague.py (line 186)
- Multiple test files

**Question**: How should we handle this signature change?

A) **Breaking change** - Update signature, update all call sites, update all tests (cleanest but more work)

B) **Optional parameter** - Make ConfigManager optional with fallback behavior (maintains some backwards compatibility)

**Recommendation**: Option A - Breaking change is cleaner since we're doing a major refactor anyway. The spec says "NO BACKWARDS COMPATIBILITY with teams.csv" so the same philosophy should apply.

**Your Answer**: Option A

---

## Question 4: Early Season Handling

**Context**: When CURRENT_NFL_WEEK < MIN_WEEKS, there isn't enough historical data to calculate rankings. The current system uses "neutral rankings" (all ranks = 16).

**Question**: How should the new system handle insufficient data?

A) **Return neutral ranks** - When weeks < MIN_WEEKS, return 16 for all rankings (current behavior)

B) **Use available weeks** - If only 3 weeks of data available but MIN_WEEKS=5, use those 3 weeks instead of neutral

C) **Configurable fallback** - Add a config option to choose between A or B

**Recommendation**: Option A matches current behavior and is simplest. Early-season predictions are inherently uncertain anyway.

**Your Answer**: Option A

---

## Question 5: SCHEDULE_SCORING Status

**Context**: SCHEDULE_SCORING is currently disabled in ConfigGenerator.py (commented out). The spec adds MIN_WEEKS to SCHEDULE_SCORING.

**Question**: Should SCHEDULE_SCORING remain disabled or be enabled as part of this refactor?

A) **Keep disabled** - Only add MIN_WEEKS to SCHEDULE_SCORING but leave it disabled in ConfigGenerator

B) **Enable it** - Enable SCHEDULE_SCORING in ConfigGenerator as part of this refactor

**Recommendation**: Option A - Keep it disabled to minimize scope. Enabling can be a separate future change.

**Your Answer**: Option A

---

## Question 6: Week Range for Team Data Files

**Context**: The spec shows weeks 1-17 in team CSV files. However, some contexts reference week 18 (teams_week_18.csv exists in sim_data).

**Question**: Should team data files contain 17 rows (weeks 1-17) or 18 rows (weeks 1-18)?

A) **17 weeks** - Fantasy regular season is weeks 1-17

B) **18 weeks** - Include week 18 for completeness

**Recommendation**: Option A (17 weeks) since fantasy regular season ends at week 17.

**Your Answer**: Option A

---

## Instructions

Please provide your answers above. Once all questions are answered, I will update the TODO file with your decisions and proceed with the second verification round (7 more iterations) before beginning implementation.
