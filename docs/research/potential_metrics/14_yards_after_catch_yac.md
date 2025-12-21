# Metric 14: Yards After Catch (YAC)

**Position Applicability:** WR, TE, RB
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires Next Gen Stats tracking

**Details:**

YAC requires tracking yards gained after reception (not available in basic stats).

**Formula:**
```
YAC per Reception = Total YAC / Total Receptions

High YAC WR (Deebo Samuel): 7.5 YAC/rec (run after catch ability)
Low YAC WR (possession receiver): 3.2 YAC/rec (catches and falls)
```

**Conclusion:** Not in existing data. Requires NGS tracking.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

---

## 3. Free Alternative Sources

### Source 1: Next Gen Stats

- URL: `https://nextgenstats.nfl.com/stats/receiving`
- Data: YAC, expected YAC (xYAC)
- Free: ✅ Unlimited
- Quality: **Excellent**

### Source 2: PlayerProfiler

- URL: `https://www.playerprofiler.com/nfl/`
- Data: YAC, YAC per reception
- Free: ✅ Unlimited

**Recommended:** **Next Gen Stats** or **PlayerProfiler**

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High
**Historical:** ⚠️ Partial (PlayerProfiler better archives)
**Predictive:** ✅ Yes

---

## 6. Implementation Complexity

**Difficulty:** Medium
**Effort:** 1-2 days

**Multiplier:**
```python
def get_yac_multiplier(yac_per_rec: float) -> float:
    if yac_per_rec >= 6.5:
        return 1.08  # Elite YAC ability
    elif yac_per_rec >= 5.0:
        return 1.04
    else:
        return 1.00
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - Medium value

**Value:** ⭐⭐⭐ (Medium)
**Feasibility:** ⭐⭐⭐ (Medium)
**Historical:** ⭐⭐⭐ (Good)

**Timeline:** 1-2 days

---

*Research conducted: 2025-12-20*
