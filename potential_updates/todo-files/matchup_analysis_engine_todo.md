# Matchup Analysis Engine - TODO

## Task Overview
Implement a Matchup Analysis Engine integrated into the starter_helper module to provide weekly opponent matchup ratings for each position. This will help identify favorable/unfavorable starts by analyzing team defense rankings, recent performance trends, and positional matchup data from ESPN APIs.

## Requirements Summary
- Add matchup ratings (1-10 scale) for each roster player vs opposing defense
- Integrate with existing starter_helper workflow via toggle control
- Use ESPN APIs for team defense statistics and schedule data
- Enhance lineup recommendations with matchup factors
- Maintain backward compatibility and minimal performance impact
- Add comprehensive configuration options and validation

## Current System Analysis
**Current Behavior** (in `starter_helper/`):
- `starter_helper.py` generates optimal lineups using CSV-based projections only
- `lineup_optimizer.py` optimizes based on fantasy points and penalties
- `starter_helper_config.py` contains basic configuration and penalties
- No opponent matchup analysis currently implemented

**Files to Modify:**
- `starter_helper/starter_helper_config.py` - Add matchup analysis configuration
- `starter_helper/lineup_optimizer.py` - Integrate matchup factors into optimization
- `starter_helper/starter_helper.py` - Add matchup analysis display and integration
- Unit tests in `starter_helper/tests/` - Test coverage for new functionality

**Files to Create:**
- `starter_helper/espn_matchup_client.py` - ESPN defense stats API client
- `starter_helper/matchup_analyzer.py` - Matchup rating calculations
- `starter_helper/matchup_models.py` - Data models for matchup data
- `starter_helper/tests/test_matchup_analyzer.py` - Matchup analysis tests
- `starter_helper/tests/test_espn_matchup_client.py` - ESPN client tests

## Master Plan

### Phase 1: Research and Planning
1. ? Ask clarifying questions about ESPN endpoints and implementation preferences
2. ? Research specific ESPN team defense statistics endpoints
3. ? Research ESPN schedule/matchup data endpoints
4. ? Test ESPN API response formats and identify data structure
5. ? Analyze existing ESPN client patterns from player-data-fetcher module

### Phase 2: Core Data Models and Configuration
6. ? Create `matchup_models.py` with Pydantic models for:
   - Team defense statistics
   - Matchup ratings
   - Weekly schedules and opponents
   - Historical performance data
7. ? Update `starter_helper_config.py` with matchup analysis settings:
   - Feature toggle controls
   - Matchup weight factors and thresholds
   - ESPN API configuration
   - Display and output options
8. ? Add configuration validation for new matchup settings

### Phase 3: ESPN API Integration
9. ? Create `espn_matchup_client.py` with async ESPN API client:
   - Team defense statistics fetching
   - Weekly schedule and opponent lookup
   - Retry logic and error handling
   - Rate limiting and caching strategies
10. ? Implement specific API endpoints:
    - Team defense stats (fantasy points allowed by position)
    - Current week NFL schedule and matchups
    - Recent game logs for defensive trends
11. ? Add data caching and performance optimization

### Phase 4: Matchup Analysis Engine
12. ? Create `matchup_analyzer.py` with core analysis functions:
    - Calculate 1-10 matchup ratings for players vs opponent defense
    - Analyze recent defensive performance trends (last 3-4 weeks)
    - Factor in home/away advantages
    - Create composite matchup scores
13. ? Implement matchup rating algorithm with configurable weights:
    - Opponent fantasy points allowed vs position (40%)
    - Recent defensive trends vs position (30%)
    - Home/away advantage (15%)
    - Strength of schedule adjustment (15%)
14. ? Add matchup analysis for all fantasy positions (QB, RB, WR, TE, K, DST)

### Phase 5: Starter Helper Integration
15. ? Enhance `lineup_optimizer.py` to include matchup factors:
    - Add matchup ratings to player scoring algorithm
    - Integrate with existing FLEX optimization logic
    - Maintain backward compatibility when matchup analysis disabled
    - Add configurable matchup weight factor (default 15%)
16. ? Update `starter_helper.py` to display matchup information:
    - Show matchup ratings in lineup recommendations
    - Add favorable/unfavorable matchup indicators
    - Display opponent defensive rankings and trends
    - Create optional detailed matchup analysis output
17. ? Ensure feature toggle works properly (ENABLE_MATCHUP_ANALYSIS)

### Phase 6: Testing and Validation
18. ? Create comprehensive unit tests for matchup functionality:
    - Test `matchup_analyzer.py` rating calculations
    - Test `espn_matchup_client.py` API integration with mocks
    - Test integration with `lineup_optimizer.py`
    - Test configuration validation and error handling
19. ? Run all existing starter_helper tests to ensure no regressions
20. ? Test performance impact and ESPN API rate limit compliance
21. ? Test feature toggle functionality (on/off scenarios)
22. ? Validate matchup ratings with manual verification

### Phase 7: Documentation and Configuration
23. ? Update `README.md` with matchup analysis features and configuration
24. ? Update `CLAUDE.md` with new starter_helper capabilities
25. ? Update configuration documentation for new matchup settings
26. ? Add troubleshooting section for ESPN API issues
27. ? Document matchup rating algorithm and calculation details

### Phase 8: Final Integration and Cleanup
28. ? Run complete functional testing of enhanced starter_helper
29. ? Verify integration works with existing CSV-based projections
30. ? Test with real roster data and validate recommendations
31. ? Ensure all unit tests pass (existing and new)
32. ? Move `matchup_analysis_engine.txt` to done folder in potential_updates

## Technical Implementation Details

### ESPN API Endpoints to Research
```python
# Potential ESPN endpoints for matchup analysis
TEAM_DEFENSE_STATS = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics"
NFL_SCHEDULE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
FANTASY_DEFENSE = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{league_id}"
TEAM_GAME_LOGS = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
```

### Configuration Structure
```python
# New settings to add to starter_helper_config.py
ENABLE_MATCHUP_ANALYSIS = True        # Toggle matchup analysis on/off
MATCHUP_WEIGHT_FACTOR = 0.15          # Impact on recommendations (0.0-1.0)
RECENT_WEEKS_FOR_DEFENSE = 4          # Weeks for defensive trend analysis
SHOW_MATCHUP_DETAILS = True           # Display matchup ratings in output
MATCHUP_RATING_THRESHOLD = 7.0        # Threshold for "favorable" matchup
HOME_FIELD_ADVANTAGE = 0.5            # Bonus points for home games
CACHE_DEFENSE_STATS_HOURS = 12        # Cache defense stats duration
```

### Matchup Rating Algorithm Design
```python
def calculate_matchup_rating(player_position, opponent_team, recent_weeks=4):
    """
    Calculate 1-10 matchup rating for player vs opponent defense

    Factors:
    - Opponent fantasy points allowed vs position (40%)
    - Recent defensive trends vs position (30%)
    - Home/away advantage (15%)
    - Strength of schedule adjustment (15%)

    Returns: Float 1.0-10.0 (10 = most favorable matchup)
    """
```

### Integration Points
- **lineup_optimizer.py**: Add matchup_rating to player scoring
- **starter_helper.py**: Display matchup indicators in output
- **starter_helper_config.py**: Add all matchup-related configuration
- **Tests**: Comprehensive coverage for all new functionality

## Key Design Decisions

1. **ESPN API Integration**: Use existing patterns from player-data-fetcher module
2. **Toggle Control**: Feature must be easily enabled/disabled via configuration
3. **Performance**: Minimal impact on existing starter_helper performance
4. **Backward Compatibility**: All existing functionality must work unchanged when disabled
5. **Caching Strategy**: Cache defense stats to minimize ESPN API calls
6. **Rating Scale**: Use 1-10 scale for easy understanding (10 = most favorable)
7. **Weight Factor**: Default 15% impact on recommendations (configurable)

## Risk Assessment and Mitigation

### Potential Risks
- **ESPN API Changes**: Endpoints may change or become unavailable
- **Performance Impact**: Additional API calls may slow down starter_helper
- **Data Accuracy**: Incorrect matchup ratings could lead to poor recommendations
- **Configuration Complexity**: Too many options may confuse users

### Mitigation Strategies
- **Graceful Fallback**: System works without matchup data when APIs unavailable
- **Async Implementation**: Non-blocking API calls with timeout handling
- **Conservative Algorithm**: Conservative rating approach with transparent calculations
- **Clear Documentation**: Comprehensive configuration guides and examples

## Success Criteria
- [OK] Provides accurate 1-10 matchup ratings for all roster players
- [OK] Integrates seamlessly with existing starter_helper workflow
- [OK] Toggle control enables/disables feature cleanly
- [OK] Minimal performance impact (<2 second additional processing time)
- [OK] Clear matchup indicators in lineup recommendations
- [OK] ESPN API integration follows existing patterns and error handling
- [OK] Comprehensive unit test coverage (>90% for new code)
- [OK] All existing tests continue to pass
- [OK] Complete documentation of new functionality

## Progress Tracking

**IMPORTANT**: Keep this file updated with progress as tasks are completed. Mark completed tasks with [OK] and add any discovered issues or changes to the plan.

**Current Status**: Ready to begin after clarifying questions are answered
**Last Updated**: [Date when progress is made]
**Completed Tasks**: 0/32
**Phase**: Research and Planning (Pending clarifying questions)

## User Requirements (CONFIRMED)

Based on user feedback:

1. **ESPN API Strategy**: Use ESPN_data_report.md to determine most efficient endpoints for required data
2. **Matchup Weight Impact**: Start with 15% weight factor (configurable)
3. **Performance Priority**: Prioritize accuracy over speed - acceptable to take time for better results
4. **Display Options**: Both simple and detailed views with toggle control
5. **Cache Strategy**: Skip cache implementation - starter_helper runs only weekly
6. **Rating Scale**: Use granular 1-100 scale for precision

## ESPN Endpoint Analysis (Based on ESPN_data_report.md)

**Available for Matchup Analysis:**

### NFL Scores API (Team Performance Data)
- **Base URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl`
- **Team Statistics**: Available in competition data with statistics arrays
- **Schedule Data**: Current week matchups via `/scoreboard` endpoint
- **Historical Performance**: Team statistics from recent games

### Fantasy Football API (Defensive Metrics)
- **Base URL**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/{scoring_format}`
- **Defense Players**: Negative IDs (e.g., -16001 for Falcons D/ST)
- **Fantasy Points Allowed**: Via stats array in defense player data
- **Weekly Performance**: Available through weekly scoringPeriodId

### Optimal Data Collection Strategy
1. **Team Defense Stats**: Use Fantasy API with defense player IDs to get fantasy points allowed by position
2. **Current Week Schedule**: Use NFL Scores API `/scoreboard` for opponent identification
3. **Recent Performance Trends**: Use Fantasy API with recent weeks (week-4 to current week)
4. **Home/Away Context**: Available in NFL Scores API competition data

This comprehensive plan addresses all aspects of implementing the matchup analysis engine while maintaining system reliability and following the established development protocols.