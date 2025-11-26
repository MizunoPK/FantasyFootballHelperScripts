# Questions: Overhaul players_projected.csv Creation

**Objective**: Overhaul the player-data-fetcher to correctly create players_projected.csv with projection-only data

**Status**: Awaiting User Answers

**Related Files**:
- `updates/players_projected_overhaul.txt` - Original specification
- `updates/todo-files/players_projected_overhaul_todo.md` - Implementation TODO

---

## Questions

### Q1: Data Model Structure

**Context**: The ESPNPlayerData model currently has `week_1_points` through `week_17_points` fields. We need to add storage for projection-only values.

**Options**:
- **Option A (RECOMMENDED)**: Add individual `week_1_projected` through `week_17_projected` fields
  - Pros: Consistent with existing pattern, explicit fields for Pydantic validation
  - Cons: More verbose (17 new fields)

- **Option B**: Add a `projected_weeks: Dict[int, Optional[float]]` dictionary field
  - Pros: More compact, flexible
  - Cons: Different access pattern than existing `week_N_points` fields

**Question**: Which option should we use for storing projected week values?

**Answer**: Option B

---

### Q2: FantasyPlayer Model Updates

**Context**: The `utils/FantasyPlayer.py` model mirrors the ESPNPlayerData structure. The export method converts ESPNPlayerData to FantasyPlayer before writing CSVs.

**Options**:
- **Option A (RECOMMENDED)**: Skip updating FantasyPlayer, access projected values directly from ESPNPlayerData in the export method
  - Pros: Simpler, fewer files to modify, FantasyPlayer is used in many places
  - Cons: Export method needs direct access to ESPNPlayerData

- **Option B**: Also add projected fields to FantasyPlayer
  - Pros: Consistent data model throughout
  - Cons: More files to modify, more tests to update

**Question**: Should we skip updating `utils/FantasyPlayer.py` and access projected values directly from ESPNPlayerData?

**Answer**: Option A

---

### Q3: fantasy_points_calculator.py Updates

**Context**: During skeptical re-verification, I discovered that `fantasy_points_calculator.py` also references the non-existent `projectedTotal` field. This file is imported and used by `espn_client.py` via the `FantasyPointsExtractor` class.

**Current code references**:
- Lines 10, 37: Config docstrings mention `projectedTotal`
- Lines 113, 137, 144-146, 154-161, 170-172: Logic checks for `projectedTotal`
- Lines 216, 219-220: Fallback logic uses `projectedTotal`

**Options**:
- **Option A (RECOMMENDED)**: Update to use correct ESPN API structure (`statSourceId` + `appliedTotal`)
  - Consistent with our research findings
  - The code currently checks for a field that doesn't exist

- **Option B**: Leave as-is if the `projectedTotal` references are never actually triggered
  - Less work but leaves incorrect code in place

**Question**: Should we update `fantasy_points_calculator.py` to use the correct ESPN API structure (removing `projectedTotal` references)?

**Answer**: Option A

---

### Q4: Scope Clarification - players.csv Behavior

**Context**: The specification says:
- players.csv: Use actuals for weeks < CURRENT_NFL_WEEK, projections for weeks >= CURRENT_NFL_WEEK
- players_projected.csv: Use projections for ALL weeks

**Current behavior**: `espn_client.py` already prioritizes actuals over projections when extracting week data. The current `_extract_raw_espn_week_points()` method does this by default.

**Question**: Should we modify players.csv logic to explicitly use `actuals` for past weeks and `projections` for current+future? Or is the current "smart" behavior (actual if available, fallback to projection) acceptable?

**Current behavior**:
```
Week < CURRENT_NFL_WEEK: Returns actual if available, fallback to projection
Week >= CURRENT_NFL_WEEK: Returns actual if available (shouldn't have any), fallback to projection
```

**Requested behavior per spec**:
```
Week < CURRENT_NFL_WEEK: Returns ONLY actual (statSourceId=0)
Week >= CURRENT_NFL_WEEK: Returns ONLY projection (statSourceId=1)
```

**Answer**: Maintain current behavior

---

## Instructions for User

Please answer each question by filling in the **Answer** field. You can write:
- "Option A" or "Option B" for simple choices
- Additional context or modifications to the recommended approach
- "Skip" if you want to defer the decision

Once all questions are answered, I will:
1. Update the TODO file with your answers
2. Continue with Iterations 6-12 (Second verification round)
3. Begin implementation

---

*Questions generated after completing 5 verification iterations (including skeptical re-verification)*
