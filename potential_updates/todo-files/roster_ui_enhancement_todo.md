# Roster UI Enhancement - TODO

## Task Overview
Enhance the Add to Roster Mode in the draft helper to display the roster in ideal draft order based on the DRAFT_ORDER configuration. When entering Add to Roster Mode, the system should show each round's ideal position and which player (if any) is currently assigned to that round slot.

## Requirements Summary
- Display roster by draft round order (1-15) instead of by position grouping
- Show each round's ideal position based on DRAFT_ORDER config
- Show which player currently occupies each round slot
- Make it clear which rounds match the ideal strategy vs deviations
- Integrate this enhanced display into the Add to Roster Mode entry point

## Current System Analysis
**Current Behavior** (in `draft_helper.py`):
- `display_roster_by_draft_order()` shows roster grouped by position type (QB, RB, WR, etc.)
- `run_add_to_roster_mode()` shows recommendations but no enhanced roster view
- DRAFT_ORDER config exists but isn't used for display

**Files to Modify:**
- `draft_helper/draft_helper.py` - Main implementation
- `draft_helper/draft_helper_config.py` - Configuration reference
- Unit tests in `draft_helper/tests/` - Test coverage for new functionality

## Master Plan

### Phase 1: Analysis and Design
1. ? Analyze current DRAFT_ORDER configuration structure and mapping
2. ? Understand how roster players are currently tracked and assigned
3. ? Design the new round-by-round display format and layout
4. ? Ask clarifying questions about specific display requirements

### Phase 2: Core Implementation
5. ? Create new function `display_roster_by_draft_rounds()` in DraftHelper class
6. ? Implement logic to map DRAFT_ORDER config to round-by-round display
7. ? Add functionality to match current roster players to their ideal round slots
8. ? Create clear display format showing ideal vs actual for each round
9. ? Handle empty slots and position flexibility (FLEX, multiple options per round)

### Phase 3: Integration
10. ? Modify `run_add_to_roster_mode()` to call new roster display function
11. ? Ensure the enhanced display appears when entering Add to Roster Mode
12. ? Test integration with existing Add to Roster workflow
13. ? Verify compatibility with current roster management functions

### Phase 4: Testing and Validation
14. ? Create unit tests for new `display_roster_by_draft_rounds()` function
15. ? Test with empty roster (all rounds empty)
16. ? Test with partially filled roster (some rounds filled)
17. ? Test with full roster (all rounds occupied)
18. ? Test with FLEX players and position flexibility
19. ? Run all existing unit tests to ensure no regressions
20. ? Manual testing of Add to Roster Mode workflow

### Phase 5: Documentation and Cleanup
21. ? Update CLAUDE.md with new roster display functionality
22. ? Update any relevant README files
23. ? Update configuration documentation if needed
24. ? Update rules files to reflect new functionality
25. ? Move roster_ui.txt to 'done' folder in potential_updates

## Technical Implementation Details

### DRAFT_ORDER Configuration Structure
```python
# From draft_helper_config.py
DRAFT_ORDER = [
    {FLEX: 1.0, QB: 0.7},    # Round 1
    {FLEX: 1.0, QB: 0.7},    # Round 2
    {FLEX: 1.0, QB: 0.8},    # Round 3
    # ... continues for 15 rounds
]
```

### Proposed Display Format
```
Current Roster by Draft Round:
=====================================
Round 1 (Ideal: FLEX): [Player Name] (Actual: RB) - 285.5 pts ?
Round 2 (Ideal: FLEX): [Empty]
Round 3 (Ideal: FLEX): [Player Name] (Actual: WR) - 245.2 pts ?
Round 4 (Ideal: FLEX): [Player Name] (Actual: QB) - 315.1 pts [WARNING]
Round 5 (Ideal: QB): [Empty]
...
Round 15 (Ideal: FLEX): [Player Name] (Actual: DST) - 95.5 pts [WARNING]

Legend: ? = Matches ideal position, [WARNING] = Different from ideal
Total: 10/15 rounds filled
```

### Function Interface Design
```python
def display_roster_by_draft_rounds(self):
    """
    Display current roster organized by draft round order based on DRAFT_ORDER config.
    Shows ideal position for each round and actual player assigned.
    """
    pass

def get_ideal_position_for_round(self, round_num: int) -> str:
    """
    Get the ideal position for a given draft round based on DRAFT_ORDER.
    Returns position with highest priority for that round.
    """
    pass

def match_players_to_rounds(self) -> Dict[int, Optional[FantasyPlayer]]:
    """
    Map current roster players to their most appropriate draft round slots.
    Returns dictionary mapping round numbers to players.
    """
    pass
```

### Key Design Decisions Needed
1. **Round Assignment Logic**: How to assign current players to specific rounds?
   - Option A: Assign based on draft order of addition (first added = Round 1)
   - Option B: Assign based on optimal fit to ideal positions
   - Option C: Allow manual round assignment

2. **FLEX Position Handling**: How to display rounds with multiple viable positions?
   - Show primary position (highest weight) as "ideal"
   - Show all viable positions with weights
   - Use special notation for flexible rounds

3. **Empty Slot Display**: How to show rounds without assigned players?
   - Show "[Empty]" with ideal position
   - Show available position options
   - Highlight priority rounds that need filling

## Risk Assessment and Mitigation

### Potential Risks
- **Display Complexity**: Round-by-round format might be overwhelming with 15 rounds
- **Assignment Logic**: Unclear how to map existing players to specific rounds
- **FLEX Handling**: Complex logic needed for position flexibility
- **Performance**: Additional computation for round mapping

### Mitigation Strategies
- Start with simple, clear display format and iterate
- Implement robust round assignment algorithm with fallbacks
- Handle FLEX positions with clear primary/secondary notation
- Optimize round mapping logic for performance

## Success Criteria
- [OK] Add to Roster Mode shows enhanced round-by-round roster display
- [OK] Each round shows ideal position from DRAFT_ORDER config
- [OK] Current players are clearly mapped to appropriate rounds
- [OK] Empty rounds are clearly indicated with ideal positions
- [OK] Display helps users understand draft strategy adherence
- [OK] All existing functionality continues to work unchanged
- [OK] Comprehensive test coverage for new functionality
- [OK] Clear documentation of new features

## Design Decisions (CONFIRMED)

1. **Round Assignment Method**: Option B - Based on optimal fit to DRAFT_ORDER strategy
   - Assign players to rounds where their position best matches the ideal position
   - Use scoring/weighting logic to determine best fit for each player

2. **FLEX Position Display**: Option A - Show only the highest weighted position
   - Display the position with the highest weight as "Ideal: [POSITION]"
   - Keep display clean and simple

3. **Empty Round Priority**: Option A - Simple "[Empty]" display
   - Show "[Empty]" with ideal position for unfilled rounds
   - Clean, straightforward display without complexity

4. **Integration Timing**: Option A - Every time entering Add to Roster Mode
   - Replace current roster display with enhanced round-by-round view
   - Becomes the new standard roster display for Add to Roster Mode

## Progress Tracking

**IMPORTANT**: Keep this file updated with progress as tasks are completed. Mark completed tasks with [OK] and add any discovered issues or changes to the plan.

**Current Status**: Ready to begin after clarifying questions are answered
**Last Updated**: [Date when progress is made]
**Completed Tasks**: 0/25
**Phase**: Analysis and Design (Pending clarifying questions)

This comprehensive plan addresses all aspects of implementing the roster UI enhancement while maintaining system reliability and following the established development protocols.