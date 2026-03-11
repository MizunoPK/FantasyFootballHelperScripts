# Epic Request: QB Rushing Upside Scoring Integration (M02)

**File Location:** `.shamt/epics/requests/metrics/metric-02-qb-rushing-upside-v2.md`

---

## Epic Overview

**Epic Name:** QB Rushing Upside Scoring Integration (M02)

**Date:** 2026-03-09

**Requested By:** User

**Epic Type:** Feature Implementation

**Estimated Complexity:** Small

---

## Problem Statement

**What problem does this epic solve?**

The player scoring algorithm does not account for QB rushing ability. QBs who run frequently add a significant floor of fantasy points through rushing yards and TDs that standard passing-only evaluations miss. Without this metric, dual-threat QBs are systematically undervalued compared to pocket passers with similar passing stats.

**Why is this important?**

QB rushing upside is a key differentiator in fantasy football. A QB averaging 50+ rushing yards per game provides a guaranteed floor that pocket passers cannot match. Expected improvement: 6-10% in QB recommendation accuracy.

**Who is affected?**

Fantasy managers evaluating or comparing QB players.

---

## Goals & Success Metrics

**Primary Goals:**
1. Implement a QB Rushing Upside calculator that tiers QBs based on rushing yards per game and/or season rushing TDs
2. Integrate the calculator into the player scoring pipeline
3. Configure thresholds and multipliers in the league config

**Success Metrics:**
- Dual-threat QBs (Lamar Jackson type) rank meaningfully higher than equivalent pocket passers
- Expected 6-10% improvement in QB evaluation accuracy
- All unit tests passing

**Out of Scope (Explicitly Not Included):**
- Passing stats (covered by other QB metrics)
- Running back or other position evaluation

---

## Requirements

### Functional Requirements

1. **Rushing Upside Calculation**
   - Calculate rushing yards per game from available weekly data
   - Consider season rushing TDs as a secondary indicator
   - Classify into tiers (EXCELLENT, GOOD, AVERAGE, POOR) using rushing yards/game and/or TD thresholds

2. **Scoring Integration**
   - Apply tier-based multiplier to QB score
   - Require minimum games played before applying adjustment

### Non-Functional Requirements

- **Maintainability:** Thresholds configurable without code changes

### Technical Requirements

- **Dependencies:** `FantasyPlayer` (rushing data), `ConfigManager`
- **Integrations:** `player_scoring.py` scoring pipeline
- **Technology Stack:** Python 3, existing project structure

---

## Research & Background

### Existing Solutions Analysis

**Current State:**
`player_scoring.py` has no QB rushing upside scoring step. QBs are evaluated on passing metrics only.

**Research Findings:**
- `rushing.rush_yds` and `rushing.rush_tds` available in `qb_data.json`
- EXCELLENT threshold: ≥50 rushing yards/game OR ≥6 rushing TDs in a season
- Dual-threat QBs (Lamar Jackson, Josh Allen) consistently outperform projections in fantasy

**Alternative Approaches Considered:**
1. **Rushing yards only:** Misses TDs from short-yardage rushing QBs
2. **Yards + TDs composite (Recommended):** Captures both types of rushing value

### Technical Constraints

**Known Limitations:**
- Sample size: requires minimum games played to avoid early-season noise

---

## Initial Feature Breakdown (Preliminary)

**Proposed Features:**

1. **Feature 1:** QB Rushing Upside Calculator Module
   - **Purpose:** Calculate rushing yards/game and season TDs; return (multiplier, tier)
   - **Key Components:** Calculation logic, dual-threshold tier classification

2. **Feature 2:** Scoring Pipeline Integration
   - **Purpose:** Add rushing upside as a QB-specific scoring step
   - **Key Components:** `_apply_qb_rushing_upside_scoring()` method

3. **Feature 3:** Configuration
   - **Purpose:** Externalize thresholds and multipliers
   - **Key Components:** `QB_RUSHING_UPSIDE_SCORING` config block

4. **Feature 4:** Unit Tests
   - **Purpose:** Verify dual-threat vs. pocket passer differentiation
   - **Key Components:** Elite rusher, minimal rusher, minimum games guard

---

## Dependencies & Risks

### External Dependencies

None beyond existing codebase.

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Position guard needed (QB only) | Low | Low | Check position before calculating |
| Early season noise | Low | Low | Require MIN_GAMES threshold |

---

## Timeline & Resources

**Estimated Timeline:** 2 days

**Team Members Required:**
- Developer: TBD

---

## Implementation Considerations

### Existing Codebase Integration

**Areas of the Codebase That May Require Changes:**
- `league_helper/util/player_scoring.py`: Add `_apply_qb_rushing_upside_scoring()` step
- `data/league_config.json`: Add `QB_RUSHING_UPSIDE_SCORING` config block

**New Areas That May Need Creation:**
- `league_helper/util/QBRushingUpsideCalculator.py`

**Coding Practices to Follow:**
- Follow existing Calculator class pattern
- Type hints, Google docstrings, error_context(), LoggingManager
- Position guard: only applies to QB

### Testing Strategy (High-Level)

- **Unit Tests:** Dual-threat QB gets EXCELLENT tier; pocket passer gets POOR tier; minimum games guard works
- **Integration Tests:** Rushing upside step fires only for QBs

---

## Open Questions

1. **Threshold design:** Should EXCELLENT require both yards AND TDs thresholds, or either one?
   - **Status:** Unanswered

---

## References

- **Related Docs:** `league_helper/util/player_scoring.py`, `data/player_data/qb_data.json`
- **Related Epics:** M03 (Pass Attempts Per Game), M06 (Completion Percentage), M07 (TD:INT Ratio), M12 (QB Quality)
- **External Resources:** N/A

---

## Next Steps

**To proceed with this epic:**
1. User reviews this request
2. User says "Start S1 for QB Rushing Upside Scoring Integration"
3. Agent reads `.shamt/guides/stages/s1/s1_epic_planning.md`
4. Agent creates git branch and FF-{N} folder during S1
5. Agent runs S1 Discovery Phase to refine this request

**This request file remains in `.shamt/epics/requests/` until S1 creates the epic folder.**
