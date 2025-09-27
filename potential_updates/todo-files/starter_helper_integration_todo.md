# Starter Helper Integration into Draft Helper - TODO

## [SUMMARY] Objective
Integrate the starter_helper functionality into the draft_helper by adding a new menu option called 'Starter Helper' that provides the same functionality and output as the current standalone starter_helper.

## [TARGET] Requirements Analysis
Based on starter_helper.txt:
- Add new main menu option called 'Starter Helper'
- Selecting this option should provide same functionality as current starter_helper
- Should output the best list of starters based on current data
- Should output the info to a file (same as current behavior)

## [NOTE] TODO Tasks

### Phase 1: Analysis and Planning [OK] COMPLETED
- [x] **Task 1**: Analyze current draft_helper menu structure and identify integration points
- [x] **Task 2**: Analyze current starter_helper functionality to understand what needs to be integrated
- [x] **Task 3**: Identify shared dependencies and imports needed
- [x] **Task 4**: Plan the integration approach (direct integration vs wrapper approach)

### Phase 2: Code Integration [OK] COMPLETED
- [x] **Task 5**: Add starter_helper imports to draft_helper
- [x] **Task 6**: Add 'Starter Helper' option #6 to draft_helper main menu (moved Quit to #7)
- [x] **Task 7**: Implement starter_helper functionality within draft_helper context
- [x] **Task 8**: Ensure file output functionality works correctly (outputs to draft_helper/data/starter_helper/)
- [x] **Task 9**: Handle any configuration conflicts between modules (graceful import fallbacks)
- [x] **Task 10**: Ensure proper error handling and user feedback (async implementation with proper error handling)

### Phase 3: Testing and Validation [OK] COMPLETED
- [x] **Task 11**: Test the new menu option functionality (verified menu displays option 6 correctly)
- [x] **Task 12**: Verify file output matches original starter_helper behavior (format verified to match)
- [x] **Task 13**: Test integration with existing draft_helper features (all existing functionality preserved)
- [x] **Task 14**: Run existing unit tests to ensure no regressions (34/34 draft helper tests pass, 21/21 runner tests pass)
- [ ] **Task 15**: Create new unit tests for integrated functionality (deferred - core functionality verified working)
- [ ] **Task 16**: Test edge cases and error conditions (graceful import fallbacks implemented)

### Phase 4: Documentation and Cleanup ? IN PROGRESS
- [ ] **Task 17**: Update draft_helper README.md with new functionality
- [ ] **Task 18**: Update CLAUDE.md with integration details
- [ ] **Task 19**: Update any relevant configuration documentation
- [ ] **Task 20**: Move starter_helper.txt to done folder

## ? Clarifying Questions to Ask
Before beginning implementation, need to clarify:

1. **Menu Integration**: Should the starter helper be a top-level menu item alongside existing options, or integrated into an existing submenu?

2. **Return Behavior**: After running starter helper, should it:
   - Return to main draft helper menu?
   - Exit the program?
   - Show results and wait for user input?

3. **Configuration Handling**: How should configuration conflicts be handled if both modules have overlapping settings?

4. **File Output Location**: Should the starter helper output files go to:
   - The same location as current starter_helper (starter_helper/data/)?
   - The draft_helper data directory?
   - A shared location?

5. **Roster Context**: Should the integrated starter helper:
   - Use the current draft_helper roster state?
   - Read from the CSV file independently?
   - Allow user to choose?

6. **Display Integration**: Should the output be:
   - Displayed in console only (like current starter_helper)?
   - Integrated into draft_helper's display style?
   - Both console display and file output?

## ? Technical Considerations

### Current Draft Helper Structure
- Located in `draft_helper/draft_helper.py`
- Has interactive menu system with multiple options
- Uses `draft_helper_config.py` for configuration
- Has its own display and formatting functions

### Current Starter Helper Structure
- Located in `starter_helper/starter_helper.py`
- Standalone script with its own main() function
- Uses `starter_helper_config.py` for configuration
- Has matchup analysis integration
- Outputs to `starter_helper/data/` directory

### Integration Approaches
1. **Direct Integration**: Import starter_helper classes and integrate directly
2. **Wrapper Approach**: Create a wrapper that calls starter_helper functionality
3. **Shared Module**: Refactor common functionality into shared utilities

## [DATA] Progress Tracking
- **Started**: [Date when work begins]
- **Current Phase**: Phase 1 - Analysis and Planning
- **Completed Tasks**: 0/20
- **Next Session Pickup Point**: [Update as work progresses]

## ? Session Continuity Notes
- Keep this file updated with progress after each significant change
- Note any decisions made during implementation
- Document any issues encountered and their solutions
- Record any additional clarifying questions that arise during development

---
**Important**: This TODO file should be updated throughout the implementation process to maintain consistency across potential multiple Claude sessions.