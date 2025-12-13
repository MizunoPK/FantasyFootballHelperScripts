# Starter Helper Research Guide (PPR)

A comprehensive guide for agents conducting start/sit analysis for **Full PPR** fantasy football weekly decisions.

> **Scoring Format:** This guide is optimized for Full PPR (1 point per reception). Target volume and receptions are weighted heavily in all recommendations.

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
7. [Report Structure](#report-structure)
8. [Position-Specific Considerations](#position-specific-considerations) (incl. FLEX, Same-Team)
9. [Common Pitfalls](#common-pitfalls)
10. [Quality Checklist](#quality-checklist)
11. [Quick Decision Mode](#quick-decision-mode)
12. [Appendix: Reference Tables](#appendix-reference-tables)

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
data/players.csv          → Current projections, injury status
data/team_data/{TEAM}.csv → Defensive rankings by position
data/game_data.csv        → Weather, location data
```

If the user has the league_helper running, the `Starter Helper Mode` can provide baseline scores. Web research supplements this with context the algorithm doesn't capture.

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
| Data Point | Why It Matters |
|------------|----------------|
| Target share % | Direct measure of opportunity |
| Air yard share % | Depth of targets (ceiling indicator) |
| Routes run | Snap involvement in passing game |
| Red zone targets | TD probability |
| QB performance/health | Pass-catcher value tied to QB |
| Opponent CB injuries | Specific coverage matchup |

#### Running Backs
| Data Point | Why It Matters |
|------------|----------------|
| Snap share % | Playing time indicator |
| Carries per game | Volume floor |
| Targets per game | PPR upside |
| Red zone carries | TD probability |
| Yards per carry (YPC) | Efficiency (but volume > efficiency) |
| Opponent run defense DVOA | Matchup quality |

#### Quarterbacks
| Data Point | Why It Matters |
|------------|----------------|
| Pass attempts per game | Volume indicator |
| Rushing upside | Dual-threat floor |
| Opponent pass defense rank | Matchup quality |
| Weather conditions | Major impact on passing |
| O-line health | Time to throw |

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

**Interpretation Guide:** (See Appendix for detailed table)
| O/U Total | Implication |
|-----------|-------------|
| 48+ | High-scoring, boost skill players |
| 44-47 | Average environment |
| 40-43 | Lower scoring, slight concern |
| <40 | Negative environment, downgrade passing game |

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

Every start/sit report should include:

```markdown
# Week {N} {Position} Start/Sit Analysis

## Executive Summary
Quick recommendation table with rankings

## Player Analysis
For each player:
- Projection and floor/ceiling
- Why Start (bullet points)
- Concerns (bullet points)
- Recent performance table

## Head-to-Head Comparison
Comparison table across all factors

## Key Matchup Factors
- Defensive rankings
- Weather (if applicable)
- Game environment (Vegas lines)

## Final Verdict
- Clear recommendation
- Tiebreaker reasoning

## Sources
- All sources cited with links
```

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
- Snap share ≥60%
- Opponent allows top-12 fantasy points to RB
- Team favored (positive game script)
- Goal-line role secured

**Key Sit Indicators:**
- Snap share ≤40% or declining
- Committee backfield with unclear roles
- Team is heavy underdog (will abandon run)
- Returning from injury (first game back)
- Opponent has elite run defense AND team will be trailing

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

1. **Recency bias** — Don't overweight one great/bad game
2. **Name value** — Start the better matchup, not the bigger name
3. **Ignoring volume** — Volume > efficiency for fantasy (especially in PPR)
4. **Overlooking game script** — Heavy underdogs abandon the run
5. **Weather dismissal** — Cold affects specific players differently (research history)
6. **Teammate injury oversight** — Always check for WR1/RB1 injuries
7. **Thursday games** — Short rest affects some players
8. **Snap share for returning players** — First game back often limited
9. **Ignoring garbage time** — Players on bad teams can rack up PPR points in blowout losses
10. **Trusting efficiency over volume** — A 15-target WR with 8 YPT beats a 5-target WR with 15 YPT in PPR

### Red Flags to Highlight

Always call out these concerns:

- Player returning from IR (snap count likely limited)
- QB with documented cold-weather struggles
- Backup QB starting (affects all pass-catchers)
- Key O-line injuries (affects entire offense)
- Divisional rivalry (often lower scoring than expected)
- International game (travel fatigue)

---

## Quality Checklist

Before finalizing any start/sit recommendation, verify:

### Data Verification
- [ ] Confirmed correct Week N matchup for each player
- [ ] Verified player's current team (check for trades/signings)
- [ ] Checked injury report (not just status, but practice participation)
- [ ] Confirmed weather forecast is for game day

### Analysis Completeness
- [ ] All 10 factors considered for each player
- [ ] Recent performance reviewed (minimum 3 games)
- [ ] Defensive matchup researched (position-specific)
- [ ] Game environment evaluated (Vegas lines)
- [ ] Weather checked (outdoor games)

### Report Quality
- [ ] Clear recommendation provided (START/SIT)
- [ ] Floor and ceiling estimated for each player
- [ ] Head-to-head comparison table included
- [ ] All sources cited with links
- [ ] Reasoning is specific, not generic

### Sanity Checks
- [ ] Does recommendation align with consensus? If not, explain why
- [ ] Are there any obvious factors being overlooked?
- [ ] Would a follow-up search change the recommendation?

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

| Rank | Meaning | Action |
|------|---------|--------|
| 1-8 | Allows MOST points (bad defense) | Start player |
| 9-16 | Above average points allowed | Lean start |
| 17-24 | Below average points allowed | Lean sit |
| 25-32 | Allows FEWEST points (good defense) | Consider sitting |

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
| 54+ | Shootout expected | Boost all skill players |
| 48-53 | High scoring | Slight boost |
| 44-47 | Average | Neutral |
| 40-43 | Lower scoring | Slight concern for pass-catchers |
| <40 | Low scoring / defensive | Downgrade passing game significantly |

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
| 2025-12-12 | 1.3 | Added: Time estimates, player name disambiguation, example final output, fixed O/U inconsistency, reduced redundancy |
| 2025-12-12 | 1.2 | Added: TL;DR quick reference, FLEX decisions, same-team comparisons, failed search handling, consolidated appendix, Vegas O/U table |
| 2025-12-12 | 1.1 | Added: Before You Start, Conflict Resolution, Confidence Levels, Quick Decision Mode, PPR-specific insights |
| 2025-12-12 | 1.0 | Initial guide created based on Week 15 WR/RB analysis methodology |
