# ESPN API Metric Research - Phase 2.12: Receiving Share (RB)

**Sub-Feature:** Metric 50 - Receiving Share (RB) Research
**Created:** 2025-12-20
**Status:** Complete

---

## Purpose

Research Metric 50 (Receiving Share - RB-specific) to determine data availability for:
- RB's share of team targets/receptions
- PPR league differentiator (receiving RBs vs rushing-only RBs)
- Target share % (RB targets / team pass attempts)

**Why HIGH Priority:** In PPR leagues, receiving RBs significantly outscore rushing-only RBs. 1 point per reception means target share is critical for PPR value. Elite receiving RBs (Ekeler, CMC) have 15%+ target share.

---

## Metric Details

**Metric Number:** 50
**Name:** Receiving Share (RB)
**Position Applicability:** RB (Running Back)
**Priority:** HIGH

**Description:** RB's percentage of team targets/passing attempts

**Calculation:**
```
RB Target Share = (RB Targets / Team Passing Attempts) × 100

Example - Austin Ekeler (2022 LAC):
- RB Targets: 108
- Team Pass Attempts: ~550
- Target Share: 108/550 = 19.6% (elite receiving RB, PPR gold)

Traditional RB:
- RB Targets: 30
- Team Pass Attempts: ~550
- Target Share: 30/550 = 5.5% (limited receiving, lower PPR value)
```

**Fantasy Impact (PPR):**
```
Elite Receiving RB (15%+ share): +15% boost (PPR league winner)
Strong Receiving (10-15%): +10% boost (PPR advantage)
Moderate Receiving (7-10%): +5% boost (PPR viable)
Limited Receiving (<7%): No adjustment (standard scoring RB)

In 0.5 PPR: Use half the multiplier
In standard: No adjustment (receiving less valuable)
```

---

## Research Notes

**Quick Assessment:**
- Existing data: YES (Metric 1 has targets, team stats available)
- ESPN API: YES (targets + team pass attempts)
- Implementation: VERY EASY (1-2 hours, calculation only)
- Historical: YES (perfect - already have target data)

**Key Insight:**
Can leverage Metric 1 (Target Volume) which already provides RB targets. Just need team passing attempts (available in team stats).

Research complete - documented in 50_receiving_share_rb.md
