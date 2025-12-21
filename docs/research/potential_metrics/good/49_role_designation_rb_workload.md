# Metric 49: Role Designation (RB Workload)

**Position Applicability:** RB (Running Back)
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires advanced tracking

**Details:**

Role Designation requires **snap count + carry/target share** to classify RB role.

**RB Role Types:**
```
Workhorse (70%+ snaps, 20+ touches): Elite volume, every-week starter
Lead Back (50-70% snaps, 15-20 touches): Strong volume, RB1/RB2
Committee (30-50% snaps, 8-15 touches): Volatile, RB2/RB3
Change-of-Pace (<30% snaps, <8 touches): Backup, rarely fantasy relevant
```

**Conclusion:** Not in existing data. Need snap count + usage metrics.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

ESPN doesn't provide snap count or role designation.

---

## 3. Free Alternative Sources

### Source 1: PlayerProfiler (Snap Share + Opportunity Share)

- URL: `https://www.playerprofiler.com/nfl/`
- Data: Snap %, opportunity share
- Free: ✅ Unlimited
- Quality: **Excellent**

**Shows RB role clearly via snap share + touch share.**

### Source 2: Pro Football Reference (Snap Counts)

- URL: `https://www.pro-football-reference.com/`
- Data: Snap counts by game
- Free: ✅ Unlimited

**Recommended:** **PlayerProfiler** (shows role directly)

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High
**Historical:** ✅ Yes (PlayerProfiler archives)
**Predictive:** ✅ Yes (cumulative role through week N)

---

## 6. Implementation Complexity

**Difficulty:** Easy-Medium
**Effort:** 1-2 days (scrape PlayerProfiler)

**Multiplier:**
```python
def get_role_multiplier(snap_pct: float, touch_share: float) -> float:
    # Workhorse
    if snap_pct >= 70 and touch_share >= 0.50:
        return 1.15
    # Lead back
    elif snap_pct >= 50 and touch_share >= 0.35:
        return 1.10
    # Committee
    elif snap_pct >= 30:
        return 1.00
    # Backup
    else:
        return 0.90
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High RB value, easy implementation

**Value:** ⭐⭐⭐⭐⭐ (Critical for RBs)
**Feasibility:** ⭐⭐⭐⭐ (Easy - scrape PlayerProfiler)
**Historical:** ⭐⭐⭐⭐ (Good)

**Timeline:** 1-2 days

---

*Research conducted: 2025-12-20*
