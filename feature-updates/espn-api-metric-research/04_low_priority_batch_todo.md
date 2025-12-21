# ESPN API Metric Research - Phase 4: LOW Priority Batch (All 29 Metrics)

**Sub-Feature:** Metrics 3, 8-11, 20, 23-38, 44-45, 48, 55-58 Research
**Created:** 2025-12-20
**Status:** Complete

---

## Overview

Completed research for all 29 LOW priority metrics in systematic batch.

**Key Patterns:**
- **Easy (calculation):** 3, 8, 10, 11, 17, 19, 24, 34, 37, 45, 58 (11 metrics)
- **Medium (scraping):** 9, 25, 26, 27-33, 35, 36, 48, 55, 56, 57 (17 metrics)
- **Hard/Defer:** 20, 23, 38, 44, 47 (5 metrics - premium data or not applicable)

**Overlap/Dependencies:**
- M37 (Snap Share Trend) ← M15 (Snap Share)
- M45 (TE Role Security) ← M42 + M15
- M56 (WR RZ Involvement) ← M7 (RZ Opportunity)
- M58 (WR Total Opportunity) ← M1 (Targets)

**Recommendations:**
- **PURSUE:** 24 metrics (easy-medium implementation)
- **DEFER:** 5 metrics (premium data, preseason only, or redundant)

All research complete - documented in individual metric files.

---

## Summary by Category

### Easy Implementation (11 metrics)
- M3: QB Weather Sensitivity (defer - edge case)
- M8: Hot/Cold Streak (pursue - calculation)
- M10: Divisional Game (pursue - static mapping)
- M11: Primetime Game (pursue - time flag)
- M24: QB Rating (pursue - formula)
- M34: Team Plays/Game (pursue - scraping)
- M37: Snap Share Trend (pursue - from M15)
- M45: TE Role Security (pursue - from M42+M15)
- M58: WR Total Opportunity (pursue - from M1)

### Medium Implementation (17 metrics)
- M9: Team Pass Rate/Tempo (pursue)
- M25-33: NGS tracking metrics (batch scraping)
- M35: Neutral Script Pass Rate (pursue)
- M36: Team RZ Efficiency (pursue - overlap M39)
- M48: Yards Before Contact RB (pursue)
- M55-57: WR situational metrics (pursue)

### Defer/Premium (5 metrics)
- M20: Success Rate (premium)
- M23: EPA (premium)
- M38: Dominator Rating (draft only)
- M44: EPA per Target TE (premium, overlap M22)
- M47: TD Equity RB (redundant - covered by M22, M46, M7)

