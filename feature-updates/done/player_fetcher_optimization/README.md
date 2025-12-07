# Player Fetcher Optimization - Work in Progress

## What This Is

Optimization of the player-data-fetcher to reduce runtime from ~15 minutes to ~2 minutes by adopting the bulk API approach already used by the historical-data-compiler.

## Why We Need This

1. **Performance**: Current runtime of ~15 minutes is unacceptable for routine data updates
2. **API Efficiency**: Making ~1500 individual API calls wastes resources and risks rate limiting
3. **Proven Pattern**: The historical-data-compiler already demonstrates a 2-minute solution

## Scope

**IN SCOPE:**
- Refactoring `espn_client.py` to use bulk API fetching
- Eliminating per-player API calls in `_get_all_weeks_data()`
- Extracting weekly data from bulk response (like historical-data-compiler)

**OUT OF SCOPE:**
- Changing output CSV format
- Adding new data fields
- Modifying other fetchers (scores, game data)

## Current Status: IMPLEMENTATION COMPLETE

All code changes implemented and verified. All 2161 tests pass (100%).

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context for future agents |
| `player_fetcher_optimization_notes.txt` | Original scratchwork notes from user |
| `player_fetcher_optimization_specs.md` | Main specification with detailed requirements |
| `player_fetcher_optimization_checklist.md` | Tracks open questions and decisions |
| `player_fetcher_optimization_todo.md` | Implementation tracking (ALL TASKS COMPLETE) |
| `player_fetcher_optimization_code_changes.md` | Documentation of all code changes |
| `player_fetcher_optimization_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Root Cause Analysis

The performance difference comes from API call patterns:

**Historical Data Compiler (fast, ~2 min):**
- ONE API call with `scoringPeriodId=0` and `limit: 1500` in X-Fantasy-Filter
- Returns ALL ~1500 players with ALL weekly stats in single response
- `_extract_weekly_points()` reads from already-fetched `player_info.get('stats', [])`

**Player Data Fetcher (slow, ~15 min):**
- Initial bulk call gets player list with basic info
- Then calls `_calculate_week_by_week_projection()` for EACH player (~1500 times)
- Which calls `_get_all_weeks_data()` making 1500 additional API calls
- Rate limiting adds 0.1-0.5s per call = ~2.5-12 minutes of delays

### Key Files

| File | Purpose |
|------|---------|
| `player-data-fetcher/espn_client.py` | Main file to modify (~2000 lines) |
| `historical_data_compiler/player_data_fetcher.py` | Reference implementation (540 lines) |

### Key Methods to Refactor

| Current Method | Lines | Issue |
|----------------|-------|-------|
| `_get_all_weeks_data()` | 436-510 | Makes per-player API call |
| `_calculate_week_by_week_projection()` | 394-434 | Calls above for each player |

## What's Resolved
- Root cause identified (per-player API calls vs bulk)
- Reference implementation exists (historical-data-compiler)
- Both use same ESPN API endpoint, just different filter parameters
- **SKIP_DRAFTED_PLAYER_UPDATES**: Remove entirely (unused)
- **USE_SCORE_THRESHOLD**: Remove entirely (unused)
- **`_get_all_weeks_data()`**: Delete entirely (no fallback needed)
- **Testing**: Both diff comparison AND specific test cases
- **Edge cases verified against ESPN API**:
  - DST negative scores: 83 found in test (e.g., Ravens D/ST Week 5: -1.0 pts)
  - Bye weeks: Handled as gaps in stats array
  - Missing data: Empty stats handled gracefully

## What's Still Pending
None - all checklist items resolved. Ready for implementation.

## How to Continue This Work

1. Read `player_fetcher_optimization_specs.md` for complete specifications
2. Read `player_fetcher_optimization_checklist.md` to see what's resolved vs pending
3. Address remaining open questions with user
4. When all items resolved: User says "Prepare for updates based on player_fetcher_optimization"
5. Follow `feature_development_guide.md` for implementation
