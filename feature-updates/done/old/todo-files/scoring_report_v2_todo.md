# Scoring Report V2 - TODO Tracking

**Objective**: Create comprehensive, independently verified scoring documentation in `docs/scoring_v2`

**Status**: Draft - Verification In Progress

---

## Phase 1: Setup and Research

### 1.1 Initial Setup
- [ ] Create `docs/scoring_v2` directory
- [ ] Create README.md with overview and table of contents

### 1.2 Identify All Scoring Metrics
Current scoring metrics (based on existing docs/scoring):
1. Normalization (01)
2. ADP Multiplier (02)
3. Player Rating Multiplier (03)
4. Team Quality Multiplier (04)
5. Performance Multiplier (05)
6. Matchup Multiplier (06)
7. Schedule Multiplier (07)
8. Draft Order Bonus (08)
9. Bye Week Penalty (09)
10. Injury Penalty (10)

### 1.3 Identify Key Files for Analysis
- `league_helper/util/PlayerManager.py` - Main scoring orchestration
- `league_helper/util/player_scoring.py` - Scoring calculations
- `league_helper/util/ScoredPlayer.py` - Scored player model
- `league_helper/util/ConfigManager.py` - Configuration/multiplier lookup
- `league_helper/util/TeamDataManager.py` - Team rankings data
- `player-data-fetcher/espn_client.py` - ESPN API integration
- `player-data-fetcher/player_data_exporter.py` - Data export logic
- `data/players.csv` - Main player data
- `data/players_projected.csv` - Projected player data
- `data/team_data/` - Team rankings by week

---

## Phase 2: Create Individual Metric Reports

For EACH metric, create a report covering:
1. What modes use the metric
2. How value/multiplier is obtained
3. Calculations involved
4. Data sources (which CSV columns)
5. How player data fetcher populates the data
6. ESPN API JSON analysis
7. Examples with top 20 players per position

### 2.1 Normalization Report
- [ ] Analyze PlayerManager for normalization logic
- [ ] Document mode usage
- [ ] Trace data flow from players.csv
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/01_normalization.md`

### 2.2 ADP Multiplier Report
- [ ] Analyze ConfigManager.get_adp_multiplier()
- [ ] Document mode usage
- [ ] Trace ADP data source (players.csv column)
- [ ] Analyze ESPN API for ADP data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/02_adp_multiplier.md`

### 2.3 Player Rating Multiplier Report
- [ ] Analyze ConfigManager.get_player_rating_multiplier()
- [ ] Document mode usage
- [ ] Trace player rating data source
- [ ] Analyze ESPN API for rating data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/03_player_rating_multiplier.md`

### 2.4 Team Quality Multiplier Report
- [ ] Analyze TeamDataManager usage
- [ ] Document mode usage
- [ ] Trace team quality data source
- [ ] Analyze ESPN API for team data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/04_team_quality_multiplier.md`

### 2.5 Performance Multiplier Report
- [ ] Analyze performance calculation logic
- [ ] Document mode usage
- [ ] Trace actual vs projected data sources
- [ ] Analyze ESPN API for performance data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/05_performance_multiplier.md`

### 2.6 Matchup Multiplier Report
- [ ] Analyze matchup calculation logic
- [ ] Document mode usage
- [ ] Trace opponent strength data sources
- [ ] Analyze ESPN API for matchup data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/06_matchup_multiplier.md`

### 2.7 Schedule Multiplier Report
- [ ] Analyze schedule calculation logic
- [ ] Document mode usage
- [ ] Trace future opponent data sources
- [ ] Analyze ESPN API for schedule data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/07_schedule_multiplier.md`

### 2.8 Draft Order Bonus Report
- [ ] Analyze draft order bonus logic
- [ ] Document mode usage
- [ ] Trace position-specific bonus data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/08_draft_order_bonus.md`

### 2.9 Bye Week Penalty Report
- [ ] Analyze bye week penalty logic
- [ ] Document mode usage
- [ ] Trace bye week data sources
- [ ] Analyze ESPN API for bye week data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/09_bye_week_penalty.md`

### 2.10 Injury Penalty Report
- [ ] Analyze injury penalty logic
- [ ] Document mode usage
- [ ] Trace injury status data sources
- [ ] Analyze ESPN API for injury data
- [ ] Document calculations
- [ ] Create examples
- [ ] Write `docs/scoring_v2/10_injury_penalty.md`

---

## Phase 3: Create Overview Documentation

### 3.1 Main README
- [ ] Create scoring algorithm overview
- [ ] Document flow diagram showing all metrics
- [ ] List mode dependencies
- [ ] Add table of contents with links

### 3.2 Data Sources Summary
- [ ] Document all CSV file structures
- [ ] Map ESPN API endpoints to data fields
- [ ] Create data flow diagram

---

## Phase 4: Validation and Finalization

### 4.1 Cross-Reference Validation
- [ ] Compare all reports against actual code
- [ ] Verify examples with real player data
- [ ] Ensure no references to old documentation

### 4.2 Final Review
- [ ] Run unit tests to ensure nothing broken
- [ ] Verify all 10 metric reports complete
- [ ] Ensure documentation is standalone and independent

---

## Verification Summary

**Iterations Completed**: 5/5 (First Round Complete)

**Requirements Coverage**:
- [x] Report per metric in docs/scoring_v2 - 10 metrics identified
- [x] Mode usage documented for each metric - All 4 modes analyzed
- [x] Value/multiplier acquisition documented - ConfigManager methods mapped
- [x] Calculations documented - 10-step algorithm verified
- [x] Data sources traced - players.csv, team_data/*.csv, season_schedule.csv
- [x] ESPN API analysis included - All JSON paths identified
- [ ] Examples with top 20 players per position - Requires implementation

**Key Files Verified**:
- `league_helper/util/player_scoring.py` - Main 10-step algorithm
- `league_helper/util/ConfigManager.py` - All multiplier/penalty getters
- `league_helper/util/TeamDataManager.py` - Team rankings (rolling windows)
- `league_helper/util/SeasonScheduleManager.py` - Schedule data
- `league_helper/util/ProjectedPointsManager.py` - Projected points for performance calc
- `player-data-fetcher/espn_client.py` - ESPN API extraction (lines 1839-1981)
- `player-data-fetcher/fantasy_points_calculator.py` - Weekly projections

**Verified Mode Usage**:
1. **Add To Roster**: adp=T, player_rating=T, team_quality=T, performance=F, matchup=F, schedule=F, draft_round=N, bye=T, injury=T
2. **Starter Helper**: adp=F, player_rating=F, team_quality=T, performance=T, matchup=T, schedule=F, bye=F, injury=F, weekly=T
3. **Trade Simulator (User)**: adp=F, player_rating=T, team_quality=T, performance=T, matchup=F, schedule=T, bye=T, injury=F
4. **Trade Simulator (Opponent)**: Same as User but bye=F

**Critical Finding**: The algorithm is 10 steps, NOT 9 (docs say 9). Consistency is calculated but NOT used as a step.

**Risk Areas**:
- Performance multiplier uses ProjectedPointsManager for pre-season projections (players_projected.csv)
- Team rankings use rolling window (MIN_WEEKS=5) - early weeks get neutral rankings
- Player rating logic differs pre-season (draftRanksByRankType) vs during season (rankings consensus)

---

## User Answers (Recommended Options Selected)

1. **Report Depth**: A - Comprehensive (full technical documentation)
2. **Examples**: C - Both (simplified + real player examples)
3. **Step Numbering**: A - Use correct 10-step numbering
4. **Mode Coverage**: C - Both (in each report + table in README)
5. **ESPN API**: A - Full JSON structure and paths
6. **Simulation**: A - League Helper only (4 main modes)
7. **Config Params**: B - Key thresholds only
8. **Projected Data**: B - Comparison only
9. **Reserve Mode**: A - Include all modes that use scoring
10. **File Organization**: A - Same structure (01-10 numbered files)

---

## Progress Notes

*Keep this section updated as work progresses*

**Session 1** (Initial):
- Created draft TODO file
- Completed 5 verification iterations
- Created questions file
- User selected all recommended answers
- Beginning implementation

---

## IMPORTANT: Maintain This File

If a new Claude agent continues this work:
1. Review this TODO file completely
2. Check current phase/step progress
3. Continue from where previous session left off
4. Update progress notes with session number
