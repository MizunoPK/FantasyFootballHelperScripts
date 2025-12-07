# Manual Trade Visualizer - Clarifying Questions

## General Workflow Questions

### Q1: Player Selection Input Format
When the user enters player numbers (e.g., "2,12"), should we:
- Accept spaces after commas? (e.g., "2, 12" or "2,12")
- Accept ranges? (e.g., "2-5" to select players 2, 3, 4, 5)
- What should happen with invalid input (letters, out-of-range numbers)?
- Should we allow the user to cancel/go back at the selection step?

**Answer:**
Accept spaces, no ranges, if invalid just ask again, and if the user types 'exit' then go back to the menu

---

### Q2: Roster Display Format
When displaying numbered rosters, what information should be shown for each player?
- Player name, position, team (like trade suggestor output)?
- Should we show projected points or scores?
- Should we show any special indicators (locked players, injured players)?
- Format preference: numbered list similar to menu selections?

**Answer:**
Use the standard __str__ for the FantasyPlayer and have a numbered list like menu selections

---

### Q3: Validation Requirements
What validations are needed for manual trades?
- Should we validate position limits (like the automated trade combinations)?
- Should we enforce team size limits?
- Should we allow uneven trades (1-for-2, 2-for-3, etc.)?
- Should we warn if a trade makes the team worse?

**Answer:**
Use the same validation as the waiver optimization and trade suggestor. You can refactor those sections to turn code into shared functions if any code were to be copied over to the manual trade visualizer

---

### Q4: Trade Impact Display
When showing trade results, should we display:
- The same format as Trade Suggestor (my improvement, their improvement)?
- Individual player scores/projections?
- Position-by-position breakdown?
- Just the overall team score change?

**Answer:**
Same format and functions as the waiver and trades

---

### Q5: Save to File Behavior
When saving trade results:
- Should we use the same file as Trade Suggestor (`trade_info.txt`)?
- Should we append to existing file or overwrite?
- Should we include a timestamp or trade type label?
- Should we save in a different location/file for manual trades?

**Answer:**
Different file for the trade visualizer. Have the name of the file be 'trade_info_{other team name}_{timestamp}.txt

---

### Q6: Multiple Trade Analysis
Should the user be able to:
- Analyze multiple different trades in one session?
- Compare multiple trade options before saving?
- Or just analyze one trade, save/skip, and return to menu?

**Answer:**
one trade, save/skip, and return to menu

---

### Q7: User Experience Details
For the interactive flow:
- Should we show the current team score before selecting players?
- Should we confirm the trade before calculating (show "You give X, you receive Y - proceed? y/n")?
- Should we allow the user to go back and change their selections?
- What should happen if no valid opponent teams exist?

**Answer:**
No, no, no, and if that''s the case then just print an error and go back to the Trade Simulator menu

---

### Q8: Error Handling
How should we handle edge cases:
- User selects same player multiple times in input?
- User selects all their players (empty roster)?
- Opponent team has no tradeable players?
- Trade would violate roster constraints?

**Answer:**
For any of these cases, just alert the user of the issue and go back to the Trade Simulator menu

---

### Q9: Integration with Existing Code
Should manual trade visualizer:
- Reuse the same `get_trade_combinations` logic (with custom inputs)?
- Or bypass that and directly create a single TradeSnapshot?
- Should it count as "mutually beneficial" or just show any trade?

**Answer:**
It should show any trade regardly of being mutually beneficial. You can bypass the get_trade_combinations and do the single trade calculations and TradeSnapshot creation seperately from it, but still reuse as much other functions as you can

---

### Q10: Locked Players
Should locked players (locked=True):
- Be excluded from display?
- Be shown but not selectable?
- Be allowed in manual trades?

**Answer:**
They are allowed in manual trades

---

## Implementation Priority Questions

### Q11: Testing Requirements
What level of testing is expected:
- Unit tests for each helper method?
- Integration test for complete flow?
- Mock user input for testing?
- What test coverage is required?

**Answer:**
All of the above. Greater than 80% test coverage at least

---

### Q12: Feature Completeness
Are there any additional features needed:
- Ability to save favorite trades?
- Trade history tracking?
- Comparison with automated suggestions?
- Any other functionality beyond the basic flow described?

**Answer:**
Not at this time

---
