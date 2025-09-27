# Fallback System Simplification - Week-by-Week Only Implementation

## [SUMMARY] Task Overview
Implement the previously requested simplification to remove ALL fallback systems except week-by-week projections. Players will get accurate week-by-week data when available, or zeros when ESPN data is unavailable. This eliminates data consistency bugs, field swapping issues, and complex maintenance overhead.

## [TARGET] Master Plan
1. [OK] Remove all fallback methods from espn_client.py
2. [OK] Simplify main processing loop to week-by-week only
3. [OK] Remove fallback configuration settings
4. [OK] Remove data_method field from all data models
5. [OK] Update shared fantasy points calculator
6. [OK] Remove ADP-related constants and logic
7. [OK] Update export columns configuration
8. [OK] Test simplified system functionality
9. ? Update documentation to reflect changes
10. [OK] Run unit tests to ensure no regressions

## [NOTE] Context Notes
- **Original Request**: Simplify to week-by-week only with zeros for missing data
- **Current Status**: All complex fallback systems still present despite being marked "done"
- **Philosophy**: Better accurate zeros than inaccurate estimates
- **Benefits**: Data consistency, simplified debugging, transparent results, reduced maintenance

## ? Technical Approach
**Week-by-Week Only Logic**:
- Use `_calculate_week_by_week_projection()` exclusively
- Remove all conditional fallback checks
- Remove `data_method` tracking (no longer needed)
- Zero values when ESPN week-by-week data unavailable

**Configuration Simplification**:
- Remove `USE_REMAINING_SEASON_PROJECTIONS`
- Remove `USE_WEEK_BY_WEEK_PROJECTIONS` (always enabled)
- Remove all ADP-related constants
- Simplify validation logic

**Data Model Updates**:
- Remove `data_method` field from ESPNPlayerData
- Remove `data_method` field from FantasyPlayer
- Update export columns to exclude data_method
- Update from_dict/to_dict methods

## ? Session History
### Session 1 (2025-01-27)
- Identified that simplification was never implemented despite being marked "done"
- Created comprehensive TODO file for implementation
- Completed: Removed all fallback systems and ADP-related code
- Simplified configuration to week-by-week only
- All unit tests passing (21/21)
- System loads and imports successfully

## [ANALYSIS] Files to Modify
- `player-data-fetcher/espn_client.py` - Remove fallback methods
- `player-data-fetcher/player_data_fetcher_config.py` - Remove fallback settings
- `player-data-fetcher/player_data_models.py` - Remove data_method field
- `shared_files/FantasyPlayer.py` - Remove data_method field
- `shared_files/fantasy_points_calculator.py` - Simplify to week-by-week only
- `player-data-fetcher/player_data_constants.py` - Remove ADP constants

## [OK] Success Criteria
- Only week-by-week projection method remains
- All fallback methods completely removed
- data_method column completely removed from all models and exports
- Simplified configuration with fewer settings
- Data consistency: fantasy_points = sum(weekly_points) for ALL players
- Players with poor ESPN data show clear zero values