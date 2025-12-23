# ESPN API Metric Research - Phase 2.14: Pressure Rate (QB)

**Sub-Feature:** Metric 53 - Pressure Rate (QB) Research
**Created:** 2025-12-20
**Status:** Complete

---

## Purpose

Research Metric 53 (Pressure Rate - QB-specific) to determine data availability for:
- QB's rate of being pressured (pressures per dropback)
- QB performance under pressure
- Differentiates elite QBs (thrive under pressure) from average
- Matchup factor (good D-line = more pressure)

**Why HIGH Priority:** QB pressure significantly impacts fantasy output. Most QBs struggle under pressure (lower completion %, more INTs). Elite QBs like Mahomes/Allen still produce despite pressure. Critical for matchup planning.

---

## Metric Details

**Metric Number:** 53
**Name:** Pressure Rate (QB)
**Position Applicability:** QB (Quarterback)
**Priority:** HIGH

**Description:** Percentage of QB dropbacks where QB is pressured by defense

**Why Important:**
- **Performance split:** QBs score ~30% less under pressure
- **Elite differentiation:** Mahomes/Allen thrive, others struggle
- **Matchup planning:** Good D-line vs poor O-line = high pressure
- **INT risk:** Pressure increases INT rate by ~50%

**Calculation:**
```
Pressure Rate = (Pressures Allowed / Dropbacks) × 100

Example - Patrick Mahomes (KC):
Pressure Rate: 28% (frequently pressured)
Performance Under Pressure: Elite (still completes 65%, low INTs)
Result: Top fantasy QB despite high pressure

Average QB:
Pressure Rate: 25%
Performance Under Pressure: Struggles (completion % drops to 50%, more INTs)
Result: Lower fantasy output under pressure
```

**Fantasy Impact:**
```
Elite QB Under Pressure (Mahomes, Allen): +5% boost (thrives despite pressure)
Average QB, Low Pressure (<25%): No adjustment (clean pocket)
Average QB, Moderate Pressure (25-30%): -5% penalty
Average QB, High Pressure (>30%): -10% penalty (frequent mistakes)
```

---

## Research Notes

**Quick Assessment:**
- Existing data: No (requires tracking data)
- ESPN API: No
- Free alternatives: Next Gen Stats (pressure rate, time to throw)
- Historical: Partial (NGS historical availability varies)
- Implementation: MEDIUM (1-2 days, scrape NGS)

**Key Insight:**
Next Gen Stats provides pressure rate and performance under pressure directly. Free and official NFL tracking data.

Research complete - documented in 53_pressure_rate_qb.md
