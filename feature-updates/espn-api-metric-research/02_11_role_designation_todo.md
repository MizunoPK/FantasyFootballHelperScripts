# ESPN API Metric Research - Phase 2.11: Role Designation (RB Workload)

**Sub-Feature:** Metric 49 - Role Designation (RB Workload) Research
**Created:** 2025-12-20
**Status:** Complete

---

## Purpose

Research Metric 49 (Role Designation - RB-specific) to determine data availability for:
- RB's role classification (workhorse, lead back, committee, backup)
- Based on snap count % + carry/target share
- Predicts RB volume and consistency
- RB-specific metric (separates elite workload from committees)

**Why HIGH Priority:** RB role is best predictor of weekly fantasy floor/ceiling. Workhorses (70%+ snaps) have higher floors and more consistent scoring. Committee backs have volatility.

---

## Metric Details

**Metric Number:** 49
**Name:** Role Designation (RB Workload)
**Position Applicability:** RB (Running Back)
**Priority:** HIGH

**Description:** RB's role classification based on snap count % and touch share

**Why Important:**
- **Volume predictor:** Workhorses get 20+ touches, backups get <8
- **Consistency:** High snap % = consistent weekly usage
- **Committee differentiation:** Identifies shared backfields
- **Floor/ceiling:** Workhorses have higher floor, lower bust rate

**Calculation:**
```
Role Types:
Workhorse: 70%+ snaps, 20+ touches per game
Lead Back: 50-70% snaps, 15-20 touches
Committee: 30-50% snaps, 8-15 touches
Change-of-Pace: <30% snaps, <8 touches

Example:
Christian McCaffrey (SF):
- Snap %: 85%
- Touches: 25 per game
- Role: Workhorse (elite volume, every-week RB1)

Committee RB:
- Snap %: 45%
- Touches: 12 per game
- Role: Committee (volatile, RB2/RB3)
```

**Fantasy Impact:**
```
Workhorse (70%+ snaps): +15% boost (elite volume, consistent)
Lead Back (50-70%): +10% boost (strong volume)
Committee (30-50%): No adjustment (volatile)
Backup (<30%): -10% penalty (limited opportunity)

Correlation with fantasy points: ~0.75
High snap % + touches = Higher weekly floor
```

---

## Research Notes

**Quick Assessment:**
- Existing data: No (requires snap count + usage metrics)
- ESPN API: No (ESPN doesn't provide snap counts)
- Free alternatives: PlayerProfiler (snap % + opportunity share)
- Historical: Yes (PlayerProfiler archives)
- Implementation: MEDIUM (1-2 days scraping)

**Key Insight:**
Role designation requires **snap count + touch share**. PlayerProfiler shows both metrics directly.

Research complete - documented in 49_role_designation_rb_workload.md
