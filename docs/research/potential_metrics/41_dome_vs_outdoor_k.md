# Metric 41: Dome vs Outdoor (K Venue)

**Position Applicability:** K (Kicker)
**Priority:** MEDIUM
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [ ] Yes
- [x] No - Requires stadium/venue tracking

**Details:**

Dome kickers have higher accuracy (controlled conditions). Outdoor kickers face wind/weather.

**Formula:**
```
Venue Type:
- Dome/Indoor: Favorable (no wind, consistent conditions)
- Outdoor: Weather-dependent (wind affects FG accuracy)
- Retractable Roof: Variable
```

---

## 2. ESPN API Availability

**Is this metric available?**

- [x] Partial - Game location available, stadium type needs mapping

---

## 3. Free Alternative Sources

### Source 1: Stadium Reference (Static Mapping)

- Create static mapping: Team → Stadium → Venue Type
- Examples:
  - Falcons (ATL) → Mercedes-Benz Stadium → Dome
  - Packers (GB) → Lambeau Field → Outdoor

**One-time setup:** Map all 32 teams to venue types

---

## 4-5. Data Quality & Historical Availability

**Reliability:** High (static mapping)
**Historical:** ✅ Yes (stadium doesn't change often)
**Predictive:** ✅ Yes

---

## 6. Implementation Complexity

**Difficulty:** Easy
**Effort:** 1-2 hours (create static venue mapping)

**Multiplier:**
```python
def get_kicker_venue_multiplier(venue_type: str) -> float:
    if venue_type == "Dome":
        return 1.05  # Favorable conditions
    elif venue_type == "Outdoor":
        return 1.00  # Weather-dependent
    else:  # Retractable
        return 1.02
```

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - Easy implementation, static mapping

**Value:** ⭐⭐⭐ (Medium - kicker-specific)
**Feasibility:** ⭐⭐⭐⭐⭐ (Very easy - static mapping)
**Historical:** ⭐⭐⭐⭐⭐ (Perfect)

**Timeline:** 1-2 hours (create team → venue type mapping)

---

*Research conducted: 2025-12-20*
