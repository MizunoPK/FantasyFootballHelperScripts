# ESPN API Metric Research - Phase 2: HIGH Priority Research

**Sub-Feature:** HIGH Priority Metrics Research (14 metrics)
**Created:** 2025-12-20
**Status:** Pre-Implementation (Starting 24 verification iterations)

---

## Purpose

Research 14 HIGH priority metrics to determine:
1. Data availability (existing, ESPN API, free alternatives)
2. **Historical data availability** (CRITICAL for simulation validation)
3. Implementation complexity
4. Recommendation (pursue/defer/skip)

These are the highest-value metrics that should be implemented first.

---

## Iteration Progress Tracker

**First Round (7 iterations):**
- [ ] 1. Files & Patterns
- [ ] 2. Error Handling
- [ ] 3. Integration Points
- [ ] 4. Algorithm Traceability Matrix
- [ ] 5. End-to-End Data Flow
- [ ] 6. Skeptical Re-verification
- [ ] 7. Integration Gap Check

**Second Round (9 iterations):**
- [ ] 8. Answer Integration
- [ ] 9. Answer Verification
- [ ] 10. Dependency Check
- [ ] 11. Algorithm Re-verify
- [ ] 12. Data Flow Re-trace
- [ ] 13. Assumption Re-check
- [ ] 14. Caller Re-check
- [ ] 15. Final Preparation
- [ ] 16. Integration Checklist

**Third Round (8 iterations):**
- [ ] 17. Fresh Eyes #1
- [ ] 18. Fresh Eyes #2
- [ ] 19. Algorithm Deep Dive
- [ ] 20. Edge Cases
- [ ] 21. Test Planning
- [ ] 22. Final Assumption Check
- [ ] 23. Final Caller Check
- [ ] 24. Readiness Check

---

## HIGH Priority Metrics (14 Total)

### Metric 1: Target Volume/Share
**Position:** WR, TE, RB
**Why HIGH:** Critical for weekly decisions
**Research Doc:** `docs/research/potential_metrics/01_target_volume.md`
**Status:** ⏳ Pending

### Metric 2: QB Context/Quality Score
**Position:** WR, TE
**Why HIGH:** Affects all pass-catchers
**Research Doc:** `docs/research/potential_metrics/02_qb_context.md`
**Status:** ⏳ Pending

### Metric 4: Vegas Lines/Game Environment
**Position:** ALL
**Why HIGH:** Game environment predictor
**Research Doc:** `docs/research/potential_metrics/04_vegas_lines.md`
**Status:** ⏳ Pending

### Metric 12: Implied Team Total
**Position:** ALL
**Why HIGH:** More precise than O/U
**Research Doc:** `docs/research/potential_metrics/12_implied_team_total.md`
**Status:** ⏳ Pending

### Metric 21: WOPR (Weighted Opportunity Rating)
**Position:** WR, TE
**Why HIGH:** Weighted opportunity metric
**Research Doc:** `docs/research/potential_metrics/21_wopr.md`
**Status:** ⏳ Pending

### Metric 22: Expected Fantasy Points (xFP)
**Position:** ALL
**Why HIGH:** Expected fantasy points baseline
**Research Doc:** `docs/research/potential_metrics/22_expected_fantasy_points.md`
**Status:** ⏳ Pending

### Metric 39: Team Red Zone TD% (K-specific)
**Position:** K
**Why HIGH:** K scoring differential
**Research Doc:** `docs/research/potential_metrics/39_team_rz_td_percentage.md`
**Status:** ⏳ Pending

### Metric 40: Kicker Accuracy by Distance
**Position:** K
**Why HIGH:** 2025 record accuracy
**Research Doc:** `docs/research/potential_metrics/40_kicker_accuracy_by_distance.md`
**Status:** ⏳ Pending

### Metric 42: Route Participation Rate (TE)
**Position:** TE
**Why HIGH:** TE usage indicator
**Research Doc:** `docs/research/potential_metrics/42_route_participation_rate.md`
**Status:** ⏳ Pending

### Metric 46: Goal-Line Role (RB)
**Position:** RB
**Why HIGH:** TD equity determinant
**Research Doc:** `docs/research/potential_metrics/46_goal_line_role.md`
**Status:** ⏳ Pending

### Metric 49: Role Designation (RB Workload)
**Position:** RB
**Why HIGH:** Workload security
**Research Doc:** `docs/research/potential_metrics/49_role_designation.md`
**Status:** ⏳ Pending

### Metric 50: Receiving Share (RB)
**Position:** RB
**Why HIGH:** Pass-catching RB value
**Research Doc:** `docs/research/potential_metrics/50_receiving_share.md`
**Status:** ⏳ Pending

### Metric 52: Pass Block Rate (QB Protection)
**Position:** QB
**Why HIGH:** QB protection quality
**Research Doc:** `docs/research/potential_metrics/52_pass_block_rate.md`
**Status:** ⏳ Pending

### Metric 53: Pressure Rate (QB)
**Position:** QB
**Why HIGH:** QB performance under pressure
**Research Doc:** `docs/research/potential_metrics/53_pressure_rate.md`
**Status:** ⏳ Pending

---

## Research Workflow

For each metric:

1. **Use TEMPLATE.md** to create research document
2. **Research 7 key questions:**
   - Existing data analysis
   - ESPN API availability
   - Free alternative sources (minimum 2-3)
   - Data quality assessment
   - **Historical data availability** (CRITICAL)
   - Implementation complexity
   - Recommendation
3. **Update RESEARCH_PROGRESS.md** after completion
4. **Save document** in `docs/research/potential_metrics/`

---

## Data Sources to Check

### For Each Metric:

**Existing Data:**
- `data/players.csv` - Player stats and projections
- `data/team_data/{TEAM}.csv` - Team statistics
- `data/game_data.csv` - Game-level data
- `simulation/sim_data/{YEAR}/weeks/week_{NN}/` - Historical snapshots

**ESPN API:**
- `docs/espn/espn_player_data.md` - Player data reference
- `docs/research/ESPN_NFL_Game_Data_Research_Report.md` - Game data reference
- ESPN API endpoints documentation

**Free Alternatives (minimum 2-3 per metric):**
- NFL Official Stats API
- Pro Football Reference
- The Odds API (for Vegas lines)
- nfelo.com (EPA data)
- Next Gen Stats
- Other position-specific sources

**Historical Data:**
- Must verify weekly snapshots available for at least 1 season
- Ideal: 3 seasons (2021, 2022, 2024)
- Data must be predictive (what we knew going INTO that week)

---

## Protocol Execution Tracker

### Algorithm Traceability Matrix (Iterations 4, 11, 19)
*No algorithms - this is research/documentation, not calculations*

### End-to-End Data Flow (Iterations 5, 12)
```
Input: 14 HIGH priority metrics from scoring_gap_analysis.md
  ↓
For each metric:
  - Use TEMPLATE.md structure
  - Research 7 key questions
  - Document findings
  - Save to docs/research/potential_metrics/
  - Update RESEARCH_PROGRESS.md
  ↓
Output: 14 completed research documents
```

### Integration Matrix (Iterations 7, 14, 23)

| New Component | Caller/Consumer | Integration Point |
|---------------|-----------------|-------------------|
| Metric research docs | Future implementation phases | Specifications for data fetching/calculation |
| RESEARCH_PROGRESS.md updates | Users/agents | Track completion status |
| Recommendations | Implementation prioritization | Decision on pursue/defer/skip |

---

## Progress Tracking

**Completion Tracker:**
- [ ] Metric 1: Target Volume/Share
- [ ] Metric 2: QB Context
- [ ] Metric 4: Vegas Lines
- [ ] Metric 12: Implied Team Total
- [ ] Metric 21: WOPR
- [ ] Metric 22: xFP
- [ ] Metric 39: Team RZ TD%
- [ ] Metric 40: Kicker Accuracy
- [ ] Metric 42: Route Participation
- [ ] Metric 46: Goal-Line Role
- [ ] Metric 49: Role Designation
- [ ] Metric 50: Receiving Share
- [ ] Metric 52: Pass Block Rate
- [ ] Metric 53: Pressure Rate

**Progress:** 0/14 metrics researched (0%)

---

## Dependencies

**Source Documents:**
- `docs/research/scoring_gap_analysis.md` (Version 3.0) - Metric definitions
- `docs/research/potential_metrics/TEMPLATE.md` - Research template
- `docs/research/potential_metrics/RESEARCH_PROGRESS.md` - Progress tracker
- `feature-updates/espn-api-metric-research/RESOLUTION_DECISIONS.md` - Methodology

**Output Location:**
- `docs/research/potential_metrics/{number}_{name}.md` - Research documents

---

## Questions for User

*No questions - all methodology decisions resolved in RESOLUTION_DECISIONS.md*

**Proceed with research?** This phase involves creating 14 detailed research documents. Each will require:
- Checking existing data sources
- Reviewing ESPN API documentation
- Researching 2-3 free alternatives
- Assessing historical data availability
- Documenting findings in standardized format

Estimated effort: Significant research time (this is a research-intensive phase, not coding)

---

## Implementation Notes

**This is a RESEARCH phase, not a coding phase:**
- No Python code will be written
- No data fetchers created
- No schema modifications
- Pure documentation/research effort

**Output:**
- 14 comprehensive research documents
- Updated progress tracker
- Clear recommendations for each metric

---

## Progress Notes

**Last Updated:** 2025-12-20
**Current Status:** Created TODO, ready to start verification iterations
**Next Steps:** Complete 24 verification iterations, then begin research
**Blockers:** None

---

## Integration Checklist

- [ ] TEMPLATE.md exists and is complete
- [ ] RESEARCH_PROGRESS.md exists and has all 58 metrics
- [ ] scoring_gap_analysis.md has definitions for all 14 metrics
- [ ] ESPN API documentation available for reference
- [ ] Free alternative sources identified in RESOLUTION_DECISIONS.md

---

## Quality Control Plan

### After Each Metric:
1. Verify all 7 sections completed
2. Verify minimum 2-3 free alternatives researched
3. Verify historical data assessment included
4. Verify clear recommendation provided
5. Update RESEARCH_PROGRESS.md

### After All 14 Metrics:
1. Review for consistency across documents
2. Verify all historical data assessments thorough
3. Verify recommendations actionable
4. Create summary of pursue/defer/skip counts
5. Commit changes

---

*Pre-implementation verification to begin: 2025-12-20*
