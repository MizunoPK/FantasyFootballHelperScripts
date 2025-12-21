# Metric 22: Expected Fantasy Points (xFP)

**Position Applicability:** ALL positions
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data in the `data/` folder?**

- [ ] Yes - Calculate from existing columns
- [x] No - Requires new data source or complex model
- [ ] Partial - Some components available

**Details:**

Expected Fantasy Points (xFP) is **NOT available in existing data** and requires either:
1. Pre-calculated xFP from analytics sites (scraping)
2. Building a custom regression model (complex)

**Checked:**
- `data/players.csv` - NO xFP column
- Has actual fantasy_points, but NOT expected points

**What is xFP?**

Expected Fantasy Points measures how many fantasy points a player *should have scored* based on their opportunity (targets, carries, air yards, etc.) assuming league-average efficiency.

**Calculation Concept:**

xFP requires **position-specific regression models**:

**WR/TE xFP Model:**
```python
# Inputs: targets, air_yards, red_zone_targets, catch_rate, team_pace
# Model: Linear regression or machine learning
xFP_WR = β0 + β1(targets) + β2(air_yards) + β3(rz_targets) + β4(team_context)

# Simplified example:
xFP_WR ≈ (targets × 1.2) + (air_yards × 0.05) + (rz_targets × 3.0)

Example:
Tyreek Hill:
- 10 targets × 1.2 = 12.0
- 150 air yards × 0.05 = 7.5
- 2 RZ targets × 3.0 = 6.0
- xFP = 25.5 points (expected)
- Actual = 28.0 points → +2.5 overperformance
```

**RB xFP Model:**
```python
# Inputs: carries, targets, red_zone_carries, goal_line_carries
xFP_RB = β0 + β1(carries) + β2(targets) + β3(rz_carries) + β4(gl_carries)

# Simplified:
xFP_RB ≈ (carries × 0.8) + (targets × 1.5) + (rz_carries × 2.0) + (gl_carries × 4.0)
```

**QB xFP Model:**
```python
# Inputs: pass_attempts, completions, rush_attempts, sacks
xFP_QB = β0 + β1(attempts) + β2(completions) + β3(rush_attempts)
```

**K xFP Model:**
```python
# Inputs: fg_attempts, avg_distance, team_points_scored
xFP_K = β0 + β1(fg_attempts) + β2(1/avg_distance) + β3(xp_attempts)
```

**Challenges with Custom Calculation:**

1. **Requires multiple input metrics** - Most not in existing data:
   - Targets (Metric 1) ❌
   - Air yards (Metric 13) ❌
   - Red zone carries/targets (Metric 7) ❌
   - Carries (basic stat) ❌

2. **Requires regression model** - Need to train on historical data:
   - Collect 2-3 seasons of data
   - Build position-specific models
   - Validate model accuracy
   - Retrain periodically

3. **Complex maintenance** - Model degrades over time:
   - League trends change (more passing, etc.)
   - Requires annual retraining

**Conclusion:** Cannot calculate from existing data. Must either:
- **Option A:** Scrape pre-calculated xFP from analytics sites (easier)
- **Option B:** Build custom xFP model (very complex, requires many metrics)

---

## 2. ESPN API Availability

**Is this metric available via ESPN Fantasy Football API?**

- [ ] Yes - Available directly
- [x] No - Not available
- [ ] Partial - Some components available

**Sources Checked:**
- [x] ESPN Player Data API
- [x] ESPN Projections endpoint

**API Data:**

ESPN API **does NOT provide xFP (Expected Fantasy Points)**.

**What ESPN Provides:**
- `projectedPoints` - ESPN's season-long projection (NOT xFP)
- `appliedStatTotal` - Actual fantasy points scored
- `stats` array - Basic stats (receptions, yards, TDs)

**What ESPN Does NOT Provide:**
- Expected fantasy points based on opportunity
- xFP vs actual comparison
- Efficiency metrics

**Difference: Projections vs xFP**

| Metric | ESPN Projections | xFP (Expected Fantasy Points) |
|--------|------------------|-------------------------------|
| **What it is** | Pre-season forecast | Weekly opportunity-based expectation |
| **Based on** | Expert analysis, historical performance | Actual usage (targets, carries, air yards) |
| **Updates** | Rarely (pre-season, injuries) | Weekly (based on game-by-game opportunity) |
| **Purpose** | Season-long ranking | Identify over/underperformers week-to-week |

**Example:**
```
Week 5 - Tyreek Hill:
- ESPN Projection (pre-season): 16.0 points per game
- xFP (based on Week 5 opportunity): 18.5 points (10 targets, 150 air yards)
- Actual FP (Week 5): 21.0 points
- Interpretation: Outperformed xFP by +2.5 (efficient game)
```

ESPN projections are **static forecasts**, xFP is **dynamic opportunity measurement**.

**Conclusion:** ESPN API does not provide xFP. Must use alternative sources or build custom model.

---

## 3. Free Alternative Sources

**What free data sources provide this metric?**

### Source 1: PlayerProfiler.com (xFP Available)

- URL: `https://www.playerprofiler.com/nfl/`
- Data format: HTML tables (scraping required)
- Update frequency: Weekly
- Free tier limits: Unlimited (public website)
- Authentication: Not required
- Data quality: **Excellent** - Industry-standard xFP calculations

**Details:**
- PlayerProfiler calculates xFP for WR/RB/TE
- Shows xFP, actual FP, and delta (over/underperformance)
- Position-specific models (different for WR vs RB)
- Historical data: ✅ Available (past seasons)
- **Limitation:** Must scrape (no official free API)

**Example Data:**
```
Player: Christian McCaffrey (RB)
xFP (Expected): 18.5 points
Actual FP: 22.0 points
Delta: +3.5 (overperforming)
```

### Source 2: 4for4.com (xFP - Premium Feature)

- URL: `https://www.4for4.com/`
- Data format: HTML tables (subscription site)
- Update frequency: Weekly
- Free tier limits: ⚠️ Very limited (most xFP data is premium)
- Authentication: Subscription required ($$$)
- Data quality: **Excellent** - Advanced analytics

**Details:**
- 4for4 has proprietary xFP models
- Covers all positions (QB, RB, WR, TE, K)
- Shows xFP trends over time
- **Limitation:** Paywall ($50-100/year)

### Source 3: FantasyPoints.com (xFP - Premium)

- URL: `https://www.fantasypoints.com/`
- Data format: HTML + API (paid tier)
- Update frequency: Weekly
- Free tier limits: ⚠️ No xFP in free tier
- Authentication: Subscription required
- Data quality: **Very High**

**Details:**
- Premium feature only
- Position-specific xFP models
- **Limitation:** Requires paid subscription

### Source 4: Custom Model (Build Your Own)

- URL: N/A (local implementation)
- Data format: CSV / Database
- Update frequency: Weekly (after games)
- Free tier limits: ✅ Unlimited (DIY)
- Authentication: N/A
- Data quality: **Depends on model**

**Details:**
- Build regression model using historical data
- Required inputs:
  - Targets, air yards (Metrics 1, 13)
  - Carries, red zone opportunities (Metric 7)
  - Team context (Metric 2, 4)
- Train on 2-3 seasons of data
- Predict expected points for current season

**Implementation:**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

# Step 1: Load historical data (2021-2023)
historical = load_historical_stats(['targets', 'air_yards', 'carries', 'rz_targets', 'actual_fp'])

# Step 2: Train position-specific models
wr_model = LinearRegression()
wr_model.fit(
    historical[historical['position'] == 'WR'][['targets', 'air_yards', 'rz_targets']],
    historical[historical['position'] == 'WR']['actual_fp']
)

# Step 3: Predict xFP for current week
current_week_wr = load_current_week_stats(['targets', 'air_yards', 'rz_targets'])
current_week_wr['xFP'] = wr_model.predict(current_week_wr[['targets', 'air_yards', 'rz_targets']])

# Step 4: Calculate delta
current_week_wr['fp_delta'] = current_week_wr['actual_fp'] - current_week_wr['xFP']
```

**Comparison:**

| Source | xFP Available | All Positions | Historical | Free Tier | Ease of Use |
|--------|--------------|---------------|------------|-----------|-------------|
| PlayerProfiler | ✅ Yes | ⚠️ WR/RB/TE only | ✅ Yes | ✅ Unlimited | Medium (scraping) |
| 4for4 | ✅ Yes | ✅ All | ✅ Yes | ❌ Paywall | Low (subscription) |
| FantasyPoints | ✅ Yes | ✅ All | ✅ Yes | ❌ Paywall | Low (subscription) |
| Custom Model | ✅ Build it | ✅ All | ✅ Yes (DIY) | ✅ Unlimited | Very Low (complex) |

**Recommended Source:** **PlayerProfiler** (free, scraping required, WR/RB/TE only)

**Alternative:** **Custom Model** (full control, but very complex - requires data science expertise)

---

## 4. Data Quality Assessment

**Reliability:** Medium-High (depends on source)
**Accuracy:** High (established models from analytics sites)
**Update Frequency:** Weekly

**Details:**

**Reliability Assessment:**
- **PlayerProfiler:** Stable site, consistent xFP methodology
- **Custom Model:** Depends on implementation quality
- Historical uptime: PlayerProfiler has good track record

**Accuracy Assessment:**
- **Methodology:** xFP models use regression on historical opportunity → fantasy points
- **Industry standard:** PlayerProfiler/4for4 models are well-validated
- **Custom models:** Accuracy depends on feature selection and training data
- **Known issues:** xFP models struggle with:
  - Low-sample players (rookies, backups)
  - Extreme efficiency (outliers)
  - Changing roles (RB committee shifts)

**Update Frequency:**
- PlayerProfiler: Updates within 48 hours post-game
- Custom model: Updates when you run it (flexible)
- Historical data: Multi-season archives available

**Known Limitations:**

1. **Small sample size issues:**
```python
# Player with 2 targets in a game
xFP = 2.4 points (based on 2 targets × 1.2)
Actual = 15.0 points (1 target = 60-yard TD)
Delta = +12.6 ← HUGE variance due to small sample
```

2. **Regression to the mean:**
- Players overperforming xFP tend to regress toward xFP
- Players underperforming xFP tend to improve toward xFP
- BUT: Elite players can sustain +xFP (better talent)

3. **Model degradation:**
- xFP models trained on old data become less accurate
- League trends change (more passing, etc.)
- Requires periodic retraining

4. **Position-specific accuracy:**
```
WR/RB xFP: Very accurate (strong opportunity → points correlation)
QB xFP: Moderately accurate (passing efficiency varies widely)
K xFP: Less accurate (team scoring is noisy week-to-week)
TE xFP: Moderately accurate (role variance high)
```

**Edge Cases:**

**Garbage Time Production:**
```python
# Player gets 5 targets in garbage time (team down 28 points)
# xFP model: 6.0 points (5 targets × 1.2)
# Actual: 12.0 points (garbage time boost)
# Delta: +6.0 (overperformance, but not sustainable)
```

**Role Changes:**
```python
# RB1 gets injured mid-game, RB2 takes over
# xFP model: 8.0 points (based on RB2 historical usage)
# Actual: 18.0 points (RB1 volume in second half)
# Delta: +10.0 (opportunity changed, model didn't know)
```

**Validation:**
- Compare xFP to actual FP correlation (should be r > 0.7)
- Check model residuals (errors should be normally distributed)
- Cross-validate on holdout data (test on previous season)

---

## 5. Historical Data Availability ⚠️ CRITICAL

**Can we obtain weekly snapshots for simulation validation?**

- [x] Yes - Historical data available (with caveats)

**Historical Data Details:**

**Seasons Available:**
- [x] 2021 season - ✅ Via PlayerProfiler (scraping) OR custom model
- [x] 2022 season - ✅ Via PlayerProfiler OR custom model
- [x] 2024 season - ✅ Via PlayerProfiler OR custom model
- [x] 2023 season - ✅ Available if needed

**Weekly Snapshot Verification:**

xFP is **calculated retrospectively** after a game is played:
- Week 5 game happens → Collect stats (targets, carries, etc.)
- Calculate xFP based on Week 5 opportunity
- Compare to Week 5 actual fantasy points

**Data Timing (Predictive vs Retrospective):**
- [x] Can be made predictive: Use weeks 1-N xFP delta to predict week N+1

**Verification:**
```
Week 5 simulation approach:

Option 1: Retrospective xFP (NOT predictive):
- Use Week 5 xFP to evaluate Week 5 performance ❌ NOT USEFUL for simulation
- This is analysis, not prediction

Option 2: xFP Delta Trend (PREDICTIVE):
- Calculate xFP delta for weeks 1-4: avg_delta = (actual - xFP) / 4
- Players with positive delta (overperforming) → boost week 5 projection
- Players with negative delta (underperforming) → reduce week 5 projection
- This IS predictive (using past efficiency to predict future)
```

**Predictive Usage:**
```python
# For week 5 projection:
# 1. Calculate cumulative xFP delta from weeks 1-4
weeks_1_4_delta = (actual_fp_weeks_1_4 - xfp_weeks_1_4).mean()

# 2. Determine if player is over/underperforming
if weeks_1_4_delta > 2.0:
    # Overperforming (expect regression downward)
    week_5_adjustment = -0.05  # 5% penalty
elif weeks_1_4_delta < -2.0:
    # Underperforming (expect positive regression)
    week_5_adjustment = +0.05  # 5% boost
else:
    # Performing as expected
    week_5_adjustment = 0.0

# 3. Apply to week 5 projection
week_5_projection *= (1 + week_5_adjustment)
```

**Historical Acquisition Process:**

**Option 1: Scrape PlayerProfiler (Easiest)**

```python
def scrape_playerprofiler_xfp(year: int, week: int) -> pd.DataFrame:
    """
    Scrape PlayerProfiler for historical xFP data.

    Returns DataFrame with columns:
    - player_name, position, xFP, actual_FP, delta
    """
    url = f"https://www.playerprofiler.com/nfl/{year}/"
    # Scraping logic
    pass
```

**Option 2: Build Custom xFP Model (Complex)**

```python
def build_xfp_model(historical_years: list) -> dict:
    """
    Train position-specific xFP models.

    Returns dict of models: {'WR': model, 'RB': model, ...}
    """
    # Load historical data (targets, carries, air yards, actual FP)
    hist = load_historical_data(historical_years)

    models = {}
    for position in ['WR', 'RB', 'TE', 'QB']:
        pos_data = hist[hist['position'] == position]

        # Train regression model
        X = pos_data[['targets', 'air_yards', 'carries', 'rz_targets']]
        y = pos_data['actual_fp']

        model = LinearRegression()
        model.fit(X, y)

        models[position] = model

    return models

def calculate_xfp_historical(year: int, week: int, models: dict) -> pd.DataFrame:
    """
    Calculate xFP for historical week using trained models.
    """
    # Load week stats
    week_stats = load_week_stats(year, week)

    for position, model in models.items():
        pos_players = week_stats[week_stats['position'] == position]
        X = pos_players[['targets', 'air_yards', 'carries', 'rz_targets']]
        pos_players['xFP'] = model.predict(X)

    return week_stats
```

**sim_data Integration:**

**Where does this metric fit?**
- [x] Player-level: Add columns to `players.csv` (xFP, xFP_delta for weeks 1-N)

**Schema Definition:**

**Player-level columns:**
- File: `simulation/sim_data/{YEAR}/weeks/week_{NN}/players.csv`
- New columns:
  - `xfp_cumulative` (float): Cumulative xFP through week N-1
  - `actual_fp_cumulative` (float): Cumulative actual FP through week N-1
  - `xfp_delta` (float): Cumulative (actual - xFP), positive = overperforming
  - `xfp_adjustment` (float): Adjustment multiplier for week N (0.95-1.05)

**Calculation Timing:**
```python
# For week 5 simulation:
# 1. Load cumulative xFP and actual FP from weeks 1-4
xfp_weeks_1_4 = sum(xfp for weeks 1-4)
actual_weeks_1_4 = sum(actual_fp for weeks 1-4)

# 2. Calculate delta
xfp_delta = actual_weeks_1_4 - xfp_weeks_1_4

# 3. Apply regression adjustment to week 5
if xfp_delta > 2.0:
    week_5_adjustment = 0.95  # Expect negative regression
elif xfp_delta < -2.0:
    week_5_adjustment = 1.05  # Expect positive regression
else:
    week_5_adjustment = 1.00

players_week_5['xfp_adjustment'] = week_5_adjustment
players_week_5['adjusted_projection'] = players_week_5['base_projection'] * week_5_adjustment
```

**Historical Data Acquisition:**
- [x] Available from PlayerProfiler (scraping)
- [x] Can build custom model (complex)

**Timeline:**
- PlayerProfiler scraping: 2-3 days
- Custom model: 1-2 weeks (model development + validation)

---

## 6. Implementation Complexity

**Difficulty:** Hard (custom model) OR Medium (scraping)
**Estimated Effort:** 1-2 weeks (custom model) OR 2-3 days (scraping)

**Breakdown:**

**Data Fetching:**

**Option A: Scrape PlayerProfiler (Recommended)**
- Complexity: **Medium**
- Pattern to follow: Similar to other scraping (Metric 1, 4, 21)
- Required packages: `requests`, `beautifulsoup4`, `pandas`
- Authentication: Not required
- Rate limiting handling: Respectful delays (2 seconds between requests)

**Option B: Build Custom xFP Model**
- Complexity: **Very Hard**
- Pattern to follow: Machine learning model development
- Required packages: `scikit-learn`, `pandas`, `numpy`
- Required data: Historical stats (targets, carries, air yards, RZ opportunities)
- Model training: Requires 2-3 seasons of data

**Data Processing:**

**Scraping Approach (Medium):**
```python
def fetch_playerprofiler_xfp(year: int) -> pd.DataFrame:
    """
    Scrape xFP from PlayerProfiler.
    """
    url = f"https://www.playerprofiler.com/nfl/{year}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse table for xFP, actual FP, delta
    # Expected columns: Player, Position, xFP, Actual FP, Delta

    return parsed_df
```

**Custom Model Approach (Very Hard):**
```python
def build_and_train_xfp_model() -> dict:
    """
    Build position-specific xFP models.

    Steps:
    1. Load historical data (2021-2023)
    2. Engineer features (targets, carries, air yards, RZ opportunities)
    3. Train separate models for WR, RB, TE, QB
    4. Validate on holdout data
    5. Return trained models
    """
    # Feature engineering
    features_wr = ['targets', 'air_yards', 'rz_targets', 'team_pace']
    features_rb = ['carries', 'targets', 'rz_carries', 'gl_carries']
    features_qb = ['attempts', 'completions', 'rush_attempts']

    # Train models
    wr_model = train_regression_model(features_wr, 'WR')
    rb_model = train_regression_model(features_rb, 'RB')
    # ... etc

    return {'WR': wr_model, 'RB': rb_model, ...}

def train_regression_model(features: list, position: str):
    """
    Train regression model for a position.
    """
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error

    # Load data
    data = load_historical_position_data(position)

    X = data[features]
    y = data['actual_fp']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Validate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"{position} model MSE: {mse}")

    return model
```

**Schema Integration:**
- New columns: `xfp_cumulative`, `actual_fp_cumulative`, `xfp_delta`, `xfp_adjustment`
- Existing columns required: `fantasy_points` (actual FP)
- Data type compatibility: All floats (compatible)
- Backward compatibility: No impact (new columns)

**Dependencies:**

**Metric Dependencies:**
- Custom model requires:
  - Metric 1: Target Volume (HIGH priority)
  - Metric 7: Red Zone Opportunity (MEDIUM priority)
  - Metric 13: Air Yards (MEDIUM priority)
  - Basic stats: Carries, receptions, yards (need source)

- Scraping approach: **No dependencies** (PlayerProfiler provides xFP directly)

**Code Dependencies:**
- File: `util/PlayerManager.py` (apply xFP adjustment)
- Purpose: Adjust projections based on xFP delta (regression adjustment)
- Integration point: After base projection, apply xFP adjustment multiplier

**External Dependencies:**
- **Scraping:** `beautifulsoup4`, `requests`
- **Custom model:** `scikit-learn`, `numpy`

**Cost Estimate:**
- Paid tier required: No (PlayerProfiler free) OR No (DIY model)
- Monthly cost: $0

**Quick Win?**
- [ ] No - Requires either scraping (2-3 days) or model building (1-2 weeks)

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High value, medium implementation (scraping approach)
- [ ] **DEFER** - If choosing custom model (very complex)

**Rationale:**

**Value:** ⭐⭐⭐⭐⭐ (Very High)
- **Best efficiency metric** - Identifies over/underperformers
- **Regression indicator** - Predicts positive/negative regression
- **Buy low / Sell high tool** - High xFP + low actual = buy, opposite = sell
- **Complements projections** - Adds context (is player efficient or lucky?)

**Feasibility:** ⭐⭐⭐ (Medium - scraping) OR ⭐ (Very Low - custom model)
- **Scraping approach:** 2-3 days, straightforward
- **Custom model:** 1-2 weeks, requires data science expertise
- **Recommended:** Scraping (much easier, same value)

**Historical Data:** ⭐⭐⭐⭐ (Good)
- ✅ Available from PlayerProfiler (scraping)
- ✅ Can make predictive (use xFP delta trend)
- ⚠️ Requires scraping historical weeks

**Maintenance:** ⭐⭐⭐ (Medium - scraping) OR ⭐⭐ (Low - custom model)
- **Scraping:** Website structure changes may break scraper
- **Custom model:** Requires annual retraining, feature engineering
- **Preferred:** Scraping (less ongoing maintenance)

**Preferred Data Source:** **PlayerProfiler** (free, established xFP methodology)

**Alternative:** **Custom model** (only if you have data science resources and want full control)

**Historical Feasibility:** ✅ **GOOD** - Available via scraping

**Implementation Priority:**
- [x] **Medium-High (after basic metrics)** - Very valuable, but requires setup time

**Recommended Approach: Scrape PlayerProfiler**

**Next Steps:**

1. **Scrape PlayerProfiler for xFP**
   - URL: `https://www.playerprofiler.com/nfl/`
   - Extract: Player name, position, xFP, actual FP, delta
   - Timeline: 2-3 days

2. **Calculate cumulative xFP delta**
   - For weeks 1-N, sum xFP and actual FP
   - Calculate delta: actual - xFP
   - Store in `xfp_delta` column

3. **Apply regression adjustment to projections**
   - If xFP delta > +2.0: Apply 0.95x multiplier (expect negative regression)
   - If xFP delta < -2.0: Apply 1.05x multiplier (expect positive regression)
   - Otherwise: No adjustment (1.00x)

4. **Test with historical data**
   - Run simulation with xFP adjustment enabled
   - Compare accuracy vs baseline
   - Validate that regression adjustment improves projections

5. **Monitor and maintain**
   - Check PlayerProfiler scraper monthly (structure changes)
   - Validate xFP values against expected ranges
   - Adjust regression thresholds if needed

**Example Impact:**
```
Player A (Overperformer):
- Weeks 1-4 actual FP: 70.0 points
- Weeks 1-4 xFP: 55.0 points
- Delta: +15.0 (averaging +3.75 per game)
- Week 5 base projection: 18.0 points
- xFP adjustment: 0.95 (expect regression)
- Adjusted projection: 18.0 × 0.95 = 17.1 points ✅ More realistic

Player B (Underperformer):
- Weeks 1-4 actual FP: 40.0 points
- Weeks 1-4 xFP: 52.0 points
- Delta: -12.0 (averaging -3.0 per game)
- Week 5 base projection: 12.0 points
- xFP adjustment: 1.05 (expect positive regression)
- Adjusted projection: 12.0 × 1.05 = 12.6 points ✅ Accounts for bad luck
```

**Blockers:**
- ⚠️ **Requires scraping implementation** (2-3 days)
- ⚠️ **Alternative: Custom model requires many metrics** (Metrics 1, 7, 13 + model building)

**Timeline:**
- Scraping approach: 2-3 days
- Custom model approach: 1-2 weeks (NOT recommended unless strong data science resources)

---

## Research Completeness Checklist

- [x] All 7 sections completed above
- [x] Position applicability documented (ALL positions)
- [x] Minimum 2-3 free alternatives researched (PlayerProfiler, 4for4, Custom Model)
- [x] Historical data availability assessed (YES - via scraping)
- [x] Schema definition provided (xfp_delta, xfp_adjustment columns)
- [x] Clear recommendation provided (PURSUE - Scraping approach)
- [x] Dependencies documented (None for scraping, many for custom model)
- [x] Effort estimate provided (2-3 days scraping, 1-2 weeks custom model)

---

## Related Metrics

**Similar/Related Metrics:**
- Metric 1: Target Volume - Input to xFP model
- Metric 7: Red Zone Opportunity - Input to xFP model
- Metric 13: Air Yards - Input to xFP model
- Metric 21: WOPR - Similar opportunity-based metric

**Notes:**
- **xFP is composite efficiency metric** - Compares actual to expected production
- Best use: Regression prediction (over/underperformers)
- Can implement standalone (scraping) OR calculate from components (custom model)
- Scraping is MUCH easier and gets same value

**Implementation Order:**
- **Recommended:** Standalone via PlayerProfiler scraping (no dependencies)
- **Alternative:** After Metrics 1, 7, 13 (build custom model - complex)

---

## Lifecycle Notes

**Data Source Stability:** Medium (scraping-dependent) to Low (custom model maintenance)
**Deprecation Risk:** Low (xFP is established fantasy metric)
**Replacement Strategy:** Start with PlayerProfiler scraping, optionally build custom model later for more control

**Enhancement Path:**
- **Phase 1 (Recommended):** Scrape PlayerProfiler for xFP values (2-3 days)
- **Phase 2:** Apply xFP delta regression adjustment to projections
- **Phase 3 (Future - Optional):** Build custom xFP model for full control (1-2 weeks)
- **Phase 4 (Advanced):** Refine regression adjustment thresholds based on validation

**Maintenance Notes:**
- **Scraping fragility:** PlayerProfiler may change HTML structure
- **Fallback plan:** If scraping breaks, disable xFP adjustment temporarily
- **Long-term:** Consider custom model only if scraping becomes unreliable

---

*Research conducted: 2025-12-20*
*Next review: After scraping implementation OR after Metrics 1, 7, 13 if building custom model*
