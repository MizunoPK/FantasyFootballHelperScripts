# Team Rankings Calculation Update - Questions (REVISED)

**Original Specification**: `updates/team_rankings_calculation_update.txt`
**TODO File**: `updates/todo-files/team_rankings_calculation_update_todo.md`

**Implementation Approach**: ESPN Scoreboard API with rolling 4-week window

---

## Implementation Questions

### Question 1: Early Season Behavior (Weeks 1-4)
**Context**: MIN_WEEKS uses **PREVIOUS weeks only** (NOT including current week). For weeks 1-4, we don't have enough previous weeks.

**Important Clarification**:
- Week 1: 0 previous weeks available
- Week 2: 1 previous week available (week 1)
- Week 3: 2 previous weeks available (weeks 1-2)
- Week 4: 3 previous weeks available (weeks 1-3)
- Week 5: 4 previous weeks available (weeks 1-4) ← **First week to use rolling window!**

**Current behavior**: When `CURRENT_NFL_WEEK <= MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS` (weeks 1-4), use neutral rankings.

**Options for weeks 1-4**:

**Option A**: Use all available previous weeks (even if < 4)
- Week 1: No previous weeks → neutral rankings (no choice)
- Week 2: Use week 1 only (1 previous week)
- Week 3: Use weeks 1-2 (2 previous weeks)
- Week 4: Use weeks 1-3 (3 previous weeks)
- Week 5+: Use 4 previous weeks (rolling window)
- Pros: Provides some team differentiation starting week 2
- Cons: Small sample size, volatile rankings

**Option B**: Continue using neutral rankings until week 5
- Weeks 1-4: All teams get rank 16 (neutral)
- Week 5+: Use full 4-week rolling window of previous weeks
- Pros: Only use rankings when we have MIN_WEEKS (4) of data
- Cons: No team differentiation for first 4 weeks of season

**Recommendation**: **Option B (Neutral until week 5)** - Aligns with MIN_WEEKS=4 threshold and avoids volatile early-season rankings.

**Question**: How should we handle weeks 1-4 (insufficient previous weeks)?
- [ ] Option A: Use all available previous weeks
- [X] Option B: Use neutral rankings until week 5 (recommended)
- [ ] Other (please specify): _______________

---

### Question 2: Bye Week Handling
**Context**: NFL teams have bye weeks where they don't play. In a 4-week window, some teams might play 3 games while others play 4.

**Example**: Week 8-11 window:
- Team A: Played weeks 8, 9, 10, 11 (4 games)
- Team B: Bye in week 9, played weeks 8, 10, 11 (3 games)

**Options**:

**Option A**: Calculate averages based on actual games played
- Team A: total_points / 4 games
- Team B: total_points / 3 games
- Pros: Fair comparison, doesn't penalize teams for bye weeks
- Cons: Different denominators might introduce minor ranking variance

**Option B**: Penalize teams with fewer games (use window size as denominator)
- Team A: total_points / 4 games
- Team B: total_points / 4 games (treats missing game as 0 points)
- Pros: Consistent denominator
- Cons: Unfairly penalizes teams for bye weeks

**Option C**: Exclude teams with bye weeks from that week's rankings
- Use neutral rank (16) for any team with fewer than 4 games in window
- Pros: Only rank teams with complete data
- Cons: Loses ranking information for teams with byes

**Recommendation**: **Option A (Actual games played)** - Fair and accurate, reflects true per-game performance.

**Question**: How should we handle bye weeks in the rolling window?
- [X] Option A: Calculate averages based on actual games played (recommended)
- [ ] Option B: Use window size as denominator (penalize byes)
- [ ] Option C: Exclude teams with byes from rankings
- [ ] Other (please specify): _______________

---

### Question 3: Missing/Incomplete Scoreboard Data
**Context**: Scoreboard data for recent weeks might be incomplete (games in progress, postponed games, API errors).

**Scenario**: Fetching scoreboard for week 10, but some games haven't finished yet or data is unavailable.

**Options**:

**Option A**: Calculate from available games only
- If only 12 of 16 games have scores, use those 12
- Teams in missing games get 0 games counted for that week
- Pros: Makes best use of available data
- Cons: Incomplete for teams in missing games

**Option B**: Skip the incomplete week entirely
- If week 10 is incomplete, use weeks 7-9 only (3-week window)
- Wait until all games are complete before including week in window
- Pros: Only uses complete data
- Cons: Reduces window size

**Option C**: Fallback to neutral rankings if any week is incomplete
- If any of the 4 weeks has incomplete data, use neutral rankings for all teams
- Pros: Conservative, avoids bad data
- Cons: Aggressive fallback, loses all ranking information

**Recommendation**: **Option A (Use available games)** - Most practical for real-time usage, teams with complete data get ranked accurately.

**Question**: How should we handle incomplete scoreboard data?
- [X] Option A: Calculate from available games only (recommended)
- [ ] Option B: Skip incomplete weeks
- [ ] Option C: Fallback to neutral rankings
- [ ] Other (please specify): _______________

---

### Question 4: Position-Specific Defense Rankings
**Context**: The current `teams.csv` includes position-specific defense rankings (def_vs_qb_rank, def_vs_rb_rank, etc.) in addition to overall offensive/defensive ranks.

**Current implementation**: Position-specific defense ranks come from ESPN's position-vs-defense statistics (cumulative season data).

**Question**: Should we also apply the rolling window approach to position-specific defense rankings?

**Options**:

**Option A**: Apply rolling window to offensive/defensive ranks only
- Keep position-specific defense ranks as cumulative season stats from ESPN API
- Pros: Simpler implementation, position defense might benefit from larger sample size
- Cons: Inconsistent methodology between overall and position-specific ranks

**Option B**: Apply rolling window to ALL rankings
- Calculate position-specific defense from game-level data in rolling window
- Would require tracking position-specific performance per game (complex)
- Pros: Consistent methodology
- Cons: Much more complex, game-level position stats not readily available in scoreboard API

**Recommendation**: **Option A (Overall ranks only)** - Scoreboard API doesn't provide position-level statistics, would require different data source.

**Question**: Should rolling window apply to position-specific defense rankings?
- [ ] Option A: Overall offensive/defensive ranks only (recommended)
- [X] Option B: All rankings including position-specific
- [ ] Position-specific ranks are not important for this update

---

### Question 5: API Error Handling & Fallback
**Context**: ESPN API calls might fail due to network issues, rate limiting, or server errors.

**Question**: If scoreboard API fails for one or more weeks in the rolling window, what should we do?

**Options**:

**Option A**: Fallback to neutral rankings (all teams = rank 16)
- Safe, prevents bad/incomplete data from affecting scoring
- Existing pattern in codebase (espn_client.py:795)
- Recommended for any API error

**Option B**: Retry failed API calls
- Attempt 2-3 retries with exponential backoff
- If still failing, fallback to neutral rankings
- More resilient but adds complexity

**Option C**: Cache previous week's rankings as fallback
- If current calculation fails, use previous week's team rankings
- Prevents complete loss of team differentiation
- Requires caching mechanism

**Recommendation**: **Option A (Fallback to neutral)** - Simple, safe, consistent with existing error handling pattern.

**Question**: How should we handle API errors when fetching scoreboard data?
- [X] Option A: Fallback to neutral rankings (recommended)
- [ ] Option B: Retry with exponential backoff
- [ ] Option C: Cache and use previous rankings
- [ ] Other (please specify): _______________

---

### Question 6: Logging Verbosity
**Context**: Need to decide logging detail level for the rolling window calculations.

**Recommendation**: Moderate logging (INFO + WARNING + ERROR)

**Question**: What logging level should we use?

- [X] Moderate logging (recommended):
  - INFO: "Calculating rolling 4-week team rankings from weeks 5-8"
  - WARNING: "Scoreboard data incomplete for week 6, calculating from 3 weeks"
  - ERROR: "Failed to fetch scoreboard for week 5: {error}"
  - DEBUG: "Team KC: 4 games, avg 28.5 pts scored, 18.3 pts allowed, offensive_rank=2"
- [ ] Minimal logging (ERROR only)
- [ ] Detailed logging (all of above + per-team calculations)

---

### Question 7: Documentation Updates
**Question**: Which documentation files should be updated?

Select all that apply:
- [X] `docs/scoring/04_team_quality_multiplier.md` - Team quality scoring documentation
- [X] Code comments and docstrings in espn_client.py
- [X] `README.md` - User-facing documentation (if behavior changes significantly)
- [X] `ARCHITECTURE.md` - Technical architecture (probably not needed for this change)

---

### Question 8: Testing Scope
**Context**: Creating new unit tests for rolling window functionality.

**Recommendation**: Comprehensive testing

**Question**: What level of test coverage do you want?

- [X] Comprehensive (recommended):
  - Test scoreboard fetching for specific weeks
  - Test performance aggregation (various game counts)
  - Test ranking calculation from scores
  - Test edge cases (weeks 1-4, bye weeks, missing data, API errors)
  - Test integration with existing team ranking flow
- [ ] Standard: Happy path + major edge cases only
- [ ] Basic: Happy path only

---

## ANSWERS SECTION

**Instructions**: Questions have been pre-answered based on technical analysis and recommendations. Please review and modify if needed.

---

### Summary of Answers:

**Question 1**: Option B - Use neutral rankings until week 5 (when 4 previous weeks are available)
**Question 2**: Option A - Calculate averages based on actual games played
**Question 3**: Option A - Calculate from available games only
**Question 4**: Option B - All rankings including position-specific (data available via player weekly stats)
**Question 5**: Option A - Fallback to neutral rankings on API error
**Question 6**: Moderate logging
**Question 7**: Update team quality docs + code comments
**Question 8**: Comprehensive testing

**CRITICAL Implementation Details**:

1. **Rolling window uses PREVIOUS weeks only** (NOT including current week):
   - Week 5 is the first week to use rolling window (uses previous weeks 1-4)
   - Week 10 uses previous weeks 6-9 (rolling 4-week window)
   - Formula: `range(current_week - MIN_WEEKS, current_week)` excludes current week
   - **Examples**:
     - Week 5: `range(1, 5)` = weeks [1, 2, 3, 4] (previous weeks)
     - Week 10: `range(6, 10)` = weeks [6, 7, 8, 9] (previous weeks)

2. **Position-specific defense rankings**:
   - Current implementation: `_calculate_position_defense_rankings()` (espn_client.py:1029)
   - Currently uses ALL previous weeks: `range(1, current_week)` (line 1069)
   - **To apply rolling window**: Change to `range(current_week - MIN_WEEKS, current_week)`
   - Uses player weekly data (already available from ESPN API)
   - This makes position-specific ranks consistent with overall offensive/defensive ranks

---

## Next Steps

With answers provided:
1. ✅ TODO file updated with ESPN scoreboard approach
2. ✅ Implementation details include previous-weeks-only logic
3. Ready to proceed with implementation

**Total Progress**: First verification round complete (3/6 iterations). Answers provided with clarified previous-weeks logic. Ready to implement!
