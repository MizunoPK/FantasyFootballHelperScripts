# Waiver Simulator - Implementation Questions

**Objective**: Add "Waiver" option to Manual Trade Visualizer

**Purpose**: These questions clarify user preferences and implementation details discovered during the first verification round (3 iterations). Your answers will be integrated into the implementation plan.

---

## Question 1: Waiver Option Placement

**Context**: The "Waiver" option needs to appear in the team selection menu alongside opponent team names.

**Question**: Where should "Waiver" appear in the team selection list?

**Options**:

**A. At the top of the list**
- Description: "Waiver" appears as option #1, before all team names
- Pros: Easy to find, prominent placement
- Cons: Inconsistent with alphabetical ordering
- Example menu:
  ```
  1. Waiver
  2. Annihilators
  3. Bo-ner
  4. Chase-ing points
  ...
  ```

**B. At the bottom of the list**
- Description: "Waiver" appears after all team names
- Pros: Doesn't disrupt team list, clear separation
- Cons: Requires scrolling if many teams
- Example menu:
  ```
  1. Annihilators
  2. Bo-ner
  3. Chase-ing points
  ...
  8. Waiver
  ```

**C. Alphabetically sorted with team names**
- Description: "Waiver" sorted alphabetically (would appear near end, after teams starting with A-V)
- Pros: Consistent sorting, predictable location
- Cons: Less prominent than dedicated placement
- Example menu:
  ```
  1. Annihilators
  2. Bo-ner
  3. Chase-ing points
  ...
  7. Waiver
  8. [Last Team]
  ```

**Recommendation**: Option B (bottom) - Clear separation between real teams and waiver wire

---

## Question 2: Empty Waiver Wire Handling

**Context**: If no waiver players are available, we need to handle this gracefully.

**Question**: What should happen if the waiver wire is empty when user selects "Waiver"?

**Options**:

**A. Show "Waiver" option but display error message if selected**
- Description: "Waiver" always appears in menu, but selecting it shows "No players available on waivers" and returns to menu
- Pros: Consistent UI (option always present)
- Cons: User might waste a click

**B. Hide "Waiver" option if waiver wire is empty**
- Description: Check waiver count before building menu; only show "Waiver" if players available
- Pros: Cleaner UI, prevents wasted clicks
- Cons: Requires checking waivers before menu display

**C. Show "Waiver (0 players)" when empty**
- Description: Always show option but indicate availability in the label
- Pros: User knows status without clicking
- Cons: Selecting it still shows error message
- Example: `8. Waiver (0 players available)`

**Recommendation**: Option B (hide if empty) - Following DRY principle, check once and handle cleanly

---

## Question 3: Waiver Player Filtering

**Context**: The waiver optimizer filters players using `Constants.MIN_WAIVER_IMPROVEMENT` (default: 5 points) to exclude very low-scoring players. This is calculated as: `lowest_roster_score + MIN_WAIVER_IMPROVEMENT`.

**Question**: Should waiver players be filtered by minimum score threshold for manual trades?

**Options**:

**A. Yes, use same filtering as waiver optimizer**
- Description: Only show waiver players who score above `(lowest_roster_score + 5 points)`
- Pros: Reduces clutter, focuses on viable pickups
- Cons: User can't see all available players
- Implementation: Use existing pattern from `start_waiver_optimizer()` line 238-240

**B. No, show all waiver players regardless of score**
- Description: Show every undrafted player (drafted=0)
- Pros: Complete transparency, user has full control
- Cons: May show many low-value players

**C. Make it optional (ask user each time)**
- Description: When "Waiver" selected, ask "Show all players or filtered list?"
- Pros: Maximum flexibility
- Cons: Extra UI step, more complex

**Recommendation**: Option A (filtered) - Consistent with waiver optimizer behavior, reduces noise

---

## Question 4: Optional Waiver Filtering

**Context**: Related to Question 3 - if we implement filtering, should it be toggleable?

**Question**: Should users be able to toggle waiver filtering on/off?

**Options**:

**A. No, always use MIN_WAIVER_IMPROVEMENT filter**
- Description: Hardcode the filtering behavior
- Pros: Simple implementation, consistent with waiver optimizer
- Cons: Less flexible

**B. Yes, add a prompt to enable/disable filtering**
- Description: After selecting "Waiver", ask "Filter low-scoring players? (Y/N)"
- Pros: User control, can see all players if desired
- Cons: Extra UI step

**C. Yes, but only if filtered list is empty**
- Description: Try filtered first, if no results, ask if user wants to see unfiltered list
- Pros: Smart fallback, prevents empty results
- Cons: More complex logic

**Recommendation**: Option A (no toggle) - Keep it simple, match waiver optimizer behavior

**Note**: If you selected Option B or C for Question 3, this question may not apply.

---

## Question 5: Waiver Team Name

**Context**: The waiver optimizer uses team name "Waiver Wire". This name appears in trade displays and output files.

**Question**: Should we reuse "Waiver Wire" or allow customization?

**Options**:

**A. Reuse "Waiver Wire" (hardcoded)**
- Description: Use same name as waiver optimizer: `TradeSimTeam("Waiver Wire", waiver_players, ...)`
- Pros: Consistency across modes, simple
- Cons: Not customizable

**B. Allow custom name via input**
- Description: Prompt user to enter name when selecting Waiver option
- Pros: Flexibility, user preference
- Cons: Extra UI step, complicates flow

**C. Use a constant that's easily configurable**
- Description: Define `WAIVER_TEAM_NAME = "Waiver Wire"` in constants.py for easy modification
- Pros: Configurable without code changes
- Cons: Requires editing constants file

**Recommendation**: Option A (hardcoded "Waiver Wire") - Consistency is more valuable than customization here

---

## Summary

**Total Questions**: 5

**Grouped by Category**:
- UI/UX: Questions 1, 2
- Filtering: Questions 3, 4
- Naming: Question 5

**Impact on Implementation**:
- Questions 1-2 affect `TradeSimulatorModeManager.start_manual_trade()` UI code
- Questions 3-4 affect waiver player retrieval logic
- Question 5 affects TradeSimTeam initialization

**Next Steps**:
After you provide answers, I will:
1. Update the TODO file with your decisions (rules.txt Step 4)
2. Execute second verification round - 3 more iterations (rules.txt Step 5)
3. Begin implementation (rules.txt Step 6+)
