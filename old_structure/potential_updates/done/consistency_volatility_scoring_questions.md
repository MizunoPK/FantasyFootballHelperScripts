# CONSISTENCY/VOLATILITY SCORING - CLARIFYING QUESTIONS

**Date**: 2025-10-05
**Source**: `consistency_volatility_scoring.txt`
**Objective**: Implement consistency/volatility analysis across all fantasy helper modes

---

## CONFIGURATION & THRESHOLDS

### Q1: Default Multiplier Values
The spec suggests starting conservatively with LOW=1.05/HIGH=0.95, but also shows LOW=1.08/HIGH=0.92 in examples.

**Question**: Which multiplier values should we use for the initial implementation?
- Option A: Conservative (LOW=1.05, MEDIUM=1.00, HIGH=0.95) - smaller impact
- Option B: Moderate (LOW=1.08, MEDIUM=1.00, HIGH=0.92) - as shown in spec examples
- Option C: Different values you prefer?

**Default if unanswered**: Will use Option B (1.08/1.00/0.92) as shown in spec examples

---

### Q2: CV Threshold Values
The spec suggests testing different thresholds in simulation, but we need initial values.

**Question**: Are the CV thresholds correct for initial implementation?
- LOW volatility: CV < 0.3
- MEDIUM volatility: 0.3 <= CV <= 0.6
- HIGH volatility: CV > 0.6

Or would you prefer different thresholds (e.g., 0.25/0.55, or 0.35/0.65)?

**Default if unanswered**: Will use 0.3 and 0.6 as specified

---

### Q3: ENABLE_CONSISTENCY_SCORING Toggle
**Question**: Should consistency scoring be enabled by default (`ENABLE_CONSISTENCY_SCORING = True`), or disabled by default (`False`) until you've tested it?

**Default if unanswered**: Will enable by default (True)

---

## IMPLEMENTATION DETAILS

### Q4: FantasyPlayer.from_dict() Method
The Starter Helper integration requires converting player_data dict to FantasyPlayer object.

**Question**: Does the `FantasyPlayer` class already have a `from_dict()` class method, or do we need to create it?

If we need to create it:
- Should it handle all FantasyPlayer attributes, or just the essentials (weekly projections, injury_status, bye_week)?
- Are there any specific attributes that must be included?

Answer: There should already be all the needed infrastructure set up for reading in the player data and turning it into FantasyPlayer objects. Your goal here will just be in analyzing the data contained in the objects.

---

### Q5: Handling Missing Weekly Projections
Some players may have missing weekly projection data (None values for certain weeks).

**Question**: How should we handle players with insufficient data for CV calculation?
- Option A: Skip consistency scoring entirely (treat as MEDIUM/neutral)
- Option B: Calculate CV only from available weeks (minimum 3-5 weeks required)
- Option C: Assign a default volatility category (e.g., MEDIUM)
- Option D: Different approach?

**Default if unanswered**: Will use Option B - calculate from available weeks if at least 3 weeks present, otherwise treat as MEDIUM

---

### Q6: Zero Projected Points Weeks
Some players may have 0 points projected for certain weeks (bye, injury, etc.).

**Question**: Should weeks with 0 projected points be:
- Option A: Included in CV calculation (increases volatility)
- Option B: Excluded from CV calculation (filter out along with None values)
- Option C: Different logic?

**Default if unanswered**: Will use Option A - include 0-point weeks in calculation (they represent real variance)

---

## STARTER HELPER SPECIFIC

### Q7: Consistency in Starter Helper Reason String
The spec shows adding consistency to the reason string in Starter Helper.

**Question**: What format do you prefer for the consistency reason?
- Option A: `"Consistency: 1.08x (CV=0.245)"` - shows multiplier and CV
- Option B: `"Consistent player (+8%)"` - more user-friendly
- Option C: `"Low volatility (1.08x)"` - category-based
- Option D: Different format?

**Default if unanswered**: Will use Option A - technical format with multiplier and CV

---

### Q8: Starter Helper Data Structure
The Starter Helper uses player_data dict, not FantasyPlayer objects directly.

**Question**: Does the player_data dict in Starter Helper already contain weekly projection data (week_1_points, week_2_points, etc.)?

If NO:
- Where should we get the weekly projections from to calculate CV?
- Should we load from players.csv, or is there another source?

**Default if unanswered**: Will assume weekly projections are in player_data dict; if not, will load from players.csv using player id/name

---

## SIMULATION & TESTING

### Q9: Simulation Priority
Phase 8 (simulation testing) is marked as optional.

**Question**: Should we include Phase 8 simulation testing in the initial implementation, or defer it until after manual validation is complete?

Answer: Do NOT consisder the simulation testing to be optional. The simulation work is a key element that should be prioritized and not have any cut corners on.

---

### Q10: Performance Considerations
Calculating CV for every player on every scoring call could add overhead.

**Question**: Should we implement any caching for consistency calculations?
- Option A: No caching - recalculate every time (simpler, always current)
- Option B: Cache CV results per player (faster, but may be stale if projections update)
- Option C: Calculate once at startup and store in player object

**Default if unanswered**: Will use Option A - no caching for initial implementation (simplicity first, optimize later if needed)

---

## DOCUMENTATION

### Q11: Example Players for Documentation
The spec uses "Kareem Hunt" as an example of a consistent player.

**Question**: Should we include real player examples in the documentation/comments, or use generic "Player A" / "Player B" examples?

**Default if unanswered**: Will use generic examples in code documentation

---

### Q12: User-Facing Messaging
**Question**: Should consistency scoring be visible to the user in the UI, or only in debug logs?

Currently planned:
- Draft Helper: Debug logs only (user sees final score)
- Starter Helper: Included in reason string (user sees "Consistency: 1.08x")

Is this correct, or would you like different visibility?

Answer: Have it visible in all modes whenever a player is being listed out along with their score.

---

## EDGE CASES

### Q13: Rookies and New Players
Rookies may not have 17 weeks of projection data yet in the season.

**Question**: For rookies or new players with limited historical projections:
- Should we skip consistency scoring?
- Should we assign a default category (MEDIUM)?
- Should we calculate from whatever weeks are available?

Answer: Always use only the weeks that have passed, meaning columns whose number is less than the current week Config variable. This applies to ALL players, not just rookies. Have another constant for the minimum number of weeks needed to calculate the consistency and default to 3 weeks. If there is not enough data yet, then default to applying the MEDIUM category
---

### Q14: DST and Kicker Volatility
Defense/Special Teams and Kickers tend to be naturally more volatile than skill position players.

**Question**: Should DST and K positions use the same multipliers as other positions, or should they have reduced/disabled consistency scoring?

**Default if unanswered**: Will use same universal multipliers for all positions (as specified), can adjust later based on simulation results

---

## VALIDATION

### Q15: Manual Testing Players
For Phase 7 end-to-end validation, we need to test with real players.

**Question**: Do you have specific players you'd like me to test with, or should I select players from the current players.csv?

If selecting from players.csv:
- Should I look for specific characteristics (high/low CV, specific positions)?
- Any players to avoid or prioritize?

**Default if unanswered**: Will select 2-3 players from players.csv with varying volatility levels (one consistent RB/WR, one volatile RB/WR, one QB) for testing

---

## SUMMARY OF ASSUMPTIONS (IF NO ANSWERS PROVIDED)

If you don't have time to answer all questions, here are the defaults I'll use:

1. ✅ Multipliers: LOW=1.08, MEDIUM=1.00, HIGH=0.92
2. ✅ CV Thresholds: 0.3 and 0.6
3. ✅ Enabled by default: ENABLE_CONSISTENCY_SCORING = True
4. ✅ Create FantasyPlayer.from_dict() if needed (with weekly projections)
5. ✅ Calculate CV from available weeks (minimum 3 weeks)
6. ✅ Include 0-point weeks in CV calculation
7. ✅ Reason format: "Consistency: 1.08x (CV=0.245)"
8. ✅ Assume weekly projections in player_data, load from CSV if not
9. ✅ Defer Phase 8 simulation testing
10. ✅ No caching for initial implementation
11. ✅ Generic examples in documentation
12. ✅ Debug logs (Draft Helper), reason string (Starter Helper)
13. ✅ Calculate from available weeks or assign MEDIUM for rookies
14. ✅ Universal multipliers for all positions including DST/K
15. ✅ Select test players from players.csv with varying volatility

**Please review these assumptions and let me know if any need to change before I begin implementation!**
