# Epic Request: RB Receiving Workload Scoring Integration (M11)

**File Location:** `.shamt/epics/requests/metrics/metric-11-rb-receiving-workload-v2.md`

---

## Epic Overview

**Epic Name:** RB Receiving Workload Scoring Integration (M11)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for RB receiving workload. In PPR leagues, an RB who receives 7+ targets per game is dramatically more valuable than a pure runner, but current scoring treats them similarly if their carry volume is the same. This leads to systematic undervaluation of receiving backs in PPR formats.

**Why is this important?**

RB receiving workload is a major differentiator in PPR fantasy. Expected improvement: 8-12% in RB evaluation accuracy, especially for identifying PPR-relevant backs.

**Who is affected?**

Fantasy managers in PPR leagues evaluating or comparing RB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement an RB Receiving Workload calculator that tiers RBs by targets per game
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds, multipliers, and minimum games requirements

**Success Metrics:**
- PPR-friendly RBs (8+ targets/game) ranked significantly higher in PPR scoring contexts
- Expected 8-12% improvement in RB accuracy
- INSUFFICIENT_DATA when below minimum games
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Carry volume (covered by M04)
- Overall touch share (covered by M19)

---

## Requirements

### Functional Requirements

1. **Targets Per Game Calculation**
   - Calculate average targets per game, excluding bye weeks
   - Require minimum games (e.g., 6) for valid tier
   - Classify into EXCELLENT (≥8 tgt/game), GOOD (5-7), AVERAGE (3-4), POOR (<3)

2. **Scoring Integration**
   - Apply tier-based multiplier
   - Return neutral for INSUFFICIENT_DATA

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (receiving targets), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No RB receiving workload scoring step exists.

**Research Findings:**
- `receiving.targets` available in `rb_data.json`
- EXCELLENT: ≥8 targets/game (Alvin Kamara, Christian McCaffrey type)
- MIN_GAMES = 6 to ensure meaningful sample

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** RB Receiving Workload Calculator Module
2. **Feature 2:** Scoring Pipeline Integration
3. **Feature 3:** Configuration (`RB_RECEIVING_WORKLOAD_SCORING` block)
4. **Feature 4:** Unit Tests

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Early season noise | Medium | Low | MIN_GAMES = 6 |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add RB receiving workload scoring step
- `data/league_config.json`: Add `RB_RECEIVING_WORKLOAD_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/RBReceivingWorkloadCalculator.py`

**Coding Practices to Follow:**
- Position guard: RB only
- Follow existing Calculator class pattern
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** EXCELLENT for ≥8 targets/game; POOR for minimal receiving; INSUFFICIENT_DATA below MIN_GAMES; bye week exclusion

---

## Open Questions

1. **PPR weighting flag:** Should this metric have a higher weight in PPR leagues than standard scoring?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/rb_data.json`
- **Related Epics:** M01 (Target Volume), M04 (Carries Per Game), M19 (Touch Share)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for RB Receiving Workload Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
