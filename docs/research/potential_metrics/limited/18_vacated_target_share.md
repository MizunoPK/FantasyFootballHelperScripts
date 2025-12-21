# Metric 18: Vacated Target Share

**Position Applicability:** WR, TE
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires preseason analysis of departed players

**Details:**

Vacated Target Share = Targets from departed players (free agents, trades, retirements)

**Example:**
```
Team loses WR1 who had 150 targets last year
Remaining WRs compete for those 150 vacated targets
Players on that team get opportunity boost
```

**Conclusion:** Requires offseason/preseason analysis, not real-time weekly data

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

---

## 3. Free Alternative Sources

### Manual Analysis Required

- Identify departed players (free agency, trades)
- Calculate their previous season targets
- Distribute to remaining players (estimation)

**Note:** This is primarily a **preseason/draft** metric, not in-season weekly adjustment

---

## 4-5. Data Quality & Historical Availability

**Reliability:** Medium (requires estimation)
**Historical:** ⚠️ Limited (preseason only)
**Predictive:** ⚠️ Preseason only (not weekly)

---

## 6. Implementation Complexity

**Difficulty:** Medium-Hard
**Effort:** 2-3 days (preseason analysis, not weekly)

---

## 7. Recommendation

**Should we pursue this metric?**

- [ ] **DEFER** - Preseason metric, not weekly

**Value:** ⭐⭐ (Low for in-season weekly projections)
**Feasibility:** ⭐⭐ (Medium-Hard, preseason only)
**Historical:** ⭐⭐ (Limited - preseason snapshots)

**Rationale:** Vacated targets are useful for **preseason draft prep**, not weekly in-season adjustments. Our system focuses on weekly projections.

**Alternative:** Covered by Metric 5 (Teammate Injury Impact) for in-season vacated targets

---

*Research conducted: 2025-12-20*
