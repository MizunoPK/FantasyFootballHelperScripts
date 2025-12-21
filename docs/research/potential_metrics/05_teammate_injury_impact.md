# Metric 5: Teammate Injury Impact

**Position Applicability:** ALL
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires injury tracking + target/usage redistribution analysis

**Details:**

Teammate Injury Impact requires:
1. Weekly injury reports (who's out/limited)
2. Historical usage redistribution when key players miss time
3. Position-specific impact modeling

**Examples:**
```
WR1 out → WR2/WR3 see +30% target increase
Star RB out → Backup RB sees +60% carry increase
Elite TE out → WRs see +15% targets, secondary TE +40%
Top WR out with elite QB → Remaining WRs benefit more than with poor QB
```

**Conclusion:** Not in existing data. Requires injury tracking + impact modeling.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] Partial - Injury status available, impact modeling not provided

**ESPN provides:**
- Current injury status (Out, Questionable, Doubtful)
- But NOT impact on teammates

---

## 3. Free Alternative Sources

### Source 1: ESPN Injury Report (Current Status)

- URL: `https://www.espn.com/nfl/injuries`
- Data: Weekly injury status
- Free: ✅ Unlimited
- Quality: **Good** (official reports)

### Source 2: Historical Target/Usage Data (Build Impact Model)

- Source: Pro Football Reference, ESPN API
- Approach: Analyze historical games where key players missed time
- Calculate average usage redistribution by position

### Source 3: FantasyPros (Manual Impact Articles)

- URL: `https://www.fantasypros.com/`
- Data: Weekly injury impact analysis (editorial)
- Free: ✅ Limited
- Quality: **Good** (expert analysis, but not data-driven)

**Recommended Approach:**
1. Scrape ESPN injury report for current status
2. Build historical impact model (WR1 out → WR2/WR3 boost)
3. Apply multipliers based on teammate injuries

---

## 4-5. Data Quality & Historical Availability

**Reliability:** Medium (injury reports reliable, impact modeling complex)
**Historical:** ⚠️ Partial (can build from historical usage data)
**Predictive:** ✅ Yes (current injury status predicts week N usage)

---

## 6. Implementation Complexity

**Difficulty:** Hard
**Effort:** 3-5 days (scraping + impact modeling)

**Steps:**
1. Scrape weekly injury reports (ESPN)
2. Identify key teammates out/limited for each player
3. Build position-specific impact model:
   - WR1 out → WR2/WR3 boost calculation
   - RB1 out → RB2 boost calculation
   - TE1 out → WR/TE2 boost calculation
4. Apply multipliers

**Example Multiplier:**
```python
def get_teammate_injury_boost(position: str, injured_teammate_role: str) -> float:
    # WR benefits when WR1 is out
    if position == "WR" and injured_teammate_role == "WR1":
        return 1.15  # WR2/WR3 see significant target boost

    # RB benefits when RB1 is out
    elif position == "RB" and injured_teammate_role == "RB1":
        return 1.25  # Backup RB becomes workhorse

    # WR benefits when elite TE is out
    elif position == "WR" and injured_teammate_role == "TE1":
        return 1.08  # Moderate target redistribution

    else:
        return 1.00  # No impact
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **DEFER** - High value but complex implementation

**Value:** ⭐⭐⭐⭐ (High - significant fantasy impact)
**Feasibility:** ⭐⭐ (Hard - requires impact modeling)
**Historical:** ⭐⭐⭐ (Good - can build from historical data)

**Rationale:**
- High value (teammate injuries create big opportunity shifts)
- Complex implementation (requires position-specific modeling)
- **Recommend deferring** until simpler MEDIUM metrics complete

**Alternative:** Start with simple version (just flag if WR1/RB1/TE1 is out, apply flat boost)

**Timeline:** 3-5 days (full implementation), 1-2 days (simple version)

---

*Research conducted: 2025-12-20*
