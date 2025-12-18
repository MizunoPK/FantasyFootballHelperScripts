# Starter Helper Research Guide (PPR)

A comprehensive guide for agents conducting start/sit analysis for **Full PPR** fantasy football weekly decisions.

> **Scoring Format:** This guide is optimized for Full PPR (1 point per reception). Target volume and receptions are weighted heavily in all recommendations.

---

## ⚠️ CRITICAL RULES FOR AGENTS - READ FIRST

**These 10 rules are NON-NEGOTIABLE. Violations will result in incomplete/incorrect reports.**

### The 5 Most Common Mistakes (AVOID THESE)

1. **Skipping Vegas lines** → ALWAYS include O/U and spread for every game
2. **Skipping weather** → ALWAYS check temperature/wind for outdoor games
3. **Using averages instead of week-by-week** → ALWAYS show individual game stats
4. **Incomplete 10-factor table** → ALWAYS fill in ALL 10 rows, not 3-4
5. **No monitoring points** → ALWAYS include "what to watch before kickoff"
6. **Considering day-of-week as a factor** → NEVER use TNF/MNF/SNF as positive or negative; focus only on scoring environment

### The 5 Core Principles (FOLLOW THESE)

1. **Volume > Efficiency > Matchup** → A 15-target WR beats an 8-target WR regardless of YPT
2. **Defense ranking convention** → #1 = allows MOST points = BEST matchup (worst defense)
3. **Include Quality Checklist IN the report** → Not just internally, show the user
4. **"Touches" = carries + receptions** → Not targets
5. **Filter by drafted status (players.csv column 8)** → Only recommend drafted=0 (available) or drafted=2 (owned). NEVER suggest drafted=1 players.

### Quick Compliance Check (Before Submitting Report)

Ask yourself: Did I include...
- [ ] Vegas O/U and spread for EVERY game?
- [ ] Weather for ALL outdoor games?
- [ ] Week-by-week tables (not just averages)?
- [ ] ALL 10 factors in comparison table?
- [ ] Key monitoring points section?
- [ ] Quality checklist at the end?
- [ ] **Verified drafted status (column 8) in players.csv for ALL recommended players?**
- [ ] **Filtered out all drafted=1 players from streaming recommendations?**

**If any box is unchecked, STOP and add the missing section.**

---

## TL;DR - Quick Reference Card

**For agents who need the essentials fast:**

### The Core Principle
> **Volume > Efficiency > Matchup > Projection** in PPR formats

### Decision Flowchart
```
1. Who has more targets/touches? → Favor higher volume
2. Similar volume? → Check matchup (defense rank vs position)
3. Similar matchup? → Check recent trend (last 3 games)
4. Still close? → Consider game environment (Vegas O/U)
5. Still close? → It's a coin flip - recommend based on floor vs ceiling need
```

### Key Thresholds (PPR)
| Position | Start Threshold | Elite Threshold |
|----------|-----------------|-----------------|
| WR | 6+ targets/game | 9+ targets/game |
| RB | 12+ touches + 3+ targets | 15+ touches + 5+ targets |
| TE | 5+ targets/game | 7+ targets/game |

**Note:** "Touches" = carries + receptions (not targets)

### Red Flags (Consider Sitting)
- First game back from IR → limited snaps
- Cold weather + QB with poor cold history
- RB snap share <40%
- 3+ week declining target trend

See [Common Pitfalls](#common-pitfalls) for complete list.

---

## Table of Contents

1. [Overview](#overview)
2. [Before You Start](#before-you-start)
3. [Research Framework](#research-framework)
4. [Required Data Points](#required-data-points)
5. [Search Strategy](#search-strategy)
6. [Analysis Methodology](#analysis-methodology)
7. [Report Structure](#report-structure) ← **Mandatory sections list**
8. [Mandatory Report Templates](#mandatory-report-templates) ← **Copy-paste templates (v1.6 expanded)**
9. [Position-Specific Considerations](#position-specific-considerations) (incl. FLEX, Same-Team)
10. [Common Pitfalls](#common-pitfalls)
11. [Quality Checklist](#quality-checklist) ← **Must include in reports**
12. [Quick Decision Mode](#quick-decision-mode)
13. [Appendix: Reference Tables](#appendix-reference-tables)

**New in v1.7:** Critical Rules section at top, numbered templates, fixed Matchup Grade Scale convention, RB Snap Share Decision Guide

**v1.6:** ECR Presentation, Win Probability, Pre-Injury Baseline, HOT/COLD Labels, Threshold Compliance, Breaking News Protocol, Projected Lineup Total, Defense Ranking Clarification

---

## Overview

### Purpose

This guide provides a systematic approach for researching and making weekly start/sit recommendations for fantasy football players. The goal is to synthesize multiple data sources into actionable advice that considers projections, matchups, trends, and context.

### When to Use This Guide

- User asks "Who should I start?" between multiple players
- User needs help setting their weekly lineup
- User wants analysis comparing players at the same position

### Output Location

Save completed assessments to: `docs/starters/assessments/week{N}_{position}_analysis_report.md`

---

## Before You Start

### Clarifying Questions to Ask

Before researching, gather this context from the user (if not provided):

| Question | Why It Matters |
|----------|----------------|
| **How many do you need to start?** | "Start 1 of 3" vs "Start 2 of 3" changes advice |
| **Playoff or regular season?** | Risk tolerance differs |
| **Current matchup situation?** | Need high floor vs. high ceiling |
| **League size?** | 8-team vs 14-team affects "startable" threshold |

**This guide assumes Full PPR scoring format.** In PPR, receptions are worth 1 point each, which significantly boosts the value of pass-catching running backs and high-volume receivers.

### Handling Ambiguous Player Names

If user provides incomplete names (e.g., "Williams", "Smith", "Johnson"):

1. **Check context** — Did they mention a team or position earlier?
2. **Ask for clarification** — "Which Williams? Javonte (DAL), Jameson (DET), or someone else?"
3. **If you must guess** — Assume the most fantasy-relevant player at that position
4. **State your assumption** — "Assuming you mean Jameson Williams (DET)..."

**Common ambiguous names to watch for:**
- Williams (Javonte, Jameson, Mike, etc.)
- Smith (multiple active players)
- Johnson (multiple active players)
- Brown (multiple active players)

### Check Internal Data First

Before web searches, check if relevant data exists in the league_helper system:

```
data/players.csv          → Current projections, injury status, drafted status
data/team_data/{TEAM}.csv → Defensive rankings by position
data/game_data.csv        → Weather, location data
```

If the user has the league_helper running, the `Starter Helper Mode` can provide baseline scores. Web research supplements this with context the algorithm doesn't capture.

### Player Availability Filtering (CRITICAL)

**IMPORTANT:** When researching streaming options or creating rankings, you MUST filter players by their `drafted` status in `players.csv` (column 8):

| drafted Value | Meaning | Include in Research? |
|---------------|---------|----------------------|
| **0** | Available on waivers | ✅ YES - Primary streaming targets |
| **1** | Rostered by another team | ❌ NO - Not available to add |
| **2** | On user's roster | ✅ YES - For start/sit decisions |

**Workflow:**
1. **Before recommending any player**, verify their `drafted` status in `players.csv`
2. **Filter out all drafted=1 players** from streaming recommendations
3. **Only suggest players with drafted=0** (available) or **drafted=2** (already owned)
4. **In reports, explicitly note** when top-ranked players are unavailable (drafted=1)

**Example:**
```markdown
### Top Streaming Options (drafted=0 only)
1. **Player A** (drafted=0) - Available, recommended
2. ~~Player B~~ (drafted=1) - NOT AVAILABLE (already rostered)
3. **Player C** (drafted=0) - Available, recommended

### Your Roster (drafted=2)
- **Player D** (drafted=2) - Start/Sit analysis
```

**Why This Matters:** Web research and expert rankings include ALL players league-wide. Your league has specific availability based on drafted status. Always filter your final recommendations to match actual availability.

### Time Sensitivity

**Critical timing considerations:**

| Day | Action |
|-----|--------|
| Tuesday-Wednesday | Initial research; injury reports preliminary |
| Thursday | TNF players locked; check Wednesday practice reports |
| Friday | Key injury designations released (Q/D/O) |
| Saturday | Final injury reports; last research window |
| Sunday morning | Final checks before lineup lock |

**Always verify injury status is current** — a "Questionable" on Tuesday may become "Out" by Sunday.

---

## Research Framework

### The 10-Factor Analysis Model

Every start/sit decision should evaluate these 10 factors:

| # | Factor | Weight | Description |
|---|--------|--------|-------------|
| 1 | **Projections** | High | Consensus weekly fantasy point projections |
| 2 | **Matchup Quality** | High | Opponent's defensive ranking vs. position |
| 3 | **Recent Performance** | High | Last 3-5 game trends (hot/cold streaks) |
| 4 | **Target/Touch Volume** | High | Opportunity share (targets for pass-catchers, carries for RBs) |
| 5 | **Game Environment** | Medium | Vegas O/U, spread, implied team total |
| 6 | **Weather Conditions** | Medium | Temperature, wind, precipitation (outdoor games) |
| 7 | **Team Context** | Medium | O-line health, QB performance, offensive scheme |
| 8 | **Opponent Context** | Medium | Secondary injuries, coverage tendencies, defensive line |
| 9 | **Injury Status** | High | Player's own health and any limitations |
| 10 | **Floor/Ceiling** | Medium | Volatility assessment and range of outcomes |

### Priority Order for Research

1. **Always start with projections** — establishes baseline expectations
2. **Matchup quality next** — identifies favorable/unfavorable situations
3. **Recent performance** — captures momentum and trends
4. **Volume metrics** — opportunity is the most stable predictor
5. **Game environment** — Vegas lines predict game script
6. **Weather (if applicable)** — major impact for outdoor games
7. **Contextual factors** — team/opponent situations

---

## Required Data Points

### For All Positions

| Data Point | Source | Priority |
|------------|--------|----------|
| Week N projection (PPR) | ESPN, FantasyPros, Yahoo | Required |
| Expert consensus ranking (ECR) | FantasyPros | Required |
| Opponent defense rank vs. position | FantasyPros, Pro Football Reference | Required |
| Last 3-5 game stats | ESPN player page | Required |
| Vegas O/U total | ESPN, DraftKings | Required |
| Vegas spread | ESPN, DraftKings | Required |
| Injury status | ESPN, team reports | Required |
| Weather forecast (outdoor) | CBS Sports, NFL Weather | Conditional |

### Position-Specific Data

#### Wide Receivers / Tight Ends
| Data Point | Why It Matters | Threshold |
|------------|----------------|-----------|
| Target share % | Direct measure of opportunity | 25%+ = elite, 20-24% = strong, 15-19% = average |
| Air yard share % | Depth of targets (ceiling indicator) | 30%+ = deep threat |
| Routes run / Route share % | Snap involvement in passing game | 70%+ = locked in |
| Red zone targets | TD probability | Track weekly + season total |
| YPRR (Yards Per Route Run) | Efficiency metric | 2.0+ = elite |
| First-read share % | How often QB looks to player first | 15%+ = primary option |
| QB performance/health | Pass-catcher value tied to QB | Check cold weather history |
| Opponent CB injuries | Specific coverage matchup | Shadow CB = concern |
| Coverage scheme | Single-high vs two-high safety | Some WRs thrive vs specific schemes |

#### Running Backs
| Data Point | Why It Matters | Threshold |
|------------|----------------|-----------|
| Snap share % | Playing time indicator | 70%+ = workhorse, 55%+ = lead |
| Carries per game | Volume floor | 15+ = reliable |
| Targets per game | PPR upside | 4+ = PPR floor boost |
| Red zone carries | TD probability | Track weekly + season total |
| Goal-line role | Who gets carries inside the 5 | Yes/No/Split |
| TD equity | Season TD rate vs opportunity | High/Moderate/Low |
| Yards per carry (YPC) | Efficiency (but volume > efficiency) | Note trend vs season avg |
| Yards before contact | O-line quality indicator | Higher = better blocking |
| Role designation | Lead back / Committee / Backup | Determines floor |
| Opponent run defense DVOA | Matchup quality | Recent 5-week trend matters |

#### Quarterbacks
| Data Point | Why It Matters | Threshold |
|------------|----------------|-----------|
| Pass attempts per game | Volume indicator | 35+ = high volume |
| Rushing upside | Dual-threat floor | 30+ rush yards = bonus |
| Opponent pass defense rank | Matchup quality | Top-10 = favorable |
| Weather conditions | Major impact on passing | See cold weather table |
| O-line health | Time to throw | Track specific injuries |
| Cold weather history | Some QBs struggle in cold | Create table if relevant |

#### Tight Ends (Streaming-Specific)
| Data Point | Why It Matters | Threshold |
|------------|----------------|-----------|
| Route share % | Involvement in passing game | 70%+ = elite for TE |
| Red zone target efficiency | TD conversion rate | Track X/Y format (e.g., 9/10) |
| EPA per target | Advanced efficiency | +0.3+ = elite |
| Role security | Is backup TE injured? | Locked = no competition |
| Defense rank vs TE | Streaming is matchup-driven | #1-8 = start, #25-32 = avoid |

### Advanced Metrics Reference

These metrics appear in high-quality analysis. Include when available:

| Metric | Definition | When to Use |
|--------|------------|-------------|
| **YPRR** | Yards Per Route Run | WR efficiency regardless of volume |
| **EPA/target** | Expected Points Added per target | Pass-catcher efficiency |
| **Air yard share** | % of team's air yards | Deep threat indicator |
| **First-read share** | % of plays as QB's first look | Target quality indicator |
| **Yards before contact** | RB yards before being touched | O-line quality |
| **Route share** | % of routes run when on field | TE/WR involvement |
| **Target share** | % of team targets | Volume indicator |
| **Red zone share** | % of team's RZ opportunities | TD equity |

---

## Search Strategy

### Recommended Search Queries

Execute these searches in parallel for each player:

```
Search 1: "{Player Name} Week {N} {Year} fantasy projections PPR"
Search 2: "{Player Name} {Year} fantasy start sit matchup analysis"
Search 3: "{Team} vs {Opponent} Week {N} {Year} matchup"
Search 4: "{Opponent} {position} defense {Year} fantasy points allowed"
Search 5: "NFL Week {N} {Year} weather forecast outdoor games"
```

### High-Quality Sources

| Source | Best For |
|--------|----------|
| **FantasyPros** | Consensus rankings, expert aggregation |
| **ESPN Fantasy** | Projections, player news, injury updates |
| **Pro Football Network** | Deep start/sit analysis, matchup breakdowns |
| **CBS Sports** | Weather reports, injury analysis |
| **Yahoo Sports** | Player news, trend analysis |
| **Underdog Network** | Advanced metrics, rankings |
| **Pro Football Reference** | Historical stats, defense rankings |

### Verification Searches

After initial research, run verification searches:

```
"{Player 1}" "{Player 2}" Week {N} rankings comparison
{Team} offense injuries Week {N} {Year}
{Opponent} secondary injuries cornerback {Year}
```

### Handling Conflicting Information

When sources disagree, use this hierarchy:

| Priority | Source Type | Example |
|----------|-------------|---------|
| 1 | Official team reports | Injury designations, depth charts |
| 2 | Consensus rankings (aggregated) | FantasyPros ECR (averages many experts) |
| 3 | Beat reporters | Team-specific insiders |
| 4 | National analysts | ESPN, CBS, Yahoo experts |
| 5 | Individual hot takes | Single analyst opinions |

**When stats conflict:**
- Use the most recent data (this week's practice reports > last week's game)
- Prefer position-specific defense rankings over overall defense rankings
- Trust volume metrics (targets, carries) over efficiency metrics (YPC, yards/target)

**When projections differ significantly (>3 points):**
- Note the range in your report
- Identify why they differ (one source may have newer injury info)
- Default to the consensus (FantasyPros aggregates 50+ experts)

### Edge Case Searches

For specific situations, use targeted searches:

```
# Player-specific weather history
"{QB Name} cold weather career stats wins losses"
"{QB Name} games under 40 degrees"

# Rookie/new player research
"{Player Name} college stats production profile"
"{Player Name} NFL draft profile athletic testing"
"{Player Name} snap count trend rookie"

# Recent team changes
"{Team} offensive coordinator play calling changes {Year}"
"{Team} offensive line injuries starting lineup"
```

### Handling Failed or Poor Search Results

When searches return limited/no useful data:

| Situation | Action |
|-----------|--------|
| **No projection found** | Use season average as baseline; note uncertainty |
| **Conflicting injury info** | Default to official team report; check Twitter for beat reporters |
| **No matchup analysis** | Calculate manually using defense rank vs position from fantasy sites |
| **Player too obscure** | Focus on volume metrics (snap %, target share) over expert opinions |
| **Searches timing out** | Use Quick Decision Mode; rely on fundamentals |

**Fallback Data Sources:**
1. ESPN player page (always has basic stats)
2. Pro Football Reference (historical data)
3. Team official website (injury reports)
4. FantasyPros ECR (consensus when individual analysis unavailable)

**When Data is Truly Unavailable:**
- State the limitation clearly in your report
- Make recommendation based on available factors
- Express lower confidence level
- Suggest user monitor for updates closer to game time

---

## Analysis Methodology

### Time Estimate

| Analysis Type | Time Required |
|---------------|---------------|
| Full analysis (2 players) | 25-30 minutes |
| Full analysis (3-4 players) | 35-45 minutes |
| Quick Decision Mode | 5-10 minutes |

### Step 1: Establish Baseline (5 min)

For each player, document:
- Current week projection (PPR points)
- Season average PPR points per game
- Expert consensus ranking (ECR)
- Opponent defense rank vs. position

### Step 2: Evaluate Matchup (5 min)

Research the defensive matchup:
- Position-specific defense ranking (not overall)
- Recent defensive performance trend (last 5 weeks)
- Key defensive injuries (CBs for WRs, DL for RBs)
- Fantasy points allowed to position

### Step 3: Assess Recent Form (5 min)

Analyze last 3-5 games:
- Points scored each week
- Target/touch volume each week
- Identify hot streaks (3+ good games) or cold streaks
- Note any outlier performances (boom/bust games)

### Step 4: Evaluate Game Environment (3 min)

Check Vegas lines:
- Over/Under total (high = more scoring opportunity)
- Spread (big underdog = negative game script for RBs)
- Implied team total (key metric)

**Interpretation Guide:**
| O/U Total | Implication |
|-----------|-------------|
| 54+ | Shootout expected, boost all skill players significantly |
| 48-53 | High-scoring, boost skill players |
| 44-47 | Average environment |
| 40-43 | Lower scoring, slight concern for pass-catchers |
| <40 | Negative environment, downgrade passing game significantly |

### Step 5: Check Weather (2 min, outdoor games only)

For outdoor games, check:
- Temperature (extreme cold affects passing)
- Wind speed (15+ mph affects passing, 20+ affects kicking)
- Precipitation (rain/snow affects ball security)

**Critical Weather Flags:**
- Temperature under 40°F → Check QB cold-weather history
- Wind over 15 mph → Downgrade deep threats
- Snow/heavy rain → Downgrade passing game

### Step 6: Identify Contextual Factors (5 min)

Research team-specific situations:
- Teammate injuries (WR1 out → WR2 boost)
- O-line injuries (affects QB/RB)
- Coaching changes or scheme adjustments
- Primetime game (some players perform differently)
- Divisional rivalry (often lower scoring)

### Step 7: Calculate Floor/Ceiling (3 min)

Based on all factors, estimate:
- **Floor:** Minimum expected points (worst-case scenario)
- **Ceiling:** Maximum expected points (best-case scenario)
- **Most Likely:** Expected outcome

**Floor/Ceiling Framework:**
| Player Type | Typical Floor | Typical Ceiling |
|-------------|---------------|-----------------|
| Elite WR1 | 12-15 | 25-35 |
| WR2/WR3 | 6-10 | 18-25 |
| Lead RB | 10-14 | 25-30 |
| Committee RB | 5-8 | 15-20 |
| Elite TE | 8-12 | 20-25 |
| Streaming TE | 3-6 | 12-18 |

---

## Report Structure

### Required Sections

Every start/sit report **MUST** include these sections. Do not skip any.

```markdown
# Week {N} {Position} Start/Sit Analysis

## Executive Summary
Quick recommendation table with rankings

## Game Environment (Vegas Lines)                    ← MANDATORY
- O/U total for each relevant game
- Spread for each relevant game
- Implied team totals
- Environment assessment (high-scoring/average/low-scoring)

## Weather Conditions                               ← MANDATORY (for outdoor games)
- Temperature forecast for each outdoor game
- Wind speed
- Precipitation risk
- Impact assessment (None/Minor/Moderate/Severe)

## Player Analysis
For each player:
- Projection and floor/ceiling
- Why Start (bullet points)
- Concerns (bullet points)
- Recent performance table (WEEK-BY-WEEK, not just averages)

## Volume Metrics Summary                           ← MANDATORY
- Target share % for WRs/TEs
- Snap share % for RBs
- Targets/touches per game
- Comparison to Start/Elite thresholds

## Head-to-Head Comparison (10-Factor)              ← MANDATORY
Full comparison table with ALL 10 factors for each player

## Key Monitoring Points Before Kickoff             ← MANDATORY
- Injuries to watch (with impact if status changes)
- Key designations to track (Friday/Saturday)
- Backup plan if starter is ruled out

## Final Verdict
- Clear recommendation
- Tiebreaker reasoning

## Quality Checklist                                ← MANDATORY (include in report)
- Verification that all 10 factors were analyzed
- Confirmation of data sources

## Sources
- All sources cited with links
```

### Sections That Are Commonly Missed

**CRITICAL:** These sections are frequently skipped but are REQUIRED:

| Section | Why It's Missed | Why It Matters |
|---------|-----------------|----------------|
| **Game Environment (Vegas)** | Agents forget to look up betting lines | Vegas O/U predicts game script; affects all players |
| **Weather Conditions** | Only checked for obvious cold games | Wind/rain affect passing; cold affects specific QBs |
| **Week-by-Week Tables** | Agents summarize instead of listing | Identifies trends, outliers, and consistency |
| **Volume Metrics** | Target share/snap share skipped | Volume is #1 predictor in PPR; thresholds matter |
| **10-Factor Comparison** | Only 3-4 factors compared | Missing factors leads to wrong recommendations |
| **Key Monitoring Points** | Not included at all | User needs to know what to watch before kickoff |
| **Quality Checklist** | Treated as internal, not in report | Proves analysis was thorough; builds trust |

**If you find yourself skipping a section, STOP and complete it.** The section exists because it impacts recommendations.

### Example Quick Summary Table

```markdown
| Rank | Player | Opponent | Projection | Floor | Ceiling | Verdict |
|------|--------|----------|------------|-------|---------|---------|
| 1 | Player A | vs TEN | 16.5 | 12 | 24 | **START** |
| 2 | Player B | @ BUF | 14.2 | 8 | 20 | **START** |
| 3 | Player C | vs KC | 11.8 | 5 | 18 | **SIT** |
```

### Confidence Levels

Always express confidence in your recommendation:

| Confidence | When to Use | Language |
|------------|-------------|----------|
| **High** | Clear advantage in 7+ factors | "Must start", "Clear choice", "Lock" |
| **Medium** | Advantage in 4-6 factors | "Lean start", "Slight edge", "Prefer" |
| **Low/Toss-up** | Close in most factors | "Coin flip", "Could go either way", "Both viable" |

**When it's a toss-up:**
- Explicitly say so — don't force a recommendation
- Highlight the 1-2 factors that could break the tie
- Suggest the user consider their specific matchup needs (floor vs. ceiling)

Example: "This is essentially a coin flip. If you need a safe floor, go with Player A. If you need upside to win your matchup, Player B has the higher ceiling."

### Playoff Considerations

In fantasy playoffs, add this context:

| Situation | Recommendation Adjustment |
|-----------|--------------------------|
| User projected to win easily | Prioritize **floor** (safe points) |
| User projected to lose | Prioritize **ceiling** (boom potential) |
| Close matchup | Balance floor/ceiling based on other starters |
| Must-win elimination game | Consider opponent's remaining players |

---

## Mandatory Report Templates

**Quick Index - 20 Templates + 1 Reference:**
| # | Template | Use For |
|---|----------|---------|
| **1** | **10-Factor Comparison** | Every report (REQUIRED) |
| **2** | **Week-by-Week Performance** | Every key player (REQUIRED) |
| **3** | **Game Environment** | Vegas lines (REQUIRED) |
| **4** | **Weather Conditions** | Outdoor games (REQUIRED) |
| **5** | **Volume Metrics** | Threshold compliance (REQUIRED) |
| **6** | **Key Monitoring Points** | Pre-kickoff watch list (REQUIRED) |
| 7 | Tier System | Organizing recommendations |
| 8 | Matchup Grade Scale | Quick matchup reference |
| 9 | QB Cold Weather | Weather-affected pass-catchers |
| 10 | Defense Rankings Breakdown | Matchup deep dive |
| 11 | Matchups to Avoid | Trap game warnings |
| 12 | Scenario-Based Guidance | Floor/ceiling situations |
| 13 | Role Designation | RB opportunity levels |
| 14 | ECR Presentation | Expert consensus |
| 15 | Win Probability | Game script impact |
| 16 | Pre-Injury Baseline | Players returning from IR |
| 17 | HOT/COLD Trend Labels | Streak identification |
| 18 | Threshold Compliance | Explaining sub-threshold starters |
| 19 | Breaking News Protocol | Mid-analysis injury updates |
| 20 | Projected Lineup Total | Final lineup summary |
| Ref | Defense Ranking Clarification | Understanding #1 vs #32 |

---

### Template 1: 10-Factor Head-to-Head Comparison Table

**COPY THIS TEMPLATE** for every report. Fill in ALL 10 rows.

```markdown
### Head-to-Head Comparison (Week {N})

| Factor | Player A | Player B | Player C | Edge |
|--------|----------|----------|----------|------|
| **1. Projection** | X.X | X.X | X.X | Player |
| **2. Matchup** | vs OPP (rank) | vs OPP (rank) | vs OPP (rank) | Player |
| **3. Recent PPG** | X.X (last 3) | X.X (last 3) | X.X (last 3) | Player |
| **4. Volume** | X tgt/X snap% | X tgt/X snap% | X tgt/X snap% | Player |
| **5. Vegas O/U** | XX.X | XX.X | XX.X | Player |
| **6. Weather** | Dome/Temp | Dome/Temp | Dome/Temp | Player |
| **7. Team Context** | Notes | Notes | Notes | Player |
| **8. Opponent Context** | Notes | Notes | Notes | Player |
| **9. Injury Status** | Healthy/Q/D | Healthy/Q/D | Healthy/Q/D | Player |
| **10. Floor/Ceiling** | X/X | X/X | X/X | Player |
| **VERDICT** | START/SIT | START/SIT | START/SIT | - |
```

### Template 2: Week-by-Week Recent Performance Table

**COPY THIS TEMPLATE** for each key player. Show actual weekly data, not just averages.

```markdown
### {Player Name} (Last 5 Games)

| Week | Rec/Tgt | Yards | TD | PPR | Notes |
|------|---------|-------|----|----|-------|
| 15 | X/X | XX | X | XX.X | Context |
| 14 | X/X | XX | X | XX.X | Context |
| 13 | X/X | XX | X | XX.X | Context |
| 12 | X/X | XX | X | XX.X | Context |
| 11 | X/X | XX | X | XX.X | Context |
| **Avg** | **X/X** | **XX** | **X.X** | **XX.X** | **Trend** |
```

### Template 3: Game Environment Table

**COPY THIS TEMPLATE** for Vegas lines section.

```markdown
### Week {N} Betting Lines

| Game | Spread | O/U Total | Implied Team Total | Environment |
|------|--------|-----------|-------------------|-------------|
| TEAM @ TEAM | FAV -X | XX.X | TEAM ~XX.X | High/Avg/Low |
| TEAM @ TEAM | FAV -X | XX.X | TEAM ~XX.X | High/Avg/Low |
```

### Template 4: Weather Conditions Table

**COPY THIS TEMPLATE** for all outdoor games.

```markdown
### Week {N} Weather Impact

| Game | Venue | Temperature | Wind | Precipitation | Impact Level |
|------|-------|-------------|------|---------------|--------------|
| TEAM @ TEAM | Stadium | ~XX°F | X-X mph | Clear/Rain/Snow | None/Minor/Moderate/Severe |
```

### Template 5: Volume Metrics Summary Table

**COPY THIS TEMPLATE** to show threshold compliance.

```markdown
### Volume Metrics vs. Thresholds

| Position | Start Threshold | Elite Threshold | Your Players Meeting |
|----------|-----------------|-----------------|----------------------|
| WR | 6+ targets/game | 9+ targets/game | Names (X tgt) |
| RB | 12+ touches + 3+ tgt | 15+ touches + 5+ tgt | Names (X touches, X tgt) |
| TE | 5+ targets/game | 7+ targets/game | Names (X tgt) |

### Snap/Target Share Tiers

| Tier | Threshold | Your Players |
|------|-----------|--------------|
| Workhorse RB | 70%+ snap | Names (X%) |
| Lead RB | 55-69% snap | Names (X%) |
| Committee RB | 40-54% snap | Names (X%) |
| Elite WR target | 25%+ share | Names (X%) |
| Strong WR target | 20-24% share | Names (X%) |
```

### Template 6: Key Monitoring Points Table

**COPY THIS TEMPLATE** at the end of every report.

```markdown
### Key Monitoring Points Before Kickoff

| Player | Watch For | Impact if Changed |
|--------|-----------|-------------------|
| Player Name | Status/metric to monitor | What happens if it changes |

### Injury Designations to Track (Friday/Saturday)

| Player | Current Status | Key Date |
|--------|---------------|----------|
| Player Name | Healthy/Q/D/O | When to check |
```

### Template 7: Tier System Template

**COPY THIS TEMPLATE** to organize recommendations by confidence level.

```markdown
### Tier 1: Must Starts
Players you start regardless of matchup.

1. **Player Name** — Reason (projection, volume, matchup)

### Tier 2: Strong Options
Players with favorable situations this week.

2. **Player Name** — Reason
3. **Player Name** — Reason

### Tier 3: Flex Considerations
Matchup-dependent or boom/bust players.

4. **Player Name** — Reason

### Tier 4: Sit / Avoid
Players to bench this week despite name value.

5. **Player Name** — Why sit (matchup, injury, volume concern)
```

### Template 8: Matchup Grade Scale

Use letter grades for quick matchup assessment.

**IMPORTANT:** This scale uses the "Fantasy Points Allowed" convention where **#1 = allows MOST points (worst defense = best matchup)**.

| Grade | Meaning | Defense Rank (FP Allowed) | Action |
|-------|---------|---------------------------|--------|
| **A+** | Elite matchup | #1-3 (allows most) | Must start |
| **A** | Great matchup | #4-8 | Strong start |
| **B+** | Good matchup | #9-12 | Lean start |
| **B** | Above average | #13-16 | Start if volume supports |
| **B-** | Slightly favorable | #17-20 | Matchup-dependent |
| **C** | Neutral | #21-24 | Pure volume play |
| **C-** | Slightly tough | #25-27 | Need elite volume |
| **D** | Tough matchup | #28-30 | Sit unless no choice |
| **F** | Avoid | #31-32 (allows fewest) | Do not start |

### Template 9: QB Cold Weather History Table

**COPY THIS TEMPLATE** when weather is a factor for pass-catchers.

```markdown
### {QB Name} Cold Weather Record

| Temperature | W-L Record | Comp % | TD/INT | Avg PPG |
|-------------|------------|--------|--------|---------|
| Under 32°F | X-X | XX% | X/X | X.X |
| Under 40°F | X-X | XX% | X/X | X.X |
| Under 50°F | X-X | XX% | X/X | X.X |
| 70°F+ (baseline) | X-X | XX% | X/X | X.X |

**Impact:** [Severe/Moderate/Minor] — [Explanation of how this affects pass-catchers]
```

### Template 10: Defense Rankings Breakdown Template

**COPY THIS TEMPLATE** for comprehensive matchup analysis.

```markdown
### Defense Rankings vs {Position} (2025)

#### Worst Defenses (Best Matchups)

| Rank | Team | PPG Allowed | Assessment |
|------|------|-------------|------------|
| #32 | Team | XX.X | Why it's favorable |
| #31 | Team | XX.X | Why it's favorable |
| #30 | Team | XX.X | Why it's favorable |

#### Best Defenses (Matchups to Avoid)

| Rank | Team | PPG Allowed | Assessment |
|------|------|-------------|------------|
| #1 | Team | X.X | Why to avoid |
| #2 | Team | X.X | Why to avoid |
| #3 | Team | X.X | Why to avoid |
```

### Template 11: Matchups to Avoid Section

**COPY THIS TEMPLATE** to warn users about trap games.

```markdown
## Matchups to Avoid

| Week | Player | Opponent | Why Avoid |
|------|--------|----------|-----------|
| X | Player Name | vs/@ TEAM | Defense rank, coverage, game script |
| X | Player Name | vs/@ TEAM | Reason |

### Why {Player} Isn't Ranked Higher
[Explanation for players with good projections but concerning matchups]
```

### Template 12: Scenario-Based Guidance Template

**COPY THIS TEMPLATE** for strategic recommendations.

```markdown
## Strategic Recommendations

### Scenario-Based Guidance

| Your Situation | Recommendation | Reasoning |
|----------------|----------------|-----------|
| **Need floor (protecting lead)** | Player A | Higher floor, consistent volume |
| **Need ceiling (chasing points)** | Player B | Boom potential, favorable matchup |
| **Best available on waivers** | Player C | Combination of availability + upside |
| **One pickup for multiple weeks** | Player D | Consistent matchups across weeks |

### If Starting X Players, Choose:

| Slots | Recommended | Alternative |
|-------|-------------|-------------|
| 1 | Player A | Player B if [condition] |
| 2 | Player A + Player B | Player A + Player C if [condition] |
| 3 (with FLEX) | A + B + C | A + B + D if [condition] |
```

### Template 13: Role Designation Reference

Use these designations for RBs to clarify opportunity level:

| Designation | Snap Share | Meaning | Floor Expectation |
|-------------|------------|---------|-------------------|
| **Workhorse** | 70%+ | Bell-cow back | High (12+ PPR) |
| **Lead back** | 55-69% | Primary but shares | Moderate (8-12 PPR) |
| **1A in committee** | 45-54% | Slight edge in split | Variable (6-15 PPR) |
| **1B in committee** | 40-50% | Even split | Low-variable (4-12 PPR) |
| **Backup** | <40% | Handcuff/change of pace | Low (2-8 PPR) |
| **Returning from IR** | Variable | First game(s) back | Very low (snap count) |

### Template 14: ECR (Expert Consensus Ranking) Presentation

**COPY THIS FORMAT** when citing expert rankings:

```markdown
| Player | ECR Range | Notes |
|--------|-----------|-------|
| Player A | WR11-12 | Consistent across sources |
| Player B | WR7-20 (varies) | Wide range = uncertainty |
| Player C | WR15 | Tight consensus |
```

**Interpretation:**
- **Tight range (±2):** Strong consensus, high confidence
- **Wide range (±5+):** Experts disagree, add "(varies)" note
- **Rising/Falling:** Note if ECR changed significantly from last week

### Template 15: Win Probability / Implied Game Script

**COPY THIS TABLE** for game environment section:

```markdown
### Game Script Projections

| Game | Win Probability | Implied Script | RB Impact | WR Impact |
|------|-----------------|----------------|-----------|-----------|
| Team A vs B | 73% A | A controls game | Positive | Neutral |
| Team C vs D | 55% D | Competitive | Neutral | Neutral |
| Team E vs F | 30% E | E likely trailing | Negative | Positive (garbage time) |
```

**Win Probability Impact:**
- **70%+ favorite:** Positive game script for RBs (can run out clock)
- **55-69%:** Neutral script
- **45-54%:** Toss-up, script unpredictable
- **<45% (underdog):** Negative for RBs, may boost pass-catchers in garbage time

### Template 16: Pre-Injury Baseline Template

**COPY THIS TEMPLATE** for players returning from IR:

```markdown
### {Player Name} - Returning from IR

**Injury:** [Injury type] (missed X games)
**Return Game:** Week N

#### Pre-Injury Baseline (Weeks X-Y)
| Metric | Average | Notes |
|--------|---------|-------|
| Snap % | XX% | Was [Workhorse/Lead/Committee] |
| Touches/Game | XX | [High/Moderate/Low] volume |
| PPR PPG | XX.X | [Context] |

#### Week N Return (First Game Back)
| Metric | Actual | vs Baseline |
|--------|--------|-------------|
| Snap % | XX% | [XX% lower] |
| Touches | XX | [Expected ramp-up] |
| PPR | XX.X | - |

**Projection:** Expect [X]% of pre-injury workload in Week N+1, ramping to full by Week N+X.
```

### Template 17: HOT/COLD Trend Labels

Use these labels consistently in reports:

| Label | Criteria | Usage |
|-------|----------|-------|
| **HOT** | 3+ consecutive games above season average | "Trevor Lawrence (**HOT** - 28.5 PPG last 3)" |
| **COLD** | 3+ consecutive games below season average | "Aaron Rodgers (**COLD** - 9.4 PPG last 3)" |
| **SURGING** | Significant improvement over 2 games | Rising trajectory |
| **SLUMPING** | Significant decline over 2 games | Falling trajectory |
| **CONSISTENT** | Within ±3 PPR of average in 4+ games | Reliable floor |
| **VOLATILE** | Boom/bust pattern (3+ swings of 10+ pts) | High variance |

**Example Usage:**
```markdown
| Player | W16 Proj | Trend | Recent PPG |
|--------|----------|-------|------------|
| Trevor Lawrence | 18.0 | **HOT** | 28.5 (last 3) |
| Aaron Rodgers | 12.6 | **COLD** | 9.4 (last 3) |
```

### Template 18: Threshold Compliance Explanation Template

**COPY THIS TEMPLATE** when streamers or depth options don't meet volume thresholds:

```markdown
### Volume Threshold Analysis

| Player | Targets/Game | Threshold Met? |
|--------|--------------|----------------|
| Player A | 4.6 | ❌ Below (5+ needed) |
| Player B | 6.2 | ✅ Meets Start threshold |
| Player C | 3.8 | ❌ Below |

**Why Sub-Threshold Players Can Still Be Started:**

These streaming options don't meet the 5+ target threshold. This is typical for waiver-wire players—elite volume is monopolized by rostered starters. For streamers, we compensate with:

1. **Matchup advantage** — Facing weak defenses boosts expected production
2. **Red zone efficiency** — TD upside despite lower volume
3. **Role expansion** — Recent injury to competitor increases opportunity
4. **Route participation** — High route share indicates involvement when on field

This is why matchup and efficiency matter more for streamers than for locked-in starters.
```

### Template 19: Breaking News Protocol

**When major injury news breaks mid-analysis:**

1. **Immediately flag affected players:**
   ```markdown
   ### ⚠️ CRITICAL UPDATE: [Player] Injury

   **News:** [Brief description of injury]
   **Impact:** [Who is affected]
   **Source:** [Link to report]
   **Updated projections below reflect this news.**
   ```

2. **Update all affected player sections:**
   - Add "**DOWNGRADED**" or "**UPGRADED**" label
   - Note original projection was "PRE-INJURY" if still shown
   - Recalculate floor/ceiling based on new situation

3. **Add to Key Monitoring Points:**
   - Track recovery timeline
   - Identify backup/replacement to monitor

**Example (QB injury affecting WR):**
```markdown
### Rashee Rice @ TEN — DOWNGRADED

**Projection:** 17.8 PPR pts *(PRE-INJURY — now obsolete)*

**⚠️ CRITICAL:** Patrick Mahomes tore his ACL in Week 15. Rice's value has collapsed with a backup QB.

**New Assessment:**
- **Floor/Ceiling:** 3 / 14 (post-Mahomes)
- **Verdict:** **SIT** — Backup QB = massive downgrade
```

### Template 20: Projected Lineup Total Template

**COPY THIS** at the end of optimal lineup recommendations:

```markdown
### Week N Optimal Lineup

| Pos | Starter | Opp | Proj | Floor | Ceiling |
|-----|---------|-----|------|-------|---------|
| QB | Player | vs X | XX.X | XX | XX |
| RB1 | Player | vs X | XX.X | XX | XX |
| RB2 | Player | vs X | XX.X | XX | XX |
| WR1 | Player | vs X | XX.X | XX | XX |
| WR2 | Player | vs X | XX.X | XX | XX |
| TE | Player | vs X | XX.X | XX | XX |
| FLEX | Player | vs X | XX.X | XX | XX |
| K | Player | vs X | XX.X | XX | XX |
| DST | Team | vs X | XX.X | XX | XX |

**Week N Projected Total:** ~XXX PPR points
**Floor Total:** ~XXX | **Ceiling Total:** ~XXX

**Alternative FLEX:** [Player] (vs X) if you need [ceiling/floor]
```

### Defense Ranking Clarification

**IMPORTANT:** Defense rankings can be expressed two ways. Always clarify which system you're using:

| System | #1 Means | #32 Means | Example |
|--------|----------|-----------|---------|
| **Fantasy Points Allowed** | Allows MOST (worst D) | Allows FEWEST (best D) | "Bengals #1 vs TE = start TEs against them" |
| **Defensive Strength** | BEST defense | WORST defense | "Bills #1 vs TE = avoid TEs against them" |

**This guide uses "Fantasy Points Allowed" convention:**
- **Low rank (#1-8)** = Bad defense = **Good matchup for fantasy**
- **High rank (#25-32)** = Good defense = **Bad matchup for fantasy**

**When writing reports, explicitly state:**
```markdown
| Defense | Rank vs WR | Meaning |
|---------|------------|---------|
| Bengals | #1 (allows most) | Elite matchup — start WRs |
| Bills | #32 (allows least) | Avoid — sit WRs |
```

---

## Position-Specific Considerations

### Wide Receivers

**Key Start Indicators:**
- Target share ≥20%
- Opponent allows top-10 fantasy points to WR
- QB playing well (no injury concerns)
- Game O/U ≥47

**Key Sit Indicators:**
- Target share declining (3+ week trend)
- Shadow coverage from elite CB expected
- QB struggling or injured
- Extreme weather (cold + wind)
- Heavy underdog (negative game script can help garbage time, but risky)

**Special Situations:**
- WR1 injury → Immediately boost WR2/WR3 value
- New QB → Uncertainty, slight downgrade until chemistry established
- Revenge game → Slight boost (narrative, not statistically significant)

### Running Backs

**Key Start Indicators:**
- Snap share ≥55% (lead back or better)
- Opponent allows top-12 fantasy points to RB
- Team favored (positive game script)
- Goal-line role secured
- Pass-catching role (4+ targets/game) provides PPR floor

**Key Sit Indicators:**
- Snap share <40% (backup territory)
- Committee backfield with unclear roles AND no receiving work
- Team is heavy underdog (will abandon run)
- Returning from injury (first game back)
- Opponent has elite run defense AND team will be trailing

**Snap Share Decision Guide:**
| Snap Share | Role | PPR Recommendation |
|------------|------|-------------------|
| 70%+ | Workhorse | Must start |
| 55-69% | Lead back | Start most weeks |
| 40-54% | Committee | Start only if 4+ targets OR elite matchup |
| <40% | Backup | Avoid unless injury to starter |

**Special Situations:**
- Backup RB with starter injured → Start if clear handcuff
- Committee back → Need PPR upside (targets) to be viable
- Short-week game (TNF) → Slight downgrade for injury-prone backs

### Tight Ends

**Key Start Indicators:**
- Target share ≥15% among pass-catchers
- Red zone target leader on team
- Opponent weak vs. TE (many teams are)
- High-scoring game environment

**Key Sit Indicators:**
- Blocking-heavy role
- Multiple TE sets splitting targets
- Opponent has elite TE coverage (rare)

### Quarterbacks

**Key Start Indicators:**
- 35+ pass attempts per game
- Rushing upside (40+ yards, TD potential)
- Opponent allows top-10 fantasy points to QB
- Dome or good weather

**Key Sit Indicators:**
- Extreme cold weather (especially for warm-weather QBs)
- High wind (15+ mph)
- Elite pass rush opponent
- Running team with low pass volume

### FLEX Decisions (Cross-Position Comparison)

When comparing players across positions (e.g., RB vs WR for FLEX):

**PPR FLEX Hierarchy:**
1. High-volume WRs (8+ targets) usually beat committee RBs
2. Workhorse RBs (70%+ snap share) usually beat WR3s
3. Pass-catching RBs (5+ targets) are premium FLEX plays
4. TEs rarely win FLEX spots unless elite (Kelce, Andrews tier)

**FLEX Decision Framework:**
| Scenario | Recommendation |
|----------|----------------|
| WR with 8+ targets vs RB with <4 targets | Start WR |
| Workhorse RB vs boom/bust WR | Start RB (safer floor) |
| Committee RB vs consistent WR2 | Start WR |
| Pass-catching RB vs low-target WR | Start RB |

**Key Insight:** In PPR, receptions provide a floor that pure rushers lack. A WR with 6 catches for 50 yards (11 pts) beats an RB with 15 carries for 60 yards and no receptions (6 pts).

### Same-Team Player Comparisons

When comparing two players from the same team (e.g., WR1 vs WR2):

**Considerations:**
- **Target distribution:** Research typical target split between them
- **Role differences:** One may be the deep threat, one the possession receiver
- **Red zone usage:** Who gets looks inside the 20?
- **Coverage:** Elite CB may shadow WR1, opening up WR2

**General Rules:**
| Situation | Recommendation |
|----------|----------------|
| Clear WR1 vs WR2 | Start WR1 unless shadow coverage confirmed |
| Co-WR1s (split targets) | Favor better matchup or recent hot hand |
| RB1 vs backup on same team | Always start RB1 unless injury concern |
| WR vs TE on same team | Favor higher target share player |

**Correlation Consideration:** Starting two players from the same team caps your ceiling (if offense struggles, both suffer) but also provides stability (if offense explodes, both benefit).

---

## Common Pitfalls

### Mistakes to Avoid

1. **Recommending drafted=1 players** — ALWAYS verify drafted status (column 8) in players.csv before suggesting any player. Only drafted=0 (available) or drafted=2 (owned) should be recommended.
2. **Recency bias** — Don't overweight one great/bad game
3. **Name value** — Start the better matchup, not the bigger name
4. **Ignoring volume** — Volume > efficiency for fantasy (especially in PPR)
5. **Overlooking game script** — Heavy underdogs abandon the run
6. **Weather dismissal** — Cold affects specific players differently (research history)
7. **Teammate injury oversight** — Always check for WR1/RB1 injuries
8. **Considering day-of-week as factor** — TNF/MNF/SNF should NOT influence rankings; only scoring environment matters
9. **Snap share for returning players** — First game back often limited
10. **Ignoring garbage time** — Players on bad teams can rack up PPR points in blowout losses
11. **Trusting efficiency over volume** — A 15-target WR with 8 YPT beats a 5-target WR with 15 YPT in PPR

### Red Flags to Highlight

Always call out these concerns:

- Player returning from IR (snap count likely limited)
- QB with documented cold-weather struggles
- Backup QB starting (affects all pass-catchers)
- Key O-line injuries (affects entire offense)
- Divisional rivalry (often lower scoring than expected)
- International game (travel fatigue)

### Factors to IGNORE

Do NOT consider these in rankings:

- **Day of week** (TNF/MNF/SNF) - Game time is irrelevant to scoring
- **Primetime games** - No statistical edge; narrative-driven bias
- **Roster flexibility** - Focus on expected points, not lineup management strategy
- **"Lock-in before other games"** - Scheduling is not a scoring factor

---

## Quality Checklist

**IMPORTANT:** This checklist must be completed AND included in your final report. It serves two purposes:
1. Ensures you don't skip required analysis steps
2. Shows the user that analysis was thorough

### Pre-Report Verification (Internal)

Before writing the report, verify you have gathered:

- [ ] Vegas O/U and spread for each relevant game
- [ ] Weather forecast for all outdoor games
- [ ] Week-by-week stats (last 3-5 games) for each player
- [ ] Target share % OR snap share % for each player
- [ ] Defensive rankings vs. position for each matchup
- [ ] **Drafted status (column 8 in players.csv) for ALL players being recommended**

**If any of these are missing, STOP and gather the data before proceeding.**

### Report Sections Checklist (Must Include All)

Verify your report contains EVERY mandatory section:

- [ ] **Executive Summary** — Quick recommendation table
- [ ] **Game Environment (Vegas Lines)** — O/U, spread, implied totals for ALL games
- [ ] **Weather Conditions** — Temperature, wind, impact level for ALL outdoor games
- [ ] **Volume Metrics Summary** — Target share/snap share with threshold comparison
- [ ] **Recent Performance Tables** — Week-by-week (NOT just averages) for key players
- [ ] **Head-to-Head Comparison (10-Factor)** — ALL 10 factors filled in, not 3-4
- [ ] **Key Monitoring Points** — What to watch before kickoff
- [ ] **Quality Checklist** — THIS checklist, included at end of report
- [ ] **Sources** — All links cited

### Data Verification (Include in Report)

- [ ] Confirmed correct Week N matchup for each player
- [ ] Verified player's current team (check for trades/signings)
- [ ] Checked injury report (not just status, but practice participation)
- [ ] Confirmed weather forecast is for game day (not current weather)
- [ ] **Verified drafted status in players.csv (column 8) - only drafted=0 or drafted=2 recommended**

### Analysis Completeness (Include in Report)

- [ ] All 10 factors considered for each player (see Head-to-Head table)
- [ ] Recent performance reviewed (minimum 3 games with week-by-week data)
- [ ] Defensive matchup researched (position-specific rankings)
- [ ] Game environment evaluated (Vegas O/U, spread, implied total)
- [ ] Weather checked for ALL outdoor games (not just cold ones)

### Report Quality (Include in Report)

- [ ] Clear recommendation provided (START/SIT) for each player
- [ ] Floor and ceiling estimated for each player
- [ ] Head-to-head comparison table included with ALL 10 factors
- [ ] All sources cited with links
- [ ] Reasoning is specific to each player, not generic

### Sanity Checks (Include in Report)

- [ ] Recommendations align with consensus (if not, explanation provided)
- [ ] No obvious factors overlooked (QB injury, weather, volume changes)
- [ ] Key monitoring points identified for user to track before kickoff

### Quality Checklist Template for Reports

**COPY THIS** to the end of every report:

```markdown
## Quality Checklist (per Starter Research Guide)

### Data Verification
- [x] Confirmed correct Week N matchups for each player
- [x] Verified player's current team (no trades/signings)
- [x] Checked injury report (status + practice participation)
- [x] Confirmed weather forecast is for game day
- [x] **Verified drafted status (players.csv column 8) - only drafted=0 or drafted=2 recommended**

### Analysis Completeness
- [x] All 10 factors considered for each player (see Head-to-Head tables)
- [x] Recent performance reviewed (minimum 3 games with week-by-week data)
- [x] Defensive matchup researched (position-specific)
- [x] Game environment evaluated (Vegas lines)
- [x] Weather checked for outdoor games

### Report Quality
- [x] Clear recommendation provided (START/SIT)
- [x] Floor and ceiling estimated for each player
- [x] Head-to-head comparison table included (10-factor format)
- [x] All sources cited with links
- [x] Reasoning is specific, not generic

### Sanity Checks
- [x] Recommendations align with consensus (or deviation explained)
- [x] No obvious factors overlooked
- [x] Key monitoring points identified for updates before kickoff
```

---

## Example Research Workflow

### Scenario: User asks "Start Waddle or Wilson this week?"

**Step 1: Initial Searches (parallel)**
```
"Jaylen Waddle Week 15 2025 fantasy projections PPR start sit"
"Michael Wilson Week 15 2025 fantasy projections PPR start sit"
"Dolphins Steelers Week 15 2025 matchup"
"Cardinals Texans Week 15 2025 matchup"
"NFL Week 15 2025 weather outdoor games"
```

**Step 2: Matchup Deep Dive**
```
"Steelers pass defense 2025 fantasy points allowed WR"
"Texans pass defense 2025 fantasy points allowed WR Derek Stingley"
```

**Step 3: Context Searches**
```
"Tua Tagovailoa cold weather career stats"
"Marvin Harrison Jr injury status Week 15 2025"
"Michael Wilson targets without MHJ"
```

**Step 4: Verification**
```
"Waddle Wilson Week 15 fantasy rankings comparison WR"
```

**Step 5: Compile and Analyze**
- Build comparison table
- Identify key differentiators
- Make recommendation with clear reasoning

### Example Final Output (Abbreviated)

After completing the research above, your recommendation might look like:

```markdown
## Quick Verdict: Start Wilson over Waddle

| Factor | Wilson | Waddle | Edge |
|--------|--------|--------|------|
| Projection | 14.2 | 13.8 | Even |
| Matchup | Tough (HOU #3 vs WR) | Good (PIT #28 vs WR) | Waddle |
| Volume | 16+ tgt (MHJ out) | 7 tgt/game | **Wilson** |
| Weather | Dome | Freezing (teens) | **Wilson** |
| QB Context | Brissett (backup) | Tua (0-5 in cold) | **Wilson** |
| Recent | 30.8 PPG last 3 | 7.9 PPG last 3 | **Wilson** |

**Confidence: High** — Wilson's elite volume (MHJ ruled OUT) overcomes
the tough matchup. Tua's 0-5 cold-weather record is disqualifying for Waddle.

**Floor/Ceiling:**
- Wilson: 8 floor / 25 ceiling (volume)
- Waddle: 4 floor / 22 ceiling (weather risk)
```

---

## Quick Decision Mode

When time is limited (user needs a fast answer), use this abbreviated process:

### 5-Minute Analysis

**Step 1: One search per player (parallel)**
```
"{Player Name} Week {N} {Year} start sit fantasy PPR"
```

**Step 2: Extract key data points**
- Projection
- Matchup rating (favorable/neutral/tough)
- Any injury concerns
- Recent trend (hot/cold)

**Step 3: Quick comparison**
| Factor | Player A | Player B |
|--------|----------|----------|
| Projection | X | Y |
| Matchup | Good/Bad | Good/Bad |
| Trend | Hot/Cold | Hot/Cold |
| Injury | Yes/No | Yes/No |

**Step 4: Recommend based on majority of factors**

### When Quick Mode is Acceptable

- User explicitly asks for quick advice
- Comparing only 2 players
- Both players are clearly startable (choosing between two good options)
- Regular season (lower stakes)

### When Full Analysis is Required

- Fantasy playoffs
- Comparing 3+ players
- One player has concerning factors (injury, returning from IR)
- User has expressed this is a critical decision
- Weather is a major factor (outdoor cold-weather game)

---

## Appendix: Reference Tables

### Fantasy Points Allowed Rankings

**IMPORTANT:** This guide uses "Fantasy Points Allowed" ranking where #1 = WORST defense (allows most).

| Rank | Meaning | Action |
|------|---------|--------|
| #1-8 | Allows MOST points (bad defense) | **Start player** — elite matchup |
| #9-16 | Above average points allowed | Lean start |
| #17-24 | Below average points allowed | Lean sit |
| #25-32 | Allows FEWEST points (good defense) | **Consider sitting** — tough matchup |

See [Defense Ranking Clarification](#defense-ranking-clarification) for detailed explanation.

### Target Share Tiers (WR/TE)

| Tier | Target Share | Interpretation |
|------|--------------|----------------|
| Elite | 25%+ | Must start |
| Strong | 20-24% | Start most weeks |
| Average | 15-19% | Matchup dependent |
| Low | 10-14% | Boom/bust, risky |
| Minimal | <10% | Avoid unless desperate |

### Snap Share Tiers (RB)

| Tier | Snap Share | Interpretation |
|------|------------|----------------|
| Workhorse | 70%+ | Must start |
| Lead back | 55-69% | Start most weeks |
| Committee lead | 40-54% | Need PPR upside |
| Backup | <40% | Avoid unless injury |

### Vegas O/U Interpretation

| O/U Total | Game Environment | Impact |
|-----------|------------------|--------|
| 54+ | Shootout expected | Boost all skill players significantly |
| 48-53 | High-scoring | Boost skill players |
| 44-47 | Average | Neutral |
| 40-43 | Lower scoring | Slight concern for pass-catchers |
| <40 | Low scoring / defensive | Downgrade passing game significantly |

**Note:** This table aligns with the Step 4 interpretation guide. Use consistently throughout reports.

### PPR Value Shifts

| Player Type | PPR Impact |
|-------------|------------|
| Pass-catching RBs | **Major boost** — floor raised significantly |
| Slot WRs | **Boost** — high volume, shorter routes = more catches |
| Target hogs | **Boost** — even inefficient targets add value |
| TD-dependent players | **Reduced** — TDs matter less as % of total |
| Efficient low-volume players | **Hurt** — fewer touches = fewer points |

### PPR Floor Boosters

These factors specifically raise floor in PPR:
- RB with 4+ targets per game (PPR RB2 floor)
- WR with 7+ targets per game (PPR WR3 floor)
- TE who runs routes on 80%+ of snaps
- Players on teams that trail often (garbage time receptions)

### PPR Red Flags

These factors hurt players more in PPR:
- RB with <2 targets per game
- WR with declining target share (3+ week trend)
- TE in blocking-heavy scheme
- Players on run-heavy teams that protect leads

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-15 | 1.7 | **Agent readability update:** Added "CRITICAL RULES FOR AGENTS - READ FIRST" section at top with 5 common mistakes, 5 core principles, and quick compliance check. Fixed Matchup Grade Scale to use correct Fantasy Points Allowed convention (#1-3 = A+, not #30-32). Added Snap Share Decision Guide to RB section clarifying 40-54% committee zone. Numbered all 20 templates for easy reference. Updated template index with REQUIRED markers. Clarified RB start threshold (55%+ instead of 60%). |
| 2025-12-15 | 1.6 | **Consistency & completeness update:** Fixed O/U interpretation inconsistency (aligned Step 4 and Appendix). Fixed target share tier inconsistency (now 25%+ = elite everywhere). Added "touch" definition (carries + receptions). Added Goal-line role to RB data points. Added 8 new templates: ECR Presentation, Win Probability/Game Script, Pre-Injury Baseline, HOT/COLD Trend Labels, Threshold Compliance Explanation, Breaking News Protocol, Projected Lineup Total, Defense Ranking Clarification. Clarified defense ranking direction throughout (Fantasy Points Allowed convention). Updated Table of Contents. |
| 2025-12-15 | 1.5 | **Advanced metrics update:** Added thresholds to all position-specific data. Added new metrics: YPRR, EPA/target, route share, first-read share, yards before contact, red zone efficiency, TD equity, role designation. Added TE streaming-specific data points. Added Advanced Metrics Reference table. Added templates: Tier System, Matchup Grade Scale (A+ to F), QB Cold Weather History, Defense Rankings Breakdown, Matchups to Avoid, Scenario-Based Guidance, Role Designation Reference. |
| 2025-12-15 | 1.4 | **Major update:** Added mandatory report templates (10-factor table, week-by-week tables, Vegas lines table, weather table, volume metrics table, key monitoring points table). Clarified that Quality Checklist must be INCLUDED in reports. Added "Sections That Are Commonly Missed" warning. Added "Pre-Report Verification" checklist. Made Game Environment, Weather, Volume Metrics, 10-Factor Comparison, and Key Monitoring Points explicitly MANDATORY sections. |
| 2025-12-12 | 1.3 | Added: Time estimates, player name disambiguation, example final output, fixed O/U inconsistency, reduced redundancy |
| 2025-12-12 | 1.2 | Added: TL;DR quick reference, FLEX decisions, same-team comparisons, failed search handling, consolidated appendix, Vegas O/U table |
| 2025-12-12 | 1.1 | Added: Before You Start, Conflict Resolution, Confidence Levels, Quick Decision Mode, PPR-specific insights |
| 2025-12-12 | 1.0 | Initial guide created based on Week 15 WR/RB analysis methodology |
