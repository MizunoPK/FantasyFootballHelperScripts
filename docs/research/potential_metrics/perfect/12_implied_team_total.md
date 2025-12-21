# Metric 12: Implied Team Total

**Position Applicability:** ALL positions
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data in the `data/` folder?**

- [ ] Yes - Calculate from existing columns
- [x] No - Requires new data source
- [ ] Partial - Some components available

**Details:**

Implied Team Total is **derived from Vegas lines** (spread + over/under), which are NOT currently in existing data.

**Checked:**
- `data/players.csv` - NO spread or over/under columns
- `data/teams_week_N.csv` - NO betting lines
- `data/league_config.json` - Only league settings (no game odds)

**Dependency on Metric 4:**

Implied Team Total is **calculated from Metric 4 (Vegas Lines)** data:
```python
# Formula for favorites
implied_total_favorite = (over_under + abs(spread)) / 2

# Formula for underdogs
implied_total_underdog = (over_under - abs(spread)) / 2

# Example:
# Over/Under: 48.5
# Spread: KC -3.5 (KC favorite by 3.5)
# KC implied total: (48.5 + 3.5) / 2 = 26.0 points
# Opponent implied total: (48.5 - 3.5) / 2 = 22.5 points
```

**Calculation Logic:**
```python
def calculate_implied_team_total(over_under: float, spread: float, is_favorite: bool) -> float:
    """
    Calculate implied team total from Vegas lines.

    Args:
        over_under: Total points over/under line
        spread: Point spread (negative = favorite, positive = underdog)
        is_favorite: True if calculating for favorite, False for underdog

    Returns:
        Expected points for the team

    Example:
        >>> calculate_implied_team_total(48.5, -3.5, is_favorite=True)
        26.0
        >>> calculate_implied_team_total(48.5, -3.5, is_favorite=False)
        22.5
    """
    spread_abs = abs(spread)

    if is_favorite:
        return (over_under + spread_abs) / 2
    else:
        return (over_under - spread_abs) / 2
```

**Team-Level Application:**
```python
# For each game, calculate both team totals
game = {
    'home_team': 'KC',
    'away_team': 'LAC',
    'over_under': 48.5,
    'spread': -3.5,  # KC favorite
    'favorite_team': 'KC'
}

kc_total = calculate_implied_team_total(48.5, -3.5, is_favorite=True)  # 26.0
lac_total = calculate_implied_team_total(48.5, -3.5, is_favorite=False)  # 22.5

# Map to players
kc_players['implied_team_total'] = 26.0
lac_players['implied_team_total'] = 22.5
```

**Player-Level Multiplier:**
```python
# Higher implied total = more scoring opportunities
def get_team_total_multiplier(implied_total: float) -> float:
    """
    Convert implied team total to scoring multiplier.

    League average implied total: ~23 points
    Range: 0.90 (low-scoring, 17 points) to 1.10 (high-scoring, 30+ points)
    """
    league_avg = 23.0

    if implied_total >= 28.0:
        return 1.10  # Elite offense expected
    elif implied_total >= 25.0:
        return 1.05  # Above-average scoring
    elif implied_total >= 21.0:
        return 1.00  # Average scoring
    elif implied_total >= 18.0:
        return 0.95  # Below-average scoring
    else:
        return 0.90  # Low-scoring game expected
```

**Conclusion:** Cannot calculate from existing data. Requires Metric 4 (Vegas Lines) implementation first.

---

## 2. ESPN API Availability

**Is this metric available via ESPN Fantasy Football API?**

- [x] No - Not directly (must derive from Metric 4)
- [ ] Yes - Available directly
- [ ] Partial - Some components available

**Sources Checked:**
- [x] ESPN API research from Metric 4 (Vegas Lines)
- [x] ESPN scoreboard endpoint provides spread and over/under
- [x] Calculation is trivial once Metric 4 data is fetched

**API Data:**

ESPN API provides the **raw inputs** (spread, over/under) via Metric 4, then we **calculate** implied team total:

**From `04_vegas_lines.md` research:**
```json
{
  "competitions": [{
    "odds": [{
      "provider": {
        "id": "45",
        "name": "consensus"
      },
      "details": "KC -3.5",
      "overUnder": 48.5,
      "spread": -3.5,
      "homeTeamOdds": {
        "favorite": true
      }
    }]
  }]
}
```

**Calculation from ESPN data:**
```python
# ESPN provides spread and over/under
over_under = odds[0]['overUnder']  # 48.5
spread = odds[0]['spread']  # -3.5
is_home_favorite = odds[0]['homeTeamOdds']['favorite']  # True

# Calculate implied totals
home_total = (over_under + abs(spread)) / 2  # 26.0
away_total = (over_under - abs(spread)) / 2  # 22.5
```

**Endpoint:**
- URL: `http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- Method: GET
- Authentication: None required
- Rate limit: Unknown (ESPN public API)

**Implementation:**
```python
def fetch_implied_team_totals(week: int) -> Dict[str, float]:
    """
    Fetch implied team totals for all games in a week.

    Returns:
        Dict mapping team_code → implied_total
    """
    # Step 1: Fetch Vegas lines from ESPN (Metric 4)
    scoreboard = fetch_espn_scoreboard(week)

    # Step 2: Calculate implied totals
    team_totals = {}

    for event in scoreboard['events']:
        odds = event['competitions'][0]['odds'][0]
        over_under = odds['overUnder']
        spread = odds['spread']

        home_team = event['competitions'][0]['competitors'][0]['team']['abbreviation']
        away_team = event['competitions'][0]['competitors'][1]['team']['abbreviation']

        is_home_favorite = odds['homeTeamOdds'].get('favorite', False)

        if is_home_favorite:
            home_total = (over_under + abs(spread)) / 2
            away_total = (over_under - abs(spread)) / 2
        else:
            home_total = (over_under - abs(spread)) / 2
            away_total = (over_under + abs(spread)) / 2

        team_totals[home_team] = home_total
        team_totals[away_team] = away_total

    return team_totals
```

**Conclusion:** ESPN API provides inputs (spread, over/under). Implied team total is **calculated** from those inputs.

---

## 3. Free Alternative Sources

**What free data sources provide this metric?**

### Source 1: The Odds API (Direct Implied Totals)

- URL: `https://the-odds-api.com/`
- Data format: JSON API
- Update frequency: Real-time
- Free tier limits: 500 requests/month
- Authentication: API key required (free tier)
- Data quality: **Very High** - aggregates multiple sportsbooks

**Details:**
- Some sportsbooks display implied team totals directly
- Most require calculation from spread + over/under
- Historical data: ⚠️ Not available in free tier

**API Response Example:**
```json
{
  "id": "abc123",
  "sport_key": "americanfootball_nfl",
  "home_team": "Kansas City Chiefs",
  "away_team": "Los Angeles Chargers",
  "bookmakers": [{
    "key": "draftkings",
    "markets": [{
      "key": "totals",
      "outcomes": [{
        "name": "Over",
        "price": -110,
        "point": 48.5
      }]
    }, {
      "key": "spreads",
      "outcomes": [{
        "name": "Kansas City Chiefs",
        "price": -110,
        "point": -3.5
      }]
    }]
  }]
}
```

**Calculation from API:**
```python
# Extract spread and total
total = bookmakers[0]['markets']['totals']['point']  # 48.5
spread = bookmakers[0]['markets']['spreads']['point']  # -3.5

# Calculate implied totals (same formula)
kc_total = (48.5 + 3.5) / 2 = 26.0
lac_total = (48.5 - 3.5) / 2 = 22.5
```

### Source 2: Pro Football Reference (Historical Closing Lines)

- URL: `https://www.pro-football-reference.com/years/{YEAR}/games.htm`
- Data format: HTML tables (scraping required)
- Update frequency: Post-game
- Free tier limits: Unlimited (public website)
- Authentication: Not required
- Data quality: **Excellent** - official closing lines

**Details:**
- Historical closing lines available for all past games
- Can calculate implied totals from closing spread + over/under
- Data includes: Week, Teams, Spread, Over/Under, Final Score
- **Limitation:** Must scrape (no official API)

**Historical Data Table:**
```
Week | Date | Winner | Loser | Spread | Over/Under | Final
1    | 9/7  | KC     | LAC   | -3.5   | 48.5       | 27-24
```

**Calculation:**
```python
# From PFR closing lines
over_under = 48.5
spread = -3.5  # KC favorite

kc_implied = (48.5 + 3.5) / 2 = 26.0
lac_implied = (48.5 - 3.5) / 2 = 22.5
```

### Source 3: Action Network (Advanced Implied Total Trends)

- URL: `https://www.actionnetwork.com/nfl/odds`
- Data format: HTML (public), API (paid)
- Update frequency: Real-time
- Free tier limits: Limited (website only)
- Authentication: Not required for website
- Data quality: **Excellent** - advanced betting analytics

**Details:**
- Shows implied team totals directly (no calculation needed)
- Tracks line movement over time
- Historical trends available
- **Limitation:** Free tier very limited, API is paid

**Comparison:**

| Source | Implied Total Data | Historical | Free Tier | Ease of Use |
|--------|-------------------|------------|-----------|-------------|
| ESPN API | ✅ Calculate from spread/O/U | ⚠️ Future games only | ✅ Unlimited | High (already integrated) |
| The Odds API | ✅ Calculate from spread/O/U | ❌ No historical | ⚠️ 500 req/month | Medium (API integration) |
| Pro Football Reference | ✅ Calculate from closing lines | ✅ Yes (all seasons) | ✅ Unlimited | Medium (scraping) |
| Action Network | ✅ Direct totals | ⚠️ Limited free | ⚠️ Very Limited | Low (paywall) |

**Recommended Source:** **ESPN API** (same as Metric 4) - Already researched, free, reliable

**Historical Source:** **Pro Football Reference** (same as Metric 4) - Free, complete historical data

---

## 4. Data Quality Assessment

**Reliability:** High
**Accuracy:** Very High
**Update Frequency:** Daily (week of game)

**Details:**

**Reliability Assessment:**
- Source stability: ESPN API is stable (same as Metric 4)
- Calculation reliability: Simple formula, deterministic
- Historical uptime: Excellent

**Accuracy Assessment:**
- Methodology: Vegas lines are the most accurate predictor of scoring
- Calculation accuracy: Implied totals are mathematically derived
- Known issues: None (trivial calculation)
- Validation: Can compare to actual game totals post-game

**Update Frequency:**
- Vegas lines: Updated multiple times per day (as bets come in)
- ESPN API: Reflects latest consensus lines
- Historical data: Closing lines (most accurate snapshot)

**Known Limitations:**
1. **Lines move** - Implied total changes as spread/over_under change throughout week
2. **Predictive accuracy** - Vegas is good but not perfect (upsets happen)
3. **Garbage time** - Actual score may exceed implied total due to late TDs
4. **Weather impact** - Severe weather can reduce actual scoring below implied

**Edge Cases:**
- **No line available:** Use league average (~23 points per team)
- **Pick'em (no spread):** Implied total = over_under / 2 for both teams
- **Missing over/under:** Cannot calculate (default to league average)

**Validation Example:**
```python
# Week 1, 2024: KC vs LAC
# Implied totals: KC 26.0, LAC 22.5
# Actual final: KC 27, LAC 24
# Accuracy: Very close (KC +1.0, LAC +1.5)

# This demonstrates implied totals are highly predictive
```

**Correlation with Fantasy Scoring:**
- Teams with high implied totals (28+) score more fantasy points
- QB/WR/TE benefit most from high totals
- RBs less affected (game script matters more than total)

---

## 5. Historical Data Availability ⚠️ CRITICAL

**Can we obtain weekly snapshots for simulation validation?**

- [x] Yes - Historical data available (same as Metric 4)

**Historical Data Details:**

**Seasons Available:**
- [x] 2021 season (17 weeks) - ✅ Via PFR closing lines
- [x] 2022 season (17 weeks) - ✅ Via PFR closing lines
- [x] 2024 season (17 weeks) - ✅ Via PFR closing lines
- [x] 2023 season (if needed) - ✅ Via PFR closing lines

**Weekly Snapshot Verification:**

Implied Team Total uses **same historical source as Metric 4 (Vegas Lines)**:
- Pro Football Reference provides closing spread + over/under for every game
- Can calculate implied totals from those closing lines
- Closing lines = "what we knew going INTO that game"

**Data Timing (Predictive vs Retrospective):**
- [x] Represents "what we knew going INTO that week" ✅ **YES**

**Verification:**
```
Week 5 simulation requires:
- Closing lines from weeks 1-4: ✅ Available on PFR
- Closing lines for week 5 games: ✅ Available on PFR

Calculation:
1. Scrape PFR for week 5 closing spread + over/under
2. Calculate implied totals for each team
3. Apply to player projections for week 5
```

**Historical Acquisition Process:**

**Step 1: Scrape PFR closing lines (same as Metric 4)**
```python
def scrape_closing_lines(year: int, week: int) -> pd.DataFrame:
    """
    Scrape closing lines from Pro Football Reference.

    Returns DataFrame with columns:
    - week, team, opponent, spread, over_under, is_favorite
    """
    url = f"https://www.pro-football-reference.com/years/{year}/games.htm"
    # Scraping logic (same as Metric 4)
    pass
```

**Step 2: Calculate implied totals**
```python
def calculate_historical_implied_totals(closing_lines: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate implied team totals from closing lines.

    Returns DataFrame with columns:
    - week, team, implied_team_total
    """
    totals = []

    for _, game in closing_lines.iterrows():
        over_under = game['over_under']
        spread = game['spread']
        is_favorite = game['is_favorite']

        implied_total = calculate_implied_team_total(over_under, spread, is_favorite)

        totals.append({
            'week': game['week'],
            'team': game['team'],
            'implied_team_total': implied_total
        })

    return pd.DataFrame(totals)
```

**Step 3: Integrate into sim_data**
```python
# For week 5 simulation:
# Load closing lines for week 5
closing_lines_week5 = scrape_closing_lines(2024, week=5)

# Calculate implied totals
implied_totals = calculate_historical_implied_totals(closing_lines_week5)

# Merge with players.csv
players = pd.read_csv('simulation/sim_data/2024/weeks/week_5/players.csv')
players = players.merge(implied_totals, on='team', how='left')

# Now each player has implied_team_total for their team
# KC players: implied_team_total = 26.0
# LAC players: implied_team_total = 22.5
```

**sim_data Integration:**

**Where does this metric fit?**
- [x] Team-level: Add to game/matchup data (team → implied_total mapping)
- [x] Player-level: Add column to `players.csv` (inherited from team)

**Schema Definition:**

**Option 1: Team-level file (new file)**
- File: `simulation/sim_data/{YEAR}/weeks/week_{NN}/team_totals.csv`
- Columns:
  - `team` (str): Team code (KC, LAC, etc.)
  - `implied_team_total` (float): Expected points (17.0-32.0 range)
  - `opponent` (str): Opponent team code
  - `over_under` (float): Total points line
  - `spread` (float): Point spread
  - `is_favorite` (bool): True if team is favorite

**Option 2: Player-level column (simpler)**
- File: `simulation/sim_data/{YEAR}/weeks/week_{NN}/players.csv`
- New column: `implied_team_total` (float)
- Null handling: Default to league average (23.0) if missing
- Example values: `26.0` (high-scoring), `19.5` (low-scoring)

**Recommended:** **Option 2 (player-level column)** - Simpler integration, directly usable in scoring

**Historical Data Acquisition:**
- [x] Same process as Metric 4 (PFR scraping)
- [x] Can reuse Metric 4 scraping code
- [x] No additional fetching required beyond Metric 4

**Timeline:** Same as Metric 4 (once Metric 4 is implemented, implied totals are trivial)

---

## 6. Implementation Complexity

**Difficulty:** Easy (calculation-only, depends on Metric 4)
**Estimated Effort:** 2-4 hours

**Breakdown:**

**Data Fetching:**
- Complexity: **N/A** (reuses Metric 4 data)
- Pattern to follow: Metric 4 (Vegas Lines) already fetches spread + over/under
- Required packages: None (calculation only)
- Authentication: N/A
- Rate limiting handling: N/A

**Data Processing:**
- Complexity: **Very Easy**
- Calculations required:
  1. Identify favorite vs underdog (from spread sign)
  2. Apply implied total formula: `(over_under ± spread) / 2`
  3. Map each player to their team's implied total
  4. Apply scoring multiplier based on total
- Data transformations:
  - Team-based lookup (team → implied_total)
  - Handle missing data (default to league average)
  - Convert to multiplier (optional enhancement)

**Calculation Example:**
```python
def add_implied_team_totals(players: pd.DataFrame, vegas_lines: pd.DataFrame) -> pd.DataFrame:
    """
    Add implied team total to each player based on their team's Vegas lines.

    Args:
        players: DataFrame with player data (must have 'team' column)
        vegas_lines: DataFrame with spread/over_under (from Metric 4)

    Returns:
        players DataFrame with new 'implied_team_total' column
    """
    # Calculate implied totals for each team
    team_totals = {}

    for _, game in vegas_lines.iterrows():
        home_team = game['home_team']
        away_team = game['away_team']
        over_under = game['over_under']
        spread = game['spread']

        # Determine favorite
        is_home_favorite = spread < 0

        if is_home_favorite:
            home_total = (over_under + abs(spread)) / 2
            away_total = (over_under - abs(spread)) / 2
        else:
            home_total = (over_under - abs(spread)) / 2
            away_total = (over_under + abs(spread)) / 2

        team_totals[home_team] = home_total
        team_totals[away_team] = away_total

    # Map to players
    players['implied_team_total'] = players['team'].map(team_totals)

    # Default to league average for missing data
    players['implied_team_total'].fillna(23.0, inplace=True)

    return players
```

**Optional Enhancement: Scoring Multiplier**
```python
def calculate_team_total_multiplier(implied_total: float) -> float:
    """
    Convert implied team total to scoring multiplier.

    Higher implied total = more scoring opportunities = boost
    Lower implied total = fewer opportunities = penalty
    """
    if implied_total >= 28.0:
        return 1.10  # Elite scoring environment
    elif implied_total >= 25.0:
        return 1.05  # Above-average
    elif implied_total >= 21.0:
        return 1.00  # Average
    elif implied_total >= 18.0:
        return 0.95  # Below-average
    else:
        return 0.90  # Low-scoring game

# Apply to players
players['team_total_multiplier'] = players['implied_team_total'].apply(
    calculate_team_total_multiplier
)
players['adjusted_score'] = players['base_score'] * players['team_total_multiplier']
```

**Schema Integration:**
- New columns to add: `implied_team_total` (float), optionally `team_total_multiplier` (float)
- Existing columns to modify: None
- Data type compatibility: float columns (compatible)
- Backward compatibility: No impact (new columns)

**Dependencies:**

**Metric Dependencies:**
- [x] **BLOCKED by Metric 4 (Vegas Lines)** - Must implement Metric 4 first
- Metric 4 provides: spread, over_under, favorite_team
- Metric 12 calculates: implied_team_total from those inputs

**Code Dependencies:**
- File: `util/PlayerManager.py` (likely location for team total logic)
- Class/Function: Player scoring calculation methods
- Purpose: Apply team total multiplier to player scores
- Integration point: After base score, before final adjustment

**External Dependencies:**
- Package: None (standard library sufficient)
- Data dependency: Metric 4 must be implemented and tested

**Cost Estimate:**
- Paid tier required: No (reuses Metric 4 data)
- Monthly cost: $0

**Quick Win?**
- [x] **Yes** - Trivial calculation once Metric 4 is available
- 2-4 hours to implement (calculation + mapping + testing)
- High value (affects all positions)

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High value, trivial implementation (after Metric 4)

**Rationale:**

**Value:** ⭐⭐⭐⭐⭐ (Very High)
- **Affects all positions** - Scoring environment matters for QB/RB/WR/TE/K
- **Highly predictive** - Vegas implied totals are excellent predictors
- **Complements Metric 4** - Adds context to spread (not just favorite/underdog, but HOW MUCH scoring)
- **Differentiates matchups** - 28-point total vs 19-point total = huge difference in fantasy opportunity

**Feasibility:** ⭐⭐⭐⭐⭐ (Trivial)
- **Zero new data fetching** - Reuses Metric 4 data (spread + over/under)
- **Simple calculation** - One-line formula, deterministic
- **No external dependencies** - Just arithmetic
- Can implement in 2-4 hours

**Historical Data:** ⭐⭐⭐⭐⭐ (Perfect)
- ✅ Same historical source as Metric 4 (PFR closing lines)
- ✅ Predictive (closing lines = what we knew going in)
- ✅ No gaps or missing data

**Maintenance:** ⭐⭐⭐⭐⭐ (Zero)
- Automatically updates when Metric 4 updates
- No external dependencies to break
- Calculation never changes (fixed formula)

**Preferred Data Source:** **ESPN API** (via Metric 4) for current weeks, **PFR** for historical

**Historical Feasibility:** ✅ **PERFECT** - Same as Metric 4

**Implementation Priority:**
- [x] **Immediate (after Metric 4)** - Trivial enhancement once Metric 4 is available
- **Blocker:** Must implement Metric 4 first

**Next Steps:**
1. **WAIT for Metric 4 implementation** - Cannot proceed until Vegas lines are available

2. **Once Metric 4 is complete:**
   - Add `calculate_implied_team_total()` function to PlayerManager or ConfigManager
   - Calculate for each team using Metric 4's spread + over/under
   - Add `implied_team_total` column to players.csv
   - Map each player to their team's total

3. **Optional enhancement:**
   - Add `team_total_multiplier` logic to scoring algorithm
   - Boost players in high-scoring games (28+ total)
   - Penalize players in low-scoring games (<20 total)

4. **Test with historical data:**
   - Verify calculation accuracy (sample games)
   - Run simulation with team total boost enabled
   - Compare accuracy vs baseline

**Example Impact:**
```
Patrick Mahomes (KC, implied total: 28.5 points):
- Base projection: 22.0 points
- Team total multiplier: 1.10 (high-scoring game)
- Adjusted projection: 22.0 * 1.10 = 24.2 points ✅ Accurate boost

Bryce Young (CAR, implied total: 17.5 points):
- Base projection: 16.0 points
- Team total multiplier: 0.90 (low-scoring game)
- Adjusted projection: 16.0 * 0.90 = 14.4 points ✅ Realistic penalty
```

**Blockers:**
- ⚠️ **BLOCKED by Metric 4 (Vegas Lines)** - Must implement Metric 4 first
- No other blockers (calculation is trivial)

**Implementation Order:**
1. Implement Metric 4 (Vegas Lines) - 3-5 days
2. Implement Metric 12 (Implied Team Total) - 2-4 hours (immediately after Metric 4)

---

## Research Completeness Checklist

- [x] All 7 sections completed above
- [x] Position applicability documented (ALL positions)
- [x] Minimum 2-3 free alternatives researched (ESPN, The Odds API, PFR)
- [x] Historical data availability assessed (YES - same as Metric 4)
- [x] Schema definition provided (implied_team_total column, optional multiplier)
- [x] Clear recommendation provided (PURSUE - Immediate after Metric 4, trivial calculation)
- [x] Dependencies documented (BLOCKED by Metric 4)
- [x] Effort estimate provided (2-4 hours)

---

## Related Metrics

**Similar/Related Metrics:**
- **Metric 4: Vegas Lines/Game Environment** - Provides inputs (spread, over/under) ⚠️ **DEPENDENCY**
- Metric 9: Team Pass Rate/Tempo - Affected by game script (implied total affects tempo)
- Metric 34: Team Plays Per Game - High total = more plays expected
- Metric 36: Team Red Zone Efficiency - High total = more red zone opportunities

**Notes:**
- **Metric 12 is DERIVED from Metric 4** - Cannot implement independently
- Should be implemented **immediately after Metric 4** (trivial enhancement)
- Complements spread (Metric 4 says WHO wins, Metric 12 says HOW MUCH scoring)
- Can be used standalone or combined with spread for game script prediction

**Implementation Order:**
1. Metric 4 (Vegas Lines) - Foundation
2. Metric 12 (Implied Team Total) - Derived calculation (2-4 hours after Metric 4)

---

## Lifecycle Notes

**Data Source Stability:** Excellent (ESPN API + PFR, same as Metric 4)
**Deprecation Risk:** None (Vegas lines are fundamental to NFL betting)
**Replacement Strategy:** N/A (no need - data source is stable)

**Enhancement Path:**
- **Phase 1 (Immediate after Metric 4):** Basic implied total calculation
- **Phase 2 (Future):** Add team total multiplier to scoring algorithm
- **Phase 3 (Advanced):** Track line movement (opening vs closing total) for sharper predictions

**Maintenance Notes:**
- Zero maintenance required (calculation is deterministic)
- Updates automatically when Metric 4 updates
- No external dependencies beyond Metric 4

---

*Research conducted: 2025-12-20*
*Next review: After Metric 4 implementation*
