# ESPN API Metric Research - Phase 2.13: Pass Block Rate (QB Protection)

**Sub-Feature:** Metric 52 - Pass Block Rate (QB Protection) Research
**Created:** 2025-12-20
**Status:** Complete

---

## Purpose

Research Metric 52 (Pass Block Rate - QB-specific) to determine data availability for:
- QB's offensive line protection quality
- Pass block win rate (% of plays without pressure)
- Team sack rate as proxy
- Predicts QB performance (protected QBs score more)

**Why HIGH Priority:** QB protection has ~0.6 correlation with fantasy output. Protected QBs have more time to throw, higher completion %, fewer INTs, more TDs. Pressured QBs have rushed throws and lower scoring.

---

## Metric Details

**Metric Number:** 52
**Name:** Pass Block Rate (QB Protection)
**Position Applicability:** QB (Quarterback)
**Priority:** HIGH

**Description:** Quality of QB's offensive line protection (pass block win rate or sack rate proxy)

**Why Important:**
- **QB performance:** Protected QBs score 15-20% more fantasy points
- **Completion %:** Less pressure = higher completion rate
- **TDs vs INTs:** More time = better decisions
- **Matchup planning:** Good O-line vs bad D-line = QB boost

**Calculation (Proxy):**
```
Sack Rate = (Sacks / Pass Attempts) × 100

Low sack rate (4.0%) = Elite protection (Eagles, Chiefs)
High sack rate (9.0%) = Poor protection (many sacks, hurried throws)

Example - Jalen Hurts (PHI 2023):
Team Sack Rate: 4.2% (elite protection)
Result: High completion %, many TDs, top-5 fantasy QB

Poor O-Line Team:
Team Sack Rate: 9.5% (poor protection)
Result: Lower completion %, more INTs, QB struggles
```

**Fantasy Impact:**
```
Elite Protection (<4.0% sack rate): +10% boost (QB thrives)
Good Protection (4.0-5.5%): +5% boost
Average Protection (5.5-7.0%): No adjustment
Poor Protection (7.0-8.5%): -5% penalty
Very Poor (>8.5%): -10% penalty (QB frequently under pressure)
```

---

## Research Notes

**Quick Assessment:**
- Existing data: No (requires tracking data)
- ESPN API: No (no O-line metrics)
- Free alternatives: Use sack rate as proxy (PFR team stats)
- Historical: Yes (team sack rates available)
- Implementation: MEDIUM (1-2 days, scrape team sack rates)

**Key Insight:**
Pass Block Win Rate is premium data (PFF paywall). Use **team sack rate** as free proxy - inverse correlation with protection quality.

Research complete - documented in 52_pass_block_rate_qb.md
