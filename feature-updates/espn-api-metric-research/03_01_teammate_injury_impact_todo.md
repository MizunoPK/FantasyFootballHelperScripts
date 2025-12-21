# ESPN API Metric Research - Phase 3.01: Teammate Injury Impact

**Sub-Feature:** Metric 5 - Teammate Injury Impact Research
**Created:** 2025-12-20
**Status:** Complete

---

## Purpose

Research Metric 5 (Teammate Injury Impact - ALL positions) to determine data availability for:
- Impact on player when key teammates are injured
- Target/usage redistribution when WR1/RB1/TE1 miss games
- Position-specific opportunity shifts
- Predicts usage spikes for backup players

**Why MEDIUM Priority:** Significant fantasy impact when stars miss time, but complex to model accurately. Backup RBs/WRs can become weekly starters.

---

## Metric Details

**Metric Number:** 5
**Name:** Teammate Injury Impact
**Position Applicability:** ALL
**Priority:** MEDIUM

**Description:** Boost/adjustment when key teammates are injured and usage redistributes

**Why Important:**
- **Opportunity creation:** WR1 out → WR2/WR3 see +30% targets
- **Backup elevation:** RB1 out → RB2 becomes workhorse (+60% carries)
- **Weekly starters:** Players become must-starts when stars are out
- **Matchup leverage:** Injury creates immediate value shift

**Calculation:**
```
Impact depends on:
1. Which teammate is injured (WR1 vs WR3 has different impact)
2. Player's position relative to injured player
3. Historical usage redistribution patterns

Example - WR2 when WR1 is out:
Normal: 6 targets/game (WR1 gets 10 targets)
WR1 injured: 8-9 targets/game (+30-50% boost)

Example - Backup RB when RB1 is out:
Normal: 5 carries/game (RB1 gets 20 carries)
RB1 injured: 18-20 carries/game (+300% boost, workhorse role)
```

**Fantasy Impact:**
```
WR1 out → WR2/WR3: +15% boost (target redistribution)
RB1 out → RB2: +25% boost (becomes workhorse)
TE1 out → WRs: +8% boost (moderate redistribution)
No key injuries: No adjustment
```

---

## Research Notes

**Quick Assessment:**
- Existing data: No (requires injury tracking + modeling)
- ESPN API: Partial (injury status yes, impact modeling no)
- Free alternatives: ESPN injury report + historical usage modeling
- Historical: Partial (can build impact model from historical data)
- Implementation: HARD (3-5 days for full model, 1-2 days for simple version)

**Key Insight:**
High value but complex. Recommend **simple version first**: Flag if WR1/RB1/TE1 is out, apply flat boost to backups. Full position-specific modeling can come later.

Research complete - documented in 05_teammate_injury_impact.md
