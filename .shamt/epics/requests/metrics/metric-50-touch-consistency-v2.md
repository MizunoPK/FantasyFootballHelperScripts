# Epic Request: Touch Consistency Index Scoring Integration (M50)

**File Location:** `.shamt/epics/requests/metrics/metric-50-touch-consistency-v2.md`

---

## Epic Overview

**Epic Name:** Touch Consistency Index Scoring Integration (M50)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for how consistent an RB's weekly workload is. Two RBs can average the same number of touches per game, but one might receive a consistent 22-24 touches every week (reliable floor) while the other swings from 8 to 30 touches depending on game script (volatile). Without this metric, the scoring pipeline cannot distinguish between these meaningfully different risk profiles.

**Why is this important?**

Touch consistency predicts weekly floor reliability for RBs. Low variance = dependable production. Expected improvement: 5-8% in RB floor/ceiling assessment accuracy.

**Who is affected?**

Fantasy managers evaluating RB players for weekly lineup decisions and trade value.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Touch Consistency Index calculator using Coefficient of Variation (CV) of weekly touches
2. Classify RBs into 5 tiers: VERY_CONSISTENT through VERY_VOLATILE
3. Integrate into the player scoring pipeline

**Success Metrics:**
- Bell cow RBs with low touch variance ranked higher for floor reliability
- Committee backs with high variance appropriately penalized
- 5-8% improvement in RB floor/ceiling assessment
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Target consistency (M51 covers WR/TE)
- Touch volume average (M04, M19 cover volume)

---

## Requirements

### Functional Requirements

1. **Touch Consistency Calculation**
   - Weekly touches = rushing attempts + receiving targets per game
   - Exclude bye weeks (0 touches)
   - Calculate mean and standard deviation of weekly touches
   - Compute Coefficient of Variation (CV = std_dev / mean) — lower CV = more consistent
   - Classify: VERY_CONSISTENT (CV ≤0.15), CONSISTENT (0.16-0.25), MODERATE (0.26-0.35), VOLATILE (0.36-0.50), VERY_VOLATILE (>0.50)
   - Require minimum 3 games for valid tier

2. **Scoring Integration**
   - Apply consistency tier multiplier to RB score

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (rushing.attempts + receiving.targets), `ConfigManager`, Python `statistics` module
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No touch consistency scoring step exists.

**Research Findings:**
- `rushing.attempts` and `receiving.targets` available in `rb_data.json`
- CV is preferable to raw std_dev because it normalizes by mean volume (allows comparison across different workload levels)
- VERY_CONSISTENT: CV ≤0.15 (bell cow predictability); VERY_VOLATILE: CV >0.50 (committee/game-script dependent)

**Alternative Approaches Considered:**
1. **Raw standard deviation:** Can't compare high-volume and low-volume RBs fairly
2. **Coefficient of Variation (Recommended):** Normalizes by mean; comparable across all workload levels

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Touch Consistency Calculator Module
   - **Purpose:** Calculate CV of weekly touches; return (multiplier, tier)
   - **Key Components:** Touch aggregation, bye exclusion, mean/std_dev/CV calculation, tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add touch consistency as an RB-specific scoring step
   - **Key Components:** `_apply_touch_consistency_scoring()` method

3. **Feature 3:** Configuration (`TOUCH_CONSISTENCY_SCORING` block with 5 tiers)

4. **Feature 4:** Unit Tests (bell cow, committee back, minimum games, bye exclusion)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Injury games inflate volatility | Low | Low | Include injury games — that IS the variance being measured |
| CV undefined when mean = 0 | Low | Low | Guard for 0 mean (returns INSUFFICIENT_DATA) |

---

## Timeline & Resources

**Estimated Timeline:** 2-3 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add touch consistency scoring step for RB
- `data/league_config.json`: Add `TOUCH_CONSISTENCY_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/TouchConsistencyCalculator.py`

**Coding Practices to Follow:**
- Position guard: RB only
- Use Python `statistics.stdev()` for sample std_dev (not population)
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** VERY_CONSISTENT for bell cow (low CV); VOLATILE for committee back (high CV); bye weeks excluded; minimum games guard; CV = 0 for perfectly consistent workload

---

## Open Questions

1. **CV thresholds:** Are 0.15/0.25/0.35/0.50 the right tier boundaries, or should they be tuned against real RB data?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/rb_data.json`
- **Related Epics:** M04 (Carries Per Game), M19 (Touch Share), M37 (Boom/Bust Frequency), M51 (Target Consistency)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Touch Consistency Index Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
