# Metric 42: Route Participation Rate (TE)

**Position Applicability:** TE (Tight End)
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data in the `data/` folder?**

- [ ] Yes - Calculate from existing columns
- [x] No - Requires new data source
- [ ] Partial - Some components available

**Details:**

Route Participation Rate is **NOT available in existing data**. This is an **advanced tracking metric**.

**Formula:**
```
Route % = (Routes Run / Team Pass Plays) × 100

Example - Travis Kelce (KC):
Routes Run: 450 out of 550 team pass plays = 81.8% (elite pass-catching TE)

Blocking TE:
Routes Run: 150 out of 550 team pass plays = 27.3% (primarily blocking)
```

**Why Route % > Snap Count:**
- TE can be on field (high snaps) but blocking (low routes = no targets)
- Route % directly measures pass-catching involvement
- Strong correlation with targets (~0.8)

**Conclusion:** Not in existing data. Requires advanced tracking stats.

---

## 2. ESPN API Availability

**Is this metric available via ESPN Fantasy Football API?**

- [x] No - Not available

ESPN Fantasy API does NOT provide route participation data. This requires advanced tracking.

---

## 3. Free Alternative Sources

### Source 1: PlayerProfiler.com (Route % Available)

- URL: `https://www.playerprofiler.com/nfl/`
- Data: Route participation % for all TEs
- Free tier: ✅ Unlimited
- Historical: ✅ Available
- Quality: **Excellent**

**Advantage:** Shows route % directly, no calculation needed.

### Source 2: Pro Football Focus (PFF - Premium)

- URL: `https://www.pff.com/`
- Data: Routes run, route %
- Free tier: ⚠️ Very limited (paywall)
- Quality: **Elite** (but expensive)

### Source 3: Next Gen Stats (Limited TE Data)

- URL: `https://nextgenstats.nfl.com/`
- Data: Some receiving stats, may not have route % for TEs
- Free tier: ✅ Unlimited
- Quality: **Very High** (official NFL)

**Recommended Source:** **PlayerProfiler** (free, shows route % directly)

---

## 4. Data Quality Assessment

**Reliability:** High (PlayerProfiler stable)
**Accuracy:** Very High (tracking data-based)
**Update Frequency:** Weekly

**Known Limitations:**
- Small sample early season
- Injury/role changes affect route %
- Weather games (fewer pass plays) skew %

---

## 5. Historical Data Availability ⚠️ CRITICAL

**Can we obtain weekly snapshots for simulation validation?**

- [x] Yes - Historical data available via PlayerProfiler

**Seasons Available:**
- 2021-2024: ✅ Via PlayerProfiler scraping

**Data Timing:** ✅ Predictive (cumulative routes through week N predicts week N+1)

**Historical Acquisition:**
```python
def scrape_playerprofiler_route_pct(year: int) -> pd.DataFrame:
    """Scrape PlayerProfiler for TE route participation %"""
    url = f"https://www.playerprofiler.com/nfl/{year}/"
    # Scraping logic
    return df  # columns: player, team, route_pct
```

**sim_data Integration:**
- File: `players.csv`
- New column: `route_pct` (float, 0-100, TEs only)
- New column: `route_multiplier` (float, 0.90-1.10)

---

## 6. Implementation Complexity

**Difficulty:** Medium
**Estimated Effort:** 1-2 days (scraping PlayerProfiler)

**Data Fetching:**
- Scrape PlayerProfiler for route % (similar to WOPR, xFP scraping)
- Extract: Player, route participation %

**Multiplier Calculation:**
```python
def get_route_pct_multiplier(route_pct: float) -> float:
    if route_pct >= 75.0:
        return 1.10  # Elite pass-catching TE
    elif route_pct >= 60.0:
        return 1.05  # Significant receiving role
    elif route_pct >= 45.0:
        return 1.00  # Balanced role
    elif route_pct >= 30.0:
        return 0.95  # Limited receiving
    else:
        return 0.90  # Primarily blocking TE
```

**Dependencies:** None

**Cost:** $0 (PlayerProfiler free)

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High TE value, medium implementation

**Rationale:**

**Value:** ⭐⭐⭐⭐⭐ (Very High for TEs)
- Best predictor of TE target opportunity
- Separates pass-catching TEs from blocking TEs
- Better than snap count alone

**Feasibility:** ⭐⭐⭐ (Medium)
- Requires scraping PlayerProfiler (1-2 days)
- Similar to WOPR/xFP scraping (established pattern)

**Historical Data:** ⭐⭐⭐⭐ (Good)
- ✅ Available via PlayerProfiler
- ✅ Predictive

**Maintenance:** ⭐⭐⭐ (Medium)
- Scraping-dependent (website structure changes)

**Preferred Data Source:** **PlayerProfiler** (free, direct route %)

**Implementation Priority:** Medium-High (after basic metrics)

**Next Steps:**
1. Scrape PlayerProfiler for TE route % (1-2 days)
2. Apply multiplier: High route % (75%+) = 1.10x, Low (<30%) = 0.90x
3. Test with historical data

**Example Impact:**
```
Travis Kelce (81% route %): 1.10x multiplier (elite pass-catcher)
Blocking TE (25% route %): 0.90x multiplier (limited targets)
```

**Blockers:** None (PlayerProfiler scraping)

**Timeline:** 1-2 days

---

## Research Completeness Checklist

- [x] All 7 sections completed
- [x] Position applicability documented (TE)
- [x] Minimum 2-3 alternatives researched (PlayerProfiler, PFF, Next Gen Stats)
- [x] Historical data assessed (YES - via PlayerProfiler)
- [x] Schema defined (route_pct, route_multiplier)
- [x] Clear recommendation (PURSUE - scraping approach)
- [x] Dependencies documented (None)
- [x] Effort estimated (1-2 days)

---

## Related Metrics

- Metric 16: Route Share (WR, TE) - Related MEDIUM priority metric
- Metric 15: Snap Share Percentage - Less predictive than route % for TEs

**Notes:**
- Route % is TE-specific HIGH priority (better than snap count)
- Scraping PlayerProfiler is established pattern (WOPR, xFP)
- Critical for differentiating TE roles

---

## Lifecycle Notes

**Data Source Stability:** Medium (PlayerProfiler scraping)
**Deprecation Risk:** Low (established fantasy metric)
**Replacement Strategy:** Primary: PlayerProfiler, Fallback: PFF (if budget allows)

---

*Research conducted: 2025-12-20*
*Next review: After implementation*
