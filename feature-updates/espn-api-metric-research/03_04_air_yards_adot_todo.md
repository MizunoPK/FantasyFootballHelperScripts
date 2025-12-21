# ESPN API Metric Research - Phase 3.04: Air Yards (aDOT)

**Sub-Feature:** Metric 13 - Air Yards (aDOT) Research
**Created:** 2025-12-20
**Status:** Complete

---

## Purpose

Research Metric 13 (Air Yards / aDOT - WR/TE) to determine data availability for:
- Average depth of target (aDOT)
- Total air yards (distance ball travels in air)
- Player profiling: deep threat vs short-area receiver
- Related to WOPR (Metric 21 uses air yards share)

**Why MEDIUM Priority:** Useful for player profiling (deep threats vs volume receivers). Already captured in WOPR metric but aDOT provides additional context.

---

## Metric Details

**Metric Number:** 13
**Name:** Air Yards (aDOT)
**Position Applicability:** WR, TE
**Priority:** MEDIUM

**Description:** Average distance ball travels in air on targets (Average Depth of Target)

**Why Important:**
- **Player profiling:** High aDOT = deep threat, low aDOT = volume receiver
- **Upside indicator:** Deep targets = big play potential
- **Consistency:** Short targets = stable floor, consistent
- **WOPR component:** Air yards share used in WOPR (Metric 21)

**Calculation:**
```
aDOT = Total Air Yards / Total Targets

Example - Deep Threat WR (Tyreek Hill):
Total Air Yards: 1,200 yards
Total Targets: 80
aDOT: 1,200 / 80 = 15.0 yards (deep threat, big plays)

Slot WR (Julian Edelman):
Total Air Yards: 600 yards
Total Targets: 80
aDOT: 600 / 80 = 7.5 yards (short area, volume)
```

**Fantasy Impact:**
```
High aDOT (12+ yards): +5% boost (big play upside, boom/bust)
Moderate aDOT (8-12 yards): No adjustment (balanced)
Low aDOT (<8 yards): No adjustment (volume-based, consistent)

Note: Value already captured in WOPR metric (air yards share)
```

---

## Research Notes

**Quick Assessment:**
- Existing data: No (requires NGS tracking)
- ESPN API: No
- Free alternatives: Next Gen Stats, PlayerProfiler
- Historical: Partial (PlayerProfiler better than NGS)
- Implementation: MEDIUM (1-2 days, likely same as WOPR source)

**Key Insight:**
Air yards share already in WOPR (Metric 21). aDOT adds player profiling but not critical for scoring adjustments.

Research complete - documented in 13_air_yards_adot.md
