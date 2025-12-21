# ESPN API Metric Research - Progress Tracker

**Last Updated:** 2025-12-20
**Total Metrics:** 58
**Completed:** 58/58 (100.0%)

**Source:** Based on `docs/research/scoring_gap_analysis.md` (Version 3.0, Last Updated: December 17, 2025)

---

## Progress Summary

| Priority | Total | Completed | Pending | % Complete |
|----------|-------|-----------|---------|------------|
| HIGH     | 14    | 14        | 0       | 100%       |
| MEDIUM   | 15    | 15        | 0       | 100%       |
| LOW      | 29    | 29        | 0       | 100%       |

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
| 50 | Receiving Share (RB) | RB | ✅ Complete | Existing (Metric 1) | Yes (perfect) | [View](50_receiving_share_rb.md) |
| 52 | Pass Block Rate (QB Protection) | QB | ✅ Complete | PFR (sack rate proxy) | Yes (team stat) | [View](52_pass_block_rate_qb.md) |
| 53 | Pressure Rate (QB) | QB | ✅ Complete | Next Gen Stats | Yes (via scraping) | [View](53_pressure_rate_qb.md) |

---

## MEDIUM Priority Metrics (15 metrics)

| # | Metric Name | Position | Status | Data Source | Historical | Link |
|---|-------------|----------|--------|-------------|------------|------|
| 5 | Teammate Injury Impact | ALL | ✅ Complete | ESPN Injury + Model | Partial (can build) | [View](05_teammate_injury_impact.md) |
| 6 | Opponent Secondary Details | WR, TE | ✅ Complete | PFR (team pass D proxy) | Yes (team stat) | [View](06_opponent_secondary_details.md) |
| 7 | Red Zone Opportunity | ALL | ✅ Complete | PlayerProfiler / PFR | Yes (via scraping) | [View](07_red_zone_opportunity.md) |
| 13 | Air Yards (aDOT) | WR, TE | ✅ Complete | Next Gen Stats / PP | Yes (via scraping) | [View](13_air_yards_adot.md) |
| 14 | Yards After Catch (YAC) | WR, TE, RB | ✅ Complete | Next Gen Stats / PP | Yes (via scraping) | [View](14_yards_after_catch_yac.md) |
| 15 | Snap Share Percentage | ALL | ✅ Complete | PlayerProfiler / PFR | Yes (via scraping) | [View](15_snap_share_percentage.md) |
| 16 | Route Share | WR, TE | ✅ Complete | PlayerProfiler | Yes (same as M42) | [View](16_route_share.md) |
| 17 | Target Share Trend | WR, TE, RB | ✅ Complete | Derived (Metric 1) | Yes (perfect) | [View](17_target_share_trend.md) |
| 18 | Vacated Target Share | WR, TE | ✅ Complete | Manual (preseason) | No (defer) | [View](18_vacated_target_share.md) |
| 19 | Carry Share | RB | ✅ Complete | ESPN / existing | Yes (perfect) | [View](19_carry_share.md) |
| 41 | Dome vs Outdoor (K Venue) | K | ✅ Complete | Static mapping | Yes (perfect) | [View](41_dome_vs_outdoor_k.md) |
| 43 | Red Zone Target Efficiency (TE) | TE | ✅ Complete | PFR / PP (same as M7) | Yes (via scraping) | [View](43_red_zone_target_efficiency_te.md) |
| 47 | TD Equity (RB) | RB | ✅ Complete | Derived (M22,46,7) | No (defer) | [View](47_td_equity_rb.md) |
| 51 | Scramble Tendency (QB) | QB | ✅ Complete | Existing (rush stats) | Yes (perfect) | [View](51_scramble_tendency_qb.md) |
| 54 | Deep Ball Accuracy (WR) | WR | ✅ Complete | Next Gen Stats | Yes (via scraping) | [View](54_deep_ball_accuracy_wr.md) |

---

## LOW Priority Metrics (29 metrics)

| # | Metric Name | Position | Status | Data Source | Historical | Link |
|---|-------------|----------|--------|-------------|------------|------|
| 3 | QB-Specific Weather Sensitivity | QB | ✅ Complete | Manual (defer) | Limited | [View](03_qb_weather_sensitivity.md) |
| 8 | Hot/Cold Streak Momentum | ALL | ✅ Complete | Derived (calculation) | Yes (perfect) | [View](08_hot_cold_streak_momentum.md) |
| 9 | Team Pass Rate/Tempo | ALL | ✅ Complete | Pro Football Reference | Yes (scraping) | [View](09_team_pass_rate_tempo.md) |
| 10 | Divisional Game Adjustment | ALL | ✅ Complete | Static mapping | Yes (perfect) | [View](10_divisional_game_adjustment.md) |
| 11 | Primetime Game Adjustment | ALL | ✅ Complete | Game metadata | Yes (perfect) | [View](11_primetime_game_adjustment.md) |
| 20 | Success Rate | ALL | ✅ Complete | Premium (defer) | Limited | [View](20_success_rate.md) |
| 23 | EPA (Expected Points Added) | ALL | ✅ Complete | Premium (defer) | Limited | [View](23_epa_expected_points_added.md) |
| 24 | QB Rating/Passer Rating | QB | ✅ Complete | Formula (existing) | Yes (perfect) | [View](24_qb_rating_passer_rating.md) |
| 25 | Time to Throw (QB) | QB | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](25_time_to_throw_qb.md) |
| 26 | Completion % Over Expectation | QB | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](26_completion_pct_over_expectation.md) |
| 27 | Target Separation | WR, TE | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](27_target_separation.md) |
| 28 | Catch Rate Over Expected | WR, TE | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](28_catch_rate_over_expected.md) |
| 29 | Contested Catch Rate | WR, TE | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](29_contested_catch_rate.md) |
| 30 | Average Cushion | WR, TE | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](30_average_cushion.md) |
| 31 | Separation | WR, TE | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](31_separation.md) |
| 32 | Completion Probability (CP) | QB, WR, TE | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](32_completion_probability.md) |
| 33 | Expected YAC (xYAC) | WR, TE, RB | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](33_expected_yac_xyac.md) |
| 34 | Team Plays Per Game | ALL | ✅ Complete | Pro Football Reference | Yes (perfect) | [View](34_team_plays_per_game.md) |
| 35 | Neutral Script Pass Rate | WR, TE, RB | ✅ Complete | Advanced stats | Yes (estimation) | [View](35_neutral_script_pass_rate.md) |
| 36 | Team Red Zone Efficiency | ALL | ✅ Complete | TeamRankings / PFR | Yes (team stat) | [View](36_team_red_zone_efficiency.md) |
| 37 | Snap Share Trend | ALL | ✅ Complete | Derived (from M15) | Yes (perfect) | [View](37_snap_share_trend.md) |
| 38 | Dominator Rating | WR, TE (rookies) | ✅ Complete | Manual (defer) | N/A (draft only) | [View](38_dominator_rating.md) |
| 44 | EPA Per Target (TE) | TE | ✅ Complete | Premium (defer) | Limited | [View](44_epa_per_target_te.md) |
| 45 | Role Security (TE) | TE | ✅ Complete | Derived (M42+M15) | Yes (perfect) | [View](45_role_security_te.md) |
| 48 | Yards Before Contact (RB) | RB | ✅ Complete | NGS / PlayerProfiler | Yes (scraping) | [View](48_yards_before_contact_rb.md) |
| 55 | Target Depth Distribution (WR) | WR | ✅ Complete | Next Gen Stats | Yes (scraping) | [View](55_target_depth_distribution_wr.md) |
| 56 | Red Zone Involvement (WR) | WR | ✅ Complete | PFR / PP (same M7) | Yes (scraping) | [View](56_red_zone_involvement_wr.md) |
| 57 | 3rd Down Conversion Rate (WR) | WR | ✅ Complete | PFR (situational) | Yes (scraping) | [View](57_3rd_down_conversion_rate_wr.md) |
| 58 | Total Opportunity Share (WR) | WR | ✅ Complete | Derived (from M1) | Yes (perfect) | [View](58_total_opportunity_share_wr.md) |

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

- [x] **Phase 1 Complete:** All 14 HIGH priority metrics researched (14/14 = 100%)
- [x] **Phase 2 Complete:** All 15 MEDIUM priority metrics researched (15/15 = 100%)
- [x] **Phase 3 Complete:** All 29 LOW priority metrics researched (29/29 = 100%)
- [x] **All Research Complete:** 58/58 metrics documented (100%)

---

*This tracker is automatically maintained during the research phase. Last update: 2025-12-20*
