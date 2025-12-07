# Player Fetcher Optimization

## Objective

Reduce player-data-fetcher runtime from ~15 minutes to ~2 minutes by replacing per-player API calls with a single bulk API call, matching the approach used by historical-data-compiler.

---

## High-Level Requirements

### 1. Bulk API Fetching

- **Current**: Makes ~1500 individual API calls via `_get_all_weeks_data()`
- **Target**: Make ONE bulk API call that returns all players with all weekly stats
- **Pattern**: Copy approach from `historical_data_compiler/player_data_fetcher.py:150-188`

### 2. Weekly Data Extraction

- **Current**: `_calculate_week_by_week_projection()` calls API per player
- **Target**: Extract weekly data from bulk response (already fetched)
- **Pattern**: Use `_extract_weekly_points()` approach from historical data compiler

### 3. Maintain Existing Functionality

- All existing output fields must be preserved
- Output CSV format unchanged

### 4. Code Cleanup

- Remove unused SKIP_DRAFTED_PLAYER_UPDATES functionality
- Remove unused USE_SCORE_THRESHOLD functionality
- Delete orphaned methods after refactoring

---

## Resolved Questions

### Algorithm/Logic Questions

1. **SKIP_DRAFTED_PLAYER_UPDATES optimization:** RESOLVED - REMOVE
   - Decision: Delete entirely - hasn't been used, won't be used again
   - Remove: `SKIP_DRAFTED_PLAYER_UPDATES` constant, `drafted_player_ids` tracking, related code blocks

2. **USE_SCORE_THRESHOLD optimization:** RESOLVED - REMOVE
   - Decision: Delete entirely - hasn't been used, won't be used again
   - Remove: `USE_SCORE_THRESHOLD` constant, `low_score_player_data` tracking, related code blocks

### Architecture Questions

3. **`_get_all_weeks_data()` method:** RESOLVED - DELETE
   - Decision: Delete entirely - no fallback needed
   - Remove the method completely after refactoring

### Testing Questions

4. **Testing strategy:** RESOLVED
   - **Decision:** Both diff comparison AND specific test cases
   - Diff: Compare old vs new CSV output
   - Test cases: Verify specific players, DST scores, bye weeks

### Edge Cases (API Verified)

5. **Bye week handling:** VERIFIED
   - Bulk API returns gaps for bye weeks (missing weeks in stats array)
   - Same handling as current code - no changes needed

6. **DST negative scores:** VERIFIED
   - Bulk API returns negative `appliedTotal` for DST (83 negative scores found in test)
   - Historical-data-compiler pattern handles this: `if position == 'DST' or actual_points > 0`

7. **Missing data players:** VERIFIED
   - Stats array returns empty for players with no data
   - Handled gracefully - returns 0 points

---

## Resolved Implementation Details

### The Bulk Fetch Approach

**Decision:** Use same endpoint with `scoringPeriodId=0` and `limit: 1500` filter
**Reasoning:** This is exactly what historical-data-compiler does, proven to work
**Source:** `historical_data_compiler/player_data_fetcher.py:170-182`

**Implementation:**
```python
# Build API URL
url = ESPN_FANTASY_API_URL.format(year=year)

# Request params - scoringPeriodId=0 means "all weeks"
params = {
    "view": "kona_player_info",
    "scoringPeriodId": 0  # 0 = all weeks in one response
}

# Headers with bulk player filter (get top 1500 by ownership)
headers = {
    "User-Agent": ESPN_USER_AGENT,
    "X-Fantasy-Filter": f'{{"players":{{"limit":{ESPN_PLAYER_LIMIT},"sortPercOwned":{{"sortPriority":4,"sortAsc":false}}}}}}'
}

data = await self.http_client.get(url, headers=headers, params=params)
```

### Weekly Points Extraction

**Decision:** Extract from `player_info.get('stats', [])` in bulk response
**Reasoning:** Stats array already contains all weekly data, no need for additional API calls
**Source:** `historical_data_compiler/player_data_fetcher.py:395-464`

**Implementation:**
```python
# Stats are already in the bulk response
stats = player_info.get('stats', [])

for stat in stats:
    season_id = stat.get('seasonId')
    scoring_period = stat.get('scoringPeriodId')
    stat_source = stat.get('statSourceId')  # 0=actual, 1=projected
    applied_total = stat.get('appliedTotal')

    # Extract actual vs projected points per week
    if stat_source == 0:  # Actual game scores
        actual_points[scoring_period] = applied_total
    elif stat_source == 1:  # Projections
        projected_points[scoring_period] = applied_total
```

---

## Implementation Notes

### Files to Modify
- `player-data-fetcher/espn_client.py` - Main refactoring target
  - Modify initial fetch to include all weekly stats (`scoringPeriodId=0`)
  - Refactor `_calculate_week_by_week_projection()` to read from bulk data
  - **DELETE:** `_get_all_weeks_data()` method
  - **DELETE:** `SKIP_DRAFTED_PLAYER_UPDATES` constant and related code
  - **DELETE:** `USE_SCORE_THRESHOLD` constant and related code
  - **DELETE:** `drafted_player_ids` and `low_score_player_data` tracking

### Dependencies
- No new dependencies required
- Uses same ESPN API endpoints, just different parameters

### Reusable Code
- `historical_data_compiler/player_data_fetcher.py` - Reference for:
  - Bulk fetch parameters (lines 170-182)
  - Weekly points extraction (lines 395-464)
  - Stats parsing logic

### Testing Strategy
- **Comparison test**: Run both old and new versions, compare output CSVs
- **Performance test**: Measure runtime improvement
- **Edge cases**: Bye weeks, injuries, missing data, DST negative scores

---

## Status: READY FOR IMPLEMENTATION
