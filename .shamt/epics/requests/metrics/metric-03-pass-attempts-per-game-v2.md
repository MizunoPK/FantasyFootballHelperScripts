# Epic Request: Pass Attempts Per Game Scoring Integration (M03)

**File Location:** `.shamt/epics/requests/metrics/metric-03-pass-attempts-per-game-v2.md`

---

## Epic Overview

**Epic Name:** Pass Attempts Per Game Scoring Integration (M03)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for QB pass attempt volume. QBs on pass-heavy teams attempt more passes per game, providing more opportunities for fantasy points from completions, yards, and TDs. Without this metric, QBs on run-heavy teams may be overvalued relative to their pass opportunity ceiling.

**Why is this important?**

Pass attempts per game is a strong predictor of QB fantasy production floor. QBs attempting 40+ passes per game have more upside than those at 28 attempts, even if efficiency metrics are similar. Expected improvement: 8-12% in QB evaluation accuracy.

**Who is affected?**

Fantasy managers evaluating or comparing QB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Pass Attempts Per Game calculator that tiers QBs by attempt volume
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds and multipliers in the league config

**Success Metrics:**
- High-volume QBs (40+ att/game) ranked higher than equivalent low-volume QBs
- 8-12% improvement in QB evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Completion percentage (covered by M06)
- Passing yards or TDs as standalone metrics

---

## Requirements

### Functional Requirements

1. **Pass Attempts Calculation**
   - Calculate average pass attempts per game from weekly data
   - Exclude bye weeks from the average
   - Classify into EXCELLENT, GOOD, AVERAGE, POOR tiers

2. **Scoring Integration**
   - Apply tier-based multiplier to QB score
   - Require minimum games/attempts before applying adjustment

### Non-Functional Requirements

- **Maintainability:** Thresholds configurable without code changes

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (passing attempts data), `ConfigManager`
- **Integrations:** `player_scoring.py` scoring pipeline
- **Technology Stack:** Python 3

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
No pass attempts scoring step in `player_scoring.py`.

**Research Findings:**
- `passing.pass_attempts` available in `qb_data.json` as a weekly array
- EXCELLENT threshold: ≥40 attempts/game; POOR threshold: <28 attempts/game
- Pass attempts correlate strongly with fantasy points scored

**Alternative Approaches Considered:**
1. **Passing yards volume:** Combines efficiency and volume — less clean separation
2. **Attempts per game (Recommended):** Pure opportunity measure independent of efficiency

### Technical Constraints

**Known Limitations:**
- Minimum attempts threshold required to avoid small-sample noise for early-season backups

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Pass Attempts Calculator Module
   - **Purpose:** Calculate attempts/game and return (multiplier, tier)
   - **Key Components:** Calculation logic, bye week exclusion, tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add as QB-specific scoring step
   - **Key Components:** `_apply_pass_attempts_scoring()` method

3. **Feature 3:** Configuration
   - **Purpose:** Externalize thresholds and multipliers
   - **Key Components:** `PASS_ATTEMPTS_SCORING` config block

4. **Feature 4:** Unit Tests
   - **Purpose:** Verify tier boundaries and edge cases
   - **Key Components:** High/low volume QBs, bye week handling, minimum threshold

---

## Dependencies & Risks

### External Dependencies

None beyond existing codebase.

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Noisy results early season | Low | Low | MIN_ATTEMPTS threshold |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

**Team Members Required:**
- Developer: TBD

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add pass attempts scoring step
- `data/league_config.json`: Add `PASS_ATTEMPTS_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/PassAttemptsCalculator.py`

**Coding Practices to Follow:**
- Follow existing Calculator class pattern
- Position guard: QB only
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** EXCELLENT tier for 40+ att/game, POOR for <28, bye week exclusion, min threshold guard
- **Integration Tests:** Pass attempts step fires only for QBs

---

## Open Questions

1. **Minimum threshold:** Should minimum be based on attempts total, games played, or both?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/qb_data.json`
- **Related Epics:** M02 (QB Rushing Upside), M06 (Completion Percentage), M12 (QB Quality)
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Pass Attempts Per Game Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
