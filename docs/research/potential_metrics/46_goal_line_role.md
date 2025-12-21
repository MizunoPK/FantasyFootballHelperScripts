# Metric 46: Goal-Line Role (RB)

**Position Applicability:** RB (Running Back)
**Priority:** HIGH
**Research Date:** 2025-12-20

---

## 1. Existing Data Analysis

**Can this metric be calculated from existing data?**

- [x] No - Requires situational data

**Details:**

Goal-Line Role requires **situational/play-by-play data** (carries inside 5-yard line).

**Formula:**
```
Goal-Line Carry Share = (RB Goal-Line Carries / Team Goal-Line Carries) × 100

Example - Christian McCaffrey:
12 goal-line carries out of 15 team attempts = 80% (primary goal-line back)

Committee RB:
3 goal-line carries out of 15 team attempts = 20% (limited TD opportunity)
```

**Why It Matters:**
- TDs worth 6 points (highest-value scoring event)
- Goal-line role predicts TDs better than total carries
- Committee backs: One gets yardage, another gets goal-line TDs

**Conclusion:** Not in existing data. Requires situational stats or red zone data.

---

## 2. ESPN API Availability

**Is this metric available via ESPN Fantasy Football API?**

- [x] No - Not available

ESPN Fantasy API does NOT provide situational stats (carries by field position).

---

## 3. Free Alternative Sources

### Source 1: Pro Football Reference (Situational Splits)

- URL: `https://www.pro-football-reference.com/players/[ID]/splits/`
- Data: Situational stats by field position
- Free tier: ✅ Unlimited
- Historical: ✅ Available
- Quality: **Excellent**

**Details:**
- PFR player pages have "Splits" section
- Shows stats by field zone (Own 1-19, Opp 1-19, Red Zone, etc.)
- Can extract carries inside opponent's 5-yard line
- **Limitation:** Per-player scraping (not single page for all RBs)

### Source 2: PlayerProfiler (Red Zone Metrics)

- URL: `https://www.playerprofiler.com/nfl/`
- Data: Red zone carries, goal-line work
- Free tier: ✅ Unlimited
- Quality: **Excellent**

**May show "Opportunity Share" or "Red Zone Touches" which correlates with goal-line role.**

### Source 3: Next Gen Stats (Limited)

- URL: `https://nextgenstats.nfl.com/`
- Data: Advanced rushing metrics
- May not have specific goal-line carry data

**Recommended Source:** **Pro Football Reference** (situational splits) or **PlayerProfiler** (if goal-line data available)

---

## 4. Data Quality Assessment

**Reliability:** High (PFR very stable)
**Accuracy:** Very High (official NFL play-by-play)
**Update Frequency:** Weekly

**Known Limitations:**
- Small sample size (few goal-line opportunities per game)
- Game script dependent (leading teams run more at goal line)
- Injury/committee changes affect role

---

## 5. Historical Data Availability ⚠️ CRITICAL

**Can we obtain weekly snapshots for simulation validation?**

- [x] Yes - Historical data available via PFR splits

**Seasons Available:**
- 2021-2024: ✅ Via PFR player splits

**Data Timing:** ✅ Predictive (cumulative goal-line carries through week N)

**Historical Acquisition:**
```python
def scrape_pfr_goal_line_carries(player_id: str, year: int) -> dict:
    """Scrape PFR player splits for goal-line carries"""
    url = f"https://www.pro-football-reference.com/players/{player_id}/splits/{year}/"
    # Parse "By Field Position" table
    # Extract: Carries inside opponent's 1-19 (goal line area)
    return {'goal_line_carries': X, 'goal_line_tds': Y}
```

**sim_data Integration:**
- File: `players.csv`
- New columns: `goal_line_carries` (int), `goal_line_share` (float, %), `goal_line_multiplier` (float)

---

## 6. Implementation Complexity

**Difficulty:** Medium-Hard
**Estimated Effort:** 2-3 days (per-player PFR scraping)

**Data Fetching:**
- Scrape PFR player splits pages (requires player ID lookup)
- OR scrape PlayerProfiler if goal-line data available
- Extract goal-line carries from situational table

**Multiplier Calculation:**
```python
def get_goal_line_multiplier(goal_line_share: float) -> float:
    if goal_line_share >= 75.0:
        return 1.15  # Primary goal-line back (many TDs)
    elif goal_line_share >= 50.0:
        return 1.10  # Strong goal-line role
    elif goal_line_share >= 25.0:
        return 1.05  # Shared role
    else:
        return 1.00  # Limited goal-line work
```

**Dependencies:** None (but related to Metric 7: Red Zone Opportunity)

**Cost:** $0 (PFR free)

---

## 7. Recommendation

**Should we pursue this metric?**

- [x] **PURSUE** - High RB value, medium-hard implementation

**Rationale:**

**Value:** ⭐⭐⭐⭐⭐ (Very High for RBs)
- Best TD predictor for RBs
- Separates TD-dependent RBs from yardage RBs
- Critical for RB committees

**Feasibility:** ⭐⭐ (Medium-Hard)
- Requires per-player PFR scraping (more complex than single-page scraping)
- Situational stats harder to extract
- 2-3 days implementation

**Historical Data:** ⭐⭐⭐⭐ (Good)
- ✅ Available via PFR splits
- ✅ Predictive

**Maintenance:** ⭐⭐⭐ (Medium)
- PFR structure changes may break scraper
- Requires player ID mapping

**Preferred Data Source:** **Pro Football Reference** (player splits pages)

**Implementation Priority:** Medium-High (after easier metrics)

**Next Steps:**
1. Map RB player names to PFR player IDs
2. Scrape PFR splits pages for goal-line carries
3. Calculate goal-line share (RB carries / team carries at goal line)
4. Apply multiplier: High share (75%+) = 1.15x, Low (<25%) = 1.00x

**Example Impact:**
```
Christian McCaffrey (80% goal-line share): 1.15x multiplier (primary TD scorer)
Committee RB (20% goal-line share): 1.00x multiplier (TD-dependent on long runs)
```

**Blockers:** Per-player scraping complexity (need player ID mapping)

**Timeline:** 2-3 days

---

## Research Completeness Checklist

- [x] All 7 sections completed
- [x] Position applicability (RB)
- [x] Alternatives researched (PFR, PlayerProfiler)
- [x] Historical data assessed (YES - PFR splits)
- [x] Schema defined
- [x] Recommendation (PURSUE - medium-hard)
- [x] Dependencies (None)
- [x] Effort estimated (2-3 days)

---

## Related Metrics

- Metric 7: Red Zone Opportunity (MEDIUM priority) - Broader than goal-line
- Metric 49: Role Designation (RB Workload) - Related to goal-line role

**Notes:**
- Goal-line role is subset of red zone opportunity (inside 5 vs inside 20)
- More specific = Better TD predictor
- Per-player scraping more complex than single-page scraping

---

## Lifecycle Notes

**Data Source Stability:** High (PFR stable)
**Deprecation Risk:** Low (situational stats are standard)
**Replacement Strategy:** Primary: PFR splits, Fallback: PlayerProfiler or estimation

---

*Research conducted: 2025-12-20*
*Next review: After implementation*
