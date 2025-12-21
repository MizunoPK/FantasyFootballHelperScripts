# ESPN API Metric Research - Phase 3.02: Opponent Secondary Details

**Sub-Feature:** Metric 6 - Opponent Secondary Details Research
**Created:** 2025-12-20
**Status:** Complete

---

## Purpose

Research Metric 6 (Opponent Secondary Details - WR/TE) to determine data availability for:
- Quality of opponent's defensive backs (CB1, CB2, slot CB, safeties)
- WR/TE matchup advantages/disadvantages
- Specific coverage matchups (WR1 vs CB1)

**Why MEDIUM Priority:** Matchup quality affects WR/TE performance significantly. Elite CBs can shut down WR1s. Weak secondaries create boom weeks for pass catchers.

---

## Metric Details

**Metric Number:** 6
**Name:** Opponent Secondary Details
**Position Applicability:** WR, TE
**Priority:** MEDIUM

**Description:** Quality of opponent's defensive backs and coverage units

**Why Important:**
- **Elite CB shutdown:** Jalen Ramsey, Patrick Surtain can limit WR1s
- **Weak secondary:** Poor pass defenses create WR/TE opportunities
- **Slot vs boundary:** Slot receivers face different CBs than boundary
- **TE coverage:** Weak safety coverage boosts TE production

**Calculation (Ideal):**
```
WR1 vs Elite CB1 (Top 5 ranked): -10% penalty
WR2 vs Weak CB2 (Bottom 10): +10% boost
Slot WR vs Poor Slot CB: +15% boost
TE vs Weak Safety coverage: +12% boost

Example - Davante Adams vs Jalen Ramsey:
Ramsey shadows Adams, limits targets/efficiency
Apply -10% penalty
```

**Proxy Approach (Free Data):**
```
Use team pass defense ranking instead of CB-specific:

Opponent ranked 1-10 (elite pass D): -10% penalty for WR/TE
Opponent ranked 11-22 (average): No adjustment
Opponent ranked 23-32 (poor pass D): +10% boost for WR/TE
```

---

## Research Notes

**Quick Assessment:**
- Existing data: No (requires defensive player tracking)
- ESPN API: No
- Free alternatives: Team pass defense proxy (PFR)
- Historical: Yes (team pass defense stats)
- Implementation: MEDIUM (1-2 days, team proxy approach)

**Key Insight:**
CB-specific data is premium (PFF paywall). Use **team pass defense rankings** as free proxy - less granular but still predictive.

Research complete - documented in 06_opponent_secondary_details.md
