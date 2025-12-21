# LIMITED Historical Data Availability (7 metrics)

Metrics in this folder have **limited or no historical data availability** due to premium paywalls, not being applicable in-season, or being redundant with other metrics.

## Characteristics:
- ❌ **Premium data required** (PFF, ESPN Analytics paywall)
- ❌ **Not applicable in-season** (draft/preseason only)
- ❌ **Redundant** (already covered by other metrics)
- ⚠️ **Limited historical coverage**

## Implementation Priority: **DEFER**
These metrics should be deferred or skipped entirely.

---

## Metrics by Category

### Premium Data Required (3 metrics)
**Recommendation:** DEFER - Not worth paywall cost

- **M20: Success Rate** (ALL positions)
  - Source: PFF Premium ($200+/year)
  - Alternative: None (proprietary calculation)
  - Value: Low (edge case)

- **M23: EPA (Expected Points Added)** (ALL positions)
  - Source: PFF/ESPN Analytics Premium
  - Alternative: M22 (xFP) provides similar insight
  - Value: Medium, but M22 covers it

- **M44: EPA Per Target (TE)**
  - Source: PFF Premium
  - Alternative: M22 (xFP) + M42 (Route %) + M43 (RZ efficiency)
  - Value: Low (overlap with M22, M42, M43)

### Not Applicable In-Season (2 metrics)
**Recommendation:** DEFER - Preseason/draft use only

- **M18: Vacated Target Share** (WR, TE)
  - When: Preseason analysis only
  - Why: Tracks departed players' targets (offseason moves)
  - Alternative: M05 (Teammate Injury Impact) for in-season
  - Value: Useful for drafts, not weekly projections

- **M38: Dominator Rating** (WR, TE rookies)
  - When: Draft evaluation only
  - Why: College production metric (not NFL)
  - Alternative: N/A (not applicable in-season)
  - Value: Draft tool, zero in-season value

### Redundant (2 metrics)
**Recommendation:** DEFER - Already covered by other metrics

- **M03: QB-Specific Weather Sensitivity** (QB)
  - Overlap: M04 (Vegas Lines) already factors weather
  - Implementation: Hard (5+ days, manual analysis)
  - Value: Low (small edge case, questionable reliability)
  - Historical: Poor (small sample sizes per QB)

- **M47: TD Equity (RB)**
  - Overlap: M46 (Goal-Line Role), M22 (xFP), M07 (Red Zone Opp)
  - Implementation: Medium-Hard (2-3 days modeling)
  - Value: Low (redundant)
  - Alternative: Use M46 + M22 + M07 combination

---

## Why These Are Deferred

### Premium Data (M20, M23, M44)
- **Cost:** $200-500+/year for PFF/ESPN Analytics
- **ROI:** Low value for cost
- **Alternatives:** Free metrics provide similar insight
  - M22 (xFP) replaces M23 (EPA)
  - M22 + M42 + M43 replace M44 (EPA per Target)

### Preseason Only (M18, M38)
- **Timing:** Not applicable during weekly in-season projections
- **Use Case:** Draft prep only
- **Alternatives:**
  - M05 (Teammate Injury) handles in-season target redistribution
  - NFL stats replace college metrics

### Edge Cases (M03, M47)
- **M03 (Weather):** Already captured by M04 (Vegas Lines)
- **M47 (TD Equity):** Redundant with M46, M22, M07 combination

---

## Historical Data Confidence: 0-30%

- **M03, M18, M38, M47:** No meaningful historical data for in-season use
- **M20, M23, M44:** Behind paywall, not accessible

**Recommended Action:** Skip implementation unless specific use case emerges or premium data becomes available.

---

## Implementation Effort (If Pursued)

**DO NOT IMPLEMENT** - These metrics are intentionally deferred:

- M03: 5+ days (manual analysis, questionable value)
- M18: N/A (preseason only)
- M20: 3+ days (if premium data obtained)
- M23: 3+ days (if premium data obtained)
- M38: N/A (draft only)
- M44: 3+ days (if premium data obtained)
- M47: 2-3 days (but redundant)

**Total Effort Saved:** 20+ days by deferring these metrics

---

*Last Updated: 2025-12-20*
