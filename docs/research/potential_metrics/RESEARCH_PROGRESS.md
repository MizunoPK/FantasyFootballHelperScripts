# ESPN API Metric Research - Progress Tracker

**Last Updated:** 2025-12-20
**Total Metrics:** 58
**Completed:** 11/58 (19.0%)

**Source:** Based on `docs/research/scoring_gap_analysis.md` (Version 3.0, Last Updated: December 17, 2025)

---

## Progress Summary

| Priority | Total | Completed | Pending | % Complete |
|----------|-------|-----------|---------|------------|
| HIGH     | 14    | 11        | 3       | 79%        |
| MEDIUM   | 15    | 0         | 15      | 0%         |
| LOW      | 29    | 0         | 29      | 0%         |

---

## Status Legend

- ⏳ **Pending** - Research not started
- 🔍 **In Progress** - Currently researching
- ✅ **Complete** - Research document finished
- ⏸️ **Deferred** - Lower priority, postponed

---

## HIGH Priority Metrics (14 metrics)

| # | Metric Name | Position | Status | Data Source | Historical | Link |
|---|-------------|----------|--------|-------------|------------|------|
| 1 | Target Volume/Share | WR, TE, RB | ✅ Complete | PFR + Sleeper | Yes (actuals) | [View](01_target_volume.md) |
| 2 | QB Context/Quality Score | WR, TE | ✅ Complete | Existing (QB stats) | Yes (perfect) | [View](02_qb_context.md) |
| 4 | Vegas Lines/Game Environment | ALL | ✅ Complete | ESPN API + PFR | Yes (via scraping) | [View](04_vegas_lines.md) |
| 12 | Implied Team Total | ALL | ✅ Complete | Derived (Metric 4) | Yes (via Metric 4) | [View](12_implied_team_total.md) |
| 21 | WOPR (Weighted Opportunity Rating) | WR, TE | ✅ Complete | NGS + PlayerProfiler | Yes (via scraping) | [View](21_wopr.md) |
| 22 | Expected Fantasy Points (xFP) | ALL | ✅ Complete | PlayerProfiler | Yes (via scraping) | [View](22_expected_fantasy_points.md) |
| 39 | Team Red Zone TD% (K-specific) | K | ✅ Complete | TeamRankings | Yes (team stat) | [View](39_team_red_zone_td_pct.md) |
| 40 | Kicker Accuracy by Distance | K | ✅ Complete | Pro Football Ref | Yes (player stat) | [View](40_kicker_accuracy_by_distance.md) |
| 42 | Route Participation Rate (TE) | TE | ✅ Complete | PlayerProfiler | Yes (via scraping) | [View](42_route_participation_rate.md) |
| 46 | Goal-Line Role (RB) | RB | ✅ Complete | Pro Football Ref | Yes (situational) | [View](46_goal_line_role.md) |
| 49 | Role Designation (RB Workload) | RB | ✅ Complete | PlayerProfiler | Yes (via scraping) | [View](49_role_designation_rb_workload.md) |
| 50 | Receiving Share (RB) | RB | ⏳ Pending | - | - | - |
| 52 | Pass Block Rate (QB Protection) | QB | ⏳ Pending | - | - | - |
| 53 | Pressure Rate (QB) | QB | ⏳ Pending | - | - | - |

---

## MEDIUM Priority Metrics (15 metrics)

| # | Metric Name | Position | Status | Data Source | Historical | Link |
|---|-------------|----------|--------|-------------|------------|------|
| 5 | Teammate Injury Impact | ALL | ⏳ Pending | - | - | - |
| 6 | Opponent Secondary Details | WR, TE | ⏳ Pending | - | - | - |
| 7 | Red Zone Opportunity | ALL | ⏳ Pending | - | - | - |
| 13 | Air Yards (aDOT) | WR, TE | ⏳ Pending | - | - | - |
| 14 | Yards After Catch (YAC) | WR, TE, RB | ⏳ Pending | - | - | - |
| 15 | Snap Share Percentage | ALL | ⏳ Pending | - | - | - |
| 16 | Route Share | WR, TE | ⏳ Pending | - | - | - |
| 17 | Target Share Trend | WR, TE, RB | ⏳ Pending | - | - | - |
| 18 | Vacated Target Share | WR, TE | ⏳ Pending | - | - | - |
| 19 | Carry Share | RB | ⏳ Pending | - | - | - |
| 41 | Dome vs Outdoor (K Venue) | K | ⏳ Pending | - | - | - |
| 43 | Red Zone Target Efficiency (TE) | TE | ⏳ Pending | - | - | - |
| 47 | TD Equity (RB) | RB | ⏳ Pending | - | - | - |
| 51 | Scramble Tendency (QB) | QB | ⏳ Pending | - | - | - |
| 54 | Deep Ball Accuracy (WR) | WR | ⏳ Pending | - | - | - |

---

## LOW Priority Metrics (29 metrics)

| # | Metric Name | Position | Status | Data Source | Historical | Link |
|---|-------------|----------|--------|-------------|------------|------|
| 3 | QB-Specific Weather Sensitivity | QB | ⏳ Pending | - | - | - |
| 8 | Hot/Cold Streak Momentum | ALL | ⏳ Pending | - | - | - |
| 9 | Team Pass Rate/Tempo | ALL | ⏳ Pending | - | - | - |
| 10 | Divisional Game Adjustment | ALL | ⏳ Pending | - | - | - |
| 11 | Primetime Game Adjustment | ALL | ⏳ Pending | - | - | - |
| 20 | Success Rate | ALL | ⏳ Pending | - | - | - |
| 23 | EPA (Expected Points Added) | ALL | ⏳ Pending | - | - | - |
| 24 | QB Rating/Passer Rating | QB | ⏳ Pending | - | - | - |
| 25 | Time to Throw (QB) | QB | ⏳ Pending | - | - | - |
| 26 | Completion % Over Expectation | QB | ⏳ Pending | - | - | - |
| 27 | Target Separation | WR, TE | ⏳ Pending | - | - | - |
| 28 | Catch Rate Over Expected | WR, TE | ⏳ Pending | - | - | - |
| 29 | Contested Catch Rate | WR, TE | ⏳ Pending | - | - | - |
| 30 | Average Cushion | WR, TE | ⏳ Pending | - | - | - |
| 31 | Separation | WR, TE | ⏳ Pending | - | - | - |
| 32 | Completion Probability (CP) | QB, WR, TE | ⏳ Pending | - | - | - |
| 33 | Expected YAC (xYAC) | WR, TE, RB | ⏳ Pending | - | - | - |
| 34 | Team Plays Per Game | ALL | ⏳ Pending | - | - | - |
| 35 | Neutral Script Pass Rate | WR, TE, RB | ⏳ Pending | - | - | - |
| 36 | Team Red Zone Efficiency | ALL | ⏳ Pending | - | - | - |
| 37 | Snap Share Trend | ALL | ⏳ Pending | - | - | - |
| 38 | Dominator Rating | WR, TE (rookies) | ⏳ Pending | - | - | - |
| 44 | EPA Per Target (TE) | TE | ⏳ Pending | - | - | - |
| 45 | Role Security (TE) | TE | ⏳ Pending | - | - | - |
| 48 | Yards Before Contact (RB) | RB | ⏳ Pending | - | - | - |
| 55 | Target Depth Distribution (WR) | WR | ⏳ Pending | - | - | - |
| 56 | Red Zone Involvement (WR) | WR | ⏳ Pending | - | - | - |
| 57 | 3rd Down Conversion Rate (WR) | WR | ⏳ Pending | - | - | - |
| 58 | Total Opportunity Share (WR) | WR | ⏳ Pending | - | - | - |

---

## How to Use This Tracker

1. **Update after each metric researched** - Change status from ⏳ to 🔍 when starting, ✅ when complete
2. **Add data source** - Note primary source (Existing / ESPN / Free Alternative: {name})
3. **Document historical** - Note if historical data is available (Yes/No/Partial)
4. **Add link** - Link to completed research doc (e.g., `[View](01_target_volume.md)`)

**Update Format:**
```
| 1 | Target Volume/Share | WR, TE, RB | ✅ Complete | ESPN API | Yes | [View](01_target_volume.md) |
```

---

## Research Workflow

1. **Start with HIGH priority** (14 metrics first)
2. **Move to MEDIUM priority** (15 metrics)
3. **Complete with LOW priority** (29 metrics)
4. **Use TEMPLATE.md** for each metric document
5. **Update this tracker** after each completion

---

## Completion Milestones

- [ ] **Phase 1 Complete:** All 14 HIGH priority metrics researched (11/14 = 79%)
- [ ] **Phase 2 Complete:** All 15 MEDIUM priority metrics researched (0/15 = 0%)
- [ ] **Phase 3 Complete:** All 29 LOW priority metrics researched (0/29 = 0%)
- [ ] **All Research Complete:** 58/58 metrics documented (0%)

---

*This tracker is automatically maintained during the research phase. Last update: 2025-12-20*
