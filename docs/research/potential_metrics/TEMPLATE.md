# Metric [N]: [Metric Name]

**Position Applicability:** [QB/RB/WR/TE/K or "All positions"]
**Priority:** [HIGH/MEDIUM/LOW]
**Research Date:** YYYY-MM-DD

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data in the `data/` folder?**

- [ ] Yes - Calculate from existing columns
- [ ] Partial - Some data exists, needs supplementation
- [ ] No - Requires external data source

**Details:**

[If YES or PARTIAL: Document exact calculation formula and reference specific column names]

[If NO: Explain why existing data is insufficient]

**Existing Columns Referenced:**
- File: `[filename.csv]`
- Columns: `[column_name_1]`, `[column_name_2]`

**Calculation Formula** (if applicable):
```
[metric_name] = [formula using existing columns]
```

**Example Calculation** (optional):
```
Player X: [show calculation with real column values]
```

---

## 2. ESPN API Availability

**Is this metric available via ESPN Fantasy Football API?**

- [ ] Yes - Available directly
- [ ] Partial - Related data available, needs calculation
- [ ] No - Not available in ESPN API

**Sources Checked:**
- [ ] ESPN Player Data API (`docs/espn/espn_player_data.md`)
- [ ] ESPN Team Stats API
- [ ] ESPN Game Data API (`docs/research/ESPN_NFL_Game_Data_Research_Report.md`)
- [ ] Other: [specify]

**API Endpoint/Field** (if available):
- Endpoint: `[API endpoint path]`
- Field name: `[field_name]`
- Data type: `[int/float/string/boolean]`
- Example value: `[sample value]`

**Evidence:**
[Document what was checked and what was found/not found]

**Limitations** (if applicable):
- Authentication required: [Yes/No]
- Rate limits: [specify if known]
- Update frequency: [real-time/daily/weekly]

---

## 3. Free Alternative Sources

**What free data sources provide this metric?**

**Source 1: [Name]**
- URL/API: `[link or API endpoint]`
- Data format: [JSON/CSV/HTML/API]
- Update frequency: [real-time/daily/weekly]
- Free tier limits: [requests per day/month, or "unlimited"]
- Authentication: [Required: API key / Not required]
- Data quality: [High/Medium/Low - based on documentation or community reports]

**Source 2: [Name]**
- URL/API: `[link or API endpoint]`
- Data format: [JSON/CSV/HTML/API]
- Update frequency: [real-time/daily/weekly]
- Free tier limits: [requests per day/month, or "unlimited"]
- Authentication: [Required: API key / Not required]
- Data quality: [High/Medium/Low]

**Source 3: [Name]** (if applicable)
- URL/API: `[link or API endpoint]`
- Data format: [JSON/CSV/HTML/API]
- Update frequency: [real-time/daily/weekly]
- Free tier limits: [requests per day/month, or "unlimited"]
- Authentication: [Required: API key / Not required]
- Data quality: [High/Medium/Low]

**Comparison:**
[Brief comparison of data quality, reliability, ease of use across sources]

**Recommended Source:** [Which free source is best and why]

---

## 4. Data Quality Assessment

**Reliability:** [High/Medium/Low]
**Accuracy:** [High/Medium/Low]
**Update Frequency:** [real-time/daily/weekly/seasonal]

**Details:**

**Reliability Assessment:**
- Source stability: [Is this a well-established API/site?]
- Historical uptime: [Known issues or downtime?]
- Community trust: [What do developers say about this source?]

**Accuracy Assessment:**
- Methodology: [How is this metric calculated by the source?]
- Known issues: [Any documented accuracy problems?]
- Validation: [Can we verify accuracy against other sources?]

**Update Frequency:**
- Live games: [How often updated during games?]
- Historical data: [When does historical data become available?]
- Consistency: [Regular update schedule or sporadic?]

**Known Limitations:**
1. [Limitation 1: e.g., "Data not available for games played in bad weather"]
2. [Limitation 2: e.g., "Historical data only goes back to 2020"]
3. [Limitation 3: e.g., "Free tier limited to 100 requests/day"]

**Edge Cases:**
- Missing data: [How often? What triggers it?]
- Incorrect data: [Known scenarios where data is wrong]
- Delayed updates: [Typical delay from game event to data availability]

---

## 5. Historical Data Availability ⚠️ CRITICAL

**Can we obtain weekly snapshots for simulation validation?**

- [ ] Yes - Historical data available
- [ ] Partial - Some seasons/weeks available
- [ ] No - Only live/current data available

**Historical Data Details:**

**Seasons Available:**
- [ ] 2021 season (17 weeks)
- [ ] 2022 season (17 weeks)
- [ ] 2024 season (17 weeks)
- [ ] 2023 season (not currently in sim_data but could add)
- [ ] Other: [specify years]

**Weekly Snapshot Verification:**
- Sample weeks checked: [e.g., weeks 1, 5, 10, 15]
- All 17 weeks available: [Yes/No]
- Gaps in coverage: [List any missing weeks]

**Data Timing (Predictive vs Retrospective):**
- [ ] Represents "what we knew going INTO that week" ✅
- [ ] Retrospective data only (not suitable for simulation)
- [ ] Unknown - requires further investigation

**Example Format** (for weekly snapshots):
```
Week 5 folder should contain:
- Weeks 1-4: Actual values
- Weeks 5-17: Projected values (as of start of week 5)
```

**sim_data Integration:**

**Where does this metric fit?**
- [ ] Player-level: Add columns to `players.csv` (actuals) and `players_projected.csv` (projections)
- [ ] Team-level: Add columns to `team_data/{TEAM}.csv`
- [ ] Game-level: Add columns to `game_data.csv`
- [ ] New file required: [Specify file name and structure]

**Schema Definition:**
- Column name(s): `[column_name]`
- Data type: `[int/float/string/boolean]`
- Null handling: [How to handle missing data]
- Example values: `[sample values]`

**Historical Data Acquisition:**
- [ ] Available via API (specify which API)
- [ ] Available via bulk download (specify URL)
- [ ] Requires web scraping (specify source)
- [ ] Not available (cannot validate in simulations)

**Timeline:** [How long to acquire historical data for 1 season?]

---

## 6. Implementation Complexity

**Difficulty:** [Easy/Medium/Hard]
**Estimated Effort:** [Hours/Days - rough estimate]

**Breakdown:**

**Data Fetching:**
- Complexity: [Easy/Medium/Hard]
- Pattern to follow: [e.g., "Follow `player-data-fetcher/` async pattern"]
- Required packages: `[package names]`
- Authentication: [API keys, OAuth, none]
- Rate limiting handling: [Required/Not required]

**Data Processing:**
- Complexity: [Easy/Medium/Hard]
- Calculations required: [Simple/Complex - describe]
- Data transformations: [List key transformations]
- Error handling: [Key error scenarios to handle]

**Schema Integration:**
- New columns to add: `[column names]`
- Existing columns to modify: `[column names or "None"]`
- Data type compatibility: [Any conversion needed?]
- Backward compatibility: [Impact on existing code]

**Dependencies:**

**Metric Dependencies:**
- [ ] Requires Metric [N]: [metric name] to be implemented first
- [ ] Requires Metric [N]: [metric name] to be implemented first
- [ ] No dependencies

**Code Dependencies:**
- File: `[file path]`
- Class/Function: `[name]`
- Purpose: [Why this dependency exists]

**External Dependencies:**
- Package: `[package name]` (version: `[X.Y.Z]`)
- Purpose: [What it's used for]
- Installation: `pip install [package]`

**Cost Estimate** (if free tier insufficient):
- Paid tier required: [Yes/No]
- Monthly cost: $[amount]
- Usage threshold: [When free tier runs out]

**Quick Win?**
- [ ] Yes - Data already exists, just need calculation logic
- [ ] No - Requires external data acquisition

---

## 7. Recommendation

**Should we pursue this metric?**

- [ ] **PURSUE** - High value, feasible implementation
- [ ] **DEFER** - Lower priority, pursue after higher-value metrics
- [ ] **SKIP** - Not feasible or insufficient value

**Rationale:**

[Explain the recommendation based on:]
- Value: How much does this improve accuracy/decisions?
- Feasibility: How easy is it to implement?
- Historical data: Can we validate in simulations?
- Maintenance: Ongoing effort to keep data current?

**Preferred Data Source:** [Existing data / ESPN API / Free Alternative: {name}]

**Historical Feasibility:** [Can we get historical data for validation?]

**Implementation Priority** (if PURSUE):
- [ ] Immediate - Critical for accuracy
- [ ] Short-term - High value, implement soon
- [ ] Long-term - Nice-to-have, lower priority

**Next Steps** (if PURSUE):
1. [Action 1: e.g., "Acquire API key for {source}"]
2. [Action 2: e.g., "Download historical data for 2021-2024"]
3. [Action 3: e.g., "Create data fetcher following player-data-fetcher pattern"]

**Blockers** (if DEFER or SKIP):
- [Blocker 1: e.g., "No historical data available"]
- [Blocker 2: e.g., "Free tier too restrictive"]
- [Blocker 3: e.g., "Insufficient accuracy improvement to justify effort"]

---

## Research Completeness Checklist

- [ ] All 7 sections completed above
- [ ] Position applicability documented (header)
- [ ] Minimum 2-3 free alternatives researched (if ESPN unavailable)
- [ ] Historical data availability assessed (CRITICAL)
- [ ] Schema definition provided (if pursuing)
- [ ] Clear recommendation provided with rationale
- [ ] Dependencies documented (metrics, packages, code)
- [ ] Effort estimate provided

---

## Related Metrics

**Similar/Related Metrics:**
- Metric [N]: [name] - [relationship: dependency, alternative, complementary]
- Metric [N]: [name] - [relationship]

**Notes:**
[Any cross-references or relationships to other metrics]

---

## Lifecycle Notes

**Data Source Stability:** [Stable/Unstable - based on source history]
**Deprecation Risk:** [Low/Medium/High]
**Replacement Strategy** (if source discontinued): [Alternative approach]

---

*Research conducted: [Date]*
*Next review: [Date or "Annual re-validation"]*
