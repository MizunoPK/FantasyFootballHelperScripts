# Score Player Usage Report

**Generated**: 2025-10-28
**Purpose**: Document all `score_player()` method calls in league_helper module
**Total Call Sites**: 8 locations across 4 modules

---

## Overview

This report documents every location where the `score_player()` method is called within the league_helper module, showing which scoring factors are enabled/disabled at each call site.

### Scoring Factors Available

| Factor | Type | Description |
|--------|------|-------------|
| `adp` | Multiplicative | Average Draft Position multiplier (ability factor) |
| `player_rating` | Multiplicative | Player quality rating multiplier (ability factor) |
| `team_quality` | Multiplicative | NFL team quality multiplier (ability factor) |
| `performance` | Multiplicative | Historical performance deviation multiplier (ability factor) |
| `matchup` | **Additive** | Current week matchup bonus (environmental factor) |
| `schedule` | **Additive** | Season schedule strength bonus (environmental factor) |
| `bye` | Additive Penalty | Bye week overlap penalties |
| `injury` | Additive Penalty | Injury risk penalties |
| `draft_round` | Additive Bonus | Position priority bonuses based on draft round |
| `roster` | Context | Roster context for bye week overlap calculations |

---

## Call Sites by Module

### 1. PlayerManager (util/PlayerManager.py)

The PlayerManager module contains the core `score_player()` method and internal calls.

**IMPORTANT**: Default parameters changed (line 559):
- `performance=False` (was True)
- `schedule=False` (was True)
- `matchup=False` (unchanged)

All internal call sites now **explicitly specify all parameters** to avoid relying on defaults.

---

#### 1.1 Initial Player Loading (Line 290)

**Location**: `league_helper/util/PlayerManager.py:290`
**Context**: `load_players_from_csv()` - Calculating baseline scores for all players

```python
player.score = self.score_player(player,
                                 adp=False,
                                 player_rating=True,
                                 team_quality=True,
                                 performance=False,
                                 matchup=False,
                                 schedule=False,
                                 bye=False,
                                 injury=True
                                 ).score
```

**Scoring Factors**:
- ✅ **Enabled**:
  - `player_rating=True` - Player quality rating
  - `team_quality=True` - NFL team quality
  - `injury=True` - Injury risk penalties

- ❌ **Disabled**:
  - `adp=False` - No draft position factor
  - `performance=False` - No historical performance
  - `matchup=False` - No matchup scoring
  - `schedule=False` - No schedule scoring
  - `bye=False` - No bye penalties (roster not finalized)

- 📝 **Roster Context**: None (uses default empty roster during initial load)

**Purpose**: Calculate **minimal baseline scores** for all players during initial data load.

**Rationale**:
- **Minimal scoring** with only stable intrinsic factors (player rating, team quality)
- **No situational factors**: performance, matchup, schedule all disabled
- **No ADP**: Draft position irrelevant for baseline scoring
- **No bye penalties**: Roster composition isn't finalized yet
- **Injury enabled**: Permanent injury risk still matters for baseline value

---

#### 1.2 Team Loading (Line 320)

**Location**: `league_helper/util/PlayerManager.py:320`
**Context**: `load_team()` - Scoring current roster players

```python
result = self.score_player(p,
                            adp=False,
                            player_rating=True,
                            team_quality=True,
                            performance=True,
                            matchup=False,
                            schedule=True,
                            bye=True,
                            injury=True
                            )
```

**Scoring Factors**:
- ✅ **Enabled**:
  - `player_rating=True` - Player quality rating
  - `team_quality=True` - NFL team quality
  - `performance=True` - Historical performance trends
  - `schedule=True` - Season schedule strength
  - `bye=True` - Bye week overlap penalties
  - `injury=True` - Injury risk penalties

- ❌ **Disabled**:
  - `adp=False` - No draft position (already drafted)
  - `matchup=False` - No current week matchup (not relevant for roster overview)

- 📝 **Roster Context**: Current team roster (implicit)

**Purpose**: Score players already on the user's roster for display and tracking.

**Rationale**:
- **Season-long factors** enabled: performance, schedule strength
- **Roster fit factors** enabled: bye penalties (roster is finalized)
- **No matchup**: Current week matchup not relevant for roster overview
- **No ADP**: Draft position irrelevant for already-drafted players

---

#### 1.3 Display Team Scores (Line 510)

**Location**: `league_helper/util/PlayerManager.py:510`
**Context**: `display_team_scores()` - Displaying detailed roster scores

```python
scored_player = self.score_player(player,
                                 adp=False,
                                 player_rating=True,
                                 team_quality=True,
                                 performance=True,
                                 matchup=False,
                                 schedule=True,
                                 bye=True,
                                 injury=True)
```

**Scoring Factors**:
- ✅ **Enabled**:
  - `player_rating=True` - Player quality rating
  - `team_quality=True` - NFL team quality
  - `performance=True` - Historical performance trends
  - `schedule=True` - Season schedule strength
  - `bye=True` - Bye week overlap penalties
  - `injury=True` - Injury risk penalties

- ❌ **Disabled**:
  - `adp=False` - No draft position (already drafted)
  - `matchup=False` - No current week matchup (not relevant for display)

- 📝 **Roster Context**: Current team roster (implicit)

**Purpose**: Display detailed scoring breakdown for all rostered players.

**Rationale**:
- **Identical to load_team scoring** for consistency
- **Full season-long scoring**: performance, schedule, bye penalties
- **No matchup**: Not relevant for roster overview display
- **No ADP**: Draft position irrelevant for display

---

### 2. AddToRosterMode (add_to_roster_mode/AddToRosterModeManager.py)

Draft recommendation mode for suggesting players to draft during season.

#### 2.1 Draft Recommendations (Line 281)

**Location**: `league_helper/add_to_roster_mode/AddToRosterModeManager.py:281`
**Context**: `get_recommendations()` - Generating draft recommendations

```python
scored_player = self.player_manager.score_player(
    p,
    draft_round=current_round,  # Current round for position bonuses
    adp=True,                   # Enable ADP multiplier
    player_rating=True,         # Enable player rating multiplier
    team_quality=True,          # Enable team quality multiplier
    performance=False,          # Disable performance deviation
    matchup=False,              # Disable matchup multiplier
    schedule=False              # Disable schedule strength multiplier
)
```

**Scoring Factors**:
- ✅ **Enabled**:
  - `adp=True` - ADP multiplier (player ability/value)
  - `player_rating=True` - Player quality rating (player ability)
  - `team_quality=True` - NFL team quality (stable team factor)
  - `draft_round=current_round` - Position priority bonuses
  - `bye` (default=True) - Bye week overlap penalties
  - `injury` (default=True) - Injury risk penalties

- ❌ **Disabled**:
  - `performance=False` - Historical performance (situational)
  - `matchup=False` - Current week matchup (situational)
  - `schedule=False` - Schedule strength (situational)

- 📝 **Roster Context**: Current team roster (implicit)

**Purpose**: Recommend best available players to draft based on stable long-term factors.

**Rationale**:
- **Enabled factors** focus on **stable, season-long player value**: ADP, player ratings, team quality, bye penalties
- **Disabled factors** are **situational/environmental**: performance (weekly variance), matchup (single week), schedule (already captured in projections)
- Draft decisions should prioritize intrinsic player quality and roster fit (bye weeks), not short-term matchup advantages

---

### 3. StarterHelperMode (starter_helper_mode/StarterHelperModeManager.py)

Weekly lineup optimization mode for sit/start decisions.

#### 3.1 Weekly Player Scoring (Line 365)

**Location**: `league_helper/starter_helper_mode/StarterHelperModeManager.py:365`
**Context**: `_score_player_for_week()` - Scoring players for weekly lineup decisions

```python
scored_player = self.player_manager.score_player(
    player_data,
    use_weekly_projection=True,
    adp=False,
    player_rating=False,
    team_quality=False,
    performance=True,
    matchup=True,
    schedule=False,  # EXPLICIT: No schedule scoring for weekly decisions
    bye=False,
    injury=False
)
```

**Scoring Factors**:
- ✅ **Enabled**:
  - `use_weekly_projection=True` - Use weekly projections (not season)
  - `performance=True` - Recent performance trends
  - `matchup=True` - Current week matchup advantage

- ❌ **Disabled**:
  - `adp=False` - Draft position (irrelevant for weekly)
  - `player_rating=False` - Season-long rating (irrelevant for weekly)
  - `team_quality=False` - Season-long team quality (irrelevant for weekly)
  - `schedule=False` - Full season schedule (irrelevant for single week)
  - `bye=False` - Bye weeks (player wouldn't be available if on bye)
  - `injury=False` - Injury penalties (player wouldn't be available if injured)

- 📝 **Roster Context**: Current team roster (implicit)

**Purpose**: Optimize weekly lineup by focusing on **this week's performance potential**.

**Rationale**:
- **Enabled factors** focus on **weekly variance**: recent performance trends, current matchup
- **Disabled factors** are **season-long or irrelevant**: ADP (draft value), player ratings (season average), team quality (season trend), schedule (multi-week), bye/injury (players already filtered)
- Weekly decisions should maximize points THIS WEEK, not season-long value

---

### 4. TradeSimulatorMode (trade_simulator_mode/)

Trade evaluation mode with two different scoring contexts.

#### 4.1 Trade Analysis - Pre/Post Trade Comparison (Line 256)

**Location**: `league_helper/trade_simulator_mode/trade_analyzer.py:256`
**Context**: `_score_players()` - Scoring players in trade evaluation

```python
scored_player = self.player_manager.score_player(
    p,
    adp=False,
    player_rating=True,
    team_quality=True,
    performance=True,
    matchup=False,
    schedule=True,
    roster=post_trade_roster
)
```

**Scoring Factors**:
- ✅ **Enabled**:
  - `player_rating=True` - Player quality (ability factor)
  - `team_quality=True` - NFL team quality (ability factor)
  - `performance=True` - Recent performance trends
  - `schedule=True` - Season schedule strength
  - `roster=post_trade_roster` - Explicit roster context for accurate bye calculations
  - `bye` (default=True) - Bye week overlap penalties
  - `injury` (default=True) - Injury risk penalties

- ❌ **Disabled**:
  - `adp=False` - Draft position (irrelevant mid-season)
  - `matchup=False` - Current week matchup (short-term, not trade decision factor)

- 📝 **Roster Context**: `post_trade_roster` (explicitly passed) - Critical for accurate bye week overlap calculations

**Purpose**: Evaluate trade impact on season-long roster strength.

**Rationale**:
- **Enabled factors** focus on **season-long value**: player ratings, team quality, schedule strength, bye overlaps
- **Disabled factors**: ADP (already drafted), matchup (too short-term for trade decisions)
- **Roster context critical**: Must pass post-trade roster to calculate bye week overlaps correctly
- Trade decisions should consider rest-of-season impact, not single-week performance

---

#### 4.2 TradeSimTeam - Opponent Scoring (Line 86)

**Location**: `league_helper/trade_simulator_mode/TradeSimTeam.py:86`
**Context**: `calculate_total_score()` - Scoring opponent team in trade simulation

```python
scored_player = self.player_manager.score_player(
    player,
    adp=False,
    player_rating=True,
    team_quality=True,
    performance=True,
    matchup=False,
    schedule=False,  # OPPONENT: Exclude schedule scoring
    bye=False,       # OPPONENT: Exclude bye penalties
    injury=False,
    roster=self.team
)
```

**Scoring Factors**:
- ✅ **Enabled**:
  - `player_rating=True` - Player quality (intrinsic ability)
  - `team_quality=True` - NFL team quality (intrinsic ability)
  - `performance=True` - Recent performance (intrinsic ability)
  - `roster=self.team` - Roster context

- ❌ **Disabled**:
  - `adp=False` - Draft position (irrelevant)
  - `matchup=False` - Current week matchup (irrelevant for trade)
  - `schedule=False` - **ASYMMETRIC**: Exclude schedule for opponent
  - `bye=False` - **ASYMMETRIC**: Exclude bye penalties for opponent
  - `injury=False` - Injury penalties

- 📝 **Roster Context**: Opponent team roster

**Purpose**: Score opponent's team using **INTRINSIC VALUE ONLY** (no environmental factors).

**Rationale**:
- **Two asymmetric factors** (bye + schedule) excluded for opponents
- **Bye penalties excluded**: We don't know opponent's roster construction strategy
- **Schedule excluded**: Opponent's schedule strength is irrelevant to our trade decision
- **Focus on intrinsic ability**: Player rating, team quality, performance only
- **Trade philosophy**: Evaluate intrinsic player value, not opponent's environmental context

---

#### 4.3 TradeSimTeam - User Scoring (Line 89)

**Location**: `league_helper/trade_simulator_mode/TradeSimTeam.py:89`
**Context**: `calculate_total_score()` - Scoring user team in trade simulation

```python
scored_player = self.player_manager.score_player(
    player,
    adp=False,
    player_rating=True,
    team_quality=True,
    performance=True,
    matchup=False,
    schedule=True,   # USER: Include schedule scoring
    bye=True,        # USER: Include bye penalties
    injury=False,
    roster=self.team
)
```

**Scoring Factors**:
- ✅ **Enabled**:
  - `player_rating=True` - Player quality (intrinsic ability)
  - `team_quality=True` - NFL team quality (intrinsic ability)
  - `performance=True` - Recent performance (intrinsic ability)
  - `schedule=True` - **ASYMMETRIC**: Include schedule for user's benefit
  - `bye=True` - **ASYMMETRIC**: Include bye penalties for user's roster
  - `roster=self.team` - Roster context

- ❌ **Disabled**:
  - `adp=False` - Draft position (irrelevant)
  - `matchup=False` - Current week matchup (irrelevant for trade)
  - `injury=False` - Injury penalties

- 📝 **Roster Context**: User team roster

**Purpose**: Score user's team with **INTRINSIC + ENVIRONMENTAL** factors.

**Rationale**:
- **Two asymmetric factors** (bye + schedule) included for user
- **Bye penalties included**: Incentivize avoiding bye week stacking on YOUR roster
- **Schedule included**: Players valuable for YOUR specific remaining schedule (especially playoffs)
- **User-centric evaluation**: Does this trade improve MY roster for MY schedule and MY bye distribution?
- **Trade philosophy**: Focus on user's roster improvement, not fair comparison

---

## Summary by Mode

### PlayerManager (Data Management)
**Philosophy**: Tiered scoring based on context

#### Baseline Loading (load_players)
- **Enabled**: player_rating, team_quality, injury
- **Disabled**: ADP, performance, matchup, schedule, bye
- **Purpose**: Minimal baseline scoring with only stable intrinsic factors

#### Roster Management (load_team, display_team)
- **Enabled**: player_rating, team_quality, performance, schedule, bye, injury
- **Disabled**: ADP, matchup
- **Purpose**: Full season-long scoring for roster assessment

### Draft Mode (AddToRosterMode)
**Philosophy**: Stable, season-long intrinsic value
**Enabled**: ADP, player_rating, team_quality, bye penalties, injury penalties, draft_round bonuses
**Disabled**: performance, matchup, schedule (situational factors)

### Weekly Lineup (StarterHelperMode)
**Philosophy**: Maximize this week's points
**Enabled**: performance, matchup, weekly projections
**Disabled**: ADP, player_rating, team_quality, schedule, bye, injury (season-long or irrelevant factors)

### Trade Evaluation (TradeSimulatorMode)
**Philosophy**: User-centric roster improvement (intrinsic + environmental)

#### Opponent Scoring (Intrinsic Value Only)
- **Enabled**: player_rating, team_quality, performance
- **Disabled**: ADP, matchup, schedule, bye
- **Purpose**: Baseline intrinsic player value

#### User Scoring (Intrinsic + Environmental)
- **Enabled**: player_rating, team_quality, performance, schedule, bye
- **Disabled**: ADP, matchup
- **Purpose**: Full value including user's schedule and roster context

**Asymmetric Factors** (user=True, opponent=False):
- `bye` - User's roster bye distribution matters; opponent's doesn't
- `schedule` - User's remaining schedule matters; opponent's doesn't

---

## Scoring Factor Usage Matrix

| Call Site | adp | player_rating | team_quality | performance | matchup | schedule | bye | injury | draft_round | roster |
|-----------|-----|---------------|--------------|-------------|---------|----------|-----|--------|-------------|--------|
| **PlayerManager.load_players** | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | - | - |
| **PlayerManager.load_team** | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | - | ✅ |
| **PlayerManager.display_team** | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | - | ✅ |
| **AddToRosterMode** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **StarterHelperMode** | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | - | ✅ |
| **TradeAnalyzer** | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | - | ✅ (post-trade) |
| **TradeSimTeam (Opponent)** | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | - | ✅ |
| **TradeSimTeam (User)** | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | - | ✅ |

**Legend**:
- ✅ = Enabled (True)
- ❌ = Disabled (False)
- - = Not specified (N/A)

**Key Changes** (Recent):
- **PlayerManager defaults changed**: `performance=False`, `schedule=False` (were True)
- **All PlayerManager internal calls**: Now explicitly specify all parameters
- **load_players**: Minimal scoring (only player_rating, team_quality, injury)
- **load_team/display_team**: Full season-long scoring (adds performance, schedule, bye)

---

## Key Patterns

### 1. Ability vs Environmental Factors

**Ability Factors** (Multiplicative - scale with player projection):
- ADP, player_rating, team_quality, performance
- Used to assess intrinsic player quality
- More important for long-term decisions (draft, trades)

**Environmental Factors** (Additive - equal bonus regardless of player):
- matchup, schedule
- Used to assess external opportunities
- More important for short-term decisions (weekly lineups)

### 2. Time Horizon Determines Factors

**Long-term decisions** (Draft, Trades):
- Enable: player_rating, team_quality, schedule, bye penalties
- Disable: matchup (too short-term)

**Short-term decisions** (Weekly lineups):
- Enable: performance, matchup
- Disable: ADP, player_rating, team_quality, schedule (too long-term)

### 3. Roster Context Importance

**Critical for**:
- Bye week overlap calculations (must pass correct roster)
- Trade evaluation (must pass post-trade roster to get accurate bye penalties)

**Not needed for**:
- Initial player loading (no roster exists yet)
- Weekly lineups (implicit current roster)

### 4. Asymmetric Scoring

**Trade Simulator** uses TWO asymmetric environmental factors:

#### Factor 1: Bye Week Penalties
- **User**: bye=True (penalize bye week stacking on user's roster)
- **Opponent**: bye=False (ignore opponent's bye distribution)
- **Rationale**: User's roster construction quality matters; opponent's is unknown

#### Factor 2: Schedule Strength Scoring
- **User**: schedule=True (value players for user's remaining schedule)
- **Opponent**: schedule=False (ignore opponent's schedule strength)
- **Rationale**: User's playoff schedule matters; opponent's is irrelevant to trade decision

**Philosophy**: Both asymmetric factors are **environmental/roster-specific**. Trade evaluation focuses on "Does this improve MY roster for MY context?" not "Is this fair for both sides?"

---

## Recommendations

### 1. Consistency
All modes are **correctly configured** for their specific use cases. No changes needed.

### 2. Documentation
This report should be referenced when:
- Adding new modes/features
- Modifying scoring factors
- Debugging unexpected scores

### 3. Future Considerations
If adding new scoring factors:
- Classify as ability (multiplicative) or environmental (additive)
- Determine appropriate time horizon (long-term vs short-term)
- Consider asymmetric usage (user vs opponent)

---

## Recent Changes (2025-10-28)

### 1. TradeSimTeam Schedule Scoring Made Asymmetric

**Location**: `league_helper/trade_simulator_mode/TradeSimTeam.py:86`

**Change**:
```python
# OLD (Opponent scoring):
schedule=True

# NEW (Opponent scoring):
schedule=False

# User scoring unchanged:
schedule=True
```

**Impact**:
- **Opponent**: Now uses intrinsic value only (player_rating, team_quality, performance)
- **User**: Uses intrinsic + environmental (adds schedule, bye)
- **Two asymmetric factors**: Both bye and schedule are now user-only

**Rationale**:
- **Schedule is roster-specific**: User's playoff schedule (weeks 15-17) determines player value
- **Opponent's schedule irrelevant**: Trade evaluation should focus on user's benefit, not opponent's
- **Consistent with bye asymmetry**: Both environmental/roster factors now asymmetric
- **User-centric philosophy**: "Does this trade help ME for MY schedule?"

**Example**:
- Trading for a WR with easy playoff schedule now shows HIGHER value delta
- Pre-change: Both sides get schedule boost (minimal net difference)
- Post-change: Only user gets schedule boost (larger positive delta for good playoff schedules)

---

### 2. PlayerManager Default Parameters Changed

**Location**: `league_helper/util/PlayerManager.py:559`

**Changes**:
```python
# OLD defaults:
def score_player(self, p, ..., performance=True, matchup=False, schedule=True, ...):

# NEW defaults:
def score_player(self, p, ..., performance=False, matchup=False, schedule=False, ...):
```

**Impact**:
1. **Default behavior is now more conservative**: Only stable factors enabled by default
2. **All internal calls explicitly specify parameters**: No reliance on defaults
3. **load_players uses minimal scoring**: Only player_rating, team_quality, injury

**Rationale**:
- **Safer defaults**: Situational factors (performance, schedule) must be explicitly enabled
- **Explicit > Implicit**: All call sites now clearly document their intent
- **Baseline scoring cleaner**: load_players gets minimal baseline without situational variance

### PlayerManager Internal Call Changes

#### load_players_from_csv() - Line 290
**Changed from**: Implicit defaults (most factors enabled)
**Changed to**: Minimal explicit scoring
- ❌ Disabled: adp, performance, matchup, schedule, bye
- ✅ Enabled: player_rating, team_quality, injury

**Impact**: Baseline player scores are now cleaner, based only on intrinsic quality (player rating, team quality) plus injury risk. No situational factors.

#### load_team() - Line 320
**Changed from**: Implicit defaults
**Changed to**: Full explicit season-long scoring
- ❌ Disabled: adp, matchup
- ✅ Enabled: player_rating, team_quality, performance, schedule, bye, injury

**Impact**: Roster scoring includes all relevant season-long factors. Explicit configuration makes intent clear.

#### display_team_scores() - Line 510
**Changed from**: Only `bye=True` specified
**Changed to**: Full explicit season-long scoring (identical to load_team)
- ❌ Disabled: adp, matchup
- ✅ Enabled: player_rating, team_quality, performance, schedule, bye, injury

**Impact**: Consistent with load_team scoring. Display shows full season-long assessment.

### Migration Impact

**Breaking Changes**: None (all call sites explicitly specify parameters)

**Behavior Changes**:
1. **load_players**: Now uses minimal scoring (more conservative)
2. **External code relying on defaults**: Would get more conservative scoring (performance=False, schedule=False)

**Recommendation**:
- ✅ **All league_helper modules updated**: Explicit parameters everywhere
- ✅ **No breaking changes**: All internal calls already updated
- ⚠️ **External code**: Should explicitly specify all parameters to avoid relying on defaults

---

## Conclusion

The league_helper module uses 8 distinct `score_player()` call sites across 4 modules, each carefully configured for its specific purpose:

1. **AddToRosterMode**: Long-term intrinsic value (ADP, ratings, team quality)
2. **StarterHelperMode**: Short-term weekly performance (performance, matchup)
3. **TradeSimulatorMode**: User-centric roster improvement with TWO asymmetric factors (bye, schedule)
   - Opponent: Intrinsic value only (ratings, performance)
   - User: Intrinsic + environmental (adds schedule, bye for user's context)
4. **PlayerManager**: Tiered scoring (minimal baseline → full season-long for roster)

All configurations are **intentional and correct** for their respective use cases. Recent changes:
- ✅ **TradeSimTeam**: Schedule scoring now asymmetric (consistent with bye penalties)
- ✅ **PlayerManager**: All parameters explicit, safer defaults (performance=False, schedule=False)
