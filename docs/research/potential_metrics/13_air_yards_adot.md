# Metric 13: Air Yards (aDOT)

**Position Applicability:** WR, TE
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires Next Gen Stats tracking

**Details:**

Air Yards (Average Depth of Target) requires **Next Gen Stats** tracking of target distance.

**Formula:**
```
aDOT = Total Air Yards / Total Targets

Example - Deep threat WR (DeSean Jackson):
aDOT: 15.2 yards (deep routes, big play potential)

Short-area WR (slot receiver):
aDOT: 7.5 yards (underneath routes, volume-based)
```

**Why It Matters:**
- High aDOT = Big play upside, higher variance
- Low aDOT = Volume-based, consistent floor
- Related to WOPR (Metric 21 uses air yards share)

**Conclusion:** Not in existing data. Requires Next Gen Stats.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

ESPN doesn't provide air yards or aDOT.

---

## 3. Free Alternative Sources

### Source 1: Next Gen Stats (Official Air Yards)

- URL: `https://nextgenstats.nfl.com/stats/receiving`
- Data: Air yards, aDOT, cushion
- Free: ✅ Unlimited
- Quality: **Excellent** (official NFL tracking)

### Source 2: PlayerProfiler (Air Yards Share)

- URL: `https://www.playerprofiler.com/nfl/`
- Data: Air yards, aDOT
- Free: ✅ Unlimited
- Quality: **Excellent**

### Source 3: Pro Football Reference (No aDOT)

- PFR doesn't provide air yards

**Recommended:** **Next Gen Stats** (official) or **PlayerProfiler**

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High (NGS official tracking)
**Historical:** ⚠️ Partial (NGS archives limited, PlayerProfiler better)
**Predictive:** ✅ Yes (cumulative aDOT through week N)

---

## 6. Implementation Complexity

**Difficulty:** Medium
**Effort:** 1-2 days (scraping NGS or PlayerProfiler)

**Multiplier:**
```python
def get_adot_multiplier(adot: float, position: str) -> float:
    # High aDOT (deep threat)
    if adot >= 12.0:
        return 1.05  # Big play upside (higher ceiling, lower floor)

    # Moderate aDOT (balanced)
    elif adot >= 8.0:
        return 1.00  # Neutral

    # Low aDOT (short-area)
    else:
        return 1.00  # Volume-based (consistent floor)
```

**Note:** aDOT is component of WOPR (Metric 21 - already researched)

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - Medium value, already part of WOPR

**Value:** ⭐⭐⭐ (Medium - useful for player profiling)
**Feasibility:** ⭐⭐⭐⭐ (Medium-Easy - scrape NGS/PlayerProfiler)
**Historical:** ⭐⭐⭐ (Good - via PlayerProfiler)

**Note:** Air yards share already captured in WOPR (Metric 21). aDOT adds player profiling context.

**Timeline:** 1-2 days (scraping, likely same source as WOPR)

---

*Research conducted: 2025-12-20*
