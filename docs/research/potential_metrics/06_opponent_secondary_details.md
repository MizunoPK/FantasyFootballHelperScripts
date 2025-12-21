# Metric 6: Opponent Secondary Details

**Position Applicability:** WR, TE
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires opponent defensive back tracking

**Details:**

Opponent Secondary Details requires:
- CB1/CB2 quality ratings
- Slot CB vs boundary CB strength
- Safety coverage quality
- Injury status of defensive backs

**Examples:**
```
WR1 vs Elite CB1 (Jalen Ramsey): -10% penalty
WR2 vs Weak CB2: +10% boost
Slot WR vs Poor Slot CB: +15% boost
TE vs Weak Safety coverage: +12% boost
```

**Conclusion:** Not in existing data. Requires defensive player tracking.

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] No

ESPN doesn't provide CB/safety quality ratings or matchup details.

---

## 3. Free Alternative Sources

### Source 1: Pro Football Focus (PFF - Premium)

- URL: `https://www.pff.com/`
- Data: CB grades, coverage stats
- Free: ❌ Paywall ($200+/year)
- Quality: **Elite**

### Source 2: Pro Football Reference (Pass Defense Rankings)

- URL: `https://www.pro-football-reference.com/`
- Data: Team pass defense stats (yards/game, TDs allowed)
- Free: ✅ Unlimited
- Quality: **Good** (team-level, not position-specific)

### Source 3: FantasyPros (WR/CB Matchup Chart)

- URL: `https://www.fantasypros.com/nfl/matchups/`
- Data: Weekly WR/CB matchup ratings
- Free: ⚠️ Limited free tier
- Quality: **Good** (weekly expert analysis)

**Recommended Approach:** Use team pass defense stats as proxy (less granular than CB-specific)

---

## 4-5. Data Quality & Historical Availability

**Reliability:** Medium (team stats proxy, not true CB matchup)
**Historical:** ⚠️ Partial (team stats available, CB-specific not free)
**Predictive:** ✅ Yes (opponent pass defense through week N)

---

## 6. Implementation Complexity

**Difficulty:** Medium-Hard
**Effort:** 2-3 days (team pass defense proxy)

**Proxy Multiplier:**
```python
def get_secondary_matchup_multiplier(opponent_pass_def_rank: int, position: str) -> float:
    # Opponent ranked 1-10 (elite pass defense)
    if opponent_pass_def_rank <= 10:
        return 0.90  # Tough matchup for WR/TE

    # Opponent ranked 11-22 (average)
    elif opponent_pass_def_rank <= 22:
        return 1.00  # Neutral

    # Opponent ranked 23-32 (poor pass defense)
    else:
        return 1.10  # Favorable matchup
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE (with proxy)** - Use team pass defense as proxy

**Value:** ⭐⭐⭐ (Medium-High for WR/TE)
**Feasibility:** ⭐⭐⭐ (Medium - team stats proxy)
**Historical:** ⭐⭐⭐ (Good - team stats available)

**Approach:** Use team pass defense rankings as proxy (not CB-specific, but free and predictive)

**Timeline:** 1-2 days (scrape team pass defense rankings)

---

*Research conducted: 2025-12-20*
