# Scoring Gap Analysis: Research Metrics vs. League Helper Implementation

**Generated:** December 12, 2025
**Purpose:** Compare metrics used in manual WR analysis to existing scoring algorithm to identify potential enhancements

---

## Executive Summary

The current 13-step scoring algorithm covers foundational metrics well but lacks several advanced metrics that proved valuable in the Week 15 WR analysis. Key gaps include:

| Priority | Gap | Impact |
|----------|-----|--------|
| **High** | Target Volume/Share | Critical for weekly decisions |
| **High** | QB Context | Affects all pass-catchers |
| **High** | Vegas Lines/Game Script | Game environment predictor |
| **High** | Implied Team Total | More precise than O/U |
| **Medium** | Teammate Injury Impact | Role changes |
| **Medium** | Opponent Secondary Details | Beyond aggregate defense rank |
| **Medium** | Team Pass Rate / Tempo | Volume opportunity |
| **Low** | Streak Momentum | Hot/cold beyond performance deviation |
| **Low** | Air Yards (aDOT) | Ceiling indicator |
| **Low** | Divisional Game Adjustment | Variance modifier |

**Total Potential Metrics Identified:** 38 metrics across 5 categories:
- Original gap metrics: 11
- Additional review metrics: 8
- Projection calculation metrics: 19 (NEW)

---

## Current System: 13-Step Scoring Algorithm

### Implemented Steps

| Step | Metric | Type | Range | Mode Usage |
|------|--------|------|-------|------------|
| 1 | **Normalization** | Base | 0-135 scale | All modes |
| 2 | **ADP Multiplier** | Multiplicative | 0.87-1.15x | Add To Roster |
| 3 | **Player Rating** | Multiplicative | 0.96-1.04x | Add To Roster, Trade Sim |
| 4 | **Team Quality** | Multiplicative | 0.91-1.09x | All modes |
| 5 | **Performance** | Multiplicative | 0.87-1.14x | Starter Helper, Trade Sim |
| 6 | **Matchup** | Additive | -4.6 to +4.6 pts | Starter Helper |
| 7 | **Schedule** | Additive | -4.3 to +4.3 pts | Trade Sim |
| 8 | **Draft Order** | Additive | 0 to +80 pts | Add To Roster |
| 9 | **Bye Week** | Penalty | 0 to -50 pts | Add To Roster, Trade Sim (User) |
| 10 | **Injury** | Penalty | 0 to -100 pts | Add To Roster |
| 11 | **Temperature** | Additive | -2.5 to +2.5 pts | Starter Helper |
| 12 | **Wind** | Additive | -3.0 to +3.0 pts | Starter Helper (QB/WR/K) |
| 13 | **Location** | Additive | -5 to +2 pts | Starter Helper |

*Note: Mode names match official terminology from `docs/scoring_v2/README.md`*

---

## Research Metrics Comparison

### Metrics ALREADY Covered by System

| Research Metric | System Step | Coverage Quality | Notes |
|-----------------|-------------|------------------|-------|
| **Projections** | Step 1 (Normalization) | Excellent | ESPN weekly/ROS projections |
| **Matchup Quality** | Step 6 (Matchup) | Good | Position-specific defense ranks |
| **Recent Performance** | Step 5 (Performance) | Good | Actual vs projected deviation |
| **Temperature** | Step 11 | Good | Ideal ~60°F, penalties at extremes |
| **Wind** | Step 12 | Good | QB/WR/K affected |
| **Location** | Step 13 | Good | Home/away/international |
| **Injury Status** | Step 10 | Good | ACTIVE/QUESTIONABLE/OUT/IR |
| **Schedule Strength** | Step 7 | Good | Future opponent avg defense rank |
| **Team Quality** | Step 4 | Good | Offensive/defensive rankings |

### Metrics NOT Covered (Gaps Identified)

#### HIGH PRIORITY

**1. Target Volume / Target Share**

| Attribute | Details |
|-----------|---------|
| Description | Number of targets and share of team's total targets |
| Research Use | Wilson: 16+ targets/game without MHJ; Waddle: 31.8% target share |
| Why Important | Direct predictor of opportunity; more reliable than projections alone |
| Data Source | ESPN stats API, Pro Football Reference |
| Suggested Step | New Step or enhance Step 6 |
| Implementation | Additive bonus based on target share percentile |

```
Proposed Thresholds:
- EXCELLENT: ≥25% target share (+3.0 pts)
- GOOD: 20-24% target share (+1.5 pts)
- AVERAGE: 15-19% target share (0 pts)
- POOR: 10-14% target share (-1.5 pts)
- VERY_POOR: <10% target share (-3.0 pts)
```

---

**2. QB Context / QB Quality Score**

| Attribute | Details |
|-----------|---------|
| Description | QB performance level and consistency for pass-catchers |
| Research Use | Mahomes = elite; Brissett = backup; Tua = weather-dependent |
| Why Important | WR/TE value directly tied to QB quality |
| Data Source | QB ratings, passer rating, completion %, historical consistency |
| Suggested Step | New Step (multiplicative for WR/TE only) |
| Implementation | QB tier multiplier applied to WR/TE scores |

```
Proposed Tiers:
- ELITE QB (Mahomes, Allen, Jackson): 1.05x
- GOOD QB (Goff, Hurts, Stroud): 1.025x
- AVERAGE QB (most starters): 1.0x
- POOR QB (struggling starters): 0.975x
- BACKUP QB (Brissett, etc.): 0.95x
```

---

**3. QB-Specific Weather Sensitivity**

| Attribute | Details |
|-----------|---------|
| Description | Player-specific performance in weather conditions |
| Research Use | Tua: 0-5 career under 40°F; 57% completion in cold |
| Why Important | Current weather scoring is generic; some players have specific vulnerabilities |
| Data Source | Historical game logs filtered by temperature |
| Suggested Step | Enhance Step 11 (Temperature) with player-specific modifiers |
| Implementation | Override temperature tier for players with documented weather issues |

```
Example: Tua Tagovailoa
- Under 40°F: Force VERY_POOR rating regardless of calculated tier
- Apply 0.85x multiplier to all Dolphins pass-catchers
```

---

**4. Vegas Lines / Game Environment Score**

| Attribute | Details |
|-----------|---------|
| Description | Over/under totals, spreads, and implied team totals |
| Research Use | Lions-Rams O/U 54.5 (high-scoring); Dolphins-Steelers O/U 42 (low-scoring) |
| Why Important | Vegas lines are the best predictor of game script and scoring environment |
| Data Source | ESPN odds, DraftKings, FanDuel APIs |
| Suggested Step | New Step (additive bonus based on game total) |
| Implementation | Bonus/penalty based on O/U total |

```
Proposed Thresholds (O/U Total):
- EXCELLENT: ≥52.5 (+4.0 pts)
- GOOD: 47.5-52.0 (+2.0 pts)
- AVERAGE: 42.5-47.0 (0 pts)
- POOR: 37.5-42.0 (-2.0 pts)
- VERY_POOR: <37.5 (-4.0 pts)
```

---

#### MEDIUM PRIORITY

**5. Teammate Injury Impact**

| Attribute | Details |
|-----------|---------|
| Description | How teammate injuries affect a player's role/targets |
| Research Use | MHJ out → Wilson becomes WR1 (30.8 PPG); Tyreek out → Waddle WR1 |
| Why Important | Massive value swing for secondary options |
| Data Source | Injury reports + historical target distribution |
| Suggested Step | New Step or enhance existing projection |
| Implementation | Boost players when their WR1/TE1/RB1 teammate is OUT |

```
Proposed Implementation:
- Primary teammate OUT: +15% score boost
- Primary teammate DOUBTFUL: +8% score boost
- Primary teammate QUESTIONABLE: +3% score boost
```

---

**6. Opponent Secondary Details**

| Attribute | Details |
|-----------|---------|
| Description | Specific cornerback/safety injuries and coverage tendencies |
| Research Use | Rams CB McCreary on IR → favorable for outside WRs |
| Why Important | Current system only uses aggregate defense rank |
| Data Source | Team injury reports, PFF coverage data |
| Suggested Step | Enhance Step 6 (Matchup) |
| Implementation | Additional bonus when key DBs are OUT |

```
Proposed Implementation:
- CB1 OUT: +2.0 pts for WRs
- CB2 OUT: +1.0 pts for WRs
- Safety OUT: +1.5 pts for TEs
```

---

**7. Red Zone Opportunity**

| Attribute | Details |
|-----------|---------|
| Description | Red zone targets, goal-line carries, red zone target share |
| Research Use | Not explicitly used but affects TD probability |
| Why Important | TDs are high-value in fantasy; red zone usage predicts TDs |
| Data Source | ESPN stats, Pro Football Reference |
| Suggested Step | New Step (additive bonus) |
| Implementation | Bonus based on red zone target share percentile |

---

#### LOW PRIORITY

**8. Hot Streak / Cold Streak Momentum**

| Attribute | Details |
|-----------|---------|
| Description | Consecutive games above/below threshold |
| Research Use | Williams: 4 straight 85+ yard games; Waddle: 3 catches in last 2 games |
| Why Important | Momentum beyond performance deviation |
| Current Coverage | Partially covered by Step 5 (Performance) |
| Gap | Step 5 averages deviation; doesn't capture consistency of streak |
| Suggested Enhancement | Add streak multiplier on top of performance |

```
Proposed Implementation:
- 4+ consecutive above-projection games: additional +1.03x
- 4+ consecutive below-projection games: additional 0.97x
```

---

**9. Snap Count / Usage Rate**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of offensive snaps played |
| Research Use | Not explicitly used but indicates role |
| Why Important | Players with high snap % have more opportunity |
| Data Source | ESPN, PFF snap counts |
| Suggested Step | New Step or combine with target share |

---

**10. Coverage Type Tendencies**

| Attribute | Details |
|-----------|---------|
| Description | Single-high vs two-high safety, zone vs man coverage |
| Research Use | Steelers play 5th-most single-high (Waddle thrives against) |
| Why Important | Certain players excel vs specific coverage types |
| Complexity | High - requires player-coverage matchup data |
| Suggested Step | Long-term enhancement to Step 6 |

---

**11. Primetime Game Adjustment**

| Attribute | Details |
|-----------|---------|
| Description | Performance variance in MNF/SNF/TNF games |
| Research Use | Waddle MNF in Pittsburgh noted as risk factor |
| Why Important | Some players/teams perform differently in primetime |
| Data Source | Historical primetime game logs |
| Suggested Step | New optional Step |

---

#### ADDITIONAL METRICS (Identified in Review)

**12. Implied Team Total**

| Attribute | Details |
|-----------|---------|
| Description | Expected points for a specific team (derived from O/U and spread) |
| Calculation | Implied Total = (O/U + Spread) / 2 for favorites |
| Why Important | More precise than O/U; accounts for lopsided games |
| Research Use | Raiders implied 13.5 pts (bad); Cowboys implied 25 pts (good) |
| Suggested Step | Enhance Vegas Lines integration |

```
Formula:
- Favorite Implied Total = (O/U + |Spread|) / 2
- Underdog Implied Total = (O/U - |Spread|) / 2

Proposed Thresholds:
- EXCELLENT: ≥27 implied pts (+3.0 pts)
- GOOD: 24-26 implied pts (+1.5 pts)
- AVERAGE: 20-23 implied pts (0 pts)
- POOR: 16-19 implied pts (-1.5 pts)
- VERY_POOR: <16 implied pts (-3.0 pts)
```

---

**13. Air Yards / aDOT (Average Depth of Target)**

| Attribute | Details |
|-----------|---------|
| Description | Average distance of passes thrown to a player |
| Why Important | High aDOT indicates big-play potential; affects ceiling |
| Data Source | ESPN, Next Gen Stats, PFF |
| Suggested Step | New Step (additive for WR only) |
| Complexity | Medium - requires target-level data |

```
Proposed Thresholds:
- EXCELLENT: ≥14.0 aDOT (+2.0 pts ceiling boost)
- GOOD: 11.0-13.9 aDOT (+1.0 pts)
- AVERAGE: 8.0-10.9 aDOT (0 pts)
- POOR: 5.0-7.9 aDOT (-0.5 pts)
- VERY_POOR: <5.0 aDOT (-1.0 pts)
```

---

**14. Yards After Catch (YAC) Rate**

| Attribute | Details |
|-----------|---------|
| Description | Yards gained after reception divided by total receiving yards |
| Why Important | High YAC players maintain value even with short passes or weak QBs |
| Data Source | ESPN, NFL Stats, PFF |
| Suggested Step | Enhance Target Share metric |
| Implementation | Bonus for high YAC with poor QB context |

---

**15. Team Pass Rate / Plays Per Game**

| Attribute | Details |
|-----------|---------|
| Description | Team's passing frequency and overall tempo |
| Why Important | High-volume passing teams create more WR/TE opportunity |
| Research Use | Lions lead NFL in plays/game, boosting all skill players |
| Data Source | NFL team stats |
| Suggested Step | Enhance Team Quality (Step 4) |

```
Proposed Implementation:
- Top 5 pass rate team: +1.5 pts for WR/TE
- Bottom 5 pass rate team: -1.5 pts for WR/TE
- Top 5 run rate team: +1.5 pts for RB
- Bottom 5 run rate team: -1.5 pts for RB
```

---

**16. Pressure Rate / QB Protection**

| Attribute | Details |
|-----------|---------|
| Description | How often QB is pressured or sacked |
| Why Important | High pressure = less time for routes to develop = fewer targets |
| Research Use | Raiders O-line terrible (0.72 inches before contact) |
| Data Source | PFF, ESPN advanced stats |
| Suggested Step | Enhance QB Context metric |

---

**17. Route Participation Rate**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of pass plays where WR runs a route |
| Why Important | Direct measure of involvement in passing game |
| Data Source | Next Gen Stats, PFF |
| Suggested Step | Combine with Target Share |
| Complexity | Medium-High |

---

**18. Divisional Game Adjustment**

| Attribute | Details |
|-----------|---------|
| Description | Performance variance in divisional matchups |
| Why Important | More game film, higher stakes, defensive familiarity |
| Research Use | Divisional games often have lower scoring, tighter coverage |
| Data Source | NFL schedule (division identification) |
| Suggested Step | New optional Step |

```
Proposed Implementation:
- Divisional game: ±1.0 pts variance modifier
- Apply negative adjustment to high-ceiling players
- Apply positive adjustment to high-floor players
```

---

**19. Third Down / High-Leverage Role**

| Attribute | Details |
|-----------|---------|
| Description | Player's usage on third down and clutch situations |
| Why Important | Third down targets often convert to first downs (chains) |
| Research Use | Not explicitly researched but affects consistency |
| Data Source | ESPN situational stats |
| Suggested Step | New optional Step (enhances Floor calculation) |

---

## PROJECTION CALCULATION METRICS (New Section)

The following metrics are specifically useful for **calculating projected fantasy point values** rather than just adjusting existing projections. These are the building blocks used by professional projection systems.

---

### Opportunity-Based Metrics (Most Predictive)

Research shows volume/opportunity metrics are more predictive than efficiency metrics for fantasy projections.

**20. WOPR (Weighted Opportunity Rating)**

| Attribute | Details |
|-----------|---------|
| Description | Combined measure of target share + air yards share |
| Formula | `WOPR = 1.5 × (Target Share) + 0.7 × (Air Yards Share)` |
| Why Important | Air yards + targets combined are more predictive than targets alone |
| Creator | Josh Hermsmeyer |
| Data Source | NFL Stats, ESPN |
| Use Case | WR/TE projection baseline |

```
Interpretation:
- Higher WOPR = higher-value targets on average
- WOPR > 0.50 = elite opportunity
- WOPR 0.35-0.50 = solid starter
- WOPR < 0.25 = limited role
```

---

**21. Opportunity Share (RB-Specific)**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of team RB carries + targets |
| Formula | `Opp Share = (Player Carries + Targets) / (Team RB Carries + Targets)` |
| Why Important | Most stable RB stat year-over-year; predicts workload |
| Data Source | ESPN, NFL Stats |
| Use Case | RB projection baseline |

```
Thresholds:
- EXCELLENT: ≥70% opportunity share (bell cow)
- GOOD: 50-69% (lead back)
- AVERAGE: 30-49% (committee)
- POOR: <30% (backup/change of pace)
```

---

**22. Expected Fantasy Points (xFP)**

| Attribute | Details |
|-----------|---------|
| Description | Projected fantasy points based on opportunity quality |
| Calculation | Uses completion probability, expected YAC, expected rushing yards |
| Why Important | Quantifies actual production vs expected production |
| Data Source | NFL Next Gen Stats |
| Use Case | Identify over/underperformers for regression |

```
Application:
- xFP > Actual FP = Buy-low candidate (due for positive regression)
- xFP < Actual FP = Sell-high candidate (due for negative regression)
```

---

**23. Fantasy Points Under/Over Expectation (FPUE/FPOE)**

| Attribute | Details |
|-----------|---------|
| Description | Difference between actual and expected fantasy points |
| Formula | `FPOE = Actual FP - Expected FP` |
| Why Important | Identifies regression candidates |
| Data Source | NFL Next Gen Stats, Fantasy Points |
| Use Case | Trade value, projection adjustments |

---

**24. Routes Per Game / Snaps Per Game**

| Attribute | Details |
|-----------|---------|
| Description | Total route-running opportunities for pass-catchers |
| Why Important | More routes = more target opportunities |
| Data Source | PFF, Next Gen Stats |
| Use Case | WR/TE opportunity ceiling |

```
Elite WRs: 35+ routes per game
Starter WRs: 25-35 routes per game
Rotational: <25 routes per game
```

---

### Efficiency Metrics (Secondary Predictive Value)

**25. Yards Per Route Run (YPRR)**

| Attribute | Details |
|-----------|---------|
| Description | Receiving yards divided by routes run |
| Formula | `YPRR = Receiving Yards / Routes Run` |
| Why Important | Most predictive efficiency metric for WRs (154% more FP for top-20 YPRR) |
| Data Source | PFF |
| Use Case | WR skill evaluation, breakout identification |

```
Benchmarks:
- Elite: ≥2.50 YPRR
- Good: 2.00-2.49 YPRR
- Average: 1.50-1.99 YPRR
- Poor: <1.50 YPRR
```

---

**26. Expected Points Added (EPA)**

| Attribute | Details |
|-----------|---------|
| Description | How much a play increases/decreases scoring probability |
| Why Important | Measures true value of each play in context |
| Data Source | NFL Next Gen Stats, nfelo |
| Use Case | Team/player efficiency evaluation |

```
Benchmarks:
- League average: 0.0 EPA per play
- Elite offense: +0.10 to +0.20 EPA per play
- Poor offense: -0.10 or worse EPA per play
```

---

**27. Rush Yards Over Expected (RYOE)**

| Attribute | Details |
|-----------|---------|
| Description | Actual rush yards minus expected yards based on blocking/situation |
| Why Important | Isolates RB skill from offensive line performance |
| Data Source | NFL Next Gen Stats |
| Use Case | RB talent evaluation independent of team |

```
Application:
- Positive RYOE = RB creating yards on his own
- Negative RYOE = RB underperforming blocking
```

---

**28. Yards Before Contact / Yards After Contact**

| Attribute | Details |
|-----------|---------|
| Description | Yards gained before/after first defender contact |
| Why Important | YBC = O-line quality; YAC = RB skill |
| Data Source | PFF, Next Gen Stats |
| Use Case | Separate RB skill from team context |

```
Elite RBs: ≥3.0 yards after contact per attempt
Average: 2.0-2.9 YACO
Poor: <2.0 YACO
```

---

**29. Success Rate**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of plays gaining positive EPA |
| Why Important | Measures consistency of positive contributions |
| Data Source | NFL Stats |
| Use Case | Floor projection for RBs |

```
Benchmarks:
- Elite: ≥50% success rate
- Good: 45-49%
- Average: 40-44%
- Poor: <40%
```

---

**30. True Catch Rate**

| Attribute | Details |
|-----------|---------|
| Description | Catches divided by catchable targets (excludes uncatchable balls) |
| Why Important | Measures receiver hands/skill independent of QB accuracy |
| Data Source | PFF, Player Profiler |
| Use Case | WR efficiency evaluation |

---

### Next Gen Stats Metrics

**31. Separation**

| Attribute | Details |
|-----------|---------|
| Description | Yards between receiver and nearest defender at catch point |
| Why Important | Open receivers = easier completions = more targets |
| Data Source | NFL Next Gen Stats |
| Use Case | WR skill + scheme evaluation |

```
Benchmarks:
- Elite separation: ≥3.5 yards
- Good: 2.5-3.4 yards
- Average: 1.5-2.4 yards
- Tight coverage: <1.5 yards
```

---

**32. Completion Probability (CP)**

| Attribute | Details |
|-----------|---------|
| Description | Likelihood of completion based on coverage, separation, throw difficulty |
| Why Important | Low CP completions = elite QB/WR connection |
| Data Source | NFL Next Gen Stats (CP 2.0 in 2025) |
| Use Case | QB evaluation, target quality assessment |

---

**33. Expected YAC (xYAC)**

| Attribute | Details |
|-----------|---------|
| Description | Predicted yards after catch based on field position, defenders nearby |
| Why Important | YAC over expected = playmaker ability |
| Data Source | NFL Next Gen Stats |
| Use Case | WR ceiling projection |

---

### Team-Level Projection Factors

**34. Team Plays Per Game**

| Attribute | Details |
|-----------|---------|
| Description | Total offensive snaps/plays run per game |
| Why Important | More plays = more opportunities for all skill players |
| Data Source | NFL Stats |
| Use Case | Team-level projection multiplier |

```
High-tempo teams (65+ plays): +5-10% opportunity boost
Low-tempo teams (<55 plays): -5-10% opportunity reduction
```

---

**35. Neutral Script Pass Rate**

| Attribute | Details |
|-----------|---------|
| Description | Pass rate when game score is within 7 points |
| Why Important | Removes game script bias; shows true offensive philosophy |
| Data Source | NFL Stats |
| Use Case | WR/RB opportunity split projection |

```
Pass-heavy (≥60%): Boost WR/TE projections
Run-heavy (≤45%): Boost RB projections
Balanced (46-59%): Neutral
```

---

**36. Team Red Zone Efficiency**

| Attribute | Details |
|-----------|---------|
| Description | TD rate on red zone possessions |
| Why Important | Affects TD probability for all skill players |
| Data Source | NFL Stats |
| Use Case | TD projection modifier |

---

### Role-Based Projection Factors

**37. Snap Share Trend**

| Attribute | Details |
|-----------|---------|
| Description | Week-over-week change in snap percentage |
| Why Important | Increasing snap share = emerging role |
| Data Source | ESPN, PFF |
| Use Case | Identify breakout candidates |

```
Rising (3+ weeks increasing): Project higher
Stable: Project current level
Declining: Project lower
```

---

**38. Dominator Rating**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of team receiving yards + TDs in college |
| Why Important | Predicts NFL target share potential for rookies |
| Data Source | Player Profiler |
| Use Case | Rookie projection baseline |

```
Elite Dominator: ≥35%
Good: 25-34%
Average: 20-24%
Poor: <20%
```

---

## Projection Calculation Framework

### Recommended Approach (Per Expert Research)

1. **Start at Team Level**
   - Project total team plays, pass attempts, rush attempts
   - Project team scoring (using Vegas lines)

2. **Apply Role-Based Shares**
   - Distribute team stats among players by position
   - Use opportunity share, target share, snap share

3. **Adjust for Efficiency**
   - Apply YPRR, EPA, success rate modifiers
   - Adjust for matchup (defensive rankings)

4. **Factor Context**
   - QB quality (for WR/TE)
   - O-line quality (for RB)
   - Weather, home/away

5. **Apply Regression**
   - Compare to xFP for over/underperformers
   - Regress outliers toward expected values

---

### Key Insight from Research

> "Volume is what fantasy analysts are trying to predict—if you can project targets, you can project fantasy points."
> — Fantasy Points Data Research

**Priority Order for Projection Accuracy:**
1. **Opportunity metrics** (targets, carries, snap share) — Most predictive
2. **Team context** (plays per game, pass rate, implied total) — Sets ceiling
3. **Efficiency metrics** (YPRR, EPA) — Secondary adjustment
4. **Matchup/situation** — Weekly variance

---

## Implementation Roadmap

### Phase 1: Quick Wins (Low Effort, High Impact)

| Enhancement | Effort | Impact | Target |
|-------------|--------|--------|--------|
| Vegas O/U integration | Medium | High | Starter Helper |
| Implied Team Total | Low | High | Starter Helper |
| QB Quality tier | Low | High | Starter Helper |
| Teammate injury boost | Medium | High | All modes |

### Phase 2: Data Enrichment (Medium Effort)

| Enhancement | Effort | Impact | Target |
|-------------|--------|--------|--------|
| Target share tracking | Medium | High | Starter Helper |
| Team Pass Rate / Tempo | Low | Medium | Starter Helper |
| Red zone opportunity | Medium | Medium | Starter Helper |
| Opponent secondary injuries | Medium | Medium | Starter Helper |

### Phase 3: Advanced Analytics (High Effort)

| Enhancement | Effort | Impact | Target |
|-------------|--------|--------|--------|
| Player-specific weather models | High | Medium | Starter Helper |
| Coverage type matchups | High | Medium | Starter Helper |
| Air Yards (aDOT) | Medium | Medium | Starter Helper |
| Pressure Rate / QB Protection | Medium | Medium | Starter Helper |
| Streak momentum scoring | Low | Low | All modes |

### Phase 4: Optional Enhancements (Lower Priority)

| Enhancement | Effort | Impact | Target |
|-------------|--------|--------|--------|
| Route Participation Rate | High | Medium | Starter Helper |
| YAC Rate | Medium | Low | Starter Helper |
| Divisional Game Adjustment | Low | Low | Starter Helper |
| Third Down Role | Medium | Low | Starter Helper |
| Primetime Game Adjustment | Low | Low | Starter Helper |

---

## Data Source Requirements

### New Data Sources Needed

#### Adjustment Metrics (Original)

| Metric | Source | API Available | Complexity |
|--------|--------|---------------|------------|
| Target share | ESPN Stats API | Yes | Low |
| Vegas lines (O/U, spread) | DraftKings/ESPN | Yes (varies) | Medium |
| Implied team total | Calculated from Vegas | N/A | Low |
| QB quality tiers | Manual curation | N/A | Low |
| Red zone targets | ESPN Stats API | Yes | Medium |
| Snap counts | ESPN/PFF | Partial | Medium |
| Coverage data | PFF Premium | Paid | High |
| Air Yards (aDOT) | Next Gen Stats/ESPN | Partial | Medium |
| Team pass/run rate | NFL Stats | Yes | Low |
| Pressure rate | PFF/ESPN | Partial | Medium |
| Route participation | Next Gen Stats | Limited | High |
| Division schedule | NFL Schedule | Yes | Low |

#### Projection Calculation Metrics (New)

| Metric | Source | API Available | Complexity |
|--------|--------|---------------|------------|
| WOPR | Calculated (target share + air yards) | N/A | Low |
| Opportunity Share | ESPN/NFL Stats | Yes | Low |
| Expected Fantasy Points (xFP) | Next Gen Stats | Limited | High |
| FPOE/FPUE | Next Gen Stats/Fantasy Points | Limited | Medium |
| Routes Per Game | PFF/Next Gen Stats | Paid/Limited | Medium |
| Yards Per Route Run (YPRR) | PFF | Paid | Medium |
| EPA | NFL Next Gen Stats/nfelo | Yes | Medium |
| Rush Yards Over Expected (RYOE) | Next Gen Stats | Limited | High |
| Yards Before/After Contact | PFF/Next Gen Stats | Paid/Limited | Medium |
| Success Rate | NFL Stats | Yes | Low |
| True Catch Rate | PFF/Player Profiler | Paid | Medium |
| Separation | Next Gen Stats | Limited | Medium |
| Completion Probability | Next Gen Stats | Limited | High |
| Expected YAC (xYAC) | Next Gen Stats | Limited | High |
| Team Plays Per Game | NFL Stats | Yes | Low |
| Neutral Script Pass Rate | NFL Stats | Yes | Medium |
| Snap Share Trend | ESPN/PFF | Yes | Low |
| Dominator Rating | Player Profiler | Partial | Low |

### Existing Data Sources to Leverage

| Metric | Current File | Enhancement |
|--------|--------------|-------------|
| Teammate injuries | `players.csv` | Cross-reference team |
| Secondary injuries | `team_data/{TEAM}.csv` | Add key player injuries |
| Game totals | `game_data.csv` | Add Vegas O/U, spread |
| Team data | `team_data/{TEAM}.csv` | Add pass/run ratio |
| Schedule | `season_schedule.csv` | Flag divisional games |

---

## Conclusion

The current 13-step scoring algorithm provides a solid foundation covering projections, team quality, matchups, weather, and injuries. However, the Week 15 WR analysis revealed that **target volume**, **QB context**, and **game environment (Vegas lines)** are critical factors not currently captured.

**Recommended Priority (Top 5):**
1. **Vegas O/U + Implied Team Total** - Best predictor of scoring environment
2. **Target share tracking** - Direct measure of opportunity
3. **QB quality tier** - Essential context for pass-catchers
4. **Teammate injury impact** - Captures role changes
5. **Team pass rate / tempo** - Volume opportunity indicator

**Total Metrics Identified:** 19 potential scoring enhancements across 4 implementation phases.

These enhancements would address the majority of the analytical gap identified in the research comparison. Phase 1 (Quick Wins) alone would capture 80% of the value with relatively low implementation effort.

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-12 | 1.0 | Initial gap analysis from Week 15 WR research |
| 2025-12-12 | 1.1 | Added 8 additional metrics; fixed mode terminology; added Phase 4 |
| 2025-12-13 | 2.0 | Added 19 projection calculation metrics; new section for building custom projections; added projection framework; expanded data sources |

## Sources

- [BetIQ - How Projections Are Created](https://betiq.teamrankings.com/fantasy-football/strategy/official-player-projections-created/)
- [Yards Per Fantasy - How to Build Projections](https://yardsperfantasy.com/build-fantasy-football-projections/)
- [Fantasy Points - Most Important WR Stats](https://www.fantasypoints.com/nfl/articles/2023/fantasy-points-data-most-important-wr-stats)
- [PFF - Yards Per Route Run](https://www.pff.com/news/fantasy-football-metrics-that-matter-yards-per-route-run)
- [Fantasy Points - YPRR Statistical Significance](https://www.fantasypoints.com/nfl/articles/2024/statistically-significant-yards-per-route-run)
- [CBS Sports - Advanced Stats 101](https://www.cbssports.com/fantasy/football/news/fantasy-football-advanced-stats-101-the-best-new-age-data-to-consider-and-what-to-avoid/)
- [FantasyData - RB Opportunity Share](https://fantasydata.com/advanced-fantasy-metrics-rb-opportunity-share)
- [nfelo - EPA Explained](https://www.nfeloapp.com/analysis/expected-points-added-epa-nfl/)
- [NFL Next Gen Stats - 2025 Metrics](https://www.nfl.com/news/next-gen-stats-new-advanced-metrics-you-need-to-know-for-the-2025-nfl-season)
- [StatRankings - NFL Advanced Metrics](https://statrankings.com/nfl/advanced/players)
