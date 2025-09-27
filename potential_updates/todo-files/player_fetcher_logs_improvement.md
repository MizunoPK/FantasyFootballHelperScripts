# Player Data Fetcher Logs Improvement - TODO

## [SUMMARY] Task Overview
Improve the player data fetcher logging system to be more readable with progress tracking that shows percentage completion and estimated remaining time.

## [TARGET] Specific Requirements
- **More readable logs**: Enhance formatting and structure of log messages
- **Progress tracking**: Add percentage completion display
- **ETA calculation**: Show estimated remaining time for completion
- **New log level**: Add level between INFO and WARNING for progress tracking

## [NOTE] Master Plan

### Phase 1: Analysis and Design
1. [OK] **Analyze current logging system** - Understand current implementation
2. ? **Ask clarifying questions** - Get details before implementation
3. ? **Design progress tracking system** - Plan ETA calculation approach
4. ? **Design new log level and formatting** - Plan readable log structure

### Phase 2: Implementation
5. ? **Create progress tracking class** - Implement ETA and percentage calculation
6. ? **Add custom log level** - Create PROGRESS level between INFO and WARNING
7. ? **Update player data fetcher** - Integrate progress tracking
8. ? **Enhance log formatting** - Make logs more readable
9. ? **Update configuration** - Add logging configuration options

### Phase 3: Testing and Validation
10. ? **Create unit tests** - Test progress tracking and logging functionality
11. ? **Run existing unit tests** - Ensure no regressions
12. ? **Integration testing** - Test with actual player data fetcher run
13. ? **Performance testing** - Ensure logging doesn't impact performance

### Phase 4: Documentation and Cleanup
14. ? **Update README files** - Document new logging features
15. ? **Update CLAUDE.md** - Update technical documentation
16. ? **Update configuration docs** - Document new logging options
17. ? **Move files to done folder** - Complete the update process

## ? Context Notes
- **Current Status**: Just fixed team rankings and CSV column preservation issues
- **Related Files**:
  - `player-data-fetcher/data_fetcher-players.py` - Main fetcher script
  - `player-data-fetcher/player_data_fetcher_config.py` - Configuration
  - `player-data-fetcher/espn_client.py` - API client with existing logging
- **Logging Framework**: Currently uses Python's `logging` module
- **Performance**: Player data fetcher currently takes 8-15 minutes for ~646 players

## ? Session History
### Current Session
- **Completed**: Analysis of requirements from player_fetcher_logs.txt
- **Notes**: Need to understand current logging structure before implementing
- **Next**: Ask clarifying questions and analyze current implementation

## [OK] Requirements Clarification (COMPLETED)
1. **Progress Format**: `"Fetched 287/646 players (44.4%) - ETA: 7m 18s"`
2. **Update Frequency**: Every 10 players processed
3. **ETA Calculation**: Based on recent performance (last 50 players) for accuracy
4. **Scope**: Both full runs and limited runs with automatic detection
5. **Log Level**: PROGRESS level separately configurable in config file

## [TARGET] Success Criteria
- [ ] Logs show clear, readable progress updates
- [ ] Percentage completion is accurate and updates appropriately
- [ ] ETA calculation is reasonable and updates as performance changes
- [ ] New logging doesn't significantly impact fetcher performance
- [ ] All existing functionality continues to work
- [ ] Unit tests cover new logging functionality
- [ ] Documentation is updated to reflect changes

---
**Note**: Keep this file updated with progress made in case a new Claude session needs to continue the work.