# Metric 50: Receiving Share (RB)

**Position Applicability:** RB (Running Back)
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [x] Yes - Partially available
- [ ] No

**Details:**

Receiving Share requires **RB targets + team passing attempts**.

**Formula:**
```
RB Target Share = (RB Targets / Team Passing Attempts) × 100

Example - Austin Ekeler (2022):
Targets: 108 out of ~550 team pass attempts = 19.6% (elite receiving RB)

Traditional RB:
Targets: 30 out of ~550 team pass attempts = 5.5% (limited receiving role)
```

**Why It Matters for PPR:**
- PPR scoring: 1 point per reception
- Receiving RBs outscore rushing-only RBs in PPR
- Target share predicts receptions better than rushing stats

**Conclusion:** Targets available in existing data (Metric 1), team pass attempts in ESPN data.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] Yes - Can be calculated from existing data

**ESPN provides:**
- RB targets (via Metric 1: Target Volume)
- Team passing attempts (team stats)

**Calculation possible using existing data sources.**

---

## 3. Free Alternative Sources

### Source 1: Pro Football Reference (Target Share)

- URL: `https://www.pro-football-reference.com/`
- Data: Targets by player, team pass attempts
- Free: ✅ Unlimited
- Quality: **Excellent**

### Source 2: PlayerProfiler (Direct Target Share %)

- URL: `https://www.playerprofiler.com/nfl/`
- Data: Target share % directly shown
- Free: ✅ Unlimited

**Recommended:** Calculate from existing Metric 1 (Targets) + team stats

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High (official stats)
**Historical:** ✅ Yes (via Metric 1 + team stats)
**Predictive:** ✅ Yes (cumulative through week N)

---

## 6. Implementation Complexity

**Difficulty:** Easy
**Effort:** 1-2 hours (calculation only)

**Multiplier:**
```python
def get_rb_receiving_multiplier(target_share_pct: float, is_ppr: bool) -> float:
    if not is_ppr:
        return 1.00  # Less valuable in standard scoring

    # PPR multipliers
    if target_share_pct >= 15.0:
        return 1.15  # Elite receiving RB (Ekeler, CMC)
    elif target_share_pct >= 10.0:
        return 1.10  # Strong receiving role
    elif target_share_pct >= 7.0:
        return 1.05  # Moderate receiving
    else:
        return 1.00  # Limited receiving
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High PPR value, easy implementation

**Value:** ⭐⭐⭐⭐⭐ (Critical for PPR leagues)
**Feasibility:** ⭐⭐⭐⭐⭐ (Very easy - use existing data)
**Historical:** ⭐⭐⭐⭐⭐ (Perfect - already have targets)

**Timeline:** 1-2 hours (calculation from existing Metric 1)

---

*Research conducted: 2025-12-20*
