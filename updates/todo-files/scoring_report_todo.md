# Scoring Report v2 Documentation - TODO

## Objective
Create comprehensive, independently verified scoring documentation in `docs/scoring_v2/` that covers all 10 scoring metrics with detailed analysis of data flow, ESPN API integration, and calculation examples.

---

## Phase 1: Setup and Research Foundation

### 1.1 Create Documentation Structure
- [ ] Create `docs/scoring_v2/` directory
- [ ] Create README.md with scoring overview

### 1.2 Core Scoring Research
- [ ] Analyze `league_helper/util/player_scoring.py` for scoring calculations
- [ ] Analyze `league_helper/util/ConfigManager.py` for multiplier/penalty retrieval
- [ ] Map which modes use which metrics
- [ ] Document data flow from ESPN API to final score

---

## Phase 2: Individual Metric Reports

For each metric, create a report covering:
1. Mode usage analysis
2. Value/multiplier retrieval
3. Calculation details
4. Data source tracing (players.csv, etc.)
5. ESPN API data mapping
6. Top 20 player examples per position

### 2.1 Normalization (01)
- [ ] Research normalization in player_scoring.py
- [ ] Document calculation formula
- [ ] Create `docs/scoring_v2/01_normalization.md`

### 2.2 ADP Multiplier (02)
- [ ] Research ADP multiplier logic
- [ ] Trace ADP data from ESPN API
- [ ] Document config thresholds
- [ ] Create `docs/scoring_v2/02_adp_multiplier.md`

### 2.3 Player Rating Multiplier (03)
- [ ] Research player rating logic
- [ ] Trace rating data source
- [ ] Create `docs/scoring_v2/03_player_rating_multiplier.md`

### 2.4 Team Quality Multiplier (04)
- [ ] Research team quality calculations
- [ ] Trace team data from ESPN API
- [ ] Create `docs/scoring_v2/04_team_quality_multiplier.md`

### 2.5 Performance Multiplier (05)
- [ ] Research actual vs projected logic
- [ ] Trace performance data sources
- [ ] Create `docs/scoring_v2/05_performance_multiplier.md`

### 2.6 Matchup Multiplier (06)
- [ ] Research current opponent strength logic
- [ ] Trace team matchup data
- [ ] Create `docs/scoring_v2/06_matchup_multiplier.md`

### 2.7 Schedule Multiplier (07)
- [ ] Research future opponent strength logic
- [ ] Trace schedule data
- [ ] Create `docs/scoring_v2/07_schedule_multiplier.md`

### 2.8 Draft Order Bonus (08)
- [ ] Research draft position bonus logic
- [ ] Document position-specific values
- [ ] Create `docs/scoring_v2/08_draft_order_bonus.md`

### 2.9 Bye Week Penalty (09)
- [ ] Research bye week penalty logic
- [ ] Trace bye week data source
- [ ] Create `docs/scoring_v2/09_bye_week_penalty.md`

### 2.10 Injury Penalty (10)
- [ ] Research injury penalty logic
- [ ] Trace injury status from ESPN API
- [ ] Create `docs/scoring_v2/10_injury_penalty.md`

---

## Phase 3: ESPN API Analysis

### 3.1 API Response Documentation
- [ ] Analyze `player-data-fetcher/espn_client.py` for API calls
- [ ] Document JSON response structures
- [ ] Map API fields to players.csv columns
- [ ] Document team data API responses

---

## Phase 4: Examples and Validation

### 4.1 Generate Examples
- [ ] Load current player data
- [ ] Calculate examples for top 20 players per position
- [ ] Include step-by-step calculation walkthrough

### 4.2 Cross-Reference Verification
- [ ] Verify calculations match actual code behavior
- [ ] Validate data source documentation

---

## Phase 5: Final Documentation

### 5.1 Complete README
- [ ] Write comprehensive scoring_v2 README
- [ ] Include flow diagram
- [ ] Document mode dependencies

### 5.2 Run Tests
- [ ] Run `python tests/run_all_tests.py`
- [ ] Ensure 100% pass rate

---

## Verification Summary (Iterations 1-5)

### Key Findings from Codebase Research:

**Core Files Identified:**
- `league_helper/util/player_scoring.py` - Main 10-step scoring algorithm (PlayerScoringCalculator class)
- `league_helper/util/ConfigManager.py` - Multiplier/penalty retrieval and thresholds
- `player-data-fetcher/espn_client.py` - ESPN API integration (2139 lines)
- `league_helper/util/PlayerManager.py` - Player data management

**Mode Usage Analysis (score_player calls):**
- `AddToRosterModeManager.py` - Draft helper mode
- `StarterHelperModeManager.py` - Roster optimizer mode
- `TradeSimTeam.py` / `trade_analyzer.py` - Trade evaluation mode
- `SimulatedOpponent.py` - Simulation system

**10 Scoring Metrics Confirmed:**
1. Normalization (`_get_normalized_fantasy_points`)
2. ADP Multiplier (`_apply_adp_multiplier`)
3. Player Rating Multiplier (`_apply_player_rating_multiplier`)
4. Team Quality Multiplier (`_apply_team_quality_multiplier`)
5. Performance Multiplier (`_apply_performance_multiplier`)
6. Matchup Multiplier (`_apply_matchup_multiplier`)
7. Schedule Multiplier (`_apply_schedule_multiplier`)
8. Draft Order Bonus (`_apply_draft_order_bonus`)
9. Bye Week Penalty (`_apply_bye_week_penalty`)
10. Injury Penalty (`_apply_injury_penalty`)

**ESPN API Data Sources:**
- Season projections: `kona_player_info` view
- Team rankings: Rolling window from scoreboard API
- Player ratings: `rankings` object with `averageRank` field
- Weekly projections: `stats` array with `appliedTotal`/`projectedTotal`
- ADP: `ownership.averageDraftPosition`
- Injury status: `injuryStatus` field

**Complexity Assessment:**
- Each metric requires ~500-1000 lines of documentation
- ESPN API JSON structures are complex (nested stats, rankings by week)
- Top 20 per position examples require actual data processing
- Estimated total: 5,000-10,000 lines across all reports

---

## Progress Tracking
Update this section as work progresses. Mark items complete with [x].

**Current Status**: Completed 5 verification iterations, creating questions file
