# Metric 51: Scramble Tendency (QB)

**Position Applicability:** QB
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [x] Partial - Rushing attempts available

**Details:**

Scramble Tendency = QB designed runs + scrambles (rushing attempts)

Mobile QBs (Lamar Jackson, Jalen Hurts) score significantly more via rushing.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] Yes - QB rushing attempts/yards available

---

## 3. Free Alternative Sources

ESPN API or Pro Football Reference for QB rushing stats

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High
**Historical:** ✅ Yes
**Predictive:** ✅ Yes

---

## 6. Implementation Complexity

**Difficulty:** Easy
**Effort:** 1-2 hours (use existing rushing data)

**Multiplier:**
```python
def get_qb_rush_multiplier(rush_attempts_per_game: float) -> float:
    if rush_attempts_per_game >= 8.0:
        return 1.15  # Elite mobile QB (Lamar, Hurts)
    elif rush_attempts_per_game >= 5.0:
        return 1.10  # Mobile QB
    elif rush_attempts_per_game >= 3.0:
        return 1.05  # Occasionally mobile
    else:
        return 1.00  # Pocket passer
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - Easy, high value for mobile QBs

**Value:** ⭐⭐⭐⭐ (High for mobile QBs)
**Feasibility:** ⭐⭐⭐⭐⭐ (Very easy - existing data)
**Historical:** ⭐⭐⭐⭐⭐ (Perfect)

**Timeline:** 1-2 hours (use existing rushing stats)

---

*Research conducted: 2025-12-20*
