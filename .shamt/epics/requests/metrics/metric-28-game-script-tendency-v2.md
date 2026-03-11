# Epic Request: Game Script Tendency Scoring Integration (M28)

**File Location:** `.shamt/epics/requests/metrics/metric-28-game-script-tendency-v2.md`

---

## Epic Overview

**Epic Name:** Game Script Tendency Scoring Integration (M28)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Medium

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for how game script (winning/losing margin) affects a team's offensive usage patterns. Teams that frequently trail tend to pass more (benefiting WR/TE), while teams that lead frequently run more (benefiting RB). Without this metric, players on pass-heavy teams due to game script are undervalued, and those on run-heavy teams are overvalued.

**Why is this important?**

Game script tendency is a strong predictor of week-to-week usage patterns. Expected improvement: 8-12% in WR/TE/RB evaluation accuracy, particularly for Starter Helper mode.

**Who is affected?**

Fantasy managers making weekly decisions for WR, TE, and RB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Classify each team's typical game script as PASS_HEAVY, BALANCED, or RUN_HEAVY based on average score differential and trailing frequency
2. Apply bonuses/penalties to WR/TE in pass-heavy situations and RB in run-heavy situations
3. Use historical game score data from `game_data.csv`

**Success Metrics:**
- WRs/TEs on pass-heavy teams (trailing avg -5+ pts) scored higher
- RBs on run-heavy teams (leading avg 5+ pts) scored higher
- Point differential capped at ±21 to prevent extreme outliers
- Expected 8-12% improvement in position accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Weekly game-specific adjustments (this is season-level tendency, not matchup-specific)
- DST evaluation
- QB evaluation (QBs benefit similarly in both scripts)

---

## Requirements

### Functional Requirements

1. **Game Script Classification**
   - Use `game_data.csv` to calculate average point differential per team
   - Classify teams: PASS_HEAVY (avg trailing or -5+ point diff), BALANCED, RUN_HEAVY (avg leading or +5+ point diff)
   - Cap point differential at ±21

2. **Position-Specific Application**
   - WR/TE: Boost in PASS_HEAVY situations (team frequently trailing)
   - RB: Boost in RUN_HEAVY situations (team frequently leading)
   - Position-specific multipliers

3. **Scoring Integration**
   - Apply tendency-based multiplier to WR/TE/RB score
   - Return neutral for teams with insufficient game data

### Non-Functional Requirements

- **Performance:** Team game script classifications should be cached per scoring run
- **Data Dependency:** Requires `data/game_data.csv` to be populated

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (team), `ConfigManager`, `game_data.csv` reader
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No game script scoring step exists.

**Research Findings:**
- `game_data.csv` contains `week`, `home_team`, `away_team`, `home_team_score`, `away_team_score`
- PASS_HEAVY: team averages -5+ point differential (frequently trailing)
- RUN_HEAVY: team averages +5+ point differential (frequently leading)
- Point diff capped at ±21 to reduce outlier impact

**Alternative Approaches Considered:**
1. **Weekly game-specific adjustment:** More accurate but requires weekly matchup data at scoring time
2. **Season-level tendency (Recommended):** Simpler, uses available historical data, directionally correct

### Technical Constraints

**Known Limitations:**
- Data from `game_data.csv` may be incomplete early in season
- A team with <5 games should use neutral classification

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Game Script Classifier
   - **Purpose:** Read game data, compute team score differentials, classify each team's tendency
   - **Key Components:** CSV reading, differential calculation, capping at ±21, team classification

2. **Feature 2:** Game Script Calculator Module
   - **Purpose:** Look up a player's team script and return (multiplier, tier) based on position
   - **Key Components:** Position-aware multiplier lookup, neutral fallback

3. **Feature 3:** Scoring Pipeline Integration
   - **Purpose:** Apply game script as a scoring step for WR/TE/RB
   - **Key Components:** `_apply_game_script_scoring()` method

4. **Feature 4:** Configuration (`GAME_SCRIPT_SCORING` block)

5. **Feature 5:** Unit Tests (pass-heavy team WR boost, run-heavy team RB boost, neutral team, capping)

---

## Dependencies & Risks

### External Dependencies

- **`data/game_data.csv`:** Must be populated for this metric to function

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| game_data.csv missing or incomplete | Medium | Medium | Graceful fallback to BALANCED for missing teams |
| Early season data scarcity | Medium | Low | Require minimum games for classification |

---

## Timeline & Resources

**Estimated Timeline:** 3-4 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add game script scoring step for WR/TE/RB
- `data/league_config.json`: Add `GAME_SCRIPT_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/GameScriptCalculator.py` (includes team classification logic)

**Coding Practices to Follow:**
- Cache team game script classifications per scoring run
- Position guard: WR, TE, RB
- Follow existing Calculator class pattern
- Type hints, Google docstrings, error_context(), LoggingManager

### Testing Strategy (High-Level)

- **Unit Tests:** Pass-heavy team WR gets boost; run-heavy team RB gets boost; balanced team returns neutral; ±21 cap applied; teams with <5 games return neutral
- **Integration Tests:** Game script data loaded from `game_data.csv` correctly

---

## Open Questions

1. **Data source for differential:** Use `game_data.csv` score columns directly, or a derived team stats file?
   - **Status:** Unanswered

2. **Minimum games:** How many games are needed before applying a script classification?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/game_data.csv`
- **Related Epics:** M44 (Opponent Offensive Strength), M34 (Recent Form)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Game Script Tendency Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
