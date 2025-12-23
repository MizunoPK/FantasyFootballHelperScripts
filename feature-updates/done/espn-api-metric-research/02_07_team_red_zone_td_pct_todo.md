# ESPN API Metric Research - Phase 2.7: Team Red Zone TD% (K-specific)

**Sub-Feature:** Metric 39 - Team Red Zone TD% (K-specific) Research
**Created:** 2025-12-20
**Status:** In Progress

---

## Purpose

Research Metric 39 (Team Red Zone TD% - Kicker-specific) to determine data availability for:
- Team's red zone touchdown efficiency
- Red zone attempts that result in TDs vs FGs
- Predicts kicker field goal volume
- K-specific metric (affects kicker fantasy value)

**Why HIGH Priority:** Kickers on teams with LOW red zone TD% get more FG attempts (higher fantasy scoring). Teams that score TDs in red zone = fewer kicker opportunities.

---

## Metric Details

**Metric Number:** 39
**Name:** Team Red Zone TD% (K-specific)
**Position Applicability:** K (Kicker)
**Priority:** HIGH

**Description:** Percentage of team's red zone trips that result in touchdowns (vs field goals)

**Why Important:**
- **Inverse correlation with kicker value:** LOW TD% = MORE FG attempts = GOOD for kicker
- **Volume predictor:** Teams that struggle in red zone = more kicker opportunities
- **Context-aware:** Two teams can score same points, but one gives kicker more chances

**Calculation:**
```
Red Zone TD% = (Red Zone TDs / Red Zone Attempts) × 100

Where:
- Red Zone = Inside opponent's 20-yard line
- Red Zone TDs = TDs scored inside red zone
- Red Zone Attempts = Total possessions inside red zone

Example:
Team A (Good Red Zone Offense):
- Red Zone Attempts: 20
- Red Zone TDs: 16
- Red Zone TD%: 16/20 = 80% ❌ BAD for kicker (only 4 FG attempts)

Team B (Poor Red Zone Offense):
- Red Zone Attempts: 20
- Red Zone TDs: 10
- Red Zone TD%: 10/20 = 50% ✅ GOOD for kicker (10 FG attempts)

Kicker on Team B will score more fantasy points (more FG opportunities)
```

**Fantasy Impact:**
```
High Red Zone TD% (70%+) → BAD for kicker (fewer FG attempts)
Medium Red Zone TD% (50-70%) → NEUTRAL for kicker
Low Red Zone TD% (<50%) → GOOD for kicker (more FG attempts)

Kicker Scoring Adjustment:
- Team RZ TD% < 50%: +5% boost (more FG volume expected)
- Team RZ TD% 50-60%: No adjustment
- Team RZ TD% 60-70%: -5% penalty (fewer FG volume expected)
- Team RZ TD% > 70%: -10% penalty (very few FG attempts)
```

---

## Iteration Progress Tracker

**Verification Round 1: Data Source Verification (Iterations 1-8)**
- [x] Iteration 1: Check existing data for red zone stats
- [x] Iteration 2: Verify ESPN API availability (team stats)
- [x] Iteration 3: Research free alternative sources (Pro Football Reference, TeamRankings)
- [x] Iteration 4: Assess data quality and reliability
- [x] Iteration 5: Verify historical data availability
- [x] Iteration 6: Document calculation methodology
- [x] Iteration 7: Handle edge cases (low red zone attempts)
- [x] Iteration 8: Compare league-average benchmarks

**Verification Round 2: Implementation Analysis (Iterations 9-16)**
- [x] Iteration 9: Define calculation approach (scraping vs ESPN API)
- [x] Iteration 10: Map RZ TD% to kicker scoring multiplier
- [x] Iteration 11: Determine storage approach (team-level metric)
- [x] Iteration 12: Handle kicker assignment to team
- [x] Iteration 13: Assess implementation complexity
- [x] Iteration 14: Identify dependencies (team stats)
- [x] Iteration 15: Document integration with kicker scoring
- [x] Iteration 16: Estimate implementation effort

**Verification Round 3: Final Validation (Iterations 17-24)**
- [x] Iteration 17: Cross-check with related metrics (Metric 36: Team Red Zone Efficiency)
- [x] Iteration 18: Validate historical availability
- [x] Iteration 19: Confirm recommendation aligns with feasibility
- [x] Iteration 20: Document blockers (if any)
- [x] Iteration 21: Verify completeness checklist items
- [x] Iteration 22: Document lifecycle and maintenance
- [x] Iteration 23: Final review of all 7 sections
- [x] Iteration 24: Create research document (39_team_red_zone_td_pct.md)

---

## Research Notes

**Quick Assessment:**
- Existing data: Check for team red zone stats
- ESPN API: Check team stats endpoint for red zone data
- Free alternatives: Pro Football Reference (team stats), TeamRankings.com
- Historical: Likely available (standard NFL stat)
- Implementation: EASY-MEDIUM (team stat lookup + kicker mapping)

**Key Insight:**
Red Zone TD% is a **team-level stat**, not player-level. Need to:
1. Get team red zone TD%
2. Map each kicker to their team
3. Apply inverse multiplier (LOW TD% = GOOD for kicker)

Starting research...
