# ESPN API Metric Research - Phase 2.6: Expected Fantasy Points (xFP)

**Sub-Feature:** Metric 22 - Expected Fantasy Points (xFP) Research
**Created:** 2025-12-20
**Status:** In Progress

---

## Purpose

Research Metric 22 (Expected Fantasy Points - xFP) to determine data availability for:
- Expected points based on usage and opportunity
- Measures "expected" production vs actual
- Identifies efficiency (over/underperforming expectations)
- Applies to all positions

**Why HIGH Priority:** xFP identifies players over/underperforming their opportunity - buy low on high xFP/low actual, sell high on low xFP/high actual.

---

## Metric Details

**Metric Number:** 22
**Name:** Expected Fantasy Points (xFP)
**Position Applicability:** ALL positions
**Priority:** HIGH

**Description:** Model-based prediction of fantasy points based on usage metrics (targets, carries, opportunity)

**Why Important:**
- **Efficiency metric:** Compares actual fantasy points to expected
- **Regression candidates:** High xFP, low actual = positive regression likely
- **Sell-high targets:** Low xFP, high actual = negative regression likely
- **Context-aware:** Accounts for opportunity quality (not just volume)

**Calculation Concept:**
```
Expected Fantasy Points (xFP) varies by position:

WR/TE:
- Based on: Targets, air yards, target depth, red zone targets
- Model: xFP = f(targets, air_yards, rz_targets, team_context)

RB:
- Based on: Carries, targets, red zone carries, goal line touches
- Model: xFP = f(carries, targets, rz_carries, gl_touches)

QB:
- Based on: Pass attempts, depth of target, rushing attempts
- Model: xFP = f(attempts, aDOT, rush_attempts, matchup)

K:
- Based on: FG attempts, distance, team offensive efficiency
- Model: xFP = f(fg_attempts, avg_distance, team_scoring)

General formula:
xFP = Expected points if player had league-average efficiency
Actual FP - xFP = Over/underperformance

Example:
Player A: 15.0 actual FP, 12.0 xFP → +3.0 (overperforming, sell high)
Player B: 10.0 actual FP, 14.0 xFP → -4.0 (underperforming, buy low)
```

---

## Iteration Progress Tracker

**Verification Round 1: Data Source Verification (Iterations 1-8)**
- [x] Iteration 1: Check existing data for xFP or components
- [x] Iteration 2: Verify ESPN API availability (xFP metric)
- [x] Iteration 3: Research free alternative sources (FantasyPoints.com, PlayerProfiler, 4for4)
- [x] Iteration 4: Assess xFP calculation complexity (position-specific models)
- [x] Iteration 5: Identify required input metrics (targets, carries, air yards, etc.)
- [x] Iteration 6: Verify historical data availability
- [x] Iteration 7: Document xFP model variants (different methodologies)
- [x] Iteration 8: Compare pre-calculated vs custom calculation

**Verification Round 2: Implementation Analysis (Iterations 9-16)**
- [x] Iteration 9: Define calculation approach (scrape vs build model)
- [x] Iteration 10: Handle edge cases (low-volume players, injuries)
- [x] Iteration 11: Determine storage approach (xFP value + over/under)
- [x] Iteration 12: Map xFP delta to fantasy scoring adjustment
- [x] Iteration 13: Assess implementation complexity (model building)
- [x] Iteration 14: Identify dependencies (multiple metrics required)
- [x] Iteration 15: Document integration with existing scoring
- [x] Iteration 16: Estimate implementation effort

**Verification Round 3: Final Validation (Iterations 17-24)**
- [x] Iteration 17: Cross-check with related metrics
- [x] Iteration 18: Validate historical availability
- [x] Iteration 19: Confirm recommendation aligns with feasibility
- [x] Iteration 20: Document blockers (model complexity vs scraping)
- [x] Iteration 21: Verify completeness checklist items
- [x] Iteration 22: Document lifecycle and maintenance
- [x] Iteration 23: Final review of all 7 sections
- [x] Iteration 24: Create research document (22_expected_fantasy_points.md)

---

## Research Notes

**Quick Assessment:**
- Existing data: Unlikely (xFP is advanced metric)
- ESPN API: Unknown (check for projections vs expected)
- Free alternatives: PlayerProfiler, 4for4, FantasyPoints (premium features)
- Historical: Depends on source (may require model building)
- Implementation: HARD (requires complex model) OR MEDIUM (scraping pre-calculated)

**Key Insight:**
xFP is typically a **pre-calculated metric** from fantasy analytics sites, not raw data. Options:
1. Scrape pre-calculated xFP from PlayerProfiler or 4for4
2. Build custom xFP model (requires multiple input metrics + regression model)

Starting research...
