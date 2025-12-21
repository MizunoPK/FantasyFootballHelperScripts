# Metric 53: Pressure Rate (QB)

**Position Applicability:** QB (Quarterback)
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires advanced tracking

**Details:**

Pressure Rate requires **Next Gen Stats tracking** (QB pressures per dropback).

**Formula:**
```
Pressure Rate = (Pressures Allowed / Dropbacks) × 100

Elite QB Under Pressure - Patrick Mahomes:
Pressure Rate: 28% (frequently pressured)
Performance Under Pressure: Elite (still scores despite pressure)

Average QB:
Pressure Rate: 25%
Performance Under Pressure: Struggles (INT rate up 50%)
```

**Why It Matters:**
- Some QBs thrive under pressure (Mahomes, Allen)
- Most QBs struggle under pressure (lower completion %, more INTs)
- Matchup factor: Good D-line vs poor O-line = high pressure

**Conclusion:** Not in existing data. Requires tracking data.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

ESPN doesn't provide pressure rate data.

---

## 3. Free Alternative Sources

### Source 1: Next Gen Stats (QB Pressure Metrics)

- URL: `https://nextgenstats.nfl.com/stats/passing`
- Data: Time to throw, pressure rate
- Free: ✅ Unlimited
- Quality: **Excellent** (official NFL tracking)

**Shows QB performance under pressure directly.**

### Source 2: Pro Football Focus (PFF - Premium)

- URL: `https://www.pff.com/`
- Data: Pressure rate, performance under pressure
- Free: ❌ Paywall
- Quality: **Elite**

### Source 3: Pro Football Reference (Sacks as Proxy)

- URL: `https://www.pro-football-reference.com/`
- Data: Sacks taken (partial proxy)
- Free: ✅ Unlimited

**Recommended:** **Next Gen Stats** (free, official tracking)

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High (Next Gen Stats)
**Historical:** ⚠️ Limited (NGS historical data availability varies)
**Predictive:** ✅ Yes (cumulative through week N)

---

## 6. Implementation Complexity

**Difficulty:** Medium
**Effort:** 1-2 days (scrape Next Gen Stats)

**Multiplier:**
```python
def get_qb_pressure_multiplier(pressure_rate_pct: float, performance_under_pressure: str) -> float:
    # Elite QBs under pressure (Mahomes, Allen)
    if performance_under_pressure == "Elite" and pressure_rate_pct >= 25.0:
        return 1.05  # Thrives despite pressure

    # Average QB under heavy pressure
    elif pressure_rate_pct >= 30.0:
        return 0.90  # Struggles under constant pressure
    elif pressure_rate_pct >= 25.0:
        return 0.95  # Moderate pressure impact
    else:
        return 1.00  # Clean pocket most plays
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High QB value, medium implementation

**Value:** ⭐⭐⭐⭐ (High for QBs)
**Feasibility:** ⭐⭐⭐ (Medium - scrape Next Gen Stats)
**Historical:** ⭐⭐⭐ (Good if NGS historical available)

**Timeline:** 1-2 days (scrape Next Gen Stats)

---

*Research conducted: 2025-12-20*
