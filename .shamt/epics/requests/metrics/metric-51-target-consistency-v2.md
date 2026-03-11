# Epic Request: Target Consistency Index Scoring Integration (M51)

**File Location:** `.shamt/epics/requests/metrics/metric-51-target-consistency-v2.md`

---

## Epic Overview

**Epic Name:** Target Consistency Index Scoring Integration (M51)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for how consistently WR and TE players receive targets week to week. Two receivers can average the same targets per game, but one might receive a reliable 9-11 targets every week (floor-dependent in PPR), while the other swings from 2 to 16 targets depending on defensive coverage and game script (volatile). Without this metric, the scoring pipeline cannot distinguish between these meaningfully different risk profiles.

**Why is this important?**

Target consistency predicts weekly floor reliability for receivers in PPR formats. Consistent target volume = predictable scoring floor. Expected improvement: 5-8% in WR/TE floor assessment accuracy.

**Who is affected?**

Fantasy managers evaluating WR and TE players for weekly lineup decisions and trade analysis.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a Target Consistency Index calculator using Coefficient of Variation (CV) of weekly targets
2. Apply WR/TE-specific tier thresholds (slightly higher than RB equivalents in M50, as receivers naturally have more variance)
3. Integrate into the player scoring pipeline

**Success Metrics:**
- Alpha receivers with consistent target share (low CV) ranked higher for reliability
- Deep-threat volatile receivers appropriately flagged
- 5-8% improvement in WR/TE floor assessment
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Touch consistency for RBs (M50 covers this)
- Target volume average (M01 covers this)
- Target share trend direction (M17 covers this)

---

## Requirements

### Functional Requirements

1. **Target Consistency Calculation**
   - Weekly targets from `receiving.targets`
   - Exclude weeks with 0 targets (bye weeks and DNP)
   - Calculate mean and standard deviation of weekly targets
   - Compute CV = std_dev / mean
   - Classify: VERY_CONSISTENT (CV ≤0.18), CONSISTENT (0.19-0.28), MODERATE (0.29-0.40), VOLATILE (0.41-0.55), VERY_VOLATILE (>0.55)
   - Note: WR/TE thresholds are slightly higher than RB M50 thresholds (receivers are naturally more variable)
   - Require minimum 3 active games for valid tier

2. **Scoring Integration**
   - Apply consistency tier multiplier to WR and TE scores

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (receiving.targets), `ConfigManager`, Python `statistics` module
- **Integrations:** `player_scoring.py`

---

## Research & Background

**Current State:** No target consistency scoring step exists.

**Research Findings:**
- `receiving.targets` available in `wr_data.json` and `te_data.json`
- WR/TE thresholds slightly higher than RB (M50) because target distribution is naturally more variable than carry distribution
- CV is appropriate for normalizing across different volume levels (alpha WR with 10 tgt/game vs. slot WR with 6 tgt/game)

**Alternative Approaches Considered:**
1. **Same thresholds as M50:** Ignores the structural difference between carry and target variance
2. **Position-specific WR/TE thresholds (Recommended):** Appropriate calibration for receiver variance patterns

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** Target Consistency Calculator Module
   - **Purpose:** Calculate CV of weekly targets; return (multiplier, tier)
   - **Key Components:** Target aggregation, bye exclusion, mean/std_dev/CV calculation, WR/TE tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add target consistency as a WR/TE scoring step
   - **Key Components:** `_apply_target_consistency_scoring()` method

3. **Feature 3:** Configuration (`TARGET_CONSISTENCY_SCORING` block with 5 tiers)

4. **Feature 4:** Unit Tests (alpha WR, deep threat, TE, minimum games, bye exclusion)

---

## Dependencies & Risks

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Blowout games with low targets inflate volatility | Low | Low | Include — reflects real game script variance |
| CV undefined when mean = 0 | Low | Low | Guard for 0 mean (INSUFFICIENT_DATA) |

---

## Timeline & Resources

**Estimated Timeline:** 2-3 days

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add target consistency scoring step for WR and TE
- `data/league_config.json`: Add `TARGET_CONSISTENCY_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/TargetConsistencyCalculator.py`

**Coding Practices to Follow:**
- Position guard: WR and TE only
- Use Python `statistics.stdev()` for sample std_dev
- Shared implementation with M50 Touch Consistency if architecturally appropriate (same CV pattern)
- Type hints, docstrings, LoggingManager, error_context()

### Testing Strategy (High-Level)

- **Unit Tests:** VERY_CONSISTENT for alpha WR with tight target window; VERY_VOLATILE for deep-threat WR; TE path verified; bye weeks excluded; minimum games guard; WR and TE thresholds different from M50

---

## Open Questions

1. **Shared implementation with M50:** Should Target Consistency and Touch Consistency share a base calculator class, given the similar CV approach?
   - **Status:** Unanswered

2. **TE-specific thresholds:** Should TEs have different thresholds than WRs, given TE usage patterns differ?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `player_scoring.py`, `data/player_data/wr_data.json`, `data/player_data/te_data.json`
- **Related Epics:** M01 (Target Volume), M17 (Target Share Trend), M37 (Boom/Bust Frequency), M50 (Touch Consistency)

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for Target Consistency Index Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
