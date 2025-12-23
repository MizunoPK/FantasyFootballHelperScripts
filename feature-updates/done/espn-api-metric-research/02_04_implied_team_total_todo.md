# ESPN API Metric Research - Phase 2.4: Implied Team Total

**Sub-Feature:** Metric 12 - Implied Team Total Research
**Created:** 2025-12-20
**Status:** In Progress

---

## Purpose

Research Metric 12 (Implied Team Total) to determine data availability for:
- Expected team points based on Vegas lines
- Calculated from spread + over/under
- Predicts scoring environment for all players

**Why HIGH Priority:** Implied team total predicts how many points a team is expected to score - higher total = more fantasy opportunities for all positions.

---

## Metric Details

**Metric Number:** 12
**Name:** Implied Team Total
**Position Applicability:** ALL positions
**Priority:** HIGH

**Description:** Expected team points calculated from Vegas lines (spread + over/under)

**Why Important:**
- **Scoring environment:** High implied total = more scoring opportunities
- **Game script:** Affects play calling (pass vs run)
- **Player volume:** More expected points = more offensive plays

**Calculation:**
```
Implied Team Total = (Over/Under + Spread) / 2  (for favorites)
Implied Team Total = (Over/Under - Spread) / 2  (for underdogs)

Example:
Over/Under: 48.5
Spread: KC -3.5
KC implied total: (48.5 + 3.5) / 2 = 26.0 points
Opponent implied total: (48.5 - 3.5) / 2 = 22.5 points
```

---

## Iteration Progress Tracker

**Verification Round 1: Data Source Verification (Iterations 1-8)**
- [x] Iteration 1: Check existing data (game_data.csv, players.csv) for spread/over_under
- [x] Iteration 2: Verify ESPN API availability (reference 04_vegas_lines.md findings)
- [x] Iteration 3: Research free alternative sources
- [x] Iteration 4: Assess data quality and reliability
- [x] Iteration 5: Verify historical data availability (simulation/sim_data/)
- [x] Iteration 6: Document schema integration approach
- [x] Iteration 7: Assess calculation complexity
- [x] Iteration 8: Document dependencies on Metric 4 (Vegas Lines)

**Verification Round 2: Implementation Analysis (Iterations 9-16)**
- [x] Iteration 9: Define calculation logic (favorite vs underdog)
- [x] Iteration 10: Determine where to store (team-level vs game-level)
- [x] Iteration 11: Handle edge cases (no spread, missing data)
- [x] Iteration 12: Map team total to individual players
- [x] Iteration 13: Define multiplier/boost logic for high totals
- [x] Iteration 14: Verify predictive value (research correlation)
- [x] Iteration 15: Document implementation effort estimate
- [x] Iteration 16: Identify code dependencies and integration points

**Verification Round 3: Final Validation (Iterations 17-24)**
- [x] Iteration 17: Cross-check with related metrics (Metric 4, 9)
- [x] Iteration 18: Validate historical availability matches Metric 4
- [x] Iteration 19: Confirm recommendation aligns with feasibility
- [x] Iteration 20: Document blockers (depends on Metric 4 implementation)
- [x] Iteration 21: Verify completeness checklist items
- [x] Iteration 22: Document lifecycle and maintenance
- [x] Iteration 23: Final review of all 7 sections
- [x] Iteration 24: Create research document (12_implied_team_total.md)

---

## Research Notes

**Quick Assessment:**
- Existing data: Check for spread/over_under columns
- ESPN API: Same as Metric 4 (already researched)
- Free alternatives: Same as Metric 4 (The Odds API, etc.)
- Historical: Same as Metric 4 (PFR has closing lines)
- Implementation: EASY (calculation-only, depends on Metric 4 data)

**Key Dependency:** This metric is **derived from Metric 4 (Vegas Lines)**. Cannot implement until Metric 4 is available.

Starting research...
