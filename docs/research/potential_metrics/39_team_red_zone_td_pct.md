# Metric 39: Team Red Zone TD% (K-specific)

**Position Applicability:** K (Kicker)
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data in the `data/` folder?**

- [ ] Yes - Calculate from existing columns
- [x] No - Requires new data source
- [ ] Partial - Some components available

**Details:**

Team Red Zone TD% is **NOT available in existing data**.

**Checked:**
- `data/players.csv` - NO red zone stats
- `data/teams_week_N.csv` - NO red zone stats (only team rankings)
- `data/league_config.json` - Only league settings

**What is Team Red Zone TD%?**

Team Red Zone TD% measures how often a team scores touchdowns (vs field goals) when they reach the red zone (opponent's 20-yard line).

**Formula:**
```
Red Zone TD% = (Red Zone TDs / Red Zone Attempts) × 100

Where:
- Red Zone = Inside opponent's 20-yard line
- Red Zone TDs = Touchdowns scored from red zone possessions
- Red Zone Attempts = Total red zone possessions (TD + FG + turnover)
```

**Kicker Impact (Inverse Relationship):**

**HIGH Red Zone TD% (70%+) = BAD for kicker:**
- Team scores TDs frequently in red zone
- Fewer FG attempts
- Lower kicker fantasy points

**LOW Red Zone TD% (<55%) = GOOD for kicker:**
- Team struggles to score TDs in red zone
- More FG attempts
- Higher kicker fantasy points

**Example:**
```
Baltimore Ravens (2024):
- Red Zone Attempts: 50
- Red Zone TDs: 38
- Red Zone FGs: 10
- Red Zone TD%: 38/50 = 76% (HIGH)
- Kicker Impact: Ravens kicker gets ~10 RZ FG attempts all season ❌ BAD

Chicago Bears (2024):
- Red Zone Attempts: 50
- Red Zone TDs: 25
- Red Zone FGs: 22
- Red Zone TD%: 25/50 = 50% (LOW)
- Kicker Impact: Bears kicker gets ~22 RZ FG attempts ✅ GOOD
```

**Calculation Requirements:**

To calculate, need:
1. **Red Zone Attempts** (team-level)
2. **Red Zone TDs** (team-level)
3. **Kicker → Team mapping** (to assign team RZ TD% to kicker)

**Kicker Scoring Adjustment:**
```python
def get_kicker_rz_multiplier(team_rz_td_pct: float) -> float:
    """
    Calculate kicker scoring multiplier based on team red zone TD%.

    Lower RZ TD% = More FG attempts = Higher multiplier
    Higher RZ TD% = Fewer FG attempts = Lower multiplier
    """
    if team_rz_td_pct >= 70.0:
        return 0.90  # Very efficient red zone = fewer FG attempts
    elif team_rz_td_pct >= 60.0:
        return 0.95  # Good red zone = slightly fewer FG attempts
    elif team_rz_td_pct >= 50.0:
        return 1.00  # Average red zone = neutral
    elif team_rz_td_pct >= 45.0:
        return 1.05  # Poor red zone = more FG attempts
    else:
        return 1.10  # Very poor red zone = many FG attempts
```

**Conclusion:** Cannot calculate from existing data. Need red zone stats from external source.

---

## 2. ESPN API Availability

**Is this metric available via ESPN Fantasy Football API?**

- [ ] Yes - Available directly
- [x] No - Not available in fantasy API
- [ ] Partial - Some components available

**Sources Checked:**
- [x] ESPN Fantasy API (player/team stats)
- [x] ESPN.com NFL Stats (public website)

**API Data:**

ESPN Fantasy API **does NOT provide red zone stats** in the standard player/team endpoints.

**What ESPN Fantasy API Provides:**
- Player stats (receptions, yards, TDs)
- Team defensive rankings
- Basic team stats (total points, yards)

**What ESPN Fantasy API Does NOT Provide:**
- Red zone attempts
- Red zone touchdowns
- Red zone field goal attempts
- Red zone efficiency

**ESPN.com Public Stats:**

ESPN's public NFL website **does show red zone stats**, but NOT via the Fantasy API:
- URL: `https://www.espn.com/nfl/stats/team/_/view/redzone`
- Format: HTML tables (would require scraping)
- Data: Red zone attempts, TDs, FG attempts, TD%

**Conclusion:** ESPN Fantasy API does not provide red zone stats. Would need to scrape ESPN.com public stats page OR use alternative source.

---

## 3. Free Alternative Sources

**What free data sources provide this metric?**

### Source 1: Pro Football Reference (Team Red Zone Stats)

- URL: `https://www.pro-football-reference.com/years/2024/`
- Data format: HTML tables (scraping required)
- Update frequency: Weekly
- Free tier limits: Unlimited (public website)
- Authentication: Not required
- Data quality: **Excellent** - Official NFL stats

**Details:**
- PFR provides team red zone stats on team pages
- Shows: Red zone attempts, TDs, TD%, success rate
- Historical data: ✅ Available (all past seasons)
- **Limitation:** Must scrape (no official API)

**Example URL:**
```
https://www.pro-football-reference.com/teams/rav/2024.htm
(Scroll to "Scoring" section → Red Zone stats)
```

**Expected Data:**
```
Team: Baltimore Ravens
Red Zone Attempts: 50
Red Zone TDs: 38
Red Zone TD%: 76.0%
Red Zone FGs: 10
```

### Source 2: TeamRankings.com (Direct Red Zone TD%)

- URL: `https://www.teamrankings.com/nfl/stat/red-zone-scoring-pct`
- Data format: HTML tables (scraping required)
- Update frequency: Daily
- Free tier limits: Unlimited (public website)
- Authentication: Not required
- Data quality: **Excellent** - Aggregated from official stats

**Details:**
- TeamRankings shows red zone TD% for all 32 teams
- Sortable table with ranks
- Shows season-to-date cumulative RZ TD%
- Historical data: ✅ Available (past seasons)
- **Advantage:** Single page with all teams (easier to scrape)

**Example Data Table:**
```
Rank | Team | Red Zone TD% | Red Zone Attempts | Red Zone TDs
1    | BAL  | 76.0%        | 50                | 38
2    | KC   | 72.0%        | 48                | 35
...
32   | CHI  | 50.0%        | 50                | 25
```

### Source 3: NFL.com Stats (Official Source)

- URL: `https://www.nfl.com/stats/team-stats/offense/red-zone-efficiency/2024/REG/all`
- Data format: HTML tables (scraping required)
- Update frequency: Real-time
- Free tier limits: Unlimited (public website)
- Authentication: Not required
- Data quality: **Excellent** - Official NFL stats

**Details:**
- NFL.com provides official red zone efficiency stats
- Shows: Red zone attempts, TDs, TD%, FG attempts
- Most authoritative source (official NFL)
- Historical data: ✅ Available
- **Limitation:** Scraping required (no public API)

### Source 4: ESPN.com Stats Page (Public Website)

- URL: `https://www.espn.com/nfl/stats/team/_/view/redzone`
- Data format: HTML tables (scraping required)
- Update frequency: Daily
- Free tier limits: Unlimited (public website)
- Authentication: Not required
- Data quality: **Very High**

**Details:**
- ESPN public stats (NOT the Fantasy API)
- Shows red zone efficiency for all teams
- Clean table format
- Historical data: ✅ Available (past seasons)

**Comparison:**

| Source | Red Zone TD% | All Teams | Historical | Free Tier | Ease of Use |
|--------|-------------|-----------|------------|-----------|-------------|
| Pro Football Reference | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Unlimited | Medium (scraping, team pages) |
| TeamRankings.com | ✅ Yes | ✅ Yes (1 page) | ✅ Yes | ✅ Unlimited | High (single page scrape) |
| NFL.com Stats | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Unlimited | Medium (scraping) |
| ESPN.com Stats | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Unlimited | Medium (scraping) |

**Recommended Source:** **TeamRankings.com** (single page with all teams, easy to scrape)

**Alternative:** **Pro Football Reference** (most comprehensive, but requires per-team scraping)

---

## 4. Data Quality Assessment

**Reliability:** High
**Accuracy:** Very High
**Update Frequency:** Weekly

**Details:**

**Reliability Assessment:**
- Source stability: TeamRankings.com is stable, consistent format
- NFL.com is official source (most reliable)
- Historical uptime: All sources have excellent track records

**Accuracy Assessment:**
- Methodology: Red zone TD% is official NFL stat (no ambiguity)
- All sources pull from official NFL data
- No known discrepancies between sources
- Calculation is simple: TDs / Attempts

**Update Frequency:**
- TeamRankings: Updates daily (sometimes within hours post-game)
- NFL.com: Updates real-time
- Pro Football Reference: Updates within 24 hours
- ESPN.com: Updates daily

**Known Limitations:**

1. **Small sample size early in season:**
```python
# Week 2: Only 4 red zone attempts
# Red Zone TD% = 3/4 = 75% (may not be representative)
# Need minimum 10-15 attempts for stable metric
```

2. **Doesn't account for quality of red zone possessions:**
```python
# Team A: 10 RZ attempts from the 5-yard line (easy TDs)
# Team B: 10 RZ attempts from the 20-yard line (harder TDs)
# Both have same RZ TD%, but Team B's low % more predictive of future FG attempts
```

3. **Turnover-heavy teams skew metric:**
```python
# Team fumbles on 1-yard line (no TD, no FG)
# Reduces RZ TD% but doesn't help kicker
```

**Edge Cases:**

**Very Low Sample (Early Season):**
```python
# Week 1: Team has only 2 red zone trips
# RZ TD%: 1/2 = 50%
# Not stable - need to wait until week 4+ (10+ attempts)

# Solution: Use previous season RZ TD% until current season sample is large enough
if current_season_rz_attempts < 10:
    use_previous_season_rz_td_pct()
else:
    use_current_season_rz_td_pct()
```

**Extreme Efficiency (Outliers):**
```python
# Team with 95% RZ TD% (extremely rare)
# Kicker gets almost no FG attempts
# Apply maximum penalty: 0.85x multiplier

# Team with 30% RZ TD% (very poor offense)
# Kicker gets many FG attempts
# Apply maximum boost: 1.15x multiplier
```

**Validation:**
- Correlate team RZ TD% with kicker fantasy points (should be negative correlation)
- Teams with low RZ TD% should have kickers scoring more fantasy points
- Expected correlation: r = -0.5 to -0.7

---

## 5. Historical Data Availability ⚠️ CRITICAL

**Can we obtain weekly snapshots for simulation validation?**

- [x] Yes - Historical data available

**Historical Data Details:**

**Seasons Available:**
- [x] 2021 season - ✅ Via TeamRankings, PFR, NFL.com
- [x] 2022 season - ✅ Via TeamRankings, PFR, NFL.com
- [x] 2024 season - ✅ Via TeamRankings, PFR, NFL.com
- [x] 2023 season - ✅ Available if needed

**Weekly Snapshot Verification:**

Red Zone TD% is **cumulative stat** (season-to-date):
- Week 5 RZ TD% = (Weeks 1-5 TDs) / (Weeks 1-5 Attempts)
- This is predictive for week 6+ projections

**Data Timing (Predictive vs Retrospective):**
- [x] Represents "what we knew going INTO that week" ✅ **YES** (cumulative through week N-1)

**Verification:**
```
Week 5 simulation requires:
- Weeks 1-4 cumulative RZ TD%
- Apply to week 5 kicker projection

Example:
Team through Week 4:
- RZ Attempts: 12
- RZ TDs: 8
- RZ TD%: 8/12 = 66.7%
- Kicker adjustment for Week 5: 0.95x (slightly fewer FG attempts expected)
```

**Historical Acquisition Process:**

**Option 1: Scrape TeamRankings (Recommended)**

```python
def scrape_teamrankings_rz_td_pct(year: int, week: int) -> pd.DataFrame:
    """
    Scrape TeamRankings for cumulative red zone TD% through a given week.

    Returns DataFrame with columns:
    - team, rz_attempts, rz_tds, rz_td_pct
    """
    url = f"https://www.teamrankings.com/nfl/stat/red-zone-scoring-pct?date={year}-{week}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse table
    # Expected columns: Rank, Team, RZ TD%, RZ Attempts, RZ TDs

    return parsed_df
```

**Option 2: Scrape Pro Football Reference**

```python
def scrape_pfr_team_rz_stats(year: int, team_code: str) -> dict:
    """
    Scrape PFR team page for red zone stats.

    Returns dict:
    {
        'rz_attempts': 50,
        'rz_tds': 38,
        'rz_td_pct': 76.0
    }
    """
    url = f"https://www.pro-football-reference.com/teams/{team_code}/{year}.htm"
    # Scraping logic to extract red zone section
    pass
```

**sim_data Integration:**

**Where does this metric fit?**
- [x] Team-level: Create team stats file OR add to existing team files
- [x] Player-level: Map kicker to team's RZ TD%

**Schema Definition:**

**Option 1: Team-level file**
- File: `simulation/sim_data/{YEAR}/weeks/week_{NN}/team_rz_stats.csv`
- Columns:
  - `team` (str): Team code (BAL, KC, etc.)
  - `rz_attempts` (int): Cumulative red zone attempts
  - `rz_tds` (int): Cumulative red zone TDs
  - `rz_td_pct` (float): RZ TD percentage (0-100)
  - `kicker_multiplier` (float): Adjustment for kicker (0.90-1.10)

**Option 2: Player-level (kicker column)**
- File: `simulation/sim_data/{YEAR}/weeks/week_{NN}/players.csv`
- New column: `team_rz_td_pct` (float) - For kickers only
- New column: `rz_td_multiplier` (float) - Kicker scoring adjustment

**Recommended:** **Option 2 (player-level column)** - Simpler integration

**Calculation Timing:**
```python
# For week 5 simulation:
# 1. Load cumulative RZ stats from weeks 1-4
rz_stats_weeks_1_4 = scrape_teamrankings_rz_td_pct(2024, week=4)

# 2. Map each kicker to their team's RZ TD%
kickers = players[players['position'] == 'K']
kickers = kickers.merge(rz_stats_weeks_1_4, on='team')

# 3. Calculate kicker multiplier
kickers['rz_td_multiplier'] = kickers['rz_td_pct'].apply(get_kicker_rz_multiplier)

# 4. Apply to week 5 kicker projections
kickers['adjusted_projection'] = kickers['base_projection'] * kickers['rz_td_multiplier']
```

**Historical Data Acquisition:**
- [x] Available from TeamRankings (easiest - single page)
- [x] Available from Pro Football Reference (per-team scraping)
- [x] Available from NFL.com (official source)

**Timeline:** 1-2 days (scraping implementation)

---

## 6. Implementation Complexity

**Difficulty:** Easy-Medium
**Estimated Effort:** 1-2 days

**Breakdown:**

**Data Fetching:**
- Complexity: **Easy-Medium** (scraping required, but simple table)
- Pattern to follow: Similar to other scraping (Metric 1, 4, 21)
- Required packages: `requests`, `beautifulsoup4`, `pandas`
- Authentication: Not required
- Rate limiting handling: Respectful delays (2 seconds between requests)

**Scraping Implementation:**
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_team_rz_td_pct(year: int) -> pd.DataFrame:
    """
    Fetch team red zone TD% from TeamRankings.

    Returns DataFrame with all 32 teams:
    - team, rz_attempts, rz_tds, rz_td_pct
    """
    url = f"https://www.teamrankings.com/nfl/stat/red-zone-scoring-pct"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    time.sleep(2)  # Respectful rate limiting

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find table with red zone stats
    table = soup.find('table', class_='datatable')

    # Parse rows
    teams_data = []
    for row in table.find_all('tr')[1:]:  # Skip header
        cols = row.find_all('td')
        if len(cols) >= 4:
            team = cols[1].text.strip()
            rz_td_pct = float(cols[2].text.strip('%'))
            # Additional columns: attempts, TDs (if available)

            teams_data.append({
                'team': team,
                'rz_td_pct': rz_td_pct
            })

    return pd.DataFrame(teams_data)
```

**Data Processing:**
- Complexity: **Very Easy**
- Calculations required:
  1. Scrape team RZ TD% (one value per team)
  2. Map kicker to team
  3. Apply multiplier formula
- Data transformations:
  - Team code normalization (TeamRankings uses full names, need abbreviations)
  - Convert RZ TD% to kicker multiplier

**Team Code Mapping:**
```python
# TeamRankings uses full names: "Baltimore Ravens"
# Need to convert to team codes: "BAL"

team_name_to_code = {
    'Baltimore Ravens': 'BAL',
    'Kansas City Chiefs': 'KC',
    'Chicago Bears': 'CHI',
    # ... all 32 teams
}

rz_stats['team_code'] = rz_stats['team'].map(team_name_to_code)
```

**Multiplier Calculation:**
```python
def calculate_kicker_multiplier(rz_stats: pd.DataFrame) -> pd.DataFrame:
    """
    Add kicker multiplier column based on RZ TD%.
    """
    def get_multiplier(rz_td_pct: float) -> float:
        if rz_td_pct >= 70.0:
            return 0.90  # Very efficient RZ = fewer FG attempts
        elif rz_td_pct >= 60.0:
            return 0.95
        elif rz_td_pct >= 50.0:
            return 1.00  # Average
        elif rz_td_pct >= 45.0:
            return 1.05
        else:
            return 1.10  # Poor RZ = many FG attempts

    rz_stats['kicker_multiplier'] = rz_stats['rz_td_pct'].apply(get_multiplier)
    return rz_stats
```

**Schema Integration:**
- New columns to add: `team_rz_td_pct` (float), `rz_td_multiplier` (float) - Kickers only
- Existing columns required: `team` (to map kicker to team)
- Data type compatibility: float columns (compatible)
- Backward compatibility: No impact (new columns)

**Dependencies:**

**Metric Dependencies:**
- [ ] No dependencies on other metrics

**Code Dependencies:**
- File: `util/PlayerManager.py` (kicker scoring adjustment)
- Purpose: Apply RZ TD multiplier to kicker scores
- Integration point: After base kicker projection, apply multiplier

**External Dependencies:**
- Package: `beautifulsoup4` (scraping)
- Package: `requests` (HTTP)

**Cost Estimate:**
- Paid tier required: No
- Monthly cost: $0 (all sources free)

**Quick Win?**
- [x] Yes (if only need current season) - 1 day scraping implementation
- [ ] No (if need historical) - 1-2 days (scraping + historical fetch)

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High value for kickers, easy implementation

**Rationale:**

**Value:** ⭐⭐⭐⭐ (High for kickers)
- **Critical for kicker accuracy** - RZ TD% inversely correlates with kicker fantasy points
- **Differentiates kickers** - Two kickers on equal offenses can have different value
- **Simple but effective** - One metric captures kicker opportunity
- **Complements team scoring** - Team can score a lot but still be poor in RZ (good for kicker)

**Feasibility:** ⭐⭐⭐⭐ (Easy)
- **Simple scraping** - Single page with all teams (TeamRankings)
- **No complex calculations** - Just team stat lookup + mapping
- **Low maintenance** - Scraping one table is straightforward
- 1-2 days implementation

**Historical Data:** ⭐⭐⭐⭐⭐ (Perfect)
- ✅ Available from multiple sources (TeamRankings, PFR, NFL.com)
- ✅ Predictive (cumulative RZ TD% through week N predicts week N+1)
- ✅ No gaps or missing data

**Maintenance:** ⭐⭐⭐⭐ (Low)
- **Scraping stability:** TeamRankings table format is consistent
- **Fallback sources:** Multiple alternatives if one breaks
- **Data stability:** Official NFL stat (won't change)

**Preferred Data Source:** **TeamRankings.com** (single page, all teams, easy to scrape)

**Alternative:** **Pro Football Reference** (more comprehensive, but per-team scraping)

**Historical Feasibility:** ✅ **PERFECT** - Available for all past seasons

**Implementation Priority:**
- [x] **Medium-High (after basic metrics)** - Important for kicker accuracy, easy to implement

**Next Steps:**

1. **Scrape TeamRankings for team RZ TD%**
   - URL: `https://www.teamrankings.com/nfl/stat/red-zone-scoring-pct`
   - Extract: Team, RZ TD%, RZ Attempts, RZ TDs
   - Timeline: 1 day

2. **Create team name → team code mapping**
   - TeamRankings uses full names ("Baltimore Ravens")
   - Convert to team codes ("BAL")
   - Store in mapping dict

3. **Calculate kicker multiplier**
   - Apply formula: Low RZ TD% = High multiplier (more FG attempts)
   - Range: 0.90x (70%+ RZ TD%) to 1.10x (<45% RZ TD%)

4. **Map kickers to team RZ TD%**
   - Load kickers from players.csv
   - Merge with team RZ TD% based on team code
   - Apply multiplier to kicker projections

5. **Test with historical data**
   - Run simulation with RZ TD multiplier enabled
   - Validate that kickers on low RZ TD% teams score higher
   - Compare accuracy vs baseline

**Example Impact:**
```
Justin Tucker (BAL, RZ TD%: 76%):
- Base projection: 9.0 points
- RZ TD multiplier: 0.90 (efficient RZ = fewer FG attempts)
- Adjusted projection: 9.0 × 0.90 = 8.1 points ✅ More realistic

Cairo Santos (CHI, RZ TD%: 50%):
- Base projection: 8.0 points
- RZ TD multiplier: 1.00 (average RZ)
- Adjusted projection: 8.0 × 1.00 = 8.0 points (no change)

Bears new kicker (RZ TD%: 45%):
- Base projection: 7.5 points
- RZ TD multiplier: 1.05 (poor RZ = more FG attempts)
- Adjusted projection: 7.5 × 1.05 = 7.875 points ✅ Accounts for volume
```

**Blockers:** None

**Timeline:** 1-2 days (scraping implementation + testing)

---

## Research Completeness Checklist

- [x] All 7 sections completed above
- [x] Position applicability documented (K - Kicker)
- [x] Minimum 2-3 free alternatives researched (TeamRankings, PFR, NFL.com)
- [x] Historical data availability assessed (YES - perfect)
- [x] Schema definition provided (team_rz_td_pct, rz_td_multiplier columns)
- [x] Clear recommendation provided (PURSUE - Easy implementation, high value for kickers)
- [x] Dependencies documented (None)
- [x] Effort estimate provided (1-2 days)

---

## Related Metrics

**Similar/Related Metrics:**
- Metric 36: Team Red Zone Efficiency (ALL positions) - Similar concept, broader application
- Metric 40: Kicker Accuracy by Distance - Complementary kicker metric
- Metric 4: Vegas Lines - Predicts total team scoring (complements RZ TD%)

**Notes:**
- **RZ TD% is kicker-specific inverse metric** - Low RZ TD% = Good for kicker
- Complements team scoring metrics (team can score a lot but be inefficient in RZ)
- Simple team-level stat that significantly improves kicker projections
- Should be implemented for all kicker projections

**Implementation Order:**
- **Standalone** - No dependencies, can implement immediately

---

## Lifecycle Notes

**Data Source Stability:** High (TeamRankings stable, multiple fallback sources)
**Deprecation Risk:** None (official NFL stat, won't disappear)
**Replacement Strategy:** Primary: TeamRankings, Fallback: PFR or NFL.com

**Enhancement Path:**
- **Phase 1 (Immediate):** Scrape TeamRankings for season-to-date RZ TD%
- **Phase 2:** Add historical RZ TD% for better early-season projections
- **Phase 3 (Future):** Track RZ TD% trends (improving vs declining)

**Maintenance Notes:**
- **Scraping stability:** TeamRankings table format is consistent year-to-year
- **Fallback plan:** If TeamRankings scraping breaks, switch to PFR or NFL.com
- **Validation:** Correlate kicker fantasy points with team RZ TD% (should be negative)

---

*Research conducted: 2025-12-20*
*Next review: After implementation and validation*
