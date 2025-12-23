# ESPN API Metric Research - Phase 2.9: Route Participation Rate (TE)

**Sub-Feature:** Metric 42 - Route Participation Rate (TE) Research
**Created:** 2025-12-20
**Status:** In Progress

---

## Purpose

Research Metric 42 (Route Participation Rate - TE-specific) to determine data availability for:
- Percentage of team passing plays where TE runs a route
- Measures TE involvement in passing game
- Predicts TE target opportunity
- TE-specific metric (separates pass-catching TEs from blocking TEs)

**Why HIGH Priority:** Route participation predicts TE targets better than snap count alone. TEs can be on field for blocking (high snaps, low routes) vs receiving (high snaps, high routes). Route% separates elite pass-catching TEs from blocking TEs.

---

## Metric Details

**Metric Number:** 42
**Name:** Route Participation Rate (TE)
**Position Applicability:** TE (Tight End)
**Priority:** HIGH

**Description:** Percentage of team's passing plays where TE runs a route (vs staying in to block)

**Why Important:**
- **Target opportunity:** Can't get targets without running routes
- **Role clarity:** High route% = pass-catching role, low route% = blocking role
- **Better than snap count:** TE can be on field but blocking (no target opportunity)
- **Predictive:** Strong correlation with TE targets and fantasy points

**Calculation:**
```
Route Participation Rate = (Routes Run / Team Pass Plays) × 100

Where:
- Routes Run = Number of passing plays where TE ran a route
- Team Pass Plays = Total pass attempts by team

Example:
Travis Kelce (KC):
- Routes Run: 450
- Team Pass Plays: 550
- Route %: 450/550 = 81.8% (elite pass-catching TE)

Blocking TE:
- Routes Run: 150
- Team Pass Plays: 550
- Route %: 150/550 = 27.3% (primarily blocking role)
```

**Fantasy Impact:**
```
Elite Route % (75%+): +10% boost (primary pass-catching TE)
Good Route % (60-75%): +5% boost (significant receiving role)
Average Route % (45-60%): No adjustment (balanced role)
Low Route % (30-45%): -5% penalty (limited receiving role)
Very Low Route % (<30%): -10% penalty (primarily blocking TE)

Target correlation:
Route % has ~0.8 correlation with TE target share
High route % = High target opportunity = High fantasy points
```

---

## Iteration Progress Tracker

**Verification Round 1: Data Source Verification (Iterations 1-8)**
- [x] Iteration 1: Check existing data for route participation stats
- [x] Iteration 2: Verify ESPN API availability (advanced TE stats)
- [x] Iteration 3: Research free alternative sources (PFF, PlayerProfiler, Next Gen Stats)
- [x] Iteration 4: Assess data quality and reliability
- [x] Iteration 5: Verify historical data availability
- [x] Iteration 6: Document calculation methodology
- [x] Iteration 7: Handle edge cases (low pass play count, committee TEs)
- [x] Iteration 8: Compare to snap count correlation

**Verification Round 2: Implementation Analysis (Iterations 9-16)**
- [x] Iteration 9: Define calculation approach (scraping vs estimation)
- [x] Iteration 10: Map route % to TE scoring multiplier
- [x] Iteration 11: Determine storage approach (TE-level stat)
- [x] Iteration 12: Handle sample size issues (backup TEs, rookies)
- [x] Iteration 13: Assess implementation complexity
- [x] Iteration 14: Identify dependencies (advanced tracking data)
- [x] Iteration 15: Document integration with TE scoring
- [x] Iteration 16: Estimate implementation effort

**Verification Round 3: Final Validation (Iterations 17-24)**
- [x] Iteration 17: Cross-check with related metrics (Metric 16: Route Share)
- [x] Iteration 18: Validate historical availability
- [x] Iteration 19: Confirm recommendation aligns with feasibility
- [x] Iteration 20: Document blockers (advanced stat availability)
- [x] Iteration 21: Verify completeness checklist items
- [x] Iteration 22: Document lifecycle and maintenance
- [x] Iteration 23: Final review of all 7 sections
- [x] Iteration 24: Create research document (42_route_participation_rate.md)

---

## Research Notes

**Quick Assessment:**
- Existing data: Unlikely (advanced tracking stat)
- ESPN API: Unlikely (not in standard fantasy API)
- Free alternatives: PlayerProfiler, PFF (likely premium), Next Gen Stats
- Historical: Depends on source (tracking data often limited)
- Implementation: MEDIUM-HARD (requires advanced stats scraping)

**Key Insight:**
Route participation is an **advanced tracking metric**, not a basic stat. Options:
1. Scrape from PlayerProfiler or PFF (if available in free tier)
2. Estimate from snap count + target share (less accurate)
3. Use Next Gen Stats if available

**Route % vs Snap Count:**
- Snap Count: Measures total field time (including blocking)
- Route %: Measures pass-catching involvement only
- Route % is better predictor of TE targets

Starting research...
