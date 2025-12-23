# ESPN API Metric Research - Specification

**Last Updated:** 2025-12-19
**Status:** Planning - Phase 1 Complete

---

## Objective

Systematically research all 58 metrics identified in `docs/research/scoring_gap_analysis.md` (v3.0) to determine:
1. Data availability (existing data, ESPN API, free alternatives)
2. **Historical data availability for simulation validation**
3. Implementation complexity
4. Recommendation (pursue or skip)

**Output:** Comprehensive research document for each metric in `docs/research/potential_metrics/` to inform implementation decisions.

---

## High-Level Requirements (From Notes)

### 1. Research Scope

**Total Metrics:** 58
- Section 1: Original gap metrics (1-11)
- Section 2: Additional review metrics (12-19)
- Section 3: Projection calculation metrics (20-38)
- Section 4: Position-specific metrics (39-58) - NEW as of Dec 17, 2025

### 2. Research Document Structure

Each metric document must answer 7 questions **IN THIS ORDER:**

1. **Existing Data:** Can it be calculated from current `data/` folder?
2. **ESPN API:** Is it available via ESPN Fantasy Football API?
3. **Free Alternatives:** What other free sources exist?
4. **Data Quality:** How reliable/accurate? Update frequency?
5. **CRITICAL - Historical Data:** Can we get weekly snapshots for `simulation/sim_data/{YEAR}/weeks/week_{NN}/`?
6. **Implementation Complexity:** Work required, dependencies, data structure fit
7. **Recommendation:** Should we pursue? Preferred source? Historical data feasibility?

### 3. Historical Data Requirements

**Structure:** `simulation/sim_data/{YEAR}/weeks/week_{NN}/`
- Each week folder: `players.csv`, `players_projected.csv`
- Year-level: `game_data.csv`, `season_schedule.csv`, `team_data/{TEAM}.csv`

**Format Options:**
- Add columns to existing files (players.csv, players_projected.csv, team_data/*.csv)
- Create new weekly snapshot files (if doesn't fit existing structure)

**Timing:** "What we knew going INTO that week" (predictive, not retrospective)

**Example:** `week_05/` snapshot should have:
- Weeks 1-4: ACTUAL metric values
- Weeks 5-17: PROJECTED metric values

### 4. Output Location

`docs/research/potential_metrics/{metric_number}_{metric_name}.md`

Examples:
- `01_target_volume.md`
- `39_team_rz_td_percentage.md`
- `52_rushing_upside_qb.md`

### 5. Research Priority

**Phase 1 (HIGH):** 14 metrics
- Original: 1, 2, 4, 12, 21, 22
- Position-Specific: 39, 40, 42, 46, 49, 50, 52, 53

**Phase 2 (MEDIUM):** 15 metrics

**Phase 3 (LOW):** 29 metrics

---

## Reference Documents

### Primary Source
- `docs/research/scoring_gap_analysis.md` (v3.0, updated Dec 17, 2025)
  - Contains all 58 metric definitions
  - Includes thresholds, position applicability, implementation suggestions

### ESPN API Documentation
- `docs/espn/espn_api_endpoints.md` - API endpoint documentation
- `docs/espn/espn_player_data.md` - Player field reference
- `docs/espn/espn_team_data.md` - Team field reference
- `docs/espn/espn_api_reference_tables.md` - ID mappings

### Existing Data Files
- `data/players.csv` - Current player stats
- `data/players_projected.csv` - Player projections
- `data/game_data.csv` - Game-level data
- `data/team_data/{TEAM}.csv` - Per-team stats (32 teams)
- `data/season_schedule.csv` - Full season schedule
- `data/configs/*.json` - Configuration settings

### Historical Data
- `simulation/sim_data/2021/` - 2021 season snapshots
- `simulation/sim_data/2022/` - 2022 season snapshots
- `simulation/sim_data/2024/` - 2024 season snapshots

---

## Data Sources to Investigate

### Primary
1. **Existing Data Files** - Check `data/` folder first
2. **ESPN Fantasy API** - Main target for new data
3. **Free Alternatives** - If ESPN doesn't provide

### Free Data Sources to Research
- NFL Official Stats API
- Pro Football Reference (check terms of use)
- The Odds API (free tier for Vegas lines)
- nfelo.com (EPA data)
- Next Gen Stats (limited public access)
- Football Outsiders (DVOA - check free vs paid tier)
- Player Profiler (true catch rate, dominator rating)
- PFF (route participation, coverage data - check free vs paid)

### Historical Data Sources
1. ESPN API historical endpoints (if available)
2. Pro Football Reference (week-by-week game logs, exportable CSV)
3. Archived snapshots (Wayback Machine, archived fantasy sites)
4. PFF historical data (check free tier access)

---

## Current Column Structure (For Integration Planning)

### players.csv / players_projected.csv
```
id, name, team, position, bye_week, drafted, locked,
fantasy_points, average_draft_position, player_rating, injury_status,
week_1_points, week_2_points, ..., week_17_points
```

### team_data/{TEAM}.csv
```
week, pts_allowed_to_QB, pts_allowed_to_RB, pts_allowed_to_WR,
pts_allowed_to_TE, pts_allowed_to_K, points_scored, points_allowed
```

**New metrics must:**
- Add columns to existing files OR
- Create new weekly snapshot files

---

## Open Questions

*To be populated during Phase 2 - Investigation*

### Research Methodology

**Q1.1 - Research Document Template:** RESOLVED
- Using standardized template approach (Option C)
- Template structure based on 7 mandatory questions
- Will be created at `docs/research/potential_metrics/TEMPLATE.md`
- Ensures consistency across all 58 metric documents

**Q1.2 - Mandatory vs Optional Sections:** RESOLVED
- **8 Mandatory Sections:**
  1. Position Applicability header (QB/RB/WR/TE/K or "All positions")
  2. Existing Data Analysis
  3. ESPN API Availability
  4. Free Alternative Sources
  5. Data Quality Assessment (includes reliability, accuracy, update frequency, limitations)
  6. Historical Data Availability (CRITICAL)
  7. Implementation Complexity
  8. Recommendation
- **Skipped Sections:** Executive Summary (redundant with Recommendation), Implementation Examples (belongs in implementation phase)
- **Integrated:** Limitations section merged into Data Quality Assessment

### Data Sources
- (Pending)

### Historical Data Strategy
- (Pending)

### Implementation Workflow
- (Pending)

---

## Resolved Implementation Details

**ALL 47 CHECKLIST ITEMS RESOLVED - 2025-12-20**

See `RESOLUTION_DECISIONS.md` for complete details (456 lines). Key decisions summarized below:

### Research Template & Structure
- Standardized template with 8 mandatory sections
- File naming: `{number}_{name}.md` (e.g., `01_target_volume.md`)
- Moderate documentation level for "not available" findings
- No code examples in research phase

### Data Verification Approach
- ESPN API: Documentation review + spot checks for HIGH priority metrics
- Free alternatives: Minimum 2-3 researched per metric
- Historical data: 1 season minimum, 4-week sample verification
- Data quality: Documentation review sufficient

### Research Workflow
- Priority order: HIGH (14) → MEDIUM (15) → LOW (29)
- Progress tracking: RESEARCH_PROGRESS.md summary document
- No fixed timeline, quality over speed
- Single researcher for consistency

### Documentation Standards
- 8 mandatory sections per metric
- Position applicability header
- Schema definition in Implementation Complexity
- Research date versioning

### Integration
- Research informs separate implementation feature
- Document dependencies between metrics
- Reference existing patterns, don't design new ones
- Keep research docs independent

---

## Assumptions

*To be documented during Phase 2 - Investigation*

### Example Format:
| Assumption | Basis | Risk if Wrong | Mitigation |
|------------|-------|---------------|------------|
| (TBD) | (TBD) | (TBD) | (TBD) |

---

## Dependency Map

*To be created during Phase 2 - Investigation*

### Module Dependencies
```
(To be documented)
```

### Data Flow
```
(To be documented)
```

---

## Out of Scope

- Implementation of metrics (this is research only)
- Creating data fetchers for metrics
- Modifying scoring algorithm
- Running accuracy simulations with new metrics

**Next Phase:** Implementation of selected metrics (separate feature)

---

## Notes

- Research should prioritize metrics with both live usage value AND historical data availability
- Metrics without historical data can still be valuable for live season usage
- Consider creating "live-only" vs "simulation-validated" metric tiers
