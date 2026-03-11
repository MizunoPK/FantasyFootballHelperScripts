# Epic Request: Turnover Rate Scoring Integration (M41)

**File Location:** `.shamt/epics/requests/metrics/metric-41-turnover-rate-v2.md`

---

## Epic Overview

**Epic Name:** Turnover Rate Scoring Integration (M41)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for a DST's turnover-generation ability. A defense that produces 2+ turnovers per game directly generates high-value fantasy scoring events (typically 2 points per turnover), while one averaging less than 1 turnover per game misses this bonus. Without this metric, elite playmaking defenses are not sufficiently differentiated from average ones.

**Why is this important?**

Turnovers are high-value fantasy events and a key differentiator among DST units. Expected improvement: 8-12% in DST scoring predictions and streaming decision accuracy.

**Who is affected?**

Fantasy managers evaluating or streaming DST units.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Turnover Rate calculator for DSTs based on interceptions + fumble recoveries per game
2. Apply 5-tier classification (EXCELLENT through VERY_POOR)
3. Integrate into the player scoring pipeline for DST position

**Success Metrics:**
- Elite playmaking DSTs (2.0+ TO/game) scored significantly higher
- VERY_POOR playmakers (<0.5 TO/game) appropriately penalized
- 8-12% improvement in DST evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Sack rate (M42), points allowed, or other DST metrics
- Offensive player evaluation

---

## Requirements

### Functional Requirements

1. **Turnover Rate Calculation**
   - Sum interceptions + fumble recoveries per game
   - Exclude bye weeks by checking for any defensive activity (sacks or turnovers)
   - Calculate turnovers per game across the season
   - Classify into EXCELLENT (≥2.0), GOOD (1.5-1.99), AVERAGE (1.0-1.49), POOR (0.5-0.99), VERY_POOR (<0.5)

2. **Scoring Integration**
   - Apply tier-based multiplier to DST score
   - Require minimum games before applying adjustment

### Non-Functional Requirements

- **Reliability:** Bye week detection must check for game activity, not just zero turnovers (active games can have 0 turnovers)

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (defense.interceptions, defense.fumbles_recovered, defense.sacks), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No turnover rate scoring step exists for DST.

**Research Findings:**
- `defense.interceptions` and `defense.fumbles_recovered` available in `dst_data.json`
- `defense.sacks` also available — useful for detecting whether a 0-turnover week was a bye or an active game
- EXCELLENT threshold: ≥2.0 TO/game

**Alternative Approaches Considered:**
1. **Turnovers only, ignore bye detection:** Risks counting byes as 0-turnover games
2. **Game activity detection via sacks (Recommended):** Accurately identifies active games even with 0 turnovers

### Technical Constraints

**Known Limitations:**
- Turnover volatility is high week-to-week; season average needed for signal
- Some high-turnover games may be outliers (e.g., 6 turnovers) — optional per-game cap may be considered

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Turnover Rate Calculator Module
   - **Purpose:** Calculate turnovers/game with bye week detection; return (multiplier, tier)
   - **Key Components:** INT + fumble recovery sum, game activity detection, tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add turnover rate as a DST-specific scoring step
   - **Key Components:** `_apply_turnover_rate_scoring()` method

3. **Feature 3:** Configuration (`TURNOVER_RATE_SCORING` block with 5 tiers)

4. **Feature 4:** Unit Tests (excellent DST, poor DST, bye week detection, all-zero week vs. active game)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Bye week counted as 0-turnover game | Medium | Medium | Use sack data to detect game activity |
| Extreme outlier game (6+ TOs) | Low | Low | Optional per-game cap configurable in config |

---

## Timeline & Resources

**Estimated Timeline:** 2-3 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add turnover rate scoring step for DST
- `data/league_config.json`: Add `TURNOVER_RATE_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/TurnoverRateCalculator.py`

**Coding Practices to Follow:**
- Position guard: DST only
- Game activity detection logic clearly documented
- Type hints, Google docstrings, error_context(), LoggingManager

### Testing Strategy (High-Level)

- **Unit Tests:** Elite DST (2+ TO/game) → EXCELLENT; poor DST → VERY_POOR; 0-turnover active game not miscounted as bye; min games guard

---

## Open Questions

1. **Turnover cap:** Should individual game turnovers be capped at 4 to reduce outlier impact on the average?
   - **Status:** Unanswered

2. **Turnover TDs:** Should pick-6s and fumble return TDs be tracked separately or as part of this metric?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/dst_data.json`
- **Related Epics:** M42 (Sack Rate), M44 (Opponent Offensive Strength)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Turnover Rate Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
