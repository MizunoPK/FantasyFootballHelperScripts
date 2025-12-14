# Always Show Calculated Projection - Checklist

## Instructions

Mark items `[x]` as they are resolved. Each resolved item should have corresponding details added to the specs file.

---

## Open Questions

### Display Format

- [x] **Q1: Which projection value to show?**
  - **RESOLVED: Context-dependent** - Use whatever projection the scoring method used (ROS or single-week)
  - Return the calculated fantasy points as part of ScoredPlayer object

- [x] **Q2: Display format - replace or add to existing score display?**
  - **RESOLVED: Projection primary, score secondary**
  - Format: `{name} - {projection} pts (Score: {score}) (Bye={bye})`

### Scope

- [x] **Q3: Which string methods need updating?**
  - **RESOLVED: ScoredPlayer only** - Update `league_helper/util/ScoredPlayer.py`
  - FantasyPlayer.__str__() unchanged (no scored context)

- [x] **Q4: Should ScoredPlayer have a projected_points field?**
  - **RESOLVED: Yes** - Add field to ScoredPlayer to hold the calculated projection value used in scoring

### Integration

- [x] **Q5: Should AddToRosterMode show the same format?**
  - **RESOLVED: Leave as-is** - Already shows raw projection (`fantasy_points`)
  - Roster review display serves different purpose than scored recommendations

- [x] **Q6: Does Starter Helper mode need changes?**
  - **RESOLVED: No additional changes** - ScoredPlayer.__str__() update applies automatically
  - Lineup totals already show raw projections

---

## Confirmed Requirements

(To be filled in as questions are resolved)

---

## Resolution Log

| Item | Resolution | Resolved By | Date |
|------|------------|-------------|------|
| | | | |

---

## Notes

- The Starter Helper mode already shows "COMBINED PROJECTED POINTS" using raw weekly projections
- The first scoring reason already shows both raw and weighted: `"Projected: X pts, Weighted: Y pts"`
- This feature essentially promotes that information to the main display line
