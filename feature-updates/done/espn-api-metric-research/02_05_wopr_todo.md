# ESPN API Metric Research - Phase 2.5: WOPR (Weighted Opportunity Rating)

**Sub-Feature:** Metric 21 - WOPR (Weighted Opportunity Rating) Research
**Created:** 2025-12-20
**Status:** In Progress

---

## Purpose

Research Metric 21 (WOPR - Weighted Opportunity Rating) to determine data availability for:
- Target share percentage
- Air yards share percentage
- Combined opportunity metric for pass-catchers
- Predicts fantasy upside for WR/TE

**Why HIGH Priority:** WOPR combines target volume and air yards to identify high-opportunity receivers - correlates strongly with fantasy production.

---

## Metric Details

**Metric Number:** 21
**Name:** WOPR (Weighted Opportunity Rating)
**Position Applicability:** WR, TE
**Priority:** HIGH

**Description:** Weighted combination of target share and air yards share, measures overall opportunity

**Why Important:**
- **Opportunity metric:** Combines volume (targets) and quality (air yards)
- **Fantasy correlation:** High WOPR = high fantasy upside
- **Predictive:** Better than targets alone (accounts for depth of target)

**Calculation:**
```
WOPR = (1.5 × Target Share) + (0.7 × Air Yards Share)

Where:
- Target Share = Player Targets / Team Total Targets
- Air Yards Share = Player Air Yards / Team Total Air Yards
- Weights: Targets weighted higher (1.5) than air yards (0.7)

Example:
Tyreek Hill (MIA):
- Targets: 10 / 35 team targets = 28.6% target share
- Air Yards: 150 / 400 team air yards = 37.5% air yards share
- WOPR = (1.5 × 0.286) + (0.7 × 0.375) = 0.429 + 0.263 = 0.692 (69.2%)

High WOPR (>50%) = elite opportunity
Medium WOPR (30-50%) = solid opportunity
Low WOPR (<30%) = limited opportunity
```

---

## Iteration Progress Tracker

**Verification Round 1: Data Source Verification (Iterations 1-8)**
- [x] Iteration 1: Check existing data for targets and air yards
- [x] Iteration 2: Verify ESPN API availability for targets (reference Metric 1)
- [x] Iteration 3: Research ESPN API for air yards data
- [x] Iteration 4: Research free alternative sources for air yards
- [x] Iteration 5: Assess data quality and reliability of WOPR calculation
- [x] Iteration 6: Verify historical data availability (targets + air yards)
- [x] Iteration 7: Document calculation methodology and weights
- [x] Iteration 8: Compare WOPR variants (different weighting schemes)

**Verification Round 2: Implementation Analysis (Iterations 9-16)**
- [x] Iteration 9: Define calculation logic (team aggregation required)
- [x] Iteration 10: Handle edge cases (low-target games, missing air yards)
- [x] Iteration 11: Determine storage approach (calculated vs stored)
- [x] Iteration 12: Map WOPR to fantasy scoring multiplier
- [x] Iteration 13: Assess implementation complexity (depends on Metric 1)
- [x] Iteration 14: Identify dependencies (Metric 1: Targets, Metric 13: Air Yards)
- [x] Iteration 15: Document integration with existing scoring system
- [x] Iteration 16: Estimate implementation effort

**Verification Round 3: Final Validation (Iterations 17-24)**
- [x] Iteration 17: Cross-check with related metrics (Metric 1, 13)
- [x] Iteration 18: Validate historical availability matches dependencies
- [x] Iteration 19: Confirm recommendation aligns with feasibility
- [x] Iteration 20: Document blockers (depends on Metrics 1 + 13)
- [x] Iteration 21: Verify completeness checklist items
- [x] Iteration 22: Document lifecycle and maintenance
- [x] Iteration 23: Final review of all 7 sections
- [x] Iteration 24: Create research document (21_wopr.md)

---

## Research Notes

**Quick Assessment:**
- Existing data: Check for targets and air_yards columns
- ESPN API: Targets available (Metric 1), air yards unknown
- Free alternatives: Pro Football Reference, Next Gen Stats, PlayerProfiler
- Historical: Depends on target + air yards availability
- Implementation: MEDIUM (calculation + dependency on two metrics)

**Key Dependencies:**
- Metric 1: Target Volume/Share (provides targets)
- Metric 13: Air Yards (provides air yards) - MEDIUM priority

Starting research...
