# Metric 52: Pass Block Rate (QB Protection)

**Position Applicability:** QB (Quarterback)
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires advanced tracking

**Details:**

Pass Block Rate requires **offensive line performance + pressure tracking**.

**Formula:**
```
Pass Block Win Rate = (Pass Plays Without Pressure / Total Pass Plays) × 100

Example - Elite O-Line (PHI 2023):
Pass Block Win Rate: 68% (QB rarely pressured, more time to throw)

Poor O-Line:
Pass Block Win Rate: 52% (QB frequently pressured, rushed throws)
```

**Why It Matters:**
- Protected QBs: More completions, fewer INTs, more TDs
- Pressured QBs: Lower completion %, more sacks, lower fantasy output
- Better protection = Better QB performance (~0.6 correlation)

**Conclusion:** Not in existing data. Requires NFL tracking data.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

ESPN doesn't provide offensive line metrics or pass block win rates.

---

## 3. Free Alternative Sources

### Source 1: Pro Football Focus (PFF - Premium Only)

- URL: `https://www.pff.com/`
- Data: Pass block win rate, O-line grades
- Free: ❌ Paywall ($200+/year)
- Quality: **Elite**

### Source 2: Next Gen Stats (Limited O-Line Data)

- URL: `https://nextgenstats.nfl.com/`
- Data: Some QB pressure metrics
- Free: ✅ Unlimited
- Quality: **High** (but limited O-line specific data)

### Source 3: Football Outsiders (Adjusted Sack Rate)

- URL: `https://www.footballoutsiders.com/`
- Data: Adjusted sack rate (team metric)
- Free: ⚠️ Limited
- Quality: **Good**

**Challenge:** Free sources don't provide comprehensive pass block win rates.

**Alternative Approach:** Use **sack rate** as proxy (inverse correlation):
- Low sack rate = Good protection
- High sack rate = Poor protection

---

## 4-5. Data Quality & Historical Availability

**Reliability:** Medium (proxy via sack rate)
**Historical:** ⚠️ Partial (sack rate available, not pass block win rate)
**Predictive:** ✅ Yes (cumulative through week N)

---

## 6. Implementation Complexity

**Difficulty:** Medium-Hard
**Effort:** 2-3 days (scraping or proxy calculation)

**Proxy Multiplier (using sack rate):**
```python
def get_qb_protection_multiplier(team_sack_rate_pct: float) -> float:
    # Sack Rate = (Sacks / Pass Attempts) × 100
    # Low sack rate = Good protection
    if team_sack_rate_pct <= 4.0:
        return 1.10  # Elite protection (Eagles, Chiefs)
    elif team_sack_rate_pct <= 5.5:
        return 1.05  # Good protection
    elif team_sack_rate_pct <= 7.0:
        return 1.00  # Average
    elif team_sack_rate_pct <= 8.5:
        return 0.95  # Poor protection
    else:
        return 0.90  # Very poor protection (many sacks)
```

**Data Source:** Pro Football Reference (team stats, sack rate)

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE (with proxy)** - Use sack rate as proxy for protection

**Value:** ⭐⭐⭐⭐ (High for QBs)
**Feasibility:** ⭐⭐⭐ (Medium - use sack rate proxy)
**Historical:** ⭐⭐⭐ (Good - sack rate available)

**Approach:** Use team sack rate as proxy for QB protection quality.

**Timeline:** 1-2 days (scrape team sack rates from PFR)

---

*Research conducted: 2025-12-20*
