# Metric 15: Snap Share Percentage

**Position Applicability:** ALL
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires snap count tracking

**Details:**

Snap Share = (Player Snaps / Team Offensive Snaps) × 100

High snap % indicates large role. Related to Metric 42 (Route % for TEs) and Metric 49 (RB Role).

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

---

## 3. Free Alternative Sources

### Source 1: Pro Football Reference

- URL: `https://www.pro-football-reference.com/`
- Data: Snap counts
- Free: ✅ Unlimited

### Source 2: PlayerProfiler

- URL: `https://www.playerprofiler.com/nfl/`
- Data: Snap %
- Free: ✅ Unlimited

**Recommended:** **PlayerProfiler** or **PFR**

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High
**Historical:** ✅ Yes
**Predictive:** ✅ Yes

---

## 6. Implementation Complexity

**Difficulty:** Medium
**Effort:** 1-2 days

**Multiplier:**
```python
def get_snap_share_multiplier(snap_pct: float) -> float:
    if snap_pct >= 80.0:
        return 1.10  # Bellcow role
    elif snap_pct >= 60.0:
        return 1.05
    else:
        return 1.00
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High value for all positions

**Value:** ⭐⭐⭐⭐ (High)
**Feasibility:** ⭐⭐⭐ (Medium)
**Historical:** ⭐⭐⭐⭐ (Good)

**Note:** Overlaps with Metric 42 (TE Route %) and Metric 49 (RB Role)

**Timeline:** 1-2 days

---

*Research conducted: 2025-12-20*
