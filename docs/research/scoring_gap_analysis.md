# Scoring Gap Analysis: Research Metrics vs. League Helper Implementation

**Generated:** December 12, 2025
**Last Updated:** December 17, 2025
**Purpose:** Compare metrics used in manual analysis to existing scoring algorithm to identify potential enhancements

---

## Executive Summary

The current 13-step scoring algorithm covers foundational metrics well but lacks several advanced metrics that proved valuable in streaming research and start/sit analysis. Key gaps include:

| Priority | Gap | Impact |
|----------|-----|--------|
| **High** | Target Volume/Share | Critical for weekly decisions |
| **High** | QB Context | Affects all pass-catchers |
| **High** | Vegas Lines/Game Script | Game environment predictor |
| **High** | Implied Team Total | More precise than O/U |
| **High** | Red Zone TD% (Team) | Kicker XP vs FG prediction |
| **Medium** | Teammate Injury Impact | Role changes |
| **Medium** | Opponent Secondary Details | Beyond aggregate defense rank |
| **Medium** | Team Pass Rate / Tempo | Volume opportunity |
| **Low** | Streak Momentum | Hot/cold beyond performance deviation |
| **Low** | Air Yards (aDOT) | Ceiling indicator |
| **Low** | Divisional Game Adjustment | Variance modifier |

**Total Potential Metrics Identified:** 58 metrics across 6 categories:
- Original gap metrics: 11
- Additional review metrics: 8
- Projection calculation metrics: 19
- **NEW: Position-specific metrics: 20** (added Dec 17, 2025)

---

## Current System: 13-Step Scoring Algorithm

### Implemented Steps

| Step | Metric | Type | Range | Mode Usage | Status |
|------|--------|------|-------|------------|--------|
| 1 | **Normalization** | Base | 0-135 scale | All modes | ✅ Implemented & Documented |
| 2 | **ADP Multiplier** | Multiplicative | 0.87-1.15x | Add To Roster | ✅ Implemented & Documented |
| 3 | **Player Rating** | Multiplicative | 0.96-1.04x | Add To Roster, Trade Sim | ✅ Implemented & Documented |
| 4 | **Team Quality** | Multiplicative | 0.91-1.09x | All modes | ✅ Implemented & Documented |
| 5 | **Performance** | Multiplicative | 0.87-1.14x | Starter Helper, Trade Sim | ✅ Implemented & Documented |
| 6 | **Matchup** | Additive | -4.6 to +4.6 pts | Starter Helper | ✅ Implemented & Documented |
| 7 | **Schedule** | Additive | -4.3 to +4.3 pts | Trade Sim | ✅ Implemented & Documented |
| 8 | **Draft Order** | Additive | 0 to +80 pts | Add To Roster | ✅ Implemented & Documented |
| 9 | **Bye Week** | Penalty | 0 to -50 pts | Add To Roster, Trade Sim (User) | ✅ Implemented & Documented |
| 10 | **Injury** | Penalty | 0 to -100 pts | Add To Roster | ✅ Implemented & Documented |
| 11 | **Temperature** | Additive | -2.5 to +2.5 pts | Starter Helper | ✅ **FULLY IMPLEMENTED** (v2.1, Nov 2025) |
| 12 | **Wind** | Additive | -3.0 to +3.0 pts | Starter Helper (QB/WR/K) | ✅ **FULLY IMPLEMENTED** (v2.1, Nov 2025) |
| 13 | **Location** | Additive | -5 to +2 pts | Starter Helper | ✅ **FULLY IMPLEMENTED** (v2.1, Nov 2025) |

*Note: Steps 11-13 (Game Conditions) were added in v2.1 (2025-11-26) and are fully operational with comprehensive test coverage (161 tests). See `docs/scoring/11_temperature_scoring.md`, `12_wind_scoring.md`, and `13_location_scoring.md` for complete documentation.*

---

## Research Metrics Comparison

### Metrics ALREADY Covered by System

| Research Metric | System Step | Coverage Quality | Implementation Status | Notes |
|-----------------|-------------|------------------|----------------------|-------|
| **Projections** | Step 1 (Normalization) | Excellent | ✅ v1.0 (2024) | ESPN weekly/ROS projections |
| **Matchup Quality** | Step 6 (Matchup) | Good | ✅ v1.0 (2024) | Position-specific defense ranks |
| **Recent Performance** | Step 5 (Performance) | Good | ✅ v1.0 (2024) | Actual vs projected deviation |
| **Temperature** | Step 11 | Good | ✅ **v2.1 (Nov 2025)** | Ideal ~60°F, all positions, ±2.5 pts |
| **Wind** | Step 12 | Good | ✅ **v2.1 (Nov 2025)** | QB/WR/K only, ±3.0 pts |
| **Location** | Step 13 | Good | ✅ **v2.1 (Nov 2025)** | Home/away/international, -5 to +2 pts |
| **Injury Status** | Step 10 | Good | ✅ v1.0 (2024) | ACTIVE/QUESTIONABLE/OUT/IR |
| **Schedule Strength** | Step 7 | Good | ✅ v1.0 (2024) | Future opponent avg defense rank |
| **Team Quality** | Step 4 | Good | ✅ v1.0 (2024) | Offensive/defensive rankings |

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
| **Position Applicability** | WR, TE (primary); RB (secondary for PPR) |

```
Proposed Thresholds (WR/TE):
- EXCELLENT: ≥25% target share (+3.0 pts)
- GOOD: 20-24% target share (+1.5 pts)
- AVERAGE: 15-19% target share (0 pts)
- POOR: 10-14% target share (-1.5 pts)
- VERY_POOR: <10% target share (-3.0 pts)

Proposed Thresholds (RB):
- EXCELLENT: ≥8 targets/game (+2.5 pts)
- GOOD: 5-7 targets/game (+1.5 pts)
- AVERAGE: 3-4 targets/game (0 pts)
- POOR: 1-2 targets/game (-1.0 pts)
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
| **Position Applicability** | WR, TE (critical); K (secondary - affects scoring drives) |

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
| **Position Applicability** | QB (primary); impacts all their pass-catchers (WR/TE); K (field conditions) |

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
| **Position Applicability** | ALL positions (universal game environment factor) |

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
| **Position Applicability** | WR, TE, RB (primary); K (secondary - affects scoring) |

```
Proposed Implementation:
- Primary teammate OUT: +15% score boost
- Primary teammate DOUBTFUL: +8% score boost
- Primary teammate QUESTIONABLE: +3% score boost

Position-Specific:
- WR: When WR1 out, WR2 becomes primary target
- RB: When RB1 out, RB2 gets full workload
- TE: When TE1 out, TE2 gets all targets
- K: When star WR/RB out, offense may struggle in red zone = more FG attempts
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
| **Position Applicability** | WR, TE (primary); QB (secondary) |

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
| Implementation | Bonus based on red zone target/carry share percentile |
| **Position Applicability** | ALL skill positions (critical TD predictor) |

```
Position-Specific Thresholds:

WR/TE:
- EXCELLENT: ≥20% red zone target share (+2.5 pts)
- GOOD: 15-19% (+1.5 pts)
- AVERAGE: 10-14% (0 pts)
- POOR: <10% (-1.0 pts)

RB:
- EXCELLENT: ≥60% goal-line carries (+3.0 pts)
- GOOD: 40-59% (+1.5 pts)
- AVERAGE: 20-39% (0 pts)
- POOR: <20% (-1.5 pts)
```

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
| **Position Applicability** | ALL positions (universal trend indicator) |

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
| **Position Applicability** | RB (critical); WR/TE (important) |

```
Position-Specific Thresholds:

RB:
- EXCELLENT: ≥70% snap share (+2.5 pts) [workhorse]
- GOOD: 55-69% (+1.5 pts) [lead back]
- AVERAGE: 40-54% (0 pts) [committee]
- POOR: <40% (-1.5 pts) [backup]

WR/TE:
- EXCELLENT: ≥85% snap share (+2.0 pts)
- GOOD: 70-84% (+1.0 pts)
- AVERAGE: 50-69% (0 pts)
- POOR: <50% (-1.0 pts)
```

---

**10. Coverage Type Tendencies**

| Attribute | Details |
|-----------|---------|
| Description | Single-high vs two-high safety, zone vs man coverage |
| Research Use | Steelers play 5th-most single-high (Waddle thrives against) |
| Why Important | Certain players excel vs specific coverage types |
| Complexity | High - requires player-coverage matchup data |
| Suggested Step | Long-term enhancement to Step 6 |
| **Position Applicability** | WR (primary); TE (secondary) |

---

**11. Primetime Game Adjustment**

| Attribute | Details |
|-----------|---------|
| Description | Performance variance in MNF/SNF/TNF games |
| Research Use | Waddle MNF in Pittsburgh noted as risk factor |
| Why Important | Some players/teams perform differently in primetime |
| Data Source | Historical primetime game logs |
| Suggested Step | New optional Step |
| **Position Applicability** | ALL positions (NOTE: Guide says NEVER use day-of-week as factor; this would need to be player-specific performance data only) |
| **IMPORTANT** | Do NOT apply generic TNF/MNF/SNF modifiers - only use if player has documented primetime performance variance |

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
| **Position Applicability** | ALL positions (more precise than O/U) |

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
| **Position Applicability** | WR (primary); TE (secondary - usually lower aDOT) |

```
Proposed Thresholds (WR):
- EXCELLENT: ≥14.0 aDOT (+2.0 pts ceiling boost)
- GOOD: 11.0-13.9 aDOT (+1.0 pts)
- AVERAGE: 8.0-10.9 aDOT (0 pts)
- POOR: 5.0-7.9 aDOT (-0.5 pts)
- VERY_POOR: <5.0 aDOT (-1.0 pts)

Proposed Thresholds (TE):
- EXCELLENT: ≥10.0 aDOT (+1.5 pts)
- GOOD: 7.0-9.9 aDOT (+0.5 pts)
- AVERAGE: 4.0-6.9 aDOT (0 pts)
- POOR: <4.0 aDOT (-0.5 pts)
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
| **Position Applicability** | WR (primary); TE (secondary); RB (critical for receiving value) |

---

**15. Team Pass Rate / Plays Per Game**

| Attribute | Details |
|-----------|---------|
| Description | Team's passing frequency and overall tempo |
| Why Important | High-volume passing teams create more WR/TE opportunity |
| Research Use | Lions lead NFL in plays/game, boosting all skill players |
| Data Source | NFL team stats |
| Suggested Step | Enhance Team Quality (Step 4) |
| **Position Applicability** | WR/TE (high pass rate); RB (high run rate) |

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
| **Position Applicability** | QB (primary); WR/TE (secondary); RB (affects pass-catching) |

---

**17. Route Participation Rate**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of pass plays where WR runs a route |
| Why Important | Direct measure of involvement in passing game |
| Data Source | Next Gen Stats, PFF |
| Suggested Step | Combine with Target Share |
| Complexity | Medium-High |
| **Position Applicability** | WR, TE only |

---

**18. Divisional Game Adjustment**

| Attribute | Details |
|-----------|---------|
| Description | Performance variance in divisional matchups |
| Why Important | More game film, higher stakes, defensive familiarity |
| Research Use | Divisional games often have lower scoring, tighter coverage |
| Data Source | NFL schedule (division identification) |
| Suggested Step | New optional Step |
| **Position Applicability** | ALL positions (universal variance modifier) |

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
| **Position Applicability** | WR/TE (3rd down targets); RB (3rd down back role) |

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
| **Position Applicability** | WR, TE only |

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
| **Position Applicability** | RB only |

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
| **Position Applicability** | ALL positions |

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
| **Position Applicability** | ALL positions |

---

**24. Routes Per Game / Snaps Per Game**

| Attribute | Details |
|-----------|---------|
| Description | Total route-running opportunities for pass-catchers |
| Why Important | More routes = more target opportunities |
| Data Source | PFF, Next Gen Stats |
| Use Case | WR/TE opportunity ceiling |
| **Position Applicability** | WR, TE only |

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
| **Position Applicability** | WR (primary); TE (secondary) |

```
Benchmarks (WR):
- Elite: ≥2.50 YPRR
- Good: 2.00-2.49 YPRR
- Average: 1.50-1.99 YPRR
- Poor: <1.50 YPRR

Benchmarks (TE):
- Elite: ≥2.00 YPRR
- Good: 1.50-1.99 YPRR
- Average: 1.00-1.49 YPRR
- Poor: <1.00 YPRR
```

---

**26. Expected Points Added (EPA)**

| Attribute | Details |
|-----------|---------|
| Description | How much a play increases/decreases scoring probability |
| Why Important | Measures true value of each play in context |
| Data Source | NFL Next Gen Stats, nfelo |
| Use Case | Team/player efficiency evaluation |
| **Position Applicability** | ALL positions |

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
| **Position Applicability** | RB only |

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
| **Position Applicability** | RB only |

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
| **Position Applicability** | RB (primary); QB (secondary) |

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
| **Position Applicability** | WR, TE, RB (receiving) |

---

### Next Gen Stats Metrics

**31. Separation**

| Attribute | Details |
|-----------|---------|
| Description | Yards between receiver and nearest defender at catch point |
| Why Important | Open receivers = easier completions = more targets |
| Data Source | NFL Next Gen Stats |
| Use Case | WR skill + scheme evaluation |
| **Position Applicability** | WR (primary); TE (secondary) |

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
| **Position Applicability** | QB (primary); WR/TE (secondary) |

---

**33. Expected YAC (xYAC)**

| Attribute | Details |
|-----------|---------|
| Description | Predicted yards after catch based on field position, defenders nearby |
| Why Important | YAC over expected = playmaker ability |
| Data Source | NFL Next Gen Stats |
| Use Case | WR ceiling projection |
| **Position Applicability** | WR, TE, RB (receiving) |

---

### Team-Level Projection Factors

**34. Team Plays Per Game**

| Attribute | Details |
|-----------|---------|
| Description | Total offensive snaps/plays run per game |
| Why Important | More plays = more opportunities for all skill players |
| Data Source | NFL Stats |
| Use Case | Team-level projection multiplier |
| **Position Applicability** | ALL positions |

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
| **Position Applicability** | WR/TE (pass-heavy); RB (run-heavy) |

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
| **Position Applicability** | ALL skill positions |

---

### Role-Based Projection Factors

**37. Snap Share Trend**

| Attribute | Details |
|-----------|---------|
| Description | Week-over-week change in snap percentage |
| Why Important | Increasing snap share = emerging role |
| Data Source | ESPN, PFF |
| Use Case | Identify breakout candidates |
| **Position Applicability** | ALL positions (critical for RB/WR/TE) |

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
| **Position Applicability** | WR, TE (rookies only) |

```
Elite Dominator: ≥35%
Good: 25-34%
Average: 20-24%
Poor: <20%
```

---

## POSITION-SPECIFIC METRICS (NEW Section - Dec 17, 2025)

The following metrics apply differently to specific positions or are only relevant to certain positions. These were identified from streaming research guides.

---

### KICKER-SPECIFIC METRICS (Critical for K Streaming)

**39. Team Red Zone TD Percentage**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of red zone trips that result in touchdowns |
| Why Important | High RZ TD% = more XPs; Low RZ TD% = more FG attempts |
| Research Use | Eagles 71% RZ TD% (2025) = strong XP volume |
| Data Source | NFL Stats, Team Rankings |
| Suggested Step | New Step for K scoring only |
| Implementation | Inverse relationship: Lower TD% = more FG opportunities |
| **Position Applicability** | K only (critical) |

```
Proposed Implementation for Kicker Scoring:

HIGH TD% (Lots of XPs, Fewer FGs):
- ≥65% TD rate: +1.5 pts (reliable XP volume)
- 55-64%: +0.5 pts (balanced)
- 45-54%: 0 pts (average)

LOW TD% (More FGs, Fewer XPs):
- 35-44%: +1.0 pts (more FG opportunities)
- <35%: +2.0 pts (high FG volume but team may struggle)

Note: Balance between XP reliability and FG opportunity
```

---

**40. Kicker Accuracy by Distance**

| Attribute | Details |
|-----------|---------|
| Description | FG% for different distance ranges (0-39, 40-49, 50+) |
| Why Important | 2025 saw record accuracy (72.5% from 50+); trust big-leg kickers |
| Research Use | Cam Little 68-yard NFL record; league-wide 84.7% FG% |
| Data Source | NFL Stats, ESPN |
| Suggested Step | Enhance K scoring with accuracy modifiers |
| Implementation | Bonus for elite accuracy, especially long-range |
| **Position Applicability** | K only |

```
Proposed Accuracy Tiers:

50+ Yard Accuracy:
- Elite (≥70%): +2.0 pts
- Good (60-69%): +1.0 pts
- Average (50-59%): 0 pts
- Poor (<50%): -1.0 pts

Overall Accuracy (All distances):
- Elite (≥90%): +1.5 pts
- Good (85-89%): +0.5 pts
- Average (80-84%): 0 pts
- Poor (<80%): -1.5 pts
```

---

**41. Dome vs Outdoor (Kicker Venue Impact)**

| Attribute | Details |
|-----------|---------|
| Description | Whether game is in dome (controlled) or outdoor (weather variables) |
| Why Important | Dome games eliminate weather risk for kickers |
| Research Use | Week 16 K rankings: SF @ IND (dome) #1, LAR @ SEA (outdoor, wind) #2 |
| Current Coverage | Partially covered by Step 13 (Location) and Step 12 (Wind) |
| Gap | Need explicit dome preference for K position |
| Suggested Enhancement | Enhance Step 13 with K-specific dome bonus |
| **Position Applicability** | K (primary); QB/WR (secondary via wind/temp) |

```
Proposed Implementation for Kickers:
- Dome game: +2.0 pts (no weather variables)
- Retractable roof (closed): +1.5 pts
- Outdoor (mild weather <40°F, <10mph wind): 0 pts
- Outdoor (cold 30-40°F OR 10-15mph wind): -1.5 pts
- Outdoor (extreme <30°F OR 15+ mph wind): -3.0 pts
```

---

### TIGHT END-SPECIFIC METRICS

**42. Route Participation Rate (TE-Specific)**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of pass plays where TE runs a route |
| Why Important | TEs with 70%+ route share are locked in as pass-catchers |
| Research Use | TE streaming guide: "70%+ = elite for TE" |
| Data Source | Next Gen Stats, PFF |
| Suggested Step | New Step (combine with snap share) |
| Implementation | Bonus for high route participation |
| **Position Applicability** | TE (critical); WR (less critical as most run routes) |

```
TE Route Share Thresholds:
- EXCELLENT: ≥70% route share (+2.5 pts)
- GOOD: 55-69% (+1.5 pts)
- AVERAGE: 40-54% (0 pts)
- POOR: <40% (-1.5 pts)
```

---

**43. Red Zone Target Efficiency (TE-Specific)**

| Attribute | Details |
|-----------|---------|
| Description | TD conversion rate on red zone targets |
| Why Important | TEs with high RZ efficiency are TD-dependent streamers |
| Research Use | "Track X/Y format (e.g., 9/10)" from TE streaming guide |
| Data Source | ESPN, NFL Stats |
| Suggested Step | Enhance Red Zone Opportunity metric |
| Implementation | Bonus for high TD conversion in RZ |
| **Position Applicability** | TE (primary); WR (secondary) |

```
TE Red Zone TD Efficiency:
- EXCELLENT: ≥50% TD rate on RZ targets (+2.0 pts)
- GOOD: 35-49% (+1.0 pts)
- AVERAGE: 20-34% (0 pts)
- POOR: <20% (-1.0 pts)
```

---

**44. EPA Per Target (TE-Specific)**

| Attribute | Details |
|-----------|---------|
| Description | Expected Points Added per target received |
| Why Important | Advanced efficiency metric showing value per opportunity |
| Research Use | "EPA per target: +0.3+ = elite" from TE streaming guide |
| Data Source | NFL Next Gen Stats |
| Suggested Step | New Step for TE efficiency |
| Implementation | Bonus for high EPA/target |
| **Position Applicability** | TE (primary metric in guide); WR (secondary) |

```
EPA Per Target Thresholds (TE):
- EXCELLENT: ≥+0.30 EPA/target (+2.0 pts)
- GOOD: +0.15 to +0.29 (+1.0 pts)
- AVERAGE: 0.00 to +0.14 (0 pts)
- POOR: <0.00 (-1.0 pts)
```

---

**45. Role Security (TE-Specific)**

| Attribute | Details |
|-----------|---------|
| Description | Whether backup TE is injured or active |
| Why Important | TEs with no competition get all targets |
| Research Use | "Is backup TE injured? Locked = no competition" |
| Data Source | Team depth charts, injury reports |
| Suggested Step | Enhance Teammate Injury Impact |
| Implementation | Bonus when TE2 is OUT |
| **Position Applicability** | TE only (unique position characteristic) |

```
TE Role Security:
- TE1 with TE2/TE3 OUT: +2.0 pts (no competition)
- TE1 with TE2 active but limited: +0.5 pts
- TE1 in committee: -1.0 pts
```

---

### RUNNING BACK-SPECIFIC METRICS

**46. Goal-Line Role**

| Attribute | Details |
|-----------|---------|
| Description | Who gets carries inside the 5-yard line |
| Why Important | Goal-line role determines TD equity |
| Research Use | "Goal-line role: Yes/No/Split" from RB data points |
| Data Source | ESPN situational stats |
| Suggested Step | Enhance Red Zone Opportunity |
| Implementation | Major bonus for exclusive goal-line back |
| **Position Applicability** | RB only |

```
Goal-Line Role Thresholds:
- EXCELLENT: Exclusive goal-line back (90%+ carries) (+3.5 pts)
- GOOD: Primary goal-line back (60-89%) (+2.0 pts)
- SPLIT: Shares goal-line duties (40-59%) (0 pts)
- POOR: Not used at goal-line (<40%) (-2.0 pts)
```

---

**47. TD Equity (RB-Specific)**

| Attribute | Details |
|-----------|---------|
| Description | Season TD rate vs opportunity (carries + targets) |
| Why Important | Identifies RBs with high/low TD probability |
| Research Use | "TD equity: High/Moderate/Low" from RB guide |
| Data Source | ESPN stats |
| Suggested Step | New Step for RB TD probability |
| Implementation | Bonus/penalty based on TD rate vs touches |
| **Position Applicability** | RB (primary); WR/TE (secondary) |

```
RB TD Equity (TDs per 100 touches):
- EXCELLENT: ≥8 TDs per 100 touches (+2.0 pts)
- GOOD: 5-7 TDs per 100 touches (+1.0 pts)
- AVERAGE: 3-4 TDs per 100 touches (0 pts)
- POOR: <3 TDs per 100 touches (-1.0 pts)
```

---

**48. Yards Before Contact (RB O-Line Quality)**

| Attribute | Details |
|-----------|---------|
| Description | Average yards gained before first contact |
| Why Important | Indicates O-line blocking quality (affects RB scoring) |
| Research Use | "Yards before contact: O-line quality indicator" |
| Data Source | PFF, Next Gen Stats |
| Suggested Step | Enhance Team Quality for RBs |
| Implementation | Bonus for good blocking, penalty for poor |
| **Position Applicability** | RB only |

```
Yards Before Contact:
- EXCELLENT: ≥3.0 YBC (+2.0 pts) [elite blocking]
- GOOD: 2.0-2.9 YBC (+1.0 pts)
- AVERAGE: 1.0-1.9 YBC (0 pts)
- POOR: <1.0 YBC (-1.5 pts) [bad O-line]
```

---

**49. Role Designation (RB Workload Type)**

| Attribute | Details |
|-----------|---------|
| Description | Lead back / Committee / Backup classification |
| Why Important | Determines floor and ceiling based on workload security |
| Research Use | "Role designation: Lead back / Committee / Backup" |
| Data Source | Depth charts, snap share, touch distribution |
| Suggested Step | New Step for RB floor/ceiling modifier |
| Implementation | Major impact on projection reliability |
| **Position Applicability** | RB only |

```
RB Role Impact on Scoring:
- WORKHORSE (70%+ snaps, 70%+ touches): +3.0 pts (highest floor)
- LEAD BACK (55-69% snaps, 60%+ touches): +1.5 pts
- COMMITTEE (40-54% snaps, 40-59% touches): 0 pts (volatile)
- CHANGE OF PACE (<40% snaps, <40% touches): -2.0 pts (low floor)
```

---

**50. Carries Per Game (RB Volume Floor)**

| Attribute | Details |
|-----------|---------|
| Description | Average rushing attempts per game |
| Why Important | 15+ carries = reliable volume floor |
| Research Use | "Carries per game: 15+ = reliable" from RB guide |
| Data Source | ESPN, NFL Stats |
| Suggested Step | Enhance or replace current projection |
| Implementation | Volume threshold for startability |
| **Position Applicability** | RB only |

```
RB Carry Volume:
- EXCELLENT: ≥20 carries/game (+3.0 pts) [bell cow]
- GOOD: 15-19 carries/game (+1.5 pts) [reliable]
- AVERAGE: 10-14 carries/game (0 pts)
- POOR: 5-9 carries/game (-1.5 pts)
- VERY_POOR: <5 carries/game (-3.0 pts)
```

---

**51. Opponent Run Defense DVOA (RB Matchup Quality)**

| Attribute | Details |
|-----------|---------|
| Description | Defense-adjusted value over average for run defense |
| Why Important | More precise than generic "defense rank" |
| Research Use | "Opponent run defense DVOA: Recent 5-week trend matters" |
| Data Source | Football Outsiders DVOA |
| Suggested Step | Enhance Step 6 (Matchup) for RBs |
| Implementation | RB-specific defensive matchup metric |
| **Position Applicability** | RB only |

```
Opponent Run Defense DVOA (Recent 5 weeks):
- EXCELLENT: ≥15% DVOA (worst run D) (+3.0 pts)
- GOOD: +5% to +14% DVOA (+1.5 pts)
- AVERAGE: -5% to +4% DVOA (0 pts)
- POOR: -15% to -6% DVOA (-1.5 pts)
- VERY_POOR: ≤-15% DVOA (elite run D) (-3.0 pts)
```

---

### QUARTERBACK-SPECIFIC METRICS

**52. Rushing Upside (Dual-Threat QBs)**

| Attribute | Details |
|-----------|---------|
| Description | Rushing yards and TD potential |
| Why Important | 30+ rush yards adds significant floor boost |
| Research Use | "Rushing upside: 30+ rush yards = bonus" from QB guide |
| Data Source | ESPN, NFL Stats |
| Suggested Step | New Step for QB rushing bonus |
| Implementation | Additive bonus for dual-threat QBs |
| **Position Applicability** | QB only |

```
QB Rushing Yards Per Game:
- EXCELLENT: ≥50 rush yds/game (+4.0 pts) [elite dual-threat]
- GOOD: 30-49 rush yds/game (+2.5 pts) [mobile QB]
- AVERAGE: 15-29 rush yds/game (+1.0 pts)
- POOR: <15 rush yds/game (0 pts) [pocket passer]

QB Rushing TDs (Season Rate):
- High (≥6 rush TDs in season): +2.0 pts
- Medium (3-5 rush TDs): +1.0 pts
- Low (<3 rush TDs): 0 pts
```

---

**53. Pass Attempts Per Game (QB Volume)**

| Attribute | Details |
|-----------|---------|
| Description | Average pass attempts per game |
| Why Important | 35+ attempts = high volume opportunity |
| Research Use | "Pass attempts per game: 35+ = high volume" from QB guide |
| Data Source | ESPN, NFL Stats |
| Suggested Step | New Step for QB volume bonus |
| Implementation | Bonus for high-volume passers |
| **Position Applicability** | QB (primary); affects WR/TE (secondary) |

```
QB Pass Attempts Per Game:
- EXCELLENT: ≥40 attempts/game (+2.5 pts) [volume leader]
- GOOD: 35-39 attempts/game (+1.5 pts) [high volume]
- AVERAGE: 28-34 attempts/game (0 pts)
- POOR: <28 attempts/game (-1.5 pts) [run-heavy offense]
```

---

**54. O-Line Health (QB Protection)**

| Attribute | Details |
|-----------|---------|
| Description | Number of starting O-linemen active |
| Why Important | QB needs time to throw; injured O-line = sacks/pressure |
| Research Use | "O-line health: Time to throw - Track specific injuries" |
| Data Source | Team injury reports, depth charts |
| Suggested Step | Enhance Team Quality for QB |
| Implementation | Penalty when multiple O-line starters OUT |
| **Position Applicability** | QB (primary); RB (secondary - affects run game) |

```
O-Line Health Impact (QB):
- All 5 starters active: +1.5 pts
- 1 starter OUT: 0 pts
- 2 starters OUT: -1.5 pts
- 3+ starters OUT: -3.0 pts (significant downgrade)
```

---

**55. Cold Weather History (QB-Specific)**

| Attribute | Details |
|-----------|---------|
| Description | Historical performance in games under 40°F |
| Why Important | Some QBs have documented struggles in cold (Tua: 0-5 under 40°F) |
| Current Coverage | Partially covered by Step 11 (Temperature) |
| Gap | Need QB-specific cold weather modifiers beyond generic temp adjustment |
| Suggested Enhancement | Create QB cold-weather table for known poor performers |
| **Position Applicability** | QB (affects all their pass-catchers) |

```
QB Cold Weather Performance Tiers:
- STRONG: Career winning record + good stats in cold (0 pts)
- AVERAGE: No significant trend (0 pts)
- POOR: Documented struggles (<50% completion, 0-X record): -3.0 pts
- APPLY TO PASS-CATCHERS: If QB has POOR cold history, apply 0.85x to all WR/TE
```

---

### WIDE RECEIVER-SPECIFIC METRICS

**56. First-Read Share (WR Target Quality)**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of plays where WR is QB's first look |
| Why Important | First-read targets are higher quality (more likely to convert) |
| Research Use | "First-read share %: 15%+ = primary option" from WR guide |
| Data Source | PFF, Next Gen Stats |
| Suggested Step | New Step for WR target quality |
| Implementation | Bonus for high first-read share |
| **Position Applicability** | WR only |

```
WR First-Read Share:
- EXCELLENT: ≥20% first-read share (+2.5 pts) [clear WR1]
- GOOD: 15-19% (+1.5 pts) [primary option]
- AVERAGE: 10-14% (0 pts)
- POOR: <10% (-1.0 pts) [secondary option]
```

---

**57. Air Yard Share (WR Deep Threat Role)**

| Attribute | Details |
|-----------|---------|
| Description | Percentage of team's total air yards |
| Why Important | 30%+ = deep threat; indicates ceiling potential |
| Research Use | "Air yard share %: 30%+ = deep threat" from WR guide |
| Data Source | ESPN, Next Gen Stats |
| Suggested Step | Combine with aDOT metric |
| Implementation | Bonus for high air yard share |
| **Position Applicability** | WR (primary); TE (less relevant) |

```
WR Air Yard Share:
- EXCELLENT: ≥35% air yard share (+3.0 pts) [elite deep threat]
- GOOD: 25-34% (+1.5 pts) [primary deep option]
- AVERAGE: 15-24% (0 pts)
- POOR: <15% (-1.0 pts) [underneath only]
```

---

**58. Shadow Coverage Matchup (WR-Specific)**

| Attribute | Details |
|-----------|---------|
| Description | Whether WR faces shadow CB (follows WR everywhere) |
| Why Important | Elite shadow CBs significantly limit production |
| Research Use | "Opponent CB injuries: Shadow CB = concern" from WR guide |
| Data Source | Team defensive schemes, PFF |
| Suggested Step | Enhance Opponent Secondary Details |
| Implementation | Penalty when facing elite shadow CB |
| **Position Applicability** | WR only (TEs rarely shadowed) |

```
Shadow Coverage Impact:
- Facing elite shadow CB (Ramsey, Diggs, etc.): -3.0 pts
- Facing average shadow CB: -1.5 pts
- No shadow coverage: 0 pts
- Shadowing CB injured/out: +2.0 pts
```

---

## EXISTING METRICS WITH POSITION-SPECIFIC APPLICATIONS

Some metrics already in the scoring algorithm apply differently to different positions. These should be documented:

---

**Wind (Step 12) - Position-Specific Impact**

| Current Implementation | Step 12 applies to QB/WR/K |
|------------------------|----------------------------|
| **QB:** High wind (15+ mph) significantly reduces deep passing accuracy (-3.0 pts) |
| **WR:** Deep threats more affected than slot receivers; 20+ mph wind = avoid WR entirely |
| **K:** 15+ mph wind reduces FG accuracy, especially 45+ yards; 20+ mph = avoid kicker entirely |
| **TE:** Less affected (shorter routes, middle of field) - suggest reduced penalty |
| **RB:** Minimal impact on rushing, slight impact on receiving |

```
Suggested Position-Specific Wind Penalties:
- QB: Current implementation (up to -3.0 pts at 20+ mph)
- WR (Deep threats, aDOT 12+): Current implementation (-3.0 pts at 20+ mph)
- WR (Underneath, aDOT <8): Reduced penalty (-1.5 pts at 20+ mph)
- K: Current implementation (up to -3.0 pts at 20+ mph)
- TE: Reduced penalty (-1.5 pts at 20+ mph)
- RB: Minimal penalty (-0.5 pts at 20+ mph for receiving-heavy backs)
```

---

**Temperature (Step 11) - Position-Specific Impact**

| Current Implementation | Step 11 applies to all positions |
|------------------------|----------------------------------|
| **QB:** Major impact on passing efficiency, especially <40°F |
| **WR/TE:** Indirect impact via QB performance + ball handling |
| **RB:** Minimal impact (rushing less affected by cold) |
| **K:** Significant impact on long FGs (45+ yards) in <40°F |

```
Suggested Position-Specific Temperature Penalties:
- QB: Current implementation (up to -2.5 pts at extremes)
- WR/TE: 80% of QB penalty (via QB performance impact)
- K: Full penalty for cold (<40°F) affecting 45+ yard attempts
- RB: 20% of current penalty (rushing less affected)
```

---

**Location (Step 13) - Position-Specific Impact**

| Current Implementation | Step 13: Home/away/international |
|------------------------|----------------------------------|
| **All positions:** Home advantage applies universally, but magnitude varies |

```
Current home/away bonus should potentially vary by position:
- QB: Full home advantage (+2.0 pts home, -1.5 pts away)
- K: Enhanced home advantage (+2.5 pts home - familiar conditions)
- RB/WR/TE: Standard home advantage (+1.5 pts home, -1.0 pts away)
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

| Enhancement | Effort | Impact | Target | Position |
|-------------|--------|--------|--------|----------|
| Vegas O/U integration | Medium | High | Starter Helper | ALL |
| Implied Team Total | Low | High | Starter Helper | ALL |
| QB Quality tier | Low | High | Starter Helper | WR/TE/K |
| Teammate injury boost | Medium | High | All modes | WR/TE/RB |
| Team RZ TD% | Low | High | Starter Helper | K |
| Dome vs Outdoor (K) | Low | High | Starter Helper | K |

### Phase 2: Data Enrichment (Medium Effort)

| Enhancement | Effort | Impact | Target | Position |
|-------------|--------|--------|--------|----------|
| Target share tracking | Medium | High | Starter Helper | WR/TE |
| Team Pass Rate / Tempo | Low | Medium | Starter Helper | ALL |
| Red zone opportunity | Medium | Medium | Starter Helper | ALL |
| Opponent secondary injuries | Medium | Medium | Starter Helper | WR/TE |
| Route participation (TE) | Medium | High | Starter Helper | TE |
| Goal-line role (RB) | Low | High | Starter Helper | RB |
| Rushing upside (QB) | Low | High | Starter Helper | QB |

### Phase 3: Advanced Analytics (High Effort)

| Enhancement | Effort | Impact | Target | Position |
|-------------|--------|--------|--------|----------|
| Player-specific weather models | High | Medium | Starter Helper | QB (affects WR/TE) |
| Coverage type matchups | High | Medium | Starter Helper | WR |
| Air Yards (aDOT) | Medium | Medium | Starter Helper | WR |
| Pressure Rate / QB Protection | Medium | Medium | Starter Helper | QB/WR/TE/RB |
| Streak momentum scoring | Low | Low | All modes | ALL |
| WOPR calculation | Medium | High | Starter Helper | WR/TE |
| YPRR tracking | Medium | High | Starter Helper | WR/TE |

### Phase 4: Optional Enhancements (Lower Priority)

| Enhancement | Effort | Impact | Target | Position |
|-------------|--------|--------|--------|----------|
| Route Participation Rate | High | Medium | Starter Helper | WR/TE |
| YAC Rate | Medium | Low | Starter Helper | WR/TE/RB |
| Divisional Game Adjustment | Low | Low | Starter Helper | ALL |
| Third Down Role | Medium | Low | Starter Helper | WR/TE/RB |
| Primetime Game Adjustment | Low | Low | Starter Helper | ALL (player-specific only) |
| Shadow coverage tracking | High | Medium | Starter Helper | WR |
| EPA per target (TE) | Medium | Medium | Starter Helper | TE |

---

## Data Source Requirements

### New Data Sources Needed

#### Adjustment Metrics (Original)

| Metric | Source | API Available | Complexity | Position |
|--------|--------|---------------|------------|----------|
| Target share | ESPN Stats API | Yes | Low | WR/TE/RB |
| Vegas lines (O/U, spread) | DraftKings/ESPN | Yes (varies) | Medium | ALL |
| Implied team total | Calculated from Vegas | N/A | Low | ALL |
| QB quality tiers | Manual curation | N/A | Low | QB/WR/TE/K |
| Red zone targets | ESPN Stats API | Yes | Medium | WR/TE/RB |
| Snap counts | ESPN/PFF | Partial | Medium | ALL |
| Coverage data | PFF Premium | Paid | High | WR/TE |
| Air Yards (aDOT) | Next Gen Stats/ESPN | Partial | Medium | WR/TE |
| Team pass/run rate | NFL Stats | Yes | Low | ALL |
| Pressure rate | PFF/ESPN | Partial | Medium | QB/OL |
| Route participation | Next Gen Stats | Limited | High | WR/TE |
| Division schedule | NFL Schedule | Yes | Low | ALL |
| Team RZ TD% | NFL Stats | Yes | Low | K |
| Kicker accuracy by distance | ESPN/NFL Stats | Yes | Low | K |

#### Projection Calculation Metrics (New)

| Metric | Source | API Available | Complexity | Position |
|--------|--------|---------------|------------|----------|
| WOPR | Calculated (target share + air yards) | N/A | Low | WR/TE |
| Opportunity Share | ESPN/NFL Stats | Yes | Low | RB |
| Expected Fantasy Points (xFP) | Next Gen Stats | Limited | High | ALL |
| FPOE/FPUE | Next Gen Stats/Fantasy Points | Limited | Medium | ALL |
| Routes Per Game | PFF/Next Gen Stats | Paid/Limited | Medium | WR/TE |
| Yards Per Route Run (YPRR) | PFF | Paid | Medium | WR/TE |
| EPA | NFL Next Gen Stats/nfelo | Yes | Medium | ALL |
| Rush Yards Over Expected (RYOE) | Next Gen Stats | Limited | High | RB |
| Yards Before/After Contact | PFF/Next Gen Stats | Paid/Limited | Medium | RB |
| Success Rate | NFL Stats | Yes | Low | RB/QB |
| True Catch Rate | PFF/Player Profiler | Paid | Medium | WR/TE/RB |
| Separation | Next Gen Stats | Limited | Medium | WR/TE |
| Completion Probability | Next Gen Stats | Limited | High | QB/WR/TE |
| Expected YAC (xYAC) | Next Gen Stats | Limited | High | WR/TE/RB |
| Team Plays Per Game | NFL Stats | Yes | Low | ALL |
| Neutral Script Pass Rate | NFL Stats | Yes | Medium | ALL |
| Snap Share Trend | ESPN/PFF | Yes | Low | ALL |
| Dominator Rating | Player Profiler | Partial | Low | WR/TE (rookies) |

#### Position-Specific Metrics (New - Dec 17, 2025)

| Metric | Source | API Available | Complexity | Position |
|--------|--------|---------------|------------|----------|
| Team RZ TD% | NFL Stats | Yes | Low | K |
| Kicker accuracy (0-39, 40-49, 50+) | NFL Stats/ESPN | Yes | Low | K |
| TE Route Participation | PFF/Next Gen | Paid/Limited | Medium | TE |
| TE EPA per target | Next Gen Stats | Limited | Medium | TE |
| TE Role Security | Depth charts/injuries | Manual | Low | TE |
| RB Goal-line role | ESPN situational | Yes | Low | RB |
| RB TD Equity | ESPN stats | Yes | Low | RB |
| RB Role designation | Depth charts/snap share | Manual/API | Low | RB |
| RB Yards before contact | PFF/Next Gen | Paid/Limited | Medium | RB |
| RB Carries per game | ESPN/NFL Stats | Yes | Low | RB |
| Run Defense DVOA | Football Outsiders | Yes (paid) | Medium | RB |
| QB Rushing yards/TDs | ESPN/NFL Stats | Yes | Low | QB |
| QB Pass attempts/game | ESPN/NFL Stats | Yes | Low | QB |
| QB O-line health | Injury reports | Manual | Low | QB |
| QB Cold weather history | Historical game logs | Manual/API | Medium | QB |
| WR First-read share | PFF/Next Gen | Paid/Limited | High | WR |
| WR Air yard share | ESPN/Next Gen | Partial | Medium | WR |
| WR Shadow coverage | PFF/Team schemes | Paid/Manual | Medium | WR |

### Existing Data Sources to Leverage

| Metric | Current File | Enhancement |
|--------|--------------|-------------|
| Teammate injuries | `players.csv` | Cross-reference team |
| Secondary injuries | `team_data/{TEAM}.csv` | Add key player injuries |
| Game totals | `game_data.csv` | Add Vegas O/U, spread |
| Team data | `team_data/{TEAM}.csv` | Add pass/run ratio, RZ TD% |
| Schedule | `season_schedule.csv` | Flag divisional games |

---

## Conclusion

The current 13-step scoring algorithm provides a solid foundation covering projections, team quality, matchups, weather, and injuries. However, the streaming research and start/sit analysis revealed that **target volume**, **QB context**, **game environment (Vegas lines)**, and **position-specific metrics** are critical factors not currently captured.

**Recommended Priority (Top 10):**
1. **Vegas O/U + Implied Team Total** - Best predictor of scoring environment (ALL positions)
2. **Target share tracking** - Direct measure of opportunity (WR/TE)
3. **QB quality tier** - Essential context for pass-catchers (WR/TE/K)
4. **Teammate injury impact** - Captures role changes (WR/TE/RB)
5. **Team pass rate / tempo** - Volume opportunity indicator (ALL)
6. **Team RZ TD%** - Kicker XP vs FG prediction (K)
7. **Dome vs Outdoor (K-specific)** - Eliminates weather risk (K)
8. **Route participation rate** - TE involvement indicator (TE)
9. **Goal-line role** - RB TD equity (RB)
10. **Rushing upside** - Dual-threat QB floor boost (QB)

**Total Metrics Identified:** 58 potential scoring enhancements across 4 implementation phases.

**NEW: Position-Specific Insights:**
- **Kickers:** Need Team RZ TD%, accuracy tracking, and enhanced dome preference
- **Tight Ends:** Need route participation, RZ efficiency, EPA/target, and role security
- **Running Backs:** Need goal-line role, TD equity, YBC, role designation, and DVOA matchups
- **Quarterbacks:** Need rushing upside, pass volume, O-line health, and cold-weather history
- **Wide Receivers:** Need first-read share, air yard share, and shadow coverage tracking

These enhancements would address the majority of the analytical gap identified in the research comparison. Phase 1 (Quick Wins) alone would capture 80% of the value with relatively low implementation effort.

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-12 | 1.0 | Initial gap analysis from Week 15 WR research |
| 2025-12-12 | 1.1 | Added 8 additional metrics; fixed mode terminology; added Phase 4 |
| 2025-12-13 | 2.0 | Added 19 projection calculation metrics; new section for building custom projections; added projection framework; expanded data sources |
| 2025-12-17 | 3.0 | Added 20 position-specific metrics from streaming research guides; documented position-specific applications of existing metrics; reorganized for clarity |
| **2025-12-27** | **3.1** | **Updated to reflect Steps 11-13 (Temperature, Wind, Location) are FULLY IMPLEMENTED in v2.1 (Nov 2025); added implementation status column; created complete documentation for game conditions scoring** |

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
- Starter Helper Research Guide (Internal) - 10-Factor Analysis Model, position-specific thresholds
- Week 16/17 TE Streaming Report (Internal) - TE-specific metrics and thresholds
- Week 16/17 K Streaming Report (Internal) - Kicker-specific metrics and venue factors
