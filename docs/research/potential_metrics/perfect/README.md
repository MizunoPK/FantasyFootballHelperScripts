# PERFECT Historical Data Availability (17 metrics)

Metrics in this folder have **perfect historical data availability** through existing data, static mappings, or simple calculations.

## Characteristics:
- ✅ **No scraping required** (or minimal one-time setup)
- ✅ **Complete historical coverage** (2021-2024+)
- ✅ **Immediate implementation** (1-2 hours typically)
- ✅ **Zero data acquisition risk**

## Implementation Priority: **HIGHEST**
These metrics should be implemented first as they require minimal effort and have guaranteed data availability.

---

## Metrics List (17 total)

### Existing/Derived Data (15 metrics)
**Data Source:** Already in system or calculable from existing stats

1. **M02: QB Context/Quality Score** - Calculate from existing QB stats
2. **M08: Hot/Cold Streak Momentum** - Calculate trend from recent games
3. **M10: Divisional Game Adjustment** - Static division mapping
4. **M11: Primetime Game Adjustment** - Game time metadata
5. **M12: Implied Team Total** - Derived from M04 (Vegas Lines)
6. **M17: Target Share Trend** - Calculate from M01 (Targets)
7. **M19: Carry Share** - Calculate from existing carry data
8. **M24: QB Rating/Passer Rating** - Standard formula from stats
9. **M34: Team Plays Per Game** - Existing team stat
10. **M37: Snap Share Trend** - Calculate from M15 (Snap Share)
11. **M41: Dome vs Outdoor (K)** - Static venue mapping (32 teams)
12. **M45: Role Security (TE)** - Derived from M42 + M15
13. **M50: Receiving Share (RB)** - Calculate from M01 + team stats
14. **M51: Scramble Tendency (QB)** - Existing QB rushing stats
15. **M58: Total Opportunity Share (WR)** - Derived from M01

### ESPN API (2 metrics)
**Data Source:** ESPN Fantasy Football API (direct access)

16. **M01: Target Volume/Share** - ESPN API (actuals)
17. **M04: Vegas Lines/Game Environment** - ESPN API + PFR scraping

---

## Implementation Notes

### Immediate (1-2 hours each)
- M08, M10, M11, M12, M17, M19, M24, M37, M45, M50, M51, M58
- Pure calculation/derivation from existing data

### One-Time Setup (1-2 hours total)
- M41: Create team → venue type mapping (32 teams, rarely changes)
- M02: Set up QB stat aggregation

### API Access (Already Available)
- M01: ESPN API (likely already integrated)
- M04: ESPN API for current, PFR scraping for historical

---

## Historical Data Confidence: 100%

All metrics in this folder can be calculated or derived from data that is:
1. Already in the system
2. Available via existing APIs
3. Static and unchanging (division/venue mappings)
4. Simple calculations from existing stats

**No external dependencies or scraping fragility.**

---

*Last Updated: 2025-12-20*
