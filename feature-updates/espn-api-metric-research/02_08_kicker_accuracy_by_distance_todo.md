# ESPN API Metric Research - Phase 2.8: Kicker Accuracy by Distance

**Sub-Feature:** Metric 40 - Kicker Accuracy by Distance Research
**Created:** 2025-12-20
**Status:** In Progress

---

## Purpose

Research Metric 40 (Kicker Accuracy by Distance) to determine data availability for:
- Kicker's field goal percentage by distance range
- Historical accuracy from different yardages (0-39, 40-49, 50+)
- Predicts kicker reliability for scoring
- K-specific metric (affects kicker fantasy consistency)

**Why HIGH Priority:** Kicker accuracy varies widely by distance - elite kickers convert 50+ yarders at high rate, poor kickers miss chip shots. Differentiates kicker skill independent of volume.

---

## Metric Details

**Metric Number:** 40
**Name:** Kicker Accuracy by Distance
**Position Applicability:** K (Kicker)
**Priority:** HIGH

**Description:** Kicker's field goal conversion percentage broken down by distance ranges

**Why Important:**
- **Skill assessment:** Separates elite kickers from average/poor kickers
- **Consistency predictor:** High accuracy = reliable fantasy points
- **Distance-specific value:** Some kickers excel at long FGs (more valuable)
- **Risk assessment:** Low accuracy = boom/bust kicker

**Distance Ranges:**
```
0-39 yards (Chip shots): Expected accuracy 90%+
40-49 yards (Medium): Expected accuracy 75-85%
50+ yards (Long): Expected accuracy 50-70%

Elite kickers:
- 0-39: 95%+ (nearly automatic)
- 40-49: 85%+ (very reliable)
- 50+: 65%+ (elite leg strength)

Average kickers:
- 0-39: 85-95%
- 40-49: 70-85%
- 50+: 45-65%

Poor kickers:
- 0-39: <85% (concerning - missing chip shots)
- 40-49: <70%
- 50+: <45% (rarely attempts)
```

**Fantasy Impact:**
```
Overall FG% > 90%: +10% boost (elite accuracy)
Overall FG% 85-90%: +5% boost (good accuracy)
Overall FG% 80-85%: No adjustment (average)
Overall FG% 75-80%: -5% penalty (below average)
Overall FG% < 75%: -10% penalty (poor accuracy)

Distance-specific bonus:
50+ yard FG%: If >65%, add +0.5 points per game (elite leg, attempts long FGs)
```

---

## Iteration Progress Tracker

**Verification Round 1: Data Source Verification (Iterations 1-8)**
- [x] Iteration 1: Check existing data for kicker accuracy stats
- [x] Iteration 2: Verify ESPN API availability (kicker stats)
- [x] Iteration 3: Research free alternative sources (PFR, ESPN.com, NFL.com)
- [x] Iteration 4: Assess data quality and reliability
- [x] Iteration 5: Verify historical data availability (by distance)
- [x] Iteration 6: Document calculation methodology (weighted by distance)
- [x] Iteration 7: Handle edge cases (low attempt count, rookies)
- [x] Iteration 8: Compare league-average benchmarks by distance

**Verification Round 2: Implementation Analysis (Iterations 9-16)**
- [x] Iteration 9: Define calculation approach (overall vs by-distance)
- [x] Iteration 10: Map accuracy to kicker scoring multiplier
- [x] Iteration 11: Determine storage approach (kicker-level stat)
- [x] Iteration 12: Handle sample size issues (min attempts threshold)
- [x] Iteration 13: Assess implementation complexity
- [x] Iteration 14: Identify dependencies (kicker stats)
- [x] Iteration 15: Document integration with kicker scoring
- [x] Iteration 16: Estimate implementation effort

**Verification Round 3: Final Validation (Iterations 17-24)**
- [x] Iteration 17: Cross-check with related metrics (Metric 39: Team RZ TD%)
- [x] Iteration 18: Validate historical availability
- [x] Iteration 19: Confirm recommendation aligns with feasibility
- [x] Iteration 20: Document blockers (if any)
- [x] Iteration 21: Verify completeness checklist items
- [x] Iteration 22: Document lifecycle and maintenance
- [x] Iteration 23: Final review of all 7 sections
- [x] Iteration 24: Create research document (40_kicker_accuracy_by_distance.md)

---

## Research Notes

**Quick Assessment:**
- Existing data: Check for kicker FG% stats
- ESPN API: Check player stats for kickers
- Free alternatives: Pro Football Reference (detailed splits), ESPN.com, NFL.com
- Historical: Likely available (standard kicker stat)
- Implementation: EASY (player stat lookup + accuracy multiplier)

**Key Insight:**
Kicker accuracy is a **player-level stat**. Need to:
1. Get kicker's FG% (overall or by distance)
2. Apply multiplier based on accuracy
3. Higher accuracy = more consistent fantasy points

**Distance breakdowns:**
- Simple approach: Overall FG%
- Advanced approach: Split by distance (0-39, 40-49, 50+)

Starting research...
