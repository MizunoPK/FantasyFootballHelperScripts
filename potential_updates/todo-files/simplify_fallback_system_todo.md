# Simplify Fallback System - TODO Progress Tracker

**Objective**: Eliminate all fallback methods except week-by-week projections to fix data consistency bugs like the Ulysses Bentley IV case.

**UPDATED REQUIREMENT**: fantasy_points should only reflect projected points for remaining games in the season (future weeks), not include already finished games.

**Progress Update Instructions**: Keep this file updated with detailed progress as tasks are completed. Mark completed tasks with [OK] and add implementation details.

---

## Phase 1: Remove Data Method Column Entirely [OK] COMPLETED

### 1.1 Remove data_method field from ESPNPlayerData model [OK] COMPLETED
- **File**: `player-data-fetcher/player_data_models.py`
- **Action**: Removed `data_method: str = "weekly"` field from ESPNPlayerData class
- **Status**: [OK] COMPLETED

### 1.2 Remove data_method field from FantasyPlayer model [OK] COMPLETED
- **File**: `shared_files/FantasyPlayer.py`
- **Action**: Removed `data_method: str = "weekly"` field from FantasyPlayer class
- **Action**: Removed `data_method=str(data.get('data_method', 'unknown'))` from from_dict method
- **Status**: [OK] COMPLETED

---

## Phase 2: Remove All Fallback Methods from espn_client.py ? IN PROGRESS

### 2.1 Remove _calculate_remaining_season_projection method [OK] COMPLETED
- **File**: `player-data-fetcher/espn_client.py`
- **Lines**: ~196-238
- **Action**: Completely removed the method and all its logic
- **Status**: [OK] COMPLETED

### 2.2 Remove _apply_empirical_adp_mapping method [OK] COMPLETED
- **File**: `player-data-fetcher/espn_client.py`
- **Lines**: 993-1037 (removed entire method)
- **Action**: Removed entire method that applied ADP estimation to zero-point players
- **Status**: [OK] COMPLETED

### 2.3 Remove _build_position_adp_mappings method [OK] COMPLETED
- **File**: `player-data-fetcher/espn_client.py`
- **Lines**: 1039-1052 (removed entire method)
- **Action**: Removed method that built position-specific ADP mappings
- **Status**: [OK] COMPLETED

### 2.4 Remove _estimate_fantasy_points_from_adp method [OK] COMPLETED
- **File**: `player-data-fetcher/espn_client.py`
- **Lines**: 1130-1161 (removed entire method)
- **Action**: Removed method that estimated fantasy points from ADP
- **Status**: [OK] COMPLETED

### 2.5 Remove supporting ADP helper methods [OK] COMPLETED
- **Methods**: `_group_players_by_position`, `_create_position_mapping`, `_calculate_correlation`
- **Action**: Removed all supporting methods for ADP mapping (lines 1054-1129)
- **Status**: [OK] COMPLETED

---

## Phase 3: Simplify Main Processing Loop [OK] COMPLETED

### 3.1 Remove fallback variables and logic [OK] COMPLETED
- **File**: `player-data-fetcher/espn_client.py`
- **Action**: Removed `fallback_used`, `fallback_type` variables from main loop
- **Action**: Removed all conditional fallback logic (lines 820-878 simplified)
- **Action**: Removed data_method mapping logic
- **Status**: [OK] COMPLETED

### 3.2 Simplify fantasy_points assignment [OK] COMPLETED
- **File**: `player-data-fetcher/espn_client.py`
- **Action**: Replaced complex fallback chain with single line:
  ```python
  fantasy_points = await self._calculate_week_by_week_projection(id, name, position)
  ```
- **UPDATED**: Modified to only include remaining season projections (current + future weeks)
- **Status**: [OK] COMPLETED

### 3.3 Update week-by-week calculation for remaining season only [OK] COMPLETED
- **File**: `player-data-fetcher/espn_client.py`
- **Method**: `_calculate_week_by_week_projection`
- **Action**: Modified to only sum remaining weeks (`start_week = CURRENT_NFL_WEEK`, includes current + future)
- **Changes**: Updated method description, removed USE_WEEK_BY_WEEK_PROJECTIONS check, updated logging
- **Status**: [OK] COMPLETED

### 3.4 Remove data_method parameter from ESPNPlayerData creation [OK] COMPLETED
- **File**: `player-data-fetcher/espn_client.py`
- **Action**: Removed data_method parameter from ESPNPlayerData constructor (line 876)
- **Status**: [OK] COMPLETED

**Phase 3 Summary**: Successfully simplified main processing loop to use ONLY remaining season week-by-week projections. fantasy_points now represents current week + future weeks potential, not past performance.

---

## Phase 4: Update Configuration Settings ? PENDING

### 4.1 Remove USE_REMAINING_SEASON_PROJECTIONS ? PENDING
- **File**: `player-data-fetcher/player_data_fetcher_config.py`
- **Action**: Remove setting entirely
- **Status**: ? PENDING

### 4.2 Remove USE_WEEK_BY_WEEK_PROJECTIONS toggle ? PENDING
- **File**: `player-data-fetcher/player_data_fetcher_config.py`
- **Action**: Remove setting (always enabled now)
- **Status**: ? PENDING

### 4.3 Remove ADP-related constants ? PENDING
- **File**: `player-data-fetcher/player_data_fetcher_config.py`
- **Constants to remove**:
  - `MIN_PLAYERS_PER_POSITION_MAPPING`
  - `MIN_ADP_RANGE_THRESHOLD`
  - `MIN_FANTASY_POINTS_BOUND_FACTOR`
  - `MAX_FANTASY_POINTS_BOUND_FACTOR`
  - `UNCERTAINTY_ADJUSTMENT_FACTOR`
  - `RECENT_WEEKS_FOR_AVERAGE`
- **Status**: ? PENDING

### 4.4 Update configuration validation ? PENDING
- **File**: `player-data-fetcher/player_data_fetcher_config.py`
- **Action**: Remove validation logic for removed settings
- **Status**: ? PENDING

---

## Phase 5: Update fantasy_points_calculator.py ? PENDING

### 5.1 Remove ADP estimation methods ? PENDING
- **File**: `shared_files/fantasy_points_calculator.py`
- **Methods**: `_estimate_from_adp`, `_extract_historical_fallback`
- **Status**: ? PENDING

### 5.2 Remove historical fallback logic ? PENDING
- **File**: `shared_files/fantasy_points_calculator.py`
- **Action**: Simplify to only week-by-week extraction
- **Status**: ? PENDING

### 5.3 Update FantasyPointsConfig ? PENDING
- **File**: `shared_files/fantasy_points_calculator.py`
- **Action**: Remove ADP and historical fallback configuration options
- **Status**: ? PENDING

---

## Phase 6: Remove Data Export References ? PENDING

### 6.1 Update player_data_exporter.py ? PENDING
- **File**: `player-data-fetcher/player_data_exporter.py`
- **Action**: Remove data_method from export logic and CSV headers
- **Status**: ? PENDING

### 6.2 Update any references in other files ? PENDING
- **Action**: Search codebase for remaining data_method references
- **Status**: ? PENDING

---

## Phase 7: Testing and Validation ? PENDING

### 7.1 Run comprehensive testing ? PENDING
- **Action**: Run existing unit tests to ensure no regressions
- **Expected**: All 241 tests should still pass
- **Status**: ? PENDING

### 7.2 Test specifically with Ulysses Bentley IV ? PENDING
- **Action**: Verify that he now has consistent data (fantasy_points = sum of weekly points)
- **Expected**: Either all zeros or consistent week-by-week data
- **Status**: ? PENDING

### 7.3 Test with high-profile players ? PENDING
- **Action**: Verify top players still have accurate week-by-week data
- **Expected**: fantasy_points = sum(weekly_points) for all players
- **Status**: ? PENDING

### 7.4 Create/update unit tests ? PENDING
- **Action**: Remove tests for deleted fallback methods
- **Action**: Add tests for simplified system
- **Status**: ? PENDING

---

## Phase 8: Documentation Updates ? PENDING

### 8.1 Update CLAUDE.md ? PENDING
- **File**: `CLAUDE.md`
- **Action**: Remove references to fallback methods and data_method
- **Action**: Update data source priority chain documentation
- **Status**: ? PENDING

### 8.2 Update module READMEs ? PENDING
- **Files**: `player-data-fetcher/README.md`
- **Action**: Remove fallback documentation
- **Action**: Update expected outcomes section
- **Status**: ? PENDING

### 8.3 Update configuration documentation ? PENDING
- **Action**: Remove references to deleted configuration settings
- **Status**: ? PENDING

---

## Phase 9: Finalization ? PENDING

### 9.1 Run final data fetcher test ? PENDING
- **Action**: Execute `run_player_data_fetcher.py` and verify clean results
- **Expected**: All players have consistent data, no field swapping
- **Status**: ? PENDING

### 9.2 Move objective to done folder ? PENDING
- **Action**: Move `simplify_fallback_system.txt` to `potential_updates/done/`
- **Status**: ? PENDING

---

## Progress Summary

- [OK] **Completed**: 3 tasks (data_method removal, one fallback method removal)
- ? **In Progress**: 1 task (removing remaining fallback methods)
- ? **Pending**: 23+ tasks across configuration, testing, documentation

## Next Steps

1. Continue removing fallback methods from espn_client.py
2. Simplify main processing loop
3. Update configuration settings
4. Test thoroughly before finalizing

## Notes

- This file should be updated after each major task completion
- Keep detailed implementation notes for future reference
- Test thoroughly at each phase to catch issues early