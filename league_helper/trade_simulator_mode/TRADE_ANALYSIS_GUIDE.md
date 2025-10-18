# Trade Analysis Guide for Claude Agents

## Purpose
This guide provides step-by-step instructions for analyzing fantasy football trade proposals and creating comprehensive trade recommendations that include both expert fantasy analysis and opponent acceptance likelihood.

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Read and Understand the Trade File](#step-1-read-and-understand-the-trade-file)
4. [Step 2: Identify the User's Roster](#step-2-identify-the-users-roster)
5. [Step 3: Research Player Expert Opinions](#step-3-research-player-expert-opinions)
6. [Step 4: Identify Opponent Rosters](#step-4-identify-opponent-rosters)
7. [Step 5: Analyze Each Trade](#step-5-analyze-each-trade)
8. [Step 6: Create the Recommendations File](#step-6-create-the-recommendations-file)
9. [Trade Analysis Framework](#trade-analysis-framework)
10. [Output Format Standards](#output-format-standards)
11. [Quality Checklist](#quality-checklist)

---

## Overview

**Input:** A trade info file (e.g., `trade_info_2025-10-18_06-36-20.txt`) containing:
- Multiple trade proposals
- Player stats and projections
- Team improvement scores

**Output:** A recommendations file (e.g., `trade_recommendations_2025-10-18.txt`) containing:
- Ranked trade recommendations (best to worst)
- Expert fantasy football analysis for each player
- Opponent roster analysis and acceptance likelihood
- Strategic advice and action plan

**Time Estimate:** 30-45 minutes for comprehensive analysis

---

## Prerequisites

### Required Information
- Trade info file path
- Current NFL week number
- Current NFL season year
- User's team name (to identify their roster)

### Required Tools
- WebSearch tool (for expert opinions)
- Read tool (for file access)
- Grep/Bash tools (for roster extraction)
- Write tool (for output file creation)

### Knowledge Requirements
- Fantasy football scoring formats (PPR, half-PPR, standard)
- Player positions and roles
- Current NFL season context (injuries, trades, etc.)

---

## Step 1: Read and Understand the Trade File

### 1.1 Locate the Trade File

```bash
# Trade files are typically in:
league_helper/trade_simulator_mode/trade_outputs/trade_info_YYYY-MM-DD_HH-MM-SS.txt
```

### 1.2 Handle Large Files

Trade files can be very large (>250KB). Use these strategies:

```python
# Read first 200 lines to see structure
Read(file_path, offset=1, limit=200)

# Read specific sections
Read(file_path, offset=200, limit=150)

# Use Bash for quick checks
bash: head -n 100 "/path/to/trade_file.txt"
bash: tail -n 50 "/path/to/trade_file.txt"
```

### 1.3 Understand File Format

Each trade proposal follows this structure:

```
#N - Trade with [Opponent Team Name]
  My improvement: +XX.XX pts (New score: XXXX.XX)
  Their improvement: +XX.XX pts (New score: XXXX.XX)
  I give:
    - [POS] [TEAM] Player Name - XX.XX pts (Bye=X)
            - Projected: XXX.XX pts, Weighted: XX.XX pts
            - Player Rating: [RATING]
            - Team Quality: [QUALITY]
            - Performance: [RATING] (+/-X.X%)
            - Bye Overlaps: X same-position, X different-position
  I receive:
    - [POS] [TEAM] Player Name - XX.XX pts (Bye=X)
            - [Same structure as above]
```

### 1.4 Extract Key Information

For each trade, note:
- **Trade number** (#1, #2, etc.)
- **Opponent team name**
- **Players given** (positions, teams, current performance)
- **Players received** (positions, teams, current performance)
- **Point improvement scores** (ignore these per user instruction)

---

## Step 2: Identify the User's Roster

### 2.1 Read Drafted Data File

```python
Read("/path/to/data/drafted_data.csv")
```

Format: `Player Name Position - Team, Owner Team Name`

### 2.2 Extract User's Team

```bash
# If user's team is "Sea Sharp":
grep "Sea Sharp" "/path/to/data/drafted_data.csv"
```

### 2.3 Organize Roster by Position

Create a mental (or written) roster structure:

```
QB: [Players]
RB: [Players]
WR: [Players]
TE: [Players]
K: [Kicker]
DST: [Defense]
```

### 2.4 Identify Roster Strengths/Weaknesses

Categorize:
- **STRENGTHS**: Positions with elite/multiple good players
- **WEAKNESSES**: Positions with injuries/busts/lack of depth
- **PRIORITY NEEDS**: Most critical positions to upgrade

---

## Step 3: Research Player Expert Opinions

### 3.1 Identify Key Players to Research

From the top 10-15 trades, identify:
1. **All players the user would receive** (highest priority)
2. **Key players the user would give up** (to understand trade-offs)
3. **Players experts might have strong opinions about**

### 3.2 Web Search Strategy

**Search Query Format:**
```
"[Player Name] fantasy football week [X] [YEAR] outlook FantasyPros"
```

**Examples:**
```
"Alvin Kamara fantasy football week 7 2025 outlook FantasyPros"
"Tony Pollard fantasy football week 7 2025 outlook FantasyPros reddit"
"Xavier Worthy fantasy football week 7 2025 ROS outlook trade value"
```

**Search Variations:**
- Add "reddit" for community sentiment
- Add "trade value" for sell/buy recommendations
- Add "ROS" (rest of season) for long-term outlook
- Add "injury" if player has health concerns

### 3.3 Run Parallel Searches

**IMPORTANT:** Run 5-6 searches in parallel for efficiency:

```python
WebSearch("Player A week 7 outlook")
WebSearch("Player B fantasy outlook")
WebSearch("Player C trade value")
WebSearch("Player D reddit fantasy")
WebSearch("Player E injury update")
WebSearch("Player F ROS outlook")
```

### 3.4 Extract Key Information from Results

For each player, document:

**Week-Specific Outlook:**
- Opponent matchup quality
- Expected role/usage
- Injuries or limitations
- Expert start/sit recommendations

**Rest-of-Season (ROS) Outlook:**
- Trend (improving/declining)
- Role security
- Injury concerns
- Expert buy/sell recommendations

**Key Quotes:**
- Expert consensus (e.g., "FantasyPros: priority sell")
- Specific stats (e.g., "70.2% route share since Week 4")
- Matchup data (e.g., "Titans allow most rushing TDs")

### 3.5 Player Categories

Categorize players based on expert consensus:

**ACQUIRE (Good targets):**
- Elite performers
- Trending up
- Secure roles
- Favorable ROS schedule

**AVOID (Bad targets):**
- Trending down
- Losing snaps/targets
- Injury concerns
- Bad matchups/schedule

**SELL HIGH:**
- Overperforming expectations
- Role about to diminish
- Injury risk increasing

**BUY LOW:**
- Underperforming talent
- Positive regression expected
- Role expanding

### 3.6 Document Source Citations

Keep track of where info came from:
- FantasyPros expert analysis
- Reddit community consensus
- Yahoo Sports rankings
- ESPN projections
- Specific expert names when available

---

## Step 4: Identify Opponent Rosters

### 4.1 Extract All Opponent Rosters

From `drafted_data.csv`, extract rosters for:
- The Eskimo Brothers
- Pidgin
- Striking Shibas
- Saquon Deez
- Annihilators
- Chase-ing points
- (Any other teams involved in trades)

```bash
grep "The Eskimo Brothers" "/path/to/drafted_data.csv"
grep "Pidgin" "/path/to/drafted_data.csv"
# etc.
```

### 4.2 Organize Each Opponent's Roster

For each opponent, create structure:

```
TEAM NAME:
  QB: [Players]
  RB: [Players]
  WR: [Players]
  TE: [Players]
  K: [Kicker]
  DST: [Defense]
```

### 4.3 Identify Team Strengths/Weaknesses

For each opponent:
- **SURPLUS POSITIONS**: Where they have depth to spare
- **DEFICIT POSITIONS**: Where they need help
- **INJURY SITUATIONS**: Players on IR, questionable, etc.

**Example:**
```
Striking Shibas:
  SURPLUS: RB (Achane, Williams, Mason, Jones on IR returning, Mixon)
  DEFICIT: WR (only have Jefferson as elite, need WR2)
  INJURIES: Aaron Jones (IR, returning soon)
```

### 4.4 Determine Trade Motivations

For each team, ask:
- What positions would they trade FROM? (surplus)
- What positions would they trade FOR? (deficit)
- Are they competing or rebuilding?
- Do they have injury concerns making them desperate?

---

## Step 5: Analyze Each Trade

### 5.1 Analyze from User's Perspective

**For each trade, evaluate:**

**A. PLAYERS GIVEN UP**
- Position value (are they starters or bench?)
- Replacement options (who fills the gap?)
- Expert outlook (should they be traded?)
- Emotional attachment (proven vs unproven)

**B. PLAYERS RECEIVED**
- Position need (does this address weakness?)
- Expert outlook (trending up or down?)
- Role security (starter or timeshare?)
- Immediate impact (Week 7) vs long-term value

**C. NET IMPACT**
- Does this improve starting lineup?
- Does this improve depth?
- Risk level (injuries, role changes)
- Upside potential

**D. GRADING SCALE**
- **A (Strongly Recommend):** Clear upgrade, low risk
- **B (Recommend):** Good value, moderate risk
- **C (Neutral/Consider):** Lateral move or trade-offs
- **D-F (Do Not Recommend):** Bad value or high risk

### 5.2 Analyze from Opponent's Perspective

**For each trade, evaluate WHY opponent would accept:**

**A. WHAT THEY GET**
- Does it fill a need? (deficit position)
- Is it an upgrade over current player?
- Does it provide depth/insurance?
- Is the value fair or better for them?

**B. WHAT THEY GIVE**
- Can they afford to lose this player? (surplus position)
- Is player trending down (sell high)?
- Do they have replacement options?
- Is the value fair or worse for them?

**C. ACCEPTANCE LIKELIHOOD**

**Very High (70-90%):**
- Clearly addresses their biggest need
- Trading from surplus position
- Gets best player in deal
- Win-win or favors them

**High (60-75%):**
- Addresses a need well
- Can spare player being traded
- Fair value proposition

**Medium (40-60%):**
- Lateral move
- Some upside but also risk
- Depends on their strategy/preferences

**Low (25-40%):**
- Gives up too much value
- Doesn't address pressing needs
- Better options available elsewhere

**Very Low (<25%):**
- Clearly bad for them
- Trades away core player for depth
- No pressing need for return pieces

### 5.3 Calculate Overall Trade Value

**Formula:**
```
Trade Value = (User Benefit Grade × 40%) + (Acceptance Likelihood × 60%)
```

**Why weight acceptance higher?**
- Best trades are worthless if they won't be accepted
- Need realistic proposals, not wishful thinking
- Focus on win-win scenarios

**Example:**
- Trade gets Grade A (excellent for user) = 90/100
- Acceptance likelihood is 30% = 30/100
- Overall value = (90 × 0.4) + (30 × 0.6) = 36 + 18 = 54/100 (mediocre)

vs.

- Trade gets Grade B (good for user) = 80/100
- Acceptance likelihood is 70% = 70/100
- Overall value = (80 × 0.4) + (70 × 0.6) = 32 + 42 = 74/100 (much better)

---

## Step 6: Create the Recommendations File

### 6.1 File Structure

```markdown
================================================================================
FANTASY FOOTBALL TRADE RECOMMENDATIONS - WEEK [X], [YEAR]
================================================================================
Based on expert analysis from FantasyPros, Reddit, Yahoo Sports, and other sources
Generated: [DATE]
Source File: [ORIGINAL_TRADE_FILE_NAME]

================================================================================
CURRENT ROSTER ANALYSIS
================================================================================
[User's strengths, weaknesses, priority needs]

================================================================================
TRADE RECOMMENDATIONS - RANKED BEST TO WORST
================================================================================

[Individual trade analyses in order]

================================================================================
SUMMARY & ACTION PLAN
================================================================================
[Strategic recommendations sorted by acceptance likelihood]

================================================================================
TRADE RANKINGS SUMMARY (VALUE + ACCEPTANCE LIKELIHOOD)
================================================================================
[Tiered rankings with grades and acceptance percentages]

================================================================================
END OF RECOMMENDATIONS
================================================================================
```

### 6.2 Individual Trade Format

For EACH trade, include these sections:

```markdown
--------------------------------------------------------------------------------
RANK #N - [RECOMMENDATION TIER] ★★★★★
Trade #X from original file
--------------------------------------------------------------------------------
GIVE: [Player A] + [Player B]
GET:  [Player C] + [Player D]

EXPERT REASONING:

✓ POSITIVE FACTOR 1: [Explanation]
  - Supporting detail 1
  - Supporting detail 2
  - Expert quote or stat

✓ POSITIVE FACTOR 2: [Explanation]
  - Supporting details...

✗ NEGATIVE FACTOR 1: [Explanation]
  - Supporting details...

VERDICT: [2-3 sentence summary of recommendation]

WHY [OPPONENT TEAM] ACCEPTS THIS TRADE:

THEIR ROSTER:
- RBs: [Players]
- WRs: [Players]
- [Other relevant positions]
- [Strengths/weaknesses summary]

✓ ACCEPTANCE REASON 1: [Why this helps them]
  - Specific details
  - Roster context

✓ ACCEPTANCE REASON 2: [Why they can spare players]
  - Depth analysis
  - Replacement options

✗ CONCERN: [Why they might hesitate]
  - What they're giving up
  - Alternative options

LIKELIHOOD THEY ACCEPT: [Percentage] ([X-Y]%)
- [Bullet points explaining likelihood]

RISK LEVEL: [Low/Medium/High/Very High]
REWARD POTENTIAL: [Low/Medium/High/Very High]
OVERALL GRADE: [A/B/C/D/F]
```

### 6.3 Use Visual Indicators

**Recommendation Tiers:**
- ★★★★★ (5 stars) = Strongly Recommend
- ★★★★☆ (4 stars) = Recommend
- ★★★☆☆ (3 stars) = Cautiously Recommend / Consider
- ★★☆☆☆ (2 stars) = Do Not Recommend
- ★☆☆☆☆ (1 star) = Strongly Avoid

**Acceptance Likelihood:**
- ★★★ = Very High (70%+)
- ★★ = Medium-High (50-70%)
- ★ = Low-Medium (30-50%)
- (No stars) = Very Low (<30%)

**Checkmarks/X-marks:**
- ✓ = Positive factor
- ✗ = Negative factor
- ❌ = Critical red flag
- 🎯 = Key opportunity
- ⚠️ = Warning/caution

---

## Trade Analysis Framework

### Framework Overview

For EACH trade, systematically analyze:

1. **User's Perspective (40% weight)**
   - What they give up
   - What they receive
   - Net roster impact
   - Expert opinions on players

2. **Opponent's Perspective (60% weight)**
   - Their roster needs/surplus
   - Why they'd want this trade
   - Acceptance likelihood
   - Fairness from their view

### User's Perspective Analysis

#### Step 1: Analyze Players Given

For each player the user would trade away:

**A. Current Role & Production**
- Starting lineup or bench?
- Recent performance trend (improving/declining/stable)
- Actual points scored vs projections
- Share of team's offense (snap %, target %, touches)

**B. Expert Outlook**
- Week-specific matchup (favorable/unfavorable)
- Rest-of-season trajectory (improving/declining)
- Injury concerns or health status
- Buy/sell/hold recommendation from experts

**C. Replacement Analysis**
- Who fills this roster spot if traded?
- Is replacement adequate or significant downgrade?
- Does user have depth at this position?

**D. Trade Value**
- Is this player being sold high or low?
- Are they a "priority sell" according to experts?
- Is their current value inflated/deflated?

#### Step 2: Analyze Players Received

For each player the user would acquire:

**A. Immediate Impact**
- Week 7 matchup quality
- Immediate starter or depth piece?
- Bye week considerations (can't start Week 7?)
- Injury status (healthy/questionable/returning)

**B. Rest-of-Season Value**
- Expert outlook (trending up/down/stable)
- Role security (starter, timeshare, backup)
- Remaining schedule quality
- Playoff schedule (Weeks 14-17)

**C. Position Need**
- Does this address user's weakness?
- Upgrade over current starter?
- Adds needed depth?
- Creates logjam at already-strong position?

**D. Risk Assessment**
- Injury history/current injuries
- Role volatility (committee backfield, WR rotation)
- Team offense quality (good/bad offense)
- Expert concerns or red flags

#### Step 3: Calculate Net Impact

**Starting Lineup Impact:**
- Does this improve Week 7 starting lineup?
- Does this improve ROS starting lineup?
- Upgrade/downgrade at each position affected

**Depth Chart Impact:**
- Does this improve bench quality?
- Better injury insurance?
- More bye week coverage?

**Risk vs Reward:**
- High risk, high reward (boom/bust players)
- Low risk, steady value (consistent producers)
- Risk level: Low/Medium/High/Very High
- Reward potential: Low/Medium/High/Very High

**Overall Grade (A-F):**
- **A:** Clear upgrade, low risk, addresses needs
- **B:** Good upgrade, moderate risk, good value
- **C:** Lateral move, trade-offs, speculation
- **D:** Questionable value, high risk, doesn't help much
- **F:** Bad trade, very high risk, clear downgrade

### Opponent's Perspective Analysis

#### Step 1: Understand Their Roster

**A. Extract Full Roster**
```bash
grep "Opponent Team Name" /path/to/drafted_data.csv
```

**B. Categorize by Position**
- **QB:** List all QBs
- **RB:** List all RBs (note injuries, byes)
- **WR:** List all WRs (note injuries, byes)
- **TE:** List all TEs (note injuries, byes)
- **K/DST:** Note their kicker and defense

**C. Identify Strengths**
- Positions with elite players (top 10 at position)
- Positions with good depth (3+ startable players)
- Surplus areas (can afford to trade away)

**D. Identify Weaknesses**
- Positions with only one startable player
- Positions with injuries/busts
- Deficit areas (need upgrades desperately)

#### Step 2: Analyze What They Receive

**A. Fills a Need?**
- Trading for their weakest position = high value
- Trading for their strength = low value
- Upgrading starter = medium-high value
- Adding depth = low-medium value

**B. Quality of Return**
- Getting best player in trade = more likely to accept
- Getting equal value = depends on needs
- Getting worse players = unlikely unless fills critical need

**C. Name Value & Perception**
- Elite names (even if declining) carry weight
- Breakout players attractive to some owners
- Proven veterans vs unproven rookies

#### Step 3: Analyze What They Give Up

**A. Can They Afford It?**
- Trading from surplus position = easy to accept
- Trading from deficit position = hard to accept
- Trading their only good player at position = very unlikely

**B. Selling High or Low?**
- Player trending down = they want to sell (easier accept)
- Player trending up = they want to keep (harder accept)
- Overperforming = sell high opportunity (easier accept)
- Underperforming = buy low opportunity (harder accept)

**C. Replacement Options**
- Have quality backup ready = easier to trade starter
- No depth behind player = harder to trade
- Player returning from IR = current starter expendable

#### Step 4: Calculate Acceptance Likelihood

**Very High (70-90%):**
- ✓ Clearly addresses their biggest weakness
- ✓ Trading from their surplus position
- ✓ Gets clearly best player in deal
- ✓ Opponents getting good value or winning trade

**High (60-75%):**
- ✓ Addresses a clear need
- ✓ Can spare player(s) being traded
- ✓ Fair value, maybe slight edge to them
- ✓ Win-win scenario

**Medium (40-60%):**
- ~ Lateral move overall
- ~ Some positions helped, some hurt
- ~ Fair value but debatable
- ~ Depends on their strategy/risk tolerance

**Low (25-40%):**
- ✗ Doesn't clearly address needs
- ✗ Trading from area they're already weak
- ✗ Questionable value proposition
- ✗ Better options likely available elsewhere

**Very Low (<25%):**
- ✗ Clearly bad for them
- ✗ Gives up best player for depth pieces
- ✗ Trading strength to add to strength
- ✗ No logical reason to accept

#### Step 5: Write Acceptance Analysis

**Template:**
```markdown
WHY [OPPONENT TEAM] ACCEPTS THIS TRADE:

THEIR ROSTER:
- RBs: [Player1], [Player2], [Player3] (note strengths/weaknesses)
- WRs: [Player1], [Player2], [Player3] (note strengths/weaknesses)
- [Other relevant positions]
- [One-line strength/weakness summary]

✓ REASON 1: [Primary motivation for accepting]
  - Specific roster context
  - How trade helps them
  - What problem it solves

✓ REASON 2: [Secondary motivation]
  - Why they can afford to trade away their players
  - Depth analysis showing replacements

✓ REASON 3: [Additional factors]
  - Timing considerations (byes, injuries)
  - Value proposition from their view

✗ CONCERN: [Why they might hesitate]
  - What they're giving up
  - Risk factors for them
  - Alternative options they have

LIKELIHOOD THEY ACCEPT: [Tier] ([X-Y]%)
- [2-3 bullet points explaining the likelihood assessment]
- [Factors that could push it higher or lower]
- [Overall assessment of trade fairness from their view]
```

**Example:**
```markdown
WHY STRIKING SHIBAS ACCEPTS THIS TRADE:

THEIR ROSTER:
- RBs: De'Von Achane (RB1), Kyren Williams (RB2), Jordan Mason, Blake Corum, Aaron Jones (IR), Joe Mixon (NFI-R)
- WRs: Justin Jefferson (elite WR1), Drake London (inconsistent), Tetairoa McMillan (rookie), Ladd McConkey (boom/bust)
- Deep at RB, desperately need WR2

✓ WADDLE IS MASSIVE WR UPGRADE: Current WR2 situation is dire
  - Justin Jefferson is elite, but need reliable WR2
  - Drake London is inconsistent, McMillan is unproven rookie
  - Waddle (WR15 in PPR) is immediate upgrade and consistent
  - With Tyreek Hill out for season, Waddle is Miami's clear WR1

✓ CAN EASILY SPARE MASON: Ridiculous RB depth makes him expendable
  - Aaron Jones returning from IR (was Vikings RB1 before injury)
  - Joe Mixon could return (Texans RB1 when healthy)
  - Achane + Kyren Williams are solid RB1/RB2 without Mason
  - Mason has value but they don't need him

✓ HENDERSON IS FREE LOTTERY TICKET: High upside, no downside
  - Henderson has high draft capital (2nd round rookie)
  - Patriots could pivot to him if he breaks out
  - Even if he busts, they have RB depth to absorb it

✗ SELLING McMillan: Giving up promising rookie WR
  - McMillan showing flashes (8th-most deep targets, 14th-most RZ targets)
  - Panthers WR1 with guaranteed volume
  - "Star in the making" per FantasyPros
  - BUT: Waddle is proven commodity, McMillan is still unproven

LIKELIHOOD THEY ACCEPT: Very High (70-80%)
- They're STACKED at RB with Jones/Mixon returning, can easily spare Mason
- WR corps is weak outside Jefferson, desperately need consistency
- Waddle slots in immediately as WR2 and provides weekly floor
- Henderson as throw-in has upside with zero risk given their RB depth
- This trade heavily favors them while still helping user - true win-win
```

---

## Output Format Standards

### File Naming Convention

```
trade_recommendations_YYYY-MM-DD.txt
```

Example: `trade_recommendations_2025-10-18.txt`

### Section Order (MANDATORY)

1. **Header** (Title, metadata, source file)
2. **Current Roster Analysis** (User's strengths/weaknesses)
3. **Trade Recommendations** (Ranked #1 to #N, best to worst)
4. **Summary & Action Plan** (Strategic recommendations)
5. **Trade Rankings Summary** (Tiered list with grades)
6. **Realistic Trade Strategy** (Acceptance likelihood ranking)
7. **Opponent Roster Analysis Summary** (All teams categorized)
8. **Final Recommendation** (Specific action steps)
9. **End marker**

### Ranking Philosophy

**Primary Sort:** Value to user (expert analysis)
**Secondary Sort:** Acceptance likelihood (practicality)

**Rank by:**
1. Trades that are BOTH good value AND likely to be accepted
2. Trades that are excellent value but unlikely to be accepted
3. Trades that are okay value and likely to be accepted
4. Trades that are bad value (regardless of acceptance)

### Writing Style Guidelines

**DO:**
- ✓ Use clear, direct language
- ✓ Support claims with expert quotes or stats
- ✓ Provide specific examples and details
- ✓ Use bullet points for readability
- ✓ Include visual indicators (✓, ✗, ★)
- ✓ Write in second person ("you should")
- ✓ Explain reasoning, not just conclusions

**DON'T:**
- ✗ Use vague language ("might", "could", "possibly")
- ✗ Make claims without evidence
- ✗ Write long paragraphs (use bullets)
- ✗ Use emojis excessively
- ✗ Assume user knows context
- ✗ Be wishy-washy (make clear recommendations)

### Tone Guidelines

**Be:**
- **Direct:** "This trade is bad. Don't do it."
- **Confident:** "Expert consensus: Pollard is a priority sell."
- **Practical:** "70% acceptance likelihood makes this your best bet."
- **Balanced:** "Waddle is good, but you're giving up WR15."

**Avoid:**
- **Hedging:** "This might potentially be good if..."
- **Uncertainty:** "It's hard to say whether..."
- **Passive:** "It could be argued that..."
- **Jargon without explanation:** Don't assume they know terms

---

## Quality Checklist

Before finalizing the recommendations file, verify:

### Content Completeness

- [ ] All top 10 trades analyzed (minimum)
- [ ] Each trade has expert reasoning section
- [ ] Each trade has opponent acceptance analysis
- [ ] User's current roster documented
- [ ] All opponent rosters identified
- [ ] Web research completed for key players
- [ ] Grades assigned (A-F) for each trade
- [ ] Acceptance percentages provided for each trade
- [ ] Action plan section completed
- [ ] Trade rankings summary included

### Expert Research Quality

- [ ] Minimum 5-6 web searches conducted
- [ ] FantasyPros opinions included
- [ ] Current week matchup analysis included
- [ ] Rest-of-season outlooks documented
- [ ] Expert quotes/stats cited
- [ ] Buy/sell/hold recommendations noted
- [ ] Injury status checked for relevant players
- [ ] Trending information (up/down) identified

### Opponent Analysis Quality

- [ ] All opponent rosters extracted
- [ ] Strengths/weaknesses identified for each team
- [ ] Surplus/deficit positions documented
- [ ] Trade motivations explained
- [ ] Acceptance likelihood justified
- [ ] Specific roster context provided
- [ ] Alternative options considered

### Strategic Value

- [ ] Trades ranked by realistic value (not just theoretical)
- [ ] Win-win trades identified and prioritized
- [ ] Bad trades clearly flagged
- [ ] Acceptance likelihood factored into rankings
- [ ] Players to target/avoid clearly listed
- [ ] Specific action order provided
- [ ] Trap trades (high acceptance, bad value) warned against

### Writing Quality

- [ ] Clear, concise language used
- [ ] Bullet points for readability
- [ ] Visual indicators used appropriately
- [ ] Sections properly formatted
- [ ] No typos or grammatical errors
- [ ] Consistent terminology throughout
- [ ] Logical flow and organization

### Format Compliance

- [ ] Correct file naming convention
- [ ] All required sections included
- [ ] Section order matches standard
- [ ] Consistent formatting throughout
- [ ] Proper use of dividers (===, ---)
- [ ] Trade analysis template followed
- [ ] Grading scale used consistently

---

## Common Pitfalls to Avoid

### Research Pitfalls

**❌ DON'T:**
- Rely on one source (need multiple expert opinions)
- Skip web research because "I know the player"
- Use outdated information (check current week)
- Ignore injury reports
- Miss recent news (trades, role changes, suspensions)

**✓ DO:**
- Cross-reference multiple expert sources
- Check both FantasyPros AND Reddit/Yahoo
- Verify current week matchup details
- Look for recent news (last 24-48 hours)
- Research both sides of every trade

### Analysis Pitfalls

**❌ DON'T:**
- Assume best value trade = best realistic trade
- Ignore opponent's perspective
- Recommend trades they'll never accept
- Overlook bye weeks (can't trade for player on bye Week 7)
- Forget about user's depth (trading starters for depth is risky)

**✓ DO:**
- Weight acceptance likelihood heavily (60%)
- Analyze from opponent's roster situation
- Prioritize win-win scenarios
- Check bye weeks for all players
- Consider user's replacement options

### Writing Pitfalls

**❌ DON'T:**
- Write vague recommendations ("might be good")
- Fail to explain reasoning
- Use jargon without explanation
- Make it too long (walls of text)
- Be inconsistent with grades/rankings

**✓ DO:**
- Make clear, decisive recommendations
- Support every claim with evidence
- Explain fantasy football terms
- Use bullets and formatting for readability
- Ensure grades match written analysis

---

## Advanced Tips

### Identifying Trade Patterns

**Pattern 1: The Desperate Seller**
- Opponent has player trending down sharply
- They're trying to dump before complete collapse
- Often propose trades heavily favoring them
- **Strategy:** Avoid these trades (Pollard example)

**Pattern 2: The Win-Win**
- User trades from strength (WR depth)
- Opponent trades from strength (RB depth)
- Both fill needs
- **Strategy:** Prioritize these (highest acceptance + fair value)

**Pattern 3: The Wishful Thinking**
- User gets clearly best player
- Opponent gets depth pieces
- Very low acceptance likelihood
- **Strategy:** Try proposing but don't expect acceptance (Kamara example)

**Pattern 4: The Trap**
- Opponent would eagerly accept
- But it's terrible value for user
- Looks tempting due to high acceptance likelihood
- **Strategy:** Clearly warn against these

### Psychology of Trade Acceptance

**Owners are more likely to accept when:**
- ✓ Trade addresses their obvious weakness
- ✓ They're trading from clear surplus
- ✓ They get the "name value" player
- ✓ Recent news makes their player concerning (injury, benching)
- ✓ They're losing games and desperate

**Owners are less likely to accept when:**
- ✗ They drafted player high (attachment)
- ✗ Player is their team's namesake
- ✗ Trade doesn't clearly help them
- ✗ They're winning and don't want to rock the boat
- ✗ Too many players involved (complex trades)

### Timing Considerations

**Week 7 Specific Factors:**
- Bye weeks (Ravens, Falcons on bye = players unusable)
- Injury reports (Wednesday-Friday updates)
- Waiver wire (Tuesday night adds affect rosters)
- Trade deadlines (varies by league, often Week 10-12)

**Rest-of-Season Factors:**
- Playoff schedule (Weeks 14-17 matchups)
- Players returning from injury
- Role changes after bye weeks
- Weather considerations (late season)

### Customization for League Format

**PPR vs Standard vs Half-PPR:**
- PPR: Value pass-catching RBs/WRs higher
- Standard: Value TD-dependent players higher
- Half-PPR: Middle ground

**Roster Settings:**
- Deep benches = value depth more
- Shallow benches = value elite starters more
- 2QB/Superflex = QBs worth much more
- TE Premium = TEs worth more

**Scoring Quirks:**
- Bonus points for long TDs
- Points per first down
- Deductions for turnovers
- Custom defensive scoring

---

## Example Workflow

### Real Example: Analyzing Trade #7 (Kamara Deal)

**Input:** Trade file shows:
- GIVE: TreVeyon Henderson + Rhamondre Stevenson
- GET: Alvin Kamara + 49ers D/ST

**Step 1: Research Players**

```python
WebSearch("Alvin Kamara fantasy football week 7 2025 outlook FantasyPros")
WebSearch("TreVeyon Henderson fantasy football week 7 2025 Patriots reddit")
WebSearch("Rhamondre Stevenson fantasy football week 7 2025 outlook")
```

**Step 2: Extract Key Findings**

**Kamara:**
- Ankle injury (questionable)
- RB28 in half-PPR (7.9 PPG)
- Maintains receiving role (59.4% route share)
- ESPN: "lineup lock" for Week 7
- Snap share declining (85% → 53%)

**Henderson:**
- BUST: Zero explosive runs through 6 weeks
- 46th in missed tackle rate
- Season-low 29.7% snap rate
- Experts: "panic about Henderson"

**Stevenson:**
- Good Week 7 matchup (Titans allow most rushing TDs)
- Gets 83% of goal-line attempts
- Low volume (10.7 touches, 51.9 yards per game)
- Only 2 top-20 finishes

**Step 3: Analyze User's Perspective**

**Grade: A**
- Dumps Henderson (confirmed bust)
- Trades Stevenson (limited upside)
- Gets Kamara (proven RB1/2 despite injury)
- Consolidates two weak RBs into one quality RB

**Step 4: Research Opponent (Saquon Deez)**

```bash
grep "Saquon Deez" /path/to/drafted_data.csv
```

**Their Roster:**
- RBs: Saquon Barkley (elite), Alvin Kamara, J.K. Dobbins
- WRs: Davante Adams, DK Metcalf, DJ Moore
- Strong at both RB and WR

**Step 5: Analyze Opponent's Perspective**

**Why they might accept:**
- ✓ Have Saquon as clear RB1, can spare Kamara
- ✓ Getting two Patriots RBs hedges their bets
- ✓ Kamara injury is concerning

**Why they probably won't:**
- ✗ Kamara >> Henderson + Stevenson in value
- ✗ They don't need depth, already have Dobbins
- ✗ No pressing need to downgrade

**Acceptance Likelihood: 30-40% (Low)**

**Step 6: Write Analysis**

```markdown
--------------------------------------------------------------------------------
RANK #1 - STRONGLY RECOMMEND ★★★★★
Trade #7 from original file
--------------------------------------------------------------------------------
GIVE: TreVeyon Henderson + Rhamondre Stevenson
GET:  Alvin Kamara + 49ers D/ST

EXPERT REASONING:

✓ DUMP HENDERSON: Experts unanimously say he's a bust
  - Zero explosive runs through 6 weeks
  - Ranks 46th in missed tackle rate, 47th in yards after contact
  - FantasyPros: "Fantasy managers should panic about Henderson's poor output"

✓ UPGRADE TO KAMARA: Despite concerns, still a proven RB1/2
  - Currently RB28 in half-PPR (7.9 PPG)
  - Ankle injury concern (limited practice, questionable)
  - BUT: Maintains receiving role (59.4% route share)
  - ESPN lists him as a "lineup lock" for Week 7

[... continue with full analysis ...]

WHY SAQUON DEEZ ACCEPTS THIS TRADE:

THEIR ROSTER:
- RBs: Saquon Barkley (elite RB1), Alvin Kamara, J.K. Dobbins
- WRs: Davante Adams, DK Metcalf, DJ Moore, Emeka Egbuka
- Strong at WR, stacked at RB

✓ DEPTH PLAY: They have Saquon Barkley as clear RB1
  - Can afford to move Kamara (ankle injury concern)
  - J.K. Dobbins is solid RB2

[... continue with full analysis ...]

LIKELIHOOD THEY ACCEPT: Medium (30-40%)
- They're strong at RB, might not need depth
- Would need to be very concerned about Kamara's ankle

OVERALL GRADE: A
```

---

## Final Notes

### Time Management

**Recommended time allocation:**
- 10 min: Reading trade file and extracting key trades
- 15 min: Web research (6-8 parallel searches)
- 10 min: Opponent roster analysis
- 30 min: Writing trade analyses
- 10 min: Creating summary sections
- 5 min: Quality check and proofreading

**Total: 80 minutes for comprehensive analysis**

### When to Ask for Help

If you encounter:
- **Unclear roster data:** Ask user for their team name
- **Missing opponent data:** Ask user to verify opponent teams
- **League format questions:** Ask about PPR/Standard, roster settings
- **Conflicting expert opinions:** Present both sides, make recommendation
- **Unusual player names:** Search multiple variations to find correct player

### Continuous Improvement

After completing analysis:
- Note which expert sources were most helpful
- Track accuracy of acceptance predictions
- Learn from any mistakes in player evaluation
- Refine template based on user feedback

---

## Appendix: Common Fantasy Football Terms

### Scoring Formats
- **PPR:** Points Per Reception (1 point per catch)
- **Half-PPR:** 0.5 points per reception
- **Standard:** No points for receptions

### Player Roles
- **RB1/WR1/etc:** Top-tier starter at position
- **RB2/WR2/etc:** Solid starter, not elite
- **Flex:** Utility position (RB/WR/TE)
- **Handcuff:** Backup who'd be valuable if starter injured
- **Committee:** Multiple players sharing position (timeshare)

### Metrics
- **Snap %:** Percentage of offensive snaps player is on field
- **Target Share:** Percentage of team's pass targets
- **Route %:** Percentage of pass plays WR runs a route
- **Touch Share:** Percentage of team's RB carries + targets
- **RZ Targets:** Red zone (inside 20 yard line) targets

### Trends
- **Buy Low:** Acquire undervalued player (talent > production)
- **Sell High:** Trade overvalued player (production > talent)
- **Trending Up:** Recent performance improving
- **Trending Down:** Recent performance declining
- **Positive Regression:** Expected improvement toward talent level
- **Negative Regression:** Expected decline toward talent level

### Roster Terms
- **Depth:** Quality backup players on bench
- **Handcuff:** Backup to own starter (insurance)
- **Lottery Ticket:** Low-owned player with huge upside if gets chance
- **Waiver Wire:** Pool of free agent players to claim

### Trade Terms
- **Win-Win:** Both teams improve
- **Fleece:** Very lopsided trade (one team wins big)
- **Buy Low:** Target struggling player with good talent
- **Sell High:** Trade productive player before decline
- **2-for-1:** Trade 2 players for 1 better player (consolidate)
- **3-for-2:** Trade 3 players for 2 better players

---

## End of Guide

This guide should enable any Claude agent to perform comprehensive fantasy football trade analysis. Remember: the goal is to provide actionable, realistic recommendations that balance expert analysis with practical acceptance likelihood.

Good luck with your trade analyses!
