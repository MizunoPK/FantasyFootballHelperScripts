# Epic Request: FG Attempts Per Game Scoring Integration (M46)

**File Location:** `.shamt/epics/requests/metrics/metric-46-fg-attempts-v2.md`

---

## Epic Overview

**Epic Name:** FG Attempts Per Game Scoring Integration (M46)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for kicker FG attempt volume. A kicker who attempts 2.5+ FGs per game has significantly more scoring upside than one with 1.5 attempts, regardless of accuracy. High-accuracy but low-volume kickers are overvalued, while high-volume kickers on teams that stall in the red zone are undervalued.

**Why is this important?**

FG attempt volume is the primary driver of kicker scoring ceiling. Expected improvement: 8-12% in kicker evaluation accuracy, complementing M05 Kicker Accuracy to provide a complete kicker assessment.

**Who is affected?**

Fantasy managers evaluating, drafting, or streaming kickers.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement an FG Attempts Per Game calculator that tiers kickers by attempt volume
2. Accurately detect bye weeks (using extra point activity as confirmation)
3. Integrate into the player scoring pipeline for K position

**Success Metrics:**
- High-volume kickers (2.5+ FGA/game) ranked higher than equivalent-accuracy lower-volume kickers
- Bye weeks correctly excluded from games played count
- 8-12% improvement in kicker evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Kicker accuracy (M05)
- Extra point volume as primary metric

---

## Requirements

### Functional Requirements

1. **FG Attempts Calculation**
   - FG attempts = FG made + FG missed per week
   - Detect active games: any FG attempt OR extra point activity indicates a game was played
   - Weeks with 0 FG attempts and 0 XP activity = bye week, exclude from count
   - Weeks with 0 FG attempts but >0 XP = real game (team scored only TDs)
   - Classify into EXCELLENT (≥2.5), GOOD (2.0-2.49), AVERAGE (1.5-1.99), POOR (1.0-1.49), VERY_POOR (<1.0)
   - Require minimum games for valid tier

2. **Scoring Integration**
   - Apply tier-based multiplier to kicker score

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (field_goals.made, field_goals.missed, extra_points.made, extra_points.missed), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No FG attempts scoring step exists for kickers.

**Research Findings:**
- `field_goals.made`, `field_goals.missed`, `extra_points.made`, `extra_points.missed` available in `k_data.json`
- XP activity used for bye detection is the recommended approach
- EXCELLENT: ≥2.5 FGA/game; VERY_POOR: <1.0 FGA/game

**Alternative Approaches Considered:**
1. **Count all 0-FGA weeks as games:** Inflates denominator with bye weeks
2. **XP-based bye detection (Recommended):** Correctly identifies active games

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** FG Attempts Calculator Module
   - **Purpose:** Calculate FGA/game with XP-based bye detection; return (multiplier, tier)
   - **Key Components:** Attempt calculation, XP activity check, tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add FG attempts as a K-specific scoring step
   - **Key Components:** `_apply_fg_attempts_scoring()` method

3. **Feature 3:** Configuration (`FG_ATTEMPTS_SCORING` block)

4. **Feature 4:** Unit Tests (high-volume K, TD-only game, bye week, low-volume K)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| TD-only game miscounted as bye | Medium | Medium | Check XP activity for game confirmation |
| Early season noise | Low | Low | MIN_GAMES threshold |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add FG attempts scoring step for K
- `data/league_config.json`: Add `FG_ATTEMPTS_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/FGAttemptsCalculator.py`

**Coding Practices to Follow:**
- Position guard: K only
- XP activity check clearly documented as bye detection mechanism
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** EXCELLENT for 2.5+ FGA/game; VERY_POOR for <1.0; TD-only game (0 FGA, XP>0) counted as active; bye (all 0) excluded; INSUFFICIENT_DATA guard

---

## Open Questions

1. **Minimum games:** What is the appropriate minimum: 3 or 5 games?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/k_data.json`
- **Related Epics:** M05 (Kicker Accuracy)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for FG Attempts Per Game Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
