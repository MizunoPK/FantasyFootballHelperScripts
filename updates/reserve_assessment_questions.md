# Reserve Assessment Mode - Implementation Questions

**Status**: Awaiting user answers

**Purpose**: Clarify implementation details and user preferences before proceeding with development.

---

## Background

After researching the codebase extensively (3 verification iterations, 11 files analyzed), I've identified several implementation decisions that require your input. Each question below includes:
- Context from the codebase research
- Multiple implementation options
- My recommendation based on patterns found
- Rationale for each approach

---

## Questions

### Question 1: Player Rating Data Source

**Context**: The scoring algorithm includes a "Player Rating Multiplier" step. We have two sources of player_rating data:
- Last season's player_rating (from `data/last_season/players.csv`)
- Current season's player_rating (from `data/players.csv`)

**Options**:

**A. Use last season's player_rating**
- Pro: Consistent with "historical performance" theme - shows what experts thought of them last year
- Pro: Represents their proven value when they were healthy
- Con: May not reflect updated expert opinion after injury or team change

**B. Use current season's player_rating**
- Pro: Reflects most recent expert consensus
- Pro: May account for changes in circumstances (team, injury recovery, etc.)
- Con: Less consistent with "historical value" approach

**My Recommendation**: **Option A** (last season's player_rating)

**Rationale**: Since we're scoring based on "potential value" from historical performance, we should use last season's rating to measure what they accomplished when healthy. Current season ratings may be artificially low due to injury status.

**Your choice**: A

---

### Question 2: Recommendation Count

**Context**: How many reserve candidates should we display to the user?

The update file says "top 10-15 players". Existing modes use `constants.RECOMMENDATION_COUNT = 10`.

**Options**:

**A. Display 10 recommendations (match existing modes)**
- Pro: Consistent with AddToRosterMode and other modes
- Pro: Keeps display concise and focused on best options
- Con: May miss some interesting candidates

**B. Display 15 recommendations (exploratory mode)**
- Pro: This is a monitoring/exploration mode, more options = better
- Pro: Gives user wider view of reserve market
- Pro: Still manageable to review
- Con: Slightly longer display

**C. Make it configurable (add RESERVE_RECOMMENDATION_COUNT to constants.py)**
- Pro: Most flexible
- Con: Adds complexity for minimal benefit

**My Recommendation**: **Option B** (15 recommendations)

**Rationale**: Reserve assessment is inherently exploratory - users want to survey the waiver market for hidden gems. 15 candidates is still manageable and provides better market coverage than 10.

**Your choice**: B

---

### Question 3: Player Matching Across Seasons (Team Changes)

**Context**: We need to match current undrafted players to their last season data using (name, position, team). However, players may have changed teams between seasons.

**Example**: A player was on KC last season, now on LAR this season. Do we still count them?

**Options**:

**A. Match by (name, position) only - ignore team**
- Pro: Captures all players even if they changed teams
- Pro: Simple implementation
- Con: Rare risk of matching wrong player with same name/position on different team
- Implementation: `{(name.lower(), position): historical_player}`

**B. Match by (name, position, team) exactly**
- Pro: Most accurate matching, no false positives
- Con: Misses players who changed teams (they won't get scored)
- Implementation: `{(name.lower(), position, team): historical_player}`

**C. Match by (name, position) and note team change in display**
- Pro: Captures all players including team changers
- Pro: Alerts user to context change ("was on KC, now on LAR")
- Con: Most complex to implement
- Implementation: Match without team, add display logic to show team change

**My Recommendation**: **Option A** (match by name + position, ignore team)

**Rationale**:
- Same-name collisions are extremely rare in NFL (different positions help)
- We WANT to capture players who changed teams - team quality is scored using CURRENT team anyway
- Simple and effective
- If a reserve player changed teams in offseason, their historical performance is still relevant

**Your choice**: A

---

### Question 4: Mode Interactivity

**Context**: Should Reserve Assessment mode be view-only, or should it allow user actions?

**Options**:

**A. View-only (display recommendations, return to menu)**
- Pro: Simple, focused design - just information display
- Pro: Users can go to "Add to Roster" mode if they want to draft
- Pro: Matches the "monitoring" use case from requirements
- Con: Requires extra navigation to draft a recommended player

**B. Allow drafting directly from this mode**
- Pro: Convenient - user can draft immediately if they see someone interesting
- Pro: One less trip back to main menu
- Con: Adds interaction complexity similar to AddToRosterMode
- Con: Blurs the line between "assessment" and "roster management"

**C. Allow "flagging" players for monitoring (add notes/watchlist)**
- Pro: Supports monitoring workflow
- Con: Requires new data structure (watchlist CSV)
- Con: Significant scope increase

**My Recommendation**: **Option A** (view-only for now)

**Rationale**:
- Keep initial implementation focused and simple
- The mode's purpose is "identify high-value players worth monitoring", not roster management
- Users can easily navigate to Add to Roster mode if they want to draft
- Can add drafting capability in future version if users request it

**Your choice**: A

---

### Question 5: Missing Historical Data Handling

**Context**: Some current players may not have data in `data/last_season/players.csv` (rookies, players not in system last year).

**Options**:

**A. Skip players with no historical data entirely**
- Pro: Reserve candidates should have proven track record
- Pro: Aligns with "historical performance" requirement
- Pro: Clean implementation - only score players with complete data
- Con: Misses injured rookies (though rare)

**B. Use current season projected points as fallback**
- Pro: Includes all injured players, even rookies
- Con: Inconsistent scoring method (historical vs projected)
- Con: Current projections for injured players may be unreliable

**C. Log warning and assign neutral score**
- Pro: Tracks which players couldn't be scored
- Con: Pollutes recommendations with unscored players

**My Recommendation**: **Option A** (skip players with no historical data)

**Rationale**:
- The whole point of this mode is identifying "proven talent that's currently injured"
- Rookies on IR don't have historical track record to evaluate
- Keep scoring methodology consistent (all based on historical performance)
- Simpler implementation with clearer semantics

**Your choice**: A

---

## Summary of Recommendations

| Question | My Recommendation | Reasoning |
|----------|-------------------|-----------|
| 1. Player Rating Source | A (last season) | Consistent with historical performance theme |
| 2. Recommendation Count | B (15 players) | Exploratory mode benefits from more options |
| 3. Player Matching | A (name + position) | Captures team changers, rare collision risk |
| 4. Mode Interactivity | A (view-only) | Keep focused, simple initial implementation |
| 5. Missing Historical Data | A (skip) | Require proven track record for reserves |

---

## Additional Notes

**Critical Finding During Research**:
The update file says to filter by "injury_status = HIGH risk", but there's no "HIGH" value in the data. After researching, I discovered `FantasyPlayer.get_risk_level()` already exists and classifies:
- **HIGH** = INJURY_RESERVE, SUSPENSION, UNKNOWN
- **MEDIUM** = QUESTIONABLE, OUT, DOUBTFUL
- **LOW** = ACTIVE

I'll use `player.get_risk_level() == "HIGH"` for filtering, which targets INJURY_RESERVE players (perfect for reserve assessment!). This requires no user decision - it's the correct interpretation of the requirement.

---

## Next Steps

After you answer these 5 questions, I will:
1. Update the TODO file to reflect your decisions
2. Perform second verification round (3 more iterations)
3. Begin implementation following the refined plan

**Please provide your answers in the format**:
```
Q1: A
Q2: B
Q3: A
Q4: A
Q5: A
```

Or feel free to explain if you want a different approach not listed!
