# Epic Request: Sack Rate Scoring Integration (M42)

**File Location:** `.shamt/epics/requests/metrics/metric-42-sack-rate-v2.md`

---

## Epic Overview

**Epic Name:** Sack Rate Scoring Integration (M42)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for a DST's sack production. A defense averaging 3.5 sacks per game provides a predictable scoring floor (sacks typically worth 1 point each), while a defense with minimal pass rush has less reliable fantasy production. Without this metric, high-sack DSTs are not sufficiently differentiated from average ones.

**Why is this important?**

Sack rate is a more consistent week-to-week metric than turnovers, making it a reliable DST floor predictor. Expected improvement: 6-8% in DST floor prediction accuracy.

**Who is affected?**

Fantasy managers evaluating or streaming DST units.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Sack Rate calculator for DSTs based on sacks per game
2. Apply 5-tier classification (EXCELLENT through VERY_POOR)
3. Integrate into the player scoring pipeline for DST position

**Success Metrics:**
- Elite pass rush DSTs (3.5+ sacks/game) scored higher
- VERY_POOR pass rush DSTs (<1.5 sacks/game) appropriately penalized
- 6-8% improvement in DST evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Turnover rate (M41), points allowed, or other DST metrics
- Offensive player evaluation

---

## Requirements

### Functional Requirements

1. **Sack Rate Calculation**
   - Calculate average sacks per game
   - Detect bye weeks using `pts_g` — if both sacks=0 AND pts_g=0, it's a bye; pts_g>0 with 0 sacks is an active (0-sack) game
   - Classify into EXCELLENT (≥3.5), GOOD (2.8-3.49), AVERAGE (2.0-2.79), POOR (1.5-1.99), VERY_POOR (<1.5)
   - Require minimum games for valid tier (INSUFFICIENT_DATA fallback)

2. **Scoring Integration**
   - Apply tier-based multiplier to DST score

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (defense.sacks, defense.pts_g), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No sack rate scoring step exists for DST.

**Research Findings:**
- `defense.sacks` available in `dst_data.json` as weekly array
- `defense.pts_g` also available — used to distinguish byes (both 0) from active 0-sack games
- EXCELLENT: ≥3.5 sacks/game

**Alternative Approaches Considered:**
1. **Treat all 0-sack weeks as games:** Inflates denominator with bye weeks
2. **pts_g-based bye detection (Recommended):** Accurate identification of active games

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Sack Rate Calculator Module
   - **Purpose:** Calculate sacks/game with accurate bye detection; return (multiplier, tier)
   - **Key Components:** Sack calculation, pts_g-based bye detection, tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add sack rate as a DST-specific scoring step
   - **Key Components:** `_apply_sack_rate_scoring()` method

3. **Feature 3:** Configuration (`SACK_RATE_SCORING` block)

4. **Feature 4:** Unit Tests (elite sacker, weak pass rush, bye detection, 0-sack active game)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Bye detection inaccuracy | Medium | Low | Use pts_g as confirmation of game activity |
| Outlier sack games | Low | Low | Include fully; reflects actual ability |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add sack rate scoring step for DST
- `data/league_config.json`: Add `SACK_RATE_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/SackRateCalculator.py`

**Coding Practices to Follow:**
- Position guard: DST only
- Bye detection logic clearly documented with pts_g check
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** Elite DST → EXCELLENT; weak pass rush → VERY_POOR; 0-sack active game not excluded; bye week correctly excluded; INSUFFICIENT_DATA for <3 games

---

## Open Questions

1. **Minimum games:** Should minimum be 3, 4, or based on a threshold of total sack attempts?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/dst_data.json`
- **Related Epics:** M41 (Turnover Rate), M44 (Opponent Offensive Strength)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Sack Rate Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
