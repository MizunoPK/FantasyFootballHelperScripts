# Update Consistency to Performance Scoring - Clarifying Questions

## Data Management Questions

### Q1: players_projected.csv Location
Where should the `players_projected.csv` file be created?
- Option A: `data/players_projected.csv` (alongside current `data/players.csv`)
- Option B: `player-data-fetcher/data/players_projected.csv`
- Option C: Other location?
Answer: Option A

### Q2: Historical Data Week Range
The instructions say "weeks 1-6" but we have historical data in `2025_compiled_data/historical_weeks/` for weeks 1-6. Currently the system is on week 6. Should we:
- Option A: Populate weeks 1-6 projections (all historical weeks available)
- Option B: Only populate weeks 1-5 (leaving week 6 for current week)
- Option C: Other approach?
Answer: Populate weeks 1-6. We are actually on week 7.

### Q3: Unmatched Players
For players that don't match between historical data and current players.csv, you said "leave their column's data as whatever the column is set to in the original players.csv". Should we:
- Option A: Copy the value from current `players.csv` (which has season projections)
- Option B: Set to 0.0 if no match found
- Option C: Keep whatever value was initially set during file creation?
Answer: Option A

## Performance Scoring Logic Questions

### Q4: Performance Calculation Method
How should we calculate the performance deviation? Should we:
- Option A: Calculate % deviation: (actual - projected) / projected
- Option B: Calculate raw difference: actual - projected
- Option C: Calculate ratio: actual / projected
- Option D: Other method?
Answer: Option A

### Q5: Performance Multiplier Thresholds
What thresholds should be used for the performance multiplier? Should we follow the same pattern as consistency?
- Current consistency uses: VERY_POOR (0.2), POOR (0.4), GOOD (0.6), EXCELLENT (0.8)
- Should performance use deviation percentages? For example:
  - VERY_POOR: < -20% (underperforming by 20%+)
  - POOR: -20% to -10%
  - AVERAGE: -10% to +10%
  - GOOD: +10% to +20%
  - EXCELLENT: > +20% (overperforming by 20%+)
Answer: yes this is good

### Q6: Performance Multiplier Values
Should the multipliers be:
- Option A: Same as consistency (0.95, 0.975, 1.0, 1.025, 1.05)
- Option B: More aggressive multipliers to reflect performance impact
- Option C: Different values?
Answer: Option A

### Q7: Minimum Weeks for Performance
You mentioned minimum 3 weeks (default). Should this be:
- Option A: 3 weeks of data required before applying multiplier
- Option B: Different minimum?
- Option C: Should we ignore weeks where actual points = 0 (player didn't play)?
Answer: Option A

## Configuration Questions

### Q8: PERFORMANCE_SCORING Structure
Should the config structure in `league_config.json` mirror CONSISTENCY_SCORING? For example:
```json
"PERFORMANCE_SCORING": {
    "MIN_WEEKS": 3,
    "THRESHOLDS": {
        "VERY_POOR": -0.2,
        "POOR": -0.1,
        "GOOD": 0.1,
        "EXCELLENT": 0.2
    },
    "MULTIPLIERS": {
        "VERY_POOR": 0.95,
        "POOR": 0.975,
        "GOOD": 1.025,
        "EXCELLENT": 1.05
    },
    "WEIGHT": 1.0
}
```
Answer: Yes, it should mirror and replace the consistency scoring like this

### Q9: Starter Helper and Trade Simulator
You mentioned setting performance to `True` in StarterHelper and TradeSimulator. Should we:
- Option A: Always enable it in these modes (hardcoded True)
- Option B: Add a config option but default to True for these modes
- Option C: Other approach?
Answer: This means to set simulation=True in the calls to score_player like self.player_manager.score_player(performance=True)

## Implementation Questions

### Q10: Player Data Fetcher Integration
When player_data_fetcher runs, should it:
- Option A: Update ONLY the current week forward in players_projected.csv
- Option B: Recalculate all weeks from current week forward
- Option C: Update current week + future weeks, preserve historical weeks 1-(CURRENT_NFL_WEEK-1)?
Answer: Update only the current week. Leave historical weeks alone

### Q11: ProjectedPointsManager Location
Where should ProjectedPointsManager be created?
- Option A: `league_helper/util/ProjectedPointsManager.py`
- Option B: Other location?
Answer: Option A

### Q12: Backwards Compatibility
You said "no need to maintain backwards compatibility". Should we:
- Option A: Completely remove all consistency-related code and tests
- Option B: Keep old consistency code commented out for reference
- Option C: Remove from main code but keep tests as historical reference?
Answer: Option A

## Testing Questions

### Q13: Test Updates
For the 192 existing tests that reference CONSISTENCY, should we:
- Option A: Update all to use PERFORMANCE instead
- Option B: Remove consistency tests, add new performance tests
- Option C: Keep some consistency tests for historical reference?
Answer: Option A

### Q14: Simulation Config Files
There are 8+ simulation config files in `simulation/simulation_configs/` with CONSISTENCY_SCORING. Should we:
- Option A: Update all of them to PERFORMANCE_SCORING
- Option B: Leave historical configs as-is, only update new configs
- Option C: Other approach?
Answer: Option B

## Additional Questions

### Q15: Week 6 Actual Points
Since we're currently in week 6, should week 6 have:
- Option A: Projected points only (week hasn't completed)
- Option B: Actual points if available
- Option C: Both projected and actual tracked separately?
Answer: The current players.csv is actually from week 7. The file in the historical weeks is accurate to what the week 6 projections were.

### Q16: DST Teams
DST teams have limited historical projection data. Should performance scoring:
- Option A: Apply to DST teams when data is available
- Option B: Skip DST teams for performance scoring
- Option C: Use a different calculation for DST?
Answer: Option B

---

Please answer these questions so I can create an accurate TODO file and implementation plan.
