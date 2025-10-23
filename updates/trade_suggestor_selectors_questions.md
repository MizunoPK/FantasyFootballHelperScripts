# Trade Suggestor Selectors - Clarifying Questions

**Objective**: Add team selection and trade type selection to Trade Suggestor mode

**Status**: AWAITING USER ANSWERS

**Created**: 2025-10-19

---

## Questions About Trade Type Selection

### Q1: Trade Type Display Format
The specification lists trade types as "1:1,1:2,2:1,2:2,3:2,2:3,3:3". Should these be displayed as:
- Option A: "1:1" (colon separator)
- Option B: "1-for-1" (descriptive format, matches existing display code)
- Option C: "1 for 1" (space separator)

**Recommendation**: Use "1-for-1" format to match existing code patterns in Manual Trade Visualizer (line 612: `trade_type = f"{len(my_selected_players)}-for-{len(their_selected_players)}"`)

### Q2: Trade Type Menu Options - Should We Include 3-for-3?
The specification lists 7 trade types (1:1, 1:2, 2:1, 2:2, 3:2, 2:3, 3:3), but the current code has `ENABLE_THREE_FOR_THREE = False` (line 51).

Should we:
- Option A: Include "3-for-3" in the selection menu (user can choose but might be slow)
- Option B: Exclude "3-for-3" entirely (keep disabled, only show 6 options)
- Option C: Include but add a warning about performance

**Current Behavior**: 3-for-3 disabled in Waiver Optimizer (line 259: "# Disabled: too many combinations")

**Recommendation**: Include in menu with performance warning, or exclude entirely?

### Q3: Default Trade Type Selection
When the trade type selection menu is shown, should any types be selected by default?

- Option A: No defaults - user must explicitly select
- Option B: Default to 1:1 and 2:2 (most common, matches current ENABLE_* constants)
- Option C: Default to all types except 3:3

**Current Behavior**: Code currently enables 1:1, 2:2, 2:1, 1:2 by default (lines 49-62)

### Q4: Trade Type Selection Validation
What should happen if the user doesn't select any trade types?

- Option A: Show error message and re-prompt
- Option B: Return to main menu (cancel operation)
- Option C: Default to 1:1 trades only

**Recommendation**: Show error and re-prompt (consistent with other input validation)

---

## Questions About Team Selection

### Q5: Team Selection - Cancel Behavior
When the user selects "Cancel" on the team selection menu, should the system:
- Option A: Return to Trade Simulator main menu (consistent with Manual Trade Visualizer line 550-552)
- Option B: Exit Trade Simulator entirely
- Option C: Show error and re-prompt

**Current Manual Trade Visualizer Behavior**: Returns to menu with message "Trade cancelled." (lines 550-552)

**Recommendation**: Match Manual Trade Visualizer behavior (Option A)

### Q6: Team Display Order
How should opponent teams be displayed in the selection menu?

- Option A: Alphabetical order (matches Manual Trade Visualizer line 541)
- Option B: By team score (highest first)
- Option C: Random/original order

**Current Manual Trade Visualizer Behavior**: Alphabetical order (line 541: `sorted(self.opponent_simulated_teams, key=lambda t: t.name)`)

**Recommendation**: Use alphabetical order to match existing pattern

---

## Questions About Implementation

### Q7: Configuration Constants - Should They Change?
The current code uses global ENABLE_* constants (lines 49-62) to control trade types. After adding user selection, should we:

- Option A: Keep constants as "maximum allowed" - user can only select from enabled types
- Option B: Ignore constants entirely - user selection overrides
- Option C: Use constants as defaults for the selection menu

**Recommendation**: Use constants as defaults (Option C) - provides flexibility while maintaining current behavior

### Q8: Performance Warning Display
Some trade type combinations can be very slow (e.g., 3-for-3, 3-for-2). Should we:

- Option A: Display estimated combinations before starting analysis
- Option B: Show warning only for slow types (3-for-3, 3-for-2, 2-for-3)
- Option C: No warnings - just analyze

**Current Behavior**: Code logs expected combinations (lines 398-403) but doesn't warn user before starting

**Recommendation**: Display estimated combinations and show warning if > 100,000 combinations?

### Q9: Save File Naming
When saving trade results with single team filter, should the filename include:

- Option A: Team name in filename (e.g., `trade_suggestor_TeamA_2025-10-19.txt`)
- Option B: Original naming (timestamp only)
- Option C: Include both team and selected trade types

**Current Behavior**: Timestamped files only (check `trade_file_writer.py` for format)

### Q10: Error Handling - No Valid Trades Found
If no trades are found with the selected team/types, should the system:

- Option A: Display "No trades found" and return to Trade Simulator menu
- Option B: Display message and re-prompt for different selections
- Option C: Display message and ask if user wants to try different team/types

**Current Behavior**: Returns to menu with message (line 433: "No mutually beneficial trades found.")

**Recommendation**: Match current behavior (Option A)

---

## Questions About User Experience

### Q11: Trade Type Selection - Display Format
How should the 7 trade type options be displayed?

```
Option A (Simple):
1. 1-for-1
2. 1-for-2
3. 2-for-1
4. 2-for-2
5. 2-for-3
6. 3-for-2
7. 3-for-3

Option B (With descriptions):
1. 1-for-1 (I give 1 player, I receive 1 player)
2. 1-for-2 (I give 1 player, I receive 2 players)
...

Option C (Grouped by balance):
Equal Trades:
  1. 1-for-1
  4. 2-for-2
  7. 3-for-3
Unequal Trades (I receive more):
  2. 1-for-2
  5. 2-for-3
Unequal Trades (I give more):
  3. 2-for-1
  6. 3-for-2
```

**Recommendation**: Option B - helpful for users to understand trade types

### Q12: Input Format for Trade Type Selection
The spec says "comma separated list like when the user is selecting multiple players in the Trade Visualizer". Should we accept:

- Option A: Numbers only (e.g., "1,2,4")
- Option B: Numbers or ranges (e.g., "1-3,5" means 1,2,3,5)
- Option C: Allow "all" keyword

**Current Trade Visualizer Behavior**: Comma-separated numbers only (check `trade_input_parser.py`)

**Recommendation**: Match Trade Visualizer pattern (Option A)

---

## Questions About Code Organization

### Q13: Helper Method Extraction
Should the team/trade type selection logic be:

- Option A: Inline in `start_trade_suggestor()` method
- Option B: Extracted to helper methods (e.g., `_select_opponent_team()`, `_select_trade_types()`)
- Option C: Added to `TradeInputParser` class

**Recommendation**: Option B - keeps `start_trade_suggestor()` clean and testable

### Q14: Test Coverage
Should we add:

- Option A: Only unit tests for new selection logic
- Option B: Unit tests + update integration tests
- Option C: Unit tests + integration tests + manual testing guide

**Recommendation**: Option B minimum (unit + integration), Option C ideal

---

## Summary of Recommendations

Based on codebase patterns, I recommend:
1. **Q1**: Use "1-for-1" format (matches existing code)
2. **Q2**: Exclude 3-for-3 entirely (keep at 6 options) OR include with warning
3. **Q3**: Default to 1:1, 2:2, 2:1, 1:2 (matches current enables)
4. **Q4**: Show error and re-prompt
5. **Q5**: Return to menu (match Manual Trade Visualizer)
6. **Q6**: Alphabetical order (match Manual Trade Visualizer)
7. **Q7**: Use constants as defaults
8. **Q8**: Display estimated combinations, warn if > 100k
9. **Q9**: Team name in filename
10. **Q10**: Display message and return to menu
11. **Q11**: Option B - show descriptions
12. **Q12**: Comma-separated numbers only
13. **Q13**: Extract to helper methods
14. **Q14**: Unit tests + integration tests

Please review these questions and provide answers for any where you prefer a different approach than my recommendation.

---

## User Answers

*Please answer questions below - especially Q2 (include 3-for-3?) and any where you disagree with recommendations*

