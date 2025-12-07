# Phase 6 & 7: File Reorganization and Modularity Improvements

## Overview
Break up large files (>800 lines) into smaller, focused modules to improve readability and maintainability.

## Target Files

### 1. TradeSimulatorModeManager.py (1,098 lines) - PRIORITY 1
**Current Issues:**
- Single file handling display, input parsing, trade analysis, and file I/O
- Hard to test individual components
- Difficult to navigate and understand

**Proposed Refactoring:**
Split into 5 modules in `league_helper/trade_simulator_mode/`:

1. **TradeSimulatorModeManager.py** (~250 lines) - Main orchestration
   - `__init__`, `run_interactive_mode`, `init_team_data`
   - `start_waiver_optimizer`, `start_trade_suggestor`, `start_manual_trade`
   - Delegates to helper classes

2. **trade_display_helper.py** (~200 lines) - NEW
   - `TradeDisplayHelper` class
   - `display_numbered_roster()`
   - `display_combined_roster()`
   - `display_trade_result()`

3. **trade_input_parser.py** (~250 lines) - NEW
   - `TradeInputParser` class
   - `parse_player_selection()`
   - `parse_unified_player_selection()`
   - `get_players_by_indices()`
   - `split_players_by_team()`

4. **trade_analyzer.py** (~300 lines) - NEW
   - `TradeAnalyzer` class
   - `get_trade_combinations()`
   - `validate_roster()`
   - `count_positions()`

5. **trade_file_writer.py** (~150 lines) - NEW
   - `TradeFileWriter` class
   - `save_manual_trade_to_file()`
   - `save_trades_to_file()`
   - `save_waiver_trades_to_file()`

**Benefits:**
- Each module has single responsibility
- Easier to test individual components
- Better code organization
- Improved maintainability

**Testing Strategy:**
- Existing tests continue to work with TradeSimulatorModeManager
- Add new unit tests for each helper class

---

### 2. PlayerManager.py (890 lines) - PRIORITY 2
**Current Issues:**
- Handles player loading, scoring, projections, and team management
- Many responsibilities in one class

**Proposed Refactoring:**
Split into 3 modules in `league_helper/util/`:

1. **PlayerManager.py** (~400 lines) - Core player management
   - Loading players from CSV
   - Basic player access methods
   - Main orchestration

2. **player_scoring.py** (~300 lines) - NEW
   - `PlayerScoringCalculator` class
   - `get_weekly_projection()`
   - `calculate_player_score()`
   - All scoring-related logic

3. **player_ranking.py** (~200 lines) - NEW
   - `PlayerRankingEngine` class
   - Ranking and sorting logic
   - ADP calculations

**Testing Strategy:**
- Existing PlayerManager tests remain
- Add targeted tests for scoring and ranking modules

---

### 3. espn_client.py (1,009 lines) - PRIORITY 3
**Current Issues:**
- Large API client with many endpoint methods
- Mix of low-level HTTP and high-level data fetching

**Proposed Refactoring:**
Split into modules in `player-data-fetcher/`:

1. **espn_client.py** (~300 lines) - Base HTTP client
   - HTTP request handling
   - Authentication
   - Error handling

2. **espn_endpoints.py** (~400 lines) - NEW
   - Endpoint URL builders
   - Query parameter construction

3. **espn_data_fetcher.py** (~300 lines) - NEW
   - High-level data fetching methods
   - Data transformation
   - Pagination handling

**Note:** Lower priority as API clients are less critical for core business logic.

---

### 4. FantasyTeam.py (795 lines) - PRIORITY 4
**Current Issues:**
- Handles roster management, lineup optimization, and scoring

**Proposed Refactoring:**
Consider splitting if patterns emerge during testing/review.
May be acceptable size given its central role.

---

## Implementation Order

1. ✅ Phase 5: Complete comprehensive testing (DONE - 802 tests)
2. 🔄 Phase 6/7: Refactor TradeSimulatorModeManager (IN PROGRESS)
3. ⏭️ Phase 6/7: Refactor PlayerManager
4. ⏭️ Phase 6/7: Consider espn_client refactoring
5. ⏭️ Phase 8: Final deduplication verification
6. ⏭️ Phase 9: Documentation updates

## Success Criteria

- All 802 existing tests continue to pass
- New modules are <400 lines each
- Each module has single, clear responsibility
- No functionality changes (refactoring only)
- Maintains backward compatibility
