# Offensive/Defensive Ranking Separation - TODO

## [SUMMARY] Task Overview
Refactor the player data system to separate team offensive/defensive rankings from individual player data by:
1. Creating a new teams.csv file with team-level data (rankings + opponents)
2. Removing team ranking columns from players.csv
3. Updating draft_helper and starter_helper to use the new teams.csv data structure
4. Enhancing starter_helper to consider positional rankings in score calculations

## [TARGET] Master Plan

### Phase 1: Analysis and Design
1. [OK] **Create comprehensive TODO file mapping all tasks for off/def ranking separation**
2. [OK] **Ask clarifying questions before beginning development**
3. [OK] **Analyze current offensive/defensive ranking implementation**
   - [OK] Examined current players.csv structure and ranking columns (team_offensive_rank, team_defensive_rank)
   - [OK] Reviewed ranking calculation in ESPN client (_calculate_team_rankings_from_stats method)
   - [OK] Understood data flow: ESPN API -> team_rankings dict -> individual player records
   - [OK] Found enhanced_scoring.py uses rankings for player score adjustments in draft_helper
   - [OK] Confirmed starter_helper does NOT currently use rankings (opportunity for enhancement)

### Phase 2: Data Structure Changes
4. [OK] **Create new teams.csv file structure and export logic**
   - [OK] Defined teams.csv schema: team, offensive_rank, defensive_rank, opponent
   - [OK] Created TeamData class with validation and CSV import/export methods
   - [OK] Implemented export logic in DataExporter with concurrent export support
   - [OK] Added extract_teams_from_players function to build teams from player data

5. [OK] **Update player data fetcher to generate teams.csv alongside players.csv**
   - [OK] Modified DataExporter.export_all_formats_with_teams method for concurrent export
   - [OK] Updated main data_fetcher-players.py to use new export method
   - [OK] Added extract_teams_from_players function to extract team data from player records
   - [OK] Teams.csv files are now generated in both data/ and shared_files/ directories

6. [OK] **Remove offensive/defensive ranking columns from players.csv**
   - [OK] Updated ESPNPlayerData model to exclude team_offensive_rank, team_defensive_rank fields
   - [OK] Updated FantasyPlayer class to remove team ranking fields
   - [OK] Modified export configurations to omit ranking columns from EXPORT_COLUMNS
   - [OK] Updated ESPN client to not assign team ranking fields to player objects
   - [OK] Updated draft_helper to use None for team rankings (temporary until teams.csv integration)

### Phase 3: Consumer Updates
7. [OK] **Update draft_helper to read team data from teams.csv**
   - [OK] Created TeamDataLoader class in draft_helper/team_data_loader.py
   - [OK] Added team data loading to DraftHelper.__init__() with status reporting
   - [OK] Updated calculate_score method to lookup team rankings from teams.csv
   - [OK] Integrated team data into enhanced scoring calculations with fallback behavior

8. [OK] **Update starter_helper to use positional rankings for score calculation**
   - [OK] Created PositionalRankingCalculator class with configurable adjustment factors
   - [OK] Implemented position-specific ranking logic (offensive positions use offensive rank, etc.)
   - [OK] Integrated into LineupOptimizer.calculate_adjusted_score() method
   - [OK] Added rank-based score multipliers with conservative 15% max impact
   - [OK] Tested integration - Elite teams get ~2.2% boost, Good teams get ~1.2% boost

### Phase 4: Testing and Validation
9. ? **Create and run unit tests for new team data functionality**
   - Test teams.csv file generation and export
   - Test team data loading in draft_helper and starter_helper
   - Test positional ranking calculations in starter_helper
   - Ensure all existing tests still pass

10. ? **Update documentation and configuration files**
    - Update CLAUDE.md with new teams.csv data flow
    - Update module READMEs with team data structure
    - Document new positional ranking features in starter_helper

11. ? **Test entire system end-to-end with new team data structure**
    - Run player data fetcher and verify teams.csv generation
    - Test draft_helper with team data lookups
    - Test starter_helper with positional ranking enhancements
    - Validate data consistency between players.csv and teams.csv

12. ? **Move completed file to done folder**

## [NOTE] Context Notes

### Key Decisions Made:
- teams.csv will follow same dual-location pattern as players.csv (data/ + shared_files/)
- Team rankings will be completely separated from individual player data
- starter_helper will gain new positional matchup analysis capabilities
- Maintain backward compatibility during transition

### Technical Approach:
- **Data Model**: Create new TeamData class alongside existing FantasyPlayer
- **Export Pipeline**: Extend existing export system to handle teams.csv in parallel
- **Consumer Integration**: Update both helpers to load team data separately
- **Matchup Analysis**: Implement team vs position ranking calculations in starter_helper

### Dependencies:
- Current offensive/defensive ranking calculation system
- ESPN API integration for team data
- Existing export pipeline (DataExporter class)
- Draft helper scoring algorithms
- Starter helper lineup optimization

### Assumptions:
- Current team ranking data is available and accurate in the ESPN API
- CURRENT_NFL_WEEK opponent data is available for matchup analysis
- Existing file management system (caps, cleanup) will work with teams.csv
- Both helpers can be updated without breaking existing functionality

## ? Session History

### Session 1 (2025-09-24)
- **Completed**: Task analysis, comprehensive TODO creation, clarifying questions
- **User Clarifications Received**:
  1. **Positional Ranking**: Offensive rank vs defensive rank difference, configurable scale
  2. **Data Source**: Extract ranking data from existing players.csv columns
  3. **Team Names**: Use same format as players.csv team column for both team and opponent
  4. **Score Calculation**: Multiply existing scores by rank-based factor (0.85-1.15 range)
  5. **Fallback**: Multiply by 1.0 if teams.csv missing, remove columns from players.csv completely
- **Next**: Analyze current offensive/defensive ranking implementation

## ? Progress Tracking Instructions
**CRITICAL**: Keep this file updated with progress as you complete each task. Mark tasks as complete with [OK] and add session notes. If a new Claude session needs to continue this work, this file contains all context needed to resume efficiently.