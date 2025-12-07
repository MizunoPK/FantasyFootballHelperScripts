# Trade Simulator Addition - Clarifying Questions

## Objective Summary
Add three new combination options to the Trade Suggestor:
1. Two-for-one (2:1 both directions)
2. Three-for-one (3:1 both directions)
3. Three-for-two (3:2 both directions)

Fill any lost roster spots using "Add to Roster mode" logic to get top recommendations.

---

## Questions for Clarification

### 1. Current Trade Suggestor Understanding

**Q1.1:** How does the current Trade Suggestor work?
- Is it currently only doing one-for-one trades?
- Where is the code located for the Trade Suggestor?
- What file(s) implement the current trade suggestion logic?

**Q1.2:** How are trades currently assessed/scored?
- What metrics are used to evaluate if a trade is good?
- Is there a scoring system similar to the simulation system?
- Are trades ranked by some criteria?

**Q1.3:** What is the current user flow for Trade Suggestor?
- How does the user select this mode?
- What inputs does the user provide?
- What output format is generated?

### 2. Add to Roster Mode

**Q2.1:** What is "Add to Roster mode"?
- Where is this code located?
- How does it determine the "top recommendation" for a roster spot?
- Does it use the same simulation/scoring system as draft mode?

**Q2.2:** How should roster spot filling work with these new trade types?
- If I trade away 2 players for 1, I lose a net of 1 roster spot - should we suggest a waiver wire add?
- If I trade away 3 for 1, I lose 2 roster spots - should we suggest 2 waiver adds?
- Should these waiver suggestions be part of the trade assessment output?

**Q2.3:** Should the waiver wire recommendations be factored into the trade score?
- Example: Trade looks bad, but if waiver wire player is great, does it make the trade better?
- Should the assessment include "Trade + Waiver Add = Net Value"?

### 3. Trade Combinations

**Q3.1:** For two-for-one trades:
- Should we generate trades where I give 2 players for 1 opponent player? ✓
- Should we generate trades where I give 1 player for 2 opponent players? ✓
- Or both directions? (Sounds like both from the description)

**Q3.2:** For three-for-one trades:
- Same question - both directions (3 mine for 1 theirs, and 1 mine for 3 theirs)?

**Q3.3:** For three-for-two trades:
- Should we do both directions (3 mine for 2 theirs, and 2 mine for 3 theirs)?

**Q3.4:** How many combinations should we generate?
- Should we limit the number of suggested trades to avoid overwhelming the user?
- Should we only show the top N trades per combination type?

### 4. Position Constraints

**Q4.1:** Are there position-based constraints on these multi-player trades?
- Example: Can I trade 2 RBs for 1 WR, or should positions match somewhat?
- Should there be "position balance" rules (e.g., can't trade away all RBs)?

**Q4.2:** Should we prevent roster rule violations?
- If league requires minimum 2 RBs, prevent trades that would leave user with only 1 RB?
- Should we check for legal roster configurations post-trade?

### 5. User Interface / Mode Selection

**Q5.1:** How should the user select these new combination options?
- New menu items in Trade Simulator mode?
- Checkboxes for "Include 2-for-1", "Include 3-for-1", "Include 3-for-2"?
- Separate modes for each combination type?

**Q5.2:** Should these be added to existing Trade Simulator output or separate?
- Should the trade_info_*.txt files include these new combinations mixed with existing trades?
- Or should there be separate output files for each combination type?

### 6. Opponent Selection

**Q6.1:** Should these multi-player trades consider all opponent teams?
- Or can the user specify which opponent(s) to generate trades for?

**Q6.2:** Should we consider multi-team trades (3-way trades)?
- Or only trades between user and one opponent at a time?

### 7. Performance Considerations

**Q7.1:** Combinatorial explosion concerns:
- For 3-for-2 trades, with roster of 15 players each, the combinations could be huge
- Should we limit the search space? (e.g., only consider starters, or top-rated players)
- Should we use sampling rather than exhaustive search?

**Q7.2:** How should we prioritize which combinations to evaluate?
- Score players first, then only combine "tradeable" players?
- Set minimum value thresholds?

### 8. Trade Assessment with Roster Filling

**Q8.1:** Workflow clarification:
- Step 1: Generate trade (e.g., give 3 players, get 1 player)
- Step 2: Net roster loss = 2 spots
- Step 3: Use "Add to Roster" logic to find top 2 waiver wire adds
- Step 4: Assess trade value as: (Player received + 2 waiver adds) vs (3 players given)
- Is this the correct workflow?

**Q8.2:** Waiver wire data source:
- Where does the waiver wire data come from?
- Is it the same `players_projected.csv` that's used for drafting?
- Should we filter out already-rostered players?

**Q8.3:** Output format:
- Should the trade output show:
  ```
  Trade: Give [Player A, Player B, Player C]
         Get [Player X]
  Recommended Waiver Adds: [Player Y, Player Z]
  Net Assessment: [Score]
  ```
- Or something different?

### 9. Backward Compatibility

**Q9.1:** Should the existing Trade Simulator functionality remain unchanged?
- Keep current one-for-one trades working as-is?
- Add these as additional options rather than replacing current behavior?

### 10. Testing

**Q10.1:** What test scenarios should we validate?
- All 6 trade directions work correctly?
- Roster filling works for different net losses?
- Edge cases (trading away all players at a position)?

**Q10.2:** Should we create new unit tests for these features?
- Or modify existing trade simulator tests?

---

---

## ANSWERS FROM CODEBASE ANALYSIS

### Files Located:
- **Trade Simulator**: `/league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
- **Add to Roster Mode**: `/league_helper/add_to_roster_mode/AddToRosterModeManager.py`
- **Supporting Classes**: `TradeSimTeam.py`, `TradeSnapshot.py`

### Current Trade Suggestor Functionality:
- Located in `start_trade_suggestor()` method (line 209-338)
- Currently generates:
  - **1-for-1 trades** (one_for_one=True)
  - **2-for-2 trades** (two_for_two=True)
  - **3-for-3 trades** (three_for_three=False for trades, True for waivers)
- Uses `get_trade_combinations()` method (line 979-1233)
- **KEY INSIGHT**: Currently only does EQUAL trades (same number from each side)
- **NEW REQUIREMENT**: Add UNEQUAL trades (2:1, 3:1, 3:2 in both directions)

### Add to Roster Mode:
- Method: `get_recommendations()` (line 217-241)
- Gets available players: `drafted=0`, `can_draft=True`
- Scores using: `player_manager.score_player()`
- Returns top `RECOMMENDATION_COUNT` (=10) players
- Sorted by score descending

### Trade Assessment:
- Uses `TradeSnapshot` to store trade details
- Uses `TradeSimTeam` to calculate team scores
- Minimum improvement threshold: `MIN_TRADE_IMPROVEMENT = 30` points
- Both teams must improve for trade to be valid

### Position Constraints:
- MAX_POSITIONS defined in constants.py:
  - QB: 2, RB: 4, WR: 4, TE: 2, K: 1, DST: 1, FLEX: 1
  - Total MAX_PLAYERS: 15
- Validation in `_validate_roster()` (line 916-977)
- FLEX eligible: RB, WR, DST

---

## ANSWERS TO QUESTIONS

### Q1: Current Trade Suggestor Understanding
✅ **ANSWERED**: Currently does 1:1, 2:2 trades. Need to add 2:1, 1:2, 3:1, 1:3, 3:2, 2:3

### Q2: Add to Roster Mode
✅ **ANSWERED**: Uses `player_manager.get_player_list()` + `score_player()` to get top 10 available players

### Q3: Trade Combinations
✅ **CONFIRMED**: Need all 6 unequal trade directions:
- 2:1 (give 2, get 1)
- 1:2 (give 1, get 2)
- 3:1 (give 3, get 1)
- 1:3 (give 1, get 3)
- 3:2 (give 3, get 2)
- 2:3 (give 2, get 3)

### Q4: Position Constraints
✅ **ANSWERED**: Use existing `_validate_roster()` method. Already handles position limits.

### Q5: User Interface
**NEEDS USER INPUT**: How to enable new trade types? Options:
- Option A: Add checkboxes in menu for each trade type
- Option B: Always include them (might be too many combinations)
- Option C: New submenu under Trade Suggestor

### Q6: Opponent Selection
✅ **ANSWERED**: Current code analyzes all opponent teams, we'll keep that behavior

### Q7: Performance Considerations
**NEEDS USER INPUT**:
- 3:2 trades have HUGE combinations (C(15,3) × C(15,2) = 455 × 105 = 47,775 per opponent)
- Should we limit to top-scored players only to reduce search space?
- Or is performance acceptable with full search?

### Q8: Trade Assessment with Roster Filling
✅ **UNDERSTOOD**: Workflow should be:
1. Execute unequal trade (e.g., give 3, get 1)
2. Calculate net roster spots lost (e.g., -2 spots)
3. Use Add to Roster logic to find top N waiver adds
4. Display trade + recommended waiver fills
5. Include waiver recommendations in output file

### Q9: Backward Compatibility
✅ **ANSWERED**: Keep existing 1:1 and 2:2 trades working. Add new options alongside them.

### Q10: Testing
✅ **PLAN**: Modify existing `test_trade_simulator.py` to add tests for new unequal trades

---

## REMAINING QUESTIONS FOR USER

### R1: User Interface Selection Method
How should users enable/disable these new trade types?
- Always include all 6 types (might generate too many trades)?
- Add menu checkboxes to select which types to include?
- Create separate mode/submenu?
For now, just have constants defined at the top of the file for toggling the different modes that I can modify myself.


### R2: Performance/Combination Limits
Should we limit the search space for 3:2 and 3:1 trades?
- Option A: No limits, search all combinations (might be slow)
- Option B: Only consider players above certain score threshold
- Option C: Sample random combinations instead of exhaustive search
No Limits

### R3: Waiver Fill Display
How should waiver recommendations be shown in output?
- Include in main trade output file?
- Separate section at end of each trade?
- Format: "Recommended adds to fill spots: Player A, Player B"
Yes to in the main trade output file as a seperate section within the trade, but still be printing the ScoredPlayer object

### R4: Number of Recommendations
How many waiver recommendations to show per trade?
- Just the top N needed to fill roster spots?
- Show alternatives (e.g., top 3 options per empty spot)?
Just the top N needed to fill spots

---

Please answer R1-R4 so I can finalize the TODO file!
