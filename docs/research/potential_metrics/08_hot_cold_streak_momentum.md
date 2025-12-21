# Metric 8: Hot/Cold Streak Momentum

**Position Applicability:** ALL
**Priority:** LOW
**Research Date:** 2025-12-20

---

## Summary

Recent performance momentum (last 2-3 games trending up/down).

**Data Source:** Derived from existing stats (calculate trend from recent games)

**Implementation:** Easy (1-2 hours - calculation)

**Recommendation:** PURSUE - Easy calculation from existing data

**Value:** ⭐⭐ (Low - recency bias risk)
**Feasibility:** ⭐⭐⭐⭐⭐ (Very easy)
**Historical:** ⭐⭐⭐⭐⭐ (Perfect)

**Multiplier:**
```python
def get_momentum_multiplier(recent_trend_pct: float) -> float:
    if recent_trend_pct >= 15.0:
        return 1.05  # Hot streak
    elif recent_trend_pct <= -15.0:
        return 0.95  # Cold streak
    else:
        return 1.00
```

---

*Research conducted: 2025-12-20*
