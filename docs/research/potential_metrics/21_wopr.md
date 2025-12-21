# Metric 21: WOPR (Weighted Opportunity Rating)

**Position Applicability:** WR, TE
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data in the `data/` folder?**

- [ ] Yes - Calculate from existing columns
- [x] No - Requires new data source
- [ ] Partial - Some components available

**Details:**

WOPR is **calculated from targets and air yards**, which are NOT currently in existing data.

**Checked:**
- `data/players.csv` - NO targets or air_yards columns
- Would need both metrics to calculate WOPR

**WOPR Formula:**
```
WOPR = (1.5 × Target Share) + (0.7 × Air Yards Share)

Where:
- Target Share = Player Targets / Team Total Targets
- Air Yards Share = Player Air Yards / Team Total Air Yards
```

**Dependencies:**
- **Metric 1: Target Volume/Share** - Provides targets (HIGH priority, already researched)
- **Metric 13: Air Yards (aDOT)** - Provides air yards (MEDIUM priority, not yet researched)

**Calculation Logic:**
```python
def calculate_wopr(player_targets: int, team_targets: int,
                   player_air_yards: int, team_air_yards: int) -> float:
    """
    Calculate WOPR (Weighted Opportunity Rating).

    Args:
        player_targets: Player's target count
        team_targets: Team's total targets
        player_air_yards: Player's air yards
        team_air_yards: Team's total air yards

    Returns:
        WOPR score (0.0-1.0 range, higher = more opportunity)

    Example:
        >>> calculate_wopr(10, 35, 150, 400)
        0.692  # 69.2% WOPR (elite opportunity)
    """
    target_share = player_targets / team_targets if team_targets > 0 else 0
    air_yards_share = player_air_yards / team_air_yards if team_air_yards > 0 else 0

    wopr = (1.5 * target_share) + (0.7 * air_yards_share)

    return wopr
```

**Team Aggregation Required:**
```python
# Step 1: Aggregate team totals
team_stats = players.groupby('team').agg({
    'targets': 'sum',
    'air_yards': 'sum'
})

# Step 2: Calculate WOPR for each player
for player in players[players['position'].isin(['WR', 'TE'])]:
    team = player['team']
    team_targets = team_stats.loc[team, 'targets']
    team_air_yards = team_stats.loc[team, 'air_yards']

    player['wopr'] = calculate_wopr(
        player['targets'],
        team_targets,
        player['air_yards'],
        team_air_yards
    )
```

**WOPR Interpretation:**
```
Elite Opportunity:   WOPR > 0.50 (50%)
Good Opportunity:    WOPR 0.40-0.50 (40-50%)
Solid Opportunity:   WOPR 0.30-0.40 (30-40%)
Limited Opportunity: WOPR 0.20-0.30 (20-30%)
Minimal Opportunity: WOPR < 0.20 (<20%)
```

**Example Calculations:**
```
Tyreek Hill (MIA) - Elite WR1:
- Targets: 10 / 35 team = 28.6% target share
- Air Yards: 150 / 400 team = 37.5% air yards share
- WOPR = (1.5 × 0.286) + (0.7 × 0.375) = 0.692 (69.2%) ✅ Elite

Jaylen Waddle (MIA) - WR2:
- Targets: 8 / 35 team = 22.9% target share
- Air Yards: 80 / 400 team = 20.0% air yards share
- WOPR = (1.5 × 0.229) + (0.7 × 0.200) = 0.484 (48.4%) ✅ Good

WR3/Flex Player:
- Targets: 4 / 35 team = 11.4% target share
- Air Yards: 50 / 400 team = 12.5% air yards share
- WOPR = (1.5 × 0.114) + (0.7 × 0.125) = 0.259 (25.9%) ⚠️ Limited
```

**Conclusion:** Cannot calculate from existing data. Requires Metric 1 (Targets) AND Metric 13 (Air Yards) implementation first.

---

## 2. ESPN API Availability

**Is this metric available via ESPN Fantasy Football API?**

- [ ] Yes - Available directly
- [ ] No - Not available
- [x] Partial - Components available separately

**Sources Checked:**
- [x] ESPN API research from Metric 1 (Targets - available)
- [x] ESPN Player Stats endpoint (checking for air yards)

**API Data:**

WOPR is **not directly provided** by ESPN API, but components may be available:

**Component 1: Targets (from Metric 1 research)**
- Available: ✅ YES (via ESPN stats array)
- Stat ID: Need to identify in stats array
- Source: `ESPN Player Data API`

**Component 2: Air Yards**
- Available: ❌ **NOT in standard ESPN API**
- ESPN does not provide air yards in fantasy API
- Would need ESPN's Next Gen Stats integration (if exists)

**ESPN API Limitations:**

From ESPN Player Data API documentation, the `stats` array includes:
- `rec` (receptions)
- `recTds` (receiving TDs)
- `recYds` (receiving yards)
- `recTar` (targets) ✅ Available

But **NOT**:
- Air yards
- Average depth of target (aDOT)
- Air yards share

**Conclusion:** ESPN API provides targets but NOT air yards. WOPR cannot be calculated from ESPN alone.

---

## 3. Free Alternative Sources

**What free data sources provide this metric?**

### Source 1: PlayerProfiler.com (Direct WOPR)

- URL: `https://www.playerprofiler.com/nfl/`
- Data format: HTML tables (scraping required)
- Update frequency: Weekly
- Free tier limits: Unlimited (public website)
- Authentication: Not required
- Data quality: **Excellent** - Calculates WOPR directly

**Details:**
- PlayerProfiler shows WOPR for all WR/TE
- Uses standard formula: (1.5 × Target Share) + (0.7 × Air Yards Share)
- Historical data: ✅ Available (past seasons)
- **Limitation:** Must scrape (no official free API)

**Example Data:**
```
Player: Tyreek Hill
Position: WR
Team: MIA
WOPR: 0.692 (69.2%)
Target Share: 28.6%
Air Yards Share: 37.5%
```

### Source 2: Pro Football Reference (Calculate from Components)

- URL: `https://www.pro-football-reference.com/years/2024/receiving.htm`
- Data format: HTML tables
- Update frequency: Weekly
- Free tier limits: Unlimited
- Authentication: Not required
- Data quality: **Very High** - Official stats

**Details:**
- Provides targets (✅)
- Provides receiving yards, receptions
- **Does NOT provide air yards** ❌
- Can calculate target share, but not WOPR

**Limitation:** Missing air yards component

### Source 3: Next Gen Stats (Air Yards Available)

- URL: `https://nextgenstats.nfl.com/stats/receiving`
- Data format: HTML tables / JSON (some endpoints)
- Update frequency: Weekly
- Free tier limits: Unlimited (public website)
- Authentication: Not required
- Data quality: **Excellent** - Official NFL tracking

**Details:**
- Provides average cushion, separation, catch %
- Provides completion percentage
- **Provides air yards!** ✅ (Avg Intended Air Yards stat)
- Provides targets ✅
- Can calculate WOPR from Next Gen Stats data

**API Availability:**
- No official public API
- Must scrape HTML tables
- Data structure: Fairly consistent, scrapable

**Example Scraping:**
```python
import requests
from bs4 import BeautifulSoup

url = "https://nextgenstats.nfl.com/stats/receiving/2024/REG"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Parse table for:
# - Player name
# - Targets
# - Avg Intended Air Yards (multiply by targets = total air yards)
# - Calculate target share and air yards share
# - Calculate WOPR
```

### Source 4: Sleeper API (Partial - Targets Only)

- URL: `https://docs.sleeper.com/`
- Data format: JSON API
- Update frequency: Weekly
- Free tier limits: Unlimited
- Authentication: Not required
- Data quality: **High**

**Details:**
- Provides targets ✅
- Provides receiving stats (yards, TDs, receptions)
- **Does NOT provide air yards** ❌
- Cannot calculate WOPR from Sleeper alone

**Comparison:**

| Source | WOPR Direct | Targets | Air Yards | Historical | Free Tier | Ease of Use |
|--------|------------|---------|-----------|------------|-----------|-------------|
| PlayerProfiler | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Unlimited | Medium (scraping) |
| Pro Football Reference | ❌ No | ✅ Yes | ❌ No | ✅ Yes | ✅ Unlimited | Medium (scraping) |
| Next Gen Stats | ⚠️ Calculate | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Unlimited | Medium (scraping) |
| Sleeper API | ❌ No | ✅ Yes | ❌ No | ✅ Yes | ✅ Unlimited | High (API) |
| ESPN API | ❌ No | ✅ Yes | ❌ No | ⚠️ Future only | ✅ Unlimited | High (API) |

**Recommended Source:** **Next Gen Stats** (provides both targets and air yards, official NFL data)

**Alternative:** **PlayerProfiler** (provides WOPR directly, but scraping required)

---

## 4. Data Quality Assessment

**Reliability:** High
**Accuracy:** Very High
**Update Frequency:** Weekly

**Details:**

**Reliability Assessment:**
- Source stability: Next Gen Stats is official NFL (very stable)
- PlayerProfiler: Community site (stable but not official)
- Historical uptime: Both have excellent track records

**Accuracy Assessment:**
- Methodology: WOPR is well-established fantasy metric
- Formula is standardized: (1.5 × TS) + (0.7 × AYS)
- Next Gen Stats uses official NFL tracking data
- Known issues: Air yards can vary by source (some use intended, some use actual)

**Update Frequency:**
- Next Gen Stats: Updates within 24 hours post-game
- PlayerProfiler: Updates within 48 hours
- Historical data: Both maintain multi-season archives

**Known Limitations:**

1. **Target distribution variance** - Game-to-game volatility high
2. **Air yards vs actual yards** - Air yards measure opportunity, not production
3. **Game script dependency** - Blowouts skew WOPR (garbage time targets)
4. **Team pace** - High-tempo teams inflate raw numbers (need shares, not totals)

**Edge Cases:**

**Low-Target Games:**
```python
# Player with 1 target out of 20 team targets
target_share = 1 / 20 = 0.05
air_yards_share = 15 / 300 = 0.05
wopr = (1.5 × 0.05) + (0.7 × 0.05) = 0.11 (11%) ⚠️ Very low

# Handle: Set minimum threshold (WOPR < 15% = "too few targets to evaluate")
```

**Missing Air Yards:**
```python
# If air yards data unavailable for a player
if pd.isna(player['air_yards']):
    # Option 1: Skip WOPR calculation (set to NULL)
    player['wopr'] = None

    # Option 2: Use target share only (degraded calculation)
    player['wopr'] = 1.5 * player['target_share']  # Less accurate
```

**TE vs WR Differences:**
```python
# TEs typically have lower air yards (shorter routes)
# May want position-specific WOPR thresholds:
wr_elite_wopr = 0.50  # 50%+
te_elite_wopr = 0.40  # 40%+ (lower due to shorter routes)
```

**Validation:**
- Cross-reference WOPR with fantasy points scored
- High WOPR players should score more fantasy points (strong correlation)
- Players with high WOPR but low fantasy points = efficiency issues (drops, poor QB)

---

## 5. Historical Data Availability ⚠️ CRITICAL

**Can we obtain weekly snapshots for simulation validation?**

- [x] Yes - Historical data available (with caveats)

**Historical Data Details:**

**Seasons Available:**
- [x] 2021 season - ✅ Via Next Gen Stats + PlayerProfiler
- [x] 2022 season - ✅ Via Next Gen Stats + PlayerProfiler
- [x] 2024 season - ✅ Via Next Gen Stats + PlayerProfiler
- [x] 2023 season - ✅ Available if needed

**Weekly Snapshot Verification:**

WOPR depends on **cumulative stats through that week**:
- Targets: Cumulative through week N
- Air Yards: Cumulative through week N
- Team totals: Cumulative through week N

**Data Timing (Predictive vs Retrospective):**
- [x] Represents "what we knew going INTO that week" ✅ **YES** (if using weeks 1-N data for week N+1)

**Verification:**
```
Week 5 simulation requires:
- Weeks 1-4 targets: Sum player targets weeks 1-4
- Weeks 1-4 air yards: Sum player air yards weeks 1-4
- Calculate WOPR from weeks 1-4 cumulative
- Apply WOPR to week 5 projection

This is PREDICTIVE (using past 4 weeks to predict week 5)
```

**Historical Acquisition Process:**

**Option 1: Scrape Next Gen Stats (Preferred)**

```python
def scrape_ngs_air_yards(year: int, week: int) -> pd.DataFrame:
    """
    Scrape Next Gen Stats for cumulative targets and air yards.

    Returns DataFrame with columns:
    - player_name, team, position, targets, avg_air_yards, total_air_yards
    """
    url = f"https://nextgenstats.nfl.com/stats/receiving/{year}/REG/{week}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse table (structure inspection needed)
    # Extract: player, targets, avg_intended_air_yards
    # Calculate: total_air_yards = avg_air_yards × targets

    return df
```

**Option 2: Scrape PlayerProfiler (Direct WOPR)**

```python
def scrape_playerprofiler_wopr(year: int) -> pd.DataFrame:
    """
    Scrape PlayerProfiler for direct WOPR values.

    Returns DataFrame with columns:
    - player_name, team, position, wopr, target_share, air_yards_share
    """
    url = f"https://www.playerprofiler.com/nfl/{year}/"
    # Scraping logic
    pass
```

**Option 3: Calculate from Metric 1 + Metric 13 (When Available)**

```python
def calculate_historical_wopr(targets_df: pd.DataFrame,
                               air_yards_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate WOPR from Metric 1 (Targets) and Metric 13 (Air Yards) data.
    """
    # Merge targets and air yards
    merged = targets_df.merge(air_yards_df, on=['player', 'week'])

    # Aggregate team totals
    team_totals = merged.groupby(['team', 'week']).agg({
        'targets': 'sum',
        'air_yards': 'sum'
    })

    # Calculate WOPR
    merged['target_share'] = merged['targets'] / merged.groupby('team')['targets'].transform('sum')
    merged['air_yards_share'] = merged['air_yards'] / merged.groupby('team')['air_yards'].transform('sum')
    merged['wopr'] = (1.5 * merged['target_share']) + (0.7 * merged['air_yards_share'])

    return merged[['player', 'week', 'wopr']]
```

**sim_data Integration:**

**Where does this metric fit?**
- [x] Player-level: Add column to `players.csv` (wopr score for WR/TE)

**Schema Definition:**

**Player-level column:**
- File: `simulation/sim_data/{YEAR}/weeks/week_{NN}/players.csv`
- New column: `wopr` (float)
- Data type: `float` (0.0-1.0 range)
- Null handling: NULL for non-WR/TE positions, 0.0 for WR/TE with insufficient data
- Example values: `0.692` (elite), `0.350` (solid), `0.150` (limited)

**Calculation Timing:**
```python
# For week 5 simulation:
# 1. Load cumulative stats from weeks 1-4
targets_weeks_1_4 = load_targets(weeks=[1, 2, 3, 4])
air_yards_weeks_1_4 = load_air_yards(weeks=[1, 2, 3, 4])

# 2. Calculate WOPR from cumulative data
wopr_week_5 = calculate_wopr(targets_weeks_1_4, air_yards_weeks_1_4)

# 3. Apply to week 5 player projections
players_week_5['wopr'] = wopr_week_5
```

**Historical Data Acquisition:**
- [x] Available from Next Gen Stats (scraping required)
- [x] Available from PlayerProfiler (direct WOPR)
- [x] Can calculate from Metrics 1 + 13 (when implemented)

**Timeline:**
- Immediate: If using PlayerProfiler (direct WOPR scraping)
- After Metrics 1 + 13: If calculating from components

---

## 6. Implementation Complexity

**Difficulty:** Medium
**Estimated Effort:** 1-2 days (depends on air yards source)

**Breakdown:**

**Data Fetching:**
- Complexity: **Medium** (requires scraping Next Gen Stats OR PlayerProfiler)
- Pattern to follow: Similar to PFR scraping (Metric 1, 4)
- Required packages: `requests`, `beautifulsoup4`, `pandas`
- Authentication: Not required
- Rate limiting handling: Respectful delays (1-2 seconds between requests)

**Option 1: Scrape Next Gen Stats**
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_ngs_receiving_stats(year: int, week: int) -> pd.DataFrame:
    """
    Fetch receiving stats from Next Gen Stats.
    """
    url = f"https://nextgenstats.nfl.com/stats/receiving/{year}/REG/{week}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    time.sleep(2)  # Respectful rate limiting

    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse table (inspect HTML structure first)
    # Expected columns: Player, Team, Targets, Avg Intended Air Yards

    return parsed_df
```

**Option 2: Scrape PlayerProfiler**
```python
def fetch_playerprofiler_wopr(year: int) -> pd.DataFrame:
    """
    Fetch WOPR directly from PlayerProfiler.
    """
    url = f"https://www.playerprofiler.com/nfl/{year}/"
    # Scraping logic
    pass
```

**Data Processing:**
- Complexity: **Easy** (once data fetched)
- Calculations required:
  1. Calculate team target totals
  2. Calculate team air yards totals
  3. Calculate target share for each player
  4. Calculate air yards share for each player
  5. Apply WOPR formula: (1.5 × TS) + (0.7 × AYS)
- Data transformations:
  - Group by team to get totals
  - Divide player stats by team stats for shares
  - Handle NULL/missing air yards

**Calculation Example:**
```python
def add_wopr_to_players(players: pd.DataFrame) -> pd.DataFrame:
    """
    Add WOPR column to players DataFrame.

    Requires players to have: targets, air_yards, team columns
    """
    # Filter to WR/TE only
    pass_catchers = players[players['position'].isin(['WR', 'TE'])].copy()

    # Calculate team totals
    team_totals = pass_catchers.groupby('team').agg({
        'targets': 'sum',
        'air_yards': 'sum'
    }).reset_index()
    team_totals.columns = ['team', 'team_targets', 'team_air_yards']

    # Merge team totals back to players
    pass_catchers = pass_catchers.merge(team_totals, on='team')

    # Calculate shares
    pass_catchers['target_share'] = pass_catchers['targets'] / pass_catchers['team_targets']
    pass_catchers['air_yards_share'] = pass_catchers['air_yards'] / pass_catchers['team_air_yards']

    # Calculate WOPR
    pass_catchers['wopr'] = (1.5 * pass_catchers['target_share']) + \
                             (0.7 * pass_catchers['air_yards_share'])

    # Merge back to full players DataFrame
    players = players.merge(
        pass_catchers[['player_id', 'wopr']],
        on='player_id',
        how='left'
    )

    return players
```

**Schema Integration:**
- New columns to add: `wopr` (float), optionally `target_share`, `air_yards_share`
- Existing columns required: `targets` (from Metric 1), `air_yards` (from Metric 13)
- Data type compatibility: float columns (compatible)
- Backward compatibility: No impact (new column)

**Dependencies:**

**Metric Dependencies:**
- [x] **Metric 1: Target Volume/Share** (HIGH priority) - Provides targets
- [x] **Metric 13: Air Yards (aDOT)** (MEDIUM priority) - Provides air yards
- Can implement independently via scraping (PlayerProfiler or Next Gen Stats)

**Code Dependencies:**
- File: `util/PlayerManager.py` (likely location for WOPR calculation)
- Class/Function: Player scoring calculation methods
- Purpose: Apply WOPR multiplier to WR/TE scores
- Integration point: After base score, adjust based on WOPR

**External Dependencies:**
- Package: `beautifulsoup4` (for scraping)
- Package: `requests` (for HTTP)
- Package: `pandas` (already used)

**Cost Estimate:**
- Paid tier required: No
- Monthly cost: $0 (all sources free)

**Quick Win?**
- [ ] No - Requires scraping implementation (1-2 days)
- [x] Yes (if Metrics 1 + 13 already implemented) - Just calculation

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High value, medium implementation (depends on air yards source)

**Rationale:**

**Value:** ⭐⭐⭐⭐⭐ (Very High)
- **Best opportunity metric for WR/TE** - Combines volume and quality
- **Highly predictive** - Strong correlation with fantasy performance
- **Identifies breakout candidates** - High WOPR + low fantasy points = buy-low opportunity
- **Complements target share** - Accounts for depth of target (deep threats get credit)

**Feasibility:** ⭐⭐⭐ (Medium)
- **Requires air yards data** - Not in ESPN API or current data
- **Scraping required** - Next Gen Stats or PlayerProfiler (1-2 days)
- **Alternative:** Wait for Metric 13 (Air Yards) implementation
- Calculation is straightforward once data available

**Historical Data:** ⭐⭐⭐⭐ (Good)
- ✅ Available from Next Gen Stats (2016+)
- ✅ Available from PlayerProfiler (2015+)
- ✅ Predictive (calculate from weeks 1-N, apply to N+1)
- ⚠️ Requires scraping historical weeks

**Maintenance:** ⭐⭐⭐ (Medium)
- **Scraping maintenance** - Websites can change structure
- **Calculation stability** - Formula is fixed, no changes expected
- **Data dependency** - Relies on external sources (Next Gen Stats, PlayerProfiler)

**Preferred Data Source:** **Next Gen Stats** (official NFL data, most reliable)

**Alternative:** **PlayerProfiler** (provides WOPR directly, no calculation needed)

**Historical Feasibility:** ✅ **GOOD** - Available via scraping

**Implementation Priority:**
- [x] **High (after Metric 1 or 13)** OR **Immediate (via PlayerProfiler scraping)**

**Implementation Approaches:**

**Approach A: Standalone Implementation (Immediate)**
- Scrape Next Gen Stats for targets + air yards
- Calculate WOPR directly
- Timeline: 1-2 days
- Pros: Independent, gets WOPR immediately
- Cons: Duplicates Metric 1/13 effort

**Approach B: Dependent Implementation (After Metrics 1 + 13)**
- Wait for Metric 1 (Targets) and Metric 13 (Air Yards)
- Calculate WOPR from those metrics
- Timeline: 2-4 hours (just calculation)
- Pros: Reuses existing data, no new scraping
- Cons: Delayed until dependencies complete

**Approach C: Hybrid (Recommended)**
- Implement Metric 1 (Targets) first - HIGH priority
- Scrape PlayerProfiler for WOPR directly (includes implied air yards)
- Later: Replace with calculated WOPR when Metric 13 available
- Timeline: 1 day (after Metric 1)
- Pros: Gets WOPR sooner, validates against calculated version later
- Cons: Some duplicate effort

**Next Steps:**

**Recommended Path: Approach C (Hybrid)**

1. **Complete Metric 1 (Targets)** - HIGH priority, already researched
   - Provides target share component of WOPR

2. **Scrape PlayerProfiler for WOPR**
   - URL: `https://www.playerprofiler.com/nfl/`
   - Get direct WOPR values (no air yards calculation needed)
   - Add `wopr` column to players.csv
   - Timeline: 1 day

3. **Apply WOPR to scoring algorithm**
   - Add WOPR multiplier to WR/TE scoring
   - High WOPR (>50%) = 1.10x boost
   - Medium WOPR (30-50%) = 1.00x (neutral)
   - Low WOPR (<30%) = 0.95x penalty

4. **Later: Implement Metric 13 (Air Yards)**
   - When MEDIUM priority metrics tackled
   - Recalculate WOPR from components (validate)
   - Switch to calculated WOPR (more control)

5. **Test with historical data**
   - Run simulation with WOPR enabled
   - Compare accuracy vs baseline
   - Expect improvement in WR/TE projections

**Example Impact:**
```
Tyreek Hill (MIA, WOPR: 69.2%):
- Base projection: 16.5 points
- WOPR multiplier: 1.10 (elite opportunity)
- Adjusted projection: 16.5 * 1.10 = 18.15 points ✅ Accurate boost

WR3 (WOPR: 22%):
- Base projection: 9.0 points
- WOPR multiplier: 0.95 (limited opportunity)
- Adjusted projection: 9.0 * 0.95 = 8.55 points ✅ Realistic penalty
```

**Blockers:**
- ⚠️ **Dependent on Metric 1 OR independent scraping** (can proceed either way)
- ⚠️ **Requires air yards** - either from scraping or Metric 13

**Timeline:**
- Standalone (scraping): 1-2 days
- After Metrics 1 + 13: 2-4 hours (calculation only)
- **Recommended: 1 day (after Metric 1, scrape PlayerProfiler)**

---

## Research Completeness Checklist

- [x] All 7 sections completed above
- [x] Position applicability documented (WR, TE)
- [x] Minimum 2-3 free alternatives researched (Next Gen Stats, PlayerProfiler, Sleeper)
- [x] Historical data availability assessed (YES - via scraping)
- [x] Schema definition provided (wopr column)
- [x] Clear recommendation provided (PURSUE - Hybrid approach recommended)
- [x] Dependencies documented (Metrics 1 + 13 OR scraping)
- [x] Effort estimate provided (1-2 days standalone, 2-4 hours if dependent)

---

## Related Metrics

**Similar/Related Metrics:**
- **Metric 1: Target Volume/Share** - Provides targets component ⚠️ **DEPENDENCY**
- **Metric 13: Air Yards (aDOT)** - Provides air yards component ⚠️ **DEPENDENCY**
- Metric 17: Target Share Trend - Tracks target share over time
- Metric 58: Total Opportunity Share (WR) - Similar concept, different formula

**Notes:**
- **WOPR is composite metric** - Best opportunity predictor for WR/TE
- Complements target share alone (accounts for depth)
- High WOPR + low fantasy points = efficiency red flag (drops, poor QB)
- Can implement standalone OR calculate from Metrics 1 + 13

**Implementation Order Options:**
1. **Immediate (Standalone):** Scrape Next Gen Stats or PlayerProfiler → WOPR
2. **Dependent:** Metric 1 → Metric 13 → Calculate WOPR (2-4 hours after both)
3. **Hybrid (Recommended):** Metric 1 → Scrape PlayerProfiler WOPR → Later validate with Metric 13

---

## Lifecycle Notes

**Data Source Stability:** Medium (scraping-dependent) to High (if using Metrics 1+13)
**Deprecation Risk:** Low (WOPR is established fantasy metric, won't disappear)
**Replacement Strategy:** Start with PlayerProfiler scraping, migrate to calculated WOPR when Metrics 1+13 available

**Enhancement Path:**
- **Phase 1 (Immediate):** Scrape PlayerProfiler for direct WOPR values
- **Phase 2 (After Metric 1):** Validate WOPR against target share (sanity check)
- **Phase 3 (After Metric 13):** Calculate WOPR from components, compare to scraped version
- **Phase 4 (Future):** Experiment with alternative WOPR weights (position-specific TE vs WR)

**Maintenance Notes:**
- **Scraping fragility:** PlayerProfiler or Next Gen Stats may change HTML structure
- **Fallback plan:** If scraping breaks, use target share only (degraded WOPR)
- **Long-term:** Prefer calculated WOPR from Metrics 1+13 (more stable)

---

*Research conducted: 2025-12-20*
*Next review: After Metric 1 and/or Metric 13 implementation*
