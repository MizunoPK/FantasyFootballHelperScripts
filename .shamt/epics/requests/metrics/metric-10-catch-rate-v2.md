# Epic Request: Catch Rate Scoring Integration (M10)

**File Location:** `.shamt/epics/requests/metrics/metric-10-catch-rate-v2.md`

---

## Epic Overview

**Epic Name:** Catch Rate Scoring Integration (M10)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for catch rate (receptions / targets). A receiver who catches 80% of targets turns opportunities into points reliably, while a 55% catch rate receiver wastes nearly half their targets. In PPR formats especially, catch rate directly predicts floor consistency.

**Why is this important?**

Catch rate measures how efficiently a receiver converts opportunities to production. Expected improvement: 5-8% in WR/TE/RB receiver evaluation accuracy.

**Who is affected?**

Fantasy managers evaluating or comparing WR, TE, and RB players as receivers.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Catch Rate calculator that tiers WR, TE, and RB receivers by catch efficiency
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds, multipliers, and minimum target requirements

**Success Metrics:**
- High catch rate receivers (75%+) ranked higher than equivalent-volume lower-rate receivers
- INSUFFICIENT_DATA when below minimum targets
- 5-8% improvement in receiver evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Target volume (M01)
- Yards per reception (M09)

---

## Requirements

### Functional Requirements

1. **Catch Rate Calculation**
   - Calculate total receptions / total targets
   - Require minimum targets (e.g., 40) for valid tier
   - Classify into EXCELLENT (≥75%), GOOD, AVERAGE, POOR tiers

2. **Scoring Integration**
   - Apply tier-based multiplier
   - Return neutral for INSUFFICIENT_DATA

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (receptions + targets), `ConfigManager`
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No catch rate scoring step exists.

**Research Findings:**
- `receiving.receptions` and `receiving.targets` available in `wr_data.json`, `te_data.json`, `rb_data.json`
- EXCELLENT: ≥75%; MIN_TARGETS = 40

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Catch Rate Calculator Module
2. **Feature 2:** Scoring Pipeline Integration
3. **Feature 3:** Configuration (`CATCH_RATE_SCORING` block)
4. **Feature 4:** Unit Tests

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Small sample noise | Medium | Medium | MIN_TARGETS = 40 |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add catch rate scoring step
- `data/league_config.json`: Add `CATCH_RATE_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/CatchRateCalculator.py`

**Coding Practices to Follow:**
- Position guard: WR, TE, RB
- Follow existing Calculator class pattern
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** EXCELLENT for ≥75%; INSUFFICIENT_DATA below minimum; all three positions tested

---

## Open Questions

1. **Minimum targets:** Is 40 the right threshold, or should it vary by position?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/wr_data.json`, `data/player_data/te_data.json`, `data/player_data/rb_data.json`
- **Related Epics:** M01 (Target Volume), M09 (YPR), M51 (Target Consistency)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Catch Rate Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
