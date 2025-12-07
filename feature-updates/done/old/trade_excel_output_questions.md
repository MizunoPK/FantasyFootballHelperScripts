# Trade Excel Output - Implementation Questions

**Objective**: Add Excel file export for Manual Trade Visualizer

**Purpose**: These questions clarify user preferences and implementation details discovered during the first verification round (3 iterations). Your answers will be integrated into the implementation plan.

---

## Question 1: Excel File Location

**Context**: The txt file is saved to `./league_helper/trade_simulator_mode/trade_outputs/`. Excel file needs a save location.

**Question**: Where should the Excel file be saved?

**Options**:

**A. Same directory as txt file (recommended)**
- Description: Save to `./league_helper/trade_simulator_mode/trade_outputs/trade_info_{name}_{timestamp}.xlsx`
- Pros: Easy to find both files together, consistent organization
- Cons: None identified
- Pattern: Follows existing convention

**B. Separate Excel subdirectory**
- Description: Save to `./league_helper/trade_simulator_mode/trade_outputs/excel/trade_info_{name}_{timestamp}.xlsx`
- Pros: Separates file types
- Cons: User must check two locations, adds complexity

**Recommendation**: Option A (same directory) - Simplicity and consistency
Option A


---

## Question 2: Excel Creation Behavior

**Context**: User has already confirmed "Save this trade to a file? (y/n)". Should Excel be automatic or require additional prompt?

**Question**: Should Excel file creation be automatic or optional?

**Options**:

**A. Always create Excel alongside txt (recommended)**
- Description: When user says 'y' to save, create both txt and xlsx automatically
- Pros: No extra prompts, user gets both formats
- Cons: User gets Excel even if they don't want it (minimal downside)
- Implementation: One code path, simpler

**B. Add separate prompt for Excel**
- Description: After saving txt, ask "Also save as Excel? (y/n)"
- Pros: User control over file types
- Cons: Extra UI step, more code complexity

**C. Make configurable via league_config.json**
- Description: Add `"EXPORT_EXCEL": true/false` setting
- Pros: User can set preference once
- Cons: Adds configuration complexity

**Recommendation**: Option A (always create) - User already confirmed save, both formats are useful

Answer: Option A

---

## Question 3: Sheet Names

**Context**: Excel file will have 4 sheets. Need to define names.

**Question**: What should the sheet names be?

**Options**:

**A. Descriptive names (recommended)**
- Description: "Summary", "Initial Rosters", "Final Rosters", "Detailed Calculations"
- Pros: Clear purpose, easy to navigate
- Cons: Longer names
- User-friendly: High

**B. Short names**
- Description: "Summary", "Before", "After", "Details"
- Pros: Shorter tabs
- Cons: Less descriptive
- User-friendly: Medium

**C. Technical names**
- Description: "Trade_Summary", "Pre_Trade_Rosters", "Post_Trade_Rosters", "Score_Breakdown"
- Pros: Unambiguous, no spaces
- Cons: Less readable, underscores awkward
- User-friendly: Low

**Recommendation**: Option A (descriptive names) - Excel handles long sheet names well, clarity is more important

Answer: Option A

---

## Question 4: Waiver Recommendations in Final Rosters

**Context**: TradeSnapshot includes waiver recommendations when trade loses roster spots. Should these appear in Final Rosters sheet?

**Question**: Should waiver recommendations be included in the Final Rosters sheet?

**Options**:

**A. Yes, as separate section (recommended)**
- Description: Show regular roster, then add section "Recommended Waiver Adds" below
- Pros: Complete picture of post-trade team state, helpful for user
- Cons: Sheet becomes longer
- Implementation: Add blank row separator, then waiver section

**B. No, only show actual roster**
- Description: Final Rosters shows only confirmed players, not recommendations
- Pros: Cleaner sheet, focused on trade itself
- Cons: Missing helpful information

**C. Separate sheet for waivers**
- Description: Create 5th sheet "Waiver Recommendations"
- Pros: Cleanly separated concerns
- Cons: More sheets to navigate, overkill for optional data

**Recommendation**: Option A (include as section) - Keeps related information together, matches txt file format

Answer: Option A

---

## Question 5: Highlighting Traded Players

**Context**: In Final Rosters sheet, some players are new (traded in), some stayed. Should we visually distinguish them?

**Question**: Should traded players be highlighted or marked?

**Options**:

**A. Add marker column (recommended)**
- Description: Add column "Status" with values like "Received", "Kept", "Dropped"
- Pros: Clear indication, sortable, works in all Excel versions
- Cons: Extra column
- Example:
  ```
  Player    Position  Score   Status
  Player1   RB        95.5    Received
  Player2   WR        88.2    Kept
  ```

**B. Use background color highlighting**
- Description: Apply green background to received players, red to dropped players
- Pros: Visual impact, no extra column
- Cons: Requires openpyxl conditional formatting, may not display consistently
- Complexity: Higher

**C. No marking**
- Description: Just list all players without distinction
- Pros: Simplest implementation
- Cons: User can't easily see what changed

**Recommendation**: Option A (marker column) - Simple, reliable, sortable, universal compatibility

Answer: Option A

---

## Question 6: Detailed Calculations Format

**Context**: Requirement says "show detailed calculations for each player, showing their starting projected points, each multiplier and associated threshold that got applied, and the final number."

**Question**: How detailed should the Detailed Calculations sheet be?

**Options**:

**A. Parse and extract numeric values (recommended)**
- Description: Parse `ScoredPlayer.reason` strings to extract multipliers (e.g., "ADP: EXCELLENT (1.5x)" → extract "1.5x")
- Pros: Clean numeric columns, can do math/analysis
- Cons: Parsing complexity, format may vary
- Columns: Player | Base Points | ADP Mult | Rating Mult | Team Mult | ... | Final Score
- Example: `Player1 | 20.5 | 1.5x | 1.2x | 1.1x | ... | 40.5`

**B. Show raw reason strings**
- Description: Put each `ScoredPlayer.reason` string in its own column
- Pros: No parsing needed, guaranteed accurate
- Cons: Less useful for analysis, not numeric
- Columns: Player | Reason1 | Reason2 | Reason3 | ...
- Example: `Player1 | Base: 20.5 | ADP: EXCELLENT (1.5x) | ...`

**C. Combined: both numeric and text**
- Description: Show parsed multipliers AND original reason strings
- Pros: Best of both worlds
- Cons: Very wide sheet (20+ columns per player)
- Complexity: High

**Recommendation**: Option A (parse numeric values) - More useful for analysis, matches user request for "calculations"

Answer: Option A

**Implementation Note**: Parsing will use regex to extract patterns like:
- "Base Projected Points: 20.5" → extract 20.5
- "ADP: EXCELLENT (1.5x)" → extract 1.5
- "Team Quality: GOOD (1.2x)" → extract 1.2

---

## Summary

**Total Questions**: 6

**Grouped by Category**:
- File Management: Questions 1-2
- Excel Structure: Questions 3-6

**Impact on Implementation**:
- Questions 1-2 affect file I/O code location and logic
- Question 3 affects sheet creation code
- Questions 4-5 affect Final Rosters sheet structure
- Question 6 affects Detailed Calculations parsing logic

**Next Steps**:
After you provide answers, I will:
1. Update the TODO file with your decisions (rules.txt Step 4)
2. Execute second verification round - 3 more iterations (rules.txt Step 5)
3. Begin implementation (rules.txt Step 6+)
