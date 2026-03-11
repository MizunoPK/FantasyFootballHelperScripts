# Epic Request: Boom/Bust Frequency Scoring Integration (M37)

**File Location:** `.shamt/epics/requests/metrics/metric-37-boom-bust-frequency-v2.md`

---

## Epic Overview

**Epic Name:** Boom/Bust Frequency Scoring Integration (M37)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for how often a player significantly exceeds or falls short of their projection. Two players with the same season average can have completely different risk profiles: one might consistently produce near their average (reliable), while another alternates between big games and busts (volatile). Without this metric, high-variance players are not appropriately flagged.

**Why is this important?**

Boom/bust frequency captures outcome variance and reliability, helping managers make risk-adjusted decisions. Expected improvement: 5-8% in weekly lineup optimization by better identifying safe floors vs. high-upside gambles.

**Who is affected?**

Fantasy managers making weekly lineup decisions for all positions.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Boom/Bust Frequency calculator that measures how often a player exceeds/misses projections by 25%+
2. Classify into reliability tiers: BOOM_MACHINE, RELIABLE, AVERAGE, RISKY, BUST_PRONE
3. Integrate into the player scoring pipeline for all positions

**Success Metrics:**
- BOOM_MACHINE players (50%+ boom rate, ≤20% bust rate) ranked higher
- BUST_PRONE players appropriately penalized
- Requires minimum 3 games with projections to produce valid tier
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Recent form direction (M34 covers this)
- Volume-based consistency (M50, M51)

---

## Requirements

### Functional Requirements

1. **Boom/Bust Calculation**
   - Boom = actual points ≥ 125% of projected points in a game
   - Bust = actual points ≤ 75% of projected points in a game
   - Neutral = within 75-125% of projection
   - Exclude games where projected = 0 (no projection available, e.g., bye)
   - Calculate boom rate, bust rate, and boom/bust ratio

2. **Tier Classification**
   - BOOM_MACHINE: boom rate ≥50%, bust rate ≤20%
   - RELIABLE: boom rate ≥35%, bust rate ≤30%
   - AVERAGE: standard variance
   - RISKY: bust rate ≥40%, boom rate <30%
   - BUST_PRONE: bust rate > boom rate and bust rate >40%

3. **Scoring Integration**
   - Apply tier-based multiplier
   - Return neutral for INSUFFICIENT_DATA (<3 games with projections)

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (actual_points + projected_points), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No boom/bust scoring step exists.

**Research Findings:**
- `actual_points` and `projected_points` both available as weekly arrays in all position JSON files
- 25% threshold is standard for boom/bust classification
- MIN_GAMES = 3 for valid tier

**Alternative Approaches Considered:**
1. **Standard deviation of points:** Doesn't capture projection quality
2. **Projection-relative boom/bust (Recommended):** Accounts for expected production level

### Technical Constraints

**Known Limitations:**
- Zero projected_points games must be excluded (bye, unrojected games)
- Low projection games (e.g., projected 2 pts) can artificially register as "boom" with 5 pts

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Boom/Bust Calculator Module
   - **Purpose:** Calculate boom/bust rates; return (multiplier, tier) with reliability classification
   - **Key Components:** 25% threshold application, rate calculation, tier logic, min games guard

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Apply reliability modifier to all positions
   - **Key Components:** `_apply_boom_bust_scoring()` method

3. **Feature 3:** Configuration (`BOOM_BUST_SCORING` block)

4. **Feature 4:** Unit Tests (boom machine, bust prone, zero projection exclusion, min games)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Low-projection game inflates boom rate | Low | Low | Document as known behavior; percentage-based is still valid |
| Insufficient projections data | Medium | Low | MIN_GAMES = 3 guard |

---

## Timeline & Resources

**Estimated Timeline:** 2-3 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add boom/bust scoring step for all positions
- `data/league_config.json`: Add `BOOM_BUST_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/BoomBustCalculator.py`

**Coding Practices to Follow:**
- Applies to all positions (no position guard)
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** BOOM_MACHINE for consistent exceeder; BUST_PRONE for consistent miss; 0-projection week excluded; MIN_GAMES guard; neutral returned for insufficient data

---

## Open Questions

1. **Threshold tuning:** Is 25% above/below projection the right boom/bust threshold?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, all `data/player_data/*_data.json` files
- **Related Epics:** M34 (Recent Form), M50 (Touch Consistency), M51 (Target Consistency)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Boom/Bust Frequency Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
