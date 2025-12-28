# Metrics Implementation Checklist

**Purpose:** Track implementation status of high-priority and position-specific metrics identified in `potential_metrics_from_player_data.md`

**Created:** 2025-12-27

**Total Metrics:** 11
- High Priority: 4 metrics
- Position-Specific: 7 metrics

---

## High Priority Implementable Metrics

### ✅ 1. Target Volume / Target Share (WR, TE, RB)

**Gap Analysis Reference:** Metric #1 (High Priority)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-01-target-volume.md`)
- [ ] Metric has been implemented

**Details:**
- Positions: WR, TE, RB
- Data Required: `receiving.targets` (weekly array)
- Team aggregation required for share calculation
- Expected bonus range: ±3.0 pts

---

### ✅ 2. Rushing Upside (Dual-Threat QBs)

**Gap Analysis Reference:** Metric #52 (QB Position-Specific)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-02-qb-rushing-upside.md`)
- [ ] Metric has been implemented

**Details:**
- Position: QB
- Data Required: `rushing.attempts`, `rushing.rush_yds`, `rushing.rush_tds`
- Expected bonus range: 0 to +4.0 pts (elite dual-threat)
- Additional bonus: +2.0 pts for ≥6 rush TDs

---

### ✅ 3. Pass Attempts Per Game (QB Volume)

**Gap Analysis Reference:** Metric #53 (QB Position-Specific)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-03-pass-attempts-per-game.md`)
- [ ] Metric has been implemented

**Details:**
- Position: QB
- Data Required: `passing.attempts` (weekly)
- Expected bonus range: ±2.5 pts
- Threshold: ≥40 attempts/game = EXCELLENT

---

### ✅ 4. Carries Per Game (RB Volume Floor)

**Gap Analysis Reference:** Metric #50 (RB Position-Specific)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-04-carries-per-game.md`)
- [ ] Metric has been implemented

**Details:**
- Position: RB
- Data Required: `rushing.attempts` (weekly)
- Expected bonus range: ±3.0 pts
- Threshold: ≥20 carries/game = EXCELLENT (bell cow)

---

## Position-Specific Metrics

### ✅ 5. Kicker Accuracy (Overall)

**Gap Analysis Reference:** Metric #40 (K Position-Specific, partial implementation)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-05-kicker-accuracy.md`)
- [ ] Metric has been implemented

**Details:**
- Position: K
- Data Required: `field_goals.made/missed`, `extra_points.made/missed`
- Expected bonus range: ±1.5 pts
- Limitation: No distance breakdown (0-39, 40-49, 50+ yards)

---

### ✅ 6. Completion Percentage (QB Efficiency)

**Gap Analysis Reference:** Related to Gap #2 (QB Context)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-06-completion-percentage.md`)
- [ ] Metric has been implemented

**Details:**
- Position: QB
- Data Required: `passing.completions`, `passing.attempts`
- Expected bonus range: ±1.5 pts
- Threshold: ≥70% = EXCELLENT

---

### ✅ 7. TD:INT Ratio (QB Efficiency)

**Gap Analysis Reference:** Not in gap analysis, but standard QB metric

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-07-td-int-ratio.md`)
- [ ] Metric has been implemented

**Details:**
- Position: QB
- Data Required: `passing.pass_tds`, `passing.interceptions`
- Expected bonus range: ±2.0 pts
- Threshold: ≥4.0 ratio = EXCELLENT

---

### ✅ 8. Yards Per Carry (RB Efficiency)

**Gap Analysis Reference:** Related to Gap #27 (Rush Yards Over Expected)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-08-yards-per-carry.md`)
- [ ] Metric has been implemented

**Details:**
- Position: RB
- Data Required: `rushing.rush_yds`, `rushing.attempts`
- Expected bonus range: ±2.0 pts
- Threshold: ≥5.0 YPC = EXCELLENT

---

### ✅ 9. Yards Per Reception (WR/TE Efficiency)

**Gap Analysis Reference:** Related to Gap #13 (Air Yards / aDOT)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-09-yards-per-reception.md`)
- [ ] Metric has been implemented

**Details:**
- Position: WR, TE
- Data Required: `receiving.receiving_yds`, `receiving.receptions`
- Expected bonus range: ±1.5 pts
- Threshold: ≥15.0 YPR (WR), ≥12.0 YPR (TE) = EXCELLENT

---

### ✅ 10. Catch Rate (WR/TE/RB Efficiency)

**Gap Analysis Reference:** Related to Gap #30 (True Catch Rate)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-10-catch-rate.md`)
- [ ] Metric has been implemented

**Details:**
- Position: WR, TE, RB
- Data Required: `receiving.receptions`, `receiving.targets`
- Expected bonus range: ±1.5 pts
- Threshold: ≥75% = EXCELLENT (reliable hands)

---

### ✅ 11. Receiving Workload (RB Pass-Catching Role)

**Gap Analysis Reference:** Related to Gap #21 (Opportunity Share)

**Status:**
- [x] Feature Request file created (`feature-updates/new_metrics/metric-11-rb-receiving-workload.md`)
- [ ] Metric has been implemented

**Details:**
- Position: RB
- Data Required: `receiving.targets`, `receiving.receptions`, `receiving.receiving_yds`
- Expected bonus range: ±2.5 pts
- Threshold: ≥8 targets/game = EXCELLENT (pass-catching specialist)

---

## Summary

**Total Progress:**
- [x] 11/11 Feature Request files created (100%)
- [ ] 0/11 Metrics implemented (0%)

**Implementation Priority:**
1. Metrics 1-4 (High Priority): Critical for improving player valuation
2. Metrics 5-11 (Position-Specific): Enhance position-specific accuracy

**Expected Overall Impact:**
- Add To Roster Mode: 12-18% improvement
- Starter Helper Mode: 15-20% improvement
- Trade Simulator Mode: 15-22% improvement

---

## Notes

- All metrics can be implemented with data from `data/player_data/*.json` files
- Some metrics require team-level aggregation (target share, opportunity share)
- See `potential_metrics_from_player_data.md` for complete implementation details
- Configuration structure proposals provided in potential metrics document
- Unit tests required for all calculations before marking as implemented
- **Additional Feature Requests:** M17 (Target Share Trend) also created in `feature-updates/new_metrics/` folder
- **Quick Reference:** See `feature-updates/new_metrics/README_REMAINING_METRICS.md` for abbreviated specs

---

## Cross-References

- **Source Analysis:** `docs/research/potential_metrics_from_player_data.md`
- **Gap Analysis:** `docs/research/scoring_gap_analysis.md`
- **Player Data:** `data/player_data/*.json`
- **Current Scoring Steps:** `docs/scoring/README.md` (Steps 1-13)
