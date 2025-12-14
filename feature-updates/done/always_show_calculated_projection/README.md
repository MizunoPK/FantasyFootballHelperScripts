# Always Show Calculated Projection - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** COMPLETE
**Current Step:** Done
**Next Action:** Commit and move to done/

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create always_show_calculated_projection_specs.md
  - [x] Create always_show_calculated_projection_checklist.md
  - [x] Create always_show_calculated_projection_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] Analyze notes thoroughly
  - [x] Research codebase patterns
  - [x] Populate checklist with questions
  - [x] Update specs with context
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Wait for user direction
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved [x]
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 1: Create TODO file
- [x] 24 Verification Iterations complete
- [x] Implementation complete
- [x] Tests passing (100% - 2223 tests)

**POST-IMPLEMENTATION PHASE**
- [x] QC Round 1 - Verified all changes
- [x] QC Round 2 - Verified algorithm and edge cases
- [x] QC Round 3 - Final skeptical review
- [x] Commit changes
- [x] Move folder to done/

---

## What This Is

Update player display methods (`__str__`, print statements) to always show the **raw/un-normalized projected points** (the actual fantasy points projection) in addition to or instead of just the weighted scoring value. Currently, player displays show the weighted `score` value used for rankings, but users want to see the actual projected fantasy points like what's displayed in Starter Helper mode.

## Why We Need This

1. **Clarity:** The weighted score (e.g., "145.67 pts") doesn't represent actual fantasy points - it's a normalized value for comparison
2. **Consistency:** Starter Helper mode shows "COMBINED PROJECTED POINTS" using raw values, but other modes don't show this
3. **User Expectation:** Users expect to see actual projected fantasy points when viewing player information

## Scope

**IN SCOPE:**
- Update `FantasyPlayer.__str__()` to show raw projected points
- Update `ScoredPlayer.__str__()` to show raw projected points
- Potentially update scoring method return values to include raw projection
- Update relevant print statements that display player information

**OUT OF SCOPE:**
- Changing how scoring calculations work
- Modifying the weighted score algorithm
- Changing the Starter Helper mode (already shows raw projections)

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `always_show_calculated_projection_notes.txt` | Original scratchwork notes from user |
| `always_show_calculated_projection_specs.md` | Main specification with detailed requirements |
| `always_show_calculated_projection_checklist.md` | Tracks open questions and decisions |
| `always_show_calculated_projection_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Current Player Display Formats

**FantasyPlayer.__str__()** - `utils/FantasyPlayer.py:380-400`
```
Patrick Mahomes (KC QB) - 15.3 pts (QUESTIONABLE) [Bye=7] [ROSTERED]
                          ^^^^
                          This is `score` (weighted value)
```

**ScoredPlayer.__str__()** - `league_helper/util/ScoredPlayer.py:64-89`
```
[QB] [KC] Patrick Mahomes - 123.45 pts (Bye=7)
                            ^^^^^^
                            This is `score` (weighted value)
```

### Where Raw Projection IS Shown

**player_scoring.py:474** - First scoring reason shows both:
```
"Projected: {orig_pts:.2f} pts, Weighted: {weighted_pts:.2f} pts"
```

**StarterHelperModeManager:349** - Combined lineup projection:
```
print(f"COMBINED PROJECTED POINTS: {total_raw_projected:.1f} pts")
```

### Key Data Fields

| Field | Location | Description |
|-------|----------|-------------|
| `fantasy_points` | FantasyPlayer | Total season projected points |
| `week_N_points` | FantasyPlayer | Weekly projection (weeks 1-17) |
| `score` | FantasyPlayer/ScoredPlayer | Weighted/normalized score for ranking |
| `weighted_projection` | FantasyPlayer | Normalized projection (0-N scale) |

## What's Resolved

1. **Q1 - Projection Value:** Context-dependent - use whatever projection the scoring method used (ROS or single-week)
2. **Q2 - Display Format:** Projection primary with score secondary: `{name} - {projection} pts (Score: {score}) (Bye={bye})`
3. **Q3 - Methods to Update:** ScoredPlayer.__str__() only
4. **Q4 - ScoredPlayer Field:** Add `projected_points` field to hold calculated projection
5. **Q5 - AddToRosterMode:** Leave as-is (already shows raw projection)
6. **Q6 - Starter Helper:** No changes needed (ScoredPlayer update applies automatically)

## What's Still Pending

(None - planning complete, ready for implementation)

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `always_show_calculated_projection_specs.md` for complete specifications
3. Read `always_show_calculated_projection_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
