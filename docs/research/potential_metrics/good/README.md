# GOOD Historical Data Availability (34 metrics)

Metrics in this folder have **good historical data availability** through reliable free scraping sources with established archives.

## Characteristics:
- ✅ **Reliable free sources** (PFR, PlayerProfiler, Next Gen Stats, TeamRankings)
- ✅ **Good historical coverage** (2021-2024, some with more)
- ⚠️ **Scraping required** (1-3 days per source typically)
- ⚠️ **Moderate implementation effort**
- ✅ **High confidence in data availability**

## Implementation Priority: **HIGH-MEDIUM**
These metrics require scraping but have proven, stable sources with good historical data.

---

## Metrics by Data Source

### Pro Football Reference (12 metrics)
**Source:** https://www.pro-football-reference.com/
**Quality:** Excellent (official NFL stats)
**Historical:** 2000+ seasons available

- M06: Opponent Secondary Details (team pass defense proxy)
- M07: Red Zone Opportunity (situational splits)
- M09: Team Pass Rate/Tempo (team stats)
- M40: Kicker Accuracy by Distance (distance splits)
- M43: Red Zone Target Efficiency (TE) (same as M07)
- M46: Goal-Line Role (RB) (situational splits)
- M52: Pass Block Rate (QB) (sack rate proxy)
- M56: Red Zone Involvement (WR) (same as M07)
- M57: 3rd Down Conversion Rate (WR) (situational splits)

### PlayerProfiler (10 metrics)
**Source:** https://www.playerprofiler.com/nfl/
**Quality:** Excellent (advanced fantasy metrics)
**Historical:** 2016+ seasons

- M15: Snap Share Percentage
- M16: Route Share (WR/TE)
- M21: WOPR (Weighted Opportunity Rating)
- M22: Expected Fantasy Points (xFP)
- M42: Route Participation Rate (TE)
- M48: Yards Before Contact (RB)
- M49: Role Designation (RB Workload)

### Next Gen Stats (13 metrics)
**Source:** https://nextgenstats.nfl.com/
**Quality:** Excellent (official NFL tracking)
**Historical:** 2016+ seasons (varies by metric)

- M13: Air Yards (aDOT)
- M14: Yards After Catch (YAC)
- M25: Time to Throw (QB)
- M26: Completion % Over Expectation (QB)
- M27: Target Separation (WR/TE)
- M28: Catch Rate Over Expected (WR/TE)
- M29: Contested Catch Rate (WR/TE)
- M30: Average Cushion (WR/TE)
- M31: Separation (WR/TE)
- M32: Completion Probability (QB/WR/TE)
- M33: Expected YAC (xYAC)
- M53: Pressure Rate (QB)
- M54: Deep Ball Accuracy (WR)
- M55: Target Depth Distribution (WR)

### TeamRankings (2 metrics)
**Source:** https://www.teamrankings.com/
**Quality:** Good (team aggregates)
**Historical:** 2010+ seasons

- M36: Team Red Zone Efficiency
- M39: Team Red Zone TD% (K-specific)

### Mixed/Estimation (2 metrics)
- M05: Teammate Injury Impact (ESPN injury + modeling)
- M35: Neutral Script Pass Rate (estimation from game logs)

---

## Implementation Effort

### Easy-Medium (1-2 days)
Single-page scraping or established patterns:
- M09, M13, M14, M15, M16, M25, M26, M36, M39, M40

### Medium (2-3 days)
Multi-page or per-player scraping:
- M05, M06, M07, M21, M22, M27-33, M35, M42, M43, M46, M48, M49, M52-57

### Batch Scraping Opportunities
**Next Gen Stats batch** (13 metrics, 3-5 days total):
- M13, M14, M25-33, M53-55

**PFR situational batch** (5 metrics, 2-3 days total):
- M07, M40, M43, M46, M56, M57

**PlayerProfiler batch** (7 metrics, 2-3 days total):
- M15, M16, M21, M22, M42, M48, M49

---

## Historical Data Confidence: 85-95%

Most metrics have:
- ✅ 2021-2024 coverage (sufficient for simulation validation)
- ✅ Weekly snapshots available
- ✅ Predictive data (cumulative stats through week N)
- ⚠️ Some NGS metrics may have limited early-season coverage

**Recommended:** Implement in batches by data source to maximize efficiency.

---

*Last Updated: 2025-12-20*
