# New Metrics Ideas - Research Document

**Created:** 2026-01-20
**Updated:** 2026-01-20
**Purpose:** Brainstorm and evaluate potential new fantasy football metrics for implementation
**Status:** Ideas only - no individual metric requests created yet

---

## Duplicate Removal Summary

The following metrics were **removed** as duplicates of existing implementations:

| Removed | Reason |
|---------|--------|
| M31: Opponent Pass Defense Ranking | Already in Step 6 Matchup Multiplier (uses pts_allowed_to_WR/TE) |
| M32: Opponent Run Defense Ranking | Already in Step 6 Matchup Multiplier (uses pts_allowed_to_RB) |
| M33: Weather Impact Score | Already in Steps 11-12 (Temperature/Wind Scoring) |
| M49: Indoor/Dome Kicker Boost | Already covered by Steps 11-12 (indoor games = no weather penalty) |

**Remaining new metrics:** 34 ideas (down from 38)
- 13 can be implemented now (data available)
- 3 can be approximated (partial data)
- 18 require new data sources

---

## Available Data Summary

Based on examination of `data/player_data/*.json`, `data/game_data.csv`, and `data/historical_data/*/team_data/*.csv`:

### Player Data Available (Weekly Arrays)

| Category | Fields | Positions |
|----------|--------|-----------|
| **Passing** | completions, attempts, pass_yds, pass_tds, interceptions, sacks | QB |
| **Rushing** | attempts, rush_yds, rush_tds | QB, RB, WR |
| **Receiving** | targets, receptions, receiving_yds, receiving_tds | RB, WR, TE |
| **Kicking** | field_goals.made/missed, extra_points.made/missed | K |
| **Defense** | sacks, interceptions, fumbles_recovered, forced_fumble, def_td, pts_g, yds_g, safety, ret_yds | DST |
| **Meta** | projected_points, actual_points, average_draft_position, player_rating, team, bye_week, injury_status | All |

### Game/Team Data Available

| Source | Fields |
|--------|--------|
| **game_data.csv** | week, home_team, away_team, temperature, gust, precipitation, scores, indoor, neutral_site, location |
| **team_data/{TEAM}.csv** | week, pts_allowed_to_QB/RB/WR/TE/K, points_scored, points_allowed |

### Data NOT Available

- Snap counts / snap percentage
- Red zone targets / carries
- Air yards / Average Depth of Target (aDOT)
- Yards After Catch (YAC)
- Routes run / Route participation
- Slot vs outside alignment
- Broken tackles / Missed tackles forced
- EPA / Success rate
- Pressure rate / QB hits
- Goal-line specific carries
- Offensive line grades

---

## Already Implemented (docs/scoring - 13 Steps)

The following scoring adjustments are **already implemented** in the 13-step scoring algorithm:

| Step | Implementation | Notes |
|------|---------------|-------|
| Step 1 | Base Scoring Normalization | ADP-based initial scores |
| Step 2 | Base Multiplier | ADP tier adjustments |
| Step 3 | Injury Adjustment | Injury status penalties |
| Step 4 | Team Quality Multiplier | Overall team strength |
| Step 5 | Bye Week Optimization | Schedule coordination |
| **Step 6** | **Matchup Multiplier** | **Position-specific opponent defense (pts_allowed_to_WR/TE/RB/QB/K)** |
| Step 7 | Schedule Strength | Full season schedule analysis |
| Step 8 | Team Penalty | Avoid specific teams |
| Step 9 | Draft Order Scoring | Position-round prioritization |
| Step 10 | Flex Adjustment | Flex eligibility bonus |
| **Step 11** | **Temperature Scoring** | **Cold/hot weather impact** |
| **Step 12** | **Wind Scoring** | **High wind impact on passing/kicking** |
| Step 13 | Location Scoring | Home/away/international |

---

## Current Metric Request Files (M01-M12, M17)

These already have individual metric request files in `feature-updates/`:

| ID | Metric | Positions | Category |
|----|--------|-----------|----------|
| M01 | Target Volume / Target Share | WR, TE, RB | Volume |
| M02 | QB Rushing Upside | QB | Efficiency |
| M03 | Pass Attempts Per Game | QB | Volume |
| M04 | Carries Per Game | RB | Volume |
| M05 | Kicker Accuracy | K | Efficiency |
| M06 | Completion Percentage | QB | Efficiency |
| M07 | TD:INT Ratio | QB | Efficiency |
| M08 | Yards Per Carry | RB | Efficiency |
| M09 | Yards Per Reception | WR, TE | Efficiency |
| M10 | Catch Rate | WR, TE, RB | Efficiency |
| M11 | RB Receiving Workload | RB | Volume |
| M12 | QB Quality | WR, TE, RB | Context |
| M17 | Target Share Trend | WR, TE, RB | Trend |

---

## New Metric Ideas - Data Availability Assessment

### Category 1: Red Zone & Scoring Opportunity

#### M13: Red Zone Target Share
- **What it measures:** Percentage of team's red zone targets (within 20 yards)
- **Positions:** WR, TE, RB
- **Data Available:** NO - No red zone specific data in current datasets
- **Impact:** High (10-15% TD prediction improvement)
- **Notes:** Would require new data source or API enhancement

#### M14: Goal-Line Carry Share
- **What it measures:** Percentage of team's goal-line rushing attempts (within 5 yards)
- **Positions:** RB
- **Data Available:** NO - No goal-line specific data
- **Impact:** High (8-12% RB TD prediction)
- **Notes:** Would require play-by-play data

#### M15: Red Zone Efficiency
- **What it measures:** TD conversion rate when in red zone
- **Positions:** All skill positions
- **Data Available:** NO - No red zone opportunity data
- **Impact:** Medium (5-8%)
- **Notes:** Requires red zone opportunity tracking

---

### Category 2: Usage & Opportunity

#### M16: Snap Count Percentage
- **What it measures:** Percentage of team offensive snaps player participates in
- **Positions:** All
- **Data Available:** NO - No snap count data in current datasets
- **Impact:** High (12-18% floor prediction)
- **Notes:** Would require snap count data source

#### M18: Route Participation Rate
- **What it measures:** Percentage of pass plays where WR/TE runs a route
- **Positions:** WR, TE
- **Data Available:** NO - No route data
- **Impact:** Medium (8-12%)
- **Notes:** Requires advanced tracking data

#### M19: Touch Share (Total Opportunity)
- **What it measures:** (Carries + Targets) as percentage of team total
- **Positions:** RB, WR
- **Data Available:** YES - Can derive from rushing.attempts + receiving.targets for all players on team
- **Impact:** High (10-14%)
- **Notes:** Calculate by summing all team touches per week

#### M20: Slot vs Outside Target Distribution
- **What it measures:** Percentage of targets from slot position
- **Positions:** WR
- **Data Available:** NO - No alignment data
- **Impact:** Medium (6-10%)
- **Notes:** Requires tracking data

---

### Category 3: Advanced Efficiency

#### M21: Air Yards / Average Depth of Target (aDOT)
- **What it measures:** Average distance of targets from line of scrimmage
- **Positions:** WR, TE
- **Data Available:** NO - No air yards or target depth data
- **Impact:** High (10-14% boom/bust prediction)
- **Notes:** Requires Next Gen Stats or similar

#### M22: Yards After Catch (YAC) Per Reception
- **What it measures:** Average yards gained after the catch
- **Positions:** WR, TE, RB
- **Data Available:** NO - No YAC data (only total receiving yards)
- **Impact:** Medium (8-12%)
- **Notes:** Requires advanced receiving metrics

#### M23: Broken Tackles Per Touch
- **What it measures:** Ratio of broken/missed tackles to total touches
- **Positions:** RB, WR
- **Data Available:** NO - No tackle data
- **Impact:** Medium (6-10%)
- **Notes:** Requires PFF or similar tracking

#### M24: Success Rate / EPA Per Touch
- **What it measures:** Expected Points Added per offensive touch
- **Positions:** RB
- **Data Available:** NO - No EPA data
- **Impact:** High (8-12%)
- **Notes:** Requires play-by-play EPA feed

#### M25: Yards Per Route Run
- **What it measures:** Receiving yards divided by routes run
- **Positions:** WR, TE
- **Data Available:** NO - No route data
- **Impact:** High (10-14%)
- **Notes:** Requires route tracking

---

### Category 4: Team Context & Game Script

#### M26: Pace of Play (Plays Per Game)
- **What it measures:** Team's average offensive plays per game
- **Positions:** All (contextual)
- **Data Available:** PARTIAL - Can estimate from (pass_attempts + rush_attempts) aggregated by team
- **Impact:** Medium (6-10%)
- **Notes:** Approximation possible by summing QB attempts + team rush attempts

#### M27: Pass-to-Run Ratio
- **What it measures:** Team's passing play percentage vs rushing
- **Positions:** WR/TE vs RB
- **Data Available:** YES - Can derive from team aggregate pass attempts vs rush attempts
- **Impact:** Medium (5-8%)
- **Notes:** Sum QB pass attempts and team rush attempts per week

#### M28: Game Script Tendency (Trailing Team Boost)
- **What it measures:** How often team plays from behind; average point differential
- **Positions:** WR, TE (benefit when trailing)
- **Data Available:** YES - game_data.csv has home_team_score, away_team_score per week
- **Impact:** High (8-12%)
- **Notes:** Can calculate win/loss margin and identify trailing situations

#### M29: Offensive Line Quality
- **What it measures:** Team's offensive line performance grade
- **Positions:** QB, RB
- **Data Available:** NO - No OL grades or metrics
- **Impact:** High (8-12%)
- **Notes:** Requires PFF or similar

#### M30: Offensive Efficiency (Points Per Drive)
- **What it measures:** Team's scoring rate normalized by possessions
- **Positions:** All (contextual)
- **Data Available:** PARTIAL - Have points_scored in team_data but no drive counts
- **Impact:** Medium (5-8%)
- **Notes:** Could approximate with points per game

---

### Category 5: Matchup & Weekly Adjustments

**NOTE:** Several metrics originally in this category are already implemented:
- ~~M31: Opponent Pass Defense Ranking~~ → **Already implemented in Step 6 (Matchup Multiplier)**
- ~~M32: Opponent Run Defense Ranking~~ → **Already implemented in Step 6 (Matchup Multiplier)**
- ~~M33: Weather Impact Score~~ → **Already implemented in Steps 11-12 (Temperature/Wind Scoring)**

*No new metrics remain in this category.*

---

### Category 6: Trend & Momentum

#### M34: Recent Form (Rolling 4-Week Average)
- **What it measures:** Average fantasy production over last 4 games
- **Positions:** All
- **Data Available:** YES - actual_points arrays available for all players
- **Impact:** Medium (5-8%)
- **Notes:** Simple rolling calculation on existing data

#### M35: Snap Count Trend
- **What it measures:** Week-over-week change in snap percentage
- **Positions:** All
- **Data Available:** NO - No snap count data
- **Impact:** Medium (6-10%)
- **Notes:** Blocked by lack of snap data

#### M36: Volume Spike Indicator
- **What it measures:** Sharp increase in touches/targets from recent baseline
- **Positions:** All
- **Data Available:** YES - targets and attempts arrays available
- **Impact:** Medium (4-6%)
- **Notes:** Can detect week-over-week volume changes

#### M37: Boom/Bust Frequency
- **What it measures:** How often player exceeds ceiling vs hits floor
- **Positions:** All
- **Data Available:** YES - actual_points and projected_points available
- **Impact:** Medium (5-8%)
- **Notes:** Can calculate variance from projections

---

### Category 7: Injury & Durability

#### M38: Injury Return Ramp-Up
- **What it measures:** Production progression for players returning from injury
- **Positions:** All
- **Data Available:** PARTIAL - Have injury_status and actual_points, but not detailed injury history
- **Impact:** Medium (4-8%)
- **Notes:** Can detect 0-point weeks followed by returns

#### M39: Games Missed Percentage
- **What it measures:** Percentage of games missed this season
- **Positions:** All
- **Data Available:** YES - Can count weeks with 0.0 actual_points
- **Impact:** Low (3-5%)
- **Notes:** Simple calculation from weekly arrays

#### M40: Injury History Risk Score
- **What it measures:** Injury frequency over past 2-3 seasons
- **Positions:** All
- **Data Available:** NO - Only current season data
- **Impact:** Medium (4-6%)
- **Notes:** Would require historical injury database

---

### Category 8: DST-Specific Metrics

#### M41: Turnover Rate (INT + Fumble Recovery Per Game)
- **What it measures:** Defensive turnovers generated per game
- **Positions:** DST
- **Data Available:** YES - defense.interceptions and defense.fumbles_recovered available
- **Impact:** High (8-12%)
- **Notes:** Direct calculation possible

#### M42: Sack Rate (Sacks Per Game)
- **What it measures:** Average sacks per game
- **Positions:** DST
- **Data Available:** YES - defense.sacks available weekly
- **Impact:** Medium (6-8%)
- **Notes:** Direct calculation possible

#### M43: Points Allowed Trend
- **What it measures:** Rolling average of points allowed
- **Positions:** DST
- **Data Available:** YES - defense.pts_g available weekly
- **Impact:** Medium (5-8%)
- **Notes:** Simple rolling calculation

#### M44: Opponent Offensive Strength
- **What it measures:** Quality of opposing offense faced this week
- **Positions:** DST
- **Data Available:** YES - Can derive from team points_scored data
- **Impact:** High (10-14%)
- **Notes:** Cross-reference game_data with team scoring

#### M45: Pressure Rate (QB Hits + Hurries)
- **What it measures:** Percentage of dropbacks with defensive pressure
- **Positions:** DST
- **Data Available:** NO - Only sacks, not pressures/hurries
- **Impact:** Medium (6-10%)
- **Notes:** Would require advanced tracking

---

### Category 9: Kicker Extensions

#### M46: Field Goal Attempts Per Game
- **What it measures:** Average FG attempts per game (opportunity volume)
- **Positions:** K
- **Data Available:** YES - field_goals.made + field_goals.missed gives attempts
- **Impact:** High (8-12%)
- **Notes:** Direct calculation possible

#### M47: Long Field Goal Accuracy (50+ yards)
- **What it measures:** Accuracy on kicks 50+ yards
- **Positions:** K
- **Data Available:** NO - No distance breakdown for FGs
- **Impact:** Medium (5-8%)
- **Notes:** Would require kick distance data

#### M48: Extra Point Attempts Per Game
- **What it measures:** PAT attempts (proxy for team TD rate)
- **Positions:** K
- **Data Available:** YES - extra_points.made + extra_points.missed gives attempts
- **Impact:** Low (4-6%)
- **Notes:** Direct calculation possible

**NOTE:** ~~M49: Indoor/Dome Kicker Boost~~ → **Already covered by Steps 11-12 (indoor games have no weather penalty)**

---

### Category 10: Workload Consistency

#### M50: Touch Consistency Index
- **What it measures:** Standard deviation of weekly touches
- **Positions:** RB
- **Data Available:** YES - rushing.attempts + receiving.targets available
- **Impact:** Medium (5-8%)
- **Notes:** Calculate std dev of weekly totals

#### M51: Target Consistency Index
- **What it measures:** Standard deviation of weekly targets
- **Positions:** WR, TE
- **Data Available:** YES - receiving.targets available weekly
- **Impact:** Medium (5-8%)
- **Notes:** Calculate std dev of weekly targets

---

## Summary: Data Availability Matrix

### YES - Can Implement Now (13 metrics)

| ID | Metric | Data Source |
|----|--------|-------------|
| M19 | Touch Share | rushing.attempts + receiving.targets (aggregate by team) |
| M27 | Pass-to-Run Ratio | QB attempts + team rush attempts |
| M28 | Game Script Tendency | game_data.csv scores |
| M34 | Recent Form (4-week) | actual_points arrays |
| M36 | Volume Spike Indicator | targets/attempts arrays |
| M37 | Boom/Bust Frequency | actual_points vs projected_points |
| M39 | Games Missed % | Count 0.0 weeks in actual_points |
| M41 | Turnover Rate (DST) | defense.interceptions + fumbles_recovered |
| M42 | Sack Rate (DST) | defense.sacks |
| M43 | Points Allowed Trend | defense.pts_g |
| M44 | Opponent Offensive Strength | team points_scored cross-reference |
| M46 | FG Attempts Per Game | field_goals.made + missed |
| M48 | PAT Attempts Per Game | extra_points.made + missed |
| M50 | Touch Consistency Index | std dev of attempts + targets |
| M51 | Target Consistency Index | std dev of targets |

### REMOVED - Already Implemented (4 metrics)

| ID | Metric | Existing Implementation |
|----|--------|------------------------|
| ~~M31~~ | Opponent Pass Defense | Step 6: Matchup Multiplier |
| ~~M32~~ | Opponent Run Defense | Step 6: Matchup Multiplier |
| ~~M33~~ | Weather Impact | Steps 11-12: Temperature/Wind Scoring |
| ~~M49~~ | Indoor/Dome Boost | Steps 11-12: Indoor = no weather penalty |

### PARTIAL - May Be Able to Approximate (3 metrics)

| ID | Metric | Limitation |
|----|--------|------------|
| M26 | Pace of Play | Can estimate from attempts, but not true play count |
| M30 | Offensive Efficiency | Have points but no drive counts |
| M38 | Injury Return Ramp-Up | Can detect returns but not detailed injury tracking |

### NO - Requires New Data Source (18 metrics)

| ID | Metric | Missing Data |
|----|--------|--------------|
| M13 | Red Zone Target Share | Red zone specific stats |
| M14 | Goal-Line Carry Share | Goal-line specific stats |
| M15 | Red Zone Efficiency | Red zone opportunities |
| M16 | Snap Count % | Snap counts |
| M18 | Route Participation | Routes run |
| M20 | Slot vs Outside | Alignment data |
| M21 | Air Yards / aDOT | Target depth |
| M22 | Yards After Catch | YAC splits |
| M23 | Broken Tackles | Tackle data |
| M24 | Success Rate / EPA | EPA data |
| M25 | Yards Per Route Run | Routes run |
| M29 | Offensive Line Quality | OL grades |
| M35 | Snap Count Trend | Snap counts |
| M40 | Injury History Risk | Multi-season injury data |
| M45 | Pressure Rate | Pressures/hurries |
| M47 | Long FG Accuracy | FG distance breakdown |

---

## Recommended Implementation Priority

### Tier 1: Implement First (High Impact, Data Available)

| ID | Metric | Impact | Effort |
|----|--------|--------|--------|
| **M41** | Turnover Rate (DST) | High | Low |
| **M28** | Game Script Tendency | High | Medium |
| **M19** | Touch Share | High | Low |
| **M44** | Opponent Offensive Strength | High | Medium |

### Tier 2: Implement Second (Medium Impact, Data Available)

| ID | Metric | Impact | Effort |
|----|--------|--------|--------|
| **M34** | Recent Form (4-week avg) | Medium | Low |
| **M50** | Touch Consistency Index | Medium | Low |
| **M51** | Target Consistency Index | Medium | Low |
| **M37** | Boom/Bust Frequency | Medium | Medium |
| **M42** | Sack Rate (DST) | Medium | Low |
| **M46** | FG Attempts Per Game | Medium | Low |

### Tier 3: Quick Wins (Low Impact, Data Available)

| ID | Metric | Impact | Effort |
|----|--------|--------|--------|
| **M27** | Pass-to-Run Ratio | Medium | Low |
| **M39** | Games Missed % | Low | Low |
| **M43** | Points Allowed Trend | Medium | Low |
| **M48** | PAT Attempts Per Game | Low | Low |
| **M36** | Volume Spike Indicator | Low | Low |

### Tier 4: Future (Requires New Data)

All metrics marked "NO" in data availability - would require:
- ESPN/Yahoo API enhancements for snap counts
- NFL Next Gen Stats for air yards, YAC, routes
- PFF subscription for OL grades, broken tackles, pressure rate
- Play-by-play data for red zone, goal-line, EPA

---

## Next Steps

1. **Select 5-6 metrics from Tier 1** for immediate implementation
2. **Create individual metric request files** for selected metrics
3. **Consider data source additions** for high-value Tier 4 metrics (snap counts, red zone)

---

**END OF IDEAS DOCUMENT**
