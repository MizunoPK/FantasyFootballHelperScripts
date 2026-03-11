# Epic Request: Opponent Offensive Strength Scoring Integration (M44)

**File Location:** `.shamt/epics/requests/metrics/metric-44-opponent-offensive-strength-v2.md`

---

## Epic Overview

**Epic Name:** Opponent Offensive Strength Scoring Integration (M44)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Medium

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for the quality of the upcoming opponent's offense when evaluating DSTs. A DST facing a bottom-5 offense (averaging 15 PPG) has a dramatically higher floor and ceiling than the same DST facing a top-5 offense (averaging 28+ PPG). Without this matchup context, DST streaming decisions are made without critical information.

**Why is this important?**

Opponent offensive strength is the most impactful weekly variable for DST fantasy scoring. Expected improvement: 10-14% in DST weekly streaming decision accuracy — the highest of any DST metric.

**Who is affected?**

Fantasy managers making weekly DST streaming decisions.

---

## Goals & Success Metrics

**Primary Goals:**
1. Calculate each NFL team's offensive strength (points per game) from historical game data
2. Look up the DST's upcoming opponent and determine matchup difficulty
3. Apply significant multiplier adjustments: boost for easy matchups (weak offenses), penalty for hard matchups (elite offenses)

**Success Metrics:**
- Easy matchup DSTs (facing bottom-5 offense) boosted significantly
- Hard matchup DSTs (facing top-3 offense) significantly penalized
- Bye weeks handled gracefully (neutral adjustment)
- 10-14% improvement in DST streaming accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Position-specific matchup adjustments for skill players (different system)
- DST's own offensive or defensive performance metrics

---

## Requirements

### Functional Requirements

1. **Team Offensive Strength Calculation**
   - Load team points-scored data from `data/historical_data/{year}/{week}/team_data/{TEAM}.csv`
   - Calculate each team's season PPG
   - Rank all 32 teams by PPG
   - Calculate league average PPG for context

2. **Matchup Lookup**
   - Use `game_data.csv` to find the DST's opponent for the current week
   - Handle bye weeks (return neutral adjustment)
   - Handle early season data scarcity (weeks 1-2 with limited PPG data)

3. **Tier Classification**
   - EXCELLENT (opponent ≤17.0 PPG or rank 28-32): Easy matchup → big boost
   - GOOD (17.1-20.0 PPG or rank 23-27): Favorable matchup
   - AVERAGE (20.1-24.0 PPG or rank 12-22): Neutral
   - POOR (24.1-27.0 PPG or rank 6-11): Difficult matchup
   - VERY_POOR (≥27.1 PPG or rank 1-5): Elite offense → big penalty

4. **Scoring Integration**
   - Apply matchup-based multiplier to DST score

### Non-Functional Requirements

- **Performance:** Team PPG calculations cached per scoring run
- **Data Robustness:** Graceful fallback when team data files are missing

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (DST team), `ConfigManager`, `game_data.csv`, `historical_data/` team CSV files
- **Integrations:** `player_scoring.py`, new `TeamStatsLoader` utility
- **Technology Stack:** Python 3, CSV reading

---

## Research & Background

**Current State:** No opponent strength scoring step exists for DST.

**Research Findings:**
- `data/game_data.csv` contains weekly schedule (home_team, away_team)
- `data/historical_data/{year}/{week}/team_data/{TEAM}.csv` contains team PPG data
- Matchup difficulty tiers have the highest expected impact of any DST metric (10-14%)
- Team code normalization may be needed (e.g., "LV" vs "LVR")

**Alternative Approaches Considered:**
1. **Use season PPG only:** May not reflect recent opponent performance
2. **Use rolling 4-week opponent PPG:** More accurate but more complex
3. **Season PPG with min-games guard (Recommended):** Good signal, available early in season

### Technical Constraints

**Known Limitations:**
- Early season (weeks 1-2): insufficient opponent data; use prior season or league average as fallback
- Missing team data files: use league average PPG
- Team code mismatches between game_data.csv and team CSV filenames

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Team Stats Loader
   - **Purpose:** Load and aggregate team PPG from historical data files
   - **Key Components:** CSV file discovery, week-by-week aggregation, team code normalization

2. **Feature 2:** Opponent Strength Calculator Module
   - **Purpose:** Look up DST's weekly opponent; determine matchup difficulty tier
   - **Key Components:** game_data.csv parsing, PPG lookup, tier classification, bye handling

3. **Feature 3:** Scoring Pipeline Integration
   - **Purpose:** Apply opponent strength multiplier to DST score
   - **Key Components:** `_apply_opponent_strength_scoring()` method with current_week parameter

4. **Feature 4:** Configuration (`OPPONENT_STRENGTH_SCORING` block)

5. **Feature 5:** Unit Tests (easy matchup, hard matchup, bye week, missing data fallback)

---

## Dependencies & Risks

### External Dependencies

- **`data/game_data.csv`:** Must be populated with schedule data
- **`data/historical_data/` team CSV files:** Must exist for opponent PPG calculation

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Missing team data files | Medium | Medium | Fallback to league average PPG |
| Early season data scarcity | Medium | High | Use prior season data or league avg for weeks 1-2 |
| Team code mismatches | Low | Medium | Normalize team codes in loader |

---

## Timeline & Resources

**Estimated Timeline:** 3-4 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add opponent strength scoring step for DST
- `data/league_config.json`: Add `OPPONENT_STRENGTH_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/TeamStatsLoader.py`: Load and aggregate team PPG from historical files
- `league_helper/util/OpponentStrengthCalculator.py`: Calculate matchup difficulty for DST

**Coding Practices to Follow:**
- Cache team PPG data per scoring run
- Position guard: DST only
- Graceful file-not-found handling (fallback to league average)
- Type hints, Google docstrings, error_context(), LoggingManager

### Testing Strategy (High-Level)

- **Unit Tests:** Easy matchup (weak opponent) → boost; hard matchup (elite offense) → penalty; bye week → neutral; missing team data → league average; ranking calculation correct
- **Integration Tests:** DST scoring with opponent context produces different results for good vs. bad matchups

---

## Open Questions

1. **Opponent PPG window:** Should we use season PPG or a rolling 4-week average of opponent PPG?
   - **Status:** Unanswered

2. **Extended applicability:** Should this metric also apply to skill position players (boost WRs vs. bad pass defenses)?
   - **Status:** Unanswered

3. **Tie-breaking between PPG and rank:** When PPG and rank thresholds conflict, which takes precedence?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/game_data.csv`, `data/historical_data/`
- **Related Epics:** M41 (Turnover Rate), M42 (Sack Rate), M28 (Game Script Tendency)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Opponent Offensive Strength Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
