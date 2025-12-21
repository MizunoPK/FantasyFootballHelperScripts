# Metric 7: Red Zone Opportunity

**Position Applicability:** ALL
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires situational/red zone stats

**Details:**

Red Zone Opportunity requires:
- Targets/carries inside the 20-yard line
- Player's share of team red zone opportunities
- Red zone touches predict TDs better than total touches

**Formula:**
```
RZ Opportunity Share = (Player RZ Touches / Team RZ Touches) × 100

Example - Davante Adams:
Red Zone Targets: 25 out of 80 team RZ plays = 31% (elite RZ role)
Result: High TD probability

Low RZ Role:
Red Zone Targets: 8 out of 80 team RZ plays = 10% (limited TD opportunity)
```

**Conclusion:** Not in existing data. Requires situational stats.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

ESPN doesn't provide red zone-specific stats.

---

## 3. Free Alternative Sources

### Source 1: Pro Football Reference (Red Zone Stats)

- URL: `https://www.pro-football-reference.com/`
- Data: Targets/carries in red zone (player splits)
- Free: ✅ Unlimited
- Quality: **Excellent**

### Source 2: PlayerProfiler (Red Zone Metrics)

- URL: `https://www.playerprofiler.com/nfl/`
- Data: Red zone opportunity share
- Free: ✅ Unlimited
- Quality: **Excellent**

### Source 3: Next Gen Stats (Limited)

- URL: `https://nextgenstats.nfl.com/`
- May have some red zone data

**Recommended:** **PlayerProfiler** or **Pro Football Reference**

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High
**Historical:** ✅ Yes (PFR splits, PlayerProfiler archives)
**Predictive:** ✅ Yes (cumulative RZ touches through week N)

---

## 6. Implementation Complexity

**Difficulty:** Medium
**Effort:** 1-2 days (scraping)

**Multiplier:**
```python
def get_red_zone_multiplier(rz_opportunity_share_pct: float) -> float:
    if rz_opportunity_share_pct >= 25.0:
        return 1.15  # Elite RZ role (high TD probability)
    elif rz_opportunity_share_pct >= 15.0:
        return 1.10  # Strong RZ involvement
    elif rz_opportunity_share_pct >= 10.0:
        return 1.05  # Moderate RZ role
    else:
        return 1.00  # Limited RZ work
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High value, medium implementation

**Value:** ⭐⭐⭐⭐ (High - best TD predictor)
**Feasibility:** ⭐⭐⭐ (Medium - scraping required)
**Historical:** ⭐⭐⭐⭐ (Good - available via PFR/PlayerProfiler)

**Note:** Similar to Metric 46 (Goal-Line Role) but broader (inside 20 vs inside 5)

**Timeline:** 1-2 days (scrape PlayerProfiler or PFR)

---

*Research conducted: 2025-12-20*
