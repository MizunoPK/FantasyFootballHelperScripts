# ESPN API Metric Research - Phase 3.03: Red Zone Opportunity

**Sub-Feature:** Metric 7 - Red Zone Opportunity Research
**Created:** 2025-12-20
**Status:** Complete

---

## Purpose

Research Metric 7 (Red Zone Opportunity - ALL positions) to determine data availability for:
- Player's touches/targets inside the 20-yard line
- Red zone opportunity share (player RZ touches / team RZ touches)
- Best predictor of touchdown scoring
- All-position metric (RB carries, WR/TE targets in RZ)

**Why MEDIUM Priority:** Red zone touches are the best TD predictor. Players with high RZ involvement have higher TD rates and fantasy ceilings.

---

## Metric Details

**Metric Number:** 7
**Name:** Red Zone Opportunity
**Position Applicability:** ALL
**Priority:** MEDIUM

**Description:** Player's share of team's red zone opportunities (targets/carries inside 20-yard line)

**Why Important:**
- **TD predictor:** RZ touches = TD opportunities
- **Volume matters:** High RZ share = more TD chances
- **Better than total touches:** RZ efficiency >> overall efficiency
- **All positions:** RBs (carries), WRs/TEs (targets), QBs (attempts)

**Calculation:**
```
RZ Opportunity Share = (Player RZ Touches / Team RZ Touches) × 100

Example - Davante Adams (WR):
Red Zone Targets: 25
Team Red Zone Plays: 80
RZ Share: 25/80 = 31% (elite RZ role, high TDs expected)

Low RZ Role WR:
Red Zone Targets: 8
Team Red Zone Plays: 80
RZ Share: 8/80 = 10% (limited TD opportunity)
```

**Fantasy Impact:**
```
Elite RZ Role (25%+ share): +15% boost (many TDs expected)
Strong RZ Role (15-25%): +10% boost (significant TD opportunity)
Moderate RZ Role (10-15%): +5% boost (occasional TDs)
Limited RZ Role (<10%): No adjustment (TD-dependent on big plays)
```

---

## Research Notes

**Quick Assessment:**
- Existing data: No (requires situational stats)
- ESPN API: No
- Free alternatives: PlayerProfiler, Pro Football Reference (splits)
- Historical: Yes (both sources have archives)
- Implementation: MEDIUM (1-2 days scraping)

**Key Insight:**
Similar to Metric 46 (Goal-Line Role for RBs) but broader scope:
- Metric 46: Inside 5-yard line (goal-line)
- Metric 7: Inside 20-yard line (entire red zone)
Both are TD predictors, red zone is broader.

Research complete - documented in 07_red_zone_opportunity.md
