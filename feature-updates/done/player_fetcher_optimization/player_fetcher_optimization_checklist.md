# Player Fetcher Optimization - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `player_fetcher_optimization_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Root cause identified:** Per-player API calls (~1500) vs single bulk call
- [x] **Solution approach:** Adopt bulk fetch pattern from historical-data-compiler
- [x] **Reference implementation:** `historical_data_compiler/player_data_fetcher.py`

---

## Algorithm/Logic Questions

- [x] **SKIP_DRAFTED_PLAYER_UPDATES:** ~~How to handle this optimization with bulk fetch?~~
  - **RESOLVED:** Remove entirely - hasn't been used, won't be used again

- [x] **USE_SCORE_THRESHOLD:** ~~How to handle low-score player preservation?~~
  - **RESOLVED:** Remove entirely - hasn't been used, won't be used again

---

## Architecture Questions

- [x] **`_get_all_weeks_data()` method:** ~~Keep, deprecate, or delete?~~
  - **RESOLVED:** Delete entirely - no fallback needed

- [x] **`_calculate_week_by_week_projection()` method:** How to refactor?
  - Must change from making API call to reading from already-fetched bulk data
  - Need to pass weekly stats through to this method
  - **RESOLVED:** Will be refactored to read from bulk data (or deleted if logic merged elsewhere)

---

## Data Flow

### Current Flow (slow)
```
1. Initial bulk fetch → get player list (no weekly stats)
2. For each player (~1500 times):
   a. Call _calculate_week_by_week_projection()
   b. Which calls _get_all_weeks_data() → API call
   c. Parse response for weekly points
3. Aggregate results
```

### Target Flow (fast)
```
1. Single bulk fetch → get ALL players with ALL weekly stats
2. For each player in response (~1500 iterations, NO API calls):
   a. Extract weekly points from stats array
   b. Calculate projections from extracted data
3. Aggregate results
```

- [x] **Current flow documented**
- [x] **Target flow documented**

---

## Testing & Validation

- [x] **Validation method:** How to confirm output is identical?
  - **RESOLVED:** Both - diff comparison AND specific test cases

- [x] **Performance measurement:** How to verify speed improvement?
  - Measure total runtime before/after

---

## Edge Cases

- [x] **Bye week handling:** ~~Ensure bye weeks still handled correctly~~
  - **VERIFIED:** Bulk API returns gaps for bye weeks (missing weeks in stats array)
  - Test: 37 players had 1 missing week each (their bye week)

- [x] **Injury status:** Injury data present in player_info
  - Extracted via `player_info.get('injuryStatus')` - same as current code

- [x] **DST negative scores:** ~~Ensure defense can still have negative scores~~
  - **VERIFIED:** 83 negative DST scores found in bulk response
  - Examples: Ravens D/ST Week 5: -1.0 pts, Broncos D/ST Week 9: -3.0 pts

- [x] **Missing data:** ~~Players with no stats (rookies, practice squad)~~
  - **VERIFIED:** Stats array returns empty for players with no data - handled gracefully

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player list | ESPN Fantasy API bulk fetch | Will be in same call |
| Weekly actual points | `stats[].appliedTotal` where `statSourceId=0` | From bulk response |
| Weekly projected points | `stats[].appliedTotal` where `statSourceId=1` | From bulk response |
| ADP | `ownership.averageDraftPosition` | Already in current response |
| Player ratings | `rankings` object | Already in current response |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Root cause | Per-player API calls (1500x) vs bulk (1x) | Today |
| Solution approach | Adopt historical-data-compiler pattern | Today |
| SKIP_DRAFTED_PLAYER_UPDATES | Remove entirely - unused | Today |
| USE_SCORE_THRESHOLD | Remove entirely - unused | Today |
| `_get_all_weeks_data()` | Delete entirely | Today |
| Testing validation | Both diff comparison AND specific test cases | Today |
| Bye week handling | Verified - gaps in stats array | Today |
| DST negative scores | Verified - 83 negative scores found in API | Today |
| Missing data players | Verified - empty stats handled gracefully | Today |
