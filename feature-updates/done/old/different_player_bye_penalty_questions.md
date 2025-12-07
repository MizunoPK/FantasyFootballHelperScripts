# Questions for Different Player Bye Penalty Implementation

## Clarifying Questions:

### 1. Configuration and Parameters
**Q1.1**: Should `DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY` have a default value? If so, what should it be?
- Should it be the same as `BASE_BYE_PENALTY`, lower, or higher?
- What's the reasoning behind the default value?
Answer: default to 5 for now as a very small bit of penalty but enough to compile into something larger when there are multiple overlaps

**Q1.2**: Should `DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY` be added to:
- `league_config.json` (the current league configuration file)?
- `parameters.json` (the simulation parameters file)?
- Both?
Just league_config.json and the json files used in the Simulation

**Q1.3**: For simulation testing, should this parameter:
- Be included in the parameter optimization ranges?
- Have a specific range of values to test (e.g., 0.0 to 10.0)?
- Be tested independently or in combination with `BASE_BYE_PENALTY`?
Yes have it independant of BASE_BYE_PENALTY and its values be (10, 0, 50)

### 2. Implementation Scope
**Q2.1**: You mention "PlayerManager scoring system" - should this apply to:
- Only the "Add to Roster" mode scoring?
- Also the "Trade/Waiver" mode scoring?
- Any other scoring contexts?
Have it functioning under the same 'bye' flag that the BASE_BYE_PENALTY works under. So wherever bye=True is already used in any calls to score_player, the new param will also be used

**Q2.2**: Should the penalty calculation consider:
- ALL roster positions (QB, RB, WR, TE, K, DST)?
- Only "starting" positions (excluding bench)?
- Only certain position types?
All positions

**Q2.3**: When counting "players on the team's roster whose bye week overlaps":
- Does this include ONLY drafted=2 (rostered) players?
- Should it exclude injured/reserve players?
- Should it exclude locked players?
There should be a roster list passed to the score_player function that you should reference

### 3. Penalty Application Logic
**Q3.1**: If a player being scored has bye_week=10, and the roster has:
- 2 QBs with bye_week=10 (same position)
- 1 RB with bye_week=10 (different position)
- 1 WR with bye_week=10 (different position)

Should the penalty be:
- BASE_BYE_PENALTY × 2 (for 2 same-position overlaps) + DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY × 2 (for 2 different-position overlaps)?
- Or some other calculation?

Answer: Correct

**Q3.2**: Should the player being scored be excluded from the overlap count?
- Example: If scoring a QB with bye_week=10, and another QB has bye_week=10, do we count that other QB only, or does the scored player count toward same-position overlaps?

Yes they should be excluded from overlap counts

**Q3.3**: How should FLEX position be treated?
- Is FLEX considered a "position" for overlap purposes?
- Should FLEX players be counted based on their actual position (RB/WR)?

Flex is not considered a position. They should be considered based on their actual position

### 4. Testing and Validation
**Q4.1**: Should new unit tests be created specifically for:
- The different-position penalty calculation logic?
- Edge cases (no overlaps, all overlaps, mixed overlaps)?
- Integration with existing bye week penalty tests?

Any and all unit tests

**Q4.2**: For manual testing/validation:
- Should we test with specific roster scenarios?
- Do you have expected penalty values for test cases?

Be as thourough as you can 

**Q4.3**: Should the simulation system:
- Generate new baseline results with this parameter?
- Compare results with and without the different-position penalty?

The new DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY should be an independant parameter that is integrqated in the same way as the original bye penalty parameter

### 5. Documentation
**Q5.1**: Should documentation updates include:
- Parameter description in parameters.json or league_config.json comments?
- README or CLAUDE.md updates explaining the new penalty?
- Inline code comments explaining the logic?

Yes, yes, and yes

**Q5.2**: Should the code changes documentation include:
- Example calculations showing how both penalties work together?
- Rationale for why different-position overlaps are penalized differently?

Yes and yes

---

## Please answer these questions to help guide the implementation.
