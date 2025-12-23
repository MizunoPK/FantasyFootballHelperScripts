# ESPN API Metric Research - Phase 2.10: Goal-Line Role (RB)

**Sub-Feature:** Metric 46 - Goal-Line Role (RB) Research
**Created:** 2025-12-20
**Status:** In Progress

---

## Purpose

Research Metric 46 (Goal-Line Role - RB-specific) to determine data availability for:
- RB's role in goal-line/red zone rushing situations
- Percentage of goal-line carries (inside 5-yard line)
- Predicts RB touchdown opportunity
- RB-specific metric (separates TD-dependent RBs from yardage RBs)

**Why HIGH Priority:** Touchdowns are highest-value fantasy scoring events (6 points in standard). Goal-line role predicts TD opportunity better than total carries. Two RBs can have same yardage but different TDs based on goal-line usage.

---

## Metric Details

**Metric Number:** 46
**Name:** Goal-Line Role (RB)
**Position Applicability:** RB (Running Back)
**Priority:** HIGH

**Description:** RB's share of team's rushing attempts inside the 5-yard line (goal-line carries)

**Why Important:**
- **TD predictor:** Goal-line carries = TD opportunities
- **Role clarity:** Separates TD-dependent RBs from yardage RBs
- **Committee differentiation:** In RB committees, one RB often gets goal-line work
- **High variance:** Goal-line role can change week-to-week (injuries, matchups)

**Calculation:**
```
Goal-Line Carry Share = (RB Goal-Line Carries / Team Goal-Line Carries) × 100

Where:
- Goal-Line Carries = Rushing attempts inside opponent's 5-yard line
- Team Goal-Line Carries = Total team rushing attempts inside 5-yard line

Example:
Christian McCaffrey (SF):
- Goal-Line Carries: 12
- Team Goal-Line Carries: 15
- Goal-Line Share: 12/15 = 80% (primary goal-line back)

Committee RB:
- Goal-Line Carries: 3
- Team Goal-Line Carries: 15
- Goal-Line Share: 3/15 = 20% (limited goal-line role)
```

**Fantasy Impact:**
```
Elite Goal-Line Role (75%+): +15% boost (primary TD scorer)
Strong Goal-Line Role (50-75%): +10% boost (significant TD opportunities)
Shared Goal-Line Role (25-50%): +5% boost (occasional TDs)
Limited Goal-Line Role (<25%): No adjustment (TD-dependent on long runs)

TD correlation:
Goal-line carry share has ~0.7 correlation with rushing TDs
High goal-line share = More TDs = Higher fantasy ceiling
```

---

## Research Notes

**Quick Assessment:**
- Existing data: Unlikely (advanced situational stat)
- ESPN API: Unlikely (not in standard stats)
- Free alternatives: Pro Football Reference (situational splits), PlayerProfiler
- Historical: Likely available (PFR has situational stats)
- Implementation: MEDIUM (scraping situational stats or estimation)

**Key Insight:**
Goal-line role is **situational stat** (requires play-by-play or situational splits). Options:
1. Scrape PFR situational stats (inside 5-yard line)
2. Scrape PlayerProfiler if available
3. Estimate from red zone carries + TD rate (less accurate)

Starting research...
