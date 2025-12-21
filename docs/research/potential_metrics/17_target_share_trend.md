# Metric 17: Target Share Trend

**Position Applicability:** WR, TE, RB
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [x] Yes - Can calculate from Metric 1 (Target Volume)

**Details:**

Target Share Trend = Change in target share over recent weeks (e.g., weeks N-3 to N vs weeks N-6 to N-4)

**Formula:**
```
Trend = Recent Target Share - Earlier Target Share

Positive trend: Player getting more involved
Negative trend: Player usage declining
```

**Conclusion:** Can calculate from existing Metric 1 (Targets)

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] Yes - Via Metric 1 (Targets) calculation

---

## 3. Free Alternative Sources

Use existing Metric 1 data (Targets)

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High (derived from Metric 1)
**Historical:** ✅ Yes (perfect - from Metric 1)
**Predictive:** ✅ Yes

---

## 6. Implementation Complexity

**Difficulty:** Easy
**Effort:** 1-2 hours (calculation from Metric 1)

**Multiplier:**
```python
def get_target_trend_multiplier(trend_pct_change: float) -> float:
    if trend_pct_change >= 20.0:
        return 1.08  # Rising role
    elif trend_pct_change <= -20.0:
        return 0.92  # Declining role
    else:
        return 1.00  # Stable
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - Easy implementation, derived from existing data

**Value:** ⭐⭐⭐ (Medium - trend analysis useful)
**Feasibility:** ⭐⭐⭐⭐⭐ (Very easy - calculation only)
**Historical:** ⭐⭐⭐⭐⭐ (Perfect - from Metric 1)

**Timeline:** 1-2 hours (calculation from existing Metric 1)

---

*Research conducted: 2025-12-20*
